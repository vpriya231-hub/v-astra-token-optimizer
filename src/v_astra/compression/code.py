from .repetition import remove_excessive_blank_lines
def compress_code(content: str) -> str:
    return remove_excessive_blank_lines(content)
