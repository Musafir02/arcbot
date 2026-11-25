import re

PRIORITY = -997

A_FIGURE = re.compile(
    r"\bhow (?:many|much)\s+(?:grams?|g|kg|calories?|cals?|carbs?|carbohydrate|sugar|salt|"
    r"protein|fat|fibre|fiber|ml|millilitres?|litres?|ounces?|oz|slices?|portions?|servings?|"
    r"spoons?|tablespoons?|teaspoons?)\b[^?!]{0,40}?\b(?:in|of|per|for)\b", re.I)
DISH = re.compile(
    r"\b(?:stew|casserole|pie|quiche|tart|cake|flapjack|brownie|biscuit|scone|pudding|"
    r"crumble|lasagne|lasagna|curry|chilli|soup|broth|risotto|paella|pizza|sandwich|"
    r"wrap|salad|roast|stir ?fry|noodle|dumpling|loaf|bake|smoothie|porridge|granola|"
    r"muffin|pastry|gravy|sauce|dressing|hummus|dip|pancake|omelette|frittata)\b", re.I)
THEIRS = re.compile(
    r"\b(?:my|the one i|i made|i baked|i cooked|homemade|home made|left ?overs?)\b|"
    r"\b(?:portion|serving|slice|bowl|plate|helping)\b", re.I)

POOL = (
    "The recipe and the portion are what set that, not a general figure: the weights on your own "
    "recipe card or the label on the pack, divided by how many it served. Tell me what went in "
    "and how many it made, and I will work the sum out with you.",
    "Nothing here can know that one - it depends what went into it and how much of it you had. "
    "Your recipe or the pack has the figures for the whole thing, so halve it or quarter it; "
    "give me the amounts and I will do the division.",
)


def respond(text, memory):
    clean = " ".join(str(text or "").lower().split())
    if not clean:
        return None
    if not A_FIGURE.search(clean):
        return None
    if not (DISH.search(clean) or THEIRS.search(clean)):
        return None
    return POOL[0]
