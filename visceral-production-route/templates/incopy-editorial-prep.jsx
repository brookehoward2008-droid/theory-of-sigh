// The Visceral Theory of Sight — InCopy Editorial Prep
// Brooke Howard
//
// For the writing/editing side in Adobe InCopy (works on a linked InDesign
// story/assignment or a standalone .icml). It does the editor's housekeeping —
// no frames moved, no images touched:
//
//   1) Typographic cleanup (GREP find/change across all stories):
//        • straight quotes  ->  typographer's quotes  ' ' " "
//        • double hyphen  --  ->  em dash  —
//        • multiple spaces  ->  single ; spaces before punctuation removed
//        • trailing spaces stripped ; 3+ returns collapsed to one blank line
//   2) Widow flag: lists any paragraph whose last line is a single word, so the
//      editor can revise the copy to fix it (the editorial fix, vs. tracking).
//   3) Copyfit: reports any overset story and by how much.
//   4) Counts: words and characters per story + totals.
//
// Run: Edit/Window > ... > Scripts panel, or File > Scripts. Open the doc first.
#target "incopy"

(function () {
    if (app.documents.length === 0) { alert("Open an InCopy document or assignment first."); return; }
    var doc = app.activeDocument;

    // ---------- 1) Typographic cleanup ----------
    function resetGrep() {
        app.findGrepPreferences = NothingEnum.NOTHING;
        app.changeGrepPreferences = NothingEnum.NOTHING;
    }
    function changeGrep(find, change) {
        resetGrep();
        app.findGrepPreferences.findWhat = find;
        app.changeGrepPreferences.changeTo = change;
        var n = doc.changeGrep().length;
        resetGrep();
        return n;
    }
    var cleanups = [
        // quotes: opening first (after start/space/open bracket/dash), then catch-all close
        ["(^|[\\s(\\[\\{—–-])\"", "$1“"],   // straight " -> left double “
        ["\"", "”"],                                    // remaining " -> right double ”
        ["(^|[\\s(\\[\\{—–-])'", "$1‘"],    // straight ' -> left single ‘
        ["'", "’"],                                     // remaining ' -> right single ’ (apostrophes)
        ["--", "—"],                                    // -- -> em dash
        [" *— *", "—"],                            // tighten spaces around em dash
        [" {2,}", " "],                                          // multiple spaces -> one
        [" +([,.;:!?])", "$1"],                                   // space before punctuation
        [" +\\r", "\r"],                                          // trailing spaces
        ["\\r{3,}", "\r\r"]                                       // 3+ returns -> one blank line
    ];
    var cleanReport = [];
    for (var c = 0; c < cleanups.length; c++) {
        try {
            var hits = changeGrep(cleanups[c][0], cleanups[c][1]);
            if (hits) cleanReport.push("  " + hits + "x  " + cleanups[c][0]);
        } catch (e) { /* skip a pattern that errors on this doc */ }
    }

    // ---------- 2/3/4) per-story widow flag, overset, counts ----------
    var stories = doc.stories.everyItem().getElements();
    var totalWords = 0, totalChars = 0, widows = [], overset = [], n = 0;
    for (var s = 0; s < stories.length; s++) {
        var st = stories[s];
        try {
            if (st.words.length === 0) continue;
            n++;
            totalWords += st.words.length;
            totalChars += st.characters.length;

            // widow flag (only when lines are composed — i.e., linked to a layout)
            var paras = st.paragraphs.everyItem().getElements();
            for (var p = 0; p < paras.length; p++) {
                try {
                    var par = paras[p];
                    if (par.lines.length < 2 || par.words.length < 3) continue;
                    if (par.lines.lastItem().words.length === 1) {
                        var snippet = String(par.contents).replace(/[\r\n]+/g, " ");
                        if (snippet.length > 46) snippet = snippet.substring(0, 46) + "…";
                        widows.push("  “" + snippet + "”");
                    }
                } catch (e2) {}
            }

            // overset (only meaningful when the story is placed in a frame)
            try {
                var conts = st.textContainers;
                if (conts.length && conts[conts.length - 1].overflows) {
                    overset.push("  story " + (s + 1) + " overflows its frame");
                }
            } catch (e3) {}
        } catch (e1) {}
    }

    var msg = "InCopy editorial prep complete.\n\n" +
        "Cleanup changes:\n" + (cleanReport.length ? cleanReport.join("\n") : "  (nothing to clean)") + "\n\n" +
        "Stories: " + n + "   Words: " + totalWords + "   Characters: " + totalChars + "\n\n" +
        "Widows (revise copy to fix): " + widows.length + "\n" + widows.slice(0, 15).join("\n") + "\n\n" +
        "Overset stories: " + overset.length + "\n" + overset.slice(0, 10).join("\n");
    $.writeln(msg);
    alert(msg);
})();
