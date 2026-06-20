"""Command-line front end for the Firefly Services InDesign API client.

Examples
--------
Test that your credentials work (mints a token, lists InDesign engine versions)::

    python -m scripts.indesign_api.cli app-versions

Render an InDesign document (reachable via a pre-signed URL) to a PDF that the
API uploads to a pre-signed PUT URL::

    python -m scripts.indesign_api.cli render \
        --asset-url "https://.../the-visceral-theory-of-sight-50pp.indd" \
        --target the-visceral-theory-of-sight-50pp.indd \
        --output-url "https://.../out.pdf?sig=..." \
        --output-name out.pdf

Inspect a document for missing links / fonts / overset before final export::

    python -m scripts.indesign_api.cli doc-info \
        --asset-url "https://.../book.indd" --target book.indd

Run ``python -m scripts.indesign_api.cli --help`` for the full list.
"""

from __future__ import annotations

import argparse
import json
import sys

from .config import Config, ConfigError
from .client import InDesignClient, InDesignAPIError, JobFailedError


def _client() -> InDesignClient:
    return InDesignClient(Config.from_env())


def _print(obj) -> None:
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def _progress(event) -> None:
    state = event.get("status", "?")
    msg = event.get("message", "")
    print(f"[job] {state} {msg}".rstrip(), file=sys.stderr)


def cmd_app_versions(args) -> int:
    _print(_client().list_app_versions())
    return 0


def cmd_scripts_list(args) -> int:
    _print(_client().list_custom_scripts(page=args.page))
    return 0


def cmd_doc_info(args) -> int:
    client = _client()
    event = client.document_info(
        assets=[client.asset(args.asset_url, args.target)],
        target_document=args.target,
        links=not args.no_links,
        fonts=not args.no_fonts,
        page_items=args.page_items,
        text_stories=args.text_stories,
        on_update=_progress,
    )
    _print(event)
    return 0


def cmd_render(args) -> int:
    client = _client()
    outputs = None
    if args.output_url:
        outputs = [client.output(args.output_url, args.output_name or "output.pdf")]
    params = {}
    if args.use_document_bleeds:
        params["useDocumentBleeds"] = True
    if args.pdf_preset:
        params["pdfPreset"] = args.pdf_preset
    if args.page_range:
        params["pageRange"] = args.page_range
    event = client.create_rendition(
        assets=[client.asset(args.asset_url, args.target)],
        target_document=args.target,
        output_media_type=args.media_type,
        outputs=outputs,
        params=params or None,
        on_update=_progress,
    )
    _print(event)
    return 0


def cmd_convert_pdf(args) -> int:
    client = _client()
    outputs = None
    if args.output_url:
        outputs = [client.output(args.output_url, args.output_name or "output.zip")]
    event = client.convert_pdf_to_indesign(
        assets=[client.asset(args.asset_url, args.target)],
        target_document=args.target,
        output_media_type=args.media_type,
        embed_links=args.embed_links,
        outputs=outputs,
        on_update=_progress,
    )
    _print(event)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m scripts.indesign_api.cli",
        description="Drive the Adobe Firefly Services InDesign API from the shell.",
    )
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("app-versions", help="List available InDesign engine versions (auth smoke test)")

    sp = sub.add_parser("scripts-list", help="List registered custom scripts")
    sp.add_argument("--page", type=int, default=0)

    sp = sub.add_parser("doc-info", help="Inspect an INDD/IDML (links, fonts, pages)")
    sp.add_argument("--asset-url", required=True, help="Pre-signed URL of the document")
    sp.add_argument("--target", required=True, help="Working-dir filename of the document")
    sp.add_argument("--no-links", action="store_true")
    sp.add_argument("--no-fonts", action="store_true")
    sp.add_argument("--page-items", action="store_true")
    sp.add_argument("--text-stories", action="store_true")

    sp = sub.add_parser("render", help="Render a document to PDF/PNG/JPEG")
    sp.add_argument("--asset-url", required=True)
    sp.add_argument("--target", required=True)
    sp.add_argument("--output-url", help="Pre-signed PUT URL to receive the result")
    sp.add_argument("--output-name", help="Result filename, e.g. book.pdf")
    sp.add_argument("--media-type", default="application/pdf",
                    choices=["application/pdf", "image/png", "image/jpeg"])
    sp.add_argument("--pdf-preset")
    sp.add_argument("--page-range", help="e.g. 'All' or '1-5'")
    sp.add_argument("--use-document-bleeds", action="store_true")

    sp = sub.add_parser("convert-pdf", help="Convert a PDF to INDD/IDML")
    sp.add_argument("--asset-url", required=True)
    sp.add_argument("--target", required=True, help="Working-dir filename of the PDF")
    sp.add_argument("--media-type", default="application/x-indesign",
                    choices=["application/x-indesign",
                             "application/vnd.adobe.indesign-idml-package"])
    sp.add_argument("--embed-links", action="store_true")
    sp.add_argument("--output-url")
    sp.add_argument("--output-name")

    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    handlers = {
        "app-versions": cmd_app_versions,
        "scripts-list": cmd_scripts_list,
        "doc-info": cmd_doc_info,
        "render": cmd_render,
        "convert-pdf": cmd_convert_pdf,
    }
    try:
        return handlers[args.command](args)
    except ConfigError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 2
    except JobFailedError as exc:
        print(f"Job failed: {exc}", file=sys.stderr)
        _print(exc.event)
        return 1
    except InDesignAPIError as exc:
        print(f"API error: {exc}", file=sys.stderr)
        if exc.body:
            print(exc.body, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
