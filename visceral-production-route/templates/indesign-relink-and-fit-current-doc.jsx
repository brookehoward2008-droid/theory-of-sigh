#target indesign
app.scriptPreferences.userInteractionLevel = UserInteractionLevels.INTERACT_WITH_ALL;

(function () {
  if (app.documents.length === 0) {
    alert("Open visceral_theory_of_sight_precision_layout.indd or the TEXT_SAFE IDML first, then run this script.");
    return;
  }

  var doc = app.activeDocument;
  var assetFolder = Folder("C:/Users/toddl/OneDrive/Desktop/SCHOOL/Graph252 booklab/visceral-theory of sight assets");
  var reportFile = File("C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/reports/indesign-relink-and-fit-current-doc-report.txt");
  var copyFile = File("C:/Users/toddl/OneDrive/Desktop/SCHOOL/Graph252 booklab/visceral-theory of sight assets/visceral_theory_of_sight_precision_layout_TEXT_LINK_SAFE.indd");
  var expectedMissing = [
  "AdobeStock_1985396810.jpeg",
  "AdobeStock_720156988.jpeg",
  "AdobeStock_987045868.jpeg",
  "houcine-ncib-J3fKbg3mkJs-unsplash.jpg"
];
  var relinked = [];
  var stillMissing = [];
  var fitted = 0;
  var failedFrames = [];

  function fileForLinkName(name) {
    var f = File(assetFolder.fsName + "/" + name);
    return f.exists ? f : null;
  }

  function safeName(link) {
    try { return link.name; } catch (e) { return ""; }
  }

  for (var i = 0; i < doc.links.length; i++) {
    var link = doc.links[i];
    var name = safeName(link);
    var target = fileForLinkName(name);
    if (target) {
      try {
        link.relink(target);
        link.update();
        relinked.push(name);
      } catch (e) {
        stillMissing.push(name + " :: relink failed: " + e);
      }
    } else {
      var isExpected = false;
      for (var m = 0; m < expectedMissing.length; m++) {
        if (expectedMissing[m] === name) isExpected = true;
      }
      if (isExpected) stillMissing.push(name);
    }
  }

  function fitFrame(tf) {
    try {
      tf.textFramePreferences.autoSizingReferencePoint = AutoSizingReferenceEnum.TOP_LEFT_POINT;
      tf.textFramePreferences.autoSizingType = AutoSizingTypeEnum.HEIGHT_ONLY;
      tf.textFramePreferences.useMinimumHeightForAutoSizing = true;
      tf.textFramePreferences.minimumHeightForAutoSizing = 12;
      tf.textFramePreferences.firstBaselineOffset = FirstBaseline.LEADING_OFFSET;

      var parentPage = tf.parentPage;
      if (parentPage && tf.overflows) {
        var gb = tf.geometricBounds;
        var pb = parentPage.bounds;
        gb[2] = Math.min(pb[2] - 8, gb[2] + 240);
        tf.geometricBounds = gb;
      }

      var guard = 0;
      while (tf.overflows && guard < 18) {
        try {
          var currentSize = Number(tf.parentStory.texts[0].pointSize);
          if (isNaN(currentSize)) currentSize = 8;
          var nextSize = Math.max(4.5, currentSize * 0.92);
          tf.parentStory.texts[0].pointSize = nextSize;
          tf.parentStory.texts[0].leading = nextSize * 1.18;
        } catch (e2) {}
        guard++;
      }
      if (!tf.overflows) fitted++;
      else failedFrames.push(tf.id);
    } catch (e) {
      failedFrames.push("frame error: " + e);
    }
  }

  for (var t = 0; t < doc.textFrames.length; t++) {
    try {
      if (doc.textFrames[t].overflows) fitFrame(doc.textFrames[t]);
    } catch (e) {
      failedFrames.push("frame loop error: " + e);
    }
  }

  try {
    reportFile.parent.create();
    reportFile.encoding = "UTF-8";
    reportFile.open("w");
    reportFile.writeln("Visceral Theory of Sight InDesign repair report");
    reportFile.writeln("Document: " + doc.name);
    reportFile.writeln("Relinked: " + relinked.length);
    reportFile.writeln(relinked.join("\n"));
    reportFile.writeln("");
    reportFile.writeln("Still missing exact source files: " + stillMissing.length);
    reportFile.writeln(stillMissing.join("\n"));
    reportFile.writeln("");
    reportFile.writeln("Overset frames fitted: " + fitted);
    reportFile.writeln("Frames still overset or errored: " + failedFrames.length);
    reportFile.writeln(failedFrames.join("\n"));
    reportFile.close();
  } catch (reportError) {}

  try {
    doc.saveACopy(copyFile);
  } catch (saveError) {}

  alert("Repair pass complete. Relinked: " + relinked.length + ". Still missing: " + stillMissing.length + ". Overset frames fitted: " + fitted + ". Report written beside the production files.");
}());
