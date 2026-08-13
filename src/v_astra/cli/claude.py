"""CLI entry point for Claude Code hook integration."""

from __future__ import annotations

import json
import sys
from typing import Any

from v_astra.integrations.claude_code import ClaudeCodeAdapter


def run() -> int:
    """Read one JSON payload from stdin, optimize it, and emit JSON to stdout."""
    try:
        raw = sys.stdin.read()
        payload: Any = json.loads(raw)
        if not isinstance(payload, dict):
            raise ValueError("Claude Code hook payload must be a JSON object")
        result = ClaudeCodeAdapter().optimize_payload(payload)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"vastra claude-hook: {exc}", file=sys.stderr)
        return 2
