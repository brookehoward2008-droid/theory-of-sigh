#!/usr/bin/env python3
"""Auto-install the easybook (``School.jsx``) InDesign script from upstream.

Run this **on your own machine** (macOS or Windows). It fetches the third-party
script from GitHub (or a local clone via ``--source``) and copies it into every
InDesign "Scripts Panel" user folder, so it appears under **Window > Utilities >
Scripts** for every InDesign version.

The script is fetched at run time and not vendored into this repo because the
upstream project ships no license.

Source: https://github.com/serjant/easybook-indesign-plugin

For scripts that ARE bundled in this repo (indesign-scripts/), use
``install_indesign_scripts.py`` instead.

Examples
--------
    python scripts/install_easybook.py                 # fetch + install
    python scripts/install_easybook.py --dry-run       # preview
    python scripts/install_easybook.py --source ./clone --prefer both
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from id_scripts_panel import find_scripts_panel_dirs, install_files, resolve_roots

REPO_URL = "https://github.com/serjant/easybook-indesign-plugin.git"
SCRIPT_NAMES = {"jsx": "School.jsx", "jsxbin": "School.jsxbin"}


def resolve_source_files(source: str | None, prefer: str, repo_url: str) -> tuple[list[Path], Path | None]:
    """Return the script files to install and a temp dir to clean up (if any)."""
    cleanup: Path | None = None
    if source:
        src_path = Path(source).expanduser()
        if src_path.is_file():
            return [src_path], None
        if not src_path.is_dir():
            raise SystemExit(f"--source path not found: {src_path}")
        base = src_path
    else:
        tmp = Path(tempfile.mkdtemp(prefix="easybook-"))
        cleanup = tmp
        print(f"Fetching {repo_url} ...")
        try:
            subprocess.run(
                ["git", "clone", "--depth", "1", repo_url, str(tmp)],
                check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            )
        except FileNotFoundError as exc:
            raise SystemExit("git is required to fetch the script (or use --source).") from exc
        except subprocess.CalledProcessError as exc:
            msg = exc.stderr.decode("utf-8", "replace") if exc.stderr else ""
            raise SystemExit(f"git clone failed: {msg.strip()}") from exc
        base = tmp

    wanted = ["jsx", "jsxbin"] if prefer == "both" else [prefer]
    files = [base / SCRIPT_NAMES[k] for k in wanted if (base / SCRIPT_NAMES[k]).is_file()]
    if not files:
        raise SystemExit(f"No {', '.join(SCRIPT_NAMES[k] for k in wanted)} found in {base}")
    return files, cleanup


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="install_easybook.py",
        description="Fetch and install the easybook School.jsx script into local InDesign.",
    )
    p.add_argument("--source", help="Local file or clone dir (default: fetch from GitHub)")
    p.add_argument("--repo-url", default=REPO_URL, help="Upstream repo URL to fetch from")
    p.add_argument("--prefer", choices=["jsx", "jsxbin", "both"], default="jsx",
                   help="Which artifact(s) to install (default: jsx)")
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

    files, cleanup = resolve_source_files(args.source, args.prefer, args.repo_url)
    try:
        print(f"Installing {', '.join(f.name for f in files)} into {len(targets)} location(s):")
        count = install_files(files, targets, args.dry_run)
    finally:
        if cleanup:
            shutil.rmtree(cleanup, ignore_errors=True)

    verb = "Would install" if args.dry_run else "Installed"
    print(f"\n{verb} {count} file(s). In InDesign: Window > Utilities > Scripts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
