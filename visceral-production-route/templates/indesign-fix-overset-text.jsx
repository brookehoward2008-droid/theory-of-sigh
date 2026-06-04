// The Visceral Theory of Sight - overset text repair pass
// Usage: open the .indd in InDesign, then run File > Scripts > Other Script...
// This script changes the active document. Save a copy first if needed.

if (app.documents.length === 0) {
  alert("Open the InDesign document first.");
} else {
  var doc = app.activeDocument;
  var report = [];
  var repaired = 0;
  var remaining = 0;

  function pageName(tf) {
    try {
      if (tf.parentPage) return tf.parentPage.name;
    } catch (e) {}
    return "pasteboard/master/unknown";
  }

  function pageSafeBounds(tf) {
    var p = tf.parentPage;
    if (!p) return null;
    var b = p.bounds; // [top,left,bottom,right]
    var mp = p.marginPreferences;
    return [
      b[0] + mp.top,
      b[1] + mp.left,
      b[2] - mp.bottom,
      b[3] - mp.right
    ];
  }

  function clampFrameToSafeArea(tf) {
    var safe = pageSafeBounds(tf);
    if (!safe) return false;
    var gb = tf.geometricBounds;
    var height = gb[2] - gb[0];
    var width = gb[3] - gb[1];
    var newTop = Math.max(safe[0], gb[0]);
    var newLeft = Math.max(safe[1], gb[1]);
    var newBottom = Math.min(safe[2], Math.max(newTop + height, safe[2]));
    var newRight = Math.min(safe[3], Math.max(newLeft + width, safe[3]));
    tf.geometricBounds = [newTop, newLeft, newBottom, newRight];
    return true;
  }

  function reduceStoryType(story) {
    var minSize = 6.5;
    var attempts = 0;
    while (story.overflows && attempts < 18) {
      try {
        for (var i = 0; i < story.texts.length; i++) {
          var t = story.texts[i];
          if (t.pointSize > minSize) {
            t.pointSize = Math.max(minSize, t.pointSize - 0.25);
            t.leading = t.pointSize * 1.22;
          }
        }
      } catch (e) {}
      attempts++;
    }
  }

  // Pass 1: fit frames to content where possible.
  for (var i = 0; i < doc.textFrames.length; i++) {
    var tf = doc.textFrames[i];
    if (!tf.isValid || !tf.overflows) continue;
    try { tf.fit(FitOptions.FRAME_TO_CONTENT); } catch (e) {}
  }

  // Pass 2: expand within safe margins and reduce type only if still overset.
  for (var j = 0; j < doc.textFrames.length; j++) {
    var frame = doc.textFrames[j];
    if (!frame.isValid || !frame.overflows) continue;
    var before = frame.overflows;
    clampFrameToSafeArea(frame);
    try { frame.fit(FitOptions.FRAME_TO_CONTENT); } catch (e2) {}
    if (frame.overflows && frame.parentStory) {
      reduceStoryType(frame.parentStory);
    }
    if (before && !frame.overflows) {
      repaired++;
      report.push("FIXED page " + pageName(frame));
    }
  }

  // Final report.
  for (var k = 0; k < doc.textFrames.length; k++) {
    var finalFrame = doc.textFrames[k];
    if (!finalFrame.isValid || !finalFrame.overflows) continue;
    remaining++;
    report.push("STILL OVERSET page " + pageName(finalFrame) + " bounds " + finalFrame.geometricBounds.join(", "));
  }

  var output = "Overset repair report for " + doc.name + "\n";
  output += "Repaired frames: " + repaired + "\n";
  output += "Remaining overset frames: " + remaining + "\n\n";
  output += report.join("\n");

  try {
    var basePath = doc.filePath ? doc.filePath.fsName : Folder.desktop.fsName;
    var outFile = File(basePath + "/visceral-overset-repair-report.txt");
    outFile.encoding = "UTF-8";
    outFile.open("w");
    outFile.write(output);
    outFile.close();
    alert(output + "\n\nReport written to: " + outFile.fsName);
  } catch (writeErr) {
    alert(output);
  }
}
