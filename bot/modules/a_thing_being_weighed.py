from ..compose import a_thing_being_weighed
from . import greeting

PRIORITY = -999


def respond(text, memory):
    if not a_thing_being_weighed.pool(text):
        return None
    try:
        reply = greeting.respond(text, memory)
    except Exception:
        return None
    if not isinstance(reply, str) or not reply.strip():
        return None
    return a_thing_being_weighed.answer_for(text, memory, reply)
