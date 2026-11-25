import re

GROUP_WORDS = (
    "kids", "children", "sons", "daughters", "boys", "girls", "parents", "grandparents",
    "grandchildren", "grandkids", "brothers", "sisters", "twins", "cousins", "nieces",
    "nephews", "aunts", "uncles", "stepchildren", "stepkids", "in-laws", "flatmates",
    "housemates", "neighbours",
)

_THE_SAME_GROUP = {
    "children": "children", "child": "children",
    "kid": "kids", "kids": "kids",
    "grandchild": "grandchildren", "grandkids": "grandchildren",
    "stepchild": "stepchildren", "stepkid": "stepkids",
}

_GROUPS = "|".join(sorted(GROUP_WORDS, key=len, reverse=True))

_AGE = r"\d{1,3}(?![\d.])"
_A_LIST_OF_AGES = _AGE + r"(?:\s*(?:,|and|&)\s*" + _AGE + r"){1,3}"

_NOT_A_UNIT = (r"(?!\s*(?:times|days|weeks|months|hours|minutes|miles|metres|kilometres|km|"
               r"kilos|kilograms|kg|pounds|quid|per\b|a\s+(?:week|month|year|day))"
               r"|\s*years(?!\s+old))")

GIVES_A_LIST = re.compile(
    r"\b(?:my|our|the|his|her)\s+(?:\w+\s+){0,2}?(?P<word>" + _GROUPS + r")\b"
    r"(?:\s+(?:are|were|is|was|aged|both))?[,\s]+(?P<ages>" + _A_LIST_OF_AGES + r")"
    r"(?![\d,.])" + _NOT_A_UNIT, re.I)

GIVES_A_LIST_BARE = re.compile(
    r"\b(?P<word>" + _GROUPS + r")\s+(?:are|were|aged|both\s+aged)\s+"
    r"(?P<ages>" + _A_LIST_OF_AGES + r")(?![\d,.])" + _NOT_A_UNIT, re.I)

THEYRE_A_LIST = re.compile(
    r"\b(?:my|our|the)?\s*(?:\w+\s+){0,2}?(?P<word>" + _GROUPS + r")\b[^.!?]{0,20}?"
    r"\b(?:they'?re|they\s+are|both\s+aged)\s+(?P<ages>" + _A_LIST_OF_AGES + r")"
    + _NOT_A_UNIT, re.I)

ASKS_THE_LIST = re.compile(
    r"\bhow\s+old\s+(?:are|were|is)\s+(?:they|their|(?:\w+\s+){0,2}?(?:" + _GROUPS + r"))\b"
    r"|\b(?:what|whats|what\s+are|what\s+were)\s+(?:are\s+|were\s+)?"
    r"(?:their|the|my|our)\s+(?:\w+\s+){0,2}?(?:" + _GROUPS + r"|ages)\b"
    r"|\bhow\s+old\s+are\s+(?:my|our|the)\s+(?:\w+\s+){0,2}?(?:" + _GROUPS + r")\b"
    r"|\b(?:their|the\s+kids'?|my\s+kids'?)\s+ages\b"
    r"|\bwhat\s+(?:were|are)\s+my\s+(?:\w+\s+){0,2}?(?:" + _GROUPS + r")\s+ages\b", re.I)

ASKS_THE_END_ONE = re.compile(
    r"\bhow\s+old\s+(?:is|was)\s+(?:your\s+|the\s+|my\s+|our\s+)?"
    r"(?P<which>youngest|oldest|elder|eldest|older|younger|little|big|little\s+one|big\s+one)\b",
    re.I)


def _the_word(word):
    found = str(word or "").lower().strip()
    found = _THE_SAME_GROUP.get(found, found)
    return found if found in GROUP_WORDS else ""


def _ages_in(value):
    return [int(number) for number in re.findall(r"\d{1,3}", str(value or ""))]


def the_list_given(text):
    line = str(text or "")
    for pattern in (GIVES_A_LIST, GIVES_A_LIST_BARE, THEYRE_A_LIST):
        found = pattern.search(line)
        if found is None:
            continue
        word = _the_word(found.group("word"))
        ages = _ages_in(found.group("ages"))
        if word and len(ages) >= 2:
            return word, ages
    return None


def watch(text, memory):
    if not isinstance(memory, dict):
        return
    given = the_list_given(text)
    if not given:
        return
    word, ages = given
    memory["group_ages"] = {"word": word, "ages": ages, "line": " ".join(str(text).split())}


def _the_kept(memory):
    if not isinstance(memory, dict):
        return "", []
    kept = memory.get("group_ages")
    if not isinstance(kept, dict):
        return "", []
    word = _the_word(kept.get("word"))
    ages = [age for age in kept.get("ages") or [] if isinstance(age, int)]
    if not word or len(ages) < 2:
        return "", []
    return word, ages


def _a_list(ages):
    said = [str(age) for age in ages]
    if len(said) == 1:
        return said[0]
    return "%s and %s" % (", ".join(said[:-1]), said[-1])


_THE_SINGULARS = {
    "children": ("child",), "kids": ("kid", "child"), "parents": ("parent",),
    "people": ("person",), "men": ("man",), "women": ("woman",),
    "twins": ("twin",), "boys": ("boy",), "girls": ("girl",),
    "sisters": ("sister",), "brothers": ("brother",),
    "sons": ("son",), "daughters": ("daughter",),
    "grandchildren": ("grandchild",), "grandparents": ("grandparent",),
    "aunts": ("aunt",), "uncles": ("uncle",), "nieces": ("niece",), "nephews": ("nephew",),
    "cousins": ("cousin",), "flatmates": ("flatmate",), "roommates": ("roommate",),
    "friends": ("friend",), "neighbours": ("neighbour",), "grandkids": ("grandkid",),
}


def _the_singulars(word):
    word = str(word or "")
    out = set(_THE_SINGULARS.get(word, ()))
    if word.endswith("s"):
        out.add(word[:-1])
    return {one for one in out if one}


def _the_end_one_is_the_group(text, end_one, word):
    after = str(text or "")[end_one.end():]
    words = [said for said in re.split(r"[^a-z']+", after.lower()) if said]
    if not words:
        return True
    first = words[0]
    if first in ("one", "ones", "of"):
        return True
    return first in _the_singulars(word)


def _the_group_asked(text, word):
    line = str(text or "").lower()
    named = [found for found in GROUP_WORDS if re.search(r"\b%s\b" % re.escape(found), line)]
    named = [_the_word(found) for found in named]
    if not named:
        return ""
    return word if word in named else None


def reply_for(text, memory):
    word, ages = _the_kept(memory)
    if not word or not ages:
        return ""
    line = str(text or "")
    asked = _the_group_asked(line, word)
    if asked is None:
        return ""
    end_one = ASKS_THE_END_ONE.search(line)
    if end_one is not None and not _the_end_one_is_the_group(line, end_one, word):
        return ""
    if end_one is not None and asked == "":
        which = end_one.group("which").lower()
        if which in ("youngest", "younger", "little", "little one"):
            return "Your youngest is %d." % min(ages)
        return "Your oldest is %d." % max(ages)
    if end_one is not None:
        which = end_one.group("which").lower()
        if which in ("youngest", "younger", "little", "little one"):
            return "Your youngest %s is %d." % (word[:-1] if word.endswith("s") else word,
                                                min(ages))
        return "Your oldest %s is %d." % (word[:-1] if word.endswith("s") else word, max(ages))
    if not ASKS_THE_LIST.search(line):
        return ""
    return "Your %s are %s." % (word, _a_list(ages))


def asks_for_the_list(text, memory):
    return bool(reply_for(text, memory))
