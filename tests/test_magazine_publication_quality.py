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
            "The anatomy of looking is a pressure system",
            "Raw Agency",
            "Social Constraint",
            "Mediation",
            "Unresolved Sight",
            "Brooke Chauntel",
            "Everett Community College, 2026",
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

    def test_plate_captions_are_clean(self) -> None:
        html = INDEX.read_text(encoding="utf-8")

        caption_blocks = re.findall(r"(?s)<figcaption>\s*A\d+ / .*?</figcaption>", html)

        # Every editorial grid figure carries a clean ``A## / …`` caption.
        self.assertGreaterEqual(len(caption_blocks), 12)

        # Captions stay prose-only: no raw filenames, stock IDs, or rights notes
        # leak into the reader-facing copy.
        crowded_source_tokens = re.compile(
            r"unsplash|AdobeStock_|\.jpeg|\.jpg|rights before final export", re.I
        )
        for caption in caption_blocks:
            self.assertIsNone(crowded_source_tokens.search(caption), caption)

    def test_references_and_internal_links_are_present(self) -> None:
        html = INDEX.read_text(encoding="utf-8")

        # The masthead navigation links into the chapter anchors of the issue.
        nav_anchors = re.findall(r'href="#([^"]+)"', html)
        self.assertGreaterEqual(len(nav_anchors), 6)
        for section in ("agency", "constraint", "mediation", "synthesis", "references"):
            self.assertIn(section, nav_anchors)

        # Every in-page anchor must resolve to a real element id (no dead links).
        for anchor in nav_anchors:
            self.assertIn(f'id="{anchor}"', html)

        # The references section carries its source notes as an ordered list.
        references_block = re.search(
            r'(?s)<section class="references[^"]*"[^>]*>.*?</section>', html
        )
        self.assertIsNotNone(references_block)
        reference_items = re.findall(r"<li>", references_block.group(0))
        self.assertEqual(len(reference_items), 5)

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
