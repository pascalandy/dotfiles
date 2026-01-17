#!/usr/bin/env uv run python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["mistralai", "python-dotenv", "tenacity"]
# ///
"""
Convert PDF/images to Markdown using Mistral OCR.

Usage:
    uv run scripts/mistral_ocr.py input.pdf -o output_mistral.md
    uv run scripts/mistral_ocr.py input.pdf --dry-run
    uv run scripts/mistral_ocr.py input.pdf --timeout 600
"""

import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv
from mistralai import Mistral
from mistralai.models import DocumentURLChunk
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

# Constants
SUPPORTED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".gif", ".webp"}
FILE_SIZE_WARNING_MB = 50
DEFAULT_TIMEOUT_SECONDS = 300
MAX_RETRIES = 3


def get_mime_type(file_path: Path) -> str:
    """Get MIME type based on file extension."""
    suffix = file_path.suffix.lower()
    mime_types = {
        ".pdf": "application/pdf",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    return mime_types.get(suffix, "application/octet-stream")


def validate_file(file_path: Path) -> tuple[bool, str | None]:
    """Validate file exists, is readable, non-empty, and supported type."""
    if not file_path.exists():
        return False, f"File not found: {file_path}"

    if not file_path.is_file():
        return False, f"Not a file: {file_path}"

    if file_path.stat().st_size == 0:
        return False, f"File is empty: {file_path}"

    if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        return (
            False,
            f"Unsupported file type: {file_path.suffix}. Supported: {supported}",
        )

    return True, None


def check_file_size(file_path: Path) -> None:
    """Warn if file exceeds threshold."""
    size_mb = file_path.stat().st_size / (1024 * 1024)
    if size_mb > FILE_SIZE_WARNING_MB:
        print(
            f"Warning: File is {size_mb:.1f} MB (>{FILE_SIZE_WARNING_MB} MB). "
            "Processing may take longer.",
            file=sys.stderr,
        )


def get_api_key() -> str | None:
    """Load API key from .env or environment."""
    import os

    script_dir = Path(__file__).parent.parent
    load_dotenv(script_dir / ".env")
    return os.environ.get("MISTRAL_API_KEY")


def mask_api_key(key: str) -> str:
    """Mask API key for display."""
    if len(key) <= 8:
        return "***"
    return f"{key[:3]}...{key[-4:]}"


def dry_run(
    file_path: Path,
    output_path: Path,
    timeout: int,
    table_format: str,
    include_images: bool,
) -> None:
    """Print what would happen without executing."""
    size_mb = file_path.stat().st_size / (1024 * 1024)
    mime_type = get_mime_type(file_path)
    api_key = get_api_key()

    print("Dry run mode - no API calls will be made\n")
    print(f"Input:  {file_path.absolute()}")
    print(f"Size:   {size_mb:.2f} MB", end="")
    if size_mb > FILE_SIZE_WARNING_MB:
        print(f" (warning: >{FILE_SIZE_WARNING_MB} MB)")
    else:
        print()
    print(f"Type:   {mime_type}")
    print(f"Output: {output_path.absolute()}")
    print()
    print("Settings:")
    print(f"  Timeout:        {timeout}s")
    print(f"  Table format:   {table_format}")
    print(f"  Include images: {'yes' if include_images else 'no'}")
    print(f"  Max retries:    {MAX_RETRIES}")
    print()
    if api_key:
        print(f"API Key: Found ({mask_api_key(api_key)})")
    else:
        print("API Key: NOT FOUND")
    print()
    print("Ready to process.")


def process_ocr(
    file_path: Path,
    output_path: Path,
    table_format: str = "markdown",
    include_images: bool = True,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
) -> None:
    """Process file with Mistral OCR and save result."""
    api_key = get_api_key()
    if not api_key:
        print("Error: MISTRAL_API_KEY not set in .env or environment", file=sys.stderr)
        sys.exit(1)

    check_file_size(file_path)

    client = Mistral(api_key=api_key, timeout_ms=timeout * 1000)
    uploaded_file = None

    try:
        # Upload file to Mistral
        uploaded_file = client.files.upload(
            file={"file_name": file_path.name, "content": file_path.read_bytes()},
            purpose="ocr",
        )

        # Get signed URL
        signed_url = client.files.get_signed_url(file_id=uploaded_file.id, expiry=1)

        # Process OCR with retry logic
        ocr_response = _call_ocr_with_retry(
            client=client,
            signed_url=signed_url.url,
            table_format=table_format,
            include_images=include_images,
        )

        # Extract markdown from pages with error handling
        pages_text = []
        for i, page in enumerate(ocr_response.pages or []):
            if hasattr(page, "markdown") and page.markdown:
                pages_text.append(page.markdown)
            else:
                print(f"Warning: Page {i + 1} has no markdown content", file=sys.stderr)

        if not pages_text:
            print("Error: No content extracted from document", file=sys.stderr)
            sys.exit(1)

        text = "\n\n".join(pages_text)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text)
        print(f"Saved: {output_path}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    finally:
        # Cleanup: delete uploaded file from Mistral servers
        if uploaded_file:
            try:
                client.files.delete(file_id=uploaded_file.id)
            except Exception as e:
                print(
                    f"Warning: Could not delete temp file from server: {e}",
                    file=sys.stderr,
                )


@retry(
    stop=stop_after_attempt(MAX_RETRIES),
    wait=wait_exponential(multiplier=1, min=2, max=30),
    retry=retry_if_exception_type((TimeoutError, ConnectionError)),
    reraise=True,
)
def _call_ocr_with_retry(
    client: Mistral,
    signed_url: str,
    table_format: str,
    include_images: bool,
):
    """Call OCR API with retry logic."""
    return client.ocr.process(
        model="mistral-ocr-latest",
        document=DocumentURLChunk(document_url=signed_url),
        table_format=table_format,  # type: ignore[arg-type]
        include_image_base64=include_images,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert PDF/images to Markdown using Mistral OCR",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.pdf                    # Output to input_mistral.md
  %(prog)s input.pdf -o output.md       # Output to specific file
  %(prog)s input.pdf --dry-run          # Show what would happen
  %(prog)s input.pdf --timeout 600      # Set 10 minute timeout
  %(prog)s image.png --no-images        # Exclude embedded images
        """,
    )
    parser.add_argument("input", type=Path, help="Input PDF or image file")
    parser.add_argument("-o", "--output", type=Path, help="Output markdown file")
    parser.add_argument(
        "--table-format",
        choices=["markdown", "html"],
        default="markdown",
        help="Table format (default: markdown)",
    )
    parser.add_argument(
        "--no-images",
        action="store_true",
        help="Exclude base64 images from output",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without calling the API",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT_SECONDS,
        help=f"Request timeout in seconds (default: {DEFAULT_TIMEOUT_SECONDS})",
    )

    args = parser.parse_args()

    # Validate input file
    valid, error = validate_file(args.input)
    if not valid:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)

    output = args.output or args.input.with_name(f"{args.input.stem}_mistral.md")

    if args.dry_run:
        dry_run(
            file_path=args.input,
            output_path=output,
            timeout=args.timeout,
            table_format=args.table_format,
            include_images=not args.no_images,
        )
        return

    process_ocr(
        args.input,
        output,
        table_format=args.table_format,
        include_images=not args.no_images,
        timeout=args.timeout,
    )


if __name__ == "__main__":
    main()
