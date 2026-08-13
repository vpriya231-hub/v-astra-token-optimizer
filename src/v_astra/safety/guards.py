def preserve_critical(original: str, optimized: str, critical_markers: list[str]) -> str:
    for marker in critical_markers:
        if marker in original and marker not in optimized:
            return original
    return optimized
