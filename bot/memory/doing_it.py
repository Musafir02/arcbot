import re

from . import topics

LENGTH_ASK = re.compile(r"\bhow (?:long|many (?:hours|minutes|days|weeks|months|years))\b", re.I)

ASK_WORDS = frozenset("""
how long many much hours hour days day weeks week months month years year minutes minute should
shall can could would will do does did is are was i me my we you it that this to for the a an in
on at about each per every and or of time
""".split())

TIME_WORDS = frozenset("""
day days week weeks month months year years weekend summer winter spring autumn today tomorrow
yesterday morning evening night ago last next this recent lately start started
""".split())

NOT_A_THING_DONE = frozenset("heal recover bleed".split())

LOOKBACK = 12


def _is_doing(word):
    if word in NOT_A_THING_DONE or topics.stem(word) in NOT_A_THING_DONE:
        return False
    if word in topics.ACTION:
        return True
    for doing in topics.ACTION:
        if len(doing) < 4 or len(word) <= len(doing):
            continue
        if word.startswith(doing):
            return True
        if doing.endswith("e") and word.startswith(doing[:-1]):
            return True
    return False


def doing_word(text):
    for word in topics.words(text):
        if _is_doing(word):
            return word
    return None


def asks_about_doing(text):
    line = str(text or "")
    if not LENGTH_ASK.search(line):
        return False
    return doing_word(line) is not None


def _the_things(memory):
    out = []
    for record in reversed((memory.get("topics") or [])[-LOOKBACK:]):
        text = record.get("text") if isinstance(record, dict) else None
        if not isinstance(text, str) or not text.strip():
            continue
        if doing_word(text) is None:
            continue
        for word in topics.keywords(text):
            if len(word) < 4 or word in TIME_WORDS or _is_doing(word):
                continue
            if word not in out:
                out.append(word)
    return out


def written_out(text, memory):
    said = " ".join(str(text or "").split()).rstrip("?.! ")
    if not asks_about_doing(said):
        return ()
    if any(word not in ASK_WORDS and not _is_doing(word) for word in said.lower().split()):
        return ()
    if not isinstance(memory, dict):
        return ()
    out = []
    for thing in _the_things(memory):
        out.append(said + " " + thing + "?")
        out.append(said + " " + thing + " each day?")
    return tuple(out)


A_MOAN = re.compile(
    r"\bi (?:can\s+)?(?:never|always|keep|constantly|usually|often|still)\b"
    r"(?:\s+(?P<verb>getting|get|doing|do|making|make|cooking|cook|picking|pick|"
    r"finding|find|managing|manage))?\b"
    r"(?P<thing>[^?.!,]{1,40}?)"
    r"\s+(?:wrong|right|messed up|ruined|spoiled|spoilt|screwed up|backwards)\b", re.I)

MOAN_VERB = {"getting": "get", "doing": "do", "making": "make", "cooking": "cook",
             "picking": "pick", "finding": "find", "managing": "manage"}


def the_ask_behind_a_moan(text):
    said = " ".join(str(text or "").split())
    if not said or len(said.split()) > 12:
        return ""
    match = A_MOAN.search(said)
    if not match:
        return ""
    thing = match.group("thing").strip(" ,")
    if not thing.split() or len(thing.split()) > 4:
        return ""
    if not topics.keywords(thing):
        return ""
    verb = (match.group("verb") or "get").lower()
    return "how do i " + MOAN_VERB.get(verb, verb) + " " + thing + " right?"
