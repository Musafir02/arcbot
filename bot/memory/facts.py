import re

from ..understanding import breeds, lexicon, normalize
from ..understanding.kinds import EMOTION_WORDS, VERB_FORMS
from ..understanding.topics import STRONG, PHRASES, WORD_NUMBERS, CONDITIONS

from .named import the_name_in
from . import taste
from .filler import TAIL_OFF


NOT_NAMES = frozenset("""
a an the this that these those not no so really very quite just still also always already
only even now here there back home off out in on at up down over around about all both too
good bad great fine ok okay sure glad happy sad angry upset tired exhausted hungry thirsty bored
busy free late early lost done ready sorry afraid scared nervous worried stressed excited
confused lonely ill sick better worse old young new first second third next last single
married pregnant vegan vegetarian allergic serious interested trying looking thinking planning
coeliac celiac diabetic asthmatic epileptic anaemic anemic intolerant lactose gluten autistic
adhd menopausal perimenopausal pescatarian flexitarian veggie
going coming getting having making doing writing working learning studying cooking moving buying
playing watching reading listening talking speaking feeling letting taking giving waiting
hoping wondering asking saying telling checking shopping cleaning walking running driving
flying travelling traveling starting finishing meeting visiting staying living eating drinking
sleeping sitting standing paying spending saving booking ordering calling texting emailing
posting sharing using fixing building creating preparing practising practicing revising
training coaching organising organizing decorating painting gardening baking coming around
fine good well okay alright nearly almost definitely probably maybe perhaps honestly actually
literally seriously totally completely absolutely pretty rather kind sort bit little lot
off down out away along through until since while because though although whether
""".split())

NAME_TAIL_MIN = {"ed": 5, "ing": 5, "ly": 6, "ous": 5, "ful": 6, "less": 6,
                 "ish": 4, "able": 6, "ible": 6, "ic": 5, "ac": 5, "ist": 6,
                 "ism": 6, "ese": 5, "ant": 6,
                 "ive": 6}
NAMES_THAT_LOOK_LIKE_STATES = frozenset("""
dominic dominick
isaac cedric frederic
ahmed mohamed muhammed jared
manish trish
kimberly
kay
""".split())
NOT_NAMES_EXTRA = frozenset("""
due owed english scottish welsh irish british muslim hindu sikh jew pagan mormon sober adhd ocd ptsd
trans gay straight lesbian bisexual asexual blind deaf disabled unemployed retired homeless
dyspraxic dyscalculic
# A condition somebody lives with is how they are, not who they are, and these two end in
# nothing a state is built out of, so the endings cannot catch them: "im depressive" was
# answered "Nice to meet you, Depressive", and a bare "im hypertensive" the same.
depressive hypertensive
knackered shattered starving freezing boiling skint broke aching sore stuck done outside inside
upstairs downstairs online offline asleep awake alright okay fine good great awful terrible
here there back home away out off in on over around up down away late early soon nearly almost
definitely probably maybe honestly seriously literally actually totally completely absolutely
cold hot warm wet dry cross half mid bloody soaked frozen numb dizzy queasy poorly shaky
safe unsafe itchy stiff calm restless faint bloated snotty sniffly achy crampy
tight weak sleepy dozy groggy foggy comfy cosy snug proud guilty unwell dirty clean poor
# How a person is, not who they are: "im unheard" was answered "Nice to meet you, Unheard" - the
# coldest reply there is to somebody saying they are not heard. "unseen" and "nobody" are the
# same shape ("im nobody" was a name too).
unseen unheard nobody
dead beat spent zonked pooped livid fuming miffed
content confident different important present silent decent pleasant fluent patient absent
violent brilliant distant recent constant sunburnt burnt
full empty unsure certain brave silly daft mad grumpy moody fed fedup
# How somebody says they are, in words that are also other things: "im grand" (Ireland), "im
# sound", "im chill", "im content", "im brill", "im mint". Nothing is repaired in any of them,
# so the repair rule cannot see them, and the store handed the word back as a name: "im grand"
# was answered "Nice to meet you, Grand" and every later turn called the person Grand.
grand sound chill content brill mint
# The same for a disparaging word: "im fat" and "im stupid" are how somebody says they are, and
# the store was filing them as a name ("Nice to meet you, Fat").
fat ugly stupid thick dumb
rundown offshore horny
dressed settled from with for by of to near into than as after
# A word about the spelling or the print of the name is not the name: "my name is spelt wrong on
# my payslip" was answered "Hi Spelt - open the payslip and check...", and "my name is misspelt on
# my contract" was answered "Nice to meet you, Misspelt." Every one of these is a thing said *of*
# a name, never a name people are given.
spelt spelled misspelt misspelled mispelt mispelled printed print handwritten hyphenated
capitalised capitalized typed type pronounced
# The words that close a sentence about somebody else's behaviour, which is where a name is
# least likely and the store was most confident: "my son doesnt call me anymore" was read as an
# introduction, so every later turn called the person Anymore, and the reply opened "Hi Anymore
# - a relative going quiet...". A name after "call me" is offered ("call me Dan"); a word that
# only says when or whether the calling happens is not offered at all.
anymore anyways someday sometime sometimes nowadays ever either neither soon later sooner
tomorrow tonight meanwhile afterwards afterward
# The same list, for the reviewers of this change who sent three more of exactly that shape:
# "my son wont call me again" was "Hi Again", and "call me anytime" and "call me whenever you
# like" introduced the person as Anytime and Whenever. They say when or whether, not who.
again anytime whenever always eventually already once then
""".split()) | frozenset("""
sweaty clammy woozy jittery achey queezy muggy bleary puffy giddy edgy antsy twitchy
hangry drowsy buzzy spacey dopey mopey quivery fidgety sniffy wobbly
# A body word that is also a dog's coat or a Snow White dwarf: "im husky" is a voice going and
# "im sneezy" is a cold starting, and both were answered "Nice to meet you, Husky".
husky sneezy
hungover hangover jetlagged jetlag dehydrated out
""".split())

NOT_A_NAME_FEELING = frozenset(
    word for cues in EMOTION_WORDS.values() for cue in cues for word in cue.split())
NOT_A_NAME_LAUGH = frozenset(lexicon.LAUGHTER)


CONDITIONS_OF_THE_MIND = frozenset("""
    bipolar schizophrenia schizophrenic psychosis psychotic anorexic bulimic ptsd ocd adhd
    autism autistic dyspraxic dyspraxia agoraphobia agoraphobic narcolepsy narcoleptic""".split())


def _health_words():
    words = set(STRONG["health"].split())
    for phrase in PHRASES["health"]:
        words.update(phrase.split())
    words.update(CONDITIONS)
    words.update(CONDITIONS_OF_THE_MIND)
    return frozenset(words)


NOT_A_NAME_ILLNESS = _health_words()

NOT_A_NAME_TRAIT = frozenset(lexicon.TRAITS)
NOT_A_NAME_DESCRIBING = frozenset("""quiet messy noisy picky fussy bossy stubborn rude spoilt
    chatty negative positive tidy untidy nosy weird odd loud hard""".split())
NOT_A_NAME_CONDITION = frozenset("""bipolar froze""".split())
NOT_A_NAME_STATE = (NOT_A_NAME_FEELING | NOT_A_NAME_ILLNESS | NOT_A_NAME_TRAIT
                    | NOT_A_NAME_DESCRIBING | NOT_A_NAME_CONDITION)

NAME_FILLER = frozenset("""
sorry oh ah ok okay so well hey hi hello hiya morning evening afternoon good hmm um err erm anyway
btw actually also and but yeah yes yep no nah right cool thanks thank please alright howdy
first quickly just then too lol haha
""".split())
NAME_FILLER_PHRASES = ("i forgot to say", "forgot to say", "i should say", "i should have said",
                       "should have said", "by the way", "for the record", "just so you know",
                       "forgot to mention", "i did not say", "i did not mention")

NAME_FOLLOWERS = frozenset("""
here there btw way hi hey hello hiya nice to meet you u thanks thank ta cheers too also again
lol haha x xo sorry but and so just actually ok okay right good great yes yeah yep im am is was
did do your my we us how pleased glad meet meetin
""".split())
NAME_PLACE_WORDS = frozenset("from in near at live living moved moving".split())
PLACE_JOIN = frozenset("in near at to from round around outside".split())
NAME_SAYS_ABOUT_ME = frozenset("""i i'm im ive i've live lives living work works working have
    has got like love hate prefer study studying play playing run running keep keep looking
    trying do doing need want grew raised born based married
    my our we we're we've myself""".split())

NAME_ASIDES = ("to be honest", "to be fair", "to be truthful", "if that helps", "if im honest",
               "i think", "i suppose", "i guess", "i expect", "by the way", "for what its worth",
               "honestly", "tbh", "btw", "anyway", "though", "actually")

NAME_ANSWER_HEDGES = re.compile(
    r"\b(?:" + "|".join(sorted(NAME_ASIDES + ("thanks", "thank you", "ta", "cheers"),
                                 key=len, reverse=True)) + r")\b", re.I)


def without_the_hedges(text):
    low = " ".join(str(text or "").lower().split())
    return " ".join(NAME_ANSWER_HEDGES.sub(" ", low).split()).strip(" ,.:;!?")

NAME_MIDDLE = r"(?:(?:actually|honestly|truthfully|officially|properly|tbh)\s+)?"

ANNOUNCED_NAME_PATTERNS = (
    re.compile(r"\bmy name(?:['\u2019]s| is|s)\s+" + NAME_MIDDLE +
               r"([a-z][a-z'-]{1,19})", re.I),
    re.compile(r"\bcall me\s+" + NAME_MIDDLE + r"([a-z][a-z'-]{1,19})", re.I),
    re.compile(r"\b(?:i am|i'm|im)\s+(?:called|named)\s+([a-z][a-z'-]{1,19})", re.I),
    re.compile(r"^\W*(?:the\s+)?names?(?:['\u2019]s)?\s+(?:is\s+)?" + NAME_MIDDLE +
               r"([a-z][a-z'-]{1,19})"
               r"(?=\s*[,.!?;:)\]]|\s*$|\s+(?:thanks|ta|cheers|btw|anyway|by the way|"
               r"nice to meet you|pleased to meet you|how are you|good to meet you)\b)", re.I),
)
GOES_BY_NAME = re.compile(r"\b(?:i|we)\s+go(?:es)?\s+by\s+([a-z][a-z'-]{1,19})", re.I)
CLAUSE_SPLIT = re.compile(r"\b(?:but|and|though|although)\b|[;,.!?]")
GUESSED_NAME_PATTERNS = (
    re.compile(r"\b(?:i am|i'm|im|we are|we're)\s+([A-Z][a-z'-]{1,19})\b"),
    re.compile(r"\b(?:i am|i'm|im|we are|we're)\s+([a-z][a-z'-]{1,19})\b", re.I),
    GOES_BY_NAME,
)
GO_BY_WAYS = frozenset("""bus car train coach tube tram plane bike foot taxi rail boat ship road
motorway""".split())


MONTHS = frozenset("""january february march april may june july august september october
november december jan feb mar apr jun jul aug sep sept oct nov dec""".split())
DAYS = frozenset("monday tuesday wednesday thursday friday saturday sunday weekend".split())
COUNTRIES = frozenset("""england scotland wales ireland britain uk america usa canada australia
new zealand france spain portugal italy germany greece turkey egypt morocco japan china korea
india pakistan thailand vietnam indonesia mexico brazil argentina peru chile colombia cuba iceland
norway sweden denmark finland netherlands belgium switzerland austria poland czech slovakia
hungary croatia serbia romania bulgaria russia ukraine israel south africa kenya nigeria ghana
philippines malaysia singapore""".split())
NOT_POSITIONS = frozenset("""upstairs downstairs inside outside indoors outdoors here there
abroad away""".split())
NOT_PLACES = MONTHS | DAYS | NOT_NAMES | NOT_POSITIONS | frozenset("""christmas easter summer winter autumn
spring morning afternoon evening night today tomorrow yesterday home work school uni
university college hospital doctor dentist""".split())

PLACE_AFTER = re.compile(
    r"\b(?:in|to|from|near|at|visit|visiting|visited|off to|trip to|travel to|went to)\s+"
    r"([A-Z][a-z]+(?:[ -][A-Z][a-z]+)?)\b")
PLACE_LOWER = re.compile(
    r"\b(?:going to|off to|flying to|fly to|travel(?:l)?ing to|trip to|holiday in|moving to|"
    r"heading to|visit(?:ing)?)\s+([a-z][a-z]{2,})\b", re.I)
NOT_A_FACT = frozenset("""again already actually anyway anyhow please sorry else though now
anybody anyone anything everywhere somewhere nothing something then though""".split())


ASK_WORDS = NOT_A_FACT | frozenset("""what who where when why how which whether can could
should would do does did""".split())


AFTER_THEN = frozenset("""do get go be have see try take make start learn visit eat stay move
buy save write read run walk swim cook book""".split())


def _fact_value(word):
    parts = re.split(r"([\s,]+)", str(word or "").strip())
    words = [parts[i] for i in range(0, len(parts), 2)]
    kept = []
    for i, value in enumerate(words):
        if value.lower() in AFTER_THEN and i and words[i - 1].lower() == "then":
            kept.append(parts[2 * i] + (parts[2 * i + 1] if 2 * i + 1 < len(parts) else ""))
            continue
        if value.lower() in ASK_WORDS:
            if value.lower() == "then" and words[i + 1:]:
                kept.append(parts[2 * i] + (parts[2 * i + 1] if 2 * i + 1 < len(parts) else ""))
                continue
            break
        kept.append(parts[2 * i] + (parts[2 * i + 1] if 2 * i + 1 < len(parts) else ""))
    out = "".join(kept).strip(" ,;:")
    if out.lower().endswith(" then"):
        out = out[:-5].rstrip(" ,;:")
    return out


HOME_IN = (r"(?:a|an|the|my|our|this|that)\s+(?:[a-z][a-z-]*\s+){0,2}"
           r"(?:flat|house|home|place|cottage|bungalow|farm|village|town|city|studio|area|"
           r"suburb|apartment|maisonette|caravan|boat)\s+(?:in|near|on|at|outside|round)\s+")

DWELLING = (r"(?:flat|house|home|cottage|bungalow|place|caravan|boat|hostel|studio|bedsit|"
            r"village|town|hamlet)")
HOME_DWELL = re.compile(
    r"\b(?:i|we)(?:\s?'?(?:m|re|ve|s)| am| are| have| has| had)?\s+"
    r"(?:(?:just|recently|finally|already|also|now)\s+)?"
    r"(?:(?P<stay>stay|stays|staying)|(?P<planned>moving|relocating|relocate|moving house)|"
    r"(?:live|living|lives|moved|moves|moving|settled|settling|relocating|relocated|relocate|"
    r"based))\s+"
    r"(?:(?:up|back|over|out|down|away)\s+)?(?:in|to|near|outside|round)\s+"
    r"(?:(?:a|an|the|our|my|their|his|her)\s+"
    r"(?:(?!(?:in|to|near|outside|round|at|by|with|from)\b)[a-z][a-z'-]*\s+){0,2}"
    + DWELLING + r"\s+)"
    r"(?:in|near|outside|round)\s+"
    r"(?P<place>[A-Za-z][A-Za-z'-]{1,}(?:[ -][A-Za-z][A-Za-z'-]{1,})?)\b", re.I)
HOME_PLACE = re.compile(
    r"\b(?:i|we)(?:\s?'?(?:m|re|ve|s)| am| are| have| has| had)?\s+"
    r"(?:(?:just|recently|finally|already|also|now)\s+)?"
    r"(?:(?P<stay>stay|stays|staying)|(?P<planned>moving|relocating|relocate|moving house)|"
    r"(?:live|living|lives|"
    r"moved|moves|moving|settled|settling|relocating|relocated|relocate|based|"
    r"rent|rents|renting|bought|buying))\s+"
    r"(?:(?:up|back|over|out|down|away|just|right|far)\s+)?"
    r"(?:(?:in|to|near|outside|round)\s+(?:" + HOME_IN + r")?|" + HOME_IN + r")"
    r"(?P<place>[A-Za-z][A-Za-z'-]{1,}(?:[ -][A-Za-z][A-Za-z'-]{1,})?)\b", re.I)
HOME_STOP = frozenset("""hope fear pain tears debt misery despair silence darkness denial poverty
sin sin sins the a an my our his her their this that these those with without for at on of two
three four five six ten twenty some any no such what which who whom when where why how much many
more less few lot lots bit town city village flat house home there here it them him me us you
case fact truth style general particular common between limbo fear
tonight today tomorrow yesterday now soon later always never usually often sometimes already still
once twice early late morning evening afternoon night weekend week month year day minute moment while
ago yet again anyway anymore then there here coming going and but so because or plus also
originally born from to into onto towards toward via until till before after about""".split())
FROM_PLACE = re.compile(
    r"(?:^were\b|\b(?:i'm|i've|i m|i am|i have|i was|im|ive|i|we're|we've|we re|we are|we have|"
    r"we were|weve|we))\s+"
    r"(?:(?:originally\s+|born\s+)?(?:come\s+)?from|born\s+in)\s+"
    r"([a-z][a-z'-]{2,}(?:[ -][a-z][a-z'-]{1,})?)\b", re.I)
FROM_MORE = re.compile(r"\boriginally\s+from\s+([a-z][a-z'-]{2,}(?:[ -][a-z][a-z'-]{1,})?)\b",
                       re.I)
FROM_GROWN = re.compile(
    r"\b(?:i|we)\s+(?:"
    r"(?:(?:grew|grows|grow)\s+up|(?:was|were|been|being)\s+(?:brought\s+up|raised))\s+"
    r"(?:in|near|just\s+outside|outside|close\s+to|on)\s+"
    r"(?:(?:a|an|the)\s+[a-z][a-z'-]{1,}(?:\s+[a-z][a-z'-]{1,})?\s+"
    r"(?:near|outside|close\s+to|just\s+outside|of)\s+)?"
    r"|(?:moved|move|moves|moved over|come|came|comes)\s+(?:here|over)\s+from\s+"
    r")([a-z][a-z'-]{2,}(?:[ -][a-z][a-z'-]{1,})?)\b", re.I)
GROWN_NOT_PLACE = frozenset("""care pride poverty debt fear church faith carehomes orphanage
carehome hostel bed sit benefit benefits hospital ill health politness""".split())
GROWN_ARTICLE = frozenset("a an some such every any this that these those".split())
GROWN_NEAR = re.compile(
    r"\b(?:near|outside|close\s+to|just\s+outside|of)\s+([a-z][a-z'-]{2,}(?:[ -][a-z][a-z'-]{1,})?)",
    re.I)


def grown_up_in_a_place(phrase):
    return _grown_up_in_a_place(phrase, "")


def _grown_up_in_a_place(phrase, text):
    words = str(phrase or "").split()
    if not words:
        return False
    low = [word.lower().strip(".,!?;:'\"") for word in words]
    if any(word in GROWN_NOT_PLACE for word in low):
        return False
    near = GROWN_NEAR.search(str(phrase or ""))
    if near and _place_name(near.group(1)):
        return True
    if low[0] in GROWN_ARTICLE:
        return False
    if low[0] == "the":
        return len(low) > 1 and low[1] in COUNTRY_ARTICLE
    return True


PLACE_MIDDLE = frozenset("""new old saint st san santa los las la le port cape fort great little
south north east west upper lower mount lake northern southern eastern western united""".split())
PLACE_NAME_FIRST = frozenset("""new saint st san santa los las la le mount lake fort cape
port sri""".split())
PLACE_LOWER_NAMED = re.compile(
    r"\b(?:going to|off to|flying to|fly to|travel(?:l)?ing to|trip to|holiday in|moving to|"
    r"heading to|visit(?:ing)?)\s+(" + "|".join(sorted(PLACE_NAME_FIRST)) + r")\s+"
    r"([a-z][a-z]{2,})\b", re.I)


def _an_everyday_word(word):
    low = str(word or "").lower()
    if not low:
        return True
    if low in normalize.LEXICON:
        return True
    for tail in ("es", "s"):
        if low.endswith(tail) and len(low) - len(tail) > 2 and low[:-len(tail)] in normalize.LEXICON:
            return True
    return False
COUNTRY_CAPS = {"uk": "UK", "us": "US", "usa": "USA", "uae": "UAE", "states": "States"}
COUNTRY_ARTICLE = frozenset("""uk us usa uae netherlands philippines bahamas maldives seychelles
states""".split())
PLACE_VERBS = frozenset("""bed sleep work school town sleep the a an see do get have try start stop
ask tell say make take give look feel stay live move eat drink buy sell pay book plan meet call go
come home there here it that this them him her me us you we my your our their about back out over
be used buy""".split())
HOME_LOOSE = re.compile(
    r"(?i:\b(?:i|we)(?:'?(?:ve|m|re|d)|\s+(?:have|has|had|am|are|was|were))?"
    r"\s+(?:now|still|just|recently|finally)?\s*"
    r"(?:liv(?:e|ing|ed)|mov(?:e|ed|ing)|settl(?:e|ed|ing)|relocat(?:e|ed|ing)|based|staying)\b)"
    r"[^.;!?]{0,30}?\b(?:in|to|at)\s+([A-Z][a-z]+(?:[ -][A-Z][a-z]+)?)\b")

SHORT_LIST = re.compile(r"^\W*(?:[A-Z][a-z]+)(?:\s*(?:,|and|or)\s*[A-Z][a-z]+)+\W*$")


DENIAL_WORDS = re.compile(r"(?:\bnot|\bnever|\bno longer|\b(?:is|are|was|were|do|does|did|can|"
                          r"could|would|should|has|have|had|wo|ca|ai)n'?t|\baint)\s+"
                          r"(?:really\s+|actually\s+|even\s+)?(?:a\s+|an\s+|any\s+|\bat all\s+)?$", re.I)


DENIAL_OF = re.compile(
    r"\b(?:i(?:m|'m| am)|we(?:re|'re| are))\s+(?:not|never|no longer)\s+"
    r"(?:really\s+|actually\s+|even\s+)?(?:a\s+|an\s+|any\s+)?"
    r"(?:(?P<food>allergic to\s+[a-z]+(?:(?:,| and| or)\s+[a-z]+){0,3})"
    r"|(?P<condition>coeliac|celiac|diabetic|asthmatic|epileptic|anaemic|anemic|"
    r"lactose intolerant|gluten intolerant)"
    r"|(?P<diet>vegan|vegetarian|pescatarian|flexitarian|veggie|plant[- ]based))", re.I)

DIET_PLANS = (r"(?:slimming world|weight watchers|intermittent fasting|whole ?30|omad|"
              r"carnivore|dukan|south beach|fast 800|5:2|16:8|4:3|"
              r"keto|paleo|atkins|low[- ]carb|mediterranean|gluten[- ]free|dairy[- ]free|"
              r"plant[- ]based|pescatarian|flexitarian|vegan|vegetarian)")
DIET_PLAN_WORD = (r"(?:(?:slimming world|weight watchers|intermittent fasting|whole ?30|omad|"
                  r"carnivore|dukan|south beach|fast 800|5:2|16:8|4:3|"
                  r"keto|paleo|atkins|low[- ]carb|mediterranean|gluten[- ]free|dairy[- ]free|"
                  r"plant[- ]based|vegan|vegetarian)|diet|dieting)")
DIET_OFF = re.compile(
    r"\b(?:i|we)\s*(?:'m|'re|m|re|am|are)\s+(?:not|no longer)\s+(?:on|doing)\s+"
    r"(?:a\s+|the\s+|an\s+)?(?P<plan>" + DIET_PLAN_WORD + r")\b"
    r"|\b(?:i|we)\s*(?:'m|'re|m|re|am|are)\s+(?:off|done with)\s+"
    r"(?:the\s+|a\s+|my\s+|that\s+)?(?P<off>" + DIET_PLAN_WORD + r")\b"
    r"|\b(?:i|we)\s+(?:came|come|came off|got|went)\s+off\s+"
    r"(?:the\s+|a\s+|my\s+)?(?P<gone>" + DIET_PLAN_WORD + r")\b"
    r"|\b(?:i|we)(?:'ve|ve|'d|d|\s+have|\s+had)?\s+"
    r"(?:stopped|quit|gave up|given up|packed in)\s+"
    r"(?:the\s+|my\s+|this\s+|on\s+)?(?:being\s+|doing\s+|eating\s+|going\s+)?"
    r"(?P<quit>" + DIET_PLAN_WORD + r")\b", re.I)

CLAUSE_EDGE = re.compile(r"[.;!?]|\b(?:and|but|so|because|though|although|which|while)\b|,", re.I)
NOT_HAVE = re.compile(r"\b(?:don'?t|do not|doesn'?t|doesnt|didn'?t|didnt|never|not|no longer|"
                      r"haven'?t|havent|hadn'?t|hadnt)\s+(?:have|has|had|own|owns|owned|keep|"
                      r"kept|got)\b|\b(?:have|has|had|got)\s+(?:no|not|never)\b",
                      re.I)
NOT_HAVE_LONGER = re.compile(
    r"\b(?:don'?t|do not|doesn'?t|doesnt|didn'?t|didnt|never|not|no longer|"
    r"haven'?t|havent|hadn'?t|hadnt)\s+(?:have|has|had|own|owns|owned|keep|"
    r"kept|got)\b", re.I)
HAVE_NONE = re.compile(
    r"\b(?:have|has|had|got)\s+(?:no|not|never)\s+"
    r"(?:(?:any|a|an|the|my|our|this|that|those|these)\b|pets?|dogs?|cats?|pupp(?:y|ies)|"
    r"kittens?|rabbits?|hamsters?|parrots?|goldfish|fish|horses?|animals?|guinea\s+pigs?|"
    r"gerbils?)\b", re.I)
A_COMPOUND_AFTER = re.compile(r"\s+[a-z]+s\b", re.I)
WITHOUT_ANIMAL = re.compile(
    r"\bwithout\s+(?:(?:a|an|any|the|my|our|his|her|their|these|those)\s+)?(?:[a-z-]+\s+)?"
    r"(?:pets?|dogs?|cats?|pupp(?:y|ies)|kittens?|rabbits?|hamsters?|parrots?|goldfish|fish|"
    r"horses?|animals?|guinea\s+pigs?|gerbils?)\b", re.I)
NOT_JUST = re.compile(r"\bnot\s+(?:(?:a|an|the|any|my|our)\s+)?$", re.I)
TAKEN_BACK_BEFORE = re.compile(
    r"\b(?:forget|forgot|forgetting)\s+(?:(?:about|with)\s+)?(?:(?:a|an|the|any|my|our|that|"
    r"this|those|these)\s+)?$", re.I)
BARE_NO = re.compile(r"^\s*(?:(?:no|not|nope)\b[\s,.]*){1,2}(?:(?:a|an|the|any|my|our)\s+)?$",
                     re.I)
NO_THEN_A_THING = re.compile(r"^\s*(?:no|nope)\b[\s,.]*(?:a|an|the|my|our|your|his|her|their)\s*$",
                             re.I)
GIVEN_AWAY = re.compile(r"\b(?:gave|give|given|giving|took|take|taken|returned|"
                        r"rehom(?:e|es|ed|ing)|got rid of)\b[^.;!?]{0,24}?\b(?:away|up|back|"
                        r"to a (?:friend|neighbour|neighbor|rescue)|to (?:my|his|her|their))\b|"
                        r"\brehom(?:e|es|ed|ing)\b[^.;!?]*", re.I)
NO_PETS = re.compile(r"\b(?:no|not got any|don'?t have any|dont have any|without any|"
                     r"never had any|no longer have any)\s+pets?\b", re.I)
EVERYTHING = "*"
DIED = re.compile(r"\b(?:died|dead|passed (?:away|on)|put (?:\S+ ){0,3}?down|"
                  r"put (?:\S+ ){0,3}?to sleep|euthanis(?:ed|e)|euthaniz(?:ed|e)|"
                  r"have (?:him|her|it|them) put (?:down|to sleep)|"
                  r"didn'?t make it|didnt make it|no longer with us)\b", re.I)
ANIMAL_DEATH = re.compile(r"\b(?:put (?:\S+ ){0,3}?(?:down|to sleep)|euthan\w*"
                           r"|no longer with us|didn'?t make it|had to be put)", re.I)
LOSS_ALL = re.compile(r"\b(?:both|all of them|all of the|all my|all our|every one|the pair|"
                      r"our pairs?)\b", re.I)
PET_PRONOUN = re.compile(r"\b(?P<pron>him|her|it|them|those|they|he|she)\b", re.I)
PLURAL_PRONOUN = frozenset("them those they".split())
HEDGE = re.compile(r"\b(?:don'?t|do not|didn'?t|did not|cant|can'?t|couldn'?t|could not|"
                   r"wouldn'?t|would not|might not|may not)\s+(?:think|know|remember|recall|say|"
                   r"mean|believe|reckon|suppose|guess|be sure|be certain)\b|"
                   r"\bnot sure|\bnot certain|\bno idea|\bprobably not|\bnot that i know|"
                   r"\bi doubt|\bdoubt it|\bnever said|\bnever told|\bnever mentioned|"
                   r"\bdidn'?t say|\bdidn'?t tell|\bdidn'?t mention|\bhaven'?t said|"
                   r"\bhavent said|\bhaven'?t told|\bhavent told|\bnot what i said", re.I)

ALLERGY = re.compile(r"\ballergic to ([a-z]+(?:[ ,]+(?:and )?[a-z]+){0,3})", re.I)
CONTRAST = re.compile(r"\b(?:allergic to|cant eat|can'?t eat|cannot eat|can not eat)\s+[a-z]+"
                      r"(?:(?:,| and| or)\s+[a-z]+){0,3}[\s,]+not\s+(?P<old>[a-z]+"
                      r"(?:(?:,| and| or)\s+[a-z]+){0,3})", re.I)
CANNOT_EAT = re.compile(r"\b(?:can'?t|cannot|can not)\s+(?:eat|have|drink|touch)\s+"
                        r"([a-z]+(?:[ ,]+(?:and |or )?[a-z]+){0,3})", re.I)
X_ALLERGY = re.compile(r"\b([a-z]+)\s+allerg(?:y|ies)\b", re.I)
NOT_AN_ALLERGEN = frozenset("""get gets getting got gotten have has had having develop develops
developed developing catch catches caught catching treat treats treated treating prevent prevents
prevented test tests tested testing cause causes caused causing trigger triggers triggered avoid
avoids avoiding manage manages managing notice notices noticed noticing control controls
controlled risk suffer suffers suffered experience make makes made become becomes became""".split())
VEGETARIAN = re.compile(r"\b(i(?:m|'m| am)|he(?:s|'s| is)|she(?:s|'s| is)|we(?:re|'re| are))\s+"
                        r"(?:a |an )?(vegan|vegetarian|pescatarian|flexitarian|veggie|veg|"
                        r"plant[- ]based)\b", re.I)
NO_MEAT = re.compile(r"\b(?:i|we) ?(?:dont|don'?t|do not|never|no longer) eat\s+"
                     r"(?:any |any more |more )?([a-z]+(?:(?:,| or| and) "
                     r"(?!i\b|im\b|i'm\b|ive\b|i'd\b|we\b|we're\b|and\b|but\b|so\b)[a-z]+)?)", re.I)
DRINK = frozenset("""alcohol booze wine wines beer beers lager lagers cider spirits gin vodka
whisky whiskey rum prosecco champagne cocktails cocktail sherry brandy""".split())
NO_DRINK = re.compile(
    r"\b(?:i|we)\s+(?:really\s+|just\s+|actually\s+)?"
    r"(?:don'?t|do not|dont|never|no longer)\s+(?:really\s+|just\s+|actually\s+)?drink\b"
    r"(?!\s+(?:enough|much|too much|a lot|loads|that much|as much|plenty|water|it\b))"
    r"(?:\s+(?:any\s?more|anymore|at\s+all|now))?\s*[.!]*$", re.I)
GAVE_UP_DRINK = re.compile(
    r"\b(?:i|we)\s*(?:have|'ve|had|ve)?\s*"
    r"(?:given\s+up|gave\s+up|quit|quitted|stopped|packed\s+in|cut\s+out)\s+"
    r"(?:the\s+|my\s+|all\s+)?(?:drinking|drink|alcohol|booze)\b"
    r"(?=\s*(?:[.,;!?]|$|\s+(?:any\s?more|anymore|at\s+all|now|for\s+good|and|but|so|"
    r"because|since|when|after|before|\d+\s+(?:years?|months?|weeks?|days?)(?:\s+ago)?|"
    r"years?\s+ago|months?\s+ago|weeks?\s+ago|ago|"
    r"in\s+\w+|at\s+\w+|last\s+\w+|this\s+\w+|on\s+\w+|over\s+\w+)))", re.I)
GAVE_UP_DRINK_THING = re.compile(
    r"\b(?:i|we)\s*(?:have|'ve|had|ve)?\s*"
    r"(?:given\s+up|gave\s+up|quit|quitted|stopped|packed\s+in|cut\s+out)\s+"
    r"(?:the\s+|my\s+|all\s+)?drinking\s+"
    r"(?P<thing>[a-z]+(?:\s+(?:or|and)\s+[a-z]+){0,3})", re.I)
NOT_DRINKING = re.compile(
    r"\b(?:i'?m|i\s+am|we'?re|we\s+are)\s+(?:a\s+|an\s+)?(?:"
    r"not\s+drinking(?!\s+(?:enough|much|too\s+much|a\s+lot|loads|as\s+much|that\s+much|"
    r"water|anything|any\s+water|it\b|at\s+the\s+(?:moment|minute)|these\s+days|for\s+now"
    r"|this\s+(?:week|month|year)|till\b|until\b))"
    r"(?:\s+(?:any\s?more|anymore|now))?"
    r"|off\s+the\s+(?:booze|drink)"
    r"|on\s+the\s+wagon|teetotal(?:ler)?|tee-total|non-drinker|nondrinker)\b", re.I)
NO_DRINK_THING = re.compile(
    r"\b(?:i|we)\s+(?:really\s+|just\s+|actually\s+)?"
    r"(?:don'?t|do not|dont|never|no longer)\s+drink\s+"
    r"(?P<thing>[a-z]+(?:\s+(?:or|and)\s+[a-z]+){0,3})", re.I)


def _the_drink_they_do_not_take(text):
    low = " ".join(str(text or "").split())
    if not low:
        return ""
    if NOT_DRINKING.search(low) or GAVE_UP_DRINK.search(low) or NO_DRINK.search(low):
        return "alcohol"
    for pattern in (NO_DRINK_THING, GAVE_UP_DRINK_THING):
        drank = pattern.search(low)
        if drank:
            thing = _finish(drank.group("thing"))
            words = [word for word in re.split(r"[ ,]+", thing.lower())
                     if word not in ("or", "and")]
            if words and all(word in DRINK for word in words):
                return thing
    return ""


MEAT = frozenset("""meat meats beef chicken pork lamb bacon ham sausages sausage fish seafood
prawns shellfish turkey duck goose venison steak mince gelatine gelatin""".split())
ANIMALS = frozenset("""dog puppy cat kitten rabbit hamster parrot goldfish fish horse pet""".split())
FREE_FROM = r"(?:dairy|gluten|lactose|nut|egg|sugar|soya|soy|wheat|yeast)[- ]free"
DIET_FREE_WORDS = frozenset("dairy gluten lactose nut egg sugar soya soy wheat yeast"
                            .split())
OTHER_DIET = re.compile(
    r"(?<!\w)(?P<subj>(?:he|she|they)(?:'s|'re|s|re)?|(?:my|his|her|their|our)\s+\w+)(?!\w)"
    r"[^.,;!?]{0,24}?"
    r"(?:(?:is|are|'s|'re|s|re)?\s*(?:a |an )?(?P<free>" + FREE_FROM + r")(?!\w)"
    r"|(?:is|are|'s|'re|s|re)?\s*(?:a |an )?(?P<word>vegan|vegetarian|pescatarian|flexitarian|"
    r"veggie|gluten[ -]free|dairy[ -]free|lactose[ -]free|wheat[ -]free|sugar[ -]free|"
    r"low[ -]carb|plant[ -]based|keto|paleo|carnivore)(?!\w)"
    r"|(?:doesn'?t|does not|doesnt|don'?t|do not|dont|never|won'?t|wont|can'?t|cant)\s+"
    r"eats?\s+(?:any\s+|any more\s+|much\s+)?"
    r"(?P<food>[a-z]+(?:\s+(?:or|and)\s+[a-z]+)?))", re.I)
THEIR_BACK = re.compile(
    r"(?<!\w)(?P<subj>(?:he|she|they)(?:'s|'re|s|re)?|(?:my|his|her|their|our)\s+\w+)(?!\w)"
    r"(?P<gap>[^.,;!?]{0,24}?)\b(?P<verb>eats|eat|likes|like|loves|love|does|do|did)\b\s+"
    r"(?:(?P<emph>eat|eats|like|likes|love|loves)\s+)?"
    r"(?:now\s+|actually\s+|really\s+)?"
    r"(?P<food>them|it|that|[a-z]+(?:\s+(?:or|and)\s+[a-z]+)?)", re.I)
A_CORRECTION = re.compile(r"\b(?:actually|no|nope|sorry|wait|oh|now|again|rather|really|"
                          r"these\s+days|after\s+all)\b", re.I)
A_NEGATOR_IN_BETWEEN = re.compile(r"\b(?:not|never|no\s+longer|n'?t|nt)\b|\wnt\b", re.I)
ALLERGEN_PLURALS = {"nut": "nuts", "peanut": "peanuts", "walnut": "walnuts",
                    "hazelnut": "hazelnuts", "cashew": "cashews", "almond": "almonds",
                    "prawn": "prawns", "egg": "eggs", "strawberry": "strawberries",
                    "kiwi": "kiwis", "berry": "berries", "sesame": "sesame", "soya": "soya"}
ONE_MORE_FOODS = frozenset("""
    milk dairy cheese butter cream yoghurt yogurt lactose egg eggs
    nut nuts peanut peanuts walnut walnuts hazelnut hazelnuts cashew cashews almond almonds
    pistachio pistachios pecan pecans brazil macadamia chestnut chestnuts pine
    wheat gluten flour bread pasta semolina spelt barley rye oats oat couscous noodles
    soya soy tofu sesame tahini mustard celery celeriac lupin corn maize rice potato potatoes
    fish salmon cod tuna haddock prawn prawns shellfish crab crabs lobster mussels oysters
    squid scallops clam clams anchovy anchovies sardine sardines mackerel trout
    meat chicken beef pork lamb bacon ham sausage sausages turkey duck venison gelatine
    gelatin yeast sugar honey chocolate coffee caffeine alcohol wine beer vinegar
    feta halloumi parmesan mozzarella cheddar brie ricotta paneer stilton gouda edam
    strawberry strawberries kiwi kiwis berry berries banana bananas apple apples
    pear pears peach peaches plum plums cherry cherries grape grapes melon melons
    mango mangoes pineapple avocado coconut tomato tomatoes onion onions garlic
    pepper spices spice curry chilli chili cinnamon cloves ginger mint
    sulphites sulphite sulfites sulfate sulphur sulfites msg aspartame sweetener
    preservatives colourings colouring dye colour color additives
    """.split())
ONE_MORE_HEAD = re.compile(
    r"^(?:(?:it'?s|its|it is|that'?s|thats|this is|these are|those are)|and|also|plus|oh|right|but|"
    r"so|yeah|yes|then|actually|sorry|true|wait|no wait|"
    r"hold on|i think|i reckon|i suppose|maybe|probably|possibly|i think maybe)\b[\s,]*", re.I)
ONE_MORE_TAIL = re.compile(r"[\s,]*(?:\btoo\b|\bas well\b|\balso\b|\bi suppose\b)[\s.!?]*$",
                           re.I)
NOT_THEIRS = re.compile(r"\b(?:want|wants|wanted|need|needs|needed|fancy|fancied|"
                        r"would like|wish i|wishes|hate|hates|hated|dislike|dislikes|"
                        r"disliked|can'?t stand|cant stand|not a fan of|afraid of|scared of|"
                        r"thinking (?:about|of)|thought (?:about|of)|considering|considered|"
                        r"might|maybe|perhaps|hoping|hope to|planning (?:to|on)|plan to|"
                        r"one day|some day|someday|eventually|dream(?:ing)? of|"
                        r"looking at|shopping for|researching|used to|use to|"
                        r"asked for|asking for|been asking|begging for|desperate for|"
                        r"mad on|mad for|keen on|keen to get|after a|after an|"
                        r"growing up|as a kid|as a child|when i was (?:little|younger|a kid|"
                        r"a child|small))\b", re.I)
A_WISH = re.compile(r"\b(?:want|wants|wanted|would like|wish i|wishes|fancy|fancied|"
                    r"need|needs|needed|thinking (?:about|of)|thought (?:about|of)|considering|"
                    r"considered|might|maybe|perhaps|hoping|hope to|planning (?:to|on)|plan to|"
                    r"one day|some day|someday|eventually|dream(?:ing)? of|looking at|"
                    r"shopping for|researching|going to get|gonna get)\b", re.I)


NOT_THEIRS_AFTER = re.compile(r"^\s*(?:,?\s*(?:when i was|as a (?:kid|child)|growing up|"
                              r"years ago|back (?:then|when)|as a young|later on))\b", re.I)
THEIRS_WORD = re.compile(r"\b(?:my|our|their|his|her|have|has|had|got|own|owns|owned|keep|"
                         r"keeps|kept|walk|walks|walked|feed|feeds|fed|bought|rescued|"
                         r"adopted|rehomed)\b", re.I)


COMING_HOME = re.compile(r"\b(?:getting|adopting|rehoming|picking (?:up|out)|collecting|"
                         r"bringing home|waiting for)\b", re.I)
ON_ITS_WAY_BETWEEN = re.compile(r"^\s*(?:(?:a|an|another|one|two|three|four|five|some|a "
                                r"rescue|a new|some new|my new|our new|the new|a little|"
                                r"a small|[0-9]+)\s+)*$", re.I)


def _coming_home(text, start):
    window = CLAUSE_EDGE.split(text[max(0, start - 60):start])[-1]
    for cue in COMING_HOME.finditer(window):
        between = window[cue.end():]
        if not ON_ITS_WAY_BETWEEN.match(between):
            continue
        return True
    return False


def _only_wanted(text, start, end):
    window = CLAUSE_EDGE.split(text[max(0, start - 60):start])[-1]
    for cue in NOT_THEIRS.finditer(window):
        if THEIRS_WORD.search(window[cue.end():]):
            continue
        return True
    return bool(NOT_THEIRS_AFTER.match(text[end:end + 30]))


def _not_theirs(animal, text, start, end):
    record = {"animal": animal, "name": None, "not_theirs": True}
    if _a_wish_for(text, start):
        record["wanted"] = True
    return record


def _a_wish_for(text, start):
    window = CLAUSE_EDGE.split(text[max(0, start - 60):start])[-1]
    if THEIRS_WORD.search(window):
        return False
    return bool(A_WISH.search(window))


CONDITION = re.compile(r"\b(?:i(?:m|'m| am)|we(?:re|'re| are))\s+(?:a |an )?"
                       r"(coeliac|celiac|diabetic|asthmatic|epileptic|anaemic|anemic|"
                       r"lactose intolerant|gluten intolerant)\b", re.I)
DIET_NAMES = {"veggie": "vegetarian"}
DIET_WORDS = frozenset("""vegan vegetarian veggie veg pescatarian flexitarian plant based raw
gluten-free dairy-free lactose-free nut-free egg-free sugar-free soya-free soy-free
wheat-free yeast-free keto paleo low-carb carnivore""".split())
SOBER_WORDS = frozenset("teetotal teetotaller tee-total non-drinker nondrinker sober".split())
DIET_NAMED = re.compile(r"\b(?:i'm|im|i've|ive|i am|i have)\b(?:\s+been)?(?:\s+\w+){0,2}?\s+"
                        r"(?P<named>" + DIET_PLANS + r")\s+diet\b", re.I)
DIET_UNDERWAY = re.compile(
    r"\b(?:i(?:m|'m| am)|we(?:re|'re| are)|i(?:'ve|ve| have))\b(?:\s+been)?\s+"
    r"(?:(?:on|doing|trying|starting|started|back on|gone)\s+(?:a\s+|the\s+|an\s+)?"
    r"(?:(?P<named>" + DIET_PLANS + r")\b|(?P<diet>diet)\b)"
    r"|(?P<dieting>dieting)\b)", re.I)
DIET_BARE = re.compile(
    r"\b(?:i'm|im|i am|i've been|ive been)\s+(?P<bare>" + FREE_FROM + r"|"
    r"low[- ]carb|plant[- ]based|carnivore|keto|paleo|pescatarian|flexitarian)\b", re.I)
DIET_DOING = re.compile(
    r"\b(?:i'm|im|i am|i've been|ive been|i have been)\s+"
    r"(?P<doing>trying to eat less|trying to eat more|trying to cut out|"
    r"trying to give up|cutting out|cutting down on|cut back on|giving up|avoiding|"
    r"eating less|eating more|not eating|off|doing)\s+(?P<what>[a-z][a-z' -]{1,38})", re.I)
DIET_WHAT = frozenset("""sugar sugars carbs carbohydrate carbohydrates dairy meat meats fish
seafood gluten wheat eggs egg alcohol booze caffeine fizzy chocolate sweets bread pasta rice
potatoes protein veg vegetables fruit junk snacks takeaway takeaways processed salt fat
calories soya soy nuts junk-food processed-food fizzy-drinks red-meat white-bread
cheese milk butter coffee tea wine beer lager cider""".split())
DIET_WHAT_TWO = ("dry january", "sober october", "clean eating", "junk food",
                 "processed food", "fizzy drinks", "red meat", "white bread")


def _the_food_named(raw):
    words = " ".join(str(raw or "").lower().split()).split()
    if not words:
        return ""
    two = " ".join(words[:2])
    if words[0] not in DIET_WHAT and two not in DIET_WHAT_TWO:
        return ""
    kept = []
    for word in words:
        if word in DIET_STOP_A_WAY_OF_EATING:
            break
        kept.append(word)
    return " ".join(kept)


DIET_QUIT = re.compile(
    r"\b(?:i|we)\s*(?:have|'ve|had|ve)?\s*"
    r"(?P<doing>gave up|given up|give up|gives up|quit|quitted|stopped|packed in|cut out|"
    r"cut back on|cut down on)\s+(?:the\s+|my\s+|all\s+|our\s+)?(?P<what>[a-z][a-z' -]{1,38})",
    re.I)
EATING_VERB = frozenset("eating drinking having taking".split())
QUIT_AS_DOING = {"gave up": "giving up", "given up": "giving up", "give up": "giving up",
                 "gives up": "giving up", "quit": "giving up", "quitted": "giving up",
                 "stopped": "giving up", "packed in": "giving up",
                 "cut out": "cutting out", "cut back on": "cutting down on",
                 "cut down on": "cutting down on"}


def _a_way_of_eating_said_with_a_verb(text):
    for match in DIET_DOING.finditer(text):
        food = _the_food_named(match.group("what"))
        if not food:
            continue
        return match.group("doing").lower() + " " + food
    for match in DIET_QUIT.finditer(text):
        what = match.group("what").split()
        food = _the_food_named(" ".join(what))
        if not food and what[0] in EATING_VERB:
            food = _the_food_named(" ".join(what[1:]))
        if not food:
            continue
        doing = match.group("doing").lower()
        return QUIT_AS_DOING.get(doing, doing) + " " + food
    return ""


DIET_BACK = re.compile(
    r"\b(?:i'm|im|i am|i've|ive|i have|i'd|we're|were|we are|we've)\s+(?:now\s+)?"
    r"back\s+on\s+(?P<back>[a-z][a-z' -]{1,38})"
    r"|\b(?:i'm|im|i am|i've|ive|i have|i'd|we're|were|we are|we've)\s+"
    r"(?:(?:back\s+to|gone\s+back\s+to|started|start|just)\s+)?(?:eating|having)\s+"
    r"(?P<eat>[a-z][a-z' -]{1,38}?)\s+again\b", re.I)


DIET_STOP_A_WAY_OF_EATING = frozenset("""for since because cos till until and but so as to
with from at in on the a an my our this that it all last next ago yesterday today years months
weeks days year month week""".split())
NO_EAT_QUALIFIER = frozenset("red white processed raw oily fatty farmed".split())
PETS = re.compile(r"\b(dog|puppy|cat|kitten|rabbit|hamster|guinea pig|parrot|goldfish|fish|horse)"
                  r"(?:s|es)?\b", re.I)
NOT_A_COUNT_GAP = r"(?!(?:and|or|but|plus|with|my|our|his|her|their|the|a|an|is|are|was|were|has|have|had|then|so|because)\b)"
AGE_GAP_WORD = (r"(?!(?:year|years|yr|yrs|month|months|mth|mths|week|weeks|wk|wks|day|days|"
                r"hour|hours|minute|minutes)\b)")
PET_COUNT = re.compile(r"\b(one|two|three|four|five|six|seven|eight|nine|ten|\d{1,2}|"
                       r"a couple of|a pair of|couple of)\s+" + NOT_A_COUNT_GAP +
                       r"(?:" + NOT_A_COUNT_GAP + AGE_GAP_WORD + r"[a-z-]+\s+){0,2}$", re.I)
PET_COUNT_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
                   "seven": 7, "eight": 8, "nine": 9, "ten": 10, "a couple of": 2,
                   "a pair of": 2, "couple of": 2}
NAME_WORD = re.compile(r"^[A-Za-z][a-z'-]{1,19}$")
NOT_A_NAME = frozenset("""and or but the a an my our his her its their is are was were has have
had got both they them one all each two three four five six seven eight nine ten of to for with
called named too also as who that which name names nickname known rescued rescue puppy kitten
isnt isn't arent aren't wasnt wasn't doesnt doesn't dont don't didnt didn't cant can't wont won't
not never neither nor hardly
dog cat pets animals years
year months month old new little big small
again now then please yet already still just even never before after later soon today tonight
tomorrow yesterday ever anything something
him her it them he she they us me you there""".split())
ANOTHER_ANIMAL = re.compile(
    r"\b(?:another|other|second|third|fourth|fifth|sixth|seventh|new|one more)\s+"
    r"(?:[a-z-]+\s+){0,1}$", re.I)
ALSO_HAVE = re.compile(r"\b(?:also|too)\s+(?:have|has|had|got|own|owns|keep|keeps|rehomed"
                       r"|adopted|took in|rescued|named)\b"
                       r"|\b(?:have|has|had|got|own|owns|keep|keeps)\s+also\b", re.I)
NOT_THEIR_DETERMINER = frozenset("his her their".split())
PET_TITLE = re.compile(r"(?i:(?:mrs|mr|ms|miss|mx|doctor|professor|prof|dr|captain|princess|"
                       r"prince|saint|dame|lady|lord|sir|st)\.?)")
PET_VERB_NAME = re.compile(
    r"\b(?:named|called)\s+(?:(?P<whose>the|our|my|a|an|their|his|her)\s+)?"
    r"(?:dog|puppy|cat|kitten|rabbit|hamster|parrot|goldfish|fish|horse)s?\s+"
    r"(?:(?P<title>" + PET_TITLE.pattern + r")\s+)?"
    r"(?P<name>[A-Za-z][A-Za-z'-]{1,19})\b")
PET_PRONOUN_NAME = re.compile(r"\b(?:named|called)\s+(?:him|her|it|them)\s+"
                              r"([A-Za-z][A-Za-z'-]{1,19})\b")
NOT_THE_VERB_NAME = frozenset("""
after before because for in into out up down over round around off on at with to from by since
while and or but so then if once already now today tomorrow yesterday tonight
house home flat garden yard boat farm stable
""".split())
NOT_A_PRONOUN_NAME = frozenset("him her it them he she they us me you".split())
PET_NAME = re.compile(
    r"\b(?:called|named)\s+(?:(?P<title>" + PET_TITLE.pattern + r")\s+)?"
    r"(?P<name>[A-Z][a-z'-]+|[a-z][a-z'-]+)\b")
NAME_AFTER_TITLE = frozenset(("who",))


def _with_title(match):
    title = match.group("title")
    name = match.group("name")
    if not title:
        return name
    if name.lower() in NOT_A_NAME and name.lower() not in NAME_AFTER_TITLE:
        return title.rstrip(".")
    return (title + " " + name) if any(char.isupper() for char in title + name) else \
        " ".join(word[:1].upper() + word[1:] for word in (title + " " + name).split())


def _name_at(match):
    return match.start("title") if match.group("title") else match.start("name")


PET_IS_NAME = re.compile(r"\b(?:dog|puppy|cat|kitten|rabbit|hamster|parrot|goldfish|fish|horse)s?\s+"
                         r"(?:is|are)\s+(?:called\s+|named\s+)?(?:(?P<title>" + PET_TITLE.pattern +
                         r")s?\s+)?(?P<name>[A-Z][a-z'-]{1,20})\b")
PET_POSSESSIVE_NAME = re.compile(
    r"\b(?:the|my|our|your|his|her|its|their)\s+(?:new\s+|little\s+|old\s+|rescue\s+)?"
    r"(?:dog|puppy|cat|kitten|rabbit|hamster|parrot|goldfish|fish|horse)s?\s*(?:'s|s)?\s+"
    r"name\s*(?:'s|is|was)\s+(?:(?P<title>" + PET_TITLE.pattern + r")\s+)?"
    r"(?P<name>[A-Za-z][A-Za-z'-]{1,19})\b", re.I)
PET_APPOSITIVE = re.compile(
    r"\b(?:dog|puppy|cat|kitten|rabbit|hamster|parrot|goldfish|fish|horse)\b[^,.;!?]{0,24},\s*"
    r"([a-zA-Z][a-zA-Z'-]{1,20})\s*(?=$|[,.;!?]|\s+(?:is|was|and|has|needs|loves|hates|does)\b)")
PET_BEFORE_FACT = re.compile(
    r"\b(?:dog|puppy|cat|kitten|rabbit|hamster|parrot|goldfish|fish|horse)s?\s+"
    r"(?P<name>[A-Za-z][A-Za-z'-]{1,19})\s+(?:is|was|are|were)\b")
NOT_A_NAME_MIDDLE = frozenset("""
upstairs downstairs outside inside indoors outdoors away home back next front behind there here
nearby around about settled used fine
""".split())
PET_ANIMALS = frozenset("""
dog puppy cat kitten rabbit hamster parrot goldfish fish horse dogs puppies cats kittens rabbits
hamsters parrots fish horses animal pet
""".split())
ANIMAL_KINDS = {
    "dog": "dog", "dogs": "dog", "puppy": "dog", "puppies": "dog",
    "cat": "cat", "cats": "cat", "kitten": "cat", "kittens": "cat",
    "rabbit": "rabbit", "rabbits": "rabbit",
    "hamster": "hamster", "hamsters": "hamster",
    "parrot": "parrot", "parrots": "parrot",
    "fish": "fish", "goldfish": "fish",
    "horse": "horse", "horses": "horse",
}


def another_animal(text, animal):
    kind = ANIMAL_KINDS.get(str(animal or "").strip().lower(), "")
    if not kind:
        return ""
    for word in re.findall(r"[a-z]+", str(text or "").lower()):
        other = ANIMAL_KINDS.get(word, "")
        if other and other != kind:
            return other
    return ""
NOT_A_PET_NAME = frozenset("""
today tomorrow yesterday tonight now soon again though although instead already still even too
also either rather which who whose what when where why how and but so or if then than there here
vet vets help advice question thing things lot lots bit one two three years year months weeks days
man men woman women boy girl child kid kids people person male female puppy dog cat kitten pet
he she they it them i we you every each some any all one ones day days week weeks month months
year years after before from with without about over under round around back away out off
""".split())
PET_NAME_ONLY = re.compile(r"\b(?:her|his|its)\s+name(?:'s| is)\s+([A-Za-z][a-z'-]{1,20})\b|"
                           r"\b(?:she|he|it)(?:'s|s)\s+(?:called|named)\s+([a-zA-Z][a-z'-]{1,20})\b|"
                           r"\b(?:we|i)(?:'ve| have)?\s+(?:named|called|call)\s+(?:him|her|it)\s+"
                           r"([a-zA-Z][a-zA-Z'-]{1,20})\b")
PET_NAME_ONLY_LOWER = re.compile(
    r"\b(?:her|his|its|their)\s+names?\s+(?:'s|is|was|actually|really)\s+"
    r"([a-z][a-z'-]{1,20})\b", re.I)
A_COMMENT_ON_THE_NAME = frozenset("""long short hard easy difficult tricky complicated silly daft
weird funny strange odd boring lovely nice horrible stupid ridiculous impossible embarrassing
forgettable unpronounceable common rare plain simple weird rubbish""".split())


def _a_name_for_the_pet(word, strict_ly=True):
    low = str(word or "").lower()
    if not word or _not_a_name(word, strict_ly=strict_ly) or low in A_COMMENT_ON_THE_NAME:
        return None
    return word
PET_NAME_ASKED = re.compile(
    r"\bwhat(?:'s| is|s)? (?:its|his|her|their) name\b|"
    r"\bwhat (?:do|shall|should) (?:i|we) call (?:it|him|her|them)\b|"
    r"\bwhat(?:'s| is|s)? the name of (?:your|the)\s+(?:dog|cat|puppy|kitten|rabbit|hamster|pet)\b",
    re.I)
USER_NAME_ASKED = re.compile(
    r"\bwhat(?:'s| is|s)? your name\b|\bwhat (?:do|shall|should) i call you\b|"
    r"\bwho am i (?:speaking|talking|chatting) to\b|\bwhat are you called\b|"
    r"\bdon'?t know (?:your name|what your name is)\b|"
    r"\bdon'?t know it yet\b|\byour name (?:again|then)\b|"
    r"\bhaven'?t (?:said|told me) your name\b", re.I)
NOT_A_NAME_THING = frozenset("""hard easy tough great rubbish weird strange wrong right broken
amazing lovely nice better worse possible impossible funny awful terrible horrible annoying
confusing complicated tricky simple stupid mad""".split())


JOB_WORDS = frozenset("""teacher nurse doctor dentist engineer chef waiter waitress builder driver
farmer student accountant lawyer manager receptionist cashier soldier police mechanic hairdresser
barber baker butcher postman designer developer programmer analyst consultant researcher
scientist professor lecturer pilot cleaner decorator handyman gardener carer midwife pharmacist
vet secretary clerk apprentice volunteer""".split())

NUMBER_WORDS = frozenset("""one two three four five six seven eight nine ten eleven twelve
thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty thirty forty fifty sixty
seventy eighty ninety hundred thousand million billion dozen zero none""".split())


def _names_something_else(low):
    if not low:
        return True
    if (low in DAYS or low in MONTHS or low in COUNTRIES or low in NOT_PLACES
            or low in NUMBER_WORDS or low in JOB_WORDS):
        return True
    try:
        from ..knowledge import costs, travel
        if low in travel.CITIES or low in costs.JOBS:
            return True
    except Exception:
        pass
    return False


def reads_as_a_name(word):
    if not bare_name(word):
        return None
    low = _finish(str(word or ""))
    if not low or low in NOT_A_NAME_THING or low in NOT_A_NAME_TRAIT \
            or _names_something_else(low):
        return None
    name = _name("im " + low)
    if name and _finish(name) == low:
        return name
    return None


NAME_ANSWER_ANNOUNCED = re.compile(
    r"^\s*(?:it's|its|it is|this is|that'?s|the name'?s|the name is|the names|the name's|"
    r"im|i'm|i am)\s+([a-z][a-z'-]{1,19})\s*[.!]?\s*$", re.I)
NAME_ANSWER_ANNOUNCED_LAST = re.compile(
    r"(?:^|\W)(?:it's|its|it is|this is|that'?s|my name'?s|my name is|call me|"
    r"im|i'm|i am)\s+([a-z][a-z'-]{1,19})\s*[.!]?\s*$", re.I)


NAMES_OFFERED = re.compile(
    r"\bfor\s+(?:a|an|your)\s+(?P<animal>[a-z]+)\s*:\s*(?P<list>[^.]*?)\.", re.I)
NAME_PICK_ASK = re.compile(
    r"\b(?:what|which)\s+(?:shall|should|would|could|do|can|will|might)\s+(?:i|we|you)\s+"
    r"(?:call|name)\s+(?:it|him|her|them|this|that|(?:my|our|the|your)\s+"
    r"(?:[a-z]+\s+)?(?:" + "|".join(sorted(PET_ANIMALS)) + r"))\b"
    r"|\bwhat(?:'s|s| is)\s+(?:a|some)\s+good\s+name\b"
    r"|\b(?:any|some)\s+(?:name\s+)?ideas?\s+for\s+(?:a\s+)?names?\b", re.I)
BUDGET = re.compile(r"\bbudget\b[^.\d]{0,40}?((?:under |over |less than |up to )?[£$€]?\s?"
                    r"\d[\d,.]*(?:\s?(?:pounds|quid|euros?|dollars?|grand|bucks|k)\b)?)", re.I)
SPEND_BUDGET = re.compile(r"\b(?:i|we)(?:'?ve|\s+have)\s+(?:only\s+)?(?:got\s+)?"
                          r"((?:about |around |up to |under |max(?:imum)? )?[£$€]?\s?\d[\d,.]*"
                          r"(?:\s?(?:pounds|quid|euros?|dollars?|grand|bucks|k)\b)?)\s*(?:to spend|on it|budget)",
                          re.I)
_INTENT = (r"(?:want|wanna|wanted|need|needed|would like|'d like|d like|plan to|planning to|"
           r"am going|are going|hoping|have|'ve|got|can|could|will|'ll|must|should|try to|"
           r"trying to)")
_WHAT_THEY_MEAN_TO_DO = (r"(?:spend|keep (?:it|the cost|costs|the budget|the price)|come in|stay|"
                         r"be (?:under|below|within)|keep to)")
_A_CAP = (r"(?:under|below|less than|up to|no more than|not more than|at most|max(?:imum)?|"
          r"within|around|about|circa)?\s*")
_MONEY_AGAIN = (r"((?:" + _A_CAP + r")(?:[\u00a3$\u20ac]\s?\d[\d,.]*|"
                r"\d[\d,.]*\s?(?:pounds?|quid|euros?|dollars?|bucks|grand|k)\b))")
INTENDED_SPEND = re.compile(
    r"\b(?:i|we)\s+(?:only\s+)?" + _INTENT + r"\s+(?:only\s+)?(?:to\s+)?" +
    _WHAT_THEY_MEAN_TO_DO + r"\b[^.\d]{0,24}?" + _MONEY_AGAIN, re.I)
THE_THING_MAY_COST = re.compile(
    r"\b(?:it|this|that|the whole thing)\s+(?:has to|needs to|should|must|will|can)" +
    r"\s+(?:only\s+)?(?:come in|stay|be|keep)\b[^.\d]{0,16}?" + _MONEY_AGAIN, re.I)
ALL_I_CAN_DO = re.compile(
    r"\b" + _MONEY_AGAIN + r"\s+is\s+all\s+(?:i|we)\s+(?:can|could|have|got|afford|manage)"
    r"\s+(?:do|afford|manage|spend|stretch to|stretch|pay)\b", re.I)
SPEND_FOR = re.compile(r"\b(?:i|we)(?:'?ve|'d|\s+have|\s+had)\s+(?:only\s+)?(?:got\s+|have\s+)?"
                       r"((?:about |around |up to |under |max(?:imum)? )?[£$€]?\s?\d[\d,.]*"
                       r"(?:\s?(?:pounds|quid|euros?|dollars?|grand|bucks|k)\b)?)"
                       r"\s+for\s+(?:a|an|the|my|our|his|her|their|your|another|\w+'s)\s+\w",
                       re.I)
MONEY_AMOUNT = (r"((?:(?:about |around |up to |under )?"
                r"(?:[£$€]\s?\d[\d,.]*|\d[\d,.]*\s?(?:pounds?|quid|euros?|dollars?|"
                r"bucks|grand|k)\b)))")
ONLY_HAVE = re.compile(r"\b(?:i|we)\s+only\s+(?:have|had|got)\s+" + MONEY_AMOUNT, re.I)
SPEND_BUDGET_NOW = re.compile(r"\b(?:i|we)(?:'ve| have)\s+only\s+(?:got\s+|have\s+)?"
                              r"((?:about |around |up to |under |max(?:imum)? )?[£$€]?\s?"
                              r"\d[\d,.]*(?:\s?(?:pounds|quid|euros?|dollars?|grand|bucks|k)\b)?)\s*"
                              r"(?:now|these days|at the moment|left)\b", re.I)
MONEY_FIGURE = (r"(?:[\u00a3$\u20ac]\s?\d[\d,.]*|\d[\d,.]*\s?"
                r"(?:pounds?|quid|euros?|dollars?|bucks|grand|k)\b)")
STRETCH_BUDGET = re.compile(
    r"\b(?:i|we)\s+(?:could|can|might|may|would|'d)\s+"
    r"(?:maybe\s+|probably\s+|possibly\s+)?"
    r"(?:stretch\s+(?:it\s+)?(?:up\s+)?to|go\s+up\s+to|push\s+(?:it\s+)?(?:up\s+)?to)\s+"
    r"((?:about |around |up to |maybe |just )?"
    r"(?:" + MONEY_FIGURE + r"|\d[\d,.]*(?=\s*(?:$|[.,;!?]|\bat a push\b|\bmax\b|"
    r"\btops\b|\bnow\b|\bfor\b))))", re.I)
INCOME_PERIOD = re.compile(r"\s*(?:a|per|each|every)\s+(?:month|week|year|fortnight)\b", re.I)
INCOME_QUALIFIER = re.compile(
    r"(?:\s+(?:between\s+(?:us|the\s+two\s+of\s+us)|together|in\s+total|altogether|combined|"
    r"after\s+tax|after\s+taxes|after\s+deductions|after\s+national\s+insurance|after\s+ni|"
    r"after\s+stoppages|net|clear|clean|now|currently|each|both)\b){0,3}", re.I)
INCOME_RATE = re.compile(r"\s*(?:an?|per|each|every|/)\s*(?:hour|hr|day|shift|weekend)\b", re.I)
INCOME = re.compile(r"\b(?:i|we)(?:'m|m\b| am| are)?\s+(?:only\s+)?(?:"
                    r"(?:earn|make|get paid|get|bring home|take home|be on|am on)"
                    r"|(?:on))\s+"
                    r"((?:about |around |roughly |up to |just )?(?:[£$€]\s?\d[\d,.]*|"
                    r"\d[\d,.]*\s?(?:pounds?|quid|euros?|dollars?|bucks|grand|k)\b))", re.I)
INCOME_BARE = re.compile(r"\b(?:i|we)(?:'m|m\b| am| are)?\s+(?:only\s+)?(?:"
                         r"earn|make|get paid|get|bring home|take home|on)\s+"
                         r"((?:about |around |roughly |up to |just )?\d[\d,.]*)", re.I)
INCOME_A_YEAR = (
    re.compile(r"\b(?:i|we)(?:'m|m\b| am| are)?\s+(?:only\s+)?"
               r"(?:earn|earns|earned|get paid|bring home|take home|be on|am on|on)\s+"
               r"((?:about |around |roughly |up to |just )?"
               r"(?:[£$€]\s?\d[\d,.]*|\d[\d,.]*(?:\s?(?:pounds?|quid|grand|k)\b)?))", re.I),
    re.compile(r"\b(?:my|our)\s+(?:salary|wages?|pay|income)\s*(?:is|was|'s|are)?\s*"
               r"((?:about |around |roughly )?"
               r"(?:[£$€]\s?\d[\d,.]*|\d[\d,.]*(?:\s?(?:pounds?|quid|grand|k)\b)?))", re.I),
)
BARE_BUDGET_LEAD = (r"(?:(?:anything|anythink|something|somewhere|maybe|probably|honestly|"
                    r"i dunno|dunno|i reckon|i'd say|say|i was thinking|i'm thinking|im thinking|"
                    r"i thought|thinking|i was going to say)\s+){0,3}")
BARE_BUDGET = re.compile(r"^\W*" + BARE_BUDGET_LEAD +
                         r"((?:(?:under|below|less than|up to|around|about|max(?:imum)?|"
                         r"no more than|not more than)\s*)"
                         r"[£$€]?\s?\d[\d,.]*(?:\s?(?:pounds|quid|euros?|dollars?|grand|bucks|k)\b)?)"
                         r"(?:\s*(?:or so|ish|please|i think|i reckon))?\W*$", re.I)
CEILING_BUDGET = re.compile(r"^\W*" + BARE_BUDGET_LEAD +
                            r"(?:nothing|not|nowt|no)\s+(?:more than|over|above|past)\s*"
                            r"([£$€]\s?\d[\d,.]*|"
                            r"\d[\d,.]*\s?(?:pounds?|quid|euros?|dollars?|bucks|k)\b)"
                            r"(?:\s*(?:or so|ish|please|i think|i reckon))?\W*$", re.I)
BUDGET_THOUGHT = re.compile(r"^\W*(?:i\s+was\s+|i'?m\s+|im\s+|i\s+am\s+)?thinking\s+"
                            r"(?:about\s+)?(?:around\s+)?"
                            r"(?P<figure>[\u00a3$\u20ac]?\s?\d[\d,.]*\s?(?:pounds?|quid|"
                            r"euros?|dollars?))", re.I)
BUDGET_ASKED = re.compile(r"^\W*(?:is|would|will|does|do|could|can|should)\s+"
                          r"(?P<figure>[\u00a3$\u20ac]?\s?\d[\d,.]*(?:\s?(?:pounds?|quid|euros?|"
                          r"dollars?))?)"
                          r"\s+(?:enough|do|be enough|get|buy|cover|work|be ok|be okay|be fine)\b", re.I)


def vague_budget(text):
    match = VAGUE_BUDGET.match(text or "")
    if not match:
        return None
    said = " ".join(match.group(0).lower().split()).strip(" .,;:!")
    if "cheap" in said and said.startswith("on "):
        return "on the cheap"
    if "cheap" in said or "reasonable" in said:
        return "cheap"
    if said.startswith("budget"):
        return said
    return "not too expensive"


VAGUE_BUDGET = re.compile(
    r"^\W*(?:(?:not|nothing|no|never)\s+(?:\w+\s+){0,2}(?:too\s+|that\s+|very\s+)?"
    r"(?:expensive|pricey|dear)|(?:something|anything|nothing)\s+(?:cheap|cheaper|reasonable)|"
    r"on\s+the\s+cheap|budget\s+(?:friendly|ish))\W*$", re.I)
MONEY = re.compile(r"([£$€]\s?\d[\d,.]*|\b\d[\d,.]*\s?(?:pounds|quid|euros?|dollars?|grand|bucks)\b)", re.I)
AGE_UNIT = (r"(?:foot|feet|ft|cm|centimetres?|centimeters?|inches?|inch|stone|st|kg|kilos?|kgs?|"
            r"pounds?|lbs?|lb|metres?|meters?|m|miles?|mph|hours?|hrs?|mins?|minutes?|weeks?|"
            r"days?|months?|percent|%)")
AGE = re.compile(r"\bi(?:m|'m| am)\s+(\d{1,2})(?![\d.,]\d)\b(?!\s*" + AGE_UNIT + r"\b)"
                 r"(?!\s*\d)", re.I)
HEIGHT_FEET = re.compile(r"\b(?:i'm|i\s+am|im|my\s+height\s+is)\s+(?P<feet>\d)\s*"
                         r"(?:foot|feet|ft|')\s*(?P<inches>\d{1,2}|ten|eleven|one|two|three|"
                         r"four|five|six|seven|eight|nine)?\s*(?:\"|''|in(?:ches)?)?"
                         r"(?=\W|$)", re.I)
HEIGHT_BARE = re.compile(r"^\s*(?:(?:no|nope|sorry|wait|ah|oh|actually|make\s+it)[,.!]?\s+)*"
                         r"(?P<feet>\d)\s*(?:foot|feet|ft)\s*(?P<inches>\d{1,2})\s*\W*$", re.I)
INCH_WORDS = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6",
              "seven": "7", "eight": "8", "nine": "9", "ten": "10", "eleven": "11"}
HEIGHT_CM = re.compile(r"\b(?:i'm|i\s+am|im|my\s+height\s+is)\s+(?P<cm>1\d{2}|2[0-2]\d)\s*"
                       r"(?:cm|centimetres?|centimeters?)\b", re.I)


_NUMBER_IN_WORDS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
    "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
    "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
    "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70,
    "eighty": 80, "ninety": 90,
}
_A_UNIT_WORD = r"(?:one|two|three|four|five|six|seven|eight|nine)"
_A_TEEN_WORD = (r"(?:ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen"
                r"|nineteen)")
_A_TEN_WORD = r"(?:twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety)"
AGE_IN_WORDS = re.compile(r"\b(?P<words>" + _A_TEN_WORD + r"(?:[-\s]" + _A_UNIT_WORD + r")?|"
                          + _A_TEEN_WORD + r"|" + _A_UNIT_WORD + r")\b", re.I)
BEFORE_A_FIGURE = re.compile(r"(?:\b(?:is|are|was|were|aged)\s+|\bi\s+am\s+|\bim\s+|\bi'm\s+"
                            r"|\bam\s+|\b(?:he|she|they|it)(?:'s|s|'re|re)\s+)$", re.I)
AFTER_A_FIGURE = re.compile(r"\s*(?:years?\b(?:\s+old\b)?|yrs?\b(?:\s+old\b)?|yo\b)?\s*"
                            r"(?:[,.!?;:]|$|\band\b|\bbut\b|\bso\b)", re.I)
NOT_YEARS_AFTER = re.compile(r"\s*(?:weeks?|months?|days?|hours?|o.clock)\b", re.I)


def _the_numbers_in_words(text):
    if not text or not any(word in text.lower() for word in _NUMBER_IN_WORDS):
        return text

    def figure(match):
        if not BEFORE_A_FIGURE.search(text[:match.start()]):
            return match.group(0)
        after = text[match.end():]
        if NOT_YEARS_AFTER.match(after) or not AFTER_A_FIGURE.match(after):
            return match.group(0)
        total = sum(_NUMBER_IN_WORDS.get(part, 0)
                    for part in re.split(r"[-\s]+", match.group("words").lower()))
        return str(total) if total else match.group(0)

    return AGE_IN_WORDS.sub(figure, text)


def _how_tall(text):
    match = HEIGHT_CM.search(text)
    if match:
        return match.group("cm") + "cm"
    match = HEIGHT_FEET.search(text) or HEIGHT_BARE.match(text)
    if not match:
        return ""
    inches = INCH_WORDS.get((match.group("inches") or "").lower(), match.group("inches") or "")
    if inches and not inches.isdigit():
        return ""
    if inches and int(inches) >= 12:
        return ""
    return match.group("feet") + " foot" + (" " + str(int(inches)) if inches else "")
MONTHS = frozenset("""january february march april may june july august september october november
december jan feb mar apr jun jul aug sep sept oct nov dec""".split())
BIRTHDAY = re.compile(
    r"\bmy\s+(?:birthday|bday|dob|date of birth)\s*(?:'s|s)?\s*"
    r"(?:is|was|falls|:|=|on|in)\s+(?:on\s+)?(?:the\s+)?"
    r"([^,.;!?]{2,28})", re.I)
BIRTHDAY_PRONOUN = {"his": "he", "her": "she", "their": "they"}


A_DATE_CLAUSE_ENDS = re.compile(r"\s+(?:and|but|so)\s+(?=(?:my|our|his|her|their)\b)", re.I)


def _the_date_clause(date):
    return A_DATE_CLAUSE_ENDS.split(str(date or ""))[0]


def _a_birthday_date(after):
    date = _the_date_clause(" ".join(str(after or "").lower().split())).strip()
    date = date.rstrip(" .,;:")
    date = re.sub(r"^(?:in|on)\s+", "", date)
    looks_like_a_date = any(word in MONTHS for word in re.split(r"[^a-z0-9]+", date)) \
        or re.search(r"\d", date)
    if not date or not looks_like_a_date:
        return ""
    if re.search(r"\b(?:to be|going|quiet|coming|soon|weekend|week|tomorrow|today)\b", date):
        return ""
    return date

WEIGH_UNITS = {"kilo": "kilos", "kilos": "kilos", "kilogram": "kilos", "kilograms": "kilos",
               "kg": "kilos", "kgs": "kilos", "stone": "stone", "st": "stone",
               "pound": "pounds", "pounds": "pounds", "lb": "pounds", "lbs": "pounds"}


def _weight_unit(word):
    word = str(word or "").lower()
    unit = WEIGH_UNITS.get(word)
    if unit is None and word.endswith("s"):
        unit = WEIGH_UNITS.get(word[:-1])
    return unit
WEIGH = re.compile(r"\bi\s+weigh\s+(\d{2,3}(?:\.\d)?)\s*([a-z]+)\b", re.I)
WEIGH_IM = re.compile(r"\bi(?:m|'m| am)\s+(\d{2,3}(?:\.\d)?)\s*([a-z]+)\b", re.I)
WEIGH_MY = re.compile(r"\bmy\s+weights?\s+(?:(?:is|are|works out at)\s+)?"
                      r"(\d{2,3}(?:\.\d)?)\s*([a-z]+)\b", re.I)

COMPOUND_AFTER = frozenset("""evening wedding birthday party house home flat garden car room
meeting funeral anniversary holiday dinner tea lunch day night weekend bedtime visit health
money phone number address school work dog cat baby pram bath""".split())
COMPOUND_THAT_IS_THEIRS = COMPOUND_AFTER - {"evening"}

MY_AGE = re.compile(r"\bmy ages?(?:'s|\s+is|\s+just)?\s+(\d{1,2})\b"
                    r"(?!\s*(?:" + AGE_UNIT + r")\b)(?!\s*\d)", re.I)
_STEP_OF = ("mum", "mom", "mother", "dad", "father", "son", "daughter", "brother", "sister")
_GRAND_OF = ("mum", "mom", "mother", "dad", "father", "son", "daughter", "child")
_BUILT_KIN = tuple(["step" + word for word in _STEP_OF]
                   + ["grand" + word for word in _GRAND_OF])
RELATIONS = ("daughter", "son", "twins", "partner", "husband", "wife", "mum", "mom", "mother",
             "dad", "father", "sister", "brother", "parents", "gran", "grandma", "grandad",
             "granny",
             "nana", "nan", "nanna", "grandmother", "grandfather", "grandpa", "aunt", "auntie",
             "aunty", "uncle", "niece",
             "nephew", "cousin", "friend", "neighbour", "neighbor", "boyfriend", "girlfriend",
             "fiance", "fiancee") + _BUILT_KIN + (
    "gran", "granddad", "stepchild")

SPOKEN_RELATION = {said: full for said, full in lexicon.CHAT.items()
                   if full in RELATIONS or (full.endswith("s")
                                            and full[:-1] in RELATIONS)}
SPOKEN_RELATION = {said: (full[:-1] if full.endswith("s") and full[:-1] in RELATIONS else full)
                   for said, full in SPOKEN_RELATION.items()}
RELATIONS = RELATIONS + tuple(word for word in SPOKEN_RELATION if word not in RELATIONS)

PEOPLE_WORD = re.compile(r"\b(?:" + "|".join(sorted(RELATIONS, key=len, reverse=True)) + r")s?\b"
                         r"|\b(?P<name>(?:my|his|her|their|our)\s+[a-z]{3,}\b)", re.I)

NOT_A_UNIT = (r"(?![\d.,]\d)(?!\d)"
              r"(?!\s*(?:foot|feet|ft|cm|centimet|inches?|inch|stone|st|kg|kilo|lbs?|lb|metres?"
              r"|meters?|miles?|mph|hours?|hrs?|mins?|minutes?|weeks?|percent|%))")
ROLE_PEOPLE = ("tutor", "childminder", "carer", "hairdresser", "barber", "instructor")
KIN = RELATIONS + (
    "nan", "gran", "granddad", "grandmother", "grandfather", "auntie", "niece", "nephew",
    "colleague", "boss", "flatmate", "housemate", "godson", "goddaughter", "manager",
    "landlord", "landlady", "lodger",
    "mate") + ROLE_PEOPLE + (
    "girl", "boy",
    "baby", "little one", "wee one")
ALONE_PERSON = ("youngest", "eldest", "oldest", "baby", "toddler", "newborn", "little one")
PERSON_MODIFIER = ("little", "big", "small", "tiny", "eldest", "oldest", "youngest", "baby",
                   "middle", "older", "younger", "teenage", "grown", "first", "second", "third",
                   "fourth", "other", "poor", "darling", "littlest", "new")
MODIFIER_BEFORE = r"(?:(?:" + "|".join(PERSON_MODIFIER) + r")\s+)?"
IN_LAW = r"(?:[ \t]*-?[ \t]*in[ \t]*-?[ \t]*laws?)?"
IN_LAW_WORD = re.compile(r"^[a-z]+(?:[ \t]*-?[ \t]*in[ \t]*-?[ \t]*laws?)$", re.I)


def an_in_law(word):
    return bool(IN_LAW_WORD.match(str(word or "").strip()))


IN_LAW_AFTER = re.compile(r"[ \t]*-?[ \t]*in[ \t]*-?[ \t]*laws?\b", re.I)
KIN_WORDS = tuple(sorted(set(KIN), key=len, reverse=True))
_RELATION_WORDS = "(?:" + "|".join(KIN_WORDS) + ")" + IN_LAW
_A_PERSON = "(?:" + _RELATION_WORDS + "|" + "|".join(ALONE_PERSON) + ")"
_A_WORD_FOR_A_PERSON = frozenset(KIN) | frozenset(ALONE_PERSON) | frozenset(PERSON_MODIFIER)
TITLE = r"(?:professor|miss|mrs|mr|ms|dr|sir|prof|dame|lord|lady|rev|capt|sgt)\.?"
TITLE_WORDS = frozenset(re.findall(r"[a-z]+", TITLE))
TITLE_GENDER = {"mr": "he", "sir": "he", "lord": "he", "mrs": "she", "ms": "she", "miss": "she",
                "lady": "she", "dame": "she"}
_NAME = (r"(?P<name>" + TITLE + r"(?:\s+[A-Za-z][A-Za-z'\-]{1,19})?"
         r"|[A-Za-z][A-Za-z'\-]{1,19})")
RELATION_NAME = re.compile(
    r"\b(?:my|our)\s+" + MODIFIER_BEFORE + r"(?P<who>" + _A_PERSON + r")(?:\s+is\s+|'s\s+|s\s+)"
    r"(?:called|named)\s+" + _NAME, re.I)
RELATION_HAVE_NAME = re.compile(
    r"\b(?:i|we)\s*(?:'ve|ve|have|got)(?:\s+got)?\s+"
    r"(?:an?\s+|one\s+|two\s+|three\s+)?"
    r"(?P<who>" + _RELATION_WORDS + r")s?\s+(?:called|named)\s+" + _NAME, re.I)
RELATION_POSSESSIVE_NAME = re.compile(
    r"\b(?:my|our)\s+" + MODIFIER_BEFORE + r"(?P<who>" + _A_PERSON + r")(?:'s|s)?\s+name\s+(?:is\s+)?"
    + _NAME, re.I)
_NOT_A_PERSON_NAME = r"(?!(?:" + "|".join(sorted(_A_WORD_FOR_A_PERSON, key=len, reverse=True)) + r")\b)"
RELATION_NAMED_AGE = re.compile(
    r"\b(?:my|our)\s+" + MODIFIER_BEFORE + r"(?P<who>" + _A_PERSON + r")\s+"
    r"(?P<name>" + _NOT_A_PERSON_NAME + r"[A-Za-z][A-Za-z'-]{1,19})"
    r"\s+(?:is|'s|was)\s+(?P<age>\d{1,3})" + NOT_A_UNIT, re.I)
RELATION_POSSESSIVE_AGE = re.compile(
    r"\b(?:my|our)\s+" + MODIFIER_BEFORE + r"(?P<who>" + _A_PERSON + r")s?'?s?\s+ages?\s+"
    r"(?:is|was|'s)\s+(?P<age>\d{1,3})" + NOT_A_UNIT, re.I)
RELATION_AGE = re.compile(
    r"\b(?:my|our)\s+" + MODIFIER_BEFORE + r"(?P<who>" + _A_PERSON + r")(?:\s+is\s+|'s\s+|s\s+|\s+)?"
    r"(?:turning\s+|turns\s+)?(?P<age>\d{1,3})" + NOT_A_UNIT, re.I)
THE_PLACE_AGE = re.compile(
    r"\bthe\s+(?P<who>" + "|".join(sorted(ALONE_PERSON, key=len, reverse=True)) + r")"
    r"(?:\s+is\s+|'s\s+|s\s+)(?P<age>\d{1,3})" + NOT_A_UNIT, re.I)
BABY_AGE = re.compile(
    r"\b(?:my|our|the)\s+(?:(?P<who>baby)|(?P<little>little\s+one|wee\s+one)|newborn|tot)"
    r"\s+(?:is|'s|was|are)\s+"
    r"(?P<age>\d{1,3})(?![\d.,]\d)(?!\d)\s*(?P<unit>months?|years?)\b"
    r"(?!\s*(?:away|ago|later|early|behind|off))", re.I)
MONTH_OLD_BABY = re.compile(
    r"\b(?:my|our|the)\s+(?P<age>\d{1,2})(?![\d.,]\d)(?!\d)\s*(?:months?)\s+old\b"
    r"(?!\s*(?:away|ago|later|early|behind|off))"
    r"(?=\s*(?:[,.;!?]|$|\s+(?:is|was|are|were|has|have|had|keeps|needs|wakes|sleeps|who|that|and|"
    r"but|eats|walks|loves|will|can|does|did|goes|cries|feeds|naps|sits|crawls|started|still|now|"
    r"baby|boy|girl|son|daughter|child|little one|wee one)\b))", re.I)
RELATION_BARE_NAME = re.compile(
    r"\b(?:my|our)\s+" + MODIFIER_BEFORE + r"(?P<who>" + _A_PERSON + r")(?:\s+is\s+|'s\s+|s\s+)"
    r"(?P<name>[A-Za-z][A-Za-z'-]{1,19})\b", re.I)
RELATION_PAIR_NAMES = re.compile(
    r"\b(?:my|our)\s+(?P<who1>" + _RELATION_WORDS + r")\s+and\s+(?P<who2>" + _RELATION_WORDS
    + r")\s+(?:are|were)\s+(?P<name1>[A-Za-z][A-Za-z'-]{1,19})\s+and\s+"
    r"(?P<name2>[A-Za-z][A-Za-z'-]{1,19})\b", re.I)
GROUP_NAMED_NAMES = re.compile(
    r"\b(?:my|our)\s+(?P<who>" + _RELATION_WORDS + r"|kids?|children)"
    r"(?:\s+and\s+(?P<who2>" + _RELATION_WORDS + r"))?\s+(?:are|were)\s+(?:called|named)\s+"
    r"(?P<rest>[A-Za-z][A-Za-z'-]{1,19}(?:\s*(?:,|and)\s*[A-Za-z][A-Za-z'-]{1,19}){1,3})\b",
    re.I)
GROUP_NAMED_AGES = re.compile(
    r"\b(?:my|our)\s+" + MODIFIER_BEFORE + r"(?P<who>" + _A_PERSON + r"|kids?|children|child)\s+(?:are|were)\s+"
    r"(?P<rest>[a-z][a-z'-]{1,19}\s+\d{1,3}(?:\s*(?:,|and)\s*[a-z][a-z'-]{1,19}\s+\d{1,3}){1,3})",
    re.I)
RELATION_WHOS_AGE = re.compile(
    r"\b(?:my|our)\s+(?P<who>" + _RELATION_WORDS + r")\s*,?\s+who(?:['\u2019]?s)?\s+"
    r"(?:is\s+)?(?P<age>\d{1,3})\b" + NOT_A_UNIT, re.I)
CHAINED_RELATION_AGE = re.compile(
    r"\b(?:my|our)\s+" + MODIFIER_BEFORE + r"(?P<first>" + _A_PERSON + r")"
    r"(?:'s|\u2019s|s)\s+(?P<second>" + _A_PERSON + r")"
    r"(?:\s+(?P<name>(?!(?:is|was|'s)\b)[A-Za-z][A-Za-z'-]{1,19}))?"
    r"\s*(?:'s|\u2019s|is|was)\s+(?P<age>\d{1,3})" + NOT_A_UNIT, re.I)


CHAINED_PERSON = re.compile(
    r"\b(?:my|our)\s+" + MODIFIER_BEFORE + r"(?P<first>" + _A_PERSON + r")"
    r"(?:'s|\u2019s|s)\s+(?P<second>" + _A_PERSON + r")\b", re.I)


def a_chained_person(text):
    found = CHAINED_PERSON.search(str(text or ""))
    if not found:
        return ""
    first = re.sub(r"(?:'s|\u2019s|s)$", "", found.group("first").lower())
    return first + "'s " + found.group("second").lower()


AGE_TO_COME_TAIL = (r"(?!\s+(?:next\s+(?:week|month|year|spring|summer|autumn|winter)|"
                    r"(?:in|on)\s+[a-z]{3,9})\b)")
HOW_THEY_FEEL = re.compile(r"\b(?:hate|hates|hated|hating|love|loves|loved|likes?|liked"
                           r"|wants?|wanted|prefers?|dreads?|shy|embarrassed|nervous"
                           r"|excited|proud|rather)\b", re.I)

_AN_AGE_IN_WORDS = ("(?:" + _A_TEN_WORD + r"(?:[-\s]" + _A_UNIT_WORD + r")?|"
                    + _A_TEEN_WORD + "|" + _A_UNIT_WORD + ")")
PRONOUN_AGE = re.compile(r"\b(?P<who>she|he|they)(?:'s|s|re|'re)?(?:\s+(?:is|are))?"
                         r"(?:\s+(?:about|around|nearly|almost|roughly|maybe|probably|just|only"
                         r"|now|already|still))*\s+"
                         r"(?P<come>turning\s+|turns\s+|will\s+be\s+|is\s+going\s+to\s+be\s+)?"
                         r"(?P<age>\d{1,3}|" + _AN_AGE_IN_WORDS + r")" + NOT_A_UNIT
                         + AGE_TO_COME_TAIL, re.I)


def a_stated_number(word):
    said = str(word or "").strip().lower()
    if not said:
        return None
    if said.isdigit():
        return int(said)
    total = sum(_NUMBER_IN_WORDS.get(part, 0) for part in re.split(r"[-\s]+", said))
    return total or None


def a_person_word(word):
    plain = " ".join(re.sub(r"[ \t]*-[ \t]*", " ", str(word or "").strip().lower()).split())
    return re.sub(r"\bin laws$", "in law", plain)
def _the_person(found, who, name=""):
    who = a_person_word(who)
    for one in found:
        if one.get("who") != who:
            continue
        if name and one.get("name") and str(one["name"]).lower() != str(name).lower():
            continue
        return one
    return None


def _relation_facts(text):
    found = []
    text = stated_not_asked(text)
    if not text:
        return found

    def entry(who, name=""):
        who = a_person_word(who)
        for known in found:
            if known.get("who") != who:
                continue
            if name and known.get("name") and str(known["name"]).lower() != str(name).lower():
                continue
            return known
        made = {"who": who}
        found.append(made)
        return made

    for match in RELATION_POSSESSIVE_AGE.finditer(text):
        entry(match.group("who").lower())["age"] = int(match.group("age"))
    for pattern in (RELATION_NAME, RELATION_POSSESSIVE_NAME, RELATION_NAMED_AGE,
                    RELATION_HAVE_NAME):
        for match in pattern.finditer(text):
            name = _finish(match.group("name"))
            if not name or _not_a_name(match.group("name"), strict_ly=False):
                continue
            if not _name_after_a_title(match.group("name")):
                continue
            if str(match.group("name")).lower() in _A_WORD_FOR_A_PERSON:
                continue
            entry(match.group("who").lower(), _tidy(name)).setdefault(
                "name", _tidy_a_titled_name(name))
    for match in RELATION_BARE_NAME.finditer(text):
        name = _bare_name(match.group("name"))
        if name:
            entry(match.group("who").lower(), name).setdefault("name", name)
    for match in RELATION_PAIR_NAMES.finditer(text):
        names = [_bare_name(match.group("name1"), pair=True),
                 _bare_name(match.group("name2"), pair=True)]
        if all(names):
            who1 = match.group("who1").lower()
            who2 = match.group("who2").lower()
            found.append({"who": who1 + " and " + who2, "names": names})
    for match in GROUP_NAMED_NAMES.finditer(text):
        said = [word for word in re.split(r"\s*(?:,|and)\s*", match.group("rest")) if word]
        names = [_bare_name(word, pair=True) for word in said]
        if len(names) < 2 or not all(names):
            continue
        who = match.group("who").lower()
        if match.group("who2"):
            who = who + " and " + match.group("who2").lower()
        found.append({"who": who, "names": names})
    for match in GROUP_NAMED_AGES.finditer(text):
        pair = re.findall(r"([A-Za-z][A-Za-z'-]{1,19})\s+(\d{1,3})", match.group("rest"))
        if len(pair) < 2:
            continue
        named = [(said, _bare_name(said, pair=True), age) for said, age in pair]
        if not all(name for _, name, _ in named):
            continue
        for who, name, age in named:
            made = {"who": match.group("who").lower(), "name": name, "age": int(age)}
            if made not in found:
                found.append(made)
    for match in BABY_AGE.finditer(text):
        made = entry(str(match.group("who") or match.group("little") or "baby").lower())
        if str(match.group("unit")).lower().startswith("month"):
            made.setdefault("months", int(match.group("age")))
        else:
            made.setdefault("age", int(match.group("age")))
    for match in MONTH_OLD_BABY.finditer(text):
        entry("baby").setdefault("months", int(match.group("age")))
    for pattern in (RELATION_AGE, THE_PLACE_AGE, RELATION_NAMED_AGE, RELATION_WHOS_AGE):
        clause = pattern is RELATION_WHOS_AGE
        for match in pattern.finditer(text):
            rest = text[match.end():]
            months = _month_age_after(text, match.end())
            if months:
                entry(match.group("who").lower()).setdefault("months", int(match.group("age")))
                continue
            if not (clause or AGE_TAIL.match(rest)):
                continue
            named = match.groupdict().get("name")
            known = (entry(match.group("who").lower(), _tidy(named)) if named
                     else entry(match.group("who").lower()))
            known.setdefault("age", int(match.group("age")))
    for tasted in taste.read_other(text):
        thing = tasted.get("thing")
        if not thing:
            continue
        key = "likes" if tasted.get("how") == "yes" else "dislikes"
        if tasted.get("eaten") and set(str(thing).split()) & DIET_GROUP:
            continue
        who = tasted.get("who")
        if who:
            known = entry(who)
        else:
            known = next((made for made in found
                          if made.get("pronoun") == tasted.get("pronoun")
                          and not made.get("who")), None)
            if known is None:
                known = {"pronoun": tasted.get("pronoun") or ""}
                found.append(known)
        held = known.setdefault(key, [])
        if thing not in held:
            held.append(thing)
    for match in OTHER_BIRTHDAY.finditer(text):
        date = _a_birthday_date(match.group("date"))
        if not date:
            continue
        said_who = (match.groupdict().get("who") or "").lower()
        said_pronoun = (match.groupdict().get("pronoun") or "").lower()
        if said_who:
            known = entry(said_who)
        else:
            pronoun_word = BIRTHDAY_PRONOUN.get(said_pronoun, said_pronoun)
            person = _the_person_the_pronoun_is(text, match.end(), pronoun_word)
            if person:
                known = entry(person)
            else:
                known = next((made for made in found
                              if made.get("pronoun") == pronoun_word and not made.get("who")), None)
                if known is None:
                    known = {"pronoun": pronoun_word}
                    found.append(known)
        known.setdefault("birthday", date)
    pronoun = PRONOUN_AGE.search(text)
    if pronoun and a_stated_number(pronoun.group("age")) is None:
        pronoun = None
    if pronoun and pronoun.group("come"):
        same_breath = re.split(r"[.!?]", text[pronoun.end():], 1)[0]
        if HOW_THEY_FEEL.search(same_breath):
            pronoun = None
    if pronoun and _month_age_after(text, pronoun.end()):
        fits = SHE if pronoun.group("who").lower() == "she" else HE
        for known in found:
            if "age" not in known and "months" not in known and known.get("who") in fits:
                known["months"] = a_stated_number(pronoun.group("age"))
                break
        else:
            if not any("months" in made for made in found):
                found.append({"months": a_stated_number(pronoun.group("age")),
                              "pronoun": pronoun.group("who").lower()})
    elif pronoun and AGE_TAIL.match(text[pronoun.end():]):
        word = pronoun.group("who").lower()
        fits = SHE if word == "she" else HE if word == "he" else frozenset()
        for known in found:
            if "age" not in known and known.get("who") in fits:
                known["age"] = a_stated_number(pronoun.group("age"))
                break
        if not any("age" in made for made in found):
            word = pronoun.group("who").lower()
            person = _the_person_the_pronoun_is(text, pronoun.start(), word)
            if person:
                found.append({"who": person, "age": a_stated_number(pronoun.group("age"))})
            else:
                found.append({"age": a_stated_number(pronoun.group("age")), "pronoun": word})
    return [known for known in found if len(known) > 1 or "who" not in known]

_SHE_SAID = frozenset("""mum mom mother daughter sister wife grandma granny nana nan grandmother aunt
niece girlfriend fiancee partner friend neighbour neighbor colleague girl boss manager landlord
landlady cousin flatmate housemate roommate lodger mate""".split())
_HE_SAID = frozenset("""dad father son brother husband grandpa grandad grandfather uncle nephew
boyfriend fiance partner friend neighbour neighbor colleague boy boss manager landlord landlady
cousin flatmate housemate roommate lodger mate""".split())


def _kin_pronoun(word):
    for prefix in ("step", "grand"):
        if word.startswith(prefix) and word[len(prefix):] in _SHE_SAID | _HE_SAID:
            return word[len(prefix):]
    return word


SHE = (_SHE_SAID | frozenset(word for word in _BUILT_KIN if _kin_pronoun(word) in _SHE_SAID)
       | frozenset(("gran", "sister in law", "mother in law", "daughter in law",
                    "sister in laws", "mother in laws")))
HE = (_HE_SAID | frozenset(word for word in _BUILT_KIN if _kin_pronoun(word) in _HE_SAID)
      | frozenset(("brother in law", "father in law", "son in law",
                   "brother in laws", "father in laws")))


def _sided(word):
    inside = _kin_pronoun(word)
    for gendered in sorted(_SHE_SAID | _HE_SAID, key=len, reverse=True):
        if inside.startswith(gendered) or inside.endswith(gendered):
            return "she" if gendered in _SHE_SAID else "he"
    return ""


_UNPOINTED = frozenset(word for word in KIN if word not in SHE and word not in HE)
SHE = SHE | frozenset(word for word in _UNPOINTED if _sided(word) == "she")
HE = HE | frozenset(word for word in _UNPOINTED if _sided(word) == "he")

A_LIMIT = re.compile(
    r"\b(?:nothing|no|not|never|nowt)\s+(?:too\s+|very\s+|much\s+|any\s+)?"
    r"(?P<move>tiring|strenuous|energetic|demanding|exhausting|exhaustive|walking|walk|walks|"
    r"long walks?|hikes?|hiking|hills?|stairs?|standing|climbing|lifting)\b"
    r"|\b(?:can'?t|cannot|can not|isn'?t able to|is not able to|not able to|only manage)\s+"
    r"(?:walk|climb|manage)\s+(?:far|long|much)\b"
    r"|\b(?:can'?t|cannot|can not|isn'?t able to|is not able to|not able to|only manage)\s+"
    r"(do|manage|get\s+up|get\s+up\s+and\s+down|get\s+up\s+the|use|cope\s+with)\s+"
    r"(?:the\s+|a\s+|any\s+)?(?:more\s+)?(?:stairs?|steps?|hills?|walks?|walking|"
    r"climbing|standing)\b"
    r"|\b(?:can'?t|cannot|can not|isn'?t able to|is not able to|not able to|only manage)\s+"
    r"(?:stand|sit)\s+(?:for\s+)?(?:long|far)\b"
    r"|\b(?:keep (?:it|the cost|costs) (?:cheap|low|small)|on a (?:tight )?budget)\b"
    r"|\b(?:nothing|no|not)\s+(?:too\s+)?(?:expensive|pricey|fancy)\b", re.I)
COMMITS_TO = re.compile(
    r"\b(?:going to|planning to|off to|about to|booking|booked|saving up|i(?:'?ve| have) booked)\b",
    re.I)
MONEY_LIMIT = re.compile(r"\b(?:cheap|budget|expensive|pricey|fancy|cost|costs|money|low)\b", re.I)


def _own_body_is_the_trouble(clean):
    try:
        from ..compose.badnews import reads_like_a_symptom
    except Exception:
        return False
    try:
        return bool(reads_like_a_symptom(clean))
    except Exception:
        return False


def a_limit_on_the_plan(text):
    if not isinstance(text, str):
        return None
    clean = " ".join(text.lower().split())
    if not clean or "?" in clean:
        return None
    match = A_LIMIT.search(clean)
    if match is None:
        return None
    if _own_body_is_the_trouble(clean):
        return None
    hit = match.group(0)
    if match.group("move") or re.search(
            r"\b(?:walk|stand|sit|climb|climbing|manage|stairs?|steps?|hills?|walking|standing)\b",
            hit):
        return "move"
    return "money" if MONEY_LIMIT.search(hit) else "other"


PLAN = re.compile(r"\b(?:(?:i(?:'m| am)|we(?:'re| are)|im|were)\s+(?:going to|planning|thinking of|off to|"
                  r"about to|hoping to|trying to|aiming to|aim to|meaning to|learning to|"
                  r"working on|writing|training|moving|"
                  r"buying|looking for|starting|organising|organizing|preparing|building|making|"
                  r"booking|saving|decorating|redecorating|painting|renovating|tiling|plastering|"
                  r"sorting|packing|cleaning|planting|digging|sewing|knitting|baking|cooking)(?: up| out| around| through)?|"
                  r"i want to|i need to|we want to|"
                  r"we need to|i(?:'?ve| have) got|i(?:'?ve| have) just got)\b", re.I)
PARTICLES = frozenset("""up out around through off""".split())
INFINITIVE_FRAME = re.compile(r"\b(?:trying|aiming|hoping|planning|meaning|learning|want|need)"
                              r"\s+to\s*$", re.I)
PERSON_OPEN = re.compile(r"^(?:i(?:'m| am)|we(?:'re| are)|im|were|i want to|i need to|we want to|"
                         r"we need to|i(?:'ve| have) got|i(?:'ve| have) just got)\s+", re.I)
PREPOSITIONS = frozenset("for to in on at with about into by from".split())
POINTING = frozenset("""it them that this these those one ones nobody nothing anything
something everything anyone someone none""".split())
ARTICLES = frozenset("""a an the my our your his her their""".split())
_FAREWELL = re.compile(r"\b(?:speak|talk|chat|text|see you|see ya|catch you|bye|goodbye|later|ttyl|"
                       r"gtg|cya|night)\b", re.I)
_GOT_A = re.compile(r"\b(?:i'?ve|ive|i have)\s+got\b(?!\s+to\b)", re.I)
_GOT_TO = re.compile(r"\b(?:i'?ve|ive|i have)\s+got\s+to\b", re.I)
MONTH_NAMES = (r"(?:january|february|march|april|may|june|july|august|september|october|november|"
               r"december)")
DAY_AND_MONTH = ("(?:" + r"\d{1,2}(?:st|nd|rd|th)?\s+(?:of\s+)?" + MONTH_NAMES +
                 r"|(?:the\s+)?\d{1,2}(?:st|nd|rd|th)\s+of\s+" + MONTH_NAMES +
                 r"|" + MONTH_NAMES + r"\s+\d{1,2}(?:st|nd|rd|th)?" + ")")
FUTURE = re.compile(
    r"\b(?:tomorrow|tonight|this (?:weekend|week|evening|morning|afternoon|month|year|"
    r"monday|tuesday|wednesday|thursday|friday|saturday|sunday)|next (?:week|weekend|month|year|"
    r"summer|winter|spring|autumn|monday|tuesday|wednesday|thursday|friday|saturday|sunday|"
    r"january|february|march|april|may|june|july|august|september|october|november|december)|"
    r"(?:(?:on|by|before|until) (?:the )?(?:monday|tuesday|wednesday|thursday|friday|saturday|"
    r"sunday|\d{1,2}(?:st|nd|rd|th))|"
    r"(?:is|are) (?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)|"
    r"(?:is|are) (?:on |in )?the \d{1,2}(?:st|nd|rd|th))|"
    r"(?:on|by|before|until) (?:the )?" + DAY_AND_MONTH + r"|"
    r"(?:is|are) (?:on )?" + DAY_AND_MONTH + r"|"
    r"(?:starts?|starting|begins?|beginning|ends?|ending|finishes|finishing|opens?|closes?|due|"
    r"scheduled|booked) (?:on )?" + DAY_AND_MONTH + r"|"
    r"in (?:january|february|march|april|may|june|july|august|september|october|november|december|"
    r"the (?:summer|winter|spring|autumn|morning|afternoon|evening))|"
    r"(?:the )?(?:week|month|summer) after|at the end of the (?:week|month|year)|"
    r"later (?:this|next) (?:week|month|year)|in (?:a|\d+|a few|two|three) (?:days?|weeks?|months?))\b",
    re.I)
PAST = re.compile(r"\b(?:was|were|went|had|did|didnt|didn't|last|yesterday|ago|already|used to|back in|"
                  r"just|never|kept|used)\b", re.I)
PAST_VERBS = frozenset("""saw met took made got went came said told gave found thought felt knew
left ran sat stood spent paid sent held won lost ate drank drove flew slept read wrote spoke broke
chose forgot began rang phoned watched visited played finished started cleaned painted fixed
argued fought moved booked texted emailed ordered carried""".split())
PAST_ARRANGED = frozenset("""agreed promised arranged booked planned sorted organised organized
reserved scheduled offered""".split())
PAST_STATES = frozenset("""tired bored excited worried wrecked shattered interested pleased scared
annoyed confused stressed exhausted married engaged retired aged blessed wicked naked sacred
beloved rugged hundred""".split())
INTENTION_AFTER = frozenset(("to", "i", "we", "you", "he", "she", "they", "that"))
PAST_DEED = re.compile(r"^(?:ok(?:ay)?[, ]+|and |so |but |also |well |oh )*"
                       r"(?:i|we|he|she|they|(?:my|our)\s+[a-z]+)\s+([a-z']+)(?:\s+([a-z']+))?\b",
                       re.I)


def a_deed(clause):
    match = PAST_DEED.match(clause or "")
    if not match:
        return False
    word = match.group(1).lower()
    if word in PAST_ARRANGED:
        return False
    if word in PAST_VERBS:
        return True
    if word.endswith("ed") and len(word) >= 5 and word not in PAST_STATES:
        return (match.group(2) or "").lower() not in INTENTION_AFTER
    return False


OWN = re.compile(r"^(?:ok(?:ay)?[, ]+|and |so |but |also |well |oh )*"
                 r"(?:i|i'm|im|i've|we|we're|were|we've|weve|my|our|me)\b", re.I)
SECOND_PERSON = re.compile(r"\b(?:you|your|you're|u|ur|yours)\b", re.I)
NEGATED = re.compile(r"\b(?:cant|can't|cannot|dont|don't|doesnt|doesn't|wont|won't|not|never|no)\b", re.I)
DETERMINERS = frozenset("""a an the my our his her their your some any this that these those
one two three""".split())
ASKED_BEFORE = re.compile(r"\b(?:what|when|where|which|remind me|tell me)\b", re.I)
ASKING = re.compile(r"\b(?:what|when|where|which|who|why|how)(?:'s|s|'re|re)?\b|"
                    r"\b(?:should|shall|can|could|would|do|does|did|is|are|was|will|any)\b", re.I)
CORRECTION_WHY = r"\s*,?\s*(?:because|cos|coz|cuz|'cause|since)\b[^.!?]*"
CORRECTION = re.compile(
    r"(?:\b(?:sorry,?\s*)?(?:no,?\s+)?(?:i\s+meant|i\s+mean)"
    r"|^(?:\s*(?:ok|okay|actually|sorry|no|oh)[, ]+)*make\s+that)\s+(?:it'?s\s+|its\s+)?"
    r"([£$\u20ac]?\s?[a-z0-9][a-z0-9 '£$\u20ac-]{0,30}?)"
    r"(?:,?\s+not\s+([a-z0-9][a-z0-9 '-]{0,30}?))?"
    r"(?:\s+instead|[,.]|$|(?=" + CORRECTION_WHY + r"))",
    re.I)
TAKES_BACK_THE_VALUE = r"(?:not|rather\s+than|instead\s+of)"
CORRECTION_PAIR = re.compile(
    r"\b(?:sorry|no|actually|oops)[, ]+"
    r"(?:(?:it'?s|its|it\s+is|that'?s|thats|that\s+is)\s+)?"
    r"(?:(?:i|we|you|they|he|she)\s*(?:'ve|ve|have|had)\s*(?:got\s+|get\s+|now\s+)?)?"
    r"((?:the\s+)?[a-z0-9][a-z0-9'-]{1,20}(?: [a-z0-9][a-z0-9'-]{1,15})?),?\s+"
    + TAKES_BACK_THE_VALUE + r"\s+"
    r"((?:the\s+)?[a-z0-9][a-z0-9'-]{1,20}(?: [a-z0-9][a-z0-9'-]{1,15})?)"
    r"(?:\s+instead\b|\s*[-,.;!?]|$)", re.I)
CORRECTION_MAKE = re.compile(
    r"^\s*(?:(?:no|nope|sorry|actually|oops|ok|okay)[,.]?\s+)?"
    r"(?:make\s+(?:that|it)|change\s+(?:that|it)\s+to|switch\s+(?:that|it)\s+to)\s+"
    r"((?:the\s+)?[a-z0-9][a-z0-9 '£$\u20ac-]{0,25}?)"
    r"(?:,?\s+(?:please|then|instead|actually|now))?\s*[.!?]?\s*$", re.I)
CORRECTION_SAID = re.compile(
    r"\b(?:no|nope|sorry|actually|oops)[,.]?\s+(?:i\s+said|i\s+did\s+say|i\s+actually\s+said|"
    r"i\s+meant\s+to\s+say)\s+(?:it'?s\s+|its\s+)?([a-z0-9][a-z0-9 '-]{0,30}?)"
    r"(?:,?\s+not\s+([a-z][a-z '-]{1,30}?))?(?:\s+instead|[,.]|$)", re.I)
MOVED_VERB = (r"(?:moved|changed|pushed|shifted|switched|bumped|rescheduled|rearranged|"
              r"brought|put|shoved|dragged)")
MOVED_TO = r"\s*(?:back|forward|ahead|earlier|later|round|on)?\s*(?:to|until|till|for)\s+"
CORRECTION_MOVED = re.compile(
    r"(?:"
    r"\b(?:got|had|get|have|has)\s+(?:it|that|this|them|the\s+[a-z]+)\s+" + MOVED_VERB + MOVED_TO +
    r"|"
    r"\b(?:it'?s|its|it\s+is|it\s+was|it\s+has|they'?ve|they\s+have|"
    r"has\s+been|have\s+been|had\s+been|been)\s+" + MOVED_VERB +
    r"(?:\s+(?:it|that|this|them))?" + MOVED_TO +
    r"|"
    r"\b(?:they|he|she|we|i|the\s+[a-z]+)\s+" + MOVED_VERB +
    r"\s+(?:it|that|this|them)" + MOVED_TO +
    r"|\b(?:it'?s|its|it\s+is)\s+now\s+(?:on|for)\s+"
    r")"
    r"((?:the\s+)?[a-z0-9][a-z0-9 ':-]{0,25}?)"
    r"(?:\s+(?:because|cos|cause|coz|due|since|so|as|seeing|what\s+with)\b"
    r"|\s+instead|[,.;!?]|$)", re.I)


CLOCK_SAID = (r"(?:\d{1,2}(?:[:.][0-5]\d)?\s*(?:am|pm|a\.m\.|p\.m\.)"
              r"|(?:[01]?\d|2[0-3]):[0-5]\d"
              r"|\d{1,2}\s*o'?\s*clock"
              r"|noon|midday|midnight)")
CLOCK_VALUE = re.compile(r"^(?:the\s+|at\s+)?(" + CLOCK_SAID + r")$", re.I)
CLOCK_IN_PLAN = re.compile(
    r"(?<![\d.:])(?:" + CLOCK_SAID + r")"
    r"|(?<=\bat )\d{1,2}(?![\d:.,a-z%])", re.I)


def a_clock_time(phrase):
    match = CLOCK_VALUE.match(" ".join(str(phrase or "").split()))
    return match.group(1) if match else ""


def the_clock_in(text):
    return CLOCK_IN_PLAN.search(str(text or ""))


def a_moved_time(phrase):
    words = [word for word in re.split(r"[^a-z0-9]+", str(phrase or "").lower()) if word]
    if not words:
        return False
    if any(word in MONTHS or word in DAYS for word in words):
        return True
    if a_clock_time(phrase):
        return True
    return bool(DATE_VALUE.fullmatch(str(phrase or "").strip())) or bool(
        re.fullmatch(r"(?:the\s+)?\d{1,2}(?:st|nd|rd|th)?", str(phrase or "").strip(), re.I))


def _a_day_taken_back(text):
    return A_DAY_TAKEN_BACK.search(text) or A_DAY_I_MEANT.search(text)


def _a_moved_time(text):
    for moved in CORRECTION_MOVED.finditer(text):
        if a_moved_time(moved.group(1)):
            return moved
    return None


CORRECTION_NUMBER_PAIR = re.compile(
    r"\b(?:sorry|no|actually|oops)[, ]+(\d+(?:\.\d+)?(?:\s+[a-z]+)?)\s+"
    + TAKES_BACK_THE_VALUE + r"\s+"
    r"(\d+(?:\.\d+)?(?:\s+[a-z]+)?)(?:\s+instead|[,.]|$)", re.I)
A_DATE_VALUE = (r"((?:the\s+)?\d{1,2}(?:st|nd|rd|th)?(?:\s+of\s+(?:the\s+)?[a-z]{3,10})?"
                r"|(?:the\s+)?\d{1,2}(?:st|nd|rd|th)?\s+[a-z]{3,10}"
                r"|the\s+[a-z]{3,10}"
                r"|[a-z]{3,10})")
AFTER_THE_VALUE = (r"(?:\s+(?:actually|instead|then|though|sorry|please|i\s+think|"
                   r"i\s+reckon|if\s+thats\s+ok|if\s+that'?s\s+ok))*\s*[.!]?\s*$")
CHANGED_TO = re.compile(
    r"\b(?:we|i|they)(?:\s*'?ve|\s+have|\s+had)?\s+"
    r"(?:moved|changed|pushed|shifted|switched|brought|put|bumped|made)\s+"
    r"(?:it|that|this|the\s+[a-z]{2,15}|our\s+[a-z]{2,15}|my\s+[a-z]{2,15})\s+"
    r"(?:back\s+|forward\s+|on\s+)?(?:to|until|for)\s+"
    + A_DATE_VALUE + AFTER_THE_VALUE, re.I)
CHANGED_BARE = re.compile(
    r"^\s*(?:(?:ok|okay|right|well|so|and|actually|no|sorry|oh)[, ]+)?"
    r"(?:make|change|move|push|put|shift|bring)\s+"
    r"it\s+(?:to\s+)?" + A_DATE_VALUE + AFTER_THE_VALUE, re.I)
CHANGED_NOW = re.compile(
    r"^\s*(?:it'?s|its|that'?s|thats)\s+(?:actually|really)\s+"
    r"(?:(?:on|in|at)\s+)?([a-z]{3,10})(?:\s+now)?\s*[.!?]?\s*$"
    r"|^\s*(?:it'?s|its|that'?s|thats)\s+(?:(?:on|in|at)\s+)?([a-z]{3,10})\s+instead"
    r"(?:\s+now)?\s*[.!?]?\s*$"
    r"|^\s*(?:(?:ok|okay)[,.]?\s+)?"
    r"(?:(?:no|nope|sorry|wait|ah|oh|oops|hold\s+on|hold\s+up|hang\s+on|hmm|um+|erm+|well)"
    r"[,.]?\s+){1,3}"
    r"(?:(?:it'?s|its|that'?s|thats)\s+)?(?:actually\s+|really\s+)?"
    r"(?:(?:on|in|at)\s+)?([a-z]{3,10})(?:\s+now)?\s*[.!?]?\s*$", re.I)


CORRECTION_A_DATE = re.compile(
    r"^\W*(?:(?:ok|okay|right|so|and|no|nope|sorry|actually|oops|wait|oh|hmm)[,.]?\s+)+"
    r"(?:(?:it'?s|its|it\s+is|that'?s|thats|the\s+date\s+is)\s+)?"
    r"(?:(?:now|on|for)\s+)?"
    + A_DATE_VALUE + AFTER_THE_VALUE, re.I)
A_DAY_TAKEN_BACK = re.compile(
    r"^\W*(?:(?:ok|okay|right|so|and|no|nope|sorry|actually|oops|wait|oh|hmm)[,.]?\s+)+"
    r"(?:(?:it'?s|its|it\s+is|make\s+it)\s+)?"
    r"(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b"
    r"(?!\s+(?:is|was|are|were|and|or|but)\b)"
    r"(?:\s+(?:now|instead)\b"
    r"|[,.]?\s*(?:i\s+(?:got|had|put)\s+(?:the|that)\s+day\s+wrong|wrong\s+day|"
    r"my\s+mistake|i\s+was\s+wrong|im\s+wrong|silly\s+me|\s+i\s+meant\b))", re.I)

A_DAY_I_MEANT = re.compile(
    r"^\W*(?:(?:ok|okay|right|so|and|no|nope|sorry|actually|oops|wait|oh|hmm)[,.]?\s+)+"
    r"i\s+(?:meant|mean|said|was\s+thinking)\s+"
    r"(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b"
    r"(?!\s+(?:is|was|are|were)\b)", re.I)

A_TIME_INSTEAD = re.compile(
    r"^\W*(?:it'?s|its|that'?s|thats)\s+"
    + A_DATE_VALUE +
    r"\s+instead\b" + AFTER_THE_VALUE, re.I)
MOVED_BY_ITS_OWN_VERB = re.compile(
    r"\b(?:it|that|this|the\s+[a-z]{2,15}|our\s+[a-z]{2,15}|my\s+[a-z]{2,15})\s+"
    r"(?:(?:has|have|had|got|was|is|been)\s+)?"
    r"(?:starts?|started|slips?|slipped|moves?|moved|pushes?|pushed|changes?|changed|"
    r"shifts?|shifted|lands?|landed|happens?|puts?)\s+"
    r"(?:back\s+|forward\s+|on\s+|to\s+|until\s+|for\s+)?"
    + A_DATE_VALUE +
    r"(?:\s+instead)?\s*[.!]?\s*$", re.I)
TRIP_DATE_MOVED = re.compile(
    r"^\W*(?:(?:ok|okay|right|well|so|and)[,.]?\s+)?"
    r"(?:(?:no|nope|sorry|actually|oops|wait|ah|oh|hmm)[,.]?\s+){1,3}"
    r"(?:(?:we|were|i|im|they|theyre|he|hes|she|shes)\s*(?:'re|'ve|'ll|'m|'s|\s+are|"
    r"\s+have|\s+had|\s+will)?\s+)?"
    r"(?:fly|flies|flying|go|goes|going|leave|leaves|leaving|head|heading|"
    r"travel|travelling|traveling|drive|driving|sail|sailing|arrive|arriving)\b"
    r"[^.!?]{0,40}?"
    r"\b(?:in|on|for)\s+"
    + A_DATE_VALUE +
    r"(?:\s+(?:now|instead))?\s*[.!]?\s*$", re.I)


NOT_A_DAY = frozenset("""today tonight tomorrow now anymore yet again either neither even sure
really quite very much bad good great one""".split())
CORRECTION_NOT = re.compile(
    r"\b(?:sorry|no|nope|actually|oops)[, ]+not\s+(?:the\s+)?([a-z][a-z'-]{1,20}"
    r"(?: [a-z][a-z'-]{1,15})?)(?:\s+instead\b|\s*[-,.;!?]|$)", re.I)
RETRACT = re.compile(
    r"^\W*(?:(?:ok|okay|no|nope|sorry|actually|wait|oh|hmm|um|yeah)[,.]?\s+)*"
    r"(?:take|taking)\s+(?:that|it|this)\s+back\b(?:\s+(?:then|please|sorry|yeah))?\W*$"
    r"|^\W*(?:(?:ok|okay|no|nope|sorry|actually|wait|oh|hmm|um|yeah)[,.]?\s+)*"
    r"(?:scratch|strike|disregard|ignore|undo|delete)\s+(?:that|it|this)\b"
    r"(?:\s+(?:out|then|please|yeah))?\W*$"
    r"|^\W*(?:(?:ok|okay|no|nope|sorry|actually|wait|oh|hmm|um|yeah)[,.]?\s+)*"
    r"forget\s+(?:what\s+)?i\s+(?:just\s+)?(?:said|told you)\b\W*$", re.I)
CORRECTION_NOT_TO = re.compile(
    r"\b(?:sorry|no|nope|actually|oops)[, ]+not\s+(?:the\s+)?"
    r"([a-z][a-z'-]{1,20}(?: [a-z][a-z'-]{1,15})?)\s*(?:,|;|-|\u2013|\u2014|\bto\b)\s*"
    r"(?:(?:it'?s|its|that'?s)\s+)?"
    r"([a-z][a-z'-]{1,20}(?: [a-z][a-z'-]{1,15})?)(?:\s+instead)?\s*[.!?]?$", re.I)


CORRECTION_NOT_PAIR = re.compile(
    r"\b(?:sorry|no|nope|actually|oops)[, ]+not\s+(?:the\s+)?([a-z0-9][a-z0-9'-]{1,20}"
    r"(?: [a-z0-9][a-z0-9'-]{1,15})?)\s*,\s*(?:its\s+|it's\s+|the\s+)?"
    r"([a-z0-9][a-z0-9'-]{1,20}(?: [a-z0-9][a-z0-9'-]{1,15})?)(?:\s+instead\b|\s*[.;!?]|$)",
    re.I)
DENIAL_OF_A_VALUE = re.compile(
    r"^\W*(?:(?:ok|okay|ah|oh|no|nope|sorry|actually|wait)\b[,.]?\s+){1,2}"
    r"(?P<whose>he|she|it|they)(?:'?s|s)?\s*"
    r"(?:isnt|is\s+not|not|wasnt|was\s+not)\b\W*"
    r"(?:(?:the\s+)?(?!(?:its|it'?s|hes|he'?s|shes|she'?s|theyre|they'?re|called|named)\b)"
    r"(?P<wrong>[a-z][a-z'-]{1,20})?\s*[,.;!?-]*\s*)?"
    r"(?:(?P<says>its|it'?s|hes|he'?s|shes|she'?s|theyre|they'?re"
    r"|(?:he|she|it|they)\s+(?:is|are)|called|named"
    r"|the\s+name\s+is|his\s+name\s+is|her\s+name\s+is|their\s+name\s+is)\b\s*"
    r"(?:called\s+|named\s+)?)?"
    r"(?P<value>[a-z][a-z'-]{1,20})?\s*[.!?]?$", re.I)
A_NAME_IS_TAKEN_BACK = frozenset(("called", "named"))


def a_name_is_taken_back(text):
    denial = DENIAL_OF_A_VALUE.match(str(text or "").strip())
    return bool(denial and denial.group("value")
                and (denial.group("says") or "").strip().lower() in A_NAME_IS_TAKEN_BACK
                and not denial.group("wrong"))


_A_SAID_NAME = r"[a-z][a-z'\-]{1,19}(?:\s+[a-z][a-z'\-]{1,19})?"
NAME_TAKEN_BACK = re.compile(
    r"^\W*(?:(?:no|nope|sorry|ah|oh|actually|wait|oi|hey)[,.!]?\s+){0,2}"
    r"(?:"
    r"i(?:'?m|\s+am)\s+not\s+(?P<said>" + _A_SAID_NAME + r")"
    r"|my\s+name(?:'?s|\s+is)?\s*(?:is|was)?\s*not\s+(?P<said2>" + _A_SAID_NAME + r")"
    r"|my\s+name(?:'?s)?\s*(?:isn'?t|ain'?t|aint)\s+(?P<said3>" + _A_SAID_NAME + r")"
    r"|(?:that|this)(?:'?s|\s+is|\s+was)\s+not\s+my\s+name"
    r"|my\s+name(?:'?s)?\s+(?:is\s+)?wrong"
    r"|you(?:'?ve|\s+have)?\s+got\s+my\s+name\s+wrong"
    r"|(?:please\s+)?(?:don'?t|do\s+not|stop)\s+(?:call|calling)\s+me\s+"
    r"(?P<said4>" + _A_SAID_NAME + r")"
    r")\W*(?:[.!]|\?)?$", re.I)


def _the_same_name(left, right):
    said = " ".join(str(left or "").lower().replace(".", " ").split())
    known = " ".join(str(right or "").lower().replace(".", " ").split())
    if not said or not known:
        return False
    return said == known or said in known.split() or known in said.split()


def the_name_they_take_back(text, stored=""):
    known = str(stored or "").strip()
    if not known:
        return None
    said = " ".join(str(text or "").split())
    from . import filler as _filler
    denial = NAME_TAKEN_BACK.match(_filler.without_filler(said))
    if not denial:
        return None
    named = ""
    for group in ("said", "said2", "said3", "said4"):
        named = named or (denial.group(group) or "").strip()
    if named and not _the_same_name(named, known):
        return None
    return known


CORRECTION_STALL = r"(?:hold\s+on|hold\s+up|hang\s+on)"
NOT_A_VALUE_START = (r"(?!\s*(?:my|your|his|her|our|their|its|thank|thanks|cheers|please"
                     r"|and|but|so|not|nothing|never|no|ok|okay|right|yes|yeah|why|what|how)\b)")
CORRECTION_HEDGE = r"(?:hmm|um+|erm+|well)"
CORRECTION_TAKEBACK = (r"(?:(?:scratch|strike|disregard)\s+(?:that|it|this)"
                       r"|(?:take|taking)\s+(?:that|it|this)\s+back"
                       r"|forget\s+(?:what\s+)?i\s+(?:just\s+)?said"
                       r"|i\s+got\s+(?:that|it|this)\s+wrong"
                       r"|i\s+had\s+(?:that|it|this)\s+wrong"
                       r"|i\s+(?:was|got\s+it)\s+wrong"
                       r"|i\s+made\s+a\s+mistake"
                       r"|i\'?m\s+wrong"
                       r"|my\s+mistake)")
CORRECTION_LEAD = (r"^\s*(?:(?:ok|okay)[,.]?\s+)?"
                   r"(?:(?:(?:no|nope|sorry|wait|ah|oh|actually|oops|"
                   + CORRECTION_STALL + r"|" + CORRECTION_HEDGE + r"|"
                   + CORRECTION_TAKEBACK + r")[,.]?\s+){1,3})")
A_MARKER_ON_THE_END = re.compile(r"\s+(?:actually|really|honestly)\s*[.!?]*\s*$", re.I)


def _the_marker_in_front(text, question=False):
    said = str(text or "").strip()
    end = A_MARKER_ON_THE_END.search(said)
    if end is None:
        return None
    head = said[:end.start()].strip()
    if not head or len(head.split()) > 8:
        return None
    if _extract(head, question):
        return None
    return "actually " + head
CORRECTION_FRAME = (r"(?:(?:it'?s|its|it\s+is|it\s+was|that'?s|thats|that\s+is|that\s+was"
                    r"|he'?s|hes|she'?s|shes|they'?re|theyre|they\s+are)\s+)")
CORRECTION_BARE = re.compile(
    CORRECTION_LEAD
    + r"(?:" + CORRECTION_FRAME + r""
       r"|(?:his|her|its|their|the)\s+names?\s+(?:is\s+|not\s+|was\s+)?)?"
    + NOT_A_VALUE_START +
    r"(?!(?:oops|sorry|wait|hold|hang|hmm|um+|erm+|nope?|actually|oh|ah"
    r"|eh|well)\b)"
                             r"([a-z][a-z'-]{1,20}(?:[ ][a-z][a-z'-]{1,15})?"
                             r"|[\u00a3$\u20ac]?\s?\d[\d,]*(?:\.\d+)?"
                             r"(?:\s?(?:pounds?|quid|euros?|dollars?|k|kilos?|kgs?|kg"
                             r"|stones?|st|lbs?|lb|grams?|g|litres?|liters?|miles?|km"
                             r"|minutes?|mins?|hours?|days?|weeks?|months?|years?)\b)?)"
                             r"\s*[.!?]?$",
                             re.I)
CORRECTION_HEDGED = re.compile(
    CORRECTION_LEAD
    + r"(?:just|only|about|around|roughly|nearly|almost|exactly|more\s+like|closer\s+to)"
    r"\s+(?:(?:it'?s|its|that'?s|thats|the)\s+)?"
    + r"([\u00a3$\u20ac]?\s?\d[\d,]*(?:\.\d+)?"
      r"(?:\s?(?:pounds?|quid|euros?|dollars?|k|kilos?|kgs?|kg|stones?|st|lbs?|lb|grams?|g"
      r"|litres?|liters?|ml|miles?|km|minutes?|mins?|hours?|days?|weeks?|months?|years?"
      r"|people|guests?|adults?|kids?|of\s+us)\b)?"
      r"|" + "|".join(sorted(NUMBER_WORDS, key=len, reverse=True)) + r")"
    r"\s*(?:now\b)?\s*(?:[.!?,]|$)",
    re.I)
CLOCK_PREFERENCE = (r"(?:\s+(?:is|would\s+be|works|suits|sounds)\s*"
                    r"(?:(?:much|a\s+lot|way|far)\s+)?"
                    r"(?:better|best|fine|good|easier|ok|okay)?)?")
CORRECTION_CLOCK = re.compile(
    CORRECTION_LEAD + r"(?:" + CORRECTION_FRAME + r")?(?:at\s+|for\s+)?"
    r"(" + CLOCK_SAID + r")" + CLOCK_PREFERENCE + r"\s*(?:instead|now)?\s*[.!]?$", re.I)
CLOCK_PREFERRED = re.compile(
    r"^\s*(?:(?:and|but|or|so)\s+)?"
    r"(" + CLOCK_SAID + r")\s+"
    r"(?:(?:is|would\s+be|sounds|seems)\s+)?(?:(?:much|a\s+lot|way|far)\s+)?"
    r"(?:better|best|fine|good|easier|ok|okay|w(?:orks|ould\s+work)|suits?|sounds?)"
    r"(?:\s+(?:better|best|fine|good))?"
    r"\s*(?:instead|then|though|now)?\s*[.!]?$", re.I)
AMOUNT_CORRECTION = re.compile(
    r"^\W*(?:(?:sorry|actually|no|nope|ok|okay|wait|well|hmm|um)\b[,.]?\s*)*"
    r"(?:(?:make|makes|change|changed|put)\s+(?:it|that|them)\s+(?:to\s+)?"
    r"|more\s+like\s+(?:[£$\u20ac]\s?)?)"
    r"(\d[\d,. ]{0,12}?)"
    r"(?:\s*(?:a|per|each)\s+(?:day|week|month|year|person|head)\b|"
    r"\s+for\s+(?:the|a|an|our|my|this|that)\s+[\w' -]{1,20}|"
    r"\s*(?:pounds?|quid|euros?|dollars?|bucks)\b|"
    r"\s+(?:instead|now)\b)?\W*$", re.I)
AMOUNT_CORRECTION_BARE = re.compile(
    r"^\W*(?:(?:sorry|actually|no|nope|ok|okay|wait|well|hmm|um)\b[,.]?\s*)+"
    r"(?:(?:it'?s|that'?s)\s+)?(?:make\s+(?:it|that|them)\s+(?:to\s+)?)?"
    r"(\d[\d,. ]{0,12}?)\s*(?:a|per|each)\s+(?:day|week|month|year|person|head)\b\W*$",
    re.I)
AMOUNT_WISH = frozenset("""want wants wanted wanting hope hopes hoped hoping wish wishes
wishing try tries trying tried going gonna like love plan plans planning intend intends
aim aims aiming""".split())
CORRECTION_MARK = re.compile(r"^\W*(?:no|nope|sorry|actually|oops)\b[,.]?\s+"
                             r"(?=(?:i|im|i'm|i've|ive|i'd|my|we|we're|we've|its|it's|i'll|"
                             r"it\s+is|that\s+is)\b)",
                             re.I)
CORRECT_FROM_MARK = ("age", "height", "city", "places", "name", "job", "budget")
CORRECTION_BARE_NO = frozenset("""thanks thank idea ideas worries worry problem way chance
doubt rush need matter point wonder clue reason sorry luck harm""".split())


CORRECTION_SHAPE = {"name": "my name is {}", "age": "i am {}", "budget": "my budget is {}",
                    "city": "i live in {}",
                    "places": "i live in {}", "job": "i work as a {}", "diet": "i am {}",
                    "allergies": "i am allergic to {}", "pets": "i have a {}"}


CLAUSE_OPENERS = frozenset("""i i'm im i've ive i'd id it it's its that that's thats this
we we're we've you you're he she they there here not no yes and but so don't dont doesn't didnt
can't cant won't wont isn't aren't was wasn't weren't is are am was were do does did have has had
could would should can will must might may be been being sorry thanks thank please just really
""".split())


COPULA_SPLIT = re.compile(r"\s+(?:is|was|are|were|be|been|being|seems|seemed|looks|looked|"
                          r"now|then|actually|though|anyway)\b", re.I)


NOT_A_VALUE = frozenset("""nothing anything something everything nobody none someone somebody
anybody everybody them they it him her us you me that this these those there here
anywhere somewhere nowhere everywhere whatever whoever whichever whenever wherever
other another else one ones same such what which who whom whose when where why how whether
he she his hes shes theyre he's she's they're thats im i'm ive i've weve we've
""".split())

POINTING_AT = frozenset("""them they it him her us you me that this these those""".split())

ARTICLES = frozenset("""a an the""".split())


_MONTH_ALT = "|".join(sorted(MONTHS, key=len, reverse=True))
DATE_VALUE = re.compile(
    r"(?:the\s+)?\d{1,2}(?:st|nd|rd|th)(?:\s+of\s+(?:" + _MONTH_ALT + r"))?"
    r"|(?:the\s+)?\d{1,2}\s+(?:" + _MONTH_ALT + r")"
    r"|(?:" + _MONTH_ALT + r")\s+(?:the\s+)?\d{1,2}(?:st|nd|rd|th)?", re.I)

_DAY_NUMBER = r"(?:0?[1-9]|[12]\d|3[01])"
CORRECTION_DATE = re.compile(
    CORRECTION_LEAD + r"(?:" + CORRECTION_FRAME + r")?(?:on\s+|in\s+)?"
    r"(?P<date>(?:the\s+)?" + _DAY_NUMBER + r"(?:st|nd|rd|th)?"
    r"(?:\s+(?:of\s+)?(?:" + _MONTH_ALT + r"))?"
    r"|(?:" + _MONTH_ALT + r")(?:\s+(?:the\s+)?" + _DAY_NUMBER + r"(?:st|nd|rd|th)?)?)"
    r"\s*[.!?]?$", re.I)


_GOING_VERB = (r"(?:fly|flies|flying|go|goes|going|travel|travels|travelling|traveling|head|heads"
               r"|heading|leave|leaves|leaving|visit|visits|visiting|get|gets|getting|are|is)")
_GOING_SAID = (r"(?:(?:we|i|they|he|she)(?:'?re|'?m|'?s)?\s+" + _GOING_VERB +
               r"|(?:the\s+|our\s+|their\s+)?(?:flight|trip|holiday|booking|wedding|party"
               r"|appointment|visit)\s+(?:is|are|'s))")
_GOING_DATE = (r"(?:the\s+)?(?:0?[1-9]|[12]\d|3[01])(?:st|nd|rd|th)?"
               r"(?:\s+(?:of\s+)?(?:" + _MONTH_ALT + r"))?"
               r"|(?:" + _MONTH_ALT + r")(?:\s+(?:the\s+)?" + r"(?:0?[1-9]|[12]\d|3[01])"
               r"(?:st|nd|rd|th)?)?")
CORRECTION_DATE_GOING = re.compile(
    CORRECTION_LEAD + _GOING_SAID + r"\s+(?:out\s+)?(?:on\s+|in\s+)?(?P<date>" + _GOING_DATE
    + r")", re.I)
CORRECTION_GOING_MOVED = re.compile(
    r"^\s*" + _GOING_SAID + r"\s+(?:out\s+)?(?:on\s+|in\s+)?(?P<date>" + _GOING_DATE + r")"
    r"\s+(?:now|instead|this\s+time|from\s+now\s+on)\b", re.I)


CORRECTION_TAIL_WORDS = frozenset("""sorry soz thanks cheers please pls
    instead then now though tho anyway either too also again ok okay ha haha lol lmao""".split())
CORRECTION_TAIL = (r"(?:" + CORRECTION_WHY + r")?"
                   r"(?:\s*,?\s*(?:i\s+mean|i\s+meant|i\s+mean\s+it|"
                   r"(?:" + "|".join(sorted(CORRECTION_TAIL_WORDS)) + r")))"
                   r"*\s*[.!?]?\s*$")


def _a_tail_hangs_off(pattern, then=""):
    if not pattern.rstrip().endswith("$"):
        return pattern
    return pattern.rstrip()[:-1] + then + CORRECTION_TAIL


CORRECTION_TRIP_FRAME = (r"(?:\s+(?:we|i)\s+(?:go|went|'re\s+going|are\s+going|'m\s+going"
                         r"|am\s+going)(?:\s+to)?)?")
CORRECTION_BARE = re.compile(_a_tail_hangs_off(CORRECTION_BARE.pattern,
                                               CORRECTION_TRIP_FRAME), re.I)
CORRECTION_DATE = re.compile(
    _a_tail_hangs_off(CORRECTION_DATE.pattern,
                      r"(?:\s+at\s+\d{1,2}(?::\d{2})?\s*(?:am|pm|o'?clock)?)?"), re.I)
AMOUNT_CORRECTION_BARE = re.compile(_a_tail_hangs_off(AMOUNT_CORRECTION_BARE.pattern), re.I)


def a_value(phrase):
    parts = re.findall(r"[a-z0-9']+", str(phrase or "").lower())
    if not parts:
        return False
    if len(parts) > 3 and not DATE_VALUE.fullmatch(str(phrase or "").strip()):
        return False
    if parts[0] in CLAUSE_OPENERS or parts[0] in NOT_A_VALUE:
        return False
    if any(word in POINTING_AT for word in parts[1:]):
        return False
    names = [word for word in parts if word not in ARTICLES]
    return any(word not in NOT_A_VALUE and word not in CLAUSE_OPENERS for word in names)


def reread(value, key):
    shape = CORRECTION_SHAPE.get(key)
    value = re.sub(r"^(?:a|an|the)\s+", "", str(value or "").strip(), flags=re.I)
    if not shape or not value:
        return {}
    found = extract(shape.format(value))
    found.pop("correction", None)
    return found
NO_THEN_A_THING_NAMED = re.compile(
    r"^\s*(?:no|nope|sorry|oops)[,.]?\s+(?:a|an)\s+"
    r"([a-z][a-z'-]{1,20}(?:\s[a-z][a-z'-]{1,15})?)\s*[.!?]?\s*$", re.I)

JOB_AFTER = re.compile(r"\b(?:i(?:'m| am)|im)\s+(?:now |just )?(?:a|an)\s+([a-z][a-z '-]{2,30})",
                       re.I)
JOB_BECOME = re.compile(r"\b(?:(?:i(?:'ve| have)?|ive)\s+(?:just\s+)?(?:become|became|retrained as|"
                        r"qualified as))\s+(?:a|an)\s+([a-z][a-z '-]{2,30})",
                        re.I)
JOB_WAS = re.compile(
    r"\b(?:i|we)\s+(?:was|were|used to be|used to work as|worked as|was working as|"
    r"were working as)\s+(?:(as)\s+)?((?:an?|the)\s+)?"
    r"([a-z][a-z '-]{2,30}?)(?=\s+(?:before|until|till|then|after|years|when|but|and|"
    r"in \d{4}|at the time)\b|[,.;!?]|$)", re.I)
WAS_NOT_A_JOB = frozenset("""kid kids child children boy girl baby toddler teenager teen lad lass
man woman person human""".split())
JOB_WORK = re.compile(r"\b(?:i work (as|in|at|for|on)|i work|my job is|"
                      r"i(?:'m| am) working as|im working as)"
                      r"\s+((?:an?|the)\s+)?([a-z][a-z '-]{2,30})", re.I)
JOB_FRAME = frozenset(("in", "at", "for", "on"))
JOB_APPOSITIVE = re.compile(r",\s*(?:a|an)\s+([a-z][a-z '-]{2,30})", re.I)
POSSESSION = re.compile(
    r"\b(?:i|we)(?:\s+(?:have|had|has|got|own|bought|keep|kept|just got|recently got))\b[^,]*,\s",
    re.I)
CORRECTION_OPENER_WORDS = frozenset("""no nope not sorry soz ok okay well actually oh ah
    yes yeah nah right wait anyway and but so then also just hi hey hello thanks please""".split())
JOB_GOT_AT = re.compile(
    r"\b(?:i|i've|ive)\s+(?:just\s+|finally\s+|only\s+|now\s+|recently\s+)?"
    r"(?:got|get|gotten|landed|bagged|start|started|began|begin|begun)"
    r"\b[^.!?]{0,25}?\b(?:job|role|position|contract)\b"
    r"(?!\s+(?:interview|interviews|offer|offers|application|applications|trial))"
    r"[^.!?]{0,20}?\b(at|with|in)\s+(an?\s+|the\s+)?([a-z][a-z '&.-]{2,30})", re.I)
JOB_GOT_FRAME = frozenset(("at", "with", "in"))
JOB_GOT_NOT_A_PLACE = NOT_PLACES | frozenset("""soon notice point start beginning first last next
day week weeks month months moment present past future offer interview application trial salary
wage wages money hours shift shifts nights evenings mornings""".split())
JOB_GOT_POSSESSIVE = re.compile(r"^(?:my|our|your|their|his|her|its|mine|ours|yours)\b", re.I)
JOB_GOT_AN_EMPLOYER = frozenset("""hospital school college university office surgery
practice nursery""".split())


def a_place_that_employs(phrase):
    words = str(phrase or "").strip(" .!?,").split()
    if not words:
        return False
    said = " ".join(words)
    if JOB_GOT_POSSESSIVE.match(said):
        return False
    if (words[0].lower() in JOB_GOT_NOT_A_PLACE
            and words[0].lower() not in JOB_GOT_AN_EMPLOYER):
        return False
    return True
JOB_AS_A = re.compile(r"\bjob\s+as\s+(?:an?\s+)?([a-z][a-z '-]{2,30})", re.I)
JOB_OWN_VOICE = re.compile(r"\b(?:i|i've|ive|im|i'm)\b", re.I)
JOB_MINE = re.compile(r"\bmy\s+(?:new\s+|first\s+|current\s+)?$", re.I)
JOB_WANTED = re.compile(r"\b(?:want|wanted|wanting|wants|looking for|hoping|hope|apply|applied|"
                        r"applying|application|would like|thinking of|considering|training to|"
                        r"study|studying|studied|need|needs|trying|try|dream|goal|someday|"
                        r"one day|qualified|interview|interviewing)\b", re.I)
JUDGEMENT_NOUNS = frozenset("""
burden joke doormat letdown disappointment waste problem mistake nuisance embarrassment fraud
imposter impostor hypocrite mess failure loser idiot muppet moron fool clown
coward liar cheat bully crybaby slob brat wimp
""".split())

JOB_STOP = frozenset("""bit little big huge real good bad terrible complete total rubbish great
boring bored stressful exhausting tiring draining demanding repetitive mind numbing busy quiet slow
fine okay ok awful horrible crap pants nightmare easy hard tough long short dull repetitive
massive proper new first second lot lots fan week month year while bit bit more less couple
surprise
few kind sort mum dad mother father parent nan granny grandad
woman women man men girl boy lady ladies bloke guy teenager teen pensioner
brit briton englishman englishwoman scotsman scotswoman
somewhere anywhere nowhere""".split())
SELF_JUDGEMENT = frozenset("""
bad terrible awful horrible rubbish useless hopeless worthless pathetic stupid dumb thick
idiot imbecile moron failure loser letdown disappointment burden nuisance waste mess disaster
wreck nightmare fool clown muppet fraud imposter impostor hypocrite doormat lazy selfish
greedy ungrateful nasty boring shit crap lousy naff rotten dreadful
shitty crappy crapola shite pants wank bollocks tosser twat prick git sod bugger arse arsehole
""".split())
ROLE_YOU_CAN_FAIL = frozenset("""
mum mom mummy mam mother mumma dad daddy father parent parents guardian carer friend partner
husband wife son daughter brother sister sibling child kid colleague coworker boss manager
employee worker teacher nurse doctor cook driver parent person student pupil apprentice learner
""".split())
SELF_JUDGEMENT_ROLE_ONLY = frozenset("poor".split())
SELF_AS_A_ROLE = re.compile(
    r"\b(?:i'?m|i am|im|we'?re|we are)\s+(?:a|an|such a|such an)\s+(?:[a-z][a-z'-]*\s+)?$"
    r"|\b(?:feel|feels|felt|feeling)\s+like\s+(?:a|an|such a|such an)\s+",
    re.I)
NOT_A_JUDGEMENT_AFTER = (r"(?!\s+(?:lot|bit|deal|day|days|week|weekend|month|year|time|times|"
                         r"mood|thing|things|while|way|shame|pity|job)\b)")
SELF_JUDGEMENT_SAID = re.compile(
    r"\b(?:im|i am|i feel|i felt|feeling|feel)\s+(?:like\s+)?"
    r"(?:such\s+|a bit of\s+|a bit\s+|a right\s+|a total\s+|a complete\s+|really\s+|so\s+|"
    r"just\s+|always\s+|pretty\s+|very\s+|quite\s+)*(?:a\s+|an\s+)?"
    r"(?:" + "|".join(sorted(SELF_JUDGEMENT)) + r")\b" + NOT_A_JUDGEMENT_AFTER
    + r"|\b(?:im|i am|i feel|i felt|feeling|feel)\s+(?:like\s+)?(?:a\s+|an\s+|a right\s+|such a\s+)"
    r"(?:" + "|".join(sorted(SELF_JUDGEMENT_ROLE_ONLY)) + r")\s+"
    r"(?!(?:lot|bit|day|days|week|weekend|month|year|time|times|mood|thing|things|while|"
    r"lot better|deal)\b)[a-z]+", re.I)


SELF_JUDGEMENT_ABOUT_A_NOUN = re.compile(
    r"\b(?:im|i am|i feel|i felt|feeling|feel)\s+(?:like\s+)?(?:a|an)\s+(?P<judged>"
    + "|".join(sorted(SELF_JUDGEMENT | SELF_JUDGEMENT_ROLE_ONLY))
    + r")\s+(?P<next>[a-z][a-z'-]*)", re.I)
JUDGEMENT_TAIL = frozenset("""and but so because though although when whenever if at in on
really tbh again today tonight now honestly actually anyway though still even too also as for
with of from to that which who""".split())


def is_a_judgement(text):
    low = " ".join(str(text or "").lower().replace("\u2019", "'").replace("'", "").split())
    about = SELF_JUDGEMENT_ABOUT_A_NOUN.search(low)
    if about:
        noun = about.group("next")
        if noun in JUDGEMENT_TAIL:
            return about.group("judged") in SELF_JUDGEMENT or about.group("judged") in ROLE_YOU_CAN_FAIL
        return noun in ROLE_YOU_CAN_FAIL or noun in SELF_JUDGEMENT or noun in JUDGEMENT_NOUNS
    return bool(SELF_JUDGEMENT_SAID.search(low))
TAKE_BACK = (" not ", " rather than ", " instead of ")
TAKE_BACK_SPLIT = re.compile(r"\s*(?:,|;)?\s+(?:not|rather than|instead of)\b", re.I)
QUALIFYING = frozenset("""
far too very that quite long much more near close nearby just only really entirely totally
always good bad great nice close
""".split())


def take_back_cut(phrase):
    text = str(phrase or "")
    for match in TAKE_BACK_SPLIT.finditer(text):
        after = text[match.end():].split()
        if after and after[0].lower().strip(".,;:!?") in QUALIFYING:
            continue
        return text[:match.start()]
    return text


def qualified_by(phrase):
    text = str(phrase or "")
    for match in TAKE_BACK_SPLIT.finditer(text):
        after = text[match.end():].split()
        if not after or after[0].lower().strip(".,;:!?") not in QUALIFYING:
            continue
        said = text[match.start():].strip(" ,.;:-'")
        if said:
            return said
    return ""
def _the_role(words):
    words = list(words[:3])
    while words and words[-1].lower().strip(".,!?") in JOB_DANGLING:
        words.pop()
    return " ".join(word.lower() for word in words)


JOB_DANGLING = frozenset("""a an the on at in of for with to and but so who that my our their his her
its this these those over under near across by from as""".split())
JOB_TAIL = (" in ", " at ", " for ", " with ", " who ", " that ", " and ", " but ", " so ") + TAKE_BACK
JOB_TAIL_PLACE = JOB_TAIL + (" on ", " near ", " across ", " covering ", " doing ",
                         " starting ", " starts ", " beginning ", " begins ")
CHANGED_WORK = re.compile(r"\b(?:(?:changed|switched|left|quit|packed in|gave up|lost)\s+"
                          r"(?:my |the )?(?:job|jobs|work|role|career)\b|new job\b)", re.I)
WORK_NOW = re.compile(r"\b(?:i(?:'m| am)|im|we(?:'re| are))\s+(?:now\s+)?"
                      r"(?:working\s+)?(in|at)\s+(an?|the)?\s*"
                      r"([a-z][a-z '-]{2,30}?)\s+(?:now|these days)\b", re.I)


WORK_DETAIL = frozenset("""
    night nights day days evening evenings morning mornings afternoon afternoons weekend
    weekends weekday weekdays shift shifts earlies lates late early overtime flexi flexitime
    home away abroad remotely onsite hybrid
""".split())
WORK_DETAIL_FILLER = frozenset("""
    a an the from at in on to my two three four both all full part time times job jobs of and
    every most some
""".split())


def is_a_place_of_work(frame):
    preposition = str(frame or "").strip().split(" ")[0].lower()
    return preposition in ("in", "at", "on")


def is_a_work_detail(value, frame=None):
    if is_a_place_of_work(frame):
        return True
    words = re.findall(r"[a-z']+", str(value or "").lower())
    meaningful = [word for word in words if word not in WORK_DETAIL_FILLER]
    if not meaningful:
        return bool(words)
    return all(word in WORK_DETAIL or word == "job" or word == "jobs" for word in meaningful)


def work_weight(value, frame=None):
    if not is_a_work_detail(value, frame):
        return 3
    return 2 if is_a_place_of_work(frame) else 1


def _finish(word):
    return word.strip().strip(".,!?;:'\"").lower()


THE_MOMENT = ("right now", "at the moment", "at present", "just now", "these days", "for now",
              "nowadays", "currently", "anymore", "any more", "already", "still", "now",
              "today", "tonight")


def without_the_moment(words):
    words = [word for word in words if str(word or "").strip()]
    while len(words) > 1:
        cut = 0
        for span in (3, 2, 1):
            if len(words) >= span and _finish(" ".join(words[-span:])) in THE_MOMENT:
                cut = span
                break
        if not cut:
            break
        words = words[:-cut]
    if len(words) == 1 and _finish(words[0]) in THE_MOMENT:
        return []
    return words


TONE_TAIL = ("to be honest", "if i am honest", "if im honest", "i must say", "by the way",
             "for the record", "just so you know", "i suppose", "i guess", "to be fair",
             "haha", "hehe", "lol", "lmao", "hmm", "though", "honestly", "actually",
             "anyway", "tbf", "ngl", "imo", "tbh", "tho")


INFINITIVE = re.compile(r"\b(?:going|go|goes|went|want|wants|wanted|need|needs|needed|try|tries|"
                        r"trying|tried|mean|means|meant|promise|promised|learn|learned|learnt|"
                        r"used|rather|hope|hoping|hate|hates|love|loves|have|has|had|like|likes|"
                        r"prefer|plan|planning|planning)\s*$", re.I)
NOT_AN_END = frozenset("""to of and but or nor not never the a an my your his her their our its
is am are was were be been do does did has have had will would shall should can could must
may might""".split())
MAY_AS_A_MONTH = frozenset("""in on by from until till to before after during through for
early late mid this next last coming end start""".split())
DAY_OF_A_MONTH = re.compile(r"^\d{1,2}(?:st|nd|rd|th)?$")


def _can_end(words):
    if not words:
        return False
    last = words[-1].lower().strip(".,!?;:'\"")
    if last not in NOT_AN_END:
        return True
    if last == "may" and len(words) > 1:
        before = words[-2].lower().strip(".,!?;:'\"")
        return before in MAY_AS_A_MONTH or bool(DAY_OF_A_MONTH.match(before))
    return False


def no_tone(text):
    out = str(text or "").strip()
    for _ in range(3):
        low = out.lower().rstrip(" .,!?;:")
        cut = next((phrase for phrase in TONE_TAIL
                    if low.endswith(" " + phrase) or low == phrase), None)
        if not cut:
            break
        left = out[:len(low) - len(cut)].rstrip(" ,;:-.)")
        words = left.split()
        if cut.startswith("to ") and INFINITIVE.search(" ".join(words)):
            break
        if words and not _can_end(words):
            break
        out = left
    return out if out.strip(" ,;:-.") else ""

def _date_change(text):
    line = str(text or "")
    if "?" in line:
        return None
    for pattern in (CHANGED_TO, CHANGED_BARE, CHANGED_NOW, CORRECTION_A_DATE,
                    A_TIME_INSTEAD, MOVED_BY_ITS_OWN_VERB):
        found = pattern.search(line)
        if found is None:
            continue
        for group in found.groups():
            if group and _a_date(group):
                return _tidy(group)
    return None


ORDINAL_DAY = re.compile(r"(?:the\s+)?\d{1,2}(?:st|nd|rd|th)", re.I)
A_DATE_WORD = MONTHS | DAYS


MOVED_PLACE_TO = re.compile(
    r"\b(?:we|i|they|you|we've|weve|i've|ive|they've)\b[^.!?]{0,24}?"
    r"\b(?:changed|change|moved|move|switched|switching|swap|swapped|shifted|transferred|"
    r"rebooked|booked)\s+(?:it|that|this|the\s+booking|the\s+trip|the\s+holiday|the\s+flight)"
    r"\s+(?:to|for|instead\s+to)\s+([A-Za-z][A-Za-z' -]{1,30})", re.I)
MOVED_PLACE_PASSIVE = re.compile(
    r"\b(?:booking|trip|holiday|flight|plan|reservation|its|it's|it)\b[^.!?]{0,30}?"
    r"\b(?:has|have|had|is|its|it's|was|were|been)\s+(?:been\s+)?"
    r"(?:changed|moved|switched|swapped|shifted)\s+to\s+([A-Za-z][A-Za-z' -]{1,30})", re.I)
NOT_A_PLACE_NAME = frozenset("""one ones other others same thing place somewhere else front back
side left right first second third last next top bottom middle here there it that this""".split())


def a_moved_place(text):
    line = str(text or "")
    if not line or "?" in line:
        return ""
    for pattern in (MOVED_PLACE_TO, MOVED_PLACE_PASSIVE):
        for found in pattern.finditer(line):
            places, _home, _said = _places("we are going to " + found.group(1))
            for place in places:
                if _a_date(place) or a_moved_time(place):
                    continue
                if place.lower() in NOT_A_PLACE_NAME:
                    continue
                return place
    return ""


def a_date_put_right(text):
    line = str(text or "")
    if "?" in line:
        return False
    return bool(CORRECTION_A_DATE.search(line) or A_DAY_TAKEN_BACK.search(line)
                or A_DAY_I_MEANT.search(line) or A_TIME_INSTEAD.search(line))


def the_date_put_right(text):
    line = str(text or "")
    if "?" in line:
        return ""
    for pattern in (CORRECTION_A_DATE, A_DAY_TAKEN_BACK, A_DAY_I_MEANT, A_TIME_INSTEAD):
        found = pattern.search(line)
        if found is not None:
            for group in found.groups():
                if group and _a_date(group):
                    return group.strip(" .,")
    return ""


def a_trip_date_put_right(text):
    line = str(text or "")
    if "?" in line:
        return ""
    found = TRIP_DATE_MOVED.search(line)
    if found is None:
        return ""
    for group in found.groups():
        if group and _a_date(group):
            return _tidy(group)
    return ""


def _a_date(word):
    phrase = str(word or "").strip()
    if not phrase:
        return False
    seen = False
    a_month = False
    a_plain_number = False
    for piece in re.split(r"\s+", phrase.lower()):
        if piece in ("of", "the"):
            continue
        if ORDINAL_DAY.fullmatch(piece) or piece in A_DATE_WORD:
            seen = True
            a_month = a_month or piece in MONTHS
            continue
        if piece.isdigit() and len(piece) <= 2 and not a_plain_number:
            a_plain_number = True
            continue
        return False
    return seen or (a_plain_number and a_month)


def _tidy(word):
    word = word.strip().strip(".,!?;:'\"")
    return word[:1].upper() + word[1:] if word else word


def _tidy_a_titled_name(word):
    words = str(word or "").split()
    if len(words) > 1 and words[0].strip(".").lower() in TITLE_WORDS:
        return " ".join(_tidy(part) for part in words)
    return _tidy(word)
A_LEAD_PREPOSITION = ("to", "in", "at", "on", "for", "into")
A_LEAD_IDIOM = frozenset("""fact facts all general public advance particular least long
last once time times order case place touch person people""".split())


def _the_value_alone(phrase):
    words = str(phrase or "").split()
    while len(words) > 1 and words[-1].strip(".,!?;:'\"").lower() in CORRECTION_TAIL_WORDS:
        words.pop()
    if len(words) > 2 and [w.lower() for w in words[-2:]] in (["i", "mean"], ["i", "meant"]):
        words = words[:-2]
    if (len(words) > 1 and words[0].lower() in A_LEAD_PREPOSITION
            and words[1].strip(".,!?;:'\"").lower() in A_LEAD_IDIOM):
        return ""
    if (len(words) > 1 and words[0].lower() in A_LEAD_PREPOSITION
            and re.search(r"[a-z]", words[1], re.I)
            and not (words[0].lower() == "for" and words[1].lower().endswith("ing"))):
        words = words[1:]
    return " ".join(words)


def _tidy_apart(word):
    word = word.strip().strip(".,!?;:'\"")
    first, _, rest = word.partition(" ")
    if first.lower() in ARTICLES:
        return (first.lower() + (" " + rest if rest else "")).strip()
    return word[:1].upper() + word[1:] if word else word


INTRO_WORDS = ("hi", "hey", "hello", "yo", "morning", "evening", "alright", "howdy", "hullo")


NAME_FRAMES = ("", "im", "iam", "i'm", "i am", "i go by", "i goes by", "we go by",
               "we goes by")


def _lowercase_name_fits(text, match):
    head = text[:match.start(1)]
    for mark in ".!?;":
        at = head.rfind(mark)
        if at != -1:
            head = head[at + 1:]
    head = head.lower().replace("\u2019", "'")
    for phrase in NAME_FILLER_PHRASES:
        head = head.replace(phrase, " ")
    words = [word.strip(",.!?;:'\"()") for word in head.split()]
    left = [word for word in words if word and not _filler_or_intro(word)]
    return " ".join(left) in NAME_FRAMES


def _filler_or_intro(word):
    if word in NAME_FILLER or word in INTRO_WORDS:
        return True
    settled = re.sub(r"(.)\1+", r"\1", word)
    if settled == word:
        return False
    return (settled in NAME_FILLER or settled in INTRO_WORDS
            or _squeezed(word) in _SQUEEZED_INTROS)


def _squeezed(word):
    return re.sub(r"(.)\1+", r"\1", word)


_SQUEEZED_INTROS = frozenset(_squeezed(word) for word in INTRO_WORDS) | {
    _squeezed(word) for word in NAME_FILLER}


VERB_ISH = re.compile(r"^[a-z]{3,}(?:in|ing)$", re.I)
TAIL_DETERMINERS = frozenset("my our the a an this that some his her their".split())


def _tail_has_a_verb(words):
    for word in words:
        low = word.lower()
        if low in SAYS_SOMETHING_VERBS or low.endswith("'s") or low.endswith("\u2019s"):
            return True
        if low in SAYS_SOMETHING_ELSE:
            return True
        if len(low) > 4 and low.endswith("ed"):
            return True
    return False


SAYS_SOMETHING_VERBS = frozenset("""is are am was were be been being have has had got get gets
do does did will would can could should shall may might must need needs want wants live lives
work works like likes love loves hate hates know knows say says go goes come comes died passed
lost found""".split())

SAYS_SOMETHING_ELSE = frozenset("""hurts hurt aches ache aches bleeds bleed swells swells throbs
throb stings sting itches itch kills kill feels feel looked looks seems seems
ran fell left went came broke broke got lost found said told bought sold died ate slept hurt felt
became caught threw took gave made drove wrote saw heard thought stood sat woke quit
""".split())


def _followers_fit(text, end, name_word=None):
    tail = re.split(r"[.!?;,]", text[end:], 1)[0]
    tail = _without_asides(tail)
    found = re.findall(r"[A-Za-z0-9']+", tail)
    at = 0
    while at < len(found):
        word = found[at]
        low = word.lower()
        at += 1
        if word.isdigit() or word[:1].isupper():
            continue
        if low in NAME_SAYS_ABOUT_ME:
            if (name_word and VERB_ISH.match(str(name_word)) and low in TAIL_DETERMINERS
                    and not _tail_has_a_verb(found[at:])):
                return False
            return True
        if low in NAME_FOLLOWERS:
            continue
        if low in NAME_PLACE_WORDS:
            if at < len(found) and found[at].lower() in PLACE_JOIN:
                at += 1
            if at >= len(found):
                return False
            at += 1
            continue
        return False
    return True


def _without_asides(tail):
    low = tail.lower().replace("\u2019", "'").replace("'", "")
    changed = True
    while changed and low.strip():
        changed = False
        for aside in NAME_ASIDES:
            aside = aside.replace("'", "")
            stripped = low.rstrip(" ,.!?")
            if stripped.endswith(aside):
                cut = stripped[: -len(aside)].rstrip(" ,")
                low = cut
                tail = cut
                changed = True
                break
    return tail


def _a_state_word(low):
    return (low in NOT_NAMES or low in NOT_NAMES_EXTRA or low in NOT_A_NAME_FEELING
            or low in NOT_A_NAME_ILLNESS or low in DIET_WORDS or low in SOBER_WORDS)


STATE_DEGREES = (("iest", "y"), ("ier", "y"), ("iest", ""), ("ier", ""),
                 ("est", ""), ("er", ""))
def _a_degree_of_a_state(low):
    for ending, restore in STATE_DEGREES:
        if not low.endswith(ending) or len(low) <= len(ending) + 2:
            continue
        stem = low[: -len(ending)] + restore
        if _a_state_word(stem):
            return True
        if len(stem) >= 3 and stem[-1] == stem[-2] and _a_state_word(stem[:-1]):
            return True
    return False


def _a_letter_too_many(low):
    if len(low) < 5 or low[-1] != low[-2]:
        return False
    return _a_state_word(low[:-1])


def _sounds_like_a_state(low):
    if low in NAMES_THAT_LOOK_LIKE_STATES:
        return False
    if _a_degree_of_a_state(low) or _a_letter_too_many(low):
        return True
    for tail, shortest in NAME_TAIL_MIN.items():
        if len(low) >= shortest and low.endswith(tail):
            return True
    return False


def _a_word_that_is_a_state(word):
    return len(word) >= 3 and (
        word in NOT_A_NAME_STATE or word in lexicon.FEELINGS or word in lexicon.A_STATE
        or word in NOT_NAMES_EXTRA)


LOOKS_WORDS = frozenset("""
blonde blond brunette ginger redhead fair pale tanned olive freckled spotty pimply
curly straight bald bearded
""".split())


def _a_word_not_a_name(low):
    return (low in LOOKS_WORDS or low in NUMBER_WORDS
            or _sounds_like_a_state(low) or _a_word_that_is_a_state(low))


COMPARED = (("er", 5), ("est", 6))


def _the_state_compared(word):
    for ending, shortest in COMPARED:
        if len(word) < shortest or not word.endswith(ending):
            continue
        stem = word[: -len(ending)]
        if not stem:
            continue
        for state in (stem, _with_its_y_back(stem), stem + "y", stem + "e",
                      *_a_letter_off_each_run(stem)):
            if state and _a_word_that_is_a_state(state):
                return state
    return None


def _with_its_y_back(stem):
    if stem.endswith("i"):
        return stem[:-1] + "y"
    return None


def _a_letter_off_each_run(word):
    out = []
    at = 0
    while at < len(word):
        end = at
        while end + 1 < len(word) and word[end + 1] == word[at]:
            end += 1
        if end > at:
            out.append(word[:end] + word[end + 1:])
        at = end + 1
    return tuple(out)


def _a_state_written_as_a_comparison_or_a_double(low):
    if normalize.reads_as_a_feeling(low) or _the_state_compared(low):
        return True
    if normalize.the_feeling_two_letters_are_gone_from(low):
        return True
    for cut in _a_letter_off_each_run(low):
        if _a_word_that_is_a_state(cut) or _the_state_compared(cut):
            return True
    return False


def _name(text):
    went_by = _name_from(GOES_BY_NAME, text, guessed=True)
    if not went_by and GOES_BY_NAME.search(text):
        for clause in CLAUSE_SPLIT.split(text):
            if not GOES_BY_NAME.search(clause):
                continue
            went_by = _name_from(GOES_BY_NAME, clause, guessed=True)
            if went_by:
                break
    for pattern in ANNOUNCED_NAME_PATTERNS:
        name = _name_from(pattern, text, guessed=False)
        if name:
            if went_by and went_by.lower() != name.lower():
                return went_by
            return name
    for pattern in GUESSED_NAME_PATTERNS:
        name = _name_from(pattern, text, guessed=True)
        if name:
            return name
    return None



SAYS_A_NAME = re.compile(r"\b(?:my name is|my name's|my names|i am called|im called|"
                         r"call me|you can call me|known as)\b", re.I)


def _a_judgement_on_themselves(low):
    if low in SELF_JUDGEMENT:
        return True
    for ending in ("ish", "y"):
        if not low.endswith(ending) or len(low) <= len(ending) + 2:
            continue
        stem = low[: -len(ending)]
        if stem in SELF_JUDGEMENT:
            return True
        if stem[-1] == stem[-2] and stem[:-1] in SELF_JUDGEMENT:
            return True
    return False


def _name_from(pattern, text, guessed):
    for match in pattern.finditer(text):
        word = match.group(1)
        low = _finish(word)
        if (low in NOT_NAMES or low in NOT_NAMES_EXTRA or low in GO_BY_WAYS
                or low in DIET_WORDS or low in SOBER_WORDS
                or low in lexicon.JOINED_WORDS or len(low) < 2):
            continue
        if not word[:1].isupper() and (low in NOT_A_NAME_STATE or _a_judgement_on_themselves(low)
                                       or low in NOT_A_NAME_LAUGH or lexicon.is_a_laugh(low)):
            continue
        spelled = normalize.spelled(low)
        if low not in NAMES_THAT_LOOK_LIKE_STATES and any(
                one in NOT_NAMES or one in NOT_NAMES_EXTRA or one in NOT_A_NAME_STATE
                for one in spelled if one != low):
            continue
        if low in NUMBER_WORDS:
            continue
        repaired = normalize.repaired_tokens(low)
        if low not in NAMES_THAT_LOOK_LIKE_STATES and any(
                one in NOT_NAMES or one in NOT_NAMES_EXTRA or one in NOT_A_NAME_STATE
                for one in repaired if one != low and len(one) >= len(low)):
            continue
        if guessed and low not in NAMES_THAT_LOOK_LIKE_STATES and _describes_them(low):
            continue
        if guessed and low not in NAMES_THAT_LOOK_LIKE_STATES and any(
                one != low and len(one) >= len(low) and _sounds_like_a_state(one)
                for one in repaired):
            continue
        if _a_state_written_as_a_comparison_or_a_double(low) and not SAYS_A_NAME.search(text):
            continue
        if normalize.reads_as_a_sound(low) and not SAYS_A_NAME.search(text):
            continue
        if not word[:1].isupper():
            if _sounds_like_a_state(low) and not SAYS_A_NAME.search(text):
                continue
            if guessed and (not _lowercase_name_fits(text, match)
                            or not _followers_fit(text, match.end(1), word)):
                continue
        return word[0].upper() + word[1:]
    return None


def _first_tail(phrase, tails=JOB_TAIL):
    found = None
    for tail in tails:
        at = phrase.find(tail)
        if at != -1 and (found is None or at < found[0]):
            found = (at, tail)
    return found


def _job_as_a(text):
    found = []
    for match in JOB_AS_A.finditer(text):
        clause = CLAUSE_EDGE.split(text[:match.start()])[-1]
        if JOB_WANTED.search(clause) or _people(clause):
            continue
        if not (JOB_OWN_VOICE.search(clause) or JOB_MINE.search(clause)):
            continue
        found.append(match)
    return found


JUDGEMENT_AFTER = frozenset("""to for at in of on with and but because when yet either too
about around""".split() + """sometimes today lately honestly though mostly usually always really
actually generally now these days""".split())


def _is_a_judgement_phrase(words):
    if not words or words[0].lower() not in JUDGEMENT_NOUNS:
        return False
    return len(words) == 1 or words[1].lower() in JUDGEMENT_AFTER


def _only_discourse_before(before):
    words = re.findall(r"[a-z']+", str(before or "").lower())
    return all(word in CORRECTION_OPENER_WORDS for word in words)


def _the_correction_named_a_thing(text, match):
    if not _only_discourse_before(text[:match.start()]):
        return False
    groups = match.groups()
    phrase = ((groups[-1] if len(groups) > 2 else groups[0]) or "").strip().lower()
    words = phrase.split()
    return bool(words) and words[0] not in JOB_WORDS


ROLE_ENDING = ("er", "or", "ist", "ian", "man", "woman", "ess", "ant", "ent")


def _was_names_a_role(phrase, article=None):
    low = [word.lower().strip(".,!?;:") for word in str(phrase or "").split() if word.strip()]
    while low and low[0] in ("both", "all", "just", "only", "still", "now", "then", "also"):
        low.pop(0)
    low = low[:3]
    if article and low:
        return True
    if not low:
        return False
    if any(len(word) > 4 and word.endswith(("ing", "ed")) for word in low):
        return False
    head = low[-1]
    if head in STATE_WORDS or head in PAST_STATES or head in PREGNANCY_STATES:
        return False
    single = [word[:-1] if word.endswith("s") and word not in JOB_WORDS else word for word in low]
    if any(word in JOB_WORDS for word in low + single):
        return True
    return len(head) > 4 and head.endswith(ROLE_ENDING)


def _job_and_city(text, name=None, question=False):
    job = city = None
    frame = ""
    if name:
        at = text.lower().find(name.lower())
        if at != -1:
            text = text[at + len(name):]
    matches = (list(JOB_AFTER.finditer(text)) or list(JOB_BECOME.finditer(text))
               or list(JOB_WORK.finditer(text)) or list(JOB_WAS.finditer(text))
               or _job_as_a(text) or list(JOB_GOT_AT.finditer(text)))
    if not matches and not POSSESSION.search(text):
        matches = [match for match in JOB_APPOSITIVE.finditer(text)
                   if not _the_correction_named_a_thing(text, match)]
        if question:
            matches = [match for match in matches
                       if re.search(r"\bi(?:'m|m| am)\b", text[:match.start()], re.I)]
    if not matches:
        return job, city, frame
    for match in matches:
        groups = match.groups()
        was_working = len(groups) > 2
        phrase = (groups[-1] if was_working else groups[0]).strip()
        place_job = (was_working and (groups[0] or "").lower() in ("in", "at", "for", "on")) \
            or match.re is JOB_AS_A or match.re is JOB_GOT_AT
        cut = _first_tail(phrase)
        if place_job and not cut:
            cut = _first_tail(phrase, tails=JOB_TAIL_PLACE)
        if cut:
            at, tail = cut
            rest = phrase[at + len(tail):]
            if tail.strip() in ("in", "at") and not city:
                place = re.match(r"([A-Z][a-z]+(?: [A-Z][a-z]+)?)", rest.strip())
                if place and place.group(1).split()[0].lower() not in NOT_PLACES:
                    city = place.group(1)
            phrase = phrase[:at]
        if match.re is JOB_GOT_AT:
            if (groups[0] or "").lower() == "in" and not (groups[1] or "").strip():
                continue
            if not a_place_that_employs(phrase):
                continue
        words = without_the_moment(phrase.split())
        if match.re is JOB_WAS and words and words[0].lower() in WAS_NOT_A_JOB:
            continue
        if match.re is JOB_WAS and not _was_names_a_role(
                phrase, article=len(groups) > 1 and groups[1]):
            continue
        if (not words or words[0].lower() in JOB_STOP or words[0].lower() in NOT_NAMES
                or words[0].lower() in NOT_NAMES_EXTRA
                or _is_a_judgement_phrase(words)):
            continue
        if name and words[0].lower() == name.lower():
            continue
        if words[0][:1].isupper() and len(words) == 1:
            continue
        if re.match(r"\s*\d", text[match.end(match.lastindex or 1):]):
            continue
        if words[0].lower() in ("bit", "little", "lot", "couple", "few"):
            continue
        if words[0].lower() in ("my", "our", "his", "her", "their", "your"):
            continue
        if words[0].lower() in SELF_JUDGEMENT:
            continue
        job = _the_role(words)
        if match.re is JOB_AS_A and not was_working:
            article = re.search(r"\bas\s+(an?)\b", match.group(0), re.I)
            frame = "as " + (article.group(1).lower() if article else "a")
        elif match.re is JOB_WAS:
            frame = "was"
        elif was_working and not (groups[0] or "").strip():
            frame = "work"
        elif was_working and (groups[0] or "").lower() in JOB_FRAME | JOB_GOT_FRAME:
            frame = " ".join(part.strip() for part in groups[:2] if part and part.strip())
            if (match.re is JOB_GOT_AT and len(frame.split()) == 1
                    and job.lower() in JOB_GOT_AN_EMPLOYER):
                frame += " a"
        break
    return job, city, frame


def place_value(phrase):
    words = str(phrase or "").split()
    if len(words) > 1 and words[0].lower() not in PLACE_MIDDLE:
        return ""
    return _place_name(phrase)
TAKES_ONE_BACK = frozenset(("not", "rather", "instead"))


I_DRIVE = re.compile(r"\bi (?:drive|drives|driving)\s+(?P<art>a |an |my |the )?"
                     r"(?P<what>[a-z0-9][\w'-]*(?: [a-z0-9][\w'-]*)?)", re.I)
NOT_A_CAR = frozenset("""
about across along around away back badly bargain bike bikes carefully car cars everywhere far
fast for from hard home in into like lorries lorry lots lot me message miles mine motorbike
motorbikes myself nail nowhere off on out point safely slowly somewhere stake that them there
these this those to too truck trucks up us van vans vehicle very wedge work
""".split())
MEASURED = frozenset("miles mile km kms kilometres kilometers hours hour mins minutes day week".split())
CAR_ASKED = re.compile(r"\b(?:do|does|did|should|can|could|would|will|have|has)\s+i\s+drive\b"
                       r"|\bdrive\s+a\b[^?.!]*\?", re.I)
CAR_NAMED = re.compile(
    r"\b(?:its|it's|it is)\s+(?:a|an)\s+(?:(?:19|20)\d\d\s+)?(?P<what>[a-z][\w'-]*(?:\s+[a-z][\w'-]*)?)"
    r"|\bmy\s+(?P<mine>[a-z][\w'-]*(?:\s+[a-z][\w'-]*)?)", re.I)
_CAR_NAMES = []


def _the_car_name_in(phrase):
    if not _CAR_NAMES:
        from ..knowledge.cars import MODELS
        _CAR_NAMES.extend(sorted(set(MODELS), key=len, reverse=True))
    flat = " ".join(str(phrase or "").replace("'", "").lower().split())
    for name in _CAR_NAMES:
        if flat == name or flat.startswith(name + " "):
            return name
    return ""


CAR_IN_THE_PAST = re.compile(
    r"\b(?:used to|used it|sold|selling|sale|wrote off|written off|scrapped|traded in|part "
    r"exchanged|had|old|previous|previously|before|last car|first car|was|were|years ago)\b", re.I)


def _car_named_in_passing(text):
    past = bool(CAR_IN_THE_PAST.search(text))
    for match in CAR_NAMED.finditer(text):
        mine = match.group("mine")
        if mine and past:
            continue
        name = _the_car_name_in(match.group("what") or mine)
        if name:
            return name
    return None


def _car(text):
    if CAR_ASKED.search(text):
        return None
    for match in I_DRIVE.finditer(text):
        phrase = _finish(match.group("what"))
        article = (match.group("art") or "").strip().lower()
        for tail in TONE_TAIL:
            if phrase.endswith(" " + tail):
                phrase = phrase[: -len(tail)].strip()
        words = phrase.split()
        while words and words[0].isdigit():
            words = words[1:]
        phrase = " ".join(words)
        if not words:
            continue
        if any(word in NOT_A_CAR for word in words) or words[-1] in MEASURED:
            continue
        if not article and words[-1].endswith("s"):
            continue
        return phrase
    return _car_named_in_passing(text)
ADJECTIVE_NAMING = frozenset("new".split())


def _reads_as_a_plural(name_word, first):
    word = str(name_word or "").lower()
    return first in ADJECTIVE_NAMING and word.endswith("s") and not word.endswith("ss")


NOT_A_PLACE_WORD = frozenset("""fine good great ok okay alright lovely rubbish awful terrible
brilliant perfect amazing wonderful horrible disgusting cancelled canceled booked sorted done
shut closed busy quiet cheap expensive pointless useless worthwhile""".split())


def _place_name(phrase):
    words = str(phrase or "").replace("-", " - ").split()
    the = ""
    if len(words) > 1 and words[0].lower() == "the" and words[1].lower() in COUNTRY_ARTICLE:
        the, words = "the ", words[1:]
    kept = []
    for i, word in enumerate(words):
        if the:
            kept.append(word)
            break
        low = word.lower()
        if i == 0 and len(words) > 1 and low in PLACE_MIDDLE:
            if words[1].lower() in DETERMINERS:
                return ""
            if _an_everyday_word(words[1]) or _reads_as_a_plural(words[1], low):
                return ""
            kept.append(word)
            continue
        if (low in HOME_STOP or low in NOT_PLACES or low in PLACE_VERBS or low.endswith("ly")
                or low in TAKES_ONE_BACK or low in NOT_A_PLACE_WORD or word == "-"):
            break
        kept.append(word)
    if not kept:
        return ""
    if len(kept) == 1 and kept[0].lower() in PLACE_MIDDLE:
        return ""
    name = " ".join(kept)
    if len(kept) == 1 and name.lower() in COUNTRY_CAPS:
        return the + COUNTRY_CAPS[name.lower()]
    return the + " ".join(w[:1].upper() + w[1:] if w.islower() else w for w in name.split())


def _born_place(text):
    born = []
    for pattern in (FROM_PLACE, FROM_GROWN):
        for match in pattern.finditer(text):
            if not re.search(r"\bborn\b", match.group(0), re.I):
                continue
            name = _place_name(match.group(1))
            if name:
                born.append((match.start(), name))
    return max(born)[1] if born else None


FROM_A_MOVE = re.compile(
    r"\b(?:moved|moves|moving|relocated|relocating|relocate|migrated)\b[^.;!?]{0,40}?"
    r"\bfrom\s+([A-Za-z][A-Za-z'-]{1,}(?:[ -][A-Za-z][A-Za-z'-]{1,})?)\b", re.I)


A_MOVE_FROM_THEN_TO = re.compile(
    r"\b(?:moved|moves|moving|relocated|relocating|relocate|migrated)\s+from\s+"
    r"[A-Za-z][A-Za-z'-]{1,}(?:[ -][A-Za-z][A-Za-z'-]{1,})?\s+"
    r"(?:to|into)\s+"
    r"(?P<place>[A-Za-z][A-Za-z'-]{1,}(?:[ -][A-Za-z][A-Za-z'-]{1,})?)\b", re.I)


def _the_person_moved(before):
    clause = re.split(r"[.;!?,]|\band\b|\bbut\b|\bso\b", str(before or ""))[-1]
    return bool(re.match(r"\s*(?:i|im|i'm|ive|i've|id|we|were|we're|weve|we've|we'd)\b",
                         clause, re.I))


def _from_place(text):
    born = []
    said = []
    for pattern in (FROM_PLACE, FROM_MORE, FROM_GROWN, FROM_A_MOVE):
        for match in pattern.finditer(text):
            if pattern is FROM_A_MOVE and not _the_person_moved(text[:match.start()]):
                continue
            phrase = match.group(1)
            if pattern is FROM_GROWN and not _grown_up_in_a_place(phrase, text):
                continue
            name = _place_name(phrase)
            if not name:
                continue
            if re.search(r"\bborn\s+in\b", match.group(0), re.I):
                born.append((match.start(), name))
            else:
                said.append((match.start(), name))
    if said:
        return max(said)[1]
    if not born:
        return None
    return max(born)[1]


A_HOME_BEFORE = re.compile(
    r"\b(?:a|an|the|my|our|their|his|her|this|that)\s+[a-z][a-z'-]*"
    r"(?:\s+[a-z][a-z'-]*){0,2}\s+(?:near|outside|round|close to|next to|by)\s+$", re.I)


def _places(text):
    places = []
    home = None
    home_said = ""
    for pattern in (HOME_DWELL, HOME_PLACE):
        for match in pattern.finditer(text):
            word = _place_name(match.group("place"))
            if not word:
                continue
            if not any(word.lower() == p.lower() for p in places):
                places.append(word)
            ahead = match.group("planned") and FUTURE.search(text)
            if home is None and not match.group("stay") and not ahead:
                home = word
                said_with = A_HOME_BEFORE.search(text[:match.start("place")])
                if said_with:
                    home_said = " ".join(said_with.group(0).split()) + " " + word
            break
        if home:
            break
    if home is None:
        for match in A_MOVE_FROM_THEN_TO.finditer(text):
            if not _the_person_moved(text[:match.start()]):
                continue
            word = _place_name(match.group("place"))
            if not word:
                continue
            if not any(word.lower() == p.lower() for p in places):
                places.append(word)
            if not FUTURE.search(text):
                home = word
            break
    for match in PLACE_AFTER.finditer(text):
        word = match.group(1)
        first = word.split()[0].lower()
        if first in NOT_PLACES or word.lower() in NOT_PLACES:
            continue
        if first in PLACE_MIDDLE:
            pair = " ".join(text[match.start(1):].split()[:2])
            word = _place_name(pair)
            if not word:
                continue
        if word not in places:
            places.append(word)
    for match in PLACE_LOWER_NAMED.finditer(text):
        if _an_everyday_word(match.group(2)):
            continue
        word = _place_name(match.group(1) + " " + match.group(2))
        if word and not any(word.lower() == p.lower() for p in places):
            places.append(word)
    for match in PLACE_LOWER.finditer(text):
        word = _finish(match.group(1))
        low = word.lower()
        if not word or low in NOT_PLACES or low in PLACE_VERBS:
            continue
        if low in PLACE_MIDDLE:
            continue
        if word[:1].isupper() and word in places:
            continue
        if any(p.lower().startswith(low + " ") for p in places):
            continue
        if not any(word.lower() == p.lower() for p in places):
            places.append(word[:1].upper() + word[1:])
    if not places and SHORT_LIST.match(text.strip()):
        for word in re.findall(r"[A-Z][a-z]+", text):
            if word.lower() not in NOT_PLACES and word not in places:
                places.append(word)
    return places, home, home_said


_QUANTITY_WORDS = frozenset("""enough much many any more less too little lots plenty loads
loads""".split())
ALLERGY_STOP = frozenset("""i we he she they it you have has had got also but so because
which and the a an my our his her their anything something everything much many most
lot food stuff no not few several some any real bad serious""".split())


OTHER_NOUNS = ("son", "daughter", "child", "children", "kid", "baby", "girl", "boy",
               "youngest", "eldest", "oldest", "husband", "wife",
               "partner",
               "boyfriend", "girlfriend", "fiance", "fiancee", "mum", "mom", "mother",
               "stepmum", "stepdad", "dad", "father", "sister", "brother", "friend",
               "mate", "colleague", "coworker", "boss", "flatmate", "housemate",
               "nephew", "niece", "grandma", "grandad", "granny", "nana", "grandpa",
               "aunt", "uncle", "cousin", "neighbour", "neighbor", "dog", "cat", "pet")
OTHER_NOUNS = OTHER_NOUNS + tuple(sorted((word for word in RELATIONS
                                          if word not in OTHER_NOUNS), key=len, reverse=True)) \
    + ("twin",)

CLAUSE_BREAK = re.compile(r"[.!?;]|\b(?:but|so|because|which|although|though|while)\b", re.I)
QUESTION_OPEN = re.compile(
    r"^(?:(?:and|but|so|then|also|oh|ok|okay|well|now|hey|sorry|please|quick|hi)\s+)*"
    r"(?:is|isnt|are|arent|was|wasnt|were|werent|am|do|dont|does|doesnt|did|didnt|has|hasnt|"
    r"have|havent|had|can|cant|could|couldnt|would|wouldnt|will|wont|shall|should|shouldnt)\b",
    re.I)
CLAUSE_JOIN = re.compile(r"\b(?:if|because|since|though|although|when|whenever|and|but|so)\b|[,;]",
                         re.I)


def stated_not_asked(text):
    said = " ".join(str(text or "").strip().split())
    if not said or not QUESTION_OPEN.match(said):
        return said
    kept = [part.strip(" ,.;:!?") for part in CLAUSE_JOIN.split(said)]
    kept = [part for part in kept if part and not QUESTION_OPEN.match(part)]
    return ", ".join(kept)

PRONOUN_SUBJECT = re.compile(r"\b(?P<pron>he|she|they|him|them|hes|shes|theyre|her)\b", re.I)

SUBJECT = re.compile(
    r"\b(?:my|our|his|her|their|the)\s+" + MODIFIER_BEFORE + r"(?P<rel>"
    + "|".join(OTHER_NOUNS) + r")"
    r"(?P<inlaw>\s+in\s+laws?)?s?\b"
    r"|\b(?P<pron>he|she|they|him|them|his|their|hes|shes|theyre|theyve)\b"
    r"|\b(?P<her>her)\b"
    r"|\b(?P<user>i'm|im|i am|i've|ive|i|me|mine|my|my own|we're|we are|we've|we|us|our)\b",
    re.I)


A_ME_WITH_SOMEONE = re.compile(
    r"\b(?:me|us|we|i)\b[^.!?]{0,24}\b(?:and|,|&)\b[^.!?]{0,24}\b(?:my|our)\s+\w+"
    r"|\b(?:my|our)\s+\w+[^.!?]{0,24}\b(?:and|,|&)\b[^.!?]{0,12}\b(?:me|us|i)\b", re.I)


def _the_person_is_in_it(clause):
    return bool(A_ME_WITH_SOMEONE.search(clause))


def subject(text, pos):
    start = 0
    for match in CLAUSE_BREAK.finditer(text, 0, pos):
        start = match.end()
    clause = text[start:pos]
    kind, who = "", ""
    for match in SUBJECT.finditer(clause):
        if match.group("rel"):
            kind = "other"
            who = " ".join((match.group("rel") + (match.group("inlaw") or "")).split()).lower()
            who = SPOKEN_RELATION.get(who, who)
        elif match.group("pron") or match.group("her"):
            kind, who = "other", ""
        else:
            kind, who = "user", ""
    if kind == "other" and who and _the_person_is_in_it(clause):
        kind = "user"
    if kind == "other" and who:
        pair = a_chained_person(clause)
        if pair and pair.split("'s ")[0] == who:
            who = pair
    if kind == "":
        bare_who, bare_name = _the_person_without_a_relation(clause)
        if bare_who or bare_name:
            kind, who = "other", bare_who
            pair = a_chained_person(clause)
            if pair and pair.split("'s ")[0] == who:
                who = pair
    return kind, who


BARE_RELATION = re.compile(
    r"\b(?P<rel>" + "|".join(sorted(OTHER_NOUNS, key=len, reverse=True)) + r")"
    r"(?P<inlaw>\s+in\s+laws?)?s?$", re.I)
NOT_A_PERSON_WORD = frozenset("""
and but so then also oh ok okay well now anyway actually quick just plus hey hi sorry right yeah yes
today tonight tomorrow yesterday here there this that these those it its he she they them their his
her him i im ive me my mine we us our ours you your yours who what which the a an some any no not
dont doesnt didnt is are was were be been am do does did have has had can could would should will
shall may might must of to for from in on at by with about time day week month year morning
evening night thing things something anything nothing everything someone anyone everyone nobody
help thanks please get got go going come coming done""".split())


BETWEEN_PERSON_AND_FACT = frozenset("""
is are was were be been being am has have had isnt arent wasnt werent hasnt havent hadnt
s does do did doesnt dont didnt can cant cannot could couldnt may might must shall should
shouldnt will wont would wouldnt get gets got become becomes became
""".split())
NOT_A_BARE_PERSON_AHEAD = frozenset("""
my our his her their your its the a an this that these those some any every no each
""".split())
A_PRONOUN_NOT_A_NAME = frozenset("""
im ive id ill ima youve youre youd youll hes shes its itd its were weve wed well theyre theyve
theyd theyll thats whats theres heres isnt arent wasnt werent hasnt havent hadnt doesnt dont didnt
cant couldnt wouldnt shouldnt wont mustnt aint lets
""".split())


def _a_person_word(word):
    return str(word or "").strip().strip(".,!?;:\"'").lower().replace("\u2019", "'").replace("'", "")


def _the_person_without_a_relation(clause):
    words = [word.strip(" ,.;:!?").strip("'") for word in clause.split()]
    words = [word for word in words if word]
    while words and words[0].lower() in ("and", "but", "so", "then", "also", "oh",
                                        "ok", "okay", "well", "now", "btw"):
        words.pop(0)
    while words and words[-1].lower() in BETWEEN_PERSON_AND_FACT:
        words.pop()
    if not words or len(words) > 3:
        return "", ""
    if any(word.lower() in NOT_A_BARE_PERSON_AHEAD for word in words[:-1]) \
            or words[-1].lower() in NOT_A_BARE_PERSON_AHEAD:
        return "", ""
    said = " ".join(words)
    found = BARE_RELATION.search(said)
    if found:
        who = found.group("rel") + (found.group("inlaw") or "")
        who = " ".join(who.lower().split())
        if who.endswith("s") and who[:-1] in RELATIONS:
            who = who[:-1]
        return SPOKEN_RELATION.get(who, who), ""
    if len(words) == 1:
        word = words[0]
        if _a_person_word(word) in NOT_A_PERSON_WORD or _a_person_word(word) in DIET_GROUP \
                or _a_person_word(word) in RELATIONS or _a_person_word(word) in A_PRONOUN_NOT_A_NAME:
            return "", ""
        if _may_be_a_name(word) and _name_after_a_title(word):
            return "", word
    return "", ""


FILLER_TAIL = frozenset(TAIL_OFF | frozenset("""please again then now though either too also
still yet anyway plus thanks thank sorry ok okay""".split()))


FILLER_TAIL_PHRASES = ("at all", "any more", "anymore", "these days", "whatsoever", "at least",
                       "any longer", "no more", "for years", "since i was little")


def _trim_filler(text):
    words = text.split()
    while True:
        while words and words[-1].strip(".,!?;:'\"").lower() in FILLER_TAIL:
            words.pop()
        tail = " ".join(words[-3:]).strip(".,!?;:'\"").lower()
        cut = next((phrase for phrase in FILLER_TAIL_PHRASES
                    if tail.endswith(phrase)), None)
        if not cut:
            break
        words = " ".join(words).strip(".,!?;:'\"")[:-len(cut)].split()
    return " ".join(words)


QUESTION_START = re.compile(r"^(?:what|which|who|how|when|where|why|can|could|should|would|"
                            r"will|shall|do|does|did|is|are|was|were|any|if)\b")


NOT_A_FOOD = frozenset("""much many more anything everything nothing something all at properly
enough food stuff lot any now yet still anymore here there""".split())

A_GENERIC_FOOD = frozenset("""food foods stuff things thing""".split())

def _trim_time_tail(item):
    words = item.split()
    while len(words) > 1:
        last = words[-1].strip(".,!?;:'\"")
        if last in NOT_A_FOOD_IN_IT or last.isdigit() or last in ("the", "a", "my", "our"):
            words.pop()
        else:
            break
    return " ".join(words)


NOT_A_FOOD_IN_IT = frozenset("""at in on before after during while when whenever until till
    by from around late early night nights morning mornings afternoon evenings evening
    midnight lunchtime bedtime work school desk shift commute""".split())


def _a_modifier_before_a_generic_noun(words):
    if len(words) < 2:
        return False
    if words[-1].strip(".,!?;:'\"").lower() not in A_GENERIC_FOOD:
        return False
    return not set(words[:-1]) & ALLERGY_STOP


def _only_stop_words(item):
    words = item.split()
    return bool(words) and all(word in NOT_A_FOOD or word in ALLERGY_STOP for word in words)


def _allergy_items(chunk):
    items = []
    chunk = re.split(r"\bnot\b|\b(?:but|so|because|which)\b", chunk)[0]
    for item in re.split(r",| and ", chunk):
        item = _trim_time_tail(_trim_filler(_finish(item)))
        if QUESTION_START.match(item.lower()):
            break
        if not item or len(item) < 2:
            continue
        if (set(item.split()) & ALLERGY_STOP
                and not _a_modifier_before_a_generic_noun(item.split())):
            continue
        if item in ("it", "them", "that", "this") or item in items:
            continue
        if (set(item.split()) & NOT_A_FOOD_IN_IT
                and not set(item.split()) & ONE_MORE_FOODS):
            continue
        if _only_stop_words(item):
            continue
        items.append(item)
    return items


ONE_MORE_DETERMINERS = frozenset("""the a an my your his her their our this that these those some""".split())
NOT_AN_ADDITION = frozenset("""not no dont don't didnt didn't doesnt doesn't scratch forget never
    nor without""".split())


def one_more(text):
    said = " ".join(str(text or "").lower().split())
    if not said:
        return []
    typed = said
    for _ in range(6):
        before = said
        said = ONE_MORE_HEAD.sub("", said).strip(" ,")
        said = ONE_MORE_TAIL.sub("", said).strip(" ,.!?")
        if said == before:
            break
    if not said or said == typed:
        return []
    items = []
    for part in re.split(r",| and | or ", said):
        words = [word.strip("'\u2019") for word in part.split() if word.strip("'\u2019")]
        if words and words[0].lower() in NOT_AN_ADDITION:
            continue
        while words and words[0] in ONE_MORE_DETERMINERS:
            words = words[1:]
        if not words or len(words) > 2:
            continue
        if words[-1] not in ONE_MORE_FOODS:
            continue
        head, last = " ".join(words[:-1]), ALLERGEN_PLURALS.get(words[-1], words[-1])
        item = (head + " " + last).strip()
        if item not in items:
            items.append(item)
    return items


SHARE_LEAD = r"(?:(?:oh|yeah|yes|and|haha|honestly|sorry|actually)[\s,]+)*"
I_SHARE_IT = re.compile(
    r"^\W*" + SHARE_LEAD + r"(?:"
    r"im|i'm|i am|me|i"
    r")\s*(?:"
    r"too|also|as well|aswell|the same|same|not alone|"
    r"have (?:it|that|this|the same)(?: too| as well)?|"
    r"do too|am too|"
    r"dont either|don't either|cant either|can't either|couldnt either|couldn't either|"
    r"havent either|haven't either|can too|could too|do as well|am as well"
    r")\W*$", re.I)
I_SHARE_IT_SHORT = re.compile(
    r"^\W*" + SHARE_LEAD + r"(?:"
    r"same here|same for me|same for us|same|same as (?:me|him|her|them|that|my [a-z]+)|me neither|"
    r"likewise|"
    r"(?:that'?s|this is) me(?: too| as well)?|"
    r"so (?:am|do|does|did|have|has|can|could|would) i|"
    r"neither (?:am|do|does|did|have|has|can|could) i|nor (?:am|do|have|can) i"
    r")\W*$", re.I)
SOMEONE_SHARES_IT_VERB_FIRST = re.compile(
    r"^\W*" + SHARE_LEAD + r"(?:so|neither|nor)\s+"
    r"(?:does|do|is|are|has|have|can|could|would)\s+(?:my|our)\s+(?P<who>[a-z][a-z'-]{1,14})\W*$",
    re.I)
SOMEONE_SHARES_IT = re.compile(
    r"^\W*" + SHARE_LEAD + r"(?:my|our)\s+(?P<who>[a-z][a-z'-]{1,14})\s+"
    r"(?:is|are|does|do|has|have|gets|got|wants)?\s*(?:too|also|as well|aswell|the same|same|"
    r"it too|that too|one too)\W*$", re.I)
SOMEONE_SHARES_IT_PRONOUN = re.compile(
    r"^\W*" + SHARE_LEAD + r"(?:he|she|they)\s+"
    r"(?:is|are|does|do|has|have)?\s*(?:too|also|as well|aswell|the same|same|it too|that too)\W*$",
    re.I)
LAST_PERSON = "@last"


def the_limit_they_share(text):
    said = " ".join(str(text or "").lower().split()).strip(" !.,")
    if not said or len(said.split()) > 6:
        return ""
    if I_SHARE_IT.match(said) or I_SHARE_IT_SHORT.match(said):
        return "i"
    found = SOMEONE_SHARES_IT.match(said) or SOMEONE_SHARES_IT_VERB_FIRST.match(said)
    if found:
        who = found.group("who").strip()
        return "" if who in ("own", "self") else who
    if SOMEONE_SHARES_IT_PRONOUN.match(said):
        return LAST_PERSON
    return ""


def denied_before(text, start):
    return bool(DENIAL_WORDS.search(str(text or "")[max(0, start - 40):start]))


def _clause(text, start):
    head = text[:start]
    cut = 0
    for edge in CLAUSE_EDGE.finditer(head):
        cut = edge.end()
    return head[cut:]


def _the_clause_before(text, start, edges=4):
    parts, last = [], 0
    head = text[:start]
    for edge in CLAUSE_EDGE.finditer(head):
        parts.append(head[last:edge.end()])
        last = edge.end()
    parts.append(head[last:])
    said, walked = parts[-1], 0
    while (walked + 1 < len(parts) and walked < edges
           and not _opens_a_subject(parts[-1 - walked])):
        walked += 1
        said = parts[-1 - walked] + said
    return said


def _opens_a_subject(clause):
    words = str(clause or "").replace(",", " ").split()
    if not words:
        return False
    return re.sub(r"[^a-z']", "", words[0].lower()) in ANY_SUBJECT


def _around(text, start):
    left = 0
    for edge in CLAUSE_EDGE.finditer(text[:start]):
        left = edge.end()
    right = len(text)
    edge = CLAUSE_EDGE.search(text, start)
    if edge:
        right = edge.start()
    return text[left:right]


def _own_named(text, start, own):
    found = []
    lowered = text.lower()
    for pet in own or []:
        name = str((pet or {}).get("name") or "").strip().lower()
        animal = str((pet or {}).get("animal") or "").strip().lower()
        if not name or not animal or len(name) < 3:
            continue
        match = re.search(r"\b" + re.escape(name) + r"\b", lowered[:start])
        if match:
            found.append(animal)
    return list(dict.fromkeys(found))


def _own_in_denial(text, own):
    gone = []
    for pet in own or []:
        name = str((pet or {}).get("name") or "").strip()
        animal = str((pet or {}).get("animal") or "").strip().lower()
        if not name or not animal or len(name) < 3:
            continue
        for match in re.finditer(r"\b" + re.escape(name) + r"\b", str(text or ""), re.I):
            if not_had(text, match.start()):
                if pet not in gone:
                    gone.append(dict(pet))
                break
    return gone


ONE_TAKEN = re.compile(r"\b(?:gave|give|giving|given|gives|rehom(?:e|ed|es|ing)|took|taken|sold|"
                       r"got rid of|went to|passed (?:away|on)|died|lost|left)\b", re.I)
DIY_OF_ALL = re.compile(r"\bone\s+of\s", re.I)
ONE_OF_THEM = re.compile(r"\b(?:one|1)\s+of\s+(?:them|those|the\s+\w+s|our\s+\w+s|my\s+\w+s)\b|"
                         r"\b(?:gave|give|giving|given|rehom(?:e|ed|es|ing)|took|taken|got rid of)\b"
                         r"[^.;!?]{0,20}?\bone\b", re.I)


def given_away_one(text, own=None):
    said = str(text or "")
    if not ONE_OF_THEM.search(said) or not ONE_TAKEN.search(said):
        return []
    kinds = {}
    for pet in own or []:
        if not isinstance(pet, dict):
            continue
        animal = str(pet.get("animal") or "").strip().lower()
        if not animal or (pet.get("count") or 1) < 2:
            continue
        kinds.setdefault(animal, pet)
    if len(kinds) != 1:
        return []
    return [dict(next(iter(kinds.values())))]


def _pointed_at(text, start, plural):
    named = [match.group(1).lower() for match in PETS.finditer(text[:start])]
    named = list(dict.fromkeys(named))
    if not named:
        return []
    return named if plural else named[-1:]


def not_had(text, start):
    clause = _clause(text, start)
    if HEDGE.search(clause):
        return False
    if (NOT_HAVE_LONGER.search(clause) or _have_none(clause + " " + text[start:])
            or WITHOUT_ANIMAL.search(clause)
            or NOT_JUST.search(clause) or taken_back_before(text, start)):
        return True
    return any(match.start() <= start <= match.end() for match in GIVEN_AWAY.finditer(text))


def _have_none(clause):
    for match in HAVE_NONE.finditer(clause):
        if A_COMPOUND_AFTER.match(clause[match.end():]):
            continue
        return True
    return False


def taken_back_before(text, start):
    said = str(text or "")
    clause = _clause(said, start)
    if HEDGE.search(clause):
        return False
    if TAKEN_BACK_BEFORE.search(clause):
        return True
    animal = PETS.match(said, start)
    rest = said[animal.end():] if animal else said[start:]
    if NO_THEN_A_THING.match(clause):
        return False
    return bool(BARE_NO.match(clause)) and not rest.strip(" .,!?;:")


def denials(text, own=None):
    said = str(text or "")
    denied = {}
    for match in ALLERGY.finditer(said):
        if not denied_before(said, match.start()):
            continue
        kind, who = subject(said, match.start())
        if kind != "other":
            continue
        person = _a_person(said, match.end(), who)
        items = [ALLERGEN_PLURALS.get(item, item) for item in _allergy_items(match.group(1))]
        if not person or not items:
            continue
        entry = next((seen for seen in denied.setdefault("theirs", [])
                      if _same_person(seen, person)), None)
        if entry is None:
            entry = dict(person, allergies=[])
            denied["theirs"].append(entry)
        entry["allergies"].extend(item for item in items if item not in entry["allergies"])
    for match in CONTRAST.finditer(said):
        items = _allergy_items(match.group("old"))
        for item in items:
            name = ALLERGEN_PLURALS.get(item, item)
            if name not in denied.setdefault("allergies", []):
                denied["allergies"].append(name)
    for match in DENIAL_OF.finditer(said):
        if match.group("food"):
            items = _allergy_items(re.sub(r"^allergic to\s+", "", match.group("food"), flags=re.I))
            if items:
                denied.setdefault("allergies", []).extend(
                    item for item in items if item not in denied.get("allergies", []))
            continue
        if match.group("condition"):
            denied["condition"] = match.group("condition").lower()
            continue
        if match.group("diet"):
            denied["diet"] = DIET_NAMES.get(match.group("diet").lower(), match.group("diet").lower())
    for match in DIET_OFF.finditer(said):
        plan = next((match.group(name) for name in ("plan", "off", "gone", "quit")
                     if match.group(name)), "")
        if not plan:
            continue
        plan = "-".join(plan.lower().replace("-", " ").split())
        denied["diet"] = DIET_NAMES.get(plan, "on a diet" if plan.startswith("diet") else plan)
    for match in DIET_BACK.finditer(said):
        food = _the_food_named(match.group("back") or match.group("eat") or "")
        if food:
            denied["diet"] = food
    if NO_PETS.search(said):
        denied["pets"] = [EVERYTHING]
    animals = []
    others = _someone_elses(said)
    for match in PETS.finditer(said):
        if not not_had(said, match.start()):
            continue
        if any(start <= match.start() < stop for start, stop in others):
            continue
        animal = match.group(1).lower()
        if animal not in animals:
            animals.append(animal)
    if not animals:
        for match in PET_PRONOUN.finditer(said):
            if not not_had(said, match.start()):
                continue
            pointed = _the_one_they_have(said, match, own)
            if not pointed and not _names_a_relative(said):
                pointed = _only_pet(own)
            for animal in pointed:
                if animal not in animals:
                    animals.append(animal)
            break
    if not animals:
        animals = _own_in_denial(said, own)
    if animals and denied.get("pets") != [EVERYTHING]:
        denied["pets"] = _merge_pets(denied.get("pets", []), _one_of_several(animals, said, own))
    return denied


def their_back(text):
    said = str(text or "")
    marked = bool(A_CORRECTION.search(said))
    found = []
    for match in THEIR_BACK.finditer(said):
        if not marked and not match.group("emph"):
            continue
        if A_NEGATOR_IN_BETWEEN.search(match.group("gap") or ""):
            continue
        verb = (match.group("emph") or match.group("verb") or "").lower()
        if not verb:
            continue
        kind = "diet" if verb.startswith("eat") or verb in ("does", "do", "did") else "taste"
        food = " ".join((match.group("food") or "").lower().split())
        if not food:
            continue
        subj = " ".join((match.group("subj") or "").lower().split())
        named = subj.startswith(("my ", "his ", "her ", "their ", "our "))
        found.append({"who": subj.split()[-1] if named else "",
                      "pronoun": "" if named else subj,
                      "kind": kind, "food": food})
    return found


ALL_OF_THEM = re.compile(r"\b(?:both|all|the\s+\w+s|my\s+\w+s|our\s+\w+s)\b", re.I)


def _one_of_several(animals, said, own):
    one_of = bool(ONE_OF_THEM.search(said))
    whole = bool(ALL_OF_THEM.search(said)
                 or re.search(r"\b(?:them|those|these)\b", said, re.I)) and not one_of
    out = []
    for animal in animals:
        if not isinstance(animal, str):
            out.append(animal)
            continue
        same = [pet for pet in (own or []) if isinstance(pet, dict)
                and str(pet.get("animal") or "").strip().lower() == animal]
        held = sum(int(pet.get("count") or 1) for pet in same)
        plural = whole or (bool(re.search(r"\b" + re.escape(animal) + r"s\b", said, re.I))
                           and not one_of)
        if held > 1 and not plural:
            out.append(dict(same[-1]))
        else:
            out.append(animal)
    return out


def _merge_pets(had, more):
    out = list(had or [])
    words = {str(item).strip().lower() for item in out if not isinstance(item, dict)}
    records = [item for item in out if isinstance(item, dict)]
    for item in more or []:
        if isinstance(item, dict):
            if item not in records:
                records.append(item)
        elif str(item).strip().lower() not in words:
            words.add(str(item).strip().lower())
            out.append(item)
    return [item for item in out if not isinstance(item, dict)] and (
        [item for item in out if not isinstance(item, dict)] + records) or records


def _the_one_they_have(said, match, own):
    return (_pointed_at(said, match.start(), match.group("pron").lower() in PLURAL_PRONOUN)
            or _own_named(said, match.start(), own) or [])


def _only_pet(own):
    held = [str((pet or {}).get("animal") or "").strip().lower() for pet in (own or [])]
    held = [animal for animal in dict.fromkeys(held) if animal]
    return held if len(held) == 1 else []


def _names_a_relative(said):
    return any(re.search(r"\b" + word + r"\b", said, re.I) for word in RELATIONS)


def _may_be_an_animal(said, match, own=None, said_before=None):
    if match.group("pron").lower() in ("it", "them", "those", "they"):
        return True
    if _names_a_relative(said) or PEOPLE_WORD.search(said):
        return False
    if ANIMAL_DEATH.search(_around(said, match.start())):
        return True
    before = str(said_before or "")
    if not before or PEOPLE_WORD.search(before) or not PETS.search(before):
        return False
    return bool(_only_pet(own))


def losses(text, own=None, said_before=None):
    said = str(text or "")
    if not DIED.search(said):
        return []
    animals = []
    others = _someone_elses(said)
    for match in PETS.finditer(said):
        if not DIED.search(_around(said, match.start())):
            continue
        if any(start <= match.start() < stop for start, stop in others):
            continue
        if _not_their_animal(said, match.start(), match.end()):
            continue
        animal = match.group(1).lower()
        if animal not in animals:
            animals.append(animal)
    if not animals:
        for match in PET_PRONOUN.finditer(said):
            if not DIED.search(_around(said, match.start())):
                continue
            pointed = _the_one_they_have(said, match, own)
            if not pointed and _may_be_an_animal(said, match, own, said_before):
                pointed = _only_pet(own)
            for animal in pointed:
                if animal not in animals:
                    animals.append(animal)
            break
    if not animals and own:
        for pet in own:
            name = str((pet or {}).get("name") or "").strip().lower()
            animal = str((pet or {}).get("animal") or "").strip().lower()
            if not animal:
                continue
            for match in DIED.finditer(said):
                if HEDGE.search(_clause(said, match.start())):
                    continue
                if name and len(name) >= 3 and re.search(r"\b" + re.escape(name) + r"\b",
                                                         said.lower()):
                    if animal not in animals:
                        animals.append(animal)
    return animals


def _allergies(text):
    mine, others = [], []
    for pattern in (ALLERGY, CANNOT_EAT, X_ALLERGY):
        for match in pattern.finditer(text):
            if pattern is not CANNOT_EAT and denied_before(text, match.start()):
                continue
            if pattern is X_ALLERGY and match.group(1).lower() in NOT_AN_ALLERGEN:
                continue
            items = _allergy_items(match.group(1))
            if not items:
                continue
            if pattern is X_ALLERGY:
                items = [ALLERGEN_PLURALS.get(item, item) for item in items]
            kind, who = subject(text, match.start())
            if kind != "other":
                mine.extend(item for item in items if item not in mine)
                continue
            person = _a_person(text, match.end(), who)
            if not person:
                continue
            entry = next((seen for seen in others if _same_person(seen, person)), None)
            if entry is None:
                entry = dict(person, allergies=[])
                others.append(entry)
            entry["allergies"].extend(item for item in items if item not in entry["allergies"])
    return mine, others


AGE_MONTHS_TAIL = re.compile(r"^\s*months?(?:\s+old)?\b", re.I)

AGE_TAIL = re.compile(
    r"^\s*(?:$|[.,;:!?)]|\b(?:and|but|so|now|today|tomorrow|yesterday|too)\b"
    r"|\bgoing on \d{1,3}\b"
    r"|\bas well\b|\bthis year\b|\byears? old\b|\bold\b"
    r"|\bnext (?:week|month|year|spring|summer|autumn|winter|monday|tuesday|wednesday|"
    r"thursday|friday|saturday|sunday)\b|\b(?:in|on|by) [a-z]{3,9}\b)",
    re.I)


def _month_age_after(text, end):
    match = AGE_MONTHS_TAIL.match(text[end:])
    if not match:
        return False
    return bool(AGE_TAIL.match(text[end + match.end():]))


AGE_TO_COME = re.compile(r"\b(?:turns?|will be|is|are|'s|shes|hes|she's|he's|theyre|they're|"
                         r"who(?:['\u2019]?s)?)\s+"
                         r"(\d{1,3})\s+"
                         r"(next\s+(?:week|month|year|spring|summer|autumn|winter)|"
                         r"(?:in|on)\s+[a-z]{3,9})\b", re.I)


OTHER_CALLED = re.compile(r"\bmy\s+(?P<who>" + _RELATION_WORDS + r")s?\s+"
                          r"(?:(?:is|was|are)\s+)?(?:called|named)\s+" + _NAME, re.I)
OTHER_NAME_IS = re.compile(r"\bmy\s+(?P<who>" + _RELATION_WORDS + r")(?:'s|s'|s)?\s+name\s+"
                           r"(?:is|was)\s+" + _NAME, re.I)
OTHER_NAMED_BARE = re.compile(r"^\s*my\s+(?P<who>" + _RELATION_WORDS + r")s?\s+"
                              r"(?P<name>[A-Za-z][a-z'-]{1,19})\s*[.!]?$", re.I)
OTHER_BIRTHDAY = re.compile(
    r"\b(?:(?:my|our)\s+(?P<who>" + _RELATION_WORDS + r")s?|(?P<pronoun>his|her|their))\s+"
    r"(?:birthday|bday|dob|date of birth)\s*(?:'s|s)?\s*"
    r"(?:is|was|falls|:|=|on|in)\s+(?:on\s+)?(?:the\s+)?"
    r"(?P<date>[^,.;!?]{2,28})", re.I)
OTHER_NAMED_BEFORE_VERB = re.compile(
    r"\bmy\s+(?P<who>" + _RELATION_WORDS + r")\s+(?P<name>[a-z][a-z'-]{1,19})\s+"
    r"(?P<verb>[A-Za-z][a-z'-]{1,19})\b")


def _the_word_then_a_verb(name, following):
    name, following = (name or "").lower(), (following or "").lower()
    if not name or not following or name in VERB_FORMS:
        return False
    if following in VERB_FORMS:
        return True
    return len(following) > 3 and following.endswith("ed")


OTHER_NAMED_CAPITAL = re.compile(
    r"\bmy\s+(?P<who>" + _RELATION_WORDS + r")\s+(?P<name>[A-Z][a-z'-]{1,19})\b")
OTHER_NAME_POSSESSIVE = re.compile(
    r"\bmy\s+(?P<who>" + _RELATION_WORDS + r")\s+(?P<name>[A-Z][a-z]{1,19})(?:['\u2019]s?|"
    r"s(?=\s+[a-z]{3,19}\s+(?:is|are|was|were|will|has|have|had)\b))\b")
OTHER_NAMED_MIDLINE = re.compile(
    r"\bmy\s+(?P<who>" + _RELATION_WORDS + r")\s+"
    r"(?P<name>[A-Za-z][a-z'-]{1,19})\s+"
    r"(?P<verb>is|was|are|were|has|have|had|does|did|will|can|loves|hates|likes|needs|wants|"
    r"keeps|goes|works|plays|sleeps|eats|starts|started|turns|turned|says|said|misses|cries|"
    r"refuses|comes|came|gets|got|seems|looks|feels|takes|took|makes|made|buys|bought|"
    r"tells|told|struggles|wont|won't|cant|can't|doesnt|doesn't|isnt|isn't|didnt|didn't|"
    r"died|dies|passed|passes|lives|lived|moved|went|grew|became|married|left|arrived|retired|"
    r"finished)\b",
    re.I)
NOT_A_NAME_MIDLINE = frozenset("""
will would can could shall should may might must did does do dont doesnt didnt wont cant
shall always never often sometimes usually still really just also only suddenly already quite
rather very too more most less least better worse then than soon later yet ever once twice
she he they them we you it its this that there here i me him her his hers their
""".split())
NOT_A_NAME_THERE = frozenset("""
name names age birthday bday anniversary death funeral wake school teacher teachers class
homework reading exam exams job work shift shifts boss mood temper speech health weight diet
appetite sleep room bedroom car phone mobile laptop house flat garden leg legs arm arms back
head hand hands knee ankle shoulder eye eyes ear ears teeth tooth hair skin cough cold
temperature illness surgery appointment hospital care medication meds pills tablets inhaler
hearing eyesight memory bills rent money wages pension benefits passport visa wedding holiday
flight train bus ticket tickets booking order parcel present presents card
""".split())


def _may_be_a_name(word):
    low = word.lower()
    return (_looks_like_a_name(word) and low not in NOT_A_NAME_MIDLINE
            and low not in NOT_A_NAME_THERE)

NOT_NAME_ENDING = ("ing", "ed", "ly")
NAMES_THAT_END_LIKE_A_VERB = frozenset("""
lily holly molly polly sally kelly emily billy willy ted ned fred jed ed
""".split())


def a_titled_name(word):
    return bool(re.fullmatch(r"(?:" + TITLE + r")\s+[A-Za-z][A-Za-z'\-]{1,19}",
                             str(word or "").strip(), re.I))


def _looks_like_a_name(word):
    low = word.lower()
    if a_titled_name(word):
        return True
    if low.strip(".") in TITLE_WORDS:
        return False
    if not NAME_WORD.match(word) or low in NOT_A_NAME or low in RELATIONS:
        return False
    if is_a_contraction(low):
        return False
    if word[:1].isupper() or low in NAMES_THAT_END_LIKE_A_VERB:
        return True
    return not low.endswith(NOT_NAME_ENDING)


def _name_after_a_title(name):
    words = str(name or "").split()
    if not words:
        return False
    title = words[0].strip(".").lower()
    if title not in TITLE_WORDS:
        return True
    if len(words) == 1:
        return False
    rest = " ".join(words[1:]).lower()
    if rest in NAME_AFTER_TITLE:
        return True
    if rest in NOT_A_NAME or rest in NOT_NAMES or rest in NOT_NAMES_EXTRA \
            or rest in _A_WORD_FOR_A_PERSON:
        return False
    return not _not_a_name(rest, strict_ly=False)


def _the_name_without_a_possessive(text):
    stems = {}
    for match in OTHER_NAME_POSSESSIVE.finditer(text):
        raw = text[match.start("name"):match.end()]
        raw = str(raw).replace("\u2019", "'").lower()
        stem = match.group("name")
        if raw and stem:
            stems[raw] = stem
    return stems


def _a_relations_name(text):
    found = []
    text = stated_not_asked(text)
    if not text:
        return found
    without_possessive = _the_name_without_a_possessive(text)
    for pattern in (OTHER_CALLED, OTHER_NAME_IS, OTHER_NAMED_BARE):
        for match in pattern.finditer(text):
            who = a_person_word(match.group("who"))
            if who.endswith("s") and who[:-1] in RELATIONS:
                who = who[:-1]
            name = match.group("name")
            if not _looks_like_a_name(name) or not _name_after_a_title(name):
                continue
            if who in [entry["who"] for entry in found]:
                continue
            found.append({"who": who, "name": name})
    for match in OTHER_NAMED_BEFORE_VERB.finditer(text):
        who = a_person_word(match.group("who"))
        if who.endswith("s") and who[:-1] in RELATIONS:
            who = who[:-1]
        name = without_possessive.get(str(match.group("name")).lower(), match.group("name"))
        if not _the_word_then_a_verb(name, match.group("verb")):
            continue
        if not _may_be_a_name(name):
            continue
        if who in [entry["who"] for entry in found]:
            continue
        found.append({"who": who, "name": name})
    for match in OTHER_NAMED_CAPITAL.finditer(text):
        who = a_person_word(match.group("who"))
        if who.endswith("s") and who[:-1] in RELATIONS:
            who = who[:-1]
        name = without_possessive.get(str(match.group("name")).lower(), match.group("name"))
        if not _may_be_a_name(name):
            continue
        if who in [entry["who"] for entry in found]:
            continue
        found.append({"who": who, "name": name})
    for match in OTHER_NAMED_MIDLINE.finditer(text):
        who = a_person_word(match.group("who"))
        if who.endswith("s") and who[:-1] in RELATIONS:
            who = who[:-1]
        name = without_possessive.get(str(match.group("name")).lower(), match.group("name"))
        if not _may_be_a_name(name):
            continue
        if who in [entry["who"] for entry in found]:
            continue
        found.append({"who": who, "name": name})
    return found


KID_COUNT = re.compile(
    r"\b(?:i|we)(?:'ve|ve|\s+have|\s+have\s+got|\s+got)\s+(?:got\s+)?"
    r"(?P<n>\d{1,2}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"a\s+couple\s+of)\s+(?:kids?|children|child)\b"
    r"|\bmy\s+(?P<m>\d{1,2}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)"
    r"\s+(?:kids?|children)\b", re.I)
KID_COUNT_AND = re.compile(
    r"\b(?:i|we)(?:'ve|ve|\s+have|\s+have\s+got|\s+got)\s+[^.;!?]{0,40}?(?:\band\b|,)\s*"
    r"(?P<n>\d{1,2}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"a\s+couple\s+of)\s+(?:kids?|children|child)\b", re.I)
KID_NUMBERS = {word: number for number, word in enumerate(
    ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
     "eleven", "twelve"))}
KID_NUMBER_WORDS = {number: word for word, number in KID_NUMBERS.items()}
FIGURE_WORDS = {word: str(number) for number, word in enumerate(
    ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
     "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen",
     "eighteen", "nineteen", "twenty"), start=1)}
FIGURE_PAIR = re.compile(r"\btwenty[\s-]+(one|two|three|four|five|six|seven|eight|nine)\b",
                         re.I)
FIGURE_WORD = re.compile(r"\b(?:" + "|".join(sorted(FIGURE_WORDS, key=len, reverse=True))
                         + r")\b", re.I)


def figures_as_digits(text):
    if not isinstance(text, str) or not text:
        return ""
    text = FIGURE_PAIR.sub(
        lambda match: str(20 + int(FIGURE_WORDS[match.group(1).lower()])), text)
    return FIGURE_WORD.sub(lambda match: FIGURE_WORDS[match.group(0).lower()], text)
KID_AGES = re.compile(
    r"\b(?:kids?|children|child)\b[^.!?]{0,24}?\b(?:are|aged?|of)\s+"
    r"(?P<ages>\d{1,2}(?:\s*(?:,|and)\s*\d{1,2})+)", re.I)
KID_AGES_AFTER_A_COMMA = re.compile(
    r"\b(?:kids?|children)\b\s*[,:;-]\s*(?P<ages>\d{1,2}(?:\s*(?:,|and)\s*\d{1,2})+)", re.I)


def kid_ages(text):
    if not isinstance(text, str):
        return []
    match = KID_AGES.search(figures_as_digits(text)) or KID_AGES_AFTER_A_COMMA.search(
        figures_as_digits(text))
    if match:
        ages = [int(number) for number in re.findall(r"\d{1,2}", match.group("ages"))]
        return [age for age in ages if 0 <= age <= 110]
    counted = _children_by_year_old(figures_as_digits(text))
    if counted:
        return _ages_held(counted)
    grouped = [entry for entry in _other_ages(text)
               if (entry.get("who") or "").lower() in KID_GROUP]
    if grouped and not any(entry.get("name") for entry in grouped):
        held = []
        for entry in grouped:
            held.extend(age for age in _ages_held(entry) if age not in held)
        if held:
            return held
    each = [entry for entry in _other_ages(text)
            if (entry.get("who") or "").lower() in KID_ONE_BY_ONE]
    if len(each) >= 2 and not any(entry.get("name") for entry in each):
        held = []
        for entry in each:
            held.extend(age for age in _ages_held(entry) if age not in held)
        if held:
            return held
    return []


ONES_BY_ONE = re.compile(
    r"\bones?\b|\bthe\s+(?:other|older|younger|little|big|small|eldest|youngest)\s+one\b", re.I)
AGES_ONLY_WORD = frozenset("""and or is are s the other older younger little big small eldest
youngest of them both now too yeah oh well ok okay right so but theyre they there its it aged old
then
years year yrs yo nearly almost just turned about""".split())


def the_ones_are_given_one_at_a_time(text):
    if not isinstance(text, str):
        return False
    return bool(ONES_BY_ONE.search(" ".join(text.lower().replace("'", "").split())))


def ages_said_one_by_one(text, count):
    if not isinstance(text, str) or not isinstance(count, int) or count < 2:
        return []
    flat = " ".join(text.lower().replace("'", "").split())
    if not flat or len(flat.split()) > 12:
        return []
    flat = figures_as_digits(ONES_BY_ONE.sub(" & ", flat))
    ages = []
    for word in re.split(r"[^a-z0-9]+", flat):
        if not word:
            continue
        if word.isdigit():
            age = int(word)
            if not 0 < age <= 120:
                return []
            ages.append(age)
        elif word not in AGES_ONLY_WORD:
            return []
    return ages if len(ages) == count else []


KID_ELSEWHERE = re.compile(
    r"^\s*(?:in|at)\s+(?:my|the|our|a|this|that)\s*(?:class|classes|classroom|school|nursery|"
    r"club|group|team|unit|year)\b|^\s*in\s+year\b|^\s*in\s+(?:reception|year)\b", re.I)
KID_ASKING = re.compile(r"^\W*(?:do|did|does|have|has|how|are|is|was|were|can|could|would)\b",
                        re.I)
KID_NONE = re.compile(
    r"\b(?:i|we)(?:'ve|ve)?\s+(?:do\s+not|dont|don't|did\s+not|didnt|didn't|have\s+not|"
    r"havent|haven't|has\s+not|hasnt|hasn't)\s+(?:got\s+)?(?:have\s+)?(?:any\s+|a\s+)?"
    r"(?:kids?|children|child)\b"
    r"|\b(?:i|we)(?:'ve|ve|\s+have|\s+have\s+got|\s+got)\s+no\s+(?:kids?|children)\b"
    r"|\bno\s+(?:kids?|children)\b"
    r"|\b(?:i|we)(?:'ve|ve|\s+have|\s+have\s+got|\s+got)\s+(?:zero|0)\s+(?:kids?|children)\b",
    re.I)
KID_NONE_NOT_AFTER_ALL = re.compile(
    r"\b(?:yet|anymore|any\s+more|with\s+me|at\s+home|living\s+at\s+home|but|instead)\b", re.I)


def kid_count(text):
    if not isinstance(text, str) or KID_ASKING.match(text):
        return None
    none = KID_NONE.search(text)
    if none and not KID_NONE_NOT_AFTER_ALL.search(text[none.end():]):
        return 0
    match = KID_COUNT.search(text) or KID_COUNT_AND.search(text)
    if not match:
        ages = kid_ages(text)
        if ages:
            return len(ages)
        counted = _children_by_year_old(figures_as_digits(text))
        if counted:
            return len(_ages_held(counted))
        grouped = [entry for entry in _other_ages(text)
                   if (entry.get("who") or "").lower() in KID_GROUP]
        if grouped and not any(entry.get("name") for entry in grouped):
            held = []
            for entry in grouped:
                held.extend(age for age in _ages_held(entry) if age not in held)
            if held:
                return len(held)
        each = [entry for entry in _other_ages(text)
                if (entry.get("who") or "").lower() in KID_ONE_BY_ONE
                and (entry.get("age") or _ages_held(entry))]
        if len(each) >= 2 and not any(entry.get("name") for entry in each):
            return len(each)
        return None
    if KID_ELSEWHERE.search(text[match.end():]):
        return None
    said = (match.group("n") or match.group("m") or "").lower()
    if said.startswith("a couple"):
        return 2
    if said.isdigit():
        return int(said)
    return KID_NUMBERS.get(said)

COUNT_OF_THEM = re.compile(
    r"\b(?:there are|there're|there is|theres|there's|that's|thats|we have|we've got|we got|we"
    r" have got)\s+(?P<n>\d{1,2}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)"
    r"\s+(?:of them|altogether|in total|in all)\b", re.I)
COUNT_OF_THEM_ELSEWHERE = re.compile(
    r"^\s*(?:at|in|on|down|up|over|for|from|who|here|there|with|left|still|near|around|about|"
    r"already|so|but)\b", re.I)
CHILDREN_WORDS = ("kid", "kids", "child", "children", "boy", "boys", "girl", "girls", "son",
                  "sons", "daughter", "daughters", "twin", "twins")


def count_of_the_people(text, memory):
    if not isinstance(text, str) or KID_ASKING.match(text):
        return None
    match = COUNT_OF_THEM.search(text)
    if not match:
        return None
    said = match.group("n").lower()
    number = int(said) if said.isdigit() else KID_NUMBERS.get(said)
    if not number or not 1 < number <= 12:
        return None
    if COUNT_OF_THEM_ELSEWHERE.match(text[match.end():]):
        return None
    if not _the_group_in_hand_is_the_children(memory):
        return None
    return number


def _the_group_in_hand_is_the_children(memory):
    user_record = (memory or {}).get("user")
    turns = (memory or {}).get("turns")
    said = ""
    if isinstance(turns, list):
        last = next((turn for turn in reversed(turns) if isinstance(turn, dict)), None)
        said = " ".join(str((last or {}).get("user") or "").lower().split())
    words = set(re.split(r"[^a-z']+", said))
    if words & set(CHILDREN_WORDS):
        return True
    if isinstance(user_record, dict) and user_record.get("kids"):
        others = set(words) & {"cats", "cat", "dogs", "dog", "pets", "pet", "fish", "birds"}
        return not others
    return False


KIDS = ("kids", "children", "child", "kid")
KID_GROUP = tuple(KIDS) + ("sons", "daughters", "boys", "girls")
KID_ONE_BY_ONE = ("son", "daughter", "sons", "daughters", "child", "children", "kid",
                  "kids", "boy", "girl", "boys", "girls", "baby", "twins", "twin")
A_COUNTED_GROUP = (r"\b(?P<whose>my|our)\s+"
                   r"(?:(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve"
                   r"|\d{1,2})\s+)?")
KID_AGES_ARE = re.compile(A_COUNTED_GROUP + r"(?P<who>" + "|".join(KIDS) + r")\s+(?:are|is)\s+"
                          r"(?:both\s+)?(?:aged?\s+)?(?P<ages>\d{1,3}"
                          r"(?:\s*(?:,|and)\s*\d{1,3})*)", re.I)
KID_GROUP_AGES_ARE = re.compile(A_COUNTED_GROUP + r"(?P<who>" + "|".join(KID_GROUP) + r")\s+"
                               r"(?:are|is)\s+(?:both\s+)?(?:aged?\s+)?"
                               r"(?P<ages>\d{1,3}(?:\s*(?:,|and)\s*\d{1,3})*)", re.I)
KID_COUNT_AGES = re.compile(
    r"\b(?:i|we)(?:\s+have|'ve|ve)(?:\s+got)?\s+(?:\w+\s+)?(?P<who>kids|children)\b"
    r"(?:[^.\d]{0,14})(?P<ages>\d{1,3}(?:\s*(?:,|and)\s*\d{1,3})*)", re.I)
KID_ADULTS_AGES = re.compile(
    r"\b(?:kids?|children|child)\b(?:[^.\d]{0,14})?(?:aged?|of|are)\s+"
    r"(?P<ages>\d{1,3}(?:\s*(?:,|and)\s*\d{1,3})+)", re.I)
KID_AGES_NOT = re.compile(r"\b(?:under|over|above|below|nearly|almost|about|round|around)\s*$", re.I)


KID_NAME_AGES = re.compile(r"\bmy\s+(?P<who>" + "|".join(KID_GROUP) + r")\s+(?:are|is)\s+(?P<rest>"
                           r"[a-z][a-z'-]{1,19}\s+\d{1,3}(?:\s*(?:,|and)\s*"
                           r"[a-z][a-z'-]{1,19}\s+\d{1,3})*)\b", re.I)
KID_NAME_AGE = re.compile(r"(?P<name>[a-z][a-z'-]{1,19})\s+(?P<age>\d{1,3})", re.I)
FIGURE_AFTER = re.compile(r"\d|\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven"
                          r"|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen"
                          r"|nineteen|twenty)\b", re.I)


NOT_A_NAME_HEDGE = frozenset("""nearly almost about around round under over above below
roughly approximately approx somewhere only just both all each every either neither
aged age ages yrs year years old""".split())


def _kids_named_with_ages(text):
    found = []
    who_word = "|".join(RELATIONS)
    for match in KID_NAME_AGES.finditer(text):
        rest = match.group("rest")
        if KID_AGES_NOT.search(text[:match.start("rest")]):
            continue
        pairs = list(KID_NAME_AGE.finditer(rest))
        if not pairs:
            continue
        if len(re.findall(r"\d{1,3}", rest)) != len(pairs) or FIGURE_AFTER.search(text[match.end():]):
            continue
        for pair in pairs:
            name, age = pair.group("name"), int(pair.group("age"))
            low = name.lower()
            if (low in NOT_A_NAME or low in KIDS or low in NOT_A_NAME_HEDGE
                    or low in NOT_A_NAME_MIDDLE or low in NOT_A_NAME_THING
                    or low in NOT_A_NAME_STATE
                    or low in MONTHS or low in DAYS or not 0 <= age <= 120):
                continue
            if age <= 2 and not name[:1].isalpha():
                continue
            found.append({"who": match.group("who").lower(), "name": name,
                          "age": age})
    return found


def _the_same_person(one, other):
    if (one.get("who") or "") != (other.get("who") or ""):
        return False
    return str(one.get("name") or "").lower() == str(other.get("name") or "").lower()


_STATE_WHO = lambda: r"\bmy\s+(?P<who>" + "|".join(sorted(RELATIONS, key=len, reverse=True)) + r")"
OTHER_STATE = re.compile(
    _STATE_WHO() + r"\s*(?P<tense>'s|is|are|was|were)\s+"
    r"(?:(?P<weeks>\d{1,2})\s*(?:weeks?|wks?)\s+)?"
    r"(?P<state>pregnant|expecting|breastfeeding|nursing a baby)\b", re.I)
PREGNANCY_STATES = ("pregnant", "expecting")
OTHER_LIMIT = re.compile(
    _STATE_WHO() + r"\s*(?:can'?t|cannot|doesn'?t|does not|won'?t|will not|isn'?t)"
    r"\s+(?:really\s+)?(?:drink|drinks)\b"
    r"(?=\s*(?:$|[.,;!?]|alcohol\b|at all\b|any ?more\b|anymore\b|either\b|though\b|"
    r"these days\b|now\b|when\b))", re.I)


OWN_STATE = re.compile(
    r"(?:^|[.;,!?]\s*|\b(?:and|but|so|because|although|though)\s+)"
    r"(?:i|im|i'm|i’m|ive|i've)\s+(?:am\s+|was\s+|feel\s+|think\s+i\s*m\s+)?"
    r"(?!not\b|no longer\b|never\b|wasnt\b|wasn't\b)"
    r"(?:(?P<weeks>\d{1,2})\s*(?:weeks?|wks?)\s+)?"
    r"(?P<state>pregnant|expecting)\b", re.I)
OWN_PREGNANCY_WEEKS_MAX = 45


def _own_states(text):
    for match in OWN_STATE.finditer(figures_as_digits(text)):
        said = match.group(0).lower()
        if re.search(r"\b(?:was|were|thought|maybe|might|may|hope|hoping|could)\b", said):
            continue
        found = {"pregnant": True}
        weeks = match.group("weeks")
        if weeks is not None and 1 <= int(weeks) <= OWN_PREGNANCY_WEEKS_MAX:
            found["weeks"] = int(weeks)
        return found
    return {}


def _other_states(text):
    found = []
    for match in OTHER_STATE.finditer(text):
        if match.group("tense").lower() in ("was", "were"):
            continue
        who = " ".join(match.group("who").lower().split())
        state = match.group("state").lower()
        if state in PREGNANCY_STATES:
            entry = {"who": who, "pregnant": True}
            weeks = match.groupdict().get("weeks")
            if weeks and 1 <= int(weeks) <= 45:
                entry["weeks"] = int(weeks)
            found.append(entry)
        else:
            found.append({"who": who, "breastfeeding": True})
    for match in OTHER_LIMIT.finditer(text):
        who = " ".join(match.group("who").lower().split())
        found.append({"who": who, "drinks": False})
    return found
YEAR_OLD = re.compile(r"\b(?P<age>\d{1,3})\s*(?:years?|yrs?)[- ]old\b", re.I)
OWN_AGE_BEFORE_IT = re.compile(r"\b(?:i|we)\s+(?:was|were|am|had been)\s*(?:a|an)?\s*$", re.I)
YEAR_OLD_ANIMAL = re.compile(r"\b(?:" + "|".join(sorted(ANIMALS)) + r")\b", re.I)
THING_AGED = re.compile(
    r"\b(?:it|its|it's|that|thats|that's|this|these|those|there|hes|he's|shes|she's|theyre|"
    r"they're|mine|ours|yours|theirs)\b[^.!?]{0,12}$", re.I)
A_PERSON_AGED = re.compile(
    r"\b(?:he|she|they|hes|she's|he's|shes|theyre|they're)\b[^.!?]{0,12}$", re.I)
NAMED_THING_AGED = re.compile(
    r"\b(?:my|our|your|his|her|their|the)\s+(?P<noun>[a-z' 0-9]{1,30}?)\s*"
    r"(?:is|was|are|were|s|'s)\b[^.!?]{0,12}$", re.I)
THING_AGED_QUALIFIED = re.compile(
    r"\b(?:a|an|the|my|our|your|his|her|their)\s+(?P<noun>[a-z'][a-z'0-9]*)(?:\s*,)?\s*"
    r"(?:(?:is|was|are|were|s|'s)\s*)?(?:(?:,\s*)?(?:about|roughly|around|nearly|only|just)\s*)?$",
    re.I)
PERSON_ELSEWHERE = frozenset("""youngest oldest eldest younger older middle first second third
last little big small""".split())
PEOPLE_AGED = frozenset(KID_GROUP) | frozenset("""kid child children boy boys girl girls son
sons daughter daughters twin twins baby babies toddler toddlers lad lads lass lasses""".split())
AFTER_YEAR_OLD = re.compile(r"^\s+(?P<word>[a-z']{2,})\b", re.I)
AFTER_YEAR_OLD_OKAY = frozenset("""and or but who which that whose now today next in at on
with too as when so already nearly exactly almost about boy girl kid child son daughter lad
lass twins baby toddler to from""".split())
CHILD_AGE_UNDER = 18
LIST_BEFORE_IT = re.compile(r"\d{1,3}\s*(?:,|and|, and)\s*$", re.I)
A_LIST_OF_AGES = re.compile(r"(?P<ages>\d{1,3}(?:\s*(?:,|and|, and)\s*\d{1,3})+)\b", re.I)


GROUP_NAMED = re.compile(r"\b(?:" + "|".join(KID_GROUP) + r")\b", re.I)
THING_NAMED_BACK = re.compile(
    r"\b(?:it|its|it's|that|thats|that's|this|these|those|there|they|theyre|they're)\b"
    r"|\b(?:my|our|your|his|her|their|the)\s+(?P<noun>[a-z' ]{1,30}?)\s*"
    r"(?:is|was|are|were|s|'s)\b", re.I)
PEOPLE_NAMED_ANYWHERE = re.compile(r"\b(?:" + "|".join(sorted(PEOPLE_AGED)) + r")\b", re.I)
SUBJECT_REACH = 80


_A_THING_SAID_IS = re.compile(
    r"\b(?:my|our|your|his|her|their|the)\s+(?P<noun>[a-z' 0-9]{1,30}?)\s*"
    r"(?:is|was|are|were|s|'s)\b[^.!?]{0,40}$", re.I)
_A_THING_POINTED_AT = re.compile(
    r"\b(?:it|its|it's|that|thats|that's|this|these|those|there|theyre|they're|mine|ours)\b"
    r"[^.!?]{0,40}$", re.I)


def _the_years_are_a_things(text):
    figures = list(YEAR_OLD.finditer(text))
    if not figures:
        return False
    for match in figures:
        before = text[max(0, match.start() - 80):match.start()]
        words = re.findall(r"[a-z']+", before.lower())
        if PEOPLE_AGED.intersection(words):
            return False
        named = _A_THING_SAID_IS.search(before)
        if named and named.group("noun").split()[-1].lower() not in PEOPLE_AGED:
            continue
        if _A_THING_POINTED_AT.search(before):
            continue
        return False
    return True


def _children_by_year_old(text):
    if not YEAR_OLD.search(text):
        return None
    if _the_years_are_a_things(text):
        return None
    if (not GROUP_NAMED.search(text)
            and re.search(r"\bmy\s+" + _A_PERSON + r"\b", text, re.I)):
        return None
    group_named = bool(GROUP_NAMED.search(text))
    if group_named and len(YEAR_OLD.findall(text)) > 1:
        return None
    ages = []
    for match in YEAR_OLD.finditer(text):
        age = int(match.group("age"))
        if not 0 <= age <= 120:
            continue
        if OWN_AGE_BEFORE_IT.search(text[:match.start()]):
            continue
        if not group_named and A_PERSON_AGED.search(
                text[max(0, match.start() - 40):match.start()]):
            continue
        if YEAR_OLD_ANIMAL is not None and YEAR_OLD_ANIMAL.search(
                text[max(0, match.start() - 24):match.start()]):
            continue
        before = text[max(0, match.start() - 40):match.start()]
        if breeds.BREED_RE.search(before):
            continue
        if not PEOPLE_NAMED_ANYWHERE.search(text):
            nearest = None
            for found in THING_NAMED_BACK.finditer(
                    text[max(0, match.start() - SUBJECT_REACH):match.start()]):
                nearest = found
            noun = (nearest.groupdict().get("noun") or "").split() if nearest else []
            if nearest is not None and (not noun or noun[-1].lower() not in PEOPLE_AGED):
                continue
        if group_named and LIST_BEFORE_IT.search(before):
            continue
        if THING_AGED.search(before):
            continue
        qualified = THING_AGED_QUALIFIED.search(before)
        if qualified:
            thing = qualified.group("noun").lower()
            if thing not in PEOPLE_AGED and thing not in PERSON_ELSEWHERE:
                continue
        named = NAMED_THING_AGED.search(before)
        if named and named.group("noun").split()[-1].lower() not in PEOPLE_AGED:
            continue
        after = AFTER_YEAR_OLD.match(text[match.end():])
        if after and not group_named and after.group("word").lower() not in AFTER_YEAR_OLD_OKAY:
            continue
        if age >= CHILD_AGE_UNDER and not group_named:
            continue
        ages.append(age)
    if not ages:
        return None
    return {"who": "kids", "ages": ages} if len(ages) > 1 else {"who": "kids", "age": ages[0]}


def _ages_held(entry):
    held = [age for age in entry.get("ages") or [] if isinstance(age, int)]
    if isinstance(entry.get("age"), int) and entry["age"] not in held:
        held.append(entry["age"])
    return held


def _keep_the_ages(found, entry):
    who = entry.get("who")
    known = next((one for one in found if one.get("who") == who), None)
    if known is None:
        found.append(dict(entry))
        return
    said, held = _ages_held(entry), _ages_held(known)
    if held and said and len(held) >= len(said) and set(said) <= set(held):
        return
    known.pop("age", None)
    known["ages"] = said if len(said) > 1 else held + [age for age in said if age not in held]
    if len(known["ages"]) == 1:
        known["age"] = known.pop("ages")[0]


def _other_ages(text):
    text = figures_as_digits(text)
    found = []
    text = stated_not_asked(text)
    if not text:
        return found
    relations = "|".join(sorted(RELATIONS, key=len, reverse=True))
    who_one = r"(?:" + relations + r")(?:\s+in\s+laws?)?"
    group_two = "grandparents|grandchildren"
    pattern = re.compile(r"\bmy\s+(?:(?P<many>(?:" + who_one + r"|" + group_two
                         + r")s?)\s+are|(?P<one>" + who_one + r")\s*(?:'s|is|was))\s+"
                         r"(?P<age>\d{1,3})\b", re.I)
    pair = re.compile(r"\bmy\s+(?P<a>" + who_one + r")\s+and\s+(?:my\s+)?(?P<b>"
                      + who_one + r")s?\s+(?:are|is)\s+(?P<ages>\d{1,3}"
                      r"(?:\s*(?:,|and)\s*\d{1,3})+)", re.I)
    for match in pair.finditer(text):
        ages = [int(number) for number in re.findall(r"\d{1,3}", match.group("ages"))]
        if not all(0 <= age <= 120 for age in ages) or len(ages) < 2:
            continue
        for who, age in zip((match.group("a").lower(), match.group("b").lower()), ages):
            entry = next((one for one in found if one.get("who") == who), None)
            if entry is None:
                found.append({"who": who, "age": age})
            else:
                entry["age"] = age
    for kid_pattern in (KID_GROUP_AGES_ARE, KID_COUNT_AGES, KID_ADULTS_AGES):
        for match in kid_pattern.finditer(text):
            ages = [int(number) for number in re.findall(r"\d{1,3}", match.group("ages"))]
            if not ages or not all(0 <= number <= 120 for number in ages):
                continue
            if KID_AGES_NOT.search(text[:match.start("ages")]):
                continue
            if not AGE_TAIL.match(text[match.end():]):
                continue
            who = (match.groupdict().get("who") or "").lower()
            if not who:
                who = next((one["who"] for one in found
                            if (one.get("who") or "").lower() in KID_GROUP), "kids")
            _keep_the_ages(found, {"who": who, "ages": ages} if len(ages) > 1
                           else {"who": who, "age": ages[0]})
    for match in CHAINED_RELATION_AGE.finditer(text):
        age = int(match.group("age"))
        if not 0 <= age <= 120 or _month_age_after(text, match.end("age")):
            continue
        first = re.sub(r"(?:'s|\u2019s|s)$", "", match.group("first").lower())
        entry = {"who": first + "'s " + match.group("second").lower(), "age": age}
        name = match.groupdict().get("name")
        if name and name.lower() not in _A_WORD_FOR_A_PERSON:
            entry["name"] = name
        found.append(entry)
    for match in RELATION_WHOS_AGE.finditer(text):
        age = int(match.group("age"))
        if not 0 <= age <= 120 or _month_age_after(text, match.end()):
            continue
        found.append({"who": match.group("who").lower(), "age": age})
    for match in AGE_TO_COME.finditer(text):
        kind, who = subject(text, match.end())
        if kind != "other" or (who and who not in RELATIONS):
            continue
        age = int(match.group(1))
        if not 0 <= age <= 120:
            continue
        turns = " ".join(match.group(2).lower().split())
        if not who:
            who = _relation_before(text, match.start())
        if who:
            entry = next((one for one in found if one.get("who") == who), None)
            if entry is not None and not entry.get("turns"):
                entry["turns"] = turns
                if entry.get("age") != age:
                    entry["to_come"] = age
                continue
            found.append({"who": who, "age": age, "turns": turns})
        else:
            pronoun = _the_pronoun(text, match.end())
            if pronoun:
                person = _the_person_the_pronoun_is(text, match.start(), pronoun)
                if person:
                    found.append({"who": person, "age": age, "turns": turns})
                else:
                    found.append({"pronoun": pronoun, "age": age, "turns": turns})
    named = re.compile(r"\bmy\s+(?P<who>" + relations + r")\s+(?P<name>[A-Za-z][a-z'-]{1,19})"
                       r"\s*(?:'s|is|was)\s+(?P<age>\d{1,3})\b", re.I)
    for match in named.finditer(text):
        name = match.group("name")
        if not _may_be_a_name(name):
            continue
        if not AGE_TAIL.match(text[match.end():]):
            continue
        age = int(match.group("age"))
        if not 0 <= age <= 120:
            continue
        who = match.group("who").lower()
        if who.endswith("s") and who[:-1] in RELATIONS:
            who = who[:-1]
        kept = _tidy(name)
        entry = _the_person(found, who, kept)
        if entry is None:
            found.append({"who": who, "name": kept, "age": age})
        else:
            entry.setdefault("name", kept)
            entry["age"] = age
    for match in pattern.finditer(text):
        plural = match.group("many")
        if plural:
            listed = A_LIST_OF_AGES.match(text, match.start("age"))
            if listed:
                ages = [int(number) for number in re.findall(r"\d{1,3}", listed.group("ages"))]
                if (len(ages) > 1 and all(0 <= one <= 120 for one in ages)
                        and AGE_TAIL.match(text[listed.end():])):
                    _keep_the_ages(found, {"who": " ".join(plural.lower().split()), "ages": ages})
                    continue
        rest = text[match.end():]
        if not AGE_TAIL.match(rest):
            continue
        age = int(match.group("age"))
        if not 0 <= age <= 120:
            continue
        who = match.group("many") or match.group("one")
        who = " ".join(who.lower().split())
        who = re.sub(r"\bin laws$", "in law", who)
        if who.endswith("s") and who[:-1] in RELATIONS:
            who = who[:-1]
        entry = _the_person(found, who)
        if entry is None:
            found.append({"who": who, "age": age})
        else:
            if entry.get("turns") and entry.get("age") not in (None, age):
                entry["to_come"] = entry["age"]
            entry["age"] = age
    counted = _children_by_year_old(text)
    if counted:
        _keep_the_ages(found, counted)
    for entry in _kids_named_with_ages(text):
        if not any(one["who"] == entry["who"] and one.get("name") == entry["name"]
                   for one in found):
            found.append(entry)
    return found


def _relation_before(text, pos):
    who = ""
    for match in re.finditer(r"\bmy\s+(" + "|".join(RELATIONS) + r")\b", text[:pos], re.I):
        who = match.group(1).lower()
    return who


def pet_appositive(text, start=0):
    animals = [match.start() for match in PETS.finditer(text)]
    later = [position for position in animals if position >= start]
    limit = later[1] if len(later) > 1 else len(text)
    span = text[start:limit]
    match = PET_APPOSITIVE.search(span)
    if not match or not _names_it_aside(match, span):
        return None
    return match.group(1)


BARE_NAME = re.compile(r"^[\W_]*([a-zA-Z][a-zA-Z'-]{1,19})[\W_]*$")
NOT_A_BARE_NAME = frozenset("""
yes yea yeah yep no nope nah ok okay k fine good great thanks thank ta cheers please
hi hello hey bye later maybe sure right true false nothing none neither dunno
sorry sure why what when where who how which it that this there here them him her
""".split())


def names_offered(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns or not isinstance(turns[-1], dict):
        return None
    match = NAMES_OFFERED.search(str(turns[-1].get("bot") or ""))
    if not match:
        return None
    names = re.findall(r"[A-Za-z][a-z'-]{1,20}", match.group("list"))
    names = [word for word in names if word.lower() not in ("or", "and")]
    if len(names) < 2:
        return None
    return {"animal": match.group("animal").lower(), "names": names}


def a_name_picked(text, memory):
    word = bare_name(text)
    if not word:
        return None
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns or not isinstance(turns[-1], dict):
        return None
    last = turns[-1]
    asked = str(last.get("bot") or "")
    asked_for_one = (asked.rstrip().rstrip('"').endswith("?")
                     and bool(PET_NAME_ASKED.search(asked)))
    theirs = bool(NAME_PICK_ASK.search(str(last.get("user") or "")))
    if not (asked_for_one or theirs or names_offered(memory)):
        return None
    return word


def bare_name(text):
    if not isinstance(text, str):
        return None
    match = BARE_NAME.match(text.strip())
    if not match:
        return None
    word = match.group(1)
    low = word.lower()
    if is_addressing(word):
        return None
    if low in NOT_A_BARE_NAME or low in NOT_A_PET_NAME or low in PET_ANIMALS:
        return None
    if not re.search(r"[aeiouy]", low) or re.fullmatch(r"\d+", low):
        return None
    return word

NOT_DIET = re.compile(r"\b(?:never|no longer|used to|isnt|isn'?t|arent|aren'?t|said|says|"
                      r"asked|wondered|whether)\b|"
                      r"\b(?:is|are|was|were|(?:he|she|it|they|we|i)(?:'s|s|'re|re)?)\s+not\b",
                      re.I)

DIET_STOP = ALLERGY_STOP | frozenset("""much many more anything everything nothing something
food stuff lot any""".split())


def foods_ruled_out(found):
    if not isinstance(found, dict):
        return []
    foods = []
    match = re.match(r"^\s*no\s+([a-z][a-z ]{1,20}?)\s*$", str(found.get("diet") or ""), re.I)
    if match:
        foods.append(match.group(1))
    mine = found.get("allergies") or ()
    if not isinstance(mine, (list, tuple)):
        mine = [mine]
    foods.extend(str(food).strip() for food in mine if str(food).strip())
    for entry in found.get("others") or ():
        if not isinstance(entry, dict):
            continue
        match = re.match(r"^\s*no\s+([a-z][a-z ]{1,20}?)\s*$",
                         str(entry.get("diet") or ""), re.I)
        if match:
            foods.append(match.group(1))
        allergies = entry.get("allergies") or ()
        if not isinstance(allergies, (list, tuple)):
            allergies = [allergies]
        foods.extend(str(food).strip() for food in allergies if str(food).strip())
    return foods


DIET_GROUP = frozenset("""meat meats fish dairy gluten wheat eggs egg sugar carbs seafood
shellfish pork beef chicken lamb alcohol nuts soya soy""".split())


OTHER_NO_DRINK = re.compile(
    r"(?<!\w)(?P<subj>(?:my|our|his|her|their)\s+[a-z]+|he|she|they)(?!\w)"
    r"[^.,;!?]{0,24}?"
    r"(?:(?:is|are|'s|'re|s|re)\s+(?:a\s+|an\s+)?"
    r"(?P<word>teetotal(?:ler|lers)?|tee-?total(?:ler|lers)?|non-?drinker|nondrinker)(?!\w))",
    re.I)


def _other_no_drink(text):
    found = []
    text = stated_not_asked(text)
    if not text:
        return found
    for match in OTHER_NO_DRINK.finditer(text):
        if NOT_DIET.search(match.group(0)):
            continue
        kind, who = subject(text, match.start("subj"))
        if kind == "":
            kind, who = _somebody(match.group("subj"))
        if kind != "other" or who in ANIMALS or who in ("i", "we"):
            continue
        person = _a_person(text, match.end(), who)
        if not person:
            continue
        entry = next((seen for seen in found if _same_person(seen, person)), None)
        if entry is None:
            entry = dict(person)
            found.append(entry)
        entry.setdefault("diet", "no alcohol")
    return found


def _somebody(subject_text):
    named = re.match(r"(?:my|his|her|their|our)\s+(\w+)", subject_text or "", re.I)
    if named:
        word = named.group(1).lower()
        return "other", SPOKEN_RELATION.get(word, word)
    return "other", ""


def _other_diets(text):
    found = []
    text = stated_not_asked(text)
    if not text:
        return found
    claimed = [span for pattern in (ALLERGY, CANNOT_EAT, X_ALLERGY)
               for span in (m.span() for m in pattern.finditer(text))]
    for match in OTHER_DIET.finditer(text):
        if any(start < match.end() and match.start() < end for start, end in claimed):
            continue
        word, food = match.group("word"), match.group("food")
        free = match.group("free")
        at = match.start("word") if word else (match.start("free") if free
                                               else match.start("food"))
        kind, who = subject(text, at)
        if kind == "":
            kind, who = _somebody(match.group("subj"))
        if kind != "other" or who in ANIMALS:
            continue
        if NOT_DIET.search(match.group(0)):
            continue
        if free or word:
            diet = "-".join((free or word).lower().replace("-", " ").split())
        else:
            food = _trim_filler(_finish(food or ""))
            if not food or set(food.split()) & DIET_STOP:
                continue
            if not set(food.split()) & DIET_GROUP:
                continue
            diet = "no " + food
        person = _a_person(text, match.end(), who)
        if not person:
            continue
        entry = next((seen for seen in found if _same_person(seen, person)), None)
        if entry is None:
            entry = dict(person)
            found.append(entry)
        entry.setdefault("diet", diet)
    for entry in _other_no_drink(text):
        person = next((seen for seen in found if _same_person(seen, entry)), None)
        if person is None:
            found.append(entry)
        else:
            person.setdefault("diet", entry["diet"])
    return found


OTHER_CONDITION = re.compile(
    r"(?<!\w)(?P<subj>(?:my|our|his|her|their)\s+[a-z][a-z'\u2019-]*(?:\s+in\s+laws?)?|he|she|they)(?!\w)"
    r"(?:'s|'re|\s+is|\s+are|\s+was|\s+were|s|\s+has|\s+have|\s+got|"
    r"\s+suffers?\s+from|\s+suffering\s+from)\s+(?:a\s+|an\s+)?"
    r"(?P<cond>coeliac|celiac|diabetic|asthmatic|epileptic|anaemic|anemic|"
    r"lactose\s+intolerant|gluten\s+intolerant|"
    r"diabetes|asthma|epilepsy|anaemia|anemia|arthritis|crohn'?s|colitis|ibs|"
    r"high\s+blood\s+pressure|high\s+cholesterol|coeliacs?\s+disease)\b"
    r"(?=\s*(?:[,.;!?]|$|\s+(?:and|but|so|because|which|too|as\s+well|now|since|at\s+the\s+moment)\b))",
    re.I)
CONDITION_AS_A_WORD = {"diabetes": "diabetic", "asthma": "asthmatic",
                       "epilepsy": "epileptic", "anaemia": "anaemic",
                       "anemia": "anaemic", "anemic": "anaemic", "celiac": "coeliac",
                       "crohns": "crohn's", "crohn": "crohn's",
                       "coeliac disease": "coeliac", "celiac disease": "coeliac",
                       "coeliacs disease": "coeliac"}


def _other_conditions(text):
    found = []
    text = stated_not_asked(text)
    if not text:
        return found
    for match in OTHER_CONDITION.finditer(text):
        if NOT_DIET.search(match.group(0)):
            continue
        kind, who = subject(text, match.start("cond"))
        if kind == "":
            kind, who = _somebody(match.group("subj"))
        if kind != "other" or who in ANIMALS:
            continue
        cond = " ".join(match.group("cond").lower().split())
        cond = CONDITION_AS_A_WORD.get(cond, cond)
        person = _a_person(text, match.end(), who)
        if not person:
            continue
        entry = next((seen for seen in found if _same_person(seen, person)), None)
        if entry is None:
            entry = dict(person)
            found.append(entry)
        entry.setdefault("condition", cond)
    return found


JOB_PHRASE = (r"(?P<job>[a-z][a-z'\u2019-]*"
              r"(?:\s+(?!(?:and|but|so|because|who|that|which|in|at|for|on|with|from|near)\b)"
              r"[a-z][a-z'\u2019-]*){0,3})")
OTHER_JOB = re.compile(
    r"(?<!\w)(?P<subj>(?:my|our|his|her|their)\s+[a-z][a-z'\u2019-]*|he|she|they)"
    r"(?:'s|'re|\s+is|\s+are|\s+was|\s+were|s)\s+(?:a|an)\s+" + JOB_PHRASE, re.I)
OTHER_JOB_AS = re.compile(
    r"(?<!\w)(?P<subj>(?:my|our|his|her|their)\s+[a-z][a-z'\u2019-]*|he|she|they)"
    r"[^.,;!?]{0,20}?\b(?:job|work|works|working|worked)\s+as\s+(?:an?\s+)?" + JOB_PHRASE,
    re.I)


OTHER_JOB_NAMED = re.compile(
    r"(?<!\w)(?P<subj>(?:my|our|his|her|their)\s+[a-z][a-z'\u2019-]*)"
    r"\s+(?P<name>[a-z][a-z'\u2019-]*)"
    r"(?:'s|\s+is|\s+was)\s+(?:a|an)\s+" + JOB_PHRASE, re.I)


def _the_job_phrase(phrase, place_job=False):
    cut = _first_tail(phrase, JOB_TAIL_PLACE if place_job else JOB_TAIL)
    if cut:
        phrase = phrase[:cut[0]]
    words = without_the_moment(phrase.split())
    if not words:
        return ""
    first = words[0].lower()
    if (first in JOB_STOP or first in NOT_NAMES or first in NOT_NAMES_EXTRA
            or first in SELF_JUDGEMENT or _is_a_judgement_phrase(words)):
        return ""
    if re.match(r"\d", first):
        return ""
    return _the_role(words)


def _other_jobs(text):
    found = []
    for pattern, place_job in ((OTHER_JOB_AS, True), (OTHER_JOB, False), (OTHER_JOB_NAMED, False)):
        for match in pattern.finditer(text):
            at = match.start("job")
            kind, who = subject(text, at)
            if kind != "other":
                continue
            if JOB_WANTED.search(CLAUSE_EDGE.split(text[:at])[-1]):
                continue
            job = _the_job_phrase(match.group("job"), place_job)
            if not job or job in SOBER_WORDS:
                continue
            person = dict(_a_person(text, at, who))
            if not person:
                continue
            said = (match.groupdict().get("name") or "").strip()
            if (said and not _not_a_name(said, strict_ly=False)
                    and _name_after_a_title(said)
                    and said.lower() not in _A_WORD_FOR_A_PERSON):
                person["name"] = _tidy(said)
            entry = next((seen for seen in found if _same_person(seen, person)), None)
            if entry is None:
                entry = dict(person)
                found.append(entry)
            entry.setdefault("job", job)
    return found


def _names_before_a_fact(text):
    found = []
    for match in PET_BEFORE_FACT.finditer(text):
        name = match.group("name")
        if _not_a_name(name, strict_ly=False) or name.lower() in NOT_A_NAME_MIDDLE:
            continue
        if name.lower() in PET_COMPOUND and not AFTER_A_PET.match(text[match.end("name"):]):
            continue
        found.append((match.start("name"), name))
    return found


def pet_name_only(text, lower=False):
    for match in PET_NAME_ONLY.finditer(text):
        name = match.group(1) or match.group(2) or match.group(3)
        name = _a_name_for_the_pet(name) if name else None
        if name:
            return name
    if lower:
        for match in PET_NAME_ONLY_LOWER.finditer(text):
            name = _a_name_for_the_pet(match.group(1), strict_ly=False)
            if name:
                return name
    return None


def _count_before(text, start):
    match = PET_COUNT.search(text[:start])
    if not match:
        return 0
    word = match.group(1).lower()
    if word.isdigit():
        return int(word)
    return PET_COUNT_WORDS.get(word, 0)


MOST_NAMES = 6


def pet_counts(text):
    found = _pets("i have " + str(text or ""))
    return [{"animal": pet["animal"], "count": pet["count"]}
            for pet in found if pet.get("count")]


def _names_after(rest, count, most=None):
    if count < 2 and not most:
        return []
    target = count if count >= 2 else most
    match = re.match(r"\s*(?:(?:are|is|were|was)\s+)?(?:called|named)\s+", rest, re.I)
    if match:
        rest = rest[match.end():]
    else:
        match = re.match(r"\s*[,:]\s*", rest)
        if not match:
            return []
        rest = rest[match.end():]
    names = []
    for piece in re.split(r"\s*(?:,|/|&|\band\b)\s*", rest):
        piece = piece.strip().strip(".!?")
        if not piece or len(piece.split()) != 1:
            break
        if not NAME_WORD.match(piece) or piece.lower() in NOT_A_NAME:
            break
        names.append(piece)
        if len(names) == target:
            break
    if count < 2:
        return names if len(names) >= 2 else []
    return names if len(names) == count else []


OTHER_PET = re.compile(r"\b(?:my|our)\s+(?:[a-z]+\s+){0,2}(?:" + "|".join(RELATIONS) +
                       r")\s+(?:has|have|got|adopted|rescued|bought|owns?|keeps?|"
                       r"doesn'?t have|doesnt have|does not have|don'?t have|dont have|"
                       r"never had|no longer has|had to (?:give|rehome))\b", re.I)


OWNER_OF = re.compile(r"\b(?:(?:my|our|his|her|their|the)\s+(?:\w+\s+){0,2}?[\w-]+"
                      r"(?:'s|s'|\u2019s))\s+(?:\w+\s+){0,2}$", re.I)
LIVES_ELSEWHERE = re.compile(r"^\s*(?:\w+\s+){0,3}?(?:next door|across the (?:road|street)|"
                             r"in (?:our|the) (?:street|road|village|block)|down the road|"
                             r"from next door|round the corner|up the road)\b", re.I)


OTHER_PEOPLE = (r"(?:neighbou?rs?|landlords?|landlad(?:y|ies)|flatmates?|housemates?|roommates?|"
                r"friends?|mates?|colleagues?|boss(?:es)?|owners?|walkers?|someone|somebody|"
                r"anyone|anybody|nobody|people|another)")
OWNER_OF_PLAIN = re.compile(r"\b(?:their|" + OTHER_PEOPLE + r")\s+(?:[a-z]+\s+){0,2}$|"
                            r"\b(?:someone|somebody|anyone|anybody|nobody)\s+else'?s?\s+"
                            r"(?:[a-z]+\s+){0,2}$", re.I)
OWN_ANIMAL = re.compile(r"\b(?:my|our)\s+(?!(?:" + OTHER_PEOPLE + r")\b)(?:[a-z]+\s+){0,2}$",
                        re.I)


OURS_ANOTHER = re.compile(r"\b(?:we|i)(?:\s+have|\s*'ve|\s*ve)?\s+(?:just\s+|also\s+)?"
                          r"(?:got|gotten|adopted|rescued|took in|taken in|bought|brought home|"
                          r"rehomed)\s+(?:another|a second|one more|a new)\b", re.I)


KIN_OWNER = re.compile(
    r"\b(?:my|our|his|her|their)\s+(?:brothers?|sisters?|mums?|moms?|mothers?|fathers?|dads?|"
    r"sons?|daughters?|grandmas?|grandads?|grandmothers?|grandfathers?|nans?|uncles?|aunts?|"
    r"cousins?|nephews?|nieces?|in-laws?|parents?|neighbou?rs?|flatmates?|housemates?|"
    r"friends?|step-?(?:mums?|moms?|dads?|sons?|daughters?))\b\s+(?:[a-z]+\s+){0,2}$", re.I)


def _not_their_animal(text, start, end):
    before = text[max(0, start - 40):start]
    if KIN_OWNER.search(before):
        return True
    if OWN_ANIMAL.search(before):
        return False
    if OURS_ANOTHER.search(before):
        return False
    return bool(OWNER_OF.search(before) or OWNER_OF_PLAIN.search(before)
                or LIVES_ELSEWHERE.match(text[end:end + 40]))


def _someone_elses(text):
    spans = []
    for match in OTHER_PET.finditer(text):
        end = re.search(r"[.!?;]", text[match.end():])
        spans.append((match.end(), match.end() + end.start() if end else len(text)))
    return spans

FOOD_BEFORE = re.compile(r"\b(?:eat|eats|eating|ate|without|cook|cooked|cooks|cooking|buy|bought|"
                         r"roast|roasted|grilled|fried|order|ordered|serve|served|avoid|avoids|"
                         r"allergic to|instead of)\s+(?:\w+\s+){0,2}$", re.I)
FOOD_AFTER = re.compile(r"\s+(?:\w+\s+){0,2}?(?:(?:for|as)\s+(?:dinner|lunch|tea|supper|"
                        r"breakfast|christmas|a meal)|tonight|today|tomorrow|last night|"
                        r"this evening)\b", re.I)
NAME_BEFORE = re.compile(r"\b(?:called|named)\s+$", re.I)
PET_COMPOUND = frozenset("""
bone bones food meat fingers finger pie cake cakes sandwich soup stock oil sauce
flap collar lead leash harness bed basket bowl cage hutch tank litter tray
toy toys treats treat biscuit biscuits brush shampoo hair fur vet insurance tag
door house kennel mask net bowlful piece poo mess hairball
""".split())
AFTER_ANIMAL = re.compile(r"[a-z]+")
AFTER_A_PET = re.compile(
    r"\s*(?:(?:is|was)(?:n't|nt)?\s+(?:\d|a\b|an\b|so\b|really\b|very\b|getting\b|not\b)|"
    r"(?:has|had|needs|likes|hates|loves|eats|sleeps|snores|bites|chews|barks|sheds|"
    r"doesn't|doesnt|isn't|isnt)\b)", re.I)
THEIR_ANIMAL = re.compile(r"\b(?:my|our)\s+$", re.I)


SOMEONE_ELSE_HAS = re.compile(
    r"\b(?:my|our)\s+(?:" + "|".join(RELATIONS) + r")(?:\s*-?\s*in\s*-?\s*laws?)?\b"
    r"(?:\s+\w+){0,2}?\s+(?:has|have|had|got)\b", re.I)
A_RELATION_OWNED = re.compile(
    r"\b(?:my|our)\s+(?:" + "|".join(RELATIONS) + r")\b"
    r"(?:\s*-?\s*in\s*-?\s*laws?|['\u2019]s?)"
    r"(?:\s+(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|older|"
    r"younger|elder|eldest|youngest|first|second|third|only|own|other))*\s+$", re.I)


def _people(text):
    found = []
    for relation in RELATIONS:
        for match in re.finditer(r"\b" + relation + r"s?\b", text, re.I):
            after = text[match.end():]
            said_possessive = after.startswith("'s") or after.startswith("s'")
            if said_possessive:
                after = after.split("'", 1)[1][1:]
            if IN_LAW_AFTER.match(after):
                found.append(relation + " in law")
                break
            words = [word.strip(".,!?;:'") for word in after.split()]
            words = [word for word in words if word]
            next_word = words[0].lower() if words else ""
            if next_word in COMPOUND_AFTER:
                if not ((str(match.group(0)).lower().endswith("s") or said_possessive)
                        and next_word in COMPOUND_THAT_IS_THEIRS):
                    continue
            before = _the_clause_before(text, match.start())
            if SOMEONE_ELSE_HAS.search(before) or A_RELATION_OWNED.search(before):
                continue
            if SELF_AS_A_ROLE.search(text[:match.start()]) and is_a_judgement(text):
                continue
            inlaw = re.match(r"\s+in\s+laws?\b", after, re.I)
            found.append(relation + (" " + " ".join(inlaw.group(0).split()) if inlaw else ""))
            break
    return found


OWNED = frozenset("""car phone mobile iphone laptop bike motorbike motorcycle van tablet ipad
camera tv television boiler oven fridge freezer dishwasher washing-machine tumble-dryer
hoover vacuum mower kettle""".split())
OWNED_VALUE = re.compile(
    r"\b(?:my|our)\s+(?P<thing>[a-z][a-z-]*)(?:\s+(?:is|was)|\s*'s)\s+(?:a|an|the)\s+"
    r"(?P<value>[a-z0-9][a-z0-9' .+-]{0,31})"
    r"|\bthe\s+(?P<thing2>[a-z][a-z-]*)\s+i\s+(?:drive|ride|use|have|own)\s+(?:is|'s)\s+"
    r"(?:a|an|the)\s+(?P<value2>[a-z0-9][a-z0-9' .+-]{0,31})"
    r"|\bi\s+(?P<verb>drive|ride)\s+(?:a|an|the)\s+(?P<value3>[a-z0-9][a-z0-9' .+-]{0,31})"
    r"|\bi(?:'ve|\u2019ve)?\s+(?:have|got)\s+(?:a|an|the)\s+"
    r"(?P<value4>[a-z0-9][a-z0-9' .+-]{0,31})",
    re.I)
OWNED_STOP = frozenset("""and but so because or plus then which that who what when where why how
if although though while also too as well""".split())
OWNED_MAKES = {
    "ford": ("car", "Ford"), "vauxhall": ("car", "Vauxhall"), "toyota": ("car", "Toyota"),
    "volkswagen": ("car", "Volkswagen"), "vw": ("car", "VW"), "bmw": ("car", "BMW"),
    "audi": ("car", "Audi"), "nissan": ("car", "Nissan"), "honda": ("car", "Honda"),
    "kia": ("car", "Kia"), "hyundai": ("car", "Hyundai"),
    "peugeot": ("car", "Peugeot"), "renault": ("car", "Renault"),
    "citroen": ("car", "Citroen"), "skoda": ("car", "Skoda"), "volvo": ("car", "Volvo"),
    "mini": ("car", "MINI"), "fiat": ("car", "Fiat"), "tesla": ("car", "Tesla"),
    "mazda": ("car", "Mazda"), "suzuki": ("car", "Suzuki"), "jaguar": ("car", "Jaguar"),
    "seat": ("car", "SEAT"), "dacia": ("car", "Dacia"), "lexus": ("car", "Lexus"),
    "mitsubishi": ("car", "Mitsubishi"), "subaru": ("car", "Subaru"),
    "mercedes": ("car", "Mercedes"), "cupra": ("car", "Cupra"),
    "iphone": ("phone", "iPhone"), "oneplus": ("phone", "OnePlus"),
    "pixel": ("phone", "Pixel"), "samsung": ("phone", "Samsung"),
    "motorola": ("phone", "Motorola"), "nokia": ("phone", "Nokia"),
    "xiaomi": ("phone", "Xiaomi"), "redmi": ("phone", "Redmi"), "oppo": ("phone", "Oppo"),
    "huawei": ("phone", "Huawei"), "honor": ("phone", "Honor"),
    "fairphone": ("phone", "Fairphone"),
    "boardman": ("bike", "Boardman"), "carrera": ("bike", "Carrera"),
    "trek": ("bike", "Trek"), "giant": ("bike", "Giant"),
    "brompton": ("bike", "Brompton"), "specialized": ("bike", "Specialized"),
    "ridgeback": ("bike", "Ridgeback"), "voodoo": ("bike", "Voodoo"),
    "cube": ("bike", "Cube"), "scott": ("bike", "Scott"),
    "pinnacle": ("bike", "Pinnacle"), "dawes": ("bike", "Dawes"),
    "worcester": ("boiler", "Worcester"), "vaillant": ("boiler", "Vaillant"),
    "ideal": ("boiler", "Ideal"), "baxi": ("boiler", "Baxi"),
    "viessmann": ("boiler", "Viessmann"), "potterton": ("boiler", "Potterton"),
    "bosch": (None, "Bosch"), "lg": (None, "LG"), "sony": (None, "Sony"),
    "panasonic": (None, "Panasonic"), "philips": (None, "Philips"),
    "dyson": (None, "Dyson"), "hoover": (None, "Hoover"), "miele": (None, "Miele"),
    "smeg": (None, "Smeg"), "aeg": (None, "AEG"), "zanussi": (None, "Zanussi"),
    "beko": (None, "Beko"), "indesit": (None, "Indesit"), "hotpoint": (None, "Hotpoint"),
    "neff": (None, "Neff"), "siemens": (None, "Siemens"), "whirlpool": (None, "Whirlpool"),
    "candy": (None, "Candy"), "shark": (None, "Shark"), "vax": (None, "Vax"),
    "henry": (None, "Henry"), "canon": (None, "Canon"), "nikon": (None, "Nikon"),
    "fujifilm": (None, "Fujifilm"), "olympus": (None, "Olympus"), "dell": (None, "Dell"),
    "lenovo": (None, "Lenovo"), "acer": (None, "Acer"), "asus": (None, "Asus"),
    "toshiba": (None, "Toshiba"), "macbook": (None, "MacBook"), "ipad": (None, "iPad"),
    "ipod": (None, "iPod"), "apple": (None, "Apple"), "surface": (None, "Surface"),
    "razer": (None, "Razer"), "flymo": (None, "Flymo"), "mountfield": (None, "Mountfield"),
    "stihl": (None, "Stihl"), "ryobi": (None, "Ryobi"), "makita": (None, "Makita"),
    "husqvarna": (None, "Husqvarna"), "rangemaster": (None, "Rangemaster"),
    "electrolux": (None, "Electrolux"),
}
OWNED_MODELS = {
    "fiesta": ("car", "Fiesta"), "focus": ("car", "Focus"), "golf": ("car", "Golf"),
    "corsa": ("car", "Corsa"), "astra": ("car", "Astra"), "polo": ("car", "Polo"),
    "clio": ("car", "Clio"), "micra": ("car", "Micra"), "yaris": ("car", "Yaris"),
    "qashqai": ("car", "Qashqai"), "mondeo": ("car", "Mondeo"),
    "fabia": ("car", "Fabia"), "ibiza": ("car", "Ibiza"),
    "sportage": ("car", "Sportage"), "tucson": ("car", "Tucson"),
    "civic": ("car", "Civic"), "passat": ("car", "Passat"), "octavia": ("car", "Octavia"),
    "transit": ("car", "Transit"),
}
OWNED_KIND = {"car": "car", "van": "car", "bike": "bike", "motorbike": "bike",
              "motorcycle": "bike", "phone": "phone", "mobile": "phone", "boiler": "boiler"}
OWNED_NOT_A_MODEL = frozenset("""old new broken dead knackered leaking noisy rubbish great fine
ok okay good bad slow fast heavy light cheap expensive tiny small big rubbish fantastic brilliant
useless amazing lovely horrible awful terrible second third hand handy faulty dodgy nightmare
disaster joke mess dream beauty beast monster bargain steal ripoff wreck banger shed pain on mine
yours theirs ours its""".split())


OPENS_AN_ASK = re.compile(r"^(?:what|which|who|whom|whose|how|where|when|why|do|does|did|is|are|"
                          r"was|were|can|could|would|should|shall|will|have|has)\b", re.I)
TELLS_ABOUT = re.compile(r"^(?:my|our|the|i|we|he|she|they)\b", re.I)


def _a_question(text):
    low = str(text or "").strip()
    if OPENS_AN_ASK.match(low):
        return True
    return low.endswith("?") and not TELLS_ABOUT.match(low)


def _owns(text):
    if not text or _a_question(text):
        return {}
    found = {}
    for match in OWNED_VALUE.finditer(text):
        thing = (match.group("thing") or match.group("thing2") or "").lower()
        said = (match.group("value") or match.group("value2") or match.group("value3")
                or match.group("value4") or "")
        if not thing and match.group("value4"):
            thing = _the_thing_of(match.group("value4"))
        if not thing:
            thing = {"drive": "car", "ride": "bike"}.get((match.group("verb") or "").lower(), "")
        thing = thing.replace("-", " ")
        if thing not in OWNED or thing in found:
            continue
        value = _the_model(said, thing)
        if value:
            found[thing] = value
    return found


def _the_thing_of(value):
    words = re.findall(r"[A-Za-z0-9][A-Za-z0-9'+-]*", str(value or ""))
    family = (OWNED_MAKES.get(words[0].lower()) or (None, ""))[0] if words else None
    return {"car": "car", "phone": "phone", "bike": "bike", "boiler": "boiler"}.get(family, "")


def _the_model(value, thing=""):
    words = []
    for word in re.findall(r"[A-Za-z0-9][A-Za-z0-9'+-]*", str(value or "")):
        if word.lower() in OWNED_STOP or len(words) == 4:
            break
        words.append(word)
    words = without_the_moment(words)
    if not words:
        return ""
    first = words[0].lower()
    if first in OWNED_NOT_A_MODEL:
        return ""
    kind = OWNED_KIND.get(str(thing or "").lower(), "")
    make = OWNED_MAKES.get(first)
    if make:
        if kind and make[0] and make[0] != kind:
            return ""
        return _spell_the_model(words)
    model = OWNED_MODELS.get(first)
    if not model or not kind or model[0] != kind:
        return ""
    return _spell_the_model(words)


def _spell_the_model(words):
    spelled = []
    for word in words:
        known = OWNED_MAKES.get(word.lower()) or OWNED_MODELS.get(word.lower())
        spelled.append(known[1] if known else word[:1].upper() + word[1:])
    return " ".join(spelled)


def _a_name_given_by_the_verb(word):
    word = str(word or "").strip()
    low = word.lower()
    if low in NOT_A_NAME or low in NOT_THE_VERB_NAME or low in NOT_A_PRONOUN_NAME:
        return False
    return bool(NAME_WORD.match(word))


GROWN_UP = {"puppy": "dog", "pup": "dog", "kitten": "cat", "kitty": "cat"}


def _the_same_animal(one, other):
    return GROWN_UP.get(one, one) == GROWN_UP.get(other, other)


def _with_the_breed(pet, breed):
    if breed:
        pet["breed"] = breed
    return pet


def _pets(text, question=False):
    theirs = _someone_elses(text)
    names = [(_name_at(match), _with_title(match)) for match in PET_NAME.finditer(text)]
    names += [(_name_at(match), _with_title(match)) for match in PET_VERB_NAME.finditer(text)
              if _a_name_given_by_the_verb(match.group("name"))
              and (match.group("whose") or "").lower() not in NOT_THEIR_DETERMINER]
    names += [(match.start(1), match.group(1)) for match in PET_PRONOUN_NAME.finditer(text)
              if _a_name_given_by_the_verb(match.group(1))]
    names += [found for found in _names_before_a_fact(text)
              if found[1] not in [name for _, name in names]]
    names += [(_name_at(match), _with_title(match)) for match in PET_IS_NAME.finditer(text)
              if _with_title(match) not in [name for _, name in names]]
    names += [(match.start("name"), _with_title(match))
              for match in PET_POSSESSIVE_NAME.finditer(text)
              if _a_name_for_the_pet(match.group("name"), strict_ly=False)
              and _with_title(match) not in [name for _, name in names]]
    names += [(match.start(1), match.group(1)) for match in PET_APPOSITIVE.finditer(text)
              if _names_it_aside(match, text)]
    names = [(position, name) for position, name in names if name.lower() not in NOT_A_NAME]
    names.sort()
    if question:
        names = [(position, name) for position, name in names if name[:1].isupper()]
    named_at = {position for position, _ in names}
    animals = [[match.start(), match.end(), match.group(1).lower(), ""]
               for match in PETS.finditer(text)
               if not any(start <= match.start() < stop for start, stop in theirs)
               and match.start() not in named_at]
    one_of_the_group = set()
    for match in breeds.BREED_RE.finditer(text):
        if any(start <= match.start() < stop for start, stop in theirs):
            continue
        if match.start() in named_at:
            continue
        breed = breeds.the_breed_named(match.group(0))
        kind = breeds.BREED_KIND.get(breed, "")
        if not kind:
            continue
        if not breeds.a_frame_before(text, match.start()):
            continue
        after = re.match(r"[\s-]*([a-z]+)", text[match.end():match.end() + 24])
        if after and after.group(1).lower() in breeds.NOT_A_CREATURE_NEXT:
            continue
        beside = [entry for entry in animals if _the_same_animal(entry[2], kind)
                  and abs(entry[0] - match.start()) <= 40]
        if beside:
            closest = min(beside, key=lambda entry: abs(entry[0] - match.start()))
            if not closest[3]:
                closest[3] = breed
                if _count_before(text, closest[0]) > 1:
                    one_of_the_group.add(closest[0])
            continue
        animals.append([match.start(), match.end(), kind, breed])
    animals.sort()
    pets = []
    one_animal = len(animals) == 1
    for index, (start, end, animal, breed) in enumerate(animals):
        limit = animals[index + 1][0] if index + 1 < len(animals) else len(text)
        before = text[max(0, start - 60):start]
        second = bool(ANOTHER_ANIMAL.search(before) or ALSO_HAVE.search(before))
        if FOOD_BEFORE.search(text[max(0, start - 30):start]):
            continue
        if taste.said_about(text, start):
            continue
        if FOOD_AFTER.match(text[end:end + 30]):
            continue
        after = re.match(r"\s*([a-z]+)(.{0,40})", text[end:], re.S)
        compound_they_have = False
        if after and after.group(1).lower() in PET_COMPOUND:
            named = (THEIR_ANIMAL.search(text[max(0, start - 12):start])
                     and AFTER_A_PET.match(after.group(2)))
            if not named:
                if not THEIR_ANIMAL.search(text[max(0, start - 12):start]):
                    continue
                compound_they_have = True
        if NAME_BEFORE.search(text[max(0, start - 12):start]):
            continue
        if _not_their_animal(text, start, end):
            pets.append(_with_the_breed(_not_theirs(animal, text, start, end), breed))
            continue
        clause = CLAUSE_EDGE.split(text[max(0, start - 60):start])[-1]
        if (_only_wanted(text, start, end)
                or NOT_HAVE.search(clause)
                or WITHOUT_ANIMAL.search(clause)
                or NOT_JUST.search(clause)
                or taken_back_before(text, start)):
            pets.append(_with_the_breed(_not_theirs(animal, text, start, end), breed))
            continue
        coming = _coming_home(text, start)
        count = _count_before(text, start)
        plural = count < 2 and text[start:end].lower().endswith("s")
        listed = _names_after(text[end:limit], count, most=MOST_NAMES if plural else None)
        if compound_they_have:
            listed = []
        if question:
            listed = [name for name in listed if name[:1].isupper()]
        if listed:
            pets.extend(_with_the_breed({"animal": animal, "name": name,
                                         **({"coming": True} if coming else {})}, breed)
                        for name in listed)
            for name in listed:
                if name in names:
                    names.remove(name)
            continue
        name = None
        for position, candidate in list(names):
            if end <= position < limit:
                name = candidate
                names.remove((position, candidate))
                break
        if question and not name:
            if PET_APPOSITIVE.search(text[start:limit]) is None:
                continue
        if not name and count > 0:
            pet = {"animal": animal, "name": name, "count": count}
        else:
            pet = {"animal": animal, "name": name}
        if coming:
            pet["coming"] = True
        age = _pet_age(text[end:limit])
        if not age and one_animal and not pet.get("count"):
            age = _pet_age_tail(text[end:limit])
        if age:
            pet["age"] = age[0]
            if age[1]:
                pet["unit"] = age[1]
        if second:
            pet["another"] = True
        if breed and start in one_of_the_group:
            pet["breed_of_one"] = True
        pets.append(_with_the_breed(pet, breed))
    return pets


PET_AGE_TAIL = re.compile(
    r"^\s*(?:is\s+(?:a|an)\s+[A-Za-z][A-Za-z'-]{1,19}\s*)?(?:,|\band\b)\s*"
    r"(?:(?:hes|shes|its|theyre|he's|she's|it's|they're|he is|she is|it is|they are)\s+)?"
    r"(?:aged?\s+)?(?P<age>\d{1,2})(?![\d.,]\d)"
    r"(?!\s*(?:kg|kilo\w*|lbs?|pounds?|stone|st|cm|inches?|inch|metres?|meters?|miles?|km|mph|"
    r"hours?|hrs?|mins?|minutes?|percent|%))"
    r"\s*(?P<unit>years?|yrs?|months?|weeks?)?\b", re.I)


def _pet_age_tail(after):
    match = PET_AGE_TAIL.match(str(after or ""))
    if not match:
        return None
    age = int(match.group("age"))
    if not 0 < age <= 40:
        return None
    unit = str(match.group("unit") or "").lower()
    return age, ("months" if unit.startswith("month")
                 else "weeks" if unit.startswith("week") else "")


PET_AGE = re.compile(
    r"^\s*(?:[A-Za-z][A-Za-z'-]{1,19}\s+)?(?:is|was|are|were)\s+(?P<age>\d{1,2})"
    r"(?![\d.,]\d)"
    r"(?!\s*(?:kg|kilo\w*|lbs?|pounds?|stone|st|cm|inches?|inch|metres?|meters?|miles?|km|mph|"
    r"hours?|hrs?|mins?|minutes?|percent|%))"
    r"\s*(?P<unit>years?|yrs?|months?|weeks?)?\b", re.I)


PET_AGE_BARE = re.compile(
    r"^\s*[,;:]?\s*(?:aged\s+)?(?P<age>\d{1,2})\s*(?P<unit>years?|yrs?|months?|weeks?)"
    r"(?:\s*old)?\b", re.I)


def _pet_age(rest):
    match = PET_AGE.match(rest) or PET_AGE_BARE.match(rest)
    if not match:
        return None
    age = int(match.group("age"))
    if not 0 < age <= 30:
        return None
    unit = (match.group("unit") or "").lower()
    if unit.startswith("month"):
        unit = "months"
    elif unit.startswith("week"):
        unit = "weeks"
    else:
        unit = ""
    return age, unit


ADDRESSING = frozenset("""
mate matey mates pal fella feller fellas chum cocker bruv bro brother sis sister
love lovey duck ducks petal hun hon dear dearie sunshine lad lass guys folks friend
son daughter dad mum mam mom missus mister sir madam flower
""".split())


def is_addressing(word):
    return isinstance(word, str) and word.lower() in ADDRESSING


def _names_it_aside(match, text):
    word = match.group(1)
    if not _not_a_name(word):
        return True
    return word[:1].isupper() and bool(re.search(r"[A-Za-z]", text[match.end():]))


NOT_A_NAME_EITHER = frozenset((
    "me", "her", "him", "us", "them", "you", "my", "your", "his", "hers", "its", "it", "this",
    "that", "these", "those", "who", "what", "which", "someone", "somebody", "anyone", "anybody",
    "everyone", "everybody", "nobody", "something", "anything", "nothing", "after", "for", "by",
    "with", "from", "up", "out", "back", "there", "here", "then", "not", "never", "still",
    "also", "too", "either", "both", "all",
))


DESCRIBING_ENDS = ("ing", "ous", "ful", "less", "ness", "able", "ible", "ity", "ation",
                   "ition", "sion")
DESCRIBING_WORDS = frozenset("""
clever stubborn overweight underweight thin tall short fat skinny slim lazy happy sad funny angry
hungry thirsty pretty ugly smelly messy noisy silly busy cheeky grumpy sleepy cranky dizzy clumsy
greedy greedy wealthy healthy rocky risky shaky steep bumpy itchy sweaty queasy tipsy
nosey spoiled bratty mardy stroppy sulky clingy fit unfit taken best worst
""".split()) | NOT_A_NAME_DESCRIBING
ED_NAMES = frozenset("fred ed ned ted jed".split())


def _describes_them(word):
    low = str(word or "").lower()
    if not low:
        return False
    if low in STATE_WORDS or low in DESCRIBING_WORDS or low in lexicon.A_STATE:
        return True
    if low in DIET_WORDS or low in DIET_NAMES or low in DIET_FREE_WORDS or low in SOBER_WORDS:
        return True
    if low in ED_NAMES:
        return False
    if low.endswith("ed") and len(low) > 3:
        return True
    return any(low.endswith(end) and len(low) > len(end) + 2 for end in DESCRIBING_ENDS)


NOT_A_NAME_WORD = frozenset("""name names nickname called known ages age""".split())


def _bare_name(word, pair=False):
    said = str(word or "").strip().strip(".,!?;:'\"")
    low = said.lower()
    if not re.fullmatch(r"[a-z][a-z'-]{1,19}", low):
        return ""
    if _not_a_name(said, strict_ly=False):
        return ""
    if low in WORD_NUMBERS:
        return ""
    if low in NOT_A_NAME_WORD:
        return ""
    if is_a_contraction(low):
        return ""
    if low in lexicon.COMMON_NAMES or low in NAMES_THAT_END_LIKE_A_VERB:
        return _tidy(_finish(said))
    if not said[:1].isupper() and _describes_them(low):
        return ""
    if not pair and low in normalize.LEXICON and not said[:1].isupper():
        return ""
    return _tidy(_finish(said))


COMMON_WORDS = frozenset(lexicon.COMMON.split()) | frozenset(lexicon.CORE_WORDS) | lexicon.A_STATE


NOT_A_NAME_ENDINGS = ("ed", "ing", "ous", "ful", "less", "ish", "able", "ible", "ive", "est", "ly",
                      "al", "ic")


def a_name_could_be(word):
    low = str(word or "").strip().lower()
    if not re.fullmatch(r"[a-z][a-z'-]{1,19}", low):
        return False
    if low in MONTHS or low in DAYS:
        return False
    if low in lexicon.COMMON_NAMES:
        return True
    if low in NOT_A_PET_NAME or low in NOT_NAMES or low in NOT_NAMES_EXTRA:
        return False
    if low in STATE_WORDS or low in DESCRIBING_WORDS:
        return False
    if low not in COMMON_WORDS and low.endswith(NOT_A_NAME_ENDINGS):
        return False
    return low not in COMMON_WORDS


NEGATED_VERB = re.compile(r"^(?P<stem>[a-z]{2,})n['\u2019]?t$")


def is_a_contraction(word):
    low = str(word or "").strip().strip(".,!?;:'\"").lower().replace("\u2019", "'")
    match = NEGATED_VERB.match(low)
    if not match:
        return False
    stem = match.group("stem")
    return stem in normalize.LEXICON or stem + "e" in normalize.LEXICON


def _not_a_name(word, strict_ly=True):
    low = word.lower()
    if is_addressing(word) or low in NOT_A_PET_NAME or low in NOT_NAMES or low in NOT_NAMES_EXTRA:
        return True
    if low in NOT_A_NAME_EITHER:
        return True
    if low in PET_ANIMALS or not re.search(r"[aeiouy]", low):
        return True
    if strict_ly and low.endswith("ly") and len(low) > 4:
        return True
    if _a_word_not_a_name(low):
        return True
    return bool(re.fullmatch(r"\d+", low))


def _object_words(rest):
    words = [w for w in re.findall(r"[a-z']+", str(rest or "").lower()) if w not in ARTICLES]
    return [w for w in words if w not in PREPOSITIONS] if words else []


def _object_plan(rest):
    if not rest:
        return False
    first = re.sub(r"[^a-z]", "", rest.split()[0].lower())
    return first in PREPOSITIONS


def _plan_verb(match, rest):
    verb = PERSON_OPEN.sub("", match.group(0), count=1).strip(" .")
    words = verb.split()
    if not words or not words[0].lower().endswith("ing"):
        return ""
    if _object_plan(rest) or words[-1].lower() in PARTICLES:
        return verb[:1].upper() + verb[1:]
    return ""


def _a_plan_has_a_thing(rest):
    if not _object_plan(rest):
        return True
    words = _object_words(rest)
    return bool(words) and words[0] not in POINTING


PLAN_CLAUSE_BREAK = re.compile(r"[.!?,;:]|\s+(?:and|but|so|then|or)\s+", re.I)
PLAN_CLAUSE_OPENER = re.compile(r"^(?:(?:and|but|so|then|or|ok|okay|also|well|oh|plus|now)\b[ ,]*)*",
                                re.I)


def _asks_about_the_plan(text, at):
    before = text[:at]
    if ASKED_BEFORE.search(before):
        return True
    clause = PLAN_CLAUSE_BREAK.split(before)[-1]
    clause = PLAN_CLAUSE_OPENER.sub("", clause.strip()).strip()
    return bool(clause) and bool(ASKING.match(clause))


def _plan_text(text, start):
    rest = text[start:].strip(" ,;:-")
    rest = re.split(r"(?<=[.!?])\s|\s+(?:but|and then|so)\s+", rest, 1)[0].strip(" ,;:-")
    rest = re.split(r",\s+(?:(?:how|what|which|where|when|who|why|should|can|could|would|do|does|"
                    r"is|are|will|any|and)\b)", rest, 1)[0].strip(" ,;:-")
    if not rest:
        return ""
    return rest[0].upper() + rest[1:] if rest else ""


COPULA = re.compile(
    r"^\W{0,2}(?:i(?:'m| am)|im|i\s+feel|i\s+felt|i(?:'ve| have)\s+been|we(?:'re| are)|were|"
    r"we\s+feel)\s+(?P<rest>.+)$", re.I)
STATE_FILLER = frozenset("""really so very quite pretty rather too still just feeling feel felt
been absolutely completely totally a bit kind of sort of kind sort getting more less somewhat
this that week weekend morning evening afternoon night today tomorrow month year""".split())
STATE_PARTICLE = frozenset("""up down in on at out off away back home here there over around
from with for by of to near into than as after upstairs downstairs online offline asleep awake
outside inside late early soon nearly almost definitely probably maybe honestly seriously
literally actually totally completely absolutely half mid bloody""".split())
STATE_MORE = frozenset("""low flat blue rough rubbish manky wiped better worse ill sick
                             unwell poorly""".split())
STATE_WORDS = frozenset(
    word for word in (NOT_NAMES_EXTRA | STATE_MORE |
                      frozenset(word for cues in EMOTION_WORDS.values()
                                for cue in cues for word in cue.split()))
    if word not in STATE_PARTICLE)


OFF_ABSENCE = re.compile(r"\boff (?:sick|work|school|college|uni|university|shift|shifts|rota)\b",
                         re.I)
OFF_AHEAD = re.compile(r"\bnext\b|\btomorrow\b|\bon\s+(?:mon|tues|wednes|thurs|fri|satur|sun)day"
                       r"|\bin\s+(?:january|february|march|april|may|june|july|august|september"
                       r"|october|november|december)\b", re.I)


def _how_they_are(clause):
    match = COPULA.match(clause)
    if not match:
        return False
    if OFF_ABSENCE.search(match.group("rest")) and OFF_AHEAD.search(clause):
        return False
    rest = " " + match.group("rest").lower() + " "
    rest = re.sub(r"[^a-z' ]", " ", FUTURE.sub(" ", rest))
    words = [word for word in rest.split() if word not in STATE_FILLER]
    words = [word for word in words if word not in STATE_PARTICLE]
    return bool(words) and all(word in STATE_WORDS for word in words)


THING_COPULA = re.compile(
    r"^\W{0,2}(?:my|our|the)\s+[a-z'\u2019\-]+(?:\s+[a-z'\u2019\-]+)?\s+"
    r"(?:is|are|was|were|has been|have been|had been|feels?|felt|seems?|seemed|looks?|looked|"
    r"gets?|got|remains?)\s+(?P<rest>.+)$", re.I)


AHEAD_OF_THE_THING = re.compile(
    r"\b(?:due|booked|scheduled|expected|coming|starting|beginning|renewal|renewed|renewing|"
    r"up\s+for|going\s+up|out\s+on|in\s+for|on\s+order|happening)\b", re.I)
THING_TODAY = frozenset("""
    broken bust bursting cracked leaking leaky dripping damp mouldy mouldering rusty
    clogged blocked jammed faulty dead knackered noisy slow patchy scratched chipped wonky
    playing playing-up playin sticking wobbling rattling screeching smoking
    """.replace("playing-up", "playing up").split())


def _how_their_things_are(clause):
    match = THING_COPULA.match(clause)
    if not match:
        return False
    raw = match.group("rest").lower()
    if AHEAD_OF_THE_THING.search(raw):
        return False
    rest = " " + raw + " "
    rest = re.sub(r"[^a-z' ]", " ", FUTURE.sub(" ", rest))
    words = [word for word in rest.split() if word not in STATE_FILLER]
    words = [word for word in words if word not in STATE_PARTICLE]
    return bool(words) and all(word in STATE_WORDS or word in THING_TODAY for word in words)


APPOINTMENT_CLOCK = re.compile(
    r"\b(?:at|around|about|for|by)\s+((?:1[0-2]|0?[1-9])(?:[:.][0-5]\d)?\s*(?:am|pm)?|noon|midday|"
    r"midnight|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\b", re.I)
APPOINTMENT_DAY = re.compile(
    r"\b(?:(?:on|this|next)\s+)?(?:mon|tues|wednes|thurs|fri|satur|sun)day\b|\b(?:today|tomorrow|"
    r"tonight|this (?:morning|afternoon|evening))\b|\b(?:(?:on|by)\s+)?" + DAY_AND_MONTH +
    r"\b", re.I)
APPOINTMENT_PAST = re.compile(
    r"\b(?:yesterday|was|were|went|had|did|last (?:night|week|monday|tuesday|wednesday|thursday|friday|"
    r"saturday|sunday)|ago|already)\b", re.I)
APPOINTMENT_OWN_SUBJECT = re.compile(
    r"^(?:ok(?:ay)?[, ]+|and |so |but |also |well |oh )*"
    r"(?:i|i'm|im|i've|i'd|id|we|we're|were|we've|weve|we'd)\b", re.I)
TAKE_BACK_WORDS = re.compile(CORRECTION_TAKEBACK + r"|mak(?:e|ing)\s+(?:that|it)", re.I)
APPOINTMENT_NOT_A_THING = frozenset("""it its it's that this he she they them there here we us
i im i'm you what when where which who why how the a an anything something nothing everything
whatever""".split())
APPOINTMENT_PAST_VERB = frozenset("""came went left rang arrived started finished met ate had was
were got sent made saw took gave told said ran sat stood put bought paid brought caught found
kept slept spoke drove flew drank began broke chose fell felt fought heard held hit hurt lost
meant read rode rose sold sang shut spent threw understood woke wore won wrote""".split())
APPOINTMENT_A_VERB = frozenset("""is are am be being comes coming arrives arriving leaves leaving
starts starting finishes finishing returns returning waits waiting""".split())
APPOINTMENT_A_DATE_VERB = frozenset("""closes closing opens opening begins beginning ends ending
starts starting finishes finishing runs running happens arrives arriving leaves leaving""".split())
APPOINTMENT_NOT_A_VERB = frozenset("""bed beds shed sheds red seed feed speed need hundred wed
aged kindred moped""".split())
APPOINTMENT_CORRECTION = frozenset("""sorry no nope nah actually wait oh ah oops rather instead
wrong not""".split())
DAY_REMARK_WORDS = frozenset("""hot cold warm freezing boiling chilly cooler warmer mild sunny
cloudy overcast windy wet rainy foggy misty grey gray bright dull damp humid muggy sticky close
lovely nice horrible awful miserable grim rubbish lousy great good fine better worse busy quiet
long short dark clear beautiful gorgeous stunning glorious pleasant freezing bitter fresh soft
weather rain rains raining snow snowing sun sunshine wind winds windy frost icy ice sleet hail
thunder storm stormy drizzle drizzling pouring showers downpour heatwave freezing""".split())
DAY_REMARK_GLUE = frozenset("""the a an and but its it is was out in up here there very really so
quite too bit rather enough still again today tonight tomorrow now morning afternoon evening all
day week week's end bit lot much more""".split())


def _the_day_described(thing):
    left = [word.strip(",.!;:'\u2019") for word in str(thing or "").lower().split()]
    left = [word for word in left if word and word not in DAY_REMARK_WORDS
            and word not in DAY_REMARK_GLUE]
    return not left


A_DAY_SAID_FIRST = re.compile(
    r"^(?:on\s+|in\s+)?(?:the\s+)?(?:\d{1,2}(?:st|nd|rd|th)?\s+(?:of\s+)?)?"
    r"(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\s+\d{1,2}(?:st|nd|rd|th)?\b", re.I)


_A_COUNT_NOT_A_CLOCK = re.compile(
    r"\b(?:dinner|lunch|breakfast|brunch|supper|tea|meal|table|tables|party|round|booking|"
    r"seats?|covers|guests?|people|plates?|portions?|helpings?|rooms?)\b", re.I)


def _the_thing_said_after_the_day(low, day):
    if day.start() > 4:
        return ""
    rest = low[day.end():].strip(" ,;:-")
    rest = re.sub(r"^(?:on|in|at)\s+", "", rest)
    kept = []
    for word in rest.split():
        bare = word.strip(",.!;:")
        if bare in APPOINTMENT_A_VERB or bare in APPOINTMENT_A_DATE_VERB:
            break
        if len(bare) > 3 and bare.endswith("ed") and bare not in APPOINTMENT_NOT_A_VERB:
            break
        kept.append(word)
    thing = " ".join(kept).strip(" ,;:-")
    thing = re.sub(r"^(?:the|my|our|a|an)\s+", "", thing)
    return thing


def _appointment(text):
    said = " ".join(text.split()).strip(" .,!;:-")
    words = said.split()
    if not words or "?" in said or len(words) > 12:
        return ""
    low = said.lower()
    if APPOINTMENT_OWN_SUBJECT.match(low):
        return ""
    if ASKING.match(low) or APPOINTMENT_PAST.search(low) or NEGATED.search(low):
        return ""
    if SECOND_PERSON.search(low):
        return ""
    clock, day = APPOINTMENT_CLOCK.search(low), APPOINTMENT_DAY.search(low)
    if clock and re.match(r"for\s", clock.group(0), re.I) and _A_COUNT_NOT_A_CLOCK.search(low[:clock.start()]):
        clock = None
    if not clock and not day:
        return ""
    if clock:
        after = low[clock.end():].strip(" ,.;:-")
        if after and not re.match(r"^(?:on\s+)?" + APPOINTMENT_DAY.pattern + r"$", after, re.I):
            return ""
    cut = min([m.start() for m in (clock, day) if m])
    thing = low[:cut].strip(" ,;:-")
    thing = re.sub(r"^(?:the|my|our)\s+", "", thing)
    thing = re.sub(r"\s+(?:is|at|on|for)$", "", thing).strip()
    if not thing and day is not None and cut == day.start():
        thing = _the_thing_said_after_the_day(low, day)
    if not thing or len(thing.split()) > 4:
        return ""
    if _the_day_described(thing):
        return ""
    if TAKE_BACK_WORDS.search(thing):
        return ""
    if thing.split()[0] in APPOINTMENT_NOT_A_THING:
        return ""
    if thing.split()[0].strip(",.!") in APPOINTMENT_CORRECTION:
        return ""
    if not re.search(r"[a-z]{3}", thing):
        return ""
    for word in thing.split():
        if word in APPOINTMENT_PAST_VERB or word in APPOINTMENT_A_VERB:
            return ""
        if len(word) > 3 and word.endswith("ed") and word not in APPOINTMENT_NOT_A_VERB:
            return ""
    if day is not None and re.search(r"\d|" + MONTH_NAMES, day.group(0), re.I):
        if thing.split()[-1].strip(",.!") in APPOINTMENT_A_DATE_VERB:
            return ""
    when = []
    if clock:
        when.append("at " + " ".join(clock.group(1).split()))
    if day:
        day_text = " ".join(day.group(0).split())
        if not re.match(r"^(?:on|this|next|today|tomorrow|tonight)\b", day_text, re.I):
            day_text = "on " + day_text
        when.append(day_text)
    return thing + " " + " ".join(when)


OBLIGATION = re.compile(r"\b(?:have|has|ve|need|needs|got|gotta|must)\s+(?:to\s+)?[a-z]", re.I)


RECURRENCE = re.compile(
    r"\b(?:every|each|most\s+(?:days?|nights?|mornings?|weeks?|weekends?|evenings?)|"
    r"usually|always|never|twice|daily|nightly|weekly|monthly|fortnightly|"
    r"weekdays?|weeknights?|on\s+weekends?|weekends)\b", re.I)


A_CLOCKED_EVENT = re.compile(
    r"\b(?:leaves?|leaving|departs?|departing|starts?|starting|begins?|beginning|arrives?|"
    r"arriving|lands?|landing|gets?\s+(?:in|there|back)|takes?\s+off|checks?\s+in|"
    r"sails?|sailing|flies?|flying|boards?|boarding|opens?|opening|closes?|closing)\b", re.I)


def _coming_up(clause):
    if RECURRENCE.search(clause):
        return False
    if FUTURE.search(clause):
        return True
    if OBLIGATION.search(clause):
        return bool(APPOINTMENT_CLOCK.search(clause) or APPOINTMENT_DAY.search(clause))
    return bool(A_CLOCKED_EVENT.search(clause) and APPOINTMENT_CLOCK.search(clause))


def _dated_plan(text, deed=None):
    if not _coming_up(text):
        return ""
    for clause in _dated_plans(text, deed):
        return clause
    return ""


CLAUSE_SUBJECT = re.compile(
    r"^\W*(?:(?:and|but|so|also|then|oh|ok|okay|well|plus)[\s,]+)*"
    r"(?:my|our|the|his|her|their|i|we|me)\b"
    r"(?:\s+(?!(?:is|are|was|were|am|in|on|at|next|this|tomorrow|tonight|over|for|by|"
    r"before|after)\b)[\w'\u2019.\-]+){0,4}", re.I)
WHEN_OR_WHERE = re.compile(
    r"\b(?:in|on|at|next|this|tomorrow|tonight|over|for|by|from|before|after)\b|"
    r"\b(?:january|february|march|april|may|june|july|august|september|october|november|december)\b",
    re.I)
A_SHARED_VERB = re.compile(r"^(?:is|are|was|were|am)\b", re.I)
CORRECTION_LEAD_RE = re.compile(CORRECTION_LEAD, re.I)
OPENER_WORDS = ("ok", "okay")
OPENER_PUNCTUATION = re.compile(r"[,.:;!?\-\u2013\u2014]\s*$")


def _the_opener_end(said):
    lead = CORRECTION_LEAD_RE.match(said)
    if not lead:
        return 0
    front = lead.group(0)
    if OPENER_PUNCTUATION.search(front):
        return lead.end()
    words = [one for one in re.split(r"[^a-z']+", front.lower()) if one]
    words = [one for one in words if one not in OPENER_WORDS]
    return lead.end() if len(words) >= 2 else 0



def without_the_correction_opener(text):
    said = " ".join(str(text or "").lower().split())
    end = _the_opener_end(said)
    if not end:
        return ""
    return said[end:].strip(" ,.;:\t\u2013\u2014")


def is_a_correction_opener(text):
    said = " ".join(str(text or "").lower().split())
    if not said:
        return False
    lead = CORRECTION_LEAD_RE.match(said + " ")
    return bool(lead and lead.end() > len(said))


def _said_after_the_subject(clause):
    match = CLAUSE_SUBJECT.match(clause)
    rest = clause[match.end():] if match else clause
    where = WHEN_OR_WHERE.search(rest)
    return (rest[:where.start()] if where else rest).strip(" ,")


def _the_verb_for(body, subject):
    first = body.split()[0].lower() if body.split() else ""
    person = str(subject or "").strip().lower()
    plural = person in ("we", "they", "you") or " and " in person
    if not plural:
        if first == "am":
            return "is" + body[2:]
        if first in ("are", "were"):
            return ("is" if first == "are" else "was") + body[len(first):]
    if person == "i" and first == "is":
        return "am" + body[2:]
    return body


def _with_the_verb_lent(clause, earlier):
    if not clause or not earlier or _said_after_the_subject(clause):
        return clause
    body = _said_after_the_subject(earlier)
    if not A_SHARED_VERB.match(body):
        return clause
    match = CLAUSE_SUBJECT.match(clause)
    subject = match.group(0) if match else ""
    body = _the_verb_for(body, subject)
    rest = clause[match.end():].lstrip() if match else clause
    if not rest:
        return clause
    return (clause[:match.end()].rstrip() + " " + body + " " + rest).strip()


def _dated_plans(text, deed=None):
    if not FUTURE.search(text) and not _coming_up(text):
        return
    at = 0
    earlier = ""
    for piece in re.split(r"(?<=[.!?])\s+|,|;|\s+(?:but|and|so|then)\s+", text):
        start = text.find(piece, at) if piece else -1
        ahead = text[:start] if start != -1 else ""
        if start != -1:
            at = start + len(piece)
        clause = " ".join(piece.split()).strip(" ,.;:-!")
        if not clause:
            continue
        opened = CORRECTION_LEAD_RE.sub("", clause, count=1).strip()
        if opened and OWN.match(opened):
            clause = opened
        joined = _with_the_person_joined_to_the_subject(ahead, clause)
        if not (OWN.match(joined) or OWN.match(clause)
                or THE_THING_HAS_A_DAY.match(clause)) or "?" in joined:
            continue
        clause = _with_the_verb_lent(joined, earlier)
        if not _coming_up(clause) or PAST.search(clause):
            continue
        if ASKING.match(re.sub(r"^(?:ok(?:ay)?[, ]+|and |so |but |also |well |oh )+", "", clause,
                               flags=re.I)):
            continue
        if SECOND_PERSON.search(clause):
            continue
        if NEGATED.search(clause):
            continue
        if _how_they_are(clause) or _how_their_things_are(clause):
            continue
        if a_deed(clause):
            if deed is not None:
                deed.append(clause)
            continue
        words = clause.split()
        if len(words) < 3 or len(words) > 18:
            continue
        if not (re.search(r"\b(?:my|our|i|we|i'm|im|me)\b", clause, re.I)
                or THE_THING_HAS_A_DAY.match(clause)):
            continue
        if len(re.findall(r"\b(?:i|my|we|our)\b", clause, re.I)) > 3:
            continue
        earlier = clause
        yield clause


THE_THING_HAS_A_DAY = re.compile(
    r"^the\s+[a-z][a-z' \-]{1,30}?\s+(?:is|are|was|were)\s+"
    r"(?:due|on|booked|scheduled|expected|renewed)\b"
    r"|^the\s+[a-z][a-z' \-]{1,30}?\s+(?:expires?|expiring|runs?\s+out|renews?)\b", re.I)


JOINED_PERSON = r"(?:me|i|(?:my|our|the|his|her|their)\s+[a-z'\u2019]{2,20})"
SUBJECT_JOIN = re.compile(
    r"^(?:and|but|so|also|well|ok|okay|oh|then|plus)?[\s,]*"
    r"(?:" + JOINED_PERSON + r")\s+and(?:\s+(?:me|i))?"
    r"(?:\s+" + JOINED_PERSON + r")?$", re.I)


def _with_the_person_joined_to_the_subject(ahead, clause):
    person = " ".join((ahead or "").split())
    if not person or not SUBJECT_JOIN.match(person):
        return clause
    return person + " " + clause



SELF_INTRO = re.compile(
    r"^\W{0,2}(?:(?:hi+|hey+|hello+|hiya)\b[\s,]*)*(?:im|i'm|i am)\s+"
    r"[a-z'\u2019\-]{2,}(?:\s+[a-z'\u2019\-]{2,})?\s*,(?P<rest>[^?]*)$", re.I)
OTHER_START = frozenset("my our his her their the it we they she he there this that".split())
NOT_A_PART = frozenset("""what how why when where who which should can could do does did is are
was were will would shall may might help thanks thank sorry please so but and if maybe just""".split())


CONTINUATION_SPLIT = re.compile(r",|;|\s+(?:and|but)\s+", re.I)
PERSON_SUBJECT = frozenset("""i im i'm i've ive i'd id we we're we've""".split())
ANY_SUBJECT = PERSON_SUBJECT | frozenset("""my our his her their he she it they there this that
you your""".split())


def _continued_parts(text):
    clauses, start = [], 0
    for match in CONTINUATION_SPLIT.finditer(text):
        clauses.append(text[start:match.start()])
        start = match.end()
    clauses.append(text[start:])
    words = clauses[0].replace(",", " ").split()
    subject = "person" if words and words[0].lower() in PERSON_SUBJECT else None
    if subject == "person" and WISHING.search(" ".join(words)):
        return []
    parts = []
    for clause in clauses[1:]:
        clause = clause.strip(" .!?,")
        if not clause:
            continue
        first = clause.split()[0].lower().strip(",")
        if first in ANY_SUBJECT:
            subject = "person" if first in PERSON_SUBJECT else "other"
            continue
        if subject != "person" or first not in CONTINUATION_VERB:
            continue
        for lead in ("i ", "i'm "):
            read = _extract(lead + clause)
            read.pop("name", None)
            read = {key: value for key, value in read.items() if key in CONTINUATION_KEYS}
            if read:
                parts.append(read)
                break
    return parts


WISHING = re.compile(
    r"\b(?:want|wanna|wish|hope|might|may|could|would|should|plan|planning|thinking|thought|"
    r"going to|gonna|used to|trying|try|like to|love to|if|unless|pretend|imagine)\b", re.I)


CONTINUATION_VERB = frozenset("""live work have got am 'm was were come comes came moved move
drive study teach train run play commute rent own need want speak hold""".split())
CONTINUATION_KEYS = frozenset("""places home city town job job_frame age pets allergies people diet
diets conditions name country county""".split())


SAME_PERSON_CLAUSE = re.compile(
    r"^\W*(?:she|he|they)\s+(?P<rest>[a-z0-9'\u2019 ]{3,80}?)\s*$", re.I)
SAME_PERSON_SPLIT = re.compile(r"[.!?;]+|,\s*|\s+(?:and|but|also|n)\s+", re.I)


def _the_relation_named(clause):
    for relation in RELATIONS:
        if re.search(r"\b(?:my|our)\s+" + relation + r"(?:'s|s)?\b", clause, re.I):
            return relation
    return None


def _a_clause_about_the_same_person(text):
    clauses = [part for part in SAME_PERSON_SPLIT.split(text or "") if part.strip()]
    if len(clauses) < 2:
        return []
    named = _the_relation_named(clauses[0])
    if not named and not any(_the_relation_named(clause) for clause in clauses[1:]):
        return []
    parts = []
    for clause in clauses[1:]:
        found = SAME_PERSON_CLAUSE.match(clause.strip())
        if not found:
            named = _the_relation_named(clause) or named
            continue
        if not named:
            continue
        read = _extract("my " + named + " " + found.group("rest").strip())
        kept = []
        for entry in read.get("others") or []:
            if not (isinstance(entry, dict) and entry.get("who")
                    and str(entry["who"]).lower() == named.lower()):
                continue
            entry = {key: value for key, value in entry.items() if key != "name"}
            if any(value for key, value in entry.items() if key != "who"):
                kept.append(entry)
        if kept:
            parts.append({"others": kept})
    return parts


def _self_intro_parts(text):
    match = SELF_INTRO.match(text.strip())
    if not match:
        return []
    parts = []
    for piece in re.split(r",|\band\b|;", match.group("rest")):
        piece = piece.strip(" .!?")
        words = piece.split()
        if not words or set(w.lower() for w in words[:1]) & (OTHER_START | NOT_A_PART):
            continue
        leads = ("",) if words[0].lower() in PERSON_SUBJECT else ("i'm ", "i ")
        for lead in leads:
            read = _extract(lead + piece)
            if read:
                parts.append(read)
                break
    return parts



def _same_thing(one, other):
    one = _tidy(str(one)).lower().strip()
    other = _tidy(str(other)).lower().strip()
    if not one or not other:
        return False
    return one == other or one.rstrip("s") == other.rstrip("s")


def _is_only_the_take_back(value, gone):
    if not gone:
        return False
    for fact, said in gone.items():
        if _same_thing(value, fact):
            return True
        for item in (said if isinstance(said, list) else [said]):
            if isinstance(item, dict):
                item = item.get("animal") or item.get("name") or ""
            if str(item) == EVERYTHING:
                return True
            if _same_thing(value, item):
                return True
    return False


BOT_NAME = re.compile(
    r"\b(?:call|calling|callin|name|naming|named)\s+(?:you|u)\s+([A-Za-z][a-z'-]{1,19})\b"
    r"|\byour name(?:'s| is| will be)\s+([A-Za-z][a-z'-]{1,19})\b", re.I)
BOT_NAME_ASKED = re.compile(r"\bwhat\b|\bwhich\b|\bwho\b", re.I)
BOT_NAME_TAG = re.compile(r"\bright\s*\?|\bam i right\b|\barent you\b|\bisnt it\b", re.I)
BOT_NAME_TITLE = frozenset("mr mrs ms miss mx dr doctor sir lady lord captain prof professor "
                           "prince princess saint dame".split())
BOT_NAME_STOP = frozenset("""when then tomorrow tonight today later back after before if once until
soon now again please ok okay mate guys someone somebody him her them it me you us everyone
all every one two three four five six seven eight nine ten eleven twelve
day week month year morning evening night weekend christmas
at in on by around about this next last half noon midnight oclock o'clock
really very so quite pretty much always never just only definitely
short tall long great cool funny weird silly fine good bad better best worse worst wrong right
hard easy nice lovely rubbish dumb stupid same different strange odd lovely amazing awesome
useless perfect brilliant terrible awful""".split())


BOT_NAME_ASK = re.compile(
    r"\bwhat(?:'s|s| is| was)?\s+your name\b|\byour name (?:again|now)\b"
    r"|\bwhat (?:should|shall|do|can|would) (?:i|we|they) (?:call|name) you\b"
    r"|\bwhat(?:'s|s| is| was) (?:it|that) (?:i|we) (?:call|called) you\b"
    r"|\b(?:do|have) you (?:got |have )?(?:a |any )?(?:name|nickname)\b"
    r"|\bwhat are you called\b"
    r"|\bcall you again\b", re.I)


def bot_name(text):
    if not isinstance(text, str):
        return None
    match = BOT_NAME.search(text)
    if not match:
        return None
    if BOT_NAME_ASKED.search(text[:match.start()]) or BOT_NAME_TAG.search(text):
        return None
    word = (match.group(1) or match.group(2) or "").strip()
    if not word or word.lower() in BOT_NAME_STOP or word.lower() in NOT_A_NAME:
        return None
    if word.lower() in BOT_NAME_TITLE:
        more = re.match(r"\s+([A-Za-z][a-z'-]{1,19})\b", text[match.end():])
        if more:
            word = word + " " + more.group(1)
    if not all(NAME_WORD.match(part) for part in word.split()):
        return None
    return word[:1].upper() + word[1:] if word.islower() else word


CORRECTION_OPENER = re.compile(r"^\s*(?:(?:no|nope|sorry|actually|wait|ah|oh|i\s+mean(?:t)?|"
                               r"make\s+that|or\s+rather)[,.\s!\u2014-]+)+", re.I)
SUBJECT_OPENERS = ((re.compile(r"^\s*(?:i'?m|i\s+am|im)\b", re.I), "im"),
                   (re.compile(r"^\s*i\s+work(?:s|ed)?\s+as\b", re.I), "i work as"),
                   (re.compile(r"^\s*i\s+work(?:s|ed)?\s+(?:in|at|for)\b", re.I), "i work in"),
                   (re.compile(r"^\s*i\s+live(?:s|d)?\s+in\b", re.I), "i live in"),
                   (re.compile(r"^\s*(?:i\s+have|i'?ve\s+got|i\s+have\s+got)\b", re.I),
                    "i have"))


def a_correction_without_a_subject(text, before):
    low = str(text or "").strip().lower()
    if not low or not any(word in low for word in TAKE_BACK):
        return {}
    opener = CORRECTION_OPENER.match(low)
    if not opener:
        return {}
    rest = low[opener.end():].strip()
    if not rest or not any(word in rest for word in TAKE_BACK):
        return {}
    before = str(before or "").strip().lower()
    for shape, frame in SUBJECT_OPENERS:
        if shape.search(before):
            found = extract(frame + " " + rest)
            if found:
                return found
    return {}


REPORTED = re.compile(
    r"^\W{0,3}(?:(?:ok|okay|so|and|but|well|no|nope|look|see|yes|yeah|actually|honestly|literally|"
    r"i\s+mean)[, ]+)*"
    r"(?:(?:i|we)\s+(?:already\s+|did\s+|just\s+|definitely\s+)?(?:said|told\s+you|mentioned)|"
    r"like\s+i\s+said|as\s+i\s+said|to\s+repeat)\b[\s,:]*(?P<rest>[^?]*\S)", re.I)


def _reported_clause(text):
    text = (text or "").strip()
    if not text or "?" in text:
        return None
    if (CORRECTION_SAID.search(text) or CORRECTION.search(text)
            or CORRECTION_PAIR.search(text) or CORRECTION_MAKE.search(text)):
        return None
    match = REPORTED.match(text)
    if not match:
        return None
    rest = match.group("rest").strip(" ,.;:-")
    return rest or None


def _paid_by_a_period(text, end):
    qualifier = INCOME_QUALIFIER.match(text[end:])
    return bool(INCOME_PERIOD.match(text, end + (qualifier.end() if qualifier else 0)))


def _a_years_pay(figure):
    said = str(figure or "")
    if re.search(r"\d[\d,.]*\s?(?:k|grand|thousand)\b", said, re.I):
        return True
    return len(re.sub(r"[^\d]", "", said)) >= 4


def extract(text, question=False):
    reported = _reported_clause(text)
    if reported:
        if _extract(reported, question):
            text = reported
    found = _extract(text, question)
    given = bot_name(text)
    if given:
        found["bot_name"] = given
    if a_limit_on_the_plan(text) is not None and not COMMITS_TO.search(text):
        found.pop("plan", None)
        found.pop("plans", None)
        correction = found.get("correction")
        if isinstance(correction, dict) and not correction.get("from"):
            found.pop("correction", None)
    for part in (_self_intro_parts(text) + _continued_parts(text)
                 + _a_clause_about_the_same_person(text)):
        for key, value in part.items():
            if key == "name":
                continue
            if key in ("places", "others"):
                found[key] = _union(found.get(key), value)
                if key == "others":
                    found[key] = _one_entry_per_person(found[key])
            elif key not in found:
                found[key] = value
    if found.get("others"):
        for entry in found["others"]:
            if isinstance(entry, dict) and entry.get("who") in SPOKEN_RELATION:
                entry["who"] = SPOKEN_RELATION[entry["who"]]
        found["others"] = _one_entry_per_person(found["others"])
    if not found.get("correction") and found.get("drop") is None:
        marked = _the_marker_in_front(text, question)
        if marked is not None:
            again = _extract(marked, question)
            for key in ("correction", "drop"):
                if again.get(key) is not None:
                    found[key] = again[key]
    return found


SAYS_WHAT_THEY_ARE = (("i", "am"), ("im",), ("i'm",), ("i", "have"), ("i", "work"),
                      ("i", "live"), ("i", "take"), ("i", "get"))
THEIR_NAME = frozenset(("name",))
THEIR_PLAN = frozenset(("plan", "plans"))


def about_themselves(said):
    words = tuple(word.lower() for word in str(said or "").split())
    if not any(words[:len(lead)] == lead for lead in SAYS_WHAT_THEY_ARE):
        return None
    kept = extract(said)
    if not kept or set(kept) <= THEIR_NAME or set(kept) <= THEIR_PLAN:
        return None
    return kept


def _one_entry_per_person(entries):
    out = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        who = str(entry.get("who") or "").lower()
        kept = None
        if who and not entry.get("pronoun"):
            for one in out:
                if str(one.get("who") or "").lower() != who or one.get("pronoun"):
                    continue
                mine = str(one.get("name") or "").lower()
                theirs = str(entry.get("name") or "").lower()
                if mine and theirs and mine != theirs:
                    continue
                kept = one
                break
        if kept is None:
            out.append(dict(entry))
            continue
        for key, value in entry.items():
            if key in ("who", "pronoun"):
                continue
            if key == "name":
                mine = str(one.get("name") or "")
                if not mine or (mine[:1].islower() and str(value)[:1].isupper()):
                    one["name"] = value
                continue
            if key == "age":
                if one.get("to_come") == value:
                    continue
                if one.get("turns") and not one.get("age"):
                    one["age"] = value
                    continue
                if isinstance(one.get("age"), int) and isinstance(value, int) and one["age"] != value:
                    if not one.get("turns"):
                        one["age"] = value
                    continue
                one["age"] = value
                continue
            if key in ("turns", "to_come"):
                if not one.get("turns"):
                    one["turns"] = value
                    if key == "to_come" and one.get("age") != value:
                        one["to_come"] = value
                continue
            if not isinstance(value, (list, tuple)):
                one.setdefault(key, value)
                continue
            have = one.setdefault(key, [])
            if isinstance(have, list):
                have.extend(item for item in value if item not in have)
    return out


def _union(one, other):
    out = list(one or [])
    for value in other or []:
        if value not in out:
            out.append(value)
    return out


def _the_pronoun(text, pos):
    start = 0
    for match in CLAUSE_BREAK.finditer(text, 0, pos):
        start = match.end()
    found = PRONOUN_SUBJECT.search(text, start, pos)
    if not found:
        return ""
    word = found.group("pron").lower()
    return {"her": "she", "him": "he", "them": "they", "shes": "she", "hes": "he",
            "theyre": "they"}.get(word, word)


RELATION_SAID = re.compile(
    r"\b(?:my|our)\s+(?P<who>" + "|".join(sorted(RELATIONS, key=len, reverse=True))
    + r")(?P<plural>s?)(?P<inlaw>\s+in\s+laws?)?\b", re.I)


def _the_person_the_pronoun_is(text, pos, pronoun):
    fits = SHE if pronoun == "she" else HE if pronoun == "he" else frozenset()
    if not fits:
        return ""
    who = ""
    for match in RELATION_SAID.finditer(text, 0, pos):
        word = a_person_word(" ".join((match.group("who")
                                       + (match.group("inlaw") or "")).split()).lower())
        if who and word != who:
            return ""
        who = word
    if not who:
        return ""
    parts = [part for part in re.split(r"[-\s]+", who) if part]
    return who if who in fits or any(part in fits for part in parts) else ""


NAME_THEN_THE_VERB = re.compile(
    r"^\W*(?:(?:and|but|so|then|also|oh|ok|okay|well|now|btw|hey|hi|quick)\W+)?"
    r"(?P<name>[A-Za-z][A-Za-z'\-]{1,19})\s+(?:is|was|has|had|isnt|wasnt|hasnt|cant|cannot|"
    r"doesnt|dont|didnt|never|only|gets|got|became)\b", re.I)


def _a_name_opening_the_clause(clause):
    found = NAME_THEN_THE_VERB.match(clause or "")
    if not found:
        return ""
    name = found.group("name")
    low = _a_person_word(name)
    if low in NOT_A_PERSON_WORD or low in RELATIONS or low in DIET_GROUP \
            or low in A_PRONOUN_NOT_A_NAME:
        return ""
    if not (_may_be_a_name(name) and _name_after_a_title(name)):
        return ""
    return name


def _the_name_in_front(text, pos):
    start = 0
    for match in CLAUSE_BREAK.finditer(text, 0, pos):
        start = match.end()
    clause = text[start:pos]
    who, name = _the_person_without_a_relation(clause)
    if name and not who:
        return name
    if not who:
        opening = _a_name_opening_the_clause(clause)
        if opening:
            return opening
    if who:
        found = re.search(r"\b(?:" + "|".join(sorted(OTHER_NOUNS, key=len, reverse=True))
                          + r")(?:\s+in\s+laws?)?s?\s+(?P<name>[A-Za-z][A-Za-z'\-]{1,19})\s*$",
                          clause, re.I)
        if found:
            name = found.group("name")
            low = name.lower().strip("'")
            if (low not in NOT_A_PERSON_WORD and low not in RELATIONS
                    and _may_be_a_name(name) and _name_after_a_title(name)):
                return name
    return ""


def _a_person(text, pos, who):
    if who:
        return {"who": who}
    named = _the_name_in_front(text, pos)
    if named:
        return {"name": named}
    pronoun = _the_pronoun(text, pos)
    if not pronoun:
        return {}
    person = _the_person_the_pronoun_is(text, pos, pronoun)
    if person:
        return {"who": person}
    return {"pronoun": pronoun}


def _same_person(seen, entry):
    who = seen.get("who") or ""
    other = entry.get("who") or ""
    if who or other:
        mine = str(seen.get("name") or "").lower()
        theirs = str(entry.get("name") or "").lower()
        return who == other and (not mine or not theirs or mine == theirs)
    return bool(seen.get("pronoun")) and seen.get("pronoun") == entry.get("pronoun")


NAME_AND_A_FIGURE = re.compile(
    r"^\W*(?:(?:no|nope|sorry|actually|wait|hold on|correction|i mean|and|but|so|oh)\W+)*"
    r"(?P<name>[A-Za-z][a-z'-]{1,19})(?:'s| is| was)\s+(?:now\s+|already\s+|actually\s+)?"
    r"(?P<age>\d{1,3})(?:\s*(?:years?|yrs?)(?:\s+old)?)?(?:\s+(?:now|already|today))?\W*$", re.I)

NOT_A_NAME_FIGURE = frozenset("""i you he she it we they there that this here what who which
the a an my your his her our their its mine yours hers ours theirs and but so now then just only
still really also too very time day week month year morning evening night today tomorrow
yesterday half""".split())


def _a_name_and_a_figure(text):
    match = NAME_AND_A_FIGURE.match(" ".join(str(text or "").split()))
    if not match:
        return None
    name = match.group("name")
    low = name.lower()
    if (low in NOT_A_NAME_FIGURE or low in NOT_A_NAME or low in NOT_A_NAME_THING
            or low in NOT_A_NAME_STATE
            or low in MONTHS or low in DAYS):
        return None
    age = int(match.group("age"))
    if not 0 < age <= 120:
        return None
    shown = name[:1].upper() + name[1:]
    return {"name": shown, "age": age}


BODY_PARTS = ("knee", "knees", "back", "shoulder", "shoulders", "hip", "hips", "ankle", "ankles",
              "foot", "feet", "heel", "heels", "calf", "calves", "shin", "shins", "thigh",
              "thighs", "hamstring", "hamstrings", "wrist", "wrists", "elbow", "elbows", "hand",
              "hands", "finger", "fingers", "thumb", "neck", "head", "chest", "stomach", "tummy",
              "tooth", "teeth", "ear", "ears", "eye", "eyes", "arm", "arms", "leg", "legs", "toe",
              "toes", "jaw", "rib", "ribs", "groin", "abdomen", "spine", "tailbone", "collarbone",
              "achilles", "quad", "quads", "glute", "glutes", "arch")
BODY_PART = re.compile(r"\b(" + "|".join(BODY_PARTS) + r")\b", re.I)
BODY_HURTS = re.compile(r"\b(?:hurt|hurts|hurting|sore|ache|aches|aching|achy|pain|painful|"
                        r"injur\w*|twinge|stiff|swollen|swelling|niggle|flare[sd] up|"
                        r"killing me|playing up)\b", re.I)
BODY_LATERAL = re.compile(r"\b(left|right|both)\s+(?:(?:outer|inner|lower|upper|front|back)\s+)?"
                          r"(?:" + "|".join(BODY_PARTS) + r")\b", re.I)
BODY_PLACE = re.compile(r"\b(?:on|in|at|to|round|around)\s+(?:the|my|his|her|their|its)\s+"
                        r"(outside|inside|front|lower|upper|top|bottom|inner|outer)\b", re.I)


SOMEONE_ELSE = re.compile(r"\b(?:my|our|the)\s+(?:(?:little|older|youngest|eldest|baby|big|"
                          r"grown[- ]up|step)\s+)?(?:son|sons|daughter|daughters|child|children|"
                          r"kid|kids|boy|boys|girl|girls|baby|babies|toddler|mum|mums|mom|mother|"
                          r"dad|dads|father|husband|wife|partner|ex|boyfriend|girlfriend|brother|"
                          r"brothers|sister|sisters|friend|friends|mate|mates|nephew|niece|cousin|"
                          r"grandma|grandad|granny|gran|nan|nanna|aunt|aunty|uncle|in-?law|"
                          r"dog|cat|puppy|kitten|patient|client|customer|colleague|boss)\b"
                          r"(?:'s|s')?", re.I)
A_PART_HANDED_OVER = re.compile(r"\b(?:his|her|their|its)\s+(?:\w+\s+){0,2}?(?:"
                                + "|".join(BODY_PARTS) + r")\b", re.I)


MY_OWN_PART = re.compile(r"\b(?:my|our)(?:\s+\w+){0,2}\s+$", re.I)
THE_PART_HURTS = re.compile(r"^\s*(?:'s|s)?\s*(?:is|are|was|were|has|have|have been|has been|"
                            r"keeps)?\s*(?:killing|hurting|hurts|sore|aching|aches|ache|painful|"
                            r"stiff|swollen|playing|giving|in pain|bad|killing me)\b", re.I)
THE_PERSON_SAYS = re.compile(r"^(?:ok(?:ay)?[, ]+|and |so |but |well |oh |also )*"
                             r"(?:i|i'm|im|i've|ive|we|we're|were|we've|weve)\b", re.I)
A_PLACE_ON_IT = re.compile(r"^(?:it|its|it's|that|that's|this|the (?:pain|ache|hurt|soreness))\b",
                           re.I)


def _tied_to_them(part, low):
    before = low[:part.start()]
    after = low[part.end():]
    if MY_OWN_PART.search(before):
        return True
    if THE_PART_HURTS.match(after):
        return True
    clause = re.split(r"[,;.!?]|\s+(?:and|but|so|then)\s+", before)[-1]
    if THE_PERSON_SAYS.match(clause.strip()) and BODY_HURTS.search(low):
        return True
    if A_PLACE_ON_IT.match(low) and BODY_PLACE.search(low):
        return True
    return False


def _theirs(part, low):
    part_at = part.start()
    owner = None
    for found in SOMEONE_ELSE.finditer(low):
        if found.start() < part_at:
            owner = found
    if owner is not None:
        between = low[owner.end():part_at]
        if not re.search(r"\b(?:my|our|i|me|mine|myself)\b", between):
            return False
    for other in A_PART_HANDED_OVER.finditer(low):
        if other.end() <= part_at + 1 and other.start() < part_at:
            return False
    return _tied_to_them(part, low)


def the_part_it_hurts(text):
    if not isinstance(text, str):
        return None
    low = " ".join(text.lower().split())
    part = None
    for found in BODY_PART.finditer(low):
        if _theirs(found, low):
            part = found
            break
    if part is None:
        return None
    lateral = BODY_LATERAL.search(low)
    place = BODY_PLACE.search(low)
    if not (BODY_HURTS.search(low) or lateral or place):
        return None
    if re.search(r"\b(?:no|not|never)\b[^.]{0,20}" + re.escape(part.group(1)) + r"\b", low):
        return None
    if not lateral and not place and re.search(r"\b" + re.escape(part.group(1)) +
                                              r"\s+(?:door|room|garden|yard|seat|window|wheel|"
                                              r"teacher|line|table|of the house)\b", low):
        return None
    held = {"part": part.group(1).lower(), "said": " ".join(text.split())}
    if lateral:
        held["side"] = lateral.group(1).lower()
    if place:
        held["place"] = place.group(1).lower()
    return held


def _extract(text, question=False):
    found = {}
    hurt = the_part_it_hurts(text)
    if hurt:
        found["hurts"] = hurt
    text = _the_numbers_in_words(text)
    diet = VEGETARIAN.search(text)
    name = _name(text)
    if name and diet and re.match(r"(?:i|we)", diet.group(1).lower()):
        if diet.group(2).lower().replace("-", " ").startswith(_finish(name) + " "):
            name = None
    if name:
        found["name"] = name
    job, city, frame = _job_and_city(text, name, question)
    if not job and CHANGED_WORK.search(text):
        moved = WORK_NOW.search(text)
        if moved:
            place = _finish(moved.group(3))
            if place and place not in JOB_STOP and len(place.split()) <= 3:
                job = place
                frame = " ".join(part for part in (moved.group(1), moved.group(2)) if part)
    if job:
        found["job"] = job
        if frame:
            found["job_frame"] = frame
    car = _car(text)
    if car:
        found["car"] = car
    places, home, home_said = _places(text)
    if home is None:
        near = HOME_LOOSE.search(text)
        if near and near.group(1).split()[0].lower() not in NOT_PLACES:
            home = near.group(1)
            if home not in places:
                places.append(home)
    origin = _from_place(text)
    if origin:
        found["from"] = origin
        if not home and origin not in places:
            places.append(origin)
    born = _born_place(text)
    if born:
        found["born"] = born
    for place in places:
        found.setdefault("places", []).append(place)
    if home and not city:
        city = home
        found["home"] = home_said or True
    if city and city not in found.get("places", []):
        found.setdefault("places", []).append(city)
    if city:
        found["city"] = city
    own = _own_states(text)
    if own:
        found.update(own)
    allergies, others = _allergies(text)
    if allergies:
        found["allergies"] = allergies
    for entry in _other_diets(text):
        known = next((seen for seen in others if _same_person(seen, entry)), None)
        if known is None:
            others.append(entry)
        else:
            known.setdefault("diet", entry["diet"])
    for entry in _other_conditions(text):
        known = next((seen for seen in others if _same_person(seen, entry)), None)
        if known is None:
            others.append(entry)
        else:
            known.setdefault("condition", entry["condition"])
    for entry in _other_jobs(text):
        known = next((seen for seen in others if _same_person(seen, entry)), None)
        if known is None:
            others.append(dict(entry))
        else:
            known.setdefault("job", entry["job"])
    for entry in _other_states(text):
        known = others[-1] if others and others[-1]["who"] == entry["who"] else None
        if known is None:
            others.append(dict(entry))
        else:
            for key, value in entry.items():
                known[key] = value
    for entry in _other_ages(text):
        known = next((seen for seen in others if _same_person(seen, entry)), None)
        if known is None:
            others.append(dict(entry))
        else:
            if entry.get("ages") or known.get("ages"):
                merged = _ages_held(known) + [age for age in _ages_held(entry)
                                              if age not in _ages_held(known)]
                held = _ages_held(entry)
                if held and len(held) >= len(_ages_held(known)):
                    merged = held
                known.pop("age", None)
                known["ages"] = merged
                if len(merged) == 1:
                    known["age"] = known.pop("ages")[0]
            else:
                known["age"] = entry["age"]
                if entry.get("turns"):
                    known["turns"] = entry["turns"]
                else:
                    known.pop("turns", None)
            if entry.get("name") and not known.get("name"):
                known["name"] = entry["name"]
    for entry in _a_relations_name(text):
        known = next((seen for seen in others if _same_person(seen, entry)), None)
        if known is None:
            others.append(dict(entry))
        else:
            known["name"] = entry["name"]
    for entry in _relation_facts(text):
        who = entry.get("who") or entry.get("pronoun") or ""
        known = None
        for seen in others:
            seen_who = seen.get("who") or seen.get("pronoun") or ""
            if (entry.get("name") and seen.get("name")
                    and str(entry["name"]).lower() != str(seen["name"]).lower()):
                continue
            if who and (seen_who == who
                        or (not seen_who and entry.get("pronoun") and not seen.get("who"))):
                known = seen
                break
        if known is None:
            others.append(entry)
            continue
        for key, value in entry.items():
            if key in ("who", "pronoun"):
                known[key] = known.get(key) or value
            else:
                known.setdefault(key, value)
    entry = _a_name_and_a_figure(text)
    if entry:
        known = next((seen for seen in others
                      if str(seen.get("name") or "").lower() == entry["name"].lower()), None)
        if known is None:
            others.append(dict(entry))
        else:
            known["age"] = entry["age"]
            known.pop("months", None)
            known.pop("ages", None)
    if others:
        for entry in others:
            for key in ("name", "age", "months"):
                if key in entry:
                    who = entry.get("who")
                    if who and who not in found.get("people", []):
                        found.setdefault("people", []).append(who)
                    break
        found["others"] = others
    if diet and re.match(r"(?:i|we)", diet.group(1), re.I):
        eating = " ".join(diet.group(2).lower().replace("-", " ").split())
        found["diet"] = DIET_NAMES.get(eating, eating)
    named = DIET_NAMED.search(text)
    if named and "diet" not in found:
        found["diet"] = " ".join(named.group(1).lower().split()).replace(" ", "-")
    underway = DIET_UNDERWAY.search(text)
    if underway and "diet" not in found:
        if underway.group("named"):
            found["diet"] = " ".join(underway.group("named").lower().split()).replace(" ", "-")
        else:
            found["diet"] = "on a diet"
    doing = _a_way_of_eating_said_with_a_verb(text)
    if doing and "diet" not in found:
        found["diet"] = doing
    bare = DIET_BARE.search(text)
    if bare and "diet" not in found:
        found["diet"] = "-".join(bare.group("bare").lower().replace("-", " ").split())
    meat = NO_MEAT.search(text)
    if meat:
        avoided = _finish(meat.group(1))
        if avoided in NO_EAT_QUALIFIER:
            rest = _finish(text[meat.end():].split()[0]) if text[meat.end():].split() else ""
            if rest in MEAT:
                avoided = avoided + " " + rest
        if avoided and avoided.lower().split()[0] not in _QUANTITY_WORDS \
                and not set(avoided.split()) & ALLERGY_STOP:
            found["diet"] = "no " + avoided
            if MEAT & set(avoided.replace(",", " ").split()):
                found["no_meat"] = True
    if not found.get("diet"):
        drank = _the_drink_they_do_not_take(text)
        if drank:
            found["diet"] = "no " + drank
    condition = CONDITION.search(text)
    if condition:
        found["condition"] = " ".join(condition.group(1).lower().split())
    pets = _pets(text, question)
    if pets:
        found["pets"] = pets
    owned = _owns(text)
    if owned:
        found["owns"] = owned
    tastes = [] if found.get("diet") else taste.read_all(text)
    if tastes:
        found["tastes"] = tastes
    budget = (BUDGET.search(text) or SPEND_BUDGET.search(text) or SPEND_FOR.search(text)
              or INTENDED_SPEND.search(text) or THE_THING_MAY_COST.search(text)
              or ALL_I_CAN_DO.search(text)
              or ONLY_HAVE.search(text) or SPEND_BUDGET_NOW.search(text)
              or STRETCH_BUDGET.search(text)
              or BARE_BUDGET.search(text) or BUDGET_ASKED.search(text)
              or BUDGET_THOUGHT.search(text) or CEILING_BUDGET.search(text))
    if not budget:
        money = INCOME.search(text)
        if money and not _paid_by_a_period(text, money.end()):
            money = None
        if not money:
            bare = INCOME_BARE.search(text)
            if bare and _paid_by_a_period(text, bare.end()):
                figure = bare.group(1).split()[-1]
                if sum(ch.isdigit() for ch in figure) >= 3:
                    money = bare
        if not money:
            for a_year in INCOME_A_YEAR:
                year = a_year.search(text)
                if (year and _a_years_pay(year.group(1))
                        and not text[year.end():].strip(" .,;!?-").strip()):
                    money = year
                    break
        if money and INCOME_RATE.match(text, money.end()):
            money = None
        budget = money
    if budget and subject(text, budget.start())[0] != "other":
        said_budget = " ".join(budget.group(1).split()).rstrip(".,;:")
        if budget.re is CEILING_BUDGET:
            said_budget = "no more than " + said_budget
        found["budget"] = said_budget
    elif not question and vague_budget(text) and subject(text, 0)[0] != "other":
        found["budget"] = vague_budget(text)
    kids = kid_count(text)
    if kids is not None:
        found["kids"] = kids
    age = AGE.search(text) or MY_AGE.search(text)
    if age:
        found["age"] = int(age.group(1))
    tall = _how_tall(text)
    if tall:
        found["height"] = tall
    birthday = BIRTHDAY.search(text)
    if birthday and subject(text, birthday.start())[0] != "other":
        date = _a_birthday_date(birthday.group(1))
        if date:
            found["birthday"] = date
    weight = WEIGH.search(text) or WEIGH_IM.search(text) or WEIGH_MY.search(text)
    if weight and subject(text, weight.start())[0] != "other":
        unit = _weight_unit(weight.group(2))
        if unit:
            found["weight"] = weight.group(1) + " " + unit
            if str(found.get("age")) == weight.group(1):
                found.pop("age", None)
    relations = _people(text)
    if relations:
        found["people"] = relations
    moved = _date_change(text)
    plan = PLAN.search(text)
    if plan and _asks_about_the_plan(text, plan.start()):
        plan = None
    if (plan and _GOT_A.search(plan.group(0)) and not FUTURE.search(text)
            and not _GOT_TO.search(text)):
        plan = None
    if plan and re.match(r"^to\s+(?:go|leave|head off|set off|get going|dash)\b",
                          _plan_text(text, plan.end()), re.I) and _FAREWELL.search(text):
        plan = None
    if plan:
        plan_text = _plan_text(text, plan.end())
        words = re.sub(r"^to\s+", "", plan_text, flags=re.I).lower().split()
        while words and words[0] in ("a", "an", "the", "my", "our"):
            words.pop(0)
        first_word = words[0] if words else ""
        after_an_infinitive = (bool(re.match(r"to\b", plan_text, re.I))
                               or bool(INFINITIVE_FRAME.search(plan.group(0))))
        if (plan_text and not re.match(r"(?:[£$€]|\d)", plan_text)
                and first_word not in NOT_PLACES
                and (after_an_infinitive
                     or (first_word not in PLACE_VERBS and _a_plan_has_a_thing(plan_text)))):
            verb = _plan_verb(plan, plan_text)
            if verb:
                plan_text = verb + " " + plan_text[:1].lower() + plan_text[1:]
            found["plan"] = plan_text
    if found.get("plan") and found.get("pets"):
        if PETS.search(found["plan"]):
            del found["plan"]
    for key in ("places", "allergies", "people"):
        if key in found:
            kept = [value for value in (_fact_value(v) for v in found[key]) if value]
            if kept:
                found[key] = kept
            else:
                del found[key]
    for entry in found.get("others") or []:
        for key in ("allergies", "places"):
            if key in entry:
                entry[key] = [value for value in (_fact_value(v) for v in entry[key]) if value]
    for key in ("budget", "diet", "city", "plan"):
        if key in found and not _fact_value(found[key]):
            del found[key]
        elif key in found:
            found[key] = _fact_value(found[key])
    if "plan" not in found:
        deed = []
        several = list(_dated_plans(text, deed))
        dated = _appointment(text) or (several[0] if several else "")
        if dated:
            found["plan"] = dated
            if len(several) > 1:
                found["plans_today"] = several
        elif deed:
            found["done"] = deed[0]
    if "plan" in found and moved is None:
        found["plans"] = found.pop("plans_today", None) or found["plan"]
    if moved is not None:
        found.pop("plan", None)
        found.pop("plans", None)
    correction = (CORRECTION_SAID.search(text) or CORRECTION.search(text)
                  or CORRECTION_PAIR.search(text) or CORRECTION_NUMBER_PAIR.search(text)
                  or _a_day_taken_back(text)
                  or _a_moved_time(text) or CORRECTION_CLOCK.search(text)
                  or CLOCK_PREFERRED.search(text)
                  or CORRECTION_MAKE.search(text))
    made = correction is not None and correction.re is CORRECTION_MAKE
    hedged = None
    if correction is None:
        dated = (CORRECTION_DATE.search(text) or CORRECTION_DATE_GOING.search(text)
                 or CORRECTION_GOING_MOVED.search(text))
        if dated is not None:
            found["correction"] = {"to": _tidy(" ".join(dated.group("date").split())),
                                   "from": None}
    if correction is None and "correction" not in found:
        hedged = None if correction is not None else CORRECTION_HEDGED.search(text)
        if hedged is not None:
            correction = hedged
        bare = None if correction is not None else CORRECTION_BARE.search(text)
        if bare is not None and bare.group(1).lower() not in CORRECTION_BARE_NO and (
                _the_value_alone(COPULA_SPLIT.split(bare.group(1))[0]).strip().lower()
                not in CORRECTION_BARE_NO):
            correction = bare
        if correction is None:
            named = NO_THEN_A_THING_NAMED.search(text)
            if named is not None and named.group(1).lower().split()[0] not in ANIMALS:
                correction = named
    if correction is None and moved is not None:
        found["correction"] = {"to": moved, "from": None}
    if correction is None:
        amount = AMOUNT_CORRECTION.search(text) or AMOUNT_CORRECTION_BARE.search(text)
        if amount:
            before = set(re.findall(r"[a-z']+", text[:amount.start()].lower())[-4:])
            if not before & AMOUNT_WISH:
                found["correction"] = {"to": amount.group(1).strip(" .,"), "from": None}
    if correction and not _is_only_the_take_back(correction.group(1), denials(text)):
        wrong = correction.group(2) if correction.re.groups > 1 else None
        value = _the_value_alone(COPULA_SPLIT.split(correction.group(1))[0])
        without_it = re.sub(r"^(?:on|in|at)\s+", "", value, flags=re.I).strip()
        if without_it and a_value(without_it):
            value = without_it
        value = the_name_in(value) or value
        if a_value(value) or hedged is not None:
            found["correction"] = {"to": _tidy(value),
                                   "from": _tidy_apart(wrong) if wrong else None}
            if made:
                found["correction"]["make"] = True
    if "correction" not in found:
        amount = AMOUNT_CORRECTION.search(text) or AMOUNT_CORRECTION_BARE.search(text)
        if amount:
            before = set(re.findall(r"[a-z']+", text[:amount.start()].lower())[-4:])
            if not before & AMOUNT_WISH:
                found["correction"] = {"to": amount.group(1).strip(" .,"), "from": None}
    if "correction" not in found and found.get("drop") is None:
        pair = CORRECTION_NOT_PAIR.search(text)
        if pair is not None:
            right, wrong = _tidy(pair.group(2)), _tidy(pair.group(1))
            if (a_value(right) and a_value(wrong)
                    and right.lower() not in NOT_A_DAY and wrong.lower() not in NOT_A_DAY):
                found["correction"] = {"to": right, "from": wrong}
    if "correction" not in found and found.get("drop") is None:
        denial = DENIAL_OF_A_VALUE.match(text)
        if denial is not None and not a_name_is_taken_back(text):
            said, wrong = denial.group("value"), denial.group("wrong")
            if said and denial.group("says") and a_value(said):
                from_wrong = (_tidy(wrong) if wrong and a_value(wrong)
                              and wrong.lower() != said.lower() else None)
                found["correction"] = {"to": _tidy(said), "from": from_wrong}
            elif said and not denial.group("says"):
                pass
    if "correction" not in found and found.get("drop") is None:
        paired = CORRECTION_NOT_TO.search(text)
        if paired is not None:
            wrong, right = _tidy(paired.group(1)), _tidy(paired.group(2))
            right = re.sub(r"\s+(?:instead|then|now)\b\W*$", "", right, flags=re.I)
            if (a_value(wrong) and a_value(right) and wrong.lower() not in NOT_A_DAY
                    and right.lower() not in NOT_A_DAY and wrong.lower() != right.lower()):
                found["correction"] = {"to": right, "from": wrong}
        gone = CORRECTION_NOT.search(text)
        if gone is not None and "correction" not in found:
            value = COPULA_SPLIT.split(gone.group(1))[0]
            if a_value(value) and value.lower() not in NOT_A_DAY:
                found["drop"] = _tidy(value)
    if not found and RETRACT.match(str(text or "").strip()):
        found["retract"] = True
    for key, value in list(found.items()):
        if isinstance(value, str) and value:
            kept = no_tone(value)
            if kept:
                found[key] = kept
            else:
                del found[key]
        elif isinstance(value, list) and all(isinstance(item, str) for item in value):
            cleaned = [(item, no_tone(item)) for item in value]
            found[key] = [kept for item, kept in cleaned
                          if kept and not RETRACT.match(kept)]
            if not found[key]:
                del found[key]
    for entry in found.get("others") or []:
        for key, value in list(entry.items()):
            if key == "who":
                continue
            if isinstance(value, str) and value:
                entry[key] = no_tone(value)
            elif isinstance(value, list) and all(isinstance(item, str) for item in value):
                entry[key] = [kept for kept in (no_tone(item) for item in value) if kept]
    if "correction" not in found and CORRECTION_MARK.search(text):
        for key in CORRECT_FROM_MARK:
            value = found.get(key)
            if isinstance(value, list):
                value = value[0] if value else None
            if isinstance(value, (int, float)):
                value = str(value)
            if not isinstance(value, str) or not value.strip():
                continue
            if not a_value(value):
                continue
            found["correction"] = {"to": _tidy(value), "from": None}
            break
    return found
