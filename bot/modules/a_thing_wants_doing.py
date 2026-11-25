from ..compose import a_thing_wants_doing, fallback
from . import greeting

PRIORITY = -999


def _the_thing_and_its_state(text, memory):
    understood = memory.get("understood") or {}
    clean = ((understood.get("clean") if isinstance(understood, dict) else None)
             or " ".join(str(text or "").lower().split()))
    return clean, a_thing_wants_doing.pool(clean, memory)


def respond(text, memory):
    clean, pool = _the_thing_and_its_state(text, memory)
    if not pool:
        return None
    said = greeting.respond(text, memory) or fallback.reply_for(text, memory)
    if not fallback._in_a_pool(said, (fallback.NEUTRAL,)):
        return None
    return fallback._choose(pool, memory, clean)
