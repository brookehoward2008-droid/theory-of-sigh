#!/usr/bin/env python3
"""
Auto-run the InDesign 50-page landscape build on Windows (Adobe InDesign + COM).

This is the "auto run InDesign" wrapper. It cannot run in a Linux/cloud session
because InDesign drives the automation over COM, so run it on the Windows
machine where InDesign and the source images live.

What it does:
  1. Regenerates the production assets + the ExtendScript builder from the
     current manifest (copies the source images into the production asset
     folder and rewrites indesign-build-full-layout.jsx with correct paths).
  2. Connects to InDesign over COM and runs that .jsx, which builds the
     50-page US Letter landscape document, audits links/overset, and exports
     .indd, .idml, and a PDF.
  3. Prints a summary and points at the JSON build report.

Requirements (Windows only):
  - Adobe InDesign installed and licensed.
  - pip install pywin32
  - Source images available. build_visceral_book.py reads from the
    Windows assets path if present, else images/labeled/ in the repo.

Usage:
  python scripts/run_indesign_autobuild.py
"""
from __future__ import annotations

import platform
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

JSX = ROOT / "visceral-production-route" / "templates" / "indesign-build-full-layout.jsx"
INDD = ROOT / "visceral-production-route" / "output" / "indesign" / "the-visceral-theory-of-sight-50pp.indd"
REPORT = ROOT / "visceral-production-route" / "reports" / "indesign-full-layout-auto-report.json"

# idScriptLanguage.JAVASCRIPT (ExtendScript)
JAVASCRIPT = 1246973031
# UserInteractionLevels.NEVER_INTERACT
NEVER_INTERACT = 1699640946

# Tried oldest-last; covers common Creative Cloud builds plus the
# version-independent ProgID.
PROGIDS = [
    "InDesign.Application",
    "InDesign.Application.CC.2024",
    "InDesign.Application.2024",
    "InDesign.Application.CC.2023",
    "InDesign.Application.2023",
    "InDesign.Application.CC.2022",
    "InDesign.Application.CC.2021",
]


def regenerate_layout() -> int:
    """Copy source images and rewrite the landscape builder JSX."""
    import build_visceral_book as b

    b.ensure_dirs()
    assets = b.scan_assets()
    b.write_full_layout_jsx(assets)
    try:
        b.generate_cover(assets)
        b.generate_book(assets)
        import export_facing_pages
        export_facing_pages.export_facing_pages()
    except Exception as exc:
        print(f"  WARNING: reportlab proof regen skipped: {type(exc).__name__}: {exc}")
    print(f"  regenerated builder JSX and copied {len(assets)} assets")
    return len(assets)


def connect_indesign():
    import win32com.client as win32

    last_error = None
    for progid in PROGIDS:
        try:
            app = win32.Dispatch(progid)
            print(f"  connected to InDesign via '{progid}'")
            return app
        except Exception as exc:  # try the next ProgID
            last_error = exc
    raise RuntimeError(
        "Could not connect to InDesign over COM. Is InDesign installed and "
        f"licensed? Last error: {last_error}"
    )


def main() -> int:
    if platform.system() != "Windows":
        print(
            "This driver automates InDesign over COM and must run on Windows "
            f"with InDesign installed. Detected OS: {platform.system()}.\n"
            "Run it on the Windows machine after: pip install pywin32"
        )
        return 2

    print("Step 1/2: regenerate layout assets + builder JSX ...")
    regenerate_layout()
    if not JSX.exists():
        print(f"ERROR: builder JSX not found at {JSX}")
        return 1

    try:
        import win32com.client  # noqa: F401
    except Exception as exc:  # ImportError, or pywin32 DLL-load failure
        print("ERROR: could not import win32com (pywin32).")
        print(f"  running python: {sys.executable}")
        print(f"  real error:     {exc!r}")
        print("  Fix it for THIS interpreter, then re-run:")
        print(f'    "{sys.executable}" -m pip install --upgrade pywin32')
        print(f'    "{sys.executable}" -m pywin32_postinstall -install')
        return 1

    print("Step 2/2: launch InDesign and run the builder ...")
    app = connect_indesign()
    try:
        app.ScriptPreferences.UserInteractionLevel = NEVER_INTERACT
    except Exception as exc:
        print(f"  WARNING: could not set UserInteractionLevel: {exc}")

    start = time.time()
    try:
        app.DoScript(str(JSX), JAVASCRIPT)
    except Exception as exc:
        print(f"ERROR: InDesign reported a script failure: {exc}")
        return 1
    print(f"  build finished in {time.time() - start:.1f}s")

    print("Outputs:")
    for path in (INDD, INDD.with_suffix(".idml"), REPORT):
        print(f"  {'OK     ' if path.exists() else 'MISSING'} {path}")
    if REPORT.exists():
        print(
            "\nReview indesign-full-layout-auto-report.json for missingLinks and "
            "oversetTextFrames before final export."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
