/// <reference types="types-for-adobe/InDesign/2015.3" />

namespace BrookeAutomation {
  export interface Report {
    command: string;
    dryRun: boolean;
    startedAt: string;
    finishedAt: string;
    documentName: string;
    changed: number;
    skipped: number;
    warnings: string[];
    errors: string[];
    details: string[];
  }

  export interface Context {
    doc: Document;
    report: Report;
  }

  function now(): string {
    return new Date().toUTCString();
  }

  function escapeText(value: string): string {
    return value.replace(/\\/g, "\\\\").replace(/"/g, '\\"').replace(/\r/g, "\\r").replace(/\n/g, "\\n");
  }

  function stringArray(values: string[]): string {
    var parts: string[] = [];
    var i: number;
    for (i = 0; i < values.length; i++) parts.push('"' + escapeText(values[i]) + '"');
    return "[" + parts.join(",") + "]";
  }

  function reportText(report: Report): string {
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

  function writeReport(report: Report): string {
    var folder = new Folder(Folder.myDocuments + "/Brooke Adobe Automation Reports");
    if (!folder.exists) folder.create();
    var safeName = report.command.replace(/[^A-Za-z0-9_-]/g, "_");
    var file = new File(folder.fsName + "/" + safeName + "-latest.json");
    file.encoding = "UTF-8";
    file.open("w");
    file.write(reportText(report));
    file.close();
    return file.fsName;
  }

  export function warn(ctx: Context, message: string): void {
    ctx.report.warnings.push(message);
  }

  export function detail(ctx: Context, message: string): void {
    ctx.report.details.push(message);
  }

  export function changed(ctx: Context, amount?: number): void {
    ctx.report.changed += amount || 1;
  }

  export function skipped(ctx: Context, message: string): void {
    ctx.report.skipped += 1;
    ctx.report.warnings.push(message);
  }

  export function styleByName(doc: Document, name: string): ParagraphStyle | null {
    try {
      var style = doc.paragraphStyles.itemByName(name);
      style.name;
      return style;
    } catch (error) {
      return null;
    }
  }

  export function parentByName(doc: Document, name: string): MasterSpread | null {
    try {
      var parent = doc.masterSpreads.itemByName(name);
      parent.name;
      return parent;
    } catch (error) {
      return null;
    }
  }

  export function runCommand(
    name: string,
    mutates: boolean,
    operation: (ctx: Context) => void,
  ): void {
    if (app.documents.length === 0) {
      alert(name + ": no InDesign document is open.");
      return;
    }

    var dryRun = mutates ? !confirm(name + "\n\nApply changes?\nChoose No for a diagnostic dry run.") : true;
    var report: Report = {
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
    var ctx: Context = { doc: app.activeDocument, report: report };

    try {
      if (mutates && !dryRun) {
        app.doScript(
          function (): void { operation(ctx); },
          ScriptLanguage.JAVASCRIPT,
          undefined,
          UndoModes.ENTIRE_SCRIPT,
          "Brooke Automation: " + name,
        );
      } else {
        operation(ctx);
      }
    } catch (error) {
      report.errors.push(String(error));
    }

    report.finishedAt = now();
    var path = writeReport(report);
    alert(
      name + " finished.\n\n" +
      "Mode: " + (dryRun ? "dry run" : "apply") + "\n" +
      "Changed: " + report.changed + "\n" +
      "Skipped: " + report.skipped + "\n" +
      "Errors: " + report.errors.length + "\n\n" +
      "Report: " + path,
    );
  }
}
