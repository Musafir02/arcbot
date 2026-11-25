import re

from ..compose import pick

HOURS_KEY = "hours"

FAMILY_NAMES = {
    "nights": "nights",
    "early": "an early start like that",
    "late": "a finish that late",
    "long": "shifts that long",
    "spread": "a week laid out like that",
    "home": "working from home",
}

EASIER_ASK = re.compile(
    r"\b(?:does|do|will|would|is|did)\s+(?:that|it|this|they)\s+(?:ever\s+|eventually\s+)?"
    r"(?:get|gets|be|become|gets)\s+(?:any\s+)?(?:easier|better|any easier)\b"
    r"|\b(?:will|do)\s+i\s+(?:ever\s+)?get (?:used to|over)\s+(?:it|them|that)\b"
    r"|\b(?:it|that|this|they)\s+(?:ever\s+)?gets?\s+(?:any\s+)?easier\b"
    r"|\b(?:does|will) (?:that|it|this) (?:ever )?stop\b", re.I)
STOP_ASK = re.compile(
    r"\b(?:i|we)\s+(?:never|can'?t|cant|don'?t|dont|just can'?t)\s+(?:ever\s+)?"
    r"(?:know when to stop|switch off|stop|wind down|log off)\b"
    r"|\bhow do i (?:switch off|stop|wind down|log off)\b"
    r"|\b(?:hard|impossible) to switch off\b", re.I)
PLAN_ASK = re.compile(
    r"\b(?:its|it is|it'?s|that is)\s+(?:so\s+)?hard to plan\b"
    r"|\b(?:i|we)\s+(?:can'?t|cant|never)\s+plan\b|\bnever know my week\b"
    r"|\bhow do i plan\b|\bimpossible to plan\b", re.I)

EASIER_TAIL = (
    "It does, and the change is in the sleep rather than in the work: {hours} only start to sit "
    "right once the going to bed moves with them, and that takes a week or two rather than a "
    "night.",
    "Yes, in stages. The first fortnight with {hours} is the worst of it, and what is still hard "
    "a month in is worth taking to a doctor, because that part is not the adjustment any more.",
    "It gets easier. The body is not the slow part - the evenings are, and those only settle once "
    "they have a fixed edge at both ends.",
)
STOP_TAIL = (
    "Then put the end on the clock rather than on the work: a time that finishes the day whatever "
    "is still undone, because the work never runs out by itself.",
    "Take the last hour back deliberately. It is easier to protect a slot than a mood, and a day "
    "with no end will take every open minute it is given.",
)
PLAN_TAIL = (
    "Plan less and keep it fixed: two or three things a week that cannot move is all a plan should "
    "hold, and the rest of the week is better left loose.",
    "Keep the sleep and one day off in the same place every week. Those two are what the rest of "
    "the week hangs on, and they hold even when the week moves under them.",
)

KINDS = (("easier", EASIER_ASK, EASIER_TAIL),
         ("stop", STOP_ASK, STOP_TAIL),
         ("plan", PLAN_ASK, PLAN_TAIL))

AWAY = re.compile(
    r"\b(?:die|died|dies|dying|death|dead|kill|killed|suicide|funeral|hospital|ambulance|"
    r"bleeding|blood|chest|breathless|sore|pain|hurts|aching|ill|sick|diagnosed|cancer|"
    r"redundant|sacked|fired|dumped|divorce|miss|miss him|miss her)\b", re.I)
FEELING = re.compile(
    r"\b(?:sad|lonely|alone|awful|terrible|horrible|miserable|hopeless|worthless|hate myself|"
    r"cant cope|can'?t cope|breaking down|crying|anxious|depressed|scared|worried sick)\b", re.I)

MOST = 12
LOOK_BACK = 1


def note(memory, family):
    if not isinstance(memory, dict) or not family:
        return
    turns = memory.get("turns")
    turn = len(turns) if isinstance(turns, list) else 0
    memory[HOURS_KEY] = {"family": str(family), "turn": turn}


def remembered(memory):
    held = memory.get(HOURS_KEY) if isinstance(memory, dict) else None
    if not isinstance(held, dict):
        return None
    turns = memory.get("turns")
    if not isinstance(turns, list):
        return None
    if held.get("turn") != len(turns) - LOOK_BACK:
        return None
    family = str(held.get("family") or "")
    return family if family in FAMILY_NAMES else None


def answer_for(text, memory):
    if not isinstance(text, str):
        return None
    clean = " ".join(text.split())
    if not clean or len(clean.split()) > MOST:
        return None
    if AWAY.search(clean) or FEELING.search(clean):
        return None
    family = remembered(memory)
    if not family:
        return None
    for _kind, pattern, pool in KINDS:
        if not pattern.search(clean):
            continue
        return pick(pool, memory, clean).format(hours=FAMILY_NAMES[family])
    return None
