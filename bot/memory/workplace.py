import re

from ..compose import pick

I_WORK = re.compile(
    r"^\s*(?:so|and|oh|well|ok|okay|right|actually|anyway|hi|hey|hello)?[\s,]*"
    r"\b(?:i|i'?m)\s+(?:still\s+|now\s+)?(?:work|working)\s+"
    r"(?P<rest>[^.!?]{2,60})", re.I)
NOT_MINE = re.compile(
    r"\b(?:(?:she|he|they|we|his|her|their|our|my)\b[^.!?]{0,20}?"
    r"(?:works|worked|working)|(?:they|we)\s+work)\b", re.I)
A_QUESTION = re.compile(
    r"^\s*(?:how|what|where|why|when|who|which|can|could|should|do|does|did|is|are|will"
    r"|would|any)\b", re.I)
NOT_A_PLACE = re.compile(
    r"^\s*(?:as|with|too|so|hard|late|early|flat|out|up|nights?|night\s+shifts?|shifts"
    r"|evenings?|weekends?|part[- ]time|full[- ]time|long\s+hours|all\s+hours|away|abroad"
    r"|remotely|on\s+my\s+own|for\s+myself|for\s+a\s+living|in\s+a\s+team|from\s+home\s+now)\b",
    re.I)
A_PLACE = re.compile(
    r"^\s*(?P<prep>in|at|for|from)\s+(?P<place>[a-z0-9][a-z0-9' \u2019,&/.-]{1,40})", re.I)
WITH_THE_DETAIL = re.compile(
    r"\b(?:shift|shifts|nights?|hours?|overtime|weekends?|all\s+day|all\s+week|every\s+day"
    r"|part[- ]time|full[- ]time|long\s+days|on\s+call)\b|\d", re.I)

USED_TO = re.compile(r"\b(?:used\s+to|use\s+to|stopped|quit|left)\b", re.I)

_TAILS = (
    "how long have you been there?",
    "what's the best part of the week there?",
    "does it leave you much time for yourself?",
    "busy one, I should think.",
    "what do you do there?",
)
_FROM_HOME_TAILS = (
    "how do you keep the day from running into the evening?",
    "the commute is hard to beat.",
    "quiet, or people at the door all day?",
    "what's the best part of it?",
    "does it give you more of the day back?",
)


A_SHIFT_NOT_A_TRADE = re.compile(
    r"^(?:nights?|days?|evenings?|weekends?|shifts?|lates?|early|mornings?|afternoons?"
    r"|part[- ]time|full[- ]time|hours|overtime|on\s+call|long\s+hours)$", re.I)


def _the_same_line(a, b):
    def clean(said):
        return re.sub(r"[^a-z0-9 ]+", " ", str(said or "").lower()).split()
    return clean(a) == clean(b)


def _the_job_the_chat_holds(memory, text=""):
    entries = (memory or {}).get("facts_log") if isinstance(memory, dict) else None
    if isinstance(entries, list):
        for entry in reversed(entries):
            if not isinstance(entry, dict) or entry.get("key") != "job":
                continue
            if not entry.get("value"):
                continue
            if text and _the_same_line(entry.get("text"), text):
                continue
            if A_SHIFT_NOT_A_TRADE.match(str(entry["value"]).strip()):
                continue
            return str(entry["value"]).strip()
        return ""
    user = (memory or {}).get("user") if isinstance(memory, dict) else None
    job = user.get("job") if isinstance(user, dict) else ""
    return str(job or "").strip()


def _with_an_article(job):
    word = str(job or "").strip()
    if not word:
        return ""
    article = "an" if word[:1].lower() in "aeiou" else "a"
    return article + " " + word


def _a_clean_place(place):
    word = re.split(r"\b(?:and|but|because|so|when|while|although|though|which|where|if)\b",
                    str(place or ""), maxsplit=1)[0]
    word = re.sub(r"[\s,.;:!?'\u2019]+$", "", word.strip())
    word = re.sub(r"\s+(?:anyway|now|though|too|still)$", "", word, flags=re.I)
    words = word.split()
    if len(words) > 5:
        word = " ".join(words[:5])
    return word.strip()


def _the_place_the_line_said(text):
    said = str(text or "").strip()
    if not said or not I_WORK.search(said):
        return None
    if A_QUESTION.match(said) or said.endswith("?") or USED_TO.search(said):
        return None
    if NOT_MINE.search(said):
        return None
    found = I_WORK.search(said)
    rest = found.group("rest").strip()
    if not rest or NOT_A_PLACE.match(rest):
        return None
    place = A_PLACE.match(rest)
    if not place or WITH_THE_DETAIL.search(place.group("place")):
        return None
    clean = _a_clean_place(place.group("place"))
    if len(clean) < 3:
        return None
    tail = rest[place.end():].strip(" ,.;:!?'\u2019")
    if len(tail.split()) > 3:
        return None
    return place.group("prep").lower(), clean


def the_place_the_person_works(text, memory):
    found = _the_place_the_line_said(text)
    if not found:
        return None
    job = _the_job_the_chat_holds(memory, text)
    if not job:
        return None
    prep, place = found
    home = prep == "from" or place.lower() in ("home", "the house")
    if home:
        return (_with_an_article(job).capitalize() + " working from home - "
                + pick(_FROM_HOME_TAILS, memory, text))
    where = prep + " " + place
    return (_with_an_article(job).capitalize() + " " + where + " - "
            + pick(_TAILS, memory, text))
