import re

from ..compose.repair import amends_to, line_of
from .dishes import KEEP_QUALITY_WORDS, PAIRING_FOODS
from .freshness import (a_cooling_question_not_a_keeping_one, soak_but_not_left_out,
                        _not_how_to_keep_it_fresh, _not_just_a_hard_loaf)
from .lookup import (DAY_WORDS, JOB_GUARD, PACK_DATE, TOOTH_OUT, entry,
                     not_the_flat_you_live_in)
from .shopping import not_a_present
from .body import a_persons_temperature

from . import cooking as _cooking_tables
from .cooking import (
    DECIDING, _line, missing, without,
    BAKED_GOODS_WORDS, CALORIE_ASKS, COMING_APART, COOK_VERBS, COOK_WORDS,
    DEFINITION_WORDS, DIABETIC_PLATE, FOOD_CALORIES, FOOD_CALORIE_MEALS, FOOD_NUTRIENTS,
    FREEZER_KEEP, FREEZE_FACTS, GLUTEN_FACT_ASKS, GLUTEN_FACT_FOODS, GLUTEN_FREE_ASKS,
    GLUTEN_FREE_DISHES, KEEPING,
    KEEP_ASK, LEAFY, LEAFY_AVOID, MEATLESS_ROAST,
    NOT_A_COOKING_LINE, OPEN_ASK, PET_LINE_WORDS, PLAN_NAMES,
    STAPLE_ASK, STORAGE, WANT_SOMETHING_ELSE, _BAKE_FAULT,
    _BAKE_THING, _CHEAP_AVOID, _EGG_DISH, _EGG_FAULT,
    _EGG_SAUCE, _FOOD, _A_TASTE, _FREEZE_AVOID, _GLUTEN_FREE_SKIP,
    _GRAIN_FOOD, _GRAIN_WORD, _MASH_NOT_THIS, _MEAL_ASK_AVOID,
    _NOT_MINE, _NO_MEAT, _NUTRIENT_ASK_WORDS, _NUTRIENT_WORDS, _OUT_ASK,
    _STAPLE_NAMES, _SWAP_ASK, _WET_FOOD, asks_a_gluten_fact, _bake, _learn_to_cook,
    _not_a_portion_ask,
    _BAKE_FAULT_FAMILIES, _BAKE_FOLLOW_SHAPES, _BAKE_KEEP_SHAPES, _BAKE_KEEPING,
    _BAKED_GOODS, _CAKE_NAMES, _NO_CAKE_RISE, _NO_LOAF_RISE, _NO_SPREAD_RISE,
    _bake_follow, _bake_keep, _gummy,
    _a_soft_fruit_is_still_a_cooking_question,
    _bake_always, _bake_burning, _bake_fault, _bake_fruit, _baked_keep,
    _body, _bread, _bread_rise_answer, _breakfast_ideas,
    _burnt_dish, _burnt_pan, _cake_fault, _calories,
    _cauliflower_rice, _chicken_time, _chocolate, _coffee_fault,
    _container_keep, _cook_word, _cookies, _dip_fault,
    _dough, _dry, _egg_fault, _eggs, _falls_apart,
    _flat, _free_of_gluten_fact, _freeze_food, _gluten_free, _grainy,
    _MINCE_GRAIN_DISH, _MINCE_GRAIN_WORD, _mince_grainy, _crowd,
    _greasy, _herbs_keep, _honey_age, _kids_veg,
    _bans_of, _legs, _lentils, _lumpy, _lunch_ideas, avoids_for_the_one_talked_about,
    _meal_ideas, _meal_plan, _meat_defrost, _mince,
    _non_stick_pan, _nut_free, _nutrients, _oil_smoking,
    _pancake_batch, _pancakes, _pasta_cook, _pastry_fault,
    _popcorn_keep, _popcorn_make, _protein, _pudding_ideas,
    _pulses, _rest_the_meat, _rice_time, _roast_joint,
    _roast_shopping, _salty, _scramble, _sides,
    _jacket, _jam_make, _mushroom_wash, _poach_fish, _soggy_lunch, _soup, _split,
    _staple, _tea_reply,
    _stuck_jar, _sugar_work, _sweet_potato, _tenders_are_a_piece, _tenders_method,
    _thighs,
    _time_budget, _tin_answer, _tough, _turkey,
    _turkey_cut, _undercooked, _vegan_bake, _watery,
    entry,
)

_EXTRA_BASICS = (
    (("lamb chops", "lamb chop", "lamb cutlets", "lamb cutlet"),
     "Lamb chops are a hot-pan job, 3 to 4 minutes a side for pink in the middle, or 5 if you "
     "want them through, then 3 minutes resting: a chop is thin, so the pan has to be properly "
     "hot before they go in and the fat edge wants standing on to render. In the oven they take "
     "12 to 15 minutes at 200C (180C fan). Salt them just before they go in, not before."),
    (("lamb shank", "lamb shanks"),
     "Braise lamb shanks: brown them in a heavy pan, then cook covered at 160C (140C fan) for 2 "
     "to 2.5 hours with stock, onion, carrot and a spoon of tomato, until the meat gives way to "
     "a fork. They are the cut a slow cooker suits, on low for 6 to 8 hours. Cook them the day "
     "before if you can, because the sauce sets and the fat comes off in one piece."),
    (("gammon steak", "gammon steaks", "gammon"),
     "Gammon steak is cooked through, not pink: 4 to 5 minutes a side in a hot pan, or 15 to 20 "
     "minutes under a grill, turning once. If it is thick or you want it milder, simmer it 15 "
     "minutes in water first, then dry it and fry it. It needs no salt - it is already cured - "
     "and a spoon of honey or marmalade in the pan at the end glazes it."),
    (("beef brisket", "brisket", "brisket joint", "rolled brisket"),
     "Brisket is a long cook, not a quick one: in the oven at 150C (130C fan), covered, for 3 "
     "to 4 hours, or about 1 hour per 500g, with a splash of stock in the tin, until a fork "
     "slides in with no pull. "
     "Season it heavily the night before if you can. It slices better after 20 minutes resting, "
     "and it is the one cut that is better the next day."),
    (("lamb kofta", "kofta", "koftas", "lamb kofte", "kofte"),
     "Kofta is minced lamb shaped by hand: mix 500g of mince with a grated onion squeezed dry, a "
     "handful of parsley, cumin, cinnamon and salt, then shape fingers around a skewer and grill "
     "them 10 to 12 minutes, turning, on a barbecue or under the grill, or bake them on a tray "
     "in the oven at 200C (180C fan) for "
     "15 to 18 minutes, or fry them 3 to 4 minutes a side. The onion is what keeps "
     "them soft; squeeze it or they fall apart."),
    (("duck legs", "duck leg", "duck thighs", "duck thigh"),
     "Roast duck legs at 160C (140C fan) for 1.5 to 2 hours, skin side up on a rack over a tin, "
     "until the skin is crisp and the meat pulls off the bone: the long slow heat is what renders "
     "the fat under the skin, and a hot oven just burns it. Prick the skin, salt it well, and do "
     "not cover them."),
    (("liver", "lambs liver", "chicken liver", "chicken livers", "calves liver", "pig liver"),
     "Liver is a hot, fast job: pat it dry, flour it lightly if you like, and fry it 2 to 3 "
     "minutes a side in a hot pan with butter, no more, until it is brown outside and still pink "
     "in the middle. Past that it goes grainy and bitter. Soaking it 30 minutes in milk takes the "
     "edge off a strong one, and it wants onions cooked slowly first, not alongside."),
    (("kidneys", "kidney", "lamb kidneys", "pig kidneys", "calves kidneys"),
     "Kidneys are a hot, fast job like liver: halve them, cut out the white core, and fry them 2 "
     "minutes a side in a very hot pan with butter, or 3 to 4 minutes in total if they are sliced. "
     "Past that they go rubbery. In a stew they are the opposite - an hour and a half, low - which "
     "is why the same meat has two timings."),
    (("whole duck", "a whole duck", "roast duck", "roasting duck"),
     "Roast a whole duck at 200C (180C fan) for 20 minutes, then at 160C (140C fan) for 20 "
     "minutes per 500g, pricking the skin all over and salting it first: the hot start crisps the "
     "skin and the lower heat renders the fat under it. Rest it 15 minutes. If you have time, pour "
     "a kettle of boiling water over it and let it dry before it goes in - that is what makes the "
     "skin crackle."),
    (("whole fish", "a whole fish", "whole salmon", "whole trout", "whole sea bass",
      "whole mackerel"),
     "A whole fish is scored on both sides and roasted at 200C (180C fan) for 20 to 25 minutes "
     "for a 1kg fish, or about 10 minutes for every 2.5cm through the thickest part, with lemon "
     "and herbs in the belly and a little oil rubbed into the skin. It is done when the eye has "
     "gone white and the fin pulls out easily. Sit it on sliced onion or fennel so it does not "
     "stick."),
    (("scallops", "scallop", "king scallops"),
     "Scallops take 1.5 to 2 minutes a side in a very hot pan and no more: pat them dry, salt "
     "them, and put them in when the oil just starts to smoke, then leave them alone until the "
     "edge is golden brown. Wet scallops steam instead of browning, and a crowded pan does the "
     "same. The orange coral is good to eat and wants half the time."),
    (("monkfish",),
     "Monkfish takes 12 to 15 minutes at 200C (180C fan), or 3 to 4 minutes a side in a hot pan: "
     "it is dense and holds together, so a rasher of bacon or a slice of prosciutto wrapped round "
     "it and a squeeze of lemon at the end is all it needs. It is done when it turns opaque white "
     "right through, and unlike cod it will not fall apart if you give it another minute."),
    (("squid", "squid rings", "calamari"),
     "Squid is either 2 minutes or 45: rings, or tubes scored in a diamond pattern, into a very hot "
     "pan for 1 to 2 minutes until they curl and turn opaque, or into a stew or a slow braise for "
     "45 minutes to an hour - anything in between is rubber. Pat them dry first, or they steam "
     "instead of browning."),
    (("crab", "dressed crab", "brown crab"),
     "A cooked crab is picked, not cooked again: twist off the claws, crack them with the back of "
     "a knife, and pull the white meat out of the shell, keeping the brown meat from the body "
     "separate because it is the stronger tasting of the two. A live crab goes into boiling salted "
     "water for about 15 minutes and cools in the water."),
    (("rabbit", "rabbit stew", "wild rabbit"),
     "Rabbit wants either a long braise or a fast roast: jointed and browned, then covered with "
     "stock and cooked at 150C (130C fan) for 1.5 to 2 hours, it comes away from the bone; the "
     "saddle roasted at 200C for 20 to 25 minutes stays moist. It is very lean, so it needs bacon, "
     "wine or a lid to keep it from drying out."),
    (("lamb neck", "neck of lamb", "lamb neck fillet", "neck fillet"),
     "A lamb neck is a braise: brown it, then cook it covered at 150C (130C fan) with stock and "
     "onions for 2 to 2.5 hours until the meat comes off the bone, or 8 hours on low in a slow "
     "cooker. Neck fillet is the quick cut of the same name - 4 to 5 minutes a side in a hot pan, "
     "rested for 5."),
    (("oxtail", "oxtail stew", "ox tail"),
     "Oxtail needs about 3 hours: brown the pieces, then cook them covered at 150C (130C fan) "
     "with stock, onion, carrot and a spoon of tomato until the meat comes away from the bone - "
     "the bone and the gelatine in it are what give the sauce its body. Skim the fat off the top "
     "before serving, and it is better made the day before."),
)

_EXTRA_GUARDS = {
    'lamb chops': ("slow cooker", "casserole", "curry", "roast a leg", "leg of lamb", "shoulder",
                   "joint", "how many", "calories", "cheap", "marinade", "rub"),
    'lamb shank': ("slow cooker", "how many", "calories", "cheap"),
    'gammon steak': ("joint", "joints", "roast", "roasting", "how many", "calories", "cheap",
                     "ham", "bacon", "sausage"),
    'beef brisket': ("steak", "steaks", "joint", "roast joint", "how many", "calories", "cheap",
                     "leftover", "leftovers", "sandwich", "slow cooker", "pressure"),
    'lamb kofta': ("leg of lamb", "shoulder", "roast", "joint", "how many", "calories", "cheap",
                   "slow cooker", "casserole", "curry"),
    'duck legs': ("breast", "breasts", "how many", "calories", "cheap", "whole duck"),
    'liver': ("pate", "pate recipe", "how many", "calories", "cheap", "iron", "pregnant",
              "healthy", "good for"),
    'kidneys': ("pain", "ache", "aches", "stone", "stones", "disease", "infection", "function",
                "failure", "dialysis", "transplant", "doctor", "gp", "hospital", "urine",
                "blood", "protein", "damage", "filter", "how many", "calories", "cheap", "iron",
                "healthy", "good for", "pregnant"),
    'whole duck': ("breast", "breasts", "legs", "leg", "how many", "calories", "cheap",
                   "leftover", "leftovers"),
    'whole fish': ("fishing", "fish tank", "tank", "aquarium", "pond", "fillet", "fillets",
                   "fishcake", "fishcakes", "stock", "monger", "market", "raw", "sashimi",
                   "sushi", "allergy", "shellfish", "how many", "calories", "cheap"),
    'scallops': ("shellfish", "allergy", "allergic", "how many", "calories", "cheap", "frozen",
                 "freezer", "raw", "sashimi", "reef", "seagull", "seagulls"),
    'oxtail': ("how many", "calories", "cheap", "soup", "dog", "dogs"),
    'monkfish': ("how many", "calories", "cheap", "frozen", "mercury", "pregnant", "sustainable"),
    'squid': ("bait", "fishing", "tank", "how many", "calories", "cheap", "frozen", "mercury",
              "pregnant", "restaurant", "menu"),
    'crab': ("hermit", "tank", "pet", "pets", "moulting", "molting", "louse", "lice", "pubic",
             "itch", "itching", "how many", "calories", "cheap", "shellfish", "allergy",
             "allergic", "pregnant", "mercury"),
    'rabbit': ("pet", "pets", "my", "hutch", "hutches", "cage", "litter", "droppings", "sick",
               "ill", "vet", "sneezing", "sneeze", "eating", "feed", "feeding", "fur",
               "neutered", "adopt", "bonded", "how many", "calories", "cheap", "wild",
               "live", "lives", "lived", "lifespan", "life span", "life expectancy",
               "how old"),
    'lamb neck': ("how many", "calories", "cheap", "pain", "stiff", "ache", "aches"),
}

if "whole" not in _cooking_tables.NOT_WANTED.get("fish", ()):
    _cooking_tables.NOT_WANTED["fish"] = ("whole",) + tuple(
        _cooking_tables.NOT_WANTED.get("fish", ()))
_EXTRA_GUARDS['rabbit'] = tuple(_EXTRA_GUARDS['rabbit']) + (
    "look after", "looking after", "care for", "caring for", "should i get", "should we get",
    "shall i get", "thinking of getting", "of getting a", "get a rabbit", "get one",
    "getting one", "own a rabbit", "owning", "new rabbit", "as a pet", "for my son",
    "for my daughter", "for my child", "for a child", "for kids", "for our", "keep a rabbit",
    "keeping a rabbit", "rabbit for", "asking for", "asked for", "wants a", "want a",
    "birthday", "get one as", "have a rabbit", "having a rabbit", "bring home", "need for",
    "needs for", "need to get", "to get a rabbit")

_cooking_tables.NOT_WANTED.update(_EXTRA_GUARDS)
_cooking_tables.BASICS = tuple(_cooking_tables.BASICS) + _EXTRA_BASICS
_STAPLE_NAMES = _STAPLE_NAMES + tuple(
    name for _names, _reply in _EXTRA_BASICS for name in _names)
_RICE_WAS_COOKED = re.compile(
    r"\b(?:cooked|leftover|left over|takeaway|take away|last night|yesterday|in the fridge|"
    r"in the freezer|refrigerated)\b")


_COOKED_RICE_KEEPS = (
    "Cooked rice keeps a day in the fridge and no longer: cool it within an hour of cooking, box "
    "it, and put it in cold. Reheat it once, all the way through until it is steaming hot, and "
    "never a second time - the spores that grow in rice left warm are not killed by reheating. "
    "Rice that sat out overnight goes in the bin, and so does anything that smells or feels "
    "slimy.")


def _the_rice_was_cooked(understood):
    said = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    return bool(_RICE_WAS_COOKED.search(said))


_TAKEN_PERSON = (r"(?:mum|mom|mam|mummy|dad|daddy|father|mother|son|daughter|child|children|"
                 r"kid|kids|baby|wife|husband|partner|boyfriend|girlfriend|friend|mate|"
                 r"brother|sister|cousin|nan|gran|granny|grandma|grandad|grandpa|niece|nephew|"
                 r"aunt|uncle|neighbour|neighbor|family|parents|him|her|them)")
_TAKING_SOMEBODY = re.compile(
    r"\b(?:take|takes|taking|took|taken|bring|brings|bringing|brought)\s+"
    r"(?:(?:my|his|her|our|their|the|a|your)\s+)?" + _TAKEN_PERSON + r"(?!'s)\b")


def _not_a_trip(understood):
    said = (understood.get("norm_text") or understood.get("text") or "").lower()
    return _TAKING_SOMEBODY.search(said) is None


_DAY_BEFORE = ("yesterday", "yesterdays", "last night", "this morning", "the day before",
               "day before", "the day after", "day after", "day later", "a day later",
               "days ago", "a couple of days ago", "2 days ago", "two days ago")

_ON_A_FLIGHT = ("plane", "planes", "flight", "flights", "flying", "airport", "airports",
                "security", "hand luggage", "carry on", "carry-on", "cabin bag", "cabin")

_OTHER_PEOPLE_AT_LUNCH = re.compile(
    r"\b(?:everyone|everybody|friends?|parents?|relatives?|"
    r"in\s?laws?|guests?|visitors?|"
    r"(?:people|folk) (?:coming|over|round|for|at)|having people|"
    r"for (?:\d+|three|four|five|six|seven|eight|nine|ten|twelve|twenty) "
    r"(?:people|adults|guests|kids|children))\b")
_PACKED_LUNCH_NOUNS = ("packed lunch", "packed lunches", "lunchbox", "lunchboxes",
                       "lunch box", "lunch boxes", "school lunch", "school lunches",
                       "work lunch", "lunch for work", "lunch to take", "take to work",
                       "take for lunch", "pack up", "packed up", "packup")


def _one_persons_lunch(understood):
    if not understood:
        return False
    lines = [str(understood.get(field) or "").lower() for field in ("text", "clean")]
    if not any(lines):
        lines = [" ".join(str(word) for word in understood.get("words") or ()).lower()]
    for said in lines:
        if any(noun in said for noun in _PACKED_LUNCH_NOUNS):
            return True
        if _OTHER_PEOPLE_AT_LUNCH.search(said):
            return False
        table = _crowd(said)
        if table >= 6 or (table >= 3 and "of us" in said):
            return False
    return True


_FREEZE_WORDS_NOT_IN_FACTS = ("blackberries", "cherries", "cooked pasta", "soup")
_FREEZE_KEEPS_ITS_KEEPING = ("ginger",)
_FREEZE_FOOD_WORDS = tuple(sorted(
    ({str(_name).lower() for _names, _fact in FREEZE_FACTS for _name in _names}
     | set(_FREEZE_WORDS_NOT_IN_FACTS))
    - set(_FREEZE_KEEPS_ITS_KEEPING)))
_FREEZE_POINTING_WORDS = ("it", "this", "that", "these", "those", "them", "the rest", "the other half",
                          "the remainder", "whats left", "what is left", "the spare", "some",
                          "any left", "any spare", "a portion", "the leftovers")

_FREEZE_ASKS = ("can i freeze", "can you freeze", "can we freeze", "could i freeze",
                "should i freeze", "do i freeze", "how do i freeze", "how to freeze",
                "how long can i freeze", "how long do i freeze", "is it ok to freeze",
                "is it okay to freeze", "is it alright to freeze", "is it safe to freeze",
                "is it fine to freeze", "will it freeze", "will this freeze", "will they freeze",
                "will that freeze", "would it freeze", "do i need to freeze",
                "does it freeze", "does this freeze", "can this be frozen", "can it be frozen",
                "can that be frozen", "can these be frozen", "can they be frozen",
                "is it freezable", "is this freezable", "ok to freeze", "freezes well",
                "freeze well", "goes in the freezer", "put it in the freezer",
                "put this in the freezer", "keep it in the freezer", "can i keep it frozen")

_AGE_WORDS = ("year old", "years old", "year-old", "years-old", "yearold", "yearsold",
              "month old", "months old", "month-old", "months-old", "monthold", "monthsold",
              "week old", "weeks old", "week-old", "weeks-old", "weekold", "weeksold")


def _open_wine(memory, understood):
    line = " " + (understood.get("clean") or "") + " "
    if any(word in line for word in (" screw cap", " screwcap", " cap ", " caps ", " cap,",
                                     " cap.", " cap?")):
        return ("A screw cap just twists off with a crack, and the ring stays on the neck - no "
                "corkscrew, and the cap goes back on between glasses. If it will not turn, hold the "
                "top still and turn the bottle.")
    if any(word in line for word in (" prosecco", " champagne", " sparkling", " cava", " fizz",
                                     " bubbly", " sekt", " cremant")):
        return ("Chill it, then hold the cork and turn the bottle rather than the cork, pointing it "
                "away from people and anything breakable, and let it sigh out rather than bang. "
                "Sparkling wine is opened cold and slowly because the gas is the wine.")
    return ("Cut the foil below the rim, then stand the bottle on the table and turn the corkscrew "
            "into the middle of the cork; lever it out in two stages on the hinge and ease the last "
            "bit by hand so it does not pop. If the cork is dry and stubborn, wrap the neck in a warm "
            "cloth for a minute first. A screw cap simply twists off.")

_SHORTAGE_ASK = ("ran out", "run out", "im out of", "i'm out of", "were out of", "are out of",
                 "we're out of", "all out of", "none left", "havent got", "haven't got",
                 "got none", "have none", "no rice left", "no pasta left",
                 "no potatoes left", "no spuds", "out of rice", "out of pasta",
                 "out of potatoes", "out of spuds")

_STAPLE_METHOD_AVOID = ("cook", "cooking", "cooked", "how long", "how much",
                        "how many", "recipe", "recipes", "method", "instructions", "best way",
                        "boil", "boiling", "boiled", "roast", "roasting", "bake", "baking",
                        "fry", "frying", "steam", "microwave")
def _porridge(memory, understood):
    said = str(understood.get("clean") or understood.get("text") or "").lower()
    if "microwave" in said or "microwaving" in said or "micro" in said.split():
        return ("Put 40g of porridge oats in a big bowl with 250ml of milk or water - a big bowl, "
                "because it climbs the sides - and microwave it on high for 2 minutes. Stir it, "
                "then give it another 30 seconds to a minute until it is as thick as you like; it "
                "thickens more as it stands, so stop while it still looks a little loose. A pinch "
                "of salt and a spoon of honey or jam at the end.")
    return ("Simmer 1 part oats to 3 parts liquid for 5 minutes, stirring now and then, and add a "
            "pinch of salt; that gives creamy porridge rather than lumps. Milk added at the end "
            "keeps it creamier than cooking it all in milk. In a microwave, a single bowl takes 2 "
            "minutes on high, stirred halfway; stop early, as it thickens as it stands.")
STOCK_BROWN = ("beef", "lamb", "pork", "veal", "oxtail", "venison", "mutton", "game", "ham")
STOCK_FISH = ("fish", "prawn", "prawns", "seafood", "shellfish", "salmon", "cod", "haddock",
              "trout", "mackerel")
STOCK_VEG = ("vegetable", "veg", "veggie", "mushroom", "mushrooms", "peelings", "scraps",
             "vegan", "vegetarian", "without bones", "no bones", "no meat")

STOCK_METHODS = {
    "chicken": (
        "Chicken or turkey stock simmers 1.5 to 2 hours at the barest bubble, and 3 if you "
        "want it stronger. Skim the grey foam off in the first twenty minutes and keep the "
        "lid off so it never boils hard, then strain it through a sieve. Cool it fast in a "
        "sink of cold water, which takes about an hour, and it keeps 4 days in the fridge or "
        "3 months frozen.",
        "Cover the picked carcass with cold water, add an onion, a carrot, a bay leaf and a few "
        "peppercorns, bring it to the barest simmer and skim the grey foam off in the first "
        "twenty minutes; 2 hours is plenty, 3 if you want it stronger. Strain it, cool it in a "
        "sink of cold water for about an hour, and it keeps 4 days in the fridge or 3 months "
        "frozen."),
    "brown": (
        "Beef, lamb or pork stock wants 3 to 4 hours at the barest simmer, after half an hour "
        "of browning the bones in a hot oven. It should set like jelly when it is cold, which "
        "is what tells you the bones were worth the time.",
        "Brown the bones with the onion and carrot halved at 220C (200C fan) for 30 minutes "
        "first, because the colour and most of the flavour come from that browning. Then cover "
        "them with cold water, add a bay leaf and a few peppercorns and simmer at the barest "
        "bubble for 3 to 4 hours, skimming the foam in the first twenty minutes. Strain it, and "
        "it keeps 4 days in the fridge or 3 months frozen."),
    "fish": (
        "Fish stock takes 20 to 30 minutes at a bare simmer and no longer - after that the bones "
        "turn it bitter and gluey. Skim the foam, don't stir it, and strain it through kitchen "
        "paper.",
        "Fish stock is the quick one: fish bones and trimmings with an onion, a carrot, a bay "
        "leaf and a few peppercorns, covered with cold water and simmered 20 to 30 minutes and "
        "no longer. Strain it through a sieve lined with kitchen paper, and it keeps 2 days in "
        "the fridge or 3 months frozen."),
    "veg": (
        "Vegetable stock simmers 30 to 40 minutes, and longer than that the sweetness goes "
        "muddy. Leave out the strong greens - cabbage, broccoli, cauliflower, beetroot - and "
        "season it at the end.",
        "Vegetable stock needs no bones at all: an onion, a carrot, a stick of celery, a bay "
        "leaf and a few peppercorns in cold water, simmered 30 to 40 minutes. Leave out "
        "cabbage, broccoli, cauliflower and beetroot, which turn it bitter and sour, put soft "
        "herbs in at the end, and it keeps 4 days in the fridge or 3 months frozen."),
}

STOCK_KEEP = (
    "Homemade stock keeps 4 days in the fridge and 3 months in the freezer. Cool it fast, get "
    "it into the fridge within 2 hours, freeze it in bags laid flat or in an ice cube tray for "
    "spoonfuls, and bring it back to a rolling boil before you eat it. A cube or a carton "
    "follows the date on the pack.")
STOCK_CUBES = (
    "A stock cube makes about 450ml of stock, one cube to a pint of water, and they are salty, "
    "so taste before you add any salt. Crumble it into hot water rather than dropping it in "
    "whole, and use half for a small pan of rice or gravy. Fresh stock in a tub beats a cube "
    "whenever the stock is the point of the dish.")
STOCK_CUBE_KEEP = (
    "A stock cube keeps its flavour for about a year in a dry cupboard, and the date on the box "
    "is the honest guide. Once the foil is open, wrap the rest or keep it in a sealed tub, "
    "because a cube that takes in damp goes hard and clumps; a soft one is still fine to use.")
STOCK_SKIM = (
    "Skim the grey foam off in the first twenty minutes with a spoon or a ladle, and keep the "
    "pot at the barest simmer with the lid off. The foam is blood and protein: it tastes flat "
    "and it is what clouds a stock, and after twenty minutes there is nothing left to skim. "
    "Don't stir the pot, or the fat mixes back in.")
STOCK_SLOW = (
    "In a slow cooker, cover the bones and vegetables with cold water and cook on low for 6 to "
    "8 hours, or high for 3 to 4, then strain it. Brown the bones in the oven first or the "
    "flavour is thin, and keep the liquid an inch below the lid. A slow cooker stock is weaker "
    "than a simmered one, so reduce it by a third before you freeze it.")
STOCK_FLAVOUR = (
    "Flavour comes from browning: roast the bones and the vegetables at 220C (200C fan) for 30 "
    "minutes before they go in the pot, and add a spoon of tomato puree or a few dried "
    "mushrooms. Don't let it boil, which drives the aroma off, and salt it only at the end. "
    "Reduce the strained stock by half and you have a stronger one for the freezer.")
STOCK_HEALTH = (
    "Stock is flavour, not medicine: it has some minerals and collagen from the bones, but the "
    "evidence for the joint and skin claims is thin, and a stock cube is mostly salt. "
    "Homemade with little or no salt is the useful version of it, and it is the cheapest way "
    "to make a soup or a stew taste of something.")
STOCK_AMOUNT = (
    "A litre of stock to 300g of risotto rice, added a hot ladle at a time; about 500ml for a "
    "soup for two; and enough to cover the bones in the pot by an inch. Whatever is left "
    "freezes in a bag, so make more than you need.")

STOCK_AVOID = (
    "share", "shares", "market", "markets", "invest", "investing", "investor",
    "investors", "trade", "trading", "trader", "portfolio", "index fund", "isa",
    "dividend", "dividends", "price", "prices", "worth", "buy", "buying", "bought",
    "sell", "selling", "sold", "company", "companies", "ftse", "nasdaq", "wall street",
    "crash", "crashed", "crypto", "bitcoin", "pension", "profit",
    "earnings", "valuation", "penny", "equities", "equity", "broker", "stockbroker",
    "in stock", "out of stock", "stock up", "stocking up", "christmas stocking",
    "cloudy", "clouded", "murky", "sediment",
    "broke", "broken", "fracture", "fractured", "sprain", "sprained", "hurt", "hurts",
    "ache", "aches", "pain", "pains", "swollen", "x-ray", "xray", "bone density",
    "osteoporosis", "arthritis", "bone meal", "garden", "plant", "plants", "soil",
    "compost", "fertiliser", "fertilizer")


def _stock_answer(memory, understood):
    said = [str(word).lower() for word in (understood.get("words") or [])]
    if not said:
        return None
    line = " %s " % " ".join(said)

    def says(*words):
        return any(" %s " % word in line for word in words)

    if says(*STOCK_VEG):
        kind = "veg"
    elif says(*STOCK_FISH):
        kind = "fish"
    elif says(*STOCK_BROWN):
        kind = "brown"
    else:
        kind = "chicken"
    time_reply, method = STOCK_METHODS[kind]
    cubes = says("cube", "cubes", "granule", "granules", "bouillon")
    keeps = says("keep", "keeps", "keeping", "keep it", "store", "storing", "last", "lasts",
                 "freeze", "freezes", "freezing", "frozen", "freezer", "fridge", "use by",
                 "go off", "gone off", "out of date", "expire", "expired", "best before")
    if cubes and keeps:
        return STOCK_CUBE_KEEP
    if cubes:
        return STOCK_CUBES
    if keeps:
        return STOCK_KEEP
    if says("slow cooker", "crockpot", "crock pot", "pressure cooker", "slow"):
        return STOCK_SLOW
    if says("skim", "skimming", "scum", "foam", "froth"):
        return STOCK_SKIM
    if says("healthy", "healthier", "good for", "benefit", "benefits", "collagen",
            "nutritious", "nutrition"):
        return STOCK_HEALTH
    if says("flavour", "flavor", "taste", "tastes", "bland", "better", "stronger",
            "strong", "rich", "richer"):
        return STOCK_FLAVOUR
    if says("how much", "how many"):
        return STOCK_AMOUNT
    if says("how long", "long", "hours", "hour", "minutes", "minute", "time", "simmer",
            "simmering", "boil", "boiling", "cook", "cooking"):
        return time_reply
    return method


_SMOKE_THINGS = ("brisket", "ribs", "rib", "pulled pork", "pork", "shoulder", "chicken", "turkey",
                 "wings", "sausage", "sausages", "salmon", "trout", "mackerel", "haddock", "fish",
                 "cheese", "tofu", "beef", "steak", "lamb", "duck")

_SMOKE_REPLIES = {
    "brisket": (
        "Brisket is low and slow: 110 to 120C at the lid, a couple of chunks of oak or hickory, "
        "and about 1.5 hours per kg - a 4kg joint is 9 to 11 hours - until it probes 93 to 95C "
        "inside. Wrap it in foil or butcher paper once the bark is dark and set, and rest it an "
        "hour before slicing."),
    "ribs": (
        "Pork ribs take 110 to 120C for four to six hours, until the meat has pulled back from the "
        "bone and the rack bends without breaking. Rub them with salt, sugar and paprika the night "
        "before, and only sauce them in the last 20 minutes or the sugar burns."),
    "chicken": (
        "Smoke chicken at 130 to 140C rather than lower, so the skin renders instead of going "
        "rubbery: about two hours for a whole bird, and off the heat at 74C in the thickest part "
        "of the thigh. Smaller pieces take 45 minutes to an hour."),
    "salmon": (
        "Hot-smoke salmon at 120C for 45 minutes to an hour, after an hour in a salt-and-sugar "
        "brine so it stays moist and the white protein does not leak out. Cold-smoking is a "
        "different job and needs a cure and a much cooler box."),
    "cheese": (
        "Smoke cheese at 90 to 110C for 30 to 45 minutes - long enough to take the colour, not "
        "long enough to melt it - and let it firm up in the fridge for a day before eating."),
    "default": (
        "Low and slow is the rule: 110 to 120C at the lid, with the meat off the direct heat, and "
        "time by thickness rather than by the clock - beef to 93 to 95C so it pulls, chicken to "
        "74C, pork ribs four to six hours. Keep the lid down, and a couple of chunks of wood is "
        "plenty; more than that turns it bitter."),
}


_SMOKING_WORDS = {"smoke", "smokes", "smoked", "smoking", "smoker", "smokers", "bbq",
                  "barbecue", "barbeque", "woodchips", "pellet", "pellets"}
_SMOKING_PHRASES = ("hot smoke", "cold smoke", "wood chips", "low and slow", "pellet grill",
                    "smoke it", "smoke them", "smoke a ", "smoke an ")


def _asks_about_a_smoker(reading):
    said = str((reading or {}).get("text") or "").lower()
    words = set(re.findall(r"[a-z']+", said))
    if "smoked" not in words:
        return True
    if words & {word for word in _SMOKING_WORDS if word != "smoked"}:
        return True
    return any(phrase in said for phrase in _SMOKING_PHRASES)


def _smoke_food(memory, reading):
    words = {str(word).lower() for word in (reading.get("words") or ())}
    for name in _SMOKE_THINGS:
        if name in words:
            if name in ("rib",):
                name = "ribs"
            elif name in ("pulled pork", "pork", "shoulder"):
                name = "ribs" if "rib" in words else "default"
            elif name in ("turkey", "wings"):
                name = "chicken"
            elif name in ("trout", "mackerel", "haddock", "fish"):
                name = "salmon"
            elif name in ("sausage", "sausages", "tofu", "beef", "steak", "lamb", "duck"):
                name = "default"
            return _SMOKE_REPLIES[name]
    return _SMOKE_REPLIES["default"]


SHORT_OF_THE_HOUSE = re.compile(
    r"\b(?:no|without|out of|ran out of|run out of|none left|nothing left|havent got|"
    r"haven't got|havent any|haven't any|dont have|don't have|didnt have|didn't have|"
    r"not got any|got none)\s+(?:\w+\s+){0,2}(?:%s)\b")


def _not_short_of(*foods):
    pattern = re.compile(SHORT_OF_THE_HOUSE.pattern % "|".join(foods))

    def guard(understood):
        said = str((understood or {}).get("text") or "").lower()
        return not pattern.search(said)
    return guard


def _make_it(nouns, props):
    out = []
    for noun in nouns:
        for prop in props:
            out.extend(("make " + noun + " " + prop, "make my " + noun + " " + prop))
    return tuple(out)


_CHEESE_TROUBLE_WORDS = ("mould", "mouldy", "mold", "moldy", "gone off", "out of date", "off",
                         "smell", "smells", "smelt", "slimy", "ammonia", "blue", "green",
                         "fuzzy", "furry", "spots", "bits", "still ok", "ok to eat",
                         "safe to eat", "can i eat", "is it ok")


_CHEESE_KIND_KEEP = {
    "soft": "Soft cheese like brie or camembert keeps about a week once opened - wax paper, then "
            "loosely in a bag in the warmest part of the fridge - and a soft one that grows mould "
            "goes in the bin whole, because the threads run right through it.",
    "blue": "Blue cheese keeps about two weeks once opened, in wax paper in the warmest part of "
            "the fridge. The blue veins are meant to be there; green or white fuzz is not, and it "
            "does not come off a blue.",
    "hard": "Hard cheese like a cheddar keeps about two weeks once opened, wrapped in wax paper in "
            "the warmest part of the fridge, and it dries out before it spoils.",
}


def _the_kind_of_cheese_named(said):
    from .keeping import BLUE_CHEESES, CHEESE_NAMES, SOFT_CHEESES

    for kind, names in (("blue", BLUE_CHEESES), ("soft", SOFT_CHEESES)):
        if any(" %s" % name in said for name in names):
            return kind
    if any(" %s" % name in said for name in CHEESE_NAMES):
        return "hard"
    return ""


def _not_a_serving_frame(reading):
    from . import dishes
    text = str((reading or {}).get("clean") or (reading or {}).get("text") or "").lower()
    return not dishes.asks_for_a_side_of_a_food(text)


def _cheese_keep(memory, reading):
    said = " %s " % str(reading.get("clean") or "").lower()
    if any(" %s " % word in said or said.strip().startswith(word)
           for word in _CHEESE_TROUBLE_WORDS):
        return ("Cut the mould off hard cheese with a good inch to spare and it is fine to eat; "
                "bin soft cheese, cream cheese and anything grated that has mould on it. To keep "
                "the rest, wrap it in wax paper or baking paper and then loosely in a bag, and "
                "keep it in the warmest part of the fridge: cling film makes it sweat and go "
                "slimy.")
    kind = _the_kind_of_cheese_named(said)
    if kind:
        return _CHEESE_KIND_KEEP[kind]
    return ("To keep cheese, wrap it in wax paper or baking paper and then loosely in a bag, in "
            "the warmest part of the fridge. A hard wedge keeps about two weeks once opened. "
            "Soft cheese keeps about a week once opened, and cling film sweats it and makes it "
            "slimy, so leave it in the tub it came in.")


MAKE_IT_THICK = _make_it(("soup", "stew", "sauce", "gravy", "curry", "chilli", "casserole"),
                         ("thick", "thicker"))
_OATS_HEALTH = ("healthy", "healthier", "healthiest", "good for me", "good for you",
               "nutritious", "nutrition", "diet", "dieting", "slimming", "lose weight",
               "put on weight", "filling", "fattening", "calories", "sugar")


def _overnight_oats(memory, reading):
    said = str(reading.get("clean") or "").lower()
    if any(word in said for word in _OATS_HEALTH):
        return ("As healthy as what you put in the jar: oats are a slow-carb breakfast and the "
                "milk or yoghurt adds protein, so a portion with fruit keeps you full till lunch. "
                "The sugar comes from the honey, syrup and dried fruit, so go easy on those - and "
                "a shop-bought pot can carry a lot of it. Make it yourself and it is one of the "
                "better breakfasts going.")
    return _OVERNIGHT_OATS_RECIPE


_OVERNIGHT_OATS_RECIPE = (
    "Overnight oats are soaked in the fridge, not cooked: about 1 part oats to 1 to 1.5 parts "
    "milk or yoghurt in a jar, left 6 hours or overnight, then eaten cold with fruit. Rolled "
    "oats are the ones that work - steel-cut stay chewy and instant oats go to mush - and a "
    "spoon of chia or a grated apple thickens them. You do not need to soak oats before "
    "cooking porridge; 5 minutes in a pan does that.")



NO_SUGAR = ("sugar free", "sugar-free", "without sugar", "no sugar", "no added sugar",
            "sugar substitute", "sugar substitutes", "sweetener", "sweeteners")


TEA_MILK_ORDER = (
    "Tea first, milk last, in a mug: you can see how strong the tea has got before you pour, and "
    "the leaves brew in water at full heat instead of water cooled by milk. Milk first is the old "
    "way with a pot and a thin china cup - a splash of milk stopped boiling water cracking the "
    "china, and it stretched a small amount of tea - so it is not wrong, just fussier, and the "
    "bottom of the cup ends up milky unless you stir.")
TEA_MILK_KIND = (
    "Semi-skimmed is the usual: whole milk tastes rounder, skimmed thinner, and both are fine. "
    "Of the plant milks, oat and soy are the closest to it.")
TEA_MILK_AMOUNT = (
    "A splash: about 15 to 30ml, a tablespoon or two, in a 250ml mug. Taste it at 10ml, because "
    "you cannot take it out, and a strong builder's tea takes more than a mild one.")
TEA_MILK_PLANT = (
    "Oat milk is the nearest to dairy in tea and the one that behaves best - the barista ones are "
    "made not to split. Soy is fine but can taste beany in a strong cup, almond is thin, and "
    "coconut changes the taste. Pour it in after the water and stir.")

TEA_MILK_AMOUNT_ASKS = ("how much milk", "much milk", "how many ml", "how many mls",
                        "how much of it", "quantity of milk", "how milky", "how strong")
TEA_MILK_KIND_ASKS = ("what milk", "which milk", "best milk", "what kind of milk",
                      "what type of milk", "milk is best", "milk should i use", "milk to use",
                      "milk do you use", "milk is good", "milk good in tea", "oat milk",
                      "soy milk", "soya milk", "almond milk", "plant milk", "skimmed milk",
                      "semi skimmed", "whole milk", "milky")

TEA_MILK_PLANT_SAID = ("oat milk", "soy milk", "soya milk", "almond milk", "plant milk",
                       "plant-based milk", "coconut milk", "nut milk")

TEA_MILK_ASK = ("how", "how much", "how many", "what", "which", "what's", "should",
                "should i", "can i", "could i", "do i", "does", "is", "are", "would",
                "will", "best", "first", "last", "before", "after", "order", "stir",
                "go in", "goes in", "put in", "instead",
                "in tea", "in my tea", "in the tea", "in a cup of tea", "in a mug of tea",
                "in a brew", "in my brew", "for tea", "for my tea", "for a cup of tea",
                "with tea", "with my tea", "with a cup of tea")


_TEA_MILK_DISH = ("egg", "eggs", "scrambled", "omelette", "omelettes", "flour", "batter",
                  "pancake", "pancakes", "dough", "biscuit", "biscuits", "chocolate",
                  "cocoa", "butter", "yoghurt", "yogurt", "gravy", "soup", "dumpling",
                  "dumplings", "bake", "baking", "baked", "filling", "icing", "frosting",
                  "meringue")

_TEA_MILK_PAN = _TEA_MILK_DISH + ("porridge", "oats", "oatmeal", "custard", "mash", "mashing",
                                  "sauce", "roux", "curry", "stew", "souffle", "quiche")

_TEA_MILK_BREW = ("tea", "teas", "teabag", "teabags", "tea bag", "tea bags", "brew",
                  "brews", "brewing", "cuppa", "cuppas", "kettle", "teapot", "pot of tea",
                  "cup of tea", "mug of tea", "mug", "cup", "hot water")


def _a_thread_of_a_pan(memory):
    if not isinstance(memory, dict):
        return False
    words = []
    for turn in (memory.get("topics") or [])[-2:]:
        if not isinstance(turn, dict):
            continue
        words.extend(turn.get("words") or ())
        words.extend(str(turn.get("text") or "").split())
    plan = (memory.get("user") or {}).get("plan")
    if isinstance(plan, str):
        words.extend(plan.split())
    low = " " + " ".join(str(word).lower() for word in words) + " "
    return any(f" {dish} " in low for dish in _TEA_MILK_PAN)


MILK_FOR_COFFEE_KIND = (
    "In coffee, oat is the plant milk that behaves best - the barista cartons are made not to "
    "split, and they foam. Soy is next and tastes slightly beany in a long black; almond is thin "
    "and can separate in hot coffee; coconut changes the taste of the cup. Whole milk foams the "
    "thickest and semi-skimmed is the usual for a flat white, and a splash of milk in black coffee "
    "takes the edge off without much milk at all.")
MILK_FOR_COFFEE_AMOUNT = (
    "A splash: about 20 to 40ml in a mug of filter coffee, a tablespoon or two, and 100 to 150ml "
    "in a latte or a cappuccino, where the milk is most of the cup. Pour it in after the coffee so "
    "you can see how dark it has gone, and heat the milk for a milky drink - cold milk takes the "
    "heat out of a small cup.")
MILK_FOR_COFFEE_SPLIT = (
    "Milk splits in coffee because the coffee is hot and acidic: the acid takes the milk towards "
    "the point where its proteins clump, and the heat sets the clumps, which is why the specks "
    "appear in a long black and not in a latte. Let the coffee cool for a minute before the milk "
    "goes in, use the fresher bottle, and use a barista plant milk if it keeps happening - those "
    "have oil and a stabiliser added so they hold together.")


def _the_milk_for_a_coffee(memory, understood):
    text = " " + ((understood or {}).get("clean") or "").lower() + " "
    if any(said in text for said in ("curdl", " split ", " split,", " splits ", " splitting ",
                                     " separated ", " separates ", " gone lumpy ",
                                     " lumps in ")):
        return MILK_FOR_COFFEE_SPLIT
    if any(said in text for said in ("how much", "how many ml", "how many mls", "how milky",
                                     "much milk", "much of it")):
        return MILK_FOR_COFFEE_AMOUNT
    return MILK_FOR_COFFEE_KIND


def _tea_milk_reply(memory, understood):
    text = " " + ((understood or {}).get("clean") or "").lower() + " "
    if not any(f" {word} " in text for word in _TEA_MILK_BREW) and _a_thread_of_a_pan(memory):
        return None
    amount = any(ask in text for ask in TEA_MILK_AMOUNT_ASKS)
    kind = any(ask in text for ask in TEA_MILK_KIND_ASKS)
    plant = any(f" {said} " in text for said in TEA_MILK_PLANT_SAID)
    if amount:
        return TEA_MILK_AMOUNT + " " + (TEA_MILK_PLANT if plant else TEA_MILK_KIND)
    if kind:
        return TEA_MILK_KIND + (" " + TEA_MILK_PLANT if plant else "")
    if plant:
        return TEA_MILK_PLANT
    return TEA_MILK_ORDER

SWAP_NOT_A_MEAL = ("what can i have for breakfast", "what should i have for breakfast",
                   "what shall i have for breakfast", "what can i make for breakfast",
                   "what can i eat for breakfast", "what to have for breakfast",
                   "ideas for breakfast", "breakfast ideas", "breakfast idea",
                   "what can i have for lunch", "what should i have for lunch",
                   "what shall i have for lunch", "what can i make for lunch",
                   "what can i eat for lunch", "what to have for lunch",
                   "ideas for lunch", "lunch ideas", "packed lunch", "lunchbox",
                   "lunch box",
                   "what can i have for dinner", "what should i have for dinner",
                   "what shall i have for dinner", "what can i make for dinner",
                   "what can i eat for dinner", "what to have for dinner",
                   "what can i have for tea", "what should i have for tea",
                   "what can i make for tea", "what can i eat for tea", "what to have for tea",
                   "what can i have for supper", "what can i make for supper",
                   "ideas for dinner", "dinner ideas", "ideas for tea", "tea ideas",
                   "ideas for supper")


_A_SUPPLY_VERB = ("using", "adding", "putting", "having", "eating", "including",
                  "containing", "needing", "buying", "serving", "cooking", "mixing")
_A_ITS_OWN_FAULT = ("sticking", "stick")
_A_WITHOUT_SUBJECT = ("it", "them", "that", "this", "they", "you", "me", "him", "her",
                      "the", "a", "an", "my", "his", "its", "their", "your", "our")


def _an_outcome(word):
    if word in _A_ITS_OWN_FAULT:
        return False
    return word.endswith("ing") and word not in _A_SUPPLY_VERB


def _a_swap_and_not_a_step(understood):
    clean = str((understood or {}).get("clean") or "")
    words = re.sub(r"[^a-z0-9' ]+", " ", clean.lower()).split()
    seen = False
    for index, word in enumerate(words):
        if word != "without":
            continue
        seen = True
        after = words[index + 1:index + 4]
        if not after:
            continue
        if after[0] in _A_WITHOUT_SUBJECT:
            if any(_an_outcome(word) for word in after[1:]):
                continue
            return True
        if _an_outcome(after[0]):
            continue
        return True
    return not seen


def _swap(entry_id, key, reply, **rest):
    avoid = tuple(rest.pop("avoid", ()) or ())
    guard = rest.pop("guard", None)
    if guard is not None:
        rest["guard"] = lambda understood: _a_swap_and_not_a_step(understood) and guard(understood)
    else:
        rest["guard"] = _a_swap_and_not_a_step
    return entry(entry_id, key, reply, avoid=SWAP_NOT_A_MEAL + avoid, **rest)




def _said_to_be_missing(clean):
    words = re.sub(r"[^a-z0-9' ]+", " ", str(clean or "").lower()).split()
    missing = set()
    for index, word in enumerate(words):
        if word == "without":
            missing.update(words[index + 1:index + 4])
    return missing


def _leaves_out(*ingredients):
    stems = set()
    for one in ingredients:
        stems.add(one)
        stems.add(one[:-1] if one.endswith("s") else one + "s")

    def guard(understood):
        said = _said_to_be_missing((understood or {}).get("clean"))
        return not any(word in stems for word in said)

    return guard

BREAD_KEEP = ("Keep bread at room temperature in a paper bag or a bread bin, not the fridge: the "
              "cold makes it go stale faster. Freeze what you won't eat in two days, sliced, and "
              "bring a stale loaf back with a splash of water and 5 minutes in a hot oven.")
BREAD_LIFE = ("A loaf keeps 3 to 4 days in a paper bag or a bread bin at room temperature, and 3 "
              "months sliced in the freezer. The fridge stales it faster than the cupboard, so "
              "leave it out and cut slices as you need them, freeze what you won't eat in two "
              "days, and a stale loaf comes back with a splash of water and 5 minutes in a hot "
              "oven.")
BREAD_DATED = ("Bread a day or two past the date is fine if it looks and smells all right: a loaf goes "
               "dry or hard before it goes unsafe, and 5 minutes in a hot oven brings it back. "
               "Don't cut the mould off and eat the rest - the threads reach further than the "
               "green you can see, so bin that loaf. Keep it in a paper bag or a bin at room "
               "temperature rather than the fridge, and freeze half sliced.")


_A_SEASON_OF_A_SHOW = re.compile(
    r"\b(?:season\s*(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten)|this season"
    r"|next season|last season|new season|final season|first season|second season"
    r"|episodes?|series|box set|binge|the show|on tv|on netflix|netflix|streaming"
    r"|football|cricket|rugby|premier league|the league|leagues|fixtures?|match|matches"
    r"|team|teams|gym|what should i watch)\b")


def _not_a_season_of_a_show(understood):
    said = " " + " ".join(str((understood or {}).get(key) or "")
                          for key in ("clean", "norm_text", "norm")).lower() + " "
    return not _A_SEASON_OF_A_SHOW.search(said)


def _bread_kept(memory, understood):
    said = " ".join(str((understood or {}).get(key) or "")
                    for key in ("clean", "norm_text", "norm")).lower()
    if any(word in said for word in PACK_DATE) or "the date" in said:
        return BREAD_DATED
    if re.search(r"\bhow long\b|\bhow many days\b|\bhow many weeks\b"
                 r"|\bshelf[- ]?life\b|\blasts? for\b", said):
        return BREAD_LIFE
    return BREAD_KEEP
NO_SANDWICH = ("that isnt a sandwich", "that isnt sandwiches", "that isnt a sandwich or",
               "that isint a sandwich", "that is not a sandwich", "that is not sandwiches",
               "that isnt just sandwiches", "isnt a sandwich", "isnt sandwiches",
               "isn't a sandwich", "isn't sandwiches", "not a sandwich", "not sandwiches",
               "no sandwich", "no sandwiches", "without a sandwich", "without sandwiches",
               "with no sandwiches", "with no bread", "not bread", "no bread", "without bread",
               "other than sandwiches", "other than a sandwich", "besides sandwiches",
               "besides a sandwich", "apart from sandwiches", "apart from a sandwich",
               "instead of sandwiches", "instead of a sandwich", "not always sandwiches",
               "sick of sandwiches", "bored of sandwiches", "hates sandwiches",
               "wont eat sandwiches", "won't eat sandwiches", "doesnt want sandwiches",
               "wont eat bread", "won't eat bread", "doesnt eat bread", "does not eat bread",
               "refuses bread", "wont eat a sandwich", "wont eat a sandwich or",
               "hates bread", "no more sandwiches", "sick of bread", "bored of bread",
               "off sandwiches", "gone off sandwiches")


_NO_SANDWICH_KID_ITEMS = (
    ("cooked pasta or rice from last night's dinner in a tub", "gluten pasta"),
    ("cheese cubes", "dairy cheese"),
    ("a boiled egg", "egg"),
    ("crackers or oatcakes", "gluten cracker crackers"),
    ("veg sticks with hummus", "sesame hummus"),
    ("a yoghurt", "dairy yoghurt"),
    ("some fruit", ""),
)
_NO_SANDWICH_ADULT_ITEMS = (
    ("last night's dinner in a tub", ""),
    ("pasta or rice salad", "gluten pasta"),
    ("cold chicken", "meat chicken"),
    ("cheese with oatcakes", "dairy cheese gluten oatcake oatcakes"),
    ("a boiled egg", "egg"),
    ("veg sticks and hummus", "sesame hummus"),
    ("soup in a flask", ""),
    ("yoghurt and fruit", "dairy yoghurt"),
    ("fruit", ""),
)


def _a_lunchbox_without(items, banned):
    return [food for food, words in items if not (set(words.split()) & banned)]


CHILD_NAMES = frozenset((
    "son", "daughter", "child", "children", "kid", "kids", "baby", "toddler", "boy", "girl",
    "stepson", "stepdaughter", "grandson", "granddaughter", "nephew", "niece", "schoolchild",
    "schoolboy", "schoolgirl", "little one", "youngest", "eldest"))
CHILDS_LUNCH_WORDS = ("lunchbox", "lunchboxes", "lunch box", "lunch boxes", "pack up",
                      "packed up", "his lunch", "her lunch", "his bag", "her bag")


def _lunch_is_for_a_child(memory, said):
    whole = set(str(said or "").split())
    if whole & CHILD_NAMES:
        return True
    if any(phrase in said for phrase in CHILDS_LUNCH_WORDS):
        return True
    if not isinstance(memory, dict):
        return False
    person = memory.get("person")
    who = str((person or {}).get("who") or "").strip().lower() if isinstance(person, dict) else ""
    if who in CHILD_NAMES:
        return True
    people = (memory.get("user") or {}).get("people") if isinstance(memory.get("user"), dict) else ()
    for one in people or ():
        if str(one).strip().lower() in CHILD_NAMES:
            return True
    return False


def _said_no_sandwich(memory):
    if not isinstance(memory, dict):
        return False
    turns = memory.get("turns")
    for turn in list(turns or [])[-4:]:
        line = str((turn or {}).get("user") if isinstance(turn, dict) else "").lower()
        if any(phrase in line for phrase in NO_SANDWICH):
            return True
    return False


def _lunch_ideas_after_a_no(memory, understood):
    reply = _lunch_ideas(memory, understood)
    offers_one = "sandwich" in reply.lower() and "not a sandwich" not in reply.lower()
    if offers_one and _said_no_sandwich(memory):
        return _no_sandwich_lunch(memory, understood)
    return reply


def _no_sandwich_lunch(memory, understood):
    said = " ".join(str(word) for word in ((understood or {}).get("words") or ())).lower()
    kid = _lunch_is_for_a_child(memory, said) or any(
        word in said for word in ("year old", "nursery", "school", "fussy", "picky"))
    user = (memory or {}).get("user") if isinstance(memory, dict) else None
    banned = set(_bans_of(user)) | set(avoids_for_the_one_talked_about(memory))
    if banned:
        for said_allergy in (user or {}).get("allergies") or ():
            for word in str(said_allergy).lower().replace(",", " ").split():
                tag = _SNACK_FAMILY_OF.get(word)
                if tag:
                    banned.add(tag)
        kept = _a_lunchbox_without(_NO_SANDWICH_KID_ITEMS if kid else _NO_SANDWICH_ADULT_ITEMS,
                                  banned)
        if not kept:
            who = "he" if kid else "you"
            return ("With that much ruled out there is nothing on the usual list to name: build "
                    "the lunch from what " + who + " already eats at home, a tub of dinner kept "
                    "cold and a drink, and check the label on every packet you use. "
                    + ("A flask of soup or leftovers does the same job and is often the easiest "
                       "with a fussy eater." if kid else ""))
        listed = ", ".join(kept[:-1]) + " and " + kept[-1] if len(kept) > 1 else kept[0]
        how_many = ("any three of those and a drink is a lunch" if len(kept) >= 3
                    else "both of those and a drink is a lunch" if len(kept) == 2
                    else "that and a drink is a lunch")
        if kid:
            return ("For a lunchbox with no sandwich: " + listed + " - " + how_many + ". A flask "
                    "of soup or leftovers does the same job and is often the easiest with a "
                    "fussy eater, because it is food they already eat at home.")
        return ("For a packed lunch with no sandwich: " + listed + " travel" +
                ("s" if len(kept) == 1 else "") + " well. " + how_many.capitalize() + ", and the "
                "tub of dinner is the one that keeps you full until tea.")
    if kid:
        return ("For a lunchbox with no sandwich: cooked pasta or rice from last night's dinner "
                "in a tub, cheese cubes or a boiled egg with crackers or oatcakes, veg sticks "
                "with hummus, a yoghurt and some fruit - any three of those and a drink is a "
                "lunch. A flask of soup or leftovers does the same job and is often the easiest "
                "with a fussy eater, because it is food they already eat at home.")
    return ("For a packed lunch with no sandwich: last night's dinner in a tub is the easiest, "
            "and pasta or rice salad, cold chicken or cheese with oatcakes, a boiled egg, veg "
            "sticks and hummus, soup in a flask, yoghurt and fruit all travel well. Any three of "
            "those plus a drink is a lunch, and the tub of dinner is the one that keeps you full "
            "until tea.")


def _coffee_late(memory, reading):
    clean = (reading.get("clean") or "").lower()
    if re.search(r"\bhow long\b|\bhow many hours\b|\bwhat time\b|\bwhen should i stop\b|"
                 r"\bstop drinking\b|\bcut off\b|\blast (?:cup|coffee)\b|\bhow late\b|"
                 r"\bbefore bed\b|\bbedtime\b|\bbefore sleep\b", clean):
        return ("Stop by early afternoon, and count back: caffeine's half-life is about five "
                "hours, so half a 4pm cup is still in you at 9pm and a quarter of it at 2am. If "
                "you are in bed at eleven, a last full cup around 2pm leaves almost nothing by "
                "then; after that make it decaf, which has about 2mg a cup against 80.")
    late = ("late", "tonight", "this evening", "in the evening", "this afternoon",
            "in the afternoon", "before bed", "bedtime", "pm", "at night", "night")
    if any(word in clean for word in late):
        if re.search(r"\b(?:should|shall|can|could|may)\s+(?:i|we)\b"
                     r"|\b(?:is|would)\s+it\s+(?:ok|okay|alright|fine|bad|a\s+bad\s+idea)\b"
                     r"|\bdo\s+i\s+dare\b", clean):
            return ("No, not if you want to sleep: half the caffeine is still there five or six "
                    "hours later, so a 4pm cup can still be working at midnight. Keep to one or "
                    "two cups a day, stop by early afternoon, make the afternoon one decaf, and "
                    "eat something with it. Palpitations, shakiness or panic that come with "
                    "caffeine are worth mentioning to a GP, especially with chest pain or "
                    "breathlessness.")
        return ("Yes, too late if you want to sleep at a normal hour: half the caffeine is still "
                "there five or six hours later, so a 4pm coffee can still be working at "
                "midnight. Keep to one or two cups a day, stop by early afternoon, make the "
                "afternoon one decaf, and eat something with it. Palpitations, shakiness or panic "
                "that come with caffeine are worth mentioning to a GP, especially with chest pain "
                "or breathlessness.")
    return ("It is the caffeine: it peaks about half an hour after the cup and takes five or six "
            "hours to leave your system, so a 4pm coffee can still be in you at midnight. Keep to "
            "one or two cups, stop by early afternoon, make the afternoon one decaf, and eat "
            "something with it. Palpitations, shakiness or panic that come with caffeine are worth "
            "mentioning to a GP, especially with chest pain or breathlessness.")

NOT_A_KEEPING_ASK = ("how do i", "how to", "recipe", "recipes", "what can i make",
                     "what can i do", "how long to cook", "how long to bake", "how long in the",
                     "take to cook", "take to bake", "cooking time", "bake", "baking", "oven",
                     "boil", "fry", "roast", "cook", "cooking", "freeze", "freezer", "frozen",
                     "defrost", "thaw", "thawing", "reheat",
                     "good for you", "healthy", "unhealthy", "fattening", "calories",
                     "how many calories", "pregnant", "pregnancy", "safe in pregnancy")

_COOKING_CLOCK = re.compile(r"\bhow long\b[^.?!]*?\btak(?:e|es|en|ing)\b")
_A_KEPT_THING = re.compile(
    r"\b(?:keep|keeps|keeping|kept|last|lasts|lasting|fridge|freezer|freeze|frozen|store|stored|"
    r"storage|shelf life|left out|left over|leftover|still (?:ok|okay|good|safe|fine)|"
    r"safe to eat|use by|go off|goes off|going off|gone off|go bad|goes bad|went bad|"
    r"out of date)\b")


_MAKE_IT_ASK = re.compile(
    r"\b(?:what (?:can|should|shall) i (?:make|cook|do|have)|what to (?:make|cook|do)|"
    r"what else can i (?:make|cook)|ideas (?:for|with)|something (?:for|with)|"
    r"use (?:it )?up|using (?:it )?up|use up the|recipe|recipes)\b")


def _not_a_make_it_ask(understood):
    text = str((understood or {}).get("clean") or "").lower()
    return not _MAKE_IT_ASK.search(text)


def _not_a_cooking_time(understood):
    if not _not_a_make_it_ask(understood):
        return False
    words = [str(word).lower() for word in (understood.get("words") or ())]
    if not words:
        return True
    joined = " ".join(words)
    if not _COOKING_CLOCK.search(joined):
        return True
    return bool(_A_KEPT_THING.search(joined))


KEEPING_WORDS = ("how long", "keep", "keeps", "keeping", "kept", "last", "lasts", "lasting",
                 "fridge", "freezer", "freeze", "frozen", "store", "stored",
                 "storage", "shelf life", "shelf-life", "still good",
                 "safe to eat", "day old", "days old",
                 "how many days", "left over", "leftover")

STORE_ASKS = ("store", "stores", "storing", "stored", "storage",
              "how do i store", "how should i store", "how do you store", "how to store",
              "best way to store", "where do i keep", "where should i keep",
              "keep it fresh", "keep them fresh", "keep fresh", "stays fresh",
              "stay fresh", "keeps fresh")

_BREAST_MILK = ("breast milk", "breast", "expressed", "baby milk", "bottle of milk",
                "baby bottle", "babies bottle")


def _milk_keep(memory, understood):
    said = " %s " % " ".join(str((understood or {}).get(key) or "")
                             for key in ("clean", "norm_text", "norm")).lower()
    if "formula" in said or "made up" in said or "made-up" in said:
        return ("Made-up formula is good for 2 hours at room temperature and 24 hours in the "
                "fridge, and the clock starts when the powder goes in - throw away whatever is "
                "left in the bottle after a feed.")
    if any(word in said for word in _BREAST_MILK):
        return ("Expressed breast milk keeps about 4 hours at room temperature, up to 4 days at "
                "the back of the fridge, and 6 months in the freezer; once thawed it is good for "
                "24 hours in the fridge and must not be refrozen.")
    keeping = ("Once opened, keep milk in the fridge and use it within about 5 days; the date on "
               "the carton is about quality, not safety, so milk that has been kept cold is fine a "
               "day or two past it.")
    spoilt = "If milk smells or tastes sour, bin it, whatever the date says."
    if "fresh" in said or any(shape in said for shape in STORE_ASKS):
        return keeping + " " + spoilt
    return spoilt + " " + keeping


_BAKE_KEEPING_SHAPED = tuple(word for word in _BAKE_KEEPING
                             if word not in ("keep", "keeps", "keeping", "kept", "last",
                                             "lasts")) + _BAKE_KEEP_SHAPES
_DRINK_NAMES = ("tea", "teas", "coffee", "coffees", "espresso", "caffeine", "energy drink",
                "energy drinks", "cola", "coke", "matcha", "chai", "green tea", "herbal tea",
                "decaf", "hot chocolate", "milkshake", "smoothie", "juice", "wine", "beer")
_ASK_WORDS = ("how", "what", "is", "are", "was", "should", "can", "could", "do", "does",
              "did", "am", "limit", "safe", "ok", "bad", "healthy", "unhealthy", "worried")
_DOSE_WORDS = ("much", "many", "too", "limit", "safe", "ok", "bad", "healthy", "unhealthy",
               "day", "daily", "week", "weekly", "cup", "cups", "mug", "mugs", "glass",
               "glasses", "pint", "pints", "litre", "litres", "liter", "liters", "mg", "ml")
_COOKING_WORDS = ("made", "make", "makes", "cooked", "cook", "cooks", "cooking",
                  "left over", "left", "leftover", "leftovers", "freeze", "frozen", "freezer",
                  "pot", "pan", "jug", "batch", "reheat", "reheated", "keep", "keeps", "store",
                  "stored", "waste", "wasting", "wasted", "bin", "binned", "pour", "poured",
                  "split", "cool", "chill", "fridge", "throw", "throwing", "thrown", "portion",
                  "portions", "soup", "stew", "curry", "dinner", "supper", "meal")


def not_a_cup_of_tea(understood):
    words = [str(word).lower() for word in (understood.get("words") or ())]
    if not words:
        return True
    joined = " %s " % " ".join(words)
    if not any(" %s " % name in joined for name in _DRINK_NAMES):
        return True
    if any(" %s " % word in joined for word in _COOKING_WORDS):
        return True
    if not any(" %s " % word in joined for word in _ASK_WORDS):
        return True
    if any(" %s " % word in joined for word in _DOSE_WORDS):
        return False
    return True


_SNACK_OPTIONS = (
    ("Greek yoghurt with berries", "dairy milk yoghurt"),
    ("an apple with a spoon of peanut butter", "nut peanut butter"),
    ("a handful of nuts with a boiled egg", "nut egg"),
    ("hummus with carrot and oatcakes", "sesame hummus chickpea"),
    ("cheese on two crackers", "dairy cheese gluten cracker"),
    ("a banana and a glass of milk", "dairy milk banana"),
    ("rice cakes with mashed avocado", "rice avocado"),
    ("home-made popcorn", "corn popcorn"),
    ("carrot sticks and a few olives", "carrot olive"),
)


_SNACK_FAMILY_OF = {}
for _tag, _named in (
        ("nut", "nut nuts peanut peanuts almond almonds cashew cashews walnut walnuts "
                "hazelnut hazelnuts pistachio pistachios pecan pecans brazil brazils"),
        ("dairy", "dairy milk milks cheese cheeses yoghurt yogurts yogurt butter cream lactose"),
        ("gluten", "gluten wheat coeliac celiac flour bread pasta cracker crackers"),
        ("sesame", "sesame tahini hummus"),
        ("egg", "egg eggs mayonnaise")):
    for _word in _named.split():
        _SNACK_FAMILY_OF[_word] = _tag


def _a_snack(memory, understood):
    user = (memory or {}).get("user") if isinstance(memory, dict) else None
    banned = set(_bans_of(user))
    banned |= set(avoids_for_the_one_talked_about(memory))
    for said in (user or {}).get("allergies") or ():
        for word in str(said).lower().replace(",", " ").split():
            tag = _SNACK_FAMILY_OF.get(word)
            if tag:
                banned.add(tag)
    chosen = [food for food, words in _SNACK_OPTIONS
              if not (set(words.split()) & banned)]
    if not chosen:
        chosen = ["whatever protein and fibre you can eat safely"]
    listed = ", ".join(chosen[:2])
    if len(chosen) >= 3:
        listed += " or " + chosen[2]
    return ("Go for protein plus fibre at about four in the afternoon, 150 to 250 calories: "
            + listed + ". It holds you a couple of hours where a biscuit holds you twenty "
            "minutes, so you are not starving at dinner.")


_not_the_flat_you_live_in_bake = not_the_flat_you_live_in
_COFFEE_LEADS = (
    ("cappuccino", "A cappuccino is a third espresso, a third steamed milk and a third foam: pull "
                   "a double espresso (about 60ml), heat about 120ml of milk to 60-65C while "
                   "letting plenty of air in so it doubles to a stiff foam, then pour the milk in "
                   "and spoon the foam on top."),
    ("latte", "A latte is a double espresso (about 60ml) with about 200ml of milk heated to 60-65C "
              "and frothed barely at all, so it is a thin layer of microfoam over hot milk rather "
              "than a cap. Pour with the jug low and the drink stays glossy."),
    ("macchiato", "A macchiato is a double espresso (about 60ml) with just a spoonful of milk foam "
                  "stained into it: heat a little milk to 60-65C, froth it, and drop a dessert "
                  "spoon of the foam on top of the shot."),
    ("americano", "An americano is a double espresso (about 60ml) with about 120ml of hot water "
                  "added, never the other way round: the water goes in after the shot because "
                  "brewing onto hot water scorches the coffee and it turns bitter."),
    ("espresso", "An espresso is about 18g of finely ground coffee to a double shot of 60ml in "
                 "25-30 seconds. Grind fine, tamp level and firm, and if it runs much faster the "
                 "grind is too coarse, if it dribbles the grind is too fine."),
)

_THE_MILK_ONLY = ("froth the milk", "froth milk", "froth", "frothing", "frothed milk",
                  "steam the milk", "steam milk", "steaming", "milk frother", "steam wand",
                  "milk steamer", "no machine", "without a machine")


def _a_coffee(memory, understood):
    said = str((understood or {}).get("norm_text")
               or (understood or {}).get("text") or "").lower()
    for name, lead in _COFFEE_LEADS:
        if name in said:
            return lead + " " + _COFFEE_MILK_TAIL
    if any(phrase in said for phrase in _THE_MILK_ONLY):
        return _THE_FROTH_CARD
    return ("A flat white is a double espresso (about 60ml) with about 100ml of milk heated to "
            "60-65C and frothed only to a thin, glossy microfoam, poured with the jug low so the "
            "foam sits in a thin layer rather than a cap on top, while a latte takes twice the "
            "milk and less foam, and a cappuccino more air again. " + _COFFEE_MILK_TAIL)


_COFFEE_MILK_TAIL = ("Whole milk froths most easily and skimmed the least. With no steamer, heat "
                     "the milk in a pan to just before it simmers and whisk hard for 20 seconds, "
                     "or shake it in a lidded jar and give it 30 seconds in the microwave.")

_THE_FROTH_CARD = ("Heat the milk to 60-65C - hot but not simmering, because above that the milk "
                   "turns and tastes cooked - then get air in for the first few seconds and stop: "
                   "with a steam wand, tip it just under the surface so it hisses, then sink it to "
                   "spin the milk into a glossy microfoam. With no machine, heat it in a pan and "
                   "whisk hard for 20 seconds, or shake it in a lidded jar and microwave it for 30 "
                   "seconds. Whole milk froths most easily and skimmed the least.")


def _tins_keep(memory, understood):
    return ("Tins keep for years in a cool cupboard, though anything acidic - tomatoes, fruit, "
            "pickles - is best inside 18 months, and a dented or rusty tin is worth using soon. "
            "The date on a tin is a best-before for quality rather than a use-by. Bin any tin that "
            "is bulging, smells sharp when you open it, or fizzes. Once it is open, what is left "
            "goes into a bowl with a lid, not back in the tin: 2 days in the fridge for tuna or "
            "beans, and eat anything acidic within a couple of days.")


def _tomato_sauce(memory, understood):
    said = " " + str((understood or {}).get("clean") or (understood or {}).get("text") or "")
    said = said.lower() + " "
    if any(phrase in said for phrase in ("how long", "simmer", "minutes", "how many minutes",
                                         "time", "takes", "take")):
        return ("Twenty to thirty minutes on a low simmer, and it is better at forty: soften the "
                "garlic in olive oil, add a tin of tomatoes and a pinch of salt, and let it go "
                "uncovered so it thickens. Tear in basil at the end and loosen it with a splash of "
                "pasta water. A long simmer is what turns tinned tomatoes from sharp into sweet, so "
                "if it tastes sour give it another ten minutes rather than more sugar.")
    return ("A good 15-minute tomato sauce: soften sliced garlic in olive oil, add a tin of tomatoes "
            "and a pinch of salt, and simmer it while the pasta cooks. Tear in a few basil leaves at "
            "the end and loosen it with pasta water.")
def freeze_cooked_answer(memory, understood):
    return _freeze_cooked(memory, understood)


FREEZE_DISH_TIMES = (
    (("mash", "mashed potato", "mashed potatoes", "potato", "potatoes"), "about one month"),
    (("lasagne", "lasagna", "pasta bake", "casserole", "shepherds pie", "cottage pie",
      "pie", "risotto", "paella", "gratin", "stew", "curry", "soup", "chilli",
      "bolognese", "leftovers", "food",
      "quiche", "frittata", "omelette", "moussaka", "tagine", "meatballs", "burrito",
      "quesadilla", "stuffing", "sausage rolls", "samosa", "spring rolls", "dumplings",
      "fishcakes", "fish cakes", "nut roast"), "about three months"),
)

FREEZE_COOKED_STEP = (
    "Reheat it from frozen until it is piping hot right through, or thaw it overnight in the "
    "fridge and use it once.")


def _freeze_cooked(memory, understood):
    said = " %s " % " ".join(str(word).lower() for word in (understood.get("words") or ()))
    for names, keeps in FREEZE_DISH_TIMES:
        if any(" %s " % name in said or " %ss " % name in said for name in names):
            return ("Yes - it keeps %s in the freezer, so cool it within an hour, then pack it "
                    "flat in bags or tubs so it freezes fast. %s" % (keeps, FREEZE_COOKED_STEP))
    return ("Yes - cooked dishes keep about three months frozen, and a month for mash, so cool it "
            "within an hour, then pack it flat in bags or tubs so it freezes fast. %s"
            % FREEZE_COOKED_STEP)


_HOT_SAID = re.compile(
    r"\b(?:hots?|hotter|scorching|scorched|scorch|sizzling|smoking|steaming|melted|melts?|"
    r"burnt|burned|burns?|blistering|straight off|off the (?:hob|ring|heat|burner)|just off|"
    r"just came off|came off the|left a (?:mark|ring|stain))\b", re.IGNORECASE)


def _a_hot_thing_is_being_set_down(understood):
    if not isinstance(understood, dict):
        return True
    said = understood.get("text") or understood.get("clean") or ""
    if not said:
        said = " ".join(understood.get("words") or ())
    return bool(_HOT_SAID.search(str(said)))


_BATTER = ("pancake", "pancakes", "crepe", "crepes", "batter", "waffle", "waffles",
           "yorkshire pudding", "yorkshire puddings", "yorkshires", "pikelet", "pikelets",
           "drop scones", "blini", "blinis")
_BATTER_IN_A_TIN = ("tin", "tins", "tray", "trays", "muffin", "muffins", "oven",
                    "yorkshire", "yorkshires", "pudding", "puddings")
_BATTER_IN_AN_IRON = ("iron", "waffle iron", "waffle maker", "waffles", "waffle")

_LOAF = ("bread", "loaf", "loaves", "sourdough", "bloomer", "brioche", "teacake", "teacakes")


def _out_of_the_tin(memory, reading):
    words = set(reading.get("words") or ())
    if words.intersection(_LOAF):
        return ("A loaf sticks to the tin when the tin was bare or the dough was wet: oil the tin "
                "all over, and line the base and the two long sides with a strip of baking paper "
                "that overhangs the top, so you lift the loaf out by the paper. Run a knife round "
                "the edges while it is still warm, wait ten minutes, then turn it out and tap the "
                "base - and let it cool on its side so the crust does not go soft.")
    return ("A cake sticks to the tin when it was greased unevenly, turned out before it had "
            "firmed, or baked in a tin that was not lined. Line it with a strip of baking paper "
            "across the base and up two sides and it lifts out whole. Run a thin knife round the "
            "edge while it is still warm, wait ten minutes, then turn it out onto a rack - and if "
            "it does crack, stick it back together with a little jam or buttercream and nobody "
            "will know.")


def _a_batter_that_sticks(memory, reading):
    words = set(reading.get("words") or ())
    if words.intersection(_BATTER_IN_AN_IRON):
        return ("A waffle iron that grips wants to be properly hot before the batter goes in, and "
                "brushed with a little oil right into the grooves: heat it five minutes, oil it, "
                "and fill to the edge of the pattern only. Leave the lid shut for a minute and "
                "let the waffle come away by itself - one pulled open early tears.")
    if words.intersection(_BATTER_IN_A_TIN):
        return ("A batter that sticks to the tin wants the fat hotter than the batter: put a little "
                "oil or dripping in each hole and heat the tin in the oven at 220C (200C fan) for "
                "10 minutes, until it shimmers, then pour the batter in and shut the door. Do not "
                "open it for 20 minutes - the cold air drops them - and if one still sticks, give "
                "it 5 minutes more, because a batter that comes away rough was not done.")
    return ("A batter that sticks wants a hotter pan and less fat than you would think: heat a "
            "non-stick or well-seasoned pan on a medium heat for a couple of minutes, wipe it "
            "with a little oil on kitchen paper, and pour when a drop of batter sizzles at once. "
            "Wait until the top bubbles and the edges look dry before you turn it, because "
            "lifting one early is what tears it, and thin a thick batter with a splash of milk, "
            "or it sits in the middle of the pan and grips.")


_STUCK_TO_A_PAN = (
    "Get the pan properly hot with the oil already in it, then leave the food alone for the first "
    "minute: it releases itself once it has browned. For pasta, stir it for the first minute in a "
    "big pan of water; for rice, rinse it and don't stir it at all.")

_FROZEN_SAID = frozenset((
    "frozen", "freezer", "freeze", "freezes", "froze", "defrost", "defrosted", "defrosting",
    "thaw", "thawed", "thawing", "cold", "ice", "straight",
))


def _a_frozen_pizza(understood):
    return bool(_FROZEN_SAID.intersection(understood.get("words") or ()))


SLICE_METHOD = ("A serrated bread knife, long gentle sawing strokes and almost no downward "
                "pressure: a sharp straight knife crushes the crumb instead of cutting it. Lay "
                "the loaf on its side so the cut is level, cut from the far edge towards you, "
                "and slice the whole loaf at once if you are going to freeze it.")
SLICE_THICK = ("About 1cm to 1.5cm for a sandwich, 2cm for toast, and a fresh sourdough wants the "
               "thicker end of that because its crumb is denser. A very thin slice tears unless "
               "the bread is a day old, since new bread is too soft to hold a thin cut.")
SLICE_WARM = ("Let it cool first, an hour on a rack for a loaf: a warm loaf is still setting "
              "inside, so a slice squashes the crumb and lets the steam out, and the cut face "
              "goes gummy. Warm bread also stales faster once it has been cut.")
STALE_FAST = ("A lean loaf with no fat or sugar in it stales faster than a shop one that has "
              "both, and the cut face is where it dries: stand the loaf cut side down on a "
              "board, keep it in a paper bag or a bin rather than the fridge, and freeze what "
              "you will not eat in two days - sliced, so you can take out what you need. A "
              "sourdough goes hard rather than mouldy first, and 5 minutes in a hot oven with a "
              "splash of water brings a slice back.")


_A_PORTION_OF_SLICES = re.compile(
    r"\b(?:a|an|one|two|three|four|five|six|\d+)\s+slices?\b|\bslices?\s+of\b")
_STICKING_A_CUT = re.compile(r"\b(?:how|why|should|which way|what is the best way)\b")


def _bread_sliced(memory, understood):
    said = " " + str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower() + " "
    if _A_PORTION_OF_SLICES.search(said) and not _STICKING_A_CUT.search(said):
        return None
    if any(word in said for word in (" stale", " stales", " staling", " hard", " dry", " drying",
                                     " why does", " why do", " goes off", " gone hard")):
        return STALE_FAST
    if any(word in said for word in (" thick", " thickness", " thin", " wide",
                                     " how wide", " size of")):
        return SLICE_THICK
    if any(word in said for word in (" warm", " hot", " just baked", " fresh out", " still warm",
                                     " straight out")):
        return SLICE_WARM
    return SLICE_METHOD

def _no_named_food(understood):
    from .meals import INGREDIENTS
    words = set(understood.get("words") or ())
    named = set()
    for key, forms in INGREDIENTS.items():
        if key == "veg":
            continue
        named.update(forms)
    return not (words & named)

_PORRIDGE_SALT = ("too salty", "salty", "too much salt", "over salted", "oversalted",
                  "salt went", "extra salt", "double salt")
_PORRIDGE_BLAND = ("bland", "tastes of nothing", "taste of nothing", "no taste", "tasteless",
                   "nothing in it", "a bit boring", "boring")


def _porridge_fault(memory, understood):
    said = str(understood.get("clean") or understood.get("text") or "").lower()
    if any(word in said for word in _PORRIDGE_SALT):
        return ("A bowl of porridge with too much salt in it takes more milk and more oats, not "
                "water: stir in a good splash of milk and a spoon more oats and give it two "
                "minutes on the heat, then a spoon of plain yoghurt or a little honey at the end. "
                "Water alone just leaves you with a thin bowl that is still salty.")
    if any(word in said for word in _PORRIDGE_BLAND):
        return ("Porridge is bland for want of salt and something on top, not for want of skill: "
                "put a pinch of salt in the pan, cook it in milk rather than water, and finish it "
                "with honey, jam, brown sugar, banana, berries or a spoon of peanut butter. Salt "
                "is the one that matters - without it everything else tastes flat.")
    if "overnight" in said or "soak" in said or "soaked" in said or "in a jar" in said:
        return ("Stir a pinch of salt and a splash more milk or yoghurt into the jar, because salt "
                "and milk are what turn the sweetness down, and leave it ten minutes to mellow. If "
                "it is still too sweet, add a spoon more oats and a little milk rather than more "
                "sugar in future: the sweetness sits on top of soaked oats rather than in them.")
    return ("Stir in a splash more milk or plain yoghurt and a pinch of salt, because salt is "
            "what turns the sweetness down, and leave it a minute to loosen. If it is still too "
            "sweet, a handful of berries or a spoon of yoghurt does more than adding more oats. "
            "Next time, leave the sugar out of the pan or the jar and put it on the table: "
            "porridge takes very little, and the milk brings out the sweetness of the oats.")


_HOT_PAN_TAKES = (
    ("a glass ceramic or induction hob",
     r"glass (?:ceramic )?hob|ceramic hob|induction (?:hob|top)|glass[- ]top hob"),
    ("a stainless steel worktop",
     r"stainless(?: steel)? (?:worktop|work top|top|surface|bench)"),
    ("the hob", r"\bhob\b"),
)
_HOT_PAN_REFUSES = (
    ("granite", r"granite", "the heat shock cracks stone"),
    ("quartz", r"quartz", "the heat shock cracks stone"),
    ("marble", r"marble", "the heat shock cracks stone"),
    ("a laminate worktop", r"laminate", "the heat shock scorches and lifts it"),
    ("a wooden worktop or board",
     r"wood(?:en)? (?:worktop|work top|(?:\w+ )?board)", "the heat scorches the wood"),
    ("a wooden table", r"wood(?:en)? table", "the heat scorches the wood"),
    ("a glass table", r"glass[- ]?top table|glass table", "the heat shock can crack it"),
)
_HOT_PAN_CAN = ("Straight off the ring a hot pan can go back down on a glass ceramic or induction "
                "hob, and on a stainless steel worktop, because those are built for it.")
_HOT_PAN_NOT = ("Keep it off granite, quartz, marble and laminate worktops, wooden boards and "
                "glass tables: the heat shock cracks stone and scorches laminate.")
_HOT_PAN_TIP = "A trivet or a folded dry cloth under it, and nothing wet on a hot hob."


def _a_hot_pan_surface(text):
    said = " %s " % (text or "").lower()
    for name, pattern, reason in _HOT_PAN_REFUSES:
        if re.search(r"(?:%s)" % pattern, said):
            return "no", name, reason
    for name, pattern in _HOT_PAN_TAKES:
        if re.search(r"(?:%s)" % pattern, said):
            return "yes", name, ""
    return None, None, ""


def _the_hot_pan_place(memory, understood):
    verdict, surface, reason = _a_hot_pan_surface(_line(understood))
    if verdict == "no":
        return ("No - not on " + surface + ": " + reason + ". " + _HOT_PAN_CAN + " "
                + _HOT_PAN_TIP)
    if verdict == "yes":
        return ("Yes - " + surface + " takes it straight off the ring. " + _HOT_PAN_NOT + " "
                + _HOT_PAN_TIP)
    return _HOT_PAN_CAN + " " + _HOT_PAN_NOT + " " + _HOT_PAN_TIP


def something_to_bake_in_the_oven(understood):
    if not isinstance(understood, dict):
        return False
    text = str(understood.get("clean") or understood.get("text") or "")
    if not text:
        return False
    from . import dishes
    return bool(dishes.dish_in(text))


_ROAST_BURNT = ("burn", "burnt", "burning", "black", "blackened", "caught", "too hot",
                "too dark", "stuck")


_ROAST_STUCK = ("stuck", "stick", "sticks", "sticking", "welded", "glued")


_ROAST_HARD = ("hard", "harder", "still hard", "too hard", "undercooked", "under cooked",
               "under-done", "not cooked", "not soft", "raw in the middle", "hard in the middle",
               "hard centre", "hard centers", "not done")


_JOINT_WORDS = ("chicken", "turkey", "beef", "lamb", "pork", "ham", "gammon", "goose", "duck",
                "joint", "bird", "brisket")

_A_JOINT_TIMING = re.compile(
    r"\bhow long\b|\bhow many minutes\b|\bhow many hours\b|\btakes?\b|\btiming\b"
    r"|\btime\b|\bminutes per\b|\bper (?:kg|500g|pound|lb)\b|\bis it done\b"
    r"|\bwhen is it done\b")

_A_FAT_WORD = re.compile(r"\bfat\b|\bdripping\b|\bdrippings\b|\blard\b|\btallow\b")


def _not_the_joint_timing(understood):
    said = " " + " ".join(str((understood or {}).get(key) or "")
                          for key in ("clean", "norm_text", "norm")).lower() + " "
    if not any(re.search(r"\b" + word + r"\b", said) for word in _JOINT_WORDS):
        return True
    if _A_FAT_WORD.search(said):
        return True
    return not _A_JOINT_TIMING.search(said)



def _roast_potatoes(memory, reading):
    clean = str(reading.get("clean") or "").lower()
    if any(word in clean for word in _ROAST_STUCK):
        return ("Sticking is the tray and the wet, not the heat: put the oiled tray in to get hot "
                "before the potatoes go on, dry them on a tea towel once they are drained, and "
                "keep them in one layer with space between them so the steam can get out. "
                "Turn them at 25 minutes with a fish slice rather than a spoon, and whatever is "
                "already browned comes away on its own.")
    if any(word in clean for word in _ROAST_HARD):
        return ("Hard in the middle is a size and time problem, not a heat problem: cut them no "
                "bigger than a golf ball, parboil them a full 8 minutes so the middle starts to "
                "cook before the outside crisps, and give the tray 10 to 15 minutes more at 200C "
                "(180C fan) in one layer. Test the biggest one with the point of a knife: it "
                "should slide in with no resistance at all.")
    if any(word in clean for word in _ROAST_BURNT):
        return ("Too hot, or the potatoes went in wet: turn the oven down to 190C (170C fan), "
                "spread them in one layer with space between them and turn them at 25 minutes. "
                "Dry them on a tea towel after the parboil and shake them rough, because a wet "
                "potato steams and then blackens at the edges before the middle is done.")
    return ("Parboil peeled potatoes for 8 minutes, drain them, shake the pan to rough up the "
            "edges, then roast at 200C (180C fan) in a thin layer of hot oil for 40 to 45 "
            "minutes. The rough edges are what go crunchy. If they came out of a freezer bag, "
            "none of that applies: 200C (180C fan) for 20 to 25 minutes straight from frozen, "
            "in one layer.")
ENTRIES = [
    entry("a-batter-that-sticks",
          (_BATTER,
           ("stuck", "sticks", "stick", "sticking", "grips", "tears", "tearing", "breaking",
            "broke", "come out", "comes out", "came out", "getting out", "get it out",
            "get them out", "come away")),
          _a_batter_that_sticks,
          bias=2,
          avoid=("flat", "thin", "thick", "fluffy", "rise", "risen", "recipe", "how many",
                 "mix", "bought", "buy", "frozen", "freeze", "warm", "reheat",
                 "oil", "which pan", "what pan", "best pan", "pan for", "shrove", "day",
                 "sugar", "lemon")),
    entry("slow-cooker-left-on", (("slow cooker", "slow-cooker", "crockpot", "crock pot"),
                                  ("leave", "left", "leaving", "on all day", "all day",
                                   "overnight", "all night", "on all night",
                                   "while im out", "while im at work",
                                   "while i am out", "while i am at work", "unattended",
                                   "keep the slow cooker on", "keep a slow cooker on",
                                   "keep the crockpot on", "keep the crock pot on",
                                   "keep it on", "keeping it on", "keep it going",
                                   "keep it warm", "keeping it warm",
                                   "safe", "ok", "okay", "fine", "alright")),
          "Yes - that is what it is built for, and leaving a slow cooker on low while you are out "
          "is an ordinary thing to do. Keep it at least half full of liquid so it does not dry out "
          "and catch, put the lid on and do not lift it, sit it on a dry worktop with the cord well "
          "away from the hot sides, and keep it to about 8 hours on low (4 on high). Cooked food "
          "left in it on warm all evening is the one to avoid: cool the food, put it in the fridge, "
          "and reheat it once, piping hot.",
          avoid=("recipe", "recipes", "what can i cook", "what to cook", "dinner ideas",
                 "frozen", "freeze", "defrost", "thaw", "reheat", "left over", "leftover",
                 "leftovers", "store", "storage", "keep in the fridge", "fridge", "freezer",
                 "clean", "cleaning", "smell", "smells", "keep it clean",
                 "dishwasher", "dish washer", "wash", "washing", "scrub", "stained",
                 "burnt on", "stuck on",
                 "gas", "hob")),
    entry("burnt-toast", (("toast", "toasted", "slice of toast", "toastie"),
                          ("burnt", "burned", "black", "charred", "scorched", "brown", "too long",
                           "in too long", "left it in")),
          "Yes, scrape the black off with a knife and eat the rest: it tastes fine, and burnt toast "
          "is not dangerous in the way people fear. Very charred bread does carry more acrylamide, "
          "so it is not something to make a habit of, but one slice is nothing to worry about. The "
          "smoke is the bigger nuisance, so open a window and run the extractor.",
          avoid=("smell", "smells", "smelling", "stink", "stinks", "stinking", "stank", "reek",
                 "reeks", "odour", "pong", "smoke", "smoky", "alarm", "toaster broke",
                 "bread bin", "gone mouldy", "mould", "mold",
                 "dog", "dogs", "puppy", "pup", "cat", "cats", "kitten", "pet", "pets", "bird",
                 "parrot", "rabbit", "hamster", "pregnant", "pregnancy", "pregnancies",
                 "baby", "toddler", "child", "kids",
                 "tummy", "stomach ache", "food poisoning")),
    entry("cracked-egg", (("egg", "eggs"), ("crack", "cracked", "cracks", "crack in the shell",
                                           "shell is cracked", "broken shell",
                                           "leak", "leaks", "leaked", "leaking", "egg leaked",
                                           "broke in the box", "broken in the box",
                                           "broke in the carton", "broken in the carton",
                                           "cracked in the box", "cracked in the carton")),
          "A hairline crack is fine: cook it and eat it. A crack with a bit of leaked white is "
          "usually fine too if it is fresh and you cook it through, but bin it if the shell is "
          "dirty from a cracked egg or it has been sitting warm, since the shell is what keeps "
          "bacteria out. Keep cracked eggs out of anything raw, like mayonnaise.",
          avoid=("shell went in", "shell in", "bit of shell", "chapped", "cracked lips",
                 "cracked skin", "cracked heel", "cracked heels", "pavement", "phone", "screen",
                 "plaster", "wall", "tile", "tiles",
                 "how do i crack", "how to crack", "crack an egg", "cracking an egg",
                 "separate an egg", "separating an egg",
                 "boil", "boiling", "boiled", "pan", "stop", "stopping", "prevent", "shells in"),
          bias=1),
    entry("crack-egg", (("egg", "eggs"), ("crack", "cracks", "cracking", "cracked")),
          "Tap it on a flat worktop, not the rim of the bowl: one firm tap, turn it a quarter "
          "and tap again, then pull the halves apart over the bowl with your thumbs and let it "
          "drop. The flat tap cracks the shell in a line; a rim tap dents it and pushes shell "
          "into the egg. If a piece does go in, lift it out with a wet finger or the edge of a "
          "shell half, which the white will not cling to.",
          avoid=("is cracked", "cracked shell", "shell is cracked", "hairline", "leaked",
                 "leaks", "still ok", "still okay", "safe to eat", "safe", "bin it", "bad egg",
                 "boil", "boiling", "boiled", "pan", "poach", "poached", "scrambl", "yolk",
                 "separate", "separating", "separated", "white", "whites",
                 "phone", "screen", "window", "wall", "pavement", "tile", "tiles", "glass",
                 "joke", "password", "code", "nuts", "walnut", "coconut", "cracker", "crackers",
                 "whip", "cracking on", "get cracking", "crack someone", "knuckle", "lip",
                 "lips", "skin", "heel", "heels", "ribs", "back")),
    entry("broken-yolk", (("yolk", "yolks"),
                          ("broke", "break", "breaks", "broken", "split", "punctured",
                           "pierced", "burst")),
          "A broken yolk is still good: fry it as it is or scramble it, and it tastes the same "
          "though it will not look as neat. When you want them whole, crack each egg into a cup "
          "first and slide the good ones into the pan, so one broken one does not spoil the rest.",
          avoid=("boil", "boiling", "boiled", "runny", "dipping", "how long", "minutes"),
          bias=1),
    entry("separate-egg", (("egg", "eggs"), ("separate", "separating", "separated",
                                             "egg white", "egg whites", "whites")),
          "Crack the egg into your hand over a bowl and let the white slide through your "
          "fingers, or tip the yolk from one half-shell to the other and let the white fall. "
          "Cold eggs separate more cleanly than warm ones, so take them straight from the "
          "fridge, and lift a stray bit of shell out with the wet shell itself, which the white "
          "will not cling to.",
          avoid=("broke", "broken", "split", "how long", "boil", "poaching water", "freeze",
                 "freezer", "frozen", "keep", "keeps", "store", "storage", "left over",
                 "stiff", "stiffly", "stiffen", "stiffens", "stiffened", "stiffening",
                 "whisk", "whisks", "whisking", "whisked", "whip",
                 "whipping", "whipped", "peak", "peaks", "meringue", "souffle", "overbeat",
                 "fold", "folds", "folding", "folded", "leftover", "leftovers"),
          bias=1),
    entry("meringue-stiffen",
          (("meringue", "meringues", "meringue mix", "meringue mixture"),
           ("stiffen", "stiffens", "stiff", "stiffly", "peak", "peaks", "wont stiffen",
            "not stiff", "floppy", "collapse", "collapsed", "whip", "whisk", "beating",
            "flat", "went flat", "gone flat", "falls flat", "fell flat", "sank", "has sunk",
            "sunk", "deflated")),
          "Whip the whites in a spotless dry bowl - any trace of yolk, grease or water stops them "
          "stiffening - add a pinch of cream of tartar or a drop of lemon, then add the sugar a "
          "spoonful at a time once they hold soft peaks and stop the moment the whisk pulls up a "
          "stiff point that stands on its own: over-whisked whites go dry and collapse when you "
          "fold the sugar in.",
          avoid=("buy", "shop", "supermarket", "keep", "keeps", "store", "freeze", "frozen",
                 "calories", "recipe for", "nest", "eton", "pavlova", "lemon meringue",
                 "how do i make meringues", "how to make meringues", "make meringues")),
    entry("hummus-grainy",
          (("hummus", "houmous", "humous"),
           ("grainy", "gritty", "lumpy", "bitty", "not smooth", "smooth", "chalky")),
          "Blend it far longer than feels sensible - 3 to 4 minutes in a food processor, scraping "
          "down twice - and add 2 to 3 tablespoons of iced water while it runs: graininess is "
          "under-blending and a paste that is too dry, and rubbing the skins off the chickpeas "
          "before you blitz them takes it the rest of the way.",
          avoid=("recipe", "calories", "healthy", "keep", "keeps", "freeze", "frozen", "store",
                 "tin of", "tahini", "what is in")),
    entry("freeze-hummus", (("hummus", "houmous", "humous"),
                            ("freeze", "freezer", "frozen", "defrost", "keep", "how long",
                             "storage", "store", "shelf life", "shelf-life")),
          "Hummus keeps about a week in the fridge in a sealed tub, and it freezes well for "
          "about four months. To freeze it, smooth it flat in a tub, thaw it overnight in the "
          "fridge and stir it well, adding a squeeze of lemon and a splash of water when it comes "
          "back, since it returns a little grainy. Leave off the pool of oil and the swirl until "
          "you serve it, because they separate.",
          avoid=("recipe", "make", "calories", "healthy")),
    entry("roast-cauliflower", (("cauliflower", "cauliflowers"),
                                ("whole", "how long", "roast", "oven", "bake", "time",
                                 "temperature", "cook")),
          "A whole head takes about 45 minutes at 200C (180C fan): rub it all over with oil, salt "
          "and pepper, sit it stalk down in a tray and cover it with foil for the first 25 minutes, "
          "then uncover it so the outside browns. It is done when a knife goes in with no "
          "resistance. Florets tossed in oil take 25 minutes at the same heat.",
          avoid=("what can i make", "what can i do with", "ideas", "leftover", "cheese sauce",
                 "soup", "rice", "mash",
                 "keep", "keeps", "keeping", "fridge", "freezer", "freeze", "store", "storage",
                 "go off", "gone off", "boil", "boiled", "boiling", "steam", "steamed",
                 "steaming", "microwave", "puree", "pureed", "rice",
                 "air fryer", "airfryer", "air-fryer")),
    entry("bake-fruit", (("apple", "apples", "bramley", "bramleys", "cooking apple",
                          "cooking apples", "baked apple", "baked apples",
                          "pear", "pears", "plum", "plums", "peach", "peaches", "nectarine",
                          "nectarines", "quince", "quinces", "baked pear", "baked pears",
                          "baked plum", "baked plums", "baked peach", "baked peaches"),
                          ("bake", "baked", "baking", "oven", "roast", "roasted", "how long",
                           "temperature", "temp", "time", "gas mark", "stew", "stewed", "poach",
                           "poached", "microwave", "core", "cored", "how hot", "soft")),
          _bake_fruit,
          avoid=("keep", "keeps", "keeping", "fridge", "freezer", "freeze", "store", "storage",
                 "go off", "gone off", "pie", "tart", "crumble",
                 "toffee", "cider", "juice", "chutney", "air fryer", "airfryer", "air-fryer",
                 "tomato", "tomatoes", "paste", "melba", "tree", "trees", "jam",
                 "smoothie", "yoghurt", "yogurt", "brandy", "stone fruit", "prune", "prunes",
                 "damson", "damsons", "greengage", "greengages",
                 "plum pudding", "steamed pudding", "christmas pudding", "summer pudding"),
          ask=("how long", "how hot", "time", "temperature", "temp", "bake", "baked", "baking",
               "oven", "roast", "stew", "stewed", "poach", "microwave", "gas mark", "soft"),
          guard=_a_soft_fruit_is_still_a_cooking_question),
    entry("slow-roast", (("slow roast", "slow-roasted", "slow roasted", "slow cooking",
                          "pot roast", "casserole", "shoulder of lamb", "lamb shoulder",
                          "shoulder of pork", "pork shoulder", "shoulder of beef"),
                         ("oven", "temperature", "how hot", "what temp", "gas mark", "heat",
                          "setting", "how do i cook", "how do i roast", "how to cook",
                          "how to roast", "how long", "best way to cook", "best way to roast",
                          "how do i slow roast", "how do i slow cook", "slow roast", "slow cook")),
          "Set the oven to 150C (130C fan, gas 2) for a slow roast: lower than that and the meat "
          "sits in the danger zone for hours, higher and the outside dries before the middle "
          "softens. A covered pot keeps it moist, and a shoulder of lamb or pork or a beef "
          "brisket wants 4 to 5 hours. It is ready when a fork twists easily in the middle.",
          avoid=("slow cooker", "crockpot", "crock pot", "air fryer")),

    entry("non-stick-pan", (("non stick", "nonstick", "teflon", "non-stick", "pan coating",
                             "coating on my pan", "coating is coming off",
                             "scratched pan", "scratched pans", "pan is scratched",
                             "pan has a scratch", "pans are scratched", "scratch in my pan",
                             "scratches in my pan", "scratches on my pan", "pan is scratched up",
                             "coating has come off", "coating came off", "coating has gone",
                             "coating is gone", "pan has lost its coating",
                             "lost its coating", "lost the coating", "bits of coating"),
                            ("clean", "cleaning", "wash", "washing", "scratch", "scratched",
                             "scratches", "scrub", "scouring", "burnt", "stained", "coating",
                             "flaking", "peeling", "stick", "sticking", "safe", "safety",
                             "still use", "use it", "throw away", "throwing away", "bin it",
                             "replace", "replacing", "worn", "bits", "coming off", "flakes")),
          _non_stick_pan, bias=1),
    entry("cast-iron-pan", (("cast iron", "cast-iron", "skillet", "griddle pan"),
                            ("clean", "washing", "wash", "soap", "soapy", "rust", "rusty", "rusts",
                             "season", "seasoning", "seasons", "reseason", "re-season", "restore",
                             "stick", "sticking", "sticks",
                             "strip", "stripped", "oily", "dry", "scrub", "black", "dishwasher",
                             "dishwashers",
                             "look after", "looks after", "looking after", "care", "caring",
                             "care for", "maintain", "maintenance", "keep it", "look",
                            "wet", "leave", "leaves", "leaving", "left", "overnight", "soak",
                            "soaks", "soaking", "soaked")),
          ("Scrub it with hot water and a stiff brush or a handful of coarse salt while it is still "
           "warm, then dry it on the hob over a low heat: a little washing-up liquid is fine, but "
           "soaking it is what strips the seasoning. To season it, rub a thin film of oil over the "
           "inside and bake it upside down at 200C for an hour, then do it once more. If it rusts, "
           "scrub the rust off first and season it the same way afterwards. Keep it out of the "
           "dishwasher: the detergent strips the seasoning off and the pan comes out with rust "
           "spots. A wok wants exactly this care too."), bias=1,
          avoid=("plant", "plants", "aspidistra", "houseplant", "leaves", "leaf", "compost",
                 "wok", "woks", "carbon steel", "carbon steel wok",
                 "watered", "garden")),
    entry("season-new-pan", (("season", "seasoning", "cure", "curing", "first use", "new pan"),
                             ("pan", "pans", "frying pan", "saucepan", "non stick", "nonstick",
                              "new", "wok", "skillet", "griddle")),
          "Wash off the factory oil in hot soapy water first. If it is cast iron or carbon steel, "
          "rub a thin film of flavourless oil over it and heat it until it just smokes, then let it "
          "cool and repeat two or three times - that is the seasoning. A non-stick pan is not "
          "seasoned at all: washing it is enough, and high heat is what ruins the coating.",
          avoid=("cast iron", "cast-iron"), guard=_not_a_season_of_a_show, bias=1),
    entry("burnt-smell", (("smell", "kitchen", "house", "flat", "room"),
                          ("burnt", "burning", "smoky", "smoke")),
          ("Open the windows and run the extractor fan, then simmer a pan of water with a splash of "
           "vinegar or a sliced lemon for ten minutes, which clears the air faster than air freshener. "
           "Wash whatever was in the oven, and leave a bowl of bicarbonate of soda in the kitchen "
           "overnight to take the last of it out of the air.")),
    entry("simmer-or-boil",
          (("simmer", "simmering", "simmered"),
           ("boil", "boiling", "boils", "difference", "rolling", "gentle", "between",
            "same thing", "mean", "means")),
          "A boil is a churn of big bubbles you cannot stir down; a simmer is a lazy tremble of "
          "small bubbles, about 90C against 100C. Stews, sauces and rice want the simmer, because "
          "a hard boil toughens meat and breaks the grains, while pasta and potatoes want the "
          "boil. When in doubt turn it down until the bubbles just keep coming.",
          avoid=("soup maker", "slow cooker", "air fryer")),
    entry("learn-to-cook",
          (("learn to cook", "learning to cook", "never cooked", "cant cook", "can't cook",
            "cook from scratch", "proper meals", "cooking basics", "basic cooking",
            "better at cooking", "where do i start cooking",
            "rubbish at cooking", "useless in the kitchen", "hopeless at cooking",
            "no good at cooking", "cannot cook", "can not cook", "cant really cook",
            "will never be able to cook",
            "how do i cook properly", "cook properly", "how do i cook for myself",
            "how do i learn to cook", "teach me to cook", "how do i get into cooking",
            "i want to learn to cook", "how do i start cooking", "how do i cook",
            "how do i cook something"),
           ("how", "what", "start", "should", "first", "beginner", "learn", "want", "where",
            "improve", "get better", "no idea", "simple", "easy",
            "cant", "can't", "cannot", "at all", "rubbish", "useless", "hopeless", "no good")),
          _learn_to_cook,
          avoid=("beans", "dried beans", "black beans", "kidney beans", "butter beans",
                 "haricot", "cannellini", "pinto", "split peas", "chickpeas", "chick peas",
                 "lentils", "lentil",
                 "reheat", "freeze", "frozen", "calories", "calorie", "oven", "air fryer",
                 "slow cooker", "microwave", "how long", "how much", "cost", "recipe for",
                 "restaurant", "takeaway", "meal plan", "for one"),
          bias=-2),
    entry("first-curry",
          (("curry", "curries"),
           ("easy", "never made", "never cooked", "first time", "simple", "beginner", "basic",
            "someone who", "no idea")),
          "Start with a chickpea or chicken curry built on four things: onion, garlic, ginger and "
          "a spoon of curry powder. Soften a chopped onion in oil for 8 minutes, add the garlic, "
          "ginger, a teaspoon of curry powder and one of cumin for a minute, then the chicken or "
          "a drained tin of chickpeas, a tin of tomatoes and 100ml of stock, and simmer 20 "
          "minutes. Stir yoghurt in off the heat at the end, and taste for salt.",
          avoid=("stain", "stains", "smell", "freeze", "left out", "reheat", "microwave",
                 "calorie", "calories", "healthy", "restaurant", "takeaway")),
    entry("pudding-store-cupboard",
          (("pudding", "dessert", "something sweet", "for afters", "afters to eat"),
           ("what i have", "i have", "i've got", "ive got", "nothing in", "store cupboard",
            "cupboard", "whatever", "left over", "leftover", "in the house", "no eggs")),
          "Eve's pudding is the one to know when the cupboard is thin: sliced apple or any fruit "
          "in a dish, then a sponge of 100g each of butter, sugar and self-raising flour with 2 "
          "eggs spread over the top, baked 40 minutes at 180C (160C fan). With no flour at all, "
          "halved bananas baked with butter, brown sugar and a pinch of cinnamon take 15 minutes.",
          avoid=("christmas", "shop", "buy", "restaurant", "calorie", "calories", "sugar free",
                 "custard powder", "black pudding", "yorkshire",
                 "bloating", "bloated", "wind", "farting", "trapped wind", "nausea", "sick",
                 "ill", "stomach", "cramps", "diarrhoea", "constipated", "reflux", "heartburn",
                 "intolerance", "allergy", "allergic", "food poisoning")),
    entry("rice-sticky", ("rice", ("sticky", "sticking", "sticks", "stick to the pan", "gluey",
                                  "mushy",
                                  "clumpy", "clumped", "clumps", "a clump", "goes clumpy",
                                  "keeps going clumpy", "gone clumpy", "all clumped together",
                                  "keeps going sticky", "keeps coming out sticky",
                                  "keeps turning out sticky", "always comes out sticky",
                                  "comes out sticky", "came out sticky", "turns out sticky",
                                  "turned out sticky", "sticky again", "keeps sticking")),
          "Rinse the rice until the water runs clear, cook it 1 part rice to 1.5 parts water with "
          "the lid on, and leave it alone: 12 minutes on a low simmer, then 10 minutes off the "
          "heat. Stirring while it cooks is what makes rice gluey.", bias=1),
    entry("sticky-rice",
          (("sticky rice", "glutinous rice", "glutinous", "sweet rice", "sticky rice flour"),
           ("cook", "cooking", "make", "how", "steam", "steaming", "soak", "soaking", "need",
            "water", "long", "rice cooker", "basket", "what", "which", "best", "kind", "type")),
          "Soak it first, then steam it: four hours or overnight in cold water, drained, spread in "
          "a lined bamboo basket or on a cloth over a pan of boiling water, and steamed for 20 to "
          "25 minutes until it is translucent and chewy. It is a different grain from ordinary "
          "rice - short, opaque and chalky - and it is never boiled or stirred, which is what makes "
          "it a sticky ball rather than a pot of mush. In a hurry, an hour in warm water does the "
          "job, and a rice cooker with a sticky-rice setting takes 1 part rice to 1 part water and "
          "does the steaming for you.",
          avoid=("went sticky", "goes sticky", "go sticky", "came out sticky", "turned sticky",
                 "too sticky", "why is my rice", "keep", "freeze", "fridge", "leftover",
                 "left over", "reheat", "safe", "how long does",
                 "sushi", "nigiri", "maki", "onigiri"),
          bias=1),
    entry("rice-leftover", ("rice", ("leftover", "left over", "yesterday", "spare")),
          ("Yesterday's rice makes great fried rice: heat a little oil, add the cold rice and fry it "
           "hard for 3 minutes without stirring much, then push it aside and scramble an egg in the "
           "gap with soy sauce, peas or whatever vegetables you have."),
          avoid=("freeze", "freezer", "frozen", "defrost", "fridge", "keep", "store",
                 "storage", "reheat", "safe", "how long", "tomorrow", "next day")),
    entry("rice-left-out", ("rice", ("left out", "overnight", "all night", "room temperature",
                                     "sat out")),
          "Rice left out at room temperature is the one leftover worth being strict about: bin it "
          "after 2 hours. Cooked rice can grow a toxin that reheating doesn't destroy, so cool any "
          "leftovers fast, fridge them within the hour, and eat them within a day.",
          avoid=("rinse", "rinsing", "washing",
                 "dry", "uncooked", "raw", "before cooking"),
          guard=soak_but_not_left_out),
    entry("rice-soak", (("soak", "soaking", "soaked"),
                        ("rice", "basmati", "jasmine", "long grain", "brown rice", "pilau",
                         "biryani", "pilaf", "white rice", "rice cooker", "sushi rice")),
          "Long grain, basmati and jasmine rice do not need soaking - rinse it in a sieve until "
          "the water runs clear and cook it straight away, and that rinse is what stops it going "
          "sticky. Soak when the dish asks for it: about 30 minutes for pilau or biryani, and an "
          "hour or two for brown rice, then use a little less water because the grains already "
          "hold some. Do not leave raw rice sitting in water overnight on the counter - do it in "
          "the fridge if you want to get ahead.",
          avoid=("leftover", "left over", "left out", "left it out", "left it", "cooked",
                 "fridge", "freezer", "freeze",
                 "reheat", "keep", "keeps", "pudding", "risotto", "sushi", "sticky", "soggy",
                 "microwave", "how long does it keep"),
          bias=1),
    entry("pasta-soak", (("soak", "soaking", "soaked"),
                         ("pasta", "spaghetti", "penne", "macaroni", "noodles", "linguine",
                          "fusilli", "tagliatelle", "orzo")),
          "Dried pasta does not need soaking: it cooks in 8 to 12 minutes in salted boiling "
          "water, and soaking it first just makes it pale and floppy. If it is cooked pasta you "
          "mean, it keeps 3 days in the fridge, and anything that sat out for more than 2 hours "
          "gets binned.",
          avoid=("left out", "left it out", "leftover", "left over", "reheat", "fridge",
                 "freezer", "freeze", "sauce", "salad", "bake", "oven", "cheese")),
    entry("pasta-rinse", (("rinse", "rinsing", "rinsed", "wash", "washing", "washed"),
                          ("pasta", "spaghetti", "penne", "macaroni", "linguine", "fusilli",
                           "tagliatelle", "orzo", "noodles")),
          "No, pasta does not need rinsing: it comes out of the pot already wet, and rinsing "
          "cools it and washes off the surface starch that makes a sauce cling. Drain it and "
          "toss it straight into the sauce, keeping a mugful of the cooking water to loosen "
          "things if it looks dry. The one exception is pasta for a cold salad, where a quick "
          "rinse under cold water stops it clumping - then drain it well and dress it while it "
          "is still slightly warm so it takes up the dressing.",
          avoid=("left out", "leftover", "left over", "reheat", "fridge", "freezer", "freeze",
                 "how long", "tomorrow", "sauce", "bake", "oven", "cheese", "jar", "jars",
                 "tinned", "tin"),
          ask=("rinse", "rinsing", "rinsed", "wash", "washing", "washed",
               "cold water", "with cold water", "under cold water", "under the tap", "tap",
               "salad", "for a salad",
               "can i", "can we", "could i", "is it ok", "is it okay", "ok to", "okay to"),
          bias=3),
    entry("pasta-drain", (("drain", "draining", "drained", "strain", "straining", "strained",
                           "colander", "sieve"),
                          ("pasta", "spaghetti", "penne", "macaroni", "noodles", "linguine",
                           "fusilli", "tagliatelle", "orzo", "shells")),
          "Scoop out a mugful of the cooking water first, then tip the pasta into a colander in "
          "the sink: that cloudy water is what loosens a sauce that has gone too thick. Shake it "
          "once, do not rinse it, and get it back into the warm pan with the sauce straight "
          "away, because drained pasta starts sticking to itself within a minute. Never leave it "
          "sitting in the colander - it carries on cooking in its own heat and goes soft.",
          avoid=("rinse", "rinsing", "rinsed", "wash", "washing", "washed",
                 "left out", "leftover", "left over", "reheat", "fridge", "freezer", "freeze",
                 "how long", "minutes", "salt", "boil", "boiling", "portion", "how much",
                 "sauce recipe", "bake", "oven", "cheese"),
          ask=("drain", "draining", "drained", "strain", "straining", "strained", "colander",
               "sieve")),
    entry("soak-nuts", (("soak", "soaking", "soaked"),
                        ("cashews", "cashew", "almonds", "almond", "walnuts", "walnut", "nuts",
                         "peanuts", "peanut", "raisins", "raisin", "sultanas", "sultana",
                         "dates", "prunes", "apricots", "dried fruit")),
          "Nuts and dried fruit are safe to soak and nothing spoils while they do it: cover them "
          "in water, keep them in the fridge, and they are soft by morning. Almonds slip their "
          "skins after a night in water, cashews blend smoother for a sauce, and raisins or "
          "dates plump up in warm water in about 20 minutes.",
          avoid=("allergy", "allergic", "anaphylactic", "calories", "protein", "rancid",
                 "gone off", "gone bad", "mouldy", "stale", "bitter", "left out", "left it")),
    entry("pasta-left-out", (("pasta", "spaghetti", "penne", "macaroni", "noodles"),
                             ("left out", "overnight", "all night", "room temperature", "sat out")),
          "Bin it, I'm afraid: cooked pasta left out for more than 2 hours isn't worth eating, "
          "even if it looks and smells fine. Get leftovers into the fridge within the hour next "
          "time and they keep 3 days.",

          avoid=("fridge", "in the fridge", "refrigerator"),
          guard=soak_but_not_left_out),
    entry("fridge-hot-food",
          (("hot food", "warm food", "hot leftovers", "leftovers", "hot pot", "hot pan",
            "warm pot", "warm pan", "warm dish", "warm container", "warm pot of", "warm pan of",
            "warm soup", "warm stew", "warm casserole", "warm curry", "warm rice", "warm pasta",
            "the pot", "a pot", "the pan", "a pan", "the stew", "a stew", "the curry",
            "the soup", "a soup", "the casserole",
            "hot soup", "hot stew", "hot casserole", "soup", "stew", "casserole", "chilli",
            "curry", "rice", "pasta", "food"),
           ("fridge", "refrigerator", "put in the fridge", "put it in the fridge", "go in the fridge",
            "in the fridge", "cool", "cooling", "cool down", "cool it down", "let it cool",
            "leave it to cool", "straight in", "put away",
            "cool right down", "cool before", "cool first", "let the pot cool",
            "let the pan cool", "goes in the fridge", "go in the fridge")),
          "Straight in is fine - a modern fridge copes with a warm pot, and food left on the "
          "counter to cool is the bigger risk. Split a big batch into shallow boxes so it drops "
          "below 5C within 90 minutes, cover it loosely while it is still warm, and keep it away "
          "from the milk and the cooked meat on the shelf below. The rule is cool it fast, not "
          "cool it first.",
          avoid=("how does", "how do fridges", "compressor", "freezer", "freeze", "defrost",
                 "too spicy", "too hot to eat", "too salty", "too much salt", "too bland",
                 "too sweet", "too sour", "too much chilli", "too much chili", "less spicy",
                 "make it milder", "way too spicy", "way too salty",
                 "reheat", "microwave", "how long", "how many days", "recipe", "what can i make",
                 "eat", "safe to eat", "ok to eat", "why is my fridge", "not cold", "frost",
                 "smell", "ice", "left out", "out overnight", "left overnight",
                 "overnight on the counter", "rice left out", "toppings",
                 "reheat in", "pasta bake", "sauce for",
                 "before washing", "before i wash", "before washing up", "washing up",
                 "wash it", "wash the pan", "washing the pan", "in the sink", "the sink",
                 "is it still ok", "is it still good", "still ok", "still good",
                 "ok after", "good after", "since friday", "since yesterday",
                 "since monday", "since tuesday", "since wednesday", "since thursday",
                 "since saturday", "since sunday", "for 2 days", "for two days", "for 3 days",
                 "for three days", "for 4 days", "for four days", "leftover", "left over",
                 "leftovers in the fridge", "cooked rice in the fridge",
                 "rice", "milk", "bottle", "bottles", "formula", "baby", "cake", "cakes",
                 "sponge", "muffin", "cupcake", "brownie", "bread", "loaf"),
          bias=2,
          guard=lambda reading: (not reading.get("kept")
                                 and a_cooling_question_not_a_keeping_one(reading))),
    entry("bbq-sticking",
          (("barbecue", "barbecues", "barbeque", "bbq", "bbqs", "grill", "grill bars",
            "barbecue grill", "charcoal grill", "gas grill"),
           ("stick", "sticks", "sticking", "stuck", "stick to")),
          "Oil the food, not the bars: get the grill hot, brush the bars clean, then brush the "
          "meat, fish or veg itself with a little oil and put it on. Leave it alone for three or "
          "four minutes - it frees itself once it has sealed - then turn it with tongs rather than "
          "a fork, and keep a spray bottle of water for flare-ups.",
          avoid=("clean", "cleaning", "scrub", "rust", "rusty", "winter", "store", "read",
                 "book", "chapter", "revision", "revise", "remember", "study", "exam",
                 "oven", "grill pan", "hob", "toast", "cheese on toast", "bacon", "pasta",
                 "rice", "cake", "dough", "how long", "temperature", "recipe", "marinade"),
          bias=3),
    entry("rice-cooked-tomorrow",
          ("rice", ("ok tomorrow", "tomorrow ok", "safe tomorrow", "the day after", "day after",
                    "still ok the day after", "still good the day after")),
          _COOKED_RICE_KEEPS,
          avoid=("water", "minutes", "how long to cook", "pot",
                 "pan", "ratio", "rinse", "raw", "dry", "uncooked", "bag", "packet", "pack",
                 "jar", "airtight", "cupboard", "larder", "past its date", "past the date",
                 "after the date", "out of date", "expired", "opened", "open for", "weevils",
                 "year", "years", "months", "idea", "ideas", "make with", "do with", "use up",
                 "what can i", "anything i can", "recipe", "recipes", "fry", "fried", "freeze",
                 "freezing", "freezer", "burnt", "burned", "burnt bits", "slimy", "smell",
                 "smells", "pudding", "milk", "sugar", "phone", "cat", "dogs", "dog", "cats",
                 "bird", "birds", "pets", "the washing", "laundry", "curry", "sushi",
                 "risotto", "paella", "bake", "baked", "salad"),
          bias=2),
    entry("rice-cooked-still-ok",
          ("rice", ("still ok", "still good", "still be ok", "still safe", "safe to eat",
                    "ok to eat")),
          _COOKED_RICE_KEEPS,
          avoid=("water", "minutes", "how long to cook", "pot", "pan", "ratio", "rinse", "raw",
                 "dry", "uncooked", "bag", "packet", "pack", "jar", "airtight", "cupboard",
                 "larder", "weevils", "year", "years", "months", "idea", "ideas", "make with",
                 "do with", "use up", "recipe", "recipes", "fry", "fried", "freeze", "freezer",
                 "burnt", "burned", "slimy", "smell", "smells", "pudding", "milk", "sugar",
                 "curry", "sushi", "risotto", "paella", "bake", "salad"),
          bias=2,
          guard=_the_rice_was_cooked),
    entry("rice-storage", ("rice", ("leftover", "left over", "reheat", "next day", "yesterday",
                                    "gone off", "safe to eat", "ok to eat", "again", "keep",
                                    "leave", "leaves", "leaving", "for 2 days", "for two days",
                                    "for 3 days", "for three days", "few days", "a day",
                                    "fridge", "last", "lasts", "store", "storing", "freeze",
                                    "freezing", "safe", "safe to eat", "how long does cooked rice",
                                    "shelf life", "shelf-life", "good for")),
          ("Cool cooked rice fast and box it: it keeps 24 hours in the fridge, no longer, and "
           "you reheat it once until it's piping hot all the way through. Rice left out at room "
           "temperature is the one leftover worth being strict about."),
          avoid=("cupboard", "larder", "bag", "tin", "dry", "uncooked", "raw", "buy", "curry",
                 "with curry", "wash", "washing", "rinse", "rinsing", "rice cooker",
                 "leave it", "left it", "phone", "mobile", "iphone", "bath", "battery",
                 "wont turn on")),
    entry("pasta-portion", (("pasta", "spaghetti", "penne", "noodles"),
                            ("per person", "portion", "how much", "much", "person", "serving",
                             "handful")),
          ("Allow 75 to 100g of dry pasta per person as a main, or 50g as a starter: a bunch of "
           "spaghetti as thick as a 10p coin is about 80g. Pasta roughly doubles in weight when "
           "cooked, so a 500g packet feeds four or five."),
          avoid=("sauce", "dressing", "salad", "water", "pan", "salted", "salt", "boiling")),
    entry("pasta-water", (("pasta", "spaghetti", "penne", "noodles", "macaroni", "fusilli"),
                          ("water", "pan", "how much water", "litre", "litres", "salt", "salted",
                           "boiling", "rolling boil", "stick", "sticks", "sticking")),
          "About a litre of water for every 100g of pasta: a big pan filled about two thirds, at "
          "a rolling boil before the pasta goes in, and a teaspoon of salt per four litres. Keep "
          "it boiling and stir for the first minute so the pieces do not stick together - there is "
          "no need for oil in the water, which only makes the sauce slide off.",
          avoid=("per person", "portion", "sauce", "dressing", "salad", "bake", "lasagne",
                 "lasagna", "soup", "pudding", "how long", "gluten")),
    entry("slow-cooker-burning", (("slow cooker", "slow cookers", "slow-cooker", "crockpot",
                                   "crock pot", "slowcooker"),
                                  ("burn", "burns", "burning", "burnt", "burned", "sticking",
                                   "sticks", "stuck", "catch", "catches", "catching", "caught",
                                   "dried out", "drying out", "dry out", "scorch", "scorched",
                                   "overcook", "overcooked", "too hot", "on the bottom",
                                   "the bottom")),
          "Nearly always too little liquid: the food should be at least a third covered, and the "
          "pot no more than two thirds full. Cook on low rather than high, keep the lid on (every "
          "lift loses about 20 minutes of heat), and add milk, cream or flour in the last half "
          "hour, because dairy and thickeners are what catch. A liner or a smear of oil stops the "
          "edges sticking, and if it only ever burns round the sides the pot is thin-based and "
          "running hot - a tea towel under it or a new pot fixes that.",
          avoid=("left on", "leave on", "left it on", "overnight", "all night", "all day",
                 "while im out", "while i am out", "safe", "recipe", "recipes",
                 "what can i cook", "what to cook", "dinner ideas", "clean", "cleaning",
                 "smell", "smells", "what can i make"),
          bias=1),
    entry("rice-portion", ("rice", ("per person", "portion", "much", "person", "serving")),
          "Allow about 75g of dry rice per person, or a mugful for two: it swells to two or three "
          "times its size, and leftover rice is better under- than over-estimated."),
    entry("rice-water", ("rice", ("water", "ratio", "much water", "how long", "long", "time",
                                  "takes", "take", "cook")),
          _rice_time,
          avoid=("fridge", "keep", "keeps", "keep for", "leftover", "left out", "freeze", "freezer",
                 "leave it", "leave it in", "left it in", "phone", "mobile", "iphone", "device",
                 "battery", "bath", "water damage", "wont turn on", "drained",
                 "pudding", "paella", "risotto", "pilau", "sushi", "milk", "sugar",
                 "cooker", "microwave", "pressure", "steamer", "instant",
                 "uncooked", "store", "storing", "stored", "last", "lasts", "jar", "airtight",
                 "wild", "cauliflower", "noodles")),
    entry("quinoa", ("quinoa", ("cook", "water", "time", "bitter")),
          "Rinse quinoa well, simmer it in twice its volume of salted water for 15 minutes, then "
          "drain and let it steam with the lid on for 5. Rinsing takes off the bitter coating; the "
          "grains are done when the little tails pop out."),
    entry("porridge", (("porridge", "oats", "oatmeal"), ("water", "milk", "creamy", "lumpy",
                                              "cook", "gluey", "stodgy", "thick", "stirring",
                                              "microwave", "make", "how long", "time")),
          _porridge,
          avoid=("what can i make", "what else", "ideas", "recipes", "biscuits", "cookies",
                 "flapjack", "granola", "muesli", "bread", "cakes", "muffins",
                 "as good", "better than", "instead of", "good for", "healthy", "fattening",
                 "which milk",
                 "overnight", "soak", "soaked", "soaking", "no cook", "uncooked",
                 "cold water", "jar", "baby", "babies", "weaning", "wean", "toddler",
                 "toddlers", "under one", "6 months", "six months", "first foods",
                 "blw", "puree")),
entry("porridge-fault",
          (("porridge", "porridge oats", "oats", "oatmeal", "ready brek", "readybrek",
            "oat so simple", "overnight oats"),
           ("too much sugar", "too sweet", "sweet", "sugary", "over sweet", "oversweet",
            "too much honey", "honey", "golden syrup", "jam", "syrup",
            "too salty", "salty", "too much salt", "over salted", "oversalted", "salt",
            "bland", "tastes of nothing", "no taste", "tasteless", "nothing in it")),
          _porridge_fault,
          avoid=("how do i make", "how to cook", "how do i cook", "how long", "microwave",
                 "what can i make", "what else", "ideas", "recipe", "recipes", "biscuits",
                 "cookies", "flapjack", "granola", "muesli", "bread", "cakes", "muffins",
                 "healthy", "healthier", "fattening", "calories", "good for you", "which milk",
                 "as good", "better than", "instead of", "baby", "babies", "weaning", "toddler",
                 "lumpy", "gluey", "stodgy", "watery", "too thin", "too thick", "thick",
                 "sauce", "soup", "stew", "curry", "bread sauce"),
          bias=2),
    entry("overnight-oats",
          (("oats", "oat", "oatmeal", "porridge", "bircher"),
           ("soak", "soaked", "soaking", "overnight", "jar")),
          _overnight_oats,
          avoid=("boil", "boiled", "cook oats", "cooking oats", "cooked oats", "how do i cook",
                 "how to cook", "how long do oats", "how long does porridge", "microwave",
                 "simmer", "lumpy",
                 "creamy", "stodgy", "gluey", "baby", "babies", "toddler", "weaning", "wean",
                 "coeliac", "celiac", "gluten", "allergy", "allergic", "reaction", "rash",
                 "fattening", "calories", "how many calories", "weight",
                 "flapjack", "flapjacks", "biscuits", "cookies", "muffins", "bread",
                 "granola", "muesli")),
    entry("couscous", ("couscous", ("cook", "water", "fluffy", "lumpy")),
          "Pour boiling water or stock over the couscous to just cover it, cover the bowl and leave "
          "it 5 minutes, then fork it through with a little olive oil. Never stir it with a spoon: "
          "that's what makes it clumpy."),
    entry("pasta-salt", (("pasta", "spaghetti", "penne", "noodles", "salt the water",
                          "salting the water", "salted the water", "salt in the water",
                          "water for pasta", "pasta water"),
                          ("salt", "salted", "salty")),
          ("Salt the water properly: about 10g, a heaped teaspoon, per litre of boiling water, so a "
           "big pan takes a good tablespoon. That is what seasons the pasta itself, since it takes "
           "up the salt while it cooks. Add it once the water is boiling so it dissolves fast, and "
           "taste the water - it should taste like the sea, not like a mistake."),
          avoid=("rice", "potato", "potatoes", "veg", "vegetables", "beans", "peas", "broccoli",
                 "egg", "eggs", "blanch", "blanching", "bread", "dough", "cake", "stock"),
          bias=2),
    entry("pasta-cook", (("pasta", "spaghetti", "noodles", "linguine", "penne", "macaroni"),
                         ("water", "salt", "boil", "time", "cook", "lump", "lumps",
                          "sticking", "stick",
                                    "together", "clump", "clumps",
                          "long", "take", "takes", "minutes")),
          _pasta_cook,
          avoid=("portion", "portions", "per person", "how much", "serving",
                 "boil over", "boils over", "boiling over", "boiled over", "overflow", "overflows",
                 "spill", "spills", "spilling", "spilled", "spilt",
                 "sticks to the pan", "stuck to the pan", "sticking to the pan", "glued to the pan",
                 "bottom of the pan", "bottom of my pan", "saucepan",
                 "fridge", "in the fridge", "leftover", "left over", "next day", "gone off",
                 *(_DAY_BEFORE),
                 "for tomorrow", "until tomorrow", "til tomorrow", "till tomorrow",
                 "ok tomorrow", "okay tomorrow", "still ok tomorrow", "tomorrow ok",
                 "ok overnight", "okay overnight", "still ok overnight", "ok the next day",
                 "okay the next day", "keep overnight", "store overnight",
                 "in the fridge overnight", "overnight in the fridge",
                 "left out overnight", "sat out overnight",
                 "keep it", "keep the rest", "keep leftovers", "keep leftover",
                 "store it", "storing", "store the rest", "stored",
                 "keep cooked", "keeps cooked", "keeping cooked", "kept cooked",
                 "keep the cooked", "store cooked", "stores cooked", "storing cooked",
                 "stored cooked", "store the cooked",
                 "freeze", "freezing", "frozen", "freezer", "defrost", "defrosting",
                 "bake", "baked", "oven", "baking",
                 "last", "lasts", "lasting", "days", "day") + _MEAL_ASK_AVOID + WANT_SOMETHING_ELSE,
          bias=1),
    entry("pasta-keep", (("pasta", "spaghetti", "penne", "noodles", "macaroni"),
                         ("fridge", "keep", "store", "leftover", "left over", "next day", "last",
                          "safe", "reheat",
                          "the day after", "day after", "a day after", "day later",
                          "a day later", "the following day", "following day", "yesterday",
                          "last night",
                          "tomorrow", "overnight", "next morning")),
          ("Cooked pasta keeps 3 days in the fridge in a sealed box, tossed with a little oil so it "
           "doesn't clump. Reheat it in the sauce with a splash of water until piping hot, once "
           "only, and bin it if it smells sour or feels slimy."),
          ask=KEEP_ASK, bias=1,
          avoid=("fry", "fried", "make", "made", "recipe", "recipes", "ideas", "do with", "bake",
                 "baked", "use up", "turn into", "dry", "dried", "uncooked", "fresh", "opened",
                 "open packet", "packet", "cupboard", "larder", "tin", "jar",
                 "dish", "dishes", "a dish", "meal", "meals", "menu", "dinner", "supper",
                 "something to eat", "idea", "ideas",
                 "soak", "soaks", "soaking", "soaked",
                 ) + KEEP_QUALITY_WORDS),
    entry("pasta-sauce", (("pasta", "tomato sauce", "tomato sauces", "passata", "marinara",
                           "napoli sauce", "napolitana sauce",
                           "tinned tomatoes", "chopped tomatoes", "tin of tomatoes",
                           "simmered tomatoes", "tomatoes"),
                          ("sauce", "tomato", "quick", "dinner", "easy", "recipe",
                           "homemade", "from scratch", "tinned", "passata",
                           "simmer", "simmering", "boil", "boiling", "how long", "minutes",
                           "how many minutes", "cook", "cooking", "pan", "hob", "stir")),
          _tomato_sauce,
          avoid=("keep", "keeps", "keeping", "store", "storing", "stored", "fridge", "freezer",
                 "freeze", "frozen", "last", "lasts", "lasting", "tomorrow",
                 "overnight", "next day", "the day after", "gone off", "go off", "still ok",
                 "still good", "open jar", "opened jar", "jar of",
                 "out of date", "past the date", "after the date", "use by", "best before",
                 "expired", "date on",
                 "im making", "i am making", "pasta bake", "lasagne", "lasagna", "casserole",
                 "leftover", "leftovers", "use up", "do with", "make with", "what can i make",
                 "what should i make", "tray",
                 "stain", "stains", "stained", "shirt", "shirts", "carpet", "sofa",
                 "settee", "tablecloth", "splashed", "spilled", "spilt", "dripped", "got on",
                 "on my", "remove", "get out", "get off", "clean off", "wipe",
                 "thicker", "thick", "too thin", "watery", "reduce", "reduction",
                 "bland", "acidic", "bitter", "too sweet", "too sour", "sour", "salty",
                 "too salty", "split", "separated", "burnt", "burned", "caught", "gone wrong",
                 "healthy", "health", "good for you", "bad for you", "calories", "sugar",
                 "nutrition", "diet",
                 "pizza", "pizza base", "pizza bases", "for pizza")),
    entry("egg-cook", (("egg", "eggs"), ("cook", "cooking", "cooked")),
          "Boil them 6 minutes for a runny yolk or 9 to 10 for hard boiled, lowering them into "
          "water that is already boiling and cooling them under the tap before you peel. Frying "
          "is butter in a hot pan, 2 to 3 minutes for a runny yolk, and scrambling is low heat "
          "and slow stirring, off the heat while it is still glossy.",
          avoid=("boil", "boiled", "boiling", "fry", "fried", "frying", "poach", "poached",
                 "poaching", "scramble", "scrambled", "scrambling", "omelette", "microwave",
                 "hard", "soft", "runny", "yolk", "shell", "crack", "cracked", "separate",
                 "fresh", "float", "safe", "pregnant", "baby", "babies", "keep", "keeps",
                 "store", "storing", "leftover", "leftovers", "replace", "substitute", "vegan",
                 "allergy", "allergic", "rice", "fried rice")),
    entry("egg-boil", (("egg", "eggs"), ("runny", "soft", "boiled", "yolk", "dipping",
                                          "dippy")),
          "Lower eggs into already boiling water: 6 minutes for a runny yolk, 7 for jammy, 9 to 10 "
          "for hard boiled. Cool them in cold water for a minute before peeling so the shell comes "
          "away cleanly.",
          avoid=("good for", "keep", "keeps", "keeping", "last", "lasts", "fridge",
                 "use by", "out of date", "go off", "gone off",
                 "fry", "fried", "frying", "poach", "poached", "poaching", "scramble",
                 "scrambled", "omelette", "green", "grey", "gray") + _NUTRIENT_ASK_WORDS),
    entry("egg-boil-soft", (("egg", "eggs", "yolk", "yolks", "egg yolk", "egg yolks"),
                            ("soft", "soft boiled", "runny", "jammy")),
          "For a soft one, 5 to 6 minutes: 5 leaves the yolk running, 6 gives a set white with a "
          "soft middle. Cool it under cold water the moment it comes out, or it carries on cooking "
          "in its own heat.", bias=1,
          avoid=("safe", "safely", "ok", "okay", "fine", "risk", "pregnant", "pregnancy",
                 "baby", "babies", "toddler", "child", "children", "kids", "dipping soldiers",
                 "fry", "fried", "frying", "poach", "poached", "poaching", "scramble",
                 "scrambled", "omelette", "green", "grey", "gray", "ring", "peel", "peeling",
                 "good for", "keep", "keeps", "keeping", "last", "lasts", "fridge",
                 "use by", "out of date", "go off", "gone off") + _NUTRIENT_ASK_WORDS),
    entry("egg-crack-boiling", (("egg", "eggs"), ("crack", "cracks", "cracking", "cracked",
                                                  "split", "splits", "burst", "bursts", "bust",
                                                  "explode", "explodes", "exploded")),
          "Nearly always the air pocket at the fat end: prick that end with a pin first, lower "
          "them in on a spoon instead of dropping them, and take them out of the fridge ten "
          "minutes before so the shell is not cold when it meets the heat. Keep the water at a "
          "gentle simmer rather than a rolling boil, and a splash of vinegar in the pan sets any "
          "white that leaks before it trails.",
          ask=("boil", "boiling", "boiled", "pan", "pot", "water", "simmer"),
          avoid=("phone", "screen", "window", "wall", "pavement", "lips", "skin", "joke", "nuts",
                 "coconut", "cracker", "crackers", "carton", "box", "shell went in",
                 "bit of shell"),
          bias=1),
    entry("egg-scramble", (("egg", "eggs", "scrambled"), ("rubbery", "rubber", "tough", "dry",
                                                          "watery", "wet", "runny", "sloppy",
                                                          "fluffy", "scramble", "scrambling")),
          _scramble,
          avoid=("fry", "fried", "frying", "boil", "boiled", "boiling", "poach", "poached",
                 "poaching", "omelette", "omelet")),
    entry("egg-poach", (("egg", "eggs"), ("poach", "poached", "poaching")),
          "Bring a pan of water to a bare simmer with a splash of vinegar, stir it into a gentle "
          "whirlpool and slide the egg in from a cup. 3 minutes gives a soft yolk; lift it out with "
          "a slotted spoon onto kitchen paper."),
    entry("egg-fresh", (("egg", "eggs"), ("fresh", "float", "old", "test", "off", "bad", "rotten",
                                          "date", "dates", "expired", "keep", "keeps", "last",
                                          "lasts", "longer", "store", "storing", "safe")),
          _eggs),
    entry("omelette", (("omelette", "omelet"),
                       ("filling", "fillings", "easy", "make", "fold", "cook",
                        "long", "take", "takes", "time", "minutes", "put", "inside",
                        "flip", "flipping",
                        "how many")),
          "Two to three minutes in the pan: beat two eggs with a pinch of salt, pour them into a "
          "hot buttered pan and pull the set edges inwards with a spatula. Add cheese, mushrooms "
          "or ham on one half, fold it over and slide it out while the middle is still soft."),
    entry("creme-anglaise", (_EGG_SAUCE, ("make", "makes", "making", "how", "recipe", "method",
                                          "custard", "thicken", "thickens", "thickening")),
          "Warm 300ml double cream with a vanilla pod or a teaspoon of paste and 100ml of milk "
          "until it steams, and beat 4 egg yolks with 60g of sugar. Pour the hot cream into the "
          "yolks slowly, whisking, then put it back on a low heat and stir without stopping for 4 "
          "to 6 minutes, to about 82C, until it coats the back of the spoon. Strain it into a jug "
          "and it thickens as it cools.",
          avoid=("flour", "cake", "grainy", "gritty", "split", "curdled", "filling", "pie"),
          bias=1),
    entry("egg-dish-fault", (_EGG_DISH, _EGG_FAULT), _egg_fault,
          avoid=("chicken", "meat", "steak", "pork", "lamb", "beef", "turkey", "fish", "tofu",
                 "cake", "biscuit", "biscuits", "bread", "pasta", "rice", "potato", "potatoes",
                 "muffin", "muffins", "scrambled", "scrambling", "poached", "boiled", "microwave",
                 "skin", "hair"),
          bias=1),

    entry("chicken-done", ("chicken", ("temperature", "temp", "internal", "thermometer", "75",
                                       "74", "done", "cooked through",
                                       "know", "knowing", "tell", "check", "checking", "cooked")),
          ("Chicken is cooked when the thickest part reaches 75C on a digital thermometer, pushed "
           "into the thigh without touching bone; 74C held for a minute is the same thing. The "
           "juices run clear and no pink is left. A whole bird at 190C (170C fan) takes 20 minutes "
           "per 500g plus 20."), bias=1,
          ask=("know", "knowing", "tell", "check", "checking", "done", "cooked through",
               "temperature", "temp", "thermometer", "internal", "is my", "is the", "is it",
               "when is it done", "when its done"),
          avoid=("oven", "fan oven", "gas mark", "safe to eat", "is it safe", "left out",
                 "overnight", "pink", "raw", "fridge", "freezer", "frozen", "defrost", "keep",
                 "store", "breast", "thigh", "roast", "roasting", "roasted", "how long",
                 "kg", "whole bird", "per 500g", "minutes",
                 "already", "off", "gone off", "fresh", "smell", "smells",
                 "left", "out all night", "all night", "overnight", "room temperature",
                 "wash", "washing", "washed", "rinse", "rinsing")),
    entry("roast-chicken", ("chicken", ("how long", "time", "roast", "roasting", "cook", "oven",
                                        "per pound", "per lb", "pound", "minutes per")),
          _chicken_time, avoid=("pox", "wing", "soup", "stock", "salad", "nugget", "thigh",
                                "rest", "resting", "rested",
                                "skin", "skinless", "crispy", "crisp", "crackling", "golden",
                                "pale", "flabby", "soggy skin",
                                "breast", "leg", "legs", "drumstick", "drumsticks",
                                "tender", "tenders", "strip", "strips", "goujon", "goujons",
                                "fridge", "freezer", "frozen", "freeze", "leftover",
                                "left over", "left", "spare", "already cooked", "keep",
                                "shelf life", "shelf-life", "good for",
                                "off", "go off", "goes off", "going off", "gone off",
                                "defrost", "defrosting", "defrosted", "thaw", "thawing", "thawed",
                                "unthaw",
                                "curry", "casserole", "pie", "stew", "simmer", "soup",
                                "marinade", "marinate", "marinating", "marinated",
                                "how many pounds", "how many lb", "how many kilos", "how many kg",
                                "how many grams", "how many birds", "how many chickens",
                                "how many do i need", "how much chicken", "how much do i need",
                                "how much will i need", "per person", "each",
                                "air fryer", "airfryer", "air fry", "air frying") + WANT_SOMETHING_ELSE
                                + PET_LINE_WORDS),
    entry("chicken-tenders", (("chicken tenders", "chicken strips", "chicken goujons", "tenders",
                               "goujons"),
                              ("how long", "long", "time", "times", "minutes", "minute", "oven",
                               "cook", "cooking", "cooked", "bake", "baked", "baking", "fry",
                               "fried", "frying", "grill", "grilled", "grilling", "air fryer",
                               "airfryer", "air", "recipe", "recipes", "temperature", "temp",
                               "done", "way", "ways", "roast", "roasted", "make", "makes",
                               "making", "boil", "boiled", "boiling")),
          _tenders_method, guard=_tenders_are_a_piece,
          bias=3,
          avoid=("leftover", "left over", "leftovers", "already cooked", "use up", "using up",
                 "salad", "soup", "stock", "sandwich", "wrap", "dog", "cat", "puppy", "kitten",
                 "pet", "vet", "nugget", "nuggets", "wing", "pox", "defrost", "thaw", "frozen",
                 "freezer", "how many", "how much", "calories", "protein", "tough", "rubbery",
                 "chewy", "texture", "side dish", "sauce")),
    entry("chicken-stuffed", ("chicken", ("stuff", "stuffing", "stuffed")),
          "Stuff the neck end only and weigh the bird with the stuffing in: use the same 20 minutes "
          "per 500g plus 20, so usually 15 to 20 minutes longer. Check the stuffing is piping hot "
          "in the middle, not just the meat."),
    entry("chicken-breast", (("chicken breast", "chicken breasts", "chicken brest",
                              "chicken brests"), ("juicy", "dry", "how long", "moist",
                                                  "moisture", "cook", "time")),
          "Flatten chicken breasts to an even thickness, season them and roast at 200C (180C fan) "
          "for 18 to 20 minutes, or until the middle is 74C. Resting them for 5 minutes keeps the "
          "juice in; slicing them straight from the oven is what dries them out."),
    entry("chicken-thighs", ("chicken", ("thigh", "thighs")), _thighs, bias=1,
          avoid=("leftover", "left over", "leftovers", "already cooked", "next day",
                 "cold chicken", "what can i do with", "what can i make", "use up", "using up",
                 "soup", "stock", "sandwich", "salad")),
    entry("chicken-legs", ("chicken", ("leg", "legs", "drumstick", "drumsticks")), _legs, bias=1,
          avoid=("leftover", "left over", "leftovers", "already cooked", "next day",
                 "cold chicken", "what can i do with", "what can i make", "use up",
                 "soup", "stock", "sandwich", "salad",
                 "defrost", "thaw",
                 "dog", "dogs", "cat", "cats", "puppy", "kitten", "pet", "pets", "raw",
                 "thigh", "thighs", "breast", "breasts", "wing", "wings", "healthy",
                 "healthier", "curry", "casserole", "pie")),
    entry("chicken-defrost", ("chicken", ("defrost", "thaw", "frozen", "forgot", "forgotten",
                                          "forget", "forgetting", "forgot to take",
                                          "forget to take", "forgetting to take",
                                          "took it out", "take it out", "out of the freezer",
                                          "still in the freezer", "still frozen")),
          "Defrost chicken in the fridge overnight, on a plate on the bottom shelf, never on the "
          "worktop. Small pieces take a few hours, a whole bird a day or two; cook it as soon as it "
          "is thawed.",
          avoid=("year", "years", "month", "months",
                 "still good", "still ok", "ok after", "use by", "out of date",
                 "safe to eat", "still safe", "safe after", "is it safe after",
                 "how long can chicken", "how long can i keep", "how long can you keep",
                 "how long can i leave", "how long does chicken last",
                 "how long does chicken keep", "stay in the freezer",
                 "last in the freezer", "keep in the freezer", "leave in the freezer",
                 "in the freezer for")),
    entry("chicken-storage", ("chicken", ("fridge", "freezer", "freeze", "freezing", "frozen",
                                          "store", "keep", "stays", "stay", "lasts", "last",
                                          "storage", "storing", "stored",
                                          "uncooked", "shelf life", "shelf-life",
                                          "good for",
                                          "go off", "goes off", "going off", "gone off")),
          "Raw chicken keeps 1 to 2 days in the fridge, on the bottom shelf, and cooked chicken "
          "3 days; both freeze well for up to 3 months. Go by the use-by date on the pack, which "
          "beats any general rule.",
          avoid=PET_LINE_WORDS + ("moist", "moisture", "juicy", "tender",
                                  "chicken out", "chickening out", "chickened out", "cold feet",
                                  "ask her out", "ask him out", "ask them out", "ask out",
                                  "ask someone out", "asking her out", "asking him out",
                                  "good for you", "good for me", "good for us", "bad for you",
                                  "bad for me", "healthy", "unhealthy", "healthier",
                                  "fattening", "nutritious", "health benefits", "protein",
                                  "what can i cook", "what can i make", "what do i make",
                                  "dinner idea", "dinner ideas", "meal idea", "meal ideas",
                                  "recipes for",
                                  "from frozen", "straight from frozen", "still frozen",
                                  "cook frozen", "cooking frozen", "cook it frozen",
                                  "cook from frozen", "cooking from frozen",
                                  "cooked from frozen",
                                  "roast from frozen", "roast it from frozen",
                                  "fry from frozen", "fry frozen",
                                  "without defrosting", "without thawing",
                                  "no need to defrost", "no need to thaw",
                                  "defrost it first", "not defrosted",
                                  "whole frozen", "frozen whole", "frozen bird",
                                  "frozen chicken in the", "frozen chicken on the",
                                  "stock", "stocks", "broth", "carcass", "carcasses",
                                  "bone", "bones", "stockpot",
                                  "has it gone off", "has my chicken gone off",
                                  "has the chicken gone off", "has this gone off", "has it gone",
                                  "is it off", "is my chicken off", "is the chicken off",
                                  "is this off", "how do i know", "how can i tell",
                                  "how do you tell", "know if", "tell if", "still ok", "still good",
                                  "ok to eat", "okay to eat", "safe to eat", "still safe",
                                  "smell", "smells", "smelly", "slimy", "sour", "funny smell"),
          bias=1),
    entry("chicken-pink", (("chicken", "turkey", "duck", "goose"),
                            ("pink", "raw", "undercooked", "bloody", "middle", "in the middle",
                             "grey", "gray", "greyish", "grey inside", "gray inside")),
          "Pink chicken in the middle means it is undercooked, so don't eat it. That is a bad "
          "sign rather than a taste thing: put it back in the pan or oven until the juices run "
          "clear and the thickest part reaches 74C, and a little pink near the bone in a roast is "
          "still fine. A grey, translucent middle is the same thing said another way: it has not "
          "come up to temperature yet, so give it another few minutes rather than looking at the "
          "colour of the outside.",
          avoid=PET_LINE_WORDS + ("storage", "store", "stores", "storing", "stored", "fridge",
                                  "freezer", "freeze", "frozen", "how long", "use by",
                                  "left out", "leftover", "leftovers", "keep", "keeps", "kept"),
          bias=1),
    entry("pork-pink", (("pork", "pork chop", "pork chops", "pork loin", "pork belly",
                         "pork shoulder", "pork steak", "gammon", "beef", "steak", "steaks",
                         "lamb", "lamb chop", "lamb chops", "veal", "red meat",
                         "meat", "pink meat", "raw meat",
                         "burger", "burgers", "mince", "minced", "minced meat", "sausage",
                         "sausages", "meatball", "meatballs", "kofta", "kofte", "nugget",
                         "nuggets", "kebab", "kebabs", "patty", "patties"),
                        ("pink", "raw", "undercooked", "bloody", "safe", "safely", "ok to eat",
                         "grey inside", "gray inside", "grey in the middle",
                         "gray in the middle", "grey through", "gray through",
                         "grey all through",
                         "okay to eat", "fine to eat", "eat it", "still ok", "rare",
                         "middle", "in the middle")),
          "A whole cut of red meat - a chop, a loin, a shoulder or a steak, whether pork, lamb or "
          "beef - can be a little pink in the middle and still be safe if it reaches 63C and "
          "rests for a few minutes, but mince, sausages and burgers have to be grey all the way "
          "through to 71C. A mouthful of raw pork or lamb by accident is very unlikely to do you "
          "harm, but a serving of it is a bad idea: salmonella, E. coli and, rarely, roundworm. "
          "Cook it through, and see a doctor if you get cramps, fever or diarrhoea in the next "
          "few days.",
          avoid=PET_LINE_WORDS + (
                                  "how much", "how many", "a day", "a week", "diet", "cancer",
                                  "bowel", "cholesterol", "processed", "portion", "portions",
                                  "healthy", "good for you", "bad for you", "should i eat",
                                  "fish", "tuna", "salmon", "cod", "haddock", "prawns",
                                  "sashimi", "ceviche", "crackling", "roast", "how long", "oven",
                                  "temperature",
                                  "thermometer", "recipe", "marinade", "freeze", "frozen",
                                  "how do i", "cook", "cooking", "grill", "fry", "frying",
                                  "sear", "bake", "barbecue", "bbq", "sunday roast",
                                  "well done", "medium rare", "how to"),
          bias=1),
    entry("mince-pink", (("mince", "minced", "minced meat", "mincemeat", "burger", "burgers",
                          "sausage", "sausages", "sausagemeat", "meatball", "meatballs",
                          "kofta", "kofte", "kebab", "kebabs", "patty", "patties", "nugget",
                          "nuggets", "raw mince", "raw burger", "rare burger", "hamburger"),
                         ("pink", "raw", "undercooked", "bloody", "safe", "safely", "ok to eat",
                          "okay to eat", "fine to eat", "eat it", "still ok", "rare", "medium",
                          "medium rare", "well done", "in the middle", "middle", "should i eat")),
          "Mince, sausages and burgers have to be cooked grey all the way through to 71C, and a "
          "whole steak does not: mincing mixes the bacteria from the outside through the meat, so "
          "a rare burger is a real risk in a way a rare steak is not. Out, order it well done; at "
          "home, no pink in the middle and the juices run clear. A mouthful of raw mince is very "
          "unlikely to do any harm, but a serving of it is a bad idea - cook it through, and see a "
          "doctor if you get cramps, fever or diarrhoea in the next few days.",
          avoid=PET_LINE_WORDS + ("how do i cook", "how to cook", "how long", "recipe",
                                  "recipes", "how do i make", "sauce", "gravy", "bolognese",
                                  "lasagne", "lasagna", "chilli", "stew", "casserole", "pie",
                                  "oven", "grill", "barbecue", "bbq", "fry", "frying", "bake",
                                  "temperature", "thermometer", "meat free", "vegetarian",
                                  "vegan", "quorn", "soya", "plant based", "i made", "leftover",
                                  "leftovers", "fridge", "freezer", "freeze", "frozen", "keep",
                                  "keeps", "kept", "store", "stores", "storing", "stored",
                                  "storage", "use by", "how much", "a week", "a day",
                                  "diet", "processed", "cancer", "protein", "calories",
                                  "pregnant", "pregnancy", "expecting", "breastfeeding",
                                  "breast feeding", "conceive", "conceiving", "trimester"),
          bias=2),
    entry("fish-raw", (("fish", "salmon", "tuna", "cod", "haddock", "mackerel", "sea bass",
                        "trout", "sardines", "sashimi", "anchovies", "yellowtail", "halibut",
                        "raw fish", "raw salmon", "raw tuna"),
                       ("raw", "undercooked", "pink", "rare", "sashimi", "ceviche", "safe",
                        "safely", "ok to eat", "okay to eat", "fine to eat", "eat it",
                        "is it ok", "can i eat", "middle", "in the middle")),
          "Raw fish is safe to eat if it has been frozen first - 24 hours at -20C kills the "
          "parasites, and that is what sushi-grade fish has had - so a fresh fillet from a "
          "fishmonger eaten the day you buy it is fine for most people, and a supermarket fillet "
          "is not meant for it. Skip raw fish altogether if you are pregnant or your immune "
          "system is weak, and never eat freshwater fish raw.",
          avoid=PET_LINE_WORDS + ("tank", "fish tank", "aquarium", "goldfish", "pond", "ponds",
                                  "fish bowl", "pet fish", "kitten", "cat", "dog", "hamster",
                                  "fish for", "rod licence", "angling",
                                  "smoked", "cured", "kipper", "fish fingers", "fish and chips",
                                  "pregnant", "pregnancy", "omega", "portions", "how long",
                                  "oven", "grill", "fry", "frying", "bake", "baking", "recipe",
                                  "temperature", "thermometer", "how do i cook", "cook it",
                                  "cooking", "poach", "steam", "season", "buy", "price",
                                  "is it off", "gone off", "still ok", "smell", "fridge",
                                  "how often", "how many times", "every day", "everyday",
                                  "twice a week", "a week", "per week", "a day"),
          bias=1),
    entry("fix-falls-apart", (COMING_APART,
                              _FOOD + ("meatballs", "meatball", "kofta", "koftas", "tofu",
                                       "paneer", "halloumi", "tempeh", "rissoles", "fish pie",
                                       "fishcakes", "fishcake", "salmon", "cod", "haddock",
                                       "toad in the hole", "sausage meat", "potatoes", "mash",
                                       "dumplings", "falafel", "stew", "casserole")),
          _falls_apart, bias=1,
          avoid=PET_LINE_WORDS + ("tank", "fish tank", "aquarium", "goldfish", "pond", "ponds",
                                  "koi", "guppy", "guppies", "betta", "bowl", "pet fish",
                                  "filter", "whitespot", "white spots", "sick", "ill",
                                  "fish for", "rod licence", "angling",
                                  "smoked", "cured", "kipper", "fish fingers", "fish and chips",
                                  "raw", "sashimi", "pregnant", "pregnancy",
                                  "my plan", "my plans", "family", "relationship", "marriage",
                                  "friendship", "my car", "my van", "my bike", "sofa", "boots",
                                  "shoes", "wall", "walls", "shed", "fence", "roof", "teeth",
                                  "hair"),
          ),
    entry("roast-shopping",
          (("roast", "roast dinner", "sunday roast", "christmas dinner", "xmas dinner",
            "turkey dinner", "chicken dinner", "roast lamb", "roast beef", "roast pork",
            "roast chicken", "roast turkey", "nut roast", "turkey"),
           ("buy", "buying", "shop", "shopping", "shopping list", "pick up", "pick some up",
            "need to buy", "need to get", "to get in", "get in", "buy for", "shop for")),
          _roast_shopping, bias=1,
          avoid=("wine", "how long", "leftover", "left over", "freeze", "frozen", "fridge",
                 "tin", "tray", "pan", "dish", "sauce", "gravy granules", "vegan", "veggie",
                 "vegetarian", "no meat", MEATLESS_ROAST, "allergy", "allergic",
                 "minutes", "longer", "another", "resting", "rest", "done", "gas mark",
                 "temperature", "oven",
                 "days", "weeks", "when", "before", "early", "advance", "order",
                 "potato", "potatoes", "carrot", "carrots", "parsnip", "parsnips", "sprout",
                 "sprouts", "cabbage", "broccoli", "peas", "cauliflower", "swede", "turnip",
                 "stuffing", "sausagemeat", "pigs in blankets", "yorkshire", "batter",
                 "bread sauce", "cranberry", "pudding", "gravy", "horseradish", "mint sauce",
                 "apple sauce", "onion", "onions")),
    entry("steak", (("steak", "beef"), ("cook", "medium", "rare", "juicy", "pan", "how long",
                                        "minute")),
          "Get a heavy pan properly hot, pat the steak dry, salt it and sear it 2 to 3 minutes a "
          "side for medium rare, turning once. Rest it 5 minutes under foil before cutting, which "
          "matters as much as the cooking.",
          avoid=("freezer", "frozen", "freeze", "fridge", "keep", "keeps", "last", "stay", "thaw",
                 "defrost", "gammon", "gammon steak", "gammon steaks")),
    entry("roast-joint", (("roast joint", "joint of beef", "beef joint", "roast beef",
                           "joint of lamb", "leg of lamb", "roast lamb", "shoulder of lamb",
                           "joint of pork", "leg of pork", "roast pork", "pork joint"),
                          ("temperature", "how long", "time", "oven", "cook", "roast",
                           "hot", "fan", "minutes", "done",
                           "doing", "making")),
          _roast_joint,
          avoid=("slow", "slowly", "low and slow", "overnight", "pulled", "serve", "serving",
                 "serves", "side", "sides", "goes with", "what with", "accompany",
                 "curry", "curries",
                 "buffet", "buffets", "party",
                 "rest", "resting", "rested")),
    entry("rest-meat", (("rest", "resting", "rested"),
                        ("meat", "steak", "roast", "joint", "chicken", "turkey", "lamb", "beef",
                         "pork", "gammon", "brisket", "ribs", "rack", "shoulder", "bird",
                         "chops", "roasted", "carve", "carving")),
          _rest_the_meat,
          avoid=("shortcrust", "pastry", "bread", "dough", "rise", "rises", "rising",
                 "proving", "proof", "sourdough", "cake",
                 "gym", "sets", "set", "rep", "reps", "run", "running", "jog", "walk", "walking",
                 "exercise", "training", "workout", "muscle", "muscles", "injury", "sore",
                 "sleep", "bed", "nap", "tired", "ill", "sick", "cold", "flu", "days", "week"),
          bias=1),
    entry("mince-grainy", (_MINCE_GRAIN_DISH, _MINCE_GRAIN_WORD),
          _mince_grainy,
          avoid=("chocolate", "fudge", "toffee", "caramel", "icing", "custard", "cake", "sugar",
                 "freeze", "freezer", "fridge", "leftover", "leftovers", "reheat")),
    entry("mince", (("mince", "minced beef", "ground beef"),
                     ("brown", "cook", "bolognese", "sauce", "grey", "tough", "rubbery", "dry")),
          _mince),
    entry("sausages", (("sausages", "sausage", "chipolata", "chipolatas", "bangers"),
                       ("cook", "oven", "pan", "juicy", "how long", "grill", "fry", "frying")),
          "Roast sausages at 200C (180C fan) for 25 to 30 minutes, turning once, or fry them on a "
          "medium heat for about 15. Pricking them lets the juice out, so don't."),
    entry("bacon", ("bacon", ("crispy", "cook", "oven", "how long")),
          "Lay bacon rashers on a rack over a tray and bake at 200C (180C fan) for 15 to 18 "
          "minutes: crisp, flat and no splashing. In a pan, start it in a cold pan on a medium heat "
          "so it renders before it burns."),
    entry("salmon", ("salmon", ("cook", "oven", "bake", "time", "how long")),
          "Bake salmon fillets at 200C (180C fan) for 12 to 15 minutes, until the flesh just "
          "flakes. In a hot pan, 4 minutes skin side down and 1 minute the other way is enough; "
          "salmon dries out fast when it's overcooked.",

          avoid=("last", "lasts", "keep", "keeps", "keeping", "store", "stored", "shelf life",
                 "fridge", "freezer", "gone off", "out of date", "tomorrow", "next day",
                 "poach", "poached", "poaching", "poached salmon", "steam", "steamed")),
    entry("mushroom-wash",
          (("mushroom", "mushrooms", "button mushrooms", "chestnut mushrooms", "portobello",
            "field mushrooms", "shiitake"),
           ("wash", "washing", "washed", "rinse", "rinsing", "clean", "cleaning", "clean them",
            "dirt", "grit", "peel", "peeled", "before cooking", "before you cook")),
          lambda memory, understood: _mushroom_wash(understood),
          avoid=("freeze", "freezing", "frozen", "keep", "keeping", "store", "storing",
                 "fridge", "last", "lasts", "slimy", "gone off", "raw", "pick", "picked",
                 "forage", "dried", "dry", "soup", "sauce", "risotto", "stuffed", "grow",
                 "growing", "garden", "poisonous"),
          ask=("wash", "washing", "washed", "rinse", "rinsing", "clean", "cleaning", "dirt",
               "grit", "peel", "peeled", "before cooking"),
          bias=3),
    entry("salmon-poach",
          (("salmon", "fish", "haddock", "cod", "trout"),
           ("poach", "poached", "poaching", "poached salmon", "poach in milk", "water bath")),
          lambda memory, understood: _poach_fish(understood),
          avoid=("bake", "baked", "baking", "roast", "roasted", "fry", "fried", "grill",
                 "grilled", "smoked", "raw", "sushi", "freeze", "frozen", "thaw", "keep",
                 "fridge", "salad", "sandwich", "teriyaki")),

    entry("dip-fault",
          (("houmous", "hummus", "humous", "tzatziki", "raita", "aioli", "mayonnaise", "mayo",
            "guacamole", "salsa", "baba ganoush", "tapenade", "dip", "dips", "garlic sauce",
            "yogurt dip", "yoghurt dip"),
           ("too thick", "too thin", "watery", "runny", "too dry", "split", "curdled",
            "gone brown", "went brown", "turned brown", "lumpy", "seized", "ruined",
            "went wrong", "fix")),
          lambda memory, understood: _dip_fault(understood),
          avoid=("simmer", "reheat", "chicken", "bolognese", "curry", "stew", "soup"),
          bias=1),
    entry("prawns-doneness", (("prawn", "prawns", "king prawns", "king prawn", "shrimp",
                               "shrimps", "tiger prawns", "prawn cocktail", "langoustine",
                               "langoustines"),
                              ("raw", "uncooked", "cooked", "ready", "already cooked",
                               "from frozen", "frozen", "cold", "safe", "safely", "ok to eat",
                               "okay to eat", "fine to eat", "eat it", "eat them", "thawed",
                               "defrosted", "need to cook", "have to cook", "should i cook",
                               "do i need to cook", "pink", "grey", "grey inside", "sushi",
                               "pregnancy", "pregnant", "eat cold", "eat them cold",
                               "without cooking", "no cooking", "without defrosting")),
          "Check the pack first, because most prawns are sold already cooked: those only need "
          "thawing, and a cooked prawn is safe to eat cold once it has defrosted overnight in the "
          "fridge. Raw prawns are grey rather than pink, and those have to be cooked all the way "
          "through until they curl, turn pink and are opaque in the middle - 2 to 3 minutes in a "
          "hot pan or 1 to 2 minutes in boiling water, and you can put them in frozen with a "
          "minute or two extra. Thawed prawns keep a day, do not go back in the freezer, and in "
          "pregnancy eat only the thoroughly cooked ones. Bin any that smell of ammonia or feel "
          "slimy.",
          avoid=("how long do prawns take", "how long to cook prawns", "how long does it take",
                 "how long do i cook", "how long should i cook", "how long do you cook",
                 "how long do king", "how long in the", "how many minutes",
                 "how do i defrost", "how to defrost", "recipe", "recipes",
                 "how do i cook", "how to cook", "best way", "method", "curry",
                 "stir fry", "stir-fry", "linguine", "pasta", "risotto", "paella", "noodle",
                 "noodles", "reheat", "keep", "keeps", "leftover", "leftovers", "freeze",
                 "refreeze", "sauce", "garlic", "butter", "tempura", "batter", "barbecue",
                 "bbq", "air fryer", "oven", "grill", "price", "buy", "sustainable", "farm",
                 "prawn cracker", "prawn crackers", "prawn toast",
                 "when pregnant", "while pregnant", "if pregnant", "in pregnancy",
                 "during pregnancy", "weeks pregnant", "im pregnant", "i'm pregnant",
                 "pregnant and", "pregnancy and") + PET_LINE_WORDS,
          bias=6),
    entry("fish-defrost", (("fish", "salmon", "cod", "prawns"), ("defrost", "frozen", "thaw")),
          "Defrost fish in the fridge overnight, still wrapped, on a plate. If you're short of "
          "time, seal it in a bag and sit it in cold water for an hour, changing the water; never "
          "defrost it on the worktop. A prawn is quicker, and needs no night in the fridge: cold "
          "water for 10 to 15 minutes, or straight into a curry or stir-fry from frozen with two or "
          "three minutes extra."),

    entry("meat-defrost", (("turkey", "mince", "sausages", "sausage", "beef", "pork", "lamb",
                            "chops", "steak", "gammon", "bacon", "joint", "liver", "kidneys",
                            "meat", "red meat",
                            "from frozen", "cook it frozen", "cooked from frozen",
                            "without defrosting", "without thawing", "no need to defrost",
                            "have to defrost", "need to defrost"),
                           ("defrost", "defrosting", "defrosted", "thaw", "thawing", "thawed",
                            "frozen")),
          _meat_defrost, bias=2,
          ask=("defrost", "defrosting", "defrosted", "thaw", "thawing", "thawed", "frozen"),
          avoid=("freezer", "freeze", "refreeze", "re-freeze", "keep in the fridge",
                 "leftover", "leftovers", "reheat", "use by", "gone off", "off smell",
                 "chicken", "prawn", "prawns", "fish", "salmon", "cod",
                 "pizza", "chips", "chip", "fries", "wedges", "waffles", "nuggets",
                 "fish fingers", "peas", "sweetcorn", "veg", "vegetables", "broccoli",
                 "spinach", "berries", "fruit", "pastry", "rice", "bread", "pie",
                 "potato", "potatoes", "dumplings", "samosa", "spring rolls", "yorkshire",
                 "cake", "pancake", "pancakes", "croissant", "dough")),
    entry("roast-potatoes", (("potato", "potatoes"),
                             ("roast", "crispy", "crisp", "crunchy", "crunchiest", "soggy",
                              "oven", "fluffy", "burn", "burnt", "burning", "black",
                              "blackened", "caught", "too hot", "stuck", "edges")),
          _roast_potatoes,
          ask=("roast", "roasts", "roasting", "roasted", "roastie", "roasties", "oven",
               "in the tin", "in the tray"),
          bias=3, guard=_not_the_joint_timing,
          avoid=("sweet", "sweet potato", "sweet potatoes", "yam", "yams",
                 "air fryer", "air fryers", "airfryer", "air-fryer", "air fried", "airfry",
                 "jacket", "jacket potato", "jacket potatoes", "baked potato", "baked potatoes",
                 "baking potato", "potato skin", "potato skins", "skin on",
                 "keep", "keeps", "keeping", "last", "lasts", "stale", "freeze", "fridge",
                 "freezer", "reheat", "leftover", "leftovers",
                 "fattening", "fatten", "calories", "calorie", "how many calories", "healthy",
                 "healthier", "unhealthy", "bad for you", "good for you", "slimming", "diet",
                 "weight loss", "waistline", "carbs", "keto", "nutrition", "nutritious",
                 "goes with", "go with", "went with", "serve with", "served with",
                 "to serve with", "accompaniment", "accompaniments", "side with",
                 "sides to go with")),
    entry("mash", (("mash", "mashed potato", "mashed potatoes"), ("lumpy", "smooth", "fluffy",
                                                                 "cream", "creamy", "make",
                                                                 "how do i mash", "how do you mash",
                                                                 "how to mash", "mash the potatoes",
                                                                 "mashing them with",
                                                                 "best", "butter", "milk",
                                                                 "how long", "boil", "boiling",
                                                                 "minutes", "time")),
          "Boil them in salted water: 15 to 20 minutes for chunks and 20 to 25 for whole medium "
          "potatoes, until a knife slides in with no resistance. Floury potatoes mash best, so "
          "steam them dry for a minute, then mash with warm milk and butter and stop as soon as "
          "it's smooth: over-beating turns it gluey.",
          avoid=_MASH_NOT_THIS),
    entry("mash-dairy-free", (("mash", "mashed potato", "mashed potatoes"),
                              ("without butter", "no butter", "butter free", "without milk",
                               "no milk", "milk free", "dairy free", "dairy-free", "no dairy",
                               "without dairy", "instead of butter", "instead of milk", "vegan",
                               "olive oil", "plant based", "plant-based")),
          "Mash it with the water it cooked in and a fat that is not butter: two or three spoons "
          "of the cooking water and two tablespoons of olive oil, or the same of a dairy-free "
          "spread, plus a splash of warm oat or soy milk if you want it looser. Work it with a "
          "fork or a whisk for a minute rather than a masher - starch and liquid are what make it "
          "smooth - and taste for salt, because without butter it wants a little more. A spoon of "
          "mustard, horseradish or a soft garlic clove cooked with the potatoes puts back some of "
          "the flavour the butter was giving."),
    entry("mash-for-baby", (("mash", "mashed potato", "mashed potatoes", "potato", "potatoes"),
                            ("baby", "babies", "for my baby", "for a baby", "weaning", "weaned",
                             "toddler", "6 months", "six months", "9 months", "first foods")),
          "Cook the potato on its own in unsalted water and mash it with a little of that water, "
          "some of their usual milk or a knob of unsalted butter, and no salt at all: babies under "
          "one should have none, and their kidneys cannot deal with it. Keep it smooth and a "
          "little looser than yours while they are learning to swallow, and add nothing else "
          "until you know they have had it before. Your health visitor is the one to ask about "
          "amounts and what to add next, because it depends on the baby's age."),
    entry("onion-cry", ("onion", ("cry", "crying", "tears", "eyes")),
          "Cutting an onion breaks its cells and releases a gas that irritates your eyes, so they "
          "make tears to wash it away. A sharp knife and a chilled onion release less of it, and "
          "the root end holds most of it, so cut that last.",
          bias=3,
          avoid=("dog", "dogs", "puppy", "puppies", "cat", "cats", "kitten", "kittens", "pet",
                 "pets", "ate", "eaten", "eat", "eats", "eating", "poison", "poisoned",
                 "poisonous", "toxic")),
    entry("leaf-can-i-eat-it",
          (("limp", "wilted", "floppy", "soggy", "slimy", "gone over", "gone brown", "brown edges"),
           ("safe", "safely", "eat", "eating", "edible", "still ok", "still good", "ok to eat",
            "still fine", "throw away", "bin it", "use it")),
          "Limp leaves are fine to eat: wilting is only water loss, so they are safe once they have "
          "had 10 minutes in iced water. Slimy, sour-smelling or brown-and-soft leaves are not "
          "safe, and no rinse fixes them, so bin those.",
          avoid=LEAFY_AVOID + ("dog", "cat", "puppy", "kitten", "pet", "baby", "toddler", "child",
                               "hair", "feel", "tired", "plant", "garden", "ground",
                               "keep", "keeps", "keeping", "stop", "stops", "crisp", "crisper",
                               "fresh", "fresher", "last", "longer", "revive", "reviving")),
    entry("dry-herbs", (("dry", "drying", "dehydrate", "dehydrating", "hang",
                         "hanging", "preserve", "preserving"),
                        ("herb", "herbs", "lavender", "rosemary", "thyme", "sage", "oregano",
                         "mint", "bay leaves", "bay leaf", "laurel", "parsley", "dill", "tarragon",
                         "chives", "marjoram", "lemon balm", "chamomile", "camomile", "basil")),
          ("Hang it in small bunches, upside down and spread out, somewhere warm, dark and dry "
           "with a bit of air moving - a shed, an airing cupboard or a room with the window open "
           "- and it is dry in one to two weeks. A low oven at 50C with the door ajar does the "
           "same in an hour or two. Strip the leaves or buds off the stems once they crumble, keep "
           "them in a sealed jar out of the light, and they hold their flavour for about a year. "
           "Lavender keeps its scent better in a paper bag than in a jar, and the buds go into a "
           "small cloth bag for a drawer or under a pillow."),
          avoid=("yellow", "yellowing", "wilt", "wilted", "wilting", "limp", "soggy", "dying",
                 "dry leaves", "dried leaves", "has dry", "have dry", "leaves are", "leaves look",
                 "leaves going", "leaves turning", "going crispy", "crispy",
                 "drooping", "droopy", "curling", "brown", "spots", "mouldy", "moldy", "mould",
                 "instead of", "substitute", "in place of", "fresh or dried", "dried or fresh",
                 "recipe", "cook with", "cooking with", "how much",
                 "store", "storing", "storage", "keep", "keeps", "keeping", "how long", "last",
                 "lasts", "shelf life")),
    entry("dried-herbs", (("rosemary", "thyme", "oregano", "herbs"), ("dried", "fresh",
                                                                    "instead", "substitute")),
          "Dried herbs are fine in anything cooked: use about half the amount of fresh and add them "
          "earlier so they soften. Keep fresh for the end, and for salads and dressings where "
          "their green taste is the point.",
          avoid=("limp", "soggy", "wilt", "wilted", "stay fresh", "keep fresh", "rubbery")),
    entry("garlic-hands", ("garlic", ("smell", "hands", "stink", "smelly")),
          "Rub your hands on something stainless steel under cold running water, like the tap or a "
          "spoon, and the smell goes; salt, lemon juice or coffee grounds work too. The sulphur "
          "compounds bind to the metal instead of your skin.",
          avoid=("breath", "bad breath", "garlic breath", "mouth", "breathe", "breathing")),
    entry("garlic-burn", (("garlic", "garlic clove", "garlic cloves"),
                          ("burn", "burns", "burnt", "burned", "burning", "bitter", "black",
                           "black bits", "went black", "gone black", "scorch", "scorched",
                           "too hot", "high heat", "caught")),
          "Garlic burns in seconds because it's full of sugar: crush or slice it and add it later "
          "than the onion, on a lower heat. If it's already bitter, start again; burnt garlic "
          "taints the whole dish.",
          avoid=("breath", "bad breath", "garlic breath", "mouth", "breathe", "breathing",
                 "still smell", "smells of")),
    entry("garlic-green", (("garlic", "garlic clove", "garlic cloves", "pickle", "pickles",
                            "pickled", "chutney", "kimchi", "sauerkraut"),
                           ("green", "blue", "teal", "turquoise", "colour", "colours", "coloured",
                            "safe", "harmless", "gone off", "off")),
          ("That green or blue is harmless: the sulphur compounds in garlic and onions turn "
           "colour with acid, and with copper or unlined iron, and nothing else about the food "
           "changes, so eat it. It shows up in garlic dressed with lemon or vinegar, in pickle "
           "brines and in pickled onions. Blanching the cloves for 30 seconds before pickling, "
           "adding the acid at the end and using a stainless pan all stop it happening."),
          avoid=("store", "storing", "storage", "keep", "keeping", "plant", "planting", "grow",
                 "growing", "how long", "sprout", "sprouting", "sprouted", "skin", "peel",
                 "smell", "burn", "burnt"),
          bias=3),
    entry("roast-vegetables", (("vegetables", "veg"), ("roast", "oven", "time", "how long")),
          "Cut vegetables into similar-sized pieces, toss them with oil and salt and roast at 200C "
          "(180C fan) for 30 to 40 minutes, turning once. Give them space on the tray; a crowded "
          "tray steams instead of roasting.",
          avoid=("take to grow", "to grow", "grow", "growing", "grows", "sow", "sowing",
                 "seed", "seeds", "harvest", "crop", "crops", "allotment", "raised bed",
                 "veg patch", "vegetable patch")),
    entry("broccoli", ("broccoli", ("cook", "boil", "steam", "steaming", "steamed", "how long",
                                    "time", "done", "tender", "know when", "soggy", "mushy",
                                    "green", "yellow", "yellowing", "gone yellow")),
          "Boil or steam broccoli for 4 to 5 minutes, until a knife goes in with a little bite "
          "left. Drain it and run it under cold water if you're not serving it straight away: that "
          "keeps it green instead of army-issue grey. Broccoli that has already gone yellow is "
          "either overdone or a few days old - it is still fine to eat, so give it 3 minutes next "
          "time and use this lot in a soup or a stir-fry rather than on the plate."),
    entry("kale", ("kale", ("cook", "boil", "steam", "steaming", "how long", "time", "done",
                            "tender", "prepare", "strip", "stalks", "bitter")),
          "Strip the leaves off the stalks - the stalks are the woody, bitter part - then boil or "
          "steam the leaves for 3 to 5 minutes, until they are soft but still bright. Curly kale "
          "takes the 5 and cavolo nero nearer 3. Massage it with oil and salt if it is going in a "
          "salad raw, which softens it in a couple of minutes without cooking it. A splash of "
          "lemon or vinegar at the end keeps the colour.",
          avoid=("keep", "keeping", "store", "last", "freeze", "grow", "growing", "plant", "slug",
                 "slugs", "crisps", "crisps", "chip", "chips", "crispy")),
    entry("cauliflower-boil", ("cauliflower",
                               ("boil", "boiled", "steam", "how long", "time", "tender", "white",
                                "grey", "soggy", "cook")),
          "Florets take 5 to 7 minutes in boiling salted water and a whole head 10 to 15, until a "
          "knife slides into the stalk with no crunch left. A tablespoon of milk or lemon in the "
          "water keeps it white rather than grey, and salt it properly or it tastes of nothing. "
          "Drain it well, because a cauliflower left sitting in its water goes soft and sulky.",
          avoid=("roast", "roasting", "roasted", "oven", "cheese", "bake", "baked", "rice",
                 "freeze", "keeping", "keep", "curry", "soup", "grow", "growing")),
    entry("cabbage-boil",
          (("cabbage", "white cabbage", "green cabbage", "savoy", "savoy cabbage", "hispi",
            "pointed cabbage", "spring greens", "greens"),
           ("boil", "boiled", "cook", "cooking", "steam", "steaming", "how long", "time", "done",
            "tender", "soft", "soggy", "prepare", "wedges", "shred")),
          "Cut it into wedges so the stalk cooks with the leaf, drop it into plenty of boiling "
          "salted water and leave the lid off: 5 to 8 minutes for a firm white or green cabbage, "
          "3 to 4 for savoy and spring greens, until a knife goes into the stalk with a little "
          "resistance left. Drain it at once and toss it with a knob of butter or a little oil - "
          "cabbage left standing in the pan carries on cooking and turns to water.",
          avoid=("red cabbage", "red cabbages", "bitter", "bitterness", "smell", "smelly",
                 "stink", "keep", "keeping", "store", "shop", "buy", "grow", "growing", "plant",
                 "slug", "slugs", "recipe", "leftover", "freeze", "pickle", "sauerkraut",
                 "coleslaw", "kimchi", "soup", "stuffed", "roll", "rolls", "meat")),
    entry("red-cabbage", (("red cabbage", "red cabbages"),
                          ("cook", "cooking", "braise", "braised", "how long", "time", "boil",
                           "vinegar", "apple", "sweet", "christmas", "prepare")),
          "Braise it rather than boil it: shred it, soften sliced onion in butter, add the cabbage "
          "with a chopped apple, two tablespoons of vinegar and a spoon of sugar, a splash of "
          "water, then put the lid on for 45 to 60 minutes on a low heat, stirring now and then. "
          "The vinegar is not for flavour alone - it is what keeps the colour a deep red instead "
          "of a grey-blue, so taste and add more at the end.",
          avoid=("bitter", "keep", "keeping", "store", "buy", "grow", "growing", "plant", "slug",
                 "slugs", "freeze", "pickle", "raw", "salad", "slaw", "coleslaw", "sauerkraut")),
    entry("cabbage-bitter",
          (("cabbage", "red cabbage", "sprouts", "sprout", "spring greens", "kale", "cauliflower",
            "broccoli", "brassica", "brassicas"),
           ("bitter", "bitterness", "sulphur", "sulfurous", "why", "tastes", "taste", "smells",
            "smelly")),
          "The bitterness is the sulphur compounds in the leaves, and cooking makes it worse the "
          "longer it goes on: past about 8 minutes a brassica turns sweet-smelling and bitter at "
          "the same time. So cook it briefly in plenty of fast-boiling water, leave the lid off, "
          "and cut it into even pieces so the stalk is not still raw when the leaf is done. If it "
          "has already gone bitter, fat and acid rescue it: butter or olive oil, a squeeze of "
          "lemon, a pinch of sugar, or bacon and onion fried first and the cabbage tossed through.",
          avoid=("smell", "smelly", "stink", "house", "room", "kitchen", "keep", "keeping",
                 "store", "buy", "grow", "growing", "plant", "slug", "slugs", "freeze", "recipe",
                 "soup", "raw", "salad",
                 "potato", "potatoes", "solanine", "green potato", "green potatoes")),
    entry("cabbage-better",
          (("cabbage", "spring greens", "sprouts", "sprout", "kale"),
           ("taste better", "tastier", "nicer", "more interesting", "liven", "boring", "bland",
            "enjoy", "like it", "make it", "how do i make")),
          "Three things, in this order: cooking it less, fat and salt. Boil or shred-and-fry it for "
          "4 to 6 minutes only, then toss it with butter or a little oil, salt, and something "
          "sharp - lemon, vinegar, or a spoon of mustard. Fried bacon or chorizo, onion softened "
          "first, a pinch of chilli or caraway, or a dusting of nutmeg all give it a reason to be "
          "on the plate. A splash of cream or a spoon of yoghurt turns it into something people go "
          "back for.",
          avoid=("bitter", "bitterness", "smell", "smelly", "stink", "keep", "keeping", "store",
                 "buy", "grow", "growing", "plant", "slug", "slugs", "freeze", "recipe", "soup",
                 "leftover")),
    entry("salad-wilt", (LEAFY, ("fresh", "keep", "keeping", "store", "storing", "crisp",
                                 "crisper", "crispy", "soggy", "slimy", "rubbery", "gone over",
                                 "last", "longer", "how long", "a week", "days")),
          "About 5 days in the salad drawer; a whole unopened bag keeps a week longer. Wash and dry "
          "the leaves properly, keep them in a bag with a piece of kitchen paper and dress them "
          "only at the table, because wet leaves and early dressing are what make salad limp. "
          "Brown-edged or slimy leaves are past it, so pick those out before they spread.",
          avoid=LEAFY_AVOID + ("instead", "instead of", "in place of", "substitute", "swap",
                               "swapped", "frozen", "freezer", "tinned", "canned", "jarred",
                               "dried", "soggy", "went soggy", "gone soggy", "going soggy",
                               "wet", "dressing", "dressed", "sauce")),
    entry("salad-revive", (LEAFY, ("limp", "wilt", "wilted", "wilty", "revive", "reviving",
                                   "floppy", "perk", "crisp up")),
          "Plunge it in iced water for 10 to 15 minutes: cut an inch off the stems first if it is "
          "a whole lettuce or a bunch, and most of the crispness comes back. Dry it in a tea "
          "towel afterwards and keep it in a bag with a piece of kitchen paper, because wet "
          "leaves are what made it limp in the first place.",
          avoid=LEAFY_AVOID),
    entry("sandwich-fillings",
          (("sandwich", "sandwiches", "sarnie", "sarnies", "butty", "butties", "toastie",
            "toasties", "toasted sandwich", "lunchbox sandwich", "packed lunch sandwich",
            "sandwich filling", "sandwich fillings", "wrap", "wraps", "flatbread"),
           ("put in", "put inside", "goes in", "go in", "fill", "filling", "fillings",
            "ideas", "idea", "different", "instead of", "bored of", "boring", "sick of",
            "always have", "something")),
          "One moist thing and one with a bit of crunch or sharpness, and it stops being a sad "
          "sandwich: cheddar with apple and pickle, tuna with celery and a little mayo (drained, "
          "or the bread goes), hummus with grated carrot and cucumber, or leftover roast chicken "
          "with lettuce and mustard. Butter both slices to the edges first so the bread does not "
          "go soggy, and keep tomato or cucumber in the middle. Egg with cress, brie with grape, "
          "or corned beef with a lot of mustard are the other three worth having in your pocket.",
          avoid=("recipe", "how do i make", "make a sandwich", "soggy", "wet bread", "how long",
                 "last", "lasts", "keep", "keeps", "keeping", "store", "stored", "freeze",
                 "frozen", "calories", "how many", "healthy", "kids", "children", "party",
                 "buffet", "platter", "shop", "buy", "cost",
                 "isnt", "is not", "not a sandwich", "not sandwiches", "no sandwich",
                 "no sandwiches", "without a sandwich", "without sandwiches",
                 "instead of a sandwich", "instead of sandwiches", "other than a sandwich",
                 "apart from sandwiches", "besides sandwiches",
                 "how filling", "fill me up", "keeps me full", "how much food"),
          bias=2),
    entry("soggy-lunch", (("salad", "salads", "lettuce", "leaves", "sandwich", "sandwiches",
                           "wrap", "wraps", "roll", "rolls", "baguette", "sub", "subs",
                           "coleslaw", "pasta salad", "lunch", "lunchbox", "packed lunch"),
                          ("soggy", "went soggy", "gone soggy", "going soggy", "goes soggy",
                           "wet", "leaky", "dressing", "dressed", "sauce")),
          _soggy_lunch,
          avoid=("limp", "wilt", "wilted", "revive", "crisp up", "how long", "last", "lasts",
                 "keep fresh", "stay fresh", "stays fresh", "freeze", "frozen", "buy", "grow")),
    entry("herbs-keep", (("herbs", "basil", "parsley", "coriander", "cilantro", "mint", "dill",
                          "chives"),
                         ("keep", "keeping", "store", "storing", "fresh", "last", "longer",
                          "how long", "a week", "days", "wilt", "wilted", "limp",
                          "soggy", "droop", "droopy", "rubbery", "slimy", "gone over")),
          _herbs_keep,
          avoid=("plant", "growing", "grow", "soil", "pot", "leaves", "dried", "dry", "drying",
                 "alive", "keep alive", "keeping alive", "from dying", "stop dying",
                 "keep dying", "keeps dying",
                 "yellow", "yellowing", "yellowed", "gone yellow", "going yellow",
                 "going over", "going to seed", "keep going", "come back", "comes back",
                 "coming back",
                 "over winter", "over the winter", "overwinter", "overwintering",
                 "through the winter", "survive", "survives", "perennial", "dies back",
                 "garden", "outside", "border"),
          bias=1),
    entry("avocado-ripen", ("avocado", ("ripe", "ripen", "hard", "quick", "soft",
                                        "how do i pick", "how do i choose", "pick a good",
                                        "choose a good", "pick the best", "good one")),
          "Put a hard avocado in a paper bag with a banana and leave it on the counter for a day or "
          "two; the banana's gas speeds it up. Once it gives slightly at the stem end it's ready, "
          "and lemon juice stops a cut one going brown."),
    entry("banana-ripe", (("banana", "bananas"),
                          ("ripe", "ripen", "ripening", "brown", "black", "quick",
                           "green", "still green", "too green", "very green", "so green",
                           "hard", "still hard", "too hard", "soften", "softer", "not ripe",
                           "unripe", "not ripening", "wont ripen", "wont go yellow")),
          "Bananas ripen fastest in a paper bag on the counter, especially with an apple; the "
          "fridge slows them right down but turns the skin black. Black-spotted skin is a sweet "
          "banana, and overripe ones are perfect for banana bread."),
    entry("banana-keep", (("banana", "bananas"), ("store", "storing", "keep", "keeping", "last",
                                                  "longer", "fresh", "fridge", "how long",
                                                  "a week",
                                                  "going black", "go black", "goes black",
                                                  "from going", "stop them going", "stop it going",
                                                  "stay fresh", "last longer")),
          "They ripen because of the ethylene gas they give off themselves, so a bunch goes "
          "together and the top of the bunch goes first. Keep them on the counter, loose rather "
          "than in a bag or the fruit bowl with other fruit - an apple or a tomato speeds them up "
          "- and pull one off the bunch as you use them. Once they are as ripe as you like them, "
          "the fridge slows them right down: the skin goes black, the fruit inside stays good for "
          "days.",
          avoid=("ripen", "riper", "overripe", "mushy", "bread", "cake",
                 "plant", "tree", "growing", "grow", "allergy", "allergic", "skin",
                 "eat", "eating", "ate", "daily", "calorie", "calories", "fattening",
                 "healthy", "carbs", "sugar", "potassium", "diet")),
    entry("season-wok", (("wok", "woks", "carbon steel wok", "carbon steel pan"),
                         ("season", "seasoning", "seasons", "reseason", "re-season", "new",
                          "first", "stick", "sticking", "strips", "stripped", "smoke", "smoky",
                          "oily", "black", "look after", "care", "factory")),
          ("A new carbon steel wok comes with a factory oil on it: scrub that off with hot water "
           "and a drop of washing-up liquid, dry it on the hob, then heat it until it just begins "
           "to smoke and wipe a teaspoon of groundnut or rapeseed oil round the inside with kitchen "
           "paper - three or four times and it goes dark and glossy. After that wash it with hot "
           "water and a soft brush, no soap and never a soak, and dry it on the heat. A wok is not "
           "non-stick; it gets closer every time you cook in it."),
          avoid=("plant", "recipe", "sauce", "which wok", "buy", "best wok", "cast iron",
                 "cast-iron", "skillet", "burnt", "burned", "bicarbonate", "clean", "cleaning",
                 "wash", "washing", "scrub", "rust", "rusty", "sticky"),
          bias=3),
    entry("wok-everyday-cleaning",
          (("wok", "woks"),
           ("clean", "cleaning", "cleaned", "wash", "washing", "washed", "scrub", "scrubbing",
            "after every use", "after use", "dry", "drying", "rust", "rusty", "sticky")),
          ("Hot water and a soft brush while it is still warm, no washing-up liquid and never a "
           "soak, then dry it on the hob over a low heat and wipe a smear of oil round the inside "
           "with kitchen paper. That thin film is the whole of the care. If a patch of rust "
           "appears, scour just that spot, dry it, and season it again on the heat - a wok is not "
           "non-stick, it gets closer every time you cook in it."),
          avoid=("season", "seasoning", "new", "first", "plant", "recipe", "sauce", "buy",
                 "best wok", "cast iron", "cast-iron", "skillet", "burnt", "burned",
                 "bicarbonate", "dishwasher", "what is a wok", "whats a wok"),
          bias=4),
    entry("peel-tomatoes",
          (("peel", "peeling", "peeled", "skin", "skins", "skinned", "de-skin", "deseed",
            "skin tomatoes", "skin a tomato", "way to skin", "skinning tomatoes",
            "skinned tomatoes", "take the skins off"),
           ("tomato", "tomatoes", "plum tomatoes", "cherry tomatoes", "tomato skin",
            "tomato skins", "them", "these", "those")),
          ("Nick a small cross in the base of each one, drop them into boiling water for 20 to 30 "
           "seconds, then straight into cold water: the skin curls back at the cross and slips off "
           "with your fingers. For a sauce you can skip peeling and just grate the tomato "
           "cut-side down on a box grater - the skin stays in your hand."),
          avoid=("seed", "seeds", "deseed only", "potato", "potatoes", "apple", "apples",
                 "mango", "orange", "oranges", "banana", "ginger", "garlic", "onion", "onions",
                 "carrot", "carrots", "butternut", "squash", "egg", "eggs", "prawn", "prawns",
                 "almond", "almonds", "peach", "peaches", "avocado",
                 "splitting", "split", "cracked", "cracks", "burst", "bursting", "rot",
                 "rotting", "blossom end", "vine", "greenhouse", "crop")),
    entry("tomato-store", ("tomatoes", ("fridge", "store", "keep", "taste", "flavour")),
          "Keep tomatoes on the counter, not in the fridge: cold kills their flavour and turns the "
          "texture mealy. Only put them in the fridge once they're fully ripe and you need to keep "
          "them a few more days.",
          avoid=("tin", "tins", "tinned", "can", "cans", "canned", "opened", "open", "jar",
                 "passata", "puree", "paste")),

    entry("bicarbonate-is-baking-soda",
          (("baking soda", "bicarbonate of soda", "bicarb", "bicarbonate"),
           ("same as bicarbonate", "same as baking soda", "same as bicarb",
            "the same as bicarbonate", "the same as baking soda", "the same thing", "the same",
            "one and the same", "identical", "or bicarbonate of soda", "or baking soda",
            "or bicarbonate", "or bicarb", "bicarbonate and baking soda",
            "baking soda and bicarbonate", "bicarbonate and soda", "is bicarb baking soda",
            "is baking soda bicarb")),
          "Yes - baking soda and bicarbonate of soda are the same thing under two names: the "
          "American name and the British one. Baking powder is the different one, because it has "
          "an acid and a starch mixed in with the bicarbonate, so it fizzes on its own and the "
          "soda needs an acid such as buttermilk, yoghurt or lemon to do anything.",
          avoid=("powder", "self raising", "self-raising", "how much", "in date", "out of date",
                 "tastes", "taste", "soapy", "cleaning", "clean", "drain", "soda bread",
                 "laundry", "washing", "drink", "drinking", "fizzy", "club soda", "soda water"),
          bias=6),
    entry("baking-soda-vs-powder", (("baking soda", "bicarbonate of soda", "bicarb", "soda",
                                     "baking powder"),
                                    ("difference", "substitute", "instead", "vs", "v", "versus",
                                     "or", "which one", "which",
                                     "or baking powder", "or soda", "or bicarb",
                                     "difference between", "which one do i need")),
          "They are not the same: baking soda is pure bicarbonate and needs an acid (buttermilk, "
          "yoghurt, lemon, treacle) to make things rise, while baking powder already has the acid "
          "in it. One way is easy and the other is not: in place of a teaspoon of soda use about "
          "three teaspoons of baking powder, and put the acid the recipe counted on in some other "
          "way or the tang is lost; in place of a teaspoon of baking powder use a quarter teaspoon "
          "of bicarbonate with a teaspoon of lemon juice or vinegar, and only in something that "
          "has the acid to meet.",
          avoid=("how much", "in date", "out of date", "old", "stale", "leftover", "flat",
                 "self raising", "self-raising", "plain flour", "cleaning", "clean", "caustic",
                 "soda bread", "drain", "laundry", "washing", "tastes", "taste", "soapy",
                 "instead", "instead of", "in place of", "substitute", "replacement",
                 "drink", "drinking", "drink it", "thirsty", "fizzy", "cola", "coke", "pop",
                 "club soda", "soda water", "tonic", "sparkling", "lemonade"),
          bias=4),
    entry("bread-make", (("bread", "dough", "loaf", "loaves", "baguette", "rolls", "buns"),
                         ("make", "making", "bake", "baking", "recipe", "from scratch", "white",
                          "wholemeal")),
          _bread,
          guard=_leaves_out("yeast"),
          avoid=("rise", "rising", "risen", "yeast", "flat", "puff", "sourdough", "starter",
                 "keep", "store",
                 "stale", "mouldy", "mould", "mold", "fresh", "tastes", "taste", "flavour",
                 "leftover bread", "left over bread", "leftovers bread", "bread leftovers",
                 "old bread", "stale bread", "yesterdays bread", "use up the bread",
                 "use up bread", "using up bread",
                 "naan", "pitta", "pita", "focaccia", "ciabatta", "soda", "banana", "garlic",
                 "cake", "cakes", "fruit", "malt", "drizzle", "teacake", "carrot", "courgette",
                 "zucchini", "pumpkin", "sultana", "sultanas", "raisin", "raisins", "cherry",
                 "long",
                 "gluten", "gluten free", "gluten-free", "rye", "spelt", "spelt flour",
                 "without egg", "without eggs", "no egg", "no eggs", "egg free",
                 "eggless", "temperature", "temp", "degrees", "gas", "mark", "hot", "how hot",
                 "oven"),
          ask=(("how", "what", "which", "recipe", "recipes", "should", "could", "can", "help",
                "advice", "tips"),)),
    entry("yeast-alive", (("yeast", "yeasts"),
                          ("alive", "dead", "died", "active", "test", "testing", "check", "fresh",
                           "old", "out of date", "expired", "expiry", "date", "working", "work",
                           "foam", "foamy", "bubble", "bubbles", "fizzy", "prove", "proof",
                           "rise", "risen", "fail", "failed")),
          "Stir a teaspoon of sugar into 100ml of water that is warm but not hot - about 35C, "
          "blood heat, because over 45C kills it - sprinkle the yeast on top and leave it 10 "
          "minutes. A thick foam across the surface means it is alive and ready to use; if it "
          "sinks and sits there, it is dead, and fresh yeast is the only fix. Do this before you "
          "weigh anything else: it costs ten minutes and it is the first thing to rule out when a "
          "loaf does not rise.",
          avoid=("how do i make", "recipe", "flour", "knead", "oven", "temperature",
                 "how much", "how many", "sourdough", "starter", "baking powder", "fresh bread"),
          ask=(("how", "what", "is", "should", "can", "does", "do", "why", "know", "tell",
                "test", "check", "still"),)),
    entry("dough-tight", (("dough", "doughs", "mix"),
                          ("tight", "stiff", "dry", "firm", "tough", "hard", "stretchy",
                           "elastic", "springy", "tearing", "tears", "resists", "resist",
                           "add water", "more water", "water", "wet", "sticky", "slack",
                           "runny", "sloppy", "tacky", "gooey")),
          _dough,
          avoid=("how do i make", "recipe", "pizza", "pastry", "cookie", "cookies", "cake",
                 "scone", "shortcrust", "biscuit", "breadcrumbs", "breaded", "filo", "puff",
                 "freeze", "freezer", "fridge", "keeping", "keeps", "overnight", "leftover",
                 "chicken", "meat", "fish", "batter"),
          ask=(("my", "should", "can", "do", "how", "what", "is", "why", "add", "need"),)),
    entry("oven-heat", (("what temperature should the oven be", "what temperature should my oven be",
                         "what temperate should the oven be", "what temp should the oven be",
                         "what temperature do i set the oven", "what temperature should i set the oven",
                         "what temp do i set the oven", "what temperature should the oven",
                         "how hot should the oven be", "what heat should the oven be",
                         "what temperature for the oven", "what temperature is the oven",
                         "what temperature should an oven be", "what temperature to cook at",
                         "what temperature should i cook at", "what gas mark should the oven be",
                         "what gas mark should my oven be", "what gas mark for the oven",
                         "what temperature should i put the oven on", "what temp should i put the oven on",
                         "what temperature do you set an oven to", "what temp do you set an oven to",
                         "what temperature is my oven meant to be", "what temperature is an oven meant to be",
                         "what setting should the oven be on", "what setting should the oven be",
                         "what setting should my oven be on", "what setting do i put the oven on"),
                        ("oven", "temperature", "temp", "hot", "heat", "cook", "bake", "set", "gas")),
          "For most things, 180C (160C fan, gas mark 4) for cakes, biscuits, a tray of "
          "vegetables and a slow roast, and 200C (180C fan, gas mark 6) for chips, roast "
          "potatoes and anything you want brown and crisp. Go to 220C (200C fan, gas mark 7) "
          "for a fast pizza or a crisp edge, and down to 150C (130C fan, gas mark 2) for "
          "meringues and slow bakes.",
          avoid=("chips", "chip", "cake", "cakes", "sponge", "chicken", "turkey", "beef", "pork",
                 "lamb", "joint", "bread", "pizza", "pastry", "yorkshire", "muffin", "scone",
                 "biscuit", "cookie", "meringue", "casserole", "fish", "salmon", "lasagne",
                 "lasagna", "pie", "potatoes", "air fryer", "airfryer", "microwave",
                 "slow cooker", "runs hot", "running hot", "too hot", "overheat", "overheats",
                 "calibrate", "thermometer", "dial", "not working", "wont heat", "won't heat",
                 "not heating", "not heat up", "broken", "smoking", "smoke", "fever", "body",
                 "fridge", "freezer", "water", "baby", "milk"),
          bias=1),
    entry("oven-hot", (("oven", "fan", "fan oven", "temperature", "temp", "gas", "gas mark",
                        "dial", "thermometer", "degrees"),
                       ("hot", "hotter", "overheats", "runs hot", "too hot", "running hot",
                        "drop", "lower", "reduce", "adjust", "temperature", "temp",
                        "check", "accurate", "wrong", "thermometer", "fan",
                        "calibrate", "calibrated", "calibration", "calibrating")),
          "Drop the dial about 20C for a fan oven, and check the real heat with a cheap oven "
          "thermometer hung in the middle: an oven that runs 25C hot browns the outside before the "
          "middle is set, which is the commonest reason a bake burns on the bottom and stays raw "
          "in the middle. Trust the thermometer over the dial, turn the tray round halfway "
          "through, and if yours runs hot by a fixed amount, note the number you actually use on "
          "a sticker inside the door.",
          avoid=("bread", "cake", "roast", "chicken", "pizza", "pastry", "yorkshire", "muffin",
                 "scone", "biscuit", "cookie", "casserole", "air fryer", "airfryer",
                 "microwave", "slow cooker", "not heating", "wont heat", "won't heat",
                 "not working", "broken", "smell", "smoke", "door", "light",
                 "noisy", "noise", "loud", "rattl", "rattling", "rattles", "grinding", "squeak",
                 "squeaky", "bulb", "seal", "hinge", "element", "stays on", "stay on",
                 "wont turn off", "won't turn off", "keeps running", "spins", "shelf", "shelves",
                 "rack", "clean", "cleaning",
                 "bill", "bills", "bill has", "bill went", "bill is", "energy", "tariff",
                 "standing charge", "unit rate", "direct debit", "kwh", "boiler",
                 "heating", "radiator", "radiators", "thermostat", "insulation",
                 "smart meter"),
          ask=(("my", "should", "can", "do", "how", "what", "is", "why", "does", "check"),),
          guard=lambda understood: (not a_persons_temperature(understood)
                                    and not something_to_bake_in_the_oven(understood))),
    entry("cake-make", (("cake", "cakes", "sponge", "victoria", "sponges"),
                        ("make", "making", "recipe", "from scratch", "plain", "vanilla",
                         "chocolate")),
          "Weigh 4 eggs in their shells and use the same weight of butter, caster sugar and "
          "self-raising flour: beat the butter and sugar until pale, add the eggs a spoon at a "
          "time, fold in the flour, then split it between two greased 20cm tins. Bake at 180C "
          "(160C fan) for 25 to 30 minutes, until it springs back and a skewer comes out clean, and "
          "sandwich it with jam and buttercream once it is cold.",
          avoid=("time", "temperature", "oven", "sink", "sank", "sunken", "stuck", "burn", "burnt",
                 "nut", "nuts", "allergy", "allergic", "birthday", "party", "freeze", "keeping",
                 "icing", "frosting", "decorate", "vegan", "gluten",
                 "without egg", "without eggs", "no egg", "no eggs", "egg free", "egg-free",
                 "eggless", "flax", "aquafaba", "chocolate") + NO_SUGAR,
          ask=(("how", "what", "which", "recipe", "recipes", "should", "could", "can", "help",
                "advice", "tips"),),
          guard=_leaves_out("egg", "butter")),
    entry("loaf-tin",
          (("loaf tin", "loaf tins", "bread tin", "cake tin", "cake tins", "tin size", "tins",
            "tin"),
           ("what size", "size", "which size", "how big", "how much", "loaf", "bread", "cake",
            "line", "lined", "lining", "grease", "greased", "parchment", "paper", "need",
            "buy", "big", "small", "fit", "fills")),
          _tin_answer,
          avoid=("of beans", "of tomatoes", "of tuna", "of soup", "of peaches", "of sweetcorn",
                 "of chickpeas", "opened", "open tin", "canned", "rust", "recycle", "recycling",
                 "biscuit", "biscuits", "baked beans",
                 "out of the tin", "out of a tin", "out of the pan", "out of a pan",
                 "out of its tin", "out of its pan", "stuck", "sticks",
                 "loosen", "loosening", "wont come out", "won't come out", "turn it out",
                 "turned out", "shrinking", "came out",
                 "roasting tin", "roast tin", "roasting", "roast", "traybake", "tray bake",
                 "chicken", "turkey", "joint of meat",
                 "make bread", "bake bread", "baking bread", "bread in", "bread dough", "knead",
                 "store", "storing", "stored", "keep", "keeps", "keeping", "kept", "how long",
                 "burnt", "burn", "clean", "cleaning", "scrub", "wash", "without butter",
                 "no butter", "instead of butter", "margarine",
                 "grease a cake tin", "grease the cake tin", "grease a loaf tin",
                 "grease the loaf tin", "grease a tin", "grease the tin", "grease and line",
                 "greasing a tin", "how do i grease", "what do i grease",
                 "prepare a cake tin", "prepare the cake tin", "prepare my cake tin",
                 "prepare a loaf tin", "prepare the loaf tin", "prepare a tin",
                 "prepare the tin", "prepare a baking tin", "how do i prepare",
                 "chickpea", "chickpeas", "lentil", "lentils", "beans", "pulses", "soak",
                 "soaking", "soaked", "drained and rinsed",
                 "paint", "painting", "paint tin", "emulsion", "wallpaper", "gloss", "undercoat"),
          ask=(("how", "what", "which", "should", "could", "can", "do i", "size", "help")),
          bias=1),
    entry("soup-make", (("soup", "soups"),
                        ("make", "making", "recipe", "vegetable", "chicken", "lentil", "leek",
                         "squash", "carrot", "from scratch")),
          "Soften a chopped onion in oil with a pinch of salt for 8 to 10 minutes, add the main "
          "vegetable - about 700g of squash, carrots, leeks or tomatoes - then cover it with a "
          "litre of stock and simmer 20 minutes until everything is soft. Blend it, taste for salt "
          "at the end, and add a potato or a handful of lentils if you want it thicker without cream.",
          avoid=("thick", "thinner", "runny", "bland", "salty", "keep", "freeze", "reheat",
                 "leftover", "tinned", "tin", "packet", "sachet", "canned", "shop",
                 "lentil", "lentils", "chickpea", "chickpeas", "split peas", "beans", "pulses"),
          ask=(("how", "what", "which", "recipe", "recipes", "should", "could", "can", "help",
                "advice", "tips", "making", "make", "made", "cooking", "cook", "want", "wanted",
                "fancy", "planning"),)),
    entry("slow-cooker-chicken", (("chicken", "bird", "chicken thighs"),
                                  ("slow cooker", "slow-cooking", "slow cooked", "crockpot",
                                   "crock pot", "slowcooker", "slow")),
          "In a slow cooker a 2kg chicken takes 4 to 5 hours on low, or 3 hours on high: sit it on "
          "a few balls of foil so it is not stewing in its own juice, and do not add water, as it "
          "makes plenty. Check the thigh juices run clear and the thickest part reaches 75C before "
          "you take it out.",
          avoid=("frozen", "defrost", "thighs only", "breast", "leg", "legs", "drumstick",
                 "drumsticks"), bias=1),
    entry("bread-rise", (("bread", "breads", "dough", "sourdough", "loaf", "loaves",
                          "focaccia", "pitta", "pita", "naan", "buns", "bun", "rolls",
                          "baguette", "ciabatta"),
                         ("rise", "rising", "risen", "flat", "yeast", "puff up", "puffed up",
                          "prove", "proves", "proving", "proved", "proof", "proofed",
                          "proofing")),
          _bread_rise_answer(),
          avoid=("mouldy", "mould", "mold", "stale",
                 "shelf life", "shelf-life", "store", "storing", "storage",
                 "keep fresh", "keeps fresh", "stays fresh", "stay fresh", "keeps for",
                 "keep for", "in the fridge", "in the freezer", "how do i keep", "how to keep",
                 "taste", "tastes", "tasting", "flavour", "flavourless", "bland", "seasoned",
                 "seasoning", "salt", "salty",
                 "without", "yeastless",
                 "sink", "sinks", "sinking", "sank", "sunk", "collapse", "collapses",
                 "collapsed", "collapsing", "deflate", "deflates", "deflated", "fallen",
                 "fell", "caved in", "caves in", "flopped"),
          bias=1),
    entry("cake-keep", ("cake", ("keep", "keeps", "keeping", "last", "lasts", "store", "storing",
                                 "fridge", "freeze", "frozen", "shelf life", "shelf-life",
                                 "how long", "still good", "gone off",
                                 "stale", "going stale", "go stale", "goes stale", "stay fresh",
                                 "stays fresh", "keep fresh", "keeps fresh", "fresh for")),
          "A plain sponge or fruit cake keeps 3 to 4 days in a tin, and a week in the fridge if it "
          "has fresh cream or custard in it. Undecorated, it freezes well for 2 months: wrap it "
          "whole, and ice it after it thaws. It goes stale because the starch firms up rather than "
          "because it dries out: a tin with a lid, half an apple in it, and 15 seconds in the "
          "microwave brings a slice back.",
          ask=KEEP_ASK,
          avoid=("bake", "baking", "oven", "tin size", "sink", "sank", "rise", "risen", "recipe",
                 "freeze", "freezing", "frozen", "how long in the oven", "how long do i bake",
                 "how long should i bake", "take", "takes", "take to cook", "start to finish",
                 "use up", "using up", "use it up", "use them up")),
    entry("baked-keep", (BAKED_GOODS_WORDS,
                         ("keep", "keeps", "keeping", "last", "lasts", "store", "storing",
                          "how long", "still good", "gone off", "shelf life", "shelf-life",
                          "fridge", "freeze", "frozen", "stale", "going stale", "stay fresh")),
          _baked_keep(),
          ask=KEEP_ASK,
          avoid=("bake", "baking", "oven", "recipe", "how long in the oven", "how long do i bake",
                 "how long should i bake", "take", "takes", "take to cook", "start to finish",
                 "temperature", "degrees", "gas mark", "why is", "why are", "why do", "sink",
                 "sank", "rise", "risen", "gooey", "crispy", "chewy", "burnt", "burn",
                 "use up", "using up", "use it up", "use them up")),
    entry("butter-keep", ("butter", ("keep", "keeps", "keeping", "last", "lasts", "store",
                                     "storing", "fridge", "freeze", "frozen", "shelf life",
                                     "shelf-life", "how long", "still good", "gone off",
                                     "rancid", "gone rancid", "smells off", "tastes off",
                                     "smells funny", "smells bad", "gone bad", "is it off",
                                     "out of the fridge", "soften")),
          "Butter keeps 2 to 3 weeks in the fridge and about 4 days in a covered dish on the "
          "counter; salted lasts longer than unsalted. It freezes for 3 months, cut into what you "
          "use in a fortnight. Rancid butter smells like old paint and tastes sharp, so bin it.",
          ask=KEEP_ASK + ("rancid", "gone rancid", "smells off", "tastes off", "smells funny",
                          "smells bad", "gone bad", "off"),
          avoid=("freeze", "freezing", "frozen", "make butter", "churn", "substitute",
                 "instead of butter", "margarine", "vegan butter", "buttercream", "shortbread",
                 "pastry", "biscuit",
                 "soften", "softening", "soft", "quickly", "quick",
                 "hard to spread", "too hard", "spread")),
    entry("avocado-keep", (("avocado", "avocados", "avocado half"),
                           ("keep", "keeps", "keeping", "last", "lasts", "store", "storing",
                            "fridge", "brown", "cut", "once cut", "half", "ripen", "ripe",
                            "shelf life", "shelf-life", "how long")),
          "A cut avocado keeps 1 to 2 days in the fridge: leave the stone in, press cling film "
          "right onto the cut face, and squeeze lemon or lime over it. The surface browns where "
          "air gets to it, which is harmless - scrape that bit off. A whole hard one ripens on the "
          "counter in 3 to 5 days and then keeps a day or two in the fridge.",
          ask=("how", "what", "can", "should", "does", "do", "will", "long", "keep", "keeps",
               "last", "lasts", "is", "are", "still", "ok", "okay", "safe", "store", "storing"),
          avoid=("grow", "tree", "plant", "guacamole", "toast", "recipe", "salad")),
    entry("leftover-pizza", (("pizza", "pizzas", "leftover pizza", "cold pizza"),
                             ("leftover", "left over", "cold", "next day", "keep", "keeps",
                              "fridge", "reheat", "reheating", "safe", "ok to eat", "still good",
                              "how long", "last", "lasts", "freeze")),
          "Cold pizza is fine if it went into the fridge within a couple of hours of arriving: eat "
          "it within 3 days, and reheat it to piping hot if you want it hot again - a splash of "
          "water in the pan or 10 minutes in a hot oven brings the base back. Pizza left out "
          "overnight is the one to throw away.",
          ask=("how", "what", "can", "should", "does", "do", "will", "long", "keep", "keeps",
               "last", "lasts", "is", "are", "still", "ok", "okay", "safe", "cold", "left",
               "leftover", "reheat", "eat"),
          avoid=("restaurant", "takeaway", "delivery", "delivered", "deliver", "order",
                 "wrong order", "charged", "complaint", "complain", "refund", "manager",
                 "arrived", "arrive", "cold when", "when it arrived", "waited", "late",
                 "missing",
                 "box", "boxes", "bin", "bins", "recycling", "recycle", "cardboard", "compost",
                 "throw away", "get rid",
                 "freeze", "freezing", "frozen", "reheat", "reheating", "warm it up",
                 "dough",
                 "oven", "bake", "baking", "baked", "to cook", "how long to cook",
                 "how long should i cook", "should i cook", "how long can i cook",
                 "how long do you cook", "cooking time", "how long do i cook",
                 "temperature", "degrees", "gas mark", "minutes", "how hot",
                 "take to cook", "takes to cook", "time in the oven")),
    entry("bread-slice", (("bread", "loaf", "loaves", "sourdough"),
                          ("slice", "slices", "sliced", "slicing", "cut", "cutting", "thick",
                           "thickness", "thin", "evenly", "warm", "hot", "stale", "stales",
                           "staling")),
          _bread_sliced, bias=3,
          avoid=("cake", "cakes", "sponge", "loaf cake", "banana bread", "malt loaf", "teacake",
                 "mould", "mouldy", "mold", "moldy", "gone off", "bin it", "toaster", "toasted",
                 "make", "bake", "baking", "recipe", "ingredients", "knead", "prove", "oven",
                 "crumbs", "breadcrumbs", "pudding", "sauce", "filling", "slice of cake",
                 "pizza", "cheese", "ham", "shop", "buy", "supermarket", "price", "baker",
                 "keep", "keeps", "keeping", "store", "storing", "fresh", "longer", "last",
                 "lasts", "lasting", "freeze", "freezer", "frozen", "shelf life", "paper bag",
                 "bread bin", "fridge",
                 "is it ok", "is it okay", "alright", "all right", "safe", "healthy", "good for",
                 "bad for", "fine to eat", "better for you", "ok", "okay",
                 "refresh", "revive", "bring it back", "bring it round", "use up", "leftover",
                 "leftovers", "do with", "fault", "dense", "sank", "sunken", "flat", "risen",
                 "rise", "rising", "prove", "proving", "knead", "kneaded",
                 "how much", "how many", "protein", "calories", "calorie", "carbs", "carb",
                 "salt", "sugar", "fibre", "fiber", "iron", "vitamin", "healthy",
                 "how long", "stale by", "already stale", "went stale", "gone stale",
                 "knife", "falls apart", "falling apart")),
    entry("bread-keep", (("bread", "loaf", "loaves"),
                          ("keep", "store", "fresh", "last", "longer", "soft", "freeze",
                                   "fridge", "bin", "paper bag", "hard", "dry",
                                   "shelf life", "shelf-life")
                          + PACK_DATE),
          _bread_kept,
          ask=KEEP_ASK,
          avoid=("stale", "going stale", "rise", "rising", "risen", "eggy", "bread and butter",
                 "garlic")),
    entry("jar-keep", (("jar", "pesto", "pickle", "pickles", "chutney", "jam", "marmalade",
                        "ketchup", "mustard", "mayonnaise", "mayo", "salsa", "dip", "tahini",
                        "puree", "purees", "tomato puree", "tomato paste"),
                       ("opened", "open", "keep", "last", "fridge", "safe", "how long", "gone off",
                        "off", "ok", "store")),
          ("Once a jar is opened it lives in the fridge: pesto, sauces and ketchup are usually good "
           "for 1 to 2 weeks, pickles, chutney, jam and mustard for months, and the label's "
           "once-opened line beats any general rule. Keep the surface under a little oil and bin it "
           "if it smells sharp or the lid bulges."),
          avoid=("rice", "pasta", "spaghetti", "noodles", "flour", "lentils", "porridge",
                 "oats", "sugar", "cereal", "couscous", "quinoa"),
          ask=KEEP_ASK),
    entry("container-keep-follow", (("it", "that", "them", "the jar", "the bottle"),
                                    ("last", "lasts", "keep", "keeps", "fridge", "how long",
                                     "storing", "store")),
          _container_keep,
          ask=("last", "lasts", "keep", "keeps", "fridge", "how long", "storing", "store"),
          bias=3,
          avoid=OPEN_ASK + TOOTH_OUT + ("lid", "lids", "stuck", "budge", "tight", "loosen",
                            "undo", "jar",
                            "holiday", "holidays", "annual leave", "days leave", "saved up",
                            "carry over", "carried over", "entitlement",
                            "put me down", "puts me down", "putting me down",
                            "keep it up", "keep going", "habit", "routine", "motivation",
                            "keep it down", "keep the noise down", "turn it down",
                            "noise", "noisy", "loud", "louder", "quiet", "quieter",
                            "music", "radio", "neighbour", "neighbours", "next door",
                            "colleague", "colleagues", "coworker", "coworkers", "co-worker",
                            "co-workers", "workmate", "workmates", "teammate", "teammates",
                            "at work", "office", "my desk", "the desk")
          + tuple(_FOOD) + ("milk", "cheese", "yogurt", "yoghurt", "cream", "butter", "eggs",
                            "rice", "pasta", "bread", "salad", "wine", "beer", "stock",
                            "day", "days", "week", "weeks", "month", "months",
                            "breakup", "break up", "broke up", "my ex", "relationship",
                            "grief", "grieving", "mourning", "bereavement", "heal",
                            "healing", "get over", "getting over", "divorce",
                            "does it take to", "will it take to", "would it take to",
                            "will it take", "would it take", "does it take",
                            "always full", "never use it all", "never use it", "never use them",
                            "use it all up", "waste", "wasting", "wasted", "went to waste",
                            "throw it away", "thrown away", "in the bin", "goes off",
                            "busy", "occupied", "entertained", "journey", "long journey",
                            "long drive", "car journey", "road trip", "motorway",
                            "flight", "plane", "ferry")),
    entry("stuck-jar", (("jar", "lid", "lids", "jam jar", "pickle jar", "screw top", "screw-top",
                         "vacuum seal", "cap"),
                        ("open", "opening", "stuck", "tight", "budge", "loosen", "undo", "turn",
                         "wont open", "won't open", "cant open", "can't open", "cannot open",
                         "hard to open", "get the lid off", "lid off", "stubborn", "grip",
                         "wont come off", "will not come off", "wont go back on",
                         "will not go back on", "stuck shut")),
          _stuck_jar,
          avoid=("sterilise", "sterilize", "sterilising", "preserve", "preserving", "baby",
                 "babies", "formula", "teat", "mould", "mouldy", "mold", "moldy",
                 "keep", "keeps", "last", "lasts", "fridge", "how long", "how many", "how much",
                 "how big", "how full", "gone off", "store", "stored", "storing", "where",
                 "storage", "shelf life"),
          bias=2),
    entry("open-wine", (("wine", "bottle of red", "bottle of white", "bottle of wine",
                         "red wine", "white wine", "rose wine"),
                        ("open", "opened", "bottle", "keep", "last", "how long",
                         "left over", "leftover", "vinegary", "gone off", "fridge")),
          ("An open bottle keeps 3 to 5 days: stopper it and keep it in the fridge, reds too, and "
           "take a red out an hour before you drink it. A vacuum stopper or a squirt of inert gas "
           "buys another day or two, and after that the wine is still fine for cooking - wine that "
           "has turned vinegary is a good vinegar."),
          avoid=("how do i open", "how to open", "how can i open", "how do you open",
                 "how would i open", "ways to open", "get the cork out", "get it open",
                 "crack it open", "pop the cork", "uncork", "corkscrew", "screw cap",
                 "twist the cap"),
          ask=KEEP_ASK),
    entry("wine-gone-flat", (("wine", "bottle of red", "bottle of white", "bottle of wine",
                              "red wine", "white wine", "rose wine", "prosecco", "champagne",
                              "sparkling wine", "cava"),
                             ("flat", "taste flat", "tastes flat", "tasting flat", "gone flat",
                              "goes flat", "went flat", "tastes dull", "lost its fizz",
                              "no fizz", "not fizzy")),
          ("Flat means the fizz has gone, or - in a still wine - the fresh edge that made it "
           "worth drinking, because the gas and the aromas escape as soon as air gets in. A "
           "stopper and the fridge slow that to 3 to 5 days; a vacuum stopper or a squirt of "
           "inert gas buys a day or two more. Past that it is cooking wine, and wine that has "
           "turned vinegary is a good vinegar."),
          avoid=("still flat", "bottle flat", "flat tyre", "flat battery", "leftover",
                 "left over", "how long", "keep", "keeps", "last", "lasts", "still good",
                 "fridge", "store", "storing", "shop", "buy"),
          bias=1),
    entry("wine-with-food", (("wine", "red wine", "white wine", "rose wine"),
                             ("goes with", "go with", "pair", "pairs", "pairing", "match",
                              "choose", "pick", "which", "good", "buy", "recommend",
                              "dinner", "roast", "steak", "fish", "chicken", "curry", "pasta",
                              "cheese", "pudding", "dessert", "party", "meal", "serve")),
          ("Match the weight, not the colour: a light white with fish or chicken, a fuller red "
           "with red meat and stews, and rose or a light red in between. If you are guessing, a dry "
           "white or a medium red goes with nearly everything on a table, acidity cuts through fat, "
           "and a slightly sweet white is the safer bet with a hot curry. Serve reds a little cool "
           "and buy two bottles of one cheaper wine rather than one expensive one."),
          avoid=("open", "opened", "keep", "keeps", "last", "how long", "left over", "leftover",
                 "vinegary", "gone off", "fridge", "corkscrew", "opener", "stain", "stains",
                 "spill", "spilled", "spilt", "carpet", "sofa", "shirt", "gift", "present",
                 "freeze", "frozen", "vinegar", "alcohol free", "units", "pregnant",
                 "good for you", "bad for you", "healthy", "health", "benefit", "benefits",
                 "calories", "safe",
                 "cook", "cooking", "cooked", "recipe", "recipes", "oven", "bake", "sauce",
                 "stew", "marinate", "marinade", "risotto", "substitute", "instead of",
                 "reduce", "deglaze", "how much"),
          bias=2),
    entry("freeze-food", (("freeze", "freezer", "freezing", "frozen"),
                          _FREEZE_FOOD_WORDS),
          _freeze_food,
          ask=KEEP_ASK,
          avoid=("soup", "soups", "broth", "mashed potato", "mash", "refreeze", "refroze",
                 "re-freeze", "thawed", "already thawed", "freeze again", "defrost",
                 "defrosting", "defrosted",
                 "stew", "stews", "casserole", "casseroles", "curry", "curries", "chilli",
                 "chili", "bolognese", "lasagne", "lasagna", "leftover", "leftovers",
                 "left over",
                 "instead", "instead of", "in place of", "substitute", "swap",
                 "how do i cook", "how long do i cook", "how to cook", "how do i reheat",
                 "how do i heat", "air fryer", "what temperature", "in the oven",
                 "from frozen", "slow cooker", "straight from frozen",
                 "brain freeze", "brainfreeze", "ice cream headache") + _FREEZE_AVOID),
    entry("cake-time", ("cake", ("how long", "bake", "baking", "time", "oven")),
          "A 20cm sponge bakes at 180C (160C fan) for 25 to 30 minutes; a loaf tin needs 45 to 55. "
          "It's done when a skewer in the middle comes out clean, and it's worth checking 5 minutes "
          "early the first time. About an hour and a half start to finish, counting mixing and "
          "cooling.",
          avoid=("keep", "keeps", "keeping", "last", "lasts", "lasting", "stale", "fresh",
                 "store", "stored", "storing", "storage", "freeze", "fridge", "freezer",
                 "reheat", "leftover", "leftovers", "go off", "gone off")),
    entry("cake-plan", ("cake", ("birthday", "party", "celebrate", "celebrating")),
          "A two-layer chocolate or madeira sponge is the easy crowd-pleaser: bake it the day before, "
          "wrap it well and fill it with buttercream on the day. One 20cm tin serves 8 to 10 people "
          "generously.",
          avoid=("how long", "time", "oven", "temperature"), bias=1),
    entry("party-bake", (("bake", "baking", "baked", "bakes", "make", "making"),
                         ("birthday", "birthday party", "party", "celebration", "christening",
                          "birthday tea", "party tea", "gathering", "friends coming",
                          "family coming")),
          ("For a birthday tea, a big chocolate or lemon traybake cut into squares is the easy "
           "one: one tin feeds 15 and you bake it the day before. Then a batch of fairy cakes, "
           "some jam tarts and a plate of sausage rolls, and the table is done.",
           "Bake a traybake the day before the party - chocolate or lemon, one tin feeds 15 in "
           "squares - then add fairy cakes, jam tarts and sausage rolls. That covers a birthday "
           "tea without any decorating."),
          guard=lambda reading: not amends_to(line_of(reading)),
          avoid=("how long", "temperature", "oven", "gas mark", "weigh", "store", "keep",
                 "freeze", "fridge", "speech", "present", "gift", "games", "decorate",
                 "decorations", "wear", "outfit", "invitations", "invites", "venue",
                 "dinner party", "dinner", "supper", "tea party", "meal", "main course",
                 "starter", "roast", "curry", "barbecue", "bbq",
                 "coffee", "wine", "beer", "lemonade", "squash", "punch", "cocktails",
                 "conversation", "small talk", "mingle", "mingling", "nobody to talk",
                 "know anyone", "networking", "talk to people", "what to say", "talk about",
                 "nervous", "strangers"),
          bias=1),
    entry("tea-party-food", (("ideas", "idea", "suggest", "suggestions", "food", "serve",
                              "make", "making", "bake", "baking", "what shall i"),
                             ("birthday tea", "party tea", "christening tea", "afternoon tea",
                              "tea party", "tea for")),
          ("A birthday tea is sandwiches and cake, not a dinner: white bread with the crusts off, "
           "filled with ham, cheese or egg mayo, then sausage rolls, a plate of crisps, and a "
           "traybake or a Victoria sponge with fairy cakes for the children, or scones with jam "
           "and cream for an afternoon tea. Nothing needs serving hot, so it can be made that "
           "morning.",
           "Keep it to sandwiches, something savoury and cake: fill white bread with ham, cheese "
           "or egg mayo, add sausage rolls, then a big sponge or traybake and fairy cakes. A jug "
           "of squash and a pot of tea, and nothing has to be hot."),
          avoid=("dinner", "supper", "roast", "curry", "meal", "cup of tea", "brew",
                 "caffeine", "green tea")),
    entry("cake-nut-free", ("cake", ("nut", "nuts", "allergy", "allergic", "allergies")),
          ("Go for a chocolate cake with no nuts at all: a plain chocolate sponge with cocoa and "
           "boiling water, iced with melted chocolate and cream. Check the chocolate and any "
           "ready-made icing for 'may contain nuts', and keep the worktop and tin clean if the "
           "allergy is serious.")),
    entry("sourdough-start", (("sourdough", "sourdough starter", "starter", "wild yeast"),
                              ("make", "making", "start", "starting", "begin", "create",
                               "from scratch", "grow", "first time", "recipe",
                               "keep it going")),
          "Stir 50g strong white flour and 50g water in a jar and leave it covered at room "
          "temperature. Every day throw half away and feed it the same 50g plus 50g. It bubbles "
          "within three to five days and is ready when it doubles in 4 to 6 hours, smells of "
          "yoghurt and tastes sour: 5 to 7 days in all. Rye or wholemeal flour starts faster; "
          "chlorinated tap water can slow it down.",
          avoid=("car", "engine", "motor", "ignition", "battery", "won't turn over",
                 "feed", "feeds", "feeding", "fed", "bubbling", "bubbles", "bubbly",
                 "smell", "smells", "acetone", "hooch", "alive", "dead", "rise", "rising")),
    entry("sourdough-feed", (("sourdough", "starter", "sourdough starter"),
                             ("feed", "fed", "bubbly", "bubbling", "bubbles", "alive", "rise",
                              "rising", "smell", "smells", "smelling", "acetone", "hooch",
                              "start", "starting", "begin", "beginning", "make", "making",
                              "create", "grow", "get going", "going", "from scratch",
                              "ready", "know", "wake", "wakes", "waking", "woke", "woken",
                              "wake up", "double", "doubles", "doubled", "doubling",
                              "look after", "care for")),
          "Feed a sourdough starter equal weights of flour and water, about its own weight, once a "
          "day at room temperature. To start one from nothing, mix 50g of wholemeal flour with 50g "
          "of water and feed it the same way every day - it takes about a week of that before it "
          "doubles reliably. It is ready to bake with when it doubles within 4 to 6 hours and "
          "smells of yoghurt rather than acetone.",
          avoid=("name", "called", "call", "ideas", "mould", "mouldy", "mold", "moldy",
                 "motor", "motors", "engine", "engines", "car", "cars", "van", "van's",
                 "battery", "lawnmower", "lawn mower", "motorbike", "motorcycle", "scooter",
                 "tool", "tools", "solenoid", "ignition", "alternator")),
    entry("sugar-grainy", (_GRAIN_FOOD, _GRAIN_WORD),
          _grainy,
          avoid=("chocolate", "choc", "honey", "maple", "bread", "cake", "biscuit", "cookie",
                 "meat", "chicken", "beef", "pork", "rice", "pasta", "potato", "potatoes")),
    entry("sugar-work", (("sugar", "sugars", "caramel", "toffee", "fudge", "praline",
                          "brittle", "syrup", "candy"),
                         ("dissolve", "dissolves", "dissolved", "dissolving", "dissolv",
                          "melt", "melts", "melting", "melted", "crystallise", "crystallised",
                          "crystallising", "crystallize", "crystallized", "crystalise",
                          "crystalised", "crystals", "grainy", "grain", "clear", "syrup",
                          "caramel", "caramelise", "caramelize", "toffee", "brittle", "boiling",
                          "bitter", "burnt", "stir", "stirring", "make", "making", "made",
                          "hard", "hardened", "hardens", "block", "solid", "lumps", "lumpy",
                          "soften", "softens", "softening")),
          _sugar_work,
          bias=1,
          avoid=("how much sugar", "calories", "calorie", "diabetes", "diabetic",
                 "grainy", "grain", "gritty", "granular", "sandy", "crunchy",
                 "cake", "cakes", "biscuit", "biscuits", "cookie", "cookies", "bread",
                 "sugar free", "free",
                 "diet", "blood sugar", "hyper", "children", "child", "kids", "kid", "toddler",
                 "baby", "tooth", "teeth", "addicted", "addiction", "quit", "give up", "eat less",
                 "cut down", "cravings", "chocolate", "choc", "honey", "maple",
                 "fat", "fatter", "fattening", "weight", "lose weight", "gain weight",
                 "healthy", "unhealthy", "bad for", "good for", "addictive", "energy",
                 "sleepy", "hyperactive", "mood", "skin", "acne",
                 "icing", "frosting", "buttercream", "fondant", "dog", "dogs", "cat", "cats",
                 "puppy", "kitten")),
    entry("chocolate-seize", (("chocolate", "choc"),
                              ("seize", "seized", "seizing", "melt", "melting", "melted", "grainy",
                               "dip", "dipped", "dipping", "strawberry", "strawberries", "fruit",
                               "stiff", "thick", "lumpy", "bloom", "white", "grey", "gray",
                               "streak", "streaks", "temper", "tempering", "microwave", "water bath",
                               "bain marie")),
          _chocolate),
    entry("bake-fault", (_BAKE_THING, _BAKE_FAULT),
          _bake_fault,
          avoid=("keep", "freeze", "fridge", "how long", "recipe", "how do i make"),
          bias=1),
    entry("cookie-spread", (("cookie", "cookies", "biscuit", "biscuits", "shortbread"),
                            ("spread", "spreading", "flat", "thin", "melt", "melted", "run",
                             "running", "wide", "squash", "pool", "grease", "greasy")),
          _cookies),
    entry("biscuit-hard", (("biscuit", "biscuits", "cookie", "cookies", "shortbread", "scone",
                            "scones"),
                           ("hard", "harder", "tough", "rock", "rocky", "dry", "stale", "brittle",
                            "snap", "breaks")),
          "Hard biscuits are usually baked a couple of minutes too long or worked too much: pull "
          "them out while the middles still look slightly soft, because they firm as they cool, "
          "and mix just until the flour is in. More butter or an extra yolk keeps them short, and "
          "a slice of bread in the tin softens them overnight.",
          avoid=("scone is dry", "scone is tough", "scone is chewy", "scones are dry",
                 "scones are tough", "scones are chewy", "scone too dry", "scones too dry",
                 "scones dry", "scone dry", "scones tough", "scone tough", "scones chewy",
                 "scone chewy", "scones came out dry", "scones went dry", "scones were too dry",
                 "scone was too dry", "scones are too dry", "scone is too dry")),
    entry("biscuit-crumble", (("biscuit", "biscuits", "cookie", "cookies", "shortbread", "scone",
                               "scones"),
                              ("crumbly", "crumbles", "crumble", "crumbs", "falling apart",
                               "falls apart", "fell apart", "sandy")),
          "Crumbly biscuits have too little fat or too much flour, and the dough was worked too "
          "long: weigh the butter properly, rub it in until it looks like breadcrumbs, and stop "
          "mixing the moment it comes together. Let them cool on the tray, because they are "
          "fragile while hot, and handle the dough as little as you can."),
    entry("jam-make",
          (("jam", "marmalade", "chutney", "preserve", "preserves", "fruit cheese"),
           ("make", "making", "homemade", "from scratch", "my own", "recipe", "sugar",
            "how do i start", "what fruit")),
          lambda memory, understood: _jam_make(understood),
          avoid=("set", "setting", "sets", "runny", "too thin", "firm", "pectin", "sterilise",
                 "sterilize", "sterilising", "jar", "jars", "store", "storing", "keep",
                 "keeping", "mouldy", "mould", "freeze", "frozen", "how long") + NO_SUGAR),
    entry("bake-always", (("baking", "bake", "bakes", "baked", "everything i bake", "all my bakes",
                           "my cakes", "my loaves", "my bakes", "when i bake", "whatever i bake"),
                          ("always", "never", "every time", "every single time", "each time",
                           "no matter what", "whatever i do", "always comes", "always come",
                           "always does", "never comes", "never come",
                           "everything i bake", "whatever i bake", "all my bakes", "when i bake")),
          _bake_always,
          avoid=("how long", "keep", "keeps", "freeze", "fridge", "recipe", "how do i make",
                 "buy", "shop", "calories", "healthy", "what temperature", "how hot"),
          bias=1),
    entry("bake-keep-follow", (_BAKE_KEEP_SHAPES,
                               ("it", "they", "them", "keep", "last", "long", "days", "freeze")),
          _bake_keep, bias=1),
    entry("bake-follow", (_BAKE_FOLLOW_SHAPES,
                          ("i", "it", "that", "them", "they", "wrong", "happen", "again", "stop",
                           "use", "eat", "ok", "differently", "else", "right", "fix", "next")),
          _bake_follow,
          avoid=("keep", "keeps", "last", "lasts", "fridge", "freeze", "reheat", "reheat",
                 "how long",
                 "toast", "toastie", "toasties"),
          bias=1),
    entry("jam-set", (("jam", "jelly", "marmalade", "chutney"),
                      ("set", "setting", "runny", "thin", "firm", "setter", "pectin", "test",
                       "plate", "wrinkle", "sugar", "how long", "boil")),
          "Jam sets at 104 to 105C, so boil it hard for 10 to 15 minutes and test a drop on a cold "
          "plate: push it with a finger, and if it wrinkles it is ready. Jam that stays runny has "
          "had too little sugar or too little pectin - add a handful of gooseberries or a squeeze "
          "of lemon and boil it again."),
    entry("jar-sterilise", (("jar", "jars", "bottle", "bottles"),
                            ("sterilise", "sterilize", "sterilising", "sterilizing", "clean",
                             "cleaning", "wash", "washing", "scald", "preserve", "preserving",
                             "jam", "chutney")),
          "Wash the jars in hot soapy water, rinse them, and stand them upside down in an oven at "
          "120C for 15 minutes; fill them while they are still hot. Lids go in a bowl of boiling "
          "water for a minute, and a dishwasher on its hottest cycle does the same job.",
          avoid=("baby", "babies", "formula", "teat", "teats", "feeding", "mould", "mouldy",
                 "mold", "moldy", "water bottle", "water bottles", "gym bottle", "sports bottle",
                 "drink bottle", "drinking bottle", "flask", "thermos", "hot water bottle",
                 "bottle of water", "reusable")),
    entry("butter-soften", ("butter", ("soften", "soft", "room temperature", "quick", "hard",
                                       "hard to spread", "spread", "spreading")),
          "Cut cold butter into small cubes and leave it 15 minutes, or grate it; both soften it "
          "fast without melting it. Don't microwave it, because butter that's too warm splits a "
          "cake mix.",
          bias=2,
          avoid=("how long", "keep", "keeps", "keeping", "last", "lasts", "still good",
                 "gone off", "go off", "shelf life", "fridge", "freeze", "frozen", "out of the fridge",
                 "safe to leave out", "leave out")),
    _swap("swap-buttermilk", (("buttermilk",), _SWAP_ASK),
          "For 250ml of buttermilk: 250ml of milk with a tablespoon of lemon juice or white "
          "vinegar, left 10 minutes to thicken. Plain yoghurt thinned with milk works too, and so "
          "does sour cream loosened with a splash of milk."),
    _swap("swap-cream", (("cream", "sour cream", "double cream", "single cream", "creme fraiche"),
                         _SWAP_ASK),
          "For cooking: milk with a knob of butter and a teaspoon of cornflour thickens much like "
          "cream. Cold, or on the side: plain yoghurt, sour cream or creme fraiche. Stir those in "
          "off the heat, because cream and yoghurt split if they boil."),
    _swap("swap-eggs", (("egg", "eggs"), _SWAP_ASK),
          "In cakes and biscuits, one egg becomes 60g of yoghurt, half a mashed banana, or a "
          "tablespoon of ground flax or chia stirred into 3 tablespoons of water and left 10 "
          "minutes. Those bind but do not lift, so add half a teaspoon of baking powder. For "
          "glazing or binding mince, a little milk or oil does the job.",
          avoid=("quiche", "quiches", "tart", "tarts", "flan", "flans", "frittata",
                 "frittatas", "custard", "creme anglaise", "pastry cream", "custard tart")),
    entry("no-eggs-in-a-set-custard",
          (("quiche", "quiches", "tart", "tarts", "flan", "flans", "frittata", "frittatas",
            "custard tart", "egg custard"),
           ("without eggs", "without egg", "no eggs", "no egg", "egg free", "egg-free",
            "eggless", "out of eggs", "ran out of eggs", "run out of eggs", "no eggs left",
            "cant eat eggs", "can't eat eggs", "allergic to eggs", "egg allergy",
            "instead of eggs", "replace the eggs", "replace eggs", "swap the eggs")),
          "A quiche is set by its eggs, so leaving them out gives you warm vegetables in a "
          "pastry case rather than a quiche. The nearest thing is 300g of silken tofu blended "
          "smooth with a tablespoon of cornflour, or 100g of chickpea flour whisked with 250ml "
          "of water and a spoon of oil for a firmer, nuttier set: bake either at 180C for 30 to "
          "35 minutes, until the middle still wobbles. If the reason is an allergy, read the "
          "pastry label too, because some shortcrust has egg in it.",
          bias=2),
    entry("drain-a-tin",
          (("tin", "tins", "can", "cans", "tinned", "canned", "can of", "tin of"),
           ("drain", "draining", "drained", "strain", "straining", "get the water out",
            "get the oil out", "water out", "oil out", "brine", "juice", "liquid")),
          "Open the tin most of the way, hold the lid down with your thumb and tip it over the "
          "sink with a gap of about a centimetre, so the liquid runs out and the food stays in. "
          "Pressing the lid flat and squeezing is tidier still, and the lid laid over a bowl "
          "makes a strainer if you want to keep the oil or brine for a dressing. Tuna in water "
          "wants a good press before the mayo; chickpeas and sweetcorn want a rinse as well.",
          avoid=("drain outside", "drain cover", "manhole", "gully", "gutter", "downpipe",
                 "plughole", "sink", "shower", "bath", "blocked", "smell", "smells", "boiling "
                 "water", "bicarbonate", "vinegar", "battery", "phone", "laptop", "pond",
                 "chickpeas", "chick peas", "beans", "bean", "lentils", "lentil", "pulses"),
          bias=1),
    _swap("swap-butter", (("butter",), _SWAP_ASK),
          "In cakes and biscuits, margarine at the same weight, or a neutral oil at about "
          "three-quarters of the weight. For frying and greasing, any oil will do. Do not swap the "
          "butter in pastry, shortbread or buttercream, where its taste is the whole point."),
    entry("butter-splits-when-melted", (("butter", "butters"),
                                        ("melt", "melts", "melted", "melting", "split",
                                         "splits", "splitting", "separated", "separates",
                                         "seized", "grainy", "oily")),
          "Melt it on the lowest heat, in small pieces, and take the pan off as soon as most of it "
          "has gone - the rest melts in the warm pan. Butter splits when it gets too hot, because "
          "the milk solids cook and squeeze the fat out and it goes grainy and oily: a split "
          "batch comes back if you let it cool a little and whisk in a teaspoon of cold water, "
          "and simply warming it again will not fix it.",
          avoid=("instead", "substitute", "swap", "replace", "alternative", "ran out",
                 "run out", "dont have", "don't have", "havent got", "haven't got",
                 "how long", "keep", "keeps", "fridge", "freeze", "frozen", "gone off",
                 "rancid", "no butter", "without butter", "dairy free", "vegan",
                 "sauce", "sauces", "hollandaise", "beurre blanc", "cake", "cakes", "pastry",
                 "shortbread", "biscuits", "frosting", "buttercream", "cookie", "cookies",
                 "toast", "sandwich", "scones", "crumbs", "mould", "mold")),
    entry("swap-soy-sauce-shortage", (("soy sauce", "soya sauce", "soy", "soya", "no soy sauce",
                              "no soya sauce"), _SWAP_ASK),
          "Salt is the honest swap: about a quarter teaspoon of salt for each tablespoon of soy "
          "sauce, with a splash of water so the dish does not dry out. Tamari is the same thing "
          "without the wheat, and in a marinade a teaspoon of balsamic or Worcestershire sauce "
          "brings back the dark savoury note."),
    entry("swap-breadcrumbs-shortage", (("breadcrumbs", "bread crumbs", "breadcrumb", "no breadcrumbs"),
                               _SWAP_ASK),
          "Blitz stale bread, or crush crackers, cornflakes or oatcakes in a bag with a rolling "
          "pin. A crumble or a gratin topping takes porridge oats or crushed crisps, and for "
          "binding mince or meatballs a slice of bread soaked in a little milk is the classic."),
    entry("swap-mayonnaise-shortage", (("mayonnaise", "mayo", "no mayonnaise"), _SWAP_ASK),
          "Plain yoghurt or sour cream for a dip or a dressing, loosened with a spoon of water "
          "or lemon, and hummus, butter or mashed avocado in a sandwich. To make it from scratch: "
          "one egg yolk with a teaspoon of mustard, then 150ml of oil added drop by drop while "
          "you whisk, and a squeeze of lemon at the end."),
    _swap("swap-milk", (("milk",), _SWAP_ASK),
          "In cakes, scones and pancakes: water plus a knob of butter, or two tablespoons of milk "
          "powder stirred into the water. Any unsweetened plant milk works too. In a savoury sauce "
          "or mash, stock or the pasta water tastes better than plain water."),
    _swap("swap-yoghurt", (("yoghurt", "yogurt"), _SWAP_ASK),
          "In marinades and dressings: sour cream, creme fraiche or buttermilk. In baking: milk "
          "with a teaspoon of lemon juice, left 10 minutes. In a curry, stir any of them in off "
          "the heat, or they split into grains."),
    entry("swap-cornflour", (("cornflour", "corn starch", "cornstarch"), _SWAP_ASK),
          "Plain flour at twice the amount, whisked into cold liquid before it goes in, or "
          "arrowroot at the same amount. Simmer a minute afterwards, but do not boil a cornflour "
          "sauce hard, because it thins out again."),
    entry("swap-lemon", (("lemon", "lemons", "lime", "limes"), _SWAP_ASK),
          "For the juice: lime is the nearest, or white wine vinegar or cider vinegar at half the "
          "amount, or a splash of orange juice if the dish is sweet anyway. For the zest: lime or "
          "orange zest, or a few drops of lemon essence. Where the lemon is the whole point - "
          "lemon drizzle, hollandaise, a lemon tart - a bottle of juice does the job, and nothing "
          "else does."),
    entry("swap-wine", (("wine", "white wine", "red wine", "vermouth", "sherry", "marsala"),
                        _SWAP_ASK),
          "Leave the wine out and use the same amount of hot stock, plus a squeeze of lemon or a "
          "teaspoon of white wine vinegar so it still tastes bright. A splash of dry vermouth or "
          "dry sherry is the closest thing to the wine itself, so half wine and half stock is a "
          "good way back. In a risotto, add the stock a ladle at a time either way, and taste for "
          "salt at the end."),
    entry("swap-rice-shortage", (("rice", "basmati rice", "long grain rice"), _SHORTAGE_ASK),
          "No rice under a curry or a stew: pasta, couscous, bulgur or a baked potato do the same "
          "job, drained and buttered the same way, and a tin of chickpeas or a handful of extra "
          "vegetables fills the plate if there is less of any of them than you thought. Keep the "
          "portion the same - 75 to 100g dry a person. Risotto, paella and egg fried rice want "
          "rice itself, so cook something else instead of swapping them.",
          avoid=_STAPLE_METHOD_AVOID + (
                 "per person", "keep", "keeps", "freeze",
                 "reheat", "leftover", "leftovers", "risotto", "paella", "rice pudding",
                 "rice cooker", "brown rice", "white rice", "sushi rice", "cauliflower rice",
                 "rice bowl", "rice krispie", "rice balls", "carbs", "calories")),
    entry("swap-pasta-shortage", (("pasta", "spaghetti", "noodles", "macaroni"), _SHORTAGE_ASK),
          "No pasta: rice, potatoes or couscous under the same sauce, and a layer of sliced potato "
          "does the job of lasagne sheets in a bake. Keep the sauce as it was - it is the part "
          "that carries the meal - and the same weight of whatever you use, 75 to 100g dry a "
          "person.",
          avoid=_STAPLE_METHOD_AVOID + (
                 "per person", "keep", "keeps", "freeze",
                 "reheat", "leftover", "leftovers", "lasagne", "salad", "carbs",
                 "calories")),
    entry("swap-potatoes", (("potatoes", "potato", "spuds", "spud"), _SHORTAGE_ASK),
          "No potatoes: pasta, rice or couscous beside the same dinner, and if it is mash that is "
          "wanted, parsnip, celeriac or butter beans mash much the same once they are soft, with "
          "butter and a little of the cooking water. Roast potatoes really do want potatoes - "
          "nothing else crisps that way - so roast carrots, squash or onions instead.",
          avoid=_STAPLE_METHOD_AVOID + (
                 "per person", "keep", "keeps", "freeze",
                 "reheat", "leftover", "leftovers", "sweet potato", "mashed potato", "mash",
                 "potato salad", "potato gratin", "gratin", "wedges", "chips",
                 "jacket", "crisps", "dauphinoise", "carbs", "calories")),
    entry("swap-baking-powder", (("baking powder", "raising agent", "no baking powder",
                                  "without baking powder"), _SWAP_ASK + _OUT_ASK),
          "A teaspoon of baking powder is a quarter teaspoon of bicarbonate of soda plus half a "
          "teaspoon of cream of tartar. Without the cream of tartar, use the quarter teaspoon of "
          "bicarbonate and swap a spoonful of the liquid for lemon juice, vinegar or buttermilk, "
          "because bicarbonate needs an acid to work. Self-raising flour already carries it - "
          "about 2 teaspoons in every 150g - so a self-raising recipe needs none at all.",
          avoid=("difference", "different", "vs", "how much", "how many", "sourdough", "starter",
                 "soda bread", "bicarbonate of soda in")),
    entry("swap-plain-flour", (("plain flour", "all-purpose flour", "all purpose flour",
                                "no plain flour", "no flour left"),
                               _SWAP_ASK + _OUT_ASK),
          "Instead of plain flour, self-raising is the usual stand-in: use it at the same weight "
          "and leave out the baking powder the recipe asks for, or add a teaspoon less. Bread "
          "flour works in cakes and scones too but drinks more liquid, so add it a spoonful at a "
          "time. For thickening a sauce, cornflour at half the amount does the job better."),
    entry("swap-yeast", (("yeast", "no yeast"), _SWAP_ASK + _OUT_ASK),
          "Without yeast, bread needs a different kind of rise: a soda bread with bicarbonate of "
          "soda and buttermilk, or flatbreads and rotis, which need no rising at all. For a pizza "
          "or a focaccia today, half a teaspoon of bicarbonate and a teaspoon of lemon juice to "
          "300g of flour will puff it in a hot oven instead."),
    entry("vegan-baking", (("vegan", "vegans", "plant based", "plant-based", "eggless", "egg free",
                            "egg-free", "dairy free", "dairy-free"),
                           ("cake", "sponge", "biscuit", "biscuits", "cookie", "cookies", "scone",
                            "scones", "muffin", "muffins", "brownie", "brownies", "pancake",
                            "pancakes", "bake", "baking", "loaf", "bread", "flapjack",
                            "flapjacks", "blondie", "blondies", "oat bar", "oat bars", "pastry",
                            "shortcrust", "pie", "pie crust", "tart", "tarts", "tart case",
                            "quiche", "flan", "crumble", "crumbles", "brioche", "challah")),
          _vegan_bake,
          avoid=("healthy", "healthier", "healthily", "unhealthy", "calories", "fattening",
                 "good for you", "bad for you"),
          bias=1),
    entry("self-raising", (("plain flour", "all-purpose flour", "flour"), ("self-raising",
                                                                        "self raising",
                                                                        "substitute", "baking powder")),
          "To make self-raising flour, add 2 level teaspoons of baking powder to every 150g of "
          "plain flour, plus a pinch of salt. Mix it well before using it, or some bakes rise more "
          "than others."),

    entry("fix-sweet", (("sweet", "sugary", "too much sugar", "over sweet"),
                        _FOOD),
          "Balance it with salt and acid rather than more of anything sweet: a pinch of salt, a "
          "squeeze of lemon or a spoon of vinegar, and a little more of whatever the dish is built "
          "on - flour, cream, yoghurt, tinned tomatoes. For a cake that is already baked, serve it "
          "with unsweetened cream or fruit, and cut the sugar by a quarter next time: most recipes "
          "take it.",
          avoid=("potato", "potatoes", "wine", "cider", "beer", "perfume", "smell", "smells",
                 "voice", "music", "dream", "dreams", "tooth", "teeth", "sherry",
                 "sweet and sour", "sour and sweet"),
          bias=1),
    entry("fix-sour", (("sour", "acidic", "too much lemon", "too much vinegar", "vinegary",
                        "too sharp"),
                       _FOOD),
          "Take the edge off with fat and sweetness rather than more of anything sour: a knob of "
          "butter or a spoon of cream, a pinch of sugar, or a little bicarbonate of soda on the "
          "tip of a knife for a tomato sauce. If it is a stew or a curry, ten more minutes of "
          "simmering with the lid off softens the acid; if it is a salad dressing, add oil rather "
          "than more honey.",
          avoid=("milk", "cream", "yoghurt", "yogurt", "off", "gone off", "date", "wine", "cider",
                 "beer", "stomach", "breath", "mood",
                 "coffee tastes", "coffee taste", "coffee that tastes", "coffee is sour",
                 "espresso tastes", "espresso is sour", "tea tastes", "tea taste",
                 "tea that tastes", "tea is sour",
                 "mouth", "tongue", "sick", "vomit",
                 "sweet and sour", "sour and sweet",
                 "coffee tastes", "coffee taste", "coffee that tastes", "coffee is sour",
                 "coffee is bitter", "espresso tastes", "espresso is sour", "latte tastes",
                 "cup of coffee taste", "tea tastes", "tea is bitter", "tea taste"),
          bias=1),
    entry("chilli-heat", (("chilli", "chili", "curry", "spicy", "spice"),
                          ("too hot", "too spicy", "too much", "cool", "milk", "hot", "mild",
                           "less", "milder", "yoghurt")),
          "To cool a dish that's too hot, stir in yoghurt, cream or coconut milk at the end, or "
          "serve it with rice and something dairy on the side. Water doesn't help; a little sugar "
          "and lemon balances the heat without hiding it.",
          avoid=("made too much", "cooked too much", "make too much", "cook too much",
                 "made far too much", "left over", "leftover", "leftovers", "freeze",
                 "freezer")),
    entry("chilli-prep", (("chilli", "chillies", "chillis", "chili"),
                          ("deseed", "de-seed", "de seed", "seed", "seeds", "pith")),
          "Cut the chilli in half lengthways and scrape out the seeds and the white pith with a "
          "teaspoon or the tip of a knife: nearly all the heat sits there, so a chilli with them "
          "out is mild and the flesh left behind still tastes of chilli. Wash your hands straight "
          "after and keep them off your eyes; leave the seeds in when you want the heat.",
          avoid=("con carne", "recipe", "sauce", "soup", "stew", "curry", "dish", "dinner",
                 "too hot", "too spicy", "cool it down", "mild", "milder", "less hot",
                 "grow", "plant", "seedling", "seeds to sow", "sow", "dry", "drying",
                 "freeze", "store", "keep", "buy")),
    entry("curry-split", (("curry", "sauce", "gravy", "hollandaise", "mayonnaise", "mayo",
                           "bearnaise", "béarnaise", "custard", "custards", "creme anglaise",
                           "crème anglaise", "creme patissiere", "crème pâtissière",
                           "pastry cream", "custard tart", "custard tarts", "custard filling",
                           "creme caramel", "crème caramel"),
                          ("split", "splits", "splitting", "curdled", "curdle", "curdling", "grainy",
                           "seized")),
          _split,
          avoid=("burnt", "burn", "burnt on", "scorched", "caught")),
    entry("soup-thick", (("soup", "stew", "casserole", "stews", "casseroles", "curry",
                          "curries", "sauce"),
                         ("thicken", "thick", "thicker", "thickens", "thicken it",
                          "thickens it", "watery", "runny", "thin", "too thin", "too watery",
                          "make soup thicker", "make my soup thicker", "make a thicker soup",
                          "make it thicker", "thicker soup",
                          *MAKE_IT_THICK,
                          "thinner", "thin down", "thin it", "make it thinner",
                          "make my soup thinner", "soup thinner", "less thick",
                          "stodgy", "stodge", "claggy", "gluey")),
          _body,
          ),
    entry("gravy-lumpy", ("gravy", ("lumpy", "lump", "lumps", "thick", "thicker", "thin",
                                    "runny", "too thin", "thicken", "thickens", "make", "smooth",
                                    "sieve", "sieved")),
          "Whisk the flour into the meat juices off the heat before adding stock, then simmer it "
          "for 5 minutes. If it's already lumpy, pour it through a sieve and push the lumps "
          "through with a spoon. Too thin or runny, simmer it uncovered to reduce it, or knead "
          "equal butter and flour and whisk that in a little at a time."),

    entry("made-too-much",
          (("too much", "far too much", "way too much", "too many", "loads", "lots", "so much",
            "plenty left", "double the amount", "overcatered"),
           ("made", "make", "makes", "cooked", "cook", "left over", "left", "leftover",
            "leftovers", "food", "dinner", "tea", "lunch", "meal", "batch", "portion",
            "portions", "soup", "stew", "curry", "chilli", "bolognese", "mash", "rice", "pasta",
            "lasagne", "lasagna", "casserole", "pie", "cake", "bread", "chicken", "meat")),
          ("Get it cold fast and split it now: cool it within an hour, keep what you will eat in "
           "the next 3 days in the fridge and freeze the rest flat in bags or tubs. Mash keeps a "
           "month frozen and stew, curry, soup or bolognese three, and a cake or a loaf freezes "
           "well sliced, three months; rice is the one to be strict with - fridge it within the "
           "hour and eat it within a day. Reheat once, until piping hot right through, and next "
           "time cook 75 to 100g of dry pasta or 60g of rice a head."),
          guard=not_a_cup_of_tea,
          avoid=("cups of tea", "cups of coffee", "cup of tea", "cup of coffee", "mugs of tea",
                 "mug of tea", "caffeine", "coffees",
                 "how much tea", "how much green tea", "green tea", "herbal tea", "black tea",
                 "tea a day", "teas a day", "tea is too much", "too much tea is",
                 "is too much tea", "how much tea is", "much tea a day",
                 "tea every day", "cup of tea a day",
                 "drink", "drinking", "drank", "alcohol", "beer", "wine", "coffee", "tea bags",
                 "spend", "spending", "spent", "money", "pay", "paid", "afford", "budget",
                 "salt", "salty", "sugar", "spice", "spices", "spicy", "seasoning", "pepper",
                 "chilli powder", "hot sauce", "exercise", "training", "work", "overtime",
                 "sleep", "slept", "screen", "sun", "throw", "throwing", "thrown", "waste",
                 "wasting", "wasted", "bin", "binned", "left out", "leftover medicine",
                 "tablet", "tablets", "medicine", "medicines",
                 "bought", "buy", "buying", "shop", "shopping", "supermarket",
                 "what can i make", "what can i do with", "make with", "use up", "use them up",
                 "what can i cook", "what can i cook with", "can i cook with",
                 "freeze", "freezer", "frozen", "thaw", "thawing", "defrost", "reheat",
                 "reheating",
                 "make myself sick", "made myself sick", "making myself sick",
                 "make myself throw up", "made myself throw up", "making myself throw up",
                 "make myself vomit", "made myself vomit", "throw up after eating",
                 "threw up after eating", "sick after eating", "vomit after eating",
                 "vomiting after eating", "purge", "purged", "purging", "binge", "binged",
                 "bingeing", "binge eating", "bulimia", "bulimic", "anorexia", "anorexic",
                 "eating disorder", "starve myself", "starving myself", "not eating",
                 "guilt about eating", "feel guilty after eating")),
    entry("chicken-left-out", ("chicken", ("overnight", "left out", "sit out", "sitting out",
                                            "out of the fridge", "all night", "room temperature")),
          "Bin it, I'm afraid: cooked chicken left out for more than 2 hours isn't safe to eat, "
          "even if it looks and smells fine. Next time, get leftovers into the fridge within an "
          "hour and they'll keep 3 days."),
    entry("leftovers-keep", (("leftovers", "leftover", "cooked food", "cooked last night",
                              "cooked yesterday", "food cooked", "from last night",
                              "dinner last night", "tea last night", "supper last night"),
                             ("how long", "safe", "fridge", "keep", "days", "store", "storing",
                              "where", "shelf life", "shelf-life", "ok", "okay", "eat",
                              "eat it", "still good", "reheat")),
          "Cooked leftovers keep 3 to 4 days in the fridge if they went in within 2 hours of "
          "cooking. Reheat them until piping hot all the way through, once only, and bin anything "
          "you're unsure about.",
          avoid=("medicine", "medicines", "tablet", "tablets", "pill", "pills", "capsule",
                 "capsules", "antibiotic", "antibiotics", "prescription", "inhaler", "syringe",
                 "epipen", "painkiller", "painkillers", "antidepressant", "antidepressants",
                 "medication",
                 "rice", "pasta", "spaghetti", "noodles", "chicken", "turkey", "ham", "gammon",
                 "bacon", "sausage", "sausages", "salmon", "fish", "prawns", "pizza", "soup",
                 "stew", "curry", "potato", "potatoes", "tofu", "cream", "milk",
                 "paint", "paintbrush", "paintbrush", "emulsion", "gloss", "undercoat", "primer",
                 "varnish", "wood stain", "woodstain", "wallpaper", "tile adhesive", "grout",
                 "cement", "mortar", "filler", "sealant", "caulk", "silicone", "sandpaper",
                 "timber", "compost", "gravel", "screws", "tiles"),
          bias=4),
    entry("a-cooked-dish-with-no-row",
          (("couscous", "bulgur", "bulghur", "quinoa", "risotto", "paella", "biryani",
            "jambalaya", "gumbo", "cassoulet", "tagine", "goulash", "moussaka", "ratatouille",
            "falafel", "paneer", "polenta", "gnocchi", "dumplings", "stuffed peppers",
            "stuffed aubergine", "vegetable bake", "macaroni cheese", "mac and cheese",
            "cauliflower cheese"),
           KEEPING_WORDS),
          "That keeps 3 to 4 days in the fridge once it is cooked: cool it within two hours, get "
          "it covered into the fridge, and reheat it once, piping hot all the way through. "
          "Anything with rice or chicken in it is the one to be strict with, and what you will not "
          "eat in that time freezes well for 2 to 3 months.",
          avoid=NOT_A_KEEPING_ASK, guard=_not_a_cooking_time),
    entry("a-dip-or-a-herb-salad-keeps",
          (("guacamole", "tzatziki", "aioli", "taramasalata", "tabbouleh", "tabouleh",
            "raita", "salsa verde", "sour cream dip", "onion dip", "egg mayonnaise"),
           KEEPING_WORDS),
          "A day or two at most, and it is the avocado, the cucumber and the fresh herbs that turn "
          "first: keep it covered, pressed down so no air is on top, and in the coldest part of "
          "the fridge. Guacamole is at its best the day it is made, so make what you will eat.",
          avoid=NOT_A_KEEPING_ASK, guard=_not_a_cooking_time),
    entry("a-baked-fruit-pudding-keeps",
          (("crumble", "apple crumble", "rhubarb crumble", "fruit crumble", "cobbler",
            "fruit tart", "apple tart", "treacle tart", "lemon tart", "jam tart",
            "baked apple", "baked apples"),
           KEEPING_WORDS),
          "A crumble or a tart keeps 2 to 3 days in the fridge, covered: the topping goes soft "
          "before it goes off. Reheat it at 180C (160C fan) for 15 minutes to crisp the top again, "
          "and freeze it unbaked for 3 months, then bake it from frozen for 20 minutes longer.",
          avoid=NOT_A_KEEPING_ASK, guard=_not_a_cooking_time),
    entry("a-set-dessert-keeps",
          (("cheesecake", "tiramisu", "panna cotta", "chocolate mousse", "lemon mousse",
            "creme caramel", "flan", "posset", "mousse"),
           KEEPING_WORDS),
          "A set dessert like that keeps 2 to 3 days in the fridge, covered, and it is better on "
          "the second day than the first. A cheesecake is 3 to 4 days and freezes well in slices; "
          "a mousse or a posset is the shortest at 2 days, because it is mostly cream and egg.",
          avoid=NOT_A_KEEPING_ASK, guard=_not_a_cooking_time),
    entry("fridge-temp", ("fridge", ("temperature", "how cold", "setting", "dial", "cold",
                                     "too warm", "feels warm", "felt warm", "running warm",
                                     "not cold enough", "warm again")),
          "Your fridge should be between 0 and 5C, with the coldest shelf at the bottom; use a "
          "thermometer rather than the dial. Keeping it properly cold is the single easiest way to "
          "make food last longer.",
          avoid=("beer", "wine", "bottle", "opened")),
    entry("beer-keeping", ("beer", ("fridge", "keep", "last", "off", "flat", "opened",
                                   "how long")),
          "Unopened beer is best within three to six months in the fridge, and drinkable for a lot "
          "longer than that; an opened bottle goes flat within a day, so finish it fresh. Keep it "
          "upright and out of sunlight, which skunks the flavour faster than age does."),
    entry("wine-no-corkscrew", (("corkscrew", "no opener", "bottle opener"),
                                ("open", "no", "without", "dont", "don't", "havent", "haven't",
                                 "forgot", "lost", "missing", "wine")),
          "Drive a long screw into the middle of the cork, leave a few centimetres sticking out and "
          "lever it up a little at a time with a fork, pliers or the back of a key. In a pinch you "
          "can push the cork in with the handle of a wooden spoon, which is fine if you are "
          "drinking the bottle now. Warm the neck in your hands first if the cork is stubborn.",
          avoid=("stain", "carpet", "spill"),
          bias=1),
    entry("wine-bottle-open",
          (("wine", "bottle of red", "bottle of white", "red wine", "white wine", "rose wine",
            "prosecco", "champagne", "sparkling wine", "cava", "cork", "screw cap"),
           ("open", "opening", "uncork", "get it open", "crack it open", "pop the cork",
            "screw cap", "twist the cap", "twist off", "undo the cap", "how do i open")),
          _open_wine,
          avoid=("no corkscrew", "without a corkscrew", "without the corkscrew", "no opener",
                 "havent got a corkscrew", "haven't got a corkscrew", "dont have a corkscrew",
                 "don't have a corkscrew", "lost the corkscrew", "forgot the corkscrew",
                 "cork broke", "cork snapped", "cork in the bottle", "how long", "gone off",
                 "go off", "goes off", "still good", "still ok", "still fine",
                 "vinegar", "keep", "last", "fridge", "leftover", "left over", "already open",
                 "opened bottle", "open bottle", "stain", "carpet", "sauce", "recipe", "risotto",
                 "gravy", "mulled",
                 "leave it out", "leaving it out", "left out", "leave it", "out overnight",
                 "overnight", "in the fridge", "in the rack", "how many days"),
          bias=1),
    entry("broken-cork", (("cork", "corks", "stopper", "broken cork", "cork breaks",
                           "cork broke", "cork has broken", "cork snapped", "piece of cork",
                           "bits of cork"),
                          ("broke", "breaks", "broken", "snapped", "snapped off",
                           "fell in", "dropped in", "crumbled", "brittle",
                           "pushed in", "in the bottle", "in the neck", "stuck", "wedged",
                           "half", "crumbs", "out", "remove")),
          ("Push it in: a cork that has snapped or dropped into the bottle does no harm to a wine "
           "you are drinking tonight, and a clean cork floats. To get it out, pour the wine into a "
           "jug through a sieve, fish the cork out and pour it back. A cork stuck in the neck comes "
           "out on a long screw turned into it and pulled with pliers."),
          avoid=("board", "floors", "flooring", "tiles", "oak", "pinboard", "bulletin", "hat",
                 "recipe", "risotto")),
    entry("salad-a-meal",
          (("salad", "salads", "leaves", "salad leaves", "green salad", "side salad"),
           ("filling", "filling up", "more filling", "fill me up", "into a meal", "a meal",
            "plate of food", "substantial", "satisfying", "keep me full", "stays with me",
            "hungry", "proper meal")),
          "Leaves are the vegetable, not the meal: add a protein, something starchy and something "
          "rich, and dress it while the starch is still warm. Chickpeas or a boiled egg, new "
          "potatoes and feta is dinner; tinned tuna, leftover rice and a spoon of mayo is lunch. "
          "A plate rather than a side bowl is the portion that fills you, and salt it properly.",
          avoid=("dressing", "vinaigrette", "keep", "keeps", "keeping", "store", "stored", "last",
                 "lasts", "long", "wilt", "wilted", "limp", "soggy", "watery", "wet", "wash",
                 "washing", "bag", "buy", "supermarket", "calories", "healthy", "fruit",
                 "pasta", "potato", "coleslaw", "slaw", "caesar", "nicoise", "sandwich", "wrap",
                 "instead of", "substitute", "swap", "recipe")),
    entry("leftover-veg", (("vegetables", "veg", "mixed veg", "root vegetables", "greens"),
                           ("leftover", "left over", "leftovers", "leftovers", "spare", "use up",
                            "what do i do", "what can i do", "what should i do")),
          "Fry them into a hash: chop them small, start with an onion and a pinch of salt, and let "
          "them crisp at the edges before you add anything wet. Roasted vegetables are better "
          "through pasta with garlic and a spoonful of the cooking water, and anything soft goes "
          "into soup with stock and a blender.",
          avoid=("raw", "freeze", "frozen", "plant", "grow", "garden", "seeds", "soup", "roast",
                 "salad", "healthy", "portion", "five a day",
                 "use up", "to use", "before it goes off", "goes off", "before they go off",
                 "going off", "use it up")),
    entry("veg-keep", (("cabbage", "mushrooms", "carrots", "lettuce", "spinach", "broccoli",
                        "courgette", "courgettes", "peppers", "vegetables", "veg", "salad",
                        "parsnip", "parsnips", "swede", "swedes", "turnip", "turnips",
                        "sprout", "sprouts", "brussels sprouts", "brussel sprouts",
                        "cauliflower", "cauliflowers", "radish", "radishes", "kale", "chard",
                        "pak choi", "bok choy", "fennel", "celeriac", "kohlrabi",
                        "sweetcorn", "corn on the cob", "runner beans", "mangetout",
                        "sugar snap peas", "asparagus",
                        "tin of beans", "tin of chickpeas", "tinned beans", "tinned chickpeas",
                        "open tin", "opened tin", "tin once opened", "once opened"),
                       ("keep", "keeps", "last", "lasts", "still ok", "still good", "gone off",
                        "safe", "how long",
                        "store", "stores", "storing", "stored", "storage"),
                       ),
          "Most veg keeps about a week in the fridge drawer, and a bit longer than you'd think if "
          "it stays dry: keep it in a bag or box, and don't wash it until you use it. Cabbage, "
          "carrots and peppers go soft before they go off; mushrooms and salad are the ones that "
          "turn slimy, so use those first. Root veg - parsnips, swede, turnips, celeriac - is the "
          "longest of all, weeks in the fridge and months somewhere cool and dark, and sprouts and "
          "cauliflower are the quick ones: a bag with the air pressed out, and eat them inside a "
          "week before they yellow. An opened tin of beans or chickpeas keeps 3 days in a covered "
          "bowl in the fridge.",
          avoid=("make", "cook", "recipe", "dinner", "meal", "tonight", "freezer", "freeze",
                 "slug", "slugs", "snail", "snails", "pest", "pests", "bug", "bugs", "insect",
                 "insects", "caterpillar", "caterpillars", "aphid", "aphids", "blackfly",
                 "greenfly", "holes", "eaten", "eating",
                 "take", "takes", "took", "jar", "jars", "pesto", "ketchup", "mayonnaise",
                 "jam", "pickle", "chutney", "tuna", "fish", "meat", "chicken", "ham",
                 "bacon", "sausage", "mince",
                 "milk", "wine", "beer", "juice", "squash", "cream", "yoghurt", "yogurt",
                 "cheese", "butter",
                 "mushroom", "mushrooms", "carrot", "carrots", "potato", "potatoes", "onion",
                 "onions", "spring onion", "spring onions", "garlic", "apple", "apples",
                 "banana", "bananas", "lemon", "lemons", "berries", "tomato", "tomatoes",
                 "eggs", "egg", "bread", "rice", "pasta", "ginger", "herbs",
                 "opened tin of beans", "opened tin of chickpeas")
                + COOK_VERBS),
    entry("food-dates", (("use by", "best before", "sell by"), ("date", "mean", "safe", "difference")),
          "'Use by' is about safety: don't eat it after that date, and don't freeze it after it "
          "either. 'Best before' is about quality, so food is usually fine for a while after, using "
          "your eyes and nose."),
    entry("leftover-pasta", ("pasta", ("leftover", "left over", "yesterday", "spare")),
          "Cold pasta is best fried: toss it in a hot pan with oil, garlic and whatever vegetables "
          "you have, and add a splash of water or passata so it doesn't stick. Or bake it in a "
          "white sauce with cheese on top for 20 minutes at 200C."),
    entry("leftover-chicken",
          (("chicken", "chicken thigh", "chicken thighs", "chicken breast", "chicken breasts",
            "chicken drumstick", "chicken drumsticks",
            "cold chicken", "cold roast chicken", "cooked chicken"),
           ("left over", "left", "leftover", "spare", "half a", "already cooked",
            "cold")),
          "Half a roast chicken is two more meals: strip the meat off the carcass now, keep it in a "
          "covered tub in the fridge for up to 3 days, and use it cold in a salad, or hot in a pie, "
          "curry, risotto, soup or sandwiches. Reheat it once, until piping hot all the way through, "
          "and simmer the carcass "
          "with an onion for stock.",
          avoid=("safe", "safely", "how long", "bin", "smell", "smells", "sick", "pregnant", "dog",
                 "cat", "freezer", "freeze", "frozen", "left out", "overnight", "all night",
                 "hour", "hours", "on the counter", "on the side", "counter", "worktop",
                 "make", "recipe", "recipes", "ideas", "cook with",
                 "room temperature", "reheat", "reheated", "microwave", "warm up", "twice")),
    entry("chicken-salad", ("chicken", ("salad", "sandwich", "wrap", "mayonnaise")),
          "Shred or slice cooked chicken and mix it with mayonnaise, a squeeze of lemon, salt and "
          "pepper, then add crunch: celery, red onion, or apple and walnuts. It's better after 20 "
          "minutes in the fridge, and keeps 2 days.",
          bias=2, avoid=("keep", "keeps", "how long", "fridge", "last", "lasts", "still ok",
                         "still good", "gone off",
                         "protein", "carbs", "carbohydrates", "calories", "calorie", "cals",
                         "kcal", "fat", "sugar", "fibre", "fiber", "nutrition", "nutrients",
                         "how much protein", "how many calories", "how many carbs",
                         "another sandwich", "isnt another", "isn't another", "not another",
                         "left over", "leftover", "leftovers", "use up", "what can i do with")),
          entry("cake-sink", (_NO_LOAF_RISE + ("souffle", "soufflé"),
                        ("sink", "sank", "sunk", "collapsed", "collapse", "sunken", "flat",
                         "dropped",
                         "fell", "fallen", "falls", "rose and fell", "risen and fallen",
                         "rose then fell", "went down", "came down",
                         "sinking", "keeps sinking", "keeps collapsing", "always sinks",
                         "sinks every time", "sank again")),
          "A cake sinks when it's underbaked, when the oven door was opened early, or when there's "
          "too much raising agent; all three make it rise fast and then drop. Bake it at 180C "
          "(160C fan) without opening the door for the first 20 minutes, and check with a skewer.",
          avoid=("taste", "tastes", "tasted", "tasting", "bland", "dull", "season", "seasoning",
                 "bread", "dough", "prove", "proved", "proving", "proof", "yeast", "sourdough",
                 "knead", "kneading", "scone", "scones", "yorkshire", "yorkshires",
                 "brownie", "brownies") + _BAKE_KEEPING_SHAPED,
          bias=2),
    entry("scone-spread",
          (("scone", "scones", "soda bread", "soda farl", "soda farls"),
           ("spread", "spreads", "spreading", "spread out", "spread flat", "flat", "wide",
            "melted", "run together", "ran together", "lost their shape", "lost its shape")),
          "Scones spread when the dough is too wet or the butter warmed up: it wants to be a soft, "
          "shaggy dough you pat out rather than roll, and the butter cold and cut in small. Handle "
          "it as little as possible, pat it to about 3cm thick, and cut straight down with a floured "
          "cutter without twisting it, because a twist seals the edges and stops the rise. A dough "
          "that is too wet also spreads before the middle sets, so add flour a spoonful at a time "
          "until it just stops sticking to the bowl.",
          bias=1),
    entry("cake-rise", (("cake", "cakes", "sponge", "sponges"),
                        ("rise", "rises", "rising", "risen", "raise", "raised", "raising",
                         "taller", "fluffy", "light")),
          "A cake rises on three things - the air you beat in, the bubbles the raising agent "
          "makes, and steam - and when it does not, the culprit is nearly always baking powder past "
          "its date (a teaspoon per 150g of plain flour, or use self-raising), the flour beaten in "
          "too hard once it went in, or the oven door opened in the first 20 minutes. Cream the "
          "butter and sugar until pale and fluffy, fold the flour in with a spoon, fill the tin "
          "two-thirds full, and bake at 180C (160C fan) without opening the door.",
          avoid=("what makes", "makes a cake", "make a cake", "make my cake", "recipe", "recipes",
                 "sunken", "sank", "sunk", "sinking", "collapsed", "bread", "sourdough", "yeast",
                 "breadmaker", "taste", "tastes", "flat", "biscuit", "biscuits"),
          bias=1),

    entry("milk", ("milk", ("sour", "off", "smell", "smells off", "smelt off", "smells sour",
                            "smells funny", "smells wrong", "in my fridge", "in the fridge",
                            "in our fridge", "keep", "how long", "date", "opened",
                            "ok", "still ok", "safe", "still good", "past it", "gone off",
                            "shelf life", "shelf-life")
                          + DAY_WORDS
                          + STORE_ASKS
                          + ("breast milk", "breastmilk", "expressed milk", "formula milk")),
          _milk_keep,
          avoid=("tooth", "teeth", "milk tooth", "milk teeth", "baby tooth", "baby teeth",
                 "tooth fairy", "fell out", "wobbly", "loose tooth",
                 "not cold", "isnt cold", "isn't cold", "broken", "warm", "noisy", "buzzing",
                 "freezer", "fridge door",
                 "smells of milk", "smells like milk", "smell of milk", "smells of cream",
                 "smells of yoghurt",
                 "pregnant", "pregnancy", "expecting", "miscarriage", "trimester",
                 "drying up", "supply", "enough milk", "low supply", "milk supply")),
    entry("oil-smoking",
          (("pan", "pans", "oil", "oils", "butter", "fat", "grease", "greases", "greasy",
            "wok", "lard", "ghee", "dripping",
            "margarine", "olive oil", "rapeseed", "sunflower", "vegetable oil", "frying pan",
            "skillet", "deep fat fryer", "fry", "fries", "frying", "fryer", "deep fry",
            "deep frying", "fry up", "chip pan", "chips"),
           ("smoking", "smokes", "smoke", "smoked", "smoky", "burnt", "burning", "too hot",
            "overheating", "smoke point", "smokes when", "reuse", "re-use", "reusing",
            "used oil", "old oil", "used cooking oil", "old frying oil", "used frying oil",
            "still good", "still use", "can i use it", "can i use it again", "can i use this oil",
            "can i use that oil", "can i use the oil", "can i use the oil again",
            "can i use this fat", "can i use that fat", "can i use it once more",
            "how hot", "hot enough", "temperature", "foam", "foams", "foamy", "foaming",
            "bubbling",
            "is hot", "is ready", "pan heat", "the heat", "test the heat", "check the heat",
            "hot oil", "oil is hot", "oil is ready", "fat is hot", "fat is ready",
            "heat the pan", "heating the pan", "heat the oil", "heating the oil",
            "put the oil in", "put in the oil", "add the oil", "adding the oil", "oil go in",
            "oil goes in", "pan first", "oil in the pan", "oil in a pan", "hot pan first",
            "pan be hot", "hot before", "before the oil", "before adding the oil",
            "pan hot before", "when do i add the oil",
            "throw out", "throw away", "get rid", "getting rid", "dispose", "disposal", "bin it",
            "recycle", "recycling", "down the sink", "what to do with", "where do i put",
            "where do i pour",
            "down the toilet", "down the loo", "down the drain", "down the plug hole",
            "down the plughole")),
          _oil_smoking,
          avoid=("healthiest", "healthy", "unhealthy", "unsaturated", "saturated", "cholesterol",
                 "calories", "burnt on", "scrub", "clean", "cleaning", "give up",
                 "belly fat", "body fat", "stomach fat", "tummy fat", "thigh fat", "leg fat",
                 "arm fat", "bingo wings", "love handles", "muffin top", "fat around",
                 "fat on my", "lose fat", "losing fat", "lost fat", "burn fat", "burning fat",
                 "burns fat", "burn belly", "fat loss", "fat burning", "spot reduce", "get abs",
                 "flat stomach", "tone my", "toning my", "loose weight",
                 "burnt food", "burnt bits", "stuck to", "bottom of my pan", "bottom of the pan",
                 "bicarbonate", "soak", "pan is burnt", "frying pan is burnt",
                 "stuck on", "stuck on it", "stuck on the pan", "stuck on the bottom",
                 "burnt stuff", "stuff stuck", "burnt pan", "burned pan", "scorched pan",
                 "rescue the pan", "rescue a burnt", "save the pan", "pan is ruined",
                 "burnt layer",
                 "smell", "smells", "smelling", "smelly", "odour", "odor", "stink", "stinks",
                 "freezer", "freeze", "freezing", "frozen", "fridge", "refrigerator",
                 "warped", "warp", "warping", "warped pan", "wont sit flat", "doesnt sit flat",
                 "doesn't sit flat", "bowed", "spins", "rocks",
                 "put a hot pan", "put the hot pan", "stand a hot pan", "stand the hot pan",
                 "set a hot pan", "set the hot pan", "hot pan on", "hot pan down",
                 "instead of", "in place of", "substitute", "substituting", "swap", "swapping",
                 "replace", "replacing", "alternative to",
                 "room temperature", "soften", "softened", "baking", "cake", "bake", "roast",
                 "instead of", "in place of", "substitute", "swap", "stand in for",
                 "alternative to",
                 "what can i use", "can i use instead", "what do i use", "use instead",
                 "instead of butter", "instead of margarine", "in place of butter",
                 "in place of margarine", "substitute for butter", "substitute for margarine",
                 "instead", "instead of", "in place of", "substitute", "alternative",
                 "no butter", "no margarine", "no lard", "no dripping", "no ghee",
                 "run out of butter", "ran out of butter", "out of butter", "out of margarine",
                 "none left", "havent got any butter", "haven't got any butter",
                 "im out of butter", "i'm out of butter",
                 "store", "stored", "storing", "storage", "cupboard", "shelf", "pantry", "larder",
                 "keep used", "keeps used", "keeping used", "kept used",
                 "where do i keep", "where can i keep", "where to keep",
                 "keep old", "keeps old", "keeping old", "kept old", "how long", "last", "lasts",
                 "engine", "engines", "car", "cars", "motor", "motorbike", "motorcycle",
                 "lawnmower", "mower", "gearbox", "gear oil", "hydraulic", "diesel", "petrol",
                 "two stroke", "2 stroke", "sump", "oil change", "garage",
                 "quit", "cigarette", "cigarettes", "vape", "fag", "fags", "i smoke",
                 "stop smoking", "stopped smoking", "electric", "cooker", "oven", "barbecue",
                 "bbq", "fire alarm", "chimney",
                 "non stick", "non-stick", "nonstick", "teflon", "coating", "coated",
                 "scratched", "scratches", "scratch", "flaking", "peeling",
                 "mug", "mugs", "plate", "plates", "cup", "cups", "saucer", "saucers", "bowl",
                 "bowls", "glass", "glasses", "tumbler", "tumblers", "teapot", "jug", "dish",
                 "dishes", "crockery", "cutlery", "worktop", "tile", "tiles",
                 "face", "faces", "forehead", "nose", "chin", "cheeks", "cheek", "skin",
                 "t-zone", "t zone", "scalp", "hair", "hands", "hand", "thighs", "elbow",
                 "elbows", "shoulders", "neck", "shine", "shines", "shiny", "sheen", "gleam",
                 "glow", "oily", "spot", "spots", "pores",
                 "blocked", "blocked up", "blockage", "blocking", "slow draining", "drains slowly",
                 "worn out"),
          ask=("my", "the", "is", "why", "what", "how", "should", "does", "do", "i", "a", "it",
               "keep", "keeps", "when", "cant", "started", "starts"),
          bias=5),
    entry("frying-oil", ("oil", ("healthiest", "healthy", "best", "cook", "frying")),
          "Olive oil or rapeseed oil is a good everyday choice: both are high in unsaturated fat "
          "and fine for normal frying. Save the extra virgin olive oil for salads and low heat, "
          "and use a plain vegetable oil when you need a very hot pan."),
    entry("chip-pan-fat",
          (("oil", "fat", "lard", "dripping", "sunflower oil", "vegetable oil", "rapeseed oil",
            "groundnut oil", "frying oil", "chip pan", "fryer", "deep fat fryer",
            "deep-fat fryer"),
           ("chips", "chip pan", "chip pans", "fryer", "fryers", "deep fat fryer",
            "deep-fat fryer", "fries", "french fries", "wedges", "doughnuts", "donuts",
            "batter", "scampi", "onion rings", "fried chicken", "tempura",
            "deep frying", "deep fry", "deep fried", "deep-fried")),
          ("For a chip pan or a fryer, fill it no more than a third full and never past half - "
           "hot fat rises when the food goes in, and a pan that is too full is the way people "
           "get burned. 180C is the temperature for chips: a cube of bread browns in about 30 "
           "seconds. Fry in small batches so the fat does not drop, stand back as the chips go "
           "in, and never leave the pan."),
          avoid=("smoking", "smokes", "smoke", "smoked", "burnt", "burning", "on fire",
                 "caught fire", "healthiest", "healthy", "unsaturated", "saturated",
                 "cholesterol", "calories", "price", "cost", "buy", "best pan", "which pan",
                 "motor", "car", "engine", "van",
                 "air fryer", "air-fryer", "airfryer", "cheapest", "which oil",
                 "what oil", "best oil", "kind of oil", "type of oil", "which fat"),
          bias=2),
    entry("cheese-store", ("cheese", ("store", "keep", "fridge", "mould", "mouldy", "mold", "moldy",
                                      "wrap", "gone off", "date", "dates", "out of date",
                                      "off", "smell", "smells", "smelt", "smells like",
                                      "slimy", "ammonia", "ammonia smell", "still ok",
                                      "blue", "blue spot", "blue spots", "gone blue",
                                      "going blue", "turning blue", "blue mould", "green",
                                      "is it ok", "ok to eat", "safe to eat", "gone slimy",
                                      "put", "where do i put", "cling film", "clingfilm",
                                      "storing", "stored", "keep it")),
          _cheese_keep, guard=_not_a_serving_frame),
    entry("kids-tea", (("kids", "children", "child", "son", "sons", "daughter", "daughters",
                        "boy", "boys", "girl", "girls"),
                       ("tea", "dinner", "supper", "meal", "food", "eat", "eats", "eating",
                        "feed", "feeds", "feeding", "fed")),
          "Keep it plain and fast: fish fingers or chicken strips with peas and oven chips, pasta "
          "with grated cheese and sweetcorn, or a cheese omelette with toast. Put something green "
          "on the plate and don't make a second dinner if they refuse it.",
          bias=1,
          guard=_no_named_food,
          avoid=("picnic", "party", "birthday", "guests", "take", "bring", "school", "packed",
                 "nuts", "nut", "peanut", "peanuts", "peanut butter", "honey", "grape", "grapes",
                 "berry", "berries", "strawberry", "strawberries", "egg", "eggs", "shellfish",
                 "choking", "sesame", "soya", "soy",
                 "breakfast", "cereal", "toast",
                 "milk", "goats milk", "goat milk", "formula", "bottle",
                 "wont eat her", "wont eat his", "wont eat their", "wont eat the", "wont eat it",
                 "won't eat her", "won't eat his", "won't eat their", "wont eat anything",
                 "wont eat at all", "will not eat it", "will not eat her", "will not eat his",
                 "not eating", "isnt eating", "isn't eating", "stopped eating",
                 "refuses to eat", "refusing to eat", "refusing food", "wont touch her food",
                 "wont touch his food", "off her food", "off his food", "off their food",
                 "gone off her food", "gone off his food", "gone off their food",
                 "fussy", "picky", "gagging", "choking", "swallowing")),
    entry("pancake-batch", (("pancake", "pancakes"),
                            ("how many", "how much", "for four", "for 4", "for six", "for 6",
                             "for eight", "for 8", "per person", "people")),
          _pancake_batch,
          avoid=STORAGE + ("how do i make", "how to make", "recipe", "method", "how do i cook")),
    entry("lasagne-time", (("lasagne", "lasagna", "macaroni cheese", "shepherds pie",
                            "cottage pie"),
                           ("how long", "oven", "time", "temperature", "day before", "ahead",
                            "assemble", "prepare", "morning", "cook")),
          "Bake a lasagne at 190C (170C fan) for 35 to 40 minutes, until it bubbles at the edges. "
          "Made ahead, cover it and keep it in the fridge. Cook it from cold with foil over the "
          "top for the first 25 minutes, and give it 15 minutes extra so the middle is hot.",
          bias=1, avoid=STORAGE),
    entry("turkey-buy", (("turkey", "goose"),
                         ("buy", "when", "christmas", "order", "days", "defrost", "thaw")),
          "Order a fresh turkey to collect on the 23rd or the morning of the 24th, and a frozen one "
          "to come out of the freezer 3 to 4 days before for a big bird. Allow 20 minutes per 500g "
          "plus 20 at 180C (160C fan), and rest it 30 minutes under foil and tea towels.",
          avoid=("keep", "keeps", "keeping", "fridge", "last", "lasts", "left out", "left after",
                 "left from", "left over", "use by", "gone off", "still ok", "safe")),
    entry("leftover-turkey",
          ("turkey", ("left over", "left", "leftover", "leftovers", "spare", "half a",
                      "already cooked", "cold", "from christmas", "after christmas")),
          "Shred or slice the cold turkey: it is the best part of the bird, and it goes into "
          "sandwiches, a salad with mayonnaise and lemon, a curry, risotto or soup for the last two "
          "minutes, or a pie under pastry. Keep it in a covered tub in the fridge for up to 3 days, "
          "reheat it once until piping hot all the way through, and simmer the stripped carcass "
          "with an onion and a carrot for 30 minutes to make stock.",
          avoid=("safe", "safely", "how long", "bin", "smell", "smells", "sick", "pregnant", "dog",
                 "cat", "freezer", "freeze", "frozen", "left out", "overnight", "all night",
                 "hour", "hours", "on the counter", "on the side", "counter", "worktop",
                 "room temperature", "reheat", "reheated", "microwave", "warm up", "twice",
                 "buy", "order", "defrost", "thaw", "weight", "size", "per person", "roast",
                 "oven", "temperature", "when should i",
                 "make", "recipe", "recipes", "ideas", "cook with")),
    entry("turkey-size", (("turkey", "goose"),
                          ("how big", "size", "much", "many", "per person", "people", "for 4",
                           "for four", "for 6", "for six", "for 8", "for eight", "for 10",
                           "for ten")),
          "Allow about 500g of turkey per person, a bit more if you want leftovers: 4kg feeds 8 "
          "comfortably, 5kg feeds 10. Check the label for the weight once it is stuffed, and buy "
          "the bird rather than a crown if you want the legs for a curry afterwards.",
          avoid=STORAGE + ("cash", "money", "currency", "spending", "spending money", "abroad",
                           "holiday", "lira", "hotel", "flight")),
    entry("banana-bread", ("banana", ("bake", "bread", "cake", "brown", "overripe", "use up",
                                      "recipe", "make")),
          "Brown bananas are perfect for banana bread: mash 3 of them with 100g melted butter, 150g "
          "sugar, 2 eggs and 200g self-raising flour, and bake at 180C (160C fan) for about an hour. "
          "It keeps 4 days in a tin and freezes well.",
          bias=1,
          avoid=KEEPING + ("why", "slow", "slower", "faster", "stop", "last longer", "keep them",
                           "keeps them", "before i can", "ripen", "ripens", "ripening", "black",
                           "overripe", "over ripe", "too ripe", "mushy", "gone off", "left over",
                           "pancake", "pancakes", "pancake batter", "crepe", "crepes",
                           "flapjack", "waffle", "waffles",
                           "plant", "plants", "tree", "palm", "leaves", "leaf", "soil", "grow",
                           "growing", "houseplant", "potted") + NO_SUGAR),
    entry("party-food", (("party", "buffet", "picnic", "birthday"),
                         ("food", "snack", "nibbles", "ideas", "make", "cook", "menu", "take",
                          "bring", "feed", "kids")),
          "Cheap food that people finish and that travels: a big bowl of pasta salad, sausage "
          "rolls or sausages on sticks, cheese and crackers, and a tray of fairy cakes. Keep it to "
          "things you can make the day before, and buy the paper plates.",
          avoid=("game", "games", "play", "playing", "activities", "activity", "entertain",
                 "entertainment", "pass the parcel", "musical chairs", "treasure hunt", "prize",
                 "prizes", "bored", "keep them busy") + _ON_A_FLIGHT,
          guard=_not_a_trip),
    entry("coffee-less", ("coffee", ("less", "afternoon", "instead", "alternative", "replace",
                                     "cut", "too much", "drink less")),
          "Try a strong decaf, or a rooibos or barley-cup drink if you want the ritual without the "
          "caffeine. Green tea or a sparkling water with lemon work too; the slump at 3pm is often "
          "dehydration and a walk as much as coffee.",
          avoid=("bitter", "sour", "taste", "tastes", "tasting", "burnt", "grind", "grinder",
                 "water", "brew", "brewing", "beans", "strength", "strong",
                 "how much", "limit", "milligrams")),

    entry("coffee-grounds",
          (("coffee grounds", "used coffee grounds", "spent coffee", "leftover coffee grounds",
            "coffee grouts"),
           ("what can i", "make", "use", "do with", "compost", "garden", "plants", "fridge",
            "smell", "smells", "smelly", "scrub", "clean", "sink", "drain", "bin", "good for",
            "keep")),
          "Put them to work rather than down the sink: a handful of used grounds goes in the "
          "compost or round plants that like a little acid - blueberries, camellias, hydrangeas - "
          "and a small dish of dry ones in the fridge takes up smells for a couple of days. They "
          "also make a gritty paste for a stained sink or a scorched pan, and a weak brew poured "
          "over the garden is fine once it is cold. Keep them out of the drain, where they set "
          "like cement, and off seedlings in a thick layer, which stops water getting through.",
          bias=1),
    entry("coffee-bitter", (("coffee", "espresso", "americano", "cafetiere", "french press",
                             "instant coffee"),
                            ("bitter", "sour", "burnt", "burning", "awful", "horrible", "nasty",
                             "tastes bad", "taste bad", "grind", "brewing")),
          _coffee_fault,
          bias=1,
          avoid=("caffeine", "decaf", "cut down", "less coffee", "quit", "give up", "sleep",
                 "pregnant", "blood pressure", "heart", "anxious", "jitters")),
    entry("tea-brew", (("tea", "green tea", "teabag", "teabags", "tea bag", "tea bags",
                        "brew", "brews", "brewing", "cuppa", "cuppas", "pot of tea", "flask",
                        "thermos"),
                       ("bitter", "sour", "stewed", "brew", "how long",
                        "make", "taste", "tastes", "steep", "weak",
                        "strong", "stronger", "watery", "temperature",
                        "pot", "teapot", "iced", "ice", "cloudy", "scum", "film",
                        "proper", "decent", "method", "perfect", "lovely",
                        "can i have", "can i get", "could i have", "could i get", "may i have",
                        "i want a", "i'd like", "id like", "ill have", "i'll have",
                        "how do you like")),
          _tea_reply,
          ask=("brew", "brewing", "steep", "steeped", "bitter", "sour", "stewed", "taste",
               "tastes", "weak", "strong", "stronger", "watery", "green tea", "black tea",
               "make tea", "tea bag", "tea bags", "teabag", "teabags", "cup", "mug", "kettle",
               "milk", "sugar", "temperature",
               "pot of tea", "teapot", "teapots", "iced tea", "ice", "cloudy", "cup of tea",
               "mug of tea", "hot water", "proper cup", "decent cup",
               "cuppa", "cuppas", "flask", "thermos",
               "can i have", "can i get", "could i have", "could i get", "may i have",
               "i want a", "i'd like", "id like", "ill have", "i'll have", "how do you like",
               "infuse", "infusing", "infused", "loose leaf", "loose leaves", "leaf tea"),
          bias=1,
          avoid=("coffee", "coffees", "espresso", "cafe", "beer", "ale", "lager", "stout",
                 "wine", "cider", "mead", "kombucha", "homebrew", "home brew")),

    entry("tea-milk",
          (("milk first", "milk in first", "milk last", "milk in last", "milk go in",
            "milk goes in", "milk in before", "milk then", "milk or tea", "tea or milk",
            "milk in a cup of tea", "milk in a mug of tea", "milk in tea", "milk in my tea",
            "milk for tea", "milk with tea", "milk for a cup of tea", "milk in a brew",
            "milk", "oat milk", "soy milk", "soya milk", "almond milk", "plant milk",
            "skimmed milk", "semi skimmed milk", "whole milk", "milk in my brew"),
           ("first", "last", "before", "after", "order", "tea", "cup of tea", "mug of tea",
            "brew", "cuppa", "stir")),
          _tea_milk_reply,
          ask=TEA_MILK_ASK,
          avoid=("coffee", "porridge", "cereal", "mash", "potato", "potatoes", "sauce",
                 "recipe", "cake", "scone", "scones", "bread", "rice pudding", "custard",
                 "baby", "babies", "newborn", "formula", "breast", "breastfeeding", "bottle",
                 "latte", "cappuccino", "flat white", "milkshake", "smoothie", "allergy",
                 "allergic", "intolerance", "lactose", "calcium", "calories", "calorie",
                 "caffeine", "protein", "pregnant", "curdl", "split", "freeze", "frozen",
                 "gone off", "off", "use by", "cloudy", "cloudiness", "scum", "film",
                 "murky",
                 ) + _TEA_MILK_DISH,
          bias=1),

    entry("milk-for-coffee",
          (("milk",), ("coffee", "coffees", "latte", "lattes", "cappuccino", "flat white",
                       "espresso", "americano", "mocha", "macchiato")),
          _the_milk_for_a_coffee,
          ask=("which", "what", "best", "good", "better", "ok", "should i", "can i", "could i",
               "do i", "does", "is", "are", "worth", "instead of", "rather than", "goes in",
               "go in", "use", "put in", "oat milk", "soy milk", "soya milk", "almond milk",
               "plant milk", "skimmed", "semi skimmed", "whole milk", "barista", "taste",
               "tastes", "split", "curdle", "froth", "foam"),
          avoid=("too much", "fast", "fasting", "calorie", "calories",
                 "caffeine", "pregnant", "pregnancy", "breastfeeding", "sleep", "anxiety",
                 "blood pressure", "stain", "stains", "machine", "beans", "bag", "buy", "buying",
                 "price", "cost", "costs", "shop", "cafe", "healthy", "good for you",
                 "bad for you", "before bed", "decorate", "art", "paint", "tables", "table",
                 "book", "books", "shop", "grinder", "descale", "clean"),
          bias=1),

    entry("tea-water-mug",
          (("kettle",),
           ("how much water", "much water", "how full", "how far to fill", "fill the kettle",
            "filling the kettle", "cups of water", "how much to fill", "full to fill")),
          "About 250ml a mug and a splash more for what boils off, so roughly 600ml for two mugs - "
          "fill one mug and tip it in twice, then a little extra. Only boiling what you need is "
          "the quickest saving in the kitchen and it scales the kettle up more slowly, but don't "
          "go under the element's minimum or the kettle will click off before it boils.",
          avoid=("descale", "limescale", "scale", "clean", "vinegar", "citric", "broken",
                 "repair", "boil dry", "element", "filter", "hard water", "calorie", "calories",
                 "caffeine", "sugar", "milk", "too many", "how many", "strong", "how long",
                 "cost", "costs", "price", "electricity", "energy", "buy", "buying", "best",
                 "which kettle", "plastic", "taste", "tastes", "tasting", "slow", "leak", "leaks",
                 "switch", "switching", "switches"),
          bias=1),

    entry("coffee-at-home",
          (("flat white", "latte", "lattes", "cappuccino", "cappuccinos", "macchiato", "mocha",
            "americano", "espresso", "steam milk", "steaming milk", "milk for coffee",
            "coffee milk", "milk frother", "steam wand", "milk steamer"),
           ("how do i make", "how to make", "how do you make", "make a", "make one", "make it",
            "how do i froth", "froth", "frothing", "how do i steam", "steam", "steaming",
            "at home", "the milk", "my milk", "properly", "like a cafe", "like a coffee shop",
            "no machine", "without a machine", "machine")),
          _a_coffee,
          avoid=("froth milk", "froth the milk", "frothy milk", "milk froth", "frothed milk",
                 "frothing milk", "best for frothing",
                 "caffeine", "how much", "too much", "how many", "before bed", "sleep",
                 "pregnant", "pregnancy", "breastfeeding", "heart", "blood pressure", "anxiety",
                 "calories", "calorie", "healthy", "healthier", "bad for", "good for",
                 "cost", "costs", "price", "buy", "buying", "best", "which", "recommend",
                 "decaf", "instant", "beans", "ground", "grinder", "pod", "pods",
                 "nespresso", "clean", "cleaning", "descale", "shop", "cafe",
                 "barista", "job", "stain", "stains", "white t shirt", "shirt"),
          bias=1),
    entry("kitchen-knives", (("knife", "knives", "blade", "honing steel", "sharpening steel"),
                             ("sharp", "sharpen", "sharpening", "blunt", "dull", "steel", "hone",
                              "honing", "properly", "the right way")),
          ("Ten strokes a side on a steel brings a blunt edge back for a week; a whetstone, coarse "
           "side then fine, once a month is what actually sharpens it. Hold the blade at 20 "
           "degrees, keep the fingers of your other hand behind the edge, and wash and dry it by "
           "hand: a dishwasher blunts a knife and splits a wooden handle."),
          bias=1),
    entry("rusty-kitchen-gear",
          (("rust", "rusty", "rusting", "rusted", "rusts"),
           ("baking tray", "baking trays", "tray", "trays", "tin", "tins", "cake tin",
            "muffin tin", "loaf tin", "tart tin", "bun tin", "roasting tin", "sheet pan",
            "bakeware", "springform", "knife", "knives", "blade", "cutlery", "fork", "forks",
            "spoon", "spoons", "whisk", "sieve", "grater", "pan", "pans", "wok",
            "tin opener", "can opener", "kitchen knife", "kitchen knives",
            "kitchen scissors", "kitchen tongs", "utensil", "utensils")),
          ("Scrub the rust off with a paste of bicarbonate of soda and water or a green scouring "
           "pad, rinse it and dry it at once. A little rust is not poisonous, but a tray that has "
           "rusted through will keep flaking into food: scrub it, rub a film of oil over it and "
           "bake it at 200C for 15 minutes to seal it again, and replace it once the metal is "
           "pitted. Knives, forks and tins rust because they sit wet, so wash and dry them by "
           "hand and never leave them in the sink or put them through the dishwasher."),
          bias=1),
    entry("board-smell", (("chopping board", "board", "worktop", "wooden spoon", "wooden spoons",
                           "spoon", "spoons", "utensils"), ("smell", "smells", "smelly",
                                                                   "onion", "garlic", "fish",
                                                                   "clean", "stain")),
          ("Scrub it with half a lemon and a big pinch of salt, rinse in the hottest water you "
           "have and dry it standing up: that lifts onion, garlic and fish out of wood or "
           "plastic. Plastic boards can go through the dishwasher, wooden ones should never."),
          avoid=("skirting", "skirting board", "skirting boards", "floorboard", "floorboards",
                 "ironing board", "whiteboard", "notice board")),
    entry("fish-smell", (("fish", "fishy", "cooking smell"), ("smell", "smells", "smelly", "stink",
                                                              "get rid", "kitchen", "house")),
          ("Boil a pan of water with a few slices of lemon or a splash of vinegar for 10 minutes "
           "with the window open: that is what clears cooking smells out of the air. Wash the pan, "
           "the board and the bin straight away, and leave a bowl of bicarbonate of soda in the "
           "fridge overnight if the smell got in there."),
          avoid=("tank", "fish tank", "aquarium", "goldfish", "pond", "ponds", "fish bowl",
                 "tropical fish", "pet fish")),
    entry("fish-tastes-fishy",
          (("fish", "fishes", "cod", "salmon", "mackerel", "haddock", "tuna", "prawns", "prawn",
            "trout", "herring", "sardines", "sprats"),
           ("tastes", "taste", "tasting", "tasted", "fishy", "tastes fishy", "too fishy",
            "smells fishy", "strong", "strongly", "muddy", "bitter")),
          ("Judge it by the smell first, not the taste: fish that is off has an ammonia or "
           "bleach-sharp smell, dull sunken eyes and flesh that stays dented when you press it, "
           "and that goes in the bin rather than on a plate. A fish that is fresh but tastes or "
           "smells strongly of the sea is usually an oily one - mackerel, herring, sardines, "
           "salmon - and soaking it in milk for 20 minutes, or rubbing it with lemon, takes the "
           "edge off. Cook it with acid and something sharp: lemon, vinegar, capers, dill, "
           "tomatoes. Frozen fish tastes stronger than fresh, so use it in a sauce or a pie "
           "rather than on its own."),
          avoid=("tank", "aquarium", "goldfish", "pet", "bowl", "pond", "kitchen smells",
                 "house smells", "get rid of", "cooking smell", "smell in", "gone off",
                 "still ok", "use by", "shelf life", "mouldy")),
    entry("bread-stale", (("bread", "loaf", "baguette", "rolls"),
                          ("stale", "dry", "hard", "yesterday", "keep fresh", "stop it going",
                           "going stale", "revive", "soft again"),
                          ("is it ok", "is it still", "ok to eat", "okay to eat", "can i eat",
                           "can i still", "still ok", "still okay", "still good", "safe to eat",
                           "eat it", "use it", "bin it", "throw it", "ruined", "gone a bit",
                           "what can i do with", "what do i do with", "hard", "dry")),
          ("Stale bread is dry, not spoilt: sprinkle it with water and warm it in a 180C oven for "
           "6 to 8 minutes and it comes back close to fresh, and a dry loaf is the right bread for "
           "toast, croutons, breadcrumbs or a panzanella. To stop it happening, keep the loaf "
           "whole and cut slices as you need them, in a paper bag or a bread bin rather than the "
           "fridge, and freeze half of it sliced on day one."),
          ask=("stale", "dry", "hard", "hardened", "tough", "yesterday", "soft again", "revive",
               "gone a bit hard", "gone hard", "gone dry", "dried", "going stale"),
          guard=_not_how_to_keep_it_fresh,
          bias=2),
    entry("bread-mouldy", (("bread", "loaf"),
                           ("mouldy", "mould", "mold", "green", "freeze", "bin",
                            "blue spots", "white spots", "black spots", "green spots",
                            "spots", "speckled", "specks", "blue fluff", "white fluff",
                            "green fuzz", "fuzzy", "furry", "fur", "spores", "blue", "greenish")),
          ("Warmth, damp and the plastic bag it came in are what mould needs, so a loaf in a warm "
           "kitchen goes green within days. Keep it in a paper bag or a bread bin, freeze half of "
           "it sliced on day one, and never keep it in the fridge unless you only ever toast it.")),
    entry("bread-mould-cut", (("bread", "loaf", "loaves"),
                              ("gone off", "off", "smells", "smell", "smelt", "slimy",
                               "still ok", "is it ok", "is it still", "ok to eat", "eaten",
                               "out of date", "past its date", "past the date", "use by",
                               "use by date", "best before", "gone past",
                               "cut the mould off", "cut it off", "scrape it", "scrape the mould",
                               "eat around", "eat it", "cut", "cutting", "scrape", "salvage",
                               "trim", "still eat", "safe", "ok", "okay", "bin", "throw",
                               "away")),
          ("Don't cut the mould off a loaf and eat the rest: the threads reach further than the "
           "green you can see, so bin it. Warmth, damp and the plastic bag it came in are what "
           "mould needs, so a loaf keeps longer in a paper bag or a bin, with half of it frozen "
           "sliced on day one. Hard cheese is the exception - cut an inch around the mould and the "
           "rest is fine."),
          avoid=("stop", "prevent", "going mouldy", "keep it", "store", "how do i keep",
                 "bread bin is", "bread bin has", "bread bin smells", "bread bin stinks",
                 "clean the bin", "clean a bread bin", "cleaning the bin", "clean my bread bin",
                 "wash the bin", "wash a bread bin", "washing the bin", "bin smells", "bin stinks",
                 "empty the bin", "emptying the bin",
                 "bread bin was", "bread bin went", "bread bin looks", "bread bin gets",
                 "mould in my bread bin", "mould in the bread bin",
                 "mould inside my bread bin", "mould inside the bread bin",
                 "mould at the bottom of the bread bin", "mould at the bottom of my bread bin",
                 "lunchbox", "lunch box", "container")
          + PACK_DATE,
          guard=_not_just_a_hard_loaf,
          bias=1),
    entry("freezer-time",
          (("freezer", "freeze", "frozen", "freezing"),
           ("how long", "long", "keep", "keeps", "last", "lasts", "stay", "stays", "months", "year",
            "years", "safe", "still good")),
          FREEZER_KEEP,
          ask=KEEP_ASK,
          avoid=("cook", "cooking", "oven", "roast", "bake", "baking", "reheat", "fry", "air fryer",
                 "boil", "microwave", "take", "defrost", "thaw", "fridge", "refrigerator",
                 "worktop", "counter", "rice", "milk", "formula", "chicken",
                 "power cut", "powercut", "power outage", "power failure", "without power",
                 "broken", "repair",
                 "not freezing", "stopped working", "freezer last", "freezer lasts",
                 "out of the freezer", "left out", "leave it out", "leaving it out",
                 "left on the side", "sitting out", "stay out", "stays out", "stood out",
                 "out overnight", "all night", "overnight")),
    entry("freeze-cooked", (("freeze", "freezer", "frozen"),
                            ("mash", "mashed potato", "potato", "stew", "curry", "soup",
                             "leftovers", "chilli", "bolognese", "food", "lasagne", "lasagna",
                             "pasta bake", "casserole", "shepherds pie", "cottage pie", "pie",
                             "risotto", "paella", "gratin",
                             "quiche", "quiches", "frittata", "frittatas", "omelette",
                             "omelettes", "moussaka", "tagine", "meatballs", "meatball",
                             "burritos", "burrito", "quesadilla", "quesadillas", "stuffing",
                             "sausage rolls", "samosas", "samosa", "spring rolls", "dumplings",
                             "fishcakes", "fish cakes", "nut roast")),
          _freeze_cooked,
          avoid=("out of the freezer", "left out", "leave it out", "leaving it out",
                 "left on the side", "sitting out", "stay out", "stays out", "stood out",
                 "out overnight", "all night")),
    entry("jacket-potato", (("jacket potato", "jacket potatoes", "baked potato",
                             "baked potatoes", "bake a potato", "bake potatoes",
                             "baking potato", "potato in the oven"),
                            ("oven", "cook", "how long", "time", "crispy", "microwave", "air",
                             "done", "know", "ready", "bake", "make", "best", "quick",
                             "fill", "filling", "topping", "toppings", "goes with", "beans",
                             "cheese", "tuna")),
          lambda memory, understood: _jacket(understood),
          avoid=("roast", "roasting", "roasted", "roasties", "soggy",
                 "wedges", "chips", "parboil", "parboiled",
                 "herb", "herbs", "spice", "spices", "seasoning", "rosemary", "thyme", "paprika",
                 "cumin",
                 "in the microwave", "how long do i microwave", "how long should i microwave",
                 "how long to microwave", "how long in the microwave")),
    entry("potato-done",
          (("potato", "potatoes"),
           ("know when", "how do i know", "how can i tell", "when are they done",
            "when are potatoes", "done", "tender", "soft", "ready", "cooked", "cooked through")),
          "Test them with a knife rather than a fork: it should slide in with no resistance at all "
          "and the potato should still hold its shape. Boiled, that is 10 to 12 minutes for small "
          "new potatoes, 15 to 20 for chunks and 20 to 25 for whole medium ones; a fork tells you "
          "too late, and a potato left a minute too long goes watery.",
          avoid=("keep", "keeps", "keeping", "store", "storing", "last", "lasts", "gone off",
                 "sprout", "sprouting", "sprouts", "mouldy", "fridge", "freezer", "green",
                 "greening", "gone green", "gone soft", "sweet potato", "sweet potatoes",
                 "roast", "roasting", "roasted", "roasties", "crispy", "crunchy", "oven",
                 "microwave", "microwaving", "microwaved", "air fryer", "air fry", "airfryer",
                 "air fried")),
    entry("potato-microwave",
          (("potato", "potatoes"),
           ("microwave", "microwaving", "microwaved")),
          "Prick a whole potato all over and give it 8 to 10 minutes on high, turning it halfway. "
          "Chunks or small new potatoes take 5 to 6 minutes with a splash of water in the dish. "
          "Let it stand a minute before you cut into it, and use a knife to check it really is soft "
          "all through.",
          avoid=("sweet potato", "sweet potatoes", "yam", "oven", "roast", "roasting", "bake",
                 "baked", "chip", "chips", "salad", "grow", "plant", "seed potato")),
    entry("corn-microwave",
          (("corn", "sweetcorn", "corn on the cob", "corn cobs", "corn cob"),
           ("microwave", "microwaving", "microwaved", "micro")),
          "In the microwave a cob takes 3 to 4 minutes on full power for one and 5 to 6 for two: "
          "leave it in its husk, or wrap it in a sheet of damp kitchen paper, and turn it once "
          "halfway. Give it a minute to stand before you butter it, because it carries on cooking. "
          "Loose kernels in a covered bowl with a splash of water take 2 to 3 minutes, stirred "
          "halfway, and frozen sweetcorn the same plus a minute.",
          avoid=("popcorn", "popping corn", "cornflour", "corn flour", "corned beef", "hash",
                 "tinned", "tin of", "salad", "salsa", "grow", "growing", "plant", "sow",
                 "sweet corn plant", "field", "tortilla", "bread", "fritter", "fritters")),
    entry("potato-airfryer",
          (("potato", "potatoes"),
           ("air fryer", "air fry", "airfryer", "air fried", "airfried")),
          "Air-fry potato chunks at 200C for 20 to 25 minutes, shaking the basket halfway: cut them "
          "to the same size, keep them in one layer and toss them in a little oil first. Parboiled "
          "ones take 12 to 15 minutes, and a whole jacket potato about 40 minutes at 190C.",
          avoid=("sweet potato", "sweet potatoes", "yam", "grow", "plant", "seed potato"),
          bias=1),
    entry("pancakes", (("pancake", "pancakes", "pancake batter", "crepe", "crepes"),
                       ("make", "recipe", "batter", "mix", "american", "fluffy", "thin",
                        "perfect", "easy", "homemade", "flat", "rise", "risen", "sink",
                        "sank", "thin", "runny",
                        "how long", "time", "cook", "cooking", "minute", "minutes")),
          _pancakes,
          avoid=("buy", "shop", "shops", "supermarket", "box", "packet", "packet mix",
                 "bought", "where can i get", "without eggs", "no eggs", "eggless", "egg free",
                 "without milk", "dairy free", "vegan", "gluten free",
                 "watery", "too thin", "too runny")),
    entry("yorkshire-pudding", (("yorkshire pudding", "yorkshire puddings", "yorkshires",
                                 "yorkshire puds"),
                                ("make", "cook", "rise", "risen", "flat", "crispy", "how",
                                 "recipe", "time", "oven", "oil", "batter")),
          "Get the tin and its oil smoking hot, 220C (200C fan), before the batter goes anywhere "
          "near it. The batter is 100g plain flour, 2 eggs, 150ml milk and a pinch of salt, rested "
          "30 minutes and poured in cold, about 1cm deep, and then the oven door stays shut for 20 "
          "minutes. Flat ones are a cool tin or a batter that was too thin.",
          avoid=("tea", "teabag", "tea bag", "dales", "terrier", "per person", "how many",
                 "reheat", "reheating", "leftover", "leftovers", "freeze", "freezer", "keep",
                 "buy", "shop", "shop bought", "supermarket", "packet",
                 "protein", "calories", "calorie", "kcal", "carbs", "carb", "carbohydrates",
                 "sugar", "fat", "fibre", "fiber", "nutrition", "nutrients")),
    entry("burgers", (("burger", "burgers", "beef burger", "patty", "patties"),
                      ("cook", "make", "recipe", "juicy", "grill", "barbecue", "bbq", "how long",
                       "homemade", "best")),
          "Use 20% fat beef mince, shape loose patties about 2cm thick and press a dent in the "
          "middle with your thumb so they stay flat as they cook. Over a high heat, give them 3 "
          "minutes a side for medium and rest them 2 minutes before they go in the bun. Salt the "
          "outside just before they hit the heat: salt in the mix makes them bouncy.",
          avoid=("sauce", "bun", "buns", "roll", "rolls", "relish", "ketchup", "restaurant",
                 "restaurants", "near me", "nearby", "takeaway", "take away", "delivery", "place",
                 "london", "near") + _NO_MEAT),
    entry("burger-no-meat", (("burger", "burgers", "patty", "patties", "bean burger",
                              "veggie burger"),
                             ("without mince", "no mince", "without beef", "no beef", "without meat",
                              "no meat", "meat free", "meat-free", "vegetarian", "veggie", "vegan",
                              "lentil", "lentils", "bean", "beans", "chickpea", "chickpeas",
                              "pulse", "pulses", "mushroom", "tofu")),
          "Mash a drained tin of black beans or chickpeas with a grated small onion, a handful of "
          "breadcrumbs, a spoon of tomato puree and an egg to bind it - or a flax egg, a tablespoon "
          "of ground flaxseed in three of water, left ten minutes - then chill the mix twenty "
          "minutes so the patties hold. Shape them 2cm thick and fry 4 to 5 minutes a side, or bake "
          "them 20 minutes at 200C (180C fan). Keep them thick and turn them gently: they are "
          "softer than beef, and a thin one breaks. A spoon of smoked paprika is what makes them "
          "taste of something."),
    entry("fish-fingers", (("fish finger", "fish fingers", "fishfingers"),
                           ("cook", "oven", "air fryer", "how long", "grill", "fry", "bake",
                            "best")),
          "Straight from the freezer, 12 to 15 minutes at 200C (180C fan) on a tray, turned once, "
          "until the crumbs are crisp and the middle is hot; an air fryer does them in 10 minutes "
          "at 190C. Don't thaw them first, or the breadcrumbs slide off. Chips, peas and something "
          "sharp to dip them in."),
    entry("halloumi", (("halloumi",),
                       ("cook", "fry", "fried", "grill", "air fryer", "squeaky", "crispy",
                        "how long", "best", "pan")),
          "Slice it 1cm thick, pat it dry and fry it in a dry non-stick pan 2 minutes a side until "
          "it is golden, or grill it 3 minutes a side. Patting it dry is what gives a crust instead "
          "of steam, and turning it once keeps it from going rubbery. It is already salty, so it "
          "needs no oil or salt."),
    entry("sweet-potato", (("sweet potato", "sweet potatoes"),
                           ("cook", "oven", "roast", "bake", "boil", "air fryer", "how long",
                            "wedges", "mash", "fries", "chips")),
          _sweet_potato,
          avoid=("cook with", "cooking with", "make with", "do with", "use up",
                 "recipes", "recipe", "ideas", "idea", "dinner", "tonight",
                 "meal", "meals"),
          bias=1),
    entry("pizza-base", (("pizza", "pizza base", "pizza dough", "dough"),
                         ("base", "dough", "make", "homemade", "recipe", "rise", "no yeast")),
          "Stir 500g strong white flour, 325ml warm water, 7g yeast and 10g salt into a soft "
          "dough, knead it 8 minutes and leave it 1 to 2 hours until doubled. Stretch it thin, "
          "and bake as hot as your oven goes, 250C, for 10 to 12 minutes. With no yeast, use a "
          "flatbread base or add a teaspoon of baking powder and rest it 20 minutes."),
    entry("pulses-soak", (("chickpeas", "chick pea", "chick peas", "dried chickpeas", "beans",
                            "dried beans", "black beans", "butter beans", "kidney beans",
                            "white beans", "haricot beans", "cannellini beans", "pinto beans",
                            "split peas", "black eyed peas"),
                          ("soak", "soaking", "soaked", "overnight", "dried", "long",
                           "need to soak", "slow", "slow cooker", "how do i cook",
                           "how do you cook", "how long do i cook", "how long to cook",
                           "still hard", "still firm", "wont soften", "will not soften",
                           "not softening", "hard after", "too hard", "without soaking",
                           "no soak", "skip the soak", "quick soak", "cook", "boil")),
          _pulses,
          bias=2,
          avoid=("coffee", "coffee bean", "coffee beans",
                 "cook with", "cooking with", "make with", "do with", "dinner", "tea", "supper",
                 "meal", "meals", "what can i make", "what should i cook",
                 "cheap recipe", "cheap recipes", "cheap meal",
                 "what could i cook", "what could i make",
                 "lentil", "lentils", "red lentils", "green lentils", "puy lentils",
                 "brown lentils", "lentil soup", "dal", "daal", "dhal",
                 "tinned", "tin of", "tin", "tins", "jarred",
                 "cheap recipe", "easy recipe", "quick recipe", "recipe with", "recipes with",
                 "recipe using", "recipe that", "recipe ideas",
                 "keep", "keeps", "keeping", "store", "stores", "storing", "stored",
                 "freezer", "freeze", "freezes", "freezing", "frozen", "defrost", "defrosting",
                 "reheat", "reheating", "leftover", "leftovers", "left over",
                 "last", "lasts", "gone off", "still good", "how long do they keep",
                 "go in the fridge", "in the fridge for", "in the fridge after",
                 "fridge for", "the fridge until", "cooked beans keep", "keep in the fridge"
                 ) + _CHEAP_AVOID),
    entry("lentils-cook",
          (("lentil", "lentils", "red lentils", "green lentils", "puy lentils", "brown lentils",
            "split lentils"),
           ("cook", "cooking", "boil", "boiling", "simmer", "how long", "minutes", "take",
            "takes", "soak", "soaking", "soaked", "overnight", "dried", "soft", "mushy",
            "firm", "soup", "dal", "daal", "dhal", "curry")),
          _lentils,
          avoid=("recipe", "recipes", "what can i make", "what can i cook", "meal idea",
                 "meal ideas", "healthy", "protein", "good for you", "calories", "calorie",
                 "nutrition", "diet", "iron", "fibre", "fiber", "lose weight",
                 "freeze", "freezes", "freezing", "frozen", "defrost", "defrosting",
                 "reheat", "reheating", "in the fridge", "keep in the fridge",
                 "how long does it keep", "left over", "leftover", "leftovers")),
    entry("frozen-pizza",
          (("frozen pizza", "frozen pizzas", "pizza"),
           ("cook", "cooking", "oven", "how long", "gas mark", "fan", "crispy",
            "soggy", "best", "properly", "bake", "baking", "preheat", "middle", "shelf",
            "air fryer",
            "defrost", "defrosting", "thaw", "thawed", "straight from", "straight in",
            "what temperature", "temp", "temps")),
          ("Frozen pizza wants a fully heated oven, not a cold one: 200C (180C fan, gas mark 6) "
           "for 12 to 15 minutes, straight on the shelf or a hot tray, until the cheese bubbles "
           "and the base lifts. A cold oven gives you a soggy middle and a pale top, and an air "
           "fryer does a small one in 8 to 10 minutes at 180C."),
          avoid=("dough", "base", "homemade", "make", "making", "recipe", "scratch", "yeast",
                 "leftover", "leftovers", "left over", "freeze", "freezing",
                 "refreeze", "keep", "keeps", "storing", "how long does", "calories",
                 "healthy", "takeaway", "delivery", "shop", "buy", "price", "toppings",
                 "stone", "pizza stone",
                 "fresh", "chilled", "ready made", "ready-made", "ready meal",
                 ),
          guard=_a_frozen_pizza),
    entry("pulses-tinned", (("tinned chickpeas", "canned chickpeas", "tinned beans",
                             "canned beans", "tinned kidney beans", "tinned butter beans",
                             "tin of chickpeas", "tin of beans", "can of chickpeas",
                             "can of beans", "tinned lentils", "tin of lentils",
                             "can of lentils", "jar of chickpeas", "jarred chickpeas",
                             "jar of beans", "jarred beans", "straight from the tin"),
                            ("soak", "soaking", "need", "use", "cook", "eat", "ready",
                             "drain", "instead", "tin", "can")),
          "Tinned chickpeas and beans are already cooked, so there is no soaking and no long "
          "simmer: drain them, rinse the salty water off and they are ready in a soup, a curry "
          "or a salad. Use about two tins where a recipe asks for 250g of dried weight. Dried "
          "ones are the ones that want 8 hours of cold water and 45 to 60 minutes of simmering.",
          avoid=("recipe", "dinner", "meal", "ideas", "what can i cook", "what can i make",
                 "what could i cook", "what could i make", "what should i cook", "cook with",
                 "make with",
                 "what can i do", "do with", "what do i do", "what should i make",
                 "what should i have", "suggest", "something quick", "quick meal",
                 "dropped", "slipped", "foot", "finger", "thumb", "toe", "burn", "burned",
                 "spill", "spilled", "broke", "broken", "shelf")),
    entry("pulses-cheaper",
          (("dried beans", "dry beans", "dried chickpeas", "dry chickpeas", "dried lentils",
            "dry lentils", "dried peas", "dried pulses", "tinned beans", "canned beans",
            "tinned chickpeas", "canned chickpeas", "tinned lentils", "canned lentils",
            "beans", "chickpeas", "lentils", "pulses",
            "tinned or dried", "dried or tinned", "dried ones", "tinned ones",
            "dried version", "tinned version", "from a tin", "out of a tin", "in a tin",
            "bag of", "a bag", "from dried"),
           ("cheaper", "cheapest", "cheap", "cost", "costs", "price", "prices", "worth it",
            "worth the money", "worth buying", "save", "saves", "saving", "money", "value", "better value",
            "more expensive", "expensive", "vs", "versus")),
          "Dried beans, chickpeas and lentils cost about a third of the tinned price for the same "
          "amount on the plate: half a kilo of dried, around £1.20, cooks up to about the same as "
          "three or four tins at 70p to 90p each, and a bag of dried lentils is under £2 a kilo "
          "where mince is £5 to £7 for 500g, so pulses are much the cheaper protein. Tinned wins "
          "when dinner has to be on the table in ten minutes; dried wins if you cook a big pot at "
          "the weekend and freeze it in portions.",
          avoid=("coffee", "baked beans", "baked bean", "green beans", "green bean",
                 "gravel", "sand", "cement", "concrete", "topsoil", "compost", "shingle",
                 "chippings", "bulk bag", "bark", "slate", "aggregate", "paving", "mortar",
                 "ballast", "mulch", "woodchip", "pebbles", "building",
                 "pasta", "rice", "noodles", "snake", "pet", "dog", "cat",
                 "dinner", "tea", "supper", "lunch", "breakfast", "meal", "meals", "tonight",
                 "salad", "curry", "soup", "recipe", "recipes", "protein",
                 "healthy", "healthier", "healthiest", "good for you", "worth eating",
                 "nutritious", "filling", "tuna", "fish", "salmon", "prawn", "prawns",
                 "tomato", "tomatoes"),
          bias=1),
    entry("tin-keep", (("tin", "tins", "tinned", "can of", "cans of", "tin of", "tins of"),
                       ("opened", "open", "once opened", "after opening", "in the fridge",
                        "half a tin", "half a can", "kept in the tin", "still in the tin",
                        "in the tin", "in a tin", "gone off", "off")),
          "An opened tin keeps 2 days in the fridge, and only once you have emptied it into a "
          "bowl or a lidded tub: leave food in the tin and the metal taints it and can make you "
          "ill. Cover it, keep it cold, and reheat it until it is piping hot. An unopened tin "
          "keeps for years in a cupboard, so trust the date stamped on it.",
          ask=("opened", "open", "once opened", "after opening", "in the fridge",
               "half a tin", "half a can", "kept in the tin", "still in the tin",
               "in the tin", "in a tin", "tin", "tins", "tinned", "tin of", "tins of",
               "can of", "cans of"),
          avoid=("paint", "paint tin", "emulsion", "gloss", "undercoat", "varnish", "wood stain",
                 "opener", "can opener", "without an opener", "without a can opener",
                 "how do i open", "how to open", "how do you open", "tin without",
                 "recipe", "dinner", "meal", "ideas", "what can i make", "what can i cook",
                 "what should i cook", "cook with", "make with", "soak", "soaking",
                 "already cooked", "do i need to cook",
                 "protein", "carbs", "carb", "carbohydrate", "carbohydrates", "calories",
                 "calorie", "fibre", "fiber", "how much fat", "how much sugar",
                 "cake", "cakes", "biscuit", "biscuits", "bread", "loaf", "baking", "traybake",
                 "cake tin", "loaf tin", "baking tin", "roasting tin", "tin foil", "foil",
                 "freeze", "freezing", "frozen",
                 "jar", "jars", "jam", "pesto", "ketchup", "mayonnaise", "chutney", "pickle",
                 "milk", "cream", "yoghurt", "bottle", "carton", "wine"),
          bias=2),
    entry("salad-dressing", (("vinaigrette", "dressing", "salad dressing"),
                             ("make", "recipe", "oil", "vinegar", "ratio", "good", "keep")),
          "Whisk 3 parts olive oil to 1 part vinegar with a teaspoon of mustard, a pinch of salt "
          "and pepper: the mustard holds it together. Make it in a jam jar and shake it, and it "
          "keeps a week in the fridge.",
          avoid=("costume", "costumes", "fancy dress", "dress up", "dressing up", "world book day",
                 "halloween", "outfit", "party outfit")),
    entry("avocado-brown", (("avocado", "avocados"),
                            ("brown", "going brown", "browning", "black", "keep", "stop")),
          "Lemon or lime juice on the cut face slows it down, and cling film pressed right onto "
          "the flesh works better than a loose lid. Brown patches are only air damage; cut them "
          "off and the rest is fine."),

    entry("stock-carcass",
          (("stock", "stocks", "broth", "broths", "carcass", "carcasses", "bones", "bone",
            "bone broth", "stockpot", "stock pot", "bouillon", "consomme", "consommé"),
           ("chicken", "turkey", "beef", "fish", "lamb", "pork", "ham", "duck", "goose",
            "venison", "vegetable", "veg", "mushroom", "mushrooms", "peelings", "scraps",
            "make", "made", "making", "recipe", "use", "keep", "keeps", "keeping",
            "store", "freeze", "freezer", "fridge", "last", "how long", "how much",
            "how many", "simmer", "simmering", "boil", "boiling", "cook", "cooking",
            "time", "hours", "minutes", "cube", "cubes", "granules", "skim", "scum",
            "foam", "risotto", "slow cooker", "pressure cooker", "healthy", "good for",
            "taste", "flavour", "flavor", "bland", "better", "stronger", "vegan",
            "vegetarian", "without bones", "no bones", "jelly")),
          _stock_answer,

          avoid=PET_LINE_WORDS + ("broken", "broke", "heal", "heals", "healing", "healed",
                                  "fracture", "fractured", "mend", "mending", "broken bone",
                                  "my bone", "my arm", "my leg", "my wrist", "my ankle",
                                  "my finger", "my toe", "my rib", "my collarbone",
                                  "human", "human body", "the body", "my body", "your body",
                                  "in the body", "in my body", "skeleton", "skeletal",
                                  "how many bones", "bones do i have", "bones in the body",
                                  "bones in my body", "bones does a", "bones has a") + STOCK_AVOID),
    entry("chicken-skin", (("chicken", "turkey"),

                           ("skin", "crispy", "crisp", "golden", "brown")),
          "Dry the skin and salt it, keep it uncovered in the fridge for an hour if you can, and "
          "roast it on a rack at 200C (180C fan) without basting or covering. Steam is the enemy: "
          "a wet bird in a crowded tin comes out pale and flabby."),
    entry("fridge-life", (("fridge",),
                          ("how long", "keep", "keeps", "last", "safe", "still ok", "gone off",
                           "days", "use by", "out of date",
                           "overnight", "til tomorrow", "till tomorrow", "until tomorrow",
                           "next day", "in the morning",
                           "ok to eat", "safe to eat", "alright to eat", "ok to drink",
                           "safe to drink", "can i eat", "can we eat", "edible")),
          ("Cooked food keeps 3 to 4 days in the fridge, raw meat and fish 1 to 2 days, and milk, "
           "cheese and yogurt until the date on the pack, or a couple of days past it if they look "
           "and smell right. Cooked rice is the exception at 1 day, and anything left out for more "
           "than 2 hours goes in the bin: the bugs that make you ill have no smell."),
          avoid=("rice", "chicken", "milk", "egg", "eggs", "cheese", "yogurt", "leftovers",
                 "leftover", "beer", "wine", "drink", "drinks", "bottle", "lager",
                 "keep water", "keeps water", "keep a jug", "keep the jug", "jug", "jugs",
                 "ginger", "spring onion", "spring onions", "scallion", "scallions",
                 "lettuce", "spinach", "rocket", "arugula", "salad", "leaves", "leafy",
                 "watercress", "herb", "herbs", "basil", "coriander",
                 "apple", "apples", "fruit", "banana", "bananas", "orange", "oranges",
                 "berries", "strawberries",
                 "boil over", "boils over", "boiling over", "boiled over", "overflow",
                 "overflows", "spill", "spills", "spilling", "spilled", "spilt",
                 "get cold", "gets cold", "get colder", "cool down", "cools down",
                 "cooling down", "get to temperature", "get down to temperature",
                 "come down to temperature", "putting food in", "put food in",
                 "how long should i wait", "wait before",
                 "smell", "smells", "smelly", "stink", "stinks", "stinking", "odour",
                 "odor", "musty", "off smell", "bad smell", "smelling fresh", "smells fresh",
                 "clean the fridge", "clean out the fridge", "clean my fridge", "cleaning the fridge",
                 "starter", "starters", "sourdough", "sour dough", "levain",
                 "wipe out", "defrost the fridge", "fridge smelling", "fridge smells")
                 + ("burnt", "burned", "charred", "scorched", "burnt on", "caught on the bottom")
                 + JOB_GUARD),

    entry("popcorn",
          (("popcorn", "pop corn", "popping corn", "popcorns"),
           _FOOD + ("pop", "popped", "popping", "kernels", "kernel", "hob", "pan", "pot",
                    "microwave", "stovetop", "stove top", "how", "best", "homemade",
                    "at home", "cinema", "salted", "salty",
                    "without oil", "no oil", "air pop", "air-popped", "air popped")),
          _popcorn_make,
          avoid=("ceiling", "popcorn ceiling", "corn on the cob", "sweetcorn", "grow",
                 "growing", "plant", "plants", "keep", "keeps", "keeping", "store",
                 "storing", "last", "lasts", "stale", "chewy", "soft", "leftover",
                 "healthy", "healthier", "calories", "diet", "weight", "fattening", "fat",
                 "makes you fat", "unhealthy",
                 "clean", "cleaning", "wash", "washing", "maker", "popper", "machine",
                 "smell", "smells", "smelling", "smelled", "smelly", "odour", "odor",
                 "smell of popcorn", "popcorn smell", "get rid of the smell", "curtains",
                 "cushions", "cushion", "carpet", "carpets",
                 "caramel", "toffee", "toffeed", "caramelised", "caramelized",
                 "why"),
          bias=1),
    entry("popcorn-keep",
          (("popcorn", "pop corn", "popping corn", "kernels"),
           ("keep", "keeps", "keeping", "store", "storing", "storage", "last", "lasts",
            "long", "stale", "soft", "chewy", "leftover", "left over", "airtight", "tin",
            "jar", "crisp", "crispy", "fresh", "how long", "came out", "comes out", "turned",
            "went", "gone", "go", "goes")),
          _popcorn_keep,
          avoid=("ceiling", "corn on the cob", "sweetcorn",
                 "smell", "smells", "smelling", "smelled", "smelly", "odour", "odor",
                 "smell of popcorn", "popcorn smell", "curtains", "cushions", "cushion")),
    entry("popcorn-health",
          (("popcorn", "pop corn"),
           ("healthy", "healthier", "healthiest", "diet", "calories", "fattening", "weight",
            "good for you", "bad for you", "snack", "better than", "nutrition", "fibre",
            "fat", "fats", "makes you fat", "make me fat", "put on weight", "carbs",
            "unhealthy")),
          "Air-popped popcorn is a good snack: a big bowl is roughly 30 to 50 calories, it is "
          "whole grain, and the fibre and the chewing make it more filling than crisps. It is the "
          "butter, the salt and the toffee that turn it into a treat, so go easy on those rather "
          "than on the popcorn itself.",
          avoid=("ceiling", "corn on the cob", "sweetcorn",
                 "smell", "smells", "smelling", "smelly", "odour", "odor",
                 "smell of popcorn", "popcorn smell", "curtains", "cushions", "cushion"),
          bias=1),
    entry("fix-bland",
          (("bland", "tasteless", "flavourless", "no flavour", "more flavour", "lacks flavour",
            "tastes of nothing", "no taste", "flat", "dull"),
           _A_TASTE),
          "Season it in that order: a pinch more salt, then a squeeze of lemon or a splash of "
          "vinegar, then something savoury like a stock cube, a splash of soy or a knob of butter. "
          "Bland food is nearly always short of salt and acid rather than spice; if you're cutting "
          "salt, the lemon and the savoury splash do most of it on their own.",
          avoid=("coffee", "flat white", "latte", "cappuccino", "espresso", "americano", "tea",
                 "wine", "beer", "cider", "lager", "champagne", "lemonade", "cola",
                 "fizzy", "battery", "tyre", "tire", "joke", "voice", "music", "greyhound", "dog",
                 "dogs", "cat", "cats", "puppy", "kitten", "rent", "landlord", "garden",
                 "flatmate", "flat mate", "neighbour", "neighbours", "mortgage", "tenancy",
                 "lease", "estate agent",
                 "pancake", "pancakes", "yorkshire pudding", "yorkshires",
                 "new flat", "my flat", "the flat", "our flat", "in the flat", "in my flat",
                 "moved in", "moved into", "moving in", "moving into", "renting", "tenancy",
                 "let agreed", "deposit",
                 "bed flat", "bedroom flat", "studio flat", "one bed", "1 bed", "two bed",
                 "2 bed", "three bed", "3 bed", "bedsit", "bungalow",
                 "a lot of stuff", "lots of stuff", "too much stuff", "boxes of stuff",
                 "stuff to move", "moving house", "house move", "moving flat", "move flat",
                 "bread", "breads", "sourdough", "loaf", "loaves", "dough",
                 "risen", "rose", "prove", "proved", "proving", "proofed", "proving basket",
                 "mould", "mouldy", "mold", "moldy", "gone off", "went off", "stale", "sour",
                 "safe to eat", "still eat", "how long does it keep", "how long does my"),
          guard=_not_the_flat_you_live_in_bake,
          bias=1),
    entry("fix-salty",
          (("salty", "too much salt", "over salted", "oversalted", "salt in it", "too salty"),
           _FOOD),
          _salty,
          avoid=("sea", "ocean", "water", "pool", "sweat", "tears", "crisps", "chips"),
          bias=1),
    entry("fix-watery",
          (("watery", "runny", "too thin", "sloppy", "too much liquid",
            "never thickens", "wont thicken", "won't thicken", "not thickening",
            "isnt thickening", "isn't thickening", "doesnt thicken", "doesn't thicken",
            "wont reduce", "won't reduce", "never reduces",
            "too wet", "a bit wet", "is wet", "went wet", "bit wet"), _FOOD + _WET_FOOD),
          _watery,
          avoid=("soup", "gravy", "ketchup", "paint", "nail", "glue", "poo", "nappy",
                 "stir fry", "stir-fry", "stirfry", "wok", "stir fried",
                 "diarrhoea", "egg", "eggs", "yolk", "yolks", "poach", "poached", "boil", "boiled",
                 "omelette", "honey", "nose", "coffee", "tea", "drink", "drinks", "mug", "cuppa",
                 "kettle",
                 "dressing", "dressings", "vinaigrette",
                 ),
          bias=1),
    entry("yoghurt-grainy",
          (("yoghurt", "yogurt", "yoghurts", "yogurts", "homemade yoghurt", "home made yoghurt",
            "home-made yoghurt", "yoghurt pot", "labneh", "skyr", "kefir"),
           ("grainy", "grainy bits", "gritty", "bitty", "lumpy", "lumps", "curdled", "separated",
            "split", "squeaky", "chalky", "went wrong", "goes wrong", "failed", "fail",
            "didnt set", "didn't set", "wont set", "won't set", "not set")),
          "Shop-bought yoghurt that looks grainy has usually been shaken about or chilled too "
          "hard in transit: stir the whey back in and eat it, it is harmless. Homemade yoghurt "
          "goes grainy when the milk got above about 46C, because the culture and the milk "
          "proteins clump: heat the milk to 85C first, cool it to 43-45C before stirring the "
          "starter in, and keep it at 43C while it sets - an oven with just the light on, or a "
          "flask, holds it steadier than a warm spot that swings.",
          avoid=("use instead", "substitute", "instead of", "how long does", "out of date",
                 "use by", "sell by", "gone off", "mould", "mold", "freeze", "freezer",
                 "frozen yoghurt", "ice cream", "watery", "runny", "calories", "protein",
                 "diet", "baby", "weaning", "greek", "which yoghurt", "best yoghurt"),
          bias=1),
    entry("fix-dry",
          (("dry", "dried out", "overcooked", "over cooked", "over-cooked", "overdone",
            "over done", "over-done"),
           _FOOD + _BAKED_GOODS + ("joint", "joints")),
          _dry,
          avoid=("scrambled", "scramble", "wine", "cider", "skin", "hands", "mouth", "weather",
                 "washing", "clothes", "dryer", "tumble", "hair", "eye", "eyes", "cough",
                 "chicken breast", "breast", "market", "markets", "shares", "stocks",
                 "portfolio", "protein", "shampoo", "conditioner",
                 "cat", "cats", "dog", "dogs", "kitten", "puppy", "pet", "pets",
                 "dishes", "plate", "plates", "towel", "towels", "sink", "draining board",
                 "dry beans", "dried beans", "dry chickpeas", "dried chickpeas",
                 "dry lentils", "dried lentils", "dry pulses", "dried pulses",
                 "dry peas", "dried peas", "split peas",
                 "brownie", "brownies",
                 "flapjack", "flapjacks", "scone", "scones", "sponge", "sponges",
                 "dry herb", "dry herbs", "dried herb", "dried herbs", "drying herbs",
                 "dry them", "dry lavender", "drying lavender",
                 "dry rub", "dry rubs", "spice rub", "rub for", "make a rub", "rub recipe",
                 "rub the", "what goes in a rub")
          + _BAKE_KEEPING,
          bias=1),
    entry("bake-burning",
          (("burnt", "burned", "burning", "burns", "burn", "charred", "scorched", "caught",
            "catching", "too brown", "brown on top", "browned too fast", "dark on top",
            "black on top", "burnt on top", "burnt on the edges", "burning around the edges",
            "burnt on the bottom", "burned on the bottom", "burn on the bottom",
            "burns on the bottom", "burning on the bottom", "burnt bottom", "bottom burnt",
            "black on the bottom", "black at the bottom", "bottom is black", "bottom is burnt",
            "bottom goes black", "burnt underneath", "burns underneath", "burning underneath",
            "bottom of my cake", "bottom of the cake", "bottom of my bread", "bottom of the loaf",
            "bottom of my pie", "cake bottom"),
           ("cake", "cakes", "sponge", "loaf", "loaves", "bread", "buns", "biscuits", "cookies",
            "muffins", "brownies", "cheesecake", "pastry", "pie", "pies", "tart", "tarts",
            "bake", "baking", "baked", "oven", "tin", "traybake", "scones", "pizza", "quiche",
            "victoria sponge", "fruit cake", "madeira")),
          _bake_burning,
          ask=("oven", "bake", "baking", "baked", "tin", "tray", "shelf", "top", "edges", "cake",
               "cakes", "sponge", "loaf", "loaves", "bread", "buns", "biscuits", "cookies",
               "muffins", "brownies", "cheesecake", "pastry", "pie", "pies", "tart", "tarts",
               "scones", "pizza", "quiche", "traybake", "bake it", "stop it",
               "bottom", "underneath", "underside"),
          avoid=("pan", "pot", "saucepan", "sauce", "gravy", "soup", "stew", "rice", "toast",
                 "toaster", "meat", "chicken", "roast", "steak", "sausage", "sausages", "bbq",
                 "barbecue", "smell", "smoke", "alarm", "iron", "shirt", "hand", "finger",
                 "skin", "sun", "candle", "coffee", "espresso", "tea ", "kettle", "panini",
                 "clean", "cleaning", "cleaned", "cleaner", "scrub", "scrubbing", "scour",
                 "soak", "wash", "washing", "wipe", "wiping", "stain", "stains", "stained",
                 "residue", "grease", "greasy", "shelf",
                 "off the tin", "off my tin", "off the tray", "get the burnt off",
                 "marks on the oven", "marks in the oven", "marks off the oven",
                 "glass", "door", "burnt on bits", "burnt on the glass", "burnt on the door",
                 "bottom of the oven", "sides of the oven", "inside of the oven",
                 "inside of my oven", "interior of the oven",
                 "stuck to the oven", "stuck on the oven"),
          bias=1),
    entry("fix-burnt",
          (("burnt", "burned", "scorched", "charred", "caught on the bottom",
            "caught at the bottom", "burnt on the bottom", "burned on the bottom",
            "stuck to the bottom"),
           _FOOD + ("stuffing", "crackling", "parsnips")),
          _burnt_dish,
          avoid=("toast", "toaster", "smell", "smoke", "alarm", "iron",
                 "cake", "cakes", "sponge", "muffins", "brownies", "scones", "loaf", "loaves",
                 "bread", "pie", "pies", "tart", "tarts", "pastry", "biscuits", "cookies",
                 "traybake", "cheesecake", "quiche", "flapjack", "fruit cake",
                 "victoria sponge", "cake tin", "baking tray", "baking sheet", "pizza",
                 "shirt", "hand", "finger", "mouth", "tongue", "skin", "sun", "candle",
                 "chest", "throat", "tummy", "stomach", "gullet", "heartburn", "reflux",
                 "acid", "indigestion", "burning when i", "burns when i", "burning in my",
                 "burns in my", "burning after", "burns after", "eyes", "eye", "lips",
                 "clean", "cleaning", "cleaned", "scrub", "scour", "soak", "soaking", "wash",
                 "washing", "comes off", "come off", "off the bottom", "off my pan",
                 "off the pan", "off the inside", "off the base", "get it off", "still stuck",
                 "stuck on", "wont come", "won't come",
                 "stuck to it", "stuck to the pan", "stuck to my pan", "stuck to the pot",
                 "stuck to my pot", "stuck in the pan", "stuck in my pan",
                 "off a pan", "off a pot", "off pots", "off pans",
                 "coffee tastes", "coffee taste", "coffee that tastes", "coffee is burnt",
                 "espresso tastes", "espresso is burnt", "tea tastes", "tea taste",
                 "tea that tastes", "tea is burnt"),
          bias=1),
    entry("fix-undercooked",
          (("undercooked", "under cooked", "under-cooked", "underbaked", "under baked",
            "underbake", "doesnt cook in the middle", "doesn't cook in the middle",
            "not cook in the middle", "wont cook in the middle", "won't cook in the middle",
            "doesnt bake in the middle", "doesn't bake in the middle",
            "not bake in the middle", "wont bake in the middle", "won't bake in the middle",
            "not cooking in the middle", "not baking in the middle",
            "isnt cooked in the middle", "isn't cooked in the middle",
            "isnt baked in the middle", "isn't baked in the middle",
            "arent cooked in the middle", "aren't cooked in the middle",
            "is not cooked in the middle", "is not baked in the middle",
            "still hard", "hard in the middle",
            "doughy", "doughy in the middle", "claggy in the middle",
            "crunchy", "raw in the middle", "not cooked through", "not cooked in the middle",
            "wet in the middle", "soggy in the middle", "not done in the middle",
            "still crunchy"),
           _FOOD + ("loaf", "loaves", "sourdough", "bread roll", "bread rolls", "traybake",
                    "yorkshires", "batter", "pancake", "pancakes", "dumplings")),
          _undercooked,
          avoid=("crispy", "salad", "slaw", "topping", "crumble", "goes with", "side", "snack",
                 "how do i make", "how to make", "how do i get", "how to get", "how do i keep",
                 "how to keep", "make crunchy", "get crunchy", "stay crunchy", "want it crunchy",
                 "want them crunchy",
                 "chicken", "turkey", "pork", "sausage", "sausages", "burger", "burgers",
                 "prawns", "prawn", "mussels", "mince",
                 "how do i make it crunchy", "how do i get it crunchy", "how do i make them crunchy",
                 "how do i keep", "keep them crunchy", "i want it crunchy", "want it crunchy",
                 "love crunchy", "like it crunchy", "extra crunchy"),
          bias=1),
    entry("fix-greasy",
          (("greasy", "oily", "fatty", "too much oil", "too oily", "swimming in oil",
            "swimming in fat", "too greasy"),
           _FOOD + ("chips", "chip", "fries", "fry", "pakora", "pakoras", "doughnuts",
                    "doughnut", "onion rings", "tempura")),
          _greasy,
          avoid=("hair", "skin", "face", "forehead", "scalp", "hands", "pizza", "takeaway",
                 "take away", "take-away", "restaurant", "chippy", "delivery", "burger van"),
          bias=1),
    entry("fix-sticking",
          (("sticking", "sticks to the pan", "stuck to the pan", "glued to the pan", "sticks"), _FOOD),
          _STUCK_TO_A_PAN,
          avoid=("label", "sticker", "drawer", "window", "door", "envelope", "stamp", "plaster",
                 "tape", "fridge", "lid",
                 "make it stick", "make it stick this time", "stick with it", "stick at it",
                 "keep it up", "keep going", "habit", "routine", "motivation", "revision",
                 "revise", "revising", "study", "studying", "exam", "exams", "practice",
                 "practising", "practicing", "training", "workout", "skills", "skill",
                 "together", "clumped", "clumps", "clumpy", "gluey", "sticky rice",
                 "cake", "cakes", "sponge", "loaf", "bread", "bun", "buns", "muffin", "muffins",
                 "pastry", "baking paper", "baking parchment", "baking tin", "cake tin",
                 "springform", "tin", "tins",
                 "pancake", "pancakes", "crepe", "crepes", "batter", "waffle", "waffles",
                 "yorkshire", "yorkshires", "yorkshire pudding", "pikelet", "pikelets"),
          bias=1),
    entry("food-stuck-to-a-pan",
          (("stuck to the pan", "stuck to my pan", "stuck on the pan", "sticks to the pan",
            "sticks to my pan", "sticking to the pan", "sticking to my pan", "glued to the pan",
            "stuck to the wok", "stuck to the skillet", "stuck to the griddle",
            "stuck to the frying pan", "stuck to the pot", "stuck to my pot",
            "stuck to the saucepan", "stuck to my saucepan", "stuck to the bottom of the pan",
            "stuck to the bottom of my pan", "stuck to the bottom of the pot",
            "stuck to the bottom of my pot", "sticking to the bottom of the pan",
            "sticking to the bottom of the pot"),
           ("pan", "pans", "frying pan", "wok", "woks", "skillet", "griddle", "saucepan",
            "saucepans", "pot", "pots", "casserole")),
          _STUCK_TO_A_PAN,
          avoid=("cake", "cakes", "sponge", "loaf", "loaves", "bread", "bun", "buns",
                 "muffin", "muffins", "pastry", "tin", "tins", "tray", "baking paper",
                 "baking parchment", "together", "clumped", "clumps", "clumpy", "gluey",
                 "sticky rice", "label", "sticker", "drawer", "window", "door", "envelope",
                 "stamp", "plaster", "tape", "fridge", "lid", "burnt", "burned", "burnt",
                 "black", "scorched", "clean", "cleaning", "scrub", "soak", "off the",
                 "non stick", "nonstick", "season", "seasoning",
                 "something", "anything", "everything", "stuff", "bits", "things", "rice")),
    entry("fix-lumpy",
          (("lumpy", "lumps"), _FOOD),
          _lumpy,
          avoid=("gravy", "mattress", "pillow", "breast", "skin", "throat", "gland", "bump",
                 "nails", "nail", "nail polish", "nail varnish", "manicure", "varnish",
                 "fingernail", "fingernails", "cuticle", "cuticles",
                 "my baby", "baby", "babies", "weaning", "weaned", "first foods", "six months",
                 "6 months", "month old", "toddler", "my son", "my daughter", "my child",
                 "her food", "his food", "their food", "the babys", "finger food"),
          bias=1),
    entry("fix-rubbery",
          (("rubbery", "like rubber", "chewy", "tough"),
           _FOOD + _BAKED_GOODS),
          _tough,
          avoid=("boots", "boot", "shoes", "shoe", "scrambled", "scramble", "scrambling",
                 "omelette", "fried egg", "poached", "mashed", "mash", "porridge", "interview",
                 "meeting", "boss", "decision", "choice",
                 "mince", "minced",
                 "popcorn", "pop corn",
                 "biscuit", "biscuits", "cookie", "cookies", "shortbread", "scone", "scones",
                 "cracker", "crackers", "flapjack", "flapjacks"),
          bias=1),
    entry("bake-gummy",
          (("gummy", "clammy", "wet in the middle", "soggy in the middle", "stodgy", "doughy",
            "raw in the middle", "undercooked in the middle", "not cooked in the middle",
            "gummy inside", "gummy in the middle", "wet inside", "stodgy in the middle",
            "doughy in the middle"),
           _BAKED_GOODS + ("bread", "loaf", "loaves", "sourdough", "focaccia", "brioche",
                           "ciabatta", "baguette", "pitta", "pita", "rolls", "bread rolls")),
          _gummy,
          avoid=("rice", "risotto", "pasta", "noodles", "semolina", "polenta", "porridge",
                 "gravy", "sauce", "stew", "bread sauce"),
          bias=1),
    entry("bake-pale",
          (("pale", "pale on top", "no colour", "not browned", "didnt brown", "did not brown",
            "wont brown", "won't brown", "stayed pale", "white on top", "looks raw",
            "looks undercooked", "underbaked", "under baked"),
           _BAKED_GOODS + ("bread", "loaf", "loaves")),
          "A bake that stays pale is short of heat or short of sugar. Check the oven with a "
          "thermometer, because most run 10 to 20C cool, and put it up 10C for the last ten "
          "minutes. Milk or egg brushed on top browns it. If the middle is still wet it is "
          "underbaked, not pale: give it 10 more minutes under foil.",
          avoid=("pale ale", "ale", "beer", "wine", "skin", "pale skin", "pale face", "i look pale",
                 "looking pale", "feel pale", "stool", "poo", "urine"),
          bias=1),
    entry("bake-soda-taste",
          (("bicarbonate", "bicarbonate of soda", "baking soda", "bicarb", "soda taste",
            "tastes of soda", "soapy", "tastes soapy", "tastes of soap", "chemical taste",
            "tastes chemical", "metallic taste", "tastes of raising agent"),
           _BAKED_GOODS + ("bread", "loaf", "loaves", "soda bread", "bake", "baked", "baking",
                           "batter", "dough")),
          "A soapy or chemical taste is too much bicarbonate, because the soda had nothing acid "
          "to react with. Use about a quarter of a teaspoon per 100g of flour and give it "
          "something sour - buttermilk, yoghurt, lemon or treacle. Sift it with the flour rather "
          "than stirring it in at the end, and a squeeze of lemon over a baked one hides most of "
          "it.",
          avoid=("clean", "cleaning", "sink", "drain", "fridge", "washing", "laundry", "stain",
                 "toilet", "bath", "oven cleaner",
                 "vs", "versus", "difference between", "or baking powder", "or soda",
                 "or bicarb", "which one",
                 ),
          bias=1),
    entry("fix-egg-white",
          (("egg white", "egg whites", "whites"), ("stiff", "peaks", "whip", "whipping", "whisk",
                                                   "fluffy", "rise", "volume")),
          "Any yolk, grease or water stops them whipping: use a clean dry bowl, separate the eggs "
          "while they're cold, then let the whites come to room temperature. A pinch of salt or a "
          "drop of lemon helps, and so does beating on a medium speed rather than flat out."),
    entry("pastry-shrink",
          (("pastry", "tart", "tart case", "quiche", "flan", "pie", "case"),
           ("shrink", "shrinks", "shrinking", "shrank", "sides", "slip", "slipping", "slides",
            "pulls", "pulled", "smaller")),
          "Pastry shrinks for three reasons: the dough is warm, it is stretched instead of eased "
          "into the tin, or it bakes without a rest. Roll it cold, press it into the corners "
          "rather than pulling it, leave a little overhang instead of trimming it flush, and chill "
          "the lined tin for 20 minutes before it goes in. That rest is what stops the sides "
          "sliding down.",
          avoid=("jumper", "jumps", "wool", "washing", "clothes", "shirt", "fabric", "cotton")),
    entry("pastry-ideas",
          (("puff pastry", "filo pastry", "phyllo pastry", "filo", "phyllo", "puff", "pastry",
            "readymade pastry", "ready made pastry", "ready-rolled pastry", "jus rol"),
           ("make with", "cook with", "do with", "what can i", "what can we", "ideas", "idea",
            "use it for", "fill it with", "fill with", "stuff it", "quick", "easy")),
          "Quick things for both, with the oven at 200C fan: puff pastry makes sausage rolls, "
          "cheese straws, palmiers, a tomato and goat's cheese tart, or a sheet folded over "
          "sliced apple as a rough tarte tatin. Filo makes spanakopita, samosas, little cigar "
          "rolls of feta and spinach, and baklava - keep it under a damp cloth while you work, "
          "because it dries out in a minute. For either one, heat the empty tray in the oven "
          "first, get the filling already cooked and cooled, brush the top with beaten egg, and "
          "don't open the door for the first 15 minutes or it sinks. Spare sheets freeze well: "
          "wrap them tight and they thaw in about 20 minutes.",
          bias=2,
          avoid=("from scratch", "how do i make", "how to make", "rough puff", "shortcrust",
                 "choux", "suet", "protein", "calories", "calorie", "kcal", "carbs", "sugar",
                 "fat", "fibre", "fiber", "healthy", "nutrition", "shrink", "shrinks", "soggy",
                 "why", "dont", "didnt", "wont", "stuck", "burnt",
                 "leftover", "left over", "spare", "use up", "going spare")),
    entry("make-puff-pastry",
          (("puff pastry", "rough puff", "puff", "flaky pastry", "palmiers", "sausage rolls",
            "vol au vent"),
           ("make", "making", "recipe", "how", "from scratch", "easy", "quick", "home",
            "homemade", "butter", "flour", "fold", "folds", "turn", "turns", "rise", "rising")),
          "Rough puff, which is the home version: 250g plain flour, 250g of butter still cold from "
          "the fridge cut into 1cm cubes, a pinch of salt, and about 120ml of iced water. Bring it "
          "to a dough with the butter still in visible lumps, rest it 20 minutes, then roll it out "
          "to a long rectangle, fold the top third down and the bottom third over it, and turn it a "
          "quarter turn. Do that four times, resting it in the fridge for 20 minutes if it starts "
          "to feel soft, and chill it 30 minutes before it goes in the oven. Cold butter and cold "
          "hands are what make it rise: if the butter melts into the flour it bakes flat and tough. "
          "Bake at 220C. Real puff, with a flattened block of butter folded inside, is worth buying "
          "for a special occasion; filo is always worth buying.",
          avoid=("dont", "didnt", "wont", "not", "soggy", "flat", "sunk", "burn", "burnt",
                 "shrink", "shrinks", "why", "stuck",
                 "protein", "calories", "calorie", "kcal", "carbs", "carb", "carbohydrates",
                 "sugar", "fat", "fibre", "fiber", "nutrition", "nutrients", "healthy",
                 "make with", "cook with", "do with", "what can i", "what can we", "use up",
                 "leftover", "left over", "with puff pastry", "goes with", "serve with")),
    entry("fix-pastry",
          ("pastry", ("breaking", "cracks", "cracking", "crumbly", "falls apart", "tears", "tearing")),
          "Pastry cracks when it's too dry or too warm: sprinkle on a little cold water, chill it "
          "for 20 minutes, and roll it between two sheets of baking paper. Patch any tear with a "
          "damp finger before it goes in the oven and nobody will see it."),
    entry("pastry-fault",
          (("pastry", "pastry case", "pastry base", "pie crust", "pie base", "pie case",
            "tart base", "tart case", "flan case", "flan base", "quiche base", "shortcrust",
            "pie", "quiche", "tart", "flan",
            "the tin", "in the tin"),
           ("shrink", "shrank", "shrunk", "shrinking", "shrinks", "pulled away", "pulls away",
            "slid down", "slides down", "slumped", "slumps", "slumping", "limp",
            "soggy", "soggy bottom", "soggy base", "soggy underneath", "wet underneath",
            "raw underneath", "pale underneath")),
          _pastry_fault,
          avoid=("clothes", "clothing", "jumper", "jumpers", "shirt", "shirts", "dress",
                 "dresses", "wool", "woollen", "cotton", "laundry", "washing", "wash",
                 "machine", "tumble", "dryer", "iron", "fabric", "curtains", "curtain",
                 "shrink wrap", "label",
                 "how do i make pastry", "pastry recipe", "shortcrust recipe",
                 "how do i make shortcrust", "puff pastry", "filo", "choux",
                 "blind bake", "blind baking", "make a quiche", "quiche recipe",
                 "make a pie", "pie recipe"),
          bias=2),
    entry("biscuit-chewy",
          (("cookie", "cookies", "biscuit", "biscuits", "shortbread", "flapjack", "flapjacks"),
           ("chewy", "chewier", "chewiness", "gooey", "squidgy", "soft centre",
            "soft in the middle")),
          "Chewy comes from soft brown sugar and pulling the tray out early: swap a third of the "
          "caster sugar for light muscovado, add an extra yolk, and take them out while the middles "
          "still look underdone, because they carry on setting on the hot tray.",
          avoid=("stale", "hard", "soften", "dog", "boot", "steak", "meat"),
          bias=2),
    entry("cake-fault",
          (("cake", "cakes", "sponge", "sponges", "loaf cake", "victoria sponge", "fairy cakes",
            "cupcakes", "batter", "birthday cake"),
           ("domed", "dome", "domes", "doming", "sunken middle", "cracked", "cracks",
            "cracking", "crack", "eggy", "tastes of egg", "taste of egg", "smells of egg",
            "rise evenly", "rises evenly", "risen evenly", "uneven", "unevenly", "lopsided",
            "soggy bottom", "tunnels", "tunnelling")),
          _cake_fault,
          avoid=("heavy", "dense", "sank", "sunk", "did not rise", "didnt rise", "dry", "stale",
                 "keep", "keeps", "last", "lasts", "fridge", "freezer", "freeze", "iced",
                 "icing", "decorate", "decorating"),
          bias=2),
    entry("fix-onion",
          (("onion", "onions"), ("burn", "burning", "burnt", "catch", "catching", "sticks")),
          "Turn the heat down to medium, add a little more oil, and splash in water whenever they "
          "start to catch; stir them every minute or two. Sweet onions want 8 to 10 minutes of "
          "gentle cooking — hot and fast is what burns them."),
    entry("fix-stirfry",
          (("stir fry", "stir-fry", "stirfry", "wok"),
           ("soggy", "watery", "limp", "steaming", "not crispy", "goes soft")),
          "A soggy stir-fry is a crowded pan: cook it in two batches over the highest heat you have, "
          "dry the vegetables well first, and add any sauce only at the very end off the heat."),
    entry("reheat-chicken", (("chicken", "turkey"),
                             ("reheat", "reheating", "reheated", "microwave", "warm up", "hot")),
          ("Yes, once, and until it is piping hot all the way through - steam rising and no cold "
           "spot in the middle. Keep cooked chicken in the fridge no more than 3 days, don't "
           "reheat it twice, and bin it if it has been out of the fridge for more than 2 hours.")),
    entry("refreeze-meat", (("meat", "mince", "chicken", "beef", "pork", "sausages", "fish"),
                            ("freeze", "freezer", "refreeze", "re-freeze", "refrozen", "freezing")),
          ("Only if it thawed in the fridge: that meat can go back in the freezer, though it will "
           "be a bit drier. Anything that thawed on the worktop or in a warm kitchen should be "
           "cooked and eaten now - cooking it first is what buys you extra days, not refreezing "
           "it raw."),
          ask=("refreeze", "re-freeze", "refrozen", "again", "back", "second time", "thawed",
               "defrosted"), bias=2),
    entry("honey-keeps", (("honey",),
                          ("go off", "gone off", "out of date", "keep", "keeps", "kept",
                           "last", "lasts", "crystallised", "crystalised", "crystallized",
                           "crystals", "hard", "hardened", "gone hard", "cloudy", "solid",
                           "gone solid", "thick", "gone thick", "granular", "grainy", "sugary",
                           "sugar crystals", "set in the jar", "store", "storing",
                           "still ok", "is it ok", "safe to eat", "use by",
                           "fridge", "cupboard",
                           "still good", "past the date", "after the", "years", "expired",
                           "best before")),
          ("Honey does not really go off - a jar keeps for years: honey that clouds or sets hard "
           "has crystallised rather than spoiled, and both are normal. Stand the jar in a bowl of "
           "hot water to loosen it, and keep it in a cupboard with the lid on. The one rule is no "
           "honey for a baby under a year, because of the botulism risk.")),
    entry("honey-baby", (("honey", "honey on", "honeys"),
                         ("baby", "babies", "baby's", "babys", "under one", "under 1", "infant",
                          "toddler", "toddlers", "month old", "months old", "weaning", "weaned",
                          "dummy", "one year old", "two year old", "three year old", "2 year old",
                          "3 year old", "newborn", "6 month", "7 month", "8 month", "9 month",
                          "10 month", "11 month")),
          _honey_age, bias=2),
    entry("honey-cough", (("honey",), ("cough", "coughs", "sore throat", "scratchy throat",
                                       "tickly", "cold", "colds", "flu", "sniffles")),
          ("A spoonful of honey is as good as any over-the-counter cough syrup for a cough or a "
           "scratchy throat, and it is the one thing the NHS suggests first: a teaspoon straight, "
           "or in a warm drink with lemon. Never under a year old, because of the botulism risk. "
           "See a doctor if it lasts more than three weeks or comes with a fever."), bias=1,
          avoid=("cold sore", "cold sores", "herpes", "lip", "lips", "blister", "blisters",
                 "honey cake", "honeycomb", "honey glaze", "honey roast", "honey mustard",
                 "recipe", "bake", "baking", "cake", "muffin", "porridge")),
    entry("raw-dough", (("cookie dough", "cake batter", "raw dough", "dough", "batter",
                         "cake mix", "cookie mixture"),
                        ("eat", "safe", "taste", "lick", "spoon", "raw")),
          ("Best not: raw flour and raw egg are both a real risk, and flour is the one people "
           "forget - it can carry E. coli straight from the field. Normal dough is for the oven; "
           "if you want to eat it raw, use a recipe with heat-treated flour and no egg.")),
    entry("raw-egg", (("raw egg", "raw eggs", "runny egg", "runny eggs", "soft boiled",
                       "dippy egg", "dippy eggs"),
                      ("eat", "safe", "ok", "okay", "fine", "pregnant", "risk")),
          ("In the UK, eggs with the British Lion mark are fine raw or runny, even for pregnant "
           "women, babies and older people, because the hens are vaccinated. Eggs without the stamp "
           "should be cooked until the white and yolk are solid. Anything with raw egg in it - mayo, "
           "mousse, homemade ice cream - should be kept in the fridge and eaten within a day or two."),
          avoid=("dog", "dogs", "puppy", "pup", "cat", "cats", "kitten", "kittens", "pet", "pets",
                 "rabbit", "hamster", "guinea pig", "budgie", "parrot", "horse"),
          bias=1),
    entry("wash-chicken", (("chicken", "turkey"), ("wash", "washing", "rinse", "rinsing",
                                                    "clean")),
          ("Don't: washing raw chicken splashes bacteria over the sink, the taps and anything "
           "within a metre, and cooking kills them anyway. Pat it dry with kitchen paper, bin the "
           "paper, wash your hands, and cook it right through."), bias=1),

    entry("cook-words",
          (tuple(COOK_WORDS),
           DEFINITION_WORDS + ("how do i", "how do you", "how to", "how should i")),
          _cook_word, bias=1, avoid=NOT_A_COOKING_LINE,
          ask=DEFINITION_WORDS + ("how do i", "how do you", "how to", "how should i")),
    entry("meal-sides",
          (("go with", "goes with", "going with", "goes nicely", "goes well with",
            "have with", "eat with", "have it with", "side for", "sides for", "side dish",
            "side dishes", "serve with", "serving with", "to serve with", "alongside",
            "what side", "which side", "pairs with",
            "pairs best with", "pairs well with", "pairs nicely with", "goes best with",
            "to go with", "to have with", "to eat with", "serve alongside", "go alongside",
            "seasoning for", "seasoning", "spice for", "spices for", "spice with",
            "spices with", "herb for", "herbs for", "herb with", "herbs with", "rub for",
            "what spice", "what spices", "what herb", "what herbs", "which spice",
            "which spices", "which herbs", "what seasoning", "flavour for",
            "how do i season", "how to season", "how should i season", "season a",
            "season the", "season it", "what to put on", "put on the",
            "dry rub", "spice rub", "rub recipe", "what goes in a rub"),
           ("chicken", "roast", "sausages", "sausage", "lamb", "beef", "steak", "halloumi",
            "feta", "prawns", "prawn", "shrimp",
            "salmon", "fish", "cod", "curry", "chilli", "daal", "dal", "pasta",
            "spaghetti", "lasagne", "lasagna", "burger", "burgers", "barbecue", "bbq",
            "turkey", "ham", "gammon", "pork", "pie", "stew", "casserole", "soup",
            "risotto", "paella", "hot dogs", "rice", "mash", "mashed potato", "potato",
            "potatoes", "chips",
            "corn", "sweetcorn", "corn on the cob",
            "tofu", "mince", "ribs", "tomato", "tomatoes", "cherry tomatoes", "pumpkin",
            "butternut") + PAIRING_FOODS + PLAN_NAMES),
          _sides,
          ask=("what", "which", "side", "sides", "serve", "serving", "go", "goes",
               "going", "with", "alongside", "suggest", "recommend", "any", "some",
               "for", "spice", "spices", "herb", "herbs", "seasoning", "rub", "flavour"),
          avoid=("sofa", "curtain", "paint", "carpet", "shirt", "jumper", "wine",
                 "close season", "closed season", "fishing season")),
    entry("bakes",
          (("chocolate cake", "chocolate sponge", "chocolate gateau", "victoria sponge",
            "sponge cake", "victoria sandwich", "plain sponge", "brownies", "brownie",
            "chocolate brownies", "scones", "scone", "cheese scones", "white bread", "bread",
            "loaf of bread", "bread dough", "banana bread", "banana loaf", "flapjack",
            "flapjacks", "cookies", "cookie", "chocolate chip cookies", "crumble", "fruit crumble",
            "apple crumble", "pastry",
            "shortcrust pastry", "pie crust",
            "sourdough", "sourdough bread", "soda bread", "soda loaf", "wholemeal bread",
            "brown bread", "bread maker", "bread machine", "breadmaker",
            "gluten free bread", "gluten-free bread"),
           ("make", "makes", "making", "bake", "baking", "recipe", "recipes", "cook",
            "cooking", "from scratch", "whats")),
          _bake,
          avoid=("rise", "rising", "prove", "proving", "wont", "won't", "went wrong", "blunt",
                 "knife", "knives", "mouldy", "mould", "soggy", "stodgy", "burnt", "stuck",
                 "sharp", "stale", "starter",
                 "tough", "chewy", "rubbery", "gummy", "pale", "sank",
                 "didnt rise", "didn't rise", "not risen", "raw in the middle",
                 "underbaked", "under baked", "is crumbly", "too crumbly", "so crumbly",
                 "came out crumbly", "come out crumbly", "went crumbly", "falls apart",
                 "falling apart",
                 "store", "storing", "storage", "keep", "keeps", "keeping", "keep fresh",
                 "stays fresh", "last", "lasts", "fridge", "freezer", "freeze", "frozen",
                 "bread bin",
                 "nail", "nails", "toenail", "toenails", "fingernail", "fingernails",
                 "soda", "without",
                 "bread maker worth", "worth a bread maker",
                 "buy a bread maker", "buying a bread maker", "buy a bread machine")
                 + NO_SUGAR,
          bias=1),
    entry("meal-plan",
          (("week", "weekly", "weeknight", "weeknights", "meal plan", "meal planning",
            "plan the week", "plan for the week", "food shop", "food shopping",
            "shop for the week", "menu", "batch", "batch cook", "batch cooking",
            "batches", "plan", "planning",
            "eat well", "eat cheap", "eat healthy", "eat healthily", "eat properly",
            "eating well", "eating cheap", "eating healthy", "eating healthily",
            "eat for less", "small budget", "tight budget", "on a budget", "cheap food",
            "cheap meals", "student", "students", "skint", "broke"),
           ("meal", "meals", "dinner", "dinners", "cook", "cooking", "cheap", "budget",
            "shop", "shopping", "batch", "ideas", "feed", "family")),
          _meal_plan,
          ask=("week", "weekly", "plan", "planning", "menu", "batch", "shop", "shopping",
               "cheap", "budget", "ideas", "what", "any", "suggest", "help"),
          avoid=("how long", "temperature", "oven", "recipe", "supermarket open",
                 "opening times", "delivery", "online shop",
                 "wedding", "weddings", "getting married", "hen do", "stag do", "venue",
                 "registrar", "bride", "groom", "guest list", "guests",
                 "away", "weekend away", "holiday", "holidays", "trip", "weekend break",
                 "city break", "getaway", "night away", "days away", "hotel", "hostel",
                 "flight", "flights", "abroad", "day out", "days out",
                 "week off", "weeks off", "week off work", "few days off", "time off")),
    entry("time-budget",
          (("minutes", "minute", "mins", "half an hour", "quarter of an hour", "hour"),
           ("dinner", "cook", "cooking", "meal", "meals", "tea", "supper", "lunch", "eat",
            "eating", "make", "making", "food", "tonight", "hurry", "hungry",
            "recipe")),
          _time_budget, bias=1,
          ask=("cook", "cooking", "dinner", "tea", "meal", "eat", "make", "food", "tonight",
               "quick", "hurry", "hungry", "recipe"),
          avoid=("how long", "should i cook", "temperature", "oven", "keep", "leftover",
                 "reheat", "freeze", "boil", "bake",
                 "quick question", "quick q",
                 "what can i cook", "what can i make", "what should i cook",
                 "what should i make", "what could i cook", "what could i make")),
    entry("meal-ideas",
          (("meal", "dinner", "supper", "tea", "tea time", "for tea", "recipe", "what can i cook",
            "what can i make", "what should i cook", "what should i make", "what shall i cook",
            "what shall i make", "what to cook", "what to make", "meal ideas",
            "what to eat", "what should i eat", "what shall i eat", "what can i eat",
            "what could i eat",
            "what could i cook", "what could i make",
            "dinner ideas",
            "what can you cook", "what can you make", "what can you help me cook",
            "what can you help me make", "can you help me cook", "can you help me make",
            "help me cook", "help me make",
            "meal plan", "meal plans", "meal planning", "plan meals", "plan my meals",
            "planning meals", "meals for the week", "plan for the week", "weekly meals",
            "food plan", "food for the week",
            "fridge", "freezer", "cupboard"),
           ("make", "cook", "quick", "easy", "ideas", "fancy", "tonight", "use up",
            "no time", "no spare time", "in a rush", "in a hurry", "not enough time",
            "too fancy", "nothing fancy", "fancy something", "something fancy",
            "can i have", "should i have", "shall i have", "cheap", "need", "want",
            "plan", "planning", "budget", "week", "weekly",
            "what is for", "whats for", "what's for", "what to have", "what should we have",
            "what shall we have", "what could we have", "what can we have", "what are we having",
            "what should i have for", "what shall i have for", "what is for dinner",
            "and not much else", "and nothing else", "nothing much else in", "and thats it",
            "not much else", "nothing else", "all i have", "all ive got",
            "all i've got", "only got", "only have", "only have got", "thats all i have",
            "that is all i have", "thats all ive got", "this is all i have",
            "for two", "for 2", "for three", "for 3", "for four", "for 4", "for five",
            "for 5", "for six", "for 6", "for eight", "for 8", "for a family",
            "guests", "guest",
            "dinner", "tea", "supper", "lunch")),
          _meal_ideas,
          ask=("what", "shall", "should", "any", "can i", "ideas", "idea", "anything",
               "suggest", "help", "quick", "easy", "fast", "cheap", "tonight", "fridge",
               "need", "want", "decide", "plan", "planning", "budget",
               "having",
               "no time", "not enough time", "no spare time", "short of time", "short on time",
               "pressed for time", "pushed for time", "dont have time", "don't have time",
               "didnt have time", "didn't have time", "hardly any time", "not much time",
               "in a rush", "rushed", "in a hurry", "last minute"),
          avoid=("how long", "temperature", "oven", "portion", "allergic",
                 "buy", "buying", "bought", "new fridge", "new freezer", "repair", "mend",
                 "broken", "not cold", "not freezing", "warm", "thermometer", "shelf", "shelves",
                 "seal", "seals", "clean", "cleaning", "smell", "smells", "defrost the fridge",
                 "power cut", "empty the fridge", "freezer burn", "frozen solid",
                 "wear", "wearing", "wore", "dress", "dress code", "outfit", "bring",
                 "roll", "rolls", "lady", "jacket",
                 "what time", "when is", "what did i", "how many",
                 "without meat", "meat free", "meat-free", "meatless",
                 "less meat", "less red meat",
                 "cant eat dinner", "cant eat anything", "cant eat much", "cant eat today",
                 "cant eat tonight", "cant eat at the moment", "cannot eat dinner",
                 "can not eat dinner", "cant face", "cannot face", "no appetite",
                 "not hungry", "off my food", "cant stomach", "cannot stomach",
                 "allergy", "breakfast", "brekkie", "brekky", "chicken thigh", "chicken thighs",
                 "chicken breast", "whole chicken", "leftover rice",
                 "left over rice", "leftover pasta", "left over pasta",
                 "sleep", "sleeping", "sleepy", "awake", "before bed", "caffeine",
                 "brew", "brewed", "brewing", "steep", "steeped", "bitter",
                 "chamomile", "green tea", "black tea", "tea bag", "tea bags",
                 "cup of tea", "mug of tea",
                 "in it", "with it", "air fryer", "slow cooker", "pressure cooker",
                 "in this", "in that", "in mine",
                 "make a budget", "make my budget", "set a budget", "budget plan",
                 "make a plan for my money", "plan my money",
                 "wedding", "weddings", "reception", "restaurant", "hotel", "canteen",
                 "on the plane", "at school", "at christmas", "christmas day", "christmas eve",
                 "in france", "in spain", "in italy", "in greece", "in portugal", "in mexico",
                 "in japan", "in china", "in india", "in thailand", "in america", "abroad",
                 "dinner vegetarian", "dinner vegan", "dinner no meat",
                 "vegetarian dinner", "vegan dinner", "plant based dinner",
                 "no meat for dinner", "dinner with no meat") + _NOT_MINE),

    entry("breakfast-skip", (("skip", "skipping", "skipped", "miss", "missed", "not eating",
                              "no breakfast", "not hungry", "never eat", "eat no",
                              "dont have breakfast", "don't have breakfast", "without breakfast",
                              "necessary", "important", "do i have to", "do i need to",
                              "must i", "is it ok", "is it bad", "is skipping"),
                             ("breakfast", "brekkie", "brekky", "meal in the morning",
                              "morning meal")),
          "Skipping breakfast is not harmful for most adults: what matters is the food you eat "
          "over the whole day, not the hour you start. Don't skip it if you are pregnant, on "
          "insulin or a diabetes tablet that can cause hypos, or a child - and eat something if "
          "you get shaky or headachy mid-morning.",
          bias=1),
    entry("breakfast-ideas",
          (("breakfast", "brekkie", "brekky"),
           ("idea", "ideas", "what", "good", "quick", "easy", "make", "have", "eat",
            "healthy", "filling", "should", "vegan", "vegetarian", "veggie",
            "plant based", "dairy free", "gluten free", "no eggs", "no dairy", "no meat",
            "allergic", "allergy", "intolerant", "doesnt eat", "doesn't eat", "cant eat",
            "can't eat")),
          _breakfast_ideas,
          avoid=("won't", "wont", "refuse", "refuses", "buffet", "hotel", "time", "late",
                 "skip", "skipping", "is it ok", "necessary", "most important", "is it bad",
                 "is it true")),
    entry("lunch-ideas",
          (("lunch", "packed lunch", "lunchbox", "lunch box", "school lunch", "work lunch"),
           ("idea", "ideas", "quick", "easy", "make", "have", "eat", "what", "should",
            "good", "healthy", "pack", "packed",
            "bring", "bringing", "worth", "own lunch")),
          _lunch_ideas_after_a_no,
          avoid=("rice", "pasta", "leftover rice", "left over rice", "potato", "potatoes",
                 "egg", "eggs", "chicken", "tuna", "cheese", "mince", "sausages", "bacon",
                 "beans", "chickpeas", "lentils", "tofu", "noodles", "couscous", "quinoa",
                 "salad", "soup", "sandwich", "bread", "ham", "fish",
                 "skipping", "skip", "no time", "missed", "forgot",
                 "say", "talk", "talk about", "conversation", "small talk",
                 "just having", "having my lunch", "just had lunch", "had my lunch",
                 "on my lunch", "eating my lunch",
                 "coming over", "come over", "coming round", "come round",
                 "over for", "round for") + _ON_A_FLIGHT,
          guard=_one_persons_lunch),
    entry("lunch-no-sandwich",
          (("lunch", "lunches", "lunchbox", "lunchboxes", "lunch box", "lunch boxes",
            "packed lunch", "packed lunches", "school lunch", "school lunches", "work lunch",
            "pack up", "packed up"),
           NO_SANDWICH),
          _no_sandwich_lunch, bias=3,
          avoid=("how long", "keep", "keeps", "keeping", "freeze", "frozen", "recipe",
                 "recipes", "calories", "healthy", "allergy", "allergic", "gluten",
                 "coeliac", "celiac") + _ON_A_FLIGHT),



    entry("snack-ideas",
          (("snack", "snacks", "snacking", "nibbles", "between meals", "in between meals"),
           ("what", "whats", "idea", "ideas", "can i have", "could i have", "should i have",
            "shall i have", "have for", "healthy", "good", "nice", "best", "quick", "easy",
            "instead", "alternative", "alternatives", "suggest", "suggestions", "fancy",
            "filling", "fill", "keep me going", "small", "light",
            "any", "not", "arent", "aren't", "take to work", "at work", "for work")),
          _a_snack,
          avoid=("stop", "stopping", "cant stop", "can't stop", "why do i", "why am i",
                 "help me", "how do i stop", "break the habit", "habit", "at night", "night",
                 "midnight", "late", "evening", "after dinner", "in bed",
                 "baby", "babies", "toddler", "child", "children", "kid", "kids", "son",
                 "daughter", "weaning", "wean", "nursery", "school",
                 "buy", "buying", "shop", "shopping", "supermarket", "price", "cost",
                 "cheapest", "brand", "best before",
                 "party", "guests", "buffet", "meeting", "christmas", "birthday", "film",
                 "cinema", "road trip", "flight",
                 "drive", "driving", "car", "journey", "train", "plane", "picnic", "camping",
                 "packed lunch", "lunchbox", "lunch box",
                 "tea", "coffee", "drink", "juice", "cola"),
          bias=1),

    entry("lunch-exclusion",
          (("lunch", "packed lunch", "lunchbox", "lunch box", "school lunch", "work lunch"),
           ("dont eat", "don't eat", "do not eat", "cant eat", "can't eat", "cannot eat",
            "doesnt eat", "doesn't eat", "does not eat", "wont eat", "won't eat",
            "no meat", "meat free", "meat-free", "no cheese", "no dairy", "no eggs", "no egg",
            "no fish", "no tuna", "no ham", "no nuts", "vegetarian", "veggie", "vegan",
            "plant based", "allergic", "allergy", "intolerant",
            "dairy free", "gluten free", "nut free", "egg free",
            "off dairy", "off meat", "off gluten", "off fish", "off eggs")),
          _lunch_ideas_after_a_no, bias=2,
          avoid=("how long", "left out", "freeze", "recipe") + _ON_A_FLIGHT),
    entry("baby-food-for-a-grown-up",
          (("baby rice", "baby porridge", "baby cereal", "baby food", "baby foods",
            "baby puree", "baby purees", "baby yoghurt", "baby biscuit", "baby biscuits",
            "baby pouch", "baby pouches", "baby jar", "baby jars", "jars of baby food",
            "jar of baby food", "baby pasta"),
           ("eat", "eating", "eaten", "adult", "adults", "grown up", "grown ups",
            "grownup", "for adults", "for me", "myself", "healthy", "any good",
            "ok for me", "is it ok", "bad for me", "good for you", "good for me",
            "bad for you", "waste", "finish")),
          "Yes, it is just food: baby rice is finely ground rice, and the jars are ordinary fruit "
          "or vegetables cooked soft with no salt or sugar added, so there is nothing in them a "
          "grown-up needs to avoid. They are bland on purpose and cost several times what the same "
          "weight of rice or fruit does, so finishing a jar is fine and buying them for yourself is "
          "not worth it.",
          avoid=("my baby", "a baby", "baby have", "baby has", "give my baby", "infant",
                 "wean", "weaning", "toddler",
                 "6 months", "six months", "month old", "months old", "newborn",
                 "how much", "how many", "portion", "recipe", "how long", "freeze"),
          bias=3),
    entry("nut-allergy",
          (("nut", "nuts", "peanut", "peanuts"),
           ("allergic", "allergy", "allergies", "eat", "avoid", "safe")),
          _nut_free,
          guard=not_a_present,
          avoid=("dog", "dogs", "cat", "cats", "puppy", "kitten", "pet", "pets", "vet",
                 "every day", "everyday", "a day", "per day", "how often", "how much",
                 "too much", "good for you", "bad for you", "healthy", "fattening",
                 "calories", "lose weight", "gain weight",
                 "breastfeeding", "breast feeding", "breastfeed", "nursing", "lactating",
                 "chestfeeding", "while feeding")),
    entry("vegan-main", ("vegan", ("main", "dinner", "meal", "cook", "ideas", "make")),
          "A chickpea and spinach curry is easy and filling: fry onion, garlic, ginger and spices, "
          "add a tin of tomatoes and a tin of chickpeas, simmer 15 minutes and stir spinach through "
          "at the end. Serve it with rice, and check the stock cube is vegan."),
    entry("vegetarian-main", ("vegetarian", ("main", "dinner", "meal", "cook", "ideas", "make",
                                             "party", "guests", "cooking")),
          "A roast vegetable and feta traybake is hard to beat: chop peppers, red onion, "
          "courgette and sweet potato, toss in oil, salt and thyme, roast at 200C for 35 minutes, "
          "then crumble feta over and give it 10 more. Serve with couscous and a sharp green salad."),
    entry("less-meat",
          (("meat", "meatless", "meat free", "meat-free", "plant based", "plant-based",
            "vegetarian", "veggie", "pulses"),
           ("less", "fewer", "cut down", "cut back", "cutting down", "cutting back", "reduce",
            "reducing", "without", "free", "swap", "swapping", "drop", "dropping", "give up",
            "trying", "start", "started", "tips", "ideas", "help", "advice", "plan", "plans")),
          "Swap rather than subtract: use lentils or a tin of beans for half the mince in a ragu, "
          "mushrooms for the other half, and chickpeas where a curry had chicken, and nobody at the "
          "table notices. Two meat-free dinners a week is easier to keep than a rule; keep the "
          "protein up with eggs, beans, lentils, tofu and cheese, which is the part people get wrong.",
          ask=("how", "what", "any", "should", "tips", "help", "trying", "want", "idea", "ideas",
               "can", "will", "kids", "children", "family", "week", "meals"),
          bias=2,
          avoid=("doesnt eat meat", "does not eat meat", "dont eat meat", "do not eat meat",
                 "doesnt eat any meat", "dont eat any meat", "no meat please", "no meat though",
                 "she is vegetarian", "hes vegetarian", "is a vegetarian", "vegetarian guest",
                 "dog", "dogs", "cat", "cats", "puppy", "kitten", "pet", "pets", "vet", "quorn",
                 "cook with chicken", "cook with beef", "cook with mince", "cook with meat",
                 "cook with lamb", "cook with pork", "cook with bacon", "cook with sausages",

                 "cook with fish", "cook with turkey",
                 "im vegetarian", "im veggie", "im vegan", "i am vegetarian", "i am veggie",
                 "i am vegan", "im a vegetarian", "im a veggie", "im a vegan",
                 "ive been vegetarian", "vegetarian for years",
                 "a vegetarian meal", "a vegetarian dinner", "a vegetarian main",
                 "a vegetarian recipe", "some vegetarian", "vegetarian meal ideas",
                 "vegetarian dinner ideas", "vegetarian main", "vegetarian recipe",
                 "a veggie meal", "a veggie dinner", "some veggie", "veggie meal ideas",
                 "a meat free meal", "a meat-free meal", "a meat free dinner",
                 "a meat-free dinner", "something vegetarian", "anything vegetarian")),
    entry("instead-of-mince",
          (("mince", "minced beef", "ground beef", "chicken", "beef", "meat"),
           ("instead", "instead of", "replace", "replacement", "substitute", "substitutes",
            "swap", "alternative", "without")),
          "Swap in pulses: red lentils for mince (a mug of them and a splash more stock, "
          "20 minutes), or a tin of green lentils and chopped mushrooms for the texture, and "
          "chickpeas, tofu or big flat mushrooms where there was chicken. Season it the way you "
          "would the meat, with stock, soy or paprika, and the swap goes unnoticed.",
          avoid=("dog", "dogs", "cat", "cats", "puppy", "pet", "pets", "raw", "freeze", "frozen",
                 "thaw", "thawed", "defrost", "reheat", "leftover", "leftovers", "how long",
                 "safe", "gone off", "off", "meal", "meals", "dinner", "dinners", "cheap",
                 "recipes", "recipe", "ideas", "menu", "veg", "vegetarian", "vegan")),
    entry("use-a-leaner-mince",
          (("turkey mince", "chicken mince", "quorn mince", "soya mince", "soy mince",
            "lean mince", "5% mince", "turkey breast mince", "vegan mince", "veggie mince"),
           ("can i use", "can i swap", "use", "instead", "swap", "works", "work",
            "in chilli", "in a chilli", "in spag bol", "in spaghetti bolognese", "in bolognese",
            "in lasagne", "in a lasagne", "in cottage pie", "in a cottage pie", "in ragu")),
          "Yes, weight for weight, and it needs a hand: turkey and chicken mince are leaner than "
          "beef, so brown them in a tablespoon of oil and add a splash more stock than the recipe "
          "says, or they go dry and chalky. Quorn and soya mince are a straight swap too - use "
          "the same volume, add stock, and give them fifteen minutes rather than forty. In a "
          "chilli or a bolognese nobody notices.",
          avoid=("dog", "dogs", "cat", "cats", "puppy", "pet", "raw", "freeze", "frozen",
                 "defrost", "reheat", "how long", "safe", "gone off", "christmas", "roast",
                 "stuffing", "carve", "whole bird", "thaw")),

    entry("beans-kids",
          (("beans", "lentils", "chickpeas", "peas"),
           ("kids", "children", "child", "toddler", "fussy", "hate", "hates", "wont eat",
            "won't eat", "refuse", "refuses", "faddy")),
          "Mash them in rather than serve them whole: beans or lentils blended into a tomato sauce "
          "or a shepherd's pie disappear, and peas or sweetcorn folded through rice do too. Put the "
          "new thing next to something they already eat, no bargaining and no second dinner, and "
          "keep offering it - it can take eight or ten tries before a child accepts a food.",
          avoid=("allergic", "allergy", "rash", "wind", "gas", "bloating", "dog", "dogs", "cat",
                 "cats", "puppy", "kitten")),
    entry("cook-tofu",
          ("tofu", ("cook", "cooking", "crispy", "crisp", "taste", "tasteless", "fry", "fried",
                    "bake", "marinade", "marinate", "press", "squeaky", "nice")),
          "Press it first: wrap the block in kitchen paper, weight it down for 15 minutes, then "
          "cube it and toss it in cornflour. Fry in a hot pan with a little oil until golden on "
          "two sides, and stir the sauce in off the heat - tofu added to a wet pan steams and stays "
          "soft. It is meant to taste of nothing, so it takes on whatever it is cooked with."),
    entry("protein-no-meat",
          ("protein", ("without meat", "no meat", "no meat or fish", "meat free", "meat-free",
                       "plant based", "plant-based", "vegan", "vegetarian", "enough",
                       "get enough", "will they",
                       "cheap", "cheapest", "budget", "afford", "affordable", "source",
                       "sources", "complete",
                       "what should i eat", "what should i have", "what do i eat",
                       "what can i eat", "what to eat", "what should i be eating",
                       "what foods", "what food", "which foods", "which food",
                       "eat for protein", "eat to get protein", "foods for protein",
                       "high in protein", "protein rich", "protein-rich", "lots of protein",
                       "good protein", "best protein", "what has protein")),
          _protein,
          avoid=("muscle", "muscles", "gym", "bulk", "bulking", "whey", "shake", "shakes",
                 "bodybuilding", "gaining"),
          bias=2),
    entry("party-food-plan",
          (("party", "buffet", "picnic", "guests", "people coming", "friends coming",
            "baby shower", "baby showers", "bridal shower", "baby sprinkle"),
           ("food", "snacks", "nibbles", "finger food", "ideas", "cheap", "feed", "make",
            "cook", "cooks", "cooking", "serve", "serving")),
          "Cheap party food people actually eat: a big pot of chilli or a pasta bake, garlic bread, "
          "and a bowl of crisps and dips. For standing-up food, sausage rolls, cheese straws and "
          "fruit on sticks go further than anything fiddly.",
          ask=("party", "buffet", "picnic", "guests", "food", "snacks", "nibbles",
               "make", "makes", "making", "cook", "cooking", "serve", "serving", "feed"),
          bias=1,
          avoid=("cake", "decorations", "music", "playlist", "venue", "invite", "invitation",
                 "conversation", "small talk", "mingle", "mingling", "nobody to talk",
                 "know anyone", "networking", "talk to people",
                 "what to say", "talk about", "nervous", "strangers") + ("picnic", "picnics")),
    entry("kids-vegetables",
          (("toddler", "kid", "kids", "child", "children", "son", "daughter")
           + _AGE_WORDS,
           ("vegetables", "veg", "broccoli", "greens", "carrot", "carrots", "fussy")),
          _kids_veg,
          ask=("vegetables", "veg", "broccoli", "greens", "carrot", "carrots", "fussy",
               "blend", "blended", "blender", "puree", "pureed", "purée", "hide", "hidden",
               "sneak", "mask", "grate", "grated"),
          avoid=("dinner", "dinners", "tonight", "for tea", "quick", "recipe", "recipes",
                 "bean", "beans", "lentil", "lentils", "chickpea", "chickpeas", "pulses",
                 "husband", "wife", "partner", "boyfriend", "girlfriend", "my mum", "my dad",
                 "my mother", "my father", "my stepdad", "my stepmum", "my nan", "my gran"),
          bias=1),
    entry("cheese-board", ("cheese", ("board", "platter", "party", "guests")),
          "For six people, pick three or four cheeses: something soft like brie, a hard one like a "
          "mature cheddar, a blue, and something goat's or sheep's for variety. Add crackers, "
          "grapes, chutney and nuts, and take them out of the fridge an hour before."),
    entry("cook-a-staple", (_STAPLE_NAMES, STAPLE_ASK), _staple, bias=1,
          guard=_not_a_portion_ask,
          avoid=("play squash", "playing squash", "squash court", "game of squash",
                 "racquetball", "licence", "license", "licencing", "licensing", "permit",
                 "angling", "angler",
                 "rod", "tackle", "bait", "close season", "day ticket",
                 "tank", "tanks", "aquarium", "fish tank", "fish tanks", "fishbowl",
                 "fish bowl", "gravel", "dechlorinator",
                 "goldfish", "tropical fish", "koi", "betta", "guppy", "pet fish",
                 "feed the fish", "feed a fish", "feed my fish", "feed fish",
                 "feed the goldfish", "feeding the fish", "feeding fish", "fish flakes",
                 "hutch", "hutches", "cage", "cages", "guinea pig", "guinea pigs", "cavies",
                 "hamster", "hamsters", "budgie", "budgies", "pet", "pets", "bedding",
                 "look after", "care for", "what do i need", "need for", "need to buy",
                 "need to get", "need before",
                 "bond", "bonding", "bonded", "introduce them", "two rabbits",
                 "pet rabbit", "house rabbit", "as a pet",
                 "alone", "left alone", "on its own", "on her own", "on his own", "lonely",
                 "last", "lasts", "lasting", "uncooked", "airtight", "stale", "staleness",
                 "leftover", "leftovers", "left over", "go with", "goes with", "gone off",
                 "per person", "portion", "portions", "serving", "servings",
                 "freeze", "freezer", "refreeze", "reheat", "keep", "keeping", "store", "ratio",
                 "fridge", "refrigerator", "out of the fridge", "left out", "leave it out",
                 "leaving it out",
                 "beef stock", "chicken stock", "turkey stock", "ham stock", "lamb stock",
                 "pork stock", "fish stock", "vegetable stock", "veg stock", "bone broth",
                 "stock cube", "stock cubes", "stock pot", "stockpot",
                 "dry", "sticky", "stuck", "salty", "lumpy", "lumps", "gluey", "claggy", "soggy",
                 "watery", "microwave", "sunk", "pink", "burnt",
                 "scrambled", "scramble", "poach", "poached", "fried", "fry", "omelette",
                 "harvest", "harvesting", "pick", "picking", "picked", "lift", "lifting",
                 "dig up", "dig them up", "ripe", "ripen", "when are they ready",
                 "plant", "grow", "paddy", "field", "sick", "allergy", "allergic", "wine",
                 "patch", "veg patch", "vegetable patch", "plot", "allotment", "raised bed",
                 "raised beds", "kitchen garden", "sow", "sowing", "harvest", "crop", "crops",
                 "slimming", "calories", "syn", "syns", "points", "crispy", "roast",
                 "stop", "sticking", "sticks", "stuck together", "clumping", "clumps",
                 "boil over", "boils over", "boiling over", "boiled over",
                 "noodles", "noodle", "vermicelli",
                 "fish finger", "fish fingers", "fishfinger", "fishfingers",
                 "without butter", "without milk", "without dairy", "no butter", "no milk",
                 "dairy", "dairy free", "vegan", "mash", "mashed", "mashing",
                 "baby", "babies", "toddler", "weaning",
                 "wash", "washing", "rinse", "rinsing",
                 "soak", "soaks", "soaking", "soaked", "overnight", "quick soak", "no soak",
                 "fridge", "fridged", "last", "lasts", "frozen", "days", "weeks", "month",
                 "breathe", "breathes", "breathing", "underwater", "gills")),
    entry("potato-boil",
          (("potato", "potatoes", "new potatoes", "spud", "spuds", "tattie", "tatties"),
           ("boil", "boiling", "how long", "minutes", "tender", "soft", "done",
            "cook", "cooking", "make",
            "mushy", "mush", "soggy", "watery", "fall apart", "falls apart", "falling apart",
            "fell apart", "break up", "breaks up", "breaking up", "broke up", "crumbly",
            "disintegrate", "disintegrates")),
          "Boil them in salted water: 10 to 12 minutes for small new potatoes, 15 to 20 for chunks, "
          "20 to 25 for whole medium ones. A knife should slide in with no resistance at all, and "
          "drain them the moment it does, or they go watery. If they keep going mushy, it is "
          "usually the potato rather than the pan: floury ones (Maris Piper, King Edward, Desiree) "
          "break up in water and are for mashing and roasting, so boil the waxy ones (Charlotte, "
          "Nicola, any new potato) and keep the water at a gentle simmer rather than a rolling "
          "boil, and do not stir them.",
          avoid=("keep", "keeps", "keeping", "store", "storing", "last", "lasts", "gone off",
                 "sprout", "sprouting", "sprouts", "mouldy", "fridge", "freezer",
                 "green", "greening", "gone green", "gone soft",
                 "roast", "roasting", "roasted", "oven", "jacket", "baked", "bake",
                 "gratin", "dauphinoise", "salad", "sweet", "scalloped", "wedges", "crispy",
                 "chips",
                 "microwave", "microwaved", "microwaving", "air fryer", "air fry", "airfryer",
                 "air fried")),
    entry("hot-pan-cool",
          (("pan", "pans", "saucepan", "frying pan", "wok", "skillet", "pot", "enamel pan",
            "cast iron", "baking tray", "roasting tin",
            "cake tin", "tins", "loaf tin", "muffin tin", "springform", "baking dish",
            "oven dish", "casserole dish", "dutch oven", "stock pot", "griddle", "chip pan",
            "pie tin", "tray"),
           ("cold water", "cold tap", "in the sink", "into the sink", "under the tap", "rinse",
            "cool it down", "cool down", "cooling down", "cooling it", "cool my pan",
            "cool the pan", "cool a pan", "ice water", "quench", "thermal shock", "soak it",
            "run it under", "let it cool", "crack", "cracked", "plunge",
            "straight away", "right away", "hot pan",
            "cool before washing", "cool it before washing", "let it cool before washing",
            "let the pan cool before", "cool the pan before", "before washing",
            "before i wash", "before washing up", "cool it first", "cool first",
            "warm water",
            "will it warp", "will cold water", "warp my pan", "warp it", "warping my pan")),
          "Give a very hot pan five minutes before it meets cold water: a thin stainless or "
          "aluminium pan can warp, and enamel or cast iron can crack. Warm water first, or fill the "
          "sink and set the pan in it rather than running the tap straight onto it. Deglazing on the "
          "hob with a splash of stock or wine is fine - it is the cold plunge from a screaming pan "
          "that is not.",
          avoid=("glass hob", "worktop", "counter", "countertop", "granite", "quartz", "marble",
                 "laminate", "wooden board", "chopping board", "trivet", "glass table",
                 "glass top", "glass-top",
                 "isolation valve", "stopcock", "stop cock", "mixer tap", "kitchen tap",
                 "dripping tap", "leaking tap", "tap washer", "cistern", "boiler",
                 "hob", "hobs", "gas hob", "electric hob", "on the hob", "ring", "on the ring",
                 "wooden table", "wood table", "the table", "work surface", "worksurface",
                 "benchtop", "on the side", "rested the hot", "rested a hot", "put the hot",
                 "placed the hot", "set the hot", "stood the hot",
                 "heating", "radiator", "shower", "bath", "washing machine",
                 "where can i put", "where do i put", "where should i put", "where to put",
                 "where can i set", "what can i put it on",
                 "has warped", "already warped", "is warped", "gone warped", "it warped",
                 "wont sit flat", "doesnt sit flat", "doesn't sit flat", "spins on the hob",
                 "rocks on the hob",
                 "my pan warped", "warped after", "warped from", "pan has warped",
                 "pan is warped", "pan warped",
                 "dishwasher", "fridge", "freezer", "refrigerator"),
          ask=("can i put", "can i rinse", "is it ok to put", "is it safe to put", "should i rinse",
               "in cold water", "cold water", "under the tap", "before washing", "before i wash",
               "cool before", "cool it", "let it cool", "let the pan cool", "will it warp",
               "warp my pan", "warp it", "warp", "warping",
               "should i", "shall i", "is it safe", "safe to", "ok to", "okay to",
               "how do i cool", "how to cool", "how can i cool", "how do you cool",
               "cool my", "cool the", "cool a", "cool down"),
          bias=6),
    entry("hot-pan-surface",
          (("pan", "pans", "saucepan", "saucepans", "frying pan", "wok", "skillet", "pot", "pots",
            "griddle", "casserole", "baking tray", "roasting tin",
            "tray", "trays", "tin", "tins", "dish", "dishes", "kettle", "casserole dish",
            "cake tin", "loaf tin", "muffin tin", "baking dish", "dutch oven", "pie tin"),
           ("hot pan", "hot pans", "glass hob", "glass top", "ceramic hob", "induction hob",
            "where can i put", "where do i put", "where should i put", "where to put",
            "where can i set", "where can i stand",
            "worktop", "worktops", "counter", "countertop", "granite", "quartz", "marble",
            "laminate", "wooden worktop", "wood worktop", "glass table", "trivet", "table",
            "wooden table", "wood table", "the table", "work surface", "worksurface", "benchtop",
            "on the side", "chopping board", "wooden board", "straight off the hob", "off the ring",
            "hot tray", "hot roasting tin", "hot baking tray", "hot dish", "hot pot",
            "hot casserole", "hot kettle")),
          _the_hot_pan_place,
          avoid=("clean", "cleaning", "wash", "washing", "scrub", "soak", "burnt", "stain",
                 "stains", "cold water", "sink", "warp", "warped", "season", "seasoning",
                 "dishwasher",
                 "fridge", "freezer", "refrigerator",
                 "in a hot pan", "in the hot pan", "in a pan", "in the pan", "into the pan",
                 "into a hot pan", "chicken", "meat", "steak", "beef", "pork", "lamb",
                 "mince", "bacon", "sausage", "sausages", "fish", "salmon", "prawn",
                 "prawns", "egg", "eggs", "oil", "butter", "onion", "onions", "garlic",
                 "potato", "potatoes", "veg", "vegetables", "rice", "pasta", "noodles",
                 "sauce", "tofu", "mushroom", "mushrooms", "flour", "dough", "pancake"),
          ask=("can i put", "can i stand", "can i set", "where can i put", "where do i put",
               "is it ok to put", "is it safe to put", "put a hot", "where should i put",
               "what should i put", "i put", "i placed", "i set", "i stood", "i rested",
               "put the hot", "placed the hot", "set the hot", "stood the hot", "rested the hot",
               "put it on", "placed it on", "set it on", "what happens",
               "is that ok", "is that alright", "is that safe", "is it ok on", "is it safe on",
               "hot pan on", "hot tray on", "hot dish on", "hot pot on", "hot tin on",
               "does a hot", "will a hot", "can a hot", "can a hot pan",
               "ok on", "safe on", "alright on", "straight off", "off the oven"),
          guard=_a_hot_thing_is_being_set_down,
          bias=6),
    entry("pan-dry",
          (("pan", "pans", "saucepan", "saucepans", "pot", "pots", "wok", "skillet", "pan"),
           ("boiled dry", "boils dry", "boil dry", "boiling dry", "boiled away", "boils away",
            "all boiled away", "went dry", "dried out", "ran dry", "left it on", "left the pan",
            "forgot it", "forgot about it")),
          "Take it off the heat and let it cool where nobody will grab it - and do not put cold "
          "water in it while it is hot, because a hot dry pan can warp or crack and the steam "
          "spits. Once it has cooled, look at the base: a rainbow tint or a blue-black patch is "
          "the metal heat-tinted, which is fine and does not affect the cooking, while food stuck "
          "on lifts in a soak of hot water and a spoon of bicarbonate of soda. A pan that boiled "
          "dry with nothing in it usually only needs a wash, and one with milk or sugar in it "
          "wants the soak.",
          avoid=("how long", "how many", "what temperature", "buy", "best pan", "non stick",
                 "nonstick", "which pan", "recipe")),
    entry("chips-cook",
          (("chips", "oven chips", "frozen chips", "fries", "french fries"),
           ("cook", "cooking", "oven", "air fryer", "fryer", "best", "properly", "how long",
            "bake", "homemade", "perfect")),
          ("Frozen chips want 20 to 25 minutes at 200C (180C fan), turning once; an air fryer does "
           "them in 12 to 15 minutes at 200C, shaken once. Fresh-cut chips take 30 to 35. One "
           "layer with space between them, and salt when they come out: a crowded tray steams."),
          avoid=("temperature", "portion", "portions", "per person", "how much", "price", "buy",
                 "shop",
                 "freezer", "freeze", "refreeze", "defrost", "heating up", "reheat", "leftover",
                 "left over", "chip shop", "takeaway",
                 "healthy", "healthier", "unhealthy", "calorie", "calories", "fat", "fattening",
                 "nutrition", "good for", "cholesterol", "salt", "diet",
                 "from scratch", "scratch")),
    entry("leftovers-freeze",
          (("freeze", "freezing", "frozen", "defrost"),
           ("leftovers", "leftover", "curry", "stew", "soup", "mash", "mashed potato", "cooked",
            "rice", "bolognese")),
          "Most cooked food freezes well: cool it within two hours, pack it in portions and label "
          "the date. Eat it within three months for the best quality, defrost it in the fridge "
          "overnight and reheat it once until piping hot. Mashed potato freezes well but goes grainy "
          "if you reheat it in a microwave, so warm it through in a pan with a splash of milk. Rice "
          "is the one to be careful with: freeze it within an hour of cooking, not the next day."),
    entry("reheat-leftovers",
          (("reheat", "reheating", "reheated", "heat up", "heat it up", "warm up", "warm it up",
            "microwave"),
           ("leftovers", "leftover", "curry", "stew", "soup", "mash", "mashed potato", "bolognese",
            "takeaway", "pizza", "rice", "chicken", "fish", "pie", "pasta", "dinner", "plate",
            "food")),
          "Reheat it until it is piping hot all the way through, not just warm at the edges: a splash "
          "of water, a lid on, and a stir halfway so it heats evenly. In a microwave, cover it, heat "
          "in one-minute bursts, then let it stand two minutes; in a pan or an oven it wants about 20 "
          "minutes at 180C. You can reheat leftovers once only - chicken and rice are the two to be "
          "strictest with - so heat what you are going to eat and bin the rest.",
          ask=("reheat", "reheating", "reheated", "heat up", "heat it up", "warm up", "warm it up",
               "leftovers", "leftover", "curry", "stew", "soup", "mash", "mashed potato",
               "bolognese", "takeaway", "pizza", "rice", "chicken", "fish", "pie", "pasta",
               "dinner", "plate"),
          avoid=("bottle", "baby", "formula", "milk feed", "bread", "cake", "pizza")),
    entry("reheat-jacket",
          (("reheat", "reheating", "reheated", "heat up", "heat it up", "warm up", "crisp up",
            "reheat them"),
           ("jacket potato", "jacket potatoes", "baked potato", "baked potatoes")),
          "A jacket potato comes back best at 200C (180C fan): split it open, brush the cut faces "
          "with oil so they crisp, and give it about 20 minutes, or 8 to 10 if you only want it hot "
          "right through. Three minutes in the microwave and then 10 in the oven is quicker and "
          "nearly as good; on its own a microwave leaves the skin soft and leathery.",
          avoid=("salad", "tuna", "cheese", "filling", "keep", "keeps", "how long",
                 "still good", "gone off", "grow", "plant")),
    entry("reheat-pizza", (("pizza", "slice", "slices"),
                           ("reheat", "reheating", "heat up", "warm up", "cold", "leftover",
                            "left over", "next day", "soggy", "crispy")),
          "Dry heat, not the microwave: 200C for 8 to 10 minutes straight on the oven shelf, or in a "
          "covered frying pan on a low heat for 5 minutes - both give you a crisp base again. A "
          "microwave heats the water in the sauce and turns the base to leather, so only use it for "
          "10 seconds if you want it warm rather than good."),
    entry("freeze-anything", (_FREEZE_ASKS, _FREEZE_POINTING_WORDS),
          _freeze_food,
          ask=KEEP_ASK,
          avoid=("soup", "soups", "broth", "mashed potato", "mash", "refreeze", "refroze",
                 "re-freeze", "thawed", "defrost", "defrosting", "defrosted", "stew", "stews",
                 "casserole", "casseroles", "curry", "curries", "chilli", "chili", "bolognese",
                 "lasagne", "lasagna", "brain freeze", "brainfreeze", "instead", "instead of",
                 "substitute", "swap", "from frozen", "ice cream",
                 "leftover", "leftovers", "left over") + _FREEZE_AVOID,
          bias=0),
    entry("refreeze-food",
          (("refreeze", "refroze", "re-freeze", "freeze again", "frozen again"),
           ("mince", "meat", "chicken", "fish", "rice", "safe", "ok", "okay", "fine", "harm",
            "again",
            "food", "thawed", "defrosted", "has thawed", "thawed out")),
          "Cooked food can go back in the freezer once - cool it within two hours, rice within one, "
          "and rice should only be reheated once after that. Raw meat or fish turns on where it "
          "thawed: on the worktop or in a warm kitchen, cook it and eat it now, because it should "
          "not be frozen again - the thaw lets bacteria multiply and freezing does not undo that. "
          "Only meat or fish that thawed in the fridge can go back in, a bit drier than before.",
          avoid=("bread", "cake", "banana", "milk", "berries")),
    entry("vegetarian-guest", (("vegetarian", "veggie", "pescatarian", "no meat",
                                "doesnt eat meat", "doesn't eat meat", "does not eat meat",
                                "eat much meat", "much meat", "not much meat", "scarcely any meat",
                                "meat free", "meat-free"),
                               ("cook", "make", "dinner", "lunch", "menu", "idea", "ideas",
                                "coming", "guest", "guests", "round", "for")),
          ("Pick a dish that is good on its own rather than meat with the meat left out: a chickpea "
           "and spinach curry with rice, a mushroom and lentil lasagne, or a tray of roasted veg "
           "with feta and couscous. One proper veggie main plus the usual sides is plenty, and it "
           "is worth asking what they actually eat, because vegetarian covers a wide range."),
          avoid=("chicken", "beef", "pork", "lamb", "turkey", "mince", "bacon", "sausage",
                 "sausages", "ham", "fish", "prawns", "salmon", "steak", "chorizo",
                 "cheap", "cheaper", "skint", "broke", "budget", "money", "afford", "fiver"),
          bias=1),
    entry("diabetic-guest", (("diabetic", "diabetics", "diabetes", "type 1", "type 2",
                              "blood sugar", "sugar diabetes"),
                             ("cook", "cooking", "make", "making", "dinner", "lunch", "meal",
                              "menu", "idea", "ideas", "coming", "guest", "guests", "visiting",
                              "round", "over", "feed", "serve")),
          DIABETIC_PLATE,
          avoid=("what is", "reversible", "reverse", "cure", "cured",
                 "symptom", "symptoms", "diagnosed", "diagnosis", "test", "tests", "hba1c",
                 "insulin", "tablets", "metformin", "level", "levels", "high", "low",
                 "hypo", "hyper", "shaky", "dizzy", "thirsty", "weeing", "losing weight",
                 "how many carbs", "carbs a day", "calories", "how much sugar", "sugar free",
                 "sugar-free", "diet drink", "beer", "alcohol", "wine", "drink", "drinks",
                 "cake", "cakes", "biscuit", "biscuits", "bake", "baking", "pudding", "dessert",
                 "sweet", "sweets", "chocolate"),
          bias=1),
    entry("one-main-everyone", (("two dinners", "two meals", "one main", "same dinner",
                                "mixed group", "half vegetarian", "mixed table",
                                "vegetarians and meat eaters", "meat eaters",
                                "everyone can eat", "everyone will eat", "everyone eats",
                                "everyone at the table"),
                               ("make", "cook", "main", "dinner", "one", "everyone", "dish",
                                "feed")),
          ("Make the vegetarian dish the main for the whole table and put the meat on the side as "
           "an extra: a mushroom and lentil lasagne, a chickpea and spinach curry with rice, or a "
           "tray of roasted veg with feta and couscous. Nobody gets a plate of sides, and you cook "
           "one dinner."),
          avoid=("chicken", "beef", "pork", "lamb", "turkey", "mince", "bacon", "sausage",
                 "sausages", "ham", "fish", "prawns", "salmon", "steak", "chorizo"),
          bias=2),
    entry("pudding-ideas", (("pudding", "puddings", "dessert", "desserts"),
                            ("make", "idea", "ideas", "quick", "easy", "nice", "sunday",
                             "dinner", "guest", "guests", "like", "want", "any",
                             "what about", "how about", "and for", "for after",
                             "bring", "bringing", "people", "crowd", "party", "family",
                             "ahead", "of us", "weekend", "feed",
                             "four", "five", "six", "seven", "eight", "nine", "ten",
                             "eleven", "twelve")),
          _pudding_ideas,
          avoid=("refuses", "refuse", "refusing", "wont eat", "won't eat", "will not eat",
                 "fussy", "picky", "faddy", "reward", "bribe", "veg", "vegetables", "dinner time",
                 "cheese", "cheeseboard", "wine", "port", "beer", "cider", "lager", "gin",
                 "brandy", "whisky", "sherry", "diabetic", "diabetes", "sugar free",
                 "no sugar", "gluten free", "pub", "restaurant", "cafe", "menu",
                 "savoury pudding", "savory pudding", "steak and kidney", "suet",
                 "black pudding", "white pudding", "pease pudding", "yorkshire pudding")),
    entry("savoury-pudding", (("savoury pudding", "savory pudding", "steak and kidney pudding",
                               "suet pudding", "suet crust"),
                              ("what goes with", "serve with", "serve", "side", "recipe", "make",
                               "making", "cook", "cooking", "how", "sunday", "dinner",
                               "gravy", "mash")),
          ("A steak and kidney pudding is dinner, not afters: line a buttered basin with suet "
           "crust (200g self-raising flour, 100g suet, a pinch of salt, water to a soft dough), "
           "fill it with beef skirt and kidney tossed in flour, season it hard and add a little "
           "stock, then lid it and steam it for three to four hours. Serve it with mashed potato, "
           "buttered greens or peas and extra gravy, and turn it out onto a plate with a cloth "
           "round the basin. It is better made a day ahead and steamed again, which is how it "
           "suits a Sunday."),
          avoid=("crumble", "rice pudding", "bread and butter", "eton mess", "dessert",
                 "sweet", "sugar", "custard",
                 "pie", "pies", "pastry", "shortcrust", "puff pastry", "filo", "oven"),
          bias=1),
    entry("no-scales", (("scales", "scale", "weigh", "weighing", "weigh out", "weighs"),
                        ("broke", "broken", "without", "no scales", "no scale", "grams", "cups",
                         "convert", "instead", "measure")),
          ("Without scales, measure with one mug and keep using it for everything in the recipe: a "
           "250ml mug holds about 150g of plain flour, 200g of caster sugar, 225g of butter or "
           "250g of milk, and a level tablespoon is 15g of flour, 12g of sugar or 15g of oil. A "
           "mug of rice to one and a half mugs of water is the same ratio by volume, so the "
           "recipe still works; if you bake often, a digital scale costs less than a bag of "
           "flour and settles it."),
          avoid=("bathroom", "my weight", "lose weight", "losing weight", "diet", "kg", "stone",
                 "pounds", "weigh myself", "scale says", "baby", "newborn", "baggage",
                 "airport", "how many grams in", "how many cups in", "how much does",
                 "how many cups")),
    entry("tart-filling", (("tart", "tarts", "tartlet", "tartlets", "flan", "flan case"),
                           ("filling", "fill", "make", "recipe", "bake", "baking", "what goes in",
                            "what should i put", "put in", "lemon", "pastry case",
                            "how do i")),
          ("A lemon tart filling is four eggs, 200g of caster sugar, the juice and zest of four "
           "lemons and 200ml of double cream, whisked together and poured into a part-baked "
           "pastry case, then baked at 150C for 30 to 35 minutes until it is set with a wobble "
           "in the middle, because it firms up as it cools and needs no cornflour. Bake it in a "
           "loose-bottomed tin you have lined with shop-bought shortcrust if you are short of "
           "time, and let it cool completely before you take it out of the tin or the sides "
           "will crack."),
          avoid=("soggy", "soggy bottom", "blind bake", "blind baking", "baking beans", "case",
                 "pastry", "shrink", "shrinkage", "crack", "cracked", "ramekin", "small pan",
                 "saucepan", "tin", "tins", "quiche", "shop", "buy", "calories", "sugar free",
                 "gluten free", "vegan",
                 "chocolate", "fruit tart", "fruit flan", "fruit tarts")),
    entry("rice-rinse", ("rice", ("wash", "washing", "rinse", "rinsing")),
          "For a risotto or a rice pudding, don't rinse it: that surface starch is what makes it "
          "creamy. For separate, fluffy grains, rinse in a sieve until the water runs clear, which "
          "washes the starch off. It was never about hygiene.",
          avoid=("cooker", "pot", "pan", "machine", "appliance",
                 "the washing", "washing machine", "washing up", "laundry", "clothes", "dishes",
                 "is done", "done yet", "line", "basket", "darks", "lights"),
          bias=1),
    entry("rice-dry-store", ("rice", ("store", "storing", "stored", "keep", "keeping", "kept",
                                      "uncooked", "jar", "airtight", "last", "lasts",
                                      "go off", "goes off", "gone off", "open", "opened",
                                      "unopened", "packet", "bag", "out of date", "past the date",
                                      "after the date", "expired", "still ok", "still good",
                                      "safe to eat", "year", "years", "months")),
          ("Dry rice keeps for years in an airtight jar in a cool, dark cupboard - the date on the "
           "bag is a best-before, not a use-by: brown rice is the one that turns, in about six "
           "months, and it tells you by smelling of old oil. Weevils or damp and it goes out. "
           "Only cooked rice needs the fridge, and that one is worth being strict about: 24 hours "
           "and no longer."),
          avoid=("cooked", "leftover", "left over", "reheat", "next day", "yesterday", "fridge",
                 "curry", "wash", "washing", "rinse", "rinsing", "freeze", "freezing",
                 "how long to cook", "water", "pudding", "puddings", "milk", "sugar",
                 "cold", "warm", "hot",
                 "cat", "cats", "dog", "dogs", "pet", "pets", "bird", "birds",
                 ) + KEEP_QUALITY_WORDS,
          bias=1),
    entry("tins-keep", (("tins", "tin of", "tins of", "tinned", "cans of", "tin", "canned food",
                         "canned goods"),
                        ("keep", "keeps", "last", "lasts", "how long", "go off", "goes off",
                         "gone off", "stored", "storage", "still ok", "still good",
                         "out of date", "past the date", "after the date", "expired", "use by",
                         "best before", "date")),
          _tins_keep,
          avoid=("simmer", "simmering", "cook", "cooking", "boil", "boiling", "fry", "frying",
                 "roast", "heat", "minutes", "recipe", "sauce", "soup", "stew", "casserole",
                 "make", "made", "dinner", "supper",
                 "paint", "polish", "wax", "oil", "petrol", "biscuit", "biscuits", "cake", "cakes",
                 "open", "opened", "once open", "half", "leftover", "left over"),
          bias=2),
    entry("sugar-keeps", (("sugar",), ("go off", "goes off", "gone off", "keep", "keeps",
                                       "how long", "still ok", "still good", "years old",
                                       "shelf life", "crystallised", "crystallized", "hard")),
          ("Sugar does not go off: white sugar keeps for years, and the date on the bag is a "
           "best-before for quality rather than a use-by. Brown sugar sets hard rather than "
           "spoiling - a slice of bread or apple in the jar softens it again - and sugar with "
           "insects or damp in it goes out."),
          avoid=("low", "high", "levels", "blood", "hypo", "diabetes", "diabetic", "im off",
                 "cutting out", "cut out", "gave up", "give up", "diet", "weight", "calories",
                 "cough", "recipe", "cake", "bake", "baking", "jam", "marmalade", "syrup",
                 "substitute", "instead of", "replace")),

    entry("chickpeas", (("chickpeas", "chickpea", "chick peas", "garbanzo beans"),
                        ("make", "do", "cook", "use", "tin", "tinned", "can", "ideas", "with")),
          "Fry a drained tin in olive oil with cumin and paprika for 8 minutes and they go crunchy "
          "enough to eat as a snack or over a salad; mash them with tahini, lemon and garlic for "
          "hummus, or simmer them in tomatoes and coconut milk for a curry in 20 minutes."),
    entry("buttermilk-make", ("buttermilk", ("make", "making", "homemade", "from milk", "yourself")),
          "Stir a tablespoon of lemon juice or white vinegar into 250ml of milk and leave it 10 "
          "minutes to thicken: that is buttermilk for a recipe. Thinned plain yoghurt or soured "
          "cream work too, and milk alone is fine in most pancake and muffin recipes.",
          avoid=("pancake", "pancakes", "muffin", "muffins", "scone", "scones", "cake",
                 "dressing", "substitute", "instead", "replace", "alternative")),
    entry("gluten-free-baking",
          (GLUTEN_FREE_ASKS, GLUTEN_FREE_DISHES),
          _gluten_free,
          bias=1,
          ask=GLUTEN_FREE_ASKS,
          avoid=_GLUTEN_FREE_SKIP),
    entry("gluten-free-fact",
          (GLUTEN_FACT_FOODS, GLUTEN_FACT_ASKS),
          _free_of_gluten_fact,
          bias=3,
          ask=GLUTEN_FACT_ASKS,
          guard=asks_a_gluten_fact),
    entry("calories-in-food",
          (CALORIE_ASKS, tuple(FOOD_CALORIE_MEALS) + tuple(FOOD_CALORIES)),
          _calories,
          avoid=("a day", "per day", "burn", "burned", "burnt", "exercise", "diet",
                 "lose weight")),
    entry("nutrients-in-food",
          (tuple(word for word, _column in _NUTRIENT_WORDS)
           + tuple("how much %s" % word for word, _column in _NUTRIENT_WORDS)
           + tuple("how many %s" % word for word, _column in _NUTRIENT_WORDS),
           tuple(FOOD_NUTRIENTS)),
          _nutrients,
          avoid=("a day", "per day", "daily", "a week", "lose weight", "build muscle", "diet",
                 "shakes", "shake", "powder", "supplement", "deficiency", "instead",
                 "substitute", "substitute for", "how do i", "recipe", "cook", "make",
                 "breast", "breasts",
                 "shirt", "shirts", "crease", "creases", "board",
                 "steaming", "steamed", "steam it", "steam them")),
    entry("calories-a-day", (("calorie", "calories", "kcal"),
                             ("a day", "per day", "daily", "should i eat", "need")),
          "An adult needs roughly 2,000 to 2,500 calories a day, and the exact number depends on "
          "your size and how much you move: about 2,000 suits most women and 2,500 most men, with "
          "1,500 to 1,800 for steady weight loss. Food labels count in kilocalories, so the "
          "\"calories\" on a packet are these numbers.",
          ask=("a day", "per day", "daily", "should i eat", "need", "how many"),
          avoid=("banana", "chicken", "bread", "carbs", "protein", "sugar")),
    entry("chicken-protein", (("chicken breast", "chicken breasts"),
                             ("protein", "calories", "macros", "nutrition")),
          "A cooked chicken breast is about 30g of protein per 100g, so a 175g breast carries "
          "roughly 50g, near a quarter of a day's protein for an adult, at about 280 calories."),

    entry("egg-fry", (("fry", "frying", "fried"),
                      ("egg", "eggs")),
          "Heat a little oil or butter in a frying pan over a medium heat until it shimmers, break "
          "the egg into a cup and slide it in, and give it 2 to 3 minutes for a runny yolk. Spoon "
          "the hot fat over the white to set the top, and salt it at the end so the yolk doesn't go "
          "spotted.",
          avoid=("rice", "bread", "toast", "chicken", "fish", "onion", "onions", "potato",
                 "potatoes", "chips", "pancake", "pancakes", "bacon", "sausage", "sausages",
                 "tomato", "mushroom", "mushrooms", "noodles", "leftover", "microwave")),
    entry("garlic-peel", (("garlic",), ("peel", "peeling", "peeled", "skins", "quick", "quickly",
                                        "easy", "faster", "fast", "hassle")),
          "Press the clove on the board with the flat of a knife until it cracks and the skin comes "
          "away in one piece; a handful of cloves shaken hard in a lidded jar works too. For a whole "
          "bulb, drop the cloves in boiling water for 30 seconds and the skins slip off.",
          avoid=("hands", "smell", "smelly", "stink", "burn", "burnt", "bitter", "bread", "butter",
                 "breath", "bad breath", "garlic breath", "mouth", "breathing",
                 "sauce", "roast", "plant", "grow", "growing", "keep", "store", "freeze", "go off",
                 "sprout", "green", "how much", "how many", "substitute", "instead", "powder",
                 "paste", "how long")),
    entry("garlic-crush",
          (("garlic", "garlic clove", "garlic cloves", "a clove of garlic"),
           ("crush", "crushed", "crushing", "mince", "minced", "chop", "chopped", "press",
            "without a press", "no press", "puree", "paste", "smash", "grate", "grated")),
          "Put the clove on the board, lay the flat of a wide knife on it and press down hard "
          "with the heel of your hand until it splits; pull the skin off, chop it, then drag the "
          "knife across the pile a few times with a pinch of salt and it turns to paste. The "
          "bottom of a glass or the back of a spoon crushes it just as well, and the fine side "
          "of a grater gives you a purée for a sauce.",
          avoid=("peel", "peeling", "peeled", "skins", "burn", "burnt", "bitter", "bread",
                 "butter", "roast", "plant", "grow", "growing", "keep", "store", "freeze", "go off",
                 "sprout", "sprouts", "green", "how much", "how many", "substitute", "instead",
                 "powder", "smell", "smelly", "hands", "how long", "cloves in a bulb",
                 "breath", "bad breath", "garlic breath", "mouth", "breathing")),
    entry("ginger-keep", (("ginger",),
                          ("keep", "store", "storing", "last", "freeze", "freezer", "fresh",
                           "fridge", "grate", "long")),
          "Keep fresh ginger, unpeeled, in the fridge drawer for about 3 weeks, or freeze it whole "
          "and grate it straight from frozen: it grates finer that way and keeps 3 months. A "
          "teaspoon of the frozen gratings is about the same as a thumb of fresh.",
          ask=KEEP_ASK),
    entry("marinade", (("marinade", "marinade", "marinate", "marinating", "marinated"),
                       ("make", "how long", "recipe", "good", "best", "overnight", "quick",
                        "goes", "go", "put", "use", "ingredients", "chicken", "steak", "meat",
                        "fish", "tofu", "lamb", "pork")),
          "Whisk 3 parts oil to 1 part acid - lemon, wine or vinegar - with salt, then add garlic, "
          "honey, soy, herbs or yoghurt. Give chicken or fish 30 minutes to 2 hours and tougher meat "
          "4 hours or overnight, always in the fridge; a lot of acid or sugar left on for a day "
          "turns meat mushy.",
          avoid=("bottle", "jar", "shop", "buy", "price")),
    entry("stirfry-sauce", (("stir fry", "stirfry", "stir-fry", "wok"),
                            ("sauce", "flavour", "flavor", "tasty", "taste")),
          "Stir 2 tablespoons of soy, 1 of oyster sauce, a teaspoon of sugar and a teaspoon of "
          "cornflour into 100ml of water or stock and pour it in when the vegetables are nearly "
          "done: it thickens in about a minute. Garlic and ginger go in first, in the oil, before "
          "anything wet.",
          avoid=("rice", "noodles", "calories", "how long", "pan", "buy")),
    entry("soup-flavour", (("soup",),
                           ("make", "better", "improve", "more flavour", "flavour", "boring",
                            "lifeless", "interesting")),
          _soup,
          avoid=("bland", "tasteless", "no taste", "tin", "can", "carton", "shop", "buy",
                 "calories", "recipe", "thicker", "thicken", "thickening", "thick", "thin",
                 "watery", "runny"),
          ask=("taste", "tastes", "tastier", "better", "flavour", "flavourless", "boring",
               "lifeless", "improve", "interesting", "dull", "flat"),
          bias=2),
    entry("beetroot-cook", (("beetroot", "beetroots", "beet"),
                            ("cook", "roast", "boil", "bake", "peel", "prepare", "long")),
          "Wrap whole beetroot in foil with a splash of oil and roast at 200C (180C fan) for 1 to "
          "1.5 hours, until a knife slides in, or boil it 40 to 60 minutes. Rub the skins off with a "
          "tea towel while they are still warm, and wear gloves unless you want pink hands.",
          avoid=("blood", "urine", "wee", "stain", "juice", "sugar", "watch")),
    entry("turkey-crown", (("turkey",), ("crown", "long", "cook", "roast", "time", "temperature",
                                        "juicy", "dry", "weight", "whole", "bird")),
          _turkey,
          avoid=("leftover", "leftovers", "sandwich", "stock", "carcass", "defrost", "freeze",
                 "calories", "price", "buy",
                 "breast", "breasts", "leg", "legs", "thigh", "thighs", "fillet", "fillets",
                 "drumstick", "drumsticks", "wing", "wings", "spatchcock", "mince", "steak",
                 "escalope", "escalopes", "butterflied")),
    entry("turkey-cut", (("turkey", "turkeys"),
                         ("breast", "breasts", "leg", "legs", "thigh", "thighs", "fillet",
                          "fillets", "drumstick", "drumsticks", "wing", "wings", "spatchcock",
                          "escalope", "escalopes", "steak", "steaks")),
          _turkey_cut, bias=2,
          avoid=("whole", "whole bird", "crown", "stuffed", "stuffing", "defrost", "thaw",
                 "frozen", "freeze", "leftover", "leftovers", "sandwich", "stock", "carcass",
                 "mince", "burger", "burgers", "price", "calories", "safe", "poison")),
    entry("stuffing-inside", (("stuffing", "stuff", "stuffed"),
                              ("inside", "in the bird", "in the turkey", "between the legs",
                               "a turkey", "the turkey", "a bird", "the bird", "for turkey",
                               "safe", "salmonella", "raw", "juices")),
          "Better not: cook it in a separate buttered tray, 25 minutes at 180C, because "
          "stuffing in a turkey soaks up the raw juices and holds the middle of the meat "
          "below a safe heat, so the bird needs about 20 minutes more and the stuffing comes out "
          "soggy. If you do stuff it, give the stuffing itself a thermometer read of 74C before the "
          "bird comes out to rest.",
          avoid=("nose", "sick", "ill", "blocked", "stuffed up", "full", "eat too much",
                 "mushroom", "pepper", "peppers", "cushion", "toy", "teddy", "envelope")),
    entry("turkey-order", (("turkey", "turkeys"),
                           ("order", "ordering", "ordered", "buy", "buying", "bought", "collect",
                            "collecting", "shop", "shopping", "when", "days", "early", "ahead",
                            "size", "big")),
          "Order it from a butcher or a supermarket a week or two ahead, and collect a fresh bird "
          "two or three days before: it keeps fine in the coldest part of the fridge for that "
          "long. If it is going in the freezer, buy it now, because a frozen turkey needs 24 hours "
          "in the fridge for every 2kg, so a 6kg bird is three days of thawing on its own.",
          avoid=("cook", "cooking", "roast", "roasting", "time", "temperature", "long", "done",
                 "defrost", "defrosting", "thaw", "thawing", "leftover", "leftovers", "sandwich",
                 "stock", "carcass", "breast", "leg", "thigh", "mince", "calories", "poison",
                 "visa", "holiday", "currency")),
    entry("cauliflower-rice", (("cauliflower", "cauliflowers"),
                               ("rice", "couscous", "carb", "carbs", "keto", "blitz", "grate",
                                "grated", "pulse", "instead", "substitute", "low carb")),
          _cauliflower_rice,
          avoid=("roast", "roasting", "whole", "cheese", "soup", "plant", "grow", "harvest",
                 "pick", "keep", "fridge", "freezer", "frozen", "freeze", "smell", "yellow",
                 "black", "spots", "worms", "caterpillar")),
    entry("burger-bind", (("burger", "burgers", "patty", "patties"),
                          ("fall apart", "falling apart", "break up", "breaking up",
                           "breaks up", "crumbly", "hold", "holds", "binding", "bind",
                           "make", "juicy", "dry", "recipe", "best", "together")),
          "Use mince that is at least 20% fat, shape it loosely without packing it down, and salt "
          "only the outside just before it goes in the pan: that is all the binding beef needs. If "
          "it keeps breaking up or the meat is lean, mix in an egg and a handful of breadcrumbs and "
          "chill the patties 20 minutes.",
          avoid=("veggie", "vegetarian", "vegan", "bean", "chicken burger", "halloumi",
                 "bun", "buns", "bap", "baps", "bread", "buy", "price", "restaurant", "london",
                 "near me", "nearby", "takeaway", "take away", "delivery", "place", "places",
                 "shop", "calories", "fast food")),
    entry("pesto", (("pesto",),
                    ("make", "recipe", "best", "how", "basil", "pine nuts", "pinenuts")),
          "Blitz 50g of basil, 30g of pine nuts, 50g of parmesan, a small garlic clove and a pinch "
          "of salt, then pour in about 100ml of olive oil with the motor still running. Rocket or "
          "spinach and walnuts stand in for basil and pine nuts, and it keeps a week in a jar under "
          "a layer of oil.",
          avoid=("jar", "shop", "price", "buy", "allergy", "nut allergy",
                 "use up", "using up", "use it up", "leftover", "left over")),
    entry("flat-bake", (("flat", "didnt rise", "didn't rise", "did not rise", "not risen",
                         "no rise", "came out flat"),
                        _NO_CAKE_RISE + ("pancake", "pancakes", "yorkshire", "batter",
                                         "bake", "baked", "baking",
                                         "cupcake", "cupcakes", "muffin", "muffins",
                                         "bun", "buns")),
          _flat,
          avoid=("spread", "spreads", "spreading", "spread out", "wide", "thinner", "melted",
                 "pooled", "pool",
                 "bread", "dough", "loaf", "taste", "tastes", "tasted", "bland", "dull",
                 "season", "fizzy", "beer", "tyre", "tire", "battery", "landlord", "rent",
                 "flatmate", "apartment", "screen", "phone", "bike", "car", "pancake", "pancakes",
                 "crepe", "crepes", "yorkshire", "yorkshires", "toad in the hole",
                 "hot", "cold", "freezing", "freezing cold", "heating", "heater",
                 "radiator", "radiators", "boiler", "warm", "leak", "leaking", "damp", "mould")
                 + _BAKE_KEEPING,
          guard=_not_the_flat_you_live_in_bake,
          bias=3),
    entry("aubergine", (("aubergine", "aubergines", "eggplant", "eggplants"),
                        ("rubbery", "bitter", "soggy", "cook", "salty", "oil", "fry")),
          ("Slice it, salt it for 20 minutes and pat it dry, then cook it in plenty of hot oil until "
           "it's deep golden: aubergine soaks up oil like a sponge, so a dry pan and too little fat "
           "is what leaves it rubbery. Roasting at 200C for 25 minutes works the same way."),
          bias=2,
          avoid=("plant", "growing", "grow", "soil", "allotment")),
    entry("peas-frozen", (("peas", "frozen peas", "pea", "petit pois", "petits pois",
                           "garden peas"),
                          ("frozen", "cook", "boil", "steam", "microwave", "how long",
                           "grey", "mushy")),
          ("Drop frozen peas into already boiling water and give them 2 to 3 minutes: they're "
           "blanched before freezing, so they need no more than that. They're done when they float "
           "and taste sweet; longer turns them grey."),
          avoid=("keep", "keeps", "keeping", "kept", "refreeze", "re-freeze", "re freeze",
                 "still good", "out of date", "go off", "gone off", "last", "lasts", "stay",
                 "good for"),
          guard=_not_short_of("peas?", "pea", "petit pois", "petits pois", "garden peas",
                              "frozen peas")),
    entry("peas-keeping", (("peas", "frozen peas", "pea", "petit pois", "petits pois",
                            "garden peas", "sweetcorn", "broad beans"),
                           ("keep", "keeps", "keeping", "kept", "last", "lasts", "stay",
                            "freezer", "refreeze", "re-freeze", "re freeze", "go off",
                            "gone off", "good for", "out of date", "how long")),
          ("Frozen peas keep about a year at -18C in a bag that stays shut: they don't go off, "
           "they dry out and turn starchy, so a bag from two winters ago is safe but not worth "
           "eating raw. Once they have thawed on the counter, cook them and eat them that day "
           "rather than freezing them again; a bag that thawed but stayed cold in the fridge can "
           "go back in the freezer, though the texture will be softer."),
          avoid=("boil", "boiled", "cook", "cooked", "cooking", "steam", "microwave", "recipe")),
    entry("banana-overripe", (("banana", "bananas"), ("overripe", "over ripe", "too ripe",
                                                       "mushy", "black", "use up", "going off",
                                                       "left over",
                                                       "too many", "so many", "lots of",
                                                       "loads of", "spare", "left")),
          ("Mash them into banana bread: 3 black bananas, 175g self-raising flour, 100g soft butter, "
           "100g sugar and 2 eggs, 50 to 55 minutes at 180C. Or peel and freeze them for smoothies; "
           "they go black in the freezer but taste the same."),
          bias=1,
          avoid=("keep", "keeps", "keeping", "stop them", "stop it", "going black", "go black",
                 "last longer", "stay fresh", "store", "storing", "storage", "how do i keep",
                 "plant", "growing", "grow", "tree", "soil",
                 "a day", "per day", "healthy", "good for you", "diet", "calories",
                 "how many can i", "is it ok to eat", "is it bad", "fattening")),
    entry("pancakes-flat", (("pancake", "pancakes", "crepes", "crepe"), ("flat", "thin", "thick",
                                                                          "fluffy", "rise", "light")),
          ("Flat pancakes are usually over-mixed or too thin: stir until the flour just disappears, "
           "leaving lumps, and use roughly 1 part flour to 1.2 of milk by volume. Resting the batter "
           "15 minutes helps, and a pinch of baking powder makes the thick American ones rise."),
          bias=2,
          avoid=("day", "shrove", "recipe book", "how do i make", "how to make", "how can i make",
                 "how do you make", "recipe", "batter")),
    entry("cake-stuck-tin", (_BAKED_GOODS + ("bread", "loaf cake"),
                             ("stuck", "sticks", "sticking", "come out", "comes out", "getting out",
                              "get it out", "broke", "breaking", "broken", "tin", "tins", "pan")),
          _out_of_the_tin,
          avoid=("baking", "bake", "temperature", "oven", "how long", "rise", "sunk", "raw",
                 "mouldy", "fridge",
                 "fruit cake", "christmas cake", "rich fruit", "wedding cake", "simnel",
                 "dark fruit",
                 "grease", "greasing", "greased", "how do i grease", "should i grease",
                 "do i need to grease", "prepare the tin", "prepare a tin")),
    entry("rice-microwave",
          (("rice", "basmati", "long grain rice", "white rice", "jasmine rice"),
           ("microwave", "microwaving", "microwaved", "micro wave")),
          "Use a big bowl, because it boils up: one mug of rice to two mugs of boiling water, a "
          "pinch of salt, a plate over the top, and 10 minutes on full power. Leave it to stand 5 "
          "minutes still covered - that is what finishes it - then fork it through from the "
          "bottom. Rinse the rice first so the grains stay separate.",
          ask=("cook", "cooking", "boil", "boiling", "instead", "how do i", "make", "making",
               "how long", "long does", "takes", "minutes", "water", "time"),
          avoid=("reheat", "reheating", "leftover", "left over", "next day", "yesterday",
                 "already cooked", "pouch", "packet", "ready cooked", "sticky", "pudding",
                 "risotto", "freeze", "freezer", "last night", "last nights", "night before",
                 "yesterdays", "spare", "is it safe", "safe to"),
          bias=2),
    entry("rice-fluffy", (("rice", "basmati", "long grain", "jasmine"),
                          ("fluffy", "separate", "not sticky", "grains", "perfect", "nice",
                           "light", "like the takeaway", "like a restaurant", "how do i get")),
          "Rinse it until the water runs clear, use 1 part rice to 1.5 parts water, bring it to a "
          "boil, then turn it right down, put the lid on and leave it 10 minutes without stirring. "
          "Take it off the heat and let it sit 5 minutes with the lid on, then fork it through from "
          "the bottom - that steam is what makes the grains separate.",
          avoid=("sticky", "sushi", "pudding", "risotto", "paella", "mushy", "stuck", "burnt",
                 "microwave", "leftover", "reheat", "how long", "per person", "freeze",
                 *(tuple(_DAY_BEFORE) + ("good for",)))),
    entry("white-sauce", (("white sauce", "bechamel", "béchamel", "roux", "cheese sauce",
                           "parsley sauce", "lumpy sauce", "thicken a sauce",
                           "thickening a sauce", "sauce for"),
                          ("make", "making", "how do i", "how to", "recipe", "lumpy", "thicken",
                           "basic", "easy", "best")),
          "Melt 25g of butter, stir in 25g of plain flour and cook it a minute, then add 300ml of "
          "milk a splash at a time, whisking each splash in before the next - that is what keeps it "
          "smooth. Simmer it 3 or 4 minutes, season with salt and pepper, and stir in a handful of "
          "grated cheese off the heat for a cheese sauce.",
          avoid=("tomato", "pasta sauce", "apple sauce", "soy sauce", "hot sauce", "bbq",
                 "cranberry", "brown sauce", "worcestershire", "gravy", "custard",
                 "bread sauce", "hollandaise", "pesto", "curry sauce", "mint sauce",
                 "sauce for pasta", "sauce for the pasta", "sauce for spaghetti",
                 "without flour", "no flour", "anything but flour", "cornflour", "corn starch",
                 "cornstarch", "arrowroot", "gluten free", "gluten-free", "without wheat",
                 "no wheat", "coeliac", "celiac")),
    entry("thicken-without-flour",
          (("thicken", "thickening", "thicker", "thickens", "roux", "slurry", "gravy"),
           ("without flour", "no flour", "not use flour", "cornflour", "corn starch",
            "cornstarch", "arrowroot", "gluten free", "gluten-free", "without wheat", "no wheat",
            "instead of flour", "other than flour", "coeliac", "celiac", "coeliacs")),
          "Cornflour is the quickest stand-in: mix one tablespoon with two tablespoons of cold "
          "water, stir it into the simmering sauce and let it bubble for two minutes - it only "
          "thickens at a boil. Arrowroot does the same and gives a clearer gloss. With no starch "
          "at all, simmer with the lid off until it coats a spoon, or off the heat whisk in a knob "
          "of cold butter or a spoonful of cream. A gluten free plain flour blend makes a roux "
          "the same way as ordinary flour.",
          avoid=("stew", "stews", "soup", "soups", "casserole", "casseroles", "hotpot",
                 "porridge", "yoghurt", "yogurt", "smoothie",
                 "stain", "starch the shirt", "wallpaper", "paint", "hair", "custard",
                 "bread sauce", "hollandaise", "jam", "setting point"),
          bias=2),
    entry("omelette-stick", (("omelette", "omelet", "frittata", "scrambled eggs", "eggs"),
                             ("stick", "sticks", "sticking", "stuck", "stuck to the pan",
                              "burn", "burning", "pan")),
          "A hot non-stick pan with butter foaming but not browning, and eggs beaten just enough "
          "to mix: pour them in, then push the set edges into the middle and tip the pan so the "
          "raw egg fills the gap. Take it off the heat while the top is still a little wet - it "
          "finishes cooking in the pan, and that is what stops it sticking and going rubbery.",
          avoid=("boil", "boiled", "poach", "scrambled eggs how", "frying", "rice", "pasta",
                 "cake", "batter", "meat", "fish", "chicken")),
    entry("pork-crackling", (("crackling", "crackle", "pork belly", "pork shoulder",
                              "pork loin", "pork roast", "pork joint"),
                             ("crispy", "crisp", "how do i", "how", "get", "make", "best",
                              "soft", "soggy", "not", "wont", "won't", "failed")),
          "Score the skin, pour a kettle of boiling water over it, dry it and rub in plenty of "
          "salt and a little oil, then roast it at 220C for 30 minutes and 180C after that, "
          "without basting or covering it, and if the skin is still soft once the meat has "
          "rested cut the crackling off and grill it for 5 minutes on a rack.",
          avoid=("dry", "dry out", "tough", "bland", "gravy", "apple sauce", "leftover",
                 "sandwich", "pulled")),
    entry("sprouts", (("sprouts", "sprout", "brussels", "brussel", "brussels sprouts"),
                      ("bitter", "taste", "tasting", "cook", "cooking", "boil", "roast",
                       "not", "less", "how do i", "how long", "best way", "nice")),

          "Bitter means overcooked or undercooked: halve them and boil 4 to 5 minutes, no more, "
          "or roast them cut side down at 200C for 20 minutes. Cut a cross in the stalk end so "
          "the middle cooks at the same time as the outside, and finish with butter, lemon or a "
          "little bacon - a pinch of sugar in the water does very little.",
          avoid=("christmas shopping", "freeze", "leftover", "soup", "keep warm", "warming",
                 "stay warm", "ahead of time", "warm", "garlic", "onion", "onions", "potato",
                 "potatoes", "seeds", "bean sprouts", "alfalfa", "keep from", "store",
                 "storing"),
          ask=("bitter", "bitterness", "sour", "taste", "tasting", "tastes")),
    entry("coffee-cafe", (("coffee", "espresso" ), ("cafe", "café", "home", "better", "taste",
                                                     "barista", "grind", "make")),
          ("Fresh beans ground just before you brew, and a scale: 60g of coffee per litre for filter, "
           "or 18g in a double espresso. Stale grounds or a brew too weak to taste is what makes "
           "home coffee thin next to a cafe's."),
          avoid=("machine", "buy", "best", "gift", "shop", "weak", "weaker", "strong",
                 "stronger", "strength",
                 "headache", "headaches", "migraine", "migraines", "worse", "anxious",
                 "anxiety", "jittery", "shaky", "palpitations", "sleep", "awake", "head")),
    entry("coffee-jitters", (("coffee", "espresso", "caffeine", "energy drinks", "energy drink"),
                             ("anxious", "anxiety", "jittery", "jitters", "shaky", "shakey",
                              "palpitations", "heart racing", "racing heart", "cant sleep",
                              "can't sleep", "keep me awake", "keeps me awake", "awake",
                              "before bed", "sleep", "panic", "wired", "keeps me up",
                              "keep me up", "up at night", "wide awake", "cant get to sleep",
                              "can't get to sleep",
                              "late", "too late", "this late", "tonight", "this evening",
                              "in the afternoon", "pm", "ok to")),
          _coffee_late,
          avoid=("stain", "stains", "machine", "pod", "pods", "shop", "buy", "gift", "table",
                 "grounds", "garden", "compost", "plant", "plants", "cupboard", "pregnant",
                 "pregnancy", "baby", "child", "toddler")),
    entry("coffee-upsets-me", (("coffee", "coffees", "espresso", "espressos", "latte", "lattes",
                                "cappuccino", "cappuccinos", "americano", "americano", "caffeine",
                                "energy drink", "energy drinks", "flat white"),
                               ("sick", "queasy", "queasiness", "nausea", "nauseous", "nauseated",
                                "stomach", "stomach ache", "stomachache", "tummy", "gut",
                                "acid", "acid reflux", "reflux", "heartburn", "indigestion",
                                "ill", "disagree", "disagrees", "cant drink",
                                "can't drink", "cannot drink", "any more", "anymore", "upsets",
                                "upset", "bloated", "bloating", "loose", "diarrhoea", "diarrhea",
                                "runs", "toilet", "makes me feel", "feel sick", "gives me")),
          "The caffeine and the acids in coffee are what do it: on an empty stomach coffee "
          "raises stomach acid and speeds the gut on, which is the sick, sloshy feeling. Drink it "
          "after food rather than instead of it, make it weaker (same water, less coffee), try a "
          "darker roast or cold brew, and take it with milk if black is the problem. If it gives "
          "you heartburn, stomach pain or loose stools most days, cut to one small cup and see a "
          "GP.",
          ask=("sick", "queasy", "nausea", "nauseous", "nauseated", "stomach", "stomach ache",
               "tummy", "gut", "acid", "reflux", "heartburn", "indigestion", "ill",
               "disagree", "disagrees", "cant drink", "can't drink", "any more", "anymore",
               "upsets", "upset", "bloated", "bloating", "loose", "diarrhoea", "diarrhea",
               "toilet", "feel sick", "makes me feel", "gives me"),
          avoid=("bad for you", "empty stomach", "healthy", "unhealthy", "how many cups",
                 "stain", "stains", "machine", "machines", "pod", "pods", "shop", "buy", "gift",
                 "grind", "grinder", "grounds", "compost", "plant", "plants", "cake", "biscuit",
                 "tiramisu", "cafe", "café", "barista", "how long", "half life", "half-life",
                 "sleep", "bed", "bedtime", "late", "awake", "tonight", "evening", "anxious",
                 "anxiety", "jittery", "jitters", "shaky", "palpitations", "headache",
                 "headaches", "migraine", "withdraw", "withdrawal", "decaf", "pregnant",
                 "pregnancy", "taste", "tastes", "strength", "strong", "weak", "how much",
                 "too much"),
          bias=3),

    entry("beans-gas",
          (("beans", "bean", "lentils", "lentil", "chickpeas", "chickpea", "pulses",
            "cabbage", "broccoli", "cauliflower", "sprouts", "kale"),
           ("gas", "gassy", "fart", "farts", "farting", "flatulence", "windy", "wind")),
          ("Beans, lentils and the cabbage family carry sugars your small intestine cannot break "
           "down, so the bacteria in your gut ferment them and give off gas. It is normal, and it "
           "settles: rinse tinned beans well, soak dried ones and pour that water away, cook them "
           "properly, and add them a little at a time so your gut adjusts over a few weeks."),
          avoid=("boiler", "hob", "cooker", "bill", "bills", "meter", "leak", "smell of gas",
                 "central heating", "weather", "forecast", "gale", "door", "gate", "window")),
    entry("potato-green",
          (("potato", "potatoes", "spuds", "spud"),
           ("green", "greening", "greened", "sprouted", "sprouting", "sprouts", "solanine",
            "bitter")),
          ("Green on a potato is chlorophyll, which is harmless, but it comes up in the light "
           "alongside solanine, which is not: cut out any green patches, and bin a potato that is "
           "green all over or has long white sprouts. Keep them in a dark cupboard rather than on "
           "the windowsill, and never eat the sprouts."),
          avoid=("how do i stop", "stop them", "keep them from", "prevent", "last longer",
                 "cupboard", "what am i doing wrong", "doing wrong"),
          bias=1),
    entry("egg-green-ring",
          (("egg", "eggs", "yolk", "yolks"),
           ("green", "grey", "gray", "ring", "sulphur", "sulfur", "greyish")),
          ("The green ring is iron from the yolk meeting sulphur from the white, which happens when "
           "an egg is cooked too long or cooled slowly. It is harmless. Lower eggs into water that "
           "is already boiling, give them 9 to 10 minutes for hard boiled, and run them under cold "
           "water straight away to stop the ring forming."),
          avoid=("keep", "keeping", "how long", "storage", "store", "peel", "peeled", "fresh",
                 "gone off", "floating", "float"),
          bias=1),
    entry("eggs-peel",
          (("egg", "eggs", "hard boiled", "hard-boiled", "hardboiled"),
           ("peel", "peels", "peeled", "peeling", "shell", "shells", "sticks", "sticking")),
          "Cool them fast in iced water - an egg peeled warm tears, and the cold sets the white "
          "away from the shell - then tap the shell all over and start at the fat end, where the "
          "air pocket is, with a teaspoon of the water under the shell to loosen it. A teaspoon of "
          "bicarbonate in the pan helps too, and the freshest eggs are the ones that stick, so an "
          "egg a week or two old peels more cleanly than one from today.",
          avoid=("how long", "minutes", "soft boiled", "runny", "green", "grey", "gray", "ring",
                 "poach", "poached", "scramble", "scrambled", "fry", "fried", "keep", "keeping",
                 "store", "fresh", "float"),
          bias=1),
    entry("potato-watery",
          (("potato", "potatoes", "boiled potatoes", "mashed potatoes"),
           ("watery", "waterlogged", "soggy", "wet", "sloppy")),
          "Drain them the second a knife slides in and let them sit in the colander off the heat "
          "for 2 minutes so the steam escapes: potatoes go watery when they sit in their water, "
          "and a lid left on traps it back on. Save a splash of the cooking water to loosen mash "
          "instead of milk if it still looks wet.",
          avoid=("sauce", "soup", "stew", "casserole", "curry", "gravy", "sweet", "salad",
                 "keep", "keeps", "fridge", "freezer", "roast", "oven", "gratin"),
          bias=3),
    entry("lasagne-runny",
          (("lasagne", "lasagna", "moussaka", "cannelloni"),
           ("runny", "watery", "sloppy", "wet", "slumped", "fell apart", "falls apart")),
          "Let it stand 10 to 15 minutes out of the oven before you cut it, which is what sets the "
          "layers: a lasagne that runs was cut straight from the oven. Next time reduce the ragu "
          "until a spoon leaves a trail and use a thicker bechamel - 50g each of butter and flour "
          "to 500ml of milk - with the egg in it.",
          avoid=("recipe", "recipe for", "vegetarian", "vegan", "freeze", "frozen", "keep",
                 "reheat", "calories", "how do i make", "how to make", "sauce"),
          bias=2),
    entry("sauce-bitter",
          (("sauce", "sauces", "gravy", "soup", "stew", "ragu", "curry", "casserole", "chilli"),
           ("bitter", "bitter taste", "tastes bitter", "too bitter", "tastes sour",
            "sour taste", "went sour", "turned sour", "is sour")),
          "Bitter in a sauce is burnt garlic, a roux or flour taken past golden, or a burnt pan "
          "scraped back in; a pinch of sugar, a spoon of cream and a squeeze of lemon take the "
          "edge off, but if it tastes of scorched garlic or flour there is no rescuing it. Low "
          "heat, garlic in last and stirred for 30 seconds is the fix next time.",
          avoid=("beer", "coffee", "tea", "chocolate", "green", "sprout", "sprouts", "lemon",
                 "orange", "greens", "keep", "keeps", "store", "fridge", "freezer", "almond",
                 "almonds", "melon", "cucumber", "kale",
                 "sour cream", "sweet and sour", "sourdough", "sauerkraut")),
    entry("smoothie-thick",
          (("smoothie", "smoothies", "shake", "protein shake"),
           ("thick", "too thick", "gluey", "stodgy", "lumpy", "wont blend", "not blending",
            "thinner", "less thick", "thin it", "thin it out", "make it thinner")),
          "Loosen it with liquid before anything else - a splash of milk, water or juice, then "
          "blend again - and add ice last: a smoothie thickens as it stands, so make it a little "
          "thinner than you want it, and a spoon of yoghurt or half a banana gives body without "
          "the clag.",
          avoid=("recipe", "recipes", "calories", "healthy", "protein", "green", "diet")),
    entry("smoothie-thin",
          (("smoothie", "smoothies", "shake", "protein shake", "milkshake", "milkshakes"),
           ("thicker", "thicken", "more filling", "filling", "add body", "more body", "bulk it",
            "too thin", "so thin", "very thin", "watery", "runny", "not filling")),
          "Leave some of the liquid out and put something solid in instead: half a banana, a "
          "spoon of Greek yoghurt, oats or peanut butter, or a handful of frozen fruit, then "
          "blend it again. Pour the milk or juice in last, a splash at a time, until it moves "
          "the way you want - ice waters it down, so keep it to a few cubes.",
          avoid=("recipe", "recipes", "calories", "healthy", "protein powder", "diet",
                 "too thick", "loosen", "add milk", "more milk")),
    entry("cheesecake-cracked",
          (("cheesecake", "baked cheesecake"),
           ("crack", "cracked", "cracks", "cracking", "sank", "fallen", "fell")),
          "A cracked cheesecake was overbaked or cooled too fast: bake it until the edge is set "
          "and the middle still wobbles, then turn the oven off and leave it inside with the door "
          "ajar for an hour so it comes down to room temperature slowly. Sour cream on top hides "
          "any crack, and a water bath stops most of them.",
          avoid=("recipe", "recipe for", "how do i make", "no bake", "no-bake", "chill", "set in the fridge", "buy")),
    entry("ice-cream-icy",
          (("ice cream", "icecream", "sorbet", "frozen yoghurt"),
           ("icy", "ice crystals", "crystals", "grainy", "rock hard", "freezer burn")),
          "Icy ice cream is water freezing into crystals: more fat and sugar (cream instead of "
          "milk, a spoon of glucose or a splash of alcohol), churn it cold, and stir a home-made "
          "tub every 30 minutes for the first 3 hours so the crystals stay small. A freezer that "
          "runs very cold makes it harder still, so move it to the door shelf.",
          avoid=("recipe", "recipe for", "how do i make", "calories", "buy", "shop", "keep",
                 "keeps", "freezer burn on meat")),
    entry("chocolate-bloom",
          (("chocolate", "chocolates"), ("white", "bloom", "grey", "gray", "streaky", "dusty",
                                         "patchy")),
          ("White streaks on chocolate are bloom, and it is harmless: either the cocoa butter has "
           "melted and set again, or damp has pulled sugar to the surface. It still melts and "
           "tastes the same. Keep it in a cool cupboard around 15 to 18C rather than the fridge, "
           "which is what causes it."),
          avoid=("white chocolate", "hot chocolate", "drinking chocolate", "milk chocolate",
                 "dark chocolate", "chocolate bar", "recipe", "cake", "mug", "sauce")),
    entry("drink-mixer",
          (("gin", "vodka", "rum", "whisky", "whiskey", "brandy", "tequila", "spirit", "spirits"),
           ("mixer", "mixers", "mix", "mix with", "goes with", "good with", "tonic", "what goes",
            "what should i", "serve with", "drink", "drinks", "dark rum", "white rum",
            "spiced rum", "what can i mix", "what to mix")),
          "Gin wants tonic about one to three with a big wedge of lemon or lime, and cucumber or a "
          "sprig of rosemary if you have it; vodka takes the same plus elderflower or ginger beer, "
          "dark rum wants ginger beer and a squeeze of lime, whisky wants soda or ginger ale, and "
          "tequila wants grapefruit soda and salt. Cheap tonic is fine but use plenty of ice and "
          "stir it, because a warm, flat G and T tastes of nothing.",
          avoid=("recipe", "cake", "sauce", "marinade", "flambe", "how much", "units", "calories",
                 "is gin bad", "how is gin made", "distillery", "cheapest", "price")),
    entry("browns-in-the-pan",
          (("meat", "steak", "steaks", "chicken", "roast", "onions", "bacon", "sausages",
            "bread", "toast", "chips", "potatoes", "browning", "pork", "lamb"),
           ("brown", "browns", "browning", "crust", "sear", "seared", "searing", "maillard",
            "grey", "gray", "greyish", "went grey", "goes grey", "no colour", "no color",
            "isnt brown", "isn't brown", "not brown", "didnt colour", "didn't colour")),
          ("It is the Maillard reaction: past about 140C the sugars and amino acids on the surface "
           "rearrange into hundreds of new flavour compounds, and that is the brown crust and the "
           "savoury smell. Pat the surface dry first, get the pan properly hot, and leave space, "
           "because steam from a crowded pan keeps everything at boiling and it goes grey instead."),
          avoid=("safe", "done", "raw", "pink", "blood", "thermometer", "temperature", "how long",
                 "pale", "stew", "casserole", "slow cooker",
                 "smell", "smells", "smelly", "gone off", "went off", "off", "mould", "mold",
                 "mouldy", "moldy", "slimy", "slime", "is it ok", "ok to eat", "safe to eat",
                 "food poisoning", "bad", "date", "use by", "keep", "keeping", "freezer",
                 "freeze", "fridge", "left out",
                 "brown bread", "brown rice", "brown sugar", "brown flour", "wholemeal",
                 "white bread", "white rice", "better for you", "healthy", "healthier",
                 "good for you", "calories", "fibre")),
    entry("milk-curdle",
          (("milk", "cream", "yoghurt", "yogurt"), ("curdle", "curdled", "curdles", "curdling",
                                                    "split", "splits", "lumpy")),
          ("Milk curdles when heat or acid makes its proteins clump together: lemon, wine, vinegar "
           "or tomatoes, or a hard boil. Add acid off the heat and slowly, keep dairy out of a "
           "rolling boil, and stir a spoonful of flour or cornflour into the milk first when you "
           "are cooking it into a sauce."),
          avoid=("sour cream", "creme fraiche", "crème fraîche", "buttermilk", "keep", "keeping",
                 "gone off", "off", "date", "freeze", "freezer", "breast", "formula", "baby")),
    entry("roast-lamb", (("lamb", "leg of lamb", "shoulder of lamb"),
                          ("roast", "roasting", "oven", "cook", "joint", "leg", "shoulder")),
          "A leg of lamb is 25 minutes per 500g at 200C (180C fan), then 15 minutes resting under "
          "foil: about 1 hour 5 in total for a 2kg leg pink, 1 hour 25 for well done. Score the "
          "fat into diamonds, push garlic and rosemary into the cuts, and put it in a hot oven.",
          avoid=("chop", "chops", "leftover", "mince", "keema", "casserole", "hotpot", "stew",
                 "kebab", "shank", "curry", "shepherd", "goes with", "with it", "side",
                 "shoulder",
                 "slow", "slowly", "slow roast", "slow roasted", "slow-roasted", "low and slow",
                 "rest", "resting", "rested",
                 "curry", "curries"),
          ask=("how long", "how many minutes", "time", "minutes", "temperature", "degrees",
               "gas mark", "how hot", "per kilo", "per kg", "per pound", "what temperature",
               "how do i roast", "how do i cook", "how should i cook", "how to roast",
               "how to cook", "best way to roast", "best way to cook"),
          bias=2),
    entry("knead-dough", (("knead", "kneading", "kneaded"),
                          ("dough", "bread", "how long", "long", "much", "should", "by hand",
                           "mixer", "machine", "enough", "until")),
          "Knead it 10 minutes by hand, or 5 to 8 minutes in a mixer with a dough hook: it is "
          "ready when it is smooth, feels a little tacky, and springs back when you press a "
          "finger in. The real test is to stretch a piece thin enough to see light through it "
          "without it tearing.",
          ask=("knead", "kneading", "how long", "how much", "should", "do i", "by hand", "mixer"),
          avoid=("prove", "proving", "proof", "proving time", "rise", "rises", "rising", "rest",
                 "resting", "sourdough", "pastry", "shortcrust", "pasta", "cake", "cookie",
                 "cookies", "biscuit", "biscuits", "no knead", "no-knead", "pizza dough",
                 "naan", "flatbread", "focaccia", "brioche", "croissant", "hot cross buns"),
          bias=1),

    entry("cake-tin-grease", (("cake", "sponge", "loaf", "bread", "baking tin", "cake tin",
                               "pastry", "bundt", "bundt tin",
                               "pie", "tart", "quiche",
                               "muffin", "muffins", "bun", "buns", "cupcake", "cupcakes",
                               "sandwich tin", "springform", "loaf tin", "muffin tin"),
                               ("tin", "tins", "pan", "grease", "greasing", "greased", "line",
                                "lining", "lined", "parchment", "baking paper", "springform",
                                "stick", "sticks", "sticking")),
          "Rub the inside of the tin all over with butter or a little oil, then dust it with flour "
          "and tip the extra out, or cut a circle of baking parchment for the base: either is enough "
          "for a sponge, and both together never hurt. For a fruit cake or a big loaf, line the "
          "sides with a strip of paper too, and let the cake cool 10 minutes in the tin before you "
          "turn it out. A pastry case wants only a thin smear of butter and no flour, or the base "
          "goes soggy.",
          ask=("grease", "greasing", "line", "lining", "paper", "parchment", "stick", "sticking",
               "how do i", "how should i", "what do i", "why does"),
          avoid=("sink", "sank", "sunken", "risen", "rise", "leftover", "freeze", "freezer",
                 "out of the tin", "out of a tin", "out of the pan", "out of a pan",
                 "turn it out", "turn out", "stuck", "how long", "recipe",
                 "loosen", "loosening", "loosened", "free the cake",
                 "clean", "cleaning", "cleaned", "wash", "washing", "scrub", "scour", "soak",
                 "burnt on", "baked on", "crusted", "off the tin",
                 "burnt", "burned", "burning", "scorched", "charred",
                 "fruit cake", "christmas cake", "rich fruit", "wedding cake", "simnel",
                 "dark fruit",
                 "bundt", "bundt tin", "bundt pan",
                 "pastry", "shortcrust", "shortcrust pastry", "pastry case", "chill the pastry",
                 "chilling", "banneton", "proving basket",
                 "dough", "hands", "bench", "knead", "kneading", "wet dough", "sticky"),
          bias=3),

    entry("bundt-tin",
          (("bundt", "bundt tin", "bundt pan", "ring tin", "kugelhopf", "gugelhupf",
            "bundt cake"),
           ("grease", "greasing", "greased", "line", "lining", "flour", "dust", "dusting",
            "stick", "sticking", "stuck", "comes out", "come out", "turn out", "prepare",
            "paste", "how do i", "should i")),
          "A bundt has no flat base for a paper circle, so use a paste instead: mix equal weights "
          "of soft butter and plain flour (a tablespoon of each is plenty for a big tin) and brush "
          "it into every groove with a pastry brush, getting right into the corners and the central "
          "tube. Tap out any loose flour and bake the cake as the recipe says, then let it stand 10 "
          "minutes in the tin before turning it out - any longer and the steam softens the crust "
          "and it tears. A silicone bundt needs no paste at all, just a light oil.",
          avoid=("recipe", "how long", "oven", "temperature", "calories", "keep", "freeze",
                 "frozen", "stale", "size", "which tin", "how big", "stuck to", "came out of",
                 "didnt come out", "didn't come out", "sank", "raw", "burnt", "burned"),
          bias=3),

    entry("cake-out-of-tin", (("cake", "sponge"),
                               ("out of the tin", "out of a tin", "out of the pan",
                                "out of a pan", "out of its tin", "out of its pan", "stuck",
                                "release", "turn it out", "turn out", "take it out",
                                "loosen", "loosening", "loosens", "run a knife", "free the cake",
                                "breaking", "without breaking")),
          "Let it cool in the tin for 10 minutes, until it starts to shrink from the sides, and "
          "turn it out then: too hot and it breaks, stone cold and it sticks. Run a thin knife "
          "round the edge first, and line the tin with baking paper next time so it cannot grab.",
          avoid=("sink", "sank", "risen", "rise", "leftover", "freeze", "freezer", "fruit")),
    entry("pastry-soggy", (("pastry", "pie", "pies", "quiche", "quiches", "tart", "tarts",
                            "flan", "pastry base", "pie base", "shortcrust"),
                           ("soggy", "sad", "wet", "bottom", "base", "blind", "blind bake",
                            "crisp", "crispy")),
          "Bake it blind: chill the lined tin for 20 minutes, prick the base, cover it with paper "
          "and baking beans, then 15 minutes at 200C (180C fan) and 5 minutes uncovered to dry the "
          "base out. Brush the hot base with beaten egg so the filling cannot soak in, and cook a "
          "wet filling down first - a quiche or a fruit pie goes soggy from the inside too.",
          ask=("soggy", "sad", "wet", "bottom", "base", "blind", "blind bake", "crisp", "crispy"),
          bias=2,
          avoid=("how do i make pastry", "pastry recipe", "make shortcrust", "shortcrust recipe",
                 "puff pastry", "filo", "choux", "pastry flour", "pasta", "pizza")),
    entry("omelette-sticking", (("omelette", "omelet", "omelettes", "omelets", "frittata",
                                 "scrambled eggs", "scrambled egg"),
                                ("sticking", "sticks", "stuck", "pan", "sticking to the pan",
                                 "burnt", "burning", "heat")),
          "Turn the heat down and add fat: a knob of butter with a teaspoon of oil in a pan that is "
          "already hot, then the egg in when the butter foams but has not browned, and a silicone "
          "spatula pushing the set edges into the middle. A stainless pan is ready when a drop of "
          "water beads and skitters across it; on a non-stick one, no metal tools and no empty pan "
          "over a high heat.",
          ask=("omelette", "omelet", "omelettes", "omelets", "frittata", "scrambled egg",
               "scrambled eggs"),
          bias=2),
    entry("bread-quantities", (("bread", "breads", "dough", "loaf", "loaves", "flour",
                                "baguette", "rolls", "buns",
                                "yeast"),
                               ("salt", "yeast", "water", "hydration", "how much", "how many",
                                "grams", "percentage", "percent", "ratio", "quantity",
                                "quantities")),
          "For a 500g loaf: 10g of salt, 7g of dried yeast and 320ml of tepid water. That is the "
          "ratio to remember rather than the grams - 2% salt, a little over 1% yeast and about 64% "
          "water by flour weight - so double the flour and double all three. The dough should feel "
          "tacky but come away from the bowl; add water a spoon at a time if it is stiff and a "
          "spoon of flour if it is sloppy.",
          ask=("bread", "dough", "loaf", "loaves", "yeast", "sourdough", "prove", "knead",
               "breadmaker", "hydration"),
          bias=2,
          avoid=("cake", "cakes", "sponge", "pastry", "scone", "scones", "pancake", "pancakes",
                 "batter", "yorkshire", "gravy", "sauce", "thicken", "porridge", "pasta",
                 "rice", "couscous", "pizza", "naan", "pitta", "pita", "soda", "banana",
                 "drink", "drinking", "drunk", "thirsty", "thirst", "glasses", "litres",
                 "liters", "bottle", "bottled", "tap water", "dehydrated", "hydrated",
                 "a day", "adult", "child", "children", "baby", "blood pressure", "diet",
                 "beer", "brewing", "wine", "cider", "kombucha",
                 "protein", "calories", "calorie", "kcal", "carbs", "carb", "carbohydrate",
                 "carbohydrates", "fibre", "fiber", "fat", "fats", "sugar", "sugars", "iron",
                 "vitamin", "vitamins", "nutrition", "nutrients", "healthy", "good for you",
                 "slice", "slices", "sandwich", "sandwiches", "toast", "toasted",
                 "sourdough", "starter", "gluten free", "gluten-free", "breadmaker",
                 "bread maker", "machine",
                 "slice", "slices", "sliced", "per slice", "in a slice", "sugar", "calories",
                 "carbs", "carbohydrate", "fibre", "fiber", "healthy", "unhealthy",
                 "good for you", "bad for you", "nutrition", "how much is in")),

    entry("cookies-basic", (("cookie", "cookies", "biscuit", "biscuits"),
                             ("how do i make", "how to make", "recipe", "from scratch", "make",
                              "bake", "chewy", "crispy")),
          "125g soft butter creamed with 100g sugar, an egg beaten in, then 200g plain flour and "
          "half a teaspoon of baking powder. Roll walnut-sized balls, space them well apart, and "
          "bake at 180C (160C fan) for 10 to 12 minutes - they firm up as they cool.",
          avoid=("leftover", "stale", "freeze", "freezer", "raw", "dog", "digestive", "rich tea",
                 "chewy", "chewier", "chewiness", "gooey", "squidgy", "soft centre",
                 "oat", "oats", "ginger", "shortbread", "flapjack", "peanut", "chocolate chip",
                 "without egg", "without eggs", "no egg", "no eggs", "egg free", "egg-free", "eggless",
                 "vegan", "dairy free", "dairy-free", "flax", "aquafaba") + NO_SUGAR),
    entry("buttercream", (("icing", "buttercream", "frosting", "ice a cake", "ice the cake",
                            "icing a cake", "ice cupcakes", "icing cupcakes",
                            "cover a cake", "coat a cake", "put icing on"),
                           ("how do i make", "how to make", "recipe", "make", "for a cake",
                            "chocolate", "vanilla", "cake", "cakes", "cupcake", "cupcakes")),
          "Beat 100g soft butter with 200g icing sugar, a spoonful at a time, then a splash of "
          "milk or vanilla until it is light and spreadable. That covers the top and middle of a "
          "20cm cake; for chocolate, beat in 50g cooled melted dark chocolate.",
          avoid=("leftover", "freeze", "freezer", "keeps", "keep", "gone hard", "runny",
                 "sugar paste", "fondant", "day before", "night before", "ahead", "fridge",
                 "in advance", "days") + NO_SUGAR),
    entry("cake-piping", (("pipe", "piping", "piped", "icing bag", "piping bag", "nozzle",
                           "nozzles", "star tip", "star nozzle", "icing nozzle", "swirl",
                           "swirls", "rosette", "rosettes", "cake decorating", "decorate a cake",
                           "write on a cake", "writing on a cake", "lettering",
                           "write happy birthday", "writing happy birthday",
                           "happy birthday on", "message on a cake", "message on the cake",
                           "name on a cake", "name on the cake"),
                          ("icing", "buttercream", "frosting", "cake", "cakes", "cupcake",
                           "cupcakes", "swirl", "swirls", "rose", "roses", "rosette",
                           "rosettes", "letters", "lettering", "writing", "tip", "nozzle",
                           "bag")),
          "Stiff buttercream, or cream whipped until it holds a peak, a star nozzle and a steady "
          "squeeze: hold the nozzle 1cm above the cake, squeeze, then stop squeezing before you "
          "lift away or you get a tail. For a swirl start in the middle and spiral out; a 1M star "
          "tip does swirls and roses, a plain round tip is for writing. Chill the icing 15 minutes "
          "if it slumps, and practise on a plate first.",
          ask=("how", "what", "which", "best", "tip", "tips", "should", "can", "do i",
               "technique", "help"),
          avoid=("plumber", "plumbing", "boiler", "radiator", "leak", "leaking", "leaks", "burst",
                 "copper", "solder", "soldering", "drain", "water pipe", "pipe under", "under the",
                 "washing machine", "tap", "gutter", "lagging", "frozen pipe", "keep", "keeps",
                 "keeping", "fridge", "freezer", "leftover", "store", "storing", "days",
                 "make icing", "make buttercream", "make the icing",
                 "cover letter", "resignation", "reference", "cv", "letter of",
                 "letter to", "letter for", "letter about", "thank you letter",
                 "letter to my", "in writing", "put it in writing",
                 "love letter", "love note", "love poem", "valentine",
                 "complaint", "complain", "eulogy", "sick note",
                 "write letters to", "writing letters to",
                 "send a letter", "sending a letter", "a letter to", "letter to a",
                 "letters to",
                 "of a letter", "start of a letter", "end of a letter",
                 "beginning of a letter", "top of a letter", "in a letter")),
    entry("chocolate-cake", (("chocolate cake", "chocolate sponge"),
                              ("how do i make", "how to make", "recipe", "from scratch", "make",
                               "bake", "basic", "simple")),
          "200g plain flour, 200g sugar, 50g cocoa, 2 eggs, 150ml milk and 100g melted butter, "
          "whisked together and baked in two lined tins at 180C (160C fan) for 22 to 25 minutes. "
          "Sandwich it with buttercream or jam and it stays soft for days.",
          avoid=("leftover", "freeze", "freezer", "sink", "sank", "mug", "vegan", "gluten")),
    entry("carve-chicken", (("carve", "carving", "carved"),
                            ("chicken", "roast chicken", "turkey", "bird")),
          "Take the legs off first: cut the skin between leg and body, bend the leg outwards and "
          "cut through the joint rather than the bone. Then slice each breast across the grain "
          "from the thin end, keeping the knife flat against the carcass, and let the bird rest "
          "before you start if you can.",
          avoid=("ham", "beef", "lamb", "pork", "gammon", "joint of", "wood", "stone", "pumpkin",
                 "chicken breast", "chicken breasts", "carving knife", "carving board",
                 "soup", "soups", "stew", "casserole", "sauce", "gravy", "pizza", "dough",
                 "bread", "cake", "curry")),
    entry("soup-plain", (("soup", "soups"),
                         ("make", "homemade", "from scratch", "basic",
                          "how do i", "recipe")),
          "Soften an onion in oil for 8 to 10 minutes, add whatever vegetables you have, cover "
          "them with stock by an inch and simmer 20 minutes. Blend it if you want it smooth, and "
          "season at the end - a spoon of cream or a squeeze of lemon lifts a plain soup.",
          ask=("what", "recipe", "do you have", "got a", "any ideas", "easy",
               "soup ideas"),
          avoid=("thicken", "thick", "thicker", "watery", "runny", "freeze", "frozen", "keep",
                 "leftover", "reheat", "healthy", "calories", "tinned", "store",
                 "storing", "stored", "stock", "bought", "shop")),
    entry("pizza-home", (("pizza",),
                         ("cook", "cooking", "bake", "oven", "at home", "stone", "tray",
                          "how do i", "best way",
                          "temp", "temperature", "gas mark", "how hot", "degrees", "heat",
                          "oven setting", "what setting", "fan")),
          "Heat the oven as high as it goes with a heavy tray or a pizza stone inside, then slide "
          "the pizza onto the hot tray and give it 8 to 12 minutes, until the edge blisters and "
          "the underside is crisp: a thin base and a preheated surface do what an oven alone will "
          "not. Keep the toppings light, because too much sauce or cheese steams the middle.",
          avoid=("base", "dough", "yeast", "flour", "make", "making", "from scratch", "recipe",
                 "freeze", "frozen", "leftover", "reheat", "takeaway", "order", "delivery",
                 "healthy", "calories")),
    entry("pesto-bitter", (("pesto",),
                           ("bitter", "bitterness", "taste", "tastes", "fix")),
          "Bitterness is usually the raw garlic and the pine nuts: toast the nuts, use half a "
          "small clove, and stir in a handful of parsley or a squeeze of lemon at the end. Blitz "
          "in short pulses, because blending for a long time warms the basil and turns it bitter, "
          "and keep it in the fridge under a film of oil for a week.",
          avoid=("grow", "growing", "plant", "plants", "garden"), bias=1),
    entry("pesto-thick", (("pesto",), ("thick", "thickens", "stodgy", "dry", "claggy")),
          "Too thick: loosen it with a spoon of the water the pasta cooked in, or a squeeze of "
          "lemon, and taste again - the starch in pasta water binds it back to the basil instead of "
          "just thinning it out. Add more oil only at the end, a little at a time.",
          avoid=("grow", "growing", "plant", "plants", "garden"),
          bias=2),
    entry("pesto-thin", (("pesto",), ("thin", "runny", "watery", "soggy", "loose")),
          "Too runny: dry the basil properly after washing and blitz in more ground nuts and "
          "parmesan, a spoon at a time, rather than more oil, which is usually what made it sloppy "
          "in the first place. A soggy pesto is wet leaves, so spin them dry and start again.",
          avoid=("grow", "growing", "plant", "plants", "garden"), bias=2),
    entry("pesto-brown", (("pesto",), ("brown", "browns", "browned", "black", "dark")),
          "Brown pesto is the basil oxidising where the air reaches it, not spoilage: press it flat "
          "in the jar and cover the surface with a film of olive oil, and stir a squeeze of lemon "
          "through before you serve it. It is still good to eat for a few days if it was in the "
          "fridge and smells fine.",
          avoid=("grow", "growing", "plant", "plants", "garden"), bias=2),
    entry("pesto-freeze", (("pesto",), ("freeze", "freezing", "frozen", "freezer", "ice cube",
                                       "ice cubes", "make ahead", "day before")),
          "Pesto freezes better than it keeps: spoon it into an ice-cube tray, freeze it, tip the "
          "cubes into a bag, and drop one straight into hot pasta. In the fridge it is good for "
          "about a week, best with a film of olive oil over the surface.",
          bias=1),
    entry("pesto-nuts", (("pesto",), ("nut", "nuts", "allergy", "allergic", "pine", "pine nuts",
                                      "substitute", "instead", "swap")),
          "Pine nuts are the classic and sunflower seeds or cashews are the usual swap, about the "
          "same weight; toast whichever you use first, because raw seeds taste flat and pine nuts "
          "turn bitter once they are brown.",
          bias=1),
    entry("pesto-vegetarian", (("pesto",), ("vegetarian", "vegan", "parmesan", "cheese", "rennet",
                                            "dairy")),
          "Most shop pesto is not vegetarian: parmesan is made with animal rennet and jars "
          "usually use it. Buy one marked vegetarian, or make it with a vegetarian hard cheese, "
          "and leave the cheese out altogether for vegan.",
          bias=2),
    entry("pesto-salt", (("pesto",), ("salt", "salty", "too salty", "oversalted", "saltier",
                                         "seasoning", "seasoned")),
          "Pesto is saltier than it tastes because the parmesan and pecorino carry it, so add a "
          "pinch only after the cheese is in. If it has gone too salty, stir through more basil, "
          "ground nuts or a spoon of breadcrumbs and finish with a squeeze of lemon; more cheese "
          "only makes it worse.",
          avoid=("grow", "growing", "plant", "plants", "garden", "blood pressure", "daily",
                 "too much salt in my diet"),
          bias=2),
    entry("rusty-cake-tin", (("cake tin", "cake tins", "baking tin", "loaf tin", "springform",
                              "sandwich tin", "traybake tin", "brownie tin"),
                             ("rusty", "rust", "rusted", "rusting")),
          "Surface rust is harmless: scrub it off with a green scourer, dry the tin, and line it "
          "with baking paper so the cake never touches the metal. Replace a tin that has rusted "
          "right through, or whose coating is flaking into the food.",
          avoid=("grow", "growing", "plant", "plants", "garden", "gate", "car", "bike"),
          bias=2),
    entry("smoke-meat",
          (("smoke", "smoking", "smoked", "smoker", "bbq", "barbecue", "barbeque", "low and slow",
            "wood chips", "pellet grill"),
           ("brisket", "ribs", "rib", "pork", "pulled pork", "shoulder", "chicken", "turkey",
            "wings", "sausage", "sausages", "salmon", "trout", "mackerel", "haddock", "fish",
            "cheese", "tofu", "beef", "steak", "lamb", "duck", "meat")),
          _smoke_food,
          avoid=("quit", "stop smoking", "gave up", "give up", "nicotine", "cigarette",
                 "cigarettes", "vape", "vaping", "patch", "patches", "pack a day", "craving",
                 "smoke alarm", "smoke detector", "alarm", "detector", "carbon monoxide",
                 "chimney", "bonfire", "exhaust", "engine", "car", "diesel", "fireplace",
                 "wood burner", "log burner", "oven", "grill pan", "oil", "frying", "burnt",
                 "smells", "smelling", "smell", "smoky kitchen", "toaster"),
          ask=("how", "what", "which", "temperature", "temp", "long", "time", "when", "recipe",
               "should i", "do i"),
          guard=_asks_about_a_smoker,
          bias=3),
]

KEEP_HOW = ("keep", "keeps", "keeping", "stay", "stays", "stop", "stopping")

KEEP_QUALITIES = ("sticking", "stick", "sticks", "stuck", "together", "al dente",
                  "warm", "hot", "heated",
                  "moist", "juicy", "tender", "succulent",
                  "crisp", "crispy", "crunchy")

_KEEP_FOOD = ("pasta", "spaghetti", "noodles", "noodle", "rice", "potato", "potatoes", "chips",
              "mash", "vegetables", "veg", "greens", "broccoli", "carrots", "beans", "peas",
              "meat", "steak", "beef", "chicken", "turkey", "pork", "lamb", "gammon", "ham",
              "sausage", "sausages", "bacon", "fish", "salmon", "cod", "prawns", "eggs",
              "pancakes", "soup", "stew", "curry", "casserole", "cakes", "cake", "bread",
              "pastry", "pasties", "buns", "joint", "roast", "breast", "thigh", "thighs",
              "chop", "chops", "cutlets", "wings", "halloumi", "tofu", "couscous", "squash",
              "paneer", "pilaf", "risotto", "pie", "pizza", "wedges",
              "yorkshire", "yorkshires", "yorkshire pudding", "yorkshire puddings",
              "stuffing", "gravy", "bread sauce", "cranberry sauce", "apple sauce",
              "burger", "burgers", "hot dog", "hot dogs", "sausage roll", "sausage rolls",
              "naan", "naans", "tortilla", "tortillas", "pitta", "pittas", "pita", "pitas",
              "chapatis", "mushey peas", "mushy peas", "dumplings", "pigs in blankets",
              "baguette", "baguettes", "ciabatta", "bagels", "cob", "cobs", "roll", "rolls")

_KEEP_MEAT = ("meat", "meats", "steak", "steaks", "mince", "joint", "chop", "chops", "thigh",
              "thighs", "wings", "cutlets", "ribs", "fillet", "loin", "stewing steak",
              "meatballs", "chicken")

_KEEP_GRAIN_WORDS = {"pasta", "spaghetti", "noodles", "noodle", "couscous"}
_KEEP_STACK_WORDS = {"pancakes", "cake", "cakes", "bread", "buns", "pastry", "pasties",
                     "waffles", "yorkshire", "yorkshires"}

_KEEP_FLATBREAD_WORDS = {"naan", "naans", "tortilla", "tortillas", "pitta", "pittas", "pita",
                         "pitas", "chapatis", "baguette", "baguettes", "ciabatta", "bagels",
                         "cob", "cobs", "roll", "rolls",
                         "garlic bread"}

_KEEP_POUR_WORDS = {"gravy", "bread sauce", "cranberry sauce", "apple sauce", "custard",
                    "onion gravy", "jus"}

_KEEP_COVERED_WORDS = {"stuffing", "burgers", "burger", "hot dogs", "hot dog", "sausage rolls",
                       "sausage roll", "pigs in blankets", "dumplings", "meatballs"}
_KEEP_CRISP_HELD_WORDS = {"potatoes", "potato", "chips", "wedges", "mash"}

_KEEP_STICK_WORDS = {"sticking", "stick", "sticks", "stuck", "together", "al dente"}
_KEEP_HOT_WORDS = {"warm", "hot", "heated"}
_KEEP_SOFT_WORDS = {"moist", "juicy", "tender", "succulent"}

_KEEP_BOILED = ("pasta", "spaghetti", "noodles", "noodle", "potato", "potatoes", "chips",
                "vegetables", "veg", "greens", "broccoli", "carrots", "beans", "peas",
                "dumplings", "gnocchi", "couscous")


def _keep_how(memory, reading):
    words = set(reading.get("words") or ())
    if not words.intersection(KEEP_QUALITIES) or not words.intersection(_KEEP_FOOD):
        return None
    if words & _KEEP_STICK_WORDS:
        if "rice" in words:
            return None
        if not words.intersection(_KEEP_BOILED):
            return None
        return ("Stir it once as it goes in and once more a minute later, keep the water at a "
                "rolling boil with room for the pieces to move, and lift it out with tongs or a "
                "spider rather than tipping it into a colander. Oil in the water does nothing - "
                "it floats - but a splash of oil through it after draining stops it setting into "
                "one lump.")
    if words & _KEEP_HOT_WORDS:
        if {"garlic", "bread"} <= words:
            words = words | {"garlic bread"}
        if "rice" in words:
            return ("Lid on and off the heat, with a folded tea towel over the pan under the lid: "
                    "rice holds warm that way for 20 to 30 minutes, and an hour or two in a "
                    "covered dish in an oven on 80C with a splash of water is the limit. That "
                    "limit is not fussiness - cooked rice left standing warm grows bacillus "
                    "cereus, so past two hours cool it fast and reheat it once, thoroughly.")
        held = ("Hold it hot rather than hotting it up later: an oven on its lowest, a slow "
                "cooker on low, or a bowl over a pan of simmering water, all covered, which keeps "
                "food above 63C where bacteria stop multiplying. ")
        if words & _KEEP_GRAIN_WORDS:
            return held + ("Keep back a cup of the cooking water and stir it through so nothing "
                           "sets into a block, and do not leave it warm for more than an hour or "
                           "two.")
        if words & _KEEP_POUR_WORDS:
            return ("Stand the jug in a pan of simmering water on the lowest ring, or pour it "
                    "into a flask, and give it a stir every so often: a sauce left on the hob "
                    "catches, and one left standing still grows a skin. Loose it with a splash of "
                    "stock or milk before it goes out, and an hour or two is as long as it holds.")
        if words & _KEEP_COVERED_WORDS:
            return ("A covered dish in the oven on its lowest, with a splash of stock "
                    "or water in the bottom so the edges do not dry: in one layer rather than "
                    "piled up, and uncovered if it is meant to stay crusty. An hour or two is "
                    "the limit - after that it is a leftover, and a leftover is cooled fast and "
                    "reheated once.")
        if words & _KEEP_FLATBREAD_WORDS:
            return ("Keep them wrapped and close together - a clean tea towel or foil - in the "
                    "low oven, or give each one a minute a side in a warm dry pan. A lid or a "
                    "covered dish steams a flatbread soft, and it dries out in the open, so ten "
                    "to fifteen minutes in the cloth is all it needs.")
        if words & _KEEP_STACK_WORDS:
            return held + ("Stack them on a plate under a clean tea towel, rather than under a "
                           "lid or foil, which traps the steam and leaves them limp, and do not "
                           "hold them warm for more than an hour or two.")
        if words & _KEEP_CRISP_HELD_WORDS:
            return held + ("One layer on a tray, uncovered, not piled in a bowl where they "
                           "steam and go soft, and do not leave them warm for more than an hour "
                           "or two.")
        return held + ("Cover it and do not leave it warm for more than an hour or two.")
    if words & _KEEP_SOFT_WORDS:
        if not words.intersection(_KEEP_MEAT):
            return None
        return ("Juiciness is decided before the pan and lost at the end: salt the meat 40 "
                "minutes ahead or soak it in brine, cook it to 74C in the middle for chicken and "
                "pork (54C for beef you want pink), and rest it under loose foil for 10 minutes "
                "so the juices settle back into the fibres. Then slice across the grain, not "
                "along it.")
    return ("Crisp survives only in the open: cool anything fried or roasted in one layer on a "
            "rack or a paper-lined tray, never in a pile or a closed tub, where the steam turns it "
            "soft within minutes. Then reheat it 4 to 5 minutes at 200C on a bare tray, not in a "
            "microwave. A dry surface before it goes in the fat is the other half of it.")


ENTRIES.append(entry("keep-how", (KEEP_HOW, KEEP_QUALITIES, _FOOD), _keep_how, bias=-1,
                     ask=KEEP_QUALITIES,
                     avoid=("party", "parties", "buffet", "guests", "for a crowd",
                            "how long", "how many", "recipe", "recipes", "fridge",
                            "freezer", "freeze", "next day", "tomorrow", "reheat",
                            "lettuce", "salad", "leaves", "spinach", "rocket", "watercress",
                            "celery", "cucumber", "cabbage", "herb", "herbs",
                            "pan", "pans", "wok", "tray", "risotto", "porridge",
                            "quinoa", "breast", "breasts", "turkey", "beef", "pork", "lamb",
                            "salmon", "cod", "fish", "prawns", "bacon", "cake",
                            )))


ENTRIES.append(entry(
    "ribs-low-and-slow",
    (("ribs", "rib", "spare ribs", "short ribs", "pork ribs", "baby back ribs", "beef ribs",
      "pork rib"),
     ("cook", "cooking", "oven", "bake", "baked", "roast", "roasted", "slow cooker",
      "slow-cooker", "crockpot", "crock pot", "tender", "long", "time", "temperature", "temp",
      "how", "glaze", "glazed", "fall off the bone")),
    ("Ribs want low and slow: 2 to 2.5 hours covered at 150C (130C fan) with a splash of water "
     "in the tray, then 15 minutes uncovered at 220C (200C fan) with a glaze to sticky them up. "
     "In a slow cooker it is 6 to 8 hours on low, then 10 minutes under the grill. They are done "
     "when the meat has pulled back from the bone and a fork twists in it easily."),
    avoid=("smoke", "smoked", "smoking", "smoker", "low and slow", "wood chips", "pellet grill",
           "last night", "yesterday", "we had", "we ate", "turned out", "came out",
           "hurt", "hurts", "hurting", "pain", "ache", "aches", "breathing", "breathe", "cough",
           "bruise", "bruised", "broken", "cracked", "cage", "x ray", "x-ray",
           "prime rib", "ribeye", "rib eye", "rib cap", "ribs recipe for a crowd",
           "how much", "cost", "costs", "price", "prices", "cheap", "expensive", "afford",
           "reheat", "reheating", "reheated", "leftover", "leftovers", "warm up", "warmed up",
           "microwave", "air fryer", "freeze", "freezer", "frozen"),
    bias=2))


ENTRIES.append(entry(
    "prick-sausages",
    (("sausage", "sausages", "banger", "bangers", "chipolata", "chipolatas", "bratwurst",
      "frankfurter", "frankfurters", "hot dog", "hot dogs"),
     ("prick", "pricked", "pricking", "prick them", "pierce", "pierced", "stab", "stabbed",
      "split", "splits", "splitting", "burst", "bursts", "bursting", "skin", "skins")),
    ("No - leave them whole. Pricking lets the fat and juice run out into the pan, so they come "
     "out drier, and it is fast high heat that splits a skin, not a skin that went unpricked: "
     "cook them at 180C (160C fan) for 25 to 30 minutes, or in a pan on a medium heat, turning "
     "them now and then, and let them colour slowly. A thick one that splits anyway is still "
     "fine to eat - it has just tightened faster than the inside cooked."),
    avoid=("how long", "minutes", "how many", "calories", "healthy", "freeze", "freezer",
           "fridge", "keep", "reheat", "how much", "cost", "price", "recipe", "make my own",
           "finger", "thumb", "injection", "vaccine", "blood", "diabetes", "glucose"),
    bias=2))

ENTRIES.append(entry(
    "jelly-wont-set",
    (("jelly", "jello", "gelatine", "gelatin", "blancmange"),
     ("set", "sets", "setting", "didnt set", "wont set", "wont", "runny", "liquid", "firm",
      "wobbly", "solid", "why", "how much", "how many", "leaves", "powder")),
    ("Jelly is measured by liquid: 4 leaves of gelatine, or 2 teaspoons of powder, to every pint "
     "(570ml), then 4 hours in the fridge - overnight to be sure. Fresh pineapple, kiwi, papaya, "
     "mango and figs have an enzyme that stops gelatine setting, so simmer those for 2 minutes "
     "first or the jelly stays liquid. Still runny after that? Melt it gently and stir in one more "
     "leaf per pint."),
    avoid=("jam", "marmalade", "setting point", "104", "105", "pectin", "boil", "boiling",
           "bramble", "blackberry", "blackberries", "crab apple", "rowan", "quince", "damson",
           "sloe", "sloes", "redcurrant", "red currant", "gooseberry", "elderflower", "cranberry",
           "mint jelly", "apple jelly", "sugar", "thermometer", "preserve", "preserves", "chutney",
           "how long does jelly keep", "keep", "keeps", "fridge life", "sweets", "candy",
           "royal jelly", "jellyfish", "jelly bean", "jelly shoes"),
    bias=2))

ENTRIES.append(entry(
    "peas-that-stay-hard",
    (("peas", "pea", "marrowfat", "garden peas", "frozen peas", "split peas"),
     ("hard", "tough", "woody", "wont soften", "wont go soft", "still hard", "not soft",
      "crunchy", "chalky", "like bullets", "bitter", "old")),
    ("Peas that stay hard are usually old: the sugar has turned to starch and no amount of cooking "
     "brings them back. Frozen garden peas need 2 to 3 minutes in boiling water, fresh ones 3 to 5. "
     "Marrowfat and other big dried peas want a soak overnight and 40 minutes of simmering, and a "
     "quarter teaspoon of bicarbonate of soda in the water helps them soften. Acid is the other "
     "culprit - lemon juice or tomatoes in the pan keep peas firm - so add those at the end."),
    avoid=("runner", "runners", "bean", "beans", "string", "stringy", "strings", "de-string",
           "sow", "sowing", "plant", "planting", "grow", "growing", "allotment", "climbing",
           "sweet pea", "sweet peas", "flower", "seed", "seeds", "germinate", "sprout",
           "protein", "calories", "healthy", "nutrition"),
    bias=2))

ENTRIES.append(entry(
    "bread-machine-loaf-failed",
    (("bread machine", "breadmaker", "bread maker", "bread-mixer", "dough hook"),
     ("failed", "fail", "didnt work", "not working", "brick", "flat", "sank", "dense", "heavy",
      "no rise", "didnt rise", "collapsed", "stodgy", "raw", "sunken")),
    ("A brick out of a bread machine is nearly always the yeast: check the date, keep it and the "
     "salt apart in the tin (salt kills yeast on contact), and use water at 20 to 25C, because hot "
     "water kills it just as well. Half a teaspoon of dried yeast to 500g of strong white flour is "
     "the other thing to check. If the dough never rose the yeast is dead; if it rose and then "
     "fell, there was too much of it or the salt went in with it."),
    avoid=("oven temperature", "oven thermometer", "fan oven", "temperature of the oven",
           "by hand", "by-hand", "sourdough", "knead", "kneading", "flour", "which flour",
           "recipe", "buy", "which machine", "best machine", "worth it", "cost", "price",
           "clean", "cleaning", "paddle", "pan stuck"),
    bias=2))
COLD_CUP_NAMES = ("tea", "coffee", "soup", "broth", "stew", "gravy", "porridge", "hot chocolate",
                  "cuppa", "brew", "drink", "dinner", "food", "plate", "mug", "cup", "pot")

COLD_CUP_ASKS = ("going cold", "goes cold", "gone cold", "keeps going cold", "keeps cold",
                 "keep going cold", "cold before", "lukewarm", "gone lukewarm", "stone cold",
                 "keep it hot", "keep hot", "keeps it hot", "keep my tea hot", "keep tea hot",
                 "keep my coffee hot", "keep the soup hot", "keep soup hot", "stays hot",
                 "stay hot", "staying hot", "goes warm", "gone warm",
                 "keep it warm", "keep warm", "keeps warm", "keep my tea warm", "keep tea warm",
                 "keep my coffee warm", "keep coffee warm", "keep the soup warm", "stays warm",
                 "stay warm", "staying warm",
                 "warm it up", "warm it back up", "cold by the time")

ENTRIES.append(
    entry("a-cup-going-cold", (COLD_CUP_NAMES, COLD_CUP_ASKS),
          "Warm the cup or the bowl first: fill it with boiling water, leave it a minute, tip it "
          "out and then fill up, because a cold mug takes most of the heat out in the first "
          "minute. A lid or a tea cosy keeps a drink hot far longer than a bigger pot does, and a "
          "flask is the only thing that holds it for hours, so make a smaller pot and top it up. "
          "For soup, a deeper bowl keeps the heat in better than a wide shallow one, and warming "
          "the bowls with hot water before you serve buys another few minutes.",
          ask=COLD_CUP_ASKS,
          avoid=("i have a cold", "have a cold", "my cold", "a bad cold", "head cold", "chesty",
                 "sore throat", "runny nose", "cough", "coughing", "sneez", "flu", "temperature",
                 "fever", "virus", "symptom", "day of work", "fridge", "freezer", "frozen",
                 "ice", "iced", "cold brew", "ice cream", "cold sore", "cold water", "recipe",
                 "how do i make", "how do you make", "kettle", "coffee machine", "brew time",
                 "reheat", "reheating", "reheat it", "warm up the leftover", "leftovers"),
          bias=3))

_RICE_PUDDING_SLOW = (
    "3 to 4 hours on low. Butter the slow cooker pot and put in 60g pudding rice, 700ml whole "
    "milk, 100ml cream, 40g sugar and a strip of lemon peel or a bay leaf: the extra milk is "
    "there because nothing evaporates in a slow cooker. Stir once after an hour and then leave "
    "the lid on, because lifting it drops the heat. Take the lid off for the last 30 minutes if "
    "you want the top to catch, and loosen it with milk before it goes into bowls.")
_RICE_PUDDING_MICROWAVE = (
    "About 25 minutes. Use a big bowl, because it swells and boils up, and put in 60g pudding "
    "rice, 600ml whole milk, 40g sugar and a strip of lemon peel. Microwave on high for 10 "
    "minutes, stir, then 8 minutes, stir, then 5 minutes at a time until the rice is soft. It "
    "carries on cooking as it stands, so stop while it is still a little loose, and finish it "
    "under the grill if you want a browned top.")
_RICE_PUDDING_PRESSURE = (
    "20 minutes on high pressure with a 10 minute natural release: 60g pudding rice, 600ml whole "
    "milk, 40g sugar and a strip of lemon peel in a dish on a trivet over water. Do not fill the "
    "pot more than half way, because milk froths up through the valve. Loosen it with milk once "
    "the pressure is down, and grill the top if you want it browned.")


def _rice_pudding_pot(memory, reading):
    said = str(reading.get("clean") or " ".join(reading.get("words") or [])).lower()
    if any(one in said for one in ("pressure cooker", "instant pot", "multicooker")):
        return _RICE_PUDDING_PRESSURE
    if any(one in said for one in ("microwave", "microwaved", "microwaving")):
        return _RICE_PUDDING_MICROWAVE
    return _RICE_PUDDING_SLOW


ENTRIES.append(entry(
    "rice-pudding-pot",
    (("rice pudding", "rice puddings"),
     ("slow cooker", "slowcooker", "slow-cooker", "crockpot", "crock pot", "microwave",
      "microwaved", "microwaving", "pressure cooker", "instant pot", "multicooker")),
    _rice_pudding_pot,
    avoid=("keep", "keeps", "keeping", "last", "lasts", "reheat", "reheating", "leftover",
           "leftovers", "shelf life", "gone off", "stale", "calories", "how much", "how many",
           "without", "vegan", "dairy free", "tin", "tinned", "shop", "buy", "rice cake",
           "rice cakes", "rice crispy", "rice crispies", "already made", "shop bought"),
    ask=("slow cooker", "slowcooker", "slow-cooker", "crockpot", "crock pot", "microwave",
         "microwaved", "microwaving", "pressure cooker", "instant pot", "multicooker"),
    bias=2))
_VEGETARIAN_FOODS = (
    (("parmesan", "parmesan cheese", "grana padano", "pecorino", "pecorino romano"),
     "Probably not: Parmesan, Grana Padano and Pecorino are set with animal rennet, which comes "
     "from the stomach of a calf or a lamb, so the traditional ones are not vegetarian. Some "
     "supermarket versions use microbial rennet instead - the ingredient list or the Vegetarian "
     "Society logo is the only way to tell."),
    (("gelatin", "gelatine", "jelly", "jelly cubes", "marshmallow", "marshmallows", "haribo",
      "gummy sweets", "gummy bears", "gummies", "wine gums", "jelly babies", "chewy sweets"),
     "Not if the packet says gelatin or gelatine: that is made from pork or beef skin and bone, so "
     "jelly, marshmallows, jelly babies and most gummy sweets are out. The vegetarian versions set "
     "with pectin, agar or carrageenan instead, and they say so on the front."),
    (("worcestershire sauce", "worcester sauce", "worcestershire"),
     "Not the ordinary Lea & Perrins: Worcestershire sauce is made with anchovies, so it is "
     "neither vegetarian nor vegan. Anchovy-free versions exist, and a splash of soy sauce or "
     "balsamic does the same job in a stew or a cheese on toast."),
    (("caesar dressing", "caesar salad", "caesar"),
     "No, not a classic one: Caesar dressing has anchovies and Parmesan, so the dressing and the "
     "salad with it are not vegetarian. Vegetarian versions swap the anchovy for capers and use a "
     "hard cheese made with microbial rennet."),
    (("pesto", "green pesto", "pesto sauce"),
     "Usually not: jarred pesto is made with Parmesan or Pecorino, and both are set with animal "
     "rennet. Look for one labelled vegetarian, or make it with a vegetarian hard cheese - the "
     "basil, pine nuts, garlic and oil are all fine."),
    (("chips", "fries", "chip shop chips", "french fries"),
     "Usually yes - potatoes and oil - but chip-shop chips can be fried in beef dripping, which is "
     "traditional in the north, and a shop that fries them in the same oil as the fish is a no for "
     "some people. Ask, or use oven chips and read the packet."),
    (("croissant", "croissants", "pastry", "pastries", "danish", "pain au chocolat",
      "puff pastry", "shortcrust"),
     "Yes: a croissant is flour, butter, yeast, sugar and egg, all of which are vegetarian, though "
     "not vegan. Ordinary pastry is vegetarian too, with one exception - some savoury pie pastry "
     "still lists lard, so read the packet before you assume."),
    (("stock cube", "stock cubes", "stock", "gravy", "gravy granules", "bouillon"),
     "Read the packet: plenty of chicken and beef stock cubes are actually vegetarian, and plenty "
     "of 'vegetable' gravies have meat fat in them. The vegetarian ones are labelled, and a "
     "vegetable stock cube with a dash of soy sauce covers the same ground."),
    (("feta", "feta cheese"),
     "Usually yes: most supermarket feta is made with microbial rennet and says so on the back, "
     "while the traditional barrel-aged Greek and Bulgarian sorts use animal rennet, so read the "
     "label before you count on it."),
    (("halloumi", "halloumi cheese"),
     "Often not: most halloumi is made with animal rennet, so look for vegetarian on the packet or "
     "the Vegetarian Society logo. The vegetarian versions grill and squeak the same way."),
    (("cheese", "cheddar", "mozzarella", "brie", "cottage cheese", "cream cheese"),
     "Most cheese is fine, but the hard ones - Parmesan, Grana Padano, Pecorino, and some "
     "traditional cheddars - are set with animal rennet. Cheddar, mozzarella and cottage cheese "
     "are usually made with microbial rennet, and the Vegetarian Society logo settles it."),
    (("wine", "beer", "cider", "ale", "lager", "stout"),
     "It may not be, technically: wine and beer are often fined with isinglass from fish swim "
     "bladders, gelatin or egg white, and the fining agent never appears on the label. Most "
     "supermarket bottles now print 'suitable for vegetarians', so buy one that does."),
    (("rice", "pasta", "bread", "noodles", "flour", "potatoes"),
     "Yes: rice, pasta, noodles, flour and potatoes are vegetarian, and bread almost always is - "
     "the exception is lard in some traditional loaves. Egg pasta is still vegetarian, it is only "
     "vegan that rules it out."),
    (("chocolate", "milk chocolate", "dark chocolate"),
     "Usually yes: cocoa, milk and cocoa butter are all vegetarian. Check the bar for gelatin in "
     "chewy or marshmallow fillings, and remember whey is fine for a vegetarian but not for a "
     "vegan."),
)
_VEG_SHAPE = ("is", "are", "was", "were", "ok", "okay", "suitable", "can i eat", "can i have",
              "can i", "does", "do", "safe", "fine", "allowed", "eat", "edible")
for _names, _verdict in _VEGETARIAN_FOODS:
    ENTRIES.append(entry("is-veg-" + _names[0].replace(" ", "-"), (_names, _VEG_SHAPE), _verdict,
                         ask=("vegetarian", "veggie"), bias=2))


ENTRIES.append(entry(
    "vegetarian-label",
    (("vegetarian", "veggie"),
     ("how do i know", "how can i tell", "how to tell", "check", "checking", "label", "labels",
      "look for", "look out", "watch out", "ingredients", "hidden", "sure", "certain", "find out",
      "what to look", "packet", "packets")),
    ("Read the ingredient list for the four that catch people out: rennet (animal, in hard cheese), "
     "gelatin (pork or beef, in sweets and jelly), anchovy (Worcestershire sauce, Caesar dressing) "
     "and lard or suet (pastry, some bread). The Vegetarian Society logo, a green V or the words "
     "'suitable for vegetarians' settle it faster than any list, and 'may contain fish' means the "
     "same fryer or the same factory rather than an ingredient."),
    avoid=("dinner", "tea", "lunch", "breakfast", "meal", "meals", "cook", "cooking", "recipe",
           "recipes", "ideas", "restaurant", "menu", "protein", "iron", "b12", "child",
           "children", "kids", "guest", "guests", "party", "cut down", "going vegetarian",
           "become", "start being", "im vegetarian", "i am vegetarian"),
    bias=1))

ENTRIES.append(entry(
    "tenderise-cheap-meat",
    (("tenderise", "tenderize", "tenderising", "tenderizing", "tenderise it", "tender",
      "tough steak", "tough meat", "cheap cut", "cheap steak", "cheap meat",
      "skirt steak", "skirt steaks", "flank", "chewy"),
     ("how do i", "how to", "make", "makes", "make it", "best way", "stop it being", "too tough",
      "chewy", "softer", "soften", "marinade", "marinate", "salt")),
    ("Salt it an hour ahead - a good pinch per side, left uncovered in the fridge - or marinate it "
     "30 minutes to an hour in something acidic: lemon juice, wine, buttermilk or yoghurt. Then "
     "cut across the grain in thin slices, which does more for a chewy steak than any marinade, "
     "and cook it fast over high heat to no more than medium, or braise it slowly for hours if it "
     "is a stewing cut like shin, chuck or brisket. A bash with a rolling pin between two sheets "
     "of baking paper works for thin cuts like flank and skirt."),
    avoid=("how long", "medium rare", "rare", "temperature", "sear", "searing", "pan", "grill",
           "barbecue", "bbq", "oven", "roast", "rest", "resting", "freezer", "frozen",
           "thaw", "defrost", "keep", "leftover", "leftovers",
           "slow cooker", "slow cook", "slow cooked", "slow cooking", "casserole", "stew",
           "stews", "stewing", "braise", "braised", "braising", "brisket", "shin", "chuck",
           "oxtail", "pot roast", "pressure cooker", "air fryer",
           "how do i cook", "how do i cook it", "cook a steak", "cooking a steak",
           "cook the steak", "cook my steak", "fry a steak", "frying a steak",
           "skirting", "skirting board", "skirting boards", "skirt board", "skirt boards",
           "paint", "paints", "painting", "repaint", "painted", "gloss", "satin", "emulsion",
           "undercoat", "woodwork", "primer"),
    bias=1))

NO_APPLIANCE = ("no oven", "without an oven", "without the oven", "dont have an oven",
                "don't have an oven", "havent got an oven", "haven't got an oven",
                "got no oven", "no hob", "without a hob", "dont have a hob",
                "don't have a hob", "havent got a hob", "haven't got a hob",
                "no microwave", "without a microwave", "dont have a microwave",
                "don't have a microwave", "havent got a microwave", "haven't got a microwave",
                "no cooker", "without a cooker", "dont have a cooker", "don't have a cooker",
                "only got a hob", "only have a hob", "only a hob", "just a hob",
                "only got a microwave", "only have a microwave", "only a microwave",
                "just a microwave", "only got a kettle", "only have a kettle", "only a kettle",
                "just a kettle", "no oven tho", "no oven though", "oven broke", "oven is broken",
                "oven doesnt work", "oven doesn't work", "oven not working", "oven is gone",
                "no oven in", "hob broke", "hob is broken", "hob doesnt work",
                "hob doesn't work", "hob not working")


def _no_appliance(memory, understood):
    if not isinstance(understood, dict):
        return None
    gone = missing(understood)
    if not gone:
        return None
    said = _line(understood)
    if any(re.search(r"\b" + re.escape(word) + r"\b", said) for word in DECIDING):
        return None

    from ..memory import last_bot

    before = str(last_bot(memory) or "").lower()
    if any(came in before for came in ("you cannot bake without an oven", "you can still eat well",
                                       "you can still eat properly", "a kettle still makes",
                                       "with an oven and no hob")):
        return None
    return without(understood)


ENTRIES.append(entry(
    "kitchen-without-an-appliance",
    (NO_APPLIANCE, ("bake", "baking", "cook", "cooking", "make", "eat", "dinner", "tea",
                    "meal", "meals", "cake", "cakes", "bread", "loaf", "biscuit", "biscuits",
                    "cookie", "cookies", "roast", "pie", "pastry", "what can i", "what should i",
                    "any ideas", "ideas", "recipe", "recipes", "tonight", "supper", "lunch",
                    "kitchen", "flat", "house", "place", "moving", "moved", "move in")),
    _no_appliance,
    avoid=("repair", "repairing", "replace", "replacing", "mend", "mending", "fix", "fixing",
           "engineer", "warranty", "guarantee", "quote", "quotes", "worth", "landlord",
           "landlady", "letting agent", "buy", "buying", "cost", "cheap", "best", "which one",
           "recommend", "brand", "install", "installing", "fit", "fitting", "fuse", "element",
           "thermostat", "fan", "door", "seal", "gas", "electric", "energy", "bill", "bills",
           "pudding", "puddings", "dessert", "desserts"),
    bias=2))
ENTRIES.append(entry(
    "duck-eggs",
    (("duck egg", "duck eggs", "ducks egg", "ducks eggs"),
     ("boil", "boiled", "boiling", "cook", "cooking", "same", "work", "works", "how long",
      "how", "use", "bake", "baking", "substitute", "instead", "too", "runny", "hard", "eat",
      "longer", "take longer", "more time", "difference", "differently", "differ")),
    "A duck egg takes about a minute longer than a hen's: 7 to 8 minutes for a runny yolk and 11 "
    "for hard boiled, from already boiling water. It is bigger, the white sets firmer and the yolk "
    "is richer, which is why it is good in baking and fried; cook it exactly like a hen's egg, "
    "cool it under the tap before peeling, and keep it in the fridge like any egg.",
    bias=3,
    avoid=("safe", "safely", "raw", "salmonella", "pregnant", "baby",
           "pond", "garden", "weed", "duckweed", "roast", "crispy", "confit", "feed",
           "feeding", "pet", "the ducks"),
))


_SMOKED_FISH = ("smoked haddock", "smoked mackerel", "smoked trout", "smoked fish", "kippers",
                "kipper", "smoked herring")
_SMOKED_FISH_REPLY = (
    "Smoked {fish} is already cooked, so it only wants heating through: 3 to 4 minutes under a hot "
    "grill, or 4 to 5 minutes in milk that is barely simmering, which keeps it moist. Flake it "
    "while it is warm into a fish pie, scrambled eggs or a salad with a squeeze of lemon.")


SMOKED_SALMON_ALREADY = (
    "Smoked salmon is cured rather than cooked, so it needs no cooking at all: eat it cold on "
    "bread with a squeeze of lemon and black pepper, or warm it through at the very end - folded "
    "into hot pasta, a risotto or scrambled eggs off the heat - because heat turns it firm and "
    "salty. Do not fry or bake it.")


def _smoked_fish_reply(memory, reading):
    said = str((reading or {}).get("text") or "").lower()
    if "smoked salmon" in said or "lox" in said:
        return SMOKED_SALMON_ALREADY
    return _SMOKED_FISH_REPLY.format(fish=_smoked_fish(reading))


def _smoked_fish(reading):
    said = str((reading or {}).get("text") or "").lower()
    for name in _SMOKED_FISH:
        if name in said:
            if name in ("kipper", "kippers", "smoked herring"):
                return "kipper"
            return name[len("smoked "):] if name.startswith("smoked ") else name
    return "haddock"

ENTRIES.append(entry(
    "smoked-fish",
    (("smoked haddock", "smoked mackerel", "smoked trout", "smoked fish", "kipper", "kippers",
      "smoked herring", "smoked salmon", "lox"),
     ("cook", "cooking", "heat", "hot", "grill", "grilled", "poach", "poached", "serve", "eat",
      "how", "best way", "what do i do", "what can i do", "warm", "warm up")),
    _smoked_fish_reply,
    avoid=("gravad", "gravlax", "healthy", "healthier", "omega",
           "pregnant", "pregnancy", "freeze", "frozen", "keep", "how long", "hot smoke",
           "cold smoke", "smoker", "wood chips", "low and slow", "barbecue", "bbq"),
    bias=2))
