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


def _print_local_agents() -> None:
    sys.path.insert(0, str(SCRIPTS))
    from agents.ollama_client import MODELS, OllamaClient  # localhost only

    client = OllamaClient(url=OLLAMA_URL)
    reachable = client.available()
    installed = set(client.models()) if reachable else set()
    if reachable:
        print(f"  Ollama: reachable; {len(installed)} model(s) installed")
    else:
        print(f"  Ollama: not reachable at {OLLAMA_URL} — run `ollama serve` (token-free)")

    def tag(model: str) -> str:
        if not reachable:
            return model
        return f"{model} [{'installed' if model in installed else 'MISSING'}]"

    print("  model plan (task -> model):")
    for task, (fast, best) in MODELS.items():
        line = f"    {task:9} {tag(fast)}"
        if best != fast:
            line += f"   (quality: {tag(best)})"
        print(line)


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
    _print_local_agents()

    print("\nOptional tooling:")
    id_cli = any(shutil.which(x) for x in ("InDesign", "indesign", "InDesignServer"))
    print(f"  InDesign on PATH: {'yes' if id_cli else 'no (IDML + PDF still build without it)'}")
    print(f"  PyInstaller     : {'OK' if shutil.which('pyinstaller') else 'not installed (pip install pyinstaller)'}")

    print("\nOffline guard (no cloud, no tokens):")
    sys.path.insert(0, str(SCRIPTS))
    from agents.local_guard import is_enforced, scan_for_cloud_sdks
    from paths import assets_dir, output_dir
    print(f"  socket guard active : {is_enforced()}")
    findings = scan_for_cloud_sdks(SCRIPTS)
    print(f"  cloud-SDK scan      : {'clean' if not findings else findings}")
    print(f"  assets (read-only)  : {assets_dir()}")
    try:
        print(f"  output (local write): {output_dir()}")
    except Exception as exc:
        print(f"  output (local write): ERROR {exc}")
        ok = False

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


def cmd_preflight(idml_path: str | None) -> int:
    sys.path.insert(0, str(SCRIPTS))
    import preflight
    report = preflight.run_preflight(Path(idml_path) if idml_path else None)
    print("[preflight]")
    for c in report["checks"]:
        print(f"  {'PASS' if c['ok'] else 'FAIL'}  {c['check']}  {c['detail']}")
    print(f"  overall: {'PASS' if report['ok'] else 'NEEDS WORK'}")
    print(f"  saved to {preflight.preflight_dir()}")
    return 0 if report["ok"] else 1


def cmd_read_preflight(pdf: str) -> int:
    sys.path.insert(0, str(SCRIPTS))
    from indesign_preflight import parse_report
    r = parse_report(Path(pdf))
    print(f"[indesign-preflight] {r['document']}")
    print(f"  profile: {r['profile']}")
    print(f"  status : {'CLEAN (nothing to do)' if r['clean'] else 'ERRORS FOUND'}")
    for e in r["errors"][:25]:
        print(f"    - {e}")
    return 0 if r["clean"] else 1


def cmd_skills() -> int:
    sys.path.insert(0, str(SCRIPTS))
    from skills import list_skills
    print("Skills (layout edits the IDML; copy uses local Ollama):")
    for s in list_skills():
        print(f"  [{s.kind:6}] {s.name:20} {s.summary}")
    return 0


def cmd_skill(name: str, idml: str | None, text: str | None) -> int:
    sys.path.insert(0, str(SCRIPTS))
    from skills import SKILLS, list_skills, run_skill
    list_skills()  # register
    if name not in SKILLS:
        print(f"unknown skill {name!r}; run --skills to list")
        return 2
    if SKILLS[name].kind == "layout":
        if not idml:
            print(f"layout skill {name!r} needs --idml PATH")
            return 2
        import shutil as _sh
        from paths import output_dir
        from skills.layout import repack_idml, unpack_idml
        work = output_dir() / "idml-work"
        if work.exists():
            _sh.rmtree(work)
        unpack_idml(Path(idml), work)
        result = run_skill(name, idml_dir=work)
        out = output_dir() / (Path(idml).stem + "-edited.idml")
        repack_idml(work, out)
        print(f"  {name}: {result}")
        print(f"  wrote {out}")
        return 0
    kwargs = {"text": text} if text is not None else {}
    print(run_skill(name, **kwargs))
    return 0


def cmd_autofix(idml: str | None, max_iters: int = 6) -> int:
    if not idml:
        print("--autofix needs --idml PATH")
        return 2
    sys.path.insert(0, str(SCRIPTS))
    import shutil as _sh
    import preflight
    from paths import output_dir
    from skills.layout import (ensure_layers, purge_purple_swatch, relink_images,
                               repack_idml, unpack_idml)

    # preflight check-name substring -> skill that fixes it
    fixers = {
        "layered": ensure_layers,
        "purple stroke": purge_purple_swatch,
        "linked not embedded": relink_images,
    }
    work = output_dir() / "idml-autofix"
    if work.exists():
        _sh.rmtree(work)
    unpack_idml(Path(idml), work)
    print(f"[autofix] {idml}")
    rep = None
    prev_fails: set[str] | None = None
    for i in range(1, max_iters + 1):
        rep = preflight.run_preflight(work)  # fetch a fresh report (also saved to disk)
        fails = [c for c in rep["checks"] if not c["ok"]]
        passed = len(rep["checks"]) - len(fails)
        status = "ALL GREEN" if not fails else "failing: " + ", ".join(c["check"] for c in fails)
        print(f"  iter {i}: {passed}/{len(rep['checks'])} pass  {status}")
        if not fails:
            break
        names = {c["check"] for c in fails}
        if names == prev_fails:
            print("    no further progress; stopping (remaining checks have no fixer).")
            break
        prev_fails = names
        for c in fails:
            for key, fixer in fixers.items():
                if key in c["check"]:
                    print(f"    applying {fixer.__name__} for {c['check']!r}: {fixer(work)}")
                    break
    out = output_dir() / (Path(idml).stem + "-fixed.idml")
    repack_idml(work, out)
    green = bool(rep and rep.get("ok"))
    print(f"  result: {'GREEN' if green else 'NOT fully green'} -> {out}")
    return 0 if green else 1


def cmd_refine_idml(idml: str | None) -> int:
    if not idml:
        print("--refine-idml needs --idml PATH")
        return 2
    sys.path.insert(0, str(SCRIPTS))
    import shutil as _sh
    import preflight
    from paths import output_dir
    from skills.layout import (ensure_layers, purge_purple_swatch, relink_images,
                               repack_idml, unpack_idml)
    work = output_dir() / "idml-refine"
    if work.exists():
        _sh.rmtree(work)
    unpack_idml(Path(idml), work)
    print(f"[refine-idml] chaining layout skills on {idml}")
    print("  ensure_layers      :", ensure_layers(work))
    print("  relink_images      :", relink_images(work))
    print("  purge_purple_swatch:", purge_purple_swatch(work))
    out = output_dir() / (Path(idml).stem + "-refined.idml")
    repack_idml(work, out)
    print(f"  wrote {out}")
    rep = preflight.run_preflight(out)
    for c in rep["checks"]:
        print(f"    {'PASS' if c['ok'] else 'FAIL'}  {c['check']}  {c['detail']}")
    print(f"  overall: {'PASS' if rep['ok'] else 'NEEDS WORK'}")
    return 0


def cmd_ingest(folder: str | None, section: str | None) -> int:
    if not folder or not section:
        print("--ingest needs --from <folder> and --section <agency|constraint|mediation>")
        return 2
    import re as _re
    import shutil as _sh
    token = {"agency": "raw-agency", "constraint": "social-constraint",
             "mediation": "mediation"}.get(section.lower())
    if not token:
        print("--section must be one of: agency, constraint, mediation")
        return 2
    src = Path(folder)
    if not src.is_dir():
        print(f"not a folder: {folder}")
        return 2
    labeled = ROOT / "images" / "labeled"
    labeled.mkdir(parents=True, exist_ok=True)
    exts = {".jpg", ".jpeg", ".png", ".webp"}
    used = [int(m.group(1)) for f in labeled.iterdir()
            if (m := _re.match(r"a(\d+)", f.name))]
    nxt = (max(used) + 1) if used else 1
    added = []
    for p in sorted(src.iterdir()):
        if p.suffix.lower() in exts:
            stem = _re.sub(r"[^a-z0-9]+", "-", p.stem.lower()).strip("-")[:48]
            name = f"a{nxt:02d}-{token}-{stem}{p.suffix.lower()}"
            _sh.copy2(p, labeled / name)
            added.append(name)
            nxt += 1
    print(f"[ingest] added {len(added)} image(s) as '{section}' to images/labeled:")
    for a in added:
        print("  ", a)
    print("Next: python scripts/build.py --book   (or run.bat)")
    return 0


def cmd_setup() -> int:
    print("[setup] auto-install local dependencies (token-free, no cloud)")
    deps = ["reportlab", "pillow", "pypdf", "pymupdf"]
    rc = subprocess.call([sys.executable, "-m", "pip", "install", "--quiet", *deps])
    print(f"  python deps: {'OK' if rc == 0 else 'FAILED'}")
    sys.path.insert(0, str(SCRIPTS))
    from agents.ollama_client import MODELS, OllamaClient
    client = OllamaClient(url=OLLAMA_URL)
    if not client.available():
        print(f"  Ollama not reachable at {OLLAMA_URL} — start `ollama serve`, then re-run --setup to pull models")
        return rc
    installed = set(client.models())
    need = [fast for fast, _best in MODELS.values() if fast not in installed]
    if not need:
        print("  Ollama models: all present")
    for model in need:
        print(f"  pulling {model} ...")
        subprocess.call(["ollama", "pull", model])
    return rc


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
    sys.path.insert(0, str(SCRIPTS))
    from agents.local_guard import enforce_local_only
    enforce_local_only()  # no cloud, no tokens: block any non-local connection

    parser = argparse.ArgumentParser(description="Visceral Theory of Sight publication engine.")
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--setup", action="store_true", help="auto-install deps + pull local models")
    g.add_argument("--check", action="store_true", help="environment + asset preflight, no output")
    g.add_argument("--preflight", action="store_true", help="audit + save a preflight report")
    g.add_argument("--skills", action="store_true", help="list available layout/copy skills")
    g.add_argument("--skill", metavar="NAME", help="run a named skill (with --idml or --text)")
    g.add_argument("--book", action="store_true", help="reportlab book + InDesign handoff artifacts")
    g.add_argument("--final", action="store_true", help="11-image refined final document")
    g.add_argument("--gen-idml", dest="gen_idml", action="store_true", help="generate editable IDML [phase 2]")
    g.add_argument("--refine-idml", dest="refine_idml", action="store_true", help="chain layout skills into one convention-correct IDML (with --idml)")
    g.add_argument("--autofix", action="store_true", help="loop preflight + skills until green (with --idml)")
    g.add_argument("--read-preflight", dest="read_preflight", metavar="PDF", help="parse an InDesign preflight report PDF")
    g.add_argument("--ingest", action="store_true", help="copy a local folder of images into the book (with --from and --section)")
    g.add_argument("--copy", action="store_true", help="regenerate copy via local Ollama [phase 3]")
    g.add_argument("--package", action="store_true", help="build standalone executable (PyInstaller)")
    g.add_argument("--all", action="store_true", help="book + final")
    parser.add_argument("--idml", metavar="PATH", help="IDML file for --preflight / layout --skill")
    parser.add_argument("--text", help="text input for a copy --skill")
    parser.add_argument("--from", dest="from_dir", metavar="DIR", help="source folder for --ingest")
    parser.add_argument("--section", help="agency|constraint|mediation (for --ingest)")
    args = parser.parse_args(argv)

    if args.setup:
        return cmd_setup()
    if args.check:
        return cmd_check()
    if args.preflight:
        return cmd_preflight(args.idml)
    if args.skills:
        return cmd_skills()
    if args.skill:
        return cmd_skill(args.skill, args.idml, args.text)
    if args.refine_idml:
        return cmd_refine_idml(args.idml)
    if args.autofix:
        return cmd_autofix(args.idml)
    if args.read_preflight:
        return cmd_read_preflight(args.read_preflight)
    if args.ingest:
        return cmd_ingest(args.from_dir, args.section)
    if args.book:
        return cmd_book()
    if args.final:
        return cmd_final()
    if args.gen_idml:
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
