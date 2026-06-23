"""Token-free local LLM client for the publication engine.

Talks to a local Ollama server (default http://127.0.0.1:11434), so copy and
caption generation cost nothing and need no API key — only localhost traffic.
If Ollama is not running, callers get a clear error and can fall back to the
hand-written copy already baked into the build.

The defaults match the OpenClaw gateway setup (model `mistral:latest`).
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass

DEFAULT_URL = "http://127.0.0.1:11434"
DEFAULT_MODEL = "mistral:latest"

# Task -> (fast model, quality model). All drawn from the local Ollama library
# the user already has installed, so every job runs token-free on a best-fit model.
MODELS = {
    "prose": ("mistral:latest", "llama3.3:70b"),          # house-voice copy, poem, captions
    "code": ("qwen2.5-coder:7b", "qwen3-coder:30b"),      # InDesign JSX / HTML / Python
    "reasoning": ("deepseek-r1:32b", "deepseek-r1:32b"),  # structure + layout planning
    "embed": ("nomic-embed-text:latest", "nomic-embed-text:latest"),  # semantic matching
}

# House voice for this title: darkly lyrical, sensory, image-led.
POET_SYSTEM = (
    "You are a darkly lyrical art-book editor for a visual-psychology issue on "
    "gaze, image memory, and the veil. Write spare, sensory, image-led prose. "
    "No cliches, no hashtags, no preamble or sign-off — return only the text."
)


@dataclass
class OllamaClient:
    url: str = DEFAULT_URL
    model: str = DEFAULT_MODEL
    timeout: float = 120.0

    def available(self) -> bool:
        """True if a local Ollama server answers on the tags endpoint."""
        try:
            urllib.request.urlopen(f"{self.url}/api/tags", timeout=3)
            return True
        except Exception:
            return False

    def models(self) -> list[str]:
        try:
            with urllib.request.urlopen(f"{self.url}/api/tags", timeout=3) as resp:
                data = json.load(resp)
            return [m.get("name", "") for m in data.get("models", [])]
        except Exception:
            return []

    def generate(
        self,
        prompt: str,
        system: str | None = None,
        temperature: float = 0.8,
    ) -> str:
        """Single-shot completion from the local model."""
        payload: dict = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": temperature},
        }
        if system:
            payload["system"] = system
        req = urllib.request.Request(
            f"{self.url}/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return json.load(resp).get("response", "").strip()
        except urllib.error.URLError as exc:
            raise RuntimeError(
                f"Ollama not reachable at {self.url}; start `ollama serve` "
                f"and `ollama pull {self.model}`."
            ) from exc

    def embed(self, text: str) -> list[float]:
        """Vector embedding via the local embedding model (nomic-embed-text)."""
        req = urllib.request.Request(
            f"{self.url}/api/embeddings",
            data=json.dumps({"model": self.model, "prompt": text}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            return json.load(resp).get("embedding", [])

    @classmethod
    def for_task(cls, task: str, quality: str = "fast", url: str = DEFAULT_URL) -> "OllamaClient":
        """Client pinned to the best local model for a task ('prose', 'code',
        'reasoning', 'embed'). quality='quality' selects the heavier model."""
        fast, best = MODELS.get(task, (DEFAULT_MODEL, DEFAULT_MODEL))
        return cls(url=url, model=best if quality == "quality" else fast)


def dark_caption(client: OllamaClient, image_description: str) -> str:
    """One evocative caption (<= 12 words) in the house voice."""
    return client.generate(
        f"Write ONE evocative caption, at most 12 words, for an image described "
        f"as: {image_description}",
        system=POET_SYSTEM,
        temperature=0.9,
    )


def section_poem(client: OllamaClient, section: str, motif: str) -> str:
    """A short dark-poetry passage for a section opener."""
    return client.generate(
        f"Write a 4-6 line dark, spare poem for the section '{section}', "
        f"circling the motif of {motif}. Lyric fragments, not exposition.",
        system=POET_SYSTEM,
        temperature=0.95,
    )
