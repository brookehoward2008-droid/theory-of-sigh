from __future__ import annotations

import json
import re
from pathlib import Path

from scripts.shared.idml_repair import repair_idml_zip
from scripts.shared.paths import REPORTS_OUT, TEMPLATE_OUT


ASSET_FOLDER = Path(
    r"C:\Users\toddl\OneDrive\Desktop\SCHOOL\Graph252 booklab\visceral-theory of sight assets"
)
SOURCE_IDML = ASSET_FOLDER / "visceral_theory_of_sight_precision_layout.idml"
TEXT_SAFE_IDML = ASSET_FOLDER / "visceral_theory_of_sight_precision_layout_TEXT_SAFE.idml"
REPORT_IN = Path(
    r"C:\Users\toddl\.codex\attachments\9f68eab0-e040-40be-b936-0ace6db11bfb\pasted-text.txt"
)

REPORT_DIR = REPORTS_OUT
TEMPLATE_DIR = TEMPLATE_OUT
REPAIR_REPORT = REPORT_DIR / "indesign-preflight-repair-report.json"
JSX_OUT = TEMPLATE_DIR / "indesign-relink-and-fit-current-doc.jsx"


def parse_preflight() -> dict[str, object]:
    if not REPORT_IN.exists():
        return {
            "source_report": str(REPORT_IN),
            "report_found": False,
            "missing_links": [],
            "overset_count": 0,
            "overset_max_characters": 0,
            "overset_total_characters": 0,
        }

    text = REPORT_IN.read_text(errors="replace")
    missing_links = re.findall(r"^([A-Za-z0-9_. ()-]+\.(?:jpe?g|png|tif|tiff))\s*$", text, re.MULTILINE)
    missing_links = [
        name
        for name in missing_links
        if f"{name}\nProblem: The linked file is missing." in text
    ]
    oversets = [int(n) for n in re.findall(r"Overset text:\s*(\d+) characters", text)]
    return {
        "source_report": str(REPORT_IN),
        "report_found": True,
        "missing_links": missing_links,
        "missing_link_unique": sorted(set(missing_links)),
        "overset_count": len(oversets),
        "overset_max_characters": max(oversets) if oversets else 0,
        "overset_total_characters": sum(oversets),
    }


def repair_idml() -> dict[str, object]:
    if not SOURCE_IDML.exists():
        raise FileNotFoundError(SOURCE_IDML)
    return repair_idml_zip(SOURCE_IDML, TEXT_SAFE_IDML)


def write_jsx(preflight: dict[str, object]) -> None:
    missing_unique = preflight.get("missing_link_unique") or []
    names_literal = json.dumps(missing_unique, indent=2)
    asset_literal = str(ASSET_FOLDER).replace("\\", "/")
    report_literal = str(REPORT_DIR / "indesign-relink-and-fit-current-doc-report.txt").replace("\\", "/")
    save_copy_literal = str(ASSET_FOLDER / "visceral_theory_of_sight_precision_layout_TEXT_LINK_SAFE.indd").replace("\\", "/")

    jsx = f"""#target indesign
app.scriptPreferences.userInteractionLevel = UserInteractionLevels.INTERACT_WITH_ALL;

(function () {{
  if (app.documents.length === 0) {{
    alert("Open visceral_theory_of_sight_precision_layout.indd or the TEXT_SAFE IDML first, then run this script.");
    return;
  }}

  var doc = app.activeDocument;
  var assetFolder = Folder("{asset_literal}");
  var reportFile = File("{report_literal}");
  var copyFile = File("{save_copy_literal}");
  var expectedMissing = {names_literal};
  var relinked = [];
  var stillMissing = [];
  var fitted = 0;
  var failedFrames = [];

  function fileForLinkName(name) {{
    var f = File(assetFolder.fsName + "/" + name);
    return f.exists ? f : null;
  }}

  function safeName(link) {{
    try {{ return link.name; }} catch (e) {{ return ""; }}
  }}

  for (var i = 0; i < doc.links.length; i++) {{
    var link = doc.links[i];
    var name = safeName(link);
    var target = fileForLinkName(name);
    if (target) {{
      try {{
        link.relink(target);
        link.update();
        relinked.push(name);
      }} catch (e) {{
        stillMissing.push(name + " :: relink failed: " + e);
      }}
    }} else {{
      var isExpected = false;
      for (var m = 0; m < expectedMissing.length; m++) {{
        if (expectedMissing[m] === name) isExpected = true;
      }}
      if (isExpected) stillMissing.push(name);
    }}
  }}

  function fitFrame(tf) {{
    try {{
      tf.textFramePreferences.autoSizingReferencePoint = AutoSizingReferenceEnum.TOP_LEFT_POINT;
      tf.textFramePreferences.autoSizingType = AutoSizingTypeEnum.HEIGHT_ONLY;
      tf.textFramePreferences.useMinimumHeightForAutoSizing = true;
      tf.textFramePreferences.minimumHeightForAutoSizing = 12;
      tf.textFramePreferences.firstBaselineOffset = FirstBaseline.LEADING_OFFSET;

      var parentPage = tf.parentPage;
      if (parentPage && tf.overflows) {{
        var gb = tf.geometricBounds;
        var pb = parentPage.bounds;
        gb[2] = Math.min(pb[2] - 8, gb[2] + 240);
        tf.geometricBounds = gb;
      }}

      var guard = 0;
      while (tf.overflows && guard < 18) {{
        try {{
          var currentSize = Number(tf.parentStory.texts[0].pointSize);
          if (isNaN(currentSize)) currentSize = 8;
          var nextSize = Math.max(4.5, currentSize * 0.92);
          tf.parentStory.texts[0].pointSize = nextSize;
          tf.parentStory.texts[0].leading = nextSize * 1.18;
        }} catch (e2) {{}}
        guard++;
      }}
      if (!tf.overflows) fitted++;
      else failedFrames.push(tf.id);
    }} catch (e) {{
      failedFrames.push("frame error: " + e);
    }}
  }}

  for (var t = 0; t < doc.textFrames.length; t++) {{
    try {{
      if (doc.textFrames[t].overflows) fitFrame(doc.textFrames[t]);
    }} catch (e) {{
      failedFrames.push("frame loop error: " + e);
    }}
  }}

  try {{
    reportFile.parent.create();
    reportFile.encoding = "UTF-8";
    reportFile.open("w");
    reportFile.writeln("Visceral Theory of Sight InDesign repair report");
    reportFile.writeln("Document: " + doc.name);
    reportFile.writeln("Relinked: " + relinked.length);
    reportFile.writeln(relinked.join("\\n"));
    reportFile.writeln("");
    reportFile.writeln("Still missing exact source files: " + stillMissing.length);
    reportFile.writeln(stillMissing.join("\\n"));
    reportFile.writeln("");
    reportFile.writeln("Overset frames fitted: " + fitted);
    reportFile.writeln("Frames still overset or errored: " + failedFrames.length);
    reportFile.writeln(failedFrames.join("\\n"));
    reportFile.close();
  }} catch (reportError) {{}}

  try {{
    doc.saveACopy(copyFile);
  }} catch (saveError) {{}}

  alert("Repair pass complete. Relinked: " + relinked.length + ". Still missing: " + stillMissing.length + ". Overset frames fitted: " + fitted + ". Report written beside the production files.");
}}());
"""
    JSX_OUT.write_text(jsx, encoding="utf-8")


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)

    preflight = parse_preflight()
    idml_report = repair_idml()
    link_status = []
    for name in preflight.get("missing_link_unique", []):
        p = ASSET_FOLDER / str(name)
        link_status.append({"name": name, "exists_in_asset_folder": p.exists(), "path": str(p)})

    write_jsx(preflight)

    report = {
        "preflight_input": preflight,
        "idml_text_repair": idml_report,
        "missing_link_status": link_status,
        "jsx_repair_script": str(JSX_OUT),
        "exact_source_files_required_for_zero_link_errors": [
            item["name"] for item in link_status if not item["exists_in_asset_folder"]
        ],
    }
    REPAIR_REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Text-safe IDML: {TEXT_SAFE_IDML}")
    print(f"Repair report: {REPAIR_REPORT}")
    print(f"InDesign JSX: {JSX_OUT}")
    print(f"Missing exact source files: {len(report['exact_source_files_required_for_zero_link_errors'])}")
    for name in report["exact_source_files_required_for_zero_link_errors"]:
        print(f"  - {name}")


if __name__ == "__main__":
    main()
