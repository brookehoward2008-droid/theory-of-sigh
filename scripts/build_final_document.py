from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path

from PIL import Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from scripts.shared.paths import ROOT, ROUTE
from scripts.shared.pdf_helpers import draw_text_block as _shared_draw_text_block
from scripts.shared.pdf_helpers import text_lines

MERGE_DIR = ROUTE / "assets" / "final-11-image-merge"
MANIFEST_CSV = MERGE_DIR / "manifest.csv"
PDF_OUT = ROUTE / "output" / "pdf"
REPORT_OUT = ROUTE / "reports"
TEMPLATE_OUT = ROUTE / "templates"
FINAL_PDF = PDF_OUT / "the-visceral-theory-of-sight-final-refined.pdf"
FINAL_REPORT = REPORT_OUT / "final-refined-build-report.md"
ASSET_REGISTER_MD = REPORT_OUT / "asset-register.md"
ASSET_SHEET_JSX = TEMPLATE_OUT / "final-11-image-asset-sheet.jsx"
APPLY_LAYOUT_REFINE_JSX = TEMPLATE_OUT / "apply-final-11-to-layout-refine.jsx"
INDESIGN_AUTOBUILD_REPORT = REPORT_OUT / "layout-refine-autobuild-report.txt"
LAYOUT_REFINE_INDD = Path(
    r"C:\Users\toddl\OneDrive\Desktop\SCHOOL\Graph252 booklab\visceral-theory of sight assets\layout refine.indd"
)
LAYOUT_REFINE_OUTPUT_INDD = LAYOUT_REFINE_INDD.with_name("layout refine_FINAL_AUTOBUILD.indd")

PAGE_W, PAGE_H = letter
BLEED = 9
MARGIN = 48
INK = colors.HexColor("#11100E")
CREAM = colors.HexColor("#F2E9DC")
PAPER = colors.HexColor("#FCFAF5")
RUST = colors.HexColor("#9B3F2D")
GOLD = colors.HexColor("#A58242")
SLATE = colors.HexColor("#314957")
MIST = colors.HexColor("#D8D0C0")
SOFT_BLACK = colors.HexColor("#171717")

HARMONIC_MARGIN_REPORT_LINES = [
    "- Inside margin: 0.75 in",
    "- Top margin: 0.85 in (0.75 x 1.1333)",
    "- Outside margin: 0.90 in (0.75 x 1.2000)",
    "- Bottom margin: 1.00 in (0.75 x 1.3333)",
    "- Column system: 12 columns with 0.1667 in gutters",
    "- Baseline system: 15 pt textual leading aligned to 7.5 pt master subdivisions",
]

METRIC_BLOCK_REPORT_LINES = [
    "- Core Latitude Anchor: 45.6 deg N (calculated solar angle progression)",
    "- Textual Leading Baseline: 15 pt (aligned to 7.5 pt master layout subdivisions)",
    "- Primary Contrast Threshold: 8:1 Evident Range",
    "- Typographic Boundary: 12-column grid lock with zero-bleed text constraints",
    "- Exposure Range: EV 12-14",
    "- Contrast Ratio: 8:1 structured shadow depth",
    "- Structural Axis: 45-degree convergence",
    "- Lens Architecture: 35mm perspective control tilt-shift",
    "- Spectrum: Monochromatic architectural calibration",
]

HARMONIC_MARGIN_JSX_TEXT = (
    "HARMONIC MARGIN ALGORITHM\\r\\r"
    "Instead of uniform margins, this build expands outward from the inside gutter to create optical spread balance.\\r"
    "Inside Margin: 0.75 in\\r"
    "Top Margin: 0.85 in (0.75 x 1.1333)\\r"
    "Outside Margin: 0.90 in (0.75 x 1.2000)\\r"
    "Bottom Margin: 1.00 in (0.75 x 1.3333)\\r"
    "Column System: 12-column grid lock; 0.1667 in gutters\\r"
    "Baseline System: 15 pt leading aligned to 7.5 pt master layout subdivisions"
)

METRIC_BLOCK_JSX_TEXT = (
    "METRIC BLOCK: SPECIFICATION DATA ARCHIVE // DIAGRAM 04-B\\r"
    "- Core Latitude Anchor: 45.6 deg N (Calculated Solar Angle Progression)\\r"
    "- Textual Leading Baseline: 15 pt (Aligned to 7.5 pt Master Layout Subdivisions)\\r"
    "- Primary Contrast Threshold: 8:1 Evident Range\\r"
    "- Typographic Boundary: 12-Column Grid Lock (Strict Zero-Bleed Text Constraints)\\r\\r"
    "METRIC DATA // CH. 2\\r"
    "- Exposure Range: EV 12-14\\r"
    "- Contrast Ratio: 8:1 structured shadow depth\\r"
    "- Structural Axis: 45-degree convergence\\r"
    "- Lens Architecture: 35mm perspective control tilt-shift\\r"
    "- Spectrum: Monochromatic architectural calibration"
)


@dataclass(frozen=True)
class ManifestRow:
    image_file: str
    title: str
    section: str
    placement: str
    caption: str
    image_path: Path


def load_manifest_rows(path: Path = MANIFEST_CSV) -> list[ManifestRow]:
    rows: list[ManifestRow] = []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            image_file = row["@ImageFile"].strip()
            rows.append(
                ManifestRow(
                    image_file=image_file,
                    title=row["Title"].strip(),
                    section=row["Section"].strip(),
                    placement=row["PagePlacement"].strip(),
                    caption=row["CaptionText"].strip(),
                    image_path=path.parent / image_file,
                )
            )
    return rows


def ensure_output_dirs() -> None:
    PDF_OUT.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.mkdir(parents=True, exist_ok=True)
    TEMPLATE_OUT.mkdir(parents=True, exist_ok=True)
    (ROUTE / "tmp").mkdir(parents=True, exist_ok=True)


def draw_full_bleed_image(c: canvas.Canvas, image_path: Path) -> None:
    with Image.open(image_path) as img:
        src_w, src_h = img.size
    scale = max((PAGE_W + (BLEED * 2)) / src_w, (PAGE_H + (BLEED * 2)) / src_h)
    draw_w = src_w * scale
    draw_h = src_h * scale
    x = (PAGE_W - draw_w) / 2
    y = (PAGE_H - draw_h) / 2
    c.drawImage(ImageReader(str(image_path)), x, y, width=draw_w, height=draw_h, preserveAspectRatio=True, mask="auto")


def draw_image_fit(c: canvas.Canvas, image_path: Path, x: float, y: float, w: float, h: float) -> None:
    with Image.open(image_path) as img:
        src_w, src_h = img.size
    scale = min(w / src_w, h / src_h)
    draw_w = src_w * scale
    draw_h = src_h * scale
    c.drawImage(
        ImageReader(str(image_path)),
        x + ((w - draw_w) / 2),
        y + ((h - draw_h) / 2),
        width=draw_w,
        height=draw_h,
        preserveAspectRatio=True,
        mask="auto",
    )


def draw_wrapped(
    c: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    width_chars: int,
    size: float,
    leading: float,
    font: str = "Helvetica",
    color=INK,
    max_lines: int | None = None,
) -> float:
    return _shared_draw_text_block(
        c, text, x, y, width_chars, leading, size, font, color, max_lines,
    )


def draw_footer(c: canvas.Canvas, page_num: int, section: str, dark: bool = False) -> None:
    color = CREAM if dark else SLATE
    c.setFont("Helvetica", 7)
    c.setFillColor(color)
    c.drawString(MARGIN, 24, "THE VISCERAL THEORY OF SIGHT")
    c.drawCentredString(PAGE_W / 2, 24, section.upper())
    c.drawRightString(PAGE_W - MARGIN, 24, f"{page_num:02d}")


def draw_cover(c: canvas.Canvas, row: ManifestRow) -> None:
    draw_full_bleed_image(c, row.image_path)
    c.setFillColor(colors.Color(0, 0, 0, alpha=0.48))
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(CREAM)
    c.setFont("Helvetica-Bold", 31)
    c.drawString(MARGIN, 582, "THE VISCERAL")
    c.drawString(MARGIN, 545, "THEORY OF SIGHT")
    c.setFont("Times-Italic", 14)
    draw_wrapped(
        c,
        "A focused visual essay on concealment, attention, and the eye as a learning boundary.",
        MARGIN,
        510,
        54,
        13,
        18,
        "Times-Italic",
        CREAM,
    )
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.line(MARGIN, 492, MARGIN + 208, 492)
    c.setFont("Helvetica", 11)
    c.setFillColor(CREAM)
    c.drawString(MARGIN, 472, "Brooke Chauntel")
    c.setFont("Helvetica", 9)
    c.setFillColor(MIST)
    c.drawString(MARGIN, 454, "Everett Community College · 2026")
    c.showPage()


def draw_toc(c: canvas.Canvas, rows: list[ManifestRow]) -> None:
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(MARGIN, 704, "VISUAL ROUTE")
    intro = (
        "This build keeps the reading path short, visual, and verifiable. The captions describe only what is visible "
        "in the local image files. Source URLs, license status, and scholarly citations remain a separate final-check task."
    )
    draw_wrapped(c, intro, MARGIN, 674, 78, 10.5, 15, "Helvetica", SLATE)
    c.setStrokeColor(RUST)
    c.setLineWidth(1.2)
    c.line(MARGIN, 624, PAGE_W - MARGIN, 624)

    y = 590
    for index, row in enumerate(rows, start=3):
        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(INK)
        c.drawString(MARGIN, y, f"{index:02d}")
        c.drawString(MARGIN + 34, y, row.title)
        c.setFont("Helvetica", 8.5)
        c.setFillColor(SLATE)
        c.drawString(300, y, row.section)
        c.drawRightString(PAGE_W - MARGIN, y, row.placement)
        y -= 24

    draw_footer(c, 2, "route")
    c.showPage()


def draw_section_page(c: canvas.Canvas, row: ManifestRow, page_num: int, section_index: int) -> None:
    dark = row.section in {"Avant-Garde", "Cinematic Grain"}
    c.setFillColor(SOFT_BLACK if dark else CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    if row.placement in {"Left-FullBleed", "Right-FullBleed", "Full-Spread", "Center-Spread"}:
        draw_full_bleed_image(c, row.image_path)
        c.setFillColor(colors.Color(0, 0, 0, alpha=0.38 if dark else 0.22))
        c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        text_x = MARGIN if "Left" not in row.placement else PAGE_W * 0.49
        text_w = 42
        text_color = CREAM
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(GOLD)
        c.drawString(text_x, 674, f"{row.section.upper()} / {row.placement.upper()}")
        c.setFont("Helvetica-Bold", 25)
        c.setFillColor(text_color)
        c.drawString(text_x, 638, row.title.upper())
        draw_wrapped(c, row.caption, text_x, 604, text_w, 10.5, 15, "Helvetica", text_color, max_lines=6)
        draw_footer(c, page_num, row.section, dark=True)
    else:
        img_x = MARGIN
        img_y = 318
        img_w = PAGE_W - (MARGIN * 2)
        img_h = 374
        draw_image_fit(c, row.image_path, img_x, img_y, img_w, img_h)
        c.setStrokeColor(GOLD)
        c.setLineWidth(1.2)
        c.rect(img_x, img_y, img_w, img_h, fill=0, stroke=1)
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(RUST)
        c.drawString(MARGIN, 282, f"{row.section.upper()} / {row.placement.upper()}")
        c.setFont("Helvetica-Bold", 24)
        c.setFillColor(INK)
        c.drawString(MARGIN, 248, row.title.upper())
        draw_wrapped(c, row.caption, MARGIN, 220, 82, 10.5, 15, "Helvetica", SLATE, max_lines=5)
        draw_footer(c, page_num, row.section)

    c.setFont("Helvetica", 7)
    c.setFillColor(GOLD if dark else RUST)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 36, f"VISUAL NODE {section_index:02d}")
    c.showPage()


def draw_back_matter(c: canvas.Canvas, rows: list[ManifestRow]) -> None:
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(MARGIN, 704, "FINAL CHECKLIST")
    checklist = (
        "The document is built from the verified local merge folder. It does not invent publication dates, source URLs, "
        "license status, or scholarly quotations. Before public upload or print, verify each image source and any required "
        "course citation format."
    )
    draw_wrapped(c, checklist, MARGIN, 674, 76, 10.5, 15, "Helvetica", SLATE)
    c.setStrokeColor(GOLD)
    c.line(MARGIN, 624, PAGE_W - MARGIN, 624)
    y = 592
    for row in rows:
        c.setFont("Helvetica-Bold", 8.5)
        c.setFillColor(INK)
        c.drawString(MARGIN, y, row.title)
        c.setFont("Helvetica", 7.5)
        c.setFillColor(SLATE)
        c.drawString(MARGIN + 170, y, row.image_file[:72])
        y -= 20

    c.setStrokeColor(RUST)
    c.line(MARGIN, y - 4, PAGE_W - MARGIN, y - 4)
    y -= 24
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(INK)
    c.drawString(MARGIN, y, "HARMONIC MARGIN + METRIC ARCHIVE")
    y -= 14
    archive_lines = [
        "Inside 0.75 in / Top 0.85 in / Outside 0.90 in / Bottom 1.00 in",
        "Textual Leading Baseline: 15 pt aligned to 7.5 pt master subdivisions",
        "Primary Contrast Threshold: 8:1 Evident Range / Exposure Range: EV 12-14",
        "Structural Axis: 45-degree convergence / Lens Architecture: 35mm perspective control tilt-shift",
    ]
    for line in archive_lines:
        c.setFont("Helvetica", 7.3)
        c.setFillColor(SLATE)
        c.drawString(MARGIN, y, line)
        y -= 11
    draw_footer(c, 14, "verification")
    c.showPage()


def write_report(rows: list[ManifestRow], output: Path) -> None:
    missing = [row.image_file for row in rows if not row.image_path.exists()]
    lines = [
        "# Final Refined Build Report",
        "",
        f"- PDF: `{output}`",
        f"- Manifest: `{MANIFEST_CSV}`",
        f"- Image rows: {len(rows)}",
        f"- Missing images: {len(missing)}",
        "- Build stance: descriptive captions only; no invented citations, source URLs, dates, or license claims.",
        "- Refinement stance: short section labels, large image fields, compact captions, and clear page numbering.",
        "",
        "## Pages",
        "",
        "1. Cover",
        "2. Visual Route",
    ]
    for index, row in enumerate(rows, start=3):
        lines.append(f"{index}. {row.title} - {row.section} - {row.placement}")
    lines.append("14. Final Checklist")
    lines.extend(
        [
            "",
            "## Harmonic Margin Algorithm",
            "",
            "Instead of uniform margins, the build expands outward from the inside gutter to create optical spread balance.",
        ]
    )
    lines.extend(HARMONIC_MARGIN_REPORT_LINES)
    lines.extend(["", "## Metric Block", ""])
    lines.extend(METRIC_BLOCK_REPORT_LINES)
    if missing:
        lines.extend(["", "## Missing", ""])
        lines.extend(f"- {name}" for name in missing)
    FINAL_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def creator_from_filename(image_file: str) -> str:
    if "unsplash" not in image_file.lower():
        return "Creator/source not verified"
    stem = image_file
    for suffix in ["_2.jpg", ".jpg", ".jpeg", ".png"]:
        if stem.lower().endswith(suffix):
            stem = stem[: -len(suffix)]
            break
    stem = stem.replace("-unsplash", "")
    parts = stem.split("-")
    creator_words: list[str] = []
    for part in parts:
        if any(char.isdigit() for char in part) or "_" in part:
            break
        creator_words.append(part)
    creator = " ".join(word.capitalize() for word in creator_words).strip()
    if not creator:
        return "Unsplash filename present; creator not verified"
    return f"{creator} / Unsplash filename present; source URL not verified"


def build_asset_register(output: Path = ASSET_REGISTER_MD) -> Path:
    ensure_output_dirs()
    rows = load_manifest_rows(MANIFEST_CSV)
    missing = [row for row in rows if not row.image_path.exists()]
    lines = [
        "================================================================================",
        "ASSET REGISTER: VERIFIED IMAGES & VECTORS",
        "================================================================================",
        "[Asset ID]    [Resource File Path]                                      [Source / Creator Attribution]",
        "--------------------------------------------------------------------------------",
    ]
    for index, row in enumerate(rows, start=1):
        asset_id = f"IMG_{index:02d}"
        resource = f"final-11-image-merge/{row.image_file}"
        creator = creator_from_filename(row.image_file)
        lines.append(f"{asset_id:<13} {resource:<57} {creator}")
    lines.extend(
        [
            "================================================================================",
            "",
            "VECTOR STATUS",
            "--------------------------------------------------------------------------------",
            "No verified vector files were found in the final-11-image-merge package.",
            "Do not list sample image or vector placeholders as production assets until matching local files exist.",
            "",
            "Verification stance: filenames and local file existence are verified; source URLs,",
            "license status, and creator attribution beyond filename parsing remain manual checks.",
        ]
    )
    if missing:
        lines.extend(["", "MISSING IMAGE FILES", "--------------------------------------------------------------------------------"])
        lines.extend(f"- {row.image_file}" for row in missing)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output


def bounds_for_placement(placement: str) -> list[float]:
    if placement in {"Left-FullBleed", "Right-FullBleed", "Full-Spread", "Center-Spread"}:
        return [-0.125, -0.125, 11.125, 8.625]
    if placement in {"Left-Grid", "Right-Grid"}:
        return [1.0, 0.9, 10.0, 7.6]
    return [1.25, 1.15, 8.75, 7.35]


def jsx_string(value: str | Path) -> str:
    text = value.as_posix() if isinstance(value, Path) else str(value)
    return json.dumps(text)


def indesign_asset_sheet_lines(rows: list[ManifestRow], absolute_asset_root: bool = False) -> list[str]:
    asset_root: str | Path = MERGE_DIR if absolute_asset_root else "final-11-image-merge/"
    lines = [
        "// Final 11-image asset sheet for InDesign ExtendScript.",
        "// Place this beside the final-11-image-merge folder or adjust ASSET_ROOT.",
        "var ASSET_ROOT = " + jsx_string(asset_root) + ";",
    ]
    if absolute_asset_root:
        lines.append('if (ASSET_ROOT.charAt(ASSET_ROOT.length - 1) !== "/") ASSET_ROOT += "/";')
    lines.extend([
        "var assetSheet = [",
    ])
    for index, row in enumerate(rows, start=3):
        bounds = ", ".join(f"{value:.3g}" for value in bounds_for_placement(row.placement))
        lines.extend(
            [
                "    {",
                f"        page: {index},",
                '        type: "image",',
                '        layer: "BACKGROUND",',
                f"        bounds: [{bounds}],",
                f"        assetPath: ASSET_ROOT + {jsx_string(row.image_file)},",
                "        fitOption: FitOptions.FILL_PROPORTIONALLY,",
                f"        title: {jsx_string(row.title)},",
                f"        section: {jsx_string(row.section)},",
                f"        caption: {jsx_string(row.caption)}",
                "    },",
            ]
        )
    lines.extend(
        [
            "];",
            "",
            "// Example page-5 placement object resolved from the manifest:",
            "// {",
            "//     page: 5,",
            '//     type: "image",',
            '//     layer: "BACKGROUND",',
            "//     bounds: [1.0, 0.9, 10.0, 7.6],",
            '//     assetPath: "final-11-image-merge/nina-zeynep-guler-fjJiVSX-BxM-unsplash_2.jpg",',
            "//     fitOption: FitOptions.FILL_PROPORTIONALLY",
            "// }",
        ]
    )
    return lines


def build_indesign_asset_sheet(output: Path = ASSET_SHEET_JSX) -> Path:
    ensure_output_dirs()
    rows = load_manifest_rows(MANIFEST_CSV)
    lines = indesign_asset_sheet_lines(rows)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output


def build_layout_refine_apply_script(output: Path = APPLY_LAYOUT_REFINE_JSX) -> Path:
    ensure_output_dirs()
    rows = load_manifest_rows(MANIFEST_CSV)
    lines = [
        "#target indesign",
        "app.scriptPreferences.userInteractionLevel = UserInteractionLevels.NEVER_INTERACT;",
        "",
        "var SOURCE_INDD = " + jsx_string(LAYOUT_REFINE_INDD) + ";",
        "var OUTPUT_INDD = " + jsx_string(LAYOUT_REFINE_OUTPUT_INDD) + ";",
        "var REPORT_FILE = " + jsx_string(INDESIGN_AUTOBUILD_REPORT) + ";",
        "",
    ]
    lines.extend(indesign_asset_sheet_lines(rows, absolute_asset_root=True))
    lines.extend(
        [
            "",
            "function main() {",
            "    logStatus('start');",
            "    var sourceFile = File(SOURCE_INDD);",
            "    var outputFile = File(OUTPUT_INDD);",
            "    if (!sourceFile.exists) throw Error('Missing source INDD: ' + SOURCE_INDD);",
            "    logStatus('source exists');",
            "    if (!outputFile.exists) throw Error('Missing prebuilt output copy: ' + OUTPUT_INDD);",
            "    logStatus('output copy exists');",
            "    var doc = app.open(outputFile);",
            "    logStatus('output copy opened: pages=' + doc.pages.length + ', masters=' + doc.masterSpreads.length);",
            "    var oldH = doc.viewPreferences.horizontalMeasurementUnits;",
            "    var oldV = doc.viewPreferences.verticalMeasurementUnits;",
            "    doc.viewPreferences.horizontalMeasurementUnits = MeasurementUnits.INCHES;",
            "    doc.viewPreferences.verticalMeasurementUnits = MeasurementUnits.INCHES;",
            "    injectEditorialPalette(doc);",
            "    logStatus('palette applied');",
            "    computeAndApplyAlgorithmicGrid(doc);",
            "    logStatus('grid applied');",
            "    var imageLayer = getOrCreateLayer(doc, 'BACKGROUND');",
            "    var textLayer = getOrCreateLayer(doc, 'TEXT');",
            "    clearLayerItems(imageLayer);",
            "    clearLayerItems(textLayer);",
            "    logStatus('layers cleared');",
            "    for (var i = 0; i < assetSheet.length; i++) {",
            "        placeAsset(doc, assetSheet[i], imageLayer, textLayer);",
            "        logStatus('placed asset page ' + assetSheet[i].page + ': ' + assetSheet[i].title);",
            "    }",
            "    injectTOCAndBibliography(doc, textLayer);",
            "    logStatus('toc and bibliography applied');",
            "    doc.viewPreferences.horizontalMeasurementUnits = oldH;",
            "    doc.viewPreferences.verticalMeasurementUnits = oldV;",
            "    doc.save(outputFile);",
            "    var statusMessage = 'Final 11-image layout refine build applied: ' + outputFile.fsName;",
            "    $.writeln(statusMessage);",
            "    logStatus(statusMessage);",
            "}",
            "",
            "function logStatus(message) {",
            "    var f = File(REPORT_FILE);",
            "    f.open('a');",
            "    f.writeln(new Date().toString() + ' | ' + message);",
            "    f.close();",
            "}",
            "",
            "function getOrCreateLayer(doc, name) {",
            "    var layer = doc.layers.itemByName(name);",
            "    if (!layer.isValid) layer = doc.layers.add({name: name});",
            "    layer.locked = false;",
            "    layer.visible = true;",
            "    return layer;",
            "}",
            "",
            "function injectEditorialPalette(doc) {",
            "    var customColors = [",
            '        { name: "Raw Concrete", space: ColorSpace.CMYK, value: [19, 15, 16, 0] },',
            '        { name: "Stark Void", space: ColorSpace.CMYK, value: [67, 60, 59, 44] },',
            '        { name: "Unbleached Page", space: ColorSpace.CMYK, value: [1, 1, 4, 0] },',
            '        { name: "Incandescent Beam", space: ColorSpace.CMYK, value: [14, 57, 100, 3] }',
            "    ];",
            "    for (var i = 0; i < customColors.length; i++) {",
            "        var colorData = customColors[i];",
            "        var targetColor = doc.colors.itemByName(colorData.name);",
            "        if (!targetColor.isValid) {",
            "            targetColor = doc.colors.add({name: colorData.name});",
            "        }",
            "        targetColor.properties = {",
            "            model: ColorModel.PROCESS,",
            "            space: colorData.space,",
            "            colorValue: colorData.value",
            "        };",
            "    }",
            "}",
            "",
            "function computeAndApplyAlgorithmicGrid(doc) {",
            "    logStatus('grid start');",
            "    var PAGE_WIDTH = 8.5;",
            "    var COL_COUNT = 12;",
            "    var GUTTER_INCHES = 0.1667;",
            "    var marginInside = 0.75;",
            "    var marginTop = marginInside * 1.1333;",
            "    var marginOutside = marginInside * 1.2000;",
            "    var marginBottom = marginInside * 1.3333;",
            "    var totalAvailableWidth = PAGE_WIDTH - (marginInside + marginOutside);",
            "    var totalGutterWidth = (COL_COUNT - 1) * GUTTER_INCHES;",
            "    var calculatedColumnWidth = (totalAvailableWidth - totalGutterWidth) / COL_COUNT;",
            "    var masterSpread = doc.masterSpreads.item(0);",
            "    var totalMasterPages = masterSpread.pages.length;",
            "    logStatus('grid master pages=' + totalMasterPages);",
            "    for (var i = 0; i < totalMasterPages; i++) {",
            "        var mPage = masterSpread.pages.item(i);",
            "        var isLeftPage = (i % 2 === 0);",
            "        logStatus('grid applying master page index=' + i);",
            "        with (mPage.marginPreferences) {",
            "            top = marginTop;",
            "            bottom = marginBottom;",
            "            left = isLeftPage ? marginOutside : marginInside;",
            "            right = isLeftPage ? marginInside : marginOutside;",
            "            columnCount = COL_COUNT;",
            "            columnGutter = GUTTER_INCHES;",
            "        }",
            "    }",
            "    logStatus('grid margins applied');",
            "    with (doc.gridPreferences) {",
            "        baselineStart = marginTop;",
            '        baselineDivision = "7.5pt";',
            "        baselineGridRelativeOption = BaselineGridRelativeOption.TOP_OF_PAGE;",
            "    }",
            "    logStatus('grid baseline applied');",
            "    $.writeln('Algorithmic grid applied. Column width: ' + calculatedColumnWidth.toFixed(4) + ' in.');",
            "}",
            "",
            "function clearLayerItems(layer) {",
            "    for (var i = layer.pageItems.length - 1; i >= 0; i--) {",
            "        try { layer.pageItems.item(i).remove(); } catch (e) {}",
            "    }",
            "}",
            "",
            "function inchBounds(values) {",
            "    return [values[0] + 'in', values[1] + 'in', values[2] + 'in', values[3] + 'in'];",
            "}",
            "",
            "function placeAsset(doc, asset, imageLayer, textLayer) {",
            "    while (doc.pages.length < asset.page) doc.pages.add();",
            "    var page = doc.pages.item(asset.page - 1);",
            "    var imgFile = File(asset.assetPath);",
            "    if (!imgFile.exists) throw Error('Missing asset: ' + asset.assetPath);",
            "    var frame = page.rectangles.add({itemLayer: imageLayer, geometricBounds: inchBounds(asset.bounds), strokeWeight: 0});",
            "    frame.textWrapPreferences.textWrapMode = TextWrapModes.NONE;",
            "    frame.place(imgFile);",
            "    frame.fit(FitOptions.FILL_PROPORTIONALLY);",
            "    frame.fit(FitOptions.CENTER_CONTENT);",
            "    var captionTop = Math.min(asset.bounds[2] + 0.15, 10.25);",
            "    var caption = page.textFrames.add({",
            "        itemLayer: textLayer,",
            "        geometricBounds: inchBounds([captionTop, 0.9, Math.min(captionTop + 0.65, 10.75), 7.6])",
            "    });",
            "    caption.contents = asset.title + ' / ' + asset.section + '\\r' + asset.caption;",
            "    caption.textFramePreferences.ignoreWrap = true;",
            "    caption.texts.item(0).pointSize = 8.5;",
            "    caption.texts.item(0).leading = 11;",
            "}",
            "",
            "function injectTOCAndBibliography(doc, textLayer) {",
            "    while (doc.pages.length < 8) doc.pages.add();",
            "    var tocPage = doc.pages.item(1);",
            "    var tocFrame = tocPage.textFrames.add({",
            "        itemLayer: textLayer,",
            "        geometricBounds: inchBounds([1.5, 0.9, 5.0, 4.5])",
            "    });",
            "    tocFrame.contents = 'CONTENTS\\r\\r' +",
            "        '03  Dappled Shade ........................ P. 3\\r' +",
            "        '04  Neon Distortion ..................... P. 4\\r' +",
            "        '05  Fading Bloom ........................ P. 5\\r' +",
            "        '06  Aster Peep .......................... P. 6\\r' +",
            "        '07  The Philodendron Window ............. P. 7\\r' +",
            "        '08  The Jeweled Veil / Register ......... P. 8\\r' +",
            "        '09  Floral Veil ......................... P. 9\\r' +",
            "        '10  Poppy Field Portrait ................ P. 10\\r' +",
            "        '11  The Patchwork of Hope ............... P. 11\\r' +",
            "        '12  Emerging from Darkness .............. P. 12\\r' +",
            "        '13  Shrouded Glance ..................... P. 13';",
            "    tocFrame.textFramePreferences.ignoreWrap = true;",
            "    tocFrame.texts.item(0).pointSize = 9.5;",
            "    tocFrame.texts.item(0).leading = 12;",
            "    tocFrame.paragraphs.item(0).pointSize = 14;",
            "",
            "    var metricFrame = tocPage.textFrames.add({",
            "        itemLayer: textLayer,",
            "        geometricBounds: inchBounds([5.35, 0.9, 10.0, 7.6])",
            "    });",
            "    metricFrame.contents = " + jsx_string(HARMONIC_MARGIN_JSX_TEXT.replace("\\r", "\r")) + " + '\\r\\r' + " + jsx_string(METRIC_BLOCK_JSX_TEXT.replace("\\r", "\r")) + ";",
            "    metricFrame.textFramePreferences.ignoreWrap = true;",
            "    metricFrame.texts.item(0).pointSize = 7.4;",
            "    metricFrame.texts.item(0).leading = 9.2;",
            "    metricFrame.paragraphs.item(0).pointSize = 9.5;",
            "",
            "    var bibPage = doc.pages.item(7);",
            "    var bibFrame = bibPage.textFrames.add({",
            "        itemLayer: textLayer,",
            "        geometricBounds: inchBounds([6.0, 0.9, 10.0, 7.6])",
            "    });",
            "    bibFrame.contents = 'PRODUCTION REGISTER & BIBLIOGRAPHY\\r\\r' +",
            "        'Visual Asset Register: IMG_01 through IMG_11 compiled locally.\\r' +",
            "        'Vector Status: no verified vector files found in the final merge package.\\r\\r' +",
            "        'READING LIST TO VERIFY\\r' +",
            "        '- Bachelard, G. (1994). The Poetics of Space. Beacon Press.\\r' +",
            "        '- Tanizaki, J. (1977). In Praise of Shadows. Leete\\'s Island Books.\\r\\r' +",
            "        'Note: source URLs, licenses, and course bibliography requirements still need final human verification.';",
            "    bibFrame.textFramePreferences.ignoreWrap = true;",
            "    bibFrame.texts.item(0).pointSize = 8.5;",
            "    bibFrame.texts.item(0).leading = 11;",
            "    bibFrame.paragraphs.item(0).pointSize = 10;",
            "}",
            "",
            "main();",
        ]
    )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output


def build_final_document(output: Path = FINAL_PDF) -> Path:
    ensure_output_dirs()
    rows = load_manifest_rows(MANIFEST_CSV)
    missing = [row.image_path for row in rows if not row.image_path.exists()]
    if missing:
        missing_text = ", ".join(str(path) for path in missing)
        raise FileNotFoundError(f"Missing manifest images: {missing_text}")

    render_target = output.with_name(output.stem + ".building.pdf")
    if render_target.exists():
        render_target.unlink()

    c = canvas.Canvas(str(render_target), pagesize=letter, pageCompression=1)
    draw_cover(c, rows[0])
    draw_toc(c, rows)
    for index, row in enumerate(rows, start=1):
        draw_section_page(c, row, page_num=index + 2, section_index=index)
    draw_back_matter(c, rows)
    c.save()
    render_target.replace(output)
    build_indesign_asset_sheet(ASSET_SHEET_JSX)
    build_layout_refine_apply_script(APPLY_LAYOUT_REFINE_JSX)
    build_asset_register(ASSET_REGISTER_MD)
    write_report(rows, output)
    return output


def main() -> None:
    output = build_final_document(FINAL_PDF)
    print(f"Final refined PDF: {output}")
    print(f"Build report: {FINAL_REPORT}")
    print(f"Asset register: {ASSET_REGISTER_MD}")
    print(f"InDesign asset sheet: {ASSET_SHEET_JSX}")
    print(f"Layout refine apply script: {APPLY_LAYOUT_REFINE_JSX}")


if __name__ == "__main__":
    main()
