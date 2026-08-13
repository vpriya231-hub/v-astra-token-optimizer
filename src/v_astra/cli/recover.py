from ..recovery.store import recover


def run(handle: str, output: str | None = None) -> int:
    content = recover(handle)
    if output:
        from pathlib import Path
        Path(output).write_text(content, encoding="utf-8")
    else:
        print(content)
    return 0
