def safe_fallback(original: str, optimized: str, retention_score: float, minimum: float) -> str:
    return optimized if retention_score >= minimum else original
