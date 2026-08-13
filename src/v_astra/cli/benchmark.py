from pathlib import Path
from ..optimizer import optimize
def run(path):
    r=optimize(Path(path).read_text(encoding="utf-8"))
    print("V-Astra Benchmark\n=================\n"
          f"Input tokens: {r.original_tokens}\nOutput tokens: {r.optimized_tokens}\n"
          f"Token savings: {r.savings_ratio:.2%}\nRetention score: {r.retention_score:.2%}")
    return 0
