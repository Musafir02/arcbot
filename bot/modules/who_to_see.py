from ..compose import who

PRIORITY = 1500


def respond(text, memory):
    try:
        return who.reply_for(text, memory) or None
    except Exception:
        return None


def takes_as_it_comes(text, memory):
    try:
        return bool(who.takes_as_it_comes(text, memory))
    except Exception:
        return False


TAKES_AS_IT_COMES = takes_as_it_comes
