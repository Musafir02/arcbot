import random
import re

from ..memory import last_bot

PRIORITY = -999

MY_CARE_ASK = re.compile(
    r"(?<![a-z])(?:what time|when|which time|what hours)\b[^?]{0,40}?\b(?:my|our)\s+"
    r"(?:son|daughter|kid|kids|child|children|boy|girl|little one|baby|niece|nephew|"
    r"grandson|granddaughter|grandchild|grandchildren|childminder|babysitter|"
    r"class|classes|lesson|lessons|course|club|swimming|training|nursery|school)\b"
    r"[^?]{0,30}?\b(?:finish|finishes|start|starts|get out|gets out|break up|breaks up|"
    r"come out|comes out|be done|is done|end|ends|go in|goes in|be picked up|gets picked up|"
    r"get home|gets home|be home|is home|get there|gets there)\b", re.I)
MY_CARE_NOT = re.compile(
    r"\b(?:bus|buses|train|trains|tram|tube|flight|flights|coach|ferry|traffic|motorway|"
    r"road|roads|strike|delayed|cancelled|appointment|appointments|doctor|dentist|hospital|"
    r"physio|clinic|surgery|nurse|pharmacy|chemist|tablets?|medicine|medication|exam|"
    r"test results?|results?)\b", re.I)
THEIR_CLASS = re.compile(
    r"\b(?:class|classes|lesson|lessons|course|club|swimming|training)\b", re.I)
A_CHILD = re.compile(
    r"\b(?:son|daughter|kid|kids|child|children|boy|girl|little one|baby|niece|nephew|"
    r"grandson|granddaughter|grandchild|grandchildren|childminder|babysitter)\b", re.I)

SCHOOL_LINES = (
    "A school day is usually the same length every day of the week, so the finish time they gave "
    "you in September still holds unless it is the last day of term, an inset day or a trip. The "
    "school office, its app or the newsletter has this term's version; give me the times and how "
    "long the journey takes and I'll work out when you need to set off.",
    "The times are set by the school or club, not by anything I can look up, but they rarely move "
    "inside a term - it is the last day of term, inset days and trips that shift them. Their "
    "office will tell you in one call and the app you sign them in on has the same; hand me the "
    "times once you have them and I'll plan the pick-up around the rest of your day.",
    "Those hours belong to the school or club, so I can't know this week's, but a school day holds "
    "steady through a term apart from the last day of it and any inset day - and those are on the "
    "school's own calendar. Tell me the finish time and the trip and the rest is arithmetic I can "
    "do with you.",
)
CLASS_LINES = (
    "A class time is set by whoever runs the course and it can move week to week - a new tutor, a "
    "session off, a room change - so the timetable you were given is the starting point rather "
    "than the answer. The provider's app, email or the notice on the door carries this week's; "
    "tell me the times and what you're fitting around them and I'll plan it with you.",
    "I can't see your timetable from here. What I can say is that classes move more often than "
    "people expect - a session cancelled, a tutor changed - and it is the provider's own message "
    "that carries the change. Bring me the times and I'll do the planning around them.",
    "The provider keeps that timetable, not me, and it changes: a bank holiday, a cancelled "
    "session, a new room. Their app or the email they send is where this week's version sits; "
    "give me the times and I'll work out the rest of your day around them.",
)


def _clean(text):
    return " ".join(str(text or "").lower().split())


def _choose(pool, memory, said=""):
    last = str(last_bot(memory) or "").strip()
    fresh = [line for line in pool if line != last]
    options = fresh or list(pool)
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    seed = len(turns) * 7919 + sum(ord(c) for c in str(said or "").lower())
    return random.Random(seed).choice(options)


def respond(text, memory):
    said = _clean(text)
    if not said:
        return None
    if MY_CARE_NOT.search(said):
        return None
    if not MY_CARE_ASK.search(said):
        return None
    pool = CLASS_LINES if THEIR_CLASS.search(said) and not A_CHILD.search(said) else SCHOOL_LINES
    return _choose(pool, memory, said)
