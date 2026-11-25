import re

from . import fallback
from . import goodnews

A_MOVE = re.compile(
    r"\b(?:i|we|they|he|she|im|i'm|we're|were|were)\s*(?:'m|'re|am|are|is)?\s*"
    r"(?:just\s+|finally\s+|now\s+|soon\s+|actually\s+|been\s+|have\s+|had\s+)?"
    r"mov(?:e|ed|ing)\s+"
    r"(?:out|houses?|household|flats?|home|abroad|in\b|into\b|back\s+(?:in\s+)?with|away)",
    re.I)
A_MOVE_NOUN = re.compile(
    r"\b(?:our|my|the)\s+move\s+(?:is|to|next|soon|coming|happens|happening)\b", re.I)
GLAD = re.compile(
    r"\b(?:first\s+(?:flat|house|home|place)|our\s+own\s+(?:flat|house|place)|"
    r"dream|finally|cant\s+wait|can'?t\s+wait|so\s+excited|excited\s+to|looking\s+forward|"
    r"got\s+the\s+keys|we\s+got\s+it|brand\s+new|bigger|nicer|better\s+place|closer\s+to|"
    r"new\s+job|promotion|girlfriend|boyfriend|partner|fiance|fiancee|husband|wife)\b", re.I)
NOT_GLAD = re.compile(
    r"\b(?:evict\w*|kicked\s+out|thrown\s+out|have\s+to|havent\s+got\s+a\s+choice|"
    r"no\s+choice|break\s*up|broke\s+up|divorce|separat\w*|lost\s+my\s+job|rent\s+(?:rise|went\s+up)|"
    r"dreading|cant\s+afford|can'?t\s+afford|sad|gutted|hate|awful|nightmare|"
    r"landlord|selling\s+up|sold\s+the\s+(?:flat|house)|for\s+work|because\s+of\s+work)\b", re.I)
ADVICE = re.compile(
    r"\b(?:should\s+(?:i|we)|shall\s+(?:i|we)|do\s+you\s+think|is\s+it\s+worth|"
    r"how\s+do\s+(?:i|we)|what\s+should|any\s+(?:advice|tips))\b", re.I)
ITS_OWN_NEWS = re.compile(
    r"\b(?:abroad|overseas|another\s+country|to\s+(?:spain|france|australia|canada|america|"
    r"portugal|italy|germany|ireland|scotland|wales)|"
    r"(?:in|into)\s+with\s+(?:my|her|his|our)\s+(?:girlfriend|boyfriend|partner|fiance|fiancee|"
    r"husband|wife|mum|mother|dad|father|parents))\b", re.I)

MANY = (
    "Big thing to have ahead of you. Where to, and are you glad to be going?",
    "That's a big change. Is it a move you wanted, or one that has to happen?",
    "Moving is a lot of work. Where are you off to, and how are you feeling about it?",
    "A move is never just a move. Where to, and is it a good thing for you?",
)


def reads_as_a_move(text):
    clean = " ".join(str(text or "").lower().split())
    if not clean or "?" in clean:
        return False
    if not (A_MOVE.search(clean) or A_MOVE_NOUN.search(clean)):
        return False
    if GLAD.search(clean) or ITS_OWN_NEWS.search(clean):
        return False
    if NOT_GLAD.search(clean) or ADVICE.search(clean):
        return False
    return True


def reads_as_a_move_cheered(text):
    clean = " ".join(str(text or "").lower().split())
    if not reads_as_a_move(clean):
        return False
    try:
        return bool(goodnews.ahead_of_now(clean))
    except Exception:
        return False


def reply_for(text, memory=None):
    if not reads_as_a_move_cheered(text):
        return None
    try:
        return fallback._choose(MANY, memory or {}, " ".join(str(text or "").lower().split()))
    except Exception:
        return None
