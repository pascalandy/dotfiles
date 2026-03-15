#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def contains(text: str, patterns: list[str]) -> tuple[bool, str]:
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE | re.DOTALL)
        if match:
            snippet = match.group(0).strip().replace("\n", " ")
            return True, snippet[:200]
    return False, "No matching text found."


def expectations_for(eval_id: int):
    if eval_id == 1:
        return [
            {
                "text": "Mentions both `opencode.json` and `AGENTS.md`.",
                "patterns": [r"opencode\.json.*AGENTS\.md", r"AGENTS\.md.*opencode\.json"],
            },
            {
                "text": "Distinguishes project-level and global scope or otherwise keeps the advice project-scoped.",
                "patterns": [r"\bproject\b.*\bglobal\b", r"\bglobal\b.*\bproject\b", r"project-level", r"in this repo"],
            },
            {
                "text": "Includes a validation or smoke-test step after editing.",
                "patterns": [r"validation", r"smoke[- ]test", r"opencode run", r"\bverify\b", r"\bcheck\b"],
            },
        ]
    if eval_id == 2:
        return [
            {
                "text": "Explains plan mode and build mode.",
                "patterns": [r"\bplan\b.*\bbuild\b", r"\bbuild\b.*\bplan\b"],
            },
            {
                "text": "Explains at least two of: subagents, commands, skills, agents.",
                "patterns": [
                    r"\bsubagent\b.*\bcommand\b",
                    r"\bcommand\b.*\bskill\b",
                    r"\bsubagent\b.*\bskill\b",
                    r"\bagent\b.*\bskill\b",
                ],
            },
            {
                "text": "Includes a permission caution.",
                "patterns": [r"\bpermission", r"keep permissions tight", r"tight permissions", r"broad access"],
            },
        ]
    if eval_id == 3:
        return [
            {
                "text": "Warns against over-triggering during ordinary coding.",
                "patterns": [r"over-trigger", r"ordinary coding", r"generic coding", r"normal coding"],
            },
            {
                "text": "Explains what belongs in `SKILL.md` versus `references/`.",
                "patterns": [r"SKILL\.md.*references/", r"references/.*SKILL\.md"],
            },
            {
                "text": "Includes the official docs URL and the GitHub repository URL.",
                "patterns": [r"opencode\.ai/docs", r"github\.com/anomalyco/opencode"],
                "require_all": True,
            },
        ]
    raise ValueError(f"Unsupported eval_id: {eval_id}")


def evaluate_expectation(text: str, expectation: dict) -> dict:
    patterns = expectation["patterns"]
    require_all = expectation.get("require_all", False)
    if require_all:
        evidence = []
        all_passed = True
        for pattern in patterns:
            passed, snippet = contains(text, [pattern])
            all_passed = all_passed and passed
            evidence.append(snippet)
        return {
            "text": expectation["text"],
            "passed": all_passed,
            "evidence": " | ".join(evidence),
        }

    passed, snippet = contains(text, patterns)
    return {
        "text": expectation["text"],
        "passed": passed,
        "evidence": snippet,
    }


def main():
    if len(sys.argv) != 2:
        print("Usage: grade_eval_outputs.py <run-dir>", file=sys.stderr)
        sys.exit(1)

    run_dir = Path(sys.argv[1]).resolve()
    metadata = json.loads(load_text(run_dir.parent.parent / "eval_metadata.json"))
    eval_id = metadata["eval_id"]
    final_text = load_text(run_dir / "outputs" / "final.md")
    transcript_text = load_text(run_dir / "outputs" / "events.jsonl")
    timing_path = run_dir / "timing.json"
    timing = json.loads(load_text(timing_path)) if timing_path.exists() else {}

    expectations = [evaluate_expectation(final_text, item) for item in expectations_for(eval_id)]
    passed = sum(1 for item in expectations if item["passed"])
    total = len(expectations)
    failed = total - passed

    grading = {
        "expectations": expectations,
        "summary": {
            "passed": passed,
            "failed": failed,
            "total": total,
            "pass_rate": round(passed / total, 4) if total else 0.0,
        },
        "execution_metrics": {
            "tool_calls": {},
            "total_tool_calls": 0,
            "total_steps": 0,
            "errors_encountered": transcript_text.lower().count('"type":"error"'),
            "output_chars": len(final_text),
            "transcript_chars": len(transcript_text),
        },
        "timing": {
            "total_duration_seconds": timing.get("total_duration_seconds", 0.0),
            "executor_duration_seconds": timing.get("total_duration_seconds", 0.0),
        },
        "claims": [],
        "user_notes_summary": {
            "uncertainties": [],
            "needs_review": [],
            "workarounds": [],
        },
    }

    (run_dir / "grading.json").write_text(json.dumps(grading, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
