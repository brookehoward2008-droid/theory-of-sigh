// The Visceral Theory of Sight - InDesign A4 grid autobuild
// Run from InDesign: File > Scripts > Other Script...
var doc = app.documents.add();
doc.documentPreferences.pageWidth = "210mm";
doc.documentPreferences.pageHeight = "297mm";
doc.documentPreferences.facingPages = true;
doc.documentPreferences.pagesPerDocument = 50;
doc.documentPreferences.documentBleedTopOffset = "3mm";
doc.documentPreferences.documentBleedBottomOffset = "3mm";
doc.documentPreferences.documentBleedInsideOrLeftOffset = "3mm";
doc.documentPreferences.documentBleedOutsideOrRightOffset = "3mm";
doc.marginPreferences.top = "16.000mm";
doc.marginPreferences.bottom = "16.000mm";
doc.marginPreferences.left = "16.000mm";
doc.marginPreferences.right = "16.000mm";
doc.marginPreferences.columnCount = 12;
doc.marginPreferences.columnGutter = "5mm";
var master = doc.masterSpreads.item(0);
master.name = "A-Master - Visceral Grid";
for (var i = 0; i < doc.pages.length; i++) {
  doc.pages.item(i).appliedMaster = master;
}
alert("Visceral A4 facing-pages document created: 50 pages, 3mm bleed, 12 columns.");
