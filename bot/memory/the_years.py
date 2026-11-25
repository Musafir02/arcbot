import re

from ..compose import pick
from .passing_the_time import _the_chat_is_heavy

_FORGETTING = re.compile(
    r"\b(?:forget|forgets|forgetting|forgetful|forgetfulness|forgot|forgotten)\b", re.I)

_TREATMENT = re.compile(
    r"\b(?:chemo|chemotherapy|radiotherapy|cancer|tumour|tumor|surgery|operation|treatment|"
    r"diagnosis|diagnosed|recovering|recovery|hospital|illness|condition)\b|\bafter my\b", re.I)
_OWN_SUBJECT = re.compile(
    r"\b(?:hair|grey|gray|greying|graying|teeth|dentures|hearing|glasses|wrinkles?|skin)\b",
    re.I)
_DISLIKE = re.compile(
    r"\b(?:hate|hates|hating|can't stand|cant stand|fed up|sick of)\b", re.I)

_LIMIT = 16

_FEELING = re.compile(
    r"\b(?:"
    r"feel(?:ing|s|ing)?\s+(?:so\s+|really\s+|quite\s+|very\s+|a bit\s+|pretty\s+)?"
    r"(?:old|ancient|past it|my age|like an old (?:man|woman|person)|like a pensioner|"
    r"about (?:90|100|eighty|ninety))\b"
    r"|feeling (?:old|ancient|my age)\b"
    r"|past it\b"
    r"|getting old\b|growing old\b|getting on a bit\b"
    r"|too old for (?:this|that|it|all this)\b"
    r"|not (?:young|getting) (?:any more|anymore)\b"
    r"|not (?:as|so) (?:young|fit|quick|strong) as (?:i|we)\b"
    r"|(?:i'?m|i am|im|i feel|i'?m feeling|i feel like i'?m)\s+(?:a bit\s+|a little\s+)?"
    r"over the hill\b"
    r"|feel(?:ing)?\s+(?:like\s+)?(?:a bit\s+)?(?:past|passed) it\b"
    r"|\b(?:im|i'?m|i am)\s+getting on\b"
    r"(?=\s*(?:$|[.,!?]|now\b|these days\b|in years\b|a bit\b))"
    r"|(?:the years?|age) (?:are |is )?(?:catching up|creeping up)\b"
    r"|feel(?:ing)?\s+(?:\d\d|like (?:i'?m |i am )?\d\d|ninety|eighty|seventy)\b"
    r"|(?:my )?(?:body|knees|back) (?:is|are) (?:letting me down|falling apart)\b"
    r")", re.I)
_SELF = re.compile(r"\b(?:i|im|i'm|iam|i am|me|my|mine)\b", re.I)
_OTHER = re.compile(
    r"\b(?:my (?:mum|dad|mother|father|gran|nan|grandad|grandma|grandpa|husband|wife|partner|"
    r"son|daughter|sister|brother|friend|boss|neighbour)|he|she|they|them|his|her|their)\b", re.I)
_BODY_CLAIM = re.compile(
    r"\b(?:knees?|hips?|back|shoulders?|joints?|wrists?|ankles?|feet|hands?|neck|spine)\b"
    r".{0,24}\b(?:hurt|hurts|aching|aches|stiff|sore|clicking|giving way)\b", re.I)
_ASK_START = re.compile(
    r"^\s*(?:is|are|was|were|will|would|shall|should|can|could|do|does|did|when|what|how|why|"
    r"where|who|any)\b", re.I)
_AGE = re.compile(
    r"\b(?:turning|turn|turned|hitting|hitting|becoming|40|50|60|70|80|ninety|forty|fifty|sixty|"
    r"seventy|eighty)\b", re.I)
_BIRTHDAY = re.compile(
    r"\b(?:turning|turn|hitting|(?:am|im|i'm)\s+(?:going to be)?)\s+"
    r"(?:\d\d|forty|fifty|sixty|seventy|eighty|ninety)\b"
    r"|\b\d\d?\s+(?:next|this|in|last)\s+(?:week|month|year|monday|tuesday|wednesday|thursday|"
    r"friday|saturday|sunday|january|february|march|april|may|june|july|august|september|"
    r"october|november|december)\b", re.I)

OLD_LINES = (
    "It is mostly the body sending invoices. What is it that made you feel it today?",
    "That is usually one bad night or one bad morning rather than an age. What set it off?",
    "Some days the body reports in and everything creaks. What is yours doing at the moment?",
    "Old is a number that only feels heavy on some days. What brought it on today?",
    "I would not take one bad day as a verdict. What has been hard work lately?",
    "Everything hurts and nothing is where you left it. What is the worst of it just now?",
)
PAST_IT_LINES = (
    "Past it at what, though? Say the thing you have decided you cannot do and we will look at it.",
    "I would want to know which thing has gone past you. What is it?",
    "That is a hard thing to decide about yourself. What is it that has started to feel beyond you?",
    "Give me the thing it is about - a job, a walk, a hobby - and we can see if it really has.",
)
TOO_OLD_LINES = (
    "Too old for it, or just tired of it? What is the thing that has got too much?",
    "There is a difference between too old and had enough. Which is it?",
    "Then do it your own way or not at all. What is it that has gone past the point of being fun?",
)
MY_AGE_LINES = (
    "Some days the body reports in and the rest of us just listen. What is doing the reporting?",
    "A day that feels its age usually had something in it. What has yours had?",
    "Then today is a slower one. What is on it?",
)
BIRTHDAY_LINES = (
    "{turn} - a birthday makes everybody take stock, and that is all this usually is. "
    "What are you dreading about it?",
    "The birthday is the loud part; the feeling is usually something else. What is behind it?",
    "Nothing changes overnight at {turn}. What have you started noticing?",
    "Everybody does this around a birthday. What would you want the next year to look like?",
)
COMPARISON_LINES = (
    "That is other people getting younger rather than you getting old. Who were you looking at?",
    "The world does look younger from here. What was it that made you notice?",
    "Everybody under thirty starts to look like a child at some point. What brought it on?",
)


def _the_turn(clean):
    found = _BIRTHDAY.search(clean)
    if not found:
        return None
    return " ".join(found.group(0).split())


def reply(text, memory):
    clean = " ".join(str(text or "").replace("\u2019", "'").split())
    if not clean or len(clean.split()) > _LIMIT:
        return None
    if "?" in clean or _ASK_START.match(clean):
        return None
    if not _FEELING.search(clean):
        return None
    said = bool(_SELF.search(clean)) or bool(
        re.match(r"^\W*(?:the years|it is|its|age)\b", clean, re.I))
    if not said or _OTHER.search(clean) or _BODY_CLAIM.search(clean):
        return None
    if _FORGETTING.search(clean):
        return None
    if _TREATMENT.search(clean) or _OWN_SUBJECT.search(clean) or _DISLIKE.search(clean):
        return None
    if _the_chat_is_heavy(memory):
        return None
    seed = str(text or "")
    turn = _the_turn(clean)
    if turn:
        turn = turn[0].upper() + turn[1:]
    if turn:
        pool = tuple(line.replace("{turn}", turn) for line in BIRTHDAY_LINES)
        return pick(pool, memory, seed_text=seed)
    if re.search(r"\b(?:past|passed) it\b|\bover the hill\b", clean, re.I):
        return pick(PAST_IT_LINES, memory, seed_text=seed)
    if re.search(r"\btoo old\b", clean, re.I):
        return pick(TOO_OLD_LINES, memory, seed_text=seed)
    if re.search(r"look at|young people|teenagers|schoolchildren|all these kids", clean,
                 re.I):
        return pick(COMPARISON_LINES, memory, seed_text=seed)
    if re.search(r"\bmy age\b", clean, re.I):
        return pick(MY_AGE_LINES, memory, seed_text=seed)
    return pick(OLD_LINES, memory, seed_text=seed)
