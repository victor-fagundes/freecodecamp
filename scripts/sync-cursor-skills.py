#!/usr/bin/env python3
"""Re-sync .cursor/skills from knowledge-work-plugins/ after upstream updates.

Usage:
  python3 scripts/sync-cursor-skills.py
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "knowledge-work-plugins"
SKILLS = ROOT / ".cursor" / "skills"

FIRST_PARTY = [
    "bio-research",
    "cowork-plugin-management",
    "customer-support",
    "data",
    "design",
    "engineering",
    "enterprise-search",
    "finance",
    "human-resources",
    "legal",
    "marketing",
    "operations",
    "pdf-viewer",
    "product-management",
    "productivity",
    "sales",
    "small-business",
]

COLLISION_RENAMES = {
    "product-management/skills/competitive-brief": "pm-competitive-brief",
    "marketing/skills/competitive-brief": "mkt-competitive-brief",
    "sales/skills/lead-triage": "sales-lead-triage",
    "small-business/skills/lead-triage": "smb-lead-triage",
    "bio-research/skills/start": "bio-research-start",
    "productivity/skills/start": "productivity-start",
}

DROP_FM_KEYS = {"allowed-tools", "compatibility", "user-invocable", "version"}


def parse_frontmatter(text: str):
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return None, text
    return m.group(1).splitlines(), m.group(2)


def rewrite_frontmatter(lines, new_name: str):
    out = []
    seen_name = False
    for line in lines:
        if not line.strip():
            out.append(line)
            continue
        key = line.split(":", 1)[0].strip()
        if key in DROP_FM_KEYS:
            continue
        if key == "name":
            out.append(f"name: {new_name}")
            seen_name = True
            continue
        out.append(line)
    if not seen_name:
        out.insert(0, f"name: {new_name}")
    return out


def adapt_body(body: str) -> str:
    body = re.sub(r"\]\(\.\./\.\./CONNECTORS\.md\)", "](references/CONNECTORS.md)", body)
    body = re.sub(r"\]\(\.\./CONNECTORS\.md\)", "](references/CONNECTORS.md)", body)
    body = body.replace("Claude Code", "Cursor")
    body = body.replace("Claude Cowork", "Cursor")
    body = re.sub(r"\bClaude:\b", "Agent:", body)
    body = re.sub(r"\bask Claude\b", "ask the agent", body, flags=re.I)
    body = re.sub(r"\bClaude draws\b", "The agent draws", body)
    body = re.sub(r"\bClaude will\b", "The agent will", body)
    body = re.sub(r"\bClaude can\b", "The agent can", body)
    body = re.sub(r"\bwhen Claude\b", "when the agent", body, flags=re.I)
    return body


def install_skills() -> list[tuple[str, str, str]]:
    if not VENDOR.exists():
        raise SystemExit(f"Missing vendor tree: {VENDOR}")

    if SKILLS.exists():
        shutil.rmtree(SKILLS)
    SKILLS.mkdir(parents=True)

    installed: list[tuple[str, str, str]] = []
    for plugin in FIRST_PARTY:
        skills_root = VENDOR / plugin / "skills"
        if not skills_root.exists():
            continue
        connectors = VENDOR / plugin / "CONNECTORS.md"
        for skill_dir in sorted(skills_root.iterdir()):
            if not skill_dir.is_dir():
                continue
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                continue
            rel = f"{plugin}/skills/{skill_dir.name}"
            new_name = COLLISION_RENAMES.get(rel, skill_dir.name)
            dest = SKILLS / new_name
            dest.mkdir(parents=True)

            text = skill_md.read_text(encoding="utf-8")
            fm_lines, body = parse_frontmatter(text)
            if fm_lines is None:
                (dest / "SKILL.md").write_text(adapt_body(text), encoding="utf-8")
            else:
                fm = rewrite_frontmatter(fm_lines, new_name)
                content = "---\n" + "\n".join(fm) + "\n---\n" + adapt_body(body)
                if not content.endswith("\n"):
                    content += "\n"
                (dest / "SKILL.md").write_text(content, encoding="utf-8")

            for child in skill_dir.iterdir():
                if child.name == "SKILL.md":
                    continue
                target = dest / child.name
                if child.is_dir():
                    shutil.copytree(child, target)
                else:
                    shutil.copy2(child, target)

            skill_text = (dest / "SKILL.md").read_text(encoding="utf-8")
            if "CONNECTORS.md" in skill_text and connectors.exists():
                ref = dest / "references"
                ref.mkdir(exist_ok=True)
                if not (ref / "CONNECTORS.md").exists():
                    shutil.copy2(connectors, ref / "CONNECTORS.md")

            installed.append((plugin, skill_dir.name, new_name))

    brainstorm = VENDOR / "product-management" / "commands" / "brainstorm.md"
    if brainstorm.exists():
        dest = SKILLS / "brainstorm"
        dest.mkdir(parents=True)
        text = brainstorm.read_text(encoding="utf-8")
        fm_lines, body = parse_frontmatter(text)
        if fm_lines is None:
            content = (
                "---\nname: brainstorm\n"
                "description: Brainstorm a product idea with a thinking partner\n"
                "---\n" + adapt_body(text)
            )
        else:
            fm_lines = [
                l for l in fm_lines if l.split(":", 1)[0].strip() not in DROP_FM_KEYS
            ]
            if not any(l.startswith("name:") for l in fm_lines):
                fm_lines.insert(0, "name: brainstorm")
            content = "---\n" + "\n".join(fm_lines) + "\n---\n" + adapt_body(body)
        (dest / "SKILL.md").write_text(
            content if content.endswith("\n") else content + "\n", encoding="utf-8"
        )
        connectors = VENDOR / "product-management" / "CONNECTORS.md"
        if connectors.exists():
            ref = dest / "references"
            ref.mkdir(exist_ok=True)
            shutil.copy2(connectors, ref / "CONNECTORS.md")
        installed.append(("product-management", "commands/brainstorm", "brainstorm"))

    return installed


def build_mcp_json() -> list[str]:
    servers: dict[str, dict] = {}
    for plugin in (
        "product-management",
        "productivity",
        "engineering",
        "enterprise-search",
    ):
        mcp_path = VENDOR / plugin / ".mcp.json"
        if not mcp_path.exists():
            continue
        data = json.loads(mcp_path.read_text())
        for name, cfg in data.get("mcpServers", {}).items():
            url = (cfg.get("url") or "").strip()
            if not url:
                continue
            if name not in servers:
                servers[name] = {"url": url}
    out = ROOT / ".cursor" / "mcp.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps({"mcpServers": dict(sorted(servers.items()))}, indent=2) + "\n"
    )
    return list(servers.keys())


def main() -> None:
    installed = install_skills()
    servers = build_mcp_json()
    print(f"Synced {len(installed)} skills → {SKILLS}")
    print(f"MCP servers: {len(servers)}")
    bad = []
    for d in SKILLS.iterdir():
        if not d.is_dir():
            continue
        md = d / "SKILL.md"
        text = md.read_text(encoding="utf-8")
        m = re.search(r"^name:\s*(.+)$", text, re.M)
        name = m.group(1).strip() if m else None
        if name != d.name:
            bad.append((d.name, name))
    if bad:
        print("Name mismatches:", bad, file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
