from ..memory import workplace

PRIORITY = 1150


def TAKES_AS_IT_COMES(text, memory):
    return bool(workplace.the_place_the_person_works(text, memory))


def respond(text, memory):
    if not isinstance(memory, dict):
        return None
    return workplace.the_place_the_person_works(text, memory)
