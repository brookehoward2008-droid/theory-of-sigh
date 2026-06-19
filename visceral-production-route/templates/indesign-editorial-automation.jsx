// The Visceral Theory of Sight — Editorial Automation
// Brooke Howard
//
// One pass that resolves the two things a printer flags: typographic WIDOWS and
// OVERSET text — without moving images or frames. Run on the open document
// (File > Scripts > Other Script...).
//
//   Pass 1 — WIDOWS: for any paragraph whose final line is a single word, tighten
//            that paragraph's tracking in small steps until the lone word pulls up
//            into the line above (exactly the "tighten the tracking" fix). If a
//            paragraph can't be resolved within the floor, it's reported so you can
//            widen that one text box by hand.
//   Pass 2 — OVERSET: grow a frame's bottom minimally within the page/bleed, else
//            copyfit the type a hair, until nothing overflows.
//
// Tunables below.
#target "indesign"

(function () {
    if (app.documents.length === 0) { alert("Open the document first."); return; }
    var doc = app.activeDocument;

    // --- tunables ---
    var TRACK_STEP = -5;     // tracking units (1/1000 em) per step
    var TRACK_FLOOR = -45;   // don't tighten a paragraph past this
    var GROW_MAX = 36, GROW_STEP = 2, SHRINK = 0.985, MIN_PT = 5, MAX_SHRINK = 80;

    function pageOf(obj) {
        try {
            var frames = obj.parentTextFrames ? obj.parentTextFrames : [obj];
            var pg = frames[0].parentPage || obj.parentPage;
            return pg ? pg.name : "pasteboard";
        } catch (e) { return "?"; }
    }

    // ---------- Pass 1: widows ----------
    var wFixed = 0, wFail = 0, wLog = [];
    var stories = doc.stories.everyItem().getElements();
    for (var s = 0; s < stories.length; s++) {
        var paras = stories[s].paragraphs.everyItem().getElements();
        for (var p = 0; p < paras.length; p++) {
            var par = paras[p];
            if (!par.isValid) continue;
            if (par.lines.length < 2) continue;                 // single line: no widow
            if (par.lines.lastItem().words.length > 1) continue; // last line already ≥2 words
            // ignore one-word paragraphs that are headings (the whole paragraph is one word)
            if (par.words.length < 3) continue;

            var start = (typeof par.tracking === "number") ? par.tracking : 0;
            var t = start, ok = false;
            while (t > TRACK_FLOOR) {
                t += TRACK_STEP;
                par.tracking = t;
                if (par.lines.length < 2 || par.lines.lastItem().words.length > 1) { ok = true; break; }
            }
            if (ok) { wFixed++; wLog.push("p" + pageOf(par) + ": widow pulled up (tracking " + t + ")"); }
            else { par.tracking = start; wFail++; wLog.push("p" + pageOf(par) + ": widow remains — widen this box by hand"); }
        }
    }

    // ---------- Pass 2: overset ----------
    var savedV = doc.viewPreferences.verticalMeasurementUnits;
    doc.viewPreferences.verticalMeasurementUnits = MeasurementUnits.POINTS;
    var bleed = doc.documentPreferences.documentBleedBottomOffset || 0;
    var oGrew = 0, oShrunk = 0, oFail = 0, oLog = [];

    function growToFit(tf) {
        var pg = tf.parentPage; if (!pg) return false;
        var limit = pg.bounds[2] + bleed, grown = 0;
        while (tf.overflows && grown < GROW_MAX) {
            var gb = tf.geometricBounds;
            if (gb[2] + GROW_STEP > limit) break;
            tf.geometricBounds = [gb[0], gb[1], gb[2] + GROW_STEP, gb[3]];
            grown += GROW_STEP;
        }
        return !tf.overflows;
    }
    function copyfit(tf) {
        var steps = 0;
        while (tf.overflows && steps < MAX_SHRINK) {
            var chars = tf.texts[0].characters, smallest = 999;
            for (var k = 0; k < chars.length; k++) {
                var ps = chars[k].pointSize;
                if (typeof ps === "number") {
                    var ns = ps * SHRINK; if (ns < MIN_PT) ns = MIN_PT;
                    chars[k].pointSize = ns; if (ns < smallest) smallest = ns;
                }
            }
            if (smallest <= MIN_PT) break;
            steps++;
        }
        return !tf.overflows;
    }
    var frames = doc.textFrames.everyItem().getElements();
    for (var i = 0; i < frames.length; i++) {
        var tf = frames[i];
        if (!tf.isValid || !tf.overflows) continue;
        if (growToFit(tf)) { oGrew++; oLog.push("p" + pageOf(tf) + ": frame grown"); }
        else if (copyfit(tf)) { oShrunk++; oLog.push("p" + pageOf(tf) + ": copyfit"); }
        else { oFail++; oLog.push("p" + pageOf(tf) + ": still overset"); }
    }
    doc.viewPreferences.verticalMeasurementUnits = savedV;

    // recount overset
    var still = 0, f2 = doc.textFrames.everyItem().getElements();
    for (var j = 0; j < f2.length; j++) if (f2[j].isValid && f2[j].overflows) still++;

    alert(
        "Editorial automation complete.\n\n" +
        "WIDOWS  — fixed " + wFixed + ", needs manual box: " + wFail + "\n" +
        "OVERSET — grown " + oGrew + ", copyfit " + oShrunk + ", unresolved " + oFail + "\n" +
        "Still overset now: " + still + "\n\n" +
        "Widows:\n" + wLog.slice(0, 20).join("\n") +
        (wFail ? "\n\n(For 'widen this box' items, drag the frame edge a few mm — Chris's other fix.)" : "")
    );
})();
