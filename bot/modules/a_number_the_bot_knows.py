from ..compose import a_number_the_bot_knows as numbers

PRIORITY = -999


def respond(text, memory=None):
    return numbers.answer_for(text, memory)
