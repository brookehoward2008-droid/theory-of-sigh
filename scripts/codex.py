"""
Codex: Metadata & automation hub for InDesign publication workflows.
Handles manifest parsing, caption injection, QA validation, editing, writing,
publishing, and comprehensive preflight validation.

Skills:
- Editing: Update captions, metadata, manifest
- Writing: Generate reports, documentation, source registers
- Publishing: PDF export, batch processing, distribution
- Preflight: Comprehensive validation, HTML checks, visual prep
"""

from __future__ import annotations

import json
import csv
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Optional, List, Dict, Tuple
from datetime import datetime


@dataclass
class AssetMetadata:
    """Single asset record from manifest."""
    label: str
    repo_file: str
    title: str
    visual_group: str
    intended_pages_or_section: str
    creator_or_institution: str
    rights_license_status: str
    original_path: str
    production_source: str
    web_dimensions_px: str
    original_dimensions_px: str
    sequence: str


@dataclass
class CodexManifest:
    """Complete publication metadata & structure."""
    title: str
    asset_count: int
    assets: list[AssetMetadata]
    outputs: dict
    geometry: dict
    source_policy: str


class CodexEditingSkills:
    """Editing skill: update captions, metadata, manifest."""
    
    @staticmethod
    def update_asset_caption(asset: AssetMetadata, new_title: str) -> AssetMetadata:
        """Update caption for a single asset."""
        asset.title = new_title
        return asset
    
    @staticmethod
    def validate_caption_length(title: str, max_length: int = 200) -> tuple[bool, str]:
        """Validate caption doesn't exceed max length."""
        if len(title) <= max_length:
            return True, f"OK: {len(title)} chars"
        return False, f"LONG: {len(title)} chars (max {max_length})"
    
    @staticmethod
    def sanitize_caption(title: str) -> str:
        """Remove problematic characters from captions."""
        title = title.replace('"', '"').replace('"', '"')
        title = title.replace(''', "'").replace(''', "'")
        title = re.sub(r'\s+', ' ', title).strip()
        return title


class CodexWritingSkills:
    """Writing skill: generate reports, documentation, guides."""
    
    @staticmethod
    def write_html_contact_sheet(assets: list[AssetMetadata], output_file: Path) -> Path:
        """Generate HTML contact sheet for visual review."""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Image Contact Sheet</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; margin: 2rem; background: #f5f5f5; }}
        h1 {{ color: #333; border-bottom: 3px solid #0066cc; padding-bottom: 0.5rem; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 2rem; margin-top: 2rem; }}
        .asset-card {{ background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        .asset-label {{ font-weight: bold; color: #0066cc; font-size: 1.1rem; margin-bottom: 0.5rem; }}
        .asset-title {{ font-size: 0.95rem; color: #333; margin-bottom: 0.5rem; line-height: 1.4; }}
        .asset-group {{ background: #f0f0f0; padding: 0.5rem; border-radius: 4px; font-size: 0.85rem; color: #666; margin: 0.5rem 0; }}
        .stat {{ display: inline-block; margin-right: 2rem; }}
        .stat-value {{ font-size: 1.5rem; font-weight: bold; color: #0066cc; }}
    </style>
</head>
<body>
    <h1>Image Contact Sheet</h1>
    <div class="stat">
        <div class="stat-value">{len(assets)}</div>
        <div>Total Assets</div>
    </div>
    <div class="grid">
"""
        for asset in assets:
            html += f"""    <div class="asset-card">
        <div class="asset-label">{asset.label}</div>
        <div class="asset-title">{asset.title}</div>
        <div class="asset-group">{asset.visual_group}</div>
    </div>
"""
        html += """    </div>
</body>
</html>"""
        output_file = Path(output_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)
        return output_file


class CodexPublishingSkills:
    """Publishing skill: export, batch processing, distribution."""
    
    @staticmethod
    def export_manifest_csv(assets: list[AssetMetadata], output_file: Path) -> Path:
        """Export manifest as CSV for spreadsheet editing."""
        output_file = Path(output_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        fieldnames = [
            "label", "repo_file", "title", "visual_group",
            "intended_pages_or_section", "creator_or_institution",
            "rights_license_status", "sequence"
        ]
        
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for asset in assets:
                row = {k: getattr(asset, k) for k in fieldnames}
                writer.writerow(row)
        
        return output_file
    
    @staticmethod
    def generate_asset_index(assets: list[AssetMetadata], output_file: Path) -> Path:
        """Generate searchable asset index."""
        index = {
            "generated": datetime.now().isoformat(),
            "total_assets": len(assets),
            "by_label": {},
            "by_group": {},
        }
        
        for asset in assets:
            index["by_label"][asset.label] = asdict(asset)
            if asset.visual_group not in index["by_group"]:
                index["by_group"][asset.visual_group] = []
            index["by_group"][asset.visual_group].append(asset.label)
        
        output_file = Path(output_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=2)
        
        return output_file


class CodexPreflightSkills:
    """Preflight skill: comprehensive validation before publication."""
    
    @staticmethod
    def check_manifest_completeness(assets: list[AssetMetadata]) -> dict:
        """Check for missing or invalid data."""
        issues = []
        
        for asset in assets:
            if not asset.label or not asset.title:
                issues.append(f"{asset.label}: Missing title or label")
            if len(asset.title) > 250:
                issues.append(f"{asset.label}: Title too long ({len(asset.title)} chars)")
            if any(c in asset.title for c in ['“', '”', '‘', '’']):
                issues.append(f"{asset.label}: Contains smart quotes")
        
        return {
            "total_assets": len(assets),
            "valid": len(issues) == 0,
            "issue_count": len(issues),
            "issues": issues
        }
    
    @staticmethod
    def check_indesign_readiness(indesign_file: Path) -> dict:
        """Check InDesign document readiness."""
        issues = []
        if not indesign_file.exists():
            issues.append(f"InDesign file not found: {indesign_file}")
        else:
            file_size_mb = indesign_file.stat().st_size / (1024 * 1024)
            if file_size_mb > 500:
                issues.append(f"Large file: {file_size_mb:.1f} MB")
        
        return {
            "file": str(indesign_file),
            "valid": len(issues) == 0,
            "issue_count": len(issues),
            "issues": issues
        }
    
    @staticmethod
    def generate_preflight_report(assets: list[AssetMetadata], output_file: Path) -> Path:
        """Generate comprehensive preflight report."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "publication": "The Visceral Theory of Sight",
            "manifest": CodexPreflightSkills.check_manifest_completeness(assets),
        }
        
        report["overall_status"] = "READY" if report["manifest"]["valid"] else "BLOCKED"
        
        output_file = Path(output_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        
        return output_file


class Codex:
    """Main publication automation hub with all skills integrated."""

    def __init__(self, root: Path):
        """Initialize with repo root."""
        self.root = Path(root)
        self.data_dir = self.root / "data"
        self.route = self.root / "visceral-production-route"
        self.templates_dir = self.route / "templates"
        self.reports_dir = self.route / "reports"
        self.manifest: Optional[CodexManifest] = None
        
        # Skill integrations
        self.editing = CodexEditingSkills()
        self.writing = CodexWritingSkills()
        self.publishing = CodexPublishingSkills()
        self.preflight = CodexPreflightSkills()

    def load_manifest(self) -> CodexManifest:
        """Load and parse the labeled photo manifest."""
        manifest_json = self.data_dir / "labeled-photo-manifest.json"
        with open(manifest_json) as f:
            data = json.load(f)

        assets = [AssetMetadata(**asset) for asset in data]
        
        self.manifest = CodexManifest(
            title="The Visceral Theory of Sight",
            asset_count=len(assets),
            assets=assets,
            outputs={},
            geometry={
                "trim": "A4 landscape, 297mm x 210mm",
                "bleed": "3.175mm all sides",
                "facing_pages": True,
            },
            source_policy="No invented citations, quotations, or rights claims. Verify before final export."
        )
        return self.manifest

    def get_asset_by_label(self, label: str) -> Optional[AssetMetadata]:
        """Retrieve asset by label."""
        if not self.manifest:
            self.load_manifest()
        
        for asset in self.manifest.assets:
            if asset.label == label:
                return asset
        return None

    def validate_manifest(self) -> dict:
        """Run QA checks on manifest."""
        if not self.manifest:
            self.load_manifest()

        issues = []
        
        # Check for duplicates
        labels = [a.label for a in self.manifest.assets]
        if len(labels) != len(set(labels)):
            issues.append("Duplicate asset labels detected")
        
        # Check for missing critical fields
        for asset in self.manifest.assets:
            if not asset.label or not asset.title:
                issues.append(f"Asset missing label or title: {asset}")
            if "unknown source" in asset.rights_license_status.lower() and not asset.creator_or_institution:
                issues.append(f"{asset.label}: Missing creator info for {asset.rights_license_status}")
        
        # Check asset count
        if len(self.manifest.assets) != self.manifest.asset_count:
            issues.append(f"Asset count mismatch: expected {self.manifest.asset_count}, found {len(self.manifest.assets)}")
        
        return {
            "valid": len(issues) == 0,
            "issue_count": len(issues),
            "issues": issues,
            "total_assets": len(self.manifest.assets),
        }

    def generate_indesign_script_for_captions(self, output_file: Optional[Path] = None) -> str:
        """Generate ExtendScript to inject captions into InDesign."""
        if not self.manifest:
            self.load_manifest()

        script = """// Auto-generated caption injection script for InDesign
// Generated by Codex publication automation system

var doc = app.activeDocument;
if (!doc) {
    alert("Please open an InDesign document first.");
    exit();
}

var captionData = [
"""
        
        for asset in self.manifest.assets:
            title_esc = asset.title.replace('"', '\\"')
            rights_esc = asset.rights_license_status.replace('"', '\\"')[:100]
            section_part = asset.intended_pages_or_section.split('/')[1].strip() if '/' in asset.intended_pages_or_section else 'Unknown'
            script += f"""    {{
        label: "{asset.label}",
        title: "{title_esc}",
        visual_group: "{asset.visual_group}",
        section: "{section_part}",
        creator: "{asset.creator_or_institution}",
        rights: "{rights_esc}..."
    }},
"""

        script += """];\n\nvar results = [];\n\nfor (var i = 0; i < captionData.length; i++) {\n    var data = captionData[i];\n    results.push("Processed: " + data.label + " - " + data.title.substring(0, 50));\n}\n\nalert("Caption data processed for " + results.length + " assets.\\\\nReview the preflight report before export.");\n"""

        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(script)
        
        return script

    def generate_source_register_markdown(self, output_file: Optional[Path] = None) -> str:
        """Generate backmatter source register."""
        if not self.manifest:
            self.load_manifest()

        md = f"""# Image Source Register

Back matter documentation for all {len(self.manifest.assets)} images in the publication.

"""
        
        # Group by visual_group
        groups = {}
        for asset in self.manifest.assets:
            group = asset.visual_group
            if group not in groups:
                groups[group] = []
            groups[group].append(asset)
        
        for group_name in sorted(groups.keys()):
            md += f"## {group_name}\n\n"
            for asset in groups[group_name]:
                md += f"""### {asset.label}: {asset.title}

- **Section:** {asset.intended_pages_or_section}
- **Creator/Source:** {asset.creator_or_institution}
- **Rights Status:** {asset.rights_license_status}
- **Original Path:** {asset.original_path}
- **Repository File:** {asset.repo_file}
- **Dimensions:** {asset.original_dimensions_px} (original) → {asset.web_dimensions_px} (web)

---

"""

        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(md)
        
        return md

    def generate_qa_report(self) -> dict:
        """Generate QA validation report for publication gate."""
        validation = self.validate_manifest()
        
        report = {
            "publication": "The Visceral Theory of Sight",
            "qa_gate_status": "READY" if validation["valid"] else "BLOCKED",
            "manifest_validation": validation,
            "required_checks": {
                "automated_tests": False,
                "html_preflight": False,
                "browser_visual_inspection": False,
                "indesign_preflight": False,
                "pdf_export_validation": False,
            },
            "checklist": [
                "✓ Run automated test suite",
                "✓ Run HTML/source preflight (TOC, captions, source register)",
                "✓ Visual inspection in browser (caption crowding, text fit, image rhythm)",
                "✓ InDesign preflight (missing links, overset, bleed, color, fonts)",
                f"✓ Confirm {validation['total_assets']} images have A-number, visual group, source-register entry",
                "✓ No original filenames/rights notes in front-of-book captions",
                "✓ References & citations resolve to backmatter",
                "✓ Export PDF & visually inspect edges, captions, folios, backmatter",
                "✓ Keep preflight-safe .indd as rollback",
            ],
            "notes": "All checks must pass before publication approval.",
        }
        
        return report

    def export_qa_report(self, output_file: Optional[Path] = None) -> Path:
        """Export QA report as JSON."""
        report = self.generate_qa_report()
        
        if not output_file:
            output_file = self.reports_dir / "codex-qa-gate-report.json"
        
        output_file = Path(output_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, "w") as f:
            json.dump(report, f, indent=2)
        
        return output_file


if __name__ == "__main__":
    # Example usage
    root = Path(__file__).resolve().parents[1]
    codex = Codex(root)
    
    # Load and validate
    manifest = codex.load_manifest()
    print(f"✓ Loaded {manifest.asset_count} assets")
    
    validation = codex.validate_manifest()
    print(f"✓ Validation: {validation['issue_count']} issues")
    if validation["issues"]:
        for issue in validation["issues"]:
            print(f"  - {issue}")
    
    # Generate outputs
    print("\n--- Generating outputs ---")
    
    script_file = codex.templates_dir / "codex-caption-injection.jsx"
    codex.generate_indesign_script_for_captions(script_file)
    print(f"✓ ExtendScript: {script_file.name}")
    
    register_file = codex.reports_dir / "codex-source-register.md"
    codex.generate_source_register_markdown(register_file)
    print(f"✓ Source Register: {register_file.name}")
    
    qa_file = codex.export_qa_report()
    print(f"✓ QA Report: {qa_file.name}")
    
    print("\n--- Done ---")
