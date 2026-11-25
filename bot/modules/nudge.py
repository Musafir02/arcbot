from ..compose import still

PRIORITY = -950


def respond(text, memory):
    try:
        return still.reply_for(text, memory)
    except Exception:
        return None


def takes_as_it_comes(text, memory):
    try:
        return bool(still.takes_as_it_comes(text, memory))
    except Exception:
        return False


TAKES_AS_IT_COMES = takes_as_it_comes
