#!/usr/bin/env python3
import re
import sys
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


def parse_frontmatter(content: str):
    match = re.match(r"^---\n(.*?)\n---\n?", content, re.DOTALL)
    if not match:
        return None
    return match.group(1)


def get_field(frontmatter: str, field: str):
    block = re.search(
        rf"^{field}:\s*\|-\n((?:(?:[ \t]+.*)|(?:\s*))*(?:\n|$))",
        frontmatter,
        re.MULTILINE,
    )
    if block:
        lines = block.group(1).splitlines()
        non_empty = [line for line in lines if line.strip()]
        if not non_empty:
            return ""
        indent = min(len(line) - len(line.lstrip()) for line in non_empty)
        return "\n".join(line[indent:] if line.strip() else "" for line in lines).strip()

    match = re.search(rf"^{field}:\s*(.+)$", frontmatter, re.MULTILINE)
    if match:
        value = match.group(1).strip()
        if value[:1] in {"\"", "'"} and value[-1:] == value[:1]:
            return value[1:-1]
        return value
    return None


def count_examples(text: str):
    return len(re.findall(r'user:\s*["\'].+?["\']\s*->', text, re.IGNORECASE))


def audit_skill(path: Path, frontmatter: str):
    errors = []
    warnings = []
    name = get_field(frontmatter, "name")
    description = get_field(frontmatter, "description")

    if not name:
        errors.append("missing `name` field")
    if not description:
        errors.append("missing `description` field")
        return errors, warnings

    if name and name != path.parent.name:
        warnings.append(f"`name` does not match directory: {name} vs {path.parent.name}")
    if "use for" not in description.lower() and "use when" not in description.lower():
        warnings.append("skill description should include a `Use for` or `Use when` clause")
    if count_examples(description) < 2:
        warnings.append("skill description should include at least two trigger examples")

    return errors, warnings


def audit_agent(frontmatter: str):
    errors = []
    description = get_field(frontmatter, "description")
    if not description:
        errors.append("missing `description` field")
    return errors, []


def audit_command(frontmatter: str):
    errors = []
    warnings = []
    description = get_field(frontmatter, "description")
    if not description:
        errors.append("missing `description` field")
        return errors, warnings
    if len(description.split()) > 7:
        warnings.append("command description should stay short")
    return errors, warnings


def main():
    totals = {"agent": 0, "command": 0, "skill": 0}
    findings = {"errors": [], "warnings": []}

    for path in iter_files(Path(".")):
        kind = classify(path)
        if not kind:
            continue

        totals[kind] += 1
        content = path.read_text(encoding="utf-8", errors="ignore")
        frontmatter = parse_frontmatter(content)
        if not frontmatter:
            findings["errors"].append((path, "missing YAML frontmatter"))
            continue

        if kind == "skill":
            errors, warnings = audit_skill(path, frontmatter)
        elif kind == "agent":
            errors, warnings = audit_agent(frontmatter)
        else:
            errors, warnings = audit_command(frontmatter)

        for item in errors:
            findings["errors"].append((path, item))
        for item in warnings:
            findings["warnings"].append((path, item))

    print("OpenCode Repository Audit")
    print("=" * 40)
    print(
        f"Scanned {totals['agent']} agent(s), {totals['command']} command(s), {totals['skill']} skill(s)"
    )

    if findings["errors"]:
        print("\nErrors:")
        for path, message in findings["errors"]:
            print(f"- {path}: {message}")

    if findings["warnings"]:
        print("\nWarnings:")
        for path, message in findings["warnings"]:
            print(f"- {path}: {message}")

    if findings["errors"]:
        print("\nHint: load `opencode-manager` before fixing these files.")
        sys.exit(1)


if __name__ == "__main__":
    main()
