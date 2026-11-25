
import datetime
import re

A_BIRTH_YEAR = (
    "Born in {born}, so you turn {turned} this year.",
    "{born}. That makes you {turned} this year.",
    "Noted - {turned} this year, going by {born}.",
)

_A_BORN = re.compile(
    r"\b(?:i\s+was\s+born|i\s+am\s+born|im\s+born|born)\b[^0-9]{0,14}\b(1[89]\d\d|20\d\d)\b", re.I)
_SOMEONE_ELSE_BORN = re.compile(
    r"\b(?:my|his|her|their|our|your|its)\s+(?:\w+\s+){0,2}?(?:was|were|is|are)\s+born\b", re.I)
_ALSO_AN_AGE = re.compile(
    r"\b(?:i\s?m|i\s+am|im|i\s+turned|i\s+will\s+be)\s+(\d{1,3})\b(?!\s*(?:years?\s+(?:ago|from)|"
    r"kg|pounds?|miles?|minutes?|hours?|days?|weeks?|months?))", re.I)


def _today():
    return datetime.date.today()


def _the_store(memory):
    from . import user
    return user(memory)


def _a_slip(clean):
    rest = str(clean or "").strip()
    born = _A_BORN.search(rest)
    if born:
        rest = (rest[:born.start()] + " " + rest[born.end():]).strip()
    return not re.search(
        r"\?|\b(?:how|what|when|where|why|who|which|should|can|could|would|do|does|did|is|are|"
        r"will|any)\b", rest, re.I)


def reply(text, memory):
    said = str(text or "")
    if not said or not _A_BORN.search(said) or _SOMEONE_ELSE_BORN.search(said):
        return None
    if not _a_slip(said) or len(said.split()) > 12:
        return None
    year = memory.get("born_year")
    try:
        year = int(year)
    except (TypeError, ValueError):
        return None
    turned = _today().year - year
    try:
        stated = _the_store(memory).get("age")
        if stated is not None and 0 < int(stated) < 130:
            turned = int(stated)
    except Exception:
        pass
    if not 0 < turned < 130:
        return None
    from ..compose import pick
    return pick(tuple(line.format(born=year, turned=turned) for line in A_BIRTH_YEAR), memory, said)


def observe(text, memory):
    said = str(text or "")
    if not said:
        return
    born = _A_BORN.search(said)
    if not born or _SOMEONE_ELSE_BORN.search(said):
        return
    try:
        year = int(born.group(1))
    except (TypeError, ValueError):
        return
    this_year = _today().year
    if not 1900 <= year <= this_year:
        return
    memory["born_year"] = year
    if _ALSO_AN_AGE.search(said):
        return
    turned = this_year - year
    if not 0 < turned < 130:
        return
    try:
        facts = _the_store(memory)
    except Exception:
        return
    if "age" in facts:
        return
    from . import remember
    remember(memory, "age", turned, said)
