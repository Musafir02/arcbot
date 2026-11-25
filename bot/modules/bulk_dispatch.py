from ..bulk.match import match

PRIORITY = -999.9


def respond(text, memory):
    return match(text)
