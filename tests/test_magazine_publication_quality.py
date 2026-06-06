from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CSS = ROOT / "styles" / "site.css"
HANDOFF = ROOT / "visceral-production-route" / "reports" / "anatomy-of-looking-indesign-handoff.md"
INDESIGN_TEMPLATE = ROOT / "visceral-production-route" / "templates" / "indesign-build-preflight-safe.jsx"


class MagazinePublicationQualityTest(unittest.TestCase):
    def test_front_matter_uses_indesign_publication_language(self) -> None:
        html = INDEX.read_text(encoding="utf-8")

        required_terms = [
            "Looking begins before language",
            "A visual psychology issue on gaze, image memory",
            "Repetition, obstruction, pose, and symbol teach the eye",
            "Image Source Register",
            "Image credits and rights notes are gathered here",
            "Women Through Time",
            "Gaze is also social behavior",
        ]

        for term in required_terms:
            self.assertIn(term, html)

        forbidden_terms = [
            "landscape-facing-page sequence",
            "12-column grid",
            "plate sequence",
            "plate captions",
            "column measures",
            "repeated crops",
            "text frame",
            "Back Matter Source Register",
            "Full source trace",
            "Sequence 01",
            "Opening Sequence",
            "Agency Sequence",
            "Constraint Sequence",
            "Mediation Sequence",
        ]

        for term in forbidden_terms:
            self.assertNotIn(term, html)

    def test_plate_captions_are_clean_and_source_register_is_complete(self) -> None:
        html = INDEX.read_text(encoding="utf-8")

        source_entries = re.findall(r"<li><strong>A\d+ / ", html)
        front_html = html.split('<div class="source-register">', 1)[0]
        front_asset_codes = re.findall(r"\bA\d{2}\s*/", front_html)
        front_sequence_words = re.findall(r"\b\w*Sequence\w*\b", front_html)
        front_caption_blocks = re.findall(r"(?s)<figcaption>.*?</figcaption>", front_html)

        self.assertEqual(front_asset_codes, [])
        self.assertEqual(front_sequence_words, [])
        self.assertEqual(len(source_entries), 64)
        self.assertTrue(front_caption_blocks)

        for removed_label in ("A02", "A03", "A04"):
            self.assertNotIn(removed_label, html)

        crowded_source_tokens = re.compile(r"unsplash|AdobeStock_|\.jpeg|\.jpg|rights before final export", re.I)
        for caption in front_caption_blocks:
            self.assertIsNone(crowded_source_tokens.search(caption), caption)

    def test_references_and_internal_links_are_present(self) -> None:
        html = INDEX.read_text(encoding="utf-8")

        toc_links = re.findall(r'<li><a href="#[^"]+">', html)
        citation_links = re.findall(r'<sup><a href="#ref-[^"]+">', html)
        references = re.findall(r'id="ref-[^"]+"', html)

        self.assertEqual(len(toc_links), 6)
        self.assertEqual(len(citation_links), 13)
        self.assertEqual(len(references), 6)

        for anchor in re.findall(r'href="#([^"]+)"', html):
            self.assertIn(f'id="{anchor}"', html)

    def test_old_school_process_language_is_not_visible(self) -> None:
        html = INDEX.read_text(encoding="utf-8")

        forbidden = [
            "Graph 252",
            "Formerly framed",
            "Group 1",
            "Group 2",
            "Group 3",
            "production route",
            "instructor review",
        ]

        for phrase in forbidden:
            self.assertNotIn(phrase, html)

    def test_handoff_requires_preflight_and_visual_checks(self) -> None:
        handoff = HANDOFF.read_text(encoding="utf-8")

        required = [
            "Run InDesign preflight",
            "Export a PDF and inspect page edges",
            "missing links",
            "overset text",
            "bleed",
            "fonts",
        ]

        for phrase in required:
            self.assertIn(phrase, handoff)

    def test_web_proof_caption_panels_keep_image_text_readable(self) -> None:
        css = CSS.read_text(encoding="utf-8")

        required_rules = [
            ".spread-image figcaption",
            ".plate-run figcaption",
            "background: color-mix(in srgb, var(--bone) 96%, white)",
            "background: color-mix(in srgb, var(--bone) 98%, white)",
            "color: var(--shadow-ink)",
        ]

        for rule in required_rules:
            self.assertIn(rule, css)

        forbidden_panel_rules = [
            ".spread-image figcaption {\n  padding: 12px 14px;\n  color: var(--lace-paper);",
        ]

        for rule in forbidden_panel_rules:
            self.assertNotIn(rule, css)

    def test_indesign_caption_modules_use_paper_panels_and_leafy_cover(self) -> None:
        jsx = INDESIGN_TEMPLATE.read_text(encoding="utf-8")

        self.assertIn('var item = assetById("A58");', jsx)
        self.assertIn("function assetById(id)", jsx)
        self.assertIn("colorPanel(page, b(236, 24, 286, 186), cream, 100);", jsx)
        self.assertIn('textFrame(page, b(240, 28, 269, 182), "THE ANATOMY\\rOF LOOKING", 24, "Bold", ink, 100);', jsx)
        self.assertIn("colorPanel(page, bounds, cream, 98);", jsx)
        self.assertIn('var tf = textFrame(page, bounds, label, 6.2, "Bold", ink, 100);', jsx)
        self.assertIn("colorPanel(page, b(18, 22, 240, 58), cream, 98);", jsx)
        self.assertNotIn('var item = groupAsset("Mediation", 0);', jsx)
        self.assertNotIn("tf.fillColor = ink", jsx)

    def test_indesign_toc_uses_native_adobe_toc(self) -> None:
        jsx = INDESIGN_TEMPLATE.read_text(encoding="utf-8")

        required = [
            "function nativeAdobeToc(doc, ink, gold)",
            'doc.paragraphStyles.add({name: "TOC Source Heading"})',
            'doc.paragraphStyles.add({name: "TOC Entry"})',
            'doc.paragraphStyles.add({name: "TOC Title"})',
            'doc.tocStyles.add({',
            'name: "Magazine Contents"',
            "createBookmarks: true",
            "makeAnchor: true",
            "tocStyle.tocStyleEntries.add(sourceStyle.name",
            "doc.createTOC(tocStyle",
            "nativeAdobeToc(doc, ink, gold);",
            "app.pdfExportPreferences.includeHyperlinks = true",
            "ExportFormat.INTERACTIVE_PDF",
            'pdfExportMode: doc.extractLabel("pdfExportMode")',
            "tocStyles: doc.tocStyles.length",
            "tocBookmarks: doc.bookmarks.length",
            "tocHyperlinks: doc.hyperlinks.length",
        ]

        for text in required:
            self.assertIn(text, jsx)

        forbidden = [
            "function linkedTocPage(",
            "function tocRow(",
            "doc.hyperlinkPageDestinations.add(",
            "doc.hyperlinkTextSources.add(",
        ]

        for text in forbidden:
            self.assertNotIn(text, jsx)

    def test_html_cover_uses_leafy_image_without_cover_caption(self) -> None:
        html = ROOT.joinpath("index.html").read_text(encoding="utf-8")
        cover_start = html.index('<figure class="cover-image">')
        cover_end = html.index("</figure>", cover_start)
        cover_markup = html[cover_start:cover_end]

        self.assertIn("a58-social-constraint-see-plus-np3s9byoqac-unsplash.jpg", cover_markup)
        self.assertNotIn("<figcaption>", cover_markup)
