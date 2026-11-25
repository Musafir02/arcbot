
from ..compose import fallback
from ..compose.the_shape_without_the_fact import the_shape_without_the_fact

PRIORITY = -999.5

_A_HEADS = 40


def _the_reply_is_only_a_placeholder(reply):
    said = " ".join(str(reply or "").lower().split())
    if not said:
        return False
    if fallback._in_a_pool(reply, (fallback.NEUTRAL,)):
        return True
    return said[:_A_HEADS] in [line.lower()[:_A_HEADS] for line in fallback.UNKNOWN]


def _the_composer_would_hedge(text, memory):
    try:
        reply = fallback.reply_for(text, memory)
    except Exception:
        return False
    return _the_reply_is_only_a_placeholder(reply)


def _the_floor_would_say_a_placeholder(text, memory):
    try:
        from . import greeting
        reply = greeting.respond(text, _a_copy_of(memory))
    except Exception:
        return False
    return _the_reply_is_only_a_placeholder(reply)


def _a_copy_of(memory):
    try:
        import copy
        return {key: value if key == "turns" else copy.deepcopy(value)
                for key, value in memory.items()}
    except Exception:
        return dict(memory)


def _a_thread_with_a_person_in_trouble(memory):
    for reader in ("_in_a_care_thread", "_in_a_loss_thread", "_in_a_crisis_thread",
                   "_thread_is_about_the_body"):
        try:
            if getattr(fallback, reader)(memory):
                return True
        except Exception:
            continue
    return False


def respond(text, memory):
    if not isinstance(memory, dict):
        return None
    understood = memory.get("understood")
    if not isinstance(understood, dict):
        return None
    pool = the_shape_without_the_fact(understood, memory)
    if pool is None:
        return None
    if _a_thread_with_a_person_in_trouble(memory):
        return None
    if not _the_composer_would_hedge(text, memory):
        return None
    if not _the_floor_would_say_a_placeholder(text, memory):
        return None
    clean = understood.get("clean") or " ".join(str(text or "").lower().split())
    return fallback._choose(pool, memory, clean)
