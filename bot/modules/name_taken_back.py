
from ..compose import pick
from ..memory import facts as extract
from ..memory import user

PRIORITY = 6600

NAME_TAKEN_BACK_SAY = (
    "Sorry — I had you as {name}. What should I call you?",
    "My mistake on {name}. What should I call you?",
    "Sorry about that — {name} was wrong. What do you go by?",
    "Ah, sorry. Not {name}, then — what should I call you?",
)
NAME_TAKEN_BACK_BARE = (
    "Sorry about that — what should I call you?",
    "My mistake. What should I call you?",
    "Sorry — what do you go by?",
)


def _the_name_i_had(memory):
    if not isinstance(memory, dict):
        return ""
    return str(user(memory).get("name") or "").strip()


def _note(text):
    return " ".join(str(text or "").lower().split())


def observe(text, memory):
    if not isinstance(memory, dict):
        return
    known = _the_name_i_had(memory)
    taken = extract.the_name_they_take_back(text, known)
    if taken is None:
        return
    user(memory).pop("name", None)
    memory["name_taken_back"] = {"name": str(taken), "said": _note(text)}
    memory["asked_for"] = "name"


def _this_line(memory, text):
    if not isinstance(memory, dict):
        return None
    held = memory.get("name_taken_back")
    if not isinstance(held, dict) or held.get("said") != _note(text):
        return None
    return held


def respond(text, memory):
    held = _this_line(memory, text)
    if held is None:
        return None
    name = str(held.get("name") or "").strip()
    if not name:
        return pick(NAME_TAKEN_BACK_BARE, memory)
    return pick([line.format(name=name) for line in NAME_TAKEN_BACK_SAY], memory)


def takes_as_it_comes(text, memory):
    return _this_line(memory, text) is not None


TAKES_AS_IT_COMES = takes_as_it_comes
