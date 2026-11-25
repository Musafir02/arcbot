
import re

from .lookup import a_food_is_being_kept, entry, only_a_container

ANSWERS = ("home-and-diy", "shopping", "fitness")

GARMENT = ("coat", "coats", "jacket", "jackets", "jumper", "jumpers", "cardigan", "fleece",
           "hoodie", "blazer", "suit", "suits", "dress", "dresses", "shirt", "shirts", "trousers",
           "skirt", "scarf", "clothes", "clothing", "wardrobe", "outfit", "uniform", "costume",
           "gloves", "hat", "beanie", "bag", "backpack", "rucksack", "handbag", "luggage",
           "suitcase", "sleeping bag", "tent",
           "jeans", "jean", "denim", "tshirt", "t shirt", "teeshirt", "tee shirt", "t-shirts",
           "t shirts", "joggers", "sweatpants", "trackies", "track suit", "tracksuit",
           "pyjamas", "pajamas", "pj s", "pjs", "nightie", "nightdress", "dressing gown",
           "bathrobe", "robe", "slippers", "socks", "sock", "tights", "stockings", "bra",
           "bras", "underwear", "boxers", "knickers", "pants", "apron", "overalls", "scrubs",
           "tabard")

SMELL = ("smell", "smells", "smelly", "smelling", "stink", "stinks", "stinking", "stunk", "odour",
         "odor", "reek", "reeking", "whiff", "musty", "must", "damp", "fusty", "sweat", "BO",
         "smoke", "smoky", "bonfire", "campfire", "fire", "cigarette", "cigarettes", "smoking",
         "tobacco", "nicotine", "vape", "curry", "cooking", "garlic", "perfume", "aftershave",
         "vinegar", "bleach", "petrol", "diesel", "paint", "chemical", "mildew", "mouldy")

NOT_A_GARMENT = ("room", "rooms", "house", "home", "flat", "kitchen", "bedroom", "living room",
                 "hall", "hallway", "car", "van", "sofa", "settee", "couch", "curtain", "curtains",
                 "carpet", "rug", "rugs", "mattress", "bed", "bedding", "duvet", "pillow",
                 "pillows", "sheet", "sheets", "towel", "towels", "washing machine", "washer",
                 "dishwasher", "fridge", "freezer", "bin", "bins", "wheelie", "oven", "microwave",
                 "kettle", "drain", "sink", "toilet", "shower", "walls", "wall", "ceiling",
                 "paint", "furniture", "chair", "chairs", "table", "wardrobe", "wardrobe door",
                 "drawer", "cupboard", "books", "book", "microwave oven", "car seats", "hands",
                 "breath", "mouth", "feet", "shoes", "shoe", "trainers", "boots", "socks",
                 "wellies", "helmet", "washing-up", "dishcloth", "cloth", "sponge", "bin bag")

ASK = ("get rid of", "get out", "get the smell", "remove", "removing", "take away", "stop the "
       "smell", "smells of", "smells like", "smelling of", "stinks of", "stinks like",
       "how do i clean", "how do i wash", "how do i freshen", "freshen up", "air out", "air it",
       "how do i make it smell better", "how do i get it to stop smelling")

_GARMENT_THEN_FOOD = re.compile(
    r"\b(?:" + "|".join(GARMENT) + r")\s+(?:potato|potatoes|baked potato|jacket potato)\b")


SMELL_SAID = ("smell", "smells", "smelly", "smelling", "smelled", "stink", "stinks", "stinking",
              "stunk", "odour", "odor", "reek", "reeks", "reeking", "reeked", "whiff", "whiffs",
              "musty", "must", "damp", "fusty", "sweat", "sweaty", "bo", "smoky", "mildew",
              "mouldy", "moldy", "stale", "fumes", "fumey", "scented")
_ODOUR_SOURCE = ("curry", "cooking", "garlic", "perfume", "aftershave", "vinegar", "bleach",
                 "petrol", "diesel", "paint", "chemical", "fire", "smoke")


def _a_source_is_not_a_smell(understood):
    words = [str(one).lower() for one in ((understood or {}).get("words") or ())]
    text = " ".join(words)
    if not any(source in text for source in _ODOUR_SOURCE):
        return True
    return any(named in text for named in SMELL_SAID)


def _a_garment_is_not_a_food(understood):
    words = (understood or {}).get("words") or ()
    text = " ".join(str(one) for one in words).lower()
    if _GARMENT_THEN_FOOD.search(text):
        return False
    if a_food_is_being_kept(understood) and only_a_container(understood, GARMENT):
        return False
    return True


ENTRIES = [
entry("smoke-in-clothes",
      (GARMENT + ("hood", "collar", "sleeves", "lining", "wool", "woollen", "dry clean only"),
       ("smoke", "smoky", "bonfire", "campfire", "woodsmoke", "wood smoke", "cigarette",
        "cigarettes", "cigarette smoke", "fag smoke", "smoking", "tobacco", "nicotine", "vape",
        "vaping", "fire", "fire pit", "chiminea", "bbq", "barbecue", "pub", "stale")),
      "Air it before you wash it: hang it outside, or in a room with a window open, for a day, "
      "because most of the smell sits on the surface and blows off. Then wash it at whatever the "
      "label allows - 30C for a washable coat, 40C for a jumper - with half the usual detergent "
      "and no softener. If it cannot be washed, hang it in a steamy bathroom for twenty minutes and "
      "air it again, or put it in a bag with a saucer of bicarbonate of soda overnight. Don't spray "
      "perfume on it; that makes smoke plus scent, and it clings harder.",
      bias=4,
      ask=SMELL,
      avoid=NOT_A_GARMENT + ("stain", "stains", "stained", "staining", "marked", "yellowed",
                             "fire alarm", "smoke alarm", "fireplace", "chimney", "wood burner",
                             "smoking meat", "smoker", "how do i stop smoking", "quit smoking",
                             "give up smoking", "smoke point", "burnt", "burning")),

entry("gym-kit-smell",
      (("gym kit", "gym clothes", "gym gear", "workout clothes", "workout gear", "sports kit",
        "running kit", "running clothes", "running gear", "training kit", "cycling kit",
        "gym top", "sports bra", "leggings", "base layer", "lycra", "sports clothes",
        "exercise clothes", "kit",
        "shorts", "gym shorts", "running shorts", "cycling shorts", "gym tops", "running tops",
        "gym top", "running top", "vest", "jersey", "sports socks", "running socks"),
       ("smell", "smells", "smelly", "smelling", "stink", "stinks", "stinking", "sweat", "sweaty",
        "odour", "odor", "musty", "damp", "fusty", "washing", "washed", "wash", "clean",
        "bacteria", "after washing", "even after washing")),
      "Wash kit cool - 30C is enough - with a scoop of bicarbonate of soda or a sports wash, no "
      "fabric softener at all, and air dry it. The smell is bacteria in the synthetic fibres, not "
      "in the sweat: sweat itself has no smell, and a warm wash with softener leaves a film the "
      "bacteria live in, which is why kit can smell the moment it gets damp again. Get it out of "
      "the gym bag the same day and hang it to dry before it goes in the basket.",
      bias=4,
      ask=SMELL,
      avoid=NOT_A_GARMENT + ("dumbbell", "dumbbells", "kettlebell", "weights", "barbell",
                             "routine", "programme", "program", "plan", "workout plan", "to buy",
                             "buy", "which shoes", "trainers to buy", "body odour", "deodorant",
                             "antiperspirant", "hyperhidrosis", "chafing", "blister",
                             "runners knee", "injury",
                             "chlorine", "pool", "swimming pool", "swim",
                             "stairs", "stair", "landing", "hall", "hallway", "landings",
                             "room", "rooms", "ceiling", "ceilings", "wall", "walls",
                             "loft", "lofts", "attic", "garage", "shed", "sheds",
                             "cupboard", "cupboards", "wardrobe", "wardrobes")),

entry("smell-in-a-garment",
      (GARMENT,
       SMELL + ("washing", "washed", "dry clean", "dry cleaning", "freshen", "air it", "aired")),
      "Air it outside for a day first, then wash it if it can be washed - at the temperature on the "
      "label - with half the usual detergent and no softener, and dry it in the open air rather "
      "than on a radiator. "
      "Anything that cannot be washed - a wool coat, a blazer, a suit - goes in a steamy bathroom "
      "for twenty minutes, or in a bag with a saucer of bicarbonate of soda overnight, and then "
      "air. If it comes back after that, the smell is in what it is stored in, so wash the drawer "
      "or the wardrobe and let both dry out before the clothes go back.",
      bias=2,
      ask=SMELL,
      guard=lambda understood: (_a_garment_is_not_a_food(understood)
                                and _a_source_is_not_a_smell(understood)),
      avoid=NOT_A_GARMENT + ("sweat", "sweaty", "sweat smell", "smells of sweat", "smell of sweat",
                             "mould", "mouldy", "mold", "moldy", "mildew", "mildewy", "mildewed",
                             "spores", "black spots", "green spots",
                             "swimsuit", "swimming costume", "bikini", "wetsuit", "wetsuits",
                             "pool", "chlorine", "swimming", "swim",
                             "stain", "stains", "stained", "staining", "marks", "yellow marks",
                             "armpit", "armpits", "fabric softener", "conditioner", "scent",
                             "perfume to wear",
                             "which perfume", "smell nice", "make it smell nice", "air freshener",
                             "candle", "diffuser", "smoke", "smoky", "bonfire", "cigarette",
                             "gym kit", "gym clothes", "running kit",
                             "bag of", "bags of")),

entry("smell-in-a-garment-why",
      (GARMENT,
       SMELL + ("washing", "washed", "dry clean", "dry cleaning", "freshen", "air it", "aired")),
      "It is bacteria eating what the wash leaves behind - sweat, body oil and skin cells - and "
      "they are not all removed by a cool quick wash, which is why a garment can smell the moment "
      "it warms up again. Synthetics hold it worst: polyester and elastane are oil-loving, so the "
      "film of body oil stays on the fibre, while cotton and linen let it go. Softener and too "
      "much detergent make it worse by leaving their own coating for the bacteria to sit in. So "
      "wash at the hottest the label allows with the amount of powder for a dirty load, skip the "
      "softener, and dry it fast and in the open air; once the smell has set in a wash at 60 with "
      "half a cup of bicarbonate of soda usually shifts it.",
      bias=3,
      ask=("why", "how come", "what makes", "whats making", "what is making", "reason",
           "what causes", "what caused"),
      guard=lambda understood: (_a_garment_is_not_a_food(understood)
                                and _a_source_is_not_a_smell(understood)),
      avoid=NOT_A_GARMENT + ("sweat", "sweaty", "sweat smell", "smells of sweat",
                             "smell of sweat",
                             "damp", "damps", "musty", "mustiness", "damp smell", "smells damp",
                             "smell damp", "smells of damp", "smell of damp", "dank",
                             "mould", "mouldy", "mold", "moldy", "mildew", "mildewy", "mildewed",
                             "spores", "black spots", "green spots",
                             "swimsuit", "swimming costume", "bikini", "wetsuit", "wetsuits",
                             "pool", "chlorine", "swimming", "swim",
                             "stain", "stains", "stained", "staining", "marks", "yellow marks",
                             "armpit", "armpits", "fabric softener", "conditioner", "scent",
                             "perfume to wear",
                             "which perfume", "smell nice", "make it smell nice", "air freshener",
                             "candle", "diffuser", "smoke", "smoky", "bonfire", "cigarette",
                             "gym kit", "gym clothes", "running kit"),
      ),
]
