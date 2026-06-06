# Brooke InDesign Automation Design

## Purpose

Build an original, typed editorial automation system for Brooke's InDesign
magazine workflow. The system supplements the existing Python-generated
magazine build without replacing it until equivalent behavior is proven.

The primary authoring language is TypeScript. Each production command compiles
to standalone, ExtendScript-safe JSX that can run from InDesign's Scripts panel
or through the existing Windows COM automation route.

## Evidence And Licensing Boundaries

| Reference | License evidence | Allowed use in this project |
| --- | --- | --- |
| `VictorStanger/InDesign-Automation-Suite` | Repository `LICENSE` says proprietary and all rights reserved. | Workflow categories, expected inputs, failure cases, and command naming only. No source code copying or redistribution. |
| `docsforadobe/Types-for-Adobe` | npm package and repository identify the package as MIT. | Direct dependency for InDesign API typing and autocomplete. Typings remain a reference layer; runtime code must remain ExtendScript-compatible. |
| `RolandDreger/indesign-set-up-baseline-grid` | README identifies CC BY 3.0 AT. | Baseline-grid interaction concepts may inform an original implementation with attribution. |
| `mark1bean/bin-packing-for-illustrator-and-indesign` | Repository `LICENSE` is MIT. | Optional reference for packing concepts, scoring choices, guide-defined bins, spacing, margins, and rotation. Any reused substantial implementation must retain the MIT notice. |

The Brooke scripts are original implementations. The project will not vendor,
copy, or translate Victor Stanger's proprietary JSX source.

## Architecture

The automation layer lives beside the current Python generators:

```text
indesign-automation/
  package.json
  tsconfig.json
  src/
    core/
      context.ts
      diagnostics.ts
      guards.ts
      measurements.ts
      reporting.ts
    editorial/
      bilingual-precision-layout.ts
      apply-master-by-content.ts
      apply-master-by-chapter.ts
      clean-empty-paragraphs.ts
      prevent-orphan-subtitles.ts
      adjust-title-spacing.ts
      import-markdown-auto.ts
      convert-heading1-to-chapter.ts
      convert-normal-to-body.ts
      format-chapters.ts
      configure-publication-preflight.ts
      configure-baseline-grid.ts
      pack-page-items.ts
    commands/
      *.ts
    brooke-automation.ts
  dist/
    *.jsx
  tests/
    *.test.cjs
```

`src/editorial/` contains behavior without automatic execution.
`src/commands/` contains small executable entry points that validate the active
document, request options when needed, run one behavior, and write a report.
`dist/` contains the standalone JSX files used by InDesign.

The existing `scripts/build_visceral_book.py` remains the magazine constructor.
Its current `configurePublicationPreflight(doc)` behavior becomes a typed
editorial command and remains in the Python-generated JSX until the typed
replacement is proven in the real document.

## Runtime Compatibility

- Target InDesign 2026 on the current Windows machine.
- Use `types-for-adobe` as compile-time API reference.
- Compile with `module: "none"` and ES3-compatible output.
- Do not depend on Node APIs at runtime.
- Do not emit CommonJS, ESM, promises, classes, spread syntax, or other syntax
  unsupported by ExtendScript.
- Bundle each command into one JSX file with a stable command header.

## Command Contract

Every command follows the same lifecycle:

1. Confirm InDesign has an active document.
2. Validate required paragraph styles, parent pages, stories, or selections.
3. Build a diagnostic plan without editing the document.
4. In dry-run mode, write the plan and stop.
5. In apply mode, perform guarded edits inside one undoable script operation.
6. Write a UTF-8 JSON-compatible report with counts, warnings, and failures.
7. Leave unresolved or ambiguous content unchanged.

Commands must never silently invent a style, parent-page assignment, language
mapping, chapter boundary, or footnote target when the document evidence is
ambiguous.

## Required Editorial Commands

### Bilingual Precision Layout

Create or repair paired facing-page text flows using explicit left-language and
right-language style mappings. Report story pairing, overset state, missing
frames, and coordinate differences. It must not assume that every facing spread
is bilingual.

### Parent Page Automation

- `apply-master-by-content`: assign a parent page when a page contains an
  explicitly mapped paragraph style or label.
- `apply-master-by-chapter`: assign chapter-opening and continuation parents
  from verified chapter-heading paragraphs.

The command reports conflicts instead of choosing when multiple rules match.

### Paragraph And Title Cleanup

- Remove empty paragraphs only around configured heading styles.
- Apply `keepWithNext` and paragraph keep options to prevent orphan subtitles.
- Normalize title spacing through paragraph styles, not manual line breaks.
- Convert imported Heading 1 and Normal styles to configured editorial styles.

All cleanup commands preserve text content unless their specific transformation
requires a verified replacement.

### Markdown Import

Import a constrained Markdown subset:

- Heading 1 through Heading 3
- Paragraphs
- Ordered and unordered lists
- Emphasis markers
- Footnote references and definitions

The importer first converts Markdown into a neutral intermediate model, then
creates InDesign paragraphs and applies mapped styles. Unsupported syntax is
reported and preserved as plain text rather than discarded.

### Footnote Conversion And Migration

Convert verified bracket references to footnotes and migrate footnotes between
paired stories only when markers and definitions form a one-to-one mapping.
Mismatched, duplicate, or missing references stop that story's conversion and
appear in diagnostics.

### Chapter Formatting

Apply chapter styles, parents, title spacing, opening-page rules, and continuation
rules from a single configuration object. A compact ScriptUI dialog may expose
apply mode and chapter mapping after the non-UI behavior is tested.

### Publication Preflight

Apply the original `Anatomy of Looking - Color Landscape` profile:

- Retain checks for missing or modified graphics, missing fonts, overset text,
  image resolution, and bleed/trim hazards.
- Disable the mismatched monochrome-plate rule.
- Disable the mismatched portrait-orientation rule.
- Preserve intentional color and US Letter landscape facing pages.

The command reports the active profile and every intentionally disabled rule.

### Baseline Grid

Configure baseline start, increment, and type-area alignment from explicit
measurements. Parent-page transfer is supported only after the destination
parent is identified. The implementation is original and includes attribution
to Roland Dreger's interaction concepts.

### Optional Page-Item Packing

Arrange selected page items within explicit page or guide-defined regions.
Default behavior preserves rotation and reading order. Experimental rotation,
random packing, and progressive compaction are opt-in and must report their
settings. This command is not used for article pages unless the user explicitly
chooses it, because editorial rhythm is more important than maximum density.

### Advanced Diagnostics

Inspect and report:

- Page count, size, orientation, facing-page state, and bleed
- Active publication preflight profile
- Missing or modified links
- Overset stories and frames
- Missing fonts
- Paragraph-style drift and overrides
- Parent-page assignments
- Unpaired bilingual stories
- Orphan-risk subtitles
- Footnote-reference mismatches
- TOC styles, bookmarks, and hyperlinks

Diagnostics are read-only by default.

## Configuration

Configuration is a plain TypeScript object compiled into the command:

```ts
interface BrookeEditorialConfig {
  dryRun: boolean;
  reportFolder: string;
  styles: {
    chapter: string;
    subtitle: string;
    body: string;
    importedHeading1: string;
    importedNormal: string;
  };
  parentRules: Array<{
    paragraphStyle: string;
    parentName: string;
  }>;
  bilingual?: {
    leftLanguage: string;
    rightLanguage: string;
    leftStyle: string;
    rightStyle: string;
  };
}
```

The first implementation uses project defaults. Later, a JSON-like config
generator can produce publication-specific command builds without adding a
runtime JSON dependency to ExtendScript.

## Error Handling And Safety

- Mutating commands run through `app.doScript` with one undo group.
- A command aborts before mutation when required styles or parents are absent.
- Item-level failures are caught, reported, and do not hide the command result.
- Reports include command name, start/end times, dry-run state, edited counts,
  skipped counts, warnings, and errors.
- No command deletes page items, stories, styles, links, or footnotes unless its
  documented purpose explicitly requires it and the target is verified.

## Testing And Verification

### Static Tests

- TypeScript compiles without errors against `types-for-adobe`.
- Generated JSX contains no module wrappers or unsupported syntax.
- Each named command is generated.
- License and attribution notices are present where required.
- The publication-preflight command contains the intentional color-landscape
  profile and both mismatched-rule exceptions.

### Fixture Tests

Text-only test fixtures validate Markdown parsing, reference matching, rule
selection, diagnostic aggregation, and packing geometry outside InDesign.

### InDesign Runtime Tests

Run commands against a duplicate test document:

1. Run dry mode and inspect the report.
2. Run apply mode.
3. Run InDesign preflight.
4. Verify missing links, overset text, fonts, bleed, color, orientation, TOC,
   bookmarks, and hyperlinks.
5. Export PDF and inspect rendered pages visually.

The current 50-page magazine remains the final integration fixture. Work is not
complete until the repository's publication QA gate passes.

## Delivery Sequence

1. Establish TypeScript compiler, typings, command contract, and diagnostics.
2. Implement publication preflight and advanced diagnostics first.
3. Implement safe paragraph cleanup, subtitle keeps, and title spacing.
4. Implement parent-page and chapter automation.
5. Implement Markdown import and style conversion.
6. Implement footnote conversion and migration.
7. Implement bilingual precision layout.
8. Implement baseline-grid and optional page-item packing.
9. Run the full magazine integration and publication QA gate.

