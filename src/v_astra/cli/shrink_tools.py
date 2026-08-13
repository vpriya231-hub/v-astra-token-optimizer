from pathlib import Path
from ..catalog.shrink import shrink_tools


def run(path: str, output: str | None = None) -> int:
    source = Path(path).read_text(encoding="utf-8")
    optimized, handle = shrink_tools(source)
    target = Path(output) if output else Path(path).with_suffix(".min.json")
    target.write_text(optimized, encoding="utf-8")
    before, after = len(source.encode()), len(optimized.encode())
    print(f"Input bytes:    {before}")
    print(f"Output bytes:   {after}")
    print(f"Byte savings:   {0 if before == 0 else 1-after/before:.2%}")
    print(f"Recovery:       {handle or 'unchanged / not needed'}")
    return 0
