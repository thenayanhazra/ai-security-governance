"""Check that every mapping in data/controls.yaml points at something real.

- NIST, ISO, EU AI Act and OWASP identifiers must appear in data/references.yaml.
- MITRE ATLAS identifiers are checked against MITRE's published data, and the
  ATLAS version is compared with the version recorded in references.yaml.
- Relative links in every Markdown file must resolve.

    python tools/validate.py --atlas path/to/ATLAS-latest.yaml
    python tools/validate.py            # downloads ATLAS-latest.yaml from GitHub
"""

from __future__ import annotations

import argparse
import re
import sys
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ATLAS_URL = "https://raw.githubusercontent.com/mitre-atlas/atlas-data/main/dist/ATLAS-latest.yaml"
REF_KEYS = ["nist_ai_rmf", "iso_42001", "eu_ai_act", "owasp_llm", "owasp_asi"]
REQUIRED = ["id", "title", "requirement", "evidence", "min_tier", *REF_KEYS, "mitre_atlas"]
KNOWN_TOOLS = {
    "ai-threat-modelling-engine",
    "mcp-adversarial-harness",
    "agentlint",
    "llm-prompt-injection-fuzzer",
}
ATLAS_REF = re.compile(r"\bAML\.T\d{4}(?:\.\d{3})?\b")
LINK = re.compile(r"\]\((?!https?://|mailto:|#)([^)\s]+)\)")


def fetch_atlas() -> str:
    """Download ATLAS-latest.yaml. In the repo it is a chain of symlinks, which
    raw.githubusercontent.com serves as the link target's path, so follow them."""
    url = ATLAS_URL
    for _ in range(5):
        text = urllib.request.urlopen(url, timeout=60).read().decode()
        target = text.strip()
        if len(target) < 200 and target.endswith(".yaml") and "\n" not in target:
            url = url.rsplit("/", 1)[0] + "/" + target
            continue
        return text
    raise RuntimeError("too many symlink hops resolving ATLAS-latest.yaml")


def load_atlas(path: str | None) -> tuple[dict, str]:
    text = Path(path).read_text() if path else fetch_atlas()
    data = yaml.safe_load(text)
    return data["techniques"], str(data["collection"]["version"])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--atlas", help="local copy of ATLAS-latest.yaml")
    args = ap.parse_args()

    data = yaml.safe_load((ROOT / "data/controls.yaml").read_text())
    refs = yaml.safe_load((ROOT / "data/references.yaml").read_text())
    techniques, atlas_version = load_atlas(args.atlas)
    errors: list[str] = []
    warnings: list[str] = []

    expected = refs["frameworks"]["mitre_atlas"]["version"].lstrip("v")
    if atlas_version != expected:
        warnings.append(f"ATLAS is now v{atlas_version}; mappings were made against v{expected}. Review and update.")

    seen = set()
    for c in data["controls"]:
        cid = c.get("id", "?")
        for field in REQUIRED:
            if field not in c:
                errors.append(f"{cid}: missing field '{field}'")
        if cid in seen:
            errors.append(f"{cid}: duplicate id")
        seen.add(cid)
        if cid.split("-")[0] not in data["domains"]:
            errors.append(f"{cid}: unknown domain")
        if c.get("min_tier") not in (0, 1, 2, 3):
            errors.append(f"{cid}: min_tier must be 0-3")
        for key in REF_KEYS:
            for ref in c.get(key, []):
                if ref not in refs[key]:
                    errors.append(f"{cid}: '{ref}' is not a known {key} identifier")
        for tid in c.get("mitre_atlas", []):
            if tid not in techniques:
                errors.append(f"{cid}: {tid} does not exist in MITRE ATLAS v{atlas_version}")
        for tool in c.get("tooling", []):
            if tool not in KNOWN_TOOLS:
                errors.append(f"{cid}: unknown tool '{tool}'")

    # ATLAS IDs cited anywhere in the prose must exist too.
    for md in ROOT.rglob("*.md"):
        if ".git" in md.parts:
            continue
        text = md.read_text()
        for tid in sorted(set(ATLAS_REF.findall(text))):
            if tid not in techniques:
                errors.append(f"{md.relative_to(ROOT)}: {tid} does not exist in MITRE ATLAS v{atlas_version}")
        for target in LINK.findall(text):
            target = target.split("#")[0]
            if target and not (md.parent / target).resolve().exists():
                errors.append(f"{md.relative_to(ROOT)}: broken link '{target}'")

    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}")
    print(f"{len(data['controls'])} controls checked against ATLAS v{atlas_version}: "
          f"{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
