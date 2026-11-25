import re

from . import kinds, lexicon
from .normalize import LEXICON as COMMON_WORDS

_COLD_SIDE = r"\b(?:freezing|cold|chilly|shivering|shivery)\b"
_HOT_SIDE = r"\b(?:sweating|sweaty|boiling|hot|burning(?: up)?)\b"
_FILL = (r"(?:\s+(?:one|two|a|an|the|some|bit|minute|minutes|or|and|then|so|very|really|"
         r"sometimes|always|all|next|im|i'm|i|am|at|in|of|night|nights|morning|"
         r"mornings|day|days|evening|evenings|afternoon|week|weekend|first|second))*\s*")
_JOIN = _FILL + r"(?:and\s+then|then|and|or|but)" + _FILL + r"\s*"
_FROM_TO = ("(?:" + _COLD_SIDE + r"\s+to\s+" + _HOT_SIDE + "|" + _HOT_SIDE + r"\s+to\s+"
            + _COLD_SIDE + ")")
_ALTERNATING = ("(?:" + _COLD_SIDE + _JOIN + _HOT_SIDE + "|" + _HOT_SIDE + _JOIN + _COLD_SIDE
                + "|" + _FROM_TO + ")")
GOING_BOTH_WAYS = re.compile(_ALTERNATING, re.I)

_CHUCK_UP = (
    r"\b(?:been |kept? |keep |still )?chuck(?:s|ed|ing)?"
    r" (?:it |them |his |her |my |their |our )?up\b"
    r"(?=\s*(?:$|[,.!?;:]|(?:all|every|again|still|constantly|most|so|since|at|during|"
    r"yesterday|today|tonight|tomorrow|now|once|twice|last|this|in|for|after|before|"
    r"the other\b)\b"
    r"|(?:my |the |his |her |their |your |our |some |that )?"
    r"(?:lunch|dinner|breakfast|tea|supper|food|water|drink|drinks|milk|coffee|beer|wine|"
    r"blood|bile|medicine|meal|it)\b))")

PARTS = (
    ("head",
     r"\bmigraines?\b|\bmigranes?\b|\bheadaches?\b|\bhead aches?\b"
     r"|\bhead\b[^.!?]{0,14}?\b(?:is |feels? |keeps? |has )?"
     r"(?:pounding|throbbing|splitting|banging|hurts?|hurting|aching|killing)\b"
     r"|\b(?:pounding|throbbing|splitting)\b[^.!?]{0,10}?\bhead\b",
     frozenset("head headache headaches migraine migraines".split())),
    ("throat",
     r"\bsore throat\b|\bstrep throat\b"
     r"|\bthroat\b[^.!?]{0,14}?\b(?:hurts?|hurting|aches?|is sore|is killing|feels? raw|"
     r"is rough|is scratchy)\b",
     frozenset("throat".split())),
    ("temperature",
     r"(?<!hay )\bfever\w*|\btemperature\b|\bshivery\b|\bchills\b|\bhot and cold\b"
     r"|\bburning up\b|" + _ALTERNATING,
     frozenset("temperature fever".split())),
    ("stomach",
     r"\bstomach (?:bug|ache|cramps?|upset)\b|\btummy (?:ache|bug)\b"
     r"|\b(?:stomach|tummy)\b[^.!?]{0,12}?\b(?:hurts?|hurting|aches?|aching|is killing|"
     r"is (?:sore|cramping))\b"
     r"|\b(?:(?:going|gonna|about)\s+to\s+|been |kept? |keep |still )?(?:throwing up|"
     r"thrown up|threw up|throws up|throw up|vomiting|vomited|vomit|vomits|puk(?:e|es|ed|ing)|"
     r"barf(?:s|ed|ing)?|" + _CHUCK_UP +
     r"|(?:be|been|being|was|were) sick(?!\s+(?:of|to death|and tired)\b)|nauseous|nausea)\b"
     r"|\bsick\b(?=\s+(?:\d|twice|once|three|four|five|since|all |last night|"
     r"yesterday|most mornings|every))"
     r"|\b(?:can ?not|cant|can't|could not|couldnt|couldn't|unable to|not able to) keep "
     r"(?:anything|much|water|fluids?|food|it) down\b"
     r"|\bkeep(?:ing)? nothing down\b"
     r"|\b(?:feel|feels|feeling|felt) sick\b(?!\s+(?:about|at|of|thinking)\b)"
     r"|\bdiarrhoea\b|\bdiarrhea\b|\bd\s?and\s?v\b",
     frozenset("stomach tummy belly gut".split())),
    ("chest",
     r"\bchest infection\b|\bchesty\b|\bwheez\w*",
     frozenset("chest".split())),
    ("teeth",
     r"\btoothaches?\b|\btooth aches?\b|\bteeth\b[^.!?]{0,14}?\b(?:hurt|hurts|aching|"
     r"ache|sensitive|killing)\b|\btooth\b[^.!?]{0,14}?\b(?:hurts?|aching|aches?|"
     r"throbbing|is killing)\b|\b(?:dental|dentist)\b[^.!?]{0,20}?\b(?:pain|"
     r"agony|hurts?)\b|\babscess\b|\bgums?\b[^.!?]{0,14}?\b(?:sore|bleeding|swollen|"
     r"hurts?|aching)\b",
     frozenset("tooth teeth gum gums mouth jaw".split())),
    ("ear",
     r"\bearaches?\b|\bear aches?\b|\b(?:ear|ears)\b[^.!?]{0,16}?\b(?:hurts?|hurting|"
     r"aching|aches?|throbbing|is killing|is sore)\b"
     r"|\bear infection\b|\bglue ear\b",
     frozenset("ear ears".split())),
)

AN_ABSCESS = re.compile(r"\babscess\w*\b", re.I)
A_MOUTH_WORD = re.compile(
    r"\b(?:tooth|toothache|toothaches|teeth|gums?|mouth|jaw|dental|dentist|molar)\b"
    r"[^.!?]{0,20}?\babscess\w*"
    r"|\babscess\w*\b[^.!?]{0,20}?\b(?:tooth|toothache|teeth|gums?|mouth|jaw|dental|molar)\b",
    re.I)
A_SPREADING_SIGN = re.compile(r"\b(?:fever|temperature|pus|pussy|puffy|swelling|swollen|"
                              r"spreading|swallow|swallowing|cheek|face)\b", re.I)
ANOTHER_PART = re.compile(r"\b(?:leg|legs|arm|arms|foot|feet|toe|toes|hand|hands|finger|"
                          r"fingers|knee|knees|hip|hips|back|shoulder|shoulders|skin|wound|"
                          r"wounds|armpit|groin|bum|bottom|thumb|elbow|ankle|shin|thigh|chest|"
                          r"stomach|tummy|neck|scalp|eye|eyes|breast|breasts|ear|ears)\b", re.I)
ALREADY_DEALT_WITH = re.compile(r"\b(?:drained|lanced|removed|burst|popped|gone)\b", re.I)
A_SAMPLE = re.compile(r"\b(?:sample|samples|test|tests|tested|testing|kit|pot|"
                      r"container|form|forms)\b", re.I)


def _an_abscess_elsewhere(text):
    if not AN_ABSCESS.search(text):
        return False
    return bool(A_MOUTH_WORD.search(text) or A_SPREADING_SIGN.search(text)
                or ANOTHER_PART.search(text) or ALREADY_DEALT_WITH.search(text))


ASKING = re.compile(
    r"\b(?:what|anything|something)\b[^.!?]{0,26}?\b(?:helps?|works?|should i (?:take|do)|"
    r"can i take|do i take|do for|to take|to do)\b"
    r"|\bhow (?:do|can) i (?:get rid of|stop|shift|ease)\b|\bany (?:advice|tips|ideas)\b")


A_LOOSE_STOOL = re.compile(
    r"\b(?:loose|runny|watery|liquid|soft)\s+(?:stools?|poos?|poops?|bowels?)\b"
    r"|\b(?:stools?|poos?|poops?|bowels?)\b[^.!?]{0,24}?"
    r"\b(?:loose|runny|watery|liquid|like water)\b"
    r"|\bthe (?:trots|shits|squits|skitters|squirts)\b",
    re.I)
A_THING_IS_TERRIBLE = re.compile(
    r"\b(?:is|are|was|were|be|being|been|seems?|looks?|feels?|gone|go(?:es|ing)?|went)\s+"
    r"(?:to\s+|a (?:bit |total |right |proper |complete |real |crock )?of\s+|such\s+|"
    r"right\s+|proper\s+|complete\s+)?"
    r"the (?:shits|trots|squits|skitters|squirts)\b", re.I)
A_CHAIR_WORD = re.compile(
    r"\b(?:leg|legs|joint|joints|seat|seats|wood|wooden|screw|screws|screwdriver|tighten|tight"
    r"|wobbly|wobble|wobbles|rickety|bracket|glue|chair|chairs|table|tables|bench|furniture"
    r"|dresser|sideboard|kitchen|carpenter|flat ?pack)\b"
    r"|\b(?:bar|counter|pub|breakfast|dining) ?stools?\b", re.I)
A_GUT_ONLY = re.compile(
    r"\b(?:runny|watery|liquid|soft|hard|firm|pale|smelly|stinking|streaked|streaks|slimy|mucus"
    r"|diarr?hoea|constipat\w*|tummy|stomach|gut|guts|ache|aches|aching|pain|pains|painful"
    r"|cramps?|cramping|sore|wind|bloat\w*|toilet|loo|bum|poo|poos|pooed|pooping|bowels?"
    r"|sick|nausea|nauseous|vomit\w*|days?|weeks?|months?|since|morning|mornings|night|nights"
    r"|yesterday|today|times|a day)\b", re.I)
A_POO_COLOUR = re.compile(r"\b(?:pale|black|tarry|bloody|blood|red|floats?|green|colour|"
                          r"color|mucus|slimy)\b", re.I)


PART_NOUNS_BY_LENGTH = {}
for _part_name, _part_pattern, _part_nouns in PARTS:
    for _noun in _part_nouns:
        PART_NOUNS_BY_LENGTH.setdefault(len(_noun), set()).add(_noun)


def _one_letter_apart(typed, spelled):
    if abs(len(typed) - len(spelled)) > 1:
        return False
    if len(typed) == len(spelled):
        return sum(1 for typed_at, spelled_at in zip(typed, spelled)
                   if typed_at != spelled_at) == 1
    short, long_ = sorted((typed, spelled), key=len)
    return any(long_[:at] + long_[at + 1:] == short for at in range(len(long_)))


def _a_part_typed_with_one_letter_wrong(word):
    fits = set()
    for length in (len(word) - 1, len(word), len(word) + 1):
        for noun in PART_NOUNS_BY_LENGTH.get(length, ()):
            if noun[0] == word[0] and _one_letter_apart(word, noun):
                fits.add(noun)
                if len(fits) > 1:
                    return None
    return fits.pop() if fits else None


A_WORD_OF_ITS_OWN = frozenset("""
    bella bell bully chesty chess earns glut glum heady heal heap heat heed tommy threat
    """.split())


def _a_word_rather_than_a_typo(word):
    if word in COMMON_WORDS or word in A_WORD_OF_ITS_OWN:
        return True
    from .topics import CONDITIONS
    return word in CONDITIONS


def _spell_the_parts(text):
    repaired = text
    for word in set(re.findall(r"[a-z]+", text.lower())):
        if len(word) < 4 or _a_word_rather_than_a_typo(word):
            continue
        part = _a_part_typed_with_one_letter_wrong(word)
        if part:
            repaired = re.sub(r"\b%s\b" % word, part, repaired)
    return repaired


def _the_gut_is_settled(text):
    words = set(re.findall(r"[a-z']+", text.lower()))
    if not words & {"stool", "stools"}:
        return True
    return bool(words & set(A_GUT_ONLY.findall(text.lower())))


def read(text):
    if not isinstance(text, str) or not text.strip():
        return None
    text = _spell_the_parts(text.replace("|", " "))
    if (A_LOOSE_STOOL.search(text) and not A_SAMPLE.search(text)
            and not A_POO_COLOUR.search(text) and not A_CHAIR_WORD.search(text)
            and not A_THING_IS_TERRIBLE.search(text)
            and not _someone_else(text) and _the_gut_is_settled(text)):
        return "stomach"
    sample = bool(A_SAMPLE.search(text))
    for name, pattern, nouns in PARTS:
        if name == "teeth" and _an_abscess_elsewhere(text):
            continue
        if name == "stomach" and sample:
            continue
        for match in re.finditer(pattern, text, re.I):
            if _the_speakers(text, match.end(), nouns, match.start()):
                return name
            if ASKING.search(text) and not _someone_else(text):
                return name
            if _just_the_part(text, match) and not _someone_else(text):
                return name
    return _said_about_itself(text)


def _the_speakers(text, at, nouns, began=None):
    words = re.findall(r"[a-z']+", text[:at])
    owner = None
    for index, word in enumerate(words):
        if word in kinds.OTHER_PEOPLE or word == "my":
            owner = (word, index)
    if owner is not None:
        word, index = owner
        if word != "my":
            return False
        return bool(words[index + 1:index + 2]) and words[index + 1] in nouns
    start = max(0, len(words) - 6)
    while start > 0 and words[start] in _A_VERB_NEEDING_ITS_SUBJECT:
        start -= 1
    tail = " ".join(words[start:])
    tail = re.sub(r"\bi'?m\b", "i am", tail)
    tail = re.sub(r"\bi'?ve\b", "i have", tail)
    tail = re.sub(r"\bwe'?re\b", "we are", tail)
    tail = re.sub(r"\bwe'?ve\b", "we have", tail)
    if SPEAKER_ILL.search(tail) or kinds._speaker_before(text, at):
        return True
    if began is None:
        return False
    return _the_speaker_is_the_subject(words, len(re.findall(r"[a-z']+", text[:began])))


_BEFORE_THE_COMPLAINT = frozenset("""i we am is are was were be been being have has had got
    get gets getting keep keeps kept stop stops stopped can cannot cant can't could couldnt
    couldn't not dont don't never still just only also really so very badly feel feels felt
    again night days woke up started begin began""".split())

_A_MAYBE = frozenset("could might may would should must can".split())
_A_NO = frozenset("not never cant cannot couldnt couldn't didnt didn't".split())


def _only_the_fillers_between(between):
    if between and between[0] in _A_MAYBE:
        if not (len(between) > 1 and between[1] in _A_NO):
            return False
        between = between[1:]
    return all(word in _BEFORE_THE_COMPLAINT for word in between)


def _the_speaker_is_the_subject(words, began):
    for index in range(len(words) - 1, -1, -1):
        if words[index] not in ("i", "we"):
            continue
        if _only_the_fillers_between(words[index + 1:began]):
            return True
    return False


_A_VERB_NEEDING_ITS_SUBJECT = ("am", "is", "are", "was", "were", "be", "been", "being", "have",
                               "has", "had", "ve", "feel", "feels", "felt", "keep", "keeps")


SPEAKER_ILL = re.compile(
    r"\b(?:i|we) (?:both |also |all )?(?:have|had|has|got|get|getting|having|been|being|keep|"
    r"keeps|keeping|am|was|are|were|feel|feeling|felt|suffer\w*|with)\b")


FILLER = frozenset("""a an the my some this that bit of a really very so proper proper
    bad worse worst sore slight terrible awful horrible nasty mild chronic another again
    another little quite too pretty still""".split())


PLAIN_SKIP = frozenset(("chest", "temperature"))
PLAIN_SKIP_WORDS = frozenset(("jaw",))
PLAIN_PAIN = frozenset(lexicon.PAIN_WORDS) | frozenset(("bad", "cramping", "cramps", "upset"))
WHEN_IT_HAPPENED = frozenset("""today tonight yesterday morning mornings afternoon afternoons
    evening evenings night nights week weeks weekend weekends month months day days all since
    last this now again every hour hours minute minutes am pm o clock time times midnight noon
    monday tuesday wednesday thursday friday saturday sunday once twice three four five six ten
    couple few several""".split())

_A_HELPER_BEFORE = frozenset("be been being am is are was were keep keeps kept still just".split())

PAIN_ADJECTIVE = frozenset("""sore painful aching achy bad swollen cramping crampy upset stiff
    throbbing stinging burning numb rough dodgy awful terrible horrible rubbish queasy
    trouble troubles""".split())
PAIN_BETWEEN = frozenset("""is am are was were be been being feels feel felt gets getting got
    gone keep keeps kept very really so too quite a bit little just now still often always""".split())
PAIN_REACH = 3
POSSESSIVE = frozenset("my his her their our your".split())
PLAIN_UNWELL = frozenset("""off rough bad awful terrible horrible rubbish dodgy queasy
    trouble troubles unhappy wrong grim""".split())
OFF_MAY_GO_ON = frozenset("""and but for since today tonight now still again all most
    lately recently days weeks months hours mornings afternoons evenings nights every
    couple few several very really quite bit little""".split())
PAIN_PHRASE = (("playing", "up"), ("acting", "up"), ("in", "knots"), ("in", "bits"),
               ("in", "a", "knot"), ("all", "over", "the", "place"), ("giving", "me", "grief"),
               ("giving", "me", "jip"))


def _an_unwell_word(words, at):
    word = words[at]
    if word in PLAIN_PAIN:
        return True
    if word not in PLAIN_UNWELL:
        return False
    if word != "off":
        return True
    return at + 1 >= len(words) or words[at + 1] in OFF_MAY_GO_ON


def _pain_after(words, index):
    for step in range(1, PAIN_REACH + 1):
        at = index + step
        if at >= len(words):
            return False
        if _an_unwell_word(words, at):
            if words[at] == "off" and not (index > 0 and words[index - 1] in POSSESSIVE):
                break
            return True
        if words[at] not in PAIN_BETWEEN:
            break
    return _phrase_after(words, index)


def _phrase_after(words, index):
    for phrase in PAIN_PHRASE:
        at = index + 1
        for word in phrase:
            if at < len(words) and words[at] in PAIN_BETWEEN:
                at += 1
            if at >= len(words) or words[at] != word:
                break
            at += 1
        else:
            return True
    return False


def _said_about_itself(text):
    found = list(re.finditer(r"[a-z']+", text))
    words = [match.group() for match in found]
    for index, word in enumerate(words):
        for name, _pattern, nouns in PARTS:
            if name in PLAIN_SKIP or word in PLAIN_SKIP_WORDS or not _the_part_word(word, nouns):
                continue
            in_front = index > 0 and words[index - 1] in PAIN_ADJECTIVE
            if not (in_front or _pain_after(words, index)):
                continue
            if _the_speakers(text, found[index].end(), nouns, found[index].start()):
                return name
            if index > 0 and words[index - 1] in ("my", "our", "me"):
                return name
            if index == 0 and _pain_after(words, index):
                return name
            if _someone_else(text):
                continue
            if in_front or _just_the_part_words(words, index):
                return name
    return None


def _the_part_word(word, nouns):
    if word in nouns:
        return word
    bare = word
    if bare.endswith("'s"):
        bare = bare[:-2]
    elif bare.endswith("s"):
        bare = bare[:-1]
    return bare if bare in nouns else None


def _just_the_part_words(words, index):
    rest = words[:index] + words[index + 1:]
    allowed = FILLER | PLAIN_PAIN | PLAIN_UNWELL | PAIN_BETWEEN
    return all(word in allowed for word in rest)


def _just_the_part(text, match):
    rest = (text[:match.start()] + " " + text[match.end():]).strip()
    words = re.findall(r"[a-z']+", rest)
    return all(word in FILLER or word in WHEN_IT_HAPPENED or word in _A_HELPER_BEFORE
               or word.isdigit() for word in words)


def _someone_else(text):
    for word in re.findall(r"[a-z']+", text):
        if word in kinds.OTHER_PEOPLE or word.rstrip("s") in kinds.OTHER_PEOPLE:
            return True
    return False
