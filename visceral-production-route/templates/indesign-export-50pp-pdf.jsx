#target indesign
app.scriptPreferences.userInteractionLevel = UserInteractionLevels.NEVER_INTERACT;

var SOURCE_INDD = "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/output/indesign/the-visceral-theory-of-sight-50pp.indd";
var OUTPUT_PDF = "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/output/pdf/the-visceral-theory-of-sight-50pp-indesign-export.pdf";
var REPORT_FILE = "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/reports/indesign-50pp-export-report.txt";

function logLine(message) {
    var report = File(REPORT_FILE);
    if (!report.parent.exists) report.parent.create();
    report.open("a");
    report.writeln(new Date().toString() + " | " + message);
    report.close();
}

function main() {
    logLine("start export");
    var source = File(SOURCE_INDD);
    if (!source.exists) throw Error("Missing source INDD: " + SOURCE_INDD);

    var doc = app.open(source);
    logLine("opened pages=" + doc.pages.length);

    var pdfFile = File(OUTPUT_PDF);
    if (!pdfFile.parent.exists) pdfFile.parent.create();

    var preset = null;
    try {
        preset = app.pdfExportPresets.itemByName("[High Quality Print]");
        preset.name;
    } catch (e) {
        preset = app.pdfExportPresets.item(0);
    }

    doc.exportFile(ExportFormat.PDF_TYPE, pdfFile, false, preset);
    logLine("exported pdf=" + OUTPUT_PDF);
    doc.save();
    logLine("saved source");
}

main();
