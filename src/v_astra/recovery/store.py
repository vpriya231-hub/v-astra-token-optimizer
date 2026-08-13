from __future__ import annotations

import hashlib
import json
from pathlib import Path

PREFIX = "vastra_ccr_"


def _root(root: str | Path | None = None) -> Path:
    return Path(root or (Path.home() / ".vastra" / "recovery"))


def store(content: str, root: str | Path | None = None) -> str:
    data = content.encode("utf-8")
    digest = hashlib.sha256(data).hexdigest()
    directory = _root(root)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{PREFIX}{digest}.json"
    if not path.exists():
        path.write_text(json.dumps({"sha256": digest, "content": content}, ensure_ascii=False), encoding="utf-8")
    return f"{PREFIX}{digest}"


def recover(handle: str, root: str | Path | None = None) -> str:
    if not handle.startswith(PREFIX):
        raise ValueError("invalid recovery handle")
    path = _root(root) / f"{handle}.json"
    if not path.exists():
        raise FileNotFoundError(handle)
    record = json.loads(path.read_text(encoding="utf-8"))
    content = record["content"]
    digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
    if digest != record.get("sha256") or digest != handle.removeprefix(PREFIX):
        raise ValueError("recovery integrity check failed")
    return content
