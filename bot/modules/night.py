from ..knowledge import sleep_aids
from ..memory import asleep

PRIORITY = 1100


def respond(text, memory):
    if not isinstance(memory, dict):
        return None
    aid = sleep_aids.answer_for(text, memory)
    if aid:
        return aid
    return asleep.answer_for(text, memory) or None
