from .repetition import remove_excessive_blank_lines, collapse_consecutive_duplicates

def compress_text(content: str) -> str:
    return collapse_consecutive_duplicates(remove_excessive_blank_lines(content))
