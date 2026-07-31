from __future__ import annotations

import unittest

from scripts.generate_preflight_autofix_jsx import (
    PAGE_W_MM,
    PAGE_H_MM,
    BLEED_MM,
    PAPER_KEYWORDS,
    build_jsx,
)


class BuildJsxTest(unittest.TestCase):
    def setUp(self) -> None:
        self.jsx = build_jsx()

    def test_jsx_is_non_empty_string(self) -> None:
        self.assertIsInstance(self.jsx, str)
        self.assertGreater(len(self.jsx), 500)

    def test_targets_indesign(self) -> None:
        self.assertIn("#target indesign", self.jsx)

    def test_sets_page_width_to_us_letter_landscape(self) -> None:
        self.assertIn(f'pageWidth  = "{PAGE_W_MM}mm"', self.jsx)

    def test_sets_page_height_to_us_letter_landscape(self) -> None:
        self.assertIn(f'pageHeight = "{PAGE_H_MM}mm"', self.jsx)

    def test_sets_bleed_on_all_sides(self) -> None:
        self.assertIn(f'documentBleedTopOffset             = "{BLEED_MM}mm"', self.jsx)
        self.assertIn(f'documentBleedBottomOffset          = "{BLEED_MM}mm"', self.jsx)
        self.assertIn(f'documentBleedInsideOrLeftOffset    = "{BLEED_MM}mm"', self.jsx)
        self.assertIn(f'documentBleedOutsideOrRightOffset  = "{BLEED_MM}mm"', self.jsx)

    def test_contains_swatch_helpers(self) -> None:
        self.assertIn("function getSwatch(name)", self.jsx)
        self.assertIn('swBlack = getSwatch("[Black]")', self.jsx)
        self.assertIn('swPaper = getSwatch("[Paper]")', self.jsx)

    def test_contains_paper_like_detection(self) -> None:
        self.assertIn("function isPaperLike(swatch)", self.jsx)
        for keyword in PAPER_KEYWORDS:
            self.assertIn(f'"{keyword}"', self.jsx)

    def test_contains_safe_color_check(self) -> None:
        self.assertIn("function isSafe(swatch)", self.jsx)
        self.assertIn('"[Black]"', self.jsx)
        self.assertIn('"[None]"', self.jsx)
        self.assertIn('"[Paper]"', self.jsx)
        self.assertIn('"[Registration]"', self.jsx)

    def test_contains_fix_item_function(self) -> None:
        self.assertIn("function fixItem(item)", self.jsx)

    def test_contains_fix_story_colors(self) -> None:
        self.assertIn("function fixStoryColors(story)", self.jsx)

    def test_contains_overset_repair_three_passes(self) -> None:
        self.assertIn("function repairOverset(tf)", self.jsx)
        self.assertIn("Pass A", self.jsx)
        self.assertIn("Pass B", self.jsx)
        self.assertIn("Pass C", self.jsx)

    def test_overset_floor_is_5_5_pt(self) -> None:
        self.assertIn("5.5", self.jsx)

    def test_saves_document(self) -> None:
        self.assertIn("doc.save()", self.jsx)

    def test_shows_alert_on_completion(self) -> None:
        self.assertIn("Preflight autofix complete", self.jsx)

    def test_handles_no_document_open(self) -> None:
        self.assertIn("No document is open", self.jsx)
        self.assertIn("app.documents.length === 0", self.jsx)

    def test_processes_master_spreads(self) -> None:
        self.assertIn("doc.masterSpreads", self.jsx)

    def test_processes_all_pages(self) -> None:
        self.assertIn("doc.pages.length", self.jsx)

    def test_image_frame_stroke_removal(self) -> None:
        self.assertIn("function hasPlacedImage(item)", self.jsx)
        self.assertIn("strokeWeight = 0", self.jsx)


class PreflightConstantsTest(unittest.TestCase):
    def test_page_dimensions_are_us_letter_landscape(self) -> None:
        self.assertAlmostEqual(PAGE_W_MM, 279.4)
        self.assertAlmostEqual(PAGE_H_MM, 215.9)

    def test_bleed_is_one_eighth_inch(self) -> None:
        self.assertAlmostEqual(BLEED_MM, 3.175)

    def test_paper_keywords_tuple(self) -> None:
        self.assertIsInstance(PAPER_KEYWORDS, tuple)
        self.assertIn("paper", PAPER_KEYWORDS)
        self.assertIn("cream", PAPER_KEYWORDS)
        self.assertIn("white", PAPER_KEYWORDS)
        self.assertIn("ivory", PAPER_KEYWORDS)


if __name__ == "__main__":
    unittest.main()
