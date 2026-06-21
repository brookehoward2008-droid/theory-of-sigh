from __future__ import annotations

import csv
import json
import re
from pathlib import Path

from PIL import Image, ImageOps

try:
    from scripts.build_visceral_book import ARTICLE_BODIES
except ModuleNotFoundError:
    from build_visceral_book import ARTICLE_BODIES


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "visceral-production-route" / "ledgers" / "source-image-ledger.csv"
IMAGE_OUT = ROOT / "images" / "labeled"
DATA_OUT = ROOT / "data"
STYLE_OUT = ROOT / "styles"
INDEX_OUT = ROOT / "index.html"
README_OUT = ROOT / "README.md"
MANIFEST_CSV = DATA_OUT / "labeled-photo-manifest.csv"
MANIFEST_JSON = DATA_OUT / "labeled-photo-manifest.json"

MAX_EDGE = 1800
JPEG_QUALITY = 82
ARTICLE_ORDER = [
    ("Opening Thesis", "The Visceral Theory of Sight", "Sight is never only an act of seeing. It is a negotiation between the body that appears, the culture that disciplines appearance, and the surface that decides what can be touched by the eye. This book moves through agency, constraint, and mediation as one visual pressure system."),
    ("Article I", "Agency / The Body", ARTICLE_BODIES["Agency"]),
    ("Article II", "Constraint / The Rule", ARTICLE_BODIES["Constraint"]),
    ("Article III", "Mediation / The Veil", ARTICLE_BODIES["Mediation"]),
    ("Synthesis", "Unresolved Sight", ARTICLE_BODIES["Synthesis"]),
]

# Ordered from the leafy blue portrait outward: botanical occlusion, soft veils,
# partial-eye pressure, abstract/painted constraint, then least-similar archival/body studies.
SIMILARITY_SEQUENCE = [
    "A58", "A23", "A54", "A55", "A66", "A38", "A40", "A39", "A57", "A31", "A27",
    "A14", "A36", "A20", "A15", "A01", "A26", "A65", "A34", "A44", "A24",
    "A13", "A22", "A09", "A63", "A64", "A25", "A30", "A43", "A52", "A61",
    "A50", "A05", "A18", "A02", "A03", "A35", "A45", "A47", "A46", "A37",
    "A04", "A10", "A19", "A08", "A07", "A06", "A11", "A12", "A16", "A17",
    "A67", "A21", "A28", "A29", "A32", "A33", "A41", "A42", "A48", "A49",
    "A51", "A53", "A56", "A59", "A60", "A62",
]


def slugify(value: str, fallback: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return (value or fallback.lower())[:72].strip("-")


def group_slug(group: str) -> str:
    if ":" in group:
        group = group.split(":", 1)[1]
    return slugify(group, "visual-group")


def read_ledger() -> list[dict[str, str]]:
    if not LEDGER.exists():
        raise FileNotFoundError(f"Missing source ledger: {LEDGER}")
    with LEDGER.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def resize_image(source: Path, target: Path) -> tuple[int, int]:
    with Image.open(source) as img:
        img = ImageOps.exif_transpose(img)
        img.thumbnail((MAX_EDGE, MAX_EDGE), Image.Resampling.LANCZOS)
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")
        elif img.mode == "L":
            img = img.convert("RGB")
        target.parent.mkdir(parents=True, exist_ok=True)
        img.save(target, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
        return img.size


def build_manifest(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for index, row in enumerate(rows, start=1):
        asset_id = row["asset_id"]
        title = row["title"]
        group = row["visual_group"]
        source = Path(row["local_production_path"])
        if not source.exists():
            print(f"WARNING: skipping {asset_id} — source image not found: {source}")
            continue

        label = f"{asset_id.lower()}-{group_slug(group)}-{slugify(title, asset_id)}.jpg"
        target = IMAGE_OUT / label
        width, height = resize_image(source, target)
        records.append(
            {
                "label": asset_id,
                "repo_file": str(target.relative_to(ROOT)).replace("\\", "/"),
                "title": title,
                "visual_group": group,
                "intended_pages_or_section": row["intended_pages_or_section"],
                "creator_or_institution": row["creator_or_institution"],
                "rights_license_status": row["rights_license_status"],
                "original_path": row["original_path"],
                "production_source": row["local_production_path"],
                "web_dimensions_px": f"{width}x{height}",
                "original_dimensions_px": row["dimensions_px"],
                "sequence": f"{index:02d}",
            }
        )
    return records


def write_manifest(records: list[dict[str, str]]) -> None:
    DATA_OUT.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "label",
        "repo_file",
        "title",
        "visual_group",
        "intended_pages_or_section",
        "creator_or_institution",
        "rights_license_status",
        "original_path",
        "production_source",
        "web_dimensions_px",
        "original_dimensions_px",
        "sequence",
    ]
    with MANIFEST_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
    MANIFEST_JSON.write_text(json.dumps(records, indent=2), encoding="utf-8")


def write_site(records: list[dict[str, str]]) -> None:
    order = {label: index for index, label in enumerate(SIMILARITY_SEQUENCE)}
    display_records = sorted(
        records,
        key=lambda record: (order.get(record["label"], len(order)), record["sequence"]),
    )
    STYLE_OUT.mkdir(parents=True, exist_ok=True)
    css = """* { box-sizing: border-box; }
body {
  margin: 0;
  background: #f5f0e8;
  color: #151310;
  font-family: Georgia, 'Times New Roman', serif;
}
header {
  padding: 52px min(7vw, 80px) 30px;
  border-bottom: 1px solid #cfc4b3;
}
h1 {
  margin: 0 0 10px;
  font-size: clamp(2.2rem, 6vw, 5.8rem);
  line-height: .92;
  font-weight: 400;
  letter-spacing: 0;
}
.dek {
  max-width: 820px;
  font-size: 1rem;
  line-height: 1.55;
  color: #4d463c;
}
.article-shell {
  padding: 44px min(7vw, 80px) 18px;
}
.article-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 22px;
  max-width: 1280px;
}
.article-panel {
  grid-column: span 6;
  padding: 22px;
  background: #151310;
  color: #f5f0e8;
  border: 1px solid #2d2922;
}
.article-panel:nth-child(1),
.article-panel:nth-child(5) {
  grid-column: span 12;
}
.article-kicker {
  display: block;
  margin-bottom: 8px;
  font-family: Arial, sans-serif;
  font-size: .72rem;
  letter-spacing: .12em;
  text-transform: uppercase;
  color: #a58242;
}
.article-panel h2 {
  margin: 0 0 14px;
  font-size: clamp(1.45rem, 3vw, 3.2rem);
  line-height: 1;
  font-weight: 400;
}
.article-panel p {
  max-width: 72ch;
  margin: 0 0 13px;
  font-size: .96rem;
  line-height: 1.6;
}
.archive-heading {
  padding: 26px min(7vw, 80px) 0;
  font-family: Arial, sans-serif;
  font-size: .75rem;
  letter-spacing: .12em;
  text-transform: uppercase;
  color: #8a6a2e;
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 22px;
  padding: 30px min(7vw, 80px) 70px;
}
figure {
  margin: 0;
  background: #fffaf1;
  border: 1px solid #d9cebc;
}
img {
  display: block;
  width: 100%;
  aspect-ratio: 4 / 5;
  object-fit: cover;
  background: #ddd3c2;
}
figcaption {
  padding: 12px;
  font-size: .82rem;
  line-height: 1.35;
}
.label {
  display: block;
  margin-bottom: 6px;
  font-family: Arial, sans-serif;
  font-size: .72rem;
  letter-spacing: .08em;
  text-transform: uppercase;
  color: #8a6a2e;
}
.rights {
  display: block;
  margin-top: 7px;
  font-family: Arial, sans-serif;
  font-size: .68rem;
  line-height: 1.3;
  color: #756e64;
}
@media (max-width: 760px) {
  .article-grid {
    display: block;
  }
  .article-panel {
    margin-bottom: 18px;
  }
}
"""
    (STYLE_OUT / "site.css").write_text(css, encoding="utf-8")

    articles = []
    for kicker, title, body in ARTICLE_ORDER:
        articles.append(
            f"""    <article class="article-panel">
      <span class="article-kicker">{html_escape(kicker)}</span>
      <h2>{html_escape(title)}</h2>
{article_body_html(body)}
    </article>"""
        )

    cards = []
    for record in display_records:
        cards.append(
            f"""    <figure>
      <img src="{record['repo_file']}" alt="{html_escape(record['title'])}">
      <figcaption>
        <span class="label">{record['label']} / {html_escape(record['visual_group'])}</span>
        {html_escape(record['title'])}
        <span class="rights">{html_escape(record['rights_license_status'])}</span>
      </figcaption>
    </figure>"""
        )
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>The Visceral Theory of Sight - Labeled Photo Archive</title>
  <link rel="stylesheet" href="styles/site.css">
</head>
<body>
  <header>
    <h1>The Visceral Theory of Sight</h1>
    <p class="dek">A clean labeled photo archive and article route for the editorial book. Read the core argument first, then move through the photos from the leafy blue portrait toward the least similar visual evidence. Every image keeps its label, visual group, rights note, and source trace in <code>data/labeled-photo-manifest.csv</code>.</p>
  </header>
  <section class="article-shell" aria-label="Article content">
    <div class="article-grid">
{chr(10).join(articles)}
    </div>
  </section>
  <div class="archive-heading">Similarity Image Archive</div>
  <main class="grid">
{chr(10).join(cards)}
  </main>
</body>
</html>
"""
    INDEX_OUT.write_text(html, encoding="utf-8")


def html_escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def article_body_html(value: str) -> str:
    paragraphs = [part.strip() for part in value.split("\n\n") if part.strip()]
    return "\n".join(f"      <p>{html_escape(paragraph)}</p>" for paragraph in paragraphs)


def write_readme(records: list[dict[str, str]]) -> None:
    README_OUT.write_text(
        f"""# The Visceral Theory of Sight

Clean GitHub-ready archive for the book layout and labeled photo set.

## What is here

- `images/labeled/` - web-optimized labeled photo copies.
- `data/labeled-photo-manifest.csv` - source, rights, grouping, and original-path ledger.
- `index.html` - simple visual contact sheet for GitHub Pages.
- `scripts/` - local build and InDesign repair scripts.
- `visceral-production-route/` - lightweight production notes, reports, templates, and selected PDF exports.

## Photo Count

{len(records)} labeled photos generated from the production source ledger.

## Rights Note

Some assets are marked Adobe Stock, Unsplash filename present, or creator not verified. Keep the manifest with the images and verify license/source before final public release.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = read_ledger()
    records = build_manifest(rows)
    write_manifest(records)
    write_site(records)
    write_readme(records)
    print(f"Generated {len(records)} labeled photos")
    print(f"Images: {IMAGE_OUT}")
    print(f"Manifest: {MANIFEST_CSV}")
    print(f"Index: {INDEX_OUT}")


if __name__ == "__main__":
    main()
