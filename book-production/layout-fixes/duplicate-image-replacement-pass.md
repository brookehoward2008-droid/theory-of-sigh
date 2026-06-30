# Duplicate Image Replacement Pass

Source PDF: `eyes_layout_preserved_author_credit_no_pink_guides_black_gutters_52pg.pdf`
Output proof: `eyes_layout_preserved_duplicate_images_replaced_captioned_52pg.pdf`

## Brooke instruction

Choose the placements and replace images that are used multiple times.

## Scope

- Replaced visible image artwork on pages: 12, 20, 21, 29, 31, 41, 43, 45
- Updated mini-captions on those pages so they no longer carry old image labels
- Preserved existing text, page numbers, author credit, black gutters, and removed pink guides
- Preserved 52-page count
- No full layout rebuild

## Method

This pass updated the page-level form XObject image resource `/Im0` for each selected page form, rather than covering the page with a flat overlay. This keeps existing text and page design elements above the image.

Each uploaded image was center-cropped to the target frame aspect and prepared at the target 300 ppi pixel dimensions for the existing placed frame. Original high-resolution Unsplash source files are still preferred when available, but this proof uses the uploaded images Brooke supplied.

## Replacements

| Page | Replaced visible repeat | New approved image | New visible label |
|---:|---|---|---|
| 12 | `a24-raw-agency-amir-geshani-2jh8d3chnec-unsplash.jpg` | `cole-keister-D6zQt8NfIq4-unsplash.jpeg` | `A68 / SOCIAL CONSTRAINT` / `Cole Keister` |
| 20 | `aris-rovas-jui9RSZdPVU-unsplash (1).jpg` | `evilicio-inc-RSgWh0jmGbo-unsplash.jpeg` | `A69 / SOCIAL CONSTRAINT` / `Evilicio Inc.` |
| 21 | `valentin-lacoste-8PafowRW8mE-unsplash.jpeg` | `elias-maurer-sSpLu7IPC8g-unsplash.jpeg` | `A70 / SOCIAL CONSTRAINT` / `Elias Maurer` |
| 29 | repeated blindfold/roses image | `liliya-grek-OaPOg0EAD2w-unsplash.jpeg` | `A71 / MEDIATION` / `Liliya Grek` |
| 31 | `a20-mediation-alex-bracken-l1sjo7tmvec-unsplash.jpg` | `sunny-ng-oLpSNDeE83A-unsplash.jpeg` | `A72 / MEDIATION` / `Sunny Ng` |
| 41 | repeated blindfold/roses image | `nikolay-hristov-5RUfRn7x-ME-unsplash.jpeg` | `A73 / SYNTHESIS` / `Nikolay Hristov` |
| 43 | `aris-rovas-jui9RSZdPVU-unsplash (1).jpg` | `thea-hdc-hwD_SVnZu7Q-unsplash.jpeg` | `A74 / SYNTHESIS` / `Thea` |
| 45 | `daniel-apodaca-uriAVs6oi3Y-unsplash (2).jpg` | `andrea-farao-SgMC5xjjsfU-unsplash (2).jpeg` | `A75 / SYNTHESIS` / `Andrea Farao` |

## Production rule

The native InDesign/source layout must receive the same image choices and source-register updates before final print export. This proof is a surgical PDF-level correction for review.
