import re

ANSWER_MODULE = "answers"

_CONDITION = re.compile(r"\b(if|unless|until|once|before|after|whenever|as long as)\b")

_HANDOFF = re.compile(r"\b(gp|doctor|nurse|pharmacist|chemist|dentist|vet|council|landlord|"
                      r"seller|retailer|shop|airline|insurer|bank|999|111|nhs|advice|adviser|"
                      r"advisor|helpline|ombudsman|employer|school)\b")
_LIMIT = re.compile(r"\b(\d+|one|two|three|four|five|six|seven|eight|nine|ten|twelve|fourteen|"
                    r"twenty)\s+(day|days|week|weeks|month|months|year|years)\b")
_MORE_THAN = re.compile(r"\b(more than|over|longer than|up to|at least)\b")

_NEGATION = re.compile(r"\b(not|no|none|never|dont|doesnt|didnt|isnt|arent|wasnt|cant|cannot|"
                       r"without|nobody|nothing)\b")
_AMOUNT = re.compile(r"\b(\d+|one|two|three|four|five|six|seven|eight|nine|ten)\b")

_QUESTION_START = frozenset((
    "what", "how", "why", "when", "where", "who", "whom", "whose", "which", "can", "could",
    "should", "would", "shall", "will", "do", "does", "did", "is", "are", "was", "were", "am",
    "have", "has", "had", "may", "might", "must", "any", "anything", "isnt", "arent", "dont",
    "doesnt", "cant", "wont", "whats", "hows", "wheres", "whys",
))

_CORRECTION = re.compile(r"\b(i meant|i mean|i said|i wasnt saying|im talking about|"
                         r"i was talking about|the other one|not my|not the)\b")

LEAD = ("Right.", "Got it.", "Fair enough.", "Okay.", "Right then.")
POOL = (
    "{lead} The test does not turn on that: {clause}.",
    "{lead} Same test either way: {clause}.",
    "{lead} That leaves the test where it was: {clause}.",
    "{lead} The bit that decides it is unchanged: {clause}.",
)

STOP = frozenset("""
a an the and or but if then than that this these those it its it's is are was were be been being
i im i'm me my you your we our they their he she his her them us of in on at to for from with
about into over under as so not no do does did done have has had can could should would will
just very really quite too also more most much many some any thing things kind sort lot bit
""".split())


def _turns(memory):
    return [t for t in (memory or {}).get("turns") or [] if isinstance(t, dict)]


def _clean(text):
    return " ".join(str(text or "").lower().replace("\u2019", "'").split())


def _answer_above(memory):
    turns = _turns(memory)
    if not turns:
        return ""
    last = turns[-1]
    if str(last.get("module") or "") != ANSWER_MODULE:
        return ""
    return str(last.get("bot") or "").strip()


def _is_a_qualifier(clean):
    if not clean or "?" in clean:
        return False
    words = clean.split()
    if len(words) > 10:
        return False
    if words[0].strip(",.") in _QUESTION_START:
        return False
    if _CORRECTION.search(clean):
        return False
    if not (_NEGATION.search(clean) or _AMOUNT.search(clean) or "kind" in clean
            or "sort of" in clean):
        return False
    return True


def _content(text):
    out = set()
    for word in re.findall(r"[a-z']+", _clean(text)):
        word = word.strip("'")
        if len(word) < 4 or word in STOP:
            continue
        out.add(word[:-1] if word.endswith("s") and len(word) > 4 else word)
    return out


def _sentences(answer):
    parts = re.split(r"(?<=[.!?])\s+", str(answer or "").strip())
    return [p.strip() for p in parts if p.strip()]


def _is_a_test(sentence):
    lowered = " " + sentence.lower() + " "
    if not _CONDITION.search(lowered) or len(sentence.split()) < 5:
        return False
    return bool(_HANDOFF.search(lowered) or _LIMIT.search(lowered)
                or (_MORE_THAN.search(lowered) and _LIMIT.search(lowered)))


def _the_test(answer):
    found = ""
    for sentence in _sentences(answer):
        if _is_a_test(sentence):
            found = sentence
    if not found:
        return ""
    words = found.rstrip(" .;:,").split()
    if len(words) > 34:
        cut = " ".join(words[:34])
        comma = cut.rfind(",")
        words = (cut[:comma] if comma > 60 else cut).split()
    found = " ".join(words).rstrip(" ,;:")
    first = found.split(" ", 1)[0]
    if first[:1].isupper() and first[1:].islower():
        found = found[0].lower() + found[1:]
    return found


def _in_contact(clean, test):
    return bool(_content(clean) & _content(test))


def answer_for(text, memory=None):
    clean = _clean(text)
    answer = _answer_above(memory)
    if not answer or not _is_a_qualifier(clean):
        return None
    test = _the_test(answer)
    if not test or _in_contact(clean, test):
        return None
    lead = LEAD[sum(ord(c) for c in clean) % len(LEAD)]
    line = POOL[sum(ord(c) for c in clean + test) % len(POOL)]
    return line.format(lead=lead, clause=test)
