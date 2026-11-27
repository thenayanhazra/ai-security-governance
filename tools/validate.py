"""Check that every mapping in data/controls.yaml points at something real.

- NIST, ISO, EU AI Act, OWASP and MITRE ATLAS identifiers must appear in data/references.yaml.
- MITRE ATLAS identifiers (in references.yaml, controls.yaml and prose) are checked
  against MITRE's published data, and the ATLAS version is compared with references.yaml.
- Control IDs cited in Markdown prose must exist in data/controls.yaml.
- Relative links and heading anchors in every Markdown file must resolve.

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
REF_KEYS = ["nist_ai_rmf", "iso_42001", "eu_ai_act", "owasp_llm", "owasp_asi", "mitre_atlas"]
REQUIRED = ["id", "title", "requirement", "evidence", "min_tier", *REF_KEYS]
IMPACTS = ("low", "moderate", "high", "severe")
KNOWN_TOOLS = {
    "ai-threat-modelling-engine",
    "mcp-adversarial-harness",
    "agentlint",
    "llm-prompt-injection-fuzzer",
}
ATLAS_REF = re.compile(r"\bAML\.T\d{4}(?:\.\d{3})?\b")
LINK = re.compile(r"\]\((?!https?://|mailto:)([^)\s]+)\)")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)


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


def heading_slugs(text: str) -> set[str]:
    """Compute GitHub-Flavored Markdown heading anchor slugs for a document."""
    slugs: set[str] = set()
    counts: dict[str, int] = {}
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADING.match(line)
        if not m:
            continue
        title = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", m.group(1))
        title = re.sub(r"[`*_~]", "", title).strip().lower()
        slug = re.sub(r"[^\w\s-]", "", title)
        slug = re.sub(r"\s+", "-", slug)
        if slug in counts:
            counts[slug] += 1
            slugs.add(f"{slug}-{counts[slug]}")
        else:
            counts[slug] = 0
            slugs.add(slug)
    return slugs


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

    for tid in refs.get("mitre_atlas", {}):
        if tid not in techniques:
            errors.append(f"data/references.yaml: {tid} does not exist in MITRE ATLAS v{atlas_version}")

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
        if "or_impact" in c:
            if c["or_impact"] not in IMPACTS:
                errors.append(f"{cid}: or_impact must be one of {', '.join(IMPACTS)}")
            elif c.get("min_tier") == 0:
                errors.append(f"{cid}: or_impact is redundant when min_tier is 0")
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

    domain_pattern = "|".join(re.escape(d) for d in data["domains"])
    control_ref = re.compile(rf"\b(?:{domain_pattern})-\d{{2}}\b")
    slug_cache: dict[Path, set[str]] = {}

    def get_slugs(path: Path) -> set[str]:
        if path not in slug_cache:
            slug_cache[path] = heading_slugs(path.read_text())
        return slug_cache[path]

    # ATLAS IDs, control IDs, relative links and heading anchors in prose must resolve.
    for md in ROOT.rglob("*.md"):
        if ".git" in md.parts:
            continue
        text = md.read_text()
        rel = md.relative_to(ROOT)
        for tid in sorted(set(ATLAS_REF.findall(text))):
            if tid not in techniques:
                errors.append(f"{rel}: {tid} does not exist in MITRE ATLAS v{atlas_version}")
        for cid in sorted(set(control_ref.findall(text))):
            if cid not in seen:
                errors.append(f"{rel}: unknown control ID '{cid}'")
        for raw_target in LINK.findall(text):
            file_part, _, anchor = raw_target.partition("#")
            target_path = (md.parent / file_part).resolve() if file_part else md.resolve()
            if not target_path.exists():
                errors.append(f"{rel}: broken link '{raw_target}'")
                continue
            if anchor and target_path.suffix == ".md":
                if anchor not in get_slugs(target_path):
                    errors.append(f"{rel}: broken anchor '{raw_target}'")

    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}")
    print(f"{len(data['controls'])} controls checked against ATLAS v{atlas_version}: "
          f"{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
