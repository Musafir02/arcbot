import re

from . import lexicon
from .normalize import (KIN, UP_TO_LEADS, background_clause, background_positions,
                        opens_without_subject, strip_leaders)

NEGATIONS = lexicon.NEGATIONS
PRONOUNS = frozenset("i you we they he she it there that this these those one".split())
SUBJECT_NEGATIONS = frozenset("no nobody none nothing neither nor".split())

GREETINGS = ("hi", "hello", "hey", "hiya", "morning", "good morning", "good afternoon",
             "good evening", "evening", "yo", "howdy", "good day", "greetings",
             "salutations")
FAREWELLS = ("bye", "goodbye", "see you", "see ya", "later", "night", "good night",
             "talk later", "take care", "ttyl", "gtg", "cya", "best wishes", "best regards",
             "kind regards", "warm regards",
             "ttfn", "cheerio", "laters", "adios", "night night", "nighty night",
             "ta ta", "see you later", "see you soon", "talk to you later",
             "speak later", "speak to you later", "catch you later", "bye for now")
THANKS = ("thanks", "thank you", "thx", "cheers", "ty", "ta", "much appreciated",
          "appreciate", "appreciated", "appreciate it")

QUESTION_WORDS = frozenset("what why how when where who which whose".split())
THANKS_ASK_NOUNS = frozenset("advice tip tips idea ideas suggestion suggestions".split())
THANKS_ASK_PREPS = frozenset("for on about with".split())
THANKS_ASK_WORDS = frozenset("any need needs looking".split())
GIVEN_ADVICE = frozenset("the your my our his her its their this that no".split())
QUESTION_STARTS = {"what", "why", "how", "when", "where", "who", "which", "whose", "can",
                   "could", "should", "would", "is", "are", "do", "does", "did", "will",
                   "have", "has", "am", "was", "were", "may", "might", "shall"}
YESNO_STARTS = QUESTION_STARTS - {"what", "why", "how", "when", "where", "who", "which",
                                  "whose"}


AFFIRM = frozenset("yes yeah yep yup yh yhh yhhh ye sure ok okay definitely absolutely correct "
                   "right probably "
                   "maybe perhaps likely "
                   "true exactly indeed agreed fine cool great nice good perfect sounds "
                   "works deal done sweet brilliant".split())
DENY = frozenset("no nope nah never not nothing none neither".split())
ACK = frozenset("ok okay cool nice great good fine sure right got understand understood "
                "thanks aha ah oh wow really hmm hm mmm alright k gotcha you me same maybe "
                "perhaps probably likely haha hehe lol fair true".split())
LAUGH = frozenset(lexicon.LAUGHTER)
POLITE = frozenset("please pls plz ta mate".split())

RECOMMEND = frozenset("recommend suggest recommendation suggestion advice idea ideas "
                      "options option pick choose best better worth".split())
TIPS = re.compile(r"\b(tips|hints|pointers|tip|hint|pointer)\b")
TIPS_WANTED = re.compile(r"\b(?:any|some|a few|few|got|need|needs|wanted|looking for|share|"
                         r"send|give(?: me)?)\s+(?:\w+\s+){0,2}$")
TIPS_ABOUT = re.compile(r"\s+(?:for|on|about|when|to)\s+\w")
TIPS_SUBJECT = re.compile(r"\b(?:i|you|we|they|he|she|it|who|that|this|people|everyone|"
                          r"nobody|someone)\s*$")
TIPS_AMOUNT = re.compile(r"(?:\d|%|\b(?:a|the)\s+\w+\s*%)\s*$")
HELP_ASK = re.compile(
    r"\b(?:anything|something)\s+(?:else\s+)?(?:i|we|you)\s+(?:can|could|should|might|would)\s+"
    r"(?:do|try|use|take|add|change)\b"
    r"|\b(?:anything|something)\s+(?:else\s+)?(?:that|which)\s+(?:helps|would help|might help|"
    r"will help|works)\s*[?.!]*\s*$"
    r"|\bany\s+(?:way|ways)\s+(?:of|to|round)\b"
    r"|\bis there any\s+(?:way|ways|thing)\s+(?:of|to|i|we|you|else)\b")
HELP_ASK_SUBJECT = re.compile(
    r"\b(?:is|was|are|were|seems|seemed|feels|felt|sounds|sounded|helps|helped|works|worked|"
    r"suits|suited|fits|fitted|does|did|its|thats|im|youre|"
    r"(?:would|will|might|must|could|can|may) be)\b")
HELP_ASK_TAIL_CLAUSE = re.compile(r"\|\s*\w+\s+\w+")
HELP_ASK_NOT = re.compile(
    r"\b(?:no|not|isnt|isn't|wasnt|wasn't|arent|aren't|cant|can't|couldnt|couldn't|dont|don't|"
    r"doesnt|doesn't|didnt|didn't|never|nothing|without|hardly)\b")
HELP_ASK_OWN_SUBJECT = re.compile(
    r"\b(?:my|our|his|her|their|your|the|a|an)\s+[a-z]")


def _asks_for_help(text):
    if HELP_ASK_OWN_SUBJECT.search(text):
        return False
    for match in HELP_ASK.finditer(text):
        if HELP_ASK_NOT.search(text[:match.start()]):
            continue
        tail = text[match.end():]
        if HELP_ASK_SUBJECT.search(tail) or HELP_ASK_TAIL_CLAUSE.search(tail):
            continue
        return True
    return False

VERDICT_ASK = re.compile(
    r"(?:and |so |but |ok |okay |also |sorry |oh |hmm )*"
    r"(?:"
    r"(?:is|was|are|were|does|do|did) (?:that|this|it)(?: all)?"
    r"(?: (?:really|actually|very|too|that|so))?"
    r"(?: (?:bad|normal|serious|dangerous|ok|okay|fine|safe|common|"
    r"a|much of a) ?"
    r"(?:problem|worry|issue|big deal)?"
    r"| (?:going to|gonna) (?:get|be) worse"
    r"| (?:going to|gonna) (?:spread|get worse))"
    r"|(?:is|was) (?:that|this|it)(?: (?:going to|gonna))? (?:get worse|getting worse|spread|serious)"
    r"|(?:is|was) (?:he|she|they) right"
    r"|(?:are|were|is|was) (?:they|these|those) (?:safe|ok|okay|fine|normal|bad|a problem|a risk|any good)"
    r"|(?:should|do|ought) i (?:be )?(?:worried|worry|worrying|bother)"
    r"|does (?:that|this|it) matter"
    r"|will (?:that|this|it) (?:get|be) (?:worse|ok|okay|fine)"
    r")"
    r"(?: then| though| honestly)?")


QUESTION_WORD = re.compile(r"\b(?:why|when|where|how|who|whom|whose|which|what)\b")


def _asks_a_verdict(text):
    flat = re.sub(r"[^a-z0-9 ]+", " ", (text or "").lower())
    flat = re.sub(r"\s+", " ", flat).strip()
    if not flat:
        return False
    words = flat.split()
    if len(words) > 30:
        return False
    if VERDICT_ASK.fullmatch(flat) is not None:
        return True
    for start in range(1, len(words) - 1):
        if len(words) - start > 7:
            continue
        if QUESTION_WORD.search(" ".join(words[:start])):
            return False
        if VERDICT_ASK.fullmatch(" ".join(words[start:])) is not None:
            return True
    return False


LIMIT_SHAPES = (
    ("no", re.compile(r"\bno\s+(?:more\s+)?([a-z][a-z' -]*?)\s*$")),
    ("nothing", re.compile(r"\bnothing\s+([a-z][a-z' -]*?)\s*$")),
    ("not", re.compile(r"\bnot\s+(?:too|very|that|so|any)\s+([a-z][a-z' -]*?)\s*$")),
    ("not_the", re.compile(r"\bnot\s+the\s+([a-z][a-z' -]*?)\s+ones?\s*$")),
    ("without", re.compile(r"\bwithout\s+(?:the\s+|any\s+)?([a-z][a-z' -]*?)\s*$")),
    ("skip", re.compile(r"\b(?:skip|hold|drop|minus|leave out)\s+(?:the\s+|any\s+)?"
                        r"([a-z][a-z' -]*?)\s*$")),
    ("dont", re.compile(r"\bi\s+(?:dont|do not|can't|cant|can not)\s+(?:eat|drink|like|want|"
                        r"have)\s+([a-z][a-z' -]*?)\s*$")),
    ("allergic", re.compile(r"\bi\s+(?:am|m)\s+allergic\s+to\s+([a-z][a-z' -]*?)\s*$")),
)
LIMIT_SOFT_BEFORE = re.compile(
    r"^(?:ok|okay|so|and|but|well|right|then|also|honestly|hmm|oh|ah|actually|btw)\b[\s,]*")
LIMIT_SOFT_AFTER = re.compile(
    r"[\s,]*(?:please|pls|thanks|thank you|then|though|tbh|honestly|lol|for me|this time|"
    r"at all|i guess|i suppose|to be honest|as well|instead)\s*$")
LIMIT_ROOM = 3
LIMIT_REFUSAL = frozenset("""idea clue way sure bad good luck doubt joke point matter rush hurry
wonder worries worry problem bother chance need thanks ta worries offence offense kidding
question answer option options choice change pain help helps well right myself yourself self
left yet though either sorry wait enough much many more less quite finished still now bake
since until after before""".split())
LIMIT_A_FACT = frozenset("""january february march april may june july august september october
november december monday tuesday wednesday thursday friday saturday sunday today tomorrow
yesterday morning afternoon evening night week weekend month year
one two three four five six seven eight nine ten eleven twelve twenty thirty forty fifty
hundred thousand couple few half lot""".split())
LIMIT_NOT_A_START = frozenset("""with without about for from by like not probably maybe wait sorry
enough too very much many more less just only at all and or but so then also""".split())
PAST_ENDS = re.compile(r"^(?:[a-z]{3,}(?:ed|ought|aught)|went|got|came|said|saw|made|took|gave|"
                       r"found|lost|left|ran|broke|fell|kept|met|paid|put|sent|sat|stood|"
                       r"thought|told|won|wrote|bought|brought|caught|chose|drove|flew|forgot|"
                       r"heard|held|hit|knew|ate|drank|slept|woke|bit|spoke|spent|built|burnt|"
                       r"burned|grew|threw|been|being)$")
A_THING_NOT_A_CLAIM = frozenset("""works work helps help changes happens matters seems makes does goes
comes gets stops starts fixes fits runs moves shows feels looks sounds costs needs stays keeps turns
grows hurts adds counts means bothers lives takes gives brings appeals excites suits
satisfies interests improves settles lasts ends agrees sticks sorts arrives
# The irregular pasts, which no ending rule reaches: "nothing got sorted", "nothing came of it",
# "nothing went right", "nothing did". Each of those was answered with the answer described back
# at the person - "Nothing there was about got sorted, so the answer holds" - so the verb is
# listed in the tense it is said in as well as the one the list starts in.
got came went did was were""".split())
CLAIM_ENDS = ((3, "ing"), (1, "s"), (2, "ed"), (1, "d"))
CLAIM_STEMS = frozenset(form[:-1] if form.endswith("s") and len(form) > 3 else form
                        for form in A_THING_NOT_A_CLAIM)


def _claim_forms(word):
    forms = {word}
    for cut, _suffix in CLAIM_ENDS:
        if len(word) > cut + 2:
            forms.add(word[:-cut])
    if word.endswith("ing"):
        forms.add(word[:-3] + "e")
    for form in list(forms):
        if len(form) > 3 and form[-1] == form[-2]:
            forms.add(form[:-1])
    return {form[:-1] if form.endswith("s") and len(form) > 3 else form for form in forms}


def names_a_claim(word):
    word = str(word or "").lower()
    if word in A_THING_NOT_A_CLAIM:
        return True
    return any(form in CLAIM_STEMS for form in _claim_forms(word))


LIMIT_NOT_A_THING = frozenset("""i me my we you he she they it them us her him his hers its our
ours your yours their theirs mine whom is are was were be been
am do does did have has had can could would should will just really very too so much any some
the a an of to for in on at and or but if that this these those there here what when where who
something anything everything nothing other else matter way bit lot lots one ones thing things
to""".split())


RULED_OUT = re.compile(
    r"\b(?:not\s+(?:a|an|the)|rather than\s+(?:a|an|the)?|instead of\s+(?:a|an|the)?)"
    r"\s+([a-z][a-z'’-]*(?:\s+[a-z][a-z'’-]*){0,2})", re.I)

RULED_OUT_ENDS = frozenset("""and but or so because if when then please though although actually
really either too now tonight today anyway for with in on at to of is are was were be been do does
did have has had can could would should will""".split())


RULED_OUT_NO_THING = frozenset("""what about recommend recommends suggest show give find is are was
were do does did can could would should will you u ur me my i we us the a an of to for in on at
and but or so if when then there here this that these those it its be been have has had any some
please thanks ok okays just also too more most than rather instead not no yes something anything
anything""".split())


_A_CLASS_OF_THING = []


def _a_class_of_thing():
    if not _A_CLASS_OF_THING:
        from ..compose.ruledout import RULED_OUT_CLASS, RULED_OUT_INSTANCES
        words = set(RULED_OUT_CLASS)
        for members in RULED_OUT_INSTANCES.values():
            words |= set(members)
        _A_CLASS_OF_THING.append(frozenset(words))
    return _A_CLASS_OF_THING[0]


RULED_OUT_CORRECTION = re.compile(
    r"\b(?:actually|i mean|sorry|make that|on second thoughts?|rather|instead|no,|nope)\b", re.I)


def _ruled_out_of(text):
    if not text:
        return []
    gone = []
    for match in RULED_OUT.finditer(text):
        said_before = text[:match.start()]
        before = [word.strip(" .,!?;:\'\u2019").lower() for word in said_before.split()][-3:]
        if not [word for word in before if word and word not in RULED_OUT_NO_THING]:
            continue
        if [word for word in match.group(1).split() if word.lower() in _a_class_of_thing()]:
            continue
        same_thing = match.group(1).split()[-1].lower() in ("one", "ones")
        if not same_thing and not RULED_OUT_CORRECTION.search(said_before):
            continue
        for word in match.group(1).split():
            word = word.strip(" .,!?;:'\u2019\u201c\u201d")
            if not word:
                break
            if word.lower() in RULED_OUT_ENDS:
                break
            gone.append(word)
            if len(gone) >= 4:
                break
    return gone


def _limit_of(text):
    if not text:
        return None
    ask = " ".join(text.replace("|", " ").split()).strip(" .,!?").lower()
    for _ in range(3):
        shorter = LIMIT_SOFT_BEFORE.sub("", ask)
        if shorter != ask:
            ask = shorter
        shorter = LIMIT_SOFT_AFTER.sub("", ask).strip(" .,!?")
        if shorter != ask:
            ask = shorter
        if ask == LIMIT_SOFT_BEFORE.sub("", LIMIT_SOFT_AFTER.sub("", ask)).strip(" .,!?"):
            break
    for _name, shape in LIMIT_SHAPES:
        match = shape.search(ask)
        if match is None:
            continue
        thing = " ".join(match.group(1).split()).strip(" .,!?")
        words = thing.split()
        if len(words) > 1 and words[-1] in ("one", "ones"):
            thing = " ".join(words[:-1])
            words = thing.split()
        if not words or len(words) > LIMIT_ROOM:
            continue
        if any(word in LIMIT_NOT_A_THING for word in words):
            continue
        if any(word in LIMIT_REFUSAL for word in words):
            continue
        if words[0] in LIMIT_NOT_A_START:
            continue
        if PAST_ENDS.match(words[-1]):
            continue
        if ask.startswith("nothing") and names_a_claim(words[-1]):
            continue
        if any(word in LIMIT_A_FACT or word.isdigit() for word in words):
            continue
        before = ask[:match.start()].strip(" .,!?")
        if before and not LIMIT_SOFT_BEFORE.sub("", before + " ") == "":
            continue
        return thing
    return None


RECOMMEND_PHRASES = ("any good", "something good", "anything good", "worth watching",
                     "worth reading", "what should i watch", "what should i read",
                     "any ideas", "what would you recommend", "what do you recommend",
                     "help me choose", "help me pick", "any suggestions")
OPINION = ("what do you think", "what about you", "your favourite", "your favorite",
           "do you like", "do you prefer", "would you rather", "in your opinion",
           "what would you", "how about you")
CHOICE = (" or ", "better than", "instead of", "vs", "versus")

OPPOSITE_PAIRS = (
    ("early", "late"), ("earlier", "later"), ("sooner", "later"), ("soon", "late"),
    ("hot", "cold"), ("warm", "cold"), ("big", "small"), ("large", "small"),
    ("long", "short"), ("high", "low"), ("good", "bad"), ("better", "worse"),
    ("wet", "dry"), ("sunny", "rainy"), ("fast", "slow"), ("quick", "slow"),
    ("cheap", "expensive"), ("busy", "quiet"), ("loud", "quiet"), ("full", "empty"),
    ("deep", "shallow"), ("heavy", "light"), ("thick", "thin"), ("wide", "narrow"),
    ("hard", "soft"), ("early", "on time"),
    ("in", "out"),
)


SCALE_ASK = re.compile(r"^\s*(?:is|are|was|were|will|would|should|when|what|how|which|be)\b")


def two_ends_of_one_scale(text):
    if not (SCALE_ASK.match(text) or "sooner or later" in text):
        return False
    for one, other in OPPOSITE_PAIRS:
        for first, second in ((one, other), (other, one)):
            if re.search(rf"\b(?:the |a |an )?{first}\s+or\s+(?:the |a |an )?{second}\b",
                         text):
                return True
    return False
REFUSED_PAIR = re.compile(
    r"^\s*(?:no|not|never|without|neither)\b"
    r"|\b(?:dont|don'?t|do not|doesnt|doesn'?t|didnt|didn'?t|wont|won'?t|wouldnt|wouldn'?t|"
    r"cant|can'?t|cannot|shouldnt|shouldn'?t)\s+(?:\w+\s+){0,2}?"
    r"(?:want|wants|wanted|like|likes|love|eat|eating|have|having|drink|drinking|wear|do|doing|"
    r"need|needs|use|fancy|stand|bother|manage)\b"
    r"|\ballergic\b|\bhate\b")


def _turns_the_pair_down(text):
    head = str(text or "").lower().split(" or ")[0]
    return bool(REFUSED_PAIR.search(head))


COMPARE = ("difference between", "different from", "compare", "which one", "or is it")

REQUEST = frozenset("help need want trying wanna please tell show explain give write make "
                    "how".split())
STEPS = ("how do i", "how can i", "how should i", "what should i", "step by step",
         "walk me through", "get started", "how to")
STEPS_WORD = re.compile(r"\bsteps\b")
WRITE = ("write", "word", "phrase", "say", "message", "text to", "email to", "letter",
         "poem", "speech", "bio", "caption", "wish")
A_COMPARISON = frozenset(("worse",))
SELF_ONLY_CUES = (
    "empty", "flat", "hollow", "blank", "numb",
    "rubbish", "crap", "rotten", "rough", "lousy",
    "like a failure", "like a mess", "like rubbish", "like crap", "like a burden",
    "like a fraud", "a mess",
    "in a bad mood", "in a low mood", "in a foul mood", "in a mood", "in a state",
    "in a right state", "out of sorts", "off colour", "off form",
)
CONFUSED_SELF_ONLY = frozenset(("confused", "confusing", "confusion", "muddled", "baffled",
                                "bewildered", "puzzled"))
LABEL_ON_A_PERSON = frozenset((
    "boring", "annoying", "tiring", "exhausting", "draining", "knackering", "frustrating",
    "depressing", "embarrassing",
))
THING_OR_PERSON_CUES = frozenset((
    "worn thin", "worn to a thread", "at my limit", "at breaking point",
    "at my wits end", "at my wits' end", "beside myself", "at the end of my patience",
    "reaching the end of my rope",
    "worrying", "stressing", "stressed out", "overthinking", "obsessing", "spiralling",
    "spiraling", "worn down",
))
OWN_PERIOD_NOUNS = frozenset("""day days week weeks month months year years weekend weekends
night nights morning mornings afternoon afternoons evening evenings shift shifts term""".split())
OWN_PERIOD_FILLER = frozenset("""a an the one few couple of real proper whole entire bit those
these sort kind old long bad""".split())
OWN_PERIOD_HEADS = frozenset("""i we i've ive me today yesterday tonight""".split())
OWN_PERIOD_STOPS = frozenset("""and but because so though while if when than then that which
who whose after before since until""".split())
NOT_THE_SPEAKERS_DAY = frozenset(("mad", "flat", "dead", "mental", "wild", "slow", "heavy"))
OWN_PERIOD_REACH = 6

PERIOD_CUES = frozenset(("at my limit",))
A_PERIOD = re.compile(
    r"\b(?:every|each|this|next|last|a|per)\s+"
    r"(?:(?:single|whole|full|other|coming|past|few|one|more)\s+)*"
    r"(?:month|week|fortnight|pay ?day|paycheck|wage)\b"
    r"|\bmonthly\b|\bweekly\b|\bfortnightly\b|\bpay ?day\b")
A_MONTH_PERIOD = re.compile(r"\b(?:month|monthly)\b|\bpay ?day\b")
A_MONEY_SUBJECT = re.compile(
    r"\b(?:rent|mortgage|bills?|electric(?:ity)?|gas|water|council tax|overdraft"
    r"|credit card|loan|debt|debts|childcare|nursery fees|fees|fuel|heating)\b")
A_LIMIT_ABOUT_PEOPLE = re.compile(
    r"\b(?:with (?:the|my|our|their|his|her|these|those)\s+"
    r"(?:kids?|children|child|family|mum|mom|dad|parents|partner|husband|wife|boss|team)"
    r"|at work|at school|at college)\b")


LAUGHED_OFF_AFTER = re.compile(
    r"(?:with\s+|in\s+)?(?:laughter|laughing|laughs|cracking up|stitches)\b")


def _laughed_off(text, cue):
    for match in re.finditer(r"\b" + re.escape(cue) + r"\b", text):
        if LAUGHED_OFF_AFTER.match(text[match.end():].strip()):
            return True
    return False
SAD_PLAIN_CUES = (
    "dead inside", "feel nothing", "like nothing matters", "not myself", "not feeling myself",
    "not been myself", "do not feel myself", "do not feel like myself", "have not felt myself",
    "have not been myself",
)
SELF_ONLY_STATE = frozenset(
    "low awful hopeless worthless shattered wiped wasted spent "
    "tense pooped whacked zonked "
    "blue "
    "raging fuming seething incandescent".split())
BODY_STATE_CUES = frozenset(("upset", "low", "awful", "rough", "rotten"))

IDIOM_STATES = re.compile(r"\bflat\s+(?:out|broke)\b|\bflat as (?:a|an) \w+|"
                          r"\bcheap\s+and\s+cheerful\b|"
                          r"\bin (?:a|the) mood for\b|"
                          r"\b(?:bit of a|a bit of a|a right|a proper)\s+"
                          r"(?:mad|weird|strange|funny|odd|daft|curious)\s+one\b")


HEART_DEGREES = (r"(?:still|really|so|very|totally|completely|utterly|absolutely|just|all|"
                  r"now|quite|too|already|a bit|kind of|sort of)")
HEART_IN_A_STATE = re.compile(
    r"\bheart(?:s|'s)?\b"
    r"(?:\s+(?:is|was|feels|felt|seems|has|had|been))*"
    r"(?:\s+" + HEART_DEGREES + r")*"
    r"\s+(?:broken|shattered|torn|in pieces|aching|aches|breaks|heavy|breaking)\b")
BROKEN_HEARTED = re.compile(r"\b(?:broken[\s-]?hearted|heart[\s-]?broken)\b")
A_BROKEN_HEART = re.compile(r"\b(?:a|an|my|our|her|his|their|your)\s+broken\s+heart\b")
BROKE_A_HEART = re.compile(r"\b(?:broke|breaks|breaking|break)\s+(?:my|our|her|his|their|your)\s+heart\b")

EMOTION_WORDS = {
    "sad": ("sad", "unhappy", "miserable", "gutted", "heartbroken", "cry", "crying", "tears",
            "disappointed", "devastated", "weepy", "tearful", "homesick", "rotten", "lousy",
            "meh", "rough", "crap", "rubbish", "fed up", "numb", "blue",
            "at my wits end", "at my wits' end", "at my limit", "at breaking point",
            "at the end of my patience", "reaching the end of my rope",
            "glum", "mopey", "teary", "downhearted", "despondent", "blah", "bleh",
            "low", "upset", "awful", "hopeless", "worthless", "grieving", "mourning",
            "despair", "despairing", "in a dark place", "emotional") \
        + SELF_ONLY_CUES + SAD_PLAIN_CUES,
    "lonely": ("lonely", "alone", "isolated", "left out"),
    "angry": ("angry", "annoyed", "furious", "cross", "irritated", "frustrated", "mad",
              "grumpy", "cheesed off",
              "cranky", "snappy", "tetchy", "ratty", "mardy",
              "livid", "seething", "fuming", "raging", "seeing red", "incandescent",
              "brassed off", "narked", "miffed", "in a strop"),
    "anxious": ("anxious", "worried", "nervous", "scared", "afraid", "stressed", "stress",
                "panic", "panicking", "overwhelmed", "dreading", "bricking it",
                "bricking myself", "shitting myself", "crapping myself",
                "shitting it", "crapping it", "cacking myself", "cacking it",
                "shitting bricks", "butterflies",
                "on edge", "nervous wreck", "worried sick", "freaking out", "petrified", "anxiety",
                "terrified", "panicky", "in bits", "restless",
                "jittery", "antsy", "edgy", "tense", "apprehensive",
                "beside myself",
                "worrying", "stressing", "stressed out", "overthinking", "obsessing",
                "spiralling", "spiraling"),
    "tired": ("tired", "exhausted", "knackered", "worn out", "drained", "no energy",
              "burned out", "burnt out", "shattered", "wiped out", "wiped",
              "zonked", "pooped", "whacked", "frazzled",
              "worn thin", "worn to a thread", "worn down",
              "fried",
              "think straight", "running on empty", "running on fumes", "head is mush",
              "heads mush", "keep my eyes open",
              "dead"),
    "happy": ("happy", "glad", "delighted", "thrilled", "pleased", "excited", "proud",
              "relieved", "chuffed", "awesome", "hopeful", "cheerful"),
    "grateful": ("grateful", "thankful", "appreciate"),
    "bored": ("bored", "boring", "nothing to do"),
    "confused": ("confused", "confusing", "confusion", "bewildered", "baffled", "muddled",
                 "puzzled", "dont understand", "do not understand", "dont get it",
                 "do not get it", "does not make sense", "makes no sense",
                 "cant get my head round", "cant get my head around", "cant get my head straight",
                 "cannot get my head round", "cannot get my head around",
                 "can not get my head round", "can not get my head around",
                 "cannot get my head straight", "can not get my head straight",
                 "cant make head nor tail", "cannot make head nor tail",
                 "can not make head nor tail",
                 "cant make head or tail", "cannot make head or tail",
                 "can not make head or tail",
                 "struggling to understand", "struggling to follow"),
    "unwell": ("hungover", "hung over", "hangover", "under the weather", "run down",
               "worse",
               "run-down", "jet lagged", "jet-lagged",
               "cream crackered", "crackered"),
    "condition": ("bipolar", "schizophrenic", "anorexic", "bulimic", "narcoleptic", "psychotic",
                  "infertile", "sterile", "paranoid", "transgender", "nonbinary", "hiv"),
}
ALWAYS_SELF_ONLY = frozenset((
    "dead", "fried", "running on empty", "running on fumes"))
SAID_AS_A_NEGATION = frozenset(("think straight", "keep my eyes open"))
NOT_A_MOOD_THERE = {
    "dead": re.compile(r"\bdead\s+(?:set|right|against|certain|last|heat|giveaway|cert|"
                       r"keen|to me|to the world)\b"
                       r"|\bso dead\b"),
    "fried": re.compile(r"\bfried\s+(?:rice|chicken|egg|eggs|bread|onion|potatoes|tomatoes|"
                        r"fish)\b"),
    "think straight": re.compile(r"\b(?:he|she|they|my|his|her|their|its)\b[^.|]{0,20}"
                                 r"\bthink straight\b"),
}
GOOD_EMOTION_NAMES = frozenset(("happy", "grateful"))
NEGATIVE = frozenset("""sad unhappy miserable gutted heartbroken cry crying tears disappointed
devastated lonely alone angry annoyed furious frustrated mad anxious worried nervous scared
afraid stressed panic overwhelmed dreading tired exhausted knackered drained sick ill hurt
pain ache sore worse worst hate awful terrible horrible bad fail failed failing lost lose
hate rubbish useless stupid annoyed upset""".split())
POSITIVE = frozenset("""happy glad delighted thrilled pleased excited proud relieved grateful
thankful love loved lovely great good nice brilliant wonderful perfect amazing fantastic
fun funny enjoy enjoyed success succeeded won win calm relaxed fine okay""".split())
TERMS_OF_ADDRESS = frozenset("""love mate pet hun honey sweetheart duck ducky flower sunshine
    pal bud chick dear darling babe lass lad bella""".split())
ADDRESSED_LINES = frozenset("""thanks thank cheers ta hello hi hiya hey morning afternoon
    evening night bye goodbye yes no ok okay alright right please sorry""".split())
OK_WORDS = frozenset(("ok", "okay", "okey"))
SAYS_HOW_THEY_ARE = frozenset("""alright alrighty grand sound chill content brill mint
    sorted""".split())
STATING_VERB = frozenset("""am is are was were feel feels feeling felt do does doing be been
    seem seems look looking""".split())
SPEAKER = frozenset(("i", "we"))
NEWS = ("i just", "i finally", "today i", "yesterday i", "we got", "we are getting",
        "i got", "i have just", "i have just", "guess what", "big news", "i start",
        "i started", "i finished", "i passed", "i failed", "i moved", "we moved")
ABOUT_BOT = ("are you a bot", "are you real", "are you human", "are you an ai",
             "are you alive", "are you ok", "do you have feelings", "your name",
             "do you remember", "can you remember", "how old are you", "what are you called",
             "are you a chatbot", "are you a person")
ABOUT_BOT_END = ("what are you", "who are you", "what are you exactly")
ROBOT_WORDS = frozenset("bot chatbot robot ai human person machine program real alive".split())
GENDER_WORDS = frozenset("male female man woman men women boy girl".split())
TASTE_VERBS = frozenset("like love prefer fancy enjoy hate dislike".split())


def _a_person_they_like(norm):
    for at, word in enumerate(norm):
        if word in TASTE_VERBS and set(norm[at + 1:]) & GENDER_WORDS:
            return True
    return False


LEARNED_ON = frozenset("data internet".split())


def _a_thing_they_own(norm):
    if not set(norm) & LEARNED_ON:
        return False
    return not set(norm) & (SELF_ASK - LEARNED_ON)


ASSISTANT_NAMES = frozenset("claude chatgpt gpt gemini copilot siri alexa bard".split())
PRODUCT_ASK_WORDS = 7
PRODUCT_ASK_TAIL = frozenset("then really though now huh yeah or not at all literally exactly "
                             "still please pls tho".split())

SELF_WORDS = frozenset("""you your yourself yours
name called call
made make create created built build built trained train programmed program designed design
wrote written
origin creator
hobbies hobby fun looking look looks
plans plan
bored busy tired awake
feel feelings dream dreams dreamt sleep eat
real alive human person bot robot ai chatgpt gpt claude gemini copilot siri alexa bard
understand remember recall forget
chat talking talk chats answering answer
doing get
from tell
heart soul souls emotion internet data male female man woman men women
model models llm llms personality single married live learn learnt asleep
cry laugh hungry drunk boy girl gender old young
okay ok alright fine""".split())
SELF_ASK = frozenset("""name called call made make create created built build trained train
programmed program designed design wrote written origin creator hobbies hobby fun looking look
looks plans plan bored busy real alive human person bot robot ai chatgpt gpt claude gemini
copilot siri alexa bard understand
remember recall forget get from tell heart soul souls emotion internet data
male female man woman men women personality single married live sleep eat dream dreams
asleep cry laugh hungry drunk boy girl gender old young""".split())
SELF_FILLER = frozenset("""what why how who where when which whose is are was were am do does
did can could will would shall should have has had a an the any some your you yourself yours
i me my at from about like of for to with now then today tonight ever actually really even
still just so much very both all or either on in by using up and so then ok okay""".split())
NOT_AFTER_THE_BOT = frozenset("you youre your u ur ya are is this it thats that".split())
NOT_BEFORE_THE_BOT = frozenset("you u ur ya your yourself yours".split())
NOT_AUX = frozenset("""can could will would do does did are is was were am have has had
    should shall""".split())
CLAUSE_OPENERS = frozenset("""when whenever if once after before until till while since
    as because unless though although""".split())
CAPABILITY = ("what can you do", "what do you do", "how do you work", "what can you help",
              "how can you help", "how do you help", "what can i ask you",
              "what are you good at", "what are you for", "what kind of things can you help")
CAPABILITY_FILLER = frozenset("actually exactly really just still even then now here please "
                              "mate pal though anyway so also "
                              "else other and but oh yeah ok okay well um hmm".split())
CAPABILITY_CARRIER = frozenset("""
    with for about me us at in on during here around then now any anything
    a an the living this that these those next last another more some all
    usually often
    tonight today tomorrow later evening morning afternoon night week weekend
    time times day days evening evenings night nights week weeks weekend weekends
    month months year years hour hours minute minutes second seconds while bit
    one two three four five ten fifteen twenty thirty sixty couple few half
""".split())
CORRECTION = ("i meant", "i mean", "sorry i meant", "rather than", "not ", "actually i",
              "correction", "i said", "no wait", "wait no", "oops i meant", "scratch that")
GOING_ON_WHEN = frozenset("""tonight today tomorrow later week weeks weekend morning evening
    night saturday sunday monday tuesday wednesday thursday friday now""".split())
DOING_FILLER = frozenset("""what whats u you ya r are is doing do up to too much been have
    has lately now today tonight then at the moment anything something nothing going on this
    week new else still with watcha whatcha wotcha watchu whatchu doin mate pal buddy love
    lovey hon hun then friend""".split())
BEEN_WHEN = frozenset("""yesterday today last night nights morning mornings afternoon afternoon
    evening evenings weekend weekends week weeks day days these all the at over on in this since
    so far lately recently""".split())
BEEN_SAID = frozenset("""did done been were was had doing do up where get got""".split())
SPENT_TIME = frozenset("""all whole day days night nights week weeks lately recently since far
    these hiding""".split())
STILL_COMING = frozenset("""tomorrow tonight later next""".split())

SMALL_TALK = ("how are you", "how is it going", "how's it going", "how is your day",
              "how's your day", "nice to meet you", "what's up", "how do you do",
              "lovely weather", "freezing", "raining", "sunny", "long week", "busy day")
ASK_KEYS = ("how_long", "how_much", "how_many", "how_often", "what", "why", "how", "when",
            "where", "who", "which", "yesno", "choice", "recommend", "steps", "opinion",
            "compare", "definition", "write", "maths", "list")
SHORT_REPLIES = ("not much", "nothing much", "same here", "me too", "you too", "no idea",
                 "not really", "sort of", "kind of", "fair enough", "sounds good",
                 "sounds great", "good idea", "will do", "i will", "i agree", "me neither",
                 "makes sense", "got it", "for sure", "why not", "of course", "i guess",
                 "that is fair", "no worries", "all good", "very funny", "so true",
                 "not bad", "not a lot", "not a clue", "no bother", "i suppose", "guess so",
                 "u too", "you as well", "same to you", "back at you", "hbu", "wbu", "nmu",
                 "true that", "fair point", "good point", "my pleasure", "any time",
                 "not really sure", "i think so", "hopefully", "probably", "definitely",
                 "absolutely", "exactly", "agreed", "correct", "right", "true",
                 "i dont know", "dont know", "i dunno", "dunno", "who knows", "no clue",
                 "search me", "you know", "not sure", "no idea to be honest",
                 "i do not know", "do not know", "not much", "how about you",
                 "i know right", "you are welcome", "no problem", "same old", "same as always",
                 "what about you", "not too bad")
AGREEMENT_IDIOMS = ("tell me about it", "you are telling me", "do not i know it",
                    "you can say that again", "you are not wrong", "preaching to the choir",
                    "you and me both", "i know right", "i hear that", "amen to that")


def agreement_of(text):
    said = " ".join(text.lower().replace(",", " ").split())
    first = " ".join(said.split("|")[0].split())
    flat = " ".join(said.replace("|", " ").split())
    return next((phrase for phrase in AGREEMENT_IDIOMS
                 if flat == phrase or first == phrase), None)
EVENT_WORDS = frozenset("""asked told said got went started finished had was were just
today yesterday tomorrow week weekend month year moved passed failed lost found bought sold
paid booked applied interview job trip visit party birthday meeting doctor dentist school
work flat house car dog cat baby wedding holiday""".split())
MATH_WORDS = frozenset("plus minus times divide divided percent percentage half double "
                       "triple sum total average calculate equals".split())
DEFINITION = ("what is a", "what is an", "what are", "what does", "difference between",
              "meaning of", "explain")
ASKS_ABOUT_A_PERSON = re.compile(r"\bwhat (?:is|are|r) (?:you|u|ya|we|us|they)\b")

BARE_DEFINITION = re.compile(
    r"^\s*(?:(?:and|but|so|then|ok|okay|right|oh|well|now|sorry|hi|hello|please)\s+)*"
    r"what(?:'s|s| is| are| was)?\s+(?:is|are|was)\s+([a-z][a-z'\u2019-]{1,28})"
    r"(?![^?]*\b(?:like|for|worth|good|cheap|cheapest|easier|easiest|better|best|worse|worst|"
    r"date|time|day|weather|price|cost|news|forecast|temperature|showing|playing|opening|"
    r"score|length|size)\b)", re.I)
NOT_A_DEFINITION_HEAD = frozenset("""a an the my your our his her their its this that these
those it i you we they he she there on in up out off about wrong going happening happened next
new best better missing too more most so all any some not just for to with from of at by under
over behind inside between near against than left coming showing playing occurring eating cooking
red one none something anything nothing everything someone anyone everyone two three four five
six seven eight nine ten half quarter third quarter percent percent cheapest easiest quickest
longest shortest biggest smallest largest worth nice easy good double triple eleven twelve thirteen fourteen fifteen sixteen seventeen
eighteen nineteen twenty thirty forty
fifty sixty seventy eighty ninety hundred thousand million""".split())

def _has_any(text, phrases):
    return any(phrase in text for phrase in phrases)


SMALL_TALK_WORDS = tuple(tuple(phrase.replace("'s", " is").replace("'", "").split())
                         for phrase in SMALL_TALK)
ADDRESS_WORDS = frozenset("""love hun hunny hon dear darling duck pet chuck sweetheart sweetie
    son sunshine mate mates friend friends guys folks""".split())
SMALL_TALK_LEFTOVER = frozenset("""
a an the for of in on out up there here it its is are was were be been am has
and or so but then now again today tonight tomorrow lately already still very really too
quite just all right well good fine bad ok okay not no thanks thank you thx ta cheers ty
u ya mate mates friend friends guys folks everybody everyone hope your way doing going
getting had have last this week month day morning evening night long busy how what about
with us we i around yet even ever only mostly to at by from much appreciated appreciate
my your our their both all two
""".split()) | ADDRESS_WORDS | frozenset(word for greeting in GREETINGS for word in greeting.split())


def small_talk_only(norm):
    if not norm or len(norm) > 10:
        return False
    for phrase in SMALL_TALK_WORDS:
        size = len(phrase)
        for at in range(len(norm) - size + 1):
            if tuple(norm[at:at + size]) != phrase:
                continue
            rest = set(norm[:at]) | set(norm[at + size:])
            if not rest - SMALL_TALK_LEFTOVER:
                return True
    return False


CUE_FOLLOW = frozenset("""at with about of by from for in on into onto upon out up down off
away back over under than if as while since during after before until though although unless
around through toward towards even again too also just still yet ever never always sometimes
often usually mostly all any some every each both either neither most much more less least
enough quite pretty really very so that when because and but or now today yesterday tonight
this these those tbh tho atm rn lol haha innit actually
inside outside deep down lately
tomorrow honestly though still lately recently afterwards anyway here there one
i me my mine myself you your yours yourself he him his she her hers it its itself we us our
ours ourselves they them their theirs themselves who whom whose what why how where which
whether is are was were am be been being will would shall should can could may might must
have has had having do does did doing done dont didnt doesnt wont cant im ive ill id youre
theyre thats its gonna going gotta
to as please pls thanks thank cheers sorry sick stiff silly rotten
mate man bro dude guys folks everyone everybody buddy pal bud hon hun love sir madam team""".split())

PHRASE_OPENERS = frozenset("""the a an this that these those my your his her its our their some
any no every each another one""".split())
CLAUSE_VERBS = frozenset("""went got came said saw made took gave found lost left ran broke fell
kept met paid put sent sat stood thought told won wrote bought brought caught chose drove flew
forgot heard held hit knew ate drank slept woke bit spoke spent built burnt burned grew threw""".split())

CLAUSE_HELPERS = frozenset("""is are was were am be been being will would shall should can
could may might must have has had having do does did doing not never just still already yet""".split())
STATE_NOUNS = frozenset("""mood state spirits temper frame mind head shape form headspace
mindset humour humor moodstate""".split())
STATE_TAIL = re.compile(r"\b(?:in|of)\s+(?:a|an|such\s+a|a\s+right|a\s+real|a\s+proper|"
                        r"the|this|that)\s*$")

SPEAKER_TAIL = re.compile(r"\bi (?:am|was|feel|felt|have been|had been|do feel|did feel"
                          r"|am feeling|was feeling|been feeling|have been feeling"
                          r"|had been feeling)$"
                          r"|\bi(?: \w+){1,3} (?:feel|feeling|felt)$"
                          r"|\b(?:we|us) (?:are|were|feel|felt|have been|had been|do feel"
                          r"|did feel|are feeling|were feeling|been feeling)$"
                          r"|\bwe(?: \w+){1,3} (?:feel|feeling|felt)$"
                          r"|^were$")


def cue_about_person(text, cue):
    if cue in PARTICLE_STATES:
        for found in re.finditer(r"\b" + re.escape(cue) + r"\b", text):
            if _a_direction(text, found.start()):
                return False
    if cue.split()[-1] in CUE_FOLLOW:
        return bool(re.search(r"\b" + re.escape(cue) + r"\b", text))
    for match in re.finditer(r"\b" + re.escape(cue) + r"\b", text):
        if _a_verb_holds_it(text, match.start()):
            continue
        rest = text[match.end():].lstrip()
        if not rest or rest[0] in ".,!?;:-|":
            return True
        following = rest.split()[0].strip(".,!?;:-|")
        if not following or following.lower() in CUE_FOLLOW:
            return True
        if following[:1].isupper() and following.lower() not in lexicon.COMMON:
            return True
        if following.lower() in STATE_NOUNS and _state_before(text, match.start()):
            return True
        if following.lower() in PHRASE_OPENERS and _clause_follows(rest):
            return True
        if _speaker_before(text, match.start()) and _verb_after(rest):
            return True
    return False


ING_THINGS = frozenset("""morning evening ceiling building wedding pudding clothing shopping
    offering meeting parking lighting heating bedding flooring roofing fencing bedding
    thing something nothing anything everything king ring string spring wing sing bring swing
    going being doing having making taking coming""".split())

ING_TAKES_NO_OBJECT = frozenset("""
    act acting appear appearing arrive arriving become becoming come coming fall falling feel
    feeling get getting go going grow growing keep keeping lie lying live living look looking
    remain remaining rest resting rise rising run running seem seeming sit sitting sleep sleeping
    sound sounding stand standing stay staying turn turning wait waiting walk walking work
    working""".split())


def _a_verb_holds_it(text, at):
    words = [word.strip(".,!?;:-|\"'").lower() for word in text[:at].split()]
    if not words:
        return False
    last = words[-1]
    return (last.endswith("ing") and last not in FEELING_CUES_BEFORE
            and last not in ING_THINGS and last not in ING_TAKES_NO_OBJECT)


def _state_before(text, at):
    words = [word.strip(".,!?;:-|\"'").lower() for word in text[:at].split()]
    return bool(STATE_TAIL.search(" ".join(words[-4:])))


def _speaker_before(text, at):
    words = [word.strip(".,!?;:-|\"'").lower() for word in text[:at].split()]
    while words and words[-1] in FEELING_FILLER:
        words.pop()
    tail = " ".join(words[-5:])
    tail = re.sub(r"\bi'?m\b", "i am", tail)
    tail = re.sub(r"\bi'?ve\b", "i have", tail)
    if SPEAKER_TAIL.search(tail):
        return True
    recent = words[-4:]
    if "my" in recent:
        for word in recent[recent.index("my") + 1:]:
            if word in MOOD_NOUNS:
                return True
    return False


def _verb_after(rest):
    words = [word.strip(".,!?;:-|\"'").lower() for word in rest.split()[:5]]
    for word in words:
        if word in CLAUSE_HELPERS or word in CLAUSE_VERBS:
            return True
        if len(word) > 3 and word.endswith(("ed", "ing")):
            return True
    return False


def _clause_follows(rest):
    words = [word.strip(".,!?;:-|'\"") for word in rest.split()]
    end = len(words)
    for i, word in enumerate(words):
        if word and word[-1] in ".,!?;:-|":
            end = i + 1
            break
    clause = [word.lower() for word in words[:min(end, 8)] if word]
    if not clause:
        return False
    for word in clause[1:]:
        if word in CUE_FOLLOW or word in CLAUSE_VERBS or word.endswith("ed"):
            return True
    return False


BODY_SUBJECT = frozenset("""stomach tummy gut belly back leg legs arm arms head throat chest skin
eye eyes ear ears tooth teeth stomachs""".split())


def _a_body_part_before(text, cue):
    for match in re.finditer(r"\b" + re.escape(cue) + r"\b", text):
        before = [word.strip(".,!?;:-|\"'").lower() for word in text[:match.start()].split()]
        before = [word for word in before if word not in FEELING_FILLER and word != "is"]
        if before and before[-1] in BODY_SUBJECT:
            return True
    return False


STATE_JOINERS = frozenset("""am is are was were be been being feel feels feeling felt still
really very so too pretty quite a bit little just now also always lately today tonight""".split())


OBJECT_MARKERS = frozenset("""the a an my your his her their our this that these those
another every some any no""".split())
TIME_MARKERS = frozenset("this that these those every each".split())
TAIL_STOPS = frozenset("""after before since until when if and but so because though while
than then too also still now today tonight lately recently honestly about at in on of for to
with by from as like""".split())


def _takes_an_object(text, end):
    words = [word.strip(".,!?;:-|\"'").lower() for word in text[end:].split()]
    for pos, word in enumerate(words):
        if not word or word in TAIL_STOPS:
            return False
        if word in OBJECT_MARKERS:
            after = words[pos + 1:pos + 2]
            if word in TIME_MARKERS and after and after[0] in TIME_FILLERS:
                return False
            return True
    return False


def _object_after(text, cue):
    return any(_takes_an_object(text, match.end())
               for match in re.finditer(r"\b" + re.escape(cue) + r"\b", text))


def _state_cue(cue):
    if cue in SELF_ONLY_STATE:
        return cue
    head = cue.split()[0]
    return head if head in SELF_ONLY_STATE else None


VERB_ONLY_STATE = frozenset("pooped".split())
COPULA_BEFORE = frozenset("""im am is are was were be been being feel feels felt feeling
get gets got gettin look looks looked seem seems seemed sound sounds sounded""".split())


def _a_copula_before(text, start):
    words = [word.strip(".,!?;:-|\"'").lower() for word in text[:start].split()]
    while words and (words[-1] in FEELING_FILLER or words[-1] in ("both", "all")):
        words.pop()
    return bool(words) and words[-1] in COPULA_BEFORE


def _state_of_a_person(text, cue):
    for match in re.finditer(r"\b" + re.escape(cue) + r"\b", text):
        if cue in SUPPLY_WORDS and _about_a_supply(text, match.end()):
            continue
        if cue in VERB_ONLY_STATE and not _a_copula_before(text, match.start()):
            continue
        if _takes_an_object(text, match.end()):
            continue
        words = [word.strip(".,!?;:-|\"'").lower() for word in text[:match.start()].split()]
        while words and (words[-1] in STATE_JOINERS or words[-1] in FEELING_FILLER):
            words.pop()
        if not words:
            return True
        subject = words[-1]
        if subject in PERSON_SUBJECT or subject in OTHER_PEOPLE:
            return True
        if subject in MOOD_NOUNS and "my" in words[:-1][-3:]:
            return True
        if _speaker_before(text, match.start()):
            return True
        return False
    return False


def _said_of_the_speaker(text, cue):
    for match in re.finditer(r"\b" + re.escape(cue) + r"\b", text):
        if _speaker_before(text, match.start()):
            return True
    return False


ABILITY_AT = re.compile(r"\b(?:bad|crap|rubbish|rough|useless|hopeless|terrible|awful|lousy|"
                        r"poor|worse|worst)\s+(?:at|with)\b")


EPISODE_NOUNS = frozenset("attack attacks episode episodes spell spells".split())


def _names_an_episode(text, cue):
    for match in re.finditer(r"\b" + re.escape(cue) + r"\b\s+(\w+)", text):
        if match.group(1).lower() in EPISODE_NOUNS:
            return True
    return False


STATE_AS_FEELING = frozenset(("down",))
FEELING_NOT_MOOD = frozenset("""for to on at""".split())
FEELING_FILLER = frozenset("""a an bit little lot kind kinda sort so too very really quite pretty
    just still always again now today totally honestly also either all more most less as
    enough well""".split())
FEELING_COPULA = frozenset("""am is are was were be been being feel feels feeling felt get gets
    getting got seem seems seemed look looks looking sound sounds sounded""".split())
FEELING_CUES_BEFORE = FEELING_COPULA | frozenset("feel feels feeling felt".split())


def a_broken_heart_shape(text):
    low = " ".join(str(text or "").lower().replace("\u2019", "'").split())
    return bool(HEART_IN_A_STATE.search(low) or BROKEN_HEARTED.search(low)
                or BROKE_A_HEART.search(low) or A_BROKEN_HEART.search(low))


NOT_THEIR_OWN = frozenset("""her his their your mum mom mother dad father son daughter husband
    wife partner friend sister brother child kid boss neighbour neighbour's nan gran""".split())

A_PERSON_ELSE = frozenset("""mum mom mother dad father son daughter husband wife partner
    friend sister brother child kid boss neighbour nan gran""".split())
A_PERSON_IS_THE_SUBJECT = re.compile(r"^(?:he|she|they|him|them)\b")
A_POSSESSED_HEART = re.compile(r"\b(?:my|our|her|his|their|your|the|a|an)\s+(?:\w+'?s\s+)?hearts?\b")


def _somebody_elses_heart(text):
    low = " ".join(str(text or "").lower().replace("\u2019", "'").split())
    if not a_broken_heart_shape(low) or _a_broken_heart_is_theirs(low):
        return False
    if A_POSSESSED_HEART.search(low):
        return False
    if A_PERSON_IS_THE_SUBJECT.match(low):
        return True
    words = low.split()
    if len(words) > 1 and words[0] in ("my", "our", "the"):
        person = words[1].strip(".,!?'\"")
        if person in A_PERSON_ELSE or person[:-1] in A_PERSON_ELSE:
            if words[2:3] in (["heart"], ["hearts"]):
                return False
            return True
    return False


HAVE_A_BROKEN_HEART = re.compile(r"\b(?:i have|i've got|ive got|i got|i had)\b[^.]{0,24}broken heart")


def _a_broken_heart_is_theirs(text):
    low = " ".join(str(text or "").lower().replace("\u2019", "'").split())
    if not a_broken_heart_shape(low):
        return False
    words = low.split()
    starts = [match.start() for match in
              (re.search(r"\bhearts?\b", low), re.search(r"\bbroken\b", low)) if match]
    at = len(low[:min(starts)].split()) if starts else 0
    window = words[max(0, at - 2):at]
    owner = window[-1] if window else ""
    if HAVE_A_BROKEN_HEART.search(low):
        return True
    if BROKE_A_HEART.search(low):
        return False
    if owner in NOT_THEIR_OWN or owner.endswith("'s") or (
            owner.endswith("s") and owner not in ("is", "was", "this", "its", "us")):
        return False
    if any(word in ("my", "our") for word in window):
        return True
    if owner in ("a", "an", "the"):
        return False
    return not re.search(r"\b(?:her|his|their|your)\b", low) \
        and bool(re.match(r"^(?:i|im|i'm|ive|i've|we|we're|weve|we've|our)\b", low))

HEDGED_LOW = frozenset((
    "could be better", "could be better i suppose", "been better", "not so good", "not too good",
    "not so great", "not that good", "not that great", "so so"))
HEDGED_DOUBT = ("i suppose", "suppose", "i guess", "guess", "ig", "i spose", "s'pose", "i gues")
HEDGED_OK = frozenset((
    "ok", "okay", "fine", "alright", "all right", "good", "well", "grand", "not too shabby"))
HEDGED_WRAPPER = frozenset("""
    im i am well yeh yeah yep oh ah eh hmm hm its it it's is honestly to be totally quite
    thanks thank you ta tbh tbf lol ig i guess suppose today love mate and you you
    honest really sure actually kinda sorta atm currently now very pretty
""".split())


def _a_hedged_low(text):
    words = [word.strip(".,!?;:-'\"|") for word in str(text or "").lower().split()]
    words = [word for word in words if word]
    doubted = False
    for phrase in HEDGED_DOUBT:
        count = len(phrase.split())
        if len(words) > count and " ".join(words[-count:]) == phrase:
            words = words[:-count]
            doubted = True
            break
    while words and words[0] in HEDGED_WRAPPER:
        words.pop(0)
    while words and words[-1] in HEDGED_WRAPPER:
        words.pop()
    answer = " ".join(words)
    return answer in HEDGED_LOW or (doubted and answer in HEDGED_OK)


def _copula_just_before(words, pos):
    for word in reversed(words[:pos]):
        if word in FEELING_FILLER:
            continue
        return word in FEELING_COPULA
    return False


def _state_as_feeling(text):
    words = [word.strip(".,!?;:-|\"'") for word in text.lower().split()]
    for pos, word in enumerate(words):
        if word not in STATE_AS_FEELING:
            continue
        if _thing_turned_down(words, pos):
            continue
        if not _copula_just_before(words, pos):
            continue
        if _particle_is_a_place(words, pos):
            continue
        after = words[pos + 1] if pos + 1 < len(words) else ""
        if after in FEELING_NOT_MOOD:
            continue
        if _whose_state(words, pos) in ("self", "other"):
            return True
    return False


WORK_ON_ME = {
    "stresses": "anxious", "stressing": "anxious", "strains": "anxious",
    "straining": "anxious", "worries": "anxious", "worrying": "anxious", "worried": "anxious",
    "frets": "anxious", "fretting": "anxious",
    "drains": "tired", "draining": "tired", "drained": "tired",
    "tires": "tired", "tiring": "tired", "exhausts": "tired", "exhausting": "tired",
    "exhausted": "tired", "wears": "tired", "wearing": "tired", "wore": "tired",
    "worn": "tired",
    "annoys": "angry", "annoying": "angry", "annoyed": "angry",
    "irritates": "angry", "irritating": "angry", "irritated": "angry",
    "frustrates": "angry", "frustrating": "angry", "frustrated": "angry",
    "bugs": "angry", "bugging": "angry", "bugged": "angry",
    "bothers": "angry", "bothering": "angry", "bothered": "angry",
    "winds": "angry", "winding": "angry",
    "upsets": "sad", "upsetting": "sad", "depresses": "sad", "depressing": "sad",
    "depressed": "sad",
    "scares": "anxious", "scaring": "anxious", "scared": "anxious",
    "frightens": "anxious", "frightening": "anxious", "frightened": "anxious",
    "confuses": "confused", "confusing": "confused", "confused": "confused",
}
ACT_ON_FILLER = frozenset("""so right really totally absolutely just always still all quite""".split())
PARTS_OF_ME = BODY_SUBJECT | frozenset("""knee knees shoulder shoulders hip hips neck ankle
    ankles wrist wrists hand hands finger fingers toe toes elbow elbows foot feet jaw tooth
    teeth sinuses earache toothache headache migraine backache""".split())
ACT_ON_LEAD = frozenset("""am is are was were be been being keep keeps kept get gets got
    always every still just really totally so very all quite sometimes often daily""".split())


def _works_on_the_speaker(text):
    words = [word.strip(".,!?;:-|\"'()").lower() for word in str(text or "").split()]
    for pos, word in enumerate(words):
        feeling = WORK_ON_ME.get(word)
        if not feeling:
            continue
        lead = None
        for back in range(pos - 1, max(pos - 4, -1), -1):
            if words[back] in ACT_ON_FILLER or words[back] in ACT_ON_LEAD:
                continue
            lead = words[back]
            break
        if lead in ("i", "i'm", "im", "me", "my", "myself", "we", "our"):
            continue
        named = [word for word in words[max(pos - 4, 0):pos] if word not in ACT_ON_FILLER]
        if any(word in PARTS_OF_ME for word in named):
            continue
        if lead and (lead.endswith("nt") or lead in ("not", "never", "no")):
            continue
        acted_on = None
        for ahead in range(pos + 1, min(pos + 4, len(words))):
            if words[ahead] in ACT_ON_FILLER:
                continue
            acted_on = words[ahead]
            break
        if acted_on not in ("me", "us"):
            continue
        return feeling
    return None


def _skeleton(word):
    return "".join(letter for letter in word.lower()
                   if letter.isalpha() and letter not in "aeiouy")


_SOUND_CUES = None


def _sound_cues():
    global _SOUND_CUES
    if _SOUND_CUES is None:
        index = {}
        known = set()
        for name, cues in EMOTION_WORDS.items():
            for cue in cues:
                if " " in cue:
                    continue
                known.add(cue)
                if len(cue) < 4:
                    continue
                index.setdefault(_skeleton(cue), {}).setdefault(name, []).append(cue)
        _SOUND_CUES = (index, known)
    return _SOUND_CUES


def feeling_by_sound(word):
    if not isinstance(word, str):
        return None
    low = word.strip().strip(".,!?;:'\"()").lower()
    if len(low) < 4 or not low.isalpha():
        return None
    index, known = _sound_cues()
    if low in known:
        return None
    if low in lexicon.COMMON_NAMES:
        return None
    matches = index.get(_skeleton(low)) or {}
    found = sorted({name for name, cues in matches.items()
                    if any(cue[:1] == low[:1] for cue in cues)})
    return found[0] if len(found) == 1 else None


FEELING_SOUND_FRAME = re.compile(r"\b(?:im|i am|i feel|i felt)\s+(?!not\b|never\b|no\b)"
                                 r"(?:(?:so|really|very|totally|proper|dead|well|quite|pretty|"
                                 r"slightly|kinda|kind of|a bit|a little|a tad)\s+)*"
                                 r"([a-z]{4,})\b")


SOUND_FOLLOWS = frozenset("""of at in with about over by again today tonight now already too
    as anymore stiff out""".split())


def _a_feeling_can_end_here(text, end):
    rest = text[end:].lstrip()
    if not rest or rest[0] in ".,!?;:":
        return True
    return rest.split()[0].strip(".,!?;:'\"") in SOUND_FOLLOWS


def _feeling_said_as_a_sound(text):
    for match in FEELING_SOUND_FRAME.finditer(text):
        if _takes_an_object(text, match.end()):
            continue
        if not _a_feeling_can_end_here(text, match.end()):
            continue
        name = feeling_by_sound(match.group(1))
        if name:
            return name
    return None


def _a_period_of_their_own(text, cue):
    for match in re.finditer(r"\b" + re.escape(cue) + r"\b", text):
        after = [word.strip(".,!?;:-|\"'").lower() for word in text[match.end():].split()]
        seen = 0
        while after and seen < 3 and after[0] in OWN_PERIOD_FILLER:
            after.pop(0)
            seen += 1
        if not after or after[0] not in OWN_PERIOD_NOUNS:
            continue
        before = [word.strip(".,!?;:-|\"'()").lower() for word in text[:match.start()].split()]
        for word in reversed(before[-OWN_PERIOD_REACH:]):
            if word in OWN_PERIOD_STOPS:
                break
            if word in OWN_PERIOD_HEADS:
                return True
    return False


ACTS_ON_THE_SPEAKER = (
    (r"(?:stress|stresses|stressing|overwhelm|overwhelms|overwhelming|worry|worries|worrying|"
     r"panic|panics|panicking)\s+(?:me\b|my head\b)", "anxious"),
    (r"(?:wear|wears|wearing|wore|tire|tires|tiring|exhaust|exhausts|exhausting|drain|drains|"
     r"draining|kill|kills|killing|knacker|knackers|knackering)\s+me\b", "tired"),
    (r"(?:get|gets|getting|got|bring|brings|bringing|brought)\s+me\s+(?:down|low)\b", "sad"),
    (r"(?:do|does|doing|done)\s+my\s+(?:head|brain|nut|swede)\s+in\b", "anxious"),
    (r"(?:drive|drives|driving|drove)\s+me\s+(?:mad|crazy|nuts|mental|insane|"
     r"up the wall|round the bend|round the twist)\b", "angry"),
    (r"(?:annoy|annoys|annoying|irritate|irritates|irritating|frustrate|frustrates|frustrating|"
     r"bug|bugs|bugging|wind|winds|winding)\s+me\s+up\b", "angry"),
)
LAUGH_AT_THE_END = re.compile(r"\b(?:lol|lmao|haha|hah|heh|jk|joking|kidding|honestly)\b[\s.!?]*$")
A_BODY_SUBJECT = frozenset(
    "back neck knee knees feet foot leg legs arm arms hand hands shoulder shoulders hip hips "
    "ankle ankles wrist wrists elbow elbows joint joints muscle muscles tooth teeth jaw ear ears "
    "eye eyes head stomach chest ribs rib side spine sciatica period periods boob boobs tit tits "
    "throat shoulder-blade".split())


def _acts_on_the_speaker(text):
    if LAUGH_AT_THE_END.search(text):
        return None
    for pattern, name in ACTS_ON_THE_SPEAKER:
        for match in re.finditer(r"\b(?:" + pattern + ")", text):
            before = text[:match.start()].split()[-2:]
            if any(word.strip(".,!?;:'\"") in A_BODY_SUBJECT for word in before):
                continue
            return name
    return None
GETTING_WORSE = re.compile(r"\b(i'?m|i am)\s+getting\s+(worse)\b", re.I)
NO_BETTER = re.compile(r"\bno\s+better\b", re.I)
BETTER_OFF = re.compile(r"\b(?:no\s+)?better\s+off\b|\bworse\s+off\b", re.I)
GOOD_WORD_MISSING = re.compile(
    r"\b(?:cant|can\s*not|couldnt|could\s*not|dont|do\s*not|didnt|did\s*not|havent|have\s*not|"
    r"hasnt|has\s*not|hadnt|had\s*not|never|not)\b[^.?!;]{0,40}?"
    r"\b(?:remember|remembered|felt|feel|feeling|been|be|was|were)\b", re.I)
GOOD_WORD_COMPARED = re.compile(
    r"\b(?:this|so|that|as)\s+(?:happy|glad|pleased|excited|proud|relieved|good|great|well|"
    r"content|calm|fine)\b", re.I)
GOOD_WORD_BY_COMPARISON = re.compile(r"\b(?:better|best)\b", re.I)


def emotion_of(text):
    text = BETTER_OFF.sub(" ", text)
    text = NO_BETTER.sub("worse", text)
    text = GETTING_WORSE.sub(lambda match: match.group(1) + " worse", text)
    text = IDIOM_STATES.sub(" ", text)
    text = ABILITY_AT.sub(" ", text)
    for name, cues in EMOTION_WORDS.items():
        for cue in cues:
            state = _state_cue(cue)
            if state and not _state_of_a_person(text, state):
                continue
            if cue in BODY_STATE_CUES:
                if _a_body_part_before(text, cue) or _object_after(text, cue):
                    continue
            idiom = NOT_A_MOOD_THERE.get(cue)
            if idiom is not None and idiom.search(text):
                continue
            if cue in LABEL_ON_A_PERSON and _said_of_the_speaker(text, cue):
                continue
            if (cue in SELF_ONLY_CUES or cue in ALWAYS_SELF_ONLY or cue in THING_OR_PERSON_CUES
                    or cue in CONFUSED_SELF_ONLY
                    or cue in A_COMPARISON) and not _said_of_the_speaker(text, cue):
                continue
            if cue in THING_OR_PERSON_CUES and _laughed_off(text, cue):
                continue
            if (cue in PERIOD_CUES and A_PERIOD.search(text)
                    and not A_LIMIT_ABOUT_PEOPLE.search(text)
                    and (A_MONTH_PERIOD.search(text) or A_MONEY_SUBJECT.search(text))):
                continue
            if cue in SAID_AS_A_NEGATION and not denied(text, cue):
                continue
            if name not in GOOD_EMOTION_NAMES and cue not in SAID_AS_A_NEGATION and denied(text, cue):
                continue
            if (name in GOOD_EMOTION_NAMES and GOOD_WORD_MISSING.search(text)
                    and not GOOD_WORD_COMPARED.search(text)
                    and not GOOD_WORD_BY_COMPARISON.search(text)):
                return "sad"
            if cue_about_person(text, cue) or _names_an_episode(text, cue):
                return name
    acted = _acts_on_the_speaker(text)
    if acted:
        return acted
    if a_broken_heart_shape(text):
        return "sad"
    sounded = _feeling_said_as_a_sound(text)
    if sounded:
        return sounded
    worked_on = _works_on_the_speaker(text)
    if worked_on:
        return worked_on
    if _state_as_feeling(text):
        return "sad"
    for name, cues in EMOTION_WORDS.items():
        if name in GOOD_EMOTION_NAMES:
            continue
        for cue in cues:
            if cue in NOT_THE_SPEAKERS_DAY or cue in PERIOD_CUES:
                continue
            if denied(text, cue):
                continue
            if _a_period_of_their_own(text, cue):
                return name
    return None


REFERRING = frozenset("about for with to in on".split())
POINTED_AT = frozenset("this that these those it them".split())


def _capability_question(norm):
    compact = [word for word in norm if word not in CAPABILITY_FILLER]
    for phrase in CAPABILITY:
        wanted = phrase.split()
        for start in range(len(compact) - len(wanted) + 1):
            if compact[start:start + len(wanted)] != wanted:
                continue
            tail = compact[start + len(wanted):]
            rest = [word for word in tail if word not in CAPABILITY_CARRIER]
            if rest:
                return False
            if any(word in REFERRING and i + 1 < len(tail) and tail[i + 1] in POINTED_AT
                   for i, word in enumerate(tail)):
                return False
            return True
    return False


ME_ASKS = ("what do you think of me", "what do you think about me", "what do you reckon of me",
           "what do you make of me", "do you like me", "do you love me", "do you care about me",
           "are you my friend", "are we friends", "am i your friend", "do you miss me",
           "would you miss me", "will you miss me", "do you hate me", "am i annoying you",
           "do you think about me", "do you think of me", "do you ever think about me",
           "are you annoyed with me", "do you like talking to me", "do you enjoy talking to me",
           "do you like chatting to me", "do you like me talking to you")
ME_TAIL = ("then", "though", "tho", "now", "honestly", "really", "lol", "haha",
           "tbh", "tbf", "ngl", "anyway", "still",
           "far", "so", "all", "at")
ME_LEAD = ("so", "ok", "okay", "oh", "yeah", "but", "well", "and", "honestly")


def _asks_how_the_bot_sees_me(norm):
    words = list(norm)
    changed = True
    while changed and words:
        changed = False
        for phrase in MOOD_TAIL:
            size = len(phrase.split())
            if size < len(words) and words[-size:] == phrase.split():
                del words[-size:]
                changed = True
        while words and words[0] in ME_LEAD:
            words.pop(0)
            changed = True
        while words and words[-1] in ME_TAIL:
            words.pop()
            changed = True
    ask = words[:-1] + ["me"] if words and words[-1] == "my" else words
    return " ".join(words) in ME_ASKS or " ".join(ask) in ME_ASKS


WHO_TALKING = frozenset("""talk talking speak speaking chat chatting message messaging
    text texting""".split())
WHO_A_THING = frozenset("""bot robot chatbot ai machine computer program human person""".split())
WHO_TAIL = frozenset("then please pls anyway again".split())


def _asks_who_this_is(norm):
    words = tuple(norm)
    while words and words[-1] in WHO_TAIL:
        words = words[:-1]
    if words in (("who", "is", "this"), ("who", "am", "i", "talking", "to"),
                 ("who", "am", "i", "speaking", "to"), ("who", "am", "i", "speaking", "with"),
                 ("who", "am", "i", "chatting", "to"), ("who", "am", "i", "chatting", "with"),
                 ("who", "am", "i", "talking", "with"), ("who", "was", "i", "talking", "to"),
                 ("who", "was", "i", "speaking", "to"), ("who", "was", "i", "speaking", "with")):
        return True
    if words[:4] == ("who", "have", "i", "been") and len(words) in (6, 7):
        return words[4] in WHO_TALKING and words[5] in ("to", "with")
    if words[:3] in (("who", "did", "i"), ("who", "was", "i"), ("who", "am", "i")) \
            and len(words) in (5, 6):
        if len(words) == 6 and words[3] != "just":
            return False
        at = 1 if len(words) == 6 else 0
        return words[3 + at] in WHO_TALKING and words[4 + at] in ("to", "with")
    if words[:3] in (("am", "i", "talking"), ("am", "i", "speaking"), ("am", "i", "chatting")):
        if len(words) == 5 and words[3] in ("to", "with"):
            return words[4] in WHO_A_THING or words[4] in ("a", "an")
        if len(words) == 6 and words[3] in ("to", "with") and words[4] in ("a", "an"):
            return words[5] in WHO_A_THING
    if words[:2] in (("is", "this"), ("is", "it")) and len(words) in (3, 4, 5):
        rest = words[2:]
        if rest and rest[0] in ("a", "an"):
            rest = rest[1:]
        if rest and rest[0] == "real":
            rest = rest[1:]
        return bool(rest) and all(word in WHO_A_THING for word in rest)
    return False


WHERE_BOT_TAIL = frozenset("""from based located at out of exactly then now though really actually
    please pls mate live living staying originally today currently""".split())


def _asks_where_the_bot_is(norm):
    words = tuple(norm)
    if not words or words[0] not in ("where", "whereabouts"):
        return False
    rest = words[1:]
    if rest[:2] == ("are", "you"):
        rest = rest[2:]
    elif rest[:2] == ("do", "you") and rest[2:3] == ("live",):
        rest = rest[3:]
    elif rest[:2] == ("you", "live"):
        rest = rest[2:]
    else:
        return False
    return all(word in WHERE_BOT_TAIL for word in rest)
ANSWERING_A_QUOTED_ASK = re.compile(
    r"\b(?:how\s+(?:do|should|would|can|might|to)\s*(?:i|you|we)?|how\s+to|"
    r"what\s+(?:do|should)\s*(?:i|you|we)?)\s*[^.?!]{0,20}?"
    r"\b(?:answer|say|reply|respond)\b[^.?!]{0,40}?"
    r"\b(?:what|who|where|why|how|when|tell\s+me|do\s+you|are\s+you|can\s+you|your)\b",
    re.IGNORECASE)


WHILE_ASK = re.compile(
    r"\bhow\s+long\s+(?:can|could|may|might|will|would|do|does)\s+(?:we|i|you|u|this)\s+"
    r"(?:[a-z]+\s+){0,2}?(?:talk|chat|keep\s+(?:going|talking|chatting)|carry\s+on|go\s+on)\b"
    r"|\bhow\s+long\s+(?:have|has|do|does|did)\s+(?:you|u)\s+(?:got|have)\b"
    r"(?=\s*(?:$|[.!?]|for\s+(?:you|me|us|now|today)\b|on\s+you\b|today\b|now\b|then\b"
    r"|and\b|so\b|to\s+(?:talk|chat|keep\s+going|carry\s+on|go\s+on)\b)"
    r"|\s+left\s*[.!?]?$)"
    r"|\bhow\s+long\s+(?:are|will)\s+(?:you|u)\s+(?:be\s+)?(?:here|around|on)\b"
    r"|\bhave\s+(?:you|u)\s+got\s+(?:all\s+day|time|much\s+time)\b"
    r"|\b(?:can|could|shall|should|may)\s+we\s+keep\s+(?:talking|going|chatting|on)\b"
    r"|\bdo\s+(?:you|u)\s+mind\s+if\s+i\s+(?:keep|carry|ramble)\b"
    r"|\bhow\s+much\s+time\s+(?:have|has|do)\s+(?:you|u|we)\s+(?:got|have)\b"
    r"|\bhow\s+many\s+(?:messages?|questions?|things)\s+can\s+i\s+(?:send|ask|give)\b"
    r"|\blimit\s+(?:on|to)\s+how\s+long\b[\s\S]{0,24}?\b(?:talk|chat|go\s+on|carry\s+on|"
    r"keep\s+going)\b")


KEEPING_ASK = re.compile(
    r"\bam i\s+(?:boring\s+(?:you|u)\b|keeping\s+(?:you|u)\b|a\s+bore\b|boring\b"
    r"|(?:talking|talk|going\s+on|rambling|wittering|waffling|droning)\s+too\s+much\b"
    r"|going\s+on(?:\s+(?:a\s+bit|and\s+on|too\s+long|like\s+this))?(?:\s*[.!?]\s*$|\s*$)"
    r"|rambling\b|wittering\b"
    r"|waffling\b|droning\s+on\b|wasting\s+(?:your|ur)\s+time\b)"
    r"|\bis\s+(?:this|it)\s+(?:boring\s+(?:you|u)\b|boring\b|dull\b|too\s+much\s+detail\b"
    r"|going\s+on\s+a\s+bit\b)"
    r"|\bdo i\s+(?:talk|go\s+on|ramble|witter|waffle)\s+too\s+much\b"
    r"|\bare (?:you|u)\s+(?:bored\s+(?:of|with)\s+(?:me|us|this|it)\b"
    r"|sick\s+of\s+me\b|fed\s+up\s+(?:of|with)\s+me\b|had\s+enough\s+of\s+me\b)"
    r"|\bdo you\s+mind\s+(?:me|my)\s+(?:going\s+on|talking|rambling|wittering)\b"
    r"|\b(?:am i|are we|was i)\s+wasting\s+(?:your|ur)\s+time\b")


STOP_ASK = re.compile(
    r"(?:(?:do|would)\s+(?:you|u)\s+want\s+me\s+to"
    r"|(?:do|would)\s+(?:you|u)\s+like\s+me\s+to"
    r"|(?:shall|should)\s+i"
    r"|(?:can|could)\s+i)\s+"
    r"(?:stop|quit|shut\s+up|leave\s+it)(?:\s+(?:now|then|talking|chatting|going\s+on))?"
    r"|(?:do|would)\s+(?:you|u)\s+(?:want|like)\s+me\s+to\s+go(?:\s+now)?")
STOP_ASK_FILLER = frozenset("""so and but ok okay well now then sorry hmm erm um oh ah hey hi
right alright just also btw honestly""".split())


def a_stop_ask(line):
    words = [word for word in str(line or "").lower().replace(",", " ").split()
             if word not in ("", " ")]
    while words and words[0].strip(".,!?") in STOP_ASK_FILLER:
        words.pop(0)
    return bool(STOP_ASK.fullmatch(" ".join(words).strip(" .!?")))


def _about_bot_kind(text, words, norm=()):
    bare = " " + text.strip() + " "
    flat = (text or "").replace(" | ", " ").replace("|", " ")
    if WHILE_ASK.search(flat):
        return "while"
    if KEEPING_ASK.search(flat) or a_stop_ask(flat):
        return "keeping"
    if _asks_where_the_bot_is(norm):
        return "where"
    if _asks_who_this_is(norm):
        return "identity"
    if ANSWERING_A_QUOTED_ASK.search(text or "") and not _self_ask(norm):
        return None
    if _asks_how_the_bot_sees_me(norm):
        return "warmth"
    if "remember" in words and {"you", "your"} & words:
        return "memory"
    if _capability_question(list(norm)):
        return "help"
    if _asks_if_the_bot_is_a_product(norm):
        return "model"
    if _recalls_their_own_line(norm):
        return None
    if _asks_what_is_new_with_the_bot(norm):
        return "doings"
    if _asks_what_the_bot_has_been_doing(norm):
        return "doings"
    if _asks_whether_the_bot_is_about(norm):
        return "doings"
    if _asks_how_it_spends_its_time(norm):
        return "doings"
    if (_asks_what_the_bot_is_doing(norm) and {"you", "u", "ya"} & words
            and words & ASKS_IF_ANYTHING):
        return "doings"
    if _asks_about_its_experience(norm):
        return "doings"
    if _self_ask(norm):
        return "memory" if {"remember", "recall", "forget"} & words else "identity"
    if _how_long_itself(norm) or _when_itself(norm):
        return "memory"
    if _counts_its_own_doings(norm):
        return "memory"
    if A_YOUR_KIN.search(" ".join(norm)) or A_YOUR_OWN_THING.search(" ".join(norm)):
        return "life"
    if (A_HOW_MANY_OF_THE_BOTS_OWN.search(" ".join(norm))
            and set(norm) & BOT_LIFE):
        return "life"
    if A_WHAT_ITS_LIKE.search(" ".join(norm)):
        return "identity"
    if _asks_about_its_own_life(norm):
        return "life"
    if _has_any(bare, ABOUT_BOT) or text.strip().endswith(ABOUT_BOT_END):
        return "identity"
    if {"you", "your"} & words and words & ROBOT_WORDS and "are" in words:
        return "identity"
    return None


STATE_WORDS = frozenset("""
low down rough tough hard heavy flat empty rubbish crap awful terrible horrible grim bad good
fine better worse ok okay upset sad miserable unhappy disappointed gutted stressed anxious
worried nervous scared frightened angry annoyed furious irritated frustrated bored tired
exhausted knackered shattered drained wiped sleepy swamped overwhelmed snowed fed unwell
poorly sick ill
mad cross fuming livid seething raging irate miffed peeved riled
""".split())
PERSON_NOUNS = frozenset("""
day days week weeks month months year years night nights morning mornings evening weekend
term shift shifts sleep time times life mood work job school college uni class classes exam
exams test deadline presentation interview head back leg legs arm arms hand hands shoulder
shoulders knee knees foot feet ankle ankles neck chest stomach tummy hip hips throat eye eyes
ear ears tooth teeth skin hair voice nerves body health
""".split())
OTHER_PEOPLE = frozenset("""
he she they him her them his hers their mum mom dad mother father son daughter kid kids baby
babies toddler toddlers child children infant newborn boy boys girl girls teenager teen lad
partner husband wife boyfriend girlfriend friend friends brother sister family colleague boss
neighbour neighbor uncle aunt cousin gran grandma grandad grandpa nan nana mate mates
dog dogs puppy pup cat cats kitten doggy hamster rabbit rabbits guinea budgie parrot pet pets
""".split())
MOOD_NOUNS = frozenset("""anxiety stress worry worries nerves mood depression grief sadness
anger panic fear energy confidence motivation appetite sleep loneliness doubt
head brain mind memory concentration focus""".split())
PERSON_SUBJECT = frozenset("i im me us we myself ourselves nobody nothing everything things".split())
BEFORE_STATE = frozenset("""
am is are was were be been being have has had having do does did feel feels feeling felt get
gets getting got seem seems seemed look looks looked sound sounds sounded taste tastes tasted
a an the so very really quite pretty too bit little lot kind kinda touch just still always again now
 today honestly totally all as than and but then of at with about over on in for from by my your
our their his its am i am not no never still even both either
will would shall should can could may might must wont cant cannot couldnt shouldnt wouldnt
ok okay right well cool sure yeah yep yes alright oh ah hmm hey hi so
""".split()) - {"i"}
PERSON_PREPOSITIONS = frozenset("of with about in at on".split())
CONJUNCTIONS = frozenset("since because when while until though although if after before "
                         "whenever and but or yet".split())
BETWEEN_STATE_AND_NOUN = frozenset("""
a an the bit little lot of kind kinda up down out off on at with about over in for from by my
your our their his its so very really quite pretty too just still always again now today
honestly totally all as than
""".split())

TIME_FILLERS = frozenset("""
morning afternoon evening night tonight noon midnight week weekend month year lately recently
afterwards afterward yesterday tomorrow nowadays midweek
""".split())

MOOD_TAIL = ("to be honest", "if i am honest", "if im honest", "to be fair", "to tell the truth",
             "to be truthful", "to be blunt", "if anything", "i must say", "i suppose", "i guess")
MOOD_TAIL_WORDS = frozenset("tbh tbf ngl honestly though tho".split())
MOOD_TAIL_TAKEN = frozenset("""going go goes went want wants wanted need needs needed try tries
    trying tried mean means meant promise promised learn learned learnt used rather hope hoping
    hate hates love loves have has had like likes prefer plan planning""".split())


def _without_mood_tail(clause):
    words = list(clause)
    changed = True
    while changed and words:
        changed = False
        if words[-1] in MOOD_TAIL_WORDS:
            words.pop()
            changed = True
            continue
        for phrase in MOOD_TAIL:
            size = len(phrase.split())
            if size >= len(words) or words[-size:] != phrase.split():
                continue
            if words[-size - 1] in MOOD_TAIL_TAKEN:
                continue
            del words[-size:]
            changed = True
            break
    return words


def _last_subject_pos(words):
    for pos in range(len(words) - 1, -1, -1):
        word = words[pos]
        if word in BEFORE_STATE:
            continue
        if len(word) > 4 and (word.endswith("ly") or word.endswith("ing")):
            continue
        if word.replace(".", "").isdigit() or word in NUMBER_WORDS:
            continue
        return pos
    return None


def _last_subject(words):
    pos = _last_subject_pos(words)
    return None if pos is None else words[pos]


PARTICLE_STATES = frozenset("down up out off in on".split())
COPULA_STATES = frozenset("ill".split())
NOUN_STATES = frozenset("flat".split())
SUPPLY_WORDS = frozenset("low short".split())
SUPPLY_PREPOSITIONS = frozenset("on in of".split())
OWN_RESERVES = frozenset("""energy patience confidence motivation enthusiasm inspiration hope
    sleep focus concentration attention steam willpower batteries charge ideas""".split())
DEGREE = frozenset("""bit little lot kind sort very really so too pretty quite more most less
as enough""".split())
DETERMINERS = frozenset("the a an my your our their his her its this that these those it them".split())

MOTION_WORDS = frozenset("""go goes going went gone walk walks walking walked wander wandering
    head heads heading headed run runs running ran drive drives driving drove ride rides riding
    rode cycle cycles cycling cycled pop pops popping popped come comes coming came hurry hurries
    hurrying stumble stumbling jog jogs jogging climb climbing jump jumping fall falls falling
    fell race racing rush rushing dash dashing nip nipping shuffle shuffling off""".split())
TIME_AFTER_A_PARTICLE = frozenset("""week weeks month months year years morning mornings
    afternoon evenings evening night nights weekend weekends time times term terms day days
    while bit moment minute minutes hour hours""".split())


def _particle_is_a_place(words, pos):
    if pos and words[pos - 1] in MOTION_WORDS:
        return True
    if len(words) - pos < 2 or words[pos + 1] not in DETERMINERS:
        return False
    return not any(word in TIME_AFTER_A_PARTICLE for word in words[pos + 2:pos + 5])


def _a_direction(text, at):
    words = [word.strip(".,!?;:-|\"'") for word in text.lower().split()]
    pos = len(text[:at].lower().split())
    return pos < len(words) and _particle_is_a_place(words, pos)

MANIPULATE = frozenset("""turn turns turned turning keep keeps kept keeping put puts putting set
sets setting hold holds holding let lets letting shut shuts shutting slow slows slowing calm
calms calming take takes taking bring brings bringing""".split())
COPULA = frozenset("""am is are was were be been being feel feels feeling felt get gets getting
got seem seems look looks sound sounds still very really quite pretty so too bit little a""".split())


def _copula_before(words, pos):
    for word in reversed(words[:pos]):
        if word in COPULA:
            return True
        if word in BEFORE_STATE:
            continue
        return False
    return True


def _noun_reading(words, pos):
    if pos and words[pos - 1] in DEGREE:
        return False
    return any(word in DETERMINERS for word in words[max(0, pos - 2):pos])


def _thing_turned_down(words, pos):
    if pos < 2 or words[pos - 2] not in DETERMINERS:
        return False
    return pos == 2 or words[pos - 3] in MANIPULATE


NUMBER_WORDS = frozenset("one two three four five six seven eight nine ten eleven twelve".split())
EVENT_NOUNS = frozenset("""funeral christening wake christmas easter birthday wedding anniversary
exam exams interview scan operation surgery birth labour induction move housewarming holiday
holidays honeymoon funeral term semester deadline appraisal review probation""".split())


def _is_person(word):
    return (word in PERSON_SUBJECT or word in PERSON_NOUNS or word in MOOD_NOUNS
            or word in OTHER_PEOPLE or word in {"that", "this", "it"})


def _names_a_thing(words, at):
    if words[at] in EVENT_NOUNS:
        return False
    return any(word in DETERMINERS for word in words[max(0, at - 3):at])


RELATIVE_SUBJECTS = frozenset(("that", "which", "who"))


def _names_somebody_else(words, at):
    return words[at] == "old" and "year" in words[max(0, at - 3):at]


def _whose_state(words, pos, head=None):
    following = [word for word in words[pos + 1:]]
    subject_at = _last_subject_pos(words[:pos if head is None else head])
    if subject_at is not None and words[subject_at] in RELATIVE_SUBJECTS:
        earlier = _last_subject_pos(words[:subject_at])
        if earlier is not None:
            subject_at = earlier
    subject = None if subject_at is None else words[subject_at]
    if subject is not None and _copula_before(words, pos):
        if subject in OTHER_PEOPLE or _names_somebody_else(words, subject_at):
            return "other"
        if _is_person(subject):
            return "self"
        if _names_a_thing(words, subject_at):
            return "thing"
        return "self"
    if following and following[0] in PERSON_PREPOSITIONS:
        if subject in OTHER_PEOPLE:
            return "other"
        if subject is not None and not _is_person(subject):
            return "thing"
        return "self"
    for word in following:
        if word in CONJUNCTIONS:
            break
        if word in BETWEEN_STATE_AND_NOUN or word in TIME_FILLERS:
            continue
        if word.endswith("ly") and len(word) > 4:
            continue
        if word in DETERMINERS:
            continue
        if word.endswith("ing") and len(word) > 4:
            return "self"
        if word in OTHER_PEOPLE:
            return "other"
        if word in PERSON_NOUNS or word in MOOD_NOUNS:
            return "self"
        return "thing"
    if subject is None:
        return "self"
    if subject in OTHER_PEOPLE:
        return "other"
    if subject in PERSON_SUBJECT or subject in PERSON_NOUNS:
        return "self"
    if subject in MOOD_NOUNS:
        return "self"
    if subject in {"that", "this", "it"}:
        return "self"
    if _names_a_thing(words, subject_at):
        return "thing"
    return "self"


BE_FORMS = frozenset("am is are was were".split())
ECHO_CARRIERS = frozenset("""so and but yet or then as well too also just same here yes
me i we us im m""".split())


def _echoed_state(words):
    if not words or len(words) > 6:
        return None
    carried = ((words[0] == "so" and len(words) > 1 and words[1] in BE_FORMS)
               or words[-1:] == ["too"]
               or words[-2:] == ["as", "well"]
               or words[-1:] == ["also"]
               or words[:2] == ["same", "here"]
               or (len(words) == 2 and words[0] in PERSON_SUBJECT and words[1] in BE_FORMS))
    if not carried:
        return None
    if words[:2] in (["same", "here"], ["me", "too"], ["same", "same"]):
        return "self"
    if any(word in PERSON_SUBJECT for word in words):
        return "self"
    if any(word in OTHER_PEOPLE for word in words):
        return "other"
    return None


def _carried_over(words, state_at):
    tail = words[state_at + 1:] if state_at is not None else words
    while tail and tail[0] in CONJUNCTIONS:
        tail = tail[1:]
    return _echoed_state(tail)


def _state_owner(clauses):
    owner = None
    carried = None
    if _works_on_the_speaker(" ".join(
            " ".join(str(word) for word in clause) if isinstance(clause, (list, tuple))
            else str(clause) for clause in clauses)):
        return "self"
    for clause in clauses:
        words = _without_mood_tail(clause)
        if owner is not None and not any(word in STATE_WORDS for word in words):
            echo = _echoed_state(words)
            if echo == "self":
                return "self"
            if echo:
                owner = echo
        state_at = None
        for pos, word in enumerate(words):
            if word not in STATE_WORDS:
                continue
            state_at = pos
            if word in NOUN_STATES and _noun_reading(words, pos):
                continue
            if word in PARTICLE_STATES:
                if _thing_turned_down(words, pos):
                    owner = "thing"
                    continue
                if not _copula_before(words, pos):
                    continue
            if word in COPULA_STATES and (pos == 0 or not _copula_before(words, pos)):
                continue
            head = None
            if word == "fed":
                if "up" not in words[pos + 1:pos + 2]:
                    continue
                head, pos = pos, pos + 1
            whose = _whose_state(words, pos, head)
            if whose is None and carried in PERSON_SUBJECT | PERSON_NOUNS:
                whose = "self"
            if whose == "self":
                return "self"
            if whose:
                owner = whose
        if owner is not None:
            echo = _carried_over(words, state_at)
            if echo == "self":
                return "self"
            if echo:
                owner = echo
        carried = _last_subject(words) or carried
    return owner


def _about_a_supply(text, end):
    rest = [word.strip(".,!?;:-|\"'").lower() for word in text[end:].split()]
    if len(rest) < 2 or rest[0] not in SUPPLY_PREPOSITIONS:
        return False
    thing = rest[1]
    return thing not in OTHER_PEOPLE and thing not in PERSON_NOUNS \
        and thing not in PERSON_SUBJECT


def shortage_of(text):
    words = [word.strip(".,!?;:-|\"'").lower() for word in text.split()]
    for at, word in enumerate(words):
        if word not in SUPPLY_WORDS or at + 2 >= len(words):
            continue
        if words[at + 1] not in SUPPLY_PREPOSITIONS:
            continue
        thing = words[at + 2]
        if thing in DETERMINERS or thing in OWN_RESERVES or thing in OTHER_PEOPLE:
            continue
        if thing in PERSON_NOUNS or thing in PERSON_SUBJECT:
            continue
        return thing
    out = re.search(r"\b(?:run|ran|running) out of ([a-z]+)", text)
    if out and out.group(1) not in OWN_RESERVES and out.group(1) not in DETERMINERS:
        return out.group(1)
    return None


BOT_LIFE = frozenset("""
family families kid kids child children son daughter mum mom mother father dad daddy parents
parent brother brothers sister sisters sibling siblings gran grans grandma grandmas grandad
grandads grandpa grandparents grandparent uncle uncles aunt aunts auntie aunties cousin cousins
niece nephews relatives relative partner husband wife girlfriend boyfriend friends friend
home house flat apartment town hometown address pets pet dog dogs cat cats kitten puppy hamster
rabbit budgie garden
job jobs work boss manager managers employer colleague colleagues coworker coworkers wages wage
salary paycheck pay paid money bank account mortgage bills rent
body face hands feet hair
birthday age born
name nickname
car cars
""".split())
BOT_LIFE_FILLER = frozenset("""
a an any some the your you u ur yourself yours own much many really actually ever then now
yet already also too about of for at in on like and or there both coming come came best
""".split())
BOT_LIFE_ASK = re.compile(r"""
    (?: (?:do|does|did)\s+(?:you|u|ya)\s+(?:have|has|got|get|own|need|want)
      | (?:have|has)\s+(?:you|u|ya)\s+got
      | (?:what|whats|what's|who|whos|who's|whose|which|how)\s+
        (?:is|are|was|were|s|does|do)?\s*(?:your|ur)
      | (?:are|is|was|were)\s+(?:you|u)\s+(?:a|an)
      # "were your mum and dad there", "was your brother there too", "are your parents
      # coming": the thing asked about is the bot's own family, said from the front with no
      # "do you have" in it. Read as an ordinary question it reached the search hedge - "I
      # don't know enough to answer that honestly" to somebody asking whether the bot's mum
      # was at a party - when the bot knows the answer perfectly well: no family at all. The
      # rest-gate below still has to pass, so "is your shop open" and "were your prices
      # online" name something outside the bot's own life and are left alone.
      | (?:are|is|was|were)\s+(?:your|ur)
    )\s*
""", re.VERBOSE)


ITSELF_LONG = re.compile(r"""
    ^\s*(?:so\s+|ok\s+|okay\s+|ah\s+|oh\s+|and\s+|but\s+)*
    (?: how\s+(?:long|many\s+years)
      | how\s+old
      | since\s+when
    )
    \s+(?:have|has|did)\s+(?:you|u|ya)\s+(?:been|be|start|started|go|going|got|get)
    \b
""", re.VERBOSE)
ITSELF_LIFE = frozenset("""
going around round about here there online alive running working doing this that it stuff
things talking chatting answering people folks folk to with us in on at now
""".split())


def _how_long_itself(norm):
    said = " ".join(norm)
    match = ITSELF_LONG.match(said)
    if not match:
        return False
    return not set(said[match.end():].split()) - ITSELF_LIFE


ITSELF_WHEN = re.compile(r"""
    ^\s*(?:so\s+|ok\s+|okay\s+|ah\s+|oh\s+|and\s+|but\s+)*
    (?: when\s+did\s+you\s+(?:start|begin|first\s+start)
      | when\s+were\s+you\s+(?:made|built|started|made\s+up)
      | how\s+long\s+ago\s+did\s+you\s+(?:start|begin)
    )
    \b
""", re.VERBOSE)
ITSELF_WHEN_TAIL = frozenset("""
going out this that it stuff then today now here online working answering helping
""".split())


def _when_itself(norm):
    said = " ".join(norm)
    match = ITSELF_WHEN.match(said)
    if not match:
        return False
    return not set(said[match.end():].split()) - ITSELF_WHEN_TAIL


BOT_DOINGS = frozenset("""
talk talked talking speaks spoke spoken speaking chat chatted chatting answer answered
answering ask asked asking help helped helping heard listening sent send messages messaged
met meet meets
""".split())
BOT_COUNTED = frozenset("""
people person persons conversation conversations chat chats message messages question questions
folk folks
""".split())
COUNT_OPENERS = frozenset("so and but then also".split())
BOT_HAVE = frozenset("have has had having".split())
BOT_CHATS = frozenset("""
chat chats conversation conversations talk talks discussion discussions catch-up
""".split())


BOT_DOERS = frozenset("""
you u ya yourself people person folk folks anyone anybody somebody someone everybody everyone
they customers users guests strangers visitors readers
""".split())
COUNT_FILLERS = frozenset("""
have has had having do does did done been being be is are was were ever already just really
also still not never once yet actually even only so far before since
""".split())


def _counts_its_own_doings(norm):
    words = list(norm)
    at = 0
    while at < len(words) and words[at] in COUNT_OPENERS:
        at += 1
    if words[at:at + 2] not in (["how", "many"], ["how", "much"]):
        return False
    rest = words[at + 2:]
    if not set(rest) & BOT_COUNTED or not {"you", "u", "ya", "your", "ur"} & set(rest):
        return False
    return any(_the_doer_is_the_bot(rest, i) for i, w in enumerate(rest)
               if w in BOT_DOINGS or w in BOT_HAVE and _a_count_of_chats(rest))


def _a_count_of_chats(rest):
    return bool(set(rest) & BOT_CHATS)


def _the_doer_is_the_bot(rest, doing):
    at = doing - 1
    while at >= 0 and (rest[at] in COUNT_FILLERS or rest[at].endswith("ly")):
        at -= 1
    return at >= 0 and rest[at] in BOT_DOERS


def _asks_about_its_experience(norm):
    words = list(norm)
    if not words:
        return False
    said = " ".join(words)
    match = EXPERIENCE_ASK.match(said)
    if not match:
        return False
    rest = said[match.end():].split()
    if not rest:
        return False
    if set(rest) & THEIR_PROBLEM:
        return False
    return all(word in EXPERIENCE_WORDS or word in BOT_LIFE or word in BOT_LIFE_FILLER
               for word in rest)


EXPERIENCE_ASK = re.compile(r"""^(?:(?:and|so|but|oh|well|ok|okay|right|hey|hi|yeah|actually|
honestly|just)\s+)*(?:have|has|did|were|was)\s+(?:you|u|ya)\s+(?:ever|once)\b""",
    re.VERBOSE)
EXPERIENCE_WORDS = frozenset("""
been be being was were had have got get went gone go going done do did seen see saw felt feel
tried try made make met meet ate eaten eat drank drunk smoked ridden rode driven drove worn wore
lived live cry cried laugh laughed hurt love loved hate hated kiss kissed miss missed win won lose
lost give gave given giving keep kept run ran swim swam cook cooked
up down through ill sick unwell happy sad tired lonely scared frightened angry upset worried
glad proud bored excited drunk lost
day days night nights week weeks month months year years time times life lived world holiday
holidays
thing things something anything nothing one ones kind sort bit lot lots
it them that this these those there before once ever really actually
myself yourself
""".split())
THEIR_PROBLEM = frozenset("""
my our me us mine ours happen happens happened occurring seems broken broke leaking dripping noisy
""".split())


KIN = frozenset("""family families kid kids child children son daughter mum mom mother father dad
    daddy parents parent brother brothers sister sisters sibling siblings gran grans grandma
    grandmas grandad grandads grandpa grandparents grandparent uncle uncles aunt aunts auntie
    aunties cousin cousins niece nephews relatives relative partner husband wife girlfriend
    boyfriend""".split())
A_YOUR_KIN = re.compile(
    r"\b(?:"
    r"(?:was|were|are|is)\s+(?:your|ur|yours)\s+(?:" + "|".join(sorted(KIN)) + r")"
    r"|(?:do|does|did|have|has)\s+(?:your|ur)\s+(?:" + "|".join(sorted(KIN)) + r")"
    r")\b")
A_YOUR_OWN_THING = re.compile(
    r"\b(?:(?:what|how)\s+about|and)\s+(?:your|ur)\s+(?:"
    + "|".join(sorted(BOT_LIFE)) + r")(?:\s+(?:too|then|either|as\s+well))?\s*[?.!]*$")

A_HOW_MANY_OF_THE_BOTS_OWN = re.compile(
    r"\b(?:how|what)\s+many\s+\w+(?:\s+\w+)?\s+(?:have|has|do|does)\s+(?:you|u|ya)\b")

A_WHAT_ITS_LIKE = re.compile(r"\b(?:what|whats|what's)\b.*\blike\s+being\s+(?:you|u|ya)\b")


def _asks_about_its_own_life(norm):
    words = list(norm)
    if not words or not {"you", "u", "ya", "your", "ur", "yours", "yourself"} & set(words):
        return False
    match = BOT_LIFE_ASK.match(" ".join(words))
    if not match:
        return False
    rest = " ".join(words)[match.end():].split()
    if not rest or set(rest) - BOT_LIFE - BOT_LIFE_FILLER:
        return False
    return bool(set(rest) & BOT_LIFE)


JOIN_OPENERS = frozenset("and".split())
A_PERSON_AFTER_A_POSSESSIVE = frozenset("""boy girl son daughter child kid baby man woman
    brother sister mum mom dad mother father friend wife husband partner""".split())

LEARNING_WORDS = frozenset("""learn learns learnt learned learning remember remembers
    remembered recall recalls forget forgets pick picks take takes keep keeps""".split())
A_HAVING = frozenset("""have has had having got gets getting want wants wanted expecting
    trying planning""".split())
CHILD_NOUNS = frozenset("""boy girl son daughter child kid kids baby babies twins""".split())
POSSESSIVE_WORDS = frozenset("your my our his her their".split())
MAKER_WORDS = frozenset("made make makes making created create built build built trained "
                        "programmed program designed wrote written".split())


def _the_bots_own_not(norm, i):
    if i + 1 < len(norm) and norm[i + 1] in NOT_BEFORE_THE_BOT:
        return True
    if i >= 1 and norm[i - 1] in NOT_AFTER_THE_BOT:
        return True
    if (i >= 2 and norm[i - 2] in NOT_BEFORE_THE_BOT and norm[i - 1] in NOT_AUX
            and (i < 3 or norm[i - 3] not in CLAUSE_OPENERS)):
        return True
    return False


_I_SAID_IT = re.compile(
    r"^\W*(?:(?:and|but|so|ok|okay|right|now|then|wait)[,. ]+)*"
    r"(?:what|which|when|where)\b[^.?!]*?\bi\b[^.?!]*?"
    r"\b(?:said|say|told|tell|mentioned|mention|asked|ask)\b", re.I)


def _recalls_their_own_line(norm):
    return bool(_I_SAID_IT.match(" ".join(str(word) for word in norm if word)))


def _self_ask(norm):
    words = set(norm)
    if not words or not words & {"you", "your", "yourself", "yours"}:
        return False
    if not words & SELF_ASK:
        return False
    if _a_person_they_like(norm) or _a_thing_they_own(norm):
        return False
    if norm and norm[0] in JOIN_OPENERS and words & MAKER_WORDS:
        return False
    if any(norm[i] in POSSESSIVE_WORDS and norm[i + 1] in A_PERSON_AFTER_A_POSSESSIVE
           for i in range(len(norm) - 1)):
        return False
    if any(norm[i] in LEARNING_WORDS and norm[i + 1] == "from" for i in range(len(norm) - 1)):
        return False
    if set(norm) & A_HAVING and set(norm) & CHILD_NOUNS:
        return False
    left = words - SELF_WORDS - SELF_FILLER - {"you", "your", "yourself", "yours"}
    if "not" in words:
        if any(norm[i] == "not" and not _the_bots_own_not(norm, i)
               for i in range(1, len(norm))):
            return False
        left = left - {"not"}
    return not left


def _about_bot(text, words, norm=()):
    return _about_bot_kind(text, words, norm) is not None


def _asks_if_the_bot_is_a_product(norm):
    if len(norm) < 2 or len(norm) > PRODUCT_ASK_WORDS or norm[0] not in ("are", "is"):
        return False
    if set(norm) & ROBOT_WORDS:
        return False
    tail = list(norm)
    while tail and tail[-1] in PRODUCT_ASK_TAIL:
        tail.pop()
    return len(tail) > 1 and tail[-1] in ASSISTANT_NAMES


def _starts_with(words, phrases):
    bare = " ".join(words)
    return any(bare == p or bare.startswith(p + " ") for p in phrases)


BEFORE_COURTESY = frozenset("aw aww ah ahh oh ohh ooh awe ha haha um umm er hmm".split())


def without_filler(norm):
    if len(norm) > 1 and norm[0] in BEFORE_COURTESY:
        return norm[1:]
    return norm


COURTESY_THING = frozenset("""card cards letter letters message messages note notes mail
    email emails text texts speech poem poem story banner sign tag tags gift gifts present
    presents cake wine chocolates flowers box bag""".split())


def _a_thing_named_after_the_courtesy(norm):
    rest = _after_thanks(norm)
    return bool(rest) and rest[0] in COURTESY_THING


def _after_thanks(norm):
    for phrase in sorted(THANKS, key=len, reverse=True):
        words = phrase.split()
        if norm[:len(words)] == words:
            rest = norm[len(words):]
            if rest[:1] and rest[0] in COURTESY_THING:
                return None
            return rest
    return None


def the_line_after_a_courtesy(norm):
    return _after_thanks(without_filler(norm))


NEEDS_ANSWER = frozenset("""hurt hurts hurting hurt ache aches aching pain painful sore agony
    worse worst not never wont cant cannot dont doesnt didnt isnt arent wasnt weren kept
    killing killed
    keeps stopped stops broken broke breaks leaking leaks leak stuck died dead die rash
    swollen bleeding bled sick unwell slow noisy noise smells burning stings itches
    problem problems wrong stuck rubbish awful terrible worried worrying scared""".split())

STILL_WRONG = re.compile(r"""
    \b(?:
        (?!cache\b)\w*ache | fever(?:ish)? | cough(?:ing)? | dizzy | nauseous? | vomit(?:ing)?
      | shiver(?:s|ing|y)? | chills | dehydrat\w+
      | (?:have|has|had|got|gotten|running|caught|catch|my|his|her|their|your)
        \s+(?:an?\s+)?(?:high\s+|slight\s+|bit\s+of\s+a\s+|touch\s+of\s+a\s+)?temperature
    )\b
""", re.X)

FOUND = frozenset("""blog article post page site website video photo picture recipe thread
    comment question quiz idea story podcast episode book film answer deal bargain
    mind""".split())
SLIPPED_FROM = frozenset("across upon into through by away past".split())
FALL = frozenset("fallen fainted".split())
FELL_WORDS = FALL | frozenset("""fell fall falls falling tripped tripping slipped slipping
    stumbled stumbling collapsed collapse""".split())


def _a_fall(rest):
    for index, word in enumerate(rest):
        if word in FALL or word.startswith("collaps"):
            return True
        if word == "fell":
            after = rest[index + 1] if index + 1 < len(rest) else ""
            if after not in ("asleep", "for", "into", "in", "behind", "out"):
                return True
            continue
        if word in ("tripped", "slipped", "slipping", "stumbled", "stumbling"):
            after = rest[index + 1:index + 7]
            if after[:1] and after[0] in SLIPPED_FROM:
                continue
            if [one for one in after if one in FOUND]:
                continue
            return True
    return False


GREETING_TAIL = frozenset("""there again all folks friends everyone everybody guys you your
    mate quick question hope hopes hoping doing day today going well good thanks thank then
    too also just so how are is it things up sup life ok okay alright fine here back""".split())
INTRODUCES = (("my", "name", "is"), ("the", "name", "is"), ("i", "am"), ("im",),
              ("call", "me"), ("this", "is"), ("its",))


def _after_greeting(norm):
    for phrase in sorted(GREETINGS, key=len, reverse=True):
        words = phrase.split()
        if norm[:len(words)] == words:
            return norm[len(words):]
    return None


def after_greeting(norm):
    return _after_greeting(list(norm or []))


FAREWELL_TAIL = frozenset("""then ok okay right well so all everyone everybody guys folks mates
    now for to soon later tomorrow tonight night good xx xxx love hun""".split())


_SAID_ON_ITS_OWN = frozenset(
    [word for phrase in THANKS + FAREWELLS for word in phrase.split()])
_THANKS_WORDS = frozenset([word for phrase in THANKS for word in phrase.split()])
_NIGHT_WISHES = ("sleep well", "sleep tight", "sleep good", "sweet dreams", "rest well",
                 "night night")
_WISH_WORDS = frozenset(" ".join(_NIGHT_WISHES).split())


def _after_farewell(norm):
    for phrase in sorted(FAREWELLS, key=len, reverse=True):
        words = phrase.split()
        if norm[:len(words)] == words:
            return norm[len(words):]
    return None


def farewell_only(norm):
    rest = _after_farewell(norm)
    if rest is None:
        return False
    if set(rest) & NEEDS_ANSWER:
        return False
    left = [word for word in rest if word not in _WISH_WORDS]
    if len(left) < len(rest) and all(word in FAREWELL_TAIL or word in POLITE for word in left):
        return True
    if rest and rest[0] in _THANKS_WORDS:
        return True
    return all(word in FAREWELL_TAIL or word in POLITE or word in _SAID_ON_ITS_OWN
               or word in TERMS_OF_ADDRESS for word in rest)


def greeting_only(norm):
    rest = _after_greeting(norm)
    if rest is None:
        return False
    if all(word in GREETING_TAIL or word in POLITE for word in rest):
        return True
    if len(rest) <= 2 and not set(rest) & NEEDS_ANSWER \
            and not _says_what_they_are(rest):
        return True
    for lead in INTRODUCES:
        if tuple(rest[:len(lead)]) != lead:
            continue
        tail = [word for word in rest[len(lead):] if word not in NAMING_WORDS]
        if not 1 <= len(tail) <= 2:
            return False
        return all(_a_name(word) for word in tail)
    return False


NAMING_WORDS = frozenset(("called", "named", "name", "names"))


def _says_what_they_are(rest):
    from ..memory.facts import about_themselves
    return bool(about_themselves(" ".join(rest)))


def _a_name(word):
    from ..memory.facts import reads_as_a_name
    return bool(reads_as_a_name(word))


HELP_WAS_GOOD = frozenset((
    "that helps", "this helps",
    "that really helps", "this really helps",
    "that helps a lot", "that helps loads", "that helps so much",
    "that helped", "this helped",
    "that really helped", "this really helped",
    "that helped a lot", "that helped loads", "that helped so much",
    "thats helpful", "that is helpful", "that was helpful",
    "this is helpful", "this was helpful",
))
BEFORE_HELP_WAS_GOOD = frozenset("ok okay yeah yep yes ah oh right cool so".split())
AFTER_HELP_WAS_GOOD = frozenset("""actually tbh honestly really though tho anyway now then
    mind cheers thanks""".split())
AFTER_HELP_WAS_GOOD_SAID_OUT = ("to be honest", "to be fair", "if im honest", "if i am honest",
                                "in all honesty", "to tell the truth")


def _says_the_help_was_good(norm):
    words = list(norm)
    while len(words) > 2 and words[0] in BEFORE_HELP_WAS_GOOD:
        words = words[1:]
    while len(words) > 2:
        said = " ".join(words)
        tail = next((phrase.split() for phrase in AFTER_HELP_WAS_GOOD_SAID_OUT
                     if said.endswith(" " + phrase)), None)
        if tail is None and words[-1] in AFTER_HELP_WAS_GOOD:
            tail = [words[-1]]
        if tail is None or len(words) - len(tail) < 2:
            break
        words = words[:-len(tail)]
    return " ".join(words) in HELP_WAS_GOOD


def _thanks_only(norm, clauses=None):
    rest = _after_thanks(norm)
    if rest is None:
        return False
    if set(rest) & NEEDS_ANSWER:
        return False
    if STILL_WRONG.search(" ".join(rest)):
        return False
    if _a_clause_of_its_own(rest, clauses):
        return False
    return not _a_fall(rest)


THANKS_ABOUT = frozenset("that this it they them those these which".split())
BETTER = frozenset("""better best glad happy pleased relieved easier lighter improved gone
    tried try trying worked works""".split())
SAYS_ABOUT_YOU = frozenset("you your yours u ya".split())
PRAISING = frozenset("""perfect great brilliant lovely delicious gorgeous superb spot amazing
    excellent wonderful nice good marvellous marvelous fantastic smashing""".split())
PRAISING_VERB = frozenset("""loved love loves liked like likes enjoyed enjoy enjoys adored
    devoured demolished wolfed""".split())
PRAISE_SAID = re.compile(r"\b(?:went|gone)\s+down\s+(?:well|a\s+treat|great|nicely)\b")
TURNED_ROUND = frozenset("but though although except however".split())
STEP_VERBS = frozenset("""cleared restarted rebooted reinstalled uninstalled deleted removed
    emptied cleaned washed rinsed changed swapped reset updated charged plugged poured soaked
    drained defrosted tried gave followed did put set""".split())
STEP_ANY_OBJECT = frozenset("put set did gave changed".split())
STEP_WRONG = frozenset("""wrong mistake error errors failed fails broken broke wont cant
    stopped worse nothing none no not still again""".split())
SIGNING_OFF = re.compile(r"""
    \b(?:i'?m|im|i\s+am|we'?re|were|we\s+are)\s+(?:off|away|going|turning\s+in|heading)\b
    | \b(?:good\s*night|goodnight|bedtime|off\s+to\s+bed|turning\s+in)\b
    | \bnothing\s+(?:else|more|left)\b | \bnothing\s+to\s+do\b
    """, re.X)


def _a_clause_of_its_own(rest, clauses=None):
    if not rest or rest[0] in THANKS_ABOUT:
        return False
    if _starts_with(rest, THANKS):
        return False
    if len(rest) < 4:
        return False
    if _a_step_done(rest):
        return _the_step_went_wrong(rest)
    if _agrees(rest) or set(rest) & BETTER:
        return False
    if _praises_the_thing(rest):
        return False
    if set(rest) & SAYS_ABOUT_YOU:
        return False
    if _a_fall_that_is_not_one(rest):
        return False
    if "temperature" in rest:
        return False
    if SIGNING_OFF.search(" ".join(rest)):
        return False
    for clause in (clauses or [])[1:]:
        if len(clause) >= 4 and clause[0] not in THANKS_ABOUT:
            return True
    return False


def _a_step_done(rest):
    if len(rest) < 3 or rest[0] not in ("i", "we"):
        return False
    if rest[1] not in STEP_VERBS and not (rest[1] == "gave" and "go" in rest[2:4]):
        return False
    after = rest[2:]
    if rest[1] in ("tried", "swapped"):
        return after[:1] == ["it"]
    if rest[1] in STEP_ANY_OBJECT and after[:1] not in (["it"], ["the"]):
        return False
    return "the" in after or "my" in after or after[:1] == ["it"]


def _the_step_went_wrong(rest):
    return bool(set(rest[2:]) & STEP_WRONG)


def _a_fall_that_is_not_one(rest):
    if not set(rest) & FELL_WORDS:
        return False
    return not _a_fall(rest)


def _praises_the_thing(rest):
    if not (set(rest) & (PRAISING | PRAISING_VERB) or PRAISE_SAID.search(" ".join(rest))):
        return False
    return not set(rest) & TURNED_ROUND


AGREE_TAIL = frozenset("""it that this these those all so much very quite a an lot bit really
    pretty good great fine nice cool ok okay lovely brilliant magic perfect spot better best
    well helps helped works worked working doing do does is was been am are you your not no
    too to and now enough still same here there just also then
    love loved loving like liked liking righto alright ace grand decent pleased glad happy
    kind kindest thoughtful generous sweet
    one ones of""".split()) | AFFIRM

AGREE_AFTER_NOT = frozenset("bad half wrong shabby".split())

NOT_FILLER = frozenset("too that so very much all quite a an to even really feeling".split())

THANKS_NOISE = frozenset("oh ah aha aah ahh ohh ooh aw aww mm mmm".split())

ADDRESSED = frozenset("""love mate pet hun duck sunshine hen flower chuck dear pal buddy
    babes shug lovey""".split())


def _agrees(rest):
    if "not" not in rest:
        return all(word in AGREE_TAIL for word in rest)
    after = rest[rest.index("not") + 1:]
    while after and after[0] in NOT_FILLER:
        after = after[1:]
    if not (after and after[0] in AGREE_AFTER_NOT):
        return False
    return all(word in AGREE_TAIL or word in AGREE_AFTER_NOT for word in after)


def _ends_with_thanks(norm):
    said_to = len(norm)
    while said_to and norm[said_to - 1] in ADDRESSED:
        said_to -= 1
    line = norm[:said_to]
    named = said_to < len(norm)
    for phrase in sorted(THANKS, key=len, reverse=True):
        words = phrase.split()
        if len(line) > len(words) and line[-len(words):] == words:
            rest = [word for word in line[:-len(words)] if word not in THANKS_NOISE]
            if not rest:
                return True
            if len(rest) > 6:
                continue
            if set(rest) <= (AFFIRM | ACK) and not named:
                continue
            if rest[:1] and rest[0] in {"no", "nope", "nah", "never", "naw"}:
                continue
            if not _agrees(rest):
                continue
            return True
    return False
OPENING_FRAME = re.compile(r"""
    \b(?:can|could|may|might)\s+i\s+ask\s+(?:you\s+)?(?:something|somethin|a\s+question|one\s+thing|advice|for\s+advice|your\s+advice)\b
  | \b(?:i|ive)?\s*(?:have|got|has)\s+(?:a\s+|one\s+|quick\s+)?question\b
  | \bquick\s+question\b
  | \b(?:i|we)\s+(?:need|want|would\s+like|could\s+use)\s+(?:(?:some|a\s+bit\s+of)\s+)?(?:your\s+)?advice\b
  | \b(?:can|could|would|will)\s+you\s+help\s+me\s+(?:with\s+something|with\s+a\s+thing|with\s+one\s+thing|out\s+with\s+something)\b
  | \bmind\s+if\s+i\s+ask\s+(?:you\s+)?(?:something|a\s+question)\b
  | \bi\s+(?:want|need)\s+to\s+ask\s+you\s+(?:something|a\s+question)\b
""", re.X)
OPENING_WORDS = frozenset("""can could may might i ask you something somethin a one thing
    question quick have got has ive we need want would like use some bit of for your advice
    help me with out will to if mind is it""".split())
OPENING_MAX = 9
TALK_ASK_VERBS = r"(?:vent|rant|moan|whinge|grumble|offload|unload)"
TALK_TAIL_WORDS = (r"(?:\s+(?:a\s+bit|a\s+minute|a\s+sec|a\s+moment|one\s+thing|"
                   r"for\s+a\s+minute|for\s+a\s+bit|about\s+something|about\s+it|"
                   r"about\s+this|to\s+you|to\s+someone|on\s+you|here|first))*")
TALK_ASK_OPENERS = (r"(?:(?:can|could|may)\s+(?:i|we)|do\s+you\s+mind\s+if\s+i|"
                    r"would\s+you\s+mind\s+if\s+i|is\s+it\s+ok\s+if\s+i|"
                    r"is\s+it\s+okay\s+if\s+i)")
TALK_OPENING = re.compile("|".join((
    r"(?:i\s+|we\s+)?(?:just\s+|really\s+|honestly\s+|properly\s+)?(?:am\s+|are\s+)?"
    r"(?:(?:want|wanna|need|have|got|gotta|planning|going|gonna)\s+)?(?:to\s+)?"
    + TALK_ASK_VERBS + TALK_TAIL_WORDS,
    r"(?:can|could|may)\s+(?:i|we)\s+(?:just\s+)?(?:have\s+a\s+)?" + TALK_ASK_VERBS
    + TALK_TAIL_WORDS,
    r"(?:i\s+|we\s+)?(?:just\s+)?(?:am\s+|are\s+)?(?:going\s+to\s+|gonna\s+)?"
    r"(?:(?:want|wanna|need|have|got|gotta)\s+(?:to\s+)?)?(?:have\s+)?a\s+"
    r"(?:proper\s+|good\s+|quick\s+|little\s+)?(?:vent|rant|moan|whinge|grumble)"
    + TALK_TAIL_WORDS,
    r"(?:i\s+)?(?:just\s+)?(?:(?:want|wanna|need|have|got|gotta)\s+(?:to\s+)?"
    r"|(?:can|could|may)\s+i\s+|let\s+me\s+)(?:get\s+)?"
    r"(?:something|somethin|this|it)\s+off\s+my\s+chest",
    r"(?:i\s+|we\s+)?(?:just\s+|really\s+)?(?:am\s+|are\s+)?"
    r"(?:(?:want|wanna|need|have|got|gotta|going)\s+(?:to\s+)?"
    r"|(?:can|could|may)\s+(?:i|we)\s+)"
    r"talk" + TALK_TAIL_WORDS,
    r"(?:i\s+)?(?:need|want|would\s+like)\s+"
    r"(?:someone|somebody|anyone|anybody)\s+to\s+talk\s+to",
    r"(?:can|could|may)\s+i\s+(?:have\s+a\s+word)",
    r"(?:i\s+)?(?:need|want)\s+a\s+word",
    TALK_ASK_OPENERS + r"\s+"
    r"(?:run|bounce|try|talk\s+through)\s+"
    r"(?:something|somethin|this|that|it|an?\s+idea|one\s+thing|a\s+couple\s+of\s+things|"
    r"a\s+few\s+things|some\s+ideas?)\s+(?:by|past|off)\s+you" + TALK_TAIL_WORDS,
    TALK_ASK_OPENERS + r"\s+"
    r"(?:pick\s+your\s+brains?|bend\s+your\s+ear)" + TALK_TAIL_WORDS,
    TALK_ASK_OPENERS + r"\s+"
    r"(?:tell\s+you\s+what\s+happened|share\s+(?:something|this|it)\s+with\s+you|"
    r"have\s+a\s+second\s+opinion|get\s+a\s+second\s+opinion)" + TALK_TAIL_WORDS,
)))
TALK_HEAD = frozenset("""right ok okay so look well honestly listen alright now then""".split())
TALK_TAIL = (("to", "be", "honest"), ("if", "that", "is", "ok"), ("if", "thats", "ok"),
             ("now",), ("please",), ("then",), ("thanks",), ("right",), ("actually",),
             ("quickly",), ("quick",), ("mate",))


def _talk_opening(text):
    words = text.split()
    changed = True
    while words and changed:
        changed = False
        if words[0] in TALK_HEAD:
            words, changed = words[1:], True
        for tail in TALK_TAIL:
            if len(words) > len(tail) + 1 and tuple(words[-len(tail):]) == tail:
                words, changed = words[:-len(tail)], True
                break
    return bool(words) and bool(TALK_OPENING.fullmatch(" ".join(words)))


def talk_frame(norm):
    text = " ".join(word for word in norm if word)
    return bool(text) and _talk_opening(text)


def opening_line(norm):
    words = [word for word in norm if word]
    if not words:
        return False
    text = " ".join(words)
    if _talk_opening(text):
        return True
    if len(words) > OPENING_MAX:
        return False
    if words[0] in {"have", "do", "does", "did"}:
        return False
    if not all(word in OPENING_WORDS for word in words):
        return False
    return bool(OPENING_FRAME.search(text))




def _short_reply(text):
    for phrase in SHORT_REPLIES:
        if text == phrase or text.startswith(phrase + " "):
            return True
    return False


COMMIT_OPEN = frozenset("""will wont would gonna going sall ill il id weve well lets let""".split())
COMMIT_TRY = frozenset("""try give go see have take""".split())
COMMIT_SUBJECT = frozenset("i we".split())
COMMIT_ALONE = ("give it a go", "give it a try", "give that a go", "give that a try",
                "give it a shot", "have a go", "have a try", "give it a whirl",
                "try that", "try it", "try this")
COMMIT_ALONE_TAIL = ("let you know", "sounds like a plan")
HEDGED_COMMIT = frozenset("might could may".split())
HEDGED_ALONE = COMMIT_ALONE + ("do that", "do it", "go for it", "ring them", "call them")
COMMIT_NO_HARM = ("worth a try", "worth a go", "worth trying", "worth a shot",
                  "cant hurt", "cannot hurt", "no harm in", "nothing to lose")
HEDGE_LEAD_ONE = frozenset("maybe probably suppose guess honestly".split())
HEDGE_LEAD_TWO = ("i suppose", "i guess", "i think", "i reckon")
NO_HARM_SUBJECT = frozenset("it its that this there".split())
COMMIT_STOP = frozenset("""you u ya your yourself yall""".split())


def _cant_for_cannot(words):
    joined = []
    index = 0
    while index < len(words):
        if words[index] == "can" and words[index + 1:index + 2] == ["not"]:
            joined.append("cant")
            index += 2
            continue
        joined.append(words[index])
        index += 1
    return " ".join(joined)


def _agrees_to_try(norm):
    words = [word for word in norm if word and word != "|"]
    if not words or len(words) > 9:
        return False
    if any(word in QUESTION_WORDS or word in COMMIT_STOP for word in words):
        return False
    bare = " ".join(words)
    hedged = list(words)
    while hedged:
        if hedged[0] in HEDGE_LEAD_ONE:
            hedged = hedged[1:]
        elif " ".join(hedged[:2]) in HEDGE_LEAD_TWO:
            hedged = hedged[2:]
        else:
            break
    said = _cant_for_cannot(hedged)
    if said.split()[:1] and said.split()[0] in NO_HARM_SUBJECT:
        said = " ".join(said.split()[1:])
    if 0 < len(said.split()) <= 7 and any(said == phrase or said.startswith(phrase + " ")
                                          for phrase in COMMIT_NO_HARM):
        return True
    if bare in COMMIT_ALONE:
        return True
    if any(bare.startswith(phrase + " ") and len(words) <= 5 for phrase in COMMIT_ALONE):
        return True
    if any(bare == phrase or bare.startswith(phrase + " ") for phrase in COMMIT_ALONE_TAIL):
        return True
    lead = strip_leaders(words)
    if lead[:1] and lead[0] in AFFIRM:
        lead = lead[1:]
        if lead[:1] == ["one"]:
            lead = lead[1:]
    if lead[:1] and lead[0] in COMMIT_SUBJECT:
        lead = lead[1:]
    if lead[:1] and lead[0] in HEDGED_COMMIT:
        rest = " ".join(lead[1:])
        return any(rest == phrase or rest.startswith(phrase + " ")
                   for phrase in HEDGED_ALONE)
    if lead[:1] and lead[0] in COMMIT_SUBJECT:
        lead = lead[1:]
    if not lead or lead[0] not in COMMIT_OPEN:
        return False
    lead = lead[1:]
    if lead[:1] == ["to"]:
        lead = lead[1:]
    return bool(lead) and lead[0] in COMMIT_TRY


ASK_THE_ROOM = frozenset("""anyone anybody somebody someone everyone everybody any1 some1
    every1 evry1 no1""".split())
ASK_THE_ROOM_ANY = frozenset("""anyone anybody any1""".split())
ASK_THE_ROOM_WANTS = frozenset("""where if how what which whether why who whom whose
    a an any some""".split())
ASK_THE_ROOM_VERB = frozenset("""know knows knew got have has had recommend recommends
    suggest suggests tried try seen see use uses found find want wants need needs""".split())


def _asks_the_room(stripped):
    if len(stripped) < 2 or stripped[0] not in ASK_THE_ROOM:
        return False
    if stripped[1] not in ASK_THE_ROOM_VERB:
        return False
    if stripped[0] in ASK_THE_ROOM_ANY:
        return True
    if stripped[1] not in ASK_FOR_A_NAME:
        return False
    return len(stripped) > 2 and stripped[2] in ASK_THE_ROOM_WANTS


TAIL_ASKS = frozenset("""ideas idea thoughts thought advice tips tip suggestions suggestion
    recommendations recommendation help pointers""".split())
TAIL_ASK_FILLER = frozenset("""any some more your please a quick few""".split())
SETUP_MOST_WORDS = 45
SETUP_NOTHING = frozenset("""thanks thank you ta cheers hi hello hey morning evening goodnight ok
    okay right so well and but oh ah hmm um yeah yes no anyway alright lol haha lmao""".split())
SETUP_CONNECTIVES = frozenset("""since because cos cause and but so if when while although
    though as then also plus or with for to of in on at by from that it its this these those
    there here neither nor either both too same me""".split())


def _asks_at_the_end(clause):
    stripped = strip_leaders(clause) or clause
    if not stripped:
        return False
    if _opens_question(stripped):
        return True
    return bool(set(stripped) & TAIL_ASKS) and set(stripped) <= (TAIL_ASKS | TAIL_ASK_FILLER)


FRAME_NOT_A_SETUP = re.compile(
    r"^(?: (?:and |but |oh |well |so |ok |okay |right |no )?"
    r"(?:never mind|nevermind|i mean|i meant|you know what i mean|i dunno|dunno"
    r"|not sure|no idea|honestly|sorry|one more thing|one thing|another thing|quick one"
    r"|back to \w+(?: \w+){0,2}"
    r"|of course|fair enough|me too|same here|no worries|anyway|just wondering"
    r"|just asking|quick question|random question|random one|hi|hey|hello|hiya"
    r"|good question)\b(?: .{0,12})?)+$")


A_FRAME_IN_FRONT = re.compile(
    r"^(?:(?:hi|hiya|hey|hello|morning|evening|ok|okay|right|well|also|i mean|i meant"
    r"|honestly|sorry|cheers"
    r"|thanks|thank you|no worries|quick one|quick question|random question|random one"
    r"|one more thing|another thing|just wondering|just asking|lol|haha|lmao|anyway"
    r"|bit of a random one|bit random|random one|and|but|so)(?:[\s,.-]+|$))+", re.I)


def _says_nothing_but_the_floor(clause):
    words = set(strip_leaders(clause) or clause)
    return not words or words <= (SETUP_NOTHING | SETUP_CONNECTIVES)


def the_setup(line):
    clauses = [clause for clause in (line.get("clauses") or []) if clause]
    if len(clauses) < 2:
        return None
    ask_at = None
    for index in range(len(clauses) - 1, 0, -1):
        if _asks_at_the_end(clauses[index]):
            ask_at = index
            break
    if ask_at is None:
        return None
    before = clauses[:ask_at]
    if any(_opens_question(clause) for clause in before):
        return None
    if all(_says_nothing_but_the_floor(clause) for clause in before):
        return None
    setup = " ".join(" ".join(strip_leaders(clause) or clause) for clause in before)
    setup = A_FRAME_IN_FRONT.sub("", setup).strip(" ,-")
    if not setup:
        return None
    if len(setup.split()) > SETUP_MOST_WORDS:
        return None
    if FRAME_NOT_A_SETUP.match(" " + setup):
        return None
    if not set(setup.split()) - SETUP_CONNECTIVES:
        return None
    return setup


def _opens_question(clause):
    stripped = strip_leaders(clause) or clause
    if _asks_the_room(stripped):
        return True
    if not stripped or stripped[0] not in QUESTION_STARTS:
        return False
    if (len(stripped) > 2 and stripped[1] in NEGATIONS
            and stripped[1] not in SUBJECT_NEGATIONS
            and stripped[2] not in PRONOUNS):
        return False
    if stripped[0] == "do" and len(stripped) > 1 and stripped[1] in QUESTION_WORDS:
        return False
    if (stripped[0] in YESNO_STARTS and len(stripped) > 1
            and _verb_form(stripped[1], stripped[0])):
        return False
    if len(stripped) > 1 and opens_without_subject(stripped, 0):
        return False
    return True


TIPS_FRAME = frozenset("""any some few got get need needs needed wanted looking look for
    share send give me us please pls thanks thank you tips tip hints hint pointers pointer
    advice a an the and or to on about this that it is are do have has i u my""".split())


QUESTION_NOUNS = frozenset("q qs question questions query queries".split())
ASKING_VERBS = frozenset("ask asks asked asking".split())
ASK_ABOUT = frozenset("about abt bout re regarding on with something anything".split())
ASK_FRAMES = frozenset("""a an and another ask asked asking but can could daft got have has
    hey hi i ive just little may mind need one please pls quick random silly small sorry stupid
    wanna want we would will""".split())
PAST_ASK = frozenset("asked told answered repeated mentioned".split())
ALREADY_ASKED = frozenset("""what why how when where who which whose whether""".split())
ASK_MODALS = frozenset("can could may might want wants wanted wanna need needs needed".split())
ASK_AUX = frozenset("""am is are was were im be been being just only still actually ever also
    always""".split())
ASK_TARGET = frozenset("you u something somethin anyone anybody".split())
HAND_OVER_VERBS = frozenset("""give gives gave send sends sent throw throws threw chuck chucks
    hit hits fire fires read reads bring brings brought pass passes offer offers ask asks quiz
    quizzes test tests""".split())
HAND_OVER_TO = frozenset("me us".split())
HAND_OVER_MINE = frozenset("knowledge trivia quiz quizzes iq memory brain".split())
HAND_OVER_LEADS = frozenset("""please pls plz kindly just maybe perhaps ok okay so and then now
    also quick quickly""".split())
HAND_OVER_MODALS = frozenset("can could will would should".split())
HAND_OVER_SUBJECTS = frozenset("you u ya".split())


def _hands_a_question_to_the_speaker(norm):
    words = [word for word in norm if word and word != "|"]
    for at, word in enumerate(words[:-1]):
        if word not in HAND_OVER_VERBS:
            continue
        handed_to = (words[at + 1] in HAND_OVER_TO
                     or (words[at + 1] in ("my", "our") and at + 2 < len(words)
                         and words[at + 2] in HAND_OVER_MINE))
        if not handed_to:
            continue
        before = words[:at]
        if not before:
            return True
        modal = any(w in HAND_OVER_MODALS for w in before)
        if not all(w in HAND_OVER_LEADS or w in HAND_OVER_MODALS
                   or (modal and w in HAND_OVER_SUBJECTS) for w in before):
            continue
        if modal or not any(w in HAND_OVER_SUBJECTS for w in before):
            return True
    return False


def _asks_a_question_coming(norm, text):
    if not 0 < len(norm) <= 12 or "?" in text or set(norm) & ALREADY_ASKED:
        return False
    if _hands_a_question_to_the_speaker(norm):
        return False
    if norm[0] in {"do", "does", "did", "any"}:
        return False
    if norm[0] in {"have", "has"} and len(norm) > 1 and norm[1] in {"you", "u", "anyone",
                                                                  "anybody", "any", "they"}:
        return False
    for at, word in enumerate(norm[:5]):
        if word == "asked" and at == 1 and norm[0] in {"i", "we"}:
            continue
        if set(norm[:at]) & PAST_ASK:
            continue
        after = norm[at + 1] if at + 1 < len(norm) else ""
        asked_here = (word in ASKING_VERBS
                      and after in ASK_TARGET | ASK_ABOUT
                      and (at == 0
                           or any(before in ASK_MODALS | ASK_AUX for before in norm[:at])
                           or after in ASK_TARGET))
        named = word in QUESTION_NOUNS or asked_here
        if not named:
            continue
        if at == 0 or any(before in ASK_FRAMES for before in norm[:at]):
            return True
    return False


def _asks_for_tips(text, norm=()):
    about = [word for word in norm if word not in TIPS_FRAME]
    for match in TIPS.finditer(text):
        before, after = text[:match.start()], text[match.end():]
        if TIPS_AMOUNT.search(before):
            continue
        if TIPS_WANTED.search(before):
            if about:
                return True
            continue
        if match.group(1) in ("tips", "hints", "pointers"):
            if TIPS_SUBJECT.search(before):
                continue
            if TIPS_ABOUT.match(after) or not after.strip(" ?.!,"):
                return True
    return False
YOU_WORDS = frozenset("you u ya ur dya".split())
ASK_VERBS = frozenset("think reckon guess recommend suggest mind".split())
ASK_FOLLOW = frozenset("""i we us ill im id it its that this these those she he they them
there my your our their should can could will would shall is are was were do does did if
whether what when where who which why how any anything something someone""".split())


def _asks_the_bot(norm):
    if len(norm) < 3:
        return False
    return (norm[0] in YOU_WORDS and norm[1] in ASK_VERBS and norm[2] in ASK_FOLLOW)

ANY_ANSWER_WANTED = frozenset("""word words luck idea ideas chance chances
    joy sign signs hint hints intel new else""".split())
ANY_ANSWER_LINKS = frozenset("on about with from of for regarding concerning re".split())
ANY_ALREADY_ASKS = frozenset(("idea", "ideas"))

def after_any_link(norm):
    if not norm or norm[0] not in ("any", "anything"):
        return ()
    if len(norm) < 2 or norm[1] not in ANY_ANSWER_WANTED:
        return ()
    for at in range(2, len(norm)):
        if norm[at] in ANY_ANSWER_LINKS:
            return tuple(norm[at + 1:])
    return ()


def _asks_after_any(norm):
    if not norm or len(norm) < 2 or norm[1] in ANY_ALREADY_ASKS:
        return False
    about = after_any_link(norm)
    return bool(about) and not _names_a_person(about)


def _names_a_person(words):
    return any(words[at] in OWNS_A_PERSON and words[at + 1] in A_PERSON_NAMED
               for at in range(len(words) - 1))

ASK_FOR_A_NAME = frozenset("""know knows knew recommend recommends suggest suggests
    found find""".split())


COMPARATIVE = frozenset(("best", "better"))
DESCRIBES = frozenset((
    "feel", "feels", "feeling", "felt", "do", "does", "did", "doing", "done", "get", "gets",
    "getting", "got", "look", "looks", "looking", "seem", "seems", "am", "is", "are", "was",
    "were", "be", "being", "been", "much", "any", "lot", "sleep", "sleeping", "slept", "eat",
    "eating", "ate", "cope", "coping", "manage", "managing",
))
AFTER_COMPARATIVE = frozenset((
    "thanks", "thank", "today", "tomorrow", "yesterday", "now", "tonight", "though", "again",
    "yet", "already", "honestly", "actually", "here", "since", "after",
))
A_PERSON_AFTER = frozenset("""
    friend friends friend's friends' mate mates mate's pal pals man men woman women half buddy
    bud fella lad matey mother father sister brother son daughter partner wife husband
    wishes regards
""".split())
A_PERSON_NAMED = (A_PERSON_AFTER_A_POSSESSIVE | KIN | A_PERSON_AFTER
                  | frozenset("""boss bosses manager managers colleague colleagues
                      neighbour neighbours neighbor neighbors teacher teachers doctor
                      doctors gp dentist dentist's""".split()))
OWNS_A_PERSON = frozenset(("my", "our", "his", "her", "your", "their", "me"))
COMPARISON = re.compile(r"(?:\s+or\s+|\bbetter than\b|\binstead of\b|\bversus\b|\bvs\b)")


ASKS_IT_BACK = ("how about you", "what about you", "how about yourself", "what about yourself",
                "and you", "and yourself", "you yourself", "what about u", "how about u",
                "how about yours", "what about yours", "and yours")


FILLER_BEFORE = ("so", "ok", "okay", "oh", "yeah", "but", "well")
FILLER_AFTER = ("then", "though", "now", "anyway", "huh", "eh")
BOUT = {"bout": "about"}


def _ask_words(norm):
    words = [BOUT.get(word, word) for word in norm]
    while words and words[0] in FILLER_BEFORE:
        words.pop(0)
    while words and words[-1] in FILLER_AFTER:
        words.pop()
    return words


def _asks_it_back(norm):
    return " ".join(_ask_words(norm)) in ASKS_IT_BACK


GREETING_ASK_WORDS = frozenset("""
    how what whats is are was were am be been r u ya you your yours yourself yourselves the
    things everything life day days week weekend evening morning night
    going doing doin do been getting keeping saying say much
    today tonight then now lately anyway mate love friend
    all alright ok okay good fine well too so it have has having
""".split())
GREETING_ASK_SUBJECT = frozenset("""you u ya your yours yourself yourselves things everything
    life day days week weekend evening morning night""".split())
GREETING_ASK_STATE = frozenset("ok okay alright good fine well".split())
GREETING_ASK_ABOUT_SOMETHING = frozenset("with about to for if when on at in".split())
GREETING_ASK_SECOND_PERSON = frozenset("you u ya your yours yourself yourselves".split())
GREETING_WHAT_SAYING = frozenset("""what are is r you u ya saying say sayin then now there
    mate all""".split())


def asks_how_i_am(norm):
    while len(norm) > 2 and norm[-2] == "with" and norm[-1] in GREETING_ASK_SECOND_PERSON:
        norm = norm[:-2]
    if not norm or len(norm) > 8:
        return False
    words = set(norm)
    if not words & GREETING_ASK_SUBJECT:
        return False
    if norm[0] == "what":
        return words <= GREETING_WHAT_SAYING
    if norm[0] != "how":
        if len(norm) > 4 or not words & GREETING_ASK_STATE \
                or not words & GREETING_ASK_SECOND_PERSON:
            return False
        at = next(index for index, word in enumerate(norm) if word in GREETING_ASK_STATE)
        if not any(word in GREETING_ASK_SECOND_PERSON for word in norm[:at]):
            return False
        return not (len(norm) > at + 1 and norm[at + 1] in GREETING_ASK_ABOUT_SOMETHING)
    return words <= GREETING_ASK_WORDS


TAG_RIGHT_NOT = frozenset("""i me my mine you your yours he him his she her hers it its we us our
    ours they them their theirs this that these those there here what who which whose
    all any anything everything something nothing none both each either neither another
    such same very quite too so just still even only also always never ever really pretty
    probably maybe perhaps definitely certainly nearly almost exactly absolutely totally
    completely obviously clearly simply possibly surely indeed actually basically honestly
    literally truly about around much many more most less least enough not no yes yeah ok
    okay right
    is are was were am be been being do does did done have has had having can could will
    would shall should may might must need ought feel feels felt look looks looked seem
    seems seemed sound sounds sounded taste tastes tasted smell smells smelled get gets got
    gotten go goes went gone keep keeps kept turn turns turned make makes made put puts set
    sets work works worked
    off on out up down in back over through round around at
    fine ok okay alright good better worse ready done sorted""".split())
TAG_ENDINGS = frozenset(("right", "innit"))
TAG_PLAN = GOING_ON_WHEN | frozenset("""day days dinner lunch breakfast tea supper later soon
    next""".split())
TAG_TIME_NUMBER = frozenset("""one two three four five six seven eight nine ten eleven twelve
    half""".split())


TAG_CHECKABLE = frozenset("""should shouldnt shall can cant could couldnt will wont would wouldnt
    may might must ought needs need gets said says told tells""".split())


def _tag_tells_a_plan(norm):
    body = norm[:-1]
    if any(word in TAG_PLAN for word in body):
        return True
    return any(word == "at" and body[index + 1] in TAG_TIME_NUMBER
               for index, word in enumerate(body[:-1]))


def _tag_checks_a_fact(norm):
    body = norm[:-1]
    for index, word in enumerate(body[:-1]):
        if word in TAG_CHECKABLE and body[index + 1] == "be":
            return False
    return any(word in TAG_CHECKABLE for word in body)


def _asks_for_confirmation(norm):
    if len(norm) < 3 or norm[-1] not in TAG_ENDINGS:
        return False
    if (_opens_question(norm) or _asks_the_bot(norm) or _tag_tells_a_plan(norm)
            or not _tag_checks_a_fact(norm)):
        return False
    if norm[-1] == "right":
        if norm[-2].endswith(("ing", "ed")):
            return False
        return norm[-2] not in TAG_RIGHT_NOT
    return len(norm) >= 4


BOT_DAY_WORDS = "|".join(("day", "weekend", "week", "evening", "morning", "night"))
BOT_DAY_SHAPES = tuple(re.compile(pattern.format(day=BOT_DAY_WORDS)) for pattern in (
    r"(?:how|what) about (?:your|ur) (?:{day})(?: (?:been|going|gone|so far))?",
    r"(?:how|what) about yours",
    r"and (?:your|ur) (?:{day})(?: (?:been|going|gone|so far))?",
    r"and yours",
    r"(?:how|what)(?:s|'s| is| was| are| were) (?:your|ur) (?:{day})"
    r"(?: (?:been|going|gone|good|ok|okay|fine|busy|alright|so far))?",
    r"(?:was|were|is|are|did) (?:your|ur) (?:{day})(?: (?:good|ok|okay|fine|busy|alright|nice))?",
    r"(?:did|have|had) you have a (?:good|nice|ok|okay|busy|long|lovely|great) (?:{day})",
    r"hope (?:you had|youre having|you are having) a (?:good|nice|lovely|great|ok|okay) (?:{day})",
))


def _asks_about_the_bot_day(norm):
    words = _ask_words(norm)
    if not words:
        return False
    line = " ".join(words)
    return any(shape.fullmatch(line) for shape in BOT_DAY_SHAPES)


ASKS_IF_ANYTHING = frozenset("anything something nothing owt".split())
SPENDS_ITS_TIME = re.compile(
    r"\b(?:how|what)\b[^.]{0,24}?\b(?:spend|spends|spending|fill|fills|filling|use|uses)\b"
    r"[^.]{0,20}?\b(?:your|you)\b[^.]{0,16}\b(?:time|day|days|evening|evenings|hours?|"
    r"life|nights?)\b|\b(?:what do|what does)\s+you\s+do\s+(?:all\s+)?(?:day|with your|"
    r"during the|in the)\b")


def _asks_how_it_spends_its_time(norm):
    if not norm or len(norm) > 12:
        return False
    words = set(norm)
    if not words & {"you", "u", "ya", "your", "ur"}:
        return False
    return bool(SPENDS_ITS_TIME.search(" ".join(norm)))

ABOUT_AT_A_TIME = frozenset("""tonight tomorrow today later weekend weekends morning afternoon
    evening night now soon week""".split())
FREE_OR_BUSY = frozenset("busy free".split())
FIRST_PERSON = frozenset("i im id ive me my mine we us our".split())
MANNERS_WORDS = frozenset("up doing much keeps keeping".split())


def _asks_whether_the_bot_is_about(norm):
    if not norm or len(norm) > 6:
        return False
    words = set(norm)
    if not words & {"you", "u", "ya", "ur", "your"}:
        return False
    if words & FIRST_PERSON:
        return False
    if words & MANNERS_WORDS:
        return False
    return bool(words & ABOUT_AT_A_TIME) or bool(words & FREE_OR_BUSY)


MANNERS_OPENERS = frozenset("what whats wats".split())
WHEN_IN_THE_ASK = frozenset("""later tomorrow morning afternoon evening night weekend weekends
    week weekdays this these days coming soon next""".split())
SAYS_WHAT_ARE_YOU = frozenset("watcha whatcha wotcha watchu whatchu watchya whatchya".split())


KEEPS_BUSY_SHAPE = frozenset("""what whats wats is keeps keeping you u ya busy so then mate
    today tonight now lately these days though anyway""".split())


def the_manners_question(norm):
    lead = 0
    while lead < len(norm) and norm[lead] in UP_TO_LEADS:
        lead += 1
    norm = norm[lead:]
    if not norm or (norm[0] not in MANNERS_OPENERS and norm[0] not in SAYS_WHAT_ARE_YOU):
        return False
    words = set(norm)
    if not {"you", "u", "ya"} & words and norm[0] not in SAYS_WHAT_ARE_YOU:
        return False
    if "been" in words and {"do", "doing"} & words:
        return False
    if "busy" in words and {"keeps", "keeping"} & words:
        return words <= KEEPS_BUSY_SHAPE
    if not {"up", "doing", "doin", "do", "at", "been"} & words:
        return False
    if words & WHEN_IN_THE_ASK and not {"up", "doing", "doin", "at", "been"} & words:
        return False
    return all(word in DOING_FILLER or word in WHEN_IN_THE_ASK for word in norm)


NEW_ASK_WORDS = frozenset("""what whats is was has have u you ya your yours with in on going
    happening been new anything something nothing else tell me us mate pal friend hey hi hello
    so and now then lately world side day days weekend week""".split())
NEW_FRAME = frozenset("new going happening been".split())
NEW_ASK_AHEAD = frozenset("""tonight tomorrow later next saturday sunday monday tuesday
    wednesday thursday friday""".split())


def _asks_what_is_new_with_the_bot(norm):
    words = set(norm)
    if not words or len(norm) > 9:
        return False
    if not words & {"you", "u", "ya", "your", "yours"}:
        return False
    if not words & NEW_FRAME:
        return False
    if words & NEW_ASK_AHEAD:
        return False
    return words <= NEW_ASK_WORDS


def _asks_what_the_bot_is_doing(norm):
    if not norm or len(norm) > 10:
        return False
    if not ({"doing", "do"} & set(norm) or norm[-1] in ("to", "much", "on")
            or "up" in norm):
        return False
    if {"going", "on"} <= set(norm) and set(norm) & GOING_ON_WHEN:
        return False
    if all(word in DOING_FILLER for word in norm):
        return True
    return _asks_what_the_bot_has_been_doing(norm)


def _asks_what_the_bot_has_been_doing(norm):
    words = set(norm)
    if not words & {"you", "u", "ya", "your", "yours"}:
        return False
    if words & STILL_COMING:
        return False
    if not words & BEEN_SAID:
        return False
    if not words & {"did", "done", "been", "were", "was", "had"} and not words & BEEN_WHEN:
        return False
    if ("where" in words and words & SPENT_TIME
            and words & {"have", "has", "been", "were", "was"}):
        return True
    if not words & {"do", "does", "did", "done", "doing"}:
        return False
    return all(word in DOING_FILLER or word in BEEN_WHEN or word in BEEN_SAID for word in norm)


def _wants_a_recommendation(norm, text):
    if set(norm) & COMPARATIVE and COMPARISON.search(" " + text + " "):
        return True
    for index, word in enumerate(norm):
        if word not in COMPARATIVE:
            continue
        before = norm[index - 1] if index else ""
        after = norm[index + 1] if index + 1 < len(norm) else ""
        if after in A_PERSON_AFTER and not (
                after in ("man", "woman") and norm[index + 2:index + 3] == ["for"]):
            continue
        if before not in DESCRIBES and after not in AFTER_COMPARATIVE:
            return True
    return bool(set(norm) & (RECOMMEND - COMPARATIVE))


GRATITUDE_OBJECT = frozenset("""a an the all any some your his her their our my that this these
    those lot lots loads much very so really again both few bit kind sort great good helpful
    useful nice lovely brilliant ever indeed awfully terribly truly too help support""".split())
GRATITUDE_JOINERS = frozenset(["and", "plus", ",", "&"])
GRATITUDE_ASK_AGAIN = frozenset("any some what how which more another".split())
TIP_WORDS = frozenset("tips hints pointers tip hint pointer".split())
COURTESY_WORD = frozenset(word for phrase in THANKS for word in phrase.split())


def _the_thing_a_thank_you_is_for(norm):
    if not norm or not _starts_with(norm, THANKS):
        return None
    for at, word in enumerate(norm[:5]):
        if word != "for":
            continue
        if any(w not in COURTESY_WORD and w not in GRATITUDE_OBJECT for w in norm[:at]):
            continue
        end = at + 1
        while end < len(norm) and norm[end] in GRATITUDE_OBJECT | RECOMMEND | TIP_WORDS:
            if end > at + 1 and norm[end] in GRATITUDE_ASK_AGAIN:
                break
            end += 1
        if end > at + 1:
            while end + 1 < len(norm) and norm[end] in GRATITUDE_JOINERS:
                run = end + 1
                while run < len(norm) and norm[run] in GRATITUDE_OBJECT | RECOMMEND | TIP_WORDS:
                    run += 1
                if run == end + 1:
                    break
                if run < len(norm) and norm[run] == "for":
                    break
                end = run
            return at, end
    return None


def _asks(norm, text):
    thing = _the_thing_a_thank_you_is_for(norm)
    if thing:
        left = norm[:thing[0]] + norm[thing[1]:]
        return _ask_labels(left, " " + " ".join(left) + " ")
    return _ask_labels(norm, text)


A_DATE_FIGURE = re.compile(
    r"\b\d{1,2}(?:st|nd|rd|th)\b"
    r"|\b\d{1,2}\s+(?:of\s+)?(?:january|february|march|april|may|june|july|august|september|"
    r"october|november|december)\b"
    r"|\b(?:january|february|march|april|may|june|july|august|september|october|november|"
    r"december)\s+\d{1,2}\b",
    re.I)


def _a_bare_definition(text):
    found = BARE_DEFINITION.search(text)
    if not found:
        return False
    head = found.group(1).lower()
    if head.endswith(("'s", "\u2019s")) or re.search(r"\d", head):
        return False
    if re.match(r"\s*s\b", text[found.end():]):
        return False
    return head not in NOT_A_DEFINITION_HEAD


def _ask_labels(norm, text):
    asks = set()
    words = set(norm)
    if _asks_the_room(norm) and norm[1] in ASK_FOR_A_NAME:
        asks.add("recommend")
    if "how" in words:
        if "long" in words:
            asks.add("how_long")
        elif "much" in words or "many" in words:
            asks.add("how_much")
        elif "often" in words or "frequently" in words:
            asks.add("how_often")
        else:
            asks.add("how")
    for label in ("what", "why", "when", "where", "who", "which"):
        if label in words:
            asks.add(label)
    if _wants_a_recommendation(norm, text) or _has_any(text, RECOMMEND_PHRASES) \
            or _asks_for_tips(text, norm):
        asks.add("recommend")
    if _has_any(text, STEPS) or STEPS_WORD.search(text) or _asks_for_help(text):
        asks.add("steps")
    if _has_any(text, OPINION):
        asks.add("opinion")
    if _has_any(text, COMPARE) or words & {"vs", "versus"}:
        asks.add("compare")
    if not ASKS_ABOUT_A_PERSON.search(text) and (
            _has_any(text, DEFINITION) or _a_bare_definition(text)):
        asks.add("definition")
    digits = bool(re.search(r"\d", A_DATE_FIGURE.sub(" ", text)))
    if words & MATH_WORDS or "%" in text or (digits and ({"of", "each", "per", "split"} & words)):
        asks.add("maths")
    if _has_any(text, (" or ",)) and not two_ends_of_one_scale(text) \
            and not _turns_the_pair_down(text):
        asks.add("choice")
    if words & {"list", "ideas", "options", "examples", "suggest"}:
        asks.add("list")
    if words & {"write", "word", "rewrite", "draft"}:
        asks.add("write")
    if _asks_a_question_coming(norm, text):
        asks.add("question_coming")
    return sorted(asks)


NOUN_REQUEST_MAX = 8
PLACE_WORD = frozenset("in at near around from to".split())
NOUN_REQUEST_SELF = frozenset("""i me my mine we our us myself your you it its he she they
    there here that this""".split())
VERBISH = frozenset("""is are was were am be been being have has had do does did done go goes
    going went gone plan planning planned visit visiting visited stay staying live living work
    working like love hate want need get got take took make made book booked fly flying drive
    driving rent rented see saw seen eat ate eaten drink drank cook cooked watch watched play
    played read come came coming think thought know knew say said tell told try tried start
    started stop stopped leave left move moved should would could will can may might must""".split())


BARE_VERBS = frozenset("""do give get go try keep sort call tell know feel be been have wait
    stop start find leave come put use take see say think love like want""".split())
VERB_FORMS = BARE_VERBS | frozenset(
    stem[:-1] + "ing" if stem.endswith("e") else stem + "ing"
    for stem in VERBISH - {"is", "are", "was", "were", "am", "be", "been", "being"}
    if len(stem) > 2 and stem.isalpha())


def _third_person(stem):
    if len(stem) > 2 and stem.endswith("y") and stem[-2] not in "aeiouy":
        return stem[:-1] + "ies"
    if stem.endswith(("s", "sh", "ch", "x", "z", "o")):
        return stem + "es"
    return stem + "s"


VERB_THIRD = frozenset(
    _third_person(word) for word in (VERBISH | BARE_VERBS)
    if word.isalpha() and word not in {"is", "are", "am", "be", "been", "being"})


PAST_AUX = frozenset("""was were been had has have""".split())


def _verb_form(word, auxiliary=""):
    if word.endswith("ing") and auxiliary not in PAST_AUX:
        return False
    return word in VERB_FORMS


def noun_phrase_request(line):
    words = [word for word in line["norm"] if word]
    if not words or len(words) > NOUN_REQUEST_MAX or line["signals"]["question_mark"]:
        return False
    if any(word in NOUN_REQUEST_SELF for word in words):
        return False
    if any(word in VERBISH and words[index - 1:index] != ["to"]
           for index, word in enumerate(words)):
        return False
    return len(words) >= 2 and any(word in PLACE_WORD for word in words)


INTEREST_HEAD = re.compile(
    r"^\W*(?:i\s*m|im|i am|i\s*ve|ive|i have|we\s*re|were|we are|i\s+got|we\s+got)\s+"
    r"(?:really\s+|so\s+|very\s+much\s+|very\s+|well\s+|quite\s+|now\s+|also\s+"
    r"|totally\s+|still\s+)?"
    r"(?:(?:getting|got|started)\s+(?:back\s+)?|back\s+)?(?:into|in to)\s+(?P<thing>[a-z' -]+?)\s*[.!]*$",
    re.I)
INTEREST_NOT = frozenset("""not a an the this that these those some any my our his her their your
    him her them us me you it fight fights argument arguments row rows trouble debt debts
    hospital bed prison it him""".split())
INTEREST_TAIL = re.compile(
    r"\s+(?:at the moment|right now|now|these days|lately|recently|a lot|lots|again"
    r"|too|as well|also"
    r"|on\s+(?:mon|tues|wednes|thurs|fri|satur|sun)days?"
    r"|every\s+(?:day|week|weekend|morning|evening|night|"
    r"mon|tues|wednes|thurs|fri|satur|sun)days?"
    r"|at\s+the\s+weekend|after\s+work|in\s+the\s+evenings?)$", re.I)


STARTED_OUT = re.compile(r"\b(?:got|getting|started)\s+(?:back\s+)?into\b", re.I)


BACK_INTO = re.compile(r"\bback\s+into\b", re.I)


def taking_up(line, read=None):
    text = str((read or {}).get("clean") or line.get("text") or "")
    text = re.sub(r"['’]", "", text).strip()
    if not text or " not " in " %s " % text.lower():
        return None
    if re.match(r"\W*(?:am|is|are|was|were)\s+(?:i|we|you|they|he|she)\b", text, re.I):
        return None
    match = INTEREST_HEAD.match(text)
    if not match:
        return None
    thing = INTEREST_TAIL.sub("", match.group("thing").strip(" .,!?")).strip()
    words = thing.split()
    if not words or len(words) > 4:
        return None
    if words[0] in INTEREST_NOT or (len(words) > 1 and words[1] in INTEREST_NOT):
        return None
    thing = thing.lower()
    if not thing:
        return None
    return {"text": thing, "words": words,
            "shape": "started" if STARTED_OUT.search(text) else "doing",
            "back": bool(BACK_INTO.search(text))}


WH_CONTINUES = frozenset("which who whom whose that".split())
NOT_A_SUBJECT = frozenset(
    [word for phrase in GREETINGS + THANKS + FAREWELLS for word in phrase.split()]
    + list(ACK) + list(LAUGH)
    + "sorry please oh ah well right yes no yeah yep nope hmm and so but also just".split())
SUBJECT_OF_ITS_OWN = PRONOUNS | frozenset(
    """anyone someone everyone nobody anybody somebody one""".split())


def _bare_subject(clause):
    if not clause:
        return False
    for word in clause:
        if word in VERBISH or (len(word) > 3 and word.endswith(("ed", "ing"))):
            return False
    first = clause[0]
    if first in DETERMINERS:
        return True
    return len(clause) == 1 and first not in NOT_A_SUBJECT


def _continues_the_sentence(clauses, index):
    if index < 1 or not _bare_subject(clauses[index - 1]):
        return False
    clause = clauses[index]
    if any(word in SUBJECT_OF_ITS_OWN for word in clause[1:3]):
        return False
    if clause[0] in WH_CONTINUES:
        return True
    if clause[0] not in YESNO_STARTS:
        return False
    return index >= 2 and _bare_subject(clauses[index - 2])
NEGATORS = frozenset("""not no never neither nor hardly barely cannot cant dont doesnt didnt
    isnt arent wasnt werent wont wouldnt shouldnt couldnt aint nothing""".split())
NEGATION_SKIP = frozenset("""really very so too much quite pretty true honestly actually
    totally completely absolutely seriously still even at all bit little kind sort feeling
    feel felt a an the""".split())

DENY_BETWEEN = NEGATION_SKIP | frozenset("""in at on for under any more most all about much
    having had havent been being be am is are was were got get getting a an the""".split())
DENY_BEFORE = re.compile(
    r"\b(?:" + "|".join(sorted(NEGATORS)) + r")\b"
    r"(?:\s+(?:" + "|".join(sorted(DENY_BETWEEN)) + r")){0,4}\s*$", re.I)


def denied(text, cue):
    for match in re.finditer(r"\b" + re.escape(cue) + r"\b", text):
        if DENY_BEFORE.search(text[:match.start()]):
            return True
    return False


def _a_state_of_the_speaker(norm, index):
    verb = False
    back = index - 1
    while back >= 0 and index - back <= 4:
        word = norm[back]
        if word in SPEAKER:
            return verb
        if word in STATING_VERB:
            verb = True
        elif word not in NEGATORS and word not in NEGATION_SKIP:
            return False
        back -= 1
    return False


SUMMONS_WHO = frozenset("""
teacher teachers head headteacher headmaster headmistress school nursery college tutor lecturer
boss manager supervisor employer hr payroll council housing landlord lettings letting agency
dwp benefits tax hmrc bank gp doctor surgery dentist hospital consultant midwife police
probation court solicitor immigration ofsted office
""".split())
SUMMONS_WHO_PHRASES = ("social services", "health visitor", "home office", "tax office",
                       "job centre", "jobcentre", "letting agent", "letting agents",
                       "the council", "the school", "the office", "the bank", "the head")
SUMMONS_SEE = ("a word", "a quick word", "to see", "to talk", "a chat", "a meeting", "to meet",
               "to discuss", "to speak", "to come in", "asked me in", "called me in",
               "for a chat", "an appointment", "to interview")
SUMMONS_WRITTEN = ("written to me", "wrote to me", "sent me a letter", "sent a letter",
                   "a letter from", "letter arrived", "letter came", "in writing")
LETTER_RECEIVED = frozenset("""got received had came come arrives arrived""".split())
LETTER_ASKED_FOR = frozenset("""need needs wanted want wants asked ask asking sent send
    sending wrote write writing expecting waiting chase chased requested requesting
    wanting""".split())
LETTER_SOMEONE_ELSES = frozenset("my his her their our".split())
LETTER_ITSELF = frozenset("letter letters note email reply".split())
SUMMONS_RANG = ("rang me", "phoned me", "called me", "left a message", "rang about",
                "phoned about", "called about", "rang the house")
SUMMONS_CALL_DONE = frozenset("""back today yesterday tonight morning afternoon evening
    earlier already just then""".split())
SUMMONS_SAID = frozenset("said says told tells explained apologised apologized asked confirmed""".split())
SUMMONS_WANTS = ("want", "wants", "wanted", "needs", "needed", "asked", "asking",
                 "would like", "requested", "told me")
SUMMONS_VERB = frozenset(SUMMONS_WANTS) | frozenset("""written wrote rang phoned called sent
    letter message""".split())
SUMMONS_NOT = frozenset("""not hasnt havent didnt doesnt dont wont never no still yet""".split())


def _asks_for_it_rather_than_got_it(norm):
    arrived = next((index for index, word in enumerate(norm)
                    if word in LETTER_RECEIVED), None)
    if arrived is None:
        return False
    return any(word in LETTER_ASKED_FOR for word in norm[:arrived + 1])


def _a_letter_someone_else_got(norm, verb):
    for index, word in enumerate(norm[:verb]):
        if word in LETTER_SOMEONE_ELSES:
            after = norm[index + 1] if index + 1 < len(norm) else ""
            if after and after not in LETTER_ITSELF:
                return True
    return False


def summons_of(norm, kind):
    if not norm or kind == "question":
        return None
    words = set(norm)
    who = None
    at = None
    for phrase in SUMMONS_WHO_PHRASES:
        if phrase in " ".join(norm):
            who = phrase
            at = norm.index(phrase.split()[0])
            break
    if who is None:
        who = next((word for word in norm if word in SUMMONS_WHO), None)
        at = norm.index(who) if who else None
    if who is None:
        return None
    verb = next((index for index, word in enumerate(norm)
                 if word in SUMMONS_VERB and word not in ("has", "have")), None)
    if verb is None:
        verb = next((index for index, word in enumerate(norm) if word in SUMMONS_VERB), None)
    joined = " " + " ".join(norm) + " "
    letter_first = (verb is not None and at > verb
                    and any(phrase in joined for phrase in SUMMONS_WRITTEN)
                    and any(word in LETTER_RECEIVED for word in norm)
                    and not _asks_for_it_rather_than_got_it(norm)
                    and not _a_letter_someone_else_got(norm, verb))
    if verb is None or (at > verb and not letter_first):
        return None
    if any(word in SUMMONS_NOT for word in norm[max(0, verb - 3):verb]):
        return None
    if letter_first or any(phrase in joined for phrase in SUMMONS_WRITTEN):
        return {"who": who, "shape": "written"}
    rang = next((phrase for phrase in SUMMONS_RANG if phrase in joined), None)
    if rang:
        gap = joined.split(rang, 1)[1].split()[:3]
        if not set(gap) & SUMMONS_CALL_DONE and not set(gap) & SUMMONS_SAID:
            return {"who": who, "shape": "rang"}
    if not words & set(SUMMONS_WANTS):
        return None
    if any(phrase in joined for phrase in SUMMONS_SEE):
        return {"who": who, "shape": "see"}
    return None


def _said_to_somebody(norm, index):
    if index != len(norm) - 1 or not 2 <= len(norm) <= 3:
        return False
    return norm[0] in ADDRESSED_LINES

STOMACH_WORDS = frozenset("""stomach stomachs tummy tummies belly bellies gut guts bowel bowels
    insides""".split())
BODY_STATE_WORDS = frozenset("upset".split())


def _a_body_not_a_mood(norm, index):
    forward = norm[index + 1] if index + 1 < len(norm) else None
    return forward in STOMACH_WORDS

BACK_AT = frozenset("you yourself u urself ya".split())
BACK_JOIN = frozenset("and about".split())
BACK_ASKING = frozenset(("what", "how"))
BACK_NOT_A_SUBJECT = frozenset("me us him her them i we my our your".split())
BACK_AFTER = frozenset("""thanks cheers ta ok okay alright fine good great well grand sound
    chill brill mint content lovely nice brilliant wonderful perfect amazing fantastic happy glad
    relaxed calm not bad tired rough meh shattered knackered wrecked awful terrible so very
    really doing feeling mate man
    complain same always
    working work busy off home out just finishing finishing up sorted done""".split())


def _asks_what_was_meant(text):
    asked = str(text or "").strip()
    if not asked:
        return False
    from ..memory import meant

    return bool(meant.MEAN.match(asked))


MEANT_APPLIED_TO = re.compile(r"\bfor\s+(?:my|our)\s+([a-z'\u2019-]+)", re.I)


def _asks_back(norm):
    words = [word for word in norm if word]
    if len(words) < 2 or words[-1] not in BACK_AT:
        return False
    if (len(words) == 2 and words[0] in BACK_JOIN) or \
            (len(words) == 3 and words[0] in BACK_ASKING and words[1] in BACK_JOIN):
        return True
    if len(words) > 2 and words[-3] in BACK_NOT_A_SUBJECT:
        return False
    if any(word in BACK_AT or word in {"youre", "your"} for word in words[:-1]):
        return False
    if words[-2] == "about" and not any(word in BACK_ASKING for word in words[:-2]):
        return False
    if words[-2] in BACK_JOIN:
        return (_polarity(norm) != 0 or emotion_of(" ".join(words)) is not None
                or any(word in BACK_AFTER for word in words[:-2]))
    return words[-2] in BACK_AFTER


def says_how_they_are(norm):
    return any(word in SAYS_HOW_THEY_ARE and _a_state_of_the_speaker(norm, index)
               for index, word in enumerate(norm))


VERDICT_NOUNS = frozenset("""joke nightmare disaster shambles mess farce ripoff con
    circus zoo mockery sham travesty letdown disappointment pain drag headache minefield
    slog waste fiasco scandal pantomime horror""".split())
COPULAS = frozenset("is are was were am be being been becomes became".split())
VERDICT_FILLER = frozenset("""a an the total complete absolute utter right proper real massive
    huge bloody bit of on one big fat""".split())
VERDICT_ADJECTIVES = frozenset("""useless pointless hopeless rubbish crap shit shite garbage
    trash pathetic""".split())
PRONOUN_SUBJECT = frozenset("it that this there he she they we i you".split())
ASKING_SUBJECT = frozenset("""what which who whom whose how why when where whatever whoever
    whichever whenever wherever""".split())
NOT_A_THING = frozenset("""week weekend day month year morning evening night afternoon term
    shift holiday trip time""".split())


def a_bad_verdict(norm, index):
    if index >= len(norm) or (norm[index] not in VERDICT_NOUNS
                             and norm[index] not in VERDICT_ADJECTIVES):
        return False
    back = index - 1
    while back >= 0 and norm[back] in VERDICT_FILLER:
        back -= 1
    if back < 0 or norm[back] not in COPULAS:
        return False
    subject = back - 1
    if (subject < 0 or norm[subject] in PRONOUN_SUBJECT or norm[subject] in ASKING_SUBJECT
            or norm[subject] in COPULAS or norm[subject] in NOT_A_THING):
        return False
    return True


def verdicts_a_thing(clean):
    text = " ".join(str(clean or "").lower().replace("\u2019", "'").replace("'", "").split())
    norm = [word for word in (re.sub(r"[^a-z0-9]+", "", part) for part in text.split()) if word]
    return any(a_bad_verdict(norm, index) for index in range(len(norm)))


def _polarity(norm):
    score = 0
    negated = False
    for index, word in enumerate(norm):
        if word in NEGATORS:
            negated = True
            continue
        if word in TERMS_OF_ADDRESS and _said_to_somebody(norm, index):
            negated = False
            continue
        if word in OK_WORDS or word in SAYS_HOW_THEY_ARE:
            feeling = 1 if _a_state_of_the_speaker(norm, index) else None
        elif word in POSITIVE:
            feeling = 1
        elif word in NEGATIVE:
            feeling = (-1 if word not in BODY_STATE_WORDS or not _a_body_not_a_mood(norm, index)
                       else None)
        elif a_bad_verdict(norm, index):
            feeling = -1
        else:
            feeling = None
        if feeling is None:
            if word not in NEGATION_SKIP:
                negated = False
            continue
        score += -feeling if negated else feeling
        negated = False
    return (score > 0) - (score < 0)


def _thanks_still_asks(norm):
    words = list(norm)
    for index, word in enumerate(words):
        if word not in THANKS_ASK_WORDS:
            continue
        back = words[index - 1] if index else ""
        if back in GIVEN_ADVICE:
            continue
        return True
    for index, word in enumerate(words):
        if word not in THANKS_ASK_NOUNS:
            continue
        back = words[index - 1] if index else ""
        if back in GIVEN_ADVICE:
            continue
        if (index + 2 < len(words) and words[index + 1] in THANKS_ASK_PREPS
                and words[index + 2].isalpha()):
            return True
    return False


PICKING = frozenset("""best better cheapest cheaper good great nice decent place places way ways
    time times thing things option options spot spots area areas""".split())
TO_A_VERB = re.compile(r"\bto\s+[a-z]+", re.I)
SAYS_WHAT_IT_IS = frozenset("""is are was were am im i'm its it's be been""".split())


OPENS_A_FRAME = frozenset("""the a an any some and also best better cheapest cheaper good great
    nice decent""".split())

PICKING_QUALITY = frozenset("best better cheapest cheaper good great nice decent".split())


def _only_the_ask(norm, asks, text):
    words = [word for word in norm if word not in POLITE]
    if not words or len(words) > 8:
        return False
    if set(words) & (SPEAKER | SAYS_WHAT_IT_IS):
        return False
    if words[0] not in OPENS_A_FRAME:
        return False
    if not set(words) & PICKING or not TO_A_VERB.search(str(text)):
        return False
    return bool(asks) or bool(set(words) & PICKING_QUALITY)


def classify(line):
    text = line["norm_text"]
    norm = line["norm"]
    words = set(norm)
    signals = line["signals"]

    clauses = line["clauses"]
    opens_like_question = any(_opens_question(clause) and not _continues_the_sentence(clauses, at)
                              for at, clause in enumerate(clauses))
    asks = _asks(norm, " " + text + " ")
    turned_back = _asks_it_back(norm) or _asks_about_the_bot_day(norm)
    tag = _asks_for_confirmation(norm)

    kind = "statement"
    courtesy = without_filler(norm)
    if not norm:
        kind = "empty"
    elif (signals["question_mark"] or _opens_question(norm) or opens_like_question
          or _asks_the_bot(norm) or _asks_for_help(text) or tag or _asks_after_any(norm)
          or (asks and _starts_with(norm, THANKS)
              and (signals["question_mark"] or set(norm) & QUESTION_WORDS
                   or _thanks_still_asks(norm)))):
        kind = "question"
    elif _only_the_ask(norm, asks, text):
        kind = "question"
        asks = sorted(set(asks) | {"recommend"})
    elif _starts_with(norm, GREETINGS) and greeting_only(norm):
        kind = "greeting"
    elif ((_starts_with(courtesy, THANKS) and _thanks_only(courtesy, clauses))
          or _says_the_help_was_good(norm)):
        kind = "thanks"
    elif _ends_with_thanks(courtesy):
        kind = "thanks"

    if turned_back:
        asks = []
    if kind != "question":
        behind = {norm[index] for index in background_clause(norm) | background_positions(norm)}
        asks = [ask for ask in asks if ask not in behind]
    if kind == "question" and (
            (not turned_back
             and any(strip_leaders(clause)[:1] and strip_leaders(clause)[0] in YESNO_STARTS
                     for clause in line["clauses"]))
            or tag):
        asks = sorted(set(asks) | {"yesno"})
    short = len(norm) <= 3
    bare = [word for word in norm if word not in POLITE]
    denied_bad = {word for word in words if word in NEGATIVE and denied(text, word)}

    intent = "statement"
    if kind == "empty":
        intent = "empty"
    elif signals["laughter"] and len(norm) <= 5:
        intent = "laugh"
    elif _starts_with(strip_leaders(norm), FAREWELLS) and farewell_only(strip_leaders(norm)):
        intent = "farewell"
    elif _about_bot(text, words, norm):
        intent = "about_bot"
    elif kind == "greeting":
        intent = "greeting"
    elif kind == "thanks":
        intent = "thanks"
    elif _has_any(" " + text + " ", CORRECTION) and ("meant" in words or "mean" in words):
        intent = "correction"
    elif (_asks_it_back(norm) or _asks_about_the_bot_day(norm)
          or _asks_what_the_bot_is_doing(norm) or the_manners_question(norm)
          or asks_how_i_am(norm)):
        intent = "smalltalk"
    elif agreement_of(text):
        intent = "ack"
    elif _short_reply(text) and len(norm) <= 6:
        intent = "ack"
    elif kind == "statement" and _agrees_to_try(norm):
        intent = "ack"
    elif (norm[0] in {"no", "nah", "nope", "never"} and len(norm) <= 5
          and norm[1:2] != ["one"]):
        intent = "deny"
    elif norm[0] in ACK and len(norm) <= 4:
        intent = "ack"
    elif len(bare) <= 3 and set(bare) <= AFFIRM:
        intent = "affirm"
    elif len(bare) <= 3 and set(bare) <= DENY:
        intent = "deny"
    elif len(bare) <= 3 and (set(bare) <= ACK or set(bare) <= LAUGH):
        intent = "ack"
    elif small_talk_only(norm):
        intent = "smalltalk"
    elif kind == "question":
        intent = "question"
    elif ("recommend" in asks or _asks_for_tips(text, norm) or _has_any(text, STEPS)
          or words & {"help", "need", "want"}):
        intent = "request"
    elif norm[:1] and norm[0] in {"tell", "explain", "show", "give", "write", "make"}:
        intent = "request"
    elif "i" in words and (any(w in NEGATIVE or w in POSITIVE for w in words
                                  if w not in denied_bad)
                            or says_how_they_are(norm)):
        intent = "feeling"
    elif ("i" in words or _acts_on_the_speaker(text)) and emotion_of(text):
        intent = "feeling"
    elif _has_any(" " + text + " ", NEWS):
        intent = "news"
    elif {"i", "me", "my", "we", "our"} & words and (words & EVENT_WORDS or len(norm) <= 12):
        intent = "news"
    elif _has_any(text, OPINION) or (words & {"think"} and kind == "question"):
        intent = "opinion"

    state_owner = _state_owner(line["clauses"])
    limit = _limit_of(text)
    suggestion = _a_suggestion_from_someone(norm, text)
    ruled_out = _ruled_out_of(text)
    emotion = None
    if "i" in words or "im" in words or "my" in words or kind != "question":
        emotion = emotion_of(text)
    if state_owner in (None, "thing") and _somebody_elses_heart(text):
        state_owner = "other"
    if emotion and state_owner in (None, "thing") and _a_broken_heart_is_theirs(text):
        state_owner = "self"
    if not emotion and _a_hedged_low(line.get("clean") or text):
        emotion = "sad"
        if state_owner in (None, "thing"):
            state_owner = "self"
    polarity = _polarity(norm)
    shortage = shortage_of(text)
    if shortage and emotion is None:
        state_owner = None

    return {
        "kind": kind,
        "intent": intent,
        "asks": asks,
        "tag": tag,
        "emotion": emotion,
        "state_owner": state_owner,
        "shortage": shortage,
        "polarity": polarity,
        "short": short,
        "first_person": bool(words & {"i", "me", "my", "we", "our", "us", "myself"}),
        "asks_opinion": "opinion" in asks,
        "asks_recommendation": "recommend" in asks,
        "asks_steps": "steps" in asks,
        "help_ask": _asks_for_help(text),
        "asks_a_verdict": _asks_a_verdict(text),
        "about_bot": intent == "about_bot",
        "about_bot_kind": (_about_bot_kind(text, words, norm)
                           if intent == "about_bot" else None),
        "counts_the_bots_own_day": _counts_its_own_doings(norm),
        "replies_to_bot": intent in ("affirm", "deny", "ack", "laugh"),
        "agrees_to_try": _agrees_to_try(norm),
        "wants_a_quiz": _hands_a_question_to_the_speaker(norm),
        "agreement": agreement_of(text),
        "summons": summons_of(norm, kind),
        "asks_back": _asks_back(norm),
        "asks_what_was_meant": _asks_what_was_meant(text),
        "excludes": [limit] if limit else [],
        "ruled_out": ruled_out,
        "constraint": limit is not None,
        "suggestion": suggestion,
    }


ROUTINE_SHAPE = re.compile(
    r"\b(?:every (?:day|week|month|morning|evening|afternoon|night|weekend|other day)|"
    r"every (?:mon|tues|wednes|thurs|fri|satur|sun)day|"
    r"each (?:day|week|morning|evening)|most (?:days|weeks|mornings|evenings)|"
    r"(?:once|twice|three times|four times|a few times) a (?:day|week|month)|"
    r"on (?:a|an) (?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)|"
    r"at the weekend)\b", re.I)
ROUTINE_IS_A_FAULT = re.compile(
    r"\b(?:pain|pains|\w*ache|\w*aches|aching|hurts?|hurting|sore|sick|ill|unwell|worse|worst|"
    r"worried|anxious|panic|cry|crying|cried|shout|shouting|shouted|argue|arguing|fight|"
    r"fighting|bleed|bleeding|blood|swollen|rash|fever|cough|coughing|vomit|vomiting|"
    r"dizzy|numb|sneeze|sneezing|stopped|stopping|wont stop|won't stop|leak|leaking|"
    r"broken|broke|craving|crave)\b", re.I)
ROUTINE_IN_THE_PAST = re.compile(r"\b(?:used to|didn'?t use to|would (?:always |often )?\w+|"
                                 r"back then|years ago|in those days)\b", re.I)
_ROUTINE_SUBJECT = re.compile(r"^\s*(?:and\s+|so\s+|well\s+|oh\s+)?(?:i|i(?:'m|ve|d)|we|we(?:'re|ve))\b",
                              re.I)


SHIFT_LATE = re.compile(
    r"\b(?:(?:i|we|im|i'm|we're|were)\s+)?(?:am|are|'m|'re|was|were)?\s*"
    r"(?:on|back on|working|work|doing|do)\s+(?:the\s+)?(?:lates|late shifts?)\b"
    r"|\bon (?:the )?lates\b|\blates (?:all|this|next|every|for)\b|\blate shifts?\b", re.I)
SHIFT_EARLY = re.compile(
    r"\b(?:(?:i|we|im|i'm|we're|were)\s+)?(?:am|are|'m|'re|was|were)?\s*"
    r"(?:on|back on|working|work|doing|do)\s+(?:the\s+)?(?:earlies|early shifts?)\b"
    r"|\bon (?:the )?earlies\b|\bearlies (?:all|this|next|every|for)\b|\bearly shifts?\b",
    re.I)
SHIFT_NIGHT = re.compile(
    r"\b(?:night shifts?|on nights|work(?:ing)? nights|nights this week)\b", re.I)


def shift_worked(text):
    text = text if isinstance(text, str) else ""
    if SHIFT_NIGHT.search(text):
        return "night"
    if SHIFT_LATE.search(text):
        return "late"
    if SHIFT_EARLY.search(text):
        return "early"
    return None


A_REPORTED_VERB = re.compile(
    r"\b(?:said|says|say|told|tells|tell|reckons?|reckoned|thinks?|thought|suggests?|suggested|"
    r"recommends?|recommended|advises?|advised|insists?|insisted|keeps? (?:saying|telling me)|"
    r"wants? me to|wanted me to|nagged? me to|pushing me to|going on at me to)\b", re.I)
A_SUGGESTED_CLAUSE = re.compile(
    r"\b(?:i|we) (?:should|shouldnt|shouldn't|ought|need|needed|have) (?:to )?"
    r"|\b(?:told|asked|tells|asks|wants?|wanted|nagged|pushing|pushed) me to\b"
    r"|\b(?:i would|id|i'd) (?:like|love|rather|be better|better off)\b", re.I)
A_TOLD_TO = re.compile(r"\b(?:was|were|am|im|been|be|got) told to\b", re.I)
A_NOT_A_SUGGESTION = re.compile(
    r"\b(?:shouldnt|shouldn't|should not|ought not|dont bother|don't bother|no point in|"
    r"not worth (?:it|the|bothering)|wait and see|sit tight|hold off|hang on|leave it for now|"
    r"think about it)\b", re.I)
A_SAID_BY = re.compile(
    r"\b(?:my|the|a|an|our|his|her|their) (?:[\w'-]+ ){0,2}?"
    r"(?:mate|friend|mum|mom|mam|mother|dad|father|sister|brother|wife|husband|partner|son|"
    r"daughter|gran|nan|grandma|grandad|neighbour|neighbor|colleague|coworker|boss|manager|"
    r"doctor|gp|nurse|physio|physiotherapist|consultant|surgeon|midwife|dentist|pharmacist|"
    r"therapist|counsellor|counselor|trainer|coach|teacher|tutor|landlord|lads|girls|bloke|"
    r"fella|chap|someone|somebody)\b", re.I)
A_SAID_BY_ANYONE = re.compile(r"\b(?:everyone|everybody|people|they|he|she)\b", re.I)


def _a_suggestion_from_someone(norm, text):
    said = " " + " ".join(norm) + " "
    report = A_REPORTED_VERB.search(said)
    if not report:
        return None
    if not (A_SUGGESTED_CLAUSE.search(said, report.start()) or A_TOLD_TO.search(said)):
        return None
    if A_NOT_A_SUGGESTION.search(said):
        return None
    before = said[:report.start()]
    named = None
    for found in A_SAID_BY.finditer(before):
        named = found.group(0).strip()
    if named:
        words = named.split()
        if words[0] in ("my", "our"):
            words[0] = "your"
        who = " ".join(words)
    elif A_SAID_BY_ANYONE.search(before):
        who = ""
    else:
        who = ""
    return {"who": who[:1].upper() + who[1:], "source": named or ""}


def is_a_routine(line, read=None):
    read = read or {}
    if read.get("kind") not in ("statement", "news", None):
        return False
    if read.get("asks"):
        return False
    text = str(line.get("plain") or line.get("clean") or line.get("text") or "").strip()
    if not text or text.endswith("?"):
        return False
    if not _ROUTINE_SUBJECT.match(text):
        return False
    if ROUTINE_IS_A_FAULT.search(text) or ROUTINE_IN_THE_PAST.search(text):
        return False
    return bool(ROUTINE_SHAPE.search(text))


CARE_HOME_PLACE = re.compile(
    r"\b(?:in|into|at)\s+(?:a|the)\s+(?:care\s+|nursing\s+|residential\s+)?home\b", re.I)
CARE_HOME_NOT = re.compile(r"\b(?:work|works|working|worked|stay|staying)\s+from\s+home\b"
                           r"|\bhome\s+(?:town|office|made|birth|baked)\b", re.I)
CARE_HOME_KIN = frozenset("""nan nana mam mammy mate mates grannie grandaddy mother-in-law
    father-in-law sister-in-law brother-in-law son-in-law daughter-in-law""".split())
CARE_HOME_MOVED = re.compile(r"\b(?:moved|moves|moving|went|goes|gone|going|put|puts|putting"
                             r"|decided|decision|agreed|arranged|sorted)\b", re.I)
CARE_HOME_VISIT = re.compile(r"\b(?:visit|visits|visiting|visited|see|seeing|saw|"
                             r"bring|brings|bringing|brought|take her|take him|take them)\b", re.I)
CARE_HOME_GUILT = re.compile(r"\b(?:guilt|guilty|selfish|should have|shouldve|my fault|blame"
                             r"|couldnt cope|could not cope|no choice|heartbroken|awful)\b", re.I)


CARE_HOME_BRING_ASKS = re.compile(
    r"\b(?:what|anything|something|whats|should i|shall i|can i|could i|do i|did i|"
    r"is there anything)\b", re.I)
CARE_HOME_BRING_WORD = re.compile(r"\b(?:bring|brings|bringing|take|takes|taking)\b", re.I)
CARE_HOME_BRING_WHO = re.compile(r"\b(?:her|him|them|she|he|they)\b", re.I)


def a_home_carried_forward(text, earlier_lines):
    line = re.sub(r"['\u2019]", "", str(text or "")).strip()
    if not line or a_care_home(line):
        return None
    if not (CARE_HOME_BRING_ASKS.search(line) and CARE_HOME_BRING_WORD.search(line)
            and CARE_HOME_BRING_WHO.search(line)):
        return None
    for earlier in reversed(list(earlier_lines or ())):
        read = a_care_home(earlier)
        if read:
            carried = dict(read)
            carried["shape"] = "bring"
            carried["carried"] = str(earlier)
            return carried
    return None


def a_care_home(text):
    from .topics import RELATIONS
    line = re.sub(r"['\u2019]", "", str(text or "")).strip()
    if not line or not CARE_HOME_PLACE.search(line) or CARE_HOME_NOT.search(line):
        return None
    lowered = line.lower()
    who, relation = "", None
    for match in re.finditer(r"\b(?:my|our|your)\s+([a-z][a-z-]*)", lowered):
        if match.group(1) in RELATIONS or match.group(1) in CARE_HOME_KIN:
            relation = match.group(1)
            who = " ".join(match.group(0).split())
            break
    if not who:
        for word in ("shes", "hes", "she", "he", "they", "theyre"):
            if re.search(r"\b%s\b" % word, lowered):
                who = word
                break
    if not who:
        return None
    if relation in ("husband", "father", "dad", "son", "brother", "uncle", "cousin", "grandad",
                    "grandpa", "grandfather", "granddad", "partner", "boyfriend", "friend",
                    "male friend", "nephew", "stepdad", "stepfather"):
        pronoun = "he"
    elif relation in ("wife", "mother", "mum", "mom", "daughter", "sister", "aunt", "gran",
                      "granny", "grandma", "grandmother", "partner", "girlfriend", "friend",
                      "niece", "stepmum", "stepmother", "nan", "nana", "mam", "mammy",
                      "grannie", "mother-in-law", "sister-in-law", "daughter-in-law"):
        pronoun = "she"
    elif relation in ("kids", "children", "child", "parents", "friends", "mates", "mate"):
        pronoun = "they"
    elif who in ("he", "hes"):
        pronoun = "he"
    elif who in ("she", "shes"):
        pronoun = "she"
    else:
        pronoun = "they"
    if relation in ("kids", "children", "parents", "friends"):
        pronoun = "they"
    if CARE_HOME_GUILT.search(lowered):
        shape = "guilt"
    elif CARE_HOME_VISIT.search(lowered):
        shape = "visiting"
    elif CARE_HOME_MOVED.search(lowered):
        shape = "moved"
    else:
        shape = "in"
    return {"text": " ".join(CARE_HOME_PLACE.search(line).group(0).split()),
            "who": who, "relation": relation, "pronoun": pronoun, "shape": shape}



_MONEY_NOUN = re.compile(
    r"\b(?:price[sd]?|pricing|cost[s]?|costing|charge[sd]?|fare[s]?|fee[s]?|rent|rental|"
    r"salary|salaries|wage[s]?|expensive|cheaper|cheapest|cheap|how\s+much\s+money)\b")
_A_PRICE_ASK = re.compile(
    r"\bhow\s+much\s+(?:is|are|was|were|will|would|does|do|did|should|can|could|might|"
    r"is\s+it|do\s+they|do\s+you|do\s+i|does\s+it)\b|"
    r"\bprice[sd]?\s+(?:of|for|on)\b|\bcost\s+of\b|"
    r"\bwhats?\s+(?:the\s+)?(?:price|cost|charge|fare|fee|rent)\b|"
    r"\bwhat\s+(?:is|are)\s+the\s+(?:price|cost|charge|fare|fee|rent)\b|"
    r"\bwhat\s+(?:does|do|will|would|should)\b[^?]{0,30}?\b(?:cost|charge)\b|"
    r"\bwhats?\s+(?:it|that|this|they|one)\s+worth\b|\bhow\s+much\s+(?:money|for)\b|"
    r"\bcheapest\b|\bdeals?\s+on\b|\bon\s+offer\b|\bdiscount(?:s|ed)?\b|"
    r"\b(?:anything|something|any|some)\s+(?:a\s+bit\s+|much\s+)?cheaper\b|"
    r"\bis\s+(?:there|that|it)\s+cheaper\b|\bcheaper\s+(?:than|option|ones?|deal)\b|"
    r"\bprice\s+match\b|"
    r"\b(?:cheaper|more\s+expensive|dearer|pricier|costlier|better\s+value)\b|"
    r"\b(?:going|market|typical|average|usual|standard|ballpark)\s+"
    r"(?:rate|price|cost|fee|charge)\b")
_A_POST_HOLDER = re.compile(
    r"\bwho(?:s|\s+is|\s+are)?\s+(?:the\s+|our\s+)?(?:prime\s+minister|pm|president|"
    r"chancellor|home\s+secretary|first\s+minister|mayor|mp|meps?|ceo|chief\s+executive|"
    r"head\s+teacher|manager|coach|owner|chair(?:man|woman|person)?)\b"
    r"(?![^?]*\b(?:of\s+the\s+year|ever|all\s+time|alive|dead)\b)")
_A_HOW_MUCH_I_SPENT = re.compile(
    r"\bhow\s+much\s+(?:did|have|has|do)\s+(?:i|we)\s+(?:spend|spent|pay|paid|earn|earned|"
    r"save|saved)\b")
_A_MY_OWN_FIGURE = re.compile(
    r"\b(?:am|do|will|would|should|have|did|can)\s+i\s+(?:be\s+)?(?:paying|charged|billed|"
    r"spending|getting\s+charged)\b|"
    r"\bmy\s+(?:own\s+)?(?:bill|bills|subscription|subscriptions|account|card|statement|"
    r"tariff|contract|plan|direct\s+debit|standing\s+order|invoice|receipt|payslip|quota|"
    r"allowance)\b")
_MONEY = re.compile(
    r"\b(?:dollars?|euros?|quid|cents?|yen|rupees?|pence|money|cash)\b")
_UNITS = (r"g|kg|kilos?|kilograms?|grams?|oz|ounces?|lbs?|pounds?|ml|l|millilit(?:re|er)s?|"
          r"litres?|liters?|cups?|tbsp|tsp|"
          r"tablespoons?|teaspoons?|celsius|fahrenheit|centigrade|degrees|stone|inches?|inch|"
          r"cm|mm|metres?|meters?|feet|foot|ft|miles?|km|yards?|pints?|quarts?|gallons?")
_UNITS_BOUGHT = (r"g|kg|kilos?|kilograms?|grams?|oz|ounces?|lbs?|ml|l|millilit(?:re|er)s?|"
                 r"litres?|liters?|cups?|tbsp|tsp|"
                 r"tablespoons?|teaspoons?|celsius|fahrenheit|centigrade|degrees|stone|"
                 r"inches?|inch|cm|mm|metres?|meters?|feet|foot|ft|miles?|km|yards?")
_A_AN_AMOUNT_OF_A_THING = re.compile(
    r"\b\d+\s*(?:" + _UNITS + r")\b\s+(?:of|in)\b|"
    r"\b(?:a|an|one|two|three|half|quarter)\s+(?:" + _UNITS_BOUGHT + r")\s+of\b")
_A_A_CONVERSION = re.compile(
    r"\bhow\s+(?:much|many)\b[^?]{0,30}?\b(?:\d+)?\s*(?:" + _UNITS +
    r")\b\s+(?:in|to|into)\s+\w")
_A_HOW_MUCH_OF_A_UNIT = re.compile(
    r"\bhow\s+much\s+(?:is|are|was)\s+(?:a\s+|an\s+|one\s+)?[\d\w\s]{0,12}?\b(?:" +
    _UNITS_BOUGHT + r")\b(?!\s+of\b)")
_A_THE_CLOCK = re.compile(r"\bwhat\s+time\s+is\s+it\b|\bwhats\s+the\s+time\b")
_A_HOW_MUCH_IT_HOLDS = re.compile(
    r"\bhow\s+much\s+(?:\w+\s+){0,2}(?:does|do|is|are|will|would|should|must|can)\b"
    r"[^?]{0,60}?\b(?:weigh|weighs|hold|holds|contain|"
    r"contains|measure|measures|store|stores|sleep|sleeps|eat|eats|drink|drinks|feed|feeds|"
    r"lift|lifts|take|takes|need|needs|use|uses|burn|burns|grow|grows|train|exercise|"
    r"practise|practice|study|water|feed|give|have|put|add)\b")
_A_HOW_MUCH_ENOUGH = re.compile(
    r"\bhow\s+much\b[^?]{0,40}?\b(?:enough|too\s+much|too\s+little|of\s+it)\b|"
    r"\bhow\s+much\s+of\b")
_A_HOW_MUCH_IS_IN = re.compile(
    r"\bhow\s+much\s+(?:is|are)\s+(?:there\s+)?left\b|"
    r"\bhow\s+much\s+(?:is|are)\s+(?:in|left\s+in)\b|"
    r"\bhow\s+much\s+(?:\w+\s+)?in\s+(?:a|an|one|the|\d)\b|"
    r"\bhow\s+much\s+(?:\w+\s+){0,2}for\s+(?:\d+|one|two|three|four|five|six|seven|eight|nine|"
    r"ten|twenty)\b[^?]{0,20}\b(?:people|persons?|portions?|servings?|guests?|adults?|kids?)\b|"
    r"\bhow\s+much\s+(?:\w+\s+){0,2}per\s+(?:person|head|portion|serving)\b")
_A_HOW_MUCH_A_FEELING = re.compile(
    r"\bhow\s+much\s+(?:do|does|did)\s+(?:you|i|we|he|she|they)\s+(?:love|care|miss)\b")
_A_ARITHMETIC = re.compile(
    r"\d\s*(?:\+|\*|x|/|plus|minus|times|divided\s+by|multiplied\s+by)\s*\d|"
    r"\d\s+-\s+\d|"
    r"\b(?:percent|per\s?cent)\b|\d\s*%|\bwhats\s+\d+\s*%|"
    r"\b(?:plus|minus|divided\s+by|multiplied\s+by)\s+(?:\d+|one|two|three|four|five|six|seven|"
    r"eight|nine|ten|twenty|thirty|fifty|hundred|thousand)\b")
_A_HAS_A_NUMBER = re.compile(r"\d|\b(?:one|two|three|four|five|six|seven|eight|nine|ten)\b")
_A_A_DIFFERENCE = re.compile(
    r"\b(?:whats|what\s+is|what\s+was)\s+the\s+difference\b|\bdifference\s+between\b|"
    r"\bhow\s+(?:do|does)\s+\w+\s+differ\b|"
    r"\bhow\s+(?:is|are|was|were)\b[^?]{0,40}?\b(?:different|differs?|distinct)\s+"
    r"(?:from|to|than)\b")
_A_DID_YOU_SEE = re.compile(
    r"\bdid\s+you\s+(?:see|hear|watch|read|catch|catch\s+up\s+on)\b|"
    r"\bhave\s+you\s+(?:seen|heard|watched|read)\b|\bdid\s+you\s+know\b")
_A_BARE_RECORD = re.compile(
    r"^\s*(?:(?:and|so|but|then)\s+)?(?:the|whats\s+the|what\s+is\s+the|which\s+is\s+the)?\s*"
    r"(?:biggest|largest|tallest|longest|smallest|deepest|highest|oldest|fastest|richest|"
    r"most\s+populous)\b")
_A_PAST_YEAR = re.compile(r"\b(?:back\s+)?in\s+(?:1[0-9]{3}|20[0-2][0-9])\b")
_A_HISTORY_ITSELF = re.compile(
    r"\b(?:first|second|third|1st|2nd|world)\s+world\s+war\b|\bworld\s+war\s+(?:one|two|1|2|ii)\b|"
    r"\bthe\s+(?:great\s+)?war\b")
_A_HOW_A_THING_MEASURES = re.compile(
    r"\bhow\s+(?:hot|cold|warm|deep|tall|high|heavy|big|large|long|wide|fast|strong)\s+"
    r"(?:is|are|was|were)\s+(?!it\b|outside\b|today\b|tonight\b|this\b|the\s+weather\b)")
_A_A_TRAFFIC_LIGHT = re.compile(r"\btraffic\s+lights?\b")
_A_A_PLAN_ABOUT_THE_WEATHER = re.compile(
    r"\b(?:the\s+)?weather\s+(?:plan|plans|permitting|dependent|depending)\b")
_A_WEATHER_HERE = re.compile(
    r"\b(?:is|will)\s+it\s+(?:be\s+)?(?:going\s+to\s+)?(?:rain|snow|sunny|windy|hot|cold)\b|"
    r"\bhow\s+(?:hot|cold|warm|windy)\s+(?:is|will)\s+it\b|"
    r"\b(?:today|tonight|tomorrow|this\s+(?:week|weekend|morning|afternoon|evening)|"
    r"outside|right\s+now|at\s+the\s+moment)\b")
_A_HOW_OLD_IS_THE_WORLD = re.compile(
    r"\bhow\s+old\s+is\s+the\s+(?:earth|world|universe|planet|sun|moon)\b")
_MONEY_ASKED = re.compile(
    r"\bhow\s+much\s+(?:is|are|was|were|will|would|does|do)\b(?!\s+(?:too|enough|of)\b)")
_MONEY_FOR = re.compile(r"\bhow\s+much\s+for\b")

_A_PLACE_THAT_KEEPS_HOURS = re.compile(
    r"\b(?:shops?|stores?|supermarkets?|gyms?|pools?|librar(?:y|ies)|chemists?|"
    r"pharmac(?:y|ies)|surger(?:y|ies)|doctors?|dentists?|banks?|garages?|stations?|offices?|"
    r"centres?|centers?|clinics?|cafes?|pubs?|restaurants?|takeaways?|chippys?|markets?|"
    r"museums?|halls?|churches?|schools?|colleges?|tips?|dumps?|post\s+office|"
    r"leisure\s+centre|swimming\s+pool|garden\s+centre|car\s+park)\b")
_A_LINE_THAT_NAMES_A_PLACE = r"(?=[^\n]*" + _A_PLACE_THAT_KEEPS_HOURS.pattern + r")"
_NOT_A_FITTING_THAT_OPENS = (r"(?![^\n]*\b(?:doors?|gates?|windows?|lids?|drawers?|eyes?|"
                            r"mouth|flaps?|valves?|caps?|tins?|jars?|boxes?)\s+"
                            r"(?:open|opens|closed|closes|shut|shuts)\b)")
_A_DAY_WORD = (r"(?:today|tonight|tomorrow|now|this\b|on\b|at\b|until\b|till\b|late\b|"
               r"for\s+the\s+day|,)")
_NOT_OPEN_TO_SOMEBODY = (r"(?![^\n]*\b(?:open|opens)\s+(?:to|for)\s+"
                         r"(?!(?:today|tonight|tomorrow|now|late|the\s+day|the\s+weekend|"
                         r"the\s+summer|christmas|easter)\b))")
_HOURS = re.compile(
    r"\bopening\s+(?:hours?|times?)\b|\bclosing\s+time\b|\blate\s+opening\b|"
    r"\bbank\s+holiday\s+hours\b|"
    r"\b(?:open|opens|closed?|closes|shuts?)\s+(?:until|till|at|on|late|early)\b|"
    + _A_LINE_THAT_NAMES_A_PLACE + _NOT_A_FITTING_THAT_OPENS + _NOT_OPEN_TO_SOMEBODY +
    r"\b(?:is|are|was|were|does|do|will)\s+(?:[\w']+\s+){0,4}?(?:open|opens)\s+"
    r"(?:today|tonight|tomorrow|now|this\s+\w+)\b|"
    + _A_LINE_THAT_NAMES_A_PLACE + _NOT_A_FITTING_THAT_OPENS + _NOT_OPEN_TO_SOMEBODY +
    r"\b(?:is|are|was|were)\s+(?:[\w']+\s+){0,3}?(?:open|opens|closed|closes|shut|shuts)\b"
    r"(?=\s*" + _A_DAY_WORD + r")|"
    + _NOT_A_FITTING_THAT_OPENS + _NOT_OPEN_TO_SOMEBODY +
    r"\b(?:is|are|was|were|does|do)\s+(?:the\s+|a\s+)?(?:\w+\s+){0,2}?"
    + _A_PLACE_THAT_KEEPS_HOURS.pattern + r"\s+(?:open|opens|closed|closes|shut|shuts)\b|"
    + _NOT_A_FITTING_THAT_OPENS + _NOT_OPEN_TO_SOMEBODY +
    _A_PLACE_THAT_KEEPS_HOURS.pattern + r"\s+(?:\w+\s+){0,2}?"
    r"(?:open|opens|closed|closes|shut|shuts)\b(?=\s*" + _A_DAY_WORD + r")|"
    + _NOT_OPEN_TO_SOMEBODY +
    r"\b(?:is|are|was|were)\s+(?:it|they|there(?:\s+anywhere)?|"
    r"(?:the|this|that|my|our|your|any)\s+\w+|"
    r"\w+)\s+open\b|"
    r"\bwhat\s+times?\s+(?:does|do|is|are|will)\b|"
    r"\b(?:when|what\s+times?)\b[^?]{0,30}?\b(?:open|opens|close|closes|closed|shut|shuts)\b")

_WEATHER = re.compile(
    r"\bweather\b|\bforecast\b|\bumbrella\b|"
    r"\bhow\s+(?:hot|cold|warm|windy)\s+(?:is|will)\s+it\b|"
    r"\b(?:is|will)\s+it\s+(?:be\s+)?(?:going\s+to\s+)?(?:rain|snow|be\s+sunny|be\s+windy|"
    r"be\s+stormy|be\s+hot|be\s+cold)\b|"
    r"\bit\s+(?:is|will|should|might)\s+(?:be\s+)?(?:rain|snow|sunny|windy|stormy)\b|"
    r"\bheat\s?wave\b|\bcold\s+snap\b|\btemperature\s+(?:today|tomorrow|outside)\b")

_NEWS = re.compile(
    r"\bnews\b|\bheadlines?\b|"
    r"\b(?:whats|what\s+is|what\s+was|anything|any|the\s+latest|latest|breaking|got\s+any)\s+"
    r"(?:the\s+)?(?:news|headlines?)\b|"
    r"\b(?:latest|update[s]?)\s+(?:on|about)\b|"
    r"\b(?:news|press|newspaper)\s+stor(?:y|ies)\s+(?:on|about)\b|"
    r"\b(?:the|any|more)\s+word\s+(?:on|about)\b|"
    r"\bwhats\s+going\s+on\s+(?:in|at|with)\s+the\s+(?:world|news|country|city)\b|"
    r"\bwhats\s+(?:happened|happening)\b|\bwhat\s+(?:is|was)\s+happening\b|"
    r"\belections?\s+(?:today|tonight|this\s+(?:week|year)|results?)\b|"
    r"\bwho\s+won\b|\bwho(?:s|\s+is)\s+winning\b|\bdid\s+(?:\w+\s+){0,3}win\b|"
    r"\bhas\s+(?:\w+\s+){0,3}(?:won|finished|played)\b|"
    r"\bthe\s+score\b|\bwhats\s+the\s+score\b|\bleague\s+table\b|\bthe\s+table\b|"
    r"\bmatch\s+result\b|\b(?:the\s+)?results?\s+(?:of|from)\s+the\s+(?:match|game)\b|"
    r"\btransfers?\s+(?:news|today|latest)\b")

_AVAILABILITY = re.compile(
    r"\b(?:in\s+stock|stock\s+levels?|available|availability|unavailable|sold\s+out|"
    r"vacanc(?:y|ies)|hiring|waiting\s+list|"
    r"bookings?\s+(?:open|available|left|for)|"
    r"(?:make|get|book|check|change|cancel|move|confirm)\s+(?:a\s+|my\s+|the\s+)?booking\b|"
    r"(?:tickets?|places?|spaces?|seats?|rooms?|jobs?|appointments?)\s+(?:\w+\s+){0,2}"
    r"(?:left|going|available|free)\b)")

_TIMETABLE = re.compile(
    r"\b(?:timetables?|next\s+(?:train|bus|flight|boat|ferry|coach)|departures?|arrivals?|"
    r"delay(?:s|ed)?|roadworks?|bus\s+times?|train\s+times?|flight\s+times?|"
    r"traffic\s+(?:report|news|today|now|on\s+the)|"
    r"\bare\s+(?:the\s+)?(?:trains|buses|tubes|flights|ferries|trams)\s+running\b|"
    r"\bis\s+the\s+(?:m\d+|a\d+|motorway|road|bridge|tunnel)\s+(?:closed|open|blocked)\b|"
    r"what\s+time\s+(?:is|does)\s+the\s+(?:train|bus|flight))\b")

_A_SERVICE = re.compile(
    r"\b(?:trains?|buses?|bus|trams?|tubes?|underground|metro|flights?|ferry|ferries|"
    r"coach(?:es)?|platform|departures?|arrivals?)\b|"
    r"\bthe\s+\d{1,3}(?:[:.]\d{2})?(?=\s*(?:running|run|runs|leaves|leaving|departs?|"
    r"departing|due|arrives?|arriving|go|goes|going|take|takes|train|bus|flight))")
_A_DAY_OR_TIME = re.compile(
    r"\b(?:today|tonight|tomorrow|yesterday|this\s+(?:morning|afternoon|evening|weekend|week)|"
    r"next\s+(?:week|weekend)|monday|tuesday|wednesday|thursday|friday|saturday|sunday|"
    r"weekends?|bank\s+holiday|christmas|easter)\b|\b\d{1,2}[:.]\d{2}\b|"
    r"\bo'?clock\b|\b\d{1,2}\s?(?:am|pm)\b|\bhalf\s+past\b|\bhow\s+often\b")


class _AServiceOnADay:

    def __init__(self, service, when):
        self.service, self.when = service, when

    def search(self, text):
        service = self.service.search(text)
        if service is None:
            return None
        when = self.when.search(text)
        if when is None:
            return None
        return service if service.start() <= when.start() else when


_A_SERVICE_STATE = re.compile(
    r"\b(?:trains?|buses?|bus|flights?|coach(?:es)?|ferry|ferries|trams?)\b.{0,40}?"
    r"\b(?:late|delayed|cancell?ed|on\s+time|on\s+strike|diverted|full\s+up)\b")

_SERVICE_ON_A_DAY = _AServiceOnADay(_A_SERVICE, _A_DAY_OR_TIME)

_RATE = re.compile(
    r"\b(?:interest\s+rate[s]?|exchange\s+rate[s]?|tax\s+rate[s]?|inflation|mortgage\s+rate[s]?|"
    r"minimum\s+wage|price\s+cap|energy\s+cap|"
    r"national\s+insurance\s+(?:rate|contribution[s]?|percent|%)|stamp\s+duty|vat|"
    r"base\s+rate)\b")

_EVENT = re.compile(
    r"\b(?:whats\s+on|what\s+is\s+on|anything\s+on(?!\s+(?:a|an|the|my|your|about|for)\b)|"
    r"events?\s+on|gig\s+guide|show\s+times?|"
    r"cinema\s+times?|fixtures?|opening\s+night|when\s+is\s+the\s+\w+\s+on\b)\b")

_A_FRESHENING = re.compile(
    r"\b(?:latest|current|newest|most\s+recent|up[\s-]to[\s-]date)\s+"
    r"(?!(?:on|about|of|in|from|at|with)\b)")

_CHANGING = (
    ("rate", _RATE),
    ("price", _A_PRICE_ASK),
    ("post", _A_POST_HOLDER),
    ("timetable", _SERVICE_ON_A_DAY),
    ("timetable", _A_SERVICE_STATE),
    ("timetable", _TIMETABLE),
    ("hours", _HOURS),
    ("weather", _WEATHER),
    ("news", _NEWS),
    ("availability", _AVAILABILITY),
    ("event", _EVENT),
)

_A_HOW_IT_WORKS = re.compile(
    r"\bhow\s+(?:do|does|did)\b|\bwhy\s+(?:do|does|did)\b|\bwhat\s+causes?\b|"
    r"\bwhat\s+caused\b|\bhow\s+come\b")
_A_MY_OWN_PLAN = re.compile(
    r"\b(?:when|what\s+time)\s+(?:(?:should|shall|do|does|can|could|will|would|must|might|"
    r"had\s+better)\s+)?(?:i|we|you)\b(?!\s+(?:open|opens|close|closes|shut|shuts|serve|"
    r"serves|trade|trades)\b)")
_A_AN_OCCASION_OF_THEIR_OWN = re.compile(
    r"\b(?:what|which)\s+time\s+(?:is|are|was|were|does|do|did|will|would)\b.{0,25}?"
    r"\b(?:funeral|wake|meeting|appointment|interview|scan|operation|procedure|checkup|"
    r"check-up|assessment|induction|shift|session|court|hearing|viewing)\b")
_A_SAYS_NOW = re.compile(
    r"\b(?:today|tonight|tomorrow|right\s+now|at\s+the\s+moment|this\s+(?:morning|"
    r"afternoon|evening|week|weekend)|currently|still)\b")

_A_HOW_MANY = re.compile(r"\bhow\s+many\b")
_A_COUNT = re.compile(r"\bhow\s+many\b|\bhow\s+far\s+is\b|\bhow\s+long\s+is\b|\bhow\s+much\b")
_A_RECORD = re.compile(
    r"\bthe\s+(?:biggest|largest|tallest|oldest|youngest|longest|shortest|highest|lowest|"
    r"deepest|shallowest|fastest|slowest|smallest|richest|poorest|wealthiest|heaviest|"
    r"lightest|widest|narrowest|thinnest|strongest|busiest|rarest|commonest|most\s+common|most\s+popular|"
    r"most\s+\w+|least\s+\w+)\b")
_A_DEFINITION = re.compile(
    r"\bwhat\s+(?:is|are|was|were)\s+(?:(?:a|an|the)\s+)?"
    r"(?!(?:latest|newest|current|best|worst|main|right|usual|cheapest|nearest|the|a|an|it|that|this|they|these|those)\b)\w+|"
    r"\bwhat\s+does\s+\w+\s+mean\b|"
    r"\bwhat\s+is\s+the\s+meaning\b|\bwhat\s+does\s+(?:a|an|the)?\s*\w+\s+do\b")
_A_WORKING = re.compile(r"\bhow\s+(?:does|do)\b.{0,40}\bwork\b|"
                        r"\bwhy\s+(?:does|do|is|are|did)\b")
_A_HISTORY = re.compile(
    r"\bwhen\s+(?:was|were|did)\b.*\b(?:built|invented|discovered|founded|written|composed|"
    r"painted|made|begin|began|start|end|ended|happen|happened|become)\b|"
    r"\bwho\s+(?:invented|discovered|founded|wrote|composed|built|painted)\b|"
    r"\bhistory\s+of\b")
_A_MEASURE = re.compile(
    r"\bhow\s+(?:tall|high|deep|wide|long|heavy|big|far)\s+is\b|"
    r"\bhow\s+far\s+away\b")
_A_MADE_OF = re.compile(r"\bmade\s+(?:of|from|out\s+of)\b")
_A_METHOD = re.compile(
    r"\bhow\s+to\b|\bhow\s+(?:do|can|should)\s+(?:i|you|we)\b|\bhow\s+long\s+(?:do|does|should|to)\s+.*"
    r"\b(?:cook|boil|bake|roast|keep|last|take|soak|chill|freeze)\b|"
    r"\bhow\s+often\s+should\s+i\b")

_A_WORD_MEANS = re.compile(
    r"\bwhat\s+(?:does|do|did)\b.{1,40}?\bmean\b\s*[?!.]*\s*$|"
    r"\bwhats?\s+(?:is\s+)?the\s+meaning\s+of\b|\bwhat\s+is\s+(?:the\s+)?meaning\b|"
    r"\bwhat\s+is\s+the\s+definition\s+of\b|\bwhat\s+do\s+you\s+mean\s+by\b|"
    r"\bdefine\b")

_SETTLED = (_A_COUNT, _A_RECORD, _A_DEFINITION, _A_WORKING, _A_HISTORY, _A_MEASURE,
            _A_MADE_OF, _A_METHOD)

_SEALED_ASKS = frozenset(("maths",))


_ASKS_WITH_A_QUESTION_WORD = re.compile(
    r"^\s*(?:(?:and|but|so|then|also|ok|okay|right|oh|well|now|sorry|ta|hi|hello|"
    r"excuse\s+me)\s+)*(?:what|whats|what's|when|whens|where|which|who|whose|why|how|"
    r"hows|how's)\b")
_ASKS_MID_LINE = re.compile(
    r"\b(?:is|are|was|were|do|does|did|can|could|will|would|shall|should|am|have|has|had)\s+"
    r"(?:i|we|you|they)\b")
_ASKS_AFTER_A_COMMA = re.compile(
    r",\s*(?:(?:and|but|so|then|also)\s+)?(?:is|are|was|were|do|does|did|can|could|will|"
    r"would|shall|should|am|have|has|had)\s+(?:i|you|we|they|it|he|she|there|the\s+\w+)\b")
_ASKS_AFTER_A_COMMA_WORD = re.compile(
    r",\s*(?:(?:and|but|so|then|also)\s+)?(?:what|whats|when|whens|where|which|who|why|how|"
    r"hows)\b")
_ASKS_WITH_AN_AUXILIARY = re.compile(
    r"^(?:is|are|was|were|do|does|did|can|could|will|would|shall|should|has|have|had|any|"
    r"anything|anyone|anyway|tell)\b")


_A_REPORTS_THE_ASK = re.compile(
    r"^\s*(?:(?:and|but|so|then|also|well|oh|anyway)\s+)*(?:i|we|they|he|she|everyone|"
    r"someone)\s+(?:already\s+|still\s+|just\s+|now\s+|never\s+|definitely\s+)?"
    r"(?:know|knows|knew|told|tell|tells|said|says|explained|explains|mentioned|mentions|"
    r"remember|remembers|reminded|found\s+out)\b")


def _a_line_asks(read, said):
    if read.get("kind") == "question":
        return True
    if _A_REPORTS_THE_ASK.search(said):
        return bool("?" in said or _ASKS_WITH_A_QUESTION_WORD.search(said)
                    or _ASKS_WITH_AN_AUXILIARY.match(said.strip())
                    or _ASKS_AFTER_A_COMMA_WORD.search(said.replace(" ,", ",")))
    if read.get("asks"):
        return True
    if read.get("intent") == "question":
        return True
    if "?" in said:
        return True
    return bool(_ASKS_WITH_A_QUESTION_WORD.search(said)
                or _ASKS_MID_LINE.search(said)
                or _ASKS_AFTER_A_COMMA.search(said.replace(" ,", ","))
                or _ASKS_WITH_AN_AUXILIARY.match(said.strip()))


def _as_typed(line):
    said = line.get("text") or line.get("clean") or ""
    if not isinstance(said, str):
        said = ""
    return " " + said.strip().lower() + " "


def _carried_on(read, previous, words):
    if not isinstance(previous, dict) or not previous.get("over_time"):
        return None
    if not read.get("followup") or len(words) > _A_FOLLOW_UP_WORDS:
        return None
    if previous.get("text") and previous.get("text") == read.get("text"):
        return None
    return True, previous.get("over_time_what")


def _text(line):
    said = line.get("plain") or line.get("clean") or ""
    if not isinstance(said, str):
        said = ""
    return " " + said.strip().lower() + " "


_BARE_LIVE_LEAD = (r"^\s*(?:(?:and|so|but|then|also|ok|okay|right|oh)\s+|"
                   r"(?:what|how)\s+about\s+)?")
_A_BARE_LIVE = (
    ("news", re.compile(_BARE_LIVE_LEAD + r"(?:the\s+|any\s+|got\s+any\s+)?(?:news|headlines?)\b")),
    ("hours", re.compile(_BARE_LIVE_LEAD + r"(?:the\s+|any\s+)?(?:opening\s+(?:hours|times)|"
                                              r"opening|closing\s+time|bank\s+holiday\s+hours)\b")),
    ("timetable", re.compile(_BARE_LIVE_LEAD + r"(?:the\s+|any\s+)?(?:delays?|roadworks?|"
                                                  r"traffic|bus\s+times?|train\s+times?|"
                                                  r"departures|arrivals|timetable)\b")),
    ("weather", re.compile(_BARE_LIVE_LEAD + r"(?:the\s+|any\s+)?(?:weather|forecast)\b")),
    ("price", re.compile(_BARE_LIVE_LEAD + r"(?:the\s+|any\s+)?(?:price|prices|cost|costs|"
                                            r"fares?|ticket\s+prices?)\b")),
)
_A_REPORTS = re.compile(
    r"\b(?:looks?|looked|seems?|seemed|sounds?|sounded|feels?|felt|was|were|is|are|has|have|"
    r"had|said|says|told|hear|heard|got|get|gets|makes?|made|turns?|turned|went|goes|"
    r"coming|comes|hit|hits|does|doesnt|did|didnt|wont|cant|helps?|ruined|spoils?)\b")

_A_BARE_ASK = 4
_A_BARE_LIVE_WORDS = 9
_A_FOLLOW_UP_WORDS = 7
_A_BARE_TAIL = re.compile(
    r"^(?:for|on|at|in|this|next|today|tonight|tomorrow|now|here|there|please|pls|thanks|ta|"
    r"anyone|anywhere)\b")
_A_DETERMINER = frozenset(("", "the", "a", "an", "any", "your", "this", "our", "these"))


def over_time(line, read, previous=None, carrying_on=False):
    read = read if isinstance(read, dict) else {}
    text = _text(line if isinstance(line, dict) else {})
    asking = _a_line_asks(read, text)
    words = text.split()
    bare = len(words) <= _A_BARE_ASK
    if asking and _A_HOW_IT_WORKS.search(text) and not _A_SAYS_NOW.search(text):
        return False, None
    if _A_ARITHMETIC.search(text) or _A_ARITHMETIC.search(_as_typed(line)):
        return False, None
    if (_SEALED_ASKS & set(read.get("asks") or ()) and _A_HAS_A_NUMBER.search(text)
            and not _A_AN_AMOUNT_OF_A_THING.search(text)):
        return False, None
    if (_A_PAST_YEAR.search(text) or _A_HOW_OLD_IS_THE_WORLD.search(text)
            or _A_HISTORY_ITSELF.search(text)):
        return False, None
    if _A_A_DIFFERENCE.search(text):
        return False, None
    if _A_HOW_A_THING_MEASURES.search(text) and not _A_WEATHER_HERE.search(text):
        return False, None
    if _A_A_TRAFFIC_LIGHT.search(text):
        return None, None
    if _A_A_PLAN_ABOUT_THE_WEATHER.search(text) and not _A_WEATHER_HERE.search(text):
        return None, None
    if (_A_HOW_MUCH_IT_HOLDS.search(text) or _A_HOW_MUCH_IS_IN.search(text)
            or _A_HOW_MUCH_ENOUGH.search(text) or _A_HOW_MUCH_A_FEELING.search(text)):
        return False, None
    if _A_AN_OCCASION_OF_THEIR_OWN.search(text):
        return None, None
    if not _MONEY.search(text) and (_A_A_CONVERSION.search(text)
                                    or _A_HOW_MUCH_OF_A_UNIT.search(text)):
        return False, None
    if _A_HOW_MUCH_I_SPENT.search(text) or _A_MY_OWN_FIGURE.search(text):
        return None, None
    if _A_THE_CLOCK.search(text):
        return None, None
    if _A_DID_YOU_SEE.search(text):
        return None, None
    if _A_BARE_RECORD.search(text) and not asking:
        return False, None
    fresh = _A_FRESHENING.sub(" ", text)
    if _A_WORD_MEANS.search(text):
        return False, None
    for what, pattern in _A_BARE_LIVE:
        found = pattern.search(fresh)
        if found and not _A_REPORTS.search(text) and len(words) <= _A_BARE_LIVE_WORDS:
            return True, what
    for what, pattern in _CHANGING:
        found = pattern.search(fresh)
        if not found:
            continue
        if what in ("hours", "timetable", "event") and _A_MY_OWN_PLAN.search(text):
            continue
        if (_A_DEFINITION.search(text)
                and fresh[:found.start()].strip() in ("what is", "what are", "whats", "what's")
                and not fresh[found.end():].strip(" ?!.,")):
            return False, None
        if asking:
            return True, what
        if bare and not _A_REPORTS.search(text):
            tail = fresh[found.end():].strip()
            if (fresh[:found.start()].strip() in _A_DETERMINER
                    and (not tail or _A_BARE_TAIL.match(tail))):
                return True, what
    if carrying_on:
        return _carried_on(read, previous, words)
    if not asking:
        return None, None
    if _SEALED_ASKS & set(read.get("asks") or ()):
        return False, None
    for pattern in _SETTLED:
        if pattern.search(text):
            return False, None
    return None, None
