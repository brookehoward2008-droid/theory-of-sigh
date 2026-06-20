#!/usr/bin/env python3
"""Package the print-kit fonts (Gloock + Cormorant Garamond) with clean,
InDesign-resolvable family/style names, derived from the vendored OFL faces in
assets/fonts/. Output goes to a "Document Fonts" folder you place next to the
.indd so InDesign auto-activates them (no missing fonts).

Usage:  python scripts/prepare_print_fonts.py [output_dir]
        default output_dir = visceral-production-route/print-kit/Document Fonts
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "fonts"


def rename(src: Path, dst: Path, family: str, subfamily: str, italic: bool = False, bold: bool = False) -> None:
    font = TTFont(str(src))
    name = font["name"]
    full = f"{family} {subfamily}".strip()
    ps = (family + "-" + subfamily).replace(" ", "")
    values = {1: family, 2: subfamily, 4: full, 6: ps, 16: family, 17: subfamily}
    for nid, val in values.items():
        name.setName(val, nid, 3, 1, 0x409)  # Windows
        name.setName(val, nid, 1, 0, 0)       # Mac
    os2, head = font["OS/2"], font["head"]
    fs = os2.fsSelection & ~((1 << 0) | (1 << 5) | (1 << 6))  # clear italic/bold/regular
    mac = head.macStyle & ~0b11
    if italic:
        fs |= (1 << 0); mac |= 0b10
    if bold:
        fs |= (1 << 5); mac |= 0b01
    if not italic and not bold:
        fs |= (1 << 6)
    os2.fsSelection, head.macStyle = fs, mac
    dst.parent.mkdir(parents=True, exist_ok=True)
    font.save(str(dst))
    print(f"  {dst.name:34} family={family!r} style={subfamily!r}")


def main() -> None:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "visceral-production-route" / "print-kit" / "Document Fonts"
    out.mkdir(parents=True, exist_ok=True)
    # Gloock — already clean
    shutil.copy(SRC / "Gloock-Regular.ttf", out / "Gloock-Regular.ttf")
    print(f"  {'Gloock-Regular.ttf':34} family='Gloock' style='Regular'")
    # Cormorant Garamond — vendored faces carry inconsistent internal names; normalize
    rename(SRC / "CormorantGaramond-Medium.ttf", out / "CormorantGaramond-Regular.ttf", "Cormorant Garamond", "Regular")
    rename(SRC / "CormorantGaramond-MediumItalic.ttf", out / "CormorantGaramond-Italic.ttf", "Cormorant Garamond", "Italic", italic=True)
    rename(SRC / "CormorantGaramond-SemiBold.ttf", out / "CormorantGaramond-SemiBold.ttf", "Cormorant Garamond", "SemiBold", bold=True)
    for lic in ("Gloock-OFL.txt", "CormorantGaramond-OFL.txt"):
        if (SRC / lic).exists():
            shutil.copy(SRC / lic, out / lic)
    print(f"Done -> {out}")


if __name__ == "__main__":
    main()
