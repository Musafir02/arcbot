import re

_STANCE = r"(?:ok|okay|alright|all\s+right|fine|happy|cool|good|easy|content)"
_OBJECT = (r"(?:that|this|it|them|those|these|the\s+\w+|my\s+\w+|"
           r"me(?:\s+\w+ing)?|me\s+\w+|if\s+i\b|it\s+if)")

_A_CHECK_ASKED = re.compile(
    r"\b(?:are|r|is|was|do|does|would|will|could)?\s*(?:you|u|ya)\s+"
    r"(?:really\s+|still\s+|definitely\s+)?(?:be\s+)?" + _STANCE + r"\s+"
    r"(?:with|wiv|wid|about|by)\s+" + _OBJECT + r"\b"
)
_A_THING_FOR_YOU = re.compile(
    r"\b(?:(?:is|was|are|were)\s+)?(?:that|this|it|those|these)\s+(?:really\s+)?"
    r"(?:ok|okay|alright|all\s+right|fine)\s+(?:with|wiv|wid|by|for)\s+(?:you|u|ya)\b"
)
_A_VERB_FOR_YOU = re.compile(
    r"\b(?:does|do|would|will|did)?\s*(?:that|this|it)\s+(?:work|suit|square|be\s+alright|"
    r"be\s+ok|be\s+fine)\s+(?:for|with|wiv|wid)\s+(?:you|u|ya)\b"
)
_A_VERB_YOU = re.compile(
    r"\b(?:does|do|would|will|did|is)\s+(?:that|this|it)\s+(?:work|suit|do)\s+(?:you|u|ya)\b"
)
_BARE_STANCE = r"(?:ok|okay|alright|all\s+right|fine|happy|cool|easy|content)"
_BARE_FOR_YOU = re.compile(
    r"^\s*(?:so\s+)?(?:" + _BARE_STANCE + r"|work|works|suit|suits|square)\s+"
    r"(?:for|with|wiv|wid|by)\s+(?:you|u|ya)\s*\??\s*$"
)

A_CHECK = (_A_CHECK_ASKED, _A_THING_FOR_YOU, _A_VERB_FOR_YOU, _A_VERB_YOU, _BARE_FOR_YOU)

AGREED = (
    "Fine by me - and it's your call, not mine.",
    "That suits me. Whether it suits you is the part I can't answer.",
    "No objection here. You're the one it has to work for, though.",
    "Sounds alright to me. I've got nothing at stake in it either way.",
    "Happy with that. It's your call at the end of it.",
    "Works for me - just don't count me as the one who decided it.",
    "That's fine as far as I'm concerned. What matters is whether it's fine by you.",
)

_NOT_A_CHECK = re.compile(
    r"\b(?:drive|driving|tow|towing|insure|sign|signing|sue|arrest|publish|fly|flying|"
    r"sail|carry|carrying|keep\s+it|eat|drink)\b"
)


def reads_as_a_check(text):
    said = " " + re.sub(r"[^a-z0-9'? ]", " ", (text or "").lower()) + " "
    if _NOT_A_CHECK.search(said):
        return False
    for shape in A_CHECK:
        if shape.search(said) or (shape is _BARE_FOR_YOU and shape.search(said.strip())):
            return True
    return False


def answer_for(text, memory=None, choose=None):
    if not reads_as_a_check(text):
        return None
    if choose is None:
        import random
        choose = random.choice
    return choose(AGREED)
