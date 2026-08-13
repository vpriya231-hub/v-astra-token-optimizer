from dataclasses import dataclass
from .compression.code import compress_code
from .compression.json import compact_json
from .compression.logs import compress_logs
from .compression.terminal import compress_terminal_output
from .compression.text import compress_text
from .models import OptimizationResult
from .safety.fallback import safe_fallback
from .tokens.counter import estimate_tokens

@dataclass(frozen=True)
class OptimizationPolicy:
    minimum_retention_score: float = 0.995
    minimum_savings_ratio: float = 0.0
    safe_mode: bool = True

def _classify(content: str) -> str:
    s, low = content.lstrip(), content.lower()
    if s.startswith(("{", "[")): return "json"
    if "traceback (most recent call last)" in low or "error:" in low: return "log"
    if s.startswith(("diff --git", "@@ ")): return "diff"
    if "command not found" in low or "$ " in content or "> " in content: return "terminal"
    if any(x in content for x in ("def ", "class ", "import ", "package ", "fun ")): return "code"
    return "text"

def _transform(content: str, kind: str) -> str:
    if kind == "json":
        try: return compact_json(content)
        except ValueError: return content
    if kind == "log": return compress_logs(content)
    if kind == "terminal": return compress_terminal_output(content)
    if kind == "code": return compress_code(content)
    return compress_text(content)

def _critical_lines(content: str) -> set[str]:
    markers = ("traceback (most recent call last)", "error:", "exception", "fatal:",
               "command not found", "permission denied", "diff --git", "@@ ")
    return {l.strip() for l in content.splitlines()
            if l.strip() and any(m in l.lower() for m in markers)}

def _retention_score(original: str, optimized: str) -> float:
    critical = _critical_lines(original)
    if not critical: return 1.0
    kept = {l.strip() for l in optimized.splitlines()}
    return len(critical & kept) / len(critical)

def optimize(content: str, policy: OptimizationPolicy | None = None) -> OptimizationResult:
    policy = policy or OptimizationPolicy()
    original_tokens = estimate_tokens(content)
    candidate = _transform(content, _classify(content))
    retention = _retention_score(content, candidate)
    result_content = (safe_fallback(content, candidate, retention, policy.minimum_retention_score)
                      if policy.safe_mode else candidate)
    optimized_tokens = estimate_tokens(result_content)
    savings = 0.0 if original_tokens == 0 else 1.0 - optimized_tokens / original_tokens
    if savings < policy.minimum_savings_ratio:
        result_content, optimized_tokens = content, original_tokens
    return OptimizationResult(original_tokens, optimized_tokens, result_content,
                              retention, result_content != content)
