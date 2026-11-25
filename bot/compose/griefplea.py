
import re

from . import fallback, loss

TAIL_SO_FAR = '(?:\\s+(?:now|next|then|though|really|at\\s+all|anymore|today|please))*\\s*\\?*\\s*$'

A_PLEA_WITH_NOTHING_IN_IT = re.compile(
    r"^(?:(?:ok|okay|so|right|and|but|well|please|now|honestly|yeah)\s+)*"
    r"(?:"
    r"(?:any\s+)?(?:ideas?|thoughts?|advice|suggestions?|tips?|help)"
    r"\s*(?:please|then|for me)?\s*\?*\s*$"
    r"|what\s+(?:do|would|should)\s+(?:you|i)\s+(?:think|do|say|suggest)" + TAIL_SO_FAR +
    r"|(?:i\s+)?(?:really\s+|just\s+)?(?:dont|don'?t|do not)\s+know\s+what\s+to\s+do"
    + TAIL_SO_FAR +
    r"|(?:im|i'?m|i\s+feel|i\s+am)\s+(?:so\s+|totally\s+|a\s+bit\s+|completely\s+)?lost"
    + TAIL_SO_FAR +
    r"|(?:where\s+do\s+i\s+(?:even\s+)?start|(?:i\s+)?(?:dont|don'?t|do not)\s+know\s+where"
    r"\s+to\s+start)" + TAIL_SO_FAR +
    r"|(?:not\s+sure|no\s+idea)\s+what\s+to\s+do" + TAIL_SO_FAR +
    r")", re.I)

NOTHING_OF_ITS_OWN = (fallback.NEUTRAL, fallback.UNKNOWN, fallback.TIPS_LINES)


def _said(text):
    return " ".join(str(text or "").lower().split())


def reply_for(text, reply, memory):
    said = _said(text)
    if not said or not A_PLEA_WITH_NOTHING_IN_IT.match(said):
        return None
    if not isinstance(memory, dict) or not str(reply or "").strip():
        return None
    if not fallback._in_a_pool(reply, NOTHING_OF_ITS_OWN):
        return None
    if not loss.continues(memory):
        return None
    pool = loss.GETTING_THROUGH_REPLIES
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    already = set(str(turn.get("bot") or "") for turn in turns)
    fresh = [line for line in pool if line not in already] or list(pool)
    return fallback.pick(fresh, memory.get("understood") or {}, said)
