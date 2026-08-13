from pathlib import Path
from ..tokens.counter import estimate_tokens
from ..optimizer import optimize
from ..catalog.shrink import shrink_tools


def run(path: str) -> int:
    content = Path(path).read_text(encoding="utf-8")
    generic = optimize(content)
    tool = generic
    try:
        shrunk, _ = shrink_tools(content)
        tool_tokens = estimate_tokens(shrunk)
        if tool_tokens < generic.optimized_tokens:
            tool = type(generic)(estimate_tokens(content), tool_tokens, shrunk, 1.0, shrunk != content)
    except (ValueError, TypeError):
        pass
    print("V-Astra Phase 3 comparison")
    print(f"Input tokens:        {estimate_tokens(content)}")
    print(f"Phase 2 output:      {generic.optimized_tokens}")
    print(f"Phase 3 best output: {tool.optimized_tokens}")
    print(f"Phase 3 savings:     {tool.savings_ratio:.2%}")
    return 0
