import re

from .fallback import PUNT, _choose
from ..understanding.kinds import names_a_claim


RULED_OUT = (
    (re.compile(r"^(?:and\s+|but\s+)?not\s+(?P<thing>(?:a|an|any|the)\s+[a-z][a-z' ]{0,24})$"),
     True),
    (re.compile(r"^(?:and\s+|but\s+)?not\s+(?P<thing>[a-z][a-z' ]{0,20}s)$"), False),
    (re.compile(r"^(?:and\s+|but\s+)?not\s+(?P<thing>[a-z][a-z' ]{0,20}\s+related)$"), False),
    (re.compile(r"^(?:and\s+|but\s+)?not\s+(?:too|much)\s+(?P<thing>[a-z][a-z' ]{1,20})$"),
     False),
    (re.compile(r"^(?:and\s+|but\s+)?nothing\s+(?P<thing>[a-z][a-z' ]{1,24})$"), False),
    (re.compile(r"^(?:and\s+|but\s+)?(?:i|we)\s+(?:really\s+|just\s+|actually\s+|personally\s+)?"
                r"(?:dont|don't|do\s+not|didnt|did\s+not|never)\s+want\s+"
                r"(?P<thing>trouble|hassle|aggro|drama|upset|bother)$"), False),
    (re.compile(r"^(?:and\s+|but\s+)?(?:i|we)\s+(?:really\s+|just\s+|actually\s+|personally\s+)?"
                r"(?:dont|don't|do\s+not|didnt|did\s+not|never)\s+want\s+to\s+"
                r"(?P<thing>(?:fall\s+out|falling\s+out|argue|fight|quarrel|kick\s+up\s+a\s+fuss|"
                r"make\s+a\s+fuss|get\s+into\s+it))$"),
     False),
    (re.compile(r"^(?:and\s+|but\s+)?(?:i|we)\s+(?:really\s+|just\s+|actually\s+|personally\s+)?"
                r"(?:dont|don't|do\s+not|didnt|did\s+not|never)\s+"
                r"(?:like|want|have|own|use|need|rate|fancy)\s+"
                r"(?P<thing>(?:a|an|any|the|my|another)\s+[a-z][a-z' ]{0,24})$"), True),
    (re.compile(r"^(?:and\s+|but\s+|no,?\s+|nah,?\s+)?(?:it|that|this)(?:'s|s)?\s+"
                r"(?:is\s+not|isnt|isn't|not)\s+"
                r"(?P<thing>(?:a|an|any|the|my|another)\s+[a-z][a-z' ]{0,24})$"), True),
    (re.compile(r"^(?:and\s+|but\s+|no,?\s+|nah,?\s+)?(?:it|that|this)(?:'s|s)?\s+"
                r"(?:is\s+not|isnt|isn't|not)\s+(?P<thing>[a-z][a-z' ]{1,20}s)$"), False),
)
RULED_OUT_WORDS = frozenset(("thing", "things", "anything", "something", "that", "this",
                             "which", "what", "any", "more", "much", "needs", "need", "uses",
                             "use", "takes", "take", "gets", "get", "has", "have", "requires",
                             "require", "wants", "want", "please", "thanks", "really", "very"))
RULED_OUT_QUALITY = frozenset((
    "bad", "good", "sad", "happy", "awful", "terrible", "horrible", "weird", "wrong", "fine",
    "ok", "okay", "sure", "nice", "lovely", "great", "better", "worse", "best", "worst",
    "big", "small", "little", "long", "short", "new", "old", "easy", "hard", "difficult",
    "expensive", "cheap", "different", "same", "busy", "tired", "stressed", "ill", "sick",
))
RULED_OUT_NOT_A_THING = frozenset((
    "case", "point", "problem", "issue", "fact", "joke", "idea", "whole", "kind", "sort",
    "type", "way", "matter", "question", "answer", "reason", "truth", "deal", "end",
    "yet", "either", "though", "well", "thanks", "is", "are", "was", "were", "be", "been",
    "going", "happening", "happened", "here", "there", "now", "ever", "again", "else", "right",
    "left", "much", "more", "less", "least", "still", "even", "already", "quite", "rather",
    "able", "possible", "worth", "enough", "true", "false", "sure", "wrong", "fine",
))
RULED_OUT_TAIL = re.compile(r"\s+(?:related|based|ish|esque)$")
RULED_OUT_PREP = re.compile(r"\s+(?:of|to|on|for|by|from|about)\s+")
RULED_OUT_OPENS_WITH = re.compile(r"^(?:with|without|in|on|at|for|about|of|to)\b")
RULED_OUT_SOFTENING = re.compile(r"^(?:and\s+|but\s+)?nothing\s+(?:too|very|that|which|of)\b")
RULED_OUT_KEEPS = re.compile(r"^(?:a|an|any|the|my|another)\s+")
RULED_OUT_REPLIES_PLAIN = (
    "There's no {thing} in that answer, so it still stands. {opening}",
    "That one never mentions {thing} at all, so nothing changes. {opening}",
    "Nothing there was about {thing}, so the answer holds. {opening}",
)
RULED_OUT_REPLIES_THE = (
    "None of that was {thing} - the answer still stands. {opening}",
    "That one never mentions {thing} at all, so nothing changes. {opening}",
    "Nothing there was {thing}, so the answer holds. {opening}",
)
A_ROW_BETWEEN_PEOPLE = frozenset((
    "row", "fuss", "scene", "argument", "argy bargy", "argie bargie", "fight", "drama",
    "falling out", "fall out", "confrontation", "trouble", "hassle", "aggro", "upset",
    "bad feeling", "bad blood", "stink", "carry on", "atmosphere",
))
A_ROW_NAMES = {
    "fall out": "falling out", "falling out": "falling out", "argue": "argument",
    "quarrel": "argument", "get into it": "argument", "fight": "fight",
    "kick up a fuss": "fuss", "make a fuss": "fuss", "row": "row", "trouble": "trouble",
    "hassle": "hassle", "bother": "bother", "aggro": "aggro", "drama": "drama", "upset": "upset",
}
RULED_OUT_REPLIES_A_ROW = (
    "Fair enough - no {thing} needed. {opening}",
    "Quite right, no {thing} wanted. {opening}",
    "Fair enough: one calm sentence, no {thing}. {opening}",
)
RULED_OUT_CLASS = frozenset((
    "tablets", "pills", "painkillers", "painkiller", "medication", "medicine", "medicines",
    "drugs", "antibiotics", "supplements", "vitamins", "inhalers", "creams", "series",
    "episodes", "thriller", "thrillers", "horror", "comedies", "documentaries", "meat",
    "dairy", "gluten", "carbs", "carbohydrates", "sugar", "chemicals", "screens", "toys",
))
RULED_OUT_INSTANCES = {
    "tablets": frozenset(("paracetamol", "ibuprofen", "aspirin", "codeine", "antihistamine",
                          "melatonin", "sertraline", "tablet", "pill", "painkiller", "dose")),
    "pills": frozenset(("paracetamol", "ibuprofen", "aspirin", "codeine", "antihistamine",
                        "melatonin", "pill", "tablet", "painkiller")),
    "painkillers": frozenset(("paracetamol", "ibuprofen", "aspirin", "codeine", "painkiller")),
    "painkiller": frozenset(("paracetamol", "ibuprofen", "aspirin", "codeine", "painkiller")),
    "medication": frozenset(("paracetamol", "ibuprofen", "tablet", "pill", "dose", "prescription")),
    "medicine": frozenset(("paracetamol", "ibuprofen", "tablet", "pill", "dose")),
    "medicines": frozenset(("paracetamol", "ibuprofen", "tablet", "pill", "dose")),
    "drugs": frozenset(("paracetamol", "ibuprofen", "antibiotic", "painkiller", "tablet")),
    "antibiotics": frozenset(("antibiotic", "penicillin", "amoxicillin")),
    "supplements": frozenset(("supplement", "vitamin", "iron", "magnesium", "omega")),
    "vitamins": frozenset(("vitamin", "supplement", "iron", "magnesium", "omega")),
    "creams": frozenset(("cream", "ointment", "lotion", "gel")),
    "series": frozenset(("series", "episode", "episodes", "season", "seasons", "film", "films",
                         "movie", "movies")),
    "episodes": frozenset(("episode", "series", "season", "film", "films", "movie", "movies")),
    "thriller": frozenset(("thriller", "murder", "mystery", "crime", "detective", "suspense",
                           "serial", "killer")),
    "thrillers": frozenset(("thriller", "murder", "mystery", "crime", "detective", "suspense",
                            "serial", "killer")),
    "horror": frozenset(("horror", "scary", "ghost", "haunted", "frightening")),
    "meat": frozenset(("meat", "chicken", "beef", "pork", "lamb", "bacon", "sausage", "mince",
                       "steak", "ham", "turkey")),
    "dairy": frozenset(("dairy", "milk", "cheese", "butter", "cream", "yoghurt", "yogurt")),
    "gluten": frozenset(("gluten", "bread", "pasta", "flour", "wheat", "couscous", "barley")),
    "carbs": frozenset(("rice", "pasta", "bread", "potato", "potatoes", "flour")),
    "carbohydrates": frozenset(("rice", "pasta", "bread", "potato", "potatoes", "flour")),
    "sugar": frozenset(("sugar", "honey", "syrup", "sweetener", "jam")),
    "chemicals": frozenset(("vinegar", "bleach", "ammonia", "caustic", "solvent", "spray",
                            "bicarbonate")),
    "screens": frozenset(("screen", "phone", "television", "tv", "laptop", "monitor", "tablet")),
    "toys": frozenset(("toy", "lego", "blocks", "play")),
}


RULED_OUT_NAMED = re.compile(r"\*[^*]{2,}\*|\"[^\"]{2,}\"|\u201c[^\u201d]{2,}\u201d")


def _named_picks(answer):
    return len(RULED_OUT_NAMED.findall(str(answer or ""))) > 1


def _class_of(word):
    word = word.strip("'")
    if not word:
        return frozenset()
    forms = {word, word + "s"}
    if word.endswith("es"):
        forms.add(word[:-2])
    if word.endswith("s"):
        forms.add(word[:-1])
    classes = {form for form in forms if form in RULED_OUT_CLASS}
    if not classes:
        stem = word[:7]
        if len(stem) >= 6:
            classes = {key for key in RULED_OUT_CLASS if key.startswith(stem)}
    if not classes:
        for key, members in RULED_OUT_INSTANCES.items():
            if forms & members:
                classes.add(key)
    return frozenset(classes)


def _a_class_word(word):
    forms = {word, word + "s"}
    if word.endswith("es"):
        forms.add(word[:-2])
    if word.endswith("s"):
        forms.add(word[:-1])
    if forms & RULED_OUT_CLASS:
        return True
    stem = word[:7]
    return len(stem) >= 6 and any(key.startswith(stem) for key in RULED_OUT_CLASS)


def _an_answer_of_that_class(answer, thing):
    said = set(re.findall(r"[a-z']+", str(answer or "").lower()))
    for word in RULED_OUT_KEEPS.sub("", thing).split():
        classes = _class_of(word)
        for key in classes:
            forms = {key, key + "s"}
            if key.endswith("s"):
                forms.add(key[:-1])
            if forms & said:
                return True
            if RULED_OUT_INSTANCES.get(key, frozenset()) & said:
                return True
            stem = key[:7]
            if len(stem) >= 6 and any(said_word.startswith(stem) for said_word in said):
                return True
        if classes and not _a_class_word(word) and _named_picks(answer):
            return True
    return False


RULED_OUT_KEEP_WHOLE = re.compile(
    r"\b(?:999|911|112|111|ambulance|a&e|casualty|emergency|urgent care|999 line)\b")
RULED_OUT_SYMPATHY = re.compile(
    r"\b(?:sorry|sad news|passed away|grief|grieving|bereave\w*|condolence\w*|"
    r"miss (?:him|her|them))\b")

RULED_OUT_OPENING = 120
RULED_OUT_WHOLE = 210


MANNERS = re.compile(r"(?:[\s,!.?]*\b(?:pls+|plz|please|pleas|plse|thx|thanx|thanks|thankyou|"
                     r"thank\s+you|ta|ty|cheers|cheerio|mate|m8|fella|buddy|bud|pal|x|xx|xxx)"
                     r"\b)+[\s,!.?]*$")


def _without_the_manners(clean):
    return MANNERS.sub("", str(clean or "")).strip()


RULED_OUT_THEN_ELSE = re.compile(
    r"[\s,;:-]+(?:then\s+|and\s+)?(?:so\s+)?(?:what|anything|something)\s+else"
    r"(?:\s+[a-z']+){0,4}\s*[.?!]*$")
RULED_OUT_NOT_THEN_ELSE = (
    (re.compile(r"^(?:and\s+|but\s+)?not\s+(?P<thing>(?:a|an|any|the)\s+[a-z][a-z' ]{0,24})$"),
     True),
    (re.compile(r"^(?:and\s+|but\s+)?not\s+(?P<thing>[a-z][a-z' ]{1,24})$"), False),
)
RULED_OUT_NO_THEN_ELSE = (
    (re.compile(r"^(?:no|nah|nope|no,|nah,|nope,)\s+(?P<thing>(?:a|an|any|the)\s+[a-z][a-z' ]{0,24})$"),
     True),
    (re.compile(r"^(?:no|nah|nope|no,|nah,|nope,)\s+(?P<thing>[a-z][a-z' ]{1,24})$"), False),
)


def _ruled_out_thing(clean):
    clean = _without_the_manners(clean)
    asked_for_the_other = bool(RULED_OUT_THEN_ELSE.search(clean))
    if asked_for_the_other:
        clean = RULED_OUT_THEN_ELSE.sub("", clean).strip(" ,;:-")
    if not clean or len(clean.split()) > 7:
        return "", False
    if RULED_OUT_SOFTENING.match(clean):
        return "", False
    thing, kept = "", False
    patterns = RULED_OUT + ((RULED_OUT_NOT_THEN_ELSE + RULED_OUT_NO_THEN_ELSE)
                            if asked_for_the_other else ())
    for pattern, with_determiner in patterns:
        found = pattern.match(clean)
        if found:
            thing, kept = found.group("thing"), with_determiner
            break
    else:
        return "", False
    thing = " ".join(word for word in thing.split() if word not in RULED_OUT_WORDS)
    thing = RULED_OUT_TAIL.sub("", thing).strip(" .,!?'\"")
    if not thing or RULED_OUT_PREP.search(thing) or RULED_OUT_OPENS_WITH.search(thing):
        return "", False
    if any(word in RULED_OUT_QUALITY for word in thing.split()):
        return "", False
    if any(word in RULED_OUT_NOT_A_THING for word in thing.split()):
        return "", False
    if clean.startswith("nothing") and any(names_a_claim(word) for word in thing.split()):
        return "", False
    kept = bool(kept and RULED_OUT_KEEPS.match(thing))
    words = thing.split()
    if len(words) > 4 or not all(word.isalpha() for word in words):
        return "", False
    return thing, kept


RULED_OUT_PARTICLES = frozenset("""out off up down away back over through around about along
together home here there it self selves""".split())


def _a_row_thing(thing):
    bare = RULED_OUT_KEEPS.sub("", " ".join(str(thing or "").split()))
    if bare in A_ROW_NAMES:
        return A_ROW_NAMES[bare]
    for phrase in sorted(A_ROW_NAMES, key=len, reverse=True):
        if bare == phrase or bare.startswith(phrase + " "):
            return A_ROW_NAMES[phrase]
    return ""


def _names_it(answer, thing):
    said = set(re.findall(r"[a-z']+", answer.lower()))
    words = RULED_OUT_KEEPS.sub("", thing).split()
    carrying = [word for word in words if word not in RULED_OUT_PARTICLES]
    if carrying:
        words = carrying
    for word in words:
        forms = {word, word + "s", word + "es", word + "ing", word + "ed"}
        if word.endswith("s"):
            forms.add(word[:-1])
        if word.endswith("es"):
            forms.add(word[:-2])
        if forms & said:
            return True
    return False


RULED_OUT_NO_ANSWER = ("sorry", "that sounds", "sounds like", "i'm listening", "i am listening",
                       "got it", "thanks for telling", "no worries", "of course", "noted",
                       "fair enough", "that's rough", "thats rough")


def _the_whole_answer(memory):
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    if not turns:
        return ""
    last = " ".join(str(turns[-1].get("bot") or "").split())
    if len(last) < 60 or last.endswith("?"):
        return ""
    if any(punt in last.lower() for punt in PUNT):
        return ""
    if last.lower().startswith(RULED_OUT_NO_ANSWER):
        return ""
    if RULED_OUT_KEEP_WHOLE.search(last.lower()) or RULED_OUT_SYMPATHY.search(last.lower()):
        return ""
    return last


def _the_standing_part(answer):
    if len(answer) <= RULED_OUT_WHOLE:
        return " ".join(answer.split())
    first = re.split(r"(?<=[.!?])\s", answer.strip())[0]
    head, _, tail = first.partition(":")
    if tail and len(head.split()) <= 8:
        first = tail
    first = " ".join(first.split())
    if len(first) <= RULED_OUT_OPENING:
        return first
    cut = first[:RULED_OUT_OPENING]
    stretches = [cut[:cut.rfind(mark)].strip(" ,;:-")
                 for mark in ("; ", ", ", " - ", " and ") if mark in cut]
    stretches = [stretch for stretch in stretches if len(stretch.split()) >= 4]
    if not stretches:
        return ""
    return max(stretches, key=len)


CLAIM_OF_FAILURE = re.compile(
    r"^\W*(?:(?:ok|okay|so|well|yeah|yep|yes|and|but|oh|right|alright|no|nope|nah|still|now)\W+)*"
    r"(?:nothing|nowt|none\s+of\s+(?:it|that|them|these|those)|neither\s+of\s+(?:them|those|it))"
    r"(?:\s+\w+){0,5}\W*$")
CLAIM_SMALL = frozenset("""at all so far yet again now still really just about on with me my it
this that them those these any more much either the a an of in for to day days week weeks moment
while times time one bit lot lots out up down been has have had is was are were am do does did""".split())
CLAIM_LEADS = ("Then it is the next part that matters: {step}",
               "Then take it a step further: {step}",
               "Then the next step: {step}",
               "Next: {step}")
CLAIM_CONDITION = re.compile(r"^(?:if|when|once|unless|before|after|until)\b", re.I)
STEP_ELSEWHERE = re.compile(r"\b(?:gp|doctor|nurse|pharmacist|chemist|dentist|vet|optician|midwife|"
                            r"health visitor|111|999|911|helpline|a&e|hospital|council|"
                            r"citizens advice|plumber|electrician|engineer|gas safe|mechanic|"
                            r"locksmith|roofer|builder|technician|specialist|repair shop)\b", re.I)
CLAIM_LEADS_IF = ("The next thing to try: {step}", "Next: {step}",
                  "Then the next check: {step}")


def _a_claim_of_failure(clean, memory):
    if not CLAIM_OF_FAILURE.match(clean):
        return ""
    words = re.findall(r"[a-z']+", clean)
    while words and words[0] in ("nothing", "nowt", "none", "neither", "of", "ok", "okay",
                                 "so", "well", "yeah", "yep", "yes", "and", "but", "oh",
                                 "right", "alright", "no", "nope", "nah", "still", "now"):
        words.pop(0)
    if not words or not any(names_a_claim(word) for word in words):
        return ""
    if any(word not in CLAIM_SMALL and not names_a_claim(word) for word in words):
        return ""
    answer = _the_whole_answer(memory)
    if not answer:
        return ""
    if answer.rstrip().endswith("?"):
        return ""
    try:
        from ..memory.repeat import _later_part
        step = " ".join(str(_later_part(clean, answer) or "").split())
    except Exception:
        return ""
    if len(step.split()) < 4 or not step:
        return ""
    conditional = bool(CLAIM_CONDITION.match(step))
    if not conditional and not STEP_ELSEWHERE.search(step):
        return ""
    step = step[:1].upper() + step[1:]
    pool = CLAIM_LEADS_IF if conditional else CLAIM_LEADS
    return _choose([line.format(step=step) for line in pool], memory or {}, clean)


PET_NAMED = re.compile(
    r"\b(?:dog|dogs|puppy|puppies|pup|pups|cat|cats|kitten|kittens|rabbit|rabbits|bunny|"
    r"bunnies|hamster|hamsters|gerbil|gerbils|guinea pig|guinea pigs|parrot|parrots|budgie|"
    r"budgies|bird|birds|horse|horses|pony|ponies|fish|goldfish|tortoise|tortoises|snake|"
    r"snakes|lizard|lizards|ferret|ferrets|pet|pets)\b")

WANTED_ONE = re.compile(
    r"\b(?:want|wants|wanted|would like|'d like|after|thinking (?:of|about)|considering|"
    r"planning to get|should (?:i|we) get|can (?:i|we) get|shall we get|get (?:a|an)|"
    r"getting (?:a|an)|looking at getting)\b")


def _a_pet_turned_down(clean, memory):
    if not PET_NAMED.search(clean):
        return False
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    for turn in reversed(turns[-2:]):
        before = " ".join(str(turn.get("user") or "").split()).lower()
        if before:
            return bool(PET_NAMED.search(before) and WANTED_ONE.search(before))
    return False


TITLES_IN_ANSWER = re.compile(r"\*[^*]{2,60}\*")
KINDS_A_LIST_CAN_SWAP = ("horror", "scary", "frightening", "creepy", "comedy", "comedies",
                         "funny", "romance", "romantic", "sad", "documentary", "gory")


def _a_list_that_can_be_swapped(answer, thing):
    words = RULED_OUT_KEEPS.sub("", " ".join(str(thing or "").split())).split()
    if not any(word in KINDS_A_LIST_CAN_SWAP for word in words):
        return False
    return len(TITLES_IN_ANSWER.findall(answer)) >= 2


def _rules_out_what_i_never_said(text, memory):
    clean = " ".join(str(text or "").lower().replace("\u2019", "'").split())
    thing, kept = _ruled_out_thing(clean)
    if not thing:
        return "", False, ""
    if _a_pet_turned_down(clean, memory):
        return "", False, ""
    answer = _the_whole_answer(memory)
    if not answer or _names_it(answer, thing):
        return "", False, ""
    if _a_list_that_can_be_swapped(answer, thing):
        return "", False, ""
    if _an_answer_of_that_class(answer, thing):
        return "", False, ""
    opening = _the_standing_part(answer)
    if not opening or _names_it(opening, thing):
        return "", False, ""
    return (thing if kept else RULED_OUT_KEEPS.sub("", thing)), kept, opening


def _ruled_out_reply(memory, clean):
    thing, kept, opening = _rules_out_what_i_never_said(clean, memory)
    if not thing:
        return ""
    opening = opening[:1].upper() + opening[1:]
    row = _a_row_thing(thing)
    if row:
        return _choose([line.format(thing=row, opening=opening)
                        for line in RULED_OUT_REPLIES_A_ROW], memory, clean)
    pool = RULED_OUT_REPLIES_THE if kept else RULED_OUT_REPLIES_PLAIN
    if not kept and thing.split()[-1].endswith("s"):
        pool = RULED_OUT_REPLIES_PLAIN[1:]
    return _choose([line.format(thing=thing, opening=opening) for line in pool], memory, clean)




def reply_for(text, memory):
    try:
        clean = " ".join(str(text or "").lower().replace("\u2019", "'").split())
        claim = _a_claim_of_failure(clean, memory)
        if claim:
            return claim
        return _ruled_out_reply(memory, clean)
    except Exception:
        return ""


def takes_as_it_comes(text, memory):
    try:
        clean = " ".join(str(text or "").lower().replace("\u2019", "'").split())
        if _a_claim_of_failure(clean, memory):
            return True
        thing, _kept, _opening = _rules_out_what_i_never_said(text, memory)
        return bool(thing)
    except Exception:
        return False
