import re

from . import fallback, verdict
from ..memory import another

NUDGES = frozenset((
    "and", "then", "and then", "the rest", "and the rest",
))
LEADING = frozenset(("ok", "okay", "right", "well", "so", "yes", "yeah", "and", "but", "then",
                     "alright", "cool", "great", "thanks", "ta", "ah", "oh"))
SHORT_BACK = 120
SYMPATHY_OPEN = ("sorry to hear", "so sorry", "i'm sorry", "im sorry", "that sounds", "awful",
                 "that's tough", "thats tough", "that's such", "thats such", "how awful")
STILL_END = (
    "That's the lot of it from me on that one. Say if you want to go back over any part of it.",
    "That's everything I have on it, and it is all above. Which bit do you want to unpick?",
    "That's the whole of it as far as I know. Is there a part of it you are unsure about?",
    "Nothing more from me on that one - it is all said. Anything in it worth going over?",
    "That's as far as I can take it. Say the word and we will go back over a piece of it.",
)


STILL_AFTER_A_LOSS = (
    "No rush on any of it. If you want to say more about them, I am here for that.",
    "Take your time - nothing here needs finishing. Say more about them whenever you like.",
    "That's all from me, and there is no hurry. I am still here if you want to talk about them.",
)
STILL_AFTER_A_HARD_DAY = (
    "No rush with it. I am still here if you want to say more about how things are.",
    "Nothing to finish here - take your time. Say more whenever you want to.",
    "That's all from me for now, and no hurry at all. I am here if you want to keep going.",
)
SORROW_MODULES = ("loss", "grief")
HARD_MODULES = ("safety", "urgent")


def _flat(text):
    return " ".join(str(text or "").lower().replace("\u2019", "'").split())


def _is_a_nudge(flat):
    if not flat or len(flat.split()) > 4:
        return False
    words = [w.strip(".,!?;:-") for w in flat.split()]
    if " ".join(w for w in words if w) in NUDGES:
        return True
    while len(words) > 1 and words[0] in LEADING:
        words = words[1:]
    words = [w for w in words if w]
    return " ".join(words) in NUDGES


def _ours(said):
    low = str(said or "").lower()
    for template in STILL_END:
        head = template.split("{")[0].strip().lower()
        if head and low.startswith(head):
            return True
    return False


def _answer_behind(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    try:
        if fallback._hedged_recently(memory):
            return ""
    except Exception:
        return ""
    walked = list(reversed(turns or []))
    for index, turn in enumerate(walked):
        if not isinstance(turn, dict):
            return ""
        if turn.get("module") in verdict.UNREADABLE:
            return ""
        said = turn.get("bot")
        if not isinstance(said, str) or not said.strip() or _ours(said):
            continue
        if turn.get("module") == "greeting":
            if said.strip().endswith("?"):
                return ""
            if not _continues_an_answer(walked[index + 1:]):
                return ""
            continue
        if said.strip().endswith("?"):
            return ""
        if _flat(said).startswith(SYMPATHY_OPEN):
            return ""
        if turn.get("module") == "memory_store" and _a_hand_back(said):
            return said
        return said if (verdict._steps(said) or len(re.split(r"(?<=[.!?]) ", said.strip())) > 1) \
            else ""
    return ""


def _continues_an_answer(behind):
    for turn in behind:
        if not isinstance(turn, dict) or turn.get("module") in ("greeting",) + tuple(verdict.UNREADABLE):
            continue
        said = turn.get("bot")
        if isinstance(said, str) and len(said.split()) >= 5:
            return True
    return False


def _a_hand_back(said):
    text = str(said or "")
    try:
        from ..memory import repeat
        parts = [part.strip() for part in repeat.SENTENCE.split(text.strip()) if part.strip()]
    except Exception:
        return False
    return bool(parts) and len(parts[0].split()) >= 6


def _sorrow_behind(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns:
        return ""
    try:
        if fallback._hedged_recently(memory):
            return ""
    except Exception:
        return ""
    last = turns[-1]
    if not isinstance(last, dict):
        return ""
    module = last.get("module")
    if module in HARD_MODULES:
        return ""
    if module in SORROW_MODULES:
        return "loss"
    said = last.get("bot")
    if isinstance(said, str) and _flat(said).startswith(SYMPATHY_OPEN):
        return "hard"
    return ""


def _the_rest_is_anothers(clean, memory=None):
    try:
        return another.other_option(clean, memory) is not None
    except Exception:
        return False


def takes_as_it_comes(text, memory):
    try:
        if _the_rest_is_anothers(text, memory):
            return False
        return bool(_is_a_nudge(_flat(text)) and (_answer_behind(memory) or _sorrow_behind(memory)))
    except Exception:
        return False


def reply_for(clean, memory):
    try:
        if not takes_as_it_comes(clean, memory):
            return None
        sorrow = _sorrow_behind(memory)
        pool = {"loss": STILL_AFTER_A_LOSS, "hard": STILL_AFTER_A_HARD_DAY}.get(sorrow, STILL_END)
        return verdict._say(pool, memory, _flat(clean))
    except Exception:
        return None
