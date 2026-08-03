"""Shared PDF-drawing helpers for ReportLab canvases."""

from __future__ import annotations

from textwrap import wrap

from reportlab.pdfgen import canvas


def text_lines(text: str, width: int, *, control_widows: bool = True) -> list[str]:
    """Split *text* into wrapped lines, preserving paragraph breaks.

    When ``control_widows`` is enabled, a paragraph's final line is not allowed
    to contain a single word when the previous line has room to lend one word.
    This is intentionally conservative: it only adjusts the final two wrapped
    lines of each paragraph and does not change page geometry.
    """
    lines: list[str] = []
    for paragraph in text.split("\n"):
        if not paragraph.strip():
            lines.append("")
            continue

        wrapped = wrap(paragraph, width=width)
        if control_widows and len(wrapped) >= 2 and len(wrapped[-1].split()) == 1:
            previous_words = wrapped[-2].split()
            if len(previous_words) > 1:
                wrapped[-2] = " ".join(previous_words[:-1])
                wrapped[-1] = previous_words[-1] + " " + wrapped[-1]
        lines.extend(wrapped)
    return lines


def _normalize_body_type(leading: float, size: float) -> tuple[float, float]:
    """Repair the known Synthesis body-size drop from the older book route.

    PR #6 restored the Synthesis body copy from 9.2 pt / 13 leading to the
    normal body size. Keeping the correction here lets the current main builder
    inherit that production fix without pulling in PR #6's broad layout, image,
    font, and generated-file changes.
    """
    if abs(size - 9.2) < 0.01 and abs(leading - 13) < 0.01:
        return 14.5, 10.4
    return leading, size


def draw_text_block(
    c: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    width_chars: int,
    leading: float,
    size: float,
    font: str,
    color,
    max_lines: int | None = None,
    *,
    control_widows: bool = True,
) -> float:
    """Word-wrap *text* and draw it line-by-line, returning the final y position."""
    leading, size = _normalize_body_type(leading, size)
    c.setFont(font, size)
    c.setFillColor(color)
    lines = text_lines(text, width_chars, control_widows=control_widows)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y
