#!/usr/bin/env uv run python3
# /// script
# dependencies = [
# ]
# ///
"""
Secure Password Generator with part1_part2_part3 structure.

Usage:
    uv run python3 password_generator.py
    uv run python3 password_generator.py --length 32
    uv run python3 password_generator.py --count 3 --copy
    chmod +x password_generator.py, then: ./password_generator.py

Examples:
    uv run python3 password_generator.py
    uv run python3 password_generator.py --length 20 --count 3
    uv run python3 password_generator.py --no-clipboard

Features:
- Secure Randomness: Uses secrets module for cryptographically secure random generation
- User-Friendly Character Set: Excludes visually ambiguous characters (I, O, l, o)
- Clear Structure: part1_part2_part3 format with underscores as separators
- Clipboard Integration: Automatically copies last password if clipboard tools available
- Error Handling: Validates input parameters and handles edge cases
- Configurable: Adjustable length, count, and clipboard behavior

Character Set:
- Uppercase: A B C D E F G H J K L M N P Q R S T U V W X Y Z (No I, O)
- Lowercase: a b c d e f g h j k m n p q r s t u v w x y z (No l, o)
- Digits:    0 1 2 3 4 5 6 7 8 9
- Symbol:    _ (Used only as a separator between parts)
"""

import argparse
import secrets
import shutil
import subprocess
import sys

# Configuration constants
DEFAULT_LENGTH = 28
DEFAULT_COUNT = 10
PART1_LEN = 4
PART3_LEN = 4

# Safe character set - excludes visually ambiguous characters
SAFE_CHARS = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz0123456789"


def validate_clipboard_tool() -> str:
    """
    Check for available clipboard tools and return the command name.

    Returns:
        str: Command name for clipboard tool ('pbcopy', 'xclip', or 'none')
    """
    if shutil.which("pbcopy"):
        return "pbcopy"
    elif shutil.which("xclip"):
        return "xclip"
    else:
        return "none"


def generate_random_part(length: int) -> str:
    """
    Generate a random string of specified length using safe character set.

    Args:
        length: Desired length of the random part

    Returns:
        str: Random string using SAFE_CHARS
    """
    if length <= 0:
        return ""

    # Generate random characters using secrets module
    return "".join(secrets.choice(SAFE_CHARS) for _ in range(length))


def generate_password(total_length: int) -> str:
    """
    Generate a password in part1_part2_part3 format.

    Args:
        total_length: Total desired length including underscores

    Returns:
        str: Generated password in part1_part2_part3 format

    Raises:
        ValueError: If total_length is invalid
    """
    # Validate total length
    min_length = PART1_LEN + PART3_LEN + 2  # 4 + 4 + 2 = 10
    if total_length < min_length:
        raise ValueError(
            f"Total length must be at least {min_length} to accommodate part1, part3, and separators"
        )

    if not isinstance(total_length, int) or total_length <= 0:
        raise ValueError("Total length must be a positive integer")

    # Calculate length for middle part
    part2_len = total_length - PART1_LEN - PART3_LEN - 2

    # Generate each part
    part1 = generate_random_part(PART1_LEN)
    part2 = generate_random_part(part2_len)
    part3 = generate_random_part(PART3_LEN)

    # Combine with underscores
    return f"{part1}_{part2}_{part3}"


def copy_to_clipboard(password: str, clipboard_tool: str) -> bool:
    """
    Copy password to system clipboard.

    Args:
        password: Password string to copy
        clipboard_tool: Name of clipboard tool to use

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if clipboard_tool == "pbcopy":
            subprocess.run(["pbcopy"], input=password, text=True, check=True)
            return True
        elif clipboard_tool == "xclip":
            subprocess.run(
                ["xclip", "-selection", "clipboard"],
                input=password,
                text=True,
                check=True,
            )
            return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    return False


def main():
    """Main function with argument parsing."""
    parser = argparse.ArgumentParser(
        description="Generate secure passwords with part1_part2_part3 structure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Generate 5 passwords with default length (28)
  %(prog)s --length 32        # Generate with custom length
  %(prog)s --count 3          # Generate 3 passwords
  %(prog)s --no-clipboard     # Disable clipboard copying
  %(prog)s --length 20 --count 2 --copy

Character Set:
  Uppercase: A-HJ-NP-Z (excludes I, O)
  Lowercase: a-kmnp-z (excludes l, o)
  Digits:    0-9
  Separator: _ (underscore only)

Security Features:
  - Uses secrets module for cryptographically secure random generation
  - Excludes visually ambiguous characters
  - Structured format for easy typing and reading
        """,
    )

    parser.add_argument(
        "--length",
        type=int,
        default=DEFAULT_LENGTH,
        help=f"Total password length including underscores (min: {PART1_LEN + PART3_LEN + 2}, default: {DEFAULT_LENGTH})",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=DEFAULT_COUNT,
        help=f"Number of passwords to generate (default: {DEFAULT_COUNT})",
    )
    parser.add_argument(
        "--no-clipboard",
        action="store_true",
        help="Disable automatic clipboard copying",
    )
    parser.add_argument(
        "--copy",
        action="store_true",
        help="Force clipboard copying (override auto-detection)",
    )

    args = parser.parse_args()

    # Validate arguments
    min_length = PART1_LEN + PART3_LEN + 2
    if args.length < min_length:
        print(f"Error: Length must be at least {min_length}", file=sys.stderr)
        sys.exit(1)

    if args.count < 1:
        print("Error: Count must be at least 1", file=sys.stderr)
        sys.exit(1)

    if args.count > 100:
        print("Error: Maximum count is 100 passwords", file=sys.stderr)
        sys.exit(1)

    # Determine clipboard behavior
    clipboard_tool = validate_clipboard_tool()
    should_copy = not args.no_clipboard and (args.copy or clipboard_tool != "none")

    print("🔐 Secure Password Generator")
    print("=" * 50)
    print(f"Length: {args.length} characters")
    print(f"Count: {args.count} passwords")
    print(f"Format: {PART1_LEN} chars + '_' + middle + '_' + {PART3_LEN} chars")
    print(f"Character set: {len(SAFE_CHARS)} safe characters (no I, O, l, o)")
    if should_copy:
        print(f"Clipboard: {clipboard_tool}")
    else:
        print("Clipboard: Disabled")
    print()

    # Generate passwords
    passwords = []
    for i in range(args.count):
        try:
            password = generate_password(args.length)
            passwords.append(password)
            print(f"[{i+1:2d}] {password}")
        except ValueError as e:
            print(f"Error generating password {i+1}: {e}", file=sys.stderr)
            sys.exit(1)

    # Copy last password to clipboard if requested
    if should_copy and passwords:
        last_password = passwords[-1]
        if copy_to_clipboard(last_password, clipboard_tool):
            print("\n✅ Last password copied to clipboard!")
        else:
            print(
                f"\n⚠️  Failed to copy to clipboard (tool: {clipboard_tool})",
                file=sys.stderr,
            )
    elif not should_copy:
        print("\n💡 Tip: Use --copy to enable clipboard integration", file=sys.stderr)

    print(f"\n🔒 Generated {len(passwords)} secure password(s)")


if __name__ == "__main__":
    main()
