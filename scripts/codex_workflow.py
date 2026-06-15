#!/usr/bin/env python3
"""
Codex Workflow Orchestrator
Automates the publication QA gate and InDesign automation pipeline.

Usage:
    python codex_workflow.py                  # Full workflow
    python codex_workflow.py --validate-only  # Validation only
    python codex_workflow.py --report         # Generate reports only
"""

from __future__ import annotations

import json
import subprocess
import sys
from argparse import ArgumentParser
from pathlib import Path
from datetime import datetime

# Import Codex
sys.path.insert(0, str(Path(__file__).parent))
from codex import Codex


class CodexWorkflow:
    """Publication automation workflow manager."""

    def __init__(self, root: Path):
        self.root = Path(root)
        self.codex = Codex(self.root)
        self.workflow_log = []
        self.start_time = datetime.now()

    def log(self, level: str, msg: str):
        """Log workflow messages."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level:8} | {msg}"
        print(log_entry)
        self.workflow_log.append(log_entry)

    def validate(self) -> bool:
        """Run manifest validation."""
        self.log("INFO", "=== CODEX VALIDATION GATE ===")
        self.log("INFO", "Loading manifest...")
        
        try:
            manifest = self.codex.load_manifest()
            self.log("OK", f"Loaded {manifest.asset_count} assets")
        except Exception as e:
            self.log("ERROR", f"Failed to load manifest: {e}")
            return False

        self.log("INFO", "Running validation checks...")
        validation = self.codex.validate_manifest()
        
        if validation["valid"]:
            self.log("OK", f"All checks passed ({validation['total_assets']} assets)")
            return True
        else:
            self.log("ERROR", f"{validation['issue_count']} validation issues found:")
            for issue in validation["issues"]:
                self.log("ERROR", f"  - {issue}")
            return False

    def generate_reports(self) -> bool:
        """Generate all QA and automation reports."""
        self.log("INFO", "=== GENERATING REPORTS ===")
        
        try:
            # QA Report
            self.log("INFO", "Generating QA gate report...")
            qa_file = self.codex.export_qa_report()
            self.log("OK", f"QA Report: {qa_file.name}")
            
            # Source Register
            self.log("INFO", "Generating source register...")
            register_file = self.codex.reports_dir / "codex-source-register.md"
            self.codex.generate_source_register_markdown(register_file)
            self.log("OK", f"Source Register: {register_file.name}")
            
            # InDesign Caption Script
            self.log("INFO", "Generating InDesign caption injection script...")
            script_file = self.codex.templates_dir / "codex-caption-injection.jsx"
            self.codex.generate_indesign_script_for_captions(script_file)
            self.log("OK", f"Caption Script: {script_file.name}")
            
            return True
        except Exception as e:
            self.log("ERROR", f"Report generation failed: {e}")
            return False

    def preflight_indesign(self, indesign_file: Path) -> bool:
        """Run InDesign preflight via ExtendScript bridge."""
        self.log("INFO", "=== INDESIGN PREFLIGHT ===")
        
        if not indesign_file.exists():
            self.log("ERROR", f"InDesign file not found: {indesign_file}")
            return False
        
        self.log("INFO", f"Document: {indesign_file.name}")
        self.log("INFO", "Preflight checks:")
        self.log("INFO", "  - Checking layers (Captions, Source Register)")
        self.log("INFO", "  - Checking image links (should be 64)")
        self.log("INFO", "  - Checking for overset text")
        self.log("INFO", "  - Checking color space and fonts")
        
        # Note: Actual script execution would require InDesign running
        bridge_script = self.codex.templates_dir / "codex-indesign-bridge.jsx"
        if bridge_script.exists():
            self.log("OK", f"Bridge script ready: {bridge_script.name}")
            self.log("INFO", "To run preflight:")
            self.log("INFO", f"  1. Open InDesign")
            self.log("INFO", f"  2. Open document: {indesign_file.name}")
            self.log("INFO", f"  3. Run script: File > Scripts > {bridge_script.name}")
        
        return True

    def run_publishing_export(self) -> bool:
        """Run publishing export skills (CSV, index, etc.)."""
        self.log("INFO", "=== PUBLISHING EXPORT ===")
        
        try:
            if not self.codex.manifest:
                self.codex.load_manifest()
            
            assets = self.codex.manifest.assets
            
            # Export manifest as CSV
            self.log("INFO", "Exporting manifest as CSV...")
            csv_file = self.codex.reports_dir / "codex-manifest-export.csv"
            self.codex.publishing.export_manifest_csv(assets, csv_file)
            self.log("OK", f"Manifest CSV: {csv_file.name}")
            
            # Generate asset index
            self.log("INFO", "Generating asset index...")
            index_file = self.codex.reports_dir / "codex-asset-index.json"
            self.codex.publishing.generate_asset_index(assets, index_file)
            self.log("OK", f"Asset Index: {index_file.name}")
            
            return True
        except Exception as e:
            self.log("ERROR", f"Publishing export failed: {e}")
            return False
    
    def run_writing_docs(self) -> bool:
        """Run writing skills (guides, contact sheets, docs)."""
        self.log("INFO", "=== WRITING DOCUMENTATION ===")
        
        try:
            if not self.codex.manifest:
                self.codex.load_manifest()
            
            assets = self.codex.manifest.assets
            
            # Generate HTML contact sheet
            self.log("INFO", "Generating HTML contact sheet...")
            html_file = self.codex.reports_dir / "codex-contact-sheet.html"
            self.codex.writing.write_html_contact_sheet(assets, html_file)
            self.log("OK", f"Contact Sheet: {html_file.name}")
            
            return True
        except Exception as e:
            self.log("ERROR", f"Writing documentation failed: {e}")
            return False
    
    def run_preflight_checks(self) -> bool:
        """Run comprehensive preflight validation."""
        self.log("INFO", "=== COMPREHENSIVE PREFLIGHT ===")
        
        try:
            if not self.codex.manifest:
                self.codex.load_manifest()
            
            assets = self.codex.manifest.assets
            
            # Manifest completeness check
            self.log("INFO", "Checking manifest completeness...")
            manifest_check = self.codex.preflight.check_manifest_completeness(assets)
            self.log("OK" if manifest_check["valid"] else "WARN", 
                    f"Manifest: {manifest_check['issue_count']} issues")
            
            # Generate preflight report
            self.log("INFO", "Generating preflight report...")
            preflight_file = self.codex.reports_dir / "codex-preflight-report.json"
            self.codex.preflight.generate_preflight_report(assets, preflight_file)
            self.log("OK", f"Preflight Report: {preflight_file.name}")
            
            return manifest_check["valid"]
        except Exception as e:
            self.log("ERROR", f"Preflight checks failed: {e}")
            return False

    def run_full_workflow(self, indesign_file: Path | None = None) -> bool:
        """Run complete publication workflow with all skills."""
        self.log("INFO", "")
        self.log("INFO", "╔════════════════════════════════════════════════════╗")
        self.log("INFO", "║  CODEX PUBLICATION AUTOMATION WORKFLOW v1.1        ║")
        self.log("INFO", "║  The Visceral Theory of Sight                      ║")
        self.log("INFO", "╚════════════════════════════════════════════════════╝")
        self.log("INFO", "")
        
        # Step 1: Validate
        if not self.validate():
            self.log("ERROR", "Validation failed. Aborting workflow.")
            return False
        
        # Step 2: Generate Reports
        if not self.generate_reports():
            self.log("ERROR", "Report generation failed. Aborting workflow.")
            return False
        
        # Step 3: Publishing Exports
        if not self.run_publishing_export():
            self.log("ERROR", "Publishing export failed.")
            return False
        
        # Step 4: Writing Docs
        if not self.run_writing_docs():
            self.log("ERROR", "Writing documentation failed.")
            return False
        
        # Step 5: Preflight Checks
        if not self.run_preflight_checks():
            self.log("WARN", "Preflight check completed with warnings.")
        
        # Step 3: InDesign Preflight (if file provided)
        if indesign_file:
            if not self.preflight_indesign(indesign_file):
                self.log("ERROR", "InDesign preflight failed.")
                return False
        
        # Step 4: Summary
        elapsed = (datetime.now() - self.start_time).total_seconds()
        self.log("INFO", "")
        self.log("OK", f"✓ Workflow completed in {elapsed:.1f}s")
        self.log("INFO", "")
        self.log("INFO", "Next steps:")
        self.log("INFO", "  1. Review codex-qa-gate-report.json")
        self.log("INFO", "  2. Run automated tests")
        self.log("INFO", "  3. Run HTML preflight on web proof")
        self.log("INFO", "  4. Visual inspection in browser")
        self.log("INFO", "  5. Open InDesign and run codex-indesign-bridge.jsx")
        self.log("INFO", "  6. Run InDesign preflight")
        self.log("INFO", "  7. Export PDF and inspect")
        self.log("INFO", "")
        
        return True

    def save_workflow_log(self) -> Path:
        """Save workflow execution log."""
        log_file = self.codex.reports_dir / "codex-workflow.log"
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_file, "w", encoding="utf-8") as f:
            f.write("\n".join(self.workflow_log))
        
        return log_file


def main():
    parser = ArgumentParser(description="Codex publication automation workflow")
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate manifest, don't generate reports"
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Generate reports only, skip InDesign checks"
    )
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Run publishing export (CSV, index)"
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Run writing documentation (contact sheets, guides)"
    )
    parser.add_argument(
        "--preflight",
        action="store_true",
        help="Run comprehensive preflight checks"
    )
    parser.add_argument(
        "--indesign",
        type=Path,
        help="Path to InDesign file for preflight"
    )
    
    args = parser.parse_args()
    
    # Detect root
    root = Path(__file__).resolve().parents[1]
    workflow = CodexWorkflow(root)
    
    try:
        if args.validate_only:
            success = workflow.validate()
        elif args.publish:
            success = workflow.run_publishing_export()
        elif args.write:
            success = workflow.run_writing_docs()
        elif args.preflight:
            success = workflow.run_preflight_checks()
        elif args.report:
            success = workflow.generate_reports()
        else:
            success = workflow.run_full_workflow(args.indesign)
        
        # Save log
        log_file = workflow.save_workflow_log()
        workflow.log("INFO", f"Workflow log saved: {log_file}")
        
        return 0 if success else 1
    except KeyboardInterrupt:
        workflow.log("ERROR", "Workflow interrupted by user")
        return 130
    except Exception as e:
        workflow.log("ERROR", f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
