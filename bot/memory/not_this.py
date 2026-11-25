import re

from ..compose import pick
from ..knowledge import travel
from . import facts
from . import user

_AFTER_THE_NAME = r"(?:\s*,?\s*(?:then|though|after all|actually|really))?"

NOT_A_PLACE = (
    re.compile(r"^(?:and\s+|but\s+|so\s+|ok\s+|okay\s+)?(?:no,?\s+|nope,?\s+|nah,?\s+)?"
               r"(?:definitely\s+|absolutely\s+|really\s+|probably\s+|actually\s+)?not\s+"
               r"(?:to\s+)?(?P<place>[a-z][a-z' -]{1,24}?)" + _AFTER_THE_NAME + r"$"),
    re.compile(r"^(?:and\s+|but\s+|so\s+|ok\s+|okay\s+)?(?:no|nope|nah),?\s+"
               r"(?:definitely\s+|absolutely\s+|really\s+|probably\s+|actually\s+)?"
               r"(?P<place>[a-z][a-z' -]{1,24}?)" + _AFTER_THE_NAME + r"$"),
    re.compile(r"^(?:and\s+|but\s+)?i\s+(?:said|meant|told you)\s+not\s+"
               r"(?P<place>[a-z][a-z' -]{1,24}?)" + _AFTER_THE_NAME + r"$"),
    re.compile(r"^(?:and\s+|but\s+)?(?:we|i|they|he|she)\s+"
               r"(?:am|are|is|was|were|will|would|re|m|s)?\s*not\s+"
               r"(?:going|heading|off|flying|driving)\s+(?:to|into)\s+"
               r"(?P<place>[a-z][a-z' -]{0,24}?)\s*"
               r"(?:anymore|any\s+more|now|then|after\s+all|this\s+time)?$"),
    re.compile(r"^(?:and\s+|but\s+)?(?:we|i)\s+(?:dont|don't|do not)\s+(?:want|fancy)\s+"
               r"(?:to go to\s+)?(?P<place>[a-z][a-z' -]{1,24}?)" + _AFTER_THE_NAME + r"$"),
)

_BE_WILL = "are|is|were|was|do|does|did|could|would|should|will|can|must"
_CONTRACTIONS = (
    (re.compile(r"\b(we|i|they|he|she|it|you)(?:'re|re)\b"), r"\1 are"),
    (re.compile(r"\b(i)(?:'m|m)\b"), r"\1 am"),
    (re.compile(r"\b(we|i|they|he|she|it)(?:'s|s)\b"), r"\1 is"),
    (re.compile(r"\b(" + _BE_WILL + r")n'?t\b"), r"\1 not"),
    (re.compile(r"\baint\b"), "is not"),
    (re.compile(r"\bim\b"), "i am"),
)

STANDS = (
    "{place}, then - no {gone}.",
    "Right - {place}, not {gone}.",
    "So {place} it is, without {gone}.",
    "{place} on its own, then.",
)
OUT = (
    "No {gone}, then. Where are you thinking instead?",
    "Fair enough - not {gone}. What are you after instead?",
    "{gone} is out, then. Where else are you looking?",
)
OUT_AFTER_A_QUESTION = (
    "No {gone}, then - say where instead and I will go with that.",
    "Fair enough - not {gone}. Tell me where you are looking and I will help from there.",
    "{gone} is out, then. Point me at somewhere else when you know it.",
)


def _the_place_the_chat_is_on(memory, gone):
    held = []
    for place in reversed(user(memory).get("places") or ()):
        if isinstance(place, str) and place.strip():
            held.append(place.strip())
    plan = user(memory).get("plan")
    if isinstance(plan, str) and plan.strip():
        held.append(plan.strip())
    for place in held:
        if place.lower() == gone.lower():
            continue
        named = _the_name_in(place, gone)
        if named:
            return named
    return ""


def _the_name_in(said, gone):
    whole = _a_place_the_chat_knows(said)
    if whole and whole.lower() != gone.lower():
        return whole
    found = ""
    for word in re.findall(r"[a-z][a-z']*", said.lower()):
        if word == gone.lower():
            continue
        named = _a_place_the_chat_knows(word)
        if named:
            found = named
    return found


def _a_place_in_play(memory, place):
    if not isinstance(memory, dict):
        return False
    held = user(memory)
    if held.get("places") or held.get("plan") or held.get("city"):
        return True
    turns = memory.get("turns")
    if not isinstance(turns, list):
        return False
    for turn in turns[-6:]:
        if not isinstance(turn, dict):
            continue
        for said in (turn.get("user"), turn.get("bot")):
            if not isinstance(said, str):
                continue
            for word in re.findall(r"[a-z][a-z']*", said.lower()):
                if word != place.lower() and _a_place_the_chat_knows(word):
                    return True
    return False


def _asked_last(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns:
        return False
    last = turns[-1]
    said = last.get("bot") if isinstance(last, dict) else None
    return isinstance(said, str) and said.strip().endswith("?")


def _a_place_the_chat_knows(place):
    word = str(place or "").strip().lower()
    if not word:
        return ""
    if word in travel.CITIES or word in travel.CITY_COUNTRY:
        return facts.place_value(word) or word.capitalize()
    if word in set(travel.CITY_COUNTRY.values()) or word in travel.CAPITALS:
        return word.capitalize()
    return ""


def _in_plain_words(text):
    line = str(text or "").strip().lower().replace("\u2019", "'")
    for shape, long_form in _CONTRACTIONS:
        line = shape.sub(long_form, line)
    return " ".join(line.split()).rstrip(".!,")


def the_place_ruled_out(text, memory):
    if not isinstance(text, str):
        return ""
    line = _in_plain_words(text)
    line = line.rstrip(".!,")
    for shape in NOT_A_PLACE:
        found = shape.match(line)
        if not found:
            continue
        place = _a_place_the_chat_knows(found.group("place"))
        if place:
            return place
    return ""


def _the_place_ruled_out(text, memory):
    gone = the_place_ruled_out(text, memory)
    if not gone or not isinstance(memory, dict):
        return None
    stands = _the_place_the_chat_is_on(memory, gone)
    if not stands and not _a_place_in_play(memory, gone):
        return None
    if stands:
        pool = STANDS
    elif _asked_last(memory):
        pool = OUT_AFTER_A_QUESTION
    else:
        pool = OUT
    lines = [shape.format(place=stands, gone=gone) for shape in pool]
    turns = memory.get("turns") if isinstance(memory.get("turns"), list) else []
    said_lately = {turn.get("bot") for turn in turns[-4:]
                   if isinstance(turn, dict) and isinstance(turn.get("bot"), str)}
    fresh = [line for line in lines if line not in said_lately] or lines
    return pick(fresh, memory, str(text or ""))


def reply_for(text, memory):
    ruled_out = _the_place_ruled_out(text, memory)
    if ruled_out:
        return ruled_out
    from . import tried

    return tried.reply_for(text, memory)
