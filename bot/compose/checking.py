import re

from ..memory.facts import COUNTRIES

HOME_NATIONS = frozenset("""england scotland wales britain uk ireland northern ireland""".split())
from . import pick

HOME_COUNTRIES = frozenset((
    "united kingdom", "england", "scotland", "wales", "northern ireland", "great britain",
    "britain", "uk", "ireland",
))
NOT_HOME_COUNTRIES = tuple(sorted(
    (name for name in COUNTRIES if name not in HOME_COUNTRIES), key=len, reverse=True))
MOVE_HOME_NAMES = frozenset((
    "united kingdom", "england", "scotland", "wales", "northern ireland", "great britain",
    "britain", "uk",
))
_A_NAMED_COUNTRY = None


def _a_named_country_in(text):
    global _A_NAMED_COUNTRY
    if _A_NAMED_COUNTRY is None:
        from ..knowledge.geography import COUNTRIES as all_countries, _COUNTRY_ALIASES
        names = sorted((set(all_countries) | set(_COUNTRY_ALIASES)) - MOVE_HOME_NAMES,
                       key=len, reverse=True)
        _A_NAMED_COUNTRY = re.compile(
            r"\b(?:" + "|".join(re.escape(name) for name in names) + r")\b", re.I)
    return bool(_A_NAMED_COUNTRY.search(text or ""))

SERVICES = (
    ("iplayer", "iPlayer"), ("bbc iplayer", "iPlayer"), ("itv hub", "ITV Hub"),
    ("itvx", "ITVX"), ("itv", "ITV"), ("channel 4", "Channel 4"), ("all 4", "All 4"),
    ("4od", "All 4"), ("my5", "My5"), ("netflix", "Netflix"), ("prime video", "Prime Video"),
    ("amazon prime", "Prime Video"), ("disney plus", "Disney+"),
    ("disney+", "Disney+"), ("now tv", "Now TV"), ("nowtv", "Now TV"), ("apple tv", "Apple TV"),
    ("paramount", "Paramount+"), ("britbox", "BritBox"), ("hayu", "Hayu"), ("sky go", "Sky Go"),
    ("sky q", "Sky Q"), ("sky tv", "Sky"), ("sky cinema", "Sky Cinema"),
    ("sky sports", "Sky Sports"), ("spotify", "Spotify"), ("audible", "Audible"),
    ("youtube", "YouTube"),
)
NOT_AVAILABILITY = re.compile(
    r"\b(?:stopping|stops|stopped|buffer\w*|glitch\w*|not working|keeps? (?:cutting|freezing|"
    r"loading)|wont play|won't play|password|log ?in|sign ?up|account|cancel\w*|subscri\w*|"
    r"price|prices|cost|costs|cheaper|worth it|share|sharing|binge|download\w*|aeroplane|"
    r"plane|offline|recommend|any good|what to watch|something to watch|worth watch\w*|"
    r"turn (?:off|on)|settings|autoplay|auto play|notification\w*|episodes? (?:left|to go)|"
    r"(?:anything|something|whats|what's)\s+(?:\w+\s+){0,2}(?:funny|good|scary|sad|new|"
    r"decent|chilled|violent|easy)\b|"
    r"what (?:can|could|should) (?:i|we) (?:watch|see|stream)|"
    r"(?:anything|something) (?:good )?(?:on|to watch))\b", re.I)

TRAVEL = {
    "train": ("train", "trains"), "trains": ("train", "trains"), "bus": ("bus", "buses"),
    "buses": ("bus", "buses"), "coach": ("coach", "coaches"), "tube": ("tube", ""),
    "underground": ("tube", ""), "metro": ("metro", ""), "tram": ("tram", "trams"),
    "ferry": ("ferry", "ferries"), "ferries": ("ferry", "ferries"),
}

_A_COMPARISON = (r"(?:best|quickest|fastest|easiest|cheapest|simplest|shortest|safest|"
                 r"most direct|nicest|prettiest)")
GET_FROM_TO = re.compile(
    r"\bhow (?:do|can|would|could) (?:i|we|you) (?:get|travel)\s+(?:to|from)\b[^?.]{0,30}\bfrom\b|"
    r"\b(?:" + _A_COMPARISON + r"\s+)?(?:route|journey|drive|commute)\s+to\b[^?.]{0,30}\bfrom\b|"
    r"\b" + _A_COMPARISON + r"\s+(?:way|route)\s+(?:to|of)\s+(?:get|getting|travel|travelling)"
    r"\s+(?:to|from)\b[^?.]{0,30}\bfrom\b|"
    r"\b" + _A_COMPARISON + r"\s+(?:way|route)\s+from\b[^?.]{0,30}\bto\b|"
    r"\b" + _A_COMPARISON + r"\s+(?:way|route)\s+(?:to|of)\s+(?:get|getting|travel|travelling)"
    r"\s+from\b[^?.]{0,30}\bto\b|"
    r"\bhow long (?:does it|will it|would it) take to (?:get|drive|travel|cycle|walk)\s+to\b"
    r"[^?.]{0,30}\bfrom\b|"
    r"\bhow (?:do|can|would|could) (?:i|we|you) (?:get|travel)\s+from\b[^?.]{0,30}\bto\b", re.I)
WANTS_A_TIME = re.compile(
    r"\b(?:what time|whatt?ime|how long|last|first|next|earliest|latest|timetable|doable|"
    r"won'?t make|is there a|are there any|how often)\b", re.I)
NOT_A_DESTINATION = re.compile(
    r"\bget(?:ting)?\s+(?:to\s+)?(?:sleep|rid|grips|know|understand|talk|the\s+(?:point|bottom)|"
    r"terms|an?\s+agreement|a\s+decision|the\s+root)\b|"
    r"\bget(?:ting)?\s+(?:over|through|around|on\s+top\s+of|out\s+of|away\s+with|the\s+hang)\b",
    re.I)
NOT_A_JOURNEY = re.compile(
    r"\b(?:delayed|delay|cancelled|cancel|refund|ticket price|how much is .{0,20}ticket|"
    r"season ticket|railcard|strike|replacement bus|sleeper|i'?m on (?:the|a) "
    r"(?:train|bus)|on the (?:train|bus)|lost property|left (?:my|her|his) \w+ on)\b", re.I)

PICKS = (
    (("beach", "beaches"), "beaches"),
    (("pub", "pubs"), "pubs"),
    (("restaurant", "restaurants", "place to eat", "places to eat", "eatery"), "restaurants"),
    (("cafe", "cafes", "coffee shop", "coffee shops"), "cafes"),
    (("walk", "walks", "hike", "hikes"), "walks"),
    (("park", "parks"), "parks"),
    (("market", "markets"), "markets"),
    (("museum", "museums", "gallery", "galleries"), "museums and galleries"),
    (("chippy", "chippies"), "chip shops"),
    (("thing to do", "things to do", "day out", "day trip"), "things to do"),
)
SHOPS = (
    ("aldi", "Aldi"), ("lidl", "Lidl"), ("tesco", "Tesco"), ("asda", "Asda"),
    ("sainsbury's", "Sainsbury's"), ("sainsburys", "Sainsbury's"), ("morrisons", "Morrisons"),
    ("waitrose", "Waitrose"), ("iceland", "Iceland"), ("co-op", "the Co-op"), ("coop", "the Co-op"),
    ("boots", "Boots"), ("superdrug", "Superdrug"), ("argos", "Argos"), ("amazon", "Amazon"),
    ("ebay", "eBay"), ("ikea", "IKEA"), ("currys", "Currys"), ("screwfix", "Screwfix"),
    ("b&q", "B&Q"), ("b and q", "B&Q"), ("homebase", "Homebase"), ("wickes", "Wickes"),
    ("halfords", "Halfords"), ("decathlon", "Decathlon"), ("sports direct", "Sports Direct"),
    ("john lewis", "John Lewis"), ("marks and spencer", "Marks and Spencer"), ("m&s", "M&S"),
    ("poundland", "Poundland"), ("home bargains", "Home Bargains"), ("the range", "The Range"),
    ("dunelm", "Dunelm"), ("asos", "ASOS"), ("wickes", "Wickes"),
)
SHOP_ASK = re.compile(
    r"\b(?:how long|how much|do they|do you|does it|can i|when|delivery|deliver|in stock|"
    r"stock|return|returns|refund|click and collect|collect|charge|postage|warranty|"
    r"guarantee|trade ?in|price|prices|cost)\b", re.I)
PICK_NOT = {
    "beach": re.compile(r"\b(?:read|reads|book|books|novel|towel|body|volleyball|ball|hut|"
                        r"huts|wedding|holiday\s+read)\b", re.I),
    "park": re.compile(r"\b(?:the car|my car|your car|the van|the bike|it there|carefully|"
                       r"properly|legally)\b", re.I),
    "walk": re.compile(r"\b(?:the dog|my dog|to work|to school|home|back|the kids to|"
                       r"take|taking|wear|wearing|bring|bringing|pack|packing|carry|boots|"
                       r"shoes|rain|wet|long|short|slow|fast|bit of a)\b", re.I),
    "market": re.compile(r"\b(?:the car|to buy|flog|sell)\b", re.I),
    "thing to do": re.compile(r"\b(?:with it|with them|with the|today|tonight|now|this evening|"
                              r"picnic|take|bring|pack)\b", re.I),
    "restaurant": re.compile(r"\b(?:wear|wearing|wore|dress|order|book a table|booking)\b", re.I),
    "chippy": re.compile(r"\b(?:order|nice from|to have|whats nice|what is nice)\b", re.I),
}
A_TIME_NOT_A_PLACE = (
    r"(?:dinner|dinnertime|dinner\s+time|lunch|lunchtime|lunch\s+time|breakfast|"
    r"breakfast\s+time|tea|teatime|tea\s+time|supper|brunch|snack|elevenses|"
    r"bed|bedtime|bed\s+time|nap|naptime|nap\s+time|playtime|play\s+time|bathtime|"
    r"bath\s+time|homework|pickup|pick\s+up|school\s+run|morning|mornings|afternoon|"
    r"afternoons|evening|evenings|night|nights|tonight|midday|noon|time)")
A_NOT_A_PLACE = (
    r"(?:(?:the|a|an)\s+)?"
    r"(?:eat|go|walk|do|take|get|see|find|pick|order|book|be|have|" + A_TIME_NOT_A_PLACE + r")\b")
A_PLACE = re.compile(
    r"\b(?:in|near|around|round|at|by|beside|from|to|outside|inside)\s+"
    r"(?!" + A_NOT_A_PLACE + r")[a-z]", re.I)
WANTS_A_PICK = re.compile(
    r"\b(?:best|good|nice|decent|any good|recommend|worth|where should|what should|"
    r"suggest|anywhere|favourite|favorite|top)\b", re.I)

A_MEAL_TIME = re.compile(
    r"\b(?:at|for|before|after|around|over)\s+(?:the\s+|my\s+|our\s+)?"
    r"(?:dinner|dinner\s*time|lunch|lunch\s*time|breakfast|breakfast\s*time|tea|tea\s*time|"
    r"supper|supper\s*time|brunch|tea ?time)\b", re.I)
A_PART_OF_DAY = re.compile(
    r"\b(?:at|in|during|over|before|after|this|tomorrow|next)\s+"
    r"(?:the\s+|my\s+|our\s+)?"
    r"(?:morning|afternoon|evening|night|midday|noon|bedtime)\b", re.I)
WANTS_A_PLAN = re.compile(
    r"\b(?:what|anything|any|how)\b[^?]{0,32}\b(?:should|shall|can|could|do)\s+(?:i|we)\s+do\b"
    r"|\bwhat\s+to\s+do\b|\bhow\s+(?:do|should)\s+(?:i|we)\s+(?:fill|pass|plan|spend)\b"
    r"|\banything\s+(?:to\s+do|planned|on|happening)\b"
    r"|\bwhat(?:'s|s|\s+s|\s+is|\s+else\s+is)?\s+(?:on|happening|going\s+on|good\s+to\s+do)\b",
    re.I)
AN_ON_ASK = re.compile(
    r"\bwhat(?:'s|s|\s+s|\s+is|\s+else\s+is)?\s+(?:on|happening|going\s+on)\b"
    r"|\banything\s+(?:on|happening)\b", re.I)
MEAL_TIME_POOL = (
    "Meals are the part worth pinning down: decide the one thing you are eating and keep the rest "
    "plain, and the time sorts itself out. What have you got in the fridge?",
    "At that time of day the trap is deciding it late. Pick the food first - something you can do "
    "with one pan is plenty - and let the rest of it be whatever it is. What do you fancy?",
    "One thing cooked and one thing cold is a meal, and it takes about twenty minutes. Tell me "
    "what is in the house and I will say which of them to use.",
)
PART_OF_DAY_POOL = (
    "The part of the day that works has one thing in it you actually want to do, and nothing else "
    "booked round it. What would that one thing be?",
    "Fill it from the other end: what would you be sorry to have missed by bedtime? That is the "
    "one thing, and the rest of the time can look after itself. What sounds good?",
    "Days like that are easier when the shape is set rather than the plan: one thing out of the "
    "house, one meal, and the rest left loose. What kind of thing do you enjoy doing?",
)


def _a_time_of_day(said):
    if not said:
        return None
    meal = A_MEAL_TIME.search(said)
    part = A_PART_OF_DAY.search(said)
    if not (meal or part) or not WANTS_A_PLAN.search(said):
        return None
    if NOT_A_DAY_OUT_PLACE.search(said):
        return None
    rest = said
    for match in (meal, part):
        if match:
            rest = rest.replace(match.group(0), " ")
    if A_PLACE.search(rest) or A_PLACE_THERE.search(rest):
        return None
    meal_pool = meal and not AN_ON_ASK.search(said)
    return pick(MEAL_TIME_POOL if meal_pool else PART_OF_DAY_POOL, {}, said)


THINGS_TO_DO_POOL = (
    "A day that works most places is one big thing in the morning and nothing booked after "
    "it, though I don't know this place well enough to name the things: one worth the journey "
    "out, one long lunch, the rest loose. What do you usually enjoy doing?",
    "Naming places I have not been to would be guessing, so here is the shape of a day "
    "instead: one big thing in the morning, one long lunch, and nothing booked after it. Are "
    "you after coast and walking, or food and towns?",
    "Pick the one thing you would be sorry to miss and plan the day round that, though I "
    "can't recommend places I have not been to: it decides where you stay, when you eat and "
    "what you drop. What sort of thing do you like doing?",
)
WANTS_A_THING_DONE = re.compile(
    r"\b(?:what|anything|something|where)\b[^?.!]{0,18}\b(?:to do|to see|to visit)\b|"
    r"\b(?:things|stuff) to do\b", re.I)
ASKS_WHAT_TO_DO = re.compile(
    r"\bwhat (?:should|shall|can|could|do) (?:i|we|you) do\b|"
    r"\bwhat (?:should|shall|can|could) (?:i|we|you) (?:see|visit)\b|"
    r"\bwhats there to do\b|\bwhat is there to do\b", re.I)
WANTS_A_DAY_OUT = re.compile(
    WANTS_A_THING_DONE.pattern + "|" + ASKS_WHAT_TO_DO.pattern, re.I)
DAY_OUT_NOT = re.compile(
    r"\b(?:about|to (?:sleep|stop|help|get|fix|make|keep)|for (?:my|the) )|"
    r"\b(?:in|at|round|around) the (?:morning|afternoon|evening|night|weekend|meantime|garden|"
    r"kitchen|office|house|home|shed|garage|bedroom|bathroom|flat|car|shower|bath)\b", re.I)
A_THING_IN_HAND = re.compile(
    r"\bwith (?:it|them|him|her|this|that|an?|a)\b|"
    r"\bwith (?:the|my) (?!kids|children|family|parents|boys|girls|toddler|baby|dog|"
    r"grandparents|grandchildren|niece|nephew|in-laws)\w+", re.I)
A_PLACE_THERE = re.compile(r"\b(?:there|here|nearby|round here|around here)\b", re.I)
A_BARE_DAY_OUT = re.compile(
    r"^\W*(?:(?:so|and|ok|okay|right|then|also|but)[\s,]+)*"
    r"(?:what|anything|something)\b[^?.!]{0,18}\b(?:to do|to see|to visit)\b|"
    r"^\W*(?:(?:so|and|ok|okay|right|then|also|but)[\s,]+)*"
    r"(?:things|stuff) to do\b|"
    r"^\W*(?:(?:so|and|ok|okay|right|then|also|but)[\s,]+)*"
    r"(?:what|where) (?:should|shall|can|could|do) (?:i|we|you) (?:do|see|visit)\b", re.I)
A_TRIP_BEFORE = re.compile(
    r"\b(?:going to|going away|off to|flying to|driving to|heading to|travelling to|traveling to|"
    r"holiday|holidays|trip to|weekend in|week in|fortnight in|visiting|booked|days in)\b", re.I)
NOT_A_DAY_OUT_PLACE = re.compile(
    r"\b(?:hospital|doctors?|dentist|gp|clinic|ward|surgery|a&e|court|work|school|nursery|"
    r"college|uni|university|interview|funeral|wedding|christening|prison|jail|care home|"
    r"vets?|physio|therapist|my mum|my dad|my sister|my brother|my son|my daughter|my kids|"
    r"my gran|my nan|my grandma|my grandad|my husband|my wife)\b", re.I)

A_TIME_AFTER = (
    r"(?!\s*(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"a\s+few|few|a\s+couple|next|this|last|the\s+(?:next|new|coming|end)|"
    r"january|february|march|april|may|june|july|august|september|october|november|"
    r"december|spring|summer|autumn|winter)\b)")
ABROAD = re.compile(
    r"\b(?:abroad|overseas|emigrat\w*|expat\w*|visa|residency|passport for|work permit|"
    r"right to (?:live|work)|liv(?:e|ing) abroad|work(?:ing)? abroad)\b"
    r"|\b(?:relocat|retir|buy(?:ing)? (?:a|an) (?:house|flat|place))\w*\b[^?.]{0,25}"
    r"\b(?:to|in|abroad)\b" + A_TIME_AFTER +
    r"|\bmov\w*\b(?!\s*out\b)[^?.]{0,25}\b(?:to|in|abroad)\b" + A_TIME_AFTER, re.I)
MOVING = re.compile(
    r"\b(?:mov|relocat|retir|buy(?:ing)? (?:a|an) (?:house|flat|place))\w*\b[^?.]{0,25}"
    r"\b(?:to|in|abroad)\b", re.I)
GOING_AWAY = re.compile(
    r"\b(?:abroad|overseas|emigrat\w*|expat\w*|planning to (?:move|go|leave)|"
    r"going to (?:move|emigrate)|thinking of (?:moving|emigrating|leaving)|"
    r"want(?:s|ed)? to (?:move|emigrate|live) (?:to|abroad|overseas))\b", re.I)
A_THING_NOT_A_PLACE = re.compile(
    r"\b(?:phone|mobile|laptop|computer|pc|tablet|account|money|funds|savings|isa|pension|bin|"
    r"box|boxes|photos?|files?|data|number|direct debit|standing order|everything|furniture|"
    r"house|flat|home|office|job|team|city|town|area|school|bedroom|kitchen)\b", re.I)
NOT_THE_PAPERWORK = re.compile(
    r"\b(?:how do i (?:ask|raise|bring (?:it )?up|mention|broach)|who do i ask|"
    r"ask (?:my|your|the) (?:boss|manager|employer)|talk to (?:my|your) (?:boss|manager)|"
    r"send(?:ing)? (?:money|cash)|transfer(?:ring)? (?:money|cash)|ripped off|scam\w*|"
    r"how much (?:money|cash) (?:to|can)|"
    r"mov(?:e|ing|ed) (?:in|on)\b|"
    r"(?:phone|mobile).{0,25}(?:charges?|roaming|data|contract|plan))\b", re.I)
MOVING_HOUSE = re.compile(
    r"\b(?:house|flat|home|office|job|team|city|town|area|neighbourhood|school)\b", re.I)
COUNCIL_WORD = re.compile(
    r"\b(?:council|councils|council tax|local authority|permit|planning permission|byelaw\w*|"
    r"blue badge|housing benefit|bulky waste|licensing|premises licence|taxi licence)\b", re.I)
PARKING_RULE = re.compile(
    r"\b(?:park|parking)\b[^?.]{0,30}\b(?:allowed|legal|illegal|ok|okay|fine|ticket|permit|"
    r"charge|charges|charged|free|sunday|sundays|resident\w*|restriction\w*|badge|disabled)\b|"
    r"\b(?:allowed|legal|illegal|ok|okay|fine|against the rules)\b[^?.]{0,25}\bpark\b|"
    r"\b(?:can|could|am i allowed to|are we allowed to|where can i|where should i|is it ok to|"
    r"is it okay to)\b[^?.]{0,20}\bpark\b", re.I)
WANTS_THE_RULES = re.compile(
    r"\b(?:can i|could i|do i|does it|how do i|how can i|what do i|what are the|whats the|"
    r"what's the|am i allowed|is it (?:allowed|legal|ok|okay|possible)|are we allowed|"
    r"will i|do we|who do i|where do i|how much is the|"
    r"how about|what about|thoughts on|what do you think (?:of|about)|is it easy to|"
    r"whats it like to|what's it like to|should we)\b", re.I)

SERVICES_POOL = (
    "A catalogue turns over every month with the rights, so I can't hold the list: "
    "{service}'s own search settles it in seconds, and says whether the thing is included or "
    "to pay for.",
    "A catalogue turns over every month with the rights, so typing the title into {service}'s "
    "own search is what says whether it is there today - I can't see it from here, and it "
    "says whether that is a rental or part of the subscription.",
    "What is on {service} changes with the rights, month to month, so I can't check it: its "
    "own search is the one that knows, and it says whether that is a rental or part of the "
    "subscription.",
)
JOURNEY_POOL = (
    "No live {mode} times from me, sorry: they are re-run all day and cancellations land "
    "late, which is why a journey planner has today's and I can't - where are you starting "
    "from, and when do you need to be there?",
    "No live {mode} times from me, sorry - they are re-run all morning and cancellations land "
    "later still, so a journey planner has the real ones and I can't: tell me the "
    "two ends and the time you have to be there and I'll help you plan around it.",
)
ROUTE_ENDS_POOL = (
    "On {start} to {end} the hour you set off decides it more than the miles do, and the bit at "
    "each end counts as much as the road between - I can't see the times or the traffic from "
    "here, sorry. A journey planner does it door to door, parking or platform included, and the "
    "one thing worth settling before you look is the time you have to be there.",
    "What settles {start} to {end} is the hour more than the distance: the peak is where it goes "
    "wrong, and the queue at both ends counts as much as the road between them, so the same pair is "
    "two different journeys at eight and at eleven. I can't see the day's times or the traffic from "
    "here, so a planner is the one that gives both ends door to door - when do you need to be "
    "there?",
    "Where in each place you start and finish settles {start} to {end} more than the route between, "
    "so fix the door first and let a planner work back from the hour you have to be there. The "
    "times are the planner's, not mine, sorry.",
)
_THE_ENDS = re.compile(r"\bto\s+(?P<end>.+?)\s+from\s+(?P<start>.+?)\s*[?.!,]*\s*$", re.I)
_THE_ENDS_REVERSED = re.compile(
    r"\bfrom\s+(?P<start>.+?)\s+to\s+(?P<end>.+?)\s*[?.!,]*\s*$", re.I)
_NOT_THE_PLACE = frozenset((
    "the", "a", "an", "on", "at", "in", "by", "for", "about", "and", "or", "but", "tomorrow",
    "today", "tonight", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday",
    "sunday", "next", "this", "please", "thanks", "quickest", "fastest", "best", "cheapest",
    "easiest", "way", "route", "time", "times",
))

def _the_route_ends(said):
    for pattern in (_THE_ENDS, _THE_ENDS_REVERSED):
        found = pattern.search(said)
        if not found:
            continue
        end = _a_place_name(found.group("end"))
        start = _a_place_name(found.group("start"))
        if end and start and end.lower() != start.lower():
            return start, end
    return None

_A_QUALIFIER_AFTER_THE_PLACE = re.compile(
    r"\s+(?P<word>by|via|with|in|on|upon|at|for|then|please|thanks|today|tomorrow|tonight|now|"
    r"early|late|weekdays|this|next|around)\b", re.I)
_A_NAME_PART = frozenset((
    "trent", "thames", "tyne", "avon", "wye", "humber", "sea", "furness", "ashfield", "arden",
    "lyme", "wolds", "moss", "ribble", "derwent", "don", "aire", "clyde", "ness", "stour",
))

def _without_a_qualifier(run):
    text = str(run or "").strip(" .?,'")
    for found in _A_QUALIFIER_AFTER_THE_PLACE.finditer(text):
        if found.group("word").lower() in ("in", "on", "upon"):
            rest = text[found.end():].split()
            if rest and rest[0].strip(".,").lower() in _A_NAME_PART:
                continue
        return text[:found.start()]
    return text

def _a_place_name(run):
    words = [word for word in _without_a_qualifier(run).split() if word]
    while words and words[-1] in _NOT_THE_PLACE:
        words.pop()
    while words and words[0] in ("the", "a", "an", "to", "from", "get", "my", "our"):
        words.pop(0)
    if not words or len(words) > 4 or any(word in ("here", "there") for word in words):
        return ""
    return " ".join(words)

ROUTE_POOL = (
    "No timetables from me, sorry: they are re-cut every few months and the day's works "
    "change them, so I can't see today's - a journey planner has the options door to door: "
    "where from, and when do you need to be there?",
    "No timetables from me, sorry - they are re-cut every few months, so the planner is the "
    "one that knows the real times between two places, and I can't: tell me the two ends and "
    "the day and I'll help you pick.",
)
PICK_POOL = (
    "Reviews beat a guess from me on the {thing} near you, which I have never been to: a map "
    "app's, sorted by what you need, is the honest way - say what matters and I'll help you "
    "narrow it down.",
    "Reviews from people who have been beat my guess on the {thing} near you, since I have never "
    "been to any of them: sort a map app's by what you need, and the count matters more than the "
    "score.",
)
SHOP_POOL = (
    "Stock, prices and delivery change by the hour and they are {shop}'s own to know, so I "
    "can't see them: its site has them worked out for your postcode, and the checkout tells "
    "you before you pay.",
    "Stock, prices and delivery are {shop}'s own to know and they change by the hour, so "
    "there is no window on them from here: its site has the answer, and the checkout tells "
    "you before you pay.",
)
ABROAD_POOL = (
    "What paperwork you need depends on your passport and what you would be doing there, so I "
    "can't tell you which one applies: gov.uk's living abroad guidance and the country's own "
    "government site are the two that count.",
    "It depends on your nationality and your plans, so the official pages are the ones to "
    "read: gov.uk's living abroad guidance, then the destination's own government site.",
)
WEATHER_POOL = (
    "A forecast is worked out for a postcode and re-run through the day, so I can't hold "
    "today's: a weather app has it for yours, hour by hour, and the week ahead when you are "
    "planning.",
    "A forecast is re-run for a postcode through the day, so there is no live weather from "
    "me: a forecast app or the national weather site has what is actually coming where you "
    "are.",
)
A_SKY_ASK = re.compile(
    r"\b(?:will|would|is|are|does|do|should|might|shall|can|could)\s+(?:it|we|they)\s+"
    r"(?:(?:going\s+to|gonna|meant\s+to|likely\s+to|supposed\s+to)\s+)?"
    r"(?:be\s+|get\s+|stay\s+|turn\s+)?"
    r"(?:raining|rainy|rain|snowing|snowy|snow|frost|frosty|freezing|freeze|thaw\w*|icy|ice|"
    r"hail|hailing|sleet|foggy|fog|misty|mist|windy|gusty|gusts|thunder|stormy|storm|sunny|"
    r"sunshine|cloudy|drizzle|drizzling|showers?|humid|muggy|warm|cold|hot|chilly|mild)\b"
    r"|\b(?:is|will|are)\s+there\s+(?:a\s+|an\s+|any\s+|much\s+)?"
    r"(?:frost|ice|snow|rain|hail|sleet|fog|mist|wind|showers?|sun|thunder|storm)\b"
    r"|\b(?:is|are|will)\s+there\s+(?:going\s+to\s+be|gonna\s+be|likely\s+to\s+be|be)\s+"
    r"(?:a\s+|an\s+|any\s+|much\s+)?"
    r"(?:frost|ice|snow|rain|hail|sleet|fog|mist|wind|showers?|sun|thunder|storms?|"
    r"heat|heatwaves?)\b"
    r"|\b(?:any|much)\s+(?:chance|risk|sign)\s+of\s+(?:a\s+|any\s+)?"
    r"(?:frost|ice|snow|rain|sleet|hail|fog|wind|thunder|showers?)\b"
    r"|\b(?:are|is|will)\s+we\s+(?:due|in\s+for)\s+(?:a\s+|any\s+|some\s+)?"
    r"(?:frost|ice|snow|rain|sleet|hail|fog|wind|thunder|showers?|storm|sun)\b", re.I)
A_SETTING = re.compile(
    r"\b(?:oven|grill|hob|fridge|freezer|microwave|kettle|boiler|radiator|cooker|washing "
    r"machine|tumble dryer|dishwasher|iron|shower|bath|sauna|engine|car|van|room|bedroom|"
    r"house|flat|dough|batter|sourdough)\b", re.I)
COUNCIL_POOL = (
    "The rules differ from one council to the next and change with the year, so I would not "
    "guess at yours: its own site has the rule and the form, and the phone line will tell you "
    "which applies to you.",
    "It depends on where you live and no two councils do it the same, so I can't see your "
    "council's rules from here: its own site is the one that decides it, and it has the form.",
)

CHOICE_POOL = (
    "Decide it on the one thing it must do well for you and compare only on that; the rest of "
    "the difference rarely matters. What must it do well?",
    "What settles these is fit rather than quality, so name the job it has to do and the limit you "
    "cannot go past - money, space or time. Which of those is tighter?",
    "When two are close, what separates them is how they are in use rather than on paper. What "
    "will you use it for most?",
)
SHORTLIST_POOL = (
    "A shortlist needs the thing you are starting from: what you are choosing between, and the one "
    "limit you cannot go past. Give me those two and I will put three or four in order.",
    "I can narrow it once I know what is on the table and what would make one of them useless to "
    "you. What is on the table?",
    "The useful part is what rules one out - money, timing, effort, or a line you will not cross. "
    "Tell me that and what you are choosing from.",
)

FORM_FROM_POOL = (
    "The form comes from the organisation that wants it, and their own site has it under the name "
    "of the thing you are applying for. Their contact page will post one if it is not there. "
    "Which organisation is it?",
    "Start from the letter or page that asked you: it names the office, and that office's site has "
    "the form to download or to fill in online. Their number can post one out. Do you still have "
    "it?",
)
FORM_TO_POOL = (
    "It goes to the address printed on the form itself - not to a general office - and a photo of "
    "it before it goes is what settles a dispute later. Which one is it?",
    "The letter that came with it names the office and the address to return it to; if it is "
    "missing, their contact page has one and a ring will confirm which. Do you have the letter?",
)

def _said(text):
    return str(text or "").lower()


def _the_line_before(memory):
    if not isinstance(memory, dict):
        return ""
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    said = [str(turn.get("user") or "").lower() for turn in turns[-3:]]
    return " ".join(said)


def _the_answers_before(memory, count=4):
    if not isinstance(memory, dict):
        return []
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    found = [str(turn.get("bot") or "").strip() for turn in turns[-count:]]
    return [line for line in reversed(found) if line]


def _the_checks_in(answer):
    found = []
    for sentence in re.split(r"(?<=[.!?])\s+", str(answer or "")):
        sentence = sentence.strip().strip("\"'\u201c\u201d").strip()
        if not sentence or len(sentence) > 320:
            continue
        if NOT_A_CHECK_SENTENCE.search(sentence):
            continue
        if A_CHECK_SENTENCE.search(sentence):
            found.append(sentence)
    for sentence in found:
        if A_CONDITION.search(sentence):
            return sentence
    return found[0] if found else ""


def _about_a_check(said, understood, memory):
    if WANTS_A_CHECK.search(said) is None or CHECK_OF_SOMETHING_ELSE.search(said):
        return None
    for answer in _the_answers_before(memory):
        checks = _the_checks_in(answer)
        if not checks:
            continue
        if checks[-1] not in ".!?":
            checks += "."
        return pick(CHECKS_POOL, understood or {}, said).replace("{checks}", checks)
    return None


def _named_service(said):
    best = ""
    for word, shown in SERVICES:
        if len(word) > len(best) and re.search(r"\b" + re.escape(word) + r"\b", said):
            best, chosen = word, shown
    return (best, chosen) if best else ("", "")


def _about_a_service(said, understood):
    word, service = _named_service(said)
    if not word or NOT_AVAILABILITY.search(said):
        return None
    platform = re.compile(
        r"\b(?:on|from|at|via|in)\s+(?:the\s+)?" + re.escape(word) + r"\b|"
        r"\b" + re.escape(word) + r"(?:'s|s')\b|"
        r"\b" + re.escape(word) + r"\s+(?:has|have|got|shows|show|streams|stream|adds)\b|"
        r"\b(?:does|do|did|is|are|has|have)\s+(?:the\s+)?" + re.escape(word) + r"\b", re.I)
    if not platform.search(said):
        return None
    if not re.search(r"\b(?:is|are|was|were|isnt|arent|any|anything|do|does|did|can|could|where|"
                     r"how)\b", said, re.I):
        return None
    return pick(SERVICES_POOL, understood or {}, said).replace("{service}", service)


def _about_a_shop(said):
    best = ""
    for word, shown in SHOPS:
        frame = re.search(
            r"(?:\b(?:at|in|from|to|does|do|did|is|are|asda's|with)\s+(?:the\s+)?"
            + re.escape(word) + r"\b)|(?:\b" + re.escape(word) + r"(?:'s|s')\b)", said)
        if frame and len(word) > len(best):
            best, chosen = word, shown
    if not best or not SHOP_ASK.search(said):
        return ""
    return chosen


def _the_mode_named(mode):
    single = (TRAVEL.get((mode or "").lower()) or ("", ""))[0]
    return single or mode


def _about_a_journey(said):
    if GET_FROM_TO.search(said) and not NOT_A_DESTINATION.search(said) and not any(
            re.search(r"\b" + re.escape(word) + r"\b", said) for word in TRAVEL):
        return "route"
    for word, (single, plural) in TRAVEL.items():
        noun = re.search(
            r"\b(?:the|a|an|my|your|our|his|her|their|this|that|these|those|last|next|first|any|"
            r"every|no|by|take the|catch the|get the)\s+" + re.escape(word) + r"\b", said)
        if not noun:
            continue
        if NOT_A_JOURNEY.search(said) or not WANTS_A_TIME.search(said):
            return None
        if word in ("tube", "metro"):
            mode = "Tube"
        else:
            mode = single
        return mode
    return None


ONLY_A_SUBJECT = re.compile(
    r"^(?:and|but|ok|okay|so|also)\s+what\s+about\b|^what\s+about\b|"
    r"^(?:and|but|also)\s+(?:the|my|your|a|an|those|these|that)\b", re.I)
HAS_A_VERB = re.compile(
    r"\b(?:is|are|was|were|has|have|had|does|do|did|can|could|will|would|should|hurts?|feels?|"
    r"seems?|goes|went|keeps?|works?|tastes?|smells?)\b", re.I)
A_QUESTION_OF_ITS_OWN = re.compile(
    r"[?,]\s*(?:is|are|was|were|does|do|did|can|could|will|would|should|how|why|when|where|what|"
    r"who|which)\b|\b(?:is|are|does|do|did|can|could|will|would|should)\s+"
    r"(?:it|that|they|this|i|we|you|he|she)\b", re.I)
A_FEW_WORDS = 5
POINTING_WORDS = frozenset((
    "the", "a", "an", "any", "some", "my", "your", "our", "their", "its", "his", "her", "these",
    "those", "that", "this", "near", "nearby", "here", "there", "around", "round", "about", "in",
    "on", "at", "to", "for", "like", "instead", "then", "too", "and", "or", "please", "though",
))
SUBJECT_KINDS = (
    ("council", re.compile(
        r"\b(?:bins?|rubbish|recycling|refuse|potholes?|librar(?:y|ies)|leisure cent(?:re|er)|"
        r"bulky waste|council tax|parking permits?|green waste|fly ?tipping|grass cutting|"
        r"school places|school catchments?|catchment areas?|catchments?|admissions|schools?)\b",
        re.I)),
    ("map", re.compile(
        r"\b(?:food|restaurants?|pubs?|cafes?|coffee shops?|takeaways?|take-aways?|beaches|walks|"
        r"things to do|days? out|markets?|parks?|chippy|chip shops?)\b", re.I)),
    ("journey", re.compile(
        r"\b(?:trains?|buses|coach|trams?|ferr(?:y|ies)|the drive|traffic)\b", re.I)),
)
_SUBJECT_LABEL = {
    "food": "restaurants", "restaurant": "restaurants", "restaurants": "restaurants",
    "pub": "pubs", "pubs": "pubs", "cafe": "cafes", "cafes": "cafes", "coffee shop": "cafes",
    "coffee shops": "cafes", "takeaway": "takeaways", "takeaways": "takeaways",
    "take-away": "takeaways", "take-aways": "takeaways", "beach": "beaches",
    "beaches": "beaches", "walk": "walks", "walks": "walks", "thing to do": "things to do",
    "things to do": "things to do", "day out": "days out", "days out": "days out",
    "market": "markets", "markets": "markets", "park": "parks", "parks": "parks",
    "chippy": "chip shops",
    "chip shop": "chip shops", "chip shops": "chip shops",
}
_SUBJECT_MODE = {"trains": "train", "buses": "bus", "trams": "tram", "ferries": "ferry",
                 "coach": "coach", "the drive": "travel", "traffic": "travel"}


def _a_country_not_home(text):
    for name in NOT_HOME_COUNTRIES:
        if re.search(r"\b" + re.escape(name) + r"\b", text):
            return name
    return ""


def _about_the_subject_named(said, understood, before=""):
    lead = ONLY_A_SUBJECT.match(said)
    if not lead:
        return None
    rest = said[lead.end():].strip(" ?.!,")
    if not rest or len(rest.split()) > A_FEW_WORDS or A_QUESTION_OF_ITS_OWN.search(said):
        return None
    if said[lead.start():lead.end()].strip().startswith(("and", "but", "also")) and \
            not re.search(r"what about", said[:lead.end()], re.I):
        if HAS_A_VERB.search(said):
            return None
    words_in_line = [word.strip("?,.!'") for word in rest.split()]
    for kind, words in SUBJECT_KINDS:
        named = words.search(rest)
        if not named:
            continue
        left = list(words_in_line)
        for word in named.group(0).lower().split():
            if word in left:
                left.remove(word)
        if [word for word in left if word and word not in POINTING_WORDS]:
            continue
        if kind == "council":
            if (ABROAD.search(before) or _a_country_not_home(before)
                    or _a_country_not_home(said)):
                return None
            return pick(COUNCIL_POOL, understood or {}, said)
        if kind == "journey":
            word = named.group(0).lower()
            return pick(JOURNEY_POOL, understood or {}, said).replace(
                "{mode}", _the_mode_named(_SUBJECT_MODE.get(word, word)))
        thing = _SUBJECT_LABEL.get(named.group(0).lower())
        if not thing:
            return None
        if not (A_PLACE.search(rest) or re.search(r"\b(?:there|here|nearby|local)\b", rest)
                or A_PLACE.search(before) or re.search(r"\b(?:there|here|nearby|local)\b", before)):
            return None
        return pick(PICK_POOL, understood or {}, said).replace("{thing}", thing)
    return None


def _about_a_pick(said, before=""):
    if not A_PLACE.search(said) and not A_PLACE.search(before):
        return None
    for words, thing in PICKS:
        for word in words:
            for match in re.finditer(r"\b" + re.escape(word) + r"\b", said):
                blocked = PICK_NOT.get(words[0])
                if blocked is not None and blocked.search(said):
                    break
                before = said[max(0, match.start() - 26):match.start()]
                if re.search(r"\b(?:in|near|around|round|at|by|beside|on|from|to)\s+(?:the\s+)?$",
                             before):
                    continue
                if not WANTS_A_PICK.search(before):
                    continue
                return thing
    return None


def _the_home_town(memory):
    if not isinstance(memory, dict):
        return ()
    user = memory.get("user")
    if not isinstance(user, dict) or not user.get("home"):
        return ()
    plans = user.get("plans")
    if isinstance(plans, str):
        plans = (plans,)
    if isinstance(plans, (list, tuple)):
        if any(GOING_AWAY.search(str(plan)) or MOVING.search(str(plan)) for plan in plans):
            return ()
    found = []
    for key in ("city", "town", "village", "hometown", "home_city"):
        value = user.get(key)
        if isinstance(value, str):
            found.append(value.strip().lower())
    return tuple(word for word in found if word and (word in HOME_NATIONS or word not in COUNTRIES))


def _the_lines_of_this_question(said, memory):
    if not isinstance(memory, dict):
        return [said]
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    earlier = [str(turn.get("user") or "").lower() for turn in turns[-3:]]
    return earlier + [said]


def _the_move_was_to_their_own_town(said, memory):
    places = _the_home_town(memory)
    if not places:
        return False
    for line in reversed(_the_lines_of_this_question(said, memory)):
        move = MOVING.search(line)
        if move:
            destination = line[move.end():move.end() + 30]
            for place in places:
                if re.search(r"(?:^|[^a-z])" + re.escape(place) + r"(?:[^a-z]|$)", destination):
                    return True
            return False
        if GOING_AWAY.search(line):
            return False
    return False


def _a_day_out(said, before=""):
    if not said or not WANTS_A_DAY_OUT.search(said) or DAY_OUT_NOT.search(said):
        return False
    if ASKS_WHAT_TO_DO.search(said) and A_THING_IN_HAND.search(said):
        return False
    if A_PLACE.search(said) and not NOT_A_DAY_OUT_PLACE.search(said):
        return True
    if not (A_PLACE_THERE.search(said) or A_BARE_DAY_OUT.search(said)):
        return False
    return bool(A_TRIP_BEFORE.search(before) and not NOT_A_DAY_OUT_PLACE.search(before))


def _about_the_rules(said, understood, before="", memory=None):
    if not WANTS_THE_RULES.search(said):
        return None
    both = said + " " + before
    strong = re.search(r"\b(?:abroad|overseas|emigrat\w*|expat\w*|visa|residency|passport for|"
                       r"work permit|right to (?:live|work)|country)\b", said)
    if (ABROAD.search(both) and (strong or _a_named_country_in(both))
            and not _the_move_was_to_their_own_town(said, memory)
            and not NOT_THE_PAPERWORK.search(said)):
        if (strong or not A_THING_NOT_A_PLACE.search(said)) and not (
                MOVING_HOUSE.search(both) and not re.search(
                    r"\b(?:abroad|overseas|country)\b", both)):
            return pick(ABROAD_POOL, understood or {}, said)
    if COUNCIL_WORD.search(said) or PARKING_RULE.search(said):
        return pick(COUNCIL_POOL, understood or {}, said)
    return None


WANTS_A_CHOICE = re.compile(
    r"\b(?:which|what)\s+(?:is|s|'s|would be|will be)\s+(?:the\s+)?(?:better|best|cheaper|"
    r"stronger|safer|easier|quicker|healthier|nicer)\b"
    r"|\bwhich (?:one )?(?:should|would|do) i (?:get|buy|use|go for|pick|choose|have)\b"
    r"|\b(?:is|are)\s+[a-z][a-z' -]{0,24}?\s+or\s+[a-z][a-z' -]{0,24}?\s+"
    r"(?:better|best|worth it|the one)\b"
    r"|\bwhat would you (?:go for|pick|choose|get)\b"
    r"|\bis it better to\b", re.I)
NOT_A_CHOICE = re.compile(
    r"\b(?:for a|for my|for the)\s+(?:burn|cut|rash|cough|cold|headache|baby|child|dog|cat)\b",
    re.I)
WANTS_A_SHORTLIST = re.compile(
    r"\b(?:short ?list|a list of|(?:a few|some|a couple of|three|two) (?:options|ideas|"
    r"suggestions|choices|picks)|options (?:for|on)|what are my options|what are the options|"
    r"(?:give|gimme|send) me (?:a few|some|three|two|a couple)|(?:suggest|recommend) "
    r"(?:a few|some|three|two))\b", re.I)
NOT_A_SHORTLIST = re.compile(
    r"\b(?:shopping list|ingredients list|list of ingredients|to do list|todo list|checklist|"
    r"waiting list|price list|job list|shortlisted|list of names)\b", re.I)
GET_A_FORM = re.compile(
    r"\b(?:get|getting|find|download|print|print off|obtain|ask for|request)\b[^?.]{0,25}"
    r"\bforms?\b", re.I)
SEND_A_FORM = re.compile(
    r"\b(?:where|who|what address|which office|which address|how do i (?:send|return|post))\b"
    r"[^?.]{0,40}\b(?:send|sending|post|return|returning|hand|hand in|submit|give)"
    r"[^?.]{0,25}\bforms?\b"
    r"|\b(?:where|who)\b[^?.]{0,40}\bforms?\b[^?.]{0,25}\b(?:go|goes|going|back)\b", re.I)
NOT_A_FORM = re.compile(
    r"\bform of (?:words|government|address|money|id|identification)\b|\b(?:in|on) (?:good |top )?"
    r"form\b|\bform an?\b|\bform (?:a|an)\b", re.I)


def _a_form(said, understood):
    if NOT_A_FORM.search(said):
        return None
    if SEND_A_FORM.search(said):
        return pick(FORM_TO_POOL, understood or {}, said)
    if GET_A_FORM.search(said):
        return pick(FORM_FROM_POOL, understood or {}, said)
    return None


def _a_choice(said, understood):
    if not WANTS_A_CHOICE.search(said) or NOT_A_CHOICE.search(said):
        return None
    return pick(CHOICE_POOL, understood or {}, said)


def _a_shortlist(said, understood):
    if not WANTS_A_SHORTLIST.search(said) or NOT_A_SHORTLIST.search(said):
        return None
    return pick(SHORTLIST_POOL, understood or {}, said)


def _about_the_sky(said, understood):
    if not A_SKY_ASK.search(said):
        return None
    if A_SETTING.search(said):
        return None
    return pick(WEATHER_POOL, understood or {}, said)


WANTS_A_CHECK = re.compile(
    r"\b(?:what|which|anything|something)\b[^?.!]{0,26}\b(?:should|shall|do|to|need to|must|"
    r"can|could)\b[^?.!]{0,24}\b(?:check|checking|look for|look at|look over|look out for|"
    r"watch out for|watch for|ask|be careful|be wary)\b|"
    r"\bwhat to (?:check|look for|look at|ask)\b|"
    r"\banything\b[^?.!]{0,26}\b(?:be careful|be wary|to watch out|to look out)\b|"
    r"\b(?:what|anything)\b[^?.!]{0,24}\bto be careful (?:of|about)\b", re.I)
CHECK_OF_SOMETHING_ELSE = re.compile(
    r"\b(?:on|about|for|in|with)\s+(?:a|an|the|my|your|his|her|their|our)\b", re.I)
A_CHECK_SENTENCE = re.compile(
    r"\bfine if\b|\bworth (?:checking|looking|a)\b|\bmatters?\b|\bwhat (?:settles|decides)\b|"
    r"\bchecks?\b|\bchecking\b|\blook (?:for|at)\b|\bwatch (?:out )?for\b|\bsigns? of\b",
    re.I)
NOT_A_CHECK_SENTENCE = re.compile(
    r"\?\s*$|\b(?:search online|look it up|not sure about that|tell me more)\b|"
    r"\b(?:999|112|111|a&e|ambulance|hospital|nhs|gp|doctor|pharmacist|midwife|vet|"
    r"urgent|emergency|straight away|right away)\b", re.I)
A_CONDITION = re.compile(r"\b(?:fine )?if (?:the|it|there|they|you|your|its)\b", re.I)
CHECKS_POOL = (
    "{checks} That is the list to go through, and I can't see it from here - which of them can "
    "you try yourself?",
    "{checks} Those are still the things that decide it, so work through them first and tell me "
    "what you find; I can only go on what you say about it.",
    "{checks} Nothing to add to that: those are what goes wrong, in the order I would check "
    "them. Which of them are you least sure about?",
)


def the_checks_already_named(text, memory=None):
    said = _said(text)
    if not said.strip():
        return None
    read = {}
    if isinstance(memory, dict):
        candidate = memory.get("understood")
        if isinstance(candidate, dict):
            read = candidate
    return _about_a_check(said, read, memory)


def answer_for(text, memory=None):
    said = _said(text)
    if not said.strip():
        return None
    read = {}
    if isinstance(memory, dict):
        candidate = memory.get("understood")
        if isinstance(candidate, dict):
            read = candidate
    service = _about_a_service(said, read)
    if service:
        return service
    sky = _about_the_sky(said, read)
    if sky:
        return sky
    mode = _about_a_journey(said)
    if mode == "route":
        ends = _the_route_ends(said)
        if ends:
            return (pick(ROUTE_ENDS_POOL, read, said)
                    .replace("{start}", ends[0])
                    .replace("{end}", ends[1]))
        return pick(ROUTE_POOL, read, said)
    if mode:
        return pick(JOURNEY_POOL, read, said).replace("{mode}", _the_mode_named(mode))
    shop = _about_a_shop(said)
    if shop:
        return pick(SHOP_POOL, read, said).replace("{shop}", shop)
    before = _the_line_before(memory)
    time_of_day = _a_time_of_day(said)
    if time_of_day:
        return time_of_day
    if _a_day_out(said, before):
        return pick(THINGS_TO_DO_POOL, read, said)
    thing = _about_a_pick(said, before)
    if thing:
        return pick(PICK_POOL, read, said).replace("{thing}", thing)
    subject = _about_the_subject_named(said, read, before)
    if subject:
        return subject
    checks = _about_a_check(said, read, memory)
    if checks:
        return checks
    rules = _about_the_rules(said, read, before, memory)
    if rules:
        return rules
    return _a_choice(said, read) or _a_shortlist(said, read) or _a_form(said, read)
