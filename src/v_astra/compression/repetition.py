def remove_excessive_blank_lines(content: str) -> str:
    lines = content.splitlines()
    result: list[str] = []
    blank_seen = False

    for line in lines:
        if not line.strip():
            if blank_seen:
                continue
            blank_seen = True
        else:
            blank_seen = False
        result.append(line)

    return "\n".join(result)
