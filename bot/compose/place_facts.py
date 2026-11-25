import re

PLACE_ASKS = re.compile(
    r"(?:\b(?:do|does|did)\s+(?:they|it)\s+(?:have|got|do|offer|allow|take|sell|serve|provide|"
    r"accept|permit|charge)\b"
    r"|\b(?:do|does|did)\s+(?:the|this|that|these|those|a|an|my|our|your)\s+"
    r"(?:[a-z'-]+\s+){0,2}(?:have|got|do|offer|allow|take|sell|serve|provide|accept|permit|"
    r"charge)\b"
    r"|\b(?:is|are)\s+there\s+(?:a\s+|any\s+)?"
    r"|\bcan\s+i\s+(?:bring|take|park|book|pay|use|get)\b"
    r"|\b(?:are|is|were|was)\s+(?:the\s+|our\s+|your\s+)?"
    r"(?:dogs?|kids?|children|child|pets?)\s+(?:allowed|welcome|permitted)\b)", re.I)
PLACE_ASKS_OF_ITS_OWN = re.compile(
    r"(?:^(?:oh |and |so |are |is |were |was |do |does |did )?"
    r"(?:the\s+|our\s+|your\s+|his\s+|her\s+)?(?:dogs?|kids?|children|child)\s+"
    r"(?:allowed|welcome|ok|okay)\b"
    r"|\b(?:dog|kid|child|family)[\s-]?friendly\b"
    r"|\bdog[\s-]?friendly\b"
    r"|\b(?:is|are)\s+(?:it|they)\s+(?:good|ok|okay|suitable|fine)\s+for\b)", re.I)
PLACE_OF_ITS_OWN = (
    "car park", "car parking", "parking", "toilets", "baby change", "takeaway", "take away",
    "beer garden", "play area", "soft play", "high chairs", "highchair", "dress code",
    "step free", "wheelchair access", "wheelchair", "accessible entrance", "table service",
    "cash only", "card only", "booking fee", "cover charge",
)
PLACE_WITH_A_VENUE = (
    "pool", "swimming pool", "dogs", "dog", "kids", "children", "child", "wifi", "wi-fi",
    "vegan", "gluten free", "vegetarian", "bookings", "booking", "tables", "music", "quiz",
    "screens", "garden", "food", "menu", "delivery", "parking", "rooms",
    "cafe", "café", "coffee", "toilets", "toilet", "loo", "car park", "gift shop", "shop",
    "restaurant", "bar", "cloakroom", "lockers", "changing rooms", "baby change", "lifts",
    "step free access", "hearing loop", "picnic", "seating", "water",
)
PLACE_ASKS_WITH_NO_SUBJECT = (
    "pool", "swimming pool", "wifi", "wi-fi", "vegan",
    "gluten free", "vegetarian", "bookings", "tables", "menu", "food", "delivery",
    "parking", "rooms",
)
PLACE_ANIMALS = ("dogs", "dog")
PLACE_PERMISSION = re.compile(
    r"\b(?:allow|allows|allowed|take|takes|taking|taken|permit|permits|permitted|welcome|"
    r"welcomes|welcomed|accept|accepts|accepted|let|lets)\b", re.I)
PLACE_LETS_ANIMALS = re.compile(
    r"\b(?:do|does|did)\s+(?:they|it)\s+(?:let|lets|welcome|welcomes)\b", re.I)
BARE_PLACE_SUBJECT = re.compile(r"\b(?:do|does|did)\s+(?:they|it)\b|\b(?:is|are)\s+(?:it|they)\b")
A_BRING_ASK = re.compile(
    r"\b(?:can|could|may|am\s+i\s+allowed\s+to)\s+(?:i\s+|we\s+)?(?:bring|take)\b"
    r"[^.!?]{0,30}\b(?:dogs?|pets?|kids?|children|child|pram|buggy)\b", re.I)
A_DESTINATION = re.compile(r"\bto\b", re.I)
A_HOME_OF_THEIR_OWN = re.compile(
    r"\b(?:my|our|his|her|their|your)\s+(?:(?:new|own|old|little|small|big|rented)\s+)?"
    r"(?:flat|house|home|place|garden|car|van|caravan|room|office|desk)\b", re.I)
PLACE_IS_THERE = re.compile(r"\b(?:is|are)\s+there\b")
PLACE_VENUES = (
    "pub", "restaurant", "cafe", "café", "coffee shop", "bar", "hotel", "b&b", "guest house",
    "campsite", "caravan site", "holiday park", "gym", "leisure centre", "swimming pool",
    "museum", "gallery", "cinema", "theatre", "venue", "shop", "store", "supermarket",
    "garden centre", "station", "salon", "barber", "hairdresser", "garage", "surgery",
    "dentist", "pharmacy", "church", "village hall", "zoo", "farm park", "library", "club",
    "spa", "soft play", "bowling", "snooker hall", "arcade",
)
PLACE_LINES = (
    "That is the place's own call, and it is usually written down: their own page lists it under "
    "visiting or facilities, and somewhere you are staying puts it in the booking terms. One "
    "phone call settles it either way.",
    "Whoever runs the place decides that, and it is one of the few things they all publish: their "
    "own page lists it under visiting or facilities, a phone call in opening hours gets a straight "
    "answer, and the booking terms cover a room.",
    "I can't see inside one particular place, so the answer is theirs: it will be on their page "
    "under visiting, or in the booking terms, and the phone settles anything the page leaves out.",
)


A_DAY = re.compile(
    r"\b(?:today|tonight|tomorrow|this\s+(?:week|weekend|monday|tuesday|wednesday|thursday|"
    r"friday|saturday|sunday)|next\s+week|the\s+weekend|weekends?|"
    r"bank\s+holiday(?:\s+monday)?|(?:mon|tues|wednes|thurs|fri|satur|sun)days?)\b")
ON_A_DAY = re.compile(
    r"^\s*(?:and|so|but|also|oh|hi|hello|quick one)?\s*,?\s*"
    r"(?:(?:is|are|will|was|were)\s+[^.!?]{1,40}?"
    r"|(?:does|do)\s+(?:the|that|this|our|your|their|his|her)\b[^.!?]{0,34}?)"
    r"\s+\b(?:on|running|happening|taking\s+place|going\s+ahead)\b")
A_CLOCK_ASK = ("open", "opens", "opening", "opened", "close", "closes", "closing", "closed",
               "shut", "shuts", "shutting")
A_CROWD_ASK = ("busy", "busier", "busiest", "crowded", "packed", "rammed", "heaving", "quiet",
               "quieter", "quietest", "dead", "queues", "queue", "waiting", "how many people")
A_SWITCHED_ON_THING = (
    "heating", "boiler", "oven", "kettle", "telly", "tv", "television", "radio", "lights",
    "light", "lamp", "fan", "alarm", "immersion", "water", "hot water", "washing machine",
    "dishwasher", "tumble dryer", "dryer", "fridge", "freezer", "phone", "laptop", "fire",
    "shower", "radiator", "hob", "grill", "microwave", "sprinkler", "washer", "damp",
)
PLACE_EVENTS = (
    "market", "boot sale", "car boot", "match", "game", "fixture", "class", "classes",
    "club night", "5 a side", "five a side", "concert", "gig", "show", "fair", "fete",
    "quiz", "sale", "service", "session", "sessions", "practice", "training", "meeting",
    "event", "festival", "parade", "funfair", "playgroup", "toddler group", "story time",
    "swim", "swimming", "lesson", "lessons", "course", "workshop", "jumble", "table top",
)
PLACE_ON_A_DAY_LINES = (
    "Whether it is on that day is the organiser's own call, and it is the last thing they "
    "change: a wet pitch, a stall that cannot come, a hall that falls through - and a bank "
    "holiday moves the day a market or a class runs. Their own page or a phone call on the "
    "morning gives the yes or no.",
    "That is settled on the day itself, not from here: a market, a match or a class is called "
    "off late when the weather turns, and a bank holiday can move it to another day. Their own "
    "page or listing is where the change goes up, and the phone is answered on the morning.",
    "Nobody could tell you that in advance from this end - whoever runs it decides late, for "
    "weather, a clash or a hall, and a holiday shifts the day. Their own page or a call on the "
    "morning is where the yes or no is.",
)
A_FREE_ASK = re.compile(
    r"\b(?:is|are|was|were)\s+(?:it|that|this|the|a|an|my|our|your)?[\s\w'-]{0,24}?\bfree\b"
    r"|\bfree\s+(?:entry|admission|to\s+get\s+in|on\s+(?:mon|tues|wednes|thurs|fri|satur|sun))\b"
    r"|\b(?:do|does)\s+(?:you|i|they|we)\s+(?:have\s+to\s+|need\s+to\s+)?pay\b")
PLACE_FREE_LINES = (
    "Whether it is free is the place's own rule and it moves with the season: some of what is "
    "there is charged even when the rest is not, and the free days change through the year. "
    "Their own site puts the price and any free day under visiting or opening times.",
    "That varies with what is on and with who is going: an event day, a member's rate and a "
    "child's rate each carry their own price, and the place sets them. Their own page lists the "
    "price for the day you are going.",
    "I can't see a place's prices from here, and they are not fixed - what is on and the time of "
    "year both change them. Their own page lists the ticket price, the free days and any "
    "concession, and the desk confirms it on the phone.",
)


def _bounded(phrase):
    return re.compile(r"(?<![a-z0-9])" + re.escape(phrase) + r"(?![a-z0-9])")


def _has(clean, phrases):
    for phrase in phrases:
        if _bounded(phrase).search(clean):
            return True
    return False


def _a_place_they_are_bringing_somebody_to(clean):
    if not A_BRING_ASK.search(clean):
        return False
    if A_DESTINATION.search(clean) and not _has(clean, PLACE_VENUES):
        return False
    return True


PLACE_FACILITIES = frozenset("""
    wifi wi-fi toilets toilet loo loos baby changing lockers locker cafe caf restaurant
    shop food drink cash machine atm cloakroom
""".split())
A_FIXTURE = re.compile(r"\bmatch(?:es)?\b|\bfixtures?\b|\bkick[\s-]?offs?\b|\bthe\s+game\b",
                        re.I)
A_RUNS_TO_A_CALENDAR = re.compile(
    r"\b(?:market|boot sale|car boot|stall|fete|fair|jumble|table top|quiz|class|classes|"
    r"session|sessions|group|club)\b", re.I)


A_STANDING_DAY = re.compile(
    r"\b(?:(?:mon|tues|wednes|thurs|fri|satur|sun)days|weekends|every\s+[a-z]+)\b", re.I)


def the_line(clean):
    if A_HOME_OF_THEIR_OWN.search(clean) and not _has(clean, PLACE_VENUES):
        return None
    if PLACE_IS_THERE.search(clean) and _has(clean, PLACE_FACILITIES):
        return None
    if A_FIXTURE.search(clean) and not A_RUNS_TO_A_CALENDAR.search(clean):
        return None
    of_its_own = bool(PLACE_ASKS_OF_ITS_OWN.search(clean))
    bringing = _a_place_they_are_bringing_somebody_to(clean)
    lets_animals = bool(PLACE_LETS_ANIMALS.search(clean) and _has(clean, PLACE_ANIMALS))
    if not (of_its_own or bringing or lets_animals or PLACE_ASKS.search(clean)):
        return _a_day_ask(clean)
    if not (of_its_own
            or bringing
            or lets_animals
            or _has(clean, PLACE_OF_ITS_OWN)
            or (_has(clean, PLACE_VENUES) and _has(clean, PLACE_WITH_A_VENUE))
            or (BARE_PLACE_SUBJECT.search(clean)
                and _has(clean, PLACE_ASKS_WITH_NO_SUBJECT))
            or (PLACE_IS_THERE.search(clean) and _has(clean, PLACE_ASKS_WITH_NO_SUBJECT)
                and not (A_HOME_OF_THEIR_OWN.search(clean) and not _has(clean, PLACE_VENUES)))
            or (BARE_PLACE_SUBJECT.search(clean)
                and _has(clean, PLACE_ANIMALS) and PLACE_PERMISSION.search(clean))):
        return _a_day_ask(clean)
    return PLACE_LINES


def _a_day_ask(clean):
    if _has(clean, A_CLOCK_ASK):
        return None
    if A_FREE_ASK.search(clean) and (_has(clean, PLACE_VENUES) or _has(clean, PLACE_EVENTS)
                                     or A_DAY.search(clean)):
        if not _has(clean, A_SWITCHED_ON_THING):
            return PLACE_FREE_LINES
    if _has(clean, A_CROWD_ASK):
        return None
    if A_STANDING_DAY.search(clean):
        return None
    if not (ON_A_DAY.search(clean) and A_DAY.search(clean)):
        return None
    if _has(clean, A_SWITCHED_ON_THING):
        return None
    if not (_has(clean, PLACE_VENUES) or _has(clean, PLACE_EVENTS)):
        return None
    return PLACE_ON_A_DAY_LINES
