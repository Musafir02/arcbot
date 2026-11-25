import re

from ..compose import talkto, urgent
from ..compose.fallback_data import WHO_TO_ASK
from ..knowledge.lookup import find as find_entry

PRIORITY = -500

ANSWERS_INSTEAD = ("small-talk",)

_A_GENERIC_OPENER = frozenset(("conversation-openers",))

_ROUTES = tuple(sorted({who for _, who in WHO_TO_ASK}, key=len, reverse=True))


def _the_entry_for(text):
    try:
        text = talkto.the_line_as_read(text)
    except Exception:
        text = text
    words = " ".join((text or "").lower().split())
    if not words:
        return None
    try:
        return find_entry({"clean": words, "words": words.split()})
    except Exception:
        return None


def DEFERS_TO(reply, text):
    found = _the_entry_for(text)
    return found is None or found.id not in _A_GENERIC_OPENER


_A_LIFE_AT_RISK = re.compile(
    r"suicid|kill(?:ing)?\s+myself|self[\s-]?harm|hurt(?:ing)?\s+myself|end(?:ing)?\s+my\s+life|"
    r"end(?:ing)?\s+it\s+all|take\s+my\s+own\s+life|want(?:ing|ed)?\s+to\s+die|"
    r"(?:not\s+want(?:ing)?|do(?:n'?t|\s+not)\s+want(?:ing)?)\s+to\s+"
    r"(?:be\s+here|live|go\s+on|carry\s+on)|better\s+off\s+dead|no\s+reason\s+to\s+live", re.I)


def _the_entry_the_line_reached(memory):
    understood = memory.get("understood")
    if not isinstance(understood, dict):
        return None
    try:
        return find_entry(understood)
    except Exception:
        return None


def _is_the_opener(entry):
    return entry is not None and entry.id in _A_GENERIC_OPENER


def _a_route_is_named(reply):
    said = (reply or "").strip()
    return bool(said) and any(said.startswith(who) for who in _ROUTES)


def _the_composer_says_a_route(text, memory):
    from . import greeting

    try:
        said = greeting.respond(text, dict(memory))
    except Exception:
        return False
    return _a_route_is_named(said)


def respond(text, memory):
    if not isinstance(memory, dict):
        memory = {}
    if urgent.reply_for(text, memory):
        return None
    if _A_LIFE_AT_RISK.search(text):
        return None
    entry = _the_entry_the_line_reached(memory)
    if entry is not None and not _is_the_opener(entry):
        return None
    if entry is None:
        found = _the_entry_for(text)
        if found is not None and not _is_the_opener(found):
            return None
    if not _is_the_opener(entry) and _the_composer_says_a_route(text, memory):
        return None
    understood = memory.get("understood")
    clean = understood.get("clean") if isinstance(understood, dict) else ""
    return talkto.answer_for(clean or text, memory) or None
