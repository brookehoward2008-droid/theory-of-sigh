#target indesign

/*
  Theory of Sight — InDesign Type System
  Brooke Chauntel

  Run from InDesign with the Theory of Sight document open:
  File > Scripts > Other Script... or place this JSX in the Scripts Panel folder.

  This script creates a print-focused paragraph and character style system,
  applies safe global document typography settings, and builds a production
  report on the pasteboard. It does not rewrite page content.
*/

(function () {
  if (app.documents.length === 0) {
    alert("Open the Theory of Sight InDesign document before running this script.");
    return;
  }

  var doc = app.activeDocument;

  function swatch(name, model, colorValue) {
    var s;
    try {
      s = doc.colors.itemByName(name);
      s.name;
    } catch (e) {
      s = doc.colors.add({ name: name, model: model, space: ColorSpace.CMYK, colorValue: colorValue });
    }
    return s;
  }

  var ink = swatch("Theory Ink", ColorModel.PROCESS, [68, 67, 64, 74]);
  var paper = swatch("Theory Paper Cream", ColorModel.PROCESS, [4, 7, 14, 0]);
  var slate = swatch("Theory Slate Stroke", ColorModel.PROCESS, [46, 26, 20, 20]);
  var bronze = swatch("Theory Bronze", ColorModel.PROCESS, [25, 42, 68, 8]);
  var muted = swatch("Theory Muted Gray", ColorModel.PROCESS, [18, 16, 18, 0]);

  function paraStyle(name, props) {
    var style;
    try {
      style = doc.paragraphStyles.itemByName(name);
      style.name;
    } catch (e) {
      style = doc.paragraphStyles.add({ name: name });
    }
    for (var key in props) {
      try {
        style[key] = props[key];
      } catch (ignore) {}
    }
    return style;
  }

  function charStyle(name, props) {
    var style;
    try {
      style = doc.characterStyles.itemByName(name);
      style.name;
    } catch (e) {
      style = doc.characterStyles.add({ name: name });
    }
    for (var key in props) {
      try {
        style[key] = props[key];
      } catch (ignore) {}
    }
    return style;
  }

  function fontChoice(names, fallback) {
    for (var i = 0; i < names.length; i++) {
      try {
        var f = app.fonts.itemByName(names[i]);
        f.name;
        return names[i];
      } catch (e) {}
    }
    return fallback;
  }

  var displayFont = fontChoice([
    "Cormorant Garamond\tSemiBold",
    "Cormorant Garamond\tRegular",
    "Adobe Garamond Pro\tSemibold",
    "Georgia\tRegular"
  ], "Georgia\tRegular");

  var bodyFont = fontChoice([
    "Source Serif 4\tRegular",
    "Source Serif Pro\tRegular",
    "Minion Pro\tRegular",
    "Georgia\tRegular"
  ], "Georgia\tRegular");

  var sansFont = fontChoice([
    "Inter\tBold",
    "Aptos\tBold",
    "Helvetica Neue\tBold",
    "Arial\tBold"
  ], "Arial\tBold");

  // Paragraph styles: print-focused, editable, and named by role.
  paraStyle("TOS Cover Title", {
    appliedFont: displayFont,
    pointSize: 54,
    leading: 52,
    tracking: -18,
    kerningMethod: "Optical",
    fillColor: paper,
    strokeColor: slate,
    strokeWeight: 0.35,
    spaceAfter: 10,
    hyphenation: false
  });

  paraStyle("TOS Section Title", {
    appliedFont: displayFont,
    pointSize: 42,
    leading: 41,
    tracking: -12,
    kerningMethod: "Optical",
    fillColor: paper,
    strokeColor: slate,
    strokeWeight: 0.25,
    spaceAfter: 8,
    hyphenation: false
  });

  paraStyle("TOS Essay Head", {
    appliedFont: displayFont,
    pointSize: 34,
    leading: 35,
    tracking: -8,
    kerningMethod: "Optical",
    fillColor: paper,
    strokeColor: slate,
    strokeWeight: 0.18,
    spaceAfter: 12,
    hyphenation: false
  });

  paraStyle("TOS Deck", {
    appliedFont: bodyFont,
    pointSize: 13,
    leading: 17,
    tracking: 2,
    kerningMethod: "Metrics",
    fillColor: paper,
    strokeColor: doc.swatches.itemByName("None"),
    strokeWeight: 0,
    spaceAfter: 10,
    hyphenation: true
  });

  paraStyle("TOS Body Copy", {
    appliedFont: bodyFont,
    pointSize: 10.25,
    leading: 14.25,
    tracking: 4,
    kerningMethod: "Metrics",
    fillColor: paper,
    strokeColor: doc.swatches.itemByName("None"),
    strokeWeight: 0,
    spaceAfter: 5,
    hyphenation: true
  });

  paraStyle("TOS Pull Quote", {
    appliedFont: displayFont,
    pointSize: 32,
    leading: 32,
    tracking: -8,
    kerningMethod: "Optical",
    fillColor: paper,
    strokeColor: slate,
    strokeWeight: 0.18,
    hyphenation: false
  });

  paraStyle("TOS Caption", {
    appliedFont: sansFont,
    pointSize: 7.25,
    leading: 9.25,
    tracking: 28,
    kerningMethod: "Metrics",
    fillColor: muted,
    strokeColor: doc.swatches.itemByName("None"),
    strokeWeight: 0,
    capitalization: Capitalization.ALL_CAPS,
    hyphenation: false
  });

  paraStyle("TOS Folio", {
    appliedFont: sansFont,
    pointSize: 7,
    leading: 8,
    tracking: 60,
    kerningMethod: "Metrics",
    fillColor: bronze,
    strokeColor: doc.swatches.itemByName("None"),
    strokeWeight: 0,
    capitalization: Capitalization.ALL_CAPS,
    hyphenation: false
  });

  paraStyle("TOS Reference Entry", {
    appliedFont: bodyFont,
    pointSize: 8.75,
    leading: 12,
    tracking: 2,
    kerningMethod: "Metrics",
    fillColor: ink,
    strokeColor: doc.swatches.itemByName("None"),
    strokeWeight: 0,
    spaceAfter: 4,
    hyphenation: true
  });

  charStyle("TOS Italic Source", {
    fontStyle: "Italic"
  });

  charStyle("TOS Small Caps Label", {
    capitalization: Capitalization.SMALL_CAPS,
    tracking: 50
  });

  charStyle("TOS Slate Stroke Accent", {
    strokeColor: slate,
    strokeWeight: 0.2
  });

  // Document-level type/print setup.
  try {
    doc.viewPreferences.horizontalMeasurementUnits = MeasurementUnits.POINTS;
    doc.viewPreferences.verticalMeasurementUnits = MeasurementUnits.POINTS;
  } catch (ignoreUnits) {}

  try {
    doc.gridPreferences.baselineDivision = 14.25;
    doc.gridPreferences.baselineStart = 36;
    doc.gridPreferences.baselineGridShown = true;
  } catch (ignoreGrid) {}

  try {
    doc.documentPreferences.facingPages = true;
  } catch (ignoreFacing) {}

  // Gentle automatic style pass based on existing text-frame scale.
  var frames = doc.textFrames;
  var styled = 0;
  for (var i = 0; i < frames.length; i++) {
    var tf = frames[i];
    if (!tf.contents || tf.contents.replace(/\s+/g, "") === "") continue;

    var para = tf.paragraphs[0];
    var size = 0;
    try { size = para.pointSize; } catch (ignoreSize) {}

    try {
      if (size >= 40) {
        para.appliedParagraphStyle = doc.paragraphStyles.itemByName("TOS Cover Title");
      } else if (size >= 28) {
        para.appliedParagraphStyle = doc.paragraphStyles.itemByName("TOS Section Title");
      } else if (size >= 16) {
        para.appliedParagraphStyle = doc.paragraphStyles.itemByName("TOS Essay Head");
      } else if (size <= 8) {
        para.appliedParagraphStyle = doc.paragraphStyles.itemByName("TOS Caption");
      } else {
        tf.paragraphs.everyItem().appliedParagraphStyle = doc.paragraphStyles.itemByName("TOS Body Copy");
      }
      styled++;
    } catch (ignoreApply) {}
  }

  // Add a small nonprinting report frame on page 1 pasteboard if possible.
  try {
    var page = doc.pages[0];
    var report = page.textFrames.add();
    report.geometricBounds = [18, -210, 220, -18];
    report.contents = "Theory of Sight type system applied\r" +
      "Styles created: Cover Title, Section Title, Essay Head, Deck, Body Copy, Pull Quote, Caption, Folio, Reference Entry\r" +
      "Frames touched by scale pass: " + styled + "\r" +
      "Next: manually confirm titles, captions, body copy, then run Preflight and Package.";
    report.textFramePreferences.ignoreWrap = true;
    report.nonprinting = true;
  } catch (ignoreReport) {}

  alert("Theory of Sight type system is ready. Styles created and a gentle scale-based pass was applied to " + styled + " text frames.");
})();
