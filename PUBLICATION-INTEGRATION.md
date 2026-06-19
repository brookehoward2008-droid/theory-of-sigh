# Publication Automation — Integration Guide

Quick reference for integrating the publication toolkit into your workflow.

## File Structure

```
scripts/
  ├── publication_hub.py                    # Core PublicationHub module
  └── publication_workflow.py           # Workflow orchestrator

visceral-production-route/
  ├── templates/
  │   ├── publication-caption-injection.jsx         # Auto-generated
  │   └── publication-indesign-bridge.jsx           # InDesign preflight
  │
  └── reports/
      ├── publication-qa-gate-report.json           # Auto-generated
      ├── publication-source-register.md            # Auto-generated
      └── publication-workflow.log                  # Auto-generated
```

## Integration Steps

### 1. Add to Existing Build Pipeline

If you have other build scripts (e.g., `build_final_document.py`), add this:

```python
# At the end of your build script
from pathlib import Path
from publication_hub import PublicationHub

root = Path(__file__).resolve().parents[1]
publication_hub = PublicationHub(root)

# Validate and generate reports
manifest = publication_hub.load_manifest()
validation = publication_hub.validate_manifest()

if validation["valid"]:
    print("✓ Manifest valid, generating reports...")
    publication_hub.export_qa_report()
    publication_hub.generate_source_register_markdown()
    publication_hub.generate_indesign_script_for_captions()
else:
    print("✗ Manifest validation failed")
    for issue in validation["issues"]:
        print(f"  - {issue}")
```

### 2. Add to GitHub Actions (CI/CD)

Create `.github/workflows/publication-qa.yml`:

```yaml
name: Publication QA Gate

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: python scripts/publication_workflow.py --validate-only
      - uses: actions/upload-artifact@v3
        if: always()
        with:
          name: publication-reports
          path: visceral-production-route/reports/
```

### 3. Add npm/Python Script Shortcut

In `package.json` (if using npm):

```json
{
  "scripts": {
    "publication:validate": "python scripts/publication_hub.py",
    "publication:workflow": "python scripts/publication_workflow.py",
    "publication:report": "python scripts/publication_workflow.py --report"
  }
}
```

Or create a Makefile:

```makefile
.PHONY: publication_hub publication-validate publication-report

publication_hub:
	python scripts/publication_workflow.py

publication-validate:
	python scripts/publication_workflow.py --validate-only

publication-report:
	python scripts/publication_workflow.py --report
```

### 4. InDesign Workflow

**Automated caption injection:**

```javascript
// In your existing InDesign scripts, add:

#include "publication-caption-injection.jsx"

// This will inject captions from the manifest
// before your existing layout operations
```

**Or manually:**

1. Generate captions: `python scripts/publication_workflow.py`
2. Open InDesign document
3. File > Scripts > publication-indesign-bridge.jsx
4. Review console output for preflight results
5. Run publication-caption-injection.jsx to inject captions

## Testing

### Unit Tests (Python)

```python
# test_publication_hub.py
from pathlib import Path
from publication_hub import PublicationHub

def test_manifest_loads():
    root = Path(__file__).resolve().parents[1]
    publication_hub = PublicationHub(root)
    manifest = publication_hub.load_manifest()
    assert manifest.asset_count == 64

def test_validation_passes():
    publication_hub = PublicationHub(root)
    manifest = publication_hub.load_manifest()
    validation = publication_hub.validate_manifest()
    assert validation["valid"] == True
```

Run with pytest:

```bash
pytest test_publication_hub.py -v
```

### Manual Testing

```bash
# Test 1: Validate manifest
python scripts/publication_workflow.py --validate-only

# Test 2: Generate reports
python scripts/publication_workflow.py --report

# Test 3: Full workflow
python scripts/publication_workflow.py

# Test 4: Check outputs
ls -la visceral-production-route/reports/publication-*
ls -la visceral-production-route/templates/publication-*
```

## Common Workflows

### Daily Development

```bash
# After editing manifest
python scripts/publication_workflow.py --validate-only

# Update reports
python scripts/publication_workflow.py --report

# Check InDesign
# Open InDesign → File > Scripts > publication-indesign-bridge.jsx
```

### Before Publication

```bash
# Full validation
python scripts/publication_workflow.py

# Review critical files
cat visceral-production-route/reports/publication-qa-gate-report.json
cat visceral-production-route/reports/publication-workflow.log

# Run InDesign preflight
# (see above)

# Run tests
pytest scripts/test_publication_hub.py -v

# Export PDF and inspect visually
```

### Emergency Rollback

If something breaks:

```bash
# Check the workflow log
cat visceral-production-route/reports/publication-workflow.log

# Validate current manifest
python scripts/publication_workflow.py --validate-only

# Restore preflight-safe InDesign backup
open visceral-production-route/output/indesign/the-visceral-theory-of-sight-50pp-preflight-safe.indd
```

## Environment Variables (Optional)

You can customize the toolkit's behavior:

```bash
# Custom manifest path
export PUBLICATION_MANIFEST="path/to/custom-manifest.json"

# Custom output path
export PUBLICATION_REPORTS="path/to/reports/"

# Custom template path
export PUBLICATION_TEMPLATES="path/to/templates/"

python scripts/publication_workflow.py
```

## Performance

- Manifest loading: ~50ms
- Validation: ~100ms
- Report generation: ~200ms
- **Total workflow: <1s**

Suitable for real-time CI/CD pipelines.

## Debugging

Enable verbose logging:

```python
# In publication_workflow.py
workflow = PublicationWorkflow(root)
workflow.log("DEBUG", "Detailed info here")
```

Or check the workflow log:

```bash
tail -50 visceral-production-route/reports/publication-workflow.log
```

## Support

For issues or feature requests, check:

1. `PUBLICATION-AUTOMATION.md` — Full documentation
2. `publication-workflow.log` — Execution details
3. `publication-qa-gate-report.json` — Validation status

---

**Last updated:** 2026-06-06
