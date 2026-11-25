import re
try:
    from ..memory import dream as _DREAM
except Exception:
    _DREAM = None
import string

SLIPS = {}

from ..understanding import lexicon
from ..understanding.normalize import LEXICON as COMMON_WORDS
from ..understanding.normalize import TIME_WORDS

GRAMMAR_ONLY = frozenset((
    "a", "an", "the", "and", "or", "but", "if", "so", "as", "at", "by", "for", "from", "in",
    "into", "of", "on", "onto", "over", "under", "to", "up", "with", "without", "about",
    "after", "before", "than", "then", "that", "this", "these", "those", "it", "its", "is",
    "are", "was", "were", "be", "been", "being", "am", "do", "does", "did", "doing", "done",
    "can", "could", "should", "would", "will", "shall", "may", "might", "must", "not", "no",
    "yes", "ok", "okay", "alright", "just", "also", "too", "very", "really", "quite", "more",
    "most", "much", "many", "any", "all", "some", "none", "every", "each", "i", "me", "my",
    "mine", "we", "us", "our", "you", "your", "he", "him", "his", "she", "her", "they",
    "them", "their", "there", "here", "when", "where", "what", "which", "who", "how", "why",
    "have", "has", "had", "having", "get", "gets", "getting", "got", "go", "goes", "going",
    "went", "give", "gives", "gave", "giving", "take", "takes", "took", "taking", "make",
    "makes", "made", "making", "eat", "eats", "ate", "eating", "eaten", "drink", "drinks",
    "drank", "drinking", "drunk", "again", "still", "always", "never", "sometimes", "often",
    "now", "today", "tonight", "yesterday", "tomorrow", "lot", "lots", "loads", "bit", "kind",
    "sort", "one", "ones", "thing", "things", "time", "times", "day", "week", "month", "year",
))


def names_a_thing(phrase):
    words = [word for word in re.split(r"[^a-z0-9']+", str(phrase or "").lower()) if word]
    return any(word not in GRAMMAR_ONLY and not word.isdigit() for word in words)

WORD = re.compile(r"[a-z0-9]+(?:'[a-z]+)?")

try:
    re._MAXCACHE = max(getattr(re, "_MAXCACHE", 512), 16384)
except Exception:
    pass

ASKING_MODALS = frozenset("can could would should may might must shall will".split())
ASKING_SUBJECTS = frozenset("i you we they he she it u".split())


def _asking_with(typed, at):
    if typed[at] not in ASKING_MODALS:
        return False
    if at + 1 < len(typed) and typed[at + 1] in ASKING_SUBJECTS:
        return True
    return at > 0 and typed[at - 1] in ASKING_SUBJECTS

MIN_SCORE = 4

MODAL_PHRASES = {
    "will": ("a will", "my will", "the will", "in the will", "their will", "write a will",
             "will and testament"),
    "can": ("can of", "cans of", "a can", "the can"),
    "cans": ("cans of", "some cans", "two cans", "three cans"),
}

FEELING_WORDS = (
    "panic", "panics", "panicking", "panicky", "panic attack", "panic attacks",
    "anxious", "anxiety", "worried", "worry", "worrying", "worries", "nervous", "on edge",
    "stressed", "stress", "stressing", "overwhelmed", "overwhelming", "freaking out",
    "depressed", "depression", "low mood", "feel low", "feeling low", "feels low", "feeling flat",
    "miserable", "crying", "cry", "tearful", "upset", "dreading", "dread", "hopeless",
    "exhausted", "drained", "burnt out", "burned out", "burnout", "fed up", "cant cope",
    "can't cope", "breaking down", "angry", "anger", "frustrated", "irritable", "snappy",
)

ASK_ABOUT = ("what", "how", "do", "can", "should", "help", "anything", "advice", "tips",
             "get rid", "rid", "stop", "treat", "treatment", "cure", "relief", "relieve", "ease",
             "prevent", "best", "works", "work", "deal with", "cope", "worse", "helps")
ORIGIN_ASK = ("come from", "comes from", "came from", "come out of", "comes out of",
              "made from", "made of", "made out of", "made with", "where from",
              "is grown", "grown in", "grows on", "is mined", "is produced")

NOT_A_NOSE = ("through my nose", "through your nose", "through his nose", "through her nose",
              "through their nose", "through the nose", "blocked nose", "blocked up nose",
              "stuffy nose", "bunged up nose", "nose is blocked", "nose is stuffy",
              "nose is bunged", "congested nose")


TOOTH_OUT = ("tooth out", "teeth out", "tooth removed", "teeth removed", "tooth pulled",
             "tooth extraction", "extractions", "tooth taken out", "teeth taken out",
             "had a tooth", "had my tooth", "had two teeth", "gap where", "where my tooth",
             "where the tooth", "the socket", "dry socket", "wisdom tooth out",
             "wisdom teeth out", "wisdom tooth removed", "after the extraction",
             "after my extraction", "after a tooth")

TOOTH_OR_GUM = ("tooth", "teeth", "toothache", "filling", "fillings", "gum", "gums", "molar",
                "molars", "dentist", "dentists", "dental", "denture", "dentures", "enamel",
                "wisdom tooth", "wisdom teeth", "braces", "mouth ulcer", "gumline")

WORD_WEIGHT = 2
PHRASE_WEIGHT = 3

_SAVING_VERB = re.compile(
    r"\b(?:save|saves|saving|saved|put\s+away|putting\s+away|put\s+by|putting\s+by|"
    r"set\s+aside|setting\s+aside|afford|affords|affording)\b", re.I)
_SAVING_FOR_A_TRIP = re.compile(
    r"\bfor\s+(?:a|an|the|my|our|their|your|his|her|this|next)?\s*"
    r"(?:holiday|holidays|trip|trips|break|weekend\s+away|city\s+break|getaway)\b", re.I)


_AFFORD_THE_TRIP = re.compile(
    r"\bafford\b[^.;!?]{0,25}?\b(?:holiday|holidays|trip|breaks?|getaway)\b", re.I)


def saving_for_a_trip(understood):
    line = (understood or {}).get("clean") or (understood or {}).get("text") or ""
    if _AFFORD_THE_TRIP.search(line):
        return False
    return not (_SAVING_VERB.search(line) and _SAVING_FOR_A_TRIP.search(line))

PRESENT_ASK = (
    "gift", "gifts", "present", "presents", "gift idea", "gift ideas", "present idea",
    "present ideas", "christmas present", "christmas gift", "birthday present", "birthday gift",
    "what should i get", "what can i get", "what do i get", "what to get",
    "what should i buy", "what can i buy", "what do i buy", "what to buy",
    "what should i give", "what can i give", "what do i give", "what to give",
    "what would you get", "what would you buy", "what would you give",
    "get him", "get her", "get them", "buy him", "buy her", "buy them", "give him", "give her",
    "for his birthday", "for her birthday", "for their birthday",
    "for his christmas", "for her christmas", "for their christmas",
)

IMPROVE = ("get better at", "better at", "get better", "better", "improve", "improving",
           "improve my", "improvement", "sort out", "sort out my", "sort myself out",
           "work on", "work on my", "get good at", "good at", "get the hang of", "brush up on",
           "practise", "practice", "sharpen up")

HOW_OFTEN_WORDS = ("how often", "how frequently", "how regularly", "how many times", "often",
                   "frequently", "regularly", "how long between", "every how long", "frequency")


def the_line(understood):
    understood = understood or {}
    return " ".join(str(understood.get(key) or "")
                    for key in ("clean", "norm_text", "plain")).lower()


def said_text(understood):
    if not isinstance(understood, dict):
        return ""
    for key in ("words", "norm"):
        taken = understood.get(key)
        if isinstance(taken, str) and taken.strip():
            return taken
        if isinstance(taken, (list, tuple)) and taken:
            return " ".join(str(word) for word in taken)
    return ""


def guard_passes(item, reading):
    guard = getattr(item, "guard", None)
    if guard is None:
        return True
    try:
        return bool(guard(reading))
    except Exception:
        return False


def asks_how_often(understood):
    said = understood if isinstance(understood, str) else the_line(understood)
    return any(word in said for word in HOW_OFTEN_WORDS)


SANDING_JOB = re.compile(
    r"\bsanding\b|\bsanded\b|\bsandpaper\b|\bsand paper\b|\bsander\b|\bsanders\b"
    r"|\b(?:need|needs|needed|should|must|can|could|shall|will|would|got|better|have to|has to)"
    r"\s+(?:i\s+)?(?:to\s+)?sand\b"
    r"|\bto sand\b|\ba sand\b"
    r"|\bsand (?:it|them|this|that|down|off|back|first|before|after|with"
    r"|the wall|the walls|the wood|the floor|the door|the doors|the ceiling|the trim|the edges?)\b"
    r"|\bfiller\b|\bfilled and sanded\b|\bpolyfilla\b|\bwood filler\b|\bfilling knife\b", re.I)


def a_sanding_job(understood):
    said = understood if isinstance(understood, str) else the_line(understood)
    return bool(SANDING_JOB.search(said))


SAID_LEADS = ("im", "i am", "im really", "im so", "im very", "im all", "ive been", "ive got", "i have",
              "i have been", "i feel", "feel", "i keep getting", "i keep being", "i get")


def said(*words, leads=SAID_LEADS):
    return tuple(f"{lead} {word}" for word in words for lead in leads)


_WRAPPED = (
    re.compile(r"^(?:and |so |ok |okay |hi |hello )?(?:what|anything|something)\s+"
               r"(?:should|can|could|would|do|will|shall)\s+i\s+"
               r"(?:do|use|try|take|put|buy)\s+(?:about|for|on)\s+(?P<subject>\S.*?)\s*\??$"),
    re.compile(r"^(?:and |so )?(?:what|anything)\s+(?:helps|works|is good)\s+"
               r"(?:for\s+|with\s+)?(?P<subject>\S.*?)\s*\??$"),
    re.compile(r"^(?:and |so )?(?:any|some|got any|have you got any|do you have any)\s+"
               r"(?:tips|advice|suggestions|ideas)\s+(?:for|on|with|about)\s+(?P<subject>\S.*?)\s*\??$"),
    re.compile(r"^(?P<subject>\S.*?)[,;:]?\s+(?:what|anything)\s+(?:helps|works)\s*\??$"),
)
_NOT_A_SUBJECT = frozenset(
    "a an the my your our their his her its it that this these those me us him them someone "
    "anyone everyone something anything nothing more less best good now then here there".split())
_NOT_A_THING = frozenset(("a living", "a go", "a bit", "a while", "a change", "the best",
                          "my best", "a start", "the same", "a look", "a hand", "a try",
                          "a break", "a rest", "for good", "the day", "the weekend",
                          "it", "that", "this", "them", "anything"))

ASK_FRAME_IDS = frozenset("""
    condensation damp limescale slug-control snoring snore-less hangover sore-throat
    sleep-trouble
    """.split())

AS_A_KIND = frozenset("something anything nothing everything".split())

MIN_TYPO_LENGTH = 4

RING_AS_A_CALL = (
    "ring the", "ring my", "ring him", "ring her", "ring them", "ring you", "ring me",
    "ring someone", "ring somebody", "ring anyone", "ring anybody", "ring people",
    "ringing someone", "ringing somebody", "ringing people", "rang someone", "rang somebody",
    "ring a", "ring an", "ring about", "ring back", "ring up", "ring round", "ring around",
    "ring for", "ring to", "ring at", "ring and", "ring later", "ring tomorrow",
    "ring in", "ring sick", "ring ahead", "ring work", "ring first thing",
    "ring first", "ring instead", "ring again", "to ring", "should ring", "will ring",
    "can ring", "could ring", "would ring", "might ring", "must ring", "need to ring",
    "have to ring", "give a ring", "give her a ring", "give him a ring", "give them a ring",
    "give me a ring", "a ring round")

ENDINGS = ("iness", "iest", "ings", "ing", "ies", "ied", "ier", "ers", "est", "er",
           "es", "ed", "ly", "s", "y", "ness", "ful")
MIN_FORM = 3


class Entry:

    __slots__ = ("id", "key", "reply", "avoid", "bias", "ask", "slips", "domain", "fault",
                 "report", "guard", "shape", "explain", "lead", "outcomes")

    def __init__(self, id, key, reply, avoid=(), bias=0, ask=(), slips=(), fault=False,
                 report=False, guard=None, shape=(), explain=False, lead="", outcomes=()):
        self.id = id
        self.key = tuple(key)
        self.reply = reply
        self.avoid = tuple(avoid)
        self.bias = bias
        self.ask = tuple(ask)
        self.slips = tuple(slips)
        self.domain = ""
        self.fault = fault
        self.report = report
        self.guard = guard
        self.shape = tuple(shape)
        self.explain = explain
        self.lead = lead
        self.outcomes = tuple(outcomes)

    def __repr__(self):
        return f"<Entry {self.id}>"


PLACES_AFTER_BACK = (r"door|doors|fence|fences|gate|gates|gatepost|gateposts|garden|gardens|"
                     r"room|rooms|seat|seats|window|windows|wall|walls|yard|porch|lawn|path|"
                     r"pathway|step|steps|stairs|packet|packets|pocket|pockets|burner|burners|"
                     r"boiler|panel|panels|bed|beds|alley|bridge|road|lane|field|fields|"
                     r"paddock|plot|car|van|shed|garage|drive|driveway|garden")
BACK_OF_THE_HOUSE = re.compile(r"\bback\s+(?:%s)\b" % PLACES_AFTER_BACK)
THE_BACK_ITSELF = re.compile(
    r"\b(?:my|your|his|her|their|our|the|lower|upper|sore|stiff|aching|aching|bad|old)\s+"
    r"back\b(?!\s+(?:%s)\b)" % PLACES_AFTER_BACK)


APPLIANCE_NAMES = (
    "tumble dryer", "washer dryer", "heat pump dryer", "condenser dryer", "vented dryer",
    "washing machine", "fridge freezer", "fish tank", "pool pump", "shower pump", "fan oven",
    "microwave", "dishwasher", "dryer", "fridge", "freezer", "oven", "cooker", "hob", "kettle",
    "toaster", "vacuum", "hoover", "mower", "lawnmower", "strimmer", "radiator", "boiler",
    "car", "van", "motorbike", "bike", "bicycle", "aquarium", "hot tub")


def the_appliance_swallows_the_name(understood, names):
    parts = [str((understood or {}).get(part) or "") for part in ("clean", "text", "norm")]
    said = " " + " ".join(parts).lower() + " "
    names = [str(name).lower() for name in (names or ()) if str(name or "").strip()]
    if not names:
        return False
    for appliance in APPLIANCE_NAMES:
        if not re.search(r"(?<![a-z0-9])" + re.escape(appliance) + r"(?![a-z0-9])", said):
            continue
        if any(name in appliance and len(name) < len(appliance) for name in names):
            return True
    return False


def the_back_is_a_body_part(understood):
    said = str((understood or {}).get("text") or "").lower()
    above = str(((understood or {}).get("leans_on") or {}).get("text") or "").lower()
    both = said + " " + above
    if not BACK_OF_THE_HOUSE.search(both):
        return True
    return bool(THE_BACK_ITSELF.search(both))


def _avoid_words(parts):
    flat = []
    for part in parts:
        if isinstance(part, str):
            flat.extend(MODAL_PHRASES.get(part, (part,)))
        elif isinstance(part, (list, tuple, set, frozenset)):
            flat.extend(_avoid_words(part))
    return tuple(flat)


PEOPLE_MALE = ("dad", "father", "grandad", "grandpa", "grandfather", "stepdad", "brother",
               "husband", "boyfriend", "son", "uncle", "nephew", "bloke", "fella", "guy",
               "he", "him", "his")
PEOPLE_FEMALE = ("mum", "mother", "mam", "nan", "nana", "gran", "granny", "grandma",
                 "grandmother", "stepmum", "sister", "wife", "girlfriend", "daughter", "aunt",
                 "niece", "she", "her", "hers")


def about_them(template, male=PEOPLE_MALE, female=PEOPLE_FEMALE):
    def reply(memory, reading):
        words = reading.get("words") or ()
        they = "they"
        for word in words:
            if word in male:
                they = "he"
                break
            if word in female:
                they = "she"
                break
        plural = they == "they"
        fills = (("{they}", they),
                 ("{them}", "them" if plural else ("him" if they == "he" else "her")),
                 ("{their}", "their" if plural else ("his" if they == "he" else "her")),
                 ("{self}", "themselves" if plural else ("himself" if they == "he" else "herself")),
                 ("{has}", "have" if plural else "has"),
                 ("{is}", "are" if plural else "is"),
                 ("{likes}", "like" if plural else "likes"),
                 ("{loves}", "love" if plural else "loves"))
        out = template
        for token, word in fills:
            out = out.replace(token, word)
        return out[:1].upper() + out[1:]
    return reply


WHERE_PHRASES = ("where to buy", "where can i buy", "where should i buy", "where do i buy",
                 "where to get", "where can i get", "where should i get", "where do i get",
                 "cheapest place", "cheapest shop", "best place to buy", "which shop",
                 "what shop", "who sells", "where sells")


PRICE_COMPARED = ("fridge", "freezer", "fridge freezer", "washing machine", "washer dryer",
                  "tumble dryer", "dishwasher", "oven", "hob", "microwave", "kettle", "toaster",
                  "hoover", "vacuum", "tv", "television", "laptop", "phone", "tablet", "sofa",
                  "bed", "mattress", "wardrobe", "pram", "pushchair", "car seat", "bike",
                  "boiler", "mower", "lawnmower")


def asks_where(understood):
    if "where" in tuple((understood or {}).get("asks") or ()):
        return True
    words = (understood or {}).get("words") or ()
    text = " " + " ".join(str(word) for word in words).lower() + " "
    return any(phrase in text for phrase in WHERE_PHRASES)


WHERE_PART_WORDS = ("spare", "spares", "part", "parts", "replacement", "door", "doors", "seal",
                    "seals", "gasket", "filter", "filters", "basket", "baskets", "tray", "trays",
                    "drawer", "drawers", "shelf", "shelves", "handle", "handles", "hinge",
                    "hinges", "lid", "lids", "element", "elements", "drum", "drums", "belt",
                    "belts", "pump", "pumps", "motor", "motors", "fan", "fans", "blade", "blades",
                    "brush", "brushes", "hose", "hoses", "pipe", "pipes", "knob", "knobs", "bulb",
                    "bulbs", "thermostat", "compressor", "descaler", "descale", "limescale")


def asks_where_a_shop_answers(understood):
    if not asks_where(understood):
        return False
    words = [str(word).lower() for word in ((understood or {}).get("words") or ())]
    if any(word in WHERE_PART_WORDS for word in words):
        return False
    text = " " + " ".join(words) + " "
    if any(thing in text for thing in PRICE_COMPARED):
        return True
    ref = str((((understood or {}).get("ref") or {}).get("it")) or "").strip().lower()
    if not ref:
        return False
    return any(ref == thing or ref.endswith(" " + thing) for thing in PRICE_COMPARED)


THE_FAULT = (("washing machine", "washing machine"), ("tumble dryer", "tumble dryer"),
             ("tumble drier", "tumble dryer"), ("spin dryer", "tumble dryer"),
             ("dishwasher", "dishwasher"), ("fridge freezer", "fridge freezer"),
             ("fridge", "fridge"), ("freezer", "freezer"), ("microwave", "microwave"),
             ("cooker", "cooker"), ("oven", "oven"), ("hob", "hob"),
             ("central heating", "central heating"), ("heating", "heating"),
             ("hot water", "hot water"), ("radiators", "radiators"),
             ("radiator", "radiator"), ("boiler", "boiler"),
             ("shower", "shower"), ("bath", "bath"), ("toilet", "toilet"), ("loo", "toilet"),
             ("extractor fan", "extractor fan"), ("smoke alarm", "smoke alarm"),
             ("front door", "front door"), ("letterbox", "letterbox"),
             ("intercom", "intercom"), ("window frame", "window"), ("window", "window"),
             ("roof", "roof"), ("guttering", "gutter"), ("gutter", "gutter"),
             ("chimney", "chimney"), ("damp patch", "damp"), ("damp", "damp"),
             ("mould", "mould"), ("mold", "mould"), ("condensation", "condensation"),
             ("leak", "leak"), ("electrics", "electrics"), ("electric", "electrics"),
             ("plug socket", "socket"), ("socket", "socket"), ("lights", "lights"),
             ("light", "light"), ("tap", "tap"), ("sink", "sink"), ("drains", "drain"),
             ("drain", "drain"), ("pipes", "pipes"), ("pipe", "pipe"),
             ("stairs", "stairs"), ("ceiling", "ceiling"), ("floor", "floor"),
             ("wall", "wall"), ("fence", "fence"), ("lock", "lock"), ("garden", "garden"),
             ("garage", "garage"))


_BOUNDED = {}
_BOUNDED_KEEP = 40000


def _bounded(name):
    got = _BOUNDED.get(name)
    if got is not None:
        return got
    got = re.compile(r"(?<![a-z0-9])" + re.escape(name) + r"(?![a-z0-9])")
    if len(_BOUNDED) >= _BOUNDED_KEEP:
        _BOUNDED.clear()
    _BOUNDED[name] = got
    return got


def the_fault(template, when_unnamed, table=THE_FAULT):
    wanted = [(re.compile(r"\b" + re.escape(word) + r"\b"), noun)
              for word, noun in sorted(table, key=lambda pair: len(pair[0]), reverse=True)]

    def reply(memory, reading):
        line = str(reading.get("text") or reading.get("clean") or "").lower()
        for pattern, noun in wanted:
            if pattern.search(line):
                return template.replace("{fault}", noun)
        return when_unnamed
    return reply



FOOD_SUBJECT = ("sourdough", "starter", "kombucha", "kefir", "ferment", "fermented",
                "fermenting", "hooch", "dough", "bread", "beer", "wine", "vinegar", "pickle",
                "yoghurt", "yogurt", "milk", "cheese", "butter", "meat", "chicken", "fish",
                "rice", "pasta", "potato", "potatoes", "food", "foods", "drink", "drinks",
                "juice", "curry", "stew", "soup", "cake", "biscuit", "biscuits")

HAS_GONE = re.compile(r"\b(?:has|have|had|'s|s|is|was)\s+(?:gone|went)\b(.*)$")
GONE_INTENSIFIER = frozenset("""all a an really very so quite proper totally completely kind sort
    bit little lot bit too pretty well""".split())
GONE_STATE = frozenset("""black white blue green grey gray red pink yellow orange purple brown
    rusty fuzzy blurry funny fuzzy quiet noisy loud silent still cold hot warm cool dark dim
    blank off bad worse flat dead solid hard soft sticky lumpy dry wet sour mouldy stale numb
    bright pale gold silver cracked wet""".split())


STOPPED_WORKING = ("stopped working", "stopped work", "stops working", "not working",
                   "isnt working", "isn't working", "packed in", "wont work", "won't work",
                   "wont start", "won't start", "wont come on", "won't come on",
                   "dead", "died", "has gone")


def a_thing_has_stopped(understood):
    reading = understood if isinstance(understood, dict) else {}
    words = " ".join(str(word) for word in (reading.get("norm") or reading.get("words") or ()))
    line = " " + (words or str(reading.get("clean") or reading.get("text") or "")).lower() + " "
    line = line.replace(" | ", " ").replace("|", " ")
    if not any(" %s " % phrase in line for phrase in STOPPED_WORKING):
        return False
    things = [str(entity.get("text") or "").lower()
              for entity in (reading.get("entities") or ())
              if isinstance(entity, dict) and entity.get("type") == "thing"]
    if not things:
        return False
    subject = str(reading.get("subject") or "").lower()
    if not subject:
        return True
    return any(thing and (thing in subject or subject in thing) for thing in things)


def the_thing_has_gone(understood):
    reading = understood if isinstance(understood, dict) else {}
    said = [str(word).lower() for word in (reading.get("words") or [])]
    line = " " + " ".join(said) + " "
    if not said:
        line = " " + str(reading.get("clean") or reading.get("text") or "").lower() + " "
    after_gone = [found.group(1) for found in HAS_GONE.finditer(line)]
    for tail in after_gone:
        words = [word.strip("'.,!?") for word in tail.split()]
        words = [word for word in words if word]
        while words and words[0] in GONE_INTENSIFIER:
            words.pop(0)
        if not words or words[0] not in GONE_STATE:
            return True
    return False


FOOD_NAMED = FOOD_SUBJECT + (
    "ham", "bacon", "sausage", "sausages", "beef", "pork", "lamb", "mince", "steak",
    "turkey", "salmon", "cod", "haddock", "tuna", "prawn", "prawns", "egg", "eggs",
    "tofu", "beans", "lentils", "leftover", "leftovers", "fruit", "berries", "veg",
    "vegetables", "salad", "gravy", "stew", "curry", "soup", "rice", "pasta",
    "noodles", "sandwich", "mayo", "mayonnaise", "cream", "custard", "pie", "quiche",
    "dinner", "lunch", "supper")

SMELL_VERBS = frozenset(("smell", "smells", "smelled", "smelt", "smelling", "smelly",
                         "stink", "stinks", "stank", "stinking"))
_BAD_IS_A_STATE = frozenset((
    "has", "have", "had", "is", "was", "are", "were", "been", "be", "being", "got", "gets",
    "getting", "gone", "went", "go", "goes", "going", "looks", "looked", "looking",
    "tastes", "tasted", "tasting", "smells", "smelled", "smelt", "smelling", "smelling"))

OFF_SAID_OF_FOOD = frozenset((
    "sour", "soured", "souring", "slimy", "slime", "tacky", "sticky", "mouldy", "moldy",
    "rancid", "curdled", "curdling", "rotten", "putrid", "funny", "bad", "dodgy", "grey",
    "fizzy", "bubbling", "discoloured", "discolored", "off"))

A_GOOD_SMELL = frozenset((
    "great", "good", "amazing", "lovely", "nice", "delicious", "fine", "wonderful",
    "fantastic", "incredible", "tasty", "better", "perfect", "heavenly", "divine", "ok",
    "okay", "alright", "lush", "yummy", "appetising", "appetizing", "gorgeous", "brilliant",
    "of", "like"))

BEFORE_OFF = frozenset((
    "has", "have", "had", "is", "was", "are", "were", "been", "be", "being", "got",
    "gets", "getting", "gone", "went", "go", "goes", "going", "looks", "looked",
    "looking", "tastes", "tasted", "the", "my", "a", "an", "bit", "little",
    "now", "and", "just", "really", "very", "so", "still", "quite", "definitely",
    "starting", "to", "on", "properly", "seriously"))

OFF_STATE_ASKS = ("still ok", "still okay", "still good", "still fine", "still safe",
                  "still alright", "still all right", "still edible", "gone off",
                  "going off", "gone bad", "went off", "gone past", "gone sour",
                  "gone mouldy", "gone slimy", "out of date", "past its date",
                  "past the date", "past their date", "use by", "best before",
                  "is off", "smells off", "are off", "smell off")


def food_has_gone_off(understood):
    if not isinstance(understood, dict):
        return False
    text = str(understood.get("plain") or understood.get("clean") or understood.get("text")
               or "").lower()
    words = tokens(text)
    if not words or not any(word in FOOD_NAMED for word in words):
        return False
    for phrase in OFF_STATE_ASKS:
        if phrase in text:
            return True
    for pos, word in enumerate(words):
        if word not in FOOD_NAMED:
            continue
        at = pos + 1
        while at < len(words) and words[at] in BEFORE_OFF:
            at += 1
        if at >= len(words):
            continue
        said = words[at]
        if said == "bad":
            between = words[pos + 1:at + 1]
            if not any(word in _BAD_IS_A_STATE for word in between):
                continue
        if said in OFF_SAID_OF_FOOD:
            return True
        if said in SMELL_VERBS:
            after = words[at + 1:at + 2]
            if not after or after[0] not in A_GOOD_SMELL:
                return True
    return False


JOB_GUARD = ("repair", "repairs", "repaired", "repairing", "fix", "fixes", "fixed", "fixing",
             "install", "installs", "installed", "installing", "installation", "fit", "fits",
             "fitted", "fitting", "engineer", "engineers", "plumber", "plumbers", "callout",
             "call out", "call-out", "come out", "coming out", "swap", "swapping")


_BORROWING_IN_THE_LINE = re.compile(
    r"\b(?:borrow(?:s|ed|ing|er|ers)?|lend(?:s|ing)?|lent|loan|loans|owed?|owes|tide me over)\b")
_OFF_A_PERSON = re.compile(
    r"\b(?:money|quid|pounds?|cash|tenner|fiver|ton|grand|\d+)\s+off\s+(?:of\s+)?"
    r"(?:a|an|my|our|your|his|her|their)\s+"
    r"(?:mum|mam|mammy|mother|mam|dad|father|parents?|brother|brothers|sister|sisters|"
    r"gran|granny|nan|nana|grandma|grandad|grandpa|son|daughter|child|kid|uncle|aunt|auntie|"
    r"cousin|husband|wife|partner|boyfriend|girlfriend|mate|mates|friend|friends|neighbour|"
    r"neighbours|boss|colleague|colleagues|workmate|flatmate|housemate|lodger|landlord)\b")


def a_price_not_a_loan(understood):
    said = understood if isinstance(understood, dict) else {}
    text = str(said.get("text") or said.get("clean") or "")
    if not text:
        text = " ".join(str(one) for one in (said.get("words") or ()))
    if not text:
        return True
    return not (_BORROWING_IN_THE_LINE.search(text) or _OFF_A_PERSON.search(text))


_FLAT_YOU_LIVE_IN = re.compile(
    r"\b(?:my|the|our|this|that|their|his|her|a|one)\s+"
    r"(?:tiny\s+|small\s+|little\s+|new\s+|old\s+|top\s+floor\s+|ground\s+floor\s+|"
    r"second\s+floor\s+|studio\s+)?flat\b"
    r"|\b(?:move|moves|moved|moving|rent|rents|rented|renting|let|letting|buy|buys|bought|"
    r"buying|sell|sells|selling|sold|view|viewing|sort|sorting|sorted|decorate|decorating|"
    r"refurbish|refurbishing)\s+(?:(?:a|an|the|my|our|this|that|his|her)\s+)?"
    r"(?:tiny\s+|small\s+|little\s+|new\s+|old\s+)?flat\b"
    r"|\b(?:heat|heating|clean|cleaning)\s+(?:a|an|the|my|our|this|that)\s+"
    r"(?:tiny\s+|small\s+|little\s+)?flat\b"
    r"|\bflats\b|\bflat\s?mates?\b|\bbedsit\b", re.IGNORECASE)


_THE_HEAT_OF_AN_ARGUMENT = re.compile(
    r"\b(?:got|get|gets|getting|bit|a bit|so|very|really|quite|all)\s+heated\b(?!\s+up)"
    r"|\bheated\s+(?:with|at|about|over|argument|arguments|discussion|discussions|row|rows|"
    r"debate|debates|exchange|exchanges|words|moment|moments|conversation)\b",
    re.IGNORECASE)


def not_the_heat_of_an_argument(understood):
    if not isinstance(understood, dict):
        return True
    said = understood.get("text") or understood.get("clean") or ""
    if not said:
        said = " ".join(understood.get("words") or ())
    return not _THE_HEAT_OF_AN_ARGUMENT.search(str(said))


_ORDER_OF_STEPS = re.compile(r"""
    \b what \s+ (?:should|shall|do|would|must|can) \s+ (?:i|we) \s+
       (?: do|sort|pick|choose|get|buy|wash|clean|tackle|start|book|pack|fix|handle
         | plan|change|replace|check|ask|say|look \s+ at|deal \s+ with|set \s+ up
         | make|go \s+ for|put \s+ up )
    \b .* \b (?:first|next|before|afterwards|after \s+ that) \b
""", re.X | re.I)


def the_ask_is_the_order_of_steps(understood):
    if not isinstance(understood, dict):
        return False
    said = understood.get("text") or understood.get("clean") or ""
    if not said:
        said = " ".join(understood.get("words") or ())
    return bool(said) and bool(_ORDER_OF_STEPS.search(str(said)))


def not_the_ask_about_the_order(understood):
    return not the_ask_is_the_order_of_steps(understood)


def not_the_flat_you_live_in(understood):
    if not isinstance(understood, dict):
        return True
    said = understood.get("text") or understood.get("clean") or ""
    if not said:
        said = " ".join(understood.get("words") or ())
    return not _FLAT_YOU_LIVE_IN.search(str(said))


_A_BAKE_OR_A_PAN = re.compile(
    r"\b(?:bread|breads|loaf|loaves|cake|cakes|sponge|scones?|pastry|pastries|tarts?|buns?|"
    r"rolls?|pizza|pizzas|pancakes?|omelettes?|omelets?|yorkshires?|puddings?|meringues?|"
    r"souffles?|biscuits?|cookies?|brownies?|crumpets?|dough|naan|pittas?|pita|ciabatta|"
    r"focaccia|baguette|batter|sourdough|flatbread|chapatis?|tortillas?|waffles?|loaf tin)\b",
    re.IGNORECASE)

_CAME_OUT_FLAT = re.compile(
    r"\b(?:came|come|comes|coming|turned|turns|turning|went|gone|goes|going)\s+"
    r"(?:out\s+)?(?:a\s+bit\s+|a\s+little\s+|really\s+|so\s+|rather\s+|too\s+)?flat\b",
    re.IGNORECASE)

_THE_GROUND_UNDERFOOT = re.compile(
    r"\b(?:walk|walks|walking|walked|stroll|strolls|hike|hikes|route|routes|path|paths|"
    r"towpath|trail|trails|terrain|ground|fields?|park|parks|promenade|seafront|beach|"
    r"miles?|kilometres?|outing|day out|somewhere to go|wheelchair|buggy|pram|pushchair)\b",
    re.IGNORECASE)


def not_the_flat_of_something_made(understood):
    if not isinstance(understood, dict):
        return True
    said = understood.get("text") or understood.get("clean") or ""
    if not said:
        said = " ".join(understood.get("words") or ())
    said = str(said)
    if not re.search(r"\bflat\b", said, re.IGNORECASE):
        return True
    if _A_BAKE_OR_A_PAN.search(said):
        return False
    if _CAME_OUT_FLAT.search(said) and not _THE_GROUND_UNDERFOOT.search(said):
        return False
    return True


_YEAR_OLD_FIGURE = re.compile(r"\b(?:\d+|a|an|one|two|three|four|five|six|seven|eight|nine|ten|eleven"
                             r"|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen"
                             r")\s*(?:years?|yrs?)\s+old\b", re.I)
_A_THING_SAID_IS = re.compile(
    r"\b(?:my|our|your|his|her|their|the)\s+(?P<noun>[a-z][a-z' -]{0,40}?)\s*"
    r"(?:is|was|are|were|'s|s)\b[^.!?]{0,40}$", re.I)
_A_THING_JUST_BEFORE = re.compile(r"\b(?:my|our|the|his|her|their)\s+[a-z][a-z']{1,14}\s*,?\s*$",
                                  re.I)
_A_THING_POINTED_AT = re.compile(
    r"\b(?:it|its|it's|that|this|they|these|those)\s+"
    r"(?:(?:is|was|are|were|'s|about|roughly|around|only|just|nearly|now|prob)\b[\s,]*){1,3}$",
    re.I)
_PEOPLE_AGED = re.compile(
    r"\b(?:i|me|my son|my daughter|my child|my children|my kid|my kids|my boy|my girl|son"
    r"|daughter|child|children|kid|kids|boy|girl|baby|toddler|teen|teenager|he|she|him|her"
    r"|his|hers|mum|dad|mother|father|wife|husband|partner|friend|nephew|niece|grandson"
    r"|granddaughter|grandchild)\b", re.I)


def the_years_are_a_things(understood):
    text = ""
    if isinstance(understood, dict):
        text = str(understood.get("text") or understood.get("clean") or "")
        if not text:
            text = " ".join(str(word) for word in (understood.get("words") or ()))
    text = " ".join(text.lower().split())
    if not text:
        return False
    figures = list(_YEAR_OLD_FIGURE.finditer(text))
    if not figures:
        return False
    for found in figures:
        window = text[max(0, found.start() - 60):found.start()]
        if _PEOPLE_AGED.search(window):
            return False
        if not (_A_THING_SAID_IS.search(window) or _A_THING_JUST_BEFORE.search(window)
                or _A_THING_POINTED_AT.search(window)):
            return False
    return True


_CHILD_WORDS = frozenset((
    "child", "childs", "children", "kid", "kids", "son", "sons", "daughter", "daughters",
    "boy", "boys", "girl", "girls", "baby", "babies", "toddler", "toddlers", "teen", "teens",
    "teenager", "teenagers", "newborn", "newborns", "stepson", "stepdaughter", "grandchild",
    "grandchildren", "grandson", "granddaughter", "nephew", "niece", "pupil", "pupils",
))
_CHILD_PHRASES = frozenset(("little one", "little boy", "little girl", "a child", "my child",
                            "the child", "our child", "my kids", "school age child"))
_A_YEARS_OLD = re.compile(r"\b(?:years?|yrs?) old\b", re.I)


def _the_age_is_a_childs(item):
    known = _CHILDS_AGE_ROWS.get(item.id)
    if known is not None:
        return known
    words, phrases = set(), []
    stack = list(item.key or ())
    while stack:
        part = stack.pop()
        if isinstance(part, str):
            plain = part.lower().replace("'s", "s")
            words.update(plain.split())
            phrases.append(plain)
        elif isinstance(part, (tuple, list, frozenset, set)):
            stack.extend(part)
    a_person = bool(_CHILD_WORDS.intersection(words)) or any(
        phrase in _CHILD_PHRASES for phrase in phrases)
    answer = a_person and _key_says_years_old(item)
    _CHILDS_AGE_ROWS[item.id] = answer
    return answer


def _key_says_years_old(item):
    stack = list(item.key or ())
    while stack:
        part = stack.pop()
        if isinstance(part, str):
            if _A_YEARS_OLD.search(part):
                return True
        elif isinstance(part, (tuple, list, frozenset, set)):
            stack.extend(part)
    return False


_CHILDS_AGE_ROWS = {}





_KEEPING_AN_EYE = re.compile(
    r"\b(?:keep|keeps|keeping|kept|have|has|having|had|get|gets|getting|got)\s+"
    r"(?:a|an|one|my|your|his|her|their|our|both|the)?\s*eyes?\s*"
    r"(?:out|on|peeled|open|skinned|glued|trained)\b"
    r"|\beyes?\s+(?:peeled|open\s+for|on\s+(?:the|him|her|them|it|that|this|what))\b"
    r"|\bturn(?:s|ed|ing)?\s+a\s+blind\s+eye\b|\beyes?\s+in\s+the\s+back\s+of\b"
    r"|\beye\s+contact\b|\beye\s+witness\b|\bprivate\s+eye\b|\beagle\s+eye\b",
    re.IGNORECASE)


def not_keeping_an_eye_on_it(understood):
    if not isinstance(understood, dict):
        return True
    said = understood.get("text") or understood.get("clean") or ""
    if not said:
        said = " ".join(understood.get("words") or ())
    return not _KEEPING_AN_EYE.search(str(said))


SHORT_OF_SLEEP = re.compile(
    r"\b(?:keep|keeps|keeping|kept)\s+(?:(?:nodding|dozing)\s*(?:off|asleep)?|(?:falling|dropping)\s+(?:off|asleep))\b"
    r"|\bnodd(?:ing|ed|s)?\s+off\b|\bdoz(?:e|es|ed|ing)\s+off\b"
    r"|\beyes?\s+(?:keep|keeps|are|were)?\s*(?:closing|dropping|shutting)\b"
    r"|\b(?:keep|keeps|keeping|kept)\s+(?:my|your|his|her|their|our|both)?\s*eyes?\s+open\b"
    r"(?!\s+for\b)"
    r"|\bf(?:all|ell)(?:ing|s)?\s+asleep\s+(?:at|in|on|during|over)\b"
    r"|\bcan\s*(?:'?t|cant|not)?\s*(?:barely|hardly)\s+(?:keep|stay)\s+"
    r"(?:(?:my|your|his|her|their|our|both)\s+)?(?:eyes?\s+open|awake|alert)\b",
    re.IGNORECASE)


NOT_TIRED_AFTER_ALL = re.compile(
    r"\b(?:hay ?fever|allerg(?:y|ies|ic)|pollen|conjunctivitis|stye|sty|glued|"
    r"swollen|puffy|watering|streaming)\b", re.IGNORECASE)


A_DEVICE_THAT_SLEEPS = frozenset((
    "laptop", "laptops", "computer", "computers", "pc", "pcs", "mac", "macs", "macbook",
    "phone", "phones", "iphone", "android", "tablet", "tablets", "ipad", "monitor", "monitors",
    "screen", "screens", "tv", "television", "televisions", "console", "consoles", "xbox",
    "playstation", "kindle", "printer", "printers", "camera", "cameras", "watch", "fitbit",
))
_A_PERSON_WHO_SLEEPS = frozenset((
    "i", "im", "i'm", "me", "myself", "we", "us", "ourselves", "he", "him", "himself",
    "she", "her", "herself", "they", "them", "themselves", "you", "eyes", "eye", "head",
    "body", "kid", "kids", "child", "children", "baby", "son", "daughter", "boy", "girl",
    "boy", "boys", "girls", "toddler", "lad", "lass", "teenager", "nan", "dad", "mum",
))
_SLEEPY_MARKS = string.punctuation + "\u2019"


def _the_device_is_the_one_falling_asleep(said, start):
    device = person = -1
    for index, word in enumerate(said[:start].split()):
        bare = word.strip(_SLEEPY_MARKS).lower()
        if bare in A_DEVICE_THAT_SLEEPS:
            device = index
        elif bare in _A_PERSON_WHO_SLEEPS:
            person = index
    return device >= 0 and device >= person


def the_body_is_short_of_sleep(understood):
    said = _the_whole_line(understood)
    if NOT_TIRED_AFTER_ALL.search(said):
        return False
    for shape in SHORT_OF_SLEEP.finditer(said):
        if not _the_device_is_the_one_falling_asleep(said, shape.start()):
            return True
    return False


def not_a_sleepy_body(understood):
    return not the_body_is_short_of_sleep(understood)


def all_of(*guards):
    def test(understood):
        return all(bool(guard(understood)) for guard in guards if guard)
    return test


def _the_whole_line(understood):
    if not isinstance(understood, dict):
        return str(understood or "").lower()
    said = " ".join(str(understood.get(key) or "") for key in ("text", "clean"))
    if not said.strip():
        said = " ".join(understood.get("words") or ())
    return said.lower()

def entry(id, key, reply, avoid=(), bias=0, ask=(), slips=(), fault=False,
          report=False, guard=None, shape=(), explain=False, lead="", outcomes=()):
    return Entry(id, key, reply, _avoid_words(avoid), bias, ask, slips, fault, report, guard,
                 shape, explain, lead, outcomes)


KINDS_WORDS = ("kinds of", "kind of", "types of", "type of", "sorts of", "sort of",
               "varieties of", "variety of", "different kinds", "different types",
               "different sorts", "different varieties")
KINDS_SHAPE = "options"
KINDS_FOLLOW_UP_WORDS = ("and", "what", "how", "about", "same", "also", "then", "so")
KINDS_ASKS_ME = re.compile(
    r"\b(?:do|does|would|will|did|can|could|are|were)\s+(?:you|u)\s+"
    r"(?:like|love|prefer|drink|eat|use|having|have|think|recommend|choose|watch|read|make|"
    r"order|rate|enjoy)\b")
KINDS_ASKS_WITH_A_VERB = re.compile(
    r"\b(?:want|wants|wanted|wanna|would like|like to|need|needs|needed|wonder|wondering|"
    r"wondered|ask|asked|know|knowing|learn|find out|show|show me|tell|tell me|curious|"
    r"after|looking for|interested|thinking of|choose|choosing|pick|picking|decide|deciding|"
    r"recommend)\b")

KINDS_SAYS_HOW_IT_IS = re.compile(
    r"\b(?:i|we|you|they|he|she|it|there|people|everyone|someone|nobody|this|that|these|those|"
    r"the|my|our|his|her|their)\b(?:\s+\w+){0,3}\s+"
    r"(?:is|are|was|were|am|has|have|had|do|does|did|can|could|will|would|should|tried|try|tries|"
    r"bought|buy|buys|made|make|makes|ate|eat|eats|cooked|cooks|keep|keeps|stock|stocks|sell|"
    r"sells|sold|use|uses|used|prefer|prefers|like|likes|liked|love| loves|love|loved|hate|"
    r"hates|hated|grow|grows|grew|got|get|gets|need|needs|want|wants)\b")

KINDS_NAMED_A_USE = re.compile(
    r"\b(?:for|best|better|good|right|make|makes|making|bake|baking|cook|cooking|roast|roasting|"
    r"boil|boiling|mash|fry|frying|chips|salad|soup|sauce|crumble|pie|cakes?|bread|jam|chutney|"
    r"keep|keeps|keeping|store|storing|freeze|frozen|buy|buying|cheap|cheapest|substitute|"
    r"instead|replace|swap|goes|go|with|worth|healthy|"
    r"bring|brings|take|takes|serve|serves|serving|dinner|lunch|supper|party|picnic|barbecue|"
    r"bbq|wedding|christmas|birthday|gift|present|occasion|hosting)\b")


def asks_the_kinds(understood):
    if not isinstance(understood, dict):
        return False
    said = str(understood.get("clean") or understood.get("text") or "")
    if said and KINDS_ASKS_ME.search(said):
        return False
    if said and not KINDS_NAMED_A_USE.search(said):
        words = " %s " % " ".join(said.lower().replace("[", " ").replace("]", " ")
                                  .replace(",", " ").replace("'", " ").split())
        lowered = " ".join(said.lower().split())
        says_it = (understood.get("intent") == "news"
                   or (understood.get("kind") != "question"
                       and not KINDS_ASKS_WITH_A_VERB.search(lowered)
                       and KINDS_SAYS_HOW_IT_IS.search(lowered)))
        if not says_it and any(kind in words for kind in KINDS_WORDS):
            return True
    return (understood.get("wants") == KINDS_SHAPE
            and not KINDS_NAMED_A_USE.search(said)
            and not set(understood.get("asks") or ()) - {"what", "yesno"})


def kinds_entries(rows):
    out = []
    for subjects, name, answer in rows:
        out.append(entry("kinds-of-%s" % name, (KINDS_WORDS, subjects), answer,
                         guard=asks_the_kinds, bias=2))
        out.append(entry("kinds-of-%s-told" % name, (KINDS_FOLLOW_UP_WORDS, subjects), answer,
                         guard=asks_the_kinds, bias=2))
    return out


_CONTRACTION = frozenset((
    "it's", "what's", "that's", "there's", "here's", "he's", "she's", "who's", "where's",
    "when's", "why's", "how's", "let's", "this's", "one's", "everyone's", "someone's",
    "nothing's", "everything's", "nobody's",
))

IRREGULAR_PLURALS = {
    "leaves": "leaf", "loaves": "loaf", "sheaves": "sheaf", "thieves": "thief",
    "wolves": "wolf", "shelves": "shelf", "selves": "self", "elves": "elf",
    "halves": "half", "calves": "calf", "scarves": "scarf", "wharves": "wharf",
    "hooves": "hoof", "knives": "knife", "wives": "wife", "lives": "life",
}


_CURLY = str.maketrans({"’": "'", "‘": "'", "ʼ": "'"})
_CURLY_ANY = ("’", "‘", "ʼ")


def _doubles_for_an_ending(stem):
    if len(stem) < 4 or stem[-1] != stem[-2] or stem[-1] in "aeiou" or stem[-1] == "s":
        return False
    if stem[-1] == "l":
        return True
    if stem[-3] not in "aeiou":
        return False
    return _is_consonant(stem, len(stem) - 4)


def _is_consonant(word, index):
    if index < 0:
        return False
    letter = word[index]
    if letter not in "aeiou":
        return True
    return letter == "u" and index > 0 and word[index - 1] == "q"


def _forms(word):
    got = _FORMS_CACHE.get(word)
    if got is not None:
        return got
    forms = _work_out_forms(word)
    frozen = frozenset(forms)
    if len(_FORMS_CACHE) >= _FORMS_CACHE_KEEP:
        _FORMS_CACHE.clear()
    _FORMS_CACHE[word] = frozen
    return frozen


_FORMS_CACHE = {}
_FORMS_CACHE_KEEP = 50000



def _work_out_forms(word):
    word = word.translate(_CURLY)
    forms = {word}
    other = lexicon.US_SPELLINGS.get(word)
    if other:
        forms.add(other)
    if word.endswith("ies") and len(word) > 5:
        forms.add(word[:-3] + "y")
    if word.endswith("y") and len(word) > 3 and word[-2] not in "aeiou":
        forms.add(word[:-1] + "ies")
    if word in IRREGULAR_PLURALS:
        forms.add(IRREGULAR_PLURALS[word])
        return forms
    if word.endswith("'s") and len(word) > 3 and word not in _CONTRACTION:
        forms.add(word[:-2])
    elif word.endswith("s'") and len(word) > 3:
        forms.add(word[:-2])
        forms.add(word[:-1])
    if len(word) > 3:
        if word.endswith("s") and not word.endswith("ss") and word not in NOT_A_WORD_WITH_AN_S:
            _add(forms, word[:-1])
        if (word.endswith("es") and len(word) > 4
                and (word[-3] in "sxzi" or word[-4:-2] in ("ch", "sh") or word[-3] == "o")):
            _add(forms, word[:-2])
        if word.endswith("ed") and len(word) > 4:
            if _engine_reads(word[:-2]) and _engine_reads(word[:-1]):
                _add(forms, word[:-1])
            else:
                _add(forms, word[:-2])
            if len(word) > 5 and _doubles_for_an_ending(word[:-2]):
                _add(forms, word[:-3])
        if word.endswith("ing") and len(word) > 5:
            stem = word[:-3]
            if word not in NOT_THE_STEM_WITH_E:
                _add(forms, stem + "e")
            if (word not in NOT_THE_STEM and stem not in NOT_A_BASE
                    and (not _cvc(stem) or (len(stem) > 2 and stem.endswith("y"))
                         or _bare_is_the_word(stem))):
                _add(forms, stem)
            if _doubles_for_an_ending(stem) and word not in NOT_THE_DOUBLED_STEM:
                _add(forms, stem[:-1])
    return forms


NOT_THE_STEM = frozenset(("teething", "sugaring", "evening", "stuffing",
                          "skirting",
                          "outing",
                          "weathering", "lettering", "wording", "boarding", "footing", "decking",
                          "clothing", "housing", "marketing", "banking", "accounting"))

NOT_A_WORD_WITH_AN_S = frozenset(("ages",))


NOT_THE_STEM_WITH_E = frozenset(("housing",))

NOT_A_BASE = frozenset(
    "about above across after against along among around at before behind below beneath "
    "beside besides between beyond by down for from in into near of off on onto out over "
    "past since through till to toward towards under until up upon with within without".split())


NOT_THE_DOUBLED_STEM = frozenset(("bedding",))


def _add(forms, form):
    if len(form) >= MIN_FORM:
        forms.add(form)

_CHAT_PHRASES = (
    r"how did we (?:start|begin|get started|meet)"
    r"|how did (?:this|our|the) (?:chat|conversation) (?:start|begin|go)"
    r"|(?:start|beginning) of (?:this|our|the) (?:chat|conversation)"
    r"|what did (?:i|we) (?:say|ask|tell you) (?:first|at the start|at the beginning)"
    r"|what was (?:the first thing|my first (?:question|line|message))"
    r"|first (?:thing|question|line|message) (?:i|we) (?:asked|said|sent)(?: you| him| her)?"
    r"|do you (?:remember|recall) what (?:i|we) (?:said|asked|told)(?: you)?(?: first)?"
    r"|what have we (?:talked|spoken) about"
    r"|what did we talk about"
)
_CHAT_TAIL = (r"(?:\s+(?:out|then|here|it|this|that|chat|conversation|talking|off|again|"
              r"everything))*\s*")
_ABOUT_THE_CHAT = re.compile(r"(?:^|\s)(?:" + _CHAT_PHRASES + r")" + _CHAT_TAIL + r"$")


def about_the_chat(own_line):
    return bool(_ABOUT_THE_CHAT.search(" ".join(tokens(str(own_line or "")))))


def _bare_is_the_word(stem):
    return (_engine_reads(stem) and not _engine_reads(stem + "e")
            and stem not in _FUNCTION_WORDS)


_FUNCTION_WORDS = frozenset(lexicon.CORE.split())


def _cvc(stem):
    if not 3 <= len(stem) <= 4:
        return False
    vowels = "aeiou"
    return stem[-1] not in vowels and stem[-2] in vowels and stem[-3] not in vowels


def tokens(text):
    return WORD.findall(text.translate(_CURLY).lower())


_THROAT = re.compile(
    r"^(?:(?:and|oh|ooh|ok|okay|so|but|right|ah|er|um|umm|hmm|sorry|also|just|plus|hey|ta|"
    r"anyway|anyways|then|actually|well)\b[\s,:-]*)+")
_BRIDGES = tuple(lexicon.HANDOFF_BRIDGES) + ("is", "was")
_BRIDGE = re.compile(r"^\s*(?:" + "|".join(re.escape(one) for one in
                                            sorted(_BRIDGES, key=len, reverse=True))
                     + r")\b[\s,.:;\-\u2013\u2014]*")
_PUNCTUATION = re.compile(r"^\s*[,.:;\-\u2013\u2014]+[\s,.:;\-\u2013\u2014]*")


def _past_a_handoff(clean):
    text = _THROAT.sub("", " ".join(str(clean or "").lower().split()))
    for lead in sorted(lexicon.HANDOFF_LEADS, key=len, reverse=True):
        if not text.startswith(lead):
            continue
        rest = text[len(lead):]
        after = None
        punctuation = _PUNCTUATION.match(rest)
        if punctuation:
            after = rest[punctuation.end():]
        else:
            bridge = _BRIDGE.match(rest)
            if bridge:
                after = rest[bridge.end():]
        if after is None:
            continue
        bridge = _BRIDGE.match(after)
        if bridge:
            after = after[bridge.end():]
        return after.strip(" ,.:;\t\u2013\u2014") or None
    return None


CARER_FRAME = re.compile(
    r"^\s*(?:my|our|the)\s+(?:poor\s+|little\s+|eldest\s+|youngest\s+|old\s+|new\s+)?"
    r"(?:son|sons|daughter|daughters|child|children|kid|kids|baby|boy|girl|toddler|teen|"
    r"teenager|mum|mam|mom|mother|dad|father|wife|husband|partner|boyfriend|girlfriend|"
    r"sister|brother|niece|nephew|grandson|granddaughter|grandchild|grandchildren|"
    r"friend|mate)\s*(?:'s|s')?\s+"
    r"(?:has|have|had|got|caught|come down with|came down with|is|are|was|were|"
    r"keeps getting|came out in|is covered in|has come out in)\s+"
    r"(?:(?:an?|the|some)\s+)*", re.I)


AN_ILLNESS = re.compile(r"\b(?:" + "|".join(sorted(lexicon.BODY_PARTS)) + r"|" + "|".join("""
ill unwell poorly sick sickness bug bugs virus infection infected cold flu fever temperature
cough coughing sneeze sneezing wheeze wheezing breath breathing rash itchy itching itch spot
spots lump lumps sore pain painful ache aching hurt hurts injury injured wound cut gash burn
scald scab bruise bruised swelling swollen stiff sprain strain break broken fracture
dislocated dizzy fainting faint vomit vomiting diarrhoea diarrhea constipation dehydrated
dehydration allergy allergic reaction hives eczema psoriasis asthma croup colic teething
chickenpox measles mumps rubella tonsillitis thrush nits lice worms threadworms ringworm
verruca verrucas wart warts boil boils abscess stye conjunctivitis earache toothache headache
migraine migraines pneumonia bronchitis covid shingles gout sciatica arthritis cystitis uti
scabies impetigo meningitis quinsy coldsore epilepsy seizure
seizures dementia alzheimers diabetes anaemia thyroid tumour leukaemia cancer stroke
""".split()) + r")(?:s|es)?\b", re.I)


def _past_the_carer(clean):
    text = " ".join(str(clean or "").lower().split())
    found = CARER_FRAME.match(text)
    if not found:
        return None
    left = text[found.end():].strip(" ,.:;\t")
    words = [word.strip(_MARKS) for word in left.split() if word.strip(_MARKS)]
    if not words:
        return None
    if AN_ILLNESS.fullmatch(words[-1]) or (
            len(words) <= 3 and any(AN_ILLNESS.fullmatch(word) for word in words)):
        return left
    return None


DEAD_AS_VERY_AFTER = frozenset((
    "quiet", "tired", "easy", "good", "bad", "cheap", "slow", "boring", "cheerful", "glad",
    "lucky", "proud", "keen", "jealous", "happy", "sure", "tricky", "hard", "funny", "rude",
    "straight", "wrong", "serious", "certain", "ahead", "silent", "knackered", "shattered",
    "comfy", "comfortable", "soft", "cosy", "cozy", "warm", "cold", "nice", "sweet", "pretty",
    "smooth", "strong", "fussy", "broke", "skint", "fun", "obvious", "scary", "gentle", "relaxed",
    "bright", "dark", "loud", "chuffed", "mint", "annoying", "embarrassing",
    "quick", "fast", "clean", "simple", "smart", "friendly", "heavy",
))


def _without_a_dead_that_only_means_very(words):
    kept = []
    for index, word in enumerate(words):
        following = words[index + 1] if index + 1 < len(words) else ""
        if (str(word).lower() == "dead"
                and str(following).lower().strip(_MARKS) in DEAD_AS_VERY_AFTER):
            continue
        kept.append(word)
    return kept


_MARKS = string.punctuation + "\u2019"


COOKING_AS_A_NAME = frozenset(("oil", "oils", "apple", "apples", "chocolate", "bacon", "fat",
                               "sauce", "wine", "salt", "cream", "onions", "onion", "ham"))


def _without_a_cooking_that_is_a_name(words):
    kept = []
    for index, word in enumerate(words):
        following = words[index + 1] if index + 1 < len(words) else ""
        if (str(word).lower() == "cooking"
                and str(following).lower().strip(_MARKS) in COOKING_AS_A_NAME):
            continue
        kept.append(word)
    return kept


CHILD_BY_PLACE = re.compile(
    r"\b(?:my|our|the|his|her|their)\s+(?:youngest|eldest|oldest|little\s+one|middle\s+one|"
    r"lad|lass|kiddo|laddie|un)\b"
    r"|\b(?:my|our|the|his|her|their)\s+(?:little|small|wee|big|older|elder|younger|poor)\s+"
    r"(?:youngest|eldest|oldest|one|lad|lass|kiddo|laddie|un|boy|girl|man)\b",
    re.I)
CHILD_PLACE_WORDS = frozenset(("youngest", "eldest", "oldest", "little", "middle"))
CHILD_SIZE_WORDS = frozenset(("little", "small", "wee", "big", "older", "elder", "younger",
                              "poor"))
CHILD_AFTER_A_SIZE = frozenset(("boy", "girl", "un", "man"))
EVERYDAY_CHILD = frozenset(("lad", "lass", "kiddo", "laddie"))
A_CHILD_WORD_BY_ITSELF = re.compile(
    r"\b(?:my|our|the|his|her|their)\s+(?:youngest|eldest|oldest|little\s+one|middle\s+one|"
    r"lad|lass|kiddo|laddie)\b", re.I)
A_CHILD_GETTING_OLDER = re.compile(
    r"\b(?:teenager|teenagers|teen|teens|teenage|teenaged|secondary\s+school|high\s?school|"
    r"senior\s+school|year\s+(?:7|8|9|10|11))\b"
    r"|\b(?:is|are|aged?|turned|turns|turning|now|nearly|just)\s+"
    r"(?:1[1-9]|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen)\b"
    r"(?!\s*(?:months?|mths?|weeks?|mos?)\b)"
    r"|\b(?:1[1-9]|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen)"
    r"\s*(?:year|yr)s?\s*old\b", re.I)
A_TEEN = re.compile(
    r"\b(?:teenager|teenagers|teen|teens|teenage|teenaged)\b"
    r"|\b(?:is|are|aged?|turned|turns|turning|now)\s+"
    r"(?:1[3-9]|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen)\b"
    r"(?!\s*(?:week|weeks|month|months|day|days|hour|hours|stone|stones|kilos?|kg|lbs?|pounds?))",
    re.I)
NOT_A_CHILD_SAID = frozenset("""dog dogs puppy puppies cat cats kitten kittens rabbit rabbits
    hamster hamsters guinea bird birds parrot parrots fish horse horses pony ponies ferret
    pet pets husband wife partner boyfriend girlfriend fiance fiancee friend friends mate mates
    boss colleague colleagues flatmate flatmates housemate housemates neighbour neighbours
    tenant tenants mum mother dad father nan nanna gran granny grandad grandpa sister brother
    aunt uncle cousin nephew niece""".split())


TWO_OF_US = re.compile(r"\A\s*(?:me|i|us)\s*[,&]?\s*(?:and|an|nd|n)\s+(?:my|our|mine)\b", re.I)


def _with_the_animal_in_hand(words, understood):
    animal = (understood or {}).get("animal_in_hand") or ""
    if not animal:
        return words
    kept = []
    for piece in words:
        low = str(piece).lower().strip(_MARKS).split("'")[0]
        kept.append(animal if low in _THE_PRONOUNS else piece)
    return kept if kept != list(words) else words


_THE_PRONOUNS = frozenset("""it its itself he him his himself hes hed she her hers herself shes
    shed they them their theirs theyre theyd this these those""".split())


def _the_animal_rules_out_that_card(item, understood):
    animal = (understood or {}).get("animal_in_hand") or ""
    if not animal:
        return False
    stood_down_for = {str(word).lower() for word in getattr(item, "avoid", ()) or ()}
    return animal in stood_down_for or animal + "s" in stood_down_for


def _with_the_child_by_place(words, clean):
    line = str(clean or "")
    if not CHILD_BY_PLACE.search(line) or TWO_OF_US.match(line):
        return words
    small = not A_TEEN.search(line)
    said = {str(word).lower().strip(_MARKS) for word in words}
    if said & NOT_A_CHILD_SAID:
        return words
    kept = []
    skipping = 0
    if A_CHILD_GETTING_OLDER.search(line) and not A_CHILD_WORD_BY_ITSELF.search(line):
        return words
    for at, word in enumerate(words):
        low = str(word).lower().strip(_MARKS)
        if skipping and (low == "one" or not low):
            skipping = 0
            continue
        skipping = 0
        child_word = low in CHILD_PLACE_WORDS or (small and low in EVERYDAY_CHILD)
        if low in CHILD_SIZE_WORDS:
            after = next((str(word2).lower().strip(_MARKS) for word2 in words[at + 1:]
                          if str(word2).lower().strip(_MARKS)), "")
            if after in CHILD_PLACE_WORDS or after in CHILD_AFTER_A_SIZE or (
                    small and after in EVERYDAY_CHILD):
                continue
        if child_word or (small and low in CHILD_AFTER_A_SIZE
                          and at and str(words[at - 1]).lower().strip(_MARKS)
                          in CHILD_SIZE_WORDS):
            kept.append("child")
            skipping = 1 if low in ("little", "middle") else 0
            continue
        kept.append(word)
    return kept


def _one_edit(shorter, longer):
    if shorter == longer:
        return True
    if abs(len(shorter) - len(longer)) > 1:
        return False
    if len(shorter) > len(longer):
        shorter, longer = longer, shorter
    i = 0
    while i < len(shorter) and shorter[i] == longer[i]:
        i += 1
    if len(shorter) < len(longer):
        return shorter[i:] == longer[i + 1:]
    rest, tail = shorter[i:], longer[i:]
    if rest[1:] == tail[1:]:
        return True
    return (len(rest) > 1 and rest[0] == tail[1] and rest[1] == tail[0]
            and rest[2:] == tail[2:])


def _stem(word):
    for ending in ENDINGS:
        if word.endswith(ending) and len(word) - len(ending) >= 3:
            return word[: -len(ending)]
    return word


_COMMON = frozenset(lexicon.COMMON.split()) | frozenset(lexicon.CORE.split())
_STEMS = frozenset(_stem(word) for word in _COMMON) | _COMMON


def _engine_reads(word):
    return (word in _COMMON or word in COMMON_WORDS or word in lexicon.CHAT
            or word in lexicon.EXPAND or _stem(word) in _STEMS
            or word in lexicon.every_word() or word in COLOUR_WORDS)


def _typo_forms(word, vocabulary):
    if len(word) < MIN_TYPO_LENGTH or _engine_reads(word):
        return set()
    close = [other for other in vocabulary
             if other[:1] == word[:1] and abs(len(other) - len(word)) <= 1
             and _one_edit(word, other)]
    families = {_stem(other) for other in close}
    if len(families) != 1:
        return set()
    forms = set()
    for other in close:
        forms |= _forms(other)
    return forms


PLURAL_ONLY_PHRASES = frozenset(("the runs", "the trots"))


def _wanted(phrase):
    got = _WANTED_CACHE.get(phrase)
    if got is None:
        if phrase.lower() in PLURAL_ONLY_PHRASES:
            got = tuple(frozenset((word,)) for word in phrase.lower().split())
        else:
            got = tuple(_forms(word) for word in phrase.lower().split())
        if len(_WANTED_CACHE) >= _FORMS_CACHE_KEEP:
            _WANTED_CACHE.clear()
        _WANTED_CACHE[phrase] = got
    return got


_WANTED_CACHE = {}


_ARTICLE_WORDS = frozenset("""the a an""".split())


_MIN_BARE_WORDS = 3


BARE_WEIGHT = PHRASE_WEIGHT - 1


def _wanted_bare(phrase):
    got = _WANTED_CACHE.get(("bare", phrase), ())
    if got:
        return got[0]
    words = phrase.lower().split()
    kept = [word for word in words if word not in _ARTICLE_WORDS]
    bare = tuple(_forms(word) for word in kept) if len(kept) >= _MIN_BARE_WORDS and len(kept) < len(words) else None
    if len(_WANTED_CACHE) >= _FORMS_CACHE_KEEP:
        _WANTED_CACHE.clear()
    _WANTED_CACHE[("bare", phrase)] = (bare,)
    return bare


_ARTICLE_FORMS = frozenset().union(*(_forms(word) for word in _ARTICLE_WORDS))


def _phrase_span_bare(forms, wanted, seen):
    n = len(wanted)
    last = len(forms) - 1
    for start in range(len(forms)):
        if not forms[start] & wanted[0]:
            continue
        span = [start]
        here = start + 1
        for j in range(1, n):
            while here <= last and not (forms[here] & wanted[j]):
                if not forms[here] & _ARTICLE_FORMS:
                    break
                here += 1
            if here > last or not (forms[here] & wanted[j]):
                break
            span.append(here)
            here += 1
        else:
            return tuple(span)
    return ()


def _shape(phrase):
    got = _SHAPE_CACHE.get(phrase)
    if got is None:
        words = tuple(phrase.lower().split())
        got = (words, PHRASE_WEIGHT if len(words) > 1 else WORD_WEIGHT)
        if len(_SHAPE_CACHE) >= _FORMS_CACHE_KEEP:
            _SHAPE_CACHE.clear()
        _SHAPE_CACHE[phrase] = got
    return got


_SHAPE_CACHE = {}


_WHERE = object()
_LINE_FORMS = object()
_PHRASE_SPANS = object()
_WANTING = object()
_ASK_ABOUT_SOMEONE = object()


def _line_forms(forms, seen):
    if seen is not None:
        got = seen.get(_LINE_FORMS)
        if got is not None and got[0] is forms:
            return got[1]
    every = set()
    for word_forms in forms:
        every |= word_forms
    every = frozenset(every)
    if seen is not None:
        seen[_LINE_FORMS] = (forms, every)
    return every


def _where(forms, seen):
    if seen is not None:
        got = seen.get(_WHERE)
        if got is not None and got[0] is forms:
            return got[1], got[2]
    where = {}
    for index, word_forms in enumerate(forms):
        for form in word_forms:
            at = where.get(form)
            if at is None:
                where[form] = [index]
            else:
                at.append(index)
    firsts = {form: at[0] for form, at in where.items()}
    if seen is not None:
        seen[_WHERE] = (forms, where, firsts)
    return where, firsts


def _phrase_span(forms, phrase, seen=None):
    spans = None
    if seen is not None:
        got = seen.get(_PHRASE_SPANS)
        if got is not None and got[0] is forms:
            spans = got[1]
        else:
            spans = {}
            seen[_PHRASE_SPANS] = (forms, spans)
        if phrase in spans:
            return spans[phrase]
        end = _phrase_span_work(forms, phrase, seen)
        spans[phrase] = end
        return end
    return _phrase_span_work(forms, phrase, None)


_SAID_BETWEEN = frozenset("""
    just only nearly almost practically finally already still again now then even really
    actually suddenly completely totally literally basically quite very so too
    has have had is was were been being keeps kept
""".split())
_A_BREATH = 2


_ASK_FRAME_FORMS = None


def _ask_frame_forms():
    global _ASK_FRAME_FORMS
    if _ASK_FRAME_FORMS is None:
        _ASK_FRAME_FORMS = frozenset().union(*(_forms(word) for word in ASK_FRAME))
    return _ASK_FRAME_FORMS


def _phrase_span_between(forms, phrase, seen=None):
    if not isinstance(phrase, str):
        return ()
    wanted = _wanted(phrase)
    if not wanted:
        return ()
    if len(wanted) == 1:
        return ()
    if wanted[0] & _ask_frame_forms():
        return ()
    key = ("between", phrase)
    spans = None
    if seen is not None:
        got = seen.get(_PHRASE_SPANS)
        if got is not None and got[0] is forms:
            spans = got[1]
        else:
            spans = {}
            seen[_PHRASE_SPANS] = (forms, spans)
        if key in spans:
            return spans[key]

    def walk(at, next_word, span):
        if next_word == len(wanted):
            return tuple(span)
        gaps = 0
        while at < len(forms) and gaps <= _A_BREATH:
            if forms[at] & wanted[next_word]:
                got = walk(at + 1, next_word + 1, span + [at])
                if got:
                    return got
            if not (forms[at] & _SAID_BETWEEN):
                return ()
            gaps += 1
            at += 1
        return ()

    answer = ()
    for start in range(len(forms)):
        if forms[start] & wanted[0]:
            answer = walk(start + 1, 1, [start])
            if answer:
                break
    if spans is not None:
        spans[key] = answer
    return answer


_ONE_SPELLING = (("won't", "will not"), ("wont", "will not"),
                 ("can't", "cannot"), ("cant", "cannot"),
                 ("shan't", "shall not"), ("dont", "do not"), ("don't", "do not"),
                 ("doesnt", "does not"), ("doesn't", "does not"),
                 ("isnt", "is not"), ("isn't", "is not"),
                 ("arent", "are not"), ("aren't", "are not"),
                 ("wasnt", "was not"), ("wasn't", "was not"),
                 ("werent", "were not"), ("weren't", "were not"),
                 ("didnt", "did not"), ("didn't", "did not"),
                 ("hasnt", "has not"), ("hasn't", "has not"),
                 ("havent", "have not"), ("haven't", "have not"),
                 ("couldnt", "could not"), ("couldn't", "could not"),
                 ("wouldnt", "would not"), ("wouldn't", "would not"),
                 ("shouldnt", "should not"), ("shouldn't", "should not"))
_ONE_SPELLING_EITHER_WAY = {}
for _short, _long in _ONE_SPELLING:
    _ONE_SPELLING_EITHER_WAY.setdefault(_short, set()).add(_long)
    _ONE_SPELLING_EITHER_WAY.setdefault(_long, set()).add(_short)


def _the_same_words(phrase):
    got = _PHRASE_OTHER_SPELLINGS.get(phrase)
    if got is None:
        got = _work_out_the_same_words(phrase)
        if len(_PHRASE_OTHER_SPELLINGS) >= _OTHER_SPELLINGS_KEEP:
            _PHRASE_OTHER_SPELLINGS.clear()
        _PHRASE_OTHER_SPELLINGS[phrase] = got
    return got


_PHRASE_OTHER_SPELLINGS = {}
_OTHER_SPELLINGS_KEEP = 4000


def _work_out_the_same_words(phrase):
    words = phrase.lower().split()
    if not words:
        return ()
    out = []
    for i, word in enumerate(words):
        for other in _ONE_SPELLING_EITHER_WAY.get(word, ()):
            if " " in other:
                out.append(" ".join(words[:i] + other.split() + words[i + 1:]))
            else:
                out.append(" ".join(words[:i] + [other] + words[i + 1:]))
    if len(words) > 1:
        for i in range(len(words) - 1):
            joined = words[i] + " " + words[i + 1]
            for other in _ONE_SPELLING_EITHER_WAY.get(joined, ()):
                if " " not in other:
                    out.append(" ".join(words[:i] + [other] + words[i + 2:]))
    return tuple(out)


def _phrase_span_work(forms, phrase, seen):
    end = _phrase_span_spelling(forms, phrase, seen)
    if end:
        return end
    for other in _the_same_words(phrase):
        end = _phrase_span_spelling(forms, other, seen)
        if end:
            return end
    return ()


def _phrase_span_spelling(forms, phrase, seen):
    wanted = _wanted(phrase)
    if not wanted:
        return ()
    n = len(wanted)
    if seen is not None:
        line = _line_forms(forms, seen)
        for word_forms in wanted:
            if not (word_forms & line):
                return ()
    if seen is None:
        if n == 1:
            for i, word_forms in enumerate(forms):
                if word_forms & wanted[0]:
                    return (i,)
            return ()
        for i in range(len(forms) - n + 1):
            if all(forms[i + j] & wanted[j] for j in range(n)):
                return tuple(range(i, i + n))
        return ()
    where, firsts = _where(forms, seen)
    if n == 1:
        if not wanted[0].isdisjoint(firsts):
            return (min(firsts[form] for form in wanted[0] if form in firsts),)
        return ()
    hits = []
    for word_forms in wanted:
        found = set()
        for form in word_forms:
            found.update(where.get(form, ()))
        if not found:
            return ()
        hits.append(found)
    for start in sorted(i for i in hits[0] if i + n <= len(forms)):
        if all(start + j in hits[j] for j in range(1, n)):
            return tuple(range(start, start + n))
    return ()


def _phrase_found(forms, phrase):
    return bool(_phrase_span(forms, phrase))


_PART_FORMS = {}
_PART_FORMS_KEEP = 20000


def _part_forms(part):
    got = _PART_FORMS.get(id(part))
    if got is not None and got[0] is part:
        return got[1]
    alternatives = part if isinstance(part, tuple) else (part,)
    every = None
    for alternative in alternatives:
        if not isinstance(alternative, str) or not alternative.strip():
            continue
        for word_forms in _wanted(alternative):
            if every is None:
                every = set()
            every |= word_forms
    if every is None:
        return None if not alternatives else frozenset()
    every = frozenset(every)
    if len(_PART_FORMS) >= _PART_FORMS_KEEP:
        _PART_FORMS.clear()
    _PART_FORMS[id(part)] = (part, every)
    return every


def _part_matches(part, forms, seen=None):
    if seen is not None:
        got = seen.get(id(part))
        if got is not None:
            return got
    every = _part_forms(part)
    if every is not None and not (every & _line_forms(forms, seen)):
        if seen is not None:
            seen[id(part)] = []
        return []
    alternatives = part if isinstance(part, tuple) else (part,)
    found = []
    for alternative in alternatives:
        if not isinstance(alternative, str) or not alternative.strip():
            continue
        span = _phrase_span(forms, alternative, seen)
        bare_hit = False
        if not span:
            bare = _wanted_bare(alternative)
            if bare is not None:
                span = _phrase_span_bare(forms, bare, seen)
                bare_hit = bool(span)
        if span:
            words, weight = _shape(alternative)
            if bare_hit and weight > BARE_WEIGHT:
                weight = BARE_WEIGHT
            found.append((weight, words, span))
    found.sort(key=lambda hit: (hit[0], not _only_the_frame(hit[1])), reverse=True)
    if seen is not None:
        seen[id(part)] = found
    return found


def _part_match(part, forms, covered=(), seen=None):
    found = _part_matches(part, forms, seen)
    if not found:
        return (0, (), ())
    for weight, words, span in found:
        if not covered or not set(span) <= set(covered):
            return (weight, words, span)
    return found[0]


def _part_score(part, forms, seen=None):
    return _part_match(part, forms, seen=seen)[0]


def _own_words(item):
    words = set()
    for part in item.key or ():
        if isinstance(part, str):
            part = (part,)
        for key in part:
            if not isinstance(key, str):
                continue
            for word in key.strip().lower().split():
                if len(word) >= MIN_TYPO_LENGTH:
                    words.add(word)
    return words


def _misspelt_avoid(item, typed, own=None):
    if own is None:
        own = _own_words(item)
    for word in item.avoid:
        if not isinstance(word, str):
            continue
        key = word.strip().lower()
        if len(key) < MIN_TYPO_LENGTH or " " in key:
            continue
        for typed_word in typed or ():
            if typed_word in own:
                continue
            if typed_word in own:
                continue
            if (len(typed_word) >= MIN_TYPO_LENGTH and not _engine_reads(typed_word)
                    and typed_word[:1] == key[:1] and _one_edit(typed_word, key)):
                return True
    return False


WANTING = ("want to", "wants to", "wanted to", "wanting to", "would like to",
           "would love to", "feel like making", "feel like doing", "feel like baking",
           "feel like cooking", "fancy making", "fancy doing", "fancy baking",
           "fancy cooking", "fancied making", "fancied doing", "thinking of", "planning to",
           "keen to", "hoping to", "in the mood for",
           "need to", "needs to", "needing to", "have to", "has to", "got to", "gotta")


WANT_FILLER = frozenset("to like of in for would feel the mood keen hoping planning thinking love "
                        "plan plans planned".split())

WANT_KNOWING = ("want to know", "wants to know", "wanted to know", "wanting to know",
                "would like to know", "want to find out", "want to check", "want to ask",
                "want to learn", "like to find out", "need to know", "needs to know",
                "need to find out", "need to check", "need to ask", "need to learn")


ASK_PEOPLE = frozenset("""
he him his she her hers they them their theirs we us our ours you your yours
son daughter wife husband partner mum dad mother father child children kids baby boy girl
brother sister nan grandad grandma
""".split())
ASK_PERSON_PRONOUNS = ("he", "she", "they", "we", "you")
ASK_PERSON_POSSESSIVES = ("his", "her", "their", "our", "your")


def _about_someone_else(phrase):
    words = phrase.split()
    if not any(word.lower() in ("i", "me", "my") for word in words):
        return ()
    out = []
    for person in ASK_PERSON_PRONOUNS:
        out.append(" ".join(person if word.lower() in ("i", "me") else word for word in words))
    for person in ASK_PERSON_POSSESSIVES:
        out.append(" ".join(person if word.lower() == "my" else word for word in words))
    return tuple(out)


def _said_about_someone(ask, forms, seen=None):
    line = _line_forms(forms, seen)
    if not any(word in line for word in ASK_PEOPLE):
        return False
    for part in ask or ():
        if seen is not None:
            got = seen.get((_ASK_ABOUT_SOMEONE, id(part)))
            if got is not None and got[0] is forms:
                if got[1]:
                    return True
                continue
        said = False
        for phrase in ((part,) if isinstance(part, str) else part):
            if not isinstance(phrase, str):
                continue
            for variant in _about_someone_else(phrase):
                if _phrase_span(forms, variant, seen):
                    said = True
                    break
            if said:
                break
        if seen is not None:
            seen[(_ASK_ABOUT_SOMEONE, id(part))] = (forms, said)
        if said:
            return True
    return False


def _ask_about_someone_only(ask, forms, seen=None):
    if not ask:
        return False
    if any(_part_score(part, forms, seen) for part in ask):
        return False
    return _said_about_someone(ask, forms, seen)


def _the_subject_it_avoids(item, forms, carried, seen=None):
    if not carried:
        return False
    if not _ask_about_someone_only(item.ask, forms, seen):
        return False
    memo = {}
    for word in item.avoid:
        if isinstance(word, str) and word.strip() and _part_score(word, carried, memo):
            import os, sys
            return True
    return False


def _the_subject_the_line_leans_on(understood):
    leans = understood.get("leans_on")
    if not isinstance(leans, dict):
        return []
    words = leans.get("words") if isinstance(leans.get("words"), list) else []
    return [_forms(word) for word in words
            if isinstance(word, str) and word.strip().lower() not in ASK_PEOPLE][:CONTEXT_WORDS]


def _the_ask_said(ask, forms, seen=None):
    if not ask:
        return True
    if any(_part_score(part, forms, seen) for part in ask):
        return True
    return _said_about_someone(ask, forms, seen)


def _wanting(forms, seen=None):
    if seen is not None:
        got = seen.get(_WANTING)
        if got is not None and got[0] is forms:
            return got[1]
    if _part_score(WANT_KNOWING, forms, seen) > 0:
        answer = False
    else:
        answer = _part_score(WANTING, forms, seen) > 0
    if seen is not None:
        seen[_WANTING] = (forms, answer)
    return answer


def _only_the_want(item, forms, seen=None):
    return not _the_ask_said(item.ask, forms, seen) if item.ask else False


def _key_on_the_want(item, forms, seen=None):
    for part in item.key:
        for alternative in (part if isinstance(part, tuple) else (part,)):
            if not isinstance(alternative, str):
                continue
            if set(alternative.lower().split()) & WANT_FILLER and _part_score(
                    alternative, forms, seen):
                return True
    return False


DENY_SAID_OF = frozenset("""i im ive we were he hes she shes they theyre it its there am is are
    was were""".split())
DENIERS = frozenset("""not no dont doesnt didnt isnt arent wasnt werent aint""".split())
STATES_AFTER = frozenset("having getting being been in".split())
DENY_BETWEEN = frozenset("""really still even any more all at very too quite a an the""".split())


def _denier_inside(covered, forms, index):
    back = 2
    while back <= 4 and index - back >= 0:
        at = index - back
        if at not in covered:
            return False
        if forms[at] & DENIERS:
            return True
        back += 1
    return False


def _denied(forms, covered):
    for index in covered:
        if index - 1 in covered and forms[index - 1] & DENIERS:
            continue
        if _denier_inside(covered, forms, index):
            continue
        back = 1
        while back <= 4 and index - back >= 0:
            before = forms[index - back]
            if before & DENIERS:
                subject = index - back - 1
                if subject < 0 or not forms[subject] & DENY_SAID_OF:
                    break
                between = forms[index - back + 1:index]
                if any(word & STATES_AFTER for word in between) and all(
                        word & (STATES_AFTER | DENY_BETWEEN) for word in between):
                    return True
                break
            if not before & DENY_BETWEEN and not before & STATES_AFTER:
                break
            back += 1
    return False


_FRAME_MASK = object()

ASK_FRAME = frozenset("""
    how hows what whats which who whom whose when where why
    is are was were am be been can could should would will shall may might must
    do does did doing i im get gets got getting
    """.split())
WHEN_WORDS = frozenset(TIME_WORDS | {word + "s" for word in TIME_WORDS} | {"bedtime"})
A_LENGTH_WORD = frozenset("""
    long last lasts lasted lasting keep keeps kept take takes taking time times run runs
    minute minutes hour hours day days week weeks month months year years
    """.split())

A_STAND_IN = frozenset("""
    it its itself they them their theirs this that these those you your we us our
    """.split())

A_SAYS_NOTHING = ASK_FRAME | WHEN_WORDS | A_LENGTH_WORD | A_STAND_IN


def _only_the_frame(words):
    return bool(words) and all(word in ASK_FRAME for word in words)


_TAKE_OFF = None


def _says_removal(forms):
    global _TAKE_OFF
    if _TAKE_OFF is None:
        _TAKE_OFF = (_forms("off"), _forms("out"), _forms("of"))
    off, out, of = _TAKE_OFF
    for index, word in enumerate(forms):
        if not word:
            continue
        if word & off:
            return True
        if out and of and index + 1 < len(forms) and word & out and forms[index + 1] & of:
            return True
    return False


FRAME_WORDS = ("without",)
FRAME_ENDS = frozenset(("and", "but", "or", "so", "then", "when", "if", "because", "while",
                        "which", "that", "to", "for", "with", "plus", "except", "besides"))
FRAME_PRONOUNS = frozenset("it its them they this that those these he she him his her".split())
_FRAME_PRONOUN_FORMS = None


def _frame_pronoun_forms():
    global _FRAME_PRONOUN_FORMS
    if _FRAME_PRONOUN_FORMS is None:
        got = frozenset()
        for word in FRAME_PRONOUNS:
            got |= _forms(word)
        _FRAME_PRONOUN_FORMS = got
    return _FRAME_PRONOUN_FORMS


def _the_subjects_own_clause(here):
    if not here or not here[0]:
        return False
    mine = _frame_pronoun_forms()
    if here[0] & mine:
        return True
    if not any(str(form).endswith("ing") for form in here[0]):
        return False
    return any(word and word & mine for word in here[1:3])


def _a_clause_about_the_thing(forms):
    starts, _end_forms = _frame_starts()
    for index, here in enumerate(forms):
        if not here:
            continue
        for first_forms, words in starts:
            if not here & first_forms:
                continue
            span = forms[index:index + len(words)]
            if len(span) == len(words) and all(
                    word and word & _forms(wanted) for word, wanted in zip(span, words)):
                after = index + len(words)
                if _the_subjects_own_clause(forms[after:after + 3]):
                    return True
    return False


def _frame_starts():
    global _FRAME_STARTS
    if _FRAME_STARTS is None:
        starts = []
        for phrase in FRAME_WORDS:
            words = phrase.split()
            starts.append((_forms(words[0]), tuple(words)))
        end_forms = frozenset()
        for word in FRAME_ENDS:
            end_forms |= _forms(word)
        _FRAME_STARTS = (starts, end_forms)
    return _FRAME_STARTS


_FRAME_STARTS = None


def _frame_masked(forms):
    starts, end_forms = _frame_starts()
    found = set()
    dead = set()
    index = 0
    while index < len(forms):
        here = forms[index]
        hit = None
        if here:
            for first_forms, words in starts:
                if not here & first_forms:
                    continue
                span = forms[index:index + len(words)]
                if len(span) == len(words) and all(
                        word and word & _forms(wanted) for word, wanted in zip(span, words)):
                    hit = words[0]
                    index += len(words) - 1
                    break
        if hit is None:
            index += 1
            continue
        found.add(hit)
        index += 1
        while index < len(forms):
            if forms[index] and forms[index] & end_forms:
                break
            dead.add(index)
            index += 1
    if not found:
        return forms, frozenset()
    return [frozenset() if at in dead else word for at, word in enumerate(forms)], frozenset(found)


def _key_names(frame_words, item):
    for part in item.key:
        for alternative in (part if isinstance(part, tuple) else (part,)):
            if isinstance(alternative, str) and set(alternative.lower().split()) & frame_words:
                return True
    return False


def _unframed(forms, seen):
    if seen is not None:
        got = seen.get(_FRAME_MASK)
        if got is not None and got[0] is forms:
            return got[1], got[2], got[3]
    masked, frame_words = _frame_masked(forms)
    memo = seen if masked is forms else {}
    if seen is not None:
        seen[_FRAME_MASK] = (forms, masked, memo, frame_words)
    return masked, memo, frame_words


ASK_PHRASE_WORDS = frozenset(("best", "way", "ways"))
_ASK_PHRASE_MASK = object()


def _without_ask_phrase(forms, seen):
    span = ()
    for phrase in ("best way", "best ways", "how best"):
        span = _phrase_span(forms, phrase, seen)
        if span:
            break
    if not span:
        return forms, seen
    if seen is not None:
        got = seen.get(_ASK_PHRASE_MASK)
        if got is not None and got[0] is forms:
            return got[1], got[2]
    masked = list(forms)
    for at in span:
        masked[at] = frozenset()
    masked = tuple(masked)
    memo = {} if seen is not None else None
    if seen is not None:
        seen[_ASK_PHRASE_MASK] = (forms, masked, memo)
    return masked, memo


REPORT_LEADS = frozenset((
    "i", "im", "ive", "am", "have", "has", "had", "got", "get", "gets", "getting", "keep",
    "keeps", "keeping", "feel", "feels", "felt", "feeling", "been", "was", "suffer", "suffering",
    "think", "thought", "reckon", "suspect", "probably", "maybe", "definitely", "sure"))
REPORT_PERSON = frozenset((
    "son", "sons", "daughter", "daughters", "child", "children", "kid", "kids", "boy", "girl",
    "baby", "toddler", "little", "youngest", "eldest", "oldest", "teen", "teenager", "lad",
    "lass", "he", "she", "him", "her", "they", "them", "husband", "wife", "partner",
    "boyfriend", "girlfriend", "fiance", "fiancee", "friend", "friends", "mate", "mates",
    "mother", "mum", "mom", "father", "dad", "nan", "nana", "grandma", "grandad", "granny",
    "brother", "brothers", "sister", "sisters", "parent", "parents", "boss", "carer",
    "his", "her", "their", "our", "one"))

REPORT_FILLER = REPORT_LEADS | REPORT_PERSON | frozenset((
    "a", "an", "the", "my", "me", "really", "very", "so", "too", "just", "still", "also",
    "suddenly", "quite", "bit", "lot", "of", "with", "and", "at", "in", "on", "today", "now"))


HAPPENING_AGAIN = frozenset((
    "again", "back", "still", "already", "anyway", "now", "once", "twice", "more", "every",
    "year", "season", "spring", "summer", "autumn", "winter", "time", "times", "keeps", "keep",
    "kept", "coming", "come", "came", "going", "goes", "went", "on", "round", "around", "at",
    "as", "usual", "this", "same", "the", "it", "its", "is", "are", "was", "were", "has", "have",
    "had", "here", "today", "tonight", "morning", "night", "week", "month", "of", "in", "and",
    "so", "but", "though", "now", "first", "before", "like", "last"))


def _said_again(forms, covered, typed=None):
    if not covered:
        return False
    if isinstance(typed, (list, tuple)) and len(typed) == len(forms):
        words = [str(word).lower() for word in typed]
    else:
        words = []
        for group in forms:
            forms_of_word = sorted(str(form).lower() for form in group) if group else []
            words.append(forms_of_word[0] if forms_of_word else "")
    last = max(covered)
    after = words[last + 1:]
    if not after:
        return False
    return all(word in HAPPENING_AGAIN or word in REPORT_FILLER for word in after)


def _bare_report(forms, covered, typed=None):
    if not covered:
        return False
    if isinstance(typed, (list, tuple)) and len(typed) == len(forms):
        words = [str(word).lower() for word in typed]
    else:
        words = []
        for group in forms:
            forms_of_word = sorted(str(form).lower() for form in group) if group else []
            words.append(forms_of_word[0] if forms_of_word else "")
    first = min(covered)
    lead = False
    person = False
    for index in range(first):
        word = words[index]
        if word in REPORT_LEADS:
            lead = True
            continue
        if word in REPORT_PERSON:
            person = True
            continue
        if word in REPORT_FILLER:
            continue
        return False
    if person and not lead:
        return False
    return lead


EXPLAIN_LEADS = frozenset((
    "what", "whats", "explain", "explained", "definition", "define", "meaning", "describe",
    "tell", "info", "information", "basics", "overview"))
EXPLAIN_FILLER = EXPLAIN_LEADS | frozenset((
    "s", "is", "are", "was", "does", "do", "did", "a", "an", "the", "of", "about", "on", "in",
    "for", "me", "us", "my", "mean", "means", "meant", "by", "symptom", "symptoms", "sign",
    "signs", "cause", "causes", "treatment", "exactly", "actually", "please", "and", "more"))


def _asks_to_explain(forms, start, typed=None):
    if not start or start > 12:
        return False
    if isinstance(typed, (list, tuple)) and len(typed) == len(forms):
        words = [str(word).lower() for word in typed]
    else:
        words = []
        for group in forms:
            forms_of_word = sorted(str(form).lower() for form in group) if group else []
            words.append(forms_of_word[0] if forms_of_word else "")
    lead = False
    for index in range(start):
        word = words[index]
        if word in EXPLAIN_LEADS:
            lead = True
            continue
        if word in EXPLAIN_FILLER:
            continue
        return False
    return lead


def _only_as_a_kind(forms, span, covered, item, typed=None):
    if len(span) != 1:
        return False
    start = min(span)
    if start < 1:
        return False
    if isinstance(typed, (list, tuple)) and len(typed) == len(forms):
        words = [str(word).lower() for word in typed]
    else:
        words = []
        for group in forms:
            forms_of_word = sorted(str(form).lower() for form in group) if group else []
            words.append(forms_of_word[0] if forms_of_word else "")
    if start - 1 >= len(words):
        return False
    if words[start - 1] not in AS_A_KIND:
        return False
    asked = set()
    for part in (item.ask or ()):
        for alternative in ((part,) if isinstance(part, str) else part):
            for word in str(alternative).lower().split():
                asked.add(word)
                asked |= {str(form).lower() for form in _forms(word)}
    said = set()
    for index in covered:
        if index in span or index >= len(words):
            continue
        said.add(words[index])
    said.discard("")
    return all(word in asked or word in EXPLAIN_FILLER for word in said)


def _says_a_shape(shapes, typed, forms):
    if isinstance(typed, (list, tuple)) and len(typed) == len(forms):
        words = [str(word).lower() for word in typed]
    else:
        words = []
        for group in forms:
            forms_of_word = sorted(str(form).lower() for form in group) if group else []
            words.append(forms_of_word[0] if forms_of_word else "")
    line = " ".join(word for word in words if word)
    if not line:
        return False
    for shape in shapes:
        try:
            if shape(line):
                return True
        except Exception:
            continue
    return False


def score(item, forms, typed=None, seen=None, frame=True, framed=False):
    if not forms:
        return 0
    if typed and _under_their_own_hands(item, typed):
        return 0
    masked, memo, frame_words = _unframed(forms, seen) if frame else (forms, seen, frozenset())
    if frame_words and not _key_names(frame_words, item):
        forms, seen = masked, memo
    framed_one = bool(framed and item.key and getattr(item, "id", "") in ASK_FRAME_IDS
                      and _the_whole_subject(item.key[0], forms, seen))
    if not item.report and not item.explain and not framed_one and not item.shape \
            and not _two_positions(forms, item):
        return 0
    if item.ask and not _the_ask_said(item.ask, forms, seen):
        if not _wanting(forms, seen) or _key_on_the_want(item, forms, seen):
            return 0
    total = 0
    covered = []
    first = ()
    removal = _says_removal(forms)
    grouped = any(isinstance(part, (tuple, list, frozenset, set))
                  for part in (item.key or ()))
    for index, part in enumerate(item.key):
        weight, words, span = _part_match(part, forms, covered, seen)
        if index == 0 and typed and len(span) == 1 and span[0] < len(typed) \
                and _asking_with(typed, span[0]):
            bare = list(forms)
            bare[span[0]] = frozenset()
            weight, _, span = _part_match(part, bare, covered)
        elif (index and removal and weight > 1 and _only_the_frame(words)
              and len(first) < 2):
            spare = [hit for hit in _part_matches(part, forms)
                     if not _only_the_frame(hit[1])]
            if spare:
                weight, words, span = spare[0]
            else:
                weight = 1 if len(words) == 1 else 0
        total += weight
        covered.extend(span)
        if index == 0:
            first = span
    if grouped and not first:
        return 0
    bare = bool(item.report) and (_bare_report(forms, covered, typed)
                                  or _said_again(forms, covered, typed))
    shaped = bool(item.shape) and bool(first) and _says_a_shape(item.shape, typed, forms)
    explained = bool(item.explain) and bool(first) and _asks_to_explain(forms, min(first), typed)
    if first and not explained and _only_as_a_kind(forms, first, covered, item, typed):
        return 0
    one_word = len(set(covered)) < 2
    if one_word and not bare and not explained:
        if not framed_one and not shaped:
            return 0
    if bare or shaped or explained:
        total += WORD_WEIGHT
    if _denied(forms, covered):
        return 0
    if not one_word and total < MIN_SCORE:
        return 0
    parts_said = _body_parts(typed) if typed else None
    ask_forms = ask_seen = None
    for word in item.avoid:
        key = word.strip().lower() if isinstance(word, str) else ""
        if key in ASK_PHRASE_WORDS:
            if ask_forms is None:
                ask_forms, ask_seen = _without_ask_phrase(forms, seen)
            if _part_score(word, ask_forms, ask_seen):
                return 0
        elif _part_score(word, forms, seen) or _phrase_span_between(forms, word, seen):
            if not _a_part_the_line_does_not_have(word, parts_said):
                return 0
    if typed and _misspelt_avoid(item, typed):
        return 0
    failing_at = _keeps_failing_at(forms, seen)
    if failing_at is not None and _keeping_row(item) and (
            not first or min(first) != failing_at + 1):
        return 0
    return total


PACK_DATE = ("past the date", "past its date", "past their date", "past the use by",
             "use by date", "use by", "sell by", "best before", "out of date",
             "after the date", "after its date", "after their date", "date on it",
             "date on the", "date says", "date said")

DAY_WORDS = ("next day", "the next day", "the day after", "day after", "yesterday",
             "tomorrow", "tomorow", "tmrw", "tomoz")

ASKS_FOR_THE_HANDS = re.compile(
    r"\b(?:can|could|would|will|are|do)\s+(?:you|u)\b|\b(?:for|help)\s+(?:me|us)\b")
A_HAND_OR_EYE_DOES_IT = re.compile(
    r"\b(?:fill|fills|filling|sign|signs|signing|print|prints|printing|scan|scans|scanning|"
    r"open|opens|opening|read|reads|reading|check|checks|checking|complete|completes|"
    r"completing|translate|translates|translating|look\s+(?:at|through|over))\b")
ASKS_WHAT_IT_SAYS = re.compile(
    r"\b(?:what|whether|if)\b|\b(?:means?|meaning|says?|explain|explains|explaining|"
    r"understand|summar\w+|translate\w*|about\s+it)\b")
OWN_THING_ON_THEIR_SIDE = re.compile(
    r"\b(?:my|our|this|that|these|those|the)\s+(?:[a-z']+\s+){0,2}"
    r"(?:form|forms|pdf|pdfs|file|files|document|documents|paperwork|scan|scans|"
    r"screenshot|screenshots|photo|photos|letter|letters|invoice|invoices|contract|"
    r"application|applications|cv|questionnaire|questionnaires)\b")
THEIR_OWN_HANDS_THINGS = frozenset("""form forms pdf pdfs file files document documents paperwork
    scan scans screenshot screenshots photo photos letter letters invoice invoices contract
    application applications cv questionnaire questionnaires""".split())


def _under_their_own_hands(item, typed):
    line = " ".join(str(word).lower() for word in typed)
    if not ASKS_FOR_THE_HANDS.search(line) or not A_HAND_OR_EYE_DOES_IT.search(line):
        return False
    if ASKS_WHAT_IT_SAYS.search(line):
        return False
    if not OWN_THING_ON_THEIR_SIDE.search(line):
        return False
    said = set()
    for part in (item.key or ()):
        for alternative in ((part,) if isinstance(part, str) else part):
            said |= {piece for piece in str(alternative).lower().split()}
    return bool(said & THEIR_OWN_HANDS_THINGS)


A_HOUSE_WARMING_UP = ("heating", "boiler", "boilers", "radiator", "radiators", "thermostat",
                      "central heating", "hot water", "immersion", "combi", "flue", "trv",
                      "house", "the flat", "my flat", "our flat", "room", "rooms", "bathroom",
                      "kitchen", "bedroom", "living room", "overnight", "no heat")

A_WEATHER_ASK = ("weather like", "weather doing", "weather going to be", "weather forecast",
                 "what is the weather", "whats the weather", "what's the weather",
                 "wether like", "whats the forecast", "what's the forecast", "the forecast for",
                 "is it cold outside", "is it cold today", "is it cold out", "is it cold enough",
                 "is it warm outside", "is it warm today", "is it warm enough",
                 "is it hot outside", "is it hot today", "is it hot enough",
                 "is it freezing", "is it raining", "is it snowing",
                 "warm enough to", "cold enough to", "how cold is it", "how hot is it",
                 "how warm is it", "what is it like outside", "whats it like outside",
                 "what's it like outside")

A_WHAT_TO_WEAR = ("what should i wear", "what do i wear", "what to wear", "what shall i wear",
                  "what should i put on", "what do i put on", "what to put on",
                  "what should he wear", "what should she wear", "what should they wear",
                  "what should we wear", "what does he wear", "what does she wear",
                  "what should i pack", "what do i pack", "what to pack", "what shall i pack",
                  "what should i take", "what do i take", "what to take", "what should i bring",
                  "what do i bring", "what to bring", "what do i need to take",
                  "what do i need to bring", "what kit", "what clothes", "which clothes",
                  "what should i put in my bag", "what do i need to wear")

KEPT_FOODS = ("bread", "loaf", "loaves", "rolls", "bagels", "milk", "butter", "cheese",
              "yoghurt", "yogurt", "cream", "eggs", "egg", "meat", "chicken", "beef",
              "pork", "lamb", "bacon", "ham", "sausages", "sausage", "fish", "salmon",
              "prawns", "rice", "pasta", "noodles", "potatoes", "potato", "flour", "oats",
              "cereal", "soup", "stew", "sauce", "gravy", "cake", "biscuits", "cookies",
              "chocolate", "fruit", "apples", "bananas", "berries", "strawberries", "salad",
              "lettuce", "spinach", "carrots", "mushrooms", "tomatoes", "onions", "peas",
              "beans", "leftovers", "leftover", "sandwich", "sandwiches", "hummus", "nuts")

KEEPING_WORDS = ("store", "stores", "stored",
                 "storing", "storage", "last", "lasts", "lasted", "fresh", "fresher",
                 "freshness", "stale", "staler", "stales", "staleness", "mould", "moulds",
                 "mouldy", "mold", "molds", "moldy", "mildew", "mildewy", "goes off",
                 "go off", "gone off", "going off", "goes bad", "gone bad", "goes hard",
                 "gone hard", "goes soggy", "gone soggy", "fridge", "freezer", "freeze",
                 "freezing", "bin", "shelf life", "cold", "warm", "damp", "how long",
                 "longer", "longest", "keep fresh", "use by", "best before")


GOES_IN = re.compile(r"\b(?:go|goes|going|went)\s+(?:in|into)\b|\bputs?\s+in\b", re.I)
COUNTED_INTO_A_THING = re.compile(
    r"\bhow many\b[^?]*\b(?:in|into|for)\s+(?:a|an|the|my|one|two|three|four|six|\d+)\s+"
    r"(?!days?\b|weeks?\b|months?\b|years?\b|mornings?\b|evenings?\b|sittings?\b|"
    r"meals?\b|servings?\b|serving\b|portion\b|portions\b|time\b)", re.I)
HOW_MANY_DAYS = re.compile(r"\bhow many (?:days|weeks|months)\b", re.I)
KEEPS_OR_STORES = re.compile(
    r"\b(?:keep|keeps|kept|keeping|store|stores|stored|storing|last|lasts|lasting|"
    r"fridge|freezer|freeze|go off|gone off)\b", re.I)


def not_a_count_for_the_box_or_the_dish(understood):
    if not isinstance(understood, dict):
        return True
    text = " " + str(understood.get("clean") or understood.get("text") or "").lower() + " "
    if (GOES_IN.search(text) or HOW_MANY_DAYS.search(text) or KEEPS_OR_STORES.search(text)
            or COUNTED_INTO_A_THING.search(text)):
        return False
    return True


def a_food_is_being_kept(understood):
    if not isinstance(understood, dict):
        return False
    text = " " + str(understood.get("norm_text") or understood.get("clean") or "").lower() + " "
    if not any(word in text for word in KEEPING_WORDS):
        return False
    words = understood.get("words") or ()
    said = {str(word).lower() for word in words}
    for food in KEPT_FOODS:
        if " " in food:
            if food in text:
                return True
        elif food in said or (" " + food + " ") in text:
            return True
    return False


CONTAINERS = ("bag", "bags", "bin bag", "bin bags", "bin", "bins", "box", "boxes",
              "packet", "packets", "pack", "packs", "tin", "tins", "jar", "jars", "tub",
              "tubs", "container", "containers", "lunchbox", "lunch box", "sack", "sacks",
              "suitcase", "suitcases", "rucksack", "rucksacks", "backpack", "backpacks",
              "handbag", "handbags", "luggage", "basket", "baskets", "crate", "crates",
              "tray", "trays", "drawer", "drawers", "cupboard", "cupboards", "shelf",
              "shelves", "fridge", "freezer")


def only_a_container(understood, names):
    if not isinstance(understood, dict):
        return False
    text = " " + " ".join(str(word).lower() for word in (understood.get("words") or ())) + " "
    found = [one for one in names if " " + one + " " in text]
    return bool(found) and all(one in CONTAINERS for one in found)


A_HOURS_ASK = ("what time does", "what time do", "what time is the", "what time are the",
               "opening hours", "opening times", "opening time", "closing time",
               "closes at", "closes today", "closes tonight", "shuts at", "shuts today",
               "close today", "close tonight", "close on", "open today", "open now",
               "open on", "is it open", "is it shut", "open until", "open till",
               "till what time", "until what time", "last entry", "last orders")

DISH_ASK = ("make with", "made with", "make using", "make from", "make out of",
            "what can i make", "what can i cook", "what should i make", "what can i do with",
            "what should i do with", "cook with", "cooking with", "do with", "using up",
            "for dinner", "for tea", "for lunch", "for supper", "for breakfast", "tonights tea",
            "something with", "dish with")


_KEEPING_VERB = frozenset(("keep", "keeps", "kept", "keeping"))
_RESULT_VERB = frozenset(("coming", "comes", "come", "turning", "turns", "turn"))
_SPOILING = frozenset((
    "mouldy", "moldy", "mould", "mold", "moulding", "molding", "slimy", "slimy", "soggy",
    "mushy", "sour", "soured", "souring", "rancid", "stale", "wilted", "wilting", "wilt",
    "limp", "off", "bad", "rotten", "rotting", "rot", "brown", "browned", "browning",
    "discoloured", "discolored", "curdled", "curdling", "curdle", "smelly", "smelling",
    "stinking", "sprouting", "sprouted", "spotted", "furry", "fuzzy", "blue", "green",
    "shrivel", "shrivelled", "shriveling",
))
_ING_NOUNS = frozenset((
    "evening", "evenings", "morning", "mornings", "ceiling", "building", "feeling", "feelings",
    "meeting", "meetings", "wedding", "pudding", "stuffing", "dressing", "filling", "parking",
    "clothing", "bedding", "writing", "painting", "drawing", "reading", "heating", "lighting",
    "awning", "herring", "sterling", "seedling", "sibling", "dumpling", "spring", "springs",
    "string", "strings", "thing", "things", "ring", "rings", "king", "wing", "wings",
))

_KEEPING_KEY = frozenset(("keep", "keeps", "kept", "keeping"))
_LIFE_KEY = frozenset(("how long", "shelf life", "shelf-life", "store", "stores", "storing",
                       "stored", "storage", "last", "lasts", "lasted", "lasting", "fresh",
                       "fresh for", "still good", "gone off", "out of date", "use by"))
_KEEPING_ROWS = {}


def _keeping_row(item):
    known = _KEEPING_ROWS.get(id(item))
    if known is None:
        keeps = False
        lives = False
        for part in item.key:
            for alternative in (part if isinstance(part, tuple) else (part,)):
                if not isinstance(alternative, str):
                    continue
                shaped = alternative.strip().lower()
                if shaped in _KEEPING_KEY:
                    keeps = True
                elif shaped in _LIFE_KEY:
                    lives = True
        known = keeps and lives
        _KEEPING_ROWS[id(item)] = known
    return known


def _gerund(forms, index):
    for form in forms[index]:
        if form in _ING_NOUNS or len(form) < 5 or not form.endswith("ing"):
            continue
        return form
    return ""


def _later_words(forms, index, reach=3):
    seen = set()
    for step in range(index, min(index + reach, len(forms))):
        seen |= forms[step]
    return seen


_RECURRING = frozenset((
    "getting", "happening", "happens", "recurring", "returning", "flaring", "cropping"))
_RECURRING_ANYWAY = frozenset(("coming", "going", "giving"))
_RECURRING_WITH = frozenset(("back", "again", "around", "round", "on"))


def _keeps_failing_at(forms, seen=None):
    if seen is not None:
        got = seen.get("keeps-failing-at")
        if got is not None:
            return None if got is False else got
    failing = None
    for index in range(len(forms) - 1):
        if not (forms[index] & _KEEPING_VERB):
            continue
        gerund = _gerund(forms, index + 1)
        if not gerund:
            continue
        if gerund in _RECURRING:
            continue
        if gerund in _RECURRING_ANYWAY and _later_words(forms, index + 1) & _RECURRING_WITH:
            continue
        result = (_later_words(forms, index + 1) & frozenset(("out",))
                  and (_later_words(forms, index + 1) & _RESULT_VERB
                       or gerund in _RESULT_VERB))
        if result or not (_later_words(forms, index + 1) | {gerund}) & _SPOILING:
            failing = index
            break
    if seen is not None:
        seen["keeps-failing-at"] = False if failing is None else failing
    return failing


def _keeps_failing(forms, seen=None):
    return _keeps_failing_at(forms, seen) is not None
_SUBJECT_POINTS = frozenset("a an the my your our his her its it of in on at for to".split())


def _the_whole_subject(part, forms, seen=None):
    span = set()
    for _weight, _words, hit in _part_matches(part, forms, seen):
        span.update(hit)
    wanted = [index for index, word_forms in enumerate(forms)
              if not (word_forms & _SUBJECT_POINTS)]
    return bool(wanted) and all(index in span for index in wanted)


MACHINE_SOUNDS = ("hum", "hums", "humming", "hummed", "buzz", "buzzes", "buzzing", "drone",
                  "drones", "droning", "vibrate", "vibrates", "vibrating", "vibration",
                  "whistle", "whistles", "whistling", "whine", "whines", "whining",
                  "squeal", "squeals", "squealing", "squeak", "squeaks", "squeaking",
                  "screech", "screeches", "screeching", "shriek", "shrieks", "shrieking",
                  "hiss", "hisses", "hissing", "gurgle", "gurgles", "gurgling", "glug",
                  "glugging", "bang", "bangs", "banging", "knock", "knocks", "knocking",
                  "rumble", "rumbles", "rumbling", "clunk", "clunks", "clunking", "clank",
                  "clanks", "clanking", "rattle", "rattles", "rattling", "tick", "ticks",
                  "ticking", "tap", "taps", "tapping", "click", "clicks", "clicking",
                  "thump", "thumps", "thumping", "roar", "roaring", "grind", "grinds",
                  "grinding", "scrape", "scrapes", "scraping")


def _rarity(entries):
    counts = {}
    for item in entries:
        words = set()
        for part in item.key:
            for alternative in (part if isinstance(part, tuple) else (part,)):
                if isinstance(alternative, str):
                    words.update(alternative.lower().split())
        for word in words:
            counts[word] = counts.get(word, 0) + 1
    return counts


_TAIL_ASK_WORDS = None


def _the_tail_asks_about(forms):
    global _TAIL_ASK_WORDS
    if _TAIL_ASK_WORDS is None:
        _TAIL_ASK_WORDS = frozenset().union(*(_forms(word) for word in (
            "what", "whats", "which", "how", "where", "when", "who", "why", "should", "shall",
            "could", "would", "can")))
    ask_words = _TAIL_ASK_WORDS
    for index in range(len(forms) - 1, 3, -1):
        word = forms[index]
        if word and (word & ask_words):
            return index
    return -1


def _rank(item, forms, rarity, seen=None):
    tail_from = _the_tail_asks_about(forms)
    matched = [_part_match(part, forms, seen=seen) for part in item.key]
    said = sum(weight for weight, words, span in matched
               if weight and not (tail_from >= 0 and min(span) >= tail_from
                                  and _only_the_frame(words)))
    total = 0
    says_what = False
    for part in item.key:
        weight, words, span = _part_match(part, forms, seen=seen)
        if weight and said > 2 and tail_from >= 0 and min(span) >= tail_from \
                and _only_the_frame(words):
            continue
        total += weight + sum(1 for word in words if rarity.get(word, 0) == 1)
        if any(word not in ASK_FRAME and word not in WHEN_WORDS and word not in A_LENGTH_WORD
               and word not in A_STAND_IN for word in words):
            says_what = True
    if not says_what:
        return 1
    return total + item.bias


_CACHE = {}
_CACHE_KEEP = 6


def _key_words(item):
    words = set()
    for part in item.key:
        for alternative in (part if isinstance(part, tuple) else (part,)):
            if isinstance(alternative, str):
                words.update(alternative.lower().split())
    return words


_KEY_FORMS = {}


def _key_forms(item):
    got = _KEY_FORMS.get(id(item))
    if got is not None and got[0] is item:
        return got[1]
    forms = set()
    for part in item.key:
        for alternative in (part if isinstance(part, tuple) else (part,)):
            if isinstance(alternative, str):
                for word in alternative.lower().split():
                    forms |= _forms(word)
    forms = frozenset(forms)
    if len(_KEY_FORMS) >= _FORMS_CACHE_KEEP:
        _KEY_FORMS.clear()
    _KEY_FORMS[id(item)] = (item, forms)
    return forms


def _two_positions(forms, item):
    key = _key_forms(item)
    found = False
    for word_forms in forms:
        if not word_forms.isdisjoint(key):
            if found:
                return True
            found = True
    return False


def _word_index(entries):
    cached = _INDEX.get(id(entries))
    if cached is not None and cached[0] is entries:
        return cached[1]
    index = {}
    for position, item in enumerate(entries):
        for word in _key_words(item):
            for form in _forms(word):
                at = index.get(form)
                if at is None:
                    index[form] = [position]
                elif at[-1] != position:
                    at.append(position)
    while len(_INDEX) >= _CACHE_KEEP:
        _INDEX.pop(next(iter(_INDEX)))
    _INDEX[id(entries)] = (entries, index)
    return index


_INDEX = {}


def _reaching(entries, forms):
    index = _word_index(entries)
    hit = set()
    for word_forms in forms:
        for form in word_forms:
            positions = index.get(form)
            if positions:
                hit.update(positions)
    if not hit:
        return entries
    return [entries[position] for position in sorted(hit)]


def _domain_rarity(entries):
    by_domain, every = {}, {}
    owners = {}
    for item in entries:
        domain = getattr(item, "domain", "") or ""
        counts = by_domain.setdefault(domain, {})
        words = set()
        for part in item.key:
            for alternative in (part if isinstance(part, tuple) else (part,)):
                if isinstance(alternative, str):
                    words.update(alternative.lower().split())
        for word in words:
            counts[word] = counts.get(word, 0) + 1
            owners.setdefault(word, set()).add(getattr(item, "id", None) or id(item))
    for word in owners:
        if owners[word] <= SLIPS.get(word, set()):
            continue
        every[word] = len(owners[word])
    return by_domain, every


def _vocabulary(entries):
    cached = _CACHE.get(id(entries))
    if cached is not None and cached[0] is entries:
        return cached[1], cached[2], cached[3]
    by_domain, every = _domain_rarity(entries)
    slips = {slip.lower() for item in entries for slip in getattr(item, "slips", ())}
    every = {word: count for word, count in every.items() if word.lower() not in slips}
    known = set()
    for word in every:
        known |= _forms(word)
    if all(getattr(item, "domain", "") for item in entries):
        while len(_CACHE) >= _CACHE_KEEP:
            _CACHE.pop(next(iter(_CACHE)))
        _CACHE[id(entries)] = (entries, by_domain, every, known)
    return by_domain, every, known


NOT_THE_ADJECTIVE = frozenset("""
    ready busy handy party army belly copy body study lady fully funny pity cosy policy every
    bully tally holy early rally holly jelly apply battery cheeky dicky factory fairy gravy
    irony kindly multiply pasty silly shiny story whisky clammy telly chilly watery shivery
    sticky
""".split())


def _y_word_stems(word):
    if len(word) < 5 or not word.endswith("y") or word[-2] in "aeiouy":
        return ()
    if word in NOT_THE_ADJECTIVE:
        return ()
    stem = word[:-1]
    return tuple(form for form in (stem, stem + "e") if len(form) >= MIN_FORM)


def _a_word_itself(word):
    return (word in _COMMON or word in COMMON_WORDS or word in lexicon.CHAT
            or word in lexicon.EXPAND)


def _read_the_adjective(words, forms, vocabulary):
    gave = False
    for index, word in enumerate(words):
        if _a_word_itself(word):
            continue
        for stem in _y_word_stems(word):
            if stem in vocabulary and stem not in forms[index]:
                forms[index] |= {stem}
                gave = True
    return gave


_A_PERSON = frozenset(PEOPLE_MALE) | frozenset(PEOPLE_FEMALE) | frozenset((
    "friend", "mate", "friends", "partner", "child", "children", "kid", "kids", "baby",
    "neighbour", "neighbor", "colleague", "boss", "teacher", "someone", "somebody", "cousin",
    "person", "people", "they", "them", "we", "us", "you"))
_NOT_A_THING_HAD = frozenset(("to", "had", "been", "being", "it", "them", "not", "no", "never",
                              "nothing", "none", "enough", "already", "yet"))


def _read_a_thing_had(words, forms):
    for index, word in enumerate(words):
        if str(word).lower() != "has":
            continue
        after = str(words[index + 1]).lower() if index + 1 < len(words) else ""
        if after in _NOT_A_THING_HAD:
            continue
        if after == "got" and index + 2 < len(words) and str(words[index + 2]).lower() == "to":
            continue
        before = [str(word).lower() for word in words[max(0, index - 4):index]]
        if not any(word in _A_PERSON for word in before):
            continue
        forms[index] |= _forms("have")


def _read_typos(words, forms, vocabulary, known):
    for index, word in enumerate(words):
        if forms[index] & known or _engine_reads(word):
            continue
        if "'" in word:
            continue
        forms[index] |= _typo_forms(word, vocabulary)


_FILLER = frozenset(("actually", "really", "honestly", "literally", "genuinely", "basically"))


def _without_possessive(word):
    for tail in ("'s", "\u2019s"):
        if word.endswith(tail):
            return word[:-2]
    return word


FEELING_ABOUT_A_THING = FEELING_WORDS + (
    "sad", "sadness", "unhappy", "scared", "frightened", "lonely", "gutted", "devastated",
    "heartbroken", "annoyed", "annoying", "furious", "cross", "upsetting", "fuming",
)

FEELING_ABOUT = frozenset("about of with over at by".split())

FEELING_ENDS = frozenset("""
    and but because so then when if that which who whom whose or also plus after before since
    till until while though although yet today tomorrow tonight now yesterday again too as
    i im ive id we they he she them us
""".split())

FEELING_NAMES_NOTHING = frozenset("""
    it them everything nothing anything something all
""".split())

FEELING_DOMAINS = frozenset(("family", "friends", "study", "health", "sleep", "pregnancy",
                             "money", "work", "lifeadmin",
                             "body", "wording", "complaints", "travel", "home"))

FEELING_FAULT_WORDS = frozenset("""
    leak leaks leaked leaking drip drips dripping burst bursts bursting broken broke breaks
    blocked blocking stopped stops smoking sparking smells smelly smell damp mould mold
    flooded flooding flood loose wobbles wobbling snapped cracked clicking noisy
""".split())


def _names_a_fault(occasion):
    return bool(FEELING_FAULT_WORDS.intersection(str(word).lower() for word in occasion))


FEELING_SPEAKER = frozenset(("i", "im", "ive", "i'm", "i've", "id", "me", "myself"))


def _speaker_is_feeling(words):
    low = [str(word).lower() for word in words]
    for pos, word in enumerate(low):
        if word not in FEELING_ABOUT_A_THING \
                and not (word == "fed" and low[pos + 1:pos + 2] == ["up"]):
            continue
        for back in low[max(0, pos - 6):pos]:
            if back in FEELING_SPEAKER:
                return True
    return False


FEARED_THINGS = frozenset("""
    dentist dentists dentistry dental flying plane planes flight flights needles needle
    injections injection jab jabs spiders spider snakes snake heights height lifts lift
    escalators dark thunder lightning storms storm blood vomit sick wasps bees mice rats
    clowns hospitals hospital doctors doctor dentists surgery operation operations
    presentations public presentations interviews interview exams exam tests test motorways
    motorway driving flying ferries tunnels enclosed spaces crowds dentists darkness
    water swimming swim pool pools
""".split())


def _names_a_feared_thing(occasion):
    return bool(FEARED_THINGS.intersection(str(word).lower() for word in occasion))


def _feeling_occasion(words):
    low = [str(word).lower() for word in words]
    for pos, word in enumerate(low):
        if word not in FEELING_ABOUT_A_THING \
                and not (word == "fed" and low[pos + 1:pos + 2] == ["up"]):
            continue
        at = pos + 1
        if at < len(low) and low[at] in ("up", "off"):
            at += 1
        if at >= len(low) or low[at] not in FEELING_ABOUT:
            continue
        got = []
        for word_after in low[at + 1:at + 6]:
            if word_after in FEELING_ENDS or not word_after.isalpha():
                break
            got.append(word_after)
        if not [word for word in got if word not in FEELING_NAMES_NOTHING]:
            continue
        return got
    return None


_WHERE_I_PUT = re.compile(r"\bwhere\s+(?:did|have|has|had)\s+i\s+(?:put|leave)\b")
_WHERE_TO_KEEP = re.compile(
    r"\bwhere\s+(?:should|shall|do|can|could|would|will|might|am\s+i\s+to)?\s*(?:to\s+)?"
    r"(?:i\s+|we\s+|you\s+)?(?:keep|store|stow|put\s+away|pack\s+away)\b")
_KEPT_SOMEWHERE = frozenset("""
keep keeps keeping kept store stores stored storing storage stow stows stowed stowing
away loft wardrobe moth moths cedar
""".split())


def _the_kept_rows():
    from . import entries as all_entries
    return [item for item in all_entries() if _key_names(_KEPT_SOMEWHERE, item)]



_HOLDS_MONEY = re.compile(r"\u00a3\s?\d|\b\d+(?:\.\d+)?\s?(?:p|pence|pounds?|quid)\b|"
                          r"\b\d+\.\d{2}\b|\bpounds?\b")


def _a_price_judged_is_not_answered_here(understood, found):
    from .prices import a_price_is_judged
    text = str(understood.get("clean") or understood.get("text") or "")
    if not a_price_is_judged(text):
        return False
    reply = getattr(found, "reply", None)
    if callable(reply):
        try:
            reply = reply({}, understood)
        except Exception:
            return False
    if reply is None:
        reply = ""
    if _HOLDS_MONEY.search(str(reply)):
        return False
    return _a_range_for_the_thing(text, understood) is not None


_THE_THING_JUDGED = re.compile(r"\bfor\s+((?:a|an|the|my|our|this|that|these|those)\s+)?"
                               r"([a-z][a-z' ]{1,40})$", re.I)

_POINTS_AT_IT = frozenset("""
    one ones it that this these those them they him her he she the thing things that one this one
""".split())


def _the_thing_the_chat_is_on(understood):
    understood = understood if isinstance(understood, dict) else {}
    ref = understood.get("ref")
    if isinstance(ref, dict):
        for key in ("it", "that", "they", "them"):
            thing = ref.get(key)
            if thing and str(thing).lower() not in _POINTS_AT_IT:
                return str(thing)
    subject = understood.get("subject")
    if subject and str(subject).lower() not in _POINTS_AT_IT:
        return str(subject)
    return ""


def _a_range_for_the_thing(text, understood=None):
    found = _THE_THING_JUDGED.search(str(text or "").strip().rstrip("?.!"))
    said = found.group(2).strip() if found else ""
    if said.lower() in _POINTS_AT_IT or not said:
        said = _the_thing_the_chat_is_on(understood)
    if not said:
        return None
    thing = " ".join((found.group(1) or "a ").split() + said.split()) if found else "a " + said
    for question in ("how much is %s" % thing, "how much does %s cost" % thing):
        entry = find({"clean": question, "words": question.split()})
        reply = getattr(entry, "reply", None)
        if callable(reply):
            try:
                reply = reply({}, {"clean": question, "words": question.split()})
            except Exception:
                continue
        if reply and _HOLDS_MONEY.search(str(reply)):
            return str(reply)
    return None


def find(understood, entries=None, reject=None, use_context=False):
    if _DREAM is not None and _DREAM.told_as_a_dream(
            understood.get("clean") or understood.get("text") or ""):
        return None
    if entries is None and _WHERE_I_PUT.search(
            " ".join(tokens(understood.get("clean") or understood.get("text") or ""))):
        return None
    if entries is None and _WHERE_TO_KEEP.search(
            " ".join(tokens(understood.get("clean") or understood.get("text") or ""))):
        kept = _the_best_entry(understood, _the_kept_rows(), reject, use_context)
        if kept is not None:
            return kept
    found = _the_best_entry(understood, entries, reject, use_context)
    if found is not None and _a_price_judged_is_not_answered_here(understood, found):
        return None
    if found is not None:
        return found
    for again in _what_is_wrong_with_them(understood):
        found = _the_best_entry(again, entries, reject, use_context)
        if found is not None:
            return found
    for again in _a_thing_that_has_not_gone(understood):
        found = _the_best_entry(again, entries, reject, use_context)
        if found is not None:
            return found
    for again in _without_the_place(understood):
        found = _the_best_entry(again, entries, reject, use_context)
        if found is not None:
            return found
    return None


_A_PLACE_ON_THEM = re.compile(
    r"(?:,?\s*(?:on|in|under|near|around|behind|above|below|beside|by|at|just (?:above|below|"
    r"under|behind|over|beside|next to))\s*(?:the\s+)?(?:my|his|her|their|our|your|its|this|"
    r"that)?\s*(?:left|right|inner|outer|lower|upper|front|back of the|top of the|side of the)?"
    r"\s*([a-z]+))\b", re.I)


def _without_the_place(understood):
    if not isinstance(understood, dict):
        return []
    clean = understood.get("clean") or understood.get("text") or ""
    said = _A_PLACE_ON_THEM.search(clean)
    if not said or said.group(1).lower() not in lexicon.BODY_PARTS:
        return []
    left = (clean[:said.start()] + clean[said.end():]).strip(" ,.;:!?")
    if len(left.split()) < 2:
        return []
    shaped = dict(understood)
    shaped["clean"] = left
    shaped["words"] = tokens(left)
    return [shaped]


_NOT_GONE = re.compile(
    r"\b(?:has|have|had|is|are|was|were|does|did)?\s*(?:not|n't|never)\s+"
    r"(?:gone|gone away|shifted|cleared|cleared up|eased|settled|improved|any better|got any better|"
    r"got better|better)\b|\bno better\b|\bwont\s+go\b|\bwon't\s+go\b|\bwould\s+not\s+go\b",
    re.I)

_SUBJECT_LEAD = re.compile(r"^(?:and|but|so|well|ok|okay|hi|hello|um|er)\b[,\s]*", re.I)
_POSSESSIVE = re.compile(r"^(?:the|my|his|her|their|our|your|a|an|this|that|these|those)\s+", re.I)


def _a_thing_that_has_not_gone(understood):
    if not isinstance(understood, dict):
        return []
    clean = understood.get("clean") or understood.get("text") or ""
    said = _NOT_GONE.search(clean)
    if not said:
        return []
    thing = _SUBJECT_LEAD.sub("", clean[:said.start()].strip(" ,.;:!?"))
    thing = _POSSESSIVE.sub("", thing).strip()
    if not thing or len(thing.split()) > 5:
        return []
    again = []
    for said_so in ("a %s that wont go away" % thing,
                    "how do i treat %s" % thing,
                    "%s still there" % thing):
        shaped = dict(understood)
        shaped["clean"] = said_so
        shaped["words"] = tokens(said_so)
        again.append(shaped)
    return again


def _what_is_wrong_with_them(understood):
    if not isinstance(understood, dict):
        return []
    cared = _past_the_carer(understood.get("clean") or understood.get("text") or "")
    if not cared:
        return []
    again = []
    for opener in ("how do i deal with ", "how do i treat "):
        said = opener + cared
        shaped = dict(understood)
        shaped["clean"] = said
        shaped["words"] = tokens(said)
        again.append(shaped)
    return again


_OF_THE_RULE_OUT = dict.fromkeys("""not a an the rather than instead of and but or please really
actually just so though although is are was were be been do does did""".split(), True)


def _without_the_ruled_out(understood):
    gone = [str(word).strip().lower() for word in understood.get("ruled_out") or []
            if str(word).strip()]
    if not gone:
        return understood
    clean = understood.get("clean") or ""
    words = understood.get("words")
    if not isinstance(words, list) or not words:
        words = tokens(clean)
    wanted = list(gone)
    left = []
    for word in words:
        key = word.lower() if isinstance(word, str) else ""
        if key and key in wanted:
            wanted.remove(key)
            continue
        left.append(word)
    if not [word for word in left if _OF_THE_RULE_OUT.get(str(word).lower()) is None]:
        return understood
    read = dict(understood)
    read["words"] = left
    read["clean"] = " ".join(word for word in left if isinstance(word, str))
    return read


_THE_DEGREE_WORDS = frozenset("degree degrees".split())
_THE_HEAT_OF_THE_DAY = frozenset("""
    hot cold warm cool heat heating temperature weather forecast oven fan oven thermometer summer
    winter sunny degrees
""".split())


def _the_degrees_are_a_temperature(understood):
    numbers = understood.get("numbers")
    if not isinstance(numbers, list) or not numbers:
        return False
    said = []
    for number in numbers:
        if isinstance(number, dict):
            said.extend(str(number.get("text") or "").lower().split())
    words = understood.get("norm")
    if isinstance(words, list):
        said.extend(str(word).lower() for word in words)
    for word in said:
        if "degree" in word:
            return True
        if any(sign in word for sign in ("\u00b0c", "\u00b0f", "\u00ba", "\u00b0", "\u00b0c")):
            return True
    return False


def _answers_a_qualification(item):
    key = _key_words(item)
    if not key & _THE_DEGREE_WORDS:
        return False
    return not bool(key & (_THE_HEAT_OF_THE_DAY - _THE_DEGREE_WORDS))


_THE_WH_WORDS = frozenset("what whats why how when where which who whose whom".split())

_ASK_FRAME = frozenset("""
    what whats why how when where which who whose whom do does did should shall can could will
    would may might must i me my we our us you your the a an is are was were be been being to
    for of in on at it that this these those there here and or but if so then also just
""".split())


_PLACES_PEOPLE_LIVE_IN = frozenset("""
    flat house home room rooms kitchen bedroom bathroom lounge hall hallway office classroom
    conservatory garage shed caravan cabin attic loft basement studio cottage
""".split())
_COLD_WORDS = frozenset("cold freezing frozen chilly baltic perishing".split())
_BETWEEN_A_PLACE_AND_ITS_COLD = frozenset("""
    is was are were get gets got been be feels feel really very so too absolutely
    bit little always still
""".split())


_HOW_A_PERSON_IS_COLD = frozenset("""
    shiver shivers shivering shivery chilled freezing numb goosebumps
""".split())
_SAYS_OF_THEMSELVES = frozenset("i im ive id iam me myself".split())


def _the_person_says_they_are_cold(typed):
    for at, word in enumerate(typed):
        if word not in _HOW_A_PERSON_IS_COLD and word not in _COLD_WORDS:
            continue
        for before in typed[max(0, at - 4):at]:
            if before in _SAYS_OF_THEMSELVES or before in ("feel", "feeling", "feels", "keep",
                                                          "keeps", "kept", "being", "got", "get"):
                return True
    return False


def _the_place_the_line_says_is_cold(typed):
    for at, word in enumerate(typed):
        if word not in _PLACES_PEOPLE_LIVE_IN:
            continue
        for next_word in typed[at + 1:at + 4]:
            if next_word in _COLD_WORDS:
                return word
            if next_word not in _BETWEEN_A_PLACE_AND_ITS_COLD:
                break
    return None


def _answers_the_cold_of_a_person(item, place=None):
    if item.domain not in FEELING_DOMAINS:
        return False
    key = _key_words(item)
    if not key & _COLD_WORDS:
        return False
    return place is None or place not in key


def _answers_the_cold_of_a_place(item, place):
    if _answers_the_cold_of_a_person(item, place):
        return False
    key = _key_words(item)
    return place in key and bool(key & _COLD_WORDS)


def _the_card_for_the_place_first(place, reached):
    if not reached:
        return reached
    for at, row in enumerate(reached):
        if at and _answers_the_cold_of_a_place(row[5], place):
            return [row] + reached[:at] + reached[at + 1:]
    return reached


def _the_ask_reading(understood, ask):
    asked = dict(understood)
    said = set(str(word).lower() for word in ask)
    asked["clean"] = " ".join(ask)
    asked["words"] = list(ask)
    asked["norm"] = list(ask)
    numbers = []
    for number in understood.get("numbers") or ():
        if not isinstance(number, dict):
            continue
        written = str(number.get("text") or "").lower().split()
        if set(written) & said or str(number.get("value")) in said:
            numbers.append(number)
    asked["numbers"] = numbers
    for key in ("entities", "things"):
        kept = []
        for thing in understood.get(key) or ():
            text = thing.get("text") if isinstance(thing, dict) else thing
            if isinstance(text, str) and set(text.lower().split()) & said:
                kept.append(thing)
        if key in understood:
            asked[key] = kept
    subject = understood.get("subject")
    asked["subject"] = subject if isinstance(subject, str) and subject.lower() in said else None
    return asked


def _the_ask_on_its_own(understood):
    focus = understood.get("focus")
    clauses = understood.get("clauses")
    if not isinstance(focus, list) or not isinstance(clauses, list) or len(clauses) < 2:
        return None
    ask = [str(word) for word in focus if isinstance(word, str) and word.strip()]
    if len(ask) < 2:
        return None
    whole = understood.get("norm") or understood.get("words")
    if not isinstance(whole, list):
        return None
    line = [str(word).lower() for word in whole if isinstance(word, str)]
    tail = [word.lower() for word in ask]
    if len(tail) >= len(line) or line[-len(tail):] != tail:
        return None
    if tail[0] not in _THE_WH_WORDS:
        return None
    return ask


def _the_best_entry(understood, entries=None, reject=None, use_context=False):
    if not isinstance(understood, dict):
        return None
    understood = _without_the_ruled_out(understood)
    clean = understood.get("clean") or ""
    words = understood.get("words")
    if not isinstance(words, list) or any(ch in clean for ch in _CURLY_ANY):
        words = tokens(clean)
    past = _past_a_handoff(clean)
    if past:
        words = tokens(past)
    left = understood.get("intensifier_left")
    intensifier = understood.get("intensifier") if left is None else left
    if isinstance(intensifier, list) and intensifier:
        going = {}
        for word in intensifier:
            if isinstance(word, str):
                going[word.lower()] = going.get(word.lower(), 0) + 1
        kept = []
        for word in reversed(words):
            key = word.lower() if isinstance(word, str) else ""
            stem = _without_possessive(key)
            hit = key if going.get(key) else (stem if going.get(stem) else "")
            if hit:
                going[hit] -= 1
                continue
            kept.append(word)
        words = kept[::-1]
    background = understood.get("background")
    if isinstance(background, list) and background and not understood.get("topic_own"):
        drop = {}
        for word in background:
            if isinstance(word, str):
                drop[word.lower()] = drop.get(word.lower(), 0) + 1
        kept = []
        for word in reversed(words):
            key = word.lower() if isinstance(word, str) else ""
            if drop.get(key):
                drop[key] -= 1
                continue
            kept.append(word)
        words = kept[::-1]
    if understood.get("kind") == "empty":
        return None
    occasion = _feeling_occasion(words)
    if occasion and not understood.get("asks") and understood.get("topic") != "pets" \
            and not _names_a_fault(occasion) and not _speaker_is_feeling(words) \
            and not _names_a_feared_thing(occasion):
        if entries is None:
            from . import entries as all_entries
            entries = all_entries()
        seen_in, known_words, _ = _vocabulary(entries)
        here = _best(understood, words, clean, [_forms(word) for word in words],
                     [word.lower() for word in words if isinstance(word, str)],
                     entries, seen_in, known_words, reject)
        if here is None or here.domain not in FEELING_DOMAINS:
            gone = {}
            for word in occasion:
                gone[word] = gone.get(word, 0) + 1
            kept_words = []
            for word in reversed(words):
                key = word.lower() if isinstance(word, str) else ""
                if gone.get(key):
                    gone[key] -= 1
                    continue
                kept_words.append(word)
            words = kept_words[::-1]
    original = words
    stripped = False
    if "dead" in [str(word).lower() for word in words]:
        words = _without_a_dead_that_only_means_very(words)
        stripped = len(words) != len(original)
    if "cooking" in [str(word).lower() for word in words]:
        words = _without_a_cooking_that_is_a_name(words)
        stripped = stripped or len(words) != len(original)
    words = _with_the_child_by_place(words, clean)
    if a_colour_is_worn(understood):
        words = [word for index, word in enumerate(words)
                 if not (isinstance(word, str) and word.lower() in COLOUR_ASKED_WORDS
                         and not _a_dress_code(words, index))] + ["wear"]
    forms = [_forms(w) for w in words]
    if entries is None:
        from . import entries as all_entries
        entries = all_entries()
    by_domain, every, known = _vocabulary(entries)
    typed = [word.lower() for word in words if isinstance(word, str)]
    if about_the_chat(understood.get("text") or clean):
        return None
    _read_typos(typed, forms, every, known)
    _read_a_thing_had([str(word).lower() for word in words], forms)
    wrapped = _wrapped_subject(clean, understood.get("norm_text"))
    whole = _best(understood, words, clean, forms, typed, entries, by_domain, every, reject)
    whole = _the_answer_the_colour_dragged_in(
        whole, understood, words, clean, entries, by_domain, every, reject)
    if a_colour_is_worn(understood):
        whole = _the_card_for_the_occasion_asked(
            whole, understood, words, clean, forms, typed, entries, by_domain, every, reject)
    item = None
    if wrapped:
        item = _the_ask_it_wraps(understood, wrapped, whole, entries, by_domain, every, reject)
    if item is None:
        item = whole
    filler = _FILLER.intersection(typed)
    kept = [word for word in words if str(word).lower() not in _FILLER] if filler else []
    bare = None
    if filler:
        bare = dict(understood)
        bare["clean"] = " ".join(str(word) for word in kept)
    if item is None and bare is not None:
        item = _best(bare, kept, bare["clean"], [_forms(word) for word in kept],
                     [word.lower() for word in kept if isinstance(word, str)],
                     entries, by_domain, every, reject)
    ask = _the_ask_on_its_own(understood)
    if ask:
        asked_for = set(word.lower() for word in ask) - _ASK_FRAME
        if item is None or not (asked_for & _key_words(item)):
            asked = _the_ask_reading(understood, ask)
            found = _best(asked, ask, asked["clean"], [_forms(word) for word in ask],
                          [word.lower() for word in ask], entries, by_domain, every, reject)
            if found is not None:
                item = found
    if item is None and stripped:
        item = _best(understood, original, clean, [_forms(word) for word in original],
                     [word.lower() for word in original if isinstance(word, str)],
                     entries, by_domain, every, reject)
    if item is None:
        described = list(forms)
        if _read_the_adjective(typed, described, every):
            item = _best(understood, words, clean, described, typed, entries, by_domain, every,
                         reject)
    if item is None and use_context and understood.get("leans_on") \
            and leans_on_a_subject(understood):
        item = _following_on(understood, entries, forms, typed, by_domain, every, known, reject)
        if item is None and bare is not None:
            item = _following_on(
                understood, entries, [_forms(word) for word in kept],
                [word.lower() for word in kept if isinstance(word, str)],
                by_domain, every, known, reject)
        if item is not None and wrapped and not about(item, wrapped):
            item = None
    if item is not None and _the_animal_rules_out_that_card(item, understood):
        pointed = _with_the_animal_in_hand(words, understood)
        if pointed is not words:
            better = _best(understood, pointed, clean, [_forms(word) for word in pointed],
                           [word.lower() for word in pointed if isinstance(word, str)],
                           entries, by_domain, every, reject)
            if better is not None:
                item = better
    if item is None:
        item = _defines(understood, forms, typed, entries, reject)
    if item is None:
        item = _the_name_alone(_the_name_card([str(word).lower() for word in words],
                                             entries, reject,
                                             _topic_domains(understood, entries)),
                               entries, reject, _topic_domains(understood, entries),
                               understood, words, use_context)
    return item


_DEFINITION_ASK = re.compile(
    r"^\s*(?:so\s+|ok\s+|okay\s+|and\s+|but\s+)?"
    r"(?:"
    r"what\s*(?:'s|\u2019s|s)?\s+(?:is|are|was|were)\s+(?P<thing>[^?.!,;:]{1,60}?)"
    r"|what\s*(?:'s|\u2019s|s)\s+(?P<thing2>[^?.!,;:]{1,60}?)"
    r"|what\s+(?:does|do)\s+(?P<thing3>[^?.!,;:]{1,60}?)\s+mean"
    r"|define\s+(?P<thing4>[^?.!,;:]{1,60}?)"
    r")\s*(?:\?)?\s*$", re.I)
_DEFINITION_TAIL = frozenset("""
    for mean means meant exactly then again please called thats it its in simple terms
    supposed to do stand stands actually really even anyway though
""".split())
_DEFINITION_POINTERS = frozenset("""
    there it that this these those he she they we you i someone anyone somebody nobody
""".split())
_DEFINITION_TROUBLE = frozenset("""
    wrong matter happening pain painful hurts hurt hurting ache aches aching smell smells smelling
    leak leaks leaking noisy noise broken stuck faulty fix
""".split()) | {"going on", "up with", "up to"}

_DEFINITION_EMPTY = frozenset("""
    a an the my your our their his her its some any this that these those of in on at to and or
    for with from about it that this there here one ones thing things stuff kind sort type
    what which who whom whose how why when where right best good
    going happening wrong up on around next
""".split())


def _the_thing_asked_about(clean):
    if not isinstance(clean, str) or not clean.strip():
        return ()
    found = _DEFINITION_ASK.match(clean.strip().lower())
    if not found:
        return ()
    thing = next((part for part in found.groups() if part), "")
    opening = (thing.split() or [""])[0].strip("'\"-")
    if opening in _DEFINITION_POINTERS:
        return ()
    raw = thing.lower().replace("\u2019", "'")
    if any(word in _DEFINITION_TROUBLE for word in _words_of(raw)) \
            or any(phrase in " %s " % raw for phrase in ("going on", "up with", "up to")):
        return ()
    words = []
    for word in thing.replace("\u2019", "'").split():
        word = word.strip("'\"-")
        if not word or word in _DEFINITION_EMPTY or word in _DEFINITION_TAIL:
            continue
        if len(word) < 2 and not word.isalpha():
            continue
        words.append(word)
    while words and words[-1] in _DEFINITION_TAIL:
        words.pop()
    return tuple(words[:3])


def _words_of(text):
    return [word.strip("'\"-?!.,;:") for word in text.split() if word.strip("'\"-?!.,;:")]


def _asks_what_it_is_for(clean):
    if not isinstance(clean, str):
        return False
    return bool(re.search(r"\bfor\b\s*\??\s*$|\bused for\b|\bdo(?:es)? (?:it|that|this) do\b",
                          clean.strip().lower()))


_DEFINING_VERBS = frozenset("""
    is are was were means mean refers gives give costs cost covers cover keeps keep works work
    helps help makes make takes take needs need holds hold comes come runs run lets let stops stop
    protects protect lets replaces replace counts count serves serve
""".split())


_BE_VERBS = frozenset("is are was were".split())
_SUBJECT_AT_MOST = 6
_DEFINITION_ARTICLES = frozenset("a an the".split())
_BEFORE_THE_THING = frozenset("""
    of in on with at from your my our their its his her
    cup mug glass slice piece bit bowl plate packet tin can bottle spoon teaspoon tablespoon
    handful pinch taste sip bite
""".split())


def _a_number(word):
    return any(char.isdigit() for char in word)


def _the_thing_in(sentence, thing):
    words = [word.lower() for word in tokens(sentence) if isinstance(word, str)]
    wanted = [_forms(word) for word in thing]
    for start in range(len(words) - len(wanted) + 1):
        run = words[start:start + len(wanted)]
        if all(_forms(word) & want for word, want in zip(run, wanted)):
            return start, words
    return None


def _the_reply_defines(reply, thing, purpose=False):
    if not isinstance(reply, str) or not reply.strip():
        return False
    opening = re.split(r"(?<=[.!?])\s", reply.strip(), maxsplit=1)[0]
    found = _the_thing_in(opening, thing)
    if found is None:
        return False
    if found[0] > _SUBJECT_AT_MOST:
        return False
    if purpose:
        return True
    start, words = found
    if start and words[0] not in _DEFINITION_ARTICLES:
        return False
    before = words[:start]
    if any(word in _BE_VERBS for word in before):
        return False
    if before and (before[-1] in _BEFORE_THE_THING or _a_number(before[-1])):
        return False
    after = words[start + len(thing):start + len(thing) + 1]
    return bool(after) and after[0] in _DEFINING_VERBS


def _the_key_names_the_thing(item, thing):
    wanted = [_forms(word) for word in thing]
    for part in item.key:
        for alternative in (part if isinstance(part, tuple) else (part,)):
            if not isinstance(alternative, str):
                continue
            words = alternative.lower().split()
            if len(words) != len(wanted):
                continue
            if all(_forms(word) & want for word, want in zip(words, wanted)):
                return True
    return False


NAME_ALONE_DOMAINS = frozenset('''family health body babyfood pregnancy'''.split())
NOT_A_NAME_ALONE = frozenset('''what why how when where which who whom whose is are was were
    am do does did can could should would will shall may might i im ive id you your u my mine
    me we our us it its that this these those there they them he she him her his hers the a an
    and or but if so then than about for with on in at to of from not no yes ok okay thanks
    please help huh'''.split())
A_STATE_AS_A_NAME_END = frozenset('''closed shut blocked swollen broken numb off blocked'''.split())
A_STATE_IN_THE_PHRASE = frozenset('''feel feels feeling felt gone went go goes going get gets
    getting got gotten been being be keep keeps keeping kept start starts started starting
    burn burns burning'''.split())


def _said_as_a_report(understood, words, entries, reject=None):
    if not isinstance(understood, dict):
        return None
    said = "i have a " + " ".join(str(word) for word in words)
    second = dict(understood)
    second["clean"] = said
    second["words"] = ["i", "have", "a"] + [str(word) for word in words]
    for key in ("background", "intensifier", "intensifier_left", "leans_on", "topic_own",
                "past", "handoff"):
        second.pop(key, None)
    return _the_best_entry(second, entries, reject, False)


def _the_name_card(typed, entries, reject=None, allowed=None):
    said = set(typed)
    found = []
    for item in entries:
        if getattr(item, "domain", None) not in NAME_ALONE_DOMAINS:
            continue
        if reject is not None and reject(item):
            continue
        if allowed is not None and getattr(item, "domain", None) not in allowed:
            continue
        key = getattr(item, "key", ()) or ()
        if not key:
            continue
        part = key[0]
        alternatives = part if isinstance(part, tuple) else (part,)
        if not alternatives or not isinstance(alternatives[0], str):
            continue
        phrase = set(alternatives[0].lower().split())
        if len(phrase) >= 2 and phrase == said:
            found.append(item)
    if not found:
        return None
    if len(found) == 1:
        return found[0]
    def _names_itself(item):
        name = (item.key[0][0] if item.key else "")
        reply = (getattr(item, "reply", "") or "").lower()[:140]
        return 0 if isinstance(name, str) and name.lower() in reply else 1
    return min(found, key=_names_itself)


def _the_name_alone(named, entries, reject, allowed=None, understood=None, words=None,
                    use_context=False):
    typed = [str(word).lower() for word in (words or ())]
    if not 2 <= len(typed) <= 4:
        return None
    if any(word in NOT_A_NAME_ALONE for word in typed):
        return None
    if any(word in A_STATE_IN_THE_PHRASE for word in typed):
        return None
    if typed[-1] in A_STATE_AS_A_NAME_END:
        return None
    if named is None:
        return None
    if not allowed:
        return None
    if understood is not None:
        allowed = _declared_for(allowed, understood)
    if getattr(named, "domain", None) not in allowed:
        return None
    said = set(typed)
    if len(said) != len(typed):
        return None
    return named


def _declared_for(allowed, understood):
    from . import by_topic
    judged = by_topic()
    topics = []
    if isinstance(understood, dict):
        found = understood.get("topics")
        topics = list(found) if isinstance(found, (list, tuple)) else []
        topics.append(understood.get("topic"))
    topics = [topic for topic in topics if isinstance(topic, str) and topic]
    if not topics:
        return set()
    return {name for name in allowed
            if any(topic in (judged.get(name) or ()) for topic in topics)}


def _defines(understood, forms, typed, entries, reject=None):
    clean = understood.get("clean") if isinstance(understood, dict) else ""
    said = clean or (understood.get("text") if isinstance(understood, dict) else "") or ""
    thing = _the_thing_asked_about(said)
    if not thing:
        return None
    purpose = _asks_what_it_is_for(said)
    best = None
    best_rank = None
    for item in entries:
        if reject is not None and reject(item):
            continue
        if not guard_passes(item, understood):
            continue
        if not _the_key_names_the_thing(item, thing):
            continue
        if not _the_reply_defines(getattr(item, "reply", ""), thing, purpose):
            continue
        if any(_part_score(word, forms) for word in item.avoid):
            continue
        rank = -len(_key_forms(item))
        if best_rank is None or rank > best_rank:
            best, best_rank = item, rank
    return best


def _named_things(understood):
    found = []
    entities = understood.get("entities") if isinstance(understood, dict) else None
    for entity in entities if isinstance(entities, list) else ():
        if not isinstance(entity, dict) or entity.get("type") not in ("place", "name", "title"):
            continue
        name = " ".join(str(entity.get("text") or "").lower().split())
        if len(name) > 2:
            found.append(name)
    return found


PLAN_WORDS = ("plan", "plans", "planning", "organise", "organize", "prepare", "preparing")


def _plans_it(item, forms):
    if not any(_part_score(word, forms) for word in PLAN_WORDS):
        return False
    return any(word in _key_words(item) for word in PLAN_WORDS)


def _names_one(item, named):
    for part in getattr(item, "key", ()) or ():
        for alternative in (part if isinstance(part, tuple) else (part,)):
            text = " ".join(str(alternative).lower().split())
            for name in named:
                if _bounded(str(name)).search(text):
                    return True
    return False

POINTS_BACK = frozenset("""it its it's that this these those there them they he she him her""".split())


FOLLOW_ON_WORDS = frozenset("""
about actually alright anyway bad better change good happen happens idea instead mean means meant
now okay otherwise question really safe suppose then thing think true wait worse wrong
common dangerous fine fix fixed happening happened knackered normal repair repaired ruined ruin
salvage salvaged save saved serious survive survived survives worrying worried worth next
""".split())


def _only_asking_about_it(understood, leans):
    earlier = set(tokens(str((leans or {}).get("clean") or (leans or {}).get("text") or "")))
    earlier.update(str(word).lower() for word in ((leans or {}).get("words") or ())
                   if isinstance(word, str))
    now = tokens(str(understood.get("clean") or understood.get("text") or ""))
    if not now:
        return False
    for word in now:
        if word in earlier or word in GRAMMAR_ONLY or word in POINTS_BACK:
            continue
        if word in FOLLOW_ON_WORDS or word.isdigit():
            continue
        return False
    return True


def names_nothing_of_its_own(understood):
    leans = understood.get("leans_on")
    if not isinstance(leans, dict):
        return False
    return _only_asking_about_it(understood, leans)


def leans_on_a_subject(understood):
    if str(understood.get("kind") or "") == "question":
        return True
    if _says_how_the_speaker_handles_it(understood):
        return True
    line = tokens(str(understood.get("clean") or understood.get("text") or ""))
    return any(word in POINTS_BACK for word in line)


_ROWS_CACHE = {}
_ROWS_KEEP = 40


ASK_NAME_CAP = 40

ASK_PLAIN_CAP = 400


def _the_names_in_the_ask(understood, every):
    split = _two_clauses(understood)
    if not split:
        return ()
    focus = split
    names = []
    for word in focus:
        if not isinstance(word, str):
            continue
        low = word.lower()
        if len(low) < 3 or low in _NOT_A_SUBJECT or low in ASK_FRAME_WORDS:
            continue
        if every.get(low, 0) > ASK_NAME_CAP or low in names:
            continue
        names.append(low)
    plain = "yesno" not in (understood.get("asks") or ())
    if not names and plain:
        for word in focus:
            if not isinstance(word, str):
                continue
            low = word.lower()
            if len(low) < 3 or low in _NOT_A_SUBJECT or low in ASK_FRAME_WORDS:
                continue
            if every.get(low, 0) > ASK_PLAIN_CAP or low in names:
                continue
            names.append(low)
    return tuple(names)


def _the_ask_in_order(understood):
    said = _two_clauses(understood)
    if not said:
        return ()
    return tuple(word for word in said if isinstance(word, str))


ASK_FRAME_WORDS = frozenset("""
    what when where which who why how should could would can will shall may might must
    is are was were be been being am do does did done doing have has had having
    get gets got getting need needs want wants like likes make makes made take takes
    go goes going put give gives tell say says know think use uses try tries
    good best better bad worse right wrong sure possible worth
    """.split())


def _two_clauses(understood):
    if not isinstance(understood, dict) or not understood.get("asks"):
        return None
    focus = understood.get("focus")
    clauses = [clause for clause in (understood.get("clauses") or ())
               if isinstance(clause, (list, tuple)) and clause != ["text"]]
    if not isinstance(focus, (list, tuple)) or not focus or len(clauses) < 2:
        return None
    last = {_forms(str(word)) for word in (clauses[-1] or ()) if isinstance(word, str)}
    earlier = {_forms(str(word)) for clause in clauses[:-1] for word in (clause or ())
               if isinstance(word, str)}
    longest = max((len([word for word in (clause or ()) if isinstance(word, str)])
                   for clause in clauses[:-1]), default=0)
    if not last or not earlier or longest < 4:
        return None
    for word in focus:
        if not isinstance(word, str):
            continue
        form = _forms(word)
        if form in last or form not in earlier:
            continue
        return None
    return tuple(word for word in focus if isinstance(word, str))


def _rows_key(forms, typed, named, frame, framed=False, asked=(), ask_said=()):
    try:
        return (tuple(tuple(sorted(str(form) for form in group)) for group in forms),
                tuple(str(word) for word in typed or ()),
                tuple(str(one) for one in named or ()), bool(frame), bool(framed),
                tuple(str(word) for word in asked or ()),
                tuple(str(word) for word in ask_said or ()))
    except TypeError:
        return None


def _line_rows(forms, typed, entries, by_domain, every, named=(), frame=True,
               stands_down=None, framed=False, ask_names=(), ask_said=()):
    key = _rows_key(forms, typed, named, frame, framed, ask_names, ask_said)
    ranked_items = None
    if key is not None:
        got = _ROWS_CACHE.get((id(entries), key))
        if got is not None and got[0] is entries:
            ranked_items = got[1]
    if ranked_items is None:
        ranked_items = _scanned_rows(forms, typed, entries, by_domain, every, named, frame,
                                     framed, ask_names, ask_said)
        if key is not None:
            if len(_ROWS_CACHE) >= _ROWS_KEEP:
                _ROWS_CACHE.pop(next(iter(_ROWS_CACHE)))
            _ROWS_CACHE[(id(entries), key)] = (entries, ranked_items)
    if stands_down is None:
        return list(ranked_items)
    return [row for row in ranked_items if not stands_down(row[5])]


def _scanned_rows(forms, typed, entries, by_domain, every, named, frame, framed=False,
                  ask_names=(), ask_said=()):
    ranked_items = []
    ask_forms = [_forms(word) for word in ask_names]
    ask_line = [_forms(word) for word in ask_said]
    seen = {}
    asked_seen = {}
    for item in _reaching(entries, forms):
        value = score(item, forms, typed, seen, frame, framed)
        if not value:
            continue
        domain = getattr(item, "domain", "") or ""
        ranked = _rank(item, forms, by_domain.get(domain) or every, seen)
        asked = 0 if _only_the_want(item, forms, seen) else 1
        run = _the_longest_run(item, ask_line, ask_forms, asked_seen)
        ranked_items.append((asked, ranked, _plans_it(item, forms),
                             _names_one(item, named), len(item.key), item, run))
    longest = max((row[6] for row in ranked_items), default=0)
    if longest:
        ranked_items = [row[:6] + (1 if row[6] == longest else 0,) for row in ranked_items]
    return ranked_items


def _the_longest_run(item, ask_line, name_forms, asked_seen):
    wanted = set()
    for forms in name_forms:
        wanted |= forms
    best = 0
    for part in item.key or ():
        for weight, words, span in _part_matches(part, ask_line, asked_seen):
            if not weight or len(span) <= best:
                continue
            if not any(_forms(str(word)) & wanted for word in words):
                continue
            best = len(span)
    return best


def _row_order(row):
    return (row[0], row[6], row[1], row[2], row[3], row[4])


PLAIN_MARGIN = 3


def _plainer(plain, framed, margin=PLAIN_MARGIN):
    better = max(row[:2] for row in plain)
    other = max(row[:2] for row in framed)
    return better[0] > other[0] or better[1] >= other[1] + margin


SUBSTITUTE_WORDS = frozenset(("substitute", "substitutes", "substitution", "instead", "swap",
                              "alternative", "alternatives", "replace", "replacement"))


def _the_subjects_own_row(forms, item, rows):
    domain = getattr(item, "domain", None)
    if not domain or not _a_clause_about_the_thing(forms):
        return False
    if not any(getattr(row[5], "domain", None) == domain for row in rows):
        return False
    return _offers_a_substitute(max(rows, key=_row_order)[5])


def _offers_a_substitute(item):
    for part in item.key:
        for alternative in (part if isinstance(part, tuple) else (part,)):
            if isinstance(alternative, str) and set(alternative.lower().split()) & SUBSTITUTE_WORDS:
                return True
    return False


RETURNED_AFTER = frozenset("""
    is are was were be been am
    im i'm youre you're hes he's shes she's theyre they're were we're
    come comes came coming
    go goes going went gone
    get gets getting got gotten
    walk walks walking walked
    drive drives driving drove driven
    fly flies flying flew flown
    run runs running ran
    head heads heading headed
    move moves moving moved
    travel travels travelling traveled
    carry carries carrying carried
    bring brings bringing brought
    take takes taking took taken
    send sends sending sent
    call calls calling called
    write writes writing wrote written
    put puts putting
    hand hands handing handed
    pay pays paying paid
    give gives giving gave given
    kick kicks kicking kicked
    sit sits sitting sat
    lie lies lying lay lain
    step steps stepping stepped
    look looks looking looked
    turn turns turning turned
    think thinks thinking thought
    bounce bounces bouncing bounced
""".split())
BODY_WORDS = lexicon.BODY_PARTS
GENERAL_BODY = frozenset(("skin", "muscle", "muscles"))
SPECIFIC_PARTS = 2
PART_INSIDE = {
    "heel": "foot", "ankle": "leg", "knee": "leg", "hip": "leg",
    "thumb": "hand", "finger": "hand", "knuckle": "hand",
    "wrist": "hand", "elbow": "arm", "shoulder": "arm",
    "jaw": "head", "tooth": "head", "ear": "head", "eye": "head",
    "rib": "chest", "belly": "stomach",
}


def _inside(part, other):
    seen = 0
    while part and seen < 4:
        if _forms(part) & _forms(other):
            return True
        part = PART_INSIDE.get(part, "")
        seen += 1
    return False


_CUT_BESIDE = frozenset((
    "lamb", "beef", "pork", "chicken", "turkey", "duck", "goose", "gammon", "veal", "venison",
    "meat", "steak", "joint", "roast", "roasting", "brisket", "mince", "sausage", "sausages",
    "ham", "bacon", "chops", "chop", "fillet", "breast", "thigh", "drumstick", "wing"))


def _a_cut_of_meat(words, index):
    near = [str(words[at]).lower() for at in (index - 2, index - 1, index + 1, index + 2)
            if 0 <= at < len(words)]
    return any(word in _CUT_BESIDE for word in near)


def _body_parts(words):
    parts = set()
    for index, word in enumerate(words or ()):
        word = str(word).lower()
        if word not in BODY_WORDS:
            continue
        if word == "back" and index and str(words[index - 1]).lower() in RETURNED_AFTER:
            continue
        if word in GENERAL_BODY:
            continue
        if _a_cut_of_meat(words, index):
            continue
        parts.add(word)
    return parts


def _key_body_parts(item):
    parts = set()
    for part in getattr(item, "key", ()) or ():
        for alternative in (part if isinstance(part, tuple) else (part,)):
            if isinstance(alternative, str):
                parts |= _body_parts(alternative.lower().split())
    return parts


def _a_part_the_line_does_not_have(word, parts_said):
    key = str(word).strip().lower() if isinstance(word, str) else ""
    if not key or " " in key or key not in BODY_WORDS:
        return False
    return key not in (parts_said or ())


def _another_part(item, line_parts):
    if not line_parts:
        return False
    parts = _key_body_parts(item)
    if not parts or len(parts) > SPECIFIC_PARTS:
        return False
    said = list(line_parts)
    return not any(_inside(other, part) for part in parts for other in said)


_STILL_GOOD_ASHERS = frozenset((
    "ok", "okay", "safe", "eat", "eats", "eating", "drink", "use", "still", "good", "gone",
    "off", "bin", "throw", "edible", "risky"))
_KEEPING_WORDS = frozenset((
    "keep", "keeps", "kept", "keeping", "last", "lasts", "store", "stored", "storage", "freeze",
    "frozen", "reheat", "reheated", "mouldy", "sour", "slimy", "stale", "gone", "date", "bin",
    "throw", "overnight", "left"))

_KEEPING_ANSWER = (
    " keeps ", " keep it ", " keep them ", " keeping it ", " in the fridge", " in the freezer",
    " in a sealed", " in an airtight", "bin it", "bin them", "throw it", "throw them",
    "no more than", "shelf life", "hours", "days in the", "a day in the", "day in the fridge",
    "within a day", "within the hour", "goes off", "gone off", "until the date", "use-by",
    "use by", "best before", "cold box", "cool it", "cool it fast")


def _asks_if_it_is_still_good(typed):
    if not typed:
        return False
    return bool(_STILL_GOOD_ASHERS.intersection(str(word).lower() for word in typed))


_A_KEEP_AND_A_LENGTH = re.compile(
    r"\bkeep(?:s)?\s+(?:about|for|up to|until|till|roughly|around|no more than|"
    r"a day|a week|a fortnight|a month|a year|"
    r"two|three|four|five|six|seven|eight|ten|twelve|\d)")


def _a_keeping_row(item):
    reply = getattr(item, "reply", "") or ""
    if not isinstance(reply, str):
        return _a_keeping_key(item)
    if not reply:
        return False
    reply = " " + " ".join(reply.lower().split()) + " "
    return any(phrase in reply for phrase in _KEEPING_ANSWER) or bool(
        _A_KEEP_AND_A_LENGTH.search(reply))


def _a_keeping_key(item):
    words = set()

    def collect(part):
        if isinstance(part, str):
            words.update(part.lower().split())
        elif isinstance(part, (tuple, list, frozenset, set)):
            for inner in part:
                collect(inner)

    collect(getattr(item, "key", ()) or ())
    return bool(_KEEPING_WORDS.intersection(words))


COLOUR_WORDS = frozenset("""red orange yellow green blue indigo violet purple pink brown black white
    grey gray beige cream tan navy gold golden silver amber turquoise lilac mauve crimson scarlet
    burgundy maroon olive khaki teal cyan magenta peach coral rust blonde fair plum cherry lemon
    lime salmon rose chestnut copper ochre ebony ivory pearl""".split())
A_COLOUR_USED = re.compile(
    r"\b(?:is|are|was|were|am|be|been|being|looks?|looked|seems?|seemed|got|gets|getting|goes|"
    r"going|went|gone|turn(?:s|ed|ing)?|becom(?:e|es|ing)|became|keep|keeps|kept|painted|paint|"
    r"dyed|dye|stained?)\s+(?:very\s+|really\s+|so\s+|too\s+|quite\s+|a bit\s+|a little\s+|"
    r"all\s+|still\s+|now\s+)?(?P<colour>[a-z]+)\b", re.IGNORECASE)


ASKING_FIRST = frozenset("""is are am was can could should would will shall may might do does did
    what which any anything how""".split())
A_COLOUR_ASKED = re.compile(
    r"\b(?:is|are|am|was|can|could|should|would|will|shall|may|might|do|does|did)\b[^.?!]{0,30}?"
    r"\b(?:ok|okay|alright|all right|fine|suitable|appropriate|respectful|acceptable|allowed|"
    r"rude|too much|not done|or|colour|color)\b"
    r"|\b(?:what|which|any|anything|something)\b[^.?!]{0,30}?"
    r"\b(?:wear|wearing|put on|outfit|clothes|colour|color|dress)\b"
    r"|\b(?:%s)\b[^.?!]{0,12}?\b(?:or|vs|versus)\b[^.?!]{0,12}?\b(?:%s)\b"
    % ("|".join(sorted(COLOUR_WORDS)), "|".join(sorted(COLOUR_WORDS))), re.IGNORECASE)
COLOUR_ASKED_WORDS = COLOUR_WORDS | frozenset(("colour", "color", "colours", "colors"))
WEARING = frozenset("""wear wearing wore worn outfit outfits clothes clothing dressed dress dresses
    suit suits tie frock gown hat hats shirt blouse trousers shoes heels""".split())
OCCASION = re.compile(
    r"\b(?:weddings?|funerals?|wakes?|memorial service|christenings?|baptisms?|naming ceremony|"
    r"proms?|graduations?|black tie|cocktail|interviews?)\b", re.IGNORECASE)


A_DRESS_CODE_AFTER = ("tie",)


def _a_dress_code(words, index):
    return (index + 1 < len(words) and words[index] in ("black", "white")
            and str(words[index + 1]).lower() in A_DRESS_CODE_AFTER)


AFTER_A_COLOUR_STANDS = frozenset("""
    ok okay alright fine acceptable allowed appropriate suitable good bad wrong safe rude risky
    smart casual formal warm cool nice better best right darker lighter brighter
    to for at in on with and or too not is was are were should would could can will shall must
    the a an this that there it i we they he she my our their his her
    be been being have has had do does did
    """.split())
WORN_AFTER_A_COLOUR = frozenset("""
    wear outfit dress dresses frock gown suit suits tie ties shirt shirts blouse top tops trousers
    pants skirt skirts jeans shorts leggings socks tights boots shoes trainers sneakers sandals
    heels flats hat hats cap jumper jumpers cardigan hoodie coat coats jacket blazer scarf gloves
    cotton linen silk wool satin lace leather denim velvet chiffon knit cashmere
    ring rings necklace bracelets earrings jewellery jewelry band watch
    """.split())


def _the_colour_is_the_whole_ask(words, index):
    if index + 1 >= len(words):
        return True
    after = index + 1
    if len(str(words[after])) == 1 and after + 1 < len(words):
        after += 1
    word = str(words[after]).lower().strip(string.punctuation)
    if not word:
        return True
    return (word in AFTER_A_COLOUR_STANDS or word in WORN_AFTER_A_COLOUR
            or word in COLOUR_WORDS)


def a_colour_is_worn(understood):
    if isinstance(understood, str):
        understood = {"text": understood}
    if not isinstance(understood, dict):
        return False
    said = str(understood.get("text") or understood.get("clean") or "")
    if not said:
        words = understood.get("words")
        said = " ".join(str(word) for word in words) if isinstance(words, (list, tuple)) else ""
    typing = tokens(said)
    typed = set(typing)
    if not typed & COLOUR_ASKED_WORDS:
        return False
    if not any(word in COLOUR_ASKED_WORDS and not _a_dress_code(typing, index)
               and _the_colour_is_the_whole_ask(typing, index)
               for index, word in enumerate(typing)):
        return False
    if not (WEARING & typed or OCCASION.search(" ".join(typing))):
        return False
    if understood.get("kind") == "question" or "?" in said:
        return True
    first = next((word for word in tokens(said) if word != "so"), "")
    return bool(first in ASKING_FIRST) or bool(A_COLOUR_ASKED.search(said))


def _the_words_without_a_colour(clean, words):
    said = {match.group("colour").lower() for match in A_COLOUR_USED.finditer(str(clean or ""))}
    said &= COLOUR_WORDS
    if not said:
        return None
    kept = [word for word in words if str(word).lower() not in said]
    if not kept or len(kept) == len(words):
        return None
    return kept


_BARE_IN_A_KEY = frozenset("""a an the and or but if then than that this these those there here i
    me my mine we us our you your yours he him his she her hers it its they them their is are was
    were am be been being do does did done have has had got get gets getting go goes went gone
    going make makes made just so not no yes very really quite too much many more most some any
    all one two three last next night morning today tonight tomorrow now still also about of to in
    on at for with from by as up down out off over again ever never always thing things bit lot
    kind sort what when where which who how why""".split())


def _the_key_words(entry):
    said = set()
    for part in (getattr(entry, "key", ()) or ()):
        if isinstance(part, str):
            said.update(part.lower().split())
        else:
            for one in part:
                said.update(str(one).lower().split())
    return said


THE_SAME_OCCASION = {
    "funeral": frozenset("funeral funerals wake wakes memorial burial cremation".split()),
    "wedding": frozenset("wedding weddings married marriage".split()),
    "christening": frozenset("christening christenings baptism baptisms naming".split()),
    "prom": frozenset(("prom", "proms")),
    "graduation": frozenset(("graduation", "graduations")),
    "interview": frozenset(("interview", "interviews")),
}


def _the_occasion_family(phrase):
    word = str(phrase or "").lower().strip()
    for family, members in THE_SAME_OCCASION.items():
        if word in members or word.startswith(family):
            return family
    return ""


def _the_occasion_words(typed):
    said = " ".join(str(word) for word in typed if isinstance(word, str))
    found = set()
    for match in OCCASION.finditer(said):
        family = _the_occasion_family(match.group(0))
        if family:
            found |= THE_SAME_OCCASION[family]
    return found


def _the_card_for_the_occasion_asked(found, understood, words, clean, forms, typed, entries,
                                     by_domain, every, reject):
    asked = _the_occasion_words(typed)
    if not asked:
        return found
    if found is not None and (_the_key_words(found) & asked):
        return found
    for_this = [entry for entry in entries
                if str(getattr(entry, "domain", "")) == "clothing"
                and (_the_key_words(entry) & asked)]
    if not for_this:
        return found
    again = _best(understood, words, clean, forms, typed, for_this, by_domain, every, reject)
    return again if again is not None else found


def _the_answer_the_colour_dragged_in(found, understood, words, clean, entries, by_domain, every,
                                      reject):
    kept = _the_words_without_a_colour(clean, words)
    if kept is None or found is None:
        return found
    others = {str(word).lower() for word in kept} - _BARE_IN_A_KEY
    if others & _the_key_words(found):
        return found
    again = _best(understood, kept, " ".join(str(word) for word in kept),
                  [_forms(word) for word in kept],
                  [word.lower() for word in kept if isinstance(word, str)],
                  entries, by_domain, every, reject)
    return again if again is not None else found


def _best(understood, words, clean, forms, typed, entries, by_domain, every, reject=None,
          framed=False):
    line_parts = _body_parts(words)

    kept = understood.get("kept")
    keeping_question = bool(kept) and _asks_if_it_is_still_good(typed)

    ask_names = _the_names_in_the_ask(understood, every)
    ask_said = _the_ask_in_order(understood)

    degrees_are_heat = _the_degrees_are_a_temperature(understood)
    aged_a_thing = the_years_are_a_things(understood)
    cold_place = None
    if not _speaker_is_feeling(typed) and not _the_person_says_they_are_cold(typed):
        cold_place = _the_place_the_line_says_is_cold(typed)

    def rank(reading, filter_keeping):

        def stands_down(item):
            if not guard_passes(item, reading):
                return True
            if degrees_are_heat and _answers_a_qualification(item):
                return True
            if aged_a_thing and _the_age_is_a_childs(item):
                return True
            if filter_keeping and not _a_keeping_row(item):
                return True
            return _another_part(item, line_parts)

        named = _named_things(reading)
        reached = _line_rows(forms, typed, entries, by_domain, every, named,
                             stands_down=stands_down, framed=framed, ask_names=ask_names,
                             ask_said=ask_said)
        plain_rows = None
        if _frame_masked(forms)[1]:
            plain_rows = _line_rows(forms, typed, entries, by_domain, every, named, frame=False,
                                    stands_down=stands_down, framed=framed, ask_names=ask_names,
                                    ask_said=ask_said)
            if plain_rows:
                plain_rows.sort(key=_row_order, reverse=True)
                if (not reached or _plainer(plain_rows, reached)
                        or _offers_a_substitute(plain_rows[0][5])
                        or _the_subjects_own_row(forms, plain_rows[0][5], reached)):
                    reached = plain_rows
        return reached, plain_rows

    ranked_items, plain = rank(understood, keeping_question)
    if not ranked_items and keeping_question:
        ranked_items, plain = rank({k: v for k, v in understood.items() if k != "kept"}, False)
    if not ranked_items:
        return _other_reading(understood, words, clean, entries, reject)
    ranked_items = [row for row in ranked_items if row[1] > 1]
    if not ranked_items:
        return _other_reading(understood, words, clean, entries, reject)
    ranked_items.sort(key=_row_order, reverse=True)
    if cold_place is not None:
        ranked_items = _the_card_for_the_place_first(cold_place, ranked_items)
    carried = _the_subject_the_line_leans_on(understood)
    ask_thing = understood.get("ask_subject")
    scene = understood.get("setting")
    scene_only = (isinstance(ask_thing, str) and isinstance(scene, str)
                  and ask_thing != scene and not _says_what_is_missing(understood)
                  and _is_a_person(understood, ask_thing) == _is_a_person(understood, scene))
    turned_down = set()
    for whole_line_first in (True, False):
        for _asked, _ranked, _plans, _named, _keys, item, _on_ask in ranked_items:
            if reject is not None and reject(item):
                turned_down.add(item.id)
                continue
            if _the_subject_it_avoids(item, forms, carried):
                continue
            if not scene_only:
                return item
            says_ask = about(item, ask_thing)
            says_scene = about(item, scene)
            if says_scene and not says_ask:
                continue
            if says_scene and whole_line_first:
                continue
            return item
        turned_down.clear()
    if plain is not None:
        for _asked, _ranked, _plans, _named, _keys, item, _on_ask in plain:
            if item.id in turned_down:
                continue
            if reject is not None and reject(item):
                continue
            if _the_subject_it_avoids(item, forms, carried):
                continue
            return item
    return _other_reading(understood, words, clean, entries, reject)


HOUSEHOLD_WORDS = {
    "we": "i", "us": "me", "our": "my", "ours": "mine", "ourselves": "myself",
    "weve": "ive", "we'd": "i'd", "we'll": "i'll", "we're": "i'm", "we've": "i've",
}


def _household_reading(words):
    shifted = [HOUSEHOLD_WORDS.get(str(word).lower(), word) for word in words]
    return shifted if shifted != list(words) else None


def _other_reading(understood, words, clean, entries, reject):
    plain = understood.get("plain")
    if isinstance(plain, str) and plain and plain != clean:
        again = {key: value for key, value in understood.items() if key != "plain"}
        again["clean"] = plain
        again["words"] = [word.lower() for word in _words_of(plain)]
        found = find(again, entries, reject)
        if found is not None:
            return found
    tidied = [word for word in understood.get("norm") or [] if isinstance(word, str)]
    typed = [word.lower() for word in words if isinstance(word, str)]
    if tidied and tidied != typed and understood.get("norm"):
        again = {key: value for key, value in understood.items() if key != "plain"}
        again["clean"] = " ".join(tidied)
        again["words"] = tidied
        again["norm"] = []
        return find(again, entries, reject)
    shifted = _household_reading([word for word in words if isinstance(word, str)])
    if shifted:
        again = {key: value for key, value in understood.items()
                 if key not in ("plain", "norm")}
        again["clean"] = " ".join(shifted)
        again["words"] = shifted
        return find(again, entries, reject)
    return None



CONTEXT_WORDS = 8


SPECIFIC = 3


def _says_a_key_word(item, forms, rarity=None):
    if rarity is None:
        rarity = {}
    for part in item.key:
        for _, words, _ in _part_matches(part, forms):
            if len(words) != 1:
                continue
            if any(ch.isdigit() for ch in words[0]) or rarity.get(words[0], 0) <= SPECIFIC:
                return True
    return False


def _touches(item, forms, rarity=None):
    if rarity is None:
        rarity = {}
    for part in item.key:
        for _, words, _ in _part_matches(part, forms):
            if words and all(word in A_SAYS_NOTHING for word in words):
                continue
            if len(words) > 1 or any(ch.isdigit() for ch in words[0]) \
                    or rarity.get(words[0], 0) <= SPECIFIC:
                return True
    return False


def _parts_across(item, carried_forms, forms):
    own, above = set(), set()
    for index, part in enumerate(getattr(item, "key", ()) or ()):
        if _part_matches(part, forms):
            own.add(index)
        if _part_matches(part, carried_forms):
            above.add(index)
    return bool(own - above) and bool(above - own)


def key_words(item):
    found = set()
    for part in getattr(item, "key", ()) or ():
        options = (part,) if isinstance(part, str) else part
        for option in options:
            for word in str(option).lower().split():
                found.add(word.rstrip("s") or word)
    return found


def about(item, subject):
    head = (str(subject or "").split() or [""])[-1]
    head = head.rstrip("s") or head
    return bool(head) and head in key_words(item)


WEIGHT_UNITS = frozenset(("kg", "kgs", "g", "gram", "grams", "kilogram", "kilograms",
                          "kilo", "kilos", "lb", "lbs", "pound", "pounds", "oz",
                          "ounce", "ounces"))


def a_weight(understood):
    for number in (understood or {}).get("numbers") or ():
        if isinstance(number, dict) and str(number.get("unit") or "").lower() in WEIGHT_UNITS:
            return True
    return False


PERSON_PRONOUNS = frozenset("he she they him them".split())


def _refers_to_the_person(understood):
    words = understood.get("norm")
    if not isinstance(words, list):
        words = str(understood.get("text") or "").lower().split()
    return any(word in PERSON_PRONOUNS for word in words)


SPEAKER_ONLY = ("i", "im", "ive", "id", "ill")
HANDLING_WORDS = ("say", "saying", "said", "tell", "telling", "answer", "answering", "agree",
                  "agreeing", "refuse", "refusing", "nod", "nodding", "smile", "smiling",
                  "laugh", "laughing", "apologise", "apologize", "explain", "explaining",
                  "ask", "asking", "keep", "keeps", "always", "never", "just", "usually")


def _says_how_the_speaker_handles_it(understood):
    line = tokens(str(understood.get("clean") or understood.get("text") or ""))
    if not line or line[0] not in SPEAKER_ONLY:
        return False
    keys = [word for word in (understood.get("keywords") or []) if isinstance(word, str)]
    if not keys:
        return False
    return all(word in HANDLING_WORDS for word in keys)


def _following_on(understood, entries, forms, typed, by_domain, every, known=(), reject=None):
    leans = understood.get("leans_on")
    if not isinstance(leans, dict):
        return None
    words = leans.get("words") if isinstance(leans.get("words"), list) else []
    carried = [word for word in words if isinstance(word, str)][:CONTEXT_WORDS]
    if not carried:
        return None
    carried_forms = [_forms(word) for word in carried]
    _read_typos(carried, carried_forms, every, known)
    together = carried_forms + forms
    together_typed = carried + typed
    allowed = _topic_domains(understood, entries)
    best, best_score, best_domain = None, 0, ""
    seen = {}
    leans_subject = leans.get("subject")
    named_subject = leans_subject if isinstance(leans_subject, str) else ""
    for item in _reaching(entries, together):
        domain = getattr(item, "domain", "") or ""
        if allowed is not None and domain not in allowed:
            continue
        if not score(item, together, together_typed, seen):
            continue
        if reject is not None and reject(item):
            continue
        if not guard_passes(item, understood):
            continue
        ranked = _rank(item, together, by_domain.get(domain) or every, seen)
        if ranked and named_subject and about(item, named_subject):
            ranked += 100
        if ranked > best_score:
            best, best_score, best_domain = item, ranked, domain
    if _only_asking_about_it(understood, leans):
        back = _the_best_entry(leans, entries, reject, False)
        if back is not None and not (best is not None and best is not back
                                     and _parts_across(best, carried_forms, forms)):
            best, best_domain = back, getattr(back, "domain", "") or ""
    if best is not None and not _touches(best, forms, by_domain.get(best_domain) or every):
        if not _parts_across(best, carried_forms, forms) \
                and not _only_asking_about_it(understood, leans):
            return None
    said = best is not None and _says_a_key_word(best, forms,
                                                  by_domain.get(best_domain) or every)
    if best is not None and not _reaches(best, carried_forms):
        return None
    subject = leans.get("subject")
    named = isinstance(subject, str) and bool(subject)
    if best is not None and named and not about(best, subject):
        return None
    if (best is not None and named and leans.get("subject_type") == "person"
            and understood.get("kind") not in ("question", "request")
            and _refers_to_the_person(understood) and not said):
        head = set(_forms(str(subject).split()[-1]))
        other = [forms for forms in carried_forms if not (forms & head)]
        words = set()
        for word in key_words(best):
            words |= _forms(word)
        if (other and not _reaches(best, other)
                and not any(forms & words for forms in other)):
            return None
    if best is not None and not named:
        if not _touches(best, carried_forms, by_domain.get(best_domain) or every):
            return None
    if best is not None and not _in_topic(best, understood):
        return None
    return best


_WEAR_ASK = re.compile(
    r"\b(?:what|which|how)\b[^.?!]{0,40}?\b(?:wear|wearing|put on|dress code)\b"
    r"|\b(?:what|which)\b[^.?!]{0,25}?\boutfit\b")


def asks_what_to_wear(understood):
    said = ""
    if isinstance(understood, dict):
        said = str(understood.get("text") or understood.get("clean") or "")
        if not said:
            words = understood.get("words")
            said = " ".join(str(word) for word in words) if isinstance(words, (list, tuple)) else ""
    return bool(_WEAR_ASK.search(" ".join(tokens(said)))) or a_colour_is_worn(understood)


def _topic_domains(understood, entries=None):
    topics = []
    if isinstance(understood, dict):
        found = understood.get("topics")
        topics = list(found) if isinstance(found, (list, tuple)) else []
        topics.append(understood.get("topic"))
        leans = understood.get("leans_on")
        if isinstance(leans, dict):
            topics.append(leans.get("topic"))
    topics = [topic for topic in topics if isinstance(topic, str) and topic]
    if not topics:
        return None
    from . import by_topic
    judged = by_topic()
    allowed = {name for name, answered in judged.items()
               if not answered or any(topic in answered for topic in topics)}
    if entries is not None:
        allowed &= {getattr(item, "domain", "") or "" for item in entries}
    if allowed and asks_what_to_wear(understood):
        allowed.add("clothing")
    return allowed if allowed else None


def _in_topic(item, understood):
    allowed = _topic_domains(understood)
    if allowed is None:
        return True
    return (getattr(item, "domain", "") or "") in allowed


def about_the_topic(item, understood):
    return _in_topic(item, understood)


MISSING_WORDS = re.compile(
    r"\b(?:no|not|without|havent|hasnt|hadnt|dont|doesnt|didnt|cant|cannot|isnt|arent|wasnt|"
    r"wont|lack|lacks|lacking|empty|none|nothing|ran out|run out|out of)\b")


def _is_a_person(understood, word):
    for ent in (understood or {}).get("entities") or ():
        if isinstance(ent, dict) and str(ent.get("text", "")).lower() == str(word).lower():
            return ent.get("type") == "person"
    return False


def _says_what_is_missing(understood):
    focus = list((understood or {}).get("focus") or ())
    for clause in (understood or {}).get("clauses") or ():
        if list(clause) == focus:
            continue
        text = " ".join(str(word) for word in clause if isinstance(word, str))
        if MISSING_WORDS.search(text):
            return True
    return False


def _reaches(item, forms):
    for part in item.key:
        if _part_matches(part, forms):
            return True
    return False


def names_its_own_subject(item, understood):
    if not isinstance(understood, dict):
        return False
    clean = understood.get("clean") or understood.get("text") or ""
    forms = [_forms(word) for word in tokens(str(clean))]
    key = getattr(item, "key", ()) or ()
    return bool(forms) and bool(key) and bool(_part_matches(key[0], forms))

def _wrapped_subject(clean, norm_text=None):
    plain = " ".join(word for word in WORD.findall(clean or "") if word not in _FILLER)
    for text in (clean, norm_text, plain):
        text = " ".join((text or "").replace(" | ", " ").split())
        if not text:
            continue
        for pattern in _WRAPPED:
            found = pattern.match(text)
            if not found:
                continue
            subject = found.group("subject").strip(" .,!?;:")
            if subject.lower() in _NOT_A_THING:
                return None
            if not any(word not in _NOT_A_SUBJECT for word in WORD.findall(subject)):
                return None
            return subject
    return None


def _the_ask_it_wraps(understood, subject, whole, entries, by_domain, every, reject):
    if not subject:
        return None
    words = [word for word in tokens(subject) if word not in _SUBJECT_POINTS]
    if len(words) == 1:
        alone = _the_subject_alone(" ".join(words), entries, by_domain, every, reject)
        if alone is not None:
            if whole is not None and getattr(whole, "id", "") in ASK_FRAME_IDS:
                return None
            return alone
    if whole is not None:
        return None
    again = {key: value for key, value in understood.items()
             if key not in ("plain", "norm", "norm_text")}
    again["clean"] = subject
    again["words"] = [word.lower() for word in _words_of(subject)]
    found = find(again, entries, reject)
    if found is not None:
        return found
    return _the_subject_alone(subject, entries, by_domain, every, reject)


COMMON_WORD = 12


def names_one_thing(words, every):
    for word in words:
        counts = [every.get(form) or 0 for form in _forms(word)]
        if not counts or max(counts) > COMMON_WORD:
            return False
    return True


def _the_subject_alone(subject, entries, by_domain, every, reject=None):
    words = tokens(subject)
    if not words:
        return None
    forms = [_forms(word) for word in words]
    typed = [word.lower() for word in words if isinstance(word, str)]
    return _best({"clean": subject, "words": None, "kind": "question"}, words, subject, forms,
                 typed, entries, by_domain, every, reject,
                 framed=names_one_thing(
                     [word for word in words if word not in _SUBJECT_POINTS], every))


GONE_OFF_SIGNS = ("smells", "smell", "smelly", "smelling", "stinks", "stinking", "slimy",
                  "gone off", "went off", "going off", "has gone off", "have gone off",
                  "gone bad", "has gone bad", "has gone slimy", "have gone slimy",
                  "out of date", "past its date", "past the date", "past their date",
                  "use by", "use-by", "best before", "still ok", "still good", "still fine",
                  "ok to eat", "safe to eat", "is it off", "mouldy", "moldy", "funny smell",
                  "off smell", "bin it", "bin them", "throw it away", "throw them away",
                  "throw it out", "throw them out")


def says_it_has_gone_off(clean):
    low = " %s " % str(clean or "").lower()
    return any((" %s " % sign) in low or (" %s" % sign) in low
               for sign in GONE_OFF_SIGNS)


def said_in_this_line(understood, memory=None):
    if isinstance(memory, dict):
        typed = memory.get("asked_now")
        if isinstance(typed, str) and typed.strip():
            return typed.strip()
    if not isinstance(understood, dict):
        return ""
    typed = understood.get("said_now")
    if isinstance(typed, str) and typed.strip():
        return typed.strip()
    focus = understood.get("focus")
    if understood.get("setup") and isinstance(focus, list) and focus:
        return " ".join(str(word) for word in focus).strip()
    text = str(understood.get("clean") or understood.get("text") or "")
    leans = understood.get("leans_on")
    carried = str(leans.get("text") or "") if isinstance(leans, dict) else ""
    if carried:
        low, carried = text.lower(), carried.lower()
        if carried in low:
            text = low.replace(carried, " ")
    return text.strip()
