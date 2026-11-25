import re

from ..compose import pick

A_DAY_FOR_SOMEONE = re.compile(
    r"(?:\b(?:turns?|is|'s|am|'m|are|'re|re) \d+\b|\b(?:im|i'm|i am) \d+\b|\b\d+ (?:next|this|in|on)\b|"
    r"\bbirthday\b|\bbday\b)", re.I)
A_TIME = re.compile(
    r"\b(?:tonight|this evening|this morning|this afternoon|tomorrow|the day after tomorrow|"
    r"next (?:week|month|year|weekend|monday|tuesday|wednesday|thursday|friday|saturday|sunday)|"
    r"this weekend|at the weekend|on monday|on tuesday|on wednesday|on thursday|on friday|"
    r"on saturday|on sunday|in (?:january|february|march|april|may|june|july|august|september|"
    r"october|november|december)|in the (?:morning|afternoon|evening)|later today|"
    r"for the rest of the (?:day|week))\b", re.I)
A_STANDING_STATE = re.compile(
    r"\b(?:every (?:day|week|night|morning|month)|"
    r"(?:twice|three times|four times|five times|six times) a (?:day|week)|"
    r"\b(?:six|seven|five|four) days a week|"
    r"live with|live(s)? with|living with|"
    r"work(s)? (?:in|at|for|from|nights|shifts|weekends)|"
    r"have (?:two|three|four|five) (?:kids|children|jobs))\b", re.I)

A_TASTE = re.compile(
    r"^(?:and |so |but )?(?P<who>i|he|she|they|we|my (?:[\w']+ )?[\w']+)\s+"
    r"(?:really |just |absolutely |also |still )*"
    r"(?:loves?|likes?|enjoys?|prefers?|(?:is|are) (?:really |very |well )?(?:into|a (?:big )?fan of))\b",
    re.I)
A_TASTE_OF_A_PERSON = re.compile(r"\b(?:you|me|him|her|them|us)\s*[.!]*\s*$", re.I)
A_CRUSH = re.compile(r"\b(?:a (?:girl|boy|man|woman|lady|lad)|someone|somebody|anyone)\b", re.I)
A_PERSON_AS_OBJECT = re.compile(
    r"\b(?:mum|mom|mother|dad|father|son|daughter|kids?|children|boys?|girls?|wife|husband|"
    r"partner|brother|sister|nana|gran|grandma|grandad|granny|family|parents|baby|friend|"
    r"mates?|neighbours?)\b", re.I)

A_START = re.compile(
    r"\b(?:starts?|starting|begins?|goes? back|going back|finish(?:es)?|leaves?|left) "
    r"(?:year|school|college|uni|university|nursery|reception)\b|"
    r"\b(?:has|sits?|taking|takes) (?:his|her|their|the) (?:gcses?|exams?|a levels?|mocks?)\b", re.I)

SHE = ("daughter", "sister", "mum", "mother", "mam", "nan", "nana", "gran", "granny",
       "aunt", "auntie", "wife", "girlfriend", "partner", "niece", "cousin", "girl",
       "granddaughter", "stepmum", "stepdaughter", "mother in law", "daughter in law",
       "sister in law")
HE = ("son", "brother", "dad", "father", "grandad", "granddad", "uncle", "husband",
      "boyfriend", "nephew", "cousin", "boy", "grandson", "stepdad", "stepson",
      "father in law", "son in law", "brother in law")
THEY = ("kids", "children", "parents", "friends", "twins", "boys", "girls", "little one",
        "little ones", "toddler", "baby", "child")

A_DAY_TAILS = (
    "{Thing} \u2014 what are you planning for it?",
    "{Thing}. What would {subj} like to do?",
    "{Thing} \u2014 is there anything {subj} {has} asked for?",
    "{Thing}. What {be} {subj} thinking of doing?",
)
A_LIKED_TAILS = (
    "{Thing} \u2014 what got {them} into it?",
    "{Thing}. Is it a new thing, or {has} {subj} always been keen?",
    "{Thing} \u2014 what's the best bit of it for {them}?",
    "{Thing}. How long has that been going on?",
    "{Thing} \u2014 is that a recent thing, or a lifelong one?",
)
A_DOING_TAILS = (
    "{Thing} \u2014 how {be} {subj} feeling about it?",
    "{Thing} \u2014 how {be} {subj} feeling about it?",
    "{Thing}. How's it going so far?",
    "{Thing}. How's it going so far?",
    "{Thing} \u2014 {be} {subj} looking forward to it?",
)
A_STATE_TAILS = (
    "{Thing} \u2014 how's that working out?",
    "{Thing}. How's that treating you?",
    "{Thing} \u2014 what's that like?",
)


A_PAST = re.compile(
    r"\b(?:yesterday|last (?:night|week|weekend|month|year|summer|christmas|monday|tuesday|"
    r"wednesday|thursday|friday|saturday|sunday)|this (?:morning|afternoon)|earlier|ago|"
    r"used to|was going to|were going to|had|saw|met|went|got married|moved|spent|asked|rang|"
    r"kicked|took|cooked|bought|ate|paid|came|left|started|finished|arrived)\b", re.I)
MONEY = re.compile(
    r"\b(?:rent|savings|bill|bills|budget|wage|wages|salary|debt|loan|cost|price|payment|"
    r"money|credit card|overdraft|mortgage)\b", re.I)
A_MEASURE = re.compile(
    r"\b(?:foot|feet|ft|cm|centimetres?|metres?|stone|kilos?|kilograms?|pounds?|inches|inch)\b", re.I)
A_MONTHS = re.compile(r"\b\d+ months?\b|\bmonths? old\b", re.I)
NOT_AN_OCCASION = re.compile(r"\b(?:age|date of birth|dob|birthday|rent|savings)\b", re.I)
A_CORRECTION = re.compile(r"(?:^\s*(?:no|nope|sorry)\b|\b(?:i (?:said|meant|told you|didn't say|did not say))\b)", re.I)


def _the_day_is_the_point(clean, match):
    if len(A_DAY_FOR_SOMEONE.findall(clean)) > 1:
        return False
    if len(re.findall(r"\b\d{1,3}\b", clean)) > 1:
        return False
    return not re.search(r"\b(?:and|but|n)\b", clean[match.end():], re.I)


def _names_my(lower, word):
    return bool(re.search(r"\bmy (?:\w+ )?" + word + r"(?:s|'s|s')?\b", lower))


def _who(clean):
    lower = clean.lower()
    lower = re.sub(r"^\s*(?:and |so |but |well )?(?:they|he|she|people|someone|everyone)\s+"
                   r"(?:said|says|say|reckons?|thinks?|told me|tell me)\s+", "", lower)
    starts = re.match(r"^\s*(?:and |so |but |well )?(he|she|they|theyre|they're)\b", lower)
    if starts:
        who = starts.group(1)
        who = "they" if who.startswith("they") else who
        return who, ("are" if who == "they" else "is")
    for word in THEY:
        if _names_my(lower, word):
            return "they", "are"
    for word in SHE:
        if _names_my(lower, word):
            return "she", "is"
    for word in HE:
        if _names_my(lower, word):
            return "he", "is"
    return "you", "are"


def _said_before(memory):
    for turn in (memory or {}).get("turns") or []:
        if isinstance(turn, dict) and str(turn.get("bot") or "").strip():
            return True
    return False


def the_opening(thing, clean, memory):
    if not thing or not clean:
        return None
    if _said_before(memory):
        return None
    if A_PAST.search(clean) or A_MEASURE.search(clean) or A_MONTHS.search(clean):
        return None
    if A_CORRECTION.search(clean):
        return None
    if MONEY.search(clean) or MONEY.search(thing) or NOT_AN_OCCASION.search(thing):
        return None
    subj, be = _who(clean)
    has = "have" if subj in ("you", "they") else "has"
    them = {"you": "you", "she": "her", "he": "him", "they": "them"}.get(subj, "you")
    taste = A_TASTE.match(clean)
    if taste and (A_TASTE_OF_A_PERSON.search(thing) or A_CRUSH.search(clean)
                  or A_PERSON_AS_OBJECT.search(clean[taste.end():])
                  or " but " in clean[taste.end():]):
        taste = None
    if taste:
        pool = A_LIKED_TAILS
    day = None if taste else A_DAY_FOR_SOMEONE.search(clean)
    if day and _the_day_is_the_point(clean, day) and not NOT_AN_OCCASION.search(thing):
        pool = (tuple(t for t in A_DAY_TAILS if "asked for" not in t) if subj == "you"
                else A_DAY_TAILS)
        if subj == "you":
            pool = tuple("{Thing} \u2014 anything you're marking it with?"
                         if "would {subj} like to do" in tail else tail for tail in pool)
    elif day:
        return None
    elif taste:
        pass
    elif A_TIME.search(clean) or A_START.search(clean):
        pool = A_DOING_TAILS
    elif A_STANDING_STATE.search(clean):
        pool = A_STATE_TAILS
    else:
        return None
    said = pick(pool, memory, clean).format(Thing=thing[:1].upper() + thing[1:],
                                            subj=subj, be=be, has=has, them=them)
    return " ".join(said.split())
