#!/usr/bin/env python3
"""Production publication engine for *The Visceral Theory of Sight*.

A single orchestrator over the project's build scripts, designed to run
locally and token-free:

  * layout + PDF generation in pure Python (no Adobe app required to run),
  * optional copy/caption generation through a local Ollama server
    (no API key, no per-token cost),
  * packaging into a standalone executable for one-click use.

Usage
-----
    python scripts/build.py --check      # environment + asset preflight, no output
    python scripts/build.py --book       # reportlab book + InDesign handoff artifacts
    python scripts/build.py --final      # 11-image refined final document
    python scripts/build.py --idml       # editable InDesign IDML (layers/links/TOC)  [phase 2]
    python scripts/build.py --copy       # regenerate section copy via local Ollama   [phase 3]
    python scripts/build.py --package    # build a standalone executable (PyInstaller)
    python scripts/build.py --all        # book + final

Notes
-----
This container has no Adobe apps and no Ollama; `--check` reports what is and
isn't available so the same engine behaves predictably on your machine.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
IMAGES = ROOT / "images" / "labeled"
CAPTION_MANIFEST = ROOT / "data" / "visceral-caption-manifest.csv"

OLLAMA_URL = "http://127.0.0.1:11434"
OLLAMA_MODEL = "mistral:latest"

# Pipeline step -> existing script invoked as a subprocess (each has its own main()).
STEP_SCRIPT = {
    "book": "build_visceral_book.py",
    "final": "build_final_document.py",
    "preflight": "build_indesign_preflight_safe.py",
}


def run_script(name: str) -> int:
    path = SCRIPTS / name
    if not path.exists():
        print(f"  ! missing script: {name}")
        return 1
    print(f"  -> python {path.relative_to(ROOT)}")
    return subprocess.call([sys.executable, str(path)], cwd=str(ROOT))


def _ollama_status() -> str:
    try:
        from agents.ollama_client import OllamaClient  # local, no network beyond localhost
    except Exception:
        sys.path.insert(0, str(SCRIPTS))
        from agents.ollama_client import OllamaClient
    client = OllamaClient(url=OLLAMA_URL, model=OLLAMA_MODEL)
    if not client.available():
        return f"not reachable at {OLLAMA_URL} — run `ollama serve` (token-free local agents)"
    models = client.models()
    return f"reachable; models: {', '.join(models) or '(none pulled yet)'}"


def cmd_check() -> int:
    ok = True
    print("Publication engine - environment check\n")
    print("Python:", sys.version.split()[0])

    print("\nPython dependencies:")
    for mod, hint in (("reportlab", "reportlab"), ("PIL", "pillow"), ("pypdf", "pypdf")):
        try:
            __import__(mod)
            print(f"  {mod:10} OK")
        except Exception:
            print(f"  {mod:10} MISSING  (pip install {hint})")
            ok = False

    print("\nAssets:")
    n_images = len(list(IMAGES.glob("*"))) if IMAGES.exists() else 0
    print(f"  images/labeled : {'OK' if n_images else 'EMPTY/MISSING'} ({n_images} files)")
    print(f"  caption manifest: {'OK' if CAPTION_MANIFEST.exists() else 'MISSING'}")

    print("\nLocal agents (token-free):")
    print(f"  Ollama: {_ollama_status()}")

    print("\nOptional tooling:")
    id_cli = any(shutil.which(x) for x in ("InDesign", "indesign", "InDesignServer"))
    print(f"  InDesign on PATH: {'yes' if id_cli else 'no (IDML + PDF still build without it)'}")
    print(f"  PyInstaller     : {'OK' if shutil.which('pyinstaller') else 'not installed (pip install pyinstaller)'}")

    print("\nModes: --book  --final  --idml[phase2]  --copy[phase3]  --package  --all")
    return 0 if ok else 1


def cmd_book() -> int:
    print("[book] reportlab book + InDesign handoff artifacts")
    return run_script(STEP_SCRIPT["book"])


def cmd_final() -> int:
    print("[final] 11-image refined final document")
    return run_script(STEP_SCRIPT["final"])


def cmd_idml() -> int:
    print("[idml] editable InDesign IDML (layers / links / parent pages / TOC)")
    print("  phase 2 — the native editable-IDML emitter is not wired yet.")
    print("  For now, `--book` writes the InDesign handoff scripts under")
    print("  visceral-production-route/templates/ that build the layout in InDesign.")
    return 2


def cmd_copy() -> int:
    print("[copy] regenerate section copy + captions via local Ollama")
    print("  phase 3 — generation hook not wired yet; the client is ready at")
    print("  scripts/agents/ollama_client.py and `--check` reports Ollama status.")
    return 2


def cmd_package() -> int:
    print("[package] standalone executable via PyInstaller")
    if not shutil.which("pyinstaller"):
        print("  PyInstaller not installed. On your machine:")
        print("    pip install pyinstaller")
        print(f"    pyinstaller --onefile --name visceral-engine {Path(__file__).name}")
        print("  (build a Windows .exe on Windows, a Mac binary on macOS).")
        return 2
    return subprocess.call(
        ["pyinstaller", "--onefile", "--name", "visceral-engine", str(Path(__file__))],
        cwd=str(ROOT),
    )


def cmd_all() -> int:
    rc = cmd_book()
    if rc != 0:
        print(f"[all] book step failed (rc={rc}); stopping.")
        return rc
    return cmd_final()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Visceral Theory of Sight publication engine.")
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true", help="environment + asset preflight, no output")
    g.add_argument("--book", action="store_true", help="reportlab book + InDesign handoff artifacts")
    g.add_argument("--final", action="store_true", help="11-image refined final document")
    g.add_argument("--idml", action="store_true", help="editable InDesign IDML [phase 2]")
    g.add_argument("--copy", action="store_true", help="regenerate copy via local Ollama [phase 3]")
    g.add_argument("--package", action="store_true", help="build standalone executable (PyInstaller)")
    g.add_argument("--all", action="store_true", help="book + final")
    args = parser.parse_args(argv)

    if args.check:
        return cmd_check()
    if args.book:
        return cmd_book()
    if args.final:
        return cmd_final()
    if args.idml:
        return cmd_idml()
    if args.copy:
        return cmd_copy()
    if args.package:
        return cmd_package()
    if args.all:
        return cmd_all()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
