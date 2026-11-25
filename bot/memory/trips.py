import re

from . import ack, facts, last_bot, not_a_trip, plan_line, user
from .facts import DAYS, KIN, MONTHS, NOT_PLACES, PLACE_VERBS

GOING = re.compile(
    r"\b(?:we're|we\s+are|were|we've|weve|we\s+have|we|i'm|i\s+am|im|i've|ive|i\s+have|i|"
    r"they're|theyre|they\s+are|they've|theyve|they|he's|shes|she's|hes)\b\s*"
    r"(?:(?:thinking\s+of|planning|hoping\s+to|looking\s+at|off|away)\s+)?"
    r"(?:going|off|heading|flying|driving|sailing|travelling|traveling|"
    r"booked|booking)\b", re.I)
GOING_BARE = re.compile(
    r"^\s*(?:and\s+|so\s+|oh\s+|right\s+|ok(?:ay)?[ ,]+)*"
    r"(?:thinking\s+of\s+|planning\s+|hoping\s+to\s+|looking\s+at\s+)?"
    r"(?:going|off|heading|flying|driving|sailing|travelling|traveling|"
    r"booked|book|booking)\b", re.I)
TO_PLACE = re.compile(r"\b(?:to|into)\s+((?:the\s+)?[a-z][a-z'\u2019-]*(?:\s+[a-z][a-z'\u2019-]*){0,3})",
                      re.I)
IN_PLACE = re.compile(r"\bin\s+((?:the\s+)?[a-z][a-z'\u2019-]*(?:\s+[a-z][a-z'\u2019-]*){0,3})",
                      re.I)
BOOKED_PLACE = re.compile(r"\b(?:booked|book|booking)\s+(?:us\s+)?"
                          r"((?:the\s+)?[a-z][a-z'\u2019-]*(?:\s+[a-z][a-z'\u2019-]*){0,3}?)\s+"
                          r"(?:for|from)\b", re.I)
NOT_A_TRIP = re.compile(r"^\s*(?:a|an|the|my|our|his|her)\s+(?:wedding|party|concert|gig|"
                        r"festival|funeral|match|game|show|play|hen|stag|birthday|christening|"
                        r"meeting|conference|interview|appointment|course|class|exam|test)\b", re.I)
NOT_AN_AMOUNT = frozenset("""half halves quarter quarters third thirds two three four five six ten
twenty hundred dozen bits pieces lumps chunks squares slices rounds""".split())
NOT_A_PLACE = frozenset("""be get got go going do see try have check sort pick take make book
lose losing lost sell selling sold lose win won keep quit leave leaving start stop manage afford
ask tell call look find put buy eat drink work bed sleep town home hospital doctor dentist
prison jobcentre funeral crematorium coroner interview solicitor tribunal
drive fly stay visit meet leave arrive catch ride walk swim camp pitch collect drop fetch
play watch celebrate shop rest
# A body failing is not a place: "i'm going to pass out", "going to faint", "im going to be sick"
# are read as a trip to Pass Out and said back as "{place}, lovely. When is it?". The verbs are
# here with the other things nobody travels to.
pass faint collapse vomit throw sick black die choke bleed fit seizure
# Going round the same ground is not a journey: "im going round in circles at work" was read as
# a trip to a place called Circles and answered "Circles - nice. When are you going?", which is the
# last thing a person who has just said they are stuck wants to hear. The words a loop is said with
# are nobody's destination.
circles circle loops loop
# "book recommendations for my dad" is a person asking for a book to read, not a trip with their
# father in it: "book" is the noun here, so the word behind it was read as the place and the reply
# was "Recommendations is booked, then. Get the big days out booked now too". A word that asks for
# a pick is never somewhere to go.
recommend recommends recommended recommendation recommendations suggest suggests suggested
suggestion suggestions ideas idea picks tips
# A person going to harm themselves is not a trip to a place called Kill Themselves: with no
# person named in the chat, "they are going to kill themselves" was answered "Kill Themselves,
# lovely. When is it?".
kill kills killing killed suicide overdosing overdose hang hanging harm hurt hurting starve
myself yourself himself herself ourselves themselves
school work church gym shop shops tesco asda aldi lidl mum mums dad dads nan gran grandparents
kids children baby partner wife husband friend friends sister brother them him her you me us
it that this there somewhere anywhere out in on up down back again now later today tomorrow
tonight yesterday first last next""".split()) | NOT_AN_AMOUNT
A_PERSON_IS_NOT_A_PLACE = re.compile(
    r"^(?:my|our|his|her|their)\s+(?P<person>(?:"
    + "|".join(sorted(KIN + ("kids", "children", "grandparents", "grandchildren", "family",
                             "relatives", "folks", "twins", "mate", "in laws", "in-laws",
                             "inlaws", "in law", "in-law", "inlaw"), key=len, reverse=True))
    + r"))(?P<plural>s)?(?P<poss>['\u2019]s?)?(?!\w)", re.I)
_NOT_A_THING_OF_THEIRS = frozenset((
    "in", "on", "at", "for", "with", "from", "to", "by", "during", "after", "before",
    "and", "or", "but", "next", "this", "last", "tomorrow", "today", "tonight", "soon",
    "later", "again", "now", "then", "there", "here", "every", "each", "all", "week",
    "weekend", "month", "year"))
A_HAPPY_COURT = r"\b(?:adopt\w*|adoption)\b"
EVERYDAY_TRIP = re.compile(
    r"\b(?:to the (?:gym|shops?|pub|supermarket|doctors?|dentist|hospital|school|office|bank)|"
    r"off to work|going to work|to bed|to sleep|to the loo|to the tip|"
    rf"(?!.*{A_HAPPY_COURT})to (?:the )?court|to (?:the )?prison|to (?:the )?job ?centre|"
    r"to (?:a |the )?funeral|"
    r"to (?:the )?crematorium|to (?:the )?coroner'?s?|to (?:a |the )?tribunal|"
    r"to (?:an |the )?interview)\b", re.I)
ON_A = re.compile(r"\b(?:on|for)\s+(?:a\s+|the\s+|our\s+)?(holiday|holidays|trip|break|"
                  r"cruise|weekend away)\b", re.I)

WITH_WHO = re.compile(r"\bwith\s+((?:the|my|our|his|her|both|all|a|an|two|three|four|\d+)\s+"
                      r"[a-z0-9](?:(?!\b(?:for|on|at|next|this|during|over|until)\b"
                      r"|\bin\s+(?!law\b))[a-z0-9' -])*)", re.I)
NUMBER_WORD = (r"(?:\d+|a\s+few|a\s+couple\s+of|few|several|a|an|one|two|three|four|five|six|"
               r"seven|eight|nine|ten|eleven|twelve|fifteen|twenty|thirty)")
FOR_HOW_LONG = re.compile(r"\bfor\s+(" + NUMBER_WORD + r"\s+"
                          r"(?:day|days|night|nights|week|weeks|fortnight|month|months)?s?"
                          r"|the weekend)\b", re.I)
JUST_HOW_LONG = re.compile(r"^(?:(?:just|only|about|maybe|probably)\s+)?"
                           r"(" + NUMBER_WORD + r"\s+"
                           r"(?:day|days|night|nights|week|weeks|fortnight|month|months))$"
                           r"|^(?:(?:just|only|maybe)\s+)((?:a|the)\s+weekend)$", re.I)
TIME_WORD = frozenset("""morning afternoon evening night today tomorrow yesterday
minute minutes moment moments hour hours second seconds bit while sec secs min mins""".split())
DURATION = re.compile(r"^(?:" + NUMBER_WORD + r"\s+)?(?:second|minute|moment|hour|bit|while|"
                      r"day|week|month|fortnight)s?$", re.I)
PACKING = re.compile(r"^(?:and\s+|also\s+|oh\s+)?(?:what|anything)\s+(?:should|shall|do|would|"
                     r"will|to)?\s*(?:we|i|you)?\s*(?:pack|bring|take)\b(.*)$", re.I)
PACKING_SAID = re.compile(
    r"^(?:and\s+|also\s+|oh\s+)?(?:should|shall|do|does|would|will|can|could)\s+"
    r"(?:we|i|you)\s+(?:need\s+to\s+)?(?:pack|bring|take|need)\b(.*)$", re.I)
ONE_THING_NEEDED = re.compile(
    r"^(?:and\s+|also\s+|oh\s+)?(?:should|shall|do|does|would|will|can|could)\s+(?:we|i|you)\s+"
    r"need\s+(?!to\b)(?:a\s+|an\s+|my\s+|our\s+|some\s+|any\s+)?(?P<thing>[a-z]+)", re.I)
NO_THING_NAMED = frozenset("""anything something nothing much else more anymore any
another""".split())


def _one_thing_they_need(low):
    found = ONE_THING_NEEDED.match(low)
    if not found:
        return ""
    thing = found.group("thing").lower()
    if thing in NO_THING_NAMED:
        return ""
    return thing


OUT_OF_SEASON = frozenset(("october",))
AN_EVENT_NOT_A_PLACE = frozenset("""picnic barbecue bbq party wedding funeral christening festival
concert gig show play match game race hen stag birthday dinner lunch barbecue""".split())
PACKING_FOR = re.compile(r"^(?:for\s+(?:the\s+)?(?:kids?|children|us|me|him|her|them|wife|husband|"
                         r"partner|trip|holiday|week|weekend|walk|beach|evenings?)|"
                         r"for\s+(?:a|one|two|three|four|five|six|ten|\d+)\s+"
                         r"(?:day|days|night|nights|week|weeks|fortnight|months?)|"
                         r"this time of year)$", re.I)
PACKING_NOTES = (
    "for {place} in {month}: layers for the evenings, one warm thing whatever the forecast says, "
    "and shoes you can walk in.",
    "pack light for {place} in {month} - a waterproof, something warm for the evening, and half "
    "the clothes you think you need.",
)
PACKING_NO_MONTH = (
    "for {place}: layers, one warm thing for the evening, and shoes you can walk in.",
)
PACKING_NO_PLACE = (
    "for {kind} in {month}: layers, one warm thing for the evening, a waterproof and shoes you "
    "can walk in - and half the clothes you think you need.",
    "{kind} in {month} fits in one bag: a change of clothes for each day, something warm for the "
    "evening, a waterproof and shoes you can walk in.",
)
PACKING_NO_PLACE_NO_MONTH = (
    "for {kind}: layers, one warm thing for the evening, a waterproof and shoes you can walk in.",
)
PACKING_WITH_KIDS = ("with the kids, one change of clothes each per day and a bag for the wet "
                     "things covers it.")
VISIT_PACKING = (
    "for {place}, nothing much: something for the table - a bottle, a pudding or flowers - and a "
    "bag for the night if you are staying over.",
    "{place} is the easy kind of visit to pack for: a bottle or a pudding for the table, and "
    "check whether they want you for the whole day or just the evening.",
    "for {place}: what you would bring to a table, and a bag only if you are staying the night.",
)
VISIT_PACKING_FOR_A_MEAL = (
    "take a bottle and something for after - a pudding, cheese and biscuits, or a box of chocolates "
    "- so you are not competing for their oven. Ask what they are cooking, then bring the thing "
    "that goes with it.",
    "a bottle for the table and something for after, and ask what they are cooking so what you "
    "bring goes with it rather than fighting for the oven.",
)
VISIT_PACKING_FOR_A_BABY = (
    "nothing for the baby - they have more than they can use. Take food: a meal for the freezer "
    "or something for lunch, and keep the visit to an hour unless they ask you to stay.",
    "what a house with a new baby wants is a cooked meal and short visits, so take dinner in a "
    "dish you do not want back, and ask before you hold the baby.",
)
A_STAY_LENGTH = re.compile(r"\bhow (?:long|many (?:nights|days)) (?:should|shall|do|would|will) "
                          r"(?:we|i) (?:stay|stop|be there|go for)\b", re.I)
VISIT_HOW_LONG = (
    "two nights is the sweet spot for family - long enough to settle in, short enough that you "
    "are missed.",
    "one night the first time, two if it is a long drive. Leave while everyone is still enjoying "
    "it rather than when the conversation has run out.",
    "a weekend is plenty unless there is something on: arrive Saturday, go home Monday, and say "
    "when you are leaving before you get there.",
)
VISIT_A_WEEK = (
    "a week with family is a long visit: agree the leaving day before you go, and keep an "
    "afternoon or two that are just yours.",
    "a week is plenty to be in somebody else's house - say when you are leaving, and plan one day "
    "of it that is just yours.",
)
VISIT_A_FEW_DAYS = (
    "a night or two is the easy length for a visit: enough to catch up, short enough that nobody "
    "is hosting for too long.",
    "one or two nights is right for family: bring something for the table, and leave while you "
    "are both still enjoying it.",
)
VISIT_A_WEEKEND = (
    "a weekend is the classic visit - one evening together, one day out, and home before the week "
    "starts.",
    "the weekend is enough for most visits: Friday night to Sunday afternoon, and say on the "
    "Friday when you are heading back.",
)
A_MEAL = re.compile(r"\b(?:dinner|lunch|tea|supper|brunch|barbecue|bbq|roast)\b", re.I)
A_NEW_BABY = re.compile(r"\b(?:new\s?born|new baby|just had a (?:baby|girl|boy)|had a baby|"
                        r"baby (?:is|was) (?:born|due)|\dbaby)\b|\bnewborn\b", re.I)
THE_FLIGHT = re.compile(r"\bhow (?:long|far) (?:is|does) the flight\b")
HOW_LONG_ASK = re.compile(r"\bhow (?:long|far)\b", re.I)
THE_MODE = re.compile(r"\bhow (?:do|are) we get(?:ting)? there\b")
THE_DRIVE = re.compile(r"\bhow (?:long|far) (?:is|does) the (?:drive|journey|trip)\b"
                       r"|\bhow (?:long|far) (?:will|would) the (?:drive|journey|trip) "
                       r"(?:take|be)(?:\b|$)"
                       r"|\bhow do we get there\b|\bhow are we getting there\b", re.I)
THE_JOURNEY_ASK = re.compile(
    r"\bhow\s+(?:long|far)\s+(?:will|would|does|do|did|is|are|might)\s+(?:it|that|this|the\s+"
    r"(?:drive|journey|trip|flight|train))?\s*(?:take|be|takes)?\s*(?:to\s+)?"
    r"(?P<mode>drive|get\s+there|get\s+to|travel|walk|sail|go)\b"
    r"|\bhow\s+(?:long|far)\s+(?:it|is\s+it)\b[^?]{0,20}\b(?P<mode2>driving|drive|flight|train)\b"
    r"|\bhow\s+long\s+to\s+(?P<mode3>get\s+there|drive|fly|travel)\b", re.I)
THE_LENGTH_ASK = re.compile(
    r"\bhow\s+long\s+(?:are|is|were|was)\s+(?:we|you|i|it)\s+(?:there|away|staying|going"
    r"|going\s+for|staying\s+for|away\s+for)\b"
    r"|\bhow\s+long\s+(?:are|is|were)\s+(?:the|our|my|your)\s+(?:trip|holiday|break|stay)\b"
    r"|\bhow\s+many\s+(?:nights|days)\s+(?:are\s+we|is\s+it|will\s+we|do\s+we|have\s+we"
    r"|should\s+we|would\s+we)\b"
    r"|\bhow\s+many\s+(?:nights|days)\s*[?.]?\s*$"
    r"|\bhow\s+long\s+for\s*[?.]?\s*$", re.I)
THE_LENGTH_NOT_SAID = (
    "You haven't said how long - how many nights are you thinking?",
    "Nothing said about how long yet - how many nights are you thinking?",
    "How many nights are you thinking? The plan hasn't got the length on it yet.",
)
THE_LENGTH_NOT_SAID_NAMED = (
    "You haven't said how long - how many nights are you thinking for {named}?",
    "How many nights are you thinking for {named}? Nothing said about that yet.",
)
THE_NIGHTS_FIRST = (
    "The nights decide what you can book, so it's worth settling that first.",
    "Once the nights are fixed the place to stay and the packing both follow.",
    "Get the nights settled and the rest of it falls into place.",
)

JOURNEY_MODE = re.compile(r"\bdriv\w*|\bby\s+car\b|\bin\s+the\s+car\b", re.I)
BY = re.compile(r"\b(?:we're|we are|were|i'm|im|i am)\s+(driving|flying|getting the train|"
                r"on the train|taking the ferry|sailing)\b", re.I)

PEAK = ("july", "august")
BUSY = ("april", "may", "june", "september", "october")
QUIET = ("november", "december", "january", "february", "march")

PEAK_NOTES = (
    "{month} is the busiest, priciest few weeks of the year, so book the place to stay now.",
    "{month} takes the school holidays, so the prices only go one way - book soon.",
    "that is the height of the season: book the place to stay now, and expect slow roads on the "
    "way down.",
)
PEAK_BOOKED_NOTES = (
    "at the height of the season the popular places fill up, so book the big days out now too.",
    "that is the busiest few weeks of the year, so get the days out booked now as well.",
)
BUSY_NOTES = (
    "it misses the worst of it: cheaper and calmer than August, and the weather is usually "
    "decent.",
    "you have timed it well - {month} is quieter and cheaper than the school holidays.",
)
QUIET_NOTES = (
    "that is out of season, so it will be quiet and cheap, and dark by half four.",
    "out of season: quiet, cheap, and short days.",
)
SEASON_NOTES = (
    "that is the season for it, so book soon - the weeks people want go first.",
    "{month} is the good time there: warm days, cool evenings, and the prices know it.",
    "{month} is when it is at its best, so the flights and the rooms are the first thing to sort.",
)
WINTER_SUN = (
    "canaries", "lanzarote", "tenerife", "gran canaria", "fuerteventura", "la palma",
    "cape verde", "madeira", "egypt", "red sea", "dubai", "abu dhabi", "marrakesh",
    "morocco", "cape town", "gambia", "thailand", "maldives", "sri lanka", "goa",
    "barbados", "jamaica", "caribbean", "cancun", "mexico", "florida", "orlando",
)
KIDS_NOTES = (
    "with kids in tow, plan one thing a day and keep a wet-day backup up your sleeve.",
    "with the kids, the beach early and something under cover for the afternoon works best.",
    "kids on a trip like that want one big thing a day and somewhere to dry out afterwards.",
)
KIDS_NUMBERED = (
    "{who}: one big thing a day is plenty, and line up something indoors for the wet afternoon.",
    "with {who}, plan one thing a day and keep a wet-day backup up your sleeve.",
)
KIDS_ONE = "with kids in tow, plan one thing a day and keep a wet-day backup up your sleeve."
WEEK_NOTES = (
    "a week gives you time for the beach days and a couple of trips out without rushing.",
    "a week is about right: long enough to settle, short enough to want to go back.",
)
WEEK_NOTES_LAND = (
    "a week gives you room for two or three places rather than one, without a day lost to "
    "moving each time.",
    "a week is about right there: enough for the big one and a quiet day either side.",
)
SEASON = frozenset("""spring springtime summer summertime autumn autumntime winter wintertime""".split())
SEA_PLACES = frozenset("""cornwall devon dorset sussex kent norfolk suffolk wales pembrokeshire
anglesey skye iona jersey guernsey crete cyprus malta sicily sardinia mallorca majorca ibiza
tenerife lanzarote fuerteventura gran canaria madeira algarve portugal spain greece turkey
croatia italy france""".split())
DAY_NOTES = (
    "that many days is room for a couple of big things and a slow morning in between.",
    "with that many days, pick the two things that matter and let the rest happen.",
)
WEEKEND_NOTES = (
    "a weekend away gives you two nights, so pick one thing to do properly rather than three.",
    "for a weekend, one big thing a day and a slow breakfast is the whole trick.",
)
LONG_NOTES = (
    "a trip that long means you can stop rushing: a couple of lazy days and one proper day out "
    "each.",
    "with that many days you can plan the big day out for the middle, when everyone has settled.",
)

ASK_WHEN = (
    "{place} - nice. When are you going?",
    "{place}, lovely. When is it?",
)
ASK_WHEN_NO_QUESTION = (
    "{place}, nice - tell me when and I can help you work out what to do with it.",
    "{place}, lovely. Say when it is and I will help you plan the days.",
)
OUTING = re.compile(r"^the (beach|coast|seaside|park|woods|forest|hills|countryside|lido|"
                    r"zoo|museum|aquarium)$",
                    re.I)
SEA_NOTES = (
    "take more food and water than you think, and check the tide before you set off.",
    "a change of clothes and a towel in the boot covers most of what goes wrong by the sea.",
    "go early for the parking, and take a bag for the wet things on the way back.",
)
LAND_NOTES = (
    "take more food and water than you think, and go early if you are driving there.",
    "sturdy shoes and a bag for the wet things covers most of what goes wrong.",
    "check the opening times before you set off, and take a coat even on a warm morning.",
)
INDOOR_NOTES = (
    "check the opening times and book the timed slot if they have one - it saves the queue.",
    "buy the tickets online the night before, and go at opening rather than the middle of the day.",
)
SEA = ("beach", "coast", "seaside", "lido")
TICKETED = ("zoo", "museum", "aquarium")
OPEN_AIR = ("park", "woods", "forest", "hills", "countryside")
ASK_WHAT = (
    "what do you want to sort out first, where to stay or what to do while you are there?",
    "what are you hoping to do while you are there?",
    "have you sorted where you are staying, or is that still open?",
)
ASK_VISIT = (
    "what are you doing while you're there?",
    "what's the plan for the visit?",
    "is it a flying visit or are you staying a while?",
)

JUST_A_DETAIL = re.compile(
    r"^\s*(?:and\s+|oh\s+|also\s+|plus\s+)?(?:with\b|"
    r"for\s+(?:a|one|two|three|four|\d|the\s+(?:week|weekend|month|fortnight))\b|"
    r"(?:a|one|two|three|four|five|six|seven|eight|nine|ten|\d+)\s+"
    r"(?:day|days|night|nights|week|weeks|fortnight|months?)\b|"
    r"(?:we're|were|we are|i'm|im|i am)\s+(?:driving|flying|getting the train|getting a\s+"
    r"(?:train|flight|ferry)|taking the (?:train|ferry|plane)|sailing|going by\s+"
    r"(?:car|train|ferry|plane)|on the (?:train|ferry))\b|"
    r"by\s+(?:car|train|ferry|plane)\b|"
    r"(?:a|one|two|three|four|five|six|seven|eight|nine|ten|\d+)\s+"
    r"(?:kids?|children|adults)\b|"
    r"what\s+(?:should|shall|do|would)\s+(?:we|i|you)\s+(?:pack|bring|take)\b|"
    r"what\s+to\s+(?:pack|bring|take)\b|"
    r"how\s+(?:long|far)\s+(?:is|does|will|would)\s+the\s+(?:drive|journey|trip|flight)\b|"
    r"how\s+(?:do|are)\s+we\s+get(?:ting)?\s+there\b)", re.I)


WARM = ("lovely", "nice", "good one")

WORD = re.compile(r"[a-z0-9'\u2019]+")


def _start(said):
    said = str(said or "")
    return said[:1].upper() + said[1:] if said else said


def _low(text):
    return " ".join(str(text or "").lower().split())


BOOKED = re.compile(r"\bbook\w*\b", re.I)
BOOKED_DONE = re.compile(r"\bbooked\b", re.I)
BOOKED_IN_PLACE = re.compile(
    r"\bbook\w*\b[^.!?]{0,40}?\bin\s+((?:the\s+)?[a-z][a-z'\u2019-]*(?:\s+[a-z][a-z'\u2019-]*){0,3})",
    re.I)
WHEN_WORD = "|".join(sorted(MONTHS | DAYS | SEASON, key=len, reverse=True))
BOOKED_IN_WHEN = re.compile(
    r"\b(?:booked|book|booking)\s+(?:us\s+)?"
    r"((?:the\s+)?[a-z][a-z'\u2019-]*(?:\s+[a-z][a-z'\u2019-]*){0,3}?)\s+in\s+"
    r"(?:" + WHEN_WORD + r"|next|this|a\s+(?:few|couple)|\d)", re.I)


PLURAL_RELATIONS = frozenset("""grandparents parents kids children siblings relatives inlaws
    grandchildren""".split())

A_POSSESSION_NOT_A_PLACE = re.compile(
    r"^(?:my|our|his|her|their|the)\s+([a-z]+(?:\s+in\s+law)?)(?:'s|\u2019s|s)?$")


def _a_relation_not_a_place(place):
    found = A_POSSESSION_NOT_A_PLACE.match(place.strip())
    if not found:
        return False
    word = found.group(1).lower()
    return (word in facts.RELATIONS or word.rstrip("s") in facts.RELATIONS
            or word in PLURAL_RELATIONS)


A_CARING_PLACE_HEAD = re.compile(
    r"^(?:the\s+|a\s+|an\s+)?(?:hospital|hospice|care home|nursing home|residential home|"
    r"clinic|infirmary|surgery|ward|a&e|ae|icu|intensive care|high dependency|coronary care)\b",
    re.I)


def _a_person_visited(line):
    if not_a_trip.IN_A_CARING_PLACE.search(str(line or "")):
        return ""
    who = not_a_trip.the_visit(line)
    if who:
        return who
    phrase = _places(line, a_visit=True)
    return phrase if phrase and _a_relation_not_a_place(phrase) else ""


def _places(line, a_visit=False):
    booked = BOOKED.search(line)
    if booked and _the_thing_booked(_low(str(line)[booked.end():])):
        return ""
    for pattern in (TO_PLACE, BOOKED_IN_PLACE, BOOKED_IN_WHEN, BOOKED_PLACE, IN_PLACE):
        found = pattern.search(line)
        if not found:
            continue
        words = [w for w in found.group(1).split() if w]
        kept = []
        for word in words:
            bare = word.lower().strip(",.;:!?")
            if not kept and bare in ("the", "a", "an"):
                kept.append(word)
                continue
            if not kept and (bare in NOT_A_PLACE or bare in MONTHS or bare in DAYS
                             or bare in SEASON or bare in STOP_AFTER):
                break
            if kept and (bare in MONTHS or bare in DAYS or bare in SEASON or bare in STOP_AFTER
                         or bare in ("with", "and", "for", "next", "this")):
                break
            kept.append(word)
        place = " ".join(kept).strip(" ,.;:!?")
        low = place.lower()
        head = [word for word in low.split() if word not in ("the", "a", "an")]
        if head and (head[0] in TIME_WORD or DURATION.match(low)):
            continue
        if NOT_A_TRIP.match(low):
            continue
        if not_a_trip.not_a_destination(words, place):
            continue
        if not place or low in NOT_A_PLACE or low in MONTHS or low in DAYS or SEASON & set(low.split()):
            continue
        if A_CARING_PLACE_HEAD.match(low):
            continue
        bare_place = re.sub(r"^(?:the|a|an)\s+", "", low)
        if bare_place in NOT_A_PLACE or bare_place in MONTHS or bare_place in DAYS:
            continue
        if not a_visit and _a_relation_not_a_place(low):
            continue
            continue
        if low in ("the", "a", "an") or len(low) < 3:
            continue
        if re.search(r"\bbook", line, re.I) and (_the_thing_booked(low)
                                                     or _a_thing_booked_for_when(low)):
            continue
        return place
    return ""


BOOKED_THING = frozenset("""table tables ticket tickets seat seats row taxi cab minicab
haircut appointment appointments slot court pitch room rooms booth class classes lesson
lessons dinner lunch breakfast delivery takeaway table tennis
physio physiotherapist dentist dental doctor doctors gp optician hygienist chiropractor
osteopath vet vets clinic scan xray x-ray bloods surgery consultation checkup
mot service servicing boiler plumber electrician garage engineer gas""".split())


def _the_thing_booked(low):
    words = [w for w in low.split() if w not in ("a", "an", "the", "my", "our", "his", "her")]
    return bool(words) and words[0] in BOOKED_THING


STAY_THING = frozenset("""caravan cottage villa apartment flat hotel lodge cabin tent campervan
camper motorhome house boat ferry crossing tunnel shuttle flight flights cruise
apartment""".split())


def _a_thing_booked_for_when(low):
    words = [w for w in low.split() if w not in ("a", "an", "the", "my", "our", "his", "her")]
    return bool(words) and words[0] in STAY_THING


STOP_AFTER = frozenset("""on in at for from with and next this that the a an to by until
till near around over through tomorrow tonight today later soon
again anyway then first""".split())


def _month(line):
    for word in WORD.findall(_low(line)):
        if word in MONTHS:
            return word
    return ""


A_WHEN_PHRASE = re.compile(
    r"\b(?:next|this|at|over|for|in the|after)\s+(?:month|week|weekend|summer|winter|spring|"
    r"autumn|christmas|xmas|easter|half term|new year|bank holiday)\b"
    r"|\b(?:tomorrow|tonight|the day after tomorrow|this afternoon|this morning)\b", re.I)


BARE_DAY = re.compile(r"\b(" + "|".join(sorted(DAYS - {"weekend"}, key=len, reverse=True)) + r")\b",
                      re.I)


def _when_phrase(line):
    said = str(line or "")
    found = A_WHEN_PHRASE.search(said)
    if found:
        return " ".join(found.group(0).lower().split())
    day = BARE_DAY.search(said)
    return day.group(1).lower() if day else ""


_GROUP = (r"(?:kids?|children|child|adults?|grown-?ups?|teenagers?|bab(?:y|ies)|toddlers?|"
          r"boys?|girls?|year\s+olds?|pensioners?|grandparents?|parents?)")
_COUNT = r"(?:a|an|one|two|three|four|five|six|seven|eight|nine|ten|\d+)"
BARE_WHO = re.compile(r"^\s*(?:and\s+|oh\s+|also\s+|plus\s+)?"
                      r"((?:" + _COUNT + r"\s+" + _GROUP + r"|\d+\s+year\s+olds?)"
                      r"(?:\s+(?:and|plus)\s+(?:an?\s+|our\s+|my\s+|their\s+|the\s+)?"
                      r"(?:" + _COUNT + r"\s+)?" + _GROUP + r")*)\b", re.I)


def _who(line):
    found = WITH_WHO.search(line)
    if found:
        return found.group(1).strip(" ,.;:!?")
    bare = BARE_WHO.match(line)
    return bare.group(1).strip(" ,.;:!?") if bare else ""


def _how_long(line):
    found = FOR_HOW_LONG.search(line)
    if found:
        return found.group(1).strip(" ,.;:!?")
    bare = JUST_HOW_LONG.match(line.strip(" .,;:!?"))
    if bare:
        return (bare.group(1) or bare.group(2)).strip()
    return ""


def _how_getting_there(line):
    found = BY.search(line)
    return found.group(1).lower() if found else ""


def _by_the_sea(place):
    words = set(_low(place).replace("-", " ").split())
    return bool(words & (SEA_PLACES | {"beach", "beaches", "coast", "seaside", "sea", "shore"}))


def _a_carded_place(place):
    try:
        from ..knowledge import travel
    except Exception:
        return False
    key = _low(place).strip()
    if key.startswith("the "):
        key = key[4:]
    for name in ("CITIES", "BEST_TIME"):
        table = getattr(travel, name, None) or {}
        if key in {str(other).lower() for other in table}:
            return True
    return False


def a_moved_destination(line, memory):
    if not isinstance(memory, dict) or not line or "?" in line:
        return None
    place = facts.a_moved_place(line)
    if not place:
        return None
    if _the_last_line_named_an_animal(memory):
        return None
    live = _the_trip_so_far(memory)
    if not live:
        return {"place": place, "month": "", "when": "", "who": "", "how_long": "", "by": ""}
    if _low(_cap(live.get("place") or "")) == _low(place):
        return None
    _keep_the_new_place(memory, place, live.get("place") or "", line)
    return dict(live, place=place)


def _the_last_line_named_an_animal(memory):
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    said = ""
    for turn in reversed(turns):
        words = turn.get("user")
        if isinstance(words, str) and words.strip():
            said = words
            break
    if not said:
        return False
    found = facts.extract(said)
    return bool(found.get("pets") or found.get("pets_gone"))


def _keep_the_new_place(memory, place, old="", said=""):
    known = user(memory)
    old_place = str(old or "").strip()
    known["places"] = _the_place_put_right(known.get("places"), old_place, place)
    known["plans"] = _the_place_put_right(known.get("plans"), old_place, place)
    known["plan"] = next((entry for entry in known["plans"] if _low(place) in _low(entry)), place)
    log = memory.get("facts_log")
    if not isinstance(log, list):
        log = memory["facts_log"] = []
    log.append({"key": "places", "value": place, "turn": len(memory.get("turns") or []),
                "text": said})
    log.append({"key": "plan", "value": place, "turn": len(memory.get("turns") or []),
                "text": said})


def _the_place_put_right(entries, old, place):
    kept = []
    put_right = False
    for entry in (entries if isinstance(entries, list) else []):
        text = str(entry or "").strip()
        if not text:
            continue
        if old and _low(old) in _low(text):
            text = re.sub(re.escape(old), lambda _m: place, text, count=1, flags=re.I)
            put_right = True
        if text not in kept:
            kept.append(text)
    if not put_right and place not in kept:
        kept.append(place)
    return kept


def a_trip(text, memory, cards=True):
    line = str(text or "").strip()
    if not line or line.endswith("?"):
        return None
    kind = ack.reads_as_a_trip(line)
    if kind and kind != "trip":
        return None
    low = _low(line)
    if EVERYDAY_TRIP.search(low) or ON_A.search(low):
        return None
    if re.search(r"\bwent\b|\bhave been\b|\bwas in\b|\blast year\b", low):
        return None
    if re.search(r"\b(?:when|where|how|what|why|should|shall|can|could|would|will|worth)\b", low) \
            and not re.search(r"\b(?:we're|were|we are|i'm|im|i am)\b", low):
        return None
    visit = _a_person_visited(line)
    if visit:
        return {"place": visit, "month": _month(low), "when": _when_phrase(low),
                "who": _who(low), "how_long": _how_long(low), "by": "", "visit": True,
                "meal": bool(A_MEAL.search(low)), "baby": bool(A_NEW_BABY.search(low))}
    if not (GOING.search(low) or GOING_BARE.search(low)):
        return None
    place = _places(line)
    if not place:
        return None
    if cards and _a_carded_place(place) and not (BOOKED_DONE.search(low)
                                                and (_month(low) or _when_phrase(low))):
        return None
    if facts.extract(line).get("name"):
        return None
    return {"place": place, "month": _month(low), "when": _when_phrase(low),
            "who": _who(low), "how_long": _how_long(low), "by": _how_getting_there(low)}


def the_trip_they_booked(text):
    said = str(text or "")
    if not BOOKED.search(said):
        return "", ""
    place = _places(said)
    if not place:
        return "", ""
    return place, _month(said) or _when_phrase(said)


def _the_trip_so_far(memory):
    facts = user(memory)
    plans = [p for p in (facts.get("plans") or []) if isinstance(p, str) and p.strip()]
    latest = facts.get("plan")
    if isinstance(latest, str) and latest.strip():
        plans.append(latest)
    for plan in reversed(plans[-3:]):
        said = plan_line(memory, plan) or plan
        trip = a_trip(said, memory, cards=False)
        if trip:
            trip["plan"] = plan
            return trip
    for turn in reversed((memory.get("turns") or [])[-4:]):
        if not isinstance(turn, dict):
            continue
        trip = a_trip(turn.get("user") or "", memory, cards=False)
        if trip:
            trip["plan"] = ""
            return trip
    return None


def _asked_last(memory):
    return str(last_bot(memory) or "").strip().endswith("?")


def _told(text, memory):
    turns = memory.get("turns") or []
    return {_low(t.get("bot")) for t in turns if isinstance(t, dict)}


def _pick(options, memory, text):
    said = _told(text, memory)
    said_inside = " ".join(said)
    turns = memory.get("turns") or []
    fresh = [o for o in options
             if _low(o) not in said and not (len(o) > 15 and _low(o) in said_inside)]
    fresh = fresh or list(options)
    seed = 0
    for turn in turns[-4:]:
        if isinstance(turn, dict):
            seed = seed * 31 + sum(ord(c) for c in str(turn.get("user") or ""))
    seed = seed * 7919 + sum(ord(c) for c in str(text or "")) + len(turns)
    return fresh[seed % len(fresh)]


def _join(parts):
    out = []
    for part in parts:
        part = str(part or "").strip()
        if part:
            out.append(part[:1].upper() + part[1:])
    return " ".join(out)


SMALL = frozenset("of the and on in de du van der le la".split())


def _with_them(named, who, memory, line):
    ask = _pick(ASK_WHAT, memory, line)
    return "{0} with {1}. {2}".format(_mid(named), _yours(who).lower(),
                                      ask[:1].upper() + ask[1:])


def _yours(who):
    words = []
    for word in str(who or "").split():
        low = word.lower()
        if low in ("my", "our", "ours"):
            words.append("your" if low != "ours" else "yours")
        elif low == "mine":
            words.append("yours")
        else:
            words.append(word)
    return " ".join(words)


def _mid(named):
    named = str(named or "")
    return "the " + named[4:] if named.startswith("The ") else named


def _cap(text):
    text = str(text or "").strip()
    if not text:
        return text
    words = []
    for position, word in enumerate(text.split()):
        if position and word.lower() in SMALL:
            words.append(word.lower())
        elif word[:1].isalpha():
            words.append(word[:1].upper() + word[1:])
        else:
            words.append(word)
    return " ".join(words)


def _seasons_we_know(place):
    try:
        from ..knowledge import travel
    except Exception:
        return ""
    key = _low(place or "").strip()
    if key.startswith("the "):
        key = key[4:]
    if not key:
        return ""
    note = travel.CITY_BEST_TIME.get(key)
    if note:
        return note
    country = travel.CITY_COUNTRY.get(key, key)
    return travel.BEST_TIME.get(country) or travel.BEST_TIME.get(key) or ""


def _their_month(note, month):
    for sentence in re.split(r"(?<=[.!?])\s+", note):
        if re.search(r"\b" + month + r"\b", sentence.lower()):
            said = _mid(sentence.strip())
            return said[:1].upper() + said[1:]
    return ""


def _in_its_season(place, month):
    try:
        from ..knowledge import travel
    except Exception:
        return False
    picks = getattr(travel, "_MONTH_PICKS", None) or {}
    row = _low(picks.get(month) or "")
    if not row:
        return False
    key = _low(place or "").strip()
    if key.startswith("the "):
        key = key[4:]
    if len(key) < 4:
        return False
    return bool(re.search(r"\b" + re.escape(key) + r"\b", row))


def _a_winter_place(place):
    key = _low(place or "").strip()
    if key.startswith("the "):
        key = key[4:]
    return any(re.search(r"\b" + re.escape(word) + r"\b", key) for word in WINTER_SUN)


def _when_note(month, memory, text, booked=False, place=""):
    known = _seasons_we_know(place)
    if known:
        return _their_month(known, month)
    if month in QUIET and (_a_winter_place(place) or _in_its_season(place, month)):
        return _pick([n.format(month=_cap(month)) for n in SEASON_NOTES], memory, text)
    if month in PEAK:
        notes = PEAK_BOOKED_NOTES if booked else PEAK_NOTES
    elif month in BUSY:
        notes = BUSY_NOTES
    elif month in QUIET:
        notes = QUIET_NOTES
    else:
        return ""
    return _pick([n.format(month=_cap(month)) for n in notes], memory, text)


def _the_visit_length(how_long, memory, text):
    if not how_long:
        return ""
    low = _low(how_long)
    if "weekend" in low:
        return _pick(VISIT_A_WEEKEND, memory, text)
    if re.search(r"night|\bday", low):
        return _pick(VISIT_A_FEW_DAYS, memory, text)
    if re.search(r"week|fortnight|month", low):
        return _pick(VISIT_A_WEEK, memory, text)
    return ""


def _who_note(who, how_long, memory, text, place=None):
    notes = []
    if who and re.search(r"\bkids?\b|\bchild|\bchildren\b|\bbaby\b|\btoddler", who):
        if re.search(r"\b(?:two|three|four|five|six|\d+)\b", who):
            notes.extend(n.format(who=who) for n in KIDS_NUMBERED)
        else:
            notes.extend(KIDS_NOTES)
    if how_long and "weekend" in how_long:
        notes.extend(WEEKEND_NOTES)
    elif how_long and re.search(r"night|\bday", how_long):
        notes.extend(DAY_NOTES)
    elif how_long and re.search(r"week|fortnight|month", how_long):
        if re.search(r"two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|fortnight|\d",
                     how_long):
            notes.extend(LONG_NOTES)
        else:
            if place is None or _by_the_sea(place):
                notes.extend(WEEK_NOTES)
            else:
                notes.extend(WEEK_NOTES_LAND)
    if not notes:
        return ""
    return _pick(notes, memory, text)


def _a_note(month, who, how_long, memory, text, booked=False, place=""):
    parts = [n for n in (_when_note(month, memory, text, booked, place),
                         _who_note(who, how_long, memory, text, place)) if n]
    return _join(parts)


SOMEWHERE_TO_EAT = re.compile(
    r"^\s*(?:(?:and|also|plus|then|oh|ok|okay)\s+)?(?:somewhere|a place|anywhere)\s+"
    r"(?:good\s+|nice\s+|decent\s+)?to\s+(?:eat|have lunch|have dinner|get food|get something "
    r"to eat|grab a bite)\b", re.I)
SOMEWHERE_TO_STAY = re.compile(
    r"^\s*(?:(?:and|also|plus|then|oh|ok|okay)\s+)?(?:somewhere|a place|anywhere)\s+"
    r"(?:good\s+|nice\s+|cheap\s+)?to\s+(?:stay|sleep|stop over|kip)\b"
    r"|^\s*(?:(?:and|also|plus|then)\s+)?(?:a|any)\s+(?:good\s+|decent\s+|cheap\s+)?"
    r"(?:hotel|b&b|guesthouse|bed for the night)\b", re.I)
def _a_known_city(place):
    place = _low(place).strip(" .,;:!?")
    if not place:
        return False
    try:
        from ..knowledge.travel import CITIES
    except Exception:
        return False
    return place in CITIES or place.split()[0] in CITIES

EAT_WITHOUT_A_CARD = (
    "I cannot name a place in {place} without guessing, so narrow it yourself: set a budget a "
    "head and how far you will walk, then pick the shortest menu - a short one usually means the "
    "kitchen is cooking it fresh.",
    "{place} is not a town I can name places in, so go by the street: the shortest menu, and the "
    "place with people in it at six rather than the one with photos of the food outside.",
)
STAY_WITHOUT_A_CARD = (
    "I cannot name a hotel in {place} without guessing, so go by the area rather than the stars: "
    "near the station if it is one night, near where you will spend the evening if it is two, and "
    "reviews from this year rather than the rating.",
    "{place} is not a town I can name hotels in. Pick the area first - the station for one night, "
    "wherever you are eating for two - then check the recent reviews for noise.",
)
EAT_WITHOUT_A_TOWN = (
    "Where are you off to? With a town I can point you at an end of it. Without one: set a budget "
    "a head and how far you will walk, then pick the shortest menu - a short one usually means "
    "the kitchen is cooking it fresh.",
    "Tell me the town and I will narrow it down. Failing that: a short menu, and the place that "
    "is busy at six rather than the one with photos of the food outside.",
)
EAT_ADVICE = (
    "Set a budget per head and how far you will walk, then pick the shortest menu - a short one "
    "usually means the kitchen is cooking it fresh, and the place with people in it at six beats "
    "the one with photos of the food outside.",
)
STAY_ADVICE = (
    "Go by the area rather than the stars: near the station if it is one night, near where you "
    "will spend the evening if it is two, and read reviews from this year rather than the rating.",
)
STAY_WITHOUT_A_TOWN = (
    "Where will you be? With a town I can say which area to look in. Without one: near the "
    "station if it is one night, near where you will eat if it is two, and reviews from this year "
    "rather than the star rating.",
    "Tell me where and I will point at an end of it. Failing that: go by the area rather than the "
    "hotel - the station for one night, the evening's end of town for two.",
)


def _the_areas_of(place):
    try:
        from ..knowledge.travel import CITY_AREA
    except Exception:
        return ""
    return str(CITY_AREA.get(_low(place).strip(" .,;:!?")) or "")


def _somewhere_for(line, memory):
    eat = bool(SOMEWHERE_TO_EAT.search(line))
    stay = bool(SOMEWHERE_TO_STAY.search(line))
    if not (eat or stay):
        return None
    trip = _the_trip_so_far(memory) or {}
    place = _cap(_as_a_visit(str(trip.get("place") or "")))
    if not place:
        understood = memory.get("understood")
        ref = understood.get("ref") if isinstance(understood, dict) else None
        if isinstance(ref, dict) and ref.get("there"):
            place = _cap(str(ref["there"]))
    if not place:
        for found in reversed([p for p in (user(memory).get("places") or []) if p]):
            place = _cap(str(found))
            break
    if not place:
        for turn in reversed([t for t in (memory.get("turns") or []) if isinstance(t, dict)]):
            said = _places(str(turn.get("user") or ""))
            if said:
                place = _cap(said)
                break
    if place and _a_known_city(place) and (eat or _the_areas_of(place)):
        return None
    if place:
        pool = EAT_WITHOUT_A_CARD if eat else STAY_WITHOUT_A_CARD
        return _pick([line.format(place=_mid(place)) for line in pool], memory, line)
    if _asked_last(memory):
        return _pick(list(EAT_ADVICE if eat else STAY_ADVICE), memory, line)
    return _pick(list(EAT_WITHOUT_A_TOWN if eat else STAY_WITHOUT_A_TOWN), memory, line)


WEEKEND_AWAY = re.compile(
    r"\b(?:weekend away|weekend break|long weekend|mini ?break|short break|few days away|"
    r"going away|get away|"
    r"(?:away|off) for (?:a|two|three|four|five|\d+) (?:week|weeks|fortnight|days?|months?)|"
    r"for (?:a fortnight|two weeks))\b", re.I)
A_BABY = re.compile(
    r"\b(?:bab(?:y|ies)|newborns?|toddlers?|infants?|napp(?:y|ies)|prams?|pushchair|"
    r"changing bag|baby bag|nurser(?:y|ies)|breastfeed\w*|formula|due date|expecting|"
    r"pregnan\w*)\b")


def _the_kind_of_trip(how_long):
    said = _low(how_long)
    if "weekend" in said:
        return "a weekend away"
    if "fortnight" in said:
        return "a fortnight away"
    if re.search(r"\bweek", said):
        return "a week away"
    if re.search(r"\bmonth", said):
        return "a month away"
    if re.search(r"\bday", said):
        return "a few days away"
    return "a weekend away"


def _the_warm_week_is_out_of_season(month):
    return _low(month or "").strip() in OUT_OF_SEASON


def _an_event_not_a_place(place):
    bare = _low(place or "").strip()
    for word in ("a ", "an ", "the ", "my ", "our "):
        if bare.startswith(word):
            bare = bare[len(word):]
            break
    return bare in AN_EVENT_NOT_A_PLACE


def a_packing_question_about_the_trip(text, memory):
    if not isinstance(memory, dict):
        return None
    line = _low(text)
    found = PACKING.search(line) if line else None
    if not found or A_BABY.search(line):
        return None
    for turn in (memory.get("turns") or [])[-6:]:
        if isinstance(turn, dict) and A_BABY.search(_low(turn.get("user"))):
            return None
    live = _the_trip_so_far(memory)
    if not live:
        for turn in reversed([t for t in (memory.get("turns") or [])[-4:]
                              if isinstance(t, dict)]):
            said = _low(turn.get("user"))
            if WEEKEND_AWAY.search(said) and not said.strip().endswith("?"):
                live = {"place": "", "month": _month(said), "when": "", "who": _who(said),
                        "how_long": _how_long(said) or "a weekend", "by": "", "plan": ""}
                break
    if not live:
        return None
    tail = found.group(1).strip(" ?.!,")
    place = _low(live.get("place"))
    if _an_event_not_a_place(place):
        return None
    if tail and not (PACKING_FOR.match(tail) or (place and tail == "for " + place)):
        return None
    return live


def the_bag_beats_the_list(text, memory):
    live = a_packing_question_about_the_trip(text, memory)
    return bool(live) and _the_warm_week_is_out_of_season(live.get("month"))


def reply_for(text, memory, cards=True):
    if not isinstance(memory, dict):
        return None
    line = " ".join(str(text or "").split())
    if not line:
        return None
    moved = a_moved_destination(line, memory)
    if moved:
        return _start(_a_new_trip(line, moved, memory))
    trip = a_trip(line, memory, cards=cards)
    if trip:
        return _start(_a_new_trip(line, trip, memory))
    if A_STAY_LENGTH.search(line):
        live = _the_trip_so_far(memory)
        if live and live.get("visit"):
            return _start(_pick(VISIT_HOW_LONG, memory, line))
    somewhere = _somewhere_for(line, memory)
    if somewhere:
        return _start(somewhere)
    about_the_trip = (PACKING.search(line) or PACKING_SAID.match(line) or THE_DRIVE.search(line)
                      or THE_FLIGHT.search(line) or THE_JOURNEY_ASK.search(line))
    if (JUST_A_DETAIL.match(line) or _only_a_length(line) or PACKING_SAID.match(line)
            or THE_JOURNEY_ASK.search(line)) \
            and (not line.endswith("?") or about_the_trip):
        live = _the_trip_so_far(memory) or a_packing_question_about_the_trip(line, memory)
        if live:
            detail = _a_detail(line, live, memory)
            if detail:
                return _start(detail)
    if THE_LENGTH_ASK.search(line) and not (THE_FLIGHT.search(line) or THE_DRIVE.search(line)
                                            or THE_JOURNEY_ASK.search(line)
                                            or THE_MODE.search(line)):
        live = _the_trip_so_far(memory)
        if live and not live.get("how_long") and not _a_length_said(memory):
            return _start(_the_length_asked(live, memory, line))
    month = _the_month_answered(line, memory)
    if month:
        live = _the_trip_so_far(memory)
        if live:
            live = dict(live, month=month)
            return _start(_a_new_trip(line, live, memory))
    return None


JUST_A_MONTH = re.compile(
    r"^\s*(?:in\s+|next\s+|this\s+|maybe\s+|probably\s+|its\s+|it's\s+|er,?\s+)*"
    r"([a-z]+)\s*[.!]?\s*$", re.I)


def _only_a_length(line):
    bare = _low(line).strip(" .,;:!?")
    bare = re.sub(r"^(?:its|it's|thats|that's|were|we're|we are|there|were there|"
                  r"its for|its about|we're there)\s+", "", bare).strip()
    return bool(FOR_HOW_LONG.fullmatch(bare) or JUST_HOW_LONG.match(bare))


def _the_month_answered(line, memory):
    asked = _low(last_bot(memory))
    if "when" not in asked:
        return ""
    found = JUST_A_MONTH.match(line)
    if not found:
        return ""
    word = found.group(1).lower()
    return word if word in MONTHS else ""


_PLURAL_PEOPLE = frozenset(("parents", "grandparents", "children", "kids", "family", "relatives",
                            "folks", "friends", "twins", "in laws", "in-laws", "inlaws"))


def _as_a_visit(place):
    match = A_PERSON_IS_NOT_A_PLACE.match(place)
    if not match:
        return place
    person = match.group("person")
    low = person.lower()
    own = (match.group("poss") or "").replace("\u2019", "'")
    if own:
        owner = person + own
    elif low in _PLURAL_PEOPLE:
        owner = person + ("'" if low.endswith("s") else "'s")
    else:
        owner = person + "'s"
    rest = place[match.end():].strip(" .,;:!?")
    first = rest.split()[0].lower() if rest else ""
    if rest and first not in _NOT_A_THING_OF_THEIRS:
        return "your " + owner + " " + rest
    return "your " + owner


def _a_new_trip(line, trip, memory):
    visit = _as_a_visit(trip["place"])
    place, who = _cap(visit), trip["who"]
    month = trip["month"]
    outing = OUTING.match(_low(trip["place"]))
    if outing:
        word = outing.group(1).lower()
        sea = word in SEA
        said = "A day {0} the {1}, {2}. ".format("in" if word in OPEN_AIR else "at", word,
                                                 _pick(WARM, memory, line))
        who_note = ""
        if who and sea:
            who_note = _who_note(who, trip["how_long"], memory, line)
        if who_note:
            return said + _join([who_note])
        notes = SEA_NOTES if sea else INDOOR_NOTES if word in TICKETED else LAND_NOTES
        return said + _join([_pick(notes, memory, line)])
    day = trip.get("when") or ""
    day = day if day in DAYS and day != "weekend" else ""
    named = place + (" in " + _cap(month) if month else (" on " + _cap(day) if day else ""))
    if who:
        named += " with " + _yours(who)
    booked = bool(re.search(r"\bbook", line, re.I))
    said = ("{0} is booked, then. ".format(named) if booked else
            "{0}, {1}. ".format(named, _pick(WARM, memory, line)))
    if visit != trip["place"]:
        note = _join([part for part in (_who_note(who, "", memory, line),
                                       _the_visit_length(trip["how_long"], memory, line)) if part])
        if note:
            return _join([said, note])
        ask = _pick(ASK_VISIT, memory, line)
        return _join([said, ask[:1].upper() + ask[1:]])
    note = _a_note(month, who, trip["how_long"], memory, line, booked, trip["place"])
    if note:
        return said + note
    if booked:
        return said + "Get the big days out booked now too, and you can take the rest as it comes."
    if not month and day:
        return said.strip()
    if not month and trip.get("when"):
        return said + _pick(ASK_WHAT, memory, line)[:1].upper() + _pick(ASK_WHAT, memory, line)[1:]
    if not month:
        if _asked_last(memory):
            return _pick(ASK_WHEN_NO_QUESTION, memory, line).format(place=place)
        return _pick(ASK_WHEN, memory, line).format(place=place)
    return said + _pick(ASK_WHAT, memory, line)[:1].upper() + _pick(ASK_WHAT, memory, line)[1:]


def _a_length_said(memory):
    for turn in reversed(memory.get("turns") or []):
        if not isinstance(turn, dict):
            continue
        text = str(turn.get("user") or "")
        if not text or text.rstrip().endswith("?"):
            continue
        found = FOR_HOW_LONG.search(text)
        if found:
            return found.group(1)
    return None


def _the_length_asked(trip, memory, line):
    place = _cap(_as_a_visit(trip.get("place") or ""))
    month = trip.get("month") or ""
    options = THE_LENGTH_NOT_SAID
    if place:
        named = _mid(place + (" in " + _cap(month) if month else ""))
        options = tuple(n.format(named=named) for n in THE_LENGTH_NOT_SAID_NAMED)
    return _join([_pick(options, memory, line), _pick(THE_NIGHTS_FIRST, memory, line)])


def _a_detail(line, trip, memory):
    low = _low(line)
    place, month = _cap(_as_a_visit(trip["place"])), trip["month"]
    named = place + (" in " + _cap(month) if month else "")
    who = _who(low) or ""
    how_long = _how_long(low)
    by = _how_getting_there(low) if _low(place) not in low else ""
    told = []
    named = _mid(named)
    kids = re.search(r"\bkids?\b|\bchild|\bchildren\b|\bbaby\b|\btoddler", who or "")
    packing = PACKING.match(low) or PACKING_SAID.match(low)
    if packing:
        tail = packing.group(1).strip(" ?.!,")
        said_as_a_need = bool(PACKING_SAID.match(low))
        if not place:
            kind = _the_kind_of_trip(trip.get("how_long") or "")
            if month:
                pool = [n.format(kind=kind, month=_cap(month)) for n in PACKING_NO_PLACE]
            else:
                pool = [n.format(kind=kind) for n in PACKING_NO_PLACE_NO_MONTH]
            return _join([_pick(pool, memory, line)])
        if trip.get("visit"):
            if said_as_a_need and _one_thing_they_need(low):
                return None
            if trip.get("baby"):
                return _pick(VISIT_PACKING_FOR_A_BABY, memory, line)
            if trip.get("meal"):
                return _pick(VISIT_PACKING_FOR_A_MEAL, memory, line)
            return _pick([n.format(place=_mid(place)) for n in VISIT_PACKING], memory, line)
        if tail and not said_as_a_need and not (PACKING_FOR.match(tail)
                                                or _low(tail) == "for " + _low(place)):
            return None
        if _an_event_not_a_place(place):
            return None
        if month:
            notes = [n.format(place=_mid(place), month=_cap(month)) for n in PACKING_NOTES]
        else:
            notes = [n.format(place=_mid(place)) for n in PACKING_NO_MONTH]
        if kids:
            notes.append(PACKING_WITH_KIDS)
        return _join([_pick(notes, memory, line)])
    if (THE_FLIGHT.search(low) or THE_DRIVE.search(low)) and HOW_LONG_ASK.search(low) \
            and _a_carded_place(place):
        return None
    if not by and not THE_MODE.search(low):
        if THE_FLIGHT.search(low):
            by = "flying"
        elif THE_DRIVE.search(low):
            by = "driving"
        elif THE_JOURNEY_ASK.search(low):
            by = "driving" if JOURNEY_MODE.search(low) else "either"
    if by == "either" or (not by and THE_MODE.search(low)):
        told.append("To {0}: the car or the train if it is a few hours, a flight if it is not - "
                    "the train is the one you can leave late on.".format(named))
    elif by in ("driving", "by car"):
        told.append("Driving to {0}, so leave early and take the break halfway - the last hour "
                    "is the one that drags.".format(named))
    elif by in ("flying", "by plane"):
        told.append("Flying to {0} - take the early flight, because the day you lose waiting "
                    "around is the first day of the trip.".format(named))
    elif by in ("getting the train", "on the train", "by train", "getting a train"):
        told.append("Taking the train to {0} is the easy way in - book it now, the cheap seats "
                    "go first.".format(named))
    elif by in ("taking the ferry", "getting a ferry", "sailing", "by ferry"):
        told.append("On the ferry to {0}, so book it now - the summer crossings fill up."
                    .format(named))
    if told:
        if who:
            told.append(_who_note(who, how_long, memory, line, place)
                        or _with_them(named, who, memory, line))
        return _join([t for t in told if t])
    if who and kids:
        return _join([_who_note(who, how_long, memory, line, place)])
    if who:
        return _with_them(named, who, memory, line)
    note = _who_note(who, how_long, memory, line, place)
    if note:
        return _join([note])
    return None
