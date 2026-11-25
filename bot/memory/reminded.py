import re

from . import recent
from .topics import content, forms, stem

WITH_THE_THING = re.compile(
    r"\bwith\s+(?:((?:my|our|the)\s+[a-z][a-z'\-]*(?:\s+[a-z][a-z'\-]*){0,2})|"
    r"(it|that|this|them|those))\b", re.I)
TRAILING = frozenset("""again before earlier already then yesterday today please so far
until up now one ones thing things stuff lot""".split())
EMPTY = frozenset("one ones thing things stuff lot".split())
STATE_ASKS = re.compile(
    r"\b(?:wrong|up|(?:the\s+)?(?:problem|matter|issue|fault|trouble|deal)|happen\w*|going\s+on|"
    r"doing|keep\s+doing|kept\s+doing|said\s+about)\b", re.I)
STATE_SAID = re.compile(
    r"\b(?:keep\w*|kept|won'?t|wont|stopped|stopping|not\s+work\w*|doesnt\s+work\w*|"
    r"hurts?|hurting|sore|pain\w*|aches?|aching|swell\w*|swollen|stiff|"
    r"broken|broke|breaks?|cracked|leak\w*|drip\w*|dripping|slip\w*|slipped|jammed|stuck|"
    r"went|gone|dying|dead|failed|failing|crash\w*|dragging|drains?|drained|"
    r"struggl\w*|worr\w*|sort\w*|sorted|fault\w*|wrong|issue\w*|problem\w*|trouble|"
    r"stinks?|stink\w*|smell\w*|noise\w*|noisy|squeak\w*|rattle\w*|vibrat\w*|"
    r"slow\w*|weak\w*|blocked|clogged|mould\w*|damp)\b", re.I)
IN_THE_PAST = re.compile(
    r"^(?:and |so |but |also |ok |okay )?(?:what|whats|which)\s+(?:was|were|did|has|have|had)\b"
    r"|\b(?:what|whats)\s+(?:was|were)\b", re.I)
AGAIN = re.compile(r"\b(?:again|before|earlier|remind me|remind me again|"
                   r"(?:cant|can not|cannot|dont|do not) remember|"
                   r"what did i say|what did i tell you)\b", re.I)
REMINDING = re.compile(r"\b(?:remind me|(?:cant|can not|cannot|dont|do not) remember)\b", re.I)
THEIR_THING = re.compile(
    r"\b(?:what|whats|which)\s+(?:was|were|is|are|did|does|has|have|had|d)\s*"
    r"((?:my|our)\s+[a-z][a-z'\-]*(?:\s+[a-z][a-z'\-]*){0,3})\b"
    r"|\b(?:what|whats|which)\s+((?:my|our)\s+[a-z][a-z'\-]*(?:\s+[a-z][a-z'\-]*){0,3})\b",
    re.I)
ASK_WORDS = frozenset("""problem problems matter issue fault trouble deal going happening doing
wrong up again before earlier then so far please""".split())
THING_TAIL = ASK_WORDS | frozenset("was were is are be been being did does has have had".split())

WHAT_IT_DID = re.compile(
    r"\b(?:what|whats)\s+(?:did|does|has|have)\s+((?:my|our|the)\s+[a-z][a-z'\-]*"
    r"(?:\s+[a-z][a-z'\-]*){0,2}?)\s+(?:keep\s+|kept\s+)?(?:doing|do|say|saying)\b", re.I)


def _trim(words):
    kept = [word for word in str(words or "").split() if word.lower() not in TRAILING]
    return " ".join(kept).strip(" .,!?")


def _said_before(thing, memory):
    words = [word for word in content(thing) if word not in EMPTY]
    if not words:
        return False
    for turn in recent(memory, 12):
        line = turn.get("user") if isinstance(turn, dict) else None
        if not line:
            continue
        said = set(content(line))
        if all(any(word == seen or forms(word) & forms(seen) or stem(word) == stem(seen)
                   for seen in said) for word in words):
            return True
    return False


def the_thing(text, memory=None):
    line = " ".join(str(text or "").lower().split())
    if not line:
        return None
    if not STATE_ASKS.search(line):
        return None
    if not (IN_THE_PAST.search(line) or REMINDING.search(line)):
        return None
    if not AGAIN.search(line):
        return None
    thing = ""
    named = WITH_THE_THING.search(line)
    if named:
        if named.group(1):
            thing = _trim(named.group(1))
        else:
            thing = _resolved(named.group(2), memory)
    else:
        did = WHAT_IT_DID.search(line)
        if did:
            thing = _trim(did.group(1))
        else:
            theirs = THEIR_THING.search(line)
            if theirs:
                thing = _the_thing_itself(theirs.group(1) or theirs.group(2))
    if not thing or not content(thing):
        return None
    return thing


def _the_thing_itself(phrase):
    words = [word for word in str(phrase or "").split() if word]
    while len(words) > 1 and words[-1].strip(".,!?").lower() in THING_TAIL:
        words = words[:-1]
    return _trim(" ".join(words))


def _resolved(pronoun, memory):
    if not isinstance(memory, dict):
        return ""
    read = memory.get("understood")
    if not isinstance(read, dict):
        return ""
    ref = read.get("ref")
    if not isinstance(ref, dict):
        return ""
    value = ref.get(str(pronoun or "").lower())
    if isinstance(value, str) and value.strip():
        return _trim(value)
    return ""


def _said_what_was_wrong(thing, memory):
    words = [word for word in content(thing) if word not in EMPTY]
    if not words:
        return False
    for turn in recent(memory, 12):
        line = turn.get("user") if isinstance(turn, dict) else None
        if not line or not STATE_SAID.search(line):
            continue
        said = set(content(line))
        if all(any(word == seen or forms(word) & forms(seen) or stem(word) == stem(seen)
                   for seen in said) for word in words):
            return True
    return False


def about_a_thing_they_said(text, memory=None):
    try:
        thing = the_thing(text, memory)
        return bool(thing) and _said_before(thing, memory) and _said_what_was_wrong(thing, memory)
    except Exception:
        return False
