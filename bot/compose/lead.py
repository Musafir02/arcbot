import re

from . import fit

_TOTAL = re.compile(
    r"^(?:about|around|roughly|just|only|under|over|about an?|an?|a)\s*"
    r"[^.]{0,60}"
    r"\b(?:minutes?|mins?|hours?|hrs?|days?)\b"
    r"[^.]{0,60}?"
    r"\b(?:start to finish|from start to finish|in total|altogether|all in|end to end)\b",
    re.I)

_OPENING = re.compile(r"^\s*(\S.*?[.!?])\s+(\S.*)$", re.S)

_METHOD = frozenset(("steps",))

_SIGNPOST = re.compile(
    r"^(?:"
    r"(?:a few|a couple of|two|three|four|five|six|\d+)\s+"
    r"(?:things?|tests?|steps?|options?|ideas?|ways?|rules?|checks?|questions?|tips?|notes?|"
    r"points?|parts?)"
    r"(?:\s*,?\s*(?:in this order|to know|to try|to check|to keep in mind|first|for you|"
    r"to start with|before you start))?"
    r"|here(?:'?s| is| are)\s+(?:the|a|an|what|how|my|our|it|this)\b[^:]{0,60}"
    r"|the following\b[^:]{0,40}"
    r"|these are\b[^:]{0,40}"
    r"|(?:great|good|fair|interesting|nice|lovely) question"
    r"|(?:that'?s|it'?s) (?:a )?(?:great|good|fair|interesting|nice) question"
    r"|you (?:asked|want(?:ed)? to know|were asking|are asking)\b[^:]{0,80}"
    r"|so (?:you'?re|you are) asking\b[^:]{0,80}"
    r"|the question (?:is|was)\b[^:]{0,80}"
    r"|let me (?:start|explain|answer|walk you through|take you through|think)"
    r"|i'?ll (?:start|explain|answer|walk you through|take you through)"
    r"|i can (?:help|answer|explain|tell you)"
    r")$", re.I)


def _sentences(reply):
    text = " ".join(str(reply or "").split())
    if not text:
        return []
    out, start = [], 0
    for end in _SENTENCE_END.finditer(text):
        before = text[start:end.start()]
        if _ABBREVIATION_END.search(before):
            continue
        out.append(text[start:end.start()].strip())
        start = end.end()
    if text[start:].strip():
        out.append(text[start:].strip())
    return [sentence for sentence in out if sentence]


_SENTENCE_END = re.compile(r"(?<=[.!?])\s+")
_ABBREVIATION_END = re.compile(
    r"\b(?:e\.g|i\.e|approx|incl|etc|vs|cf|fig|dept|est|ref|tel|mr|mrs|ms|dr|prof)\.$", re.I)


def _wants_the_method(understood):
    if not isinstance(understood, dict):
        return False
    want = understood.get("wants")
    if isinstance(want, str):
        want = want.strip().lower()
    return want in _METHOD


_ASKS_HOW_OFTEN = re.compile(
    r"\bhow\s+(?:often|frequently)\b|\bhow\s+many\s+times\b|\bwhat\s+interval\b", re.I)
_A_RATE = re.compile(
    r"\b(?:once|twice|(?:three|four|five|six|\d+)\s+times"
    r"|every(?:\s+other)?(?:\s+\w+)?\s+(?:day|week|month|year|morning|evening|night)"
    r"|daily|weekly|monthly|yearly|nightly|fortnightly"
    r"|\d+\s+times\s+(?:a|an|per|each)\s+(?:day|week|month|year)"
    r"|(?:two|three|four|five)\s+times\s+(?:a|an|per|each)\s+(?:day|week|month|year))"
    r"(?:\s+(?:a|an|per|each)\s+(?:day|week|month|year))?\b", re.I)


def rate_first(reply, understood, line=None):
    if not isinstance(reply, str) or not reply.strip():
        return reply
    if not isinstance(line, str) or not _ASKS_HOW_OFTEN.search(line):
        return reply
    parts = _sentences(reply)
    if len(parts) < 2:
        return reply
    if _A_RATE.search(parts[0]):
        return reply
    for at, sentence in enumerate(parts[1:], 1):
        if _A_RATE.match(sentence) and len(sentence.split()) <= 22:
            return " ".join([sentence] + parts[:at] + parts[at + 1:])
    return reply


def answer_first(reply, understood, line=None):
    if not isinstance(reply, str) or not reply.strip():
        return reply
    reply = rate_first(reply, understood, line)
    parts = _sentences(reply)
    if len(parts) > 1:
        first = parts[0].rstrip(".!? ").strip()
        if first and _SIGNPOST.match(first):
            reply = " ".join(parts[1:])
    reply = verdict_first(reply, understood, line)
    if _wants_the_method(understood):
        return method_first(reply, understood)
    return cause_first(reply, understood)


_VERDICT_OPENS = re.compile(
    r"^(?:yes|yeah|yep|no|nope)\b(?=\s*[,.;:!?-]|\s*$)"
    r"|^(?:not really|not usually|not always)\b"
    r"|^(?:worth it|not worth it|worth the money)\b"
    r"|^(?:it is|it's) (?:worth|not worth|fine|safe|okay|ok|not safe|not fine)\b"
    r"|^(?:it depends|usually|definitely|in most cases|most of the time)\b", re.I)


_THINKING_IT_OVER = re.compile(
    r"\bworth\b[^.]{0,40}\b(?:whether|asking|thinking|a thought|considering|wondering|"
    r"talking about it|a conversation|a talk|checking first)\b", re.I)


def verdict_first(reply, understood, line=None):
    if not isinstance(reply, str) or not reply.strip():
        return reply
    if _the_want(understood) != fit.YESNO:
        return reply
    parts = _sentences(reply)
    if len(parts) < 2:
        return reply
    bare_opening = parts[0].rstrip(".!? ").strip()
    if _VERDICT_OPENS.match(bare_opening):
        return reply
    for place, sentence in enumerate(parts[1:], 1):
        bare = sentence.rstrip(".!? ").strip()
        if not bare or not _VERDICT_OPENS.match(bare):
            continue
        if _THINKING_IT_OVER.search(bare):
            continue
        try:
            if fit.gives(bare, fit.YESNO, line) is False:
                continue
        except Exception:
            continue
        rest = " ".join(parts[:place] + parts[place + 1:])
        return "%s %s" % (sentence, rest)
    return reply


def method_first(reply, understood):
    if not isinstance(reply, str) or not reply.strip():
        return reply
    if not _wants_the_method(understood):
        return reply
    found = _OPENING.match(reply)
    if not found:
        return reply
    opening, rest = found.group(1).strip(), found.group(2).strip()
    if not _TOTAL.match(opening):
        return reply
    if not rest:
        return reply
    return "%s %s" % (rest, opening)


_CAUSE_SENTENCE = re.compile(
    r"^\s*(?:the|a|an)\s+"
    r"(?:usual|main|most likely|likely|commonest|common|real|other|whole)?\s*"
    r"(?:reason|cause)s?\b(?![?!])",
    re.I)


def _wants_the_cause(understood):
    if not isinstance(understood, dict):
        return False
    want = understood.get("wants")
    if isinstance(want, str):
        want = want.strip().lower()
    return want == fit.REASON


def cause_first(reply, understood):
    if not isinstance(reply, str) or not reply.strip():
        return reply
    if not _wants_the_cause(understood):
        return reply
    parts = _sentences(reply)
    if len(parts) < 2:
        return reply
    for index in range(1, len(parts)):
        if _CAUSE_SENTENCE.match(parts[index]):
            moved = parts[index]
            rest = parts[:index] + parts[index + 1:]
            return " ".join([moved] + rest)
    return reply


_HARD = frozenset((fit.TIME, fit.AMOUNT, fit.PLACE, fit.PERSON, fit.MEANING,
                   fit.YESNO, fit.PICK, fit.STEPS, fit.OPTIONS, fit.REASON))

_SAID_WORD = re.compile(r"[a-z0-9]+")


def _the_want(understood):
    if not isinstance(understood, dict):
        return ""
    want = understood.get("wants")
    if not isinstance(want, str):
        return ""
    return want.strip().lower()


def _the_opening(reply):
    return fit.first_sentence(reply)


def _already_said(lead_said, opening):
    mine = [w for w in _SAID_WORD.findall(lead_said.lower()) if len(w) > 2]
    if not mine:
        return lead_said.lower().strip(" .,!?") == " ".join(_SAID_WORD.findall(opening.lower()))
    there = set(_SAID_WORD.findall(opening.lower()))
    return all(word in there for word in mine)


def _the_own_sentence_holding(parts, bare):
    mine = [w for w in _SAID_WORD.findall(bare.lower()) if len(w) > 2]
    if not mine:
        return None
    for at, part in enumerate(parts):
        there = set(_SAID_WORD.findall(part.lower()))
        if all(word in there for word in mine):
            return at
    return None

def the_sentence_owed(reply, understood, declared=None):
    if not isinstance(reply, str) or not reply.strip():
        return reply
    if not isinstance(declared, (tuple, list)) or len(declared) != 2:
        return reply
    shape, said = declared
    shape = shape.strip().lower() if isinstance(shape, str) else ""
    if shape not in _HARD or _the_want(understood) != shape:
        return reply
    if callable(said):
        try:
            said = said(understood)
        except Exception:
            return reply
    if not isinstance(said, str) or not said.strip():
        return reply
    bare = " ".join(said.split()).rstrip(" .!?")
    if not bare:
        return reply
    opening = _the_opening(reply)
    if reply.lstrip().lower().startswith(bare.lower()):
        return reply
    if _already_said(bare, opening):
        return reply
    line = understood.get("text") if isinstance(understood, dict) else None
    if not isinstance(line, str):
        line = (understood.get("clean") if isinstance(understood, dict) else "") or ""
    try:
        if fit.gives(bare, shape, line) is False:
            return reply
    except Exception:
        return reply
    parts = _sentences(reply)
    at = _the_own_sentence_holding(parts, bare)
    if at is not None and at > 0:
        return " ".join(parts[at:] + parts[:at])
    return "%s. %s" % (bare, reply.lstrip())


_LIFTABLE = frozenset((fit.TIME, fit.AMOUNT, fit.PLACE))

_POINTS_BACKWARDS = re.compile(
    r"^\s*(?:it|its|it's|that|that's|this|these|those|they|them|their|there\s+(?:it|they|you|we|that|those|these)\b|then|so|and|but|also|"
    r"otherwise|still|though|however|either|neither|both|such|the same|which|who|if|unless|"
    r"in that case|at that point|after that|for now)\b", re.I)


_OPENS_WITH_SYMPATHY = re.compile(
    r"^\s*(?:(?:i'm|i am|so|very|truly)\s+)*(?:sorry|apologies)\b|"
    r"^\s*that'?s\s+(?:hard|awful|terrible|rough|grim|rotten|a lot)\b|"
    r"^\s*i'?m\s+so\s+sorry\b|^\s*my\s+(?:heart|sympathies)\b", re.I)


_OPENS_WITH_A_WARNING = re.compile(
    r"^\s*(?:there'?s?\s+(?:is\s+)?no\s+safe\b|no\s+safe\b|never\b|do\s+not\b|don'?t\b|"
    r"(?:call|ring|phone)\s+999\b|999\b|go\s+to\s+(?:a&e|the\s+hospital)\b)", re.I)


_SHARED_WORDS = frozenset((
    "the", "and", "for", "that", "this", "with", "you", "your", "have", "has", "are", "was",
    "were", "what", "when", "where", "which", "who", "why", "how", "should", "could", "would",
    "will", "been", "being", "about", "there", "their", "them", "they", "from", "into", "than",
    "then", "some", "any", "can", "does", "did", "doing", "not", "but", "one", "out", "over",
    "very", "just", "like", "get", "gets", "got", "much", "many", "more", "most", "long",
    "take", "takes", "need", "needs", "want", "wants", "make", "made", "is", "it"))


def _words(text):
    return {word for word in re.findall(r"[a-z]{4,}", str(text or "").lower())
            if word not in _SHARED_WORDS}


def _names_the_line(sentence, line):
    if not line:
        return True
    asked = _words(line)
    return bool(asked & _words(sentence))


def _sentence_stands_alone(sentence):
    text = " ".join(str(sentence or "").split())
    if len(text.split()) < 4:
        return False
    if _POINTS_BACKWARDS.match(text):
        return False
    return not text.endswith("?")


def shape(reply, understood, line=None):
    if not isinstance(reply, str) or not reply.strip():
        return reply
    if not isinstance(understood, dict):
        return reply
    want = understood.get("wants")
    if not isinstance(want, str):
        return reply
    want = want.strip().lower()
    if want in _METHOD:
        return method_first(reply, understood)
    if want not in _LIFTABLE:
        return reply
    parts = _sentences(reply)
    if len(parts) < 2:
        return reply
    if fit.gives(parts[0], want, line) is True or fit.is_a_punt(parts[0]):
        return reply
    if re.search(r"\d", parts[0]) and _names_the_line(parts[0], line):
        return reply
    if _OPENS_WITH_SYMPATHY.search(parts[0]):
        return reply
    if _OPENS_WITH_A_WARNING.search(parts[0]):
        return reply
    when_asked = bool(line) and re.search(r"\bwhen\b", line, re.I) is not None
    for index in range(1, len(parts)):
        sentence = parts[index]
        if when_asked and not fit.CLOCK.search(sentence):
            continue
        if _OPENS_WITH_A_WARNING.search(sentence):
            continue
        if not _sentence_stands_alone(sentence):
            continue
        if want not in (fit.TIME, fit.AMOUNT) and (fit._a_time(sentence) or fit._an_amount(sentence)):
            continue
        if fit.gives(sentence, want, line) is not True:
            continue
        if not _names_the_line(sentence, line):
            continue
        moved = [sentence] + parts[:index] + parts[index + 1:]
        return " ".join(moved)
    return reply
