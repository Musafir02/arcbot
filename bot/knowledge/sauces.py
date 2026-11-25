import re

from .lookup import entry as _entry

ANSWERS = ("cooking", "food-and-drink")

_IS_A_SAUCE = ("sauce", "sauces", "sauce.", "sauces?")

_ASKING = ("sauce", "sauces", "make", "makes", "making", "made", "recipe", "recipes",
           "cook", "cooking", "how",
           "what", "whats", "need", "want", "christmas", "turkey", "roast", "lamb", "beef",
           "pork", "goose", "ham", "dinner", "homemade", "from scratch", "jar", "bought",
           "ahead", "make it ahead", "ahead of time", "in advance", "the day before",
           "keep", "keeps", "keeping", "kept", "last", "lasts", "freeze", "freezes", "freezer",
           "freezing", "frozen", "defrost", "fridge", "refrigerate", "how long",
           "how much", "sugar", "vinegar", "hot", "mild", "quick", "easy", "best", "good",
           "nice", "serve", "served", "with", "goes")
_NOT_A_RECIPE = ("lumpy", "lumps", "lump", "thick", "thicker", "thicken", "thickened",
                 "thickening", "runny", "thin", "watery", "sweet", "sweeter", "too sweet",
                 "sharp", "sour", "bitter", "salty", "bland", "separated", "split", "curdled",
                 "grainy", "gelatinous", "out of date", "use by", "gone off", "mouldy")

_KEEPING = re.compile(
    r"\b(?:keep|keeps|keeping|kept|last|lasts|lasting|freeze|freezes|freezer|freezing|frozen|"
    r"defrost|fridge|refrigerated|refrigerate|how long|how many days|till|until)\b", re.I)

_A_KEEPING_WORD = re.compile(
    r"\b(?:keep|keeps|keeping|kept|last|lasts|lasting|freeze|freezes|freezer|freezing|frozen|"
    r"defrost|fridge|refrigerated|refrigerate)\b", re.I)

_A_COOKING_TIME = re.compile(
    r"\b(?:how long|how many minutes)\b[^.?!]{0,45}?"
    r"\b(?:cook|cooks|cooking|simmer|simmering|boil|boiling|bake|baking|roast|roasting|"
    r"microwave|microwaving|reheat|reheating|stir|stirring|reduce|reducing|whisk|whisking|"
    r"take|takes|leave|on the stove|on the hob|in the oven|stove|hob|oven)\b"
    r"|\b(?:simmer|simmering|cook|cooking|boil|boiling|bake|baking|roast|roasting|stir|"
    r"stirring|reduce|reducing|whisk|whisking)\b[^.?!]{0,30}?\buntil\b", re.I)

_AN_UNTIL = re.compile(r"\b(?:till|until)\b", re.I)

_A_STEP_LENGTH = re.compile(
    r"\b(?:how long|how many minutes|how many hours)\b[^.?!]{0,40}?"
    r"\b(?:sit|sits|sitting|rest|rests|resting|stand|stands|standing|set|sets|setting|"
    r"soak|soaks|soaking|marinate|marinating|chill|chilling|before (?:you )?serv|"
    r"before use|to cool)\b", re.I)

_KEEPS = {
    "bread sauce": (
        "Bread sauce is best the day it is made. It keeps 2 days covered in the fridge, and it "
        "reheats gently with a splash of milk in a pan rather than in the microwave, which makes "
        "the crumbs grainy. It does not freeze well: the sauce splits and the breadcrumbs go "
        "gritty, so make it fresh and reheat what is left."),
    "cranberry sauce": (
        "In a clean jar with a lid the sauce keeps 2 weeks in the fridge, and it freezes for 3 "
        "months in small tubs. Thaw it overnight, because the set loosens a little and a stir "
        "brings it back; it keeps a week once a jar has been opened."),
    "mint sauce": (
        "Mint sauce keeps about a month in a sealed jar in the fridge, and it does not freeze: "
        "the mint goes black and limp and the vinegar takes over. Make it in small amounts and "
        "stir in fresh mint if it has been sitting a while."),
    "apple sauce": (
        "Apple sauce keeps 4 to 5 days in a covered dish in the fridge and freezes for 3 months "
        "in bags or tubs. Thaw it overnight and stir it, because it can look watery once it "
        "defrosts - a spoon of butter or a quick beat brings it back."),
    "horseradish sauce": (
        "Fresh horseradish sauce keeps 3 or 4 days in the fridge, and it does not freeze well: "
        "the cream splits and the heat fades. A jarred one lasts months in the fridge once "
        "opened."),
    "brandy butter": (
        "Brandy butter keeps 2 weeks covered in the fridge and freezes for 3 months - roll it in "
        "a log and slice it cold. Let it soften a few minutes at the table but do not leave it "
        "out of the fridge for long."),
}

_SAUCE_OR_TOUM = _IS_A_SAUCE + ("toum",)
_SAUCE_OR_HOLLANDAISE = _IS_A_SAUCE + ("hollandaise", "bearnaise", "béarnaise")

_IS_A_BRANDY_BUTTER = ("brandy butter", "hard sauce", "brandy cream", "brandy butter sauce")

_GARLIC_EMULSION = (
    "Crush 4 peeled garlic cloves with a good pinch of salt to a smooth paste, then add 200ml of "
    "neutral oil a few drops at a time, beating all the time, and a little lemon juice whenever "
    "it thickens - the garlic takes up the oil and it turns white and thick like mayonnaise. If "
    "it splits, put a fresh clove in a clean bowl and beat the split batch into it a spoonful at "
    "a time. For the quick yoghurt version, stir crushed garlic, lemon and salt into 200g of "
    "thick yoghurt.")
_GARLIC_YOGHURT = (
    "Crush one garlic clove to a paste with a good pinch of salt - crushing rather than chopping "
    "is what stops it biting - then stir it into 200g of thick Greek yoghurt with a squeeze of "
    "lemon and leave it 10 minutes. A tablespoon of mayonnaise keeps it from splitting when it "
    "meets hot food, and grated cucumber, mint or a little cumin turns it into a dip.")


def _garlic_sauce(memory, understood):
    line = ((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    if "yoghurt" in line or "yogurt" in line:
        return _GARLIC_YOGHURT
    return _GARLIC_EMULSION


_SAUCES = (
    (("bread sauce", "breadsauce"),
     "Simmer 300ml of whole milk with half an onion studded with 4 cloves and a bay leaf for 10 "
     "minutes, then fish the onion out, stir in 100g of fresh white breadcrumbs and simmer 3 to 4 "
     "minutes until it is thick and creamy. Season it with salt, pepper and grated nutmeg, and "
     "stir in a knob of butter at the end. Make it an hour ahead and reheat it gently with a "
     "splash of milk.",
     ("stuffing", "stuffing a chicken", "sandwich", "toast", "breadcrumbs for", "stale bread")),
    (("cranberry sauce", "cranberry jam", "cranberries", "cranberry"),
     "Tip 250g of cranberries into a pan with 100g of sugar, the zest and juice of an orange and "
     "2 tablespoons of water, and simmer it 8 to 10 minutes, until the berries pop and it is "
     "thick but still a little chunky. It firms up as it cools, so take it off while it is looser "
     "than you want it on the plate. A jar keeps a week in the fridge and it freezes well.",
     ("juice", "uti", "water infection", "cystitis", "vitamin", "good for you", "healthy",
      "dried", "supplement", "tablets", "grow", "growing", "bush", "bog")),
    (("mint sauce", "mint jelly"),
     "Pour 4 tablespoons of boiling water over 4 tablespoons of sugar and stir until it has "
     "dissolved, add 4 tablespoons of white wine vinegar, then stir in a big handful of mint "
     "chopped as finely as you can and leave it 20 minutes. That is the sweet-sharp mint sauce "
     "for lamb; mint jelly is the bought set version, and a spoon of redcurrant jelly with fresh "
     "mint does the same job in a hurry.",
     ("grow", "growing", "plant", "pot", "dying", "wilted", "yellow", "spread", "take over",
      "peppermint", "tea", "oil", "leaves in")),
    (("apple sauce", "applesauce", "apple compote"),
     "Peel, core and chop 3 cooking apples, put them in a pan with 2 tablespoons of water and 1 "
     "of sugar, and simmer 8 to 10 minutes with the lid on until they collapse. Beat them smooth "
     "or leave it chunky, and stir in a knob of butter for a richer one. Bramleys are the apples "
     "that go fluffy; eaters stay in lumps and taste sweeter.",
     ("skin", "peel", "good for you", "healthy", "vitamin", "baby", "weaning", "tree",
      "grow", "orchard", "variety", "bake in the oven")),
    (("horseradish sauce", "horseradish cream", "horseradish"),
     "Grate fresh horseradish root finely - or use a jarred one - and fold about 2 tablespoons of "
     "it into 4 tablespoons of creme fraiche or whipped double cream with a squeeze of lemon, a "
     "pinch of salt and a little sugar. Grate it near an open window or in a food processor: the "
     "heat is in the fumes, not the flesh, and it hits the back of your nose.",
     ("grow", "growing", "plant", "root in the garden", "is it a weed", "leaves")),
    (("brandy butter", "hard sauce", "brandy cream"),
     "Beat 100g of soft butter with 100g of icing sugar until it is pale, then add 3 to 4 "
     "tablespoons of brandy a spoonful at a time: it should be stiff enough to hold a spoon "
     "upright. Chill it in a dish and serve it cold with Christmas pudding or mince pies, where "
     "it melts into the pudding rather than sitting on top of it.",
     ("how much brandy", "drunk", "alcohol free", "without alcohol", "for a child"),
     _IS_A_BRANDY_BUTTER),
    (("peppercorn sauce", "green peppercorn sauce", "pepper sauce", "peppercorn"),
     "Pour off most of the fat from the pan you cooked the steak in and set it back on a medium "
     "heat: add a splash of brandy or red wine and scrape the brown bits up, then 150ml of stock "
     "and a tablespoon of crushed green peppercorns, and let it reduce by half. Take it off the "
     "heat, stir in 100ml of double cream and a teaspoon of Dijon, and put it back for a minute "
     "until it coats a spoon. Season at the end and taste first: reduced stock is already salty, "
     "and a sauce made with cream takes a lot of pepper.",
     ("grow", "growing", "plant", "peppercorns in", "grinder", "white pepper", "black pepper",
      "sneezing", "buy", "brand", "jar", "shop"),
     _IS_A_SAUCE),
    (("mushroom sauce", "mushroom cream sauce", "creamy mushroom sauce"),
     "Fry 200g of sliced mushrooms in butter over a high heat until the water they give off has "
     "gone and they squeak in the pan, then add a chopped shallot and a splash of wine or stock "
     "and scrape the brown bits up. Add 150ml of stock, reduce it by half, pour in 100ml of cream "
     "and simmer 3 minutes; finish off the heat with thyme or tarragon and a knob of butter. Do "
     "not crowd the pan or they steam grey instead of browning.",
     ("grow", "growing", "foraging", "picking", "poisonous", "magic", "dried", "buy", "shop",
      "keep in the fridge", "gone slimy"),
     _IS_A_SAUCE),
    (("garlic sauce", "toum", "garlic cream", "lebanese garlic sauce", "garlic yoghurt sauce",
      "garlic yogurt sauce"),
     _garlic_sauce,
     ("buy", "jar", "shop", "brand", "grow", "planting", "bread", "chicken kiev",
      "calories", "healthy", "keep", "freeze"),
     _SAUCE_OR_TOUM),
    (("hollandaise", "hollandaise sauce", "bearnaise", "béarnaise"),
     "Whisk 2 egg yolks with a tablespoon of water and a teaspoon of lemon juice in a bowl over a "
     "pan of barely simmering water until it thickens enough to hold a ribbon, then take it off "
     "the heat and beat in 125g of melted butter a few drops at a time, with the bowl still warm "
     "but not hot. Season with salt and a little cayenne. If it gets too thick, a spoon of warm "
     "water loosens it; if it splits, a teaspoon of cold water beaten in hard usually brings it "
     "back. Keep it warm, never hot, or the yolks scramble.",
     ("buy", "jar", "shop", "sachet", "packet", "leftover", "reheat", "freeze",
      "eggs benedict", "poached egg"),
     _SAUCE_OR_HOLLANDAISE),
)


_MADE_IN_THE_PAN = ("peppercorn sauce", "mushroom sauce")



def _keeps(reply, keeping):
    def answer(memory, reading):
        line = ""
        if isinstance(reading, dict):
            line = str(reading.get("norm_text") or reading.get("clean") or
                       reading.get("text") or "")
        if _A_KEEPING_WORD.search(line):
            return keeping or None
        if _AN_UNTIL.search(line) or _A_STEP_LENGTH.search(line):
            return reply(memory, reading) if callable(reply) else reply
        if _A_COOKING_TIME.search(line):
            return None
        if keeping and _KEEPING.search(line):
            return keeping
        if not keeping and _KEEPING.search(line):
            return None
        return reply(memory, reading) if callable(reply) else reply
    return answer


def _rows():
    entries = []
    for number, row in enumerate(_SAUCES):
        names, reply, avoid = row[0], row[1], row[2]
        gate = row[3] if len(row) > 3 else _IS_A_SAUCE
        entries.append(_entry(
            "sauce-" + names[0].replace(" ", "-"),
            (names, _ASKING),
            _keeps(reply, _KEEPS.get(names[0], "")),
            ask=gate,
            avoid=avoid + _NOT_A_RECIPE + (
                () if names[0] in _MADE_IN_THE_PAN
                else ("meat", "steak", "joint", "roasting tin", "gravy", "stock")),
            bias=2 + (1 if number == 0 else 0)))
    return entries


ENTRIES = _rows()
