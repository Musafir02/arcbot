from ..compose import pick
from .lookup import entry

ANSWERS = ("cooking", "food-and-drink")

_FAT_CHOICE = (
    "butter or oil", "oil or butter", "butter or olive oil", "olive oil or butter",
    "butter or margarine", "margarine or butter",
    "which fat", "what fat", "which is the best fat",
)

_ALT_FAT = "|".join(_FAT_CHOICE)

_IN_THE_PAN = (
    "fry", "fries", "fried", "frying", "cook", "cooks", "cooked", "cooking", "roast",
    "roasting", "bake", "baking", "pan", "sear", "searing", "saute", "sauté", "stir fry",
    "griddle", "skillet", "onion", "onions", "potato", "potatoes", "carrot", "carrots",
    "mushroom", "mushrooms", "egg", "eggs", "steak", "chicken", "sausage", "sausages",
    "cake", "sauce", "curry", "pancake", "pancakes", "shallow fry", "deep fry", "oven",
)

_NOT_A_PAN = (
    "healthy", "healthier", "unhealthy", "healthiest", "cholesterol", "calories", "fattening",
    "saturated", "unsaturated", "good for you", "bad for you", "heart", "diet", "dieting",
    "spread", "toast", "on toast", "sandwich", "margarine or butter on", "lurpak",
    "how much", "how many", "keep", "keeps", "last", "lasts", "fridge", "freezer", "freeze",
    "gone off", "off", "rancid", "mouldy", "mould", "substitute", "instead of butter",
    "without butter", "dairy free", "vegan", "allergy", "lactose",
)

_A_DISH_WITH_ITS_OWN_METHOD = (
    "roast potato", "roast potatoes", "roasties", "roast parsnip", "roast parsnips",
    "roast carrot", "roast carrots", "roast veg", "roast vegetables", "roast squash",
    "roast swede", "roast beetroot", "roast celeriac",
)

def _asks_between(line):
    low = " " + _fold(str(line or "")) + " "
    if not any(phrase in low for phrase in (" " + _ALT_FAT + " ")):
        return False
    if not any(" " + word + " " in low for word in _IN_THE_PAN):
        return False
    return not any(" " + word + " " in low for word in _NOT_A_PAN)


def _fold(text):
    return " ".join(str(text or "").lower().split())


THE_CARD = (
    "Oil takes the heat and butter gives the taste: butter starts to burn at about 150C, "
    "so for a hot pan or a hot oven use oil and add butter at the end. Butter on its own "
    "is for a low pan where nothing goes above that heat - onions, mushrooms, eggs, 15 to "
    "20 minutes on a low heat for the onions - and in a cake oil keeps it moist for days "
    "while butter gives the flavour most people expect.")

THE_DECIDER = (
    "For onions either is fine: butter on a low heat for 15 to 20 minutes gives the taste and "
    "will not burn below 150C, and oil takes a hotter pan - so oil for a hard fry and butter for "
    "the onions.",
    "Low heat for butter, high heat for oil: onions in butter on a low heat for 15 to 20 minutes "
    "sweeten without catching, and a pan hot enough to brown goes to the oil.",
)


def _last_reply(memory):
    turns = (memory or {}).get("turns") or []
    if not turns:
        return ""
    return str((turns[-1] or {}).get("bot") or "")


def _fat_for_the_pan(memory, reading):
    said = _last_reply(memory)
    if said.startswith(THE_DECIDER[0][:40]) or said.startswith(THE_DECIDER[1][:40]):
        return None
    if said.startswith(THE_CARD[:40]):
        return pick(THE_DECIDER, memory)
    return THE_CARD


ENTRIES = (
    entry("fat-for-the-pan", (_FAT_CHOICE, _IN_THE_PAN),
          _fat_for_the_pan,
          avoid=_NOT_A_PAN + _A_DISH_WITH_ITS_OWN_METHOD, bias=-1),
)
