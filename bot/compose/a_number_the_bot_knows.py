
import re

LINES = (
    (("samaritans", "samaritan"),
     "Samaritans is 116 123 - free, any hour."),
    (("domestic abuse helpline", "domestic violence helpline", "national domestic abuse helpline",
      "refuge", "womens aid", "women's aid"),
     "The domestic abuse helpline is 0808 2000 247 - free, any hour, and they will plan the next "
     "step with you."),
    (("acas",),
     "ACAS is 0300 123 1100, charged at your usual rate, and they will tell you where you stand "
     "on a work problem."),
    (("nhs 111", "111", "nhs direct"),
     "NHS 111 is on 111 - free, any hour, and they will say what to do about a symptom and where "
     "to go."),
    (("988",),
     "988 is the crisis line in the US - free, any hour, and you can call or text it."),
    (("999", "911", "112", "emergency services"),
     "Ring 999 - or 911, or 112 - and say where you are and what has happened."),
)

ASKS = (
    re.compile(r"(?<![a-z])(?:what(?:'s|s| is)?\s+the\s+|what\s+is\s+the\s+|the\s+|whats\s+|what\s+)?"
               r"(?:phone\s+|telephone\s+)?number\s+(?:for|of|to)\s+(.{2,60})$"),
    re.compile(r"(?<![a-z])(?:do you have|have you got|any idea of)\s+(?:a\s+|the\s+)?"
               r"(?:phone\s+)?number\s+(?:for|of|to)\s+(.{2,60})$"),
    re.compile(r"(?<![a-z])(?:how do i|how can i|how to|where do i|can i|do i)\s+"
               r"(?:ring|call|phone|dial|contact|reach)\s+(.{2,60})$"),
    re.compile(r"(?<![a-z])(?:what(?:'s|s| is)?\s+the\s+)?(?:phone\s+)?number\s+(?:for\s+)?"
               r"(.{2,40}?)\s+again$"),
    re.compile(r"^(.{2,40}?)(?:'s|s)?\s+(?:phone\s+)?number$"),
    re.compile(r"^(.{2,40}?)\s+(?:phone\s+)?number\s*\?*$"),
    re.compile(r"(?<![a-z])([a-z][a-z' ]{1,40}?)\s+(?:phone\s+)?number\s*[?!.]*$"),
)

NO_NUMBER_HERE = (
    (("childline",), "I don't have Childline's number here. A search for 'childline' brings up "
                     "their own page, and the free number is on it."),
    (("alcoholics anonymous", "al anon", "alanon"),
     "I don't have Alcoholics Anonymous's number here. A search for 'alcoholics anonymous' "
     "brings up their own page, and a local meeting line is on it."),
    (("mind", "shelter", "stepchange", "age uk", "ageuk", "victim support", "cruse",
      "nspcc", "rethink"),
     "I don't hold that number. Their own page is where it lives - a search for the name brings "
     "it up, and a helpline's number is the one on it (a map app would only give you a branch)."),
)

_REPEAT_TURNS = 3

AND_THE_NEXT = re.compile(
    r"^(?:and|also|what about|how about|whats|what is|what's)\b[\s,]*(?:the\s+|a\s+)?"
    r"(?:number\s+(?:for|of)\s+)?(?:for\s+|of\s+)?(.{2,40})$")
A_BARE_NAME = re.compile(r"^[a-z][a-z' ]{1,30}$")

ASKS_AGAIN = re.compile(r"\b(?:again|what was (?:it|that)|remind me|one more time|i missed (?:it|that))\b")


def _said_before(memory):
    replies = [reply for reply in _replies(memory) if reply]
    if not replies:
        return ""
    last = replies[-1]
    for _names_, said in LINES + NO_NUMBER_HERE:
        if last == " ".join(str(said).split()):
            return said
    return ""


def _carried_thing(text):
    line = " ".join(str(text or "").lower().replace("\u2019", "'").split()).strip(" ?!.,")
    found = AND_THE_NEXT.match(line)
    if found:
        return found.group(1).strip(" ?!.,'\"")
    if A_BARE_NAME.match(line):
        return line
    return ""



_IN_FRONT = re.compile(r"^(?:sorry|hi|hello|hey|ok|okay|oh|so|and|also|er|um)\s*[,!.]\s*")
_BEHIND = re.compile(r"\s*\b(?:again|please|one more time|now|thanks|thank you)\b\s*[?!.]*$")


def _asked_about(text):
    line = " ".join(str(text or "").lower().replace("’", "'").split())
    line = line.strip(" ?!.,")
    line = _IN_FRONT.sub("", _BEHIND.sub("", line)).strip(" ?!.,")
    if not line:
        return ""
    for ask in ASKS:
        found = ask.search(line)
        if found:
            thing = found.group(1).strip(" ?!.,'\"")
            thing = re.sub(r"^(?:the|a|an)\s+", "", thing)
            if thing:
                return thing
    return ""


def _names(thing, names):
    for name in names:
        if re.search(r"(?<![a-z0-9])" + re.escape(name) + r"(?![a-z0-9])", thing):
            return True
    return False


def _replies(memory):
    out = []
    for turn in (memory or {}).get("turns") or ():
        if isinstance(turn, dict):
            out.append(" ".join(str(turn.get("bot") or turn.get("reply") or "").split()))
        elif isinstance(turn, (list, tuple)) and len(turn) >= 2:
            out.append(" ".join(str(turn[1] or "").split()))
        else:
            out.append("")
    return out


def already_said(number, memory):
    said = str(number).replace(" ", "")
    for reply in _replies(memory)[-_REPEAT_TURNS:]:
        if said and said in reply.replace(" ", ""):
            return True
    return False


def not_a_number(reply):
    return not re.search(r"\d", str(reply or ""))


def answer_for(text, memory=None):
    line = " ".join(str(text or "").lower().split())
    again = bool(ASKS_AGAIN.search(line))
    before = _said_before(memory)
    thing = _asked_about(text)
    if not thing and before:
        thing = _carried_thing(text)
    if thing:
        for names, said in LINES:
            if not _names(thing, names):
                continue
            number = re.search(r"\d[\d ]{2,}", said)
            if number and already_said(number.group(0), memory) and not again:
                return None
            return said
        for names, said in NO_NUMBER_HERE:
            if _names(thing, names):
                return said
    if before and again:
        return before
    return None
