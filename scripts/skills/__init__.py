"""Composable engine skills for editing layout and copy.

Skills are small, named operations the engine can list and run:
  * layout skills edit an unpacked InDesign IDML (swatches, links, layers, ...),
  * copy skills rewrite text with the local Ollama models.

Register with ``@skill(name, kind, summary)``; run via ``run_skill(name, **kw)``.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass
class Skill:
    name: str
    kind: str  # "layout" | "copy"
    summary: str
    func: Callable


SKILLS: dict[str, Skill] = {}


def skill(name: str, kind: str, summary: str):
    def deco(func: Callable) -> Callable:
        SKILLS[name] = Skill(name=name, kind=kind, summary=summary, func=func)
        return func
    return deco


def _load_all() -> None:
    from . import layout, copy  # noqa: F401  (import side effect: registers skills)


def list_skills() -> list[Skill]:
    _load_all()
    return sorted(SKILLS.values(), key=lambda s: (s.kind, s.name))


def run_skill(name: str, **kwargs):
    _load_all()
    if name not in SKILLS:
        raise KeyError(f"unknown skill {name!r}; have {sorted(SKILLS)}")
    return SKILLS[name].func(**kwargs)
