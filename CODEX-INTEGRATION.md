# Codex Integration Guide

Quick reference for integrating Codex into your publication workflow.

## File Structure

```
scripts/
  ├── codex.py                    # Core Codex module
  └── codex_workflow.py           # Workflow orchestrator

visceral-production-route/
  ├── templates/
  │   ├── codex-caption-injection.jsx         # Auto-generated
  │   └── codex-indesign-bridge.jsx           # InDesign preflight
  │
  └── reports/
      ├── codex-qa-gate-report.json           # Auto-generated
      ├── codex-source-register.md            # Auto-generated
      └── codex-workflow.log                  # Auto-generated
```

## Integration Steps

### 1. Add to Existing Build Pipeline

If you have other build scripts (e.g., `build_final_document.py`), add this:

```python
# At the end of your build script
from pathlib import Path
from codex import Codex

root = Path(__file__).resolve().parents[1]
codex = Codex(root)

# Validate and generate reports
manifest = codex.load_manifest()
validation = codex.validate_manifest()

if validation["valid"]:
    print("✓ Manifest valid, generating Codex reports...")
    codex.export_qa_report()
    codex.generate_source_register_markdown()
    codex.generate_indesign_script_for_captions()
else:
    print("✗ Manifest validation failed")
    for issue in validation["issues"]:
        print(f"  - {issue}")
```

### 2. Add to GitHub Actions (CI/CD)

Create `.github/workflows/codex-qa.yml`:

```yaml
name: Codex QA Gate

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: python scripts/codex_workflow.py --validate-only
      - uses: actions/upload-artifact@v3
        if: always()
        with:
          name: codex-reports
          path: visceral-production-route/reports/
```

### 3. Add npm/Python Script Shortcut

In `package.json` (if using npm):

```json
{
  "scripts": {
    "codex:validate": "python scripts/codex.py",
    "codex:workflow": "python scripts/codex_workflow.py",
    "codex:report": "python scripts/codex_workflow.py --report"
  }
}
```

Or create a Makefile:

```makefile
.PHONY: codex codex-validate codex-report

codex:
	python scripts/codex_workflow.py

codex-validate:
	python scripts/codex_workflow.py --validate-only

codex-report:
	python scripts/codex_workflow.py --report
```

### 4. InDesign Workflow

**Automated caption injection:**

```javascript
// In your existing InDesign scripts, add:

#include "codex-caption-injection.jsx"

// This will inject captions from the manifest
// before your existing layout operations
```

**Or manually:**

1. Generate captions: `python scripts/codex_workflow.py`
2. Open InDesign document
3. File > Scripts > codex-indesign-bridge.jsx
4. Review console output for preflight results
5. Run codex-caption-injection.jsx to inject captions

## Testing

### Unit Tests (Python)

```python
# test_codex.py
from pathlib import Path
from codex import Codex

def test_manifest_loads():
    root = Path(__file__).resolve().parents[1]
    codex = Codex(root)
    manifest = codex.load_manifest()
    assert manifest.asset_count == 67

def test_validation_passes():
    codex = Codex(root)
    manifest = codex.load_manifest()
    validation = codex.validate_manifest()
    assert validation["valid"] == True
```

Run with pytest:

```bash
pytest test_codex.py -v
```

### Manual Testing

```bash
# Test 1: Validate manifest
python scripts/codex_workflow.py --validate-only

# Test 2: Generate reports
python scripts/codex_workflow.py --report

# Test 3: Full workflow
python scripts/codex_workflow.py

# Test 4: Check outputs
ls -la visceral-production-route/reports/codex-*
ls -la visceral-production-route/templates/codex-*
```

## Common Workflows

### Daily Development

```bash
# After editing manifest
python scripts/codex_workflow.py --validate-only

# Update reports
python scripts/codex_workflow.py --report

# Check InDesign
# Open InDesign → File > Scripts > codex-indesign-bridge.jsx
```

### Before Publication

```bash
# Full validation
python scripts/codex_workflow.py

# Review critical files
cat visceral-production-route/reports/codex-qa-gate-report.json
cat visceral-production-route/reports/codex-workflow.log

# Run InDesign preflight
# (see above)

# Run tests
pytest scripts/test_codex.py -v

# Export PDF and inspect visually
```

### Emergency Rollback

If something breaks:

```bash
# Check the workflow log
cat visceral-production-route/reports/codex-workflow.log

# Validate current manifest
python scripts/codex_workflow.py --validate-only

# Restore preflight-safe InDesign backup
open visceral-production-route/output/indesign/the-visceral-theory-of-sight-50pp-preflight-safe.indd
```

## Environment Variables (Optional)

You can customize Codex behavior:

```bash
# Custom manifest path
export CODEX_MANIFEST="path/to/custom-manifest.json"

# Custom output path
export CODEX_REPORTS="path/to/reports/"

# Custom template path
export CODEX_TEMPLATES="path/to/templates/"

python scripts/codex_workflow.py
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
# In codex_workflow.py
workflow = CodexWorkflow(root)
workflow.log("DEBUG", "Detailed info here")
```

Or check the workflow log:

```bash
tail -50 visceral-production-route/reports/codex-workflow.log
```

## Support

For issues or feature requests, check:

1. `CODEX.md` — Full documentation
2. `codex-workflow.log` — Execution details
3. `codex-qa-gate-report.json` — Validation status

---

**Last updated:** 2026-06-06
