from __future__ import annotations

import csv
import json
import random
import re
from pathlib import Path

from PIL import Image, ImageOps


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
DISPLAY_RANDOM_SEED = 20260604


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
    display_records = records[:]
    random.Random(DISPLAY_RANDOM_SEED).shuffle(display_records)
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
"""
    (STYLE_OUT / "site.css").write_text(css, encoding="utf-8")

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
    <p class="dek">A clean labeled photo archive for the editorial book. The photos are arranged in a randomized viewing sequence while each image keeps its label, visual group, rights note, and source trace in <code>data/labeled-photo-manifest.csv</code>.</p>
  </header>
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
