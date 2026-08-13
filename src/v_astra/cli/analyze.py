from pathlib import Path
from ..optimizer import _classify
from ..tokens.counter import estimate_tokens
def run(path):
    p=Path(path); c=p.read_text(encoding="utf-8")
    print(f"File: {p}\nCharacters: {len(c)}\nLines: {len(c.splitlines())}\nType: {_classify(c)}\nToken est.: {estimate_tokens(c)}")
    return 0
