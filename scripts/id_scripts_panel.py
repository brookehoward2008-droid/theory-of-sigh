"""Shared helpers for installing ExtendScripts into InDesign's Scripts Panel.

Used by ``install_indesign_scripts.py`` (installs the repo's bundled scripts) and
``install_easybook.py`` (fetches a third-party script). InDesign exposes user
scripts placed under, per version and locale:

    macOS:   ~/Library/Preferences/Adobe InDesign/Version <v>/<locale>/Scripts/Scripts Panel
    Windows: %APPDATA%/Adobe/InDesign/Version <v>/<locale>/Scripts/Scripts Panel

Anything dropped there shows up under Window > Utilities > Scripts.
"""

from __future__ import annotations

import os
import platform
import shutil
from pathlib import Path

SCRIPT_EXTENSIONS = {".jsx", ".jsxbin"}


def default_pref_roots() -> list[Path]:
    """Return the base InDesign preferences directory for this OS (may be empty)."""
    system = platform.system()
    if system == "Darwin":
        return [Path.home() / "Library" / "Preferences" / "Adobe InDesign"]
    if system == "Windows":
        appdata = os.environ.get("APPDATA")
        base = Path(appdata) if appdata else Path.home() / "AppData" / "Roaming"
        return [base / "Adobe" / "InDesign"]
    # Linux / other: InDesign does not run here.
    return []


def find_scripts_panel_dirs(roots: list[Path], create_missing: bool = False) -> list[Path]:
    """Find every ``.../Version X/<locale>/Scripts/Scripts Panel`` directory."""
    found: list[Path] = []
    for root in roots:
        if not root.is_dir():
            continue
        for version_dir in sorted(root.glob("Version *")):
            candidates = list(version_dir.glob("*/Scripts/Scripts Panel"))
            candidates += [version_dir / "Scripts" / "Scripts Panel"]
            for cand in candidates:
                if cand.is_dir():
                    found.append(cand)
                elif create_missing and cand.parent.parent.is_dir():
                    cand.mkdir(parents=True, exist_ok=True)
                    found.append(cand)
    seen: set[Path] = set()
    unique: list[Path] = []
    for path in found:
        if path not in seen:
            seen.add(path)
            unique.append(path)
    return unique


def install_files(files: list[Path], targets: list[Path], dry_run: bool) -> int:
    """Copy each file into each target folder; return the number of copies."""
    copied = 0
    for target in targets:
        for src in files:
            dest = target / src.name
            if not dry_run:
                shutil.copy2(src, dest)
            print(f"  {'Would copy' if dry_run else 'Installed'}: {src.name} -> {dest}")
            copied += 1
    return copied


def resolve_roots(overrides: list[str]) -> list[Path]:
    """Return preference roots from CLI overrides, else OS defaults."""
    if overrides:
        return [Path(r).expanduser() for r in overrides]
    return default_pref_roots()
