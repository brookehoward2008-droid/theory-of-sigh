from __future__ import annotations

from pypdf import PageObject, PdfReader, PdfWriter, Transformation

from scripts.shared.paths import PDF_OUT as PDF_DIR

SOURCE = PDF_DIR / "the-visceral-theory-of-sight-50pp.pdf"
OUTPUT = PDF_DIR / "the-visceral-theory-of-sight-facing-pages.pdf"


def add_page_to_spread(
    spread: PageObject,
    page: PageObject,
    x_offset: float,
    target_w: float,
    target_h: float,
) -> None:
    source_w = float(page.mediabox.width)
    source_h = float(page.mediabox.height)
    scale = min(target_w / source_w, target_h / source_h)
    placed_w = source_w * scale
    placed_h = source_h * scale
    tx = x_offset + (target_w - placed_w) / 2
    ty = (target_h - placed_h) / 2
    spread.merge_transformed_page(
        page,
        Transformation().scale(scale).translate(tx, ty),
    )


def export_facing_pages() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(
            f"Source PDF not found: {SOURCE}\n"
            "Run the visceral book build first to generate it."
        )
    reader = PdfReader(str(SOURCE))
    writer = PdfWriter()
    page_w = float(reader.pages[0].mediabox.width)
    page_h = float(reader.pages[0].mediabox.height)
    spread_w = page_w * 2

    def blank_spread() -> PageObject:
        return PageObject.create_blank_page(width=spread_w, height=page_h)

    # Reader-spread convention: cover sits alone on the right.
    spread = blank_spread()
    add_page_to_spread(spread, reader.pages[0], page_w, page_w, page_h)
    writer.add_page(spread)

    page_index = 1
    while page_index < len(reader.pages):
        spread = blank_spread()
        add_page_to_spread(spread, reader.pages[page_index], 0, page_w, page_h)
        if page_index + 1 < len(reader.pages):
            add_page_to_spread(spread, reader.pages[page_index + 1], page_w, page_w, page_h)
        writer.add_page(spread)
        page_index += 2

    with OUTPUT.open("wb") as f:
        writer.write(f)

    print(f"Facing-pages PDF: {OUTPUT}")
    print(f"Source pages: {len(reader.pages)}")
    print(f"Spread pages: {len(writer.pages)}")


if __name__ == "__main__":
    export_facing_pages()
