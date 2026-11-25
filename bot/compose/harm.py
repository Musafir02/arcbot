import re

from . import pick

HURTING = "hurting_someone"

_HURT = re.compile(
    r"\b(?:kill|killing|murder|murdering|strangle|strangling|throttle|throttling|choke|choking|"
    r"stab|stabbing|shoot|shooting|poison|poisoning|punch|punching|hit|hitting|smack|smacking|"
    r"thump|thumping|whack|whacking|slap|slapping|kick|kicking|drown|drowning|deck|decking|"
    r"bash|bashing|batter|battering|gouge|gouging|clobber|clobbering|pummel|pummelling|"
    r"headbutt|headbutting|garrotte|garrote|hurt|hurting|smash|smashing|"
    r"shake|shaking|shook|shaken|"
    r"beat\s+up|beat\s+(?:the\s+)?(?:living\s+)?daylights\s+out\s+of|"
    r"do\s+(?:him|her|them)\s+in|knock\s+(?:him|her|them)\s+out|run\s+(?:him|her|them)\s+over|"
    r"set\s+fire\s+to|burn\s+down|get\s+(?:him|her|them)\s+back|get\s+my\s+own\s+back\s+on)\b")
_PERSON = re.compile(
    r"\b(?:him|her|them|"
    r"(?:his|her|their|your|my|our)\s+(?:face|head|teeth|nose|jaw)|"
    r"(?:(?:my|your|his|her|their|our|the)\s+)?"
    r"(?:boss|manager|husband|wife|partner|boyfriend|girlfriend|ex|fiance|fiancee|"
    r"mum|mom|dad|mother|father|brother|sister|sons?|daughters?|child(?:ren)?|kids?|"
    r"bab(?:y|ies)|toddlers?|infants?|newborns?|gran|nan|"
    r"grandma|grandad|grandmother|grandfather|aunt|uncle|cousin|in-laws?|"
    r"neighbour|neighbor|landlord|landlady|tenant|flatmate|housemate|roommate|"
    r"mate|friend|colleague|coworker|co-worker|teacher|headteacher|classmate|"
    r"stepmum|stepdad|stepson|stepdaughter|mother-in-law|father-in-law|"
    r"careworker|carer|nurse|doctor|dr|gp|dentist|social\s+worker|"
    r"referee|coach|vicar|priest|imam|rabbi|officer|policeman|policewoman|cop|"
    r"driver|cyclist|bus\s+driver|security\s+guard|bouncer|celebrity|politician|"
    r"(?:that|the)\s+(?:man|woman|bloke|guy|girl|lady|person|kid)|"
    r"those\s+(?:people|kids|children|men|women)|everyone|everybody))\b")
_THE_PERSON = re.compile(
    r"\b((?:my|your|his|her|their|our)\s+[a-z][a-z'-]*(?:\s+in[-\s]?laws?)?"
    r"|(?:that|the)\s+(?:man|woman|bloke|guy|lady|person|kid)|him|her|them)\b")
_IDIOM = re.compile(
    r"\b(?:kill\s+(?:time|the\s+(?:lights?|mood|music|engine|conversation))"
    r"|kill\s+two\s+birds|kill\s+it|killed\s+it|killing\s+(?:time|the\s+time)|"
    r"(?:could|can)\s+murder\s+a\b|murder\s+(?:a\s+)?(?:song|tune|curry|pint|coffee|brew)|"
    r"shake\s+it\s+off|shake\s+a\s+leg|shake\s+hands?|shake\s+(?:the\s+)?dust|"
    r"shake\s+up|shake\s+(?:some\s+)?sense\s+into|shake\s+a\s+fist|no\s+great\s+shakes|"
    r"hit\s+the\s+(?:road|sack|hay|shops?|gym|bottle|roof|ground|deck|bar|pub|town)"
    r"|hit\s+the\s+nail|hit\s+a\s+wall|hit\s+it\s+off|"
    r"beat\s+(?:the\s+traffic|the\s+queue|the\s+rush|the\s+clock|a\s+retreat|the\s+heat)"
    r"|beat\s+(?:the\s+)?(?:eggs|cream|batter)|"
    r"(?:slap|smack)\s+(?:some\s+)?(?:butter|sauce|paint)|"
    r"kick\s+(?:the\s+tyres|off|back\s+and\s+relax|it)|kick\s+(?:the\s+)?(?:habit|bucket)|"
    r"kick\s+(?:\w+\s+){0,3}out\b|"
    r"shoot\s+(?:hoops|some\s+hoops|the\s+shit)|shoot\s+through|"
    r"strangle\s+a\s+yawn|strangled\s+a\s+yawn)\b", re.I)

_WISH = re.compile(
    r"\b(?:want|wanna|wants|wanting|going|gonna|about|ready|tempted|could|would|might|may|will|"
    r"shall|should|need|needs|have|gotta|dying|half|like|feel)\b")
_BARE_LEAD = frozenset(("just", "please", "honestly", "god", "and", "then", "so", "ok", "okay",
                        "right", "look", "mate", "now", "sometimes", "nearly", "almost"))
_FEELINGS = re.compile(r"\bhurt(?:ing)?\s+(?:[a-z']+\s+){0,3}feelings?\b", re.I)

POOL = (
    "I'm not going to help with that, but something has pushed you a long way. What happened?",
    "That is a lot of anger to be carrying. What has actually happened?",
    "Fair to be that angry. What has been going on?",
)
NAMED = "Sounds like {person} has worn you down. What has been the worst of it?"
A_SMALL_CHILD = re.compile(r"\b(?:bab(?:y|ies)|infants?|newborns?|toddlers?|little one)\b", re.I)
A_CHILD = re.compile(r"\b(?:child|children|kid|kids|stepchild|stepchildren|sons?|daughters?)\b(?!"
                     r"[\s-]+in[\s-]?law)", re.I)
_IN_LAW = re.compile(r"^[\s-]+in[\s-]?laws?\b", re.I)
_JOINERS = frozenset((
    "because", "who", "that", "so", "and", "but", "or", "if", "when", "whenever", "while",
    "at", "on", "in", "to", "for", "with", "about", "over", "again", "today", "tonight", "now",
    "last", "this", "every", "is", "was", "has", "had", "does", "did", "will", "would", "keeps",
    "kept", "said", "says", "told", "tells", "called", "texted", "right", "still", "just",
    "tomorrow", "yesterday", "later", "soon",
))
BABY_LINES = (
    "Put some distance between you and them before anything else: out of the room, and put them "
    "down somewhere safe first. Then ring someone today - a partner, a friend, your health "
    "visitor or your GP - and say the words you just typed. Being this close to the edge is not a "
    "thing to sit on alone.",
    "Step out of the room before anything else, and put them down somewhere safe first. Then ring "
    "somebody today rather than later: a health visitor, a GP, or a friend who will come over. "
    "Every parent gets to the end of their rope, and the ones who say it out loud are the ones who "
    "get help.",
)
CHILD_LINES = (
    "Step away from them before you say another word: out of the room, and a walk if you can. "
    "Then ring somebody today - a partner, a friend, your GP - and say the words you just typed. "
    "Wanting to hurt your own child is not a thing to carry on your own.",
    "Put some distance between you and them now, and give it an hour before you speak to them "
    "again. Then tell one person today what you have just written - someone who will take it "
    "seriously. Being this far past the end of your rope is not something to sit on alone.",
)
OUTBURST = re.compile(r"\b(?:something|anything|whatever)\b[.,!?]*$", re.I)
OUTBURST_WALL = re.compile(r"\b(?:a|the) wall\b", re.I)
OUTBURST_VERB = re.compile(r"\b(?:hit|punch|smack|slap|kick|smash|thump|whack|headbutt|"
                           r"scream|shout|throw)\b", re.I)


_BODY = frozenset(("face", "head", "teeth", "nose", "jaw"))


def _person_said(clean):
    text = " ".join(str(clean or "").lower().split())
    hurt = _HURT.search(text)
    for span in ([text[hurt.start():]] if hurt else []) + [text]:
        said = _said_back(span)
        if said:
            return said
    return ""


def _said_back(text):
    found = _THE_PERSON.search(text)
    if not found:
        return ""
    if not _stands_on_its_own(text, found):
        return ""
    said = found.group(1).strip()
    if said.partition(" ")[2] in _BODY:
        return ""
    head, _, rest = said.partition(" ")
    if head in ("the", "that"):
        return ""
    swaps = {"my": "your", "our": "your", "his": "their", "her": "their", "its": "their"}
    if head in swaps:
        said = (swaps[head] + " " + rest).strip()
    elif said in ("him", "her"):
        said = "them"
    if said in ("their", "them", "your"):
        return ""
    return said


def reads_as_hurting_someone(clean):
    text = " ".join(str(clean or "").lower().replace("\u2019", "'").split())
    if not text or "?" in text:
        return False
    if _IDIOM.search(text):
        return False
    if re.search(r"\bkill(?:ing)?\s+(?:my|your|him|her)sel(?:f|ves)?\b|\bkill(?:ing)?\s+me\b", text):
        return False
    hurt = _HURT.search(text)
    if not hurt:
        return False
    if _FEELINGS.search(text):
        return False
    if not _PERSON.search(text[hurt.start():]):
        tail = text[hurt.start():hurt.start() + 40]
        if not (OUTBURST.search(tail)
                or (OUTBURST_WALL.search(tail) and OUTBURST_VERB.search(tail))):
            return False
    opening = text[:hurt.start()].strip(" ,;:-\u2013\u2014")
    if re.search(r"\b(?:dont|don'?t|do not|never|no longer|wouldnt|wouldn'?t|couldnt|couldn'?t|"
                 r"cant|can'?t|wont|won'?t)\b(?:\s+\w+){0,4}\s*$", opening):
        return False
    if re.search(r"\b(?:he|she|they|we|you|his|her|their|its)\b(?:\s+\w+){0,3}\s+"
                 r"(?:wants?|wanted|is|was|keeps|kept|might|may|will|would)\s*$", opening):
        return False
    if re.search(r"\b(?:i|i'm|im|i'd|id|ive)\b", opening):
        return bool(_WISH.search(opening))
    return not opening or all(word in _BARE_LEAD for word in opening.split())


def reads_as_our_reply(reply):
    text = " ".join(str(reply or "").split())
    if not text:
        return False
    if text in POOL or text in BABY_LINES or text in CHILD_LINES:
        return True
    head, _, tail = NAMED.partition("{person}")
    return bool(head and tail and text.startswith(head) and text.endswith(tail)
                and len(text) > len(head) + len(tail))


def _child_at_the_hurt(flat):
    hurt = _HURT.search(flat)
    if not hurt:
        return ""
    tail = flat[hurt.start():]
    first = _PERSON.search(tail)
    if not first:
        return ""
    phrase = first.group(0)
    if _IN_LAW.match(tail[first.end():]):
        return ""
    if not _stands_on_its_own(tail, first):
        return ""
    if A_SMALL_CHILD.search(phrase):
        return "small"
    return "child" if A_CHILD.search(phrase) else ""


def _stands_on_its_own(text, found):
    rest = text[found.end():].lstrip(" ,.;:!?-")
    if not rest:
        return True
    word = re.match(r"[a-z']+", rest)
    return bool(word) and word.group(0) in _JOINERS


def reply_for(clean, memory=None):
    if not reads_as_hurting_someone(clean):
        return None
    flat = " ".join(str(clean or "").lower().split())
    child = _child_at_the_hurt(flat)
    if child == "small":
        return pick(BABY_LINES, memory, clean)
    if child:
        return pick(CHILD_LINES, memory, clean)
    person = _person_said(clean)
    options = list(POOL)
    if person and person not in ("him", "her", "them"):
        options.append(NAMED.format(person=person))
    if not person:
        options = list(POOL)
    return pick(options, memory, clean)
