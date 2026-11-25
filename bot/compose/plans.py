import re

TRIP_TOLD = re.compile(
    r"\b(?:going|off|away|flying|fly|flies|travelling|traveling|trip|holiday|hols|flight|"
    r"abroad|visiting|weekend away)\b")
WORK_TOLD = re.compile(
    r"\b(?:new job|job interview|interview|first day|start(?:ing)? (?:work|my new job)|"
    r"back to work|work at|work in|new role|promotion|training day|induction|night shift)\b")
HEALTH_TOLD = re.compile(
    r"\b(dentist|doctors?|gp|surgery|hospital|check-?up|scan|x-?ray|optician|jab|vaccine|"
    r"physio|clinic|antenatal)\b")
MOVE_TOLD = re.compile(
    r"\b(?:moving|move house|moving house|new flat|new house|moving out|house move|"
    r"removal van|packing up|exchanging contracts)\b")
EVENT_TOLD = re.compile(
    r"\b(wedding|getting married|funeral|christening|birthday party|concert|gig|match|"
    r"conference|exam|driving test|course)\b")
PLACE_AND_MONTH = re.compile(
    r"\b([a-z][a-z'\-]{2,})\s+in\s+(?:january|february|march|april|may|june|july|august|"
    r"september|october|november|december|the (?:spring|summer|autumn))\b")
PLAN_KINDS = (
    ("move", MOVE_TOLD),
    ("health", HEALTH_TOLD),
    ("work", WORK_TOLD),
    ("event", EVENT_TOLD),
    ("trip", TRIP_TOLD),
)
A_PLACE_NAMED = re.compile(r"\b(?:to|in|back to|visiting|off to)\s+([a-z][a-z'\-]{2,})\b")
PLAN_NOT_A_PLACE = frozenset("""
about and appointment back bed before be been being birthday business check check-up christening
concert conference course do doctors early exam funeral get gig go going have holiday honeymoon
home hospital interview it its late match me my night party scan see sleep somebody someone test
that the them then there today tomorrow trip wedding work yesterday you
""".split())

WHO_WITH_ME = re.compile(r"\bwho(?:'s|s| is| else| all)?\b[^?]{0,24}\b(?:with|coming|going|"
                         r"travelling|traveling)\b[^?]{0,16}\b(?:me|us|my|our)\b")
WHAT_TIME = re.compile(r"\b(?:what|which)\s+time\b")
TIME_DOING = re.compile(r"\b(?:leave|leaving|set off|get there|be there|arrive|arriving|set out|"
                        r"head off|check in|start|go|be)\b")
WHAT_TO_TAKE = re.compile(r"\b(?:what|anything)\b[^?]{0,34}\b(?:bring|bringing|take|taking|"
                          r"pack|packing|wear|wearing)\b[^?]{0,24}\b(?:with (?:me|us)|for the|"
                          r"on the|for a|to the|for my|for our)\b")
WHAT_FIRST = re.compile(r"\b(?:what|anything|is there anything|what else)\b[^?]{0,44}"
                        r"\b(?:before i (?:go|leave|set off|travel)|before we (?:go|leave|set off|"
                        r"travel)|beforehand|on the day|the day before|when i get there|"
                        r"when we get there|to do before (?:i|we) go|to sort before|"
                        r"to organise before|to organize before)\b")
WHAT_MISSED = re.compile(r"\b(?:anything|what) (?:have|did) i (?:miss|missed)\b[^?]{0,30}"
                         r"\b(?:while|off|away|on (?:holiday|leave)|out of)\b"
                         r"|\bwhile i was (?:off|away|on holiday|on leave)\b"
                         r"|\bcatch up on\b[^?]{0,20}\b(?:while|since|off|back)\b")

ABOUT_THEMSELVES = re.compile(r"\b(?:i|me|my|we|us|our|i'm|im|i've|ive)\b")


def _the_plan_told(memory, clean=""):
    if not isinstance(memory, dict):
        return None
    turns = memory.get("turns") or []
    mine = " ".join(str(clean or "").lower().split())
    behind = 0
    for turn in reversed(turns[-6:]):
        said = " ".join(str(turn.get("user") or "").lower().split())
        if not said or said == mine:
            continue
        behind += 1
        if behind > 3:
            break
        for kind, pattern in PLAN_KINDS:
            found = pattern.search(said)
            if not found:
                continue
            place = ""
            if kind == "trip":
                for named in A_PLACE_NAMED.finditer(said):
                    word = named.group(1)
                    if word not in PLAN_NOT_A_PLACE:
                        place = word
                        break
            word = found.group(1) if found.groups() else ""
            return kind, place, word
        named = PLACE_AND_MONTH.search(said)
        if named and named.group(1) not in PLAN_NOT_A_PLACE:
            return "trip", named.group(1), ""
    return None


def _the_ask(clean):
    if WHAT_MISSED.search(clean):
        return "missed"
    if WHO_WITH_ME.search(clean):
        return "who"
    if WHAT_TIME.search(clean) and TIME_DOING.search(clean):
        return "time"
    if WHAT_TO_TAKE.search(clean):
        return "take"
    if WHAT_FIRST.search(clean):
        return "first"
    return None


def answer_for(text, memory):
    said = " ".join(str(text or "").lower().split())
    if not said:
        return None
    if not ABOUT_THEMSELVES.search(said):
        return None
    ask = _the_ask(said)
    if ask is None:
        return None
    plan = _the_plan_told(memory, said)
    if plan is None:
        return None
    kind, place, word = plan
    return _the_line(ask, kind, place, word)


def _the_line(ask, kind, place, word=""):
    if ask == "who":
        if kind == "health":
            return ("Nobody has to come with you unless you are having something that needs a lift "
                    "home - then ask. Is anyone going with you?")
        if kind == "event":
            return "Check who is named on the invitation or ticket. Who are you going with?"
        if place:
            return ("The booking lists everyone who is travelling to %s on it. Who are you going "
                    "with?" % place.capitalize())
        return "The booking lists everyone who is travelling on it. Who are you going with?"
    if ask == "time":
        if kind == "health":
            where = (" at the %s" % word if word and word not in ("check-up", "scan", "clinic")
                     else " at the surgery")
        elif kind == "work":
            where = " at work"
        elif place:
            where = " in %s" % place.capitalize()
        else:
            where = " there"
        return ("What time do you need to be%s? Work back from the journey, and add half an hour "
                "for the queue." % where)
    if ask == "take":
        if kind == "move":
            return ("Pack one box of the things you need on day one and keep it with you - what's "
                    "top of that list?")
        if place:
            return ("The forecast for %s decides most of the bag, so check it the day before. Will "
                    "you be on your feet most of the day?" % place.capitalize())
        return ("It depends on what you will be doing, more than on the weather: on your feet all "
                "day, or sitting down?")
    if ask == "first":
        if kind == "move":
            return ("Meter readings and a change of address are the two that cost money if they "
                    "slip. Are those done?")
        if kind == "health":
            return ("Write down what you want to ask while you're there - it's easy to forget on "
                    "the day. What's the main thing?")
        if kind == "work":
            return ("Sort the paperwork they asked for and the route there the night before. "
                    "What time are you due in?")
        return "Sort the one thing that has a date on it first. What's already booked?"
    if ask == "missed":
        if kind == "work":
            return ("Ask one person what changed while you were off - that's the whole catch-up. "
                    "Who would you ask?")
        return ("Most of what comes in while you're away sorts itself out. What's the one thing "
                "with a deadline this week?")
    return None
