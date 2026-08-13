from .repetition import collapse_consecutive_duplicates
def compress_terminal_output(content: str) -> str:
    return collapse_consecutive_duplicates(content)
