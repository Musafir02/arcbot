from ..memory import outgoings

PRIORITY = 8000


def TAKES_AS_IT_COMES(text, memory):
    if not isinstance(memory, dict):
        return False
    return bool(outgoings.reply_for(text, memory))


def respond(text, memory):
    if not isinstance(memory, dict):
        return None
    return outgoings.reply_for(text, memory) or None
