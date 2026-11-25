from ..memory import when

PRIORITY = 7500


def TAKES_AS_IT_COMES(text, memory):
    if not isinstance(memory, dict):
        return False
    return bool(when.how_long_answer(text, memory))


def respond(text, memory):
    if not isinstance(memory, dict):
        return None
    answer = when.how_long_answer(text, memory)
    return answer or None
