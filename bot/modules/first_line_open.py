from ..compose import fallback
from ..compose.fallback_data import A_RECEIPT_OF_NOTHING, COLD_OPEN
from . import greeting

PRIORITY = -999.5


def _has_a_turn_behind_it(memory):
    for one in (memory.get("turns") or []):
        if isinstance(one, dict) and str(one.get("bot") or "").strip():
            return True
    return False


def respond(text, memory):
    if _has_a_turn_behind_it(memory):
        return None
    try:
        reply = greeting.respond(text, memory)
    except Exception:
        return None
    if not reply or not A_RECEIPT_OF_NOTHING.search(str(reply)):
        return None
    clean = " ".join(str(text or "").split())
    return fallback._choose(COLD_OPEN, memory, clean)
