from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
HANDOFF = ROOT / "visceral-production-route" / "reports" / "anatomy-of-looking-indesign-handoff.md"


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
        ]

        for term in forbidden_terms:
            self.assertNotIn(term, html)

    def test_plate_captions_are_clean_and_source_register_is_complete(self) -> None:
        html = INDEX.read_text(encoding="utf-8")

        plate_labels = re.findall(r'<span class="label">A\d+ / ', html)
        source_entries = re.findall(r"<li><strong>A\d+ / ", html)
        front_caption_blocks = re.findall(
            r"(?s)<figcaption>\s*<span class=\"label\">A\d+ / .*?</figcaption>",
            html,
        )

        self.assertEqual(len(plate_labels), 67)
        self.assertEqual(len(source_entries), 67)
        self.assertTrue(front_caption_blocks)

        crowded_source_tokens = re.compile(r"unsplash|AdobeStock_|\.jpeg|\.jpg|rights before final export", re.I)
        for caption in front_caption_blocks:
            self.assertIsNone(crowded_source_tokens.search(caption), caption)

    def test_references_and_internal_links_are_present(self) -> None:
        html = INDEX.read_text(encoding="utf-8")

        toc_links = re.findall(r'<li><a href="#[^"]+">', html)
        citation_links = re.findall(r'<sup><a href="#ref-[^"]+">', html)
        references = re.findall(r'id="ref-[^"]+"', html)

        self.assertEqual(len(toc_links), 6)
        self.assertEqual(len(citation_links), 11)
        self.assertEqual(len(references), 5)

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
