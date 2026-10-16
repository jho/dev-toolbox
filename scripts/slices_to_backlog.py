#!/usr/bin/env python3
"""Inspect an Event Model worktree and emit a planning work graph."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


def run_git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=root, check=True, capture_output=True, text=True
    )
    return result.stdout


def git_base(root: Path, requested: str | None) -> str | None:
    if requested:
        return requested
    for candidate in ("@{upstream}", "origin/main", "main"):
        result = subprocess.run(
            ["git", "merge-base", "HEAD", candidate],
            cwd=root,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    return None


def changed_files(root: Path, base: str | None) -> dict[str, str]:
    changes: dict[str, str] = {}
    commands: list[list[str]] = []
    if base:
        commands.append(["diff", "--name-status", f"{base}...HEAD"])
    commands.extend(
        [
            ["diff", "--name-status"],
            ["diff", "--cached", "--name-status"],
        ]
    )
    for command in commands:
        output = run_git(root, *command)
        for line in output.splitlines():
            parts = line.split("\t", 1)
            if len(parts) == 2:
                changes[parts[1]] = parts[0]
    status = run_git(root, "status", "--porcelain=v1", "--untracked-files=all")
    for line in status.splitlines():
        if len(line) >= 4:
            path = line[3:]
            changes.setdefault(path, "??" if line[:2] == "??" else line[:2].strip())
    return dict(sorted(changes.items()))


def relevant(path: str) -> bool:
    return (
        path.endswith(".em")
        or "/slices/" in f"/{path}"
        or path.endswith(".event-modeling.md")
    )


def run_em(root: Path, args: list[str]) -> dict[str, Any]:
    try:
        result = subprocess.run(
            ["em", *args], cwd=root, capture_output=True, text=True, timeout=60
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as error:
        return {"ok": False, "error": str(error)}
    value: Any = result.stdout.strip()
    if ("--json" in args or args[:1] == ["export"]) and result.stdout.strip():
        try:
            value = json.loads(result.stdout)
        except json.JSONDecodeError:
            value = result.stdout.strip()
    return {
        "ok": result.returncode == 0,
        "exitCode": result.returncode,
        "value": value,
        "stderr": result.stderr.strip(),
    }


def state_summary(path: Path) -> dict[str, Any]:
    text = path.read_text()
    phase = re.search(r"\*\*Current phase:\*\*\s*(.+)", text)
    step = re.search(r"\*\*Current step:\*\*\s*(.+)", text)
    open_questions = len(re.findall(r"^- \[ \]", text, flags=re.MULTILINE))
    return {
        "path": str(path),
        "phase": phase.group(1).strip() if phase else None,
        "step": step.group(1).strip() if step else None,
        "uncheckedItems": open_questions,
    }


def model_report(root: Path, path: Path, changed: dict[str, str]) -> dict[str, Any]:
    relative = str(path.relative_to(root))
    status = run_em(root, ["status", relative, "--json"])
    exported = run_em(root, ["export", relative])
    slices: list[dict[str, Any]] = []
    exported_slices = (
        exported.get("value", {}).get("model", {}).get("slices", [])
        if isinstance(exported.get("value"), dict)
        else []
    )
    changed_slice_paths = [
        path_name
        for path_name in changed
        if "/slices/" in f"/{path_name}" and path_name.endswith(".md")
    ]
    for slice_info in exported_slices:
        doc_path = slice_info.get("doc", {}).get("path")
        if not doc_path:
            continue
        full_doc = path.parent / doc_path
        if str(full_doc.relative_to(root)) not in changed_slice_paths:
            continue
        slices.append(
            {
                "key": slice_info.get("key"),
                "path": str(full_doc.relative_to(root)),
                "pattern": slice_info.get("pattern"),
                "status": slice_info.get("doc", {}).get("status"),
                "ratified": slice_info.get("doc", {}).get("ratifiedOn") is not None,
            }
        )
    return {
        "path": relative,
        "validation": run_em(root, ["validate", relative]),
        "status": status,
        "export": exported,
        "slices": slices,
    }


def build_graph(root: Path, base: str | None) -> dict[str, Any]:
    changed = changed_files(root, base)
    relevant_changes = {path: status for path, status in changed.items() if relevant(path)}
    models = [root / path for path in relevant_changes if path.endswith(".em")]
    if not models:
        models = [root / path for path in changed if path.endswith(".em")]
    states = [root / path for path in changed if path.endswith(".event-modeling.md")]
    reports = [model_report(root, path, changed) for path in models]
    work_items: list[dict[str, Any]] = []
    for report in reports:
        for slice_info in report["slices"]:
            work_items.append(
                {
                    "id": slice_info["key"],
                    "stage": "implement",
                    "model": report["path"],
                    "slice": slice_info["path"],
                    "dependsOn": [],
                    "verification": [f"scenarios:{slice_info['key']}"],
                }
            )
    blockers: list[str] = []
    if not relevant_changes:
        blockers.append("No changed Event Model or slice artifacts were found in the worktree.")
    if any(path.endswith(".em") for path in relevant_changes) and not work_items:
        blockers.append("An Event Model changed, but no changed slice document was found.")
    if any(not report["validation"]["ok"] for report in reports):
        blockers.append("At least one changed Event Model failed em validation.")
    return {
        "schemaVersion": "1.0",
        "repository": str(root),
        "base": base,
        "head": run_git(root, "rev-parse", "HEAD").strip(),
        "changed": changed,
        "relevantChanges": relevant_changes,
        "eventModelingState": [state_summary(path) for path in states],
        "models": reports,
        "workItems": work_items,
        "blockers": blockers,
        "ready": bool(work_items) and not blockers,
        "orchestration": "external-harness",
    }


def markdown(graph: dict[str, Any]) -> str:
    lines = ["# Event Model planning graph", "", f"- Ready: `{graph['ready']}`"]
    if graph["base"]:
        lines.append(f"- Base: `{graph['base']}`")
    lines.extend(["", "## Work items"])
    if graph["workItems"]:
        for item in graph["workItems"]:
            lines.append(f"- `{item['id']}` — `{item['slice']}`")
    else:
        lines.append("- None")
    lines.extend(["", "## Blockers"])
    if graph["blockers"]:
        lines.extend(f"- {blocker}" for blocker in graph["blockers"])
    else:
        lines.append("- None")
    lines.extend(["", "External harness owns parallel execution, worktrees, branches, and PRs."])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--base", help="merge-base ref; defaults to upstream, origin/main, or main")
    parser.add_argument("--format", choices=("json", "markdown", "both"), default="both")
    args = parser.parse_args()
    root = Path(run_git(args.repo_root.resolve(), "rev-parse", "--show-toplevel").strip())
    base = git_base(root, args.base)
    graph = build_graph(root, base)
    if args.format in ("json", "both"):
        print(json.dumps(graph, indent=2))
    if args.format == "both":
        print("\n---\n")
    if args.format in ("markdown", "both"):
        print(markdown(graph), end="")
    return 0 if graph["ready"] or not graph["relevantChanges"] else 1


if __name__ == "__main__":
    sys.exit(main())
