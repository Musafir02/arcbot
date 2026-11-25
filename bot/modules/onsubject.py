from ..compose import fallback
from ..compose import onsubject

PRIORITY = -998


def respond(text, memory):
    reading = onsubject.pool(text, memory=memory)
    if not reading:
        reading = onsubject.place_pool(text, memory=memory)
    if not reading:
        return None
    try:
        reply = fallback.reply_for(text, memory)
    except Exception:
        return None
    if not isinstance(reply, str) or not fallback._in_a_pool(reply, (fallback.UNKNOWN,)):
        return None
    return reading
