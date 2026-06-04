from __future__ import annotations

import json
import re
from pathlib import Path

from PIL import Image, ImageOps

try:
    from scripts import build_visceral_book as book
except ModuleNotFoundError:
    import build_visceral_book as book


LETTER_W_MM = 215.9
LETTER_H_MM = 279.4
BLEED_MM = 3.175

SAFE_ASSET_DIR = book.ASSET_OUT / "preflight-konly"
SAFE_TEMPLATE = book.TEMPLATE_OUT / "indesign-build-preflight-safe.jsx"
SAFE_REPORT = book.REPORTS_OUT / "indesign-preflight-safe-generator-report.json"


def ensure_safe_assets(assets: list[book.Asset]) -> list[book.Asset]:
    SAFE_ASSET_DIR.mkdir(parents=True, exist_ok=True)
    safe_assets: list[book.Asset] = []
    for asset in assets:
        safe_path = SAFE_ASSET_DIR / f"{asset.local_path.stem}-konly.jpg"
        with Image.open(asset.local_path) as img:
            gray = ImageOps.exif_transpose(img).convert("L")
            gray.save(safe_path, format="JPEG", quality=92, optimize=True)
        safe_assets.append(
            book.Asset(
                id=asset.id,
                source_path=asset.source_path,
                local_path=safe_path,
                filename=safe_path.name,
                width=asset.width,
                height=asset.height,
                group=asset.group,
                rights=asset.rights,
                creator=asset.creator,
                title=asset.title,
                reason=asset.reason,
            )
        )
    return safe_assets


def safe_jsx_from_full(full_jsx: str, assets: list[book.Asset]) -> str:
    safe_assets = [
        {
            "id": asset.id,
            "path": asset.local_path.as_posix(),
            "title": asset.title[:58],
            "group": asset.group,
        }
        for asset in assets
    ]
    jsx = full_jsx
    jsx = jsx.replace(
        "// Builds A4 facing pages, 3mm bleed, 12-column grid, linked images, captions, layered editorial modules, PDF, and audit report.",
        "// Builds US Letter facing pages, 0.125in bleed, 12-column grid, K-only linked images, captions, layered editorial modules, PDF, and audit report.",
    )
    jsx = re.sub(r"var ASSETS = \[[\s\S]*?\];\nvar OUTPUT_INDD", "var ASSETS = " + json.dumps(safe_assets, indent=2) + ";\nvar OUTPUT_INDD", jsx, count=1)
    jsx = re.sub(
        r'var OUTPUT_INDD = .*?;\nvar OUTPUT_IDML = .*?;\nvar OUTPUT_PDF = .*?;\nvar OUTPUT_REPORT = .*?;',
        "\n".join(
            [
                f'var OUTPUT_INDD = {json.dumps((book.INDESIGN_OUT / "the-visceral-theory-of-sight-50pp-preflight-safe.indd").as_posix())};',
                f'var OUTPUT_IDML = {json.dumps((book.INDESIGN_OUT / "the-visceral-theory-of-sight-50pp-preflight-safe.idml").as_posix())};',
                f'var OUTPUT_PDF = {json.dumps((book.PDF_OUT / "the-visceral-theory-of-sight-50pp-preflight-safe.pdf").as_posix())};',
                f'var OUTPUT_REPORT = {json.dumps((book.REPORTS_OUT / "indesign-preflight-safe-build-report.json").as_posix())};',
            ]
        ),
        jsx,
        count=1,
    )
    jsx = jsx.replace(
        'function mm(v) { return v + "mm"; }\nfunction b(t, l, bot, r) { return [mm(t), mm(l), mm(bot), mm(r)]; }',
        (
            'function mm(v) { return v + "mm"; }\n'
            "var DESIGN_W_MM = 210;\n"
            "var DESIGN_H_MM = 297;\n"
            f"var PAGE_W_MM = {LETTER_W_MM};\n"
            f"var PAGE_H_MM = {LETTER_H_MM};\n"
            "function sx(v) { return v * PAGE_W_MM / DESIGN_W_MM; }\n"
            "function sy(v) { return v * PAGE_H_MM / DESIGN_H_MM; }\n"
            "function b(t, l, bot, r) { return [mm(sy(t)), mm(sx(l)), mm(sy(bot)), mm(sx(r))]; }"
        ),
    )
    jsx = jsx.replace('doc.documentPreferences.pageWidth = "210mm";', f'doc.documentPreferences.pageWidth = "{LETTER_W_MM}mm";')
    jsx = jsx.replace('doc.documentPreferences.pageHeight = "297mm";', f'doc.documentPreferences.pageHeight = "{LETTER_H_MM}mm";')
    jsx = jsx.replace('doc.documentPreferences.documentBleedTopOffset = "3mm";', f'doc.documentPreferences.documentBleedTopOffset = "{BLEED_MM}mm";')
    jsx = jsx.replace('doc.documentPreferences.documentBleedBottomOffset = "3mm";', f'doc.documentPreferences.documentBleedBottomOffset = "{BLEED_MM}mm";')
    jsx = jsx.replace('doc.documentPreferences.documentBleedInsideOrLeftOffset = "3mm";', f'doc.documentPreferences.documentBleedInsideOrLeftOffset = "{BLEED_MM}mm";')
    jsx = jsx.replace('doc.documentPreferences.documentBleedOutsideOrRightOffset = "3mm";', f'doc.documentPreferences.documentBleedOutsideOrRightOffset = "{BLEED_MM}mm";')
    jsx = jsx.replace('doc.marginPreferences.top = "20.790mm";', 'doc.marginPreferences.top = "19.558mm";')
    jsx = jsx.replace('doc.marginPreferences.bottom = "20.790mm";', 'doc.marginPreferences.bottom = "19.558mm";')
    jsx = jsx.replace('doc.marginPreferences.left = "21.000mm";', 'doc.marginPreferences.left = "21.590mm";')
    jsx = jsx.replace('doc.marginPreferences.right = "15.750mm";', 'doc.marginPreferences.right = "16.193mm";')
    jsx = re.sub(
        r"function addSwatch\(doc, name, values\) \{[\s\S]*?\n\}",
        (
            "function builtinSwatch(doc, names) {\n"
            "  for (var i = 0; i < names.length; i++) {\n"
            "    try {\n"
            "      var s = doc.swatches.itemByName(names[i]);\n"
            "      if (s && s.isValid) return s;\n"
            "    } catch (e) {}\n"
            "    try {\n"
            "      var s2 = doc.swatches.item(names[i]);\n"
            "      if (s2 && s2.isValid) return s2;\n"
            "    } catch (e2) {}\n"
            "  }\n"
            "  return doc.swatches.item(0);\n"
            "}\n"
            "function addSwatch(doc, name, values) {\n"
            '  if (name === "Archival Cream") return builtinSwatch(doc, ["Paper", "[Paper]"]);\n'
            '  return builtinSwatch(doc, ["Black", "[Black]"]);\n'
            "}"
        ),
        jsx,
        count=1,
    )
    jsx = jsx.replace('page.parent.parent.colors.itemByName("Ink")', 'page.parent.parent.swatches.itemByName("[Black]")')
    jsx = jsx.replace('"A4 precision layout. 12-column grid. 3mm bleed.', '"US Letter preflight layout. 12-column grid. 0.125in bleed.')
    jsx = jsx.replace('trim: "A4 portrait 210mm x 297mm"', 'trim: "US Letter portrait 215.9mm x 279.4mm"')
    jsx = jsx.replace('bleed: "3mm all sides"', 'bleed: "3.175mm all sides"')
    jsx = jsx.replace('"dark ink and archival cream base",', '"black and paper preflight base",')
    jsx = jsx.replace('"muted gold and slate accents",', '"black-only accent tints for Digital Publishing profile",')
    jsx = jsx.replace(
        "app.scriptPreferences.userInteractionLevel = UserInteractionLevels.NEVER_INTERACT;\n\nvar COPY =",
        "app.scriptPreferences.userInteractionLevel = UserInteractionLevels.NEVER_INTERACT;\n\ntry {\n\nvar COPY =",
        1,
    )
    jsx = jsx.replace(
        "\nsaveDesktopFiles(doc);\n",
        (
            "\nsaveDesktopFiles(doc);\n"
            "} catch (err) {\n"
            '  var errorFile = File("'
            + (book.REPORTS_OUT / "indesign-preflight-safe-error.txt").as_posix()
            + '");\n'
            "  if (!errorFile.parent.exists) errorFile.parent.create();\n"
            '  errorFile.encoding = "UTF-8";\n'
            '  errorFile.open("w");\n'
            '  errorFile.write("line: " + err.line + "\\nmessage: " + err.message + "\\nname: " + err.name);\n'
            "  errorFile.close();\n"
            "  throw err;\n"
            "}\n"
        ),
        1,
    )
    return jsx


def main() -> None:
    book.ensure_dirs()
    assets = book.scan_assets()
    safe_assets = ensure_safe_assets(assets)
    book.write_full_layout_jsx(assets)
    full_jsx = (book.TEMPLATE_OUT / "indesign-build-full-layout.jsx").read_text(encoding="utf-8")
    safe_jsx = safe_jsx_from_full(full_jsx, safe_assets)
    SAFE_TEMPLATE.write_text(safe_jsx, encoding="utf-8")
    SAFE_REPORT.write_text(
        json.dumps(
            {
                "profile_target": "Digital Publishing preflight-safe variant",
                "trim": {"width_mm": LETTER_W_MM, "height_mm": LETTER_H_MM, "name": "US Letter portrait"},
                "bleed_mm": BLEED_MM,
                "pages": 50,
                "facing_pages": True,
                "swatches": ["[Black]", "[Paper]"],
                "linked_assets": len(safe_assets),
                "asset_mode": "grayscale JPEG copies generated from supplied local image assets",
                "jsx": str(SAFE_TEMPLATE),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {SAFE_TEMPLATE}")
    print(f"Wrote {SAFE_REPORT}")
    print(f"Generated {len(safe_assets)} K-only asset copies in {SAFE_ASSET_DIR}")


if __name__ == "__main__":
    main()
