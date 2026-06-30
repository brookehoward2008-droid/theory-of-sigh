# PR #6 Image Asset Recovery Plan

Branch: `book-image-assets-from-pr6`
Source branch: `claude/gallant-ptolemy-k0zpgr`
Base branch: `main`

## Purpose

Recover the useful image asset work from PR #6 while preserving the current book structure.

This branch is image-production focused. It should not carry over the full PR #6 layout rebuild.

## Print requirement

Digital print target: 300 effective dpi at final placed size.

This means every placed image must be checked by page placement, crop, and scale. File metadata alone is not enough.

## Valuable PR #6 image work

PR #6 contains a cleaner print asset route:

- `images/print-300dpi/`
- A01-A59 print-image sequence
- original-style source filenames for many Unsplash assets
- cleaner section ordering by visual group

## Safety rule

Do not accept PR #6 A-code renumbering as final until page placements are checked against the current layout-preserved proof.

Final register target:

`original filename -> stable book image ID -> page placement -> effective dpi -> back matter entry`

## Next action

Build a page-by-page 300 effective dpi audit from the current PDF proof, then import only the image files that fail or need original-name recovery.
