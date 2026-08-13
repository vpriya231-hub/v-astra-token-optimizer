from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Iterable
import json
import time

@dataclass(frozen=True)
class BenchmarkCase:
    name: str
    payload: dict[str, Any]

@dataclass(frozen=True)
class BenchmarkResult:
    name: str
    original_bytes: int
    optimized_bytes: int
    bytes_saved: int
    savings_ratio: float
    changed: bool
    transformations: tuple[str, ...]
    elapsed_ms: float

    @property
    def savings_percent(self) -> float:
        return self.savings_ratio * 100.0

def _size(payload: dict[str, Any]) -> int:
    return len(json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))

def _transformations(report: Any) -> tuple[str, ...]:
    if report is None:
        return ()
    value = getattr(report, "transformations", None)
    if value is None and isinstance(report, dict):
        value = report.get("transformations")
    return tuple(str(x) for x in (value or ()))

def run_benchmark(cases: Iterable[BenchmarkCase], optimizer: Callable):
    results = []
    for case in cases:
        original = _size(case.payload)
        start = time.perf_counter()
        optimized, report = optimizer(case.payload)
        elapsed = (time.perf_counter() - start) * 1000
        new_size = _size(optimized)
        saved = max(original - new_size, 0)
        results.append(BenchmarkResult(
            case.name, original, new_size, saved,
            saved / original if original else 0.0,
            optimized != case.payload,
            _transformations(report), elapsed
        ))
    return results

def default_cases():
    repeated = "The system should preserve the requested context. " * 18
    return [
        BenchmarkCase("claude-code-hook", {
            "prompt": repeated, "session_id": "benchmark-session",
            "hook_event_name": "UserPromptSubmit"}),
        BenchmarkCase("openai-compatible-messages", {
            "messages": [
                {"role": "system", "content": repeated},
                {"role": "user", "content": "Summarize the request."}],
            "model": "benchmark-model"}),
        BenchmarkCase("generic-input", {
            "input": repeated, "metadata": {"source": "phase6", "keep": True}}),
        BenchmarkCase("repetitive-text", {
            "prompt": "hello\n\nhello\n\nhello\n\nhello\n\nhello"}),
        BenchmarkCase("json-in-content", {
            "messages": [{"role": "user", "content": json.dumps(
                {"task": "optimize", "notes": repeated}, ensure_ascii=False)}]}),
        BenchmarkCase("mixed-metadata", {
            "prompt": repeated, "session_id": "phase6",
            "cwd": "/tmp/project", "extra": {"keep": True, "priority": "normal"}}),
    ]
