from ..memory import aboutthem

PRIORITY = 7150


def TAKES_AS_IT_COMES(text, memory):
    return bool(aboutthem.an_age_ahead(text, memory))


def CLAIMS_INSTEAD(text, memory):
    return bool(aboutthem.an_age_ahead(text, memory))


def respond(text, memory):
    if not isinstance(memory, dict):
        return None
    return aboutthem.an_age_ahead(text, memory) or None
