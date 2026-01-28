#!/usr/bin/env uv run python3
# /// script
# dependencies = [
#     "requests",
#     "python-dotenv",
#     "tiktoken",
#     "yt-dlp",
#     "rich",
# ]
# ///
"""
YouTube Transcript Generator with Deepgram API.

Downloads YouTube audio, transcribes with Deepgram nova-3,
and outputs timestamped transcripts in multiple formats.
"""

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import requests
import tiktoken
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.status import Status

# Paths (repo-relative by default)
SCRIPT_DIR = Path(__file__).parent.resolve()
DOTENV_PATH = SCRIPT_DIR / ".env"
# Expected location: <repo>/.opencode/skill/transcript/scripts/transcript.py
PROJECT_ROOT = SCRIPT_DIR.parents[3]
# Export directory (hardcoded per project conventions)
OUTPUT_DIR = Path("~/Documents/_my_docs/61_transcription_exports_yt").expanduser()

# Claude models for prompt summaries
VALID_CLAUDE_MODELS = (
    "claude-opus-4-5",
    "claude-sonnet-4-5",
    "claude-haiku-4-5",
)
DEFAULT_CLAUDE_MODEL = "claude-opus-4-5"
DEFAULT_PROMPT = "follow_along_note"

console = Console()


def retry_request(func, max_attempts: int = 3, initial_delay: float = 1.0):
    """Execute function with exponential backoff retry logic."""
    delay = initial_delay
    last_exception = None

    for attempt in range(1, max_attempts + 1):
        try:
            if attempt > 1:
                console.print(f"   [yellow]Retry {attempt}/{max_attempts}...[/yellow]")
            return func()
        except Exception as e:
            last_exception = e
            if attempt == max_attempts:
                console.print(f"   [red]Failed after {max_attempts} attempts[/red]")
                raise last_exception from None  # type: ignore[reportGeneralTypeIssues]
            console.print(f"   [yellow]Failed, retrying in {delay}s...[/yellow]")
            time.sleep(delay)

    raise last_exception  # type: ignore[reportGeneralTypeIssues]


def get_video_info(url: str) -> dict:
    """Get video title and ID using yt-dlp."""
    # Try without cookies first (works for public videos)
    result = subprocess.run(
        ["yt-dlp", "--get-title", "--get-id", url],
        capture_output=True,
        text=True,
    )
    # Fall back to cookies if needed
    if result.returncode != 0:
        result = subprocess.run(
            [
                "yt-dlp",
                "--cookies-from-browser",
                "chrome",
                "--get-title",
                "--get-id",
                url,
            ],
            capture_output=True,
            text=True,
            check=True,
        )
    elif not result.stdout.strip():
        raise ValueError("Could not retrieve video info")

    lines = result.stdout.strip().split("\n")
    if len(lines) < 2:
        raise ValueError("Could not retrieve video title and ID")

    title = lines[0]
    video_id = lines[1]

    if not title or title == "NA":
        raise ValueError("Video may be private, deleted, or unavailable")

    return {"title": title, "video_id": video_id}


def clean_title(title: str) -> str:
    """Clean video title for filesystem use."""
    cleaned = re.sub(r"[^a-zA-Z0-9 ]", "", title)
    cleaned = cleaned.replace(" ", "_")
    return cleaned[:50]


def create_output_dir(title: str, video_id: str) -> Path:
    """Create timestamped output directory."""
    date_formatted = datetime.now().strftime("%Y_%m_%d_%Hh%M")
    cleaned_title = clean_title(title)
    dir_name = f"{date_formatted}_{cleaned_title}_{video_id}"
    output_dir = Path(OUTPUT_DIR) / dir_name
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def download_audio(url: str, output_dir: Path) -> Path:
    """Download audio from YouTube as MP3."""
    output_template = str(output_dir / "audio.%(ext)s")
    # Try without cookies first (works for public videos)
    result = subprocess.run(
        [
            "yt-dlp",
            "-x",
            "--audio-format",
            "mp3",
            "--audio-quality",
            "0",
            "-o",
            output_template,
            url,
        ],
        capture_output=True,
    )
    # Fall back to cookies if needed
    if result.returncode != 0:
        subprocess.run(
            [
                "yt-dlp",
                "--cookies-from-browser",
                "chrome",
                "-x",
                "--audio-format",
                "mp3",
                "--audio-quality",
                "0",
                "-o",
                output_template,
                url,
            ],
            check=True,
            capture_output=True,
        )
    audio_path = output_dir / "audio.mp3"
    if not audio_path.exists():
        raise FileNotFoundError("Audio download failed")
    return audio_path


def transcribe_audio(audio_path: Path, api_key: str) -> dict:
    """Transcribe audio using Deepgram API (nova-3 model)."""
    url = "https://api.deepgram.com/v1/listen"
    params = {
        "model": "nova-3",
        "detect_language": "true",
        "punctuate": "true",
        "paragraphs": "true",
    }
    headers = {
        "Authorization": f"Token {api_key}",
        "Content-Type": "audio/mp3",
    }

    with open(audio_path, "rb") as audio_file:
        response = requests.post(
            url, params=params, headers=headers, data=audio_file, timeout=300
        )

    response.raise_for_status()
    result = response.json()

    if "error" in result:
        raise ValueError(f"Deepgram error: {result['error']}")

    return result


def parse_transcript(response: dict) -> tuple[str, str, str]:
    """Parse Deepgram response into different output formats."""
    channel = response["results"]["channels"][0]["alternatives"][0]

    # Plain text transcript
    transcript_text = channel["transcript"]

    # Timestamped sentences
    sentences_lines = []
    paragraphs = channel.get("paragraphs", {}).get("paragraphs", [])
    for paragraph in paragraphs:
        for sentence in paragraph.get("sentences", []):
            start = int(sentence["start"])
            end = int(sentence["end"])
            text = sentence["text"]
            sentences_lines.append(f"[{start}s - {end}s] {text}")
    sentences_text = "\n".join(sentences_lines)

    # JSON data (paragraphs structure)
    json_data = json.dumps(paragraphs, indent=2)

    return transcript_text, sentences_text, json_data


def save_outputs(
    output_dir: Path, transcript: str, sentences: str, json_data: str
) -> dict[str, Path]:
    """Save all output files."""
    files = {}

    transcript_path = output_dir / "raw_transcript.txt"
    transcript_path.write_text(transcript, encoding="utf-8")
    files["transcript"] = transcript_path

    sentences_path = output_dir / "raw_sentences.txt"
    sentences_path.write_text(sentences, encoding="utf-8")
    files["sentences"] = sentences_path

    json_path = output_dir / "raw_transcript.json"
    json_path.write_text(json_data, encoding="utf-8")
    files["json"] = json_path

    return files


def count_tokens(text: str) -> int:
    """Count tokens using tiktoken (cl100k_base encoding)."""
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


def get_token_counts(output_dir: Path) -> dict[str, int]:
    """Get token counts for all output files."""
    counts = {}
    for filename in ["raw_transcript.txt", "raw_sentences.txt", "raw_transcript.json"]:
        filepath = output_dir / filename
        if filepath.exists():
            content = filepath.read_text(encoding="utf-8")
            counts[filename] = count_tokens(content)
    return counts


def open_folder(path: Path) -> None:
    """Open folder in Finder (macOS) or print path."""
    if platform.system() == "Darwin":
        subprocess.run(["open", str(path)], check=False)


def render_markdown_with_glow(markdown_path: Path) -> None:
    """Render a markdown file in the terminal using glow (if available)."""
    if not markdown_path.exists():
        return

    markdown_text = markdown_path.read_text(encoding="utf-8")

    if not shutil.which("glow"):
        console.print("[dim]glow not found; rendering markdown with rich[/dim]")
        console.print("[dim]Install glow: brew install glow[/dim]")
        console.print(Markdown(markdown_text))
        return

    result = subprocess.run(
        ["glow", f"./{markdown_path.name}"],
        cwd=str(markdown_path.parent),
        check=False,
    )
    if result.returncode != 0:
        console.print("[yellow]glow failed; rendering markdown with rich[/yellow]")
        console.print(Markdown(markdown_text))


def get_api_key_from_keyring() -> str | None:
    """Retrieve Deepgram API key from macOS keyring via chezmoi."""
    try:
        result = subprocess.run(
            [
                "chezmoi",
                "secret",
                "keyring",
                "get",
                "--service=deepgram",
                "--user=api_key",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip() or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def validate_env() -> str:
    """Get Deepgram API key from keyring or environment."""
    # Try keyring first
    api_key = get_api_key_from_keyring()

    # Fall back to environment variable
    if not api_key:
        api_key = os.getenv("DEEPGRAM_API_KEY")

    if not api_key:
        console.print("[red]Missing Deepgram API key[/red]")
        console.print("Add to macOS keyring:")
        console.print("  chezmoi secret keyring set --service=deepgram --user=api_key")
        console.print("")
        console.print("Or set DEEPGRAM_API_KEY environment variable")
        sys.exit(1)

    return api_key


def validate_youtube_url(url: str) -> bool:
    """Validate YouTube URL format."""
    patterns = [
        r"^https?://(www\.)?youtube\.com/watch\?v=[\w-]+",
        r"^https?://youtu\.be/[\w-]+",
        r"^https?://(www\.)?youtube\.com/shorts/[\w-]+",
    ]
    return any(re.match(pattern, url) for pattern in patterns)


def scan_prompts(prompts_dir: Path) -> list[dict]:
    """Scan prompts directory for bundled prompt files."""
    prompts = []
    if not prompts_dir.exists():
        return prompts

    for prompt_file in sorted(prompts_dir.glob("*.md")):
        prompts.append(
            {
                "name": prompt_file.stem,
                "filename": prompt_file.name,
                "path": prompt_file,
            }
        )

    return prompts


def normalize_prompt_name(name: str) -> str:
    """Normalize a prompt name for matching."""
    normalized = name.strip()
    if normalized.lower().endswith(".md"):
        normalized = normalized[:-3]
    return normalized.lower()


def resolve_prompt(prompts: list[dict], name: str) -> dict:
    """Resolve a bundled prompt by filename stem (case-insensitive)."""
    target = normalize_prompt_name(name)
    for prompt in prompts:
        if prompt["name"].lower() == target:
            return prompt

    available = ", ".join(p["name"] for p in prompts) if prompts else "none"
    raise ValueError(f"Unknown prompt '{name}'. Available prompts: {available}")


def run_claude_prompt(
    transcript_path: Path, prompt_path: Path, output_path: Path, model_name: str
) -> None:
    """Run Claude CLI with transcript and prompt, save output."""
    transcript_content = transcript_path.read_text(encoding="utf-8")
    prompt_content = prompt_path.read_text(encoding="utf-8")

    full_prompt = f"Based on this transcript:\n\n{transcript_content}\n\nFollow these instructions:\n\n{prompt_content}"

    result = subprocess.run(
        [
            "claude",
            "-p",
            "--dangerously-skip-permissions",
            "--model",
            model_name,
            full_prompt,
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    output_path.write_text(result.stdout, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    # Load env early to check API key status for help
    load_dotenv(dotenv_path=DOTENV_PATH)
    api_key_status = (
        "set"
        if (get_api_key_from_keyring() or os.getenv("DEEPGRAM_API_KEY"))
        else "NOT SET"
    )

    parser = argparse.ArgumentParser(
        description=f"""YouTube Transcript Generator from Deepgram

Default (transcript + follow_along_note prompt):
  uv run %(prog)s "https://youtu.be/dQw4w9WgXcQ"
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage=argparse.SUPPRESS,
        epilog=f"""
Output files (in timestamped folder):
  {{prompt}}.md, raw_transcript.txt, raw_sentences.txt, raw_transcript.json, meta.txt

Environment:
  DEEPGRAM_API_KEY  [{api_key_status}]
""",
        add_help=False,
    )
    parser.add_argument("-h", "--help", action="help", help=argparse.SUPPRESS)
    required_group = parser.add_argument_group("Required argument")
    required_group.add_argument(
        "url",
        nargs="?",
        help="YouTube URL",
    )
    options_group = parser.add_argument_group("Options")
    options_group.add_argument(
        "--no-prompt",
        action="store_true",
        help="Transcript only, skip AI summary",
    )
    options_group.add_argument(
        "--prompt",
        nargs="?",
        const=DEFAULT_PROMPT,
        default=DEFAULT_PROMPT,
        metavar="NAME",
        help=f"Use different prompt (default: {DEFAULT_PROMPT})",
    )
    options_group.add_argument(
        "--model",
        type=str.lower,
        choices=VALID_CLAUDE_MODELS,
        default=DEFAULT_CLAUDE_MODEL,
        metavar="MODEL",
        help=f"Claude model (default: {DEFAULT_CLAUDE_MODEL})",
    )
    options_group.add_argument(
        "--list-prompts",
        action="store_true",
        help="List available prompts",
    )
    options_group.add_argument(
        "--list-models",
        action="store_true",
        help="List available models",
    )
    # Show help if no arguments provided
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    if not (args.list_prompts or args.list_models) and not args.url:
        parser.error(
            "the following arguments are required: url (unless --list-prompts or --list-models is used)"
        )

    return args


def main() -> None:
    """Main workflow."""
    # Load environment
    load_dotenv(dotenv_path=DOTENV_PATH)
    args = parse_args()
    prompts = scan_prompts(SCRIPT_DIR / "prompts")

    if args.list_models:
        for model in VALID_CLAUDE_MODELS:
            console.print(model)

    if args.list_prompts:
        for prompt in prompts:
            console.print(prompt["name"])
    if args.list_models or args.list_prompts:
        return

    selected_prompt = None
    if args.prompt and not args.no_prompt:
        try:
            selected_prompt = resolve_prompt(prompts, args.prompt)
        except ValueError as e:
            console.print(f"[red]{e}[/red]")
            sys.exit(1)

    api_key = validate_env()

    # Validate URL
    if not validate_youtube_url(args.url):
        console.print(f"[red]Invalid YouTube URL:[/red] {args.url}")
        sys.exit(1)

    console.print()

    # Get video info
    with Status("[cyan]Fetching video info...[/cyan]", console=console):
        try:
            info = retry_request(lambda: get_video_info(args.url))
        except subprocess.CalledProcessError:
            console.print("[red]Failed to get video info[/red]")
            sys.exit(1)

    console.print(f"[bold green]🎬 {info['title']}[/bold green]")
    console.print()

    # Create output directory
    output_dir = create_output_dir(info["title"], info["video_id"])

    # Download audio
    with Status("[cyan]Downloading audio...[/cyan]", console=console):
        try:
            audio_path = retry_request(lambda: download_audio(args.url, output_dir))
        except subprocess.CalledProcessError:
            console.print("[red]Failed to download audio[/red]")
            sys.exit(1)
    console.print("[green]⬇️  Downloaded[/green]")

    # Transcribe
    with Status("[cyan]Transcribing with Deepgram...[/cyan]", console=console):
        try:
            response = retry_request(lambda: transcribe_audio(audio_path, api_key))
        except requests.RequestException as e:
            console.print(f"[red]Transcription failed:[/red] {e}")
            sys.exit(1)
    console.print("[green]📝 Transcribed[/green]")

    # Parse and save
    transcript, sentences, json_data = parse_transcript(response)
    save_outputs(output_dir, transcript, sentences, json_data)

    # Cleanup audio
    audio_path.unlink()

    # Run Claude prompt if selected
    summary_path: Path | None = None
    if selected_prompt:
        with Status("[cyan]Generating summary...[/cyan]", console=console):
            tmp_transcript = SCRIPT_DIR / "tmp_transcript.txt"
            shutil.copy(output_dir / "raw_transcript.txt", tmp_transcript)

            try:
                output_file = output_dir / selected_prompt["filename"]
                run_claude_prompt(
                    tmp_transcript,
                    selected_prompt["path"],
                    output_file,
                    args.model,
                )
                summary_path = output_file
                console.print(f"[green]🧠 {selected_prompt['filename']}[/green]")
            except subprocess.CalledProcessError as e:
                console.print(f"[red]Failed to generate summary:[/red] {e.stderr}")
            finally:
                if tmp_transcript.exists():
                    tmp_transcript.unlink()

    # Token counts
    counts = get_token_counts(output_dir)
    labels = ["transcript txt", "sentences txt", "transcript json"]
    tokens_str = " | ".join(
        f"{v:,} ({label})" for v, label in zip(counts.values(), labels, strict=True)
    )
    console.print()
    console.print(f"[dim]📊 Tokens: {tokens_str}[/dim]")
    console.print(f"[dim]📂 {output_dir}[/dim]")

    # Save meta.txt
    date_str = datetime.now().strftime("%Y_%m_%d %Hh%M")
    meta_content = f"""Title: {info["title"]}
Date: {date_str}
URL: {args.url}
Tokens: {tokens_str}
"""
    (output_dir / "meta.txt").write_text(meta_content, encoding="utf-8")

    # Open folder
    open_folder(output_dir)
    if summary_path:
        console.print()
        render_markdown_with_glow(summary_path)


if __name__ == "__main__":
    main()
