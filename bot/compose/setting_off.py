import re

ASK_SHAPE = re.compile(
    r"(?<![a-z])(?:(?:what|which)\s+time|when|how\s+early|how\s+late)\s+"
    r"(?:should|shall|do|does|did|will|would|must|can|could|need|have|am|are|is)\b"
    r"|(?<![a-z])(?:early|late)\s+enough\b"
    r"|(?<![a-z])(?:best|better|ideal|sensible|wisest)\s+time\b")
ASK_LATEST = re.compile(
    r"(?<![a-z])(?:(?:what'?s|what\s+is|when'?s|which\s+is)\s+the\s+latest"
    r"|latest\s+(?:time\s+)?(?:i|we)\s+(?:can|could|should|would)\b)")
FIRST_PERSON = re.compile(r"(?<![a-z])(?:i|we|us|im|i'm|ive|i've|ill|i'll|well|we'll)(?![a-z])")
THEIR_OWN_CHOICE = re.compile(
    r"(?<![a-z])(?:best|better|ideal|sensible|wisest|reasonable|(?:early|late)\s+enough)(?![a-z])")
SOMEBODY_ELSE = re.compile(
    r"(?<![a-z])(?:he|she|they|him|her|hers|his|them|their|mum|dad|mother|father|son|daughter|"
    r"brother|sister|partner|husband|wife|friend|boss|colleague)(?![a-z])")
SETTING_OFF = ("leave", "leaves", "leaving", "set off", "setting off", "set out", "setting out",
               "head off", "heading off", "get going", "getting going", "start out",
               "starting out", "get there", "getting there", "be there", "arrive", "arriving",
               "get to the", "get to my", "get to work", "getting to the", "getting to my",
               "getting to work")

NOT_A_JOURNEY = ("leave him", "leave her", "leave them", "leave my husband", "leave my wife",
                 "leave my partner", "leave my boyfriend", "leave my girlfriend", "leave my job",
                 "leave my marriage", "leave the country", "leave home for good", "leave work",
                 "leave school", "leave college", "leave uni", "leave the army", "leave it",
                 "leave that", "leave the light", "leave the lights", "leave the heating",
                 "leave the oven", "leave the door", "leave the window", "leave the keys",
                 "leave the car", "leave a message", "leave a review", "leave a tip",
                 "leave feedback", "leave a comment", "leave the dishes", "leave the washing",
                 "leave for good",
                 "leave the bin", "leave the bins", "leave the rubbish", "leave the dog",
                 "leave the cat", "leave the kids", "leave the baby", "leave me", "leave us",
                 "leave time", "leave it to")

SET_OFF_A_THING = re.compile(
    r"set(?:ting)?\s+off\s+(?:the|a|an|my|our)\s+(?:alarm|alarms|firework|fireworks|sprinkler|"
    r"sprinklers|flare|detector|trigger|siren|airbag|extinguisher|smoke|bomb)\b")

THEIR_TIMETABLE = re.compile(
    r"(?<![a-z])(?:does|do|did|will|would)\s+(?:the|my|our|your|his|her|their|this|that)\s+"
    r"(?:bus|buses|train|trains|tram|trams|tube|ferry|boat|ship|plane|flight|flights|coach|"
    r"coaches|match|game|film|show|class|lesson|appointment|shift|service|services)\b")

A_TIME_GIVEN = re.compile(
    r"(?<![a-z0-9])(?:at|by|for|before|until|till)\s+\d{1,2}(?::\d\d)?(?:\s*(?:am|pm|a\.m|p\.m))?"
    r"(?![a-z0-9])"
    r"|(?<![a-z0-9])\d{1,2}(?::\d\d)?\s*(?:am|pm|a\.m|p\.m)(?![a-z])", re.I)

THE_HOUR_IS_FIXED = re.compile(
    r"(?<![a-z])(?:have\s+to\s+be|need\s+to\s+be|got\s+to\s+be|due|starts?|begins?|booked|"
    r"meeting|appointment|interview|flight|ceremony|table|class|shift|lesson|course|visit|"
    r"delivery|viewing)\b")

A_DESTINATION = re.compile(
    r"(?<![a-z])(?:to|for|into|towards|toward)\s+(?:the\s+|a\s+|an\s+|my\s+|our\s+)?"
    r"(?!be\b|do\b|go\b|get\b|set\b|head\b|leave\b|arrive\b|make\b|see\b|take\b|find\b|"
    r"know\b|come\b|there\b|here\b|it\b|them\b|him\b|her\b|us\b|me\b|you\b)"
    r"[a-z][a-z'\-]*(?![a-z])")

POINTERS = ("searching for it will turn up", "a search should sort you out",
            "i don't know enough to answer that", "that's beyond what i know",
            "can't check live times", "timetables and listings change by the hour",
            "the operator's app", "the operator's or the venue's own app",
            "times like that i can't see", "put the journey into",
            "i'd rather not guess", "a quick search online will get you",
            "that was the whole of my answer", "that is all of what i know on it",
            "that is everything i have on that one", "that's the lot i have on that one",
            "that's most of what i know on it",
            "no strong view on that one")

NEEDS_THE_HOUR = (
    "Work back from the hour you have to be there, not forward from now: a journey planner for that "
    "time of day gives the journey, then ten minutes on top for parking and finding the door, and "
    "that is when to set off. I can't see today's traffic or the timetables from here - the planner "
    "or the operator's app has them, live on the morning. What time do you have to be there?",
    "The hour you have to be there is the bit that decides it, and the journey a planner gives for "
    "that time of day is the rest, plus ten minutes for parking and getting in. Today's roads and "
    "delays are the one thing nothing here can see - check the planner just before you go. What "
    "time is it you need to be there?",
)

THE_HOUR_IS_KNOWN = (
    "Work back from that hour: a journey planner for that time of day gives the journey and the "
    "traffic so far, and ten minutes on top covers parking and the walk in. Look at the planner "
    "again just before you go, because that is when a closure or a cancellation is real.",
    "Take the hour you have to be there, take the journey a planner gives for that time of day off "
    "it, and set off ten minutes earlier than that for parking and finding the door. The live part "
    "- an accident, a cancelled train - is the planner's or the operator's app's on the morning.",
)

THE_HOUR_THEY_SAID = (
    "You said %s, so that is the hour to work back from: a journey planner for that time of day gives "
    "the journey, ten minutes on top covers parking and the walk in, and that is when to set off. "
    "Look at the planner again on the morning, because that is when a closure or a delay is real.",
    "Work back from %s: the planner's journey for that time of day, plus ten minutes for parking and "
    "finding the door, taken off it. The live part - a crash, a cancelled train - is only in the "
    "planner or the operator's app on the day.",
)

A_PLACE_NAMED = (
    "I can't see today's roads or trains from here, so the journey part has to come off a planner - "
    "but the working out is the same either way: the hour you have to be there, minus the journey "
    "for that time of day, minus ten minutes for parking and the walk in. Check the planner on the "
    "morning, when the traffic is real.",
    "Nobody here knows what that journey takes today; a journey planner does, and it knows the "
    "traffic with it. Work back from the hour you have to be there, allow ten minutes for parking "
    "and getting in, and look at the planner again before you set off.",
)


def _the_hour_already_said(text, memory):
    turns = [t for t in (memory or {}).get("turns") or [] if isinstance(t, dict)]
    for turn in reversed(turns[-2:]):
        said = " ".join(str(turn.get("user") or "").lower().split())
        if not said or not THE_HOUR_IS_FIXED.search(said):
            continue
        found = A_TIME_GIVEN.search(said)
        if not found:
            continue
        hour = re.sub(r"^(?:at|by|for|before|until|till)\s+", "", found.group(0).strip())
        return hour
    return ""


def is_a_pointer(reply):
    said = str(reply or "").lower()
    return any(shape in said for shape in POINTERS)


def reads_it(text):
    said = " ".join(str(text or "").lower().split())
    if not said:
        return False
    if not (ASK_SHAPE.search(said) or ASK_LATEST.search(said)):
        return False
    if not (FIRST_PERSON.search(said)
            or (THEIR_OWN_CHOICE.search(said) and not SOMEBODY_ELSE.search(said))):
        return False
    if not any(verb in said for verb in SETTING_OFF):
        return False
    if any(fence in said for fence in NOT_A_JOURNEY):
        return False
    if SET_OFF_A_THING.search(said):
        return False
    if THEIR_TIMETABLE.search(said):
        return False
    return True


def _choose(pool, memory):
    turns = (memory or {}).get("turns") or []
    last = ""
    if turns and isinstance(turns[-1], dict):
        last = str(turns[-1].get("bot") or "")
    for line in pool:
        if not last or line[:30] not in last:
            return line
    return pool[0]


def answer_for(text, memory=None):
    if not reads_it(text):
        return None
    said = " ".join(str(text or "").lower().split())
    if A_TIME_GIVEN.search(said):
        return _choose(THE_HOUR_IS_KNOWN, memory)
    hour = _the_hour_already_said(text, memory)
    if hour:
        return _choose(tuple(line % hour for line in THE_HOUR_THEY_SAID), memory)
    if A_DESTINATION.search(said):
        return _choose(A_PLACE_NAMED, memory)
    return _choose(NEEDS_THE_HOUR, memory)
