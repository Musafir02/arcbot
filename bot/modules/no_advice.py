from ..compose import no_advice

PRIORITY = 1050


def respond(text, memory):
    try:
        pool = no_advice.pool_name(text)
    except Exception:
        return None
    if not pool:
        return None
    if not TAKES_AS_IT_COMES(text, memory):
        return None
    try:
        return no_advice.reply_for(pool, text, memory)
    except Exception:
        return None


def TAKES_AS_IT_COMES(text, memory=None):
    try:
        if not no_advice.says_no_advice(text):
            return False
        return not no_advice.says_a_death(text)
    except Exception:
        return False
