/*  The Visceral Theory of Sight — Refine Type + Export Digital-Print PDF
    Brooke Howard

    Runs on the OPEN 50pp InDesign document. It does four things and changes
    nothing about the layout, image placement, or page geometry:

      1. TYPE REFINE  — replaces the generic default face with the locked pairing:
                          • Display (large type)  -> Gloock
                          • Body / labels / caption -> Cormorant Garamond
                          • Italic body            -> Cormorant Garamond Italic
                        Assignment is by point size, so headlines vs. body are
                        kept distinct. Size, colour, leading, position untouched.
      2. WIDOWS       — Chris Larson's note: any paragraph whose last line is a
                        single word gets its tracking tightened a hair until the
                        lone word pulls up. (pp. 3,5,8,9,27,28,29,39,40 + anywhere.)
      3. BODY SIZE    — Chris's note: body text shrank from p40. Body paragraphs
                        at ~9.2pt on pp.40+ are restored to the book body size.
      4. PRINT PDF    — exports a PDF/X-4 (CMYK, document bleed, crop marks) ready
                        for an online/offset printer.

    Fonts: put the supplied "Document Fonts" folder next to this .indd (InDesign
    auto-activates it), or activate Gloock + Cormorant Garamond from Adobe Fonts.

    Run: File > Scripts > Other Script...  (open the document first)
*/
#target "indesign"

(function () {
    if (app.documents.length === 0) { alert("Open the 50pp document first."); return; }
    var doc = app.activeDocument;

    // ---------------- CONFIG (tweak to taste) ----------------
    var DISPLAY_FONT = "Gloock";
    var DISPLAY_STYLE = "Regular";
    var BODY_FONT    = "Cormorant Garamond";
    var BODY_REG     = "Regular";
    var BODY_ITAL    = "Italic";

    var DISPLAY_MIN_PT = 18;     // >= this point size is treated as display -> Gloock

    var WIDOW_TRACK_STEP = -5;   // tracking units per step
    var WIDOW_TRACK_FLOOR = -45; // don't tighten past this

    var BODY_FIX_FIRST_PAGE = 40; // restore body size from this page onward
    var BODY_SMALL_LO = 8.6, BODY_SMALL_HI = 9.6; // the "shrunk" body range to fix
    var BODY_TARGET_PT = 10.4;    // the book's normal body size
    var BODY_MIN_WORDS = 25;      // only treat long paragraphs as body (skip captions)

    var EXPORT_PRESET_TRY = ["[PDF/X-4:2008]", "[PDF/X-4:2010]"];
    // ---------------------------------------------------------

    var report = [], missingFonts = {};

    function fontExists(family, style) {
        try { var f = app.fonts.itemByName(family + "\t" + style); return f.isValid; }
        catch (e) { return false; }
    }
    function setFont(obj, family, style) {
        try {
            if (!fontExists(family, style)) { missingFonts[family + " " + style] = true; return false; }
            obj.appliedFont = family + "\t" + style;
            return true;
        } catch (e) { return false; }
    }
    function pageIntOf(obj) {
        try {
            var tf = obj.parentTextFrames && obj.parentTextFrames.length ? obj.parentTextFrames[0] : obj;
            var pg = tf.parentPage;
            return pg ? parseInt(String(pg.name), 10) : -1;
        } catch (e) { return -1; }
    }

    // ---------- 1) TYPE REFINE (by size, preserve everything else) ----------
    var changedRuns = 0;
    var stories = doc.stories.everyItem().getElements();
    for (var s = 0; s < stories.length; s++) {
        var runs;
        try { runs = stories[s].textStyleRanges.everyItem().getElements(); } catch (e0) { continue; }
        for (var r = 0; r < runs.length; r++) {
            var run = runs[r];
            try {
                if (!run.isValid || String(run.contents) === "") continue;
                var ps = run.pointSize;
                if (typeof ps !== "number") { // mixed: fall back to first char
                    try { ps = run.characters[0].pointSize; } catch (eP) { ps = 10; }
                }
                var wasItalic = /italic|oblique/i.test(String(run.fontStyle));
                if (ps >= DISPLAY_MIN_PT) {
                    setFont(run, DISPLAY_FONT, DISPLAY_STYLE);
                } else if (wasItalic) {
                    setFont(run, BODY_FONT, BODY_ITAL);
                } else {
                    setFont(run, BODY_FONT, BODY_REG);
                }
                changedRuns++;
            } catch (e1) { /* skip a run that can't be measured */ }
        }
    }
    report.push("Type: re-fonted " + changedRuns + " runs (display>=" + DISPLAY_MIN_PT + "pt -> " + DISPLAY_FONT + ", else " + BODY_FONT + ").");

    // ---------- 2) BODY SIZE restore on pp. >= BODY_FIX_FIRST_PAGE ----------
    var bodyFixed = 0;
    var frames = doc.textFrames.everyItem().getElements();
    for (var i = 0; i < frames.length; i++) {
        var tf = frames[i];
        try {
            if (!tf.isValid) continue;
            var pg = tf.parentPage; if (!pg) continue;
            if (parseInt(String(pg.name), 10) < BODY_FIX_FIRST_PAGE) continue;
            var paras = tf.texts[0].paragraphs.everyItem().getElements();
            for (var p = 0; p < paras.length; p++) {
                var par = paras[p];
                var sz = par.pointSize;
                if (typeof sz === "number" && sz >= BODY_SMALL_LO && sz <= BODY_SMALL_HI && par.words.length >= BODY_MIN_WORDS) {
                    par.pointSize = BODY_TARGET_PT;
                    bodyFixed++;
                }
            }
        } catch (e2) {}
    }
    report.push("Body size: restored " + bodyFixed + " paragraph(s) on pp." + BODY_FIX_FIRST_PAGE + "+ to " + BODY_TARGET_PT + "pt.");

    // ---------- 3) WIDOWS (tighten tracking until lone last word pulls up) ----------
    var wFixed = 0, wFail = 0;
    for (var s2 = 0; s2 < stories.length; s2++) {
        var ps2 = stories[s2].paragraphs.everyItem().getElements();
        for (var q = 0; q < ps2.length; q++) {
            var par2 = ps2[q];
            try {
                if (!par2.isValid || par2.lines.length < 2) continue;
                if (par2.words.length < 3) continue;
                if (par2.lines.lastItem().words.length !== 1) continue;
                var start = (typeof par2.tracking === "number") ? par2.tracking : 0;
                var t = start, ok = false;
                while (t > WIDOW_TRACK_FLOOR) {
                    t += WIDOW_TRACK_STEP; par2.tracking = t;
                    if (par2.lines.length < 2 || par2.lines.lastItem().words.length > 1) { ok = true; break; }
                }
                if (ok) wFixed++; else { par2.tracking = start; wFail++; }
            } catch (e3) {}
        }
    }
    report.push("Widows: fixed " + wFixed + (wFail ? (", " + wFail + " need a wider text box by hand") : "") + ".");

    // ---------- 4) EXPORT DIGITAL-PRINT PDF (PDF/X-4, CMYK, bleed, marks) ----------
    var outFile = File(doc.fullName.fsName.replace(/\.indd$/i, "") + "-PRINT.pdf");
    var exported = false, usedPreset = "";
    for (var k = 0; k < EXPORT_PRESET_TRY.length && !exported; k++) {
        try {
            var preset = app.pdfExportPresets.itemByName(EXPORT_PRESET_TRY[k]);
            if (preset.isValid) {
                // make sure marks + document bleed travel with it
                app.pdfExportPreferences.useDocumentBleedWithPDF = true;
                app.pdfExportPreferences.cropMarks = true;
                app.pdfExportPreferences.bleedMarks = false;
                app.pdfExportPreferences.pageInformationMarks = true;
                doc.exportFile(ExportFormat.PDF_TYPE, outFile, false, preset);
                exported = true; usedPreset = EXPORT_PRESET_TRY[k];
            }
        } catch (e4) {}
    }
    if (!exported) { // manual fallback if the X-4 preset isn't present
        try {
            var pp = app.pdfExportPreferences;
            pp.useDocumentBleedWithPDF = true;
            pp.cropMarks = true;
            pp.pageInformationMarks = true;
            try { pp.pdfColorSpace = PDFColorSpace.CMYK; } catch (eC) {}
            try { pp.standardsCompliance = PDFXStandards.PDFX42010_STANDARD; } catch (eS) {}
            doc.exportFile(ExportFormat.PDF_TYPE, outFile, false);
            exported = true; usedPreset = "manual CMYK + bleed + marks";
        } catch (e5) { report.push("Export FAILED: " + e5); }
    }
    if (exported) report.push("Exported print PDF (" + usedPreset + "):\n  " + outFile.fsName);

    // ---------- font availability warning ----------
    var miss = [], any = false;
    for (var key in missingFonts) { if (missingFonts.hasOwnProperty(key)) { miss.push(key); any = true; } }
    var fontMsg = any
        ? ("\n\nMISSING FONTS (install the supplied 'Document Fonts' or activate from Adobe Fonts, then re-run):\n  " + miss.join("\n  "))
        : "\n\nFonts: Gloock + Cormorant Garamond resolved OK.";

    alert("Refine + export complete.\n\n" + report.join("\n") + fontMsg);
})();
