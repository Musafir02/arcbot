from ..memory import groupages

PRIORITY = 7050

ANSWERS = ("family-and-parenting",)


def observe(text, memory):
    try:
        groupages.watch(text, memory)
    except Exception:
        return


def respond(text, memory):
    if not isinstance(memory, dict):
        return None
    try:
        return groupages.reply_for(text, memory) or None
    except Exception:
        return None


def TAKES_AS_IT_COMES(text, memory):
    if not isinstance(memory, dict):
        return False
    try:
        return groupages.asks_for_the_list(text, memory)
    except Exception:
        return False
