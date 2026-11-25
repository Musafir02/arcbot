
import re

_AM = r"(?:i\s*m|im|iam|i\s+am)"
_ARE = r"(?:we\s*'?\s*re|we\s+are)"

_TONE = re.compile(
    r"(?:\s+(?:tbh|tho|though|now|anyway|actually|really|literally|honestly|i\s+suppose|"
    r"i\s+guess|still|also|too|by\s+the\s+way|btw|atm|at\s+the\s+moment|lol|ha|haha|"
    r"lmao|so\s+yeah|yeah|innit|mate|dude))+$")

_SITUATIONS = (
    ("tenant", re.compile(
        rf"^(?:{_AM}|{_ARE})\s+(?:a\s+|an\s+)?(?:private\s+|council\s+|housing\s+association\s+)?"
        r"(?:tenant|tenants|renter|renters|lodger|lodgers)$"
        r"|^(?:i|we)\s+rent(?:ing)?(?:\s+(?:a|an|my|our|the)\s+"
        r"(?:flat|house|home|place|bungalow|room|council\s+flat|housing\s+association\s+flat))?$"
        r"|^(?:i|we)\s+pay\s+rent$"), (
        "Good to know - renting decides who has to act when something in the place goes wrong. "
        "What's on your mind?",
        "Right, so you rent. What are you trying to sort out?",
        "Renting, noted. What would you like a hand with?",
    )),
    ("carer", re.compile(
        r"^(?:i\s*m|im|iam|i\s+am)\s+(?:a\s+|an\s+)?(?:unpaid\s+|full[- ]time\s+|part[- ]time\s+|"
        r"young\s+|family\s+)?carer$"
        r"|^(?:i\s*m|im|iam|i\s+am)\s+(?:a\s+)?carer\s+for\s+(?:a\s+)?"
        r"(?:relative|someone|somebody|family)$"), (
        "Carers carry a lot that nobody gets to see. Is it help for you you're after, or "
        "something for the person you look after?",
        "Good to know. What would help most - something for you, or something for them?",
        "Caring is a job with no clocking off. What's the hard bit at the moment?",
    )),
    ("single_parent", re.compile(
        rf"^(?:{_AM})\s+(?:a\s+|an\s+)?(?:single|lone|solo)\s+"
        r"(?:parent|mum|mom|dad|mother|father|mam)$"), (
        "One pair of hands for all of it. What's the part that's hardest at the moment?",
        "Good to know - that's a lot to hold on your own. What are you trying to sort out?",
        "Right. What would help most this week?",
    )),
    ("student", re.compile(
        rf"^(?:{_AM})\s+(?:a\s+|an\s+)?(?:(?:mature|full[- ]time|part[- ]time|postgrad|"
        r"phd|undergrad|university|uni|college)\s+)*student$"), (
        "Student, then. What are you trying to work out?",
        "Good to know. What's the thing on your mind?",
        "Student life - what would help?",
    )),
    ("owner", re.compile(
        rf"^(?:{_AM})\s+(?:a\s+|an\s+)?home\s*owner$"
        r"|^(?:i|we)\s+own\s+(?:my|our|the)\s+(?:house|flat|home|place)$"
        r"|^(?:i|we)\s+own\s+(?:it|mine|ours)$"), (
        "Good to know - owning it means the repairs are yours to arrange. What's on your mind?",
        "So it's your own place. What are you trying to sort out?",
        "Home owner, noted. What would you like a hand with?",
    )),
    ("self_employed", re.compile(
        rf"^(?:{_AM})\s+(?:a\s+)?self[- ]?employed$"
        r"|^(?:i|we)\s+work\s+for\s+(?:myself|ourselves)$"
        rf"|^(?:{_AM})\s+(?:a\s+)?(?:freelancer|contractor|sole\s+trader)$"), (
        "Self-employed, so no payroll to fall back on and nobody to ask upstairs. What are you "
        "trying to sort out?",
        "Working for yourself, then. What's on your mind?",
        "Good to know. What would help most?",
    )),
    ("benefits", re.compile(
        rf"^(?:{_AM}|{_ARE})\s+on\s+(?:benefits|universal\s+credit|uc|tax\s+credits|"
        r"pip|esa|jsa|income\s+support|housing\s+benefit)$"), (
        "Good to know - the rules on that are worth checking before you decide anything. What "
        "are you trying to work out?",
        "Right. What are you trying to sort out?",
        "Noted. What's the thing you need a hand with?",
    )),
    ("disabled", re.compile(
        rf"^(?:{_AM})\s+(?:disabled|a\s+disabled\s+person)$"
        r"|^(?:i|we)\s+have\s+(?:a\s+)?disabilit(?:y|ies)$"
        rf"|^(?:{_AM})\s+(?:registered\s+)?(?:blind|deaf|partially\s+sighted)$"), (
        "Good to know, and I won't assume what it means for you. What do you need a hand with?",
        "Thanks for telling me - it's useful to know rather than guess. What would help most?",
        "Right, noted. What's on your mind?",
    )),
    ("separated", re.compile(
        rf"^(?:{_AM})\s+(?:divorced|separated|a\s+divorcee|newly\s+single|recently\s+single)$"
        r"|^(?:i|we)\s+got\s+divorced$"), (
        "Right - that's a lot to carry, and a pile of admin along with it. What needs sorting "
        "first?",
        "Good to know. What's on your mind about it?",
        "Noted. What would you like a hand with?",
    )),
)

_POOLS = {kind: lines for kind, _pattern, lines in _SITUATIONS}


def _line(clean):
    said = str(clean or "").replace("\u2019", "'").strip().lower()
    said = said.strip(" .,!;:-\"'")
    said = re.sub(r"\s+", " ", said)
    while True:
        trimmed = _TONE.sub("", said)
        if trimmed == said:
            return said
        said = trimmed


def reads_as_situation(clean):
    said = _line(clean)
    if not said or "?" in said:
        return None
    for kind, pattern, _lines in _SITUATIONS:
        if pattern.match(said):
            return kind
    return None


def pool(clean):
    kind = reads_as_situation(clean)
    if not kind:
        return None
    return _POOLS[kind]
