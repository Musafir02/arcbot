from ..compose import fallback, kept_nearby

PRIORITY = -999

FALLBACK_MODULES = frozenset(("greeting", "chat"))


def _answered_by_the_fallback(memory):
    turns = (memory or {}).get("turns") or []
    if not turns:
        return False
    return str(turns[-1].get("module") or "") in FALLBACK_MODULES


def respond(text, memory):
    try:
        if not _answered_by_the_fallback(memory):
            return None
        nearby = kept_nearby.answer_for(text, memory)
        if not nearby:
            return None
        return fallback._choose(nearby, memory, text)
    except Exception:
        return None
