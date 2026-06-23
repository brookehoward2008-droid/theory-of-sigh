"""Where the engine reads assets vs. where it writes new material.

Rule (from the local setup):
  * OneDrive holds source assets the engine may **read**.
  * All **new / generated** material is written to the **local PC**, never OneDrive.

``assert_not_onedrive()`` enforces the write rule; ``output_dir()`` returns a
safe, local, non-OneDrive output root. Override locations with env vars:

  * ``VTS_ASSETS_DIR`` — folder to read source assets from (may be on OneDrive)
  * ``VTS_OUTPUT_DIR`` — folder to write outputs to (must be local, not OneDrive)
"""
from __future__ import annotations

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def is_onedrive(path) -> bool:
    """True if *path* lives under a OneDrive folder (OneDrive, 'OneDrive - X')."""
    parts = [p.lower() for p in Path(path).expanduser().parts]
    return any(p == "onedrive" or p.startswith("onedrive ") or p.startswith("onedrive-") for p in parts)


def assert_not_onedrive(path) -> None:
    """Refuse to write anywhere under OneDrive."""
    if is_onedrive(path):
        raise PermissionError(
            f"refusing to write to OneDrive: {path}\n"
            "New material must be saved on the local PC. "
            "Set VTS_OUTPUT_DIR to a local folder (e.g. C:\\VTS-output)."
        )


def assets_dir() -> Path:
    """Read-only source assets. Defaults to the repo images; override with
    VTS_ASSETS_DIR to point at a OneDrive assets folder for *reading*."""
    env = os.environ.get("VTS_ASSETS_DIR")
    return Path(env).expanduser() if env else REPO_ROOT / "images" / "labeled"


def output_dir() -> Path:
    """Local, non-OneDrive folder for all generated output. Created on demand."""
    env = os.environ.get("VTS_OUTPUT_DIR")
    out = Path(env).expanduser() if env else REPO_ROOT / "build" / "out"
    assert_not_onedrive(out)
    out.mkdir(parents=True, exist_ok=True)
    return out


def preflight_dir() -> Path:
    """Local folder for saved preflight reports (under the output root)."""
    d = output_dir() / "preflight"
    d.mkdir(parents=True, exist_ok=True)
    return d
