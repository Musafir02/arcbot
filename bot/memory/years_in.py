import re

from ..compose import pick
from ..memory import facts

_A_LEAD_IN = r"(?:(?:so|well|oh|and|actually|tbh|honestly|yeah|yes)\s+,?\s*)?"
_LISTEN = r"listen\s*,\s*"
_A_LENGTH = (r"(?:for\s+|about\s+|nearly\s+|over\s+|almost\s+)?"
             r"(?P<count>\d{1,2}|an?|one|a few|a couple of|several|many)\s*(?P<unit>years?|yrs?|months?)\b")
_A_TAIL = r"(?:\s+(?:now|already|so far|in total|and counting|today|lol|haha|hah))?"
BEEN_AT_IT = re.compile(
    _A_LEAD_IN + r"(?:i(?:'ve| have)?|ive)\s+been\s+(?P<doing>[a-z][a-z' ]{0,24}?)\s+" + _A_LENGTH
    + _A_TAIL, re.I)
BEEN_AT_IT_BARE = re.compile(
    _A_LEAD_IN + r"(?:been\s+|doing\s+it\s+)(?P<doing>[a-z][a-z' ]{0,20}?)?\s*" + _A_LENGTH
    + _A_TAIL, re.I)

NOT_A_STINT = re.compile(r"\b(?:minutes?|mins?|hours?|hrs?|days?|weeks?)\b", re.I)

_A_GERUND = re.compile(r"^(?P<stem>[a-z]{3,}?)(?:ing|in)$", re.I)
THE_JOB_NOUNS = frozenset(facts.JOB_WORDS)


def _a_job_word(doing):
    low = doing.strip().lower()
    if not low:
        return False
    if low in THE_JOB_NOUNS:
        return True
    match = _A_GERUND.match(low)
    if match:
        stem = match.group("stem")
        return any(stem and word.startswith(stem) for word in THE_JOB_NOUNS)
    return False


def _alike(doing, job):
    a = re.sub(r"[^a-z]", "", doing.lower())
    b = re.sub(r"[^a-z]", "", job.lower())
    if not a or not b:
        return False
    if a in b or b in a:
        return True
    return a[:4] == b[:4]


def _the_filed_job(memory):
    user = memory.get("user") if isinstance(memory, dict) else None
    if isinstance(user, dict):
        job = user.get("job")
        if isinstance(job, str) and job.strip():
            return job.strip()
    log = memory.get("facts_log") if isinstance(memory, dict) else None
    for fact in reversed(log or []):
        if isinstance(fact, dict) and fact.get("key") == "job":
            value = fact.get("value")
            if isinstance(value, str) and value.strip():
                return value.strip()
    return ""


def _the_doing_and_the_length(text, memory):
    if not isinstance(text, str):
        return "", 0, "years"
    said = text.strip()
    if not said or "?" in said:
        return "", 0, "years"
    if NOT_A_STINT.search(said):
        return "", 0, "years"
    match = BEEN_AT_IT.fullmatch(said) or BEEN_AT_IT_BARE.fullmatch(said)
    if not match:
        return "", 0, "years"
    doing = (match.group("doing") or "").strip()
    doing = re.sub(r"^(?:a|an|the)\s+", "", doing, flags=re.I)
    filed = _the_filed_job(memory)
    if not filed:
        return "", 0, "years"
    named = not re.fullmatch(r"(?:doing\s+)?(?:it|that|this|the\s+job)", doing or "", re.I)
    if named and not _alike(doing, filed):
        return "", 0, "years"
    filing = filed
    count = _the_count(match.group("count"))
    unit = "months" if (match.group("unit") or "").lower().startswith(("month", "mnth")) else "years"
    return filing, count, unit


_NUMBERS = ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
            "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen",
            "eighteen", "nineteen")

_TENS = ("", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety", "")


def _the_count(word):
    low = str(word or "").strip().lower()
    if low.isdigit():
        return int(low)
    if low in _NUMBERS:
        return _NUMBERS.index(low)
    return {"a": 1, "an": 1, "a few": 3, "a couple of": 2, "several": 4, "many": 8}.get(low, 0)


def _the_figure_in_words(count):
    whole = int(round(count))
    if 0 <= whole < len(_NUMBERS):
        return _NUMBERS[whole].capitalize()
    if whole < 100:
        tens, ones = divmod(whole, 10)
        return (TENS_WORD(tens) + ("-" + _NUMBERS[ones] if ones else "")).capitalize()
    return str(whole)


def TENS_WORD(tens):
    return _TENS[tens] if 0 <= tens < len(_TENS) else str(tens)


def _with_an(word):
    return ("an " if word[:1].lower() in "aeiou" else "a ") + word


def _the_stint(job, count, memory=None, said="", unit="years"):
    if unit == "months" and count < 24:
        figure = _the_figure_in_words(count)
        if count < 12:
            frames = (
                "{figure} months {at_it} - the first year is the hardest stretch of it.",
                "{figure} months {at_it}. That is still the part where everyone is finding their "
                "feet.",
                "{figure} months {at_it} - how are you finding it so far?",
            )
        else:
            frames = (
                "{figure} months {at_it} - past the first year, then.",
                "{figure} months {at_it}. The first year is the one that tests everyone.",
                "{figure} months {at_it} - what has got easier?",
            )
        return pick([f.format(figure=figure, at_it=_as_a(job)) for f in frames], memory or {},
                    f"{said} {job}")
    if unit == "months":
        count = count // 12
    figure = _the_figure_in_words(count)
    if count < 1.5:
        frames = (
            "A year {at_it} - the first one is the hardest.",
            "A year in already. It gets easier from here, or at least more familiar.",
            "A year {at_it}. You've got past the bit where everyone feels useless.",
        )
        return pick([f.format(at_it=_as_a(job)) for f in frames], memory or {},
                    f"{said} {job}")
    frames = (
        "{figure} years {at_it} - that's a long stretch.",
        "{figure} years {at_it}. You must know it inside out by now.",
        "{figure} years {at_it} is more than most people stick at anything.",
        "{figure} years {at_it} - what keeps you at it?",
    )
    return pick([f.format(figure=figure, at_it=_as_a(job)) for f in frames], memory or {},
                f"{said} {job}")


def _as_a(job):
    return "as " + _with_an(job)


def the_years_in_the_doing(text, memory):
    job, count, unit = _the_doing_and_the_length(text, memory)
    if not job or count <= 0:
        return ""
    return _the_stint(job, count, memory, text, unit)


THE_PRONOUN = re.compile(r"^(?:so\s+)?(?P<who>she|he|they)(?:'s|s| has| have|'ve| have been|s been)?"
                         r"\s+been\s+(?P<doing>[a-z][a-z' ]{0,24}?)\s*", re.I)
THEIR_LENGTH = re.compile(
    r"^(?:so\s+)?(?P<who>she|he|they)(?:'s|s| has|'ve| have)?\s+been\s+"
    r"(?P<doing>[a-z][a-z' ]{0,24}?)\s+"
    r"(?:(?:for|about|nearly|over|almost)\s+)?"
    r"(?P<count>\d{1,2}|an?|one|a few|a couple of|several|many|years)\s*"
    r"(?P<unit>years?|yrs?|months?)?\b"
    r"(?:\s+(?:now|already|so far|in total|and counting|lol|haha))?\s*$", re.I)


def _the_person_holding_a_job(memory, who):
    fits = {"she": facts.SHE, "he": facts.HE}.get(who, facts.SHE | facts.HE)
    log = memory.get("facts_log") if isinstance(memory, dict) else None
    for fact in reversed(log or []):
        if not isinstance(fact, dict) or fact.get("key") != "other":
            continue
        value = fact.get("value")
        if not isinstance(value, dict):
            continue
        relation = str(value.get("who") or "").strip().lower()
        job = str(value.get("job") or "").strip()
        if not relation or not job:
            continue
        if relation in fits:
            return relation, job
    return "", ""


def _their_stint(relation, job, count, memory=None, said="", unit="years"):
    theirs = "Your " + relation
    if not count:
        frames = (
            "{theirs} has been at it a while, then. That is not nothing.",
            "{theirs} has put the years in - no wonder it comes up.",
        )
        return pick([f.format(theirs=theirs) for f in frames], memory or {}, f"{said} {job}")
    span = "months" if unit == "months" and count < 24 else "years"
    if span == "years" and unit == "months":
        count = count // 12
    figure = _the_figure_in_words(count)
    low = figure.lower()
    if span == "months" and count < 12:
        frames = (
            "{theirs} has been {a_job} for {low} months - early days, then.",
            "{low} months in as {a_job} for {theirs_lower}. The first year is the hard one.",
            "{theirs} has been {a_job} for {low} months - how is it going?",
        )
    else:
        frames = (
            "{theirs} has been {a_job} for {low} " + span + " - that's a long stretch.",
            "{figure} " + span + " is a long time for {theirs_lower} to stay in one job.",
            "{theirs} has been {a_job} for {low} " + span + ". That is a lot of years behind them.",
        )
    return pick([f.format(theirs=theirs, theirs_lower=theirs.lower(), figure=figure, low=low,
                          a_job=_with_an(job)) for f in frames], memory or {}, f"{said} {job}")


def the_years_in_their_doing(text, memory):
    if not isinstance(text, str) or not isinstance(memory, dict):
        return ""
    said = text.strip()
    if not said or "?" in said:
        return ""
    match = THEIR_LENGTH.fullmatch(said)
    if not match:
        return ""
    unit = (match.group("unit") or "years").lower()
    relation, job = _the_person_holding_a_job(memory, match.group("who").lower())
    if not relation:
        return ""
    doing = (match.group("doing") or "").strip()
    doing = re.sub(r"^(?:a|an|the)\s+", "", doing, flags=re.I)
    named = not re.fullmatch(r"(?:doing\s+)?(?:it|that|this|the\s+job)", doing or "", re.I)
    if named and not _alike(doing, job):
        return ""
    count = _the_count(match.group("count"))
    months = unit.startswith(("month", "mnth"))
    if not count and (match.group("count") or "").lower() not in ("years",):
        return ""
    return _their_stint(relation, job, count, memory, said, "months" if months else "years")
