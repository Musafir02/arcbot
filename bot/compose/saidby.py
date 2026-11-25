import re

from . import pick

QUOTED = re.compile(r'"([^"]{3,300})"|\u201c([^\u201d]{3,300})\u201d')
SAID = re.compile(
    r"\b(?P<who>(?:my|his|her|their|our|the)\s+[a-z][a-z'-]*(?:\s+(?:in[-\s]?laws?|wife|husband))?"
    r"|he|she|they|someone|somebody|everyone|everybody|a\s+friend|a\s+mate)\b"
    r"(?:\s+[a-z']+){0,3}?\s+"
    r"(?:said|says|saying|texted|texts|text|messaged|messages|emailed|emails|wrote|writes|"
    r"goes|went|was\s+like|shouted|shouts|yelled|yells|screamed|screams|whispered|whispers|"
    r"keeps?\s+(?:saying|shouting|telling\s+me)|kept\s+(?:saying|shouting|telling\s+me)|"
    r"has\s+said|had\s+said|told\s+me|tells\s+me)\b", re.I)
SAID_TO_ME = re.compile(r"\b(?:said|says|texted|texts|messaged|emailed|told\s+me)\s+(?:to\s+)?(?:me)?\b",
                        re.I)
A_WISH = re.compile(
    r"\b(?:i|we)\s+(?:want|wants|wanted|need|needs|needed|would\s+like|d\s+like|dont|don'?t)\b"
    r"|\b(?:i|im|i'm|we|we're|weve|we've)\s+(?:am\s+|are\s+|is\s+)?(?:going\s+to|leaving|done|out)\b"
    r"|\b(?:i|we)\s+miss\b"
    r"|\bi\s+(?:want|need)\s+out\b"
    r"|\bwe\s+need\s+to\s+talk\b"
    r"|\b(?:its|it'?s)\s+over\b", re.I)
A_DECLARATION = re.compile(r"\b(?:i|we)\s+(?:really\s+|still\s+)?(?:love|hate)\s+(?:you|him|her|them)\b",
                           re.I)
NOT_SPOKEN_TO_THEM = re.compile(
    r"\b(?:note|notes|sign|signs|label|notice|letter|email\s+says|form|ticket|invoice|bill|"
    r"receipt|menu|website|app|screen|message\s+on|instructions|recipe|book|leaflet|poster|"
    r"song|songs|lyric|lyrics|radio|telly|tv|advert|advertisement|film|movie|poem|poems|"
    r"show|podcast|headline|article|quote)\b",
    re.I)
OWN_SAYING = re.compile(r"(?:said|say|says|texted|text|texts|messaged|message|emailed|email|wrote|"
                        r"told|replied|answered|sent)", re.I)
OWN_SUBJECT = frozenset("i i'd id we we'd weve i've ive".split())
OWN_FILLER = frozenset("just also only then never always still even actually already finally "
                       "once today yesterday".split())

THEY_SAID = (
    "{Who}'s saying that is a lot to sit with. How are you taking it?",
    "That's a big thing to have said to you. What's going round your head?",
    "Hard to be on the end of that one. Do you want to talk it through?",
)
THEY_SAID_AGAIN = (
    "{Who} keeps coming back to it, and that wears you down more than one saying does. What do "
    "you say back?",
    "Said often enough it stops being about the words. What do you think is behind it?",
)
THEY_DECLARED = (
    "That's a big thing to have said to you. What went through your head?",
    "Words like that change the room. How do you feel about it?",
    "Hard to know what to do with being told that. What do you want to say back?",
)
ASKING_ABOUT_IT = re.compile(
    r"\?|\b(?:what does that mean|what do i say|what should i say|what do i reply|what should i "
    r"reply|can (?:he|she|they) do that|is that allowed|what do i do|should i)", re.I)
WHO = re.compile(r"\b(my|his|her|their|our|the)\s+([a-z][a-z'-]*)\b", re.I)


def the_quotation(text):
    found = QUOTED.search(str(text or ""))
    if not found:
        return ""
    return " ".join((found.group(1) or found.group(2) or "").split())


def _the_one_who_said_it(text):
    found = SAID.search(str(text or ""))
    if not found:
        return ""
    who = " ".join(found.group("who").lower().split())
    if who in ("he", "she", "they", "someone", "somebody", "everyone", "everybody"):
        return who
    return who


def _before_the_quotation(text):
    found = QUOTED.search(text)
    return text[:found.start()] if found else ""


def said_by_the_person(text):
    words = [word.strip(",.!?;:") for word in _before_the_quotation(text).lower().split()]
    for index in range(len(words) - 1, -1, -1):
        if not OWN_SAYING.fullmatch(words[index]):
            continue
        for word in reversed(words[:index]):
            if word in OWN_FILLER:
                continue
            return word in OWN_SUBJECT
        return False
    return False


def reads_as_somebody_elses_wish(text):
    said = " ".join(str(text or "").lower().split())
    if not said or '"' not in said and "\u201c" not in said:
        return False
    quoted = the_quotation(said)
    if not quoted or len(quoted.split()) < 2:
        return False
    if not (A_WISH.search(quoted) or A_DECLARATION.search(quoted)):
        return False
    if NOT_SPOKEN_TO_THEM.search(said) or ASKING_ABOUT_IT.search(said):
        return False
    if said_by_the_person(said):
        return False
    return bool(SAID.search(said) or SAID_TO_ME.search(said))


A_PRONOUN_HEAD = frozenset("he she they someone somebody everyone everybody".split())


def _who_phrase(text):
    who = _the_one_who_said_it(text)
    if not who or who.split()[0] not in A_PRONOUN_HEAD:
        return ""
    return who[:1].upper() + who[1:]


def _fits_the_head(line, who):
    return "{Who}" not in line or bool(who)


def _the_card_keeps_its_turn(text, memory):
    if not text:
        return False
    try:
        from ..modules import answers
    except Exception:
        return False
    try:
        return bool(answers.respond(text, {} if memory is None else memory))
    except Exception:
        return False


def reply_for(text, memory=None):
    if not reads_as_somebody_elses_wish(text):
        return None
    if _the_card_keeps_its_turn(text, memory):
        return None
    said = " ".join(str(text or "").lower().split())
    who = _who_phrase(said)
    if A_DECLARATION.search(the_quotation(said)) and not A_WISH.search(the_quotation(said)):
        pool = list(THEY_DECLARED)
    else:
        again = bool(re.search(
            r"\b(?:keeps?\s+(?:saying|shouting|on)|kept\s+(?:saying|shouting|on)|always\s+says|"
            r"says\s+it\s+again|over\s+and\s+over)\b", said))
        lines = THEY_SAID_AGAIN if again else THEY_SAID
        pool = [line for line in lines if _fits_the_head(line, who)]
    return pick([line.format(Who=who) for line in pool], memory, said)
