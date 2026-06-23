"""Layout-editing skills that operate on an unpacked IDML directory."""
from __future__ import annotations

import re
import zipfile
from pathlib import Path

from . import skill


def unpack_idml(idml: Path, dest: Path) -> Path:
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(idml) as zf:
        zf.extractall(dest)
    return dest


def repack_idml(src_dir: Path, out: Path) -> Path:
    """Re-zip an IDML. 'mimetype' must be stored first and uncompressed."""
    src_dir, out = Path(src_dir), Path(out)
    if out.exists():
        out.unlink()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        mt = src_dir / "mimetype"
        if mt.exists():
            zf.write(mt, "mimetype", compress_type=zipfile.ZIP_STORED)
        for p in sorted(src_dir.rglob("*")):
            if p.is_file() and p.name != "mimetype":
                zf.write(p, str(p.relative_to(src_dir)))
    return out


def _violet_swatches(graphic_xml: str) -> list[str]:
    out = []
    for self_, space, val in re.findall(
        r'<Color\b[^>]*\bSelf="([^"]+)"[^>]*\bSpace="([^"]*)"[^>]*\bColorValue="([^"]*)"', graphic_xml
    ):
        v = [float(x) for x in val.split()] if val else []
        if (space == "CMYK" and len(v) == 4 and v[1] > 60 and v[0] > 40 and v[2] < 30) or \
           (space == "RGB" and len(v) == 3 and v[0] > 60 and v[2] > 100 and v[1] < v[2] * 0.7):
            out.append(self_)
    return out


@skill("purge_purple_swatch", kind="layout",
       summary="Remove the purple/violet swatch and any stroke that uses it.")
def purge_purple_swatch(idml_dir: Path) -> dict:
    idml_dir = Path(idml_dir)
    gx_path = idml_dir / "Resources" / "Graphic.xml"
    gx = gx_path.read_text(encoding="utf-8", errors="ignore")
    violets = _violet_swatches(gx)
    result = {"candidate_swatches": violets, "stroke_fixes": 0, "removed_swatches": []}
    if not violets:
        return result

    targets = sorted(idml_dir.glob("Spreads/*.xml")) + sorted(idml_dir.glob("MasterSpreads/*.xml"))
    for sp in targets:
        text = sp.read_text(encoding="utf-8", errors="ignore")
        new = text
        for v in violets:
            new, n = re.subn(rf'StrokeColor="{re.escape(v)}"', 'StrokeColor="Swatch/None"', new)
            result["stroke_fixes"] += n
        if new != text:
            sp.write_text(new, encoding="utf-8")

    # Drop a swatch definition only if nothing references it any more (safe).
    corpus = "".join(p.read_text(encoding="utf-8", errors="ignore") for p in targets)
    corpus += (idml_dir / "Resources" / "Styles.xml").read_text(encoding="utf-8", errors="ignore") \
        if (idml_dir / "Resources" / "Styles.xml").exists() else ""
    new_gx = gx
    for v in violets:
        if corpus.count(f'"{v}"') == 0:
            new_gx = re.sub(rf'<Color\b[^>]*\bSelf="{re.escape(v)}"[^>]*?/>\s*', "", new_gx)
            result["removed_swatches"].append(v)
    if new_gx != gx:
        gx_path.write_text(new_gx, encoding="utf-8")
    return result


@skill("relink_images", kind="layout",
       summary="Re-point image links to a local Links/ folder (kills dead OneDrive paths).")
def relink_images(idml_dir: Path, links_dir: str = "Links") -> dict:
    idml_dir = Path(idml_dir)
    result = {"relinked": 0, "links_dir": links_dir}

    def repl(m: re.Match) -> str:
        uri = m.group(1)
        fname = uri.replace("\\", "/").rstrip("/").split("/")[-1]
        result["relinked"] += 1
        return f'LinkResourceURI="file:{links_dir}/{fname}"'

    for sp in sorted(idml_dir.glob("Spreads/*.xml")):
        text = sp.read_text(encoding="utf-8", errors="ignore")
        new = re.sub(r'LinkResourceURI="([^"]*)"', repl, text)
        if new != text:
            sp.write_text(new, encoding="utf-8")
    return result


@skill("ensure_layers", kind="layout",
       summary="Create named layers (background/images/type/captions) if missing.")
def ensure_layers(idml_dir: Path, names: tuple[str, ...] = ("background", "images", "type", "captions")) -> dict:
    idml_dir = Path(idml_dir)
    dm_path = idml_dir / "designmap.xml"
    dm = dm_path.read_text(encoding="utf-8", errors="ignore")
    existing = re.findall(r'<Layer\b[^>]*\bName="([^"]*)"', dm)
    to_add = [n for n in names if n not in existing]
    result = {"existing": existing, "added": to_add}
    if not to_add:
        return result

    m = re.search(r'<Layer\b[^>]*?/>', dm)
    if m:
        template, insert_at = m.group(0), m.end()
    else:
        template = ('<Layer Self="ugen" Name="x" Visible="true" Locked="false" '
                    'IgnoreWrapping="false" ShowGuides="true" LockGuides="false" '
                    'UI="true" Expendable="true" Printable="true"/>')
        opened = re.search(r'<Document\b[^>]*>', dm)
        insert_at = opened.end() if opened else 0

    clones = []
    for i, name in enumerate(to_add, 1):
        c = re.sub(r'\bSelf="[^"]*"', f'Self="uLayerGen{i}"', template)
        c = re.sub(r'\bName="[^"]*"', f'Name="{name}"', c)
        clones.append(c)
    dm = dm[:insert_at] + "".join(clones) + dm[insert_at:]
    dm_path.write_text(dm, encoding="utf-8")
    return result
