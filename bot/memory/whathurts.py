
import random
import re

from . import facts as extract
from . import last_user
from .told import _quote as quote_said

BODY_PARTS = extract.BODY_PARTS
BODY_PART = extract.BODY_PART

WHICH_PART = re.compile(r"\bwhich (?:one|side|part|" + "|".join(BODY_PARTS) + r")\b"
                        r"|\bwhat side\b|\bleft or right\b", re.I)

AFTER_WHICH_ONE = re.compile(r"\bwhich one\b(.*)$", re.I)
A_SIDE_TAIL = frozenset((
    "was", "is", "it", "that", "did", "i", "say", "said", "then", "again", "exactly", "hurts",
    "hurt", "of", "them", "those", "the", "two", "please", "one", "side", "part", "was"))

HURTING_ASK = re.compile(r"\b(?:hurt|hurts|hurting|sore|ache|aching|pain|painful)\b", re.I)


def _vary(options, memory):
    turns = memory.get("turns") or []
    recent = {t.get("bot") for t in turns[-5:]}
    fresh = [o for o in options if o not in recent] or list(options)
    return random.Random(len(turns)).choice(fresh)


def which_one_is_a_side(low):
    found = AFTER_WHICH_ONE.search(low)
    if not found:
        return True
    return not [word for word in re.findall(r"[a-z']+", found.group(1).lower())
                if word not in A_SIDE_TAIL]


def before(memory):
    held = (memory.get("user") or {}).get("hurts") or {}
    return str(held.get("part") or "") if isinstance(held, dict) else ""


def after(memory, held_before):
    held = (memory.get("user") or {}).get("hurts")
    if (isinstance(held, dict) and held_before
            and str(held.get("part") or "") != held_before):
        held["was"] = held_before


ASKED_ABOUT_A_PART = re.compile(r"^\s*(?:who|what|which|when|where|why|how|does|do|did|is|are|was|"
                                r"should|shall|can|could|would|will|any)\b|\?\s*$", re.I)


def _a_question_about_a_part(line):
    return bool(ASKED_ABOUT_A_PART.search(str(line or "")))


def what_is_hurting_reply(memory, low):
    if not HURTING_ASK.search(low) or not re.search(r"\bsa(?:y|id)\b|\bwhat .*\b(?:hurt|sore|pain)\b",
                                                    low):
        return None
    held = (memory.get("user") or {}).get("hurts")
    if not isinstance(held, dict) or not held.get("part"):
        previous = " ".join(str(last_user(memory) or "").split())
        if _a_question_about_a_part(previous):
            asked = extract.BODY_PART.search(previous.lower())
            what = asked.group(1).lower() if asked else "it"
            return _vary(["You asked about a sore " + what + " - you haven't told me about "
                          "anything of your own hurting.",
                          "Nothing of yours - you were asking about a sore " + what + "."], memory)
        if (extract.BODY_PART.search(previous.lower())
                and extract.BODY_HURTS.search(previous.lower())):
            return quote_said(previous, memory)
        return _vary(["You haven't told me about anything hurting.",
                      "Nothing of yours is hurting as far as I know.",
                      "You haven't said that anything is hurting."], memory)
    part = str(held.get("part") or "")
    was = str(held.get("was") or "")
    side = str(held.get("side") or "")
    one = "your " + (side + " " if side else "") + part
    verb = "were" if part.endswith("s") else "was"
    if was:
        return _vary(["It is " + one + " - you put the " + was + " right.",
                      one[:1].upper() + one[1:] + ", since you put the " + was + " right.",
                      "You said " + one + " in the end, not the " + was + "."], memory)
    return _vary(["It is " + one + " that you said " + verb + " hurting.",
                  one[:1].upper() + one[1:] + " - that is the one.",
                  "You said " + one + "."], memory)


def the_part_asked(memory, low):
    if not WHICH_PART.search(low):
        return None
    if not which_one_is_a_side(low):
        return None
    held = (memory.get("user") or {}).get("hurts")
    if not isinstance(held, dict) or not held.get("part"):
        return None
    part = str(held.get("part") or "").strip().lower()
    asked = BODY_PART.search(low)
    if asked and asked.group(1).lower() not in (part, part.rstrip("s"), part + "s"):
        return None
    if not asked:
        previous = " ".join(str(last_user(memory) or "").lower().split())
        if part not in previous and part.rstrip("s") not in previous:
            return None
    side = str(held.get("side") or "").strip()
    place = str(held.get("place") or "").strip()
    if side:
        said = _vary([side[:1].upper() + side[1:] + " " + part + ".",
                      "Your " + side + " " + part + " - that is what you said.",
                      "The " + side + " one."], memory)
        if place:
            said = _vary([side[:1].upper() + side[1:] + " " + part + ", " + place + " side.",
                          "Your " + side + " " + part + ", the " + place + " of it."], memory)
        return said
    if place:
        return _vary(["The " + place + " of it - you did not say which side.",
                      "The " + place + " of your " + part + ", you said. Left or right you did "
                      "not say.",
                      "You said the " + place + " of it. Not which side."], memory)
    return _vary(["You said your " + part + ", without saying which side.",
                  "Just your " + part + " - you did not say left or right."], memory)
