from __future__ import annotations

import unittest

from scripts.create_clean_labeled_repo import (
    slugify,
    group_slug,
    html_escape,
    article_body_html,
    ARTICLE_ORDER,
    SIMILARITY_SEQUENCE,
)


class SlugifyTest(unittest.TestCase):
    def test_basic_lowercase_and_hyphen(self) -> None:
        self.assertEqual(slugify("Hello World", "fallback"), "hello-world")

    def test_special_characters_removed(self) -> None:
        self.assertEqual(slugify("Foo! Bar? Baz.", "fb"), "foo-bar-baz")

    def test_multiple_hyphens_collapsed(self) -> None:
        self.assertEqual(slugify("one---two", "x"), "one-two")

    def test_leading_trailing_hyphens_stripped(self) -> None:
        self.assertEqual(slugify("--trimmed--", "x"), "trimmed")

    def test_empty_string_uses_fallback(self) -> None:
        self.assertEqual(slugify("", "Fallback"), "fallback")

    def test_only_special_chars_uses_fallback(self) -> None:
        self.assertEqual(slugify("!@#$%", "Backup"), "backup")

    def test_truncates_to_72_chars(self) -> None:
        long_input = "a" * 200
        result = slugify(long_input, "fallback")
        self.assertLessEqual(len(result), 72)

    def test_numeric_characters_preserved(self) -> None:
        self.assertEqual(slugify("Image 42 Final", "img"), "image-42-final")


class GroupSlugTest(unittest.TestCase):
    def test_plain_group_name(self) -> None:
        self.assertEqual(group_slug("Raw Agency"), "raw-agency")

    def test_colon_prefix_stripped(self) -> None:
        self.assertEqual(group_slug("Group 1: Mediation"), "mediation")

    def test_empty_group_uses_fallback(self) -> None:
        result = group_slug("")
        self.assertEqual(result, "visual-group")


class HtmlEscapeTest(unittest.TestCase):
    def test_ampersand_escaped(self) -> None:
        self.assertEqual(html_escape("A & B"), "A &amp; B")

    def test_less_than_escaped(self) -> None:
        self.assertEqual(html_escape("<tag>"), "&lt;tag&gt;")

    def test_greater_than_escaped(self) -> None:
        self.assertEqual(html_escape("a > b"), "a &gt; b")

    def test_double_quote_escaped(self) -> None:
        self.assertEqual(html_escape('say "hello"'), "say &quot;hello&quot;")

    def test_no_escaping_needed(self) -> None:
        self.assertEqual(html_escape("plain text"), "plain text")

    def test_all_special_chars_together(self) -> None:
        self.assertEqual(
            html_escape('<a href="x">&</a>'),
            "&lt;a href=&quot;x&quot;&gt;&amp;&lt;/a&gt;",
        )


class ArticleBodyHtmlTest(unittest.TestCase):
    def test_single_paragraph(self) -> None:
        result = article_body_html("Hello world")
        self.assertEqual(result, "      <p>Hello world</p>")

    def test_multiple_paragraphs(self) -> None:
        result = article_body_html("First paragraph\n\nSecond paragraph")
        self.assertIn("      <p>First paragraph</p>", result)
        self.assertIn("      <p>Second paragraph</p>", result)

    def test_empty_paragraphs_skipped(self) -> None:
        result = article_body_html("First\n\n\n\nSecond")
        lines = [line for line in result.split("\n") if line.strip()]
        self.assertEqual(len(lines), 2)

    def test_html_chars_escaped_in_body(self) -> None:
        result = article_body_html("Use <b> & </b>")
        self.assertIn("&lt;b&gt;", result)
        self.assertIn("&amp;", result)


class ArticleOrderTest(unittest.TestCase):
    def test_article_order_has_five_entries(self) -> None:
        self.assertEqual(len(ARTICLE_ORDER), 5)

    def test_article_order_starts_with_opening_thesis(self) -> None:
        kicker, title, body = ARTICLE_ORDER[0]
        self.assertEqual(kicker, "Opening Thesis")
        self.assertEqual(title, "The Visceral Theory of Sight")
        self.assertTrue(len(body) > 50)

    def test_article_order_ends_with_synthesis(self) -> None:
        kicker, title, body = ARTICLE_ORDER[-1]
        self.assertEqual(kicker, "Synthesis")
        self.assertEqual(title, "Unresolved Sight")


class SimilaritySequenceTest(unittest.TestCase):
    def test_sequence_has_expected_entries(self) -> None:
        self.assertEqual(len(SIMILARITY_SEQUENCE), 67)

    def test_sequence_starts_with_a58(self) -> None:
        self.assertEqual(SIMILARITY_SEQUENCE[0], "A58")

    def test_no_duplicate_entries(self) -> None:
        self.assertEqual(len(set(SIMILARITY_SEQUENCE)), len(SIMILARITY_SEQUENCE))


if __name__ == "__main__":
    unittest.main()
