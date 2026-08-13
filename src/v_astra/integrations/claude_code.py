"""Claude Code integration for V-Astra Token Optimizer Phase 5.

The integration is intentionally stdlib-only and hook-friendly:
- accepts Claude Code-style JSON payloads
- optimizes the user prompt/content locally
- preserves unrelated fields
- never calls an external API
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from v_astra.provider.request import optimize_request


class ClaudeCodeAdapter:
    """Optimize Claude Code hook payloads using the existing V-Astra pipeline."""

    name = "claude-code"

    def optimize_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        result = deepcopy(payload)

        # Claude Code UserPromptSubmit-style payload.
        if isinstance(result.get("prompt"), str):
            optimized, _report = optimize_request(
                {"model": "claude-code", "messages": [{"role": "user", "content": result["prompt"]}]}
            )
            result["prompt"] = optimized["messages"][0]["content"]

        # Also support generic message/input payloads for future hook variants.
        for key in ("messages", "input"):
            if key in result:
                optimized, _report = optimize_request(
                    {"model": "claude-code", key: result[key]}
                )
                result[key] = optimized[key]

        return result
