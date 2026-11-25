import re

from ..memory import narrow

WHEN_ASK = re.compile(
    r"^\W*(?:(?:and|so|but|ok|okay|oh|ah|right|well|yes|yeah|hi|hey|please|then|now|quick"
    r"|sorry|also)\W+)*"
    r"(?:when|what\s+time|what\s+day|which\s+day|what\s+date|which\s+date)\s+"
    r"(?:is|are|was|were|do|does|did|will|shall|have|has|am)\b", re.I)

HOW_TO_MOMENT = re.compile(
    r"\b(?:best|good|right|ideal|worst)\s+time\b|\btime\s+to\s+"
    r"(?:plant|sow|prune|book|go|start|take|give|use|apply|cut|paint|ring)\b", re.I)

A_MONTH = re.compile(
    r"\b(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?"
    r"|aug(?:ust)?|sep(?:t|tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\b", re.I)
A_CLOCK = re.compile(
    r"\b(?:at|by|around|about|from|until|till)\s+\d{1,2}(?::\d{2})?\s*"
    r"(?:am|pm|a\.m|p\.m|o'?clock)?\b", re.I)

MOST_WORDS = 45


def asks_for_a_when(text):
    if HOW_TO_MOMENT.search(text or ""):
        return False
    return bool(WHEN_ASK.search(text or ""))


def holds_a_date(text):
    said = text or ""
    return bool(narrow.has_a_date(said) or A_CLOCK.search(said))


DATE_TOKEN = re.compile(
    r"\b(?:mon|tues?|wed(?:nes)?|thur?s?|fri|sat(?:ur)?|sun(?:day)?)(?:day)?\b"
    r"|\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\b"
    r"|\b\d{1,2}(?:st|nd|rd|th)\b"
    r"|\b\d{1,2}(?::\d{2})?\s*(?:am|pm|a\.m|p\.m|o'?clock)\b"
    r"|\b(?:19|20)\d{2}\b", re.I)


def _date_words(text):
    return {word.lower().rstrip(".") for word in DATE_TOKEN.findall(text or "")}


def the_same_date(one, two):
    first = _date_words(one)
    return bool(first and first & _date_words(two))


def the_fact_asked_for(text, reply):
    if not asks_for_a_when(text):
        return False
    if len((reply or "").split()) > MOST_WORDS:
        return False
    return holds_a_date(reply)
