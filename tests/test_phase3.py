import json
from pathlib import Path
from v_astra.catalog.shrink import shrink_tools
from v_astra.context.pack import pack
from v_astra.context.analyzer import analyze
from v_astra.recovery.store import recover


def test_tool_catalog_shrinks_and_recovers(tmp_path):
    original = json.dumps({"tools": [{"name": "search", "description": "Search files. " + "Verbose detail. " * 30, "inputSchema": {"type": "object", "properties": {"q": {"type": "string"}}, "required": ["q"]}}]})
    out, handle = shrink_tools(original, tmp_path)
    assert len(out) < len(original)
    assert handle
    assert recover(handle, tmp_path) == original
    data = json.loads(out)
    assert data["tools"][0]["name"] == "search"
    assert data["tools"][0]["inputSchema"]["required"] == ["q"]


def test_tool_catalog_fail_open():
    original = "not json"
    try:
        shrink_tools(original)
    except json.JSONDecodeError:
        pass
    else:
        raise AssertionError("malformed JSON should be rejected by the low-level shrinker")


def test_context_pack_deduplicates_and_preserves_critical():
    items = [
        analyze("normal context", "a"),
        analyze("normal context", "duplicate"),
        analyze("ERROR: permission denied", "error"),
    ]
    result = pack(items, budget_tokens=10)
    assert any(i.critical for i in result.items)
    assert len(result.items) == 2
