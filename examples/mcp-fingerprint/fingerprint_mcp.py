#!/usr/bin/env python3
"""Fingerprint MCP tool definitions to detect unreviewed changes (SUP-02 / KRI-06).

Canonicalises each tool's name, description, inputSchema and annotations into a
SHA-256 digest so description edits ("rug pulls") or schema changes fail CI or
block runtime loading until re-reviewed.

Usage:
    # Create or update a lockfile from an MCP tools/list JSON export
    python examples/mcp-fingerprint/fingerprint_mcp.py lock tools.json -o mcp-tools.lock.json

    # Verify a live/CI tools/list export against the approved lockfile
    python examples/mcp-fingerprint/fingerprint_mcp.py check tools.json --lock mcp-tools.lock.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

FIELDS = ("name", "description", "inputSchema", "annotations")


def canonical_tool(tool: dict[str, Any]) -> dict[str, Any]:
    """Extract the security-relevant fields of an MCP tool definition."""
    return {k: tool[k] for k in FIELDS if k in tool}


def fingerprint_tool(tool: dict[str, Any]) -> str:
    payload = json.dumps(canonical_tool(tool), sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


def load_tools(path: Path) -> list[dict[str, Any]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(raw, list):
        return raw
    if isinstance(raw, dict):
        if "tools" in raw and isinstance(raw["tools"], list):
            return raw["tools"]
        if "result" in raw and isinstance(raw["result"], dict) and isinstance(raw["result"].get("tools"), list):
            return raw["result"]["tools"]
    raise ValueError(f"{path}: expected a JSON list or an object containing a 'tools' list")


def build_lock(tools: list[dict[str, Any]], server: str) -> dict[str, Any]:
    entries: dict[str, dict[str, Any]] = {}
    for tool in sorted(tools, key=lambda t: t.get("name", "")):
        name = tool.get("name")
        if not name:
            raise ValueError("tool entry is missing required 'name' field")
        if name in entries:
            raise ValueError(f"duplicate tool name '{name}' (possible shadowing)")
        entries[name] = {
            "sha256": fingerprint_tool(tool),
            "description_length": len(tool.get("description", "")),
        }
    return {"schema_version": 1, "server": server, "tools": entries}


def compare_against_lock(tools: list[dict[str, Any]], lock: dict[str, Any]) -> list[str]:
    """Return a list of human-readable drift messages (empty means exact match)."""
    issues: list[str] = []
    expected: dict[str, dict[str, Any]] = lock.get("tools", {})
    seen: set[str] = set()

    for tool in tools:
        name = tool.get("name")
        if not name:
            issues.append("unnamed tool entry found")
            continue
        if name in seen:
            issues.append(f"duplicate tool '{name}' detected (possible tool shadowing)")
            continue
        seen.add(name)
        digest = fingerprint_tool(tool)
        if name not in expected:
            issues.append(f"unapproved tool added: '{name}' ({digest})")
        elif expected[name]["sha256"] != digest:
            issues.append(
                f"tool definition changed (SUP-02): '{name}' "
                f"expected {expected[name]['sha256']}, got {digest}"
            )

    for name in sorted(set(expected) - seen):
        issues.append(f"approved tool removed: '{name}'")

    return issues


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Fingerprint MCP tool definitions (SUP-02 / KRI-06).")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_lock = sub.add_parser("lock", help="Write a lockfile from an MCP tools/list JSON export")
    p_lock.add_argument("manifest", type=Path, help="Path to MCP tools/list JSON")
    p_lock.add_argument("-s", "--server", default="default", help="Server label recorded in lockfile")
    p_lock.add_argument("-o", "--output", type=Path, required=True, help="Output lockfile path")

    p_check = sub.add_parser("check", help="Check an MCP tools/list JSON export against a lockfile")
    p_check.add_argument("manifest", type=Path, help="Path to MCP tools/list JSON")
    p_check.add_argument("-l", "--lock", type=Path, required=True, help="Approved lockfile path")

    args = ap.parse_args(argv)
    tools = load_tools(args.manifest)

    if args.cmd == "lock":
        lock = build_lock(tools, args.server)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8")
        print(f"locked {len(lock['tools'])} tool(s) -> {args.output}")
        return 0

    lock = json.loads(args.lock.read_text(encoding="utf-8"))
    issues = compare_against_lock(tools, lock)
    if issues:
        for issue in issues:
            print(f"FAIL: {issue}", file=sys.stderr)
        return 1
    print(f"OK: {len(tools)} tool(s) match {args.lock}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
