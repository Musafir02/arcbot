from ..memory import will_it_work

PRIORITY = 1000


def respond(text, memory):
    try:
        return will_it_work.reply_for(text, memory)
    except Exception:
        return None


def takes_as_it_comes(text, memory):
    try:
        return bool(will_it_work.reply_for(text, memory))
    except Exception:
        return False


TAKES_AS_IT_COMES = takes_as_it_comes
