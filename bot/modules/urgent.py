from ..compose import urgent

PRIORITY = -900

ANSWERS = ()

ANSWERS_INSTEAD = ("health",)


def respond(text, memory):
    return urgent.reply_for(text, memory)
