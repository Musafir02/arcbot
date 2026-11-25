import re

from .aboutness import is_a_hedge as _a_hedge, restates_the_line, unlike_the_line
from . import fallback as _fallback

A_LIMIT = re.compile(
    r"(?:doesn'?t|does\s+not|won'?t|will\s+not|can'?t|cannot|isn'?t\s+keen|not\s+keen|"
    r"hates?|allergic|refuses?|avoids?|no\s+(?:meat|alcohol|drink|drinking|stairs|loud\s+\w+|"
    r"sugar|gluten|dairy|fish|pork|nuts))\b", re.I)

A_PERSON = re.compile(
    r"\b(?:he|she|they|him|her|them|we|us|i|i'?m|im|i'?ve|you|one\s+of\s+us|somebody|someone|"
    r"everybody|everyone|(?:my|our|his|her|their|your)\s+(?:mum|mom|mother|dad|father|son|"
    r"daughter|child|kid|baby|wife|husband|partner|boyfriend|girlfriend|brother|sister|friend|"
    r"mate|nan|gran|grandad|grandma|aunt|uncle|cousin|boss|colleague|family|in-laws?|parents?|"
    r"niece|nephew|flatmate|housemate|guests?))\b", re.I)

A_MACHINE_VERB = re.compile(
    r"\b(?:boils?|starts?|charges?|connects?|turns?|shuts?|opens?|closes?|fires?|spins?|prints?|"
    r"works?|drains?|heats?|pairs?|loads?|syncs?|boots?|scans?|locks?|rings?|beeps?|plays?|"
    r"records?|downloads?|uploads?|updates?|runs?|shows?|detects?|responds?|freezes?|crashes?|"
    r"drips?|flushes?|restarts?)\b", re.I)

_A_SAYING = (r"said|tried|asked|told|rung|rang|called|emailed|texted|written|complained")
AN_ATTEMPT = re.compile(
    r"(?:\b(?:i|we|he|she|they|you)(?:'?ve|\s+have|\s+had)?\s+(?:already\s+|just\s+)?"
    r"(?:" + _A_SAYING + r")\b"
    r"|\b(?:" + _A_SAYING + r")\s+(?:that|it|him|her|them)\b"
    r"|\b(?:already|just)\s+(?:" + _A_SAYING + r")\b"
    r"|\bi\s+did\s+that\b|\bsaid\s+no\b)", re.I)

A_HISTORY = re.compile(
    r"(?:\bwas\s+(?:fine|ok|okay|all\s+right)\b|\bused\s+to\b|\bsince\s+(?:last|the|march|april|"
    r"may|june|july|august|september|october|november|december|january|february)\b|"
    r"\bfor\s+(?:\d+|two|three|four|five|six|seven|eight|nine|ten|a\s+few|years|months|weeks|"
    r"days)\b|\bit\s+started\b|\bstarted\s+(?:in|last|when)\b|"
    r"\bevery\s+(?:day|week|morning|night|time)\b)", re.I)

_REPLIES = {
    "limit": (
        "%s - is that a hard no, or just something to keep off the plan?",
        "%s, then. Does that rule the whole thing out, or only that part of it?",
        "%s - how far does the plan have to go round it?",
    ),
    "attempt": (
        "%s - how did that go down?",
        "%s, so what did they say?",
        "%s - what came of it?",
    ),
    "history": (
        "%s - how often is it happening now?",
        "%s, so something changed. What was it like just before that?",
        "%s - has anything else changed since?",
    ),
}

_TIDY = (
    (r"\bi'?m\b", "I'm"), (r"\bi'?ve\b", "I've"), (r"\bi'?ll\b", "I'll"), (r"\bi'?d\b", "I'd"),
    (r"\bdont\b", "don't"), (r"\bdoesnt\b", "doesn't"), (r"\bdidnt\b", "didn't"),
    (r"\bcant\b", "can't"), (r"\bwont\b", "won't"), (r"\bim\b", "I'm"), (r"\bive\b", "I've"),
    (r"\bhavent\b", "haven't"), (r"\bisnt\b", "isn't"), (r"\bwasnt\b", "wasn't"),
    (r"\btheyre\b", "they're"), (r"\bthats\b", "that's"), (r"\bits\b", "it's"),
    (r"\bi\b", "I"),
) + tuple(
    (r"\b%s\b" % word, word.capitalize()) for word in (
        "january", "february", "march", "april", "may", "june", "july", "august", "september",
        "october", "november", "december", "monday", "tuesday", "wednesday", "thursday",
        "friday", "saturday", "sunday"))

_LEAD = re.compile(r"^(?:and|but|so|also|well|ok|okay|oh|ah|right|yeah|yes)\s+", re.I)
_QUESTION_OPEN = re.compile(
    r"^(?:what|why|how|when|where|who|which|whose|is|are|was|were|do|does|did|can|could|"
    r"should|would|will|shall|have|has|had|am|if)\b", re.I)


def _clean_line(text):
    return " ".join(str(text or "").lower().replace("\u2019", "'").split())


SERIOUS = re.compile(
    r"\b(?:bull(?:y|ied|ies|ying)|cancer|chemo|tumour|biopsy|died|dying|death|funeral|bereave\w*|"
    r"grief|grieving|abuse[ds]?|assault\w*|miscarr\w*|stillborn|self[-\s]?harm|suicide|suicidal|"
    r"custody|social\s+services|evict\w*|homeless|bankrupt\w*|debt\s+collector|depress\w*|"
    r"anxiety|panic\s+attack|addict\w*|drinking\s+too\s+much|hospital|sectioned)\b", re.I)


def the_thread_is_serious(turns, line=""):
    said = " ".join(str(one.get("user") or "") for one in (turns or ())) + " " + str(line or "")
    return bool(SERIOUS.search(said))


def fallback_heavy(turns):
    try:
        return bool(_fallback.reads_as_heavy_news(_clean_line(turns[-1].get("user")))
                    or _fallback._the_thread_is_heavy({"turns": turns}))
    except Exception:
        return False


def the_clause_said_back(text):
    said = " ".join(str(text or "").split()).strip(" .,!?-")
    while True:
        shorter = _LEAD.sub("", said)
        if shorter == said:
            break
        said = shorter
    for pattern, instead in _TIDY:
        said = re.sub(pattern, instead, said, flags=re.I)
    if not said:
        return ""
    return said[0].upper() + said[1:]


def the_kind_of_detail(clean):
    if A_LIMIT.search(clean) and A_PERSON.search(clean) and not A_MACHINE_VERB.search(clean):
        return "limit"
    if AN_ATTEMPT.search(clean):
        return "attempt"
    if A_HISTORY.search(clean):
        return "history"
    return None


def detail_pool(clean, memory):
    clean = _clean_line(clean)
    if len(clean.split()) < 3 or "?" in clean or _QUESTION_OPEN.match(clean):
        return None
    turns = [turn for turn in ((memory or {}).get("turns") or []) if isinstance(turn, dict)]
    if not turns:
        return None
    if fallback_heavy(turns) or the_thread_is_serious(turns):
        return None
    kind = the_kind_of_detail(clean)
    if not kind:
        return None
    clause = the_clause_said_back(clean)
    if len(clause.split()) < 3:
        return None
    said = _second_person(clause)
    return tuple(line % said for line in _REPLIES[kind])


_SECOND_PERSON_WORDS = {
    "i": "you", "i'm": "you're", "i've": "you've", "i'll": "you'll", "i'd": "you'd",
    "im": "you're", "ive": "you've", "ill": "you'll", "id": "you'd",
    "my": "your", "mine": "yours", "me": "you", "myself": "yourself",
}


def _second_person(clause):
    words = []
    for at, word in enumerate(str(clause or "").split()):
        core = word.rstrip(",.?!")
        swap = _SECOND_PERSON_WORDS.get(core.lower().replace("\u2019", "'").replace("'", "'"))
        if not swap:
            words.append(word)
            continue
        if at == 0:
            swap = swap[:1].upper() + swap[1:]
        words.append(swap + word[len(core):])
    return " ".join(words)


def says_nothing_about_the_line(reply, text):
    reply = str(reply or "")
    if not reply.strip():
        return True
    if len(reply.split()) > 22:
        return False
    if _a_hedge(reply) or restates_the_line(reply, text):
        return True
    about, said = unlike_the_line(reply, text)
    return bool(about) and not said
