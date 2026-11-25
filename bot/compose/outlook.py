
import re

_WORDS = re.compile(r"[a-z0-9']+")

_POINTS_AT_THE_THREAD = re.compile(
    r"^\W*(?:and\s+|but\s+|so\s+|ok(?:ay)?\s+|also\s+)?"
    r"(?:does|do|did|will|would|can|could|is|are|am|was|were|has|have|should)\s+"
    r"(?:it|its|it'?s|that|this|them|they|things|i|we|life|everything)\b"
    r"|^\W*(?:what\s+(?:happens|happened|now)|where\s+does\s+that|how\s+long\s+(?:till|until|"
    r"before|does|will))")

_OUTCOME = re.compile(
    r"\b(?:better|worse|normal|again|ok|okay|alright|fine|same|improve|improves|change|changes|"
    r"always|ever|forever|go(?:es)?\s+away|get\s+over|recover|heals?|happens?|now|tomorrow|"
    r"feel\s+like\s+this)\b"
    r"|\b(?:stop|stops|stopped|end|ends|pass|passes|ease|eases|last|lasts)\b\s*"
    r"(?:soon|now|altogether|completely|on\s+its\s+own|eventually|in\s+a\s+day\s+or\s+two)?"
    r"\s*[?.!]*$")

try:
    from .fallback_data import BODY_PARTS, HEALTH_WORDS, SYMPTOM_WORDS
    _THE_THING_ITSELF = frozenset(BODY_PARTS | HEALTH_WORDS | SYMPTOM_WORDS)
except Exception:
    _THE_THING_ITSELF = frozenset()

LINES_IN_CRISIS = (
    "I can't promise how it goes from here, and anyone who says they can is guessing. What is in "
    "your hands is the line - people ring it again the same day, and that is what it is for. Ring "
    "it if it turns, and tell me what the next hour looks like.",
    "Nobody can put a shape on that from here, and I won't pretend to. The part you can act on is "
    "the call: they have heard all of this before, at three in the morning included, so use it "
    "again the moment it gets heavier.",
    "That is not a thing I can answer for you, and it does not need an answer tonight. The number "
    "does not run out - ring it again if it turns, and say what today is like for you.",
)

LINES_IN_AN_EMERGENCY = (
    "I can't promise how it goes, and nobody can from here. The thing that changes it is the call "
    "in the answer above - if you have not rung yet, ring now and stay on the line with them; they "
    "can hear what I can't.",
    "Nobody can say how it goes, and the part you can act on is the call you were told to make. If "
    "you have made it, do what they say over anything I could add; if not, make it before anything "
    "else.",
    "That is not a thing I can answer for you, and my guess would be worth less than the one in the "
    "answer above. The call is what stands between you and how it goes - everything else waits.",
)

LINES_WITH_HELP = (
    "I can't promise how it goes, and nobody honestly can. What they told you on that call is "
    "worth more than anything I could add, so stay with it - and ring again if it turns rather "
    "than waiting it out.",
    "Nobody can say how it goes from here, and the part in your hands is what the line told you to "
    "do next. Do that, and ring them back if anything changes.",
    "That is not something I can answer for you, and it does not need an answer tonight. Somebody "
    "who can help knows about it now - keep that number open and use it again if it gets heavier.",
)

LINES_WHEN_SOMEONE_IS_HURTING_YOU = (
    "I can't promise how it goes, and nobody honestly can - not from a line of chat. What I can say "
    "is that none of it is your fault, and the number in the answer above is for exactly the "
    "question you just asked; they hear it all day.",
    "Nobody can say how it goes, and you should not have to work it out alone. The line above can "
    "talk it through with you - what you want, not only what is happening - and that is worth more "
    "than my guess.",
    "I can't say how it goes from here, and I would be making it up if I tried. What is in your "
    "hands is the call: they will not tell you to leave or to stay, and asking costs nothing.",
)

def points_at_the_thread(text):
    clean = " ".join(str(text or "").lower().split())
    if not clean or len(clean.split()) > 12:
        return False
    return bool(_POINTS_AT_THE_THREAD.match(clean))


def asks_the_outlook(text, clean=None):
    said = " ".join(str(clean if clean is not None else text or "").lower().split())
    if not said or len(said.split()) > 9:
        return False
    if not _OUTCOME.search(said):
        return False
    if _THE_THING_ITSELF and set(_WORDS.findall(said)) & _THE_THING_ITSELF:
        return False
    return bool(_POINTS_AT_THE_THREAD.match(said))


def the_pool(in_crisis, help_is_coming, asked_them_to_call=False, abuse=False):
    if abuse:
        return LINES_WHEN_SOMEONE_IS_HURTING_YOU
    if in_crisis:
        return LINES_WITH_HELP if help_is_coming else LINES_IN_CRISIS
    if asked_them_to_call:
        return LINES_WITH_HELP if help_is_coming else LINES_IN_AN_EMERGENCY
    return None
