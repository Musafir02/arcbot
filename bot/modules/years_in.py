from ..memory import years_in

PRIORITY = 1150


def respond(text, memory):
    if not isinstance(memory, dict):
        return None
    return (years_in.the_years_in_the_doing(text, memory)
            or years_in.the_years_in_their_doing(text, memory) or None)


def takes_as_it_comes(text, memory):
    if not isinstance(memory, dict):
        return False
    return bool(years_in.the_years_in_the_doing(text, memory)
                or years_in.the_years_in_their_doing(text, memory))


TAKES_AS_IT_COMES = takes_as_it_comes
