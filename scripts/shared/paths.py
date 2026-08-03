"""Canonical project paths used across build scripts."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROUTE = ROOT / "visceral-production-route"

ASSET_OUT = ROUTE / "assets"
PDF_OUT = ROUTE / "output" / "pdf"
INDESIGN_OUT = ROUTE / "output" / "indesign"
LEDGER_OUT = ROUTE / "ledgers"
NOTES_OUT = ROUTE / "notes"
MANIFEST_OUT = ROUTE / "manifest"
TEMPLATE_OUT = ROUTE / "templates"
REPORTS_OUT = ROUTE / "reports"


def ensure_dirs(*paths: Path) -> None:
    """Create directories (with parents) for every path supplied."""
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)
