from __future__ import annotations

import copy
import json
import re
from typing import Any

from ..recovery.store import store

_DROP_KEYS = {
    "examples", "example", "deprecated", "title", "x-examples", "x-documentation",
}
_CONSTRAINT_SENTENCE = re.compile(r"[^.!?]*(?:must|should|required|only|cannot|cannot be|valid|allowed|format|enum|pattern|minimum|maximum|limit|timeout)[^.!?]*[.!?]", re.I)


def _shorten_description(value: str, max_chars: int = 260) -> str:
    value = " ".join(value.split())
    if len(value) <= max_chars:
        return value
    lead = value[:150].rsplit(" ", 1)[0]
    constraints = _CONSTRAINT_SENTENCE.findall(value)
    parts = [lead]
    for sentence in constraints:
        sentence = " ".join(sentence.split())
        if sentence not in parts and sum(len(p) + 1 for p in parts) + len(sentence) <= max_chars:
            parts.append(sentence)
    return " ".join(parts)[:max_chars].rstrip() + "…"


def _walk(node: Any) -> Any:
    if isinstance(node, list):
        return [_walk(x) for x in node]
    if not isinstance(node, dict):
        return node
    out = {}
    for key, value in node.items():
        if key in _DROP_KEYS:
            continue
        if key == "description" and isinstance(value, str):
            out[key] = _shorten_description(value)
        else:
            out[key] = _walk(value)
    return out


def _catalog_shape(data: Any) -> tuple[str | None, list[dict[str, Any]] | None]:
    if isinstance(data, list) and all(isinstance(x, dict) for x in data):
        return None, data
    if isinstance(data, dict) and isinstance(data.get("tools"), list):
        return "tools", data["tools"]
    return None, None


def shrink_tools(content: str, recovery_root: str | None = None) -> tuple[str, str | None]:
    """Shrink a JSON tool catalog. Returns (json, recovery_handle).

    The transformation is fail-open: malformed JSON, unsupported shapes, or a
    non-smaller result return the original content and no handle.
    """
    data = json.loads(content)
    key, tools = _catalog_shape(data)
    if tools is None:
        return content, None
    candidate = _walk(copy.deepcopy(data))
    encoded = json.dumps(candidate, ensure_ascii=False, separators=(",", ":"))
    if len(encoded) >= len(content):
        return content, None
    handle = store(content, recovery_root)
    return encoded, handle
