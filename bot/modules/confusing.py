import random
import re

from ..compose import fallback, hedge

PRIORITY = -900

WITH_A_THING_LINES = (
    "Which bit of {thing} stops making sense? Say the first line that does and we'll take it "
    "from there.",
    "Which part of {thing} loses you - the start, or somewhere in the middle?",
    "What is it about {thing} that isn't going in - the words, or the order of it?",
    "Let's take {thing} one line at a time. Which line is the first one that doesn't land?",
)

WITHOUT_A_THING_LINES = (
    "What is the thing itself - a letter, a form, a set of instructions? Even the name helps.",
    "Say the last bit that made sense and I'll take it from there.",
    "Which part is clear and which part is foggy? Start where it stops making sense.",
)

SECOND_PERSON = {"my": "your", "our": "your", "me": "you", "us": "you", "mine": "yours",
                 "ours": "yours"}
SECOND_PERSON_RE = re.compile(r"\b(my|our|me|us|mine|ours)\b")


def _said_back(thing):
    return SECOND_PERSON_RE.sub(lambda m: SECOND_PERSON[m.group(1)], thing or "").strip()


def respond(text, memory):
    understood = memory.get("understood") or {}
    confusion = understood.get("confusion") or {}
    if not confusion:
        return None
    clean = fallback._matchable(text)
    if not hedge.only_a_shrug(text, memory, misreads=hedge.MISREAD_AS_GOOD_NEWS):
        return None
    thing = _said_back(confusion.get("thing"))
    state = random.getstate()
    try:
        if thing:
            return fallback._choose([line.format(thing=thing) for line in WITH_A_THING_LINES],
                                    memory, clean)
        return fallback._choose(WITHOUT_A_THING_LINES, memory, clean)
    finally:
        random.setstate(state)
