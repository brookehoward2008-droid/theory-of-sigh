"""Hard 'no cloud, no tokens' guarantee for the publication engine.

The engine must run entirely on the local machine -- local Ollama only, no API
keys, no cloud round-trips that could burn metered time. This module enforces
that two ways:

  * ``enforce_local_only()`` blocks any socket connection to a non-loopback
    address at runtime, so a stray import cannot phone home.
  * ``scan_for_cloud_sdks()`` statically flags cloud LLM SDKs / non-local URLs
    in the engine source.
"""
from __future__ import annotations

import ipaddress
import socket
from pathlib import Path

_REAL_CONNECT = socket.socket.connect
_LOOPBACK_NAMES = {"localhost", "127.0.0.1", "::1"}

# Cloud LLM SDKs / hosted endpoints the engine must never depend on.
_FORBIDDEN = (
    "import anthropic", "from anthropic", "import openai", "from openai",
    "google.generativeai", "import cohere", "replicate",
    "api.openai.com", "api.anthropic.com", "googleapis.com",
)


def _is_local(address) -> bool:
    try:
        host = address[0]
    except (TypeError, IndexError):
        return True  # non-INET sockets (AF_UNIX, etc.) are local by nature
    if host in _LOOPBACK_NAMES:
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def enforce_local_only() -> None:
    """Patch sockets so only loopback connections succeed. Idempotent."""
    if is_enforced():
        return

    def guarded_connect(self, address):
        if not _is_local(address):
            raise OSError(
                f"offline engine: blocked non-local connection to {address!r} "
                "(local Ollama only; no API tokens, no cloud)."
            )
        return _REAL_CONNECT(self, address)

    guarded_connect._local_guard = True  # type: ignore[attr-defined]
    socket.socket.connect = guarded_connect  # type: ignore[assignment]


def is_enforced() -> bool:
    return getattr(socket.socket.connect, "_local_guard", False)


def scan_for_cloud_sdks(root: Path) -> list[str]:
    """Human-readable findings of cloud-LLM usage in ``*.py`` under ``root``."""
    findings: list[str] = []
    self_name = Path(__file__).name
    for path in sorted(Path(root).rglob("*.py")):
        if path.name == self_name:
            continue  # this module legitimately defines the patterns it scans for
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for needle in _FORBIDDEN:
            if needle in text:
                findings.append(f"{path.name}: contains {needle!r}")
    return findings
