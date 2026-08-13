def remove_excessive_blank_lines(content: str) -> str:
    result = []
    for line in content.splitlines():
        if line.strip():
            result.append(line)
    return "\n".join(result)

def collapse_consecutive_duplicates(content: str, minimum_repeats: int = 3) -> str:
    lines, result, i = content.splitlines(), [], 0
    while i < len(lines):
        j = i + 1
        while j < len(lines) and lines[j] == lines[i]: j += 1
        count = j - i
        if count >= minimum_repeats and lines[i].strip():
            result.append(f"{lines[i]} [x{count}]")
        else:
            result.extend(lines[i:j])
        i = j
    return "\n".join(result)

def compress_repetition(content: str) -> str:
    """Apply the existing repetition compression passes."""
    result = remove_excessive_blank_lines(content)
    return collapse_consecutive_duplicates(result)
