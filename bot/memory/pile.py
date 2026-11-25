import re

from ..compose import pick

_A_HAVE = r"(?:i|we)(?:'ve|ve|\s+have)"
_A_FILLER = r"(?:(?:\s+|,\s*)(?:only|just|still|already|now|got|have)){0,3}"
_A_NUMBER = (r"(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|fifteen|"
             r"twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|a hundred|a dozen|"
             r"hundred|thousand)")
AN_AMOUNT_THEY_HAVE = re.compile(
    r"^\W*(?:(?:oh|well|but|and|so|yeah|yeh|yep|no|nah|ok|okay|god|blimey|honestly|honest)"
    r"[,\s]+)*"
    r"(?:i|we)(?:'ve|ve|\s+have)" + _A_FILLER + r"\s+"
    r"(?P<amount>too\s+(?:many|much)|loads|plenty|lots|a\s+lot|tons|hundreds|thousands|millions|dozens|"
    r"(?:about|around|over|nearly|almost)\s+" + _A_NUMBER + r")"
    r"(?:\s+of\s+(?:them|it|those|these|everything))?"
    r"(?:\s+(?P<thing>[a-z][a-z'-]*(?:\s+[a-z][a-z'-]*){0,3}))?"
    r"\W*$", re.I)

A_BACK_REFERENCE = frozenset((
    "", "them", "it", "those", "these", "everything", "of them", "of it", "of those",
    "of these", "of everything",
))

NOT_A_PILE = re.compile(
    r"\b(?:time|on|to\s+do|going\s+on|happening|to\s+say|on\s+my\s+plate|on\s+at\s+work)\b", re.I)

A_DAY = re.compile(
    r"\b(?:today|tonight|last night|yesterday|this morning|this afternoon|this evening|"
    r"at the weekend|this weekend|last weekend|all day|all morning|the other day|done)\b", re.I)

SHORT = 8

A_PILE_TOO_BIG = (
    "Then don't take the whole pile on: the handful that actually matter first, and the rest can "
    "wait until they do.",
    "Start with the ones you actually use and let the rest sit — a pile only gets smaller from "
    "the top. Which of it matters?",
    "That is more than anyone gets through in one go. Which of it would you miss if it went?",
    "Take the shortlist rather than the pile: what are the two or three that really count?",
)


def _the_thing(found):
    return " ".join((found.group("thing") or "").split()).lower()


def reads_the_pile(text, memory=None):
    line = " ".join(str(text or "").split())
    if not line or "?" in line or len(line.split()) > SHORT:
        return False
    found = AN_AMOUNT_THEY_HAVE.match(line)
    if not found:
        return False
    if A_DAY.search(line):
        return False
    thing = _the_thing(found)
    if thing not in A_BACK_REFERENCE:
        return False
    if thing and NOT_A_PILE.search(thing):
        return False
    return True


def reply_for(text, memory=None):
    if not reads_the_pile(text, memory):
        return None
    return pick(A_PILE_TOO_BIG, memory if isinstance(memory, dict) else {}, text)
