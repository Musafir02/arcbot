import re

from . import fallback, fallback_data

BARE_DAY = re.compile(
    r"^(?:and|or|also|what\s+about|how\s+about|what\s+if|and\s+what\s+about|so)?\s*"
    r"(?:(?:on|for|at)\s+)?(?:the\s+)?(?:bank\s+holiday\s+)?(?:(?:next|this|that)\s+)?"
    r"(?:monday|tuesdays?|wednesdays?|thursdays?|fridays?|saturdays?|sundays?|"
    r"weekends?|weekly|tomorrow|today|tonight|week|month|"
    r"christmas|boxing\s+day|new\s+year|easter|half\s+term|bank\s+holidays?|holidays?)"
    r"(?:\s+(?:day|morning|afternoon|evening|lunchtime|night))?[\s.?!]*$")

CHECK_REQUEST = re.compile(
    r"\b(?:can|could|would|will)\s+(?:you|u|ya)\s+(?:just\s+|please\s+|maybe\s+|quickly\s+|"
    r"quick\s+)*(?:check|look\s+(?:it|that|this)?\s*up|look|search|google|find\s+(?:it\s+)?out|"
    r"see)\b"
    r"|\bjust\s+(?:check|look\s+it\s+up|look|google\s+it|google|search)\b"
    r"|\b(?:check|look\s+it\s+up|search|google)\s+(?:it|that|this)?\s*for\s+me\b")

CHECK_REQUEST_ALONE = re.compile(
    r"^\s*(?:(?:and|so|ok|okay|well|but|then|cool|right|please)\s+)*"
    r"(?:(?:can|could|would|will)\s+(?:you|u|ya)\s+)?"
    r"(?:just\s+|please\s+|maybe\s+|quickly\s+|quick\s+)*"
    r"(?:check|look\s+(?:it|that|this)?\s*up|look|search|google|find\s+(?:it\s+)?out|see)"
    r"(?:\s+(?:it|that|this|for\s+me|then|now|again|please))*[\s.?!]*$")

SHORT_WORDS = ("open", "shut", "cost", "time", "road", "news", "bus", "car", "hot", "cold",
               "won", "jam", "tube")


def _the_limit_just_given(memory):
    try:
        said = str(fallback.last_bot(memory) or "").strip()
    except Exception:
        return None, ()
    if not said:
        return None, ()
    for kind, phrases, options in fallback_data.LIVE_KINDS:
        for line in options:
            head = str(line)[:40]
            if head and said.startswith(head):
                return options, tuple(str(one) for one in phrases)
    for pool in (fallback.CANNOT_ANYTHING, fallback.CANNOT_SEE_ANYTHING_LINES,
                 fallback.CANNOT_YOUR_OWN):
        for line in pool:
            head = str(line)[:40]
            if head and said.startswith(head):
                return pool, ()
    return None, ()


def _the_hours_pool():
    for kind, _phrases, options in fallback_data.LIVE_KINDS:
        if kind == "hours":
            return options
    return ()


def _words_of(phrases):
    words = set()
    for phrase in phrases:
        for word in re.findall(r"[a-z]+", phrase.lower()):
            if len(word) >= 4 or word in SHORT_WORDS:
                words.add(word)
    return words


def the_day_after(text, memory):
    clean = str(text or "").strip().lower()
    if not BARE_DAY.match(clean):
        return None
    hours = _the_hours_pool()
    if not hours:
        return None
    just, _phrases = _the_limit_just_given(memory)
    if not just or just != hours:
        return None
    return fallback._choose(hours, memory, clean)


def asked_to_check(text, memory):
    clean = str(text or "").strip().lower()
    if not CHECK_REQUEST.search(clean):
        return None
    just, phrases = _the_limit_just_given(memory)
    if not just:
        return None
    if not CHECK_REQUEST_ALONE.match(clean):
        covered = _words_of(phrases)
        if not covered:
            return None
        if not any(word in re.findall(r"[a-z]+", clean) for word in covered):
            return None
    return fallback._choose(just, memory, clean)


def answer_for(text, memory):
    return the_day_after(text, memory) or asked_to_check(text, memory)
