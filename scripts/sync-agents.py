#!/usr/bin/env python3
"""Generate native Codex and Claude agents from portable toolbox roles."""

import argparse
import json
import re
from pathlib import Path


CLAUDE_TOOLS = {
    "read": "Read",
    "search": "Grep",
    "shell": "Bash",
    "edit": "Edit",
    "git": "Bash(git:*)",
    "github": "Bash(gh:*)",
}


def role_definition(path: Path) -> tuple[dict, str]:
    text = path.read_text()
    if not text.startswith("---\n"):
        raise SystemExit(f"Role is missing YAML frontmatter: {path}")
    _, frontmatter, body = text.split("---\n", 2)
    metadata: dict = {}
    current_list = None
    for line in frontmatter.splitlines():
        if not line.strip():
            continue
        if line.startswith("  - ") and current_list:
            metadata[current_list].append(line[4:].strip())
            continue
        key, separator, value = line.partition(":")
        if not separator:
            continue
        key = key.strip()
        value = value.strip()
        if value == "[]":
            metadata[key] = []
            current_list = key
        elif value:
            metadata[key] = value
            current_list = None
        else:
            metadata[key] = []
            current_list = key
    metadata.setdefault("skills", [])
    metadata.setdefault("capabilities", [])
    metadata.setdefault("handoffs", [])
    if not re.fullmatch(r"[a-z0-9-]+", metadata.get("name", "")):
        raise SystemExit(f"Invalid role name in frontmatter: {path}")
    return metadata, body.lstrip("\n")


def codex_agent(role: str, metadata: dict, body: str) -> str:
    instructions = (
        f"You are the {role} agent.\n\n"
        f"Skills to use when applicable: {', '.join(metadata['skills']) or 'none'}.\n"
        f"Handoff targets: {', '.join(metadata['handoffs']) or 'none'}.\n\n"
        "Follow the portable role definition below. Delegate to a handoff target when the work "
        "clearly enters that role's responsibility and the user has asked for delegation or the "
        "applicable workflow requests it.\n\n"
        f"{body}"
    )
    return (
        f"name = {json.dumps(role)}\n"
        f"description = {json.dumps(metadata['description'])}\n"
        f"developer_instructions = {json.dumps(instructions)}\n"
    )


def claude_agent(role: str, metadata: dict, body: str) -> str:
    tools = [CLAUDE_TOOLS[name] for name in metadata["capabilities"]]
    lines = ["---", f"name: {role}", f"description: {metadata['description']}"]
    if tools:
        lines.append("tools:")
        lines.extend(f"  - {tool}" for tool in tools)
    if metadata["skills"]:
        lines.append("skills:")
        lines.extend(f"  - {skill}" for skill in metadata["skills"])
    lines.extend(["---", "", body])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--surface", choices=("codex", "claude", "both"), required=True)
    parser.add_argument("--codex-target", type=Path)
    parser.add_argument("--claude-target", type=Path)
    args = parser.parse_args()

    root = args.repo_root.resolve()
    roles_dir = root / "roles"
    definitions = {}
    for path in sorted(roles_dir.glob("*.md")):
        metadata, body = role_definition(path)
        definitions[metadata["name"]] = (metadata, body)

    if args.surface in ("codex", "both"):
        if not args.codex_target:
            raise SystemExit("--codex-target is required for the codex surface")
        target = args.codex_target
        target.mkdir(parents=True, exist_ok=True)
        for role, (metadata, body) in definitions.items():
            (target / f"{role}.toml").write_text(
                codex_agent(role, metadata, body)
            )

    if args.surface in ("claude", "both"):
        if not args.claude_target:
            raise SystemExit("--claude-target is required for the claude surface")
        target = args.claude_target
        target.mkdir(parents=True, exist_ok=True)
        for role, (metadata, body) in definitions.items():
            (target / f"{role}.md").write_text(
                claude_agent(role, metadata, body)
            )

    print(f"Synced {len(definitions)} portable roles for {args.surface}")


if __name__ == "__main__":
    main()
