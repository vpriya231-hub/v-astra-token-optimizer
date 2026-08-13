from .repetition import collapse_consecutive_duplicates
def compress_logs(content: str) -> str:
    return collapse_consecutive_duplicates(content)
