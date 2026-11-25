from .lookup import entry

ANSWERS = ("cooking", "food-and-drink")

SORTS = {
    "basmati": {
        "label": "basmati",
        "time": "10 to 12 minutes",
        "water": "1 part rice to 1.5 parts water",
        "what": "a long grain that cooks up dry and separate, which is why it suits curry",
        "for": "curry, biryani and pilau",
        "stands_in": "If you do not have basmati, jasmine or any long grain cooks the same way at the same water and time.",
    },
    "jasmine": {
        "label": "jasmine rice",
        "time": "10 to 12 minutes",
        "water": "1 part rice to 1.5 parts water",
        "what": "a long grain, softer and a little sweeter than basmati",
        "for": "Thai food, stir-fries and curry",
        "stands_in": "If you do not have jasmine, basmati or any long grain cooks the same way at the same water and time.",
    },
    "long grain": {
        "label": "white rice",
        "time": "10 to 12 minutes",
        "water": "1 part rice to 1.5 parts water",
        "what": "the everyday one and the least fussy",
        "for": "anything",
        "stands_in": "Basmati or jasmine will do just as well at the same water and time.",
    },
    "arborio": {
        "label": "arborio",
        "time": "18 to 20 minutes, with hot stock added a ladle at a time",
        "water": "3 to 4 parts hot stock",
        "what": "a short grain that sheds starch, so it goes creamy as you stir it",
        "for": "risotto",
        "stands_in": "If you do not have arborio, carnaroli is better still, or short grain pudding rice at a push.",
    },
    "carnaroli": {
        "label": "carnaroli",
        "time": "18 to 20 minutes, with hot stock added a ladle at a time",
        "water": "3 to 4 parts hot stock",
        "what": "the best risotto rice: it holds its shape better than arborio and takes a little "
                "more stock",
        "for": "risotto",
        "stands_in": "If you do not have carnaroli, arborio works, though it goes a little softer.",
    },
    "bomba": {
        "label": "bomba rice",
        "time": "18 to 20 minutes",
        "water": "1 part rice to 2.5 or 3 parts stock",
        "what": "a short grain that swells without bursting, so it stays separate",
        "for": "paella",
        "stands_in": "If you do not have bomba, arborio works, though it goes creamier, so do not stir it.",
    },
    "sushi": {
        "label": "sushi rice",
        "time": "12 to 15 minutes",
        "water": "1 part rice to 1.2 parts water",
        "what": "a short grain that goes sticky enough to hold together, then seasoned with "
                "vinegar, sugar and salt",
        "for": "sushi and onigiri",
        "stands_in": "If you do not have sushi rice, pudding rice will do at a push, though it is stickier still.",
    },
    "pudding": {
        "label": "pudding rice",
        "time": "25 to 30 minutes",
        "water": "1 part rice to about 4 parts milk, or half milk and half water",
        "what": "a short grain that goes soft and creamy in milk",
        "for": "rice pudding",
        "stands_in": "If you do not have pudding rice, arborio is very close.",
    },
    "brown": {
        "label": "brown rice",
        "time": "25 to 30 minutes, then 10 minutes off the heat with the lid on",
        "water": "1 part rice to 2 parts water",
        "what": "white rice with the bran left on, which makes it nuttier, chewier and slower to cook",
        "for": "anything white rice does, if you have the extra twenty minutes",
        "stands_in": "If you do not have brown rice, white rice works at 1 to 1.5 for 10 to 12 minutes, but it will not taste the same.",
    },
    "wild": {
        "label": "wild rice",
        "time": "40 to 45 minutes",
        "water": "1 part rice to 2.5 parts water",
        "what": "not rice at all but a grass seed: dark, chewy, and usually mixed into a rice "
                "rather than eaten alone",
        "for": "mixing into long grain rice for colour and bite",
        "stands_in": "There is no real stand-in for wild rice, so leave it out rather than swap it.",
    },
    "sticky": {
        "label": "sticky rice",
        "time": "20 to 25 minutes in a steamer after an hour's soak",
        "water": "1 part rice to 1 part water, then steamed rather than boiled",
        "what": "glutinous rice, which is sticky enough to eat with your fingers",
        "for": "Thai sticky rice and rice balls",
        "stands_in": "If you do not have sticky rice, sushi rice is the nearest thing in a supermarket.",
    },
}

NAMES = {
    "basmati": ("basmati",),
    "jasmine": ("jasmine", "jasmine rice", "thai rice"),
    "long grain": ("long grain", "long-grain", "plain rice", "white rice", "regular rice"),
    "arborio": ("arborio", "risotto rice", "risotto"),
    "carnaroli": ("carnaroli",),
    "bomba": ("bomba", "paella rice"),
    "sushi": ("sushi rice", "sushi"),
    "pudding": ("pudding rice", "rice pudding", "pudding"),
    "brown": ("brown rice", "wholegrain rice", "wholegrain", "brown"),
    "wild": ("wild rice", "wild"),
    "sticky": ("sticky rice", "glutinous rice"),
}

DISHE_DEFAULT = None
DISHES = (
    (("paella", "paellas"), "bomba"),
    (("risotto", "risottos"), "arborio"),
    (("sushi", "onigiri", "maki"), "sushi"),
    (("rice pudding", "pudding"), "pudding"),
    (("biryani", "biriyani", "pilau", "pilaf", "pullao"), "basmati"),
    (("curry", "curries", "kedgeree", "kheer", "dhal", "dal"), "basmati"),
    (("stir fry", "stir-fry", "stirfry"), "jasmine"),
    (("jollof", "nasi goreng"), "long grain"),
    (("sticky rice", "mango sticky rice"), "sticky"),
)

ANY_SORT = ("rice", "basmati", "jasmine", "long grain", "arborio", "carnaroli", "bomba",
            "sushi rice", "pudding rice", "brown rice", "wild rice", "sticky rice",
            "glutinous rice", "paella rice", "risotto rice", "wholegrain rice")

SWAP_ASK = ("instead", "instead of", "swap", "swaps", "swapped", "swap for", "substitute",
            "substitute for", "stand in", "stand-in", "replace", "replacement", "alternative",
            "or can i use", "can i use", "could i use", "what can i use", "use for", "work for",
            "works for", "will it work", "does it work", "ok to use", "okay to use", "fine to use")

DISH_ASK = ("what rice", "which rice", "best rice", "right rice", "rice for", "rice should i",
            "rice do i", "rice to use", "rice goes", "rice with")

NOT_A_SWAP = ("how long", "how much water", "minutes", "time", "keep", "kept", "leftover",
              "left over", "reheat", "freeze", "frozen", "healthy", "healthier", "health",
              "fibre", "fiber", "calories", "calorie", "weight", "blood sugar", "diet",
              "diabetes", "recipe", "how do i make", "how do i cook", "cook it", "wash", "rinse",
              "mushy", "soggy", "burnt", "burned", "rice cooker", "microwave",
              "pasta", "spaghetti", "noodles", "noodle", "potato", "potatoes", "quinoa",
              "couscous", "bulgur", "barley", "bread", "cauliflower", "orzo",
              "dog", "dogs", "cat", "cats", "puppy", "kitten", "baby", "babies", "toddler",
              "parrot", "rabbit", "hamster", "fish", "tortoise", "horse")


def _said(understood):
    said = str((understood or {}).get("clean") or "")
    if not said:
        said = " ".join((understood or {}).get("words") or [])
    return " " + said.lower() + " "


def _sort_named(said, names=None):
    found = []
    for key, words in (names or NAMES).items():
        at = len(said)
        for word in words:
            for form in (" " + word + " ", " " + word + "s "):
                where = said.find(form)
                if where >= 0 and where < at:
                    at = where
                    break
        if at < len(said):
            found.append((at, key))
    return [key for _, key in sorted(found)]


def _dish_recent(memory):
    for turn in reversed(((memory or {}).get("turns") or [])[-4:]):
        said = " " + str(turn.get("user") or "").lower() + " "
        dish, dish_word = _dish_named(said)
        if dish:
            return dish, dish_word
    return None, None


def _dish_named(said):
    for words, sort in DISHES:
        for word in words:
            if " " + word + " " in said or " " + word + "s " in said:
                return sort, word
    return None, None


def _swap(memory, understood):
    said = _said(understood)
    named = _sort_named(said)
    dish, dish_word = _dish_named(said)
    if not dish and (named or _dish_recent(memory)[0]):
        dish, dish_word = _dish_recent(memory)
    wanted_for_dish = SORTS.get(dish, {})

    if len(named) > 1 and named[0] != named[1]:
        held, wanted = named[0], named[1]
        h, w = SORTS[held], SORTS[wanted]
        if (h["water"], h["time"]) == (w["water"], w["time"]):
            return ("%s will stand in for %s on the same water and time - %s, %s - and the "
                    "difference is the grain: it is %s."
                    % (h["label"].capitalize(), w["label"], h["water"], h["time"], h["what"]))
        return ("%s will stand in for %s: it wants %s and %s, where %s wants %s and %s. It is %s, "
                "so the dish comes out with that grain instead."
                % (h["label"].capitalize(), w["label"], h["water"], h["time"],
                   w["label"], w["water"], w["time"], h["what"]))

    if dish and (not named or named[0] == dish):
        w = wanted_for_dish
        said = "For %s, %s is the one: %s, %s. It is %s." % (
            dish_word, w["label"], w["water"], w["time"], w["what"])
        if w.get("stands_in"):
            said += " " + w["stands_in"]
        return said

    if dish and named:
        held = named[0]
        h, w = SORTS[held], wanted_for_dish
        return ("You can use %s in %s, but %s is the one for it: %s, %s. %s is %s, where %s is %s, "
                "so the dish comes out with that grain in it."
                % (h["label"], dish_word, w["label"], w["water"], w["time"],
                   w["label"].capitalize(), w["what"], h["label"], h["what"]))

    if dish:
        w = wanted_for_dish
        said = "For %s, %s is the one: %s, %s. It is %s." % (
            dish_word, w["label"], w["water"], w["time"], w["what"])
        if w.get("stands_in"):
            said += " " + w["stands_in"]
        return said

    if not named:
        return ("Plain long grain rice is the safe one for most things: %s, %s. Basmati and "
                "jasmine are the same water and time with a different grain, and brown rice "
                "wants %s for %s."
                % (SORTS["long grain"]["water"], SORTS["long grain"]["time"],
                   SORTS["brown"]["water"], SORTS["brown"]["time"]))
    held = named[0]
    h = SORTS[held]
    return ("%s works in place of white rice: %s, %s. It is %s."
            % (h["label"].capitalize(), h["water"], h["time"], h["what"]))


def _dish(memory, understood):
    return _swap(memory, understood)


def _swap_reply(memory, understood):
    return _swap(memory, understood)


def _dish_reply(memory, understood):
    return _swap(memory, understood)


ENTRIES = [
    entry("rice-swap", (ANY_SORT, tuple(SWAP_ASK)),
          _swap_reply,
          avoid=NOT_A_SWAP,
          bias=2),

    entry("rice-for-dish", (("rice", "paella", "paellas", "risotto", "risottos", "sushi",
                             "onigiri", "maki", "rice pudding", "biryani", "biriyani", "pilau",
                             "pilaf", "pullao", "sticky rice", "mango sticky rice", "curry",
                             "curries", "kedgeree", "kheer", "dhal", "dal", "stir fry", "stir-fry",
                             "stirfry", "jollof", "nasi goreng"),
                            tuple(DISH_ASK)),
          _dish_reply,
          avoid=NOT_A_SWAP + ("how do i make", "how do i cook a", "recipe for",
                              "how much", "per person", "people", "each"),
          bias=2),
]
