import copy
import re

from ..memory import last_bot, last_user

ASK_IF_A_THING_IS_SAFE = re.compile(
    r"\bis\s+(?:it|that|this|they)\s+(?:safe|dangerous|a\s+(?:fire\s+)?(?:risk|hazard))\b"
    r"|\bis\s+it\s+(?:safe|alright|ok|okay)\s+to\s+(?:use|keep|leave|run|plug|carry\s+on)\b"
    r"|\bis\s+(?:the|my|our)\s+[a-z']{3,20}\s+(?:safe|dangerous|a\s+(?:fire\s+)?(?:risk|hazard))\b"
    r"|\bcan\s+i\s+(?:still\s+)?(?:use|keep|leave|run|plug)\s+(?:it|this|that)\b"
    r"|\bcan\s+(?:it|that|this)\s+be\s+(?:used|left|kept)\b", re.I)

A_THING_THAT_PLUGS_IN = frozenset("""
    boiler heater charger plug socket cable lead extension kettle toaster oven hob grill
    microwave fridge freezer washing machine washer tumble dryer dishwasher immersion shower
    radiator thermostat lamp light lights fan dehumidifier laptop phone mobile tablet
    hairdryer straighteners iron blanket fire chimney gas electrics wiring fuse
    """.split())

A_SAFETY_WORD = re.compile(
    r"\b(?:safe|safely|unsafe|dangerous|danger|risk|risky|hazard|hazardous|fire|"
    r"electrocut\w*|shock|shocks|shocking)\b")

A_FAULT_DESCRIBED = re.compile(
    r"\b(?:cracked|cracking|frayed|fraying|exposed|bare|sparks?|sparking|smoking|smokes|"
    r"smelt|smells?|burning|burnt|scorched|melting|melted|toasted|hot|overheat\w*|"
    r"buzzing|buzzes|fizzing|tripping|trips|dripping|drips|leaking|leaks|leak|wet|damp|"
    r"loose|live|popped|banging|loud\s+bang)\b")

A_SAFETY_TEST_LINES = (
    "The test with {thing} is a burning smell, sparks, or heat you would not leave the room "
    "with: any of those and switch it off at the wall and leave it until somebody has looked at "
    "it. None of them and it will keep until the morning.",
    "Three things make {thing} a no for tonight - a burning smell, sparks, or a plug or socket "
    "that is hot to the touch. Any of those, off at the wall and not again until it has been "
    "looked at. If it is only a noise or a drip, it can wait for the morning.",
    "Nothing about {thing} needs deciding tonight unless it smells of burning, or water is "
    "anywhere near the electrics: then switch it off at the wall and have it looked at. "
    "Otherwise leave it be and ring somebody in the morning.",
    "Keep it plain with {thing}: if it smells of burning or the socket is hot, off at the wall "
    "and no more of it tonight. A drip or a rattle can wait for the morning - bowl under it, "
    "nothing electrical near it.",
)

A_RULING_ALREADY = ("off at the wall", "unplug", "don't use it", "do not use it",
                    "stop using it", "turn it off", "switch it off", "ring 999", "call 999",
                    "get out")
A_SAFETY_ALREADY_RULED = (
    "No - the answer above still stands: it stays off until somebody has looked at it.",
    "Same answer as before: not used again until it has been checked.",
    "That has not changed: off, and looked at before it goes back on.",
)


def reply_for(clean, memory):
    text = " ".join(str(clean or "").lower().split())
    if not text or not ASK_IF_A_THING_IS_SAFE.search(text):
        return None
    thing = _the_thing_on_the_table(text, memory)
    if not thing:
        return None
    if not (_a_safety_word(text) or _the_thing_is_described_faulty(memory, thing)):
        return None
    card = _the_answers_have_this(text, memory)
    if card and (thing in card.lower() or not _a_shrug(card)):
        return None
    if the_bot_already_ruled(memory):
        return A_SAFETY_ALREADY_RULED
    return tuple(line.format(thing="the " + thing) for line in A_SAFETY_TEST_LINES)


def _a_safety_word(clean):
    return bool(A_SAFETY_WORD.search(str(clean or "").lower()))


def _the_thing_is_described_faulty(memory, thing):
    said = " ".join(str(last_user(memory) or "").lower().split())
    if not said or not thing or thing not in said:
        return False
    return bool(A_FAULT_DESCRIBED.search(said))


def _a_shrug(reply):
    said = str(reply or "").lower()
    return any(phrase in said for phrase in (
        "i don't know enough", "i do not know enough", "beyond what i know", "rather not guess",
        "not sure about that one", "i'm not sure about that", "search should sort", "quick search",
        "search online", "better sources", "can't call that one", "cant call that one"))


def _the_thing_on_the_table(clean, memory):
    for text in (clean, last_user(memory)):
        found = [word for word in re.findall(r"[a-z']{3,20}", str(text or "").lower())
                 if word in A_THING_THAT_PLUGS_IN]
        if found:
            return found[-1]
    return ""


A_DANGER_SAID = re.compile(
    r"\b(?:fires?|flames?|smoke|shocks?|shocking|electrocut\w*|burns?|burnt|scorch\w*|"
    r"unsafe|kills?|fatal|explodes?|explosion|catch(?:es)? fire)\b")


def the_bot_already_ruled(memory):
    said = str(last_bot(memory) or "").lower()
    if not any(phrase in said for phrase in A_RULING_ALREADY):
        return False
    return bool(A_DANGER_SAID.search(said))


def _the_answers_have_this(clean, memory):
    try:
        from ..modules import answers

        said = answers.respond(clean, copy.deepcopy(memory if isinstance(memory, dict) else {}))
    except Exception:
        return None
    return said if isinstance(said, str) and said.strip() else None
