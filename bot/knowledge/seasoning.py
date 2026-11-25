import re

from .lookup import entry

ANSWERS = ("cooking", "food-and-drink")

_SPICE_AMOUNTS = (
    (("garlic", "cloves of garlic", "clove of garlic", "garlic cloves", "garlic clove"),
     "Two or three cloves for a curry, stew or sauce that serves four: a fat clove is about a "
     "teaspoon once crushed, so a teaspoon of the jarred paste stands in for one."),
    (("garlic powder", "garlic granules"),
     "Half a level teaspoon of garlic powder for a curry for four, which stands in for a clove "
     "or two; granules are weaker, so use a whole teaspoon, and add either one with the liquid "
     "rather than at the end, because they need a minute to soften."),
    (("black pepper", "ground pepper", "peppercorns", "pepper"),
     "Half a teaspoon of ground black pepper for a dish that serves four, stirred in at the end "
     "with the salt: pepper is aroma rather than heat, and it goes flat when it cooks for a long "
     "time, so a long stew wants it twice - once at the start and a little at the end."),
    (("vanilla", "vanilla extract", "vanilla essence"),
     "A teaspoon of vanilla extract in a 20cm cake; essence is weaker, so use two, and vanilla "
     "paste about the same as the extract."),
    (("cinnamon",),
     "A teaspoon or two in a 20cm sponge, and half a teaspoon on a bowl of porridge: start with "
     "one and taste, because an old jar is weaker than a new one."),
    (("baking powder",),
     "Two level teaspoons per 200g of plain flour, which is what lifts a sponge. Self-raising "
     "flour already has it in, so add none there."),
    (("bicarbonate of soda", "bicarbonate", "bicarb", "baking soda"),
     "Half a teaspoon per 200g of plain flour, with something acid - buttermilk, yogurt, lemon "
     "juice - to set it off; on its own it leaves a soapy taste."),
    (("allspice", "ground allspice", "pimento", "pimento berries"),
     "A quarter teaspoon of ground allspice for a 20cm cake, or six berries in a jar of pickle: "
     "it tastes of clove, cinnamon and nutmeg at once, so a little stands in for all three."),
    (("mixed spice", "pumpkin spice"),
     "Two teaspoons in a 20cm cake, or a teaspoon across a dozen buns: it is a blend, so it is "
     "gentler than any single spice in it."),
    (("nutmeg",),
     "A quarter of a whole nut, grated, for a 20cm cake or a pan of rice pudding. Whole nutmeg "
     "keeps its flavour for years and ground loses it in months."),
    (("ground ginger", "ginger"),
     "A teaspoon of ground ginger in a 20cm cake or a stir-fry for four; fresh ginger is about "
     "three times the weight for the same heat."),
    (("garam masala",),
     "A teaspoon or two for a curry for four, stirred in at the very end with the heat off: it "
     "is a finishing blend, and cooked from the start it loses the scent that is the point of "
     "it."),
    (("curry powder", "masala"),
     "A tablespoon of curry powder for a curry for four. Fry it in the oil for half a minute "
     "before the liquid goes in and it tastes twice as strong."),
    (("chilli powder", "chili powder", "cayenne", "chilli flakes", "chili flakes"),
     "Half to one teaspoon for four, and taste before the second half: heat builds as it cooks, "
     "so it is easy to overshoot and hard to take back."),
    (("chilli", "chili", "chillies", "chilis", "chile"),
     "One chilli for four is enough heat for most people: add a second at the end if you want "
     "more, and taking out the seeds and white pith halves the heat without losing the taste."),
    (("cumin", "ground cumin", "cumin seeds"),
     "A teaspoon of ground cumin in a chilli or a curry for four, or a tablespoon of the seeds, "
     "which want thirty seconds in a dry hot pan first to wake them up."),
    (("fresh coriander", "coriander leaves", "coriander to garnish", "coriander garnish"),
     "A small handful of fresh coriander for four, torn in at the end: the stems hold most of "
     "the flavour, so chop them into the sauce and keep the leaves for the top."),
    (("coriander", "ground coriander", "coriander seeds"),
     "A teaspoon of ground coriander for a curry for four; the seeds toast in a dry pan in half "
     "a minute and grind to something fresher and more citrus than the jar."),
    (("turmeric",),
     "Half a teaspoon is colour and a teaspoon is flavour for a dish that serves four; more than "
     "that turns bitter, which is why it is never heaped in."),
    (("paprika", "smoked paprika"),
     "A teaspoon for four is enough for the colour and the smoke; it burns in a hot pan, so add "
     "it with the liquid rather than at the start."),
    (("oregano", "dried oregano"),
     "A teaspoon of dried oregano for four, or a tablespoon of fresh leaves. Dried oregano wants "
     "ten minutes in the sauce to soften; fresh is stirred in at the end."),
    (("thyme", "fresh thyme", "dried thyme", "thyme leaves"),
     "Three or four sprigs of fresh thyme for four, or a teaspoon of the dried leaves: the woody "
     "stems come out before serving, so tie them in a bundle if you want the job easy."),
    (("rosemary", "fresh rosemary", "dried rosemary"),
     "One sprig for a roast for four, or a teaspoon of the needles chopped fine. It is strong "
     "and resinous, so it goes in at the start with the meat rather than at the end."),
    (("sage", "fresh sage", "dried sage"),
     "Four or five leaves for four, or a teaspoon dried and crumbled: it is the strongest of the "
     "soft herbs and turns medicinal if it is doubled, so it is the one to under-do."),
    (("bay leaf", "bay leaves", "bay"),
     "One leaf for a stew or a pan of rice for four, and take it out at the end: two is plenty "
     "in a big pot, and a broken leaf left in is what makes a stew taste of the cupboard."),
    (("basil", "fresh basil", "dried basil"),
     "A handful of fresh leaves for four, torn in off the heat at the end, or a teaspoon of dried "
     "in the sauce while it cooks. Dried basil loses the scent that is the reason to use it."),
    (("parsley", "fresh parsley", "dried parsley"),
     "Two tablespoons of chopped fresh parsley for four, stirred in at the end. Dried parsley is "
     "mostly for colour, so use twice as much and expect little taste from it."),
    (("dill", "fresh dill"),
     "A tablespoon of chopped dill for four, in at the end: it is a soft herb and the scent goes "
     "with heat, so it is stirred through just before the pot comes off."),
    (("mint", "fresh mint", "dried mint"),
     "A handful of leaves for four, torn rather than chopped, or a teaspoon of dried mint. In a "
     "yogurt sauce or a salad it wants to be the last thing that goes in."),
    (("mixed herbs", "italian herbs", "herbes de provence", "dried herbs"),
     "A teaspoon of mixed dried herbs for four; a tablespoon if the pot is a big one and cooking "
     "for an hour or more, because the dried leaves give up their taste slowly."),
    (("spice", "spices", "spice mix", "seasoning", "mixed herbs and spices"),
     "A tablespoon of a ground spice blend for a dish that serves four, and a tablespoon over a "
     "kilo of chicken: taste after the first spoonful, because blends vary more in heat than "
     "their labels let on."),
    (("saffron",),
     "Three or four threads for a paella or a risotto for four, steeped in a spoonful of the hot "
     "stock first: any more than that and it starts to taste of the chemist's shelf."),
    (("star anise", "star aniseed", "stars anise"),
     "One whole star anise for a bottle of mulled wine or a slow-cooked pork for four: it is "
     "liquorice-strong, and two would take over the whole pot."),
    (("clove", "cloves", "ground clove", "ground cloves"),
     "A quarter teaspoon of ground cloves for a 20cm cake, or four to six whole ones in a bottle "
     "of mulled wine: it is strong, and more than that tastes medicinal."),
)
_SPICE_NOT_A_DOSE = ("plant", "planting", "planted", "grow", "growing", "sow", "sowing",
                     "good for", "bad for", "healthy", "safe", "allergy", "allergic",
                     "ate", "eaten", "dog", "cat", "puppy", "kitten", "baby", "toddler",
                     "pregnan", "out of date", "gone off", "mouldy", "price", "prices",
                     "water", "sun", "sunlight", "soil", "compost", "fertiliser",
                     "fertilizer", "plant food", "in a pot", "in the garden",
                     "cost", "buy", "cheapest", "substitute", "instead of", "swap",
                     "each", "servings",
                     "portions", "buns", "rolls", "batches", "a crowd",
                     "how much is", "how much are", "how much for", "jar", "jars",
                     "in a bulb", "in one bulb", "a bulb of", "bulb of",
                     "in my coffee", "in coffee", "in my tea", "in tea",
                     "too much", "how much is too much", "limit", "a day", "per day",
                     "con carne",
                     "bell pepper", "bell peppers", "red pepper", "green pepper",
                     "yellow pepper", "orange pepper", "sweet pepper", "sweet peppers",
                     "jalapeno", "jalapenos", "scotch bonnet", "romano", "padron")


_MULLED_WINE = ("Four to six whole cloves, a cinnamon stick snapped in two and a star anise in a "
                "bottle of red: warm it gently for twenty minutes without letting it boil, and "
                "taste before you add any sugar.")


_PUMPKIN_LATTE = ("A quarter to half a teaspoon for a mug, whisked into the coffee with the milk "
                  "and a little sugar: it is mostly cinnamon, so it needs the sugar to taste of "
                  "anything.")


def _spice_amount(memory, understood):
    said = " " + re.sub(r"[^a-z0-9 ]+", " ",
                        str((understood or {}).get("clean") or "").lower()) + " "
    if any((" " + word + " ") in said for word in _SPICE_NOT_A_DOSE):
        return ""
    if "mulled wine" in said:
        return _MULLED_WINE
    if "pumpkin spice" in said and any(drink in said for drink in
                                       ("latte", "coffee", "cappuccino", "mug", "cup")):
        return _PUMPKIN_LATTE
    first_at, first_len, first_reply = None, 0, ""
    for variants, reply in _SPICE_AMOUNTS:
        for variant in variants:
            found = re.search(r"\b" + variant + r"\b", said)
            if found is None:
                continue
            at = found.start()
            if first_at is None or at < first_at or (at == first_at and len(variant) > first_len):
                first_at, first_len, first_reply = at, len(variant), reply
    return first_reply

ENTRIES = [
    entry("spice-amount",
          (("clove", "cloves", "garlic", "pepper", "black pepper", "ground pepper",
            "peppercorns", "cinnamon", "vanilla", "baking powder", "bicarbonate",
            "bicarb", "baking soda", "mixed spice", "allspice", "pumpkin spice", "nutmeg",
            "ginger", "curry powder", "garam masala", "masala", "chilli powder", "chili powder",
            "cayenne", "chilli flakes", "chilli", "chili", "chillies", "turmeric", "paprika", "cumin", "coriander", "saffron",
            "oregano", "thyme", "rosemary", "sage", "bay leaf", "bay leaves", "bay",
            "basil", "parsley", "dill", "mint", "mixed herbs", "italian herbs", "dried herbs",
            "star anise", "cardamom", "fennel seeds", "mustard seeds",
            "spice", "spices", "spice mix", "seasoning"),
           ("how much", "how many", "much", "many", "amount", "spoon", "spoons",
            "teaspoon", "teaspoons", "tablespoon", "tablespoons",
            "in a curry", "in the curry", "in a stew", "in the stew", "in a sauce",
            "in the sauce", "in a soup", "in the soup", "in a chilli", "in the chilli")),
          _spice_amount,
          bias=3,
          ask=("how much", "how many", "much", "many", "amount", "spoon", "spoons",
               "teaspoon", "teaspoons", "tablespoon", "tablespoons", "grams", "handful"),
          avoid=_SPICE_NOT_A_DOSE +
          ("calories", "carbs", "protein", "how many calories", "cholesterol")),
]
