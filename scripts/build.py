"""Build orchestrator for The Visceral Theory of Sight production route.

Usage:
    python scripts/build.py               # full build
    python scripts/build.py --visceral     # 50pp visceral book only
    python scripts/build.py --final        # 11-image final refined PDF only
    python scripts/build.py --check        # verify assets exist, no generation
"""

from __future__ import annotations

from scripts.build_final_document import build_final_document, write_report
from scripts.build_visceral_book import (
    PDF_OUT,
    ensure_dirs,
    clean_generated_dirs,
    generate_book,
    generate_cover,
    scan_assets,
    write_full_layout_jsx,
    write_grid_handoff,
    write_ledger,
    write_manifest,
    write_notes,
)
from scripts.shared.paths import PDF_OUT as _PDF_OUT
from scripts.shared.paths import ROOT, ROUTE

FINAL_PDF = _PDF_OUT / "the-visceral-theory-of-sight-final-refined.pdf"


def check_assets() -> bool:
    """Verify source images exist without running a full build."""
    from scripts.build_visceral_book import SOURCE_ASSETS

    if not SOURCE_ASSETS.exists():
        print(f"ERROR: Source asset directory not found: {SOURCE_ASSETS}")
        return False

    images = sorted(
        [p for p in SOURCE_ASSETS.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}]
    )
    canonical = [p for p in images if not p.name.startswith("a")]
    non_canonical = [p for p in images if p.name.startswith("a")]

    print(f"Source directory: {SOURCE_ASSETS}")
    print(f"  Total image files: {len(images)}")
    print(f"  Canonical (labeled): {len(canonical)}")
    print(f"  Prefixed (aNN-*): {len(non_canonical)}")
    print(f"  Repository cover: {ROOT / 'images' / 'cover.jpg'} exists={ (ROOT / 'images' / 'cover.jpg').exists()}")

    missing = []
    for p in images:
        if not p.exists():
            missing.append(p)
    if missing:
        print(f"ERROR: {len(missing)} image paths cannot be read")
        for p in missing:
            print(f"  {p}")
        return False

    manifest_csv = ROUTE / "assets" / "final-11-image-merge" / "manifest.csv"
    if manifest_csv.exists():
        import csv

        with manifest_csv.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        bad = [r["@ImageFile"] for r in rows if not (manifest_csv.parent / r["@ImageFile"]).exists()]
        if bad:
            print(f"WARNING: {len(bad)} manifest entries reference missing images:")
            for name in bad:
                print(f"  {name}")
        else:
            print(f"  Manifest: {len(rows)} rows, all images present")
    else:
        print(f"  Manifest: not found at {manifest_csv} (skipping)")

    print("All checks passed." if not missing else "")
    return len(missing) == 0


def build_visceral_book() -> None:
    """Build the 50-page visceral theory of sight book."""
    print("=" * 72)
    print("BUILD: 50-page Visceral Theory of Sight book")
    print("=" * 72)

    ensure_dirs()
    clean_generated_dirs()
    assets = scan_assets()
    print(f"  Assets scanned: {len(assets)}")

    write_ledger(assets)
    print(f"  Ledger written: {ROUTE / 'ledgers' / 'source-image-ledger.csv'}")

    write_notes(assets)
    print(f"  Notes written: {ROUTE / 'notes' / 'critical-process-notes.md'}")

    write_grid_handoff()
    print("  Grid handoff written (JSON, CSV, MD, JSX)")

    write_full_layout_jsx(assets)
    print("  Full-layout InDesign JSX written")

    generate_cover(assets)
    print(f"  Cover PDF generated: {PDF_OUT / 'cover-design.pdf'}")

    generate_book(assets)
    print(f"  Book PDF generated: {PDF_OUT / 'the-visceral-theory-of-sight-50pp.pdf'}")

    write_manifest(assets)
    print(f"  Manifest written: {ROUTE / 'manifest' / 'production-manifest.json'}")

    print("Visceral book build complete.\n")


def build_final_refined() -> None:
    """Build the 11-image final refined PDF."""
    from scripts.build_final_document import FINAL_PDF as TARGET_PDF, FINAL_REPORT

    print("=" * 72)
    print("BUILD: 11-image Final Refined PDF")
    print("=" * 72)

    output = build_final_document(TARGET_PDF)
    print(f"  Final refined PDF: {output}")
    print(f"  Build report: {FINAL_REPORT}")

    print("Final refined PDF build complete.\n")


def full_build() -> None:
    """Run end-to-end build: visceral book + final refined PDF."""
    build_visceral_book()
    build_final_refined()
    print("=" * 72)
    print("FULL BUILD COMPLETE")
    print("=" * 72)
    print()
    print("Outputs:")
    print(f"  Cover PDF:       {PDF_OUT / 'cover-design.pdf'}")
    print(f"  50pp Book PDF:   {PDF_OUT / 'the-visceral-theory-of-sight-50pp.pdf'}")
    print(f"  Final PDF:       {ROUTE / 'output' / 'pdf' / 'the-visceral-theory-of-sight-final-refined.pdf'}")
    print(f"  Manifest:        {ROUTE / 'manifest' / 'production-manifest.json'}")
    print(f"  InDesign JSX:    {ROUTE / 'templates' / 'indesign-build-full-layout.jsx'}")
    print(f"  Reports:          {ROUTE / 'reports' / 'final-refined-build-report.md'}")
    print(f"  Design analysis:  {ROOT / 'instructions' / 'design-analysis-and-recommendations.md'}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build The Visceral Theory of Sight production route")
    parser.add_argument("--visceral", action="store_true", help="Build 50pp visceral book only")
    parser.add_argument("--final", action="store_true", help="Build 11-image final refined PDF only")
    parser.add_argument("--check", action="store_true", help="Verify assets without generating outputs")
    args = parser.parse_args()

    if args.check:
        ok = check_assets()
        sys.exit(0 if ok else 1)
        return

    if args.visceral:
        build_visceral_book()
    elif args.final:
        build_final_refined()
    else:
        full_build()


if __name__ == "__main__":
    main()
