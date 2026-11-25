
import re


def _has(line, phrases):
    for phrase in phrases:
        if re.search(r"(?<![a-z0-9])" + re.escape(phrase) + r"(?![a-z0-9])", line):
            return True
    return False


def _words(line):
    return set(re.findall(r"[a-z0-9']+", line))


def _names_one_of(line, phrases):
    words = _words(line)
    for phrase in phrases:
        parts = phrase.split()
        if len(parts) == 1:
            if parts[0] in words:
                return True
        elif re.search(r"(?<![a-z0-9])" + r"\s+".join(re.escape(part) for part in parts) +
                       r"(?![a-z0-9])", line):
            return True
    return False


OWN_PERSON = frozenset("""
my our his her their i me we us myself himself herself yourself husband wife partner boyfriend
girlfriend fiance fiancee mum mom mother dad father son daughter kid kids child children baby
nan nana grandma grandad granny sister brother friend friends boss manager landlord landlady
neighbour neighbor colleague carer stepmum stepdad stepson stepdaughter nephew niece
""".split())
NOBODY_NAMED = frozenset("""
it that this these those he she they him her them you your me us i we someone somebody anyone
anybody everyone everybody something anything nothing
""".split())
ABOUT_THE_BOT = ("made you", "created you", "built you", "who are you", "what are you",
                 "who made u", "who created u", "made u", "your name", "were you made",
                 "invented you", "designed you")


CONTACT_ASKS = ("postcode", "postal code", "phone number", "telephone number", "telephone",
                "contact number", "contact details", "their number", "the number for",
                "number for the", "whats the number", "what's the number", "what is the number",
                "the address", "address of", "address for")
WHERE_ASKS = ("where is the", "where's the", "wheres the", "weres the", "where is a",
              "where is an", "where can i find", "where do i find", "nearest branch",
              "nearest one", "nearest shop", "nearest store", "nearest office",
              "closest branch", "nearest chemist", "nearest pharmacy")
PLACE_NOUNS = ("station", "airport", "office", "shop", "store", "supermarket", "bank",
               "post office", "tip", "recycling centre", "dump", "library", "pool",
               "swimming pool", "leisure centre", "park", "car park", "car park", "surgery",
               "pharmacy", "chemist", "hospital", "museum", "hotel", "restaurant", "pub",
               "cafe", "church", "cathedral", "school", "college", "university", "market",
               "garage", "petrol station", "bus stop", "train station", "coach station",
               "toilets", "loo", "customer service", "reception", "depot", "showroom",
               "river", "lake", "mountain", "hill", "beach", "coast", "forest", "wood",
               "castle", "palace", "bridge", "square", "street", "road", "lane", "avenue",
               "village", "town", "city", "centre", "center")
NOT_A_PLACE = re.compile(
    r"(?<![a-z])(?:parcel|order|delivery|refund|application|claim|appointment|interview|"
    r"flight|connection|luggage|suitcase|passport|keys|wallet|phone|remote|charger|filter|"
    r"point of|point in|sense of|point to|best place to put|best place for it)(?![a-z])")
NOT_A_LOOKUP = re.compile(
    r"^\s*who\b|(?<![a-z])(?:how do you say|how do i say|how would you say|how to say|"
    r"what does [a-z' ]{1,20} mean|translate|in french|in spanish|in german|in italian|"
    r"in welsh)(?![a-z])")
PLACE_POOL = (
    "A postcode, a phone number and opening hours all change hands, so I can't hold them: a "
    "map app turns the name into the address, the postcode and the number, and the place's "
    "own page has today's hours.",
    "The place's own page is the one with today's hours, and a map app has the address and "
    "the number, so tell me what they say and I'll help with the rest - I can't look either "
    "up from here.",
)
TRAVEL_WORDS = ("train", "trains", "station", "airport", "coach", "bus", "buses", "flight",
                "flights", "plane", "ferry", "tram", "tube", "underground", "motorway", "road",
                "drive", "driving", "journey", "commute", "cycle", "walk", "route", "miles",
                "distance", "terminals", "platform", "coast", "beach", "island", "seaside",
                "harbour", "harbor", "port", "stadium", "venue", "town centre", "city centre")
GET_TO_ASKS = ("how do i get to", "how do you get to", "how do i get from", "how to get to",
               "how to get from", "directions to", "the way to", "get to", "get from",
               "way to get to", "way to get from", "way into town")
ROUTE_ASKS = re.compile(
    r"(?<![a-z])(?:how far (?:is|are) (?:it |that )?(?:from|away from)|"
    r"how many miles (?:is it |are there )?from|"
    r"how long does it take to (?:get|travel|drive|walk|cycle|go)\b|"
    r"how far is it\b|best route from|distance (?:from|between))(?![a-z])")
NOT_A_JOURNEY = ("in advance", "get over", "get fit", "get better", "get decent", "get going",
                 "get there with", "how do i get a", "how do i get my", "how do i get more",
                 "how do i get rid", "how do i get out of", "get toned", "get crispy",
                 "get to sleep", "get up", "get through", "get started", "get going",
         "get a passport", "get an appointment", "get a visa", "get my passport",
         "get a driving test", "get my licence", "get a refund", "get pregnant")
TAKE_TO_ASKS = re.compile(r"(?<![a-z])how long does it take to(?![a-z])")
GOES_TO = tuple(PLACE_NOUNS) + ("airport", "station", "town", "city", "coast", "beach",
                                "work", "school", "office", "home", "town centre",
                                "city centre", "train station", "bus stop")
PLACE_ROUTE_POOL = (
    "Miles and minutes depend on the roads on the day, which is why a journey planner is the "
    "one to ask - I can't measure one from here: put the two places in and it gives the "
    "distance and the time in one go.",
    "The roads decide it rather than the map, so I can't give you the miles and the time "
    "myself: put the two places into a map app and it'll have both; say what you're planning "
    "and I'll help with the rest of it.",
)

TRADES = ("plumber", "electrician", "builder", "builders", "roofer", "painter", "decorator",
          "joiner", "carpenter", "plasterer", "tiler", "gardener", "cleaner", "locksmith",
          "boiler engineer", "gas engineer", "heating engineer", "accountant", "bookkeeper",
          "solicitor", "lawyer", "conveyancer", "dentist", "optician", "vet", "mechanic",
          "tutor", "physio", "physiotherapist", "chiropodist", "hairdresser", "barber",
          "mover", "movers", "removals", "surveyor", "architect", "tree surgeon",
          "pest controller", "chimney sweep", "appliance repair", "man with a van")
HIRING = ("find", "recommend", "any good", "know a", "know any", "know of", "looking for",
          "need a", "need an", "need someone", "someone who", "near me", "nearby", "local",
          "in my area", "can anyone", "suggest", "anybody", "anyone", "ne1", "some1", "any1")
NOT_A_TRADE = ("vacuum cleaner", "steam cleaner", "carpet cleaner", "oven cleaner",
               "drain cleaner", "glass cleaner", "mascara", "lawyered")
NOT_A_HIRE = ("do i need a", "do i need an", "will i need a", "will i need an",
              "should i get a", "should i get an", "myself", "died", "death", "bereave",
              "funeral", "complaint", "complain", "how do i", "how to", "why did",
              "my own", "sack", "dismiss", "tribunal", "quote from", "already got",
              "says i need", "told me i need", "said i need", "joining", "joined",
              "registered with", "agreeing a price with", "already have", "already seeing")
OWN_PROFESSIONAL = re.compile(
    r"(?<![a-z])my\s+(?:[a-z]+\s+){0,2}(?:" + "|".join(TRADES) + r")(?![a-z])")
QUOTING_TRADES = ("plumber", "electrician", "builder", "builders", "roofer", "painter",
                  "decorator", "joiner", "carpenter", "plasterer", "tiler", "gardener",
                  "locksmith", "boiler engineer", "gas engineer", "heating engineer", "mover",
                  "movers", "removals", "tree surgeon", "pest controller", "chimney sweep",
                  "appliance repair", "man with a van", "cleaner", "mechanic")
TRADE_POOL = (
    "Who is any good and who is free changes month to month, so I can't vouch for one: a "
    "directory or map app search for {trade} near you sorted by the recent reviews, then two "
    "written quotes before you book anyone.",
    "The recent reviews are what tells you and I can't see them from here: a map app search "
    "for {trade} near you sorted by reviews is the quickest way in; ask for two quotes, and "
    "check they're registered before you pay a deposit.",
)
PROFESSIONAL_POOL = (
    "Whether they're taking new people and how long the wait is are the two things that "
    "decide it, and neither is something I can see: a map app or the profession's own finder "
    "lists them by area - ring two and ask about the wait and the fee before you go.",
    "The wait and the fee are the parts that decide it and I can't see either from here: a "
    "map app or the official finder for {trade} near you shows who is taking on new people, so "
    "read the recent reviews and ring before you set off.",
)

PICKED_IN_A_PLACE = (
    "place", "places", "area", "part", "parts", "bit", "side", "neighbourhood", "neighborhood",
    "quarter", "hotel", "hotels", "restaurant", "restaurants", "pub", "pubs", "bar", "bars",
    "cafe", "cafes", "café", "beach", "beaches", "town", "city", "village", "park", "museum",
    "museums", "gallery", "market", "markets", "spot", "spots", "stay", "campsite", "campsites",
    "site", "sites", "walk", "walks", "swim", "swimming", "view", "coffee", "breakfast",
    "brunch", "chippy", "takeaway", "shop", "shops", "things to do", "thing to do",
    "things to see", "day out", "day trip", "beer garden")
PICK_ASKS = ("best", "top", "good", "nice", "decent", "recommend", "worth", "which")
NOT_A_PICK = ("best time", "good time", "right time", "busiest time", "cheapest time",
              "worth it if", "worth it when", "worth buying", "worth the money")
IN_A_PLACE = re.compile(
    r"\b(?:in|near|around|round|outside)\s+(?:the\s+|this\s+|that\s+)?"
    r"(?:here|there|[a-z][a-z'\-]*)")
NEAR_ME = re.compile(r"(?<![a-z])(?:near|around|round|by) (?:me|us|here)(?![a-z])")
PICK_POOL = (
    "Reviews beat anything I could say about {thing}, which I have never been to: a map app or "
    "the town's visitor site will name the ones people rate - tell me what you want from it and "
    "I'll help you choose.",
    "Reviews beat a guess from me about {thing}, since I have never been to any of them: a map "
    "app or the local visitor site names the ones people rate - say what matters and I'll help "
    "you narrow it down.",
)
PICK_ANYWHERE_POOL = (
    "Reviews from people who have been beat any guess of mine about a place, and a map app or "
    "the town's visitor site names the ones people rate: tell me what you want from the trip "
    "and I'll help you choose.",
    "Other people's reviews beat anything I could say about a place, and I have never been to it: "
    "a map app or the local visitor site sorts it by what you want from the trip - say what "
    "matters and I'll help you narrow it down.",
)

WORTH_VISITING = re.compile(
    r"(?<![a-z])(?:is|are|will)\b[^.!?]{0,40}\bworth (?:visiting|going to|a visit|seeing)"
    r"(?![a-z])")

WHO_FACT = re.compile(
    r"(?<![a-z])(?:who|whos|who's)\s+(?:is|are|was|were|owns|runs|makes|made|plays|played|"
    r"wrote|writes|invented|founded|created|discovered|sang|sings|composed|directed|built|"
    r"designed|painted|won)(?![a-z])")
WHO_POOL = (
    "The record is the only place it is written down, and a name I got half right would stick, "
    "so I can't check one: "
    "Wikipedia has it with its sources and the official site will confirm it - tell me what "
    "you find and I'll help you make sense of it.",
    "The Wikipedia page for it answers that in a line and cites where the line comes from, "
    "and I can't look it up from here: paste what it says and I'll help you weigh the rest.",
)

FIGURE_ASKS = re.compile(
    r"(?<![a-z])(?:population|how many people (?:live|are there)|how tall|how deep|"
    r"how high|how old (?:is|are)|how heavy|how big (?:is|are|was)|how large|how long is the|"
    r"how wide|how many miles away|how far away|how far is|square miles|"
    r"square metres does)(?![a-z])")
SETTING_ASKS = re.compile(
    r"(?<![a-z])(?:should|shall|do i|can i|need to|would i|is it best|is best|ought)(?![a-z])")
METHOD_ASKS = re.compile(r"^\W*(?:how (?:do|would|can|might) (?:you|i|we|one)|ways? to|"
                         r"any (?:way|tips))(?![a-z])")
POLICY_WORDS = ("return window", "refund policy", "returns policy", "warranty", "guarantee",
                "terms and conditions", "the policy", "their policy", "rules")
FIGURE_POOL = (
    "The date on a figure matters as much as the figure, and I can't check one I wasn't told: "
    "Wikipedia has that number with its source - tell me what it says and I'll help you make "
    "sense of it.",
    "A number I invented would be worse than none, and the year is half of it, so I would not "
    "guess: the Wikipedia page or the official site will have it, with the source; paste what "
    "it says and I'll help you weigh it up.",
)

MATERIALS = ("slab", "slabs", "tile", "tiles", "brick", "bricks", "paint", "wallpaper", "turf",
             "gravel", "sand", "cement", "mortar", "decking", "boards", "panel", "panels",
             "pots", "seeds", "bulbs", "compost", "bark", "chippings", "insulation",
             "plasterboard", "skirting", "beading", "underlay", "carpet", "lino", "edging",
             "fence posts", "screws", "hooks", "plants", "shrubs", "trees")
MATERIAL_ASK = re.compile(
    r"(?<![a-z])(?:how many|how much)\b[^.!?]{0,40}?"
    r"(?<![a-z])(?:do i need|will i need|should i (?:get|buy)|would i need|do we need|"
    r"to cover|for a|for an|for my|needed)(?![a-z])")
HOW_MANY_POOL = (
    "I can do that sum if you give me the numbers: the length and width of what you're covering, "
    "and how much one slab, pot, roll or bag covers. Tell me those and I'll work out how many to "
    "buy, with a little extra for cuts.",
    "Give me the measurements - the area's length and width, and the size of one of them - and "
    "I'll do the arithmetic, waste and cuts included. That's the part I'm good for; the size of "
    "your patio is the part I can't see.",
)

BUY_ASK = re.compile(
    r"(?<![a-z])(?:where can i|where do i|where could i|where should i|where to|who sells|"
    r"where sells)\s+(?:buy|get|find|pick up|order)(?![a-z])")
BUY_THING = re.compile(
    r"\b(?:buy|get|find|pick up|order|sells|selling)\s+(?:me\s+)?"
    r"((?:a|an|some|any|the|one|my|our)?\s*[a-z][a-z'\-]*(?:\s+[a-z][a-z'\-]*){0,3})")
BUY_TAIL = frozenset("""
    today tonight tomorrow now online cheap cheaply near nearby locally please then round
    second hand secondhand from at in on shop shops store stores
""".split())
BUY_TAIL_PHRASES = (" today", " tonight", " tomorrow", " now", " online", " cheap", " cheaply",
                    " near me", " near you", " nearby", " locally", " round here", " in town",
                    " second hand", " secondhand", " please", " asap", " this week")
BUY_THING_STOPS = re.compile(r"\s(?:for|to|as|with|in|on|at|from|near|under|around|that|which|"
                             r"because|so|and|or|but)\s")
BUY_NOT = ("advice", "help", "support", "information", "info", "a loan", "a mortgage", "a job",
           "apprenticeship", "work", "jab", "jabs", "vaccine", "vaccination", "prescription",
           "treatment", "test", "checked", "tested", "treated", "seen", "blocked list",
           "settings", "setting", "menu", "my money back")
BUY_NOT_THINGS = frozenset("""
rate rates price prices deal deals offer offers quote quotes times time hours opening
availability stock information info news number address date dates list lists
loan loans fixed repaired serviced mended certificate certificates replacement
payslip payslips document documents form forms passport licence license visa
""".split())
BUY_NOT_PEOPLE = ("one", "ones", "someone", "somebody", "anyone", "anybody", "person", "people")
BUY_NOT_THE_THING = ("matched", "made", "done", "fixed", "printed", "framed", "engraved",
                     "repaired", "serviced", "mended", "altered", "adjusted", "measured",
                     "fitted", "installed", "drilled", "cleaned", "mounted", "trimmed",
                     "sharpened", "copied", "printed off")
SERVICE_WORK = {
    "fixed": "repair", "fix": "repair", "mended": "repair", "mend": "repair",
    "repaired": "repair", "repair": "repair", "serviced": "service", "service": "service",
    "cleaned": "cleaning", "clean": "cleaning", "cut": "cut", "trimmed": "trimming",
    "trim": "trimming", "altered": "alterations", "alter": "alterations",
    "adjusted": "adjustment", "adjust": "adjustment", "framed": "framing", "frame": "framing",
    "engraved": "engraving", "engrave": "engraving", "sharpened": "sharpening",
    "sharpen": "sharpening", "printed": "printing", "print": "printing",
    "fitted": "fitting", "fit": "fitting", "installed": "installation", "install": "installation",
    "drilled": "drilling", "drill": "drilling", "mounted": "mounting", "mount": "mounting",
    "copied": "copying", "copy": "copying", "restored": "restoration", "restore": "restoration",
    "valeted": "valet", "valet": "valet", "resoled": "resoling", "resole": "resoling",
    "replaced": "replacement", "replace": "replacement", "resprayed": "respray",
    "respray": "respray", "washed": "washing", "wash": "washing",
}
SERVICE_PHRASES = (
    ("taken in", "alterations"), ("take in", "alterations"), ("taking in", "alterations"),
    ("let out", "alterations"), ("taken up", "alterations"), ("taken in a bit", "alterations"),
)
SERVICE_NOUNS = (
    ("haircut", ("hair cut", "")), ("hair cut", ("hair cut", "")),
    ("dry cleaning", ("dry cleaning", "")), ("mot", ("mot", "car")),
)
SERVICE_JOB_NAMES = {
    ("hair", "cut"): "haircuts",
    ("", "hair cut"): "haircuts",
    ("key", "cut"): "key cutting",
    ("car", "mot"): "an MOT",
    ("car", "washing"): "a car wash",
    ("shoes", "resoling"): "shoe repairs",
    ("shoe", "resoling"): "shoe repairs",
}
SERVICE_POOL = (
    "The last few reviews and two prices are what decide a {job}, not a list I could keep: "
    "search a map app or a directory near you, read the recent ones, and ring two for a price "
    "before you book.",
    "Prices for the same {job} swing wide, so the reviews and two quotes decide it: a map app "
    "or a directory near you, sorted by the recent ones, then two prices before you book.",
)
SERVICE_ASK = re.compile(
    r"(?<![a-z])(?:where can i|where do i|where could i|where should i|where to|who can|"
    r"who could|who should i|who does|who would|anywhere i can)\s+"
    r"(?:get|have|take|find|send|put)\b|(?<![a-z])(?:who can|who could|who does|who would)\b"
    r"|(?<![a-z])(?:can|could|should|would|will)\s+i\s+(?:get|have)\b")
SERVICE_THING = re.compile(
    r"\b(?:get|have|take|send|put|fix|repair|mend|service|clean|cut|alter|resole|reheel|"
    r"replace)\s+(?:me\s+)?((?:a|an|the|my|our|some)?\s*[a-z][a-z'\-]*"
    r"(?:\s+[a-z][a-z'\-]*){0,2})")
SERVICE_NOT_A_THING = frozenset("""
it that this them one ones me him her us you yourself myself anything something nothing
""".split())
SERVICE_NOT_HEALTH = frozenset("""
teeth tooth dental blood bloods jab injection vaccine vaccination wound stitches cast mole skin
eye eyes ear ears smear scan xray procedure
""".split())
SERVICE_STOPS = frozenset("""
cheap cheaply properly professionally done somewhere someone today tonight tomorrow please again
back off out about that which because so and or for taken take taking let
""".split())
BUY_POOL = (
    "Stock moves by the hour and a phone call is the only thing that checks it, so I can't "
    "see who has {thing} near you: a map app search shows what's nearest, and ring before you "
    "set off.",
    "Stock moves by the hour, so a list from me would be wrong by the time you got there: a "
    "map app or the chain's own site will say who has {thing} near you, and a ring first "
    "saves the trip.",
)


def _the_trade(line):
    for trade in TRADES:
        if re.search(r"(?<![a-z])" + re.escape(trade) + r"(?![a-z])", line):
            return trade
    return ""


def _the_thing(line):
    found = BUY_THING.search(line)
    if not found:
        return ""
    text = " " + found.group(1).strip()
    for phrase in BUY_TAIL_PHRASES:
        if text.endswith(phrase):
            text = text[:-len(phrase)]
    cut = BUY_THING_STOPS.search(text)
    if cut:
        text = text[:cut.start()]
    words = [w for w in text.split() if w not in BUY_TAIL]
    while words and words[-1] in ("a", "an", "the", "some", "any", "my", "our", "of", "for"):
        words.pop()
    thing = " ".join(words[:4]).strip()
    if not thing or thing in ("a", "an", "the", "some", "any", "it", "one", "them", "me"):
        return ""
    return thing


def _trade_route(line, ctx):
    trade = _the_trade(line)
    if not trade or _has(line, NOT_A_TRADE) or _has(line, NOT_A_HIRE):
        return None
    if OWN_PROFESSIONAL.search(line):
        return None
    if not _has(line, HIRING):
        return None
    pool = TRADE_POOL if trade in QUOTING_TRADES else PROFESSIONAL_POOL
    return tuple(line.format(trade=trade) for line in pool)


def _buy_route(line, ctx):
    if not BUY_ASK.search(line) or _has(line, BUY_NOT):
        return None
    thing = _the_thing(line)
    if not thing or thing.split()[-1] in BUY_NOT_THINGS:
        return None
    if thing.split()[0].strip() in ("my", "our"):
        return None
    if _has(" " + thing + " ", BUY_NOT_THE_THING) or _has(" " + thing + " ", BUY_NOT_PEOPLE):
        return None
    return tuple(pool.format(thing=thing) for pool in BUY_POOL)


def _the_service(line, pointed=""):
    if not SERVICE_ASK.search(line):
        return None
    work = ""
    for phrase, word in SERVICE_PHRASES:
        if re.search(r"(?<![a-z])" + re.escape(phrase) + r"(?![a-z])", line):
            work = word
            break
    if not work:
        for verb, word in sorted(SERVICE_WORK.items(), key=lambda pair: -len(pair[0])):
            if re.search(r"(?<![a-z])" + re.escape(verb) + r"(?![a-z])", line):
                work = word
                break
    if not work:
        for noun, (word, thing) in SERVICE_NOUNS:
            if re.search(r"(?<![a-z])" + re.escape(noun) + r"(?![a-z])", line):
                return word, thing
        return None
    found = SERVICE_THING.search(line)
    if not found:
        return None
    words = []
    for word in found.group(1).split():
        if word in ("a", "an", "the", "my", "our", "some", "of", "for", "to", "in", "on"):
            continue
        if word in BUY_TAIL or word in SERVICE_WORK or word in SERVICE_STOPS:
            break
        words.append(word)
    if words and words[0] in SERVICE_NOT_A_THING:
        words = [word for word in str(pointed or "").lower().split() if re.search(r"[a-z]", word)]
        if not words or words[0] in SERVICE_NOT_A_THING:
            return None
    if not words:
        return None
    if any(word in SERVICE_NOT_HEALTH for word in words):
        return None
    return work, " ".join(words[:3])


def _service_route(line, ctx):
    found = _the_service(line, ctx.get("pointed") if isinstance(ctx, dict) else "")
    if not found:
        return None
    work, thing = found
    job = SERVICE_JOB_NAMES.get((thing, work)) or (thing + " " + work).strip()
    return tuple(pool.format(job=job) for pool in SERVICE_POOL)


def _about_a_place(line, ctx):
    if ctx.get("places"):
        return True
    if ctx.get("travel"):
        return True
    if WORTH_VISITING.search(line):
        return True
    return bool(NEAR_ME.search(line))


def _the_picked_thing(line):
    found = ""
    for phrase in PICKED_IN_A_PLACE:
        if len(phrase) <= len(found):
            continue
        if _names_one_of(line, (phrase,)):
            found = phrase
    if found == "thing to do" or found == "things to do":
        return "things to do"
    return found


def _pick_route(line, ctx):
    if not _has(line, PICK_ASKS) and not WORTH_VISITING.search(line):
        return None
    if _has(line, NOT_A_PICK) or not _about_a_place(line, ctx):
        return None
    if WORTH_VISITING.search(line) and IN_A_PLACE.search(line):
        thing = _the_picked_thing(line)
        if not thing:
            return PICK_ANYWHERE_POOL
        return tuple(pool.format(thing=thing) for pool in PICK_POOL)
    where = IN_A_PLACE.search(line)
    if not where:
        return None
    thing = _the_picked_thing(line[:where.start()])
    if not thing:
        return None
    return tuple(pool.format(thing=thing) for pool in PICK_POOL)


def _how_many_route(line, ctx):
    if not (MATERIAL_ASK.search(line) and _names_one_of(line, MATERIALS)):
        return None
    if not re.search(r"(?<![a-z])how (?:many|much)(?![a-z])", line):
        return None
    return HOW_MANY_POOL


def _place_route(line, ctx):
    if NOT_A_PLACE.search(line) or NOT_A_LOOKUP.search(line):
        return None
    if _has(line, CONTACT_ASKS):
        return PLACE_POOL
    if not _has(line, WHERE_ASKS):
        return None
    if not _names_one_of(line, PLACE_NOUNS):
        return None
    return PLACE_POOL


def _route_route(line, ctx):
    if _has(line, NOT_A_JOURNEY):
        return None
    words = _words(line)
    travel = bool(words & set(TRAVEL_WORDS))
    if ROUTE_ASKS.search(line):
        if not (travel or ctx.get("places")):
            return None
        if TAKE_TO_ASKS.search(line) and not (ctx.get("places") or _names_one_of(line, GOES_TO)):
            return None
        return PLACE_ROUTE_POOL
    if _has(line, GET_TO_ASKS) and (travel or ctx.get("places")):
        return PLACE_ROUTE_POOL
    if re.search(r"(?<![a-z])from\b[^.!?]{1,40}\bto(?![a-z])", line) and travel \
            and re.search(r"how (?:do|can|should|would) (?:i|you|we)", line):
        return PLACE_ROUTE_POOL
    return None


OPEN_CHEMIST_HOURS = re.compile(
    r"(?<![a-z])(?:open|opens|opening|closed|closing|closes|shut|shuts|late|late-night|latenight|"
    r"tonight|now|today|sunday|weekend|bank holiday|out of hours|24 ?hour|all night)(?![a-z])")
CHEMISTS = ("pharmacy", "pharmacies", "chemist", "chemists", "dispensary")
OPEN_CHEMIST_POOL = (
    "Most towns have one open late: a big chain chemist usually runs to 10 or 11, a supermarket "
    "one shuts by 8 and earlier on a Sunday, and a bank holiday moves it again. Which of the ones "
    "near you is open tonight I can't see - the NHS pharmacy finder lists them with the closing "
    "time and the distance, and 111 says the same on the phone.",
    "There is nearly always a late chemist somewhere in a town - the chains stay open to about 10, "
    "and the ones inside supermarkets shut by 8, earlier on a Sunday - but the hours near you are "
    "not something I can look up. The NHS pharmacy finder shows what is open now and until when; "
    "111 will find you one if the phone is easier, and an out-of-hours prescription can go there.",
)


def _open_chemist_route(line, ctx):
    if not _has(line, CHEMISTS) or not OPEN_CHEMIST_HOURS.search(line):
        return None
    if re.search(r"(?<![a-z])(?:what|anything|something|buy|get|recommend)(?![a-z])", line) \
            and not re.search(r"(?<![a-z])(?:open|closes|close|shut|late|tonight)(?![a-z])", line):
        return None
    return OPEN_CHEMIST_POOL


def _who_route(line, ctx):
    if not WHO_FACT.search(line) or _has(line, ABOUT_THE_BOT):
        return None
    words = _words(line)
    if words & OWN_PERSON:
        return None
    if re.search(r"(?<![a-z])(?:who|whos|who's)\s+(?:is|was|were|are)\s+"
                 r"(?:it|that|this|he|she|they|them|you|thou)\b", line):
        return None
    return WHO_POOL


def _tide_route(line, ctx):
    if not TIDE_ASK.search(line):
        return None
    if TIDE_WHY.search(line):
        return None
    return TIDE_POOL


def _figure_route(line, ctx):
    if not FIGURE_ASKS.search(line) or SETTING_ASKS.search(line):
        return None
    if METHOD_ASKS.search(line) or _has(" " + line + " ", POLICY_WORDS):
        return None
    if _words(line) & OWN_PERSON:
        return None
    if re.search(r"(?<![a-z])how (?:old|tall|big|heavy|deep|far) (?:is|are) "
                 r"(?:he|she|they|it|you|we)(?![a-z])", line):
        return None
    return FIGURE_POOL


RECORD_ASKS = re.compile(
    r"(?<![a-z])(?:biggest|largest|tallest|longest|oldest|youngest|smallest|deepest|shallowest|"
    r"highest|lowest|heaviest|lightest|fastest|slowest|widest|narrowest|thinnest|strongest|"
    r"richest|poorest|wealthiest|busiest|coldest|hottest|wettest|driest|sunniest)(?![a-z])|"
    r"\bmost\s+(?:populous|expensive|common|popular|visited|deadly|abundant|spoken)(?![a-z])")
RECORD_ASKED = re.compile(
    r"(?<![a-z])(?:what|whats|what's|which|whichs|which's|who|whos|who's|where|wheres|where's|"
    r"name|tell me)(?![a-z])")
RECORD_POOL = (
    "I can't check a record from here, sorry - the list moves when somebody breaks it. Wikipedia "
    "keeps it with the date each one was set; paste what it says and I'll help you weigh it up.",
    "No record book here, sorry, and a half-remembered number would be wrong without saying so. "
    "The Wikipedia page for it keeps the list and dates it - tell me what it says and we can go "
    "from there.",
)


def _record_route(line, ctx):
    if not ctx.get("settled"):
        return None
    if not RECORD_ASKS.search(line) or not RECORD_ASKED.search(line):
        return None
    if _words(line) & OWN_PERSON or SETTING_ASKS.search(line) or METHOD_ASKS.search(line):
        return None
    if re.search(r"(?<![a-z])(?:the best|my best|your best|best way|worst way|best time)(?![a-z])",
                 line):
        return None
    if _has(" " + line + " ", ("size", "sizes", "pack", "packs", "box", "boxes", "bottle",
                              "bottles", "tin", "tins", "bag", "bags")):
        return None
    if _has(" " + line + " ", ("number", "numbers", "word", "words", "letter", "letters",
                              "digit", "digits", "prime", "sum", "total")):
        return None
    return RECORD_POOL


TRAVEL_TOPICS = ("geography-and-travel", "travel", "holidays", "days-out", "outdoors")


def _the_reading(understood):
    if not understood:
        return {"places": set(), "travel": False, "pointed": "", "settled": False}
    places = set()
    for entity in understood.get("entities") or ():
        if isinstance(entity, dict) and entity.get("type") == "place" and entity.get("text"):
            places.add(entity["text"])
    pointed = ""
    ref = understood.get("ref")
    if isinstance(ref, dict):
        for key in ("it", "that", "they", "them"):
            value = ref.get(key)
            if isinstance(value, str) and value.strip():
                pointed = value.strip()
                break
    topics = set(understood.get("topics") or ())
    if understood.get("topic"):
        topics.add(understood["topic"])
    travel = bool(topics & set(TRAVEL_TOPICS))
    settled = understood.get("over_time") is False
    return {"places": places, "travel": travel, "pointed": pointed, "settled": settled}


TIDE_ASK = re.compile(
    r"(?<![a-z])(?:what|which|whats|what's)\s+time\s+(?:is|are|does|do|will|would)"
    r"[^.!?]{0,24}?(?<![a-z])(?:high|low|the)\s*tides?(?![a-z])"
    r"|(?<![a-z])when(?:'s|s|'re|re| is| are| does| do| will| can| should)?\s+(?:the\s+)?"
    r"(?:high|low)\s+tide(?![a-z])"
    r"|(?<![a-z])when\s+(?:is|does|will)\s+the\s+tide(?![a-z])"
    r"|(?<![a-z])is\s+the\s+tide\s+(?:in|out|coming|going|high|low|up|down)(?![a-z])"
    r"|(?<![a-z])tide\s+(?:is\s+)?(?:in|out)\s+or\s+(?:in|out)(?![a-z])"
    r"|(?<![a-z])tide\s+(?:times|table|timetable)(?![a-z])"
    r"|(?<![a-z])what(?:'s|s|\s+is)\s+the\s+tide\s+(?:doing|like)(?![a-z])"
    r"|(?<![a-z])how\s+(?:high|low|far\s+out)\s+(?:is|will|does)\s+the\s+tide(?![a-z])"
    r"|(?<![a-z])when\s+(?:can|should)\s+(?:i|we)\s+(?:swim|walk|launch|get)\s+(?:out|across|on\s+the\s+"
    r"water|to\s+the\s+boat)(?![a-z])")
TIDE_WHY = re.compile(
    r"(?<![a-z])(?:why|how\s+(?:do|does|come)|what\s+causes?|explain|explained|what\s+are)\b"
    r"[^.!?]{0,20}(?<![a-z])tides?(?![a-z])"
    r"|(?<![a-z])tides?\b[^.!?]{0,24}(?:work|works|happen|caused|spring|neap|moon)(?![a-z])")
TIDE_POOL = (
    "High and low water move by up to an hour a day, and by minutes between two beaches a few "
    "miles apart, so a tide time is the one thing I would not guess: a tide-table site for "
    "that beach, or the harbour or pier's own page, has today and tomorrow, and the local "
    "paper prints them too.",
    "Two beaches a few miles apart turn minutes apart and the same one is an hour later "
    "tomorrow, so I can't hold today's times: the harbour's page or a tide table for that "
    "beach has them, with the height as well as the clock time - the height is the bit that "
    "matters if you are walking a causeway or launching a boat.",
)



FILLING_IT_IN = re.compile(
    r"(?<![a-z])(?:form|forms|application|answers|questionnaire|survey|booking|checkout|basket|"
    r"page|webpage|website|site|screen|portal|online|typed|filled\s+it\s+in|"
    r"filled\s+the\s+form\s+in)(?![a-z])")
SAVING_FAILED = re.compile(
    r"(?<![a-z])(?:didnt|didn't|did\s+not|doesnt|doesn't|does\s+not|wouldnt|wouldn't|would\s+not|"
    r"wont|won't|will\s+not|refused\s+to)\s+(?:save|keep|remember)(?![a-z])")
LOST_THE_WORK = re.compile(
    r"(?<![a-z])(?:didnt|didn't|did\s+not|doesnt|doesn't|does\s+not|wouldnt|wouldn't|would\s+not|"
    r"wont|won't|will\s+not|refused\s+to)\s+(?:save|keep|remember)(?![a-z])"
    r"|(?<![a-z])(?:went|took\s+me|jumped)\s+back\s+to\s+the\s+start(?![a-z])"
    r"|(?<![a-z])(?:start|do)\b[^.!?]{0,22}?(?<![a-z])(?:again|from\s+scratch)(?![a-z])"
    r"|(?<![a-z])(?:all\s+over\s+again)(?![a-z])"
    r"|(?<![a-z])(?:lost|wiped|cleared|erased|emptied)\s+(?:my\s+|the\s+|all\s+|the\s+whole\s+)?"
    r"(?:answers|work|everything|it\s+all|the\s+lot|basket|cart|form|application)(?![a-z])"
    r"|(?<![a-z])(?:disappeared|vanished|never\s+went\s+through)(?![a-z])"
    r"|(?<![a-z])(?:timed\s+out|crashed)(?![a-z])"
    r"|(?<![a-z])(?:signed\s+me\s+out|logged\s+me\s+out|kicked\s+me\s+out|threw\s+me\s+out)(?![a-z])"
    r"|(?<![a-z])(?:cant|can't|couldnt|couldn't|wont|won't)\s+(?:let\s+me\s+|allow\s+me\s+)?"
    r"(?:submit|send\s+it)(?![a-z])")
ON_A_SCREEN = re.compile(
    r"(?<![a-z])(?:online|website|web\s?site|site|webpage|web\s?page|page|screen|portal|checkout|"
    r"basket|cart|typed|typing|type|submitted|submit|link|app|browser|internet|form\s+online|"
    r"filling\s+in|click\w*|tap\w*|refresh\w*|reload\w*|scroll\w*|timed\s+out|session|"
    r"the\s+back\s+button|save\s+button)(?![a-z])")
THE_WORK_ITSELF = re.compile(
    r"(?<![a-z])(?:whole|entire|all\s+of\s+(?:it|my|the)|every\s+(?:answer|page|line|word)|"
    r"all\s+(?:of\s+)?(?:my|the)\s+(?:answers|work))(?![a-z])")
BACK_TO_START = re.compile(
    r"(?<![a-z])(?:went|took\s+me|jumped|sent\s+me)\s+back\s+to\s+the\s+start(?![a-z])"
    r"|(?<![a-z])(?:start|do)\b[^.!?]{0,22}?(?<![a-z])(?:again|from\s+scratch)(?![a-z])"
    r"|(?<![a-z])(?:all\s+over\s+again)(?![a-z])")
THE_BARE_FORMS = re.compile(
    r"(?<![a-z])(?:form|forms|application|applications|answers|questionnaire|survey)(?![a-z])")
NOT_A_WRECKED_FORM = ("in the post", "by post", "posted", "paper", "printed", "print it",
                      "in the letter", "through the door", "on paper", "claim", "compensation",
                      "lost my bag", "lost bag")
WRECKED_POOL = (
    "I can't see their system, but this order gets a lost form back more often than not: the back "
    "button before a reload, then a saved draft or a 'continue where you left off' link, then the "
    "service itself - ask them to check the half-finished application before you type it all "
    "again, because a duplicate is harder to undo than a gap.",
    "Their system isn't visible from here, so the order is what matters: back one page rather than "
    "reloading, then the drafts or 'continue your application' link, then the service itself, "
    "quoting any reference you were given. When you do type it again, keep the long answers in a "
    "document and paste them in, so a second timeout costs you nothing.",
)


def the_wrecked_form_reply(line):
    if not line or _has(line, NOT_A_WRECKED_FORM):
        return None
    if not FILLING_IT_IN.search(line) or not LOST_THE_WORK.search(line):
        return None
    if THE_BARE_FORMS.search(line) and not (ON_A_SCREEN.search(line)
                                           or SAVING_FAILED.search(line)
                                           or BACK_TO_START.search(line)
                                           or THE_WORK_ITSELF.search(line)):
        return None
    return WRECKED_POOL


READERS = (_trade_route, _service_route, _buy_route, _pick_route, _how_many_route, _place_route,
           _route_route, _who_route, _tide_route, _figure_route, _record_route,
           _open_chemist_route)


def for_the_ask(clean, repaired="", understood=None):
    if not clean:
        return None
    ctx = _the_reading(understood)
    for line in (clean, repaired or ""):
        if not line or not line.strip():
            continue
        for reader in READERS:
            found = reader(line, ctx)
            if found:
                return found
    return None
