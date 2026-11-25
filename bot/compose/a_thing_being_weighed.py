import re

from . import pick

RECEIPTS = (
    "got it. is there anything you'd like a hand with?",
    "thanks for telling me \u2014 i'm here if you want to dig into any of that.",
    "i'm listening \u2014 say more if it helps.",
)

_WEIGHING = (r"(?:looking at|looking into|thinking about|thinking of|considering|weighing up|"
             r"deciding on|deciding between|going for|applying for|trying for|after)")
_WEIGH = re.compile(
    r"^\s*(?:so|and|but|ok|okay|well|oh|right)?\s*"
    r"(?:(?:i'?m|im|i am|we'?re|we are|she'?s|he'?s|they'?re|my (?:wife|husband|partner|mum|dad|"
    r"son|daughter|friend))\s+)?"
    r"(?:still\s+|also\s+|just\s+|now\s+|actually\s+)?"
    + _WEIGHING + r"\s+(?P<thing>[a-z0-9' -]{3,45}?)\s*$")
_DECIDING = re.compile(
    r"\b(?:deciding|torn|choosing|stuck) (?:between|over)\s+(?:a|an|two|three|some|the)?\s*"
    r"(?P<thing>[a-z0-9' -]{3,45}?)\s*$")
_LOOKING_FOR = re.compile(
    r"\b(?:looking for|shopping for|hunting for|asking about|going to see|getting a quote for|"
    r"getting quotes for)\s+(?:a|an|some|a new|new|some new)\s+(?P<thing>[a-z0-9' -]{3,45}?)\s*$")
_ITS_FOR = re.compile(
    r"^\s*(?:and\s+|oh\s+|well\s+)?(?:it'?s|its|they'?re|the one i want is)\s+"
    r"(?:for|to be for)\s+(?:a|an|the|our|my|some)\s+(?P<thing>[a-z0-9' -]{3,45}?)\s*$"
    r"|^\s*(?:and\s+|oh\s+|well\s+)?(?:it'?s|its)\s+(?:a|an)\s+(?P<bare>[a-z0-9' -]{3,45}?)\s*$")

KINDS = {
    "job": ("job", "role", "position", "interview", "apprenticeship", "placement", "internship",
            "secondment", "promotion", "shift"),
    "event": ("wedding", "venue", "party", "birthday", "funeral", "christening", "anniversary",
              "reception", "celebration", "gathering", "conference", "shower", "bash"),
    "bought": ("boiler", "blanket", "car", "van", "bike", "bicycle", "laptop", "computer",
               "phone", "mobile", "tablet", "mattress", "sofa", "settee", "chair", "table",
               "desk", "pram", "pushchair", "cot", "seat", "washer", "machine", "fridge",
               "freezer", "oven", "cooker", "dishwasher", "dryer", "vacuum", "hoover", "kettle",
               "tv", "television", "monitor", "printer", "watch", "coat", "jacket", "boots",
               "boot", "tent", "caravan", "scooter", "mower", "lawnmower", "trimmer",
               "dehumidifier", "fryer", "microwave", "radiator", "pump", "panel", "burner"),
}
_KIND_OF = {}
for _kind, _words in KINDS.items():
    for _word in _words:
        _KIND_OF[_word] = _kind
        _KIND_OF[_word + "s"] = _kind

NOT_A_DECISION = re.compile(
    r"\b(?:pain|ache|hurts?|hurting|blood|bleeding|lump|rash|doctor|gp|nurse|hospital|surgery|"
    r"symptom|dose|doses|tablet|tablets|antibiotic|prescription|period|pregnant|pregnancy|"
    r"rent|rent arrears|evict\w*|deposit|landlord|council tax|benefits?|universal credit|"
    r"salary|wage|wages|payslip|court|solicitor|police|dead|died|dying|divorce|"
    r"my (?:mum|dad|son|daughter|husband|wife|partner|friend|brother|sister|baby))\b")

ASKS = re.compile(r"^\s*(?:so|but|and|ok|okay)?\s*(?:what|which|how|when|where|who|why|is|are|"
                  r"was|were|do|does|did|can|could|should|would|will|shall|am)\b")

_OPENERS = ("a", "an", "the", "some", "my", "our", "a new", "new", "some new", "your", "his",
            "her", "their", "any")

_VOWELS = frozenset("aeiou")


def _plain(text):
    return re.sub(r"\s+", " ", str(text or "").lower().replace("\u2019", "'")).strip()


def _bare(phrase):
    said = _plain(phrase).strip(" .,!?-")
    for opener in sorted(_OPENERS, key=len, reverse=True):
        if said.startswith(opener + " "):
            said = said[len(opener) + 1:]
            break
    return said.strip(" .,!-")


_A_NOT_AN = ("used", "unused", "useful", "one", "once", "usual", "uniform", "university", "euro",
             "european", "ubiquitous")


def _as_said(name, head):
    first = name.split()[0] if name.split() else ""
    if first in ("an", "a") or first.isdigit() or first in _POSSESSIVE:
        return name
    if first in ("the", "some", "any"):
        name = " ".join(name.split()[1:])
        first = name.split()[0] if name.split() else ""
        if not name:
            return ""
    if first.isdigit() or first in _POSSESSIVE or _is_plural(head):
        return name
    return _with_article(name)


def _with_article(phrase):
    said = _bare(phrase)
    if not said or said[0].isdigit() or _is_plural(said.split()[-1]):
        return said
    if said.split()[0] in _A_NOT_AN:
        return "a " + said
    if _is_plural(said.split()[0]) and len(said.split()) == 1:
        return said
    return ("an " if said[0] in _VOWELS else "a ") + said


_CUTS_HEAD = ("i think", "i reckon", "i suppose", "apparently", "though", "actually", "maybe",
              "probably", "instead", "than", "from", "on", "at", "in", "with", "about", "to",
              "and", "or", "for", "this week", "this weekend", "next week", "next month",
              "for now")
_CUTS_NAME = ("i think", "i reckon", "i suppose", "apparently", "though", "than i", "and",
              "or", "this week", "this weekend", "next week", "next month", "for now")
_ALREADY_HAVE = re.compile(r"\b(?:my|our|mine|your|their)\b")
_POSSESSIVE = ("my", "our", "mine", "your", "their", "his", "her", "its")
_ARTICLES = ("a", "an", "the", "some", "any")


def _is_plural(word):
    return word.endswith("s") and not word.endswith("ss")


def _cut_at(said, cuts):
    low = " " + said + " "
    at = len(said)
    for word in cuts:
        found = low.find(" " + word + " ")
        if -1 < found < at:
            at = found
    return said if at >= len(said) else said[:at].strip()


def _head_and_name(thing):
    raw = _plain(thing).strip(" .,!?-")
    said = _bare(raw)
    if not said:
        return "", "", ""
    head_part = _cut_at(said, _CUTS_HEAD)
    head = head_part.split()[-1].strip(".,!?-").lower() if head_part.split() else ""
    return head, _cut_at(raw, _CUTS_NAME), head_part


def _read(said):
    if not said or ASKS.match(said) or NOT_A_DECISION.search(said):
        return None, None
    thing = None
    match = _WEIGH.search(said) or _DECIDING.search(said)
    if match:
        thing = match.group("thing")
    else:
        match = _LOOKING_FOR.search(said)
        if match:
            thing = match.group("thing")
        else:
            match = _ITS_FOR.search(said)
            if match:
                thing = match.group("thing") or match.group("bare")
    if not thing:
        return None, None
    if re.search(r"\bthan\b", _plain(thing)):
        return None, None
    head, name, head_part = _head_and_name(thing)
    if not head or not name or len(name.split()) > 6:
        return None, None
    if head.split()[-1].endswith("ing") or name.split()[0].endswith("ing"):
        return None, None
    kind = _KIND_OF.get(head)
    if kind in ("job", "bought") and _ALREADY_HAVE.search(head_part):
        return None, None
    if not kind:
        return None, None
    return kind, name


_BOUGHT = (
    "With {thing}, what happens after you pay is what decides it: who repairs {it}, what the "
    "guarantee actually covers, and what the running cost is against the price. Get those three in "
    "writing, then compare. What will you be asking of {it}?",
    "For {thing}, the three questions a shop will not put on the label are who repairs {it}, what "
    "the guarantee covers and what the running cost is. Ask all three before you look at the "
    "price. Is it for every day or now and then?",
    "Buying {thing} comes down to use and after-sales: what you will ask of {it}, and who takes "
    "{it} back if something goes wrong. Settle those two and the shopping is the easy part. What "
    "is it for, mainly?",
)

_JOB = (
    "For {thing}, preparation decides more than the day itself: one story for each line of your "
    "CV, and two questions about what the job actually has to deal with. Then ask what the hours "
    "and the first three months look like. Which stage are you at?",
    "Before {thing}, the work that pays is two or three stories you could tell a friend, and one "
    "question you genuinely want answered - the person who asks it is the one they remember. Do "
    "you know who you will be talking to?",
    "With {thing}, find out what the job has to deal with before you decide what to talk about: "
    "the hours, the team, and what happened to the last person in the role. Have you seen the job "
    "description, or just the advert?",
)

_EVENT = (
    "For {thing}, the order that saves arguments is the date, then how many people, then what each "
    "one can cost - places quote by the head and by the day. Settle the first two before you look "
    "at any room, or the room decides them for you. How many are you expecting?",
    "With {thing}, the two numbers to pin down first are how many people and what each of them can "
    "cost, before you fall for a place; the date then follows whatever is left. Roughly how many?",
    "For {thing}, read it backwards: what you can spend, divided by the people coming, is what any "
    "place has to beat. Do that sum before you visit anywhere. How many are coming?",
)

_POOLS = {"bought": _BOUGHT, "job": _JOB, "event": _EVENT}


def pool(line):
    kind, thing = _read(_plain(line))
    if not kind:
        return None
    head, name, _ = _head_and_name(thing)
    said = _as_said(name, head)
    return tuple(template.format(thing=said, it="them" if _is_plural(head) else "it")
                 for template in _POOLS[kind])


def reads_as_a_receipt(reply):
    said = _plain(reply)
    return bool(said) and any(said.startswith(receipt) for receipt in RECEIPTS)


def answer_for(text, memory=None, reply=""):
    if not reads_as_a_receipt(reply):
        return None
    options = pool(text)
    if not options:
        return None
    return pick(options, memory if isinstance(memory, dict) else {}, text)
