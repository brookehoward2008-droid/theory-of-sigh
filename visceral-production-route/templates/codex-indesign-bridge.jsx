// Codex InDesign Bridge
// Automatically applies caption data to InDesign document from Codex metadata
// Usage: Run this script with InDesign open and a document loaded

#target indesign

(function () {
    // ============================================================================
    // CODEX INDESIGN BRIDGE - Caption & Metadata Injection
    // ============================================================================

    var SCRIPT_NAME = "Codex InDesign Bridge";
    var VERSION = "1.0";

    // Configuration
    var CONFIG = {
        // Text frame master page settings
        captionLayerName: "Captions",
        captionFrameName: "Caption_Frame",
        sourceRegisterLayerName: "Source Register",
        
        // Typography
        captionFontSize: 10,
        captionFontName: "Helvetica",
        captionColor: "Black",
        
        // Spacing
        captionMarginBottom: 12, // points
    };

    /**
     * Main handler - validate document and prepare for caption injection
     */
    function main() {
        var doc = app.activeDocument;
        
        if (!doc) {
            alert(SCRIPT_NAME + ": No document open. Please open an InDesign document first.");
            return false;
        }

        log("===============================================");
        log(SCRIPT_NAME + " v" + VERSION);
        log("===============================================");
        log("Document: " + doc.name);
        log("Pages: " + doc.pages.length);
        
        // Preflight checks
        var preflightOK = preflight(doc);
        if (!preflightOK) {
            alert(SCRIPT_NAME + ": Preflight failed. See console for details.");
            return false;
        }

        log("\n✓ Preflight passed");
        log("\nReady for caption injection. Next steps:");
        log("1. Import caption data from Codex metadata");
        log("2. Validate all 67 images present");
        log("3. Inject captions for each visual group");
        log("4. Run InDesign preflight");
        log("5. Export PDF");
        log("\nConsult codex-qa-gate-report.json before final handoff.");
        
        return true;
    }

    /**
     * Preflight checks on InDesign document
     */
    function preflight(doc) {
        var issues = [];

        // Check for required layers
        var requiredLayers = [CONFIG.captionLayerName, CONFIG.sourceRegisterLayerName];
        for (var i = 0; i < requiredLayers.length; i++) {
            var layerExists = false;
            for (var j = 0; j < doc.layers.length; j++) {
                if (doc.layers[j].name === requiredLayers[i]) {
                    layerExists = true;
                    break;
                }
            }
            if (!layerExists) {
                issues.push("Missing layer: " + requiredLayers[i]);
            }
        }

        // Check for missing links
        var missingLinks = 0;
        for (var i = 0; i < doc.links.length; i++) {
            if (!doc.links[i].status === LinkStatus.LINK_OK) {
                missingLinks++;
                log("⚠ Missing link: " + doc.links[i].name);
            }
        }
        if (missingLinks > 0) {
            issues.push("Found " + missingLinks + " missing or modified links");
        }

        // Check for overset text
        var overset = 0;
        for (var i = 0; i < doc.textFrames.length; i++) {
            if (doc.textFrames[i].overflows) {
                overset++;
            }
        }
        if (overset > 0) {
            issues.push("Found " + overset + " text frames with overset text");
        }

        // Report issues
        if (issues.length === 0) {
            log("✓ All preflight checks passed");
            return true;
        } else {
            log("✗ Preflight issues found:");
            for (var i = 0; i < issues.length; i++) {
                log("  - " + issues[i]);
            }
            return false;
        }
    }

    /**
     * Placeholder for caption injection from Codex
     * This will be populated by codex.py via generate_indesign_script_for_captions()
     */
    function injectCaptions(doc, captionData) {
        var injected = 0;
        
        log("\nInjecting captions for " + captionData.length + " assets...");
        
        for (var i = 0; i < captionData.length; i++) {
            var data = captionData[i];
            
            try {
                // Find the text frame for this asset
                var frameLabel = "caption_" + data.label;
                var frame = findFrameByLabel(doc, frameLabel);
                
                if (frame) {
                    // Clear existing text
                    frame.contents = "";
                    
                    // Build caption text
                    var captionText = data.label + ": " + data.title + "\n";
                    captionText += data.visual_group + " • " + data.section;
                    
                    // Apply text
                    frame.contents = captionText;
                    
                    // Apply formatting
                    formatCaption(frame);
                    
                    injected++;
                    log("  ✓ " + data.label);
                } else {
                    log("  ⚠ Frame not found: " + frameLabel);
                }
            } catch (e) {
                log("  ✗ Error processing " + data.label + ": " + e.message);
            }
        }
        
        log("Injected " + injected + " captions");
        return injected;
    }

    /**
     * Find a frame by label
     */
    function findFrameByLabel(doc, label) {
        for (var i = 0; i < doc.textFrames.length; i++) {
            if (doc.textFrames[i].label === label) {
                return doc.textFrames[i];
            }
        }
        return null;
    }

    /**
     * Apply caption formatting
     */
    function formatCaption(frame) {
        try {
            // Set font and size
            frame.paragraphs[0].appliedFont = app.fonts.itemByName(CONFIG.captionFontName);
            frame.paragraphs[0].pointSize = CONFIG.captionFontSize;
            
            // Set color
            frame.paragraphs[0].appliedFont.fillColor = doc.activeLayer.parent.swatches.itemByName(CONFIG.captionColor);
        } catch (e) {
            // Silently fail if formatting unavailable
        }
    }

    /**
     * Logging utility
     */
    function log(msg) {
        $.writeln(msg);
    }

    // ============================================================================
    // ENTRY POINT
    // ============================================================================

    try {
        var success = main();
        if (success) {
            alert(SCRIPT_NAME + ": Ready for caption injection.\nSee console for details.");
        }
    } catch (e) {
        alert(SCRIPT_NAME + " ERROR: " + e.message);
        $.writeln("Stack trace:");
        $.writeln(e.stack);
    }
})();
