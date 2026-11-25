import re

from .cooking import PET_LINE_WORDS
from .lookup import PACK_DATE, entry

ANSWERS = ("cooking", "food-and-drink")

_RAW_VEG_GROUPS = (
    ("potato", ("potato", "potatoes", "sweet potato", "sweet potatoes"),
     "Cook %(one)s rather than eating %(them)s raw: a raw potato and any green patch on it "
     "carry solanine, which gives stomach ache and vomiting, and the raw starch is hard to "
     "digest. Boil, roast or mash %(them)s, and bin any potato with green patches or sprouts."),
    ("starchy", ("yam", "yams", "cassava", "plantain", "plantains"),
     "Cook %(one)s rather than eating %(them)s raw: the starch is hard to digest uncooked and "
     "%(one)s tastes bitter and astringent raw. Boil, roast or fry %(them)s until tender, and "
     "peel cassava and cook it right through - raw cassava carries cyanide, and boiling or "
     "frying is what takes it out."),
    ("dried-bean", ("kidney beans", "red kidney beans", "cannellini beans", "haricot beans",
                    "black beans", "pinto beans", "butter beans", "soya beans", "soy beans",
                    "flageolet beans", "chickpeas", "chick peas", "black-eyed beans"),
     "Dried %(one)s have to be boiled hard for at least ten minutes: raw and undercooked ones "
     "carry a protein that causes violent vomiting and cramps, and a slow cooker never gets hot "
     "enough. Tinned ones are already cooked, so rinse and eat them."),
    ("green-bean", ("green beans", "runner beans", "broad beans", "french beans",
                    "string beans"),
     "Cook %(one)s rather than eating them raw: they hold a protein that upsets the stomach, so "
     "boil or steam them four to five minutes until they are tender but still squeaky. A handful "
     "raw in a salad is not dangerous for most people, but they taste better cooked."),
    ("salad", ("broccoli", "cauliflower", "kale", "spinach", "peas", "mangetout",
               "sugar snap peas", "carrot", "carrots", "cucumber", "courgette", "courgettes",
               "beetroot", "onion", "onions", "spring onion", "spring onions", "mushroom",
               "mushrooms", "cabbage", "red cabbage", "sweetcorn", "sweet corn", "pepper",
               "peppers", "bell pepper", "celery", "radish", "radishes", "lettuce", "fennel",
               "avocado", "tomato", "tomatoes", "cress", "watercress", "rocket", "leek",
               "garlic", "ginger", "parsnip", "swede", "turnip"),
     "%(Cap)s %(are)s fine raw: wash %(them)s and eat %(them)s as %(they)s %(are)s - the "
     "crunch and the vitamins are what cooking takes out. A minute in boiling water softens "
     "%(them)s if you would rather have %(them)s cooked."),
)

_RAW_VEG_PLURAL_S = frozenset(("sweetcorn", "sweet corn", "cress", "watercress", "mangetout"))

_RAW_VEGETABLE_NAMES = tuple(sorted(
    (name for _, names, _ in _RAW_VEG_GROUPS for name in names), key=len, reverse=True))

_RAW_VEG_ONE = dict((name, (group, text)) for group, names, text in _RAW_VEG_GROUPS
                    for name in names)

_RAW_VEGETABLE_NOT = (
    "how long", "how do i cook", "how to cook", "how long to cook", "how long do i cook",
    "recipe", "recipes", "roast", "roasting", "roasted", "boil", "boiling", "boiled", "steam",
    "steaming", "fry", "frying", "fried", "air fry", "air fryer", "slow cooker", "soup",
    "curry", "stew", "bake", "baking", "baked", "microwave", "grow", "growing", "grown",
    "plant", "planting", "garden", "allotment", "seed", "seeds", "harvest", "blight",
    "fridge", "freezer", "freeze", "keeping", "keeps", "keep", "store", "shop", "buy",
    "cheapest", "price", "calories", "protein", "fibre", "vitamin", "nutrition", "diet",
    "sprout", "sprouts", "alfalfa", "beansprouts", "bean sprouts", "green potato",
    "green potatoes", "solanine", "dog", "dogs", "puppy", "cat", "cats", "kitten",
    "vet", "rabbit", "hamster", "guinea pig", "bird", "chicken", "chickens",
)


def _raw_vegetable(memory, reading=None):
    understood = reading if isinstance(reading, dict) else {}
    text = " " + str(understood.get("clean") or "").replace("'s", " ") + " "
    for name in _RAW_VEGETABLE_NAMES:
        if " %s " % name not in text:
            continue
        _, template = _RAW_VEG_ONE[name]
        plural = name.endswith("s") and name not in _RAW_VEG_PLURAL_S
        return template % {"one": name, "Cap": name[:1].upper() + name[1:],
                           "them": "them" if plural else "it",
                           "they": "they" if plural else "it",
                           "are": "are" if plural else "is"}
    return None


OFF_ASKS = ("ok", "okay", "safe", "still", "eat", "eat it", "bin", "throw", "use", "use it",
            "fine", "smell", "smells", "smelly", "sour", "bad", "should i keep", "should i",
            "slimy", "slime", "slimy feel", "tacky", "musty", "discoloured", "discolored",
            "grey green", "grey-green", "green patches", "gone slimy", "is slimy",
            "off", "gone off", "going off", "go off", "went off", "gone bad",
            "how do i know", "how can i tell", "how do you tell", "know if", "tell if",
            "fresh", "is fresh", "still fresh", "smells fresh", "looks fresh", "fresh to eat",
            "fresh enough", "is it fresh", "fresh or not",
            "out of date", "past its date", "past the date", "past their date",
            "use by", "use by date", "best before", "gone past",
            "next day", "the next day", "the day after", "day after", "day later",
            "days later", "yesterday", "in the fridge", "out of the fridge",
            "slimy", "gone slimy", "went slimy", "is slimy", "looks slimy",
            "smells off", "smelt off", "smells wrong", "smells funny", "has gone",
            "gone bad", "has gone bad", "looks off", "is off")

OFF_THE_THING = ("off the", "off my", "off your", "off his", "off her", "off its", "off them",
                 "off it", "cut off", "cutting off", "chop off", "chopping off", "slice off",
                 "skin off", "take the skin", "fat off", "off the bone", "turn off", "turned off",
                 "switch off", "switched off", "day off", "days off", "time off", "off work",
                 "off sick", "show off", "better off", "worse off", "off the menu", "off the heat",
                 "off the hob", "off the plate")

OFF_WORDS = PACK_DATE + (
             "still ok", "still ok to eat", "still good", "ok to eat", "okay to eat", "gone off",
             "going off", "off", "smells", "smell", "smelly", "slimy", "funny", "bad",
             "tacky", "musty", "discoloured", "discolored", "grey green", "grey-green",
             "gone bad", "past it", "past its date", "is it safe", "safe to eat",
             "out of date", "past the date", "past their date", "use by", "use by date",
             "best before", "gone past", "gone past its date",
             "fresh", "is fresh", "still fresh", "smells fresh", "looks fresh", "fresh to eat",
             "fresh enough", "is it fresh", "fresh or not",
             "next day", "the next day", "the day after", "day after", "yesterday", "tomorrow",
             "tomorow", "tmrw", "tomoz",
             "in the fridge", "out of the fridge",
             "after a day", "after one day", "after 2 days", "after two days", "after 3 days",
             "after three days", "after 4 days", "after four days", "after 5 days",
             "after five days", "a couple of days later", "a few days later",
             "bin", "bin it", "throw", "throw it", "throw away", "throw out", "chuck",
             "toss", "chuck it", "toss it",
             "still eat", "eat this", "eat that", "can i eat", "still alright",
             "still all right", "alright")

SPOILAGE_BIAS = 3

EXTRA_FOODS = ("yogurt", "yoghurt", "cream", "soured cream", "single cream", "double cream",
               "ham", "gammon", "leftover", "leftovers", "pate", "smoked salmon", "prawn",
               "prawns", "sausage", "sausages", "burger", "burgers", "milk", "kefir")


def _names_no_food(understood):
    from . import meals
    understood = understood if isinstance(understood, dict) else {}
    words = {str(word).lower() for word in (understood.get("words") or ())}
    text = " " + str(understood.get("clean") or "").lower() + " "
    known = meals.IN_A_DISH | set(meals.INGREDIENTS) | set(EXTRA_FOODS)
    if any(word in known for word in words):
        return False
    return not any(name in known and (" %s " % name) in text for name in known)


DIET_WORDS = ("every day", "a day", "a week", "per day", "per week", "healthy", "unhealthy",
              "good for you", "bad for you", "diet", "dieting", "processed", "nutrition",
              "nutritious", "protein", "calories", "vitamins", "how many", "too much",
              "too many", "pregnant", "pregnancy", "listeria", "cholesterol", "diabetic",
              "diabetes", "allergic", "allergy", "intolerant", "lactose", "toddler", "baby",
              "for a toddler", "for a baby")

RAW_WORDS = ("raw", "undercooked", "undercook", "underdone", "bloody", "raw inside",
             "pink in the middle", "still pink", "not cooked through", "rare", "medium rare",
             "blue steak")

UNDERCOOKED_PINK = RAW_WORDS + ("pink",)

_NOT_THIS = ("frozen", "defrost", "defrosting", "thaw", "thawing", "left out", "overnight",
             "buy", "buying", "to buy", "shop for", "shopping list",
             "room temperature", "reheat", "reheating", "reheated", "heat up", "heated up",
             "warm up", "microwave", "warm through", "piping hot", "fridge",
             "how many days", "how many day", "does it last", "do they last", "will it last",
             "days in the fridge", "day in the fridge", "days in a fridge",
             "how long", "why", "what causes", "cause",
             "how do i keep", "how do i store", "how to keep", "how to store",
             "how can i keep", "how should i keep", "how can i store",
             "dry", "dried out", "overcooked", "rubbery", "tough", "chewy",
             "refreeze", "refroze", "re-freeze", "refreezing", "freeze again", "frozen again",
             "sold me", "sold us", "sold it to me", "refund", "money back", "take it back",
             "take them back", "bring it back", "return it", "bought it like that",
             "illegal to sell", "sell food", "selling food", "sell by", "complaint",
             "complain", "bought out of date", "bought it out of date", "bought this out of date",
             "buying out of date", "out of date when i bought", "was out of date when i bought",
             "freezer burn", "freezer burnt", "freezerburn", "freezer-burn", "freezer burned",
             "frost bitten", "frostbite")

UNRIPE_WORDS = ("unripe", "unripened", "underripe", "under ripe", "not ripe", "isnt ripe",
                "green tomatoes", "green tomato", "green bananas", "green banana",
                "green plums", "green mango", "hard avocado", "hard mango", "hard peach",
                "hard peaches", "hard pears")
UNRIPE_NOT = ("potato", "potatoes", "solanine", "chutney", "relish", "recipe", "recipes",
              "make", "making", "cook", "cooking", "cook them", "fried green", "fry",
              "how do i ripen", "ripen them", "get them to ripen", "plant", "growing", "grow",
              "shop", "buy", "pick", "when to pick", "harvest", "blight", "garden")

POISONING_WORDS = ("food poisoning", "poisoning", "campylobacter", "salmonella", "listeria",
                   "give you", "give me", "make you ill", "make you sick", "make me ill",
                   "make me sick", "get ill", "get sick", "harmful", "carry", "causes",
                   "cause food", "why is it bad", "why is chicken bad", "why dangerous")
POISONING_NOT = ("how long", "how many days", "how do i cook", "how do i cook it", "cook it",
                 "cooking time", "roast", "roasting", "temperature", "defrost", "defrosting",
                 "thaw", "thawing", "freeze", "freezing", "fridge", "freezer", "rice",
                 "left out", "reheat", "reheating", "i have", "i got", "i ate", "i think i",
                 "my stomach", "diarrhoea", "vomiting", "symptoms", "treatment", "how to treat",
                 "restaurant", "takeaway", "cafe", "pub", "wedding", "buffet", "kebab",
                 "gave me", "made me", "report", "complaint", "claim", "compensation",
                 "sue", "advice", "what should i do")

MINCE_WORDS = ("mince", "minced", "mincemeat", "mince meat", "ground beef", "ground meat",
               "ground lamb", "ground pork", "beef mince", "lamb mince", "pork mince",
               "turkey mince", "chicken mince")

MINCE_KEEPING_WORDS = ("day", "days", "next day", "the day after", "day after", "days later",
                       "keep", "keeps", "keeping", "kept", "how long",
                       "ok to eat", "safe to eat", "use by",
                       "yesterday", "tomorrow", "tonight", "left out", "left over", "leftovers",
                       "in the fridge", "out of the fridge", "fridge", "freezer", "frozen")


_A_FAULT_IN_THE_DISH = re.compile(
    r"\b(?:too (?:hot to eat|hot for|spicy|salt\w*|sweet|sour|bland|thick|thin|dry)"
    r"|way too (?:spicy|hot|salty)|less spicy|make it milder|too much (?:chilli|chili|salt|spice)"
    r"|to cool it down)\b")


def _not_a_fault_in_the_dish(understood):
    said = str((understood or {}).get("clean") or "").lower()
    return not _A_FAULT_IN_THE_DISH.search(said)

MINCE_VERDICT_WORDS = ("still ok", "still good", "still fine", "still safe", "still alright",
                       "still all right", "smells", "smell", "smelly", "slimy", "sour", "off",
                       "gone bad", "gone off", "went off", "looks off", "is off", "green")


def _mince_keeping_is_its_own_row(understood):
    said = str((understood or {}).get("text") or (understood or {}).get("clean") or
               " ".join((understood or {}).get("words") or ())).lower()
    said = " %s " % re.sub(r"[^a-z0-9']+", " ", said).strip()
    if not any(" %s " % word in said for word in MINCE_WORDS):
        return True
    if any(" %s " % word in said for word in MINCE_VERDICT_WORDS):
        return True
    return not any(" %s " % word in said for word in MINCE_KEEPING_WORDS)
_KEEPING_IN_THE_LINE = ("fridge", "freezer", "keep", "keeps", "keeping", "last", "lasts",
                        "ok", "okay", "safe", "still", "next day", "tomorrow", "gone off",
                        "go off", "went off", "smell", "smells", "slimy", "sour", "days",
                        "how long", "bin", "throw", "eat")


_PAST_KEEPING = ("yesterday", "last night", "this morning", "days ago", "day ago",
                 "the day before", "a couple of days", "a few days")
_COOKING_ASK = ("what can i make", "what can i do with", "what should i make", "what can i cook",
                "what shall i cook", "what should i cook", "cook tonight", "cook for dinner",
                "make tonight", "recipe", "recipes", "meal idea", "ideas for", "idea for",
                "how do i make", "how to make", "how do i cook", "how to cook", "cook it",
                "reheat", "re-heat", "use up", "using up", "what goes with", "serve with",
                "side for", "freeze")


def _not_a_recipe_now(understood):
    text = " ".join(str((understood or {}).get("clean") or "").lower().split())
    if any(word in text for word in _COOKING_ASK):
        return False
    if any(word in text for word in _KEEPING_IN_THE_LINE):
        return True
    return any(word in text for word in _PAST_KEEPING)


_COUNT_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
                "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "fourteen": 14,
                "a couple of": 2, "a few": 3, "a": 1}
_DAYS_AGO = re.compile(
    r"\b(\d{1,2}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|fourteen)"
    r"\s+days?\s+(?:ago|old|since)\b|"
    r"\b(?:in the fridge|in there|sat there|sitting there|been there|in the pot|in the tub)"
    r"(?:\s+(?:for|about|nearly|over))?\s+(\d{1,2}|one|two|three|four|five|six|seven|eight|"
    r"nine|ten|eleven|twelve|fourteen)\s+days?\b|"
    r"\b(?:made|cooked|did it|made it|cooked it)\s+(\d{1,2}|one|two|three|four|five|six|seven|"
    r"eight|nine|ten|eleven|twelve|fourteen)\s+days?\b", re.I)
_DAYS_SAID = (
    ("the day before yesterday", 2), ("yesterday", 1), ("this morning", 0), ("last night", 1),
    ("tomorrow", 1), ("the next day", 1), ("next day", 1),
    ("a couple of days", 2), ("two days", 2), ("a few days", 3), ("three days", 3),
    ("a week", 7), ("a fortnight", 14), ("a month", 30),
)


def _how_many_days_ago(text):
    match = _DAYS_AGO.search(text)
    if match:
        said = next(part for part in match.groups() if part)
        number = _COUNT_WORDS.get(said.lower())
        return int(said) if number is None else number
    for phrase, days in _DAYS_SAID:
        if phrase in text:
            return days
    return None


_ENDS_ON_AN_ASK = re.compile(r"\b(?:ok|okay|alright|all right|safe|edible)\s*[.!]*$", re.I)
_VERDICT_ASKS = ("can i", "could i", "should i", "shall i", "do i", "is it", "is that", "is this",
                 "will it", "would it", "are they", "does it", "ok to", "okay to", "safe to",
                 "still ok", "still good", "still fine", "am i ok", "too late", "gone off")

def _the_verdict_on_the_days(days):
    if days is None:
        return ""
    if days <= 0:
        return "Yes - it is from today or last night, so it is fine."
    if days == 1:
        return "Yes - a day in the fridge is nothing, so it is fine."
    if days <= 3:
        return ("Yes - %d days is inside the 3 to 4 days a cooked dish keeps in the fridge, so it "
                "is fine." % days)
    if days == 4:
        return ("At the edge, I'm afraid: 3 to 4 days is the limit, so today is the last day I "
                "would eat it and I would not leave it for tomorrow.")
    return ("No, I would not: a cooked dish keeps 3 to 4 days in the fridge, and rice only 1, so "
            "%d days is past it." % days)


_LEFTOVERS_RULE = ("Cooled within two hours and kept covered in the fridge, a cooked dish keeps 3 "
                   "to 4 days, and anything with rice in it only 1. Reheat only the portion you "
                   "are eating, once, until it is piping hot right through - a second reheating is "
                   "where people get caught. It is past it if it smells sour or looks slimy, and "
                   "if it sat out warm for more than 2 hours, bin it whatever it looks like.")


def _the_leftovers_answer(memory, reading):
    from .lookup import the_line

    reading = reading if isinstance(reading, dict) else {}
    said = " ".join(str(reading.get("clean") or "").lower().split())
    asked = (any(word in said for word in _VERDICT_ASKS)
             or "?" in str(reading.get("text") or "")
             or bool(_ENDS_ON_AN_ASK.search(said)))
    if not asked:
        return _LEFTOVERS_RULE
    verdict = _the_verdict_on_the_days(_how_many_days_ago(the_line(reading)))
    if not verdict:
        return _LEFTOVERS_RULE
    if verdict.startswith("No"):
        return verdict + (" Reheating does not make it safe: the toxins old food builds up do not "
                          "all break down with heat and they do not all smell.")
    return verdict + " " + _LEFTOVERS_RULE



_MONEY_IN_THE_LINE = re.compile(
    r"[£$€]\s?\d|\b\d+\s?(?:pounds?|quid|dollars?|euros?|bucks?)\b|"
    r"\b(?:money|budget|pay|paid|payday|salary|wages?|savings?|income|pension|"
    r"rent|mortgage|bills?|overdraft|debt|direct debit|standing order)\b|"
    r"\b\d{2,}\s*(?:left ?overs?|spare|over a month|over each|over every)\b|"
    r"\b(?:left ?overs?|spare)\b[^?.!]{0,20}\b(?:each|every|per)\s+(?:week|month|year|payday)\b")


def _not_about_money(understood):
    if not isinstance(understood, dict):
        return True
    said = " ".join(str(value) for value in (understood.get(key) for key in
                                             ("clean", "norm_text", "text", "plain"))
                    if isinstance(value, str)).lower()
    return _MONEY_IN_THE_LINE.search(said) is None

ENTRIES = (
    entry("chicken-food-poisoning", (("chicken", "chickens", "turkey"),
                                     POISONING_WORDS),
          "Yes - chicken is the commonest source of food poisoning in Britain, because "
          "campylobacter lives on the raw meat and a drop of the juice is enough to make you ill. "
          "Heat is what kills it: cook chicken right through to 74C in the thickest part, don't "
          "wash it raw (that splashes the bacteria round the sink), keep it away from anything you "
          "eat uncooked, and wash your hands, the board and the knife afterwards. Symptoms come 1 "
          "to 3 days later, usually cramps and diarrhoea for about a week, and the thing that "
          "matters is fluid; blood in it, a high fever or a week with no improvement is a GP.",
          avoid=POISONING_NOT + DIET_WORDS + _NOT_THIS + OFF_THE_THING + RAW_WORDS
          + ("dog", "dogs", "puppy", "cat", "cats", "kitten", "pet", "pets", "vet",
             "swallowed", "swallow", "chewed", "choking", "choke", "vomiting"),
          bias=6),
    entry("plant-leaves-poisonous",
          (("tomato leaves", "tomato leaf", "tomato plant leaves", "tomato stems",
            "potato leaves", "potato leaf", "potato shoots", "potato sprouts",
            "rhubarb leaves", "rhubarb leaf", "aubergine leaves", "courgette leaves"),
           ("poison", "poisonous", "toxic", "toxic to", "safe to eat", "safe to feed",
            "edible", "can i eat", "can you eat", "eat them", "eat the leaves", "harmful",
            "dangerous", "eat it")),
          "The leaves and stems of tomatoes, potatoes and rhubarb contain solanine and oxalic "
          "acid, which are mild poisons: a stray leaf in a salad will do you no harm, but a "
          "plateful brings a stomach ache, sickness and diarrhoea, and cooking does not destroy "
          "it. So don't eat them and don't brew them as tea, wash your hands after handling the "
          "plants, and keep pets and small children away from the leaves. The fruit, the tubers "
          "and the rhubarb stalks are the parts that are food.",
          avoid=("yellow", "yellowing", "pale", "blight", "spots", "curl", "curling", "wilt",
                 "wilting", "holes", "black", "brown", "feed", "fertiliser", "compost", "prune",
                 "pruning", "grow", "growing", "harvest", "plant them", "when to plant"),
          bias=2),
    entry("still-chicken", ("chicken", OFF_WORDS),
          "Chicken is the one to be strict about: a sour or ammonia smell, a tacky or slimy feel, "
          "or any change of colour means bin it, and cooking it will not make it safe. Raw chicken "
          "keeps 1 to 2 days in the fridge and cooked chicken 3; if it has sat out warm for more "
          "than 2 hours, that is enough on its own.",
          avoid=DIET_WORDS + UNDERCOOKED_PINK + _NOT_THIS + PET_LINE_WORDS + OFF_THE_THING,
          ask=OFF_ASKS, bias=SPOILAGE_BIAS),
    entry("still-meat", (("meat", "beef", "lamb", "pork", "steak", "mince", "joint"), OFF_WORDS),
          "Red meat is more forgiving than chicken: a grey-brown colour on the outside of a chop "
          "is just air and it is fine, but a sour or putrid smell, a sticky tacky surface or "
          "green patches means bin it. Raw beef, lamb and pork keep 3 to 5 days in the fridge, "
          "mince only 1 to 2.",
          guard=_mince_keeping_is_its_own_row,
          avoid=DIET_WORDS + UNDERCOOKED_PINK + _NOT_THIS + PET_LINE_WORDS + OFF_THE_THING,
          ask=OFF_ASKS, bias=SPOILAGE_BIAS),
    entry("still-fish", (("fish", "salmon", "cod", "prawns", "prawn", "haddock", "tuna",
                          "fish is off", "fish off", "fish gone off", "fish has gone off",
                          "salmon is off", "prawns are off", "fish gone bad", "fish is bad",
                          "fish is fresh", "fish fresh", "salmon is fresh", "salmon fresh",
                          "prawns are fresh", "cod is fresh"),
                         OFF_WORDS),
          "Fish goes off faster than anything else and does not forgive it: it should smell of the "
          "sea, so an ammonia or fishy-sharp smell, flesh that stays dented when you press it, or "
          "grey gills means bin it. Use it the day you buy it or freeze it that day.",
          avoid=DIET_WORDS + RAW_WORDS + _NOT_THIS + PET_LINE_WORDS + OFF_THE_THING
          + ("kitchen", "fried", "frying", "fry", "get rid of the smell", "smell out",
             "tank", "fish tank", "aquarium", "goldfish", "pond", "ponds", "fish bowl",
             "tropical fish", "pet fish", "fish tank water",
             "dishwasher", "washing machine", "fridge", "freezer", "oven", "microwave", "sink",
             "bin", "bins", "bin smells", "cupboard smells", "room smells", "house smells",
             "smells of fish", "smells like fish", "smelling of fish",
             "how often", "a week", "per week", "every day", "every other day", "twice a week",
             "three times a week", "times a week"),
          ask=OFF_ASKS, bias=SPOILAGE_BIAS + 1),
    entry("still-ham", (("ham", "bacon", "sausage", "sausages", "salami", "chorizo"), OFF_WORDS),
          "Cured meat is not immune: a slimy feel, a sour or musty smell, or grey-green patches "
          "means bin it. Ham keeps about 3 days once the pack is open, dry-cured bacon up to a "
          "week, and sausages 2 to 3 days.",
          avoid=DIET_WORDS + RAW_WORDS + _NOT_THIS + PET_LINE_WORDS + OFF_THE_THING,
          ask=OFF_ASKS, bias=SPOILAGE_BIAS),
    entry("still-yogurt", (("yogurt", "yoghurt", "cream", "creme fraiche", "soured cream"),
                           OFF_WORDS),
          "Bin it if it smells sour or fizzy rather than tangy, or if there is any mould on the "
          "surface; a little watery separation on top is fine, so stir it back in. Cream keeps "
          "about 5 days once opened, and yogurt a week past its date if it has been in the fridge.",
          avoid=DIET_WORDS + _NOT_THIS + PET_LINE_WORDS + OFF_THE_THING
          + ("sun cream", "suncream", "sunscreen", "sunblock", "moisturiser", "moisturizer",
             "face cream", "hand cream", "body cream", "eczema cream", "nappy cream",
             "shaving cream", "cold cream", "ice cream", "eye cream", "facial cream", "spot cream",
             "out of date", "past the date", "past its date", "past their date", "use by",
             "use by date", "best before", "date on the lid", "went out of date",
             "starter", "starters", "sourdough", "ginger bug", "kombucha scoby"),
          ask=OFF_ASKS, bias=SPOILAGE_BIAS),
    entry("still-date-rule", (("out of date", "past its date", "past the date", "past their date",
                               "use by", "use by date", "use-by", "best before", "best-before",
                               "gone past", "after the date", "date on it", "date on the",
                               "still edible"),
                              ("is my", "is it", "is this", "is that", "are my", "are these",
                               "my", "still", "ok", "safe", "good", "edible", "eat", "keep",
                               "bin", "throw", "use")),
          "Two dates mean two things: use-by is about safety, so the food goes in the bin after "
          "it, even if it looks and smells fine; best-before is about quality, so dry rice, "
          "pasta, flour and sugar are fine for months past it, and a tin for years. For anything "
          "fresh, smell it and touch it: a sour smell, a slimy surface or mould means bin it, and "
          "cooked food is 2 days in the fridge whatever the label said.",
          avoid=DIET_WORDS + _NOT_THIS + PET_LINE_WORDS + OFF_THE_THING + (
                 "out of milk", "out of bread", "out of rice", "out of chicken", "out of cheese",
                 "out of eggs", "out of sugar", "out of flour", "run out", "ran out", "none left",
                 "havent got", "recipe", "how do i cook", "how long to cook", "how long do i cook",
                 "freeze", "defrost", "reheat", "sell by", "expiry",
                 "passport", "licence", "license", "driving licence", "mot", "insurance",
                 "warranty", "guarantee", "ticket", "tickets", "coupon", "voucher", "gift card",
                 "card", "cards", "debit card", "credit card",
                 "car is out of date", "car out of date", "car is past its", "van is out of date",
                 "van out of date", "vehicle is out of date", "bike is out of date",
                 "tyre", "tyres", "tire", "tires",
                 "membership", "subscription", "battery", "batteries", "smoke alarm", "alarm",
                 "fire extinguisher", "medicine", "medication", "tablets", "inhaler", "epipen",
                 "food bank", "sell by date", "sell-by", "expiry date", "expires"),
          ask=OFF_ASKS, bias=-3),
    entry("still-unnamed",
          (("smells off", "smelt off", "smells funny", "gone off", "has gone off",
            "went off", "smells wrong", "smells a bit off", "gone bad", "has gone bad",
            "looks off", "smells iffy", "smells dodgy"),
           ("can i cook", "can i eat", "cook it", "eat it", "still cook", "still eat",
            "ok to eat", "safe to eat", "is it ok", "is it safe", "use it", "bin it",
            "throw it", "keep it", "should i")),
          "If it smells sour, or wrong rather than just strong, bin it - cooking does not make an "
          "off food safe. Cooked rice, cooked meat and anything with a sauce are the strict ones; "
          "hard cheese and dry bread are the ones you can judge by looking.",
          avoid=("kitchen", "room", "rooms", "house", "flat", "home", "bin", "bins",
                 "drain", "drains", "fridge", "freezer", "oven", "microwave",
                 "dishwasher", "washing machine", "tumble dryer", "sink", "cupboard",
                 "car", "cars", "van", "garage", "loft", "shed", "sofa", "carpet",
                 "dog", "dogs", "cat", "cats", "puppy", "pet", "pets", "vet",
                 "smoke", "damp", "mould", "mold", "musty", "gas", "paint") + PET_LINE_WORDS,
          ask=OFF_ASKS, bias=2, guard=_names_no_food),
    entry("still-unripe", (UNRIPE_WORDS, OFF_WORDS + ("eat", "safe", "ok", "okay", "fine",
                                                     "poison", "poisonous", "toxic", "harm",
                                                     "ill", "sick", "bad for")),
          "Unripe fruit and veg are safe to eat - hard, sour and starchy rather than sweet, not "
          "poisonous - and a day or two on the counter, or in a paper bag with a banana, ripens "
          "most of them; cooking does the rest, as fried green tomatoes and green banana show. A "
          "green potato is the one exception: that green is solanine, it does not cook out, so "
          "bin it.",
          avoid=DIET_WORDS + _NOT_THIS + PET_LINE_WORDS + OFF_THE_THING + UNRIPE_NOT,
          ask=OFF_ASKS + ("eat", "safe", "poison", "poisonous", "toxic", "harm", "ill", "sick"),
          bias=3),
    entry("raw-vegetable",
          ((tuple(_RAW_VEGETABLE_NAMES),
            ("raw", "uncooked", "not cooked", "eat raw", "eat it raw", "eat them raw",
             "eat it uncooked", "without cooking", "safely eat raw", "can you eat raw"))),
          _raw_vegetable,
          avoid=_RAW_VEGETABLE_NOT,
          bias=4),
    entry("eggs-food-poisoning", (("egg", "eggs", "egg white", "egg yolk", "runny egg",
                                  "runny eggs"), POISONING_WORDS),
          "Eggs are the second commonest source after chicken, and the germ is salmonella, which "
          "sits on the shell and sometimes in the egg. In Britain a British Lion-marked egg is "
          "fine raw or runny, even in pregnancy, because those flocks are vaccinated; an unmarked "
          "egg, a duck egg or anything from abroad is the one to cook through. Keep eggs cold, "
          "don't wash them, and bin one that is cracked and dirty. Cramps and diarrhoea come 12 "
          "to 72 hours later and usually pass in a few days; fluid is the thing that matters.",
          avoid=POISONING_NOT + DIET_WORDS + _NOT_THIS + OFF_THE_THING + RAW_WORDS
          + ("dog", "dogs", "puppy", "cat", "cats", "kitten", "pet", "pets", "vet",
             "how do i cook", "boil", "boiling", "boiled", "poach", "poached", "scrambl",
             "fry", "frying", "fried", "omelette", "bake", "baking", "meringue", "mayonnaise",
             "white", "whites", "yolk", "yolks", "shell", "cracked", "crack", "float",
             "freshness", "how long", "keep", "keeps", "box", "date"),
          bias=4),
    entry("rice-food-poisoning", (("rice", "rices"), POISONING_WORDS),
          "Yes - rice is the leftover worth being strict about. The germ is bacillus cereus, "
          "whose spores survive cooking, so rice left sitting warm grows them and reheating does "
          "not always clear what they made. Cool it fast (spread it on a tray or rinse it under "
          "cold water), box it within the hour, keep it in the fridge no more than a day, and "
          "reheat it once, piping hot all the way through. Cramps and vomiting inside a few "
          "hours of eating are the usual sign; fluid is what matters, and a day of it or blood "
          "in it is a GP.",
          avoid=tuple(w for w in POISONING_NOT if w != "rice") + DIET_WORDS + _NOT_THIS
          + OFF_THE_THING + RAW_WORDS
          + ("dog", "dogs", "puppy", "cat", "cats", "kitten", "pet", "pets", "vet",
             "pudding", "risotto", "paella", "sushi", "cook", "cooking", "boil", "boiling",
             "how much water", "basmati", "brown rice", "wild rice", "microwave"),
          bias=4),
    entry("raw-sprouts", (("sprouts", "sprout", "alfalfa", "bean sprouts", "beansprouts",
                           "mung beans", "radish sprouts"),
                          ("raw", "eat", "eating", "safe", "ok", "okay", "washed", "wash",
                           "cook", "cooked", "cooking", "salad", "pregnant", "pregnancy",
                           "should i", "can i", "are they", "in a sandwich")),
          "Bean and alfalfa sprouts are the one salad thing to be careful with: they are grown "
          "warm and damp, which is exactly what bacteria like, and rinsing does not remove what "
          "has got inside the seed. Eat them cooked - stir-fried or dropped into soup for a "
          "minute - and if you want them raw, buy a bag that says ready to eat and keep it cold. "
          "Pregnant, elderly, or on treatment that lowers your immunity, cook them: the same "
          "advice covers a raw mung-bean salad.",
          avoid=("brussels", "brussel", "christmas", "roast", "roasting", "boil", "boiling",
                 "steam", "steaming", "how long", "minutes", "how do i cook", "how to cook",
                 "grow", "growing", "grown", "seed", "seeds", "garden", "window sill",
                 "windowsill", "jar", "potato", "potatoes", "get rid of", "pest", "aphid"),
          bias=3),
    entry("fly-on-food", (("fly", "flies", "bluebottle", "bluebottles", "wasp", "wasps"),
                          ("landed", "landing", "land", "on my food", "on my sandwich",
                           "on my dinner", "on my drink", "in my drink", "in my food",
                           "in my tea", "crawling", "walked on", "sat on")),
          "Brush it off and eat the food: a fly that lands for a moment leaves little behind, "
          "and the dose is what matters. If it has been walking about on it, cut away that patch "
          "or rinse what you can, and tip out a drink it fell into. What is worth avoiding is "
          "food a fly has been sitting on for a while, or anything from a bin or off the floor, "
          "because flies feed on waste and carry it on their legs.",
          avoid=("airport", "security", "hand luggage", "check in", "flight", "flights",
                 "plane", "heathrow", "gatwick", "holiday", "abroad", "how do i get rid of",
                 "get rid of flies", "infestation", "traps", "trap", "kite", "flag", "butterfly",
                 "butterflies", "drone", "dragonfl", "firefl", "fly a", "flying to",
                 "flying out", "business", "screen", "net curtains",
                 "on me", "landed on me", "landing on me", "on my arm", "on my leg",
                 "on my face", "on my neck", "on my hand", "on my head", "keeps landing",
                 "stinging", "stung", "sting", "chasing me", "buzzing", "swat"),
          bias=4),
    entry("past-it-in-the-fridge",
          (("leftovers", "leftover", "left over", "curry", "stew", "casserole", "chilli",
            "tagine", "goulash", "bolognese", "lasagne", "risotto", "soup", "stew", "rice",
            "shepherds pie", "cottage pie", "the sauce", "the broth", "the dish"),
           ("a week", "one week", "two weeks", "three weeks", "a fortnight", "fortnight",
            "weeks", "a month", "one month", "two months", "months", "week old", "weeks old",
            "last week", "the week before", "a while", "ages")),
          "Past it, I'm afraid - bin it. A cooked dish keeps 3 to 4 days in the fridge, and rice "
          "only 1, so a dish from last week is well beyond that, and reheating it does not make "
          "it safe: the toxins that build up in old food do not all break down with heat and "
          "they do not all smell. Scrape it out, wash the box with hot soapy water, and next "
          "time freeze the half you will not eat within the three days.",
          avoid=("use by", "use-by", "best before", "sell by", "date on", "supermarket", "shop",
                 "frozen", "freezer", "defrost", "thaw", "refreeze", "refroze", "reheat",
                 "reheating", "microwave", "recipe", "what can i make", "what can i cook",
                 "meal ideas", "how do i make", "how to make", "cook it", "how long do i cook",
                 "fridge is", "fridge not", "not cold", "stopped working", "warm in the fridge",
                 "temperature", "thermometer", "power cut", "smells", "sour", "slimy", "mould",
                 "mouldy", "mold", "moldy", "gone off", "go off", "off",
                 "rice", "chicken", "meat", "beef", "lamb", "pork", "fish", "prawns", "milk",
                 "cream", "yoghurt", "yogurt", "cheese", "eggs", "egg", "pasta", "bread",
                 "baby", "babies", "toddler", "child", "children", "dog", "cat", "pregnant",
                 "each month", "every month", "each week", "every week", "each year",
                 "every year", "per week", "per month", "per year", "each payday",
                 "left over each", "left over every", "left over per",
                 "leftover each", "leftover every", "leftover per", "leftover a month",
                 "leftover this month", "leftovers each", "leftovers every"),
          bias=3,
          guard=_not_about_money),
    entry("still-leftovers",
          (("leftovers", "leftover", "left over", "left in the fridge", "whats left",
            "what's left", "the rest of the", "curry", "stew", "casserole", "chilli", "tagine",
            "goulash", "bolognese", "shepherds pie", "cottage pie", "lasagne", "risotto"),
           ("ok", "okay", "is it ok", "is that ok", "safe", "is it safe", "safe to eat",
            "eat", "eat it", "still", "still good", "still ok", "next day", "the next day",
            "tomorrow", "fridge", "gone off", "go off", "went off", "smell", "smells",
            "smelly", "sour", "slimy", "days", "day", "how long", "keep", "keeps", "last",
            "lasts", "bin", "throw", "been in", "sat in", "made on", "cooked it on",
            "yesterday", "last night", "this morning",
            "a week", "one week", "two weeks", "three weeks", "a fortnight", "fortnight",
            "weeks", "a month", "one month", "two months", "months", "week old", "weeks old",
            "last week", "the week before", "a while", "ages")),
          _the_leftovers_answer,
          avoid=DIET_WORDS + UNDERCOOKED_PINK
                + ("frozen", "defrost", "defrosting", "thaw", "thawing", "left out", "overnight",
                   "all night", "all day", "room temperature", "sat out", "sitting out",
                   "how do i keep", "how do i store", "how to keep", "how to store",
                   "how can i keep", "how should i keep", "refreeze", "refroze", "re-freeze",
                   "freeze again", "reheat it twice", "how many times can i reheat",
                   "how do i reheat", "how to reheat", "best way to reheat", "why",
                   "what causes", "cause", "mouldy", "mould", "moldy", "mold")
                + ("chicken", "turkey", "meat", "beef", "lamb", "pork", "steak", "mince",
                   "fish", "salmon", "cod", "prawns", "prawn", "ham", "bacon", "sausage",
                   "egg", "eggs", "rice", "milk", "cheese", "yogurt", "yoghurt", "cream",
                   "pasta", "pizza", "bread", "potato", "potatoes", "tomato", "tomatoes",
                   "how long does", "how long do", "how long can i", "how long will",
                   "how long should", "how long to",
                   "simmer", "simmering", "boil", "boiling", "fry", "frying", "bake", "baking",
                   "roast", "roasting", "grill", "grilling", "oven", "slow cooker", "air fryer",
                   "minutes", "start to finish", "how do i cook", "how to cook", "how long do i cook",
                   "how many days", "what can i make", "what can i eat", "what can i have",
                   "what to eat",
                   "what goes with", "goes with", "serve with", "side dish", "side for",
                   "what can i do with", "recipe", "recipes", "use up",
                   "using up", "idea", "ideas", "meal ideas", "dinner ideas", "how do i make",
                   "how to make", "how do i cook", "how to cook", "how long do i cook",
                   "how long to cook"),
          ask=("ok", "okay", "safe", "eat", "eat it", "still", "next day", "tomorrow", "fridge",
               "can i have", "have it", "have some", "can i still have", "can i eat it",
               "gone off", "go off", "went off", "smell", "smells", "smelly", "sour", "slimy",
               "days", "day", "how long", "keep", "keeps", "last", "lasts", "bin", "throw",
               "should i", "made it", "made on", "cooked it on", "been in", "sat in",
               "a week", "two weeks", "a month", "last week"),
          bias=2,
          guard=lambda understood: (_not_a_recipe_now(understood)
                                    and _not_a_fault_in_the_dish(understood))),
    entry("five-second-rule", (("floor", "ground", "carpet", "worktop", "pavement",
                                "five second rule", "five seconds rule", "5 second rule",
                                "five-second rule", "five second", "five seconds", "5 second"),
                               ("dropped", "drop", "fell", "fallen", "picked it up", "pick it up",
                                "blew on it", "kiss it better", "true", "real", "myth",
                                "a thing", "still ok", "safe", "eat it")),
          "The five-second rule is not real: bacteria stick the moment food touches the floor, "
          "and it is the wetness that decides how much, not the seconds. A dry biscuit or a piece "
          "of toast is a small risk - brush it off and use your judgement - but anything damp, "
          "sticky or eaten with your hands should go in the bin, and anything dropped outside or "
          "in a bathroom always should. If it did go down, it is a wait-and-see, not a hospital "
          "trip: a healthy stomach usually deals with it.",
          avoid=("phone", "screen", "keys", "won't turn on", "wont turn on", "signal",
                 "cracked", "dropped it", "dropped my phone", "dropped the", "dropped a",
                 "dropped out", "prices dropped", "temperature dropped", "how do i stop",
                 "my back", "my hip", "fell over", "fell down", "fell off the ladder",
                 "fell off my bike", "fell out of bed"),
          bias=3),
)

_ROOM_ODOUR = ("out of the house", "out of my house", "out of the flat", "out of my flat",
               "out of the kitchen", "out of the room", "house smells", "flat smells",
               "kitchen smells", "room smells", "smell wont go", "smells wont go",
               "wont go away", "lingering smell", "stinks in here")
for _item in ENTRIES:
    _item.avoid = _item.avoid + _ROOM_ODOUR


_SHELLFISH = ("mussels", "mussel", "oysters", "oyster", "clams", "clam", "cockles", "scallops",
              "shellfish", "lobster", "crab", "whelks", "razor clams")
_R_MONTHS = ("without an r", "without an 'r'", "without the letter r", "month with an r",
             "months with an r", "only in months", "in an r month", "no r in the month",
             "r in the month", "summer months", "in may", "in june", "in july", "in august",
             "in september", "spawning",
             "ok to eat", "okay to eat", "alright to eat")
ENTRIES = ENTRIES + (
    entry("shellfish-r-rule",
          (_SHELLFISH, _R_MONTHS),
          "The rule about only eating shellfish in months with an r is about the days before "
          "fridges: May to August are the warm months, when shellfish spoil fastest and when "
          "mussels spawn and go watery. It is not a law now - farmed mussels and rope-grown "
          "ones are sold all year and are safe - so buy from a fishmonger or a shop with a busy "
          "counter, keep them cold, and use the tests that actually tell you: a live mussel is "
          "shut, or shuts when you tap it, and one that stays open goes in the bin; cook them in "
          "a covered pan for 5 to 8 minutes and throw away any that are still shut afterwards. "
          "Eat them the day you buy them, and never eat them raw.",
          avoid=("pregnant", "pregnancy", "expecting", "baby", "toddler", "child", "weaning",
                 "recipe", "white wine", "garlic", "restaurant", "frozen", "freeze",
                 "how long do they keep", "dog", "cat",
                 "open", "opened", "unopened", "didnt open", "didn't open", "stays open",
                 "still alive", "alive", "dead", "gone off", "smell", "smells", "smelly",
                 "bad ones", "keep in the fridge", "fridge"),
          bias=4),
)

_LEAFY_GREENS = ("spinach", "baby spinach", "lettuce", "lettuce leaves", "little gem",
                 "kale", "curly kale", "salad leaves", "salad leaf", "bag of salad",
                 "salad bag", "rocket", "watercress", "cress", "chard", "spring greens",
                 "leafy greens", "bok choy", "pak choi", "collard greens", "cavolo nero",
                 "greens")

_LEAFY_SIGNS = ("yellow", "yellowed", "yellowing", "gone yellow", "going yellow",
                "turning yellow", "turned yellow", "gone a bit yellow", "slightly yellow",
                "gone slimy", "slimy", "slime", "brown", "browning", "gone brown",
                "turned brown", "black spots", "mushy", "gone soft",
                "yellow leaves", "yellow leaf", "yellowed leaves", "yellowing leaves",
                "brown leaves", "slimy leaves", "soggy", "soggy leaves",
                "use it", "eat it", "still use", "still eat")

_LEAFY_SHOWS = re.compile(
    r"\b(?:yellow\w*|brown\w*|black\w*|slimy|slime|mushy|sour\w*|smell\w*|smelly)\b", re.I)


def _the_leaf_shows_a_colour(understood):
    if not isinstance(understood, dict):
        return False
    return bool(_LEAFY_SHOWS.search(understood.get("clean") or understood.get("text") or ""))


_CABBAGES = ("cabbage", "white cabbage", "green cabbage", "red cabbage", "savoy",
             "savoy cabbage", "hispi", "pointed cabbage")

_CABBAGE_SIGNS = ("yellow", "yellowed", "yellowing", "gone yellow", "going yellow",
                  "turning yellow", "yellow leaves", "yellow leaf", "brown", "browning",
                  "gone brown", "limp", "wilting", "wilted", "soft", "outer leaves",
                  "slimy", "smelly")

ENTRIES = ENTRIES + (
    entry("leafy-greens-yellow",
          (_LEAFY_GREENS, _LEAFY_SIGNS),
          "Check for slime before you look at the colour: a yellow or floppy leaf is age rather "
          "than poison - light and time break the green down - so pick those out and use the "
          "rest. Slimy, sour-smelling or brown-and-soft leaves are not safe, and once one leaf "
          "is slimy the bag is best binned, because the slime is bacteria and rinsing does not "
          "take it off. Wilting on its own is only water loss, so 10 minutes in iced water brings "
          "the crunch back, and limp-but-dry leaves are perfect in a soup, a curry or a stir-fry. "
          "Keep the bag in the salad drawer with a piece of kitchen paper in it and eat it within "
          "3 to 5 days of opening.",
          avoid=("garden", "gardening", "allotment", "plot", "compost", "feed", "fertiliser",
                 "fertilizer", "blight", "grow", "growing", "grown", "plant", "plants",
                 "planting", "seed", "seeds", "seedlings", "sow", "sowing", "soil", "hydroponics",
                 "tomato", "courgette", "why are my leaves", "recipe", "recipes",
                 "how do i cook", "how to cook", "how long does", "how long do", "how long can i",
                 "keep", "keeps", "last", "lasts", "freeze", "frozen",
                 "revive", "reviving", "bring it back", "crisp", "crispness", "fresh again",
                 "use up", "using up", "what can i do with", "what can i make", "ideas",
                 "cook", "cooking", "cooked", "pan", "boil", "boiling", "steam",
                 "steaming", "wilt it", "wilted in a pan"),
          guard=_the_leaf_shows_a_colour,
          bias=2),
    entry("cabbage-yellow-outer-leaves",
          (_CABBAGES, _CABBAGE_SIGNS),
          "Yellow or brown outer leaves on a cabbage are just age: peel off the ones that have "
          "gone, trim the dried stem end, and the firm head inside is still good - a whole "
          "cabbage keeps a month or more in the fridge, and a cut half keeps a couple of weeks "
          "wrapped. The one to bin is a head that is slimy or sour-smelling right through, or "
          "soft all the way to the middle. If only the outside looks tired, it is a stir-fry or "
          "a soup rather than the bin.",
          avoid=("garden", "gardening", "allotment", "plot", "compost", "feed", "fertiliser",
                 "fertilizer", "blight", "grow", "growing", "grown", "plant", "plants",
                 "planting", "seed", "seeds", "seedlings", "sow", "sowing", "soil",
                 "flower", "flowers", "flowering", "bolted", "bolting", "recipe", "recipes",
                 "slaw", "coleslaw", "pickle", "pickling", "ferment", "sauerkraut",
                 "how long does", "how long do", "how long can i", "keep", "keeps", "last",
                 "lasts", "freeze", "frozen", "how do i cook", "how to cook", "roast"),
          bias=3),
)
