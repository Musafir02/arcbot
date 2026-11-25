import re

from . import pick

HEDGE_OPENERS = (
    "i'm not sure about that one",
    "that's beyond what i know well",
    "i don't know enough to answer that honestly",
)

_JUDGE = (r"(?:ok|okay|alright|all right|good|nice|safe|doable|suitable|any good|any cop|"
          r"any use|decent|handy|worth it|worth going|worth seeing)")
VERDICT_ASK = re.compile(
    r"^\s*(?:so|but|and|ok|okay)?\s*(?:do you think\s+)?"
    r"(?:"
    r"(?:is|are|was|were)\s+[a-z' ]{2,40}?\s+" + _JUDGE +
    r"|(?:would|will)\s+[a-z' ]{2,40}?\s+(?:suit|work for|be ok for|be alright for|"
    r"be all right for|be good for)\b"
    r"|(?:is|was|would)\s+[a-z' ]{0,40}?\s*worth\s+(?:it|a (?:look|visit|go|trip|day out)|"
    r"going|the (?:trip|money|hype))\b"
    r")"
    r"|\b(?:is|would)\s+it\s+" + _JUDGE + r"\b")
NOT_A_JUDGEMENT = re.compile(
    r"\b(?:eat|eaten|ate|eating|cook|cooked|cooking|cooker|freeze|frozen|defrost|fridge|"
    r"left out|left over|leftover|reheat|next day|day after|still ok|still good|gone off|"
    r"use by|sell by|best before|chicken|meat|fish|rice|milk|eggs|yoghurt|yogurt|"
    r"dose|dosage|mg|ml|tablet|tablets|pill|pills|medicine|paracetamol|ibuprofen|antibiotic|"
    r"pregnan\w*|symptom\w*|rash|fever|temperature|covid|flu|"
    r"old enough|how old|legal|illegal|allowed|the law|licen\w+|rules|"
    r"cost|costs|price|prices|how much|cheaper|afford|salary|wage|wages|tax|refund|deposit|"
    r"visa|passport|insur\w*|contract|tenancy|notice period|"
    r"worth buying|worth fixing|worth repairing|worth selling|repair|fix|broken)\b")

_THING = re.compile(
    r"^\s*(?:so|but|and|ok|okay)?\s*(?:do you think\s+)?(?:is|are|was|were|would|will)\s+"
    r"(?P<thing>[a-z' ]{2,40}?)\s+(?:" + _JUDGE +
    r"|suit|work for|be ok for|be alright for|be all right for|be good for)\b")
_BARE_NOUN = frozenset("""area place street road estate flat house home hotel restaurant cafe
    pub school nursery gym club class course town city village beach park market walk route
    holiday trip""".split())
_NOT_A_THING = frozenset("food menu price cost drink beer wine coffee".split())
_STOP = ("suit", "work", "be", "ok", "okay", "alright", "good", "nice", "safe", "doable",
         "worth", "any", "decent", "handy", "all")

_TRIP_CRITERIA = ("how far the flight or the drive is, how hot it gets, and how much walking "
                  "there is once you are there")
_TRIP_WHERE = ("Reviews from the last few months say what a place is like now rather than five "
               "years ago.")
_CHILD_CRITERIA = ("the flight or the drive, the heat, and how far the beach, the food and the "
                   "shops are from the room")
_CHILD_WHERE = ("The hotel's own page and the last few months of reviews cover the rest, and a "
                "map app shows the walk to the sand.")
_SAFE_CRITERIA = ("the time of day you would be out, how busy the street is then, and whether "
                  "you would be walking it alone")
_SAFE_WHERE = ("The police's own crime map for the postcode says more than any general view of "
               "a place does.")
_SAFE_OBJECT_CRITERIA = ("the moving parts, the fixings and the seals, and anything cracked, "
                         "loose, or smelling of gas or hot plastic")
_SAFE_OBJECT_WHERE = ("Whoever services them will look it over for very little, and a gas or "
                      "electrical job wants a registered engineer rather than a guess.")
_SCHOOL_CRITERIA = ("the walk there, what the mornings feel like, and how easy it is to get a "
                    "straight answer out of the staff")
_SCHOOL_WHERE = ("Their own site has the numbers and the last report, and other parents tell you "
                 "the rest.")
_FOOD_CRITERIA = ("the last few months of reviews, the menu, and whether the price suits the "
                  "evening you have in mind")
_FOOD_WHERE = ("Their own page and the recent reviews have all three, and one visit settles it.")
_STAY_CRITERIA = ("the last few months of reviews, how far it is from where you want to be, and "
                  "what the noise is like at night")
_STAY_WHERE = ("Their own page and recent reviews cover all three, and the map listing shows the "
               "walk into town.")
_CLASS_CRITERIA = ("the times you can actually get to, who takes the session, and whether the "
                   "first one is free")
_CLASS_WHERE = ("Their timetable and a trial session answer that better than any review.")
_WALK_CRITERIA = ("the distance, how much of it is up or down, and the ground underfoot")
_WALK_WHERE = ("A map app shows the distance and the climb in a minute, and street view shows you "
               "the path.")
_HOME_CRITERIA = ("the walk from the station or the bus, the light in the rooms, the noise at the "
                  "time you would be home, and what the neighbours are like")
_HOME_WHERE = ("A map app shows the walk and the streets, and one visit on a weekday evening "
               "tells you the noise.")

TRIP = (
    "{lead}never been, so no verdict from me. What decides a trip there is {criteria}. {where}",
    "{lead}no first-hand knowledge of the place, so no verdict from me. The things that settle it "
    "are {criteria}. {where}",
)
WITH_CHILDREN = (
    "{lead}not been with a little one, so I can't call it. What decides that trip is {criteria}. "
    "{where}",
    "{lead}can't call it from here. With a child in tow it comes down to {criteria}. {where}",
)
SAFE_ = (
    "{lead}can't tell you whether a place is safe from here, and I won't guess at it. What "
    "changes the answer is {criteria}. {where}",
    "{lead}no way for me to know about crime on a street I can't see, so no verdict from me. It "
    "turns on {criteria}. {where}",
)
SAFE_OBJECT = (
    "{lead}I can't look at it from here, so no verdict from me on whether it is safe. What a "
    "check comes down to is {criteria}. {where}",
    "{lead}no way for me to see the state of it, and safety is not something I'll guess at. It "
    "comes down to {criteria}. {where}",
)
SCHOOL = (
    "{lead}can't judge a school from here, and guessing would be worse than saying so. What tells "
    "you most is {criteria}. {where}",
    "{lead}no verdict from me on that one - I can't see inside a school from here. What tells you "
    "most is {criteria}. {where}",
)
FOOD = (
    "{lead}not eaten there, so no verdict from me. What decides it is {criteria}. {where}",
)
STAY = (
    "{lead}not stayed there, so no verdict from me. What decides it is {criteria}. {where}",
)
CLASS = (
    "{lead}can't judge one from here. It comes down to {criteria}. {where}",
)
WALK = (
    "{lead}can't see the ground from here, so I won't guess at how hard it is. What decides it is "
    "{criteria}. {where}",
)
SIGHT = (
    "{lead}no first-hand knowledge of the place, so no verdict from me. The things that settle it "
    "are {criteria}. {where}",
)
FAMILY = (
    "{lead}can't judge a place to bring children up from here. What decides it is {criteria}. "
    "{where}",
)
HOME = (
    "{lead}no way of seeing a place I haven't been to, so no verdict from me. What decides it is "
    "{criteria}. {where}",
)
OTHER = (
    "No first-hand knowledge of that one, so no verdict from me - and guessing would be worse than "
    "saying so. What settles most of these is what you want out of it, what you would do with it "
    "if it turned out to be no good, and what people who wanted the same thing say about it once "
    "they have had it a few months. Reviews from people who wanted the same thing say more than "
    "the page selling it.",
    "No first-hand knowledge of that one here, so no verdict from me. What it comes down to is "
    "how it works for the thing you actually want it for, how it holds up after a few months, "
    "and what it costs you if it is wrong. Recent reviews from people who wanted the same thing "
    "are the shortest way to all three.",
)
_SCREEN_CRITERIA = ("who made it and what you thought of theirs before, how long it takes to get "
                    "going, and whether you want to think or switch off")
_SCREEN_WHERE = ("A trailer or the first chapter tells you more in ten minutes than any review, "
                 "and the recent reviews say whether it holds up after the opening.")
_JOB_CRITERIA = ("the pay, the hours, and what the day actually looks like rather than what the "
                 "job is called")
_JOB_WHERE = ("The pay scales are published, and asking two people who do it now about a normal "
              "week settles more than any article.")
SCREEN = (
    "{lead}no first-hand knowledge of that one, so no verdict from me. What decides it is "
    "{criteria}. {where}",
    "{lead}can't judge it from here. It comes down to {criteria}. {where}",
)
JOB = (
    "{lead}wouldn't want to call that from here. What decides it is {criteria}. {where}",
    "{lead}no first-hand knowledge of that one. The honest answer turns on {criteria}. {where}",
)

_ABOUT_THE_BOT = re.compile(r"\b(?:are|is|was|were)\s+(?:you|u|ya|the bot|this bot|"
                            r"this thing|the chatbot)\b|"
                            r"\b(?:ok|okay|alright|all right|fine|good|bad)\s+(?:with|to|for)\s+"
                            r"(?:you|u|ya)\b")
_PLACE = re.compile(r"\b(?:area|areas|street|streets|road|roads|neighbourhood|neighborhood|estate|"
                    r"town|city|village|centre|center|park|beach|seafront|suburb|postcode|place|"
                    r"location|block|here|there|abroad|hotel|hostel|flat|house|home|station|"
                    r"walkway|alley|underpass|path|route|car park|sea|lake|river|coast|"
                    r"seaside|harbour|harbor)\b")
_SAFE = re.compile(r"\b(?:safe|safety|rough|dodgy|crime|mugged|sketchy|dangers?)\b")
_FEELING = re.compile(r"\b(?:feel|feels|feeling|felt)\b|\blike this\b|\babout myself\b|"
                      r"\bfor me to\b")
_SCREEN = re.compile(r"\b(?:films?|movies?|series|show|shows|book|books|novel|album|game|games|"
                     r"documentar(?:y|ies)|podcasts?|sitcom|box set)\b")
_JOB = re.compile(r"\b(?:jobs?|careers?|trades?|profession|line of work|working as|"
                  r"worth (?:doing|studying|training))\b")
_SAFE_OBJECT = re.compile(r"\b(?:bikes?|cars?|vans?|mopeds?|scooters?|motorcycles?|ladders?|"
                          r"boilers?|heaters?|wood ?burners?|wiring|electrics|roof|chainsaws?|"
                          r"trampolines?|swing sets?|woodburner)\b")
_SCHOOL = re.compile(r"\b(?:school|schools|nursery|nurseries|preschool|pre-school|childminder|"
                     r"creche|cr[e\u00e8]che|kindergarten|college|university|uni)\b")
_STAY = re.compile(r"\b(?:hotel|hotels|b&b|b and b|hostel|guest house|guesthouse|apartment|"
                   r"villa|cottage|campsite)\b")
_FOOD = re.compile(r"\b(?:restaurant|restaurants|caf[e\u00e9]|pub|takeaway|bar|canteen|chippy|"
                   r"kebab shop|menu|food)\b")
_CLASS = re.compile(r"\b(?:gym|gyms|class|classes|club|clubs|course|courses|lessons|"
                    r"swimming pool|pool|leisure centre)\b")
_WITH_CHILDREN = re.compile(r"\b(?:toddlers?|bab(?:y|ies)|kids?|children|child|pram|buggy|"
                            r"pushchair|teenagers?|families)\b")
_WALK = re.compile(r"\b(?:walk|walks|route|hike|climb|stairs|hill)\b")
_RAISING = re.compile(r"\b(?:bring (?:up|ing up)|raise|raising|grow(?:ing)? up|settle down|"
                      r"to live|live in|family life)\b")
_SIGHT = re.compile(r"\b(?:old town|town cent(?:re|er)|city cent(?:re|er)|market|attractions?|"
                    r"museum|gallery|castle|cathedral|zoo|theme park|water park)\b")
_TRIP = re.compile(r"\b(?:holiday|holidays|trip|resort|resorts|beach|town|city|village|island|"
                   r"abroad|seaside|centre|center|market|attraction|museum|zoo|park|cruise|cruises|"
                   r"ferry|flight|flights|long haul|day out|days out|weekend away)\b")
_NAMED = re.compile(r"\S\s+(?:the\s+|a\s+|an\s+)?[A-Z][a-z]{2,}")
_TRAVEL_TOPICS = frozenset(("geography-and-travel", "travel", "holidays", "places"))
_NOT_A_PLACE_TOPICS = frozenset((
    "sport", "fitness", "health", "body", "eating", "food-and-drink", "money", "work",
    "technology", "pets", "law", "driving", "school-and-study", "hobbies", "home-and-garden",
    "beauty", "clothes"))
_SIGHT_CRITERIA = ("how much walking there is, whether it goes up or down, and how busy it gets "
                   "at the time you would go")
_SIGHT_WHERE = ("The place's own page has the access and the opening times, and a map app shows "
                "the walk and the climb")
_FAMILY_CRITERIA = ("the schools and how you get into them, how much green space is within "
                    "walking distance, and what there is for children to do")
_FAMILY_WHERE = ("The council's own site lists the schools and the areas they take, and an "
                 "afternoon walk round on a school day tells you the rest")
_HOME = re.compile(r"\b(?:flat|house|home|area|neighbourhood|neighborhood|street|road|estate|"
                   r"place|location|block)\b")


def _the_thing(said):
    found = _THING.search(said)
    if not found:
        return ""
    words = found.group("thing").split()
    while words and words[-1] in _STOP:
        words.pop()
    while words and words[0] in ("it", "this", "that", "there", "they", "these", "those"):
        words.pop(0)
    owning = False
    while words and words[0] in ("my", "our"):
        words.pop(0)
        owning = True
    if owning and words:
        return ("that " + " ".join(words))[:1].upper() + ("that " + " ".join(words))[1:]
    while len(words) > 1 and words[-1] in ("a", "an", "the", "one", "career", "idea", "option",
                                           "choice"):
        words.pop()
    if len(words) == 1 and words[0] in ("a", "an", "the", "one"):
        return ""
    if not words or words[-1] in _NOT_A_THING:
        return ""
    thing = " ".join(words)
    if len(words) == 1 and words[0] in _BARE_NOUN:
        thing = "that " + words[0]
    return thing[:1].upper() + thing[1:]


def _pool(said, named=False, other_subject=False, travel=False):
    if _SAFE.search(said) and _SAFE_OBJECT.search(said) and not _HOME.search(said):
        return SAFE_OBJECT, _SAFE_OBJECT_CRITERIA, _SAFE_OBJECT_WHERE
    if _SCHOOL.search(said):
        return SCHOOL, _SCHOOL_CRITERIA, _SCHOOL_WHERE
    if _STAY.search(said):
        return STAY, _STAY_CRITERIA, _STAY_WHERE
    if _FOOD.search(said):
        return FOOD, _FOOD_CRITERIA, _FOOD_WHERE
    if _CLASS.search(said):
        return CLASS, _CLASS_CRITERIA, _CLASS_WHERE
    if _SIGHT.search(said):
        return SIGHT, _SIGHT_CRITERIA, _SIGHT_WHERE
    if _RAISING.search(said) and _WITH_CHILDREN.search(said):
        return FAMILY, _FAMILY_CRITERIA, _FAMILY_WHERE
    somewhere = bool(_PLACE.search(said) or _TRIP.search(said) or named or travel)
    if (_WITH_CHILDREN.search(said) and (somewhere or not _SAFE.search(said))
            and not (other_subject and not somewhere)
            and not (_SAFE.search(said) and _the_thing(said) and not somewhere)
            and not (_HOME.search(said) and not _TRIP.search(said))):
        return WITH_CHILDREN, _CHILD_CRITERIA, _CHILD_WHERE
    if _SAFE.search(said) and not _PLACE.search(said):
        return None, None, None
    if _SAFE.search(said):
        return SAFE_, _SAFE_CRITERIA, _SAFE_WHERE
    if _WALK.search(said):
        return WALK, _WALK_CRITERIA, _WALK_WHERE
    if _TRIP.search(said):
        return TRIP, _TRIP_CRITERIA, _TRIP_WHERE
    if _HOME.search(said):
        return HOME, _HOME_CRITERIA, _HOME_WHERE
    if _SCREEN.search(said):
        return SCREEN, _SCREEN_CRITERIA, _SCREEN_WHERE
    if _JOB.search(said):
        return JOB, _JOB_CRITERIA, _JOB_WHERE
    return OTHER, "", ""


_PAST_ASK = re.compile(r"^(?:and\s+)?(?:was|were|did|how was|how were|how did)\b")


def reads_as_a_verdict_ask(text):
    said = re.sub(r"\s+", " ", str(text or "").lower().replace("\u2019", "'")).strip()
    if not said or not VERDICT_ASK.search(said):
        return False
    if _ABOUT_THE_BOT.search(said):
        return False
    if _FEELING.search(said):
        return False
    if _PAST_ASK.search(said) and _the_thing(said).lower() in ("", "it", "that", "this", "they"):
        return False
    return not NOT_A_JUDGEMENT.search(said)


def reads_as_a_hedge(reply):
    said = str(reply or "").strip().lower().replace("\u2019", "'")
    return any(said.startswith(opener) for opener in HEDGE_OPENERS)


def _the_topics(memory):
    if not isinstance(memory, dict):
        return set()
    understood = memory.get("understood") or {}
    if not isinstance(understood, dict):
        return set()
    topics = set(understood.get("topics") or ())
    if understood.get("topic"):
        topics.add(understood["topic"])
    return topics


def pool_for(text, memory=None):
    raw = re.sub(r"\s+", " ", str(text or "").replace("\u2019", "'")).strip()
    said = raw.lower()
    if not reads_as_a_verdict_ask(said):
        return None
    topics = _the_topics(memory)
    pool, criteria, where = _pool(said, named=bool(_NAMED.search(raw)),
                                 other_subject=bool(topics & _NOT_A_PLACE_TOPICS),
                                 travel=bool(topics & _TRAVEL_TOPICS))
    if pool is None:
        return None
    if pool is OTHER and not _the_thing(said):
        return None
    if pool is OTHER:
        return pool
    thing = _the_thing(said)
    lead = thing + " \u2014 " if thing else ""
    said_lines = []
    for line in pool:
        line = line.format(lead=lead, criteria=criteria, where=where)
        said_lines.append(line if lead else line[:1].upper() + line[1:])
    return tuple(said_lines)


def answer_for(text, memory=None, reply=""):
    if not reads_as_a_hedge(reply):
        return None
    pool = pool_for(text, memory)
    if not pool:
        return None
    return pick(pool, memory if isinstance(memory, dict) else {}, text)
