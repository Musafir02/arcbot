import re


PLAN_ASK = re.compile(
    r"(?:whats? (?:the |our )?plan|what is the plan|"
    r"the plan for (?:the|our|this) (?:day|trip|weekend|evening|visit)|"
    r"what (?:should|shall|do) we do (?:first|next|then)|"
    r"where (?:do|should) we start|whats? the order|"
    r"how (?:should|do|shall) we plan|plan (?:out )?the (?:day|trip|weekend)|"
    r"sort (?:out )?the plan)"
    r"(?=\s*(?:$|[.?!]|(?:then|now|today|tonight|tomorrow|weekend)\b"
    r"|for (?:the|this|our|next|\w+day)\b|on \w+day\b))")

PLAN_PLACE = re.compile(
    r"\b(?:gig|gigs|venue|concert|show|match|game|festival|tour|theatre|cinema|museum|"
    r"exhibition|station|train|flight|airport|coach|trip|day out|weekend away|night out)\b")
PLAN_MEAL = re.compile(r"\b(?:eat|eats|eating|food|meal|dinner|lunch|breakfast|restaurant|"
                       r"table|bite|pub|pizza|curry)\b")
PLAN_BED = re.compile(r"\b(?:stay over|stay the night|staying over|hotel|hotels|bed|room|"
                      r"sleep|sleeping|airbnb|hostel)\b")
PLAN_BOOKED = re.compile(r"\b(?:booked|reserved|sorted|got a table|have a table|already got)\b")
PLAN_TOGETHER = re.compile(r"\b(?:\d+|two|three|four|five|six|seven|eight|several|few|both) "
                           r"of (?:us|them|you)\b")
PLAN_DOORS = re.compile(
    r"\b(?:gig|gigs|venue|concert|show|match|game|festival|tour|theatre|cinema|museum|"
    r"exhibition)\b")

PLAN_QUESTION = re.compile(
    r"^(?:so |ok |okay |and |but |then )*(?:what|why|how|when|where|who|which)\b"
    r"|^(?:so |ok |okay |and |but |then )*(?:can|could|should|shall|do|does|did|is|are|was|were|"
    r"will|would|have|has|am|any)\s+(?:i|you|we|they|he|she|it|there|this|that|one)\b")

PLAN_EMPTY = frozenset("""
hi hello hey ok okay cool nice great thanks thank you yes yeah no nope sure right ah oh hmm
lol haha good fine maybe alright
""".split())


def _a_statement(line):
    said = " ".join(str(line or "").lower().split())
    said = said.strip(" .!,")
    if not said or "?" in said or PLAN_QUESTION.match(said):
        return ""
    words = said.split()
    if len(words) < 2 or len(words) > 14 or set(words) <= PLAN_EMPTY:
        return ""
    return said


def _the_plan_the_thread_holds(memory, ask=""):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    ask = " ".join(str(ask or "").lower().split())
    said = [_a_statement(t.get("user")) for t in turns
            if " ".join(str(t.get("user") or "").lower().split()) != ask]
    said = [one for one in said if one]
    if len(turns) < 3:
        return None, []
    if len(said) < 2:
        return None, []
    thread = " ".join(said)
    parts = sum(bool(one.search(thread)) for one in (PLAN_PLACE, PLAN_MEAL, PLAN_BED,
                                                     PLAN_TOGETHER))
    if parts < 2 or not (PLAN_PLACE.search(thread) or PLAN_BED.search(thread)):
        return None, []
    thing = said[0]
    meal, bed = bool(PLAN_MEAL.search(thread)), bool(PLAN_BED.search(thread))
    booked = bool(PLAN_BOOKED.search(thread))
    settled = []
    for one in reversed(said[1:]):
        if one in settled:
            continue
        settled.append(one)
        if len(settled) == 2:
            break
    settled.reverse()
    order = "the hour that cannot move"
    if meal:
        order += ", then the meal"
    if bed:
        order += ", then the bed"
    book = ("the table and the room" if meal and bed
            else "the table" if meal else "the room" if bed else "the two bookings")
    return thing, settled, order, book, booked


def _quoted_back(settled):
    quoted = ['"%s"' % one for one in settled]
    if len(quoted) == 1:
        return quoted[0]
    if len(quoted) == 2:
        return "%s and %s" % (quoted[0], quoted[1])
    return "%s and %s" % (", ".join(quoted[:-1]), quoted[-1])


def plan_ask_pool(clean, memory=None):
    said = " ".join(str(clean or "").lower().split())
    if not PLAN_ASK.search(said):
        return None
    _plan = _the_plan_the_thread_holds(memory if isinstance(memory, dict) else {}, said)
    if not _plan[1]:
        return None
    thing, settled, order, book, booked = _plan
    named = _quoted_back([thing] + list(settled))
    said_back = named
    left = ("the doors time - the venue's own page has that"
            if PLAN_DOORS.search(" ".join(settled) + " " + thing)
            else "the hour you have to be there - the booking page has that")
    if booked:
        tail = "The one thing that runs out is done already, so the hours are all that is left."
        close = "Fix the hours round it and the day runs itself."
    else:
        tail = "Book %s tonight: the rest is only times." % book
        close = "Get %s settled and the day runs itself." % book
    return (
        "You have told me %s, so the order is %s. %s" % (said_back, order, tail),
        "I have it all: %s. The order is %s, and the one thing left to find is %s."
        % (said_back, order, left),
        "Nothing here needs looking up - you have told me %s, and that is a day out with the"
        " order already in it: %s. %s" % (said_back, order, close),
    )
