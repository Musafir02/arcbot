import re

from .lookup import asks_where_a_shop_answers, entry

ANSWERS = ("shopping", "money")

TIME_ASK = ("when", "what month", "which month", "what time of year", "time of year",
            "best time", "best month", "cheapest time", "cheapest month", "right time",
            "good time", "good month", "month to buy", "time to buy", "when to buy", "what time",
            "black friday", "january",
            "january sales", "sell off", "price drop", "prices drop", "go down", "come down",
            "going down",
            "get the best deal", "get a better deal", "get a good deal", "get the cheapest",
            "get a cheaper")

TIME_ASK_SHAPE = tuple(re.compile(" " + re.escape(phrase) + "s? ") for phrase in TIME_ASK)

WHEN_ASKING = ("when is", "when are", "when was", "when's", "when should", "when shall",
               "when can", "when could", "when do ", "when does", "when did", "when will",
               "when would", "when to buy", "when to get", "when to sell", "when in the year",
               "when is the best", "when is a good", "when is the cheapest")

PRICE_ASK = ("sale", "sales", "cheapest", "cheaper", "cheap", "discount", "discounts", "deal",
             "deals", "half price")

WHEN_ASK = TIME_ASK + PRICE_ASK

PERIOD_NOUNS = ("month", "months", "week", "weeks", "weekend", "weekends", "summer", "winter",
                "spring", "autumn", "christmas", "easter", "season", "seasons", "year", "years")
PERIOD_PREPOSITION = ("in", "at", "over", "during", "for")
COMPARING = ("cheaper", "cheapest", "best", "deal", "deals", "discount", "discounts", "sale",
             "sales", "half price", "price drop", "prices drop")


def _a_period_beside_a_comparison(line):
    words = line.split()
    if not any(word in COMPARING for word in words) and not any(
            phrase in line for phrase in ("half price", "price drop", "prices drop")):
        return False
    for at, word in enumerate(words):
        if word not in PERIOD_NOUNS:
            continue
        if any(before in PERIOD_PREPOSITION for before in words[max(0, at - 3):at]):
            return True
    return False

NOT_THE_CALENDAR = (
    "replace", "replacing", "replacement", "change", "changes", "changing", "changed",
    "due for", "need a new", "need new",
    "insurance", "insure", "renew", "renews", "renewal", "renewals", "renewing", "policy",
    "policies", "premium", "premiums", "no claims", "auto renew", "auto-renew", "excess",
    "quote", "quotes", "cover", "covers", "mot", "tax", "service", "servicing",
    "last", "lasts", "lasting", "long does", "how often",
    "clean", "cleaning", "wash", "washing", "repair", "repairs",
    "warranty", "guarantee", "return", "refund",
    "delivery", "deliver", "install", "installation", "measure", "measuring", "size", "firm",
    "soft", "cheap one", "second hand", "secondhand", "used", "sell", "selling", "selling my",
    "start", "starts", "starting", "started", "wont start", "takes ages", "takes a while",
    "slow to", "stalls", "stalling", "cut out", "cuts out", "misfire", "flat", "leak", "leaks",
    "leaking", "noise", "noisy", "smell", "smells", "warning light", "dashboard",
    "rid of", "dispose", "tip", "recycle",
    "book the van", "book a van", "book the removals",
    "hire a van", "hire the van", "hiring a van", "hired a van", "van hire", "removals",
    "man with a van", "moving house", "moving flat",
    "run", "runs", "running", "put", "turn", "switch", "use", "switch on",
    "switching on", "leave it on", "left on",
    "cover", "covers", "topper", "protector", "sheet", "sheets", "battery", "batteries",
    "charger", "case", "spare", "part", "parts", "filter", "filters", "bulb", "bulbs",
    "contract", "sim", "sim only", "upgrade", "pay monthly", "accessory", "accessories",
    "seat", "seats", "car seat", "cot", "cots", "pram", "buggy", "highchair", "pushchair",
    "take down", "taken down", "taking it down", "put up", "put it up", "putting up", "decorate",
    "decorating", "trim the tree",
    "worth it", "worth the", "worth buying", "good deal", "real deal", "good price", "fair price",
    "good buy", "rip off", "rip-off", "ripoff", "overpriced", "too expensive",
    "service", "serviced", "servicing", "mot", "mot test", "mot due", "service interval",
    "servicing interval",
    "short this month", "short this week", "short till", "short until",
    "short of money", "short on money", "short of cash", "short on cash", "short of funds",
    "a bit short", "bit short", "money is short", "moneys short", "money's short",
    "money is a bit short", "money is tight", "money is a bit tight", "tight month",
    "running short", "running a bit short",
    "cook", "cooks", "cooking", "cooked", "roast", "roasting", "bake", "baking", "baked",
    "defrost", "defrosting", "thaw", "thawing", "preheat", "preheated", "simmer", "boil",
    "boiling", "season", "seasoning", "recipe", "chicken", "turkey", "joint of", "gas mark",
    "degrees", "temperature",
)


_HAS_FAILED = ("broken", "broke", "breaks", "breaking", "faulty", "fault", "stopped",
               "not working", "isnt working", "isn't working", "went wrong", "gone wrong",
               "goes wrong", "packed in", "conked out", "died", "dead", "wont start",
               "won't start", "wont spin", "won't spin", "leaking", "months old", "years old")

_BUY_THE_NEXT = ("when should i buy", "when to buy", "when should i get", "when to get",
                 "best time to buy", "when is the best time to buy", "when should i replace",
                 "time to buy a new", "when do i buy", "when can i buy", "when will i buy",
                 "cheapest time to buy")


def _line(understood):
    reading_ = understood or {}
    text = reading_.get("clean") or reading_.get("norm_text") or ""
    if not text and reading_.get("words"):
        text = " ".join(reading_["words"])
    return " " + str(text).lower() + " "


def _says_it(line, name):
    forms = {name, name + "s", name + "es"}
    if name.endswith("s"):
        forms.add(name[:-1])
    if any(re.search(r"(?<![a-z])" + re.escape(form) + r"(?![a-z])", line)
           for form in forms):
        return True
    if " " in name or len(name) < 6:
        return False
    for word in line.split():
        word = word.strip(".,!?;:'\"()")
        if len(word) >= 5 and _one_edit_apart(word, name):
            return True
    return False


def _one_edit_apart(typed, name):
    if abs(len(typed) - len(name)) > 1:
        return False
    if len(typed) == len(name):
        return sum(1 for a, b in zip(typed, name) if a != b) <= 1
    short, long_ = (typed, name) if len(typed) < len(name) else (name, typed)
    return any(long_[:i] + long_[i + 1:] == short for i in range(len(long_)))


def _asks_the_calendar(understood, own=()):
    line = _line(understood)
    if own and not any(_says_it(line, name) for name in own):
        return False
    for name in own:
        line = line.replace(" " + name + " ", " ")
        line = line.replace(" " + name + "s ", " ")
    ask = [phrase for phrase in TIME_ASK if phrase in line]
    compared_period = _a_period_beside_a_comparison(line)
    if not (any(shape.search(line) for shape in TIME_ASK_SHAPE) or compared_period):
        return False
    if ask and not [phrase for phrase in ask if phrase != "when"]:
        if not any(phrase in line for phrase in WHEN_ASKING):
            return False
    if (any(phrase in line for phrase in _HAS_FAILED)
            and not any(phrase in line for phrase in _BUY_THE_NEXT)):
        return False
    return not any(phrase in line for phrase in NOT_THE_CALENDAR)


def _avoid_for(own):
    return tuple(word for word in NOT_THE_CALENDAR
                 if not any(one.startswith(word) or word.startswith(one)
                            for name in own for one in name.split()))


def _whenbuy(reply, own):

    def answer(memory, understood):
        if not _asks_the_calendar(understood, own):
            return None
        return reply

    return answer


WHEN_TO_BUY = (
    (("mattress", "mattresses"),
     "The January sales and the Black Friday week are when mattresses are marked down, though most "
     "mattress prices are 'on sale' all year, so compare two or three on firmness rather than on "
     "the percentage off. Buy somewhere with a 60-night trial: ten minutes in a shop tells you "
     "little about how you will sleep."),
    (("sofa", "sofas", "settee", "settees", "couch", "couches", "armchair", "armchairs"),
     "Sofas are cheapest in the January sales and over bank holiday weekends, when the chains run "
     "20 to 30 per cent off. A made-to-order sofa takes six to twelve weeks, so for Christmas you "
     "want to order by early November - and check the delivery date in writing rather than the "
     "one on the website."),
    (("tv", "tvs", "television", "televisions", "telly"),
     "Televisions are cheapest on Black Friday and in the January sales, and again in February to "
     "April, when the year's new models arrive and last year's drop a few hundred pounds for the "
     "same panel. If you do not need this year's model, spring is the quiet bargain."),
    (("washing machine", "washing machines", "tumble dryer", "tumble dryers", "fridge",
      "fridge freezer", "freezer", "dishwasher", "oven"),
     "White goods are cheapest on Black Friday and in the January sales, and the January price on "
     "last year's model usually beats the Black Friday one. Measure the gap and the doorway "
     "before you buy, and check the energy rating: over ten years the running cost matters more "
     "than the purchase price."),
    (("laptop", "laptops", "computer", "computers", "tablet", "tablets"),
     "Laptops and tablets are cheapest on Black Friday, in the January sales, and in the "
     "back-to-school weeks of late August when the makers push student models. A machine whose "
     "replacement has just launched drops the most, so check whether a newer model is out."),
    (("phone", "phones", "mobile", "mobiles", "iphone", "smartphone", "smartphones"),
     "The cheapest month for last year's phone is the one after the new model lands, which is "
     "usually late September to November, and Black Friday adds a further cut. Buying outright "
     "and keeping it four years is nearly always cheaper than the annual upgrade."),
    (("car", "cars", "van", "vans", "motorbike", "motorbikes"),
     "A car is cheapest at the end of a month or a quarter, when a dealer is chasing a sales "
     "target and will move on price, and in the quiet weeks of August and late December. New "
     "plates in March and September make the previous plate's stock cheaper, and a pre-registered "
     "car saves the most of all - just check you are the first registered keeper."),
    (("coat", "coats", "winter coat", "winter coats", "jacket", "jackets", "winter boots",
      "wellingtons",
      "ski boots", "ski boot", "skiing", "ski", "snowboard", "snowboarding"),
     "Winter coats and boots are cheapest in the January sales and at the end of the season in "
     "February, when the shops clear the rails for spring. Buy then for next winter, and buy the "
     "best you can afford: a waterproof shell at the higher price outlasts three cheap ones."),
    (("summer clothes", "holiday clothes", "swimwear", "swimsuit", "sandals", "shorts", "sunglasses"),
     "Summer clothes, swimwear and sandals are cheapest in August and early September, when the "
     "shops clear them out for knitwear, so late summer is the moment for next year's holiday. "
     "Sizes go first, so go early in the clearance rather than at the end of it."),
    (("garden furniture", "barbecue", "barbecues", "bbq", "patio", "parasol", "sun lounger"),
     "Garden furniture and barbecues are cheapest at the end of August and in September, when the "
     "season ends and the garden ranges go on clearance - but the choice is picked over by then. "
     "Buy late for price, or in March for choice."),
    (("bike", "bikes", "bicycle", "bicycles"),
     "Bikes are cheapest in September and October as the season ends, and again when next year's "
     "models arrive and the old ones are cleared. A last-year model with the same frame is the "
     "bargain worth having."),
)

SALES_CALENDAR = (
    "The big retail sales are the January sales (from Boxing Day to the end of January), the "
    "Black Friday week at the end of November, the Easter and August bank holiday weekends, and "
    "the end-of-season clearances - summer things in August, winter things in January and "
    "February. January and Black Friday are the deepest cuts, and the item you want most is the "
    "one worth waiting for rather than buying on impulse at a weaker sale."
)


def _general_sales(memory, understood):
    if not _asks_the_calendar(understood):
        return None
    return SALES_CALENDAR


def _christmas(memory, understood):
    if not _asks_the_calendar(understood):
        return None
    line = _line(understood)
    doing = any(one in line for one in (" take ", " taken ", " taking ", " put ", " putting ",
                                        " pack ", " packing ", " throw ",
                                        " go up ", " goes up ", " going up ", " gone up ",
                                        " come down ", " comes down ", " coming down "))
    gone = any(one in line for one in (" down ", " up ", " away ", " out "))
    if doing and gone:
        return None
    tree = any(one in line for one in ("tree", "trees", "real tree", "fir"))
    lights = any(one in line for one in ("light", "lights", "fairy", "decorations", "baubles",
                                        "tinsel", "ornaments"))
    if tree and not lights:
        return ("Buy a real tree in mid-December, a week or two before Christmas: a tree cut in "
                "November drops its needles by the big day, so ask the grower when it was cut and "
                "keep it in water. Artificial trees are cheapest in the January sales, so buy the "
                "one you want now and store it.")
    if lights and not tree:
        return ("Christmas lights and decorations are cheapest in the first week of January, at 70 "
                "to 90 per cent off, so buy for next year on the 2nd or 3rd rather than in "
                "November, when the same set is full price.")
    return ("Buy a real tree in mid-December, a week or two before Christmas, from a grower who "
            "will tell you when it was cut; lights and decorations are cheapest in the first week "
            "of January, at 70 to 90 per cent off, for next year.")


ENTRIES = [
    entry("whenbuy-" + words[0].replace(" ", "-"), (words, WHEN_ASK), _whenbuy(reply, words),
          avoid=_avoid_for(words),
          guard=lambda understood: not asks_where_a_shop_answers(understood),
          bias=2)
    for words, reply in WHEN_TO_BUY
] + [
    entry("whenbuy-christmas", (("christmas tree", "christmas trees", "christmas decorations",
                                "christmas lights", "decorations", "fairy lights", "tinsel",
                                "baubles", "ornaments"), WHEN_ASK), _christmas,
          avoid=_avoid_for(("christmas tree", "christmas decorations")),
          guard=lambda understood: not asks_where_a_shop_answers(understood), bias=2),
    entry("whenbuy-sales-calendar",
          (("sale", "sales", "bargains", "discounts", "deals", "black friday", "january sales",
            "clearance", "reductions", "price cuts"),
           ("when", "what month", "which month", "when are", "time of year", "this year",
            "next month", "coming up")),
          _general_sales),
]
