import argparse
from .analyze import run as analyze_run
from .benchmark import run as benchmark_run
from .optimize import run as optimize_run

def build_parser():
    p = argparse.ArgumentParser(prog="vastra", description="V-Astra Token Optimizer")
    p.add_argument("--version", action="version", version="0.2.0a1")
    sub = p.add_subparsers(dest="command", required=True)
    o = sub.add_parser("optimize", help="optimize a file"); o.add_argument("path"); o.add_argument("-o","--output"); o.add_argument("--unsafe",action="store_true")
    a = sub.add_parser("analyze", help="analyze a file"); a.add_argument("path")
    b = sub.add_parser("benchmark", help="benchmark a file"); b.add_argument("path")
    return p

def main():
    a = build_parser().parse_args()
    if a.command == "optimize": raise SystemExit(optimize_run(a.path,a.output,not a.unsafe))
    if a.command == "analyze": raise SystemExit(analyze_run(a.path))
    raise SystemExit(benchmark_run(a.path))

if __name__ == "__main__": main()
