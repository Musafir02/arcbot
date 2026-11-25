
import re

from . import fallback

A_FIRST_TIME = re.compile(
    r"\b(?:first time|first one|first ever|first go|first race|first shift|first day|"
    r"never done (?:one|this|it|that) before|never done (?:one|this|it|that)|"
    r"never (?:done|run|given|taught|led|organised|organized|played|performed)\b[^?]*\bbefore|"
    r"never had one|havent done (?:one|this|it) before|haven't done (?:one|this|it) before|"
    r"(?:its|it's|this is) my first|my first time|ive never|i've never|not done one before)\b", re.I)
A_FIRST_FENCED = re.compile(
    r"\b(?:died|death|dying|dead|loss|lost|grief|bereave\w*|funeral|miscarriage|stillborn|"
    r"cancer|hospice|hospital|operation|surgery|diagnos\w*|chemo|baby|babies|pregnan\w*|birth|"
    r"numb|passed away|put to sleep|euthanis\w*)\b", re.I)

A_A_TASK = re.compile(
    r"\b(?:talk|speech|presentation|pitch|demo|interview|viva|defence|defense|panel|"
    r"race|marathon|half marathon|10k|5k|parkrun|triathlon|swim|match|game|final|heat|"
    r"test|exam|driving test|theory test|practical|audition|performance|gig|show|"
    r"shift|first day|day one|lesson|class|course|lecture|seminar|reading|sermon|"
    r"wedding speech|best man|maid of honour|toast|eulogy|chair|chairing|meeting|"
    r"appointment|scan|procedure|surgery|flight|driving lesson|lesson)\b", re.I)


A_FIRST_NAMES_ITS_THING = re.compile(
    r"\b(?:had|eaten|tried|cooked|made|bought|seen|visited|flown|driven|used|caught|owned|"
    r"worn|grown|sold|wrote|read|played|kept|baked|brewed)\s+(?:a|an|the|any|some)\s+\w+", re.I)


def _a_task_they_faced(text, memory):
    if A_A_TASK.search(text):
        return True
    if A_FIRST_NAMES_ITS_THING.search(text):
        return False
    turns = (memory or {}).get("turns") if isinstance(memory, dict) else None
    for turn in reversed(list(turns or [])[-4:]):
        if isinstance(turn, dict) and turn.get("user") and A_A_TASK.search(str(turn["user"])):
            return True
    return False

FIRST_TIME = (
    "The first one is the one you over-prepare for, and that is the right mistake to make. Say it "
    "out loud once, all the way through, to a person or the wall - that is the step people skip "
    "and the one that takes the nerves down. What is the part that worries you most?",
    "Nobody is calm for their first one, and the nerves go in the first two minutes once you are "
    "actually in it. Walk it through out loud once beforehand rather than reading it over again in "
    "your head. What is it you are facing?",
    "Everybody's first is the worst one, and almost nobody does it as badly as they think. Practise "
    "it once, out loud and timed, and know that the beginning is the part to have ready. What would "
    "go wrong if it went wrong?",
)

def reply_for(text, memory=None):
    if not text:
        return None
    low = " ".join(str(text).lower().split())
    if not low or low.endswith("?"):
        return None
    if not A_FIRST_TIME.search(low) or A_FIRST_FENCED.search(low):
        return None
    if not _a_task_they_faced(low, memory or {}):
        return None
    return fallback._choose(FIRST_TIME, memory or {}, low)
