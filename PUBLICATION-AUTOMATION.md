# Publication Automation System

This is an automated publication workflow system for InDesign-based magazines. It handles manifest validation, caption injection, QA gating, and report generation for *The Visceral Theory of Sight*.

## What It Does

- **Validates** the photo manifest (64 images with metadata)
- **Generates** InDesign ExtendScript for automatic caption injection
- **Creates** the backmatter source register from metadata
- **Reports** QA gate status before final handoff
- **Bridges** Python automation with InDesign workflows

## Quick Start

### 1. Run Full Workflow

```bash
python scripts/publication_workflow.py
```

This will:
- Validate all 64 assets
- Generate QA gate report
- Generate source register markdown
- Generate caption injection script for InDesign
- Output a workflow log

### 2. Validate Only

```bash
python scripts/publication_workflow.py --validate-only
```

Check if manifest is valid without generating files.

### 3. Generate Reports Only

```bash
python scripts/publication_workflow.py --report
```

Regenerate QA reports and documents.

### 4. With InDesign Preflight

```bash
python scripts/publication_workflow.py --indesign "path/to/document.indd"
```

Include InDesign-specific preflight checks.

## Outputs

It generates these files:

### Reports
- `visceral-production-route/reports/publication-qa-gate-report.json` — QA checklist & status
- `visceral-production-route/reports/publication-source-register.md` — Backmatter documentation
- `visceral-production-route/reports/publication-workflow.log` — Execution log

### Scripts
- `visceral-production-route/templates/publication-caption-injection.jsx` — Auto-generated captions for InDesign
- `visceral-production-route/templates/publication-indesign-bridge.jsx` — InDesign preflight bridge

## Architecture

### PublicationHub Module (`scripts/publication_hub.py`)

Core publication automation class:

```python
from publication_hub import PublicationHub

publication_hub = PublicationHub(root)

# Load manifest
manifest = publication_hub.load_manifest()  # 64 assets

# Validate
validation = publication_hub.validate_manifest()

# Generate outputs
publication_hub.generate_indesign_script_for_captions()
publication_hub.generate_source_register_markdown()
publication_hub.export_qa_report()
```

**Methods:**
- `load_manifest()` — Parse labeled-photo-manifest.json
- `validate_manifest()` — QA checks on metadata
- `get_asset_by_label(label)` — Lookup single asset
- `generate_indesign_script_for_captions()` — ExtendScript for captions
- `generate_source_register_markdown()` — Backmatter docs
- `generate_qa_report()` — QA gate validation
- `export_qa_report()` — Save report as JSON

### Workflow Orchestrator (`scripts/publication_workflow.py`)

High-level workflow manager:

```python
from publication_workflow import PublicationWorkflow

workflow = PublicationWorkflow(root)
workflow.run_full_workflow()
```

**Phases:**
1. Validation gate (manifest checks)
2. Report generation (QA, source register, scripts)
3. InDesign preflight (optional)
4. Summary & next steps

### InDesign Bridge (`templates/publication-indesign-bridge.jsx`)

ExtendScript for InDesign automation:

```javascript
// Run inside InDesign
// File > Scripts > publication-indesign-bridge.jsx

// Preflight checks:
// - Required layers (Captions, Source Register)
// - Missing/modified links
// - Overset text
// - Color space & fonts
```

## QA Gate Checklist

Before publication, the workflow validates:

- ✓ Automated test suite passes
- ✓ HTML/source preflight (TOC, captions, 64 source-register entries)
- ✓ Browser visual inspection (caption crowding, text fit, image rhythm)
- ✓ InDesign preflight (missing links, overset, bleed, color, fonts)
- ✓ 64 images with A-number, visual group, source-register entry
- ✓ No original filenames/rights notes in front-of-book captions
- ✓ References & citations resolve to backmatter
- ✓ PDF export validation (trim, bleed, gutters, folios, captions)
- ✓ Preflight-safe .indd kept as rollback

## Manifest Format

The photo manifest (`data/labeled-photo-manifest.json`) contains:

```json
[
  {
    "label": "A01",
    "repo_file": "images/labeled/a01-...jpg",
    "title": "Photo title",
    "visual_group": "Group 3: Mediation",
    "intended_pages_or_section": "Pages 27-38 / Article III, The Veil",
    "creator_or_institution": "Creator or Source",
    "rights_license_status": "Rights info",
    "original_path": "C:\\path\\to\\original.jpg",
    "production_source": "C:\\path\\to\\production.jpg",
    "web_dimensions_px": "1539x1800",
    "original_dimensions_px": "3096x3620",
    "sequence": "01"
  }
]
```

**Fields:**
- `label` — A01–A67 (asset identifier)
- `title` — Caption text for publication
- `visual_group` — Thematic grouping
- `intended_pages_or_section` — Where in magazine
- `creator_or_institution` — Rights holder
- `rights_license_status` — Licensing notes
- `original_path` — Original source file
- `production_source` — Production-ready file
- `web_dimensions_px` — Web preview size
- `original_dimensions_px` — Original size
- `sequence` — Order in publication

## InDesign Workflow

### Step 1: Validate with the workflow

```bash
python scripts/publication_workflow.py
```

Review `publication-qa-gate-report.json`.

### Step 2: Open InDesign

Open your 50-page magazine layout:
```
output/indesign/the-anatomy-of-looking-50pp-indesign-base.indd
```

### Step 3: Run Preflight Bridge

```
File > Scripts > Other Scripts...
  → templates/publication-indesign-bridge.jsx
```

This checks:
- Captions and Source Register layers exist
- Image links are present and valid
- No overset text
- Color space and fonts are correct

### Step 4: Inject Captions

Use `publication-caption-injection.jsx` to auto-populate captions:

```
File > Scripts > Other Scripts...
  → templates/publication-caption-injection.jsx
```

This pulls from your manifest and injects into text frames.

### Step 5: Run Native InDesign Preflight

```
Window > Output > Preflight
```

Check for:
- Missing links
- Overset text
- Bleed, color space, fonts

### Step 6: Export PDF

```
File > Export > PDF
```

Inspect exported PDF for:
- Page trim and bleed
- Caption formatting
- Image placement and crop
- Backmatter readability

## Reports & Documentation

### QA Gate Report

`publication-qa-gate-report.json`:

```json
{
  "publication": "The Visceral Theory of Sight",
  "qa_gate_status": "READY",
  "manifest_validation": {
    "valid": true,
    "issue_count": 0,
    "total_assets": 64
  },
  "checklist": [
    "✓ Run automated test suite",
    "✓ Run HTML/source preflight",
    ...
  ]
}
```

### Source Register

`publication-source-register.md`:

Backmatter documentation for all 64 images:

```markdown
## Group 3: Mediation

### A01: A photograph of an attractive woman...

- **Section:** Pages 27-38 / Article III, The Veil
- **Creator/Source:** Creator not verified
- **Rights Status:** Local/generated/unknown source...
- **Dimensions:** 3096x3620 → 1539x1800 (web)

---
```

### Workflow Log

`publication-workflow.log`:

Timestamped execution log for debugging:

```
[23:59:07] INFO     | === PUBLICATION VALIDATION GATE ===
[23:59:07] OK       | Loaded 64 assets
[23:59:07] OK       | All checks passed (64 assets)
```

## Customization

### Add New Assets

Edit `data/labeled-photo-manifest.json` and re-run the workflow:

```bash
python scripts/publication_workflow.py
```

### Modify Caption Format

Edit the `generate_indesign_script_for_captions()` method in `scripts/publication_hub.py`:

```python
def generate_indesign_script_for_captions(self, output_file=None) -> str:
    # Customize caption text here
    caption_text = f"{asset.label}: {asset.title}"
    # ...
```

### Customize QA Checklist

Edit the `generate_qa_report()` method:

```python
def generate_qa_report(self) -> dict:
    report = {
        "checklist": [
            "✓ Your custom check here",
            # ...
        ]
    }
```

## Architecture Diagram

```
┌─────────────────────────────────────────────────┐
│  labeled-photo-manifest.json (64 assets)        │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
    ┌────────────────────────────┐
    │  PublicationHub (Python)            │
    │  - Validation gate         │
    │  - Manifest parser         │
    │  - Report generator        │
    └────────┬───────────┬───────┘
             │           │
      ┌──────▼────┐  ┌───▼──────────┐
      │  publication-   │  │  publication-qa-   │
      │  caption- │  │  gate-report │
      │  injection│  │  .json       │
      │  .jsx     │  └──────────────┘
      └──────┬────┘
             │
             ▼
    ┌─────────────────────┐
    │  InDesign Bridge    │
    │  - Preflight check  │
    │  - Caption inject   │
    │  - Export PDF       │
    └─────────────────────┘
```

## Troubleshooting

### "Unicode encoding error" on Windows

Already fixed in version 1.0 — uses UTF-8 with explicit encoding.

### "Manifest validation issues"

Check `publication-workflow.log` for specific issues:

```bash
# Look for ERROR entries
grep ERROR visceral-production-route/reports/publication-workflow.log
```

### InDesign script won't run

1. Ensure InDesign is open with a document
2. Confirm script file exists: `templates/publication-indesign-bridge.jsx`
3. Check InDesign console for errors: `Window > Utilities > ExtendScript Toolkit`

### Missing links in InDesign

Run preflight to locate:

```
Window > Output > Preflight
```

Relink missing images or update paths in manifest.

## Version History

### v1.0 (Current)

- ✓ Manifest validation
- ✓ Caption injection script generation
- ✓ Source register generation
- ✓ QA gate report
- ✓ InDesign preflight bridge
- ✓ Workflow orchestration
- ✓ Full UTF-8 support on Windows

## License & Attribution

This toolkit is part of the *visceral-theory-of-sight* project.

For publication guidelines, see `AGENTS.md`.

---

**Last updated:** 2026-06-06  
**Author:** Brooke Howard
