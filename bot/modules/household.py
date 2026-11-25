from ..memory import household

PRIORITY = 7050


def observe(text, memory):
    try:
        household.observe(text, memory)
    except Exception:
        return


def respond(text, memory):
    try:
        return household.answer(text, memory) or None
    except Exception:
        return None


def takes_as_it_comes(text, memory):
    try:
        return bool(household.takes_as_it_comes(text, memory))
    except Exception:
        return False


TAKES_AS_IT_COMES = takes_as_it_comes
