from ..compose import a_first_time

PRIORITY = -996


def respond(text, memory):
    return a_first_time.reply_for(text, memory)
