# Book Recovery Notes — Preserve This Work

This branch is a safe recovery branch for **The Visceral Theory of Sight**.

## Current recovery intent

Preserve the original tight editorial layout and update only the necessary production items:

- keep the original InDesign/page rhythm as the visual master
- update the book with the new real-photo replacements only where non-photo imagery was removed
- fix copy defects, smashed/mixed words, widows, back matter, image reference alignment, and bibliography
- avoid full layout regeneration unless Brooke explicitly requests it

## Current print proof target

Use the layout-preserved photo-update PDF as the current proof target from the ChatGPT working session:

- file: `eyes_layout_preserved_photo_update_52pg.pdf`
- trim target: `11.25 in x 8.75 in`
- page target: `52 pages`
- purpose: digital print file for ordering books

## Safety rules

Do not delete the local project folder.

Do not use destructive cleanup, hard reset, recursive removal, or force-push repair steps without a separate verified backup branch.

Do not treat generated PDFs/code-first rebuilds as the layout master unless Brooke approves that direction.

## Repo scan warnings

The repository currently contains multiple automation/build routes. Some scripts generate new PDFs, InDesign JSX files, reports, and asset ledgers. Some cleanup helpers remove generated folders under `visceral-production-route` before rebuilding. That may be acceptable for generated artifacts, but it is not safe to use as the master repair path for the final editorial book without a backup and a confirmed file target.

The existing automation route also contains older trim/page assumptions, including US Letter landscape and A4 handoff language. The current recovery target is the 11.25 x 8.75 in / 52-page layout-preserved book proof.

## Recommended next repair steps

1. Keep this branch as the recovery checkpoint.
2. Locate the original packaged `.indd`, `.idml`, links folder, and latest layout-preserved PDF.
3. Add the final PDF/package artifacts only after confirming the exact files.
4. Create a separate working branch for repairs, such as `book-production-polish`.
5. Make changes surgically: copy fixes, image-source register, bibliography, and exact page-level replacements only.
