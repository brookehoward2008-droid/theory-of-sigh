# Publication Engine

A single, local, token-free orchestrator for building *The Visceral Theory of
Sight* — layout/PDF in pure Python, optional copy generation through a local
Ollama server (no API key, no per-token cost), and packaging into a standalone
executable.

## What runs where

| Capability | Where it runs | Notes |
|---|---|---|
| Book + PDF + InDesign handoff scripts | anywhere with Python | pure Python; no Adobe app required |
| Editable IDML (layers/links/parents/TOC) | anywhere with Python | phase 2 |
| Copy / caption / poem generation | **your machine**, via local Ollama | token-free; needs `ollama serve` + a pulled model |
| Native InDesign automation | **your machine**, with InDesign | optional (ExtendScript / InDesign Server) |
| `.exe` / app build | **your OS** (Windows exe on Windows) | PyInstaller |

> This repo is built and tested in a remote Linux container that has **no Adobe
> apps and no Ollama**. The engine is written so the same commands behave
> predictably on your machine, where those tools live. The engine only ever
> reads this repo and files you provide — it does not scan your drive unless you
> run it locally and point it at a folder.

## Usage

```bash
python scripts/build.py --check      # environment + asset preflight, no output
python scripts/build.py --book       # reportlab book + InDesign handoff artifacts
python scripts/build.py --final      # 11-image refined final document
python scripts/build.py --idml       # editable InDesign IDML (layers/links/TOC)  [phase 2]
python scripts/build.py --copy       # regenerate section copy via local Ollama   [phase 3]
python scripts/build.py --package    # build a standalone executable (PyInstaller)
python scripts/build.py --all        # book + final
```

## Local agents (token-free)

The engine talks to a local [Ollama](https://ollama.com) server — the same
`mistral:latest` model the OpenClaw gateway uses — so generation costs nothing
and needs no key.

```bash
ollama serve
ollama pull mistral:latest
python scripts/build.py --check      # confirms "Ollama: reachable; models: ..."
```

Client: `scripts/agents/ollama_client.py` (`OllamaClient`, plus `dark_caption`
and `section_poem` helpers in the book's house voice). If Ollama is not
running, the build falls back to the hand-written copy already in the repo.

## Packaging into an executable

```bash
pip install pyinstaller
pyinstaller --onefile --name visceral-engine scripts/build.py
# build a Windows .exe on Windows; a macOS binary on macOS
```

## Roadmap

1. **Engine skeleton** — orchestrator + local Ollama client + `--check`. ✅
2. **Editable IDML generator** — the *good-version* design as a convention-correct
   InDesign file: real layers, linked images, parent pages, generated TOC;
   labels and the stray purple stroke removed.
3. **Ollama copy agents** — dark-poetry section copy, the epigraph poem, and
   distinct per-image captions, generated locally.
4. **Package** — PyInstaller spec + this guide kept current.
