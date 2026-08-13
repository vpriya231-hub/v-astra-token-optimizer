from v_astra.benchmark import default_cases, run_benchmark
from v_astra.provider.request import optimize_request

def run() -> int:
    results = run_benchmark(default_cases(), optimize_request)
    original = sum(r.original_bytes for r in results)
    optimized = sum(r.optimized_bytes for r in results)
    saved = sum(r.bytes_saved for r in results)
    changed = sum(r.changed for r in results)
    print("V Astra Token Optimizer — Phase 6 Real-world Benchmark")
    print("=" * 58)
    for r in results:
        print(f"{r.name:28} {r.original_bytes:6} -> {r.optimized_bytes:6} bytes  "
              f"{r.savings_percent:6.2f}%  {r.elapsed_ms:7.3f} ms")
    print("-" * 58)
    print(f"Cases changed:       {changed}/{len(results)}")
    print(f"Original bytes:      {original}")
    print(f"Optimized bytes:     {optimized}")
    print(f"Bytes saved:         {saved}")
    print(f"Overall savings:     {(saved/original*100) if original else 0:.2f}%")
    return 0

if __name__ == "__main__":
    raise SystemExit(run())
