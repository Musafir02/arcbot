from ..compose import what_decides_it

PRIORITY = -998


def respond(text, memory):
    try:
        return what_decides_it.answer_for(text, memory)
    except Exception:
        return None
