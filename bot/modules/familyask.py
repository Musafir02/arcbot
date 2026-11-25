import re

from ..compose import fallback

PRIORITY = 1100
ANSWERS = ("about-the-bot",)

_PARENTS = ("mum", "mums", "mam", "mams", "mom", "moms", "mother", "mothers", "dad", "dads",
            "father", "fathers", "parent", "parents", "mummy", "daddy")
_GRANDPARENTS = ("gran", "grans", "granny", "grannies", "grandma", "grandmas", "grandad",
                 "grandads", "grandpa", "grandpas", "nana", "nanas", "nan", "nans", "grandparent",
                 "grandparents")
_SIBLINGS = ("brother", "brothers", "sister", "sisters", "sibling", "siblings", "half brother",
             "half sister", "stepbrother", "stepsister", "step brother", "step sister")
_CHILDREN = ("kid", "kids", "child", "children", "son", "sons", "daughter", "daughters",
             "baby", "babies", "grandchild", "grandchildren", "grandson", "granddaughter")
_PARTNER = ("wife", "wives", "husband", "husbands", "partner", "partners", "girlfriend",
            "boyfriend", "fiance", "fiancee", "other half")
_EXTENDED = ("aunt", "aunts", "auntie", "aunties", "uncle", "uncles", "cousin", "cousins",
             "nephew", "nephews", "niece", "nieces", "in law", "in laws", "mother in law",
             "father in law", "brother in law", "sister in law")
_FAMILY = ("family", "families", "relatives", "relations", "folks", "kin")

CLASSES = (
    ("grandparent", _GRANDPARENTS),
    ("parent", _PARENTS),
    ("sibling", _SIBLINGS),
    ("child", _CHILDREN),
    ("partner", _PARTNER),
    ("extended", _EXTENDED),
    ("family", _FAMILY),
)
RELATION = {}
for _class, _words in CLASSES:
    for _word in _words:
        RELATION[_word] = _class
_ALL_RELATIONS = sorted(RELATION, key=len, reverse=True)
THE_RELATION = re.compile(r"\b(?:your|ur|yours|you're|youre)\s+(?:\w+\s+){0,2}?(?:"
                          + "|".join(re.escape(w) for w in _ALL_RELATIONS) + r")\b", re.I)
_LEAD_IN = (r"(?:(?:and|so|but|oh|well|ok|okay|right|hey|hi|yeah|yes|no|nah|actually|honestly|"
            r"just|quick|sorry|lol|haha|ha|eh|ah|hmm|huh|then|now)\b[,!.]?\s+)*")
A_HAVE_RELATION = re.compile(
    r"^" + _LEAD_IN +
    r"(?:(?:have|has|do|does|did)\s+(?:you|u|ya)\s+(?:have\s+|got\s+|ever\s+)*"
    r"|got\s+|any\s+)"
    r"(?:any\s+|a\s+|an\s+|some\s+)?(?:"
    + "|".join(re.escape(w) for w in _ALL_RELATIONS) + r")\b", re.I)
A_RELATION = re.compile(r"\b(?:" + "|".join(re.escape(w) for w in _ALL_RELATIONS) + r")\b", re.I)
HOW_MANY_RELATION = re.compile(
    r"^" + _LEAD_IN + r"how many\s+(?:\w+\s+){0,2}?(?:"
    + "|".join(re.escape(w) for w in _ALL_RELATIONS) + r")\b[\w\s,']*\b(?:you|u|ya)\b", re.I)

A_QUESTION = re.compile(
    r"^" + _LEAD_IN +
    r"(?:(?:can|could|would|will)\s+you\s+)?(?:tell|told|say|talk|chat)\s+(?:me\s+)?"
    r"(?:something\s+|a\s+bit\s+|more\s+|anything\s+)?about\s+|"
    r"(?:is|are|was|were|do|does|did|have|has|had|will|would|can|could|should|shall|"
    r"who|whos|whose|what|whats|what's|where|wheres|when|whens|why|whys|how|hows|which|"
    r"any|anyone|ever|doesnt|didnt|isnt|arent|wasnt|werent)\b",
    re.I)
AND_ANOTHER = re.compile(r"\band\b\s+(?:your|ur)\s+\w+", re.I)
NOT_ABOUT_THE_BOT = re.compile(
    r"\b(?:my|our|his|her|their)\s+(?:"
    + "|".join(re.escape(w) for w in _ALL_RELATIONS) + r")\b", re.I)

NO_ONE = {
    "parent": (
        "No mum and dad of my own - I'm a program, so there's no one who brought me up to be "
        "anywhere.",
        "None on my side: I'm a program, so no parents and no childhood to have them in.",
        "I haven't got parents - I'm a program, so there's no mum and dad at the end of a phone.",
    ),
    "grandparent": (
        "No grandparents of mine - I'm a program, so nothing like that on my side.",
        "None, no: I'm a program, so no nan and grandad to go and see.",
        "I haven't got grandparents - I'm a program, so there's no family of mine at all.",
    ),
    "sibling": (
        "No brothers and no sisters - I'm a program, so no family of my own.",
        "None, no: I'm a program, so there's nobody to fall out with at Christmas.",
        "I haven't got siblings - I'm a program, so nobody grew up alongside me.",
    ),
    "child": (
        "No children of my own - I'm a program, so nobody calls me anything but the bot.",
        "None, no: I'm a program, so no kids and no school run.",
        "I haven't got any - I'm a program, so there's no family of mine to bring up.",
    ),
    "partner": (
        "Nobody like that - I'm a program, so no partner and no one to ring on the way home.",
        "None, no: I'm a program, so there's no other half on my side.",
        "I haven't got one - I'm a program, so nobody's waiting up for me.",
    ),
    "extended": (
        "None of those on my side - I'm a program, so no aunts, uncles or cousins.",
        "Nobody like that: I'm a program, so there's no family of mine to be an aunt or uncle to.",
        "I haven't got any - I'm a program, so no relatives at all.",
    ),
    "family": (
        "No family of my own - I'm a program, so there is nobody on my side of it.",
        "None, no: I'm a program, so no family, no birthday list, nobody to ask after.",
        "I haven't got any - I'm a program, so there's no family of mine at all.",
    ),
}
_HOW_IT_WENT = (
    "Tell me about yours - how did it go?",
    "How did it go with yours?",
    "What about your lot - how did it go?",
)
_THE_PEOPLE = (
    "Tell me about yours though - do you see much of them?",
    "What about your lot?",
    "How are yours doing?",
)
A_PAST_ASK = re.compile(
    r"\b(?:was|were|did|said|had|went|wore|told|thought|felt|been|there|at it|come)\b", re.I)
_NO_HAND_BACK = re.compile(r"\b(?:think|feel|felt|mind|care|miss|lonely|sorry|upset)\b", re.I)


def the_relation(text):
    said = " ".join(str(text or "").split())
    match = (THE_RELATION.search(said) or A_HAVE_RELATION.match(said)
             or HOW_MANY_RELATION.match(said))
    if not match:
        return None
    words = [w.lower().strip(",.'") for w in match.group(0).split()]
    found = [w for w in words if w in RELATION]
    if not found:
        return None
    if AND_ANOTHER.search(said[match.end():]):
        rest = A_RELATION.search(said[match.end():])
        if rest and rest.group(0).lower() != found[0]:
            return found[0] + " and " + rest.group(0).lower()
    return found[0]


def the_class(text):
    said = " ".join(str(text or "").split())
    match = (THE_RELATION.search(said) or A_HAVE_RELATION.match(said)
             or HOW_MANY_RELATION.match(said))
    if not match:
        return None
    words = [w.lower().strip(",.'") for w in match.group(0).split()]
    for word in words:
        if word in RELATION:
            return RELATION[word]
    return None


A_CHOICE = re.compile(
    r"\bor\b\s+(?!(?:not|no|is|are|was|were|else|anything|something|otherwise)\b|(?:"
    + "|".join(re.escape(w) for w in _ALL_RELATIONS) + r")\b)\w+", re.I)


def is_a_family_ask(text):
    said = " ".join(str(text or "").split())
    if not said:
        return False
    if (not THE_RELATION.search(said) and not A_HAVE_RELATION.match(said)
            and not HOW_MANY_RELATION.match(said)):
        return False
    if NOT_ABOUT_THE_BOT.search(said):
        return False
    if A_CHOICE.search(said):
        return False
    return bool(A_QUESTION.match(said) or A_HAVE_RELATION.match(said)
                or HOW_MANY_RELATION.match(said) or said.endswith("?"))


def reply_for(text, memory=None):
    if not is_a_family_ask(text):
        return None
    said = " ".join(str(text or "").split())
    kind = the_class(said) or "family"
    told = NO_ONE[kind]
    said_of = _HOW_IT_WENT if A_PAST_ASK.search(said) else _THE_PEOPLE
    seed = " ".join(str(text or "").lower().split())
    honest = fallback.pick(told, memory or {}, seed)
    if _NO_HAND_BACK.search(said):
        return honest
    return honest + " " + fallback.pick(said_of, memory or {}, seed)


def TAKES_AS_IT_COMES(text, memory):
    return is_a_family_ask(text)


def respond(text, memory):
    if not isinstance(memory, dict):
        memory = {}
    return reply_for(text, memory)
