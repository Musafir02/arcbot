import re

from ..compose import pick
from . import meant

DOUBTS_THE_ANSWER = re.compile(
    r"\b(?:that|this|it|you|youre|you're)\s+(?:makes?|made|making|doesnt|doesn't|isnt|isn't|are|"
    r"arent|aren't)\s+(?:no|not|any)\s+(?:sense|sensible)\b"
    r"|\b(?:not|never) making (?:any )?sense\b"
    r"|\b(?:doesnt|doesn't|didnt|didn't|wouldnt|wouldn't|wont|won't)\s+(?:make|makes|made)\s+"
    r"(?:any\s+)?sense\b"
    r"|\bare you (?:sure|certain)\b|\byou sure\b"
    r"|\b(?:that|this|it) (?:cant|can't|cannot|doesnt|doesn't|wont|won't) be right\b"
    r"|\b(?:thats|that's|this is) (?:nonsense|rubbish|wrong|not right|a load of)\b"
    r"|\b(?:youre|you're|you are|u r) (?:confusing|confused) me\b"
    r"|\bi (?:dont|don't) follow\b|\bi (?:dont|don't) get (?:that|this|it)\b",
    re.I)

SAYS_THE_ANSWER_IS_WRONG = re.compile(
    r"\b(?:cant|can't|cannot|doesnt|doesn't|wont|won't) be right\b"
    r"|\b(?:nonsense|rubbish|not right|wrong|a load of)\b"
    r"|\bare you (?:sure|certain)\b|\byou sure\b", re.I)

DOUBT_TAIL = frozenset("""at all though tho tbh really sorry mate love god no way innit like
    ok okay then haha lol""".split())

UNCLEAR_ANSWER = (
    "That is on me. Which bit was the muddled one?",
    "Fair enough. Say which part and I will put it another way.",
    "Let me try that again, plainer. Which bit lost you?",
)

DOUBTING = (
    "Fair enough to check it. Which bit looks wrong, and I'll say where I got it.",
    "Then I may have it wrong. Say what you were expecting and we'll compare the two.",
    "It could be out of date, that is a real risk with these things. Point at the part and I will "
    "go through it.",
)

_MEANT_LEADS = tuple(sorted(lead.split("{", 1)[0].strip().lower()
                            for lead in meant.REPEAT_LEADS + meant.LEADS))

SHORTEST_ANSWER = 40
MOST_WORDS_IN_A_DOUBT = 9


def _the_answer_just_given(memory):
    if not isinstance(memory, dict):
        return ""
    turns = memory.get("turns")
    if not isinstance(turns, list) or not turns:
        return ""
    last = turns[-1]
    return str(last.get("bot") or "") if isinstance(last, dict) else ""


def the_doubt(text, memory):
    said = _the_answer_just_given(memory)
    if len(said.strip()) < SHORTEST_ANSWER:
        return None
    line = " ".join(str(text or "").lower().replace("\u2019", "'").split())
    words = line.split()
    if not words or len(words) > MOST_WORDS_IN_A_DOUBT:
        return None
    hit = None
    for found in DOUBTS_THE_ANSWER.finditer(line):
        tail = line[found.end():].strip(" .,!?;:-")
        if all(word in DOUBT_TAIL for word in tail.split()):
            hit = found
    if not hit:
        return None
    if SAYS_THE_ANSWER_IS_WRONG.search(line) and not re.search(r"\bsense\b", line, re.I):
        return "wrong"
    return "unclear"


def reply_for(text, memory):
    kind = the_doubt(text, memory)
    if kind is None:
        return None
    line = " ".join(str(text or "").lower().replace("\u2019", "'").split())
    if kind == "wrong":
        return pick(DOUBTING, memory, line)
    plainer = meant.answer_for(line, memory) if isinstance(memory, dict) else None
    if plainer and plainer.lower().startswith(_MEANT_LEADS):
        return None
    return pick(UNCLEAR_ANSWER, memory, line)
