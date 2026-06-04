# Final 11-Image Merge Audit

Generated for `layout refine.indd` handoff on 2026-06-03.

## Data Merge Package

- CSV: `visceral-production-route/assets/final-11-image-merge/manifest.csv`
- Images: `visceral-production-route/assets/final-11-image-merge/`
- Row count: 11 image rows plus header
- Image path strategy: bare filenames in `@ImageFile`, with the CSV stored beside the copied image files so InDesign Data Merge can resolve them directly.

## Alias Notes

The requested `_2.jpg` files were not present as separate source files in the school asset folder during this pass. To keep the user's requested manifest names intact, these four source images were copied into the merge package under the requested `_2.jpg` aliases:

- `see-plus-NP3s9BYOqAc-unsplash.jpg` -> `see-plus-NP3s9BYOqAc-unsplash_2.jpg`
- `igor-rand-GIW9CCL3HxA-unsplash.jpg` -> `igor-rand-GIW9CCL3HxA-unsplash_2.jpg`
- `nina-zeynep-guler-fjJiVSX-BxM-unsplash.jpg` -> `nina-zeynep-guler-fjJiVSX-BxM-unsplash_2.jpg`
- `enesh-taganova-IoXGIDqVqYQ-unsplash (1).jpg` -> `enesh-taganova-IoXGIDqVqYQ-unsplash (1)_2.jpg`

## Verification Rules

- Every `@ImageFile` value in `manifest.csv` must exist in the same folder as the CSV.
- Captions stay descriptive and do not claim source facts, dates, licenses, or scholarly support.
- Unsplash filenames indicate likely source type only; source URLs and current license status still need manual verification before final print or public upload.
- `CodeGraph` was not initialized in this project, so code-structure inspection used direct file reads for this pass.
