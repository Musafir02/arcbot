import re

from . import measure

WORK_CHECK = re.compile(
    r"^(?:(?:and|but|so|ok(?:ay)?|right|oh|hmm|well|then)[, ]+)*"
    r"(?:will|would|does|do|might|should|can)\s+(?:that|it|this|they|those)\s+"
    r"(?:work|help|do\s+(?:it|the\s+job)|fix\s+(?:it|that)|be\s+(?:enough|ok|okay|all\s+right|"
    r"alright|fine)|make\s+a\s+difference)"
    r"(?:\s+(?:for|on)\s+(?:me|us|him|her|them|this|that))?"
    r"(?:\s+(?:then|though|now|too))?\s*$", re.I)

ACHIEVES = re.compile(
    r"\b(?:almost nothing|nothing needs|nothing to scrub|does the job|does the trick|"
    r"catches|clears|lifts|comes away|comes off|gets rid of|no more|beats|kills|sinks|"
    r"survives|stops?|fixes|sorts|dries|settles|holds|works|helps?|lets (?:her|him|them|you)|"
    r"keeps (?:them|it) (?:off|away|out))\b", re.I)

NOT_ACHIEVING = re.compile(
    r"\b(?:does nothing|nothing except|does not|doesn't|dont|don't|never|won't|wont|"
    r"isn't|is not|not\s+enough|makes it worse)\b", re.I)

JOINS_ON = frozenset(("which", "that", "who", "and", "but", "so", "then", "because", "though",
                      "while", "as", "if", "when", "also"))

YES_IN_FRONT = ("Yes", "It does", "That does it", "Yes, it does")

THE_MOST_QUOTED = 11
TRAILING_FILLER = ("too", "as well", "also", "then", "though")

A_NEW_CLAUSE = frozenset("""and so but or which is are was were then because when if that
it they there this these with plus while as""".split())
SENTENCE = re.compile(r"(?<=[.!?])\s+")


def asks_if_it_will_work(line):
    text = " ".join(str(line or "").split()).strip(" ?.!,")
    return bool(text) and bool(WORK_CHECK.match(text))


def _the_clauses(sentence):
    parts = re.split(r"[,;:]\s+|\s+-\s+", str(sentence))
    return [part.strip(" .") for part in parts if part.strip(" .")]


def _without_filler(clause):
    said = clause.strip(" .")
    for filler in TRAILING_FILLER:
        if said.lower().endswith(" " + filler):
            said = said[: -len(filler) - 1].rstrip(" ,.")
    return said


def _what_it_achieves(card):
    for sentence in reversed([part.strip() for part in SENTENCE.split(str(card)) if part.strip()]):
        if not ACHIEVES.search(sentence) or NOT_ACHIEVING.search(sentence):
            continue
        for clause in _the_clauses(sentence):
            if not ACHIEVES.search(clause) or NOT_ACHIEVING.search(clause):
                continue
            if (re.split(r"\s+", clause) or [""])[0].lower().strip(",.;:") in JOINS_ON:
                continue
            clause = _without_filler(clause)
            if 4 <= len(clause.split()) <= THE_MOST_QUOTED:
                return clause
    return ""


def reply_for(text, memory):
    if not asks_if_it_will_work(text):
        return None
    card = measure._the_card_said_last(memory)
    if not card:
        return None
    said = _what_it_achieves(card)
    if not said:
        return None
    if str(said).lstrip().lower().startswith(("yes", "no")):
        return None
    if said[:1].isupper() and (said[1:2].islower() or (said[1:2] == " " and said[2:3].islower())):
        said = said[0].lower() + said[1:]
    said = said.rstrip(" .")
    at = sum(ord(letter) for letter in str(text or "")) % len(YES_IN_FRONT)
    return "%s \u2014 %s." % (YES_IN_FRONT[at], said)
