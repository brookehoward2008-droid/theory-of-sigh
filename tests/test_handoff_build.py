"""Tests for the handoff package InDesign build generator."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDOFF_JSX = ROOT / "visceral-production-route" / "templates" / "indesign-handoff-build.jsx"
HANDOFF_REPORT = ROOT / "visceral-production-route" / "reports" / "handoff-build-generator-report.json"
HANDOFF_ASSETS = ROOT / "visceral-production-route" / "assets" / "handoff"


class HandoffBuildGeneratorTest(unittest.TestCase):
    """Verify the handoff build script produces correct outputs."""

    def test_jsx_file_exists(self) -> None:
        self.assertTrue(HANDOFF_JSX.exists(), f"Expected JSX at {HANDOFF_JSX}")

    def test_jsx_is_nonempty(self) -> None:
        content = HANDOFF_JSX.read_text(encoding="utf-8")
        self.assertGreater(len(content), 1000)

    def test_jsx_contains_document_setup(self) -> None:
        content = HANDOFF_JSX.read_text(encoding="utf-8")
        self.assertIn('doc.documentPreferences.pageWidth = "279.4mm"', content)
        self.assertIn('doc.documentPreferences.pageHeight = "215.9mm"', content)
        self.assertIn("doc.documentPreferences.facingPages = true", content)
        self.assertIn("doc.documentPreferences.pagesPerDocument = 50", content)

    def test_jsx_contains_bleed_settings(self) -> None:
        content = HANDOFF_JSX.read_text(encoding="utf-8")
        self.assertIn('doc.documentPreferences.documentBleedTopOffset = "3.175mm"', content)

    def test_jsx_contains_konly_swatches(self) -> None:
        content = HANDOFF_JSX.read_text(encoding="utf-8")
        self.assertIn("[Black]", content)
        self.assertIn("[Paper]", content)

    def test_jsx_contains_all_50_pages_data(self) -> None:
        content = HANDOFF_JSX.read_text(encoding="utf-8")
        self.assertIn('"page_number": 0', content)
        self.assertIn('"page_number": 49', content)

    def test_jsx_contains_image_placement(self) -> None:
        content = HANDOFF_JSX.read_text(encoding="utf-8")
        self.assertIn("FitOptions.FILL_PROPORTIONALLY", content)
        self.assertIn("FitOptions.CENTER_CONTENT", content)

    def test_jsx_contains_export_functions(self) -> None:
        content = HANDOFF_JSX.read_text(encoding="utf-8")
        self.assertIn("ExportFormat.PDF_TYPE", content)
        self.assertIn("ExportFormat.INDESIGN_MARKUP", content)

    def test_jsx_contains_overset_guard(self) -> None:
        content = HANDOFF_JSX.read_text(encoding="utf-8")
        self.assertIn("fitText", content)
        self.assertIn("overflows", content)

    def test_jsx_contains_error_handling(self) -> None:
        content = HANDOFF_JSX.read_text(encoding="utf-8")
        self.assertIn("handoff-build-error.txt", content)
        self.assertIn("} catch (err) {", content)

    def test_jsx_references_handoff_assets(self) -> None:
        content = HANDOFF_JSX.read_text(encoding="utf-8")
        self.assertIn("assets/handoff/page_0_img_0_xref_12.png", content)

    def test_report_file_exists(self) -> None:
        self.assertTrue(HANDOFF_REPORT.exists(), f"Expected report at {HANDOFF_REPORT}")

    def test_report_contains_expected_fields(self) -> None:
        report = json.loads(HANDOFF_REPORT.read_text(encoding="utf-8"))
        self.assertEqual(report["manifest_version"], "1.0.0-PROD")
        self.assertEqual(report["manifest_status"], "PRODUCTION_READY")
        self.assertEqual(report["total_pages"], 50)
        self.assertEqual(report["total_assets"], 73)
        self.assertEqual(report["trim"]["width_mm"], 279.4)
        self.assertEqual(report["trim"]["height_mm"], 215.9)
        self.assertEqual(report["bleed_mm"], 3.175)

    def test_report_has_coordinate_mapping(self) -> None:
        report = json.loads(HANDOFF_REPORT.read_text(encoding="utf-8"))
        mapping = report["coordinate_mapping"]
        self.assertIn("bleed-inclusive points", mapping["source_system"])
        self.assertIn("page-relative mm", mapping["target_system"])

    def test_handoff_assets_copied(self) -> None:
        self.assertTrue(HANDOFF_ASSETS.is_dir())
        pngs = list(HANDOFF_ASSETS.glob("*.png"))
        self.assertEqual(len(pngs), 73)

    def test_jsx_does_not_contain_placeholder_paths(self) -> None:
        content = HANDOFF_JSX.read_text(encoding="utf-8")
        self.assertNotIn("/home/user/", content)
        self.assertNotIn("C:\\Users\\", content)
        self.assertNotIn("PLACEHOLDER", content)


class HandoffCoordinateConversionTest(unittest.TestCase):
    """Verify coordinate conversion from bleed-inclusive points to trim-relative mm."""

    def test_full_page_image_extends_into_bleed(self) -> None:
        """Page 0 full-page image should have negative top (bleed) coordinates."""
        content = HANDOFF_JSX.read_text(encoding="utf-8")
        # Page 0 image bbox: (115.0, 0.0, 695.0, 630.0) in bleed-inclusive pts
        # Expected trim-relative: top = (0 - 9) * 0.3528 = -3.175mm
        self.assertIn("-3.175", content)

    def test_trim_bottom_bleed_extension(self) -> None:
        """Full-height image should extend to bottom bleed = 219.075mm."""
        content = HANDOFF_JSX.read_text(encoding="utf-8")
        self.assertIn("219.075", content)

    def test_primary_column_alignment(self) -> None:
        """Primary text column at 54.4pt should map to ~16mm from trim edge."""
        from scripts.build_from_handoff import _pt_to_trim_mm, BLEED_PT
        result = _pt_to_trim_mm(54.4)
        self.assertAlmostEqual(result, 16.0, places=0)


if __name__ == "__main__":
    unittest.main()
