"""Unit tests for tools/build.py and tools/validate.py (offline, deterministic)."""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import build  # noqa: E402
import validate  # noqa: E402


def mock_atlas_from_refs() -> tuple[dict, str]:
    refs = yaml.safe_load((ROOT / "data/references.yaml").read_text(encoding="utf-8"))
    ver = refs["frameworks"]["mitre_atlas"]["version"].lstrip("v")
    techniques = {tid: {"name": title} for tid, title in refs["mitre_atlas"].items()}
    return techniques, ver


def test_build_check_is_in_sync() -> None:
    assert build.main(["--check"]) == 0


def test_governance_json_bundle() -> None:
    gov = json.loads((ROOT / "dist/governance.json").read_text(encoding="utf-8"))
    assert gov["schema_version"] == build.SCHEMA_VERSION
    assert len(gov["domains"]) == 10
    assert len(gov["controls"]) == 40
    assert len(gov["kris"]) == 13
    assert len(gov["threats"]) == 20
    kri04 = next(k for k in gov["kris"] if k["id"] == "KRI-04")
    assert kri04["thresholds"]["green_max"] == 5
    assert kri04["thresholds"]["amber_max"] == 15


def test_oscal_catalog_structure_and_determinism() -> None:
    controls, refs, _, _ = build.load(ROOT)
    first = build.oscal_catalog_json(controls, refs)
    second = build.oscal_catalog_json(controls, refs)
    assert first == second

    parsed = json.loads(first)
    cat = parsed["catalog"]
    assert cat["metadata"]["oscal-version"] == "1.1.2"
    assert len(cat["groups"]) == 10
    total_controls = sum(len(g["controls"]) for g in cat["groups"])
    assert total_controls == 40


def test_control_selector_embeds_valid_json() -> None:
    html = (ROOT / "docs/control-selector.html").read_text(encoding="utf-8")
    m = re.search(r'<script id="gov-data" type="application/json">(.*?)</script>', html, re.DOTALL)
    assert m is not None
    embedded = json.loads(m.group(1).replace("<\\/", "</"))
    assert len(embedded["controls"]) == 40
    assert len(embedded["kris"]) == 13


def test_validate_repo_passes_offline() -> None:
    techniques, ver = mock_atlas_from_refs()
    errors, warnings, count = validate.validate_repo(ROOT, techniques, ver)
    assert count == 40
    assert errors == []
    assert warnings == []


def test_validate_catches_bad_data_and_prose_errors(tmp_path: Path) -> None:
    shutil.copytree(ROOT / "data", tmp_path / "data")
    techniques, ver = mock_atlas_from_refs()

    # Inject redundant or_impact on a tier 0 control
    controls = yaml.safe_load((tmp_path / "data/controls.yaml").read_text(encoding="utf-8"))
    controls["controls"][0]["or_impact"] = "high"
    (tmp_path / "data/controls.yaml").write_text(yaml.safe_dump(controls), encoding="utf-8")

    # Inject unknown control in kris.yaml
    kris = yaml.safe_load((tmp_path / "data/kris.yaml").read_text(encoding="utf-8"))
    kris["kris"][0]["controls"].append("GOV-99")
    (tmp_path / "data/kris.yaml").write_text(yaml.safe_dump(kris), encoding="utf-8")

    # Inject unknown component in threats.yaml
    threats = yaml.safe_load((tmp_path / "data/threats.yaml").read_text(encoding="utf-8"))
    threats["threats"][0]["components"].append("C99")
    (tmp_path / "data/threats.yaml").write_text(yaml.safe_dump(threats), encoding="utf-8")

    # Inject broken prose references and broken anchor
    (tmp_path / "doc.md").write_text(
        "# Valid Heading\n\nBad refs: GOV-99, KRI-99, T-99, AML.T9999, [bad](#missing-anchor)\n",
        encoding="utf-8",
    )

    errors, _, _ = validate.validate_repo(tmp_path, techniques, ver)
    joined = "\n".join(errors)
    assert "or_impact is redundant when min_tier is 0" in joined
    assert "references unknown control 'GOV-99'" in joined
    assert "unknown component 'C99'" in joined
    assert "unknown control ID 'GOV-99'" in joined
    assert "unknown KRI ID 'KRI-99'" in joined
    assert "unknown threat ID 'T-99'" in joined
    assert "AML.T9999 does not exist" in joined
    assert "broken anchor '#missing-anchor'" in joined
