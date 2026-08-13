# V-Astra Token Optimizer

Open-source context and token optimization engine for AI coding agents.

**License:** Apache-2.0  
**Status:** Phase 2 — Working Optimization Engine

Phase 2 provides repeated-content compression, JSON compaction, safe fallback, retention checks, token/savings reporting, and a local CLI.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
vastra analyze example.txt
vastra optimize example.txt -o optimized.txt
vastra benchmark example.txt
```

Token reduction alone is not considered success: safe mode preserves critical information and falls back to the original content when retention is insufficient.

Roadmap: exact tokenizer backends → repository-aware context ranking → tool-output optimization → provider/MCP integrations.
