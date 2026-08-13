from __future__ import annotations

from typing import Dict

from .base import TokenCount, TokenizerBackend


class ByteFallbackTokenizer:
    """Deterministic dependency-free baseline; deliberately not an exact token count."""

    name = "byte-fallback"

    def count(self, text: str) -> TokenCount:
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        return TokenCount(
            count=len(text.encode("utf-8")),
            backend=self.name,
            exact=False,
        )


class TiktokenBackend:
    """Optional exact tokenizer backed by the installed tiktoken package."""

    def __init__(self, model: str):
        if not isinstance(model, str) or not model.strip():
            raise ValueError("model must be a non-empty string")
        self.model = model
        self.name = f"tiktoken:{model}"

    def count(self, text: str) -> TokenCount:
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        try:
            import tiktoken
        except ImportError as exc:
            raise RuntimeError(
                "tiktoken is required for the exact tiktoken backend; "
                "install it with `pip install tiktoken`"
            ) from exc

        encoding = tiktoken.encoding_for_model(self.model)
        return TokenCount(
            count=len(encoding.encode(text)),
            backend=self.name,
            exact=True,
        )


class TokenizerRegistry:
    def __init__(self, backends: Dict[str, TokenizerBackend] | None = None):
        self._backends: Dict[str, TokenizerBackend] = dict(backends or {})

    def register(self, backend: TokenizerBackend) -> None:
        name = getattr(backend, "name", None)
        if not isinstance(name, str) or not name:
            raise ValueError("backend must expose a non-empty name")
        self._backends[name] = backend

    def get(self, name: str) -> TokenizerBackend:
        try:
            return self._backends[name]
        except KeyError as exc:
            raise KeyError(f"unknown tokenizer backend: {name}") from exc

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._backends))


def default_registry() -> TokenizerRegistry:
    registry = TokenizerRegistry()
    registry.register(ByteFallbackTokenizer())
    return registry
