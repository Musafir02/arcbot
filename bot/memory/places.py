import re

from ..memory import facts as extract
from ..memory import others
from ..memory.store_lines import WHERE_ASK



OTHER_PLACE = re.compile(
    r"\bmy (\w+)s?\b[^.!?]{0,60}?\b(?:live|lives|living|moved|moves|moving|settled|based|"
    r"staying|relocated)\s+(?:in|to|near|at)\s+([A-Za-z][A-Za-z'-]{1,}"
    r"(?:[ -][A-Za-z][A-Za-z'-]{1,})?)", re.I)
OTHER_PLACE_PRONOUN = re.compile(
    r"\b(?:she|he|they)\s+(?:has\s+|had\s+|just\s+|now\s+)?(?:live[sd]?|lives|living|"
    r"moved|moves|moving|settled|relocated|is\s+based|are\s+based)\s+(?:in|to|near|at)\s+"
    r"([A-Za-z][A-Za-z'-]{1,}(?:[ -][A-Za-z][A-Za-z'-]{1,})?)", re.I)
PLACE_ENDS = frozenset("""last next this that year years month months week weeks ago previously
before then soon now already after""".split())
OTHER_PERSON_NAMED = re.compile(
    r"\bmy (\w+)s?\b(?:[^.!?]{0,40}?\b(?:is|are|was|were)\s+(?:called|named|known as)\b|"
    r"[^.!?]{0,12}$)", re.I)
A_QUESTION_ASKED = re.compile(
    r"^\W*(?:and\s+|but\s+|so\s+)?(?:do|does|did|is|are|was|were|has|have|had|can|could|"
    r"will|would|should|shall|may|might|am)\b", re.I)


def _a_place(value):
    words = []
    for word in re.split(r"[ -]", value):
        low = word.lower()
        if low in PLACE_ENDS or low in extract.NOT_PLACES or low in extract.HOME_STOP:
            break
        words.append(word)
        if len(words) == 2:
            break
    if not words:
        return None
    first = words[0].lower()
    if first in extract.HOME_STOP or first in extract.NOT_PLACES or first in PLACE_ENDS:
        return None
    return " ".join(w[:1].upper() + w[1:] if w.islower() else w for w in words)


NOT_A_PLACE_VALUE = frozenset("""
i me my we us our you your he him his she her it its they them their
one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen
sixteen seventeen eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety
hundred thousand million first second third last next again too either neither
""".split())


def _the_place_alone(text):
    low = " ".join(str(text or "").strip().lower().rstrip(".!,").split())
    if not low or low.endswith("?"):
        return None
    opener = extract.CORRECTION_OPENER.match(low)
    if not opener:
        opener = re.match(r"not\s+[a-z'-]+[, ]+", low)
        if not opener:
            return None
    rest = low[opener.end():].strip(" .,!-")
    rest = re.sub(r"^(?:in|to|at|from|near)\s+", "", rest)
    words = rest.split()
    if not words or len(words) > 2 or any(word in NOT_A_PLACE_VALUE for word in words):
        return None
    return extract.place_value(rest) or None


def _said_places(memory):
    found = []
    last = ""
    fresh = False
    for turn in memory.get("turns") or []:
        text = turn.get("user") or ""
        if not text or text.rstrip().endswith("?") or A_QUESTION_ASKED.search(text):
            fresh = False
            continue
        named = ""
        gave = False
        for match in OTHER_PLACE.finditer(text):
            place = _a_place(match.group(2))
            named = match.group(1)
            if place:
                found.append((named, place))
                gave = True
        if not named:
            asked = OTHER_PERSON_NAMED.search(text.rstrip())
            if asked:
                named = asked.group(1)
        if named:
            last = named
        elif last and not OTHER_PLACE_PRONOUN.search(text) and fresh:
            alone = _the_place_alone(text)
            if alone:
                found.append((last, alone))
                gave = True
        if last and not gave:
            for match in OTHER_PLACE_PRONOUN.finditer(text):
                place = _a_place(match.group(1))
                if place:
                    found.append((last, place))
                    gave = True
        fresh = gave
    return found


def _a_town_moved(memory, text):
    alone = _the_place_alone(text)
    if not alone:
        low = " ".join(str(text or "").strip().lower().split())
        frame = OTHER_PLACE_PRONOUN.search(low) if extract.CORRECTION_OPENER.match(low) else None
        if not frame:
            return None
        alone = _a_place(frame.group(1))
        if not alone:
            return None
    turns = [turn.get("user") or "" for turn in (memory.get("turns") or [])]
    before = turns[-1] if turns else ""
    if not before or not (OTHER_PLACE.search(before) or OTHER_PLACE_PRONOUN.search(before)):
        return None
    said = _said_places(memory)
    if not said or said[-1][1].lower() == alone.lower():
        return None
    who = str(said[-1][0]).lower()
    plural = who.endswith("s")
    return ("Got it — your " + who + (" live in " if plural else " lives in ") + alone + ".")


def _other_place(memory, who):
    want = (who or "").lower().rstrip("s")
    found = [(said, place) for said, place in _said_places(memory)
             if not want or said.lower().rstrip("s") == want]
    if not found:
        return None
    said, place = found[-1]
    plural = said.lower().endswith("s")
    return "Your " + said.lower() + (" live in " if plural else " lives in ") + place + "."


def _asked_person(memory, low):
    named = re.search(r"\b" + WHERE_ASK + r" (?:does|do) my (\w+) (?:live|come from)\b|\b"
                      + WHERE_ASK + r" is my (\w+) (?:living|based)\b", low)
    if named:
        return named.group(1) or named.group(2) or ""
    if re.search(r"\b" + WHERE_ASK + r" (?:does|do) (?:he|she|they) (?:live|come from)\b|\b"
                 + WHERE_ASK + r" is (?:he|she|they) (?:living|based)\b", low):
        person = memory.get("person")
        who = person.get("who") if isinstance(person, dict) else ""
        if who:
            return str(who).lower()
        said = _said_places(memory)
        return str(said[-1][0]).lower() if said else ""
    plain = re.search(r"\b" + WHERE_ASK + r" (?:is|are|was|were) (?:my|our) ([a-z]+)\b", low)
    if plain:
        word = plain.group(1).lower()
        if word.endswith("s") and word[:-1] in extract.KIN_WORDS:
            word = word[:-1]
        if (word in extract.KIN_WORDS or word in extract.RELATIONS
                or any(str(one.get("who") or "").lower() == word for one in others(memory))):
            return word
    by_name = re.search(r"\b" + WHERE_ASK + r" (?:does|do) ([a-z][a-z'-]{1,}) (?:live|"
                        r"come from)\b", low)
    if by_name:
        word = by_name.group(1).lower()
        if word in ("he", "she", "they", "my", "your", "i", "we", "it", "the", "a"):
            return ""
        for entry in others(memory):
            if str(entry.get("name") or "").lower() == word:
                return str(entry.get("who") or "").lower()
    return ""
