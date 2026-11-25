import re

from .lookup import DISH_ASK, entry

ANSWERS = ("cooking", "food-and-drink")


_ASKED_BEFORE = ("say", "said", "saying", "tell", "told", "remind", "remember", "mention",
                 "mentioned", "earlier")
_NOT_PRICE = ("price", "prices", "priced", "cost", "costs", "asking", "sell", "selling",
              "sold", "worth", "cheap", "expensive", "supermarket", "shop price")

CAFFEINE_MG = (
    (("instant", "nescafe", "granules"), "A mug of instant coffee is about 60 to 80mg"),
    (("decaf", "decaffeinated"), "Decaf is 2 to 5mg a mug, so almost none"),
    (("filter", "cafetiere", "french press", "percolator", "drip"),
     "A mug of filter coffee or cafetiere coffee is about 90 to 140mg"),
    (("espresso", "americano", "flat white", "latte", "cappuccino", "single shot"),
     "A single espresso is about 65mg, and a latte or americano made with one shot is the same"),
    (("green tea", "matcha"), "Green tea is about 25 to 40mg a mug"),
    (("black tea", "tea", "tea bag", "tea bags", "builder"), "A mug of black tea is about 50mg"),
    (("red bull", "energy drink", "energy drinks", "monster", "relentless"),
     "An energy drink is about 80mg a 250ml can, and the big 500ml cans are double that"),
    (("cola", "coke", "pepsi", "fizzy"), "A 330ml can of cola is about 35mg"),
)


def _caffeine_per_drink(memory, understood):
    said = " " + re.sub(r"[^a-z0-9% ]+", " ", str((understood or {}).get("clean") or "").lower()) + " "
    lead = ""
    for words, phrase in CAFFEINE_MG:
        for word in words:
            if " " + word + " " in said:
                lead = phrase
                break
        if lead:
            break
    rest = ("The usual daily limit for an adult is 400mg, which is about four instant coffees, "
            "and 200mg in pregnancy.")
    if not lead:
        return ("It varies with the drink: a mug of instant coffee is 60 to 80mg, filter coffee "
                "90 to 140mg, a single espresso about 65mg, black tea about 50mg, green tea 25 to "
                "40mg and a 330ml cola about 35mg. " + rest)
    return lead + ". " + rest


_BAKED_WITH_COFFEE = ("cake", "cakes", "bun", "buns", "bread", "loaf", "muffin", "muffins",
                      "biscuit", "biscuits", "scone", "scones", "brownie", "brownies",
                      "flapjack", "sponge", "sourdough", "dessert", "tart", "cheesecake",
                      "pudding", "tiramisu", "walnut cake", "coffee cake")

_COFFEE_CROWD = ("people", "crowd", "party", "batch", "litre", "litres", "jug", "flask", "urn",
                 "thermos", "guests", "everyone", "mugs")
_COFFEE_TIME = ("how long", "steep", "steeped", "press", "plunge", "minutes", "leave it",
                "how many minutes")

_COFFEE_RATIO = ("two level tablespoons of ground coffee per 200ml mug, which is about 12g, so "
                 "60g fills a litre jug and 240g makes 20 mugs")
_COFFEE_METHOD = ("in a cafetiere, pour water a minute off the boil, leave it three to four "
                  "minutes, then press and pour it all off the grounds, because coffee left "
                  "standing on them goes on brewing and turns bitter")


def _coffee_strength(memory, understood):
    said = " " + re.sub(r"[^a-z0-9% ]+", " ", str((understood or {}).get("clean") or "").lower()) + " "

    def says(words):
        return any(" " + word + " " in said for word in words)

    if says(_COFFEE_TIME):
        return ("In a cafetiere: pour water a minute off the boil, leave it three to four minutes, "
                "then press and pour it all off the grounds or it goes on brewing and turns "
                "bitter. That is " + _COFFEE_RATIO + ".")
    if says(_COFFEE_CROWD):
        return ("240g of ground coffee makes 20 mugs, each mug holding about two level tablespoons, "
                "12g, and 60g filling a litre jug. " + _COFFEE_METHOD.capitalize() +
                ". Go stronger for espresso, weaker with milk.")
    return ("Measure it by the mug: " + _COFFEE_RATIO + ". " + _COFFEE_METHOD.capitalize() +
            ". Stronger for espresso, weaker with milk.")


COUNT_IN_PACK = (
    (("spring onion", "spring onions", "scallion", "scallions"),
     ("bunch", "bunches"), "About 7 spring onions in a bunch", "a bunch is roughly 100g"),
    (("banana", "bananas"), ("bunch", "bunches"), "About 5 bananas in a bunch",
     "they are sold by weight and a bunch is 4 to 6"),
    (("clove", "cloves", "garlic"), ("bulb", "bulbs", "head", "heads", "garlic bulb"),
     "About 10 cloves in a bulb of garlic", "a bulb is 10 to 12, and a big one can be 15"),
    (("walnut", "walnuts", "walnut halves"), ("handful", "handfuls"),
     "About 7 walnut halves in a handful", "a handful is 20 to 25g"),
    (("almond", "almonds"), ("handful", "handfuls"), "About 20 to 25 almonds in a handful",
     "a handful is 30 to 35g"),
    (("rasher", "rashers", "bacon"), ("packet", "packets", "pack", "packs"),
     "About 7 or 8 rashers in a 250g packet of bacon", "the pack says the weight, not the count"),
    (("mushroom", "mushrooms"), ("punnet", "punnets", "pack", "packs", "box", "boxes"),
     "About 10 mushrooms in a 250g punnet", "a punnet is 250g, and a big one 400g"),
    (("strawberr", "strawberries"), ("punnet", "punnets"),
     "About 20 to 25 strawberries in a 400g punnet", "the count depends on the size"),
    (("tomato", "tomatoes"), ("punnet", "punnets", "vine", "vines", "pack", "packs"),
     "About 6 tomatoes in a 400g punnet", "and a vine is usually 5 or 6 on the truss"),
)

_COUNT_ASK = ("how many", "how many are", "many", "number of", "how much does", "how much do",
              "weigh", "weighs", "weight", "grams", "gram")
_COUNT_NOT_COUNTING = ("plant", "planting", "planted", "grow", "growing", "grew", "sow",
                       "sowing", "sow", "spacing", "apart", "deep", "when to", "best time",
                       "should i eat", "can i eat", "a day", "per day", "every day", "calories",
                       "carbs", "protein", "recipe", "cook", "cooked", "roast", "roasted",
                       "price", "prices", "cost", "costs", "buy", "buying", "cheap", "freeze",
                       "freezing", "keep", "keeping", "store", "storing")


def _count_in_a_pack(memory, understood):
    said = " " + re.sub(r"[^a-z0-9 ]+", " ", str((understood or {}).get("clean") or "").lower()) + " "
    if any((" " + word + " ") in said for word in _COUNT_NOT_COUNTING):
        return ""
    if not any(phrase in said for phrase in _COUNT_ASK):
        return ""
    for things, packs, count, note in COUNT_IN_PACK:
        if not any((" " + word + " ") in said or (" " + word) in said for word in packs):
            continue
        names = [word for word in things if word in said]
        if not names:
            continue
        return count + ": " + note + ", so buy by weight and use the count as a guide."
    return ""


AMOUNT_IN_A_DISH = (
    (("cake", "cakes", "sponge", "victoria sponge", "sandwich cake", "cake mix",
      "baking", "bake", "baking a cake"),
     {("eggs", "egg"):
      ("Three eggs for a 20cm sponge",
       "weigh them in their shells and use the same weight of soft butter, caster sugar and "
       "self-raising flour - about 175g of each for three medium eggs - so the cake always "
       "balances however big the eggs are"),
      ("butter",):
      ("About 175g of soft butter for a 20cm sponge",
       "the exact weight is the weight of three eggs in their shells, with the same of caster "
       "sugar and self-raising flour"),
      ("sugar", "caster sugar"):
      ("About 175g of caster sugar for a 20cm sponge",
       "weigh three eggs in their shells and use that weight of butter, sugar and self-raising "
       "flour, which is the whole of a victoria sponge",
       "A slice of a 20cm sponge has about 18g of sugar in it, and the whole cake has about "
       "175g, which is nobody's portion - it is the slice that matters"),
      ("flour",):
      ("About 175g of self-raising flour for a 20cm sponge",
       "weigh three eggs in their shells and use that weight of soft butter, caster sugar and "
       "flour; fold the flour in last and stop as soon as it is mixed"),
      ("milk",):
      ("A tablespoon or two of milk at the end, and only if the batter is stiff",
       "a sponge batter should drop slowly off the spoon, so loosen it a spoonful at a time")}),
    (("pancake", "pancakes", "batter", "crepe", "crepes"),
     {("milk",):
      ("About 600ml of milk to 200g of plain flour and 3 eggs, which makes about 16 thin "
       "pancakes",
       "for four people; a thicker batter for American-style pancakes is 300ml of milk to "
       "250g of self-raising flour and 2 eggs"),
      ("flour",):
      ("200g of plain flour for four people",
       "with 3 eggs and 600ml of milk, which makes about 16 thin pancakes; a family with small "
       "children is happy on 150g, and they take a minute a side in a hot pan"),
      ("sugar",):
      ("A teaspoon of sugar in the batter is plenty",
       "it helps them brown but does not make them sweet; the sweetness goes on at the table")}),
    (("bolognese", "bolagnese", "ragu", "spag bol", "spaghetti bolognese", "mince"),
     {("tomatoes", "tomato", "tins of tomatoes", "tin of tomatoes", "chopped tomatoes"):
      ("One 400g tin of chopped tomatoes to 500g of mince",
       "with a tablespoon of tomato puree and a good 40 minutes of simmering, which is what "
       "turns it from mince in tomato sauce into a ragu"),
      ("onions", "onion"):
      ("One onion to 500g of mince",
       "chopped small and softened first, with a carrot and a stick of celery if you have "
       "them"),
      ("garlic",):
      ("Two cloves of garlic to 500g of mince",
       "in with the onion at the end of its cooking so it does not burn")}),
    (("curry", "curries", "korma", "tikka", "masala", "balti", "dahl", "daal"),
     {("onions", "onion"):
      ("One large onion to 500g of meat or vegetables",
       "cooked slowly until it is properly golden before the spices go in, which is most of "
       "the flavour of a curry"),
      ("cream", "double cream"):
      ("About 100ml of cream for a curry for four",
       "stirred in at the end off the heat so it does not split; yogurt goes in the same way, a "
       "spoonful at a time"),
      ("tomatoes", "tomato", "tinned tomatoes", "chopped tomatoes"):
      ("One 400g tin of tomatoes for a curry for four",
       "or four fresh ones, and let it cook down until the oil separates before the meat or "
       "vegetables go back in")}),
    (("mash", "mashed potato", "mash potato", "mashed potatoes"),
     {("butter",):
      ("About 50g of butter per kilo of potatoes",
       "with 100ml of warm milk beat in at the end; warm milk and butter go in before the "
       "mashing, cold milk makes it gluey"),
      ("milk",):
      ("About 100ml of warm milk per kilo of potatoes",
       "with 50g of butter, both warmed first so the mash does not go cold and gluey"),
      ("salt",):
      ("A good pinch of salt in the water, and a little more once it is mashed",
       "salted water is the only chance the potato itself gets to be seasoned")}),
    (("meringue", "meringues", "pavlova", "meringue nests"),
     {("sugar", "caster sugar"):
      ("50g of caster sugar for each egg white",
       "added a spoonful at a time once the whites are at soft peaks, and the bowl and whisk "
       "completely free of grease or the whites will not hold"),
      ("eggs", "egg", "egg whites"):
      ("One egg white to 50g of caster sugar, so three whites take 150g",
       "and a pavlova wants the same mix with a teaspoon of cornflour and vinegar folded in")}),
    (("cup of tea", "a brew", "cuppa", "mug of tea"),
     {("sugar",):
      ("None unless you add it: a level teaspoon of sugar is about 4g, so two sugars is 8g and "
       "roughly 30 calories in the mug",
       "the tea bag itself has no sugar in it at all"),
     }),
    (("porridge", "porage", "oats", "oatmeal"),
     {("milk",):
      ("About 300ml of milk to 50g of oats for one bowl",
       "or half milk and half water, which is how most people like it; stir it as it comes to "
       "the boil or it catches on the pan"),
      ("oats", "oat"):
      ("50g of oats and 300ml of milk for one bowl",
       "a pinch of salt in it makes a real difference, and it takes about five minutes on the "
       "hob or three in the microwave, stirred halfway")}),
    (("gravy",),
     {("stock", "water"):
      ("About 300ml of stock for gravy for four",
       "with a tablespoon of flour cooked into the meat juices first; add the stock a little at "
       "a time and stir, or it goes lumpy")}),
)

_RECIPE_ASK = ("how much", "how many", "much", "many", "amount", "quantity")
_NOT_A_RECIPE = ("is in", "are in", "is there in", "are there in", "contains", "contain",
                 "how much is", "how much are", "price", "prices", "cost", "costs",
                 "calories", "calorie", "carbs", "protein", "per slice", "per portion",
                 "a day", "per day", "every day", "healthy", "healthier", "good for",
                 "bad for", "is it ok", "is it okay")
_PORTION = ("slice", "slices", "piece of", "portion", "serving", "per slice", "helping")
_ONLY_MADE = frozenset(("batter", "dough", "bolognese", "bolagnese", "ragu", "spag bol",
                        "spaghetti bolognese", "mince", "curry", "curries", "korma", "tikka",
                        "masala", "balti", "mash", "mashed potato", "mash potato",
                        "mashed potatoes", "meringue", "meringues", "pavlova",
                        "meringue nests", "gravy", "cup of tea", "cuppa", "mug of tea",
                        "porridge", "porage", "yorkshire pudding", "yorkshires"))


def _amount_in_a_dish(memory, understood):
    said = " " + re.sub(r"[^a-z0-9 ]+", " ", str((understood or {}).get("clean") or "").lower()) + " "
    if not any(phrase in said for phrase in _RECIPE_ASK):
        return ""
    for dish_words, amounts in AMOUNT_IN_A_DISH:
        named = [dish for dish in dish_words if (" " + dish + " ") in said]
        if not named:
            continue
        for ingredients, row in amounts.items():
            if not any((" " + word + " ") in said or (" " + word + "s ") in said
                       for word in ingredients):
                continue
            amount, note = row[0], row[1]
            as_eaten = row[2] if len(row) > 2 else ""
            if any(phrase in said for phrase in _PORTION):
                return ""
            if (any(phrase in said for phrase in _NOT_A_RECIPE)
                    and not any(dish in _ONLY_MADE for dish in named)
                    and not _cooking_words(said)):
                if not as_eaten:
                    return ""
                return as_eaten + ("" if as_eaten.endswith((".", "!", "?")) else ".")
            return amount + ". " + note[:1].upper() + note[1:] + "."
    return ""


_COOKING_WORDS = ("goes in", "go in", "put in", "add", "do i need", "should i use", "use",
                  "recipe", "make", "making", "mix", "batter", "dough", "cook", "cooking",
                  "for a", "for the", "for my", "to a", "into")


def _cooking_words(said):
    return any((" " + word + " ") in said for word in _COOKING_WORDS)



_DRESS_IS_A_GARMENT = re.compile(
    r"\b(?:a|an|the|my|her|his|our|their|this|that|these|those|your|another|one|two|any|some)"
    r"\s+(?:\w+\s+){0,3}dress(?:es)?\b"
    r"|\bsize\s+\d*\s*dress(?:es)?\b"
    r"|\b(?:wear|wears|wearing|wore|worn|buy|buys|bought|buying|make|makes|making|made|sew|"
    r"sews|sewing|sewn|alter|alters|altering|altered|return|returns|returning|returned|try|"
    r"tries|trying|tried|fit|fits|fitting|fitted|hem|hems|hemming|shorten|shortening|iron|"
    r"ironing|hang|hanging|pack|packing|choose|choosing|pick|picking)\s+(?:a|an|the|my|her|"
    r"his|this|that|your)?\s*(?:new\s+|old\s+|long\s+|short\s+|black\s+|white\s+|red\s+|"
    r"blue\s+|green\s+|pink\s+|navy\s+|floral\s+|silk\s+|linen\s+|lace\s+|summer\s+|"
    r"winter\s+|evening\s+|cocktail\s+|prom\s+|wedding\s+|bridesmaid\s+|christening\s+|"
    r"maxi\s+|midi\s+)?dress(?:es)?\b"
    r"|\bdress\s+(?:size|sizes|shop|shops|code|sense|hanger|hangers|pattern|patterns|fabric|"
    r"material|making|alterations?)\b"
    r"|\bdressmaking\b|\bwedding\s+dress\b|\bbridesmaid\s+dress(?:es)?\b", re.IGNORECASE)


def _a_dress_is_not_dressing(understood):
    said = str((understood or {}).get("clean") or "").lower()
    if not said:
        said = str((understood or {}).get("text") or "").lower()
    return not _DRESS_IS_A_GARMENT.search(said)


ENTRIES = [
    entry("caffeine-per-drink",
          (("caffeine", "mg of caffeine"),
           ("how much", "much", "many", "amount", "mg", "milligrams",
            "have caffeine", "has caffeine", "caffeine in", "contain caffeine",
            "contains caffeine", "any caffeine")),
          _caffeine_per_drink,
          ask=("how", "much", "many", "amount", "mg", "milligrams", "caffeine in",
               "have caffeine", "has caffeine", "contain caffeine", "contains caffeine",
               "any caffeine"),
          avoid=("safe", "limit", "too much", "pregnan", "day", "daily", "cut down", "cutting",
                 "give up", "quitting", "sleep", "sleeping", "bed", "energy", "tired",
                 "withdraw", "headache", "weak", "watery", "bitter", "sour", "taste", "tastes",
                 "tasting", "brew", "brewing", "strong", "stronger",
                 "child", "children", "kid", "kids", "son", "daughter", "toddler", "baby",
                 "year old", "years old", "teenager", "teenagers",
                 "breastfeed", "breast feed", "breast feeding", "breastfed", "nursing",
                 "nurse", "lactating", "chestfeed", "chest feed", "while feeding",
                 "still feeding")),
    entry("pinch", (("pinch", "pinches", "dash"),
                    ("how much", "what", "much", "salt", "spice", "recipe", "mean",
                     "grams", "gram", "weigh", "weighs", "weight")),
          "A pinch is what you can hold between your thumb and finger: about 1/16 of a "
          "teaspoon, a little under half a gram of salt, and a good pinch nearer one. A dash "
          "of liquid is about 1/8 of a teaspoon, and a handful is 30 to 40g.",
          ask=("how", "much", "many", "what", "big", "measure", "mean", "means", "size"),
          avoid=_ASKED_BEFORE),
    entry("splash", (("splash", "glug", "drizzle"),
                     ("how much", "what", "much", "milk", "oil", "sauce", "cream", "recipe")),
          "A splash is a loose tablespoon or two, and a drizzle a thin stream over the top: "
          "both are meant to be tasted and topped up, so start small.",
          ask=("how", "much", "many", "what", "mean", "means", "big"),
          avoid=_ASKED_BEFORE),
    entry("dressing-quantity",
          (("dressing", "vinaigrette", "salad dressing", "salad sauce"),
           ("how much", "how many", "much", "many", "for 2", "for 3", "for 4", "for 5", "for 6",
            "for 7", "for 8", "for ten", "for twelve", "people", "per person", "a head",
            "salad", "make", "need")),
          "About a tablespoon (15ml) a head, made at 3 parts oil to 1 of vinegar or lemon: 45ml of "
          "oil and 15ml of vinegar dresses four, 70ml and 25ml dresses six, plus a teaspoon of "
          "mustard and a pinch of salt either way. Put the dressing in the bottom of the bowl and "
          "toss the leaves on top of it rather than pouring it over.",
          ask=("how much", "how many", "much", "many", "per person", "per head", "a head",
               "each", "for 2", "for 3", "for 4", "for 5", "for 6", "for 7", "for 8",
               "for ten", "for twelve"),
          guard=_a_dress_is_not_dressing,
          avoid=_ASKED_BEFORE + _NOT_PRICE + ("wound", "wound dressing", "cut", "burn", "ulcer",
                                             "bandage", "surgical", "window dressing")),
    entry("knob", (("knob", "knobs", "dollop", "dollops", "squirt", "squirts", "gob",
                    "a slug of", "slug of", "slugs of", "a squirt of", "squirt of",
                    "a dollop of", "dollops of", "a knob of", "knobs of", "a gob of"),
                   ("how much", "how many", "what", "much", "butter", "cream", "size",
                    "mean", "means", "big", "recipe")),
          "A knob is about a tablespoon, 15g; a dollop is nearer two tablespoons. Both are meant "
          "to be judged by eye, since a walnut-sized lump is a knob and you can always add a "
          "little more.",
          ask=("how", "much", "many", "what", "mean", "means", "size", "big"),
          avoid=_ASKED_BEFORE + _NOT_PRICE),
    entry("spoonful", (("spoonful", "spoonfuls", "spoon", "spoons", "cupful", "cupfuls"),
                       ("how much", "how many", "what", "much", "size", "mean", "means",
                        "big", "recipe")),
          "A spoonful means a level tablespoon, 15ml unless the recipe says heaped; a cupful is "
          "250ml, filled level rather than heaped. Go by the recipe where it gives a weight.",
          ask=("how", "much", "many", "what", "mean", "means", "size", "big"),
          avoid=_ASKED_BEFORE + _NOT_PRICE + ("cupful of rice", "cup of rice", "cupful of flour",
                                             "cup of flour", "cupful of sugar", "cup of sugar")),
    entry("drop", (("a drop of", "drop of", "drops of", "a grating", "grating of",
                    "a scattering", "scattering of", "a sprinkling", "sprinkling of"),
                   ("how much", "how many", "what", "much", "size", "mean", "means", "big")),
          "A drop is the smallest amount you can taste, a grating is one pass over the fine side "
          "of the grater, and a scattering is a light pinch over the top: all three are to "
          "taste, so start small and add more.",
          ask=("how", "much", "many", "what", "mean", "means", "size", "big"),
          avoid=_ASKED_BEFORE + ("eye", "ear", "nose", "diffuser", "price", "asking", "rain",
                                 "hint", "temperature", "charge")),
    entry("bunch", (("bunch", "bunches", "sprig", "sprigs", "punnet"),
                    ("how much", "how many", "what", "much", "size", "mean", "means", "big",
                     "parsley", "thyme", "basil", "coriander", "mint", "dill", "rosemary")),
          "A bunch is whatever you can close one hand round at the stems; a sprig is a single "
          "small stem, and a punnet is the little basket soft fruit comes in. None of them is a "
          "weight, so go by eye, and add herbs a little at a time and taste as you go.",
          ask=("how", "much", "many", "what", "mean", "means", "size", "big"),
          avoid=_ASKED_BEFORE + _NOT_PRICE + DISH_ASK + (
              "buy", "banana", "bananas", "grape", "grapes",
              "flower", "flowers", "wedding", "bouquet", "bouquets")),
    entry("nip", (("a nip of", "nip of", "a swig of", "swig of", "a tot of", "tot of",
                   "a nip", "a tot", "a swig", "nip measure", "single measure"),
                  ("how much", "how many", "what", "much", "size", "mean", "means", "big",
                   "drink", "spirit", "spirits", "measure", "recipe", "pour")),
          "A nip or a tot is a 25ml measure, the small end of a pub single; a swig is a mouthful "
          "of whatever you are drinking and no measure at all. A shot in a recipe is usually 25 "
          "to 35ml, so measure it rather than free-pour.",
          ask=("how", "much", "many", "what", "mean", "means", "size", "big"),
          avoid=_ASKED_BEFORE + ("bite", "nip at", "nip out", "nip to", "nip in")),
    entry("coffee-strength", (("coffee", "grounds", "ground coffee", "espresso", "cafetiere",
                               "french press"),
                              ("cup", "cups", "mug", "mugs", "per cup", "tablespoons", "strong",
                               "cafetiere", "cafetieres", "french press", "jug", "strength",
                               "scoop", "scoops", "weak", "weaker", "stronger",
                               "people", "crowd", "party", "batch", "litre", "litres",
                               "press", "plunge", "steep", "long", "use", "used")),
          _coffee_strength,
          ask=("per", "tablespoon", "tablespoons", "scoop", "scoops", "strong", "stronger",
               "strength", "weak", "weaker", "cafetiere", "french press", "mug", "make",
               "making", "brew",
               "ratio", "grounds", "ground coffee",
               "how long", "how many people", "people", "crowd", "party", "litre", "litres",
               "batch", "press", "plunge", "steep", "use"),
          avoid=("machine", "machines", "pod", "pods", "capsule", "capsules", "grinder",
                 "clean", "cleaning", "descale", "descaler", "kettle", "buy", "best",
                 "cheapest", "gift", "shop", "too much", "a day", "per day", "daily", "limit",
                 "safe", "caffeine", "tea")),
    entry("coffee-taste", (("coffee", "ground coffee", "brew", "espresso", "americano"),
                           ("bitter", "sour", "taste", "tastes", "tasting", "burnt", "weak",
                            "watery", "strong", "stronger", "brew", "brewing", "grind",
                            "better", "improve")),
          "Coffee that tastes wrong is nearly always the brew, not the bean: water just off the "
          "boil (about 90 to 95C rather than boiling), a slightly coarser grind and less time in "
          "the water, so 3 to 4 minutes in a cafetiere or 25 to 30 seconds for espresso. Bitter "
          "means too hot, too fine or too long; sour or thin means the other way, with a finer "
          "grind and a little longer. A tiny pinch of salt in the cup takes the edge off a "
          "bitter pot.",
          ask=("how", "why", "what", "make", "makes", "making", "fix", "improve", "better",
               "taste", "tastes", "tasting", "bitter", "sour", "burnt", "brew", "brewing",
               "grind", "weak", "watery", "strong", "stronger"),
          avoid=_ASKED_BEFORE + _BAKED_WITH_COFFEE),
    entry("count-in-a-pack",
          (("bunch", "bunches", "punnet", "punnets", "packet", "packets", "handful", "handfuls",
            "bulb", "bulbs"),
           ("spring onion", "banana", "bananas", "clove", "cloves", "garlic", "walnut",
            "walnuts", "almond", "almonds", "rasher", "rashers", "bacon", "mushroom",
            "mushrooms", "strawberr", "strawberries", "tomato", "tomatoes")),
          _count_in_a_pack,
          bias=3,
          ask=("how many", "how many are", "many", "number of", "how much does", "how much do",
               "weigh", "weighs", "weight", "grams", "gram"),
          avoid=_ASKED_BEFORE + _NOT_PRICE + ("flower", "flowers", "wedding", "bouquet",
                                             "bouquets", "plant", "planting", "grow", "growing",
                                             "sow", "sowing", "apart", "spacing",
                                             "should i eat", "can i eat", "per day",
                                             "every day", "calories", "carbs", "protein")),
    entry("amount-in-a-dish",
          (("eggs", "egg", "milk", "butter", "cream", "onions", "onion", "sugar", "flour",
            "tomatoes", "tomato", "garlic", "salt", "oats", "stock", "caster sugar"),
           ("cake", "cakes", "sponge", "pancake", "pancakes", "batter", "bolognese", "ragu",
            "curry", "curries", "korma", "tikka", "masala", "mash", "mashed potato",
            "meringue", "meringues", "pavlova", "porridge", "gravy", "cup of tea", "cuppa",
            "mug of tea", "yorkshire pudding")),
          _amount_in_a_dish,
          bias=2,
          ask=("how much", "how many", "much", "many", "amount", "quantity", "per person",
               "do i need", "goes in", "go in", "put in"),
          avoid=_ASKED_BEFORE + _NOT_PRICE + ("how long", "how many minutes", "how many mins",
                                             "calories", "carbs", "protein", "how much is",
                                             "how much are", "weight", "how heavy")),
]
