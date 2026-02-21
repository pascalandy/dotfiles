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


class SummaryCLIError(Exception):
    """Exception for summary CLI failures (timeout, context limit, etc.)."""

    pass


# Paths (repo-relative by default)
SCRIPT_DIR = Path(__file__).parent.resolve()
DOTENV_PATH = SCRIPT_DIR / ".env"
# Export directory (hardcoded per project conventions)
OUTPUT_DIR = Path("~/Documents/_my_docs/61_transcription_exports_yt").expanduser()

# AI summary providers
PROVIDER_CODEX = "codex"
PROVIDER_CLAUDE = "claude"
VALID_PROVIDERS = (PROVIDER_CODEX, PROVIDER_CLAUDE)
DEFAULT_PROVIDER = PROVIDER_CODEX

# Claude models for prompt summaries
VALID_CLAUDE_MODELS = (
    "claude-opus-4-5",
    "claude-sonnet-4-5",
    "claude-haiku-4-5",
)
DEFAULT_CLAUDE_MODEL = "claude-opus-4-5"

# Codex defaults for prompt summaries
DEFAULT_CODEX_MODEL = "gpt-5.3-codex"
DEFAULT_CODEX_REASONING_EFFORT = "high"
CODEX_SUGGESTED_MODELS = (
    "gpt-5.3-codex",
    "gpt-5.2",
    "gpt-5.2-mini",
    "gpt-5.2-max",
)

DEFAULT_PROMPT = "follow_along_note"

# Claude context limits and summary timeout settings
CLAUDE_SAFE_INPUT_LIMIT = 150_000  # Safe input limit (tokens), leaves room for output
SUMMARY_CLI_TIMEOUT = 600  # 10 minutes (matches SKILL.md recommendation)
SUMMARY_MAX_RETRIES = 3  # Retry attempts for summary CLI failures

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


def validate_context_size(
    transcript_text: str, prompt_text: str
) -> tuple[bool, int, str]:
    """
    Pre-flight validation of combined context size.

    Returns:
        tuple: (is_valid, total_tokens, error_message)
    """
    transcript_tokens = count_tokens(transcript_text)
    prompt_tokens = count_tokens(prompt_text)
    # Overhead for "Based on this transcript:" framing
    overhead_tokens = count_tokens("Based on this transcript:\n\n")

    total_tokens = transcript_tokens + prompt_tokens + overhead_tokens

    if total_tokens > CLAUDE_SAFE_INPUT_LIMIT:
        error_msg = (
            f"Context size ({total_tokens:,} tokens) exceeds safe limit "
            f"({CLAUDE_SAFE_INPUT_LIMIT:,} tokens). "
            f"Transcript: {transcript_tokens:,}, Prompt: {prompt_tokens:,}"
        )
        return False, total_tokens, error_msg

    return True, total_tokens, ""


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


def ensure_cli_available(command_name: str) -> None:
    """Fail fast when a required CLI is missing from PATH."""
    if shutil.which(command_name):
        return
    raise SummaryCLIError(
        f"Required CLI '{command_name}' was not found on PATH. Install it and try again."
    )


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


def get_models_for_provider(provider: str) -> tuple[str, ...]:
    """Return available model names for a summary provider."""
    if provider == PROVIDER_CLAUDE:
        return VALID_CLAUDE_MODELS
    return CODEX_SUGGESTED_MODELS


def resolve_model(provider: str, model_name: str | None) -> str:
    """Resolve model name for the selected provider."""
    if provider == PROVIDER_CLAUDE:
        return (model_name or DEFAULT_CLAUDE_MODEL).lower()
    return model_name or DEFAULT_CODEX_MODEL


def is_valid_model(provider: str, model_name: str) -> bool:
    """Validate model name for the selected provider."""
    if provider == PROVIDER_CLAUDE:
        return model_name in VALID_CLAUDE_MODELS
    return True


def run_summary_prompt(
    provider: str,
    transcript_path: Path,
    prompt_path: Path,
    output_path: Path,
    model_name: str,
) -> dict:
    """Run provider-specific summary generation."""
    if provider == PROVIDER_CLAUDE:
        return run_claude_prompt(transcript_path, prompt_path, output_path, model_name)
    return run_codex_prompt(transcript_path, prompt_path, output_path, model_name)


def print_summary_usage(usage_stats: dict) -> None:
    """Print summary provider usage details."""
    if usage_stats.get("provider") == PROVIDER_CLAUDE:
        console.print(f"[dim]📊 Total: {usage_stats['total_tokens']:,} tokens[/dim]")
        return

    console.print(
        f"[dim]⚙️ {usage_stats['model']} ({usage_stats['reasoning_effort']})[/dim]"
    )


def format_summary_meta(usage_stats: dict | None) -> str:
    """Format summary details saved in meta.txt."""
    if usage_stats and usage_stats.get("provider") == PROVIDER_CLAUDE:
        return (
            "Claude: "
            f"{usage_stats['total_tokens']:,} tokens "
            f"(input: {usage_stats['input_tokens']:,}, output: {usage_stats['output_tokens']:,})"
        )
    if usage_stats and usage_stats.get("provider") == PROVIDER_CODEX:
        return (
            "Codex: "
            f"{usage_stats['model']} "
            f"(reasoning: {usage_stats['reasoning_effort']})"
        )
    return "No AI summary"


def run_claude_prompt(
    transcript_path: Path, prompt_path: Path, output_path: Path, model_name: str
) -> dict:
    """
    Run Claude CLI with transcript and prompt, save output.

    Uses --system-prompt for the prompt template to reduce user message tokens.
    Includes timeout protection and retry logic.

    Returns:
        dict with usage stats: {"input_tokens": int, "output_tokens": int, "total_tokens": int}

    Raises:
        SummaryCLIError: If Claude CLI fails after retries or context limit exceeded.
    """
    ensure_cli_available("claude")

    transcript_content = transcript_path.read_text(encoding="utf-8")
    prompt_content = prompt_path.read_text(encoding="utf-8")

    # Pre-flight validation
    is_valid, total_tokens, error_msg = validate_context_size(
        transcript_content, prompt_content
    )
    if not is_valid:
        raise SummaryCLIError(error_msg)

    console.print(f"[dim]Context: {total_tokens:,} tokens (input)[/dim]")

    # User message: just the transcript content
    user_message = f"Based on this transcript:\n\n{transcript_content}"

    def _run_claude() -> subprocess.CompletedProcess:
        """Inner function for retry wrapper."""
        return subprocess.run(
            [
                "claude",
                "-p",
                "--dangerously-skip-permissions",
                "--model",
                model_name,
                "--tools",
                "",  # Disable all tools - forces text output only
                "--output-format",
                "json",  # Get usage stats
                "--system-prompt",
                prompt_content,
                user_message,
            ],
            capture_output=True,
            text=True,
            check=True,
            timeout=SUMMARY_CLI_TIMEOUT,
        )

    try:
        result = retry_request(_run_claude, max_attempts=SUMMARY_MAX_RETRIES)
    except subprocess.TimeoutExpired:
        raise SummaryCLIError(
            f"Claude CLI timed out after {SUMMARY_CLI_TIMEOUT} seconds. "
            "The transcript may be too long or the model may be overloaded."
        )
    except subprocess.CalledProcessError as e:
        raise SummaryCLIError(f"Claude CLI failed: {e.stderr or e.stdout or str(e)}")

    # Parse JSON response
    try:
        response_data = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        raise SummaryCLIError(f"Failed to parse Claude response: {e}")

    # Validate expected schema (claude --output-format json returns {result, usage, ...})
    if "result" not in response_data:
        raise SummaryCLIError(
            f"Unexpected Claude JSON schema. Expected 'result' field. "
            f"Got keys: {list(response_data.keys())}"
        )

    # Extract content and usage
    content = response_data["result"]
    usage = response_data.get("usage", {})

    # Claude splits input tokens across multiple fields (caching)
    input_tokens = (
        usage.get("input_tokens", 0)
        + usage.get("cache_creation_input_tokens", 0)
        + usage.get("cache_read_input_tokens", 0)
    )
    output_tokens = usage.get("output_tokens", 0)

    # Save the actual content (not the JSON)
    output_path.write_text(content, encoding="utf-8")

    return {
        "provider": PROVIDER_CLAUDE,
        "model": model_name,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
    }


def run_codex_prompt(
    transcript_path: Path, prompt_path: Path, output_path: Path, model_name: str
) -> dict:
    """Run Codex CLI with transcript and prompt, save markdown output."""
    ensure_cli_available("codex")

    transcript_content = transcript_path.read_text(encoding="utf-8")
    prompt_content = prompt_path.read_text(encoding="utf-8")
    user_message = (
        f"{prompt_content.strip()}\n\nBased on this transcript:\n\n{transcript_content}"
    )

    codex_output_path = output_path.parent / ".tmp_codex_last_message.md"

    def _run_codex() -> subprocess.CompletedProcess:
        return subprocess.run(
            [
                "codex",
                "exec",
                "--skip-git-repo-check",
                "--sandbox",
                "read-only",
                "--model",
                model_name,
                "--config",
                f'model_reasoning_effort="{DEFAULT_CODEX_REASONING_EFFORT}"',
                "--output-last-message",
                str(codex_output_path),
                "-",
            ],
            input=user_message,
            stdout=subprocess.PIPE,
            text=True,
            check=True,
            timeout=SUMMARY_CLI_TIMEOUT,
            stderr=subprocess.DEVNULL,
        )

    try:
        result = retry_request(_run_codex, max_attempts=SUMMARY_MAX_RETRIES)
    except subprocess.TimeoutExpired:
        raise SummaryCLIError(
            f"Codex CLI timed out after {SUMMARY_CLI_TIMEOUT} seconds. "
            "The transcript may be too long or the model may be overloaded."
        )
    except subprocess.CalledProcessError as e:
        details = e.stdout.strip() if e.stdout else str(e)
        raise SummaryCLIError(f"Codex CLI failed: {details}")

    output_text = ""
    if codex_output_path.exists():
        output_text = codex_output_path.read_text(encoding="utf-8").strip()
        codex_output_path.unlink(missing_ok=True)

    if not output_text:
        output_text = (result.stdout or "").strip()

    if not output_text:
        raise SummaryCLIError("Codex CLI returned empty output.")

    output_path.write_text(f"{output_text}\n", encoding="utf-8")

    return {
        "provider": PROVIDER_CODEX,
        "model": model_name,
        "reasoning_effort": DEFAULT_CODEX_REASONING_EFFORT,
    }


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

Default (transcript + follow_along_note prompt via Codex):
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
        "--provider",
        choices=VALID_PROVIDERS,
        default=DEFAULT_PROVIDER,
        help=f"Summary provider (default: {DEFAULT_PROVIDER})",
    )
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
        type=str,
        default=None,
        metavar="MODEL",
        help=(
            "Model name. Defaults: "
            f"codex={DEFAULT_CODEX_MODEL}, claude={DEFAULT_CLAUDE_MODEL}"
        ),
    )
    options_group.add_argument(
        "--list-prompts",
        action="store_true",
        help="List available prompts",
    )
    options_group.add_argument(
        "--list-models",
        action="store_true",
        help="List available models for the selected provider",
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
        for model in get_models_for_provider(args.provider):
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

    selected_model = resolve_model(args.provider, args.model)
    if not is_valid_model(args.provider, selected_model):
        console.print(
            "[red]Invalid Claude model:[/red] "
            f"{selected_model}. Use --list-models --provider claude"
        )
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

    # Run summary prompt if selected
    summary_path: Path | None = None
    usage_stats: dict | None = None
    if selected_prompt:
        with Status(
            f"[cyan]Generating summary with {args.provider}...[/cyan]", console=console
        ):
            try:
                output_file = output_dir / selected_prompt["filename"]
                transcript_file = output_dir / "raw_transcript.txt"

                usage_stats = run_summary_prompt(
                    args.provider,
                    transcript_file,
                    selected_prompt["path"],
                    output_file,
                    selected_model,
                )

                summary_path = output_file
                console.print(f"[green]🧠 {selected_prompt['filename']}[/green]")
                print_summary_usage(usage_stats)
            except SummaryCLIError as e:
                console.print(f"[red]{args.provider} error:[/red] {e}")

    console.print()
    console.print(f"[dim]📂 {output_dir}[/dim]")

    # Save meta.txt
    date_str = datetime.now().strftime("%Y_%m_%d %Hh%M")
    tokens_info = format_summary_meta(usage_stats)
    meta_content = f"""Title: {info["title"]}
Date: {date_str}
URL: {args.url}
{tokens_info}
"""
    (output_dir / "meta.txt").write_text(meta_content, encoding="utf-8")

    # Open folder
    open_folder(output_dir)
    if summary_path:
        console.print()
        render_markdown_with_glow(summary_path)


if __name__ == "__main__":
    main()
