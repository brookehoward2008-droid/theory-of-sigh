# The Anatomy of Looking - InDesign Handoff

## Protected Base

- Original setup preserved: `output/indesign/the-visceral-theory-of-sight-50pp-preflight-safe.indd`
- New working base: `output/indesign/the-anatomy-of-looking-50pp-indesign-base.indd`
- New IDML companion: `output/indesign/the-anatomy-of-looking-50pp-indesign-base.idml`

The new files are copies of the earlier preflight-safe InDesign setup. The original remains untouched.

## Production Target

- Format: landscape facing pages
- Trim: 279.4 mm x 215.9 mm
- Bleed: 3.175 mm on all sides
- Structure: 50-page magazine route
- Structure: facing-page magazine issue with clean captions, article sections, references, and source register

## Caption Rule

Front-of-book captions stay clean:

- image label
- visual group
- short editorial caption

Original filenames, visual groups, rights notes, and source traces are preserved in the back-matter image source register.

## Publication-Flaw Checklist

Before publication:

- Run the automated test suite and the HTML/source preflight checks.
- Open the live/local HTML proof in a browser and visually inspect article rhythm, captions, text fit, source-register readability, and image crop behavior.
- Run InDesign preflight for missing links, overset text, bleed, color space, and missing fonts.
- Confirm every image has an A-number, visual group, and source-register entry.
- Confirm no original filename or rights note crowds a front-of-book caption.
- Confirm references and citation marks resolve to the back matter.
- Export a PDF and inspect page edges, captions, backmatter, and full-bleed image spreads.
- Use any available visual inspection tool before approval: browser screenshot checks for the web proof, PDF render checks for exported pages, and InDesign preflight for the `.indd`.
- Keep the original preflight-safe `.indd` as the rollback file.
