import re

from . import kinds

_KIND_WORDS = ("size", "time", "date", "day", "price", "cost", "number",
                "weight", "height", "dose")
_A_KIND = {
    "size": re.compile(r"\b(?:in\s+(?:a|an)|size)\s+"
                       r"(xs|s|m|l|xl|xxl|small|medium|large|extra large)\b"
                       r"|\b(?:was|is|its|it's|make\s+it|actually|instead)\s+(?:a\s+)?"
                       r"(xs|xl|xxl|small|medium|large|extra\s+large)\b", re.I),
    "time": re.compile(r"\b(?:at|from)\s+(\d{1,2}(?:[:.]\d{2})?\s?(?:am|pm)?|half\s+\w+"
                       r"|midday|noon|midnight)\b"
                       r"|\b(\d{1,2}(?:[:.]\d{2})?\s?(?:am|pm))\b"
                       r"|\b(half\s+(?:past\s+)?(?:one|two|three|four|five|six|seven|eight"
                       r"|nine|ten|eleven|twelve))\b"
                       r"|\b(midday|noon|midnight)\b", re.I),
    "day": re.compile(r"\b(?:%s)\b" % "|".join(
        ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
         "tomorrow", "tonight")), re.I),
    "date": re.compile(r"\b(?:the\s+)?((?:0?[1-9]|[12][0-9]|3[01])(?:st|nd|rd|th))\b"
                       r"|\b(?:in|on)\s+(january|february|march|april|may|june|july|august"
                       r"|september|october|november|december)\b", re.I),
    "price": re.compile(r"(?:£|\$|€)\s?\d[\d,]*(?:\.\d+)?"
                        r"|\b\d[\d,]*(?:\.\d+)?\s?(?:quid|pounds|euros|dollars|grand)\b"
                        r"|\b(?:quoted|paid|charged|cost)\s+(?:me\s+)?(?:£|\$|€)?\s?\d[\d,]*", re.I),
    "weight": re.compile(r"\b\d+(?:\.\d+)?\s?(?:kg|kilos?|stone|st|lbs?|pounds?)\b", re.I),
    "height": re.compile(r"\b\d+(?:\.\d+)?\s?(?:cm|ft|feet|foot|inches|in)\b", re.I),
    "dose": re.compile(r"\b\d+(?:\.\d+)?\s?(?:mg|ml|mcg|micrograms?|g)\b", re.I),
}
_A_KIND_FOR_WORD = {
    "size": "size", "time": "time", "date": "date", "day": "day", "birthday": "date",
    "price": "price", "cost": "price", "number": "price", "weight": "weight",
    "paid": "price", "pay": "price", "spend": "price", "spent": "price",
    "height": "height", "dose": "dose",
}

ASKS_BACK = re.compile(
    r"\b(?:what|which|who|when|where|how\s+\w+)\b[^?!]{0,40}?"
    r"\bdid\s+i\s+(?:say|said|tell\s+you|told\s+you|mention|mentioned)\b"
    r"|\b(?:what|which)\s+(?:[a-z']+\s+){1,3}?(?:was|is|were)\s+it\b"
    r"|\bwhat(?:'s|\s+is|\s+was)\s+my\s+(?:[a-z']+\s+){1,3}?again\b"
    r"|\bremind\s+me\s+(?:what|which|when|where|who|how\s+many|how\s+much)\b"
    r"|\bwhat\s+did\s+i\s+say\b"
    r"|\bwhat\s+(?:was|were|am|is)\s+(?:i|we)\s+going\s+to\s+\w+"
    r"|\bwhat\s+(?:was|is)\s+it\s+(?:he|she|they|we|i|you)\b"
    r"|\bhow\s+(?:much|many)\b[^?!]{0,25}?\bdid\s+i\s+(?:say|said|need|want|ask)\b", re.I)

_AN_ATTRIBUTE = re.compile(
    r"\b(?:age|ages|old|size|name|price|cost|weight|height|colour|color|birthday|date|time|"
    r"number|address|surname|title)\b", re.I)

_THE_ASK = frozenset("""
what which who whom whose when where why how remind me again say said saying says tell told
telling mention mentioned i you my our we us it its that this these those was were is are be
been being did do does done about of to the a an and or for with in on at by as if so but not
any some please just really thing things one ones kind sort name called exact exactly already
""".split())

_VAGUE = frozenset("""
go going went get got getting do doing done make making take taking put thing things way bit
lot time now then well good bad sure really quite maybe first last next other another same
back again more most much many little big small old new long short like want wanted need
""".split())

_NOT_A_DETAIL = re.compile(
    r"\bhow\s+(?:old|many|much|long|often|far|heavy|tall)\b"
    r"|\bwhat\s+time\b|\bwhat\s+(?:day|date)\b|\bwhen\b", re.I)

_SHORT_WORD = 3

_QUESTION = re.compile(r"^\s*(?:what|which|who|when|where|why|how|should|shall|can|could|would"
                       r"|will|do|does|did|is|are|am|have|has|if|any)\b|\?\s*$", re.I)
_INTENTION = re.compile(r"\b(?:was|were|am|is|going)\s+(?:i\s+)?(?:going\s+)?to\s+"
                        r"(?:ask|say|do|tell|mention)\b|\bwhat\s+(?:i\s+)?was\s+going\s+to\b",
                        re.I)


def flat(text):
    return " ".join(str(text or "").split())


def _words(text):
    return [word.strip("'") for word in re.findall(r"[a-z']+", flat(text).lower())]


def _stem(word):
    for suffix in ("ing", "ies", "es", "ed", "s"):
        if len(word) > len(suffix) + _SHORT_WORD and word.endswith(suffix):
            return word[: -len(suffix)]
    return word


def about(text):
    return {_stem(word) for word in _words(text)
            if word not in _THE_ASK and word not in _VAGUE}


ASKS_BACK_A_KIND = re.compile(
    r"\b(?:what|which)\s+(?:%(kind)s)\b[^?!]{0,22}?\bagain\b"
    r"|\bthe\s+(?:%(kind)s)\s+(?:(?:that\s+)?(?:i|we)\s+(?:said|gave|told\s+you|mentioned)"
    r"|again)\b"
    r"|\b(?:did|have)\s+(?:i|we)\b[^?!]{0,30}?\b(?:%(kind)s)\b"
    r"|\bhow\s+(?:much|many)\b[^?!]{0,25}?\bagain\b" % {"kind": "|".join(sorted(_A_KIND_FOR_WORD))},
    re.I)


_A_TELLING = re.compile(r"^\s*(?:was|is|were|are|should\s+be|came\s+in|goes|needs|will\s+be)\b",
                        re.I)

_A_PAST_ACT = re.compile(r"\b(?:did|have)\s+(?:i|we)\b", re.I)


def _a_kind_named(text):
    for word in _words(text):
        if word in _A_KIND_FOR_WORD:
            return word
    return None


def is_a_recall_ask(text):
    flat_text = flat(text)
    if ASKS_BACK.search(flat_text):
        return True
    named = ASKS_BACK_A_KIND.search(flat_text)
    if named and not _A_TELLING.match(flat_text[named.end():]):
        return True
    if not _A_PAST_ACT.search(flat_text):
        return False
    return bool(_a_kind_named(flat_text) or re.search(r"\bhow\s+much\b", flat_text))


def _the_last_reply(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    for turn in reversed(turns if isinstance(turns, list) else ()):
        if isinstance(turn, dict) and flat(turn.get("bot")):
            return flat(turn.get("bot"))
    return ""


def the_lines(memory):
    said = []
    turns = memory.get("turns") if isinstance(memory, dict) else None
    for turn in turns if isinstance(turns, list) else ():
        if not isinstance(turn, dict):
            continue
        line = flat(turn.get("user"))
        if line:
            said.append(line)
    return said


def _the_best_line(wanted, lines, questions=False):
    best = None
    for place, line in enumerate(lines):
        if is_a_recall_ask(line):
            continue
        if _QUESTION.search(line) and not questions:
            continue
        shared = wanted & about_any(line)
        if not shared:
            continue
        longest = max(len(word) for word in shared)
        if longest < _SHORT_WORD:
            continue
        score = (len(shared), longest, place)
        if best is None or score > best[0]:
            best = (score, line)
    return best[1] if best else None


def about_any(text):
    return {_stem(word) for word in _words(text)
            if word not in _THE_ASK and len(word) >= _SHORT_WORD}


_A_MY_VALUE = re.compile(r"\bmy\s+(?:[a-z']+\s+){0,3}?(?:is|was)\s+(?P<value>[^.;,?]+?)\s*$",
                         re.I)
_A_VALUE_START = re.compile(r"^(?:[0-9]|a\b|an\b|the\b|on\b|in\b|at\b|for\b|about\b)", re.I)

_A_VALUE_VERB = re.compile(r"^(?:quoted|paid|charged|cost|costs|size|in\s+(?:a|an)|at|from)\s+",
                           re.I)


_A_THE_CALENDAR = re.compile(r"^\W*(?:what|which)\s+(?:day|date|time)\s+is\s+it\s*\??$", re.I)
_A_SAID_AGAIN = re.compile(r"\b(?:again|before|earlier|did\s+(?:i|we)|have\s+i|you\s+know|"
                           r"tell\s+me|remind)", re.I)


def _the_kind_asked(said):
    if _A_THE_CALENDAR.search(said) and not _A_SAID_AGAIN.search(said):
        return None
    words = {word for word in _words(said) if word in _A_KIND_FOR_WORD}
    if not words:
        if not re.search(r"\bhow\s+much\b", said) or about(said):
            return None
        return "price"
    if about(said) - {_stem(word) for word in words}:
        return None
    return _A_KIND_FOR_WORD[sorted(words)[0]]


def _a_value_of_the_kind(kind, lines):
    pattern = _A_KIND.get(kind)
    if not pattern:
        return None
    for line in reversed(lines):
        match = pattern.search(flat(line))
        if not match:
            continue
        groups = [group for group in match.groups() if group]
        value = (groups[0] if groups else match.group(0)).strip(" .,;")
        value = _A_VALUE_VERB.sub("", value).strip(" .,;")
        if re.search(r"[a-z0-9]", value) and len(value.split()) <= 4:
            return value
    return None


def _the_value(line):
    match = _A_MY_VALUE.search(flat(line))
    if not match:
        return None
    value = match.group("value").strip()
    if not re.search(r"[a-z0-9]", value) or len(value.split()) > 6:
        return None
    return value if _A_VALUE_START.match(value) else None


def _carried(line, wanted):
    if len(line) <= 120:
        return line
    parts = re.split(r"(?<=[.!?;])\s+|,\s+(?=and\b|but\b)", line)
    holding = [part for part in parts if wanted & about_any(part)]
    return holding[0].strip(" ,.;") if holding else line


def _the_value_of_the_kind(said, lines, memory):
    kind = _the_kind_asked(said)
    if not kind:
        return None
    value = _a_value_of_the_kind(kind, lines)
    return "You said " + value + "." if value else None


_A_FIGURE = re.compile(
    r"[\u00a3$\u20ac]\s?\d[\d.,]*"
    r"|\b\d[\d.,]*\s?(?:%|g|kg|grams?|kilos?|ml|cl|litres?|liters?|pints?|oz|lbs?|tbsp|tsp"
    r"|cups?|mugs?|slices?|sheets?|hours?|hrs?|minutes?|mins?|days?|weeks?|months?|years?"
    r"|miles?|km|metres?|meters?|pounds?|quid|dollars?|euros?|degrees?)\b", re.I)
_AN_AMOUNT_ASKED = re.compile(r"\bhow\s+(?:much|many)\b", re.I)


def _the_figure_for_a_thing(said, lines, memory):
    if not _AN_AMOUNT_ASKED.search(said):
        return None
    wanted = about(said) - _VAGUE
    if not wanted:
        return None
    for line in reversed(lines):
        if not wanted & about_any(line):
            continue
        found = _A_FIGURE.search(line)
        if found:
            return "You said " + found.group(0).strip().rstrip(" .,") + "."
    return None


def _the_line_itself(said, lines, memory):
    figure = bool(_NOT_A_DETAIL.search(said))
    if figure and not _the_kind_asked(said):
        return None
    wanted = about(said)
    if not wanted:
        return None
    line = None if figure else _the_best_line(wanted, lines,
                                             questions=bool(_INTENTION.search(said)))
    if figure or not line:
        return None
    named = {_stem(word) for word in _words(said) if _AN_ATTRIBUTE.fullmatch(word)}
    if named and not (named & about_any(line)):
        return None
    answered = about_any(_the_last_reply(memory))
    if wanted & about_any(line) & answered:
        return None
    value = _the_value(line)
    if value:
        return "You said " + value.rstrip(" .") + "."
    return 'You said: "' + _carried(line, wanted) + '"'


_MEMORY_READERS = (_the_value_of_the_kind, _the_figure_for_a_thing, _the_line_itself)


def _the_kind_they_gave(said, lines, memory):
    found = kinds.the_line_that_gives(said, lines)
    if not found:
        return None
    return 'You said: "' + found["line"] + '"'



def the_kind_they_gave(text, memory):
    said = flat(text)
    if not said:
        return None
    if _A_THE_CALENDAR.search(said) and not _A_SAID_AGAIN.search(said):
        return None
    return kinds.the_line_that_gives(said, the_lines(memory))


def an_earlier_turn(text, memory):
    said = flat(text)
    lines = the_lines(memory)
    if len(lines) > 1 and lines[-1] == said:
        lines = lines[:-1]
    if not is_a_recall_ask(said):
        return _the_kind_they_gave(said, lines, memory)
    for reader in _MEMORY_READERS:
        answer = reader(said, lines, memory)
        if answer:
            return answer
    return _the_kind_they_gave(said, lines, memory)


def reply_for(text, memory):
    return an_earlier_turn(text, memory)
