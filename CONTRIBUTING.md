# Contributing

Thank you for helping keep this governance kit accurate, concise and practical.

## Single source of truth

Do **not** hand-edit generated files. Edit the YAML source files under `data/` and regenerate:

| Source of truth | Generated outputs |
|---|---|
| `data/controls.yaml` + `data/references.yaml` | `framework/control-catalogue.md`, `crosswalk/crosswalk.md`, `crosswalk/crosswalk.csv` |
| `data/kris.yaml` | `board/kri-library.md` |
| `data/threats.yaml` | `threat-models/agentic-ai-reference-threat-model.md` |
| All `data/*.yaml` | `dist/governance.json`, `dist/oscal-catalog.json`, `docs/control-selector.html` |

## Local workflow

```bash
pip install -e ".[dev]"
python tools/build.py           # regenerate Markdown, CSV, JSON, OSCAL and selector UI
python tools/build.py --check   # verify generated files are in sync
python tools/validate.py        # verify mappings, ATLAS IDs, control/KRI/threat refs and anchors
pytest -q                       # run unit tests
```

Optional JSON Schema check:

```bash
check-jsonschema --schemafile schemas/controls.schema.json data/controls.yaml
check-jsonschema --schemafile schemas/kris.schema.json data/kris.yaml
check-jsonschema --schemafile schemas/threats.schema.json data/threats.yaml
```

## Editorial guidelines

- Keep prose plain, concise and actionable; avoid compliance boilerplate.
- Use British English spelling consistently (`catalogue`, `organisation`, `authorisation`, `behaviour`, `artefact`).
- Every new framework mapping must first exist in `data/references.yaml` (and for MITRE ATLAS, in MITRE's published dataset).
- Paraphrase ISO/IEC 42001 titles; never paste copyrighted normative ISO text.
