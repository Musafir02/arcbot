from ..compose import the_trouble_named as pool

PRIORITY = -997


def respond(text, memory):
    return pool.reply_for(text, memory)


def TAKES_AS_IT_COMES(text, memory=None):
    return respond(text, memory) is not None
