from ..compose import ward

PRIORITY = -985

def respond(text, memory):
    return ward.answer_for(text, memory)
