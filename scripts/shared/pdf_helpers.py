"""Shared PDF-drawing helpers for ReportLab canvases."""

from __future__ import annotations

from textwrap import wrap

from reportlab.pdfgen import canvas


def text_lines(text: str, width: int) -> list[str]:
    """Split *text* into wrapped lines, preserving paragraph breaks."""
    lines: list[str] = []
    for paragraph in text.split("\n"):
        if not paragraph.strip():
            lines.append("")
        else:
            lines.extend(wrap(paragraph, width=width))
    return lines


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
) -> float:
    """Word-wrap *text* and draw it line-by-line, returning the final y position."""
    c.setFont(font, size)
    c.setFillColor(color)
    lines = text_lines(text, width_chars)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y
