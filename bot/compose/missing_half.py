import re

A_COMPARISON = re.compile(
    r"\bwho(?:'s|s| is| was)?\s+(?:the\s+)?(?:older|younger|eldest|oldest|youngest)\b|"
    r"\b(?:am|is|are|was|were)\b[^.!?]{0,40}\b(?:older|younger|eldest|oldest)\b|"
    r"\bhow (?:much|many years)\s+(?:older|younger)\b|"
    r"\b(?:older|younger) (?:than )?(?:me|him|her|them)\b", re.I)

A_GAP = re.compile(r"\bhow\s+(?:much|many\s+years)\s+(?:older|younger)\b", re.I)

A_GROUP = re.compile(
    r"\b(?:family|families|class|team|group|household|siblings|relatives|relations|kids|"
    r"children|brothers|sisters|friends|everyone|everybody|all of them|the rest)\b", re.I)

KIN = ("mum", "mam", "mom", "mother", "dad", "father", "parent", "parents", "brother", "sister",
        "son", "daughter", "child", "kid", "wife", "husband", "partner", "girlfriend",
        "boyfriend", "fiance", "fiancee", "gran", "granny", "nan", "nana", "grandma",
        "grandad", "grandpa", "grandfather", "aunt", "auntie", "uncle", "cousin", "nephew",
        "niece", "stepson", "stepdaughter", "stepdad", "stepmum", "mate", "friend", "boss",
        "colleague", "neighbour", "landlord", "flatmate", "housemate", "boy", "girl", "baby")
A_PERSON_NAMED = re.compile(r"\b(?:my|our)\s+(" + "|".join(KIN) + r")(?:'s|s')?\b", re.I)
A_THING_NAMED = re.compile(r"\bmy\s+([a-z][a-z'-]+)\b", re.I)
A_SOMEONE = re.compile(r"\b(?:him|her|them|they|he|she)\b", re.I)
A_THROUGH_SOMEONE = re.compile(r"\b(?:his|hers|her|their|theirs|its)\s+[a-z][a-z'-]+", re.I)
A_MYSELF = re.compile(r"\b(?:i|i'm|im|me|my|mine|myself|we|us|our)\b", re.I)

WITH_MINE = (
    "I've got you at {mine}, but nothing on {theirs}, so there's no two numbers to put together. "
    "Tell me that one and I'll say which of you is older.",
    "You're {mine} in what you've told me and {theirs} has no age beside it. Give me that and the "
    "comparison takes one line.",
)
WITHOUT_MINE = (
    "There's nothing beside {theirs}: I have no age of yours either. Give me both and I'll say "
    "which of you is older.",
    "The only age here would be {theirs}, and yours is the other half. Tell me yours and I'll do "
    "the rest.",
)
BOTH_MISSING = (
    "I have {known} and no age of yours, and nothing on {theirs} either. Those two numbers and the "
    "comparison takes one line.",
    "What I have is {known}; what is missing is your own age and {theirs}. Give me those and I'll "
    "say which of you is older.",
)
NOBODY_ELSE = (
    "Nothing beside your own age is here to put it against. Give me theirs and I'll say which of "
    "you is older.",
    "One number is not a comparison, and yours is the only one here. Tell me theirs and the answer "
    "is one line.",
)
TWO_THINGS = (
    "Those are two made things, so what settles it is the year each one was made - on the thing "
    "itself, on its rating label, or in its manual. Give me the two years and I'll say which is "
    "older.",
    "The age of a made thing is the year it was made, and nothing you've told me has either one. "
    "The label or the manual will have it; two years and the comparison takes one line.",
)
THEIR_AGE_ONLY = (
    "I've got {theirs} at {their_age}, but never your age, so there is one number where there "
    "should be two. Tell me yours and I'll say which of you is older.",
    "{theirs} is {their_age} in what you've told me and your own age is not there. Give me that "
    "and the comparison takes one line.",
)
HIM_OR_HER = (
    "I've an age here and no way to tell who you mean. Say who it is and I'll put the two side by "
    "side.",
    "Nothing in the line says who that is, so there's no second age for me to reach. Name the "
    "person and the comparison takes one line.",
)
THEY_ARE_OLDER = ("{Theirs} is older - {their_age} to your {mine}.",)
I_AM_OLDER = ("You're older - {mine} to {theirs}'s {their_age}.",)
SAME_AGE = ("Neither of you - you're both {mine}.",)


def _choose(pool, text):
    return pool[sum(ord(one) for one in text) % len(pool)]


def _a_sentence(line):
    return line[0].upper() + line[1:] if line else line


FEMALE = frozenset("mum mam mom mother sister wife gran granny nan nana grandma daughter aunt "
                    "auntie niece stepmum stepdaughter girlfriend fiancee".split())
MALE = frozenset("dad father brother husband grandad grandpa grandfather son uncle nephew stepdad "
                 "stepson boyfriend fiance".split())


def _fits(low, who):
    if re.search(r"\b(?:them|they)\b", low):
        return True
    she = re.search(r"\bher\b|\bshe\b", low) is not None
    he = re.search(r"\bhim\b|\bhis\b|\bhe\b", low) is not None
    if she and not he:
        return who in FEMALE
    if he and not she:
        return who in MALE
    return True


def _given_beside(low, who):
    return re.search(r"\bmy\s+" + who + r"\b[^.!?,]{0,16}?\b\d{1,3}\b", low) is not None


def _the_ages(memory):
    mine = None
    user = memory.get("user") or {}
    try:
        if user.get("age") is not None:
            mine = int(user.get("age"))
    except (TypeError, ValueError):
        mine = None
    others = {}
    for entry in memory.get("others") or []:
        if not isinstance(entry, dict) or entry.get("age") is None:
            continue
        who = str(entry.get("who") or "").strip().lower()
        if not who:
            continue
        try:
            others[who] = int(entry.get("age"))
        except (TypeError, ValueError):
            continue
    return mine, others


def _the_known_list(others):
    parts = []
    for who, age in list(others.items())[:2]:
        parts.append("your " + who + " at " + str(age))
    if len(parts) == 2:
        return parts[0] + " and " + parts[1]
    if not parts:
        return "nothing"
    return parts[0]


def the_missing_half(text, memory):
    low = " ".join(str(text or "").lower().split())
    if not low or not A_COMPARISON.search(low):
        return ""
    if A_GAP.search(low):
        return ""
    if A_GROUP.search(low):
        return ""
    if A_THROUGH_SOMEONE.search(low):
        return ""
    mine, others = _the_ages(memory)
    named = []
    for one in A_PERSON_NAMED.findall(low):
        one = one.lower()
        if one not in named:
            named.append(one)
    things = []
    for one in A_THING_NAMED.findall(low):
        one = one.lower()
        if one not in KIN and one not in things:
            things.append(one)
    if named:
        unknown = [one for one in named if one not in others and not _given_beside(low, one)]
        if not unknown:
            return ""
        theirs = "your " + unknown[0]
        if things:
            return ""
        if mine is not None:
            return _choose(WITH_MINE, low).format(mine=str(mine), theirs=theirs)
        if others:
            return _choose(BOTH_MISSING, low).format(
                known=_the_known_list(others), theirs=theirs)
        return _a_sentence(_choose(WITHOUT_MINE, low).format(theirs=theirs))
    if things:
        if len(things) >= 2 and not A_SOMEONE.search(low):
            if re.search(r"\b\d{4}\b|\b(?:19|20)\d\d\b", low):
                return ""
            return _a_sentence(_choose(TWO_THINGS, low))
        return ""
    if not A_SOMEONE.search(low):
        if others and mine is not None:
            return ""
        if mine is not None:
            return _a_sentence(_choose(NOBODY_ELSE, low).format(mine=str(mine)))
        return ""
    if not others:
        return ""
    fits = [who for who in others if _fits(low, who)]
    if mine is None and len(fits) == 1:
        who = fits[0]
        return _a_sentence(_choose(THEIR_AGE_ONLY, low).format(
            theirs="your " + who, their_age=str(others[who])))
    if mine is not None and len(fits) == 1:
        who = fits[0]
        their_age = others[who]
        theirs = "your " + who
        if their_age == mine:
            return _choose(SAME_AGE, low).format(mine=str(mine))
        if their_age > mine:
            return _choose(THEY_ARE_OLDER, low).format(
                Theirs=theirs[0].upper() + theirs[1:], their_age=str(their_age),
                mine=str(mine))
        return _a_sentence(_choose(I_AM_OLDER, low).format(
            theirs=theirs, their_age=str(their_age), mine=str(mine)))
    return _a_sentence(_choose(HIM_OR_HER, low).format(known=_the_known_list(others)))


__all__ = ["the_missing_half", "A_COMPARISON"]
