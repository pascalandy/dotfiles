#!/usr/bin/env python3
import subprocess
from pathlib import Path


SKIP_PARTS = {".git", "node_modules", "__pycache__"}


def iter_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        yield path


def classify(path: Path):
    path_str = str(path)
    if path.name == "SKILL.md" and "/skill/" in path_str:
        return "skill"
    if path.suffix == ".md" and (
        ".opencode/agent/" in path_str or "/dot_config/opencode/agent/" in path_str
    ):
        return "agent"
    if path.suffix == ".md" and (
        ".opencode/command/" in path_str or "/dot_config/opencode/command/" in path_str
    ):
        return "command"
    return None


def git_status():
    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
        return result.stdout.splitlines()
    except Exception:
        return []


def main():
    inventory = {"agent": [], "command": [], "skill": []}

    for path in iter_files(Path(".")):
        kind = classify(path)
        if kind:
            inventory[kind].append(str(path))

    print("OpenCode Inventory")
    print("=" * 40)
    for kind in ("agent", "command", "skill"):
        print(f"{kind.title()}s: {len(inventory[kind])}")
        for item in sorted(inventory[kind])[:10]:
            print(f"- {item}")
        if len(inventory[kind]) > 10:
            print(f"- ... and {len(inventory[kind]) - 10} more")
        print()

    changed = [line for line in git_status() if line.strip()]
    if changed:
        print("Changed files:")
        for line in changed[:20]:
            print(f"- {line}")
        if len(changed) > 20:
            print(f"- ... and {len(changed) - 20} more")
        print()

    print("Review the changed resources above and update docs only where the inventory actually changed.")


if __name__ == "__main__":
    main()
