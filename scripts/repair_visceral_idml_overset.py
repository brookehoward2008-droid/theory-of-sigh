from __future__ import annotations

import json
from pathlib import Path

from scripts.shared.idml_repair import repair_idml_zip
from scripts.shared.paths import REPORTS_OUT


SOURCE_IDML = Path(
    r"C:\Users\toddl\OneDrive\Desktop\SCHOOL\Graph252 booklab\visceral-theory of sight assets\visceral_theory_of_sight_precision_layout.idml"
)
OUTPUT_IDML = SOURCE_IDML.with_name("visceral_theory_of_sight_precision_layout_TEXT_SAFE.idml")
REPORT_PATH = REPORTS_OUT / "idml-overset-repair-report.json"


def main() -> None:
    if not SOURCE_IDML.exists():
        raise FileNotFoundError(SOURCE_IDML)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    report = repair_idml_zip(SOURCE_IDML, OUTPUT_IDML)
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Repaired IDML: {OUTPUT_IDML}")
    print(f"Report: {REPORT_PATH}")
    print(f"Style changes: {len(report['style_changes'])}")
    print(f"Text frame preferences repaired: {report['text_frame_preferences_repaired']}")
    print(f"Story point-size overrides repaired: {report['story_point_size_overrides_repaired']}")


if __name__ == "__main__":
    main()
