#!/usr/bin/env uv run python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "openai",
#     "typer",
#     "rich",
#     "python-dotenv",
#     "pillow",
# ]
# ///
"""
Generate images using OpenRouter API with Gemini 3 Pro Image model.

Requires OPENROUTER_API_KEY in environment or .env file.

Examples:
    # Show help
    uv run gen_image.py --help

    # Dry run (no API call)
    uv run gen_image.py --dry-run --prompt "A sunset over mountains"

    # Generate with default settings
    uv run gen_image.py --prompt "A sunset over mountains"

    # Generate multiple images
    uv run gen_image.py --prompt "A sunset" --nbr-img-output 3

    # Edit existing image
    uv run gen_image.py --prompt "Make sky more dramatic" --input-image photo.jpg

    # Quiet mode (only output path)
    uv run gen_image.py --prompt "A sunset" --quiet
"""

import base64
import os
import platform
import subprocess
import sys
import traceback
from datetime import datetime
from io import BytesIO
from pathlib import Path

import typer
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image
from rich.console import Console
from rich.panel import Panel

# Constants
__version__ = "1.0.0"
MODEL_NAME = "google/gemini-3-pro-image-preview"
API_BASE_URL = "https://openrouter.ai/api/v1"

app = typer.Typer(
    help="Generate images using OpenRouter API (Gemini 3 Pro Image)\n\nDocs: https://github.com/pascalandy/forzr/blob/main/.opencode/skill/nano-banana-pro-3/SKILL.md",
    no_args_is_help=True,
)

# Global console - will be configured per-command
console = Console()
console_stderr = Console(file=sys.stderr)


def get_api_key() -> str | None:
    """Get API key from .env, then environment."""
    # Load .env from script directory and current directory
    script_dir = Path(__file__).parent.parent
    load_dotenv(script_dir / ".env")
    load_dotenv()  # Also check current directory

    return os.environ.get("OPENROUTER_API_KEY")


def _open_file(filepath: str, quiet: bool = False) -> None:
    """Open file with default application (cross-platform)."""
    try:
        if platform.system() == "Darwin":
            # macOS
            subprocess.run(["open", filepath], check=True)
        elif platform.system() == "Windows":
            # Windows - use os.startfile instead of subprocess with shell=True
            os.startfile(filepath)  # type: ignore[attr-defined]
        else:
            # Linux and others
            subprocess.run(["xdg-open", filepath], check=True)
    except (subprocess.CalledProcessError, FileNotFoundError, OSError) as e:
        if not quiet:
            console_stderr.print(f"[yellow]Warning:[/yellow] Could not open file: {e}")


def generate_default_filename(index: int = 1, file_format: str = "png") -> str:
    """Generate timestamped filename, optionally with index for multiple images."""
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    ext = "jpeg" if file_format.lower() == "jpeg" else "png"
    if index == 1:
        return f"{timestamp}-generated.{ext}"
    else:
        return f"{timestamp}-generated-{index}.{ext}"


def save_image_from_base64(
    data_url: str, output_path: Path, file_format: str = "png"
) -> None:
    """Extract base64 image data and save as PNG or JPEG."""
    # data_url format: "data:image/png;base64,<base64_data>"
    base64_data = data_url.split(",", 1)[1] if "," in data_url else data_url

    image_bytes = base64.b64decode(base64_data)
    image = Image.open(BytesIO(image_bytes))

    # Convert to RGB if needed
    if image.mode == "RGBA":
        rgb_image = Image.new("RGB", image.size, (255, 255, 255))
        rgb_image.paste(image, mask=image.split()[3])
    elif image.mode == "RGB":
        rgb_image = image
    else:
        rgb_image = image.convert("RGB")

    # Save with format
    save_format = "JPEG" if file_format.lower() == "jpeg" else "PNG"
    rgb_image.save(str(output_path), save_format)


def load_image_as_base64(image_path: Path) -> str:
    """Load an image file and convert to base64 data URL."""
    with Image.open(image_path) as img:
        # Convert to RGB if needed
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        b64_data = base64.b64encode(buffer.read()).decode("utf-8")
        return f"data:image/png;base64,{b64_data}"


# Valid image sizes and aspect ratios
VALID_SIZES = ["1K", "2K", "4K"]
VALID_ASPECT_RATIOS = [
    "1:1",  # 1024x1024 (default)
    "2:3",  # 832x1248
    "3:2",  # 1248x832
    "3:4",  # 864x1184
    "4:3",  # 1184x864
    "4:5",  # 896x1152
    "5:4",  # 1152x896
    "9:16",  # 768x1344
    "16:9",  # 1344x768
    "21:9",  # 1536x672
]


@app.command()
def generate(
    version: bool = typer.Option(
        False,
        "--version",
        "-V",
        help="Show version and exit",
        is_eager=True,
    ),
    prompt: str = typer.Option(
        None,
        "--prompt",
        "-p",
        help="Image description or editing instructions",
    ),
    filename: str = typer.Option(
        None,
        "--filename",
        "-f",
        help="Output filename (default: timestamped)",
    ),
    input_image: list[str] = typer.Option(  # noqa: B008
        [],
        "--input-image",
        "-i",
        help="Input image path(s) for editing/modification (multiple allowed, up to 14)",
    ),
    size: str = typer.Option(
        "1K",
        "--size",
        "-s",
        help="Image size: 1K (default), 2K, or 4K",
    ),
    aspect_ratio: str = typer.Option(
        None,
        "--aspect-ratio",
        "-a",
        help="Aspect ratio: 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9",
    ),
    seed: int = typer.Option(
        None,
        "--seed",
        help="Seed for reproducible results",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        "-n",
        help="Show what would be done without making API call",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Debug output with API request/response details",
    ),
    nbr_img_output: int = typer.Option(
        1,
        "--nbr-img-output",
        "-c",
        min=1,
        max=4,
        help="Number of images to generate (1-4)",
    ),
    format: str = typer.Option(
        "png",
        "--format",
        "-F",
        help="Output format: png, jpeg",
    ),
    thinking: str = typer.Option(
        None,
        "--thinking",
        "-t",
        help="Thinking mode: low, medium, high",
    ),
    negative_prompt: str = typer.Option(
        None,
        "--negative-prompt",
        "-N",
        help="What to avoid in generation",
    ),
    safety: str = typer.Option(
        None,
        "--safety",
        help="Safety filter level: off, low, medium, high",
    ),
    output_dir: str = typer.Option(
        "./EXPORT",
        "--output-dir",
        "-o",
        help="Output directory for generated images",
    ),
    open_after: bool = typer.Option(
        False,
        "--open-after",
        help="Open image(s) after generation",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Suppress non-essential output (only show file paths)",
    ),
    timeout: int = typer.Option(
        120,
        "--timeout",
        help="API request timeout in seconds (default: 120)",
    ),
    no_color: bool = typer.Option(
        False,
        "--no-color",
        help="Disable colored output",
    ),
) -> None:
    """Generate or edit an image from a text prompt.

    Examples:
        uv run gen_image.py --prompt "A sunset over mountains"
        uv run gen_image.py --prompt "Edit sky" --input-image photo.jpg
    """

    # Initialize consoles with NO_COLOR support (before any output)
    no_color_env = os.environ.get("NO_COLOR") is not None
    no_color_final = no_color or no_color_env
    console.no_color = no_color_final
    console_stderr.no_color = no_color_final

    # Handle version flag
    if version:
        console.print(__version__)
        raise typer.Exit(0)

    # Validate prompt is provided
    if not prompt:
        console_stderr.print("[red]Error:[/red] --prompt is required")
        raise typer.Exit(2)

    # Validate size
    size_upper = size.upper()
    if size_upper not in VALID_SIZES:
        console_stderr.print(
            f"[red]Error:[/red] Invalid size '{size}'. Must be one of: {', '.join(VALID_SIZES)}"
        )
        raise typer.Exit(2)

    # Validate format
    format_lower = format.lower()
    if format_lower not in ["png", "jpeg"]:
        console_stderr.print(
            f"[red]Error:[/red] Invalid format '{format}'. Must be 'png' or 'jpeg'"
        )
        raise typer.Exit(2)

    # Validate thinking mode if provided
    if thinking and thinking.lower() not in ["low", "medium", "high"]:
        console_stderr.print(
            f"[red]Error:[/red] Invalid thinking mode '{thinking}'. Must be 'low', 'medium', or 'high'"
        )
        raise typer.Exit(2)

    # Validate safety filter if provided
    if safety and safety.lower() not in ["off", "low", "medium", "high"]:
        console_stderr.print(
            f"[red]Error:[/red] Invalid safety level '{safety}'. Must be 'off', 'low', 'medium', or 'high'"
        )
        raise typer.Exit(2)

    # Validate aspect ratio if provided
    if aspect_ratio and aspect_ratio not in VALID_ASPECT_RATIOS:
        console_stderr.print(
            f"[red]Error:[/red] Invalid aspect ratio '{aspect_ratio}'."
        )
        console_stderr.print(f"Valid options: {', '.join(VALID_ASPECT_RATIOS)}")
        raise typer.Exit(2)

    # Validate input images if provided
    input_image_paths: list[Path] = []
    if input_image:
        if len(input_image) > 14:
            console_stderr.print(
                f"[red]Error:[/red] Maximum 14 input images allowed, got {len(input_image)}"
            )
            raise typer.Exit(2)

        for img_path_str in input_image:
            img_path = Path(img_path_str)
            if not img_path.exists():
                console_stderr.print(
                    f"[red]Error:[/red] Input image not found: {img_path_str}"
                )
                raise typer.Exit(2)
            input_image_paths.append(img_path)

    # Resolve API key
    resolved_key = get_api_key()

    # Resolve output directory
    output_dir_path = Path(output_dir)

    # Resolve filename (handle multiple images)
    if filename and nbr_img_output > 1:
        # For multiple images with custom filename, append index
        base_filename = Path(filename).stem
        file_ext = Path(filename).suffix
        output_paths = [
            output_dir_path / f"{base_filename}-{i}{file_ext}"
            for i in range(1, nbr_img_output + 1)
        ]
    elif filename:
        # If filename is an absolute path, use it as-is; otherwise put it in output_dir
        filename_path = Path(filename)
        if filename_path.is_absolute():
            output_paths = [filename_path]
        else:
            output_paths = [output_dir_path / filename]
    else:
        # Multiple images with default timestamped names in output_dir
        output_paths = [
            output_dir_path / generate_default_filename(i, format_lower)
            for i in range(1, nbr_img_output + 1)
        ]

    output_path = output_paths[0]  # Use first for display

    # Determine mode
    if input_image_paths:
        mode = "Editing" if len(input_image_paths) == 1 else "Composing/Blending"
    else:
        mode = "Generating"

    # Dry run output (always show even in quiet mode as it's critical feedback)
    if dry_run:
        console_stderr.print(
            Panel.fit(
                "[bold cyan]DRY RUN[/bold cyan] - No API call will be made",
                title="Mode",
            )
        )
        if not quiet:
            console_stderr.print(f"[bold]Mode:[/bold] {mode}")
            if input_image_paths:
                if len(input_image_paths) == 1:
                    console_stderr.print(
                        f"[bold]Input Image:[/bold] {input_image_paths[0].resolve()}"
                    )
                else:
                    console_stderr.print(
                        f"[bold]Input Images ({len(input_image_paths)}):[/bold]"
                    )
                    for img_path in input_image_paths:
                        console_stderr.print(f"  - {img_path.resolve()}")
            console_stderr.print(f"[bold]Prompt:[/bold] {prompt}")
            if negative_prompt:
                console_stderr.print(f"[bold]Negative Prompt:[/bold] {negative_prompt}")
            if nbr_img_output > 1:
                console_stderr.print(f"[bold]Number of Images:[/bold] {nbr_img_output}")
                console_stderr.print("[bold]Output Files:[/bold]")
                for p in output_paths:
                    console_stderr.print(f"  - {p.resolve()}")
            else:
                console_stderr.print(f"[bold]Output:[/bold] {output_path.resolve()}")
            console_stderr.print(f"[bold]Size:[/bold] {size_upper}")
            console_stderr.print(
                f"[bold]Aspect Ratio:[/bold] {aspect_ratio or '1:1 (default)'}"
            )
            console_stderr.print(f"[bold]Format:[/bold] {format_lower}")
            console_stderr.print(
                f"[bold]Output Directory:[/bold] {output_dir_path.resolve()}"
            )
            if thinking:
                console_stderr.print(f"[bold]Thinking Mode:[/bold] {thinking.lower()}")
            if safety:
                console_stderr.print(f"[bold]Safety Filter:[/bold] {safety.lower()}")
            if open_after:
                console_stderr.print("[bold]Open After:[/bold] Yes")
            if seed is not None:
                console_stderr.print(f"[bold]Seed:[/bold] {seed}")
            console_stderr.print(
                f"[bold]API Key:[/bold] {'[green]SET[/green]' if resolved_key else '[red]NOT SET[/red]'}"
            )
            console_stderr.print(f"[bold]Model:[/bold] {MODEL_NAME}")
            console_stderr.print(f"[bold]Endpoint:[/bold] {API_BASE_URL}")

        if verbose:
            console_stderr.print(
                "\n[bold cyan][DEBUG][/bold cyan] Request Body (would be sent):"
            )
            image_config = {"image_size": size_upper}
            if aspect_ratio:
                image_config["aspect_ratio"] = aspect_ratio

            content = prompt
            if input_image_paths:
                content = f"[{len(input_image_paths)} image(s) + text prompt]"

            request_body = {
                "model": MODEL_NAME,
                "messages": [
                    {
                        "role": "user",
                        "content": content,
                    }
                ],
                "modalities": ["image", "text"],
                "image_config": image_config,
            }
            if seed is not None:
                request_body["extra_body"] = {"seed": seed}

            import json

            console_stderr.print(json.dumps(request_body, indent=2))

        return

    # Validate API key
    if not resolved_key:
        console_stderr.print("[red]Error:[/red] No API key provided.")
        console_stderr.print("Set OPENROUTER_API_KEY in .env or environment variable.")
        console_stderr.print("Get your key at: https://openrouter.ai/keys")
        raise typer.Exit(1)

    # Create output directory if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not quiet:
        console_stderr.print(
            f"[bold]{mode} {nbr_img_output} image{'s' if nbr_img_output > 1 else ''}...[/bold]"
        )
        if input_image_paths:
            if len(input_image_paths) == 1:
                console_stderr.print(f"  Input: {input_image_paths[0]}")
            else:
                console_stderr.print(f"  Inputs ({len(input_image_paths)}):")
                for img_path in input_image_paths:
                    console_stderr.print(f"    - {img_path}")
        console_stderr.print(f"  Prompt: {prompt}")
        if negative_prompt:
            console_stderr.print(f"  Negative Prompt: {negative_prompt}")
        console_stderr.print(f"  Output Dir: {output_dir_path.resolve()}")
        console_stderr.print(f"  Size: {size_upper}")
        if aspect_ratio:
            console_stderr.print(f"  Aspect Ratio: {aspect_ratio}")
        console_stderr.print(f"  Format: {format_lower}")
        if thinking:
            console_stderr.print(f"  Thinking: {thinking.lower()}")
        if safety:
            console_stderr.print(f"  Safety: {safety.lower()}")
        if seed is not None:
            console_stderr.print(f"  Seed: {seed}")
        if nbr_img_output > 1:
            for p in output_paths:
                console_stderr.print(f"  Output: {p}")
        else:
            console_stderr.print(f"  Output: {output_path}")

    try:
        client = OpenAI(
            base_url=API_BASE_URL,
            api_key=resolved_key,
            timeout=timeout,
        )

        # Build image_config
        image_config = {"image_size": size_upper}
        if aspect_ratio:
            image_config["aspect_ratio"] = aspect_ratio

        # Build message content
        # Prepare prompt with negative prompt if provided
        full_prompt = prompt
        if negative_prompt:
            full_prompt = f"{prompt}. Avoid including: {negative_prompt}"

        if input_image_paths:
            # Image editing/composition: send image(s) + prompt
            message_content = []
            for img_path in input_image_paths:
                image_data_url = load_image_as_base64(img_path)
                message_content.append(
                    {
                        "type": "image_url",
                        "image_url": {"url": image_data_url},
                    }
                )
            message_content.append(
                {
                    "type": "text",
                    "text": full_prompt,
                }
            )
        else:
            # Text-to-image generation
            message_content = full_prompt

        # Build extra_body
        extra_body = {
            "modalities": ["image", "text"],
            "image_config": image_config,
        }
        if seed is not None:
            extra_body["seed"] = seed
        if thinking:
            # Map thinking mode to effort level
            effort_map = {
                "low": "low",
                "medium": "medium",
                "high": "high",
            }
            extra_body["reasoning"] = {
                "effort": effort_map.get(thinking.lower(), "medium")
            }

        if safety:
            # Add safety filter settings to extra_body
            extra_body["safety_settings"] = {
                "category_harm_enabled": safety.lower() != "off"
            }

        if verbose:
            console_stderr.print("\n[bold cyan][DEBUG][/bold cyan] API Request:")
            console_stderr.print(f"  Model: {MODEL_NAME}")
            console_stderr.print(f"  Endpoint: {API_BASE_URL}/chat/completions")

        # Make API call with progress spinner
        if console_stderr.is_terminal:
            with console_stderr.status(
                f"[bold]{mode}...{' (this may take a minute)' if not quiet else ''}",
                spinner="dots",
            ):
                try:
                    response = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=[
                            {
                                "role": "user",
                                "content": message_content,
                            }
                        ],
                        extra_body=extra_body,
                    )
                except KeyboardInterrupt:
                    if not quiet:
                        console_stderr.print("\n[yellow]Interrupted by user[/yellow]")
                    raise typer.Exit(130) from None
        else:
            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {
                            "role": "user",
                            "content": message_content,
                        }
                    ],
                    extra_body=extra_body,
                )
            except KeyboardInterrupt:
                if not quiet:
                    console_stderr.print("\n[yellow]Interrupted by user[/yellow]")
                raise typer.Exit(130) from None

        message = response.choices[0].message

        if verbose:
            console_stderr.print("[bold cyan][DEBUG][/bold cyan] Response received")
            if hasattr(message, "images") and message.images:
                console_stderr.print(f"  Images in response: {len(message.images)}")

        # Check for images in response
        if hasattr(message, "images") and message.images:
            num_to_save = min(len(message.images), nbr_img_output)
            for idx in range(num_to_save):
                image_data = message.images[idx]
                image_url = image_data["image_url"]["url"]
                current_output_path = output_paths[idx]
                save_image_from_base64(image_url, current_output_path, format_lower)

                if verbose:
                    # Get image size from saved file
                    img = Image.open(current_output_path)
                    size_mb = current_output_path.stat().st_size / (1024 * 1024)
                    console_stderr.print(
                        f"  Image {idx + 1}: {img.width}x{img.height} pixels, {size_mb:.1f} MB"
                    )

                # Output path to stdout (data output)
                console.print(str(current_output_path.resolve()))

                if not quiet:
                    console.print("[green]Image saved[/green]")

            # Open images if requested
            if open_after:
                for output_p in output_paths[:num_to_save]:
                    try:
                        _open_file(str(output_p), quiet)
                    except Exception as e:
                        if not quiet:
                            console_stderr.print(
                                f"[yellow]Warning:[/yellow] Could not open image: {e}"
                            )
        else:
            # Fallback: check content for text response
            if message.content:
                console_stderr.print(
                    f"[yellow]Model response:[/yellow] {message.content}"
                )
            console_stderr.print(
                "[red]Error:[/red] No image was generated in the response."
            )
            raise typer.Exit(1)

    except KeyboardInterrupt:
        if not quiet:
            console_stderr.print("\n[yellow]Interrupted by user[/yellow]")
        raise typer.Exit(130) from None
    except Exception as e:
        console_stderr.print(f"[red]Error generating image:[/red] {e}")
        if verbose:
            traceback.print_exc(file=sys.stderr)
        raise typer.Exit(1) from e


if __name__ == "__main__":
    app()
