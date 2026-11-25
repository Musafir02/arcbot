import re

from . import pick

OWN_SERIOUS_CONDITION = re.compile(
    r"\b(?:cancers?|tumou?rs?|leuka?emia|lymphoma|myeloma|melanoma|mesothelioma|"
    r"motor neurone|multiple sclerosis|huntington\w*|parkinson\w*|alzheim\w*|dementia|"
    r"cerebral palsy|muscular dystrophy|cirrhosis|copd|emphysema|motor\w* disease|"
    r"heart failure|kidney failure|terminal|palliative|metasta\w+|malignant|carcinoma|"
    r"\bm\.?s\.?)\b", re.I)
A_FINDING = re.compile(
    r"\b(?:a\s+)?(?:shadow|mass|growth|nodule|spot|something)\s+(?:on|in)\s+(?:my|the|his|her)\s+"
    r"(?:lung|lungs|breast|kidney|kidneys|liver|bowel|brain|prostate|womb|uterus|cervix|ovary|"
    r"ovaries|thyroid|skin|colon|pancreas|bladder|spine|bone|bones|chest|lymph)\b|"
    r"\b(?:they|the\s+doctor|the\s+doctors|the\s+consultant|the\s+radiologist|the\s+scan|"
    r"the\s+mammogram|the\s+x-?ray|the\s+results?)\s+(?:found|saw|spotted|noticed|picked\s+up|"
    r"showed)\s+(?:something|a\s+(?:shadow|mass|growth|nodule|spot|lump))\b", re.I)
A_BENIGN_FINDING = re.compile(
    r"(?<!not\s)\b(?:benign|harmless|was\s+nothing|nothing\s+(?:to\s+worry|serious|bad|sinister)|"
    r"all\s+(?:fine|clear)|turned\s+out\s+(?:fine|nothing))\b", re.I)
ITS_THE_SPEAKERS = re.compile(
    r"(?:\bit'?s\b|\bit is\b|\bive\b|\bi've\b|\bi have\b|\bi had\b|\bi got\b|\bim\b|\bi'm\b|"
    r"\bi was\b|\bi am\b|\bthey found\b|\btheyve found\b|\bthey've found\b|\bfound out\b|"
    r"\b(?:my|the|their)\s+(?:cancer|tumou?rs?|leuka?emia|lymphoma|melanoma)\b|"
    r"\bthe (?:biopsy|scan|results?|tests?|lump|mri|x-?ray)\b|\bmy (?:biopsy|scan|results?|"
    r"tests?|lump|mri|x-?ray)\b|\bgot the results\b|\bdiagnosed\b|\bdiagnosis\b)", re.I)
NOT_ABOUT_THEIR_BODY = re.compile(
    r"\b(?:sponsor\w*|fundrais\w*|raising|raise money|awareness|charity|marathon|"
    r"race for life|donat\w*|nurses?|nursing|(?:works?|working) (?:at|in|for)|shift|"
    r"documentar\w*|film|episode|podcast|research(?:ing)?|study|statistics?)\b", re.I)
A_SCARE = re.compile(
    r"\b(?:scare|false alarm|all clear|came back clear|turned out (?:fine|nothing|benign)|"
    r"it was (?:benign|nothing)|they said it was nothing)\b", re.I)
A_GOOD_TURN = re.compile(
    r"\b(?:gone|all gone|shrank|shrunk|shrink\w*|in remission|remission|no sign of|cured|"
    r"all clear|clear scan|finished (?:the )?(?:chemo|treatment|radiotherapy))\b", re.I)
NOT_LANDED = re.compile(
    r"\b(?:not|isnt|isn't|no longer|never|clear of|free of|benign|ruled out|test\w* for|"
    r"check\w* for|screen\w* for|scared|worried|afraid|terrified|think|thought|might|maybe|"
    r"may have|probably|hopefully|pray|praying|what if|is it|is that|or is it|could it)\b", re.I)

A_WORRY = re.compile(
    r"\b(?:think|thinks|thought|might|maybe|could|may\s+have|possibly|probably|suspect\w*|scared|"
    r"afraid|terrified|worried|worry|fear|fears|hoping|praying|waiting|wait|"
    r"test\w*(?:\s+(?:me|him|her))?\s+for|check\w*(?:\s+(?:me|him|her))?\s+for|"
    r"screen\w*\s+for|being\s+tested|results\s+(?:are|is)\s+(?:due|back)|"
    r"\b(?:is|are|was|were)\s+(?:having|going\s+in|in)\s+(?:a\s+|an\s+|the\s+)?"
    r"(?:scan|test|biopsy|procedure|op|operation)|"
    r"\b(?:scan|scans|test|tests|biopsy|biopsies|mammogram|smear|op|operation|procedure|"
    r"appointment)\s+(?:is|are|was|were)\s+(?:on|at|next|this|tomorrow|in)\b|"
    r"\b(?:have|has|having|got)\s+(?:a\s+|an\s+|the\s+|my\s+)?(?:blood\s+|ct\s+|mri\s+|"
    r"x[ -]?ray\s+|smear\s+|pregnancy\s+)?(?:scan|test|biopsy|mammogram|smear|op|operation|"
    r"procedure|surgery)\s+(?:on|next|this|tomorrow|in|at)\b)"
    ,re.I)
A_MEDICAL_TEST = re.compile(
    r"\b(?:scan|scans|biopsy|biopsies|mammogram|smear|smear test|blood test|bloods|mri|ct scan|"
    r"ultrasound|x[ -]?ray|xray|ecg|swab|test results|results of (?:my|the)|my results|"
    r"the results|results?|op|ops|operation|operations|procedure|procedures|surgery)\b", re.I)
NOT_A_MEDICAL_TEST = re.compile(
    r"\b(?:exam|exams|gcse|gcses|a level|a levels|alevel|school|uni|university|course|driving|"
    r"lottery|election|football|match)\b", re.I)

AN_ANIMAL = re.compile(
    r"\b(?:dog|dogs|cat|cats|puppy|kitten|pet|pets|rabbit|hamster|guinea pig|horse|pony|"
    r"parrot|ferret|tortoise|lizard|snake|fish)\b", re.I)
A_QUESTION_ABOUT_IT = re.compile(
    r"\b(?:could|might|can|is|are|was|would|will|does|do)\s+(?:it|this|that)\s+(?:be|mean)\b|"
    r"\bwhat\s+if\s+(?:it|this)\b|\bdo\s+you\s+think\b|\bany\s+chance\b|"
    r"\bwhat\s+are\s+the\s+chances\b", re.I)
KIN = (r"mum|mummy|mom|mommy|mother|dad|daddy|father|son|daughter|child|children|kid|kids|"
       r"wife|husband|partner|boyfriend|girlfriend|brother|sister|gran|granny|grandma|grandad|"
       r"grandpa|nana|nan|aunt|auntie|uncle|cousin|friend|mate|neighbour|neighbor|baby|sister|"
       r"in[- ]law|niece|nephew|stepson|stepdaughter|stepdad|stepmum|fiance|fiancee")
_A_RELATIVE = re.compile(r"\b(?:my|our)\s+(?:" + KIN + r")(?:'?s)?\b", re.I)

RULED_OUT = re.compile(
    r"\b(?:they|he|she|we|the\s+(?:doctor|doctors|consultant|gp|specialist|hospital|scan|"
    r"tests?|results?|biopsy)|doc(?:tor)?)\b[^.!?]{0,16}?\bruled\s+out\b[^.!?]{0,20}?"
    r"\b(?:cancer|tumou?rs?|malignant|carcinoma|lymphoma|leuka?emia|melanoma)\b", re.I)
NEGATED_CONDITION = re.compile(
    r"\b(?:(?:it'?s|it is|its|that'?s|that is|it|that)\s+(?:not|isnt|isn'?t|wasnt|wasn'?t|"
    r"wasn'?t\s+not)|(?:they|the doctor|the consultant|the gp|the results?|the tests?)\s+"
    r"(?:said|say|told me|came back|were|was)?\s*(?:it\s+)?(?:not|isnt|isn'?t|wasnt|wasn'?t))"
    r"\s+(?:a\s+|the\s+|any\s+)?(?:cancer|tumou?r|malignant|carcinoma|lymphoma|leuka?emia|"
    r"melanoma)\b", re.I)
RULED_OUT_TAIL = re.compile(
    r"\s*(?:(?:now|today|though\s+thankfully|thankfully|thank\s+god|at\s+last|finally|so\s+far|"
    r"great|brilliant|and\s+i\s+(?:am|feel)\s+(?:so\s+)?(?:relieved|glad|happy)|"
    r"im\s+(?:so\s+)?(?:relieved|glad|happy)|which\s+is\s+(?:great|a\s+relief)|"
    r"what\s+a\s+relief|thanks|cheers|anyway)\s*)*[.!]*$", re.I)

THE_WAIT = (
    "That wait between a test and an answer is the worst part of it, and nothing is known until "
    "somebody tells you. What have they actually said so far?",
    "Sitting with a maybe is harder than sitting with an answer, even a bad one. Try not to spend "
    "the wait on the worst version of it. When do you hear?",
    "That is a frightening thing to be carrying around. Write your questions down before the "
    "appointment - they go out of your head in the room. Who is going with you?",
)
THE_WAIT_AFTER_A_TEST = THE_WAIT[:2]
THEIR_WAIT = (
    "Waiting on somebody else's results is a helpless feeling, and nothing is known until they are "
    "back. What have they been told about when they will know?",
    "Sitting with a maybe about someone you love is harder than sitting with an answer. Try not to "
    "plan around the worst version of it. Who is with them?",
    "That is frightening, and it is a lot to carry around. What has actually been said so far - and "
    "who is looking after you in it?",
)
THE_NEWS = (
    "I'm sorry. That is a hell of a thing to be told, and there is no right way to take it. "
    "Who is with you today?",
    "That is the kind of news that stops the week. How are you doing with it so far?",
    "You don't have to make sense of it today. Do you want to talk about it, or shall I ask about "
    "something else for a while?",
    "That's a heavy word to hear about yourself. Who is looking after you in it?",
    "I'm sorry. Do you want to tell me what they said?",
)
THE_ILLNESS_GOING = (
    "That is the best kind of news to hear, and it is worth saying out loud today. How did they tell "
    "you?",
    "Gone is a good word to hear about it. What does that leave for you - a check in a few months, "
    "or the whole thing behind you?",
    "That is a weight off. Do the people who were worried with you know yet?",
)
THE_THING_RULED_OUT = (
    "Then it is not that, and that is the news you were after. What did they say it is instead?",
    "Ruled out. That is a weight off, whatever else came with it. How are you doing?",
    "Good. Not that, then. Did they say what it is?",
)


def _the_relative(text):
    return _A_RELATIVE.search(text)


def _the_wait(text):
    found = OWN_SERIOUS_CONDITION.search(text) or A_FINDING.search(text)
    if found:
        return found
    if NOT_A_MEDICAL_TEST.search(text):
        return None
    return A_MEDICAL_TEST.search(text)


def tells_of_a_condition_of_their_own(text):
    if not text or NOT_ABOUT_THEIR_BODY.search(text):
        return False
    if AN_ANIMAL.search(text) or A_QUESTION_ABOUT_IT.search(text):
        return False
    condition = OWN_SERIOUS_CONDITION.search(text)
    if not condition:
        condition = A_FINDING.search(text)
        if not condition or A_BENIGN_FINDING.search(text):
            return False
    owner = ITS_THE_SPEAKERS.search(text)
    if not owner:
        return False
    if A_SCARE.search(text) or A_GOOD_TURN.search(text):
        return False
    landed = NOT_LANDED.search(text)
    if landed and landed.start() < condition.start():
        return False
    mine = _the_relative(text)
    if mine and mine.start() < owner.start():
        return False
    return True


def reads_as_the_wait_of_their_own(text):
    if not text or NOT_ABOUT_THEIR_BODY.search(text):
        return False
    if AN_ANIMAL.search(text) or A_QUESTION_ABOUT_IT.search(text):
        return False
    if A_SCARE.search(text) or A_GOOD_TURN.search(text):
        return False
    if not A_WORRY.search(text) or not _the_wait(text):
        return False
    if _the_relative(text):
        return tells_of_a_condition_of_their_own(text)
    return not tells_of_a_condition_of_their_own(text)


def reads_as_the_wait_of_somebody_elses(text):
    if not text or NOT_ABOUT_THEIR_BODY.search(text):
        return False
    if AN_ANIMAL.search(text) or A_QUESTION_ABOUT_IT.search(text):
        return False
    if A_SCARE.search(text) or A_GOOD_TURN.search(text):
        return False
    if not A_WORRY.search(text) or not _the_wait(text):
        return False
    return bool(_the_relative(text))


def reads_as_a_thing_ruled_out(text):
    said = " ".join(str(text or "").lower().split())
    if not said or "?" in said:
        return False
    if A_QUESTION_ABOUT_IT.search(said) or re.match(
            r"\s*(?:is|are|was|were|did|does|do|has|have|had|can|could|would|will|should|any)\b",
            said):
        return False
    for match in RULED_OUT.finditer(said):
        if RULED_OUT_TAIL.match(said[match.end():]):
            return True
    for match in NEGATED_CONDITION.finditer(said):
        if RULED_OUT_TAIL.match(said[match.end():]):
            return True
    return False


def reads_as_the_news_of_their_own(text):
    if not tells_of_a_condition_of_their_own(text):
        return False
    return not A_WORRY.search(text)


def reads_as_the_illness_going(text):
    if not text or NOT_ABOUT_THEIR_BODY.search(text):
        return False
    if not OWN_SERIOUS_CONDITION.search(text):
        return False
    turn = A_GOOD_TURN.search(text)
    if not turn:
        return False
    if "?" in text or NOT_LANDED.search(text[:max(0, turn.start())] or " "):
        return False
    if re.match(r"\s*(?:is|are|was|were|will|would|could|can|has|had|have|did|does|do|"
                r"any\s+chance|do\s+you\s+think)\b", text):
        return False
    return bool(RULED_OUT_TAIL.match(text[turn.end():]))


def pool_for(text):
    if reads_as_a_thing_ruled_out(text):
        return THE_THING_RULED_OUT
    if reads_as_the_illness_going(text):
        return THE_ILLNESS_GOING
    if reads_as_the_news_of_their_own(text):
        return THE_NEWS
    if reads_as_the_wait_of_somebody_elses(text):
        return THEIR_WAIT
    if reads_as_the_wait_of_their_own(text):
        return THE_WAIT
    return None


def names_a_condition(text):
    said = " ".join(str(text or "").lower().split())
    return bool(OWN_SERIOUS_CONDITION.search(said) or A_FINDING.search(said))


def reply_for(text, memory=None):
    pool = pool_for(text)
    if not pool:
        return None
    if pool is THE_WAIT and not names_a_condition(text):
        pool = THE_WAIT_AFTER_A_TEST
    return pick(pool, memory if isinstance(memory, dict) else {}, text)
