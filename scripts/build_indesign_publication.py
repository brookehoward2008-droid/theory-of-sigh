#!/usr/bin/env python3
"""
Generate a production InDesign build script for *The Visceral Theory of Sight*.

This emits an ExtendScript (.jsx) that builds the 51-page publication the
proper, production way:

  - US Letter landscape, facing pages, 3.175 mm bleed
  - CMYK process swatches
  - a complete PARAGRAPH + CHARACTER STYLE system (named "VT / ...") so every
    text element is style-driven and globally editable
  - a master spread (rich-black ground + automatic folio)
  - the 51-page structure with images placed and the real copy flowed into
    style-tagged frames (article bodies thread across each section's pages)
  - a preflight pass, then IDML + print-PDF export

It does NOT require InDesign to GENERATE (pure text emission). You run the
emitted .jsx inside InDesign (File ▸ Scripts ▸ Other Script…), then
File ▸ Package for the printer hand-off.

The font choice is parameterised in FONTS below — change one line to swap the
body face once it is locked. Fonts must be installed/Adobe-activated in
InDesign under the family/style names given here.

Usage:
  python scripts/build_indesign_publication.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_visceral_book as vb  # noqa: E402

OUT_JSX = ROOT / "visceral-production-route" / "templates" / "indesign-publication-build.jsx"

# --- Fonts (EDIT to your locked choice) --------------------------------------
# Each role -> (InDesign family, style). The body face is the open question;
# swap "Spectral" for "Fraunces" / "Lora" / "Outfit" / an Adobe Font, etc.
FONTS = {
    "display": ("Gloock", "Regular"),         # section titles, epigraph title, closing
    "body": ("Spectral", "Regular"),          # article + reading text
    "body_italic": ("Spectral", "Italic"),    # emphasis / verse option
    "sans": ("Work Sans", "Regular"),         # captions, folios
    "sans_bold": ("Work Sans", "Bold"),       # eyebrows / labels / attribution
}

# --- Palette as CMYK process swatches (approximate; printer may fine-tune) ----
SWATCHES = {
    "VT Rich Black": (60, 50, 50, 100),   # full-bleed ground
    "VT Cream": (4, 5, 13, 0),            # primary text
    "VT Gold": (30, 45, 85, 12),          # accents, eyebrows
    "VT Slate": (68, 48, 40, 18),         # cool accent
    "VT Teal": (72, 22, 46, 4),           # accent
}

# --- Paragraph styles ---------------------------------------------------------
# keys: font(role), size, leading, track(1/1000 em), color(swatch),
#       align(LEFT_ALIGN/CENTER_ALIGN/RIGHT_ALIGN/LEFT_JUSTIFIED), caps(bool),
#       before, after, indent
PARA_STYLES = [
    ("VT / Body",            dict(font="body", size=10.4, leading=14.5, track=10, color="VT Cream", align="LEFT_ALIGN", after=6)),
    ("VT / Body Lead",       dict(font="body", size=10.4, leading=14.5, track=10, color="VT Cream", align="LEFT_ALIGN", after=6)),
    ("VT / Section Number",  dict(font="sans_bold", size=12, leading=14, track=120, color="VT Gold", caps=True)),
    ("VT / Section Title",   dict(font="display", size=64, leading=58, track=-10, color="VT Cream")),
    ("VT / Section Blurb",   dict(font="body", size=11, leading=15.5, track=10, color="VT Cream", after=0)),
    ("VT / Eyebrow",         dict(font="sans_bold", size=8, leading=10, track=90, color="VT Gold", caps=True)),
    ("VT / Caption",         dict(font="sans", size=7, leading=9.5, track=10, color="VT Cream")),
    ("VT / Folio",           dict(font="sans", size=7.5, leading=9, track=40, color="VT Cream")),
    ("VT / Epigraph Title",  dict(font="display", size=46, leading=46, color="VT Cream")),
    ("VT / Epigraph Credit", dict(font="sans_bold", size=13, leading=16, track=60, color="VT Gold", caps=True)),
    ("VT / Epigraph Verse",  dict(font="body", size=16, leading=24, track=12, color="VT Cream")),
    ("VT / Epigraph Reply",  dict(font="body", size=12, leading=16.5, track=8, color="VT Cream")),
    ("VT / Intro Headline",  dict(font="display", size=30, leading=30, color="VT Cream")),
    ("VT / Pull Quote",      dict(font="display", size=22, leading=24, color="VT Cream")),
    ("VT / Title",           dict(font="display", size=54, leading=50, color="VT Cream")),
    ("VT / Subtitle",        dict(font="sans_bold", size=11, leading=15, track=80, color="VT Gold", caps=True)),
    ("VT / TOC Header",      dict(font="display", size=34, leading=36, color="VT Cream")),
    ("VT / TOC Entry",       dict(font="body", size=13, leading=22, color="VT Cream")),
    ("VT / Colophon",        dict(font="body", size=10, leading=14, track=10, color="VT Cream")),
    ("VT / Source Entry",    dict(font="sans", size=8, leading=11.5, track=10, color="VT Cream")),
    ("VT / Works Consulted", dict(font="body", size=10, leading=14.5, track=10, color="VT Cream", after=6)),
    ("VT / Closing",         dict(font="display", size=40, leading=42, color="VT Cream")),
]

# --- Character styles ---------------------------------------------------------
CHAR_STYLES = [
    ("VT / Italic",        dict(font="body_italic")),
    ("VT / Caption Label", dict(font="sans_bold", color="VT Gold")),
    ("VT / TOC Folio",     dict(font="sans_bold", color="VT Gold")),
    ("VT / Accent Gold",   dict(color="VT Gold")),
    ("VT / Accent Teal",   dict(color="VT Teal")),
]

# Epigraph poem (Hannah Flagg Gould, "Thoughts" — public domain).
POEM_Q = (
    "Eyes, say, why were ye given your sight,\r"
    "Your full blue orbs, with their roll and their light,\r"
    "Which your lids of the lily with violet tinge\r"
    "So often of late, with their long, dark fringe\r"
    "From their folds in your arches descended to shade?\r"
    "Ye have told many things—but not why ye were made."
)
POEM_A = (
    "“We were made to delight in the beauties of earth;\r"
    "Then to see how they perished, how little their worth\r"
    "They are changing, illusive, uncertain and brief,\r"
    "From the flower’s opening bud to its soon withered leaf.\r"
    "The birth of their being is joined to decay;\r"
    "They flourish, allure, and expire in a day.\r"
    "On things like ourselves with delight we have shone;\r"
    "We have studied their language and found it our own;\r"
    "But the offspring of grief would extinguish their light,\r"
    "And the spoiler’s pale hand lock them up from our sight.\r"
    "Or, keener, far keener, they’d let us behold\r"
    "Their looks turning from us, unfeeling and cold,\r"
    "Bequeathing this line, as we saw them depart,\r"
    "‘We go not alone, but are drawn by the heart!’\r"
    "For things such as these, and still more were we made;\r"
    "For watching, for aching, to sink and to fade;\r"
    "To pour forth in silence the waters of sorrow,\r"
    "Then, to close in a night that will bring us no morrow?”"
)


def js(value) -> str:
    """Safe JS literal via JSON (handles quotes/unicode/newlines)."""
    return json.dumps(value, ensure_ascii=True)


def build_model():
    """Pull the real content + image list from the reportlab build."""
    vb.ensure_dirs()
    assets = vb.scan_assets()
    by = {"Agency": [], "Constraint": [], "Mediation": [], "Synthesis": []}
    for a in assets:
        for key in by:
            if key in a.group:
                by[key].append(a)
    # Synthesis has no dedicated group; draw from the full set.
    by["Synthesis"] = assets[:]
    cover = next((a for a in assets if "white lace blindfold" in a.filename.lower()), assets[0])
    return assets, by, cover


def section_block(section, assets_for_section, start_page, n_content):
    """Return JS for a section: opener page + threaded article across content pages."""
    numeral, title, sub = vb.SECTION_TITLES[section]
    blurb = vb.SECTION_BLURB[section]
    body = vb.ARTICLE_BODIES[section]
    imgs = [a.local_path.name for a in assets_for_section] or ["asset-01.jpg"]
    caps = [(a.short_caption or a.caption or "") for a in assets_for_section]
    return {
        "section": section,
        "numeral": numeral,
        "title": title,
        "sub": sub,
        "blurb": blurb,
        "body": body,
        "images": imgs,
        "captions": caps,
        "openerPage": start_page,
        "contentPages": list(range(start_page + 1, start_page + 1 + n_content)),
    }


def main() -> None:
    assets, by, cover = build_model()

    sections = [
        section_block("Agency", by["Agency"], 9, 8),
        section_block("Constraint", by["Constraint"], 18, 9),
        section_block("Mediation", by["Mediation"], 28, 11),
        section_block("Synthesis", by["Synthesis"], 40, 6),
    ]

    # Source register rows for back matter.
    register = [
        {"id": a.id, "title": a.title, "group": a.group,
         "creator": a.creator, "rights": a.rights, "file": a.local_path.name}
        for a in assets
    ]

    works = (
        "McDermott, L. Self-representation in Upper Paleolithic female figurines. / "
        "Havelock, C. M. The Aphrodite of Knidos and her successors. / Reeder, E. D. "
        "Pandora: Women in Classical Greece. / Studies in veiling iconography, the "
        "Vera Icona, lace, and theories of mediation. Editions, page ranges, and "
        "image licenses to be confirmed before final print."
    )
    colophon = (
        "The Visceral Theory of Sight is a visual-psychology issue on gaze, image "
        "memory, and the veil. Photographs are credited in the Image Source Register; "
        "scholarly works are listed under Works Consulted. Printed white on black."
    )

    # Resolve font roles to family strings for the JSX.
    fonts_js = {role: {"family": fam, "style": sty} for role, (fam, sty) in FONTS.items()}

    para_js = []
    for name, spec in PARA_STYLES:
        d = dict(spec)
        family, style = FONTS[d.pop("font")]
        d["font"], d["style"] = family, style
        para_js.append([name, d])
    char_js = []
    for name, spec in CHAR_STYLES:
        d = dict(spec)
        if "font" in d:
            family, style = FONTS[d.pop("font")]
            d["font"], d["style"] = family, style
        char_js.append([name, d])

    jsx = JSX_TEMPLATE.format(
        fonts=js(fonts_js),
        swatches=js(SWATCHES),
        para=js(para_js),
        char=js(char_js),
        cover=js("cover.jpg"),
        title_img=js(by["Mediation"][0].local_path.name if by["Mediation"] else assets[1].local_path.name),
        intro=js(vb.intro_copy()),
        poem_q=js(POEM_Q),
        poem_a=js(POEM_A),
        sections=js(sections),
        register=js(register),
        works=js(works),
        colophon=js(colophon),
        out_indd=js("the-visceral-theory-of-sight-51pp.indd"),
        out_idml=js("the-visceral-theory-of-sight-51pp.idml"),
        out_pdf=js("the-visceral-theory-of-sight-51pp-indesign.pdf"),
    )
    OUT_JSX.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSX.write_text(jsx, encoding="utf-8")
    print(f"Wrote {OUT_JSX}")
    print(f"  {len(PARA_STYLES)} paragraph styles, {len(CHAR_STYLES)} character styles, "
          f"{len(SWATCHES)} swatches, {len(assets)} images, 51 pages")


JSX_TEMPLATE = r"""// The Visceral Theory of Sight — production InDesign build
// Generated by build_indesign_publication.py. Run inside InDesign:
//   File > Scripts > Other Script...  then  File > Package.
// Fonts must be installed / Adobe-activated under the names in FONTS below.
#target "indesign"

(function () {{
    var FONTS = {fonts};
    var SWATCHES = {swatches};
    var PARA = {para};
    var CHAR = {char};
    var SECTIONS = {sections};
    var REGISTER = {register};

    // --- Geometry (points): US Letter landscape, 3.175mm (9pt) bleed ---
    var PW = 792, PH = 612, BL = 9, MG = 45;
    var L = MG, R = PW - MG, T = MG, B = PH - MG;            // content box (top-left origin)
    var assetFolder = (function () {{
        var f = File($.fileName);
        var repo = f.parent.parent.parent;                  // templates -> route -> repo
        return Folder(repo.fsName + "/visceral-production-route/assets");
    }})();
    var coverFolder = (function () {{
        var f = File($.fileName);
        return Folder(f.parent.parent.parent.fsName + "/images");
    }})();
    var outFolder = (function () {{
        var f = File($.fileName);
        var d = Folder(f.parent.parent.fsName + "/output/indesign");
        if (!d.exists) d.create();
        return d;
    }})();

    app.scriptPreferences.measurementUnit = MeasurementUnits.POINTS;
    var prevUI = app.scriptPreferences.userInteractionLevel;
    app.scriptPreferences.userInteractionLevel = UserInteractionLevels.NEVER_INTERACT;

    var doc = app.documents.add();
    with (doc.documentPreferences) {{
        pageSize = "Letter";
        pageWidth = PW; pageHeight = PH;
        pageOrientation = PageOrientation.LANDSCAPE;
        facingPages = true;
        documentBleedTopOffset = BL; documentBleedBottomOffset = BL;
        documentBleedInsideOrLeftOffset = BL; documentBleedOutsideOrRightOffset = BL;
    }}
    doc.viewPreferences.horizontalMeasurementUnits = MeasurementUnits.POINTS;
    doc.viewPreferences.verticalMeasurementUnits = MeasurementUnits.POINTS;

    // --- Swatches (CMYK) ---
    function swatch(name, cmyk) {{
        var s;
        try {{ s = doc.colors.itemByName(name); if (!s.isValid) throw 0; }}
        catch (e) {{
            s = doc.colors.add();
        }}
        s.properties = {{ name: name, model: ColorModel.PROCESS, space: ColorSpace.CMYK, colorValue: cmyk }};
        return s;
    }}
    for (var sw in SWATCHES) if (SWATCHES.hasOwnProperty(sw)) swatch(sw, SWATCHES[sw]);
    function col(name) {{ return doc.swatches.itemByName(name); }}

    // --- Paragraph styles ---
    function applyText(st, p) {{
        st.appliedFont = p.font;
        if (p.style) {{ try {{ st.fontStyle = p.style; }} catch (e) {{}} }}
        if (p.size != null) st.pointSize = p.size;
        if (p.leading != null) st.leading = p.leading;
        if (p.track != null) st.tracking = p.track;
        if (p.color) st.fillColor = col(p.color);
        if (p.align) st.justification = Justification[p.align];
        if (p.caps) st.capitalization = Capitalization.ALL_CAPS;
        if (p.before) st.spaceBefore = p.before;
        if (p.after) st.spaceAfter = p.after;
        if (p.indent) st.firstLineIndent = p.indent;
    }}
    for (var i = 0; i < PARA.length; i++) {{
        var nm = PARA[i][0], pr = PARA[i][1];
        var ps;
        try {{ ps = doc.paragraphStyles.itemByName(nm); if (!ps.isValid) throw 0; }}
        catch (e) {{ ps = doc.paragraphStyles.add({{ name: nm }}); }}
        applyText(ps, pr);
    }}
    for (var j = 0; j < CHAR.length; j++) {{
        var cn = CHAR[j][0], cr = CHAR[j][1];
        var cs;
        try {{ cs = doc.characterStyles.itemByName(cn); if (!cs.isValid) throw 0; }}
        catch (e2) {{ cs = doc.characterStyles.add({{ name: cn }}); }}
        if (cr.font) {{ cs.appliedFont = cr.font; if (cr.style) try {{ cs.fontStyle = cr.style; }} catch (e3) {{}} }}
        if (cr.color) cs.fillColor = col(cr.color);
    }}
    function PS(n) {{ return doc.paragraphStyles.itemByName(n); }}

    // --- Master spread: rich-black ground + auto folio ---
    var master = doc.masterSpreads.item(0);
    for (var mp = 0; mp < master.pages.length; mp++) {{
        var page = master.pages[mp];
        var bg = page.rectangles.add();
        bg.geometricBounds = [-BL, (mp === 0 ? -BL : 0), PH + BL, (mp === 0 ? PW : PW + BL)];
        bg.fillColor = col("VT Rich Black");
        bg.strokeColor = doc.swatches.itemByName("None");
        bg.sendToBack();
        var folio = page.textFrames.add();
        var fx = (mp === 0) ? L : (PW - 90);
        folio.geometricBounds = [PH - 36, fx, PH - 22, fx + 60];
        folio.insertionPoints[0].contents = SpecialCharacters.AUTO_PAGE_NUMBER;
        folio.texts[0].appliedParagraphStyle = PS("VT / Folio");
        folio.texts[0].justification = (mp === 0) ? Justification.LEFT_ALIGN : Justification.RIGHT_ALIGN;
    }}

    // --- Helpers ---
    function ensurePages(n) {{ while (doc.pages.length < n) doc.pages.add(); }}
    function pg(n) {{ return doc.pages[n - 1]; }}              // 1-based
    function frame(page, gb) {{
        var tf = page.textFrames.add();
        tf.geometricBounds = gb;                               // [top,left,bottom,right]
        tf.textFramePreferences.insetSpacing = [0, 0, 0, 0];
        return tf;
    }}
    function styled(page, gb, text, styleName) {{
        var tf = frame(page, gb);
        tf.contents = text;
        tf.parentStory.texts[0].appliedParagraphStyle = PS(styleName);
        return tf;
    }}
    function place(page, gb, fileName, folder) {{
        var rect = page.rectangles.add();
        rect.geometricBounds = gb;
        rect.strokeColor = doc.swatches.itemByName("None");
        var f = File((folder || assetFolder).fsName + "/" + fileName);
        if (f.exists) {{
            rect.place(f);
            try {{ rect.fit(FitOptions.FILL_PROPORTIONALLY); rect.fit(FitOptions.CENTER_CONTENT); }} catch (e) {{}}
        }}
        return rect;
    }}
    function rule(page, x1, y1, x2, y2, colorName, w) {{
        var ln = page.graphicLines.add();
        ln.geometricBounds = [y1, x1, y2, x2];
        ln.strokeColor = col(colorName); ln.strokeWeight = w;
    }}

    ensurePages(51);

    // ============ FRONT MATTER ============
    // p1 cover: full-bleed image + title
    place(pg(1), [-BL, -BL, PH + BL, PW + BL], {cover}, coverFolder);
    styled(pg(1), [PH - 200, L, PH - 96, R], "THE VISCERAL\rTHEORY OF SIGHT", "VT / Title");
    styled(pg(1), [PH - 90, L, PH - 64, R], "The Anatomy of Looking", "VT / Subtitle");

    // p2-3 title spread
    place(pg(2), [-BL, -BL, PH + BL, PW + BL], {title_img}, assetFolder);
    styled(pg(3), [T + 40, L, T + 150, R], "THE VISCERAL\rTHEORY OF SIGHT", "VT / Title");
    styled(pg(3), [T + 160, L, T + 200, R], "A visual-psychology issue on gaze, image memory, and the veil.", "VT / Subtitle");

    // p4 epigraph
    styled(pg(4), [T, L, T + 16, L + 200], "EPIGRAPH", "VT / Eyebrow");
    styled(pg(4), [T + 30, L, T + 150, L + 320], "from\r“Thoughts”", "VT / Epigraph Title");
    styled(pg(4), [T + 150, L, T + 172, L + 320], "HANNAH FLAGG GOULD", "VT / Epigraph Credit");
    rule(pg(4), L, T + 182, L + 180, T + 182, "VT Gold", 1.4);
    styled(pg(4), [T + 200, L, B, L + 330], {poem_q}, "VT / Epigraph Verse");
    rule(pg(4), L + 360, T + 16, L + 360, B - 10, "VT Gold", 0.75);
    styled(pg(4), [T + 16, L + 388, B, R], {poem_a}, "VT / Epigraph Reply");

    // p5 TOC
    styled(pg(5), [T, L, T + 16, L + 200], "CONTENTS", "VT / Eyebrow");
    styled(pg(5), [T + 24, L, T + 80, R], "Agency / Constraint / Mediation / Synthesis", "VT / TOC Header");
    var tocEntries = [
        ["Front Matter", "01"], ["Epigraph: “Thoughts” — Hannah Flagg Gould", "04"],
        ["Introduction: The Visceral Theory of Sight", "06"], ["I. Agency", "09"],
        ["II. Constraint", "18"], ["III. Mediation", "28"], ["IV. Synthesis", "40"],
        ["Back Matter", "47"]
    ];
    var tocText = "";
    for (var t = 0; t < tocEntries.length; t++) tocText += tocEntries[t][0] + "\t" + tocEntries[t][1] + "\r";
    var tocFrame = styled(pg(5), [T + 100, L, B, R], tocText, "VT / TOC Entry");
    // Right-aligned folio with a dotted leader via a right tab stop.
    tocFrame.parentStory.paragraphs.everyItem().tabList =
        [{{ alignment: TabStopAlignment.RIGHT_ALIGN, position: (R - L - 12), leader: "." }}];

    // p6-8 intro
    styled(pg(6), [T, L, T + 16, L + 200], "INTRODUCTION", "VT / Eyebrow");
    styled(pg(6), [T + 24, L, T + 130, L + 360], "The Visceral Theory\rof Sight", "VT / Intro Headline");
    styled(pg(6), [T + 150, L, B, L + 360], {intro}, "VT / Body");
    place(pg(7), [-BL, -BL, PH + BL, PW + BL], "asset-03.jpg", assetFolder);
    styled(pg(7), [T, L, T + 90, R - 120], "The image does not give\ritself all at once.", "VT / Intro Headline");
    styled(pg(8), [T, L, T + 16, L + 240], "THE THREE PRESSURES", "VT / Eyebrow");
    styled(pg(8), [T + 40, L, B, R], {intro}, "VT / Body");

    // ============ SECTIONS ============
    for (var s = 0; s < SECTIONS.length; s++) {{
        var sec = SECTIONS[s];
        // opener: full-bleed image + numeral + title + blurb
        var op = pg(sec.openerPage);
        place(op, [-BL, -BL, PH + BL, PW + BL], sec.images[0], assetFolder);
        var tx = L + 360;
        styled(op, [T, tx, T + 18, R], "ARTICLE " + sec.numeral, "VT / Section Number");
        styled(op, [T + 24, tx, T + 130, R], sec.title, "VT / Section Title");
        styled(op, [T + 140, tx, T + 200, R], sec.blurb, "VT / Section Blurb");

        // content pages: thread the article body through left-column frames, image right
        var prev = null;
        for (var cp = 0; cp < sec.contentPages.length; cp++) {{
            var page = pg(sec.contentPages[cp]);
            // image + body column alternate sides by parity
            var imgName = sec.images[(cp + 1) % sec.images.length];
            var capL = sec.captions[(cp + 1) % sec.captions.length] || "";
            var colBox;
            if (cp % 2 === 0) {{
                place(page, [T, L, B, L + 300], imgName, assetFolder);
                styled(page, [B - 40, L + 8, B - 8, L + 290], sec.title.toUpperCase() + "  —  " + capL, "VT / Caption");
                colBox = [T, L + 330, B, R];
            }} else {{
                place(page, [T, R - 300, B, R], imgName, assetFolder);
                styled(page, [B - 40, R - 292, B - 8, R - 8], sec.title.toUpperCase() + "  —  " + capL, "VT / Caption");
                colBox = [T, L, B, R - 330];
            }}
            var tf = frame(page, colBox);
            tf.parentStory.appliedParagraphStyle = PS("VT / Body");
            if (prev) {{ prev.nextTextFrame = tf; }}
            else {{ tf.contents = sec.body; tf.parentStory.texts[0].appliedParagraphStyle = PS("VT / Body"); }}
            prev = tf;
        }}
    }}

    // ============ BACK MATTER ============
    // p47-48 source register (two pages, styled list)
    function registerText(rows) {{
        var out = "";
        for (var r = 0; r < rows.length; r++) {{
            out += rows[r].id + "  " + rows[r].title + "  —  " + rows[r].creator + "; " + rows[r].rights + "\r";
        }}
        return out;
    }}
    var half = Math.ceil(REGISTER.length / 2);
    styled(pg(47), [T, L, T + 16, L + 240], "IMAGE SOURCE REGISTER", "VT / Eyebrow");
    styled(pg(47), [T + 28, L, B, R], registerText(REGISTER.slice(0, half)), "VT / Source Entry");
    styled(pg(48), [T, L, T + 16, L + 260], "IMAGE SOURCE REGISTER / CONTINUED", "VT / Eyebrow");
    styled(pg(48), [T + 28, L, B, R], registerText(REGISTER.slice(half)), "VT / Source Entry");

    // p49 works consulted
    styled(pg(49), [T, L, T + 16, L + 200], "WORKS CONSULTED", "VT / Eyebrow");
    styled(pg(49), [T + 28, L, B, R], {works}, "VT / Works Consulted");

    // p50 colophon
    styled(pg(50), [T, L, T + 16, L + 160], "COLOPHON", "VT / Eyebrow");
    styled(pg(50), [T + 28, L, B, R], {colophon}, "VT / Colophon");

    // p51 closing
    styled(pg(51), [PH / 2 - 30, L, PH / 2 + 30, R], "Sight remains unfinished.", "VT / Closing");

    // ============ PREFLIGHT + EXPORT ============
    var report = {{ pages: doc.pages.length, missingFonts: [], missingLinks: [], overset: [] }};
    for (var li = 0; li < doc.links.length; li++) if (doc.links[li].status == LinkStatus.LINK_MISSING) report.missingLinks.push(doc.links[li].name);
    for (var fi = 0; fi < doc.fonts.length; fi++) if (doc.fonts[fi].status != FontStatus.INSTALLED) report.missingFonts.push(doc.fonts[fi].name);
    for (var ti = 0; ti < doc.textFrames.length; ti++) if (doc.textFrames[ti].overflows) report.overset.push(ti);

    var inddFile = File(outFolder.fsName + "/" + {out_indd});
    doc.save(inddFile);
    var idmlFile = File(outFolder.fsName + "/" + {out_idml});
    doc.exportFile(ExportFormat.INDESIGN_MARKUP, idmlFile);
    try {{
        var pdfFile = File(outFolder.fsName + "/" + {out_pdf});
        doc.exportFile(ExportFormat.PDF_TYPE, pdfFile, false, app.pdfExportPresets.itemByName("[High Quality Print]"));
    }} catch (e) {{}}

    app.scriptPreferences.userInteractionLevel = prevUI;
    var msg = "Built 51-page publication.\n" +
        "Paragraph styles: " + doc.paragraphStyles.length + "\n" +
        "Missing fonts: " + report.missingFonts.join(", ") + "\n" +
        "Missing links: " + report.missingLinks.length + "\n" +
        "Overset frames: " + report.overset.length + "\n\n" +
        "Next: review, then File > Package for the printer.";
    $.writeln(msg);
}})();
"""


if __name__ == "__main__":
    main()
