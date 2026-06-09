"""Generate an InDesign JSX that auto-fixes the preflight errors reported for
visceral_theory_of_sight_precision_layout.indd.

Preflight profile: Digital Publishing
Total errors: 347 (COLOR 130, TEXT 215, DOCUMENT 2)

Error categories fixed
----------------------
COLOR (130 items)
  SCRIPTABLE (~40 items):
  - CMY / RGB strokes on lines/shapes → [Black]
  - CMY / RGB fills on rectangles    → [Black] or [Paper]
  - Image-frame strokes              → removed (strokeWeight = 0)
  - All story text fill colors       → [Black]

  NOT SCRIPTABLE (~90 items — placed image content):
  - Files like 1.png, AdobeStock_*.jpeg contain RGB/CMY pixel data.
    InDesign cannot recolor placed image content via script.
    Fix: use K-only grayscale copies (see indesign-build-preflight-safe.jsx).

TEXT (215 items)
  - Overset text repaired via three passes:
      A. Height-only auto-sizing (handles systematic 2-char / 21-char oversets)
      B. Frame expansion to page safe area
      C. Progressive type-size reduction (floor 5.5 pt)
  NOTE: The page size change (A4 portrait → US Letter landscape) makes the
  page ~81 mm shorter, so frames built for A4 will overflow until auto-sized.

DOCUMENT (2 items)
  - Page size: 210 mm × 297 mm (A4 portrait) → 279.4 mm × 215.9 mm (US Letter landscape)
  - Bleed:     3 mm all sides                → 3.175 mm all sides

Output
------
The JSX is written to:
  visceral-production-route/templates/indesign-preflight-autofix-current-doc.jsx

Run the JSX inside InDesign:
  File > Scripts > Other Script… → select the output file
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_OUT = ROOT / "visceral-production-route" / "templates"
REPORTS_OUT   = ROOT / "visceral-production-route" / "reports"
JSX_OUT       = TEMPLATES_OUT / "indesign-preflight-autofix-current-doc.jsx"
REPORT_OUT    = REPORTS_OUT   / "preflight-autofix-generator-report.json"

# Target values (Digital Publishing profile requirements)
PAGE_W_MM = 279.4
PAGE_H_MM = 215.9
BLEED_MM  = 3.175

# Paper-like color name keywords → map to [Paper]
PAPER_KEYWORDS = ("paper", "cream", "white", "mist", "unbleach", "ivory")


def build_jsx() -> str:
    paper_test = " ||\n".join(
        f'        n.indexOf("{kw}") >= 0'
        for kw in PAPER_KEYWORDS
    )
    return f"""\
// visceral_theory_of_sight_precision_layout.indd — preflight autofix
// Profile: Digital Publishing  |  Total errors targeted: 347
//
// Fixes applied by this script:
//   (1) Page size  → US Letter landscape  {PAGE_W_MM} mm × {PAGE_H_MM} mm
//   (2) Bleed      → {BLEED_MM} mm on all four sides
//   (3) CMY / RGB fills & strokes on shapes/lines → [Black] or [Paper]
//   (4) Image-frame strokes                       → strokeWeight = 0
//   (5) All story text fill colors                → [Black]
//   (6) Overset text: auto-size ▸ frame-expand ▸ type-reduction (floor 5.5 pt)
//
// NOT fixed by this script (requires K-only source images):
//   Placed image content CMY errors (1.png, AdobeStock_*.jpeg, etc.)
//   → Use indesign-build-preflight-safe.jsx for a fully compliant rebuild.
//
// Usage: In InDesign open the .indd, then run
//        File > Scripts > Other Script … → pick this file.
//
// ─────────────────────────────────────────────────────────────────────────────

#target indesign

if (app.documents.length === 0) {{
  alert(
    "No document is open.\\n" +
    "Open visceral_theory_of_sight_precision_layout.indd first, " +
    "then run this script again."
  );
}} else {{

  app.scriptPreferences.userInteractionLevel =
    UserInteractionLevels.INTERACT_WITH_ERRORS_ONLY;

  try {{

    var doc  = app.activeDocument;
    var log  = [];
    var nFill   = 0;
    var nStroke = 0;
    var nText   = 0;
    var nFixed  = 0;
    var nLeft   = 0;

    // ── 1. Document preferences: page size + bleed ───────────────────────────
    doc.documentPreferences.pageWidth  = "{PAGE_W_MM}mm";
    doc.documentPreferences.pageHeight = "{PAGE_H_MM}mm";
    doc.documentPreferences.documentBleedTopOffset             = "{BLEED_MM}mm";
    doc.documentPreferences.documentBleedBottomOffset          = "{BLEED_MM}mm";
    doc.documentPreferences.documentBleedInsideOrLeftOffset    = "{BLEED_MM}mm";
    doc.documentPreferences.documentBleedOutsideOrRightOffset  = "{BLEED_MM}mm";
    log.push("Page size  → {PAGE_W_MM} mm × {PAGE_H_MM} mm  (US Letter landscape)");
    log.push("Bleed      → {BLEED_MM} mm all sides");

    // ── 2. Swatch helpers ────────────────────────────────────────────────────
    function getSwatch(name) {{
      var s;
      try {{ s = doc.swatches.itemByName(name); if (s && s.isValid) return s; }}
      catch (e) {{}}
      try {{ s = doc.swatches.item(name);       if (s && s.isValid) return s; }}
      catch (e) {{}}
      return null;
    }}

    var swBlack = getSwatch("[Black]");
    var swPaper = getSwatch("[Paper]");
    var swNone  = getSwatch("[None]");

    function isPaperLike(swatch) {{
      if (!swatch || !swatch.isValid) return false;
      var n = swatch.name.toLowerCase();
      return (
        {paper_test}
      );
    }}

    function isSafe(swatch) {{
      if (!swatch || !swatch.isValid) return true;
      var n = swatch.name;
      return (
        n === "[Black]"        ||
        n === "[None]"         ||
        n === "[Paper]"        ||
        n === "[Registration]"
      );
    }}

    function safeTarget(swatch) {{
      return isPaperLike(swatch) ? swPaper : swBlack;
    }}

    // ── 3. Fix fills and strokes on one page item ────────────────────────────
    function hasPlacedImage(item) {{
      try {{ return item.images && item.images.length > 0; }}
      catch (e) {{ return false; }}
    }}

    function fixItem(item) {{
      try {{
        var fc = item.fillColor;
        if (fc && fc.isValid && !isSafe(fc)) {{
          item.fillColor = safeTarget(fc);
          nFill++;
        }}
      }} catch (e) {{}}

      try {{
        var sw = item.strokeWeight;
        var sc = item.strokeColor;
        if (sc && sc.isValid && !isSafe(sc) && sw > 0) {{
          if (hasPlacedImage(item)) {{
            item.strokeWeight = 0;
          }} else {{
            item.strokeColor = swBlack;
          }}
          nStroke++;
        }}
      }} catch (e) {{}}
    }}

    // ── 4. Fix text fill colors in a story ───────────────────────────────────
    function fixStoryColors(story) {{
      try {{
        var chars = story.characters;
        for (var c = 0; c < chars.length; c++) {{
          try {{
            var fc = chars[c].fillColor;
            if (fc && fc.isValid && !isSafe(fc)) {{
              chars[c].fillColor = swBlack;
              nText++;
            }}
          }} catch (e) {{}}
        }}
      }} catch (e) {{}}
    }}

    // ── 5. Process all page items ────────────────────────────────────────────
    function processItems(items) {{
      for (var i = 0; i < items.length; i++) {{
        try {{ fixItem(items[i]); }} catch (e) {{}}
      }}
    }}

    for (var p = 0; p < doc.pages.length; p++) {{
      try {{ processItems(doc.pages[p].allPageItems); }} catch (e) {{}}
    }}

    for (var ms = 0; ms < doc.masterSpreads.length; ms++) {{
      var mSpread = doc.masterSpreads[ms];
      for (var mp = 0; mp < mSpread.pages.length; mp++) {{
        try {{ processItems(mSpread.pages[mp].allPageItems); }} catch (e) {{}}
      }}
    }}

    for (var s = 0; s < doc.stories.length; s++) {{
      try {{ fixStoryColors(doc.stories[s]); }} catch (e) {{}}
    }}

    log.push("Fill colors corrected:    " + nFill);
    log.push("Stroke colors corrected:  " + nStroke);
    log.push("Text fills corrected:     " + nText);

    // ── 6. Overset text — three-pass repair ──────────────────────────────────
    function repairOverset(tf) {{

      // Pass A — height-only auto-sizing (fixes systematic 2-char / 21-char oversets)
      try {{
        var prefs = tf.textFramePreferences;
        prefs.autoSizingType           = AutoSizingTypeEnum.HEIGHT_ONLY;
        prefs.autoSizingReferencePoint = AutoSizingReferenceEnum.TOP_LEFT_POINT;
        prefs.useMinimumHeightForAutoSizing = true;
        prefs.minimumHeightForAutoSizing    = 4;
      }} catch (e) {{}}
      if (!tf.overflows) {{ nFixed++; return; }}

      // Pass B — expand frame down to page safe area
      try {{
        var pg = tf.parentPage;
        if (pg) {{
          var gb = tf.geometricBounds.slice();
          var pb = pg.bounds;
          var mp = pg.marginPreferences;
          var safeBottom = pb[2] - mp.bottom;
          if (gb[2] < safeBottom) {{
            gb[2] = safeBottom;
            tf.geometricBounds = gb;
          }}
        }}
      }} catch (e) {{}}
      if (!tf.overflows) {{ nFixed++; return; }}

      // Pass B2 — expand to full page bleed bottom (last resort before font reduction)
      try {{
        var pg2 = tf.parentPage;
        if (pg2) {{
          var gb2 = tf.geometricBounds.slice();
          var pb2 = pg2.bounds;
          if (gb2[2] < pb2[2]) {{
            gb2[2] = pb2[2];
            tf.geometricBounds = gb2;
          }}
        }}
      }} catch (e) {{}}
      if (!tf.overflows) {{ nFixed++; return; }}

      // Pass C — reduce point size (floor 5.5 pt, 0.35 pt steps, max 40 iterations)
      var guard = 0;
      while (tf.overflows && guard < 40) {{
        try {{
          var sz = Number(tf.parentStory.texts[0].pointSize);
          if (isNaN(sz) || sz <= 5.5) break;
          var ns = Math.max(5.5, sz - 0.35);
          tf.parentStory.texts[0].pointSize = ns;
          tf.parentStory.texts[0].leading   = ns * 1.20;
        }} catch (e) {{ break; }}
        guard++;
      }}

      if (!tf.overflows) nFixed++;
      else nLeft++;
    }}

    for (var t = 0; t < doc.textFrames.length; t++) {{
      try {{
        var tf = doc.textFrames[t];
        if (tf.isValid && tf.overflows) repairOverset(tf);
      }} catch (e) {{}}
    }}

    log.push("Overset frames repaired:  " + nFixed);
    if (nLeft > 0) {{
      log.push("Still overset (manual):   " + nLeft +
               "  (thread text or cut copy to fix)");
    }}

    // ── 7. Save ──────────────────────────────────────────────────────────────
    doc.save();
    log.push("Document saved.");

    var imageNote = (
      "\\n\\nNOTE: Placed image CMY errors (*.png, *.jpeg) cannot be fixed\\n" +
      "by script — they require K-only grayscale source files.\\n" +
      "Run indesign-build-preflight-safe.jsx for a fully clean build."
    );
    alert("Preflight autofix complete.\\n\\n" + log.join("\\n") + imageNote);

  }} catch (mainErr) {{
    alert(
      "Autofix error on line " + mainErr.line + ":\\n" +
      mainErr.message
    );
  }}

}}
"""


def main() -> None:
    TEMPLATES_OUT.mkdir(parents=True, exist_ok=True)
    REPORTS_OUT.mkdir(parents=True, exist_ok=True)

    jsx = build_jsx()
    JSX_OUT.write_text(jsx, encoding="utf-8")
    print(f"JSX written:    {JSX_OUT}")

    # Counts from current preflight report
    color_count          = 130
    color_scriptable     = 40   # strokes, fills, text — fixable by script
    color_image_content  = 90   # placed image CMY — requires K-only source files
    overset_count        = 215
    doc_count            = 2
    total                = color_count + overset_count + doc_count

    report = {
        "script": str(JSX_OUT),
        "target_document": "visceral_theory_of_sight_precision_layout.indd",
        "preflight_profile": "Digital Publishing",
        "preflight_error_counts": {
            "color_total": color_count,
            "color_scriptable_fixes": color_scriptable,
            "color_image_content_not_scriptable": color_image_content,
            "overset_text": overset_count,
            "document_setup": doc_count,
            "grand_total": total,
        },
        "fixes": {
            "page_size": {
                "from": "210 mm × 297 mm  (A4 portrait)",
                "to":   f"{PAGE_W_MM} mm × {PAGE_H_MM} mm  (US Letter landscape)",
            },
            "bleed": {
                "from": "3 mm all sides",
                "to":   f"{BLEED_MM} mm all sides",
            },
        },
        "color_strategy": {
            "paper_like_fills": "→ [Paper]  (matches: "
            + ", ".join(PAPER_KEYWORDS) + ")",
            "all_other_non_black": "→ [Black]",
            "image_frame_strokes": "→ strokeWeight = 0  (removed)",
            "story_text": "→ [Black]",
            "placed_image_content": "NOT FIXABLE by script — requires K-only grayscale source files",
        },
        "overset_strategy": {
            "pass_a": "AutoSizingType = HEIGHT_ONLY, minimumHeight 4pt (handles systematic 2-char/21-char oversets)",
            "pass_b": "Expand frame bottom to page safe area",
            "pass_b2": "Expand frame to full page bottom (last resort)",
            "pass_c": "Reduce point size 0.35 pt per iteration, floor 5.5 pt, max 40 iterations",
        },
        "limitations": [
            "Placed image CMY content (*.png, *.jpeg) cannot be recolored by script",
            "For fully preflight-clean output use indesign-build-preflight-safe.jsx (K-only images)",
            "Threaded text frames may still show overset if thread partner also needs resizing",
        ],
        "usage": (
            "In InDesign: File > Scripts > Other Script… "
            "→ select indesign-preflight-autofix-current-doc.jsx"
        ),
    }
    REPORT_OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Report written: {REPORT_OUT}")


if __name__ == "__main__":
    main()
