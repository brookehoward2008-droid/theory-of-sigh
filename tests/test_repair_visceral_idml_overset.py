from __future__ import annotations

import unittest

from scripts.repair_visceral_idml_overset import (
    STYLE_POINT_SIZES,
    replace_attr,
    repair_styles,
    repair_text_frame_preferences,
    repair_story_overrides,
)


class ReplaceAttrTest(unittest.TestCase):
    def test_replaces_existing_attribute(self) -> None:
        tag = '<ParagraphStyle PointSize="12" Leading="14">'
        result = replace_attr(tag, "PointSize", "8.5")
        self.assertIn('PointSize="8.5"', result)
        self.assertIn('Leading="14"', result)

    def test_adds_missing_attribute(self) -> None:
        tag = '<ParagraphStyle Name="VT Body">'
        result = replace_attr(tag, "PointSize", "8.5")
        self.assertIn('PointSize="8.5"', result)
        self.assertTrue(result.endswith(">"))

    def test_preserves_tag_structure(self) -> None:
        tag = '<TextFramePreference AutoSizingType="None">'
        result = replace_attr(tag, "AutoSizingType", "HeightOnly")
        self.assertIn('AutoSizingType="HeightOnly"', result)
        self.assertTrue(result.startswith("<TextFramePreference"))
        self.assertTrue(result.endswith(">"))

    def test_replaces_only_target_attribute(self) -> None:
        tag = '<Style Name="Body" PointSize="10" Leading="12">'
        result = replace_attr(tag, "Leading", "15")
        self.assertIn('PointSize="10"', result)
        self.assertIn('Leading="15"', result)


class RepairStylesTest(unittest.TestCase):
    def test_repairs_known_style_point_size(self) -> None:
        xml = '<ParagraphStyle Name="VT Body" PointSize="14" Leading="18">'
        result, changes = repair_styles(xml)
        self.assertIn('PointSize="8.5"', result)
        new_leading = round(8.5 * 1.22, 3)
        self.assertIn(f'Leading="{new_leading:g}"', result)
        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0]["style"], "VT Body")
        self.assertEqual(changes[0]["old_point_size"], "14")

    def test_repairs_multiple_styles(self) -> None:
        xml = (
            '<ParagraphStyle Name="VT Title" PointSize="48" Leading="60">\n'
            '<ParagraphStyle Name="VT Caption" PointSize="10" Leading="12">'
        )
        result, changes = repair_styles(xml)
        self.assertEqual(len(changes), 2)
        self.assertIn('PointSize="36"', result)
        self.assertIn('PointSize="6.5"', result)

    def test_ignores_unknown_style_names(self) -> None:
        xml = '<ParagraphStyle Name="Unknown Style" PointSize="14" Leading="18">'
        result, changes = repair_styles(xml)
        self.assertEqual(changes, [])
        self.assertIn('PointSize="14"', result)

    def test_skips_tags_without_name(self) -> None:
        xml = '<ParagraphStyle PointSize="20" Leading="24">'
        result, changes = repair_styles(xml)
        self.assertEqual(changes, [])
        self.assertIn('PointSize="20"', result)

    def test_adds_hyphenation_and_glyph_scaling(self) -> None:
        xml = '<ParagraphStyle Name="VT Body" PointSize="14">'
        result, _ = repair_styles(xml)
        self.assertIn('Hyphenation="true"', result)
        self.assertIn('DesiredGlyphScaling="100"', result)
        self.assertIn('MinimumGlyphScaling="94"', result)
        self.assertIn('MaximumGlyphScaling="103"', result)

    def test_all_known_styles_have_correct_sizes(self) -> None:
        for style_name, expected_size in STYLE_POINT_SIZES.items():
            xml = f'<ParagraphStyle Name="{style_name}" PointSize="999" Leading="999">'
            result, changes = repair_styles(xml)
            self.assertEqual(len(changes), 1)
            self.assertIn(f'PointSize="{expected_size:g}"', result)


class RepairTextFramePreferencesTest(unittest.TestCase):
    def test_sets_auto_sizing_type(self) -> None:
        xml = '<TextFramePreference AutoSizingType="None">'
        result, count = repair_text_frame_preferences(xml)
        self.assertEqual(count, 1)
        self.assertIn('AutoSizingType="HeightOnly"', result)
        self.assertIn('AutoSizingReferencePoint="TopLeftPoint"', result)
        self.assertIn('UseMinimumHeightForAutoSizing="true"', result)
        self.assertIn('MinimumHeightForAutoSizing="12"', result)
        self.assertIn('FirstBaselineOffset="LeadingOffset"', result)

    def test_counts_multiple_text_frames(self) -> None:
        xml = (
            '<TextFramePreference AutoSizingType="None">\n'
            '<TextFramePreference AutoSizingType="None">\n'
            '<TextFramePreference AutoSizingType="None">'
        )
        result, count = repair_text_frame_preferences(xml)
        self.assertEqual(count, 3)

    def test_leaves_non_text_frame_tags_alone(self) -> None:
        xml = '<ObjectExportOption SomeAttr="value">'
        result, count = repair_text_frame_preferences(xml)
        self.assertEqual(count, 0)
        self.assertEqual(result, xml)


class RepairStoryOverridesTest(unittest.TestCase):
    def test_large_point_sizes_scaled_down(self) -> None:
        xml = 'PointSize="120"'
        result, count = repair_story_overrides(xml)
        self.assertEqual(count, 1)
        self.assertIn('PointSize="36"', result)

    def test_very_large_point_sizes_capped_at_36(self) -> None:
        xml = 'PointSize="200"'
        result, count = repair_story_overrides(xml)
        self.assertIn('PointSize="36"', result)

    def test_medium_large_point_sizes_scaled(self) -> None:
        xml = 'PointSize="70"'
        result, count = repair_story_overrides(xml)
        self.assertIn('PointSize="22"', result)

    def test_mid_range_point_sizes(self) -> None:
        xml = 'PointSize="40"'
        result, count = repair_story_overrides(xml)
        self.assertIn('PointSize="14"', result)

    def test_small_large_point_sizes(self) -> None:
        xml = 'PointSize="24"'
        result, count = repair_story_overrides(xml)
        self.assertIn('PointSize="9"', result)

    def test_sizes_between_18_and_24(self) -> None:
        xml = 'PointSize="19"'
        result, count = repair_story_overrides(xml)
        self.assertIn('PointSize="7"', result)

    def test_small_sizes_left_unchanged(self) -> None:
        xml = 'PointSize="10"'
        result, count = repair_story_overrides(xml)
        self.assertEqual(count, 0)
        self.assertIn('PointSize="10"', result)

    def test_exactly_18_left_unchanged(self) -> None:
        xml = 'PointSize="18"'
        result, count = repair_story_overrides(xml)
        self.assertEqual(count, 0)
        self.assertIn('PointSize="18"', result)

    def test_auto_leading_replaced(self) -> None:
        xml = 'AutoLeading="120"'
        result, count = repair_story_overrides(xml)
        self.assertIn('AutoLeading="0"', result)

    def test_multiple_overrides_in_one_document(self) -> None:
        xml = 'PointSize="120" text PointSize="70" more PointSize="10"'
        result, count = repair_story_overrides(xml)
        self.assertEqual(count, 2)
        self.assertIn('PointSize="36"', result)
        self.assertIn('PointSize="22"', result)
        self.assertIn('PointSize="10"', result)


if __name__ == "__main__":
    unittest.main()
