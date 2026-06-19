# InDesign Publication Build

A production, style-driven InDesign build of *The Visceral Theory of Sight* —
51 pages, A3 landscape (420×297 mm), facing pages, 3.175 mm bleed, CMYK, with a full
**paragraph + character style system** so every text element is globally editable.

## Files
- `scripts/build_indesign_publication.py` — generator. Copies the 64 images
  into `visceral-production-route/assets/` and writes the build script below.
- `visceral-production-route/templates/indesign-publication-build.jsx` — the
  ExtendScript that builds the document inside InDesign.

## One-time setup
1. **Fonts** — install / Adobe-activate the faces named in `FONTS` at the top of
   `build_indesign_publication.py`. Defaults:
   - Display: **Gloock**
   - Body: **Spectral** (swap to your locked choice — Fraunces / Lora / Outfit /
     an Adobe Font — by editing one line)
   - Labels / captions: **Work Sans**
   The vendored TTFs for Gloock / Work Sans (and Cormorant, Crimson) are in
   `assets/fonts/`; double-click to install, or activate equivalents from Adobe Fonts.

## Build steps
1. Generate (copies images + writes the JSX):
   ```
   python scripts/build_indesign_publication.py
   ```
2. In InDesign: **File ▸ Scripts ▸ Other Script…** and run
   `visceral-production-route/templates/indesign-publication-build.jsx`.
   It creates the swatches, the style system, the master (rich-black ground +
   automatic folio), all 51 pages with images placed and copy flowed into
   style-tagged frames, then exports `.indd`, `.idml`, and a print PDF to
   `visceral-production-route/output/indesign/`.
3. Read the preflight summary it prints (missing fonts / links / overset).
4. **File ▸ Package…** to produce the printer hand-off bundle (INDD + `Links/`
   + `Document Fonts/` + PDF + instructions report).

## Style system (named `VT / …`)
**Paragraph:** Body, Body Lead, Section Number, Section Title, Section Blurb,
Eyebrow, Caption, Folio, Epigraph Title, Epigraph Credit, Epigraph Verse,
Epigraph Reply, Intro Headline, Pull Quote, Title, Subtitle, TOC Header,
TOC Entry, Colophon, Source Entry, Works Consulted, Closing.
**Character:** Italic, Caption Label, TOC Folio, Accent Gold, Accent Teal.
**Swatches (CMYK):** VT Rich Black, VT Cream, VT Gold, VT Slate, VT Teal.

Edit any style once and it updates everywhere — that is the point of the
style-driven build.

## Notes
- Colors are CMYK process for print; your printer may fine-tune exact values.
- The generator runs anywhere (pure text emission); the `.jsx` requires InDesign.
- The script is authored for InDesign's scripting DOM; verify the preflight
  summary on first run and adjust frame geometry to taste in InDesign.
