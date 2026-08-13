from .repetition import remove_excessive_blank_lines


def compress_text(content: str) -> str:
    return remove_excessive_blank_lines(content)
