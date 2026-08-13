# Phase 2 — Working Optimization Engine

Phase 2 adds a real local optimization pipeline:

Input → classify → type-aware transform → retention check → safe fallback → savings report.

## CLI
`vastra analyze file.txt`
`vastra optimize file.txt -o optimized.txt`
`vastra benchmark file.txt`

Safe mode is enabled by default. Provider-specific exact tokenizers and deeper repository-aware optimization are planned for later phases.
