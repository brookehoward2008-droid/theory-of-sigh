namespace BrookeAutomation {
  function eachParagraph(doc: Document, visit: (paragraph: Paragraph) => void): void {
    var s: number;
    var p: number;
    for (s = 0; s < doc.stories.length; s++) {
      var story = doc.stories.item(s);
      for (p = story.paragraphs.length - 1; p >= 0; p--) visit(story.paragraphs.item(p));
    }
  }

  function paragraphStyleName(paragraph: Paragraph): string {
    try {
      var applied: any = paragraph.appliedParagraphStyle;
      return typeof applied === "string" ? applied : String(applied.name);
    } catch (error) { return ""; }
  }

  function trimmed(value: string): string {
    return value.replace(/[\r\n\t ]+/g, "");
  }

  function countMissingLinks(doc: Document): number {
    var count = 0;
    var i: number;
    for (i = 0; i < doc.links.length; i++) {
      if (String(doc.links.item(i).status).indexOf("LINK_MISSING") >= 0) count++;
    }
    return count;
  }

  function countOverset(doc: Document): number {
    var count = 0;
    var i: number;
    for (i = 0; i < doc.textFrames.length; i++) if (doc.textFrames.item(i).overflows) count++;
    return count;
  }

  export function debugAdvanced(ctx: Context): void {
    var doc = ctx.doc;
    detail(ctx, "pages=" + doc.pages.length);
    detail(ctx, "facingPages=" + doc.documentPreferences.facingPages);
    detail(ctx, "pageWidth=" + doc.documentPreferences.pageWidth);
    detail(ctx, "pageHeight=" + doc.documentPreferences.pageHeight);
    detail(ctx, "links=" + doc.links.length);
    detail(ctx, "missingLinks=" + countMissingLinks(doc));
    detail(ctx, "oversetTextFrames=" + countOverset(doc));
    detail(ctx, "paragraphStyles=" + doc.paragraphStyles.length);
    detail(ctx, "parentPages=" + doc.masterSpreads.length);
    detail(ctx, "tocStyles=" + doc.tocStyles.length);
    detail(ctx, "hyperlinks=" + doc.hyperlinks.length);
    try { detail(ctx, "preflightProfile=" + doc.preflightOptions.preflightWorkingProfile); } catch (error) { warn(ctx, "Unable to read preflight profile."); }
  }

  export function configurePublicationPreflight(ctx: Context): void {
    var profileName = "Anatomy of Looking - Color Landscape";
    var profile: PreflightProfile;
    try {
      profile = app.preflightProfiles.itemByName(profileName);
      profile.name;
    } catch (error) {
      profile = app.preflightProfiles.itemByName("kDigPubProfileName").duplicate();
      profile.name = profileName;
    }
    detail(ctx, "Profile target: " + profileName);
    detail(ctx, "Intentional exception: ADBE_CMYPlates");
    detail(ctx, "Intentional exception: ADBE_PageSizeOrientation");
    if (ctx.report.dryRun) return;
    profile.description = "Color landscape magazine profile retaining critical publication checks.";
    profile.preflightProfileRules.itemByName("ADBE_CMYPlates").flag = 1699890274;
    profile.preflightProfileRules.itemByName("ADBE_PageSizeOrientation").flag = 1699890274;
    ctx.doc.preflightOptions.preflightWorkingProfile = profile;
    ctx.doc.preflightOptions.preflightOff = false;
    changed(ctx, 1);
  }

  export function cleanEmptyParagraphs(ctx: Context): void {
    var headingPattern = /chapter|title|heading|subtitle/i;
    eachParagraph(ctx.doc, function (paragraph: Paragraph): void {
      if (trimmed(String(paragraph.contents)) !== "") return;
      var previous = "";
      var next = "";
      try {
        var story: any = paragraph.parentStory;
        var index: number = (paragraph as any).index;
        if (index > 0) previous = paragraphStyleName(story.paragraphs.item(index - 1));
        if (index + 1 < story.paragraphs.length) next = paragraphStyleName(story.paragraphs.item(index + 1));
      } catch (error) {}
      if (!headingPattern.test(previous) && !headingPattern.test(next)) return;
      if (ctx.report.dryRun) detail(ctx, "Would remove empty paragraph near heading.");
      else { paragraph.remove(); changed(ctx, 1); }
    });
  }

  export function preventOrphanSubtitles(ctx: Context): void {
    eachParagraph(ctx.doc, function (paragraph: Paragraph): void {
      if (!/subtitle|subhead|heading 2/i.test(paragraphStyleName(paragraph))) return;
      if (ctx.report.dryRun) detail(ctx, "Would apply keep-with-next to " + paragraphStyleName(paragraph) + ".");
      else {
        paragraph.keepWithNext = 1;
        paragraph.keepLinesTogether = true;
        changed(ctx, 1);
      }
    });
  }

  export function adjustTitleSpacing(ctx: Context): void {
    var i: number;
    for (i = 0; i < ctx.doc.paragraphStyles.length; i++) {
      var style = ctx.doc.paragraphStyles.item(i);
      if (!/chapter|title|heading 1/i.test(style.name)) continue;
      detail(ctx, "Title style: " + style.name);
      if (!ctx.report.dryRun) {
        style.spaceBefore = "0pt";
        style.spaceAfter = "12pt";
        style.keepWithNext = 2;
        changed(ctx, 1);
      }
    }
  }

  function applyParentRules(ctx: Context, chapterOnly: boolean): void {
    var rules = chapterOnly
      ? [{ style: "Chapter Title", parent: "Chapter Opening" }, { style: "Chapter Heading", parent: "Chapter Opening" }]
      : [{ style: "Chapter Title", parent: "Chapter Opening" }, { style: "Article Title", parent: "Article Opening" }];
    var p: number;
    var r: number;
    for (p = 0; p < ctx.doc.pages.length; p++) {
      var page = ctx.doc.pages.item(p);
      var matches: string[] = [];
      for (r = 0; r < rules.length; r++) {
        var found = page.textFrames.length > 0 && String(page.textFrames.item(0).parentStory.contents).indexOf(rules[r].style) >= 0;
        if (found) matches.push(rules[r].parent);
      }
      if (matches.length > 1) { skipped(ctx, "Conflicting parent rules on page " + page.name); continue; }
      if (matches.length === 0) continue;
      var parent = parentByName(ctx.doc, matches[0]);
      if (!parent) { skipped(ctx, "Missing parent page: " + matches[0]); continue; }
      detail(ctx, "Page " + page.name + " -> " + matches[0]);
      if (!ctx.report.dryRun) { page.appliedMaster = parent; changed(ctx, 1); }
    }
  }

  export function applyMasterByContent(ctx: Context): void { applyParentRules(ctx, false); }
  export function applyMasterByChapter(ctx: Context): void { applyParentRules(ctx, true); }

  function convertStyle(ctx: Context, fromName: string, toName: string): void {
    var target = styleByName(ctx.doc, toName);
    if (!target) { skipped(ctx, "Missing target style: " + toName); return; }
    eachParagraph(ctx.doc, function (paragraph: Paragraph): void {
      if (paragraphStyleName(paragraph) !== fromName) return;
      detail(ctx, fromName + " -> " + toName);
      if (!ctx.report.dryRun) { paragraph.appliedParagraphStyle = target; changed(ctx, 1); }
    });
  }

  export function convertHeading1ToChapter(ctx: Context): void { convertStyle(ctx, "Heading 1", "Chapter Title"); }
  export function convertNormalToBody(ctx: Context): void { convertStyle(ctx, "Normal", "Body"); }

  export function formatChapters(ctx: Context): void {
    convertHeading1ToChapter(ctx);
    adjustTitleSpacing(ctx);
    preventOrphanSubtitles(ctx);
    applyMasterByChapter(ctx);
  }

  export function importMarkdownAuto(ctx: Context): void {
    var file = File.openDialog("Choose a Markdown file", "*.md") as File;
    if (!file) { skipped(ctx, "No Markdown file selected."); return; }
    file.encoding = "UTF-8";
    file.open("r");
    var contents = file.read();
    file.close();
    var lines = contents.split(/\r?\n/);
    detail(ctx, "Markdown lines: " + lines.length);
    if (ctx.report.dryRun) return;
    var frame = ctx.doc.pages.item(0).textFrames.add(ctx.doc.activeLayer as Layer);
    frame.geometricBounds = ["20mm", "20mm", "195mm", "259mm"];
    frame.contents = contents.replace(/^### (.*)$/gm, "$1").replace(/^## (.*)$/gm, "$1").replace(/^# (.*)$/gm, "$1");
    changed(ctx, 1);
  }

  export function convertBracketsToFootnotes(ctx: Context): void {
    var matches = 0;
    eachParagraph(ctx.doc, function (paragraph: Paragraph): void {
      var found = String(paragraph.contents).match(/\[[0-9]+\]/g);
      if (found) matches += found.length;
    });
    detail(ctx, "Bracket references found: " + matches);
    if (!ctx.report.dryRun && matches > 0) warn(ctx, "Conversion requires one-to-one reference definitions; no ambiguous references were changed.");
  }

  export function migrateFootnotesBetweenDocs(ctx: Context): void {
    detail(ctx, "Open documents: " + app.documents.length);
    if (app.documents.length !== 2) {
      skipped(ctx, "Footnote migration requires exactly two open documents.");
      return;
    }
    warn(ctx, "Migration requires verified one-to-one story pairing; diagnostic only until pairing is unambiguous.");
  }

  export function bilingualPrecisionLayout(ctx: Context): void {
    var spreadCount = ctx.doc.spreads.length;
    detail(ctx, "Facing pages: " + ctx.doc.documentPreferences.facingPages);
    detail(ctx, "Spreads inspected: " + spreadCount);
    if (!ctx.doc.documentPreferences.facingPages) skipped(ctx, "Document is not configured for facing pages.");
    var i: number;
    for (i = 0; i < ctx.doc.spreads.length; i++) {
      var spread = ctx.doc.spreads.item(i);
      if (spread.pages.length !== 2) warn(ctx, "Spread " + (i + 1) + " is not a two-page pair.");
    }
  }

  export function configureBaselineGrid(ctx: Context): void {
    detail(ctx, "Baseline start: 0mm");
    detail(ctx, "Baseline increment: 12pt");
    if (ctx.report.dryRun) return;
    ctx.doc.gridPreferences.baselineStart = "0mm";
    ctx.doc.gridPreferences.baselineDivision = "12pt";
    ctx.doc.gridPreferences.baselineGridRelativeOption = BaselineGridRelativeOption.TOP_OF_MARGIN_OF_BASELINE_GRID_RELATIVE_OPTION;
    changed(ctx, 1);
  }

  export function packPageItems(ctx: Context): void {
    var selection: any[] = app.selection as any[];
    detail(ctx, "Selected items: " + selection.length);
    if (selection.length < 2) { skipped(ctx, "Select at least two page items to pack."); return; }
    warn(ctx, "Editorial-safe mode preserves rotation and reading order. Packing is diagnostic until explicit region rules are supplied.");
  }
}
