
import re

TOO_LONG = 12

TASTE = re.compile(
    r"^(?:so |and |but |ok |okay )?(?:do|did|would|will|should)\s+i\s+"
    r"(?:actually\s+|even\s+|really\s+|still\s+|probably\s+|think\s+i\s+)?"
    r"(?:like|love|enjoy|hate|want|fancy|prefer|get\s+on\s+with)\b", re.I)

RELATION = (r"(?:mum|mom|mam|dad|father|mother|son|daughter|child|kid|boy|girl|baby|sister|"
            r"brother|sibling|friend|mate|boss|manager|partner|husband|wife|boyfriend|"
            r"girlfriend|fianc\w*|nan|nana|gran|granny|grandma|grandad|grandpa|aunt|auntie|"
            r"uncle|cousin|niece|nephew|neighbour|neighbor|landlord|landlady|carer|colleague|"
            r"coworker|in-?laws?|stepson|stepdaughter|stepsister|stepbrother|ex|flatmate|"
            r"housemate|roommate|tutor|teacher|dog|cat|puppy|kitten|vet)")
THEM = (r"(?:(?:my|our|his|her|their)\s+" + RELATION + r"|she|he|they|him|her|them)")

AN_AGE_NAME_OR_PLACE = re.compile(r"\bhow\s+old\b|\bname\b|\bwhere\b", re.I)
WORK = re.compile(r"\bwhat\s+(?:does|do|did)\s+" + THEM + r"\s+(?:do|work\s+as)\b"
                  r"|\bwhats?\s+" + THEM + r"\s+like\b"
                  r"|\bwhat\s+is\s+" + THEM + r"\s+like\b", re.I)
ABOUT_THEM = re.compile(
    r"\b(?:who|what|where|when|which|how(?:\s+\w+)?)\s+(?P<about>(?:\w+\s+){0,2})"
    r"(?:is|was|are|were|does|did|do|has|have)\s+" + THEM + r"\b", re.I)
ALREADY_SAID = re.compile(r"\b[A-Za-z]{4,}\b")
STOP_ABOUT = frozenset("what whats which when where who whom whose does did have has about going "
                       "doing being their there these those".split())
A_NEED_OF_THEIRS = re.compile(
    r"\b" + THEM + r"\s+(?:need|needs|want|wants|take|takes|build|builds|make|makes|cook|"
    r"cooks|wear|wears|bring|brings|give|gives|try|tries|use|uses|buy|buys|eat|eats|say|says|"
    r"tell|tells|get|gets|say\s+to|do\s+about)\b", re.I)

STAY = re.compile(
    r"\bhow\s+long\s+(?:is|are|will|would|might|could|does|do)\s+" + THEM + r"\s+"
    r"(?:(?:likely|going|expected|probably|meant)\s+to\s+)?(?:be\s+)?(?:in|staying|stay|away|"
    r"off|be\s+off|be\s+in|have\s+to\s+stay|need\s+to\s+stay)\b"
    r"|\bhow\s+long\s+(?:is|are)\s+(?:the\s+)?(?:course|treatment|recovery|stay|operation)"
    r"\s+(?:going\s+to\s+)?(?:take|last)\b", re.I)
MISSING = re.compile(r"\b(?:missing|lost|gone|disappeared|found|ran\s+off|run\s+off|"
                     r"not\s+come\s+home|havent\s+come\s+home|hasnt\s+come\s+home)\b", re.I)
WHERE_THEY_ARE = re.compile(r"\bwhere(?:'s|\s+is|\s+are|\s+was|\s+were)\s+" + THEM + r"\b", re.I)
A_PRONOUN = re.compile(r"\b(?:she|he|they|him|her|them)\b", re.I)
SAID_WHO = re.compile(r"\b(?:my|our|his|her|their)\s+" + RELATION + r"\b|\b(?:mum|dad|son|"
                      r"daughter|sister|brother|friend|mate|partner|husband|wife|nan|gran|"
                      r"boss|colleague|neighbour)\b", re.I)

NOT_THIS = re.compile(
    r"\b(?:excess|booking|reference|policy|premium|prescription|appointment|balance|account|"
    r"order|invoice|bill|refund|renewal|renew|due\s+date|expiry|expires|warranty|guarantee|"
    r"membership|subscription|statement|receipt|tracking|delivery|parcel|form|deadline|"
    r"opening|closing|open|close|closed|hours|times|timetable|train|bus|flight|"
    r"what\s+time|"
    r"cost|price|how\s+much)\b", re.I)
RECALL = re.compile(r"\b(?:was\s+it|which\s+(?:\w+\s+)?was\s+it|what\s+did\s+i\s+say|"
                    r"again\b.*\bwhat|remind\s+me\s+what)\b", re.I)
A_HOW_TO = re.compile(r"\bhow\s+(?:do|does|did|can|could|should)\s+(?:i|you|we)\b", re.I)

PROSE = {
    "taste": (
        "That one's yours, not mine: I can't know what you like from here. What does your gut say?",
        "No way for me to know that, sorry - only you can say. What is your instinct telling you?",
        "I'd only be guessing, and you'd know in a second. What do you reckon?",
    ),
    "work": (
        "I've not met them, so I can't say what they do. What do they do?",
        "No idea, sorry - nobody has told me. What do they do for a living?",
        "Not a thing I could know. Tell me about them and I'll keep it straight from here: what "
        "do they do for a living?",
    ),
    "theirs": (
        "I've never met them, so I've nothing on that one - you'd know better than any page. "
        "Tell me and I'll keep it for the rest of our chat.",
        "That's yours to know and mine to be told. What's the answer?",
        "No idea, sorry - nobody has introduced us. Tell me and it stays here with me.",
    ),
    "stay": (
        "Only the people looking after them can say that - ask the nurse on the ward and they "
        "will give you a rough day. How are they in themselves?",
        "Nobody here can say how long they'll keep them in. The staff on the ward can, and the "
        "desk will ring through for you. How are they doing?",
        "That's the ward's call, not mine - the nurse looking after them knows, and it is one "
        "question at the desk. How is she in herself?",
    ),
}


def _bare(text):
    return re.sub(r"\s+", " ", (text or "").strip()).strip(" .!,").lower()


def _a_thing_already_said(match, memory):
    about = (match.group("about") or "").strip()
    words = [w for w in ALREADY_SAID.findall(about.lower()) if w not in STOP_ABOUT]
    if not words:
        return False
    turns = [str(t.get("user") or "").lower() for t in (memory.get("turns") or [])
             if isinstance(t, dict)]
    earlier = " ".join(turns[:-1])
    return any(w in earlier for w in words)


def _somebody_of_theirs(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)][-6:]
    return any(SAID_WHO.search(str(t.get("user") or "")) for t in turns)


def reads(text, memory=None):
    line = _bare(text)
    if not line:
        return None
    if len(line.split()) > TOO_LONG:
        return None
    if NOT_THIS.search(line) or RECALL.search(line) or A_HOW_TO.search(line):
        return None
    if AN_AGE_NAME_OR_PLACE.search(line):
        return None
    if MISSING.search(line) or WHERE_THEY_ARE.search(line):
        return None
    if A_NEED_OF_THEIRS.search(line):
        return None
    if TASTE.search(line):
        return "taste"
    for kind, pattern in (("work", WORK), ("stay", STAY), ("theirs", ABOUT_THEM)):
        found = pattern.search(line)
        if not found:
            continue
        if found.re is ABOUT_THEM and _a_thing_already_said(found, memory or {}):
            return None
        if A_PRONOUN.search(line) and not re.search(
                r"\b(?:my|our|his|her|their)\s+" + RELATION, line, re.I):
            if not _somebody_of_theirs(memory or {}):
                return None
        return kind
    return None


def reply_for(text, memory):
    kind = reads(text, memory)
    if not kind:
        return None
    lines = PROSE[kind]
    turns = len([t for t in (memory.get("turns") or []) if isinstance(t, dict)])
    return lines[turns % len(lines)]
