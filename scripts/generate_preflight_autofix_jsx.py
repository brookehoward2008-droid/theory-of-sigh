"""Generate an InDesign JSX that auto-fixes the preflight errors reported for
visceral_theory_of_sight_precision_layout.indd.

Preflight profile: Digital Publishing

Error categories fixed
----------------------
COLOR (194 items)
  - All CMY / RGB strokes and fills converted to [Black]
  - Paper-like fills (Cream, Mist, Ivory, Unbleached …) converted to [Paper]
  - Image-frame strokes removed (strokeWeight = 0)
  - All story text fill colors converted to [Black]

TEXT (199 items)
  - Overset text repaired via three passes:
      A. Height-only auto-sizing
      B. Frame expansion to page safe area
      C. Progressive type-size reduction (floor 5.5 pt)

DOCUMENT (2 items)
  - Page size: 210 mm × 297 mm (A4) → 279.4 mm × 215.9 mm (US Letter landscape)
  - Bleed:     3 mm               → 3.175 mm on all sides

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

from scripts.shared.page_constants import US_LETTER_BLEED_MM, US_LETTER_H_MM, US_LETTER_W_MM
from scripts.shared.paths import REPORTS_OUT as _REPORTS_OUT
from scripts.shared.paths import TEMPLATE_OUT as _TEMPLATES_OUT


TEMPLATES_OUT = _TEMPLATES_OUT
REPORTS_OUT   = _REPORTS_OUT
JSX_OUT       = TEMPLATES_OUT / "indesign-preflight-autofix-current-doc.jsx"
REPORT_OUT    = REPORTS_OUT   / "preflight-autofix-generator-report.json"

# Target values (Digital Publishing profile requirements)
PAGE_W_MM = US_LETTER_W_MM
PAGE_H_MM = US_LETTER_H_MM
BLEED_MM  = US_LETTER_BLEED_MM

# Paper-like color name keywords → map to [Paper]
PAPER_KEYWORDS = ("paper", "cream", "white", "mist", "unbleach", "ivory")


def build_jsx() -> str:
    paper_test = " ||\n".join(
        f'        n.indexOf("{kw}") >= 0'
        for kw in PAPER_KEYWORDS
    )
    return f"""\
// visceral_theory_of_sight_precision_layout.indd — full preflight autofix
// Profile: Digital Publishing
//
// Fixes applied by this script:
//   (1) Page size  → US Letter landscape  {PAGE_W_MM} mm × {PAGE_H_MM} mm
//   (2) Bleed      → {BLEED_MM} mm on all four sides
//   (3) All CMY / RGB fills / strokes → [Black] (paper-like colors → [Paper])
//   (4) Image-frame strokes          → removed (strokeWeight = 0)
//   (5) All story text fill colors   → [Black]
//   (6) Overset text: auto-size ▸ frame-expand ▸ type-reduction (floor 5.5 pt)
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

      // Pass A — height-only auto-sizing
      try {{
        var prefs = tf.textFramePreferences;
        prefs.autoSizingType           = AutoSizingTypeEnum.HEIGHT_ONLY;
        prefs.autoSizingReferencePoint = AutoSizingReferenceEnum.TOP_LEFT_POINT;
        prefs.useMinimumHeightForAutoSizing = true;
        prefs.minimumHeightForAutoSizing    = 12;
      }} catch (e) {{}}
      if (!tf.overflows) {{ nFixed++; return; }}

      // Pass B — expand frame to page safe area
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

      // Pass C — reduce point size (floor 5.5 pt)
      var guard = 0;
      while (tf.overflows && guard < 36) {{
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

    alert("Preflight autofix complete.\\n\\n" + log.join("\\n"));

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

    # Count preflight items from the known report
    color_count   = 194
    overset_count = 199
    doc_count     = 2
    total         = color_count + overset_count + doc_count

    report = {
        "script": str(JSX_OUT),
        "target_document": "visceral_theory_of_sight_precision_layout.indd",
        "preflight_profile": "Digital Publishing",
        "fixes": {
            "page_size": {
                "from": "210 mm × 297 mm  (A4 portrait)",
                "to":   f"{PAGE_W_MM} mm × {PAGE_H_MM} mm  (US Letter landscape)",
            },
            "bleed": {
                "from": "3 mm all sides",
                "to":   f"{BLEED_MM} mm all sides",
            },
            "color_errors_targeted":   color_count,
            "overset_errors_targeted": overset_count,
            "document_errors_targeted": doc_count,
            "total_preflight_errors_targeted": total,
        },
        "color_strategy": {
            "paper_like_fills": "→ [Paper]  (matches: "
            + ", ".join(PAPER_KEYWORDS) + ")",
            "all_other_non_black": "→ [Black]",
            "image_frame_strokes": "→ strokeWeight = 0  (removed)",
            "story_text": "→ [Black]",
        },
        "overset_strategy": {
            "pass_a": "AutoSizingType = HEIGHT_ONLY",
            "pass_b": "Expand frame bottom to page safe area",
            "pass_c": "Reduce point size 0.35 pt per iteration, floor 5.5 pt",
        },
        "usage": (
            "In InDesign: File > Scripts > Other Script… "
            "→ select indesign-preflight-autofix-current-doc.jsx"
        ),
    }
    REPORT_OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Report written: {REPORT_OUT}")


if __name__ == "__main__":
    main()
