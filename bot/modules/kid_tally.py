from ..memory import kidcount

PRIORITY = 7050

ANSWERS = ("family-and-parenting",)


def respond(text, memory):
    try:
        return kidcount.reply_for(text, memory) or None
    except Exception:
        return None
