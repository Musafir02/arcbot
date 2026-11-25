import hashlib
import re

from ..understanding.kinds import a_stop_ask

_A_COUNT = re.compile(r"\bhow\s+many\b", re.I)
COUNT_LINES = (
    "As many as you like - there's no cap on messages here, so send them as they come.",
    "No limit on messages: as many as you want, long or short.",
    "Send as many as you like; there's no count I'm keeping.",
)

PRIORITY = 7400

WHILE_LINES = (
    "As long as you like — I'm not watching a clock, and nothing else is waiting on me. Say when "
    "you've had enough and I'll leave it there.",
    "No limit I can see: there's nowhere else I need to be, so take the time you need. If you'd "
    "rather pick it up later, that's fine too.",
    "All the time you want — I'm not counting lines or minutes, and I keep the thread while we "
    "talk. Say the word when you want to stop.",
    "There's no clock on this at my end. Go at your own pace, and if you'd rather stop and come "
    "back to it, that's no trouble.",
)

KEEPING_LINES = (
    "Not at all — carry on, I'm following. Say the rest of it.",
    "No, and I'd say so if it got hard to follow. Keep going.",
    "You're not boring me. Take as long as it needs.",
    "Not a bit of it. Nothing else is happening at this end, so go on.",
    "You're fine. I'm reading all of it, and I'll ask if I lose the thread.",
)

WHILE_TAILS = (
    "",
    "Where were we?",
    "What were you in the middle of?",
)
KEEPING_TAILS = ("",)


def _seed(text):
    return int.from_bytes(hashlib.sha1(str(text or "").encode("utf-8")).digest()[:6], "big")


def _pick(lines, text):
    return lines[_seed(text) % len(lines)]


THEIR_OWN_STOP = re.compile(
    r"(?:should|shall|can|could|may)\s+(?:i|we)\s+"
    r"(?:stop|quit|give\s+up|pack\s+it\s+in|leave\s+it|jack\s+it\s+in)"
    r"(?:\s+(?:now|then|it|this|that|doing\s+(?:it|this|that)))?\s*[.!?]*")


def _a_bare_stop_about_a_thing(text, memory):
    said = " ".join(str(text or "").lower().split())
    if not THEIR_OWN_STOP.fullmatch(said):
        return False
    if not a_stop_ask(said):
        return False
    topic = (memory or {}).get("topic") or {}
    return bool(str(topic.get("text") or "").strip())


def _the_kind(understood):
    if not isinstance(understood, dict):
        return None
    kind = understood.get("about_bot_kind")
    return kind if kind in ("while", "keeping") else None


def _already_said(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns:
        return ""
    last = turns[-1]
    if isinstance(last, dict):
        return str(last.get("bot") or "")
    return ""


def TAKES_AS_IT_COMES(text, memory=None):
    understood = memory.get("understood") if isinstance(memory, dict) else None
    return _the_kind(understood) is not None


def respond(text, memory):
    understood = memory.get("understood") if isinstance(memory, dict) else None
    kind = _the_kind(understood)
    if kind is None:
        return None
    if kind == "keeping" and _a_bare_stop_about_a_thing(text, memory):
        return None
    said = _already_said(memory)
    if kind == "while" and _A_COUNT.search(str(text or "")):
        lines, tails = COUNT_LINES, ("",)
    elif kind == "while":
        lines, tails = WHILE_LINES, WHILE_TAILS
    else:
        lines, tails = KEEPING_LINES, KEEPING_TAILS
    order = _rotate(lines, text)
    for line in order:
        if line not in said:
            break
    else:
        line = order[0]
    tail = _pick(tails, text + " tail")
    return (line + (" " + tail if tail else "")).strip()


def _rotate(lines, text):
    at = _seed(text) % len(lines)
    return tuple(lines[at:]) + tuple(lines[:at])
