from v_astra.optimizer import optimize
def test_repeated_content_reduces_tokens():
    r=optimize("line\nline\nline\nline\n"); assert r.changed; assert r.optimized_tokens < r.original_tokens
def test_error_is_preserved():
    r=optimize("hello\nERROR: database unavailable\nERROR: database unavailable\n")
    assert "ERROR: database unavailable" in r.content and r.retention_score >= .995
def test_json_compaction():
    r=optimize('{\n  "name": "V-Astra",\n  "enabled": true\n}')
    assert r.changed and '"name":"V-Astra"' in r.content
