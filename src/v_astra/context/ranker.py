from ..models import ContextItem


def rank(items: list[ContextItem]) -> list[ContextItem]:
    return sorted(items, key=lambda item: (item.critical, item.priority), reverse=True)
