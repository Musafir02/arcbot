from ..compose import ruledout

PRIORITY = -450


def respond(text, memory):
    try:
        return ruledout.reply_for(text, memory) or None
    except Exception:
        return None


def takes_as_it_comes(text, memory):
    try:
        return bool(ruledout.takes_as_it_comes(text, memory))
    except Exception:
        return False


TAKES_AS_IT_COMES = takes_as_it_comes
