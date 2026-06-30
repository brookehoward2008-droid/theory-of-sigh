# PR6 300 DPI Relink Summary

Source audit: `current-book-300-effective-dpi-audit.md`
Matrix: `pr6-300dpi-relink-matrix.csv`

## Current proof failure count

- 30 failing placements
- 26 unique embedded photo objects needing replacement or relink

## PR6 match buckets

- 15 high-confidence ID matches to PR6 `images/print-300dpi/`
- 4 medium-confidence slug matches that require visual verification
- 7 items with no exact PR6 print-source match

## High-confidence PR6 relink candidates

These have matching creator/slug identity and should be visually verified before relinking:

- `maria-budanova-pristavskaya-dk8OHEIfT9o` -> `images/print-300dpi/a01-raw-agency-maria-budanova-pristavskaya-dk8oheift9o-unsplash.jpg`
- `aris-rovas-jui9RSZdPVU` -> `images/print-300dpi/a41-mediation-aris-rovas-jui9rszdpvu-unsplash.jpg`
- `valentin-lacoste-8PafowRW8mE` -> `images/print-300dpi/a58-mediation-valentin-lacoste-8pafowrw8me-unsplash.jpg`
- `amir-geshani-2jh8d3chnec` -> `images/print-300dpi/a05-raw-agency-amir-geshani-2jh8d3chnec-unsplash.jpg`
- `brunxs-monochrome-spniqdcpi9u` -> `images/print-300dpi/a07-raw-agency-brunxs-monochrome-spniqdcpi9u-unsplash.jpg`
- `drew-dizzy-graham-ctkgzjtmjqu` -> `images/print-300dpi/a09-raw-agency-drew-dizzy-graham-ctkgzjtmjqu-unsplash.jpg`
- `yadu-nandlal-xpnvhcurfs` -> `images/print-300dpi/a19-raw-agency-yadu-nandlal-xpnvhcurfs-unsplash.jpg`
- `alex-bracken-l1sjo7tmvec` -> `images/print-300dpi/a42-mediation-alex-bracken-l1sjo7tmvec-unsplash.jpg`
- `arielle-allouche-h82rqe4gria` -> `images/print-300dpi/a44-mediation-arielle-allouche-h82rqe4gria-unsplash.jpg`
- `camila-quintero-franco-mc852jack1g` -> `images/print-300dpi/a46-mediation-camila-quintero-franco-mc852jack1g-unsplash.jpg`
- `elvis-kaiser-rqbk5ez6qa0` -> `images/print-300dpi/a48-mediation-elvis-kaiser-rqbk5ez6qa0-unsplash.jpg`
- `flaviu-costin-vr-sbbcwklc` -> `images/print-300dpi/a50-mediation-flaviu-costin-vr-sbbcwklc-unsplash.jpg`

## Medium-confidence matches

These have likely matching IDs but require visual confirmation because the filename spelling differs:

- `daniel-apodaca-uriAVs6oi3Y` -> `images/print-300dpi/a59-mediation-daniela-podacauri-avs6oi3y-unsplash.jpg`
- `jan-kopriva-n3BtiYgu5NI` -> `images/print-300dpi/a02-raw-agency-janko-priva-n3btiygu5ni-unsplash.jpg`

## No exact PR6 match

These must be selected manually before relinking:

- generated/local unknown-source blindfold/roses image
- `a18-social-constraint-adobestock-730927617.jpg`
- `a06-social-constraint-adobestock-1040196803.jpg`
- `a07-social-constraint-adobestock-1044937382.jpg`
- `a08-social-constraint-adobestock-1225023891.jpg`
- `a10-social-constraint-adobestock-1462135790.jpg`

## Production rule

Do not rename current book references blindly. Relink visually confirmed source files first, export a fresh proof, rerun the 300 effective dpi audit, then update the back matter/source register.
