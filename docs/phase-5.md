# Phase 5 — Claude Code Integration

## Goal

Connect the existing V-Astra optimization engine to Claude Code's local hook-style
JSON flow without introducing a network dependency.

## What this overlay adds

- `src/v_astra/integrations/claude_code.py`
  - `ClaudeCodeAdapter`
  - optimizes `prompt`, `messages`, or `input`
  - preserves unrelated Claude Code metadata
- `src/v_astra/cli/claude.py`
  - reads one JSON object from stdin
  - emits one optimized JSON object to stdout
  - exits with code `2` for invalid input
- `tests/test_phase5.py`
  - prompt optimization
  - metadata preservation
  - message payload support
  - CLI round-trip
  - invalid payload handling

## Important

This package does not call Claude, Anthropic, or any remote API. It only transforms
the hook payload locally using the Phase 4 provider optimization layer.

## CLI registration

After copying the overlay, add these two pieces to
`src/v_astra/cli/main.py`:

```python
from .claude import run as claude_run
```

Inside `build_parser()`:

```python
h = sub.add_parser("claude-hook", help="optimize a Claude Code hook JSON payload")
```

Inside `main()` before the final fallback:

```python
if a.command == "claude-hook": raise SystemExit(claude_run())
```

Then the hook command can be used as:

```bash
echo '{"prompt":"hello\n\n\nworld"}' | python -m v_astra.cli.main claude-hook
```

The expected JSON contains the optimized prompt while preserving other fields.

## Validation

Run:

```bash
python -m pytest -q
```

Phase 5 is complete when the full test suite passes and the Claude hook
round-trip test succeeds.

## Scope boundary

Phase 5 is the Claude Code integration layer. Real-world performance/usage
benchmarking is intentionally deferred to Phase 6.
