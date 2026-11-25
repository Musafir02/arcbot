import re

from . import pick

_LEAD = r"(?:(?:ok|okay|so|right|hi|hey|well)\s+)?"
_POLITE = r"(?:(?:please|just)\s+)?"
_TALK = r"(?:talk|chat|speak)"
_VERB = (r"(?:want|wanna|need|needed|would\s+like|'?d\s+like|have\s+to|got\s+to|gotta|"
         r"have|got)")

TALK_ASKS = tuple(re.compile(_LEAD + pattern) for pattern in (
    r"(?:can|could|would|will)\s+you\s+" + _POLITE + _TALK +
    r"\s+(?:to|with)\s+me\s+(?:about|through)\s+(?P<subject>.+)$",
    r"(?:can|could|may)\s+(?:i|we)\s+(?:please\s+)?" + _TALK +
    r"(?:\s+(?:to|with)\s+you)?\s+(?:about|through)\s+(?P<subject>.+)$",
    r"(?:i|we)\s+(?:just\s+|really\s+|honestly\s+)?" + _VERB +
    r"\s+(?:to\s+)?" + _TALK +
    r"(?:\s+(?:to|with)\s+you)?\s+(?:about|through)\s+(?P<subject>.+)$",
    _POLITE + _TALK + r"\s+to\s+me\s+(?:about|through)\s+(?P<subject>.+)$",
    r"(?:can|could|would|will)\s+you\s+" + _POLITE +
    r"help\s+me\s+(?:think|talk|work)\s+(?:about|through|out)\s+(?P<subject>.+)$",
    r"(?:i|we)\s+(?:just\s+|really\s+)?" + _VERB +
    r"\s+(?:to\s+)?(?:think|work)\s+(?:about|through|out)\s+(?P<subject>.+)$",
))

BLANK_SUBJECTS = frozenset((
    "it", "this", "that", "them", "something", "somethin", "anything", "everything",
    "stuff", "a thing", "one thing", "it all", "something else",
))
_SUBJECT_TAIL = re.compile(
    r"\s+(?:with|to)\s+(?:you|me)\s*$|\s+(?:again|please|now|today|tonight|later|tomorrow|"
    r"sometime|soon|this\s+(?:evening|afternoon|morning|weekend)|next\s+week)\s*$")
_WHEN = (r"(?:again|now|today|tonight|tomorrow|later|sometime|soon|"
         r"this\s+(?:evening|afternoon|morning|weekend)|next\s+week|"
         r"when\s+(?:you\s+)?(?:have|get|'ve\s+got)\s+a\s+(?:minute|mo|moment))")
_A_TIME_BEFORE_THE_THING = re.compile(
    r"\b(talk|chat|speak|think|work)\s+(?:to\s+(?:you|me)\s+)?"
    r"(?:" + _WHEN + r"\s+)+(?=(?:about|through|out)\b)")
_SUBJECT_HEAD = re.compile(r"^(?:the|that|this)\s+thing\s+(?:about|with)\s+")
_SOMETHING_ELSE = re.compile(
    r"^(?:something|anything|somebody|anybody|a\s+different\s+thing|something\s+different|"
    r"another\s+thing|anything\s+else\s+at\s+all)\s+else\s*[,;:\-\u2013\u2014]?\s*")
_SUBJECT_END = re.compile(
    r"\s+(?:its|it's|it is|it was|it's|and|but|because|cos|cuz|coz|so|which|that|who|"
    r"i|ive|i've|we|were|we're|he|she|they|my|our)\b.*$")
_CLAUSE_START = re.compile(
    r"^(?:how|what|why|whether|if|when|where|which|who|whoever|whatever)\b")
_SUBJECT_END_CLAUSE = re.compile(
    r"\s+(?:its|it's|it is|it was|and|but|because|cos|cuz|coz|which|that)\b.*$")
_HEDGED_END = re.compile(r"\s*,?\s*(?:maybe|perhaps|i\s+think|i\s+reckon|if\s+that\s+is\s+ok)\s*$")

_OWNERS = (("my", "your"), ("our", "your"))

_A_BARE_INVITATION = re.compile(
    _LEAD + r"(?:(?:can|could|may|shall|should)\s+(?:i|we)\s+" + _POLITE +
    r"|(?:i|we)\s+" + _VERB + r"\s+(?:to\s+)?|" + _POLITE + r")"
    r"(?:talk|chat|speak)(?:\s+(?:to|with)\s+(?:you|me))?"
    r"(?:\s+" + _WHEN + r")+\s*[?.!]*$")
_A_LEAD_IN_FRONT = re.compile(
    _LEAD + r"(?:(?:can|could|may|shall|should)\s+(?:i|we)\s+" + _POLITE +
    r"|(?:i|we)\s+" + _VERB + r"\s+(?:to\s+)?)"
    r"(?:talk|chat|speak)")
INVITED = (
    "Yes - I'm here whenever you are. What's on your mind?",
    "Any time. What is it you want to talk about?",
    "Of course. What's going on, and where do you want to start?",
)

POOL = (
    "Of course. Tell me about {thing} - what's the part that's bothering you most?",
    "{Thing} it is. What's on your mind about it?",
    "Happy to. Where do you want to start with {thing}?",
    "Right, {thing} - go on. What's the bit you want to think out loud about?",
)
POOL_CLAUSE = (POOL[0], POOL[3])
WEIGHING = (
    "Yes. What are the options you're weighing, as they stand now?",
    "Let's lay them out. What's on each side of it?",
    "Of course. What would you lose with each one?",
)
WEIGHING_WORDS = frozenset("""
options option choice choices decision decisions pros cons
""".split())


_TYPED_SHORT = (("u", "you"), ("ya", "you"), ("ur", "your"), ("yr", "your"),
                ("wana", "want"), ("wanna", "want"), ("wanta", "want"))
_REPEATED_WORD = re.compile(r"\b(\w+)(\s+\1\b)+")


def _as_typed(line):
    line = _REPEATED_WORD.sub(r"\1", line)
    words = [_TYPED_SHORT_DICT.get(word, word) for word in line.split()]
    return " ".join(words)


_TYPED_SHORT_DICT = dict(_TYPED_SHORT)


def the_line_as_read(text):
    return _A_TIME_BEFORE_THE_THING.sub(r"\1 ", _as_typed(text))


def _subject(text):
    text = the_line_as_read(text)
    for pattern in TALK_ASKS:
        found = pattern.match(text)
        if not found:
            continue
        subject = " " + found.group("subject").strip().rstrip(".!?,")
        subject = _SUBJECT_TAIL.sub("", subject).strip()
        subject = _SUBJECT_HEAD.sub("", subject).strip()
        subject = _SOMETHING_ELSE.sub("", subject).strip()
        clause = bool(_CLAUSE_START.match(subject))
        subject = (_SUBJECT_END_CLAUSE if clause else _SUBJECT_END).sub("", subject).strip()
        subject = _HEDGED_END.sub("", subject).strip()
        if subject in BLANK_SUBJECTS:
            return ""
        words = subject.split()
        if not words or len(words) > (9 if clause else 5):
            return ""
        for mine, theirs in _OWNERS:
            if words[0] == mine:
                words[0] = theirs
                break
        return " ".join(words)
    return ""


def answer_for(text, memory):
    line = " ".join((text or "").lower().split())
    if not line:
        return ""
    subject = _subject(line)
    if not subject:
        typed = _as_typed(line)
        if _A_BARE_INVITATION.match(typed) and (_A_LEAD_IN_FRONT.match(typed)
                                               or typed.rstrip().endswith("?")):
            return pick(INVITED, memory or {}, text)
        return ""
    if set(subject.split()) & WEIGHING_WORDS:
        return pick(WEIGHING, memory or {}, text)
    frames = POOL_CLAUSE if _CLAUSE_START.match(subject) else POOL
    lines = [one.format(thing=subject, Thing=subject[:1].upper() + subject[1:])
             for one in frames]
    return pick(lines, memory or {}, text)
