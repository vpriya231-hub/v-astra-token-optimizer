from __future__ import annotations

import re
from dataclasses import dataclass

from ..models import ContextItem
from ..tokens.counter import estimate_tokens
from .ranker import rank


@dataclass(frozen=True)
class PackedContext:
    items: tuple[ContextItem, ...]
    original_tokens: int
    packed_tokens: int
    omitted_items: int

    @property
    def savings_ratio(self) -> float:
        if self.original_tokens <= 0:
            return 0.0
        return 1.0 - self.packed_tokens / self.original_tokens


def _key(content: str) -> str:
    return re.sub(r"\s+", " ", content).strip()


def deduplicate(items: list[ContextItem]) -> list[ContextItem]:
    seen: set[str] = set()
    result: list[ContextItem] = []
    for item in rank(items):
        key = _key(item.content)
        if key and key in seen:
            continue
        if key:
            seen.add(key)
        result.append(item)
    return result


def pack(items: list[ContextItem], budget_tokens: int) -> PackedContext:
    if budget_tokens < 1:
        raise ValueError("budget_tokens must be positive")
    original_tokens = sum(estimate_tokens(i.content) for i in items)
    unique = deduplicate(items)
    selected: list[ContextItem] = []
    used = 0
    for item in unique:
        cost = estimate_tokens(item.content)
        if item.critical or used + cost <= budget_tokens:
            selected.append(item)
            used += cost
        if used >= budget_tokens:
            break
    return PackedContext(tuple(selected), original_tokens, used, len(items) - len(selected))
