from dataclasses import dataclass
from typing import Literal


ContentType = Literal[
    "code", "text", "json", "log", "terminal", "diff", "error", "unknown"
]


@dataclass(frozen=True)
class ContextItem:
    content: str
    source: str = "unknown"
    content_type: ContentType = "unknown"
    priority: float = 0.5
    critical: bool = False


@dataclass(frozen=True)
class OptimizationResult:
    original_tokens: int
    optimized_tokens: int
    content: str
    retention_score: float
    changed: bool

    @property
    def savings_ratio(self) -> float:
        if self.original_tokens == 0:
            return 0.0
        return 1.0 - (self.optimized_tokens / self.original_tokens)
