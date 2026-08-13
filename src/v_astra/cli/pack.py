from pathlib import Path
from ..context.analyzer import analyze
from ..context.pack import pack


def run(paths: list[str], budget: int, output: str | None = None) -> int:
    items = [analyze(Path(p).read_text(encoding="utf-8"), p) for p in paths]
    result = pack(items, budget)
    text = "\n\n".join(f"### {i.source}\n{i.content}" for i in result.items)
    if output:
        Path(output).write_text(text, encoding="utf-8")
    else:
        print(text)
    print(f"\nOriginal tokens: {result.original_tokens}")
    print(f"Packed tokens:   {result.packed_tokens}")
    print(f"Savings:         {result.savings_ratio:.2%}")
    print(f"Omitted items:   {result.omitted_items}")
    return 0
