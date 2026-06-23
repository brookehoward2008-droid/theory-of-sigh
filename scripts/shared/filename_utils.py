"""Filename-based rights and creator inference used by multiple build scripts."""

from __future__ import annotations


def infer_rights(name: str) -> str:
    """Return a rights-verification note based on filename keywords."""
    lowered = name.lower()
    if "unsplash" in lowered:
        return "Unsplash filename present; verify source URL and license before final export."
    if "adobestock" in lowered:
        return "Adobe Stock filename present; verify local license before final export."
    return "Local/generated/unknown source; verify creator, source, and usage rights before final export."


def infer_creator(name: str) -> str:
    """Return a best-guess creator attribution from the filename."""
    lowered = name.lower()
    if "unsplash" in lowered:
        slug = name.split("-unsplash")[0]
        return slug.replace("-", " ").title() + " / Unsplash filename"
    if "adobestock" in lowered:
        return "Adobe Stock contributor not verified"
    return "Creator not verified"
