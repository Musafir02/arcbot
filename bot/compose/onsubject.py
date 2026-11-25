import re

A_ASK_OPENER = re.compile(
    r"^\s*(?:can|could|do|does|did|is|are|was|were|would|will|should|am|shall|have|has|had|"
    r"what|when|where|which|who|why|how|if)\b", re.I)
A_BACK_REFERENCE = re.compile(
    r"\b(?:it|that|this|there|he|she|they|him|her|them|one|those|these|hers|his|theirs)\b", re.I)
A_SUBJECT_WORD_LIMIT = 2
A_EMPTY_ASK_WORDS = 2
A_EMPTY_ASK_LENGTH = 7
A_EMPTY_ASK_OPENER = re.compile(r"^\s*(?:how|when)\b", re.I)
A_POINTER_ASK = re.compile(r"^\s*(?:which|who)\b|^\s*how\s+come\b", re.I)
A_HELP_ASK = re.compile(
    r"^\s*(?:what|anything)\s+(?:would\s+|will\s+|might\s+)?helps?\b|"
    r"^\s*what\s+(?:can|should|could)\s+(?:i|we)\s+do\b|"
    r"^\s*how\s+(?:do|can|should)\s+i\s+(?:help|calm|support|comfort|reassure)\b", re.I)
A_RECALL_ASK = re.compile(
    r"^\s*(?:how many|how much)\b(?:(?!\bhow much (?:is|does|do|will|would)\b).)*?"
    r"\b(?:do i have|have i got|do we have|did i|did we|did he|did she)\b|"
    r"^\s*how many\b(?:\s+\w+){0,2}\s*$|^\s*how many\b.*\bagain\s*$|"
    r"^\s*what (?:day|date|time)\b|^\s*whats the (?:day|date|time)\b|"
    r"^\s*when (?:did|was that|were that|does my|is my|do i|are we)\b|"
    r"^\s*did you (?:get|catch|hear|note|remember|write)\b|"
    r"\b(?:what|how old|how long ago) (?:did|do|was) i (?:say|said|tell|told|mention|planning|"
    r"planning to do|doing)\b|\bdid i (?:say|tell|mention)\b", re.I)
A_COMPARISON_ASK = re.compile(
    r"\b(?:too (?:far|much|long|late|early|expensive|cheap|old|big|small)|worth it|a lot|"
    r"any good|good value|cheaper|expensive|good for|reasonable|enough)\b|"
    r"\b(?:is|was|would) (?:that|it|this) (?:good|bad|fair|ok|okay|decent)\b", re.I)
A_COOKING_TIME_ASK = re.compile(r"\bhow long\b", re.I)
A_FOOD_PRONOUN = re.compile(r"\b(?:it|them|those|that)\b", re.I)
A_ROASTING_WORD = re.compile(r"\b(?:roast|roasting|roasted|bake|baking|baked|oven)\b", re.I)
A_BOILING_WORD = re.compile(r"\b(?:boil|boiling|boiled|simmer|simmering)\b", re.I)
A_OTHER_METHOD = re.compile(
    r"\b(?:grill|grilling|grilled|fry|frying|fried|rest|resting|steam|steaming|poach|poaching|"
    r"barbecue|barbeque|bbq|microwave|air fryer|toast|toasting)\b", re.I)
A_NAMED_FOOD = re.compile(
    r"\b(?:chicken|turkey|beef|lamb|pork|ham|gammon|duck|goose|joint|steak|sausage|"
    r"sausages|fish|salmon|potato|potatoes|egg|eggs|rice|pasta|bread|cake|pastry|pie|"
    r"casserole|stew|chops|chop|brisket|shoulder|leg|breast|thigh|fillet|kettle)\b", re.I)
COOKING_TIME_SHAPES = {
    "oven": "Time depends on what it is and how heavy: a chicken is about 20 minutes per 500g plus "
            "20 minutes at 190C, and a joint of beef 15 to 25 minutes per 500g once it has browned. "
            "Tell me which it is and how much it weighs, and I'll do the sum.",
    "boil": "Boiling time depends on what they are: eggs are 6 minutes from boiling water for a "
            "runny yolk and 9 to 10 for a hard one. Tell me what it is and I'll narrow it down.",
    "either": "Time depends on the food and how it is cooked: a chicken is about 20 minutes per "
              "500g plus 20 minutes at 190C in the oven, and eggs are 6 minutes from boiling "
              "water for a runny yolk. Tell me what it is and how you are cooking it.",
}
A_COOKING_ASK = re.compile(
    r"\b(?:cook|cooking|cooked|roast|roasting|bake|baking|boil|boiling|fry|frying|grill|oven|"
    r"freezer|fridge|thaw|defrost|stuffing|gravy|rice|pasta|potato|potatoes|recipe|rest it)\b",
    re.I)
A_LOST_THING = re.compile(
    r"\b(?:lost|mislaid|misplaced|can'?t find|cannot find)\b|"
    r"\bleft (?:it|them|my|the|his|her)\b[^.?!]*\b(?:in|on|at|by)\b", re.I)
A_MACHINE_CUE = re.compile(
    r"\b(?:laptop|computer|phone|tablet|charger|charging|screen|windows|macbook|pc)\b", re.I)
A_A_QUESTION_ASK = re.compile(
    r"^\s*(?:what|whats|when|whens|where|wheres|which|who|whos|why|whys|how|hows|is|are|was|"
    r"were|do|does|did|can|could|should|would|will|shall|have|has|am|any|anything)\b", re.I)
A_JUDGEMENT_ASK = re.compile(
    r"\b(?:stupid|silly|daft|mad|unreasonable|out of order|selfish|allowed)\b", re.I)
A_JUDGEMENT_OF_AMOUNT = re.compile(
    r"\b(?:is|was|would) (?:that|it|this) (?:good|bad|ok|okay|enough|fair|normal|reasonable|"
    r"a lot|too much|too little|decent)\b", re.I)
AMOUNT_KINDS = ("money", "bills")
MACHINE_BEFORE_MACHINE_KINDS = ("car",)
A_WORDS_ASK = re.compile(
    r"^\s*(?:what|whats|how|hows|should|shall|can you|could you|would you|do i need to|give me|"
    r"help me)\b[^?]*\b(?:write|writing|word|words|say|saying|tell|telling|ask|asking|reply|"
    r"answer|email|letter|phone|ring|call|complain|phrase)\b", re.I)
A_NAMING_ASK = re.compile(
    r"\b(?:should|shall|will|would|can|could|do|to) (?:i|we|you) (?:call|name)\b|"
    r"\b(?:call|name) (?:it|him|her|them)\b", re.I)
A_PLACE_WORD = frozenset(("work", "school", "college", "hospital", "bank", "town", "city",
                          "flat", "flats", "home", "house", "garage"))
A_DETERMINER = frozenset(("a", "an", "the", "my", "our", "your", "his", "her", "their", "this"))
A_PLACE_PREP = frozenset(("at", "to", "from", "in", "into", "near", "off", "for", "of", "on"))
A_EXPLANATION = re.compile(r"\b(?:thats why|that is why|because|so that|the reason)\b", re.I)
A_NEEDS_A_NEIGHBOUR = {
    "washing": frozenset(("machine", "machines", "powder", "liquid", "detergent", "basket",
                          "line", "drum", "load", "cycle")),
}
A_SHOWN_AS = {"washing": "washing machine", "sacked": "job"}
A_ITS_OWN_SUBJECT = re.compile(
    r"\b(?:little one|little man|youngest|eldest|oldest|the baby)\b"
    r"|\b(?:he|she|they|him|her|them|son|daughter|child|kid|boy|girl)\b[^?]{0,12}\b\d+\b",
    re.I)
A_DVLA_WORD = re.compile(r"\b(?:mot|dvla|tax|sorn|licence|license|log ?book|v5|clamped)\b", re.I)
WHO_CAR_GARAGE = "a garage will tell you over the phone"

A_LIGHT_KEY = frozenset(("leave", "pay", "order", "booking", "paint", "drill", "work", "delivery",
                         "bid", "invoice", "credit", "deal", "cover", "fill", "charge", "term"))

STOP = frozenset("""
a an the and or but if so then than that this those these i me my mine you your yours we us our he
she it they them him her his hers their there here what which who whom whose when where why how do
does did done doing is are was were be been being am have has had having will would can could
should shall may might must not no nor yes ok okay just also too very really quite about for with
without on in into at by from to of as up down out off over under again more most much many any
some all both each either neither other another same such own only ever never always still yet
already even though although because while since until before after during against between among
right well thing things stuff get got give take make made say said tell told want wanted need
needed like liked know knew think thought feel felt go going went come came back put let try tried
use used find found work works working day days time times week weeks month months year years one
two three four five six seven eight nine ten bit lot lots sort kind way ways now today tomorrow
yesterday please thanks thank hi hello hey yeah yep nope um uh oh ah eh due anyway gonna wanna dont
doesnt didnt isnt wasnt cant couldnt wouldnt shouldnt havent hasnt im ive id ill youre youve theyre
thats whats heres theres whose wont
""".split())

KINDS = (
    ("tenancy", ("landlord", "tenancy", "tenant", "tenants", "deposit", "eviction", "lease",
                 "letting", "lettings", "rent", "flat", "flats")),
    ("pet", ("vet", "puppy", "puppies", "kitten", "kittens", "dog", "dogs", "cat", "cats",
             "rabbit", "rabbits", "hamster", "guinea", "parrot", "fleas", "flea", "litter")),
    ("car", ("mot", "tyre", "tyres", "brake", "brakes", "clutch", "gearbox", "engine", "battery",
             "batteries", "hybrid", "mileage", "garage", "mechanic", "dvla", "car", "cars")),
    ("bills", ("bill", "bills", "electric", "electricity", "energy", "supplier", "meter",
               "standing", "tariff", "direct", "debit", "arrears")),
    ("health", ("prescription", "pharmacist", "pharmacy", "symptom", "symptoms", "migraine",
                "infection", "swelling", "swollen", "rash", "piles", "pain", "dose", "tablets",
                "tablet", "medicine", "doctor", "hospital", "nurse", "clinic", "surgery")),
    ("work", ("sacked", "redundancy", "disciplinary", "warning", "rota", "shift", "shifts",
              "overtime", "payslip", "employer", "manager", "boss", "hr", "union", "interview",
              "contract", "job", "workplace", "work", "leave")),
    ("school", ("gcse", "gcses", "a-level", "a-levels", "exam", "exams", "revision", "homework",
                "teacher", "lesson", "lessons", "school", "college", "university", "ucas",
                "course", "term", "paper", "papers")),
    ("home", ("boiler", "radiator", "radiators", "thermostat", "dishwasher", "washer", "washing",
              "fridge", "freezer", "oven", "hob", "toilet", "shower", "leak", "leaking", "damp",
              "mould", "ceiling", "roof", "gutter", "gutters", "socket", "wiring", "plumber",
              "electrician", "limescale", "drain", "drains", "filter", "pump", "tap", "taps")),
    ("diy", ("curtain", "curtains", "rail", "drill", "shelf", "shelves", "paint", "wall", "walls",
             "screw", "screws", "rawplug", "rawplugs", "tile", "tiles", "tiling", "grout",
             "sanding", "filler", "sealant", "flatpack")),
    ("travel", ("passport", "visa", "boarding", "luggage", "suitcase", "adapter", "plug",
                "flight", "flights", "airport", "hotel", "train", "booking", "holiday",
                "abroad", "japan", "spain", "france", "italy", "greece", "portugal", "germany",
                "holland", "turkey", "egypt", "mexico", "canada", "america", "australia",
                "ireland", "scotland", "wales", "england", "london", "paris", "rome", "madrid",
                "lisbon")),
    ("shopping", ("receipt", "refund", "returns", "warranty", "guarantee", "seller", "order",
                  "delivery", "shop", "store")),
    ("money", ("overdraft", "mortgage", "loan", "loan", "benefits", "universal", "pension",
               "savings", "debt", "invoice", "bill", "bills", "tax", "salary", "wages", "wage",
               "pay", "bank", "credit", "budget", "money")),
)

PLACES = frozenset((
    "japan", "spain", "france", "italy", "greece", "portugal", "germany", "holland", "turkey",
    "egypt", "mexico", "canada", "america", "australia", "ireland", "scotland", "wales",
    "england", "london", "manchester", "birmingham", "edinburgh", "cardiff", "belfast",
    "dublin", "paris", "rome", "madrid", "lisbon", "new", "york", "florida", "california",
))

A_PASSPORT_WORD = frozenset(("passport", "passports", "visa", "visas"))
WHO_PASSPORT = "gov.uk's own page states it, and the passport office will confirm it on the phone"
A_THING_VERB_ASK = re.compile(
    r"\b(?:renew|renewing|cancel|cancelling|canceled|refund|rebook|upgrade|print|return)\b",
    re.I)

WHO = {
    "tenancy": "Shelter's advice line or your council's tenancy team will tell you what the rule "
               "is",
    "pet": "your vet's reception will answer that in one call, and the breeder or rescue you got "
           "them from knows the rest",
    "car": "a garage will tell you over the phone, and the DVLA's own page has the rule",
    "bills": "your supplier will say what their own rules are, and Citizens Advice has the free "
             "script for asking them",
    "health": "a pharmacist will settle it across the counter, and 111 if it cannot wait",
    "work": "ACAS will tell you where you stand in one free call, and your contract says what "
            "was agreed",
    "school": "the school office will tell you, and the exam board's specification says it in "
              "writing",
    "home": "the manual for that model says what it does, and a plumber will confirm it on the "
            "phone",
    "diy": "the instructions that came with it say, and anyone behind the counter at a builders' "
           "merchant will tell you",
    "travel": "the operator's own site states it, and the airline or the hotel will confirm it "
              "in a message",
    "shopping": "the shop's own page states it, and their chat will confirm it in writing",
    "money": "your bank or the office that runs it has the exact rule in writing",
}

SHAPES = {
    "howlong": "{subject}, then. {on} I can't put a time on that from here; {who}.",
    "yesno": "{subject}, then. {on} I can't say yes or no from here; {who}.",
    "how": "{subject}, then. {on} I can't talk you through it without seeing it; {who}.",
    "what": "{subject}, then. {on} That one is past what I know well; {who}.",
    "words": "{subject}, then. Keep it to three lines, say what you want and by when; {who}.",
    "howmuch": "I haven't got a figure for {subject}, and a guessed one is worse than none. "
               "{on} {who}.",
}


A_OPEN_ASK = re.compile(
    r"\bwhat (?:do|should|shall|can|could|would) (?:i|we|you|they) do\b|"
    r"\bwhat (?:happens|now|next)\b|\bwhat does (?:that|it|this) mean\b", re.I)
A_KNOWS_IT = 0.6
A_WORD = re.compile(r"[a-z0-9']+")
A_TURNS_ON = {
    "tenancy": "what settles it is the agreement and what is in writing",
    "pet": "what settles it is the age and the breed",
    "car": "what settles it is the age, the mileage and the last MOT",
    "bills": "what settles it is the account and what the supplier has already been told",
    "health": "what settles it is how long it has gone on and what has already been tried",
    "work": "what settles it is the dates and what was put in writing",
    "school": "what settles it is the subject, the board and the dates",
    "home": "what settles it is the model and when it started",
    "diy": "what settles it is the size and what it is fixed to",
    "travel": "what settles it is the booking reference and the dates",
    "shopping": "what settles it is the receipt and the date you bought it",
    "money": "what settles it is the account and the figures",
}


def _words(line):
    return re.findall(r"[a-z']+", str(line or "").lower())


def _bare_follow_up(clean):
    text = " ".join(str(clean or "").lower().split())
    if not text or len(_words(text)) > 8:
        return None
    if not (A_ASK_OPENER.match(text) or text.rstrip().endswith("?")):
        return None
    subject = [w for w in _words(text) if w not in STOP and len(w) > 2]
    if len(subject) > A_SUBJECT_WORD_LIMIT:
        return None
    if not A_BACK_REFERENCE.search(text):
        if (len(subject) > A_EMPTY_ASK_WORDS or len(_words(text)) > A_EMPTY_ASK_LENGTH
                or not A_EMPTY_ASK_OPENER.match(text)):
            return None
    return text


def _stem(word):
    word = str(word or "").lower().strip("'")
    for suffix in ("ing", "ies", "ied", "es", "ed", "s"):
        if len(word) > len(suffix) + 2 and word.endswith(suffix):
            word = word[:-len(suffix)]
            break
    if len(word) > 3 and word.endswith("e"):
        word = word[:-1]
    return word


def _only_a_place(words, index):
    before = words[index - 1] if index > 0 else ""
    if before in A_PLACE_PREP:
        return True
    if before in A_DETERMINER and index > 1 and words[index - 2] in A_PLACE_PREP:
        return True
    return False


def _beside(words, index, allowed):
    if index > 0 and words[index - 1] in allowed:
        return True
    return index + 1 < len(words) and words[index + 1] in allowed


def _named(line, skip_place_words=False, light=True):
    words = _words(line)
    said = {}
    for index, word in enumerate(words):
        said.setdefault(_stem(word), []).append(index)
    found = []
    for kind, keys in KINDS:
        for key in keys:
            places = said.get(_stem(key))
            if not places:
                continue
            if light and key in A_LIGHT_KEY:
                continue
            neighbour = A_NEEDS_A_NEIGHBOUR.get(key)
            if neighbour and not any(_beside(words, index, neighbour) for index in places):
                continue
            if skip_place_words and key in A_PLACE_WORD and all(
                    _only_a_place(words, index) for index in places):
                continue
            found.append((key, kind))
            break
    return found


def _the_subject(memory, clean=""):
    now = " ".join(str(clean or "").lower().split())
    lines = []
    topic = memory.get("topic") if isinstance(memory, dict) else None
    if isinstance(topic, dict) and topic.get("text"):
        said = " ".join(str(topic["text"]).lower().split())
        if said and said != now:
            lines.append(str(topic["text"]))
    turns = list(memory.get("turns") or []) if isinstance(memory, dict) else []
    for turn in reversed(turns[-5:]):
        if not isinstance(turn, dict) or not turn.get("user"):
            continue
        said = " ".join(str(turn["user"]).lower().split())
        if said and said != now:
            lines.append(str(turn["user"]))
    said_things = []
    for turn in reversed(turns):
        if not isinstance(turn, dict) or not turn.get("user"):
            continue
        said = " ".join(str(turn["user"]).lower().split())
        if not said or said == now or A_A_QUESTION_ASK.match(said):
            continue
        if A_EXPLANATION.search(said):
            continue
        said_things.append(str(turn["user"]))
        if len(said_things) == 2:
            break
    if not said_things:
        return "", "", ""
    newest = _named(said_things[0], skip_place_words=True)
    if len({kind for _word, kind in newest}) > 1:
        for word, kind in _named(now, skip_place_words=True):
            if kind in {named_kind for _word, named_kind in newest}:
                return word, kind, now
    for line in said_things:
        named = _named(line, skip_place_words=True)
        if named:
            word, kind = named[0]
            return word, kind, line
    return "", "", ""


def _already_the_who(word, kind):
    stem = _stem(word)
    return any(_stem(each) == stem for each in _words(WHO.get(kind) or ""))


def _beside_the_who(line, kind, subject):
    keys = dict(KINDS).get(kind) or ()
    by_stem = {}
    for key in keys:
        by_stem.setdefault(_stem(key), key)
    for word in _words(line):
        key = by_stem.get(_stem(word))
        if not key or key == subject or key in A_LIGHT_KEY or key in PLACES:
            continue
        if _already_the_who(key, kind):
            continue
        return key
    return ""


def _shape(text):
    if A_WORDS_ASK.match(text):
        return "words"
    if re.search(r"\bhow long\b", text) or re.search(r"\bhow soon\b", text):
        return "howlong"
    if re.search(r"\bhow much\b", text) or re.search(r"\bhow many\b", text):
        return "howmuch"
    if re.match(r"^\s*how\b", text):
        return "how"
    if re.match(r"^\s*(?:what|which|who|when|where)\b", text):
        return "what"
    return "yesno"


def _content(text):
    return [word for word in A_WORD.findall(str(text or "").lower()) if len(word) > 3]


def _already_said(sentence, memory):
    mine = _content(sentence)
    if not mine:
        return True
    seen = set()
    turns = memory.get("turns") if isinstance(memory, dict) else None
    for turn in list(turns or [])[-3:]:
        if isinstance(turn, dict):
            seen.update(_content(turn.get("bot")))
    if not seen:
        return False
    return sum(1 for word in mine if word in seen) >= A_KNOWS_IT * len(mine)


def _one_sentence(text, limit=250):
    said = " ".join(str(text or "").split())
    stop = said.find(". ")
    if 40 < stop < limit:
        said = said[:stop + 1]
    if len(said) > limit:
        cut = said.rfind(", ", 0, limit - 3)
        if cut < 100:
            cut = said.rfind(" ", 0, limit - 3)
        said = said[:max(cut, 100)].rstrip(" ,;:-") + ", and"
    for opener in ('"', "(", "["):
        if said.count(opener) % 2:
            at = said.rfind(opener)
            if at > 40:
                said = said[:at].rstrip(" ,;:-")
    return said


def _cap(clause):
    clause = str(clause or "")
    return clause[0].upper() + clause[1:] if clause else clause


A_THERE = re.compile(r"\bthere\b", re.I)
A_NOT_A_PLACE = frozenset((
    "january", "february", "march", "april", "may", "june", "july", "august", "september",
    "october", "november", "december", "jan", "feb", "mar", "apr", "jun", "jul", "aug", "sep",
    "sept", "oct", "nov", "dec", "monday", "tuesday", "wednesday", "thursday", "friday",
    "saturday", "sunday", "week", "weeks", "weekend", "month", "months", "year", "years", "day",
    "days", "morning", "afternoon", "evening", "night", "spring", "summer", "autumn", "winter",
    "a", "an", "the", "my", "our", "your", "his", "her", "their", "this", "that", "these",
    "those", "it", "them", "all", "some", "any", "no", "one", "two", "three", "ten", "twenty",
    "future", "past", "total", "general", "fact", "particular", "touch", "writing", "person",
    "which", "what", "order", "case", "time", "front", "bed", "hospital", "work", "school",
))
A_NAMED_PLACE = re.compile(r"\b(?:in|to|at|from|visiting|visit)\s+([a-z][\w'-]*)", re.I)
A_REPEAT_LEAD = re.compile(r"^same (?:as before|answer)\b[^:]{0,40}:", re.I)
A_EXISTENTIAL_THERE = re.compile(
    r"\b(?:is|are|was|were|isn't|aren't|wasn't|weren't)\s+there\b|\bthere(?:'s| is| are| was| were)\b",
    re.I)


def _the_place(line):
    for match in A_NAMED_PLACE.finditer(str(line or "").lower()):
        word = match.group(1)
        if word not in A_NOT_A_PLACE and word not in STOP and len(word) > 2:
            return word
    return None


def _the_answer_about_the_place(text, line, memory):
    if not A_THERE.search(text):
        return ""
    if A_EXISTENTIAL_THERE.search(text) or _shape(text) == "howlong":
        return ""
    place = _the_place(line)
    if not place:
        return ""
    spliced = A_THERE.sub("in " + place, text, count=1)
    chat = memory if isinstance(memory, dict) else {}
    clean = {"turns": [turn for turn in (chat.get("turns") or []) if isinstance(turn, dict)]}
    try:
        from . import fallback
        from ..modules import answers
        answer = answers.respond(spliced, clean)
    except Exception:
        return ""
    if not answer or not str(answer).strip():
        return ""
    from . import fallback
    if fallback._in_a_pool(str(answer), (fallback.UNKNOWN,)):
        return ""
    first = _one_sentence(str(answer))
    rest = str(answer)[len(first):].strip()
    second = _one_sentence(rest)
    said = (first + (" " + second if second else "")).strip()
    if A_REPEAT_LEAD.match(said):
        return ""
    if place.lower() not in said.lower():
        return ""
    return said


def _what_it_knows(line, memory):
    line = " ".join(str(line or "").split())
    if not line:
        return ""
    try:
        from ..knowledge import lookup
        from ..understanding import understand
        from . import fallback
        reading = understand(line)
        entry = lookup.find(reading)
        if entry is None:
            return ""
        answer = entry.reply
        if callable(answer):
            answer = answer({}, reading)
        if not isinstance(answer, str) or not answer.strip():
            return ""
        if fallback._in_a_pool(answer, (fallback.UNKNOWN,)):
            return ""
    except Exception:
        return ""
    for sentence in re.split(r"(?<=[.!?])\s+", " ".join(answer.split())):
        if len(sentence) < 40 or _already_said(sentence, memory):
            continue
        return _one_sentence(sentence)
    return ""


def _the_line_before(chat, now):
    for turn in reversed(list(chat.get("turns") or [])[-3:]):
        if not isinstance(turn, dict) or not turn.get("user"):
            continue
        said = str(turn["user"])
        if " ".join(said.lower().split()) == now:
            continue
        if _the_place(said):
            return said
    return ""


def place_pool(clean, understood=None, memory=None):
    text = _bare_follow_up(clean)
    if text is None or not A_THERE.search(text) or A_EXISTENTIAL_THERE.search(text):
        return None
    if _shape(text) == "howlong":
        return None
    if A_POINTER_ASK.match(text) or A_HELP_ASK.match(text) or A_JUDGEMENT_ASK.search(text):
        return None
    if A_RECALL_ASK.search(text) or A_COMPARISON_ASK.search(text) or A_COOKING_ASK.search(text):
        return None
    if A_NAMING_ASK.search(text) or A_ITS_OWN_SUBJECT.search(text):
        return None
    chat = memory if isinstance(memory, dict) else {}
    try:
        from . import fallback
        if not fallback._in_a_pool(fallback.reply_for(clean, chat), (fallback.UNKNOWN,)):
            return None
    except Exception:
        return None
    line = _the_line_before(chat, text)
    if not line:
        return None
    answer = _the_answer_about_the_place(text, line, chat)
    place = _the_place(line)
    if not answer or not place:
        return None
    return "%s, then. %s" % (_cap(place), answer)


def _food_above(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    for turn in (turns or [])[-6:]:
        if not isinstance(turn, dict):
            continue
        said = str(turn.get("user") or "")
        if A_COOKING_ASK.search(said) or A_NAMED_FOOD.search(said) or A_ROASTING_WORD.search(said):
            return True
    return False


def pool(clean, understood=None, memory=None):
    text = _bare_follow_up(clean)
    if text is None:
        return None
    if A_POINTER_ASK.match(text) or A_HELP_ASK.match(text) or A_JUDGEMENT_ASK.search(text):
        return None
    if A_NAMING_ASK.search(text):
        return None
    if A_ITS_OWN_SUBJECT.search(text):
        return None
    subject = _the_subject(memory or {}, text)[0]
    if not subject and A_COOKING_TIME_ASK.search(text) and A_FOOD_PRONOUN.search(text) \
            and not A_NAMED_FOOD.search(text) and not _food_above(memory or {}):
        if A_ROASTING_WORD.search(text):
            return COOKING_TIME_SHAPES["oven"]
        if A_BOILING_WORD.search(text):
            return COOKING_TIME_SHAPES["boil"]
        if A_COOKING_ASK.search(text) and not A_OTHER_METHOD.search(text):
            return COOKING_TIME_SHAPES["either"]
    if A_RECALL_ASK.search(text) or A_COMPARISON_ASK.search(text) or A_COOKING_ASK.search(text):
        return None
    subject, kind, line = _the_subject(memory or {}, text)
    if not subject:
        return None
    if line != text:
        mine = [named_kind for _word, named_kind in _named(text, skip_place_words=True)]
        if mine and kind not in mine:
            return None
    who = WHO.get(kind)
    if not who:
        return None
    if kind in AMOUNT_KINDS and A_JUDGEMENT_OF_AMOUNT.search(text):
        return None
    if kind in MACHINE_BEFORE_MACHINE_KINDS and A_MACHINE_CUE.search(line):
        return None
    if A_LOST_THING.search(str(line or "")):
        return None
    if _already_the_who(subject, kind):
        subject = _beside_the_who(line, kind, subject) or subject
    if subject in PLACES and A_THING_VERB_ASK.search(text):
        return None
    if subject in A_PASSPORT_WORD:
        who = WHO_PASSPORT
    if kind == "car" and not (A_DVLA_WORD.search(text) or A_DVLA_WORD.search(str(line or ""))):
        who = WHO_CAR_GARAGE
    said = subject if subject in PLACES else "the " + A_SHOWN_AS.get(subject, subject)
    shape_kind = _shape(text)
    shape = SHAPES[shape_kind]
    if shape.startswith("{subject}"):
        said = said[0].upper() + said[1:]
    known = ""
    if A_OPEN_ASK.search(text) and not _named(text, skip_place_words=True):
        known = _what_it_knows(line, memory or {})
    whole = ""
    if not known:
        whole = _the_answer_about_the_place(text, line, memory or {})
    if whole:
        return f"{said}, then. {whole}"
    if known:
        ends = known[-1:] in ".!?"
        join = " " if ends else "; "
        place = _cap(who) if ends else who
        if shape_kind == "howmuch":
            return (f"I haven't got a figure for {said}, and a guessed one is worse than none - "
                    f"{known}{join}{place}.")
        return f"{said}, then. {known}{join}{place}."
    turns_on = A_TURNS_ON.get(kind)
    on = ""
    if turns_on and shape_kind != "words":
        on = turns_on[0].upper() + turns_on[1:] + "."
    reply = shape.format(subject=said, on=on, who=who)
    return re.sub(r"\s+", " ", reply).replace(" .", ".").strip()
