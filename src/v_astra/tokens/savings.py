def savings_ratio(original: int, optimized: int) -> float:
    if original <= 0:
        return 0.0
    return max(0.0, 1.0 - optimized / original)
