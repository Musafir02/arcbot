import re

CHANGED = re.compile(
    r"\b(?:change|changed|changes|changing|swapped|swapping|switched|switching|"
    r"given up|give up|gave up|gone off|went off|cut out|cut down|cutting out|cutting down|"
    r"stopped|stopping|quit|quitting|dropped|ditched|overhauled|tweaked|reworked)\b", re.I)
SUBJECT_CHANGED = re.compile(
    r"\b(?:is|are|has|have|had|got)\s+(?:all\s+)?(?:changed|different|new)\b"
    r"|\bis\s+not\s+the\s+same\b|\bnot the same\b", re.I)
WANTS = re.compile(
    r"\b(?:want(?:s|ed)?|wanna|need(?:s|ed)?|should|shall|ought|could|would|might|may|"
    r"thinking|thought|considering|planning|plan|trying|try|hoping|hope|ready|about|"
    r"worth|idea|better)\b", re.I)
HOW_TO = re.compile(r"\bhow\s+(?:do|does|can|could|should|would|might|to)\b|"
                    r"\bwhat(?:'s| is) the best way\b|\bany (?:tips|advice|ways)\b", re.I)
WHEN_TAIL = re.compile(r"\b(?:a|an|one|two|three|four|five|six|few|couple(?: of)?|\d+)\s+"
                       r"(?:day|week|month|year|while)s?(?:\s+or so)?\s+ago\b|"
                       r"\b(?:last|this)\s+(?:week|month|year)\b|"
                       r"\b(?:recently|lately|these days|nowadays)\b", re.I)
FILLER = frozenset("""
    i me my our we you your it its the a an to of and but so or now just really also too very
    much lot bit still again already even actually all right ok okay well oh ah yeah yes no
    have has had ve ive weve youve theyve im am is are was were be been do does did done
    dont doesnt didnt cant
""".split())
ASKS = {
    "diet": "What does a normal day look like now?",
    "budget": "What are you working with now?",
    "hours": "What are your hours now?",
    "job": "What are you doing now?",
}
WISHES = {
    "diet": ("What is the change for - weight, energy, or something a doctor said? That decides "
             "which swaps are worth it."),
    "budget": "What is the change for - a bill, a save, or paying something off?",
}
KEPT = "Good to know. "
DROPPING = "{was}, so I'll drop that - {ask}"
CHANGED_ASK = "What is it now?"
WISHED = "What are you trying to change about it? Tell me and I'll be concrete."
NOT_WANTING = re.compile(r"\b(?:don'?t|doesn'?t|didn'?t|not|never|no need|no plans|no intention)\b"
                         r"[^.!?]{0,20}\b(?:want|wanna|need|going to|gonna|plan|plans|thinking|"
                         r"planning|change|changing)\b", re.I)


def _names(line, subject):
    words = str(subject or "").strip()
    if not words:
        return False
    pattern = r"\b" + r"\s+".join(re.escape(part) for part in words.split()) + r"\b"
    return re.search(pattern, line, re.I) is not None


def _left_over(line, subject):
    mine = str(line or "")
    words = str(subject or "").strip()
    if words:
        mine = re.sub(r"\b" + r"\s+".join(re.escape(part) for part in words.split()) + r"\b",
                      " ", mine, flags=re.I)
    mine = WHEN_TAIL.sub(" ", mine)
    for pattern in (CHANGED, SUBJECT_CHANGED, WANTS):
        mine = pattern.sub(" ", mine)
    return [word for word in re.findall(r"[a-z']+", mine.lower())
            if word not in FILLER and word not in words.lower().split()]


def reported(text, subject):
    line = str(text or "").strip()
    if not line or not _names(line, subject):
        return None
    if HOW_TO.search(line) or NOT_WANTING.search(line):
        return None
    moved = CHANGED.search(line) or SUBJECT_CHANGED.search(line)
    if not moved:
        return None
    if _left_over(line, subject):
        return None
    before = line[:moved.end()]
    if WANTS.search(before):
        return "wanting"
    return "changed"


def reply(kind, subject, was=None):
    key = str(subject or "").strip().lower()
    if kind == "wanting":
        return WISHES.get(key) or WISHED
    ask = ASKS.get(key) or CHANGED_ASK
    if not was:
        return KEPT + ask
    settled = str(was).strip().rstrip(".")
    if settled.startswith("no "):
        settled = "You don't eat " + settled[3:]
    else:
        settled = "You were " + settled
    return DROPPING.format(was=settled, ask=ask[0].lower() + ask[1:])
