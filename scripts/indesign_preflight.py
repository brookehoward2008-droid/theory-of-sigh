"""Read an Adobe InDesign preflight report (exported as PDF).

InDesign exports preflight results as a PDF with a 'Document:' line, a
'Preflight Profile Used:' line, an Error/Page table, and 'Nothing to do.'
(or 'No errors') when the document is clean. This lets the engine fetch
InDesign's own authoritative findings and fold them into the fix-until-green
loop alongside the structural IDML checks.
"""
from __future__ import annotations

import re
from pathlib import Path


def parse_report(pdf_path: Path) -> dict:
    import fitz  # PyMuPDF, installed by `build.py --setup`

    doc = fitz.open(str(pdf_path))
    text = "\n".join(doc.load_page(i).get_text() for i in range(doc.page_count))

    def grab(label: str) -> str | None:
        m = re.search(rf"{re.escape(label)}\s*(.+)", text)
        return m.group(1).strip() if m else None

    clean = bool(re.search(r"nothing to do|no errors", text, re.I))
    errors: list[str] = []
    if not clean:
        skip = {"error", "page", "indesign preflight report", ""}
        for line in text.splitlines():
            s = line.strip()
            if s.lower() in skip or s.endswith(".indd") or s.startswith("Document:") \
                    or s.startswith("Preflight Profile"):
                continue
            errors.append(s)

    return {
        "document": grab("Document:"),
        "profile": grab("Preflight Profile Used:"),
        "clean": clean,
        "errors": errors,
        "pages": doc.page_count,
    }


if __name__ == "__main__":
    import json
    import sys
    print(json.dumps(parse_report(Path(sys.argv[1])), indent=2))
