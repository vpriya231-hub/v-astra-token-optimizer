from __future__ import annotations
import json
from dataclasses import dataclass
from typing import Any, Callable
from .request import OptimizationReport, optimize_request

@dataclass
class GatewayResult:
    request: dict[str, Any]
    report: OptimizationReport
    response: Any = None

class OptimizationGateway:
    """Local provider wrapper; transport and credentials remain with the caller."""
    def __init__(self, sender: Callable[[dict[str, Any]], Any]):
        self._sender = sender
    def send(self, payload: dict[str, Any]) -> GatewayResult:
        optimized, report = optimize_request(payload)
        return GatewayResult(optimized, report, self._sender(optimized))

def optimize_request_json(text: str) -> tuple[str, OptimizationReport]:
    payload = json.loads(text)
    if not isinstance(payload, dict):
        raise ValueError("request JSON must contain an object at the top level")
    optimized, report = optimize_request(payload)
    return json.dumps(optimized, ensure_ascii=False, separators=(",", ":")), report
