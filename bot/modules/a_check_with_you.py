from ..compose import check_with_you

PRIORITY = -999


def respond(text, memory):
    return check_with_you.answer_for(text, memory)
