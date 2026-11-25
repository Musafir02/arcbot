from ..compose import fallback, theirperson

PRIORITY = 250


def respond(text, memory):
    reply = theirperson.reply_for(text, memory)
    if not reply:
        return None
    if not theirperson.may_replace(fallback.reply_for(text, memory), text):
        return None
    return reply
