# Phase 7 — Tokenizer Backend Abstraction

## Objective
Introduce a provider-neutral token counting interface so optimization and benchmarking
can use real tokenizer implementations when available, while keeping the core package
dependency-free.

## Design
- `TokenizerBackend` defines the stable backend contract.
- `TokenCount` records the count, backend name, and whether the result is exact.
- `ByteFallbackTokenizer` is deterministic and explicitly marked non-exact.
- `TiktokenBackend` is an optional exact backend for models supported by `tiktoken`.
- `TokenizerRegistry` provides explicit backend registration and lookup.
- No provider credentials or network calls are required.

## Safety requirements
- Never label a heuristic/byte count as exact.
- Optional dependencies are imported lazily.
- Invalid model/backend configuration raises a clear error.
- Token counting must not mutate the supplied text.
- Unicode input must be handled deterministically.

## Acceptance criteria
- Phase 1–6 behavior remains intact.
- Phase 7 tests pass without optional dependencies.
- Optional `tiktoken` integration is isolated and clearly identified as exact only when
  the library performs the actual model encoding.
- No network access is performed by the tokenizer layer.
