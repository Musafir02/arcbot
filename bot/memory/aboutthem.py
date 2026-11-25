import datetime
import re

from . import topics
from .facts import HE, SHE

PRONOUN = re.compile(r"\b(?P<own>his|her|their)\s+(?P<thing>[a-z][a-z' -]{0,20})"
                     r"|\b(?P<who>he|she|they)\b"
                     r"|\b(?P<obj>him|her|them)\b", re.I)

THEIR_AGE = re.compile(r"\bhow\s+old\b|\bwhat\s+age\b|\bhow\s+big\b|\btheir\s+age\b|\bhis\s+age\b"
                       r"|\bher\s+age\b", re.I)

ASKS = re.compile(r"\bhow\s+(?:much|many|long|often|early|late)\b|\bwhat\s+time\b"
                  r"|\bwhen\s+(?:is|are|do|does|will|can)\b", re.I)

GIVEN = re.compile(r"\b\d{1,3}\b|\ba\s+(?:one|two|three|four|five|six|seven|eight|nine|ten|"
                   r"eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen)\b", re.I)

CHILD_AGE = 18

BABY_MONTHS = 24
SPOKEN = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight",
          9: "nine", 10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen",
          15: "fifteen", 16: "sixteen", 17: "seventeen"}


def _the_child(text, memory):
    said = str(text or "")
    if not said or not isinstance(memory, dict):
        return None, ""
    if THEIR_AGE.search(said) or GIVEN.search(said) or not ASKS.search(said):
        return None, ""
    if "?" not in said and not topics._leads_a_question(said):
        return None, ""
    found = PRONOUN.search(said)
    if not found:
        return None, ""
    word = (found.group("who") or found.group("own") or found.group("obj") or "").lower()
    if word == "she" or word == "her":
        fits = SHE
    elif word == "he" or word == "his":
        fits = HE
    else:
        fits = SHE | HE
    for entry in _people(memory):
        who = str(entry.get("who") or "").strip().lower()
        if not who or who not in fits:
            continue
        months = entry.get("months")
        if isinstance(months, int) and 0 < months < BABY_MONTHS:
            return "%s month old" % SPOKEN.get(months, str(months)), who
        age = entry.get("age")
        if isinstance(age, int) and 0 < age < CHILD_AGE:
            return "%s year old" % SPOKEN.get(age, str(age)), who
    return None, ""


def _people(memory):
    found = []
    person = memory.get("person")
    if isinstance(person, dict) and person.get("who") and (
            person.get("age") is not None or person.get("months") is not None):
        found.append(person)
    for entry in memory.get("others") or ():
        if isinstance(entry, dict):
            found.append(entry)
    return found


def with_the_age(text, memory):
    how_old, _who = _the_child(text, memory)
    if not how_old:
        return ""
    said = str(text)
    found = PRONOUN.search(said)
    if not found:
        return ""
    if found.group("own"):
        thing = found.group("thing").strip()
        written = said[:found.start()] + "a %s's %s" % (how_old, thing) + said[found.end():]
    else:
        written = said[:found.start()] + "a " + how_old + said[found.end():]
    written = " ".join(written.split())
    return written if written != said else ""

AHEAD_ASK = re.compile(r"\b(?:how\s+old|what\s+age)\s+(?:will|would|is|does)\b", re.I)
AHEAD_TIME = re.compile(
    r"\bnext\s+(?P<next>year|summer|birthday)\b"
    r"|\bthis\s+time\s+next\s+year\b"
    r"|\bin\s+(?P<years>\d{1,2}|a|one|two|three|four|five|six|seven|eight|nine|ten)\s+years?\b"
    r"|\bin\s+(?P<year>(?:19|20)\d\d)\b", re.I)
COUNT = {word: number for number, word in enumerate(
    ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
     "eleven", "twelve"), 0)}
KIN = re.compile(r"\bmy\s+(?:little\s+|big\s+|eldest\s+|youngest\s+)?"
                 r"(?P<who>son|daughter|boy|girl|child|kid|lad|little one)\b", re.I)

KIN_SAME = {"son": ("son", "boy"), "boy": ("boy", "son"), "lad": ("lad", "boy", "son"),
            "daughter": ("daughter", "girl"), "girl": ("girl", "daughter"),
            "child": ("child", "kid", "son", "daughter", "boy", "girl"),
            "kid": ("kid", "child", "son", "daughter", "boy", "girl"),
            "little one": ("little one", "child", "kid", "son", "daughter", "boy", "girl")}


def an_age_ahead(text, memory):
    said = " ".join(str(text or "").split())
    if not said or not AHEAD_ASK.search(said):
        return None
    when = AHEAD_TIME.search(said)
    if not when:
        return None
    age, words = _the_one_asked_about(said, memory)
    if age is None:
        return None
    years = _the_years_ahead(when)
    if years is None or years < 0:
        return None
    day = _the_day_named(when, years)
    if not day:
        return None
    subject = _the_subject(words)
    verb = (" " if words.startswith("your ") else "") + _the_future(words)
    return "%s%s %s %s." % (subject, verb, _an_age_said(age + years), day)


def _the_years_ahead(when):
    if when.group("next"):
        return 1 if when.group("next").lower() == "year" else None
    if when.group("year"):
        try:
            return int(when.group("year")) - datetime.date.today().year
        except (TypeError, ValueError):
            return None
    count = when.group("years")
    if not count:
        return None
    return int(count) if count.isdigit() else COUNT.get(count.lower())


def _the_day_named(when, years):
    if years == 0:
        return "now" if not when.group("year") else "in %s" % when.group("year")
    if when.group("year"):
        return "in %s" % when.group("year")
    if years == 1:
        return "next year"
    return "in %s years" % SPOKEN.get(years, str(years))


def _the_one_asked_about(said, memory):
    if not isinstance(memory, dict):
        return None, ""
    people = _people(memory)
    named = KIN.search(said)
    if named:
        who_said = named.group("who").lower()
        fits = KIN_SAME.get(who_said, (who_said,))
        for entry in people:
            who = str(entry.get("who") or "").strip().lower()
            if not who or who not in fits:
                continue
            age = entry.get("age")
            if isinstance(age, int) and 0 < age < CHILD_AGE:
                return age, "your " + who_said
        return None, ""
    found = PRONOUN.search(said)
    if not found:
        return None, ""
    word = (found.group("who") or found.group("own") or found.group("obj") or "").lower()
    if word in ("she", "her"):
        fits, said_who = SHE, "she"
    elif word in ("he", "his", "him"):
        fits, said_who = HE, "he"
    else:
        fits, said_who = SHE | HE, "they"
    for entry in people:
        who = str(entry.get("who") or "").strip().lower()
        if not who or who not in fits:
            continue
        age = entry.get("age")
        if isinstance(age, int) and 0 < age < CHILD_AGE:
            return age, said_who
    return None, ""


def _an_age_said(age):
    if isinstance(age, int) and 0 < age <= 12:
        return SPOKEN.get(age, str(age))
    return str(age)


def _the_subject(words):
    words = (words or "").strip()
    return words[:1].upper() + words[1:] if words else "They"


def _the_future(words):
    return "will be" if (words or "").startswith("your ") else "'ll be"
