import re

DREAM = re.compile(r"\b(dreamt|dreamed|dreaming|dream|dreams)\b")
FIRST_PERSON = re.compile(r"\b(?:i|im|i'm|ive|i've|id|i'd|my|me)\b")
NAMED_A_NIGHTMARE = re.compile(
    r"\b(?:nightmares?|night terrors?|(?:bad|scary|terrible|awful|horrible)\s+dreams?)\b")
A_WISH = re.compile(r"\bdream(?:s|ing)?\s+of\b|\b(?:i|we)\s+have\s+a\s+dream\b(?![^.]*\b(?:last|other)\s+night)\b")
A_WISH_TO_BE_GONE = re.compile(
    r"\bdream(?:s|t|ed|ing)?\s+(?:of|about)\s+(?:my\s+own\s+|me\s+|being\s+)?"
    r"(?:ending\s+it(?:\s+all)?|ending\s+things|ending\s+my\s+life|ending\s+everything|"
    r"kill(?:ing)?\s+myself|suicide|suicidal|dying|death|being\s+dead|dead|not\s+waking|"
    r"not\s+being\s+here|disappearing|gone\s+for\s+good)\b", re.I)
DREAM_VERB = re.compile(r"\b(?:dreamt|dreamed|dreaming)\b")
A_SAID_WISH = re.compile(
    r"\b(?:ending\s+it\s+all|ending\s+things|kill(?:ing)?\s+myself|kill\s+me|suicide|suicidal|"
    r"want(?:ed|ing)?\s+to\s+die|wanted\s+to\s+be\s+dead|wish(?:ed)?\s+i\s+(?:was|were)\s+dead|"
    r"not\s+being\s+here|not\s+here\s+any\s+more|don'?t\s+want\s+to\s+be\s+here)\b", re.I)

A_DREAM_AHEAD = re.compile(
    r"\bdream(?:s)?\s+(?:job|jobs|career|role|home|house|flat|holiday|holidays|trip|car|"
    r"wedding|team|life|garden|kitchen|body|figure|man|woman|partner|business|company|"
    r"kitchen|room|wardrobe|outfit)\b")
A_SCENE_OF_NOTHING = re.compile(r"^(?:about\s+)?(?:it|that|this|him|her|them|one)?$")


def the_scene(line):
    text = " ".join(str(line or "").lower().split())
    if not text or len(text) > 400:
        return None
    if NAMED_A_NIGHTMARE.search(text):
        return None
    found = DREAM.search(text)
    if not found:
        return None
    before = text[:found.start()]
    if not FIRST_PERSON.search(before):
        return None
    scene = text[found.end():].strip(" ,.:;!-")
    if A_WISH.search(text) or "one day" in scene or A_SCENE_OF_NOTHING.match(scene):
        return None
    if A_WISH_TO_BE_GONE.search(text) or A_SAID_WISH.search(text):
        return None
    if A_DREAM_AHEAD.search(text) and not DREAM_VERB.search(text):
        return None
    return scene or None


def named(line):
    return the_scene(line) is not None


def dreamed_before(line, pattern):
    text = " ".join(str(line or "").lower().split())
    scene = the_scene(text)
    if scene is None or not pattern.search(scene):
        return False
    return not pattern.search(text[:text.find(scene)])


SETTLED_IT = re.compile(
    r"\b(?:just|only)\s+(?:a\s+|an\s+)?(?:bad\s+|weird\s+|strange\s+|silly\s+|daft\s+)?"
    r"(?:dream|nightmare)\b|"
    r"\b(?:it|that|this)\s+(?:was|were|is)\s+(?:only\s+|just\s+)?(?:a\s+)?"
    r"(?:dream|nightmare)\b|"
    r"\bnot\s+real\b|\bwasn'?t\s+real\b|\bnever\s+happened\b|"
    r"\b(?:he|she|they|it)(?:'s|\s+is|\s+was|\s+were)?\s+"
    r"(?:fine|ok|okay|alright|all\s+right|safe|still\s+here|still\s+alive|alive)\b",
    re.I)


DREAM_NAMED = re.compile(
    r"\b(?:i|we)\s+(?:just\s+)?(?:had\s+(?:a\s+|the\s+|this\s+)?(?:dream|nightmare|bad\s+dream)"
    r"|(?:had|have)\s+(?:a\s+|this\s+)?(?:dream|nightmare|nightmares|bad\s+dreams?|weird\s+dreams?)"
    r"|dream(?:t|ed|ing)?(?:\s+about|\s+that|\s+of|,|\s+i\b)"
    r"|keep\s+dreaming|kept\s+dreaming|nightmares?\s+(?:about|where|that)"
    r"|(?:was|were)\s+dreaming)\b",
    re.I)
DREAM_NAMED_LOOSE = re.compile(
    r"\b(?:in\s+(?:my|a|the)\s+dream|in\s+my\s+nightmare|in\s+dreams?|"
    r"dreamt|dreamed|dreaming|nightmares?|nightmare)\b",
    re.I)
DREAM_IS_HAPPENING_NOW = re.compile(
    r"\b(?:woke\s+up|woken\s+up|wake\s+up|awake|awoken|"
    r"still\s+(?:there|here|going|on|going\s+on|burning|bleeding|hurting|happening|smoking|"
    r"happens|feel|feels|have|got)|"
    r"right\s+now|just\s+now|this\s+minute|at\s+the\s+moment|"
    r"and\s+i\s+(?:can'?t|cannot|cant)\s+(?:breathe|move|feel|stop)|"
    r"it\s+(?:is|was)\s+real|"
    r"i\s+(?:can|could)\s+smell\s+(?:smoke|gas|burning)|"
    r"i\s+(?:have|took|taken|swallowed|drank|drunk)\s+(?:them|it|the|some|a\s+few|"
    r"\d+|all\s+of)|\b\d+\s+(?:of\s+them|tablets|pills)|"
    r"i\s+am\s+(?:bleeding|burning|stuck|trapped|drowning|having|on\s+fire)|"
    r"i'?m\s+(?:bleeding|burning|stuck|trapped|drowning|having|on\s+fire|not\s+breathing)|"
    r"my\s+(?:arm|leg|chest|head|back|side|stomach|belly|hand|foot|face)\s+(?:is\s+|feels\s+)?"
    r"(?:numb|bleeding|swollen|hot|painful|hurts|broken|blue)|"
    r"there\s+(?:is|are)\s+(?:smoke|flames?|blood|pain)|"
    r"the\s+(?:smoke|flames?|alarm|bleeding)\s+(?:is|are)\s+(?:still|now|real)|"
    r"(?:i\s+|we\s+)?(?:can\s+)?(?:smell|smells|smelling)\s+(?:smoke|gas|burning)|"
    r"\b(?:smoke|flames?)\s+(?:is\s+|are\s+)?(?:coming|pouring|everywhere)|"
    r"\balarm\s+(?:is\s+|keeps\s+)?(?:going|beeping|sounding)|"
    r"\b(?:is|are)\s+(?:going|happening)\s+(?:on\s+)?now|"
    r"\b(?:he|she|they|it|the\s+baby|my\s+baby)(?:'s|s|\s+is|\s+was|\s+are|\s+were)?\s+"
    r"(?:not|isn'?t|wasn'?t|aren'?t|aint|ain'?t|no\s+longer)\s+"
    r"(?:breathing|moving|responding|waking|conscious|with\s+us|alive)|"
    r"\b(?:shes|hes|theyre|its)\s+(?:not|isn'?t)\s+(?:breathing|moving|responding|waking|conscious)|"
    r"\b(?:lying|lay)\s+(?:there|on\s+the\s+(?:floor|ground|bed|road))\s+(?:now|still)|"
    r"\b(?:there'?s|theres)\s+smoke\s+(?:in|coming|everywhere)|"
    r"\b(?:i\s+can\s+hear|i\s+hear)\s+(?:the\s+alarm|smoke\s+alarm|sirens))\b",
    re.I)


def told_in_the_turn_before(memory):
    turns = (memory or {}).get("turns") if isinstance(memory, dict) else None
    if not (isinstance(turns, list) and turns and isinstance(turns[-1], dict)):
        return False
    last = turns[-1]
    if str(last.get("module") or "") == "dreams":
        return True
    return the_scene(str(last.get("user") or "")) is not None


def told_as_a_dream(line):
    return named(line) and a_dream_is_not_happening(line)


def a_dream_is_not_happening(line):
    if not line:
        return False
    text = str(line)
    if not (DREAM_NAMED.search(text) or DREAM_NAMED_LOOSE.search(text)):
        return False
    if A_WISH_TO_BE_GONE.search(text) or A_SAID_WISH.search(text):
        return False
    if A_DREAM_AHEAD.search(text) and not DREAM_VERB.search(text):
        return False
    return not DREAM_IS_HAPPENING_NOW.search(text)

A_DEATH_BEFORE_THE_DREAM = re.compile(
    r"\b(?:died|dying|death|dead|deaths|passed\s+away|passed\s+on|killed|funeral|buried|"
    r"cremation|widow|widowed)\b[^.]*?\b(?:dream|dreams|dreamt|dreamed|dreaming|dreamed|"
    r"nightmare|nightmares)\b",
    re.IGNORECASE)


def a_death_came_first(line):
    return bool(A_DEATH_BEFORE_THE_DREAM.search(" ".join(str(line or "").lower().split())))
