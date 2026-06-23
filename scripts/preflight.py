"""Automated preflight: audit the build inputs, save a report, reload it.

Reports are written to the local output area (``paths.preflight_dir()`` -- never
OneDrive) as a timestamped JSON plus a stable ``latest.json`` and ``latest.md``,
so each refinement pass can pick up exactly where the last one left off: the
preflight and the editing flow stay in harmony.
"""
from __future__ import annotations

import json
import re
import sys
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from paths import preflight_dir  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / "images" / "labeled"
CAPTION_MANIFEST = ROOT / "data" / "visceral-caption-manifest.csv"


def _mm(pt: float) -> float:
    return round(pt / 72 * 25.4, 1)


def _is_violet(space: str, vals: list[float]) -> bool:
    if space == "CMYK" and len(vals) == 4:
        return vals[1] > 60 and vals[0] > 40 and vals[2] < 30
    if space == "RGB" and len(vals) == 3:
        return vals[0] > 60 and vals[2] > 100 and vals[1] < vals[2] * 0.7
    return False


def audit_idml(idml: Path) -> dict:
    """Structural audit of an .idml file (or an already-unpacked directory)."""
    with tempfile.TemporaryDirectory() as tmp:
        if idml.is_file():
            with zipfile.ZipFile(idml) as zf:
                zf.extractall(tmp)
            base = Path(tmp)
        else:
            base = idml

        def read(rel: str) -> str:
            p = base / rel
            return p.read_text(encoding="utf-8", errors="ignore") if p.exists() else ""

        dm, pf, gx, fx, sx = (read(f) for f in (
            "designmap.xml", "Resources/Preferences.xml", "Resources/Graphic.xml",
            "Resources/Fonts.xml", "Resources/Styles.xml"))
        spreads = "".join(p.read_text(encoding="utf-8", errors="ignore")
                          for p in sorted(base.glob("Spreads/*.xml")))

        pw = re.search(r'\bPageWidth="([^"]+)"', pf)
        ph = re.search(r'\bPageHeight="([^"]+)"', pf)
        width = float(pw.group(1)) if pw else 0.0
        height = float(ph.group(1)) if ph else 0.0
        violets = [self_ for self_, space, val in re.findall(
            r'<Color\b[^>]*\bSelf="([^"]+)"[^>]*\bSpace="([^"]*)"[^>]*\bColorValue="([^"]*)"', gx)
            if _is_violet(space, [float(x) for x in val.split()] if val else [])]
        violet_use = sum(1 for m in re.finditer(r'StrokeColor="([^"]+)"', spreads)
                         if m.group(1) in violets)
        return {
            "file": str(idml),
            "page_mm": [_mm(width), _mm(height)] if width and height else None,
            "orientation": ("landscape" if width > height else "portrait") if width and height else "unknown",
            "layers": re.findall(r'<Layer\b[^>]*\bName="([^"]*)"', dm),
            "master_spreads": len(list(base.glob("MasterSpreads/*.xml"))),
            "pages": len(re.findall(r'<Page\b', spreads)),
            "fonts": sorted(set(re.findall(r'<FontFamily\b[^>]*\bName="([^"]*)"', fx))),
            "images_placed": len(re.findall(r'<(?:Image|EPS)\b', spreads)),
            "images_linked": spreads.count("LinkResourceURI"),
            "images_embedded": spreads.count("<Contents>"),
            "toc_style": ("TOCStyle" in sx) or ("TOCStyle" in pf),
            "violet_swatches": violets,
            "violet_stroke_usage": violet_use,
        }


def _chk(name: str, ok: bool, detail: str = "") -> dict:
    return {"check": name, "ok": bool(ok), "detail": detail}


def run_preflight(idml_path: Path | None = None) -> dict:
    report: dict = {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "assets": {
            "images_labeled": len(list(IMAGES.glob("*"))) if IMAGES.exists() else 0,
            "caption_manifest": CAPTION_MANIFEST.exists(),
        },
        "checks": [],
        "idml": None,
    }
    try:
        from agents.local_guard import is_enforced, scan_for_cloud_sdks
        report["offline_guard"] = is_enforced()
        report["cloud_sdk_findings"] = scan_for_cloud_sdks(ROOT / "scripts")
    except Exception:
        report["offline_guard"] = None

    checks = report["checks"]
    checks.append(_chk("images present", report["assets"]["images_labeled"] > 0,
                       f"{report['assets']['images_labeled']} files"))
    checks.append(_chk("caption manifest present", report["assets"]["caption_manifest"]))
    checks.append(_chk("no cloud-SDK usage", not report.get("cloud_sdk_findings"),
                       str(report.get("cloud_sdk_findings") or "clean")))

    if idml_path and Path(idml_path).exists():
        a = audit_idml(Path(idml_path))
        report["idml"] = a
        checks.append(_chk("layered (>1 layer)", len(a["layers"]) > 1, f"{len(a['layers'])} layer(s)"))
        checks.append(_chk("images linked not embedded", a["images_embedded"] == 0,
                           f"{a['images_embedded']} embedded"))
        checks.append(_chk("parent/master pages", a["master_spreads"] > 0))
        checks.append(_chk("generated TOC style", a["toc_style"]))
        checks.append(_chk("no purple stroke box", a["violet_stroke_usage"] == 0,
                           f"{a['violet_stroke_usage']} use(s); swatches {a['violet_swatches']}"))

    report["ok"] = all(c["ok"] for c in checks)
    _save(report)
    return report


def _markdown(report: dict) -> str:
    lines = [f"# Preflight - {report['generated']}", "",
             f"Overall: **{'PASS' if report.get('ok') else 'NEEDS WORK'}**", "",
             "| Check | Status | Detail |", "|---|---|---|"]
    for c in report["checks"]:
        lines.append(f"| {c['check']} | {'PASS' if c['ok'] else 'FAIL'} | {c['detail']} |")
    a = report.get("idml")
    if a:
        lines += ["", "## IDML", "",
                  f"- geometry: {a['page_mm']} mm ({a['orientation']})",
                  f"- layers: {a['layers']}",
                  f"- fonts: {', '.join(a['fonts'])}",
                  f"- images: {a['images_placed']} placed / {a['images_linked']} linked / {a['images_embedded']} embedded",
                  f"- TOC style: {a['toc_style']}",
                  f"- purple swatches: {a['violet_swatches']} (stroke uses: {a['violet_stroke_usage']})"]
    return "\n".join(lines) + "\n"


def _save(report: dict) -> None:
    d = preflight_dir()
    ts = re.sub(r"[^0-9]", "", report["generated"])
    (d / f"preflight-{ts}.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    (d / "latest.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    (d / "latest.md").write_text(_markdown(report), encoding="utf-8")


def load_latest() -> dict | None:
    p = preflight_dir() / "latest.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


if __name__ == "__main__":
    idml = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    rep = run_preflight(idml)
    print(json.dumps({"ok": rep["ok"], "checks": rep["checks"]}, indent=2))
    print("saved to", preflight_dir())
