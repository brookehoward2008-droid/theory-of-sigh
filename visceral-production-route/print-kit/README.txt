THE VISCERAL THEORY OF SIGHT — Print-finishing kit
==================================================
Keeps your 50pp InDesign layout exactly as-is. It only refines the type,
applies Chris Larson's two fixes, and exports a digital-print-ready PDF.

WHAT'S IN HERE
  refine-and-export-print-pdf.jsx  <- the main script (type + widows + body + PDF)
  add-photos.jsx                   <- appends new photos as full-bleed pages
  Document Fonts/                  <- Gloock + Cormorant Garamond (open-licensed)

ONE-TIME FONT SETUP (fixes the "generic / missing fonts" problem)
  Easiest: copy the "Document Fonts" folder so it sits RIGHT NEXT TO your
  .indd file (same folder). InDesign auto-activates fonts placed there — no
  install needed, and they travel with the package.
  Alternative: activate "Cormorant Garamond" from Adobe Fonts (free with your
  Creative Cloud) and double-click Gloock-Regular.ttf to install it.

STEPS
  1. Open thevisceraltheoryofsight50pp.indd in InDesign.
  2. File > Scripts > Other Script...  ->  run  refine-and-export-print-pdf.jsx
     It will:
       - swap the generic default face for the locked pairing:
           Gloock  (headlines / large display type)
           Cormorant Garamond  (body, labels, captions; italic where italic)
         Sizes, colours, leading and positions are untouched, so the layout
         does not move.
       - fix the typographic WIDOWS Chris flagged (pp. 3,5,8,9,27,28,29,39,40 and
         anywhere else) by tightening that paragraph's tracking until the lone
         last word pulls up. Any it can't resolve are reported "widen by hand."
       - restore BODY SIZE on pages 40+ (Chris's note) back to the book's 10.4pt.
       - export  <docname>-PRINT.pdf  next to your document as PDF/X-4
         (CMYK, with your 9pt document bleed and crop marks) — ready to send to
         an online printer.
  3. Read the summary alert. If it lists missing fonts, finish the font setup
     above and run it again.

ADDING MORE PHOTOS
  Run  add-photos.jsx,  pick one or more image files, and each is appended as a
  new full-bleed page (with an editable caption) at the END of the book. Drag
  them into position in the Pages panel, then re-run the refine+export script so
  the new captions get the right font and a fresh PDF is produced.
  Want photos dropped onto specific existing pages instead? Tell me the page
  numbers and send the image files and I'll script exact placement.

TUNING (open the .jsx in a text editor; CONFIG block at the top)
  DISPLAY_MIN_PT   - point size at/above which type is treated as a headline
                     (-> Gloock). Lower it to send more subheads to Gloock.
  BODY_TARGET_PT   - the body size pages 40+ are restored to (default 10.4).
  WIDOW_TRACK_FLOOR- how far tracking may tighten to clear a widow.

NOTES
  - Images stay linked and RGB in the document; the PDF/X-4 export converts them
    to CMYK for print via the export profile. Keep the original image files with
    the document (Package... bundles them).
  - Nothing in this kit alters page count, image placement, or geometry.
