from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
import copy
from ..compression.json import compact_json
from ..compression.repetition import compress_repetition

@dataclass(frozen=True)
class OptimizationReport:
    provider: str
    original_bytes: int
    optimized_bytes: int
    changed: bool
    transformations: tuple[str, ...] = field(default_factory=tuple)
    @property
    def savings_ratio(self) -> float:
        return 0.0 if self.original_bytes <= 0 else 1.0 - self.optimized_bytes / self.original_bytes

def _provider_name(payload: dict[str, Any]) -> str:
    provider = str(payload.get("_vastra_provider", "")).lower().strip()
    if provider: return provider
    if "messages" in payload and "system" in payload: return "anthropic-compatible"
    if "messages" in payload: return "openai-compatible"
    return "generic"

def _compact_messages(messages: Any) -> tuple[Any, bool]:
    if not isinstance(messages, list): return messages, False
    out, changed = [], False
    for msg in messages:
        if not isinstance(msg, dict):
            out.append(msg); continue
        item = copy.deepcopy(msg)
        value = item.get("content")
        if isinstance(value, str):
            new = compact_json(value) if value.lstrip().startswith(("{", "[")) else value
            new = compress_repetition(new)
            if new != value:
                item["content"] = new
                changed = True
        out.append(item)
    return out, changed

def optimize_request(payload: dict[str, Any]) -> tuple[dict[str, Any], OptimizationReport]:
    before = repr(payload).encode("utf-8")
    result = copy.deepcopy(payload)
    provider = _provider_name(result)
    transformations = []
    for key in ("messages", "input"):
        if key in result:
            optimized, changed = _compact_messages(result[key])
            if changed:
                result[key] = optimized
                transformations.append(f"{key}:content-compression")
    result.pop("_vastra_provider", None)
    after = repr(result).encode("utf-8")
    return result, OptimizationReport(provider, len(before), len(after), result != payload, tuple(transformations))
