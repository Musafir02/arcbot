import random
import re
try:
    from ..memory import dream as _dream
except Exception:
    _dream = None

WORD = re.compile(r"[a-z0-9]+(?:'[a-z]+)?")

FAMILY = frozenset({
    "mum", "mam", "mom", "mother", "mummy", "mommy", "dad", "father", "daddy", "son",
    "daughter", "baby", "toddler", "child", "kid", "boy", "girl", "nan", "nana", "granny",
    "gran", "grandma", "grandad", "grandpa", "grandmother", "grandfather", "husband", "wife",
    "partner", "boyfriend", "girlfriend", "brother", "sister", "friend", "neighbour",
    "neighbor", "uncle", "aunt", "auntie", "cousin", "stepson", "stepdaughter", "stepdad",
    "stepmum", "fiance", "fiancee", "flatmate", "housemate", "carer", "patient",
    "niece", "nephew", "grandson", "granddaughter", "stepson", "stepdaughter", "godson",
    "goddaughter", "toddler", "newborn", "childminder", "flatmate", "teenager", "teen",
    "adolescent",
})

PRO_ANSWERING = re.compile(
    r"\b(?:my|his|her|their|our|the)\s+(?:carers?|care\s+workers?|support\s+workers?|"
    r"social\s+workers?|personal\s+assistants?|nurses?|midwives?|midwife|doctors?|gps?|"
    r"physios?|therapists?)\b[^.?!]{0,30}\b(?:isn'?t|is\s+not|not|hasn'?t|has\s+not|never|"
    r"no)\s+respond(?:ing|ed|e)?\b"
    r"|\bno\s+response\s+from\s+(?:my|the|our)\s+(?:carer|care\s+worker|support\s+worker|"
    r"social\s+worker|personal\s+assistant|nurse|doctor|gp|physio|therapist)s?\b")
BODY_IN_THE_ROOM = re.compile(
    r"\b(?:floor|ground|bed|sofa|settee|couch|bath|pavement|street|doorstep)\b"
    r"|\b(?:collapsed|collapsing|fell|fallen|fainted|pass(?:ed)?\s+out|seizure|fitting)\b"
    r"|\b(?:breathing|breath|breathe|pulse|blue|lips|cold|clammy|sweating|eyes|pale|grey|gray)\b"
    r"|\b(?:unconscious|out\s+cold|unresponsive|in\s+front\s+of\s+me|with\s+me|next\s+to\s+me)\b"
    r"|\b(?:to\s+(?:pain|touch|voices?|noise|light|stimulus)|(?:his|her|their)\s+name)\b")

NOW = (
    "unresponsive", "not responding", "no response", "wont wake", "won't wake", "cant wake",
    "can't wake", "not waking", "not breathing", "stopped breathing", "isnt breathing",
    "isn't breathing", "struggling to breathe", "cant breathe", "can't breathe", "gasping",
    "struggling for breath", "fighting for breath", "gasping for breath", "struggling for air",
    "unconscious", "unconcious", "collapsed", "limp", "floppy", "fitting", "seizure",
    "convulsing", "choking", "turning blue", "gone blue", "blue lips", "no pulse",
    "cardiac", "overdose", "took too many", "swallowed his tongue",
    "had a fit", "has a fit", "having a fit", "having fits", "keeps fitting", "kept fitting",
    "keeps having fits", "kept having fits",
    "isnt responding", "isn't responding", "isnt responsive", "isn't responsive", "not responsive",
)

BLUE_LOOSE = re.compile(
    r"\b(?:is|are|was|were|looks?|looking|went|goes|getting|turned|turning|has gone|have gone)"
    r"\b[^.?!;]{0,14}\bblue\b")
BLUE_BETWEEN = (
    r"(?:\s+(?:a\s+bit|a\s+little|very|really|quite|all|pale|grey|gray|and|has\s+gone|"
    r"have\s+gone|had\s+gone|gone|getting|looking|turning|turned|is|are|was|were|looks?|"
    r"looked|went|goes))*")
BLUE_BODY = re.compile(
    r"\b(?:lips?|mouth|tongue|face|cheeks?|skin|fingers?|fingertips?|hands?|nails?|feet|foot|"
    r"toes?|arms?|legs?|body)\b" + BLUE_BETWEEN + r"\s+blue\b"
    r"|\b(?:he|she|they|baby|boy|girl|kid|child|son|daughter|mum|mam|mom|dad|father|mother|"
    r"wife|husband|partner|brother|sister|nan|granny|gran|grandad|grandma|grandpa|stepson|"
    r"stepdaughter|nephew|niece|friend|neighbour)\b" + BLUE_BETWEEN + r"\s+blue\b")

GREY_LOOSE = re.compile(
    r"\b(?:is|are|was|were|looks?|looking|went|goes|getting|turned|turning|has gone|have gone|"
    r"had gone|going|gone)\b[^.?!;]{0,14}\b(?:grey|gray)\b")
GREY_BETWEEN = (
    r"(?:\s+(?:a\s+bit|a\s+little|very|really|quite|all|pale|and|"
    r"has\s+gone|have\s+gone|had\s+gone|has\s+turned|have\s+turned|had\s+turned|"
    r"is\s+going|are\s+going|was\s+going|were\s+going|gone|going|goes|getting|looking|"
    r"turning|turned|is|are|was|were|looks?|looked|went))*")
GREY_PEOPLE = "|".join(sorted(FAMILY | {"he", "she", "they", "hes", "shes", "everyone"},
                              key=len, reverse=True))
GREY_PERSON_STATE = (
    r"(?:\s+(?:a\s+bit|a\s+little|very|really|quite|all|pale|and|"
    r"has\s+gone|have\s+gone|had\s+gone|has\s+turned|have\s+turned|had\s+turned|"
    r"gone|goes|went|is|are|was|were|looks?|looked|turned))*")
GREY_BODY = re.compile(
    r"\b(?:lips?|mouth|tongue|face|cheeks?|skin|fingers?|fingertips?|hands?|nails?|feet|foot|"
    r"toes?|arms?|legs?|body)\b" + GREY_BETWEEN + r"\s+(?:grey|gray)\b"
    r"|\b(?:" + GREY_PEOPLE + r")\b" + GREY_PERSON_STATE + r"\s+(?:grey|gray)\b")

TODAY = (
    "confused", "drowsy", "very sleepy", "sleepy and", "temperature of 40", "40 degrees",
    "39 degrees", "39.5 degrees", "temperature of 39", "temperature of 39.5",
    "very hot to touch", "burning up", "hit his head", "hit her head",
    "hit their head", "banged his head", "banged her head", "fell and hit",
    "fell down the stairs", "wont stop bleeding", "wont stop vomit", "dehydrated",
    "not had a wee", "hasnt had a wee", "hasnt done a wee", "hasnt been for a wee",
    "no wet nappy", "dry nappy", "not passing urine",
)

STUCK = re.compile(
    r"\bstuck\b[^.?!]{0,30}\bthroat\b|\bthroat\b[^.?!]{0,30}\bstuck\b"
    r"|\b(?:cant|can't|unable to|couldn't|couldnt) (?:talk|speak|breathe)\b[^.?!]{0,25}\bthroat\b"
    r"|\bthroat\b[^.?!]{0,25}\b(?:cant|can't|couldn't|couldnt) (?:talk|speak|breathe)\b"
    r"|\bcant get it out\b|\bcan't get it out\b"
    r"|\bturning purple\b|\bgoing purple\b|\bgone purple\b")

INGEST = frozenset("""
    swallowed swallow swallowing ate eaten eating drank drunk drinking chewed chewing
    licked sucking sucked gulped gulping sipped downed
""".split())
CHEMICAL = ("washing tablet", "washing pod", "laundry tablet", "laundry pod", "dishwasher tablet",
            "detergent", "bleach", "antifreeze", "drain cleaner", "oven cleaner", "disinfectant",
            "weedkiller", "weed killer", "screenwash", "screen wash", "paint thinner", "methanol",
            "hand sanitiser", "hand sanitizer", "white spirit", "caustic",
            "paint", "air freshener", "perfume", "aftershave", "mouthwash", "nail polish",
            "nail varnish", "polish remover", "vape", "e-liquid", "eliquid", "e-cigarette",
            "lighter fluid", "petrol", "paraffin", "turps", "turpentine", "caustic soda")
MEDICINE = frozenset("""
    tablet tablets pill pills capsule capsules paracetamol ibuprofen aspirin medicine medicines
    painkiller painkillers supplement supplements vitamins antidepressant antidepressants
    methadone insulin codeine morphine steroids
""".split())
SMALL_OBJECT = ("battery", "batteries", "magnet", "magnets", "coin", "marble", "bead", "button",
                "sim card", "screw", "drawing pin", "earring", "lego")

AMBIGUOUS = ("unresponsive", "not responding", "no response", "limp", "floppy", "fitting",
             "confused", "drowsy", "burning up", "very hot to touch")
AMBIGUOUS_CUES = AMBIGUOUS + ("wont wake", "won't wake", "cant wake", "can't wake", "not waking",
                              "isnt responding", "isn't responding", "isnt responsive",
                              "isn't responsive", "not responsive")
NOT_A_BODY = frozenset("to by about from into of".split())
MANNER = frozenset("well nicely easily fine ok okay perfectly together up out round around".split())
SETTLING = frozenset("well nicely easily fine perfectly beautifully smoothly brilliantly".split())
CALENDAR = frozenset("today yesterday lately recently nowadays".split())
SECOND_CLAUSE = re.compile(r"(?:but|and|then|so|because|yet|though|when)\b")
SETTLING_PHRASES = re.compile(
    r"(?:at|in|into|with)\s+(?:the\s+|his\s+|her\s+|their\s+|our\s+|a\s+)?(?:new\s+)?"
    r"(?:nursery|preschool|playgroup|school|class|clubs?|teams?|groups?|other\s+kids|the\s+others)\b")

PLACE = frozenset("""
    floor ground bed bath sofa settee stairs street garden ward car cot pram pushchair chair
    table hospital home room arms lap arms shoulders knees chest hands
""".split())
OBJECT_WORD = frozenset("""
    it them the a an my our his her their its this that these those new some carpet door floor
    tiles kitchen bathroom wardrobe blind window shelves shelf units sink sofa curtains decor
""".split())
SYMPTOM = frozenset("""
    fever temperature temp cold flu cough rash pain headache seizure shivers sweat sweats
""".split())
ORDINARY_STATE = frozenset("""
    tired sleepy asleep hungry teething crying cross grumpy upset angry excited playing bored
    told naughty tantrum tantrums whingey whinging
""".split())
DURATION = frozenset("minute minutes min hour hours day days week weeks month months year years".split())
ONLINE = frozenset("""
    chat whatsapp messenger facebook instagram twitter tiktok app forum thread threads messages
    texts email emails phone phonecalls slack discord reddit linkedin zoom teams skype group
    groups feed forum list mailing
""".split())


def _not_a_body(rest, before=""):
    words = rest.split()
    if not words:
        return False
    first = words[0]
    second = words[1] if len(words) > 1 else ""
    third = words[2] if len(words) > 2 else ""
    if first in NOT_A_BODY:
        if first == "to" and (second in TO_PAIN or (second in ("the", "any", "some", "his", "her")
                                                    and third in TO_PAIN)):
            return False
        if first == "to" and _fed_and_unresponsive(before, rest):
            return False
        return True
    if first.strip(".,!?;:") in SETTLING:
        tail = " ".join(words[1:]).strip(" .,!?;:")
        if not tail or tail in CALENDAR:
            return True
        if SECOND_CLAUSE.match(tail):
            return True
        return bool(SETTLING_PHRASES.match(tail))
    if first == "together" and second in ("a", "an", "the", "my", "our", "his", "her", "their",
                                          "some", "these", "those", "this"):
        return True
    if first in ("when", "whenever"):
        return bool(set(words[:6]) & ORDINARY_STATE)
    if first == "in":
        if second in ("with", "at"):
            return True
        if second in MANNER and second not in PLACE:
            return True
        if second in ("the", "a", "an", "his", "her", "their", "my", "our"):
            return third not in PLACE
        return False
    if first == "with":
        if second in ("a", "an", "the"):
            return third not in SYMPTOM
        return second in OBJECT_WORD
    if first == "on":
        if second in ("the", "a", "an", "my", "his", "her", "their", "our", "this", "that"):
            return third in ONLINE
        return second in ONLINE
    if first == "for":
        return second in DURATION or (second in ("a", "an", "one", "two", "half") and third in DURATION)
    return False
WAKE_CUES = ("wont wake", "won't wake", "cant wake", "can't wake", "not waking")
WAKE_OBJECT = frozenset({
    "him", "her", "them", "it", "my", "your", "his", "our", "their", "the", "this", "that",
}) | {
    "mum", "mam", "mom", "mother", "dad", "father", "son", "daughter", "baby", "toddler",
    "child", "kid", "boy", "girl", "nan", "nana", "gran", "granny", "grandma", "grandad",
    "grandpa", "husband", "wife", "partner", "brother", "sister", "friend", "uncle", "aunt",
    "niece", "nephew", "newborn", "patient",
}
DEATH = ("died", "dies", "dying", "passed away", "passed on", "funeral", "buried", "cremation",
         "bereave", "widow", "death", "killed")

VERBY = ("fitting", "burning up")
OBJECTISH = re.compile(
    r"^\s+(the|a|an|my|your|his|her|their|our|its|it|me|him|them|us|you|new|some|these|those|"
    r"this|that|another|two|three|four|five|one|carpet|door|floor|tiles|kitchen|bathroom|"
    r"wardrobe|blind|window|shelves|shelf|units|sink|sofa)\b")

CONFUSED_SIGN = re.compile(r"\b(suddenly|very|extremely|really|getting more|more)\b")
CONFUSED_AFTER = re.compile(r"^\s*(?:and|,|or)\b")

TO_PAIN = ("pain", "the pain", "any pain", "stimulus", "stimuli", "voice", "voices", "sound",
           "noise", "loud", "touch", "light", "nothing", "anything")

SMALL_PERSON = frozenset("""
    baby babies newborn infant toddler child kid son daughter boy girl little
""".split())
A_FEED = frozenset("""
    milk formula feed feeds feeding bottle breast solids weaning
""".split())


NOSE_BREATH = re.compile(
    r"\b(?:can'?t|cannot|couldn'?t|could\s+not|struggling|hard|unable|not|trouble)"
    r"\s+(?:to\s+)?breath\w*[^.?!]{0,18}?\bthrough\b[^.?!]{0,12}?\bnose\b")

NOSE_RED = (
    r"\b(?:going|turning|gone|looks?)\s+blue\b",
    r"\bblue\s+(?:lips|round\s+the\s+lips|in\s+the\s+face)\b",
    r"\bgrey\b", r"\bgray\b", r"\bgrunt\w*\b",
    r"\bribs?\b[^.?!]{0,25}\b(?:suck\w*|pulling|pulling\s+in|drawing|recession)\b",
    r"\b(?:pulling|sucking|drawing)\s+(?:in|at)\b[^.?!]{0,25}\b(?:ribs?|chest)\b",
    r"\bchest\b[^.?!]{0,25}\b(?:pulling|sucking|drawing)\s+in\b",
    r"\blimp\b", r"\bfloppy\b", r"\bunresponsive\b", r"\bnot\s+responding\b",
    r"\bunconscious\b",
    r"\bhard\s+to\s+(?:wake|rouse|arouse|waken)\b",
    r"\bwont\s+wake\b", r"\bwon'?t\s+wake\b", r"\bnot\s+waking\b",
    r"\b(?:wouldnt|wouldn'?t|didnt|didn'?t|never)\s+(?:wake|woke)\b",
    r"\b(?:couldnt|couldn'?t)\s+be\s+woken\b", r"\bisnt\s+waking\b", r"\bisn'?t\s+waking\b",
    r"\bout\s+cold\b",
    r"\bseizure\b", r"\bfitting\b", r"\bconvuls\w*\b",
    r"\b(?:had|has|having|with)\s+(?:a|another)\s+fit\b",
    r"\bsnoring\b", r"\bapnoea\b", r"\bapnea\b",
    r"\bnot\s+breathing\b", r"\bstops?\s+breathing\b",
    r"\bchoking\b", r"\bchokes?\b", r"\bcpr\b", r"\bambulance\b",
    r"\bhigh\s+temperature\b", r"\btemperature\s+of\s+\d", r"\bburning\s+up\b",
)

NOSE_RED_BESIDE = re.compile("|".join("(?:%s)" % pattern for pattern in NOSE_RED))


def _fed_and_unresponsive(before, rest):
    who = re.sub(r"[^a-z ]", " ", before.lower()).split()[-3:]
    what = re.sub(r"[^a-z ]", " ", rest.lower()).split()[:4]
    return bool(set(who) & SMALL_PERSON) and bool(set(what) & A_FEED)

FIT_OF = re.compile(
    r"\bfits?\s+of\s+(?:cough\w*|sneez\w*|giggl\w*|laughter|laughing|screaming|crying|"
    r"the\s+giggles|rage|temper|anger|pique|panic|inspiration)\b")
FIT_ROUTINE = re.compile(
    r"\b(?:every\s+(?:few|couple\s+of|so\s+many)\s+(?:months|weeks|years)|twice\s+a\s+year|"
    r"once\s+a\s+year|a\s+(?:few|couple)\s+of\s+times\s+a\s+year|now\s+and\s+(?:then|again)|"
    r"occasionally|from\s+time\s+to\s+time|keppra|epilep\w*)\b")
FIT_STILL_RINGS = ("cant breathe", "can't breathe", "not breathing", "stopped breathing",
                   "turning blue", "blue lips", "unconscious", "collapsed", "wont stop",
                   "won't stop", "isnt stopping", "isn't stopping", "keeps going", "ambulance",
                   "999", "on the floor", "shaking all over", "convulsing", "stiff")

PRONOUN_SAFE = (
    "had a fit", "has a fit", "having a fit", "having fits", "keeps fitting", "kept fitting",
    "keeps having fits", "kept having fits", "not breathing", "stopped breathing", "unconscious",
    "went limp", "gone limp", "limp in my arms", "limp in her arms", "limp in his arms",
    "no pulse", "seizure", "convulsing", "choking", "overdose", "took too many", "collapsed",
    "cardiac", "isnt breathing", "isn't breathing",
)

SOFT_STATES = frozenset({"floppy", "limp", "confused", "drowsy", "burning up", "very hot to touch",
                         "very sleepy", "sleepy and"})
NORMAL_ASK = re.compile(
    r"\b(?:is that|is it|is this|should i|do i need to)\b[^.?!]{0,40}"
    r"\b(?:normal|ok|okay|fine|worry|worried|worrying|serious|dangerous)\b")

PAST_MARK = re.compile(
    r"\b(?:ago|last (?:year|month|summer|winter|autumn|spring|week)|in (?:19|20)\d\d|"
    r"years back|months back|"
    r"when (?:i|he|she|they|it|we) (?:was|were) (?:a |an )?"
    r"(?:baby|babies|toddler|tot|child|kid|teenager|born|little|small|young|tiny|"
    r"at school|\d+|one|two|three|four|five|six|seven|eight|nine|ten)|"
    r"as a (?:baby|child|kid|toddler|teenager)|used to)\b")

def reads_as_a_story(clean):
    return bool(PAST_MARK.search(clean)) and (
        not NOW_WORDS.search(clean) or bool(ALL_BETTER.search(clean)))


NEARLY = (" almost ", " nearly ", " like to have ")

NOW_WORDS = re.compile(
    r"\b(?:now|right now|still|since|today|tonight|this (?:morning|evening|afternoon)|"
    r"at the moment|any ?more)\b")
ALL_BETTER = re.compile(
    r"\b(?:now|since|and)\b[^.?!]{0,16}\b(?:he|she|they|it|i|we)\s*(?:is|are|was|were|'s)?\s*"
    r"(?:fine|ok|okay|better|recovered|alright|back to normal|himself again|herself again)\b|"
    r"\b(?:now|since)\s*(?:hes|shes|theyre|its|im)\s*(?:fine|ok|okay|better|recovered|alright)\b")

ASKING = (" about ", " what ", " why ", " how ", " should i", " can i", " is that ", " do i")

NOW_REPLIES = (
    "Don't wait on that: ring 999 or 911 now and stay on the line with them. Put them on "
    "their side, tilt the head back so the airway stays open, and don't leave them alone.",
    "That needs an ambulance now. Ring 999 or 911, say exactly what you're seeing, and keep "
    "them on their side while you wait; if they stop breathing normally, start CPR and keep "
    "going until help comes.",
    "Ring 999 or 911 straight away and don't try to drive them in yourself. Stay with them, "
    "check they're breathing, and follow what the call handler tells you.",
)

POISON_NOW_REPLIES = (
    "Ring 999 or 911 now and say what they swallowed and how long ago; keep the packet or the "
    "bottle to read out. Don't make them sick and don't give them anything to drink.",
    "That's a 999 call now, and have the container ready to name to the handler. Keep them "
    "sitting up, wipe their mouth but don't rinse it, and don't try to make them vomit.",
)

POISON_TODAY_REPLIES = (
    "Ring 111 now rather than waiting, and have the packet in your hand: they will tell you "
    "whether they need to be seen. Don't make them sick. If they go sleepy, drool, cough or "
    "struggle to breathe, that's 999.",
    "Get advice on that today - 111 or the poisons line, with the packet to hand - and watch "
    "them closely for the next few hours. Anything drowsy, vomiting, drooling or breathing "
    "oddly means 999.",
)

TODAY_REPLIES = (
    "Get that looked at today rather than waiting: ring 111 or your GP now, and tell them "
    "just what you told me. If they get drowsy, hard to wake, or their breathing changes, "
    "that's 999.",
    "That's worth a call today - 111 or the doctor - and mention how it started. If they get "
    "harder to wake or go blue or floppy, ring 999 instead of waiting.",
)


GAIT_BEFORE = frozenset("a an the this that his her my your their our".split())


def _named_a_gait(clean, start):
    before = clean[:start].split()
    return bool(before) and before[-1] in GAIT_BEFORE


GAIT_STEM = re.compile(r"(?:ing|ed|s)\b")


def _walking(rest):
    return bool(GAIT_STEM.match(rest.lstrip()))


WAKE_OCCASION = frozenset("for to at on before until by".split())
FIGURE_OF_SPEECH = ("at the idea", "at the thought", "at the prospect", "at the mention")


def _signs_a_body(clean, phrase, rest, start=0):
    if phrase == "limp":
        return not _named_a_gait(clean, start) and not _walking(rest)
    if phrase in WAKE_CUES:
        words = rest.split()
        if words and words[0] == "up":
            words = words[1:]
        if not words:
            return True
        if words[0] in WAKE_OCCASION:
            return False
        return bool(set(words[:5]) & WAKE_OBJECT)
    if phrase == "burning up":
        return not any(rest.lstrip().startswith(phrase_) for phrase_ in FIGURE_OF_SPEECH)
    if phrase == "confused":
        return bool(CONFUSED_SIGN.search(clean) or CONFUSED_AFTER.match(rest))
    return True


def _first(clean, phrases):
    for phrase in phrases:
        start = clean.find(phrase)
        while start >= 0:
            rest = clean[start + len(phrase):]
            if phrase not in AMBIGUOUS_CUES:
                return phrase
            if not _signs_a_body(clean, phrase, rest, start):
                start = clean.find(phrase, start + 1)
                continue
            if phrase in VERBY and OBJECTISH.match(rest):
                start = clean.find(phrase, start + 1)
                continue
            if not _not_a_body(rest, clean[:start]):
                return phrase
            start = clean.find(phrase, start + 1)
    return None


PETS = frozenset("""
    dog dogs puppy puppies cat cats kitten kittens rabbit rabbits bunny hamster gerbil guinea pig
    parrot budgie bird birds fish goldfish tortoise turtle snake lizard ferret pony horse horses
    chinchilla
""".split())


LAUGH_IDIOM = re.compile(
    r"\b(?:collaps\w*|went down|doubled over|fell about|fell over)\s+"
    r"(?:laughing|giggling|in (?:a )?(?:fit|stitches|hysterics)|with laugh\w*|helpless)\b")


def _pet_is_the_subject(clean):
    words = WORD.findall(clean)
    for i, word in enumerate(words):
        if word in FAMILY:
            return False
        if word in PETS:
            return True
    return False


def reply_for(text, memory=None):
    clean = " ".join(str(text or "").lower().split())
    if _dream is not None and _dream.a_dream_is_not_happening(clean):
        return None
    if NOSE_BREATH.search(clean) and not NOSE_RED_BESIDE.search(clean):
        return None
    words = set(WORD.findall(clean))
    pronoun_grey = bool(words & {"he", "she", "hes", "shes"}) and bool(GREY_BODY.search(clean))
    if (not words & FAMILY and not pronoun_grey
            and not (words & {"he", "she"} and _first(clean, PRONOUN_SAFE))):
        return None
    if PRO_ANSWERING.search(clean) and not BODY_IN_THE_ROOM.search(clean):
        return None
    if _pet_is_the_subject(clean):
        return None
    if (FIT_OF.search(clean) or FIT_ROUTINE.search(clean)) and not any(
            mark in clean for mark in FIT_STILL_RINGS):
        return None
    if LAUGH_IDIOM.search(clean):
        return None
    if any(mark in clean for mark in DEATH):
        return None
    nearly = any(hedge in " " + clean + " " for hedge in NEARLY)
    swallowed = bool(words & INGEST)
    chem_text = clean.replace("paint ball", " ").replace("paintball", " ")
    chemical = swallowed and any(phrase in chem_text for phrase in CHEMICAL)
    poisoned = swallowed and not chemical and (
        bool(words & MEDICINE) or any(phrase in clean for phrase in SMALL_OBJECT))
    blue = BLUE_LOOSE.search(clean) and BLUE_BODY.search(clean)
    grey = GREY_LOOSE.search(clean) and GREY_BODY.search(clean)
    now = None if nearly else (_first(clean, NOW) or ("is blue" if blue else None)
                              or ("is grey" if grey else None)
                              or ("airway" if STUCK.search(clean) else None)
                              or ("chemical" if chemical else None))
    if now and reads_as_a_story(clean):
        now = None
    if now in SOFT_STATES and NORMAL_ASK.search(clean):
        now = None
    today = None
    if "?" not in clean and not any(ask in " " + clean + " " for ask in ASKING):
        today = _first(clean, TODAY) or ("swallowed" if poisoned else None)
        if today and PAST_MARK.search(clean):
            today = None
    pools = {"chemical": POISON_NOW_REPLIES, "swallowed": POISON_TODAY_REPLIES}
    for state, options in ((now, NOW_REPLIES), (today, TODAY_REPLIES)):
        options = pools.get(state, options)
        if state:
            turns = (memory or {}).get("turns") or []
            recent = {t.get("bot") for t in turns[-5:] if isinstance(t, dict)}
            fresh = [o for o in options if o not in recent] or list(options)
            seed = len(turns) * 7919 + sum(ord(c) for c in clean)
            return random.Random(seed).choice(fresh)
    return None
