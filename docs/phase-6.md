# Phase 6 — Real-world Benchmark

## Objective
Measure the existing optimizer against realistic AI request shapes without
calling any provider API.

## Cases
- Claude Code hook-style payload
- OpenAI-compatible messages
- generic input payload
- repetitive text
- JSON embedded in message content
- mixed metadata + prompt payload

## Metrics
Original UTF-8 bytes, optimized UTF-8 bytes, bytes saved, savings percentage,
changed/unchanged, transformations, and local execution time.

## Acceptance criteria
- Phases 1–5 remain intact.
- Phase 6 tests pass.
- Benchmark is fully offline.
- Metadata is preserved.
- Fixtures contain no secrets or personal data.
