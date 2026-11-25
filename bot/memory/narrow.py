import re

PLACE = re.compile(r"\b(?:oven|hob|pan|grill|fridge|freezer|microwave|slow cooker"
                   r"|barbecue|barbie|air fryer|steamer|skillet|airing cupboard|kettle"
                   r"|pot|saucepan|dish|tray|tin)\b", re.I)
COOKS = re.compile(r"\b(?:bake|baking|roast|roasting|boil|boiling|fry|frying|grill|grilling"
                   r"|simmer|simmering|steam|steaming|cook|cooking|reheat|reheating"
                   r"|warm|warming)\b", re.I)

URGENT = re.compile(r"\b(?:999|111|a&e|a and e|emergency|urgent|chest pain"
                    r"|can(?:no|'|’)t breathe|cannot breathe|difficulty breathing"
                    r"|stiff neck|can(?:no|'|’)t swallow|cannot swallow"
                    r"|unconscious|not breathing|suicid\w*|overdos\w*|self[- ]harm"
                    r"|see (?:a|your|the) (?:gp|doctor|physio|nurse|dentist|midwife|pharmacist))\b",
                    re.I)

ASKS = (
    ("money", re.compile(r"\bhow much (?:does|do|is|are|will|would|should|can|could)\b"
                         r".*\b(?:cost|costs|pay|price|spend|budget|charge|charges"
                         r"|fee|fees|quote|rate|rates)\b"
                         r"|\bwhat(?:'s| is) the price\b|\bhow much for\b")),
    ("money", re.compile(
        r"\b(?:is|are|was|were|will|would|does|do|did|should)\s+"
        r"(?:that|this|it|they|those|these|the\s+[a-z]+|a\s+[a-z]+|an\s+[a-z]+)"
        r"(?:\s+(?:be|going to be))?(?:\s+[a-z]+){0,3}\s+"
        r"(?:expensive|pricey|costly|cheap)\b"
        r"|\bhow much (?:is|was|are|were)\s+(?:that|this|it|those|these)\b")),
    ("pressure", re.compile(r"\bwhat pressure\b|\bhow much pressure\b"
                           r"|\bwhat should the pressure\b")),
    ("distance", re.compile(r"\bhow far\b|\bhow many (?:miles|km|kilometres|kilometers)\b")),
    ("clock", re.compile(r"\bwhat time\b|\bat what time\b|\bwhat(?:'s| is) the time\b")),
    ("time", re.compile(r"\bhow long\b|\bhow many (?:minutes|mins|hours|hrs|days|weeks)\b"
                        r"|\bhow much time\b")),
    ("heat", re.compile(r"\b(?:what|which) (?:temperature|temp|temps|degrees)\b|"
                        r"\bhow (?:hot|warm)\b|\bwhat heat\b"
                        r"|\bwhat gas mark\b|\bhow (?:high|low) (?:a )?(?:heat|temperature)\b")),
    ("amount", re.compile(r"\bhow much\b|\bhow many\b|\bhow (?:big|large)\b|\bwhat size\b")),
    ("order", re.compile(r"\bbefore (?:or|and) after\b|\bwhich (?:first|way round)\b"
                         r"|\bin what order\b|\b(?:the day before|ahead of time|in advance)\b")),
    ("cause", re.compile(r"\bwhy\b"
                         r"|\bwhat(?:'s| is| was| could be| might be| else could be)?\s+"
                         r"(?:causing|caused|causes?|cause|behind)\b"
                         r"|\bwhat(?:'s| is) the reason\b|\breason (?:for|behind)\b")),
    ("remedy", re.compile(
        r"\bwhat (?:can|could|should|do) i (?:take|use)\b[^?]{0,30}\b(?:it|that|this)\b"
        r"|\banything (?:i can|to) take for (?:it|that|this)\b"
        r"|\bhow (?:do|can) i (?:treat|soothe|ease) (?:it|this|that)\b"
        r"|\bwhat (?:eases|soothes|helps with) (?:it|this|that)\b"
        r"|^\s*(?:and\s+|so\s+|ok\s+|okay\s+|but\s+|well\s+|right\s+)*"
        r"(?:is\s+there\s+(?:anything|something)"
        r"|anything"
        r"|(?:what|which)\s+(?:can|could|should|shall|do|would)\s+i)"
        r"(?:\s+i)?\s*(?:can\s+|could\s+|should\s+|shall\s+)?(?:take|use)\b"
        r"(?:\s+(?:for|of)\s+(?:it|that|this|them|those|the pain|the ache))?"
        r"(?:\s+(?:instead|now|then|please|again))?\W*$")),
    ("date", re.compile(r"\bwhen (?:was|were|did|does|do|is|are|had|could|can|might)\b"
                        r"|\bwhen exactly\b"
                        r"|\bwhat (?:year|date)\b|\bwhich year\b|\bhow long ago\b")),
)

DONENESS = re.compile(r"\b(?:done|ready|cooked|baked|finished|ready to eat|is it ready)\b")

ASKS_THE_DATE_ITSELF = re.compile(r"\b(?:what|which)\s+(?:year|date)\b|\bhow long ago\b")
A_LENGTH = re.compile(
    r"\b(?P<lead>for|since|about|nearly|almost|over|going on|the last|the past|these last|the "
    r"best part of)\s+(?:(?P<amount>\d+|a|an|one|two|three|four|five|six|seven|eight|nine|ten|"
    r"eleven|twelve|a couple of|couple of|a few|few|several|a good)\s+)?"
    r"(?P<unit>hours?|days?|weeks?|months?|years?|nights?|fortnight|weekends?|monday|tuesday|"
    r"wednesday|thursday|friday|saturday|sunday|christmas|yesterday)\b",
    re.I)

LENGTH_FILLER = frozenset("""
    its it's it has is been being bin like that this the same way here still yeah yep yes well
    honestly god ugh urgh so and but no not much pretty just only nothing change changed
    different doing happening going on now we we've were i im ive i've of a an half
    for since about nearly almost over going the last past these best part a an couple few
    several good
    """.split())

LENGTH_NAMED_DAYS = frozenset((
    "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "christmas"))


def only_a_length(text):
    if not isinstance(text, str) or "?" in text:
        return False
    found = A_LENGTH.search(text)
    if not found:
        return False
    rest = (text[:found.start()] + " " + text[found.end():]).replace(",", " ").split()
    if len(rest) > 6:
        return False
    return all(word.lower() in LENGTH_FILLER for word in rest)

NOT_RELATIVE = r"(?!\s+(?:less|more|earlier|later|longer|shorter)\b)"
SPAN_FILLER = r"\s+(?:(?:full|whole|solid|clear)\s+)?"

CLOCK = re.compile(r"\b\d{1,2}\s*(?::\s*\d{2}\s*(?:am|pm|a\.m\.|p\.m\.)?|\s*(?:am|pm|a\.m\.|p\.m\.))"
                   r"|\b\d{1,2}\.\d{2}\b|\b(?:midday|midnight|noon)\b", re.I)

CAUSE = re.compile(r"\b(?:because|since|due to|caused by|causes?|causing|usually"
                   r"|commonly|linked to|comes from)\b"
                   r"|\b(?:is|are|was|were)\b[^.!?]*:|,\s*so\b", re.I)

REMEDY = re.compile(
    r"\b(?:paracetamol|ibuprofen|aspirin|painkillers?|pain-relief|antihistamines?|antacids?"
    r"|lozenges?|gargle|gargles|honey|lemon|salt[- ]water|steam|plasters?|antiseptic"
    r"|rehydration|over[- ]the[- ]counter|pharmac(?:y|ist)|plenty to drink|drink plenty"
    r"|\bdrops?\b"
    r"|drink water|anti-inflammator[^ ]*)\b",
    re.I)


SYMPTOM = re.compile(
    r"\b(?:pain|ache|aches|aching|achy|sore|hurt|hurts|hurting|ill|sick|unwell|symptom|symptoms"
    r"|cold|flu|cough|coughs|coughing|throat|headache|migraine|temperature|fever|nausea"
    r"|rash|rashy|itch|itches|itching|swelling|swollen|nose|ear|earache|earwax|eye|eyes|stomach"
    r"|tummy|constipat\w*|diarrhoea|hayfever|hay fever|allerg\w*|sprain\w*|strain\w*|cramp|cramps"
    r"|burn|burns|burnt|blister\w*|tooth|toothache|gum|gums|verruca|hearing)\b",
    re.I)

REMEDY_CUT = re.compile(r"\s*[,;:]\s*")
REMEDY_JOINER = re.compile(r"^(?:and|but|so|then|plus|also|or|instead)\s+", re.I)


def _the_remedy_in(said):
    said = str(said or "")
    if not REMEDY.search(said) or not SYMPTOM.search(said):
        return None
    for sentence in [s.strip() for s in SENTENCE.split(said) if s.strip()]:
        pieces = [piece.strip() for piece in REMEDY_CUT.split(sentence) if piece.strip()]
        for at, piece in enumerate(pieces):
            if not REMEDY.search(piece):
                continue
            kept = [piece]
            while at + len(kept) < len(pieces) and len(" ".join(kept).split()) < 6:
                kept.append(pieces[at + len(kept)])
            part = tidy(REMEDY_JOINER.sub("", ", ".join(kept).strip(" ,;:")))
            if part and part.count("(") == part.count(")"):
                return part
    return None


def carries(reply, kind):
    if kind == "remedy":
        return bool(REMEDY.search(" ".join(str(reply or "").lower().split())))
    span = SPANS.get(str(kind or ""))
    return bool(span and span.search(str(reply or "")))


MONTHS_LONG = (r"(?:january|february|march|april|may|june|july|august|september|october"
               r"|november|december|jan|feb|mar|apr|jun|jul|aug|sept?|oct|nov|dec)")
WEEKDAY_OR_CLOCK = (r"|\b(?:(?:this|next|last|coming|bank)\s+)?(?:monday|tuesday|wednesday"
                    r"|thursday|friday|saturday|sunday)\b"
                    r"|\b\d{1,2}(?::\d{2})?\s*(?:am|pm)\b")
DAY_OR_YEAR = re.compile(
    r"\b\d{1,4}\s*(?:bc|bce|ad|ce)\b"
    r"|\b(?:1[0-9]|20[0-9])\d{2}\b"
    r"|\b[1-9]\d{2}\b"
    r"|\b(?:[1-9]|[12]\d|3[01])(?:st|nd|rd|th)?\s+(?:of\s+)?" + MONTHS_LONG + r"\b"
    r"|\b" + MONTHS_LONG + r"\s+\d{1,2}(?:st|nd|rd|th)?\b" + WEEKDAY_OR_CLOCK, re.I)

DATED_STRONG = re.compile(
    r"\b\d{1,4}\s*(?:bc|bce|ad|ce)\b"
    r"|\b(?:[1-9]|[12]\d|3[01])(?:st|nd|rd|th)?\s+(?:of\s+)?" + MONTHS_LONG + r"\b"
    r"|\b" + MONTHS_LONG + r"\s+\d{1,2}(?:st|nd|rd|th)?\b" + WEEKDAY_OR_CLOCK, re.I)


def has_a_date(sentence):
    if DATED_STRONG.search(sentence):
        return True
    return bool(SPANS["date"].search(SPANS["money"].sub(" ", sentence)))

FULL_LENGTH = (r"(?:\d+(?:\.\d+)?|one|two|three|four|five|six|seven|eight|nine|ten|eleven"
               r"|twelve|a few|a couple of|a|an)\s+(?:full|whole|entire)\s+(?:days?"
               r"|nights?|weeks?|months?|years?|hours?|minutes?)\b")

AMOUNT_UNIT = (r"microgrammes?|micrograms?|milligrammes?|milligrams?|millilitres?|milliliters?"
               r"|centilitres?|decilitres?|grammes?|grams?|mg|mcg|\u00b5g|g|kg|ml|l|litres?|liters?"
               r"|tbsp|tsp|tablespoons?|teaspoons?|cups?|parts?|people|slices?|tins?"
               r"|oz|lbs?|pounds?|tablets?|capsules?|drops?|puffs?|sprays?|units?|iu"
               r"|kcal|calories|pouches?|sachets?|scoops?")

SIGNALS = {
    "money": re.compile(r"£\s?\d|\b\d[\d,.]*\s*(?:pounds?|quid|euros?|dollars?)\b", re.I),
    "distance": re.compile(r"\b\d+(?:\.\d+)?\s*(?:m|km|metres?|meters?|miles?|mi)\b", re.I),
    "pressure": re.compile(r"\b\d+(?:\.\d+)?\s*(?:bar|psi)\b", re.I),
    "clock": CLOCK,
    "time": re.compile(r"\b\d+(?:\.\d+)?(?:\s*(?:-|to|–|and)\s*\d+(?:\.\d+)?)?"
                       + SPAN_FILLER +
                       r"(?:minutes?|mins?|hours?|hrs?|seconds?|secs?|days?|weeks?|months?"
                       r"|years?)\b"
                       + NOT_RELATIVE +
                       r"|\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve"
                       r"|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty"
                       r"|thirty|forty|forty-five|fifty|sixty|seventy|eighty|ninety"
                       r"|twenty-four|thirty-six)"
                       + SPAN_FILLER +
                       r"(?:minutes?|mins?|hours?|hrs?|seconds?|secs?|days?|weeks?|months?"
                       r"|years?)\b"
                       + NOT_RELATIVE +
                       r"|\b(?:an?|one|two|three|four|five|six|seven|eight|nine|ten|a couple of|a few)\s+"
                       r"(?:hours?|minutes?|days?|weeks?|months?|years?)\s+and\s+a\s+half\b" + NOT_RELATIVE +
                       r"|\b(?:an?|one|two|three|four|five|six|seven|eight|nine|ten|a couple of|a few)\s+"
                       r"and\s+a\s+half\s+"
                       r"(?:hours?|minutes?|days?|weeks?|months?|years?)\b" + NOT_RELATIVE +
                       r"|\bhalf\s+an?\s+(?:hour|minute|second)\b" + NOT_RELATIVE +
                       r"|\b(?:a|an|one|half an|a couple of|a few|a handful of)\s+"
                       r"(?:(?:full|whole|solid|clear)\s+)?"
                       r"(?:minute|second|hour|day|week|month|year)s?\b" + NOT_RELATIVE +
                       r"|\b\d+(?:\.\d+)?\s*[-\u2013]\s*(?:minutes?|mins?|hours?|hrs?"
                       r"|days?|weeks?|months?|years?)\b" + NOT_RELATIVE +
                       r"|\b\d+\s*hours?\s*\d+\b" + NOT_RELATIVE +
                       r"|\b" + FULL_LENGTH + NOT_RELATIVE, re.I),
    "heat": re.compile(r"\b\d{2,3}\s*(?:°\s*)?c\b|\b\d{2,3}\s*degrees?\b|\bgas mark \d\b", re.I),
    "amount": re.compile(r"\b\d+(?:\.\d+)?\s*(?:" + AMOUNT_UNIT + r")\b", re.I),
    "order": re.compile(r"\b(?:before|after|first|last|ahead|in advance)\b", re.I),
    "date": DAY_OR_YEAR,
}

SPANS = {
    "money": re.compile(r"£\s?\d[\d,]*(?:\.\d+)?(?:\s*(?:-|to|–)\s*£?\s?\d[\d,]*(?:\.\d+)?)?",
                        re.I),
    "distance": re.compile(r"\b\d+(?:\.\d+)?\s*(?:m|km|metres?|meters?|miles?|mi)\b", re.I),
    "pressure": re.compile(r"\b(?:between\s+)?\d+(?:\.\d+)?"
                           r"(?:\s*(?:-|to|and|–)\s*\d+(?:\.\d+)?)?\s*(?:bar|psi)\b", re.I),
    "clock": CLOCK,
    "time": re.compile(r"\b\d+\s*(?:months?|years?)\s*(?:-|to|or|and|–)\s*"
                       r"(?:\d+(?:\.\d+)?|two|three|four|five|six|seven|eight|nine|ten"
                       r"|twelve|eighteen|twenty-four)\s*(?:months?|years?)\b"
                       r"|\b\d+\s*hours?\s*(?:and\s*)?\d+\s*(?:minutes?|mins?)?\b"
                       r"|\b\d+(?:\.\d+)?(?:\s*(?:-|to|–|and)\s*\d+(?:\.\d+)?)?\s*"
                       r"(?:minutes?|mins?|hours?|hrs?|seconds?|secs?|days?|weeks?"
                       r"|years?|months?|decades?|centur(?:y|ies))"
                       r"(?:\s*(?:per|a)\s*\d*\s*(?:g|kg|kilo|pound|lb))?\b"
                       + NOT_RELATIVE +
                       r"|\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve"
                       r"|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty"
                       r"|thirty|forty|forty-five|fifty|sixty|seventy|eighty|ninety)"
                       r"(?:\s*(?:or|to|and|-|\u2013)\s*(?:one|two|three|four|five|six|seven"
                       r"|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen"
                       r"|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty"
                       r"|seventy|eighty|ninety))?"
                       r"\s+(?:minutes?|mins?|hours?|hrs?|seconds?|secs?|days?|weeks?|months?"
                       r"|years?)\b"
                       + NOT_RELATIVE +
                       r"|\b(?:an?|one|two|three|four|five|six|seven|eight|nine|ten)\s+"
                       r"(?:hours?|minutes?|days?|weeks?|months?|years?)\s+and\s+a\s+half\b"
                       + NOT_RELATIVE +
                       r"|\b(?:an?|one|two|three|four|five|six|seven|eight|nine|ten)\s+and\s+"
                       r"a\s+half\s+(?:hours?|minutes?|days?|weeks?|months?|years?)\b"
                       + NOT_RELATIVE +
                       r"|\bhalf\s+an?\s+(?:hour|minute|second)\b" + NOT_RELATIVE +
                       r"|\b(?:an|one|half an) hour\b" + NOT_RELATIVE +
                       r"|\b(?:a|an|one)\s+(?:second|minute|hour|day|week|month|year)\s+or\s+"
                       r"(?:two|three|four|five|six)\b" + NOT_RELATIVE +
                       r"|\b(?:a couple of|a few)\s+(?:weeks?|months?|years?)\b" + NOT_RELATIVE +
                       r"|\b(?:a|an|one)\s+(?:full|whole|solid)\s+"
                       r"(?:minutes?|hours?|days?|weeks?|months?|years?)\b" + NOT_RELATIVE +
                       r"|\b\d+(?:\.\d+)?\s*[-\u2013]\s*(?:minutes?|mins?|hours?|hrs?"
                       r"|days?|weeks?|months?|years?)\b" + NOT_RELATIVE +
                       r"|\b" + FULL_LENGTH + NOT_RELATIVE, re.I),
    "heat": re.compile(r"\b\d{2,3}\s*(?:°\s*)?c\b(?:\s*\(\s*\d{2,3}\s*°?\s*c\s*fan\s*\))?"
                       r"|\bgas mark \d\b", re.I),
    "amount": re.compile(r"\b\d+(?:\.\d+)?\s*(?:" + AMOUNT_UNIT + r")\b", re.I),
    "cause": CAUSE,
    "date": DAY_OR_YEAR,
}

RATE = re.compile(r"\bper\b\s*(?:kilo|kg|500g|pound|lb|person|head|each|serving|litre|liter)\b"
                  r"|\ba (?:kilo|pound|person)\b|\beach\b", re.I)

FREQUENCY_AFTER = re.compile(
    r"^\s*(?:a|an|per|each|every|once\s+a|twice\s+a|\d+\s*times\s+a)\s*"
    r"(?:day|week|month|year|session|evening|morning|night|go|class|lesson|walk|run|"
    r"fortnight|hour)\b", re.I)
FREQUENCY_AFTER_TIMES = re.compile(r"^\s*times\b", re.I)
FREQUENCY_BEFORE = re.compile(r"\b(?:every|each|once\s+every|once\s+in)\s*$", re.I)
FREQUENCY_AFTER_AT_A_TIME = re.compile(r"^\s*at\s+a\s+time\b", re.I)

LENGTH_OF_THE_JOB = re.compile(
    r"\bhow long (?:does|do|will|would|is|did|should) (?:it|that|this|they|these|the)\b"
    r"|\bhow long (?:until|before|till|til)\b"
    r"|\bhow much time\b", re.I)

class _NoLength:

    def __bool__(self):
        return False

    def __repr__(self):
        return "NO_LENGTH"


NO_LENGTH = _NoLength()

A_COUNTDOWN = re.compile(r"\bhow long (?:until|before|till|til)\b", re.I)

A_MOMENT = re.compile(r"\b(?:\d+(?:\.\d+)?|one|two|three|four|five|six|seven|eight|nine|ten"
                      r"|fifteen|twenty|thirty|forty-five|sixty|a few|a couple of)"
                      r"\s*(?:seconds?|secs?)\b", re.I)

RATE_LEAD = re.compile(r"^\s*(?:with|at|on|after|using|in)\b[^,;:]{0,60},\s*", re.I)

A_SET_OF_STEPS = re.compile(r"\b(?:then|next|after that|finally|lastly|step \d)\b"
                            r"|\b(?:wipe|rinse|boil|scrub|soak|coat|vacuum|hoover|descale"
                            r"|bleed|unblock|flush|brush|blot|vacuum|lather|scrub|polish"
                            r"|add|stir|mix|fill|leave it|leave them|run a|wash|clean)\b", re.I)


SEQUENCE = re.compile(r"\b(?:then|next|after that|finally|lastly|plus|followed by)\b", re.I)

WAIT = re.compile(r"\b(?:rest|resting|cool|cooling|leave|leaving|sit|sitting|stand|standing"
                  r"|wait|waiting|chill|chilling|set|setting)\b", re.I)

STEP = re.compile(r";\s*|:\s*|,\s*(?:then|and then|and)\s+|\s+(?:then|and then|and)\s+"
                  r"|\s+but\s+", re.I)

AFTER = re.compile(r"\b(?:off the heat|out of the oven|rest|resting|cool|cooling|leave|leaving"
                   r"|sit|sitting|stand|standing|wait|waiting|chill|chilling|set|setting)\b", re.I)


OVEN = frozenset(("oven", "bake", "baked", "bakes", "baking", "roast", "roasted", "roasts",
                  "roasting"))

WHERE = frozenset("""oven hob grill pan pot microwave barbecue bbq steamer fryer airfryer""".split())
BEFORE = re.compile(r"\b(?:before|until|till|til|by the time)\b", re.I)
RESULT = re.compile(r"\b(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|twelve|eighteen"
                    r"|twenty-four)(?:\s*(?:-|to|or)\s*(?:\d+|one|two|three|four|five|six"
                    r"|seven|eight|nine|ten|twelve))?\s*(?:days?|weeks?|months?|years?)\b",
                    re.I)

BARE_UNIT = re.compile(r"^\d+(?:[.,]\d+)?\s*(?:seconds?|secs?|minutes?|mins?|hours?|hrs?"
                       r"|days?|weeks?|months?|years?)[.!]?$", re.I)

KEEPS = re.compile(r"\b(?:keeps?|keeping|kept|fridge|freezer|frozen|freeze|leftovers?|shelf life"
                   r"|stored?|storing|use by)\b", re.I)

QUALIFIER_WORDS = frozenset("hard soft runny jammy medium rare well done fan gas top bottom"
                            " thick thin large small whole skimmed semi".split())
QUALIFIER = re.compile(r"\b(?:" + "|".join(sorted(QUALIFIER_WORDS, key=len, reverse=True))
                       + r")\b", re.I)
QUALIFIER_FILLER = frozenset("a an the and or but so too very quite not no more less most"
                             " it its it's this that these those".split())

SENTENCE = re.compile(r"(?<=[.!?])\s+")
NUM_RANGE = re.compile(r"\b(?:between\s+)?-?\d+(?:\.\d+)?\s+and\s+-?\d+(?:\.\d+)?", re.I)
RANGE_JOIN = "\x00"
THOUSANDS = re.compile(r"(?<=\d),(?=\d{3}(?:\D|$))")
THOUSANDS_JOIN = "\x02"


def pieces_of(text, pattern):
    guarded = NUM_RANGE.sub(lambda found: found.group(0).replace(" and ", RANGE_JOIN),
                            str(text or ""))
    guarded = THOUSANDS.sub(THOUSANDS_JOIN, guarded)
    return [piece.replace(RANGE_JOIN, " and ").replace(THOUSANDS_JOIN, ",")
            for piece in re.split(pattern, guarded)]

WORD = re.compile(r"[a-z0-9']+")

EMPTY = frozenset("""
a an the and or but if then than that this these those it its is are was were be been being
am do does did doing done have has had having i me my mine you your yours we us our they them
their he she his her one ones so too very just also as at by for from in into of off on onto
to up with about after before again any can could should would will shall may might must not
no yes ok okay please thanks thank there here what which who whom whose when where why how
much many long need needs needed want wants like get gets got make makes made use uses used
good best better still only even more most less few all some same other own now
# "around" and its family say a figure is approximate, not what a clause is about. Left in,
# "and how do i get around" was one content word, and the sentence it named in the answer before
# it was the one that happens to write "around twelve to fifteen euros" - so a question about
# the trams was answered with the cheap-meal card.
around roughly approximately
take takes took taken
""".split())

SAME = {}


def _same(words):
    group = frozenset(str(words).split())
    for word in group:
        SAME[word] = group


_same("crisp crispy crunchy crackling")
_same("soft tender mushy soggy")
_same("juicy moist")
_same("hot warm")
_same("cold chilled cool")
_same("quick fast quickest speedy faster")
_same("cheap cheaper cheapest budget affordable saving")
_same("expensive pricey costly")
_same("big large huge bigger")
_same("small little tiny smaller")
_same("leave left leaving leaves")

OPTION = re.compile(r"^\s*(?:and|what about|for)\b", re.I)
NOT_OPTION = re.compile(r"\b(?:is|are|was|were|do|does|did|will|would|can|could|should|shall"
                        r"|have|has|had|change|changes|take|takes|need|needs|use|uses)\b", re.I)

FOLLOW_UP = re.compile(r"^\s*(?:and|also|plus|what about|how about|what if|if|then|does that"
                       r"|would that|will that|does it|is that)\b")

UNIT = re.compile(r"\b(?:minutes?|mins?|hours?|hrs?|seconds?|days?|weeks?|degrees?|g|kg|ml"
                  r"|litres?|liters?|tbsp|tsp|cups?|bar|psi|miles?|metres?|meters?)\b", re.I)
NAMING_IGNORE = frozenset("""
use using used instead recipe version way time times take takes taking need needs
put putting cook cooking make making do doing think reckon okay ok actually really
also still there then already right again another one ones bit lot kind sort thing things
worth good best better worse fine matter matters any much should shall must
safe saf unsafe unsaf dangerous dangerou alright normal risky sensible sensibl
""".split())
BARE_RANGE = re.compile(r"\d(?:[\d.,]*\d)?\s*(?:-|to|and|–)\s*\d(?:[\d.,]*\d)?\s*$")
ASKS_ABOUT_IT = re.compile(r"^\s*(?:is|are|do|does|should|shall|can|could|will|would|must"
                           r"|need|have|was|were)\b|\?\s*$")

ASKING_ONLY = frozenset("""how what when where which who why much many long time times take takes
taking keep keeps keeping last lasts stay stays good safe should does do is are was were it its
and or the a an of in on at for to from with you we i that this these those still about""".split())

YES_NO = re.compile(r"^\s*(?:do|does|should|shall|can|could|is|are|will|would|must|need"
                     r"|have)\s+(?:i|we|you|it|they|he|she|this|that|there)\b"
                     r"|\bdo (?:i|we|you) need to\b")

STEP_VERB = re.compile(r"\b(?:do|does|should|shall|can|could|will|would|must|need|have)"
                       r"\s+(?:i|we|you)\s+"
                       r"(?:(?:need|have|want|got)\s+to\s+|be\s+)?"
                       r"([a-z']+)", re.I)


def step_word(question):
    found = STEP_VERB.search(flat(question))
    return found.group(1).lower() if found else None


def kind_of(question):
    clean = " ".join(str(question or "").lower().split())
    for kind, pattern in ASKS:
        if pattern.search(clean):
            if kind == "date" and DONENESS.search(clean):
                return None
            return kind
    return None


def asks_a_part(question):
    return (kind_of(question) is not None or _property_ask(question) or _option_ask(question)
            or _named_follow_up(question) or bool(YES_NO.search(flat(question)))
            or bool(ASKS_FREQUENCY.search(flat(question)))
            or bool(ASKS_FOR_A_HAND.search(flat(question))))


def _named_follow_up(question):
    clean = flat(question)
    if not FOLLOW_UP.search(clean):
        return False
    named = [word for word in words_of(clean) if word not in NAMING_IGNORE and len(word) > 2]
    return 1 <= len(named) <= 4


_COUNTED_UNIT = re.compile(
    r"\b(?:\d+(?:\.\d+)?|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve"
    r"|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty"
    r"|fifty|sixty|seventy|eighty|ninety|a couple of|a few)"
    r"\s+(?:full\s+|whole\s+|solid\s+|straight\s+)?"
    r"(seconds?|secs?|minutes?|mins?|hours?|hrs?|days?|weeks?|months?|years?)\b", re.I)


def _gives_a_figure_in(part, unit):
    return any(_unit_stem(hit.group(1)) == unit
               for hit in _COUNTED_UNIT.finditer(str(part or "")))


CLAUSE_BREAK = re.compile(r";\s+|,\s+(?:and|but|so)\s+|,\s+", re.I)


def _the_clause_in_the_unit(sentence, unit):
    for clause in CLAUSE_BREAK.split(str(sentence or "")):
        part = clause.strip()
        if not part or not _gives_a_figure_in(part, unit):
            continue
        part = re.sub(r"^(?:and|but|so|then|also)\s+", "", part, flags=re.I)
        if len(part.split()) >= 3:
            return part[:1].upper() + part[1:]
    return None


def _the_sentence_in_the_unit(reply, unit):
    for sentence in re.split(r"(?<=[.!?])\s+", str(reply or "")):
        part = sentence.strip()
        if part and _gives_a_figure_in(part, unit):
            return _the_clause_in_the_unit(part, unit) or part
    return None


def part_in_the_unit(reply, question):
    asked = ASKED_UNIT.search(str(question or ""))
    if asked is None:
        return None
    part = narrow(reply, question)
    if not isinstance(part, str) or not part.strip():
        return None
    unit = _unit_stem(asked.group(1))
    said = [word for word in re.findall(r"[A-Za-z]+", part) if _unit_stem(word) == unit
            and word.lower().rstrip("s") in _UNITS]
    return part if said else None


PAPERWORK = re.compile(
    r"\b(?:passport|licen[cs]e|visa|insurance|policy|certificate|document|membership|permit"
    r"|registration|warranty|guarantee|contract|tenancy|agreement|ticket|card|badge|ehic|ghic"
    r"|prescription|mortgage|bond|deed|statement|mot)\b")
A_VALIDITY_ASK = re.compile(
    r"\bwhen\s+(?:does|do|will|did)\b[^?]{0,40}\bexpir"
    r"|\bexpiry\b|\bexpiration\b"
    r"|\bhow\s+long\s+(?:is|are|does|do|will)\b[^?]{0,40}\b(?:valid|last)\b"
    r"|\b(?:is|are)\b[^?]{0,40}\b(?:still\s+)?(?:valid|in\s+date|out\s+of\s+date|expired)\b")



def asked_unit(question):
    asked = ASKED_UNIT.search(str(question or ""))
    return _unit_stem(asked.group(1)) if asked else None


def _states_a_length(part):
    return any(True for _ in _COUNTED_UNIT.finditer(str(part or "")))


OUTCOME_ASKS = (
    ("survives", re.compile(
        r"\bwill (?:it|that|this|they) (?:be )?(?:alright|all right|ok|okay|fine|safe)\b"
        r"|\bis (?:it|that|this) (?:going to be )?(?:alright|all right|ok|okay|fine|safe)\b"
        r"|\bwill (?:it|that|this) (?:survive|recover|work again|be ruined|be knackered)\b"
        r"|\bis (?:it|that|this) (?:ruined|knackered|a write[- ]off|done for)\b"
        r"|\bcan (?:it|that|this) be (?:saved|fixed|repaired|salvaged)\b"
        r"|\bis (?:it|that|this) worth (?:fixing|repairing)\b", re.I)),
    ("serious", re.compile(
        r"\bis (?:that|this|it) (?:bad|serious|dangerous|normal|common)\b"
        r"|\bhow (?:bad|serious) is (?:it|that|this)\b"
        r"|\bshould i (?:be )?worr(?:y|ied)\b"
        r"|\bis (?:that|this) (?:something|anything) to worry about\b"
        r"|\bis that (?:a|normal)\b", re.I)),
    ("next", re.compile(
        r"\bwhat happens (?:now|next)\b"
        r"|\bwhat next\b|\bwhat(?:'s| is| was) (?:the )?next\b|\bso what now\b"
        r"|\bwhat now\b", re.I)),
    ("explain", re.compile(
        r"\bwhat does (?:that|this|it) mean\b|\bwhat do you mean\b"
        r"|\bwhat(?:'s| is) that (?:mean|mean then)\b|\bmeaning what\b", re.I)),
)


def the_outcome_asked(question):
    said = flat(question)
    for which, pattern in OUTCOME_ASKS:
        if pattern.search(said):
            return which
    return ""


def the_part_asked(reply, question, about=""):
    part = narrow(reply, question, about)
    unit = asked_unit(question)
    if unit is None or _gives_a_figure_in(part, unit) or not _states_a_length(part):
        return part
    return _the_sentence_in_the_unit(reply, unit) or part


A_RATE_ON_A_FIGURE = re.compile(
    r"\s+(?:a|an|per|each)\s+(year|month|week|day|hour)\b", re.I)
A_PERIOD_IN_A_LINE = re.compile(
    r"\b(?:a|an|per|each)\s+(year|month|week|day|hour)\b", re.I)


def _a_rate_cut_from_its_figure(reply, part, question):
    whole = flat(reply)
    piece = flat(part)
    figure = next(SPANS["money"].finditer(piece), None)
    if figure is None:
        return False
    asked = A_PERIOD_IN_A_LINE.search(flat(question))
    periods = []
    for hit in SPANS["money"].finditer(whole):
        if hit.group(0).lower() != figure.group(0).lower():
            continue
        found = A_RATE_ON_A_FIGURE.match(whole[hit.end():hit.end() + 14])
        if not found:
            return False
        periods.append(found.group(1).lower())
    if not periods:
        return False
    return not asked or asked.group(1).lower() not in periods


def narrow(reply, question, about=""):
    said = flat(question)
    if A_VALIDITY_ASK.search(said) and (PAPERWORK.search(said) or PAPERWORK.search(flat(about))):
        return None
    part = _narrow(reply, question)
    if part is None:
        return None
    if JOINS.match(flat(part)):
        return None
    if kind_of(question) == "money" and _a_rate_cut_from_its_figure(reply, part, question):
        return None
    return part


JOINS = re.compile(r"^(?:which|that|who|whom|whose|where|because|though|although|whereas"
                   r"|while|yet|however|instead|plus|as well)\b", re.I)


_STATE_LENGTH_ASKS = re.compile(
    r"\b(?:last|lasts|lasted|keep|keeps|kept|stays?|stay like this|be like this|go away|"
    r"goes away|clear up|clears up|get better|gets better|recover|recovers|heal|heals)\b", re.I)
_A_DOING = re.compile(
    r"\b(?:ice|icing|rest|resting|take|taking|apply|applying|use|using|hold|holding|keep|keeping|"
    r"wear|wearing|put|putting|wrap|wrapping|elevate|elevating|soak|soaking|leave|leaving|rinse|"
    r"rinsing|clean|cleaning|stretch|stretching|massage|massaging|drink|drinking|eat|eating|"
    r"swallow|swallowing|avoid|avoiding|stop|stopping|exercise|exercising|compress|bandage|"
    r"dress|dressing|change|changing|walk|walking|run|running|sit|sitting|lie|lying)\b")


def _a_length_of_a_doing(sentence, part, question):
    if not _STATE_LENGTH_ASKS.search(flat(question)):
        return False
    said = flat(sentence)
    cut = flat(part)
    at = said.find(cut) if cut else -1
    if at < 0:
        return False
    doing = set(_A_DOING.findall(said))
    if not doing or doing & set(_A_DOING.findall(flat(question))):
        return False
    return bool(_A_DOING.search(_a_clause_before(said, at)))


_A_CUT_OFF_BEFORE = re.compile(
    r"\b(?:over|under|above|below|past|aged|beyond|around|about|from|at|by|until|till|"
    r"after|before|of)\s*$", re.I)
_A_CUT_OFF_AFTER = re.compile(
    r"^\s*(?:or\s+(?:over|older|under|younger|more|less)|and\s+(?:over|under)|of\s+age)\b", re.I)
_A_DURATION_VERB = re.compile(
    r"\b(?:last|lasts|lasted|lasting|take|takes|took|taking|settle|settles|go|goes|went|gone|"
    r"going|run|runs|ran|keeping|kept|stay|stays|stayed|heal|heals|healed|clear|clears|"
    r"cleared|recover|recovers|recovered|recede|recedes|ease|eases|expires?|expiring|"
    r"is|are|was|were|be|been|being)\b", re.I)
_IN_MONTHS_OR_YEARS = re.compile(r"\b(?:month|months|year|years)\b", re.I)
_A_RANGE = re.compile(r"\b(?:to|or|-|and)\b", re.I)
_A_BARE_FIGURE = re.compile(
    r"(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|"
    r"fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|\d{1,3}|a|an|"
    r"half)", re.I)


def _a_cut_off_not_a_length(sentence, part):
    said = flat(sentence)
    cut = flat(part).rstrip(". ")
    if not cut:
        return False
    at = said.find(cut)
    if at < 0:
        return False
    before = said[:at]
    after = said[at + len(cut):]
    if not (_A_CUT_OFF_BEFORE.search(before) or _A_CUT_OFF_AFTER.match(after)):
        return False
    if not (_IN_MONTHS_OR_YEARS.search(cut) or _A_BARE_FIGURE.fullmatch(cut)):
        return False
    if _A_RANGE.search(cut):
        return False
    clause = _a_clause_before(said, at)
    return not _A_DURATION_VERB.search(clause)


def _a_clause_before(said, at):
    start = 0
    for mark in (",", ";", ":"):
        cut = said.rfind(mark, 0, at)
        if cut >= 0:
            start = max(start, cut + 1)
    return said[start:at]


def the_doings_length(reply, question):
    whole = flat(reply)
    if not whole or not _STATE_LENGTH_ASKS.search(flat(question)):
        return ""
    kind = kind_of(question)
    if kind not in ("time", "clock"):
        return ""
    clauses = []
    for sentence in SENTENCE.split(str(reply or "")):
        if not sentence.strip() or not SIGNALS[kind].search(sentence):
            continue
        part = _part(sentence, kind, question)
        if not part or part is NO_LENGTH:
            continue
        if not _a_length_of_a_doing(sentence, part, question):
            return ""
        said = flat(sentence)
        clause = _the_clause_around(said, said.find(flat(part)))
        if clause and flat(clause) != whole:
            clauses.append(clause)
    return clauses[0] if clauses else ""


def _the_clause_around(said, at):
    if at < 0:
        return ""
    start = 0
    for mark in (",", ";", ":"):
        cut = said.rfind(mark, 0, at)
        if cut >= 0:
            start = max(start, cut + 1)
    end = len(said)
    for mark in (",", ";", ":"):
        cut = said.find(mark, at)
        if cut >= 0:
            end = min(end, cut)
    return said[start:end].strip(" .")


def _at_another_place(sentence, part, question):
    asked = {word.lower() for word in PLACE.findall(flat(question))}
    if not asked:
        return False
    said = flat(sentence)
    cut = flat(part)
    at = said.find(cut) if cut else -1
    if at < 0:
        return False
    found = PLACE.search(said[at + len(cut):])
    if not found:
        return False
    return found.group(0).lower() not in asked


def _gives_another_places_figure(sentence, kind, question):
    if kind not in SPANS:
        return False
    part = _part(sentence, kind, question)
    if not part or part is NO_LENGTH:
        return False
    return _at_another_place(sentence, part, question)


def _narrow(reply, question):
    if not isinstance(reply, str) or not reply.strip():
        return None
    kind = kind_of(question)
    if kind == "remedy":
        part = _the_remedy_in(reply)
        return part if part and flat(part) != flat(reply) else None
    if kind is not None and kind not in SPANS:
        return None
    whole = flat(reply)
    if URGENT.search(whole):
        return None
    sentences = [s.strip() for s in SENTENCE.split(reply.strip()) if s.strip()]
    when_ask = False
    if kind == "date":
        dated = _dated(sentences, question, whole)
        if dated:
            return dated
        if ASKS_THE_DATE_ITSELF.search(flat(question)):
            return None
        when_ask = True
        kind = "time" if SIGNALS["time"].search(reply) else None
        if kind is None:
            return _the_answer_said_again(sentences, whole)
    wanted = {word for word in words_of(question) if word not in POINTS_BACK}
    if wanted:
        naming = [one for one in sentences if wanted & set(words_of(one))]
        if naming:
            sentences = [one for one in naming
                         if not _gives_another_places_figure(one, kind, question)] or sentences
    if kind == "cause":
        only = {word for word in wanted
                if sum(word in set(words_of(one)) for one in sentences) == 1}
        if only:
            named = [one for one in sentences if only & set(words_of(one))]
            if named:
                sentences = named
        openings = sentences[:1] if flat(question).strip(" ?!.") == "why" else sentences
        for sentence in openings:
            if CAUSE.search(sentence):
                return tidy(sentence) if flat(sentence) != whole else None
        return None
    if kind == "time" and PLACE.search(question):
        sentences = [one for one in sentences if PLACE.search(one) or COOKS.search(one)]
    if kind == "time" and BEFORE.search(question):
        for sentence in [one for one in sentences if RESULT.search(one)]:
            found = [_figure(match, sentence) for match in RESULT.finditer(sentence)]
            part = tidy(found[-1]) if found else None
            if part and flat(part) != whole:
                return part
    piece = _named_clause(reply, question)
    if piece:
        piece = _with_unit(piece, reply)
        if kind is not None and kind in SPANS and SIGNALS[kind].search(piece):
            part = _part(piece, kind, question)
            if part is NO_LENGTH:
                part = None
            if part and _at_another_place(piece, part, question):
                part = None
            if part:
                part = tidy(part)
                if part and flat(part) != whole:
                    return part
    if kind is None:
        often = _how_often(sentences, question, whole)
        if often:
            return often
        found = _not_a_figure(sentences, question, whole, reply)
        if found:
            return found
        named = _the_part_they_named(sentences, question, whole)
        if named:
            return named
        for guess in ("time", "money", "distance", "amount", "heat"):
            one = _the_item_they_named(piece or reply, guess, question)
            if one:
                part = tidy(one)
                if part and flat(part) != whole:
                    return part
        if piece and (FOLLOW_UP.search(flat(question)) or YES_NO.search(flat(question))
                      or ASKS_ABOUT_IT.search(flat(question))):
            said = tidy(piece)
            if not _informative(piece) or _cuts_a_list(piece, reply):
                holder = [one for one in sentences if flat(piece) in flat(one)]
                longer = tidy(holder[0]) if holder else None
                if longer and len(longer.split()) > len(said.split()) \
                        and flat(longer) != whole:
                    return longer
            if said and flat(said) != whole:
                return said
        return None
        return None
    wait = bool(WAIT.search(question))
    skipped_a_cut_off = False
    for sentence in sentences:
        if not SIGNALS[kind].search(sentence):
            continue
        both = _a_figure_each(sentence, kind)
        if both:
            one = _the_half_they_named(both, question)
            if one:
                part = tidy(one)
                if part and flat(part) != whole:
                    return part
        if wait and kind == "time" and not WAIT.search(sentence):
            continue
        part = _part(sentence, kind, question)
        if part is NO_LENGTH:
            continue
        if part and _at_another_place(sentence, part, question):
            continue
        if part and part is not NO_LENGTH and _a_length_of_a_doing(sentence, part, question):
            continue
        if part and part is not NO_LENGTH and _a_cut_off_not_a_length(sentence, part):
            skipped_a_cut_off = True
            continue
        if part:
            part = tidy(_as_a_length(part))
            if part and flat(part) != whole:
                holder = _the_sentence_a_figure_hangs_on(part, sentence, whole, when_ask)
                if holder:
                    return holder
                return part
        if when_ask:
            return _the_answer_said_again(sentences, whole)
        if skipped_a_cut_off:
            continue
        return None
    if kind == "time" and (LENGTH_OF_THE_JOB.search(flat(question))
                           or _STATE_LENGTH_ASKS.search(flat(question))):
        said = _the_time_it_does_keep(sentences, whole)
        if said:
            return said
    return None


NO_SET_TIME = "No set time on that one - "
A_STAGE = ("It's a stage rather than a set stretch: {when} is where it starts.",)
A_START_LEAD = re.compile(r"\b(?:around|about|at|by|from|after|past)\s+$", re.I)


def _the_start_age(sentence, figure, at):
    flat_sentence = flat(sentence) if hasattr(sentence, "split") else str(sentence)
    try:
        before = flat_sentence[max(0, at - 24):at]
    except Exception:
        return None
    lead = A_START_LEAD.search(before)
    if lead:
        return " ".join((lead.group(0).strip() + " " + figure).split())
    return " ".join(figure.split())



def _the_time_it_does_keep(sentences, whole):
    start_age = None
    for sentence in sentences:
        if not SIGNALS["time"].search(sentence):
            continue
        timed, last_end = [], -1
        for match in SIGNALS["time"].finditer(sentence):
            if match.start() < last_end:
                continue
            last_end = match.end()
            if IN_A_RELATIVE.search(sentence[:match.start()]):
                continue
            if FREQUENCY_AFTER.match(match.group(0)) \
                    and not _a_period_of_extent(sentence, match.start()):
                continue
            if FREQUENCY_AFTER.match(sentence[match.end():]):
                continue
            timed.append(match)
        if not timed:
            continue
        if LENGTH_OF_THE_JOB.search(sentence) or re.search(r"\bdepends\b", sentence, re.I):
            continue
        if start_age is None and all(_a_cut_off_not_a_length(sentence, match.group(0))
                                     for match in timed):
            one = timed[0]
            start_age = _the_start_age(flat(sentence), one.group(0), one.start())
        clause = None
        for one in re.split(r"\s*(?:;|,\s*(?:and|but|so)\b)", sentence.strip()):
            one = one.strip(" .,")
            if _only_a_cut_off(one) or not _says_a_time(one):
                continue
            clause = one
            break
        if clause is None:
            continue
        if len(clause.split()) < 3 or len(clause.split()) > 24:
            continue
        if flat(clause) == whole:
            continue
        return NO_SET_TIME + clause[0].lower() + clause[1:] + "."
    if start_age:
        return A_STAGE[0].format(when=start_age)
    return None


_A_PERIOD_OF_EXTENT = re.compile(
    r"\b(?:until|till|til|from|after|by|for|about|around|up to|past|through|over|under|beyond)\s+"
    r"(?:about\s+|around\s+|roughly\s+|nearly\s+|almost\s+|just\s+)?$", re.I)


def _a_period_of_extent(sentence, at):
    return bool(_A_PERIOD_OF_EXTENT.search(flat(sentence)[:at]))


def _says_a_time(clause):
    return bool(SIGNALS["time"].search(clause)
                or re.search(r"\b(?:long|longer|slow|quick|soon|never|until|till|months?|weeks?|"
                             r"years?|days?|hours?|minutes?)\b", clause, re.I))


def _only_a_cut_off(clause):
    figures = [match.group(0) for match in SIGNALS["time"].finditer(clause)]
    if not figures:
        return False
    return all(_a_cut_off_not_a_length(clause, figure) for figure in figures)


def _the_answer_said_again(sentences, whole):
    if len(sentences) < 2:
        return None
    opening = tidy(sentences[0])
    if not opening or flat(opening) == whole or len(opening.split()) > 30:
        return None
    return opening


A_WHEN_WORD = re.compile(r"\b(?:within|by|in|on|at|from|after|before|until|till|til|since|every"
                         r"|each|during|over|under|about|around|past|for|of)\b", re.I)


def _the_sentence_a_figure_hangs_on(part, sentence, whole, when_ask=False):
    if not when_ask:
        return None
    if A_WHEN_WORD.search(part) or len(part.split()) > 4:
        return None
    holder = tidy(sentence)
    if not holder or flat(holder) == whole or len(holder.split()) > 25:
        return None
    if flat(part).strip(" .,;:!?") not in flat(holder):
        return None
    return holder


ASKS_FREQUENCY = re.compile(r"\bhow (?:often|regularly|frequently)\b|\bhow many times\b", re.I)

FREQUENCY = re.compile(
    r"\bonce (?:a|an|every|per|or twice|in a)\b"
    r"|\b(?:twice|thrice|nightly|daily|weekly|fortnightly|monthly|yearly|annually)\b"
    r"|\b(?:two|three|four|five|six|seven|eight|ten|twelve) (?:times|sessions|days|nights"
    r"|weeks|months|years) (?:a|per|each)\b"
    r"|\b(?:two|three|four) (?:or|to) (?:three|four|five) (?:times|sessions|days|nights)\b"
    r"|\bevery (?:(?:couple|few|other|one|two|three|four|six|twelve|\d+)\s+(?:of\s+)?)?"
    r"(?:day|week|month|year|morning|evening|night|fortnight)s?"
    r"|\bnot on a fixed\b", re.I)

FREQUENCY_IGNORE = frozenset("""
often regular regularly frequent frequently times time many much usually normally should
shall need needs want wants how do does did i we you they it them the a an of for in on at
winter summer spring autumn fall morning evening night day week month year now
and but so then or also plus because while which
""".split())

ASKED_UNIT = re.compile(r"\bhow many\s+(seconds?|secs?|minutes?|mins?|hours?|hrs?|days?"
                        r"|weeks?|months?|years?)\b", re.I)
_UNITS = {"second": "second", "sec": "second", "minute": "minute", "min": "minute",
          "hour": "hour", "hr": "hour", "day": "day", "week": "week", "month": "month",
          "year": "year"}


def _unit_stem(word):
    bare = str(word or "").strip(".,;:!?").lower().rstrip("s")
    return _UNITS.get(bare, bare)

RATE_FREQ = re.compile(r"\b(?:a|an|per|each) (?:day|week|month|year)\b", re.I)

FREQ_CLAUSE = re.compile(r";\s*|(?<=[.!?])\s+|,\s+(?:and|but|so|then)\s+")


def _same_word(one, other):
    if one == other:
        return True
    short = 4 if min(len(one), len(other)) >= 4 else 3
    return one[:short] == other[:short]


def _names_one_of(wanted, words):
    return any(_same_word(word, said) for word in wanted for said in words)


TRIGGER_PATTERN = (r"\b(?:whenever|when|as soon as|if)\s+(?:it\s+|they\s+|you\s+)?"
                   r"(?:needs?|starts?|looks?|furs?|smells?|sounds?|shows?|gets?|builds?|feels?"
                   r"|goes?|is\b)")
TRIGGER = re.compile(TRIGGER_PATTERN, re.I)

RATE_INTERVAL = re.compile(
    r"\bonce (?:a|an|every|per|or twice|in a)\b"
    r"|\b(?:twice|thrice)\s+(?:a|an|per|each|every|daily|weekly|monthly|yearly|nightly)\b"
    r"|\b(?:daily|weekly|fortnightly|monthly|yearly|annually|nightly)\b"
    r"|\b(?:two|three|four|five|six|seven|eight|ten|twelve) (?:times|sessions|days|nights"
    r"|weeks|months|years) (?:a|per|each)\b"
    r"|\bevery (?:other )?(?:day|week|fortnight|month|year|morning|evening|few|couple|\d+)\b"
    r"|\bevery (?:month|week|day|year) or (?:two|so)\b"
    + "|" + TRIGGER_PATTERN)

A_BARE_COUNT = re.compile(r"\b(?:once|twice|thrice|(?:" 
                          r"two|three|four|five|ten) times)\b(?!\s*(?:a|an|per|each|every|"
                          r"daily|weekly|monthly|yearly|nightly|or\b|in a\b))", re.I)


def _only_a_count(piece):
    found = list(FREQUENCY.finditer(piece))
    if not found:
        return False
    return all(A_BARE_COUNT.match(match.group(0)) or match.group(0).lower().strip() in
               ("once", "twice", "thrice") for match in found) and \
        not RATE_INTERVAL.search(piece)


ONLY_THE_INTERVAL_ASK = re.compile(
    r"^\s*(?:and |also |so |ok |okay |oh |right )*"
    r"(?:how (?:often|regularly|frequently)|how many times)"
    r"(?:\s+(?:should|do|would|must|need|needs|shall)\s+(?:i|we|you))?"
    r"(?:\s+(?:i|we)\s+(?:need|have|ought)\s+to)?"
    r"(?:\s+do(?:es)?\s+(?:that|it|this|so))?"
    r"(?:\s+(?:do|does)\s+(?:i|we)\s+need\s+to)?"
    r"(?:\s+(?:it|that|this|them|those))?"
    r"(?:\s+(?:again|then|now|really))?"
    r"\s*[?.!]*\s*$", re.IGNORECASE)

NO_INTERVAL_SAID = ("The steps don't say how often, and I'd rather not make a number up - go by "
                    "when it needs doing again rather than by a calendar.")


A_HOW_OFTEN_THE_DOING = re.compile(
    r"\b(?:how often|how many times|how regularly|how frequently)\b"
    r".*\b(?:it|that|this|them|those)"
    r"(?:\s+(?:up|out|down|off|in|on|round|around|over|through|away|back|again|properly|too))?"
    r"\s*[?.!]*\s*$", re.IGNORECASE)


def _how_often(sentences, question, whole):
    if not ASKS_FREQUENCY.search(flat(question)):
        return None
    wanted = {word for word in words_of(question)
              if word not in NAMING_IGNORE and word not in FREQUENCY_IGNORE and len(word) > 2}
    rates = []
    counted = None
    for sentence in sentences:
        about = bool(wanted) and _names_one_of(wanted, words_of(sentence))
        clause = _freq_clause(sentence, weak=about or not wanted,
                              wanted=wanted if about else frozenset())
        if not clause:
            continue
        if wanted and not about:
            continue
        said = tidy(clause)
        if not said or flat(said) == whole:
            continue
        if FREQUENCY.search(flat(said)) and not _only_a_count(said):
            return said
        if _only_a_count(said):
            counted = counted or said
            continue
        rates.append(said)
    for said in rates:
        if _only_a_count(said):
            counted = counted or said
            continue
        if not (FREQ_LIMIT.search(said) or FREQ_PORTION.search(said)):
            return said
    if counted:
        return counted
    if rates:
        return rates[0]
    for sentence in sentences:
        if TRIGGER.search(sentence) and re.search(r"\bagain\b", sentence, re.I):
            said = tidy(sentence)
            if said and flat(said) != whole:
                return said
    opening = sentences[0].strip() if sentences else ""
    first_word = opening.split()[0].strip(",.;:").lower() if opening.split() else ""
    the_doing = bool(A_HOW_OFTEN_THE_DOING.search(flat(question)) and wanted and first_word
                     and _names_one_of(wanted, [first_word]))
    if ((ONLY_THE_INTERVAL_ASK.match(question) or the_doing)
            and not RATE_INTERVAL.search(whole) and A_SET_OF_STEPS.search(whole)):
        return NO_INTERVAL_SAID
    return rates[0] if rates else None


FREQ_LIMIT = re.compile(r"\b(?:never|no more than|not more than|at most|at least|less than|"
                        r"more than|up to|until|before)\b", re.I)
FREQ_PORTION = re.compile(r"\d+\s*(?:g|kg|ml|cl|l|oz)\b|\b(?:pouches?|grams?|tins?|cans?|"
                          r"packets?|litres?|liters?|sachets?)\b", re.I)


def _counts_on_the_answer(piece):
    return bool(re.search(r"\b(?:the same|same count|that count|as above|as before)\b", piece, re.I))


def _freq_clause(sentence, weak=False, wanted=frozenset()):
    pieces = [piece.strip(" ,;:") for piece in FREQ_CLAUSE.split(sentence) if piece.strip(" ,;:")]
    found = [piece for piece in pieces
             if FREQUENCY.search(piece) or (weak and RATE_FREQ.search(piece))]
    if not found:
        return None
    if len(sentence.split()) <= 30:
        return sentence
    if wanted:
        found = [piece for piece in found if _names_one_of(wanted, words_of(piece))]
        if not found:
            return None
    plain = [piece for piece in found if not _counts_on_the_answer(piece)] or found
    piece = plain[0]
    if len(plain) > 1 and re.match(r"(?:then|and|also|plus|after that|afterwards)\b", piece, re.I):
        piece = plain[1]
    if len(piece.split()) <= 3 and len(found) > 1:
        piece = " ".join(found[-2:])
    if len(piece.split()) > 14:
        parts = [part.strip(" ,;:") for part in re.split(r",\s*", piece) if part.strip(" ,;:")]
        at = [index for index, part in enumerate(parts) if FREQUENCY.search(part)]
        if at:
            last = at[-1]
            piece = parts[last]
            if len(piece.split()) <= 5 and last:
                piece = parts[last - 1] + ", " + piece
    return piece if len(piece.split()) >= 2 else None

def _dated(sentences, question, whole):
    wanted = set(words_of(question))
    for word in list(wanted):
        wanted.update(SAME.get(word, ()))
    best, best_score = None, (-1, -1)
    for sentence in sentences:
        if not has_a_date(sentence):
            continue
        score = (1 if DATED_STRONG.search(sentence) else 0,
                 len(wanted.intersection(words_of(sentence))))
        if score > best_score:
            best, best_score = sentence, score
    if best is None or flat(best) == whole:
        return None
    return tidy(best)


ASKS_FOR_A_HAND = re.compile(r"\b(?:tips?|tricks?|hacks?|advice|pointers?|suggestions?|ideas?)\b", re.I)
NAMES_A_PART = 2


def _the_part_they_named(sentences, question, whole):
    if not ASKS_FOR_A_HAND.search(flat(question)):
        return None
    sentence = _by_words(sentences, question)
    if not sentence:
        return None
    shared = set(words_of(question)) & set(words_of(sentence))
    if len(shared) < NAMES_A_PART:
        return None
    said = tidy(sentence)
    if said and flat(said) != whole:
        return said
    return None


def _not_a_figure(sentences, question, whole, reply=None):
    option = _by_option(sentences, question)
    if option and flat(option) != whole:
        return _with_the_script(option, sentences, reply) or tidy(option)
    step = _by_step(sentences, question)
    if step and flat(step) != whole:
        return _with_the_script(step, sentences, reply) or tidy(step)
    if _property_ask(question):
        sentence = _by_words(sentences, question)
        if sentence and flat(sentence) != whole:
            return tidy(sentence)
    return None


def _named_clause(answer, question):
    named = [word for word in words_of(question)
             if word not in NAMING_IGNORE and len(word) > 2]
    if not named:
        return None
    pairs = [(named[i], named[i + 1]) for i in range(len(named) - 1)]
    pieces = [piece.strip() for piece in
              pieces_of(" ".join(str(answer or "").split()),
                        r";\s*|(?<=[.!?])\s+|,\s+(?:and|but|so)\s+|\s+(?:and|but|so)\s+")
              if piece.strip()]
    roots = {_root(word) for word in named}
    pieces = clauses(" ".join(str(answer or "").split()), NAMED_BREAK)
    best, best_score, best_count = None, 0, 0
    for piece in pieces:
        said = flat(piece)
        score = len([pair for pair in pairs if _says(said, " ".join(pair))]) if pairs else 0
        if not score:
            score = len({_root(word) for word in words_of(piece)}.intersection(roots))
        if score > best_score:
            best, best_score, best_count = piece, score, 1
        elif score == best_score and score:
            best_count += 1
    if not best or best_count != 1:
        return None
    if not roots <= {_root(word) for word in words_of(answer)}:
        return None
    return best.rstrip(".!?,;: ")


def _root(word):
    for ending in ("ing", "ed", "es", "s"):
        if len(word) > len(ending) + 2 and word.endswith(ending):
            word = word[:-len(ending)]
            break
    return word[:-1] if len(word) > 3 and word.endswith("e") else word


def _says(text, phrase):
    pattern = r"\b" + r"[a-z]*\s+".join(re.escape(word) for word in phrase.split()) + r"[a-z]*\b"
    return re.search(pattern, flat(text)) is not None


def _informative(piece):
    return bool(re.search(r"\d", piece) or COOKS.search(piece) or WAIT.search(piece))


def _cuts_a_list(piece, answer):
    said = " ".join(str(piece or "").split())
    whole = " ".join(str(answer or "").split())
    if not said or said not in whole:
        return False
    rest = whole[whole.index(said) + len(said):]
    return bool(re.match(r"\s*(?:[,;]|\band\b)", rest))


def _with_unit(piece, reply):
    text = piece.strip()
    if not BARE_RANGE.search(text) or UNIT.search(text[-12:]):
        return text
    before = flat(reply)
    at = before.find(flat(text))
    units = list(UNIT.finditer(before if at < 0 else before[:at]))
    if not units:
        return text
    return text + " " + units[-1].group(0)


def _property_ask(question):
    if not re.search(r"\bhow (?:do|can|should|would|could) (?:i|we|you)\b", flat(question)):
        return False
    if OWN_SAVING.search(flat(question)):
        return False
    return any(word in SAME for word in words_of(question))


OWN_SAVING = re.compile(r"\b(?:start|begin|keep|stop|try|need|want)\s+(?:to\s+)?sav(?:e|ing)\b"
                        r"|\bsav(?:e|ing)\s+(?:up\b|money\b|for\b)", re.I)


def _option_ask(question):
    clean = flat(question)
    return bool(OPTION.search(clean) and QUALIFIER.search(clean) and not NOT_OPTION.search(clean)
                and len(words_of(clean)) <= 8)


def _stands_alone(piece):
    text = str(piece or "").strip()
    if not text:
        return False
    if re.search(r"\d", text):
        return True
    return len(words_of(text)) >= 2


def _by_option(sentences, question):
    qualifier = QUALIFIER.search(question)
    if not qualifier:
        return None
    for sentence in sentences:
        clause = _clause_with(sentence, qualifier.group(0))
        if clause and flat(clause) != flat(sentence):
            if _only_a_qualifier(clause):
                return sentence
            return clause if _stands_alone(clause) else sentence
    return None


def _only_a_qualifier(clause):
    words = [word for word in words_of(clause) if word not in QUALIFIER_FILLER]
    return bool(words) and all(word in QUALIFIER_WORDS for word in words)


SAYS_SOMETHING = re.compile(r"^(?:and |then |so )?(?:say|tell|ask|text|message|write|word|phrase"
                            r"|reply|mention|bring|raise|broach)\b", re.I)
BAREST_VERDICT = 24


def _by_step(sentences, question):
    if not YES_NO.search(flat(question)):
        return None
    wanted = set(words_of(question))
    step = step_word(question)
    if step:
        wanted = {step} | set(SAME.get(step, ()))
    for sentence in sentences:
        raw = WORD.findall(flat(sentence))
        if not raw:
            continue
        first = raw[0]
        if len(first) > 3 and first.endswith("s") and not first.endswith("ss"):
            first = first[:-1]
        if first in wanted:
            cut = re.split(r"[:,]\s+", sentence.strip())[0].strip() or sentence
            return cut if _stands_alone(cut) else sentence.strip()
    return None


def _with_the_script(part, sentences, reply=None):
    head = str(part or "").strip().strip(".?! ")
    said = flat(head)
    if not said or len(said) > BAREST_VERDICT or " " not in said:
        return None
    if not SAYS_SOMETHING.match(said):
        return None
    whole_answer = [one.strip() for one in SENTENCE.split(str(reply or "").strip()) if one.strip()]
    if not whole_answer:
        whole_answer = sentences
    for at, sentence in enumerate(whole_answer):
        if flat(sentence).startswith(said):
            words = _the_quotation(_to_the_end_of_the_script(whole_answer, at))
            if not words:
                return None
            return '%s, like this: %s' % (head, words)
    return None


QUOTED_WORDS = re.compile(r'"[^"]{10,}"')
QUOTED_WORDS_SINGLE = re.compile(r"(?::\s|,\s)'(.{10,}?[.?!])'(?=\s|$)")


def _the_quotation(sentence):
    text = str(sentence or "")
    found = QUOTED_WORDS.search(text)
    if found:
        return found.group(0).strip()
    found = QUOTED_WORDS_SINGLE.search(text)
    if found:
        return "'%s'" % found.group(1).strip()
    return None


def _to_the_end_of_the_script(sentences, at):
    text = sentences[at].strip()
    index = at
    while index + 1 < len(sentences) and text.count('"') % 2:
        index += 1
        text = text + " " + sentences[index].strip()
    return text


def _by_words(sentences, question):
    wanted = set(words_of(question))
    for word in list(wanted):
        wanted.update(SAME.get(word, ()))
    if not wanted:
        return None
    best, best_score, best_length = None, 0, 0
    for sentence in sentences:
        score = len(wanted.intersection(words_of(sentence)))
        length = len(words_of(sentence))
        if score and (score > best_score or (score == best_score and length < best_length)):
            best, best_score, best_length = sentence, score, length
    return best


DURATION_ADJECTIVE = re.compile(r"\b(\d+(?:\.\d+)?)\s*[-–]\s*"
                                r"(minutes?|mins?|hours?|hrs?|days?|weeks?|months?|years?)\b",
                                re.I)


def _as_a_length(text):
    def say(match):
        number, unit = match.group(1), match.group(2).lower()
        if number not in ("1", "1.0") and not unit.endswith("s"):
            unit += "s"
        return number + " " + unit
    return DURATION_ADJECTIVE.sub(say, str(text))


POINTS_BACK = frozenset("until till til whole thing things".split())


def _names_a_thing(question):
    return any(word not in ASKING_ONLY and word not in POINTS_BACK
               for word in words_of(flat(question)))


CARRIES_ON = re.compile(
    r"^\s*(?:and|so|also|then|but|ok|okay|right|plus|same|also|what about|how about|what of)\b",
    re.I)

EITHER_OR = re.compile(r"\d[^.;]{0,40}\bor\b[^.;]{0,40}\d", re.I)
FIGURE_MEASURE = re.compile(r"\d+(?:\.\d+)?\s*(?:to\s*\d+(?:\.\d+)?\s*)?[-\u2013]?\s*([a-z%]+)",
                            re.I)


def _measure(span):
    found = FIGURE_MEASURE.search(str(span or ""))
    return found.group(1).lower() if found else ""


def _figure(match, text):
    text = str(text or "")
    start = match.start()
    left = start
    while left > 0 and (text[left - 1].isdigit() or text[left - 1] in ",."):
        left -= 1
    if left == start:
        return match.group(0)
    return text[left:match.end()].lstrip(".,")


def _a_figure_each(sentence, kind):
    figure = SPANS.get(kind)
    if not figure or ";" not in str(sentence or ""):
        return None
    halves = [one.strip() for one in sentence.split(";") if one.strip()]
    if len(halves) < 2:
        return None
    stated = any(figure.search(one) for one in halves)
    if not stated:
        return None
    if any(not (figure.search(one) or BARE_RANGE.search(one.rstrip(".!?"))) for one in halves):
        return None
    return halves


A_UNIT_WORD = re.compile(r"\b(seconds?|secs?|minutes?|mins?|hours?|hrs?|days?|weeks?|months?"
                         r"|years?)\b")
A_BARE_RANGE = re.compile(r"\b\d+(?:\.\d+)?\s*(?:-|to|or|and|\u2013)\s*\d+(?:\.\d+)?\b")
A_FOR_A_THING = re.compile(r"\s*(?:seconds?|secs?|minutes?|mins?|hours?|hrs?|days?|weeks?"
                           r"|months?|years?)?\s*for\b", re.I)


def _the_item_they_named(sentence, kind, question):
    figure = SPANS.get(kind)
    if not figure:
        return None
    said = set(words_of(flat(question)))
    if not said:
        return None
    body = sentence.split(":", 1)[1] if ":" in sentence else sentence
    starts = re.compile(figure.pattern + "|" + A_BARE_RANGE.pattern, re.I)
    found = [match for match in starts.finditer(body)
             if not _a_frequency(body, match.end())]
    if len(found) < 2:
        return None
    items = []
    for index, match in enumerate(found):
        stop = found[index + 1].start() if index + 1 < len(found) else len(body)
        items.append((match.group(0), body[match.start():stop]))
    if any(not A_FOR_A_THING.match(piece, len(span)) for span, piece in items):
        return None
    scored = [(len(said & set(words_of(piece))), piece) for _, piece in items]
    best = max(score for score, _ in scored)
    winners = [piece for score, piece in scored if score == best]
    if best == 0 or len(winners) != 1:
        return None
    item = re.sub(r"[\s,]*(?:and|or)?[\s,]*$", "", winners[0].strip())
    if not A_UNIT_WORD.search(item):
        unit = next((A_UNIT_WORD.search(one) for _, one in items if A_UNIT_WORD.search(one)), None)
        if not unit:
            return None
        head = A_BARE_RANGE.search(item)
        split = head.end() if head else len(item)
        item = item[:split] + " " + unit.group(0).lower() + item[split:]
    return item


def _the_half_they_named(halves, question):
    said = set(words_of(flat(question)))
    if not said:
        return None
    scored = [(len(said & set(words_of(one))), one) for one in halves]
    best = max(score for score, _ in scored)
    winners = [one for score, one in scored if score == best]
    if best == 0 or len(winners) != 1:
        return None
    return winners[0]


IN_A_RELATIVE = re.compile(r"\b(?:who|which|whose)\b", re.I)
A_WEATHER_WINDOW = re.compile(
    r"\b(?:forecast|rain|showers?|dry|damp|frost|wind|sunshine?|weather|mild|warm|cold)\b"
    r"[^.;:,]{0,25}\bfor\s+$", re.I)
AT_A_TIME = re.compile(r"^\s*(?:at a time|to warm up|to cool|of it)\b", re.I)
IN_A_CONDITION = re.compile(r"\b(?:if|unless|when|whenever|once)\b", re.I)
A_BOUNDED = re.compile(r"\b(?:more than|less than|at least|at most|up to|within|over|under"
                       r"|no more than|not more than)\s+$", re.I)
A_STATE_FOR = re.compile(r"\b(?:gone on|been|lasted|going on|had (?:it|this|that))\b"
                         r"[^.;:]{0,30}\bfor\s+$", re.I)
A_RELATIVE_AFTER = re.compile(
    r"^\s*(?:before|after)\s+(?!you\b|i\b|we\b|they\b|it\b|he\b|she\b|\w+ing\b)\w", re.I)


def _a_condition(sentence, match):
    if AT_A_TIME.match(sentence[match.end():]):
        return True
    if A_RELATIVE_AFTER.match(sentence[match.end():]):
        return True
    before = sentence[:match.start()]
    if IN_A_CONDITION.search(before) and A_BOUNDED.search(before):
        return True
    if A_STATE_FOR.search(before):
        return True
    if A_WEATHER_WINDOW.search(before):
        return True
    return bool(IN_A_RELATIVE.search(before))


def _part(sentence, kind, question):
    figure = SPANS.get(kind)
    qualifier = QUALIFIER.search(question)
    if qualifier:
        clause = _clause_with(sentence, qualifier.group(0))
        if clause:
            found = [_figure(match, clause) for match in figure.finditer(clause)] if figure else []
            if found:
                return found[-1]
            if re.search(r"\d", clause):
                return clause
    spans = [_figure(match, sentence) for match in figure.finditer(sentence)] if figure else []
    if kind == "time" and spans and LENGTH_OF_THE_JOB.search(flat(question)):
        lengths = [_figure(match, sentence) for match in figure.finditer(sentence)
                   if not _a_frequency(sentence, match.end(), match.start())
                   and not (A_MOMENT.fullmatch(match.group(0).strip())
                            and not A_COUNTDOWN.search(flat(question)))
                   and not _a_condition(sentence, match)]
        if not lengths:
            return NO_LENGTH
        lead = RATE_LEAD.match(sentence)
        if lead and figure.search(lead.group(0)):
            cut = sentence[lead.end():].strip()
            if cut and figure.search(cut):
                sentence = cut
                lengths = [_figure(match, sentence) for match in figure.finditer(sentence)
                           if not _a_frequency(sentence, match.end(), match.start())]
        spans = lengths
    if kind == "time" and spans and not LENGTH_OF_THE_JOB.search(flat(question)):
        rates = [_figure(match, sentence) for match in figure.finditer(sentence)
                 if _a_frequency(sentence, match.end(), match.start())]
        lengths = [_figure(match, sentence) for match in figure.finditer(sentence)
                   if not _a_frequency(sentence, match.end(), match.start())]
        if rates and lengths:
            return rates[0]
    if not spans:
        if kind == "clock":
            return None
        return sentence if len(sentence.split()) <= 28 else None
    wanted_unit = ASKED_UNIT.search(question or "")
    if kind == "time" and wanted_unit and len(spans) > 1:
        unit = _unit_stem(wanted_unit.group(1))
        same = [span for span in spans if _unit_stem(span.split()[-1]) == unit]
        if len(same) == 1:
            return same[0]
    if kind == "amount":
        return _clause(sentence, question) or sentence
    if kind in ("money", "distance"):
        return spans[0]
    if RATE.search(question):
        wanted = [span for span in spans if re.search(r"\bper\b|\ba\b", span, re.I)]
        if not wanted:
            return None
        if len(spans) > 1 and re.search(r"\b(?:takes|so)\b", sentence, re.I):
            return sentence
        return wanted[0]
    options = re.findall(r"\b\d+(?:[^,.;:]{0,18}?)\bfor\b", sentence, re.I)
    if len(options) >= 2:
        return None
    if kind == "time" and BEFORE.search(question):
        result = [_figure(match, sentence) for match in RESULT.finditer(sentence)]
        if result:
            return result[-1]
    if len(spans) > 1 and not SEQUENCE.search(sentence):
        lead = re.split(r"[:,;]\s+|\s+-\s+", sentence.strip())[0]
        lead_spans = [match.group(0) for match in SPANS.get(kind, ()).finditer(lead)]
        rest = [span for span in spans if span not in lead_spans]
        if len(lead_spans) == 1 and any(_measure(span) != _measure(lead_spans[0])
                                        for span in rest):
            return lead_spans[0]
    if len(spans) == 1:
        return spans[0]
    stepped = _step_time(sentence, question, figure)
    if stepped:
        return stepped
    if SEQUENCE.search(sentence) and not WAIT.search(question):
        return spans[-1]
    if (not _names_a_thing(question) and CARRIES_ON.search(question)
            and not re.search(r"\bper\b", spans[0], re.I)
            and not EITHER_OR.search(sentence)):
        return _clause_holding(sentence, spans[0]) or spans[0]
    return _clause(sentence, question) or sentence


def _canonical(word):
    return "oven" if word in OVEN else word


def _a_frequency(sentence, end, start=None):
    after = sentence[end:]
    if start is not None and FREQUENCY_BEFORE.search(sentence[:start]):
        return True
    return bool(FREQUENCY_AFTER.match(after) or FREQUENCY_AFTER_TIMES.match(after)
                or FREQUENCY_AFTER_AT_A_TIME.match(after))


def _same_step(asked, words):
    if {_canonical(word) for word in asked} & {_canonical(word) for word in words}:
        return True
    for mine in asked:
        for theirs in words:
            short, long_ = (mine, theirs) if len(mine) <= len(theirs) else (theirs, mine)
            if len(short) >= 4 and len(long_) - len(short) >= 2 and short in long_:
                return True
    return False


def _step_time(sentence, question, figure):
    asked = {word.rstrip("s") for word in words_of(question) if len(word) > 3}
    pieces = []
    for piece in (one.strip() for one in STEP.split(sentence) if one.strip()):
        if pieces and BARE_UNIT.match(piece):
            pieces[-1] = pieces[-1] + " and " + piece
        else:
            pieces.append(piece)
    if not (SEQUENCE.search(sentence) or AFTER.search(sentence)):
        places = {word for piece in pieces for word in words_of(piece) if word in WHERE}
        if len(places) < 2:
            return None
    if len(pieces) < 2:
        return None
    named, cooking, waiting = [], [], []
    for piece in pieces:
        found = [_figure(match, piece) for match in figure.finditer(piece)] if figure else []
        if not found:
            continue
        if KEEPS.search(piece):
            continue
        words = {word.rstrip("s") for word in words_of(piece) if len(word) > 3}
        waiting_here = bool(AFTER.search(piece))
        (waiting if waiting_here else cooking).append(found[-1])
        if _same_step(asked, words) and not (waiting_here and not WAIT.search(question)):
            named.append(found[-1])
    if not (SEQUENCE.search(sentence) or AFTER.search(sentence) or named):
        return None
    if asked:
        if len(named) == 1:
            return named[0]
        if named:
            return None
    if WAIT.search(question) and waiting:
        return waiting[-1]
    if len(set(cooking)) > 1:
        return None
    if cooking:
        return cooking[-1]
    return waiting[-1] if waiting else None


ASIDE = re.compile(r"\s+-(?!\s*-)[^-;.!?]{1,200}?-\s+"
                   r"|[\u2014\u2013][^\u2014\u2013]{1,200}?[\u2014\u2013]"
                   r"|\([^()]{1,200}\)")
ASIDE_ON = re.compile("(?:" + ASIDE.pattern + r")(?:(?:and|but|so)\s+|,\s*|;\s*)?")
HELD = re.compile(r"\x01(\d+)\x01")


def _aside_held(text):
    kept = []

    def hide(match):
        kept.append(match.group(0).strip())
        return " \x01%d\x01 " % (len(kept) - 1)

    return ASIDE_ON.sub(hide, str(text or "")), kept


def _aside_back(piece, kept):
    return " ".join(HELD.sub(lambda match: kept[int(match.group(1))], piece).split())


def clauses(text, pattern):
    return clauses_bare(text, pattern)[0]


def clauses_bare(text, pattern):
    held, kept = _aside_held(text)
    pieces, bare = [], []
    for piece in pieces_of(held, pattern):
        dressed = _aside_back(piece, kept).strip(" ,;:")
        if not dressed:
            continue
        pieces.append(dressed)
        bare.append(" ".join(HELD.sub(" ", piece).split()).strip(" ,;:"))
    return pieces, bare


NAMED_BREAK = re.compile(r";\s*|(?<=[.!?])\s+|,\s+(?:and|but|so)\s+|\s+(?:and|but|so)\s+")
LEANING = re.compile(r"^(?:or|and|but|so|plus|also)\b", re.I)
CLAUSE_BREAK = re.compile(r"(?:;\s*|,(?!\d)\s*|\s+(?:and|but|so)\s+)")
CLAUSE_BREAK_COLON = re.compile(r"(?:;\s*|,(?!\d)\s*|\s+(?:and|but|so)\s+|:\s*)")


def _clause(text, question):
    wanted = set(words_of(question))
    if not wanted:
        return None
    pieces, bare = clauses_bare(text, CLAUSE_BREAK)
    if len(pieces) < 2:
        return None
    scores = [len(wanted.intersection(words_of(piece))) for piece in bare]
    best = max(scores)
    if best and scores.count(best) == 1:
        piece = pieces[scores.index(best)]
        return None if LEANING.match(piece) else piece
    return None


def _clause_with(text, word):
    pieces = clauses(text, CLAUSE_BREAK_COLON)
    hits = [piece for piece in pieces if re.search(r"\b" + re.escape(word) + r"\b", piece, re.I)]
    return hits[0] if len(hits) == 1 else None


def _clause_holding(text, span):
    pieces = [piece.strip() for piece in pieces_of(text, CLAUSE_BREAK_COLON)
              if piece and piece.strip()]
    hits = [piece for piece in pieces if span in piece]
    return hits[0] if len(hits) == 1 else None


def words_of(text):
    found = []
    for word in WORD.findall(flat(text)):
        word = word.strip("'")
        if not word or word in EMPTY:
            continue
        if len(word) > 3 and word.endswith("s") and not word.endswith("ss"):
            word = word[:-1]
        if word not in found:
            found.append(word)
    return found


def flat(text):
    return " ".join(str(text or "").lower().split())


def tidy(text):
    if not isinstance(text, str):
        return None
    text = " ".join(text.split()).strip().rstrip(",;:")
    if not text:
        return None
    if text[0].islower():
        text = text[0].upper() + text[1:]
    if not text.endswith((".", "!", "?")):
        text += "."
    return text
