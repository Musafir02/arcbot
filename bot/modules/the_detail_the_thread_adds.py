from ..compose import fallback, thread_detail

PRIORITY = -999


def respond(text, memory):
    clean = fallback._matchable(fallback._plain((memory.get("understood") or {}).get("clean") or text))
    pool = thread_detail.detail_pool(clean, memory)
    if not pool:
        return None
    said = fallback.reply_for(text, memory)
    if not thread_detail.says_nothing_about_the_line(said, fallback._matchable(text)):
        return None
    return fallback._choose(list(pool), memory, fallback._matchable(text))
