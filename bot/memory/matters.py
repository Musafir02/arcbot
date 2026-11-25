import re

from . import people

MINE = "my "

SO = re.compile(r"^\s*(?:and|but|also|oh|well|so|see)?\s*,?\s*"
                r"(?P<who>she|he)(?P<is>'s|s)?\s+(?P<rest>[^?]{2,60})\s*$", re.I)
FACT_VERB = frozenset("""
live lives lived living is are was were has have had keeps keep kept falls fall fell falling
refuses refuse refused wont won't cant can't cannot doesnt doesn't never always still only on
takes take uses use needs need gets get goes go wants want sits sit walks walk forgets forget
wears wear uses stopped stops started starts keeps manages manages
""".split())
A_REPORT = re.compile(r"^\s*(?:says?|said|told|thinks?|wants?|asked|keeps saying|thinks)\b", re.I)
THEIR_DIET = re.compile(
    r"^(?:"
    r"(?:does\s*nt|does\s+not|do\s*nt|don'?t|won'?t|wont|cant|can'?t|never|only)"
    r"\s+(?:eat|eats|drink|drinks|touch|touches|stand|stands|like|likes|want|wants)\b"
    r"|(?:is\s+)?(?:hates?|likes?|loves?|avoids?|allergic|refuses?)\b"
    r")", re.I)
MOST_WORDS = 8

ON_THEIR_OWN = re.compile(
    r"^liv(?:es?|ing)\s+"
    r"(?:on\s+(?:her|his|their|its)\s+own|by\s+(?:her|him|them)sel(?:f|ves)|alone)\b\s*"
    r"|^(?:is\s+)?"
    r"(?:on\s+(?:her|his|their|its)\s+own|by\s+(?:her|him|them)sel(?:f|ves)|alone)"
    r"(?:\s+at\s+home)?\b\s*",
    re.I)
LIVES_ALONE = "lives alone" 


def _the_person(memory):
    others = memory.get("others") if isinstance(memory, dict) else None
    if not isinstance(others, list):
        return None
    seen = []
    for record in others:
        if not isinstance(record, dict):
            continue
        who = str(record.get("who") or "").strip().lower()
        if who and who not in [one[0] for one in seen]:
            seen.append((who, record))
    if len(seen) != 1:
        return None
    who, record = seen[0]
    sex = ""
    if who in people.HIM:
        sex = "him"
    elif who in people.HER:
        sex = "her"
    return who, record, sex


def about_them(text, memory):
    if not isinstance(text, str):
        return ""
    found = SO.match(text)
    if not found:
        return ""
    rest = " ".join(found.group("rest").split())
    if len(rest.split()) > MOST_WORDS:
        return ""
    if A_REPORT.match(rest) or THEIR_DIET.match(rest):
        return ""
    alone = ON_THEIR_OWN.match(rest)
    if alone:
        rest = (LIVES_ALONE + " " + rest[alone.end():]).strip()
    elif rest.split()[0].strip(",.").lower() not in FACT_VERB:
        return ""
    person = _the_person(memory)
    if person is None:
        return ""
    who, _record, sex = person
    said = found.group("who").lower()
    if sex and ((said == "she" and sex != "her") or (said == "he" and sex != "him")):
        return ""
    if who in rest.lower().split():
        return ""
    if alone:
        return MINE + who + " " + rest
    if found.group("is"):
        return MINE + who + " is " + rest
    return MINE + who + " " + rest

THEIR_WORD = re.compile(
    r"^\s*(?:and|but|so|also|oh|well|see)?\s*,?\s*"
    r"(?P<who>she|he|they|mum|mom|dad|nan|nana|gran|granny|grandma|grandad)\b"
    r"(?:'s|s|\s+is|\s+are)?\s+"
    r"(?:says?|said|tells? me|told me|insists?|insisted|reckons?|reckoned|claims?|claimed|"
    r"keeps saying|thinks?)\s+"
    r"(?:(?:that\s+)?(?:she|he|they)(?:'s|s|\s+is|\s+are)?\s+)?"
    r"(?P<what>fine|alright|all right|ok|okay|grand|managing|coping|all good|not too bad)\b"
    r"(?:\s*,?\s*(?:thank you|thanks|i think|i reckon|really|honestly|though|anyway|actually)"
    r"){0,2}\s*[.!]?\s*$", re.I)
CARE_MATTER = re.compile(
    r"\b(?:fall|falls|fallen|fell|falling|carer|carers|care|dementia|alzheim\w*|memory|"
    r"forget\w*|confused|hospital|stroke|doctor|gp|surgery|social services|needs assessment|"
    r"pendant|alarm|key safe|blood thinner\w*|warfarin|tablets|medication)\b", re.I)
FINE_REPLY = (
    "That usually means your {who} doesn't want a fuss, not that nothing is wrong. Don't argue "
    "the point - ask for one small thing instead, the GP appointment with you in the room, and "
    "let the doctor carry the worry.",
    "They say that to keep the peace, and it does not mean it has stopped. Keep a note of when it "
    "happens and ring your {who}'s GP yourself: they can act on what you tell them, and nobody "
    "has to ask for it.",
    "How your {who} feels is worth believing; the risk is not something to take their word for. "
    "Make the whole ask one thing you do together - the free falls review, or a walk to the end "
    "of the road - so there is nothing to admit to.",
)


def _a_worry_in_the_chat(memory):
    if not isinstance(memory, dict):
        return False
    turns = memory.get("turns") or ()
    said = []
    for turn in list(turns)[-5:]:
        if isinstance(turn, dict):
            said.append(str(turn.get("user") or ""))
        elif isinstance(turn, (list, tuple)) and turn:
            said.append(str(turn[0]))
        else:
            said.append(str(turn))
    return bool(CARE_MATTER.search(" ".join(said)))


def what_they_say(text, memory):
    if not isinstance(text, str):
        return ""
    found = THEIR_WORD.match(text)
    if not found:
        return ""
    person = _the_person(memory)
    if person is None:
        return ""
    who, _record, sex = person
    said = found.group("who").lower()
    if sex and ((said in ("she", "her") and sex != "her") or (said == "he" and sex != "him")):
        return ""
    if not _a_worry_in_the_chat(memory):
        return ""
    pool = list(FINE_REPLY)
    at = memory.get("fine_said") if isinstance(memory, dict) else 0
    if not isinstance(at, int) or at < 0:
        at = 0
    if isinstance(memory, dict):
        memory["fine_said"] = at + 1
    return pool[at % len(pool)].format(who=who)

_ONE_AGE = re.compile(r"\b(?P<age>\d{1,3})\b")
_NOT_THE_OLD_ONE = re.compile(r"\b(?:not|instead of|rather than|no wait,? not)\s+(?P<old>\d{1,3})\b",
                              re.I)
_OLDEST = re.compile(r"\b(?:oldest|eldest|older|bigger|elder|big one)\b", re.I)
_YOUNGEST = re.compile(r"\b(?:youngest|younger|littlest|little|smallest|baby|wee one)\b", re.I)
_A_CORRECTION = re.compile(r"\b(?:actually|no|nope|sorry|wait|i mean|i meant|make it|makes it|"
                           r"not|instead)\b", re.I)


def _the_group_ages(memory):
    if not isinstance(memory, dict):
        return None, []
    found = []
    for entry in memory.get("others") or ():
        if not isinstance(entry, dict):
            continue
        ages = [age for age in entry.get("ages") or () if isinstance(age, int)]
        if len(ages) > 1:
            found.append((entry, ages))
    if len(found) != 1:
        return None, []
    return found[0]


def _say_the_ages(ages):
    ages = sorted(ages)
    if len(ages) == 2:
        return "%d and %d" % (ages[0], ages[1])
    return ", ".join(str(age) for age in ages[:-1]) + " and " + str(ages[-1])


def a_corrected_age(text, memory):
    if not isinstance(text, str):
        return ""
    low = " ".join(text.lower().split())
    if not low or len(low.split()) > 10:
        return ""
    entry, ages = _the_group_ages(memory)
    if entry is None:
        return ""
    numbers = [int(m.group("age")) for m in _ONE_AGE.finditer(low)]
    numbers = [age for age in numbers if 0 < age <= 120]
    if not numbers:
        return ""
    correcting = bool(_A_CORRECTION.search(low))
    replaced = _NOT_THE_OLD_ONE.search(low)
    if replaced:
        was = int(replaced.group("old"))
        new = [age for age in numbers if age != was]
        if was in ages and new:
            ages[ages.index(was)] = new[0]
            entry["ages"] = sorted(ages)
            return "Right — %s, then." % _say_the_ages(entry["ages"])
        return ""
    if _OLDEST.search(low) and not _YOUNGEST.search(low):
        ages[ages.index(max(ages))] = numbers[0]
        entry["ages"] = sorted(ages)
        return "Right — %s, then." % _say_the_ages(entry["ages"])
    if _YOUNGEST.search(low) and not _OLDEST.search(low):
        ages[ages.index(min(ages))] = numbers[0]
        entry["ages"] = sorted(ages)
        return "Right — %s, then." % _say_the_ages(entry["ages"])
    if correcting and numbers[0] not in ages:
        which = " or the ".join(str(age) for age in sorted(ages))
        return "Which one is %d — the %s?" % (numbers[0], which)
    return ""
