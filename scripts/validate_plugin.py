#!/usr/bin/env python3
"""Small dependency-free Agent Plugins 1.0 package validator."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
NAME = re.compile(r"^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")
SEMVER = re.compile(r"^0\.[0-9]+\.[0-9]+(?:[-+][0-9A-Za-z.-]+)?$")


def load(name: str) -> dict:
    value = json.loads((ROOT / name).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{name}: object required")
    return value


manifest = load("plugin.json")
if manifest.get("$schema") != SCHEMA:
    raise ValueError("plugin.json: Agent Plugins 1.0 schema is required")
if not isinstance(manifest.get("name"), str) or not NAME.fullmatch(manifest["name"]):
    raise ValueError("plugin.json: invalid name")
if not isinstance(manifest.get("version"), str) or not SEMVER.fullmatch(manifest["version"]):
    raise ValueError("plugin.json: invalid version")
for field in ("description", "license"):
    if not isinstance(manifest.get(field), str) or not manifest[field].strip():
        raise ValueError(f"plugin.json: {field} is required")

mcp = load("mcp.json")
if mcp.get("$schema") != MCP_SCHEMA or not isinstance(mcp.get("mcpServers"), dict):
    raise ValueError("mcp.json: Agent Plugins 1.0 MCP schema is required")
for server_name, server in mcp["mcpServers"].items():
    if not isinstance(server, dict) or server.get("type") != "streamable-http":
        raise ValueError(f"mcp.json: {server_name} must be streamable-http")
    if not isinstance(server.get("url"), str) or not server["url"].startswith("https://"):
        raise ValueError(f"mcp.json: {server_name} must use HTTPS")
    if "headers" in server or "env" in server:
        raise ValueError(f"mcp.json: {server_name} must not embed credentials")

skill_dirs = list((ROOT / "skills").iterdir())
if len(skill_dirs) != 1 or not (skill_dirs[0] / "SKILL.md").is_file():
    raise ValueError("skills: exactly one SKILL.md package is required")
skill_text = (skill_dirs[0] / "SKILL.md").read_text(encoding="utf-8")
if "---" not in skill_text or "plaintext" not in skill_text or "/i/<token>" not in skill_text:
    raise ValueError("skills: expected frontmatter and secret-safe handoff rules")

secret_patterns = (
    re.compile(r"sk-[A-Za-z0-9]{16,}"),
    re.compile(r"Bearer\s+[A-Za-z0-9._-]{20,}"),
    re.compile(r"AGE-SECRET-KEY-1-[A-Za-z0-9]+"),
    re.compile(r"-----BEGIN [A-Z ]+PRIVATE KEY-----"),
)
for path in ROOT.rglob("*"):
    text = path.read_text(encoding="utf-8", errors="ignore") if path.is_file() else ""
    if any(pattern.search(text) for pattern in secret_patterns):
        raise ValueError(f"secret-like content found in {path.relative_to(ROOT)}")

print(f"PASS {manifest['name']} {manifest['version']}")
