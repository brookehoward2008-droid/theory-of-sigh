/*  The Visceral Theory of Sight — Add Photos
    Brooke Howard

    Appends each image you pick as a NEW full-bleed page at the end of the book
    (non-destructive — your existing 50 pages are untouched). Each new page gets
    the image fitted to fill the page + bleed, plus a small caption frame in
    Cormorant Garamond you can edit. Move/reorder pages in InDesign afterward.

    For photos that must land on a SPECIFIC existing page, do that by hand (or
    tell me the page numbers and send the files and I'll script exact placement).

    Run: File > Scripts > Other Script...  (open the document first)
*/
#target "indesign"

(function () {
    if (app.documents.length === 0) { alert("Open the document first."); return; }
    var doc = app.activeDocument;

    var files = File.openDialog("Choose photos to add (you can select several)", undefined, true);
    if (!files || !files.length) { return; }

    var oldUnits = doc.viewPreferences.horizontalMeasurementUnits;
    doc.viewPreferences.horizontalMeasurementUnits = MeasurementUnits.POINTS;
    doc.viewPreferences.verticalMeasurementUnits = MeasurementUnits.POINTS;

    var pw = doc.documentPreferences.pageWidth;
    var ph = doc.documentPreferences.pageHeight;
    var bl = Math.max(
        doc.documentPreferences.documentBleedTopOffset,
        doc.documentPreferences.documentBleedBottomOffset,
        doc.documentPreferences.documentBleedInsideOrLeftOffset,
        doc.documentPreferences.documentBleedOutsideOrRightOffset
    ) || 9;

    var added = 0, failed = [];
    for (var i = 0; i < files.length; i++) {
        try {
            var pg = doc.pages.add(LocationOptions.AT_END);
            // full-bleed image frame
            var imgFrame = pg.rectangles.add();
            imgFrame.geometricBounds = [-bl, -bl, ph + bl, pw + bl]; // top,left,bottom,right (points)
            imgFrame.strokeWeight = 0;
            imgFrame.place(File(files[i].fsName));
            imgFrame.fit(FitOptions.FILL_PROPORTIONALLY);
            imgFrame.fit(FitOptions.CENTER_CONTENT);
            // caption frame (editable, Cormorant)
            var cap = pg.textFrames.add();
            cap.geometricBounds = [ph - 48, 36, ph - 24, pw - 36];
            cap.contents = "A## — caption (edit me)";
            try {
                cap.texts[0].appliedFont = "Cormorant Garamond\tItalic";
                cap.texts[0].pointSize = 9;
                cap.texts[0].fillColor = doc.swatches.itemByName("Paper").isValid ? "Paper" : "Black";
            } catch (eF) {}
            added++;
        } catch (e) { failed.push(files[i].name + ": " + e); }
    }

    doc.viewPreferences.horizontalMeasurementUnits = oldUnits;
    alert("Added " + added + " photo page(s) at the end of the book." +
          (failed.length ? ("\n\nFailed:\n" + failed.join("\n")) : "") +
          "\n\nReorder them into place in the Pages panel, then re-run the refine+export script.");
})();
