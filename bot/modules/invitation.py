from ..compose import invitation

PRIORITY = -500
ANSWERS_INSTEAD = ("small-talk",)


def DEFERS_TO(reply, text):
    return True


def respond(text, memory):
    if not isinstance(memory, dict):
        memory = {}
    return invitation.reply_for(text, memory)
