"""Copy-editing skills powered by the local Ollama prose model.

All run token-free against local Ollama. When Ollama is not running the skills
degrade gracefully (return the input or a clear placeholder) so a build never
blocks on copy generation.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agents.ollama_client import POET_SYSTEM, OllamaClient  # noqa: E402

from . import skill


@skill("refine_copy", kind="copy",
       summary="Rewrite a passage in the book's dark, spare house voice.")
def refine_copy(text: str, instruction: str = "tighten and darken; keep the meaning") -> str:
    client = OllamaClient.for_task("prose")
    if not client.available():
        return text  # offline: leave copy untouched
    return client.generate(
        f"Rewrite the passage below. {instruction}.\n\nPASSAGE:\n{text}",
        system=POET_SYSTEM, temperature=0.7)


@skill("generate_poem", kind="copy",
       summary="Write a short dark-poetry passage for a section opener.")
def generate_poem(section: str = "Introduction", motif: str = "the veil and the gaze") -> str:
    client = OllamaClient.for_task("prose")
    if not client.available():
        return f"[poem unavailable offline - start Ollama to generate '{section}']"
    return client.generate(
        f"Write a 4-6 line dark, spare poem for the section '{section}', circling the "
        f"motif of {motif}. Lyric fragments, not exposition.",
        system=POET_SYSTEM, temperature=0.95)
