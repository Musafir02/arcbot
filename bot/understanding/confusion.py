

import re

from .kinds import DENY_BEFORE


CONFUSION_A_THING = (r"(?:the|this|that|these|those|my|our|your|his|her|their|its|a|an)"
                     r"\s+(?:[a-z'-]+\s+){0,8}?[a-z'-]+")
CONFUSION_CUT = frozenset("""
of for with and in at to from about by on that which but so because when if as while
""".split())
CONFUSION_TRAILING = frozenset("""
the a an it its is are was were this these those my our me i we you
""".split())
CONFUSION_SAID_OF_A_THING = re.compile(
    r"\b(?P<thing>" + CONFUSION_A_THING + r")\s+"
    r"(?:is|are|was|were|looks?|seems?|reads?|sounds?)\s+"
    r"(?:(?:so|really|very|totally|just|completely|properly|bloody|dead|too|all)\s+)?"
    r"(?P<cue>confusing|baffling|impossible|incomprehensible|unreadable|a nightmare|double dutch|"
    r"gobbledygook)\b")
CONFUSION_POINTS_AT_NOTHING = re.compile(
    r"\b(?:this|that|it|all this|all of this|everything|the whole thing)\s+(?:is|are|was)\s+"
    r"(?:(?:so|really|very|totally|just|completely|properly)\s+)?"
    r"(?P<cue>confusing|baffling|impossible|incomprehensible|a nightmare|double dutch)\b")
CONFUSION_CANNOT_FOLLOW = re.compile(
    r"\b(?:i|we)\s+(?:just\s+|still\s+|really\s+|honestly\s+|literally\s+|even\s+)?"
    r"(?:can not|cannot|cant|could not|couldnt|do not|dont|did not|didnt)\s+"
    r"(?P<cue>follow|understand|make\s+sense\s+of|figure\s+out|work\s+out|get)\s+"
    r"(?P<thing>" + CONFUSION_A_THING + r")")
CONFUSION_BY_A_THING = re.compile(
    r"\b(?:i am|im|i feel|i felt|i was|i get|i got|we are|we got|were|feeling)\s+"
    r"(?:(?:so|really|totally|completely|properly|just|a bit)\s+)?"
    r"(?P<cue>baffled|lost|stumped|puzzled|confused|flummoxed)\s+"
    r"(?:by|with|on|at)\s+(?P<thing>" + CONFUSION_A_THING + r")")
CONFUSION_HARD_TO = re.compile(
    r"\b(?P<thing>" + CONFUSION_A_THING + r")\s+"
    r"(?:is|are|was|were)\s+"
    r"(?:(?:so|really|very|too|just|almost)\s+)?"
    r"(?:impossible|hard|difficult|tough|not\s+easy|awkward)\s+to\s+"
    r"(?P<cue>read|follow|understand|fill\s+in|make\s+sense\s+of|work\s+out|get\s+through)\b")
CONFUSION_HEAD_NOR_TAIL = re.compile(
    r"\b(?:i|we)\s+(?:(?:just|still|really)\s+)?"
    r"(?:can not|cannot|cant|could not|couldnt|do not|dont|did not|didnt)\s+"
    r"(?P<cue>make|tell)\s+(?:head|heads)\s+(?:nor|or)\s+tail\s+of\s+"
    r"(?P<thing>" + CONFUSION_A_THING + r")")
CONFUSION_MAKES_NO_SENSE = re.compile(
    r"\b(?P<thing>" + CONFUSION_A_THING + r")\s+"
    r"(?P<cue>makes|made|does not make|doesnt make|did not make|didnt make)\s+"
    r"(?:any\s+|no\s+|much\s+)?sense\b")
CONFUSION_HEAD_SPINNING = re.compile(
    r"\bmy\s+head\s+(?:is|was|'s)\s+(?:spinning|swimming|in a spin|all over the place)\b"
    r"\s+(?:with|from|over)\s+"
    r"(?P<thing>(?:(?:all|both)\s+(?:of\s+)?)?" + CONFUSION_A_THING +
    r"|all\s+(?:this|that|it)|everything|it)\b")


CONFUSION_HELPER_NOT = re.compile(
    r"\b(?:can\s+not|cannot|do\s+not|dont|does\s+not|doesnt|did\s+not|didnt|could\s+not|"
    r"couldnt|would\s+not|wouldnt|will\s+not|wont|shall\s+not|should\s+not|shouldnt|"
    r"is\s+not|isnt|are\s+not|arent|was\s+not|wasnt|were\s+not|werent|have\s+not|havent|"
    r"has\s+not|hasnt|had\s+not|hadnt|must\s+not)\s*$")


def _a_confusion_ruled_out(before_cue):
    return bool(DENY_BEFORE.search(CONFUSION_HELPER_NOT.sub("", before_cue)))


def _a_thing_trimmed(thing):
    words = []
    for word in (thing or "").split():
        if word in CONFUSION_CUT:
            break
        words.append(word)
    while words and words[-1] in CONFUSION_TRAILING:
        words.pop()
    if len(words) < 2 or not any(word not in CONFUSION_TRAILING for word in words[1:]):
        return None
    return " ".join(words)


def confusion_of(line):
    for clause in [part.strip() for part in str(line.get("norm_text") or "").split("|")]:
        if not clause:
            continue
        found = CONFUSION_POINTS_AT_NOTHING.search(clause)
        if found:
            return {"shape": "nothing_named", "thing": None}
        for pattern, shape in ((CONFUSION_HARD_TO, "hard_to"),
                               (CONFUSION_SAID_OF_A_THING, "said_of_a_thing"),
                               (CONFUSION_MAKES_NO_SENSE, "said_of_a_thing"),
                               (CONFUSION_CANNOT_FOLLOW, "cannot_follow"),
                               (CONFUSION_HEAD_NOR_TAIL, "cannot_follow"),
                               (CONFUSION_BY_A_THING, "by_a_thing"),
                               (CONFUSION_HEAD_SPINNING, "head_spinning")):
            found = pattern.search(clause)
            if not found:
                continue
            before_cue = clause[:found.start("cue")] if "cue" in found.groupdict() else clause[:found.start()]
            if _a_confusion_ruled_out(before_cue):
                continue
            thing = _a_thing_trimmed(found.groupdict().get("thing"))
            return {"shape": shape, "thing": thing}
    return None
