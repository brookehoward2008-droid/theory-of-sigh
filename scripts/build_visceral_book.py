from __future__ import annotations

import csv
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from textwrap import wrap

from PIL import Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
try:
    from pypdf import PdfReader, PdfWriter
    _PYPDF_OK = True
except BaseException:
    _PYPDF_OK = False

from scripts.shared.filename_utils import infer_creator, infer_rights
from scripts.shared.paths import ROOT
from scripts.shared.pdf_helpers import draw_text_block as _draw_text_block

_WINDOWS_ASSETS = Path(
    r"C:\Users\toddl\OneDrive\Desktop\SCHOOL\Graph252 booklab\visceral-theory of sight assets"
)
SOURCE_ASSETS = _WINDOWS_ASSETS if _WINDOWS_ASSETS.exists() else ROOT / "images" / "labeled"
COVER_IMAGE = ROOT / "images" / "cover.jpg"
ROUTE = ROOT / "visceral-production-route"
ASSET_OUT = ROUTE / "assets"
PDF_OUT = ROUTE / "output" / "pdf"
INDESIGN_OUT = ROUTE / "output" / "indesign"
LEDGER_OUT = ROUTE / "ledgers"
NOTES_OUT = ROUTE / "notes"
MANIFEST_OUT = ROUTE / "manifest"
TEMPLATE_OUT = ROUTE / "templates"
REPORTS_OUT = ROUTE / "reports"

# US Letter landscape trim. Matches the InDesign preflight-safe route and the
# committed 50pp proof: facing pages, multi-image spreads, full-bleed section
# title pages.
TRIM_W, TRIM_H = 279.4 * mm, 215.9 * mm  # 11 x 8.5 in
BLEED = 3.175 * mm
PAGE_W, PAGE_H = TRIM_W + (2 * BLEED), TRIM_H + (2 * BLEED)
MARGIN = 16 * mm
GUTTER = 5 * mm
COLUMNS = 12
# Safe content rectangle in page (bleed-inclusive) coordinates.
CONTENT_L = BLEED + MARGIN
CONTENT_R = PAGE_W - BLEED - MARGIN
CONTENT_B = BLEED + MARGIN
CONTENT_T = PAGE_H - BLEED - MARGIN
LIVE_W = CONTENT_R - CONTENT_L
LIVE_H = CONTENT_T - CONTENT_B
COLUMN_W = (LIVE_W - (GUTTER * (COLUMNS - 1))) / COLUMNS
# Legacy aliases (kept so any stray references stay valid).
OUTER_MARGIN = MARGIN
INNER_MARGIN = MARGIN
TOP_MARGIN = MARGIN
BOTTOM_MARGIN = MARGIN
INK = colors.HexColor("#11100E")
CREAM = colors.HexColor("#F3EBDD")
GOLD = colors.HexColor("#A58242")
SLATE = colors.HexColor("#526B7A")
MIST = colors.HexColor("#D8D0C0")
SOFT_BLACK = colors.HexColor("#1C1B19")

ARTICLE_BODIES = {
    "Agency": (
        "The body becomes the first instrument of authorship before it becomes a subject for "
        "interpretation. A hand, a shoulder, a mouth, a turned face: the figure enters as pressure, "
        "not as explanation. It claims the page by being present, and that presence unsettles the "
        "viewer who has not yet been handed a rule for reading it.\n\n"
        "This is the oldest grammar of looking. In LeRoy McDermott's study of Upper Paleolithic "
        "female figurines, the strange proportions of the earliest carved bodies read not as another "
        "person's gaze but as self-representation, the body seen from within by the one who inhabits "
        "it.[1] Sight begins as ownership before it becomes display.\n\n"
        "A figure can be partial and still be active. A cropped body still claims space; a single eye "
        "still returns the look. So the opening pages stay close, image-led, and a little "
        "uncomfortable, letting presence arrive before permission. Looking here is not passive "
        "reception. The eye learns by pressure, repetition, and contrast, and a body seen across a "
        "sequence becomes a pattern the viewer is slowly trained to recognize. Before culture explains "
        "the figure, the figure has already insisted on being seen."
    ),
    "Constraint": (
        "Culture turns visibility into a protocol. Bodily force is no longer allowed to stand alone; "
        "it is arranged by posture, costume, rank, ritual, maternity, and inherited rules of display. "
        "A face still looks outward, but now it looks through an architecture of expectation.\n\n"
        "Elizabeth Mulley's study of Laura Muntz gives this constraint an intimate register: womanhood "
        "represented through maternity, care, loss, and symbolic burden, the body made legible by the "
        "roles it is asked to carry.[2] Mary Morrissy's account of Una Watters adds the everyday, where "
        "the woman is set inside ordinary weather, labor, and street life rather than idealized apart "
        "from it.[3]\n\n"
        "Constraint does not erase agency; it redirects it. The body still carries force, but that "
        "force is shaped by who is permitted to look and who is expected to be seen. The viewer is "
        "disciplined too. Each repeated crop, pose, and symbol teaches a visual habit, until seeing is "
        "no longer simple contact but compliance, resistance, and learned interpretation happening at "
        "once. The room has rules, and the eye has already agreed to most of them before it knows "
        "that it is choosing to obey."
    ),
    "Mediation": (
        "The veil is an editing system, not a disappearance. Where the body and the rule meet a "
        "surface that can interrupt both, lace, shadow, fabric, blur, flowers, hair, and darkness "
        "become interfaces. They do not simply hide the figure; they decide how slowly it is allowed "
        "to arrive.\n\n"
        "A blocked face increases attention, because the viewer has to complete the missing "
        "information. Denial becomes structure. This is the logic the art of obstruction has always "
        "understood: Symbolism treats the visible world as a carrier for inward states, and Surrealism "
        "turns ordinary surfaces into dream pressure and psychological interruption.[4][5] The covered "
        "eye and the displaced face push the viewer toward interpretation rather than recognition.\n\n"
        "So this section opens its grid and lets the images feel secretive, with more negative space "
        "and more surface. The body wants to appear; the rule wants to organize appearance; the veil "
        "controls the tempo of access. The point is not mystery for its own sake but cognitive "
        "pressure. A hidden gaze makes the eye work, and meaning arrives only through that effort. What "
        "is withheld is not absence; it is the part of the image still being decided."
    ),
    "Synthesis": (
        "Sight becomes visceral when these forces remain active together. The final movement refuses "
        "to resolve the body, the rule, and the veil into a clean hierarchy. Agency begins the "
        "argument, constraint disciplines it, and mediation keeps it unresolved, and the image grows "
        "powerful precisely because no single force wins.\n\n"
        "This is the thesis the whole issue has been building toward: psychological pressure does not "
        "come from clear depiction. It comes from calculated revelation, the image negotiating what "
        "can be seen, how quickly, and what stays withheld even after attention has been spent. The "
        "body is present but not fully available. Culture is legible but never neutral. The veil "
        "interrupts, yet it also teaches the eye how to continue.\n\n"
        "So the closing pages keep the layout asymmetrical. Large images take authority; text presses "
        "beside them, slightly displaced. A symmetrical page would imply that sight had settled, and "
        "this argument needs sight to stay unstable, because instability is where looking turns into "
        "learning. The anatomy of looking is never finished. It only changes the surface it has to "
        "cross next, and asks the eye to begin the work again."
    ),
}

# First *content* page of each section (the page after its full-bleed title page).
SECTION_PAGE_START = {
    "Agency": 9,
    "Constraint": 18,
    "Mediation": 28,
    "Synthesis": 40,
}


@dataclass
class Asset:
    id: str
    source_path: Path
    local_path: Path
    filename: str
    width: int
    height: int
    group: str
    rights: str
    creator: str
    title: str
    reason: str
    caption: str = ""
    short_caption: str = ""


def ensure_dirs() -> None:
    for path in (ASSET_OUT, PDF_OUT, INDESIGN_OUT, LEDGER_OUT, NOTES_OUT, MANIFEST_OUT, TEMPLATE_OUT, REPORTS_OUT, ROOT / "scripts"):
        path.mkdir(parents=True, exist_ok=True)


def clean_generated_dirs() -> None:
    for path in (ASSET_OUT, PDF_OUT, INDESIGN_OUT, LEDGER_OUT, NOTES_OUT, MANIFEST_OUT, TEMPLATE_OUT, REPORTS_OUT):
        if path == ASSET_OUT:
            path.mkdir(parents=True, exist_ok=True)
            for child in sorted(path.iterdir(), reverse=True):
                if child.name == "final-11-image-merge":
                    continue
                try:
                    if child.is_file() or child.is_symlink():
                        child.unlink()
                    elif child.is_dir():
                        shutil.rmtree(child)
                except PermissionError:
                    pass
            continue
        if path.exists() and ROUTE in path.parents:
            try:
                shutil.rmtree(path)
            except PermissionError:
                # Windows/OneDrive can keep a generated folder handle open after
                # PDF preview. Leave the folder shell in place and clear what is
                # not locked so the build can still refresh its artifacts.
                for child in sorted(path.rglob("*"), reverse=True):
                    try:
                        if child.is_file() or child.is_symlink():
                            child.unlink()
                        elif child.is_dir():
                            child.rmdir()
                    except PermissionError:
                        pass
        path.mkdir(parents=True, exist_ok=True)


def apply_print_boxes(pdf_path: Path) -> None:
    if not _PYPDF_OK:
        return
    reader = PdfReader(str(pdf_path))
    writer = PdfWriter()
    for page in reader.pages:
        page.mediabox.lower_left = (0, 0)
        page.mediabox.upper_right = (PAGE_W, PAGE_H)
        page.bleedbox.lower_left = (0, 0)
        page.bleedbox.upper_right = (PAGE_W, PAGE_H)
        page.trimbox.lower_left = (BLEED, BLEED)
        page.trimbox.upper_right = (BLEED + TRIM_W, BLEED + TRIM_H)
        writer.add_page(page)
    with pdf_path.open("wb") as f:
        writer.write(f)


def infer_group(index: int, name: str) -> str:
    lowered = name.lower()
    if any(term in lowered for term in ["lace", "veil", "blindfold", "flowers", "obscured"]):
        return "Group 3: Mediation"
    if any(term in lowered for term in ["stock", "portrait", "shadow", "hidden", "mirror", "sunglasses"]):
        return "Group 2: Social Constraint"
    if index % 3 == 0:
        return "Group 1: Raw Agency"
    if index % 3 == 1:
        return "Group 2: Social Constraint"
    return "Group 3: Mediation"


def infer_reason(group: str, name: str) -> str:
    if "Agency" in group:
        return "Body, eye, hand, or facial presence reads as physical self-possession before social coding."
    if "Constraint" in group:
        return "Pose, cropping, gaze control, object barrier, or social presentation turns visibility into protocol."
    return "Fabric, lace, blur, flower, veil, or partial face makes sight mediated rather than simply hidden."


CAPTION_MANIFEST = ROOT / "data" / "visceral-caption-manifest.csv"
_CAPTION_FALLBACK = {
    "Agency": "Presence arrives before permission; the body speaks first.",
    "Constraint": "The pose turns looking into a rule already agreed to.",
    "Mediation": "A surface intervenes, and sight has to earn the face.",
}


def _norm(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.lower())


def _asset_core(filename: str) -> str:
    """Strip the repo 'aNN-theme-' prefix so the original name can match the manifest."""
    stem = filename.rsplit(".", 1)[0]
    stem = re.sub(r"^a\d+-(mediation|social-constraint|raw-agency)-", "", stem)
    return _norm(stem)


def load_caption_index() -> list[tuple[str, str, str]]:
    index: list[tuple[str, str, str]] = []
    if not CAPTION_MANIFEST.exists():
        return index
    with CAPTION_MANIFEST.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            name = (row.get("filename") or "").strip()
            if name:
                index.append(
                    (
                        _norm(name.rsplit(".", 1)[0]),
                        (row.get("short_caption") or "").strip(),
                        (row.get("caption") or "").strip(),
                    )
                )
    return index


def caption_for(asset: Asset, index: list[tuple[str, str, str]]) -> tuple[str, str]:
    """Return (short_caption, caption) for an asset, matched by original filename."""
    core = _asset_core(asset.filename)
    best: tuple[str, str] | None = None
    best_len = 0
    for key, short_cap, full_cap in index:
        if key and (key in core or core in key) and len(key) > best_len:
            best = (short_cap, full_cap)
            best_len = len(key)
    if best:
        return best
    group = "Agency" if "Agency" in asset.group else "Constraint" if "Constraint" in asset.group else "Mediation"
    fallback = _CAPTION_FALLBACK[group]
    return (fallback, fallback)


def make_cover_asset(fallback: Asset) -> Asset:
    """Use images/cover.jpg as the front-cover image when present, else the fallback plate."""
    if not COVER_IMAGE.exists():
        return fallback
    with Image.open(COVER_IMAGE) as img:
        width, height = img.size
    return Asset(
        id="COVER",
        source_path=COVER_IMAGE,
        local_path=COVER_IMAGE,
        filename=COVER_IMAGE.name,
        width=width,
        height=height,
        group="Mediation",
        rights="",
        creator="",
        title="Cover",
        reason="",
    )


def _canonical_cores() -> set[str]:
    """Original-name cores of the canonical plates (the repo's 64-image labeled set)."""
    repo_dir = ROOT / "images" / "labeled"
    cores: set[str] = set()
    if repo_dir.exists():
        for p in repo_dir.iterdir():
            if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}:
                cores.add(_asset_core(p.name))
    return cores


def _filter_to_canonical(files: list[Path]) -> list[Path]:
    """Keep only source files matching a canonical plate, so a full-res source folder
    that still holds the deleted originals (67) is locked back to the published 64."""
    cores = _canonical_cores()
    if not cores:
        return files
    kept: list[Path] = []
    for p in files:
        core = _asset_core(p.name)
        if any(c and (c in core or core in c) for c in cores):
            kept.append(p)
    return kept


def scan_assets() -> list[Asset]:
    files = sorted(
        [p for p in SOURCE_ASSETS.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}],
        key=lambda p: p.name.lower(),
    )
    files = _filter_to_canonical(files)
    assets: list[Asset] = []
    caption_index = load_caption_index()
    for i, path in enumerate(files, start=1):
        out_name = f"asset-{i:02d}{path.suffix.lower()}"
        local = ASSET_OUT / out_name
        shutil.copy2(path, local)
        with Image.open(local) as img:
            width, height = img.size
        group = infer_group(i, path.name)
        title = path.stem
        asset = Asset(
            id=f"A{i:02d}",
            source_path=path,
            local_path=local,
            filename=path.name,
            width=width,
            height=height,
            group=group,
            rights=infer_rights(path.name),
            creator=infer_creator(path.name),
            title=title,
            reason=infer_reason(group, path.name),
        )
        asset.short_caption, asset.caption = caption_for(asset, caption_index)
        assets.append(asset)
    return assets


def draw_bg(c: canvas.Canvas, dark: bool = True) -> None:
    # Whole magazine runs black-background / white-text.
    c.setFillColor(SOFT_BLACK)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)


def draw_text_block(
    c: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    width_chars: int = 50,
    leading: float = 14,
    size: float = 10,
    font: str = "Times-Roman",
    color=CREAM,
    max_lines: int | None = None,
) -> float:
    return _draw_text_block(
        c, text, x, y, width_chars, leading, size, font, color, max_lines,
    )


def draw_label(c: canvas.Canvas, text: str, x: float, y: float, color=GOLD) -> None:
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(color)
    c.drawString(x, y, text.upper())


def draw_page_number(c: canvas.Canvas, page: int, dark: bool = True) -> None:
    c.setFont("Helvetica", 7)
    c.setFillColor(CREAM if dark else INK)
    c.drawRightString(PAGE_W - 36, 24, f"{page:02d}")


def image_box(c: canvas.Canvas, asset: Asset, x: float, y: float, w: float, h: float) -> None:
    reader = ImageReader(str(asset.local_path))
    iw, ih = asset.width, asset.height
    scale = max(w / iw, h / ih)
    sw, sh = iw * scale, ih * scale
    sx = x + (w - sw) / 2
    sy = y + (h - sh) / 2
    c.saveState()
    clip = c.beginPath()
    clip.rect(x, y, w, h)
    c.clipPath(clip, stroke=0, fill=0)
    c.drawImage(reader, sx, sy, sw, sh, preserveAspectRatio=False, mask="auto")
    c.restoreState()


def image_caption(c: canvas.Canvas, asset: Asset, x: float, y: float, w: float, dark: bool = False) -> None:
    c.setFillColor(CREAM if dark else INK)
    c.setFont("Helvetica-Oblique", 6.5)
    caption = f"{asset.id} / {(asset.short_caption or asset.caption)}"
    c.drawString(x, y, caption[:104])
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.4)
    c.line(x, y - 5, x + w, y - 5)


def translucent_panel(c: canvas.Canvas, x: float, y: float, w: float, h: float, dark: bool = False, alpha: float = 0.84) -> None:
    c.saveState()
    if dark:
        c.setFillColor(colors.Color(0.05, 0.045, 0.04, alpha=alpha))
    else:
        c.setFillColor(colors.Color(0.953, 0.922, 0.866, alpha=alpha))
    c.rect(x, y, w, h, fill=1, stroke=0)
    c.restoreState()


def overlay_caption(c: canvas.Canvas, asset: Asset, x: float, y: float, w: float, dark: bool = True) -> None:
    translucent_panel(c, x - 6, y - 12, w + 12, 30, dark=dark, alpha=0.72)
    c.setFont("Helvetica-Bold", 6.5)
    c.setFillColor(CREAM if dark else INK)
    c.drawString(x, y + 2, f"{asset.id} / {asset.group.split(': ')[-1].upper()}")
    c.setFont("Helvetica-Oblique", 6.2)
    c.drawString(x, y - 7, (asset.short_caption or asset.caption)[:80])


def draw_pull_quote(c: canvas.Canvas, lines: list[str], y: float, dark: bool = False) -> None:
    c.saveState()
    c.setFillColor(colors.Color(0.65, 0.51, 0.26, alpha=0.88))
    c.rect(0, y - 18, PAGE_W, 118, fill=1, stroke=0)
    c.setFillColor(CREAM if not dark else INK)
    c.setFont("Helvetica-Bold", 28)
    for i, line in enumerate(lines):
        c.drawString(58 + (i % 2) * 30, y + 62 - (i * 31), line)
    c.restoreState()


def intro_copy() -> str:
    return (
        "Sight is never only an act of seeing. It is a negotiation between the body "
        "that appears, the culture that disciplines appearance, and the surface that "
        "decides what the eye is allowed to touch. This issue moves through agency, "
        "constraint, and mediation as one continuous pressure system: the anatomy of "
        "looking, traced from the body outward to the veil."
    )


def section_copy(section: str) -> str:
    return ARTICLE_BODIES[section]


def _article_chunks(section: str, words_per_page: int = 86) -> list[str]:
    """Split a section body into sequential, sentence-aligned chunks (one per page)."""
    words = ARTICLE_BODIES[section].replace("\n", " ").split()
    chunks: list[str] = []
    i = 0
    while i < len(words):
        end = min(i + words_per_page, len(words))
        while end < len(words) and words[end - 1][-1] not in ".!?":
            end += 1
        chunks.append(" ".join(words[i:end]))
        i = end
    return chunks


def article_excerpt(section: str, page: int, target_chars: int = 520) -> str:
    """Sequential article text for a content page; empty once the article is spent."""
    start_page = SECTION_PAGE_START[section]
    offset = max(0, page - start_page)
    chunks = _article_chunks(section)
    return chunks[offset] if offset < len(chunks) else ""


def scrim(c: canvas.Canvas, alpha: float = 0.42, dark: bool = True) -> None:
    """Full-page wash over an image so overlaid type stays legible."""
    c.saveState()
    base = 0.04 if dark else 0.95
    c.setFillColor(colors.Color(base, base, base, alpha=alpha))
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.restoreState()


SECTION_TITLES = {
    "Agency": ("I", "Agency", "The Body / presence before permission"),
    "Constraint": ("II", "Constraint", "The Rule / visibility as protocol"),
    "Mediation": ("III", "Mediation", "The Veil / the tempo of access"),
    "Synthesis": ("IV", "Synthesis", "Sight that refuses to settle"),
}

# One-sentence meaning printed under each section title.
SECTION_BLURB = {
    "Agency": (
        "Agency is the body as its own first statement: a hand, an eye, a turned "
        "face that claims attention as pressure, before any rule arrives to explain it."
    ),
    "Constraint": (
        "Constraint is culture turning visibility into protocol: pose, costume, rank, "
        "and ritual teach a body how it may appear, and teach the viewer how to approve it."
    ),
    "Mediation": (
        "Mediation is the veil as an editing system: lace, shadow, fabric, and blur do "
        "not simply hide the body, they decide how slowly it is allowed to be seen."
    ),
    "Synthesis": (
        "Synthesis is sight that refuses to settle: body, rule, and veil stay active at "
        "once, so looking stays unfinished and the image keeps its pressure."
    ),
}


def draw_section_title(c: canvas.Canvas, page: int, section: str, asset: Asset) -> None:
    """Full-bleed image spread carrying the section title and its meaning."""
    numeral, title, sub = SECTION_TITLES.get(section, ("", section, ""))
    blurb = SECTION_BLURB.get(section, "")
    image_box(c, asset, 0, 0, PAGE_W, PAGE_H)
    scrim(c, alpha=0.56, dark=True)
    x = CONTENT_L
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(x, CONTENT_B + 230, "ARTICLE " + numeral)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.4)
    c.line(x, CONTENT_B + 214, x + 150, CONTENT_B + 214)
    c.setFillColor(CREAM)
    c.setFont("Helvetica-Bold", 54)
    c.drawString(x, CONTENT_B + 150, title)
    c.setFont("Times-Italic", 15)
    c.drawString(x, CONTENT_B + 120, sub)
    # Subtext under the title: what this section means.
    draw_text_block(c, blurb, x, CONTENT_B + 92, width_chars=74, leading=15, size=10.5, color=CREAM)
    draw_page_number(c, page, dark=True)


def draw_cover(c: canvas.Canvas, asset: Asset, page_num: int | None = None) -> None:
    image_box(c, asset, 0, 0, PAGE_W, PAGE_H)
    scrim(c, alpha=0.34, dark=True)
    x = CONTENT_L
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x, CONTENT_B + 150, "THE ANATOMY OF LOOKING")
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.line(x, CONTENT_B + 134, x + 260, CONTENT_B + 134)
    c.setFillColor(CREAM)
    c.setFont("Helvetica-Bold", 52)
    c.drawString(x, CONTENT_B + 78, "THE VISCERAL")
    c.drawString(x, CONTENT_B + 30, "THEORY OF SIGHT")
    c.setFont("Times-Roman", 13)
    c.drawString(x, CONTENT_B + 8, "the body, the gaze, and the veil")
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(x, CONTENT_B - 22, "BROOKE CHAUNTEL")
    if page_num:
        draw_page_number(c, page_num, dark=True)


def draw_title_spread(c: canvas.Canvas, asset: Asset, side: str) -> None:
    """Two-page title spread: full-bleed image (left page) facing the title (right page)."""
    if side == "left":
        image_box(c, asset, 0, 0, PAGE_W, PAGE_H)
        scrim(c, alpha=0.42, dark=True)
        draw_label(c, "the anatomy of looking", CONTENT_L, CONTENT_B + 40, color=GOLD)
        draw_page_number(c, 2, dark=True)
    else:
        draw_bg(c, dark=True)
        c.setFillColor(GOLD)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(CONTENT_L, CONTENT_T - 30, "TITLE")
        c.setFillColor(CREAM)
        c.setFont("Helvetica-Bold", 56)
        c.drawString(CONTENT_L, CONTENT_T - 132, "THE VISCERAL")
        c.drawString(CONTENT_L, CONTENT_T - 190, "THEORY OF SIGHT")
        c.setFont("Times-Italic", 15)
        c.drawString(CONTENT_L, CONTENT_T - 222, "A visual psychology issue on gaze, image memory, and the veil.")
        c.setFillColor(GOLD)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(CONTENT_L, CONTENT_T - 252, "Brooke Chauntel")
        c.setFillColor(MIST)
        c.setFont("Helvetica", 10)
        c.drawString(CONTENT_L, CONTENT_T - 270, "Everett Community College · 2026")
        text = (
            "This issue uses local image files supplied for production. Adobe Stock and Unsplash assets "
            "require license and source verification before public release; locally generated or unknown "
            "files require creator and usage confirmation. Citations are real and listed in Works "
            "Consulted; exact editions, page ranges, and licenses are confirmed before final print."
        )
        draw_text_block(c, text, CONTENT_L, CONTENT_B + 116, width_chars=70, leading=13, size=9.5, color=MIST)
        draw_page_number(c, 3, dark=True)


def draw_title_page(c: canvas.Canvas) -> None:
    draw_bg(c)
    draw_label(c, "title page", CONTENT_L, CONTENT_T - 6)
    c.setFillColor(CREAM)
    c.setFont("Helvetica-Bold", 46)
    c.drawString(CONTENT_L, CONTENT_T - 120, "The Visceral")
    c.drawString(CONTENT_L, CONTENT_T - 168, "Theory of Sight")
    c.setFont("Times-Roman", 14)
    c.drawString(CONTENT_L, CONTENT_T - 200, "A 50-page editorial art book on controlled revelation.")
    c.setFillColor(CREAM)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(CONTENT_L, CONTENT_T - 232, "Brooke Chauntel")
    c.setFillColor(MIST)
    c.setFont("Helvetica", 10)
    c.drawString(CONTENT_L, CONTENT_T - 252, "Everett Community College · 2026")
    c.setFillColor(CREAM)
    c.setFont("Helvetica", 8.5)
    c.drawString(CONTENT_L, CONTENT_B + 30, "Compiled and designed as an alternate local production route.")
    c.drawString(CONTENT_L, CONTENT_B + 16, "All citations and rights marked for verification before final export.")
    draw_page_number(c, 2)


def draw_legal(c: canvas.Canvas) -> None:
    draw_bg(c)
    draw_label(c, "legal / credits", 72, PAGE_H - 90)
    text = (
        "This proof package uses local image files supplied for production. It does not certify "
        "publication rights. Adobe Stock files require license verification. Unsplash-named files "
        "require source URL verification. Locally generated or unknown files require creator and "
        "usage confirmation.\n\n"
        "Scholarly source placeholders: McDermott on Paleolithic agency and the body; Havelock/Reeder "
        "on Greek art, cultural constraint, posture, and social rule; veiling iconography, Vera Icona, "
        "lace, and mediation theory. Exact article titles, page numbers, and quotations remain verify "
        "before final export unless source PDFs are added to the workspace."
    )
    draw_text_block(c, text, CONTENT_L, CONTENT_T - 44, width_chars=108, leading=14, size=10)
    draw_page_number(c, 3)


def draw_toc(c: canvas.Canvas) -> None:
    draw_bg(c, dark=True)
    draw_label(c, "contents", CONTENT_L, CONTENT_T - 6, color=GOLD)
    c.setFillColor(CREAM)
    c.setFont("Helvetica-Bold", 34)
    c.drawString(CONTENT_L, CONTENT_T - 64, "Agency / Constraint / Mediation")
    entries = [
        ("Front Matter", "01"),
        ("Introduction: The Visceral Theory of Sight", "05"),
        ("I. Agency", "08"),
        ("II. Constraint", "17"),
        ("III. Mediation", "27"),
        ("IV. Synthesis", "39"),
        ("Back Matter", "46"),
    ]
    y = CONTENT_T - 122
    for title, page in entries:
        c.setFont("Times-Roman", 14)
        c.setFillColor(CREAM)
        c.drawString(CONTENT_L, y, title)
        title_w = c.stringWidth(title, "Times-Roman", 14)
        c.setStrokeColor(MIST)
        c.setLineWidth(0.6)
        c.setDash([1, 3])
        c.line(CONTENT_L + title_w + 12, y + 3, CONTENT_R - 34, y + 3)
        c.setDash([])
        c.setFont("Helvetica-Bold", 13)
        c.setFillColor(GOLD)
        c.drawRightString(CONTENT_R, y, page)
        y -= 36
    draw_page_number(c, 4)


def draw_intro(c: canvas.Canvas, page: int, assets: list[Asset]) -> None:
    dark = True
    draw_bg(c, dark=dark)
    if page == 5:
        draw_label(c, "introduction", CONTENT_L, CONTENT_T - 6)
        c.setFillColor(CREAM)
        c.setFont("Helvetica-Bold", 34)
        c.drawString(CONTENT_L, CONTENT_T - 72, "The Visceral Theory")
        c.drawString(CONTENT_L, CONTENT_T - 110, "of Sight")
        draw_text_block(c, intro_copy(), CONTENT_L, CONTENT_T - 156, width_chars=44, leading=14, size=10.5)
        # Staggered image cluster fills the right half of the landscape spread.
        image_box(c, assets[0], 432, CONTENT_T - 250, 196, 250)
        image_box(c, assets[5 % len(assets)], 638, CONTENT_T - 250, 118, 250)
        image_box(c, assets[10 % len(assets)], 432, CONTENT_B, 324, 168)
        overlay_caption(c, assets[0], 444, CONTENT_T - 236, 170, dark=True)
    elif page == 6:
        image_box(c, assets[2 % len(assets)], 0, 0, PAGE_W, PAGE_H)
        scrim(c, alpha=0.5, dark=True)
        c.setFillColor(CREAM)
        c.setFont("Helvetica-Bold", 30)
        c.drawString(CONTENT_L, CONTENT_T - 44, "The image does not give")
        c.drawString(CONTENT_L, CONTENT_T - 80, "itself all at once.")
        draw_text_block(c, "Controlled revelation is the method. Tension is the evidence.", CONTENT_L, CONTENT_B + 44, width_chars=78, leading=14, size=11, color=CREAM)
    else:
        draw_label(c, "the three pressures", CONTENT_L, CONTENT_T - 6)
        cols = [CONTENT_L, CONTENT_L + 238, CONTENT_L + 476]
        labels = [("AGENCY", "body as force"), ("CONSTRAINT", "body as protocol"), ("MEDIATION", "veil as edit")]
        top = CONTENT_T - 48
        for x, (head, sub) in zip(cols, labels):
            c.setFillColor(GOLD)
            c.rect(x, top, 92, 3, fill=1, stroke=0)
            c.setFillColor(CREAM)
            c.setFont("Helvetica-Bold", 18)
            c.drawString(x, top - 30, head)
            c.setFont("Times-Roman", 11)
            c.drawString(x, top - 48, sub)
        image_box(c, assets[7 % len(assets)], CONTENT_L, CONTENT_B + 92, LIVE_W, 150)
        draw_text_block(c, intro_copy(), CONTENT_L, CONTENT_B + 70, width_chars=112, leading=13, size=9.5)
    draw_page_number(c, page, dark=dark)


def draw_plate_page(c: canvas.Canvas, page: int, section: str, a0: Asset, a1: Asset, a2: Asset, accent, offset: int) -> None:
    """Image-forward plate page used once a section's article text is spent."""
    draw_bg(c, dark=True)
    if offset % 2 == 1:
        gap = 16
        iw = (LIVE_W - 2 * gap) / 3
        ih = LIVE_H * 0.66
        ytop = CONTENT_T - ih
        for k, a in enumerate((a0, a1, a2)):
            image_box(c, a, CONTENT_L + k * (iw + gap), ytop, iw, ih)
        draw_label(c, section.upper() + " / sequence", CONTENT_L, ytop - 24, color=accent)
        overlay_caption(c, a0, CONTENT_L + 14, ytop + 12, 180, dark=True)
    else:
        image_box(c, a0, 0, 0, PAGE_W, PAGE_H)
        scrim(c, alpha=0.32, dark=True)
        draw_label(c, section.upper() + " / sequence", CONTENT_L, CONTENT_T - 6, color=GOLD)
        overlay_caption(c, a0, CONTENT_L + 14, CONTENT_B + 18, 240, dark=True)
    draw_page_number(c, page, dark=True)


def draw_article_page(c: canvas.Canvas, page: int, section: str, section_assets: list[Asset], offset: int) -> None:
    """Landscape editorial page. Variants 1 and 3 carry multiple images per spread."""
    variant = offset % 5
    dark = True
    draw_bg(c, dark=dark)
    fg = CREAM if dark else INK
    accent = SLATE if section == "Mediation" else GOLD
    body_text = article_excerpt(section, page)
    n = len(section_assets)
    a0 = section_assets[offset % n]
    a1 = section_assets[(offset + 1) % n]
    a2 = section_assets[(offset + 2) % n]
    if not body_text:
        draw_plate_page(c, page, section, a0, a1, a2, accent, offset)
        return
    if variant == 0:
        # Dominant image left, text column right.
        iw = LIVE_W * 0.56
        image_box(c, a0, CONTENT_L, CONTENT_B, iw, LIVE_H)
        tx = CONTENT_L + iw + 26
        c.setFillColor(accent)
        c.rect(tx, CONTENT_T - 30, 60, 4, fill=1, stroke=0)
        c.setFillColor(fg)
        c.setFont("Helvetica-Bold", 26)
        c.drawString(tx, CONTENT_T - 64, section.upper())
        draw_text_block(c, body_text, tx, CONTENT_T - 96, width_chars=31, leading=14.5, size=10.4, color=fg)
        overlay_caption(c, a0, CONTENT_L + 14, CONTENT_B + 18, 220, dark=True)
    elif variant == 1:
        # Two stacked images left, text right.
        iw = LIVE_W * 0.46
        h = (LIVE_H - 18) / 2
        image_box(c, a0, CONTENT_L, CONTENT_B + h + 18, iw, h)
        image_box(c, a1, CONTENT_L, CONTENT_B, iw, h)
        tx = CONTENT_L + iw + 30
        c.setFillColor(accent)
        c.rect(tx, CONTENT_T - 30, 60, 4, fill=1, stroke=0)
        c.setFillColor(fg)
        c.setFont("Helvetica-Bold", 26)
        c.drawString(tx, CONTENT_T - 64, section.upper())
        draw_text_block(c, body_text, tx, CONTENT_T - 96, width_chars=37, leading=14.5, size=10.4, color=fg)
        overlay_caption(c, a1, CONTENT_L + 14, CONTENT_B + 16, 200, dark=True)
    elif variant == 2:
        # Full-bleed single image, scrim, pull statement, text panel.
        image_box(c, a0, 0, 0, PAGE_W, PAGE_H)
        scrim(c, alpha=0.52, dark=True)
        draw_label(c, f"article / {section}", CONTENT_L, CONTENT_T - 10, color=accent)
        c.setFillColor(CREAM)
        c.setFont("Helvetica-Bold", 30)
        c.drawString(CONTENT_L, CONTENT_T - 56, "Only one eye remains;")
        c.drawString(CONTENT_L, CONTENT_T - 90, "the image gets louder.")
        translucent_panel(c, CONTENT_L - 6, CONTENT_B - 6, LIVE_W * 0.48 + 12, 152, dark=True, alpha=0.58)
        draw_text_block(c, body_text, CONTENT_L + 8, CONTENT_B + 128, width_chars=46, leading=12.5, size=8.6, color=CREAM, max_lines=10)
    elif variant == 3:
        # Triptych: three images across, text band beneath.
        gap = 16
        iw = (LIVE_W - 2 * gap) / 3
        ih = LIVE_H * 0.6
        ytop = CONTENT_T - ih
        for k, a in enumerate((a0, a1, a2)):
            image_box(c, a, CONTENT_L + k * (iw + gap), ytop, iw, ih)
        c.setFillColor(accent)
        c.rect(CONTENT_L, ytop - 22, 60, 4, fill=1, stroke=0)
        c.setFillColor(fg)
        c.setFont("Helvetica-Bold", 18)
        c.drawString(CONTENT_L, ytop - 50, f"{section.upper()} / SEQUENCE")
        draw_text_block(c, body_text, CONTENT_L, ytop - 72, width_chars=112, leading=12.5, size=9, color=fg, max_lines=5)
        overlay_caption(c, a1, CONTENT_L + iw + gap + 12, ytop + 12, 180, dark=True)
    else:
        # Text left, dominant image right.
        iw = LIVE_W * 0.56
        ix = CONTENT_R - iw
        image_box(c, a0, ix, CONTENT_B, iw, LIVE_H)
        c.setFillColor(accent)
        c.rect(CONTENT_L, CONTENT_T - 30, 60, 4, fill=1, stroke=0)
        c.setFillColor(fg)
        c.setFont("Helvetica-Bold", 26)
        c.drawString(CONTENT_L, CONTENT_T - 64, section.upper())
        draw_text_block(c, body_text, CONTENT_L, CONTENT_T - 96, width_chars=31, leading=14.5, size=10.4, color=fg)
        overlay_caption(c, a0, ix + 14, CONTENT_B + 18, 200, dark=True)
    draw_page_number(c, page, dark=dark)


def draw_synthesis(c: canvas.Canvas, page: int, section_assets: list[Asset], offset: int) -> None:
    variant = offset % 2
    dark = True
    draw_bg(c, dark=dark)
    fg = CREAM if dark else INK
    body_text = article_excerpt("Synthesis", page)
    n = len(section_assets)
    a0 = section_assets[offset % n]
    a1 = section_assets[(offset + 1) % n]
    if not body_text:
        draw_plate_page(c, page, "Synthesis", a0, a1, section_assets[(offset + 2) % n], GOLD, offset)
        return
    if variant == 0:
        # Full-bleed image, text column on the right.
        image_box(c, a0, 0, 0, PAGE_W, PAGE_H)
        scrim(c, alpha=0.46, dark=True)
        tx = CONTENT_L + LIVE_W * 0.54
        c.setFillColor(GOLD)
        c.rect(tx, CONTENT_T - 30, 60, 4, fill=1, stroke=0)
        c.setFillColor(CREAM)
        c.setFont("Helvetica-Bold", 26)
        c.drawString(tx, CONTENT_T - 64, "Unresolved Sight")
        draw_text_block(c, body_text, tx, CONTENT_T - 92, width_chars=33, leading=13, size=9.2, color=CREAM)
        overlay_caption(c, a0, CONTENT_L + 14, CONTENT_B + 18, 200, dark=True)
    else:
        # Image left, second image upper-right, framed closing text.
        iw = LIVE_W * 0.5
        image_box(c, a0, CONTENT_L, CONTENT_B, iw - 12, LIVE_H)
        image_box(c, a1, CONTENT_L + iw + 12, CONTENT_T - LIVE_H * 0.5, LIVE_W - iw - 12, LIVE_H * 0.5)
        tx = CONTENT_L + iw + 12
        c.setStrokeColor(GOLD)
        c.setLineWidth(1.6)
        c.line(tx, CONTENT_B + LIVE_H * 0.44, CONTENT_R, CONTENT_B + LIVE_H * 0.44)
        c.setFillColor(CREAM)
        c.setFont("Helvetica-Bold", 20)
        c.drawString(tx, CONTENT_B + LIVE_H * 0.37, "Looking never arrives clean.")
        draw_text_block(c, body_text, tx, CONTENT_B + LIVE_H * 0.31, width_chars=44, leading=13, size=9.2, color=CREAM, max_lines=10)
    draw_page_number(c, page, dark=dark)


def draw_back_matter(c: canvas.Canvas, page: int, assets: list[Asset]) -> None:
    draw_bg(c, dark=True)
    if page in (46, 47):
        first = page == 46
        draw_label(c, "image source register" if first else "image source register / continued", CONTENT_L, CONTENT_T - 6, color=CREAM)
        subset = assets[:32] if first else assets[32:]
        col_x = [CONTENT_L, CONTENT_L + LIVE_W / 2 + 12]
        per_col = (len(subset) + 1) // 2
        for ci, cx in enumerate(col_x):
            chunk = subset[ci * per_col:(ci + 1) * per_col]
            y = CONTENT_T - 40
            for asset in chunk:
                c.setFillColor(GOLD)
                c.setFont("Helvetica-Bold", 8)
                c.drawString(cx, y, asset.id)
                c.setFillColor(CREAM)
                c.setFont("Times-Roman", 8)
                c.drawString(cx + 30, y, asset.title[:40])
                c.setFillColor(MIST)
                c.setFont("Helvetica", 6.5)
                c.drawString(cx + 30, y - 9, f"{asset.creator[:38]} - rights verify")
                y -= 26
    elif page == 48:
        draw_label(c, "works consulted", CONTENT_L, CONTENT_T - 6, color=CREAM)
        text = (
            "[1] LeRoy McDermott. \"Self-Representation in Upper Paleolithic Female Figurines.\" "
            "Current Anthropology 37, no. 2 (1996): 227-275.\n\n"
            "[2] Elizabeth Mulley. \"Madonna/Mother/Death and Child: Laura Muntz and the Representation "
            "of Maternity.\" RACAR 25, no. 1/2 (1998): 84-93.\n\n"
            "[3] Mary Morrissy. \"Una Watters: Everywoman Caught in the Rain.\" New Hibernia Review 25, "
            "no. 3 (2021): 39-53.\n\n"
            "[4] The Metropolitan Museum of Art. \"Surrealism.\" Heilbrunn Timeline of Art History.\n\n"
            "[5] The Metropolitan Museum of Art. \"Symbolism.\" Heilbrunn Timeline of Art History.\n\n"
            "Editions, page ranges, and image licenses to be confirmed before final print."
        )
        draw_text_block(c, text, CONTENT_L, CONTENT_T - 44, width_chars=118, leading=14, size=10, color=CREAM)
    elif page == 49:
        draw_label(c, "colophon", CONTENT_L, CONTENT_T - 6, color=CREAM)
        text = (
            "The Visceral Theory of Sight is a visual-psychology issue on gaze, image memory, and the veil. "
            "Written, sequenced, and designed by Brooke Chauntel for Everett Community College, 2026. "
            "Photographs are credited in the Image Source Register; scholarly works are listed under Works Consulted. "
            "Set in Helvetica and Times, printed white on black."
        )
        draw_text_block(c, text, CONTENT_L, CONTENT_T - 44, width_chars=118, leading=14, size=10, color=CREAM)
    else:
        c.setFont("Helvetica-Bold", 40)
        c.setFillColor(CREAM)
        c.drawString(CONTENT_L, CONTENT_T - 120, "Sight remains")
        c.drawString(CONTENT_L, CONTENT_T - 168, "unfinished.")
        draw_text_block(c, "Every act of looking leaves a remainder: memory, attention, and the need to interpret what the eye cannot settle.", CONTENT_L, CONTENT_B + 96, width_chars=92, leading=14, size=10, color=CREAM)
    draw_page_number(c, page, dark=True)


def write_ledger(assets: list[Asset]) -> None:
    csv_path = LEDGER_OUT / "source-image-ledger.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "asset_id",
                "local_production_path",
                "original_path",
                "creator_or_institution",
                "title",
                "date",
                "rights_license_status",
                "visual_group",
                "intended_pages_or_section",
                "reason_it_matches_tone",
                "dimensions_px",
            ]
        )
        for i, asset in enumerate(assets):
            section = "Pages 27-38 / Article III, The Veil"
            if "Agency" in asset.group:
                section = "Pages 8-16 / Article I, The Body"
            elif "Constraint" in asset.group:
                section = "Pages 17-26 / Article II, The Constraint"
            writer.writerow(
                [
                    asset.id,
                    str(asset.local_path),
                    str(asset.source_path),
                    asset.creator,
                    asset.title,
                    "unknown",
                    asset.rights,
                    asset.group,
                    section,
                    asset.reason,
                    f"{asset.width}x{asset.height}",
                ]
            )


def write_notes(assets: list[Asset]) -> None:
    notes = f"""# The Visceral Theory of Sight - Critical Process Notes

## Production Geometry

The rebuilt proof uses A4 portrait trim with 3 mm bleed on all sides. PDF MediaBox
includes the bleed; PDF TrimBox is A4. The handoff files in `templates/` record
the same 12-column grid for InDesign and Affinity setup.

## Source Synthesis

This proof treats the argument as one visual arc rather than three isolated summaries.
McDermott is held as the placeholder route for the body as agency and origin.
Havelock/Reeder is held as the placeholder route for posture, Greek art, social rule,
and the body as cultural protocol. Veiling iconography, Vera Icona, lace, and mediation
theory are held as the placeholder route for partial sight and refusal.

No direct quotations are used because source texts were not present in this workspace.
All scholarly citations remain marked: verify before final export.

The article copy is embedded as four long-form bodies: Agency, Constraint, Mediation,
and Synthesis. Article pages draw progressive excerpts from those bodies so the
50-page PDF and the InDesign full-layout JSX carry real article text rather than
repeating short section placeholders.

## Grid Theory

The layout uses a 12-column modular asymmetrical grid. Outer margin is 7.5 percent
of A4 trim width, inner margin is 10 percent, top and bottom margins are 7 percent
of trim height, and gutters are 5 mm. It does not make every spread symmetrical
because the project is about controlled revelation, not clean disclosure. The grid
tightens in the Constraint section and loosens in the Veil section. That shift lets
the page system behave like the argument: body, rule, surface.

## Image Grouping

Local image assets scanned: {len(assets)}.

- Group 1: Raw Agency - body, hand, eye, facial pressure, physical presence.
- Group 2: Social Constraint - pose, object, mirror, rank, display, discipline.
- Group 3: Mediation - lace, veil, flower, fabric, blur, shadow, partial access.

## Design Support

Agency is image-led and close to the body. Constraint becomes more formal and column-aware.
Mediation uses more atmosphere, negative space, and surface interruption. The reader should
feel the unresolved tension between looking and not being allowed to fully see.

## Execution Strategy: Making The Grid Resist Itself

The final layout applies three controlled disruptions. Overlap appears through captions and
text panels crossing image edges. Broken flow appears when large image blocks interrupt the
reading path and force the text to resume from a displaced column. Layering appears through
photographs as background fields, translucent text panels as the base reading layer, and
accent labels or pull quotes as the top pressure layer.

These moves are intentional rather than decorative. They make the page behave like the
argument: visibility is never neutral, never complete, and never given without a surface
intervening.

## Rights-Sensitive Work Remaining

- Verify every Adobe Stock license against the user's account or school license.
- Verify every Unsplash filename against its source URL and current license terms.
- Verify local/generated image provenance before final print or public upload.
- Replace all scholarly placeholders with exact bibliographic records if required.

## InDesign Preflight Note

If InDesign reports overset text, run `templates/indesign-fix-overset-text.jsx`
against the open `.indd`. It attempts frame fitting, margin-safe expansion, and
controlled type reduction, then writes a remaining-issues report.
"""
    (NOTES_OUT / "critical-process-notes.md").write_text(notes, encoding="utf-8")


def write_grid_handoff() -> None:
    grid = {
        "document": {
            "trim": {"name": "A4 portrait", "width_pt": TRIM_W, "height_pt": TRIM_H, "width_mm": 210, "height_mm": 297},
            "bleed": {"all_sides_mm": 3, "all_sides_pt": BLEED},
            "media": {"width_pt": PAGE_W, "height_pt": PAGE_H},
            "orientation": "portrait",
            "pages": 50,
        },
        "grid": {
            "columns": COLUMNS,
            "gutter_mm": 5,
            "gutter_pt": GUTTER,
            "outer_margin_percent_of_width": 7.5,
            "inner_margin_percent_of_width": 10,
            "top_margin_percent_of_height": 7,
            "bottom_margin_percent_of_height": 7,
            "outer_margin_pt": OUTER_MARGIN,
            "inner_margin_pt": INNER_MARGIN,
            "top_margin_pt": TOP_MARGIN,
            "bottom_margin_pt": BOTTOM_MARGIN,
            "live_width_pt": LIVE_W,
            "column_width_pt": COLUMN_W,
        },
        "modules": {
            "standard_text_block": "3-4 columns wide, variable height",
            "caption": "1-2 columns wide, short fixed height",
            "pull_quote": "full-bleed horizontal box with accent frame",
            "gap": "large negative space as conceptual pause",
        },
        "execution_rules": [
            "Use master pages for page numbers, section headers, margins, and grid.",
            "Let selected images bleed under text blocks.",
            "Use broken reading flow: paragraph, image interruption, resumed text.",
            "Layer background image, base text, then labels and quotes.",
            "Keep source and rights verification visible until final export.",
        ],
    }
    (TEMPLATE_OUT / "indesign-affinity-grid-blueprint.json").write_text(json.dumps(grid, indent=2), encoding="utf-8")

    with (TEMPLATE_OUT / "indesign-affinity-grid-blueprint.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["field", "value", "unit_or_note"])
        writer.writerow(["trim_width", "210", "mm"])
        writer.writerow(["trim_height", "297", "mm"])
        writer.writerow(["bleed", "3", "mm all sides"])
        writer.writerow(["columns", COLUMNS, "count"])
        writer.writerow(["gutter", "5", "mm"])
        writer.writerow(["outer_margin", f"{OUTER_MARGIN / mm:.3f}", "mm, 7.5 percent trim width"])
        writer.writerow(["inner_margin", f"{INNER_MARGIN / mm:.3f}", "mm, 10 percent trim width"])
        writer.writerow(["top_margin", f"{TOP_MARGIN / mm:.3f}", "mm, 7 percent trim height"])
        writer.writerow(["bottom_margin", f"{BOTTOM_MARGIN / mm:.3f}", "mm, 7 percent trim height"])
        writer.writerow(["column_width", f"{COLUMN_W / mm:.3f}", "mm"])
        writer.writerow(["standard_text_block", "3-4", "columns"])
        writer.writerow(["caption_module", "1-2", "columns"])
        writer.writerow(["pull_quote_module", "full bleed", "horizontal accent box"])

    md = f"""# InDesign / Affinity Technical Grid Blueprint

## Document

- Trim: A4 portrait, 210 mm x 297 mm.
- Bleed: 3 mm on all sides.
- Media/artboard with bleed: {(PAGE_W / mm):.3f} mm x {(PAGE_H / mm):.3f} mm.
- Pages: 50.
- Master page: page numbers, section headers, margins, and 12-column grid.

## Grid

- Columns: {COLUMNS}.
- Gutter: 5 mm.
- Outer margin: {(OUTER_MARGIN / mm):.3f} mm, 7.5 percent of trim width.
- Inner margin: {(INNER_MARGIN / mm):.3f} mm, 10 percent of trim width.
- Top margin: {(TOP_MARGIN / mm):.3f} mm, 7 percent of trim height.
- Bottom margin: {(BOTTOM_MARGIN / mm):.3f} mm, 7 percent of trim height.
- Column width after margins and gutters: {(COLUMN_W / mm):.3f} mm.

## Modules

- Standard text block: 3-4 columns wide, variable height.
- Caption module: 1-2 columns wide, short fixed height.
- Pull quote module: full-bleed horizontal box, huge broken line text, accent frame.
- Gap module: negative space as conceptual pause.

## Execution Rules

- Overlap captions and text blocks slightly onto image corners.
- Let selected images bleed under text boxes.
- Break reading flow with image interruptions.
- Layer background image, base text, labels, and quotes.
- Keep all scholarly and rights verification flags visible until final export.
"""
    (TEMPLATE_OUT / "indesign-affinity-grid-blueprint.md").write_text(md, encoding="utf-8")

    handoff = """# IDML / InDesign / Affinity Handoff

## What This Package Provides

- A4 PDF proof with explicit A4 TrimBox and 3 mm BleedBox.
- Facing-pages reader-spread PDF for layout review.
- Full 50-page InDesign JSX layout builder with linked image placement.
- Native InDesign target: `output/indesign/the-visceral-theory-of-sight-50pp.indd`.
- IDML import target for Affinity: `output/indesign/the-visceral-theory-of-sight-50pp.idml`.
- InDesign JSX autobuild script that creates a 50-page A4 facing-pages document.
- InDesign JSX overset-repair script for active `.indd` preflight cleanup.
- JSON, CSV, and Markdown grid blueprints with exact measurements.

## IDML / Affinity Boundary

IDML is the supported bridge from InDesign to Affinity Publisher. The generated
InDesign script saves the native `.indd` and exports a real `.idml` through InDesign.
Affinity Publisher can open/import that IDML. Affinity's native `.afpub` format is
not generated by InDesign; save the imported IDML from Affinity Publisher to create
`output/affinity/the-visceral-theory-of-sight-50pp.afpub`.

1. Open InDesign.
2. Run `templates/indesign-build-full-layout.jsx` to create the complete 50-page linked layout.
3. Use the saved native `.indd` in `output/indesign/`.
4. Run Preflight. If needed, run `templates/indesign-fix-overset-text.jsx`.
5. Open/import the generated `.idml` in Affinity Publisher and save as `.afpub`.

Use `templates/indesign-create-a4-grid.jsx` only when you want a blank grid document.

## Overset Text Preflight Repair

The pasted preflight report shows overset text across many pages. Open the `.indd`,
then run `templates/indesign-fix-overset-text.jsx`. The script makes three passes:

1. Fit frames to content where possible.
2. Expand overset frames within the page's margin-safe area.
3. Reduce type size and leading gradually, stopping at a readable minimum.

It writes a report beside the InDesign file and lists any frames that still need
manual threading or copy edits.

## Affinity Route

Affinity Publisher can use the generated IDML plus the same A4 measurements from
`indesign-affinity-grid-blueprint.md`. Use the PDF proof for visual review and the
IDML for the closest editable Affinity handoff.

## Precision Values

- Trim: A4 portrait, 210 mm x 297 mm.
- Bleed: 3 mm all sides.
- Columns: 12.
- Gutter: 5 mm.
- Outer margin: 15.750 mm.
- Inner margin: 21.000 mm.
- Top margin: 20.790 mm.
- Bottom margin: 20.790 mm.
- Column width: 9.853 mm.
"""
    (TEMPLATE_OUT / "idml-indesign-affinity-handoff.md").write_text(handoff, encoding="utf-8")

    jsx = f"""// The Visceral Theory of Sight - InDesign A4 grid autobuild
// Run from InDesign: File > Scripts > Other Script...
var doc = app.documents.add();
doc.documentPreferences.pageWidth = "210mm";
doc.documentPreferences.pageHeight = "297mm";
doc.documentPreferences.facingPages = true;
doc.documentPreferences.pagesPerDocument = 50;
doc.documentPreferences.documentBleedTopOffset = "3mm";
doc.documentPreferences.documentBleedBottomOffset = "3mm";
doc.documentPreferences.documentBleedInsideOrLeftOffset = "3mm";
doc.documentPreferences.documentBleedOutsideOrRightOffset = "3mm";
doc.marginPreferences.top = "{(TOP_MARGIN / mm):.3f}mm";
doc.marginPreferences.bottom = "{(BOTTOM_MARGIN / mm):.3f}mm";
doc.marginPreferences.left = "{(INNER_MARGIN / mm):.3f}mm";
doc.marginPreferences.right = "{(OUTER_MARGIN / mm):.3f}mm";
doc.marginPreferences.columnCount = 12;
doc.marginPreferences.columnGutter = "5mm";
var master = doc.masterSpreads.item(0);
master.name = "A-Master - Visceral Grid";
for (var i = 0; i < doc.pages.length; i++) {{
  doc.pages.item(i).appliedMaster = master;
}}
alert("Visceral A4 facing-pages document created: 50 pages, 3mm bleed, 12 columns.");
"""
    (TEMPLATE_OUT / "indesign-create-a4-grid.jsx").write_text(jsx, encoding="utf-8")

    fix_jsx = """// The Visceral Theory of Sight - overset text repair pass
// Usage: open the .indd in InDesign, then run File > Scripts > Other Script...
// This script changes the active document. Save a copy first if needed.

if (app.documents.length === 0) {
  alert("Open the InDesign document first.");
} else {
  var doc = app.activeDocument;
  var report = [];
  var repaired = 0;
  var remaining = 0;

  function pageName(tf) {
    try {
      if (tf.parentPage) return tf.parentPage.name;
    } catch (e) {}
    return "pasteboard/master/unknown";
  }

  function pageSafeBounds(tf) {
    var p = tf.parentPage;
    if (!p) return null;
    var b = p.bounds; // [top,left,bottom,right]
    var mp = p.marginPreferences;
    return [
      b[0] + mp.top,
      b[1] + mp.left,
      b[2] - mp.bottom,
      b[3] - mp.right
    ];
  }

  function clampFrameToSafeArea(tf) {
    var safe = pageSafeBounds(tf);
    if (!safe) return false;
    var gb = tf.geometricBounds;
    var height = gb[2] - gb[0];
    var width = gb[3] - gb[1];
    var newTop = Math.max(safe[0], gb[0]);
    var newLeft = Math.max(safe[1], gb[1]);
    var newBottom = Math.min(safe[2], Math.max(newTop + height, safe[2]));
    var newRight = Math.min(safe[3], Math.max(newLeft + width, safe[3]));
    tf.geometricBounds = [newTop, newLeft, newBottom, newRight];
    return true;
  }

  function reduceStoryType(story) {
    var minSize = 6.5;
    var attempts = 0;
    while (story.overflows && attempts < 18) {
      try {
        for (var i = 0; i < story.texts.length; i++) {
          var t = story.texts[i];
          if (t.pointSize > minSize) {
            t.pointSize = Math.max(minSize, t.pointSize - 0.25);
            t.leading = t.pointSize * 1.22;
          }
        }
      } catch (e) {}
      attempts++;
    }
  }

  // Pass 1: fit frames to content where possible.
  for (var i = 0; i < doc.textFrames.length; i++) {
    var tf = doc.textFrames[i];
    if (!tf.isValid || !tf.overflows) continue;
    try { tf.fit(FitOptions.FRAME_TO_CONTENT); } catch (e) {}
  }

  // Pass 2: expand within safe margins and reduce type only if still overset.
  for (var j = 0; j < doc.textFrames.length; j++) {
    var frame = doc.textFrames[j];
    if (!frame.isValid || !frame.overflows) continue;
    var before = frame.overflows;
    clampFrameToSafeArea(frame);
    try { frame.fit(FitOptions.FRAME_TO_CONTENT); } catch (e2) {}
    if (frame.overflows && frame.parentStory) {
      reduceStoryType(frame.parentStory);
    }
    if (before && !frame.overflows) {
      repaired++;
      report.push("FIXED page " + pageName(frame));
    }
  }

  // Final report.
  for (var k = 0; k < doc.textFrames.length; k++) {
    var finalFrame = doc.textFrames[k];
    if (!finalFrame.isValid || !finalFrame.overflows) continue;
    remaining++;
    report.push("STILL OVERSET page " + pageName(finalFrame) + " bounds " + finalFrame.geometricBounds.join(", "));
  }

  var output = "Overset repair report for " + doc.name + "\\n";
  output += "Repaired frames: " + repaired + "\\n";
  output += "Remaining overset frames: " + remaining + "\\n\\n";
  output += report.join("\\n");

  try {
    var basePath = doc.filePath ? doc.filePath.fsName : Folder.desktop.fsName;
    var outFile = File(basePath + "/visceral-overset-repair-report.txt");
    outFile.encoding = "UTF-8";
    outFile.open("w");
    outFile.write(output);
    outFile.close();
    alert(output + "\\n\\nReport written to: " + outFile.fsName);
  } catch (writeErr) {
    alert(output);
  }
}
"""
    (TEMPLATE_OUT / "indesign-fix-overset-text.jsx").write_text(fix_jsx, encoding="utf-8")


def write_full_layout_jsx(assets: list[Asset]) -> None:
    js_assets = [
        {
            "id": asset.id,
            "path": asset.local_path.as_posix(),
            "title": asset.title[:58],
            "group": asset.group,
            "caption": asset.caption,
            "short_caption": asset.short_caption,
        }
        for asset in assets
    ]
    assets_literal = json.dumps(js_assets, indent=2)
    copy_literal = json.dumps(
        {
            "intro": intro_copy(),
            "agency": ARTICLE_BODIES["Agency"],
            "constraint": ARTICLE_BODIES["Constraint"],
            "mediation": ARTICLE_BODIES["Mediation"],
            "synthesis": ARTICLE_BODIES["Synthesis"],
        },
        indent=2,
    )
    section_meta = {
        key: {
            "numeral": SECTION_TITLES[key][0],
            "title": SECTION_TITLES[key][1],
            "sub": SECTION_TITLES[key][2],
            "blurb": SECTION_BLURB[key],
        }
        for key in ("Agency", "Constraint", "Mediation", "Synthesis")
    }
    section_meta_literal = json.dumps(section_meta, indent=2)
    cover_path_literal = json.dumps(COVER_IMAGE.as_posix() if COVER_IMAGE.exists() else "")
    output_indd = INDESIGN_OUT / "the-visceral-theory-of-sight-50pp.indd"
    output_idml = INDESIGN_OUT / "the-visceral-theory-of-sight-50pp.idml"
    output_pdf = PDF_OUT / "the-visceral-theory-of-sight-50pp-indesign-auto.pdf"
    output_report = REPORTS_OUT / "indesign-full-layout-auto-report.json"
    jsx = f"""// The Visceral Theory of Sight - full 50-page InDesign layout builder
// Run from InDesign: File > Scripts > Other Script...
// Builds US Letter landscape facing pages, 3.175mm bleed, full-bleed section title pages with descriptions, multi-image spreads, captions, PDF, and audit report.

var ASSETS = {assets_literal};
var OUTPUT_INDD = {json.dumps(output_indd.as_posix())};
var OUTPUT_IDML = {json.dumps(output_idml.as_posix())};
var OUTPUT_PDF = {json.dumps(output_pdf.as_posix())};
var OUTPUT_REPORT = {json.dumps(output_report.as_posix())};

app.scriptPreferences.userInteractionLevel = UserInteractionLevels.NEVER_INTERACT;

var COPY = {copy_literal};

var SECTION = {section_meta_literal};

var COVER_PATH = {cover_path_literal};

function mm(v) {{ return v + "mm"; }}
function b(t, l, bot, r) {{ return [mm(t), mm(l), mm(bot), mm(r)]; }}
function pageBounds(page, bounds) {{
  var pb = page.bounds;
  var topOffset = Number(pb[0]);
  var leftOffset = Number(pb[1]);
  return [
    mm(topOffset + parseFloat(bounds[0])),
    mm(leftOffset + parseFloat(bounds[1])),
    mm(topOffset + parseFloat(bounds[2])),
    mm(leftOffset + parseFloat(bounds[3]))
  ];
}}
function asset(i) {{ return ASSETS[i % ASSETS.length]; }}
function assetByName(sub) {{
  for (var i = 0; i < ASSETS.length; i++) {{
    if (ASSETS[i].title.toLowerCase().indexOf(sub) >= 0) return ASSETS[i];
  }}
  return null;
}}

function groupAsset(groupName, i) {{
  var matches = [];
  for (var a = 0; a < ASSETS.length; a++) {{
    if (ASSETS[a].group.indexOf(groupName) >= 0) matches.push(ASSETS[a]);
  }}
  if (matches.length === 0) return asset(i);
  return matches[i % matches.length];
}}

function copyChunk(key, n) {{
  var text = COPY[key] || COPY.synthesis;
  var words = text.replace(/\\r|\\n/g, " ").split(/\\s+/);
  var wordsPerPage = 86;
  var chunks = [];
  var i = 0;
  while (i < words.length) {{
    var end = Math.min(i + wordsPerPage, words.length);
    while (end < words.length) {{
      var last = words[end - 1].charAt(words[end - 1].length - 1);
      if (last === "." || last === "!" || last === "?") break;
      end++;
    }}
    chunks.push(words.slice(i, end).join(" "));
    i = end;
  }}
  var startPage = key === "agency" ? 9 : key === "constraint" ? 18 : key === "mediation" ? 28 : 40;
  var offset = Math.max(0, n - startPage);
  return (offset < chunks.length) ? chunks[offset] : "";
}}

function setupDoc() {{
  var doc = app.documents.add();
  doc.documentPreferences.pageWidth = "279.4mm";
  doc.documentPreferences.pageHeight = "215.9mm";
  doc.documentPreferences.facingPages = true;
  doc.documentPreferences.pagesPerDocument = 50;
  doc.documentPreferences.documentBleedTopOffset = "3.175mm";
  doc.documentPreferences.documentBleedBottomOffset = "3.175mm";
  doc.documentPreferences.documentBleedInsideOrLeftOffset = "3.175mm";
  doc.documentPreferences.documentBleedOutsideOrRightOffset = "3.175mm";
  doc.marginPreferences.top = "16mm";
  doc.marginPreferences.bottom = "16mm";
  doc.marginPreferences.left = "16mm";
  doc.marginPreferences.right = "16mm";
  doc.marginPreferences.columnCount = 12;
  doc.marginPreferences.columnGutter = "5mm";
  return doc;
}}

function addSwatch(doc, name, values) {{
  try {{
    var s = doc.colors.itemByName(name);
    s.name;
    return s;
  }} catch (e) {{
    return doc.colors.add({{name: name, model: ColorModel.PROCESS, space: ColorSpace.RGB, colorValue: values}});
  }}
}}

function fitText(tf, minSize) {{
  var attempts = 0;
  while (tf.overflows && attempts < 40) {{
    try {{
      var txt = tf.texts[0];
      txt.pointSize = Math.max(minSize, txt.pointSize - 0.35);
      txt.leading = txt.pointSize * 1.22;
    }} catch (e) {{}}
    attempts++;
  }}
}}

function textFrame(page, bounds, text, size, fontStyle, swatch, opacity) {{
  var tf = page.textFrames.add();
  tf.geometricBounds = pageBounds(page, bounds);
  tf.contents = text;
  try {{
    tf.textFramePreferences.insetSpacing = ["2mm", "2mm", "2mm", "2mm"];
    tf.textFramePreferences.verticalJustification = VerticalJustification.TOP_ALIGN;
    tf.textFramePreferences.autoSizingReferencePoint = AutoSizingReferenceEnum.TOP_LEFT_POINT;
    tf.textFramePreferences.autoSizingType = AutoSizingTypeEnum.OFF;
    tf.textFramePreferences.useMinimumHeightForAutoSizing = true;
    tf.textFramePreferences.minimumHeightForAutoSizing = 8;
    tf.texts[0].appliedFont = app.fonts.item("Helvetica");
    tf.texts[0].fontStyle = fontStyle || "Regular";
    tf.texts[0].pointSize = size;
    tf.texts[0].leading = size * 1.22;
    tf.texts[0].fillColor = swatch;
  }} catch (e) {{}}
  if (opacity < 100) {{
    try {{ tf.transparencySettings.blendingSettings.opacity = opacity; }} catch (e2) {{}}
  }}
  fitText(tf, 5.5);
  return tf;
}}

function imageFrame(page, bounds, item, opacity) {{
  var rect = page.rectangles.add();
  rect.geometricBounds = pageBounds(page, bounds);
  rect.strokeWeight = 0;
  try {{
    rect.place(File(item.path));
    rect.fit(FitOptions.FILL_PROPORTIONALLY);
    rect.fit(FitOptions.CENTER_CONTENT);
  }} catch (e) {{
    rect.fillColor = page.parent.parent.colors.itemByName("Ink");
  }}
  if (opacity < 100) {{
    try {{ rect.transparencySettings.blendingSettings.opacity = opacity; }} catch (e2) {{}}
  }}
  return rect;
}}

function countMissingLinks(doc) {{
  var missing = 0;
  for (var i = 0; i < doc.links.length; i++) {{
    try {{
      if (doc.links[i].status === LinkStatus.LINK_MISSING) missing++;
    }} catch (e) {{}}
  }}
  return missing;
}}

function countOversetFrames(doc) {{
  var overset = 0;
  for (var i = 0; i < doc.textFrames.length; i++) {{
    try {{
      if (doc.textFrames[i].isValid && doc.textFrames[i].overflows) overset++;
    }} catch (e) {{}}
  }}
  return overset;
}}

function exportPdf(doc) {{
  var pdfFile = File(OUTPUT_PDF);
  if (!pdfFile.parent.exists) pdfFile.parent.create();
  var preset = null;
  try {{
    preset = app.pdfExportPresets.itemByName("[High Quality Print]");
    preset.name;
  }} catch (e) {{
    preset = app.pdfExportPresets.item(0);
  }}
  doc.exportFile(ExportFormat.PDF_TYPE, pdfFile, false, preset);
}}

function writeBuildReport(doc) {{
  var reportFile = File(OUTPUT_REPORT);
  if (!reportFile.parent.exists) reportFile.parent.create();
  var report = {{
    document: "The Visceral Theory of Sight",
    generatedAt: new Date().toString(),
    pageCount: doc.pages.length,
    facingPages: doc.documentPreferences.facingPages,
    trim: "US Letter landscape 279.4mm x 215.9mm",
    bleed: "3.175mm all sides",
    columns: 12,
    assetCount: ASSETS.length,
    linkCount: doc.links.length,
    missingLinks: countMissingLinks(doc),
    textFrameCount: doc.textFrames.length,
    oversetTextFrames: countOversetFrames(doc),
    moodyLayoutRules: [
      "dark ink and archival cream base",
      "muted gold and slate accents",
      "large image fields",
      "overlap captions",
      "broken text flow",
      "full-bleed pressure pages",
      "layered translucent panels"
    ],
    outputs: {{
      indd: OUTPUT_INDD,
      idml: OUTPUT_IDML,
      pdf: OUTPUT_PDF
    }}
  }};
  reportFile.encoding = "UTF-8";
  reportFile.open("w");
  reportFile.write(JSON.stringify(report, null, 2));
  reportFile.close();
}}

function colorPanel(page, bounds, swatch, opacity) {{
  var rect = page.rectangles.add();
  rect.geometricBounds = pageBounds(page, bounds);
  rect.strokeWeight = 0;
  rect.fillColor = swatch;
  try {{ rect.transparencySettings.blendingSettings.opacity = opacity; }} catch (e) {{}}
  return rect;
}}

function caption(page, bounds, item, ink, cream) {{
  var theme = item.group.replace("Group 1: ", "").replace("Group 2: ", "").replace("Group 3: ", "");
  var label = item.id + " / " + theme + "\\n" + (item.short_caption || item.caption || "");
  var tf = textFrame(page, bounds, label, 6.4, "Bold", cream, 100);
  try {{ tf.fillColor = cream; tf.transparencySettings.blendingSettings.opacity = 92; }} catch(e) {{}}
  return tf;
}}

function pageNum(page, n, ink) {{
  textFrame(page, b(204, 250, 212, 270), ("0" + n).slice(-2), 6.5, "Regular", cream, 100);
}}

function configurePreflight(doc) {{
  // Color landscape magazine profile: duplicate Digital Publishing but allow
  // CMY plates (color photos) and landscape orientation. Mirrors the
  // Brooke Automation configurePublicationPreflight command.
  var profileName = "Anatomy of Looking - Color Landscape";
  var profile = null;
  try {{ profile = app.preflightProfiles.itemByName(profileName); profile.name; }}
  catch (e) {{
    try {{ profile = app.preflightProfiles.itemByName("kDigPubProfileName").duplicate(); profile.name = profileName; }}
    catch (e2) {{ try {{ profile = app.preflightProfiles.add(); profile.name = profileName; }} catch (e3) {{ return; }} }}
  }}
  try {{ profile.description = "Color landscape magazine profile; CMY plates and landscape orientation intentionally allowed."; }} catch (e4) {{}}
  try {{ profile.preflightProfileRules.itemByName("ADBE_CMYPlates").flag = 1699890274; }} catch (e5) {{}}
  try {{ profile.preflightProfileRules.itemByName("ADBE_PageSizeOrientation").flag = 1699890274; }} catch (e6) {{}}
  try {{
    doc.preflightOptions.preflightWorkingProfile = profile;
    doc.preflightOptions.preflightOff = false;
  }} catch (e7) {{}}
}}

function saveDesktopFiles(doc) {{
  var inddFile = File(OUTPUT_INDD);
  var idmlFile = File(OUTPUT_IDML);
  if (!inddFile.parent.exists) inddFile.parent.create();
  doc.save(inddFile);
  doc.exportFile(ExportFormat.INDESIGN_MARKUP, idmlFile);
  exportPdf(doc);
  writeBuildReport(doc);
}}

function cover(page, doc, ink, cream, gold) {{
  var item = groupAsset("Mediation", 0);
  if (COVER_PATH && File(COVER_PATH).exists) item = {{ path: COVER_PATH, id: "COVER", title: "Cover", group: "Mediation", caption: "", short_caption: "" }};
  imageFrame(page, b(-4, -4, 220, 284), item, 100);
  colorPanel(page, b(120, -4, 220, 284), ink, 46);
  textFrame(page, b(150, 18, 162, 230), "THE ANATOMY OF LOOKING", 10, "Bold", gold, 100);
  textFrame(page, b(164, 18, 198, 252), "THE VISCERAL\\rTHEORY OF SIGHT", 33, "Bold", cream, 100);
  textFrame(page, b(198, 18, 210, 232), "the body, the gaze, and the veil", 11, "Regular", cream, 100);
}}

function sectionTitle(page, key, ink, cream, gold) {{
  var meta = SECTION[key];
  var openerItem = (key === "Mediation") ? (assetByName("allef-vinicius") || groupAsset(key, 1)) : groupAsset(key, 1);
  imageFrame(page, b(-4, -4, 220, 284), openerItem, 100);
  colorPanel(page, b(-4, -4, 220, 284), ink, 56);
  textFrame(page, b(94, 18, 106, 180), "ARTICLE " + meta.numeral, 11, "Bold", gold, 100);
  textFrame(page, b(108, 18, 150, 252), meta.title, 38, "Bold", cream, 100);
  textFrame(page, b(150, 18, 164, 250), meta.sub, 12, "Italic", cream, 100);
  textFrame(page, b(166, 18, 202, 230), meta.blurb, 10, "Regular", cream, 100);
}}

function frontMatter(page, n, doc, ink, cream, gold) {{
  if (n === 2) {{
    imageFrame(page, b(-4, -4, 220, 284), groupAsset("Mediation", 1), 100);
    colorPanel(page, b(-4, -4, 220, 284), ink, 40);
    textFrame(page, b(190, 18, 202, 220), "THE ANATOMY OF LOOKING", 10, "Bold", gold, 100);
  }} else if (n === 3) {{
    textFrame(page, b(18, 18, 30, 120), "TITLE", 11, "Bold", gold, 100);
    textFrame(page, b(34, 18, 96, 250), "THE VISCERAL\\rTHEORY OF SIGHT", 40, "Bold", cream, 100);
    textFrame(page, b(98, 18, 118, 250), "A visual psychology issue on gaze, image memory, and the veil.", 13, "Regular", cream, 100);
    textFrame(page, b(150, 18, 200, 250), "This issue uses local image files supplied for production. Adobe Stock and Unsplash assets require license and source verification before public release. Citations are real and listed in Works Consulted; exact editions, page ranges, and licenses are confirmed before final print.", 9, "Regular", cream, 100);
  }} else {{
    textFrame(page, b(18, 18, 30, 220), "CONTENTS", 11, "Bold", gold, 100);
    textFrame(page, b(34, 18, 82, 250), "Agency / Constraint / Mediation", 34, "Bold", cream, 100);
    var tocTitles = "Front Matter\\rIntroduction: The Visceral Theory of Sight\\rI. Agency\\rII. Constraint\\rIII. Mediation\\rIV. Synthesis\\rBack Matter";
    textFrame(page, b(96, 18, 200, 215), tocTitles, 13, "Regular", cream, 100);
    var pf = textFrame(page, b(96, 215, 200, 255), "01\\r05\\r08\\r17\\r27\\r39\\r46", 13, "Bold", gold, 100);
    try {{ pf.texts[0].justification = Justification.RIGHT_ALIGN; }} catch (e) {{}}
  }}
}}

function introPage(page, n, doc, ink, cream, gold) {{
  if (n === 5) {{
    textFrame(page, b(20, 18, 52, 200), "The Visceral Theory of Sight", 26, "Bold", cream, 100);
    textFrame(page, b(58, 18, 180, 150), COPY.intro, 10.5, "Regular", cream, 100);
    imageFrame(page, b(20, 158, 118, 252), groupAsset("Mediation", n), 100);
    imageFrame(page, b(122, 158, 199, 252), groupAsset("Agency", n), 100);
    caption(page, b(102, 162, 118, 248), groupAsset("Mediation", n), ink, cream);
  }} else if (n === 6) {{
    imageFrame(page, b(-4, -4, 220, 284), groupAsset("Constraint", n), 100);
    colorPanel(page, b(-4, -4, 220, 284), ink, 48);
    textFrame(page, b(148, 18, 186, 250), "The image does not give itself all at once.", 26, "Bold", cream, 100);
    textFrame(page, b(186, 18, 200, 252), "Controlled revelation is the method. Tension is the evidence.", 11, "Regular", cream, 100);
  }} else {{
    textFrame(page, b(18, 18, 30, 220), "THE THREE PRESSURES", 12, "Bold", gold, 100);
    textFrame(page, b(40, 18, 70, 96), "AGENCY\\rbody as force", 14, "Bold", cream, 100);
    textFrame(page, b(40, 100, 70, 178), "CONSTRAINT\\rbody as protocol", 14, "Bold", cream, 100);
    textFrame(page, b(40, 182, 70, 262), "MEDIATION\\rveil as edit", 14, "Bold", cream, 100);
    imageFrame(page, b(80, 18, 150, 263), groupAsset("Agency", n), 100);
    textFrame(page, b(156, 18, 198, 255), COPY.intro, 9.5, "Regular", cream, 100);
  }}
}}

function articlePage(page, n, section, item, item2, item3, doc, ink, cream, gold, slate) {{
  var mode = n % 3;
  var body = copyChunk(section.toLowerCase(), n);
  if (!body) {{
    imageFrame(page, b(-4, -4, 220, 284), item, 100);
    colorPanel(page, b(-4, -4, 220, 284), ink, 30);
    textFrame(page, b(18, 18, 30, 220), section + " / SEQUENCE", 9, "Bold", gold, 100);
    caption(page, b(176, 18, 200, 150), item, ink, cream);
    return;
  }}
  if (mode === 0) {{
    // Dominant image left, text column right.
    imageFrame(page, b(16, 16, 199, 150), item, 100);
    textFrame(page, b(20, 160, 44, 262), section, 20, "Bold", cream, 100);
    textFrame(page, b(46, 160, 199, 262), body, 9.2, "Regular", cream, 100);
    caption(page, b(180, 20, 199, 110), item, ink, cream);
  }} else if (mode === 1) {{
    // Full-bleed image, scrim, pull statement, body panel.
    imageFrame(page, b(-4, -4, 220, 284), item, 100);
    colorPanel(page, b(-4, -4, 220, 284), ink, 50);
    textFrame(page, b(20, 18, 26, 170), "ARTICLE / " + section, 8, "Bold", gold, 100);
    textFrame(page, b(30, 18, 74, 240), "Only one eye remains; the image gets louder.", 24, "Bold", cream, 100);
    colorPanel(page, b(150, 12, 200, 150), ink, 58);
    textFrame(page, b(154, 18, 198, 146), body, 8.6, "Regular", cream, 100);
  }} else {{
    // Triptych: three images across, text band beneath (multi-image spread).
    imageFrame(page, b(16, 16, 132, 95), item, 100);
    imageFrame(page, b(16, 100, 132, 179), item2, 100);
    imageFrame(page, b(16, 184, 132, 263), item3, 100);
    textFrame(page, b(140, 16, 162, 262), section + " / SEQUENCE", 16, "Bold", cream, 100);
    textFrame(page, b(164, 16, 199, 262), body, 9, "Regular", cream, 100);
    caption(page, b(116, 104, 132, 175), item2, ink, cream);
  }}
}}

function backMatter(page, n, doc, ink, cream, gold) {{
  if (n === 50) {{
    textFrame(page, b(40, 18, 96, 230), "Sight remains\\runfinished.", 34, "Bold", cream, 100);
    textFrame(page, b(150, 18, 190, 250), "Every act of looking leaves a remainder: memory, attention, and the need to interpret what the eye cannot settle.", 10, "Regular", cream, 100);
    return;
  }}
  var head = n === 46 ? "IMAGE SOURCE REGISTER" : n === 47 ? "IMAGE SOURCE REGISTER / CONTINUED" : n === 48 ? "SOURCE LIST" : "COLOPHON";
  textFrame(page, b(18, 18, 34, 255), head, 14, "Bold", gold, 100);
  if (n === 46 || n === 47) {{
    var startIdx = n === 46 ? 0 : 32;
    var lines = "";
    for (var i = startIdx; i < Math.min(startIdx + 32, ASSETS.length); i++) {{
      lines += ASSETS[i].id + "  " + ASSETS[i].title + " - rights verify\\r";
    }}
    textFrame(page, b(40, 18, 200, 255), lines, 8, "Regular", cream, 100);
  }} else if (n === 48) {{
    textFrame(page, b(40, 18, 200, 255), "McDermott: Paleolithic agency and the body. Havelock/Reeder: Greek art, cultural constraint, posture, social rule. Veiling iconography / Vera Icona / lace / mediation theory. Verify all exact source details before final export. No direct quotations are used because source texts were not supplied.", 10, "Regular", cream, 100);
  }} else {{
    textFrame(page, b(40, 18, 200, 255), "The Visceral Theory of Sight is a visual-psychology issue on gaze, image memory, and the veil. Written, sequenced, and designed by Brooke Chauntel for Everett Community College, 2026. Photographs are credited in the Image Source Register; scholarly works are listed under Works Consulted. Set in Helvetica and Times, printed white on black.", 10, "Regular", cream, 100);
  }}
}}

var doc = setupDoc();
var ink = addSwatch(doc, "Ink", [17, 16, 14]);
var cream = addSwatch(doc, "Archival Cream", [243, 235, 221]);
var gold = addSwatch(doc, "Muted Gold", [165, 130, 66]);
var slate = addSwatch(doc, "Slate Blue", [82, 107, 122]);

for (var p = 0; p < doc.pages.length; p++) {{
  var page = doc.pages[p];
  var n = p + 1;
  colorPanel(page, b(-4, -4, 220, 284), ink, 100);
  if (n === 1) cover(page, doc, ink, cream, gold);
  else if (n <= 4) frontMatter(page, n, doc, ink, cream, gold);
  else if (n <= 7) introPage(page, n, doc, ink, cream, gold);
  else if (n === 8) sectionTitle(page, "Agency", ink, cream, gold);
  else if (n <= 16) articlePage(page, n, "AGENCY", groupAsset("Agency", n), groupAsset("Agency", n + 1), groupAsset("Agency", n + 2), doc, ink, cream, gold, slate);
  else if (n === 17) sectionTitle(page, "Constraint", ink, cream, gold);
  else if (n <= 26) articlePage(page, n, "CONSTRAINT", groupAsset("Constraint", n), groupAsset("Constraint", n + 1), groupAsset("Constraint", n + 2), doc, ink, cream, gold, slate);
  else if (n === 27) sectionTitle(page, "Mediation", ink, cream, gold);
  else if (n <= 38) articlePage(page, n, "MEDIATION", groupAsset("Mediation", n), groupAsset("Mediation", n + 1), groupAsset("Mediation", n + 2), doc, ink, cream, gold, slate);
  else if (n === 39) sectionTitle(page, "Synthesis", ink, cream, gold);
  else if (n <= 45) articlePage(page, n, "SYNTHESIS", asset(n), asset(n + 1), asset(n + 2), doc, ink, cream, gold, slate);
  else backMatter(page, n, doc, ink, cream, gold);
  pageNum(page, n, ink);
}}

// Final overset guard.
for (var i = 0; i < doc.textFrames.length; i++) {{
  if (doc.textFrames[i].overflows) fitText(doc.textFrames[i], 5.5);
}}

configurePreflight(doc);
saveDesktopFiles(doc);
"""
    (TEMPLATE_OUT / "indesign-build-full-layout.jsx").write_text(jsx, encoding="utf-8")


def generate_cover(assets: list[Asset]) -> None:
    cover = PDF_OUT / "cover-design.pdf"
    c = canvas.Canvas(str(cover), pagesize=(PAGE_W, PAGE_H))
    preferred = next((a for a in assets if "white lace blindfold" in a.filename.lower()), assets[0])
    preferred = make_cover_asset(preferred)
    draw_cover(c, preferred)
    c.showPage()
    c.save()
    apply_print_boxes(cover)


def generate_book(assets: list[Asset]) -> None:
    book = PDF_OUT / "the-visceral-theory-of-sight-50pp.pdf"
    c = canvas.Canvas(str(book), pagesize=(PAGE_W, PAGE_H))
    cover_asset = next((a for a in assets if "white lace blindfold" in a.filename.lower()), assets[0])
    cover_asset = make_cover_asset(cover_asset)
    title_asset = next((a for a in assets if "Mediation" in a.group and a is not cover_asset), assets[1])
    draw_cover(c, cover_asset, page_num=1)
    c.showPage()
    draw_title_spread(c, title_asset, "left")
    c.showPage()
    draw_title_spread(c, title_asset, "right")
    c.showPage()
    draw_toc(c)
    c.showPage()

    for page in range(5, 8):
        draw_intro(c, page, assets)
        c.showPage()

    agency_assets = [a for a in assets if "Agency" in a.group] or assets
    constraint_assets = [a for a in assets if "Constraint" in a.group] or assets
    med_assets = [a for a in assets if "Mediation" in a.group] or assets
    page_assets = assets.copy()
    # Each section opens with a full-bleed image + title page, then content pages.
    for offset, page in enumerate(range(8, 17)):
        if offset == 0:
            draw_section_title(c, page, "Agency", agency_assets[3 % len(agency_assets)])
        else:
            draw_article_page(c, page, "Agency", agency_assets, offset - 1)
        c.showPage()
    for offset, page in enumerate(range(17, 27)):
        if offset == 0:
            draw_section_title(c, page, "Constraint", constraint_assets[1 % len(constraint_assets)])
        else:
            draw_article_page(c, page, "Constraint", constraint_assets, offset - 1)
        c.showPage()
    for offset, page in enumerate(range(27, 39)):
        if offset == 0:
            draw_section_title(c, page, "Mediation", next((a for a in assets if "allef-vinicius" in a.filename.lower()), med_assets[2 % len(med_assets)]))
        else:
            draw_article_page(c, page, "Mediation", med_assets, offset - 1)
        c.showPage()
    for offset, page in enumerate(range(39, 46)):
        if offset == 0:
            draw_section_title(c, page, "Synthesis", page_assets[20 % len(page_assets)])
        else:
            draw_synthesis(c, page, page_assets, offset - 1)
        c.showPage()
    for page in range(46, 51):
        draw_back_matter(c, page, assets)
        c.showPage()
    c.save()
    apply_print_boxes(book)


def write_manifest(assets: list[Asset]) -> None:
    manifest = {
        "title": "The Visceral Theory of Sight",
        "route": str(ROUTE),
        "asset_count": len(assets),
        "outputs": {
            "cover_pdf": str(PDF_OUT / "cover-design.pdf"),
            "book_pdf": str(PDF_OUT / "the-visceral-theory-of-sight-50pp.pdf"),
            "indesign_file": str(INDESIGN_OUT / "the-visceral-theory-of-sight-50pp.indd"),
            "idml_file": str(INDESIGN_OUT / "the-visceral-theory-of-sight-50pp.idml"),
            "affinity_native_target": str(ROUTE / "output" / "affinity" / "the-visceral-theory-of-sight-50pp.afpub"),
            "ledger": str(LEDGER_OUT / "source-image-ledger.csv"),
            "notes": str(NOTES_OUT / "critical-process-notes.md"),
            "grid_blueprint_json": str(TEMPLATE_OUT / "indesign-affinity-grid-blueprint.json"),
            "grid_blueprint_markdown": str(TEMPLATE_OUT / "indesign-affinity-grid-blueprint.md"),
            "indesign_autobuild_jsx": str(TEMPLATE_OUT / "indesign-create-a4-grid.jsx"),
            "indesign_full_layout_jsx": str(TEMPLATE_OUT / "indesign-build-full-layout.jsx"),
            "indesign_overset_repair_jsx": str(TEMPLATE_OUT / "indesign-fix-overset-text.jsx"),
            "idml_handoff_notes": str(TEMPLATE_OUT / "idml-indesign-affinity-handoff.md"),
        },
        "source_policy": "No invented citations, quotations, page numbers, or rights claims. Verify before final export.",
        "geometry": {
            "trim": "A4 portrait, 210mm x 297mm",
            "bleed": "3mm all sides",
            "columns": 12,
            "gutter": "5mm",
            "outer_margin": "7.5 percent of trim width",
            "inner_margin": "10 percent of trim width",
            "top_bottom_margin": "7 percent of trim height",
        },
    }
    (MANIFEST_OUT / "production-manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    ensure_dirs()
    clean_generated_dirs()
    assets = scan_assets()
    write_ledger(assets)
    write_notes(assets)
    write_grid_handoff()
    write_full_layout_jsx(assets)
    generate_cover(assets)
    generate_book(assets)
    write_manifest(assets)
    print(f"Built production route: {ROUTE}")
    print(f"Assets copied: {len(assets)}")
    print(f"Cover PDF: {PDF_OUT / 'cover-design.pdf'}")
    print(f"Book PDF: {PDF_OUT / 'the-visceral-theory-of-sight-50pp.pdf'}")
    print(f"Ledger: {LEDGER_OUT / 'source-image-ledger.csv'}")
    print(f"Notes: {NOTES_OUT / 'critical-process-notes.md'}")


if __name__ == "__main__":
    main()
