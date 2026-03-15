#!/usr/bin/env python3
import json
import os
import shutil
import subprocess
import sys
import time
import argparse
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[5]
SKILL_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = SKILL_ROOT.parent / "opencode-manager-workspace"
SKILL_CREATOR_ROOT = Path("/Users/andy16/.codex/skills/skill-creator")

GRADE_SCRIPT = SKILL_ROOT / "scripts" / "grade_eval_outputs.py"
AGGREGATE_SCRIPT = SKILL_CREATOR_ROOT / "scripts" / "aggregate_benchmark.py"
VIEWER_SCRIPT = SKILL_CREATOR_ROOT / "eval-viewer" / "generate_review.py"


EVAL_NAMES = {
    1: "project-setup-safe-defaults",
    2: "workflow-and-subagent-decision-guide",
    3: "merge-overlapping-skills",
}


def load_evals():
    evals_path = SKILL_ROOT / "evals" / "evals.json"
    return json.loads(evals_path.read_text(encoding="utf-8"))["evals"]


def response_only_prompt(prompt: str) -> str:
    return (
        "Answer in markdown only. Do not create, modify, or write any files. "
        "Do not ask for confirmation. Respond directly to the request.\n\n"
        f"{prompt}"
    )


def reset_iteration_root(iteration_root: Path):
    if iteration_root.exists():
        shutil.rmtree(iteration_root)
    iteration_root.mkdir(parents=True)


def write_eval_metadata(eval_dir: Path, eval_item: dict):
    metadata = {
        "eval_id": eval_item["id"],
        "eval_name": EVAL_NAMES[eval_item["id"]],
        "prompt": eval_item["prompt"],
        "assertions": eval_item["expectations"],
    }
    (eval_dir / "eval_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )


def prepare_project(run_dir: Path, with_skill: bool):
    project_dir = run_dir / "project"
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "README.md").write_text(
        "# Eval Workspace\n\nTemporary workspace for OpenCode skill evaluation.\n",
        encoding="utf-8",
    )
    (project_dir / "opencode.json").write_text(
        json.dumps(
            {
                "$schema": "https://opencode.ai/config.json",
                "permission": {
                    "edit": "deny",
                    "bash": {"*": "deny"},
                    "webfetch": "deny",
                }
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    if with_skill:
        target_skill = project_dir / ".opencode" / "skill" / "opencode-manager"
        target_skill.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(SKILL_ROOT, target_skill, dirs_exist_ok=True)
    return project_dir


def run_opencode(project_dir: Path, prompt: str):
    command = [
        "opencode",
        "run",
        "--dir",
        str(project_dir),
        "--agent",
        "plan",
        prompt,
    ]
    started = time.time()
    try:
        completed = subprocess.run(
            command,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
            timeout=45,
            env={
                **os.environ,
                "NO_COLOR": "1",
                "TERM": "dumb",
            },
        )
    except subprocess.TimeoutExpired as exc:
        completed = subprocess.CompletedProcess(
            command,
            124,
            exc.stdout or "",
            (exc.stderr or "") + "\n[TIMEOUT] OpenCode run exceeded 45 seconds.\n",
        )
    duration = round(time.time() - started, 3)
    return completed, duration


def save_run(run_dir: Path, result, duration: float):
    outputs_dir = run_dir / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)
    (outputs_dir / "final.md").write_text(result.stdout, encoding="utf-8")
    (outputs_dir / "stderr.txt").write_text(result.stderr, encoding="utf-8")
    (outputs_dir / "events.jsonl").write_text("", encoding="utf-8")

    timing = {
        "total_tokens": 0,
        "duration_ms": int(duration * 1000),
        "total_duration_seconds": duration,
    }
    (run_dir / "timing.json").write_text(json.dumps(timing, indent=2) + "\n", encoding="utf-8")


def run_grader(run_dir: Path):
    subprocess.run(
        [sys.executable, str(GRADE_SCRIPT), str(run_dir)],
        cwd=REPO_ROOT,
        check=True,
    )


def generate_benchmark(iteration_root: Path):
    subprocess.run(
        [
            sys.executable,
            str(AGGREGATE_SCRIPT),
            str(iteration_root),
            "--skill-name",
            "opencode-manager",
            "--skill-path",
            str(SKILL_ROOT),
        ],
        cwd=REPO_ROOT,
        check=True,
    )

    benchmark_path = iteration_root / "benchmark.json"
    benchmark = json.loads(benchmark_path.read_text(encoding="utf-8"))
    benchmark["metadata"]["runs_per_configuration"] = 1
    benchmark["metadata"]["executor_model"] = "opencode default model"
    benchmark["metadata"]["analyzer_model"] = "inline manual analysis"
    benchmark["notes"] = [
        "Single run per configuration for this first-pass benchmark.",
        "Token counts are unavailable from this CLI harness, so they remain zero.",
    ]
    benchmark_path.write_text(json.dumps(benchmark, indent=2) + "\n", encoding="utf-8")


def generate_viewer(iteration_root: Path, previous_workspace: Path | None):
    command = [
        sys.executable,
        str(VIEWER_SCRIPT),
        str(iteration_root),
        "--skill-name",
        "opencode-manager",
        "--benchmark",
        str(iteration_root / "benchmark.json"),
        "--static",
        str(iteration_root / "review.html"),
    ]
    if previous_workspace and previous_workspace.exists():
        command.extend(["--previous-workspace", str(previous_workspace)])
    subprocess.run(command, cwd=REPO_ROOT, check=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--iteration", type=int, default=1)
    args = parser.parse_args()

    iteration_root = WORKSPACE_ROOT / f"iteration-{args.iteration}"
    previous_workspace = (
        WORKSPACE_ROOT / f"iteration-{args.iteration - 1}" if args.iteration > 1 else None
    )

    reset_iteration_root(iteration_root)
    evals = load_evals()

    for eval_item in evals:
        eval_dir = iteration_root / f"eval-{eval_item['id']}-{EVAL_NAMES[eval_item['id']]}"
        eval_dir.mkdir(parents=True, exist_ok=True)
        write_eval_metadata(eval_dir, eval_item)

        for config_name, with_skill in (("with_skill", True), ("without_skill", False)):
            run_dir = eval_dir / config_name / "run-1"
            project_dir = prepare_project(run_dir, with_skill)
            result, duration = run_opencode(project_dir, response_only_prompt(eval_item["prompt"]))
            save_run(run_dir, result, duration)
            run_grader(run_dir)

    generate_benchmark(iteration_root)
    generate_viewer(iteration_root, previous_workspace)


if __name__ == "__main__":
    main()
