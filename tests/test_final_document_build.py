from __future__ import annotations

import csv
import json
import unittest
from pathlib import Path

from pypdf import PdfReader

from scripts.build_final_document import (
    APPLY_LAYOUT_REFINE_JSX,
    ASSET_REGISTER_MD,
    ASSET_SHEET_JSX,
    FINAL_PDF,
    MANIFEST_CSV,
    build_final_document,
    build_indesign_asset_sheet,
    build_layout_refine_apply_script,
    build_asset_register,
    load_manifest_rows,
)
from scripts.build_visceral_book import (
    ARTICLE_BODIES,
    INDESIGN_OUT,
    PDF_OUT,
    article_excerpt,
    ensure_dirs,
    generate_book,
    scan_assets,
    write_full_layout_jsx,
)
from scripts.build_indesign_preflight_safe import SAFE_REPORT, SAFE_TEMPLATE


class FinalDocumentBuildTest(unittest.TestCase):
    def test_full_book_article_model_contains_longform_section_bodies(self) -> None:
        required = {"Agency", "Constraint", "Mediation", "Synthesis"}

        self.assertEqual(set(ARTICLE_BODIES), required)
        for section in required:
            words = ARTICLE_BODIES[section].replace("\n", " ").split()
            self.assertGreaterEqual(len(words), 180, section)

        self.assertIn("the body becomes the first instrument of authorship", ARTICLE_BODIES["Agency"].lower())
        self.assertIn("culture turns visibility into a protocol", ARTICLE_BODIES["Constraint"].lower())
        self.assertIn("the veil is an editing system", ARTICLE_BODIES["Mediation"].lower())
        self.assertIn("Sight becomes visceral when these forces remain active together", ARTICLE_BODIES["Synthesis"])
        self.assertNotEqual(article_excerpt("Agency", 8), article_excerpt("Agency", 16))

    def test_full_book_pdf_contains_article_body_text(self) -> None:
        ensure_dirs()
        assets = scan_assets()
        generate_book(assets)

        output = PDF_OUT / "the-visceral-theory-of-sight-51pp.pdf"
        reader = PdfReader(str(output))
        self.assertEqual(len(reader.pages), 51)

        extracted = " ".join(("\n".join(page.extract_text() or "" for page in reader.pages)).split())
        extracted_lower = extracted.lower()
        self.assertIn("the body becomes the first instrument of authorship", extracted_lower)
        self.assertIn("culture turns visibility into a protocol", extracted_lower)
        self.assertIn("the veil is an editing system", extracted_lower)
        self.assertIn("Sight becomes visceral when these forces remain active together", extracted)

    def test_full_indesign_layout_script_saves_indd_and_exports_idml(self) -> None:
        ensure_dirs()
        assets = scan_assets()
        write_full_layout_jsx(assets)

        script = Path(__file__).resolve().parents[1] / "visceral-production-route" / "templates" / "indesign-build-full-layout.jsx"
        contents = script.read_text(encoding="utf-8")
        self.assertIn("var OUTPUT_INDD", contents)
        self.assertIn("var OUTPUT_IDML", contents)
        self.assertIn("the-visceral-theory-of-sight-50pp.indd", contents)
        self.assertIn("the-visceral-theory-of-sight-50pp.idml", contents)
        self.assertIn("doc.save(inddFile)", contents)
        self.assertIn("doc.exportFile(ExportFormat.INDESIGN_MARKUP, idmlFile)", contents)
        self.assertEqual(INDESIGN_OUT.name, "indesign")

    def test_preflight_safe_indesign_script_matches_digital_publishing_profile(self) -> None:
        self.assertTrue(SAFE_TEMPLATE.exists())
        contents = SAFE_TEMPLATE.read_text(encoding="utf-8")

        self.assertIn('doc.documentPreferences.pageWidth = "279.4mm";', contents)
        self.assertIn('doc.documentPreferences.pageHeight = "215.9mm";', contents)
        self.assertIn('documentBleedTopOffset = "3.175mm";', contents)
        self.assertIn('return builtinSwatch(doc, ["Black", "[Black]"]);', contents)
        self.assertIn('return builtinSwatch(doc, ["Paper", "[Paper]"]);', contents)
        self.assertIn("preflight-konly/asset-01-konly.jpg", contents)
        self.assertIn("the-visceral-theory-of-sight-50pp.indd", contents)
        self.assertIn("the-visceral-theory-of-sight-50pp-indesign-auto.pdf", contents)
        self.assertNotIn("the-visceral-theory-of-sight-50pp-preflight-safe.indd", contents)
        self.assertNotIn("ColorSpace.RGB", contents)
        self.assertNotIn('pageWidth = "210mm"', contents)
        self.assertNotIn('pageHeight = "297mm"', contents)

    def test_preflight_safe_generator_report_documents_required_targets(self) -> None:
        self.assertTrue(SAFE_REPORT.exists())
        report = json.loads(SAFE_REPORT.read_text(encoding="utf-8"))

        self.assertEqual(report["trim"]["name"], "US Letter landscape")
        self.assertEqual(report["trim"]["width_mm"], 279.4)
        self.assertEqual(report["trim"]["height_mm"], 215.9)
        self.assertEqual(report["bleed_mm"], 3.175)
        self.assertEqual(report["pages"], 50)
        self.assertEqual(report["swatches"], ["[Black]", "[Paper]"])
        self.assertEqual(report["linked_assets"], 64)

    def test_manifest_rows_have_existing_images(self) -> None:
        rows = load_manifest_rows(MANIFEST_CSV)

        self.assertEqual(len(rows), 11)
        for row in rows:
            self.assertTrue(row.image_path.exists(), str(row.image_path))
            self.assertTrue(row.title)
            self.assertTrue(row.section)
            self.assertTrue(row.caption)

    def test_manifest_has_no_placeholder_paths(self) -> None:
        with MANIFEST_CSV.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))

        self.assertTrue(rows)
        for row in rows:
            image_file = row["@ImageFile"]
            self.assertNotIn("images/", image_file)
            self.assertNotIn("cover_background", image_file)
            self.assertNotIn("architectural_shadow", image_file)

    def test_final_document_builds_polished_pdf(self) -> None:
        output = Path(__file__).resolve().parents[1] / "visceral-production-route" / "tmp" / FINAL_PDF.name

        build_final_document(output)

        self.assertTrue(output.exists())
        self.assertGreater(output.stat().st_size, 1_000_000)

        reader = PdfReader(str(output))
        self.assertEqual(len(reader.pages), 14)

        extracted = "\n".join(page.extract_text() or "" for page in reader.pages)
        self.assertIn("THE VISCERAL THEORY OF SIGHT", extracted)
        self.assertIn("Dappled Shade", extracted)
        self.assertNotIn("[MISSING", extracted)
        self.assertNotIn("cover_background", extracted)

    def test_indesign_asset_sheet_uses_real_manifest_assets(self) -> None:
        output = Path(__file__).resolve().parents[1] / "visceral-production-route" / "tmp" / ASSET_SHEET_JSX.name

        build_indesign_asset_sheet(output)

        contents = output.read_text(encoding="utf-8")
        self.assertIn("var assetSheet = [", contents)
        self.assertIn('page: 5', contents)
        self.assertIn('type: "image"', contents)
        self.assertIn('layer: "BACKGROUND"', contents)
        self.assertIn('bounds: [1.0, 0.9, 10.0, 7.6]', contents)
        self.assertIn('assetPath: "final-11-image-merge/nina-zeynep-guler-fjJiVSX-BxM-unsplash_2.jpg"', contents)
        self.assertIn("FitOptions.FILL_PROPORTIONALLY", contents)
        self.assertNotIn("your_new_asset.jpg", contents)
        self.assertNotIn("cover_background.jpg", contents)
        self.assertIn('handwritten word \\"Hope\\"', contents)

    def test_layout_refine_apply_script_targets_copy_safe_indd(self) -> None:
        output = Path(__file__).resolve().parents[1] / "visceral-production-route" / "tmp" / APPLY_LAYOUT_REFINE_JSX.name

        build_layout_refine_apply_script(output)

        contents = output.read_text(encoding="utf-8")
        self.assertIn("layout refine.indd", contents)
        self.assertIn("layout refine_FINAL_AUTOBUILD.indd", contents)
        self.assertIn("final-11-image-merge", contents)
        self.assertIn("var doc = app.open(outputFile)", contents)
        self.assertIn("if (!outputFile.exists) throw Error", contents)
        self.assertNotIn("app.open(sourceFile)", contents)
        self.assertNotIn("saveACopy", contents)
        self.assertNotIn("sourceFile.copy(", contents)
        self.assertIn("fit(FitOptions.FILL_PROPORTIONALLY)", contents)
        self.assertIn("Final 11-image layout refine build applied", contents)
        self.assertNotIn("your_new_asset.jpg", contents)

    def test_layout_refine_apply_script_injects_verified_toc_and_register(self) -> None:
        output = Path(__file__).resolve().parents[1] / "visceral-production-route" / "tmp" / APPLY_LAYOUT_REFINE_JSX.name

        build_layout_refine_apply_script(output)

        contents = output.read_text(encoding="utf-8")
        self.assertIn("function injectTOCAndBibliography(doc, textLayer)", contents)
        self.assertIn("CONTENTS", contents)
        self.assertIn("Dappled Shade", contents)
        self.assertIn("PRODUCTION REGISTER & BIBLIOGRAPHY", contents)
        self.assertIn("Visual Asset Register: IMG_01 through IMG_11 compiled locally.", contents)
        self.assertIn("READING LIST TO VERIFY", contents)
        self.assertNotIn("IMG_33", contents)

    def test_layout_refine_apply_script_injects_editorial_palette(self) -> None:
        output = Path(__file__).resolve().parents[1] / "visceral-production-route" / "tmp" / APPLY_LAYOUT_REFINE_JSX.name

        build_layout_refine_apply_script(output)

        contents = output.read_text(encoding="utf-8")
        self.assertIn("function injectEditorialPalette(doc)", contents)
        self.assertIn('"Raw Concrete"', contents)
        self.assertIn('"Stark Void"', contents)
        self.assertIn('"Unbleached Page"', contents)
        self.assertIn('"Incandescent Beam"', contents)
        self.assertIn("ColorSpace.CMYK", contents)
        self.assertIn("ColorModel.PROCESS", contents)
        self.assertIn("[19, 15, 16, 0]", contents)
        self.assertNotIn("Color System Updated!", contents)

    def test_layout_refine_apply_script_applies_algorithmic_grid(self) -> None:
        output = Path(__file__).resolve().parents[1] / "visceral-production-route" / "tmp" / APPLY_LAYOUT_REFINE_JSX.name

        build_layout_refine_apply_script(output)

        contents = output.read_text(encoding="utf-8")
        self.assertIn("function computeAndApplyAlgorithmicGrid(doc)", contents)
        self.assertIn("var COL_COUNT = 12", contents)
        self.assertIn("var GUTTER_INCHES = 0.1667", contents)
        self.assertIn("var marginInside = 0.75", contents)
        self.assertIn("var marginTop = marginInside * 1.1333", contents)
        self.assertIn("columnCount = COL_COUNT", contents)
        self.assertIn('baselineDivision = "7.5pt"', contents)
        self.assertIn("new Date().toString()", contents)
        self.assertNotIn("toISOString", contents)
        self.assertNotIn("Algorithmic Grid Implemented!", contents)

    def test_layout_refine_apply_script_injects_harmonic_margin_metric_archive(self) -> None:
        output = Path(__file__).resolve().parents[1] / "visceral-production-route" / "tmp" / APPLY_LAYOUT_REFINE_JSX.name

        build_layout_refine_apply_script(output)

        contents = output.read_text(encoding="utf-8")
        self.assertIn("HARMONIC MARGIN ALGORITHM", contents)
        self.assertIn("Inside Margin: 0.75 in", contents)
        self.assertIn("Top Margin: 0.85 in", contents)
        self.assertIn("Outside Margin: 0.90 in", contents)
        self.assertIn("Bottom Margin: 1.00 in", contents)
        self.assertIn("METRIC BLOCK: SPECIFICATION DATA ARCHIVE // DIAGRAM 04-B", contents)
        self.assertIn("Textual Leading Baseline: 15 pt", contents)
        self.assertIn("7.5 pt Master Layout Subdivisions", contents)
        self.assertIn("Primary Contrast Threshold: 8:1 Evident Range", contents)
        self.assertIn("METRIC DATA // CH. 2", contents)
        self.assertIn("Exposure Range: EV 12-14", contents)
        self.assertIn("Structural Axis: 45-degree convergence", contents)
        self.assertIn("Lens Architecture: 35mm perspective control tilt-shift", contents)

    def test_build_report_documents_harmonic_margin_metric_archive(self) -> None:
        output = Path(__file__).resolve().parents[1] / "visceral-production-route" / "tmp" / FINAL_PDF.name

        build_final_document(output)

        contents = (Path(__file__).resolve().parents[1] / "visceral-production-route" / "reports" / "final-refined-build-report.md").read_text(encoding="utf-8")
        self.assertIn("## Harmonic Margin Algorithm", contents)
        self.assertIn("Inside margin: 0.75 in", contents)
        self.assertIn("Top margin: 0.85 in", contents)
        self.assertIn("Outside margin: 0.90 in", contents)
        self.assertIn("Bottom margin: 1.00 in", contents)
        self.assertIn("## Metric Block", contents)
        self.assertIn("Core Latitude Anchor: 45.6 deg N", contents)
        self.assertIn("Exposure Range: EV 12-14", contents)

    def test_asset_register_uses_verified_assets_not_placeholders(self) -> None:
        output = Path(__file__).resolve().parents[1] / "visceral-production-route" / "tmp" / ASSET_REGISTER_MD.name

        build_asset_register(output)

        contents = output.read_text(encoding="utf-8")
        self.assertIn("ASSET REGISTER: VERIFIED IMAGES & VECTORS", contents)
        self.assertIn("IMG_01", contents)
        self.assertIn("see-plus-NP3s9BYOqAc-unsplash_2.jpg", contents)
        self.assertIn("IMG_11", contents)
        self.assertIn("VECTOR STATUS", contents)
        self.assertIn("No verified vector files were found", contents)
        self.assertNotIn("images/cover_background.jpg", contents)
        self.assertNotIn("architectural_shadow.jpg", contents)
        self.assertNotIn("concrete_geometry.jpg", contents)
        self.assertNotIn("sightline_axis.ai", contents)


if __name__ == "__main__":
    unittest.main()
