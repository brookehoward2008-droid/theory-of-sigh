# Agent Handoff — Visceral Theory of Sight publication engine

Continue this build **locally and free** (local Ollama, no cloud, no API
tokens). Cloud usage is exhausted; a local agent (OpenClaw + Ollama, or Codex
via Ollama) takes over from here. This file is the brief.

## Golden rules (do not break)

1. **No cloud, no tokens.** Local Ollama only. The engine enforces this at
   runtime (`scripts/agents/local_guard.py` → `enforce_local_only()` blocks any
   non-loopback socket). `python scripts/build.py --check` must show
   `socket guard active : True` and `cloud-SDK scan : clean`.
2. **OneDrive is read-only; write only to the local PC.** OneDrive holds source
   assets you may READ. All NEW/generated material saves to a LOCAL folder.
   `scripts/paths.py` enforces it (`assert_not_onedrive`). Set
   `VTS_OUTPUT_DIR` to a local folder (e.g. `C:\VTS-output`) and, if reading
   OneDrive assets, `VTS_ASSETS_DIR` to that OneDrive folder.
3. **Target design = `good_version.4.pdf`** — dark cover, poem, dark poetic
   copy, real InDesign TOC, new images, tight geometric/gestalt layout.
   Keep the copy + back matter layout. Produce an **editable IDML**
   (named layers, linked images, parent pages, generated TOC) — *not* a
   flattened file. Remove the template labels and the stray purple stroke.

## Run it locally (free)

```bat
:: 1. open the token-free local API window
Start "Open Local Ollama API Environment.bat"   (launcher #6)
:: 2. ensure Ollama is up (models already installed)
ollama serve
:: 3. point outputs at a LOCAL folder (never OneDrive)
set VTS_OUTPUT_DIR=C:\VTS-output
set VTS_ASSETS_DIR=C:\Users\toddl\OneDrive\...\visceral-theory of sight assets   :: read-only
:: 4. sanity check
python scripts\build.py --check
```

`--check` must report: deps OK, images found, `socket guard active : True`,
cloud-SDK scan clean, and an `output (local write)` path that is **not** under
OneDrive.

## What is already built (committed on branch `claude/gallant-ptolemy-k0zpgr`)

| File | Purpose |
|---|---|
| `scripts/build.py` | Orchestrator: `--check/--book/--final/--idml/--copy/--package/--all`; enforces offline guard at startup |
| `scripts/agents/ollama_client.py` | Local Ollama client; per-task model routing (`OllamaClient.for_task`), `generate`, `embed`, `dark_caption`, `section_poem` |
| `scripts/agents/local_guard.py` | `enforce_local_only()` (blocks non-local sockets), `scan_for_cloud_sdks()` |
| `scripts/paths.py` | OneDrive-read / local-write rule: `assets_dir()`, `output_dir()`, `assert_not_onedrive()`, `preflight_dir()` |
| `PUBLICATION-ENGINE.md` | Usage + per-task model table + what-runs-where |

## Local model map (all token-free; you have every one installed)

| Task | model (fast) | quality option |
|---|---|---|
| prose / poem / captions | `mistral:latest` | `llama3.3:70b` |
| code (JSX / HTML / Python) | `qwen2.5-coder:7b` | `qwen3-coder:30b` |
| reasoning / layout planning | `deepseek-r1:32b` | — |
| embeddings (image↔copy match) | `nomic-embed-text:latest` | — |

Use `OllamaClient.for_task("code", quality="quality")` to pin the heavy model.

## What to build next (in order) — let the local code model implement these

### A. Skills layer — advanced layout + copy editing  (`scripts/skills/`)
A registry of small named operations the engine lists and runs.

- `scripts/skills/__init__.py`: `@skill(name, kind, summary)` decorator,
  `SKILLS` dict, `list_skills()`, `run_skill(name, **kw)`.
- `scripts/skills/layout.py` (edit an unpacked IDML dir):
  - `unpack_idml(idml, dest)` / `repack_idml(src_dir, out)` — note: IDML zips
    must store `mimetype` **first, uncompressed**.
  - `purge_purple_swatch(idml_dir)` — find violet swatches (CMYK M>60,C>40,Y<30
    or RGB purple), repoint any `StrokeColor` using them to `Swatch/None`, then
    drop the now-unreferenced `<Color>` defs.
  - `relink_images(idml_dir, links_dir="Links")` — rewrite every
    `LinkResourceURI="file:..."` to `file:Links/<filename>` (kills the dead
    `C:/Users/toddl/OneDrive/...` paths; point at a LOCAL links folder).
  - `ensure_layers(idml_dir, names=["background","images","type","captions"])`,
    `rebuild_toc(idml_dir)` — later.
- `scripts/skills/copy.py` (via `OllamaClient.for_task("prose")`, offline =
  leave text unchanged): `refine_copy(text, instruction)`, `generate_poem(
  section, motif)`, `regenerate_captions(...)`.
- Wire `--skills` (list) and `--skill NAME ...` into `build.py`.

### B. Preflight artifacts — auto-saved, auto-loaded  (`scripts/preflight.py`)
- `audit_idml(idml)` → dict (geometry/orientation, layers, master count, fonts,
  images placed/linked/embedded, TOCStyle, violet swatches + stroke usage).
- `run_preflight(idml_path=None)` → builds a report (assets + offline guard +
  ollama plan + idml audit + pass/fail checks), **writes to
  `paths.preflight_dir()`**: `preflight-<ts>.json`, `latest.json`, `latest.md`.
- `load_latest()` reads `latest.json` so each refinement pass starts from the
  last known state (preflight ↔ editing stay in harmony).
- Acceptance: after a run, `<VTS_OUTPUT_DIR>/preflight/latest.json` exists and
  its `checks` reflect: layered>1, 0 embedded images, master pages present,
  TOC style present, 0 purple-stroke uses.

### C. Phase 2 — editable IDML generator  (biggest task)
Rebuild `good_version.4` as a convention-correct IDML:
- geometry: landscape ~286 mm pages (match `good_version.4`); facing pages.
- named layers, linked images (local `Links/`), parent/master pages,
  paragraph/character styles, a generated TOC.
- run skills A on it: purge purple, relink, ensure layers, rebuild TOC.
- write the `.idml` to `paths.output_dir()`.

### D. Phase 3 — copy agents
Generate the epigraph poem + dark-poetry section copy + distinct per-image
captions with the prose model; keep the existing back matter.

## Inputs / assets

- **Design reference:** `good_version.4.pdf` (25 spreads = 50 pp; outlined text;
  it is a *proof*, not editable). Its colophon says "Set in Helvetica and
  Times" — that's the generic-font render to replace with the real type.
- **Source IDMLs** (uploaded): landscape, **one layer**, default fonts, image
  links point to a dead `C:/Users/toddl/OneDrive/...` path → must relink to a
  local `Links/` folder.
- **Images:** `images/labeled/` (62 in repo) + OneDrive assets (read-only).
- **Missing vs target:** multiple layers, real custom fonts, a generated TOC
  bound to styles, and the **poem** page (add it).

## Definition of done

- `python scripts/build.py --check` all green locally (guard on, cloud-SDK
  clean, output path local).
- The generated `.idml` opens in InDesign with named layers, locally-linked
  images, parent pages, a generated TOC, no template labels, no purple box.
- Every output lives under the local `VTS_OUTPUT_DIR`; **nothing** is written to
  OneDrive.

## First commands for the local agent

```bat
python scripts\build.py --check
:: then implement A (skills) → B (preflight) → C (IDML) → D (copy),
:: committing after each, running --check between steps.
```
