from ..compose import fallback, plan_ask

SEARCH_ONLY = fallback._is_a_hedge

PRIORITY = -999


def respond(text, memory):
    clean = fallback._matchable(fallback._plain((memory.get("understood") or {}).get("clean") or text))
    pool = plan_ask.plan_ask_pool(clean, memory)
    if pool is None:
        return None
    said = fallback.reply_for(text, memory)
    if not SEARCH_ONLY(said or ""):
        return None
    return fallback._choose(pool, memory, fallback._matchable(text))
