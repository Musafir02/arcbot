import re

from ..understanding import line_as_read
from .dishes import KEEP_QUALITY_WORDS, PLAN_NAMES
from .keeping_cooked import COOKED_KEEP_ASK, COOKED_KEEP_AVOID, COOKED_KEEPS
from .lookup import (entry, find, kinds_entries, says_it_has_gone_off as _says_it_has_gone_off,
                     TOOTH_OR_GUM)
from .meals import NOT_MINE_ENTRY as _NOT_MINE, says_a_diet as _says_a_diet
from .bake_faults import (_BAKE_FAULT, _BAKE_FAULT_FAMILIES, _BAKE_THING,
                          _bake_always, _bake_fault)
from .prices import a_price_is_judged
from .units import BIRD_GRAMS, people_in_groups
from .cooking_tables import (NOT_WANTED, MEAL_IDEAS, SIDES, SEASONINGS, DIET_VARIANTS, FREEZE_FACTS, FOOD_CALORIES, FOOD_NUTRIENTS, FOOD_CALORIE_MEALS, BAKES, KEEPS, PANTRY, DISHES, RECIPES)

ANSWERS = ("cooking", "food-and-drink")

BREAD_TIP = ("A slice of bread in the tin keeps them soft; 15 seconds in the microwave brings one "
             "back the next day.")
BAKED_GOODS = {
    "brownie": ("Brownies", "4 to 5 days in a sealed tin at room temperature",
                "They freeze for 3 months, cut into squares first.", BREAD_TIP),
    "blondie": ("Blondies", "4 to 5 days in a sealed tin", "They freeze for 3 months.", BREAD_TIP),
    "cookie": ("Cookies", "a week in an airtight tin",
               "The dough freezes for 3 months, shaped and ready to bake from frozen.", BREAD_TIP),
    "biscuit": ("Biscuits", "a week or two in a tin", "A baked tin freezes for 3 months.",
                BREAD_TIP),
    "muffin": ("Muffins", "2 to 3 days in a tin, best the day they are baked",
               "They freeze for 2 months.", BREAD_TIP),
    "flapjack": ("Flapjacks", "a week in a tin", "They freeze for 3 months.", BREAD_TIP),
    "oat bar": ("Oat bars", "a week in a tin", "They freeze for 3 months.", BREAD_TIP),
    "oat cracker": ("Oat crackers", "a week or two in a tin",
                    "A baked tin freezes for 3 months.", BREAD_TIP),
    "cupcake": ("Cupcakes", "2 to 3 days in a tin, unfrosted",
                "They freeze for 2 months, unfrosted.", BREAD_TIP),
    "doughnut": ("Doughnuts", "only the day you buy them", "They do not freeze well.",
                 "Ten seconds in the microwave brings one back closer to fresh than you would "
                 "think."),
}
BAKED_GOODS_WORDS = ("oat bar", "oat bars", "oat cracker", "oat crackers", "brownie", "brownies", "blondie", "blondies",
                     "cookie", "cookies",
                     "biscuit", "biscuits", "muffin", "muffins", "flapjack", "flapjacks",
                     "cupcake", "cupcakes", "doughnut", "doughnuts", "donut", "donuts")


CONTAINER_FOODS = ("jam", "pesto", "pickle", "pickles", "chutney", "marmalade", "ketchup",
                   "mustard", "mayonnaise", "mayo", "salsa", "tahini", "preserve", "preserves",
                   "olives", "gherkins", "relish")


CONTAINER_MONTHS = ("jam", "pickle", "pickles", "chutney", "marmalade", "preserve", "preserves",
                    "olives", "gherkins", "relish", "mustard", "ketchup")


def _container_keep(memory, reading):
    turns = (memory or {}).get("turns") or []
    for turn in reversed(turns[-2:]):
        said = str(turn.get("user") or "").lower() if isinstance(turn, dict) else ""
        named = [word for word in CONTAINER_FOODS if word in said]
        if named:
            food = named[0].capitalize()
            if named[0] in CONTAINER_MONTHS:
                keep = "keep" if food.endswith("s") else "keeps"
                return (f"{food} {keep} for months in the fridge once it is opened, and an opened "
                        "sauce or pesto 1 to 2 weeks. The label's once-opened line beats any "
                        "general rule, so bin it if it smells sharp or the lid bulges.")
            return (f"An opened {named[0]} is best within 1 to 2 weeks, kept in the fridge, and "
                    "the label's once-opened line beats any general rule. Bin it if it smells "
                    "sharp, looks odd or the lid bulges.")
    return ""


def _stuck_jar(memory, reading):
    line = str((reading or {}).get("text") or (reading or {}).get("clean") or "").lower()
    said = ("Tap the edge of the lid all the way round with the handle of a knife, then grip it "
            "through a rubber glove, a silicone mat or a wide rubber band - the grip is usually "
            "what is missing. If it still will not turn, stand the jar in a bowl of hot water for "
            "two minutes so the metal lid swells, or slide the back of a spoon under the rim to "
            "let air in.")
    if any(word in line for word in CONTAINER_FOODS):
        said += " Once open, jam, pickles and chutney keep for months, an opened sauce 1 to 2 weeks."
    return said


def _baked_keep():
    def reply(memory, reading):
        line = str(reading.get("text") or reading.get("clean") or "").lower()
        for name in sorted(BAKED_GOODS, key=len, reverse=True):
            if name in line:
                label, keeps, frozen, tip = BAKED_GOODS[name]
                return f"{label} keep {keeps}. {frozen} {tip}"
        return ""
    return reply


KEEP_ASK = ("how", "what", "which", "can", "could", "should", "would", "where", "is", "are",
            "does", "do i", "will",
            "worth", "ok", "okay", "safe", "still", "long", "last", "lasts", "store", "storing",
            "stored", "leftover", "leftovers", "left over", "next day", "tomorrow", "reheat",
            "gone off", "go off", "goes off", "going off", "shelf life", "shelf-life")

OPEN_ASK = ("open a tight", "open a stuck", "open a stubborn", "get the lid off",
            "get this lid off", "get the cap off", "lid is stuck", "lid stuck",
            "lid wont come off", "lid won't come off", "wont open", "won't open",
            "wont turn", "won't turn", "wont budge", "won't budge", "cant open", "can't open",
            "cannot open", "hard to open", "struggling to open", "stubborn lid", "tight lid",
            "stuck lid", "how do i open", "how to open", "how can i open")

_FOOD = ("sauce", "soup", "stew", "curry", "chilli", "casserole", "gravy", "dish", "dinner",
         "supper", "meal", "food", "cooked", "cook", "cooking", "taste", "tastes", "tasted",
         "made", "make", "fix", "fixing", "came out", "turned out", "went wrong",
         "chicken", "meat", "rice", "pasta", "cake", "bread", "pastry", "potatoes", "stir fry",
         "custard", "mash", "roast", "bake", "baking", "bolognese", "lasagne", "lasagna",
         "risotto", "pie", "cobbler", "traybake", "noodles", "eggs", "fish", "mince", "beef",
         "pork", "lamb", "vegetables", "veg", "pancakes", "porridge", "stock", "broth",
         "salt", "seasoning", "spices", "herbs", "pepper", "marinade", "dressing", "steak",
         "squid", "prawns", "bacon", "sausages", "turkey", "burgers",
         "ragu", "rag\u00f9", "bolognaise", "meatballs", "meatloaf", "tagine", "daal", "dhal",
         "biryani", "paella", "ratatouille", "goulash", "gnocchi", "hummus", "burrito", "katsu",
         "macaroni cheese", "mac and cheese", "waffles", "frittata", "ramen", "quesadilla",
         "cottage pie", "shepherds pie", "shepherd's pie", "fish pie", "quiche", "couscous",
         "pesto", "guacamole", "tapenade", "dip", "dips", "pilaf", "pilau",
         "burger", "hamburger", "falafel", "patty", "patties",
         "parsnip", "parsnips", "carrot", "carrots", "sprouts", "brussels sprouts", "cabbage",
         "kale", "leek", "leeks", "beetroot", "swede", "turnip", "cauliflower", "broccoli",
         "roast potatoes", "roast veg", "stuffing", "dumplings", "yorkshire pudding",
         "yorkshire puddings", "yorkshires", "toad in the hole", "batter", "crepe", "crepes")

_A_FAULT_SAID = ("came out", "turned out", "went wrong")
_A_TASTE = tuple(word for word in _FOOD if word not in _A_FAULT_SAID)

def _corn(understood):
    said = " " + " ".join(str(word).lower() for word in (understood.get("words") or [])) + " "
    if any(cue in said for cue in (" microwave ", " microwaved ", " microwaving ",
                                   " microwaves ", " micro ")):
        return ("In the microwave a cob takes 3 to 4 minutes on full power for one and 5 to 6 for "
                "two: leave it in its husk, or wrap it in a damp piece of kitchen paper, and turn "
                "it once. It carries on cooking as it stands, so give it a minute before you "
                "butter it. Loose kernels in a covered bowl with a splash of water take 2 to 3 "
                "minutes, stirred halfway.")
    if any(cue in said for cue in (" air fryer ", " airfryer ", " air fried ", " airfry ")):
        return ("In the air fryer rub the cobs with a little oil and give them 10 to 12 minutes at "
                "190C, turning once: the kernels blister at the tips and that is the point. Two "
                "cobs fit in a normal basket; more than that and they steam instead of browning.")
    if any(cue in said for cue in (" grill ", " grilled ", " grilling ", " barbecue ", " bbq ",
                                   " char ", " charred ")):
        return ("Under a hot grill or on the barbecue, 10 to 12 minutes, turning every few "
                "minutes until the kernels start to char in patches - rub them with a little "
                "butter or oil first so they colour rather than dry. Boiled instead, 6 to 8 "
                "minutes in unsalted water; salt toughens it.")
    return ("Boil it in unsalted water for 6 to 8 minutes - salt toughens it - or grill it, "
            "turning it now and then, for 10 to 12 minutes until the kernels start to char. In "
            "the microwave a cob takes 3 to 4 minutes on full power. Butter, salt and pepper, and "
            "it needs nothing else.")


BASICS = (
    (("brown rice",),
     "Brown rice wants more water and longer than white: one mug of rice to two mugs of water, "
     "lid on, 25 to 30 minutes on the lowest heat. Then 10 minutes off the heat before you fork "
     "it through. Rinse it first and don't stir it."),
    (("quinoa",),
     "Quinoa takes 12 to 15 minutes: one part quinoa to two of water, lid on, simmering, then 5 "
     "minutes off the heat and fork it through. Rinse it first, or it tastes soapy."),
    (("couscous",),
     "Couscous needs no cooking: same volume of boiling water or stock as couscous, cover the bowl "
     "and leave it 5 minutes, then fork it through with a knob of butter and a squeeze of lemon so "
     "it stays loose."),
    (("barley", "pearl barley"),
     "Pearl barley takes 25 to 30 minutes simmered in three times its volume of water or stock, "
     "and whole barley 45 to 60. It is done when a grain squashes between your fingers with no "
     "chalky middle, so taste it rather than time it."),
    (("bulgur", "bulgur wheat"),
     "Bulgur wheat takes 10 to 12 minutes simmered in twice its volume of water, or pour boiling "
     "stock over it, cover and leave it 20 minutes off the heat. Fork it through with a little "
     "olive oil."),
    (("wild rice",),
     "Wild rice is a grass seed rather than a rice, so it takes 40 to 45 minutes in plenty of "
     "boiling water - about three parts water to one of rice - until the grains split and taste "
     "nutty. Drain it and rinse off the starch."),
    (("rice cooker",),
     "Rinse the rice first, then the same one mug of rice to one and a half mugs of water, level "
     "off with the back of a finger and don't go past the line inside the bowl. Let it finish on "
     "its own, leave it on warm for 10 minutes, then fork it through."),
    (("rice", "basmati", "long grain rice", "white rice", "jasmine rice", "rice cooker"),
     "One mug of rice to one and a half mugs of water, lid on, 10 to 12 minutes on the "
     "lowest heat, then 10 minutes off the heat with the lid still on before you fork it "
     "through. Rinse it until the water runs clear first. Don't stir it and don't drain it - "
     "that is what makes it gluey."),
    (("porridge", "oats", "oatmeal", "porridge oats"),
     "50g of oats to 300ml of milk or water per person, with a pinch of salt, stirred over a "
     "medium heat for 4 to 5 minutes. Take it off while it still looks a little loose, because it "
     "thickens as it stands, and stir in a splash more milk if it sets."),
    (("white sauce", "cheese sauce", "bechamel", "béchamel"),
     "About 10 minutes start to finish. Melt 50g of butter, stir in 50g of plain flour and cook "
     "that for a minute, then add 500ml of milk a good splash at a time, whisking each one in "
     "before the next goes in. Simmer it for 5 minutes until it coats the back of a spoon, then "
     "season it. For a cheese sauce, stir in 100g of grated cheddar once it is off the heat."),
    (("mash", "mashed potato"),
     "Use a floury potato like Maris Piper or King Edward, cut into even chunks and boiled in "
     "salted water for 15 to 20 minutes. Drain them, leave them in the colander for a minute to "
     "steam dry, then mash with butter and warm milk - cold milk makes it gluey - and don't use a "
     "food processor."),
    (("vegetables", "veg"),
     "The one rule for vegetables is short and hot: steam or boil them 5 to 7 minutes so "
     "they still have a bite, or roast them at 200C (180C fan) for 25 to 35 minutes in oil "
     "with salt. Cut them to a similar size and they finish together, and salt the water "
     "rather than the pan."),
    (("chop an onion", "chop onions", "chopping an onion", "chopping onions", "dice an onion",
      "dice onions", "dicing an onion", "dice onions", "slice an onion", "cut an onion",
      "cut up an onion", "prepare an onion"),
     "Halve it top to bottom through the root, lay a half cut side down and slice across it "
     "towards the root, then cut the slices the other way, and it is diced. Leave the root end on "
     "until the last cut, because it holds the layers together. Use the sharpest knife you have "
     "and keep the tip on the board: a blunt knife crushes the cells and releases more of the "
     "sulphur that makes your eyes water."),
    (("peel a potato", "peel potatoes", "peeling potatoes", "peel a potato quickly",
      "how do i peel potatoes", "prepare potatoes", "prepare a potato"),
     "Take the skin off in strips with a peeler, working away from you and turning the potato as "
     "you go, then dig any eyes out with the tip of the peeler. Drop them into a bowl of cold "
     "water if they are not going in the pan straight away, because peeled potato goes pink in "
     "the air. Peel floury ones like Maris Piper just before they cook, not the night before."),
    (("chop garlic", "crush garlic", "mince garlic", "chop a garlic clove",
      "prepare garlic", "chop garlic cloves", "peel a garlic clove", "peel garlic cloves"),
     "Lay the clove on the board, put the flat of the knife on top and press down with the heel "
     "of your hand: the skin slips off and the clove is already crushed. Chop it roughly, "
     "sprinkle a pinch of salt on it and drag the flat of the knife over it in circles to turn it "
     "into a paste. Crushed like that it sweetens in the pan; left in chunks it burns."),
    (("peel ginger", "chop ginger", "grate ginger", "prepare ginger", "mince ginger"),
     "Scrape the skin off with the edge of a teaspoon, which follows the knobs better than a "
     "peeler and wastes less of the root. Grate it on the fine side of a grater, or freeze the "
     "knob whole and grate it from frozen, which is quicker and keeps for months. The skin is "
     "thin and edible, so it can stay on if it is going into a curry."),
    (("chop a carrot", "chop carrots", "dice a carrot", "dice carrots", "slice a carrot",
      "slice carrots", "prepare carrots", "prepare a carrot"),
     "Top and tail it, cut it in half lengthways and lay the flat side down so it cannot roll. "
     "For sticks, cut each half into lengths and slice those; for dice, cut the lengths into "
     "batons first, then turn them and slice across. Keep every piece the same size, because "
     "that is what makes them cook at the same rate."),
    (("chop mushrooms", "slice mushrooms", "prepare mushrooms", "cleaning mushrooms",
      "cleaning a mushroom"),
     "Wipe the caps with damp kitchen paper, or rinse them quickly under the tap and dry them on "
     "a tea towel - either works, because a few seconds of water adds nothing a mushroom did not "
     "already have, and only a bowl of soaking water makes them watery. Snap the stalk out level "
     "with the cap and slice straight down through cap and stalk together. Do not crowd the pan - "
     "a crowded pan of mushrooms boils in its own water and never browns."),
    (("cut an avocado", "prepare an avocado", "peel an avocado", "stone an avocado",
      "remove the stone from an avocado", "slice an avocado", "how do i cut an avocado"),
     "Run the knife round the stone from top to bottom, twist the two halves apart, then lever "
     "the stone out with a spoon rather than the knife. Peel the skin back or scoop the flesh out "
     "with a spoon, and slice it while it is still in its shell. Squeeze lemon or lime over it if "
     "it is going to sit, because cut avocado goes brown in the air."),
    (("peel a mango", "cut a mango", "prepare a mango", "slice a mango",
      "how do i cut a mango"),
     "Slice the two cheeks off either side of the flat stone, score the flesh in a grid without "
     "cutting the skin, then push the skin inside out and cut the cubes off it. A peeler and a "
     "knife down the sides of the stone works too and wastes a little more. A ripe mango gives "
     "slightly under your thumb; a hard one is stringy and sour."),
    (("cut up a pineapple", "cut a pineapple", "prepare a pineapple", "peel a pineapple",
      "how do i cut a pineapple", "how do i cut up a pineapple", "slice a pineapple"),
     "Slice the top and the base off flat so it stands up, then cut the skin away in strips from "
     "top to bottom, taking the eyes with it. Cut it into quarters, stand each one up and slice "
     "the core out, then cut the rest into the pieces you want. The core is tough raw but fine "
     "in a smoothie."),
    (("juice a lemon", "juice a lime", "squeeze a lemon", "squeeze a lime", "juice an orange",
      "juice lemons", "squeeze lemons"),
     "Roll it on the worktop with the heel of your hand first to break the cells inside, then cut "
     "it across the middle rather than top to tail. Push a fork into the cut face and squeeze, "
     "turning as you go, and strain out the pips. A lemon at room temperature gives more juice "
     "than one out of the fridge."),
    (("onions", "onion"),
     "Chop it, then soften it in oil on a low heat for 8 to 10 minutes with a pinch of salt: "
     "that is what makes it sweet and golden. A hot pan browns the outside and leaves the "
     "middle raw and sharp, so turn the heat down and give it the time."),
    (("corn on the cob", "sweetcorn", "corn"), _corn),
    (("butternut squash", "butternut", "squash"),
     "Halve it, scoop out the seeds, rub the cut sides with oil and roast face down at 200C "
     "(180C fan) for 40 to 45 minutes. Cubed it takes 25 to 30 minutes, and it is done when "
     "a knife goes in with no resistance."),
    (("pork chops", "pork chop"),
     "Pat them dry, season, and sear in a hot pan 3 to 4 minutes a side, then rest 5 minutes "
     "- pork is safe slightly pink now, at 70C in the middle. A thick chop also finishes in "
     "the oven at 200C (180C fan) for 10 to 12 minutes."),
    (("fish", "white fish", "cod", "haddock", "salmon fillet", "fillet of fish"),
     "Bake fillets at 200C (180C fan) for 12 to 15 minutes - done when the thickest part flakes "
     "into opaque white, so keep it a minute short rather than a minute long - or fry them skin "
     "side down in a hot pan for 4 minutes, then 2 on the other side."),
    (("potato wedges", "wedges"),
     "Cut them into wedges about 2cm at the thick edge, toss in oil, salt and paprika and roast "
     "at 200C (180C fan) for 25 to 30 minutes, turning once at halfway: they are done when the "
     "edges are deep gold and a knife slides into the thick part. Parboiling 8 minutes first "
     "makes them crisper outside and fluffier in."),
    (("chard", "swiss chard"),
     "Cook the stems first: slice them and fry 4 to 5 minutes, then add the leaves for 2 to 3 "
     "minutes more, because the stems take far longer. A knob of butter, a pinch of salt and a "
     "squeeze of lemon, and the leaves wilt down to almost nothing."),
    (("peppers", "bell peppers", "bell pepper"),
     "Fry sliced peppers in a hot pan with oil for 6 to 8 minutes until the edges soften and "
     "catch a little colour, or roast halves at 200C (180C fan) for 25 minutes. They go sweet "
     "with long cooking and stay crunchy with short cooking, so it depends what you want."),
    (("celery", "celery sticks"),
     "Slice it and soften it in butter for 6 to 8 minutes: that is the base of a soup or a "
     "stew, and it goes sweet rather than stringy. On its own, braise the sticks with stock "
     "and a lid for 20 minutes, or shave them raw into a salad with lemon and salt."),
    (("fennel", "fennel bulb"),
     "Slice it thin and roast at 200C (180C fan) for 25 minutes with oil, salt and a little "
     "lemon - the aniseed goes sweet. Raw and shaved with olive oil, lemon and parmesan it is "
     "a salad in 5 minutes. Cut out the tough core first."),
    (("celeriac",),
     "Peel it thickly, cube it and boil for 15 to 20 minutes, then mash it half and half with "
     "potato - it is wet on its own and needs the potato to hold it. It browns fast once it is "
     "cut, so drop the pieces in water with a squeeze of lemon until they go in the pan; raw and "
     "shredded with mayonnaise, mustard and lemon it is remoulade."),
    (("turnip", "turnips"),
     "Small young turnips only want 10 to 12 minutes boiled, or 25 minutes roasted in wedges "
     "at 200C (180C fan) with oil and honey. Big older ones are woody and bitter, so peel "
     "them well and mash them with potato and butter instead."),
    (("broad beans", "fava beans"),
     "Boil them for 4 to 5 minutes, then pop them out of their skins - the skins are tough and "
     "bitter, and the beans inside are sweet. Small ones can stay in their skins. Dress them "
     "with oil, lemon, mint and a little salt."),
    (("shallots", "shallot"),
     "Slice them and soften in butter for 6 to 8 minutes on a low heat - they are sweeter and "
     "milder than onions, so they need less time and brown faster. Whole, roast them at 200C "
     "(180C fan) for 25 to 30 minutes with oil and a pinch of salt."),
    (("pak choi", "bok choy", "pak choy"),
     "Halve it lengthways and fry cut side down in a hot pan for 2 to 3 minutes, then add a "
     "splash of soy sauce, a little garlic and a lid for 1 minute more. It is done when the "
     "base is tender and the leaves have just wilted, so it takes about 5 minutes in all."),
    (("mange tout", "mangetout", "sugar snap peas", "snow peas"),
     "Stir-fry them in a very hot pan for 2 to 3 minutes, or steam them for 3: they are done "
     "as soon as they are hot through and still squeak when you bite one. Don't boil them, or "
     "the sweetness goes into the water."),
    (("buttermilk", "leftover buttermilk"),
     "Buttermilk is not cooked on its own: it is what makes soda bread rise with bread soda, it "
     "thins a pancake batter, and it tenderises chicken in a marinade for an hour before frying. "
     "It is naturally sour and thick, so in a recipe you can stand in for it with milk and a "
     "squeeze of lemon left for 10 minutes."),
    (("marrow", "vegetable marrow", "marrows"),
     "Roast it in thick rings: peel it, scoop out the seeds, cut 2cm rings, oil and salt them and "
     "give them 30 to 35 minutes at 200C (180C fan) until the edges colour. Or halve it, salt it "
     "and let it drain 20 minutes, then stuff it with mince and rice and bake 45 minutes at 190C "
     "(170C fan) - it is mostly water, so the salt-and-drain is what stops it going to mush."),
    (("chicory", "endive"),
     "Halve it and braise cut side down in butter for 3 to 4 minutes, then add a splash of "
     "stock and a lid for 10 minutes, which takes the bitterness down. Raw, the leaves are a "
     "scoop for a dip, and a little sugar or orange in the pan helps too."),

)

_STAPLE_NAMES = tuple(name for _names, _reply in BASICS for name in _names)

def _learn_to_cook(memory, understood):
    said = {_fold(str(word).lower()) for word in (understood.get("words") or ())}
    if said & _foods_said():
        return None
    return ("Learn four things and the rest follows: pasta with a sauce, an omelette, a tray of "
            "roasted vegetables, and a one-pot curry or stew. Cook the same one twice in a week "
            "rather than a new one each night, and taste as you go - food that tastes flat "
            "usually wants salt, a squeeze of lemon, or more time in the pan. A cheap "
            "thermometer takes the fear out of chicken and pork.")

NOT_A_METHOD = ("make with", "made with", "make using", "use up", "using up", "use it up",
                "what can i", "what should i", "what could i", "hate", "hates", "hated",
                "dislike", "dislikes", "allergic", "allergy", "cant stand", "cannot stand",
                "doesnt like", "does not like", "dont like", "do not like", "wont eat",
                "wont touch", "fussy", "left with", "half a",
                "yesterday", "yesterdays", "last night", "the day before", "day before",
                "the day after", "day after", "day later", "a day later", "days ago",
                "a couple of days ago", "2 days ago", "two days ago",
                "backhand", "forehand", "racket", "racquet", "tennis court", "squash court",
                "badminton", "volleyball", "netball", "the ball", "cricket")

KNOWS_READY = ("know when", "how do i know", "how will i know", "how can i tell",
               "when are they ready", "when are mine ready", "are they ready", "are mine ready",
               "are they done yet", "when do i know")

DISH_BEFORE = frozenset("sweet fried roast roasted baked mashed creamed scalloped glazed "
                        "cauliflower sushi paella overnight egg fried".split())
DISH_AFTER = frozenset("pudding salad bake gratin pie bread cake cakes balls bolognese cheese "
                       "curry soup stew krispie crispy noodle noodles bowl paper wrap sushi "
                       "ball bite finger patty".split())


STAPLE_ASK = ("cook", "cooking", "make", "making", "how", "long", "boil", "boiling",
              "time", "much", "ratio", "method", "properly", "instructions", "best way",
              "minutes", "do i", "should i", "recipe")


_BODY_TOO_THICK = (
    "Too thick: add hot stock, milk or just water a splash at a time, stirring, until it pours the "
    "way you want it, then taste it again because thinning takes the salt with it. A spoon of "
    "butter or cream stirred in at the end does the same with more flavour, and a stew that has "
    "cooked down only needs the lid on for ten minutes."
)
_BODY_TOO_THIN = (
    "Simmer it uncovered for 10 minutes to reduce it, or blend a ladleful and stir it back in for "
    "body without flour. A handful of red lentils thickens a soup or stew in 15 minutes; for a "
    "stew, take the lid off for the last half hour."
)


_TOO_THICK_SAID = ("too thick", "so thick", "very thick", "really thick", "is thick", "its thick",
                   "it's thick", "thick and", "stodgy", "claggy", "gluey", "thinner",
                   "less thick", "thin down", "thin it", "make it thinner", "soup thinner",
                   "make my soup thinner")


_REST_BODY = ("my shoulder", "my knee", "my back", "my hip", "my leg", "my arm", "my neck",
              "injured", "injury", "injuries", "pain", "painful", "hurts", "hurting",
              "sore", "stiff", "stiffness", "sprain", "sprained", "pulled a muscle",
              "after a fall", "physio", "physiotherapist", "gym", "workout", "worked out",
              "exercise", "exercising", "training", "trained", "running", "run", "sports day",
              "my joint", "my joints", "joint pain", "aching", "ache", "aches")
_REST_CUT = ("lamb", "pork", "beef", "veal", "venison", "joint", "roast", "brisket",
             "turkey", "chicken", "duck", "goose", "steak", "ribs", "rib", "ham", "gammon",
             "shoulder of", "leg of", "of lamb", "of pork", "of beef", "meat", "wellington")


_REST_CUT_PHRASE = ("of lamb", "of pork", "of beef", "of veal", "shoulder of", "leg of")


def _resting_a_body_part(said):
    body = any(" " + word + " " in said for word in _REST_BODY)
    cut = any(" " + word + " " in said for word in _REST_CUT)
    if body and not any(phrase in said for phrase in _REST_CUT_PHRASE):
        return True
    return body and not cut


def _rest_the_meat(memory, understood):
    from .dishes import ask_kind, reply as dish_reply
    from .lookup import find
    said = " " + " ".join(str(word) for word in ((understood or {}).get("words") or [])) + " "
    if " the rest " in said or " rest of " in said:
        return None
    if _resting_a_body_part(said):
        return None
    if ask_kind(understood) == "rest" and dish_reply("rest", memory, understood):
        next_row = find(understood, reject=lambda item: item.id == "rest-meat")
        if getattr(next_row, "id", None) == "plan-followup":
            return None
    minutes = ("loosely under foil and off the heat, not back in the oven: 15 to 20 minutes for "
               "a chicken or a turkey, 10 to 20 for a joint of beef, lamb or pork, 5 to 10 for a "
               "steak or chops, and 20 to 30 for a brisket")
    reason = ("standing lets the heat that has built up round the outside move back into the "
              "middle, so the juice stays in the meat when you carve it instead of running out "
              "onto the board")
    if "why" in ((understood or {}).get("asks") or ()):
        return ("Rest it because " + reason + " - " + minutes + ". It stays hot that long under "
                "the foil, so nothing is lost by waiting.")
    return (minutes[0].upper() + minutes[1:] + ". " + reason[0].upper() + reason[1:]
            + ". It stays hot that long under the foil, so nothing is lost by waiting.")


def _body(memory, understood):
    said = " " + " ".join(_fold(str(word)) for word in (understood.get("words") or [])) + " "
    thickening = "thicken" in said or "thicker" in said or "thickening" in said
    complaining = any(shape in said for shape in _TOO_THICK_SAID)
    if complaining and not thickening:
        return _BODY_TOO_THICK
    return _BODY_TOO_THIN


CHILD_WORDS = (" kid", " kids", " child", " children", " son", " daughter", " toddler", " baby",
               " fussy", " picky", " wont eat", " won't eat", " refuses", " weaning",
               " nursery", " school dinner", " school dinners", " he wont", " she wont")


def _about_a_child(memory, understood):
    line = " " + ((understood or {}).get("clean") or "") + " "
    if any(word in line for word in CHILD_WORDS):
        return True
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return False
    for turn in reversed(turns[-3:]):
        said = " " + (turn.get("user") or "") + " " if isinstance(turn, dict) else ""
        if any(word in said for word in CHILD_WORDS):
            return True
    return False


KIDS_VEG = ("Keep serving one small piece of veg next to something they already like, without a "
            "fight or a reward: it can take ten tries before a toddler accepts a new one. Roasting "
            "carrots or broccoli in a little oil makes them sweeter, and a dip to dunk turns it "
            "into a game. Grated or blended into what they already eat - carrot in the bolognese, "
            "courgette in a muffin, spinach in a soup - gets the veg in without a standoff.")


ADULT_VEG = ("Put them where you already eat rather than on a separate pile: grated carrot or "
             "courgette in the mince, a handful of spinach stirred into pasta at the end, frozen "
             "peas straight into rice, beans or lentils bulking out a chilli. Frozen and tinned "
             "count, and so does a bag of mixed veg thrown into a tray bake. Aim for one extra "
             "portion at a meal you already have rather than a new meal you have to keep up.")


def _more_veg(memory, understood):
    if not _about_a_child(memory, understood):
        return ADULT_VEG
    return None if _the_veg_card_was_just_said(memory) else KIDS_VEG


def _the_veg_card_was_just_said(memory):
    opening = KIDS_VEG[:40].lower()
    for last in (memory.get("turns") or [])[-2:]:
        if isinstance(last, dict) and opening in (last.get("bot") or "").lower():
            return True
    return False


def _kids_veg(memory, understood):
    if not _about_a_child(memory, understood):
        return None
    return None if _the_veg_card_was_just_said(memory) else KIDS_VEG


def _harvest_crops():
    from .garden import harvest_crops
    return harvest_crops()


def _done_words():
    from .garden import DONE_NOT
    return DONE_NOT


_A_HEAT_OR_TIME = re.compile(
    r"\b(minutes?|mins?|minutes'|hours?|hrs?|seconds?|degrees?|celsius|fahrenheit|gas mark|"
    r"temp|temperature|oven)\b|\bhow long\b")
_A_HOW_MUCH = re.compile(r"\bhow (much|many)\b")
_A_SIDE_SAID = re.compile(r"\bsides?\b")


def _not_a_portion_ask(understood):
    text = str(understood.get("clean") or understood.get("norm_text")
               or " ".join(understood.get("words") or [])).lower()
    if _A_HOW_MUCH.search(text) and not _A_HEAT_OR_TIME.search(text):
        return False
    if _A_SIDE_SAID.search(text) and not _A_HEAT_OR_TIME.search(text):
        return False
    return True


def _staple(memory, understood):
    said = [_fold(str(word).lower()) for word in (understood.get("words") or [])]
    joined = " " + " ".join(said) + " "
    for phrase in NOT_A_METHOD:
        if phrase in joined:
            return None
    if any(phrase in joined for phrase in KNOWS_READY):
        done = _done_words()
        if not any(" %s " % word in joined for word in done):
            _harvest = _harvest_crops()
            if any(" %s " % crop in joined for crop in _harvest):
                return None
    for names, reply in BASICS:
        for name in names:
            parts = [_fold(piece) for piece in name.split()]
            size = len(parts)
            for start in range(len(said) - size + 1):
                if said[start:start + size] != parts:
                    continue
                before = said[start - 1] if start else ""
                after = said[start + size] if start + size < len(said) else ""
                if before in DISH_BEFORE or after in DISH_AFTER:
                    continue
                if name not in ("white sauce", "cheese sauce", "bechamel", "béchamel") and (
                        "sauce" in said or "saucy" in said):
                    continue
                rest = said[:start] + said[start + size:]
                guards = NOT_WANTED.get(names[0], ())
                if name != names[0]:
                    guards = guards + NOT_WANTED.get(name, ())
                own = _fold(reply.lower()) if isinstance(reply, str) else ""
                if _a_guard_said(rest, joined, guards, own):
                    continue
                return reply(understood) if callable(reply) else reply
    return None


_AN_APPLIANCE = ("slow cooker", "slow cookers", "crockpot", "crock pot", "air fryer",
                 "pressure cooker", "instant pot", "oven")


def _an_appliance_has_the_line(text):
    try:
        from . import dishes
    except Exception:
        return False
    return dishes._names_an_appliance_and_a_cut(text)


def _a_guard_said(rest, joined, guards, own=""):
    for guard in guards:
        if " " in guard:
            phrase = _fold(guard)
            if phrase in joined and phrase not in own:
                if guard not in _AN_APPLIANCE or not _an_appliance_has_the_line(joined):
                    return True
        elif guard in rest:
            return True
    return False


def _pancakes(memory, understood):
    words = set(understood.get("words") or [])
    if "mix" in words and not words & {"make", "made", "making", "recipe", "batter", "whisk",
                                        "homemade", "from"}:
        return None
    if words & {"american", "fluffy", "thick", "buttermilk", "scotch"}:
        return ("For a dozen thick American pancakes, whisk 150g plain flour, 2 teaspoons of baking "
                "powder, a tablespoon of sugar, 2 eggs and 250ml milk into a thick batter that "
                "holds its shape, and let it rest 10 minutes. Cook them in a buttered pan on a "
                "medium heat, 2 minutes a side, and turn them once, when bubbles pop and stay open. "
                "The baking powder is what lifts them; for thin pancakes leave it out and use "
                "300ml milk.")
    return ("For about 12 thin pancakes, whisk 100g plain flour, 2 eggs and 300ml milk with a pinch of "
            "salt, then let the batter rest 20 minutes. Cook them in a hot non-stick pan with a little "
            "butter, about a minute a side, until bubbles pop on top and the edges look dry. The rest "
            "is what stops them tearing; American ones want a teaspoon of baking powder and a "
            "thicker batter. Flat ones are a batter that was too thin, or an old raising agent.")


def _pancake_batch(memory, understood):
    people = None
    for number in understood.get("numbers") or []:
        value, unit = number.get("value"), number.get("unit")
        if not isinstance(value, (int, float)) or not 2 <= value <= 40:
            continue
        if unit in (None, "", "people", "person", "persons", "adults", "adult", "kids", "guests",
                    "portions", "servings"):
            people = int(round(value))
            break
    if people is None:
        return ("For four people allow 200g plain flour, 3 eggs and 600ml milk, which makes about "
                "16 thin pancakes; a family with small children is happy on 150g. Cook them a "
                "minute a side in a hot pan until the bubbles pop and the edges look dry.")
    grams = 50 * people
    flour = "%dkg" % (grams // 1000) if grams % 1000 == 0 else (
        "%d and a half kg" % (grams // 1000) if grams > 1000 and grams % 500 == 0
        else "%dg" % grams)
    eggs = 0.75 * people
    whole = int(eggs)
    egg_words = ("%d or %d eggs" % (whole, whole + 1) if 0.4 <= eggs - whole <= 0.6
                 else "%d eggs" % int(round(eggs)))
    millilitres = 150 * people
    if millilitres < 1000:
        milk = "%dml of milk" % millilitres
    elif millilitres % 1000 == 0:
        milk = "%d litres of milk" % (millilitres // 1000)
    else:
        milk = ("%.1f litres of milk" % (millilitres / 1000.0)).replace(".0 litres", " litres")
    return ("For %d people allow %s plain flour, %s and %s, which makes about %d thin pancakes. "
            "Cook them a minute a side in a hot non-stick pan with a little butter, until the "
            "bubbles pop and the edges look dry; for thick American ones add a teaspoon of baking "
            "powder per 200g of flour." % (people, flour, egg_words, milk, 4 * people))


def _sweet_potato(memory, understood):
    words = set(understood.get("words") or [])
    if words & {"boil", "boiled", "boiling", "steam", "steamed", "steaming", "mash", "mashed",
                "puree", "pureed"}:
        return ("Boil peeled chunks for 12 to 15 minutes, until a knife slides in with no "
                "resistance: sweet potato softens faster than white potato, so test it at 10. "
                "Drain and steam it dry for a minute, then mash it with butter and a pinch of salt "
                "and go easy on the milk, because it is wetter than white potato.")
    if words & {"microwave", "microwaved", "microwaving", "quick", "quickly", "fast",
                "fastest", "hurry", "hurried", "hungry", "rush"}:
        return ("One medium sweet potato, pricked all over with a fork, takes 5 to 8 minutes on "
                "high: give it 5, turn it, then a minute at a time until a knife slides in with no "
                "resistance. Two take 10 to 12 minutes, and chunks for mash take 8. It steams in "
                "there rather than crisping, so give the skin 5 minutes in a hot oven or a dry pan "
                "afterwards if you want it crisp.")
    if words & {"fryer", "airfryer", "airfried"}:
        return ("In the air fryer, wedges cut into 2cm pieces take 15 to 18 minutes at 190C, shaken "
                "once halfway: toss them in a little oil, salt and paprika first and do not crowd "
                "the basket, or they steam instead of crisping. Whole ones take 35 to 40 minutes at "
                "180C, and fries cut thin take 12 to 15 minutes.")
    return ("For wedges, cut them into 2cm pieces, toss them in oil, salt and paprika and roast at "
            "200C (180C fan) for 25 to 30 minutes. Whole, they bake in about 45 minutes at 200C, or "
            "8 minutes in the microwave for one on its own. Boiled for mash, chunks take 12 to 15 "
            "minutes.")

PET_LINE_WORDS = ("dog", "dogs", "puppy", "pup", "cat", "cats", "kitten", "kittens", "pet",
                  "pets", "vet", "swallowed", "swallow", "chewed", "choking", "choke",
                  "poisoned", "vomiting")


def _thighs(memory, understood):
    words = " ".join(understood.get("words") or [])
    if "lemon" in words or "potato" in words or "potatoes" in words:
        return ("Halve the potatoes, toss everything with oil, lemon slices and salt, and roast at "
                "200C (180C fan) for 35 to 40 minutes, skin side up, until the skin is crisp and the "
                "juices run clear. Squeeze the roasted lemon over before serving.")
    return ("Roast chicken thighs at 200C (180C fan) for 35 to 40 minutes, skin side up and spaced "
            "out, until the skin is crisp and the juices run clear. Salt the skin before they go in "
            "and don't crowd the tray, or they steam instead of crisping.")


def _weight_words(kilos):
    if kilos < 1:
        return f"{int(round(kilos * 1000))}g"
    return f"{kilos:g}kg"
def _legs(memory, understood):
    reply = _legs_method(understood)
    words = " ".join(understood.get("words") or [])
    if "frozen" in words or "freezer" in words:
        reply += " From frozen, add about 10 minutes and check at the bone before you serve it."
    return reply


def _legs_method(understood):
    words = " ".join(understood.get("words") or [])
    small = "drumstick" in words or "drumsticks" in words
    done = ("It is done when the juices at the thickest part run clear and the meat pulls away from "
            "the bone - if you have a thermometer, 74C.")
    if "boil" in words or "boiling" in words or "poach" in words or "poached" in words or \
            "simmer" in words or "simmering" in words:
        return (f"Simmer {'drumsticks' if small else 'the legs'} in salted water for "
                f"{'20 to 25' if small else '25 to 30'} minutes. {done}")
    if "grill" in words or "grilled" in words or "grilling" in words or "barbecue" in words or \
            "barbeque" in words or "bbq" in words:
        return (f"Over medium heat, a {'drumstick' if small else 'leg'} takes about "
                f"{'8 to 10 minutes a side' if not small else '10 minutes a side'}, turning once and "
                f"moving it off the hottest spot if it colours too fast. {done}")
    if "slow" in words or "crockpot" in words or "crock" in words:
        return ("In a slow cooker, legs take 3 to 4 hours on low with a splash of stock or a tin of "
                f"tomatoes; drumsticks are done nearer 2 to 3. {done}")
    if "air" in words:
        return (f"In an air fryer, {'drumsticks' if small else 'legs'} take "
                f"{'20 to 25' if small else '25 to 30'} minutes at 190C, turned once, until the skin "
                f"is crisp. {done}")
    if small:
        return ("Roast drumsticks at 200C (180C fan) for 25 to 30 minutes, skin side up and spaced "
                "out, until the skin is crisp and the juices at the bone run clear. Salt the skin "
                "first, and give them a turn halfway if your oven has a hot spot.")
    return ("A whole chicken leg takes 35 to 40 minutes at 200C (180C fan), skin side up: a "
            "drumstick alone is 25 to 30. It is done when the juices at the thickest part run "
            "clear and the meat pulls away from the bone - if you have a thermometer, 74C. Salt "
            "the skin and don't crowd the tray, or it steams instead of crisping.")


TENDER_ADJECTIVE_BEFORE = frozenset(("my", "so", "really", "very", "more", "most", "too", "not",
                                     "is", "super", "nice", "them", "properly", "and", "are"))


def _tenders_are_a_piece(understood):
    words = [w.lower() for w in (understood.get("words") or []) if isinstance(w, str)]
    if "tenders" in words or "strips" in words or "goujons" in words:
        return True
    for i, word in enumerate(words):
        if word == "chicken" and i + 1 < len(words) and words[i + 1] in ("tender", "strip",
                                                                        "goujon"):
            before = words[i - 1] if i else ""
            return before not in TENDER_ADJECTIVE_BEFORE
    return False


def _tenders_method(memory, understood):
    words = " ".join(understood.get("words") or [])
    done = ("They are done when the middle is 74C and no pink is left - cut the thickest one "
            "open if you have no thermometer.")
    if "air" in words or "airfryer" in words or "airfryers" in words:
        return ("In an air fryer, chicken tenders take 9 to 10 minutes at 190C in a single layer, "
                "shaken once halfway. " + done)
    if "grill" in words or "grilled" in words or "grilling" in words:
        return ("Under a hot grill, chicken tenders take 4 to 5 minutes a side, turned once. " + done)
    if ("fry" in words or "fried" in words or "frying" in words or "pan" in words
            or "shallow" in words):
        return ("In a frying pan over a medium heat, chicken tenders take 3 to 4 minutes a side, "
                "until golden outside and white in the middle. " + done)
    return ("Chicken tenders are thin, so 10 to 12 minutes in a 200C (180C fan) oven is enough: "
            "spread out on an oiled tray and turned once halfway. " + done)


def _bird_weight(understood):
    for number in understood.get("numbers") or []:
        value, unit = number.get("value"), number.get("unit")
        if not isinstance(value, (int, float)) or value <= 0:
            continue
        kilos = {"kg": value, "g": value / 1000.0, "lb": value * 0.4536,
                 "oz": value * 0.02835}.get(unit)
        if kilos and 0.4 <= kilos <= 12:
            said = str(number.get("text") or "")
            if not re.search(r"\d|\b(?:kilo\w*|kg|g|lb|lbs|pound|pounds|oz|ounce|ounces)\b",
                             said.lower()):
                said = _weight_words(kilos)
            ours = re.match(r"(?:a|an)\s+(.+)$", said.lower())
            if ours:
                said = ours.group(1)
            return kilos, said
    return None


def _hours_words(hours):
    hours = int(round(hours / 3.0)) * 3
    if hours < 24:
        return f"{hours} hours"
    days, rest = divmod(hours, 24)
    whole = {1: "a day", 2: "two days", 3: "three days", 4: "four days", 5: "five days"}
    half = {1: "a day and a half", 2: "two and a half days", 3: "three and a half days"}
    if rest == 0 and days in whole:
        return whole[days]
    if rest == 12 and days in half:
        return half[days]
    return f"{hours} hours"


def _in_words(minutes):
    minutes = int(round(minutes / 5.0)) * 5
    hours, rest = divmod(minutes, 60)
    if not hours:
        return f"{rest} minutes"
    hours_text = f"{hours} hour" + ("" if hours == 1 else "s")
    return f"{hours_text} {rest} minutes" if rest else hours_text


def _chicken_time(memory, understood):
    said_line = str((understood or {}).get("clean") or (understood or {}).get("text") or "")
    if a_price_is_judged(said_line):
        return None
    check = ("Check the thigh reads 74C on a thermometer and the juices run clear, then rest it "
             "for 15 minutes before carving.")
    kilos, said = _bird_weight(understood) or (2.0, "2kg")
    return ("About 20 minutes per 500g plus 20 minutes at 190C (170C fan), so a "
            f"{said} bird takes roughly {_in_words(20 * (kilos / 0.5) + 20)}. " + check)





SEASONING_ASKS = re.compile(
    r"\b(?:spices?|herbs?|seasoning|flavours?|flavors?|rub|marinade)\b"
    r"|\bseason(?:ed)?\s+(?:a|an|the|it|them|my|your|with|before|after|well|up)\b"
    r"|\bhow\s+(?:do|to|should)\s+(?:i|you)\s+season\b"
    r"|\bput\s+on\b")



_A_RUB = (
    "A dry rub is salt, sugar, pepper and paprika in roughly equal parts, then whatever else the "
    "food wants - garlic powder, cumin, mustard powder, chilli, dried thyme. About a tablespoon "
    "of rub covers a kilogram of meat: rub it on with a little oil, leave it an hour or overnight "
    "in the fridge, and keep the sugar under a fifth of the mix if it is going on a hot barbecue, "
    "because sugar burns before the meat is done.")


def _a_seasoning(text):
    best = None
    for names, reply in SEASONINGS:
        for name in names:
            if re.search(r"\b" + re.escape(name) + r"\b", text) and (
                    best is None or len(name) > best[0]):
                best = (len(name), reply)
    if best:
        return best[1]
    if re.search(r"\b(?:dry rub|spice rub|make a rub|what goes in a rub|rub recipe)\b", text):
        return _A_RUB
    return None


SIDE_ASKS = re.compile(
    r"\b(?:go|goes|going|went)\s+(?:well\s+|nicely\s+|best\s+)?with\b"
    r"|\b(?:what|which)\s+(?:side|sides)\b"
    r"|\bside\s+(?:dish|dishes|for|to)\b|\bsides\s+(?:for|to|with)\b"
    r"|\bserve\s+(?:it\s+|them\s+|this\s+)?with\b|\bserving\s+with\b"
    r"|\bto\s+serve\s+with\b|\balongside\b|\bon\s+the\s+side\b"
    r"|\bpairs\s+with\b|\bwhat\s+(?:can|should)\s+i\s+(?:have|serve)\s+with\b")

_ONES = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven",
         8: "eight", 9: "nine"}
_TEENS = {10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen",
          15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen"}
_TENS = {20: "twenty", 30: "thirty", 40: "forty", 50: "fifty", 60: "sixty", 70: "seventy",
         80: "eighty", 90: "ninety"}


def _spelled_counts():
    counts = {word: value for words in (_ONES, _TEENS, _TENS) for value, word in words.items()
              if value >= 2}
    for tens, tens_word in _TENS.items():
        for one, one_word in _ONES.items():
            counts[tens_word + " " + one_word] = tens + one
    counts["hundred"] = 100
    counts["a hundred"] = 100
    return counts


_CROWD_NUMBERS = _spelled_counts()
_CROWD_SPELLED = "|".join(sorted(_CROWD_NUMBERS, key=len, reverse=True))
_CROWD_FOR = re.compile(r"\bfor\s+(" + _CROWD_SPELLED + r")\b")
_CROWD_WITHIN = re.compile(r"\b(" + _CROWD_SPELLED
                           + r")\s+(?:people|of us|adults|guests|coming)\b")
_CROWD_PHRASES = ("for a crowd", "a crowd", "big group", "lots of people", "loads of people",
                  "a dozen",
                  "dinner party", "buffet", "guests", "guest coming", "guests coming",
                  "people coming", "people round", "family over", "the in laws", "in-laws",
                  "entertaining", "everyone is coming", "everyone's coming", "a party",
                  "whole family", "big family", "family dinner", "big dinner", "large family",
                  "extended family",
                  "having friends", "having people", "friends round", "friends coming",
                  "family round", "family coming", "friends over for", "friends over to",
                  "people over for", "people over to", "mates over", "mates round")
_OCCASIONS = ("birthday", "anniversary", "christening", "wedding", "retirement",
              "graduation", "mother's day", "mothers day", "father's day", "fathers day",
              "christmas", "easter", "thanksgiving", "wake", "funeral", "celebration",
              "special occasion")


_NOT_A_TABLE = ("minute", "minutes", "min", "mins", "hour", "hours", "hr", "hrs", "second",
                "seconds", "sec", "secs", "calorie", "calories", "cal", "cals", "kcal",
                "kilo", "kilos", "kilogram", "kilograms", "kg", "gram", "grams", "g", "mg",
                "litre", "litres", "liter", "liters", "ml", "oz", "ounce", "ounces", "lb",
                "lbs", "pound", "pounds", "degree", "degrees", "c", "f", "cm", "mm", "inch",
                "inches", "quid", "dollar", "dollars", "euro", "euros", "pence", "pennies",
                "slices", "slice", "pieces", "piece", "tins", "tin", "cans", "can", "spoons",
                "spoon", "tablespoons", "teaspoons")


def _people_after(text, end):
    rest = text[end:].strip().split()
    after = rest[0].strip(".,!?;:").lower() if rest else ""
    return after not in _NOT_A_TABLE


def _crowd(text):
    text = str(text or "").lower().replace("-", " ")
    numbers = [int(match.group(1)) for match in re.finditer(r"\bfor\s+(\d{1,3})\b", text)
               if _people_after(text, match.end())]
    numbers += [_CROWD_NUMBERS[match.group(1)] for match in _CROWD_FOR.finditer(text)
                if _people_after(text, match.end())]
    numbers += [_CROWD_NUMBERS[word] for word in _CROWD_WITHIN.findall(text)]
    for count in re.findall(r"\b(\d{1,3})\s+(?:people|of us|adults|guests|coming)\b", text):
        numbers.append(int(count))
    grouped = people_in_groups(text)
    if grouped:
        numbers.append(grouped)
    if numbers:
        return max(numbers)
    if any(phrase in text for phrase in _CROWD_PHRASES):
        return 6
    return 0


_TABLE_PHRASES = ("people coming", "people round", "people over", "people for dinner",
                  "people to feed", "people to cook for", "of us", "guests coming",
                  "guests for dinner")


_NAMED_TABLE = re.compile(
    r"\b(?:cook|cooking|cooked|make|making|made|bake|baking|hosting|having|feed|feeding)\b"
    r"[^.?!]{0,24}\b(?:for|to)\s+(?:my|our|the|his|her|their)\s+(?:\w+'?s\s+)?"
    r"(?:in\s?laws?|parents?|mums?|moms?|mothers?|dads?|fathers?|folks|familys?|relatives?|"
    r"friends?|neighbou?rs?|guests?|colleagues|workmates|sisters?|brothers?|grandparents?)\b"
    r"|\b(?:my|our)\s+(?:\w+'?s\s+)?(?:in\s?laws?|parents?|mums?|moms?|mothers?|dads?|"
    r"fathers?|folks|familys?|friends?|neighbou?rs?|grandparents?)\b[^.?!]{0,24}"
    r"\b(?:coming|come|round|over|visiting|staying)\b[^.?!]{0,18}"
    r"\b(?:dinner|lunch|tea|supper|meal|eat)\b",
    re.IGNORECASE)


def _named_table(text):
    return bool(_NAMED_TABLE.search(str(text or "")))


def _table_text(text):
    text = str(text or "").lower()
    count = _crowd(text)
    if count >= 6:
        return True
    if not count:
        return _named_table(text)
    if count >= 3 and any(phrase in text for phrase in _CROWD_PHRASES + ("of us",)):
        return True
    if any(phrase in text for phrase in _TABLE_PHRASES) and any(
            word in text for word in ("cook", "cooking", "make", "feed", "serve")):
        return True
    return (count >= 3 and any(phrase in text for phrase in _TABLE_PHRASES)
            and any(word in text for word in ("lunch", "lunches", "meal", "meals", "eat")))


_CROWD_VERBS = ("cook", "cooking", "make", "serve", "feed", "dinner", "tea", "supper",
                "lunch", "eat", "eating")

_CROWD_FOOD = ("food", "foods", "meal", "meals", "dish", "dishes", "buffet", "nibbles",
               "finger food", "spread", "platter", "platters", "menu")

_CROWD_QUANTITY = ("how much", "how many", "amount", "quantity", "weighs", "weight", "grams",
                   " kg", "kilos", "per head", "per person", "per guest")
_CROWD_NOT_A_MEAL = ("poison", "poisoning", "hygiene", "allergy", "allergic", "reaction",
                     "ill", "sick", "sickness", "waste", "bin", "bins", "food bank",
                     "dog food", "cat food", "pet food", "baby food", "fast food")


def _crowd_ask(clean):
    text = str(clean or "").lower()
    if not _table_text(text):
        return False
    if any(word in text for word in _CROWD_VERBS):
        return True
    if any(phrase in text for phrase in _CROWD_NOT_A_MEAL):
        return False
    if any(word in text for word in _CROWD_FOOD):
        return not any(phrase in text for phrase in _CROWD_QUANTITY)
    return False


_CROWD_WORDS = {v: k for k, v in _CROWD_NUMBERS.items()}


def _trays(count):
    if count >= 13:
        return ("two or three trays of it, on the top and middle shelves, or one dish made in "
                "the biggest pot you own")
    if count >= 9:
        return ("two trays of it, on the top and middle shelves and swapped halfway, to feed "
                + _CROWD_WORDS.get(count, str(count)))
    if count and count <= 5:
        return ("one tray of it is plenty for " + _CROWD_WORDS.get(count, str(count)))
    if not count:
        return "which does four to six, so count the potatoes yourself"
    return "which feeds eight from one oven"


def _crowd_meal(banned, occasion, count=0):
    vegetarian = bool({"meat", "chicken", "beef", "pork", "lamb", "mince", "bacon",
                       "sausage", "sausages", "ham", "turkey", "fish", "salmon", "cod",
                       "tuna", "prawn", "prawns"} & banned)
    if vegetarian:
        dish = ("a big mushroom and lentil lasagne or a chickpea and vegetable traybake, made in "
                "the largest dish you own")
        amount = "about 300g of the dish per person"
    else:
        dish = ("a tray of chicken thighs or sausages with halved potatoes, peppers and onions at "
                "200C (180C fan) for 45 minutes")
        amount = "about 200g of meat and a big potato each"
    reply = ("Cook one big oven dish rather than several pans: " + dish + ", " + _trays(count)
             + ". Allow " + amount + ", add a loaf of bread and a bowl of salad, and write the "
             "times down so nothing needs the oven at once.")
    if occasion:
        reply += (" Anything that can be made that morning - a chilli, a stew, a lasagne - just "
                  "gets reheated, which leaves the day free.")
    return reply


def _occasion(text):
    if any(word in text for word in _OCCASIONS):
        return True
    return bool(re.search(r"\b\d{1,3}(?:st|nd|rd|th)\b", text))


def _crowd_or_any(text, banned):
    if _table_text(text):
        return _crowd_meal(banned, _occasion(text), _crowd(text))
    if _occasion(text) and any(
            phrase in text for phrase in ("what should i cook", "what can i cook",
                                          "what shall i cook", "what to cook", "what to make",
                                          "meal", "dinner", "cook", "no idea")):
        return _crowd_meal(banned, True, _crowd(text))
    return _any_meal(banned)


A_TIME_OR_HEAT_ASK = re.compile(
    r"\b(how many minutes?|how many mins?|how long|how much time|minutes a side|mins a side|"
    r"minutes per side|what temperature|what temp|what heat|gas mark|how do i time)\b")


def _sides(memory, understood):
    text = str(understood.get("clean") or " ".join(understood.get("words") or [])).lower()
    if re.search(r"\bpain\b|\bstitch\b|\bside effects?\b|\bleft side\b|\bright side\b", text):
        return None
    if A_TIME_OR_HEAT_ASK.search(text):
        return None
    if SEASONING_ASKS.search(text):
        seasoned = _a_seasoning(text)
        if seasoned:
            return seasoned
    table = _table_side(text)
    plan = _plan_side(memory, text)
    if plan:
        return plan[1]
    if table:
        return table[1]
    from . import dishes
    if dishes.asks_for_a_side_of_a_food(text):
        return dishes.general_sides(text)
    return None


def plan_side(memory, text):
    found = _plan_side(memory, str(text or "").lower())
    return found[1] if found else None


def side_for(memory, text):
    side = plan_side(memory, text)
    if side:
        return side
    from . import dishes
    for line in [str(text or "")] + list(dishes.recent_texts(memory))[:3]:
        found = _table_side(line.lower())
        if found:
            return found[1]
    return None


def _table_side(text):
    best = None
    for names, reply in SIDES:
        for name in names:
            if re.search(r"\b" + re.escape(name) + r"\b", text) and (
                    best is None or len(name) > best[0]):
                best = (len(name), reply)
    return best


def _plan_side(memory, text):
    from . import dishes
    lines = [text]
    if isinstance(memory, dict):
        lines += list(dishes.recent_texts(memory))[:2]
    for line in lines:
        name = dishes.dish_in(line)
        plan = dishes.PLANS.get(name or "")
        if not plan:
            continue
        if not plan.get("sides"):
            return None
        names = [wanted for group in plan.get("names", ()) for wanted in group]
        return (len(name), plan["sides"])
    return None


ANY_MEAL = ("Ten-minute dinners: pasta with garlic, chilli and olive oil; eggs on toast; or cold "
            "rice fried with frozen veg, an egg and soy sauce. Tell me what is in the fridge and "
            "I will pick one.")

DIABETIC_PLATE = (
    "Cook the same sort of dinner as for anyone, with the starchy part smaller and the "
    "vegetables bigger: chicken or fish with two veg, a chilli with beans instead of rice, or an "
    "omelette and salad. Halve the potatoes, rice or pasta rather than cutting them out, go "
    "wholegrain where you can, skip the sugary drinks, and keep pudding small - and ask them "
    "what they usually do rather than guessing.")

DIABETES_WORDS = ("diabetic", "diabetics", "diabetes", "sugar diabetes", "type 1", "type 2",
                  "blood sugar")


def _says_diabetes(text):
    folded = " " + re.sub(r"[^a-z0-9]+", " ", str(text or "").lower()).strip() + " "
    return any(" %s " % word in folded for word in DIABETES_WORDS)

PLAN_WEEK = ("Pick four dinners you already cook and plan the week on one list before you shop, "
             "then cook once for two nights: a big chilli or a tray of roast vegetables tonight, "
             "the rest in "
             "a pasta bake or wraps tomorrow, and one night that needs no cooking at all. Put one "
             "double batch in the freezer for the night you are late home, and keep two fallbacks "
             "in the cupboard - pasta and a tin of tomatoes, rice and eggs - for the night the "
             "plan falls apart.")

PLAN_CHEAP = ("Cheap weeks come from the same eight things: rice, pasta, tins of tomatoes, "
              "chickpeas or lentils, onions, carrots, frozen veg and eggs. Pick four dinners you "
              "already cook from those and put them on the fridge: a big chilli or bolognese "
              "stretched with lentils so it eats twice, a tray of roast vegetables with the rest "
              "in a pasta bake, a lentil dhal, and beans on toast. That is about 20 pounds a head "
              "for the week, and nothing in it goes off.")

PLAN_BATCH = ("Cook two big pots on one afternoon and the week is half done: a chilli or "
              "bolognese and a curry or dhal, each cooled and split into portions, then frozen "
              "flat in bags so they thaw in minutes. Cook rice and pasta fresh while a portion "
              "reheats, label the bags with the date, and eat them within three months.")

MONTHS_SAID = re.compile(
    r"\b(?:january|february|march|april|may|june|july|august|september|october|november"
    r"|december|jan|feb|mar|apr|jun|jul|aug|sept|sep|oct|nov|dec)\b")
GOING_SAID = re.compile(
    r"\bwhere (?:should|can|could|shall|do|to) (?:i|we)? ?(?:go|get|find|shop)\b"
    r"|\bwhere to (?:go|shop)\b|\bweeks? abroad\b")
EATING_WORDS = frozenset("meal dinner cook cooking eat eating food shop shopping menu recipe "
                         "supper lunch tea feed leftover batch portion".split())
PLAN_WORDS = frozenset("batch batches batchcook freezer freeze freezing portion portions".split())
CHEAP_PLAN_WORDS = frozenset("cheap cheapest skint budget broke money afford tight".split())
TONIGHT_WORDS = frozenset("tonight tonite tnite today now".split())

TIME_PHRASES = (("quarter of an hour", 15), ("half an hour", 30), ("an hour", 60))
TIME_WORDS = (("forty five", 45), ("forty", 40), ("thirty", 30), ("twenty five", 25),
              ("twenty", 20), ("eighteen", 18), ("fifteen", 15), ("twelve", 12), ("ten", 10),
              ("five", 5))
TIME_TWENTY = ("Twenty minutes is enough for: a stir-fry, with the rice on before anything else; "
               "pasta with garlic, chilli and a tin of tomatoes; or an omelette with bread and "
               "salad, which is the quickest of the three.")
TIME_SOON = ("Twenty-five minutes is enough for: a stir-fry, with the rice on before anything "
             "else; pasta with garlic, chilli and a tin of tomatoes; an omelette with bread and "
             "salad; or vegetables cut small and roasted 25 minutes at 200C while couscous "
             "steeps in the same time.")
TIME_MIDDLING = ("Half an hour is enough for: chicken pieces or sausages in the oven while the "
                 "potatoes boil, a tray of vegetables cut small roasted with couscous, or pasta "
                 "baked with a tin of tomatoes and cheese. Put the oven on first and the kettle "
                 "second, and with an hour you can leave a chilli or a curry to simmer.")


def _minutes_named(said):
    found = re.search(r"\b(\d{1,3})\s*(?:minutes?|mins?)\b", said)
    if found:
        return int(found.group(1))
    for phrase, minutes in TIME_PHRASES:
        if phrase in said:
            return minutes
    for phrase, minutes in TIME_WORDS:
        if re.search(r"\b" + phrase + r"\b", said):
            return minutes
    return None


def _time_budget(memory, understood, text=None):
    words = understood.get("words")
    if not isinstance(words, (list, tuple)):
        words = str(understood.get("clean") or "").split()
    said = " ".join(_fold(word) for word in words)
    minutes = _minutes_named(said)
    if minutes is None:
        return None
    if minutes <= 15:
        return ANY_MEAL
    if minutes <= 22:
        return TIME_TWENTY
    if minutes <= 28:
        return TIME_SOON
    if minutes <= 90:
        return TIME_MIDDLING
    return None


CHEAP_DISHES = (
    "a big spag bol with lentils cooked in with the mince",
    "a tray of roast vegetables with couscous and feta",
    "sausages with mash and onion gravy",
    "a chickpea and tomato curry with rice",
    "beans on toast with a poached egg",
)
CHEAP_TAIL = ("Eggs, tins, pasta, rice and frozen veg are where the money goes furthest, and the "
              "mince stretched with lentils does two dinners.")
CHEAP_TAIL_MEATFREE = ("Eggs, tins, pasta, rice and frozen veg are where the money goes furthest, "
                       "and a pot of lentils or beans does two dinners.")


def _cheap_dinners(banned=frozenset()):
    dishes = [one for one in CHEAP_DISHES
              if not _mentions(one, banned) and not _bans(tuple(one.split()), one, banned)]
    if not dishes:
        dishes = list(CHEAP_DISHES)
    if _mentions(CHEAP_TAIL, banned) or _bans(("mince",), CHEAP_TAIL, banned):
        tail = CHEAP_TAIL_MEATFREE
    else:
        tail = CHEAP_TAIL
    listed = ", ".join(dishes[:-1]) + " or " + dishes[-1]
    return ("Cheap dinners that feed four for about a fiver: " + listed + ". " + tail)


PROTEIN_SOURCES = ("You can get plenty without meat: eggs, milk, cheese and yogurt, a tin of beans "
                   "or chickpeas (about 15g of protein), lentils (about 18g per 100g dry), tofu, "
                   "nuts, seeds and wholegrains. Spread it over the day rather than one meal - "
                   "beans at lunch, eggs or tofu at dinner, yogurt and nuts as a snack - and there "
                   "is no need to count anything.")
PROTEIN_COMPLETE = ("Rice and beans together give all the amino acids the body cannot make itself, "
                    "and so do beans on toast, lentils with rice, and hummus with bread. You do "
                    "not have to pair them at the same meal, either: it is the day's food that "
                    "counts, not one plate, so a peanut butter sandwich and a bean chilli on the "
                    "same day is enough.")


def _protein(memory, understood):
    text = str((understood or {}).get("clean") or "").lower()
    if re.search(r"\bcomplete\b", text):
        return PROTEIN_COMPLETE
    return PROTEIN_SOURCES
BAKED_APPLES = ("Baked apples take 25 to 30 minutes at 180C (160C fan, gas 4): core them, score "
                "the skin round the middle so they do not burst, fill the hole with raisins, brown "
                "sugar and a knob of butter, and stand them in a dish with a splash of water so "
                "they do not dry out. A big Bramley needs 35 to 40 minutes and goes to a fluff, "
                "while an eater keeps its shape and is done when a knife slides in with no push.")


BAKED_FRUIT = {
    "pear": ("Baked pears take 25 to 30 minutes at 180C (160C fan, gas 4): halve them and scoop "
             "the core out with a teaspoon, then sit them cut side up in a dish with a splash of "
             "water, a knob of butter and a spoon of sugar. A firm Conference needs 35 to 40 "
             "minutes and a ripe one 20, and either is done when a knife slides in with no push."),
    "plum": ("Baked plums take 15 to 20 minutes at 180C (160C fan, gas 4): halve them and take "
             "the stones out, sit them cut side up in a dish with a spoon of sugar and a splash "
             "of water. They give off a lot of juice, and that syrup is the best part; a whole "
             "one needs 10 minutes more."),
    "peach": ("Baked peaches and nectarines take 20 to 25 minutes at 180C (160C fan, gas 4): "
              "halve them and take the stones out, cut side up in a dish with a knob of butter "
              "and a spoon of sugar. A ripe one gives to a knife at 20 minutes, and a hard one "
              "needs 10 minutes more and is better poached."),
    "quince": ("Baked quince takes far longer than the softer fruit: about 1 hour 30 minutes at "
               "160C (140C fan, gas 3), halved and cored, cut side up in a dish with sugar and a "
               "splash of water. It goes from pale and hard to pink and soft, and it is done when "
               "a knife goes in with no resistance."),
}

STEWED_FRUIT = {
    "apple": ("Stewed or poached: peel, core and slice them, then simmer in a pan with a spoon "
              "of sugar, a splash of water and a squeeze of lemon for 8 to 10 minutes with the "
              "lid on, until they fall apart. A Bramley takes 5, and an eater holds its shape."),
    "pear": ("Stewed or poached pears: peel, halve and core them, then simmer with a spoon of "
             "sugar, a splash of water and a squeeze of lemon for 10 to 15 minutes with the lid "
             "on, until a knife goes in easily. A firm pear takes the 15, and poaching them whole "
             "in wine or syrup wants 20 to 25."),
    "plum": ("Stewed plums: halve them and take the stones out, then simmer with a spoon of sugar "
             "and a splash of water for 6 to 8 minutes with the lid on, until they slump. They "
             "fall apart quickly, so stop while they still hold their shape."),
    "peach": ("Stewed peaches: halve and stone them, then simmer with a spoon of sugar and a "
              "splash of water for 5 to 8 minutes with the lid on. The skins slip off after a "
              "minute in the hot liquid if you want them off."),
    "quince": ("Stewed quince: peel, quarter and core them, then simmer with sugar and a squeeze "
               "of lemon for 45 minutes to an hour with the lid on, until they turn pink and "
               "soft."),
}

MICROWAVED_FRUIT = {
    "apple": ("In a microwave: core them, stand them in a dish with a centimetre of water, cover "
              "it and give two medium apples 6 to 8 minutes on full power, turning them once. "
              "They go soft rather than brown, so finish them under the grill for 3 minutes if "
              "you want the tops caught."),
    "pear": ("In a microwave: halve and core them, stand them cut side up in a dish with a "
             "centimetre of water, cover it and give two halves 4 to 6 minutes on full power. "
             "They go soft rather than brown, so finish them under the grill for 3 minutes if "
             "you want the tops caught."),
    "plum": ("In a microwave: halve and stone them, stand them in a dish with a centimetre of "
             "water and a spoon of sugar, cover it and give four halves 3 to 4 minutes on full "
             "power. They collapse fast, so check them at 3."),
    "peach": ("In a microwave: halve and stone them, stand them cut side up in a dish with a "
              "centimetre of water, cover it and give two halves 4 to 6 minutes on full power. A "
              "ripe one is done at 4; a hard one is better in the oven than longer in there."),
    "quince": ("A quince will not soften in a microwave - it is too hard and too dry - so give it "
               "the oven, or the pan with sugar and lemon for 45 minutes to an hour."),
}


_SOFT_FRUIT = re.compile(r"\b(?:going soft|gone soft|soft spot|soft spots|getting soft|"
                         r"turning soft)\b")
_SOFT_FRUIT_WANTS_THE_OVEN = re.compile(
    r"\b(?:oven|bake|baked|baking|roast|roasted|roasting|stew|stewed|stewing|poach|poached|"
    r"poaching|microwave|microwaved|use up|using up|what can i do with|what can i make with|"
    r"what do i do with)\b")


def _a_soft_fruit_is_still_a_cooking_question(understood):
    text = str((understood or {}).get("clean") or "").lower()
    return bool(_SOFT_FRUIT_WANTS_THE_OVEN.search(text)) or not _SOFT_FRUIT.search(text)


def _the_baked_fruit(text):
    for name, fruit in (("quince", "quince"), ("nectarine", "peach"), ("peach", "peach"),
                        ("plum", "plum"), ("pear", "pear")):
        if re.search(r"\b" + name + r"(?:es|s)?\b", text):
            return fruit
    return "apple"


def _bake_fruit(memory, understood):
    text = str((understood or {}).get("clean") or "").lower()
    fruit = _the_baked_fruit(text)
    if re.search(r"\b(?:stew|stews|stewed|stewing|boil|boils|boiled|boiling|simmer|simmered|"
                 r"simmering|poach|poached|poaching|puree|pureed)\b", text):
        return STEWED_FRUIT[fruit]
    if re.search(r"\bmicrowave\b", text):
        return MICROWAVED_FRUIT[fruit]
    return BAKED_FRUIT.get(fruit, BAKED_APPLES)


JACKET_BAKE = (
    "Prick it, rub it with oil and salt, and bake at 200C (180C fan) for about an hour for a "
    "medium potato, until a knife slides in with no resistance. The oil and salt are what make "
    "the skin crisp; 8 minutes in the microwave first cuts the oven time to 25.")
JACKET_FILL = (
    "Cheese and beans, tuna mayo, coleslaw, chilli or last night's bolognese: butter and salt "
    "first, then the topping, and back in the oven for 5 minutes if you want the cheese melted. "
    "A wet filling wants something crisp alongside - a pickled onion, a handful of salad.")


def _jacket(understood):
    said = str((understood or {}).get("clean") or "").lower()
    if re.search(r"\b(fill|filling|fillings|topping|toppings|goes with|what with|put in|"
                 r"beans|cheese|tuna|coleslaw|chilli)\b", said):
        return JACKET_FILL
    return JACKET_BAKE


JAM_RECIPE = (
    "Weigh the fruit, then add the same weight of sugar and simmer it until it reaches 104 to "
    "105C, which is 10 to 15 minutes of hard boiling: test a drop on a cold plate and if it "
    "wrinkles when you push it, it is ready. Soft fruit needs a squeeze of lemon for pectin, and "
    "the jars go in hot.")
CHUTNEY_RECIPE = (
    "Chutney is fruit or veg with half its weight of sugar and enough vinegar to cover, simmered "
    "down until a spoon drawn across the pan leaves a trail - an hour or two - then potted in hot "
    "jars and left 3 to 4 weeks to mellow. The vinegar is what keeps it, so do not skimp on it.")


def _jam_make(understood):
    said = str((understood or {}).get("clean") or "").lower()
    if "chutney" in said or "preserve" in said:
        return CHUTNEY_RECIPE
    return JAM_RECIPE


POACH_FISH = (
    "Poach {fish} in water that is trembling rather than bubbling, about 80C, for 6 to 8 minutes "
    "for a fillet, or 15 to 20 minutes for a whole side in a 120C oven. It is done when a knife "
    "goes into the thick end and the flakes just separate; milk, a bay leaf and a few peppercorns "
    "in the water are what a restaurant poach tastes of.")


def _poach_fish(understood):
    text = str((understood or {}).get("clean") or "").lower()
    for name in ("haddock", "cod", "trout", "salmon"):
        if re.search(r"\b" + name + r"\b", text):
            return POACH_FISH.format(fish=name)
    return POACH_FISH.format(fish="salmon")


MUSHROOM_WASH = (
    "Rinse them quickly under the tap and dry them on a tea towel - mushrooms take on very "
    "little water in a few seconds, and a wipe with damp kitchen paper leaves the grit in the "
    "gills. Do not leave them soaking in a bowl, which is the one thing that does make them "
    "watery, and cook them straight after.")
MUSHROOM_PEEL = (
    "No need: the skin on button, chestnut and portobello mushrooms is thin and it is flavour, so "
    "wipe or rinse them, snap out the stalk if it is woody, and slice. Peel only a field mushroom "
    "with gritty skin or a shiitake with a tough stem, and cut the stem off at the cap rather "
    "than peeling it.")


def _mushroom_wash(understood):
    said = str((understood or {}).get("clean") or "").lower()
    if re.search(r"\bpeel", said) or re.search(r"\bskin\b", said):
        return MUSHROOM_PEEL
    return MUSHROOM_WASH


def _meal_plan(memory, understood):
    words = [str(word).lower() for word in (understood.get("words") or [])]
    text = " ".join([str(understood.get("clean") or "").lower()] + _recent_user_turns(memory))
    folded = [_fold(word) for word in words]
    said = folded + [_fold(word) for word in re.findall(r"[a-z']+", text)]
    if ((MONTHS_SAID.search(text) or GOING_SAID.search(text))
            and not set(said).intersection(EATING_WORDS)):
        return None
    if any(word in PLAN_WORDS for word in said) or re.search(r"\bfreez|\bbatch", text):
        return PLAN_BATCH
    if any(word in CHEAP_PLAN_WORDS for word in said):
        return PLAN_CHEAP
    return PLAN_WEEK


def _same(word, wanted):
    return bool(word) and bool(wanted) and (word == wanted or word.startswith(wanted))


_BAKED_GOODS = ("cake", "cakes", "cupcake", "cupcakes", "muffin", "muffins", "bun", "buns",
                "scone", "scones", "brownie", "brownies", "blondie", "blondies", "cookie",
                "cookies", "biscuit", "biscuits", "shortbread", "flapjack", "flapjacks",
                "sponge", "sponges", "loaf", "loaves", "bun loaf", "traybake", "traybakes",
                "cheesecake", "cheesecakes", "madeira", "doughnut", "doughnuts", "donut",
                "donuts", "fruit cake", "victoria sponge")

_NO_SPREAD_RISE = tuple(name for name in _BAKED_GOODS
                        if name not in ("cookie", "cookies", "biscuit", "biscuits", "shortbread"))

_CAKE_NAMES = ("cake", "cakes", "cupcake", "cupcakes", "sponge", "sponges", "loaf cake",
               "victoria sponge", "madeira", "fruit cake", "traybake", "traybakes")
_NO_CAKE_RISE = tuple(name for name in _NO_SPREAD_RISE if name not in _CAKE_NAMES)


_NO_LOAF_RISE = tuple(name for name in _NO_SPREAD_RISE
                      if name not in ("loaf", "loaves", "bun loaf"))


_BAKE_KEEPING = ("keep", "keeps", "keeping", "kept", "last", "lasts", "how long", "freeze",
                 "freezes", "freezer", "fridge", "refrigerate", "store", "storing", "stored",
                 "stays fresh", "stay fresh", "still good", "gone off", "go off", "use by")

_BAKED = _BAKED_GOODS + ("baking", "bread", "breadcrumbs", "waffle", "waffles")

_BAKE_NAMES = (("cupcake", "cupcakes"), ("muffin", "muffins"), ("brownie", "brownies"),
               ("cookie", "cookies"), ("biscuit", "biscuits"), ("flapjack", "flapjacks"),
               ("scone", "scones"), ("sponge", "sponges"), ("loaf", "loaves"),
               ("traybake", "traybakes"), ("bread", "bread"), ("cake", "cakes"),
               ("bun", "buns"), ("tart", "tarts"), ("pie", "pies"), ("pastry", "pastry"))


def _the_bake_named(words):
    mass = ("bread", "pastry")
    for one, many in _BAKE_NAMES:
        if any(_same(word, many) or _same(word, one) for word in words):
            return (one, False) if one in mass else (many, True)
    return "", False

_BAKE_DISH = ("pasta", "lasagne", "lasagna", "moussaka", "cannelloni", "macaroni",
              "macaroni cheese", "fish pie", "cottage pie", "shepherds pie", "shepherd's pie",
              "quiche", "frittata", "gratin")

_RICE_DISH = ("biryani", "paella", "pilaf", "pilau", "fried rice", "risotto", "couscous")

_DIP_DISH = ("hummus", "houmous", "pesto", "guacamole", "tapenade", "dip", "dips")

_SAUCE_DISH = ("bolognese", "bolognaise", "bol", "ragu", "curry", "chilli", "chili", "stew",
               "casserole", "soup", "sauce", "dahl", "dal", "tagine", "goulash", "stroganoff")


def _asks_why(words):
    said = " ".join(words)
    return ("why" in words or "howcome" in words or "what did i do wrong" in said
            or "what went wrong" in said or "what am i doing wrong" in said)


def _dry(memory, understood):
    text = str(understood.get("clean") or "").lower()
    words = [str(word).lower() for word in (understood.get("words") or [])]
    if any(_same(word, wanted) for word in words
           for wanted in ("biscuit", "biscuits", "cookie", "cookies", "shortbread")):
        return None
    rescue = ("Serve it with something wet — gravy, a spoon of yoghurt, a squeeze of lemon and oil — "
              "and next time take it out 5 minutes earlier and rest it under foil. Dry meat or fish is "
              "nearly always overcooked, and resting is what keeps the juice in.")
    if _asks_why(words):
        rescue = ("Dry meat or fish is nearly always overcooked: it went past the point where the "
                  "juices set, or it was cooked hard and fast without a rest, so the juice ran out "
                  "of it. Take it out 5 minutes earlier next time and rest it under foil, and serve "
                  "this one with something wet - gravy, a spoon of yoghurt, a squeeze of lemon and "
                  "oil.")
    said = " ".join(words)
    if any(word in ("pasta", "spaghetti", "penne", "macaroni", "tagliatelle", "fusilli", "noodles",
                    "noodle", "rice noodles", "udon") for word in words) and any(
                        word in ("overcooked", "over-cooked", "over cooked", "mushy", "soggy")
                        for word in words):
        return ("Overcooked pasta cannot be brought back, but it can be used: drain it, toss it in "
                "oil so it stops sticking, and fold it into a bake, a frittata or a soup where soft "
                "is fine. Next time salt the water properly, take it off a minute before the packet "
                "says, and taste a piece rather than trusting the clock, because a big pan of "
                "boiling water comes back to the boil slowly and the first minute is not cooking.")
    named = any(_same(word, wanted) for word in words for wanted in _BAKE_DISH) or any(
        " " in wanted and wanted in said for wanted in _BAKE_DISH)
    if named and any(
            word in ("bake", "baked", "baking", "oven", "overcooked", "over-cooked", "dry")
            for word in words):
        return ("A bake or a pie dries out when it goes in uncovered or stays in too "
                "long: stir a "
                "splash of milk or a spoon of passata through the sauce, cover it with foil and "
                "give it 10 minutes at 180C to come back. Next time keep a little bechamel back "
                "to pour over the top, and cover it for the first 20 minutes.")
    if any(_same(word, wanted) for word in words for wanted in _BAKED):
        thing, plural = _the_bake_named(words)
        head = ("Dry " + thing + (" are" if plural else " is")) if thing else "A dry bake is"
        return (head + " usually a minute or two too long in the oven, or a little too much "
                "flour. Take it out as soon as a skewer comes out with a crumb on it, weigh the "
                "flour rather than scooping it with a cup, and don't overbeat - and a dry bake is "
                "still good with cream, custard or something wet on it.")
    if any(word in ("rice", "ricecooker") for word in words) or any(
            _same(word, wanted) for word in words for wanted in _RICE_DISH):
        return ("Dry rice means too little water or too long on the heat: add a splash of hot water, "
                "put the lid back on and steam it for 5 minutes on the lowest heat. Next time use one "
                "and a half parts water to one of rice, lid on, 10 minutes, then rest it off the heat.")
    if any(word in _DIP_DISH for word in words):
        return ("Loosen it a spoonful at a time rather than all at once: a splash of cold water and "
                "a squeeze of lemon for hummus, or a little more oil for a pesto, blitzed or stirred "
                "through until it is soft again. A dull, dry taste is usually not enough salt or "
                "acid rather than not enough oil.")
    if any(_same(word, wanted) for word in words for wanted in _SAUCE_DISH):
        return ("A sauce that has gone dry wants liquid back, not less time in the pan: a little "
                "stock, the water the pasta cooked in, a spoon of tinned tomatoes or a splash of "
                "milk, then the lid on and five minutes at a bare simmer. A stew, a "
                "curry or a chilli tightens as it stands, so loosen it at the end rather than "
                "watering it at the start, and keep the heat low enough that it does not catch.")
    if any(_same(word, "pastry") for word in words):
        return ("Dry pastry wants a sprinkle of cold water and a 20 minute rest in the fridge, then roll "
                "it between two sheets of baking paper. Next time keep the fat cold and add water a "
                "tablespoon at a time, because pastry dries out fast once the flour is in.")
    if "safe to eat" in text or "ok to eat" in text or any(
            word in ("safe", "safely", "food-poisoning", "ill") for word in words):
        return ("Dry is a texture problem, not a safety one: if it was cooked through (75C inside, no "
                "pink meat and clear juices) it is fine cold, or reheated once until steaming. " + rescue)
    return rescue


def _bread(memory, understood):
    words = [str(word).lower() for word in (understood.get("words") or [])]
    said = " ".join(words)
    wholemeal = any(word in ("wholemeal", "wholewheat", "whole") for word in words) or any(
        phrase in said for phrase in ("whole wheat", "whole-wheat", "wholemeal flour"))
    brown = any(word in ("brown", "granary", "malted") for word in words)
    if wholemeal or brown:
        return ("Use 500g of wholemeal flour (or 300g wholemeal flour and 200g strong white "
                "flour, which rises more easily), 7g of dried yeast, 10g of salt and 350ml of warm "
                "water: wholemeal drinks "
                "more and takes longer, so leave it somewhere warm 2 to 3 hours until it has "
                "doubled rather than 1 to 2. Knead 10 minutes, shape it into a tin, leave it 45 "
                "minutes more, then bake at 220C (200C fan) for 35 to 40 minutes and tap the base: "
                "a hollow sound means it is done.")
    return ("Put 500g strong white flour, 7g of dried yeast, 10g of salt and 320ml of warm water in "
            "a bowl, mix it to a sticky dough and knead 10 minutes until it stops tearing. Leave it "
            "somewhere warm 1 to 2 hours until it has doubled, shape it into a tin, leave it another "
            "45 minutes, then bake at 220C (200C fan) for 30 to 35 minutes and tap the base: a "
            "hollow sound means it is done.")


COMING_APART = ("falls apart", "fall apart", "falling apart", "fell apart", "fallen apart",
                "falls to bits", "falling to bits", "fell to bits", "came apart", "coming apart",
                "breaks up", "breaking up", "breaks apart", "breaking apart", "broke up",
                "broken up", "does not hold together", "doesn't hold together",
                "doesnt hold together", "will not hold together", "won't hold together",
                "wont hold together", "not holding together", "disintegrates",
                "disintegrated", "crumbling", "crumbles")

_FISH_NAMES = ("fish", "fillets", "fillet", "white fish", "cod", "haddock", "pollock",
               "hake", "tilapia", "basa", "fish fillet", "fish fillets", "salmon",
               "fishcake", "fishcakes", "fish cake", "fish cakes", "monkfish", "plaice",
               "trout", "sea bass", "bream", "swordfish", "tuna steak")
_COMING_APART_ON_PURPOSE = ("stew", "casserole", "pulled", "slow cooker", "slow cooked",
                            "braise", "braised", "tagine", "goulash", "how long", "until it")
_MUSHY_OWN_ROW = ("pasta", "spaghetti", "penne", "macaroni", "noodles", "noodle", "rice",
                  "peas", "beans", "lentils", "porridge", "oats", "couscous")


def _falls_apart(memory, understood):
    words = [str(word).lower() for word in (understood.get("words") or [])]
    said = " " + " ".join(words) + " "
    text = str(understood.get("clean") or "").lower()
    whole = said + " " + text + " "
    why = _asks_why(words)

    def names(*wanted):
        return any(_same(word, one) for word in words for one in wanted)

    if names(*_FISH_NAMES):
        if names("pie", "pies", "fish pie"):
            return ("A fish pie comes apart because the sauce is thin, not because the fish broke: "
                    "make the white sauce thick enough to hold a spoon (about 40g butter and 40g "
                    "flour to 400ml milk) and let the pie stand 10 minutes out of the oven before "
                    "you cut it, so the starch sets. A crumble or a pastry lid that slides off is "
                    "the same fault - too much liquid under the crust.")
        if why:
            return ("A fillet comes apart for two reasons: it went into the pan wet, so it steamed "
                    "instead of sealing, or it was moved before the skin had set. Dry it with "
                    "kitchen paper, get the pan properly hot, lay it in skin side down, press it "
                    "flat for ten seconds and leave it four minutes before you turn it once. A "
                    "fillet that still breaks up was probably overcooked, so take it out the "
                    "moment the thickest part just flakes.")
        return ("Pat the fillet dry with kitchen paper and get the pan properly hot before it goes "
                "in: wet fish on a cool pan steams instead of sealing, and that is what makes it "
                "break up. Lay it in skin side down, press it flat for ten seconds, then leave it "
                "alone for four minutes - it releases itself when the skin has set - turn once and "
                "give it two more, and take it out the moment the thickest part just flakes. "
                "Baking at 200C (180C fan) for 12 to 15 minutes on baking paper is the gentler "
                "way, and a fish stew is meant to break up: stir it in at the end.")

    if names("meatballs", "meatball", "kofta", "koftas", "rissoles", "falafel", "sausage meat",
             "meatloaf", "patties", "patty"):
        return ("Something ground and shaped needs a binder and a rest: one egg and a handful of "
                "breadcrumbs per 500g, mix it just until it holds - overworking makes it springy "
                "- then chill it 20 minutes before it meets the pan, because cold holds together "
                "and warm does not. Sear it in a hot pan without moving it for two minutes a side "
                "so a crust forms, then finish it in a 200C oven rather than turning it again. Too "
                "lean a mince is the other cause: 20% fat is what keeps it in one piece.")

    if names("tofu", "paneer", "halloumi", "tempeh"):
        return ("Press the water out first: wrap the block in a clean tea towel with a weight on it "
                "for 15 minutes, then dust it in cornflour before it goes in the pan. That dry "
                "coat is what holds a crust together, and a hot pan with a little oil that you "
                "leave alone for three minutes does the rest. In a stir-fry, add it last and fold "
                "rather than stir.")

    if names("potatoes", "potato", "mash"):
        return ("Floury potatoes break up and waxy ones hold their shape, so buy the right one: "
                "Maris Piper or King Edward for mash and roast, Charlotte or Jersey Royal for a "
                "salad or a tray of boiled ones. Cut them the same size, cook them from cold "
                "water at a bare simmer rather than a rolling boil, and drain them in a colander "
                "for a minute to steam dry before they go in the oven.")

    if names("dumplings", "dumpling", "gnocchi"):
        return ("A dumpling falls apart when the dough is too wet or the pot is at a rolling boil: "
                "use 100g of suet to 200g of self-raising flour with just enough cold water to "
                "bring it together, drop them onto the stew, put the lid on and keep it at a bare "
                "simmer for 20 minutes without lifting the lid. Gnocchi want the same gentle heat, "
                "and they are done a minute after they float.")

    if names("cake", "cakes", "sponge", "bread", "loaf", "loaves", "pastry", "scone", "scones",
             "biscuit", "biscuits", "cookie", "cookies", "brownie", "brownies", "muffin",
             "muffins", "traybake", "yorkshire pudding", "yorkshires", "burger", "burgers",
             "rice", "peas", "pasta", "noodles", "omelette", "pancake", "pancakes"):
        return None

    if names("chicken", "turkey", "lamb", "beef", "pork", "roast", "joint", "shoulder",
             "brisket", "ham", "gammon"):
        return ("Coming apart is how you know it is done: a shoulder, a brisket or a chicken thigh "
                "is ready when it pulls apart with no resistance, and a whole bird is done at 74C "
                "in the thickest part of the thigh. If it is coming apart before it is cooked "
                "through, the heat was too high - turn it down to 150C (130C fan), add a splash of "
                "water to the tin and give it another hour covered, because slow and low is what "
                "turns the connective tissue to gelatine rather than drying the meat out.")

    if names("stew", "casserole", "tagine", "goulash", "braise", "pulled"):
        return ("Nothing has gone wrong: a stew, a braise and a slow-cooked shoulder are meant to "
                "come apart, and that is the sign the connective tissue has turned to gelatine. A "
                "shoulder at 150C takes 3 to 4 hours; if it is coming apart before you want it to, "
                "take it off the heat 20 minutes early and let it sit covered, or lift the pieces "
                "out and reduce the liquid on its own.")

    if any(cue in whole for cue in _COMING_APART_ON_PURPOSE):
        return ("Nothing has gone wrong if it is a stew, a braise or a slow-cooked shoulder: they "
                "are meant to come apart, and that is the connective tissue turning to gelatine. A "
                "shoulder at 150C takes 3 to 4 hours. If it is breaking up before you want it to, "
                "take it off the heat early and let it sit covered.")

    if names(*_MUSHY_OWN_ROW):
        return None

    if why:
        return ("It is nearly always one of two things: it was cooked too long, so what held it "
                "together gave up, or it was turned and moved before it had a crust to hold onto. "
                "Take it off the heat a little earlier next time and leave it alone in the pan "
                "until it releases itself.")
    return ("Handle it less and cook it a little less: food comes apart when it is overcooked, or "
            "when it is moved in the pan before it has sealed. Dry the surface, get the pan hot, "
            "leave it alone until it releases itself, and turn it once. If it is already in "
            "pieces, a bake, a soup or a sauce is the way to serve it rather than a plate.")


_DOUGH_WET = ("wet", "sticky", "slack", "runny", "sloppy", "tacky", "gooey")
_DOUGH_DRY = ("tight", "stiff", "dry", "firm", "tough", "stretchy", "elastic", "springy",
              "tearing", "tears", "resists", "resist")
_DOUGH_NOT = ("not", "no", "never", "isnt", "isn't", "arent", "aren't", "dont", "don't",
              "doesnt", "doesn't", "wasnt", "wasn't", "cant", "can't", "hardly")


def _dough(memory, understood):
    words = [str(word).lower() for word in (understood.get("words") or [])]
    direction = ""
    for index, word in enumerate(words):
        negated = any(
            earlier in _DOUGH_NOT or earlier.endswith("n't")
            for earlier in words[max(0, index - 2):index])
        if word in _DOUGH_WET:
            direction = "more flour" if not negated else "more water"
        elif word in _DOUGH_DRY:
            direction = "more water" if not negated else "more flour"
    if direction == "more flour":
        return ("Add flour a spoonful at a time and knead it in before you judge, because a dough "
                "is wettest in the first few minutes: it should cling to your hand and come away "
                "clean. Wetter is better for an open crumb, so stop as soon as it stops running "
                "and keep a little of the water back next time, since flour alone can be 10% "
                "different in how much it drinks.")
    return ("Add water a spoonful at a time and knead a minute after each one: a stiff dough "
            "reads drier than it is, because the flour takes a few minutes to take up what is "
            "already in there, and you only feel the difference after kneading. A bread dough "
            "should be tacky rather than sticky - it clings to your hand but comes away clean - "
            "and it is ready when a piece stretches thin enough to see light through without "
            "tearing. If you overshoot, a spoonful of flour brings it back.")


_MASH_DISH = ("mash", "mashed potato", "mashed potatoes", "duchess potatoes")
_CHICKPEA_WET = ("hummus", "houmous", "humus")
_GREEN_DIP_WET = ("pesto",)
_OLIVE_DIP_WET = ("tapenade",)
_DIP_DISH_WET = ("dip", "dips")
_AVOCADO_WET = ("guacamole", "guac", "avocado", "avocados")
_PASTRY_WET = ("quiche", "pie", "tart", "flan", "pastry case")
_PASTRY_DOUGH_WET = ("pastry", "shortcrust", "shortcrust pastry", "pie crust")
_DUMPLING_WET = ("dumpling", "dumplings", "suet", "dumpling mix", "cobbler topping")

_RICE_WET = ("rice", "ricecooker", "biryani", "paella", "pilaf", "pilau")
_RISOTTO_WET = ("risotto", "risotto rice", "arborio")
_COUSCOUS_WET = ("couscous", "bulgur", "bulghur")
_WET_FOOD = ("bulgur", "bulghur", "avocado", "avocados", "guac", "tart", "flans",
             "shortcrust", "dough", "arborio", "rice cooker",
             "moussaka", "cannelloni", "gratin", "macaroni", "lasagne", "lasagna",
             "falafels", "fritter", "fritters", "bhaji", "bhajis", "kofta", "koftas",
             "fishcakes", "fish cakes", "patties", "burger", "burgers",
             "batter", "oats", "oatmeal", "grits", "icing", "frosting", "buttercream",
             "ganache", "smoothie", "smoothies", "milkshake", "yoghurt", "yogurt", "raita",
             "tzatziki", "labneh", "dal", "lentils", "lentil", "coleslaw", "slaw", "salad",
             "meatball", "stuffing", "stuffings")
_BAKE_WET = ("lasagne", "lasagna", "moussaka", "cannelloni", "pasta bake", "macaroni cheese",
             "mac and cheese", "fish pie", "cottage pie", "shepherds pie", "shepherd's pie",
             "gratin", "frittata", "traybake")
_FRY_MIX_WET = ("falafel", "falafels", "fritter", "fritters", "bhaji", "bhajis", "kofta",
                "koftas", "fishcake", "fishcakes", "fish cake", "fish cakes", "patty", "patties",
                "burger", "burgers", "sausage", "sausages", "sausage meat", "meatloaf",
                "meatballs", "stuffing", "forcemeat")
_BREAD_DOUGH_WET = ("dough", "doughs", "bread dough", "pizza dough",
                    "sourdough", "focaccia", "naan", "ciabatta", "rolls", "buns", "brioche",
                    "bagels", "wholemeal", "pitta")
_BATTER_WET = ("batter", "cake mixture", "sponge mixture", "pancake", "pancakes", "waffles",
               "yorkshire", "yorkshires", "crepe", "crepes", "drop scones")
_PORRIDGE_WET = ("porridge", "oats", "oatmeal", "porridge oats", "oat", "grits")

_WET_CUSTARD = ("custard", "creme anglaise", "creme patissiere", "creme patisserie",
                "pastry cream")
_WET_ICING = ("icing", "frosting", "buttercream", "ganache", "glaze")
_WET_DRINK = ("smoothie", "smoothies", "milkshake", "milkshakes", "shake", "shakes")
_WET_YOGHURT = ("yoghurt", "yogurt", "raita", "tzatziki", "labneh", "yoghurt dip")
_WET_DIP_WORDS = ("raita", "tzatziki", "dip", "dips", "cucumber", "mint")
_WET_DAL = ("dal", "dhal", "daal", "lentil", "lentils", "lentil soup", "split peas")
_WET_SLAW = ("coleslaw", "slaw", "salad", "salads")

_PLANT_MILK = ("oat milk", "oatmilk", "almond milk", "soy milk", "soya milk", "rice milk",
               "cashew milk", "hazelnut milk", "plant milk", "milk alternative", "coconut milk")
_PLANT_MILK_DISH = ("curry", "stew", "soup", "sauce", "cake", "batter", "smoothie", "porridge",
                    "rice pudding", "custard", "ice cream", "coffee", "tea", "chai", "latte")


def _watery(memory, understood):
    words = [str(word).lower() for word in (understood.get("words") or [])]
    said = " ".join(words)
    words = [word for word in words if word + " milk" not in said]
    if any(name in said for name in _PLANT_MILK) and not any(
            word in said for word in _PLANT_MILK_DISH):
        return ("A carton of oat, almond or soy milk that pours thin has separated: shake it hard "
                "for half a minute before you open it and it comes back together, and a cheap "
                "barista one holds up better in coffee. Homemade oat milk is thin by nature - "
                "blend 1 part oats to 4 of water, strain it lightly, and add a pinch of salt; it "
                "thickens as it stands in the fridge.")
    named = [names for names in (_MASH_DISH, _CHICKPEA_WET, _GREEN_DIP_WET, _OLIVE_DIP_WET,
                                 _DIP_DISH_WET, _AVOCADO_WET, _BAKE_WET, _FRY_MIX_WET,
                                 _BREAD_DOUGH_WET, _BATTER_WET, _PORRIDGE_WET,
                                 _PASTRY_WET, _PASTRY_DOUGH_WET,
                                 _RICE_WET, _RISOTTO_WET, _COUSCOUS_WET,
                                 _WET_CUSTARD, _WET_ICING, _WET_DRINK, _WET_YOGHURT,
                                 _WET_DAL, _WET_SLAW, _DUMPLING_WET)
             if any(_same(word, wanted) for word in words for wanted in names)
             or any(" " in wanted and wanted in said for wanted in names)]
    if any(names is _MASH_DISH for names in named):
        return ("Mash goes watery when the potatoes come out of wet water or the milk goes in cold: "
                "drain them, put the pan back on a low heat for a minute to steam the rest off, "
                "then mash with warm milk and butter. If it has already gone loose, warm it through "
                "in the pan and stir rather than adding anything - it firms up as the extra water "
                "steams away.")
    if any(names is _CHICKPEA_WET for names in named):
        return ("A hummus goes watery from water or ice going in with the chickpeas, or from too much "
                "lemon: drain the tin well, add a spoon more tahini or a few more chickpeas and "
                "blitz again, and serve it chilled, because it thickens as it sits. Loosen it later "
                "with oil, not water.")
    if any(names is _OLIVE_DIP_WET for names in named):
        return ("Tapenade goes watery from olives that came out of the brine wet, or from too much "
                "oil: drain them, dry them on a tea towel, and pound or pulse them with the capers "
                "and anchovy before the oil goes in. A thin tapenade wants more olives and a few "
                "capers, not less oil, and it firms up in the fridge.")
    if any(names is _GREEN_DIP_WET for names in named):
        return ("Pesto goes watery from basil that was still wet, or from too much oil in one go: "
                "dry the leaves in a tea towel, pound or pulse them with the nuts and cheese first "
                "and add the oil last, a little at a time. A thin pesto in the jar wants more grated "
                "cheese and nuts rather than less oil.")
    if any(names is _DIP_DISH_WET for names in named):
        return ("A dip goes watery from water in the base: drain the tin or squeeze out the grated "
                "vegetable, then thicken it with a spoon of the same solid - chickpeas, yogurt, "
                "cream cheese - and taste it again, because thinning it dilutes the salt and the "
                "acid too.")
    if any(names is _AVOCADO_WET for names in named):
        return ("Guacamole goes watery from over-ripe avocado or too much lime: mash it with a fork "
                "rather than a blender, drain any liquid off and stir in a little more avocado, and "
                "leave the stone in if you are keeping it - it slows the browning, not the water.")
    if any(names is _BAKE_WET for names in named):
        return ("A bake goes watery when the sauce was thin before it was layered, or the vegetables "
                "still had water in them. Next time drain and squeeze the veg and let the sauce "
                "come to a simmer with a spoon of cornflour slaked in cold water before it goes in. "
                "For this one, give it 10 to 15 minutes uncovered at the same heat, then rest it "
                "10 minutes before you cut it, and the sauce will firm up.")
    if any(names is _DUMPLING_WET for names in named):
        return ("A dumpling mix that is too wet wants plain flour a spoonful at a time until it "
                "stops sticking to the bowl, then shape them with wet hands and drop them onto a "
                "stew that is simmering, put the lid on and give them 20 minutes without lifting "
                "it. Too wet and they spread out into the gravy instead of sitting on top.")
    if any(names is _FRY_MIX_WET for names in named):
        return ("A mix that will not hold together is too wet to fry: squeeze grated onion or veg "
                "in a clean tea towel, stir in a spoonful of plain or gram flour, and chill it for "
                "30 minutes so the starch takes up the water. Make sure the oil is properly hot "
                "before the first one goes in - a cool pan is what turns a soft mix into a pancake.")
    if any(names is _BREAD_DOUGH_WET for names in named):
        return _dough(memory, understood)
    if any(names is _BATTER_WET for names in named):
        return ("A batter that is too wet wants flour, not heat: whisk in a spoonful at a time "
                "until it coats the back of the spoon, then let it rest 20 minutes so the flour "
                "takes up the liquid. Too thin and it will not hold the bubbles, so pancakes come "
                "out pale and flat rather than risen, and a cake will not hold its rise either.")
    if any(names is _PORRIDGE_WET for names in named):
        return ("Porridge that has gone too loose wants a minute more on the heat with the lid off "
                "and a stir, and less milk next time: 40g of oats to 300ml of milk or water is "
                "enough for one, and it thickens as it stands. Do not add more oats once it is "
                "cooking, because they will not soften in time.")
    if any(names is _RISOTTO_WET for names in named):
        return ("Risotto that will not thicken wants more stirring, not more heat: keep it moving "
                "and add the stock a ladle at a time, waiting for each one to be taken up, then beat "
                "in cold butter and grated cheese off the heat at the end - that is what makes it "
                "creamy and loose at the same time.")
    if any(names is _COUSCOUS_WET for names in named):
        return ("Couscous goes watery from too much water: pour it into a wide dish, fork it through "
                "to break up the clumps and leave it uncovered for 5 minutes so the steam escapes. "
                "Next time use the same volume of couscous and boiling water, cover it for 5 "
                "minutes, then fork it with a knob of butter rather than stirring it.")
    if any(names is _PASTRY_WET for names in named):
        return ("A quiche or a pie goes watery when the filling is too wet or the egg is undercooked: "
                "give it 5 to 10 minutes more in a 180C oven and it will set, and next time cook the "
                "vegetables or the fruit down first and let them cool, then blind-bake the case "
                "before the filling goes in.")
    if any(names is _PASTRY_DOUGH_WET for names in named):
        return ("Pastry is a dough, not a filling: if it is wet and sticky, work in a little more "
                "flour a spoon at a time, wrap it and give it 20 minutes in the fridge, and roll it "
                "between two sheets of baking paper rather than dusting it with more flour. Shortcrust "
                "wants about half its weight in fat to flour, and cold hands.")
    if any(names is _RICE_WET for names in named):
        return ("Rice goes watery from too much water or the lid coming off: tip it into a sieve, "
                "then back in the pan with the lid on and 5 minutes on the lowest heat to steam dry. "
                "Next time one and a half parts water to one of rice, lid on, and leave it alone.")
    if any(names is _WET_CUSTARD for names in named):
        return ("Custard that is thin has not had enough heat: stir a teaspoon of cornflour into a "
                "splash of cold milk, whisk it in and give it 2 more minutes on a low heat until it "
                "coats the back of the spoon. It also thickens as it cools, so take it off before "
                "it looks set rather than after.")
    if any(names is _WET_ICING for names in named):
        return ("Icing that is too thin wants icing sugar, a spoon at a time, beaten in until it "
                "holds a soft peak: a teaspoon of water or milk goes a long way, so add that in "
                "drops. A glaze is meant to be thin - it should coat the back of the spoon and run "
                "off in ribbons, which is a different job from icing a cake.")
    if any(names is _WET_DRINK for names in named):
        return ("A thin smoothie or shake wants less liquid and something solid: half a banana, a "
                "spoon of oats or yoghurt, or a handful of frozen fruit, blended again - the fruit "
                "and the ice are what give it body. Pour the milk or juice in last, a splash at a "
                "time, instead of all at the start.")
    if any(names is _WET_YOGHURT for names in named):
        pot = ("A pot of yoghurt that has gone watery has separated, and that is harmless: stir it "
               "back together, or spoon the whey off the top, or strain it through muslin or a "
               "clean tea towel in a sieve for an hour for a thicker pot.")
        dip = ("A yoghurt dip goes watery because the vegetables in it were wet: salt the grated "
               "cucumber or carrot for 10 minutes, squeeze it out in a tea towel, and fold it into "
               "thick yoghurt at the end - a spoon of cream cheese or labneh brings back one that "
               "has already split.")
        if any(word in said for word in _WET_DIP_WORDS):
            return dip + " " + pot
        return pot + " " + dip
    if any(names is _WET_DAL for names in named):
        return ("A thin dal wants the lid off for 10 more minutes, stirring now and then: it "
                "thickens as the lentils break up, and mashing a ladleful against the side of the "
                "pan and stirring it back in thickens it at once. Add water a splash at a time at "
                "the end, because dal sets as it cools.")
    if any(names is _WET_SLAW for names in named):
        return ("A watery salad is nearly always salt pulling the water out of the vegetables: salt "
                "the shredded cabbage or the cucumber for 10 minutes, squeeze it in a clean tea "
                "towel, and dress it just before it goes to the table. Mayo loosened with a splash "
                "of vinegar coats better than a thick spoonful.")
    pan_food = any(word in ("sauce", "sauces", "stew", "curry", "chilli", "chili", "gravy", "ragu",
                            "bolognese", "bolognaise", "daal", "dhal", "dal", "tagine", "goulash",
                            "casserole", "cassoulet", "broth", "stock", "soup", "soups", "jus")
                   for word in words)
    thin = pan_food or any(word in ("watery", "runny", "thin", "sloppy", "liquid", "thickens",
                                    "thicken", "reduce", "reduces") for word in words) or any(
        phrase in said for phrase in ("never thickens", "wont thicken", "won't thicken",
                                      "not thickening", "doesnt thicken", "doesn't thicken"))
    if not thin and any(phrase in said for phrase in ("too wet", "a bit wet", "is wet", "went wet",
                                                      "bit wet")):
        return ""
    return ("Take the lid off and let it simmer for 10 to 15 minutes: most of the water goes off in "
            "the steam. To thicken it properly, stir in a spoon of tomato puree, a handful of red "
            "lentils, or cornflour slaked in cold water, and give it 5 more minutes.")


def _lumpy(memory, understood):
    words = [str(word).lower() for word in (understood.get("words") or [])]
    if any(_same(word, "mash") or word in ("potato", "potatoes") for word in words):
        return ("Mash them while they're hot with plenty of butter and warm milk, and beat with a "
                "wooden spoon rather than a fork. Lumps come from cold potatoes or too little fat; "
                "if they're stubborn, push the mash through a sieve or a potato ricer.")
    if any(_same(word, "custard") for word in words):
        return ("Take it off the heat and whisk hard, then push it through a sieve. Custard goes "
                "lumpy when the heat is too high or the eggs go in too fast, so next time pour the "
                "hot milk into the eggs a splash at a time and cook it slowly, stirring.")
    if any(_same(word, "porridge") or _same(word, "oats") for word in words):
        return ("Beat in a splash more milk or water and whisk it hard; porridge lumps come from "
                "dry oats hitting hot liquid too fast. Next time stir the oats into cold liquid and "
                "bring it up slowly, stirring all the time.")
    return ("Whisk it hard with the pan off the heat and push it through a sieve, because lumps "
            "break up far better off the ring. Next time stir the flour into the fat before any "
            "liquid goes in, then add the liquid a splash at a time.")


_FREEZE_AVOID = ("make with", "cook with", "do with", "what can i make", "what can i cook", "ideas", "dinner", "tonight", "use up")
_CHEAP_AVOID = ("cheap", "cheap recipe", "cheap recipes", "cheap meal", "budget")
_MEAL_ASK_AVOID = ("cook with", "cooking with", "make with", "do with", "ideas", "idea", "dinner", "tonight", "meal", "meals", "recipes", "recipe")
WANT_SOMETHING_ELSE = ("bored", "bored of", "sick of", "tired of", "fed up", "had enough",
                       "what else", "something else", "anything else", "instead",
                       "other ideas")


_CLUMP_WORDS = ("clump", "clumps", "clumped", "clumping", "lump", "lumps", "stuck", "sticks",
                "sticking", "together", "gluey", "sticky")


_EGG_STORE = ("store", "storing", "stored", "keep", "keeps", "keeping", "last", "lasts",
              "longer", "fridge", "fridged", "freeze", "room", "counter", "cupboard")
_EGG_STORE_TEXT = ("Keep eggs cold and steady: in the fridge, in their carton, pointy end down, "
                   "away from anything strong-smelling, because the shells are porous. Stored that "
                   "way they keep well past their date. ")
_EGG_TEST_TEXT = ("Put a suspect egg in a glass of water: one that lies flat on the bottom is "
                  "fresh, one that stands on end is older but fine, and one that floats is past it. ")


def _eggs(memory, understood):
    words = [str(word).lower() for word in (understood.get("words") or [])]
    if any(word in ("fresh", "off", "bad", "rotten", "float", "test", "edible", "safe",
                    "date", "dated", "expired", "expiry", "ok", "okay", "fine", "use",
                    "usable", "eat", "eaten", "yesterday", "week", "weeks", "old")
           for word in words) and not any(word in _EGG_STORE for word in words):
        return _EGG_TEST_TEXT + _EGG_STORE_TEXT.strip()
    return _EGG_STORE_TEXT + _EGG_TEST_TEXT.strip()


def _pasta_cook(memory, understood):
    words = [str(word).lower() for word in (understood.get("words") or [])]
    text = ("Use a big pan of well-salted water, about 10g of salt per litre, and cook the pasta "
            "one minute less than the packet says. Keep a mug of the cooking water: a splash of it "
            "makes any sauce cling to the pasta.")
    if any(word in _CLUMP_WORDS for word in words):
        text += (" Clumping is the pasta sitting still in water that is not deep or hot enough, so "
                 "stir it for the first minute and again every couple of minutes, and leave the "
                 "oil out: it stops the sauce clinging.")
    return text


def _popcorn_make(memory, understood):
    words = [str(word).lower() for word in (understood.get("words") or [])]
    pan = ("Three kernels and a tablespoon of oil in a big lidded pan over medium heat, and when "
           "those three pop, add a single layer of kernels and put the lid back on. Shake the pan "
           "every so often and take it off the heat when the pops slow to one every few seconds, "
           "about 3 minutes for four tablespoons of kernels. Tip it into a bowl, salt it while it "
           "is hot, and leave the lid off so the steam gets away and it stays crisp.")
    microwave = ("Put a quarter of a cup of kernels in a paper bag or a bowl with a plate over it "
                 "and give it 2 to 3 minutes on full power, stopping the moment the pops slow to "
                 "one every few seconds; a bag is the easy way because the steam escapes. Salt it "
                 "while it is hot and leave the lid off the bowl so it stays crisp.")
    dry = ("Dry kernels pop without any oil: shake a single layer of them in a heavy lidded pan "
           "over medium heat, lifting the pan off the ring every few seconds so the bottom does "
           "not scorch, until the pops slow. Or use an air popper, which is the same thing with "
           "the stirring done for you.")
    if any(_same(word, way) for word in words
           for way in ("microwave", "microwaved", "microwaving", "microwaves", "bag", "bags")):
        return microwave + " " + pan if "hob" in words or "pan" in words else microwave
    if any(_same(word, way) for word in words
           for way in ("oil", "air", "popper", "diet", "healthy")):
        return dry
    return pan


def _popcorn_keep(memory, understood):
    words = [str(word).lower() for word in (understood.get("words") or [])]
    if any(_same(word, fault) for word in words
           for fault in ("chewy", "soggy", "squidgy", "tough", "rubbery")):
        return ("Chewy popcorn was either stale to start with or it did not get hot enough: use "
                "kernels under a year old, keep them in a sealed jar rather than the fridge, and "
                "give the pan a few more seconds after the pops slow to one every few seconds. "
                "Leave the lid off the bowl once it is out, because the steam it sits in is what "
                "turns the rest soft.")
    return ("Kernels keep for about a year in a sealed jar in a cool cupboard, and popped corn goes "
            "soft within a day or two, so an airtight tin is what keeps it crisp. Popcorn that "
            "comes out chewy was stale to start with or did not get hot enough: use kernels under "
            "a year old and give the pan a few more seconds after the pops slow.")


_STEWED_FRUIT = ("apple", "apples", "pear", "pears", "rhubarb", "plum", "plums",
                 "cherry", "cherries", "apricot", "apricots", "berry", "berries",
                 "fruit", "quince", "peach", "peaches")
_STEWED_WHY = (
    (("apple", "apples"), "apple", "a Bramley collapses to a fluff while a Cox or a Braeburn "
     "holds its shape, so use Bramleys for a sauce, a crumble or a compote"),
    (("pear", "pears"), "pear", "a Conference softens where a Comice is for eating raw, and a "
     "hard pear wants 10 more minutes"),
    (("rhubarb",), "rhubarb", "thin young stalks give way in 5 minutes and thick old ones want "
     "15, so pick the thin ones and add the sugar once they have softened"),
    (("plum", "plums"), "plum", "a ripe plum collapses in 5 minutes and a firm one holds, so "
     "halve them and taste at 5"),
    (("cherry", "cherries"), "cherry", "cherries want 5 to 8 minutes and go from firm to jam "
     "quickly, so take them off while they still hold"),
    (("apricot", "apricots", "peach", "peaches"), "apricot", "a ripe one collapses in 5 minutes "
     "and an underripe one stays firm whatever you do, so halve them and poach them gently"),
    (("berry", "berries"), "berry", "berries want only 2 or 3 minutes and a hard one was "
     "underripe to begin with"),
    (("quince",), "quince", "a quince stays hard for 40 minutes and then turns pink and soft all "
     "at once, so give it the time and taste it"),
)


def _stewed_fruit(words):
    named, why = "fruit", ("a firm one holds its shape where a ripe one collapses, so use the "
                           "ripe ones for a compote")
    for forms, name, reason in _STEWED_WHY:
        if any(_same(word, form) for word in words for form in forms):
            named, why = name, reason
            break
    return ("A stewed %s that stays hard was the fruit rather than the cooking: %s. Give it 10 "
            "more minutes with a splash of water and taste as it goes, because it goes from firm "
            "to pulp quickly once it starts." % (named, why))


def _tough(memory, understood):
    words = [str(word).lower() for word in (understood.get("words") or [])]
    if any(_same(word, "squid") for word in words):
        return ("Squid is either 2 minutes or 40: flash it in a very hot pan, or stew it slowly with "
                "tomatoes and wine for 40 minutes. Anything in between turns it to rubber.")
    if (any(_same(word, fruit) for word in words
            for fruit in _STEWED_FRUIT)
            and any(_same(word, way) for word in words
                    for way in ("stewed", "stew", "poached", "compote", "baked", "puree"))):
        return _stewed_fruit(words)
    if (any(_same(word, pot) for word in words
            for pot in ("stew", "stews", "casserole", "braise", "braised", "braising", "goulash",
                        "hotpot", "tagine", "ragu", "chilli", "chili"))
            and not any(_same(word, fruit) for word in words for fruit in _STEWED_FRUIT)):
        return ("A tough stew is an underdone one rather than an overcooked one: another 30 to 45 "
                "minutes at a bare simmer with the lid on, and top the liquid up if it is running "
                "low. A simmer that is really a boil tightens the meat instead of softening it, so "
                "keep it just trembling and test a piece with a fork - it is ready when it gives "
                "way without resistance.")
    if any(_same(word, meat) for word in words
           for meat in ("steak", "meat", "beef", "pork", "lamb", "chicken", "chop", "chops",
                        "turkey", "sausage", "sausages", "burger", "burgers", "roast", "gammon",
                        "duck", "ribs")):
        if _asks_why(words):
            return ("It went tough from cooking too fast or from not resting: the muscle fibres "
                    "contract and squeeze the juice out, and a cheap cut needs longer at a lower "
                    "heat to break down instead - 2 hours at 160C with liquid in the pan. This "
                    "piece is best sliced thinly across the grain and served with something wet.")
        return ("Slice it thinly across the grain and serve it with something wet; that rescues more "
                "tough meat than anything else. It went tough from cooking too fast or not resting, "
                "so next time go slower: a cheap cut wants 2 hours at 160C with liquid in the pan.")
    if any(_same(word, starch) for word in words
           for starch in ("pasta", "noodle", "noodles", "rice")):
        return ("Tough here is underdone rather than overcooked: give it 5 more minutes in boiling "
                "water and test it with the tip of a knife, and cut the pieces the same size so they "
                "finish together. A pan that never came back to the boil is the usual reason it is "
                "still hard in the middle when the outside is done.")
    if any(_same(word, bake) for word in words
           for bake in ("cake", "cakes", "sponge", "sponges", "muffin", "muffins", "cupcake",
                        "cupcakes", "scone", "scones", "brownies", "brownie", "bun", "buns",
                        "traybake", "traybakes", "loaf", "loaves")):
        thing, plural = _the_bake_named(words)
        return ("Tough " + thing + (" are" if plural else " is") if thing else "A tough bake is") + (
            " mixed too much or a little too long in the oven, or short of fat. Stir only until "
            "the flour disappears, fold rather than beat, and weigh the butter rather than "
            "eyeballing it, because a sponge wants as much fat as eggs by weight. One that is "
            "already tough is best eaten warm with something wet, or torn up for a trifle.")
    if any(_same(word, pastry) for word in words
           for pastry in ("pastry", "shortcrust", "shortcrust pastry", "pie crust",
                          "pie", "tart", "quiche", "crumble")):
        return ("Tough pastry is over-worked or too wet: keep the fat cold, rub it in with your "
                "fingertips only until it looks like fine breadcrumbs, add iced water a spoon at a "
                "time and bring it together fast. Shortcrust wants about half its weight in fat to "
                "flour, and 20 minutes in the fridge before it is rolled; roll it between two sheets "
                "of greaseproof so you never stretch it. Pastry that is already baked cannot be "
                "rescued, so serve it with something wet.")
    if any(_same(word, bread) for word in words
           for bread in ("bread", "loaf", "roll", "rolls", "baguette", "pitta", "naan", "bun",
                         "buns", "bagel", "bagels")):
        return ("Tough bread is usually over-kneaded or baked too slowly: knead until the dough "
                "springs back and stops tearing, prove it somewhere warm until it has doubled, and "
                "bake it hot (220C) for the first 10 minutes so it rises before the crust sets. "
                "Bread that has already gone leathery comes back in a hot oven for 5 minutes with a "
                "splash of water in the tin.")
    if any(_same(word, egg) for word in words for egg in ("egg", "eggs", "omelette", "scrambled")):
        return ("Rubbery eggs have been cooked too long, and in a microwave that happens in seconds: "
                "beat them, give them 30 seconds at a time on medium, stir hard between each go, "
                "and stop while they still look a little wet, because they carry on setting as "
                "they stand. The same rule in a pan - low heat, slow stirring, off the heat early.")
    return ("Rubbery is overcooked, or a batter that was beaten too much: pancakes and batters want "
            "a lumpy mix and a minute less in the pan. It's hard to rescue on the plate, so serve it "
            "with something wet and cook it less next time.")


_BAKE = ("cake", "cakes", "sponge", "bread", "loaf", "buns", "bun", "scones", "scone",
         "muffins", "muffin", "brownies", "brownie", "pancakes", "yorkshire pudding", "biscuits",
         "biscuit", "pastry", "dough", "batter", "pie")


def _salty(memory, understood):
    words = [str(word).lower() for word in ((understood or {}).get("words") or [])]
    if any(_same(word, bake) for word in words for bake in _BAKE):
        return ("Baking is the one place salt cannot be cooked out or bulked out: leave it and cut the "
                "salt from whatever goes with it, or add a little more sugar and fat to push it into "
                "the background. Next time weigh the salt with the measuring spoons rather than "
                "shaking it in, and remember salted butter is already about a quarter salt.")
    return ("Don't add water: bulk it out with more of what's already in it — potatoes, rice, tinned "
            "tomatoes, cream or unsalted stock — and finish with a squeeze of lemon. In a soup or "
            "stew, a peeled potato simmered in it for 15 minutes takes up some of the salt too.")


def _scramble(memory, understood):
    words = [str(word).lower() for word in (understood.get("words") or [])]
    asks_how = (understood.get("kind") == "question"
                or any(_same(word, "how") for word in words))
    if asks_how and not any(_same(word, fault) for word in words
                            for fault in ("watery", "wet", "sloppy", "rubbery", "rubber", "tough",
                                          "dry", "hard", "overcooked", "chewy", "curdled",
                                          "mushy")):
        return ("Beat 2 or 3 eggs with a pinch of salt, melt a knob of butter in a pan over a low "
                "heat, pour them in and stir slowly with a spatula, pushing the set egg in from the "
                "edges. Take them off while they still look a little wet, after 2 or 3 minutes, "
                "and stir in a little more butter off the heat.")
    if any(_same(word, wet) for word in words for wet in ("watery", "wet", "sloppy")):
        return ("Watery scrambled eggs have been cooked too long: the curds squeeze out their "
                "water as they tighten. Cook them low and slow, stirring, and take them off while "
                "they still look a little loose, then stop the heat with a knob of cold butter or "
                "a spoon of creme fraiche.")
    return ("Rubbery scrambled eggs come from too much heat: cook them low and slow, stirring, and "
            "take them off while they still look slightly wet, because they carry on setting. A "
            "knob of butter at the end stops them going dry.")


_EGG_DISH = ("omelette", "omelet", "omelettes", "omelets", "frittata", "frittatas", "quiche",
             "quiches", "fried egg", "fried eggs", "creme anglaise", "creme patissiere",
             "creme patisserie", "pastry cream", "custard sauce")
_EGG_FAULT = ("rubbery", "rubber", "tough", "leathery", "overcooked", "over cooked",
              "fell apart", "falls apart", "falling apart", "wouldnt fold", "wont fold",
              "split", "splits", "curdled", "grainy", "gritty", "watery", "weeping", "dense",
              "soggy", "lumpy", "chewy")
_EGG_PAN = ("omelette", "omelet", "omelettes", "omelets")
_EGG_FRITTATA = ("frittata", "frittatas")
_EGG_QUICHE = ("quiche", "quiches")
_EGG_FRIED = ("fried egg", "fried eggs")
_EGG_SAUCE = ("creme anglaise", "creme patissiere", "creme patisserie", "pastry cream",
              "custard sauce")


def _egg_fault(memory, understood):
    words = [str(word).lower() for word in ((understood or {}).get("words") or [])]
    if not words:
        return None
    said = " ".join(words)

    def named(names):
        return any(name in said for name in names)

    def fault(*names):
        return any(_same(word, name) for word in words
                   for name in names) or any(name in said for name in names)

    if named(_EGG_SAUCE) and fault("grainy", "gritty", "split", "splits", "curdled", "curdles",
                                  "lumpy", "scrambled"):
        return ("A grainy or split creme anglaise has curdled, because the eggs went above about "
                "82C. Take it off the heat at once, whisk in a splash of cold milk to stop it "
                "cooking, then strain it through a sieve and it comes back smooth. Next time cook "
                "it over a low heat, stirring all the time, and pull it off as soon as it coats "
                "the back of the spoon.")
    if named(_EGG_SAUCE):
        return None
    if named(_EGG_QUICHE):
        if fault("rubbery", "rubber", "tough", "dense", "overcooked", "over cooked"):
            return ("A rubbery quiche is a custard that stayed in too long: the filling is firm "
                    "at about 80C, so bake it at 180C for 30 to 35 minutes, until the middle "
                    "still has a slight wobble, and let it cool for 20 minutes, because it firms "
                    "as it stands. Two eggs to 200ml of double cream in a 20cm tin sets soft; "
                    "more egg than that sets like rubber.")
        return None
    if named(_EGG_FRIED):
        return ("Fried eggs go rubbery when the white sets hard before the yolk is warm: cook "
                "them on a medium heat with a lid on for 2 to 3 minutes, so the top sets in the "
                "steam, and take them out while the yolk still wobbles. On a high heat the white "
                "blisters and toughens long before the yolk is hot.")
    if named(_EGG_FRITTATA) or named(_EGG_PAN):
        if fault("fell apart", "falls apart", "falling apart", "wouldnt fold", "wont fold",
                 "broke", "tears", "tore"):
            return ("An omelette tears when the eggs are too thin for the pan, so use a 20cm pan "
                    "and no more than three eggs, let the base set for 45 seconds before you fold, "
                    "and fold it with a spatula in the pan instead of lifting it out. A frittata "
                    "is finished under the grill and never folded, which is the same dish without "
                    "the part that breaks.")
        if fault("soggy", "watery", "wet"):
            return ("An omelette or frittata that stays wet is a vegetable problem: mushrooms, "
                    "courgette, spinach and onion all give out water as they cook. Fry them first, "
                    "on their own, until their water has gone and they are starting to colour, and "
                    "let them cool a little before the eggs go in. A pinch of salt in the beaten "
                    "egg also helps it set.")
        if fault("rubbery", "rubber", "tough", "leathery", "overcooked", "over cooked",
                 "chewy"):
            return ("An omelette goes rubbery from the pan and the clock rather than the eggs: a "
                    "20cm pan on a medium heat, two beaten eggs with a pinch of salt, and pull the "
                    "set edges into the middle for 60 to 90 seconds, then fold and slide it out "
                    "while the top still looks a little wet. A small pan steams it instead of "
                    "setting it, and one more minute is enough to make it leathery.")
        return None
    return None



def _cookies(memory, understood):
    words = [str(word).lower() for word in (understood.get("words") or [])]
    said = " ".join(words)
    if any(phrase in said for phrase in ("didnt spread", "didn't spread", "did not spread",
                                        "not spread", "not spreading", "wont spread",
                                        "won't spread", "stayed in a ball", "stayed in balls",
                                        "too thick", "too small", "didnt flatten",
                                        "didn't flatten", "did not flatten", "stayed round")):
        return ("Cookies that stay in a ball have usually had too much flour or butter that was "
                "too cold: weigh the flour rather than scooping the cup, use soft butter, and "
                "press each ball down to about 1cm with the back of a spoon before it goes in. A "
                "tablespoon of milk or an extra yolk loosens a dry dough, and the oven wants to be "
                "properly hot, 180C (160C fan), so they set before they can spread.")
    return ("Cookies spread when the dough is warm or the butter is too soft: chill the dough 30 "
            "minutes and put it on a cool tray, and leave a good 5cm between them. Too much sugar "
            "or a greased tin makes them spread further, and a fan oven needs 20C less than the "
            "recipe.")


def _chocolate(memory, understood):
    words = [str(word).lower() for word in (understood.get("words") or [])]
    said = " ".join(words)
    told_apart = re.sub(r"\bwhite\s+(?=chocolate\b)", "", said).split()
    if any(_same(word, fault) for word in told_apart
           for fault in ("bloom", "white", "streak", "streaks", "grey", "gray")):
        return ("White streaks on chocolate are bloom, and it is harmless: either cocoa butter or "
                "sugar has come to the surface because the chocolate got warm and then cool again. "
                "It still tastes the same and it is fine to eat or to melt. To stop it happening, "
                "store it cool and steady, around 15 to 18C, and never in the fridge.")
    if any(phrase in said for phrase in ("healthy", "good for you", "bad for you",
                                        "better for you", "fattening", "sugar", "calorie",
                                        "calories", "diet")):
        return ("As a treat, chocolate is fine: dark with 70% cocoa or more has the least sugar, so "
                "it is the one to pick if you are watching it, and two squares is a normal "
                "portion. White chocolate is the sweetest of the three because it is cocoa butter, "
                "milk and sugar with no cocoa solids at all.")
    if any(phrase in said for phrase in ("real chocolate", "is it chocolate", "actually chocolate",
                                        "made of", "made from", "contain", "contains",
                                        "what is chocolate", "is white chocolate",
                                        "whats in chocolate", "what's in chocolate")):
        if "white" in words:
            return ("White chocolate is cocoa butter, milk powder and sugar, with no cocoa solids "
                    "at all, which is why it tastes of vanilla and milk rather than of chocolate. "
                    "It is still real chocolate by the labelling rules - at least 20% cocoa butter "
                    "in Europe - just a different thing from dark, and it is the sweetest of the "
                    "three.")
        return ("What most people mean by chocolate is dark: cocoa solids and cocoa butter with "
                "sugar, and the higher the percentage the less sugar there is. Milk chocolate "
                "adds milk powder and more sugar, and white chocolate is cocoa butter, milk and "
                "sugar with no cocoa solids at all.")
    if any(_same(word, "temper") for word in words):
        return ("To temper chocolate, melt two thirds of it in a bowl over barely simmering water "
                "to 45C (or 40C for white), take it off the heat and stir in the rest, chopped, "
                "until it drops to 27C, then warm it gently back to 31C for dark or 29C for milk "
                "and white. That sets it glossy and hard at room temperature. A thermometer earns "
                "its keep; without one, a clean spoon dipped in should set firm in 5 minutes.")
    if (any(_same(word, want) for word in words
            for want in ("dip", "dipped", "dipping", "strawberry", "strawberries"))
            and not any(_same(word, want) for word in words
                        for want in ("melt", "melting", "melted"))):
        return ("Melt it slowly, then dip: dry the fruit first so the chocolate grips, dip about "
                "two thirds of the way in, let the extra drip back into the bowl, and set them on "
                "baking paper in the fridge for 10 minutes to set hard. If the chocolate feels "
                "thin, stir in a handful more chopped chocolate off the heat.")
    if any(_same(word, fault) for word in words
           for fault in ("seize", "seized", "seizing", "grainy", "lumpy", "stiff")):
        return ("Chocolate seizes when even a drop of water gets in, and the fix is more water, "
                "not less: stir in a teaspoon of boiling water at a time, off the heat, until it "
                "goes smooth again. A tablespoon of warm cream does the same and leaves you with "
                "a ganache.")
    return ("Melt chocolate in a bowl over barely simmering water, with the bowl not touching the "
            "water, or in 20-second bursts in the microwave, stirring between them. Keep every "
            "spoon and bowl dry, because a drop of water makes it seize, and take it off while "
            "most of it is melted - the rest will go as you stir.")
_GRAIN_FOOD = ("fudge", "toffee", "caramel", "icing", "frosting", "buttercream", "fondant",
               "praline", "brittle", "tablet", "syrup", "candy", "custard")
_GRAIN_WORD = ("grainy", "gritty", "crystal", "crystals", "crystallised", "crystallized",
               "crystalised", "crystalized", "granular", "sandy", "crunchy", "grain")


def _grainy(memory, understood):
    words = [str(word).lower() for word in (understood.get("words") or [])]

    def has(*names):
        return any(_same(word, name) for word in words for name in names)

    if has("icing", "frosting", "buttercream", "glaze", "fondant", "drizzle"):
        return ("Grainy icing is undissolved sugar: sift the icing sugar first, then add the "
                "liquid a teaspoon at a time, and if it is already made, beat in a spoonful of "
                "warm milk or a few drops of lemon juice and it goes smooth. Cold liquid and "
                "coarse sugar are what leave the grain, so warm the milk slightly next time and "
                "give it a full minute of beating.")
    if has("fudge", "tablet", "praline", "brittle", "candy"):
        return ("Grainy fudge has sugar crystals in it, which happens when it is stirred while it "
                "boils or a crust of sugar from the pan gets back in. Warm it very gently with two "
                "tablespoons of milk and beat it hard until it is smooth again, or press it out "
                "flat and call it tablet. Next time stir only until the sugar dissolves, then "
                "wipe the pan sides down with a wet pastry brush and leave it to 116C.")
    if has("custard", "creme", "anglaise"):
        return ("Grainy custard has curdled: the eggs got too hot too fast. Take it off the heat "
                "at once, whisk in a splash of cold milk to stop it cooking, then strain it "
                "through a sieve into a jug and it comes back smooth. Next time cook it over a "
                "low heat, stirring all the time, and take it off at about 82C or as soon as it "
                "coats the back of the spoon.")
    if has("toffee", "caramel"):
        return ("Grainy caramel or toffee has crystallised: add a tablespoon of water and warm it "
                "very gently without stirring until the crystals melt, then let it cool slowly. "
                "It crystallises when the sugar is stirred once it is boiling, or when one "
                "crystal from the side of the pan gets back in, so stir only until the sugar has "
                "dissolved and keep the sides of the pan wiped clean.")
    return ("Sugar that sets grainy has crystallised, from stirring once it boils or a crystal "
            "from the pan getting back in. Warm it gently with a tablespoon of water until it "
            "melts back, and next time stir only until the sugar dissolves, wipe the pan sides "
            "with a wet pastry brush, and add a spoonful of golden syrup or a squeeze of lemon "
            "at the start.")



_SUGAR_MAKING = ("caramel", "caramels", "toffee", "praline", "brittle", "fudge", "candy")
_SUGAR_TROUBLE = ("crystallise", "crystallised", "crystallising", "crystallize", "crystallized",
                  "crystallizing", "crystalise", "crystalised", "crystalize", "crystalized",
                  "crystals", "crystal", "grainy", "grain", "crust", "crusty", "seize", "seized")


def _sugar_work(memory, understood):
    words = [str(word).lower() for word in (understood.get("words") or [])]

    def has(*names):
        return any(_same(word, name) for word in words for name in names)

    if has("bitter", "burnt", "burned", "burning", "smoky", "smells"):
        if _burnt_on_the_pan(" ".join(words)):
            return ""
        return ("A bitter caramel has gone past the colour: sugar keeps cooking after it leaves "
                "the heat, so it went from amber to dark before it came off. Start again and pull "
                "it at the colour of a copper penny, and have the cream ready to add off the heat "
                "so it stops at once. One that tastes of the pan is not worth saving.")
    if has("hard", "hardened", "hardens", "block", "solid", "lumps", "lumpy", "stuck",
           "soften", "softens", "softening"):
        return ("Sugar that has set hard has taken up damp and dried out again: put the bag in the "
                "microwave for 10 seconds at a time, or stand a slice of bread or a peeled apple in "
                "the jar overnight, and it breaks up. Keep it in an airtight jar away from the "
                "steam of the kettle, because it is the damp that sets it into a block.")
    if has(*_SUGAR_TROUBLE) and not has("dissolve", "dissolves", "dissolving", "dissolved", "melt",
                                        "melts", "melting", "melted"):
        return ("Sugar crystallises when it is stirred once it is boiling, or when one grain from "
                "the side of the pan drops back in. Melt it back with a tablespoon of water over a "
                "low heat without stirring, and next time stir only until the sugar has dissolved, "
                "wipe the pan sides down with a wet pastry brush, and add a squeeze of lemon or a "
                "spoonful of golden syrup at the start.")
    if (has("syrup", "coffee", "cocktail", "cocktails", "tea", "dissolve", "dissolves",
            "dissolving", "dissolved", "melt", "melts", "melting", "melted")
            or not has(*_SUGAR_MAKING)):
        return ("Sugar dissolves fastest in hot liquid: warm the water or milk first, stir until "
                "the liquid is clear rather than for a set time, and use about 200g of sugar to "
                "100ml of water for a syrup. Caster sugar goes in quicker than granulated and "
                "icing sugar dissolves almost at once. A spoonful of lemon juice or golden syrup "
                "stops a syrup crystallising as it cools.")
    if has("toffee", "toffees", "fudge", "praline", "brittle", "candy"):
        return ("Caramel is the base of all of them, then the temperature sets what you get: "
                "200g sugar in a dry heavy pan, swirled not stirred, to the colour of a copper "
                "penny. Toffee is that plus 60g butter and a splash of cream stirred in off the "
                "heat, cooked on to 150C (hard crack) and poured to set; fudge comes off at 116C "
                "(soft ball), then you beat it in the pan as it cools so it stays smooth instead "
                "of grainy. A sugar thermometer earns its keep here.")
    return ("Caramel is sugar cooked until it changes colour, and nothing else: 200g sugar in "
            "a dry heavy pan over a medium heat, not stirred but swirled, until it is the "
            "colour of a copper penny - then straight off the heat, because it keeps cooking. "
            "For a sauce, add a splash of warm cream off the heat, as it spits. A wet caramel "
            "is 200g sugar with 60ml water and a squeeze of lemon, boiled without stirring.")

def _soup(memory, understood):
    words = [str(word).lower() for word in (understood.get("words") or [])]
    if any(_same(word, want) for word in words
           for want in ("better", "flavour", "improve", "boring", "lifeless", "interesting")):
        return ("Add salt first, then a squeeze of lemon or a splash of vinegar: most dull soup is "
                "short of both, not of spice. After that something savoury - a stock cube, a spoon "
                "of miso, a parmesan rind or a knob of butter - and roast the vegetables next time "
                "rather than boiling them.")
    return ("Soften an onion and a carrot in butter with a pinch of salt, add whatever vegetables "
            "or pulses you have and enough stock to cover them, and simmer 20 minutes. Blend it "
            "smooth or leave it chunky, taste it, and finish with salt, pepper and a squeeze of "
            "lemon.")


def _flat(memory, understood):
    words = [str(word).lower() for word in (understood.get("words") or [])]

    def has(*wanted):
        return any(_same(word, want) for word in words for want in wanted)

    if has("pancake", "pancakes", "batter", "crepe", "crepes"):
        return ("Flat pancakes are usually old baking powder or a batter that was beaten too much: "
                "use a fresh tin, stir until it is just combined, and let the batter rest 10 "
                "minutes before it hits the pan. A properly hot pan matters too - the first one is "
                "always the test.")
    if has("yorkshire", "puddings"):
        return ("Yorkshire puddings want a smoking tin and cold batter: put a little oil in each "
                "hole, heat it in a 220C oven until it shimmers, pour the batter in and don't open "
                "the door for 20 minutes.")
    if has("scon", "scones"):
        return ("Flat scones come from handling: keep the butter cold, rub it in quickly, pat the "
                "dough out rather than rolling it hard, and cut straight down with a sharp cutter so "
                "the edges stay free to rise.")
    return ("Something that came out flat is short of rise, because the baking powder was past "
            "its date, the flour was beaten after it went in, or the oven was not up to heat. "
            "Check the baking powder is in date (about half a teaspoon to 100g of flour), stop "
            "beating once the flour is in, and let the oven come fully up to heat before the tin "
            "goes in.")


_FROM_FROZEN = ("from frozen", "cook it frozen", "cooked from frozen", "without defrosting",
                "without thawing", "no need to defrost", "skip the defrosting",
                "do i have to defrost", "have to defrost", "need to defrost")
_FROZEN_TIME = ("how long", "how many hours", "how many days", "how many minutes", "overnight",
                "thaw time", "how long does it take", "what temperature", "what temp")
_FROZEN_WHAT = ("what can i cook", "what can i make", "what can we cook", "what can we make",
                "what should i cook", "what should i make", "what to cook", "meal ideas",
                "what could i cook", "what could i make")
_FROZEN_ASK = ("can i", "could i", "may i", "is it", "should i", "do i", "how do i", "ok to",
               "okay to", "safe to", "fine to", "am i able", "any way to", "is there a way")
_FROZEN_CUTS = (("mince", "beef mince", "lamb mince", "pork mince"), "break it up as it loosens")
_FROZEN_WHOLE = (("sausage", "A sausage", True), ("sausages", "Sausages", False),
                 ("bacon", "Bacon", True), ("chops", "Chops", False), ("chop", "A chop", True),
                 ("steak", "A steak", True), ("steaks", "Steaks", False),
                 ("liver", "Liver", True), ("kidneys", "Kidneys", False))
_FROZEN_ONE = ("{} can go straight into the pan from frozen: cook it a few minutes longer than you "
               "would thawed, turning it so it colours on all sides, and check it is piping hot in "
               "the middle.")
_FROZEN_MANY = ("{} can go straight into the pan from frozen: cook them a few minutes longer than "
                "you would thawed, turning so they colour on all sides, and check they are piping "
                "hot in the middle.")


def _frozen_from_the_bag(understood):
    text = " ".join(str(understood.get("clean") or "").lower().split())
    if any(word in text for word in ("turkey", "joint", "whole bird", "roasting")):
        return False
    if not any(word in text for word in _FROM_FROZEN):
        return False
    if any(word in text for word in _FROZEN_WHAT):
        return False
    if any(word in text for word in _FROZEN_TIME):
        return False
    if any(word in text for word in _FROZEN_ASK):
        return True
    return any(word in text for word in ("from frozen", "cooked from frozen", "cook it frozen",
                                         "without defrosting", "without thawing",
                                         "no need to defrost", "skip the defrosting"))


_FROZEN_CUT_WORDS = tuple(_FROZEN_CUTS[0]) + tuple(word for word, _, _ in _FROZEN_WHOLE)


def _frozen_cook_reply(understood):
    text = " ".join(str(understood.get("clean") or "").lower().split())
    words = text.split()
    if not any(cut in words for cut in _FROZEN_CUT_WORDS):
        lean = understood.get("leans_on")
        if isinstance(lean, dict):
            subject = str(lean.get("subject") or "").lower().split()
            words = words + [word for word in subject if word in _FROZEN_CUT_WORDS]
    if any(cut in words for cut in _FROZEN_CUTS[0]):
        led = ("Mince can go straight into the pan from frozen: brown it over a high heat, "
               "break it up as it loosens and give it a few extra minutes before the sauce goes in.")
    else:
        said, one = next(((said, one) for word, said, one in _FROZEN_WHOLE if word in words),
                        ("", False))
        if said:
            led = (_FROZEN_ONE if one else _FROZEN_MANY).format(said)
        else:
            led = ("Usually yes for small cuts - mince, sausages, bacon, chops: they can go "
                   "straight into a hot pan or a sauce from frozen, a few minutes longer than "
                   "thawed and piping hot all the way through.")
    return led + (" A whole bird or a big joint is the exception: it has to thaw first, or the "
                  "outside overcooks while the middle stays raw. Do not refreeze it once it has "
                  "started to thaw.")


def _meat_defrost(memory, understood):
    text = " ".join(str(understood.get("clean") or "").lower().split())
    if any(word in text for word in _FROZEN_WHAT) and any(
            word in text for word in ("frozen", "freezer")):
        return None
    if _frozen_from_the_bag(understood):
        return _frozen_cook_reply(understood)
    small = ("mince", "sausage", "sausages", "chop", "chops", "steak", "steaks", "bacon",
             "liver", "kidney", "kidneys")
    if not any(word in text for word in small) and ("turkey" in text or "bird" in text):
        kilos, said = _bird_weight(understood) or (None, None)
        time = f"{_hours_words(24 * kilos / 2)}" if kilos else "two and a half days"
        return (f"A turkey wants {time} in the fridge. That is 24 hours for every 2kg: leave it in "
                "its wrapper in a tray on the bottom shelf and never on the worktop, and once it is "
                "thawed cook it within 2 days. A crown thaws in 24 hours.")
    if not any(word in text for word in small) and "joint" in text:
        kilos, said = _bird_weight(understood) or (None, None)
        hours = f"about {_hours_words(24 * kilos / 2)}" if kilos else "a day for every 2kg"
        return (f"Give it {hours} in the fridge. A {said or '2kg'} one goes in the night before: "
                "leave it in its wrapper in a tray on the bottom shelf, never on the worktop, and "
                "cook it within 2 days of thawing. A rolled or boned one is quicker than one on the "
                "bone.")
    if not any(word in text for word in small):
        return ("In the fridge, on a plate on the bottom shelf, never on the worktop or in warm "
                "water. A turkey or a big joint wants a day or two there; mince, sausages and "
                "chops thaw overnight, and the microwave's defrost setting is the shortcut if you "
                "are short of time - cook the meat straight away when you use it.")
    return ("In the fridge, on a plate on the bottom shelf: mince, sausages and chops thaw "
            "overnight. If you are short of time use the microwave's defrost setting and cook the "
            "meat straight away, and never thaw it on the worktop or in warm water.")


def _turkey(memory, understood):
    said = " ".join([str(word).lower() for word in (understood.get("words") or [])]
                    + [str(understood.get("text") or "").lower()])
    if "crown" not in said:
        kilos, weight_said = _bird_weight(understood) or (5.0, "5kg")
        return ("A whole turkey roasts at 180C (160C fan) for 20 minutes per kg plus 70 minutes: a "
                f"{weight_said} bird takes about {_in_words(20 * kilos + 70)}. Cook the stuffing in "
                "a separate tray, because a stuffed bird needs longer and the middle of the "
                "stuffing is the last thing to get hot. Check the thigh at the deepest point, not "
                "the breast, for 74C, and rest it 30 to 45 minutes under foil before carving.")
    return ("Roast a turkey crown at 180C (160C fan) for 20 minutes per 500g plus 20 minutes, until "
            "a thermometer in the thickest part reads 74C, then rest it 30 minutes under foil. Salt "
            "it the night before or push butter under the skin, and cover the top with foil if it "
            "browns too fast.")


def _cut_time(understood, per_kilo, extra, example):
    weight = _bird_weight(understood)
    if not weight:
        return example
    kilos, said = weight
    return "so a %s one is about %s." % (said, _in_words(kilos * per_kilo + extra))


def _turkey_cut(memory, understood):
    said = " ".join([str(word).lower() for word in (understood.get("words") or [])]
                    + [str(understood.get("text") or "").lower()])

    def has(*words):
        return any(word in said for word in words)

    done = "Take it to 74C in the thickest part and rest it 10 minutes under foil."
    dark = ("Take the thickest part to 80C, where dark meat goes tender rather than tight, and "
            "rest it 10 minutes under foil.")
    if has("spatchcock"):
        return ("A spatchcocked bird is flat, so it roasts fast and even: 200C (180C fan) at 20 "
                "minutes per kg, "
                + _cut_time(understood, 20, 0, "so a 4kg one is about 1 hour 20 minutes.")
                + " " + done)
    if has("wing", "wings"):
        return ("Turkey wings roast at 200C (180C fan) in 25 to 30 minutes, turned once, and they "
                "are done at 74C in the thickest part, so rest them 5 minutes under foil.")
    if has("drumstick", "drumsticks"):
        return ("Turkey drumsticks take 35 to 40 minutes at 200C (180C fan), turned once so the "
                "skin browns all over. " + dark)
    if has("leg", "legs"):
        return ("Turkey legs take 45 to 50 minutes at 190C (170C fan), skin side up, turned once. "
                + dark)
    if has("thigh", "thighs"):
        return ("Boneless turkey thighs take 40 to 45 minutes at 190C (170C fan); bone-in ones "
                "want 10 minutes more. " + dark)
    if has("fillet", "fillets", "steak", "steaks", "scallop", "scallops"):
        return ("Turkey fillets, steaks and escalopes are thin and quick: 20 to 25 minutes at "
                "190C (170C fan), or 8 to 10 minutes in a hot pan. They are done at 74C, so "
                "check one and rest them 5 minutes under foil.")
    boneless = has("boneless", "rolled", "butterflied", "flat")
    if boneless:
        return ("A boneless, rolled turkey breast wants 30 minutes per 500g at 190C (170C fan), "
                + _cut_time(understood, 60, 0, "so a 1.5kg one takes about 1 hour 30 minutes.")
                + " " + done)
    return ("A bone-in turkey breast takes 20 minutes per 500g plus 20 at 190C (170C fan), "
            + _cut_time(understood, 40, 20, "so a 2kg one is about 1 hour 40 minutes.")
            + " " + done)


def _hummus(memory, understood):
    said = " ".join([str(word).lower() for word in (understood.get("words") or [])]
                    + [str(understood.get("text") or "").lower()])
    no_tahini = ("no tahini" in said or "without tahini" in said or "tahini free" in said
                 or "tahini" in said and any(phrase in said for phrase in (
                     "dont have", "don't have", "ran out", "out of", "none", "substitute",
                     "instead of", "replace")))
    if no_tahini:
        return ("Without tahini, blitz the drained tin of chickpeas with the juice of a lemon, a "
                "small garlic clove, a good pinch of salt and 2 tablespoons of olive oil, then "
                "loosen it with iced water a spoon at a time. A spoon of yogurt or a second squeeze "
                "of lemon stands in for the richness the tahini would give.")
    return ("Blitz a drained tin of chickpeas with 2 tablespoons of tahini, the juice of a lemon, a "
            "small garlic clove and half a teaspoon of salt, then loosen it with iced water a spoon "
            "at a time - that is what makes it fluffy. A pinch of bicarbonate of soda in the pan "
            "softens the skins if you boil your own chickpeas.")


JOINT_BEEF = ("Beef or lamb: 20 minutes at 220C (200C fan) to brown it, then 190C (170C fan) for "
              "15 minutes a 500g for rare, 20 for medium and 25 for well done. The reliable check "
              "is a meat thermometer in the thickest part - 52C rare, 60C medium, 70C well done - "
              "and rest it 20 minutes under foil before carving.")
JOINT_PORK = ("Pork wants 30 minutes a 500g at 180C (160C fan), cooked right through with no pink "
              "in the middle, and crackling needs the oven at 220C (200C fan) for the first 25 "
              "minutes. A meat thermometer in the thickest part should read 70C, then rest the "
              "joint 20 minutes under foil before carving.")
GOING_OFF_ASK = ("go off", "goes off", "going off", "gone off", "went off", "shelf life",
                 "use by", "freezer", "fridge", "leftover", "leftovers")
KEEPING_VERB = ("keep", "keeps", "keeping", "kept", "last", "lasts", "freeze", "freezes")
IN_THE_OVEN = ("oven", "roast", "roasting", "roasted", "cook", "cooks", "cooking", "cooked",
               "temperature", "gas mark", "how long do i", "how long should i")


def _roast_joint(memory, understood):
    line = " ".join(str((understood or {}).get("text") or "").lower().split())
    if any(phrase in line for phrase in GOING_OFF_ASK):
        return None
    if (any(phrase in line for phrase in KEEPING_VERB)
            and not any(word in line for word in IN_THE_OVEN)):
        return None
    words = [str(word).lower() for word in (understood.get("words") or [])]
    pork = ("pork", "pork joint", "leg of pork", "shoulder of pork", "loin of pork",
            "belly pork", "ham", "gammon")
    if any(_same(word, wanted) for word in words for wanted in ("pork", "gammon", "ham")):
        return JOINT_PORK
    if any(_same(word, wanted) for word in words for wanted in ("beef", "lamb", "mutton")):
        return JOINT_BEEF
    return JOINT_BEEF + " " + JOINT_PORK


KEEPING_SENSE = ("freeze", "freezes", "freezer", "freezing", "frozen", "defrost", "defrosted",
                 "fridge", "refrigerate", "refrigerated", "reheat", "reheated", "reheating",
                 "refreeze", "keep", "keeps", "keeping", "kept", "last", "lasts", "storage",
                 "store", "stored", "storing", "leftover", "leftovers")


_MINCE_GRAIN_DISH = ("bolognese", "bolognaise", "bol", "ragu", "ragout", "mince", "minced",
                     "chilli", "chili", "con carne", "lasagne", "lasagna",
                     "cottage pie", "shepherds pie", "shepherd's pie", "keema", "meat sauce",
                     "spag bol", "spaghetti bolognese", "taco", "tacos", "taco meat")
_MINCE_GRAIN_WORD = ("grainy", "gritty", "granular", "pellets", "grains")
_MINCE_PIE_PHRASE = re.compile(r"\bmince ?pies?\b")
_BOLOGNESE_WORDS = ("bolognese", "bolognaise", "spag bol", "spaghetti bolognese", "bol")


def _mince_grainy(memory, understood):
    words = [str(word).lower() for word in (understood.get("words") or [])]
    if any(_same(word, sense) for word in words for sense in KEEPING_SENSE):
        return None
    if _MINCE_PIE_PHRASE.search(" ".join(words)):
        return None
    if (any(_same(word, name) for word in words for name in _BOLOGNESE_WORDS)
            and not any(_same(word, "sauce") for word in words)):
        return None
    return ("A grainy sauce is usually the mince: it went into a pan that was not hot enough, so "
            "it boiled in its own juice instead of browning. Heat a heavy pan until a drop of "
            "water sizzles, then brown the mince in two batches. Leave it alone for 2 to 3 "
            "minutes at a time so it colours before the liquid goes in. For the pot you have, "
            "give it a slow half hour with the lid on, which softens the grains, and stir in a "
            "spoon of butter at the end.")


def _mince(memory, understood):
    words = [str(word).lower() for word in (understood.get("words") or [])]
    if any(_same(word, sense) for word in words for sense in KEEPING_SENSE):
        return None
    if any(_same(word, tough) for word in words
           for tough in ("tough", "rubbery", "chewy", "dry")):
        return ("Minced meat goes tough and grainy when it is cooked too long or boiled in its own "
                "juice: brown it fast in a hot pan in batches, then add liquid only once it has "
                "coloured. A pinch of bicarb (half a teaspoon per 500g) keeps it soft in a long "
                "bolognese.")
    return ("Brown mince in batches over a high heat and don't stir it much: it should sizzle and "
            "colour, not steam. Pale, grey mince is mince that was crowded in the pan.")


VAGUE = frozenset({"vegetables", "veg"})
_VAGUE_KEYS = frozenset({"vegetables", "vegetable", "veg"})


MEAT = frozenset("meat chicken beef pork lamb mince bacon sausage sausages ham turkey prawn "
                 "prawns".split())
FISH = frozenset("fish salmon cod tuna".split())
DAIRY = frozenset("dairy milk cheese butter cream yoghurt yogurt".split())

CHEESES = frozenset("feta halloumi parmesan mozzarella cheddar gruyere stilton brie camembert "
                    "ricotta paneer pecorino gouda edam wensleydale".split())
EGGS = frozenset("egg eggs".split())
NUTS = frozenset("nut nuts peanut peanuts".split())
GLUTEN = frozenset("gluten wheat pasta spaghetti bread toast flour couscous noodles barley rye "
                   "bulgur semolina cracker crackers cake biscuit biscuits pastry pitta".split())
SHELLFISH = frozenset("shellfish prawn prawns crab crabs lobster mussels oysters squid clams "
                      "scallops".split())
FAMILIES = {"meat": MEAT, "fish": FISH, "dairy": DAIRY, "egg": EGGS, "nut": NUTS,
            "gluten": GLUTEN, "shellfish": SHELLFISH}
NO_MEAT_DIET = MEAT | FISH

CONDITION_BANS = {"coeliac": GLUTEN, "celiac": GLUTEN, "gluten intolerant": GLUTEN,
                  "lactose intolerant": DAIRY}
NOT_THIS = re.compile(r"(?:\bnot|\bnon|\bnever|\bno longer|\bn't|\baint|\bain't)\s+"
                      r"(?:really\s+|actually\s+|even\s+)?(?:a\s+|an\s+|any\s+|\bat all\s+)?$")

FOOD = (r"(meat|chicken|beef|pork|lamb|mince|bacon|sausage|sausages|ham|turkey|fish|salmon|"
        r"cod|tuna|prawn|prawns|shellfish|crab|lobster|mussels|oysters|squid|clams|"
        r"dairy|milk|cheese|butter|cream|yoghurt|yogurt|egg|eggs|"
        r"nut|nuts|peanut|peanuts|gluten)")
AVOIDED = re.compile(
    r"\b(?:no|without)\s+(?:(?:any|more|the|any more)\s+)?" + FOOD + r"\b"
    r"|\b(?:dont|don't|do not|doesnt|doesn't|does not|didnt|didn't|did not|cant|can't|"
    r"cannot|wont|won't|will not|wouldnt|wouldn't|refuse|refuses|refused|never)\s+"
    r"(?:eat|eating|have|use|using|cook with|want|touch|order)\s+(?:any\s+)?"
    r"(?:really\s+|usually\s+)?" + FOOD + r"\b"
    r"|\b(?:allergic|allergy|intolerant|intolerance)\s+to\s+" + FOOD + r"\b"
    r"|\b(?:hate|hates|avoid|avoiding|skip|skipping|off|cutting out|cut out)\s+"
    r"(?:the\s+|all\s+)?" + FOOD + r"\b"
    r"|\bnot\s+(?:a fan of|keen on|fussed about)\s+" + FOOD + r"\b"
    r"|\b(?:havent|haven't|hasnt|hasn't|hadnt|hadn't)\s+(?:got|any)\s+(?:any\s+)?" + FOOD
    + r"\b"
    r"|\b(?:there\s+is\s+no|there's\s+no|theres\s+no|got\s+no|we\s+have\s+no|i\s+have\s+no)\s+"
    + FOOD + r"\b")
FREEFROM = re.compile(
    r"\b(meat|dairy|milk|cheese|gluten|wheat|nut|nuts|peanut|peanuts|egg|eggs)\s+free\b")
TROUBLE = re.compile(
    r"\b(nut|nuts|peanut|peanuts|dairy|milk|lactose|egg|eggs)\s+"
    r"(?:allergy|allergies|intolerance|intolerant)\b")


def _said_so_far(understood, memory):
    line = line_as_read(understood)
    earlier = []
    turns = memory.get("turns")
    if isinstance(turns, list):
        earlier = [str(turn.get("user") or "") for turn in turns[-4:] if isinstance(turn, dict)]
    return " ".join(earlier + [line])

_PEOPLE_AFTER = r"(?:people|persons?|of us|of you|guests|adults|heads|folk|for dinner|for lunch)"
_COUNT_WORD_SHAPES = "one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve"
_COUNT_VALUE = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
                "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12}


MEATLESS_ROAST = ("nut roast", "nutroast", "nut wellington", "nut loaf", "lentil roast",
                  "lentil loaf", "bean roast", "chickpea roast", "vegetable roast",
                  "vegetable wellington", "veg roast", "veggie roast", "tofu roast",
                  "tofu wellington", "seitan roast", "halloumi roast", "mushroom wellington",
                  "mushroom roast", "cauliflower roast", "beetroot roast", "vegan roast",
                  "vegetarian roast")


def _head_count(text):
    text = str(text or "").lower()
    when = (r"(?:on\s+\w+day|tonight|tomorrow|this weekend|next week|at the weekend|"
            r"this christmas|for christmas)")
    shapes = (rf"\bfor\s+(\d{{1,2}})\s*{_PEOPLE_AFTER}", rf"\bfor\s+({_COUNT_WORD_SHAPES})\s*{_PEOPLE_AFTER}",
              rf"\b(\d{{1,2}})\s*{_PEOPLE_AFTER}", rf"\b({_COUNT_WORD_SHAPES})\s*{_PEOPLE_AFTER}",
              rf"\bfor\s+(\d{{1,2}})\s*{when}", rf"\bfor\s+({_COUNT_WORD_SHAPES})\s*{when}",
              rf"\bfor\s+(\d{{1,2}})\s*(?=[,.!?]|$)", rf"\bfor\s+({_COUNT_WORD_SHAPES})\s*(?=[,.!?]|$)",
              rf"\bwe(?:'re| are)\s+(\d{{1,2}})\b", rf"\bwe(?:'re| are)\s+({_COUNT_WORD_SHAPES})\b")
    for shape in shapes:
        found = re.search(shape, text)
        if not found:
            continue
        value = found.group(1)
        number = int(value) if value.isdigit() else _COUNT_VALUE.get(value)
        if number and 2 <= number <= 20:
            return number
    return None


def _roast_shopping(memory, understood):
    text = str(understood.get("clean") or understood.get("text") or "").lower()
    people = _head_count(text)
    trimmings = ("potatoes, carrots, parsnips or swede, and something green like cabbage or "
                 "sprouts, plus oil, and stock and flour for the gravy")
    if "turkey" in text or "christmas dinner" in text or "xmas dinner" in text:
        per, bird, timing = BIRD_GRAMS, "turkey", "20 minutes per 500g plus 90"
        if people:
            body = (f"About {people * per / 1000:g}kg of turkey for {people}, at {per}g a person "
                    f"on the bone")
        else:
            body = ("Most people do turkey: about 500g a person on the bone, so a 4kg bird feeds "
                    "eight")
    elif "chicken" in text:
        per, bird, timing = BIRD_GRAMS, "chicken", "20 minutes per 500g plus 20"
        if people:
            body = (f"About {people * per / 1000:g}kg of chicken for {people}, at {per}g a person "
                    f"on the bone")
        else:
            body = (f"About {per}g of chicken a person on the bone, so a 3kg bird feeds six and a "
                    "1.5kg one feeds three")
    else:
        per, bird = 250, ""
        timing = "20 minutes per 500g plus 20"
        if people:
            body = (f"About {people * per / 1000:g}kg of raw joint for {people}, which is 250g a "
                    f"person")
        else:
            body = "For a roast: about 250g of raw joint a person, so 1.5kg feeds six"
    text_out = (f"{body}. Then {trimmings}. For timing, work on {timing} at 200C (180C fan), and "
                "rest it 15 minutes before carving.")
    if not bird:
        text_out += (" Add flour, eggs and milk for Yorkshire puddings, and mint or apple sauce if "
                     "it is lamb or pork.")
    return text_out


_DIET_ASKED = re.compile(
    r"\b(?:is|are|was|were|does|do|isnt|isn't|arent|aren't)\s+"
    r"((?:[a-z']+\s+){0,3}?)(?:vegetarian|vegan|veggie|vego)\b", re.I)
_DIET_ASK_NOT_A_FOOD = frozenset(
    "there anything something any this that it these those he she they him her them my your our "
    "their his its ok okay fine alright safe suitable good bad healthy fine too also still".split())


def _ask_about_the_food(text, at):
    for match in _DIET_ASKED.finditer(text[:at]):
        if match.end() <= at and not (_DIET_ASK_NOT_A_FOOD & set(match.group(1).split())):
            return True
    return False


def _excluded(text):
    text = str(text or "").lower().replace("\u2019", "'").replace("-", " ")
    events = []

    def note(position, families, positive=True):
        events.append((position, families, positive))

    for match in re.finditer(r"\b(?:vegetarian|veggie|vego)\b", text):
        if _ask_about_the_food(text, match.start()):
            continue
        note(match.start(), NO_MEAT_DIET, not _denied_at(text, match.start()))
    for match in re.finditer(r"\b(?:vegan|plant based|plantbased)\b", text):
        if _ask_about_the_food(text, match.start()):
            continue
        note(match.start(), NO_MEAT_DIET | DAIRY | EGGS, not _denied_at(text, match.start()))
    for pattern in (AVOIDED, FREEFROM, TROUBLE):
        for match in pattern.finditer(text):
            word = next((part for part in match.groups() if part), "")
            if not word:
                continue
            families = _families_of(word)
            denied = _denied_at(text, match.start())
            note(match.start(), families, not denied)
            note(match.start(), _foods_in_list(_list_words(text[match.end():match.end() + 80])),
                 not denied)
            if pattern is FREEFROM:
                note(match.start(),
                     _foods_in_list(_list_words(text[max(0, match.start() - 80):match.start()],
                                              backwards=True)), not denied)
    for condition, foods in CONDITION_BANS.items():
        for match in re.finditer(r"\b" + condition.replace(" ", r"\s+") + r"\b", text):
            note(match.start(), foods, not _denied_at(text, match.start()))
    state = {}
    for _position, families, positive in sorted(events, key=lambda event: event[0]):
        for word in families:
            state[word] = positive
    banned = {word for word, on in state.items() if on}
    if "cheese" in banned or DAIRY & banned:
        banned.update(CHEESES)
    return banned


_LACTOSE_WORDS = ("lactose", "milk sugar", "lactase")
_NOT_LACTOSE_WORDS = ("vegan", "dairy free", "dairy-free", "no dairy", "allergic", "allergy",
                      "anaphyla", "milk protein", "cut out dairy", "give up dairy", "avoid dairy")


def _a_lactose_intolerance(said):
    if not any(word in said for word in _LACTOSE_WORDS):
        return False
    plain = said.replace("\u2019", "'")
    return not any(word in plain for word in _NOT_LACTOSE_WORDS)


def _record_says_lactose(known):
    if not isinstance(known, dict):
        return False
    said = []
    for key in ("allergies", "diet", "diets", "condition", "conditions"):
        value = known.get(key)
        if isinstance(value, str):
            said.append(value)
        elif isinstance(value, (list, tuple, set)):
            said.extend(str(one) for one in value)
    return _a_lactose_intolerance(" ".join(said).lower().replace("-", " "))


def _their_diet_is_a_lactose_intolerance(memory):
    if not isinstance(memory, dict):
        return False
    known = None
    try:
        import bot.modules.memory_store as _store
        known = _store.user(memory) or {}
    except Exception:
        known = memory.get("user") if isinstance(memory.get("user"), dict) else {}
    return _record_says_lactose(known)


LIST_JOINERS = frozenset(("and", "or", "plus", "with", "also", "as", "well", "&", "+", ","))
LIST_FOODS = frozenset(FAMILIES) | EGGS | NUTS | GLUTEN | DAIRY | SHELLFISH | FISH | MEAT \
    | CHEESES | frozenset(("lactose",))


def _families_of(word):
    if word == "lactose":
        return DAIRY
    if word == "wheat":
        return GLUTEN
    return FAMILIES.get(word, {word})


def _foods_in_list(words):
    found = set()
    for word in words:
        word = word.strip(".,!?;:'")
        if not word:
            continue
        if word in LIST_JOINERS:
            continue
        if word not in LIST_FOODS:
            break
        found |= _families_of(word)
    return found


def _list_words(text, backwards=False):
    if backwards:
        return list(reversed(re.findall(r"[a-z']+|[&+,]", str(text or "").lower())))
    return re.findall(r"[a-z']+|[&+,]", str(text or "").lower())


def _denied_at(text, start):
    return bool(NOT_THIS.search(text[max(0, start - 30):start]))


EAT_ASK = re.compile(
    r"\b(?:can|could|may|should|shall)\s+i\s+(?:eat|have|drink|order|try)\s+(?P<a>[\w ']+)"
    r"|\b(?:is|are)\s+(?P<b>[\w ']+?)\s+(?:ok|okay|fine|alright|safe|allowed)\s+"
    r"(?:for\s+me|for\s+us)\b"
    r"|\bam\s+i\s+(?:ok|okay|fine|alright|safe|allowed)\s+(?:to\s+(?:eat|have|drink)\s+)?"
    r"(?P<c>[\w ']+)"
    r"|\b(?:is|would)\s+(?P<d>[\w ']+?)\s+(?:be\s+)?(?:bad|wrong|a\s+problem)\s+for\s+me\b",
    re.I)

FANCY_ASK = re.compile(
    r"\b(?:i\s+(?:fancy|fancied|fancying|crave|craved|craving|feel like|quite fancy|"
    r"really fancy|was thinking (?:of|about)|thought (?:i'd|i would|of having|about having)|"
    r"was going to (?:have|make|get)|was planning (?:to have|to make|on))|"
    r"i(?:'m| am)\s+(?:thinking (?:of|about)|craving|feeling like)|"
    r"i(?:'d| would)\s+(?:go for|have|make))\s+", re.I)

EAT_ASK_THEM = re.compile(
    r"\b(?:can|could|may|should|shall)\s+(?:he|she|they|him|her|them|it"
    r"|(?:my|our|the)\s+[a-z']+)\s+(?:eat|have|drink|order|try)\s+(?P<a>[\w ']+)"
    r"|\b(?:is|are)\s+(?P<b>[\w ']+?)\s+(?:ok|okay|fine|alright|safe|allowed)\s+for\s+"
    r"(?:him|her|them|(?:my|our|the)\s+[a-z']+)\b"
    r"|\b(?:is|would)\s+(?P<d>[\w ']+?)\s+(?:be\s+)?(?:bad|wrong|a\s+problem)\s+for\s+"
    r"(?:him|her|them|(?:my|our)\s+[a-z']+)\b",
    re.I)

MADE_OF = {}
for _names, _families in (
        (("peanut", "peanuts", "satay", "pesto", "marzipan", "baklava", "praline", "nutella", "muesli", "granola",
          "nut roast", "peanut butter", "almond", "almonds", "cashew", "cashews", "walnut",
          "walnuts", "hazelnut", "hazelnuts", "pecan", "pecans", "pistachio", "pistachios"),
         (NUTS,)),
        (("pasta", "spaghetti", "bread", "toast", "noodles", "couscous", "pastry", "cake",
          "biscuit", "biscuits", "cracker", "crackers", "pitta", "flour", "crumpet", "bagel",
          "wrap", "wraps", "barley", "rye", "semolina", "scone", "scones", "pizza", "sandwich",
          "soy sauce", "soya sauce"),
         (GLUTEN,)),
        (("cake", "cakes", "quiche", "quiches"), (GLUTEN, DAIRY, EGGS)),
        (("cheese", "butter", "cream", "milk", "yoghurt", "yogurt", "ice cream", "custard",
          "paneer", "halloumi", "mozzarella"), (DAIRY,)),
        (("oat milk", "soy milk", "soya milk", "rice milk", "coconut milk", "hemp milk",
          "pea milk", "plant milk", "oat drink", "soya drink"), ()),
        (("almond milk", "cashew milk", "hazelnut milk"), (NUTS,)),
        (("croissant",), (GLUTEN, DAIRY)),
        (("chicken", "beef", "steak", "pork", "lamb", "bacon", "ham", "sausage", "sausages",
          "turkey", "mince", "gelatine", "lard"), (MEAT,)),
        (("fish", "salmon", "tuna", "cod"), (FISH,)),
        (("prawn", "prawns", "crab", "crabs", "lobster", "mussels", "oysters", "squid", "clams",
          "scallops", "shellfish"), (MEAT, SHELLFISH)),
        (("egg", "eggs", "mayonnaise", "mayo", "meringue", "omelette"), (EGGS,)),
        (("rice", "potato", "potatoes", "chips", "lentils", "chickpeas", "beans", "quinoa",
          "corn", "tofu", "fruit", "vegetables", "veg", "salad", "broccoli", "carrot",
          "buckwheat", "cornflour", "corn flour", "rice flour", "gram flour", "tamari",
          "baking powder", "bicarbonate of soda", "bicarb", "cream of tartar", "yeast",
          "baking soda",
          "carrots", "spinach", "peas", "banana", "bananas", "apple", "apples", "oranges",
          "oats", "porridge", "honey", "fig", "figs", "olive oil", "oil", "salt", "sugar", "tinned tomatoes",
          "tomato", "tomatoes", "onion", "onions", "garlic", "courgette", "courgettes",
          "sweet potato", "sweet potatoes", "squash", "mushrooms"), ()),
):
    for _name in _names:
        MADE_OF[_name] = frozenset().union(*_families)

FAMILY_SAY = {
    id(NUTS): ("is made with nuts", "sunflower seeds or a spoon of yoghurt give the same crunch"),
    id(GLUTEN): ("is made with wheat flour", "rice, potatoes or a corn pasta do the same job"),
    id(DAIRY): ("is made with milk", "olive oil or a dairy-free spread does the same job"),
    id(EGGS): ("is made with egg", "a spoon of yoghurt where a recipe asks for one does the same"),
    id(MEAT): ("is meat", "chickpeas, lentils or tofu fill the same gap"),
    id(FISH): ("is fish", "chickpeas, lentils or tofu fill the same gap"),
    id(SHELLFISH): ("is shellfish", "chickpeas, lentils or tofu fill the same gap"),
}
SELF_SAY = {id(NUTS): "that is nuts", id(DAIRY): "that is dairy", id(EGGS): "that is egg",
            id(MEAT): "that is meat", id(FISH): "that is fish", id(SHELLFISH): "that is shellfish"}
FISH_SPLIT = ("Fish is the one people mean differently - if you do not eat it either, chickpeas, "
              "lentils or tofu fill the same gap.")

EAT_ASK_BARE = re.compile(
    r"\b(?:is|are|was|were)\s+(?P<e>[\w ']+?)\s+(?:ok|okay|fine|alright|safe|allowed)"
    r"\s*[?.!,]*$", re.I)

EAT_ASK_IF = re.compile(
    r"\b(?:is|are|was|were)\s+(?P<f>[\w ']+?)\s+(?:ok|okay|fine|alright|safe|allowed)\s+"
    r"(?:if|since|because|as|when|now that)\b", re.I)

EAT_ANY = re.compile(r"\bwhat\s+(?:can|could|should)\s+i\s+(?:eat|have)\b"
                     r"|\bwhat\s+(?:food|foods)\s+can\s+i\s+(?:eat|have)\b", re.I)
EAT_ANY_WORDS = frozenset("what can could should shall i eat have to now then instead please "
                          "today tonight for a also still tonight really actually at the moment "
                          "me us we just more".split())

MAY_HAVE = {}
for _name in ("cake", "cakes", "icing", "biscuits", "biscuit", "cookies", "chocolate", "dessert",
              "desserts", "ice cream", "muesli", "cereal", "granola", "flapjack", "brownie",
              "brownies", "pie", "pastry", "curry", "curries", "salad", "sandwich", "sandwiches",
              "bread", "sauce", "sauces"):
    MAY_HAVE[_name] = NUTS

BAN_SAY = ((NUTS, "nuts"), (GLUTEN, "gluten"), (DAIRY, "dairy"), (EGGS, "egg"), (MEAT, "meat"),
           (FISH, "fish"), (SHELLFISH, "shellfish"))
ANY_FAMILY = (NUTS, GLUTEN, DAIRY, EGGS, MEAT, FISH, SHELLFISH)


def _food_named(text):
    words = re.findall(r"[a-z']+", str(text or "").lower())
    for size in (2, 1):
        for start in range(len(words) - size + 1):
            phrase = " ".join(words[start:start + size])
            if phrase in MADE_OF:
                return phrase
    return None


def _foods_named(text):
    words = re.findall(r"[a-z']+", str(text or "").lower())
    found, taken = [], set()
    for size in (2, 1):
        for start in range(len(words) - size + 1):
            if any(at in taken for at in range(start, start + size)):
                continue
            phrase = " ".join(words[start:start + size])
            if phrase in MADE_OF:
                found.append(phrase)
                taken.update(range(start, start + size))
    return found


SINGULAR_IN_S = frozenset("couscous hummus muesli asparagus fish veg molasses".split())


def _is_plural(food):
    word = food.split()[-1]
    if word in SINGULAR_IN_S or word.endswith("ss"):
        return False
    return word.endswith("s")


def _named_as(text, food):
    text = str(text or "").lower()
    for match in re.finditer(r"\b" + r"\s+".join(re.escape(part) for part in food.split()) + r"\b",
                             text):
        after = re.match(r"[\s-]+([a-z']+)", text[match.end():])
        if after and after.group(1) in MADE_OF:
            continue
        before = text[:match.start()].rstrip()
        free = re.search(r"([a-z]+)\s+free$", before)
        qualifier = ""
        if free and free.group(1) in FREE_OF:
            qualifier = free.group(1) + " free "
            before = before[:free.start()].rstrip()
        article = re.search(r"([a-z']+)$", before)
        if article and article.group(1) in ("a", "an", "the"):
            return article.group(1) + " " + qualifier + food
        return qualifier + food
    return food


def _bans_for(understood, memory):
    banned = _bans_from_store(memory) | _excluded(_mine_only(_said_so_far(understood, memory)))
    line = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    if any(word in line for word in _NOT_LACTOSE_WORDS):
        pass
    elif _a_lactose_intolerance(line) or _their_diet_is_a_lactose_intolerance(memory):
        banned = set(banned) | {"lactose"}
    return banned


THIRD_PERSON = re.compile(
    r"^\s*(?:my\s+(?!own\b)[a-z']+|the\s+(?:baby|kid|kids|child|children|little one|dog|cat)|"
    r"he|she|they|his|her|their|hubby|other half|partner's)\b", re.I)


def _mine_only(text):
    parts = [part.strip() for part in re.split(r"(?<=[.!?;])\s+|\s*,\s*|\s+and\s+|\s+but\s+",
                                               str(text or "")) if part.strip()]
    return " ".join(part for part in parts if not THIRD_PERSON.match(part))


def _bans_from_store(memory):
    user = memory.get("user") if isinstance(memory, dict) else None
    if not isinstance(user, dict):
        return set()
    return _bans_of(user)


def _bans_of(facts):
    banned = set()
    if not isinstance(facts, dict):
        return banned
    for item in facts.get("allergies") or ():
        word = str(item).lower()
        banned.update(FAMILIES.get(word) or {word})
    for item in facts.get("condition") or ():
        said = str(item).lower()
        for condition, foods in CONDITION_BANS.items():
            if condition in said:
                banned.update(foods)
    diet = str(facts.get("diet") or "").lower()
    if diet in ("vegetarian", "veggie", "vego"):
        banned.update(NO_MEAT_DIET)
    elif diet in ("vegan", "plant based", "plantbased"):
        banned.update(NO_MEAT_DIET | DAIRY | EGGS)
    elif diet.startswith("no "):
        word = diet[3:].strip()
        banned.update(FAMILIES.get(word) or {word})
    return banned


def _named_families(banned):
    return {family for family, name in BAN_SAY if name in banned}


def _bans_said(banned):
    named = _named_families(banned)
    names = [name for family, name in BAN_SAY if family in named]
    if not names:
        names = [name for family, name in BAN_SAY if family & banned]
    if "meat" in names and "shellfish" in names:
        names.remove("shellfish")
    if "meat" in names and "fish" in names:
        names.remove("fish")
    return names


BAN_SAY_NAME = {id(NUTS): "nuts", id(GLUTEN): "gluten", id(DAIRY): "milk",
                id(EGGS): "egg", id(MEAT): "meat", id(FISH): "fish",
                id(SHELLFISH): "shellfish"}

FREE_OF = {id(NUTS): "nut-free", id(GLUTEN): "gluten-free", id(DAIRY): "dairy-free",
           id(EGGS): "egg-free", id(MEAT): "meat-free", id(FISH): "fish-free",
           id(SHELLFISH): "shellfish-free"}


def _the_guest(memory, text):
    others = memory.get("others") if isinstance(memory, dict) else None
    if not isinstance(others, list) or not others:
        return None
    low = " ".join(str(text or "").lower().split())
    named = [other for other in others
             if isinstance(other, dict) and other.get("who")
             and re.search(r"\b" + re.escape(str(other["who"]).lower()) + r"\b", low)]
    if len(named) == 1:
        return named[0]
    if named:
        return None
    return others[0] if len(others) == 1 and isinstance(others[0], dict) else None


def _food_may(text):
    words = re.findall(r"[a-z']+", str(text or "").lower())
    for size in (2, 1):
        for start in range(len(words) - size + 1):
            phrase = " ".join(words[start:start + size])
            if phrase in MAY_HAVE:
                return phrase
    return None


def _someones_else_can_eat(match, line, memory):
    guest = _the_guest(memory, line)
    if not guest:
        return None
    if not (guest.get("allergies") or guest.get("condition")):
        return None
    said = " ".join(str(part or "") for part in match.groups() if part)
    food = _food_named(said) or _food_may(said)
    if not food:
        return None
    banned = _bans_of(guest)
    if not banned:
        return None
    if _record_says_lactose(guest) and not any(word in said.lower()
                                               for word in _NOT_LACTOSE_WORDS):
        answer = _lactose_answer(food, said)
        if answer:
            return answer
    return _not_for_them(food, banned, guest, said)


def _not_for_them(food, banned, guest, text=""):
    named = _named_as(text, food)
    who = str((guest or {}).get("who") or "").strip().lower()
    them = ("your " + who) if who else "them"
    named_here = _named_families(banned)
    hits = [family for family in ANY_FAMILY if family & MADE_OF.get(food, frozenset())
            and family & banned]
    hits.sort(key=lambda family: 0 if family in named_here else 1)
    if hits:
        said = FAMILY_SAY[id(hits[0])][0]
        if _is_plural(food):
            said = re.sub(r"\bis\b", "are", said)
        return ("No: " + named + " " + said + ", so it is off the table for " + them + ". "
                "A pack or a menu that says " + FREE_OF.get(id(hits[0]), "free from it") +
                " is the only check that settles it.")
    may = [family for family in ANY_FAMILY if family & MAY_HAVE.get(food, frozenset())
           and family & banned]
    if not may:
        return None
    family = may[0]
    what = "nuts" if family is NUTS else BAN_SAY_NAME.get(id(family), "it")
    return (named.capitalize() + " can be made without " + what + ", but the bought or "
            "restaurant version often has " + ("them" if what == "nuts" else "it") + " in, so for " +
            them + " the pack or the menu has to say " + FREE_OF.get(id(family), "free from it") +
            ".")


_POINTING = frozenset((
    "what", "how", "about", "and", "or", "then", "instead", "also", "so", "but", "just", "please",
    "with", "without", "for", "to", "can", "could", "may", "should", "shall", "would", "will",
    "do", "does", "did", "a", "an", "the", "be", "is", "are", "was", "were", "am", "i", "we",
    "you", "he", "she", "they", "him", "her", "them", "it", "that", "this", "those", "these",
    "ok", "okay", "fine", "alright", "safe", "allowed", "out", "off", "table", "no", "good",
    "wrong", "problem", "any", "some", "still", "too", "as", "well", "me", "my", "our", "us",
    "now", "next", "there", "again", "one", "thing", "things", "either", "neither", "not", "yes",
    "much", "many", "all", "right", "dodgy", "bad", "avoid", "of", "on", "in", "at",
))


_LEAVE_IT_OUT = frozenset((
    "no", "not", "dont", "doesnt", "didnt", "without", "avoid", "skip", "drop", "leave", "hold",
    "minus", "except", "apart",
))


def _foods_a_line_points_at(line):
    words = re.findall(r"[a-z']+", str(line or "").lower())
    if not words or len(words) > 7:
        return []
    foods = _foods_named(line)
    if not foods:
        may = _food_may(line)
        return [may] if may else []
    spare = set(" ".join(foods).split())
    left = [word for word in words if word not in spare and word not in _POINTING]
    if left:
        return []
    if any(word in _LEAVE_IT_OUT for word in words):
        return []
    return foods


def pointed_at_a_food(understood, memory):
    if not isinstance(understood, dict):
        return None
    line = str(understood.get("clean") or understood.get("text") or "")
    foods = _foods_a_line_points_at(line)
    if not foods:
        return None
    guest = _the_guest(memory, line)
    guest_bans = _bans_of(guest) if guest else frozenset()
    if guest_bans:
        hits = [food for food in foods if food in MADE_OF and _bans_it(food, guest_bans)]
        return _not_for_them(hits[0], guest_bans, guest, line) if len(hits) == 1 else None
    banned = _bans_for(understood, memory)
    if not _bans_said(banned):
        return None
    hits = [food for food in foods if food in MADE_OF and _bans_it(food, banned)]
    return _one_food_answer(hits[0], banned, line) if len(hits) == 1 else None


def suits_them(understood, memory):
    if not isinstance(understood, dict):
        return None
    line = str(understood.get("clean") or understood.get("text") or "")
    if EAT_ANY.search(line):
        said_here = [word for word in re.findall(r"[a-z']+", line.lower())
                     if word not in EAT_ANY_WORDS]
        if said_here:
            return None
        banned = _bans_for(understood, memory)
        if not _bans_said(banned):
            return None
        return _any_meal(banned)
    about_them = EAT_ASK_THEM.search(line)
    if about_them:
        return _someones_else_can_eat(about_them, line, memory)
    pointed = pointed_at_a_food(understood, memory)
    if pointed:
        return pointed
    banned = _bans_for(understood, memory)
    if not _bans_said(banned):
        return None
    asked = EAT_ASK.search(line) or EAT_ASK_IF.search(line)
    bare = False
    if not asked:
        if not EAT_ASK_BARE.search(line) or "still" in line.lower():
            return None
        asked = EAT_ASK_BARE.search(line)
        bare = True
    if asked:
        named_foods = _foods_named(asked.group(0))
        if not named_foods:
            return None
        if len(set(named_foods)) > 1:
            named_foods = [food for food in named_foods
                           if _bans_it(food, banned)]
            if not named_foods:
                return None
        return _one_food_answer(named_foods[0], banned, asked.group(0), bare=bare)
    return None


def considered(understood, memory):
    if not isinstance(understood, dict):
        return None
    line = str(understood.get("clean") or understood.get("text") or "")
    considering = FANCY_ASK.search(line)
    if not considering:
        return None
    banned = _bans_for(understood, memory)
    if not _bans_said(banned):
        return None
    food = _food_they_avoid(_foods_named(line[considering.end():]), banned)
    if food is None:
        return None
    return _one_food_answer(food, banned, line)


FREE_OF = {"meat": MEAT, "fish": FISH, "dairy": DAIRY, "milk": DAIRY, "lactose": DAIRY,
           "cheese": DAIRY, "gluten": GLUTEN, "wheat": GLUTEN, "nut": NUTS, "nuts": NUTS,
           "peanut": NUTS, "peanuts": NUTS, "egg": EGGS, "eggs": EGGS, "shellfish": SHELLFISH,
           "sugar": frozenset(), "soya": frozenset(), "soy": frozenset()}


def _free_of(text, food):
    text = str(text or "").lower().replace("\u2019", "'").replace("-", " ")
    phrase = r"\s+".join(re.escape(part) for part in food.split())
    for match in re.finditer(r"\b([a-z]+)\s+free\s+" + phrase + r"\b", text):
        if match.group(1) in FREE_OF:
            return FREE_OF[match.group(1)]
    for match in re.finditer(phrase + r"\s+(?:is\s+|are\s+)?([a-z]+)\s+free\b", text):
        if match.group(1) in FREE_OF:
            return FREE_OF[match.group(1)]
    return frozenset()


NOT_SETTLED_BY_THE_RECIPE = {
    "oats": ("With the right packet: an oat has no gluten in it, but oats are grown and milled "
             "next to wheat, so ordinary porridge oats are not safe for a coeliac. The ones "
             "marked gluten free are, and they cost about the same."),
    "porridge": ("With the right packet: an oat has no gluten in it, but oats are grown and "
                 "milled next to wheat, so ordinary porridge oats are not safe for a coeliac. "
                 "The ones marked gluten free are, and they cost about the same."),
    "oatmeal": ("With the right packet: an oat has no gluten in it, but oats are grown and "
                "milled next to wheat, so ordinary porridge oats are not safe for a coeliac. "
                "The ones marked gluten free are, and they cost about the same."),
}


def _bans_it(food, banned):
    return any(family & MADE_OF[food] and family & banned for family in ANY_FAMILY)


def _food_they_avoid(named_foods, banned):
    for food in named_foods:
        if _bans_it(food, banned):
            return food
    return None

LACTOSE_LOW = ("cheese", "butter", "cream")
LACTOSE_HIGH = ("milk", "yoghurt", "yogurt", "ice cream")
_LACTOSE_SAYS = {
    "cheese": ("Yes, usually: ageing eats almost all of the lactose, so a hard cheese such as "
               "cheddar or parmesan is the dairy food most people with a lactose intolerance can "
               "eat without trouble. Soft cheese - brie, cottage cheese, ricotta, mozzarella - "
               "has more of it left, so try a small amount with a meal first."),
    "butter": ("Yes: butter is mostly fat with only a trace of milk sugar left in it, so a normal "
               "spread is fine for most people with a lactose intolerance. Cream and ghee are the "
               "same idea; milk, yoghurt and ice cream are the ones with real lactose in them."),
    "cream": ("Yes, in a small amount: cream has far less lactose than milk, so a spoonful in a "
              "sauce is usually fine. Milk, soft cheese, yoghurt and ice cream are where most of "
              "the lactose is."),
    "milk": ("Not much of it, and not on its own: milk is where most of the lactose is, so a "
             "small glass with a meal is the test, and lactose-free milk is ordinary milk with the "
             "sugar already split - it does the same job in tea, on cereal and in cooking."),
    "yoghurt": ("Often yes: live yoghurt is easier than milk because the cultures do part of the "
                "digesting, so a small pot with a meal is usually fine. A big tub on its own, or "
                "ice cream, is where people notice it."),
    "yogurt": ("Often yes: live yogurt is easier than milk because the cultures do part of the "
               "digesting, so a small pot with a meal is usually fine. A big tub on its own, or "
               "ice cream, is where people notice it."),
    "ice cream": ("Not much of it: ice cream is milk and cream with sugar on top, so it is one of "
                  "the higher ones. A couple of spoons after a meal is a different thing from a "
                  "whole tub, and lactase tablets taken with the first mouthful cover it."),
}


_LACTOSE_FREE_ASK = re.compile(r"lactose[\s-]*free", re.I)


def _lactose_answer(food, text):
    if _LACTOSE_FREE_ASK.search(str(text or "")):
        return ("Yes: lactose-free milk is ordinary milk with the milk sugar already split, so it "
                "does the same job in tea, on cereal and in cooking. There are lactose-free "
                "yoghurts and soft cheeses too, though a hard cheese or butter has almost none "
                "left in it anyway.")
    if food in _LACTOSE_SAYS:
        return _LACTOSE_SAYS[food]
    if DAIRY & MADE_OF.get(food, frozenset()):
        return ("It depends how much milk is in it: milk, soft cheese, yoghurt and ice cream hold "
                "most of the lactose, while a hard cheese or butter has almost none left. Try a "
                "small portion with a meal, and lactose-free milk and lactase tablets are there "
                "for the ones that catch you out.")
    return None


def _one_food_answer(food, banned, text, bare=False):
    avoid = _bans_said(banned)
    if "lactose" in banned:
        answer = _lactose_answer(food, text)
        if answer:
            return answer
    made_of = MADE_OF[food] - _free_of(text, food)
    hits = [family for family in ANY_FAMILY if family & made_of and family & banned]
    named_here = _named_families(banned)
    hits.sort(key=lambda family: 0 if family in named_here else 1)
    if bare and not hits:
        return None
    if not hits:
        if food in FISH and MEAT in named_here and FISH not in named_here:
            return FISH_SPLIT
        if len(avoid) == 1:
            what = avoid[0]
        else:
            what = ", ".join(avoid[:-1]) + " or " + avoid[-1]
        named = _named_as(text, food)
        if food == "honey" and {"meat", "dairy", "egg"} <= banned:
            return ("Some vegans avoid honey, so it depends how strict you are - sugar or golden "
                    "syrup does the same job in a recipe.")
        if made_of:
            them = "them" if what in ("nuts",) else "it"
            return ("Nothing in " + named + " needs " + what + ", but a bought one can have " +
                    them + " in - check the label.")
        if "gluten" in avoid and food in NOT_SETTLED_BY_THE_RECIPE:
            return NOT_SETTLED_BY_THE_RECIPE[food]
        if _is_plural(food):
            return ("Yes: " + named + " have no " + what + " in them, so they are fine for you.")
        return "Yes: " + named + " has no " + what + " in it, so it is fine for you."
    said, swap = FAMILY_SAY[id(hits[0])]
    named = _named_as(text, food)
    if food in hits[0] and id(hits[0]) in SELF_SAY:
        return ("No: " + SELF_SAY[id(hits[0])] + ", and it is off the table for you. " +
                swap[0].upper() + swap[1:] + ".")
    if _is_plural(food):
        said = re.sub(r"\bis\b", "are", said)
    return ("No: " + named + " " + said + ", and that is off the table for you. " +
            swap[0].upper() + swap[1:] + ".")


def _no_meat_also_means_fish(banned):
    return banned | FISH if MEAT & banned else banned


def _bans(names, idea, banned):
    for name in names:
        if name in banned:
            return True
        if any(part in banned for part in name.split()):
            return True
    text = idea.lower()
    return any(re.search(r"\b" + re.escape(word) + r"\b", text) for word in banned)


MEAT_SAYS = MEAT | frozenset(
    "chorizo salami pancetta prosciutto pepperoni steak brisket liver kidney venison duck "
    "goose rabbit pheasant partridge anchovies anchovy sardines mackerel haddock kippers".split())
FISH_SAYS = FISH | frozenset(
    "anchovies anchovy sardines mackerel haddock kipper kippers shellfish prawns crab lobster "
    "mussels oysters squid clams scallops".split())
DAIRY_SAYS = DAIRY | CHEESES | frozenset("mozzarella creme buttermilk ghee".split())
EGG_SAYS = EGGS | frozenset("mayonnaise mayo omelette quiche custard meringue".split())
NUT_SAYS = NUTS | frozenset("almonds almond cashews cashew walnuts walnut pistachios pistachio "
                           "hazelnuts hazelnut pecans pecan brazil marzipan praline satay "
                           "nutella pesto".split())
SHELLFISH_SAYS = SHELLFISH | frozenset("prawn crab lobster mussel oyster squid clam scallop "
                                       "prawns crabs lobsters mussels oysters clams scallops".split())
DAIRY_SWAPS = (
    (re.compile(r"\ba knob of butter\b", re.I), "a little oil"),
    (re.compile(r"\b(?:a|one) spoon of cream\b", re.I), "a spoon of oat cream"),
    (re.compile(r"\bdouble cream\b", re.I), "oat cream"),
    (re.compile(r"\bmashed with butter\b", re.I), "mashed with olive oil"),
    (re.compile(r"\b(?<!peanut )(?<!cocoa )(?<!shea )(?<!apple )(?<!nut )(?<!butter )butter\b"
                r"(?!\s*beans?\b)", re.I), "oil"),
    (re.compile(r"\b(?<!coconut )(?<!oat )(?<!soy )(?<!almond )(?<!plant )(?<!rice )(?<!hemp )"
                r"(?<!butter )(?<!goat )(?<!sheep )milk\b", re.I), "plant milk"),
    (re.compile(r"\bsour cream\b", re.I), "soya yogurt"),
    (re.compile(r"\bcr[eè]me fra[iî]che\b", re.I), "soya cream"),
    (re.compile(r"\bor buttermilk\b", re.I), "or plant milk with a squeeze of lemon"),
    (re.compile(r"\b(?<!soya )(?<!soy )(?<!coconut )(?<!plant )(?<!oat )(?<!almond )"
                r"(?<!greek )(?:yoghurt|yogurt)\b", re.I), "soya yoghurt"),
)


NUT_SWAPS = (
    (re.compile(r"\balmond milk\b", re.I), "oat milk"),
    (re.compile(r"\balmond flour\b", re.I), "plain flour"),
    (re.compile(r"\bground almonds\b", re.I), "ground seeds"),
    (re.compile(r"\bflaked almonds\b", re.I), "seeds"),
    (re.compile(r"\b(?<!sunflower )(?<!seed )(?<!soya )(?<!olive )peanut butter\b", re.I),
     "sunflower seed butter"),
    (re.compile(r"\bnut butter\b", re.I), "seed butter"),
)


GLUTEN_WORDS = ("pasta", "toast")
GLUTEN_SWAPS = (
    ("pasta", re.compile(r"\b(?<!free )(?<!free- )pasta\b", re.I), "gluten-free pasta"),
    ("toast", re.compile(r"\b(?<!free )(?<!free- )toast\b", re.I), "gluten-free toast"),
)


NOT_THE_DAIRY = re.compile(r"\b(?:oat|soy|soya|coconut|almond|plant|rice|hemp|cashew|peanut|"
                           r"shea|cocoa|apple|nut)\s+$", re.I)


CAUTION_SAID = re.compile(
    r"\b(?:check|read|look at|watch)\s+(?:the\s+)?(?:label|labels|packet|packets|ingredients|"
    r"ingredient list|back of the (?:pack|packet|tin|box|jar)|pesto|chocolate|jar)"
    r"|\bmay contain\b|\ballergen|\bcross[- ]contamination"
    r"|\bask (?:the staff|them|whoever|at the counter|before)" 
    r"|\bcan have (?:it|them) in\b|\bcan (?:sometimes )?carry\b|\bmay have\b"
    r"|\boff the table for\b|\bnot for you\b|\brather not risk\b|\bstay (?:well )?clear\b"
    r"|\b(?:avoid|avoiding|watch out for)\b|\bfree from\b|\b(?:nut|dairy|gluten)[- ]free\b", re.I)

PLANT_SAID = re.compile(r"\b(?:vegan|vegetarian|plant based|plant-based|dairy free|dairy-free|"
                        r"egg free|"
                        r"margarine|flax egg|flaxseed|oat milk|soya milk|soy milk|almond milk|"
                        r"oat cream|soya cream|nutritional yeast|aquafaba)\b", re.I)


SWAP_BEFORE = re.compile(r"(?:instead of|in place of|rather than|swap for|substitute for|"
                         r"no need for|without|free of|for (?:each|every|the)|per|"
                         r"flax|chia|linseed|vegan|plant|soya|soy|oat|coconut|almond|nut)\s+"
                         r"(?:\d+\s*(?:g|ml)\s+(?:of\s+)?)?$", re.I)
SWAP_AFTER = re.compile(r"\s*-?\s*(?:free|replacer|substitute|swap)\b", re.I)
SWAP_WINDOW = 34


def _a_swap_not_a_dish(text, at, word):
    before = text[max(0, at - SWAP_WINDOW):at]
    after = text[at + len(word):at + len(word) + SWAP_WINDOW]
    return bool(SWAP_BEFORE.search(before) or SWAP_AFTER.match(after))


def _says_a_food(text, words):
    found = []
    for word in words:
        for match in re.finditer(r"\b" + re.escape(word) + r"(?:s|es)?\b", text, re.I):
            if word in DAIRY_SAYS and NOT_THE_DAIRY.search(text[:match.start()]):
                continue
            if word == "butter" and re.match(r"\s+beans?\b", text[match.end():], re.I):
                continue
            if _a_swap_not_a_dish(text, match.start(), match.group(0)):
                continue
            found.append(word)
            break
    return found


def avoids(memory, understood=None):
    if not isinstance(memory, dict):
        return frozenset()
    read = understood if isinstance(understood, dict) else memory.get("understood")
    if not isinstance(read, dict):
        read = {}
    try:
        return frozenset(_bans_for(read, memory))
    except Exception:
        return frozenset()


def _family_of(word):
    word = str(word or "").strip().lower()
    if not word:
        return set()
    for key in (word, word[:-1] if word.endswith("s") else word):
        if key in FAMILIES:
            return set(FAMILIES[key])
    return {word}


def avoids_for_the_one_talked_about(memory):
    if not isinstance(memory, dict):
        return frozenset()
    person = memory.get("person")
    if not isinstance(person, dict):
        return frozenset()
    who = str(person.get("who") or "").strip().lower()
    if not who:
        return frozenset()
    banned = set()
    for record in memory.get("others") or ():
        if not isinstance(record, dict):
            continue
        if str(record.get("who") or "").strip().lower() != who:
            continue
        for item in record.get("allergies") or ():
            banned |= _family_of(item)
        break
    return frozenset(banned)


def _the_banned_words(banned):
    words = set()
    if MEAT & banned or FISH & banned:
        words |= MEAT_SAYS
    if FISH & banned:
        words |= FISH_SAYS
    if DAIRY & banned and "lactose" not in banned:
        words |= DAIRY_SAYS
    if EGGS & banned:
        words |= EGG_SAYS
    if NUTS & banned:
        words |= NUT_SAYS
    if SHELLFISH & banned:
        words |= SHELLFISH_SAYS
    return frozenset(words)




SWAP_CLAUSE = re.compile(r"\b(?:in place of|instead of|rather than|or use|substitute for|"
                         r"swap for|no need for|works too)\b", re.I)


SAYS_THE_FOOD_IS_OUT = re.compile(
    r"off the table|not for you|you (?:cannot|can't|can not|shouldn't|should not) have|"
    r"leave (?:that|it|them|those) out|leave out the|you (?:do not|don't|dont) eat|"
    r"since you (?:are |'re )?(?:not eating|vegan|vegetarian|dairy|gluten)|"
    r"not eating (?:meat|dairy|gluten|eggs)|you avoid|you're avoiding|you are avoiding|"
    r"no meat|without the meat|swap (?:it|that)|there is no egg|that is egg|that's egg|"
    r"that is meat|those are meat|no dairy", re.I)


GLUTEN_FREE_ALREADY = re.compile(
    r"\b(?:gluten[- ]free|corn pasta|rice pasta|rice noodles|corn noodles|buckwheat|polenta|"
    r"cornmeal|chickpea pasta|lentil pasta|gram flour|rice flour)\b", re.I)


SUBSTITUTE_ASK = re.compile(
    r"\b(?:instead of|in place of|rather than|substitute|alternative to|replacement for|"
    r"replace|what can i use (?:for|in)|swap (?:it |that )?for|do without|without)\b", re.I)


def _rewritten_outside_swaps(text, pattern, swap, leave=None):
    parts = re.split(r"([.!?:]\s+|,\s+)", text)
    for i in range(0, len(parts), 2):
        if not SWAP_CLAUSE.search(parts[i]) and not (leave and leave.search(parts[i])):
            parts[i] = pattern.sub(swap, parts[i])
    return "".join(parts)


def _uncautioned(text, words):
    if not CAUTION_SAID.search(text):
        return set(_says_a_food(text, words))
    fresh = set()
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        if CAUTION_SAID.search(sentence):
            continue
        fresh |= set(_says_a_food(sentence, words))
    return fresh


def _nut_swapped(text, banned, line):
    if not (NUTS & banned) or not _a_nut_swap_is_safe(text, line):
        return text
    swapped = text
    for pattern, swap in NUT_SWAPS:
        swapped = _rewritten_outside_swaps(swapped, pattern, swap)
    if swapped == text or names_a_banned_food(swapped, banned, line):
        return text
    return swapped


def _a_nut_swap_is_safe(text, line):
    if SAYS_THE_FOOD_IS_OUT.search(text):
        return False
    return not _says_a_food(str(line or ""), NUT_SAYS)


def fitted_for_the_one_talked_about(reply, banned, line=""):
    if not isinstance(reply, str) or not reply.strip() or not banned:
        return reply
    text = reply
    text = _nut_swapped(DIET_VARIANTS.get(text.strip(), text), banned, line)
    if names_a_banned_food(text, banned, line):
        return None
    return text


def names_a_banned_food(reply, banned, line=""):
    if not isinstance(reply, str) or not reply.strip() or not banned:
        return False
    words = _the_banned_words(banned)
    if not words:
        return False
    said_already = set(_says_a_food(str(line or ""), words))
    said_already |= {word[:-1] for word in said_already if word.endswith("s")}
    left = [word for word in _uncautioned(reply, words)
            if word not in said_already and word[:-1] not in said_already]
    return bool(left)


def fits_the_diet(reply, banned, line=""):
    if not isinstance(reply, str) or not reply.strip() or not banned:
        return reply
    text = reply
    line_words = set(_says_a_food(str(line or ""),
                                 set(_the_banned_words(banned)) | set(GLUTEN_WORDS)))
    if GLUTEN & banned:
        for word, pattern, swap in GLUTEN_SWAPS:
            if word not in line_words:
                text = _rewritten_outside_swaps(text, pattern, swap,
                                                leave=GLUTEN_FREE_ALREADY)
    words = _the_banned_words(banned)
    if not words:
        return text
    if _ask_about_the_food(str(line or "").lower(), len(str(line or ""))):
        return text
    said_already = set(_says_a_food(str(line or ""), words))
    said_already |= {word[:-1] for word in said_already if word.endswith("s")}
    left = [word for word in _uncautioned(text, words)
            if word not in said_already and word[:-1] not in said_already]
    if not left:
        return text
    nuts_only = NUTS & banned and not (banned - NUTS)
    if MEAT & banned or FISH & banned or nuts_only:
        text = DIET_VARIANTS.get(text.strip(), text)
    if DAIRY & banned and "lactose" not in banned and not PLANT_SAID.search(text):
        for pattern, swap in DAIRY_SWAPS:
            text = _rewritten_outside_swaps(text, pattern, swap)
    text = _nut_swapped(text, banned, line)
    said = _says_a_food(text, words)
    if PLANT_SAID.search(text):
        said = [word for word in said
                if word not in DAIRY_SAYS and word not in EGG_SAYS
                and word not in MEAT_SAYS and word not in FISH_SAYS]
    left = [word for word in said if word not in said_already]
    if not left:
        return text
    if SUBSTITUTE_ASK.search(str(line or "").lower()):
        return text
    if SAYS_THE_FOOD_IS_OUT.search(text):
        return text
    without = _the_card_without_that_sentence(text, left, words)
    if without:
        return without
    first = re.split(r"(?<=[.!?])\s+", text.strip(), maxsplit=1)[0]
    if not [word for word in _says_a_food(first, words) if word in left or word[:-1] in left]:
        return text
    return None


def _the_card_without_that_sentence(text, left, words):
    bits = re.split(r"([.!?]+\s+|;\s+|,\s+(?:then|and)\s+)", str(text).strip())
    keep = []
    dropped = 0
    for index in range(0, len(bits), 2):
        part = bits[index]
        names = _says_a_food(part, words)
        if [word for word in names if word in left or word[:-1] in left]:
            dropped += 1
            continue
        keep.append(part)
    if not dropped or not keep:
        return None
    if not keep[0].strip(" ,.;:") or keep[0] is not bits[0]:
        return None
    said = ", ".join(part.strip(" ,.;:").lower() if index else part.strip(" ,;")
                     for index, part in enumerate(keep) if part.strip(" ,.;:"))
    if not said:
        return None
    if len(said) < 40 or len(said) < 0.55 * len(str(text).strip()):
        return None
    said = said[0].upper() + said[1:]
    return said if said.endswith((".", "!", "?")) else said + "."


def _any_meal(banned):
    if GLUTEN & banned:
        egg = "" if {"egg", "eggs"} & banned else " and an egg"
        cheese = "hummus" if DAIRY & banned else "cheese"
        return ("Ten-minute dinners, all gluten free: rice fried with frozen veg" + egg +
                "; a jacket potato with beans and " + cheese +
                "; or a chickpea and tomato curry with rice. Tell me what is in the fridge and "
                "I will pick one.")
    if {"egg", "eggs"} & banned:
        if DAIRY & banned:
            return ("Ten-minute dinners: a chickpea and tomato curry with rice; pasta with garlic, "
                    "chilli and olive oil; or beans on toast with hummus. Tell me what is in the "
                    "fridge and I will pick one.")
        return ("Ten-minute dinners: a chickpea and tomato curry with rice; pasta with garlic, "
                "chilli and olive oil; or beans on toast with a little cheese or hummus. Tell me "
                "what is in the fridge and I will pick one.")
    if MEAT <= banned:
        return ("Ten-minute dinners: pasta with garlic, chilli and olive oil; a chickpea and "
                "tomato curry with rice; or eggs on toast. Tell me what is in the fridge and I "
                "will pick one.")
    return ANY_MEAL


_NOT_A_DISH = frozenset((
    "tonight", "today", "now", "later", "tomorrow", "weekend", "evening", "lunchtime", "noon",
    "quick", "quickly", "fast", "easy", "easier", "simple", "cheap", "cheaper", "healthy",
    "healthier", "nice", "tasty", "good", "new", "different", "something", "anything", "nothing",
    "some", "one", "two", "few", "first", "family", "kids", "friends", "guests", "everyone",
    "vegetarian", "vegan", "gluten", "dairy", "free", "light", "filling", "cosy", "comfort",
))


def _cauliflower_rice(memory, understood):
    words = {_fold(str(word)) for word in (understood.get("words") or [])}
    method = ("Grate or blitz a head of cauliflower into rice-sized bits, wrap it in a tea towel "
              "and squeeze out the water, then fry it in a little oil for 4 to 5 minutes with salt "
              "until it is hot but still has a bite. Do not boil it: that is what makes it soggy. "
              "One head makes four good portions and keeps three days in the fridge.")
    if words & {"carb", "carbs", "keto", "diet", "diabetes", "sugar", "low"}:
        return ("Cauliflower is one of the lowest-carb vegetables there is: about 3g of carbs per "
                "100g, against about 28g in cooked rice, so it works on a low-carb or diabetic "
                "plate. " + method)
    return method


def _recipe_for_unknown_dish(lowered):
    match = re.search(r"\brecipe\b(?:\s+(?:for|of|to make))?\s+(.*)$", lowered)
    if not match:
        return False
    tail = re.findall(r"[a-z']+", match.group(1))
    if not tail:
        return False
    if any(word in ("idea", "ideas", "meal", "dinner", "tea", "supper") for word in tail):
        return False
    food_words = [word for word in tail if word not in _NOT_A_DISH][:3]
    if not food_words:
        return False
    return all(word not in _INGREDIENT_WORDS and word not in _FOOD for word in food_words)
def _first_sentence(idea):
    parts = re.split(r"(?<=[.!?])\s+", idea.strip(), maxsplit=1)
    return parts[0] if parts else idea


def _leftover(folded, clean):
    return (any(word in LEFTOVER_WORDS for word in folded)
            or any(phrase in clean for phrase in LEFTOVER_PHRASES))


_PULSES_HARD = re.compile(
    r"\b(?:still (?:hard|firm|crunchy|tough|chalky)|not soft(?:ening)?|wont (?:soften|go soft)"
    r"|will not (?:soften|go soft)|never soften|hard after|too hard|too firm|took ages"
    r"|been cooking (?:for )?(?:an|two|2|three|3) hours?)\b")
_PULSES_NO_SOAK = re.compile(
    r"\b(?:without (?:a )?soaking|without a soak|no soak(?:ing)?|skip(?:ped)? the soak"
    r"|skip(?:ping)? soaking|didnt soak|did not soak|forgot to soak|forget to soak"
    r"|no time to soak|havent soaked|have not soaked|not soaked|quick soak|quick-soak"
    r"|in a hurry|short on time|last minute|just cook|straight from the bag"
    r"|without the soak|unsoaked)\b")
_PULSES_TIN = re.compile(r"\b(?:tinned|canned|jarred|jar|tin|tins|packet|carton)\b"
                         r"|\bcans? of\b")
_PULSES_FRESH = re.compile(
    r"\b(?:green|runner|broad|french|string|stringy|snap|mangetout|edamame|pea|peas)\b")
_PULSES_DRIED = re.compile(
    r"\b(?:soak|soaks|soaked|soaking|overnight|quick soak|no soak|dried|dry|bag|bags|packet"
    r"|packets|tinned|tin|canned|can)\b")
_PULSES_APPLIANCE = re.compile(
    r"\b(?:slow cooker|slow cookers|crock ?pot|pressure cooker|pressure cookers|instant pot"
    r"|air fryer|air fryers|multicooker|multi cooker)\b")
_PULSES_KIDNEY = re.compile(r"\b(?:kidney|kidney beans?)\b")


def _pulses(memory, understood):
    said = _words_and_text(understood)
    if (_PULSES_FRESH.search(said) and "split peas" not in said
            and not _PULSES_DRIED.search(said)):
        return None
    if _PULSES_TIN.search(said) and not _PULSES_HARD.search(said):
        return None
    if _PULSES_APPLIANCE.search(said) and not _PULSES_KIDNEY.search(said):
        return None
    if _PULSES_HARD.search(said):
        return ("Old beans are usually the reason: a bag that has sat in the cupboard for years "
                "takes twice as long however you cook it. Keep it at a bare simmer with the lid "
                "just off, top it up with hot water, and give it another 20 to 30 minutes with a "
                "half teaspoon of bicarbonate of soda in the pan - and leave the salt, tomato and "
                "vinegar until the beans are soft, because acid early is the other thing that "
                "keeps the skins tough. Hard water does the same, so use filtered water if yours "
                "is very chalky.")
    if _PULSES_NO_SOAK.search(said):
        return ("You can skip the soaking: boil them hard for 2 minutes, take the pan off the "
                "heat and leave it covered for an hour, then simmer as usual - or cook them "
                "straight from the bag for 30 to 45 minutes longer and top up with hot water. "
                "Kidney beans are the one exception: boil them hard for 10 minutes before the "
                "simmer, and never cook them raw in a slow cooker.")
    return ("Dried chickpeas and beans want 8 hours of cold water, then 45 to 60 minutes of hard "
            "simmering; lentils need no soaking at all, just 20 to 30 minutes in the pan. Kidney "
            "beans must be boiled hard for 10 minutes, never slow cooked raw.")


def _lentils(memory, understood):
    return ("No soaking: rinse and simmer in plenty of water. Red lentils split and go soft in 15 "
            "to 20 minutes, which soups and dal want; green or brown stay whole at 20 to 25; puy "
            "take about 25 and hold their shape in salads. Salt near the end, not at the start, and "
            "taste at 15 minutes: a minute either way is firm against mushy. One mug of dried makes "
            "two cooked, and a bay leaf and half an onion in the water do more for flavour than "
            "anything added later.")


_PLAN_ASK = re.compile(
    r"\b(?:meal plans?|meal planning|planning meals|plan (?:my |the |a )?(?:week|meals)\b"
    r"|meals for the week|weekly meal|food plan|plan a week of meals)")


def _keeps_its_own_name(memory, understood, idea):
    from . import meals

    words = [_fold(word) for word in (understood.get("words") or ())]
    named = []
    for place, word in enumerate(words):
        if _INGREDIENT_WORDS.get(word) != _INGREDIENT_WORDS.get(word, word):
            continue
        name = _INGREDIENT_WORDS.get(word)
        if name and _fold(name) == word and word not in named:
            named.append(word)
        if place + 1 < len(words):
            pair = word + " " + words[place + 1]
            if _INGREDIENT_WORDS.get(pair) and _fold(_INGREDIENT_WORDS[pair]) == pair:
                named.append(pair)
    if len(named) != 1:
        return False
    text = " ".join(words)
    if (any(word in LEFTOVER_WORDS for word in words)
            or any(phrase in text for phrase in LEFTOVER_PHRASES)):
        return False
    if meals._diet_said(memory):
        return False
    if any(f"{marker} {named[0]}" in text for marker in ("old", "stale", "dry", "yesterday")):
        return False
    if meals._is_the_ruled_out_food(named[0], " ".join(words)):
        return False
    said = [_fold(word) for word in re.findall(r"[a-z']+", idea.lower())]
    return named[0] not in said

PET_ANIMALS = ("rabbit", "rabbits", "bunny", "bunnies", "guinea pig", "guinea pigs", "guineapig",
               "hamster", "hamsters", "gerbil", "gerbils", "chinchilla", "chinchillas",
               "degus", "degu", "hedgehog", "hedgehogs", "tortoise", "tortoises", "parrot",
               "parrots", "budgie", "budgies")
_PET_OWNED = ("my ", "our ", "pet ", "the pet ")
_PET_EATING = ("ate", "eaten", "eats", "chewed", "chewing", "nibbled", "nibbling", "got into",
               "stole", "stolen", "swallowed")

_ORDER_NOT_A_MEAL = ("first or last", "last or first", "first or after", "before or after",
                     "in first", "in last", "go in first", "goes in first", "go in last",
                     "goes in last", "which goes in", "which one goes in", "which first",
                     "in what order", "what order", "order do i", "either way round",
                     "milk first", "milk last")


_MILK_IN_TEA_NOT_A_MEAL = ("in tea", "in my tea", "in the tea", "in a cup of tea",
                           "in a mug of tea", "in a brew", "in my brew", "in the brew",
                           "for a cup of tea", "for my tea with milk")


def _a_brew_not_a_dinner(line):
    low = " " + str(line or "").lower() + " "
    if any(f" {phrase} " in low for phrase in _ORDER_NOT_A_MEAL):
        return True
    if " milk " not in low and not low.startswith(" milk"):
        return False
    return any(f" {phrase} " in low or f" {phrase}." in low
               for phrase in _MILK_IN_TEA_NOT_A_MEAL)


def _an_order_not_a_dinner(line):
    low = " " + str(line or "").lower() + " "
    return any(f" {phrase} " in low for phrase in _ORDER_NOT_A_MEAL)


_PLANT_NOT_A_DINNER = ("tree", "trees", "bush", "bushes", "shrub", "shrubs", "sapling",
                       "saplings", "seedling", "seedlings", "plant", "plants", "potted",
                       "bare root", "bare-root", "root ball", "compost", "greenhouse",
                       "allotment", "windowsill", "window sill", "cuttings", "cutting")
_PLANT_GARDEN_VERB = ("bought", "buy", "buying", "planted", "planting", "grow", "growing",
                      "grew", "repot", "repotted", "died", "dying", "dead", "water", "watering",
                      "feed", "feeding", "prune", "pruning", "sow", "sowing", "sowed",
                      "transplant", "potted on", "flowering", "fruiting")
_PLANT_COOK_ASK = ("cook", "cooks", "cooking", "recipe", "recipes", "make", "makes", "making",
                   "eat", "eating", "dinner", "supper", "lunch", "roast", "bake", "baking",
                   "fry", "boil", "serve", "dish", "meal", "use up", "use them", "use it")


_PLANT_SOURCE = re.compile(
    r"\b(?:from|off|out of|in|on|at)\s+(?:the\s+|my\s+|our\s+|a\s+|an\s+|his\s+|her\s+"
    r"|their\s+)?(?:" + "|".join(_PLANT_NOT_A_DINNER) + r")\b")


_PLANT_KITCHEN_PLANT = ("herb", "herbs")
_PLANT_BEARS = ("has fruit", "have fruit", "had fruit", "with fruit", "full of fruit",
                "loaded with fruit", "in fruit", "covered in fruit", "bears fruit",
                "bearing fruit", "producing fruit")
_PLANT_DO_WITH = ("do with", "use", "using", "used up", "glut", "too many", "loads of",
                  "all these", "all this", "all the", "bumper", "plenty of", "left over",
                  "what can i", "what should i", "what do i")


def _the_garden_has_this_plant(line):
    from .garden import ENTRIES as _GARDEN_ENTRIES
    text = str(line or "")
    words = tuple(word for word in re.split(r"[^a-z0-9']+", text.lower()) if word)
    reading = {"clean": text, "text": text, "words": words, "kind": "ask"}
    return find(reading, entries=_GARDEN_ENTRIES) is not None


_PLANT_WOODY = ("tree", "trees", "bush", "bushes", "shrub", "shrubs", "sapling", "saplings",
                "bare root", "bare-root", "root ball", "climber", "climbers", "hedge", "hedges")
_PLANT_PURCHASE = ("bought", "buy", "buying", "picked up", "came home with", "brought home",
                   "arrived", "delivered", "got it home")


def _a_plant_from_the_shop(line):
    low = " " + str(line or "").lower().replace("'", " ") + " "
    return (any(f" {word} " in low for word in _PLANT_WOODY)
            and any(f" {word} " in low for word in _PLANT_PURCHASE))


def _a_plant_not_a_dinner(line):
    low = " " + str(line or "").lower().replace("'", " ") + " "
    if not any(f" {word} " in low for word in _PLANT_NOT_A_DINNER):
        return False
    if (any(f" {word} " in low for word in _PLANT_KITCHEN_PLANT)
            and any(f" {word} " in low for word in ("bought", "buy", "buying", "got", "picked up"))):
        return False
    if any(f" {word} " in low for word in _PLANT_GARDEN_VERB):
        return _the_garden_has_this_plant(line) or _a_plant_from_the_shop(line)
    if any(f" {phrase} " in low for phrase in _PLANT_BEARS):
        return False
    named = sum(low.count(f" {word} ") for word in _PLANT_NOT_A_DINNER)
    asked = (any(f" {word} " in low for word in _PLANT_COOK_ASK)
             or any(f" {word} " in low for word in _PLANT_DO_WITH))
    if named and asked and len(_PLANT_SOURCE.findall(low.replace("  ", " "))) >= named:
        return False
    if any(f" {word} " in low for word in _PLANT_COOK_ASK):
        return False
    return _the_garden_has_this_plant(line) or _a_plant_from_the_shop(line)


_FEEDING_ANIMALS = (r"rabbits?|bunn(?:y|ies)|guinea\s?pigs?|hamsters?|gerbils?|chinchillas?|"
                    r"degus?|hedgehogs?|tortoises?|budgies?|parrots?")
FEEDING_EATS = re.compile(
    r"\b(?:" + _FEEDING_ANIMALS + r")\b(?:\W+\w+){0,3}?\W+(?:eat|eats|eating|have|has|drink|"
    r"drinks|be\s+fed|be\s+given|be\s+allowed|allowed|take|tolerate)\b")
FEEDING_GIVEN = re.compile(
    r"\b(?:feed|feeding|fed|give|giving|gave)\b(?:\W+\w+){0,2}?\W+(?:my|our|the|a|an)?\W*"
    r"(?:" + _FEEDING_ANIMALS + r")\b")
FEEDING_SAFE_FOR = re.compile(
    r"\b(?:safe|ok|okay|fine|bad|good|toxic|poisonous|dangerous|harmful|lethal)\b"
    r"(?:\W+\w+){0,4}?\W+(?:for|to)\b(?:\W+\w+){0,2}?\W+(?:" + _FEEDING_ANIMALS + r")\b")


FEEDING_NOT_FOOD = ("recipe", "recipes", "roast", "braise", "casserole", "stew", "fry", "bake",
                    "butcher", "joint", "dinner", "supper", "meal", "chef", "oven", "pan",
                    "sous vide", "marinade", "rub")


def _feeding_ask(line):
    low = " " + str(line or "").lower() + " "
    if any(word in low for word in FEEDING_NOT_FOOD):
        return False
    return bool(FEEDING_EATS.search(low) or FEEDING_GIVEN.search(low)
                or FEEDING_SAFE_FOR.search(low))


def _pet_not_dinner(line):
    low = " " + str(line or "").lower() + " "
    animals = [animal for animal in PET_ANIMALS if f" {animal} " in low]
    if not animals:
        return False
    if any(f" {owner}{animal} " in low for animal in animals for owner in _PET_OWNED):
        return True
    return any(f" {verb} " in low for verb in _PET_EATING)


PET_MEAT_ANIMALS = ("duck", "goose", "gander", "pigeon", "quail", "pheasant", "deer")
PET_HOME = re.compile(
    r"\b(?:in\s+the\s+(?:room|house|home|lounge|living\s+room|front\s+room|kitchen|bedroom|"
    r"garden)|indoors|hutch|cage|coop|aviary|litter\s+tray|is\s+called|named|kept\s+in)\b")
PET_NOT_FOOD = ("bought", "butcher", "from the shop", "from the market", "farmers market",
                "in the freezer", "frozen", "from the farm shop", "shot", "from a shoot",
                "joint", "breast", "thigh", "leg", "casserole")
PET_CARE = ("feed", "feeding", "fed", "food for", "called", "named", "care", "vet", "hutch",
            "litter", "breed", "groom", "sick", "ill", "not eating", "wont eat", "won't eat",
            "ate", "eaten", "eats", "chewed", "chewing", "nibbled", "nibbling", "got into",
            "stole", "stolen", "swallowed")
PET_COOKING_ASK = ("cook", "make", "recipe", "dinner", "tea", "supper", "meal", "roast",
                   "braise", "use up")


def _reads_as_a_pet(line):
    low = " " + str(line or "").lower() + " "
    if any(marker in low for marker in PET_NOT_FOOD):
        return False
    if _pet_not_dinner(line):
        return True
    owned = any(f"my {animal} " in low or f"our {animal} " in low
                for animal in PET_MEAT_ANIMALS)
    return owned and bool(PET_HOME.search(low))


def _pet_or_meat(line):
    low = str(line or "").lower()
    if not any(word in low for word in PET_COOKING_ASK):
        return None
    if any(word in low for word in PET_CARE):
        return None
    if not _reads_as_a_pet(low):
        return None
    for name, (aliases, idea) in PANTRY.items():
        if name not in PET_ANIMALS + PET_MEAT_ANIMALS:
            continue
        if f" {name} " not in low and f" {name}s " not in low:
            continue
        meat = str(idea)
        head, _, rest = meat.partition(": ")
        if not rest or not head or head.lower().split()[0] not in name:
            rest = meat
        rest = rest.strip()
        if not rest:
            return None
        return ("That reads as a pet rather than a dinner, and I would keep it off the plate. "
                "If you meant the meat, " + rest[0].lower() + rest[1:])
    return None


def _meal_ideas(memory, understood):
    from . import meals

    words = understood.get("words")
    if not isinstance(words, list):
        words = " ".join(words or ()).split()
    line = str(understood.get("clean") or " ".join(str(word) for word in words))
    text = line
    turns = memory.get("turns")
    if isinstance(turns, list):
        text += " " + " ".join(str(turn.get("user") or "") for turn in turns[-4:]
                               if isinstance(turn, dict))
    if _pet_not_dinner(line):
        return _pet_or_meat(line)
    if _a_brew_not_a_dinner(line):
        return None
    if _PLAN_ASK.search(line.lower()):
        return ("Pick four dinners you already cook and put them on the fridge, then shop for "
                "just those - one double batch goes in the freezer for the night you are late "
                "home. Keep one night loose for eggs on toast or a takeaway, and plan whatever "
                "spoils first for the day after you shop.")
    if any(word in line.lower() for word in ("dessert", "puddings", "pudding", "afters",
                                             "ice cream", "sweet thing")):
        return None
    banned = (frozenset(_no_meat_also_means_fish(_excluded(text)))
              | frozenset(_short_of_food(text))
              | frozenset(negated_ingredients(understood)))
    table = re.sub(r"\bfor\s+\d{1,3}\s*(?:min|mins|minute|minutes|hour|hours|sec|seconds)\b",
                   " ", text).lower()
    asking = str(understood.get("intent") or "") != "news" and (
        str(understood.get("kind") or "") == "question"
        or str(understood.get("intent") or "") in ("question", "request")
        or any(word in line.lower() for word in (
            "what", "idea", "ideas", "something", "suggest", "suggestion", "dinner",
            "dinners", "meal", "meals", "menu", "tea", "supper", "lunch", "cook for",
            "make for", "feed", "recipe", "anything", "any", "need", "want", "party",
            "guests", "everyone")))
    table_count = _crowd(table)
    at_table = asking and not _says_a_diet(line) and (
        table_count >= 6
        or (table_count >= 3
            and any(phrase in line.lower() for phrase in _CROWD_PHRASES))
        or (
            _occasion(table) and any(
                phrase in line.lower() for phrase in ("what should i cook", "what can i cook",
                                                      "what shall i cook", "what to cook",
                                                      "what to make", "meal", "dinner", "cook",
                                                      "no idea"))))
    if at_table:
        return _crowd_or_any(table, banned)
    idea = meals.suggest(memory, understood)
    if idea and banned and _bans((), str(idea), banned):
        idea = None
    if idea and _keeps_its_own_name(memory, understood, idea):
        words = understood.get("words")
        if not isinstance(words, list):
            words = " ".join(words or ()).split()
        own = _pantry_idea([str(word) for word in words] + str(
            understood.get("clean") or "").split(), banned, line.lower())
        if own and isinstance(own[1], str) and own[1].strip():
            idea = own[1]
    if idea:
        return idea
    asks_food = (understood.get("topic") in ("cooking", "food-and-drink")
                 or any(phrase in line.lower() for phrase in MEAL_ASK_PHRASES))
    if asks_food:
        from_pantry = meal(understood, banned=banned, memory=memory)
        if (isinstance(from_pantry, str) and from_pantry.strip()
                and not _bans((), from_pantry, banned)):
            return from_pantry
    if meals.unknown_food(understood):
        return None
    if not banned and re.search(r"\bwithout\b", line.lower()) and not _says_a_diet(line):
        return None
    if _says_diabetes(text):
        return DIABETIC_PLATE
    return _any_meal(banned)


def pantry_idea(name):
    folded = _fold(str(name or "").lower())
    if not folded:
        return None
    for aliases, idea in PANTRY.values():
        for alias in aliases:
            key = _fold(str(alias).lower())
            if key == folded or key == folded.rstrip("s") or key.rstrip("s") == folded:
                return idea
    return None


def _pantry_idea(words, banned, clean=""):
    found = None
    reached = None
    for name, (aliases, idea) in PANTRY.items():
        if _bans(aliases, idea, banned):
            continue
        if any(phrase in clean for phrase in NOT_THIS_FOOD.get(name, ())):
            continue
        for alias in aliases:
            parts = alias.split()
            for start in range(len(words) - len(parts) + 1):
                if all(_fold(words[start + offset]) == _fold(parts[offset])
                       for offset in range(len(parts))):
                    spot = (start, -len(parts))
                    if reached is None or spot < reached:
                        reached = spot
                        found = (start, idea)
                    break
    return found


def _occasion(text):
    if any(word in text for word in _OCCASIONS):
        return True
    return bool(re.search(r"\b\d{1,3}(?:st|nd|rd|th)\b", text))


def _crowd_or_any(text, banned):
    if _table_text(text):
        return _crowd_meal(banned, _occasion(text), _crowd(text))
    if _occasion(text) and any(
            phrase in text for phrase in ("what should i cook", "what can i cook",
                                          "what shall i cook", "what to cook", "what to make",
                                          "meal", "dinner", "cook", "no idea")):
        return _crowd_meal(banned, True, _crowd(text))
    return _any_meal(banned)


ANY_BREAKFAST = ("Porridge with a spoon of peanut butter and a banana, eggs on toast, or yoghurt "
                 "with fruit and oats: any of the three takes under ten minutes and keeps you going "
                 "until lunch. If mornings are rushed, boil an egg the night before and take a "
                 "piece of fruit with it.")

def _porridge(banned):
    if GLUTEN & banned:
        milk = "oat milk" if DAIRY & banned else "milk"
        return "Porridge made with gluten free oats and " + milk
    if DAIRY & banned:
        return "Porridge made with oat milk and a spoon of jam"
    return "Porridge with a banana and a spoon of jam"


BREAKFAST_CHOICES = (
    (frozenset(), lambda banned: _porridge(banned)),
    (EGGS | GLUTEN, "eggs on toast"),
    (GLUTEN | NUTS, "toast with peanut butter"),
    (GLUTEN, "beans on toast"),
    (GLUTEN, "toast with hummus"),
    (DAIRY | GLUTEN, "yoghurt with fruit and oats"),
    (DAIRY, "rice cakes with cheese"),
    (EGGS, "a boiled egg with fruit"),
    (NUTS, "a banana with a handful of nuts"),
)
BREAKFAST_TAIL = (": any of the three takes under ten minutes and keeps you going all morning.")


SHORT_OF_ASK = re.compile(r"\b(?:out of|ran out of|run out of|none left|nothing left|"
                          r"short of|outta|havent got|haven't got)\s+")


def _short_of_food(text):
    found = set()
    for match in SHORT_OF_ASK.finditer(str(text or "").lower()):
        found |= _foods_in_list(_list_words(str(text).lower()[match.end():match.end() + 60]))
    return found


def _rushed(banned):
    if not (EGGS & banned):
        return (" If mornings are rushed, boil an egg the night before and take a piece of fruit.")
    return (" If mornings are rushed, put it out the night before and eat it on the way, because "
            "a breakfast you can pick up beats one you skip.")


def _breakfast_ideas(memory, understood):
    text = _said_so_far(understood, memory)
    banned = _no_meat_also_means_fish(_excluded(text))
    short = _short_of_food(text)
    if not banned and not short:
        return ANY_BREAKFAST
    banned = banned | short
    ideas = []
    for needs, idea in BREAKFAST_CHOICES:
        if needs & banned:
            continue
        ideas.append(idea(banned) if callable(idea) else idea)
        if len(ideas) == 3:
            break
    if not ideas:
        return ("A bowl of fruit and a glass of juice, or a slice of toast with jam if bread is "
                "allowed" + BREAKFAST_TAIL + _rushed(banned))
    if len(ideas) == 1:
        return ideas[0] + BREAKFAST_TAIL + _rushed(banned)
    said = ", ".join(ideas[:-1]) + (" or " if len(ideas) == 2 else ", or ") + ideas[-1]
    return said + BREAKFAST_TAIL + _rushed(banned)




ANY_LUNCH = ("A sandwich or wrap with something filling (cheese, tuna, ham, hummus), fruit, "
             "something crunchy and a drink is a packed lunch in five minutes; cook extra dinner "
             "and take the leftovers in a tub and it is quicker still. Keep anything with meat, "
             "fish, egg or dairy cold until you eat it.")


def _lunch_ideas(memory, understood):
    words = understood.get("words")
    if not isinstance(words, list):
        words = " ".join(understood.get("words") or []).split()
    text = _said_so_far(understood, memory)
    banned = _no_meat_also_means_fish(_excluded(text))
    if not banned:
        return ANY_LUNCH
    fillings = [name for name, needs in (("cheese", DAIRY), ("tuna", {"tuna"}),
                                        ("ham", {"ham"}), ("egg", EGGS),
                                        ("hummus", set()), ("avocado", set()),
                                        ("roasted vegetables", set()))
                if not (needs & banned)]
    if "gluten" in banned:
        if fillings:
            return ("For a lunch that is not a sandwich: a rice or potato salad with " +
                    ", ".join(fillings[:3]) + ", fruit and a drink. Cook extra dinner and take the "
                    "leftovers in a tub and it is quicker still. Keep it in a cool bag until lunch.")
        return ("For a lunch that is not a sandwich: cook extra dinner and take the leftovers in a "
                "tub with rice, potatoes or salad, fruit and a drink. Keep it in a cool bag until "
                "lunch.")
    if not fillings:
        return ("Cook extra dinner and take the leftovers in a tub with fruit and something crunchy: "
                "that is a packed lunch in five minutes. Keep it in a cool bag until lunch.")
    reply = ("A sandwich or wrap with " + ", ".join(fillings[:3]) + ", fruit, something crunchy and "
             "a drink is a packed lunch in five minutes. Cook extra dinner and take the leftovers "
             "in a tub and it is quicker still.")
    if banned:
        return reply + " Keep it in a cool bag until lunch."
    return reply + " Keep anything with meat, fish, egg or dairy cold until you eat it."


FREEZER_KEEP = ("In the freezer, about 3 months for most things before the quality drops: raw "
                "meat and fish, cooked dishes, soup, stock, bread, cake, cheese and butter. A whole "
                "bird or a joint goes 6 months, blanched veg and fruit 6 to 12, and ice cream 2 to "
                "3. It stays safe long past that, just drier, so write the date on the bag. The "
                "fridge is much shorter: raw meat 1 to 2 days, cooked food 3 to 4.")


FREEZE_ANY = ("Most food freezes well for about 3 months: cool it fast, portion it into bags, press "
              "the air out and write the date on. Defrost in the fridge overnight rather than on the "
              "counter.")


HONEY_BABY = (
    "No honey at all before the first birthday: it can carry botulism spores that a baby's gut is "
    "too young to deal with, and heat does not destroy them, so cooked honey is out too. That "
    "covers honey in porridge, on a dummy or in a homemade cough remedy. From the first birthday it "
    "is fine, so a toddler or an older child can have it.")

HONEY_OLDER = (
    "From the first birthday honey is fine, so a toddler can have it in porridge or a warm drink - "
    "keep the spoon small and brush teeth afterwards, because it is sugar. The one rule is no honey "
    "at all under a year, and that includes cooked honey, because botulism spores survive heat.")


def _honey_age(memory, understood):
    text = understood.get("clean") or ""
    if re.search(r"\b(toddlers?|2 year old|3 year old|two year old|three year old)\b", text):
        return HONEY_OLDER
    return HONEY_BABY


_FREEZE_WORD_FORMS = ("freeze", "freezes", "freezing", "frozen", "freezer", "freezers",
                      "freezed", "freezed")
_FREEZE_POINTS_AT = ("it", "this", "that", "these", "those", "them", "the rest", "the other half",
                     "the remainder", "whats left", "what is left", "the spare", "some",
                     "any left", "any spare", "a portion", "the leftovers", "left over",
                     "the whole lot", "the remainder of it")


def _points_at_something(words):
    clean = [word.strip(".,!?").replace("'", "").lower() for word in words]
    for at in range(len(clean)):
        for size in (3, 2, 1):
            if " ".join(clean[at:at + size]) not in _FREEZE_POINTS_AT:
                continue
            for step in (-1, -2, size, size + 1):
                i = at + step
                if 0 <= i < len(clean) and clean[i] in _FREEZE_WORD_FORMS:
                    return True
    return False


def _freeze_units(words):
    units = list(words)
    for size in (2, 3):
        units += [" ".join(words[i:i + size]) for i in range(len(words) - size + 1)]
    return units


def _a_freeze_fact(words):
    best = None
    for names, fact in FREEZE_FACTS:
        for name in names:
            for at, word in enumerate(_freeze_units(words)):
                if _same(word, name):
                    score = (word == name, len(name.split()), at)
                    if best is None or score > best[0]:
                        best = (score, fact)
    return best[1] if best else None


_NOT_A_FREEZER = frozenset("""
    card cards account accounts subscription subscriptions membership phone credit file
    report reports score payment payments direct debit standing order
""".split())


def _names_one_food(words):
    seen = set()
    for names, fact in FREEZE_FACTS:
        for name in names:
            for at, unit in enumerate(_freeze_units(words)):
                if _same(unit, name):
                    seen.add(fact)
                    break
    return next(iter(seen)) if len(seen) == 1 else None


def _the_dish_the_chat_names(memory):
    try:
        from ..memory import recent
        turns = recent(memory, 4) or ()
    except Exception:
        return None
    for turn in reversed(list(turns)):
        if not isinstance(turn, dict):
            continue
        said = turn.get("user")
        if not isinstance(said, str) or not said.strip():
            continue
        fact = _names_one_food(said.lower().split())
        if fact is not None:
            return fact
    return None


def _freeze_food(memory, understood):
    words = understood.get("words")
    if not isinstance(words, list):
        words = " ".join(understood.get("words") or []).split()
    words = [str(word).lower() for word in words]
    if _NOT_A_FREEZER & {word.strip(".,!?\"'") for word in words}:
        return None
    fact = _a_freeze_fact(words)
    if fact is not None:
        return fact
    if not _points_at_something(words):
        return None
    earlier = _the_dish_the_chat_names(memory)
    if earlier is not None:
        return earlier
    return FREEZE_ANY


SOYA = frozenset("soya soy soya bean soy bean soya sauce tofu edamame".split())
ALSO_OUT = {
    "shellfish": "And nothing with shellfish in it either: prawns, crab, lobster, mussels, squid, "
                 "and check sauces and stocks for seafood.",
    "soya": "And nothing with soya in it either: tofu, edamame, soya sauce, and check the label "
            "on bread and chocolate.",
}


def _nut_free(memory, understood):
    banned = avoids(memory)
    if (GLUTEN | EGGS) & banned:
        return None
    also = [ALSO_OUT[name] for name in ("shellfish",) if FAMILIES[name] & banned]
    if SOYA & banned:
        also.append(ALSO_OUT["soya"])
    turns = memory.get("turns")
    recent = ""
    if isinstance(turns, list):
        recent = " ".join(str(turn.get("user") or "") for turn in turns[-2:]
                          if isinstance(turn, dict)).lower()
    if "cake" in recent or "bake" in recent or "birthday" in recent:
        return ("Then go for a plain chocolate sponge: cocoa, flour, eggs, butter and sugar, no "
                "nuts. Check the chocolate, the icing sugar and any sprinkles for 'may contain "
                "nuts', and keep the tin and worktop clean if the allergy is serious.")
    return ("Plenty: meat, fish, eggs, rice, pasta, potatoes and plain fruit and veg are all "
            "nut-free, so pasta with tomato sauce or roast chicken and potatoes works. Check the "
            "labels on chocolate, muesli, pesto and satay, and anything marked 'may contain "
            "nuts'." + (" " + " ".join(also) if also else ""))


_HAVE_NONE = ("havent any", "haven't any", "have got none", "have none", "has none", "got none",
              "there is no ", "there's no ", "there are no ", "none in the house",
              "none in the cupboard", "none at home", "none left at home",
              "nothing in the house", "nothing in the cupboard", "nothing in the fridge",
              "theres none", "there's none",
              "have no egg", "have no eggs", "have no milk", "have no butter", "have no yeast",
              "have no cream", "have no buttermilk", "have no cornflour", "have no flour",
              "have no plain flour", "have no baking powder", "have no sugar", "have no cheese",
              "have no rice", "have no onions", "have no bread")
_OUT_ASK = ("out of", "none left", "nothing left", "empty", "what do i do", "what do i use") \
    + _HAVE_NONE

def _vegan_bake(memory, understood):
    words = understood.get("words")
    if not isinstance(words, (list, tuple)):
        words = str(understood.get("clean") or "").split()
    folded = {_fold(word) for word in words}
    if folded & {_fold(one) for one in ("pancake", "pancakes", "crepe", "crepes", "waffle",
                                        "waffles", "drop scone")}:
        return ("Pancakes need no egg at all: 100g of plain flour, a teaspoon of baking powder, a "
                "pinch of salt and 300ml of unsweetened soya or oat milk, whisked and rested 20 "
                "minutes, then cooked in a little oil. The first one always fails, so make it the "
                "cook's. For thicker American ones, add a tablespoon of oil and a teaspoon of "
                "sugar.")
    if folded & {_fold(one) for one in ("scone", "scones", "drop scone", "drop scones")}:
        return ("Rub 50g of a hard vegan block margarine, or 40ml of neutral oil, into 225g of "
                "self-raising flour, then bring it together with about 120ml of unsweetened soya "
                "milk and a squeeze of lemon. Pat it out, cut the scones and bake at 220C for 12 "
                "to 15 minutes. The block margarine, not a tub spread, is what makes it short.")
    if folded & {_fold(one) for one in ("pastry", "shortcrust", "shortcrust pastry", "pie",
                                        "pie crust", "tart", "tarts", "tart case", "flan",
                                        "quiche", "quiche case")}:
        return ("Vegan shortcrust is the same weights with the fat swapped: 225g plain flour, a "
                "pinch of salt and 100g of a hard vegan block margarine (or 90ml of neutral oil), "
                "rubbed in until it looks like breadcrumbs, then cold water a spoon at a time until "
                "it just comes together. Rest it 30 minutes in the fridge, roll it thin on a floured "
                "board, and blind bake at 190C (170C fan) for 15 minutes for a tart or quiche case. "
                "Brush the top with plant milk rather than egg and it browns just as well.")
    if folded & {_fold(one) for one in ("crumble", "crumbles", "fruit crumble", "cobbler")}:
        return ("Swap the butter and nothing else changes: rub 100g of a hard vegan block "
                "margarine into 200g plain flour with 75g sugar until it looks like breadcrumbs, "
                "scatter it over the fruit and bake at 190C (170C fan) for 35 to 40 minutes, until "
                "the fruit bubbles at the edges and the top is golden.")
    if folded & {_fold(one) for one in ("biscuit", "biscuits", "cookie", "cookies",
                                        "shortbread")}:
        return ("Biscuits are the easiest bake to make vegan: a hard block margarine in place of "
                "the butter at the same weight, and a tablespoon of plant milk if the dough will "
                "not come together. No egg and no raising agent needed, so nothing else changes, "
                "and they keep a day or two less.")
    if folded & {_fold(one) for one in ("flapjack", "flapjacks", "oat bar", "oat bars",
                                        "granola bar", "granola bars")}:
        return ("A flapjack needs no egg, so the only swap is the butter: 150g of a hard vegan "
                "block margarine or 120ml of neutral oil with 120g of golden syrup is the sticky "
                "part. Melt them together, stir in 300g of porridge oats, press it into a lined "
                "20cm tin and bake at 180C (160C fan) for 20 to 25 minutes. Let it go completely "
                "cold in the tin or it will crumble when you cut it.")
    if (folded & {_fold(one) for one in ("bread", "loaf", "loaves", "roll", "rolls", "baguette",
                                         "focaccia", "pizza", "pizza dough", "flatbread", "naan")}
            and not folded & {_fold(one) for one in ("banana", "carrot", "courgette", "zucchini",
                                                     "apple", "date", "pumpkin", "lemon", "fruit",
                                                     "soda", "cake", "brioche", "challah")}):
        return ("Ordinary bread is vegan already: flour, water, yeast and salt, with oil or a hard "
                "block margarine where the recipe wants a fat, and sugar feeds the yeast without "
                "leaving any behind. Only an enriched loaf needs a swap - oil for the butter, plant "
                "milk for the milk, and golden syrup for the honey. Check a bought loaf, though: "
                "milk powder and dried egg turn up in cheap sliced bread and in brioche.")
    if folded & {_fold(one) for one in ("brownie", "brownies", "blondie", "blondies")}:
        return ("For brownies, two flax eggs do the job: a tablespoon of ground flaxseed and "
                "three of water each, left five minutes to go gluey. Use an oil-based or vegan "
                "block margarine for the butter and keep the oven 10C lower, because brownies are "
                "meant to come out fudgy and the flax makes them catch sooner.")
    return ("A cake takes three swaps: 60g of yoghurt or half a mashed banana, or a flax egg (a "
            "tablespoon of ground flaxseed and three of water, left five minutes), for each egg; "
            "unsweetened soya or oat milk for the milk; and a block margarine or 80g of neutral oil "
            "for every 100g of butter. Add an extra half teaspoon of baking powder, because the egg "
            "was doing some of the lifting, and give it five minutes longer in the oven. Soya milk "
            "browns best, and a sponge made this way keeps a day less.")


_VEGAN_ASK = ("vegan", "vegans", "plant based", "plant-based", "dairy free", "dairy-free",
              "dairyfree", "egg free", "egg-free", "eggless", "no egg", "no eggs", "no butter",
              "without butter", "no milk", "milk free", "milk-free")


def _asks_vegan(folded):
    said = " ".join(folded)
    return any(phrase in said for phrase in _VEGAN_ASK)


_SWAP_ASK = ("instead", "substitute", "swap", "replace", "replacement", "alternative",
             "without",
             "what can i use", "what do i use", "what should i use", "what else can i use",
             "ran out", "run out", "havent got", "haven't got", "dont have", "don't have",
             "im out of", "i'm out of", "were out of", "we're out of", "are out of",
             "im all out",
             "i'm all out", "out of stock of", "none of", "none left", "nothing left",
             "no longer have",
             *_HAVE_NONE,
             "egg free", "egg-free", "eggless", "no egg", "no eggs")

SUBSTITUTE_PHRASES = ("instead of", "in place of", "substitute", "swap ", "what can i use",
                      "what do i use", "ran out of", "run out of", "havent got", "haven't got",
                      "dont have", "don't have")

KEEPING = ("keep", "keeps", "keeping", "shelf life", "shelf-life", "last", "lasts",
           "safe", "still ok", "ok to eat",
           "gone off", "went off", "go off", "goes off", "going off", "off", "left out",
           "use by", "days", "how long",
           "reheat", "reheating", "warmed up")

COOK_VERBS = ("boil", "boiling", "boiled", "roast", "roasting", "roasted", "steam", "steaming",
              "steamed", "fry", "frying", "fried", "bake", "baking", "baked", "microwave",
              "grill", "grilling", "grilled", "parboil", "poach", "poaching", "simmer",
              "simmering", "air fry", "air-fry", "in the oven", "on the hob", "blanch")

STORAGE = ("keep", "keeps", "keeping", "shelf life", "shelf-life", "fridge", "freezer",
           "freeze", "frozen", "refreeze",
           "refreezing", "reheat", "reheating", "reheated", "last", "lasts",
           "left out", "use by", "gone off", "go off", "goes off", "going off",
           "still ok", "ok to eat", "safe")




NUTRIENT_COLUMNS = {
    "protein": ("protein", "protein"),
    "carbs": ("carbs", "carbohydrate"),
    "sugar": ("sugar", "sugar"),
    "fat": ("fat", "fat"),
    "fibre": ("fibre", "fibre"),
    "iron": ("mg", "iron"),
    "calcium": ("mg", "calcium"),
    "potassium": ("mg", "potassium"),
    "salt": ("g", "salt"),
}

NUTRIENT_CONTEXT = {
    "iron": "Women need about 15mg a day and men about 9mg, and the iron in plants and grains "
            "is taken up better with something containing vitamin C.",
    "calcium": "Adults need about 700mg a day.",
    "potassium": "The target is about 3,500mg a day.",
    "salt": "The daily limit is 6g, and bread, cheese and cured meat are where most of it hides.",
}

_MINERALS = ("iron", "calcium", "potassium", "salt")

_NUTRIENT_WORDS = (
    ("carbohydrates", "carbs"), ("carbohydrate", "carbs"), ("carbs", "carbs"), ("carb", "carbs"),
    ("protein", "protein"), ("proteins", "protein"),
    ("saturated fat", "fat"), ("saturates", "fat"), ("fat", "fat"), ("fats", "fat"),
    ("sugar", "sugar"), ("sugars", "sugar"),
    ("fibre", "fibre"), ("fiber", "fibre"),
    ("iron", "iron"), ("calcium", "calcium"), ("potassium", "potassium"),
    ("salt", "salt"), ("salty", "salt"),
)

_NUTRIENT_ASK_WORDS = (tuple(word for word, _column in _NUTRIENT_WORDS)
                       + ("calorie", "calories", "cals", "kcal", "kilocalories", "nutrition"))

_NUTRIENT_DISH = ("bread", "cake", "pie", "tart", "muffin", "sauce", "soup", "sandwich", "wrap",
                  "curry", "salad", "smoothie", "juice", "pudding", "jam", "chips", "butter",
                  "cheese", "cream", "biscuit", "cereal", "porridge", "pasta", "rice", "pizza",
                  "stew", "casserole", "roast", "bake", "baked", "fried", "milkshake",
                  "flapjack", "brownie", "cookie", "pancake", "waffle", "toast", "milk", "sugar",
                  "flour", "crisps", "chocolate", "yoghurt", "yogurt", "egg", "nuts", "peanut",
                  "roll", "rolls", "burger", "burgers", "bun", "buns", "pastry", "puff")
_NUTRIENT_JOIN = ("and", "with", "plus")


_COUNT_WORDS = {"one": 1, "1": 1, "two": 2, "2": 2, "three": 3, "3": 3, "four": 4, "4": 4,
                "five": 5, "5": 5, "six": 6, "6": 6, "seven": 7, "7": 7, "eight": 8, "8": 8,
                "nine": 9, "9": 9, "ten": 10, "10": 10}


def _plurals(word):
    if not word.isalpha() or word.endswith("s"):
        return word
    if word.endswith(("ch", "sh", "ss", "x", "z")):
        return word + "es"
    if word in ("potato", "tomato", "hero"):
        return word + "es"
    if word.endswith("y") and word[-2:-1] not in "aeiou":
        return word[:-1] + "ies"
    return word + "s"


def _portion_count(words, index):
    back = words[max(0, index - 4):index]
    said = " ".join(back)
    if said.endswith("a couple of") or said.endswith("couple of"):
        return 2
    if said.endswith("a few"):
        return 3
    if said.endswith("half a") or said.endswith("half an"):
        return 0.5
    for word in reversed(back):
        if word in _COUNT_WORDS:
            return _COUNT_WORDS[word]
    return 1


def _squashed(word):
    return re.sub(r"(.)\1+", r"\1", word)


def _one_letter_apart(short, long):
    index = 0
    while index < len(short) and short[index] == long[index]:
        index += 1
    return short[index:] == long[index + 1:]


def _the_food_named_by_a_slip(words, table):
    for index, word in enumerate(words):
        name = _a_food_word_misspelt(word, table)
        if name is None:
            continue
        before = words[index - 1] if index else None
        after = words[index + 1] if index + 1 < len(words) else None
        if after and (after in _NUTRIENT_DISH or after in _NUTRIENT_JOIN):
            return None
        if before and before in _NUTRIENT_JOIN:
            return None
        return name, _portion_count(words, index)
    return None


def _a_food_word_misspelt(word, names):
    if len(word) < 5 or not word.isalpha():
        return None
    if word in names:
        return None
    squashed = _squashed(word)
    for name in names:
        if " " in name or len(name) < 5 or name[0] != word[0]:
            continue
        if len(name) == len(word):
            if squashed == _squashed(name):
                return name
            if name[-1] == word[-1] and sum(one != other for one, other in zip(word, name)) == 1:
                return name
        elif abs(len(name) - len(word)) == 1 and name[-1] == word[-1]:
            shorter, longer = sorted((word, name), key=len)
            if _one_letter_apart(shorter, longer):
                return name
    return None


def _nutrient_food(clean, table):
    matches = [food for food in table
               if re.search(r"(?<![a-z0-9])" + re.escape(food) + r"s?(?![a-z0-9])", clean)]
    words = re.findall(r"[a-z0-9']+", clean)
    if not matches:
        return _the_food_named_by_a_slip(words, table)
    best = max(matches, key=len)
    if any(food not in best and food.rstrip("s") not in best
           and _plurals(food) not in best for food in matches):
        return None
    parts = best.split()
    for index in range(len(words) - len(parts) + 1):
        chunk = words[index:index + len(parts)]
        if chunk[:-1] != parts[:-1]:
            continue
        if chunk[-1] != parts[-1] and chunk[-1] != _plurals(parts[-1]):
            continue
        before = words[index - 1] if index else None
        after = words[index + len(parts)] if index + len(parts) < len(words) else None
        if after and (after in _NUTRIENT_DISH or after in _NUTRIENT_JOIN):
            return None
        if before and before in _NUTRIENT_JOIN:
            return None
        return best, _portion_count(words, index)
    return None


def _nutrient_asked(clean):
    for word, column in _NUTRIENT_WORDS:
        if re.search(r"(?<![a-z0-9])" + re.escape(word) + r"(?![a-z0-9])", clean):
            return column
    return None


_PROTEIN_SHARES = ((0.8, "most"), (0.5, "half"), (0.3, "a third"), (0.22, "a quarter"),
                   (0.18, "a fifth"), (0.08, "a tenth"))


def _grams(value):
    if value <= 0:
        return None
    if value < 1:
        return "under a gram"
    if float(value) == int(value):
        return "%d" % int(value)
    return ("%.1f" % value).rstrip("0").rstrip(".")


_WEIGHT_WORDS = (("kilograms?|kg", 1000.0, "g"), ("grammes?|grams?|g", 1.0, "g"),
                 ("millilitres?|milliliters?|ml", 1.0, "ml"), ("centilitres?|cl", 10.0, "ml"),
                 ("litres?|liters?|l", 1000.0, "ml"), ("pints?", 568.0, "ml"))

_AMOUNT_ASKED = re.compile(r"\d|\b(?:half|quarter|dozen|pints?|litres?|liters?|bowls?|plates?|"
                           r"glasses?|mugs?|cups?|slices?|pieces?|portions?|servings?|tins?|"
                           r"spoons?|tablespoons?|teaspoons?)\b")


def _portion_size(portion):
    found = re.search(r"(\d+(?:\.\d+)?)\s*(g|ml)\b", str(portion).lower())
    return (float(found.group(1)), found.group(2)) if found else None


def _weight_in_the_line(clean, portion):
    base = _portion_size(portion)
    if base is None:
        return None
    for pattern, scale, unit in _WEIGHT_WORDS:
        found = re.search(r"(\d+(?:\.\d+)?)\s*(?:" + pattern + r")\b", clean)
        if found and base[1] == unit:
            return float(found.group(1)) * scale / base[0], found.group(0)
    if base[1] == "ml":
        found = re.search(r"\b(half a pint|a pint|one pint)\b", clean)
        if found:
            many = 0.5 if found.group(1).startswith("half") else 1.0
            return many * 568.0 / base[0], found.group(1)
    return None


def _figure(value):
    if value >= 10:
        return "%d" % int(round(value))
    return ("%.1f" % value).rstrip("0").rstrip(".")


def _nutrients(memory, understood):
    clean = (understood.get("clean") or "").lower()
    if not clean:
        return None
    plain = (understood.get("plain") or "").lower()
    if plain == clean:
        plain = ""
    column = _nutrient_asked(clean)
    read = clean
    if column is None and plain:
        column = _nutrient_asked(plain)
        read = plain if column is not None else clean
    if column is None:
        return None
    found = _nutrient_food(read, FOOD_NUTRIENTS)
    if found is None and plain:
        found = _nutrient_food(plain if read == clean else clean, FOOD_NUTRIENTS)
    if found is None:
        return None
    food, count = found
    subject, portion, numbers = FOOD_NUTRIENTS[food]
    if column not in numbers:
        return None
    value = numbers[column] * count
    scaled, said_amount = None, None
    if count == 1:
        weighed = _weight_in_the_line(clean, portion)
        if weighed is not None:
            scaled, said_amount = weighed
            if abs(scaled - 1.0) < 0.01:
                scaled = None
        elif _portion_size(portion) is None:
            for word in _AMOUNT_ASKED.findall(clean):
                if not word:
                    return None
                if word in portion.lower() or _plurals(word) in portion.lower():
                    continue
                if word in subject.lower() or _plurals(word) in subject.lower():
                    continue
                return None
    said = subject[:1].upper() + subject[1:]
    if count > 1:
        pieces = said.split()
        if pieces[0] in ("A", "An"):
            pieces = pieces[1:]
        head = pieces.index("of") - 1 if "of" in pieces else len(pieces) - 1
        pieces[head] = _plurals(pieces[head])
        said = ("%g " % count if count != int(count) else
                {2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight",
                 9: "Nine", 10: "Ten"}.get(int(count), str(int(count)))) + " " + " ".join(pieces)
        subject = said
        portion = ""
    name = NUTRIENT_COLUMNS[column][1]
    unit = "mg" if column in ("iron", "calcium", "potassium") else "g"
    plural = count > 1 or food in _CALORIE_PLURAL or subject[:2] not in ("a ", "an", "A ", "An ")
    if scaled:
        said = said_amount[:1].upper() + said_amount[1:]
        if food not in said.lower():
            said += " of " + food
        value *= scaled
    amount = _figure(value) if value else None
    if amount is None:
        sentence = "%s %s no %s to speak of" % (said, ("have" if plural else "has"), name)
    else:
        sentence = ("%s %s about %s%s of %s" % (said, ("have" if plural else "has"), amount,
                                                unit, name))
    if portion and portion != "one" and not scaled and portion.lower() not in said.lower():
        sentence += " (%s)" % portion
    sentence += "."
    if column == "protein" and value:
        if value >= 50:
            sentence += " That is more protein than an adult needs in a day."
        else:
            for share, word in _PROTEIN_SHARES:
                if value / 50.0 >= share:
                    hedge = "" if word == "most" else "about "
                    sentence += (" That is %s%s of a day's protein for an adult."
                                 % (hedge, word))
                    break
    if column in NUTRIENT_CONTEXT:
        sentence += " " + NUTRIENT_CONTEXT[column]
    return sentence


_CALORIE_PLURAL = ("strawberries", "grapes", "chips", "crisps", "peanuts")

_CALORIE_NOT_A_DISH = ("dough", "base", "bases", "recipe", "homemade", "home made")

CALORIE_ASKS = ("calorie", "calories", "cals", "kcal", "kilocalories",
                "how many calories")

_CALORIE_OWN = ("chicken breast", "chicken breasts")

_CALORIE_DISH = ("bread", "cake", "pie", "tart", "muffin", "sauce", "soup", "sandwich", "wrap",
                 "curry", "salad", "smoothie", "juice", "pudding", "jam", "crisps", "chips",
                 "butter", "cheese", "cream", "biscuit", "cereal", "porridge", "pasta", "rice",
                 "pizza", "stew", "casserole", "roast", "bake", "baked", "fried", "milkshake",
                 "flapjack", "brownie", "cookie", "pancake", "waffle", "toast", "milk", "sugar",
                 "roll", "rolls", "burger", "burgers", "bun", "buns", "pastry", "puff")
_CALORIE_JOIN = ("and", "with", "plus")


def _names_a_food(line):
    lowered = line.lower()
    for table in (FOOD_CALORIES, FOOD_CALORIE_MEALS, FOOD_NUTRIENTS):
        for name in table:
            if name and name in lowered:
                return True
    return False


def _calories(memory, understood):
    clean = understood.get("clean") or ""
    plain = understood.get("plain") or ""
    if plain and plain != clean and not _names_a_food(clean):
        clean = plain
    if not any(word in clean for word in CALORIE_ASKS):
        return None
    if any(food in clean for food in _CALORIE_OWN):
        return None
    if any(re.search(r"(?<![a-z0-9])" + re.escape(word) + r"(?![a-z0-9])", clean)
           for word in _CALORIE_NOT_A_DISH):
        return None
    words = re.findall(r"[a-z0-9']+", clean)

    def _part_of_a_dish(name):
        tail = name.split()[-1]
        for i, word in enumerate(words):
            if word == tail:
                after = words[i + 1] if i + 1 < len(words) else None
                return after in _CALORIE_DISH
        return False

    meal = None
    for dish in sorted(FOOD_CALORIE_MEALS, key=len, reverse=True):
        if _part_of_a_dish(dish):
            continue
        if re.search(r"(?<![a-z0-9])" + re.escape(dish) + r"(?![a-z0-9])", clean):
            meal = dish
            break
    if meal:
        subject, portion, count = FOOD_CALORIE_MEALS[meal]
        said = subject[:1].upper() + subject[1:]
        return f"{said} is about {count} calories ({portion})."
    matches = [food for food in FOOD_CALORIES
               if re.search(r"(?<![a-z0-9])" + re.escape(food) + r"s?(?![a-z0-9])", clean)]
    if not matches:
        slipped = _the_food_named_by_a_slip(words, FOOD_CALORIES)
        if slipped is None:
            return None
        matches = [slipped[0]]
    best = max(matches, key=len)
    if any(food not in best for food in matches):
        return None
    head, tail = best.split()[0], best.split()[-1]
    before = after = None
    for i, word in enumerate(words):
        if word == tail:
            after = words[i + 1] if i + 1 < len(words) else None
            back = i - len(best.split()) + 1
            before = words[back - 1] if back >= 1 else None
    if after and (after in _CALORIE_DISH or after in _CALORIE_JOIN):
        return None
    if before and before in _CALORIE_JOIN:
        return None
    subject, portion, count = FOOD_CALORIES[best]
    said = subject[:1].upper() + subject[1:]
    verb = "are" if best in _CALORIE_PLURAL and subject[:2] not in ("a ", "an") else "is"
    return f"{said} {verb} about {count} calories ({portion})."


GLUTEN_FREE_ASKS = ("gluten free", "gluten-free", "glutenfree", "without gluten", "no gluten",
                    "free from gluten", "wheat free", "wheat-free", "without wheat", "no wheat",
                    "gluten allergy", "coeliacs", "coeliac", "contain gluten",
                    "contains gluten",
                    "gluten and dairy free", "dairy and gluten free", "gluten and egg free",
                    "egg and gluten free", "gluten and dairy-free", "dairy-free and gluten-free")

GLUTEN_FREE_DISHES = ("make", "making", "made", "bake", "baking", "baked", "cook", "cooking",
                      "recipe", "version", "instead", "cake", "cakes", "sponge", "brownie",
                      "brownies", "cookie", "cookies", "muffin", "muffins", "biscuit",
                      "biscuits", "bread", "loaf", "loaves", "roll", "rolls", "pastry",
                      "shortcrust", "scone", "scones", "pancake", "pancakes", "batter",
                      "flour", "pasta", "spaghetti", "noodles", "macaroni", "lasagne",
                      "how do i", "can i", "how can i")

_GLUTEN_FREE_SKIP = ("gravy", "porridge", "sauce", "soup", "curry", "stew", "casserole", "stock",
                     "marinade", "dressing", "coating", "roux", "thicken", "thickening",
                     "yorkshire", "shortbread", "beer", "lager", "ale", "cider", "wine", "what can i eat", "what can i cook",
                     "what should i eat", "what can i have", "meal", "meals", "dinner", "lunch",
                     "snack", "ideas", "what to eat", "taste", "tastes", "tasting", "healthier",
                     "better for you", "good for you", "worth it", "is it bad", "lose weight",
                     "how do i know", "do i have", "have i got", "diagnosed", "diagnosis",
                     "symptoms", "signs", "blood test", "test for", "contagious", "curable",
                     "cause", "causes", "anaemia", "underactive", "deficiency")


_GLUTEN_MAKING = ("make", "making", "bake", "baking", "cook", "cooking", "recipe", "version",
                  "how do i", "how can i", "how to")


def _gluten_free(memory, understood):
    clean = understood.get("clean") or ""
    folded = " " + re.sub(r"[^a-z0-9 ]+", " ", clean.lower()) + " "
    if (re.match(r"(is|are|does|do|can|should)\b", clean)
            and not any(" %s " % word in folded for word in _GLUTEN_MAKING)):
        return ("Not the ordinary one: wheat flour is what bread, pasta, cakes and most biscuits "
                "are made from, so unless the packet says gluten free it is not. A gluten-free "
                "loaf is a different product rather than the same loaf without something in it, "
                "and check the label for 'may contain wheat' on sauces, stock and chips.")
    if any(" %s " % word in folded for word in ("bread", "loaf", "loaves", "roll", "rolls",
                                                "baguette", "pizza", "naan", "focaccia")):
        return ("Buy this one rather than bake it: a gluten-free loaf needs a batter, not a dough, "
                "plus psyllium or xanthan to stand in for the stretch, and it is the one thing a "
                "shop does better. For a bun or a pizza base, a gluten-free bread flour blend "
                "with a teaspoon of xanthan per 500g and a wet dough, proved in the tin, gets "
                "there.")
    if any(" %s " % word in folded for word in ("pasta", "spaghetti", "penne", "macaroni",
                                                "lasagne", "noodles")):
        return ("Buy it: dried pasta made from corn, rice or buckwheat is the one gluten-free swap "
                "that works, and the fresh gluten-free pasta in the chiller is better still. Cook "
                "it in plenty of salted water and taste a minute before the packet says, because "
                "it goes from firm to mushy quickly, and dress it straight away - it does not "
                "wait like wheat pasta does.")
    if any(" %s " % word in folded for word in ("pastry", "shortcrust", "tart", "pie", "quiche",
                                                "flan", "crust")):
        return ("Gluten-free shortcrust: 200g of a gluten-free plain flour blend with half a "
                "teaspoon of xanthan gum, 100g of cold butter rubbed in, then a beaten egg or a "
                "few spoons of iced water to bring it together. Rest it 30 minutes in the fridge "
                "and roll it between two sheets of baking paper, because it tears. It needs no "
                "blind-bake change: 15 minutes at 190C (170C fan).")
    said = ("A gluten-free bake needs a blend, not one flour: a shop gluten-free plain flour blend "
            "with a quarter teaspoon of xanthan gum per 200g, and a splash more liquid than the "
            "recipe says, because there is no stretch in it to hold water. Let the batter stand "
            "20 minutes before it goes in the oven and it stops tasting gritty. Expect it to "
            "brown faster, so drop the oven 10C and give it five minutes longer.")
    if any(" %s " % word in folded for word in ("dairy", "milk", "butter", "cheese", "yoghurt",
                                                "yogurt", "vegan", "plant")):
        said += (" For the dairy, unsweetened soya or oat milk goes in one for one, and a hard "
                 "dairy-free block margarine replaces the butter at the same weight.")
    return said


GLUTEN_FACT_DIET = ("gluten allergy", "coeliacs", "coeliac")
GLUTEN_FACT_ASKS = tuple(
    [ask for ask in GLUTEN_FREE_ASKS if ask not in GLUTEN_FACT_DIET]
    + ["free of gluten", "gluten in it", "have gluten", "has gluten", "contain wheat"])
GLUTEN_FACT_FOODS = tuple(sorted(MADE_OF))
GLUTEN_FACT_SWAPS = frozenset(
    "bread toast pasta spaghetti noodles couscous pastry cake cakes biscuit biscuits cracker "
    "crackers pitta flour crumpet bagel wrap wraps barley rye semolina scone scones pizza "
    "sandwich".split())
GLUTEN_FACT_NAMED_SWAP = {
    "soy sauce": "Tamari is made without wheat and tastes the same.",
    "soya sauce": "Tamari is made without wheat and tastes the same.",
}


GLUTEN_FACT_NOT_PLAIN = {
    "sausage": ("Usually not: most sausages have rusk in them, which is bread, so look for the "
                "ones marked gluten free."),
    "sausages": ("Usually not: most sausages have rusk in them, which is bread, so look for the "
                 "ones marked gluten free."),
    "chips": ("Not always: chips from a chip shop are sometimes dusted with flour, so ask there "
              "and read the packet on oven chips."),
}
GLUTEN_FACT_OPENING = re.compile(
    r"^\s*(?:is|are|does|do|did|can|could|should|would|will|was|were|has|have)\b", re.I)
GLUTEN_FACT_MAKING = re.compile(
    r"\b(?:make|makes|making|bake|bakes|baking|cook|cooks|cooking|recipe|recipes|how do i|"
    r"how can i|how to|homemade|from scratch)\b", re.I)


def asks_a_gluten_fact(understood):
    if not isinstance(understood, dict):
        return False
    clean = understood.get("clean") or ""
    if not GLUTEN_FACT_OPENING.match(clean):
        return False
    lowered = clean.lower()
    if not any(ask in lowered for ask in GLUTEN_FACT_ASKS):
        return False
    food = _food_named(clean)
    if food is None:
        return False
    return not GLUTEN_FACT_MAKING.search(lowered.replace(food, " "))


def _free_of_gluten_fact(memory, understood):
    clean = understood.get("clean") or ""
    if not GLUTEN_FACT_OPENING.match(clean):
        return ""
    food = _food_named(clean)
    if food is None:
        return ""
    if GLUTEN_FACT_MAKING.search(clean.lower().replace(food, " ")):
        return ""
    if food in GLUTEN_FACT_NOT_PLAIN:
        return GLUTEN_FACT_NOT_PLAIN[food]
    phrase = r"\s+".join(re.escape(part) for part in food.split())
    if re.search(r"\b(?:[a-z]+)\s+free\s+" + phrase + r"\b", clean.lower()):
        return ""
    named = _named_as(clean, food)
    plural = _is_plural(food)
    if GLUTEN & MADE_OF[food]:
        said = "are made with wheat flour" if plural else "is made with wheat flour"
        reply = "No: " + named + " " + said + ", so it is not gluten free."
        if food in GLUTEN_FACT_NAMED_SWAP:
            return reply + " " + GLUTEN_FACT_NAMED_SWAP[food]
        if food in GLUTEN_FACT_SWAPS:
            swap = FAMILY_SAY[id(GLUTEN)][1]
            return reply + " " + swap[:1].upper() + swap[1:] + "."
        return reply + " The gluten-free one is a different product, so check the label."
    if food in NOT_SETTLED_BY_THE_RECIPE:
        return NOT_SETTLED_BY_THE_RECIPE[food]
    if plural:
        return ("Yes: " + named + " have no gluten in them. The plain ones are gluten free; "
                "check the packet on flavoured or own-brand versions.")
    return ("Yes: " + named + " has no gluten in it. The plain one is gluten free; check the "
            "packet on flavoured or own-brand versions.")


_SWAP_VERDICTS = (
    (("yoghurt", "yogurt", "greek yoghurt", "greek yogurt"),
     ("cream", "double cream", "single cream", "creme fraiche"),
     "Yes, in anything cold or stirred in at the end: spoon it in off the heat, because yoghurt "
     "splits if it boils. It will not whip and it will not thicken a sauce the way cream does."),
    (("cornflour", "corn starch", "cornstarch"),
     ("plain flour", "self-raising flour", "self raising flour", "flour"),
     "Not in baking: cornflour has no gluten, so a cake or a loaf will not hold or rise. As a "
     "thickener it works, at one tablespoon where the recipe asks for two of plain flour, mixed "
     "into cold liquid first."),
    (("oil", "olive oil", "vegetable oil", "sunflower oil", "rapeseed oil"),
     ("butter", "margarine"),
     "In cakes, yes: use 80g of oil for every 100g of butter, and expect a slightly denser crumb. "
     "Not in pastry or shortbread, and not where you cream butter and sugar for air."),
    (("honey",),
     ("sugar",),
     "Yes, at three-quarters of the weight, and take a tablespoon or two out of the liquid. Bake "
     "10C cooler than the recipe says, because honey browns faster than sugar."),
    (("frozen peas", "frozen sweetcorn", "frozen veg", "frozen vegetables"),
     ("fresh", "fresh peas", "fresh vegetables"),
     "Yes, straight from the bag with no thawing: give them a minute or two longer in the pan. "
     "Frozen peas are sweeter than fresh ones that have sat about."),
    (("stock cube", "stock cubes", "bouillon", "stock powder", "stock pot", "stock pots"),
     ("stock", "chicken stock", "beef stock", "vegetable stock"),
     "Yes: one cube per 500ml of water for a stock-strength base, and half a cube in a small or "
     "already salty dish. Crumble it in rather than dropping it whole."),
    (("margarine",),
     ("butter",),
     "Yes in cakes and biscuits, at the same weight, if it is a block margarine meant for baking. "
     "The soft spread in a tub holds more water and gives a wetter, paler bake."),
    (("bicarbonate of soda", "bicarb", "baking soda"),
     ("baking powder",),
     "Not on its own: bicarbonate is about four times stronger than baking powder and needs an "
     "acid to work. Use a quarter of a teaspoon of bicarbonate with a teaspoon of lemon juice or "
     "vinegar in place of each teaspoon of baking powder."),
    (("evaporated milk",),
     ("cream", "double cream", "single cream"),
     "Yes for cooking, sauces and coffee: it will not whip, but it will not split in a hot sauce "
     "either, so it is the safer one to keep in the cupboard."),
)



LACKS = (
    ("oven", ("no oven", "without an oven", "dont have an oven", "don't have an oven", "no ovens",
              "oven is broken", "oven's broken", "ovens broken", "oven doesnt work",
              "oven doesn't work", "just a hob", "only a hob", "hob only", "no cooker",
              "no stove", "only a microwave", "just a microwave", "microwave only",
              "no grill", "without a grill", "only have a microwave", "only got a microwave",
              "just have a microwave", "just got a microwave", "only have the hob",
              "only got a hob", "only have one hob", "no oven at home", "broken oven",
              "oven broke", "oven packed in", "no working oven", "oven isnt working",
              "oven is not working", "oven has broken",
              "oven has packed in", "ovens packed in", "oven packed up", "oven has packed up",
              "oven conked out", "oven has conked out", "oven died", "oven has died",
              "oven is dead", "oven broke down", "oven has broken down", "oven has broke",
              "oven stopped working", "oven has stopped working", "oven is on the blink",
              "oven has gone", "oven is gone", "oven has had it", "oven is knackered",
              "oven not heating", "oven isnt heating", "oven won't heat", "oven wont heat",
              "no oven space", "ova has gone")),
    ("hob", ("no hob", "without a hob", "no cooker", "no stove", "only a microwave",
             "only got a kettle", "only have a kettle", "just a kettle", "only the kettle",
             "just a microwave", "microwave only", "no rings", "no burners",
             "only have a microwave", "only got a microwave", "just have a microwave",
             "only have the microwave")),
    ("microwave", ("no microwave", "without a microwave")),
    ("freezer", ("no freezer", "without a freezer", "no room in the freezer")),
    ("kettle", ("no kettle", "without a kettle")),
)

REQUIRES = {
    "oven": ("oven", "roast", "roasting", "roasted", "bake", "baking", "baked", "grill",
             "grilled", "traybake", "tray bake", "casserole", "190c", "200c", "180c", "220c",
             "160c", "170c", "210c", "230c", "fan oven"),
    "hob": ("fry", "fried", "frying", "pan", "simmer", "boil", "boiling", "saucepan", "hob",
            "stir fry", "stir-fry", "poach", "steam", "griddle"),
    "microwave": ("microwave", "microwaved"),
    "freezer": ("freezer", "freeze", "frozen", "defrost"),
}


LACK_HEADS = ("dont have", "don't have", "do not have", "doesnt have", "doesn't have", "didnt have",
              "didn't have", "havent got", "haven't got", "hasnt got", "hasn't got",
              "have not got", "has not got", "not got", "got no", "no longer have")
LACK_NOUNS = {"oven": ("an oven", "a oven", "oven"), "hob": ("a hob", "hob"),
              "microwave": ("a microwave", "microwave"), "freezer": ("a freezer", "freezer"),
              "kettle": ("a kettle", "kettle")}
LACK_SAID = tuple((name, head + " " + noun)
                  for name, nouns in LACK_NOUNS.items()
                  for head in LACK_HEADS for noun in nouns)

LACK_ATTACHED = ("thermometer", "gloves", "glove", "mitt", "mitts", "tray", "dish", "rack",
                 "shelf", "light", "bulb", "door", "liner", "paper", "foil", "bag", "bags")


def _says_gone(phrases, segments):
    for segment in segments:
        for phrase in phrases:
            for found in re.finditer(re.escape(phrase), segment):
                after = segment[found.end():].strip().split(" ", 1)[0].strip(".,!?;:")
                if after not in LACK_ATTACHED:
                    return True
    return False


def _line(understood):
    return (((understood or {}).get("clean") or "") + " "
            + ((understood or {}).get("norm_text") or "")).lower()


def missing(understood):
    text = _line(understood)
    segments = text.split("|")
    gone = set()
    for name, phrases in LACKS:
        if _says_gone(phrases, segments):
            gone.add(name)
    for name, phrase in LACK_SAID:
        if name not in gone and _says_gone((phrase,), segments):
            gone.add(name)
    return gone


TURNS_DOWN = ("no", "not", "without", "nothing", "never", "needs none", "free")

DECIDING = ("repair", "repairing", "replace", "replacing", "mend", "mending", "fix", "fixing",
            "service", "servicing", "quote", "quotes", "scrap", "scrapping", "engineer",
            "warranty", "guarantee", "call-out")


def _sentences(text):
    return [one for one in re.split(r"(?<=[.!?;:])\s+|\n+", text) if one.strip()]


def unusable(text, understood):
    gone = missing(understood)
    if not gone or not isinstance(text, str) or not text.strip():
        return False
    clean = str(understood.get("clean") or "").lower()
    if any(phrase in clean for phrase in EMPTY_ASK_PHRASES):
        return False
    words = set()
    for name in gone:
        words.update(REQUIRES.get(name, ()))
    for sentence in _sentences(text.lower()):
        for word in words:
            if not re.search(r"\b" + re.escape(word) + r"\b", sentence):
                continue
            if any(one in sentence.split() for one in TURNS_DOWN):
                continue
            if any(one in sentence for one in DECIDING):
                continue
            return True
    return False


NO_OVEN = (
    "With a hob you can still eat well: pasta with a sauce made in the pan, rice with stir-fried "
    "veg and an egg on top, a one-pan curry of chickpeas or lentils with tomatoes, quesadillas or "
    "toasted sandwiches pressed in a dry pan, or potatoes boiled and then crushed into a pan with "
    "butter and greens. Eggs, tinned fish and beans all cook in a pan in minutes.")

NO_HOB = (
    "With only a microwave you can still eat properly: jacket potatoes (10 minutes, turned once), "
    "rice or pasta cooked in a big bowl of water, porridge, scrambled eggs, steamed frozen veg, "
    "tinned soup or beans, and a poached egg in a mug of water. Give a jacket potato a rub of oil "
    "and salt first and it comes out closer to oven-baked.")

NO_BAKING = (
    "You cannot bake without an oven, but a fridge cake needs none: melt 100g butter, 200g "
    "chocolate and 2 tablespoons of golden syrup in a pan, stir in 200g crushed biscuits and a "
    "handful of raisins, press it into a tin and chill it for 2 hours. A cheesecake that sets in "
    "the fridge, tiramisu and lemon posset are the same trick: they set cold, not in the oven.")

_GRIDDLE_DOUGH = ("scone", "scones", "drop scone", "drop scones", "pikelet", "pikelets",
                  "chapati", "chapatis", "chapatti", "chapattis", "roti", "rotis")
_GRIDDLE_BATTER = ("pancake", "pancakes", "crumpet", "crumpets", "pikelet", "pikelets")
_GRIDDLE_WARM = ("wrap", "wraps", "tortilla", "tortillas", "pitta", "pittas", "pita", "pitas")
GRIDDLE_BAKES = re.compile(
    r"\b(?:" + "|".join(_GRIDDLE_DOUGH + _GRIDDLE_BATTER + _GRIDDLE_WARM) + r")\b", re.I)
GRIDDLE_DOUGH = re.compile(r"\b(?:" + "|".join(_GRIDDLE_DOUGH) + r")\b", re.I)
GRIDDLE_BATTER = re.compile(r"\b(?:" + "|".join(_GRIDDLE_BATTER) + r")\b", re.I)

_GRIDDLE_TAIL = ("What will not work on a hob is anything that has to rise and brown in a tin - a "
                 "sponge, a loaf, pastry - and those are the no-bake answers instead.")


def _griddle_answer(said):
    text = str(said or "").lower()
    batter = GRIDDLE_BATTER.search(text)
    if batter:
        return ("A " + batter.group(0).rstrip("s") + " is a pan job as it is: the batter goes into a "
                "hot non-stick pan with a little butter, about a minute a side until bubbles pop and "
                "the edges set. Crumpets want rings in a dry pan on a low heat until the top sets and "
                "the holes stay open. " + _GRIDDLE_TAIL)
    dough = GRIDDLE_DOUGH.search(text)
    if dough:
        name = dough.group(0)
        if name.rstrip("s") not in ("scone", "drop scone", "pikelet"):
            return ("A " + name.rstrip("s") + " cooks in a heavy dry pan, not a tin: the same dough "
                    "made a little thicker and patted out, about 5 minutes a side on a low heat "
                    "with a lid on, until the middle is set and the edges have caught. Scones, "
                    "pikelets and roti are the same trick. " + _GRIDDLE_TAIL)
        return ("A scone cooks in a heavy pan: the same dough made a little thicker and patted out, "
                "in a dry pan on a low heat with a lid on for about 5 minutes a side, until the "
                "middle is set and the edges have caught. Drop scones, pikelets, chapatis and roti "
                "are the same trick on a hot dry pan. " + _GRIDDLE_TAIL)
    warm = re.search(r"\b(?:wrap|wraps|tortilla|tortillas|pitta|pittas|pita|pitas)\b", text)
    named = warm.group(0).rstrip("s") if warm else "wrap"
    other = "and a wrap warms the same way" if named.startswith("pitt") else "and a pitta puffs the same way"
    return ("A " + named + " is warmed rather than baked: 30 seconds a side in a dry hot pan and it "
            "is soft enough to fold, " + other + ". " + _GRIDDLE_TAIL)


NO_OVEN_BREAD = (
    "Bread with no oven is flatbread: flour, water, salt and a little oil, rested 20 minutes, "
    "rolled thin and cooked in a dry hot pan for two minutes a side. The same dough pushed into a "
    "hot oiled frying pan, lid on, turned once, makes a thick loaf that will do for toast.")

NO_KETTLE = (
    "A kettle still makes a real meal out of couscous: put it in a bowl, pour boiling water over "
    "to just cover it, cover the bowl for five minutes, then fork it through with tinned "
    "chickpeas or tuna, chopped tomato, olives and lemon. Overnight oats (soak them in the "
    "fridge), instant porridge, pot noodles and cup soup need nothing more. If you can stretch to "
    "a cheap single-ring hob, it opens up pasta, rice, eggs and tinned soup.")

NO_OVEN_ONLY = (
    "With an oven and no hob, cook in one tray: chicken thighs or sausages with chopped potato, "
    "onion and pepper, oil, salt and herbs, 40 minutes at 200C (180C fan), turned once. Jacket "
    "potatoes take an hour at the same heat, baked pasta or a tin of tomatoes with butter and "
    "breadcrumbs bakes in 25 minutes, and roasted veg with a drained tin of chickpeas makes a "
    "meal on its own.")

NO_MICROWAVE = (
    "Without a microwave, a pan does the same jobs: reheat rice or leftovers with a splash of water "
    "over a low heat, defrost in the fridge overnight, and cook porridge or scrambled eggs in a "
    "saucepan in about five minutes.")

LISTING = ("i have", "i've got", "ive got", "i only have", "only have", "only got", "just have",
           "just got", "there's", "theres", "in the fridge", "in my fridge", "in the cupboard",
           "in my cupboard", "sat in")

COOKING_ASKS = ("cook", "cooking", "make", "making", "dinner", "dinners", "supper", "tea",
                "meal", "meals", "eat", "eating", "recipe", "recipes", "idea", "ideas", "food",
                "lunch", "breakfast", "roast", "bake", "baking", "hungry",
                "need", "needs", "want", "wants", "dessert", "desserts", "pudding", "puddings",
                "sweet", "cake", "cakes", "biscuits", "cookies")


SWEET_ASK = re.compile(r"\b(?:desserts?|puddings?|sweets?|biscuits?|cookies?|meringues?"
                       r"|possets?|trifles?|make ahead|make-ahead)\b")
CROWD = re.compile(r"\b(?:[89]|1[0-9]|[2-9][0-9])\b")

BREAD = re.compile(r"\b(?:bread|loaf|loaves|flatbread|naan|pitta|pita)\b", re.I)

CAKEISH = re.compile(r"\b(?:cake|cakes|biscuit|biscuits|cookie|cookies|brownie|brownies|"
                     r"muffin|muffins|scone|scones|meringue|meringues|pastry|pastries|"
                     r"flapjack|flapjacks)\b", re.I)

def _asks_for_sweet(text):
    text = str(text).lower()
    if "sweet potato" in text:
        return False
    return bool(SWEET_ASK.search(text))


def _no_baking(text):
    said = str(text or "")
    if GRIDDLE_BAKES.search(said):
        return _griddle_answer(said)
    if BREAD.search(said) and not CAKEISH.search(said):
        base = NO_OVEN_BREAD
    else:
        base = NO_BAKING + (" " + NO_OVEN_BREAD if BREAD.search(said) else "")
    many = CROWD.search(said)
    if not many:
        return base
    return base + (" For " + many.group() + " people make two tins of it and cut it small, "
                        "or set one big cheesecake in a deep tin and chill it overnight.")


PUDDING_IDEAS = (
    "An apple and blackberry crumble is the easiest crowd-pleaser: fruit in a dish, a crumble of "
    "butter, flour and sugar on top, 35 minutes at 180C, and custard. Baked rice pudding and bread "
    "and butter pudding are just as easy and soft enough for anyone who finds chewing hard; Eton "
    "mess takes five minutes if you buy the meringues.")


def _pudding_ideas(memory, understood):
    text = str(((understood or {}).get("clean") or "")).lower()
    many = CROWD.search(text)
    if not many:
        return PUDDING_IDEAS
    return PUDDING_IDEAS + (" For " + many.group() + " people make two dishes of it and put the "
                            "custard out in a jug.")


def without(understood):
    gone = missing(understood)
    if not gone:
        return None
    words = (understood or {}).get("words") if isinstance(understood, dict) else None
    text = " ".join(words) if isinstance(words, list) else _line(understood)
    text = str(text).lower()
    asking = any(re.search(r"\b" + re.escape(one) + r"\b", text) for one in COOKING_ASKS)
    listing = any(one in text for one in LISTING)
    if not (asking or listing):
        named = any(one in text for one in HAVE_ONE["hob"] + HAVE_ONE["microwave"]
                    + HAVE_ONE["kettle"] + HAVE_ONE["oven"] + ONLY_ONE["hob"]
                    + ONLY_ONE["microwave"] + ONLY_ONE["kettle"])
        if not (named and len(text.split()) <= 8):
            return None
    baking = ("bake", "baking", "cake", "cakes", "bread", "pie", "pastry", "pastries",
              "biscuit", "biscuits", "cookie", "cookies", "meringue", "meringues",
              "yorkshire", "scone", "scones", "loaf", "loaves", "muffin", "muffins",
              "brownies", "flapjack", "flapjacks")
    how = "bake" if any(one in text for one in baking) or _asks_for_sweet(text) else ""
    if "oven" in gone and how == "bake" and "hob" not in gone:
        return _no_baking(text)
    if "oven" in gone and "hob" not in gone and GRIDDLE_BAKES.search(text):
        return _griddle_answer(text)
    have = available(text, gone)
    if "hob" in gone or "hob" not in have:
        if "oven" in have:
            return NO_OVEN_ONLY
        if "microwave" in have:
            return NO_HOB
        return NO_KETTLE
    if "oven" in gone or "oven" not in have:
        return NO_OVEN
    if "microwave" in gone and how != "bake":
        return NO_MICROWAVE
    return None


ONLY_ONE = {
    "kettle": ("only got a kettle", "only have a kettle", "only a kettle", "just a kettle",
               "only the kettle"),
    "microwave": ("only have a microwave", "only got a microwave", "only a microwave",
                  "just a microwave", "just have a microwave", "just got a microwave",
                  "microwave only", "only the microwave"),
    "hob": ("only a hob", "just a hob", "only have a hob", "only got a hob", "hob only",
            "only have one hob"),
    "oven": ("only an oven", "only have an oven", "only got an oven", "oven only"),
}
HAVE_ONE = {
    "oven": ("got an oven", "have an oven", "have the oven", "the oven works", "there's an oven",
             "theres an oven", "oven works"),
    "hob": ("got a hob", "have a hob", "there's a hob", "theres a hob", "got a cooker",
            "have a cooker"),
    "microwave": ("got a microwave", "have a microwave", "there's a microwave",
                  "theres a microwave"),
    "kettle": ("got a kettle", "have a kettle", "there's a kettle", "theres a kettle"),
}


def available(text, gone):
    text = str(text).lower()
    for name, phrases in ONLY_ONE.items():
        if any(one in text for one in phrases):
            return {name}
    named = {name for name, phrases in HAVE_ONE.items() if any(one in text for one in phrases)}
    named -= set(gone or ())
    if named:
        return named
    return {"oven", "hob", "microwave", "kettle"} - set(gone or ())

def _herbs_keep(memory, understood):
    words = set((understood or {}).get("words") or ())
    clean = " " + ((understood or {}).get("clean") or "") + " "
    if {"slimy", "slime", "rotten", "mouldy", "moldy"} & words or "gone over" in clean:
        return ("A slimy herb is past saving, so bin the slimy stems and pick out the ones that are "
                "still green to use today. It happens when the leaves stay wet: a bag with damp "
                "kitchen paper is right, a wet one sat in a warm fridge is not. Next bunch, stand "
                "the stems in an inch of water with a bag over the top, or freeze what you cannot "
                "use in the next few days.")
    return ("Stand soft herbs in a jar with an inch of water, loosely covered with a bag, or wrap "
            "them in damp kitchen paper in the fridge. Basil hates the cold, so keep that one on "
            "the windowsill instead.")



COOK_WORDS = {
    "reduce": "Reducing is simmering a sauce uncovered until water boils off and it thickens and "
              "tastes stronger. Watch it at the end - the last two minutes do most of the work.",
    "sear": "Searing is browning meat hard in a hot pan, for flavour and colour, not for cooking "
            "it through. Pat it dry first and leave it alone until it releases by itself.",
    "blanch": "Blanching is a minute or two in boiling water, then straight into cold water: it "
              "sets the colour of green vegetables and loosens tomato and peach skins.",
    "sweat": "Sweating is softening onion or vegetables slowly in a little fat with the lid on, "
             "without colouring them. Low heat, five to ten minutes.",
    "al dente": "Al dente means pasta with a little bite left in the middle: take a minute off "
                "the packet time, taste it, and keep testing.",
    "fold": "Folding is mixing gently with a big spoon, turning the bowl and cutting through, so "
            "you keep the air in whipped egg white or cream.",
    "deglaze": "Deglazing is pouring wine, stock or water into a hot pan after frying and "
               "scraping the brown bits up: that is where the flavour is.",
}


NEEDS_DEFINITION = frozenset(("reduce", "fold", "sear", "sweat"))

WORD_SUBJECT = {
    "reduce": ("sauce", "stock", "gravy", "wine", "juice", "glaze", "syrup", "liquid",
               "broth", "soup", "half", "pan", "thicken", "thickens", "jam", "cream"),
    "fold": ("flour", "egg", "eggs", "white", "whites", "batter", "mixture", "dough",
             "cream", "sugar", "meringue", "ingredient", "ingredients", "pastry", "bowl",
             "spoon", "spatula", "filling", "chocolate"),
    "sear": ("steak", "meat", "beef", "chicken", "fish", "salmon", "pork", "lamb", "tuna",
             "pan", "joint", "roast", "sausage", "tofu", "scallop"),
    "sweat": ("onion", "onions", "shallot", "shallots", "leek", "garlic", "carrot",
              "vegetables", "veg", "celery", "mushroom", "pan", "butter", "fat", "oil"),
    "blanch": ("vegetable", "vegetables", "greens", "bean", "beans", "broccoli", "tomato",
               "tomatoes", "peach", "almond", "almonds", "potato", "potatoes", "chips",
               "spinach", "cauliflower", "cabbage"),
    "deglaze": ("pan", "wine", "stock", "sauce", "bits", "meat", "roast", "gravy"),
}

NOT_A_COOKING_LINE = ("pain", "pains", "maths", "math", "percentage", "equation", "fraction",
                      "algebra", "fitted sheet", "bed sheet", "sheets", "towel", "towels",
                      "laundry", "pillow", "duvet", "hands sweating", "sweaty", "armpits",
                      "my hands", "my feet", "fever", "night sweats", "anxious", "anxiety",
                      "nerves", "doctor", "gp appointment", "hospital", "sick", "ill",
                      "temperature of the room", "heating bill", "electricity", "gas bill",
                      "poker", "cards", "card game", "blackjack", "origami", "folding chair",
                      "folding table", "geology", "tectonic", "fold in the rock",
                      "relationship", "boyfriend", "girlfriend",
                      "belly fat", "my back", "my shoulder",
                      "spam", "email", "emails", "e-mail", "inbox", "junk mail", "scam",
                      "unsubscribe", "newsletter", "mailbox",
                      "brightness", "bright", "brighter", "dim", "dimmer", "screen", "screens",
                      "display", "volume", "louder", "loud", "screen time", "data usage",
                      "my diet", "diet", "diets", "dieting", "sugar intake", "blood sugar",
                      "less sugar", "down on sugar", "cut out sugar", "sugary", "cravings")

DEFINITION_WORDS = ("mean", "means", "meaning", "difference", "what is", "what's", "whats",
                    "between", "versus", "vs", "definition")


def _names_a_subject(word, said):
    if any(subject in said for subject in WORD_SUBJECT.get(word, ())):
        return True
    return any(word + pronoun in said for pronoun in (" it", " them", " this", " these"))


def _cook_word_hit(word, said):
    if word in said:
        return said.find(word), word
    stem = word.rstrip("e")
    if len(stem) > 3 and stem in said:
        return said.find(stem), word
    return None


def _cook_word(memory, understood):
    said = str(understood.get("clean") or " ".join(understood.get("words") or [])).lower()
    found = sorted(hit for hit in (_cook_word_hit(word, said) for word in COOK_WORDS) if hit)
    named = []
    for pos, word in found:
        if any(pos >= other_pos and pos + len(word) <= other_pos + len(other) and word != other
               for other_pos, other in found):
            continue
        named.append(word)
    if not named:
        return None
    if not any(word in said for word in DEFINITION_WORDS):
        named = [word for word in named
                 if word not in NEEDS_DEFINITION or _names_a_subject(word, said)]
        if not named:
            return None
    if len(named) == 1:
        return COOK_WORDS[named[0]]
    return "%s %s" % (COOK_WORDS[named[0]], COOK_WORDS[named[1]])


_MASH_NOT_THIS = ("without butter", "no butter", "butter free", "without milk", "no milk",
                  "milk free", "dairy free", "dairy-free", "no dairy", "without dairy",
                  "vegan", "baby", "babies", "for my baby", "for a baby", "weaning", "weaned",
                  "toddler", "6 months", "six months", "9 months", "first foods",
                  "keep", "keeps", "keeping", "store", "storing", "storage", "fridge",
                  "freezer", "freeze", "refrigerate", "reheat", "reheated", "leftover",
                  "left over", "last", "lasts", "gone off", "safe",
                  )

_NO_MEAT = ("without mince", "no mince", "without beef", "no beef", "without meat", "no meat",
            "meat free", "meat-free", "vegetarian", "veggie", "vegan", "lentil", "lentils",
            "bean", "beans", "chickpea", "chickpeas", "pulse", "pulses")

_BAKE_ALIASES = None


def _bake_aliases():
    global _BAKE_ALIASES
    if _BAKE_ALIASES is None:
        _BAKE_ALIASES = tuple(sorted(
            (([_fold(part) for part in alias.split()], name)
             for name, (aliases, _) in BAKES.items() for alias in aliases),
            key=lambda pair: -len(pair[0])))
    return _BAKE_ALIASES


_TIMING_ASKS = ("how long", "minutes", "temperature", "what temp", "fan", "gas mark", "preheat",
                "how hot")


_PANTRY_AS_WORDS = None


def _pantry_words():
    global _PANTRY_AS_WORDS
    if _PANTRY_AS_WORDS is None:
        _PANTRY_AS_WORDS = frozenset(_fold(name) for name in PANTRY)
    return _PANTRY_AS_WORDS


def _bake_hits(folded, skip_pantry=False):
    hits = []
    for parts, name in _bake_aliases():
        if skip_pantry and len(parts) == 1 and parts[0] in _pantry_words():
            continue
        for start in range(len(folded) - len(parts) + 1):
            if folded[start:start + len(parts)] == parts:
                hits.append((parts, name))
                break
    return hits


def _names_a_bake(understood):
    words = understood.get("words")
    if not isinstance(words, (list, tuple)):
        words = str(understood.get("clean") or "").split()
    folded = [_fold(word) for word in words]
    return any(not _already_baked(folded, parts)
               for parts, _name in _bake_hits(folded, skip_pantry=True))


_ALREADY_BAKED_WORDS = frozenset("leftover leftovers stale old yesterday already".split())
_ALREADY_BAKED_PHRASES = ("use up", "using up", "used up", "left over", "left from",
                          "already made", "got spare", "going stale")


def _already_baked(folded, parts):
    for start in range(len(folded) - len(parts) + 1):
        if folded[start:start + len(parts)] != parts:
            continue
        window = folded[max(0, start - 3):start]
        if any(word in _ALREADY_BAKED_WORDS for word in window):
            return True
        return any(phrase in " ".join(window) for phrase in _ALREADY_BAKED_PHRASES)
    return False


def _bake(memory, understood, text=None):
    words = understood.get("words")
    if not isinstance(words, (list, tuple)):
        words = str(understood.get("clean") or "").split()
    folded = [_fold(word) for word in words]
    if text:
        folded = folded + [_fold(word) for word in str(text).lower().split()]
    said = " ".join(folded)
    if any(phrase in said for phrase in _TIMING_ASKS):
        return None
    if any(phrase in said for phrase in _NO_YEAST):
        return None
    if not (understood.get("asks") or any(word in ("how", "what", "whats", "recipe")
                                          for word in folded)):
        return None
    if _asks_vegan(folded):
        return None
    hits = _bake_hits(folded, skip_pantry=len(ingredients(understood)) > 1)
    if not hits or _already_baked(folded, hits[0][0]):
        return None
    return BAKES[hits[0][1]][1]


_NONSTICK_CLEAN = ("clean", "cleaning", "wash", "washing", "scrub", "scouring", "burnt",
                   "stained")
_NONSTICK_KEEP = ("safe", "safety", "still use", "use it", "throw", "bin it", "replace",
                  "replacing", "worn", "bits", "coming off", "flakes", "scratched", "scratches",
                  "scratch", "flaking", "peeling", "coating")


def _non_stick_pan(memory, understood):
    said = " ".join(str((understood or {}).get(key) or "")
                    for key in ("clean", "norm_text", "norm")).lower()
    wants_clean = any(word in said for word in _NONSTICK_CLEAN)
    if not wants_clean and any(word in said for word in _NONSTICK_KEEP):
        return ("Small scratches are fine to keep cooking on. Once it is scratched through to the "
                "metal, or the coating is flaking or peeling into the food, replace the pan: you "
                "do not want flakes of coating in a meal, and a worn pan stops being non-stick "
                "anyway. Until then, keep metal tools, scouring pads and an empty pan on high "
                "heat away from it, because those are what scratch it.")
    return ("Warm water, washing-up liquid and a soft sponge, then dry it with a cloth: no "
            "scouring pad, no wire wool and no metal tools, because a scratch in the coating is "
            "what ruins it. For burnt-on food, simmer a little water in the pan for five minutes "
            "and lift it with a wooden spatula rather than scraping. If the coating is flaking or "
            "peeling, replace the pan - that is not something to cook through.")
TEA_METHOD_TEXT = (
    "Fresh water boiled once, one teabag per mug, three to four minutes and then the bag out: "
    "that is the whole of a good cup, and the milk goes in last. Green tea wants cooler water, "
    "about 80C, for two to three minutes, and black tea wants it just off the boil, three to "
    "five. Bitter tea has steeped too long in water that was too hot, and a mug that tastes of "
    "the last one is a bag left sitting in it.")

TEA_POT_TEXT = (
    "Warm the pot first with a splash of boiling water swirled round and tipped away, then one "
    "teabag or one teaspoon of leaves per cup and one extra for the pot, water just off the "
    "boil, three to four minutes. Take the bags or leaves out before it goes to the table, and a "
    "cosy keeps the second cup hot without stewing it.")

TEA_ICED_TEXT = (
    "Cold brew it: eight teabags to a litre of cold water in the fridge overnight, bags out in "
    "the morning, then lemon and sugar to taste, which has none of the bitterness of a hot brew "
    "cooled down. In a hurry, brew double strength in a mug of boiling water for four minutes, "
    "take the bags out, and pour it over a jug of ice.")

TEA_CLOUDY_TEXT = (
    "Cloudy tea is the minerals in hard water binding with the tannin, and it is harmless to "
    "drink: filter the water, or use bottled, to get it clear, or add a small pinch of "
    "bicarbonate of soda to the pot, which keeps the tannin dissolved. It is not a dirty kettle "
    "and it is not a sign the tea has gone off.")

TEA_FAULT_TEXT = (
    "Green tea wants water at about 80C for 2 to 3 minutes; black tea wants it just off the "
    "boil for 3 to 5. Bitter tea is nearly always tea that steeped too long in water that was "
    "too hot, and sour or stewed tea is a pot left standing on a warmer or in the leaves: "
    "pour it off them and make the next one weaker and shorter.")


TEA_GREEN_TEXT = (
    "Green tea wants water at about 80C rather than boiling, for two to three minutes: boil the "
    "kettle and let it stand for a minute or two, or add a splash of cold water first. Water "
    "straight off the boil makes it bitter, and green tea goes bitter quickly, so pull the bag "
    "out at three minutes and drink it soon after.")

TEA_TWICE_TEXT = (
    "A second cup from the same teabag is weak and mostly colour, but it is harmless: if you "
    "want it stronger, use a fresh bag and pull it out sooner instead. Reuse one within the same "
    "hour at most, and not once it has been sitting in milk.")


_ASKS_WHAT_TO_HAVE = re.compile(
    r"\b(?:what|anything|something|whats|what's)\b[^.?!]*\b(?:have|eat|cook|make|do)\b")
_FOR_A_MEAL = re.compile(
    r"\bfor\s+(?:my\s+|our\s+|the\s+|his\s+|her\s+)?"
    r"(?:tea|dinner|lunch|supper|breakfast|brekkie|supper|teatime|tea time)\b")


def _tea_reply(memory, understood):
    said = " ".join(str((understood or {}).get(key) or "")
                    for key in ("clean", "norm_text", "norm")).lower()
    if _FOR_A_MEAL.search(said) and _ASKS_WHAT_TO_HAVE.search(said):
        return None
    words = set(re.findall(r"[a-z']+", said))
    if words & {"iced", "ice"}:
        return TEA_ICED_TEXT
    if words & {"pot", "teapot", "teapots"}:
        return TEA_POT_TEXT
    if words & {"cloudy", "cloudiness", "scum", "murky", "film"}:
        return TEA_CLOUDY_TEXT
    if words & {"green", "greens", "sencha", "matcha", "jasmine"}:
        return TEA_GREEN_TEXT
    if words & {"twice", "again", "reuse", "re-use", "second"}:
        return TEA_TWICE_TEXT
    if words & {"bitter", "sour", "soured", "stewed", "weak", "strong", "stronger", "watery",
                "tastes", "taste", "tasting", "stewing"}:
        return TEA_FAULT_TEXT
    return TEA_METHOD_TEXT


def _rice_time(memory, understood):
    words = set((understood or {}).get("words") or ())
    asks = set((understood or {}).get("asks") or ())
    brown = words & {"brown", "wholegrain", "whole"}
    if brown:
        return ("Brown rice takes 25 to 30 minutes, with a little more water: 1 part rice to 2 "
                "parts water, lid on, low simmer. Let it sit 5 minutes off the heat, still covered, "
                "before you fork it through. White long grain is 1 part rice to 1.5 parts water for "
                "12 minutes, then 10 minutes off the heat. Too much water is what turns rice to "
                "porridge.")
    if asks & {"how_long", "when"}:
        return ("White long grain takes 10 to 12 minutes on a low simmer with the lid on, then 10 "
                "more off the heat. Use 1 part rice to about 1.5 parts water by volume, or the "
                "fingertip test: water one knuckle above the rice. Brown and wholegrain are the "
                "ones that take longer. Too much water is what turns rice to porridge.")
    return ("Use 1 part rice to about 1.5 parts water by volume for long grain, or the fingertip "
            "test: water one knuckle above the rice, and give it 12 minutes on a low simmer with the "
            "lid on, then 10 more off the heat. Brown and wholegrain rice are the ones that take "
            "longer. Too much water is what turns rice to porridge.")

_NO_YEAST = ("no yeast", "without yeast", "yeastless", "yeast free", "yeast-free",
             "no need for yeast", "dont need yeast", "don't need yeast")


def _bread_rise_answer():
    def answer(memory, understood):
        said = str(understood.get("clean") or " ".join(understood.get("words") or [])).lower()
        if any(one in said for one in _NO_YEAST):
            return None
        if "sourdough" in said or "sour dough" in said or "starter" in said:
            return ("A sourdough loaf rises on the starter, not on warmth alone: a starter that "
                    "doubles in 4 to 6 hours after a feed is strong enough to bake with, and one "
                    "that only bubbles is not, so feed it twice a day for three days first. Then "
                    "give the bulk 4 to 6 hours at room temperature with three or four sets of "
                    "stretch and fold in the first two hours, and shape it with real tension. A "
                    "flat loaf usually wants a stiffer dough and a longer, colder second prove.")
        if "fridge" in said or "overnight" in said or "in the cold" in said:
            return ("A night in the fridge is a slow prove on purpose, not a fault: shape it cold, "
                    "then leave it an hour at room temperature before it goes in the oven. If it "
                    "hasn't risen at all by the morning, the yeast is dead, so check the date.")
        if "twice" in said or "second prove" in said or "second rise" in said or "two proves" in said:
            return ("Yes, twice: the first is done when the dough has doubled, and the second is the "
                    "shaped loaf, about an hour, until it springs back slowly when you poke it. "
                    "Skipping the second gives you a tight, close crumb.")
        if ("wont" in said or "won't" in said or "isnt" in said or "isn't" in said
                or "not rising" in said or "didnt" in said or "didn't" in said
                or "hasnt risen" in said or "stalled" in said):
            return ("Give it another hour somewhere around 25C, until it has doubled, and check the "
                    "water was warm rather than hot and that the yeast is in date. If it still "
                    "hasn't moved at all, the yeast is dead, so start again with fresh yeast.")
        return ("Leave it somewhere around 25C for 1 to 2 hours, until the dough has doubled. Yeast "
                "eats the sugars in the flour and gives off gas, and the stretchy gluten holds it "
                "in bubbles, so warmth and time are the whole job. If it hasn't moved at all, the "
                "yeast is dead, so check the date and use water that's warm rather than hot.")
    return answer



_COFFEE_BITTER = (
    "Bitter coffee is over-extracted: grind it coarser, let the water come off the boil for half "
    "a minute, and take it off the grounds sooner - about 4 minutes in a cafetiere, 25 to 30 "
    "seconds for an espresso. Sour is the same dial the other way and wants a finer grind, hotter "
    "water and a little longer. Stale beans and a dirty machine make both, and instant tastes "
    "bitter when it is made with boiling water - let the kettle rest first.")
_COFFEE_SOUR = (
    "Sour coffee is under-extracted: grind it finer, use water just off the boil rather than "
    "boiling, and give it longer on the grounds - about 4 minutes in a cafetiere, 25 to 30 "
    "seconds for an espresso. Bitter is the same dial the other way and wants a coarser grind and "
    "a shorter brew. A sour note that only shows up with milk is usually the milk.")
_COFFEE_BURNT = (
    "A burnt taste is over-extraction or too dark a roast: grind it coarser, let the water come "
    "off the boil for half a minute and shorten the brew, and try a medium roast instead of a "
    "dark one. Scrub the pot and the filter basket too, because old oils go acrid and taste "
    "burnt even with fresh beans.")


def _coffee_fault(memory, understood):
    words = set(re.findall(r"[a-z']+", (understood or {}).get("clean") or ""))
    if words & {"sour", "soured", "acidic", "acid", "vinegary"}:
        return _COFFEE_SOUR
    if words & {"burnt", "burned", "burning", "scorched", "scorching"}:
        return _COFFEE_BURNT
    return _COFFEE_BITTER


LEAFY = ("salad", "lettuce", "leaves", "leafy", "greens", "spinach", "rocket", "arugula",
         "watercress", "salad leaves", "mixed leaves", "lambs lettuce")
LEAFY_AVOID = ("slug", "slugs", "snail", "pest", "garden", "grow", "growing", "plant", "plants",
               "my baby", "the baby", "baby is", "baby has", "a baby", "newborn",
               "child", "children", "toddler",
               "dog", "dogs", "cat", "cats", "puppy", "feel", "feeling", "tired", "exhausted",
               "weak", "unwell", "limp after", "run",
               "that take", "does that take", "will that take", "this take", "it take",
               "take", "takes", "taking", "took",
               "what can i make", "what can i do with", "what should i make", "use up",
               "use it up", "recipe", "recipes", "cook", "cooking", "soup", "pan", "side dish",
               "tea", "teas", "infuse", "infusing", "infused", "brew", "brewing", "brewed",
               "coffee")

_PAN_DISH = ("rice", "sauce", "soup", "stew", "curry", "porridge", "pasta", "potatoes",
             "eggs", "chicken", "meat", "fish", "mince", "cake", "gravy", "custard", "beans",
             "omelette", "omelettes", "omelet", "omelets", "frittata", "frittatas",
             "scrambled egg", "fried egg", "poached egg", "pancake", "pancakes",
             "lentils", "chilli", "beef", "pork", "lamb", "veg", "vegetables", "noodles",
             "garlic", "onion", "onions", "bread", "steak", "bacon", "sausages", "oats",
             "tomato", "tomatoes", "mushrooms", "cheese", "butter", "oil", "toast")
_PAN_CLEAN = ("clean", "cleaning", "cleaned", "scrub", "scour", "soak", "soaking", "wash",
              "washing", "comes off", "come off", "off the bottom", "off my pan", "off the pan",
              "off the inside", "off the base", "get it off", "gets it off", "still stuck",
              "stuck on", "wont come", "won't come",
              "off the tin", "off my tin", "off the tray", "off my tray", "off the sheet",
              "get the burnt off", "burnt off", "stained")

_BURNT_PAN_REPLY = ("Put an inch of water and two tablespoons of bicarbonate of soda in it and "
                    "simmer for ten minutes, then lift the burnt layer with a wooden spoon: "
                    "almost nothing needs scrubbing after that. Stainless steel and enamel can "
                    "take a vinegar soak instead, but never scour a non-stick pan, since it "
                    "takes the coating off for good.")


_PAN_WORDS = ("pan", "pans", "pot", "pots", "saucepan", "saucepans", "wok", "tray", "trays",
              "casserole", "skillet")

_REMOVAL_FROM_A_PAN = ("out of the pan", "out of my pan", "out of a pan", "out of the pot",
                       "out of my pot", "out of a pot", "out of the wok", "out of the saucepan",
                       "out of the casserole", "out of it", "out of there", "get it out",
                       "get the burnt out", "get the burnt off", "get it off")

_BURNT_ON_A_PAN = _REMOVAL_FROM_A_PAN + (
    "off the pan", "off my pan", "off a pan", "off the bottom", "off my bottom", "off the base",
    "off the inside", "off the outside", "burnt on", "burned on", "burnt-on", "burnt black",
    "burned black", "black on the outside", "black on the bottom", "black outside",
    "scorched on the outside", "scorched on the bottom",
    "on the pan", "on my pan", "on a pan", "in the pan", "in my pan", "on the saucepan",
    "on the tray", "in the tray", "on the bottom of the pan", "at the bottom of the pan",
    "burnt the bottom of", "burned the bottom of", "burnt a pan", "burned a pan",
    "burnt my pan", "burned my pan", "burnt the pan", "burned the pan", "burn the pan",
    "burnt my saucepan", "burnt the saucepan", "burnt a saucepan", "burned my saucepan",
    "burnt my pot", "burned my pot", "burnt the pot", "burnt a pot", "burnt my wok",
    "burnt the tray", "burnt my tray", "burnt the base of", "burnt a frying pan")


def _burnt_on_the_pan(text):
    return (_says(text, _BURNT_ON_A_PAN)
            and _says(text, ("burnt", "burned", "black", "blackened", "scorched", "scorch",
                             "burn mark", "scorch mark", "scorched on", "stain", "stained",
                             "discoloured", "discolored", "scratch", "scratched")))

_BURNT_DISH_REPLY = ("Take it off the heat and lift out the burnt bits rather than stirring them "
                     "in, because the smoky taste spreads through everything. If it has gone all "
                     "the way through, a splash of stock and something creamy hides a little of "
                     "it, but a properly burnt sauce is better started again.")


_BURNT_MEAT = ("roast", "joint", "chicken", "turkey", "lamb", "beef", "pork", "gammon", "duck",
               "steak", "sausage", "sausages", "bacon", "ham", "ribs", "brisket", "meatloaf",
               "meatballs", "whole chicken", "thighs", "drumsticks", "wings")
_BURNT_MEAT_REPLY = (
    "Take it out of the tin and carve or cut the black edge away rather than scraping at it, and "
    "taste a slice from the middle before you decide anything, because a joint that caught on one "
    "side is usually fine underneath. Leave the burnt fat and juices in the tin instead of pouring them "
    "into the gravy, and if the middle is still underdone, cover the joint with baking paper and "
    "give it another 10 to 15 minutes at 20C lower. Next time stand it on a rack or a bed of onion "
    "and carrot so it is not sitting in the tin, and cover it loosely once it has browned.")


_BURNT_VEG = ("potato", "potatoes", "parsnip", "parsnips", "carrot", "carrots", "swede",
              "turnip", "sprouts", "broccoli", "cauliflower", "onion", "onions", "chips",
              "roast veg", "roast vegetables", "vegetables", "veg", "squash", "pumpkin",
              "courgette", "courgettes", "aubergine", "peppers", "beetroot", "sweet potato",
              "sweet potatoes", "leek", "leeks", "kale", "cabbage")
_BURNT_VEG_REPLY = (
    "Cut the black edges off with the corner of a spatula rather than scraping them, toss what is "
    "left in a fresh spoon of oil and give it 10 more minutes at 20C lower: a roast vegetable "
    "catches on the edges long before the middle. Anything black right through goes in the bin, and "
    "a tray that is badly caught is better mashed with butter than carved.")
_BURNT_BATTER = ("yorkshire", "yorkshires", "yorkshire pudding", "yorkshire puddings",
                 "toad in the hole", "batter", "popover", "popovers", "dutch baby")
_BURNT_BATTER_REPLY = (
    "Cut the black tops off rather than scraping them and eat the rest: batter burns because the "
    "fat was smoking before it went in, or the tin sat too high. Next time put the tin on the middle "
    "shelf, get the fat hot but not smoking - a drop of batter should sizzle rather than spit - pour "
    "the batter in cold, and do not open the door for the first 20 minutes.")
_BURNT_EATING_ASK = ("bad for", "bad for you", "bad for me", "harmful", "dangerous",
                     "cancer", "carcinogen", "carcinogenic", "poison", "poisonous", "toxic",
                     "safe to eat", "still eat", "can i eat", "can you eat", "can i still",
                     "ok to eat", "okay to eat", "alright to eat", "healthy", "unhealthy",
                     "does it matter", "is it ok", "is it okay", "is it safe", "is it bad",
                     "is charred", "is burnt food", "burnt food bad", "charred food bad",
                     "burnt food", "burned food", "charred food", "burnt meat", "charred meat",
                     "bbq food", "barbecue food")
_BURNT_EATING_REPLY = (
    "It is not poisonous, and one burnt dinner is nothing to worry about. The black is carbon, plus "
    "acrylamide where the food was starchy - bread, potatoes, chips - and other compounds where it "
    "was meat, and the advice is about habit rather than about a single meal. So scrape the black "
    "off toast and roast potatoes and eat the rest, cut the charred edge off meat, and keep properly "
    "blackened food to the odd occasion rather than most weeks. The fat that drips onto a hot grill "
    "and smokes is best kept off the food: cook a little slower and turn things instead of leaving "
    "them in one spot.")

_ROAST_PARTS = ("stuffing", "crackling")
_ROAST_PART_REPLY = (
    "Cut the burnt patches away and keep what is underneath - whatever caught on top is usually "
    "fine in the middle, and a black patch comes off with a knife before it goes on the plate. If "
    "what is left is dry, spoon a little stock or gravy over it, and next time put it in later "
    "than the joint, so it gets less time at the heat.")


def _burnt_dish(memory, understood):
    said = " ".join(str((understood or {}).get(k) or "")
                    for k in ("clean", "norm_text", "norm")).lower()
    if _says(said, _BURNT_EATING_ASK):
        return _BURNT_EATING_REPLY
    if _says(said, _BURNT_BATTER):
        return _BURNT_BATTER_REPLY
    if (_says(said, _BURNT_VEG)
            and not _says(said, ("chicken", "beef", "lamb", "pork", "turkey", "gammon", "duck",
                                 "steak", "sausage", "sausages", "bacon", "ham", "joint",
                                 "brisket", "meatballs"))):
        return _BURNT_VEG_REPLY
    without_vessel = _VESSEL_PHRASES.sub(" ", said)
    if _says(without_vessel, _ROAST_PARTS):
        return _ROAST_PART_REPLY
    if (_says(without_vessel, _BURNT_MEAT)
            and not _says(without_vessel, _PAN_WORDS + ("sauce", "gravy", "soup", "stew",
                                                        "curry", "rice"))):
        return _BURNT_MEAT_REPLY
    baked = _VESSEL_PHRASES.sub(" ", said)
    if _says(baked, _PAN_DISH):
        return _BURNT_DISH_REPLY
    if _says(said, _PAN_WORDS) or _says(baked, _TIN_OR_OVEN):
        return ""
    return _BURNT_DISH_REPLY


_BAKE_NOUNS = ("cake", "cakes", "sponge", "loaf", "bread", "buns", "biscuits", "cookies",
               "muffins", "brownies", "cheesecake", "pastry", "pie", "pies", "tart", "tarts",
               "traybake", "scones", "flapjack", "quiche", "yorkshire", "pizza", "madeira",
               "fruit cake", "victoria sponge", "bakewell")
_GRIME_WORDS = ("grease", "greasy", "stuck", "stuck on", "marks", "mark", "stains", "stained",
                "clean", "cleaning", "cleaned", "scrub", "scrubbing", "scour", "soak",
                "soaking", "bicarbonate", "get off", "get it off", "comes off", "wipe",
                "wiping", "washing", "washed")
_TIN_OR_OVEN = ("oven", "tin", "tray", "hob", "grill", "glass", "rack", "shelf", "dish",
                "plate", "pan", "cooker", "door", "inside")


_BURNT_ON = ("burnt on", "burned on", "baked on", "stuck on", "stuck", "black inside",
             "inside of my oven", "black on the inside", "black at the back")

_VESSEL_PHRASES = re.compile(
    r"\b(?:cake|loaf|pie|tart|muffin|bun|biscuit|bread|traybake|flan|roast|toast)\s+"
    r"(?:tins?|trays?|pans?|moulds?|molds?|dishes?|dish|sheets?|cases?|liners?|tins?)\b")


def _words_and_text(understood):
    parts = []
    for key in ("clean", "norm_text"):
        parts.append(str((understood or {}).get(key) or ""))
    words = (understood or {}).get("norm")
    if isinstance(words, (list, tuple)):
        parts.append(" ".join(str(word) for word in words))
    else:
        parts.append(str(words or ""))
    return " ".join(parts).lower()


def _says(said, phrases):
    return re.search(r"\b(?:%s)\b" % "|".join(re.escape(one) for one in phrases), said) is not None


def _burnt_pan(memory, understood):
    said = " ".join(str((understood or {}).get(key) or "")
                    for key in ("clean", "norm_text", "norm")).lower()
    if _says(said, _PAN_CLEAN):
        return _BURNT_PAN_REPLY
    if _says(said, _PAN_DISH):
        return ""
    return _BURNT_PAN_REPLY


_BAKED_BURNT = ("cake", "cakes", "sponge", "loaf", "loaves", "bread", "buns", "bun", "scones",
                "scone", "muffins", "muffin", "brownies", "brownie", "biscuits", "biscuit",
                "pastry", "pie", "tart", "quiche", "roast potatoes", "roasties", "chips", "fries")


_TIN_SIZE = ("A 2lb loaf tin is 19 x 11cm for a 900g loaf and a 1lb tin is 15 x 9.5cm for a "
             "450g one; a 20cm round cake tin takes the 4-egg sponge and an 18cm one the 3-egg.")
_TIN_FILL = ("Fill a bread tin two-thirds full and a cake tin three-quarters at most.")
_TIN_LINE = ("Line bread with baking parchment; for a cake, grease the tin and line only the base, "
             "because loose paper at the sides makes the sponge climb rather than rise.")
_TIN_GREASE = ("Rub the inside of the tin all over with butter or a little oil, then dust it with "
               "flour and tip the extra out; a circle of baking paper on the base does the same job.")
_TIN_FRUIT = ("A fruit cake or a Christmas cake wants a deep tin, not a sponge tin: a 20cm round "
              "one for a 2kg mix, lined with a double thickness of parchment and a collar of "
              "paper round the outside, because it bakes for two and a half hours or more.")
_TIN_GREASE_WORDS = ("grease", "greased", "greasing", "butter the", "dust with flour", "dust it")
_TIN_LINE_WORDS = ("line", "lined", "lining", "parchment", "baking paper", "greaseproof", "paper",
                   "line it", "line the")
_TIN_FRUIT_WORDS = ("fruit cake", "christmas cake", "rich fruit", "wedding cake", "simnel",
                    "dark fruit")


def _tin_answer(memory, understood):
    said = " ".join(str((understood or {}).get(key) or "")
                    for key in ("clean", "norm_text", "norm")).lower()
    if any(word in said for word in _TIN_FRUIT_WORDS):
        return " ".join((_TIN_FRUIT, _TIN_SIZE))
    if any(word in said for word in _TIN_LINE_WORDS):
        return " ".join((_TIN_LINE, _TIN_SIZE, _TIN_FILL))
    if any(word in said for word in _TIN_GREASE_WORDS):
        return " ".join((_TIN_GREASE, _TIN_SIZE))
    return " ".join((_TIN_SIZE, _TIN_FILL, _TIN_LINE))


_CAKE_FAULT_WORDS = (
    ("domed", "dome", "domes", "doming", "raised in the middle", "rises in the middle"),
    ("cracked", "cracks", "cracking", "crack", "split on top", "splits on top"),
    ("eggy", "tastes of egg", "taste of egg", "smells of egg", "egg taste", "tasting of egg"),
    ("soggy bottom", "soggy underside", "wet bottom", "soggy base"),
)


def _cake_fault(memory, understood):
    said = " ".join(str((understood or {}).get(key) or "")
                    for key in ("clean", "norm_text", "norm")).lower()
    words = said
    if any(word in words for word in _CAKE_FAULT_WORDS[0]):
        return ("A dome is the outside setting before the middle has caught up: bake 10C lower, "
                "170C (150C fan) on the middle shelf, use the tin the recipe names rather than a "
                "smaller one, and stop beating the moment the flour is in. Trim the dome flat with "
                "a bread knife before you fill it, and nobody sees it.")
    if any(word in words for word in _CAKE_FAULT_WORDS[1]):
        return ("A split top is the crust setting while the middle is still rising: lower the oven "
                "10C, put the tin on the middle shelf, and keep the door shut for the first 20 "
                "minutes. Cool it in the tin for 10 minutes, then on a rack, because a cake cooled "
                "in a hot tin goes clammy and splits.")
    if any(word in words for word in _CAKE_FAULT_WORDS[2]):
        return ("An eggy taste is too many eggs for the flour or a bake that stopped a few minutes "
                "short: add a quarter teaspoon of salt and a teaspoon of vanilla or the zest of a "
                "lemon, and give it 5 more minutes, checking with a skewer. The same mix tastes "
                "eggier cold, so try it once it has cooled rather than from the tin.")
    if any(word in words for word in _CAKE_FAULT_WORDS[3]):
        return ("A soggy bottom is underbaked underneath: use a metal tin rather than a ceramic "
                "dish, bake on the middle shelf and not above a tray of water, and give it 5 to 10 "
                "minutes longer with foil over the top once it is brown. A cold filling or a wet "
                "fruit layer under a thick batter does the same thing.")
    return ("An even rise is a level batter and a steady oven: sift the raising agent through the "
            "flour rather than adding it last, spread the batter level with the back of a spoon, "
            "and use a tin that the mix fills by two thirds. Turn the tin once, after 15 minutes, "
            "if your oven browns the back corner first.")


_PASTRY_SHRINK_WORDS = ("shrink", "shrank", "shrunk", "shrinking", "shrinks", "pulled away",
                        "pulls away", "slid down", "slides down", "slumped", "slumps",
                        "slumping", "limp")


def _pastry_fault(memory, understood):
    said = " ".join(str((understood or {}).get(key) or "")
                    for key in ("clean", "norm_text", "norm")).lower()
    if any(word in said for word in _PASTRY_SHRINK_WORDS):
        return ("Pastry shrinks when it is stretched into the tin: press it gently into the corners "
                "rather than pulling the sides up, chill the lined case for 20 minutes before it "
                "goes in, and leave the overhang on until after baking, because the spare pastry "
                "holds the sides up while they set.")
    return ("A soggy pastry base wants more heat underneath it and less water in the filling: "
            "blind bake it 5 minutes longer than the recipe says, brush the warm base with beaten "
            "egg white before the filling goes in, and stand the tin on a hot baking sheet so the "
            "heat reaches the pastry rather than stopping at the filling.")


_BAKE_PREVENTION = (
    "Lay a sheet of foil loosely over the top as soon as it starts to colour, and turn the "
    "oven down 10 to 20C (or move the tin a shelf lower): a cake that catches on top is "
    "nearly always an oven running hot, a shelf too high or a dark tin, not the mixture. If "
    "the top is brown and the middle still wobbles, cover it and give it another 10 to 15 "
    "minutes rather than turning the heat up. If the bottom is already black, cut that off, "
    "trim the dark top and serve the rest - and next time check your oven with a thermometer, "
    "since most run 10 to 20C hotter than the dial says.")
_BAKE_BURNT = (
    "Cut or grate the black off once it has cooled, and if only the top is dark the rest is "
    "fine - a dark top on a fruit cake is often just the sugar. If the middle is still wet, "
    "cover the tin loosely with foil and give it another 10 to 15 minutes. Next time move the "
    "oven shelf down one and tent the tin with foil after 20 minutes, because a bake burns on "
    "top while the middle is still wet.")
_BAKE_BOTTOM = re.compile(r"\b(?:bottom|bottoms|underneath|underside|base of the tin)\b", re.I)
_BAKE_BOTTOM_REPLY = (
    "Lift the shelf up one, slide a baking sheet or two under the tin to take the direct heat and "
    "drop the oven 10C, because a bottom that burns first means too much heat from underneath and "
    "a hot oven burns the base while the middle is still wet. Line a dark or thin tin with baking "
    "paper, and turn the tin if one corner of the oven browns hard. If the top is browning before "
    "the middle is set, lay a sheet of foil loosely over it so the base can catch up. If the "
    "bottom has already caught, cut or grate the black off and eat the rest, and check the oven "
    "once with a thermometer, since most run 10 to 20C hotter than the dial says.")
_BAKE_STOP = re.compile(r"\b(?:stop|stops|prevent|avoid)\b|\bwhy\b", re.I)
_BAKE_DONE = re.compile(r"\b(?:burnt|burned|caught)\b", re.I)


def _bake_burning(memory, understood):
    said = " ".join(str((understood or {}).get(key) or "")
                    for key in ("clean", "norm_text", "norm")).lower()
    text = _words_and_text(understood)
    baked = _VESSEL_PHRASES.sub(" ", text)
    if (not _says(baked, _BAKE_NOUNS) and not _says(baked, _BAKED_BURNT)
            and _says(text, _TIN_OR_OVEN)):
        return ""
    if _BAKE_BOTTOM.search(said):
        return _BAKE_BOTTOM_REPLY
    if _BAKE_STOP.search(said) or "burning" in said:
        return _BAKE_PREVENTION
    if _BAKE_DONE.search(said):
        return _BAKE_BURNT
    return _BAKE_PREVENTION


def _burnt(memory, understood):
    words = [str(word).lower() for word in ((understood or {}).get("words") or [])]
    said = " ".join(words)
    if any(_same(word, bake) for word in words for bake in _BAKED_BURNT) or any(
            " " in bake and bake in said for bake in _BAKED_BURNT):
        return ("A burnt top on a bake is usually saveable: take it out at once, cover the tin loosely "
                "with foil so the middle carries on cooking, and when it is cool cut the black off "
                "with a serrated knife or grate it away - a dark top on a fruit cake is often just "
                "the sugar. Next time move the shelf down one, drop the oven 10C and tent the tin with "
                "foil after 20 minutes, because a bake burns on top while the middle is still wet.")
    if any(word in ("toast", "toaster") for word in words):
        return ("Scrape the black off with a knife and eat the rest: burnt toast is not dangerous, and "
                "a scrape takes the bitter taste with it. Next time set the toaster one notch lower "
                "and stay next to it, because toast goes from golden to black in under a minute.")
    return ("Take it off the heat and lift out the burnt bits rather than stirring them in, because "
            "the smoky taste spreads through everything. If it has gone all the way through, a splash "
            "of stock and something creamy hides a little of it, but a properly burnt sauce is better "
            "started again.")


_FRIED_GREASY = ("chips", "chip", "fries", "fry", "pakora", "pakoras", "onion rings", "doughnut",
                 "doughnuts", "tempura", "batter", "fried", "sweet potato fries")
_POT_GREASY = ("stew", "curry", "sauce", "soup", "gravy", "chilli", "bolo", "bolognese", "ragu",
               "casserole", "dal", "daal", "stir fry", "stirfry", "stir-fry", "mince")
_MEAT_GREASY = ("roast", "chicken", "steak", "lamb", "pork", "beef", "sausage", "sausages",
                "bacon", "duck", "turkey", "gammon", "burger", "burgers", "meatballs")
_PASTRY_GREASY = ("quiche", "pie", "tart", "pastry", "pastry case", "flan")


def _greasy(memory, understood):
    words = [str(word).lower() for word in ((understood or {}).get("words") or [])]
    said = " ".join(words)
    have = lambda names: (any(_same(word, wanted) for word in words for wanted in names)
                          or any(" " in wanted and wanted in said for wanted in names))
    if have(_FRIED_GREASY):
        return ("Greasy fried food means the oil was not hot enough, so the food steamed instead of "
                "sealing and took the fat up like a sponge: 180C for chips and about 190C for a "
                "batter, test it with a cube of bread that should sizzle and go golden in 30 seconds, "
                "and do not crowd the pan, because the temperature drops as soon as it is full. "
                "Drain on a rack or kitchen paper, never on a plate, and salt it the moment it comes out.")
    if any(_same(word, wanted) for word in words
           for wanted in ("roast potatoes", "roasties", "potatoes", "potato", "wedges",
                          "hash browns")) and any(_same(word, wanted) for word in words
                                                  for wanted in ("roast", "roasted", "oven")):
        return ("Greasy roast potatoes mean the oil was not hot enough or the tin was crowded: parboil "
                "them 8 minutes, drain and shake the pan to rough the edges, then roast them in a "
                "thin layer of oil that is already smoking hot at 200C (180C fan), in one layer with "
                "room between them. Cold oil, or a full tin, is what leaves them oily, and a rack "
                "over the tin drains the rest.")
    if have(_PASTRY_GREASY):
        return ("A greasy pastry case is the filling rather than the pastry: cheese in a quiche gives "
                "up its fat, and mince in a pie floats it to the top. Drain the cooked filling in a "
                "sieve over a bowl, thicken it with a spoon of cornflour, and blind-bake the case "
                "first so the fat has somewhere to go; a layer of breadcrumbs on the base soaks up "
                "the rest.")
    if have(_MEAT_GREASY):
        return ("Most of that fat is meant to be there, so spoon it off rather than cook it away: tilt "
                "the tin and take the fat out with a spoon or a bulb baster, keeping a spoonful for "
                "the potatoes, and finish the meat uncovered at a higher heat for the last 10 minutes "
                "so the skin or the outside crisps. Resting it on a rack, not in the tin, keeps it "
                "out of the fat.")
    if have(_POT_GREASY):
        return ("Skim the fat off the top with a spoon, or lay a piece of kitchen paper flat on the "
                "surface and lift it out - that takes the oil and leaves the sauce. A stew that is "
                "still greasy wants the lid off for 10 minutes, and a spoon of something sharp "
                "(lemon, vinegar, tomato puree) cuts through what is left. Next time brown the meat "
                "and pour the fat out of the pan before the liquid goes in.")
    return ("Greasy comes from too much oil or oil that was not hot enough to seal the food: get the "
            "pan properly hot before anything goes in, shake the excess off in a sieve, and drain on "
            "kitchen paper rather than on a plate. In a sauce, skim the fat off the top with a spoon "
            "and finish with a squeeze of lemon.")


_CUSTARD_NAMES = ("custard", "custards", "creme anglaise", "crème anglaise", "creme patissiere",
                  "crème pâtissière", "pastry cream", "custard tart", "custard tarts",
                  "custard filling", "creme caramel", "crème caramel")


def _split(memory, understood):
    words = [str(word).lower() for word in ((understood or {}).get("words") or [])]
    said = " ".join(words)
    if any(_same(word, name) for word in words for name in _CUSTARD_NAMES) or any(
            " " in name and name in said for name in _CUSTARD_NAMES):
        return ("A curdled custard is the eggs getting hot too fast, so the protein in them sets "
                "into grains: take it off the heat at once, whisk in a spoonful of cold cream or "
                "milk to stop it cooking, then push it through a sieve and it comes back smooth. "
                "Next time pour the hot milk into the beaten eggs a splash at a time, keep the pan "
                "over a low heat, stir all the time, and take it off at 82C, because a custard that "
                "comes to the boil will always curdle.")
    if any(word in ("mayonnaise", "mayo", "aioli", "garlic mayo", "garlic mayonnaise", "remoulade")
           for word in words):
        return ("Mayonnaise splits when the oil goes in faster than the yolk can take it up, so start "
                "again with a clean bowl: an egg yolk, a teaspoon of water and a pinch of salt, then "
                "the oil a drop at a time until it thickens and only then in a thin stream. To rescue "
                "a split one, put a fresh yolk in a clean bowl and whisk the split mayonnaise into it "
                "a spoon at a time - one yolk will bring back up to about a mugful.")
    if any(word in ("hollandaise", "béarnaise", "bearnaise", "butter sauce") for word in words):
        return ("Hollandaise splits when the bowl gets too warm or the butter goes in too hot: take "
                "the bowl off the water at once, add a teaspoon of cold water and whisk hard. If it "
                "will not come back, start a fresh yolk in a clean bowl with a spoon of water and "
                "whisk the split sauce into it a little at a time, off the heat. Next time keep the "
                "water barely trembling and let the melted butter cool for a minute first.")
    return ("A sauce splits when it gets too hot: take it off the heat and whisk in a spoonful of cold "
            "cream or butter to bring it back. Next time, lower the heat and add dairy at the end.")


_UNDER_BAKE = ("cake", "cakes", "sponge", "muffin", "muffins", "loaf", "loaves", "bread", "buns",
               "bun", "scone", "scones", "brownie", "brownies", "traybake", "yorkshire",
               "yorkshires", "pudding", "puddings", "pie", "tart", "quiche")
_UNDER_BREAD = ("bread", "loaf", "loaves", "sourdough", "bread roll", "bread rolls")
_UNDER_STARCH = ("rice", "couscous", "quinoa", "bulgur", "bulghur", "barley", "lentils", "lentil",
                 "porridge", "oats", "polenta", "pasta", "noodles", "noodle", "spaghetti",
                 "macaroni", "penne", "tagliatelle", "gnocchi", "dumplings", "dumpling")
_UNDER_VEG = ("vegetables", "vegetable", "veg", "greens", "potato", "potatoes", "carrots", "carrot", "parsnips", "parsnip", "swede", "turnip",
              "sprouts", "broccoli", "cauliflower", "cabbage", "beans", "peas", "leeks", "leek",
              "beetroot", "squash", "pumpkin", "courgette", "courgettes", "aubergine")


def _undercooked(memory, understood):
    words = [str(word).lower() for word in ((understood or {}).get("words") or [])]
    said = " ".join(words)
    have = lambda names: (any(_same(word, wanted) for word in words for wanted in names)
                          or any(" " in wanted and wanted in said for wanted in names))
    if have(_UNDER_BREAD):
        return ("A doughy loaf has not had long enough in the oven, or it did not prove enough: put it "
                "back in at 200C (180C fan) for 10 minutes, then turn it out and tap the base - a "
                "hollow sound means it is done, a dull thud means it wants 5 more. Next time let it "
                "prove until a poke springs back slowly and bake it to 96C in the middle rather than "
                "trusting the time on the packet.")
    if have(_UNDER_BAKE):
        return ("Put it back in the oven at 160C (140C fan) for 10 minutes with a sheet of foil "
                "loosely over the top, so the middle catches up without the top burning, and test it "
                "again with a skewer: it wants a few damp crumbs, not wet mixture. Next time drop "
                "the oven 10C and give it 5 minutes longer, and check with a skewer before you take "
                "it out - a cake that looks set and wobbles in the middle is not done.")
    if have(_UNDER_STARCH):
        return ("It wants more time and a little more water: a splash of hot water, the lid back on "
                "and 5 minutes on the lowest heat will finish rice, couscous or quinoa. Pasta and "
                "noodles go back into the boiling water for 2 to 3 minutes, and lentils want another "
                "10. Taste a piece rather than looking at the clock, because the packet time assumes "
                "a pan that came back to the boil quickly.")
    if have(_UNDER_VEG):
        return ("Boiled vegetables go hard in the middle when the pieces are different sizes or the "
                "water never got back to a rolling boil: cut them the same size, salt the water, and "
                "give them another 5 minutes, testing with the point of a knife - it should slide in "
                "with no resistance at all. Roast ones want 10 more minutes in a hotter oven, and "
                "parboiling potatoes for 8 minutes before they go in the tin stops the hard centre.")
    return ("It needs a few more minutes rather than more heat: cover it and give it 5, then test it "
            "with a knife or a skewer in the middle, where the heat gets last. A wider, shallower "
            "dish cooks through faster than a deep one.")
_DIP_FIXES = (
    (("houmous", "hummus", "humous"),
     "Houmous thickens in the fridge, so loosen it with a spoonful of cold water or lemon juice "
     "and a little more oil, taste for salt, and serve it at room temperature."),
    (("tzatziki", "raita", "yogurt dip", "yoghurt dip"),
     "Sit it in a sieve over a bowl for twenty minutes: thin tzatziki or raita is nearly always a "
     "wet cucumber, so squeeze the grated cucumber dry and stir it back in with a pinch of salt."),
    (("aioli", "mayonnaise", "mayo"),
     "A thin mayonnaise takes more oil whisked in slowly; a split one comes back from a fresh "
     "yolk in a clean bowl with the split mixture drizzled in a few drops at a time."),
    (("guacamole",),
     "Guacamole browns where the air gets at it: press cling film right onto the surface, keep "
     "the stone in the bowl if you have one, and a squeeze of lime slows it down. It is still "
     "fine to eat brown."),
    (("salsa",),
     "Drain the chopped tomato in a sieve for ten minutes and salt it at the end: salsa goes "
     "watery from the tomato juice, and a spoonful of tomato puree thickens what is left."),
    (("baba ganoush", "tapenade"),
     "It wants balancing rather than more of anything: a squeeze of lemon and a little olive oil "
     "stirred in slowly will loosen it, and salt and lemon are what it usually lacks."),
)

_DIP_PLAIN = ("A cold dip is put right cold, so leave the pan alone: a spoonful of water or lemon "
              "loosens it, a pinch of salt and twenty minutes in a sieve thickens it, and a little "
              "oil whisked in slowly brings back one that has split.")


OIL_SMOKE_POINTS = (
    ("butter, or clarified butter", "about 150C"),
    ("extra virgin olive oil", "about 180 to 200C"),
    ("a plain or light olive oil", "about 200 to 240C"),
    ("rapeseed, sunflower or vegetable oil", "about 220 to 230C"),
    ("groundnut or rice bran oil", "about 230C"),
)


_BODY_PART = re.compile(
    r"\b(?:arm|arms|hand|hands|finger|fingers|thumb|thumbs|foot|feet|toe|toes|wrist|wrists|"
    r"leg|legs|chest|tummy|stomach|belly|lap|neck|shoulder|shoulders|eye|eyes|face|skin|"
    r"baby|child|toddler|kid)\b")
_ONTO_A_PERSON = ("splashed", "splashes", "splash", "spat", "spits", "spitting", "spit",
                  "flicked", "jumped out", "pops", "popped", "scalded", "burnt my", "burned my",
                  "burnt me", "burnt himself", "burnt herself", "burned me")


def _a_dish_with_a_heat(text):
    from . import dishes
    plan = dishes.PLANS.get(dishes.dish_in(str(text or "")) or "")
    return bool(isinstance(plan, dict) and plan.get("temp"))


def _fat_has_landed_on_a_person(text):
    return bool(_BODY_PART.search(text)) and any(word in text for word in _ONTO_A_PERSON)


_SOMETHING_IS_WRONG_WITH_THE_PAN = (
    "smoke", "smokes", "smoking", "smoked", "smoky", "smoke point", "smoking point",
    "burnt", "burn", "burns", "burning", "burned", "too hot", "overheat", "overheating",
    "on fire", "caught fire", "in flames", "flaming", "flamed", "black", "spoiled",
    "ruined", "wasted", "not right", "gone wrong", "tastes", "taste", "smell", "smells",
    "stinks", "bubbling", "bubbles", "foam", "foams", "foaming", "foamy",
    "spat", "spits", "spitting", "spattered", "splashed", "jumped out", "popped",
)


def _oil_smoking(memory, understood):
    understood = understood if isinstance(understood, dict) else {}
    text = str(understood.get("clean") or understood.get("text") or "").lower()
    if _fat_has_landed_on_a_person(text):
        return ""
    if _burnt_on_the_pan(text):
        return ""
    if _says(text, ("smoke point", "smoking point", "smokes at", "smoke at", "smoke too")):
        return ("Every fat has a smoke point: " + "; ".join(
            f"{name} {temp}" for name, temp in OIL_SMOKE_POINTS) +
            ". Above that it is breaking down, so keep the pan under it - a thermometer takes the "
            "guesswork out, and a drop of the oil in a cold pan, brought up slowly, tells you when "
            "it is ready.")
    if _says(text, ("in the water", "pasta water", "rice water", "boiling water", "the water for",
                    "water for the pasta", "water for the rice", "in the pot of water",
                    "into the water", "salt water", "salted water", "the pasta water")):
        return ""
    if _says(text, ("put the oil in", "put in the oil", "add the oil", "adding the oil",
                    "put oil in", "add oil to", "adding oil", "add oil",
                    "oil go in", "oil goes in", "oil first or the pan", "pan first",
                    "oil in the pan", "oil in a pan", "oil in pan",
                    "hot pan first",
                    "pan be hot", "pan hot before", "before the oil", "before adding the oil",
                    "before adding oil", "hot pan",
                    "pan hot before", "when do i add the oil")):
        return ("Pan first, then the oil: a dry pan heats faster and you can watch the oil for the "
                "heat - it thins and shimmers at about 180C, and a cube of bread turns golden in 30 "
                "seconds. Give the oil 20 seconds before the food goes in. Cold oil in a cold pan "
                "is for rendering fat, not a sear.")
    if not _says(text, ("oil", "fat", "pan", "fry", "frying", "deep fry", "chip pan",
                         "dripping", "lard", "ghee", "wok")) and _a_dish_with_a_heat(text):
        return ""
    if _says(text, ("how hot", "hot enough", "what temperature", "temperature for", "hot should",
                    "heat of the oil", "temperature does",
                    "is hot", "is ready", "pan heat", "the heat", "test the heat",
                    "check the heat", "hot oil", "oil is hot", "oil is ready", "fat is hot",
                    "fat is ready", "heat the pan", "heating the pan", "heat the oil",
                    "heating the oil")):
        return ("Around 180C for most frying, 170C for chips so they cook through before they "
                "colour; with no thermometer a cube of day-old bread turns golden in about 30 "
                "seconds. Heat the oil with nothing in it and fry in small batches so it does not "
                "drop. Stay under the fat's smoke point: "
                + "; ".join(f"{name} {temp}" for name, temp in OIL_SMOKE_POINTS[:1] + OIL_SMOKE_POINTS[2:4])
                + ".")
    _fat_named = _says(text, ("oil", "fat", "dripping", "lard", "ghee", "grease", "butter"))
    if _fat_named and _says(text, ("down the sink", "down the drain", "down the toilet",
                                   "down the loo", "down the plug hole", "down the plughole")):
        return ("No - never down the sink, the loo or the drain: fat sets hard as it cools and "
                "closes the pipe, and hot water only pushes it further down to block somewhere "
                "worse, which is a plumber's bill. Let it cool, pour it into the bottle or a jar "
                "you were going to bin, and put that in the rubbish; wipe the pan out with kitchen "
                "roll before you wash it.")
    if _fat_named and _says(text, ("throw out", "throw away", "throwing out", "get rid", "getting rid",
                    "dispose", "disposal", "bin it", "bin used", "bin the oil", "recycle",
                    "recycling", "down the sink", "where do i put", "where do i pour",
                    "what to do with",
                    "where does it go", "where can i put", "put used", "pour it", "pour old",
                    "do with old oil", "do with used oil", "do with the oil", "do with the fat",
                    "do with leftover oil", "what do i do with", "where does it go", "pour it",
                    "pour the oil", "tip it")):
        return ("Let it cool completely, then funnel it back into the bottle it came in or any "
                "screw-top jar you were going to bin, and put that in the rubbish - never down the "
                "sink, because it sets in the drain and it is what makes fatbergs. A small amount "
                "from one pan can be soaked up with kitchen roll and binned; a big batch goes to "
                "the tip, and most councils and some supermarkets take used cooking oil for "
                "recycling. Keep a jar under the sink and pour into it while it is still warm, and "
                "it never gets as far as the drain.")
    if _says(text, ("reuse", "re-use", "again", "second time", "keep the oil", "straining",
                    "strain", "can i use", "can i still use", "still use", "still good",
                    "fine to use", "ok to use", "okay to use", "fry in", "fry with")):
        return ("Let it cool, strain it through a fine sieve or a coffee filter, and use it once "
                "more for something at a lower heat. Oil that has smoked has started to break "
                "down, so it will taste acrid and it will smoke sooner next time; bin it if it "
                "smells bitter or looks dark and sticky.")
    if _says(text, ("foam", "foams", "foamy", "foaming", "foamed", "bubbling up", "bubbles up",
                    "spitting",
                    "spits", "spattered", "spattering")):
        return ("Oil that foams has water in it rather than too much heat: dry the food with kitchen "
                "paper and lower it in gently, cook in two batches so the pan does not drop below "
                "its temperature, and keep the lid or the basket dry. If oil you have already used "
                "a few times foams as soon as anything goes in, it is spent - let it cool, bin it "
                "in a bottle, and start with fresh.")
    if not _says(text, _SOMETHING_IS_WRONG_WITH_THE_PAN):
        return ""
    return ("The fat is past its smoke point, so turn the heat down and take the pan off the ring "
            "for a minute rather than carrying on. Open a window or put the extractor on, and once "
            "it has cooled wipe the pan out and start again with fresh fat - the smoked oil has "
            "turned acrid and it will make the food taste of it. Butter and extra virgin olive oil "
            "smoke first (about 150C and 180C), so use a plain vegetable oil or clarified butter "
            "when you want the pan very hot. If it ever actually catches, put a lid or a baking "
            "tray over the pan and turn the heat off - never water.")


def _dip_fault(understood):
    text = ((understood or {}).get("clean") or "").lower()
    if any(name in text for name in ("houmous", "hummus", "humous")):
        if any(word in text for word in ("watery", "too thin", "runny", " thin")):
            return ("Watery houmous usually has too much liquid or not enough tahini: drain the "
                    "chickpeas well, then stir in a spoonful of tahini and a little olive oil and "
                    "chill it for 20 minutes, because it firms up cold. Taste for salt and lemon "
                    "at the end.")
    for names, fix in _DIP_FIXES:
        if any(name in text for name in names):
            return fix
    return _DIP_PLAIN


_SOGGY_BREAD = ("sandwich", "sandwiches", "wrap", "wraps", "roll", "rolls", "baguette", "sub",
                "subs", "ciabatta", "pitta", "pita", "tortilla", "toastie", "butty", "butties",
                "bread", "loaf", "bun", "buns", "brioche", "focaccia", "sourdough")
_SOGGY_LEAF = ("salad", "salads", "lettuce", "leaves", "coleslaw", "slaw", "pasta salad",
               "greens", "spinach", "rocket", "cucumber", "tomato", "tomatoes")


def _soggy_lunch(memory, understood):
    words = [str(word).lower() for word in ((understood or {}).get("words") or [])]
    said = " ".join(words)

    def _names(family):
        return (any(_same(word, name) for word in words for name in family)
                or any(" " in name and name in said for name in family))

    if _names(_SOGGY_BREAD):
        return ("A sandwich goes soggy because the wet filling soaks into the bread: butter both "
                "slices right to the edges first, or spread mayonnaise or soft cheese as a "
                "barrier, and keep tomato, cucumber and lettuce in the middle rather than against "
                "the bread. Packed in the morning, the wet things go in a separate tub and are "
                "added at lunchtime, which is the only thing that really works on a hot day.")
    if _names(_SOGGY_LEAF):
        return ("A salad goes soggy because the leaves are still wet or the dressing went on early: "
                "dry them properly in a tea towel or a salad spinner, dress it at the table, and keep "
                "the wet things - tomato, cucumber, dressing - at the bottom of the bowl until you "
                "eat. Salt draws the water out too, so season it in the last minute rather than "
                "ahead.")
    return ("A packed lunch goes soggy because water gets in from somewhere. Keep the wet things "
            "- tomato, cucumber, dressing, a drink - in their own tub and stand the leaky ones "
            "upright, put a layer of kitchen paper or a lettuce leaf under the bread, and pack the "
            "dry things on top. A leaking drink and a damp fork do more damage than a whole "
            "morning in the bag.")

_BAKE_FOLLOW_SHAPES = ("what did i do wrong", "what went wrong", "why did that happen",
                       "why does that happen", "why did it happen", "what else could it be",
                       "why did they sink", "why did it sink", "why did that sink",
                       "why did some of them sink", "why do they sink", "why does it sink",
                       "how do i stop that next time", "how do i stop it next time",
                       "stop it next time", "what should i do differently",
                       "how do i get it right", "will it happen again", "what do i change",
                       "what could i do differently next time",
                       "can i still use it", "can i still eat it", "can i still use them",
                       "is it still ok", "are they still ok", "how do i use it up",
                       "what do i do with it now")
_NEXT_SHAPES = ("stop", "differently", "next time", "get it right", "happen again",
                "what do i change")
_USE_SHAPES = ("still use", "still eat", "still ok", "use it up", "what do i do with")
_BAKE_KEEP_SHAPES = ("how long does it keep", "how long will it keep", "how long do they keep",
                     "how long will they keep", "how long does it last", "how long will it last",
                     "how long do they last", "how long will they last", "will it keep",
                     "do they keep", "will they last")


def _bake_keep_sentence(bakes):
    said = " ".join(bakes)
    if any(word in said for word in ("scone", "scones", "biscuit", "biscuits", "cookie",
                                     "cookies", "shortbread")):
        return ("Scones and biscuits are at their best the day they are baked and keep 2 days in "
                "a tin; freeze them baked for 2 months and warm them through for 5 minutes at "
                "150C, which brings back most of the crust.")
    if any(word in said for word in ("bread", "loaf", "loaves", "sourdough", "bun", "buns",
                                     "roll", "rolls", "focaccia", "baguette")):
        return ("Bread keeps 2 to 3 days in a paper bag or a bread bin, cut side down, and a "
                "month in the freezer sliced; the fridge is what makes it stale fastest, so "
                "freeze what you will not eat in two days.")
    if "cupcake" in said or "muffin" in said:
        return ("Cupcakes and muffins keep 2 to 3 days in a tin, best the day they are baked, "
                "and they freeze well undecorated for 2 months: defrost them at room "
                "temperature in a single layer.")
    return ("A cake keeps 3 days in a tin, or freezes for 2 months undecorated; a crumbly or "
            "dry one is best eaten in the next day or two, or frozen in slices.")


def _bake_keep(memory, reading):
    line = str((reading or {}).get("text") or (reading or {}).get("clean") or "").lower()
    if not any(shape in line for shape in _BAKE_KEEP_SHAPES):
        return ""
    turns = (memory or {}).get("turns") or []
    for turn in reversed(turns[-3:]):
        said = str(turn.get("user") or "").lower() if isinstance(turn, dict) else ""
        if not any(name in said for name in _BAKED):
            continue
        if "cupcake" in said or "muffin" in said:
            return _bake_keep_sentence([said])
        return ""
    return ""


def _bake_follow(memory, reading):
    line = str((reading or {}).get("text") or (reading or {}).get("clean") or "").lower()
    if not any(shape in line for shape in _BAKE_FOLLOW_SHAPES):
        return ""
    turns = (memory or {}).get("turns") or []
    bakes = []
    for turn in reversed(turns[-3:]):
        said = str(turn.get("user") or "").lower() if isinstance(turn, dict) else ""
        if any(name in said for name in _BAKED):
            bakes.append(said)
    if not bakes:
        return ""
    family = None
    for said in [line] + bakes:
        for candidate in _BAKE_FAULT_FAMILIES:
            if any(word in said for word in candidate[0]):
                family = candidate
                break
        if family is not None:
            break
    if family is None:
        if any(shape in line for shape in _USE_SHAPES + _BAKE_KEEP_SHAPES):
            return _bake_keep_sentence(bakes)
        return ""
    _, cause, cure, rescue = family
    if any(shape in line for shape in _USE_SHAPES):
        return f"It is still worth eating: {rescue}."
    if any(shape in line for shape in _NEXT_SHAPES):
        if not cause[0].isupper():
            cause = cause[0].upper() + cause[1:]
        return f"Next time, {cure}. {cause}."
    return f"{cause}. {cure[0].upper() + cure[1:]}."


_BREAD_WORDS = ("bread", "loaf", "loaves", "sourdough", "bun", "buns", "roll", "rolls", "baguette",
                "focaccia", "pitta", "pita", "brioche", "ciabatta")
_GUMMY_CAKE = ("Gummy means it needed longer, not a hotter oven: the outside set while the middle "
               "was still wet. Give it another 5 to 10 minutes at the same heat with foil over the "
               "top, and test the centre with a skewer, not the edge.")
_GUMMY_BREAD = ("A gummy loaf is under-baked rather than under-proved: tap the base for a hollow "
                "sound, and if the middle feels heavy put it back for 10 minutes at the same heat. "
                "Next time prove until a floured finger springs back slowly.")


def _gummy(memory, understood):
    clean = (understood.get("clean") or "").lower()
    if any(re.search(r"(?<![a-z])" + word + r"(?![a-z])", clean) for word in _BREAD_WORDS):
        return _GUMMY_BREAD
    return _GUMMY_CAKE





from .cooking_entries import ENTRIES as _LISTED_ENTRIES
from .cooking_entries import NO_SUGAR as _NO_SUGAR

ENTRIES = list(_LISTED_ENTRIES)


_KINDS = (
    (("tea", "teas"), "tea",
     "Black, green, white and oolong are the same leaf, picked and processed differently: black "
     "is fully oxidised and malty, green is steamed or pan-fired and grassy, white is the young "
     "leaf dried, and oolong sits between green and black. Everything else - peppermint, "
     "chamomile, rooibos, fruit - is a herbal infusion rather than tea, so it brews and keeps "
     "differently."),
    (("pasta", "pastas"), "pasta",
     "Long pasta - spaghetti, linguine, tagliatelle - is for thin sauces that coat it. Short "
     "shapes - penne, fusilli, rigatoni - hold chunkier sauces, and the ridges and tubes are there "
     "to catch them. Filled pasta - ravioli, tortellini - is a meal with its sauce inside. Dried "
     "is durum wheat and water; fresh is egg and soft wheat, cooks in two or three minutes, and "
     "is richer. Wholewheat is the same shapes with the bran left in, and takes a minute longer."),
    (("oil", "oils"), "oil",
     "Olive oil splits in two: extra virgin is the cold-pressed first press, peppery and best "
     "raw or for low heat, and ordinary olive oil is refined, plainer and fine for frying. "
     "Rapeseed is the mild all-rounder and the cheapest British one. Sunflower and vegetable oil "
     "are neutral and take high heat, which is what chips and stir-fries want. Sesame is for "
     "flavour, a teaspoon at the end, and coconut oil tastes of coconut. Groundnut oil is the "
     "one restaurants fry in, because it is neutral and stable when hot."),
    (("honey", "honeys"), "honey",
     "It is named for the flower the bees worked: clover and acacia are light and mild, heather "
     "and chestnut are dark and strong, and orange blossom is perfumed. Runny or set is the same "
     "honey - set has simply crystallised, which a warm jug of water undoes. Raw or unfiltered "
     "means it has not been heated, so it is cloudier and tastes more of the flowers. Never give "
     "any honey to a baby under one, because of the botulism risk."),
    (("milk", "milks"), "milk",
     "Cow's milk comes by fat: whole at about 3.5%, semi-skimmed at 1.7% and skimmed at almost "
     "nothing, and the fat is what carries the taste in coffee and sauces. Fresh and UHT are the "
     "same milk, one pasteurised hotter so it keeps for months unopened. Goat's and sheep's are "
     "the other animals, sharper and richer. Plant milks - oat, soya, almond, coconut - are a "
     "different drink, and the barista ones are the ones that do not split in hot coffee."),
    (("bean", "beans"), "bean",
     "Dried or tinned is the first split: dried needs soaking overnight and a hard ten-minute "
     "boil, tinned is cooked and ready. After that it is the bean: kidney is the chilli one, "
     "cannellini and haricot are creamy and white (baked beans are haricot in tomato), black "
     "beans are earthy for Mexican food, and butter beans are the big soft ones. Chickpeas, "
     "lentils and split peas are the same family - pulses - and they cook without soaking."),
    (("lettuce", "lettuces"), "lettuce",
     "Crisphead - iceberg - is the crunchy one that keeps for a week and is mostly water. Cos, "
     "or romaine, is the upright one with a spine, and it is the one for Caesar. Butterhead - "
     "round and little gem - is soft and sweet, and wilts first. Loose-leaf - oakleaf, lollo "
     "rosso, frisée - is the curly one to tear into a bowl. Rocket and spinach are leaves sold "
     "beside it, not lettuce, and they are peppery or earthy rather than crisp."),
    (("wine", "wines"), "wine",
     "Red, white and rosé are about the skin, not the grape: red is fermented on it, white off "
     "it, and rosé briefly on it. Sparkling is a second fermentation for the bubbles, and "
     "fortified - sherry, port, madeira - has spirit added, which is why it keeps for weeks after "
     "opening. The other axis is the grape and where it grew, which is what makes a Chablis lean "
     "and a Chardonnay from a hot place buttery, and a wine dry or sweet."),
    (("coffee", "coffees"), "coffee",
     "Two beans: arabica is the fruity, slightly acidic one in most good coffee, and robusta is "
     "stronger, more bitter and has about twice the caffeine, which is why instant and cheap "
     "espresso blends use it. Roast runs from light, which keeps the fruit and the acidity, to "
     "dark, which tastes of the roast itself. Then it is ground to the brew: fine for espresso, "
     "medium for a filter machine, coarse for a cafetière. Instant is brewed and dried, a "
     "different drink, not a weaker one."),
    (("yoghurt", "yogurt", "yoghurts", "yogurts"), "yoghurt",
     "Natural is milk and cultures and nothing else, and it is what to cook with. Greek is the "
     "same yoghurt strained of its whey, so it is thicker and higher in protein; Greek-style is "
     "thickened with milk powder and is cheaper and sweeter. Set is cultured in the pot and stays "
     "firm, stirred is smooth. Skyr is strained further still, so it is very thick and very high "
     "in protein. Live yoghurt has the cultures still alive, which is the kind that helps an "
     "unsettled stomach."),
)

ENTRIES.extend(kinds_entries(_KINDS))



for _offered, _replaced, _verdict in _SWAP_VERDICTS:
    ENTRIES.append(entry("uses-%s-for-%s" % (_offered[0].replace(" ", "-"),
                                             _replaced[0].replace(" ", "-")),
                         (_offered, _replaced), _verdict, bias=2, ask=_SWAP_ASK,
                         avoid=tuple("%s instead of" % name for name in _replaced)))


FREEZER_WORDS = ("freeze", "freezes", "freezer", "frozen", "freezing")

STILL_FROZEN_WORDS = ("from frozen", "still frozen", "cooked from frozen", "cook it frozen",
                      "without defrosting", "without thawing", "no need to defrost")

COOKING_VERBS = re.compile(r"\b(?:cook|cooks|cooking|roast|roasts|roasting|bake|bakes|baking|"
                           r"fry|fries|frying|boil|boils|boiling|simmer|simmering|grill|"
                           r"grilling|steam|steaming)\b")


def _already_cooked_is_the_question(understood):
    text = " ".join(str((understood or {}).get("clean") or "").lower().split())
    if any(word in text for word in COOKED_KEEP_ASK):
        return True
    return not COOKING_VERBS.search(text)

KEEP_WORDS = ("keep", "keeps", "keeping", "shelf life", "shelf-life", "store", "storing",
              "reheat", "reheats", "reheating", "reheated",
              "storage", "stored", "last",
              "lasts", "longer", "go off", "goes off", "gone off",
              "going off", "sprout", "sprouts", "sprouting", "soft", "gone soft", "bendy",
              "mouldy", "mould", "moldy", "dried out", "dry out", "wilt", "wilted", "limp",
              "rot", "rotten", "green", "greening", "fridge",
              "next day", "the next day", "tomorrow", "past its date", "past the date",
              "out of date", "once opened", "once open",
              "still ok", "still good", "still fine", "still safe", "still edible",
              "are they ok", "are these ok", "ok to eat", "safe to eat",
              "smell", "smells", "smelling", "smelly", "tastes old", "taste old", "tastes off",
              "tastes funny", "tastes strange", "tasted old", "gone stale", "tastes stale",
              "tastes sour", "smells off", "smells funny", "smells sour", "smells musty")


ENTRIES.append(entry("gone-off-pot",
                     (("soup", "soups", "stew", "stews", "broth", "curry", "curries",
                       "chilli", "casserole", "gravy", "sauce", "sauces", "dahl", "dal",
                       "tagine", "goulash", "leftovers", "yogurt", "yoghurt", "custard",
                       "cream", "rice", "risotto rice", "pasta", "pot", "tub", "batch", "food",
                       "potato", "potatoes", "jacket potato", "boiled potatoes", "spuds",
                       "bolognese", "ragu", "risotto", "chowder", "hotpot", "stock", "stocks"),
                      ("mould", "moulds", "mouldy", "mold", "moldy", "gone off", "gone bad",
                       "slimy", "sliminess", "slick", "smells odd", "smell odd",
                       "gone sour", "smells off", "smells funny", "smells wrong", "smells bad",
                       "smelt off", "tastes off", "tastes funny", "tastes wrong",
                       "tastes sour", "smelly", "fizzy", "fizzing",
                       "fuzz", "furry", "fuzzy")),
                     "Bin it. Mould, an off smell or a slimy feel in a soup, sauce, stew or a "
                     "cooked grain means threads and bacteria under the surface where you cannot "
                     "see them, and heating it through does not make it safe - the opposite of "
                     "hard cheese. A pot that tastes sharp, fizzes or has bubbles is the same "
                     "answer with no mould showing.",
                     bias=2,
                     avoid=("cheese", "cheeses", "bread", "loaf", "loaves", "sour cream",
                            "hand cream", "body cream", "shaving cream", "nappy cream",
                            "face cream", "facial cream", "eye cream", "spot cream",
                            "eczema cream", "cold cream", "moisturiser", "moisturizer",
                            "sun cream", "suncream", "sunscreen", "sunblock", "lip balm",
                            "lip salve", "aftershave", "toner",
                            "plant", "plants", "houseplant", "house plant", "compost",
                            "potting soil", "potting compost", "soil", "seedling", "seedlings",
                            "garden", "terracotta", "saucer",
                            "chicken", "chickens", "meat", "beef", "pork", "lamb", "fish",
                            "dog", "dogs", "puppy", "pup", "pups", "cat", "cats",
                            "kitten", "kittens", "pet", "pets", "vet", "rabbit", "hamster",
                            "going off", "goes off", "do they go off", "does it go off",
                            "keep food from", "keep from", "prevent", "stop food", "last longer",
                            "make it last", "shelf life", "how long",
                            "joke", "jokes", "comedy",
                            "sourdough", "dough", "starter", "yeast", "prove", "proving",
                            "rise", "rising", "ferment", "fermenting", "kombucha", "kimchi",
                            "brew", "brewing", "curdle", "curdled", "curdling", "separated",
                            "stock cube", "stock cubes", "stock pot", "stockpot",
                            "split", "split sauce", "sauce split",
                            "off her food", "off his food", "off their food",
                            "off our food", "off my food", "off your food",
                            "gone off food", "gone off eating",
                            "dog", "dogs", "puppy", "pup", "puppies", "cat", "cats",
                            "kitten", "kittens", "pet", "pets", "vet")))

ENTRIES.append(entry("keep-eggs", (("egg", "eggs"), KEEP_WORDS),
                     "Raw eggs keep about three weeks past the date on the box if they have stayed "
                     "cold, so the fridge is the place for them: in their carton on a shelf rather "
                     "than in the door, where the temperature swings. Go by the date and by how "
                     "they smell when you crack one.",
                     bias=1,
                     avoid=("salad", "sandwich", "sandwiches", "sarnie", "butty", "mayo",
                            "mayonnaise", "cress", "filler",
                            "every day", "everyday", "every morning", "daily", "a day",
                            "per day", "how many",
                            "ok to eat a day", "ok to eat every", "okay to eat every",
                            "fine to eat every", "good for you",
                            "healthy", "cholesterol", "too many", "how often")))
ENTRIES.append(entry("keep-egg-salad", (("egg salad", "egg mayonnaise", "egg mayo",
                                         "egg sandwich", "egg sandwiches", "egg sarnie",
                                         "egg and cress"),
                                        KEEP_WORDS + ("out", "overnight", "tomorrow")),
                     "Egg salad keeps 2 days in the fridge, covered, on a shelf rather than in the "
                     "door, and no more than 2 hours out at room temperature before it should go "
                     "in the bin: mayonnaise and boiled egg together is the part that turns. If it "
                     "has sat out at a picnic since morning, don't risk it.",
                     bias=2))
ENTRIES.append(entry("keep-boiled-eggs", (("egg", "eggs"),
                                          ("boil", "boiled", "boiling", "cooked", "hard boiled",
                                           "shell on", "peeled", "devilled", "deviled")),
                     "Boiled eggs keep about a week in the fridge with the shell on, and 2 to 3 "
                     "days once peeled, in a covered bowl of water. Raw ones in their shells keep "
                     "far longer: about three weeks past the date on the box if they stayed cold.",
                     ask=("keep", "keeps", "keeping", "kept", "last", "lasts", "store", "stored",
                          "fridge", "ok", "safe", "week", "days",
                          "good for"),
                     bias=2))


COOKED_WORDS = ("boil", "boiled", "boiling", "cooked", "leftover", "leftovers", "left over",
                "reheat", "reheated", "mashed", "roasted")

USE_UP_WORDS = ("what can i do with", "what do i do with", "what to do with",
                "what can i make with", "what can i cook with", "use up", "use them",
                "using up", "recipe", "recipes", "idea", "ideas")

COOKING_WORDS = ("oven", "bake", "baking", "baked", "roast", "roasted", "fry", "frying",
                 "grill", "temperature", "minutes", "heat",
                 "microwave", "microwaved", "microwaving", "steam", "steamed", "steaming",
                 "poach", "poached", "poaching")

STORING = ("how do i store", "how should i store", "how do you store", "best way to store",
           "how to store", "storing")

KEEP_DATE_WORDS = ("out of date", "past the date", "past its date", "use by", "best before",
                   "still ok", "still good", "still fine")
KEEP_EXTRA_WORDS = {food: KEEP_DATE_WORDS for food in ("butter", "cheese")}

MOULD_WORDS = ("mould", "mouldy", "mold", "moldy")
_SPOILT_WORDS = ("smell", "smells", "smelly", "smelt", "off", "gone off", "going off", "slimy",
                 "sour", "grey", "gray", "tacky", "separated", "watery", "fizzy", "mould",
                 "mouldy", "mold", "moldy", "pink", "rot", "rotten", "bad", "went bad")

KEEP_STAND_DOWN = {
                   "garlic": ("breath", "bad breath", "garlic breath", "breathe", "breathing",
                              "smell", "smells", "smelt", "smelled", "stinks", "burn", "burnt",
                              "burned", "burning", "bitter", "black", "went black"),
                   "cheese": STORING + MOULD_WORDS + (
                       "off", "is bad", "are bad", "gone bad"),
                   "cream": _SPOILT_WORDS + ("sun cream", "sunscreen", "hand cream", "face cream",
                                             "eye cream", "shaving cream", "moisturiser",
                                             "ice cream", "cream cheese", "cream tea",
                                             "cream cake", "cream cakes", "cream cracker",
                                             "cream crackers", "cream soda", "clotted",
                                             "creme egg", "cream liqueur"),
                   "avocado": _SPOILT_WORDS,
                   "mince": _SPOILT_WORDS,
                   "ham": _SPOILT_WORDS,
                   "lemons": ("juice", "juices", "squash", "cordial"),
                   "soup": ("paste", "pastes", "powder", "powders", "spice", "spices",
                            "seasoning", "seasonings", "stock cube", "stock cubes")
                           + MOULD_WORDS + ("moulds",)}

METHOD_WORDS = ("melt", "melts", "melting", "melted", "toast", "toasted", "toasting")

DONENESS = ("know when", "know if they are done", "when they are done", "when it is done",
            "how long to cook", "how long to boil", "how long to roast", "how long to bake",
            "how long to microwave", "how long to air fry", "how long to airfry",
            "how long to grill", "how long to fry", "how long to steam", "tender")

GREEN_SAFETY_WORDS = ("can i eat", "eat them", "eat green", "safe", "poison", "poisonous",
                      "toxic", "solanine", "solamine")

BAKED_LINE_WORDS = ("cake", "cakes", "sponge", "sponges", "drizzle", "muffin", "muffins",
                    "cupcake", "cupcakes", "biscuit", "biscuits", "cookie", "cookies", "scone",
                    "scones", "brownie", "brownies", "loaf", "loaves", "bread", "bun", "buns",
                    "pastry", "pie", "pies", "tart", "tarts", "flapjack", "shortbread",
                    "crumpet", "crumpets", "teacake", "teacakes")

_COOKED_KEEPING = ("cooked", "cook", "boiled", "mashed", "stewed", "roast", "roasted",
                   "leftover", "leftovers", "left over")
_KEEPING_ASK = ("keep", "keeps", "keeping", "store", "stored", "storage",
                "last", "lasts", "still ok", "still good", "gone off", "going off",
                "out of date", "use by", "overnight", "til tomorrow", "till tomorrow")
for _row in ENTRIES:
    if _row.id == "fridge-life":
        _row.avoid = _row.avoid + tuple(_name for _names, _ in KEEPS for _name in _names)
        ENTRIES.append(entry("fridge-life-cooked", (_COOKED_KEEPING, _KEEPING_ASK),
                             _row.reply, bias=1,
                             avoid=("rice", "burnt", "burned", "charred", "scorched",
                                    "burnt on", "caught on the bottom")))


_A_BLANK_FILLER = re.compile(r"\b(?:stuff|junk|odds and ends)\b")


def _a_food_and_not_a_blank(understood):
    clean = str((understood or {}).get("clean") or "").lower()
    return not _A_BLANK_FILLER.search(clean)


_OFF_ASK = ("off", "is bad", "are bad", "gone bad", "gone over", "past it", "off yet",
            "already off", "off to eat", "off by now")
_OFF_THE_THING = ("off the", "off my", "off your", "off his", "off her", "off its", "off them",
                  "off it", "cut off", "cutting off", "chop off", "chopping off", "slice off",
                  "skin off", "take the skin", "fat off", "off the bone", "turn off", "turned off",
                  "switch off", "switched off", "day off", "days off", "time off", "off work",
                  "off sick", "show off", "better off", "worse off", "off the menu",
                  "off the heat", "off the hob", "off the plate", "off the pan", "take it off",
                  "take them off")

KEEP_AHEAD_OF_THE_GENERAL = frozenset(("courgette", "aubergine", "broccoli", "radish",
                                       "butternut squash", "cabbage"))

for _names, _reply in KEEPS:
    _avoid = (STORING if "egg" in _names[0]
              else COOKED_WORDS + USE_UP_WORDS + COOKING_WORDS + DONENESS + METHOD_WORDS
              ) + BAKED_LINE_WORDS
    if _names[0] == "potato":
        _avoid = _avoid + GREEN_SAFETY_WORDS
    _avoid += KEEP_STAND_DOWN.get(_names[0], ()) + KEEP_QUALITY_WORDS + _OFF_THE_THING
    _key = KEEP_WORDS + _OFF_ASK + KEEP_EXTRA_WORDS.get(_names[0], ())
    _bias = 2 if _names[0] in KEEP_AHEAD_OF_THE_GENERAL else 1
    ENTRIES.append(entry("keep-%s" % _names[0], (_names, _key), _reply, avoid=_avoid,
                         bias=_bias, guard=_a_food_and_not_a_blank))

for _names, _reply in COOKED_KEEPS:
    ENTRIES.append(entry("cooked-keep-%s" % _names[0],
                         (_names, KEEP_WORDS + ("good for",) + FREEZER_WORDS),
                         _reply,
                         avoid=USE_UP_WORDS + ("raw", "uncooked", "freezer burn") + STILL_FROZEN_WORDS
                         + ("shelf life", "shelf-life")
                         + COOKED_KEEP_AVOID,
                         bias=2, ask=COOKED_KEEP_ASK,
                         guard=lambda u: _already_cooked_is_the_question(u)
                         and _a_food_and_not_a_blank(u)))


KEEPS_COOKED = (
    (("jacket potato", "jacket potatoes", "baked potato", "baked potatoes", "potato skins"),
     "A jacket potato is fine the next day: cool it within an hour, keep it in the fridge covered "
     "and eat it within 2 days, skin and all. Reheat it until it is piping hot right through, or "
     "cut it up and fry it - a foil-wrapped one left on the side overnight goes in the bin."),
    (("coleslaw", "slaw"),
     "Coleslaw keeps 3 days in the fridge once it is opened, and homemade 2, because it is the "
     "mayonnaise that turns. Keep the tub cold and eat it by the date on it, and bin slaw that "
     "smells sharp or has gone watery in the bottom of the tub."),
    (("scone", "scones", "fruit scone", "cheese scone"),
     "Scones are best the day they are made and keep 2 days in a tin, or a day in the fridge. "
     "Sprinkle them with water and give them 3 minutes in a warm oven to bring them back; freeze "
     "them on the day and refresh from frozen, and bin any with green on them."),
    (("sushi", "shop sushi", "sushi box"),
     "Shop sushi is made to be eaten the day you buy it: keep it in the fridge, eat it within 24 "
     "hours and do not leave it out on the side. The rice and the raw fish are what go off, so "
     "bin what is left rather than keeping it for tomorrow."),
    (("tuna", "tinned tuna", "tin of tuna", "canned tuna"),
     "An opened tin of tuna keeps 2 days in the fridge, emptied into a bowl with a lid - left in "
     "the tin it tastes of metal. Eat it cold in a sandwich or flake it through a sauce, and do "
     "not freeze it, because it comes back dry and woolly."),
    (("cooked salmon", "cooked fish", "leftover salmon", "leftover fish", "smoked salmon"),
     "Cooked salmon keeps 2 days in the fridge, covered, and it is better cold in a salad than "
     "reheated, which dries it out. Cool it within an hour of cooking and bin it after 2 days; "
     "smoked salmon keeps 3 days once the pack is open and freezes for a month."),
    (("prawn", "prawns", "cooked prawns", "king prawns"),
     "Cooked prawns keep 2 days in the fridge, in a sealed box away from anything raw, and ones "
     "from the deli counter keep a day less than a sealed pack. Eat them cold or warm them through "
     "in a sauce rather than frying them again, and bin any that smell of ammonia."),
    (("gravy", "gravies", "onion gravy", "leftover gravy", "brandy sauce"),
     "Gravy keeps 2 days in the fridge, less than the meat does, because it is mostly liquid and "
     "it cools slowly in the jug: get it in within 2 hours of making it, standing the jug in a "
     "bowl of cold water if it is still hot. Reheat it until it boils right through, and bin any "
     "that has sat out on the table all evening."),
    (("stuffing", "sage and onion", "forcemeat", "stuffing balls"),
     "Cooked stuffing keeps 2 days in the fridge and it is the leftover to be strict with, because "
     "it has been inside the bird and soaked up the juices: cool it within 2 hours, box it, and "
     "reheat it until it is piping hot right through. Stuffing that never went in the oven is a "
     "different thing and keeps as long as the bread in it."),
    (("custard", "homemade custard", "custard sauce", "creme anglaise"),
     "Homemade custard keeps 2 days in the fridge, in a jug with a lid or a sheet of cling film "
     "pressed onto the surface so no skin forms. Reheat it gently and stir rather than boiling it, "
     "and bin any that has stood on the table through dinner."),
    (("trifle", "trifles", "sherry trifle"),
     "A trifle keeps 2 days in the fridge, and it is the cream and the fruit that turn rather than "
     "the sponge: cover it once it is made and eat it within a day or two. Do not freeze it - the "
     "cream splits and the sponge goes watery."),
)
KEEPS_COOKED_WORDS = KEEP_WORDS + ("reheat", "reheating", "reheated", "heat up", "heated up",
                                  "warm up", "warmed up", "make ahead", "make it ahead",
                                  "do it ahead", "do that ahead", "ahead", "ahead of time",
                                  "in advance", "the day before", "day before", "the night before",
                                  "night before", "keep it warm")
for _names, _reply in KEEPS_COOKED:
    ENTRIES.append(entry("keep-" + _names[0].replace(" ", "-"), (_names, KEEPS_COOKED_WORDS),
                         _reply,
                         bias=1,
                         guard=_a_food_and_not_a_blank,
                         avoid=USE_UP_WORDS + DONENESS + (
                             "how long to cook", "how long to bake", "how long to boil",
                             "how long to fry", "how do i cook", "how do i make", "recipe",
                             "in the oven", "microwave", "air fryer", "temperature")))

for _row in ENTRIES:
    if _row.id == "fridge-life":
        _row.avoid = _row.avoid + tuple(_name for _names, _reply in KEEPS_COOKED
                                        for _name in _names)





LEFTOVER_IDEAS = {
    "egg": "Eggs going spare: a frittata or a tortilla takes six or eight at once with whatever "
           "veg is in the fridge, a quiche takes four plus milk and cheese, and meringues or a "
           "pavlova use up whites on their own. Hard boiled, they keep a week and make "
           "sandwiches, or halve them into a salad with mustard and oil.",
    "chicken": "Cooked chicken: shred it into a salad with mayonnaise, lemon and something "
               "crunchy, or stir it through fried rice with soy sauce and peas for a 10-minute "
               "dinner.",
    "potato": "Leftover potatoes: crush them a little and fry them in hot oil until crisp, or "
              "slice them into a frittata with eggs.",
    "pasta": "Leftover pasta: loosen it in a hot pan with a splash of water and a little oil, or "
             "bake it with a spoon of tomato sauce and cheese on top.",
    "salmon": "Leftover salmon: flake it through pasta or a salad with lemon and yoghurt, and "
              "don't reheat it hard or it dries out.",
    "bread": "Stale bread: tear it into croutons fried in oil and garlic, or blitz it into "
             "breadcrumbs and freeze them.",
    "lentil": "Leftover dhal: thin it with a splash of stock into soup, or eat it cold as a dip "
              "with bread and yoghurt.",
    "coconut milk": "Half a tin of coconut milk: simmer it with curry paste and whatever veg you "
                    "have for 10 minutes, or stir it into rice instead of water for a coconut "
                    "rice. It freezes in an ice cube tray for next time.",
    "cream": "Cream or soured cream going spare: stir it into a chilli or curry off the heat so "
             "it does not split, spoon it over baked potatoes or fruit, or let it down with a "
             "squeeze of lemon and use it as a dressing. Soured cream also freezes badly, so use "
             "it rather than keep it.",
    "sprout": "Leftover sprouts: halve them and fry cut side down in butter until they caramelise, "
              "about 8 minutes, or shred them raw into a salad with lemon, oil and toasted nuts.",
    "marrow": "Half a marrow left: scoop out the seeds, stuff it with mince and rice and bake it "
              "45 minutes at 190C (170C fan), or grate it into a curry - the water it gives up "
              "thickens the sauce as it cooks.",
    "buttermilk": "Buttermilk going spare: soda bread takes 284ml, or thin a pancake batter with "
                  "it, or marinate chicken in it for an hour before frying - it tenderises the meat.",
    "hot cross bun": "Buns going stale: butter them and bake them in a bread and butter pudding, "
                     "or halve and toast them under a grill with a little sugar on top.",
    "stuffing": "Leftover stuffing: shape it into balls and fry or roast them 15 minutes at 200C "
                "(180C fan), or press it into a tray and cut it into crisp squares - it is the "
                "best part of the tray, so do not bin it.",
    "porridge": "Leftover porridge: loosen it with milk and reheat it, or beat in an egg and fry "
                "spoonfuls in butter for oat fritters with jam.",
    "bolognese": "Leftover bolognese: bake it with pasta and white sauce, spoon it over a jacket "
                 "potato, or thin it with stock and beans into a soup.",
    "curry": "Leftover curry: reheat it once until piping hot and eat it with rice, or bake it "
             "under a mash topping for a curry pie.",
}

_NAMED_FOODS = tuple(sorted({word for aliases, _reply in PANTRY.values() for word in aliases}))

_FOODS_SAID = None


def _foods_said():
    global _FOODS_SAID
    if _FOODS_SAID is None:
        _FOODS_SAID = ({_fold(str(word).lower()) for word in _NAMED_FOODS}
                       | {_fold(str(word).lower()) for word in _STAPLE_NAMES})
    return _FOODS_SAID
LEFTOVER_SOUP = ("Soup is the easiest use of leftovers: soften an onion, add whatever veg you "
                 "have in order of toughness, cover with stock, simmer 20 minutes and blend or "
                 "leave it chunky - season at the end. Any cooked meat goes in for the last five "
                 "minutes only, and a spoon of something sharp (lemon, mustard, a splash of "
                 "vinegar) is what stops it tasting like a fridge. Whatever you reheat must be "
                 "piping hot all the way through once, and rice that has sat out is the one "
                 "thing to bin.")


def _leftover_meal_reply(memory, understood):
    from . import meals
    words = understood.get("words") or ()
    if isinstance(words, str):
        words = words.split()
    words = tuple(words) or tuple(str(understood.get("clean") or "").lower().split())
    named = meals.named_food(words, understood)
    if named in LEFTOVER_IDEAS:
        return LEFTOVER_IDEAS[named]
    if named:
        idea = PANTRY.get(named, (None, ""))[1] if isinstance(PANTRY.get(named), tuple) else ""
        if not meals.idea_is_a_dish(idea):
            said = meals.use_it_up(named)
            if said:
                return said
    return LEFTOVER_SOUP


ENTRIES.append(entry(
    "leftover-meal",
    (("leftovers", "leftover", "left over", "odds and ends", "bits and pieces",
      "left in the fridge"),
     ("make", "made", "cook", "meal", "dinner", "tea", "supper", "soup", "ideas",
      "recipe", "recipes", "what can i", "do with", "use up", "using up", "turn into",
      "throw", "waste")),
    _leftover_meal_reply,
    ask=("how", "what", "can", "could", "any", "ideas", "should", "do i", "i have",
         "need", "got", "have"),
    bias=-2,
    avoid=("how long", "safe", "safely", "fridge", "freezer", "freeze", "frozen", "refreeze",
           "re-freeze", "refroze", "defrost", "defrosted", "thawed", "reheat", "reheated",
           "room temperature", "left out", "gone off", "smell", "smells", "sick", "pregnant",
           "dog", "cat", "bin", "keep") + _NAMED_FOODS))
NOT_THIS_FOOD = {
    "sprout": ("bean sprout", "alfalfa", "mung", "soy sprout", "soya sprout"),
    "bean": ("bean sprout",),
    "butter": ("peanut butter", "peanut", "cocoa butter", "apple butter"),
    "corn": ("sweetcorn", "corned"),
    "cream": ("ice cream", "cream cheese", "cream cracker"),
    "chocolate": ("hot chocolate",),
    "buttermilk": ("buttermilk powder", "powdered buttermilk"),
    "rabbit": ("rabbit food", "rabbit pellets"),
    "duck": ("duck food",),
    "chicken": ("chicken food", "chicken pellets"),
    "rice": ("rice cake", "rice cakes", "rice crispy",
             "rice crispies", "rice krispie", "rice krispies", "rice cracker", "rice crackers",
             "rice paper", "rice vinegar", "rice wine", "rice flour", "rice drink"),
}

PLANT_MILKS = ("coconut milk", "oat milk", "soy milk", "almond milk", "rice milk",
               "cashew milk", "coconut cream")

LEFTOVER_WORDS = frozenset("leftover leftovers cooked stale yesterday".split())
LEFT_POINTER = ("what's left", "whats left", "what is left", "anything left", "some left",
                "is left", "left over", "leftovers", "use up", "using up")
LEFTOVER_PHRASES = ("left over", "left from", "use up", "using up", "got spare", "spare ",
                    "what's left", "whats left", "what is left", "anything left", "some left",
                    "is left", "left of the")

COOKED_WORDS = frozenset("""
leftover leftovers cooked roast roasted mashed already precooked pre-cooked yesterday
""".split())

JOINERS = frozenset("and or plus with also then &".split())


def _words_just_before(folded, place, reach):
    window = []
    for word in reversed(folded[max(0, place - reach):place]):
        if word in JOINERS:
            break
        window.append(word)
    return window

MEAL_CUES = frozenset("""
make makes made making cook cooking bake baking baked meal meals dinner tea lunch supper brunch snack
idea ideas recipe recipes quick quickish something anything leftover leftovers use eat
""".split())

MEAL_WANTS = ("i fancy", "i really fancy", "fancy something", "fancy a ", "could go for",
              "could murder", "in the mood for", "i'd love", "i would love", "i quite fancy",
              "i'd quite like", "i would quite like")

MEAL_PHRASES = MEAL_WANTS + ("what can i do with", "what do i do with", "what to do with", "use up",
                "something with", "something quick", "something easy", "make with",
                "cook with", "recipes with", "recipes for", "recipe with", "recipe for",
                "ideas with", "meal with", "dish with", "recipe", "recipes", "idea", "ideas",
                "dinner ideas", "lunch ideas", "meal ideas",
                "what can i make", "what can i cook", "what should i make", "what should i cook",
                "thing to do with", "things to do with", "easiest thing to do with",
                "using up", "any ideas", "got left",
                "what should i do with", "what should i make", "what should i cook",
                "what else can i do with",
                "i have", "i've got", "ive got", "we have", "we've got", "weve got",
                "only have", "only got", "just have", "just got", "left in the",
                "in the fridge", "in the cupboard",
                "on their way out", "on the way out", "past its best", "past their best",
                "need using", "needs eating", "going over", "starting to go")

BOUGHT_PHRASES = ("i bought", "i've bought", "ive bought", "just bought", "i got a",
                  "i got some", "picked up a", "picked up some", "i brought home",
                  "we bought", "we got a")

MEAL_ASK_PHRASES = MEAL_WANTS + ("what can i do with", "what do i do with", "what to do with",
                                 "use up", "using up", "any ideas", "ideas", "idea", "got left",
                                 "thing to do with", "things to do with",
                    "easiest thing to do with",
                    "what else", "anything else", "something else", "any suggestions",
                    "suggestions",
                    "going soft", "gone soft", "going off", "on its way out", "needs using",
                    "to use up", "left over", "leftover",
                    "on their way out", "on the way out", "past its best", "past their best",
                    "need using", "needs eating", "going over", "starting to go",
                    "too much", "too many", "a lot of", "lots of", "loads of", "plenty of",
                    "glut of", "overrun with", "spare ")

FOOD_CUES = frozenset("""
dinner lunch supper brunch meal meals tea cook cooking bake baking recipe recipes idea ideas
leftover leftovers
""".split())

NOT_MEAL_ASKS = frozenset("how_long how_much how_often how why".split())

USE_UP_ASKS = ("use up", "using up", "use it up", "use them up", "use this up",
               "use that up", "use these up", "use those up", "to use up", "uses up",
               "use the rest", "what can i do with", "what do i do with", "what to do with",
               "what can i make with", "what can i cook with", "what should i do with")

RESTRICTED_EATING = (
    "only eat", "only eats", "only ate", "only ever eats", "will only eat",
    "will only eats", "only drink", "only drinks", "wont eat", "won't eat",
    "will not eat", "wont touch", "refuses to eat", "refuse to eat", "refuses to touch",
    "eats nothing but", "eat nothing but", "eats hardly anything", "lives on",
    "fussy eater", "picky eater", "is that normal", "is it normal",
)
SUBSTITUTE_WORDS = frozenset("""
substitute substitutes substitution substitutions instead swap swaps swapping replace replaces
replacing replacement alternative alternatives
""".split())
SUBSTITUTE_PHRASES = ("out of", "ran out", "run out", "no more", "none left", "in place of")

PROBLEM_WORDS = frozenset("""
safe safely safety poison poisoning reheat reheated reheating raw undercooked overcooked
overcook undercook mould mouldy mold moldy expired expiry defrost thaw thawed freezer
ill sick stomach allergic allergy date burnt burned
pox chickenpox flu fever cough poorly unwell infection virus covid sore headache migraine
toothache nausea nauseous vomiting diarrhoea rash bleeding pregnant
""".split())

ACTIVITY_PHRASES = ("easter egg", "easter eggs", "play dough", "playdough", "decorate", "decorating",
                    "dye ", "dyed", "paint the", "painted", "craft", "costume", "trick or treat",
                    "stocking filler", "advent calendar", "science experiment", "volcano")

MAKING_IT_YOURSELF_PHRASES = ("make my own", "make our own", "making my own", "making our own",
                              "made my own", "made our own", "make it myself",
                              "make them myself", "make it ourselves", "make them ourselves",
                              "make your own", "making your own", "from scratch")

ILLNESS_PHRASES = ("a cold", "my cold", "his cold", "her cold", "got a cold", "a temperature",
                   "runny nose", "sore throat", "feel sick", "feeling sick", "being sick")

SICK_PHRASES = ("im sick", "i'm sick", "i am sick", "ive been sick", "i've been sick",
                "being sick", "feel sick", "feeling sick", "felt sick", "im ill", "i'm ill",
                "i am ill", "been ill", "feeling ill", "poorly", "unwell", "stomach bug",
                "tummy bug", "sick bug", "food poisoning", "a cold", "my cold", "got a cold",
                "have a cold", "flu", "a temperature", "sore throat", "nauseous", "nausea",
                "throwing up", "vomiting", "hangover", "recovering from", "getting over",
                "no appetite", "lost my appetite", "off my food",
                "cross contamination", "cross-contamination", "contamination",
                "ill from food", "sick from food")

SICK_EAT_WORDS = ("eat", "eating", "food", "drink", "drinking", "appetite", "meal", "meals",
                  "dinner", "tea", "lunch", "breakfast", "snack", "keep down", "stomach",
                  "contamination", "contaminated", "cross contamination")


PREVENTION_ASK = re.compile(
    r"\b(?:avoid|avoiding|prevent|preventing|not\s+get|don'?t\s+get|dont\s+get|never\s+get|"
    r"stop\s+(?:me\s+)?getting|protect\s+(?:myself|yourself|against))\b"
    r"|\b(?:without|so\s+(?:i|we|they|he|she)\s+don'?t|so\s+(?:i|we|they|he|she)\s+dont)\s+"
    r"(?:\w+\s+){0,3}?(?:poison\w*|getting\s+ill|get\s+ill|becoming\s+ill|going\s+off)\b")


AWAY_FROM_HOME = frozenset("""
abroad holiday holidays travelling traveling trip trips camping mexico india egypt thailand
turkey morocco peru kenya bali spain france greece italy portugal america usa canada australia
airport plane flight hotel resort street beach restaurant takeaway abroad
""".split())

_SICK_FROM_FOOD = re.compile(r"\b(?:ill|sick)\s+(?:from|off)\s+food\b")

FOOD_SAFETY_RULES = (
    "Four things do most of the work: wash your hands before you cook and after you touch raw "
    "meat; keep raw meat and fish away from anything you eat raw - its own board, the bottom "
    "shelf of the fridge; cook meat right through and reheat leftovers until they are piping "
    "hot; and get anything that should be cold into the fridge within two hours, rice within "
    "the hour. The fridge wants to be 5C or below, and a use-by date only holds while the pack "
    "has stayed cold.")


def _eat_when_ill(memory, understood):
    text = ((understood or {}).get("clean") or "").lower()
    if PREVENTION_ASK.search(text) or "contamination" in text or _SICK_FROM_FOOD.search(text):
        if ingredients(understood) or set(_plain_words(text)) & AWAY_FROM_HOME:
            return None
        return FOOD_SAFETY_RULES
    return ("Keep it plain and small: toast, crackers, rice, a banana, clear soup or plain "
            "yoghurt, and sip more than you feel like - little and often beats one big glass. "
            "Go back to proper meals over a day or two, and get advice the same day if you "
            "cannot keep any drink down or you are passing much less urine than usual.")

PROBLEM_PHRASES = ("from frozen", "still frozen", "when frozen", "cook it frozen", "is it frozen",
                   "still ok", "ok to eat", "okay to eat", "gone off", "left out", "off the "
                   "counter", "is it ok", "is it safe")

EMPTY_PHRASES = ("no food", "nothing to eat", "nothing in the fridge", "nothing in the cupboard",
                 "nothing in the cupboards", "nothing in the kitchen", "bare cupboard",
                 "cupboard is bare", "cupboards are bare", "empty fridge")

EMPTY_ASK_PHRASES = ("nothing in", "nothing left in the", "nothing at all in",
                     "nothing in the house")

MEAL_WORDS = frozenset("dinner tea supper lunch eat eating cook cooking food meal meals "
                       "bite takeaway order".split())

PET_WORDS = frozenset("dog dogs cat cats puppy kitten hamster rabbit pet pets bird".split())

EMPTY_KITCHEN = ("An empty kitchen still makes supper: pasta with a tin of tomatoes and garlic, "
                 "eggs on toast, or rice with a tin of beans and chilli. The shop that fixes it is "
                 "short and cheap: eggs, pasta, rice, tinned tomatoes, a tin of chickpeas or beans, "
                 "onions, frozen peas, cheese, bread and milk. Those cover twenty dinners between "
                 "them, and the frozen and tinned things keep for months.")

_INGREDIENT_WORDS = {}
def _fold(word):
    word = str(word).lower().replace("\u2019", "'").strip(".,!?;:'\"")
    if len(word) > 4 and word.endswith("ies"):
        return word[:-3] + "y"
    if len(word) > 4 and word.endswith("oes"):
        return word[:-2]
    if len(word) > 3 and word.endswith("es") and word[-3] in "sxzh":
        return word[:-2]
    if len(word) > 2 and word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    return word


def _fold_meal_ideas():
    vague = {_fold(word) for word in VAGUE}
    for name in list(PANTRY):
        aliases, idea = PANTRY[name]
        kept = tuple(alias for alias in aliases if _fold(alias) not in vague)
        if kept and kept != tuple(aliases):
            PANTRY[name] = (kept, idea)
    claimed = {}
    for name, (aliases, _idea) in PANTRY.items():
        claimed.setdefault(name, name)
        for alias in aliases:
            claimed.setdefault(_fold(alias), name)
    for names, idea in MEAL_IDEAS:
        group = tuple(name for name in names if _fold(name) in vague)
        solid = tuple(name for name in names if _fold(name) not in vague)
        if group and all(_fold(name) in claimed for name in solid):
            PANTRY.setdefault(_fold(group[0]), (group, idea))
            for name in names:
                claimed.setdefault(_fold(name), _fold(group[0]))
            continue
        key = None
        for name in names:
            if _fold(name) in vague:
                continue
            key = claimed.get(_fold(name))
            break
        if key is None:
            key = _fold(names[0])
            alone = tuple(name for name in names
                          if _fold(name) not in claimed or name == names[0])
            PANTRY[key] = (alone, idea)
        else:
            aliases, short = PANTRY[key]
            extra = tuple(name for name in names
                          if _fold(name) not in claimed and _fold(name) not in vague)
            PANTRY[key] = (tuple(aliases) + extra, short)
        for name in names:
            claimed.setdefault(_fold(name), key)


_fold_meal_ideas()

for _name, (_aliases, _idea) in PANTRY.items():
    for _alias in _aliases:
        _INGREDIENT_WORDS[_fold(_alias)] = _name


_ALIASES_BY_LENGTH = sorted(((tuple(_fold(_alias).split()), _name)
                             for _name, (_aliases, _idea) in PANTRY.items()
                             for _alias in _aliases),
                            key=lambda pair: -len(pair[0]))

_ALIAS_TEXT = {tuple(_fold(_alias).split()): _alias
               for _name, (_aliases, _idea) in PANTRY.items()
               for _alias in _aliases}


FORMS = (
    ("frozen", ("frozen", "freezer")),
    ("tinned", ("tinned", "canned", "tin of", "can of")),
    ("dried", ("dried", "dry")),
    ("jarred", ("jarred", "jar of")),
    ("fresh", ("fresh",)),
)

OUT_ASKS = ("havent got", "havent", "dont have", "didnt have", "ran out", "run out", "out of",
            "no fresh")
OUT_OF_FRESH = ("Out of fresh {food}, tinned or frozen is the stand-in: tinned is the better one "
                "in a sauce, drained and given 10 minutes to lose the tinny edge, and frozen goes "
                "in straight from the bag for a soup or a stew. Only a salad really wants it fresh.")
OUT_OF_FORM = {
    "fresh": OUT_OF_FRESH,
    "tinned": ("Nothing tinned, so the same food in another form stands in: frozen goes in "
               "straight from the bag with 3 or 4 minutes extra, fresh wants adding later than the "
               "tin would and a taste for salt at the end, and dried beans or chickpeas want "
               "soaking overnight and 40 minutes in the pan. For tomatoes, passata, a carton of "
               "chopped ones or a spoon of puree does the tin's job."),
    "frozen": ("Nothing in the freezer, so fresh does the same job: it cooks faster and brings "
               "less liquid, so add it later than the recipe says and taste for salt at the end. "
               "Tinned works in anything simmered, and dried wants soaking first."),
    "dried": ("No dried {food}, so tinned is the stand-in: it is already cooked, so it goes in for "
              "the last 10 minutes rather than at the start, and a tin is roughly what 100g of "
              "dried would have given. Frozen needs no soaking either."),
    "jarred": ("No jar of {food}, so the fresh or frozen version does the job: a jar is drained "
               "and rinsed only because it is salty, so taste at the end and add a little more "
               "salt than you would have. Frozen goes in straight from the bag."),
}


FORM_ADVICE = {
    "frozen": ("Frozen {food}, yes: in a sauce, soup or curry it goes in frozen with 3 or 4 "
               "minutes extra, and anything wet wants thawing and squeezing first or the pan goes "
               "wet. Picked and frozen within hours, it cooks as good as fresh."),
    "tinned": ("Tinned {food}, yes: drain off the liquid, then taste before adding salt, because a "
               "tin is already seasoned, and give beans or chickpeas 10 minutes in a sauce to lose "
               "the tinny edge. Tinned tomatoes blended smooth are passata, and a tin is thinner "
               "than puree, so simmer it down by half to thicken."),
    "dried": ("Dried {food}, yes in anything cooked, at about half the weight of fresh, soaked or "
              "simmered first if it is a pulse or a mushroom and added early so there is time to "
              "soften. Fresh is for the end, where the green taste is the point."),
    "jarred": ("A jar of {food}, yes: drain or rinse before it goes in, and taste at the end, "
               "because a jar is saltier than the same thing cooked from scratch."),
    "fresh": ("Fresh {food} instead of frozen or tinned, yes, but fresh cooks faster and brings "
              "less liquid: add it later than the recipe says and check the salt at the end, "
              "because the tinned and frozen versions carry their own."),
}

FROZEN_MEAT = ("Frozen {food}, yes, but it has to be thawed right through first: overnight in the "
               "fridge on a plate on the bottom shelf, never on the worktop, then cooked as normal. "
               "Straight from the freezer it needs longer and slower, so the middle is done before "
               "the outside dries out. Fish thaws in a few hours and cooks in minutes.")
FROZEN_FRUIT = ("Frozen fruit is picked ripe and frozen within hours, so out of season it beats "
                "the fresh punnets: use it from frozen in a crumble, a smoothie or on porridge, "
                "or half thawed in yoghurt. It goes soft as it thaws, so it will not hold its "
                "shape in a tart; roast it from frozen with a spoon of sugar if you want it whole.")
FRUIT_WORDS = frozenset("""fruit fruits berry berries raspberry raspberries strawberry
    strawberries blueberry blueberries blackberry blackberries cherry cherries plum plums peach
    peaches mango mangoes pineapple banana bananas apple apples rhubarb currant currants
    gooseberry gooseberries""".split())


def _form_word(words, start, span):
    for word in words[start:start + span]:
        for form, names in FORMS:
            if word in names:
                return form
    for word in words[max(0, start - 2):start]:
        for form, names in FORMS:
            if word in names:
                return form
    return ""


def _form_swap(memory, understood, text=None):
    words = understood.get("words")
    if not isinstance(words, (list, tuple)):
        words = str(understood.get("clean") or "").split()
    folded = [_fold(word) for word in words]
    if text:
        folded += [_fold(word) for word in str(text).lower().split()]
    said = " ".join(folded)
    if not any(ask in said for ask in _SWAP_ASK):
        return None
    used = [False] * len(folded)
    first = None
    seen = []
    head = ""
    for parts, name in _ALIASES_BY_LENGTH:
        span = len(parts)
        for start in range(len(folded) - span + 1):
            if any(used[start:start + span]):
                continue
            if all(folded[start + offset] == parts[offset] for offset in range(span)):
                for offset in range(span):
                    used[start + offset] = True
                seen.append(name)
                form = _form_word(folded, start, span)
                if form and first is None:
                    first = (start, span, form, _ALIAS_TEXT.get(parts, " ".join(parts)), name)
                    head = next(names for one, names in FORMS if one == form)
                break
    if first is None:
        for index, word in enumerate(folded):
            if word in FRUIT_WORDS and _form_word(folded, index, 1) == "frozen":
                return FROZEN_FRUIT
        return None
    start, span, form, spoken, food = first
    if food not in FORM_FOODS:
        return None
    if any(other != food for other in seen):
        return None
    first_word = spoken.split()[0].lower() if spoken.split() else ""
    if first_word and any(first_word == form_word for form_word in head):
        spoken = " ".join(spoken.split()[1:]) or spoken
    if any(ask in " ".join(folded[:start + span]) for ask in OUT_ASKS):
        return OUT_OF_FORM[form].format(food=spoken)
    if form == "frozen":
        if food in MEAT:
            return FROZEN_MEAT.format(food=spoken)
        if food in FRUIT_WORDS:
            return FROZEN_FRUIT
    return FORM_ADVICE[form].format(food=spoken)


FORM_FOODS = ("spinach", "mushroom", "tomato", "pea", "sweetcorn", "bean", "chickpea", "lentil",
              "fish", "salmon", "prawn", "chicken", "mince", "turkey", "bacon", "potato",
              "onion", "carrot", "broccoli", "kale", "cabbage", "cauliflower", "courgette",
              "aubergine", "squash", "pepper", "leek", "apple", "banana", "lemon", "berry",
              "peach", "mango", "fruit", "herb", "herbs", "garlic", "chilli", "ginger",
              "blackberry", "raspberry", "strawberry", "blueberry", "cod", "haddock", "tuna",
              "sardine", "anchovy", "coconut", "date", "fig", "plum", "cherry", "gooseberry",
              "rhubarb", "gooseberries")

_FORM_FOOD_WORDS = tuple(sorted({word
                                 for name in FORM_FOODS
                                 for alias in PANTRY.get(name, ((), ""))[0]
                                 for word in _fold(alias).split()}
                                | set(FORM_FOODS)))

FORM_SWAP_WORDS = ("instead", "swap", "swapping", "substitute", "replace", "out of",
                   "ran out", "run out", "havent got", "havent any", "dont have", "didnt have",
                   "no fresh")
ENTRIES.append(entry("form-swap", (tuple(word for _form, names in FORMS for word in names
                                        if word != "canned"),
                                  FORM_SWAP_WORDS),
                     _form_swap, ask=_SWAP_ASK,
                     avoid=("keep", "keeps", "keeping", "store", "storing", "last", "lasts",
                            "gone off", "going off", "mouldy")))


NEGATIONS = frozenset("""
without no not except minus avoiding avoid hate hates hateful allergic dislike dont don't
never leave skip skipped out off
stand wont won't refuse refuses sick
havent haven't hasnt hasn't hadnt hadn't didnt didn't
""".split())

RULING_OUT_PHRASES = ("not a fan of", "not a fan", "not keen on", "not fussed about",
                      "cant stand", "can t stand", "cannot stand", "sick of", "tired of",
                      "bored of", "fed up of", "fed up with", "had enough of", "gone off",
                      "allergic to", "instead of", "hate", "hates", "dislike", "dislikes",
                      "loathe", "not into")
REFUSAL_REACH = 6
CLAUSE_BREAK = frozenset("but though although however except apart besides instead also".split())


def _refused_before(folded, place):
    if place <= 0:
        return False
    window = []
    for word in reversed(folded[max(0, place - REFUSAL_REACH):place]):
        if word in CLAUSE_BREAK:
            break
        window.insert(0, word)
    plain = " " + " ".join(window) + " "
    return any((" " + cue + " ") in plain for cue in RULING_OUT_PHRASES)

FOOD_CLASSES = {
    "bacon": ("meat",), "chicken": ("meat",), "ham": ("meat",), "mince": ("meat",),
    "sausage": ("meat",), "prawn": ("shellfish", "fish"), "salmon": ("fish",),
    "tuna": ("fish",), "egg": ("egg",), "butter": ("dairy",), "cheese": ("dairy",),
    "cream": ("dairy",), "milk": ("dairy",), "yoghurt": ("dairy",),
    "bread": ("gluten",), "pasta": ("gluten",), "flour": ("gluten",),
    "tortilla": ("gluten",),
}

DIETS = (
    (("vegan", "plant based", "plantbased", "no animal"),
     ("meat", "fish", "shellfish", "dairy", "egg")),
    (("vegetarian", "veggie", "vego", "no meat"), ("meat", "fish", "shellfish")),
    (("pescetarian", "pescatarian"), ("meat",)),
    (("dairy free", "dairyfree", "lactose", "no dairy", "milk free"), ("dairy",)),
    (("gluten free", "glutenfree", "coeliac", "celiac", "no gluten", "wheat free"),
     ("gluten",)),
)

FILLER = frozenset("""
a an the and or plus too also some a bit little half of with without im i am m we us my our
have has got get only just thats that it is are so oh hey hi and its ive weve some more
i'm im you're we're theyre
nah nope yeah yep yeh eh well ok okay hmm hm um umm er erm literally honestly actually
""".split())

_DIET_WORDS = frozenset(word for _cues, _ruled in DIETS for _cue in _cues for word in _cue.split())

NEGATION_REACH = 3
COOKED_REACH = 3

SOFTENED = frozenset("much many sure enough lots lot bit little some just only".split())

EVENT_HEADS = frozenset("""christmas easter thanksgiving halloween birthday wedding anniversary
christening funeral wake valentine valentines chocolate""".split())


def _renamed_by_an_event(folded, place):
    if place == 0:
        return False
    return folded[place - 1] in EVENT_HEADS


_READ_FOR_INGREDIENTS = {}
_READ_FOR_INGREDIENTS_KEEP = 4000


def _named_ingredients(understood):
    if not isinstance(understood, dict):
        return [], []
    words = understood.get("words")
    if not isinstance(words, (list, tuple)):
        words = str(understood.get("clean") or "").split()
    folded = [_fold(word) for word in words]
    repaired = [_fold(word) for word in str(understood.get("plain") or "").split()]
    if len(repaired) == len(folded) and repaired != folded:
        folded = repaired
    told = _READ_FOR_INGREDIENTS.get(tuple(folded))
    if told is None:
        told = _work_out_ingredients(folded)
        if len(_READ_FOR_INGREDIENTS) >= _READ_FOR_INGREDIENTS_KEEP:
            _READ_FOR_INGREDIENTS.clear()
        _READ_FOR_INGREDIENTS[tuple(folded)] = told
    return list(told[0]), list(told[1])


def _work_out_ingredients(folded):
    used = [False] * len(folded)
    present = set(folded)
    hits = []
    for parts, name in _ALIASES_BY_LENGTH:
        if parts[0] not in present:
            continue
        span = len(parts)
        for start in range(len(folded) - span + 1):
            if any(used[start:start + span]):
                continue
            if all(folded[start + offset] == parts[offset] for offset in range(span)):
                for offset in range(span):
                    used[start + offset] = True
                hits.append((start, name, span))
                break
    named, negated = [], []
    refused_ends = []
    for place, name, span in sorted(hits):
        if name in named:
            continue
        if _renamed_by_an_event(folded, place):
            continue
        named.append(name)
        before = folded[max(0, place - NEGATION_REACH):place]
        ruled = _refused_before(folded, place) or (
                any(word in NEGATIONS for word in before)
                and not any(word in SOFTENED for word in before))
        if not ruled and _on_a_list_already_ruled_out(folded, place, refused_ends):
            ruled = True
        if ruled:
            negated.append(name)
            refused_ends.append(place + span)
    return named, negated


REFUSAL_JOINERS = frozenset("or and nor either plus also both".split())


def _on_a_list_already_ruled_out(folded, place, refused_ends):
    for end in refused_ends:
        between = folded[end:place]
        if between and all(word in REFUSAL_JOINERS for word in between):
            return True
    return False


def diet_exclusions(understood):
    if not isinstance(understood, dict):
        return []
    clean = str(understood.get("clean") or "").lower()
    words = understood.get("words") if isinstance(understood.get("words"), (list, tuple)) else None
    folded = [_fold(word) for word in (words or clean.split())]
    classes = set()
    for cues, ruled in DIETS:
        for cue in cues:
            if " " in cue:
                if cue in clean:
                    classes.update(ruled)
                    break
            elif cue in folded:
                classes.update(ruled)
                break
    if not classes:
        return []
    return [name for name, kinds in FOOD_CLASSES.items() if classes.intersection(kinds)]


WITHOUT = {
    "rice": "Fry the cold rice hard with frozen veg and soy sauce, or cook it in stock with a "
            "handful of chopped herbs.",
    "pasta": "Toss the pasta with olive oil, sliced garlic and a little chilli, and keep back a splash "
             "of the cooking water to loosen it.",
    "potato": "Cut the potatoes into wedges, toss with oil and salt, and roast at 200C (180C fan) for 35 "
              "minutes.",
    "potato_wedges": "",
    "bread": "Toast the bread and rub a cut garlic clove over it, then spoon over chopped tomatoes with "
             "olive oil.",
    "spinach": "Wilt the spinach in a hot pan with a little oil, garlic and a grate of nutmeg, 2 minutes.",
    "cabbage": "Shred the cabbage and fry it hard in oil with a pinch of salt until the edges char, 5 "
               "minutes.",
    "chickpea": "Roast a drained tin of chickpeas at 200C (180C fan) for 25 minutes with oil, salt and paprika.",
    "bean": "Fry a drained tin of beans with garlic, cumin and a tin of tomatoes, and simmer 15 minutes.",
    "lentil": "Simmer the lentils with a tin of tomatoes, cumin and stock for 20 minutes.",
    "tomato": "Halve the tomatoes and roast at 200C (180C fan) for 25 minutes with oil, salt and thyme.",
    "mushroom": "Fry the mushrooms hard in oil until they squeak and brown, then finish with garlic and "
                "parsley.",
    "courgette": "Slice the courgette thick, oil and salt it, and grill 4 minutes a side.",
    "pepper": "Roast the pepper halves at 200C (180C fan) for 25 minutes, then peel and dress with oil.",
    "carrot": "Roast the carrot batons at 200C (180C fan) for 30 minutes with oil, salt and cumin.",
    "onion": "Slice the onions thick and cook slowly in oil for 20 minutes until sweet and brown.",
    "banana": "Slice the banana over porridge, or mash it into a batter and fry small pancakes.",
    "apple": "Stew the apple in slices with a splash of water and cinnamon for 8 minutes.",
    "sweetcorn": "Fry a drained tin of sweetcorn in a hot pan with oil, chilli and lime, 5 minutes.",
    "pea": "Simmer the peas 3 minutes and crush them with oil, salt and mint.",
    "garlic": "Warm sliced garlic slowly in oil and spoon it over anything plain.",
    "lemon": "Squeeze the lemon over greens with oil and salt, or steep the zest in hot water for tea.",
    "oats": "Simmer the oats with water or a dairy-free drink for 5 minutes and top with fruit.",
    "egg": "Boil the eggs 7 minutes, cool them, and eat with salt and toast.",
    "milk": "Warm the milk with a spoon of honey and a pinch of cinnamon.",
    "cheese": "Grate the cheese over hot pasta or potatoes with plenty of black pepper.",
    "yoghurt": "Stir the yoghurt into soup off the heat, or spoon it over fruit.",
    "butter": "Melt the butter into hot potatoes or pasta with salt and pepper.",
    "cream": "Stir the cream into a pan of mushrooms off the heat with salt and pepper.",
    "flour": "Mix the flour with water and a pinch of salt into a batter for pancakes.",
}
WITHOUT.pop("potato_wedges")


def _is_food_list(folded, clean):
    named = False
    for word in folded:
        if not word or word in FILLER or word in _DIET_WORDS or word in NEGATIONS:
            continue
        if word in _INGREDIENT_WORDS:
            if _INGREDIENT_WORDS[word] not in _VAGUE_KEYS:
                named = True
            continue
        return False
    return named


def ingredients(understood):
    named, negated = _named_ingredients(understood)
    kept = [name for name in named if name not in negated]
    kept = [name for name in kept
            if not any(name != other and name in other.split() for other in kept)]
    clean = str((understood or {}).get("clean") or "").lower()
    return [name for name in kept
            if not any(phrase in clean for phrase in NOT_THIS_FOOD.get(name, ()))]


def negated_ingredients(understood):
    named, negated = _named_ingredients(understood)
    return [name for name in negated if name in named]


def _mentions(text, names):
    if not names:
        return False
    words = [_fold(word) for word in str(text or "").lower().split()]
    for word in words:
        name = _INGREDIENT_WORDS.get(word)
        if name is None:
            for ending in ("", "s", "es"):
                name = _INGREDIENT_WORDS.get(_fold(word.rstrip(",.")) + ending)
                if name is not None:
                    break
        if name in names:
            return True
    return False


def cooked_ingredients(understood):
    words = understood.get("words") if isinstance(understood, dict) else None
    if not isinstance(words, (list, tuple)):
        words = str((understood or {}).get("clean") or "").split()
    folded = [_fold(word) for word in words]
    ready = []
    for place, word in enumerate(folded):
        name = _INGREDIENT_WORDS.get(word)
        if not name or name in ready:
            continue
        if not any(word in COOKED_WORDS
                   for word in _words_just_before(folded, place, COOKED_REACH)):
            continue
        before = folded[max(0, place - NEGATION_REACH):place]
        if any(word in NEGATIONS for word in before):
            continue
        ready.append(name)
    return ready


MEAT_SWAPS = {"chicken": "chickpeas or tofu", "turkey": "chickpeas or lentils",
              "mince": "lentils or chickpeas", "sausage": "chickpeas or halloumi",
              "bacon": "mushrooms and smoked paprika", "ham": "mushrooms",
              "pork": "mushrooms or chickpeas", "lamb": "chickpeas or lentils",
              "beef": "lentils or mushrooms", "steak": "mushrooms or aubergine",
              "chorizo": "smoked paprika and mushrooms",
              "tuna": "chickpeas", "salmon": "chickpeas or tofu", "prawn": "chickpeas",
              "fish": "chickpeas or tofu"}

_VEG_WORDS = frozenset("vegetarian vegetarians veggie veggies vegan vegans".split())

_VEG_PHRASES = ("no meat", "meat free", "meat-free", "without meat", "dont eat meat",
                "don't eat meat", "doesnt eat meat", "does not eat meat", "eat no meat")

_VEG_GUESTS = re.compile(r"\b(?:one|two|three|four|five|six|seven|eight|nine|ten|some|half|a few"
                         r"|\d+)\b[^.]{0,40}\bveg(?:gie|gies|an|ans|etarian|etarians)\b")

_VEG_DINNER = ("A red lentil dhal is the dinner I would cook: lentils, an onion, garlic, cumin "
               "and a tin of tomatoes simmered 20 minutes, with rice or bread. Or chickpeas and "
               "spinach: fry onion, garlic and spices, add a tin of chickpeas and a tin of "
               "tomatoes, simmer 15 minutes and stir spinach through at the end.")
_VEG_DINNER_CHEAP = " Both cost about 50p a head."

_VEG_ELSEWHERE = re.compile(r"\b(?:my|his|her|their|our)\b[^.]{0,30}"
                            r"\b(?:is|are|was|doesn'?t|does not|don'?t|do not|won'?t|will not)\b"
                            r"[^.]{0,30}\bveg")

_SELF_VEG = re.compile(r"\b(?:i'?m|im|i am|we'?re|we are|as a)\b[^.]{0,30}"
                       r"\bveg(?:gie|gies|an|ans|etarian|etarians)\b")


def _plain_words(text):
    return re.findall(r"[a-z']+", str(text).lower())


def _veg_dinner(missing, cheap=False):
    if _mentions(_VEG_DINNER, missing):
        return _any_meal(set(missing))
    return _VEG_DINNER + (_VEG_DINNER_CHEAP if cheap else "")


def _diet(folded, clean):
    if _VEG_ELSEWHERE.search(clean) and not _SELF_VEG.search(clean):
        return ""
    if any(word in ("vegan", "vegans") for word in folded):
        return "vegan"
    if (any(word in _VEG_WORDS for word in folded)
            or any(phrase in clean for phrase in _VEG_PHRASES)
            or _VEG_GUESTS.search(clean)):
        return "vegetarian"
    return ""


def _recent_user_turns(memory, count=4):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return []
    return [str(turn.get("user") or "") for turn in turns[-count:]
            if isinstance(turn, dict)]


def _diet_from_turns(earlier):
    for said in reversed(earlier):
        found = _diet(re.findall(r"[a-z0-9']+", said.lower()), said.lower())
        if found:
            return found
    return ""


_BARE_NO_CUES = frozenset(("no", "none", "without", "not", "nothing"))

SHORTAGE_AFTER = frozenset(("left", "house", "home", "cupboard", "fridge", "freezer", "gone",
                            "shop", "shops", "supermarket", "kitchen", "larder", "pantry"))


def _refused_foods(text, families=False):
    said = _fold(str(text or ""))
    said = re.sub(r"\b(?:tired|sick|bored)\s+of\b|\bfed\s+up\s+(?:of|with)\b", " no ", said)
    refused = set()
    words = re.findall(r"[a-z']+", said)
    for start, word in enumerate(words):
        if word not in _REFUSAL_CUES:
            continue
        index = start + 1
        while index < len(words):
            here = words[index]
            name = _INGREDIENT_WORDS.get(here) or _INGREDIENT_WORDS.get(_fold(here))
            if name:
                after = words[index + 1:index + 3]
                if word in _BARE_NO_CUES and any(part in SHORTAGE_AFTER for part in after):
                    break
                refused.add(name)
                index += 1
                continue
            if here in FAMILIES:
                if families:
                    refused.update(DAIRY if here == "lactose" else FAMILIES[here])
                index += 1
                continue
            if here in _REFUSAL_FILLER or here in _REFUSAL_JOINERS:
                index += 1
                continue
            break
    return refused


def refused_foods(understood):
    if not isinstance(understood, dict):
        return frozenset()
    said = str(understood.get("clean") or understood.get("text") or "")
    return frozenset(_refused_foods(said))


DINNER_ASK_WORDS = frozenset("""
make makes making cook cooking meal meals dinner tea lunch supper snack idea ideas recipe recipes
something anything
""".split())


NOT_A_DINNER_LIMIT = frozenset(("flour",))

AND_NO = ("with no", "with none", "with not much", "with only")

DINNER_NAMED = frozenset("""
dinner dinners tea supper lunch meal meals main cook cooking cooked roast fry fried bake baked
""".split())

SHORTAGE_WORDS = ("ran out", "run out", "out of", "none left", "nothing left", "havent got",
                  "haven't got", "dont have", "don't have", "have no", "has no", "not got",
                  "no more", "all gone",
                  "in the house", "in the cupboard", "in the fridge", "in the freezer")


LUNCH_AND_BREAKFAST = frozenset("lunch lunches breakfast brunch lunchbox lunchboxes".split())


_STAND_IN_ASK = ("instead", "instead of", "substitute", "substitutes", "sub for", "sub for it",
                 "swap", "swaps", "replace", "replacement", "in place of", "stand in for",
                 "what else can i use", "what else could i use", "what do i use instead")
_STAND_IN_USE = re.compile(
    r"what (?:can|could|do|should) i use(?!\s+(?:it|them|that|this|those|these|leftovers?"
    r"|the rest)\b)")


def asks_for_a_stand_in(understood):
    said = _clean(understood) if not isinstance(understood, dict) else _clean(understood)
    if any(phrase in said for phrase in _STAND_IN_ASK):
        return True
    return bool(_STAND_IN_USE.search(said))


def a_dinner_without(understood, memory=None):
    said = _clean(understood)
    if asks_for_a_stand_in(understood):
        return None
    if not _refused_foods(said):
        return None
    if not isinstance(memory, dict):
        memory = {}
    if any(phrase in said for phrase in SHORTAGE_WORDS):
        return None
    if _refused_foods(said) <= NOT_A_DINNER_LIMIT:
        return None
    words = set(_said_words(understood))
    if any(phrase in said for phrase in AND_NO) and not words & DINNER_NAMED:
        return None
    asking = any(phrase in said for phrase in MEAL_ASK_PHRASES)
    if not asking:
        asked = understood.get("asks") if isinstance(understood, dict) else None
        asking = bool(asked) and bool(words & DINNER_ASK_WORDS)
    if not asking:
        return None
    if any(word in said.split() for word in LUNCH_AND_BREAKFAST):
        return None
    cooked = dish(understood, memory) or meal(understood, memory=memory)
    if not (isinstance(cooked, str) and cooked.strip()):
        return None
    return None if unusable(cooked, understood) else cooked


_REFUSAL_CUES = frozenset((
    "no", "not", "without", "never", "hate", "hates", "hated", "dislike", "dislikes",
    "refuse", "refuses", "refused", "wont", "won't", "doesnt", "doesn't", "dont", "don't",
    "cant", "can't", "cannot", "avoid", "avoids", "avoids", "off",
    "fussy", "banned", "allergic", "intolerant", "skip", "skipping"))

_REFUSAL_JOINERS = frozenset(("or", "and", "nor", "plus", "also"))

_REFUSAL_FILLER = frozenset((
    "eat", "eats", "eating", "have", "has", "having", "use", "uses", "want", "wants",
    "like", "likes", "liked", "love", "loves", "loved", "care", "cares", "keen",
    "the", "any", "more", "much", "really", "at", "all", "a", "an", "this", "that",
    "these", "those", "it", "them", "some", "my", "his", "her", "their", "our", "of",
    "food", "foods", "stuff", "things", "thing", "dish", "dishes", "kind", "sort",
    "me", "us", "him", "her", "to", "for", "with", "is", "are", "was", "were"))


def _dishes_without(banned):
    banned = {str(name) for name in banned}
    found = []
    for dish in DISHES:
        uses = tuple(dish.get("uses") or ())
        if not uses or any(name in banned for name in uses):
            continue
        if _mentions(dish.get("text") or "", banned):
            continue
        found.append(dish)
    return found


def _best_dish(found, ready=(), missing=(), avoid=(), diet=""):
    best, best_uses = None, 1
    trimmed = None
    for candidate in DISHES:
        uses = candidate["uses"]
        if diet and any(name in MEAT for name in uses):
            continue
        if not all(name in found for name in uses):
            continue
        if candidate.get("text") in avoid:
            continue
        if missing and _mentions(candidate["text"], missing):
            if any(name in uses for name in missing):
                continue
            cut = _without_the_trimmings(candidate["text"], missing)
            if cut and trimmed is None and len(uses) > 1:
                trimmed = dict(candidate, text=cut,
                               without=tuple(sorted(name for name in missing
                                                    if _mentions(candidate["text"], (name,)))))
            continue
        if avoid and all(word in _fold(" ".join(avoid)) for word in candidate["id"].split("-")):
            continue
        if any(name in missing for name in uses):
            continue
        keeps = candidate.get("cooked", ())
        if any(name in ready and name not in keeps for name in uses):
            continue
        if len(uses) > best_uses:
            best, best_uses = candidate, len(uses)
    return best or trimmed


SENTENCE = re.compile(r"(?<=[.!?])\s+")


def _served_without(dish):
    left_out = " and ".join(dish.get("without") or ())
    text = str(dish.get("text") or "")
    name, colon, method = text.partition(": ")
    if colon and name and not _mentions(name, dish.get("without") or ()):
        return f"{name}, no {left_out}: {method}"
    return f"Without the {left_out}: " + (text[:1].lower() + text[1:] if text else text)


def _without_the_trimmings(text, missing):
    parts = [part.strip() for part in SENTENCE.split(str(text or "").strip()) if part.strip()]
    while len(parts) > 1 and _mentions(parts[-1], missing):
        parts.pop()
    if not parts or _mentions(parts[0], missing):
        return ""
    return " ".join(parts)




def dish(understood, avoid=(), memory=None):
    if _names_a_bake(understood):
        return None
    return meal(understood, dishes_only=True, avoid=avoid, memory=memory)


ENTRIES.append(entry(
    "eat-when-ill", (SICK_PHRASES, SICK_EAT_WORDS), _eat_when_ill, bias=1,
    avoid=("blood", "chest pain", "cant breathe", "can't breathe", "short of breath",
           "pregnant", "weeks", "baby", "babies", "toddler", "my son", "my daughter",
           "my mum", "my dad", "my husband", "my wife", "my partner", "child", "children",
           "diarrhoea", "diarrhea", "three days", "four days", "a week", "doctor",
           "hospital", "medicine", "antibiotic", "tests", "why do i", "why am i",
           "cold rice", "cold chicken", "cold pizza", "left out", "gone off", "ok to eat",
           "safe to eat", "still ok", "is it ok",
           "help a cold", "help my cold", "help the cold", "help a cough", "help my cough",
           "help a sore throat", "help my throat", "does honey", "will honey", "honey help",
           "honey and lemon", "lemon and honey", "honey in warm water",
           "my cat", "my dog", "my puppy", "my kitten", "my rabbit", "my hamster",
           "my guinea pig", "my parrot", "my budgie", "my tortoise", "my pet", "my puppy",
           "cat", "dog", "puppy", "kitten", "rabbit", "hamster", "guinea pig", "parrot",
           "budgie", "tortoise", "the cat", "the dog", "the puppy", "the kitten",
           ) + TOOTH_OR_GUM))

_WHAT_IS_IT = re.compile(
    r"\b(?:is|are)\s+(?:a|an)?\s*[a-z]+\s+(?:a|an)?\s*"
    r"(?:fruit|vegetable|berry|berries|tuber|root|grain|pulse)s?\s*(?:\?|$|or\b|,|\.)")

def _reads_as_news(understood, clean=""):
    from . import meals

    return meals.reads_as_news(understood, clean)

_CHOICE_WORDS = ("should i", "shall i", "do i use", "can i use", "could i use", "which",
                 "better", "instead", "rather", "or is", "or would", "or should", "or do i",
                 "what about", "worth using", "go for", "stick to")

_COOKING_MEDIUM = ("oil|olive oil|water|stock|wine|milk|cream|margarine|ghee|lard|dripping|"
                   "suet|vinegar|lemon|honey|syrup|sugar|salt|pepper|flour|cornflour|"
                   "butter|yoghurt|juice|sauce|gravy|rub|marinade|foil|paper|trays?|tins?")

_ANY_FOOD_TEXT = None


def _any_food_text():
    global _ANY_FOOD_TEXT
    if _ANY_FOOD_TEXT is None:
        names = sorted({_fold(str(alias)) for aliases, _idea in PANTRY.values()
                        for alias in aliases}, key=len, reverse=True)
        _ANY_FOOD_TEXT = "|".join(re.escape(name) for name in names if name)
    return _ANY_FOOD_TEXT


def _a_choice_of_foods(clean):
    low = _fold(str(clean or ""))
    if " or " not in low:
        return False
    if not any(word in low for word in _CHOICE_WORDS):
        return False
    foods = _any_food_text()
    if not foods:
        return False
    other = foods + "|" + _COOKING_MEDIUM
    return bool(re.search(r"\b(?:%s)\s+or\s+(?:%s)\b" % (foods, other), low))


def meal(understood, dishes_only=False, text=None, banned=None, diet=None, memory=None,
         avoid=(), pointed_back=False):
    if _names_a_bake(understood):
        return None
    if not isinstance(understood, dict):
        return None
    if _says_it_has_gone_off(understood.get("clean")):
        return None
    if names_a_dish(understood):
        _said = str(understood.get("clean") or "").lower()
        if not any(word in _said for word in _USE_UP_WORDS):
            return None
    from . import picking
    if picking.choosing(understood):
        return None
    shared = " ".join([str(understood.get("clean") or "")]
                      + [str(word) for word in (understood.get("words") or ())])
    if _feeding_ask(shared):
        return None
    if _pet_not_dinner(shared) or _reads_as_a_pet(shared):
        return _pet_or_meat(shared)
    if _a_brew_not_a_dinner(shared):
        return None
    if _a_plant_not_a_dinner(shared):
        return None
    if understood.get("kind") in ("empty", "greeting", "thanks"):
        return None
    words = understood.get("words") or ()
    folded = [_fold(word) for word in words]
    earlier = _recent_user_turns(memory)
    clean_now = str(understood.get("clean") or "").lower()
    whole = " ".join([clean_now] + [str(said).lower() for said in earlier])
    crowd = _crowd_ask(clean_now)
    if (not crowd and earlier
            and any(word in clean_now for word in _CROWD_FOOD + _CROWD_VERBS)):
        crowd = _crowd_ask(whole)
    if banned is None:
        banned = frozenset(_excluded(" ".join(
            [str(understood.get("clean") or ""), " ".join(str(word) for word in words)]
            + earlier)))
    refused = _refused_foods(" ".join([str(understood.get("clean") or "")] + earlier))
    if refused - set(banned):
        banned = frozenset(banned | refused)
    if text is not None:
        lower = str(text).lower()
        typed = str(understood.get("text") or "").lower()
        repaired = str(understood.get("plain") or "").lower()
        if repaired and repaired != typed and lower == typed:
            lower = repaired
        own = [_fold(word) for word in lower.split()]
        if (not any(word in _INGREDIENT_WORDS for word in own)
                and not any(phrase in lower for phrase in EMPTY_PHRASES)
                and not any(phrase in lower for phrase in EMPTY_ASK_PHRASES)
                and not any(phrase in lower for phrase in LEFT_POINTER + USE_UP_ASKS)
                and not crowd):
            return None
    asks = set(understood.get("asks") or ())
    if (asks & NOT_MEAL_ASKS and not _crowd_ask(understood.get("clean") or "")
            and not (asks & NOT_MEAL_ASKS == {"how"}
                     and any(phrase in str(understood.get("clean") or "").lower()
                             for phrase in USE_UP_ASKS))):
        return None
    if any(word in PROBLEM_WORDS for word in folded):
        return None
    if any(word in SUBSTITUTE_WORDS for word in folded):
        return None
    clean = str(understood.get("clean") or "").lower()
    if _WHAT_IS_IT.search(clean):
        return None
    if _VEG_GUESTS.search(clean):
        banned = frozenset(banned | MEAT)
    if any(phrase in clean for phrase in SUBSTITUTE_PHRASES):
        return None
    if any(phrase in clean for phrase in PROBLEM_PHRASES):
        return None
    if any(phrase in clean for phrase in RESTRICTED_EATING):
        if not (any(word in MEAL_CUES for word in folded) and _refused_foods(clean)):
            return None
    if any(phrase in clean for phrase in ILLNESS_PHRASES):
        return None
    if any(phrase in clean for phrase in ACTIVITY_PHRASES):
        return None
    if any(phrase in clean for phrase in MAKING_IT_YOURSELF_PHRASES):
        return None
    empty_kitchen = any(phrase in clean for phrase in EMPTY_PHRASES)
    if not empty_kitchen and any(phrase in clean for phrase in EMPTY_ASK_PHRASES):
        empty_kitchen = any(word in MEAL_WORDS for word in folded)
    if empty_kitchen and not any(word in PET_WORDS for word in folded):
        return EMPTY_KITCHEN
    asked = (any(word in MEAL_CUES for word in folded)
             or any(phrase in clean for phrase in MEAL_PHRASES)
             or crowd)
    bought = any(phrase in clean for phrase in BOUGHT_PHRASES)
    asked = asked or bought
    asks_what_to_cook = (any(word in MEAL_CUES for word in folded)
                         or any(phrase in clean for phrase in MEAL_ASK_PHRASES))
    named = ingredients(understood)
    if (understood.get("topic") not in ("cooking", "food-and-drink")
            and not any(word in FOOD_CUES for word in folded)
            and not (named and (asks_what_to_cook or bought))
            and not crowd
            and not _is_food_list(folded, clean)):
        return None
    if not (asked or _is_food_list(folded, clean)):
        return None
    found = [name for name in named if name not in _VAGUE_KEYS
             and name not in VAGUE] or named
    missing = list(negated_ingredients(understood))
    said_no = list(missing)
    for name in diet_exclusions(understood):
        if name in found:
            found = [other for other in found if other != name]
        if name not in missing:
            missing.append(name)
    if banned:
        refused_here = [name for name in found
                        if name in banned or any(part in banned for part in name.split())]
        missing.extend(refused_here)
        found = [name for name in found if name not in refused_here]
    diet = diet or _diet(folded, clean) or _diet_from_turns(earlier)
    if not found:
        if any(phrase in clean for phrase in EMPTY_ASK_PHRASES):
            return EMPTY_KITCHEN
        if crowd:
            return _crowd_meal(banned, _occasion(whole), _crowd(whole))
        if earlier and any(phrase in clean for phrase in LEFT_POINTER):
            for said in reversed(earlier):
                for name in ingredients({"words": str(said).lower().split(),
                                         "clean": str(said).lower()}):
                    if name in LEFTOVER_IDEAS:
                        return LEFTOVER_IDEAS[name]
        if diet:
            whole = " ".join([clean] + [said.lower() for said in earlier])
            if _crowd(whole) >= 6 or _occasion(whole):
                return _crowd_meal(banned, _occasion(whole), _crowd(whole))
            return _veg_dinner(set(banned) | set(missing),
                              any(word in CHEAP_PLAN_WORDS for word in _plain_words(whole)))
        if _refused_foods(clean) and banned:
            for dish in _dishes_without(banned):
                if dish.get("text") and dish["text"] not in avoid:
                    return dish["text"]
        if said_no and any(word in MEAL_WORDS for word in folded) \
                and not _reads_as_news(understood, clean):
            return _any_meal(set(banned) | set(said_no))
        return None
    no_meat = bool(diet) or bool(MEAT & set(banned))
    leftover = _leftover(folded, clean)
    if (len(found) == 1
            and not pointed_back
            and not bought
            and not _is_food_list(folded, clean)
            and not any(phrase in clean for phrase in MEAL_PHRASES)
            and not leftover
            and not (no_meat and any(name in MEAT for name in found))):
        return None
    swap = ""
    if no_meat:
        left = [name for name in found if name in MEAT]
        if left:
            meat = left[0]
            instead = MEAT_SWAPS.get(meat, "chickpeas")
            swap = f"{instead[0].upper() + instead[1:]} do the same job in most dishes. "
            picked = []
            for word in re.findall(r"[a-z]+", instead):
                name = _INGREDIENT_WORDS.get(_fold(word))
                if name and name not in banned:
                    picked.append(name)
                    break
            found = (picked or ["chickpea"]) + [name for name in found if name not in MEAT]
    best = _best_dish(found, cooked_ingredients(understood), missing, avoid, diet)
    if best is not None:
        if best.get("without"):
            return swap + _served_without(best)
        return swap + best["text"]
    if dishes_only:
        return None
    from . import meals
    if (any(word in LEFTOVER_WORDS for word in folded)
            or any(phrase in clean for phrase in LEFTOVER_PHRASES)):
        for name in found:
            row = PANTRY.get(name)
            idea = row[1] if row else ""
            if not idea or _mentions(idea, missing) or idea in avoid:
                continue
            if meals.idea_is_a_dish(idea):
                continue
            said_name = name
            for word in re.findall(r"[a-z]+", clean):
                if _fold(word) == _fold(name) or _fold(word) == name:
                    said_name = word
                    break
            use = meals.use_it_up(said_name)
            if use:
                return use
    if not swap and (any(word in LEFTOVER_WORDS for word in folded)
                     or any(phrase in clean for phrase in LEFTOVER_PHRASES)):
        for name in found:
            if name in LEFTOVER_IDEAS and LEFTOVER_IDEAS[name] not in avoid \
                    and not _mentions(LEFTOVER_IDEAS[name], missing):
                if name == "milk" and _mentions(clean, PLANT_MILKS):
                    continue
                return LEFTOVER_IDEAS[name]
    if _a_choice_of_foods(clean):
        return None
    ideas = [PANTRY[name][1] for name in found[:2]
             if not _mentions(PANTRY[name][1], missing) and PANTRY[name][1] not in avoid]
    if not ideas:
        ideas = [WITHOUT[name] for name in found[:2]
                 if name in WITHOUT and not _mentions(WITHOUT[name], missing)
                 and WITHOUT[name] not in avoid]
    said = " ".join(ideas) if ideas else None
    if said is not None and said in avoid:
        return None
    return said


def _meal_texts():
    texts = [dish["text"] for dish in DISHES if dish.get("text")]
    for name in PANTRY:
        texts.extend([PANTRY[name][1], LEFTOVER_IDEAS.get(name, ""), WITHOUT.get(name, "")])
    texts.extend([EMPTY_KITCHEN, *EMPTY_ASK_PHRASES])
    return frozenset(text.strip() for text in texts if text)


_MEAL_TEXTS = _meal_texts()
_MEAL_METHODS = tuple(text.partition(": ")[2] for text in _MEAL_TEXTS if ": " in text)


def _is_meal_answer(said):
    said = str(said or "").strip()
    if not said:
        return False
    if said in _MEAL_TEXTS:
        return True
    method = said.partition(": ")[2]
    return len(method) > 40 and any(m.startswith(method) for m in _MEAL_METHODS)


_NUMBER_WORD = (r"\d+|an?|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|fifteen|"
                r"twenty|thirty|forty|fifty|sixty|ninety")
_TIMING = re.compile(
    r"\b(?:%s)(?:\s*(?:to|or|-|and a half)\s*(?:%s))?\s*(?:minutes?|mins?|hours?|hrs?)\b"
    % (_NUMBER_WORD, _NUMBER_WORD), re.I)

_BACK_REFERENCE = frozenset("""
that it this those these there them one dish recipe meal dinner supper thing
""".split())
_WORD = re.compile(r"[a-z']+")

_KEEP_WORDS = frozenset("""
keep keeps keeping kept store stores stored storing fridge freezer freeze frozen last lasts
lasting leftover leftovers
""".split())
_KEEP_TIME = re.compile(
    r"%s|\b(?:\d+|a|an|one|two|three|four|five|six|seven|eight|nine|ten)\s*"
    r"(?:days?|weeks?|months?|years?)\b" % _TIMING.pattern, re.I)

_KEEP_TIME_ASK = re.compile(r"\bhow (?:long|many (?:days?|weeks?|hours?|months?))\b", re.I)

_COOKING_SENSE = frozenset("""
oven pan hob grill microwave boil boiling simmer fry frying stir stirring whisk whisking
roast roasting bake baking cook cooking heat
""".split())

COOKED_KEEPING = ("Once it is cooked, cool it within two hours and keep it covered in the fridge: "
                  "it keeps 3 to 4 days, and you can reheat it once, piping hot all the way "
                  "through. Anything with rice or chicken should go in the fridge straight away "
                  "rather than sit out.")


_SPEAKS_OF_KEEPING = re.compile(
    r"\b(?:keeps?|keeping|lasts?|lasting|stays? good)\b[^.]{0,60}\b(?:days?|weeks?|months?|years?"
    r"|hours?)\b"
    r"|\b(?:in|into|out of|from) the fridge\b|\bfreez(?:e|es|er|ing)\b"
    r"|\b(?:days?|weeks?)\b[^.]{0,40}\bin the fridge\b", re.I)


def speaks_of_keeping(reply):
    return bool(isinstance(reply, str) and _SPEAKS_OF_KEEPING.search(reply))


def keeping_ask(understood):
    if not isinstance(understood, dict):
        return False
    clean = str(understood.get("clean") or "").lower()
    words = set(_WORD.findall(clean))
    if not words & _KEEP_WORDS or words & (_COOKING_SENSE - {"roast", "roasting"}):
        return False
    return bool(_KEEP_TIME_ASK.search(clean))


_TOTAL_TIME = re.compile(
    r"start to finish|from start to finish|in total|altogether|all in\b|in all\b|end to end",
    re.I)

_RECIPE_STEP = re.compile(
    r"\b(?:fry|fries|frying|fried|add|adds|adding|simmer|simmering|bake|baking|roast|"
    r"roasting|boil|boiling|stir|stirring|grill|griddle|wilt|wilted|toss|mash|whisk|"
    r"blend|braise|poach|steam|season|drain|serve)\b", re.I)


def _the_answer_names_a_food(said):
    return bool({_fold(word) for word in _WORD.findall(str(said or "").lower())} & _foods_said())


def keeping_followup(understood, memory):
    if not isinstance(understood, dict) or not isinstance(memory, dict):
        return None
    clean = str(understood.get("clean") or "").lower()
    words = set(_WORD.findall(clean))
    if not words & _KEEP_WORDS or words & _COOKING_SENSE:
        return None
    if not _KEEP_TIME_ASK.search(clean):
        return None
    if not words & _BACK_REFERENCE:
        return None
    for turn in ((memory.get("turns") or [])[-3:] if isinstance(memory.get("turns"), list) else []):
        said = str(turn.get("user") or "").lower() if isinstance(turn, dict) else ""
        if any(name in said for name in _BAKED_GOODS):
            return None
    turns = memory.get("turns")
    if not isinstance(turns, list) or not turns or not isinstance(turns[-1], dict):
        return None
    if turns[-1].get("module") != "answers":
        return None
    said = str(turns[-1].get("bot") or "")
    if set(_WORD.findall(said.lower())) & _KEEP_WORDS:
        return None
    if not _TIMING.search(said) and not _RECIPE_STEP.search(said):
        return None
    if not _the_answer_names_a_food(said):
        return None
    return COOKED_KEEPING


def timing_followup(understood, memory):
    if not isinstance(understood, dict) or not isinstance(memory, dict):
        return None
    asks = set(understood.get("asks") or ())
    words = set(understood.get("words") or ())
    clean = str(understood.get("clean") or "").lower()
    if not (asks & {"how_long"} or "how long" in clean or "how many minutes" in clean):
        return None
    if not words & _BACK_REFERENCE:
        if {_fold(word) for word in words} & set(_INGREDIENT_WORDS):
            return None
        if {_fold(word) for word in words} & _KEEP_WORDS:
            return None
    turns = memory.get("turns")
    if not isinstance(turns, list) or not turns or not isinstance(turns[-1], dict):
        return None
    last = turns[-1]
    said = str(last.get("bot") or "").strip()
    if last.get("module") != "answers":
        kept = memory.get("last_answer")
        kept_text = str((kept or {}).get("reply") or "").strip() if isinstance(kept, dict) else ""
        head = kept_text[:40].lower()
        if not kept_text or len(kept_text) < 40 or head not in said.lower():
            return None
        said = kept_text
    if not _is_meal_answer(said):
        return None
    sentences = [part for part in re.split(r"(?<=[.!?])\s+", said) if part.strip()]
    total = [part for part in sentences if _TOTAL_TIME.search(part)]
    when = None
    for part in total + [part for part in sentences if part not in total]:
        times = {" ".join(found.group(0).lower().split())
                 for found in _TIMING.finditer(part)}
        if len(times) == 1:
            when = times.pop()
            break
    if when is None:
        return None
    said_words = set(_fold(word) for word in _WORD.findall(said.lower()))
    named = [word for word in understood.get("words") or ()
             if _fold(word) in _INGREDIENT_WORDS and _fold(word) not in said_words]
    if named:
        return None
    return "About %s for that one, start to finish." % when



_RECIPE_ASK = ("make", "making", "made", "cook", "cooking", "recipe", "recipes", "how", "what goes",
               "ingredients", "from scratch", "method", "proper", "best way", "how long", "simmer",
               "bake", "time", "worth", "should i",
               "fancy", "craving", "crave", "mood", "want", "wanting",
               "feel like", "feels like", "feeling like", "felt like",
               "whats a good", "what's a good", "whats the best", "what's the best",
               "what is a good", "what is the best",
               "filling ideas", "fillings", "fillings for")

_RECIPE_ASK_WORDS = re.compile(
    r"(?<![a-z])(?:" + "|".join(re.escape(one) for one in
                                sorted(_RECIPE_ASK, key=len, reverse=True)) + r")(?![a-z])")

_DISH_ON_ITS_OWN_FILLER = frozenset((
    "a", "an", "the", "some", "my", "our", "me", "please", "pls", "plz", "ta", "thanks",
    "thank", "you", "hi", "hello", "hey", "ok", "okay", "oh", "ah", "so", "well", "just",
    "quick", "easy", "simple", "nice", "good", "proper", "some", "and", "then", "for",
    "tonight", "today", "now", "it", "that", "one", "again", "recipe", "recipes"))


def _this_line_only(understood):
    words = understood.get("words")
    if isinstance(words, list) and words:
        return " ".join(str(word).lower() for word in words)
    return str(understood.get("clean") or "").lower()


def _names_nothing_but_the_dish(text, names):
    left = " " + " ".join(str(text or "").lower().split()) + " "
    named = False
    for name in sorted(names, key=len, reverse=True):
        needle = " " + str(name).lower() + " "
        if needle in left:
            left = left.replace(needle, " ")
            named = True
    return named and all(word in _DISH_ON_ITS_OWN_FILLER for word in left.split())


_WANT_PHRASES = re.compile(r"\b(?:fancy|fancied|craving|crave|in the mood for|really want|"
                           r"i want|would love|i'd love|i would love|feel like|feels like|"
                           r"feeling like)\b")

_WANT_ACTION = re.compile(r"\b(?:want|wants|wanting|fancy|fancied|craving|crave|love|loves|"
                          r"feel|feels|feeling)\s+(?:like\s+)?"
                          r"(?:to|it|that|this|you|me|him|her|them|us|if|when|how|why|what)\b")


_WANT_TO_COOK = re.compile(r"\b(?:want|wants|wanting|fancy|fancied|would love|i'd love|"
                           r"i would love)\s+to\s+(?:make|cook|bake|roast|do|try)\b")


_WANT_TO_LEARN_COOK = re.compile(
    r"\b(?:want|wants|wanting|fancy|fancied|would love|i'd love|i would love|would like|"
    r"i'd like|thinking of|planning to|going to|gonna|hope to|hoping to)\b[^.!?]{0,24}?"
    r"\b(?:learn|learning|learnt|learned|start|starting|started|try|trying)\s+"
    r"(?:to\s+|how\s+to\s+)?(?:make|cook|bake|roast)\b")


def _wants_the_dish(text):
    if _WANT_TO_COOK.search(text) or _WANT_TO_LEARN_COOK.search(text):
        return True
    return bool(_WANT_PHRASES.search(text)) and not _WANT_ACTION.search(text)

_RECIPE_NOT_THIS = re.compile(
    r"\b(?:without(?!\s+(?:(?:any\s+)?yeast|(?:a|an|the|my)\s+"
    r"(?!(?:an?\s+)?(?:oven|grill|hob|stove|range|microwave|air ?fryer|cooker|barbecue|bbq)\b)))"
    r"|dairy[- ]free|gluten[- ]free|egg[- ]free|nut[- ]free|sugar[- ]free|vegan|"
    r"vegetarian|substitute|substitutes|substitution|instead of|swap|swapped|swapping|"
    r"replace|replacing|alternative|reheat|reheated|reheating|leftover|leftovers|store|storing|"
    r"stored|storage|freeze|freezes|freezing|air fryer|slow cooker|pressure cooker|microwave|"
    r"keep|keeps|keeping|kept|last|lasts|lasting|go off|goes off|gone off|safe to eat|edible|"
    r"still good|still ok|still okay|"
    r"how much|how many|"
    r"thicken|thickening|thickens|runny|watery|lumpy|curdled|curdles|split|splits|"
    r"too salty|too spicy|too sweet|bland|burnt|burning)\b")


_RECIPE_ANSWERS = ("question", "request", "statement")


def _recipe_only_when_asked_for_this(reply, names=(), no_yeast_ok=False):
    total = re.split(r"(?<=[.!?])\s+", reply.strip())[0]

    def answer(memory, understood):
        text = _said_so_far(understood, memory)
        alone = _names_nothing_but_the_dish(_this_line_only(understood), names)
        if not alone and not _RECIPE_ASK_WORDS.search(text):
            return None
        if _WANT_ACTION.search(text) and not _WANT_TO_COOK.search(text) \
                and not _WANT_TO_LEARN_COOK.search(text):
            return None
        if understood.get("intent") not in _RECIPE_ANSWERS and not _wants_the_dish(text) \
                and not alone:
            return None
        if not no_yeast_ok and any(one in text for one in _NO_YEAST):
            return None
        if _RECIPE_NOT_THIS.search(text):
            return None
        line = str(understood.get("clean") or "").lower()
        if _RECIPE_KEEPING.search(line) and not _RECIPE_COOKING.search(line):
            return None
        if understood.get("asks") == ["how_long"]:
            return total
        return reply
    return answer


_RECIPE_KEEPING = re.compile(
    r"\b(?:keep|keeps|keeping|shelf[ -]life|last|lasts|lasted|store|stores|storing|storage|"
    r"go off|goes off|gone off|past its date|past the date|out of date|next day|tomorrow|"
    r"once opened|once open|mouldy|mould|moldy|mold|use by)\b")
_RECIPE_COOKING = re.compile(
    r"\b(?:cook|cooks|cooking|cooked|boil|boils|boiling|bake|bakes|baking|roast|roasting|"
    r"fry|frying|grill|grilling|steam|steaming|make|makes|making|recipe|prepare|prep|"
    r"assemble|heat|oven|simmer|reheat)\b")


_RECIPE_GROWING_WORDS = (
    "sow", "sows", "sowing", "sowed", "germinate", "germinating", "seedling", "seedlings",
    "allotment", "veg patch", "vegetable patch", "raised bed", "raised beds",
    "harvest", "harvesting", "crop", "crops", "plant out", "planting out", "thin out",
    "thin the seedlings")

ANNOUNCED_DISH = (
    "im making", "i'm making", "im doing", "i'm doing", "im cooking", "i'm cooking",
    "im gonna make", "i'm gonna make", "im going to make", "i'm going to make",
    "im gonna do", "i'm gonna do", "im going to do", "i'm going to do",
    "i am making", "i am doing", "i am cooking", "i am gonna make", "i am going to make",
    "i am gonna do", "i am going to do")

_A_POT_ALREADY_MADE = re.compile(
    r"\b(?:made|cooked|done|ate|had)\b[^.?!]{0,24}\b(?:yesterday|last night|this morning|"
    r"the night before|the day before|days? ago|\d+ days?)\b"
    r"|\b(?:left ?overs?|left over)\b"
    r"|\b(?:in|been in) the (?:fridge|freezer|pot|tub)\b"
    r"|\bmade (?:on|for) (?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b", re.I)


def _a_made_pot_is_not_its_recipe(understood):
    if not isinstance(understood, dict):
        return True
    text = understood.get("norm_text") or understood.get("clean") or ""
    return not _A_POT_ALREADY_MADE.search(str(text))


_RECIPE_FAULT_WORDS = (
    "thicker", "thicken", "thickens", "thickening",
    "thinner", "too thick", "too thin", "watery", "runny", "stodgy", "lumpy",
    "curdled", "curdles", "split", "splits", "too salty", "too spicy", "too sweet",
    "bland", "burnt", "burning")

for _names, _key, _reply, _avoid in RECIPES:
    def _alone(line, _only=tuple(_names)):
        return _names_nothing_but_the_dish(line, _only)

    ENTRIES.append(entry("recipe-" + _key[0].replace(" ", "-"),
                         (_names, _RECIPE_ASK),
                         _recipe_only_when_asked_for_this(
                             _reply, _names, no_yeast_ok=_key[0] == "soda bread"),
                         ask=tuple(_RECIPE_ASK) + tuple(_names),
                         shape=(_alone,),
                         bias=(2 if _key[0] in ("rice and peas", "soda bread")
                               else 1 if _key[0] == "sandwich" else 0),
                         avoid=tuple(_avoid) + _RECIPE_FAULT_WORDS + _RECIPE_GROWING_WORDS
                         + _NO_SUGAR + ANNOUNCED_DISH,
                         guard=_a_made_pot_is_not_its_recipe))
_USE_UP_WORDS = ("leftover", "leftovers", "left over", "left from", "use up", "using up",
                 "used up", "spare", "stale", "already made", "goes off", "go off",
                 "out of date")
_PANTRY_FOODS = frozenset(
    [_fold(alias) for aliases, _reply in PANTRY.values() for alias in aliases]
    + [_fold(name) for name in PANTRY])


def names_a_dish(understood):
    if not isinstance(understood, dict):
        return None
    words = understood.get("words")
    if not isinstance(words, (list, tuple)):
        words = str(understood.get("clean") or "").split()
    folded = [_fold(word) for word in words if str(word).strip()]
    for aliases, _keys, _body, _avoid in RECIPES:
        for alias in aliases:
            parts = [_fold(part) for part in alias.split()]
            if not parts or " ".join(parts) in _PANTRY_FOODS:
                continue
            if len(parts) == 1:
                hit = parts[0] in folded
            else:
                hit = any(folded[at:at + len(parts)] == parts
                          for at in range(len(folded) - len(parts) + 1))
            if hit:
                return alias
    return None


ENTRIES.append(entry(
    "blind-bake",
    (("pastry", "flan", "pastry case", "pastry base", "pie base", "tart base",
      "pie case", "tart case", "flan case", "blind bake", "blind baking",
      "quiche", "quiches"),
     ("blind", "blind bake", "blind baking", "bake", "baking", "line", "lined", "weights",
      "baking beans", "dry rice", "empty case", "before the filling",
      "how long", "how many minutes")),
    ("Line the tin with the pastry, prick the base all over with a fork, then cover it with a "
     "sheet of crumpled parchment and fill that with baking beans or dry rice. Bake at 200C "
     "(180C fan) for 15 minutes, lift the paper and beans out, and give it another 5 minutes to "
     "dry the base before the filling goes in. Blind just means baked empty - the weights stop "
     "the base rising and the sides slumping."),
    bias=1,
    avoid=("shrank", "shrink", "shrunk", "soggy", "sunk", "sank", "raw", "burnt", "burned",
           "cracked", "cracking", "crumbly", "falls apart", "how do i make pastry",
           "pastry recipe", "shortcrust", "rough puff", "puff pastry", "choux", "filo",
           "filling", "freeze", "frozen", "keep", "leftover",
           "make a quiche", "cook a quiche", "quiche recipe", "quiche recipe")))

ENTRIES.append(entry(
    "season-pan",
    (("pan", "pans", "wok", "skillet"),
     ("season", "seasoning", "seasoned", "reseason", "re-season", "cure", "curing",
      "sticking", "sticks", "ruined", "unusable", "lost its coating")),
    ("A pan that sticks has usually lost its thin layer of baked-on oil: scrub it, dry it on the "
     "hob, rub a film of neutral oil over the inside and heat it until it just smokes, then wipe "
     "the surplus off with kitchen paper. Twice more and it is slippery again. That works on "
     "stainless steel, carbon steel and cast iron. A non-stick pan is the exception - once the "
     "coating is scratched through, nothing brings it back, so replace it."),
    ask=("how", "what", "should", "do i", "can", "when", "why", "my"),
    avoid=("cast iron", "cast-iron", "carbon steel", "rust", "rusty", "rusts", "dishwasher",
           "chicken", "steak", "salmon", "fish", "meat", "veg", "vegetables", "potatoes",
           "rice", "pasta", "soup", "stew", "curry", "to taste", "salt and pepper",
           "smoking", "smoke", "fire", "alarm", "burnt", "burning")))


POINT_BACK = ("with them", "with it", "with those", "with these", "with that",
              "make with them", "make with it", "make with those", "make with these",
              "do with them", "do with it", "do with those", "do with that",
              "use it up", "use them up", "use those up", "use these up", "use that up",
              "use up the rest", "using it up", "using them up", "using those up",
              "using these up", "using that up", "using up the rest",
              "out of them", "out of it", "what about them",
              "what about it", "else can i do with", "else can i make with",
              "else could i do with", "else to do with", "else can i use",
              "any ideas", "any idea", "any other ideas", "any suggestions", "suggestions",
              "what else", "anything else", "something else", "what do you suggest")
POINT_BACK_BARE = frozenset(("any ideas", "any idea", "any other ideas", "any suggestions",
                             "suggestions", "what else", "anything else", "something else",
                             "what do you suggest"))
THE_FOOD_OR_THE_MEAL = frozenset(("it them those these this rest leftover leftovers left other "
                                 "using use dinner tea supper lunch breakfast meal meals "
                                 "pudding dessert snack").split())
POINT_BACK_OBJECT = re.compile(r"\b(?:for|about|on)\s+(.+)$", re.I)


def _ideas_are_for_something_else(said):
    named = POINT_BACK_OBJECT.search(said)
    if named is None:
        return False
    return not (set(re.findall(r"[a-z']+", named.group(1).lower())) & THE_FOOD_OR_THE_MEAL)
PAIRING_WORDS = ("goes with", "go with", "to go with", "serve with", "served with",
                 "serve on the side", "on the side", "side dish", "side dishes",
                 "what can i serve", "what should i serve", "what to serve",
                 "pair with", "pair it with", "pairing", "accompany")

SECOND_IDEA = ("what else", "anything else", "something else", "another idea",
               "another one", "any other", "other ideas", "what other")


POINT_BACK_STOP = ("going off", "gone off", "went off", "off the", "use by", "best before",
                   "out of date", "still ok", "ok to eat", "okay to eat", "safe to eat",
                   "mouldy", "moldy", "mould", "mold", "smells", "smelly", "slimy",
                   "defrost", "raw", "undercooked", "allergic", "food poisoning", "vomit",
                   "diarrhoea", "threw up", "sick after", "my cat", "my dog", "the cat",
                   "the dog")


def recent_replies(memory, count=2):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return ()
    said = [str(turn.get("bot") or "") for turn in turns[-count:] if isinstance(turn, dict)]
    return tuple(said[-count:])


def _words_of(text):
    return re.findall(r"[a-z0-9']+", str(text or "").lower())


def _food_before(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return []
    for turn in reversed(turns[-3:]):
        if not isinstance(turn, dict):
            continue
        said = str(turn.get("user") or "")
        if any(phrase in said.lower() for phrase in POINT_BACK_STOP):
            return []
        words = _words_of(said)
        if ingredients({"words": words}):
            return words
    return []


def pointed(memory, understood):
    if not isinstance(understood, dict):
        return None
    if ingredients(understood):
        return None
    clean = str(understood.get("clean") or "").lower()
    if not any(phrase in clean for phrase in POINT_BACK):
        return None
    if (not any(phrase in clean for phrase in POINT_BACK if phrase not in POINT_BACK_BARE)
            and _ideas_are_for_something_else(clean)):
        return None
    if any(phrase in clean for phrase in PAIRING_WORDS):
        return None
    earlier = _food_before(memory)
    if not earlier:
        return None
    reading = dict(understood)
    reading["words"] = earlier + _words_of(" ".join(understood.get("words") or ()))
    reading["clean"] = " ".join(earlier) + " " + clean
    if any(phrase in clean for phrase in SECOND_IDEA):
        reading["new_dish_only"] = True
    return reading
_PLANNED_FOOD = ("chicken", "beef", "pork", "lamb", "mince", "fish", "salmon", "pasta", "rice",
                 "curry", "chilli", "soup", "stew", "bread", "cake", "potato", "potatoes",
                 "courgette", "spinach", "chickpeas", "lentils", "eggs", "cheese", "milk")

ENTRIES.append(entry(
    "meal-prep",
    (("meal prep", "meal-prep", "meals prepped", "prep meals", "prep for the week",
      "prep on sunday", "batch cook", "batch cooking", "batch-cook", "cook ahead",
      "cook once eat twice", "cook once and eat twice"),
     ("how", "what", "should", "can", "start", "begin", "tip", "tips", "help", "want",
      "worth", "week", "weekly", "sunday", "idea", "ideas", "best", "way")),
    ("Cook two big things on one day and portion them: a pot of chilli or bolognese and a tray of "
     "roast veg, then cook rice or pasta fresh on the day. Cool it within two hours, box it in the "
     "portions you will actually eat, and keep three days in the fridge or freeze the rest. Chop "
     "an onion, wash a bag of salad and grate some cheese while you are there and a weekday dinner "
     "takes ten minutes. Cooked rice is the one to freeze on the day, not the next."),
    avoid=("safe", "food safety", "how long", "defrost", "gone off")))

ENTRIES.append(entry(
    "plan-the-week",
    (("shopping list", "food shop", "weekly shop", "the week's shop", "weeks shop",
      "meals for the week", "dinners for the week", "week of dinners", "week of meals",
      "weeknight dinners", "what to cook this week", "cook this week", "food for the week"),
     ("how", "what", "should", "help", "start", "make", "write", "do", "tip", "tips", "idea",
      "ideas", "best", "way")),
    ("Write down five dinners, not seven: three you can cook without thinking, one new one and one "
     "night for leftovers or something from the freezer. Then shop once from that list, plus "
     "breakfast and lunch things, and buy the fresh veg you will use in the first three days. A "
     "plan you can move a night around is the one that survives; a strict seven-day plan usually "
     "gets abandoned by Wednesday."),
    avoid=("diet", "lose weight", "calories", "calorie", "baby", "toddler", "school lunch",
           "meal plan", "meal planning", "weekly meal plan", "airport", "flight",
           "supermarket", "supermarkets", "cheapest", "cheaper", "which shop", "price",
           "prices", "aldi", "lidl", "tesco", "asda", "sainsburys", "sainsbury's", "morrisons",
           "waitrose", "ocado", "iceland", "co-op", "co op"),
    bias=1))

ENTRIES.append(entry(
    "food-waste",
    (("stop wasting food", "wasting food", "waste food", "food waste", "throw away food",
      "throwing food away", "food going off", "use up food", "reduce waste",
      "waste so much food", "wasting so much food", "waste food every week",
      "so much food goes off", "food goes off before", "throw so much food away",
      "throwing so much food away", "food in the bin", "ends up in the bin"),
     ("how", "what", "should", "can", "stop", "reduce", "avoid", "tips", "tip", "help",
      "way", "ways", "best", "less", "not", "waste", "wasting", "wasted", "throw", "throwing",
      "away", "week", "month", "much")),
    ("Look in the fridge before you go to the shop: see what is left, then plan the next two "
     "dinners around it. Keep the oldest veg at the front of the drawer, freeze bread, milk and "
     "any meat you will not use in two days on the day you buy it, and treat the freezer as a "
     "pause button rather than a cupboard. A weekly \"whatever is left\" soup or frittata uses up "
     "the odds and ends, and a written list stops you buying a third bag of carrots."),
    avoid=("bin", "council", "collection", "compost", "recycling", "smell", "smells")))

SCALE_DOWN = (
    "Halve every ingredient and leave the oven temperature alone: the tin goes one size down if "
    "the batter looks thin in it, and start checking five minutes early. Cooking time does not "
    "halve - a smaller cake or loaf takes about two thirds as long - so test it with a skewer "
    "sooner than you think. Halve the raising agent exactly, and if the sum gives you half an "
    "egg, beat one and use half of it.")
SCALE_UP = (
    "Double every ingredient and use a bigger tin rather than a deeper one, so the middle cooks "
    "at the same speed. It takes longer than twice the time is worth assuming: start checking at "
    "the original time and give it another ten or fifteen minutes if the skewer comes out wet. "
    "Salt, spice and raising agent go up by less than double, to taste, and a big batch is better "
    "split between two tins than crammed into one.")
SCALE_UP_WORDS = ("double", "doubling", "doubled", "times two", "scale up", "for 20",
                  "for twenty", "for 30", "for a crowd", "for a big group", "bigger batch")


def _scaling_reply(memory, reading):
    line = str((reading or {}).get("text") or (reading or {}).get("norm") or "").lower()
    words = set(re.findall(r"[a-z']+", line))
    if any(word in words or ((" " in word) and word in line) for word in SCALE_UP_WORDS):
        return SCALE_UP
    if "scale" in words and "up" in words:
        return SCALE_UP
    return SCALE_DOWN


ENTRIES.append(entry(
    "halve-a-recipe",
    (("halve", "halving", "halved", "half the recipe", "cut the recipe in half",
      "cut a recipe in half", "cut this recipe in half", "make half", "half a batch",
      "double", "doubling", "doubled", "double the recipe", "double up", "scale", "scaling",
      "scale down", "scale up", "times two", "times three", "third of the recipe",
      "scale a recipe", "scale up a recipe", "scale down a recipe", "scale the recipe",
      "double a recipe", "halve a recipe", "double the recipe", "halve the recipe",
      "two thirds of the recipe"),
     ("recipe", "recipes", "batch", "ingredients", "quantities", "amounts", "portions",
      "portion", "loaf", "cake", "mixture", "sauce", "soup", "stew", "casserole",
      "bolognese", "traybake", "biscuits", "cookies", "curry", "chilli", "pie", "roast",
      "for two", "for four", "for six", "for eight", "for twelve", "for 20", "for 20 people",
      "for twenty", "for 30", "for a crowd", "for a big group",
      "cooking time", "baking time", "bake time", "oven time")),
    _scaling_reply,
    bias=1,
    avoid=("marathon", "half marathon", "race", "half price", "bill", "bills", "dose",
           "dosage", "paracetamol", "ibuprofen", "tablet", "tablets", "chips", "half a chicken",
           "half a pizza", "wine", "beer", "rent", "mortgage", "salary", "wage")))
ENTRIES.append(entry(
    "cook-for-one",
    (("cook", "cooking", "cook for", "meal", "meals", "dinner", "dinners", "recipe", "recipes",
      "food", "eat", "eating"),
     ("for one", "for one person", "for myself", "on my own", "just me", "only me",
      "just for me", "single", "alone")),
    ("Cook two portions and let the second one be tomorrow's lunch or dinner: it is barely more "
     "work and it is the whole trick. Buy the smaller packs where they exist, freeze half a loaf "
     "and half a pack of mince on the day, and keep eggs, tinned tomatoes, pasta, rice and frozen "
     "veg in as the base of a ten-minute dinner. A frying pan and one small pot will do most of "
     "it."),
    bias=1,
    ask=("ideas", "worth", "bother", "should", "plan", "planning", "batch", "portions",
         "portion", "leftovers", "what can i", "what should i", "meal ideas", "meals for",
         "dinner ideas", "recipes for", "cooking for one", "cook for one", "for myself",
         "on my own", "just me", "only me", "just for me", "cook for", "cooking for",
         "eat for", "what to cook", "ideas for"),
    avoid=("lonely", "loneliness", "widow", "grief", "died", "bereave",
           "upstairs", "downstairs", "stair", "stairs", "stairwell", "landing", "loft",
           "attic", "cellar", "garage", "gutter", "gutters", "roof",
           "wardrobe", "sofa", "settee", "couch", "furniture", "mattress", "bed frame",
           "bookcase", "bookshelf", "shelving", "shelf", "shelves", "flat pack", "flat-pack",
           "flatpack", "move house", "moving house", "house move", "curtain", "curtains",
           "blind", "blinds", "carpet", "paint", "wall", "walls", "door", "doors",
           "window", "windows", "tile", "tiles", "fence", "shed", "decking", "mower",
           "lawn", "drill", "hook", "hooks", "car", "van", "bike", "bicycle",
           "washing", "laundry", "ironing", "dishes", "washing up", "hoover", "vacuum",
           "cleaning", "washing machine", "dishwasher", "boiler", "radiator", "tap",
           "toilet", "fridge", "freezer", "bin", "bins",
           "raise", "raising", "child", "children", "kid", "kids",
           "bring up", "bringing up", "single parent", "single mum", "single dad",
           "save money", "saving money", "afford", "rent", "bills", "money",
           "restaurant", "restaurants", "cafe", "pub", "eat out", "eating out", "meal out",
           "go for a meal", "going out for", "out for dinner", "out for lunch", "takeaway")))

ENTRIES.append(entry(
    "more-vegetables",
    (("eat more veg", "eat more vegetables", "more vegetables", "more veg", "get veg into",
      "vegetables in my diet", "eat veg", "five a day", "more greens",
      "blend veg", "blend vegetables", "blended veg", "blend the veg", "hide veg",
      "hide the veg", "hidden veg", "puree veg", "puree the veg", "puree vegetables",
      "sneak veg", "sneak the veg", "veg into a sauce", "vegetables into a sauce"),
     ("how", "what", "should", "shall", "can", "help", "tips", "tip", "ideas", "way", "ways",
      "best", "want", "need", "get", "eating", "hide", "blend", "sneak", "puree")),
    _more_veg,
    avoid=("child", "children", "kids", "kid", "toddler", "baby", "son", "daughter", "fussy",
           "picky", "refuses", "wont eat", "won't eat", "freeze", "freezer", "freezing",
           "frozen", "blanch", "batch cook", "batch cooking")))

ENTRIES.append(entry(
    "freeze-meals",
    (("freeze", "freezing", "frozen", "freezer"),
     ("meal", "meals", "dinner", "dinners", "supper", "batch", "ahead", "well",
      "which food", "what food")),
    ("Stews, curries, chilli, bolognese, soup, lasagne and shepherd's pie all freeze well and come "
     "back the same; cook them a bit under and freeze in portions flat in bags so they thaw fast. "
     "Leave out potatoes cooked in a stew, pasta and rice cooked in it, and add fresh pasta, rice "
     "or a jacket potato on the day. Cool within two hours, label the date, eat within three "
     "months, and defrost in the fridge overnight."),
    avoid=("breast milk", "formula", "baby food", "wedding cake", "cake")))

ENTRIES.append(entry(
    "guests-cheap",
    (("guests", "guest", "party", "crowd", "lots of people", "big meal", "whole family",
      "table full", "people coming"),
     ("cheap", "cheaply", "budget", "save money", "afford", "stretch", "inexpensive",
      "cost", "money")),
    ("One big dish that stretches beats several small ones: a chilli, a curry or a pasta bake with "
     "bread and a big salad, where the cheap starch and veg do the filling and the meat is the "
     "flavour. Chicken thighs, mince, tinned tomatoes, lentils and beans cost far less than "
     "prime cuts or fillets, and a slow-cooked shoulder of pork or lamb feeds a table for very "
     "little. "
     "Ask people to bring the pudding or the drinks and nobody minds."),
    avoid=("restaurant", "takeaway", "wedding", "caterer", "catering")))
ENTRIES.append(entry(
    "mussels-unopened",
    (("mussel", "mussels", "clams", "clam", "shellfish", "oysters", "oyster"),
     ("open", "opened", "closed", "unopened", "shut", "eat", "eating", "ok", "okay", "safe",
      "didnt", "didn't", "not", "still", "bin", "throw", "gone off", "cook", "cooking",
      "steam", "steamed", "how long")),
    "Tap each mussel before cooking and bin any that stays open, plus any with a broken shell; "
    "after cooking, bin the ones that stayed shut, because an unopened one was dead before it "
    "went in. Steam the rest in a covered pan with a splash of wine or water for four to five "
    "minutes, and eat them the same day rather than keeping them for tomorrow.",
    avoid=("paint", "shell", "seashell", "shells on the beach", "razor")))


from .cooking_more import (ENTRIES as _TAIL_ENTRIES, PLAN_KEYS, asks_a_food_fact,
                           first_plan, follow_up, minutes_said, plan_recent, remembered,
                           wants, _clean, _said_words)

ENTRIES.extend(_TAIL_ENTRIES)
