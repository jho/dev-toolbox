#!/usr/bin/env python3
"""Inspect an Event Model worktree and emit a planning work graph."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


EXCLUDED_DIRS = {".git", "node_modules", "vendor", "dist", "build", "target"}


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
            parts = line.split("\t")
            if len(parts) >= 2:
                # For renames/copies, retain both paths. Active-file discovery below
                # ignores the historical path when it no longer exists.
                for path in parts[1:]:
                    changes[path] = parts[0]
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


def em_command(root: Path) -> dict[str, Any]:
    """Resolve the repository-supported em command, preferring an explicit pin."""
    pre_commit = root / ".pre-commit-config.yaml"
    if pre_commit.exists():
        text = pre_commit.read_text()
        pinned = re.search(r"@milehimikey/em@([^\s'\"]+)", text)
        if pinned and re.search(r"entry:.*validate", text):
            return {
                "command": ["npx", "--yes", f"@milehimikey/em@{pinned.group(1)}"],
                "source": str(pre_commit.relative_to(root)),
                "version": pinned.group(1),
            }

    package_json = root / "package.json"
    if package_json.exists():
        try:
            package = json.loads(package_json.read_text())
        except json.JSONDecodeError:
            package = {}
        dependencies = {
            **package.get("dependencies", {}),
            **package.get("devDependencies", {}),
        }
        version = dependencies.get("@milehimikey/em")
        if version:
            return {
                "command": ["npx", "--no-install", "@milehimikey/em"],
                "source": "package.json",
                "version": version,
            }

    if shutil.which("em"):
        return {"command": ["em"], "source": "PATH", "version": None}

    return {"command": None, "source": "unavailable", "version": None}


def run_em(root: Path, args: list[str]) -> dict[str, Any]:
    resolved = em_command(root)
    if not resolved["command"]:
        return {
            "ok": False,
            "error": "No supported em command found (checked repository pin and PATH).",
            "command": None,
            "source": resolved["source"],
            "version": resolved["version"],
        }
    try:
        result = subprocess.run(
            [*resolved["command"], *args],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            timeout=60,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as error:
        return {
            "ok": False,
            "error": str(error),
            "command": resolved["command"],
            "source": resolved["source"],
            "version": resolved["version"],
        }
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
        "command": resolved["command"],
        "source": resolved["source"],
        "version": resolved["version"],
    }


def state_summary(path: Path, root: Path | None = None) -> dict[str, Any]:
    text = path.read_text()
    phase = re.search(r"\*\*Current phase:\*\*\s*(.+)", text)
    step = re.search(r"\*\*Current step:\*\*\s*(.+)", text)
    open_questions = len(re.findall(r"^- \[ \]", text, flags=re.MULTILINE))
    return {
        "path": str(path.relative_to(root)) if root else str(path),
        "phase": phase.group(1).strip() if phase else None,
        "step": step.group(1).strip() if step else None,
        "uncheckedItems": open_questions,
    }


def is_active_path(path: Path, root: Path) -> bool:
    try:
        relative_parts = path.relative_to(root).parts
    except ValueError:
        return False
    return path.exists() and not any(part in EXCLUDED_DIRS for part in relative_parts)


def discover_models(root: Path) -> list[Path]:
    candidates = sorted(
        path
        for path in root.rglob("*.em")
        if is_active_path(path, root)
    )
    state_backed = [path for path in candidates if (path.parent / ".event-modeling.md").exists()]
    if state_backed:
        return state_backed
    root_models = [path for path in candidates if path.parent == root]
    return root_models


def state_for_model(root: Path, model: Path) -> Path | None:
    adjacent = model.parent / ".event-modeling.md"
    if adjacent.exists():
        return adjacent
    root_state = root / ".event-modeling.md"
    if model.parent == root and root_state.exists():
        return root_state
    return None


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
    model = exported.get("value", {}).get("model", {}) if isinstance(exported.get("value"), dict) else {}
    arrow_dependencies: dict[str, set[str]] = {}
    for arrow in model.get("arrows", []):
        from_ref = arrow.get("fromRef", "")
        to_ref = arrow.get("toRef", "")
        if "/" in from_ref and "/" in to_ref:
            from_slice = from_ref.split("/", 1)[0]
            to_slice = to_ref.split("/", 1)[0]
            arrow_dependencies.setdefault(to_slice, set()).add(from_slice)
    changed_slice_paths = [
        path_name
        for path_name in changed
        if "/slices/" in f"/{path_name}"
        and path_name.endswith(".md")
        and is_active_path(root / path_name, root)
    ]
    for slice_info in exported_slices:
        doc_path = slice_info.get("doc", {}).get("path")
        if not doc_path:
            continue
        full_doc = path.parent / doc_path
        if not full_doc.exists() or str(full_doc.relative_to(root)) not in changed_slice_paths:
            continue
        doc = slice_info.get("doc", {})
        dependencies = set(arrow_dependencies.get(slice_info.get("key"), set()))
        for element in slice_info.get("elements", []):
            for source in element.get("from") or []:
                source_ref = source.get("ref", "")
                if "/" in source_ref:
                    dependencies.add(source_ref.split("/", 1)[0])
        slices.append(
            {
                "key": slice_info.get("key"),
                "path": str(full_doc.relative_to(root)),
                "pattern": slice_info.get("pattern"),
                "status": doc.get("status"),
                "ratified": doc.get("ratifiedOn") is not None,
                "dependsOn": sorted(dependencies),
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
    models = discover_models(root)
    states = [state for model in models if (state := state_for_model(root, model))]
    reports = [model_report(root, path, changed) for path in models]
    work_items: list[dict[str, Any]] = []
    changed_slice_keys = {
        slice_info["key"]
        for report in reports
        for slice_info in report["slices"]
    }
    for report in reports:
        for slice_info in report["slices"]:
            dependencies = [
                dependency
                for dependency in slice_info["dependsOn"]
                if dependency in changed_slice_keys
            ]
            work_items.append(
                {
                    "id": slice_info["key"],
                    "stage": "implement",
                    "model": report["path"],
                    "slice": slice_info["path"],
                    "pattern": slice_info["pattern"],
                    "status": slice_info["status"],
                    "ratified": slice_info["ratified"],
                    "dependsOn": dependencies,
                    "verification": [f"scenarios:{slice_info['key']}"],
                }
            )
    blockers: list[str] = []
    if not relevant_changes:
        blockers.append("No changed Event Model or slice artifacts were found in the worktree.")
    inspection_failed = False
    for report in reports:
        if not report["validation"]["ok"]:
            inspection_failed = True
            tool = report["validation"].get("command") or "no supported em command"
            detail = report["validation"].get("stderr") or report["validation"].get("error", "unknown error")
            blockers.append(f"Event Model validation failed for {report['path']} using {tool}: {detail}")
        elif not report["export"]["ok"]:
            inspection_failed = True
            tool = report["export"].get("command") or "no supported em command"
            detail = report["export"].get("stderr") or report["export"].get("error", "unknown error")
            blockers.append(f"Could not inspect slices for {report['path']} using {tool}: {detail}")
    if (
        any(path.endswith(".em") and not status.startswith("D") for path, status in relevant_changes.items())
        and not work_items
        and not inspection_failed
    ):
        blockers.append("An Event Model changed, but no changed slice document was found.")
    if not models and relevant_changes:
        blockers.append("No active Event Model file with adjacent state was discovered.")
    for state in states:
        if not state.exists():
            blockers.append(f"Event Model state file is missing: {state.relative_to(root)}")
    for report in reports:
        if not report["validation"]["ok"]:
            continue
        for slice_info in report["slices"]:
            if slice_info["status"] != "ready-to-implement" or not slice_info["ratified"]:
                blockers.append(
                    f"Slice {slice_info['key']} is not ready to implement "
                    f"(status={slice_info['status']}, ratified={slice_info['ratified']})."
                )
    return {
        "schemaVersion": "1.0",
        "repository": str(root),
        "base": base,
        "head": run_git(root, "rev-parse", "HEAD").strip(),
        "changed": changed,
        "relevantChanges": relevant_changes,
        "eventModelingState": [state_summary(path, root) for path in states],
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
            depends = ", ".join(item["dependsOn"]) or "none"
            lines.append(
                f"- `{item['id']}` — `{item['slice']}` "
                f"({item['pattern']}, status={item['status']}, dependsOn={depends})"
            )
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
