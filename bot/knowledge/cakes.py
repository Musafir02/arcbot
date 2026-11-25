import re

ANSWERS = ("cooking", "food-and-drink")


_CAKE_SHAPES = (("20cm tin", "20cm tins", 8, 10),
                ("23cm tin", "23cm tins", 12, 14),
                ("25cm tin", "25cm tins", 18, 20),
                ("30 x 20cm traybake", "30 x 20cm traybakes", 15, 18))
_CAKE_COUNTS = {"a dozen": 12, "dozen": 12, "ten": 10, "twelve": 12, "fifteen": 15,
                "sixteen": 16, "eighteen": 18, "twenty": 20, "twenty five": 25,
                "thirty": 30, "thirty five": 35, "forty": 40, "forty five": 45,
                "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90,
                "a hundred": 100, "hundred": 100}
_CAKE_CLOCK = ("minute", "minutes", "min", "mins", "hour", "hours", "cm", "g", "kg",
               "degrees", "second", "seconds", "percent")
_CAKE_DAY_BEFORE = ("Bake it the day before, wrap it well and fill it with buttercream on the "
                    "day.")
_CAKE_SIZE = ("Size it by the tin: 20cm serves 8 to 10, 23cm 12 to 14, 25cm 18 to 20, and a "
              "30 x 20cm traybake cut into squares feeds 15 to 18.")
_CAKE_DOUBLE = ("To double a recipe double every weight and split it between two tins with the "
                "same heat and time.")
_CAKE_DECOR = ("Buttercream or icing between the layers and on top is all a party cake needs: "
               "spread it warm, chill the cake first, and keep it plain or add a handful of "
               "fruit or sweets.")
_CAKE_BASE = ("A two-layer chocolate or madeira sponge is the easy crowd-pleaser: bake it the "
              "day before, wrap it well and fill it with buttercream on the day. One 20cm tin "
              "serves 8 to 10 people generously.")
_CAKE_SIZE_WORDS = ("how much cake", "size", "sized", "big", "bigger", "serve", "serving",
                    "people", "guests", "crowd", "portions", "slices", "serves", "serve",
                    "feeds", "feed", "heads")
_CUPCAKE_WORDS = ("cupcake", "cupcakes", "cup cake", "cup cakes", "fairy cake", "fairy cakes")
_CUPCAKE_KEEP = ("Twelve to a tray and two a head, so one 12-hole tray covers six people: bake "
                 "them at 180C (160C fan) for 12 to 18 minutes and ice them on the day.")


def _cake_count(text):
    text = " " + str(text or "").lower() + " "
    found = []
    for pattern in (r"\b(\d{1,3})\s+(?:people|guests|kids|children|adults|persons|portions|"
                    r"slices|of us|head)\b",
                    r"\bfor\s+(\d{1,3})\b",
                    r"\b(?:feeds|feed|serves|serve)\s+(\d{1,3})\b",
                    r"\bparty\s+of\s+(\d{1,3})\b"):
        for match in re.finditer(pattern, text):
            after = text[match.end():].strip().split(" ")
            if after and after[0].strip(",.") in _CAKE_CLOCK:
                continue
            found.append(int(match.group(1)))
    for words, value in _CAKE_COUNTS.items():
        if re.search(r"\b" + words + r"\b", text):
            found.append(value)
    return max(found) if found else 0


_CAKE_DOUBLE_WORDS = ("double", "doubling", "halve", "halving", "half the", "scale up",
                     "scaling up", "bigger batch", "twice as much", "two batches")
_CAKE_DECOR_WORDS = ("ice", "icing", "iced", "decorate", "decorating", "decorated",
                     "buttercream", "frost", "frosting", "fill it", "filling", "pipe",
                     "piping", "writing on", "writing happy birthday")


def _cake_asks(text, words):
    text = " " + str(text or "").lower() + " "
    for word in words:
        if " " in word:
            if word in text:
                return True
        elif re.search(r"\b" + word + r"\b", text):
            return True
    return False


def _cake_tin_size(text):
    text = " " + str(text or "").lower().replace(" cm", "cm") + " "
    if re.search(r"\b30\s*x\s*20\s*cm\b", text):
        return _CAKE_SHAPES[3]
    for shape in _CAKE_SHAPES[:3]:
        size = shape[0].split("cm")[0]
        if re.search(r"\b" + size + r"\s*cm\b", text):
            return shape
    return None


def _cake_tins(count):
    best = None
    for n20 in range(0, 9):
        for n23 in range(0, 9):
            for n25 in range(0, 9):
                for ntr in range(0, 9):
                    counts = (n20, n23, n25, ntr)
                    tins = sum(counts)
                    if not tins or tins > 12:
                        continue
                    low = sum(n * shape[2] for n, shape in zip(counts, _CAKE_SHAPES))
                    high = sum(n * shape[3] for n, shape in zip(counts, _CAKE_SHAPES))
                    if high < count:
                        continue
                    kinds = len([n for n in counts if n])
                    score = (tins, kinds, high - count)
                    if best is None or score < best[0]:
                        best = (score, counts, low, high)
    return best


_CAKE_NUMBERS = ("", "one", "two", "three", "four", "five", "six")


def cake_plan(memory, understood):
    line = " " + str((understood or {}).get("clean") or "") + " "
    count = _cake_count(line)
    if not count:
        shape = _cake_tin_size(line)
        if shape is not None:
            if "traybake" in shape[0]:
                said = f"A {shape[0]} cut into squares feeds {shape[2]} to {shape[3]}. "
            else:
                said = (f"A {shape[0].replace(' tin', '')} two-layer sponge feeds "
                        f"{shape[2]} to {shape[3]}.")
            return " ".join((said, _CAKE_DAY_BEFORE, _CAKE_DOUBLE)).strip()
        if _cake_asks(line, _CAKE_DOUBLE_WORDS):
            return _CAKE_DOUBLE.strip()
        if _cake_asks(line, _CAKE_DECOR_WORDS):
            return _CAKE_DECOR.strip()
        if _cake_asks(line, _CUPCAKE_WORDS):
            return _CUPCAKE_KEEP
        if _cake_asks(line, _CAKE_SIZE_WORDS):
            return " ".join((_CAKE_SIZE, _CAKE_DAY_BEFORE, _CAKE_DOUBLE)).strip()
        return _CAKE_BASE
    if _cake_asks(line, _CUPCAKE_WORDS):
        trays = -(-count * 2 // 24)
        said = (f"{count * 2} cupcakes for {count} people: two a head, baked at 180C for 12 to 18 "
                "minutes and iced on the day.")
        if trays > 1:
            said += f" That is {trays} trays of 24, and a muffin tray takes 12 at a time."
        return said
    counts = low = high = None
    for index, shape in enumerate(_CAKE_SHAPES[:3] if count <= 20 else ()):
        if count <= shape[3]:
            counts = tuple(1 if i == index else 0 for i in range(4))
            low, high = shape[2], shape[3]
            break
    if counts is None:
        fit = _cake_tins(count)
        if not fit:
            return None
        _score, counts, low, high = fit
    tins = sum(counts)
    parts = [f"{_CAKE_NUMBERS[n]} {_CAKE_SHAPES[i][0] if n == 1 else _CAKE_SHAPES[i][1]}"
             for i, n in enumerate(counts) if n]
    if tins == 1:
        shape = parts[0].split(" ", 1)[1]
        if "traybake" in shape:
            said = f"One {shape} cut into squares feeds {low} to {high}, which covers {count}."
        else:
            said = (f"A {shape.replace(' tin', '')} two-layer sponge feeds {low} to {high}, so one "
                    f"tin covers {count}.")
    else:
        kinds = len(parts)
        said = (f"{', '.join(parts[:-1])} and {parts[-1]}" if kinds > 1 else parts[0])
        said = (f"{said[0].upper()}{said[1:]} "
                f"{'feed' if tins > 1 else 'feeds'} {low} to {high} between them, which covers "
                f"{count}.")
    return " ".join((said, _CAKE_DAY_BEFORE,
                     "Double every weight and split it between the tins with the same heat and "
                     "time.")).strip()


CAKE_KEY = (("cake", "cakes", "cupcake", "cupcakes", "fairy cakes"),
            ("birthday", "party", "celebrate", "celebrating",
             "people", "guests", "crowd", "number", "scale", "scale up", "bigger",
             "double", "doubling", "halve", "how many", "serves", "serve", "feed",
             "serving", "slices", "portions"))
CAKE_AVOID = ("how long", "time", "temperature", "sink", "sank", "sunken", "stuck", "burn",
             "burnt", "nut", "nuts", "allergy", "gluten", "vegan", "egg", "eggs",
             "egg free", "eggless", "butter", "flour", "sugar", "cocoa", "vanilla",
             "what size tin", "which tin", "tin size", "how many tins",
             "clove", "cloves", "cinnamon", "nutmeg", "mixed spice", "allspice", "turmeric",
             "paprika", "cardamom", "saffron", "spice", "spices", "teaspoon", "tablespoon",
             "keep", "keeps", "last", "freeze", "fridge",
             "calorie", "calories", "kcal", "cals")

_EGG_BATTER = ("For batter, use four eggs to 200g plain flour and 300ml milk, with a pinch of salt, "
               "and rest it half an hour: the eggs are what make a Yorkshire rise, so don't cut "
               "them down. That fills a 12-hole tin.")
_EGG_PANCAKE = ("Two eggs to 150g plain flour and 300ml milk makes about eight thin pancakes, "
                "enough for four people. More eggs make them richer and more likely to tear; "
                "they don't make more pancakes.")
_EGG_MERINGUE = ("One egg white to 50g caster sugar, so a meringue nest for four takes two egg "
                 "whites: whisk them to stiff peaks, then add the sugar a spoon at a time until "
                 "it feels smooth between your fingers.")
_EGG_SPONGE = ("Weigh the eggs in their shells and use the same weight of soft butter, caster "
               "sugar and self-raising flour: three eggs fills a 20cm two-layer sandwich tin "
               "(about 175g of each), and four fills a 23cm one. The eggs are the measure, so "
               "there is no fixed count - a bigger bake starts by weighing more eggs.")


_EGG_SKIP = ("Not for the mix: the egg binds a cake and helps it rise, and in most sponges 60g of "
             "yoghurt, half a mashed banana or a tablespoon of ground flax in three of water does "
             "the same job. Egg-free sponges are a little more crumbly and stale sooner, so eat "
             "them within a day or two, and don't expect a swap to work in a meringue or a "
             "genoise, which are made of egg.")


def cake_eggs(memory, understood):
    line = " " + str((understood or {}).get("clean") or "") + " "
    if _cake_asks(line, ("needed", "necessary", "essential", "required", "have to", "can i skip",
                         "skip the egg", "skip eggs", "do without")):
        return _EGG_SKIP
    if _cake_asks(line, ("yorkshire", "batter", "toad in the hole", "popover")):
        return _EGG_BATTER
    if _cake_asks(line, ("pancake", "pancakes", "crepe", "crepes", "drop scone")):
        return _EGG_PANCAKE
    if _cake_asks(line, ("meringue", "meringues", "pavlova")):
        return _EGG_MERINGUE
    return _EGG_SPONGE


CAKE_EGGS_AVOID = ("instead", "instead of", "substitute", "substitutes", "substituting", "swap",
                   "swaps", "swapping", "replace", "replaces", "replacing", "replacement",
                   "without", "egg free", "egg-free", "eggless", "vegan", "flax", "flaxseed",
                   "allergy", "allergic")
CAKE_EGGS_KEY = (("cake", "cakes", "sponge", "sponge cake", "victoria sponge", "madeira", "birthday cake", "sandwich cake", "yorkshire pudding", "batter",
                  "pancakes", "pancake", "meringue", "meringues", "cupcakes", "cupcake"),
                 ("eggs", "egg", "how many eggs"))
