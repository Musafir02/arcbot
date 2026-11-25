from ..compose import a_trouble, fallback

PRIORITY = -999


def respond(text, memory):
    clean = fallback._matchable(fallback._plain((memory.get("understood") or {}).get("clean") or text))
    pool = a_trouble.trouble_pool(clean, memory)
    if not pool:
        return None
    said = fallback.reply_for(text, memory)
    if not a_trouble.says_nothing_about_the_line(said, fallback._matchable(text)):
        return None
    return fallback._choose(list(pool), memory, fallback._matchable(text))
