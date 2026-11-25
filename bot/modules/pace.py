from ..compose import pace

PRIORITY = 1300


def respond(text, memory):
    try:
        return pace.reply_for(text, memory)
    except Exception:
        return None


def takes_as_it_comes(text, memory):
    try:
        return pace.the_pace_line(text, memory) or pace.the_keep_up_line(text, memory)
    except Exception:
        return False


TAKES_AS_IT_COMES = takes_as_it_comes
