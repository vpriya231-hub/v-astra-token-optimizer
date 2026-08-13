from ..models import ContextItem
from .ranker import rank


def select(items: list[ContextItem], limit: int = 200) -> list[ContextItem]:
    return rank(items)[:limit]
