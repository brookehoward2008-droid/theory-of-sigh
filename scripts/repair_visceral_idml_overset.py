from __future__ import annotations

import json
import os
import re
import zipfile
from pathlib import Path


_ASSETS_DIR = Path(os.environ["VISCERAL_ASSETS_DIR"]) if os.environ.get("VISCERAL_ASSETS_DIR") else (Path(__file__).resolve().parents[1] / "images" / "labeled")
SOURCE_IDML = _ASSETS_DIR / "visceral_theory_of_sight_precision_layout.idml"
OUTPUT_IDML = SOURCE_IDML.with_name("visceral_theory_of_sight_precision_layout_TEXT_SAFE.idml")
REPORT_PATH = Path(__file__).resolve().parents[1] / "visceral-production-route" / "reports" / "idml-overset-repair-report.json"


STYLE_POINT_SIZES = {
    "VT Title": 36.0,
    "VT Subtitle": 12.0,
    "VT Section Label": 8.0,
    "VT Heading": 18.0,
    "VT Body": 8.5,
    "VT Caption": 6.5,
    "VT Caption White": 6.5,
    "VT Pull Quote": 18.0,
    "VT Big Quote": 30.0,
    "VT Folio": 6.5,
}


def replace_attr(tag: str, attr: str, value: str) -> str:
    if re.search(rf'\b{attr}="[^"]*"', tag):
        return re.sub(rf'\b{attr}="[^"]*"', f'{attr}="{value}"', tag)
    return tag[:-1] + f' {attr}="{value}">'


def repair_styles(xml: str) -> tuple[str, list[dict[str, str]]]:
    changes: list[dict[str, str]] = []

    def repl(match: re.Match[str]) -> str:
        tag = match.group(0)
        name_match = re.search(r'Name="([^"]+)"', tag)
        if not name_match:
            return tag
        name = name_match.group(1)
        if name not in STYLE_POINT_SIZES:
            return tag

        old_size = re.search(r'PointSize="([^"]+)"', tag)
        old_leading = re.search(r'Leading="([^"]+)"', tag)
        new_size = STYLE_POINT_SIZES[name]
        new_leading = round(new_size * 1.22, 3)
        tag = replace_attr(tag, "PointSize", f"{new_size:g}")
        tag = replace_attr(tag, "Leading", f"{new_leading:g}")
        tag = replace_attr(tag, "AutoLeading", "0")
        tag = replace_attr(tag, "Hyphenation", "true")
        tag = replace_attr(tag, "DesiredGlyphScaling", "100")
        tag = replace_attr(tag, "MinimumGlyphScaling", "94")
        tag = replace_attr(tag, "MaximumGlyphScaling", "103")
        changes.append(
            {
                "style": name,
                "old_point_size": old_size.group(1) if old_size else "missing",
                "new_point_size": f"{new_size:g}",
                "old_leading": old_leading.group(1) if old_leading else "missing",
                "new_leading": f"{new_leading:g}",
            }
        )
        return tag

    return re.sub(r'<ParagraphStyle\b[^>]*>', repl, xml), changes


def repair_text_frame_preferences(xml: str) -> tuple[str, int]:
    count = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal count
        tag = match.group(0)
        count += 1
        tag = replace_attr(tag, "AutoSizingType", "HeightOnly")
        tag = replace_attr(tag, "AutoSizingReferencePoint", "TopLeftPoint")
        tag = replace_attr(tag, "UseMinimumHeightForAutoSizing", "true")
        tag = replace_attr(tag, "MinimumHeightForAutoSizing", "12")
        tag = replace_attr(tag, "FirstBaselineOffset", "LeadingOffset")
        return tag

    return re.sub(r'<TextFramePreference\b[^>]*>', repl, xml), count


def repair_story_overrides(xml: str) -> tuple[str, int]:
    # Some generated ranges can carry direct point-size overrides. Scale only
    # large values so intentional caption/body sizing from repaired styles remains.
    count = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal count
        value = float(match.group(1))
        if value <= 18:
            return match.group(0)
        count += 1
        if value >= 120:
            new_value = 36
        elif value >= 70:
            new_value = 22
        elif value >= 40:
            new_value = 14
        elif value >= 24:
            new_value = 9
        else:
            new_value = 7
        return f'PointSize="{new_value:g}"'

    xml = re.sub(r'PointSize="([0-9.]+)"', repl, xml)
    xml = re.sub(r'AutoLeading="120"', 'AutoLeading="0"', xml)
    return xml, count


def main() -> None:
    if not SOURCE_IDML.exists():
        raise FileNotFoundError(SOURCE_IDML)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    report: dict[str, object] = {
        "source_idml": str(SOURCE_IDML),
        "output_idml": str(OUTPUT_IDML),
        "original_left_untouched": True,
        "style_changes": [],
        "text_frame_preferences_repaired": 0,
        "story_point_size_overrides_repaired": 0,
    }

    with zipfile.ZipFile(SOURCE_IDML, "r") as zin, zipfile.ZipFile(OUTPUT_IDML, "w", compression=zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == "Resources/Styles.xml":
                xml = data.decode("utf-8", errors="ignore")
                xml, changes = repair_styles(xml)
                report["style_changes"] = changes
                data = xml.encode("utf-8")
            elif info.filename.startswith("Spreads/") and info.filename.endswith(".xml"):
                xml = data.decode("utf-8", errors="ignore")
                xml, repaired = repair_text_frame_preferences(xml)
                report["text_frame_preferences_repaired"] = int(report["text_frame_preferences_repaired"]) + repaired
                data = xml.encode("utf-8")
            elif info.filename.startswith("Stories/") and info.filename.endswith(".xml"):
                xml = data.decode("utf-8", errors="ignore")
                xml, repaired = repair_story_overrides(xml)
                report["story_point_size_overrides_repaired"] = int(report["story_point_size_overrides_repaired"]) + repaired
                data = xml.encode("utf-8")
            zout.writestr(info, data)

    report["output_bytes"] = OUTPUT_IDML.stat().st_size
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Repaired IDML: {OUTPUT_IDML}")
    print(f"Report: {REPORT_PATH}")
    print(f"Style changes: {len(report['style_changes'])}")
    print(f"Text frame preferences repaired: {report['text_frame_preferences_repaired']}")
    print(f"Story point-size overrides repaired: {report['story_point_size_overrides_repaired']}")


if __name__ == "__main__":
    main()
