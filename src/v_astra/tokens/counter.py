def estimate_tokens(text: str) -> int:
    # Conservative provider-neutral estimate for Phase 1.
    # Phase 2 will add pluggable tokenizer backends.
    if not text:
        return 0
    return max(1, (len(text) + 3) // 4)
