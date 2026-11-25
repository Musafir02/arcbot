import re

from . import topics

OPENERS = re.compile(
    r"^\W*(?:(?:and|but|so|ok|okay|right|alright|well|now)\s+)*"
    r"(?P<opener>back\s+to|back\s+on|returning\s+to|as\s+for|(?:anyway|so)\s+about|about)"
    r"\s+(?P<rest>[^.?!]+.*)$",
    re.I,
)

STORE_FRAME = re.compile(
    r"^(?:and\s+|so\s+)?(?:what|how)\s+about\s+"
    r"(?=(?:back\s+(?:to|on)|returning\s+to|as\s+for|(?:anyway|so)\s+about|about)\b)",
    re.I,
)


POINTER = frozenset("""the a an my our your his her its their this that these those some any""".split())

ASK_OPENS = re.compile(r"^(?:what|which|whose|how\s+much|how\s+many|where|when|who|why|should|"
                       r"can|could|do|does|did|is|are|will|would)\b", re.I)

NOTHING_NAMED = frozenset("""it its that this these those they them there their one ones
he she him her his anything something everything""".split())


def _the_chat_has(words, memory):
    if isinstance(memory, dict):
        for turn in memory.get("turns") or ():
            if not isinstance(turn, dict):
                continue
            said = set(topics.words(turn.get("user") or "")) | set(topics.words(turn.get("bot") or ""))
            if said.intersection(words):
                return True
    return False


def _the_parts(text):
    match = OPENERS.match(STORE_FRAME.sub("", str(text or "")))
    if not match:
        return None
    rest = match.group("rest").strip()
    if not rest:
        return None
    thing, ask = None, ""
    if "," in rest:
        thing, ask = rest.split(",", 1)
    else:
        found = re.search(r"\s+(?=(?:what|which|where|when|who|why|how|should|can|could|do|does|is|"
                          r"are|will|would)\b)", rest, re.I)
        if found:
            thing, ask = rest[:found.start()], rest[found.start():]
    if thing is None:
        return None
    thing = thing.strip(" ,.:;?!")
    ask = ask.strip(" ,.:;?!")
    if not thing or not ask:
        return None
    if match.group("opener").lower().strip() == "about" and "," not in rest:
        return None
    named = [word for word in topics.words(thing) if word not in POINTER]
    if not named or set(named) <= NOTHING_NAMED:
        return None
    return named, ask


def _the_lines(named, ask):
    thing = " ".join(named)
    measure = re.match(r"^(how\s+(?:much|many))\s+(.+)$", ask, re.I)
    if measure:
        return [(measure.group(1) + " " + thing + " " + measure.group(2)).strip()]
    first, space, after = ask.partition(" ")
    if first.lower() in ("what", "which", "whose"):
        return [(first + " " + thing + " " + after).strip(), (ask + " " + thing).strip()]
    if re.match(r"^how\b", ask, re.I):
        return []
    return [(ask + " " + thing).strip()]


def _the_domain_of_the_chat(named, memory):
    if not isinstance(memory, dict):
        return ""
    said = set(named)
    for turn in reversed(list(memory.get("turns") or ())):
        if not isinstance(turn, dict):
            continue
        line = turn.get("user") or ""
        if not said.intersection(topics.words(line)):
            continue
        try:
            item = topics._entry(line)
        except Exception:
            return ""
        return str(getattr(item, "domain", "") or "") if item is not None else ""
    return ""


def a_return_to_the_topic(text, memory):
    parts = _the_parts(text)
    if not parts:
        return ""
    named, ask = parts
    if not _the_chat_has(set(named), memory):
        return ""
    try:
        whole = topics._entry(text)
        without = topics._entry(ask)
    except Exception:
        return ""
    domain = _the_domain_of_the_chat(named, memory)
    for line in _the_lines(named, ask):
        try:
            item = topics._entry(line)
        except Exception:
            continue
        if item is None:
            continue
        if whole is not None and item is whole:
            continue
        if not topics._names_it(line, item) and without is not None and without is item:
            continue
        if domain and str(getattr(item, "domain", "") or "") != domain:
            continue
        return line
    return ""


def the_thing_named(text):
    match = OPENERS.match(str(text or ""))
    if not match:
        return ""
    rest = match.group("rest").strip()
    if "," not in rest:
        return ""
    return rest.split(",", 1)[0].strip(" ,.:;?!")


QUANTITY_ASK = re.compile(r"^\s*(?:how\s+(?:much|many)|what\s+(?:weight|size|length|price|"
                          r"quantity))\b", re.I)
A_NUMBER = re.compile(r"\b(?:\d|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
                      r"half|a couple|a few)\b", re.I)


def _the_sentence_with_the_amount(answer):
    for sentence in re.split(r"(?<=[.!?])\s+", str(answer or "")):
        if sentence.strip() and A_NUMBER.search(sentence):
            return sentence.strip()
    return ""


def as_the_same_answer(reply, text, short=None):
    from . import again as same_again

    thing = the_thing_named(text) or "that"
    ask = (_the_parts(text) or ("", ""))[1]
    if ask and QUANTITY_ASK.match(ask) and not A_NUMBER.search(str(short or "")):
        short = _the_sentence_with_the_amount(reply) or short
    short = same_again._short(short or same_again.unframed(reply) or str(reply or ""))
    named = same_again.the_name_the_answer_says(short, thing, card=reply)
    if not named or named.lower() in short.lower():
        return same_again.AGAIN[0].format(reply=short)
    return same_again.DETAIL_AGAIN[1].format(detail=named, reply=short)


def a_bare_return(text, memory=None):
    match = OPENERS.match(STORE_FRAME.sub("", str(text or "")))
    if not match:
        return False
    rest = match.group("rest").strip()
    if not rest or "," in rest:
        return False
    if re.search(r"\b(?:what|which|where|when|who|why|how|should|can|could|do|does|did|is|are|"
                 r"will|would)\b", rest, re.I):
        return False
    named = [word for word in topics.words(rest) if word not in POINTER]
    if not named or set(named) <= NOTHING_NAMED:
        return False
    return bool(memory is None or _the_chat_has(set(named), memory))
