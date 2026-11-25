from .lookup import entry

ANSWERS = ("cooking", "food-and-drink")

TIME_ASK = frozenset(("how long", "minutes", "minute", "mins", "time", "long", "take", "takes",
                      "took", "quickest"))

PASTA_MINUTES = (
    (("thin spaghetti", "spaghettini", "angel hair", "linguine", "vermicelli", "capellini"),
     "8 to 9 minutes"),
    (("spaghetti", "penne", "fusilli", "macaroni", "farfalle", "bow", "bows"),
     "10 to 11 minutes"),
    (("rigatoni", "tagliatelle", "orecchiette", "cannelloni", "pappardelle", "conchiglie"),
     "11 to 13 minutes"),
    (("tortellini", "ravioli", "gnocchi", "tortelloni"), "3 to 4 minutes"),
)

NOODLES = ("Noodles are quick but not all the same: thin or instant ones are 3 to 4 minutes, egg "
           "noodles 4 to 5, and dried rice noodles 6 to 8, so check the packet for yours.")

SHAPES = tuple(shape for keys, _minutes in PASTA_MINUTES for shape in keys) + ("noodles", "noodle")

NOT_A_TIME = ("squash", "spaghetti squash", "butternut", "courgette", "zucchini", "pumpkin",
              "in the oven", "pasta bake", "baked pasta", "bake", "baked", "baking",
              "how many sheets", "how many lasagne", "how much", "portion", "portions", "per person", "fridge", "freezer",
              "keep", "keeps", "keeping", "leftover", "left over", "next day", "reheat",
              "last", "lasts", "lasting", "days", "day",
              "gone off", "sauce recipe", "salad", "sticking", "stuck", "clump", "clumps",
              "boil over", "boils over", "boiling over", "boiled over", "overflow", "overflows",
              "spill", "spills", "spilling", "spilled", "spilt")


PASTA_KINDS = (
    ("long strands", "spaghetti, linguine and tagliatelle",
     "a ragu, a carbonara or a butter sauce the strands can carry"),
    ("tubes", "penne and rigatoni",
     "a baked dish, and a thick sauce that fills the tube"),
    ("twists and shells", "fusilli, farfalle and conchiglie",
     "a sauce with bits in it that needs something to cling to, and pasta salad"),
    ("tiny shapes", "orzo and stelline", "soup, and a salad that should not be all bulk"),
    ("sheets", "lasagne", "a bake, layered instead of tossed"),
    ("filled", "ravioli and tortellini", "a meal on its own with butter or a light sauce"),
)

KINDS_ASK = ("kinds of pasta", "types of pasta", "sorts of pasta", "varieties of pasta",
             "kind of pasta", "type of pasta", "sort of pasta", "shapes of pasta",
             "shape of pasta", "what shapes", "which shapes", "what kinds", "what types",
             "different types", "different kinds", "how many types", "how many kinds")


def _the_kinds(memory=None, understood=None):
    members = ["%s (%s) for %s" % (family, shapes, for_what)
               for family, shapes, for_what in PASTA_KINDS]
    return ("Pasta comes down to six families, and the family decides the job: "
            + "; ".join(members[:-1])
            + " and " + members[-1] + ". The time goes by the shape as well: 8 to 9 minutes for "
            "thin strands, 10 to 11 for spaghetti and penne, 11 to 13 for rigatoni and "
            "tagliatelle, and 3 to 4 for the filled ones. Fresh pasta is 2 to 3 minutes, not the "
            "packet time.")


def _minutes(words):
    joined = " ".join(words)
    if "noodle" in joined or "noodles" in joined:
        return NOODLES
    for keys, minutes in PASTA_MINUTES:
        if any(key in joined for key in keys):
            return "About %s for that one." % minutes
    return "Dried pasta is 8 to 12 minutes, depending on the shape: 8 to 9 for thin spaghetti."


def _pasta_time(memory, understood):
    words = [str(word).lower() for word in (understood.get("words") or [])]
    if "fresh" in words:
        first = ("Fresh pasta is 2 to 3 minutes, not the packet time: it is done the moment it "
                 "floats and loses its chalky middle, so taste a strand at 2 minutes.")
    else:
        first = _minutes(words)
    return (first + " Use a big pan with about 10g of salt per litre, keep a mug of the water for "
            "the sauce, and taste a piece a minute before the packet says: shapes differ, and so "
            "do pans.")


PASTA_FOR_DISH = (
    (("ragu", "bolognese", "meat sauce", "slow cooked", "slow-cooked"),
     "Tagliatelle or pappardelle, or rigatoni",
     "a wide strand has the surface a thick meat sauce clings to, and a tube holds it; spaghetti "
     "is fine but most of the sauce ends up on the plate"),
    (("carbonara", "creamy sauce", "cream sauce", "cheese sauce", "macaroni cheese",
      "mac and cheese"),
     "Spaghetti or rigatoni",
     "the sauce is a coating rather than a filling, so a long strand or a tube both work, and "
     "the ridges on rigatoni hold it"),
    (("bake", "baked", "oven", "lasagne", "lasagna"),
     "Penne, rigatoni or lasagne sheets",
     "a tube keeps its shape through the oven and the sauce gets inside it, where a long strand "
     "turns to one lump"),
    (("soup", "broth", "minestrone"),
     "Orzo, stelline or any tiny shape",
     "small shapes cook in the broth and sit on the spoon, and orzo thickens it a little"),
    (("salad", "cold"),
     "Fusilli, farfalle or penne",
     "the nooks and the flat middles catch the dressing, and none of them clump when they are "
     "cold"),
    (("pesto",),
     "Trofie, fusilli or linguine",
     "trofie is the shape pesto comes from, and the others give it something to cling to"),
    (("seafood", "prawns", "prawn", "clams", "mussels"),
     "Linguine or spaghetti",
     "a long strand twines round the shellfish and the sauce stays light instead of collecting "
     "in a tube"),
)

DISH_WORDS = tuple(word for keys, _shapes, _why in PASTA_FOR_DISH for word in keys)

NOT_A_DISH = tuple(word for word in NOT_A_TIME if word not in DISH_WORDS)

_A_FAULT_IN_THE_DISH = ("watery", "soggy", "limp", "dry", "drier", "bland", "tasteless",
                        "mushy", "stodgy", "sticky", "gluey", "overcooked", "burnt",
                        "salty", "too salty", "undercooked", "stale")


def _for_the_dish(memory=None, understood=None):
    said = " ".join(str(word).lower() for word in (understood.get("words") or []))
    said = said or str(understood.get("clean") or "").lower()
    for keys, shapes, why in PASTA_FOR_DISH:
        if any(key in said for key in keys):
            return "%s, because %s." % (shapes, why)
    return ("Match the shape to the sauce rather than to the packet: a thick meat sauce wants a "
            "wide strand or a tube, a thin one wants a long strand, and a bake wants penne or "
            "rigatoni.")


ENTRIES = [
    entry("pasta-for-dish", (("pasta", "spaghetti", "penne", "fusilli", "rigatoni", "tagliatelle",
                              "linguine", "farfalle", "conchiglie", "ravioli", "tortellini",
                              "macaroni", "orzo", "trofie", "pappardelle"), tuple(DISH_WORDS)),
          _for_the_dish,
          avoid=NOT_A_DISH + _A_FAULT_IN_THE_DISH
          + ("how long", "how much", "per person", "portion", "portions",
                              "calories", "carbs", "instead", "substitute", "swap", "stand in",
                              "replace", "difference between", "how do i", "recipe", "recipes",
                              "how to make", "how do i make", "im making", "i am making",
                              "im cooking", "i am cooking"),
          bias=2),

    entry("pasta-kinds", (("pasta", "spaghetti", "penne", "fusilli", "rigatoni", "tagliatelle",
                           "linguine", "farfalle", "conchiglie", "ravioli", "tortellini",
                           "lasagne", "orzo", "macaroni"), tuple(KINDS_ASK)),
          _the_kinds,
          avoid=NOT_A_DISH + ("how long", "how much", "per person", "portion", "portions",
                              "gluten", "free", "vegan", "vegetarian", "calories", "carbs",
                              "instead", "substitute", "swap", "stand in", "replace",
                              "which one", "which is better", "difference between"),
          bias=1),

    entry("pasta-time", (("pasta", "spaghetti", "penne", "fusilli", "macaroni", "rigatoni",
                          "tagliatelle", "linguine", "farfalle", "orecchiette", "tortellini",
                          "ravioli", "gnocchi", "cannelloni", "noodles", "noodle"),
                         tuple(sorted(TIME_ASK))),
          _pasta_time,
          avoid=NOT_A_TIME,
          bias=2),

    entry("pasta-pan", (("pasta", "spaghetti", "penne", "fusilli", "macaroni", "rigatoni",
                         "tagliatelle", "linguine", "farfalle", "orecchiette", "tortellini",
                         "ravioli", "gnocchi", "cannelloni", "noodles", "noodle"),
                        ("pan", "pans", "pot", "pots", "saucepan", "saucepans", "wok",
                         "size", "big", "large", "wide", "deep", "enough room")),
          "A big pot with room to spare: about 5 litres of water for 500g of pasta, so it comes "
          "back to the boil quickly and the strands do not stick together. A wide shallow pan or "
          "a large frying pan is fine for long shapes if you stir, and easier for a small "
          "portion; any deep saucepan works for short shapes.",
          avoid=NOT_A_TIME + ("burnt", "burned", "non stick", "nonstick", "non-stick", "cast iron",
                              "coating", "season", "seasoning", "clean", "wash", "scour"),
          bias=1),

    entry("pasta-bake", (("pasta", "lasagne", "lasagna", "macaroni", "cannelloni", "pasta bake"),
                         ("in the oven", "oven", "bake", "baked", "baking", "pasta bake")),
          "Cook the pasta 2 minutes short of the packet, mix it with a sauce that is wetter than "
          "you think, top it and bake it 20 to 25 minutes at 200C (180C fan) until the top is "
          "browned and bubbling. Cover it with foil for the first 15 minutes and the middle stays "
          "loose instead of drying out.",
          avoid=("boil", "boiling", "water", "portion", "portions", "per person", "dry", "dried",
                 "leftover", "left over", "freeze", "reheat", "how many",
                 "im making", "i am making", "im cooking", "i am cooking", "im doing",
                 "i am doing", "im baking", "i am baking", "we are making", "we are cooking"),
          bias=1),

    entry("squash-roast", (("squash", "spaghetti squash", "butternut", "pumpkin", "acorn squash"),
                           ("roast", "roasted", "roasting", "oven", "bake", "baked", "cook",
                            "cooked", "cooking", "long", "time", "minutes")),
          "Halve it, scoop out the seeds and roast it cut side down at 200C for 35 to 40 minutes, "
          "until a knife goes into the flesh like butter; spaghetti squash wants 40 to 45, then "
          "fork it into strands. A whole one takes nearer an hour.",
          avoid=("blossom end", "rot", "growing", "grow", "seedling", "plant", "plot", "soil",
                 "court", "racket", "game", "player", "drink", "cordial", "juice", "sirop",
                 "seeds to sow", "variety"),
          bias=1),

    entry("pasta-soft", (("pasta", "spaghetti", "penne", "macaroni", "fusilli", "tagliatelle",
                          "rigatoni", "linguine", "noodles", "tortellini"),
                         ("mushy", "soggy", "overcooked", "over cooked", "too soft", "soft",
                          "slimy", "ruined", "sticky", "went wrong")),
          "Overcooked pasta has taken on water and lost its bite, so drain it now and stop the "
          "cooking under cold water. Toss it straight into a thick sauce - a ragu, a bake, or "
          "tomato with a spoon of cream cheese - rather than a thin one it cannot hold, and it "
          "will pass. Next time taste a piece a minute before the packet time.",
          avoid=("rice", "clump", "clumps", "together", "stuck", "sticking", "pan", "how long",
                 "minutes", "portion", "leftover", "sauce recipe", "in the oven", "bake"),
          bias=2),

    entry("drain-the-pot", (("drain", "drains", "draining", "drained", "strain", "strains",
                             "straining", "strained", "colander", "sieve"),
                            ("pasta", "spaghetti", "penne", "macaroni", "linguine", "fusilli",
                             "tagliatelle", "orzo", "noodles", "noodle",
                             "potato", "potatoes", "new potatoes", "veg", "vegetables",
                             "broccoli", "cauliflower", "carrots", "carrot", "greens", "peas",
                             "green beans", "spinach", "kale", "cabbage", "courgette",
                             "courgettes", "chickpeas", "lentils", "beans", "sweetcorn")),
          "Tip the whole pan into a colander in the sink, and keep a mugful of the water back "
          "first, because it is full of starch and it loosens a sauce that looks dry. Drain it "
          "the moment it is al dente or just tender - it keeps cooking in its own heat - then "
          "shake it dry and get it into the sauce or back into the warm pan, since anything left "
          "standing in a colander goes sticky within a couple of minutes. No colander is no "
          "problem: hold the lid on with a gap and pour slowly.",
          avoid=NOT_A_TIME + ("rinse", "rinsing", "washed", "wash", "fridge", "freezer",
                              "freeze", "leftover", "left over", "reheat", "rice", "sauce",
                              "bake", "oven", "salad", "cheese", "tin", "tinned"),
          bias=2),

    entry("lasagne-sheets", (("lasagne", "lasagna"),
                             ("sheets", "sheet", "pre cook", "precook", "pre cooked", "boil",
                              "soak", "how long", "cook", "cooking", "fresh", "dried")),
          "Fresh lasagne sheets need no cooking at all: layer them straight in. Dried sheets made "
          "without egg go in dry too, as long as the sauce is wet enough; dried egg pasta is "
          "better for 3 or 4 minutes in boiling water first. Either way rest the finished dish 10 "
          "minutes before cutting so it holds together.",
          avoid=("how long do i bake", "in the oven", "oven", "reheat", "freeze", "freezer",
                 "calories", "per person", "how many", "how much", "leftover", "left over",
                 "vegetarian", "vegan", "recipe", "keep", "keeps", "keeping", "fridge", "store",
                 "storage", "safe", "next day", "gone off"),
          bias=1),
]
