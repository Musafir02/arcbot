
import random
import re

from . import fallback

YES_LINES = (
    "Yes - it is serious, and that is why ringing is the thing to do now rather than something to "
    "sleep on. Tell me how it goes.",
    "Yes. Ringing is not an overreaction here: it is the whole point of the line I gave you. Do "
    "that first, and come back to me after.",
    "Yes it is, and the number I gave you is what it is for. Make the call, and we can go through "
    "the rest after.",
    "Yes - this is not one to wait and see about. Do the call now, and come back to me when you "
    "have.",
)

_CONTINUATION = ("greeting", "already")

_EMERGENCY_CASES = frozenset((
    "abuse", "bleeding", "breathing", "chest", "chest_slow", "dog_attack", "dog_bite", "fire",
    "gas", "general", "hanging", "head_injury", "heat", "overdose", "poison", "seizure",
    "self_harm", "stroke", "swallowed_thing", "unconscious",
))

AFTER_THE_CALL_LINES = (
    "Still yes - and you have made the call, which was the part that mattered. Stay with what they "
    "tell you, and say if anything changes.",
    "Still yes, and it is with people who can do something about it now. Do what they say over "
    "anything I could offer, and tell me how it goes.",
    "Yes it is, and the call was the thing to do - you have done it. Whatever they told you to do "
    "next is what matters now.",
)

_CALLS_SOMEBODY = re.compile(
    r"\b(?:999|911|112|ambulance|paramedics|emergency\s+services|116\s?123|988|0808|0800|1-?800)\b")


_HELP_IS_COMING = re.compile(
    r"\b(?:i|we|he|she|they)\s+(?:have\s+|had\s+|has\s+)?(?:already\s+)?(?:rang|phoned|called)\b"
    r"|\brang\s+(?:them|999|911|112|an\s+ambulance|the\s+(?:police|line))\b"
    r"|\b(?:on\s+(?:their|its|the)\s+way|are\s+coming|is\s+coming|are\s+here|is\s+here|"
    r"has\s+arrived|have\s+arrived|the\s+crew|paramedics|the\s+operator|the\s+emergency\s+line|"
    r"fire\s+brigade|emergency\s+line\s+says|they\s+said)\b")


def _the_answer_behind(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    after = []
    for turn in reversed(turns[-6:]):
        if turn.get("module") == "safety":
            after.append(str(turn.get("user") or "").lower())
            return str(turn.get("bot") or "").lower(), after
        if turn.get("module") not in _CONTINUATION:
            return None, []
        said = " ".join((str(turn.get("user") or ""), str(turn.get("bot") or "")))
        after.append(said.lower())
    return None, []


_AGREES_IT_IS_BAD = re.compile(
    r"^\W*(?:that|thats|that'?s|this|it|its|it'?s)\s+(?:is\s+|was\s+)?"
    r"(?:really\s+|pretty\s+|very\s+|so\s+|proper\s+|well\s+)?"
    r"(?:bad|awful|terrible|serious|grim|horrible|scary|frightening)\W*$")


def _a_bare_verdict_ask(text, memory, clean):
    read = memory.get("understood")
    if isinstance(read, dict) and read.get("asks_a_verdict"):
        return True
    if _AGREES_IT_IS_BAD.match(clean):
        return True
    return bool(fallback.reads_as_a_verdict(text, memory))


def reply_for(text, memory):
    clean = " ".join(str(text or "").lower().split())
    if not clean:
        return None
    behind, after = _the_answer_behind(memory)
    if not behind:
        return None
    if memory.get("safety_case") not in _EMERGENCY_CASES:
        return None
    if memory.get("safety_safe") is True:
        return None
    if not _CALLS_SOMEBODY.search(behind):
        return None
    if not _a_bare_verdict_ask(text, memory, clean):
        return None
    pool = AFTER_THE_CALL_LINES if any(_HELP_IS_COMING.search(said) for said in after) else YES_LINES
    options = [line for line in pool
               if line not in [t.get("bot") for t in (memory.get("turns") or [])[-5:]]]
    if not options:
        options = list(pool)
    seed = len(memory.get("turns") or []) * 7919 + sum(ord(c) for c in clean + behind)
    return random.Random(seed).choice(options)
