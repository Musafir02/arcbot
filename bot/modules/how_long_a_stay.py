import re

from ..compose import pick

PRIORITY = 1050

STAY = re.compile(
    r"\b(?:coming|comes|came|coming over|coming round|getting here|arriving|arrives|visiting)\b"
    r"[^.!?]{0,40}?\b(?:stay|staying|stays|visit|to us|over|round|for (?:the )?weekend|"
    r"for \w+ (?:days|nights|weeks))\b"
    r"|\b(?:is|are|was|were)\s+(?:coming\s+)?(?:to\s+)?staying\b"
    r"|\bstaying\s+(?:with\s+us|here|over|for)\b"
    r"|\bstopping\s+(?:with\s+us|over|here)\b"
    r"|\b(?:a|the)\s+visit\b",
    re.I)

A_LENGTH = re.compile(
    r"\bfor\s+(?:about\s+|just\s+|only\s+)?"
    r"(\d+|a|an|one|two|three|four|five|six|seven|eight|nine|ten|a\s+few|a\s+couple\s+of)"
    r"\s*(day|days|night|nights|week|weeks)\b"
    r"|\b(?:for\s+)?(?:the|this|that|next|at\s+the)\s+weekend\b"
    r"|\b(?:a|one)\s+week\b"
    r"|\b(?:a|one)\s+fortnight\b",
    re.I)

A_LENGTH_SAID = re.compile(
    r"\b(?:\d+|two|three|four|five|six|seven|eight|nine|ten|twenty)\s*(?:full|whole|more|extra)?\s*"
    r"(?:days?|nights?|weeks?|hours?|minutes?)\b"
    r"|\ba\s+(?:week|fortnight|month)\b|\bweekend\b|\bfortnight\b",
    re.I)

ASKS_A_LENGTH = re.compile(
    r"\bhow\s+long\b|\bhow\s+many\s+(?:days|nights|weeks)\b|\bhow\s+much\s+time\b",
    re.I)

GENERIC = frozenset("""
about actually again all also and an any are around as at be been before both but by can could do
does doing else even ever exactly for from get getting go going got had has have he her here hers
him his how i if in into is it its just keep know like long may me might more much my nearly no
not now of off on once one only or our ours out over own please really right said say she should
so some still take takes taking than that the their theirs them then there these they thing this
those to too up us very want was way we well were what when where which while who why will with
would you your yours sorted stuff bit bits stay stays staying visit visiting long weekend days
nights
""".split())

A_LENGTH_REPLY = (
    "{length} is a comfortable stay: one shared outing a day is enough for that long, and keep "
    "one evening back for yourself.",
    "For {length}, plan one outing a day rather than a schedule - and leave one evening free.",
    "{length} gives you room for an outing a day. The rest of the card is what matters more: the "
    "bed and the meal times.",
)

ADVICE = (
    "Three or four days is the sweet spot for a first stay: long enough to settle in, short "
    "enough that nobody runs out of things to say.",
    "A weekend to a week. Past a week, plan one evening apart or the visit starts to feel like a "
    "duty for both of you.",
    "Up to a week is the usual answer - long enough to settle in, and the length where an outing "
    "a day and one evening kept back still feel like a visit.",
)

ASKS_ADVICE = re.compile(
    r"\bhow\s+long\s+(?:should|do\s+you\s+think|would\s+you|is\s+(?:it\s+)?(?:right|normal))\b"
    r"|\bhow\s+many\s+(?:days|nights)\s+should\b"
    r"|\bhow\s+long\s+(?:is\s+)?(?:too\s+long|long\s+enough)\b",
    re.I)

NO_LENGTH = (
    "You have not said how long they are staying, and that is what decides it: a weekend is one "
    "outing, a week is three or four. How long is it?",
    "How long is the stay? A weekend wants one thing planned and a week wants two or three, so "
    "the answer changes with it.",
    "How long are they with you for? Tell me and I will say how much to plan - the bed and the "
    "meal times are the same either way.",
)


def _words(text):
    return re.findall(r"[a-z0-9']+", str(text or "").lower())


def _the_stay(memory):
    for turn in reversed(memory.get("turns") or []):
        if not isinstance(turn, dict):
            continue
        said = str(turn.get("user") or "")
        if STAY.search(said):
            return said
    return ""


def _the_length_said(memory):
    found = A_LENGTH.search(_the_stay(memory))
    if not found:
        return ""
    if found.group(1):
        return ("%s %s" % (found.group(1), found.group(2))).lower()
    return found.group(0).strip().lower()


def _the_opening(reply):
    text = str(reply or "")
    cut = re.search(r"[.!?](?:\s|$)", text)
    return text[:cut.end()] if cut else text


def _the_last_answer(memory):
    for turn in reversed(memory.get("turns") or []):
        if not isinstance(turn, dict):
            continue
        reply = str(turn.get("bot") or "")
        if reply:
            return reply, str(turn.get("module") or "")
    return "", ""


def _a_subject_of_its_own(text):
    for word in _words(text):
        if word in GENERIC or len(word) <= 2:
            continue
        if word.isdigit():
            continue
        return True
    return False


def respond(text, memory):
    if not isinstance(memory, dict) or not memory.get("turns"):
        return None
    if not ASKS_A_LENGTH.search(str(text or "")):
        return None
    if _a_subject_of_its_own(text):
        return None
    stay = _the_stay(memory)
    if not stay:
        return None
    last, module = _the_last_answer(memory)
    if not last or module != "answers":
        return None
    if A_LENGTH_SAID.search(_the_opening(last)):
        return None
    length = _the_length_said(memory)
    if length:
        said = pick(A_LENGTH_REPLY, memory, seed_text=length).format(length=length)
        return said[:1].upper() + said[1:]
    if ASKS_ADVICE.search(str(text or "")):
        return pick(ADVICE, memory, seed_text=stay)
    return pick(NO_LENGTH, memory, seed_text=stay)
