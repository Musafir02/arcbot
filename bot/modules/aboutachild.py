import copy

from ..memory import aboutthem
from ..understanding import understand
from . import answers

PRIORITY = 1100


def TAKES_AS_IT_COMES(text, memory):
    return bool(aboutthem.with_the_age(text, memory))


def respond(text, memory):
    if not isinstance(memory, dict):
        return None
    written = aboutthem.with_the_age(text, memory)
    if not written:
        return None
    seen = copy.deepcopy(memory)
    seen["understood"] = understand(written, seen)
    reply = answers._answer(written, seen)
    if not reply:
        return None
    return str(reply).strip() or None
