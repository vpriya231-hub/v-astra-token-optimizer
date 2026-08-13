from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ClaudeInputPolicy:
    """Input-side policy tuned for Claude Code style workloads.

    This is a policy layer, not a claim that Claude Code is intercepted. Phase 4
    will add the local provider proxy needed for automatic traffic rewriting.
    """
    shrink_tool_catalogs: bool = True
    deduplicate_context: bool = True
    preserve_errors_and_diffs: bool = True
    compact_repeated_tool_results: bool = True
    reversible_transforms: bool = True
    target_input_savings: float = 0.30


def default_policy() -> ClaudeInputPolicy:
    return ClaudeInputPolicy()
