import argparse
from .analyze import run as analyze_run
from .benchmark import run as benchmark_run
from .optimize import run as optimize_run
from .shrink_tools import run as shrink_tools_run
from .pack import run as pack_run
from .recover import run as recover_run
from .compare import run as compare_run

def build_parser():
    p = argparse.ArgumentParser(prog="vastra", description="V-Astra Token Optimizer")
    p.add_argument("--version", action="version", version="0.3.0a1")
    sub = p.add_subparsers(dest="command", required=True)
    o = sub.add_parser("optimize", help="optimize a file"); o.add_argument("path"); o.add_argument("-o","--output"); o.add_argument("--unsafe",action="store_true")
    a = sub.add_parser("analyze", help="analyze a file"); a.add_argument("path")
    b = sub.add_parser("benchmark", help="benchmark a file"); b.add_argument("path")
    s = sub.add_parser("shrink-tools", help="shrink a JSON tool catalog"); s.add_argument("path"); s.add_argument("-o","--output")
    c = sub.add_parser("pack", help="pack multiple context files into a token budget"); c.add_argument("paths", nargs="+"); c.add_argument("--budget", type=int, required=True); c.add_argument("-o","--output")
    r = sub.add_parser("recover", help="recover original content from a V-Astra handle"); r.add_argument("handle"); r.add_argument("-o","--output")
    x = sub.add_parser("compare", help="compare Phase 2 and Phase 3 optimization"); x.add_argument("path")
    return p

def main():
    a = build_parser().parse_args()
    if a.command == "optimize": raise SystemExit(optimize_run(a.path,a.output,not a.unsafe))
    if a.command == "analyze": raise SystemExit(analyze_run(a.path))
    if a.command == "benchmark": raise SystemExit(benchmark_run(a.path))
    if a.command == "shrink-tools": raise SystemExit(shrink_tools_run(a.path,a.output))
    if a.command == "pack": raise SystemExit(pack_run(a.paths,a.budget,a.output))
    if a.command == "recover": raise SystemExit(recover_run(a.handle,a.output))
    raise SystemExit(compare_run(a.path))

if __name__ == "__main__": main()
