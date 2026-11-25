import re

from . import pick

HOURS = (
    "Opening hours are set by each branch rather than by the chain, and they shift at bank "
    "holidays and at short notice. The branch's own page or its map listing has today's - that's "
    "the bit that catches people out.",
    "A branch keeps its own hours and they move for holidays, a delivery day or a refit, so "
    "nothing said from here would be right today. A map app's listing for that branch is the "
    "quickest check, and a phone call settles it.",
    "Hours like that are local and they change: bank holidays, stock takes, a summer timetable. "
    "Ring the place or look at its map listing - both are updated when the hours move.",
)
A_PLACE = frozenset("""
    shop shops store stores supermarket tesco asda sainsburys sainsbury aldi lidl morrisons
    coop co-op iceland waitrose branch bank banks building society library libraries tip dump
    recycling pool lido leisure gym market stall cafe caff cafe restaurant chippy chippies
    takeaway takeaway kebab chip pizza pub pubs bar pharmacy chemist chemists surgery gp
    doctors dentist dental hospital garage showroom museum gallery gallery bowling cinema
    theatre softplay church chapel club hairdresser hairdressers barber salon vets vet
    merchants warehouse centre center office reception
    beach beaches seafront promenade park parks playground zoo farm station airport stadium
    ground services mall sauna spa rink bowling karting
""".split())
NOT_A_VENUE = frozenset("""
    window windows jar tin box boxes door doors envelope packet bottle can letter parcel
    present gift browser app file folder email shift work school run day week
""".split())
THE_PEOPLE = frozenset("""
    son daughter kid kids child children baby wife husband partner mum mom mother dad father
    boyfriend girlfriend nan grandma grandad grandson granddaughter friend boss manager
""".split())
HOURS_ASK = re.compile(
    r"\b(?:when|what\s+time[s]?)\s+(?:does|do|is|are|will|would|can|should)\b[^?]{0,44}?"
    r"\b(?:open|opens|opening|close|closes|closing|shut|shuts|shutting)\b"
    r"|\b(?:is|are)\b[^?]{0,32}?\bopen\b")
LATE_ASK = re.compile(r"\bhow\s+late\b|\bopen\s+late\b|\bopen\s+early\b"
                      r"|\bopening\s+(?:hours|times?)\b|\bclosing\s+time\b"
                      r"|\btill\s+(?:when|what\s+time)\b")
HOW_TO_OPEN = re.compile(r"\bhow\s+(?:do|to|can|should)\s+(?:i\s+)?open\b")

TRAVEL = frozenset("""
    bus buses coach coaches train trains tram trams tube underground flight flights plane
    planes ferry ferries motorway motorways a-road by-pass bypass line lines route routes
    service services replacement bus traffic junction
""".split())
STATUS = frozenset("""
    running delayed delay delays cancelled canceled cancellation cancel strike strikes closed
    shut diverted diversion disruption disruptions roadworks traffic
""".split())
TRAVEL_CLAIM = frozenset("""
    claim claims claimed refund refunds compensation compensate money owed reimburse reclaim
    pays insurance insurer hotel rebook rebooking
""".split())
ASKED = re.compile(r"\b(?:is|are|will|any|does|do)\b|"
                   r"^\s*(?:any\s+)?(?:delays?|disruptions?|traffic|roadworks?|road\s+works|"
                   r"cancellations?|strikes?|engineering\s+works)\b")
OPENS_ASKING = re.compile(r"^\s*(?:is|are|will|any|does|do|what|when|how)\b")
STORY = re.compile(r"\b(?:was|were|got|had|did|have|has|theyve|weve|ive|again|yesterday|"
                   r"this\s+morning|last\s+night)\b")
STATUS_PHRASES = ("engineering works", "called off", "on time", "bus replacement",
                  "replacement bus", "road works")
ROAD = re.compile(r"(?<![a-z0-9])[am]\s?\d{1,3}(?![a-z0-9])")
TRAVEL_LINES = (
    "Disruption can clear or spread within the hour, so only today's version is worth acting "
    "on: the operator's app or a journey planner has the next service, and for a road the "
    "traffic service names the stretch.",
    "Whether it is running today is on the operator's own system, and delays move. Their app or "
    "a journey planner shows the next one and any disruption - check it just before you set off.",
)
ON_WORDS = frozenset("""
    cinema theatre theater pictures gig gigs match game show concert festival listings listing
    play screening movie movies film films odeon vue cineworld multiplex venue
""".split())
ON_EVENT = frozenset("""
    market markets festival fete fair gig gigs match game show concert cinema theatre play
    screening event events boot sale
""".split())
ON_ASK = re.compile(r"\b(?:whats?|what\s+is)\s+on\b|\blistings?\b|\bwhats\s+on\s+at\b"
                    r"|\bis\s+(?:it|that|the\s+[a-z]+)\s+on\b|\bstill\s+on\b")
KICK_OFF = re.compile(
    r"\bwhat\s+time\s+(?:is|does|do|will)\b[^?]{0,24}?\bkick\s*-?\s*off\b"
    r"|\bwhen\s+(?:is|does)\b[^?]{0,24}?\bkick\s*-?\s*off\b"
    r"|\bwhat\s+time\s+(?:is|does)\s+the\s+(?:match|game|final)\b"
    r"|\bis\s+the\s+(?:match|game)\s+on\b")
WHAT_IS_GOOD = re.compile(
    r"\b(?:whats?|what\s+is|anything)\s+(?:good|worth\s+(?:seeing|watching|a\s+look))\b"
    r"|\bwhats?\s+(?:the\s+)?(?:new|latest)\s+(?:film|movie|play|show)\b"
    r"|\bwhat\s+(?:film|films|movie|movies|play|plays)\s+(?:is|are)\s+(?:on|showing|worth)\b"
    r"|\bwhats?\s+worth\s+(?:seeing|watching)\b")
WHATS_ON_LINES = (
    "Listings turn over every week and seats sell out quietly, so the venue's own page or a "
    "listings app is the only schedule that is right today: times, prices and what is left.",
    "That is this week's timetable, and it changes more often than a general answer could keep "
    "up with. The venue's own page or a listings app has the times, plus the number if you want "
    "to check seats.",
)
KICK_OFF_LINES = (
    "Kick-off moves for television and it can move twice, so the club's own page or a sports app "
    "is the one to trust - anything said from here could be a week out of date.",
    "The fixture list is the club's own, and televised games get moved late. Their page or a "
    "sports app has the time and says if it has been moved.",
)

BUSY = re.compile(r"\bhow\s+busy\b|\bis\s+(?:it|the\s+[a-z]+)\s+busy\b"
                  r"|\bhow\s+long\s+(?:is|are)\s+(?:the\s+)?(?:wait|queue|line)\b"
                  r"|\bwhats\s+the\s+(?:wait|queue|line)\b|\bwaiting\s+times?\b"
                  r"|\bis\s+there\s+(?:a\s+|any\s+)?(?:queue|wait|line)\b"
                  r"|\bwill\s+there\s+be\s+(?:a\s+)?(?:queue|wait|line)\b"
                  r"|\bhow\s+(?:packed|crowded|heaving|rammed)\b"
                  r"|\bwhats\s+the\s+(?:waiting\s+time|wait\s+time)\b"
                  r"|\bis\s+the\s+(?:queue|wait|line)\s+(?:long|bad|big|short|quick|slow)\b"
                  r"|\bwhen\s+(?:is|are)\s+(?:\w+\s+){0,4}"
                  r"(?:quiet|emptiest|quietest|least\s+busy)\b"
                  r"|\b(?:is|are|was|were|will|would)\s+(?:\w+\s+){1,4}"
                  r"(?:busy|packed|heaving|rammed|crowded|manic)\b")
CROWD = re.compile(
    r"\b(?:busy|packed|heaving|rammed|crowded|manic|chocka|jammed|mobbed)\b", re.I)

A_PERSON_SUBJECT = re.compile(
    r"\b(?:is|are|was|were|will|would|does|do|did)\s+(?:my\s+|our\s+|your\s+|the\s+)?"
    r"(?:he|she|they|him|her|them|you|we|i|mum|mom|mother|mam|dad|father|da|boss|manager|"
    r"sister|brother|son|daughter|wife|husband|partner|boyfriend|girlfriend|friend|mate|"
    r"nan|nana|gran|granny|grandma|grandad|grandpa|aunt|uncle|cousin|kid|kids|child|children|"
    r"baby|lad|lass|boy|girl|colleague|neighbour|neighbor|landlord|tenant|staff|team|people|"
    r"everyone|anyone|someone|nobody|somebody|bot|assistant|robot)\b")
A_WAIT_NOUN = re.compile(r"\b(?:wait|waiting|queue|queues|queuing|queueing|waiting\s+times?)\b")

BUSY_ASKS = re.compile(
    r"^\s*(?:is|are|was|were|will|would|do|does|did|can|could|should|any|how|what|whats|when"
    r"|where|which|who)\b|\?\s*$")
BUSY_LINES = (
    "A queue changes hour to hour: the weekend and school pick-up are the busy half of the week "
    "and a weekday morning the quiet one, and a wet Saturday pushes everybody indoors at once. "
    "Nobody publishes it everywhere, so one call settles today faster than anything I could "
    "guess, and their own page has a live wait if they keep one.",
    "It will be worse at the weekend and around school pick-up, and better first thing, but "
    "today's wait is only on their system. Ring them before you set off - the place itself is the "
    "only one that knows.",
    "The busy hours are much the same everywhere - late morning to mid afternoon at the weekend, "
    "and the hour after school lets out - and the weather moves the whole thing. Today's version "
    "is at the place: their own page keeps a live count where it keeps one, and one call settles "
    "the rest.",
)
BUSY_NO_PLACE = (
    "A wait is live and local, so the only figure that is right is the one at that place today: "
    "their own page keeps it where they keep one, and one call settles the rest. Waits are usually "
    "shortest first thing and longest from mid morning on. Which place is it?",
    "That changes hour to hour and place to place, so I can't put a number on it - their own page "
    "or phone has today's, and a map app's popular times shows the busy hours if you are picking "
    "when to go. First thing is usually the quiet end. Which place did you have in mind?",
)
BUSY_NO_PLACE_AND_CONTEXT = (
    "A wait is live and local, so today's figure is only at the place itself: their own page keeps "
    "it where they keep one, one call settles the rest, and first thing is usually the quiet end of "
    "the day.",
    "That one moves hour to hour and place to place, so I can't put a number on it: their own page "
    "or phone has today's, and a map app's popular times shows the busy hours if you are choosing "
    "when to go.",
)
A_PLACE_IN_A_TURN = re.compile(
    r"\b(?:beach|seafront|promenade|gym|pool|leisure\s+cent\w+|tip|dump|hospital|casualty|clinic"
    r"|surgery|pharmacy|chemist|supermarket|shop|store|market|pub|restaurant|cafe|takeaway|park"
    r"|playground|museum|gallery|zoo|library|station|airport|car\s+park|high\s+street"
    r"|town\s+cent\w+|mall|ground|stadium|theatre|cinema|venue|club|centre|sauna|spa|dentist"
    r"|bank|services|attraction|soft\s*play|ice\s+rink|bowling)\b")
A_AND_E = re.compile(
    r"\b(?:a\s*&\s*e|a\s+and\s+e|a\s*and\s*e|casualty|emergency\s+department"
    r"|emergency\s+room|urgent\s+care|walk[-\s]?in\s+cent\w+|minor\s+injuries)\b")

PRICE_ASK = re.compile(r"\bhow\s+much\s+(?:is|are|does|do|will)\b"
                       r"|\bwhats?\s+the\s+(?:price|charge|cost|fee|rate)\b")
FREE_ASK = re.compile(
    r"\bis\s+(?:the\s+|a\s+)?[a-z' -]{2,24}\s+free\b"
    r"|\bis\s+(?:entry|admission|parking)\s+free\b"
    r"|\bis\s+there\s+a\s+charge\b"
    r"|\bpay\s+to\s+(?:park|get\s+in|go\s+in|enter|visit)\b"
    r"|\bdo\s+(?:i|we)\s+have\s+to\s+pay\s+(?:to|for\s+(?:a|an|the|any|my|our))\b")
FREE_COMPOUND = frozenset("""
    gluten dairy sugar fat nut nuts wheat lactose caffeine msg toll duty tax hands care cruelty
    smoke contact peanut egg soya soya soy
""".split())
PRICE_THING = frozenset("""
    parking park bus buses train trains tube taxi cab admission entry entrance ticket tickets
    delivery postage post fee fees fare fares hire rental charge
""".split())
PRICE_LINES = (
    "Rates like that are set by whoever runs the place and they change with the season: their "
    "own site or one quick call has the figure they actually charge, and a map listing carries "
    "the number if there is no site.",
    "Admission and parking prices are set locally and move with the season, so the current one "
    "is on their website or through one call, and a map listing has the number.",
)

AVAIL = re.compile(
    r"\b(?:tickets?|seats?|tables?|rooms?|spaces?|places?|slots?|pitches?|appointments?)\s+left\b"
    r"|\b(?:are|is)\s+there\s+(?:any\s+|a\s+)?(?:tickets?|seats?|tables?|rooms?|spaces?|"
    r"pitches?)\b"
    r"|\b(?:is\s+it|are\s+they)\s+(?:fully\s+)?(?:booked\s+up|full|sold\s+out)\b"
    r"|\b(?:is|are|has|have|did|does|will)\b[^?]{0,20}?\bsold\s+out\b"
    r"|\bcan\s+(?:i|we)\s+(?:still\s+)?(?:get|book)\s+(?:a|any)\s+(?:table|seat|ticket|room"
    r"|space|pitch|slot)\b")
AVAIL_LINES = (
    "What is left is on their booking system rather than anywhere I can see, and it changes by "
    "the hour. Their booking page shows what is still free, and the box office settles a "
    "sell-out in a second.",
    "Anything still free is in their own system, sorry - it moves too fast for a general answer. "
    "Their booking page shows it, and ringing is quicker if you are on your way.",
)

LOCAL_AREA = re.compile(
    r"\b(?:my|our)\s+(?:town|village|area|county|streets?|roads?|ward|district|neighbourhood|"
    r"postcode|council|city)\b")
LOCAL_ASK = re.compile(r"\bhow\s+many\b|\bpopulation\b|\bwho\s+is\b|\bwhich\s+band\b|"
                       r"\bhow\s+do\s+i\s+find\b|\bwhat\s+is\s+the\s+population\b")
LOCAL_LINES = (
    "Figures about your own patch come from your council, and they publish them: their site has "
    "it - the box at the top takes your postcode - and one call to the main number works if the "
    "site buries it.",
    "Your council holds that and keeps it up to date. Their site has it, or one call to the main "
    "number answers it - the postcode does most of the work.",
)
TERM_DATES = re.compile(r"\bterm\s+dates?\b|\binset\s+days?\b|\bacademic\s+year\b|\bwhen\s+do\s+"
                        r"(?:the\s+)?schools?\s+(?:break|finish|start)\b")
TERM_LINES = (
    "Term dates are the school's own calendar, and the inset days are the bit a general answer "
    "always gets wrong. The school's site has both, and the council lists every school's in one "
    "place if you need to compare.",
    "The school sets its own term dates and its own inset days. Their page has both, and the "
    "council's site collects them all if you are looking at more than one school.",
)

NEARBY_AREA = re.compile(
    r"\bnear\s?(?:me|us|here)\b|\bround\s+here\b|\bnear\sby\b|\bnearby\b"
    r"|\bin\s+my\s+(?:area|town|village|city|street|road|postcode|neighbourhood)\b"
    r"|\bmy\s+(?:postcode|area|town|village)\b")
ASKS_LOCAL = re.compile(
    r"\bis\s+there\b|\bare\s+there\b|\bwhere\b|\bwheres\b|\bwhich\b|\bany\b"
    r"|\banywhere\b|\bcan\s+(?:i|we|you)\b|\bcould\s+(?:i|we|you)\b|\bdo\s+you\s+know\b"
    r"|\b(?:i|we)\s+(?:need|want|are\s+looking|am\s+looking)\b|\blooking\s+for\b"
    r"|\brecommend\b|\bfind\b|\bwhats\s+good\b|\bgood\s+(?:place|places|spot|spots)\b")
NEAREST = re.compile(r"\b(?:nearest|closest)\s+(?!to\b)[a-z]+")
NEARBY_SERVICE = frozenset("""
    pharmacy chemist cashpoint atm supermarket shop store garage launderette laundrette dentist
    doctors surgery hospital petrol gym pool park school nursery vet takeaway chippy pub cafe
    restaurant bank tip
""".split())
DELIVER = re.compile(r"\bdeliver(?:y|s|ed)?\s+(?:to|in)\b|\bdeliver\s+to\s+my\b|"
                     r"\bdo\s+(?:they|you)\s+deliver\b")
DELIVER_LINES = (
    "Delivery depends on the postcode and the day, and only the shop's own checker knows it: put "
    "your postcode in on their site and it says yes or no in a second, with the earliest slot.",
    "That depends on the postcode, which their own delivery checker holds - it takes ten seconds "
    "with your postcode in, and it shows the earliest date too.",
)
NEARBY_LINES = (
    "What is near you depends on your postcode, so a map app is the one that knows: it lists the "
    "closest in order of distance, with today's hours and a phone number for each one.",
    "A map app puts them in order of distance and carries the phone number, which is faster than "
    "any list I could give you from here.",
)

HOW_TO = re.compile(r"\bhow\s+(?:do|can|should|would)\s+(?:i|we)\b|\bhow\s+to\b|"
                    r"\bwhat\s+do\s+i\s+need\s+to\b|\bwhats\s+the\s+best\s+way\b")

OFFICIAL_ASK = re.compile(
    r"\b(?:whats|what\s+is|what\s+are)\s+the\s+(?:law|rules?|legal\s+position|regulations?)\b"
    r"|\bis\s+it\s+(?:legal|allowed|illegal)\b|\bam\s+i\s+(?:allowed|legally)\b"
    r"|\bdo\s+i\s+need\s+(?:a|an|any|to)\b"
    r"|\bhow\s+do\s+i\s+(?:get|apply|renew|replace|register|order|book)\b"
    r"|\bhow\s+do\s+i\s+(?:check|find\s+out)\s+(?:if|whether|who|what)\b")
OFFICIAL_THING = frozenset("""
    licence license permit permission registration certificate copy record records badge card
    cscs dbs crb passport visa form application skip planning consent exemption grant benefit
    number registered register renewal certificate blue disabled
""".split())
RULES_ASK = re.compile(r"\b(?:law|legal|allowed|rules?|regulations?|illegal)\b")
GAME = frozenset("""
    uno chess poker monopoly scrabble darts snooker dominoes cluedo risk rummy bingo
""".split())
ASK_STOP = frozenset("""
    what whats is are the a an it i we you do does to of on for in my our and if can could
    there be this that rule rules law legal allowed illegal regulations regulation about
""".split())
OFFICIAL_LINES = (
    "Anything with a form behind it is set by the office that issues it, and the fee and the "
    "paperwork change with the year. Their official page - GOV.UK for the national ones, your "
    "council for anything local - names what to send, what it costs and how long it takes.",
    "The form, the fee and the waiting time all come from the office that issues it, and they "
    "change. Their own page is the one to act on, and it says who to ring if your case does not "
    "fit the standard one.",
    "The rules differ by council and by country, so the version that counts is on the issuing "
    "office's own page: GOV.UK has the national forms, and the page names who to ring about the "
    "rest.",
)
RULES_LINES = (
    "Rules like that are set locally and the byelaws differ from one council to the next: your "
    "council's site has them, plus the permit if one is needed, and their phone line answers the "
    "odd case.",
    "The rules differ by council and by country, so the local version is the only one worth "
    "acting on: the council's site has it, and GOV.UK has the national half.",
)


PET = frozenset("""
    cat cats dog dogs kitten puppy pet pets hamster rabbit budgie parrot
""".split())
DIED = frozenset("""
    died dead death passing euthanised put down cremated
""".split())


A_REPORT = re.compile(
    r"\b(?:every\s+(?:single\s+)?(?:day|week|morning|evening|night|time)"
    r"|all\s+(?:week|weeks|month|months|year|day|days|morning|night|the\s+time)"
    r"|for\s+(?:weeks|months|days|ages|hours)"
    r"|since\s+(?:january|february|march|april|may|june|july|august|september|october|november"
    r"|december|last|monday|tuesday|wednesday|thursday|friday|saturday|sunday|easter|christmas|then)"
    r"|each\s+(?:day|week|morning)"
    r"|the\s+whole\s+(?:week|month|day)"
    r"|ruined|ruins|wrecked|wrecks|chaos|nightmare|fed\s+up|sick\s+of|so\s+tired|held\s+me\s+up"
    r"|made\s+me\s+late|cost\s+me|missed\s+my)\b")


def reads_as_a_report(text):
    said = " ".join(str(text or "").lower().split())
    return bool(said) and not said.endswith("?") and bool(A_REPORT.search(said))


def _words(clean):
    return re.findall(r"[a-z0-9'-]+", clean)


def reads_as_crowd(clean):
    text = " ".join(str(clean or "").lower().split())
    return bool(text) and bool(CROWD.search(text)) and bool(BUSY_ASKS.search(text))


def reads_as_busy(clean):
    text = " ".join(str(clean or "").lower().split())
    return bool(text) and bool(BUSY.search(text)) and bool(BUSY_ASKS.search(text))


def _a_place_a_line_back(memory):
    for turn in reversed(((memory or {}).get("turns") or [])[-3:]):
        if not isinstance(turn, dict):
            continue
        for side in ("user", "bot"):
            said = " ".join(str(turn.get(side) or "").lower().split())
            if said and A_PLACE_IN_A_TURN.search(said):
                return said
    return ""


def pool(clean, memory=None):
    text = " ".join(str(clean or "").lower().split())
    if not text:
        return None
    said = set(_words(text))
    if reads_as_a_report(text):
        return None
    if BUSY.search(text) and BUSY_ASKS.search(text):
        if A_PERSON_SUBJECT.search(text):
            return None
        if said & A_PLACE or A_PLACE_IN_A_TURN.search(text) or A_AND_E.search(text):
            return BUSY_LINES
        if _a_place_a_line_back(memory):
            return BUSY_LINES
        if not A_WAIT_NOUN.search(text):
            return None
        if (memory or {}).get("turns"):
            return BUSY_NO_PLACE_AND_CONTEXT
        return BUSY_NO_PLACE
    if ((HOURS_ASK.search(text) and (said & A_PLACE or "it" in said))
            or (LATE_ASK.search(text) and said & A_PLACE)):
        if not HOW_TO_OPEN.search(text) and not said & NOT_A_VENUE and not said & THE_PEOPLE:
            return HOURS
    if KICK_OFF.search(text):
        return KICK_OFF_LINES
    if said & (ON_WORDS | ON_EVENT) and ON_ASK.search(text):
        return WHATS_ON_LINES
    if said & ON_WORDS and WHAT_IS_GOOD.search(text):
        return WHATS_ON_LINES
    if ((said & TRAVEL or ROAD.search(text)) and not HOW_TO.search(text)
            and not said & TRAVEL_CLAIM and not THEIR_OWN_ONLINE.search(text)
            and ASKED.search(text)
            and not (STORY.search(text) and not OPENS_ASKING.search(text))
            and (said & STATUS or any(phrase in text for phrase in STATUS_PHRASES))):
        return TRAVEL_LINES
    if (PRICE_ASK.search(text) and said & PRICE_THING) or (
            FREE_ASK.search(text) and not said & FREE_COMPOUND):
        return PRICE_LINES
    if AVAIL.search(text):
        return AVAIL_LINES
    if LOCAL_AREA.search(text) and LOCAL_ASK.search(text):
        return LOCAL_LINES
    if DELIVER.search(text):
        return DELIVER_LINES
    if TERM_DATES.search(text):
        return TERM_LINES
    if (NEARBY_AREA.search(text) and ASKS_LOCAL.search(text)) or (
            NEAREST.search(text) and said & NEARBY_SERVICE):
        return NEARBY_LINES
    if OFFICIAL_ASK.search(text) and not (said & PET and said & DIED):
        if said & OFFICIAL_THING:
            return OFFICIAL_LINES
        if RULES_ASK.search(text) and not said & GAME and said - ASK_STOP:
            return RULES_LINES
    return None


A_STATUS_SPENT_ON = re.compile(
    r"^\s*(?:any\s+|the\s+)?(?:delays?|disruptions?|traffic|roadworks?|road\s+works|"
    r"cancellations?|strikes?|engineering\s+works)\s+"
    r"(?:on|at|near|around|by|into|outside|through)\b")


THEIR_OWN_ONLINE = re.compile(
    r"\b(?:my|our)\s+(?:site|website|web\s*page|page|shop|store|storefront|listing|listings|"
    r"blog|channel|profile|etsy|ebay|account|sales)\b")


NOT_THEIR_STATUS = re.compile(r"\b(?:my|our|order|parcel|delivery|claim|refund)\b")


def pool_over_a_receipt(clean):
    text = " ".join(str(clean or "").lower().split())
    if not text or not A_STATUS_SPENT_ON.search(text):
        return None
    if reads_as_a_report(text):
        return None
    bare = text[4:].strip() if text.startswith("the ") else text
    found = pool(bare)
    if found:
        return found
    if NOT_THEIR_STATUS.search(bare):
        return None
    return TRAVEL_LINES


A_FOLLOW_UP = re.compile(
    r"^\s*(?:is|are|will|would|how\s+(?:long|much|bad|far)|what\s+about|and\b|"
    r"does|do)\b")
A_BACK_REFERENCE = re.compile(r"\b(?:it|that|they|them|those|this|the\s+same|still)\b")


def more_about_the_journey(clean, memory):
    text = " ".join(str(clean or "").lower().split())
    if not text or not A_FOLLOW_UP.search(text) or not A_BACK_REFERENCE.search(text):
        return None
    turns = [t for t in (memory.get("turns") or []) if t.get("bot")]
    if not turns:
        return None
    last = turns[-1].get("bot") or ""
    if last in TRAVEL_LINES:
        return TRAVEL_LINES
    from . import fallback_data
    for _kind, _phrases, options in fallback_data.LIVE_KINDS:
        if last and last in options:
            return tuple(options)
    return None


A_PLACE_NAMED = re.compile(
    r"\b(?:map app|maps|google maps|the council|council'?s?|gov\.uk|\.gov\b|government"
    r"|operator'?s?|journey planner|traffic service|road agency|roads agency|national rail"
    r"|pharmac(?:y|ist)|chemist|\bgp\b|doctor'?s|surgery|the ward|nurse|vet'?s?|veterinary"
    r"|their (?:own )?(?:site|website|web page|page|app|account|office|desk|number)"
    r"|the (?:official )?(?:site|website) of|official (?:page|site)"
    r"|box office|ticket office|the office that|issuing office|passport office|dvla"
    r"|registry office|landlord|letting agent|estate agent|employer|\bhr\b|payroll"
    r"|your bank|the bank|insurer|insurance company|the airline|the hotel|the venue"
    r"|the airline'?s?|one call|give them a ring|ring them|call them|their line)\b")
HOLDS_IT = re.compile(
    r"\b(?:has|have|shows|lists|carries|publishes|updates)\b[^.]{0,30}"
    r"\b(?:number|form|fee|price|prices|hours|wait|times|schedule|status|page|listing)\b")


def says_where_to_look(reply):
    said = " ".join(str(reply or "").lower().split())
    if not said:
        return False
    return bool(A_PLACE_NAMED.search(said) or HOLDS_IT.search(said))

A_KIT = re.compile(
    r"\b(?:shed|wardrobe|bookcase|bookcases|shelves|shelving|shelf|flat\s*pack|flatpack|kit|"
    r"units?|desk|bed|bunk|trampoline|greenhouse|climbing\s+frame|table|chair|chairs|cabinet|"
    r"bbq|barbecue|swing\s*set|playhouse|sideboard|tiles?|flooring|laminate|decking|fence|"
    r"fencing|gate|sheds|curtain\s+pole|blinds?|radiator\s+cover|sofa|settee|couch|mattress|"
    r"sofa\s+bed|armchair|dining\s+table)\b")
A_FIXTURE = re.compile(
    r"\b(?:tap|taps|sink|sinks|shower|showers|toilet|loo|cistern|ballcock|bath|bathroom\s+suite|"
    r"stopcock|soil\s+pipe|waste\s+pipe)\b")
AN_APPLIANCE = re.compile(
    r"\b(?:boiler|washing\s+machine|washer|dishwasher|fridge|freezer|oven|cooker|hob|microwave|"
    r"kettle|toaster|hoover|vacuum|dryer|tumble\s+dryer|radiator|thermostat|heater|dehumidifier|"
    r"mower|lawnmower|strimmer|hedge\s+trimmer|drill|printer|laptop|phone|tablet|console|"
    r"telly|tv|television|router|doorbell|camera|battery|charger|remote)\b")
PAPERWORK = re.compile(
    r"\b(?:letter|form|invoice|bill|statement|contract|policy|insurance|quote|receipt|"
    r"reference|application|claim|tenancy|lease|mortgage|payslip|p60|p45|council\s+tax|licence|"
    r"license|passport|visa|permit|booking|confirmation|delivery|order|parcel|refund|warranty|"
    r"guarantee|tracking)\b")

A_COMMITMENT = re.compile(
    r"\b(?:gym\s+membership|phone\s+contract|mobile\s+contract|care\s+home|home\s+care|"
    r"lease\s+car|car\s+finance|direct\s+debit|times\s+share|gym|membership|contract|"
    r"subscription|tariff|tenancy|lease|timeshare|nursery|course|classes|insurance|policy|"
    r"broadband|loan|finance|hp)\b")
ASK_GET_OUT = re.compile(
    r"\bget\s+out\s+of\b|\bhow\s+(?:do|can|should)\s+(?:i|we)\s+(?:cancel|stop|end|leave|quit|"
    r"exit)\b|\bcancel\s+(?:it|my|the|this|that|our)\b|\bstop\s+paying\b|\bend\s+(?:the|my|"
    r"this|our)\b|\bgive\s+notice\b|\bopt\s+out\b|\bcome\s+out\s+of\b|\bbreak\s+(?:the|my)\b")

NOT_ABOUT_THE_CONVERSATION = re.compile(
    r"\b(?:what|which)\s+(?:was|were|did|have|had)\s+(?:i|we|you)\b|\bwhat\s+am\s+i\b|"
    r"\bdo\s+you\s+remember\b|\bwhat\s+did\s+(?:i|we|you)\s+(?:say|ask|tell)\b|"
    r"\bwhat\s+(?:i|we)\s+(?:said|asked|told)\b|\bremind\s+me\b")
NOT_A_LOOKUP_BUT_A_REQUEST = re.compile(
    r"\b(?:help\s+me|can\s+you|could\s+you|would\s+you|will\s+you|shall\s+i)\s+"
    r"(?:write|draft|word|put|phrase|text|reply|answer|compose|translate|summari[sz]e|rewrite|"
    r"shorten|tidy|check|read)\b|\bwrit(?:e|ing)\s+(?:it|that|this|him|her|them)\b|"
    r"\bdraft\s+(?:it|that|this|something)\b|"
    r"\b(?:write|reply|text|email|message|answer)\s+(?:to\s+)?(?:him|her|them|the\s+\w+)\b|"
    r"\bhow\s+(?:do|should)\s+i\s+(?:write|word|phrase|put)\b|\b(?:re)?word\s+(?:it|that|this)\b|"
    r"^make\s+(?:it|this|that|them)\b|\bmake\s+it\s+(?:more|less|a\s+bit|much)\b|"
    r"\b(?:add|drop|cut|keep)\s+(?:a|the)\s+(?:line|bit|sentence|word)\b")

NOT_ABOUT_THE_VISIT = re.compile(
    r"\bwill\s+(?:they|he|she|it)\s+need\b|\bneed\s+to\s+come\s+(?:in|inside|out|back|round)\b|"
    r"\bcome\s+(?:in|inside|out|back|round)\b|\bneed\s+access\b|\bget\s+to\s+it\b|"
    r"\bhow\s+long\s+will\s+(?:they|he|she|someone|the\s+(?:engineer|plumber|fitter|installer|"
    r"technician|electrician|man))\b|\b(?:they|he|she)\s+(?:turn\s+up|arrive)\b|"
    r"\b(?:have|get)\s+(?:it\s+|everything\s+|them\s+)?ready\b|\bready\s+(?:for|when)\s+"
    r"(?:them|him|her|someone|the\s+\w+)\b|\bwhat\s+(?:do|should)\s+i\s+(?:tell|say\s+to|show|"
    r"give|ask|bring)\b|\bwait\s+in\b|\bbe\s+(?:in|there)\s+(?:for|all)\s+(?:the\s+)?(?:day|morning|afternoon)\b")

A_PLAN_ASK = re.compile(
    r"\bwhat\s+time\s+(?:should|do|shall|would)\s+(?:i|we)\b|\bwhen\s+should\s+(?:i|we)\b|"
    r"\bshould\s+(?:i|we)\s+(?:start|begin|leave|set\s+off|get\s+up)\b|"
    r"\bhow\s+long\s+(?:before|ahead)\b|^\W*shall\s+i\b|\bshall\s+i\s+(?:also|do|just|be)\b")

A_COOKING_LINE = re.compile(
    r"\b(?:cook|cooked|cooking|roast|bake|baking|fry|frying|boil|grill|simmer|steam|poach|"
    r"marinate|season|seasoning|baste|skin|thighs?|breasts?|fillet|mince|pasta|rice|sauce|dough|"
    r"pastry|chicken|beef|pork|lamb|turkey|fish|prawn|veg|vegetables|potatoes|onion|garlic)\b")

A_READING_JUST_GIVEN = re.compile(
    r"\b(?:is|was|are)\s+(?:that|this|it|those)\s+(?:too|about\s+right|ok\b|okay\b|normal\b|"
    r"enough\b|much\b|low\b|high\b|fine\b)|\bis\s+\d[\d.,]*\s*\w*\s+(?:enough|too|ok\b|fine\b|normal\b)")

A_WHY_ASK = re.compile(
    r"\bis\s+that\s+why\b|\bwhy\s+(?:does|do|is|are|would|did|has|have|am\s+i)\b|"
    r"\bwhat\s+causes?\b|\bcould\s+that\s+be\s+(?:why|it)\b|\bis\s+that\s+(?:what|the\s+reason)\b")

A_NOW_OR_NEVER_ASK = re.compile(
    r"\b(?:now|today|tonight|tomorrow|this\s+evening|the\s+day\s+before|the\s+night\s+before|"
    r"last\s+night|overnight)\b[^.?!]{0,40}\b(?:can|could|should|shall|will)\s+(?:i|we)\b|"
    r"\b(?:can|could|should|shall)\s+(?:i|we)\b[^.?!]{0,40}\b(?:now|today|tonight|tomorrow|"
    r"overnight|the\s+day\s+before)\b")

A_DECISION_ABOUT_GOING_ON = re.compile(
    r"\bshould\s+(?:i|we)\s+(?:stop|keep|carry\s+on|carry|bother|risk|go\s+ahead|wait|"
    r"use|still|replace|fix|put\s+up\s+with)\b|"
    r"\b(?:is|was)\s+(?:it|that)\s+(?:safe|ok\b|okay\b|fine\b|alright)\s+to\s+"
    r"(?:keep|carry|use|go\s+on|carry\s+on)\b")

A_METHOD_OR_ADVICE_ASK = re.compile(
    r"\bhow\s+(?:do|can|should|would)\s+(?:i|we|you)\s+(?:take|get|put|fit|remove|undo|open|"
    r"change|replace|fix|clean|unblock|unblock|bleed|reset|wire|connect|assemble|dismantle|strip|"
    r"hang|mount|seal|glue|screw|drill|paint|cut|adjust|tighten|loosen)\b|"
    r"\bwhat\s+would\s+you\s+do\b|\bwhat\s+should\s+(?:i|we)\s+do\b|"
    r"\bwhat\s+do\s+you\s+(?:think|reckon|suggest|recommend)\b|\bany\s+(?:advice|ideas|thoughts)\b")

A_JUDGEMENT_ASK = re.compile(
    r"\bworth\b|\bvalue\b|\bany\s+good\b|\bgood\s+(?:idea|buy)\b|\bhow\s+much\b|"
    r"\bcheaper\b|\bbetter\s+buy\b|\bshould\s+(?:i|we)\s+(?:buy|get)\b|\bwaste\s+of\s+money\b")

NOT_ON_THE_PLATE = re.compile(
    r"\bservic(?:e[sd]?|ing)\b|\bhow\s+often\b|"
    r"\brinse\s+aid\b|\bsalt\b|\bdescal\w*|\badditive\b|\bsoftener\b|"
    r"\b(?:which|what)\s+filter\b|\bfilter\s+(?:does|should)\b|"
    r"\btablets?\b|\bpowder\b|\bdetergent\b|"
    r"\bhow\s+(?:do|should)\s+(?:i|we)\s+(?:use|load|set|run|fill)\b|"
    r"\bshould\s+(?:i|we)\s+(?:use|put|add|fill|run)\b")

NOT_HERE = re.compile(
    r"\b(?:pain|hurts?|ache|aching|sore|swollen|swelling|rash|lump|bleeding|blood|dose|dosage|"
    r"tablets?|pills?|medicines?|medication|prescription|symptoms?|sick|vomiting|dizzy|breath|"
    r"chest|stomach|mum|mom|dad|son|daughter|wife|husband|partner|baby|child|kids?|gran|nan)\b")

ASK_TOOLS = re.compile(
    r"\b(?:what\s+tools?|what\s+(?:do|will|would|might)\s+(?:i|we|you)\s+need|tools?\s+(?:do|will)"
    r"|what\s+do\s+i\s+need\s+(?:to|for)|what\s+will\s+i\s+need)\b")
ASK_HOW_LONG = re.compile(
    r"\bhow\s+long\s+(?:does|do|will|would|should|to|is|takes?)\b|\bhow\s+many\s+hours\b|"
    r"\bhow\s+long\s+(?:a|an|one|it|they|that)\b")
ASK_SIZE = re.compile(
    r"\bwhat\s+size\b|\bwill\s+it\s+fit\b|\bhow\s+big\b|\bwhat\s+(?:kind|sort)\s+of\s+\w+\s+"
    r"(?:do|will)\s+(?:i|we)\b|\bwhich\s+(?:one|size|model)\b")
ASK_BE_IN = re.compile(
    r"\bbe\s+in\s+for\s+it\b|\bneed\s+(?:to\s+)?be\s+(?:in|here|home)\b|\bsign\s+for\s+it\b|"
    r"\b(?:does|will)\s+(?:it|someone|they)\s+need\s+to\s+be\s+in\b|\bwaiting\s+in\b")
ASK_COVERED = re.compile(
    r"\b(?:covered|cover\s+(?:it|this|that|me)|tell\s+the\s+insurance|insurance\s+(?:about|know)|"
    r"claim\s+(?:on|for)|on\s+the\s+policy|included|comes?\s+with\s+it)\b")
ASK_EXACT = re.compile(
    r"\bwhich\s+(?:model|part|spare|size|one|type|version)\b|\bwhat\s+(?:model|number)\b|"
    r"\bpart\s+number\b|\bwhich\s+one\s+(?:do|should|will)\b")
ASK_SEND_BACK = re.compile(
    r"\bsend\s+(?:it|them|that|this|the\s+old\s+one)\s+(?:back|off|in)\b|"
    r"\bsend\s+(?:it\s+|them\s+)?(?:back|off)\b|\b(?:do|must|should|need\s+to|have\s+to)\s+"
    r"(?:i\s+)?(?:return|post|send)\b|\breturn\s+(?:it|them|the\s+old\s+one)\b")

CARRIERS = {
    ("tools", "kit"): (
        "The instruction sheet in the box lists the tools and the fixings, and says which of them "
        "you can do without",
        "The parts list that came with it names the tools it wants, and the fixings are usually "
        "in the box with them",
    ),
    ("tools", "appliance"): (
        "The installation page for your model lists what it needs, and the plate on the machine "
        "says which model yours is",
        "The maker's own page for that model names the tools and whether the fixings come with it",
    ),
    ("how_long", "kit"): (
        "The instruction sheet gives the number of hours for two people, and the maker's page "
        "usually repeats it with the same figure",
        "The maker's page for it has the build time, and the instructions break that down into "
        "what has to be done in order",
    ),
    ("how_long", "appliance"): (
        "The maker's page for your model says how long the job should take, and the plate on it "
        "tells you the model",
        "Whoever services that make will give you a time on the phone from the model number "
        "alone, which is on the plate",
    ),
    ("how_long", "paperwork"): (
        "The reference on the paperwork is what a straight answer is given against, and the office "
        "named on it is the one that holds the times",
        "Whoever issued it can say where yours has got to from the reference - and the letter or "
        "the confirmation says who that is",
    ),
    ("be_in", "kit"): (
        "The order confirmation and the tracking page say whether it needs a signature, and they "
        "are what count on the day",
        "Whoever is delivering it puts the answer on the tracking page, and the confirmation says "
        "what happens if nobody is in",
    ),
    ("size", "kit"): (
        "The maker's page for each version gives the footprint and the clearance it needs, and the "
        "size chart is the part that settles which one fits",
        "The maker's page has the dimensions for each version, so the sheet and the page together "
        "settle which one fits your space",
    ),
    ("size", "appliance"): (
        "The maker's page for your model has the dimensions, and the plate on it tells you the "
        "model",
        "The plate on it gives the model number, and the maker's page has the size for that exact "
        "one",
    ),
    ("be_in", "paperwork"): (
        "The order confirmation or the tracking page says whether it needs a signature, and that "
        "is the one that counts on the day",
        "Whoever is delivering it puts the answer on the tracking page, and the confirmation says "
        "what happens if nobody is in",
    ),
    ("covered", "paperwork"): (
        "The policy or the reference says: what is covered, what the excess is, and what they ask "
        "you to tell them, all in the same document",
        "The terms that came with it settle it, and a phone call quoting the reference gets a yes "
        "or no from the people who apply them",
    ),
    ("send_back", "paperwork"): (
        "What it wants back, in what state and by when is on the page it came with, and the "
        "reference on it is how you check they have got it",
        "Whatever came with it sets out what to return and what to keep; the office named on the "
        "paper will confirm against the reference",
    ),
    ("get_out", "commitment"): (
        "The way out is written in the terms you were given: the notice period, whether it has to "
        "be in writing, and the date it renews on - and a written notice sent to the address on "
        "that paperwork is what they have to answer",
        "It comes down to the wording you signed: how much notice it wants, whether it renews "
        "itself, and who the notice has to go to. Notice in writing, sent to the address on the "
        "paperwork, is the version that gets an answer",
    ),
    ("exact", "appliance"): (
        "The plate on it - inside the door or on the back - gives the model and the part number, "
        "and that is what the maker's page is searched by",
        "The model and serial on the plate are what any parts page wants, and they make the answer "
        "exact rather than near",
    ),
    ("first_step", "kit"): (
        "The instruction sheet in the box and the maker's page for it between them cover what it "
        "needs and what to do when it will not - and the sheet is the one that came with your "
        "copy",
        "Start with what came with it: the sheet and the parts list say what it should do and "
        "what is missing, and the maker's page for that exact one says the rest",
    ),
    ("first_step", "appliance"): (
        "The plate on it - inside the door or on the back - gives the model and the serial, and the "
        "maker's page for that model has the fault codes, the parts and who services it",
        "Whatever the question is, the model number on the plate is the way in: the maker's page "
        "for it, or the engineer on the phone, will take that and work from there",
    ),
    ("first_step", "fixture"): (
        "The part that goes on those is the cheap one - a washer, a cartridge, a seal or a valve, a "
        "few pounds rather than a new unit - and the make settles which: it is stamped on the body "
        "of it or under the cap, and the maker's page for that exact one has the part number and "
        "the video for the job",
        "Most of what goes wrong on one is a seal, a washer or a valve, and none of them is dear - "
        "take the make and model off it, on the body or under the handle, and the maker's page for "
        "that model shows the part and how the head comes off",
    ),
    ("tools", "fixture"): (
        "It is a spanner job rather than a kit: the maker's page for the model names the sizes, and "
        "a plumber's merchant has the washer or the cartridge",
        "The fittings come with the unit, and the maker's page for that model says which sizes you "
        "need for it",
    ),
    ("how_long", "fixture"): (
        "With the part in hand it is a short job - the maker's page for the model gives the time, "
        "and it is usually the inside of an hour for a washer or a cartridge",
        "The maker's page for that model says how long it takes, and most of that is the water off "
        "and the old part out",
    ),
}
KINDS = ((A_FIXTURE, "fixture"), (A_KIT, "kit"), (AN_APPLIANCE, "appliance"),
         (PAPERWORK, "paperwork"), (A_COMMITMENT, "commitment"))
ASKS = ((ASK_GET_OUT, "get_out"), (ASK_TOOLS, "tools"), (ASK_HOW_LONG, "how_long"),
        (ASK_SIZE, "size"), (ASK_BE_IN, "be_in"), (ASK_COVERED, "covered"),
        (ASK_SEND_BACK, "send_back"), (ASK_EXACT, "exact"))

OPENER = (
    "I can't see {S} from here, sorry",
    "I haven't got {S} in front of me, sorry",
    "There is no way for me to check {S} from here, sorry",
)
OPENER_TERMS = (
    "I can't see the terms on {S} from here, sorry",
    "I haven't got the small print for {S}, sorry",
    "I can't check what {S} says about getting out, sorry",
)
QUESTION = {
    "tools": ("What does your sheet list?", "What came in the box with it?"),
    "how_long": ("What does it say on the sheet?", "Does the sheet give a time for the job?"),
    "size": ("What have you got to fit it in?", "What do the dimensions say on yours?"),
    "be_in": ("What does the tracking say?", "Did they give you a time slot?"),
    "covered": ("What does the paperwork say it covers?", "Do you have the reference to hand?"),
    "send_back": ("What does it ask you to send?", "Have you got the reference on it?"),
    "get_out": ("How much notice does it ask for?", "Do you still have the terms it came with?"),
    "exact": ("What is the model number on it?", "Can you read the plate on it?"),
    "first_step": ("What does the plate say on yours?", "Have you got the sheet that came with it?"),
}


QUESTION_KIND = {
    ("first_step", "kit"): ("Have you got the sheet that came with it?",
                            "Is the sheet it came with still about?"),
    ("tools", "appliance"): ("What does the plate say your model is?",
                             "Do the fixings come with it or are they extra?"),
    ("first_step", "fixture"): ("Do you know the make of it?",
                                 "Can you see the make on it?"),
    ("tools", "fixture"): ("Do you know the make of it?",
                            "Is the make on it anywhere?"),
}


THEIR_OWN = frozenset(("my", "our", "your", "his", "her", "their", "the", "this", "that",
                       "these", "those"))
A_RECEIPT = re.compile(
    r"\b(?:got|bought|ordered|received|arrived|came|delivered|picked\s+up|sent\s+(?:me|us)|"
    r"turned\s+up|was\s+delivered|was\s+sent|it's\s+here|its\s+here|came\s+with)\b")
A_JOB_ON_IT = re.compile(
    r"\bput(?:ting)?\s+(?:\w+\s+){0,4}(?:up|together)\b|\bassembl\w*|\binstall\w*|"
    r"\bbuild\w*|\berecting\b|\bfitting\b")
THEIR_COPY_ASKS = frozenset(("be_in", "send_back", "exact"))


def _they_have_it(said, ask, determiner):
    if ask in THEIR_COPY_ASKS:
        return True
    if determiner in THEIR_OWN:
        return True
    return bool(A_RECEIPT.search(said) or A_JOB_ON_IT.search(said))


def _said(text):
    return " ".join(str(text or "").lower().split())


_DETERMINER = re.compile(
    r"\b(my|the|our|your|this|that|a|an|his|her|their)\s+$")


def _the_thing_named(said):
    best = None
    for pattern, kind in KINDS:
        for match in pattern.finditer(said):
            word = match.group(0)
            if best is None or len(word) > len(best[0]):
                best = (word, kind, match.start())
    if best is not None:
        papers = list(PAPERWORK.finditer(said))
        if papers:
            word = papers[0].group(0)
            best = (word, "paperwork", papers[0].start())
    if best is None:
        return None
    word, kind, start = best
    before = said[:start]
    said_as = "the %s" % word
    found = _DETERMINER.search(before)
    determiner = found.group(1) if found else None
    if found:
        said_as = "%s %s" % ({"my": "your", "our": "your"}.get(found.group(1), found.group(1)),
                             word)
    return said_as, kind, determiner


def _the_thing_in_the_thread(memory):
    turns = (memory or {}).get("turns") or []
    seen = 0
    for turn in reversed(turns):
        said = _said(turn.get("user") if isinstance(turn, dict) else "")
        if not said:
            continue
        found = _the_thing_named(said)
        if found:
            word, kind = found[0], found[1]
            word = re.sub(r"^(?:my|our|your|his|her|their|the|a|an)\s+", "", word)
            return "the " + word, kind, "the"
        seen += 1
        if seen >= 2:
            return None
    return None


def on_the_thing(clean, memory=None, understood=None):
    said = _said(clean)
    if (not said or NOT_HERE.search(said) or NOT_ABOUT_THE_CONVERSATION.search(said)
            or NOT_A_LOOKUP_BUT_A_REQUEST.search(said) or A_JUDGEMENT_ASK.search(said) or A_PLAN_ASK.search(said)
            or A_COOKING_LINE.search(said) or A_READING_JUST_GIVEN.search(said)
            or A_WHY_ASK.search(said) or A_METHOD_OR_ADVICE_ASK.search(said) or A_DECISION_ABOUT_GOING_ON.search(said)
            or A_NOW_OR_NEVER_ASK.search(said)
            or NOT_ABOUT_THE_VISIT.search(said)):
        return None
    thing = _the_thing_named(said)
    from_the_thread = thing is None
    thing = thing or _the_thing_in_the_thread(memory)
    if not thing:
        return None
    word, kind, determiner = thing
    ask = None
    for pattern, name in ASKS:
        if pattern.search(said):
            ask = name
            break
    if ask is None:
        if not from_the_thread:
            return None
        if NOT_ON_THE_PLATE.search(said):
            return None
        ask = "first_step"
    if not from_the_thread and not _they_have_it(said, ask, determiner):
        return None
    pool = CARRIERS.get((ask, kind))
    if not pool:
        return None
    opener_pool = OPENER_TERMS if ask == "get_out" else OPENER
    opener = pick(opener_pool, memory or {}, said).format(S=word)
    carrier = pick(pool, memory or {}, said)
    question = pick(QUESTION_KIND.get((ask, kind)) or QUESTION[ask], memory or {}, said)
    return "%s. %s. %s" % (opener, carrier, question)