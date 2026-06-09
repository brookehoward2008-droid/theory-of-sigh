// visceral_theory_of_sight_precision_layout.indd — full preflight autofix
// Profile: Digital Publishing
//
// Fixes applied by this script:
//   (1) Page size  → US Letter landscape  279.4 mm × 215.9 mm
//   (2) Bleed      → 3.175 mm on all four sides
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

if (app.documents.length === 0) {
  alert(
    "No document is open.\n" +
    "Open visceral_theory_of_sight_precision_layout.indd first, " +
    "then run this script again."
  );
} else {

  app.scriptPreferences.userInteractionLevel =
    UserInteractionLevels.INTERACT_WITH_ERRORS_ONLY;

  try {

    var doc  = app.activeDocument;
    var log  = [];
    var nFill   = 0;
    var nStroke = 0;
    var nText   = 0;
    var nFixed  = 0;
    var nLeft   = 0;

    // ── 1. Document preferences: page size + bleed ───────────────────────────
    doc.documentPreferences.pageWidth  = "279.4mm";
    doc.documentPreferences.pageHeight = "215.9mm";
    doc.documentPreferences.documentBleedTopOffset             = "3.175mm";
    doc.documentPreferences.documentBleedBottomOffset          = "3.175mm";
    doc.documentPreferences.documentBleedInsideOrLeftOffset    = "3.175mm";
    doc.documentPreferences.documentBleedOutsideOrRightOffset  = "3.175mm";
    log.push("Page size  → 279.4 mm × 215.9 mm  (US Letter landscape)");
    log.push("Bleed      → 3.175 mm all sides");

    // ── 2. Swatch helpers ────────────────────────────────────────────────────
    function getSwatch(name) {
      var s;
      try { s = doc.swatches.itemByName(name); if (s && s.isValid) return s; }
      catch (e) {}
      try { s = doc.swatches.item(name);       if (s && s.isValid) return s; }
      catch (e) {}
      return null;
    }

    var swBlack = getSwatch("[Black]");
    var swPaper = getSwatch("[Paper]");
    var swNone  = getSwatch("[None]");

    function isPaperLike(swatch) {
      if (!swatch || !swatch.isValid) return false;
      var n = swatch.name.toLowerCase();
      return (
                n.indexOf("paper") >= 0 ||
        n.indexOf("cream") >= 0 ||
        n.indexOf("white") >= 0 ||
        n.indexOf("mist") >= 0 ||
        n.indexOf("unbleach") >= 0 ||
        n.indexOf("ivory") >= 0
      );
    }

    function isSafe(swatch) {
      if (!swatch || !swatch.isValid) return true;
      var n = swatch.name;
      return (
        n === "[Black]"        ||
        n === "[None]"         ||
        n === "[Paper]"        ||
        n === "[Registration]"
      );
    }

    function safeTarget(swatch) {
      return isPaperLike(swatch) ? swPaper : swBlack;
    }

    // ── 3. Fix fills and strokes on one page item ────────────────────────────
    function hasPlacedImage(item) {
      try { return item.images && item.images.length > 0; }
      catch (e) { return false; }
    }

    function fixItem(item) {
      try {
        var fc = item.fillColor;
        if (fc && fc.isValid && !isSafe(fc)) {
          item.fillColor = safeTarget(fc);
          nFill++;
        }
      } catch (e) {}

      try {
        var sw = item.strokeWeight;
        var sc = item.strokeColor;
        if (sc && sc.isValid && !isSafe(sc) && sw > 0) {
          if (hasPlacedImage(item)) {
            item.strokeWeight = 0;
          } else {
            item.strokeColor = swBlack;
          }
          nStroke++;
        }
      } catch (e) {}
    }

    // ── 4. Fix text fill colors in a story ───────────────────────────────────
    function fixStoryColors(story) {
      try {
        var chars = story.characters;
        for (var c = 0; c < chars.length; c++) {
          try {
            var fc = chars[c].fillColor;
            if (fc && fc.isValid && !isSafe(fc)) {
              chars[c].fillColor = swBlack;
              nText++;
            }
          } catch (e) {}
        }
      } catch (e) {}
    }

    // ── 5. Process all page items ────────────────────────────────────────────
    function processItems(items) {
      for (var i = 0; i < items.length; i++) {
        try { fixItem(items[i]); } catch (e) {}
      }
    }

    for (var p = 0; p < doc.pages.length; p++) {
      try { processItems(doc.pages[p].allPageItems); } catch (e) {}
    }

    for (var ms = 0; ms < doc.masterSpreads.length; ms++) {
      var mSpread = doc.masterSpreads[ms];
      for (var mp = 0; mp < mSpread.pages.length; mp++) {
        try { processItems(mSpread.pages[mp].allPageItems); } catch (e) {}
      }
    }

    for (var s = 0; s < doc.stories.length; s++) {
      try { fixStoryColors(doc.stories[s]); } catch (e) {}
    }

    log.push("Fill colors corrected:    " + nFill);
    log.push("Stroke colors corrected:  " + nStroke);
    log.push("Text fills corrected:     " + nText);

    // ── 6. Overset text — three-pass repair ──────────────────────────────────
    function repairOverset(tf) {

      // Pass A — height-only auto-sizing
      try {
        var prefs = tf.textFramePreferences;
        prefs.autoSizingType           = AutoSizingTypeEnum.HEIGHT_ONLY;
        prefs.autoSizingReferencePoint = AutoSizingReferenceEnum.TOP_LEFT_POINT;
        prefs.useMinimumHeightForAutoSizing = true;
        prefs.minimumHeightForAutoSizing    = 12;
      } catch (e) {}
      if (!tf.overflows) { nFixed++; return; }

      // Pass B — expand frame to page safe area
      try {
        var pg = tf.parentPage;
        if (pg) {
          var gb = tf.geometricBounds.slice();
          var pb = pg.bounds;
          var mp = pg.marginPreferences;
          var safeBottom = pb[2] - mp.bottom;
          if (gb[2] < safeBottom) {
            gb[2] = safeBottom;
            tf.geometricBounds = gb;
          }
        }
      } catch (e) {}
      if (!tf.overflows) { nFixed++; return; }

      // Pass C — reduce point size (floor 5.5 pt)
      var guard = 0;
      while (tf.overflows && guard < 36) {
        try {
          var sz = Number(tf.parentStory.texts[0].pointSize);
          if (isNaN(sz) || sz <= 5.5) break;
          var ns = Math.max(5.5, sz - 0.35);
          tf.parentStory.texts[0].pointSize = ns;
          tf.parentStory.texts[0].leading   = ns * 1.20;
        } catch (e) { break; }
        guard++;
      }

      if (!tf.overflows) nFixed++;
      else nLeft++;
    }

    for (var t = 0; t < doc.textFrames.length; t++) {
      try {
        var tf = doc.textFrames[t];
        if (tf.isValid && tf.overflows) repairOverset(tf);
      } catch (e) {}
    }

    log.push("Overset frames repaired:  " + nFixed);
    if (nLeft > 0) {
      log.push("Still overset (manual):   " + nLeft +
               "  (thread text or cut copy to fix)");
    }

    // ── 7. Save ──────────────────────────────────────────────────────────────
    doc.save();
    log.push("Document saved.");

    alert("Preflight autofix complete.\n\n" + log.join("\n"));

  } catch (mainErr) {
    alert(
      "Autofix error on line " + mainErr.line + ":\n" +
      mainErr.message
    );
  }

}
