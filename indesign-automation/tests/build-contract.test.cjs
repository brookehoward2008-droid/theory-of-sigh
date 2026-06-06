const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");

const root = path.resolve(__dirname, "..");

const requiredCommands = [
  "bilingual_precision_layout",
  "migrate_footnotes_between_docs",
  "convert_brackets_to_footnotes",
  "apply_master_by_content",
  "apply_master_by_chapter",
  "clean_empty_paragraphs",
  "prevent_orphan_subtitles",
  "adjust_title_spacing",
  "import_markdown_auto",
  "convert_heading1_to_chapter",
  "convert_normal_to_body",
  "format_chapters_gui",
  "configure_publication_preflight",
  "configure_baseline_grid",
  "pack_page_items",
  "debug_advanced",
];

test("project declares pinned typed Adobe build dependencies", () => {
  const pkg = JSON.parse(fs.readFileSync(path.join(root, "package.json"), "utf8"));
  assert.equal(pkg.scripts.build, "node scripts/build-commands.cjs");
  assert.match(pkg.devDependencies.typescript, /^\d+\.\d+\.\d+$/);
  assert.match(pkg.devDependencies["types-for-adobe"], /^\d+\.\d+\.\d+$/);
});

test("every requested command has a TypeScript entry point", () => {
  for (const command of requiredCommands) {
    assert.ok(
      fs.existsSync(path.join(root, "src", "commands", `${command}.ts`)),
      `missing command source: ${command}`,
    );
  }
});

test("every requested command builds to a standalone ExtendScript-safe JSX", () => {
  for (const command of requiredCommands) {
    const output = path.join(root, "dist", `${command}.jsx`);
    assert.ok(fs.existsSync(output), `missing JSX output: ${command}`);
    const source = fs.readFileSync(output, "utf8");
    assert.match(source, /Brooke Adobe Automation/);
    assert.match(source, /runCommand/);
    assert.doesNotMatch(source, /\brequire\s*\(/);
    assert.doesNotMatch(source, /\bimport\s+/);
    assert.doesNotMatch(source, /\bexport\s+/);
    assert.doesNotMatch(source, /=>/);
    assert.doesNotMatch(source, /\bclass\s+/);
  }
});

test("publication preflight preserves intentional color landscape output", () => {
  const output = fs.readFileSync(
    path.join(root, "dist", "configure_publication_preflight.jsx"),
    "utf8",
  );
  assert.match(output, /Anatomy of Looking - Color Landscape/);
  assert.match(output, /ADBE_CMYPlates/);
  assert.match(output, /ADBE_PageSizeOrientation/);
  assert.match(output, /preflightWorkingProfile/);
});

test("reference-license boundaries are documented", () => {
  const notice = fs.readFileSync(path.join(root, "THIRD_PARTY_NOTICES.md"), "utf8");
  assert.match(notice, /VictorStanger\/InDesign-Automation-Suite/);
  assert.match(notice, /not copied/i);
  assert.match(notice, /types-for-adobe/i);
  assert.match(notice, /Roland Dreger/i);
  assert.match(notice, /mark1bean/i);
});
