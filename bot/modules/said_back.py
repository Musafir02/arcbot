from ..memory import lineback

PRIORITY = 350


def respond(text, memory):
    return lineback.reply_for(text, memory)


