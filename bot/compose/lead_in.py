import copy
import re

from . import fallback
from ..memory import ack

LEAD_IN = re.compile(
    r"^\s*(?:(?:and|but|so|also|plus|then|ok|okay|right|well|oh|ah|now|anyway|still)\b[\s,.!\-]*)+",
    re.I)

A_QUESTION = re.compile(
    r"^(?:is|are|was|were|am|do|does|did|can|could|will|would|should|shall|may|might|"
    r"have|has|had|what|when|where|which|who|whose|why|how)\b", re.I)
FEWEST_WORDS = 3

THE_FLOOR_OR_A_NOD = re.compile(
    r"^(?:ask away|i'?m listening|i am listening|go on\b|tell me more|say more\b|"
    r"i'?m here\b|take your time|over to you|spill it|i'?m all ears|"
    r"got it\b|noted\b|thanks for telling me|fair enough|right then|okay then|"
    r"sure\b|of course\b|go ahead\b|i'?ll do my best|good luck with it|"
    r"anything else\b|what'?s on your mind|ask me anything)", re.I)


def _only_the_floor_or_a_nod(said):
    text = str(said or "").strip()
    if not text:
        return True
    if fallback.is_a_hedge(text):
        return True
    try:
        if ack.reads_as_a_receipt(text):
            return True
    except Exception:
        pass
    return bool(THE_FLOOR_OR_A_NOD.match(text))


def _the_rest_after_the_lead_in(line):
    match = LEAD_IN.match(line)
    if not match:
        return ""
    rest = line[match.end():].strip()
    if not rest or not A_QUESTION.match(rest):
        return ""
    if len(rest.split()) < FEWEST_WORDS:
        return ""
    return rest


def _a_copy(memory):
    try:
        return {key: value if key == "turns" else copy.deepcopy(value)
                for key, value in memory.items()}
    except Exception:
        return memory


def _read_as_its_own_line(rest, memory):
    mine = _a_copy(memory)
    try:
        from ..modules import understand
        understand.observe(rest, mine)
    except Exception:
        return mine
    return mine


NAMED_HELP_NOW = re.compile(
    r"\b(?:999|112|111|ambulance|a&e|casualty|emergency|suicid\w*|overdos\w*|poison\w*|"
    r"bleeding|unconscious|not breathing|chest pain|anaphyla\w*)\b", re.I)


NO_NEWS = frozenset("""a an and the i me my we us our you your it its is was were be been being am
are do does did done can could would should will shall may might must have has had having to of in
on at for with from about as that this these those there here then now so but or if not no yes
well oh ah ok okay right sure got noted thanks thank you please just very really quite too also
still any some all more most much many long far off soon quickly quick plenty time times diary
forward looking look round around coming come going go ahead mind anything something nothing else
one ones what whats when where which who why how say said tell told""".split())


def _an_echo_of_the_ask(said, line):
    words = re.findall(r"[a-z0-9&']+", str(said or "").lower())
    asked = set(re.findall(r"[a-z0-9&']+", str(line or "").lower()))
    return not [word for word in words if word not in NO_NEWS and word not in asked]


def _a_reply_of_its_own(said):
    return bool(said) and not _only_the_floor_or_a_nod(said)


def the_answer_the_lead_in_hid(text, memory):
    line = " ".join(str(text or "").strip().split())
    rest = _the_rest_after_the_lead_in(line)
    if not rest:
        return None
    whole = fallback.reply_for(line, _a_copy(memory))
    if not _only_the_floor_or_a_nod(whole) and not _an_echo_of_the_ask(whole, line):
        return None
    without = fallback.reply_for(rest, _read_as_its_own_line(rest, memory))
    if not _a_reply_of_its_own(without) or without == whole:
        alone = {key: value for key, value in memory.items() if key != "turns"}
        fresh = fallback.reply_for(rest, _read_as_its_own_line(rest, alone))
        if fresh and _a_reply_of_its_own(fresh) and fresh != whole:
            without = fresh
    if not without:
        return None
    if without == whole:
        return None
    if NAMED_HELP_NOW.search(str(whole or "")) or NAMED_HELP_NOW.search(str(without or "")):
        return None
    if not _a_reply_of_its_own(without):
        return None
    return without
