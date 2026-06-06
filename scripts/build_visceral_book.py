from __future__ import annotations

import csv
import json
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
from pypdf import PdfReader, PdfWriter


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ASSETS = Path(
    r"C:\Users\toddl\OneDrive\Desktop\SCHOOL\Graph252 booklab\visceral-theory of sight assets"
)
ROUTE = ROOT / "visceral-production-route"
ASSET_OUT = ROUTE / "assets"
PDF_OUT = ROUTE / "output" / "pdf"
INDESIGN_OUT = ROUTE / "output" / "indesign"
LEDGER_OUT = ROUTE / "ledgers"
NOTES_OUT = ROUTE / "notes"
MANIFEST_OUT = ROUTE / "manifest"
TEMPLATE_OUT = ROUTE / "templates"
REPORTS_OUT = ROUTE / "reports"
EXCLUDED_ASSET_IDS = {"A02", "A03", "A04"}

TRIM_W, TRIM_H = A4
BLEED = 3 * mm
PAGE_W, PAGE_H = TRIM_W + (2 * BLEED), TRIM_H + (2 * BLEED)
OUTER_MARGIN = TRIM_W * 0.075
INNER_MARGIN = TRIM_W * 0.10
TOP_MARGIN = TRIM_H * 0.07
BOTTOM_MARGIN = TRIM_H * 0.07
GUTTER = 5 * mm
COLUMNS = 12
LIVE_W = TRIM_W - INNER_MARGIN - OUTER_MARGIN
COLUMN_W = (LIVE_W - (GUTTER * (COLUMNS - 1))) / COLUMNS
INK = colors.HexColor("#11100E")
CREAM = colors.HexColor("#F3EBDD")
GOLD = colors.HexColor("#A58242")
SLATE = colors.HexColor("#526B7A")
MIST = colors.HexColor("#D8D0C0")
SOFT_BLACK = colors.HexColor("#1C1B19")

ARTICLE_BODIES = {
    "Agency": (
        "The body becomes the first instrument of authorship before it becomes a subject for interpretation. "
        "In the first movement of this issue, sight begins with bodily insistence: a hand, a shoulder, a mouth, "
        "an eye, or a turned face does not wait for culture to explain it. The figure enters as pressure. It "
        "occupies the field with the blunt force of being present, and that presence matters because the viewer "
        "has not yet been given a stable rule for reading it.\n\n"
        "McDermott gives this article its earliest time marker: the female body can be read as more than a passive "
        "object of display. His argument around Upper Paleolithic figurines opens a different possibility: that bodily "
        "representation may also carry evidence of lived perception, self-reference, and embodied seeing. That matters "
        "because a body can be partial and still be active. A face can be interrupted and still hold attention. A hand "
        "can become the first sign of agency before the viewer has named the person. The issue treats the body as origin, not "
        "because origin is simple, but because every later system of looking must first meet the fact of the body.\n\n"
        "Agency is close, image-led, and slightly uncomfortable. Faces and fragments interrupt the viewer before the viewer "
        "has decided what kind of image this is. A direct stare can feel like contact. A hidden eye can feel like refusal. "
        "A turned face can feel like a body protecting its own interior life. The body is not an illustration of theory. "
        "It is the condition that makes theory necessary.\n\n"
        "This is also where the neural-learning backdrop enters quietly. Looking is not passive reception. The eye learns "
        "by comparing pressure, repetition, interruption, and contrast. A body seen once is an image. A body seen across "
        "time becomes a pattern the reader has to interpret. The first article therefore builds a visual lesson in agency: "
        "presence arrives before permission."
    ),
    "Constraint": (
        "Culture turns visibility into a protocol. The second movement begins when bodily force is no longer allowed "
        "to stand alone. The figure becomes arranged by posture, costume, rank, gender, ritual, and inherited rules of "
        "display. A face can still look outward, but it now looks through an architecture of expectation. A body can "
        "still occupy the frame, but the frame has begun to instruct it.\n\n"
        "The movement through time matters here. Maternity, labor, beauty, mourning, ordinary weather, and public presence "
        "are not separate categories; they are visual roles that cultures attach to women. Mulley's study of Laura Muntz "
        "shows how maternity can be made symbolic, intimate, and burdened at once. Morrissy's work on Una Watters brings "
        "the woman back into everyday weather and street life, where representation is less idealized and more socially "
        "placed.\n\n"
        "Constraint does not erase agency. It redirects it. The body still carries force, but that force is shaped by "
        "context: who is permitted to look, who is expected to be seen, and what a culture teaches the viewer to accept "
        "as natural. This section feels less wild than the first, but more tense. The reader should sense that the body has entered "
        "a room where every gesture is already being measured.\n\n"
        "This matters to the theory of sight because the viewer is also constrained. We do not only look at the ruled "
        "body; we learn the rule by looking. Repetition, obstruction, pose, and symbol teach the eye how social meaning "
        "attaches to bodies through time. The eye becomes disciplined alongside the figure. Seeing is no "
        "longer just contact. It is compliance, resistance, and learned interpretation happening at the same time."
    ),
    "Mediation": (
        "The veil is an editing system, not a disappearance. The third movement begins where the body and the rule meet "
        "a surface that can interrupt both. Lace, shadow, fabric, blur, flowers, hair, hands, and darkness all become "
        "interfaces. They do not simply hide the figure. They decide how slowly the figure can arrive.\n\n"
        "The veiling route is held through iconography, Vera Icona, lace, secrecy, and the larger problem of mediated "
        "access. The key point is not that the viewer is denied. The key point is that denial becomes structure. A veil "
        "produces a special kind of attention because the eye has to work without full possession. It keeps searching, "
        "comparing edges, reading textures, and inventing continuity from fragments.\n\n"
        "Art movement history clarifies the pressure. Symbolism treats the visible world as a carrier for inward states; "
        "Surrealist image logic turns ordinary surfaces into psychic interruption. The covered eye, the soft obstruction, "
        "and the displaced face do not merely hide information. They make interpretation the subject. The viewer is asked "
        "to feel the delay between perception and certainty.\n\n"
        "This section becomes more atmospheric, with more surface interruption and slower perception, but it still carries "
        "an argument: mediation is the place where agency and constraint become visible as tension. The body wants to "
        "appear. The rule wants to organize appearance. The veil controls the tempo of access.\n\n"
        "The idea stays modular: surface, delay, pressure, "
        "partial access. Those repeated terms create a learning path through the atmosphere. The reader can feel the "
        "mystery without getting lost inside it. The veil does not remove meaning. It makes meaning arrive through effort."
    ),
    "Synthesis": (
        "Sight becomes visceral when these forces remain active together. The final movement refuses to solve the body, "
        "the rule, and the veil into a clean hierarchy. Agency begins the argument, constraint disciplines it, and "
        "mediation keeps it unresolved. The image becomes powerful because no single force wins.\n\n"
        "This is the core thesis of the book: psychological pressure does not come from clear depiction alone. It comes "
        "from calculated revelation. The viewer feels the image because the image negotiates what can be seen, how quickly "
        "it can be seen, and what remains withheld even after attention has been spent. The body is present, but not fully "
        "available. Culture is legible, but not neutral. The veil interrupts, but also teaches the eye how to continue.\n\n"
        "Psychology gives the gaze its behavioral force. Research on gaze cueing and social attention shows that eye "
        "direction affects an observer's attention and social interpretation, which is why a portrait can feel active "
        "even when nothing in the frame moves. The gaze is not only a theme. It is a human signal system.\n\n"
        "The synthesis refuses easy balance. Large images take authority, and the argument holds sight in motion instead "
        "of pretending it has settled. The instability is not decoration. It is the final proof of the argument: unstable "
        "sight is where learning happens.\n\n"
        "The conclusion keeps the claims careful. It does not invent quotations, publication details, or license certainty. "
        "It names the scholarly routes that support the issue and keeps the theory visible in the reading itself."
    ),
}

SECTION_PAGE_START = {
    "Agency": 8,
    "Constraint": 17,
    "Mediation": 27,
    "Synthesis": 39,
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


def infer_rights(name: str) -> str:
    lowered = name.lower()
    if "unsplash" in lowered:
        return "Unsplash filename present; verify source URL and license before final export."
    if "adobestock" in lowered:
        return "Adobe Stock filename present; verify local license before final export."
    return "Local/generated/unknown source; verify creator, source, and usage rights before final export."


def infer_creator(name: str) -> str:
    lowered = name.lower()
    if "unsplash" in lowered:
        slug = name.split("-unsplash")[0]
        return slug.replace("-", " ").title() + " / Unsplash filename"
    if "adobestock" in lowered:
        return "Adobe Stock contributor not verified"
    return "Creator not verified"


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


def scan_assets() -> list[Asset]:
    files = sorted(
        [p for p in SOURCE_ASSETS.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}],
        key=lambda p: p.name.lower(),
    )
    assets: list[Asset] = []
    for i, path in enumerate(files, start=1):
        out_name = f"asset-{i:02d}{path.suffix.lower()}"
        local = ASSET_OUT / out_name
        shutil.copy2(path, local)
        with Image.open(local) as img:
            width, height = img.size
        group = infer_group(i, path.name)
        title = path.stem
        assets.append(
            Asset(
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
        )
    return assets


def draw_bg(c: canvas.Canvas, dark: bool = False) -> None:
    c.setFillColor(SOFT_BLACK if dark else CREAM)
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
    color=INK,
    max_lines: int | None = None,
) -> float:
    c.setFont(font, size)
    c.setFillColor(color)
    lines: list[str] = []
    for para in text.split("\n"):
        if not para.strip():
            lines.append("")
        else:
            lines.extend(wrap(para, width=width_chars))
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def draw_label(c: canvas.Canvas, text: str, x: float, y: float, color=GOLD) -> None:
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(color)
    c.drawString(x, y, text.upper())


def draw_page_number(c: canvas.Canvas, page: int, dark: bool = False) -> None:
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
    c.setFont("Helvetica", 6.5)
    caption = f"{asset.id} / {asset.title[:68]} / rights: verify"
    c.drawString(x, y, caption[:100])
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
    c.setFont("Helvetica", 6.2)
    c.drawString(x, y - 7, "A controlled glimpse becomes part of the argument.")


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
        "decides what can be touched by the eye. This book moves through agency, "
        "constraint, and mediation as one visual pressure system."
    )


def section_copy(section: str) -> str:
    return ARTICLE_BODIES[section]


def article_excerpt(section: str, page: int, target_chars: int = 520) -> str:
    words = ARTICLE_BODIES[section].replace("\n", " ").split()
    if not words:
        return ""
    start_page = SECTION_PAGE_START[section]
    offset = max(0, page - start_page)
    words_per_page = max(55, target_chars // 6)
    start = min(offset * words_per_page, max(0, len(words) - words_per_page))
    excerpt_words = words[start : start + words_per_page]
    return " ".join(excerpt_words)


def draw_cover(c: canvas.Canvas, asset: Asset, page_num: int | None = None) -> None:
    draw_bg(c, dark=True)
    image_box(c, asset, 66, 138, PAGE_W - 132, PAGE_H * 0.68)
    c.setFillColor(CREAM)
    c.setFont("Helvetica-Bold", 37)
    c.drawCentredString(PAGE_W / 2, 103, "THE VISCERAL")
    c.drawCentredString(PAGE_W / 2, 66, "THEORY OF SIGHT")
    c.setFont("Times-Roman", 10)
    c.drawCentredString(PAGE_W / 2, 43, "the body, the gaze, and the veil")
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.line(138, 124, PAGE_W - 138, 124)
    if page_num:
        draw_page_number(c, page_num, dark=True)


def draw_title_page(c: canvas.Canvas) -> None:
    draw_bg(c)
    draw_label(c, "title page", 72, PAGE_H - 90)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 40)
    c.drawString(72, PAGE_H - 185, "The Anatomy")
    c.drawString(72, PAGE_H - 228, "of Looking")
    c.setFont("Times-Roman", 13)
    c.drawString(74, PAGE_H - 270, "A 50-page visual psychology issue on attention, image memory, and human sight.")
    c.setFont("Helvetica", 8)
    c.drawString(74, 90, "Compiled as a visual psychology issue for publication review.")
    c.drawString(74, 76, "All citations and rights marked for verification before final export.")
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
    draw_text_block(c, text, 78, 185, width_chars=78, leading=13, size=9)
    draw_page_number(c, 3)


def draw_toc(c: canvas.Canvas) -> None:
    draw_bg(c)
    draw_label(c, "contents", 72, PAGE_H - 90)
    c.setFont("Helvetica-Bold", 30)
    c.setFillColor(INK)
    c.drawString(72, PAGE_H - 150, "Body / Rule / Veil")
    entries = [
        ("Front Matter", "01-04"),
        ("Introduction: The Anatomy of Looking", "05-07"),
        ("I. The Body", "08-16"),
        ("II. The Constraint", "17-26"),
        ("III. The Veil", "27-38"),
        ("Synthesis and Reflection", "39-45"),
        ("Back Matter", "46-50"),
    ]
    x_positions = [72, 245, 420]
    y = PAGE_H - 235
    for i, (title, pages) in enumerate(entries):
        x = x_positions[i % 3]
        if i and i % 3 == 0:
            y -= 115
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(GOLD if i % 2 else INK)
        c.drawString(x, y, pages)
        c.setFont("Times-Roman", 11)
        c.setFillColor(INK)
        draw_text_block(c, title, x, y - 19, width_chars=19, leading=12, size=10)
    draw_page_number(c, 4)


def draw_intro(c: canvas.Canvas, page: int, assets: list[Asset]) -> None:
    draw_bg(c, dark=page == 6)
    dark = page == 6
    if page == 5:
        image_box(c, assets[0], 54, 370, 190, 285)
        image_box(c, assets[5], 260, 300, 285, 175)
        image_box(c, assets[10], 340, 500, 170, 130)
        draw_label(c, "introduction", 72, 250)
        c.setFont("Helvetica-Bold", 30)
        c.setFillColor(INK)
        c.drawString(72, 212, "The Anatomy")
        c.drawString(72, 178, "of Looking")
        draw_text_block(c, intro_copy(), 74, 138, width_chars=70, leading=13, size=9.5)
    elif page == 6:
        image_box(c, assets[2], 48, 118, PAGE_W - 96, PAGE_H - 190)
        c.setFillColor(CREAM)
        c.setFont("Helvetica-Bold", 24)
        c.drawString(72, PAGE_H - 88, "The image does not give itself all at once.")
        draw_text_block(c, "Controlled revelation is the method. Tension is the evidence.", 74, 92, 62, 13, 10, color=CREAM)
    else:
        cols = [(72, 510), (246, 430), (420, 350)]
        labels = [("AGENCY", "body as force"), ("CONSTRAINT", "body as protocol"), ("MEDIATION", "veil as edit")]
        for (x, y), (head, sub) in zip(cols, labels):
            c.setFillColor(GOLD)
            c.rect(x, y, 92, 3, fill=1, stroke=0)
            c.setFillColor(INK)
            c.setFont("Helvetica-Bold", 16)
            c.drawString(x, y - 32, head)
            c.setFont("Times-Roman", 11)
            c.drawString(x, y - 51, sub)
        draw_text_block(c, intro_copy(), 72, 235, width_chars=76, leading=14, size=10)
    draw_page_number(c, page, dark=dark)


def draw_article_page(c: canvas.Canvas, page: int, section: str, asset: Asset, variant: int) -> None:
    dark = variant in {2, 5}
    draw_bg(c, dark=dark)
    fg = CREAM if dark else INK
    accent = GOLD if section != "Mediation" else SLATE
    body_text = article_excerpt(section, page)
    if variant == 0:
        image_box(c, asset, 48, 170, 356, 510)
        translucent_panel(c, 360, 470, 178, 155, dark=dark, alpha=0.88)
        c.setFillColor(fg)
        c.setFont("Helvetica-Bold", 24)
        c.drawString(374, 590, section.upper())
        draw_text_block(c, body_text, 376, 552, 29, 12.2, 8.2, color=fg)
        overlay_caption(c, asset, 72, 186, 210, dark=True)
    elif variant == 1:
        image_box(c, asset, 176, 238, 390, 365)
        c.setFillColor(accent)
        c.rect(64, 112, 104, 548, fill=1, stroke=0)
        c.setFillColor(CREAM)
        c.setFont("Helvetica-Bold", 25)
        c.saveState()
        c.translate(105, 180)
        c.rotate(90)
        c.drawString(0, 0, section.upper())
        c.restoreState()
        translucent_panel(c, 148, 188, 345, 86, dark=dark, alpha=0.80)
        draw_text_block(c, body_text, 164, 250, 55, 11, 7.7, color=fg, max_lines=8)
        overlay_caption(c, asset, 408, 252, 138, dark=True)
    elif variant == 2:
        image_box(c, asset, 0, 0, PAGE_W, PAGE_H)
        c.setFillColor(colors.Color(0, 0, 0, alpha=0.46))
        c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        draw_pull_quote(c, ["ONLY ONE", "EYE REMAINS,", "THE IMAGE", "GETS LOUDER."], PAGE_H - 280, dark=True)
        c.setFillColor(colors.Color(0, 0, 0, alpha=0.66))
        c.rect(54, 72, 228, 260, fill=1, stroke=0)
        draw_label(c, f"article / {section}", 72, 386, color=accent)
        draw_text_block(c, body_text, 72, 302, 38, 11.2, 7.8, color=CREAM, max_lines=17)
    elif variant == 3:
        image_box(c, asset, 54, 420, 260, 238)
        image_box(c, asset, 286, 118, 260, 402)
        c.setStrokeColor(accent)
        c.setLineWidth(2.2)
        c.line(54, 410, 548, 518)
        translucent_panel(c, 72, 272, 292, 98, dark=dark, alpha=0.78)
        c.setFillColor(fg)
        c.setFont("Helvetica-Bold", 18)
        c.drawString(84, 343, "A body becomes legible through pressure.")
        draw_text_block(c, body_text, 86, 318, 52, 10.6, 7.5, color=fg, max_lines=8)
        overlay_caption(c, asset, 330, 490, 150, dark=True)
    elif variant == 4:
        c.setStrokeColor(accent)
        for i in range(12):
            x = INNER_MARGIN + BLEED + i * (COLUMN_W + GUTTER)
            c.line(x, 58, x, PAGE_H - 58)
        image_box(c, asset, 82, 170, 438, 456)
        draw_pull_quote(c, ["THE VEIL", "DOES NOT", "DISAPPEAR", "THE BODY."], 112, dark=False)
        c.setFillColor(CREAM if section == "Mediation" else SOFT_BLACK)
        c.rect(356, 468, 190, 108, fill=1, stroke=0)
        draw_text_block(c, body_text, 370, 548, 31, 10.2, 7.4, color=INK if section == "Mediation" else CREAM, max_lines=10)
    else:
        image_box(c, asset, 112, 95, 410, 605)
        translucent_panel(c, 62, 598, 278, 68, dark=dark, alpha=0.76)
        c.setFillColor(fg)
        c.setFont("Helvetica-Bold", 17)
        c.drawString(78, 638, "Looking is edited by access")
        draw_text_block(c, body_text, 74, 112, 38, 10.4, 7.4, color=fg, max_lines=12)
        overlay_caption(c, asset, 344, 116, 150, dark=True)
    draw_page_number(c, page, dark=dark)


def draw_synthesis(c: canvas.Canvas, page: int, asset: Asset, variant: int) -> None:
    dark = variant % 2 == 0
    draw_bg(c, dark=dark)
    fg = CREAM if dark else INK
    body_text = article_excerpt("Synthesis", page)
    if variant in {0, 3}:
        image_box(c, asset, 38, 76, 392, 642)
        c.setFillColor(colors.Color(0, 0, 0, alpha=0.30) if dark else colors.Color(0.953, 0.922, 0.866, alpha=0.35))
        c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        translucent_panel(c, 382, 452, 176, 190, dark=dark, alpha=0.82)
        c.setFillColor(fg)
        c.setFont("Helvetica-Bold", 20)
        c.drawString(404, 610, "Unresolved Sight")
        draw_text_block(c, body_text, 404, 574, 28, 11.2, 7.8, color=fg)
        overlay_caption(c, asset, 76, 104, 180, dark=True)
    else:
        image_box(c, asset, 132, 132, 426, 492)
        c.setStrokeColor(GOLD)
        c.setLineWidth(2)
        c.rect(64, 94, 418, 552, fill=0, stroke=1)
        draw_pull_quote(c, ["LOOKING", "NEVER", "ARRIVES", "CLEAN."], PAGE_H - 198, dark=dark)
        translucent_panel(c, 84, 82, 404, 70, dark=dark, alpha=0.78)
        draw_text_block(c, body_text, 96, 132, 76, 10, 7.4, color=fg, max_lines=7)
    draw_page_number(c, page, dark=dark)


def draw_back_matter(c: canvas.Canvas, page: int, assets: list[Asset]) -> None:
    draw_bg(c)
    if page == 46:
        draw_label(c, "image credits", 72, PAGE_H - 72)
        y = PAGE_H - 110
        for asset in assets[:14]:
            line = f"{asset.id}. {asset.title[:42]} | {asset.creator[:26]} | rights verify"
            y = draw_text_block(c, line, 72, y, 86, 10, 7.5)
    elif page == 47:
        draw_label(c, "image credits continued", 72, PAGE_H - 72)
        y = PAGE_H - 110
        for asset in assets[14:]:
            line = f"{asset.id}. {asset.title[:42]} | {asset.creator[:26]} | rights verify"
            y = draw_text_block(c, line, 72, y, 86, 10, 7.5)
    elif page == 48:
        draw_label(c, "source list", 72, PAGE_H - 72)
        text = (
            "McDermott: Paleolithic agency and the body. Verify exact article/book details before final export.\n\n"
            "Havelock/Reeder: Greek art, cultural constraint, posture, social rule, and controlled body. Verify exact source details before final export.\n\n"
            "Veiling iconography / Vera Icona / lace / mediation theory. Verify exact scholarly source details before final export.\n\n"
            "No direct quotations are used in this proof because the source texts were not supplied in the current workspace."
        )
        draw_text_block(c, text, 72, PAGE_H - 120, 82, 14, 10)
    elif page == 49:
        draw_label(c, "process / critical notes", 72, PAGE_H - 72)
        text = (
            "The issue closes by returning to the reader's own attention. Agency, constraint, and mediation are not separate stages of seeing; they are pressures that arrive together whenever a face, veil, gesture, or symbol asks to be interpreted. "
            "Sight remains active because the mind keeps revising what the eye first accepted."
        )
        draw_text_block(c, text, 72, PAGE_H - 120, 82, 14, 10)
    else:
        c.setFont("Helvetica-Bold", 34)
        c.setFillColor(INK)
        c.drawString(72, PAGE_H - 180, "Sight remains")
        c.drawString(72, PAGE_H - 220, "unfinished.")
        draw_text_block(c, "Every act of looking leaves a remainder: memory, attention, and the human need to interpret what the eye cannot settle.", 74, 150, 72, 14, 10)
    draw_page_number(c, page)


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
    assets = [asset for asset in assets if asset.id not in EXCLUDED_ASSET_IDS]
    js_assets = [
        {
            "id": asset.id,
            "path": asset.local_path.as_posix(),
            "title": asset.title[:58],
            "group": asset.group,
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
    output_indd = INDESIGN_OUT / "the-visceral-theory-of-sight-50pp.indd"
    output_idml = INDESIGN_OUT / "the-visceral-theory-of-sight-50pp.idml"
    output_pdf = PDF_OUT / "the-visceral-theory-of-sight-50pp-indesign-auto.pdf"
    output_report = REPORTS_OUT / "indesign-full-layout-auto-report.json"
    jsx = f"""// The Anatomy of Looking - full 50-page InDesign issue builder
// Run from InDesign: File > Scripts > Other Script...
// Builds the print issue, linked image sequence, PDF proof, and audit report.

var ASSETS = {assets_literal};
var OUTPUT_INDD = {json.dumps(output_indd.as_posix())};
var OUTPUT_IDML = {json.dumps(output_idml.as_posix())};
var OUTPUT_PDF = {json.dumps(output_pdf.as_posix())};
var OUTPUT_REPORT = {json.dumps(output_report.as_posix())};

app.scriptPreferences.userInteractionLevel = UserInteractionLevels.NEVER_INTERACT;

var COPY = {copy_literal};

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
function assetById(id) {{
  for (var a = 0; a < ASSETS.length; a++) {{
    if (ASSETS[a].id === id) return ASSETS[a];
  }}
  return ASSETS[0];
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
  var startPage = key === "agency" ? 8 : key === "constraint" ? 17 : key === "mediation" ? 27 : 39;
  var offset = Math.max(0, n - startPage);
  var wordsPerPage = 52;
  var start = Math.min(offset * wordsPerPage, Math.max(0, words.length - wordsPerPage));
  return words.slice(start, start + wordsPerPage).join(" ");
}}

function setupDoc() {{
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
  return doc;
}}

function configurePublicationPreflight(doc) {{
  var profileName = "Anatomy of Looking - Color Landscape";
  var profile;
  try {{
    profile = app.preflightProfiles.itemByName(profileName);
    profile.name;
  }} catch (missing) {{
    profile = app.preflightProfiles.itemByName("kDigPubProfileName").duplicate();
    profile.name = profileName;
  }}
  profile.description = "Color landscape magazine profile. Keeps Digital Publishing checks while allowing intentional color plates and landscape orientation.";
  profile.preflightProfileRules.itemByName("ADBE_CMYPlates").flag = 1699890274;
  profile.preflightProfileRules.itemByName("ADBE_PageSizeOrientation").flag = 1699890274;
  doc.preflightOptions.preflightWorkingProfile = profile;
  doc.preflightOptions.preflightOff = false;
  return profile;
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
  while (tf.overflows && attempts < 18) {{
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
    tf.textFramePreferences.autoSizingType = AutoSizingTypeEnum.HEIGHT_ONLY;
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
  fitText(tf, 6.5);
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
  try {{
    app.interactivePDFExportPreferences.exportReaderSpreads = false;
    app.interactivePDFExportPreferences.generateThumbnails = true;
    doc.exportFile(ExportFormat.INTERACTIVE_PDF, pdfFile, false);
    return "interactive";
  }} catch (interactiveErr) {{}}
  var preset = null;
  try {{
    app.pdfExportPreferences.includeHyperlinks = true;
    app.pdfExportPreferences.exportLayers = false;
  }} catch (prefsErr) {{}}
  try {{
    preset = app.pdfExportPresets.itemByName("[High Quality Print]");
    preset.name;
  }} catch (e) {{
    preset = app.pdfExportPresets.item(0);
  }}
  doc.exportFile(ExportFormat.PDF_TYPE, pdfFile, false, preset);
  return "print";
}}

function writeBuildReport(doc) {{
  var reportFile = File(OUTPUT_REPORT);
  if (!reportFile.parent.exists) reportFile.parent.create();
  var report = {{
    document: "The Anatomy of Looking",
    generatedAt: new Date().toString(),
    pageCount: doc.pages.length,
    facingPages: doc.documentPreferences.facingPages,
    trim: "A4 portrait 210mm x 297mm",
    bleed: "3mm all sides",
    columns: 12,
    assetCount: ASSETS.length,
    linkCount: doc.links.length,
    missingLinks: countMissingLinks(doc),
    hyperlinkCount: doc.hyperlinks.length,
    tocStyles: doc.tocStyles.length,
    tocBookmarks: doc.bookmarks.length,
    tocHyperlinks: doc.hyperlinks.length,
    preflightProfile: doc.preflightOptions.preflightWorkingProfile,
    intentionalColorLandscape: true,
    pdfExportMode: doc.extractLabel("pdfExportMode"),
    textFrameCount: doc.textFrames.length,
    oversetTextFrames: countOversetFrames(doc),
    moodyLayoutRules: [
      "dark ink and archival cream base",
      "muted gold and slate accents",
      "large image fields",
      "overlap captions",
      "broken text flow",
      "full-bleed pressure pages",
      "solid paper caption panels"
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
  var label = "A controlled glimpse becomes part of the argument.";
  colorPanel(page, bounds, cream, 98);
  var tf = textFrame(page, bounds, label, 6.2, "Bold", ink, 100);
  return tf;
}}

function nativeTocSource(page, title, sourceStyle) {{
  var source = page.textFrames.add();
  source.geometricBounds = pageBounds(page, b(2, 2, 8, 70));
  source.contents = title;
  source.paragraphs.item(0).appliedParagraphStyle = sourceStyle;
  source.nonprinting = true;
  return source;
}}

function nativeAdobeToc(doc, ink, gold) {{
  var sourceStyle = doc.paragraphStyles.add({{name: "TOC Source Heading"}});
  var entryStyle = doc.paragraphStyles.add({{name: "TOC Entry"}});
  var titleStyle = doc.paragraphStyles.add({{name: "TOC Title"}});
  try {{
    entryStyle.pointSize = 11;
    entryStyle.leading = 16;
    entryStyle.spaceAfter = 10;
    entryStyle.fillColor = ink;
    entryStyle.tabStops.add({{position: "150mm", alignment: TabStopAlignment.RIGHT_ALIGN}});
    titleStyle.pointSize = 24;
    titleStyle.leading = 29;
    titleStyle.spaceAfter = 18;
    titleStyle.fillColor = ink;
  }} catch (styleErr) {{}}

  nativeTocSource(doc.pages.item(4), "Opening Thesis", sourceStyle);
  nativeTocSource(doc.pages.item(7), "The Body", sourceStyle);
  nativeTocSource(doc.pages.item(16), "The Rule", sourceStyle);
  nativeTocSource(doc.pages.item(26), "The Veil", sourceStyle);
  nativeTocSource(doc.pages.item(38), "Synthesis", sourceStyle);
  nativeTocSource(doc.pages.item(47), "Sources", sourceStyle);

  var tocStyle = doc.tocStyles.add({{
    name: "Magazine Contents",
    title: "CONTENTS",
    titleStyle: titleStyle,
    createBookmarks: true,
    makeAnchor: true
  }});
  tocStyle.tocStyleEntries.add(sourceStyle.name, {{
    formatStyle: entryStyle,
    pageNumberPosition: PageNumberPosition.AFTER_ENTRY,
    separator: "\\t"
  }});

  app.activeWindow.activePage = doc.pages.item(3);
  doc.createTOC(tocStyle, false, undefined, ["24mm", "28mm"], false, doc.activeLayer);
  var tocFrame = doc.pages.item(3).textFrames.lastItem();
  tocFrame.geometricBounds = pageBounds(doc.pages.item(3), b(34, 24, 242, 188));
  try {{
    tocFrame.textFramePreferences.insetSpacing = ["2mm", "2mm", "2mm", "2mm"];
    tocFrame.textFramePreferences.verticalJustification = VerticalJustification.TOP_ALIGN;
  }} catch (frameErr) {{}}
  fitText(tocFrame, 8);
}}

function pageNum(page, n, ink) {{
  textFrame(page, b(282, 184, 289, 202), ("0" + n).slice(-2), 6.5, "Regular", ink, 100);
}}

function saveDesktopFiles(doc) {{
  var inddFile = File(OUTPUT_INDD);
  var idmlFile = File(OUTPUT_IDML);
  if (!inddFile.parent.exists) inddFile.parent.create();
  doc.save(inddFile);
  doc.exportFile(ExportFormat.INDESIGN_MARKUP, idmlFile);
  doc.insertLabel("pdfExportMode", exportPdf(doc));
  writeBuildReport(doc);
}}

function cover(page, doc, ink, cream, gold) {{
  var item = assetById("A58");
  colorPanel(page, b(0, 0, 297, 210), ink, 100);
  imageFrame(page, b(30, 24, 232, 186), item, 100);
  colorPanel(page, b(236, 24, 286, 186), cream, 100);
  textFrame(page, b(240, 28, 269, 182), "THE ANATOMY\\rOF LOOKING", 24, "Bold", ink, 100);
  textFrame(page, b(270, 62, 282, 148), "women, attention, and the psychology of sight", 8, "Regular", ink, 100);
}}

function frontMatter(page, n, doc, ink, cream, gold) {{
  if (n === 2) {{
    textFrame(page, b(62, 24, 118, 170), "The Anatomy\\rof Looking", 30, "Bold", ink, 100);
    textFrame(page, b(126, 26, 152, 160), "A 50-page visual psychology issue on attention, image memory, and human sight.", 10, "Regular", ink, 100);
    textFrame(page, b(245, 24, 272, 160), "Issue dossier: psychology of sight, image memory, Symbolism, Surrealist interruption, and the human habit of reading faces before words.", 7, "Regular", ink, 100);
  }} else if (n === 3) {{
    textFrame(page, b(216, 24, 271, 182), "CREDITS / RIGHTS NOTE\\rImages are credited in the source register at the back. Adobe Stock, Unsplash, archive, and local image files require final rights confirmation before publication.", 8, "Regular", ink, 100);
  }} else {{}}
}}

function introPage(page, n, doc, ink, cream, gold) {{
  imageFrame(page, b(32, 24, 132, 84), groupAsset("Mediation", n), 100);
  imageFrame(page, b(88, 98, 178, 186), groupAsset("Constraint", n), 100);
  imageFrame(page, b(154, 44, 238, 132), groupAsset("Agency", n), 85);
  colorPanel(page, b(188, 18, 252, 156), cream, 88);
  textFrame(page, b(196, 26, 224, 148), "The Anatomy of Looking", 21, "Bold", ink, 100);
  textFrame(page, b(226, 27, 258, 160), COPY.intro, 8.6, "Regular", ink, 100);
  caption(page, b(124, 72, 145, 134), groupAsset("Mediation", n), ink, cream);
}}

function articlePage(page, n, section, item, doc, ink, cream, gold, slate) {{
  var mode = n % 6;
  var accent = section === "MEDIATION" ? slate : gold;
  if (mode === 0) {{
    imageFrame(page, b(24, 14, 216, 142), item, 100);
    colorPanel(page, b(144, 122, 205, 194), cream, 96);
    textFrame(page, b(152, 130, 176, 188), section, 18, "Bold", ink, 100);
    textFrame(page, b(176, 130, 204, 188), copyChunk(section.toLowerCase(), n), 7.8, "Regular", ink, 100);
    caption(page, b(196, 24, 216, 92), item, ink, cream);
  }} else if (mode === 1) {{
    imageFrame(page, b(42, 68, 210, 196), item, 100);
    colorPanel(page, b(18, 22, 240, 58), cream, 98);
    textFrame(page, b(44, 28, 198, 52), section, 18, "Bold", ink, 100);
    colorPanel(page, b(150, 46, 204, 176), cream, 96);
    textFrame(page, b(156, 52, 198, 168), copyChunk(section.toLowerCase(), n), 7.2, "Regular", ink, 100);
  }} else if (mode === 2) {{
    imageFrame(page, b(0, 0, 297, 210), item, 100);
    colorPanel(page, b(78, 0, 116, 210), cream, 98);
    textFrame(page, b(82, 26, 112, 182), "ONLY ONE EYE REMAINS, THE IMAGE GETS LOUDER.", 18, "Bold", ink, 100);
    colorPanel(page, b(212, 18, 278, 100), cream, 98);
    textFrame(page, b(218, 24, 272, 94), copyChunk(section.toLowerCase(), n), 7.2, "Regular", ink, 100);
  }} else if (mode === 3) {{
    imageFrame(page, b(34, 20, 120, 102), item, 100);
    imageFrame(page, b(112, 92, 250, 182), item, 92);
    textFrame(page, b(124, 28, 164, 128), "A body becomes legible through pressure.", 13, "Bold", ink, 100);
    textFrame(page, b(166, 28, 210, 118), copyChunk(section.toLowerCase(), n), 7.6, "Regular", ink, 100);
    caption(page, b(106, 78, 127, 148), item, ink, cream);
  }} else if (mode === 4) {{
    imageFrame(page, b(42, 30, 226, 180), item, 100);
    colorPanel(page, b(26, 158, 196, 206), cream, 98);
    textFrame(page, b(36, 164, 138, 200), "THE VEIL DOES NOT DISAPPEAR THE BODY.", 14, "Bold", ink, 100);
    colorPanel(page, b(68, 24, 132, 104), cream, 96);
    textFrame(page, b(74, 30, 126, 98), copyChunk(section.toLowerCase(), n), 7.0, "Regular", ink, 100);
  }} else {{
    imageFrame(page, b(22, 44, 266, 178), item, 100);
    colorPanel(page, b(26, 28, 58, 128), cream, 94);
    textFrame(page, b(30, 34, 54, 122), "LOOKING IS EDITED BY ACCESS.", 12, "Bold", ink, 100);
    caption(page, b(240, 120, 264, 190), item, ink, cream);
  }}
}}

function backMatter(page, n, doc, ink, cream, gold) {{
  if (n === 50) {{
    textFrame(page, b(60, 24, 108, 172), "Sight remains\\runfinished.", 28, "Bold", ink, 100);
    textFrame(page, b(226, 24, 258, 172), "Every act of looking leaves a remainder: memory, attention, and the human need to interpret what the eye cannot settle.", 8, "Regular", ink, 100);
  }} else {{
    var head = n === 46 ? "IMAGE CREDITS" : n === 47 ? "IMAGE CREDITS CONTINUED" : n === 48 ? "SOURCE LIST" : "REFERENCES";
    textFrame(page, b(28, 24, 48, 172), head, 16, "Bold", ink, 100);
    var body = "Images are credited in the register, and rights remain to be confirmed before publication. The issue follows agency, constraint, and mediation as three linked pressures in the psychology of sight.";
    textFrame(page, b(64, 24, 246, 172), body, 8.5, "Regular", ink, 100);
  }}
}}

var doc = setupDoc();
configurePublicationPreflight(doc);
var ink = addSwatch(doc, "Ink", [17, 16, 14]);
var cream = addSwatch(doc, "Archival Cream", [243, 235, 221]);
var gold = addSwatch(doc, "Muted Gold", [165, 130, 66]);
var slate = addSwatch(doc, "Slate Blue", [82, 107, 122]);

for (var p = 0; p < doc.pages.length; p++) {{
  var page = doc.pages[p];
  var n = p + 1;
  colorPanel(page, b(0, 0, 297, 210), cream, 100);
  if (n === 1) cover(page, doc, ink, cream, gold);
  else if (n <= 4) frontMatter(page, n, doc, ink, cream, gold);
  else if (n <= 7) introPage(page, n, doc, ink, cream, gold);
  else if (n <= 16) articlePage(page, n, "AGENCY", groupAsset("Agency", n), doc, ink, cream, gold, slate);
  else if (n <= 26) articlePage(page, n, "CONSTRAINT", groupAsset("Constraint", n), doc, ink, cream, gold, slate);
  else if (n <= 38) articlePage(page, n, "MEDIATION", groupAsset("Mediation", n), doc, ink, cream, gold, slate);
  else if (n <= 45) articlePage(page, n, "SYNTHESIS", asset(n), doc, ink, cream, gold, slate);
  else backMatter(page, n, doc, ink, cream, gold);
  if (n !== 4) pageNum(page, n, ink);
}}

nativeAdobeToc(doc, ink, gold);

// Final overset guard.
for (var i = 0; i < doc.textFrames.length; i++) {{
  if (doc.textFrames[i].overflows) fitText(doc.textFrames[i], 6.5);
}}

saveDesktopFiles(doc);
"""
    (TEMPLATE_OUT / "indesign-build-full-layout.jsx").write_text(jsx, encoding="utf-8")


def generate_cover(assets: list[Asset]) -> None:
    cover = PDF_OUT / "cover-design.pdf"
    c = canvas.Canvas(str(cover), pagesize=(PAGE_W, PAGE_H))
    preferred = next((a for a in assets if "white lace blindfold" in a.filename.lower()), assets[0])
    draw_cover(c, preferred)
    c.showPage()
    c.save()
    apply_print_boxes(cover)


def generate_book(assets: list[Asset]) -> None:
    book = PDF_OUT / "the-visceral-theory-of-sight-50pp.pdf"
    c = canvas.Canvas(str(book), pagesize=(PAGE_W, PAGE_H))
    cover_asset = next((a for a in assets if "white lace blindfold" in a.filename.lower()), assets[0])
    draw_cover(c, cover_asset, page_num=1)
    c.showPage()
    draw_title_page(c)
    c.showPage()
    draw_legal(c)
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
    for offset, page in enumerate(range(8, 17)):
        draw_article_page(c, page, "Agency", agency_assets[offset % len(agency_assets)], offset % 6)
        c.showPage()
    for offset, page in enumerate(range(17, 27)):
        draw_article_page(c, page, "Constraint", constraint_assets[offset % len(constraint_assets)], offset % 6)
        c.showPage()
    for offset, page in enumerate(range(27, 39)):
        draw_article_page(c, page, "Mediation", med_assets[offset % len(med_assets)], offset % 6)
        c.showPage()
    for offset, page in enumerate(range(39, 46)):
        draw_synthesis(c, page, page_assets[(offset + 18) % len(page_assets)], offset % 5)
        c.showPage()
    for page in range(46, 51):
        draw_back_matter(c, page, assets)
        c.showPage()
    c.save()
    apply_print_boxes(book)


def write_manifest(assets: list[Asset]) -> None:
    manifest = {
        "title": "The Anatomy of Looking",
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
