from ..models import ContextItem


def analyze(content: str, source: str = "unknown") -> ContextItem:
    lowered = content.lower()

    if "traceback" in lowered or "error:" in lowered:
        content_type = "error"
        critical = True
    elif "diff --git" in lowered or lowered.startswith("@@"):
        content_type = "diff"
        critical = True
    elif content.lstrip().startswith(("{", "[")):
        content_type = "json"
        critical = False
    else:
        content_type = "text"
        critical = False

    return ContextItem(
        content=content,
        source=source,
        content_type=content_type,
        priority=1.0 if critical else 0.5,
        critical=critical,
    )
