/*
 * register-toc.jsx — Image Source Register as a native, updatable InDesign TOC.
 *
 * Same machinery as a contents page: it collects every paragraph in the
 * "ImageCredit" style into a generated, page-numbered, leader-dotted list, so
 * the register is style-driven (no run-together text, no stray frame strokes)
 * and refreshes with Layout > Update Table of Contents.
 *
 * Run with the book open: Window > Utilities > Scripts > double-click, or
 * File > Scripts > Run. It then:
 *   1. ensures an "ImageCredit" paragraph style (apply this to each image's
 *      credit line: id / source / rights),
 *   2. ensures a "RegisterEntry" style used to format the generated lines,
 *   3. builds an "Image Source Register" TOC style collecting ImageCredit,
 *   4. generates the register and loads it onto the place cursor.
 */
#target "indesign"
(function () {
    if (app.documents.length === 0) {
        alert("Open the book document first, then run register-toc.jsx.");
        return;
    }
    var doc = app.activeDocument;

    function ensureParagraphStyle(name) {
        var s = doc.paragraphStyles.itemByName(name);
        if (!s.isValid) { s = doc.paragraphStyles.add({ name: name }); }
        return s;
    }

    var creditStyle = ensureParagraphStyle("ImageCredit");
    var entryStyle = ensureParagraphStyle("RegisterEntry");

    // Right-aligned tab with a dot leader so page numbers align with dotted leaders.
    // Cosmetic — tune the position to your column width in the Paragraph Style panel.
    try {
        entryStyle.tabList = [{
            alignment: TabStopAlignment.RIGHT_ALIGN,
            position: 480,
            leader: "."
        }];
    } catch (e) {}

    // TOC style that collects ImageCredit -> RegisterEntry.
    var tocName = "Image Source Register";
    var toc = doc.tocStyles.itemByName(tocName);
    if (!toc.isValid) { toc = doc.tocStyles.add({ name: tocName }); }
    try { toc.title = "IMAGE SOURCE REGISTER"; } catch (e2) {}

    // Reset and define the single entry mapping.
    while (toc.tocStyleEntries.length > 0) { toc.tocStyleEntries[-1].remove(); }
    var entry = toc.tocStyleEntries.add();
    entry.styleName = creditStyle.name;     // source paragraphs to collect
    entry.formatStyle = entryStyle;         // how each generated line is styled
    entry.level = 1;
    try {
        entry.pageNumberPosition = PageNumberPosition.AFTER_ENTRY;
        entry.separator = "\t";             // tab -> dotted leader from the style
    } catch (e3) {}

    // Generate. With no target frame, InDesign loads the place cursor.
    doc.createTOC(toc, true);
    alert(
        "Image Source Register generated.\n\n" +
        "1. Click the register page to place it.\n" +
        "2. Apply the 'ImageCredit' paragraph style to each image's credit line\n" +
        "   (id / source / rights) so it gets collected.\n" +
        "3. Layout > Update Table of Contents to refresh after image changes."
    );
})();
