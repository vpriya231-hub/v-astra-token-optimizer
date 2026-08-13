import json


def compact_json(content: str) -> str:
    data = json.loads(content)
    return json.dumps(data, separators=(",", ":"), ensure_ascii=False)
