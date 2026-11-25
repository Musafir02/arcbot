
import re

BABY_WORDS = frozenset("""
baby babies babydoll newborn babe infant toddler twins nappy nappies pram buggy cot
labour labor midwife caesarean csection breastfeeding bottle-feeding christening
""".split())

A_BIRTH = re.compile(
    r"\b(?:had|has|having|gave|give|giving|born|arrived|arrives|delivered|induced|"
    r"in\s+labour|in\s+labor|went\s+into\s+labour|went\s+into\s+labor)\b", re.I)

JUST_BORN = re.compile(r"\bborn\b", re.I)
A_YEAR = re.compile(r"\b(?:19|20)\d\d\b")

A_BIRTH_WEIGHT = re.compile(r"\b\d+\s*(?:lb|lbs|pound|pounds|oz|ounces)\b", re.I)

NOT_THE_BABY = re.compile(
    r"\b(?:puppy|kitten|dog|cat|lamb|calf|chick|seedling|plant)\b", re.I)

HOW_MANY_TURNS = 3


def _the_lines(memory):
    lines = []
    current = memory.get("topic") if isinstance(memory, dict) else None
    if isinstance(current, dict):
        lines.append(current)
    for record in reversed((memory.get("topics") or [])[-HOW_MANY_TURNS:]):
        if isinstance(record, dict):
            lines.append(record)
    said = []
    for record in lines:
        words = record.get("words")
        text = record.get("text") or ""
        said.append(" ".join([text] + list(words) if isinstance(words, list) and words else [text]))
    return said


def the_thread_has_a_new_baby(memory, understood=None):
    if not isinstance(memory, dict):
        return False
    reading = understood if isinstance(understood, dict) else {}
    line = str(reading.get("clean") or reading.get("text") or "")
    if line and NOT_THE_BABY.search(line):
        return False
    said = _the_lines(memory)
    if not said:
        return False
    together = " ".join(said)
    if NOT_THE_BABY.search(together):
        return False
    words = set(re.findall(r"[a-z']+", together.lower()))
    if JUST_BORN.search(together) and not A_YEAR.search(together):
        return True
    if words & BABY_WORDS and (A_BIRTH.search(together) or A_BIRTH_WEIGHT.search(together)):
        return True
    if A_BIRTH_WEIGHT.search(together) and A_BIRTH.search(together):
        return True
    return False


def the_baby_is_new(memory, understood=None):
    return the_thread_has_a_new_baby(memory, understood)
