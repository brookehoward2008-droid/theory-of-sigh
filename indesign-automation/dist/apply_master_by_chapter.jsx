// Brooke Adobe Automation - original ExtendScript-safe JSX
/// <reference types="types-for-adobe/InDesign/2015.3" />
var BrookeAutomation;
(function (BrookeAutomation) {
    function now() {
        return new Date().toUTCString();
    }
    function escapeText(value) {
        return value.replace(/\\/g, "\\\\").replace(/"/g, '\\"').replace(/\r/g, "\\r").replace(/\n/g, "\\n");
    }
    function stringArray(values) {
        var parts = [];
        var i;
        for (i = 0; i < values.length; i++)
            parts.push('"' + escapeText(values[i]) + '"');
        return "[" + parts.join(",") + "]";
    }
    function reportText(report) {
        return "{\n" +
            '  "command": "' + escapeText(report.command) + '",\n' +
            '  "dryRun": ' + (report.dryRun ? "true" : "false") + ",\n" +
            '  "startedAt": "' + escapeText(report.startedAt) + '",\n' +
            '  "finishedAt": "' + escapeText(report.finishedAt) + '",\n' +
            '  "documentName": "' + escapeText(report.documentName) + '",\n' +
            '  "changed": ' + report.changed + ",\n" +
            '  "skipped": ' + report.skipped + ",\n" +
            '  "warnings": ' + stringArray(report.warnings) + ",\n" +
            '  "errors": ' + stringArray(report.errors) + ",\n" +
            '  "details": ' + stringArray(report.details) + "\n" +
            "}\n";
    }
    function writeReport(report) {
        var folder = new Folder(Folder.myDocuments + "/Brooke Adobe Automation Reports");
        if (!folder.exists)
            folder.create();
        var safeName = report.command.replace(/[^A-Za-z0-9_-]/g, "_");
        var file = new File(folder.fsName + "/" + safeName + "-latest.json");
        file.encoding = "UTF-8";
        file.open("w");
        file.write(reportText(report));
        file.close();
        return file.fsName;
    }
    function warn(ctx, message) {
        ctx.report.warnings.push(message);
    }
    BrookeAutomation.warn = warn;
    function detail(ctx, message) {
        ctx.report.details.push(message);
    }
    BrookeAutomation.detail = detail;
    function changed(ctx, amount) {
        ctx.report.changed += amount || 1;
    }
    BrookeAutomation.changed = changed;
    function skipped(ctx, message) {
        ctx.report.skipped += 1;
        ctx.report.warnings.push(message);
    }
    BrookeAutomation.skipped = skipped;
    function styleByName(doc, name) {
        try {
            var style = doc.paragraphStyles.itemByName(name);
            style.name;
            return style;
        }
        catch (error) {
            return null;
        }
    }
    BrookeAutomation.styleByName = styleByName;
    function parentByName(doc, name) {
        try {
            var parent = doc.masterSpreads.itemByName(name);
            parent.name;
            return parent;
        }
        catch (error) {
            return null;
        }
    }
    BrookeAutomation.parentByName = parentByName;
    function runCommand(name, mutates, operation) {
        if (app.documents.length === 0) {
            alert(name + ": no InDesign document is open.");
            return;
        }
        var dryRun = mutates ? !confirm(name + "\n\nApply changes?\nChoose No for a diagnostic dry run.") : true;
        var report = {
            command: name,
            dryRun: dryRun,
            startedAt: now(),
            finishedAt: "",
            documentName: app.activeDocument.name,
            changed: 0,
            skipped: 0,
            warnings: [],
            errors: [],
            details: [],
        };
        var ctx = { doc: app.activeDocument, report: report };
        try {
            if (mutates && !dryRun) {
                app.doScript(function () { operation(ctx); }, ScriptLanguage.JAVASCRIPT, undefined, UndoModes.ENTIRE_SCRIPT, "Brooke Automation: " + name);
            }
            else {
                operation(ctx);
            }
        }
        catch (error) {
            report.errors.push(String(error));
        }
        report.finishedAt = now();
        var path = writeReport(report);
        alert(name + " finished.\n\n" +
            "Mode: " + (dryRun ? "dry run" : "apply") + "\n" +
            "Changed: " + report.changed + "\n" +
            "Skipped: " + report.skipped + "\n" +
            "Errors: " + report.errors.length + "\n\n" +
            "Report: " + path);
    }
    BrookeAutomation.runCommand = runCommand;
})(BrookeAutomation || (BrookeAutomation = {}));
var BrookeAutomation;
(function (BrookeAutomation) {
    function eachParagraph(doc, visit) {
        var s;
        var p;
        for (s = 0; s < doc.stories.length; s++) {
            var story = doc.stories.item(s);
            for (p = story.paragraphs.length - 1; p >= 0; p--)
                visit(story.paragraphs.item(p));
        }
    }
    function paragraphStyleName(paragraph) {
        try {
            var applied = paragraph.appliedParagraphStyle;
            return typeof applied === "string" ? applied : String(applied.name);
        }
        catch (error) {
            return "";
        }
    }
    function trimmed(value) {
        return value.replace(/[\r\n\t ]+/g, "");
    }
    function countMissingLinks(doc) {
        var count = 0;
        var i;
        for (i = 0; i < doc.links.length; i++) {
            if (String(doc.links.item(i).status).indexOf("LINK_MISSING") >= 0)
                count++;
        }
        return count;
    }
    function countOverset(doc) {
        var count = 0;
        var i;
        for (i = 0; i < doc.textFrames.length; i++)
            if (doc.textFrames.item(i).overflows)
                count++;
        return count;
    }
    function debugAdvanced(ctx) {
        var doc = ctx.doc;
        BrookeAutomation.detail(ctx, "pages=" + doc.pages.length);
        BrookeAutomation.detail(ctx, "facingPages=" + doc.documentPreferences.facingPages);
        BrookeAutomation.detail(ctx, "pageWidth=" + doc.documentPreferences.pageWidth);
        BrookeAutomation.detail(ctx, "pageHeight=" + doc.documentPreferences.pageHeight);
        BrookeAutomation.detail(ctx, "links=" + doc.links.length);
        BrookeAutomation.detail(ctx, "missingLinks=" + countMissingLinks(doc));
        BrookeAutomation.detail(ctx, "oversetTextFrames=" + countOverset(doc));
        BrookeAutomation.detail(ctx, "paragraphStyles=" + doc.paragraphStyles.length);
        BrookeAutomation.detail(ctx, "parentPages=" + doc.masterSpreads.length);
        BrookeAutomation.detail(ctx, "tocStyles=" + doc.tocStyles.length);
        BrookeAutomation.detail(ctx, "hyperlinks=" + doc.hyperlinks.length);
        try {
            BrookeAutomation.detail(ctx, "preflightProfile=" + doc.preflightOptions.preflightWorkingProfile);
        }
        catch (error) {
            BrookeAutomation.warn(ctx, "Unable to read preflight profile.");
        }
    }
    BrookeAutomation.debugAdvanced = debugAdvanced;
    function configurePublicationPreflight(ctx) {
        var profileName = "Anatomy of Looking - Color Landscape";
        var profile;
        try {
            profile = app.preflightProfiles.itemByName(profileName);
            profile.name;
        }
        catch (error) {
            profile = app.preflightProfiles.itemByName("kDigPubProfileName").duplicate();
            profile.name = profileName;
        }
        BrookeAutomation.detail(ctx, "Profile target: " + profileName);
        BrookeAutomation.detail(ctx, "Intentional exception: ADBE_CMYPlates");
        BrookeAutomation.detail(ctx, "Intentional exception: ADBE_PageSizeOrientation");
        if (ctx.report.dryRun)
            return;
        profile.description = "Color landscape magazine profile retaining critical publication checks.";
        profile.preflightProfileRules.itemByName("ADBE_CMYPlates").flag = 1699890274;
        profile.preflightProfileRules.itemByName("ADBE_PageSizeOrientation").flag = 1699890274;
        ctx.doc.preflightOptions.preflightWorkingProfile = profile;
        ctx.doc.preflightOptions.preflightOff = false;
        BrookeAutomation.changed(ctx, 1);
    }
    BrookeAutomation.configurePublicationPreflight = configurePublicationPreflight;
    function cleanEmptyParagraphs(ctx) {
        var headingPattern = /chapter|title|heading|subtitle/i;
        eachParagraph(ctx.doc, function (paragraph) {
            if (trimmed(String(paragraph.contents)) !== "")
                return;
            var previous = "";
            var next = "";
            try {
                var story = paragraph.parentStory;
                var index = paragraph.index;
                if (index > 0)
                    previous = paragraphStyleName(story.paragraphs.item(index - 1));
                if (index + 1 < story.paragraphs.length)
                    next = paragraphStyleName(story.paragraphs.item(index + 1));
            }
            catch (error) { }
            if (!headingPattern.test(previous) && !headingPattern.test(next))
                return;
            if (ctx.report.dryRun)
                BrookeAutomation.detail(ctx, "Would remove empty paragraph near heading.");
            else {
                paragraph.remove();
                BrookeAutomation.changed(ctx, 1);
            }
        });
    }
    BrookeAutomation.cleanEmptyParagraphs = cleanEmptyParagraphs;
    function preventOrphanSubtitles(ctx) {
        eachParagraph(ctx.doc, function (paragraph) {
            if (!/subtitle|subhead|heading 2/i.test(paragraphStyleName(paragraph)))
                return;
            if (ctx.report.dryRun)
                BrookeAutomation.detail(ctx, "Would apply keep-with-next to " + paragraphStyleName(paragraph) + ".");
            else {
                paragraph.keepWithNext = 1;
                paragraph.keepLinesTogether = true;
                BrookeAutomation.changed(ctx, 1);
            }
        });
    }
    BrookeAutomation.preventOrphanSubtitles = preventOrphanSubtitles;
    function adjustTitleSpacing(ctx) {
        var i;
        for (i = 0; i < ctx.doc.paragraphStyles.length; i++) {
            var style = ctx.doc.paragraphStyles.item(i);
            if (!/chapter|title|heading 1/i.test(style.name))
                continue;
            BrookeAutomation.detail(ctx, "Title style: " + style.name);
            if (!ctx.report.dryRun) {
                style.spaceBefore = "0pt";
                style.spaceAfter = "12pt";
                style.keepWithNext = 2;
                BrookeAutomation.changed(ctx, 1);
            }
        }
    }
    BrookeAutomation.adjustTitleSpacing = adjustTitleSpacing;
    function applyParentRules(ctx, chapterOnly) {
        var rules = chapterOnly
            ? [{ style: "Chapter Title", parent: "Chapter Opening" }, { style: "Chapter Heading", parent: "Chapter Opening" }]
            : [{ style: "Chapter Title", parent: "Chapter Opening" }, { style: "Article Title", parent: "Article Opening" }];
        var p;
        var r;
        for (p = 0; p < ctx.doc.pages.length; p++) {
            var page = ctx.doc.pages.item(p);
            var matches = [];
            for (r = 0; r < rules.length; r++) {
                var found = page.textFrames.length > 0 && String(page.textFrames.item(0).parentStory.contents).indexOf(rules[r].style) >= 0;
                if (found)
                    matches.push(rules[r].parent);
            }
            if (matches.length > 1) {
                BrookeAutomation.skipped(ctx, "Conflicting parent rules on page " + page.name);
                continue;
            }
            if (matches.length === 0)
                continue;
            var parent = BrookeAutomation.parentByName(ctx.doc, matches[0]);
            if (!parent) {
                BrookeAutomation.skipped(ctx, "Missing parent page: " + matches[0]);
                continue;
            }
            BrookeAutomation.detail(ctx, "Page " + page.name + " -> " + matches[0]);
            if (!ctx.report.dryRun) {
                page.appliedMaster = parent;
                BrookeAutomation.changed(ctx, 1);
            }
        }
    }
    function applyMasterByContent(ctx) { applyParentRules(ctx, false); }
    BrookeAutomation.applyMasterByContent = applyMasterByContent;
    function applyMasterByChapter(ctx) { applyParentRules(ctx, true); }
    BrookeAutomation.applyMasterByChapter = applyMasterByChapter;
    function convertStyle(ctx, fromName, toName) {
        var target = BrookeAutomation.styleByName(ctx.doc, toName);
        if (!target) {
            BrookeAutomation.skipped(ctx, "Missing target style: " + toName);
            return;
        }
        eachParagraph(ctx.doc, function (paragraph) {
            if (paragraphStyleName(paragraph) !== fromName)
                return;
            BrookeAutomation.detail(ctx, fromName + " -> " + toName);
            if (!ctx.report.dryRun) {
                paragraph.appliedParagraphStyle = target;
                BrookeAutomation.changed(ctx, 1);
            }
        });
    }
    function convertHeading1ToChapter(ctx) { convertStyle(ctx, "Heading 1", "Chapter Title"); }
    BrookeAutomation.convertHeading1ToChapter = convertHeading1ToChapter;
    function convertNormalToBody(ctx) { convertStyle(ctx, "Normal", "Body"); }
    BrookeAutomation.convertNormalToBody = convertNormalToBody;
    function formatChapters(ctx) {
        convertHeading1ToChapter(ctx);
        adjustTitleSpacing(ctx);
        preventOrphanSubtitles(ctx);
        applyMasterByChapter(ctx);
    }
    BrookeAutomation.formatChapters = formatChapters;
    function importMarkdownAuto(ctx) {
        var file = File.openDialog("Choose a Markdown file", "*.md");
        if (!file) {
            BrookeAutomation.skipped(ctx, "No Markdown file selected.");
            return;
        }
        file.encoding = "UTF-8";
        file.open("r");
        var contents = file.read();
        file.close();
        var lines = contents.split(/\r?\n/);
        BrookeAutomation.detail(ctx, "Markdown lines: " + lines.length);
        if (ctx.report.dryRun)
            return;
        var frame = ctx.doc.pages.item(0).textFrames.add(ctx.doc.activeLayer);
        frame.geometricBounds = ["20mm", "20mm", "195mm", "259mm"];
        frame.contents = contents.replace(/^### (.*)$/gm, "$1").replace(/^## (.*)$/gm, "$1").replace(/^# (.*)$/gm, "$1");
        BrookeAutomation.changed(ctx, 1);
    }
    BrookeAutomation.importMarkdownAuto = importMarkdownAuto;
    function convertBracketsToFootnotes(ctx) {
        var matches = 0;
        eachParagraph(ctx.doc, function (paragraph) {
            var found = String(paragraph.contents).match(/\[[0-9]+\]/g);
            if (found)
                matches += found.length;
        });
        BrookeAutomation.detail(ctx, "Bracket references found: " + matches);
        if (!ctx.report.dryRun && matches > 0)
            BrookeAutomation.warn(ctx, "Conversion requires one-to-one reference definitions; no ambiguous references were changed.");
    }
    BrookeAutomation.convertBracketsToFootnotes = convertBracketsToFootnotes;
    function migrateFootnotesBetweenDocs(ctx) {
        BrookeAutomation.detail(ctx, "Open documents: " + app.documents.length);
        if (app.documents.length !== 2) {
            BrookeAutomation.skipped(ctx, "Footnote migration requires exactly two open documents.");
            return;
        }
        BrookeAutomation.warn(ctx, "Migration requires verified one-to-one story pairing; diagnostic only until pairing is unambiguous.");
    }
    BrookeAutomation.migrateFootnotesBetweenDocs = migrateFootnotesBetweenDocs;
    function bilingualPrecisionLayout(ctx) {
        var spreadCount = ctx.doc.spreads.length;
        BrookeAutomation.detail(ctx, "Facing pages: " + ctx.doc.documentPreferences.facingPages);
        BrookeAutomation.detail(ctx, "Spreads inspected: " + spreadCount);
        if (!ctx.doc.documentPreferences.facingPages)
            BrookeAutomation.skipped(ctx, "Document is not configured for facing pages.");
        var i;
        for (i = 0; i < ctx.doc.spreads.length; i++) {
            var spread = ctx.doc.spreads.item(i);
            if (spread.pages.length !== 2)
                BrookeAutomation.warn(ctx, "Spread " + (i + 1) + " is not a two-page pair.");
        }
    }
    BrookeAutomation.bilingualPrecisionLayout = bilingualPrecisionLayout;
    function configureBaselineGrid(ctx) {
        BrookeAutomation.detail(ctx, "Baseline start: 0mm");
        BrookeAutomation.detail(ctx, "Baseline increment: 12pt");
        if (ctx.report.dryRun)
            return;
        ctx.doc.gridPreferences.baselineStart = "0mm";
        ctx.doc.gridPreferences.baselineDivision = "12pt";
        ctx.doc.gridPreferences.baselineGridRelativeOption = BaselineGridRelativeOption.TOP_OF_MARGIN_OF_BASELINE_GRID_RELATIVE_OPTION;
        BrookeAutomation.changed(ctx, 1);
    }
    BrookeAutomation.configureBaselineGrid = configureBaselineGrid;
    function packPageItems(ctx) {
        var selection = app.selection;
        BrookeAutomation.detail(ctx, "Selected items: " + selection.length);
        if (selection.length < 2) {
            BrookeAutomation.skipped(ctx, "Select at least two page items to pack.");
            return;
        }
        BrookeAutomation.warn(ctx, "Editorial-safe mode preserves rotation and reading order. Packing is diagnostic until explicit region rules are supplied.");
    }
    BrookeAutomation.packPageItems = packPageItems;
})(BrookeAutomation || (BrookeAutomation = {}));
BrookeAutomation.runCommand("apply_master_by_chapter", true, BrookeAutomation.applyMasterByChapter);
