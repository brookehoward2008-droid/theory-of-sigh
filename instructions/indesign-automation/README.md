# InDesign automation — what to use, and how it's wired here

You've been bouncing book drafts through chat LLMs and getting unusable layouts.
The fix is to stop asking a language model to *imagine* a layout and instead drive
**Adobe's real InDesign engine** with your fixed grid, fonts, and assets. There
are three official routes for that. This repo now ships an integration for the
one that fits automated, repeatable book production.

## The three routes (and which one to pick)

| Route | What it is | Runs where | Best for | In this repo |
|-------|-----------|-----------|----------|--------------|
| **Firefly Services — InDesign API** | Cloud REST API (`indesign.adobe.io`): data merge, custom scripts, rendition (PDF/PNG/JPEG), document info, PDF↔INDD | Adobe's cloud — **no local InDesign needed** | Headless, repeatable, scriptable book builds and proofs | ✅ `scripts/indesign_api/` |
| **UXP plugin** | Modern desktop extension (panel + JS) for InDesign 2023 (v18.5)+ | Your machine, inside the InDesign app | A button-driven panel for hands-on editorial work | Recommended next step (see below) |
| **Adobe Express add-on** | Web design surface; the MCP server config you provided wires it into Claude Code | Your machine (via `npx`) | Social/web derivatives, not print-grade book layout | ✅ `.mcp.json` |

**Recommendation for the 50pp book:** the **InDesign API** is the spine. It's
deterministic (Adobe's engine, not an LLM guess), it reuses the assets you already
have (the caption manifest CSV, the JSX scripts, the grid geometry), and it
produces the actual end product — a print-ready PDF — without you clicking through
InDesign by hand. Add the **UXP plugin** later if you want an in-app panel for
manual touch-ups. The **Express add-on** is for web/social spin-offs, not the book.

> ExtendScript `.jsx` (what `visceral-production-route/templates/*.jsx` uses today)
> still works, but Adobe is steering everyone to UXP for desktop and to the
> InDesign API for automation. Your existing `.jsx` logic isn't wasted — it can be
> packaged as a **custom script** and run *through* the InDesign API (see below).

## What got installed

- **`scripts/indesign_api/`** — a dependency-free Python client + CLI for the
  Firefly Services InDesign API (stdlib only, no `pip install`).
- **`.env.example`** — template for your Adobe credentials (copy to `.env`).
- **`.mcp.json`** — the Adobe Express add-on MCP server you provided.

## Install locally

> ⚠️ This session runs in an ephemeral cloud container, **not on your machine**.
> I can't reach your local InDesign, Creative Cloud, or laptop filesystem from
> here. So "install locally" = pull this branch on your own machine and run the
> steps below there. Everything needed is committed to the repo.

### 1. Get Firefly Services InDesign API credentials
1. Go to the [Adobe Developer Console](https://developer.adobe.com/console) with an
   account that has Firefly Services / InDesign API entitlement.
2. Create (or open) a project and add the **InDesign API**.
3. Add a **Server-to-Server (OAuth)** credential. Note the **Client ID**,
   **Client Secret**, and the **scopes** listed on the credential page.

### 2. Configure this repo
```bash
cp .env.example .env
# edit .env and paste your Client ID + Client Secret
set -a && . ./.env && set +a   # load the vars into your shell
```

### 3. Smoke-test the connection
```bash
python -m scripts.indesign_api.cli app-versions
```
A JSON list of InDesign engine versions means auth + connectivity work.

### 4. Install the Express add-on MCP (optional)
The `.mcp.json` in this repo registers it for Claude Code in this project. On your
machine you can instead add it globally:
```bash
claude mcp add adobe-express-add-on -- npx @adobe/express-developer-mcp@latest --yes
```

## Desktop ExtendScripts (Scripts Panel)

ExtendScripts (`.jsx`) aren't UXP/CEP plugins — they install into InDesign's
**Scripts Panel** user folder and appear under **Window → Utilities → Scripts**
in every InDesign session. Two installers handle this. Both run **on your own
machine** (macOS/Windows, where InDesign lives — they can't touch a headless
cloud box) and copy into every `Version */<locale>/Scripts/Scripts Panel` folder
they find, so every InDesign version (and any `do script` automation) can reach
the scripts. Both support `--dry-run`, `--indesign-root`, and `--create-missing`.

### Bundled scripts → `install_indesign_scripts.py`
Installs everything in [`indesign-scripts/`](../../indesign-scripts/) (currently
`SpeedUpInDesign.jsx` — Gregor Fellenz's fast-settings toggle). Add more `.jsx`
files to that folder and re-run.

```bash
python scripts/install_indesign_scripts.py            # install all bundled scripts
python scripts/install_indesign_scripts.py --dry-run  # preview
python scripts/install_indesign_scripts.py --source path/to/MyScript.jsx
```

### Third-party easybook → `install_easybook.py`
[serjant/easybook-indesign-plugin](https://github.com/serjant/easybook-indesign-plugin)
is a class/yearbook layout helper (`School.jsx`). It's **not vendored** here (the
upstream ships no license), so this installer fetches it at run time.

```bash
python scripts/install_easybook.py                 # fetch from GitHub + install
python scripts/install_easybook.py --prefer both   # also install the compiled .jsxbin
python scripts/install_easybook.py --source ./clone  # install from a local clone
```

> Heads-up: these are interactive desktop scripts (they open dialogs), so they
> belong in the Scripts Panel. They won't run unattended through the cloud
> InDesign API custom-scripts route without first removing their UI prompts.

## How it maps to the book pipeline

Every endpoint is asynchronous: POST a job → get a `jobId` + `statusUrl` → poll
until `succeeded` / `partial_success` / `failed`. The client handles the polling.
Input assets are passed as **pre-signed URLs** the API downloads; outputs are
**pre-signed PUT URLs** the API uploads results to.

| Book task | Endpoint | Client method / CLI |
|-----------|----------|---------------------|
| Inject captions from `data/visceral-caption-manifest.csv` into a tagged template | `/v3/merge-data` | `client.data_merge(...)` |
| Export the 50pp layout to a press-ready PDF | `/v3/create-rendition` | `render` / `client.create_rendition(...)` |
| Preflight: find missing links, missing fonts, page geometry | `/v3/document-info` | `doc-info` / `client.document_info(...)` |
| Turn an existing proof PDF back into editable INDD/IDML | `/v3/convert-pdf-to-indesign` | `convert-pdf` / `client.convert_pdf_to_indesign(...)` |
| Run your existing `.jsx` automation server-side | `/v3/scripts` then `/v3/{id}/{name}` | `client.submit_custom_script(...)` → `client.execute_custom_script(...)` |

### Example: render a document to PDF
```bash
python -m scripts.indesign_api.cli render \
  --asset-url  "https://<presigned-GET>/the-visceral-theory-of-sight-50pp.indd" \
  --target     the-visceral-theory-of-sight-50pp.indd \
  --output-url "https://<presigned-PUT>/book.pdf" \
  --output-name book.pdf \
  --use-document-bleeds --pdf-preset "PDF/X-4:2008"
```

### Example: programmatic use
```python
from scripts.indesign_api import Config, InDesignClient

client = InDesignClient(Config.from_env())
event = client.document_info(
    assets=[client.asset("https://.../book.indd", "book.indd")],
    target_document="book.indd",
    links=True, fonts=True,
)
print(event["status"], event.get("data", {}).get("fontInfo"))
```

## Honest constraints
- **Credentials are yours.** The client reads them from env vars and never stores
  them in the repo. `.env` is gitignored.
- **Network.** This cloud session may not be allowed to reach `indesign.adobe.io`
  or Adobe IMS. The client is written to the documented contract; run the smoke
  test from your own machine to confirm live access.
- **Assets need URLs.** The API pulls inputs and pushes outputs over pre-signed
  URLs (S3/Azure/Dropbox style). You supply those; the client wires them in.

## Endpoint reference (v3, `https://indesign.adobe.io`)
- `POST /v3/merge-data` — data merge (CSV → INDD/PDF/PNG/JPEG)
- `POST /v3/merge-data-tags` — list a template's data-merge tags
- `POST /v3/create-rendition` — render to PDF/PNG/JPEG
- `POST /v3/document-info` — pages, links, fonts, page items, text stories
- `POST /v3/convert-pdf-to-indesign` — PDF → INDD/IDML (ZIP output)
- `POST /v3/remap-links` — swap file links for AEM URLs
- `POST /v3/scripts` · `GET /v3/scripts` · `GET|DELETE /v3/scripts/{name}` — manage custom scripts
- `POST /v3/{script_id}/{script_name}` — execute a custom script
- `GET /v3/app-versions` — available InDesign engine versions
- `GET /v3/status/{id}` — poll any job's status

Auth: `Authorization: Bearer <S2S token>` + `x-api-key: <client id>`.
