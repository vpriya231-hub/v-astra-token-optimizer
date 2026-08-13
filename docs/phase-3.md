# Phase 3 — Input Intelligence & Reversible Context Compression

Phase 3 moves V-Astra from simple content compression toward **input-side optimization** for AI coding agents.

## What is new

- JSON tool-catalog shrinking with structural preservation.
- Reversible content-addressed recovery handles before model-visible lossy transforms.
- Context deduplication and token-budget packing.
- Claude-oriented input policy profile.
- CLI commands: `shrink-tools`, `pack`, `recover`, `compare`.
- Fail-open behavior for unsupported/non-beneficial transformations.

## Claude Code goal

Claude Code spends input tokens on more than the assistant's final answer: tool definitions, tool results, files, logs, history and repeated context can all cross the provider boundary. Phase 3 targets those upstream payloads.

**Important:** Phase 3 does not yet transparently intercept Claude Code traffic. Phase 4 is planned to add the local provider proxy/wrapper layer that can apply these transformations automatically before provider requests.

## Safety model

1. Store exact original bytes before a lossy transform.
2. Transform only recognized structures.
3. Keep structural fields such as names, parameters, required fields and enums.
4. Pass through unchanged when the result is not smaller or cannot be parsed.
5. Verify recovery integrity with SHA-256.

## Benchmark rule

Do not claim superiority from inferred byte/token estimates alone. V-Astra will use a reproducible provider-traffic benchmark in a later phase and compare against a pinned Caveman baseline.
