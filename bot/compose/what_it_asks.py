import re

from bot.compose.fit import AMOUNT, OPTIONS, PICK

MONEY_VERB_ASK = re.compile(
    r"\bwhat should (?:i|we) (?:tip\b|spend (?:on)(?! it)\b|budget for\b|"
    r"pay (?:for|a|an|my|the|him|her|them)\b)", re.I)
SPEND_IT_ON = re.compile(
    r"\bwhat (?:should|shall|do) (?:i|we) (?:spend|put) it (?:on|into|in)\b", re.I)
PRESENT_LOOKING = re.compile(r"\b(?:present|gift|pressie)s?\b[^?.!]{0,20}?\bfor\b", re.I)
NOT_A_PRESENT_ASK = re.compile(
    r"\b(?:thank(?:s| you)|refund|receipt|return(?:ed|ing)?|"
    r"buying|bought|got|gave|given|giving|keeps)\b", re.I)
ALTERNATIVES = re.compile(r"\bor\b", re.I)


def _names_alternatives(line, match):
    window = line[max(0, match.start() - 80):match.end() + 80]
    seat = match.start() - max(0, match.start() - 80)
    spent = 0
    for part in re.split(r"[,;:?.!]", window):
        if spent <= seat <= spent + len(part):
            return bool(ALTERNATIVES.search(part))
        spent += len(part) + 1
    return bool(ALTERNATIVES.search(window))


def _the_line_once(understood):
    for key in ("plain", "text", "clean"):
        value = understood.get(key)
        if isinstance(value, str) and value.strip():
            return " ".join(value.lower().replace("\u2019", "'").split())
    return ""


def the_shape_it_asks(understood, want):
    if not isinstance(understood, dict):
        return want
    line = _the_line_once(understood)
    if not line:
        return want
    if SPEND_IT_ON.search(line):
        return PICK
    money = MONEY_VERB_ASK.search(line)
    if money and not _names_alternatives(line, money):
        return AMOUNT
    if want is None and PRESENT_LOOKING.search(line) and not NOT_A_PRESENT_ASK.search(line):
        return OPTIONS
    return want
