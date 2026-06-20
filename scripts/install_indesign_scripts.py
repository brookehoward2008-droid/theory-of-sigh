#!/usr/bin/env python3
"""Install the repo's bundled InDesign ExtendScripts into the local Scripts Panel.

Run this **on your own machine** (macOS or Windows, where InDesign is installed).
It copies every ``.jsx`` / ``.jsxbin`` in the source folder (default:
``indesign-scripts/`` in this repo) into every InDesign "Scripts Panel" user
folder it finds — all versions and locales — so the scripts appear under
**Window > Utilities > Scripts** and are available to every InDesign session.

Examples
--------
    # Install all bundled scripts for every installed InDesign version:
    python scripts/install_indesign_scripts.py

    # Preview without copying:
    python scripts/install_indesign_scripts.py --dry-run

    # Install from a different folder, or a single file:
    python scripts/install_indesign_scripts.py --source path/to/scripts
    python scripts/install_indesign_scripts.py --source path/to/MyScript.jsx

There is no InDesign on a headless cloud machine — run this locally.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from id_scripts_panel import (
    SCRIPT_EXTENSIONS,
    find_scripts_panel_dirs,
    install_files,
    resolve_roots,
)

# Default source: the indesign-scripts/ folder next to this repo's scripts/ dir.
DEFAULT_SOURCE = Path(__file__).resolve().parent.parent / "indesign-scripts"


def collect_scripts(source: Path) -> list[Path]:
    if source.is_file():
        if source.suffix.lower() not in SCRIPT_EXTENSIONS:
            raise SystemExit(f"Not an ExtendScript file: {source}")
        return [source]
    if not source.is_dir():
        raise SystemExit(f"Source not found: {source}")
    files = sorted(
        p for p in source.iterdir()
        if p.is_file() and p.suffix.lower() in SCRIPT_EXTENSIONS
    )
    if not files:
        raise SystemExit(f"No .jsx/.jsxbin scripts found in {source}")
    return files


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="install_indesign_scripts.py",
        description="Install bundled InDesign ExtendScripts into local Scripts Panel folders.",
    )
    p.add_argument("--source", default=str(DEFAULT_SOURCE),
                   help="Folder of scripts or a single .jsx/.jsxbin (default: indesign-scripts/)")
    p.add_argument("--indesign-root", action="append", default=[],
                   help="Override InDesign preferences base dir (repeatable; for testing)")
    p.add_argument("--create-missing", action="store_true",
                   help="Create the Scripts Panel folder when a version's Scripts folder exists")
    p.add_argument("--dry-run", action="store_true", help="Show what would happen without copying")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)

    roots = resolve_roots(args.indesign_root)
    if not roots:
        print(
            "No InDesign preferences location is known for this OS. InDesign runs "
            "on macOS/Windows — run this there, or pass --indesign-root.",
            file=sys.stderr,
        )
        return 2

    targets = find_scripts_panel_dirs(roots, create_missing=args.create_missing)
    if not targets:
        print(
            "No InDesign 'Scripts Panel' folders found under:\n  "
            + "\n  ".join(str(r) for r in roots)
            + "\nIs InDesign installed and launched at least once? "
            "Try --indesign-root or --create-missing.",
            file=sys.stderr,
        )
        return 1

    files = collect_scripts(Path(args.source).expanduser())
    names = ", ".join(f.name for f in files)
    print(f"Installing {len(files)} script(s) [{names}] into {len(targets)} location(s):")
    count = install_files(files, targets, args.dry_run)

    verb = "Would install" if args.dry_run else "Installed"
    print(f"\n{verb} {count} file(s). In InDesign: Window > Utilities > Scripts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
