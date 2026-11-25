from ..memory import taking

PRIORITY = 1000


def respond(text, memory):
    return taking.reply_for(text, memory) or None


def takes_as_it_comes(text, memory):
    try:
        return bool(taking.the_ask_and_the_subject(text, memory))
    except Exception:
        return False


TAKES_AS_IT_COMES = takes_as_it_comes
