import re

_DECLINED_LITERAL = (r"(?:advice|advise|solutions?|tips?|suggestions?|a\s+lecture|"
                     r"lectures?|to\s+be\s+told\s+what\s+to\s+do|"
                     r"telling\s+me\s+what\s+to\s+do)")

_NO_ADVICE = re.compile(
    r"\b(?:(?:i|we|he|she|they)\s+(?:dont|don't|do\s+not|doesnt|doesn't|didnt|didn't|"
    r"wouldnt|wouldn't)\s+(?:really\s+|actually\s+|even\s+)?"
    r"(?:want|need|wanted|needed|asked\s+for|ask\s+for)\s+"
    r"(?:(?:any|no|your|more|further|the|medical|financial|legal|diet|parenting|career)\s+){0,2}"
    r"(?:" + _DECLINED_LITERAL + r")|"
    r"(?:i|we|im|i'm)\s+(?:am\s+)?(?:not|n't)\s+(?:looking|asking|after|here)\s+for\s+"
    r"(?:a\s+|any\s+|the\s+)?(?:advice|solutions?|fix|fixing|tips?|suggestions?)|"
    r"(?:not|n't)\s+looking\s+for\s+(?:a\s+|any\s+)?(?:solution|advice|fix)|"
    r"no\s+(?:advice|solutions?|tips?|lectures?)(?:\s+(?:please|thanks|thank\s+you))?|"
    r"without\s+(?:the\s+)?(?:advice|lecture|tips)|"
    r"(?:dont|don't|do\s+not|no)\s+(?:give|giving)\s+me\s+(?:any\s+)?(?:advice|tips)|"
    r"not\s+(?:asking|looking)\s+for\s+(?:advice|a\s+solution)|"
    r"(?:dont|don't|do\s+not|stop)\s+tell(?:ing)?\s+me\s+what\s+to\s+do|"
    r"(?:i|i've|ive)\s+(?:already\s+)?know\s+what\s+to\s+do,\s+(?:i\s+)?(?:just|only)\s+"
    r"(?:want|wanted|need|needed))\b", re.I)

_WANT_TO_BE_HEARD = re.compile(
    r"\b(?:(?:just|only|really)\s+(?:want|wanted|need|needed)\s+(?:to\s+)?"
    r"(?:talk|vent|be\s+heard|get\s+(?:it|this|that|something)\s+off\s+(?:my|our)\s+chest)|"
    r"(?:just|only)\s+(?:wanted|want|needed)\s+to\s+(?:say\s+(?:it|this|that|something)|"
    r"tell\s+(?:you|u|someone|somebody|them|him|her)\s+something)|"
    r"(?:just|only)\s+(?:wanted|want)\s+(?:to\s+)?(?:say|tell)\s+(?:it\s+)?out\s+loud|"
    r"wanted\s+to\s+say\s+it\s+out\s+loud|"
    r"i\s+(?:just\s+)?(?:want|wanted)\s+to\s+be\s+heard|"
    r"(?:just\s+|only\s+)?(?:want|wanted|need|needed)\s+(?:someone|somebody|a\s+person)\s+"
    r"(?:who\s+)?(?:to\s+)?listen|"
    r"just\s+(?:talk|listen)\s+to\s+me|"
    r"(?:let|allow)\s+me\s+(?:to\s+)?(?:talk|vent|rant)|"
    r"(?:just\s+|only\s+)?(?:want|need|wanted|needed)\s+to\s+(?:vent|rant)|"
    r"can\s+i\s+(?:just\s+)?(?:vent|rant)|"
    r"i\s+need\s+(?:a\s+)?(?:vent|rant)|"
    r"can\s+i\s+just\s+talk)\b", re.I)

_JUST_LISTEN = re.compile(r"\b(?:just|only)\s+listen(?:\s+to\s+me)?(?:\s+please)?\s*[.!]*$",
                          re.I)

_ASKS_A_VIEW = re.compile(
    r"\b(?:what\s+(?:do\s+)?(?:you|u)\s+(?:think|reckon|make\s+of\s+it)|"
    r"whats\s+your\s+(?:honest\s+)?(?:opinion|view|take)|what\s+is\s+your\s+(?:opinion|view|take)|"
    r"your\s+honest\s+opinion|your\s+view\s+on\s+it|"
    r"(?:must|would\s+you)\s+think\s+of\s+me|does\s+that\s+(?:sound|seem)\s+?"
    r"(?:mad|silly|wrong|bad)|am\s+i\s+(?:being\s+)?(?:mad|silly|wrong|unreasonable))\b", re.I)

_NOT_THIS = re.compile(
    r"\b(?:what|some|good|the\s+best|better)\s+advice\b|"
    r"should\s+i\s+take\s+(?:her|his|their|my|any|some)\s+advice|"
    r"(?:give|giving|offer|offering)\s+(?:her|him|them|my|his|your)\s+advice|"
    r"(?:dont|don't|do\s+not)\s+want\s+to\s+give|"
    r"asked\s+(?:for|about)\s+(?:her|his|their|my)\s+advice", re.I)

_AN_ASK = re.compile(
    r"(?:\b(?:what|how|which|when|where|who|why|should|could|would|can|is|are|does|do)\b"
    r"[^?.!]{0,60}\?|\b(?:what|how|which|where|who)\b\s+(?:do|should|can|could|would)\b|"
    r"\bwhats\b|\bwhat's\b|\bshould\s+i\b|\bcan\s+i\b|\bcould\s+i\b)", re.I)


_A_DECLINE = re.compile(
    r"(?:%s)|(?:%s)|(?:%s)" % (_NO_ADVICE.pattern, _WANT_TO_BE_HEARD.pattern, _JUST_LISTEN.pattern),
    re.I)
_AN_ASK_LATER = re.compile(
    r"\b(?:what|whats|what's|how|which|when|where|who|why|should|could|would|can|is|are|was|"
    r"were|do|does|did|will|want\s+to\s+know|wondering|wonder\s+if|"
    r"tell\s+me\s+(?:if|whether|what|how)|let\s+me\s+know\s+(?:if|whether|what|how))\b",
    re.I)
_NOT_AN_ASK = re.compile(
    r"\b(?:is\s+that\s+(?:ok|okay|alright|fine)|if\s+thats?\s+(?:ok|okay|alright|fine)|"
    r"does\s+that\s+make\s+sense|is\s+that\s+alright\s+with\s+you)\b", re.I)


def _what_is_left_after_the_decline(line):
    said = _A_DECLINE.search(line)
    if not said:
        return line
    return line[said.end():]


def asks_something_of_its_own(line):
    left = _NOT_AN_ASK.sub(" ", _what_is_left_after_the_decline(line))
    return bool(_AN_ASK_LATER.search(left))


A_DEATH = re.compile(
    r"\b(?:died|dying|dead|death|killed|suicide|passed\s+away|passed\s+on|funeral|burial|"
    r"cremation|took\s+(?:his|her|their)\s+own\s+life|"
    r"buried|burying|bereav\w*|grief|grieving|widow|widowed|mourning)\b|"
    r"\b(?:lost|bury|lose|losing)\s+(?:my|our|her|his|their|the)?\s*(?:mum|mom|mother|dad|father|"
    r"wife|husband|baby|child|son|daughter|brother|sister|partner|gran|granny|nan|grandad|"
    r"grandpa|friend|mate)\b", re.I)


def _plain(text):
    return " ".join((text or "").split())


def says_a_death(text):
    return bool(A_DEATH.search(_plain(text)))


def asks_for_a_view(text):
    return bool(_ASKS_A_VIEW.search(_plain(text)))


def says_no_advice(text):
    line = _plain(text)
    if not line:
        return False
    said = bool(_NO_ADVICE.search(line) or _WANT_TO_BE_HEARD.search(line)
                or _JUST_LISTEN.search(line))
    if not said:
        return False
    if asks_for_a_view(line):
        return True
    if _NOT_THIS.search(line):
        return False
    rest = _JUST_LISTEN.sub(" ", _WANT_TO_BE_HEARD.sub(" ", line))
    if _AN_ASK.search(rest):
        return False
    if asks_something_of_its_own(line):
        return False
    return True


def pool_name(text):
    if not says_no_advice(text):
        return None
    return "a_view" if asks_for_a_view(text) else "no_advice"


HEARD = (
    "Fair enough - I'll keep the advice to myself. Tell me the rest of it.",
    "Understood. I'm listening - how are you doing with it?",
    "Right, no fixing from me then. What's on your mind?",
    "That's fair. Say it all and I'll just listen.",
    "No advice, then. Go on - I'm here.",
    "Okay - no advice from me. Where are you with it all?",
)

A_VIEW = (
    "Then tell me the whole of it and I'll say what I think - no fixing, just my honest view.",
    "Okay - the situation as it is, and I'll give you my straight view of it.",
    "I'll tell you what I think, then. What's the situation?",
    "Fair enough. Lay it out and I'll tell you honestly what I make of it.",
)


def lines_for(pool):
    return A_VIEW if pool == "a_view" else HEARD


def reply_for(pool, text, memory=None):
    from . import pick

    return pick(list(lines_for(pool)), memory, text)
