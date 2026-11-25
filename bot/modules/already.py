from ..memory import already

PRIORITY = 400


def respond(text, memory):
    return already.reply_for(text, memory)


TAKES_AS_IT_COMES = already.takes_as_it_comes
