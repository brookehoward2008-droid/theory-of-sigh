#!/usr/bin/env python3
"""Auto-install the easybook (``School.jsx``) script into the local InDesign.

Run this **on your own machine** (macOS or Windows) where Adobe InDesign is
installed. It locates every InDesign "Scripts Panel" user folder — across all
installed versions and locales — and copies the script there. After it runs,
the script shows up in InDesign under **Window > Utilities > Scripts** (double-
click to run), and is available to every InDesign session and to automation
that drives InDesign via "do script".

Source: https://github.com/serjant/easybook-indesign-plugin

Examples
--------
    # Fetch the script from GitHub and install it for all InDesign versions:
    python scripts/install_easybook.py

    # Install from a local clone instead of fetching:
    python scripts/install_easybook.py --source /path/to/easybook-indesign-plugin

    # See what would happen without copying anything:
    python scripts/install_easybook.py --dry-run

This cannot run against InDesign from a headless cloud machine — there is no
InDesign there. Run it locally.
"""

from __future__ import annotations

import argparse
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_URL = "https://github.com/serjant/easybook-indesign-plugin.git"
SCRIPT_NAMES = {"jsx": "School.jsx", "jsxbin": "School.jsxbin"}


def default_pref_roots() -> list[Path]:
    """Return the base InDesign preferences directory for this OS."""
    system = platform.system()
    if system == "Darwin":
        return [Path.home() / "Library" / "Preferences" / "Adobe InDesign"]
    if system == "Windows":
        appdata = os.environ.get("APPDATA")
        if appdata:
            return [Path(appdata) / "Adobe" / "InDesign"]
        return [Path.home() / "AppData" / "Roaming" / "Adobe" / "InDesign"]
    # Linux / other: InDesign does not run here.
    return []


def find_scripts_panel_dirs(roots: list[Path], create_missing: bool) -> list[Path]:
    """Find every ``.../Version X/<locale>/Scripts/Scripts Panel`` directory."""
    found: list[Path] = []
    for root in roots:
        if not root.is_dir():
            continue
        for version_dir in sorted(root.glob("Version *")):
            # Standard layout includes a locale folder (e.g. en_US); also handle
            # the rare case where Scripts sits directly under the version dir.
            candidates = list(version_dir.glob("*/Scripts/Scripts Panel"))
            candidates += [version_dir / "Scripts" / "Scripts Panel"]
            for cand in candidates:
                if cand.is_dir():
                    found.append(cand)
                elif create_missing and cand.parent.parent.is_dir():
                    # Only create when the locale/Scripts parent already exists.
                    cand.mkdir(parents=True, exist_ok=True)
                    found.append(cand)
    # De-duplicate while preserving order.
    seen: set[Path] = set()
    unique: list[Path] = []
    for path in found:
        if path not in seen:
            seen.add(path)
            unique.append(path)
    return unique


def resolve_source_files(source: str | None, prefer: str, repo_url: str) -> tuple[list[Path], Path | None]:
    """Return the script files to install, and a temp dir to clean up (if any).

    ``prefer`` is one of ``jsx``, ``jsxbin``, or ``both``.
    """
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
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
            )
        except FileNotFoundError as exc:
            raise SystemExit("git is required to fetch the script (or use --source).") from exc
        except subprocess.CalledProcessError as exc:
            msg = exc.stderr.decode("utf-8", "replace") if exc.stderr else ""
            raise SystemExit(f"git clone failed: {msg.strip()}") from exc
        base = tmp

    wanted = ["jsx", "jsxbin"] if prefer == "both" else [prefer]
    files: list[Path] = []
    for kind in wanted:
        candidate = base / SCRIPT_NAMES[kind]
        if candidate.is_file():
            files.append(candidate)
    if not files:
        raise SystemExit(f"No {', '.join(SCRIPT_NAMES[k] for k in wanted)} found in {base}")
    return files, cleanup


def install(files: list[Path], targets: list[Path], dry_run: bool) -> int:
    copied = 0
    for target in targets:
        for src in files:
            dest = target / src.name
            action = "Would copy" if dry_run else "Installed"
            if not dry_run:
                shutil.copy2(src, dest)
            print(f"  {action}: {src.name} -> {dest}")
            copied += 1
    return copied


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="install_easybook.py",
        description="Install the easybook School.jsx script into local InDesign Scripts Panel folders.",
    )
    p.add_argument("--source", help="Local file or clone dir to install from (default: fetch from GitHub)")
    p.add_argument("--repo-url", default=REPO_URL, help="Upstream repo URL to fetch from")
    p.add_argument("--prefer", choices=["jsx", "jsxbin", "both"], default="jsx",
                   help="Which artifact(s) to install (default: jsx)")
    p.add_argument("--indesign-root", action="append", default=[],
                   help="Override InDesign preferences base dir (repeatable; for testing/custom installs)")
    p.add_argument("--create-missing", action="store_true",
                   help="Create the Scripts Panel folder when a version's Scripts folder exists but the panel folder doesn't")
    p.add_argument("--dry-run", action="store_true", help="Show what would happen without copying")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)

    roots = [Path(r).expanduser() for r in args.indesign_root] or default_pref_roots()
    if not roots:
        print(
            "No InDesign preferences location is known for this OS "
            f"({platform.system()}). InDesign runs on macOS/Windows — run this "
            "installer there, or pass --indesign-root.",
            file=sys.stderr,
        )
        return 2

    targets = find_scripts_panel_dirs(roots, create_missing=args.create_missing)
    if not targets:
        print(
            "No InDesign 'Scripts Panel' folders found under:\n  "
            + "\n  ".join(str(r) for r in roots)
            + "\nIs InDesign installed and launched at least once? "
            "You can pass --indesign-root or --create-missing.",
            file=sys.stderr,
        )
        return 1

    files, cleanup = resolve_source_files(args.source, args.prefer, args.repo_url)
    try:
        print(f"Installing {', '.join(f.name for f in files)} into {len(targets)} location(s):")
        count = install(files, targets, args.dry_run)
    finally:
        if cleanup:
            shutil.rmtree(cleanup, ignore_errors=True)

    verb = "Would install" if args.dry_run else "Installed"
    print(f"\n{verb} {count} file(s). In InDesign: Window > Utilities > Scripts.")
    if not args.dry_run:
        print("If InDesign is open, the script appears immediately (or after reopening the Scripts panel).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
