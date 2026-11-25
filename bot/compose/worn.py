import re

from . import trouble

WEAR = re.compile(r"""
    \b(?:is|are|was|were|'s|its|it's|gets|got|has\s+been|have\s+been|had\s+been)\b
    [^.!?,;]{0,22}?
    \b(?:
        killing\s+me | the\s+death\s+of\s+me
      | doing\s+my\s+head\s+in
      | driving\s+me\s+(?:mad|crazy|nuts|up\s+the\s+wall|round\s+the\s+bend|insane)
      | a\s+(?:(?:real|right|total|proper|absolute|bit\s+of\s+a|such\s+a|bloody)\s+)?
        (?:nightmare|mare|pain|slog|chore)
      | wearing\s+me\s+(?:down|out)
      | getting\s+on\s+top\s+of\s+me
      | taking\s+(?:forever|ages|all\s+day|all\s+week|so\s+long|longer\s+than)
      | never\s+ending | endless
      | (?:getting\s+)?out\s+of\s+control
      | going\s+on\s+forever
      | taking\s+over\s+my\s+life
    )\b
""", re.X)

PILE = re.compile(r"""
    \b(?:
        (?:so\s+much|so\s+many|loads\s+of|lots\s+of|tons\s+of|masses\s+of|piles?\s+of|a\s+heap\s+of)
        [^.!?,;]{0,30}?
        \b(?:to\s+(?:do|sort|mark|write|finish|file|get\s+through|deal\s+with|catch\s+up\s+on
                       |work\s+through|go\s+through))
      | (?:i'?m|im|i\s+am|i'?ve|ive|i\s+have|we'?re|we\s+are)\b[^.!?,;]{0,22}?
        \b(?:swamped|snowed\s+under|drowning|behind\s+on|way\s+behind|backed\s+up)
      | \b(?:the\s+)?(?:backlog|to[- ]?do\s+list|housework|ironing|washing\s+up|paperwork)\b
        [^.!?,;]{0,20}?
        \b(?:piling\s+up|stacking\s+up|mounting\s+up|out\s+of\s+control|never\s+ends)
      | \b(?:a\s+)?(?:mountain|heap|pile|ton|tonne|stack)\s+of\s+(?:the\s+|my\s+|our\s+)?[a-z]+
      | \b(?:piling|piling\s+up|stacking\s+up|mounting\s+up)\b
    )
""", re.X)

MONEY = frozenset(("rent", "mortgage", "bill", "bills", "debt", "debts", "arrears", "council",
                   "loan", "loans", "overdraft", "credit", "card", "cards", "repayment",
                   "repayments", "interest", "owe", "owed", "fines"))

WEATHER = frozenset(("heat", "cold", "weather", "humidity", "sun", "rain", "summer", "winter",
                     "wind", "snow", "frost", "traffic", "commute", "bus", "train", "tube"))

A_STRETCH = frozenset(("week", "weeks", "month", "months", "day", "days", "year", "years",
                       "term", "shift", "shifts", "morning", "afternoon", "evening", "night",
                       "nights", "weekend", "fortnight", "time", "while", "hour", "hours"))

EXTRA_BODY = frozenset(("pelvis", "bump", "tummy", "womb", "cervix", "abdomen"))

NOT_A_JOB = frozenset(("everything", "anything", "things", "thing", "stuff", "life", "all",
                       "lot", "world", "loads", "too", "much", "up", "piling", "stacking",
                       "mounting", "behind", "snowed", "under", "swamped", "drowning",
                       "backed"))

POINTING = frozenset(("this", "that", "these", "those", "the", "a", "an", "my", "our", "it",
                      "its", "it's", "last", "past", "few", "couple", "of", "whole", "every",
                      "all", "and", "been", "has", "have", "had", "always", "so", "far", "now",
                      "recently", "lately", "today", "i", "im", "i'm", "ive", "i've", "we",
                      "we're", "with", "to", "many", "again", "on", "out", "control", "sort",
                      "sorting", "sorted"))

ROLE = frozenset(("work", "job", "jobs", "office", "employer", "boss", "school", "uni",
                  "university", "college", "course", "degree", "business", "placement",
                  "apprenticeship", "phd", "thesis"))

PILE_REPLIES = (
    "Then it's a sorting job before it's a doing job: what has to happen today, and what can "
    "wait until next week?",
    "Start with the smallest one and finish it before you look at the rest of the pile.",
    "Piles like that shrink the moment you start. Which one is actually due first?",
    "Ugh. Pick the one that would be a relief to have done, and give it twenty minutes.",
)

JOB_REPLIES = (
    "That one's a slog. What's it fighting you on?",
    "It's usually the fiddly part that eats the time. Which bit is the worst?",
    "Ugh, the kind of job that takes longer than anyone says. Where are you up to with it?",
    "Fair enough - that sort of thing gets into your head. What's the bit you keep putting off?",
)

ROLE_REPLIES = (
    "Then something has to give. Is it the hours, the people, or the work itself?",
    "That wears you down. What's the worst part of it at the moment?",
    "Fair enough - a job like that takes it out of you. What's the bit that does it?",
    "That's worth taking seriously: what would make the week easier?",
)

CONTENT = re.compile(r"[a-z0-9']+")


def pool(shape):
    if shape == "pile":
        return PILE_REPLIES
    if shape == "role":
        return ROLE_REPLIES
    return JOB_REPLIES


def reads_as_worn(clean, words=None, repaired=""):
    text = " ".join(str(clean or "").lower().split())
    if not text or "?" in text:
        return None
    shape = _shape(text, words)
    if shape is None and repaired and repaired != text:
        shape = _shape(repaired)
    return shape


def _shape(text, words=None):
    words = set(words) if words else set(CONTENT.findall(text))
    if not words:
        return None
    if trouble.someone_elses(words):
        return None
    if trouble.reads_as_trouble(text, words):
        return None
    if trouble.PLEA.search(text):
        return None
    if words & WEATHER:
        return None
    if words & MONEY:
        return None
    for match in PILE.finditer(text):
        if _names_a_job(text):
            return "pile"
    for match in WEAR.finditer(text):
        subject = text[:match.start()]
        if set(CONTENT.findall(subject)) & (trouble.BODY_PART | EXTRA_BODY):
            continue
        if _is_a_role(subject):
            return "role"
        if _names_a_job(subject):
            return "job"
    return None


def _content_words(clause):
    return [word for word in CONTENT.findall(clause)
            if word not in POINTING and word not in A_STRETCH]


def _is_a_role(clause):
    content = _content_words(clause)
    return bool(content) and all(word in ROLE for word in content)


def _names_a_job(clause):
    content = _content_words(clause)
    return bool(content) and not all(word in NOT_A_JOB for word in content)
