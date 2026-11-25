import re

from ..knowledge import lookup
from ..understanding import understand
from . import plans

_NOT_GOT = (
    re.compile(r"\b(?:still\s+)?(?:havent|haven't|hasnt|hasn't|aint|ain't)\s+"
               r"(?:got|gotten|had|bought|sorted|ordered|found|booked|chosen|picked)\s+"
               r"(?P<thing>[a-z][a-z' -]*)$", re.I),
    re.compile(r"\b(?:dont|don't|do\s+not|doesnt|doesn't)\s+have\s+(?P<thing>[a-z][a-z' -]*)$",
               re.I),
    re.compile(r"\b(?:not|n't)\s+(?:got|gotten)\s+(?P<thing>[a-z][a-z' -]*)$", re.I),
    re.compile(r"\b(?:no|without)\s+(?P<thing>[a-z][a-z' -]*?)\s+yet\b", re.I),
    re.compile(r"\b(?:need|needs|needed)\s+(?P<thing>[a-z][a-z' -]*)$", re.I),
)
_OCCASION = re.compile(
    r"\b(?:got|have|having|going\s+to|off\s+to|invited\s+to|for|at)\s+"
    r"(?P<occ>(?:a|an|the|my|our|his|her|their)\s+[a-z0-9][a-z0-9' -]{2,40})",
    re.I)

_OCCASION_HEAD = re.compile(
    r"^(?P<occ>(?:a|an|the|my|our|his|her|their)\s+[a-z][a-z0-9' -]{1,30}?)"
    r"(?:\s+(?:is|are|was|will\s+be|'s)\b.*)?$", re.I)

WORN = frozenset("""
outfit outfits dress dresses suit suits shirt shirts blouse blouses top tops skirt skirts
trousers pants shoes heels hat hats coat coats jacket jackets tie ties frock frocks jumpsuit
clothes clothing gown gowns boots sandals something
""".split())
GIVEN = frozenset("""
present presents gift gifts pressie card cards flowers bouquet wrapping paper
""".split())
GENERIC = frozenset("""
anything everything much sorted sorted organised organized booked arranged planned done
started chosen picked
""".split())


def _clauses(text):
    return [part.strip(" .!?,") for part in re.split(
        r"\s*(?:,|;|\band\b|\bbut\b|\bso\b|\bbecause\b)\s*", str(text or "").lower()) if part.strip()]


STOP = frozenset("a an the my our your his her their for to of in on at with and yet".split())


def _content(text):
    return {word for word in re.findall(r"[a-z']+", str(text or "").lower()) if word not in STOP}


def _what_is_missing(text):
    for clause in _clauses(text):
        for frame in _NOT_GOT:
            found = frame.search(clause)
            if found:
                phrase = found.group("thing").strip()
                thing = re.sub(r"^(?:a|an|the|my|our|any|some|another)\s+", "", phrase)
                thing = re.split(r"\s+(?:for|to|in|at|on|from)\s+|\s+yet\b", thing)[0].strip()
                if thing:
                    return thing, phrase
    return None


def _the_occasion(text, missing):
    found_all = []
    for clause in _clauses(text):
        found_all.extend(_OCCASION.finditer(clause))
        head = _OCCASION_HEAD.match(clause)
        if head:
            found_all.append(head)
    for found in found_all:
        occ = found.group("occ").strip(" -")
        after = re.split(r"\s+(?:for|to)\s+", occ)
        if len(after) > 1:
            occ = after[-1]
        occ = re.sub(r"\s+(?:in|on|at|for|to|next|this|the|with|of|yet)$", "", occ).strip(" -")
        if not occ or _content(occ) & _content(missing):
            continue
        if len(occ.split()) > 7:
            continue
        return occ[2:] if occ.lower().startswith("a ") else occ
    return None


def as_question(text):
    if not isinstance(text, str) or not text.strip():
        return None
    said = " ".join(text.lower().split())
    if "?" in said:
        return None
    missing = _what_is_missing(said)
    if not missing:
        return None
    thing, phrase = missing
    words = _content(phrase) | _content(thing)
    occasion = _the_occasion(said, thing)
    if not occasion:
        return None
    if words & GIVEN:
        return "what should i get for " + occasion
    if words & WORN or "wear" in words:
        return "what should i wear to " + occasion
    if words & GENERIC:
        return "how do i plan " + occasion
    return None


def answer(text, memory=None):
    question = as_question(text)
    if not question:
        return None
    store = memory if isinstance(memory, dict) else {}
    try:
        entry = lookup.find(understand(question, store))
    except Exception:
        return None
    if entry is None:
        return None
    reply = plans._the_reply(entry, question, store)
    if not isinstance(reply, str) or not reply.strip() or reply[:1].islower():
        return None
    return reply.strip()
