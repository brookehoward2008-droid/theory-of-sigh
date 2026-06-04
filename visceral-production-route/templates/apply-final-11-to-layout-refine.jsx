#target indesign
app.scriptPreferences.userInteractionLevel = UserInteractionLevels.NEVER_INTERACT;

var SOURCE_INDD = "C:/Users/toddl/OneDrive/Desktop/SCHOOL/Graph252 booklab/visceral-theory of sight assets/layout refine.indd";
var OUTPUT_INDD = "C:/Users/toddl/OneDrive/Desktop/SCHOOL/Graph252 booklab/visceral-theory of sight assets/layout refine_FINAL_AUTOBUILD.indd";
var REPORT_FILE = "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/reports/layout-refine-autobuild-report.txt";

// Final 11-image asset sheet for InDesign ExtendScript.
// Place this beside the final-11-image-merge folder or adjust ASSET_ROOT.
var ASSET_ROOT = "C:/Users/toddl/OneDrive/Documents/visceral/visceral-production-route/assets/final-11-image-merge";
if (ASSET_ROOT.charAt(ASSET_ROOT.length - 1) !== "/") ASSET_ROOT += "/";
var assetSheet = [
    {
        page: 3,
        type: "image",
        layer: "BACKGROUND",
        bounds: [-0.125, -0.125, 11.1, 8.62],
        assetPath: ASSET_ROOT + "see-plus-NP3s9BYOqAc-unsplash_2.jpg",
        fitOption: FitOptions.FILL_PROPORTIONALLY,
        title: "Dappled Shade",
        section: "Avant-Garde",
        caption: "A stylized portrait of a woman looking directly through bright green leaves with intense sunlight casting sharp shadows across her face."
    },
    {
        page: 4,
        type: "image",
        layer: "BACKGROUND",
        bounds: [-0.125, -0.125, 11.1, 8.62],
        assetPath: ASSET_ROOT + "igor-rand-GIW9CCL3HxA-unsplash_2.jpg",
        fitOption: FitOptions.FILL_PROPORTIONALLY,
        title: "Neon Distortion",
        section: "Avant-Garde",
        caption: "A vibrant and moody portrait with heavy motion blur featuring a face bathed in psychedelic pink and blue neon lighting."
    },
    {
        page: 5,
        type: "image",
        layer: "BACKGROUND",
        bounds: [1, 0.9, 10, 7.6],
        assetPath: ASSET_ROOT + "nina-zeynep-guler-fjJiVSX-BxM-unsplash_2.jpg",
        fitOption: FitOptions.FILL_PROPORTIONALLY,
        title: "Fading Bloom",
        section: "Flora",
        caption: "A tight macro crop focusing on a woman's green eye and nose as she holds a stem of wilted white daisy flowers against her cheek."
    },
    {
        page: 6,
        type: "image",
        layer: "BACKGROUND",
        bounds: [1, 0.9, 10, 7.6],
        assetPath: ASSET_ROOT + "enesh-taganova-IoXGIDqVqYQ-unsplash (1)_2.jpg",
        fitOption: FitOptions.FILL_PROPORTIONALLY,
        title: "Aster Peep",
        section: "Flora",
        caption: "A playful composition showing only the right side of a woman's face and eye as she peeks out from behind a dense bush of purple aster wildflowers."
    },
    {
        page: 7,
        type: "image",
        layer: "BACKGROUND",
        bounds: [-0.125, -0.125, 11.1, 8.62],
        assetPath: ASSET_ROOT + "umesh-soni-hpklBuuel_k-unsplash.jpg",
        fitOption: FitOptions.FILL_PROPORTIONALLY,
        title: "The Philodendron Window",
        section: "Flora",
        caption: "A compelling macro shot showing only a single bright hazel eye peering through a natural opening in a massive vibrant green split-leaf philodendron."
    },
    {
        page: 8,
        type: "image",
        layer: "BACKGROUND",
        bounds: [1.25, 1.15, 8.75, 7.35],
        assetPath: ASSET_ROOT + "janko-ferlic-brZT6bdt6NA-unsplash.jpg",
        fitOption: FitOptions.FILL_PROPORTIONALLY,
        title: "The Jeweled Veil",
        section: "Cultural",
        caption: "A striking close-up focusing on the intense blue eyes of a woman wearing a traditional bindi and a brilliant intricate gold headpiece while pulling a tan and red veil across her face."
    },
    {
        page: 9,
        type: "image",
        layer: "BACKGROUND",
        bounds: [1.25, 1.15, 8.75, 7.35],
        assetPath: ASSET_ROOT + "alexander-krivitskiy-az7rqWLWkhI-unsplash.jpg",
        fitOption: FitOptions.FILL_PROPORTIONALLY,
        title: "Floral Veil",
        section: "Cinematic Grain",
        caption: "A grain-textured black and white close-up portrait of a woman looking into the camera from behind a dense bundle of small delicate wildflowers."
    },
    {
        page: 10,
        type: "image",
        layer: "BACKGROUND",
        bounds: [-0.125, -0.125, 11.1, 8.62],
        assetPath: ASSET_ROOT + "elvis-kaiser-Rqbk5ez6Qa0-unsplash.jpg",
        fitOption: FitOptions.FILL_PROPORTIONALLY,
        title: "Poppy Field Portrait",
        section: "Avant-Garde",
        caption: "A vibrant outdoor portrait of a young woman with curly blonde hair wearing a traditional embroidered white blouse and a floral crown framed by bright red poppies."
    },
    {
        page: 11,
        type: "image",
        layer: "BACKGROUND",
        bounds: [1, 0.9, 10, 7.6],
        assetPath: ASSET_ROOT + "teslariu-mihai-tK-SzdDiUIs-unsplash.jpg",
        fitOption: FitOptions.FILL_PROPORTIONALLY,
        title: "The Patchwork of Hope",
        section: "Flora",
        caption: "A close-up portrait of a woman's face in dappled sunlight featuring a medical bandage across her cheek adorned with small colorful flowers and the handwritten word \"Hope\"."
    },
    {
        page: 12,
        type: "image",
        layer: "BACKGROUND",
        bounds: [1, 0.9, 10, 7.6],
        assetPath: ASSET_ROOT + "drew-dizzy-graham-cTKGZJTMJQU-unsplash.jpg",
        fitOption: FitOptions.FILL_PROPORTIONALLY,
        title: "Emerging from Darkness",
        section: "Cinematic Grain",
        caption: "A high-contrast black-and-white portrait of a freckled woman looking over her shoulder her face softly illuminated against a stark pitch-black background."
    },
    {
        page: 13,
        type: "image",
        layer: "BACKGROUND",
        bounds: [-0.125, -0.125, 11.1, 8.62],
        assetPath: ASSET_ROOT + "andrey-zvyagintsev-T8IkNlQojCQ-unsplash.jpg",
        fitOption: FitOptions.FILL_PROPORTIONALLY,
        title: "Shrouded Glance",
        section: "Cinematic Grain",
        caption: "A grainy black and white close-up portrait of a woman pulling a thick wool sweater or blanket up to cover the lower half of her face leaving only her intense expressive eye visible."
    },
];

// Example page-5 placement object resolved from the manifest:
// {
//     page: 5,
//     type: "image",
//     layer: "BACKGROUND",
//     bounds: [1.0, 0.9, 10.0, 7.6],
//     assetPath: "final-11-image-merge/nina-zeynep-guler-fjJiVSX-BxM-unsplash_2.jpg",
//     fitOption: FitOptions.FILL_PROPORTIONALLY
// }

function main() {
    logStatus('start');
    var sourceFile = File(SOURCE_INDD);
    var outputFile = File(OUTPUT_INDD);
    if (!sourceFile.exists) throw Error('Missing source INDD: ' + SOURCE_INDD);
    logStatus('source exists');
    if (!outputFile.exists) throw Error('Missing prebuilt output copy: ' + OUTPUT_INDD);
    logStatus('output copy exists');
    var doc = app.open(outputFile);
    logStatus('output copy opened: pages=' + doc.pages.length + ', masters=' + doc.masterSpreads.length);
    var oldH = doc.viewPreferences.horizontalMeasurementUnits;
    var oldV = doc.viewPreferences.verticalMeasurementUnits;
    doc.viewPreferences.horizontalMeasurementUnits = MeasurementUnits.INCHES;
    doc.viewPreferences.verticalMeasurementUnits = MeasurementUnits.INCHES;
    injectEditorialPalette(doc);
    logStatus('palette applied');
    computeAndApplyAlgorithmicGrid(doc);
    logStatus('grid applied');
    var imageLayer = getOrCreateLayer(doc, 'BACKGROUND');
    var textLayer = getOrCreateLayer(doc, 'TEXT');
    clearLayerItems(imageLayer);
    clearLayerItems(textLayer);
    logStatus('layers cleared');
    for (var i = 0; i < assetSheet.length; i++) {
        placeAsset(doc, assetSheet[i], imageLayer, textLayer);
        logStatus('placed asset page ' + assetSheet[i].page + ': ' + assetSheet[i].title);
    }
    injectTOCAndBibliography(doc, textLayer);
    logStatus('toc and bibliography applied');
    doc.viewPreferences.horizontalMeasurementUnits = oldH;
    doc.viewPreferences.verticalMeasurementUnits = oldV;
    doc.save(outputFile);
    var statusMessage = 'Final 11-image layout refine build applied: ' + outputFile.fsName;
    $.writeln(statusMessage);
    logStatus(statusMessage);
}

function logStatus(message) {
    var f = File(REPORT_FILE);
    f.open('a');
    f.writeln(new Date().toString() + ' | ' + message);
    f.close();
}

function getOrCreateLayer(doc, name) {
    var layer = doc.layers.itemByName(name);
    if (!layer.isValid) layer = doc.layers.add({name: name});
    layer.locked = false;
    layer.visible = true;
    return layer;
}

function injectEditorialPalette(doc) {
    var customColors = [
        { name: "Raw Concrete", space: ColorSpace.CMYK, value: [19, 15, 16, 0] },
        { name: "Stark Void", space: ColorSpace.CMYK, value: [67, 60, 59, 44] },
        { name: "Unbleached Page", space: ColorSpace.CMYK, value: [1, 1, 4, 0] },
        { name: "Incandescent Beam", space: ColorSpace.CMYK, value: [14, 57, 100, 3] }
    ];
    for (var i = 0; i < customColors.length; i++) {
        var colorData = customColors[i];
        var targetColor = doc.colors.itemByName(colorData.name);
        if (!targetColor.isValid) {
            targetColor = doc.colors.add({name: colorData.name});
        }
        targetColor.properties = {
            model: ColorModel.PROCESS,
            space: colorData.space,
            colorValue: colorData.value
        };
    }
}

function computeAndApplyAlgorithmicGrid(doc) {
    logStatus('grid start');
    var PAGE_WIDTH = 8.5;
    var COL_COUNT = 12;
    var GUTTER_INCHES = 0.1667;
    var marginInside = 0.75;
    var marginTop = marginInside * 1.1333;
    var marginOutside = marginInside * 1.2000;
    var marginBottom = marginInside * 1.3333;
    var totalAvailableWidth = PAGE_WIDTH - (marginInside + marginOutside);
    var totalGutterWidth = (COL_COUNT - 1) * GUTTER_INCHES;
    var calculatedColumnWidth = (totalAvailableWidth - totalGutterWidth) / COL_COUNT;
    var masterSpread = doc.masterSpreads.item(0);
    var totalMasterPages = masterSpread.pages.length;
    logStatus('grid master pages=' + totalMasterPages);
    for (var i = 0; i < totalMasterPages; i++) {
        var mPage = masterSpread.pages.item(i);
        var isLeftPage = (i % 2 === 0);
        logStatus('grid applying master page index=' + i);
        with (mPage.marginPreferences) {
            top = marginTop;
            bottom = marginBottom;
            left = isLeftPage ? marginOutside : marginInside;
            right = isLeftPage ? marginInside : marginOutside;
            columnCount = COL_COUNT;
            columnGutter = GUTTER_INCHES;
        }
    }
    logStatus('grid margins applied');
    with (doc.gridPreferences) {
        baselineStart = marginTop;
        baselineDivision = "7.5pt";
        baselineGridRelativeOption = BaselineGridRelativeOption.TOP_OF_PAGE;
    }
    logStatus('grid baseline applied');
    $.writeln('Algorithmic grid applied. Column width: ' + calculatedColumnWidth.toFixed(4) + ' in.');
}

function clearLayerItems(layer) {
    for (var i = layer.pageItems.length - 1; i >= 0; i--) {
        try { layer.pageItems.item(i).remove(); } catch (e) {}
    }
}

function inchBounds(values) {
    return [values[0] + 'in', values[1] + 'in', values[2] + 'in', values[3] + 'in'];
}

function placeAsset(doc, asset, imageLayer, textLayer) {
    while (doc.pages.length < asset.page) doc.pages.add();
    var page = doc.pages.item(asset.page - 1);
    var imgFile = File(asset.assetPath);
    if (!imgFile.exists) throw Error('Missing asset: ' + asset.assetPath);
    var frame = page.rectangles.add({itemLayer: imageLayer, geometricBounds: inchBounds(asset.bounds), strokeWeight: 0});
    frame.textWrapPreferences.textWrapMode = TextWrapModes.NONE;
    frame.place(imgFile);
    frame.fit(FitOptions.FILL_PROPORTIONALLY);
    frame.fit(FitOptions.CENTER_CONTENT);
    var captionTop = Math.min(asset.bounds[2] + 0.15, 10.25);
    var caption = page.textFrames.add({
        itemLayer: textLayer,
        geometricBounds: inchBounds([captionTop, 0.9, Math.min(captionTop + 0.65, 10.75), 7.6])
    });
    caption.contents = asset.title + ' / ' + asset.section + '\r' + asset.caption;
    caption.textFramePreferences.ignoreWrap = true;
    caption.texts.item(0).pointSize = 8.5;
    caption.texts.item(0).leading = 11;
}

function injectTOCAndBibliography(doc, textLayer) {
    while (doc.pages.length < 8) doc.pages.add();
    var tocPage = doc.pages.item(1);
    var tocFrame = tocPage.textFrames.add({
        itemLayer: textLayer,
        geometricBounds: inchBounds([1.5, 0.9, 5.0, 4.5])
    });
    tocFrame.contents = 'CONTENTS\r\r' +
        '03  Dappled Shade ........................ P. 3\r' +
        '04  Neon Distortion ..................... P. 4\r' +
        '05  Fading Bloom ........................ P. 5\r' +
        '06  Aster Peep .......................... P. 6\r' +
        '07  The Philodendron Window ............. P. 7\r' +
        '08  The Jeweled Veil / Register ......... P. 8\r' +
        '09  Floral Veil ......................... P. 9\r' +
        '10  Poppy Field Portrait ................ P. 10\r' +
        '11  The Patchwork of Hope ............... P. 11\r' +
        '12  Emerging from Darkness .............. P. 12\r' +
        '13  Shrouded Glance ..................... P. 13';
    tocFrame.textFramePreferences.ignoreWrap = true;
    tocFrame.texts.item(0).pointSize = 9.5;
    tocFrame.texts.item(0).leading = 12;
    tocFrame.paragraphs.item(0).pointSize = 14;

    var metricFrame = tocPage.textFrames.add({
        itemLayer: textLayer,
        geometricBounds: inchBounds([5.35, 0.9, 10.0, 7.6])
    });
    metricFrame.contents = "HARMONIC MARGIN ALGORITHM\r\rInstead of uniform margins, this build expands outward from the inside gutter to create optical spread balance.\rInside Margin: 0.75 in\rTop Margin: 0.85 in (0.75 x 1.1333)\rOutside Margin: 0.90 in (0.75 x 1.2000)\rBottom Margin: 1.00 in (0.75 x 1.3333)\rColumn System: 12-column grid lock; 0.1667 in gutters\rBaseline System: 15 pt leading aligned to 7.5 pt master layout subdivisions" + '\r\r' + "METRIC BLOCK: SPECIFICATION DATA ARCHIVE // DIAGRAM 04-B\r- Core Latitude Anchor: 45.6 deg N (Calculated Solar Angle Progression)\r- Textual Leading Baseline: 15 pt (Aligned to 7.5 pt Master Layout Subdivisions)\r- Primary Contrast Threshold: 8:1 Evident Range\r- Typographic Boundary: 12-Column Grid Lock (Strict Zero-Bleed Text Constraints)\r\rMETRIC DATA // CH. 2\r- Exposure Range: EV 12-14\r- Contrast Ratio: 8:1 structured shadow depth\r- Structural Axis: 45-degree convergence\r- Lens Architecture: 35mm perspective control tilt-shift\r- Spectrum: Monochromatic architectural calibration";
    metricFrame.textFramePreferences.ignoreWrap = true;
    metricFrame.texts.item(0).pointSize = 7.4;
    metricFrame.texts.item(0).leading = 9.2;
    metricFrame.paragraphs.item(0).pointSize = 9.5;

    var bibPage = doc.pages.item(7);
    var bibFrame = bibPage.textFrames.add({
        itemLayer: textLayer,
        geometricBounds: inchBounds([6.0, 0.9, 10.0, 7.6])
    });
    bibFrame.contents = 'PRODUCTION REGISTER & BIBLIOGRAPHY\r\r' +
        'Visual Asset Register: IMG_01 through IMG_11 compiled locally.\r' +
        'Vector Status: no verified vector files found in the final merge package.\r\r' +
        'READING LIST TO VERIFY\r' +
        '- Bachelard, G. (1994). The Poetics of Space. Beacon Press.\r' +
        '- Tanizaki, J. (1977). In Praise of Shadows. Leete\'s Island Books.\r\r' +
        'Note: source URLs, licenses, and course bibliography requirements still need final human verification.';
    bibFrame.textFramePreferences.ignoreWrap = true;
    bibFrame.texts.item(0).pointSize = 8.5;
    bibFrame.texts.item(0).leading = 11;
    bibFrame.paragraphs.item(0).pointSize = 10;
}

main();
