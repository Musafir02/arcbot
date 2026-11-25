import re

from ..compose.remark import person_pronouns
from . import relations

LEAD = r"^\W*(?:(?:and|but|so|oh|also|well|yeah|yep|ok|okay|right|alright|honestly|god)\W+)*"
PERSON = (r"(?P<who>he|she|they|him|her|them|"
          r"(?:my|our|his|her|their)\s+[a-z][a-z'-]*)")
DISLIKE = (r"(?:hates?|hated|dislikes?|disliked|cant\s+stand|cant\s+face|can\s*not\s+stand|"
           r"couldnt\s+stand|doesnt\s+like|does\s*not\s+like|didnt\s+like|isnt\s+keen\s+on|"
           r"not\s+keen\s+on|is\s+struggling\s+with|struggles\s+with|is\s+fed\s+up\s+with)")
LIKES = (r"(?:loves?|loved|adores?|adored|likes?|liked|enjoys?|enjoyed|is\s+loving|"
         r"is\s+enjoying|gets?\s+on\s+well\s+with|has\s+taken\s+to)")
FEELING = re.compile(LEAD + PERSON + r"\s+(?:(?:really|just|now|still|actually|absolutely|"
                     r"completely|totally|properly)\s+)*(?P<how>" + DISLIKE + r"|" + LIKES + r")"
                     r"\s+(?P<thing>.+?)\s*[.!]*$", re.I)
A_THING = re.compile(r"^(?:(?:the|his|her|their|its|my|our|a|an)\s+)?[a-z][a-z'-]*"
                     r"(?:\s+[a-z][a-z'-]*){0,3}$", re.I)
POINTS_BACK = re.compile(r"^(?:it|that|this|these|those|them|him|her|everything|all\s+of\s+it|"
                         r"the\s+whole\s+thing)$", re.I)
ASKING = re.compile(r"\?|\b(?:what|why|how|should|shall|can|could|would|any\s+idea|advice|help|"
                    r"do\s+you\s+think|is\s+it|does\s+it)\b", re.I)
DEFINITE = re.compile(r"^(?:the|his|her|their|its|my|our|this|that|these|those)\s+", re.I)
WORDS = frozenset("""it that this these those them him her everything all
    the a an and but so oh also well yeah yep ok okay right alright
    really just now still actually absolutely completely totally properly
    very quite bit lot little much more less""".split())

WITH_THING = {
    "no": (
        "{thingcap} is hard going for {person}, then. What's the worst part?",
        "That's a shame about {thing}. What's {person} finding hardest?",
        "{thingcap} isn't working for {person}, then. What would make the most difference?",
    ),
    "yes": (
        "That's good - {thingcap} is working for {person}, then. What does {they} like best?",
        "Good news. What is it about {thing} that {person} has taken to?",
        "That's the best news of the day, that one. What's {person} enjoying most about {thing}?",
    ),
}
WITHOUT_THING = {
    "no": (
        "That's hard going for {person}, then. What's the worst part?",
        "Not what you hoped for {person}. Which bit is worst?",
        "That's a shame. What's {person} finding hardest?",
    ),
    "yes": (
        "That's good news. What does {person} like best about it?",
        "Good to hear - what's {person} enjoying most?",
        "That's a good sign. What made the difference for {person}?",
    ),
}


def _the_last_person(text, memory):
    low = str(text or "").lower()
    match = FEELING.match(low)
    if not match:
        return "", ""
    who = match.group("who")
    if who.startswith(("my ", "our ")):
        return "your " + who.split()[-1], who.split()[-1]
    if who.startswith(("his ", "her ", "their ")):
        return "", who
    person = ""
    try:
        person = relations._person_from_pronoun(low, memory) or ""
    except Exception:
        person = ""
    if person and not re.match(r"^(?:my|our|your|his|her|their)\b", person):
        person = "your " + person
    return person, who


def reply_for(text, memory):
    low = " ".join(str(text or "").lower().split())
    if not low or ASKING.search(low):
        return None
    match = FEELING.match(low)
    if not match:
        return None
    person, _ = _the_last_person(low, memory)
    if not person:
        return None
    thing = match.group("thing").strip(" .,!;:")
    if not thing:
        return None
    back = bool(POINTS_BACK.match(thing))
    if not back:
        if not A_THING.match(thing):
            return None
        if not DEFINITE.match(thing) and not _an_earlier_turn(memory, low):
            return None
        if not DEFINITE.match(thing) and not _says_something(thing):
            return None
    if not _an_earlier_turn(memory, low) and not DEFINITE.match(thing):
        return None
    how = "no" if re.search(r"(?:^|\s)(?:" + DISLIKE + r")(?:\s|$)", match.group("how")) else "yes"
    pool = WITHOUT_THING[how] if back else WITH_THING[how]
    filled = [_fill(frame, person, thing if not back else "") for frame in pool]
    return _vary(filled, memory, low)


def _says_something(thing):
    words = [word for word in re.split(r"[^a-z']+", thing.lower()) if word]
    return bool(words) and any(word not in WORDS for word in words)


def _an_earlier_turn(memory, low):
    from .history import an_earlier_turn
    try:
        return an_earlier_turn(memory, low)
    except Exception:
        return False


def _fill(frame, person, thing):
    they = person_pronouns(person)[0]
    said = frame.replace("{person}", person).replace("{they}", they)
    if "{thing" in frame or "{Thing}" in frame:
        said = (said.replace("{thingcap}", thing[:1].upper() + thing[1:])
                    .replace("{Thing}", thing[:1].upper() + thing[1:])
                    .replace("{thing}", thing))
    return said[:1].upper() + said[1:]


def _vary(options, memory, line=""):
    from ..compose import pick
    return pick(options, memory, line)
