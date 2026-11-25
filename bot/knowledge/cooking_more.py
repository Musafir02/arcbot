import re

from .lookup import (asks_the_kinds, entry, find,
                     says_it_has_gone_off as _says_it_has_gone_off)

from .cooking import (
    CROWD,
    DAIRY,
    DISHES,
    FOOD_CLASSES,
    MEAL_IDEAS,
    MEAL_PHRASES,
    PANTRY,
    PET_WORDS,
    _INGREDIENT_WORDS,
    _SWAP_ASK,
    _a_brew_not_a_dinner,
    _crowd,
    _table_text,
    _excluded,
    _fold,
    _mentions,
    _occasion,
    _sides,
    side_for,
    dish,
    ingredients,
    meal,
    missing,
    negated_ingredients,
    pointed,
    pointed_at_a_food,
    without,
)

ENTRIES = []

A_SIDE_WITH_NO_DISH = (
    "Two of these three, and the plate balances itself: something starchy (new potatoes, rice, "
    "bread), a vegetable cooked hot and quick (greens with butter, roasted carrots, a sharp "
    "salad), and something cool or sharp to cut through it (yoghurt, pickles, a squeeze of "
    "lemon). So a roast takes potatoes and greens, anything in a sauce takes rice or bread and a "
    "salad, and a barbecue takes coleslaw and pickles.")


def _a_side_or_the_three_jobs(memory, understood):
    return (_sides(memory, understood) or side_for(memory, understood.get("clean") or "")
            or A_SIDE_WITH_NO_DISH)


ENTRIES.append(entry(
    "a-side-dish",
    (("side dish", "side dishes", "sides for", "sides to", "sides with", "a side for"),
     ("what", "which", "any", "idea", "ideas", "options", "suggest", "suggestion",
      "suggestions", "recommend", "recommendation", "give", "something", "serve", "make",
      "need", "want", "help", "pick", "choose")),
    _a_side_or_the_three_jobs,
    avoid=("side effect", "side effects", "pain", "pain in my side", "stitch", "left side",
           "right side", "whose side", "side of the road", "sleep on")))



COOKED_THROUGH_WORDS = (
    "know", "knowing", "tell", "check", "checking", "done", "cooked", "cooked through",
    "ready", "how can i tell", "how do i tell", "how do you tell", "when is it done",
    "when its done", "internal", "temperature", "temp", "thermometer",
)
NOT_A_DONENESS_QUESTION = (
    "how long", "minutes", "kg", "per 500g", "recipe", "oven temperature", "gas mark",
    "keep", "keeps", "keeping", "kept", "fridge", "freezer", "freeze", "frozen", "defrost",
    "thaw", "reheat", "left out", "overnight", "leftover", "leftovers", "left over", "already",
    "pregnant", "pregnancy", "baby", "babies", "toddler", "child", "children", "kids",
    "food poisoning", "sick", "ill", "off", "gone off", "fresh", "smell", "smells",
    "burnt", "burnt to", "overcooked", "dry", "tough", "rubbery", "recipe", "what can i make",
    "how do i cook", "how do you cook", "how to cook", "how do i bake", "how to bake",
    "how do i fry", "how to fry", "how do i roast", "how to roast", "how do i grill",
    "how to grill", "how should i cook", "best way to cook",
)

ENTRIES.append(entry(
    "fish-done", (("fish", "cod", "haddock", "hake", "pollock", "sea bass", "tilapia"),
                  COOKED_THROUGH_WORDS),
    "Fish is done when it flakes at its thickest point and has turned from glassy to opaque all "
    "the way through, and a thermometer in the thickest part reads about 60C. Cod or haddock loins "
    "take 10 to 12 minutes at 200C, and a thin fillet 6 to "
    "8. A fork should slide in with no resistance - if the middle still looks see-through, give "
    "it two more minutes rather than serving it early.",
    avoid=NOT_A_DONENESS_QUESTION))

ENTRIES.append(entry(
    "pork-done", (("pork", "pork chop", "pork chops", "chops", "loin", "gammon", "tenderloin"),
                  COOKED_THROUGH_WORDS),
    "Pork is done when the juices run clear where you pierce the thickest part and a thermometer "
    "reads 71C: a chop can keep the faintest blush of pink in the middle and still be safe, but "
    "not wet, jelly-like meat. A 2.5cm chop takes 4 minutes a side in a hot pan and 5 minutes "
    "resting, and a loin joint roasts 25 minutes per 500g at 200C (180C fan).",
    avoid=NOT_A_DONENESS_QUESTION))

ENTRIES.append(entry(
    "lamb-done", (("lamb", "leg of lamb", "lamb chops", "shoulder of lamb", "rack of lamb"),
                  COOKED_THROUGH_WORDS),
    "Lamb is done by temperature in the thickest part: 55C is pink, 60C is medium, 70C is well "
    "done, and it is juiciest if you take it out 5C under and rest it 10 minutes. A leg roasts 25 minutes per "
    "500g at 180C (160C fan) plus 25 minutes on top, and a chop takes 3 minutes a side for pink.",
    avoid=NOT_A_DONENESS_QUESTION))

ENTRIES.append(entry(
    "beef-done", (("beef", "rib of beef", "rib roast", "roast beef", "beef joint"),
                  COOKED_THROUGH_WORDS),
    "Roast beef is 50C rare, 55C medium rare, 60C medium and 70C well done inside, read in the "
    "thickest part; it climbs about 5C while it rests, so pull it out 5C under what you want and "
    "rest it 15 minutes before carving, and at 220C (200C fan) allow 12 minutes per 500g. A steak "
    "is a pan question, not a roast one.",
    avoid=NOT_A_DONENESS_QUESTION))

ENTRIES.append(entry(
    "turkey-done", (("turkey", "turkey crown"), COOKED_THROUGH_WORDS),
    "A turkey is done when the thickest part of the thigh reads 74C and the juices run clear, not "
    "pink, where you pierce it; the breast reads about 70C by then and carries on cooking as it "
    "rests. Without a thermometer, the leg should move freely in its socket and the skin pull "
    "away easily - then rest it 30 minutes under foil.",
    avoid=NOT_A_DONENESS_QUESTION))

ENTRIES.append(entry(
    "swap-dairy",
    (("dairy", "dairy free", "dairy-free", "no dairy", "milk free", "milk-free", "without dairy",
      "lactose", "lactose free", "lactose-free", "plant milk", "oat milk", "soya milk",
      "soy milk", "almond milk"),
     _SWAP_ASK + ("how do i make", "how to make", "how can i make", "what can i eat",
                  "cut out", "cutting out")),
    "Every dairy ingredient has a straight swap: unsweetened soya or oat milk in place of milk, "
    "one for one, olive oil or a dairy-free spread for butter, and soya yoghurt for yoghurt. "
    "Where a recipe wants buttermilk, put a tablespoon of lemon juice in 250ml of plant milk and "
    "leave it ten minutes. Soya is the one with as much protein as milk, so pancakes, porridge "
    "and coffee taste least different with it.",
    avoid=("formula", "baby", "babies", "newborn", "breastfeeding", "calcium", "cheese board",
           "how much calcium")))

FATTENING_WORDS = ("fattening", "make me fat", "makes me fat", "make you fat", "makes you fat",
                   "put on weight", "gain weight", "fatten", "too fattening", "fatten me")

ENTRIES.append(entry(
    "fattening-food",
    (("banana", "bananas", "potato", "potatoes", "bread", "pasta", "rice", "nuts", "cheese",
      "eggs", "egg", "avocado", "chocolate", "honey", "fruit", "oats", "porridge", "yoghurt",
      "yogurt", "olive oil", "butter", "milk", "smoothie", "smoothies", "juice"),
     FATTENING_WORDS),
    "No single food is fattening - what decides your weight is the total across the day, so a "
    "banana at about 100 calories is a snack, not a cause. The foods blamed most often are the "
    "ones that go down fast and leave you hungry: bread, pasta, rice and juice. Eat them with "
    "protein and vegetables, or in one sitting rather than all day, and they stop being a problem.",
    avoid=("lose weight", "losing weight", "weight loss", "how much should i weigh", "bmi",
           "diabetes", "diabetic", "keto", "fasting", "calories in", "how many calories",
           "allergy", "allergic", "intolerant", "pregnant", "toddler", "baby", "dog", "cat")))
ENTRIES.append(entry(
    "starter-name", (("sourdough", "starter", "sourdough starter", "levain"),
                     ("name", "named", "naming", "call it", "call him", "call her", "call my")),
    ("Bread people go straight for the pun - Doughlene, Clint Yeastwood, Bread Pitt, Jane Dough - "
     "and everyone who asks about it wants the joke, so any name with dough, yeast or rise in it "
     "works. The starter does not care, and saying the name out loud once a day is a good reminder "
     "to feed it."),
    ask=("should i name", "should we name", "should i call", "should we call",
         "what should i name", "what should i call", "what to name", "what could i name",
         "suggest", "ideas", "idea", "any name", "good name", "nice name", "name for my",
         "name my", "help me name", "help me pick", "recommend", "come up with",
         "think of a name", "how do i name", "rename", "what would you call"),
    avoid=("feed", "feeding", "not rising", "didnt rise", "died", "hooch", "grey", "mould",
           "mold", "smell", "start", "begin", "first", "day", "wifi", "band", "cat", "dog",
           "discard", "flour", "water ratio"),
    bias=1))
ENTRIES.append(entry(
    "pan-boil-over",
    (("pan", "pans", "pot", "pots", "saucepan", "water", "milk", "pasta", "rice", "soup",
      "sauce", "stock", "porridge", "oats", "stew", "custard"),
     ("boil over", "boils over", "boiling over", "boiled over", "overflow", "overflows",
      "spill", "spills", "spilling", "spilled", "spilt", "stop it", "keep it from")),
    "Turn the heat down so it is a steady simmer rather than a rolling boil, and leave the lid "
    "half on. A wooden spoon laid across the top of the pan breaks the bubbles before they reach "
    "the rim, and a splash of oil or a knob of butter in starchy water (pasta, rice) stops the "
    "foam building. Fill the pan no more than two thirds and stir once at the start. Milk and "
    "tomato sauces catch on the base and then spatter, so stir them and keep them low.",
    avoid=("recipe", "how long", "burnt", "stuck", "sticks", "soggy", "kettle", "boiler",
           "central heating", "radiator", "water tank", "egg", "eggs",
           "floor", "floors", "sofa", "carpet", "rug", "cushion",
           "highchair", "bib",
           "remote", "remote control", "phone", "mobile", "iphone", "keyboard", "laptop",
           "tablet", "ipad", "kindle", "earbuds", "headphones", "controller", "console",
           "camera", "speaker", "charger", "tv"),
    ask=("boil", "boils", "boiling", "boiled", "overflow", "spill", "spills", "spilling",
         "spilled", "spilt", "stop", "stops", "stopping", "keep", "keeps", "keeping",
         "prevent"),
    bias=2))

ENTRIES.append(entry(
    "cream-whip",
    (("cream", "double cream", "whipping cream", "single cream"),
     ("whip", "whipping", "whipped", "stiff", "peaks", "hand", "by hand", "overwhipped",
      "split", "grainy")),
    "Cold cream, a cold bowl and a big balloon whisk: whip in a steady circle, keeping the "
    "whisk under the surface so you beat air in rather than flick it over the side. Double "
    "cream takes 2 to 3 minutes by hand and stiffens just as the trails stop disappearing. "
    "Stop a moment before it looks ready, because it goes grainy fast; a splash of milk "
    "whisked in rescues one that has gone too far.",
    avoid=("ice cream", "sunburn", "eczema", "skin", "soup", "sauce", "coffee", "tea",
           "freeze", "frozen"),
    ask=("whip", "whipping", "whipped", "peaks", "stiff")))

ENTRIES.append(entry(
    "chicken-joint",
    (("chicken", "whole chicken", "bird"),
     ("joint", "jointing", "portion", "portions", "cut up", "butcher", "eight pieces",
      "legs", "thighs", "breast off")),
    "Take the legs off first: cut through the skin between leg and body, bend the leg back "
    "until the hip joint pops, then cut through the middle of the joint rather than through "
    "bone. Then take the wings off at the shoulder, and cut each breast away from the "
    "backbone, following the ridge with the knife tip. A sharp knife and a pair of kitchen "
    "scissors for the joints do most of the work, and the carcass goes in the pot for stock.",
    avoid=("raw", "undercooked", "pink", "defrost", "freeze", "worth", "buy", "cheapest",
           "welfare"),
    ask=("joint", "jointing", "cut up", "eight pieces", "portions")))

ENTRIES.append(entry(
    "cake-tin-line",
    (("cake tin", "cake tins", "muffin tin", "loaf tin", "sandwich tin", "tin", "muffins",
      "springform", "springform tin", "loose bottom tin"),
     ("grease", "greasing", "line", "lining", "parchment", "greaseproof", "stick", "sticking",
      "comes out", "release", "loosen", "flour", "floured", "dust", "dusting", "prepare",
      "preparing")),
    "Rub the tin with butter or a flavourless oil, then cut a circle of baking parchment for "
    "the base - a square folded into quarters and trimmed to the corner is the quick way - "
    "and grease that too. For muffins and small tins, grease every cup and dust with flour, "
    "or use paper cases. Run a thin knife round the edge the moment it comes out and leave "
    "the cake in the tin for 10 minutes before turning it out.",
    avoid=("roast", "roasting", "hob", "pan", "frying", "wok", "baking tray", "traybake",
           "bread", "loaf of bread", "fruit cake", "christmas cake", "rich fruit",
           "wedding cake", "simnel", "dark fruit", "bundt", "bundt tin",
           "dry", "dried out", "overcooked", "over-cooked", "crumbly", "flat", "didnt rise",
           "didn't rise", "sank", "soggy", "raw", "uncooked", "burnt", "burned"),
    ask=("grease", "greasing", "line", "lining", "parchment", "greaseproof", "stick",
         "sticking", "comes out", "release", "flour", "dust", "prepare", "should i",
         "do i need", "how do i")))

ENTRIES.append(entry(
    "grease-a-tin-or-pan",
    (("pan", "pans", "tin", "tins", "tray", "trays", "mould", "moulds", "ramekin", "ramekins",
      "cake tin", "loaf tin", "muffin tin", "baking tin", "baking tray", "roasting tin",
      "frying pan", "grill pan", "wok", "dish", "loaf"),
     ("grease", "greased", "greasing", "greaseproof", "parchment", "baking paper")),
    "Rub a thin film of butter or flavourless oil all round the inside with a piece of kitchen "
    "paper. A cake tin also wants a dusting of flour, tapped round and the extra tipped out, or "
    "a lining of baking parchment on the base; a pan or a roasting tin wants only the oil, "
    "wiped on while it is cold.",
    avoid=("clean", "cleaning", "wash", "washing", "scrub", "soak", "burnt", "stuck",
           "get off", "get the fat", "grease off", "remove", "degrease", "season",
           "how long", "oven temperature", "temperature", "recipe", "buy",
           "non stick", "non-stick", "scratched", "scratches", "scratches on", "safe",
           "unsafe", "replace", "coating", "flaking", "peeling", "still ok", "toxic"),
    bias=2,
    ask=("grease", "greasing", "non stick", "parchment")))

ENTRIES.append(entry(
    "frittata",
    (("frittata", "Spanish omelette", "spanish tortilla", "omelette for a crowd",
      "tortilla espanola", "tortilla española", "potato tortilla"),
     ("make", "how", "oven", "bake", "pan", "eggs", "filling", "how many eggs", "serve")),
    "Cook the vegetables or potato first in an ovenproof frying pan until soft, then pour over "
    "6 beaten eggs for a 20cm pan, seasoned and with a handful of cheese if you like. Keep it "
    "on a low heat for 3 to 4 minutes until the edges set, then finish it under the grill or "
    "in a 180C oven for 8 to 10 minutes until the middle is just set. It takes 6 eggs to feed "
    "four, and it is good cold the next day.",
    avoid=("frying pan", "non stick", "non-stick", "buy", "best", "pan set"),
    ask=("frittata", "spanish omelette", "spanish tortilla", "how many eggs",
         "tortilla espanola", "espanola", "espanol", "potato tortilla")))

_FLATBREAD_KINDS = (
    ("tortilla", ("tortilla", "tortillas", "wrap", "wraps", "fajita", "burrito")),
    ("chapati", ("chapati", "chapatis", "chapatti", "roti", "rotis")),
    ("pitta", ("pitta", "pitas", "pita", "pittas")),
)


def _flatbread_answer():
    def answer(memory, understood):
        said = " " + str(understood.get("clean") or "").lower() + " "
        if "spanish" in said or "espanola" in said or "espanol" in said or "omelette" in said:
            return None
        for name, words in _FLATBREAD_KINDS:
            if any(" " + word + " " in said or said.strip().endswith(" " + word)
                   for word in words):
                return _FLATBREAD_RECIPES[name]
        return _FLATBREAD_RECIPES["quick"]
    return answer


_FLATBREAD_RECIPES = {
    "tortilla": (
        "Plain flour, salt, a little oil or lard and warm water, nothing else: about 250g of "
        "flour to 150ml of warm water and a tablespoon of oil. Knead for two minutes, rest the "
        "dough under a bowl for 20, then roll each one out as thin as you can. Cook in a dry, very "
        "hot pan for about 30 seconds a side - they want speckles, not browning, or they go crisp "
        "instead of foldable. Press the bubble down with a spatula as it puffs and stack them under "
        "a tea towel."),
    "chapati": (
        "Wholemeal flour and water, no raising agent and no yoghurt: about 200g of wholemeal or "
        "atta to 120ml of warm water, a pinch of salt and a smear of oil. Knead for five minutes "
        "until smooth, rest 20 minutes, roll thin, then cook in a dry pan for a minute a side "
        "until it speckles. Hold it over a flame with tongs for a couple of seconds at the end and "
        "it puffs up."),
    "pitta": (
        "Pitta needs yeast, because the pocket is steam trapped inside the dough: 250g of strong "
        "white flour, 150ml of warm water, 5g of instant yeast, 5g of salt and a teaspoon of oil. "
        "Knead, prove an hour until doubled, then roll out about 1cm thick - too thin and there is "
        "no steam to open it. Bake on a tray as hot as the oven goes, 250C, for about five minutes, "
        "and they puff and hollow as they cool."),
    "quick": (
        "Self-raising flour, a pinch of salt and enough yoghurt or water to make a soft dough: "
        "about 250g of flour to 150g of yoghurt, kneaded for a minute and rested for 10. Roll them "
        "thin, then cook each one in a dry, very hot frying pan for a minute a side until it "
        "blisters and puffs. Keep them under a tea towel while you do the rest, and eat them the "
        "same day; they freeze well between sheets of paper."),
}


ENTRIES.append(entry(
    "flatbreads",
    (("flatbread", "flatbreads", "flat bread", "pitta", "pita", "tortilla wraps", "chapati",
      "naan", "tortilla", "tortillas", "corn tortilla", "flour tortilla"),
     ("make", "making", "recipe", "how", "dough", "pan", "quick", "no yeast", "no oven")),
    _flatbread_answer(),
    avoid=("pizza", "shop", "buy", "buying", "freezer aisle", "gluten", "sourdough",
           "bread maker", "breadmaker"),
    ask=("make", "making", "recipe", "dough", "pan", "quick", "no yeast", "no oven")))

ENTRIES.append(entry(
    "lunchbox-cold",
    (("lunchbox", "lunch box", "packed lunch", "lunch", "lunches", "sandwiches", "salad",
      "bento",
      "keep my food", "keep the food", "food cold", "food cool", "food at work"),
     ("cold", "cool", "cooler", "ice pack", "warm", "hot day", "stay fresh", "safe", "keep")),
    "Freeze a bottle of water or a small ice pack overnight and put it in the bag with the food, "
    "or freeze the sandwich fillings themselves (hummus, cooked chicken, cheese) and let them "
    "thaw by lunchtime. A bag with a lining holds the cold far better than a paper one, and the "
    "food wants to sit against the cold pack rather than next to it. Rice, cooked meat and "
    "dairy are the things to be strict about: over 5C for more than a couple of hours and they "
    "are not worth eating.",
    avoid=("school bag", "uniform", "homework", "kids won't", "refuse to eat", "soggy",
           "went soggy", "gone soggy", "going soggy", "dressing", "dressed", "wet",
           "food warm", "lunch warm", "keep it warm", "keep them warm", "stay warm",
           "still warm", "food hot", "lunch hot", "keep it hot", "hot lunch"),
    ask=("cold", "cool", "cooler", "ice pack", "warm", "hot day", "stay fresh", "safe", "keep")))

ENTRIES.append(entry(
    "lunchbox-hot",
    (("lunchbox", "lunch box", "packed lunch", "lunch", "lunches", "food", "soup", "stew",
      "curry", "leftovers", "flask", "thermos", "pie", "pasta", "rice"),
     ("warm", "hot", "still warm", "steaming")),
    "Fill a wide-mouth flask with boiling water for five minutes, empty it, then put the food in "
    "steaming hot and it will still be warm at lunchtime; a tea towel round the flask adds an "
    "hour or two. The middle ground is the risky bit, because food between 5C and 63C grows "
    "bacteria, so reheat it until it is steaming just before it goes in and throw away what is "
    "left at the end of the day.",
    avoid=("cold", "cool", "ice", "freezer", "fridge", "hot day", "hot weather", "sunburn",
           "chilli", "chili", "spicy", "hot sauce", "fever", "temperature", "oven", "bake",
           "baking", "roast", "raw", "defrost", "reheat"),
    ask=("warm", "hot", "still warm", "steaming")))


_APPLE_BROWN = (
    "Toss the cut pieces in lemon or lime juice, or dip them in lightly salted water for a minute "
    "and pat them dry, and press cling film right onto the cut faces. It is an enzyme in the flesh "
    "meeting the air, nothing to do with going off, so a browned apple is safe - cut the marks off "
    "and eat it.")

_WET_BROWN = (
    "Drop them into a bowl of cold water as you cut them, with a squeeze of lemon if you have one, "
    "and they will stay pale until they are cooked. It is an enzyme in the flesh meeting the air "
    "rather than spoilage, so browned potato or aubergine is safe - trim the marks and carry on.")

_DRY_BROWN = (
    "Keep the cut face covered with cling film or a drop of lemon juice until you cook it, and "
    "wipe rather than wash if it has to wait, as water makes it slimy. The brown marks are only "
    "air on the flesh, so a browned avocado is safe - cut them away and use the rest.")

_MUSHROOM_BROWN = (
    "A mushroom darkens as it ages, and that on its own is not spoiling - brush it rather than "
    "wash it, keep it in a paper bag in the fridge, and cook it soon. Slime, a sour or fishy smell "
    "or dark wet patches mean it has gone, so bin those.")

_MUSHROOM_SAFE = (
    "Look at the texture, not the colour: a mushroom is fine while it is firm and dry with a "
    "pleasant smell, brown cap or not. Slimy skin, a sour or fishy smell, or dark wet patches mean "
    "bin it, and cooked mushrooms left out for more than two hours go too.")

_CELERY_BROWN = (
    "Stand cut sticks in a jar of cold water in the fridge, or wrap them tight, and they keep their "
    "colour for a week. Brown edges are just air and water loss, so trim them off and the rest is "
    "fine.")

_PRODUCE_BROWN = (
    "It is an enzyme in the cut flesh meeting the air, so the fix is to keep the air off or make it "
    "acid: lemon juice, a bowl of cold salted water, or cling film pressed onto the cut face. Brown "
    "patches are not spoilage - trim them and eat the rest.")

_BROWN_SAFE_ASKS = re.compile(
    r"\bsafe\b|\bok\b|\bokay\b|\bstill good\b|\bcan i eat\b|\bcan you eat\b|"
    r"\bthrow (it|them|away)\b|\bstill fine\b", re.I)
_BROWN_SAFE = (
    "It is safe: browning is an enzyme in the cut flesh meeting the air, not spoilage, so trim the "
    "marks off and eat the rest. To stop it next time, keep the air off the cut face - lemon or "
    "lime juice, a bowl of cold salted water, or cling film pressed right onto it.")

_MUSHROOM_WORDS = re.compile(r"\bmushrooms?\b", re.I)

_BROWN_KINDS = (
    (("apple", "apples", "pear", "pears"), _APPLE_BROWN),
    (("potato", "potatoes", "aubergine", "aubergines", "eggplant", "parsnip", "parsnips",
      "artichoke", "artichokes", "salsify", "jerusalem artichoke"), _WET_BROWN),
    (("mushroom", "mushrooms", "chestnut mushrooms", "button mushrooms"), _MUSHROOM_BROWN),
    (("avocado", "avocados"), _DRY_BROWN),
    (("celery", "celeriac"), _CELERY_BROWN),
)


def _produce_brown(memory, understood):
    said = " " + str((understood or {}).get("clean") or "").lower() + " "
    mushrooms = _MUSHROOM_WORDS.search(said)
    if _BROWN_SAFE_ASKS.search(said):
        return _MUSHROOM_SAFE if mushrooms else _BROWN_SAFE
    if mushrooms:
        return _MUSHROOM_BROWN
    for names, reply in _BROWN_KINDS:
        if any(" " + name + " " in said for name in names):
            return reply
    return _PRODUCE_BROWN


ENTRIES.append(entry(
    "produce-brown",
    (("apple", "apples", "pear", "pears", "potato", "potatoes", "aubergine", "aubergines",
      "eggplant", "mushroom", "mushrooms", "celery", "parsnip", "parsnips", "artichoke",
      "artichokes", "fruit", "fruits"),
     ("brown", "browning", "going brown", "went brown", "gone brown", "gone black", "gone dark",
      "going black", "going grey", "going gray", "gone grey", "gone gray",
      "turns brown", "turn brown", "turning brown", "go black", "goes black", "went black",
      "go dark", "oxidise", "oxidize", "oxidation", "discolour", "discolor", "keeps browning",
      "stop them going brown")),
    _produce_brown,
    avoid=("tree", "trees", "plant", "plants", "garden", "growing", "grow", "leaf", "leaves",
           "soil", "basil", "lawn", "cook", "cooked", "cooking", "roast", "roasted", "fry",
           "fried", "frying", "sear", "seared", "maillard", "pan", "hot oven", "oven",
           "meat", "chicken", "beef", "bread", "toast", "ripen", "ripe", "ripening", "banana",
           "bananas", "chips", "crisps"),
    bias=2))

WAKE_WORDS = ("for the wake", "at the wake", "the wake", "funeral tea", "after the funeral",
              "funeral reception", "wake food", "wakes")
HOLD_WORDS = ("buffet", "party", "finger food", "sandwiches", "quiche", "sausage rolls",
              "plates", "dishes")
_HOT_HELD = re.compile(r"\bwarm\b|\bhot\b|\bheat\b|\bheating\b|\bstay hot\b", re.I)
_COLD_HELD = re.compile(r"\bcold\b|\bchill\b|\bfresh\b", re.I)
_AHEAD = re.compile(r"\badvance\b|\bahead\b|\bnight before\b|\bday before\b|"
                    r"\bmake ahead\b|\bprepare\b|\bprep\b", re.I)


_FOOD_IN_LINE = frozenset(PANTRY) | frozenset(_INGREDIENT_WORDS) | frozenset((
    "food", "foods", "meal", "meals", "dish", "dishes", "cook", "cooking", "eat", "eaten",
    "buffet", "sandwiches", "sandwich", "quiche", "sausage roll", "sausage rolls", "finger food",
    "nibbles", "canapes", "cake", "soup", "plates", "platter", "spread", "catering", "menu",
    "recipe", "recipes", "bake", "baked", "roast", "salad", "cheese", "crisps", "dips",
    "vegetarian", "vegan", "picnic", "barbecue", "bbq", "pudding", "dessert", "starter"))
_FOOD_JOB = re.compile(r"\b(?:warm|hot|cold|chill|fresh|safe|soggy|sitting out|sat out|"
                       r"left out|stand out)\b", re.I)
_OUR_OWN = re.compile(
    r"\b(?:im|i am|i'm|we are|we're|were|my|our|me and|my wife and i)\b[^.]{0,24}"
    r"\b(?:having|throwing|hosting|organis|organiz|putting on|holding|planning)\b"
    r"|\b(?:my|our|the) (?:party|barbecue|bbq|buffet|wake|christening|wedding) (?:food|spread)\b"
    r"|\bfor \d+ (?:people|guests|heads)\b|\bfor \w+ (?:people|guests)\b", re.I)


_A_PRONOUN_HELD = re.compile(
    r"\b(?:keep|keeps|keeping|kept|hold|holds|holding|stay|stays|staying|stand|stands|"
    r"standing|serve|serves|serving|served|leave|leaves|leaving|left|put|puts|putting)\s+"
    r"(?:[a-z']+\s+){0,2}(?:it|them|that|those|these|things|everything)\b[^.]{0,24}"
    r"\b(?:warm|hot|cold|chill|chilled|fresh|safe)\b", re.I)


def _about_the_food(understood):
    line = " " + " ".join(str(word) for word in (understood.get("words") or ())).lower() + " "
    words = set(re.findall(r"[a-z']+", line))
    if words & _FOOD_IN_LINE:
        return True
    if _OUR_OWN.search(line):
        return True
    if _A_PRONOUN_HELD.search(line):
        return True
    return bool(_FOOD_JOB.search(line)) and bool(
        re.search(r"\b(?:people|guests|heads|crowd|everyone)\b", line))


def _wake_food(memory, understood):
    return ("Food that needs no carving and no serving: sandwiches cut small, sausage rolls, a "
            "quiche, a pot of soup kept hot, cut cake, and plenty of tea. Make it the day before, "
            "allow three or four sandwich pieces a head, and ask two people to keep the teapot "
            "going and the plates moving, because that is the job nobody thinks to do.")


def _buffet_holding(memory, understood):
    line = " " + " ".join(str(word) for word in (understood.get("words") or ())).lower() + " "
    if _AHEAD.search(line):
        return ("Make sandwiches the night before, wrapped in the fridge, and leave the salad or "
                "tomato out until the morning because it turns the bread wet. Egg, cheese and ham "
                "fillings keep the best; nothing already filled should sit out for more than two "
                "hours.")
    if _COLD_HELD.search(line) and not _HOT_HELD.search(line):
        return ("Cold food wants to stay under 5C: keep the bowls in the fridge until people "
                "arrive, stand them in a bigger bowl of ice, and put out a little at a time. Rice, "
                "cooked meat and dairy are the things to be strict about, and anything out for "
                "more than two hours goes in the bin.")
    return ("Hot food wants to stay above 63C: a slow cooker on low, an oven on its lowest with the "
            "door ajar, or a lidded pan on a trivet, served in small batches so what is out gets "
            "eaten. Cold food wants to stay under 5C. Anything that has sat between the two for "
            "more than two hours is the food that makes people ill, so bin it.")


ENTRIES.append(entry(
    "wake-food",
    ((WAKE_WORDS),
     ("cook", "food", "make", "serve", "bring", "sandwiches", "tea", "catering", "buffet",
      "much", "how many", "feed", "after", "reception")),
    _wake_food, bias=2, guard=_about_the_food,
    avoid=("died", "death", "passed away", "grief", "grieving", "miss her", "miss him",
           "sympathy", "condolences", "what do i say", "what to say", "eulogy", "speech",
           "baby", "babies", "newborn", "newborns", "infant", "infants", "toddler", "toddlers",
           "my baby", "night feed", "night feeds", "waking for feeds", "weaning",
           "month old", "months old", "week old", "weeks old", "year old", "years old",
           "wake for a feed", "wakes for a feed", "wake for feeds")))

ENTRIES.append(entry(
    "buffet-holding",
    ((HOLD_WORDS),
     ("keep", "warm", "hot", "cold", "chill", "advance", "ahead", "night before", "day before",
      "make ahead", "prepare", "prep", "safe", "left out", "sit out", "stay fresh")),
    _buffet_holding, bias=2, guard=_about_the_food,
    avoid=("ideas", "idea", "suggest", "suggestions", "what can i make", "what should i make",
           "menu", "cheap", "recipe", "recipes", "how much food", "how many sandwiches",
           "how much do i need", "how many do i need",
           "soggy", "going soggy", "goes soggy", "went soggy", "gone soggy",
           "soggy bottom", "wet", "dressing", "dressed",
           "kids", "kid", "children", "child", "toddlers", "toddler", "games", "game", "play",
           "playing", "activities", "activity", "busy", "entertain", "bored", "occupy",
           "neighbour", "neighbours", "neighbor", "neighbors", "next door", "next-door",
           "upstairs", "downstairs", "flat above", "flat below", "loud music", "noise", "noisy",
           "keeps having", "keeps throwing", "every weekend", "all night", "all hours")))
STAPLES = frozenset("""garlic onion salt pepper oil butter flour milk stock lemon tomato
cheese bread""".split())

MEAT_NAMES = frozenset("chicken mince sausage bacon ham tuna salmon prawn".split())

GREEN_NAMES = frozenset("spinach pea broccoli courgette cabbage pepper".split())
GREEN_IN_TEXT = ("spinach", "peas", "pea ", "broccoli", "courgette", "cabbage", "kale",
                 "green bean", "mangetout", "greens")

LIMIT_WORDS = frozenset("""quick quickly fast rush rushed hurry quickish simple easy easier
cheaper cheap basic plain lighter light lightly""".split())
SIMPLE_PHRASES = ("nothing too fancy", "nothing fancy", "not too fancy", "nothing complicated",
                  "nothing too complicated", "no fuss", "keep it simple", "plain and simple",
                  "nothing special", "nothing flashy", "something plain", "plain food")
HEAT_WORDS = frozenset("""spicy spice spicier spicy-hot hotter hottest chilli chillies chili
chillis kick fiery heat""".split())
HEAT_IN_TEXT = ("chilli", "chili", "curry", "cajun", "paprika", "harissa", "hot sauce",
                "spice", "spiced", "curried", "spicy", "ginger", "cumin")
HEAT_INGREDIENTS = ("chilli", "chili", "chillies", "chillis", "cayenne", "paprika", "harissa",
                    "sriracha", "jalapeno", "tabasco", "chilli powder", "curry powder",
                    "hot sauce", "chilli flakes", "chilli sauce", "cajun")
_TASTE_RULED_OUT = re.compile(
    r"\b(?:wont|won't|wouldnt|wouldn't|doesnt|doesn't|dont|don't|didnt|didn't|never|no|"
    r"hates?|hated|dislikes?|disliked|refuses?|refused|not)\b"
    r"(?:\s+(?:eat|eats|eating|to|anything|something|food|foods|stuff|things|thing|meals?|"
    r"dishes|very|too|much|that|this|these|those|so|really|any|all|of|or|and|the|a|an|it|"
    r"them|sort|kind|hot|fan|keen|into|like|likes|at))*"
    r"\s+(?:spicy|spiced|spicier|spice|chilli|chili|chillies|chillis|curry|curried|fiery)\b")
_HOT_FOOD_RULED_OUT = re.compile(
    r"\b(?:wont|won't|wouldnt|wouldn't|doesnt|doesn't|dont|don't|didnt|didn't|never|"
    r"hates?|hated|dislikes?|refuses?|refused)\b"
    r"(?:\s+(?:eat|eats|eating|anything|something|very|too|much|that|so|really|any))*"
    r"\s+hot\s+(?:food|foods|stuff|things|sauce|curry|dishes?)\b")
VEG_WORDS = frozenset("vegetarian vegan veggie meatless".split())
MEAT_FREE_PHRASES = ("no meat", "without meat", "not eat meat", "doesnt eat meat",
                     "doesn't eat meat", "dont eat meat", "don't eat meat", "off meat",
                     "no fish", "no chicken")
DAIRY_FREE_PHRASES = ("no dairy", "dairy free", "dairy-free", "without dairy", "milk free",
                      "milk-free", "no milk products", "off dairy", "lactose free",
                      "lactose-free")
DAIRY_FOODS = tuple(name for name, kinds in FOOD_CLASSES.items() if "dairy" in kinds)
COMING_FOR = ("for dinner", "for tea", "for supper", "for lunch", "coming for", "coming over",
              "coming round", "coming to", "round for", "over for", "having people",
              "having friends", "having guests", "to cook for", "cooking for")
EVENT_WORDS = frozenset("""guests guest party parties buffet crowd birthday anniversary
celebrate celebration""".split())
MENU_PHRASES = ("no idea what to cook", "what to cook", "what should i cook", "what to make",
                "what shall i cook", "cook for", "cooking for", "make for")
BIG_DAYS = frozenset("""christmas xmas thanksgiving easter hanukkah diwali ramadan eid""".split())
COOKING_FOR = ("having a", "having some", "im making", "i'm making", "were making", "we're making",
               "im cooking", "i'm cooking", "for a", "for the", "for my", "party food", "buffet",
               "celebrat", "hosting", "come over", "coming over")
PEOPLE_WORDS = frozenset("""mum mom dad family friends visitors mother father parents sister
brother inlaws in-laws boyfriend girlfriend""".split())
CROWD_PHRASE = re.compile(
    r"\b(?:people|friends|family|guests?|company)\s+(?:coming\s+)?over\b"
    r"|\b(?:for|feeding|there are|there's|theres|we are|we're)\s+"
    r"(?:\d+|three|four|five|six|seven|eight|nine|ten|eleven|twelve|fourteen|fifteen|twenty|"
    r"thirty|a dozen)\b|\b\d+\s+of\s+us\b")
DISLIKE_WORDS = frozenset("""hate hates hated dont don't doesnt doesn't wont won't wouldnt
wouldn't dislike dislikes picky refuse refuses""".split())
SOMEONE_ELSE = re.compile(
    r"\b(?:my|his|her|our|their|the|one)\s+(?:daughter|son|kid|kids|child|children|boy|girl|"
    r"teenager|husband|wife|partner|mum|mom|dad|father|mother|brother|sister|friend|friends|"
    r"nan|gran|granny|grandma|grandad|grandpa|guest|guests|inlaws|in-laws|other half|"
    r"mother in law|father in law)\b"
    r"|\b(?:he|she|they)\s+(?:wont|won't|doesnt|doesn't|refuses|hates|dislikes|isnt|isn't)\b")


def _about_someone_else(understood):
    return bool(SOMEONE_ELSE.search(_clean(understood)))
GREEN_WORDS = frozenset("green greens".split())

PLAN_LAPSE = 2
MINUTES = {
    "potato-egg-hash": 15, "courgette-mushroom-pasta": 20, "chicken-spinach-cream": 20,
    "frittata": 20, "egg-fried-rice": 10, "cheese-omelette": 8, "mushroom-omelette": 10,
    "courgette-frittata": 20, "ham-omelette": 8, "tomato-pasta": 15, "tuna-pasta": 15,
    "courgette-pasta": 15, "mushroom-pasta": 15, "bacon-pasta": 15, "mac-cheese": 20,
    "pea-pasta": 12, "garlic-spaghetti": 10, "chicken-rice": 30, "leftover-chicken-rice": 10,
    "chicken-potato-tray": 45, "chickpea-curry": 20, "chickpea-spinach": 15, "lentil-soup": 30,
    "dhal": 25, "sausage-potato": 40, "sausage-bean": 30, "bolognese": 35, "cottage-pie": 50,
    "mince-pasta": 25, "salmon-potato": 40, "prawn-pasta": 15, "tuna-potato": 20,
    "bean-quesadilla": 5, "cheese-quesadilla": 5, "toastie": 5, "eggy-bread": 5,
    "pancakes": 20, "shortbread": 30, "banana-pancakes": 10, "banana-smoothie": 2,
    "porridge": 5, "overnight-oats": 480, "apple-crumble": 45, "veg-soup": 30,
    "veg-stirfry": 10, "cheesy-mash": 20, "mince-onion": 25, "onion-omelette": 12,
    "fried-potato-onion": 20, "chicken-onion-curry": 35, "loaded-jacket": 30, "shakshuka": 25,
    "spinach-pasta": 15, "bean-tomato": 20, "tuna-rice": 10, "prawn-rice": 15,
    "lemon-chicken": 45, "mash-cheese": 10, "scrambled-eggs": 5, "mushroom-cream": 10,
}

PANTRY_MINUTES = {
    "egg": 5, "pasta": 10, "rice": 10, "potato": 50, "chicken": 40, "mince": 25, "sausage": 25,
    "bacon": 15, "ham": 5, "tuna": 15, "salmon": 15, "prawn": 10, "chickpea": 30, "bean": 5,
    "lentil": 25, "cheese": 5, "tomato": 15, "onion": 25, "garlic": 5, "mushroom": 10,
    "spinach": 5, "courgette": 15, "pepper": 10, "carrot": 25, "broccoli": 15, "cabbage": 10,
    "pea": 15, "sweetcorn": 10, "bread": 5, "tortilla": 5, "flour": 25, "milk": 10, "cream": 10,
    "butter": 30, "yoghurt": 2, "lemon": 5, "banana": 10, "apple": 15, "oats": 5,
}

CROWD_DISHES = frozenset(("bolognese", "cottage-pie", "chicken-potato-tray", "chickpea-curry", "dhal",
                   "sausage-bean", "veg-soup", "mac-cheese", "salmon-potato", "lemon-chicken",
                   "apple-crumble", "frittata"))

FOR_ONE = frozenset(("frittata", "courgette-frittata", "cheese-omelette", "mushroom-omelette",
                     "onion-omelette", "ham-omelette", "toastie", "scrambled-eggs",
                     "egg-fried-rice", "bean-quesadilla", "cheese-quesadilla", "eggy-bread",
                     "banana-pancakes", "pancakes", "porridge", "overnight-oats"))

THIN = frozenset(("veg-soup", "lentil-soup"))

SWEET_WORDS = frozenset("pudding puddings dessert desserts afters sweet-tooth".split())
SWEET_PHRASES = ("something sweet", "something warm for after", "something for after", "for after",
                 "to follow", "after that", "sweet course", "for pudding", "for dessert",
                 "for afters")
SWEET_DISHES = frozenset(("apple-crumble", "pancakes", "shortbread", "banana-pancakes",
                          "banana-smoothie", "porridge", "overnight-oats"))
DINNER_WORDS = frozenset("""dinner tea supper lunch brunch meal meals food cook cooking make made
tonight eat eating""".split())
CHATTER = frozenset("""thanks thank ok okay lol haha yes yeah no nope sure great nice cool
hi hello bye morning night fine""".split())
TECHNIQUE_WORDS = frozenset("""time timing temperature oven degrees gas grill boil boiling roast
roasting fry frying bake baking rest resting cover covered lid stir seasoning""".split())
BAKING_WORDS = frozenset("""cake cakes bake baking baked sponge icing buttercream biscuit
biscuits cookie cookies muffin muffins cupcake cupcakes scone scones pastry loaf bread brownie
brownies tart drizzle frosting""".split())
DISH_WORDS = frozenset("""curry curries pasta soup soups pie pies stew roast salad sandwich
sandwiches risotto casserole burger pizza traybake omelette frittata macaroni lasagne""".split())
MEAL_FRAME = frozenset("""dinner tea supper lunch brunch meal meals food cook cooking cooked eat
 eating tonight make pudding dessert
 something anything""".split())
SAID_PHRASES = ("what did i say", "what did i tell", "did i tell you", "what did you say",
                "remind me what", "what have i said", "did i say")
PLAN_KEYS = ("have", "avoid", "limit", "veg", "vegan", "occasion", "simple", "no_green",
             "sweet", "crowd", "heat", "no_heat")
AVOID_TEXT = {"cheese": ("cheese", "parmesan", "cheddar", "mozzarella", "feta", "halloumi",
                         "pecorino", "gruyere", "blue cheese"),
              "dairy": tuple(sorted(DAIRY)),
              "milk": ("milk", "cream", "butter", "yoghurt", "yogurt", "creme fraiche"),
              "butter": ("butter",), "egg": ("egg", "eggs"),
              "meat": tuple(sorted(MEAT_NAMES)),
              "fish": ("fish", "tuna", "salmon", "prawn", "anchovy", "cod")}
VEGAN_BAD = ("cheese", "parmesan", "cheddar", "mozzarella", "feta", "halloumi", "milk",
             "cream", "butter", "yoghurt", "yogurt", "egg", "eggs", "honey", "creme fraiche")
PERSON_WORDS = frozenset("""she he her his him they their them son daughter boy girl child
children kid kids toddler baby mum mom mummy daddy husband wife partner friend nan nana grandma
granny grandad niece nephew""".split())
TASTE_WORDS = frozenset("""likes like loves love hates hate hated prefers prefer adores adore
favourite favorite keen fussy refuses refused""".split())
SWAP_PHRASES = ("instead", "substitute", "stand in", "replace", "swap")
METHOD_PHRASES = ("how do i", "how do you", "how should i", "how long", "how much",
                  "what temperature", "how to")


NEW_MEAL_PHRASES = ("what can i cook", "what can i make", "what should i cook",
                    "what should i make", "what can i do with", "meal ideas", "dinner ideas",
                    "any ideas", "what shall i cook")
_GROWING_WORD = frozenset("""plant plants planted planting seedling seedlings seed seeds
    tree trees bush bushes shrub shrubs crop crops allotment allotments garden greenhouse
    growing grow grows grown sow sowed sowing""".split())


def _a_crop_not_a_larder(understood):
    words = set(_said_words(understood))
    if not words & _GROWING_WORD:
        return False
    if _meal_asked(understood):
        return False
    return True


STOCK_PHRASES = ("have", "has", "got", "there is", "theres", "there are", "left over",
                 "leftover", "in the fridge", "in the freezer", "in the cupboard",
                 "in the pantry", "in the house", "in my kitchen", "at home")


def _clean(understood):
    return str((understood or {}).get("clean") or "").lower()


def _said_words(understood):
    words = (understood or {}).get("words") or ()
    return [_fold(word) for word in words]


def minutes_said(understood):
    text = " " + _clean(understood) + " "
    for pattern, unit in ((r"(\d+)\s*(?:mins|min|minutes|minute)\b", 1),
                          (r"(\d+)\s*(?:hrs|hr|hours|hour)\b", 60),
                          (r"(\d+)\s*and\s*a\s*half\s*(?:hours|hour|hrs|hr)\b", 90)):
        found = re.search(pattern, text)
        if found:
            return int(found.group(1)) * unit
    if re.search(r"\bhalf an hour\b", text):
        return 30
    return None


ALLERGY_WORDS = frozenset("allergic allergy allergies intolerant intolerance anaphylactic "
                          "anaphylaxis".split())
ALLERGY_PHRASES = ("cant eat", "can't eat", "cannot eat", "must avoid", "have to avoid",
                   "no nuts at all", "nut free diet")


A_WISH_FOR_A_FOOD = re.compile(r"\b(?:eat|eating|ate|get|getting|want|wants|wanted|need|needs|"
                              r"like|likes|try to eat|trying to eat|cut down on|cut back on)"
                              r"\s+(more|less|fewer)\s+(?:of\s+)?([a-z]+)")


def _the_foods_wanted_more_or_less(said_clean, named):
    if not named:
        return set()
    wished = set()
    for found in A_WISH_FOR_A_FOOD.finditer(said_clean or ""):
        word = found.group(2).strip(",.")
        name = _INGREDIENT_WORDS.get(word)
        if name is None:
            for ending in ("", "s", "es"):
                name = _INGREDIENT_WORDS.get(_fold(word) + ending)
                if name is not None:
                    break
        if name in named:
            wished.add(name)
    return wished


def _the_foods_wanted_more(said_clean, named):
    if not named:
        return set()
    more = set()
    for found in A_WISH_FOR_A_FOOD.finditer(said_clean or ""):
        if found.group(1) not in ("more",):
            continue
        word = found.group(2).strip(",.")
        name = _INGREDIENT_WORDS.get(word)
        if name is None:
            for ending in ("", "s", "es"):
                name = _INGREDIENT_WORDS.get(_fold(word) + ending)
                if name is not None:
                    break
        if name in named:
            more.add(name)
    return more


def wants(understood, old=None):
    context = {key: list(value) if isinstance(value, list) else value
               for key, value in (old or {}).items()}
    words = set(_said_words(understood))
    said_clean = _clean(understood)
    named = list(ingredients(understood))
    refused = list(negated_ingredients(understood))
    if words & ALLERGY_WORDS or any(phrase in said_clean for phrase in ALLERGY_PHRASES):
        for name in named:
            if name not in refused:
                refused.append(name)
    if _refuses(understood):
        for name in named:
            if name not in refused:
                refused.append(name)
    wished = _the_foods_wanted_more_or_less(said_clean, named)
    if wished:
        fancy = None
        for name in sorted(_the_foods_wanted_more(said_clean, named)):
            fancy = context.setdefault("fancy", [])
            if name not in fancy:
                fancy.append(name)
    for name in named:
        if name in refused or name in wished:
            continue
        have = context.setdefault("have", [])
        if name not in have:
            have.append(name)
    for name in refused:
        avoid = context.setdefault("avoid", [])
        if name not in avoid:
            avoid.append(name)
    if context.get("have") and any(phrase in said_clean for phrase in ONLY_PHRASES):
        context["only"] = True
    limit = minutes_said(understood)
    if limit is not None:
        context["limit"] = limit
    if words & VEG_WORDS or any(phrase in _clean(understood) for phrase in MEAT_FREE_PHRASES):
        context["veg"] = True
    if any(phrase in said_clean for phrase in DAIRY_FREE_PHRASES):
        avoid = context.setdefault("avoid", [])
        for name in DAIRY_FOODS:
            if name not in avoid:
                avoid.append(name)
    if "vegan" in words:
        context["vegan"] = True
    if CROWD_PHRASE.search(said_clean):
        context["crowd"] = True
    if ((context.get("veg") or context.get("vegan")) and not context.get("have")
            and (not context.get("crowd") or _meal_asked(understood))):
        context["diet"] = True
    if context.get("veg") and context.get("have"):
        meat = [name for name in context["have"] if name in MEAT_NAMES]
        if meat:
            context["have"] = [name for name in context["have"] if name not in MEAT_NAMES]
            if not context["have"]:
                context.pop("have", None)
                context["diet"] = True
    foodish = (bool(words & DINNER_WORDS) or bool(ingredients(understood))
               or any(phrase in _clean(understood) for phrase in COMING_FOR))
    said_clean = _clean(understood)
    if foodish and (_occasion(said_clean) and any(phrase in said_clean
                                                  for phrase in MENU_PHRASES)
                    or CROWD_PHRASE.search(said_clean) or words & BIG_DAYS
                    or (words & PEOPLE_WORDS
                        and any(phrase in said_clean for phrase in COMING_FOR))
                    or (words & EVENT_WORDS
                        and any(phrase in said_clean for phrase in COOKING_FOR))):
        context["occasion"] = True
    if words & LIMIT_WORDS or any(phrase in said_clean for phrase in SIMPLE_PHRASES):
        context["simple"] = True
    if words & HEAT_WORDS:
        if _a_taste_ruled_out(said_clean):
            context["no_heat"] = True
            avoid = context.setdefault("avoid", [])
            for name in HEAT_INGREDIENTS:
                if name not in avoid:
                    avoid.append(name)
        else:
            context["heat"] = True
    sweet = bool(words & SWEET_WORDS) or any(phrase in _clean(understood) for phrase in SWEET_PHRASES)
    if sweet and not ingredients(understood):
        context["sweet"] = True
        context.pop("have", None)
    if words & DISLIKE_WORDS and words & (GREEN_WORDS | {"veg", "vegetables", "veggies"}):
        context["no_green"] = True
    return context


def _fits(names, context):
    names = set(names)
    if names & set(context.get("avoid") or ()):
        return False
    if context.get("veg") and names & MEAT_NAMES:
        return False
    if context.get("no_green") and names & GREEN_NAMES:
        return False
    if context.get("no_heat") and names & set(HEAT_INGREDIENTS):
        return False
    return True


def _text_conflict(dish, context):
    text = (dish.get("text") or "").lower()
    for name in context.get("avoid") or ():
        for word in AVOID_TEXT.get(name, (name,)):
            if word in text:
                return True
    if context.get("vegan") and any(word in text for word in VEGAN_BAD):
        return True
    return False


QUICK_MINUTES = 20


def _quick_limit(context):
    if context.get("limit"):
        return context["limit"]
    return QUICK_MINUTES if context.get("simple") else None


def _quick_enough(minutes, context):
    limit = _quick_limit(context)
    return not (limit and minutes and minutes > limit)


def _score(dish, context):
    have = set(context.get("have") or ())
    uses = set(dish["uses"])
    minutes = MINUTES.get(dish["id"])
    score = len(uses & have) * 4 - len(have - uses) * 3
    if minutes is not None:
        score -= minutes // 25
        limit = _quick_limit(context)
        if limit and minutes > limit:
            score -= 6
    if context.get("simple") and minutes is not None:
        score -= max(0, minutes - 20) // 5
    if have and have <= uses:
        score += 4
    if have:
        score -= len(uses - have - STAPLES)
    else:
        score -= len(uses) * 2
    if context.get("occasion") and dish["id"] in THIN:
        score -= 6
    if context.get("occasion") and dish["id"] in FOR_ONE:
        score -= 10
    if context.get("heat"):
        text = (dish.get("text") or "").lower()
        score += 6 if any(word in text for word in HEAT_IN_TEXT) else -2
    if context.get("occasion") and dish["id"] in CROWD_DISHES:
        score += 8
        if (minutes or 0) >= 30:
            score += 4
        elif context.get("limit") is None:
            score -= 2
    return score


def _meal_idea_for(name):
    if name not in PANTRY:
        return None
    words = set(PANTRY[name][0]) | {name}
    for names, idea in MEAL_IDEAS:
        if words & set(names):
            return idea
    return None


def _ideas(context, limit=True):
    out = []
    have = list(context.get("have") or ())
    quick = _quick_limit(context) if limit else None
    for name in reversed(have):
        if name not in PANTRY or not _fits((name,), context):
            continue
        idea = PANTRY[name][1]
        if quick and (PANTRY_MINUTES.get(name) or 0) > quick:
            faster = _meal_idea_for(name)
            if faster:
                idea = faster
            elif limit:
                continue
        if _mentions(idea, context.get("avoid") or ()) or _text_conflict({"text": idea}, context):
            continue
        out.append((name, idea))
    return out


def plan_reply(context, memory=None, skip=()):
    if not context:
        return None
    if not context.get("have") and context.get("fancy"):
        context = dict(context, have=list(context["fancy"]))
    if context.get("only"):
        ideas = _ideas(context, limit=bool(context.get("limit") or context.get("simple")))
        if ideas:
            return " ".join(idea for _, idea in ideas[:2])
    offered = context.get("offered") or ()
    skip_ids = set(skip) | set(offered if isinstance(offered, (list, tuple, set)) else ())
    scored = []
    for dish in DISHES:
        if dish["id"] in skip_ids or not _fits(dish["uses"], context):
            continue
        if (dish["id"] in SWEET_DISHES) is not bool(context.get("sweet")):
            continue
        have = set(context.get("have") or ())
        if not have and not context.get("sweet") and not context.get("diet"):
            continue
        if have and not set(dish["uses"]) & have:
            continue
        if have and set(dish["uses"]) - have - STAPLES:
            continue
        if context.get("limit") or context.get("simple"):
            if not _quick_enough(MINUTES.get(dish["id"]), context):
                continue
        if context.get("no_green") and any(word in dish["text"].lower()
                                           for word in GREEN_IN_TEXT):
            continue
        if context.get("no_heat") and any(word in dish["text"].lower()
                                          for word in HEAT_IN_TEXT):
            continue
        if _text_conflict(dish, context):
            continue
        scored.append((_score(dish, context), dish))
    if scored:
        scored.sort(key=lambda pair: -pair[0])
        if memory is not None and isinstance(memory.get("meal"), dict):
            memory["meal"].setdefault("offered", []).append(scored[0][1]["id"])
        return _with_heat(scored[0][1]["text"], context)
    ideas = _ideas(context)
    if not ideas:
        ideas = _ideas(context, limit=False)
    if ideas:
        return " ".join(idea for _, idea in ideas[:2])
    return None


def _a_taste_ruled_out(said):
    for pattern in (_TASTE_RULED_OUT, _HOT_FOOD_RULED_OUT):
        for found in pattern.finditer(said or ""):
            after = (said or "")[found.end():found.end() + 12].lower()
            if after.strip().startswith("enough"):
                continue
            return True
    return False


def _with_heat(text, context):
    if not context.get("heat") or context.get("no_heat"):
        return text
    lowered = (text or "").lower()
    if any(word in lowered for word in HEAT_IN_TEXT):
        return text
    return (text.rstrip() + " Add chopped chilli or a pinch of chilli flakes with the onion for "
            "the heat - taste at the end and add more if it needs it.")


def plan_recent(memory):
    plan = (memory or {}).get("meal")
    if not isinstance(plan, dict):
        return None
    turns = (memory or {}).get("turns") or []
    if len(turns) - int(plan.get("turn") or 0) > PLAN_LAPSE:
        return None
    return plan


def _last_reply(memory):
    turns = (memory or {}).get("turns") or []
    if not turns:
        return ""
    return str((turns[-1] or {}).get("bot") or "")


def remembered(understood, memory):
    if not isinstance(understood, dict):
        return None
    if understood.get("kind") in ("empty", "greeting"):
        return None
    if _says_it_has_gone_off(understood.get("clean")):
        return None
    plan = plan_recent(memory)
    words = set(_said_words(understood))
    said = _clean(understood)
    topic = understood.get("topic_own")
    if words & PET_WORDS and not plan:
        return None
    if not plan and _a_crop_not_a_larder(understood):
        return None
    food = (topic in ("cooking", "food-and-drink") or bool(words & DINNER_WORDS)
            or bool(ingredients(understood)) or bool(negated_ingredients(understood)))
    if not food and not plan:
        return None
    stocked = (bool(ingredients(understood) or negated_ingredients(understood))
               and understood.get("kind") == "statement"
               and any(phrase in said for phrase in STOCK_PHRASES))
    wish = bool(_the_foods_wanted_more(said, list(ingredients(understood))))
    asking_with_food = (bool(ingredients(understood))
                        and any(phrase in _clean(understood) for phrase in NEW_MEAL_PHRASES))
    asking_how = (any(phrase in said for phrase in METHOD_PHRASES)
                  and len(ingredients(understood)) == 1
                  and not words & EVENT_WORDS and not CROWD_PHRASE.search(said))
    if not plan and (words & TECHNIQUE_WORDS or asking_how
                     or (not _meal_asked(understood) and not stocked and not asking_with_food
                         and not wish)):
        return None
    new = wants(understood)
    kept = {key: new[key] for key in PLAN_KEYS if key in new}
    if new.get("fancy"):
        kept["fancy"] = new["fancy"]
    if not kept and not food:
        return None
    if not plan and kept and set(kept) <= {"veg", "vegan"}:
        last_ask = set(str(((memory.get("turns") or [{}])[-1] or {}).get("user") or "")
                       .lower().split())
        if not last_ask & DINNER_WORDS:
            return None
    if not plan and not kept and understood.get("kind") != "question":
        return None
    if plan and plan.get("have") and _asks_about_a_food_it_has_not_got(understood, plan):
        return plan
    merged = wants(understood, plan)
    merged.setdefault("started", len(memory.get("turns") or []))
    merged["turn"] = len(memory.get("turns") or [])
    offered = [name for name in (merged.get("offered") or ()) if isinstance(name, str)]
    said_last = _last_reply(memory)
    if said_last:
        for dish in DISHES:
            if dish["id"] not in offered and dish["text"] in said_last:
                offered.append(dish["id"])
    if offered:
        merged["offered"] = offered[-4:]
    allergies = _allergy_names(memory)
    if allergies:
        gone = [name for name in (merged.get("have") or ())
                if _is_allergy_food(name, allergies)]
        if gone:
            left = [name for name in (merged.get("have") or ()) if name not in gone]
            if left:
                merged["have"] = left
            else:
                merged.pop("have", None)
            avoid = list(merged.get("avoid") or ())
            avoid.extend(name for name in gone if name not in avoid)
            merged["avoid"] = avoid
    return merged


def _allergy_names(memory):
    user = (memory or {}).get("user") or {}
    return [str(name).lower() for name in (user.get("allergies") or ()) if str(name).strip()]


def _is_allergy_food(name, allergies):
    folded = _fold(str(name))
    stem = folded[:4]
    return bool(stem) and any(stem in allergy[:4] or allergy[:4] in folded
                              for allergy in allergies if len(allergy) >= 4)


_ABOUT_A_FOOD = ("what about", "how about", "what can i do with", "what else with",
                 "instead of", "without")


def _asks_about_a_food_it_has_not_got(understood, plan):
    named = [name for name in ingredients(understood)
             if name not in (plan.get("have") or ())]
    if len(named) != 1 or set(named) & set(plan.get("avoid") or ()):
        return False
    if set(_said_words(understood)) & DINNER_WORDS:
        return False
    said = _clean(understood)
    if any(phrase in said for phrase in _ABOUT_A_FOOD):
        return True
    return bool(ABSENCE.search(said))


ABSENCE = re.compile(r"\b(?:havent|haven't|dont have|don't have|didnt have|didn't have|"
                     r"ran out|run out|out of|got any|no)\b")


def _narrowing(understood, plan=None, longest=10):
    words = set(_said_words(understood))
    if not words or len(words) > longest:
        return None
    if understood.get("kind") in ("empty", "greeting", "thanks"):
        return None
    said = _clean(understood)
    own = understood.get("topic_own")
    if own not in (None, "cooking", "food-and-drink") and not ingredients(understood):
        narrowed = any(key in wants(understood) for key in PLAN_KEYS if key != "simple")
        if not (plan and (narrowed or "limit" in wants(understood))):
            return None
    if words <= CHATTER and not words & DINNER_WORDS:
        return None
    if any(phrase in said for phrase in SWAP_PHRASES):
        return None
    if any(phrase in said for phrase in WITH_PHRASES):
        return None
    if set(understood.get("asks") or ()) & {"how", "how_long", "how_much", "where", "how_often",
                                            "why"}:
        return None
    if words & TECHNIQUE_WORDS and minutes_said(understood) is None:
        return None
    if "yesno" in set(understood.get("asks") or ()):
        if ingredients(understood) or words & {"it", "its", "that", "this", "them", "those"}:
            return None
    if ingredients(understood) and any(phrase in said for phrase in NEW_MEAL_PHRASES):
        return None
    if words & BAKING_WORDS and not words & {"dinner", "tea", "supper", "lunch", "meal"}:
        return None
    if any(phrase in said for phrase in SAID_PHRASES):
        return None
    if (words & PERSON_WORDS and words & TASTE_WORDS
            and not words & DINNER_WORDS and minutes_said(understood) is None):
        return None
    new = wants(understood)
    if new.get("heat") and (plan or {}).get("sweet"):
        return None
    kept = any(key in new for key in PLAN_KEYS if key != "simple")
    kept = (kept or "limit" in new or bool(words & LIMIT_WORDS) or "heat" in new
            or any(phrase in said for phrase in SIMPLE_PHRASES))
    asked = (bool(words & DINNER_WORDS)
             or any(phrase in said for phrase in MEAL_PHRASES
                    if phrase not in BARE_MEAL_NOUNS)
             or _the_bare_ideas_are_about_food(understood, said))
    pointed = any((plan or {}).get(key) for key in PLAN_KEYS)
    asking = understood.get("kind") == "question" or bool(understood.get("asks"))
    if not kept and not (asked and pointed and asking):
        return None
    return wants(understood, plan)


BARE_MEAL_NOUNS = ("idea", "ideas", "recipe", "recipes")
BARE_MEAL_OBJECT = re.compile(r"\b(?:ideas?|recipes?)\s+(?:for|with|using|about|on)\s+(.*)", re.I)
THE_FOOD_IN_HAND = frozenset("it them those these this rest leftover leftovers other left "
                             "using use".split())


def _the_bare_ideas_are_about_food(understood, said):
    if not any(noun in said for noun in BARE_MEAL_NOUNS):
        return False
    if ingredients(understood):
        return True
    named = BARE_MEAL_OBJECT.search(said)
    if named is None:
        return True
    return bool(set(re.findall(r"[a-z']+", named.group(1).lower())) & THE_FOOD_IN_HAND)

ONLY_PHRASES = ("only have", "only got", "only have got", "nothing but", "all i have",
                "all i've got", "all ive got", "just have", "thats all i", "that's all i")
WITH_PHRASES = ("have with it", "have with that", "eat with it", "goes with", "go with it",
                "serve with it", "serve it with", "served with", "on the side", "alongside",
                "what can i have", "what should i have", "with that meal")
PICK_PHRASES = ("you pick", "you choose", "you decide", "your call", "your choice",
                "up to you", "whatever you think", "whatever you like", "i don't mind",
                "i dont mind", "either is fine", "pick one", "you tell me")


def _idea_on_the_plate(plan, memory):
    said = _last_reply(memory)
    if not said:
        return None
    lowered = said.lower()
    for name in plan.get("have") or ():
        for alias in (PANTRY.get(name) or ((),))[0]:
            if alias in lowered:
                return said
    return None


def _chosen(plan):
    dishes = {dish["id"]: dish for dish in DISHES}
    for name in reversed(list(plan.get("offered") or ())):
        dish = dishes.get(name)
        if dish and _fits(dish["uses"], plan) and not _text_conflict(dish, plan):
            return dish["text"]
    return None


_A_REACTION = ("nut free diet", "no nuts at all", "no dairy at all", "carry an epipen")


def _an_allergy(understood):
    said = _clean(understood)
    if set(_said_words(understood)) & ALLERGY_WORDS:
        return True
    return any(phrase in said for phrase in _A_REACTION)


def _nothing_to_change(understood, memory):
    new = wants(understood)
    if any(key in new for key in PLAN_KEYS if key != "avoid"):
        return None
    plan = plan_recent(memory) or {}
    if not plan.get("offered"):
        return None
    kept = list(new.get("avoid") or ())
    said = _last_reply(memory)
    if not kept or not said:
        return None
    names = f"{' or '.join(kept[:2])}"
    if _an_allergy(understood):
        banned = sorted(_excluded(_clean(understood)))
        mine = [word for word in _said_words(understood) if word in banned]
        theirs = _about_someone_else(understood)
        in_dish = [word for word in banned if _mentions(said, (word,))]
        who = "theirs" if theirs else "that one"
        if in_dish:
            left_out = in_dish[0]
            where = " or ".join(mine[:2]) or left_out
            return (f"The {left_out} is where the {where} is, so leave it out of {who} and keep "
                    "the rest the same - and read the label on anything that came in a packet "
                    "before you use it.")
        if mine:
            return (f"There is no {' or '.join(mine[:2])} in that dish as it stands, so it is "
                    f"safe{' for them' if theirs else ''} - just keep the boards and knives clean, "
                    "and read the label on anything that came in a packet before you use it.")
        return None
    if _about_someone_else(understood):
        if _mentions(said, kept):
            return f"Then make theirs without the {names} and keep the rest the same - it works."
        return f"That one has no {names} in it anyway, so theirs is fine."
    if _mentions(said, kept):
        return f"Leave the {names} out of that one and it still works."
    return f"That one has no {names} in it anyway, so you're fine."


ACK_WORDS = frozenset("""ok okay k cool nice great good fine fair sure right true exactly yeah yep
yes no nah thanks thank cheers ta please sorry oh ah mm hmm mmm got get gotcha noted understood
makes sense sounds sound will do try trying then so and but that this it its low high heat slow
quickly gently careful huh righto alright perfect ace brill lovely accepted""".split())


def _only_an_acknowledgement(text):
    words = re.findall(r"[a-z']+", (text or "").lower())
    if not words or len(words) > 7:
        return False
    return all(word in ACK_WORDS for word in words)


A_SUM_OF_MONEY = re.compile(
    r"£\s*[0-9]|\b[0-9][0-9,]*(?:\.[0-9]+)?\s*(?:pounds?|quid|bucks)\b"
    r"|\b(?:tenner|fiver|score)\b"
    r"|\b(?:a|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|fifteen|twenty|"
    r"thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred)\s+(?:pounds?|quid|bucks)\b",
    re.I)


def follow_up(understood, memory):
    if _says_it_has_gone_off(understood.get("clean")):
        return None
    pointed_food = pointed_at_a_food(understood, memory)
    if pointed_food:
        return pointed_food
    plan = plan_recent(memory)
    if not plan:
        return None
    said = _clean(understood)
    if asks_the_kinds(understood):
        return None
    if _only_an_acknowledgement(said):
        return None
    if A_SUM_OF_MONEY.search(said):
        return None
    if _a_brew_not_a_dinner(said):
        return None
    if len(said.split()) <= 6 and any(phrase in said for phrase in PICK_PHRASES):
        chosen = _chosen(plan) or _idea_on_the_plate(plan, memory)
        if chosen:
            return chosen
        return None
    if int(plan.get("started") or 0) >= len(memory.get("turns") or []):
        return None
    context = _narrowing(understood, plan)
    if not context:
        if plan.get("fancy") and not plan.get("have") and _a_bare_meal_ask(understood):
            return plan_reply(dict(plan, have=list(plan["fancy"])), memory)
        return None
    if context.get("sweet") and not (plan.get("have") or plan.get("offered")):
        return None
    added = [name for name in (context.get("have") or ())
             if name not in (plan.get("have") or ())]
    if added and not (context.get("avoid") or context.get("veg") or context.get("vegan")):
        return None
    answering = context
    if not context.get("have") and context.get("fancy"):
        answering = dict(context, have=list(context["fancy"]))
    reply = _nothing_to_change(understood, memory) or plan_reply(answering, memory)
    if reply is None:
        return None
    if reply.strip() == str(_last_reply(memory) or "").strip():
        others = [idea for _, idea in _ideas(answering, limit=False) if idea != reply]
        if others:
            reply = " ".join(others[:2])
    if isinstance(memory.get("meal"), dict):
        offered = context.get("offered") or memory["meal"].get("offered") or []
        context["offered"] = list(offered)[-4:]
        memory["meal"] = context
    return reply


BARE_MEAL_ASK_WORDS = frozenset("""
    what shall should i we you can could do to for now then tonight tonights have eat make cook
    cooking dinner tea supper lunch meal meals something anything a an the some quick easy simple
    """.split())


def _a_bare_meal_ask(understood):
    if ingredients(understood) or set(understood.get("asks") or ()) & {"how", "how_long",
                                                                      "how_much", "why"}:
        return False
    words = set(_said_words(understood))
    if not words or words - BARE_MEAL_ASK_WORDS:
        return False
    return bool(words & {"cook", "make", "cooking", "dinner", "tea", "supper", "lunch", "meal",
                         "eat"})


REFUSAL = re.compile(r"\b(?:won['\u2019]?t|wouldn['\u2019]?t|don['\u2019]?t|doesn['\u2019]?t|"
                     r"didn['\u2019]?t|can['\u2019]?t stand|hates?|hated|dislikes?|refuses?|"
                     r"picky|not eat|no thanks)\b")


def _refuses(understood):
    if set(_said_words(understood)) & DISLIKE_WORDS:
        return True
    return bool(REFUSAL.search(_clean(understood)))


THE_WAY_TO_COOK = re.compile(
    r"\b(?:best|quickest|fastest|easiest|simplest|cheapest|healthiest|healthier|safest|right|"
    r"proper|good|nice) way (?:to|of)\b"
    r"|\bthe way (?:to|of) (?:cook|cooking|make|making|bake|baking|roast|boil|fry|steam)\b")


def _meal_asked(understood):
    said = _clean(understood)
    if THE_WAY_TO_COOK.search(said):
        return False
    words = set(_said_words(understood))
    if not words & MEAL_FRAME:
        return False
    if words & DISH_WORDS or words & BAKING_WORDS:
        return False
    if words & {"breakfast", "lunch", "brunch"}:
        return False
    if len(ingredients(understood)) > 1:
        return False
    said = _clean(understood)
    return not any(phrase in said for phrase in SAID_PHRASES)


FOOD_PROPERTY = re.compile(
    r"\b(?:gluten|wheat|dairy|lactose|calories|calorie|carbs|carb|protein|fat|fattening|sugar|"
    r"salt|healthy|healthier|safe|vegan|vegetarian|allergy|allergic|coeliac|"
    r"ok|okay|fine|alright|good|bad|worth it)\b", re.I)
COOK_REQUEST = re.compile(r"\b(?:cook|cooks|cooking|cooked|make|makes|making|bake|recipe|recipes|"
                          r"dinner|teatime|supper|lunch|meal|meals|feed|serve)\b", re.I)


def asks_a_food_fact(understood):
    if not isinstance(understood, dict):
        return False
    said = _clean(understood)
    if not said or COOK_REQUEST.search(said):
        return False
    if not (understood.get("asks") or understood.get("kind") == "question"):
        return False
    if not FOOD_PROPERTY.search(said):
        return False
    return True


def first_plan(understood, memory=None):
    plan = plan_recent(memory)
    if plan and int(plan.get("started") or 0) < len(memory.get("turns") or []):
        return None
    context = _narrowing(understood, longest=14)
    if not context:
        return None
    if not _meal_asked(understood):
        return None
    if not any(key in context for key in ("limit", "veg", "vegan", "no_green", "occasion",
                                          "simple", "sweet")):
        return None
    if set(context) - {"started", "turn"} <= {"veg", "vegan", "diet", "simple", "limit"}:
        return None
    if _left_to_the_meal_entry(understood, context):
        return None
    return plan_reply(context)


def _left_to_the_meal_entry(understood, context):
    text = str(understood.get("clean") or " ".join(str(w).lower()
                                                   for w in (understood.get("words") or [])))
    if _crowd(text) >= 6:
        return True
    if _occasion(text) and any(phrase in text for phrase in
                               ("cook", "dinner", "meal", "make", "eat")):
        return True
    if set(context) - {"started", "turn"} <= {"sweet"}:
        try:
            if find(understood) is not None:
                return True
        except Exception:
            pass
    if set(context) <= {"sweet"} and any(phrase in text for phrase in THIN_CUPBOARD_PHRASES):
        return True
    if set(context) <= {"simple", "started", "turn"}:
        return True
    return False


THIN_CUPBOARD_PHRASES = ("with what i have", "with what i've got", "with what ive got",
                         "what i have in", "in the cupboard", "in the fridge", "in the pantry",
                         "left in the")


CHILLI_FRUIT = ("chilli", "chillies", "chili", "chilies", "chile", "jalapeno", "jalapenos",
                "serrano", "birdseye", "scotch bonnet", "habanero", "red chilli", "green chilli",
                "pepper", "peppers", "bell pepper", "bell peppers", "red pepper", "green pepper",
                "sweet pepper", "chilli pepper", "chili pepper")

SEED_FRUIT = CHILLI_FRUIT + ("pomegranate", "pomegranates", "tomato", "tomatoes", "cucumber",
                             "cucumbers", "courgette", "courgettes", "marrow", "pumpkin",
                             "squash", "butternut", "melon", "melons", "watermelon",
                             "aubergine", "eggplant")

_CHILLI_SEEDS = (
    "Cut the stalk off and halve it lengthways, then scrape the seeds and the pale pith out with "
    "the tip of a knife or a teaspoon - that pith is where most of the heat sits, so take it out "
    "too if you want the chilli mild. Slice it on a board, not in your hand, and keep your hands "
    "away from your eyes and your mouth. Wash the board, the knife and your hands in cold water "
    "and soap straight after: the oil that burns is not washed off by rinsing. If your hands do "
    "burn, rub them with oil then wash again, or soak them in milk, not water.")
_POMEGRANATE_SEEDS = (
    "Cut the crown off and score the skin down the ridges, then break it open in a bowl of water "
    "and knock the seeds out with a wooden spoon: the seeds sink, the pith and the membrane float "
    "and you can skim them off. Doing it under water is what stops the juice reaching your shirt, "
    "and it is much quicker than picking them out.")
_TOMATO_SEEDS = (
    "Halve it across the middle, not top to bottom, and squeeze or scoop the seeds out with a "
    "finger or a teaspoon. The jelly round them is the flavour, so keep it if you are cooking; "
    "for a sandwich or a salad, a sieve catches the juice and you can salt the halves and leave "
    "them upside down for ten minutes instead.")
_CUCUMBER_SEEDS = (
    "Halve it lengthways and run a teaspoon down the middle to scoop the watery seeds out - a "
    "grapefruit spoon has the right edge for it. Salt the halves and leave them face down for "
    "fifteen minutes afterwards and the water comes out too, which is what a soggy sandwich is.")
_MELON_SEEDS = (
    "Halve it and scoop the seeds out with a spoon, then rinse the last of the strings off under "
    "the tap. A watermelon is easier cut into wedges and the seeds flicked out with the tip of a "
    "knife, and if you want it neat, cut it in slices and stamp the seeds out with a small round "
    "cutter.")
_SQUASH_SEEDS = (
    "Halve it and scoop the strings and seeds out with a metal spoon, working round the edge "
    "towards the middle. Keep the seeds: rinse them, toss in a little oil and salt and roast "
    "them at 180C for 10 to 15 minutes.")


def _deseed(memory, understood):
    words = " ".join(understood.get("words") or [])
    for family, reply in ((("pomegranate", "pomegranates"), _POMEGRANATE_SEEDS),
                          (("tomato", "tomatoes"), _TOMATO_SEEDS),
                          (("cucumber", "cucumbers", "courgette", "courgettes", "marrow"),
                           _CUCUMBER_SEEDS),
                          (("melon", "melons", "watermelon"), _MELON_SEEDS),
                          (("pumpkin", "squash", "butternut"), _SQUASH_SEEDS)):
        if any(word in words for word in family):
            return reply
    return _CHILLI_SEEDS


ENTRIES.append(entry(
    "deseed-chilli",
    (SEED_FRUIT,
     ("deseed", "de-seed", "deseeding", "seeds", "seed", "seedless", "membrane", "pith",
      "core", "coring", "take out", "take the seeds out", "remove the seeds", "remove seeds",
      "get rid of the seeds", "less hot", "not so hot", "milder", "mild", "heat")),
    _deseed,
    avoid=("chilli con carne", "con carne", "recipe", "grow", "growing", "plant", "plants",
           "seedling", "sow", "sowing", "germinate", "sauce", "oil", "powder", "flakes",
           "paste", "jam", "pickle", "pickled", "dry", "dried", "freeze", "freezer", "keep",
           "store", "storage", "shelf life", "go off", "best variety", "which chilli",
           "scoville", "how hot is",
           "roast", "roasting", "roasted", "toast", "toasted", "salt", "salted", "snack",
           "saving", "save the seeds", "harvest", "collect the seeds"),
    ask=("how do i", "how to", "how can i", "should i", "do i need to", "is it better",
         "deseed", "de-seed", "seeds", "membrane", "pith"),
    bias=2))


ENTRIES.append(entry(
    "umami",
    (("umami", "the fifth taste", "savoury taste", "savory taste"),
     ("what", "how", "explain", "mean", "get", "add", "more", "boost", "taste", "tasteless",
      "food", "dish", "cook", "put", "sauce", "good", "source", "sources")),
    ("Umami is the savoury taste that makes food taste deep and round rather than just salty: it "
     "comes from glutamates, and the everyday sources are soy sauce, fish sauce, miso, tomato "
     "paste, mushrooms, hard cheese, anchovies, seaweed, stock cubes and slow-cooked meat. It is "
     "what a dish is missing when it is seasoned but still flat, so add a spoon of one of those "
     "rather than more salt, and give it a squeeze of lemon or a splash of vinegar to make it "
     "show. Parmesan, tomato and mushroom together are why a good ragu tastes bigger than its "
     "ingredients."),
    explain=True))

SLOT_IDEAS = (
    ("brunch", (
        "Brunch is one thing on the table people help themselves to: scrambled eggs on toast with "
        "tomatoes and something green, a frittata cut into wedges, or pancakes with fruit and "
        "yoghurt. For more than four, baked eggs in one dish with bread beside it - fried eggs for "
        "eight are cold before the last one is done.")),
    ("lunch", (
        "Two shapes that work: a sandwich with something wet in it - hummus, tuna mayo, leftover "
        "roast - plus fruit, or soup with bread. The real answer is cooking extra at dinner: cold "
        "roast chicken, or lentils with feta, is a five-minute lunch the next day.")),
    ("snack", (
        "One thing with protein and one with fibre holds you until the next meal: apple with "
        "peanut butter, yoghurt with fruit, toast with cheese, or a handful of nuts.")),
)

SLOT_ASKS = ("what should i", "what can i", "what shall i", "what do i", "ideas", "any ideas",
             "suggest", "suggestions", "make", "have", "eat", "cook", "fix", "quick", "easy")


def _one_person_at_this_meal(understood):
    if not understood:
        return True
    for field in ("text", "clean"):
        line = str(understood.get(field) or "").lower()
        if line and _table_text(line):
            return False
    return True


def _a_meal_for_the_slot(memory, understood):
    text = " " + str((understood or {}).get("clean") or "").lower() + " "
    for slot, reply in SLOT_IDEAS:
        if " " + slot in text or slot + "s " in text:
            return reply
    return None


ENTRIES.append(entry(
    "meal-idea-for-a-slot",
    ((("brunch", "brunches", "snack", "snacks", "elevenses",
       "what should i make for lunch", "what can i make for lunch",
       "what shall i make for lunch", "what do i make for lunch"), SLOT_ASKS)),
    _a_meal_for_the_slot,
    avoid=("dinner", "tea", "tonight", "roast", "chicken", "beef", "pork", "lamb", "fish",
           "salmon", "pasta", "rice", "egg", "eggs", "potato", "potatoes", "bread", "cheese",
           "soup", "salad", "cake", "biscuit", "pancake", "porridge", "toast", "hummus",
           "sandwich", "curry", "chilli", "stew", "pie", "pizza", "noodles", "quinoa",
           "how long", "how do i cook", "how do i make", "recipe", "freeze", "leftover",
           "leftovers", "calories", "healthy", "diet", "batch", "pudding", "dessert",
           "birthday", "kids", "toddler", "baby", "weaning", "school lunch", "lunchbox",
           "restaurant", "takeaway", "book", "table for"),
    guard=_one_person_at_this_meal,
    bias=1))


ON_WORDS = (
    "put on", "to put on", "put on it", "put on them", "what can i put", "what to put",
    "goes on", "go on", "have on", "add to", "add on", "add in",
    "topping", "toppings", "topping ideas", "on top",
)

NOT_A_TOPPING_ASK = (
    "how long", "how do i cook", "how do you cook", "how to cook", "how do i make",
    "how do you make", "recipe", "from scratch", "calories", "freeze", "frozen", "defrost",
    "keep", "keeps", "keeping", "kept", "fridge", "leftover", "leftovers", "left over",
    "buy", "cheaper", "price", "cost", "substitute", "instead of", "how much", "healthy",
    "diet", "make with", "make from", "batch", "bake", "roast", "boil", "fry", "grill",
    "shop", "supermarket", "brand", "best buy", "how many",
)

ON_TOPPINGS = (
    ("toast", ("toast",), (
        "Butter first, then something sharp or salty on top: peanut butter and sliced banana, "
        "mashed avocado with salt and lemon, beans with a dash of Worcestershire, or a tin of "
        "sardines on hot toast. Cheese on toast under the grill for 3 minutes is the fastest good "
        "one, and a sliced tomato under the cheese stops it going dry.")),
    ("pasta", ("pasta", "spaghetti", "penne", "macaroni", "fusilli", "tagliatelle", "linguine"), (
        "Something you can stir through in the time the pasta boils: garlic and chilli warmed in "
        "olive oil, a tin of tomatoes simmered 10 minutes with a pinch of sugar, or cream cheese "
        "with lemon zest and black pepper. Keep a mug of the pasta water - a splash of it makes "
        "any of them cling instead of sitting in the bottom of the bowl.")),
    ("rice", ("rice", "basmati", "long grain", "boiled rice"), (
        "Cold cooked rice is best fried: hot oil, an egg, soy sauce and whatever veg is in the "
        "drawer, 4 minutes. On hot rice, a curry or a chilli ladled over it is dinner, and cold "
        "rice with tuna, sweetcorn and mayo is a lunch - the rice wants a day old for either, "
        "because fresh rice steams instead of frying.")),
    ("chips", ("chips", "fries", "french fries"), (
        "Salt and vinegar, gravy, curry sauce, garlic mayo, or cheese and chilli: chip-shop curry "
        "sauce is the one to try if you want the bag to feel like a treat. A fried egg on top "
        "makes it a meal, and mushy peas or a pickled onion cut through the fat.")),
    ("porridge", ("porridge", "oats", "oatmeal"), (
        "Sweet: honey or jam with a spoon of peanut butter, stewed apple with cinnamon, or frozen "
        "berries stirred in while it is hot. Savoury: butter, salt and a poached egg, or grated "
        "cheese and black pepper - porridge is only oats cooked in water or milk, so it takes "
        "either, and the salt is what makes the sweet version taste of something.")),
    ("noodles", ("noodles", "noodle", "ramen"), (
        "A sauce in the time they boil: a spoon of peanut butter, soy sauce, a squeeze of lime and "
        "some chilli; or fry them with an egg and whatever veg you have plus soy sauce. Sesame "
        "oil and sliced spring onion at the end is what makes them taste like the takeaway.")),
    ("couscous", ("couscous",), (
        "Couscous takes a dressing better than it takes a sauce: lemon juice, olive oil, chopped "
        "tomato, cucumber, parsley and feta is a lunch in 10 minutes. It also drinks up the juices "
        "of a stew or roast veg, which is why it is served under them.")),
    ("salad", ("salad", "leaves", "lettuce", "rocket"), (
        "Something sharp, something salty, something crunchy: olive oil and lemon or vinegar, "
        "then salt, then nuts, seeds or croutons. A dressing of 2 parts oil to 1 part vinegar "
        "with a spoon of mustard, shaken in a jar, keeps a week in the fridge.")),
    ("crackers", ("crackers", "cracker", "crispbread", "oatcakes"), (
        "Cheese, chutney and an apple; cream cheese with smoked salmon or cucumber; hummus and "
        "something crunchy; butter and a sliced boiled egg with salt and pepper. Anything soft "
        "wants something crisp on it, and anything dry wants something wet.")),
    ("soup", ("soup",), (
        "A swirl of cream or yogurt loosens a thick soup, and something crisp on top - croutons, "
        "toasted seeds, a handful of crushed crisps - makes it feel finished. A squeeze of lemon "
        "or a splash of vinegar at the end lifts a soup that tastes flat, which is usually what "
        "it is missing rather than salt.")),
    ("pancakes", ("pancakes", "pancake", "crepes", "crepe"), (
        "Lemon and sugar is the classic, and butter with golden syrup or jam works as well "
        "without the fuss. For savoury, fold cheese and ham inside, or put a fried egg on top. "
        "Keep them warm in a low oven and add the topping at the table, so nothing goes soggy.")),
    ("ice-cream", ("ice cream", "icecream", "gelato"), (
        "Hot chocolate sauce, tinned peaches or raspberries with a splash of their juice, crushed "
        "biscuits or toasted nuts, and a pinch of salt on anything caramel. A shot of espresso "
        "over vanilla is affogato, which is the best 30-second pudding there is.")),
    ("yoghurt", ("yoghurt", "yogurt"), (
        "Fruit and a spoon of honey, granola or toasted oats for crunch, and nuts or seeds for "
        "texture; a spoon of peanut butter and a little cocoa makes it taste like dessert. Plain "
        "yoghurt with chopped cucumber, mint, salt and garlic is a dip instead, and it wants "
        "straining first if it is watery.")),
)

for _staple, _words, _reply in ON_TOPPINGS:
    ENTRIES.append(entry("topping-on-" + _staple, (_words, ON_WORDS), _reply,
                         avoid=NOT_A_TOPPING_ASK))
del _staple, _words, _reply
