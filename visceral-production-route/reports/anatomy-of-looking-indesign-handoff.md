# Anatomy of Looking — InDesign Handoff

Handoff notes for taking *The Visceral Theory of Sight* ("The Anatomy of Looking"
issue) from the generated proof into a final InDesign export. Keep it short,
verify before you trust it, and do not call the issue done until preflight and a
visual page check have both run.

## Verified Production Geometry

These values match the committed proof PDF and
`indesign-preflight-safe-generator-report.json`. Treat them as the source of truth
for the current export route:

- Trim: **US Letter landscape, 279.4 mm x 215.9 mm** (11 x 8.5 in).
- Bleed: **3.175 mm** all sides (MediaBox includes bleed; TrimBox is the trim).
- Pages: **50**, facing pages on.
- Swatches: **[Black]** and **[Paper]** only (CMYK / no stray RGB).
- Linked assets: **64** scanned locally. See the open item below before exporting.

> Heads-up: older notes (`critical-process-notes.md`, the root geometry report,
> and `templates/idml-indesign-affinity-handoff.md`) still describe an A4 portrait
> route. The shipped proof is the US Letter landscape route. Reconcile those docs
> before anyone treats A4 as current.

## Scripts In This Package

- `templates/indesign-build-preflight-safe.jsx` — builds the 50-page landscape
  `.indd` against the Digital Publishing profile and exports
  `the-visceral-theory-of-sight-50pp-indesign-auto.pdf`.
- `templates/indesign-build-full-layout.jsx` — full linked layout builder; saves
  the native `.indd` and exports `.idml` for Affinity.
- `templates/indesign-preflight-autofix-current-doc.jsx` — autofix pass for the
  active document.
- `templates/indesign-fix-overset-text.jsx` — overset-text repair for the active
  document.
- `templates/codex-caption-injection.jsx` — caption injection from the manifest.

## Preflight Checklist (do this before export)

Run InDesign preflight on the open `.indd` and clear every item before you export
anything final. The Digital Publishing profile should flag:

- **missing links** — every placed image must be present and up to date; relink
  anything that shows modified or missing.
- **overset text** — no hidden or clipped copy. If preflight reports overset text,
  run `templates/indesign-fix-overset-text.jsx`, then re-check; thread or copy-edit
  whatever it cannot resolve automatically.
- **bleed** — full-bleed images must run past the trim to the 3.175 mm bleed line;
  confirm the document bleed is set, not faked with oversized frames.
- color space — CMYK only, swatches limited to [Black] and [Paper].
- **fonts** — all fonts present and not substituted; no missing or pink-highlighted
  glyphs. Embed or package fonts for the final handoff.

## PDF Visual Check (do this after export)

Export a PDF and inspect page edges before sign-off. Page through every spread and
look for:

- trim and **bleed** holding on full-bleed spreads (no white slivers at the edge).
- gutters and inner margins — nothing important lost in the binding creep.
- folios present and correct on body pages.
- captions not crowding the image or each other, and no cropped caption text.
- backmatter readable — the Image Source Register must stay legible at final size.
- no source filenames, Adobe Stock IDs, or rights notes leaking under front-of-book
  images; those belong only in the backmatter register.

## Open Items To Resolve Before Final Export

- **Asset count: 64 (resolved).** Three plates (A02–A04) were deleted from the
  source set, so 64 is the canonical count. The manifest, web proof, source
  register, generated reports, and tests are reconciled to 64. Plate numbering
  keeps its original labels (A01, A05–A67) with a gap where A02–A04 were.
- **Citations.** Scholarly references are still marked to verify; replace
  placeholders with exact bibliographic records before public release.
- **Rights.** Confirm every Adobe Stock and Unsplash asset against a real license,
  and verify local/generated provenance, before print or public upload.
