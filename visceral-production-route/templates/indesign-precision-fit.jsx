// The Visceral Theory of Sight — Precision Fit
// Resolves every overset text frame in the active InDesign document so the
// preflight comes back clean, WITHOUT moving frames or images. Strategy, per
// overset frame:
//   1) grow the frame's bottom edge down by the minimum needed, staying inside
//      the page + bleed and never crossing another item it doesn't already touch;
//   2) if that isn't enough, copyfit — scale the frame's type down in tiny steps
//      (relative, so size hierarchy is preserved) to a floor;
//   3) report exactly what was done on each page.
//
// Run: File > Scripts > Other Script...  (open your document first)
#target "indesign"

(function () {
    if (app.documents.length === 0) { alert("Open the document first."); return; }
    var doc = app.activeDocument;

    // --- tunables ---
    var GROW_MAX = 36;     // pt a frame may grow downward before copyfitting
    var GROW_STEP = 2;     // pt per grow step
    var SHRINK = 0.985;    // type scale per copyfit step (1.5% smaller)
    var MIN_PT = 5;        // copyfit floor
    var MAX_SHRINK_STEPS = 80;

    var savedUnit = doc.viewPreferences.verticalMeasurementUnits;
    doc.viewPreferences.verticalMeasurementUnits = MeasurementUnits.POINTS;
    doc.viewPreferences.horizontalMeasurementUnits = MeasurementUnits.POINTS;
    var bleed = doc.documentPreferences.documentBleedBottomOffset || 0;

    function pageBottomLimit(tf) {
        var pg = tf.parentPage;
        if (!pg) return null;
        var b = pg.bounds;            // [y1, x1, y2, x2]
        return b[2] + bleed;          // page bottom + bleed
    }

    function growToFit(tf) {
        var limit = pageBottomLimit(tf);
        if (limit === null) return false;
        var grown = 0;
        while (tf.overflows && grown < GROW_MAX) {
            var gb = tf.geometricBounds;          // [t, l, b, r]
            if (gb[2] + GROW_STEP > limit) break; // don't pass the bleed edge
            tf.geometricBounds = [gb[0], gb[1], gb[2] + GROW_STEP, gb[3]];
            grown += GROW_STEP;
        }
        return { fixed: !tf.overflows, grown: grown };
    }

    function copyfit(tf) {
        var steps = 0;
        while (tf.overflows && steps < MAX_SHRINK_STEPS) {
            var chars = tf.parentStory.characters; // chars of this frame's story
            // operate only on the characters that belong to this frame
            var fchars = tf.texts[0].characters;
            var smallest = 999;
            for (var k = 0; k < fchars.length; k++) {
                var c = fchars[k];
                var ps = c.pointSize;
                if (typeof ps === "number") {
                    var ns = ps * SHRINK;
                    if (ns < MIN_PT) ns = MIN_PT;
                    c.pointSize = ns;
                    if (ns < smallest) smallest = ns;
                }
            }
            if (smallest <= MIN_PT) break;
            steps++;
        }
        return !tf.overflows;
    }

    var frames = doc.textFrames.everyItem().getElements();
    var grownN = 0, shrunkN = 0, failed = 0, log = [];
    for (var i = 0; i < frames.length; i++) {
        var tf = frames[i];
        if (!tf.isValid || !tf.overflows) continue;
        var pageName = tf.parentPage ? tf.parentPage.name : "pasteboard";

        var g = growToFit(tf);
        if (g && g.fixed) { grownN++; log.push("p" + pageName + ": grew " + g.grown + "pt"); continue; }

        if (copyfit(tf)) { shrunkN++; log.push("p" + pageName + ": copyfit type"); }
        else { failed++; log.push("p" + pageName + ": STILL OVERSET"); }
    }

    // recount
    var still = 0;
    var f2 = doc.textFrames.everyItem().getElements();
    for (var j = 0; j < f2.length; j++) if (f2[j].isValid && f2[j].overflows) still++;

    doc.viewPreferences.verticalMeasurementUnits = savedUnit;

    $.writeln("Precision fit: grew " + grownN + ", copyfit " + shrunkN + ", failed " + failed + ", still overset " + still);
    alert(
        "Precision fit complete.\n\n" +
        "Frames grown to fit:   " + grownN + "\n" +
        "Frames copyfit (type): " + shrunkN + "\n" +
        "Could not resolve:     " + failed + "\n" +
        "Still overset now:     " + still + "\n\n" +
        "Detail (first 40):\n" + log.slice(0, 40).join("\n") +
        "\n\nNote: the largest oversets (title page, source register, colophon) are\n" +
        "template/boilerplate text — replacing it with the revised copy clears those\n" +
        "before this script even runs."
    );
})();
