from ..compose import their_detail

PRIORITY = -997


def respond(text, memory):
    return their_detail.reply_for(text, memory)
