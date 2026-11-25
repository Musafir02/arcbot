import re

from . import pick
from .fallback_data import BAD_STRETCH_REPLIES

A_DAY_DENIED = re.compile(
    r"\b(?:not|never|hardly|isnt|isn't|wasnt|wasn't|arent|aren't|aint|ain't)\s+"
    r"(?:\w+\s+){0,2}"
    r"(?:the\s+)?(?:best|good|great|nice|fine|brilliant|amazing|alright|lush|smashing)\s+"
    r"(?:day|week|weekend|night|morning|evening|afternoon|shift|start|time)\b")

A_HAD_BETTER = re.compile(
    r"\b(?:ive|i've|weve|we've|i)\s+had\s+better\s+(?:day|days|week|weeks|weekend|weekends|"
    r"night|nights|morning|mornings|evening|evenings|afternoon|shift|shifts)\b")

A_DAY_OWNS_THE_GRADE = re.compile(
    r"(?:\b(?:i|im|i'm|we|we're|things|everything|life|work|today)\b"
    r"|\b(?:my|our)\s+(?:day|week|weekend|night|morning|evening|afternoon|shift|start|time|"
    r"life|mood|year)\b"
    r"|\bthe\s+(?:day|week|weekend|morning|night)\b)"
    r"\s+(?:could|would|can)\s+(?:have\s+been|of\s+been|be\s+going|be)\s+"
    r"(?:a\s+lot\s+|much\s+|alright\s+|ok\s+)?better\b"
    r"|\b(?:could|would)\s+be\s+going\s+better\b")
A_DAY_GRADED_ALONE = re.compile(
    r"^\W*(?:(?:it|so|well|yeah|yea|aye|oh|hi)\s+){0,2}"
    r"(?:could|would|can|might)\s+(?:have\s+been|of\s+been|be\s+going|be)\s+"
    r"(?:a\s+lot\s+|much\s+|alright\s+|ok\s+)?better\b"
    r"(?:\s+(?:tbh|honestly|today|now|so\s+far|though|i\s+guess|i\s+suppose|lately|"
    r"at\s+the\s+moment|right\s+now|this\s+week|this\s+morning|thanks|cheers)\b)*\W*$")

QUESTION_OPENERS = frozenset("""
is isnt isn't was wasnt wasn't are arent aren't do does did will would should could can may might
have has had who what when where why how
""".split())

A_CHEER = re.compile(
    r"\bgood time\b|\bbest of it\b|\bnice one\b|\bpleased\b|\bwhat happened\b|"
    r"\bthe best bit\b|\bhow did the rest of it go\b|\blovely\b|\bhappy for you\b|"
    r"\bgreat news\b|\bwell done\b|\bcongratulat", re.I)
A_SHRUG = re.compile(
    r"\bthanks for telling me\b|\bis there anything you'?d like a hand with\b|"
    r"\bsay more if it helps\b|\bgot it\b|\bnoted\b", re.I)


def reads_as_a_low_day(text):
    clean = " ".join(str(text or "").lower().split())
    if not clean:
        return False
    graded = bool(A_DAY_GRADED_ALONE.search(clean)) or bool(
        (A_DAY_DENIED.search(clean) or A_HAD_BETTER.search(clean)
         or A_DAY_OWNS_THE_GRADE.search(clean))
        and (clean.split() or [""])[0] not in QUESTION_OPENERS)
    return graded


def _may_replace(reply):
    if not reply:
        return False
    from .fallback import is_a_hedge
    if is_a_hedge(reply):
        return True
    if reply.startswith("Noted:"):
        return True
    return bool(A_CHEER.search(reply) or A_SHRUG.search(reply))


def answer_for(text, reply, memory=None):
    if not reads_as_a_low_day(text):
        return None
    if not _may_replace(reply):
        return None
    return pick(BAD_STRETCH_REPLIES, memory if isinstance(memory, dict) else {}, text)
