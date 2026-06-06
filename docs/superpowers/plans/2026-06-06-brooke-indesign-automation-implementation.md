# Brooke InDesign Automation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build original, typed, standalone InDesign JSX commands for Brooke's editorial workflow using Types-for-Adobe.

**Architecture:** Add an isolated `indesign-automation/` TypeScript project beside the existing Python magazine generator. Shared global-namespace core and editorial modules compile separately with each command entry point so every output is a standalone ExtendScript-safe JSX file.

**Tech Stack:** TypeScript, `types-for-adobe`, Node.js build/test scripts, ExtendScript-safe JSX, Python publication tests, InDesign 2026 COM runtime.

---

### Task 1: Typed Project And Command Builder

**Files:**
- Create: `indesign-automation/package.json`
- Create: `indesign-automation/tsconfig.base.json`
- Create: `indesign-automation/scripts/build-commands.cjs`
- Create: `indesign-automation/tests/build-commands.test.cjs`

- [ ] Write a failing test requiring all requested command names and standalone JSX outputs.
- [ ] Run the test and confirm failure because the typed project does not exist.
- [ ] Add package configuration and the command-aware build script.
- [ ] Install pinned TypeScript and Types-for-Adobe dependencies.
- [ ] Run the test and confirm the build contract passes.

### Task 2: Shared Safety And Diagnostic Runtime

**Files:**
- Create: `indesign-automation/src/core/runtime.ts`
- Create: `indesign-automation/src/core/reporting.ts`
- Create: `indesign-automation/src/editorial/diagnostics.ts`
- Create: `indesign-automation/src/commands/debug_advanced.ts`
- Test: `indesign-automation/tests/source-contract.test.cjs`

- [ ] Write failing tests for active-document guards, dry-run reporting, undo grouping, and diagnostic fields.
- [ ] Run tests and confirm expected failures.
- [ ] Implement the core runtime, report writer, and read-only diagnostic command.
- [ ] Compile and run the contract tests.

### Task 3: Publication And Editorial Cleanup Commands

**Files:**
- Create: `indesign-automation/src/editorial/publication.ts`
- Create: `indesign-automation/src/editorial/text-cleanup.ts`
- Create: command entry points for publication preflight, empty-paragraph cleanup, orphan subtitle prevention, and title spacing.
- Test: `indesign-automation/tests/source-contract.test.cjs`

- [ ] Write failing tests for the color-landscape profile and cleanup command contracts.
- [ ] Implement original guarded behaviors.
- [ ] Compile and verify standalone outputs.

### Task 4: Parent, Chapter, And Import Commands

**Files:**
- Create: `indesign-automation/src/editorial/parents.ts`
- Create: `indesign-automation/src/editorial/import-conversion.ts`
- Create: command entry points for parent assignment, chapter assignment, Markdown import, Heading 1 conversion, Normal conversion, and chapter formatting.
- Test: `indesign-automation/tests/source-contract.test.cjs`

- [ ] Write failing source/output contract tests.
- [ ] Implement explicit mapping and conflict-reporting behavior.
- [ ] Compile and verify standalone outputs.

### Task 5: Footnote, Bilingual, Baseline, And Packing Commands

**Files:**
- Create: `indesign-automation/src/editorial/footnotes.ts`
- Create: `indesign-automation/src/editorial/bilingual.ts`
- Create: `indesign-automation/src/editorial/layout-tools.ts`
- Create: command entry points for footnote conversion/migration, bilingual precision layout, baseline grid, and page-item packing.
- Test: `indesign-automation/tests/source-contract.test.cjs`

- [ ] Write failing source/output contract tests.
- [ ] Implement original guarded behaviors and required attribution notices.
- [ ] Compile and verify standalone outputs.

### Task 6: Magazine Integration And Publication QA

**Files:**
- Modify: `scripts/build_indesign_preflight_safe.py`
- Modify: `tests/test_final_document_build.py`
- Create: `indesign-automation/README.md`

- [ ] Update the existing generator report to name the color-landscape profile and intentional exceptions.
- [ ] Add publication tests for the typed automation outputs.
- [ ] Run `npm test`, `npm run build`, and the full Python test suite.
- [ ] Run the generated publication-preflight and diagnostic JSX against the magazine duplicate.
- [ ] Run InDesign preflight and visually inspect the exported PDF.

