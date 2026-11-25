import re

from ..compose.badnews import reads_as_bad_news
from . import topics

_NOTHING_ELSE = r"(?:\s+(?:now|next|anymore|any more|at all))?"
_STATE_SOURCE = (r"(?:im|i am|were|we are)\s+(?:just\s+)?(?:so\s+)?(?:lost|stuck)\b"
                 r"(?:\s+(?:in\s+a\s+rut|on|with|about)\s+(?:this|it|that))?")
_STATE = re.compile(r"^\W*(?:" + _STATE_SOURCE + r")\s*(?:\?|\.|!)*\s*$")

_LEADS = r"(?:(?:and|but|so|well|oh|honestly|then|i mean|like|just|seriously|really)\s+)*"
_ASK_BODY = (
    r"(?:"
    r"(?:i|we)(?:'ve| have|'m| am)?\s+(?:just\s+|really\s+|still\s+|honestly\s+|actually\s+)*"
    r"(?:dont|don'?t|do not|doesnt|does not)\s+know\s+what\s+to\s+do" + _NOTHING_ELSE +
    r"|(?:(?:i|we)(?:'ve| have|'m| am)?\s+)?(?:got\s+|have\s+)?no\s+idea\s+what\s+to\s+do"
    + _NOTHING_ELSE +
    r"|(?:i|we)(?:'ve| have)?\s+(?:just\s+|really\s+|honestly\s+)*(?:dont|don'?t|do not)\s+"
    r"know\s+where\s+to\s+(?:start|begin|turn)" + _NOTHING_ELSE +
    r"|(?:i|we)(?:'ve| have)?\s+(?:no\s+idea|dont|don'?t|do not)\s+what\s+(?:comes\s+)?next\b"
    + _NOTHING_ELSE +
    r"|what\s+(?:do|should|shall|can|could)\s+(?:i|we)\s+do" + _NOTHING_ELSE +
    r"|what\s+(?:am|are)\s+(?:i|we)\s+supposed\s+to\s+do" + _NOTHING_ELSE +
    r"|(?:" + _STATE_SOURCE + r")"
    r")")

STUCK = re.compile(r"^\W*" + _LEADS + _ASK_BODY + r"\s*(?:\?|\.|!)*\s*$")

AN_ASK_AT_THE_END = re.compile(
    r"(?:^|[\s,;:.!?\u2014-]+)" + _LEADS + _ASK_BODY + r"\s*(?:\?|\.|!)*\s*$")
REACTION_FRAME = re.compile(
    r"^(?:(?:oh|well|god|wow|yeah|ok|okay|hmm|blimey|cor|ah|yes|no)\s+)*"
    r"(?:that sounds|this sounds|that looks|this looks|that seems|that feels|that must be"
    r"|that must have been|thats|that's|this is|that is|it is|its|it's|sounds|looks|seems|feels"
    r"|that|this|it)\s+"
    r"(?P<about>(?:[a-z']+\s*){1,3})$", re.I)
NAMES_A_THING = re.compile(
    r"\b(?:like|as|than|a|an|the|my|your|his|her|their|our|some|any|this|that|these|those"
    r"|one|two|three)\b", re.I)


def _a_reaction_to_what_was_said(lead):
    text = " ".join(str(lead or "").split()).strip(" ,;:.!?-\u2014")
    if not text:
        return False
    found = REACTION_FRAME.match(text)
    if not found:
        return False
    return not NAMES_A_THING.search(found.group("about"))


def the_ask_in(low):
    text = " ".join(str(low or "").split())
    if STUCK.match(text):
        return text
    found = AN_ASK_AT_THE_END.search(text)
    if not found:
        return ""
    lead = text[:found.start()].strip(" ,;:.!?-\u2014")
    if lead and not _a_reaction_to_what_was_said(lead):
        return ""
    return found.group(0).strip(" ,;:.!?-\u2014")


_DEATH = re.compile(
    r"\b(?:died|dying|passed (?:away|on)|funeral|buried|cremat\w*|death|widow\w*|"
    r"put (?:him|her|it|them)? ?down|euthanis\w*|we lost (?:her|him|them|mum|dad|my))\b")
_AN_OBJECT = (r"(?!\s+(?:a|an|the|my|your|his|her|their|our|some|this|that|these|those|no|one|"
              r"two|three|four|five|another|all|[a-z]+ing)\b)")
_ENDING = re.compile(
    r"\b(?:left me" + _AN_OBJECT + r"|walked out|threw me out|kicked me out|"
    r"(?:broke|split) up" + _AN_OBJECT + r"|separated|"
    r"divorc\w*|she'?s gone|he'?s gone|affair|cheated)\b")
_JOB = re.compile(
    r"\b(?:lost my (?:job|work|business|contract)|redundant|redundancy|laid off|sacked|"
    r"(?:got|been|were|was|im|i am|i'?m|getting|get|being)\s+fired\b(?!\s+up\b)|"
    r"let (?:me|him|her|us|them) go|resigned|walked out of (?:my|the) job|"
    r"contract not renewed|hours (?:were )?cut|"
    r"(?:my|our|the|a)\s+pay cut\b|"
    r"pay cut\b[^.!?]*\b(?:job|work|hours|salary|wage|boss|employer|shift|contract)\b|"
    r"\b(?:job|work|hours|salary|wage|boss|employer|shift|contract)\b[^.!?]*\bpay cut)\b")
_OWED = (r"(?:the |my |our )?(?:rent|bills?|payments?|mortgage|council tax|card|loan|gas|"
         r"electric(?:ity)?|water|dues|money|everything|childcare|nursery|school meals?)")
_MONEY = re.compile(
    r"\b(?:in debt|arrears|behind on " + _OWED + r"|behind with " + _OWED + r"|"
    r"can'?t afford|cannot afford|bailiffs|evicted|eviction|"
    r"repossession|bankrupt|overdraft|credit cards? maxed|money is tight|"
    r"low on (?:money|cash|funds|dosh)|short of money|skint|brokest|"
    r"(?:i|we)(?:'ve| have)?\s+no money|"
    r"down to my last (?:\d+|tenner|fiver|pound|quid|twenty|fifty))\b")
_SKINT = re.compile(
    r"\b(?:im|i am|i'?m|we are|we'?re|were)\s+(?:so\s+|totally\s+|completely\s+|proper\s+)?"
    r"broke\b")
_ILLNESS = re.compile(
    r"\b(?:diagnos\w*|cancer|tumour|tumor|chemo\w*|radiotherapy|biopsy|hospice|"
    r"terminally ill|(?:had|having|a|another|suspected)\s+stroke\b(?!\s+of\b)|"
    r"heart attack|dementia|alzheimers|parkinsons|multiple sclerosis|"
    r"(?:has|have|got|with)\s+ms\b(?!\s+(?:word|teams|office|excel|project|outlook|"
    r"access|paint|edge|windows))|"
    r"in (?:the )?hospital|intensive care)\b")
_FEELING = re.compile(
    r"\b(?:im|i am|i'?m|i feel|i'?ve been|ive been|feeling)\b(?:\s+\w+){0,4}\s+"
    r"(?:stressed|overwhelmed|exhausted|knackered|burnt out|burned out|anxious|panicking|"
    r"depressed|miserable|drowning|struggling|at the end of my tether|spiralling|"
    r"all over the place|low\b(?!\s+(?:on|in|down)\b)|down\b(?!\s+to\b)|"
    r"flat\b(?!\s+(?:tire|tyre|battery|mate|screen|white|bread|out|packed))|blue\b|rubbish|awful|"
    r"hopeless|empty)\b")
_FLAT = re.compile(
    r"\b(?:im|i am|i'?m|ive|i'?ve|i feel|i'?ve been|ive been|feeling)\b(?:\s+\w+){0,4}\s+"
    r"(?:tired of (?:it all|everything|this|all this|life)|fed up|had enough|sick of (?:it|"
    r"everything|all this)|worn out|worn down|running on empty|drained|no energy)\b")
_PLAN = re.compile(
    r"\b(?:i want to|i wanna|im thinking of|i'?m thinking of|im going to|i'?m going to|"
    r"i plan to|i'?d like to|i would like to|ive decided to|i'?ve decided to|"
    r"we want to|we'?re thinking of)\b")
_MAKING = re.compile(
    r"\b(?:cook|cooking|bake|baking|make|making|build|building|grow|growing|plant|planting|"
    r"sew|sewing|knit|knitting|paint|painting|brew|brewing|roast|roasting|grill|grilling|"
    r"barbecue|smoke|smoking|pickle|pickling|ferment|fermenting)\b")

_SELF = re.compile(
    r"\b(?:learn|learning|study|studying|studies|practi[cs]e|practi[cs]ing|take (?:it |that )?up|"
    r"get (?:fit|fitter|healthier|stronger|in shape)|lose (?:some )?weight|"
    r"start(?:ing)? (?:running|swimming|cycling|walking|yoga|pilates|climbing|the gym|"
    r"going to the gym|lessons?|classes?)|"
    r"guitar|piano|drums|violin|ukulele|singing|choir|"
    r"running|swimming|cycling|yoga|pilates|climbing|tennis|football|rugby|"
    r"drawing|sketching|painting|photography|pottery|"
    r"write|writing|a book|a novel|a blog|code|coding|programming|"
    r"a language|spanish|french|italian|german|welsh|"
    r"uni|university|college|a course|a degree|an evening class|open university)\b")

DEATH = (
    "Nothing has to be decided today. When something does, it is usually one dull thing - a "
    "phone call, a form - so take whichever is in front of you and let the rest wait.",
    "There's no right order for this, and no rush to find one. Pick the smallest thing that "
    "has to happen this week and leave the rest of it.",
    "The next step is usually paperwork, and it keeps. If it helps more, tell me about them "
    "instead.",
)
ENDING = (
    "Then start with tonight rather than the whole thing: somewhere to sleep, and what you say "
    "to the people who will ask.",
    "Nothing about the why has to be settled now. The next day or two is the only real "
    "question - where you stay, what you eat, who you ring.",
    "Take it in the order it hurts least: a roof and money first, the rest after. Is either of "
    "those already sorted?",
)
JOB = (
    "Money has dates, so start there: what the last pay and any notice money come to, and when "
    "they land.",
    "One small thing tomorrow, one the day after - a CV refreshed, a single application. "
    "Momentum does more than a plan here.",
    "First find out what you are owed and when: final pay, holiday, notice. Work out the next "
    "month before the next year.",
)
MONEY = (
    "Start with whatever has a deadline - the rent, or the bill that is actually overdue - then "
    "ring the people owed it. They are used to that call.",
    "Free advice beats guessing: StepChange or Citizens Advice will work it out with you for "
    "nothing. Ring one of them this week.",
    "Do the sums in one sitting - what comes in, what has to go out, what is left - and ring "
    "whoever you owe before they ring you.",
)
ILLNESS = (
    "The next thing is a question for the doctor rather than for you: what happens next, and "
    "what to do if. Write those two down before the appointment.",
    "Nothing has to be understood today. Take one practical thing - the appointment, the form, "
    "who drives you - and let the rest wait.",
    "Ask what the treatment is for and what it is meant to do, and take someone with you to "
    "write the answers down.",
)
FEELING = (
    "Then take the smallest thing that would ease it - one call made, one thing dropped, half "
    "an hour of nothing. Which is easiest?",
    "You don't have to sort the whole week. Pick the one thing that would make today lighter "
    "and do only that.",
    "Start with the basics - food, sleep, one thing off the list - and let the rest wait until "
    "tomorrow.",
)
PLAN = (
    "Then pick the smallest first move - one website, one phone call, one list - and do only "
    "that today.",
    "Start with the piece you can finish in an hour: a list of what it costs, or the one call "
    "you have been putting off.",
    "Do the boring first step, whatever it is - the form, the quote, the phone call. The rest "
    "gets clearer after it.",
    "Find one person who has done it and ask what their first week looked like. Then do the "
    "smallest thing off that list today.",
)
SELF = (
    "Then make the first go small enough to be easy: twenty minutes of it today, and nothing "
    "promised beyond that.",
    "Pick the beginner's version and do it once this week, badly. It gets clearer once there is "
    "something to improve.",
    "Start with the hour you would actually do it in, not the plan for it. What would that hour "
    "look like?",
)
HARD = (
    "One thing at a time, then. What is the smallest thing that would make today easier?",
    "You don't have to have a plan. Pick the single next step and ignore the rest of it for now.",
    "Start with whatever has a deadline, if anything does; if nothing does, start with eating "
    "something.",
)
_ANIMAL = re.compile(
    r"\b(?:dog|dogs|puppy|pup|cat|cats|kitten|pet|rabbit|bunny|hamster|guinea pig|horse|pony|"
    r"budgie|parrot|ferret|tortoise|goldfish|fish)\b")
PET_LOSS = (
    "Nothing has to be decided today, and nothing has to be tidied away either. What is the "
    "house like without them?",
    "There is no step to take today. If it helps, tell me about them - what they were like.",
    "The quiet is the hard part, and it takes the time it takes. Take today as slowly as it "
    "comes.",
)

EMERGENCY = re.compile(
    r"\b(?:999|911|112|111|a&e|a and e|casualty|ambulance|emergency department|out of hours|"
    r"urgent care|walk-in cent(?:re|er))\b", re.I)

URGENT_ALREADY_GIVEN = (
    "The advice you just had is the first thing to do. Nothing else needs a plan until someone "
    "has seen you.",
    "What you were just told to do is the whole of the list today - the rest keeps until "
    "someone has seen you.",
    "Get seen first. Nothing on the list is worth doing before that, and it will all still be "
    "there afterwards.",
)


FIRST_SENTENCE = re.compile(r"[.!?](?:\s|$)")
A_CONDITION_IN_FRONT = re.compile(r"\b(?:if|unless|when|whether|in case)\b", re.I)


FIRST_LINE = (
    "Nothing looks like a first step when it is all in one heap. Say the situation in a line and "
    "we'll find the smallest piece of it.",
    "It is usually one thing pretending to be ten. What is the part that keeps coming back?",
    "The fog is normal with this much on. Name one thing that happened today and we will start "
    "there.",
)


def _opens_with_an_emergency(reply):
    said = " ".join(str(reply or "").split())
    found = EMERGENCY.search(said)
    if not found:
        return False
    end = FIRST_SENTENCE.search(said)
    if end and found.start() >= end.end():
        return False
    return not A_CONDITION_IN_FRONT.search(said[:found.start()])


def the_advice_was_to_get_seen(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    for turn in reversed(turns or []):
        if isinstance(turn, dict) and str(turn.get("bot") or "").strip():
            return _opens_with_an_emergency(str(turn["bot"]))
    return False


POOLS = ((_DEATH, DEATH), (_ENDING, ENDING), (_JOB, JOB), (_MONEY, MONEY), (_SKINT, MONEY),
         (_ILLNESS, ILLNESS),
         (_FEELING, FEELING), (_FLAT, FEELING), (_PLAN, PLAN))


def pool(text, memory):
    low = " ".join(str(text or "").lower().replace("\u2019", "'").split())
    ask = the_ask_in(low)
    if not ask:
        return None
    before = _before(memory)
    if not before:
        if _START_ASK.match(ask):
            return _not_said_again(HARD, memory)
        if _STATE.match(low):
            return None
        return _not_said_again(FIRST_LINE, memory)
    if the_advice_was_to_get_seen(memory):
        return _not_said_again(URGENT_ALREADY_GIVEN, memory)
    for pattern, replies in POOLS:
        if pattern is _PLAN and _MAKING.search(before):
            continue
        if pattern is _PLAN and _SELF.search(before):
            if _the_answer_gave_a_step(memory):
                continue
            return _not_said_again(SELF, memory)
        if pattern.search(before):
            if pattern is _DEATH and _ANIMAL.search(before):
                continue
            return _not_said_again(replies, memory)
    if reads_as_bad_news(before):
        return _not_said_again(HARD, memory)
    return None


DOING = frozenset("""start starts begin pick do try ask ring call phone write book get go take read
watch cook bake keep put set use buy check plan split choose make find look learn practice practise
send fill sign download join tell speak say warm rinse boil cut add mix stop ease slow wear walk run
""".split())


def _the_answer_gave_a_step(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    said = ""
    for turn in reversed(turns or []):
        if isinstance(turn, dict) and str(turn.get("bot") or "").strip():
            said = " ".join(str(turn["bot"]).lower().split())
            break
    if not said:
        return False
    if re.search(r"\d", said) or ":" in said:
        return True
    return any(w in DOING for w in re.findall(r"[a-z']+", said)[:6])


def _not_said_again(replies, memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    said = " ".join(str(turn.get("bot") or "").lower() for turn in (turns or [])[-4:]
                    if isinstance(turn, dict))
    if not said:
        return replies
    def written(reply):
        words = [w for w in re.findall(r"[a-z']+", reply.lower())
                 if len(w) > 3 and w not in topics.STOPWORDS]
        shared = sum(1 for w in words if w.rstrip("s") in said)
        if not words:
            return False
        return shared >= 3 and shared / len(words) >= 0.35
    return tuple(sorted(replies, key=written))


_START_ASK = re.compile(
    r"^\W*(?:(?:so|and|but|well|oh|honestly|then|i mean|like|just|seriously|really|the thing is|"
    r"see|look)\s+)*"
    r"(?:"
    r"(?:(?:i|we)\s+)?(?:(?:really|honestly|just|even|still)\s+)*"
    r"(?:(?:dont|don'?t|do not)\s+(?:even\s+)?know|dunno|(?:have\s+)?no\s+(?:idea|clue))\s+"
    r"where\s+to\s+(?:start|begin)"
    r"|(?:where|how)\s+(?:do|should|shall|can|could)\s+(?:i|we)\s+(?:even\s+)?"
    r"(?:start|begin)"
    r"|where\s+to\s+(?:start|begin)"
    r")(?:\s+(?:now|first|today|at\s+all))?\s*(?:\?|\.|!)*$", re.I)


def _before(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns:
        return ""
    last = turns[-1]
    if not isinstance(last, dict):
        return ""
    return " ".join(str(last.get("user") or "").lower().replace("\u2019", "'").split())
