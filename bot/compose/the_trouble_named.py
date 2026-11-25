import re

from . import fallback

A_THE_TROUBLE = re.compile(
    r"^(?:so\s+|well\s+|and\s+|but\s+|ok\s+|okay\s+|yeah\s+|yeh\s+|no\s+|also\s+|honestly\s+)*"
    r"(?:(?:it'?s|its|it\s+is)\s+(?:the|my|our|his|her|their|this|that|me)?\s*"
    r"(?P<thing>[a-z][a-z' -]{2,40}?)\s+(?:that'?s|thats|what'?s|which\s+is|is)\s+"
    r"(?:the\s+|my\s+|our\s+)?(?:problem|trouble|issue|worry|wrong|bit\s+that'?s\s+wrong)"
    r"|(?:the|my|our)\s+(?:problem|trouble|issue)\s+(?:is|was)\s+"
    r"(?:the|my|our|his|her|their)?\s*(?P<thing2>[a-z][a-z' -]{2,40}))", re.I)
A_BROKEN_NOW = re.compile(
    r"\b(?:broken|broke|not\s+working|stopped\s+working|packed\s+in|packed\s+up|dead|leaking"
    r"|flooding|blown|on\s+fire|smoking|sparking|no\s+power|no\s+hot\s+water|not\s+coming\s+on"
    r"|not\s+starting|wont\s+start)\b", re.I)
A_ASK = re.compile(r"\?|\b(?:can|could|should|how|what|when|why|which|who|shall)\b", re.I)
FILLER = {"a", "an", "the", "my", "our", "his", "her", "their", "this", "that", "me", "it",
          "and", "but", "so", "for", "of", "with", "on", "in", "at", "to"}


def _has(text, words):
    return bool(set(re.findall(r"[a-z']+", text)) & set(words))


SUPPLY = ("electric", "electricity", "electrics", "power", "meter", "fuse", "fuses", "gas")
HEATING = ("boiler", "heating", "radiator", "radiators", "hot", "immersion", "thermostat")
WATER = ("water", "leak", "leaking", "drain", "drains", "tap", "taps", "sink", "toilet", "plumbing",
         "pipe", "pipes", "shower", "bath")
VEHICLE = ("car", "van", "bike", "motorbike", "scooter", "engine", "tyre", "tyres", "clutch",
           "mot", "gearbox", "battery", "brakes")
CONNECTION = ("wifi", "internet", "broadband", "signal", "mobile", "phone", "router", "connection",
              "landline", "data")
BILL = ("rent", "mortgage", "council", "tax", "bill", "bills", "energy", "debt", "loan", "money",
        "fees", "fee", "service", "charge", "charges")

SAY = {
    "supply": (
        "A supply goes wrong in one of two ways - a bill that has got away from you, or the supply "
        "itself - and the first step is different for each. Which is it for you?",
        "With the electric or the gas it is nearly always the bill or the supply, and one is a "
        "phone call to the supplier while the other is a payment plan. Which is it?",
    ),
    "heating": (
        "Heating trouble is usually either a bill you can't cover or the boiler not doing its job, "
        "and the first step is different for each. Which is it for you?",
        "The heating has two ways of becoming the problem - what it costs, or it not coming on - "
        "and the fix is different for each. Which one is it?",
    ),
    "water": (
        "Water in the wrong place is a today job and water that has stopped is the supplier's; the "
        "first move is different for each. Which is it for you?",
        "Two different problems wear the same word: a leak, which is a today job, and a supply "
        "that has gone, which is the water company's. Which one is yours?",
    ),
    "vehicle": (
        "A vehicle goes wrong in two ways that matter - something is not right with it, or what "
        "putting it right costs - and the first step is different for each. Which is it?",
        "With a car it is usually the thing itself or the bill to fix it, and only one of those is "
        "the garage's. Which one is the trouble?",
    ),
    "connection": (
        "Broadband goes wrong in two ways - the connection dropping, or the bill - and the first "
        "check is different for each. Which is it?",
        "A connection problem is either the line or the account, and the supplier's own status page "
        "answers the first before you ring anybody. Which of the two is it?",
    ),
    "bill": (
        "A bill becomes the problem in one of two ways - too big for the month, or wrong on the "
        "paper - and the first step is different for each. Which is it?",
        "It is usually either the amount or the paper, and a bill that is wrong is worth a call "
        "before a payment plan. Which one is it for you?",
    ),
}


def _family(thing):
    if _has(thing, VEHICLE):
        return "vehicle"
    if _has(thing, CONNECTION):
        return "connection"
    if _has(thing, BILL):
        return "bill"
    if _has(thing, SUPPLY):
        return "supply"
    if _has(thing, HEATING):
        return "heating"
    if _has(thing, WATER):
        return "water"
    return None


def _the_wording(memory, family):
    try:
        turns = memory.get("turns") or ()
    except AttributeError:
        turns = ()
    wordings = SAY[family]
    return wordings[len(turns) % len(wordings)]


def reply_for(text, memory=None):
    clean = " ".join(str(text or "").lower().split())
    if not clean or "?" in clean:
        return None
    match = A_THE_TROUBLE.search(clean)
    if not match:
        return None
    thing = (match.group("thing") or match.group("thing2") or "").strip()
    if not thing:
        return None
    if A_ASK.search(clean):
        return None
    rest = (clean[:match.start()] + " " + clean[match.end():])
    if [word for word in re.findall(r"[a-z']+", rest) if word not in FILLER]:
        return None
    words = [word for word in re.findall(r"[a-z']+", thing) if word not in FILLER]
    if not words:
        return None
    family = _family(thing)
    if family is None:
        return None
    if A_BROKEN_NOW.search(clean):
        return None
    said = fallback.reply_for(text, memory if memory is not None else {})
    if said and not (fallback._nothing_to_stand_behind(said) or fallback._is_a_hedge(said)):
        return None
    return _the_wording(memory if memory is not None else {}, family)
