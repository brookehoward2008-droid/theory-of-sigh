# Bundled InDesign ExtendScripts

Drop any `.jsx` / `.jsxbin` you want available in InDesign into this folder, then
install them all into your local Scripts Panel with:

```bash
python scripts/install_indesign_scripts.py
```

The installer copies every script here into every InDesign "Scripts Panel" user
folder it finds (all versions/locales, macOS or Windows). They then appear under
**Window → Utilities → Scripts** in InDesign — double-click to run.

## Scripts in this folder

| Script | What it does | Author |
|--------|--------------|--------|
| `SpeedUpInDesign.jsx` | Toggles InDesign into fast settings (typical display, no live screen drawing, preflight off, no page thumbnails, no URL auto-update, no preview generation). Run again to restore. | Gregor Fellenz — publishingx.de, inspired by Erica Gamet / InDesignSecrets |

Each script keeps its original author/attribution header. These are interactive
desktop scripts (they may open dialogs), so they belong in the Scripts Panel, not
the headless cloud InDesign API route.
