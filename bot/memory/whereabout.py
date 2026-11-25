import re

PLACE_LINE = re.compile(
    r"^(?:(?:its|it'?s|it is|were|we'?re|we are|im|i'?m|i am|somewhere|anywhere|out)\s+)?"
    r"(?:right\s+)?(?P<lead>near|round|around|close to|not far from|outside of|outside|by|in)\s+"
    r"(?P<place>[a-z][a-z' .-]{1,28})$", re.I)

QUALIFIED_LINE = re.compile(
    r"^(?:somewhere|anywhere|out somewhere|away somewhere)\s+(?P<place>[a-z][a-z' -]{2,28})$",
    re.I)

NOT_A_PLACE = frozenset("""
january february march april may june july august september october november december
jan feb mar apr jun jul aug sep sept oct nov dec
monday tuesday wednesday thursday friday saturday sunday
morning afternoon evening night nights week weekend month year
day days time times moment minute hour
bed home house garden kitchen oven bath bedroom lounge hall office car van toilet sink
here there it this that
fact general particular short long end total all once first last
future public private secret common advance writing person people
progress practice tears pain shock doubt error trouble
""".split())

ASKS_FOR_A_PLACE = re.compile(
    r"\b(?:where|somewhere|anywhere|place|places|ideas?|recommend|suggest(?:ion)?|"
    r"days? out|day trip|holiday|holidays|weekend away|getaway|trip|travel|visit|stay|"
    r"eat out|restaurant|pub|cafe|coffee shop|walk|see|explore|"
    r"go out|going out|things to do|whats on)\b", re.I)


def the_place(line):
    text = (line or "").strip().strip(" .!,").lower()
    if not text or len(text.split()) > 5:
        return ""
    match = PLACE_LINE.match(text)
    if not match:
        match = QUALIFIED_LINE.match(text)
        if not match:
            return ""
    place = match.group("place").strip(" .")
    if not place:
        return ""
    first = place.split()[0]
    if first in NOT_A_PLACE or place in NOT_A_PLACE:
        return ""
    if first in ("a", "an"):
        return ""
    if place.startswith("the ") and place[4:] in NOT_A_PLACE:
        return ""
    return place


def the_question_with_the_place(text, memory):
    place = the_place(text)
    if not place:
        return ""
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns:
        return ""
    for turn in reversed(turns[-3:]):
        if not isinstance(turn, dict):
            continue
        asked = str(turn.get("user") or "").strip()
        if not asked or not ASKS_FOR_A_PLACE.search(asked):
            continue
        said = set(re.findall(r"[a-z']+", str(turn.get("bot") or "").lower()))
        if place.split()[0] in said:
            return ""
        return asked.rstrip(" ?.") + " " + (text or "").strip().strip(" .!")
    return ""
