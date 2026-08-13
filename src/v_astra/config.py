from dataclasses import dataclass


@dataclass(frozen=True)
class OptimizerConfig:
    target_savings_ratio: float = 0.30
    minimum_retention_score: float = 0.995
    max_context_items: int = 200
    safe_mode: bool = True
