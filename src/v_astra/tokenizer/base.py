from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class TokenCount:
    count: int
    backend: str
    exact: bool


class TokenizerBackend(Protocol):
    name: str

    def count(self, text: str) -> TokenCount:
        """Return a deterministic token count for text."""
        ...
