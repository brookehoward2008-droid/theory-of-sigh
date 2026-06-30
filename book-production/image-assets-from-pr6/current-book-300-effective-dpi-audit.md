# Current Book 300 Effective DPI Audit

PDF audited: `eyes_layout_preserved_photo_update_52pg.pdf`

## Print rule

Digital print target: **300 effective dpi at final placed size**. A 0.5 dpi tolerance is used for PDF coordinate rounding. This audit uses the image native pixel dimensions divided by the actual placed size in inches. File metadata dpi is not treated as proof of print readiness.

## Summary

- Pages audited: 52
- Meaningful photo placements audited: 45
- Unique meaningful embedded photo objects: 41
- Placement pass count: 15
- Placement fail count under 300 effective dpi: 30
- Unique photo objects needing replacement/relink: 26

## Placement status counts

- FAIL_UNDER_200_EFFECTIVE_DPI: 25
- PASS_300_EFFECTIVE_DPI: 15
- FAIL_200_TO_239_EFFECTIVE_DPI: 2
- FAIL_240_TO_299_EFFECTIVE_DPI: 3

## Pages with failing placed photos

01 (1), 02 (1), 07 (1), 08 (1), 09 (1), 10 (1), 11 (1), 12 (1), 14 (1), 16 (1), 18 (1), 19 (1), 21 (1), 23 (1), 24 (1), 25 (1), 27 (1), 28 (1), 29 (1), 31 (1), 33 (1), 35 (1), 37 (1), 39 (1), 40 (1), 41 (1), 42 (1), 43 (1), 45 (1), 46 (1)

## Highest priority failures

| Page | Temp ID | Xref | Candidate filename | Native px | Placed in | Effective dpi | Required px for 300 | Shortfall |
|---:|---|---:|---|---:|---:|---:|---:|---:|
| 25 | PHOTO-023 | 199 | a08-social-constraint-adobestock-1225023891.jpg | 1091x848 | 11.251x8.745 | 97.0 | 3376x2624 | +2285x+1776 |
| 12 | PHOTO-011 | 139 | a24-raw-agency-amir-geshani-2jh8d3chnec-unsplash.jpg | 1192x932 | 11.25x8.796 | 106.0 | 3375x2639 | +2183x+1707 |
| 27 | PHOTO-025 | 208 | a10-social-constraint-adobestock-1462135790.jpg | 1192x932 | 11.25x8.796 | 106.0 | 3375x2639 | +2183x+1707 |
| 40 | PHOTO-037 | 269 | aris-rovas-jui9RSZdPVU-unsplash (1).jpg | 1192x932 | 11.25x8.796 | 106.0 | 3375x2639 | +2183x+1707 |
| 33 | PHOTO-030 | 238 | a26-mediation-arielle-allouche-h82rqe4gria-unsplash.jpg | 1259x980 | 11.242x8.751 | 112.0 | 3373x2626 | +2114x+1646 |
| 16 | PHOTO-015 | 161 | a36-raw-agency-drew-dizzy-graham-ctkgzjtmjqu-unsplash.jpg | 1270x988 | 11.248x8.75 | 112.9 | 3375x2626 | +2105x+1638 |
| 07 | PHOTO-006 | 88 | aris-rovas-jui9RSZdPVU-unsplash (1).jpg | 1293x1006 | 11.243x8.748 | 115.0 | 3374x2625 | +2081x+1619 |
| 18 | PHOTO-006 | 88 | aris-rovas-jui9RSZdPVU-unsplash (1).jpg | 1293x1006 | 11.243x8.748 | 115.0 | 3374x2625 | +2081x+1619 |
| 43 | PHOTO-006 | 88 | aris-rovas-jui9RSZdPVU-unsplash (1).jpg | 1293x1006 | 11.243x8.748 | 115.0 | 3374x2625 | +2081x+1619 |
| 37 | PHOTO-034 | 255 | a38-mediation-elvis-kaiser-rqbk5ez6qa0-unsplash.jpg | 1338x1041 | 11.247x8.75 | 119.0 | 3374x2626 | +2036x+1585 |
| 39 | PHOTO-036 | 264 | a44-mediation-flaviu-costin-vr-sbbcwklc-unsplash.jpg | 1350x1054 | 11.25x8.783 | 120.0 | 3376x2636 | +2026x+1582 |
| 02 | PHOTO-002 | 25 | a01-mediation-a-photograph-of-an-attractive-woman-with-a-wh... | 1530x1194 | 11.254x8.782 | 136.0 | 3377x2635 | +1847x+1441 |
| 41 | PHOTO-002 | 25 | a01-mediation-a-photograph-of-an-attractive-woman-with-a-wh... | 1530x1194 | 11.254x8.782 | 136.0 | 3377x2635 | +1847x+1441 |
| 09 | PHOTO-008 | 108 | valentin-lacoste-8PafowRW8mE-unsplash.jpeg | 1546x1198 | 11.292x8.75 | 136.9 | 3388x2625 | +1842x+1427 |
| 14 | PHOTO-013 | 153 | a30-raw-agency-brunxs-monochrome-spniqdcpi9u-unsplash.jpg | 1546x1198 | 11.289x8.748 | 136.9 | 3387x2625 | +1841x+1427 |
| 01 | PHOTO-001 | 16 | maria-budanova-pristavskaya-dk8OHEIfT9o-unsplash (1).jpeg | 1545x1198 | 11.284x8.75 | 136.9 | 3386x2625 | +1841x+1427 |
| 21 | PHOTO-019 | 183 | valentin-lacoste-8PafowRW8mE-unsplash.jpeg | 1545x1198 | 11.284x8.75 | 136.9 | 3386x2625 | +1841x+1427 |
| 23 | PHOTO-021 | 191 | a06-social-constraint-adobestock-1040196803.jpg | 1545x1198 | 11.284x8.75 | 136.9 | 3386x2625 | +1841x+1427 |
| 28 | PHOTO-026 | 212 | a20-mediation-alex-bracken-l1sjo7tmvec-unsplash.jpg | 1545x1198 | 11.284x8.75 | 136.9 | 3386x2625 | +1841x+1427 |
| 31 | PHOTO-026 | 212 | a20-mediation-alex-bracken-l1sjo7tmvec-unsplash.jpg | 1545x1198 | 11.284x8.75 | 136.9 | 3386x2625 | +1841x+1427 |
| 35 | PHOTO-032 | 247 | a32-mediation-camila-quintero-franco-mc852jack1g-unsplash.jpg | 1545x1198 | 11.284x8.75 | 136.9 | 3386x2625 | +1841x+1427 |
| 45 | PHOTO-040 | 296 | daniel-apodaca-uriAVs6oi3Y-unsplash (2).jpg | 1800x1406 | 11.25x8.788 | 160.0 | 3375x2637 | +1575x+1231 |
| 19 | PHOTO-017 | 173 | yadunandlal-XPnvhcUR-fs-unsplash.jpeg | 900x1195 | 5.451x7.238 | 165.1 | 1636x2172 | +736x+977 |
| 42 | PHOTO-038 | 282 | daniel-apodaca-uriAVs6oi3Y-unsplash (2).jpg | 836x1195 | 5.064x7.239 | 165.1 | 1520x2172 | +684x+977 |
| 08 | PHOTO-007 | 102 | daniel-apodaca-uriAVs6oi3Y-unsplash (2).jpg | 1793x384 | 9.728x2.083 | 184.3 | 2919x626 | +1126x+242 |
| 24 | PHOTO-022 | 195 | a07-social-constraint-adobestock-1044937382.jpg | 2055x1008 | 9.738x4.777 | 211.0 | 2922x1434 | +867x+426 |
| 10 | PHOTO-009 | 117 | a18-social-constraint-adobestock-730927617.jpg | 1150x1528 | 5.449x7.241 | 211.0 | 1635x2173 | +485x+645 |
| 29 | PHOTO-027 | 218 | a01-mediation-a-photograph-of-an-attractive-woman-with-a-wh... | 1352x1795 | 5.451x7.237 | 248.0 | 1636x2172 | +284x+377 |
| 46 | PHOTO-041 | 300 | jan-kopriva-n3BtiYgu5NI-unsplash (1).jpeg | 2445x1199 | 9.741x4.777 | 251.0 | 2923x1434 | +478x+235 |
| 11 | PHOTO-010 | 128 | a24-raw-agency-amir-geshani-2jh8d3chnec-unsplash.jpg | 1196x1932 | 4.479x7.236 | 267.0 | 1344x2171 | +148x+239 |

## Notes

- The audit excludes FlateDecode masks/overlays and small rule graphics; it counts only meaningful JPEG/DCT photo placements over the area threshold.
- Several repeated full-page overlays at 300 dpi are mask/texture objects and are not treated as source photographs.
- The `original_name_candidate` column comes from the earlier original-filename register draft, so rows marked for manual review should not be used as final back-matter citations yet.
- A true final pass still needs source-file relinking in InDesign or the production builder, then a re-export and repeat audit.
