# Production Polish Checklist

Working branch: `book-production-polish`

Protected branch: `book-recovery-do-not-delete`

Main branch: leave untouched until the book proof is approved.

## Primary production target

- Book: **The Visceral Theory of Sight**
- Current proof target: `eyes_layout_preserved_photo_update_52pg.pdf`
- Trim: **11.25 in x 8.75 in**
- Pages: **52**
- Output purpose: digital print file for ordering books
- Layout rule: preserve the original tight editorial layout. Do not rebuild the book from code unless Brooke asks for a rebuild.

## Page-level polish tasks

### Copy and typography

- Fix smashed/mixed words throughout the PDF.
- Fix typographic widows on pages 03, 05, 08, 09, 27, 28, 29, 39, and 40.
- Keep body type consistent from page 40 onward.
- Avoid changing frame rhythm unless required to correct a widow or overset issue.
- Preserve the original visual hierarchy and editorial tension.

### TOC

- Keep the TOC InDesign-style.
- Generate or update TOC from the actual section starts.
- Do not fake a new TOC layout if the original TOC is visually correct.
- Verify page numbers after photo replacements and final back matter changes.

### Photos

- Keep the new real-photo replacements only where non-photo imagery was removed.
- Do not replace strong existing photo pages.
- Check replacement pages visually: 7, 8, 15, 17, 20, 21, 22, 24, 43, 45, and 46.
- Maintain existing image frame crops as much as possible.

### Image reference register

- Rebuild image source register so each image code aligns with the correct placed image.
- Remove duplicate references if an image was removed.
- Do not leave `creator not verified` or `rights verify` in the final public/order copy unless intentionally kept as a private proof warning.
- Confirm Unsplash filenames, Adobe Stock identifiers, and local creator notes.

### Bibliography / works consulted

- Build a clean Works Consulted section.
- Remove placeholder language such as incomplete licenses, page ranges pending, or source verification warnings from the final order proof unless the proof is explicitly marked private.
- Keep citations consistent with the body references.

### Final print checks

- Confirm page count is even: 52 pages.
- Confirm trim is 11.25 in x 8.75 in.
- Confirm no crop marks, color bars, slug, or printer metadata marks remain in the order file.
- Confirm no cut-off text on the last page.
- Confirm all placed images are photographs.
- Confirm no obvious low-resolution image is used as a full-page feature.

## Do not run as final master

The repo contains scripts that generate new PDFs and layout routes. These are useful for audit or support, but not the final layout master unless Brooke explicitly approves.

Do not use a generated 50-page US Letter or A4 route as the final print-order PDF.

## Next branch work

1. Add or reference the current final proof files.
2. Update repo documentation to distinguish original layout proof from generated build routes.
3. Align build constants only after the actual final InDesign/PDF target is confirmed.
