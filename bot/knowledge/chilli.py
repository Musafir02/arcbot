import re

from . import lookup
from . import lookup
from .lookup import entry, said_in_this_line

ANSWERS = ("cooking", "food-and-drink")

DISH = ("con carne", "con carni", "bolognese", "chilli beef", "stew", "recipe", "dish",
        "saucepan", "in a curry")
COOKED = (" pot ", "pot of", "a pot", "batch", "cooked", "already made", "made it")
_CHILLI_IN_THE_LINE = ("chilli", "chillies", "chile", "chiles", "jalapeno", "jalapenos",
                       "habanero", "scotch bonnet", "birds eye")


def _the_vegetables_or_the_pot(memory, understood, vegetable_answer, pot_answer):
    if _a_chilli_in_this_line(memory, understood):
        return vegetable_answer
    if isinstance(memory, dict) and _a_dish_in_the_chat(memory, understood):
        pot = pot_answer(memory, understood)
        if isinstance(pot, str) and pot.strip():
            return pot
    return vegetable_answer


def _a_dish_in_the_chat(memory, understood):
    from . import dishes
    try:
        return bool(dishes.dish_for(memory, understood))
    except Exception:
        return False


def _the_plans_keeping_answer(memory, understood):
    from . import dishes
    return dishes.follow_up(memory, understood)


def _the_cooked_dish_freezing_answer(memory, understood):
    from .cooking_entries import freeze_cooked_answer
    return freeze_cooked_answer(memory, understood)


def _a_chilli_in_this_line(memory, understood):
    text = said_in_this_line(understood, memory).lower()
    return any(word in text for word in _CHILLI_IN_THE_LINE)


HEAT_WORDS = ("simmer", "simmering", "simmered", "cook", "cooking", "boil", "boiling", "fry",
              "frying", "fried", "roast", "roasting", "roasted", "bake", "baking", "baked",
              "oven", "hob", "pan", "minutes", "stir fry", "grill", "steam")


CURRY_HEAT = (
    (("korma", "pasanda", "butter chicken", "makhani"),
     "mildest on the menu, creamy and with no chilli heat at all"),
    (("tikka masala", "tikka", "masala"),
     "mild, a tomato and cream sauce with a little warmth"),
    (("rogan josh", "dhansak", "balti"),
     "medium, warming rather than burning"),
    (("madras",),
     "the first properly hot one on most menus, hot without being punishing"),
    (("jalfrezi",),
     "hot, with green chillies and peppers left in"),
    (("vindaloo",),
     "very hot, and hotter in some kitchens than others"),
    (("phal", "naga", "tindaloo"),
     "the hottest thing on the menu, and past the point where most people taste anything else"),
)

CURRY_NAMES = {name: name for names, _ in CURRY_HEAT for name in names}

CURRY_ORDER_LINE = "korma, pasanda, butter chicken, tikka masala, rogan josh, balti, dhansak, madras, jalfrezi, vindaloo, phaal"

_HEAT_WORDS = ("spicy", "spice", "spicier", "hot", "hotter", "hottest", "mild", "milder",
               "mildest", "heat", "strength", "how strong", "scoville", "burn", "burning",
               "too spicy", "too hot", "which is mildest", "least spicy")


_A_FAULT_IN_THE_DISH = (
    "too spicy", "too hot to eat", "too hot for me", "too hot for the kids", "way too hot",
    "way too spicy", "far too spicy", "far too hot", "cool it down", "cool the heat",
    "cool this down", "make it milder", "make it less spicy", "less spicy", "not so spicy",
    "too much chilli", "too much chili", "blow your head off", "burning my mouth",
)


def _curry_heat(memory, understood):
    words = [str(word).lower() for word in (understood.get("words") or [])]
    said = " ".join(words)
    flat = " " + str(understood.get("clean") or understood.get("text") or "").lower() + " "
    flat = re.sub(r"[^a-z0-9' ]+", " ", flat)
    if any(phrase in flat for phrase in _A_FAULT_IN_THE_DISH):
        return None
    for index, (names, place) in enumerate(CURRY_HEAT):
        for name in names:
            if name in said:
                return ("A %s is %s. Mildest to hottest the usual menu runs %s, so ask for it mild "
                        "and the kitchen leaves the chilli out - and if you want heat with flavour, "
                        "step one up the list rather than two."
                        % (name, place, CURRY_ORDER_LINE))
    return ("Mildest to hottest the usual takeaway menu runs %s. A korma or pasanda has no chilli "
            "heat at all, a tikka masala is mild, and a jalfrezi and up are the hot end; ask for "
            "any of them mild and the kitchen makes it without the chilli."
            % CURRY_ORDER_LINE)


_SHORTAGE = re.compile(
    r"\b(?:but no|and no|no|without|short of|missing|havent got|haven't got|not got"
    r"|ran out of|run out of)\s+((?:[a-z']+\s*){0,3})")
_BEAN_STEMS = ("bean", "kidney", "pinto", "cannelli", "haricot", "baked", "black")


def _short_of_something_else(understood):
    for match in _SHORTAGE.finditer(lookup.said_text(understood)):
        near = match.group(1).split()[:3]
        if not any(word.startswith(_BEAN_STEMS) for word in near):
            return False
    return True


A_COOK_CLOCK_VERB = re.compile(r"\b(?:take|takes|taking|simmer|simmering|boil|boiling|fry|frying|"
                               r"bake|baking|roast|roasting|cook|cooks|cooking|poach|steam|grill)\b")
A_KEEPING_CUE = re.compile(r"\b(?:keep|keeps|keeping|kept|last|lasts|lasting|store|stored|fridge|"
                           r"freezer|freeze|frozen|good for|leftover|left over|reheat|reheats|"
                           r"out of date|use by|still good|safe to eat|night|tomorrow)\b")
A_POT_OF_CHILLI_KEEPS = (
    "A pot of chilli keeps 3 days in the fridge, in a sealed box, once it has cooled within "
    "two hours of cooking; it freezes for 3 months and it is better the next day anyway. "
    "Reheat it once, until it is piping hot right through, and don't leave it out on the "
    "hob overnight.")


def _the_pot_keeps(memory, understood):
    said = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    if A_COOK_CLOCK_VERB.search(said) and not A_KEEPING_CUE.search(said):
        return ""
    return A_POT_OF_CHILLI_KEEPS


ENTRIES = (
    entry("chilli-keep",
          (("chilli", "chillies", "chilli pepper", "jalapeno", "jalapenos", "habanero",
            "scotch bonnet"),
           ("use up", "keep", "keeping", "store", "storage", "how long", "last", "left over",
            "leftover", "glut", "plenty of")),
          lambda memory, understood: _the_vegetables_or_the_pot(
              memory, understood,
              "Loose in the fridge drawer they keep a week or two, and longer in a paper bag than "
              "in plastic: the bag holds the moisture that turns them soft. A glut is better "
              "frozen or dried than left to go wrinkly - both keep the heat - and a handful also "
              "becomes chilli oil, which is the fastest way to use up twenty at once.",
              _the_plans_keeping_answer),
          avoid=DISH + HEAT_WORDS + ("too spicy", "too hot", "less spicy", "too dry", "is dry",
                                     "tastes dry",
                        "came out dry", "too wet", "plant", "grow", "growing", "sow", "seedling",
                        "powder", "flakes", "paste", "freeze", "frozen", "drying", "dry them",
                        "instead of", "substitute", "swap", "replace", "oil",
                        "take", "takes", "taking") + COOKED,
          bias=1),
    entry("chilli-pot-keep",
          (("chilli", "chillies", "chilli con carne", "chilli beef"),
           ("keep", "keeps", "keeping", "good for", "last", "lasts", "how long", "store",
            "fridge", "freezer", "freeze", "leftover", "left over")),
          _the_pot_keeps,
          ask=(" pot ", "pot of", "a pot", "batch", "cooked", "made", "leftover", "left over",
               "con carne", " pan ", "pan of", "a pan"),
          avoid=("plant", "grow", "growing", "seedling", "sow", "powder", "flakes", "paste",
                 "how hot", "too spicy", "too dry", "instead of", "con carne", "con carni",
                 "take", "takes", "taking", "simmer", "simmering", "boil", "boiling", "fry",
                 "frying", "oven", "hob", "how long to cook", "cooking time"),
          bias=1),
    entry("curry-heat",
          (("korma", "pasanda", "butter chicken", "tikka masala", "tikka", "rogan josh", "dhansak",
            "balti", "madras", "jalfrezi", "vindaloo", "phal", "naga", "tindaloo", "curry",
            "curries"),
           _HEAT_WORDS),
          _curry_heat,
          avoid=("recipe", "how do i make", "how to make", "calories", "sugar", "healthy",
                 "wine", "beer", "drink", "side", "sides", "goes with", "naan", "rice",
                 "hangover", "heartburn", "reflux", "indigestion", "stomach", "baby", "toddler",
                 "child", "kids", "plant", "grow", "seedling", "powder", "flakes", "paste"),
          bias=1),
    entry("curry-yoghurt",
          (("curry", "curries", "dal", "daal", "dhal", "tikka", "masala", "korma",
            "rogan josh", "balti"),
           ("yoghurt", "yogurt", "dahi", "cream", "coconut milk", "raita", "creme fraiche",
            "crème fraîche", "soured cream", "sour cream")),
          "Yes - a spoonful of yoghurt stirred in at the end is the usual finish: it cools the "
          "heat and rounds off a sharp or bitter edge. Take the pan off the heat first and stir "
          "the yoghurt into a spoonful of the sauce in a cup before it goes back in, so it does "
          "not split; full-fat or Greek yoghurt splits less than low-fat, and a splash of cream "
          "or coconut milk does the same job.",
          avoid=("split", "splits", "splitting", "curdled", "curdle", "curdling", "grainy",
                 "seized", "too thick", "too thin", "watery", "runny", "calories", "healthy",
                 "how many", "protein", "freeze", "frozen", "mouldy", "out of date", "gone off"),
          bias=1),
    entry("chilli-freeze",
          (("chilli", "chillies", "chilli pepper", "jalapeno", "jalapenos", "habanero",
            "scotch bonnet"),
           ("freeze", "frozen", "freezing", "bag up", "ice cube")),
          lambda memory, understood: _the_vegetables_or_the_pot(
              memory, understood,
              "Freeze them whole in a bag and slice them still frozen: they go soft, so they are "
              "for cooking rather than for a salad, but the heat survives a few months. Chopped "
              "into an ice-cube tray with a little oil is the other way, one cube per curry, and "
              "there is no need to blanch them first.",
              _the_cooked_dish_freezing_answer),
          avoid=DISH + ("too spicy", "too hot", "too dry", "is dry", "plant", "grow", "growing",
                        "sow", "not working", "broken", "instead of", "oil",
                        "leftover", "left over", "cooked", "already made", "batch")
          + COOKED,
          bias=1),
    entry("chilli-dry",
          (("chilli", "chillies", "chilli pepper", "jalapeno", "jalapenos", "habanero",
            "scotch bonnet"),
           ("dry", "dried", "drying", "dehydrate", "dehydrator", "dry them out")),
          "Thread them on cotton and hang the string by a sunny window until they are leathery "
          "and rattle when you shake one, which takes two to three weeks in a warm room, or split "
          "them and dry them in a low oven at 60C with the door ajar for six to eight hours. Dry "
          "them whole and they keep a year in a jar; grind them for flakes once they are crisp.",
          avoid=DISH + ("too spicy", "too hot", "too dry", "is dry", "tastes dry", "came out dry",
                        "too wet", "plant", "grow", "growing", "sow", "tumble dryer",
                        "washing", "instead of", "oil",
                        "boiled dry", "boils dry", "boil dry", "boiling dry", "boiled away",
                        "boils away", "caught on the bottom", "stuck to the bottom",
                        "saucepan", "in the pan", "in the pot"),
          bias=1),
    entry("chilli-vegetable",
          (("chilli", "chillies", "chilli pepper", "jalapeno", "jalapenos", "habanero",
            "scotch bonnet", "birds eye", "bird's eye"),
           ("chop", "chopped", "slice", "prepare", "prep", "how hot", "hot", "heat", "spicy",
            "strength", "how strong")),
          "Heat is in the variety before it is in the size: a jalapeno is mild enough to eat raw, "
          "a bird's eye or a scotch bonnet will heat a whole curry, and the same kind varies from "
          "one to the next, so taste a sliver before you commit to two. Chop them small and add "
          "them early for a rounded heat, or late and sliced for a sharp one; the white pith and "
          "the seeds carry most of it, so scraping them out takes the edge off without making it "
          "mild. Wash your hands straight after and keep them off your eyes, or wear gloves for "
          "the very hot ones: the oil stays on skin for hours and soap barely shifts it.",
          avoid=DISH + ("deseed", "de-seed", "seed", "seeds", "pith", "too spicy", "too hot",
                        "less spicy", "mild", "milder", "cool down", "cool it", "flakes",
                        "powder", "paste", "plant", "grow", "growing", "sow", "seedling")),
    entry("chilli-eye",
          (("chilli", "chillies", "chili", "chillis", "jalapeno", "jalapenos", "habanero",
            "scotch bonnet", "chilli oil", "chilli juice"),
           ("in my eye", "in the eye", "in my eyes", "my eye", "my eyes", "eyeball",
            "eye is", "eyes are", "eye hurts", "eyes hurt", "stinging", "stings", "rubbed my eye",
            "rubbing my eye",
            "in her eye", "in his eye", "in their eye", "his eye", "her eye", "their eye")),
          "Don't rub it: rinse the eye with milk if you have some, then clean, cool water or "
          "saline for ten to fifteen minutes with the lid held open, and blink it through. The "
          "burn fades over an hour or so and the redness can last a day. Ring 111 or go to an eye "
          "casualty the same day if the pain is getting worse rather than better, if your sight is "
          "blurred, or if you wear a contact lens - take it out first. Wash your hands and the "
          "knife before you touch your face again, because the oil sits on skin for hours and soap "
          "barely shifts it.",
          avoid=DISH),

    entry("chilli-substitute",
          (("chilli", "chillies", "chilli flakes", "chilli powder", "chilli sauce", "chili",
            "chilli paste", "cayenne", "paprika", "gochujang", "sriracha"),
           ("instead of", "substitute", "substitution", "swap", "replace", "alternative",
            "no chillies", "run out", "ran out", "out of", "stand in", "same as")),
          "Paprika plus a pinch of cayenne is the closest thing to chilli powder: about four parts "
          "paprika to one of cayenne, and smoked paprika if you want the depth back. For flakes, a "
          "teaspoon is roughly one fresh chilli, so half a teaspoon of cayenne or a chopped red "
          "pepper does the job, and a spoon of sriracha, gochujang or hot sauce adds heat and a "
          "little sweetness. Without any of those, black pepper and a little ginger give the bite "
          "even though the flavour is different.",
          avoid=DISH + ("deseed", "de-seed", "pith", "how hot", "how spicy", "too spicy",
                        "too hot", "plant", "grow", "growing", "sow", "seedling", "store",
                        "freeze", "keep", "dry them", "drying", "make chilli oil")),
    entry("chilli-oil",
          (("chilli oil", "chili oil"),
           ("make", "recipe", "how do i", "store", "keep", "last", "shelf life", "infuse",
            "chillies in", "with dried")),
          "Warm 200ml of a plain oil with four sliced chillies and a crushed garlic clove over the "
          "lowest heat for five minutes - it should barely bubble, because burnt chilli turns "
          "bitter - then let it cool completely before you bottle it. Keep it in the fridge and use "
          "it within a fortnight, since fresh garlic and fresh chilli in oil will grow things at "
          "room temperature; dried flakes in oil keep far longer, up to three months cold.",
          avoid=DISH + ("chop", "deseed", "seed", "pith", "how hot", "how spicy", "too spicy",
                        "less spicy", "store chillies", "freeze", "instead of", "substitute",
                        "plant", "grow", "sow")),
    entry("chilli-beans",
          (("chilli", "chili", "chilli con carne", "chili con carne", "chillies"),
           ("beans", "bean", "kidney beans", "kidney bean", "black beans", "pinto beans",
            "cannellini", "baked beans", "haricot", "tin of beans", "tinned beans")),
          "Beans are optional, and it is a regional thing rather than a rule: Tex-Mex chilli "
          "usually has none, and most home versions have kidney beans. If you want them, a 400g "
          "tin of kidney or black beans, drained and rinsed, goes in with the tomatoes so it "
          "simmers the last 30 minutes - about one tin to 500g of mince, and no longer, because "
          "they go floury. Without them, keep the mince at 500g and add an extra onion or a "
          "handful of red lentils with the stock so it does not go dry and sharp. Baked beans are "
          "the sweet one: they work, but they want less sugar and a splash of vinegar in the pot.",
          ask=("chilli", "chili"),
          avoid=("how do i make", "how do you make", "recipe", "green beans", "runner beans",
                 "broad beans", "soak", "soaking", "dried beans", "grow", "plant", "sow",
                 "beans on toast", "side", "salad"),
          guard=_short_of_something_else,
          bias=6),
)

