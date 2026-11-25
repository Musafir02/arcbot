import re

from ..memory import lineback

PRIORITY = 7060

_A_THIRD_PARTY_ASK = re.compile(
    r"\bwhat\s+did\s+(?:they|he|she|them|it|the\s+[a-z]+"
    r"|(?!(?:i|we|you|my|our)\b)[a-z]+)\s+"
    r"(?:say|said|tell\s+(?:you|me)|told\s+(?:you|me)|quote|quoted|charge|charged|offer"
    r"|offered|reckon|reckoned|suggest|suggested|text|texted|come\s+back\s+with|wants?)\b"
    r"|\bwhat\s+(?:did|have|has)\s+(?:they|he|she)\s+(?:said|told\s+(?:you|me))\b"
    r"|\bremind\s+me\s+what\s+(?:they|he|she)\s+(?:said|say|told\s+you|quoted|wanted)\b",
    re.I)

_NOT_A_DETAIL = frozenset("""
what which who whom whose when where why how say said saying says tell told telling mention
mentioned quote quoted quotes charge charged offer offered reckon suggested text texted remind
me my our we us i you your it its that this these those was were is are be been being did do does
done about of to the a an and or for with in on at by as if so but not any some please just really
thing things one ones kind sort name called exact exactly already again
they them their theirs he him his she her hers
would could should shall will may might must can cant cannot itll id
""".split())

_A_KIND = {
    "cost": "figure", "costs": "figure", "price": "figure", "quote": "figure",
    "quoted": "figure", "charge": "figure", "charged": "figure", "offer": "figure",
    "offered": "figure", "pay": "figure", "paid": "figure", "much": "figure", "many": "figure",
    "number": "figure",
}

_SOMEBODY_SPOKE = re.compile(
    r"\b(?!i\b|we\b)(?:they|he|she|the\s+[a-z]+|[a-z]+)\s+"
    r"(?:said|says|say|told|tells|quoted|asked|charges?|offer(?:s|ed)?|reckons|thinks|texted|called"
    r"|wants)\b", re.I)

_A_FIGURE = re.compile(
    r"(?:£|\$|€)\s?\d[\d,.]*\s?(?:k\b|m\b)?"
    r"|\b\d[\d,.]*\s?(?:k\b|grand\b|thousand\b|quid\b|pounds?\b|p\b)"
    r"|\b\d[\d,.]*\b", re.I)

_QUESTION = re.compile(r"^\s*(?:what|which|who|when|where|why|how|should|shall|can|could|would"
                       r"|do|does|did|is|are|was|were|will|have|has|am)\b", re.I)

_REPORTING_VERB = re.compile(
    r"\b(?P<who>(?:[a-z]+\s+)?[a-z]+)\s+"
    r"(?:said|says|telling\s+me|told\s+me|tells\s+me|reckoned|texted|quoted|charged|offered"
    r"|asked|wants|wanted|asks|needs|went)\b\s+(?:that\s+)?"
    r"(.+)$", re.I)

_THE_PERSON = frozenset(("i", "we", "me", "us", "im", "ive", "id"))

_A_MONEY = re.compile(r"[£$€]|\b\d[\d,.]*\s?(?:k|m|grand|thousand|quid|pounds?|p)\b", re.I)
_A_UNIT_AFTER = re.compile(
    r"^\s*(?:years?|yrs?|months?|weeks?|days?|hours?|hrs?|minutes?|mins?|miles?|km|kilometres?"
    r"|kilograms?|kg|stone|feet|foot|inches|times?|percent|%|o'?clock)\b", re.I)


def _details(text):
    return {word.strip("'") for word in re.findall(r"[a-z']+", str(text or "").lower())
            if word.strip("'") not in _NOT_A_DETAIL and len(word.strip("'")) > 1}


def _the_kind_of_answer(said):
    for word in re.findall(r"[a-z']+", str(said or "").lower()):
        kind = _A_KIND.get(word.strip("'"))
        if kind:
            return kind
    return ""


def _the_last_somebody_spoke(said, memory):
    wanted = _details(said)
    kind = _the_kind_of_answer(said)
    for line in reversed(lineback.the_lines(memory)):
        if _QUESTION.search(line) or lineback.is_a_recall_ask(line):
            continue
        if not _SOMEBODY_SPOKE.search(line):
            continue
        if kind or not wanted or (wanted & _details(line)):
            return line
    return None


def _the_reported_clause(line):
    clause = ""
    for match in _REPORTING_VERB.finditer(line):
        who = match.group("who").split()[-1].strip("',")
        if who in _THE_PERSON:
            continue
        clause = match.group(2).strip()
    clause = clause.rstrip(" .!?,")
    clause = re.sub(r"^(?:for|to|about|of|at)\s+(?=(?:£|\$|€)?\s?\d)", "", clause, flags=re.I)
    words = clause.split()
    if not words or len(words) > 14:
        return ""
    if _QUESTION.search(clause) or not re.search(r"[a-z0-9]", clause, re.I):
        return ""
    return clause


def _the_figure_the_line_gave(line):
    figures = [found for found in _A_FIGURE.finditer(line)
               if not _A_UNIT_AFTER.match(line[found.end():])]
    money = [found for found in figures if _A_MONEY.search(found.group(0))]
    if len(money) == 1:
        return money[0].group(0).strip()
    if not money and len(figures) == 1:
        return figures[0].group(0).strip()
    return ""


def respond(text, memory):
    said = lineback.flat(text)
    if not said or not _A_THIRD_PARTY_ASK.search(said):
        return None
    line = _the_last_somebody_spoke(said, memory)
    if not line:
        return None
    if _the_kind_of_answer(said) == "figure":
        figure = _the_figure_the_line_gave(line)
        if figure:
            return "You said " + figure + "."
    clause = _the_reported_clause(line)
    if clause:
        return "You said " + clause + "."
    return None
