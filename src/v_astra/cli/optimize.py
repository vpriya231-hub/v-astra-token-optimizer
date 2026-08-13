from pathlib import Path
from ..optimizer import OptimizationPolicy, optimize
def run(path, output=None, safe=True):
    p=Path(path); r=optimize(p.read_text(encoding="utf-8"), OptimizationPolicy(safe_mode=safe))
    print(f"Tokens: {r.original_tokens} -> {r.optimized_tokens}")
    print(f"Savings: {r.savings_ratio:.1%} | Retention: {r.retention_score:.1%}")
    if output: Path(output).write_text(r.content,encoding="utf-8"); print(f"Output: {output}")
    else: print("\n--- Optimized content ---\n"+r.content)
    return 0
