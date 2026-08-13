import json
from v_astra.benchmark import BenchmarkCase, default_cases, run_benchmark

class Report:
    transformations = ("content-compression",)

def fake_optimizer(payload):
    result = json.loads(json.dumps(payload))
    if isinstance(result.get("prompt"), str):
        result["prompt"] = result["prompt"].replace("\n\n", "\n")
    return result, Report()

def test_default_cases_are_nonempty():
    cases = default_cases()
    assert len(cases) == 6
    assert all(isinstance(c, BenchmarkCase) for c in cases)

def test_benchmark_measures_savings_and_transformations():
    result = run_benchmark(
        [BenchmarkCase("sample", {"prompt": "hello\n\nworld", "keep": True})],
        fake_optimizer,
    )[0]
    assert result.changed is True
    assert result.bytes_saved > 0
    assert result.savings_ratio > 0
    assert result.transformations == ("content-compression",)

def test_unchanged_payload_has_zero_savings():
    result = run_benchmark(
        [BenchmarkCase("unchanged", {"prompt": "hello"})],
        lambda payload: (dict(payload), None),
    )[0]
    assert result.changed is False
    assert result.bytes_saved == 0
    assert result.savings_ratio == 0.0

def test_unicode_is_measured_as_utf8():
    result = run_benchmark(
        [BenchmarkCase("unicode", {"prompt": "മലയാളം"})],
        lambda payload: (dict(payload), None),
    )[0]
    expected = len(json.dumps({"prompt": "മലയാളം"}, ensure_ascii=False,
                              separators=(",", ":")).encode("utf-8"))
    assert result.original_bytes == expected
