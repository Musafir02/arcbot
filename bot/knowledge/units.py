import math
import re

UNITS = {
    "length": [
        ("mm", ("mm", "millimetre", "millimetres", "millimeter", "millimeters"), 0.001),
        ("cm", ("cm", "centimetre", "centimetres", "centimeter", "centimeters"), 0.01),
        ("m", ("m", "metre", "metres", "meter", "meters"), 1.0),
        ("km", ("km", "kilometre", "kilometres", "kilometer", "kilometers"), 1000.0),
        ("inch", ("in", "inch", "inches"), 0.0254),
        ("foot", ("ft", "foot", "feet"), 0.3048),
        ("yard", ("yd", "yard", "yards"), 0.9144),
        ("mile", ("mi", "mile", "miles"), 1609.344),
    ],
    "mass": [
        ("mg", ("mg", "milligram", "milligrams"), 0.001),
        ("g", ("g", "gram", "grams", "gramme", "grammes"), 1.0),
        ("kg", ("kg", "kilogram", "kilograms", "kilo", "kilos"), 1000.0),
        ("ounce", ("oz", "ounce", "ounces"), 28.349523125),
        ("pound", ("lb", "lbs", "pound", "pounds"), 453.59237),
        ("stone", ("st", "stone", "stones"), 6350.29318),
    ],
    "volume": [
        ("ml", ("ml", "millilitre", "millilitres", "milliliter", "milliliters"), 1.0),
        ("l", ("l", "litre", "litres", "liter", "liters"), 1000.0),
        ("tsp", ("tsp", "teaspoon", "teaspoons"), 5.0),
        ("tbsp", ("tbsp", "tablespoon", "tablespoons"), 15.0),
        ("dessertspoon", ("dsp", "dessertspoon", "dessertspoons"), 10.0),
        ("cup", ("cup", "cups"), 240.0),
        ("mug", ("mug", "mugs"), 250.0),
        ("fl oz", ("fl oz", "floz", "fluid ounce", "fluid ounces"), 28.4131),
        ("pint", ("pt", "pint", "pints"), 568.261),
        ("gallon", ("gal", "gallon", "gallons"), 4546.09),
    ],
    "speed": [
        ("km/h", ("kmh", "km/h", "kph", "kilometres an hour", "kilometers an hour",
                  "kilometres per hour", "kilometers per hour"), 1.0),
        ("mph", ("mph", "miles an hour", "miles per hour"), 1.609344),
    ],
    "time": [
        ("second", ("s", "sec", "secs", "second", "seconds"), 1.0),
        ("minute", ("min", "mins", "minute", "minutes"), 60.0),
        ("hour", ("hr", "hrs", "hour", "hours"), 3600.0),
        ("day", ("day", "days"), 86400.0),
        ("week", ("week", "weeks"), 604800.0),
        ("fortnight", ("fortnight", "fortnights"), 1209600.0),
    ],
    "area": [
        ("sq m", ("sq m", "square metre", "square metres", "square meter", "square meters",
                  "m2", "sqm"), 1.0),
        ("hectare", ("hectare", "hectares"), 10000.0),
        ("sq km", ("sq km", "square kilometre", "square kilometres", "square kilometer",
                   "square kilometers", "km2", "sqkm"), 1000000.0),
        ("sq ft", ("sq ft", "square foot", "square feet", "sqft", "ft2"), 0.09290304),
        ("sq yd", ("sq yd", "square yard", "square yards", "sqyd", "yd2"), 0.83612736),
        ("acre", ("acre", "acres"), 4046.8564224),
        ("sq mile", ("sq mile", "square mile", "square miles", "sqmi", "mi2"),
         2589988.110336),
    ],
}

SYSTEM = {"mm": "metric", "cm": "metric", "m": "metric", "km": "metric", "mg": "metric",
          "second": "metric", "minute": "metric", "hour": "metric", "day": "metric",
          "week": "metric", "fortnight": "metric",
          "g": "metric", "kg": "metric", "ml": "metric", "l": "metric", "tsp": "metric",
          "tbsp": "metric", "km/h": "metric", "inch": "imperial", "foot": "imperial",
          "yard": "imperial", "mile": "imperial", "ounce": "imperial", "pound": "imperial",
          "stone": "imperial", "mph": "imperial", "pint": "imperial", "gallon": "imperial",
          "fl oz": "imperial", "cup": "us",
          "sq m": "metric", "hectare": "metric", "sq km": "metric", "sq ft": "imperial",
          "sq yd": "imperial", "acre": "imperial", "sq mile": "imperial"}

SAID = {"second": "seconds", "minute": "minutes", "hour": "hours", "day": "days",
        "week": "weeks", "fortnight": "fortnights",
        "mm": "mm", "cm": "cm", "m": "metres", "km": "km", "inch": "inches", "foot": "feet",
        "yard": "yards", "mile": "miles", "mg": "mg", "g": "grams", "kg": "kg",
        "ounce": "ounces", "pound": "pounds", "stone": "stone", "ml": "ml", "l": "litres",
        "tsp": "teaspoons", "tbsp": "tablespoons", "dessertspoon": "dessertspoons",
        "cup": "cups", "pint": "pints",
        "gallon": "gallons", "km/h": "km/h", "mph": "mph", "fl oz": "fl oz",
        "sq m": "square metres", "hectare": "hectares", "sq km": "square kilometres",
        "sq ft": "square feet", "sq yd": "square yards", "acre": "acres",
        "sq mile": "square miles"}

SAID_ONE = {"second": "second", "minute": "minute", "hour": "hour", "day": "day",
            "week": "week", "fortnight": "fortnight",
            "inch": "inch", "foot": "foot", "yard": "yard", "mile": "mile", "ounce": "ounce",
            "pound": "pound", "stone": "stone", "cup": "cup", "pint": "pint",
            "gallon": "gallon", "tsp": "teaspoon", "tbsp": "tablespoon",
            "dessertspoon": "dessertspoon", "m": "metre",
            "fl oz": "fluid ounce", "l": "litre", "g": "gram", "km": "km",
            "kg": "kilogram", "ml": "ml", "mm": "mm",
            "mg": "mg", "cm": "cm", "km/h": "km/h", "mph": "mph",
            "sq m": "square metre", "hectare": "hectare", "sq km": "square kilometre",
            "sq ft": "square foot", "sq yd": "square yard", "acre": "acre",
            "sq mile": "square mile"}

GRAMS_PER_CUP = (
    ("icing sugar", 120), ("brown sugar", 220), ("sugar", 200),
    ("flour", 120), ("cornflour", 120), ("oats", 90),
    ("butter", 227), ("margarine", 227),
    ("rice", 185), ("couscous", 175), ("lentils", 190), ("breadcrumbs", 110),
    ("milk", 240), ("water", 240), ("cream", 240), ("yogurt", 245), ("yoghurt", 245),
    ("honey", 340), ("oil", 220), ("jam", 320), ("peanut butter", 260),
    ("grated cheese", 100), ("cheese", 100),
    ("chocolate chips", 170), ("chocolate", 170), ("cocoa", 85),
    ("nuts", 140), ("almonds", 140), ("cashews", 140), ("peanuts", 145), ("walnuts", 100),
    ("raisins", 150), ("pumpkin seeds", 130),
    ("salt", 288), ("baking powder", 190),
)

GRAMS_PER_TSP = (
    ("baking powder", 4), ("bicarbonate", 4), ("bicarb", 4), ("baking soda", 4),
    ("yeast", 3), ("salt", 6), ("cinnamon", 2.6), ("paprika", 2.4), ("cumin", 2.1),
    ("turmeric", 2.4), ("cayenne", 1.8), ("spice", 2.5), ("pepper", 2.3),
    ("sugar", 4.2), ("cocoa", 2.5), ("flour", 2.6), ("cornflour", 2.5), ("butter", 4.7),
    ("oil", 4.5), ("honey", 7), ("milk", 5), ("water", 5), ("oats", 3),
)

PIECE_GRAMS = (
    ("clove of garlic", 5), ("garlic clove", 5), ("bulb of garlic", 45),
    ("garlic bulb", 45),
    ("slice of bread", 36), ("slice of ham", 20), ("slice of cheese", 20),
    ("slice of bacon", 25), ("rasher", 25),
    ("slice of cake", 60), ("slice of pizza", 100), ("slice of toast", 30),
    ("bread roll", 60), ("crumpet", 60), ("pancake", 40),
    ("chicken breast", 170), ("chicken thigh", 100), ("drumstick", 100),
    ("egg", 55), ("banana", 120), ("apple", 150), ("orange", 140), ("satsuma", 70),
    ("pear", 170), ("peach", 150), ("plum", 70), ("lemon", 100), ("lime", 70),
    ("avocado", 150), ("potato", 170), ("onion", 150), ("carrot", 80), ("tomato", 120),
    ("courgette", 200), ("pepper", 160), ("mushroom", 20), ("aubergine", 250),
    ("cauliflower", 700), ("broccoli", 400),
    ("swede", 900), ("cucumber", 300), ("butternut squash", 1000), ("sweet potato", 200),
    ("cabbage", 900), ("leek", 200), ("parsnip", 150), ("beetroot", 150), ("turnip", 250),
    ("head of celery", 400), ("head of broccoli", 400), ("head of cauliflower", 700),
    ("bunch of grapes", 400), ("punnet of strawberries", 300),
    ("bunch of spring onions", 100), ("bunch of spring onion", 100),
    ("bunch of parsley", 30), ("bunch of coriander", 30), ("bunch of mint", 30),
    ("bunch of basil", 30), ("bunch of dill", 20), ("bunch of thyme", 20),
    ("bunch of rosemary", 20), ("bunch of chives", 20), ("bunch of sage", 20),
    ("punnet of cherry tomatoes", 250), ("punnet of raspberries", 300),
    ("lettuce", 300), ("head of lettuce", 300), ("iceberg lettuce", 600), ("round lettuce", 200),
    ("punnet of blueberries", 200), ("fennel bulb", 250), ("red cabbage", 900),
    ("sausage", 60), ("strawberry", 12), ("sprout", 10), ("raspberry", 4),
    ("biscuit", 10), ("square of chocolate", 10),
)

_WHOLE_PIECE = tuple(name for name, _grams in PIECE_GRAMS if " of " in name)

_DISH_AFTER = re.compile(
    r"\s+(?:pie|pies|bread|soup|soups|sandwich|sandwiches|curry|curries|salad|salads|sauce|"
    r"sauces|cake|cakes|tart|tarts|crumble|smoothie|smoothies|juice|juices|jam|chutney|toast|"
    r"stew|stews|casserole|risotto|pizza|pizzas|burger|burgers|wrap|wraps|muffin|muffins|"
    r"pancake|pancakes|batter|filling|topping|chips|mash|puree|dip|dressing|mayo|stock|broth|"
    r"crisps|pickle|relish|ketchup|crust|pastry|dough|flour|powder|extract|oil|wine|"
    r"cordial|squash|tea|coffee|milkshake|yoghurt|yogurt)\b")
_MEASURE_AFTER_PIECE = re.compile(
    r"\b(?:in|into)\s+(?:cups?|ml|mls|millilitres?|milliliters?|litres?|liters?|pints?|"
    r"fl\s*oz|fluid ounces?)\b")

_WHOLE_THING = re.compile(r"\b(?:heads?|bunch(?:es)?|punnets?)\s+of\s+")
_UNCOUNTED = re.compile(
    r"\b(?:tin|tins|can|cans|jar|jars|packet|packets|pack|packs|box|boxes|bag|bags|"
    r"punnet|punnets|bunch|bunches|tub|tubs|carton|cartons|loaf|loaves|head|heads|"
    r"handful|handfuls|scoop|scoops|bottle|bottles)\b")
_COUNT = re.compile(
    r"(?<![\w.])(three[\s-]quarters?|two[\s-]thirds?|half|a\s+half|quarter|a\s+quarter"
    r"|a\s+third"
    r"|(?:one|two|three|four)\s+and\s+a\s+half"
    r"|\d+(?:\.\d+)?|a|an|one|two|three|four|five|six|seven|eight|nine|ten)"
    r"(?:\s+of)?(?:\s+an?)?"
    r"\s+(?:(?:small|large|medium|big|whole|ripe|fresh|cooked|raw)\s+)?$")

AS_KITCHEN_SAYS = {"cheese": "grated cheese", "chocolate": "grated chocolate",
                   "cocoa": "cocoa powder"}

_COMPONENT = re.compile(
    r"\bhow (?:much|many)\s+(?:of\s+)?(?:grams?\s+of\s+)?"
    r"(?:sugar|salt|fat|protein|fibre|fiber|carbs?|carbohydrates?|calories|kcal|alcohol|"
    r"caffeine|sodium|calcium|iron|vitamins?)\b")
_WEIGH = re.compile(r"\b(?:weigh|weighs|weight|heavy|heavier)\b")

_COMPONENT_MEASURED = re.compile(
    r"\bhow (?:much|many)\s+(?:of\s+)?(?:grams?\s+of\s+)?"
    r"(?P<component>sugar|salt|fat|protein|fibre|fiber|carbs?|carbohydrates?|calories|kcal|"
    r"alcohol|caffeine|sodium|calcium|iron|vitamins?)"
    r"(?:\s+(?:is|are)(?:\s+there)?)?\s+(?:in|per)\s+(?:a|one|1|an)\s+"
    r"(?:level\s+|heaped\s+)?(?P<measure>teaspoons?|tablespoons?|tbsp|tsp|dessertspoons?|"
    r"spoons?|spoonfuls?|cups?)(?:\s+of\s+(?P<again>[a-z]+))?\s*[?.!]*$")


def _the_component_is_the_whole_measure(clean):
    found = _COMPONENT_MEASURED.search(clean)
    if not found:
        return False
    again = found.group("again")
    if not again:
        return True
    component = found.group("component")
    return again in (component, component + "s")


_DRY_IN_A_MEASURE = re.compile(
    r"\bhow (?:much|many)\s+(?:of\s+)?(?:grams?\s+of\s+)?"
    r"(?P<food>icing sugar|brown sugar|cocoa powder|cocoa|cornflour|breadcrumbs|peanut butter|"
    r"flour|jam|cream|yoghurt|yogurt|oats|rice|cheese|chocolate)"
    r"(?:\s+(?:is|are)(?:\s+there)?)?\s+(?:in|per)\s+(?:a|one|1|an)\s+"
    r"(?:level\s+|heaped\s+)?(?P<measure>teaspoons?|tablespoons?|tbsp|tsp|dessertspoons?|"
    r"spoons?|spoonfuls?|cups?)(?:\s+of\s+(?P<again>[a-z]+))?\s*[?.!]*$")


def _the_thing_measured_by_itself(clean):
    found = _DRY_IN_A_MEASURE.search(clean)
    if not found:
        held = _COMPONENT_MEASURED.search(clean)
        if not held or not held.group("measure").startswith("cup"):
            return None
        if not _the_component_is_the_whole_measure(clean):
            return None
        found = held
    food = found.groupdict().get("food") or found.group("component")
    again = found.group("again")
    if again and again not in (food, food + "s", food.split()[-1]):
        return None
    return f"how many grams in a {found.group('measure')} of {food}"

OBJECT_GRAMS = (
    ("suitcase", 4000), ("cabin bag", 2500), ("holdall", 1500), ("backpack", 1200),
    ("rucksack", 1200), ("handbag", 800), ("briefcase", 1500),
    ("microwave", 12000), ("kettle", 1000), ("toaster", 1500), ("air fryer", 5000),
    ("slow cooker", 4000), ("washing machine", 70000), ("tumble dryer", 40000),
    ("dishwasher", 45000), ("fridge freezer", 80000), ("fridge", 70000), ("freezer", 40000),
    ("oven", 50000), ("hob", 10000), ("vacuum cleaner", 6000), ("hoover", 6000),
    ("iron", 1200), ("sewing machine", 8000),
    ("laptop", 1500), ("chromebook", 1300), ("tablet", 500), ("ipad", 500), ("phone", 200),
    ("iphone", 200), ("desktop", 8000), ("printer", 8000), ("monitor", 5000),
    ("television", 15000), ("games console", 4000), ("playstation", 4500), ("xbox", 4500),
    ("smart speaker", 700), ("router", 500), ("camera", 600),
    ("bicycle", 12000), ("bike", 12000), ("e-bike", 22000), ("scooter", 12000),
    ("mobility scooter", 40000),
    ("pram", 10000), ("pushchair", 8000), ("wheelchair", 15000), ("car seat", 7000),
    ("car battery", 18000), ("tyre", 8000), ("roof box", 15000), ("caravan", 1200000),
    ("motorhome", 2800000), ("trailer", 300000),
    ("piano", 200000), ("sofa", 50000), ("armchair", 25000), ("mattress", 25000),
    ("wardrobe", 80000), ("desk", 30000), ("dining table", 40000), ("bookshelf", 25000),
    ("chest of drawers", 30000), ("bed", 40000), ("cot", 20000), ("bunk bed", 50000),
    ("coffee table", 20000), ("laundry basket", 3000), ("trampoline", 40000),
    ("greenhouse", 50000),
    ("boiler", 30000), ("radiator", 10000), ("water butt", 20000), ("wheelie bin", 15000),
)

_COUNTED_THING = re.compile(
    r"(?<![\w.])(?:\d+|a|an|one|two|three|four|five|six|my|your|our|his|her|their|the)\s+$")


def _object_weight(clean):
    if not _WEIGH.search(clean) or re.search(r"\btoo\s+(?:heavy|much)\b", clean):
        return None
    if not re.search(r"\bhow\s+(?:much|heavy|many|big)\b|\bwhat(?:'s| is)?\s+(?:the\s+)?weight\b",
                     clean):
        return None
    if re.search(r"\b(?:cost|costs|price|prices|worth|sell|selling|buy|buying|allowance|"
                 r"allowed|limit|limits|maximum|max|can)\b", clean):
        return None
    best = None
    for name, grams in OBJECT_GRAMS:
        for words in (name, _many(name)):
            match = re.search(rf"(?<![\w.]){re.escape(words)}(?![\w])"
                              r"(?=\s*(?:$|[,?]|weigh|weighs|heavy|about|is\b))", clean)
            if not match:
                continue
            if not _COUNTED_THING.search(clean[:match.start()]):
                continue
            if best is None or len(name) > len(best[0]):
                best = (name, grams)
    if not best:
        return None
    name, grams = best
    article = "an" if name[0] in "aeiou" else "a"
    return f"{article.capitalize()} {name} is about {_kilos(grams)}."


def _many(name):
    if name.endswith("y") and len(name) > 1 and name[-2] not in "aeiou":
        return name[:-1] + "ies"
    if name.endswith(("o", "ch", "sh", "s", "x")):
        return name + "es"
    return name + "s"


def _kilos(grams):
    if grams >= 1000:
        return f"{_fmt(grams / 1000)} kg"
    return f"{_fmt(grams)} g"


_SHARE_OF_CUP = {"cup": 1.0, "tbsp": 1 / 16, "tsp": 1 / 48}

GAS_OVEN = ((1, 140, 275), (2, 150, 300), (3, 170, 325), (4, 180, 350), (5, 190, 375),
            (6, 200, 400), (7, 220, 425), (8, 230, 450), (9, 240, 475))
FAN_COOLER = 20


_NO_PLURAL = ("in", "pt", "mi")


def _build():
    names = {}
    for family, items in UNITS.items():
        for unit, words, _ in items:
            for word in words:
                names[word] = (family, unit)
                if len(word) <= 4 and word.isalpha() and not word.endswith("s") \
                            and word not in _NO_PLURAL:
                    names.setdefault(word + "s", (family, unit))
    pattern = "|".join(re.escape(word) for word in sorted(names, key=len, reverse=True))
    return names, re.compile(r"(?<![\w.])(?:" + pattern + r")(?![\w])")


_NAMES, _UNIT_WORD = _build()
_NUMBER = re.compile(r"(?<![\w.])(\d[\d,]*(?:\.\d+)?|a|an|one)(?![\w])")
_TARGET = re.compile(r"(?:to|in|into|as|->|=)\s*$")
_SAY_K = re.compile(r"(\d)\s*k\b")

_JOINED = re.compile(r"(?<=\d)(?=\s*(?:kg|mg|ml|cm|mm|km|oz|lbs|lb|ft|in|st|pt|g|l|"
                     r"m|metres?|meters?)\b)")

_FRACTION = {("1", "4"): 0.25, ("1", "2"): 0.5, ("3", "4"): 0.75, ("1", "3"): 1 / 3,
             ("2", "3"): 2 / 3}
_SLASH = re.compile(r"(?<![\w.])(\d)\s*/\s*(\d)(?![\d/])")
_AND_A_HALF = re.compile(r"(?<![\w.])(\d|one|two|three|four|five)\s+and\s+a\s+half\b")
_SAID_WHOLE = {"a": 1, "an": 1, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
_UNIT_AND_A_HALF = re.compile(r"(?<![\w.])(?:(?P<count>\d+|an?|one|two|three|four)\s+)?"
                              r"(?P<unit>cups?|tablespoons?|tbsp|teaspoons?|tsp|ounces?|oz|"
                              r"pints?|quarts?|litres?|liters?|sticks?)\s+and\s+a\s+half\b")
_MIXED = re.compile(r"(?<![\w.])(\d+)\s+(\d)\s*/\s*(\d)(?![\d/])")

_WORD_FRACTION = ((re.compile(r"\bthree[\s-]quarters?(?:\s+of)?(?:\s+an?)?\b"), "0.75"),
                  (re.compile(r"\btwo[\s-]thirds?(?:\s+of)?(?:\s+an?)?\b"), "0.67"),
                  (re.compile(r"\b(?:one|an?)[\s-]third(?:\s+of)?(?:\s+an?)?\b"), "0.33"),
                  (re.compile(r"\bhalf(?:\s+of)?(?:\s+an?)?\b"), "0.5"),
                  (re.compile(r"\ban?\s+quarter(?:\s+of)?(?:\s+an?)?\b"), "0.25"))


def _factor(family, unit):
    for name, _, factor in UNITS[family]:
        if name == unit:
            return factor
    return None


def _words(unit):
    for family, items in UNITS.items():
        for name, words, _ in items:
            if name == unit:
                return words
    return ()


def _grams(value):
    rounded = value + 1e-9
    return f"{rounded:,.0f}" if abs(value) >= 10 else f"{value:.1f}".rstrip("0").rstrip(".")


def _fmt(value):
    size = abs(value)
    if size >= 1000:
        text = f"{value:,.0f}"
    elif size >= 100:
        text = f"{value:.0f}"
    elif size >= 1:
        text = f"{value:.1f}"
    else:
        text = f"{value:.2f}"
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


def _value(raw):
    if raw in ("a", "an", "one"):
        return 1.0
    try:
        return float(raw.replace(",", ""))
    except ValueError:
        return None


def _mentions(clean):
    found = []
    for match in _UNIT_WORD.finditer(clean):
        family, unit = _NAMES[match.group(0)]
        if match.group(0) == "in" and _number_before(clean, match.start()) is None:
            continue
        found.append((match.start(), match.end(), family, unit))
    return found


def _number_before(clean, start):
    window = clean[max(0, start - 24):start]
    found = None
    for match in _NUMBER.finditer(window):
        if not window[match.end():].strip():
            found = _value(match.group(1))
    return found


def _say(value, unit, one=None):
    if one if one is not None else value == 1:
        return SAID_ONE.get(unit, SAID.get(unit, unit))
    return SAID.get(unit, unit)


_SPLIT = {"week": ("day", 7.0), "day": ("hour", 24.0)}


def _split_time(result, to_unit):
    smaller = _SPLIT.get(to_unit)
    if not smaller or abs(result - round(result)) < 1e-9:
        return None
    small_unit, per = smaller
    whole = int(result)
    rest = round((result - whole) * per)
    if rest == 0 or rest >= per:
        return None
    return (f"{whole} {_say(whole, to_unit)} and {rest} "
            f"{_say(rest, small_unit)}")


def _sentence(value, family, from_unit, to_unit, in_phrase=False):
    factor, other = _factor(family, from_unit), _factor(family, to_unit)
    if not factor or not other:
        return None
    result = value * factor / other
    about = "" if SYSTEM.get(from_unit) == SYSTEM.get(to_unit) else "about "
    left = ("one " + _say(1, from_unit)) if value == 1 else _amount_phrase(value, from_unit)
    split = _split_time(result, to_unit) if family == "time" else None
    if split:
        return f"{left[0].upper()}{left[1:]} is {about}{split}."
    said = _cups_phrase(result, to_unit, spoons=family == "mass" and to_unit == "cup")
    amount = f"{about}{said}" if said != f"{_fmt(result)} {_say(result, to_unit, one=False)}" \
        else f"{about}{_fmt(result)} {_say(result, to_unit, one=_fmt(result) == '1')}"
    if in_phrase and value == 1:
        verb = "is" if abs(result - 1) < 0.06 else "are"
        return f"There {verb} {amount} in {left}."
    return f"{left[0].upper()}{left[1:]} is {amount}."


def _temperature(clean):
    for pattern, wanted, convert in (
        (r"(-?\d+(?:\.\d+)?)\s*(?:degrees?\s*|°\s*)?(?:c|celsius|centigrade)\b"
         r".*?\b(?:in|to|into|as)\s*(?:degrees?\s*)?(?:f|fahrenheit)\b",
         "F", lambda c: c * 9 / 5 + 32),
        (r"(-?\d+(?:\.\d+)?)\s*(?:degrees?\s*|°\s*)?(?:f|fahrenheit)\b"
         r".*?\b(?:in|to|into|as)\s*(?:degrees?\s*)?(?:c|celsius|centigrade)\b",
         "C", lambda f: (f - 32) * 5 / 9),
    ):
        match = re.search(pattern, clean)
        if match:
            value = float(match.group(1))
            source = "°C" if wanted == "F" else "°F"
            if wanted == "C":
                mark, celsius, fahrenheit = min(GAS_OVEN, key=lambda row: abs(row[2] - value))
                if abs(fahrenheit - value) <= 12:
                    return (f"{_fmt(value)}{source} is about {_fmt(convert(value))}°C - gas mark "
                            f"{mark}, which most recipes call {_fmt(celsius)}°C.")
            return f"{_fmt(value)}{source} is {_fmt(convert(value))}°{wanted}."
    return None


_C_ASKS = re.compile(r"\bcelsius|\bcentigrade|\bdegrees? c\b|°c\b|\bc\b")
_F_ASKS = re.compile(r"\bfahrenheit|\bdegrees? f\b|°f\b|\bf\b")


_BARE_TEMPERATURE = re.compile(
    r"\s*(?:convert\s+)?(?:degrees?\s+)?(?:c|celsius|centigrade|f|fahrenheit)\s+"
    r"(?:to|in|into)\s*(?:degrees?\s+)?(?:c|celsius|centigrade|f|fahrenheit)\s*")


def _temperature_rule(clean):
    if _NUMBER.search(clean):
        return None
    if not (_HOW_TO.search(clean) or _BARE_TEMPERATURE.fullmatch(clean)):
        return None
    celsius = _C_ASKS.search(clean)
    fahrenheit = _F_ASKS.search(clean)
    if celsius and fahrenheit:
        if celsius.start() < fahrenheit.start():
            return ("Multiply the Celsius by 9, divide by 5 and add 32: 20°C is 68°F. The quick "
                    "way in your head is to double it and add 30, which is close enough for "
                    "the weather.")
        return ("Take away 32, then multiply by 5 and divide by 9: 68°F is 20°C. The quick way "
                "in your head is to take away 30 and halve it.")
    return None


def _mark_for(celsius):
    return min(GAS_OVEN, key=lambda row: abs(row[1] - celsius))


def _oven(clean):
    mark_said = re.search(r"gas\s*mark\s*(\d)", clean)
    fan_asked = bool(re.search(r"\bfan\b", clean))
    gas_asked = bool(re.search(r"\bgas\b", clean))
    number = re.search(r"(-?\d{2,3})\s*(?:degrees?\s*|°\s*)?(c|celsius|centigrade|fan|f|fahrenheit)\b",
                       clean)
    if mark_said:
        mark = int(mark_said.group(1))
        row = next((row for row in GAS_OVEN if row[0] == mark), None)
        if not row:
            return None
        return (f"Gas mark {mark} is {row[1]}°C ({row[2]}°F), or {row[1] - FAN_COOLER}°C "
                f"in a fan oven.")
    if not number and fan_asked and not re.search(r"\b(how long|minutes?|hours?|mins)\b", clean):
        bare = re.search(r"(?<![\d.])(\d{2,3})(?![\d.])", clean)
        asking = re.search(r"\b(what|which|how|convert|equivalent|set|change|turn|use)\b", clean)
        if bare and asking and 90 <= float(bare.group(1)) <= 280:
            celsius = float(bare.group(1))
            return (f"{_fmt(celsius)}°C is {_fmt(celsius - FAN_COOLER)}°C in a fan oven, "
                    f"gas mark {_mark_for(celsius)[0]}.")
    if not number:
        return None
    celsius = float(number.group(1))
    fahrenheit = number.group(2) in ("f", "fahrenheit")
    if fahrenheit and (fan_asked or gas_asked):
        celsius = (celsius - 32) * 5 / 9
        said = f"{number.group(1)}°F is {_fmt(celsius)}°C"
        if fan_asked:
            said += f", or {_fmt(celsius - FAN_COOLER)}°C in a fan oven"
        said += f", gas mark {_mark_for(celsius)[0]}"
        return said + "."
    if number.group(2) == "fan" and gas_asked:
        plain = celsius + FAN_COOLER
        return (f"{_fmt(celsius)}°C on a fan setting is {_fmt(plain)}°C in a plain oven, "
                f"gas mark {_mark_for(plain)[0]}.")
    if gas_asked:
        if re.search(r"\d\s*(?:degrees?\s*|°\s*)?(f|fahrenheit)\b", clean):
            celsius = (celsius - 32) * 5 / 9
            return (f"{number.group(1)}°F is gas mark {_mark_for(celsius)[0]}, and "
                    f"{_fmt(celsius)}°C in a plain oven.")
        return (f"{_fmt(celsius)}°C is gas mark {_mark_for(celsius)[0]}, and "
                f"{_fmt(celsius - FAN_COOLER)}°C in a fan oven.")
    if number.group(2) == "fan":
        plain = celsius + FAN_COOLER
        return (f"{_fmt(celsius)}°C on a fan setting is {_fmt(plain)}°C in a plain oven, "
                f"gas mark {_mark_for(plain)[0]}.")
    if fan_asked:
        return (f"{_fmt(celsius)}°C is {_fmt(celsius - FAN_COOLER)}°C in a fan oven, "
                f"gas mark {_mark_for(celsius)[0]}.")
    return None


def _butter(clean):
    if "butter" not in clean or not re.search(r"\bsticks?\b", clean):
        return None
    if not re.search(r"\b(grams?|g|oz|ounces?|cups?|tablespoons?|tbsp|teaspoons?)\b", clean) and not \
            re.search(r"\b(?:how (?:much|many)|what is|whats|what's|weigh\w*)\b", clean):
        return None
    count = re.search(r"(half an?|a|an|one|\d+(?:\.\d+)?)\s+sticks?\b", clean)
    if re.search(r"\bpounds?\b", clean) and not re.search(r"\bcups?\b", clean):
        return "There are four sticks of butter in a pound, 450 g, so a stick is a quarter of one."
    if "block" in clean:
        return ("A stick is 113 g, so a 250 g block is about two and a quarter sticks; butter "
                "sold in sticks is usually four to a 450 g block.")
    said = count.group(1) if count else "a"
    amount = 0.5 if said.startswith("half") else _value(said)
    if amount is None:
        return None
    if re.search(r"\bcups?\b", clean) and not re.search(r"\bgrams?\b|\bg\b", clean):
        return "One stick of butter is half a cup, which is 8 tablespoons or about 113 g."
    if amount == 1:
        return "A stick of butter is about 113 g, which is half a cup or 8 tablespoons."
    if amount == 0.5:
        return "Half a stick of butter is about 57 g, which is 4 tablespoons."
    return f"{_fmt(amount)} sticks of butter is about {_fmt(amount * 113.4)} g."


PACK_GRAMS = (
    ("chopped tomatoes", 400), ("plum tomatoes", 400), ("tomatoes", 400),
    ("baked beans", 415), ("kidney beans", 400), ("black beans", 400), ("cannellini beans", 400),
    ("beans", 400), ("chickpeas", 400), ("chick peas", 400), ("lentils", 400),
    ("sweetcorn", 340), ("tuna", 145), ("sardines", 120), ("coconut milk", 400),
    ("passata", 680), ("condensed milk", 397), ("butter", 250), ("cream", 300),
    ("honey", 340), ("jam", 340), ("marmalade", 340), ("peanut butter", 340),
    ("ice cream", 500), ("cheese", 400), ("cheddar", 400), ("feta", 200),
    ("soup", 400), ("tomato soup", 400), ("peaches", 410), ("pears", 410), ("pineapple", 435),
    ("peas", 400), ("corned beef", 340), ("yogurt", 500), ("yoghurt", 500),
    ("chicken breasts", 500), ("chicken breast", 500), ("mince", 500), ("bacon", 250),
    ("pasta", 500), ("spaghetti", 500), ("penne", 500), ("fusilli", 500), ("macaroni", 500),
    ("sausages", 400),
    ("flour", 1500), ("sugar", 1000), ("rice", 1000),
    ("crisps", 25), ("popcorn", 70), ("biscuits", 200), ("cereal", 375),
    ("salad leaves", 200), ("spinach", 200), ("salad", 200), ("carrots", 1000),
    ("chocolate", 100), ("bread", 800), ("potatoes", 2000), ("carrots", 1000),
    ("onions", 1000),
    ("cola", 330), ("coke", 330), ("lemonade", 330),
    ("toothpaste", 100), ("shampoo", 300), ("conditioner", 250), ("coffee", 200),
    ("grapes", 400), ("olive oil", 500), ("washing up liquid", 500),
    ("ketchup", 460), ("wine", 750), ("beer", 330), ("vinegar", 500),
)
PACK_DRAINED = {"tuna": 112, "sweetcorn": 285, "sardines": 90, "peas": 285,
                "peaches": 220, "pears": 220, "pineapple": 250}
PACK_IN_ML = ("coconut milk", "cream", "ice cream", "cola", "coke", "lemonade",
              "shampoo", "conditioner", "olive oil", "washing up liquid", "wine", "beer",
              "vinegar")
_PACK_WORD = re.compile(r"\b(?:tin|tins|can|cans|jar|jars|packet|packets|pack|packs|bag|bags|"
                        r"block|blocks|carton|cartons|tub|tubs|box|boxes|bar|bars|sleeve|sleeves|"
                        r"tube|tubes|loaf|loaves|punnet|punnets|bottle|bottles)\b")
_PACK_ASK = re.compile(r"\bgrams?\b|\bg\b|\bml\b|\bmls\b|weigh|weighs|weight|ounces?|"
                       r"\boz\b|how\s+(?:big|heavy)|what\s+size|how\s+many\s+(?:grams?|ml|"
                       r"ounces?|oz)\b")


def _pack(clean):
    if not _PACK_WORD.search(clean) or not _PACK_ASK.search(clean):
        return None
    if re.search(r"\b(?:cost|costs|costing|price|prices|cheap|cheaper|expensive)\b", clean):
        return None
    best = None
    for name, grams in PACK_GRAMS:
        if not re.search(rf"\b{re.escape(name)}\b", clean):
            continue
        if name == "cream" and "ice cream" in clean:
            continue
        if best is None or len(name) > len(best[0]):
            best = (name, grams)
    if not best:
        return None
    name, grams = best
    container = _PACK_WORD.search(clean).group(0)
    if container.endswith("s"):
        container = container[:-1]
    amount = f"{grams} ml" if name in PACK_IN_ML else _kilos(grams)
    reply = f"A standard {container} of {name} is {amount}"
    drained = PACK_DRAINED.get(name)
    if drained:
        reply += f", about {drained} g once drained"
    return reply + "."


_COUNT_ASK = re.compile(
    r"\bhow many\s+(?P<piece>[a-z][a-z' -]{1,28}?)\s+"
    r"(?:are\s+there\s+|are\s+|do\s+you\s+get\s+|can\s+you\s+get\s+|would\s+you\s+get\s+|"
    r"come\s+|come in|go\s+)?(?:in|into|per|to)\s+(?:a|an|one|1)\s+"
    r"(?P<box>packet|pack|bag|box|tin|can|jar|punnet|tub|block|bar|loaf|sleeve|tube|carton)\b"
    r"(?:\s+of\s+(?P<of>[a-z][a-z' ]{1,45}?))?(?=[,.?!]|$)")
COUNTED_PACKS = {
    "egg": "A box is six or twelve - the box says which, and the twelve is a dozen.",
    "teabag": "A box is usually 80 or 160 tea bags, and a small box of 40 is common too.",
    "tea bag": "A box is usually 80 or 160 tea bags, and a small box of 40 is common too.",
    "gelatine": "A packet is usually 12 sheets, and one sheet sets about 100ml of liquid.",
    "stock cube": "A box is usually 10 or 12 cubes, and one cube makes about 450ml of stock.",
}
_COUNT_CONTENT = {"slice": ("bread", "slice of bread"), "slices": ("bread", "slice of bread"),
                  "squares": ("chocolate", "square of chocolate"),
                  "square": ("chocolate", "square of chocolate")}
_NOT_A_COUNT = re.compile(r"^(?:grams?|g|mls?|kilos?|kgs?|litres?|liters?|pints?|ounces?|oz|"
                          r"calories?|kcal|carbs?|sugars?|units?|prices?|costs?|servings?|"
                          r"portions?|people|persons?)\b")


def _singular(name):
    for ending, swap in (("ies", "y"), ("oes", "o"), ("ches", "ch"), ("shes", "sh"),
                         ("ses", "s"), ("es", ""), ("s", "")):
        if name.endswith(ending) and len(name) > len(ending):
            gone = name[: -len(ending)] + swap
            if any(gone in (key, _plural_of(key)) for key, _g in PIECE_GRAMS):
                return gone
    return name.rstrip("s") or name


def _table_grams(name, table):
    best = None
    for key, grams in table:
        if name in (key, _plural_of(key)):
            if best is None or len(key) > len(best[0]):
                best = (key, grams)
    return best


def _pack_count(clean):
    found = _COUNT_ASK.search(clean)
    if not found:
        return None
    piece = " ".join(found.group("piece").split())
    box = found.group("box")
    if _NOT_A_COUNT.match(piece):
        return None
    counted = COUNTED_PACKS.get(piece) or COUNTED_PACKS.get(piece.rstrip("s"))
    if counted:
        return counted
    words = (found.group("of") or "").split()
    for size in range(len(words), 0, -1):
        said = " ".join(words[:size])
        counted = COUNTED_PACKS.get(said) or COUNTED_PACKS.get(_singular(said))
        if counted:
            return counted
    content, name = _COUNT_CONTENT.get(piece, (piece, piece))
    if _COUNT_CONTENT.get(piece):
        singular = name
    else:
        singular = _singular(name)
    packed = _table_grams(content, PACK_GRAMS)
    one = _table_grams(singular, PIECE_GRAMS) or _table_grams(name, PIECE_GRAMS)
    if (not packed or not one) and words:
        for size in range(len(words), 0, -1):
            other = " ".join(words[:size])
            if _table_grams(_singular(other), PIECE_GRAMS):
                packed = _table_grams(_singular(other), PACK_GRAMS) or packed
                one = _table_grams(_singular(other), PIECE_GRAMS)
                break
    if not packed or not one or not one[1]:
        return None
    count = int(round(packed[1] / one[1]))
    if count < 2:
        return None
    said = _plural_of(one[0])
    return (f"About {count} {said} in a {box}: a {box} is about {_kilos(packed[1])} and one "
            f"{one[0]} about {_fmt(one[1])}g, so the count moves with the size of both.")


LOOSE = (
    ("knob of butter", "A knob of butter is about 10 g, a scant tablespoon."),
    ("squeeze of lemon", "A squeeze of lemon is about a teaspoon, 5 ml."),
    ("squeeze of lime", "A squeeze of lime is about a teaspoon, 5 ml."),
    ("squeeze of honey", "A squeeze of honey is about a teaspoon, 7 g."),
    ("shot of espresso", "A single shot of espresso is about 25 ml, a double 50 ml."),
    ("shot", "A single shot is 25 ml and a double 50 ml, 25 g and 50 g of a thin liquid."),
    ("glass of wine", "A small glass of wine is 125 ml, a medium 175 ml and a large 250 ml."),
    ("glass of milk", "A glass of milk is about 200 ml, which is roughly 205 g."),
    ("glass of water", "A glass of water is about 200 ml, which is 200 g, and a big one 250 ml."),
    ("mug of tea", "A mug of tea is about 250 ml."),
    ("wedge of lemon", "A wedge of lemon is about 15 g, and gives a teaspoon or two of juice."),
    ("wedge of lime", "A wedge of lime is about 15 g, and gives a teaspoon or two of juice."),
    ("pot of yogurt", "A small pot of yogurt is 150 g and a big one 500 g."),
    ("pot of cream", "A pot of cream is 300 ml, and a small one 150 ml."),
    ("glass of orange juice", "A glass of orange juice is about 200 ml, which takes two or three oranges."),
    ("glass of apple juice", "A glass of apple juice is about 200 ml."),
    ("glass of juice", "A glass of juice is about 200 ml."),
    ("glass of squash", "A glass of squash is about 200 ml, made up with water."),
    ("glass of cola", "A glass of cola is about 200 ml, which is most of a 330 ml can."),
)
_LOOSE_ASK = re.compile(r"\bhow\s+(?:much|many|big)\b|\bgrams?\b|\bg\b|\bml\b|\bmls\b|"
                        r"weigh|weighs|weight|ounces?\b|\boz\b|what\s+size")
_LOOSE_NOT = re.compile(r"\b(?:unit|units|alcohol|drink|drinking|pregnan\w*|calorie\w*|"
                        r"cost|costs|price|prices|cheap|expensive|drunk|drive|driving)\b")
_IN_A_VESSEL = re.compile(
    r"\b(?P<liquid>water|milk|juice|squash|cola|wine)\s+in\s+(?:a|one)\s+"
    r"(?:(?P<size>small|medium|big|large|tall)\s+)?(?P<vessel>glass|cup|mug|pint)"
    r"(?!\s+of\b)")
_VESSEL_ML = {"glass": 200, "cup": 250, "mug": 250, "pint": 568}


def _in_a_vessel(clean):
    found = _IN_A_VESSEL.search(clean)
    if not found:
        return None
    liquid, vessel = found.group("liquid"), found.group("vessel")
    size = found.group("size")
    if vessel == "glass":
        for phrase, reply in LOOSE:
            if phrase == f"glass of {liquid}":
                return reply
    amount = _VESSEL_ML[vessel]
    if size in ("big", "large", "tall"):
        amount = 250
    return (f"A {vessel} of {liquid} is about {amount} ml"
            + (", which is 200 g" if liquid == "water" and vessel == "glass" else "")
            + ".")


def _loose(clean):
    if not _LOOSE_ASK.search(clean) or _LOOSE_NOT.search(clean):
        return None
    in_vessel = _in_a_vessel(clean)
    if in_vessel:
        return in_vessel
    best = None
    for phrase, reply in LOOSE:
        if re.search(rf"\b{re.escape(phrase)}\b", clean):
            if best is None or len(phrase) > len(best[0]):
                best = (phrase, reply)
    return best[1] if best else None


LIQUID_GRAMS_LITRE = (("milk", 1030), ("cream", 1010), ("honey", 1420), ("oil", 920),
                      ("water", 1000))

_PER_CUP = re.compile(r"\bper\s+(?:a\s+|one\s+|each\s+)?(?:cups?|mugs?)\b"
                      r"|\bfor\s+(?:a|one|each|every)\s+(?:cups?|mugs?)\b")


def _liquid_weight(clean):
    if _PER_CUP.search(clean):
        return None
    if not _asks_for_weight(clean):
        return None
    if re.search(r"\b(?:cost|costs|price|prices|worth|sell|buy|buying|calories|protein)\b", clean):
        return None
    liquid = None
    for name, grams in LIQUID_GRAMS_LITRE:
        if re.search(rf"\b{name}\b", clean):
            liquid = (name, grams)
            break
    if not liquid:
        return None
    millilitres, said = None, ""
    for start, end, family, unit in _mentions(clean):
        if family != "volume" or unit in ("cup", "tbsp", "tsp"):
            continue
        value = _number_before(clean, start)
        if value is None:
            continue
        millilitres = value * _factor("volume", unit)
        said = (f"a {SAID_ONE.get(unit, unit)}" if value == 1
                else _amount_phrase(value, unit))
        break
    if millilitres is None:
        if not re.search(r"\bmugs?\b", clean):
            return None
        millilitres, said = 250.0, "a mug"
    grams = millilitres * liquid[1] / 1000.0
    return f"{said[0].upper() + said[1:]} of {liquid[0]} weighs {_mass_said(grams)}."


def _mass_said(grams):
    if grams < 1000:
        return f"{_grams(grams)} g"
    kilos = grams / 1000.0
    text = f"{kilos:.2f}" if kilos < 2 else f"{kilos:,.1f}"
    return f"{text.rstrip('0').rstrip('.')} kg"
BIRD_GRAMS = 500
_BIRDS = ("turkey", "turkeys", "chicken", "chickens", "duck", "ducks", "goose", "geese")

MADE_NOT_MEASURED = frozenset(("the dish", "cake"))

PER_PERSON = (
    (("potato", "potatoes", "new potatoes", "mash"), 250, "g", "potatoes"),
    (("chicken breast", "chicken breasts", "chicken thigh", "chicken thighs", "chicken"),
     200, "g", "chicken"),
    (("mince", "beef mince", "lamb mince"), 150, "g", "mince"),
    (("steak", "steaks"), 200, "g", "steak"),
    (("salmon", "salmon fillet", "salmon fillets"), 150, "g", "salmon"),
    (("fish", "white fish", "cod", "haddock"), 150, "g", "fish"),
    (("meat", "joint", "roast beef", "beef", "lamb", "pork"), 250, "g", "raw meat"),
    (("turkey", "turkeys"), BIRD_GRAMS, "g", "turkey"),
    (("duck", "ducks"), BIRD_GRAMS, "g", "duck"),
    (("goose", "geese"), BIRD_GRAMS, "g", "goose"),
    (("ham", "gammon", "gammon joint"), 250, "g", "ham"),
    (("prawns", "prawn", "king prawns"), 150, "g", "prawns"),
    (("cheese", "cheddar"), 50, "g", "cheese"),
    (("sausage", "sausages"), 2, "each", "sausages"),
    (("egg", "eggs"), 2, "each", "eggs"),
    (("salad", "salad leaves", "lettuce", "rocket", "spinach"), 50, "g", "salad leaves"),
    (("couscous", "bulgur", "bulghur"), 60, "g", "couscous"),
    (("quinoa",), 60, "g", "quinoa"),
    (("lentils", "red lentils", "green lentils", "dal", "dhal"), 75, "g", "dried lentils"),
    (("prawns", "shrimp"), 150, "g", "prawns"),
    (("wine", "red wine", "white wine", "rose", "prosecco", "fizz", "champagne"), 0.5,
     "bottle", "wine"),
    (("chips", "oven chips", "fries", "french fries"), 150, "g", "chips"),
    (("carrot", "carrots"), 1, "each", "carrot"),
    (("sandwich", "sandwiches", "finger sandwiches", "rounds of sandwiches"), 3, "each",
     "sandwiches"),
    (("sausage roll", "sausage rolls"), 3, "each", "sausage rolls"),
    (("quiche", "quiches"), 150, "g", "quiche"),
    (("food", "dish", "casserole", "pasta bake", "curry"), 300, "g", "the dish"),
    (("cake",), 60, "g", "cake"),
    (("stuffing",), 50, "g", "stuffing"),
    (("gravy",), 150, "ml", "gravy"),
    (("pigs in blankets", "pig in blankets"), 3, "each", "pigs in blankets"),
    (("scone", "scones"), 2, "each", "scones"),
    (("hummus", "houmous"), 50, "g", "hummus"),
    (("porridge oats", "porridge", "oats"), 50, "g", "porridge oats"),
    (("soup",), 300, "ml", "soup"),
    (("meatballs", "meatball"), 4, "each", "meatballs"),
    (("slices of bread", "slice of bread", "bread"), 2, "each", "slices of bread"),
    (("sprouts", "brussels sprouts", "brussel sprouts"), 5, "each", "sprouts"),
    (("yorkshire puddings", "yorkshire pudding", "yorkshires"), 2, "each", "yorkshire puddings"),
    (("broccoli",), 80, "g", "broccoli"),
    (("baked beans", "beans"), 150, "g", "baked beans"),
    (("custard",), 100, "ml", "custard"),
    (("coleslaw",), 75, "g", "coleslaw"),
    (("pizza", "pizzas"), 3, "each", "slices of pizza"),
    (("burger", "burgers"), 2, "each", "burgers"),
    (("mince pie", "mince pies"), 2, "each", "mince pies"),
)

PER_PERSON_WHEN_COUNTED = (
    (("rice", "basmati", "long grain rice"), 75, "g", "dry rice"),
    (("pasta", "spaghetti", "penne", "fusilli", "macaroni", "tagliatelle"), 100, "g",
     "dry pasta"),
)

DISHES_FOR_A_TABLE = (
    (("chilli con carne", "chili con carne", "chilli", "chili", "chilli beef", "chilli mince"),
     ("mince",), ("rice",), True, True),
    (("spaghetti bolognese", "bolognaise", "bolognese", "spag bol"),
     ("mince",), ("spaghetti", "pasta"), True, False),
    (("lasagne", "lasagna"), ("mince",), None, True, False),
    (("shepherds pie", "shepherd's pie", "cottage pie"), ("mince",), ("potato",), False, False),
    (("tarka dal", "dhal", "dal"), ("lentils",), ("rice",), False, True),
    (("curry", "curries", "tikka masala", "korma", "bhuna", "jalfrezi"), ("chicken",), ("rice",),
     False, True),
    (("casserole", "stew"), ("meat",), ("potato",), False, False),
)
_TIN_FOR = 4

_CHILLI_THE_VEGETABLE = re.compile(r"\bhow (?:much|many) (?:red |green |small |big |hot )?"
                                   r"chilli(?:es)?\b")

_A_DISH_PART = re.compile(r"\s+(?:powder|powders|sauce|sauces|paste|pastes|oil|flakes|seeds|"
                          r"seasoning|spice|spices|mix|puree|ketchup|granules|extract|essence|"
                          r"leaf|leaves|plant|pepper|peppers)\b")


_A_TIME_IS_THE_ASK = re.compile(
    r"\bhow long\b|\bhow soon\b|\bwhat time\b|\bwhen\b|"
    r"\bhow many (?:hours?|minutes?|mins?|days?)\b")


def _a_dish_for_a_table(clean):
    if not isinstance(clean, str) or not clean:
        return None
    if _A_TIME_IS_THE_ASK.search(clean):
        return None
    people = _people_asked(clean)
    if not people or people < 2 or people > 60:
        return None
    said = " ".join(clean.lower().split())
    named = None
    for names, main, side, tomatoes, spice in DISHES_FOR_A_TABLE:
        for name in names:
            found = re.search(rf"(?<![\w.]){re.escape(name)}(?![\w])", said)
            if not found:
                continue
            if _A_DISH_PART.match(said[found.end():]):
                continue
            if named is None or len(name) > len(named[0]):
                named = (name, main, side, tomatoes, spice)
    if named is None:
        return None
    _name, main, side, tomatoes, spice = named
    if _name in ("chilli", "chili") and _CHILLI_THE_VEGETABLE.search(said):
        return None
    found = []
    for part in (main, side):
        if not part:
            continue
        allowance = _an_allowance(part)
        if allowance:
            found.append(allowance)
    if not found:
        return None
    each = [f"{amount:g} g of {noun}" for amount, noun in found]
    total = [f"{_a_weight(amount * people)} of {noun}" for amount, noun in found]
    dish = _name
    if len(each) == 1:
        per_head = each[0]
        all_of_it = total[0]
    else:
        per_head = " and ".join(each)
        all_of_it = " and ".join(total)
    reply = f"For {people}, {dish} is about {per_head} each: {all_of_it} in all."
    if tomatoes:
        tins = max(1, round(people / _TIN_FOR))
        tin = "tin" if tins == 1 else "tins"
        reply += f" One 400 g tin of tomatoes does four, so {tins} {tin}."
    if spice:
        reply += " Use a little more spice than the recipe says - a big batch tastes milder."
    return reply


def _an_allowance(names):
    for foods, amount, kind, noun in PER_PERSON + PER_PERSON_WHEN_COUNTED:
        if kind != "g" or not amount:
            continue
        if any(name in foods for name in names):
            return amount, noun
    return None


def _a_weight(grams):
    if grams >= 1000:
        kilos = round(grams / 100.0) / 10
        return f"{kilos:g} kg"
    return f"{grams:g} g"


_CONTAINER = re.compile(r"\b(?:bags?|packs?|packets?|tins?|cans?|jars?|boxes?|cartons?)\b")
_AN_ASK = re.compile(r"\bhow (?:much|many|big|large)\b|\bwhat size\b")
CORRECTING = re.compile(r"\b(?:actually|no|nah|sorry|instead|make\s+it|make\s+that|"
                        r"change\s+it|change\s+that|now)\b", re.I)

_PEOPLE_WORD = re.compile(r"\b(?:per\s+(?:person|head)|an?\s+person|an?\s+head(?!\s+of\b)|"
                          r"people|persons?|"
                          r"of\s+us|of\s+you|guests|adults?|between\s+us|party|table\s+for|"
                          r"we(?:'re|\s+are)\s+\d{1,3}\b|there\s+are\s+\d{1,3}\b|"
                          r"expecting\s+\d{1,3}\b|"
                          r"each\s+(?:person|head|guest|adult|of\s+us|one)|family\s+of)"
                          r"\b|\beach\b")
_BARE_FOR_COUNT = re.compile(
    r"\bfor\s+(?:\d{1,2}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\b")
_NOT_A_TABLE_BEFORE = frozenset(("it", "them", "that", "this", "one", "some", "oven"))
NOT_A_TABLE = (
    r"(?!\s*(?:minutes?|mins?|hours?|hrs?|days?|weeks?|months?|years?|slices?|meals?|"
    r"dinners?|lunches?|kg|kilos?|g|grams?|litres?|liters?|ml|pints?|cans?|tins?|packs?|"
    r"batches?|portions?|servings?|kms?|kilometres?|kilometers?|k|miles?|metres?|meters?|"
    r"m|ft|feet|foot|yards?|steps?|laps?|lengths?|rounds?|times?|degrees?))")


_PEOPLE_COUNT = re.compile(
    r"\b(?:for|between)\s+(\d{1,2}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)"
    r"\s+(?:people|persons?|guests|adults|of\s+us|of\s+you|heads)\b"
    r"|\b(\d{1,2})\s+(?:people|persons?|guests|adults|heads)\b"
    r"|\bfamily\s+of\s+(\d|one|two|three|four|five|six|seven|eight|nine|ten)\b"
    r"|\bfor\s+(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"\d{1,2})\b"
    + NOT_A_TABLE +
    r"|\b(?:we(?:'re|\s+are)|there(?:'s|\s+are))\s+"
    r"(\d{1,3}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\b"
    + NOT_A_TABLE +
    r"|\b(\d{1,3}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\s+of\s+us\b"
    r"|\b(?:party|table|group|booking|buffet)\s+(?:of|for)\s+"
    r"(\d{1,3}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\b"
    r"|\b(\d{1,3}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|a dozen)\s+"
    r"coming\b"
    r"|\b(\d{1,3}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\s+(?:of\s+us\s+)?"
    r"(?:for|at)\s+(?:dinner|lunch|supper|christmas|the\s+weekend)\b")
_PORTION_AVOID = re.compile(
    r"\b(?:calories|kcal|carbs?|protein|sugar|fat|fibre|fiber|cost|costs|price|prices|worth|"
    r"budget|alcohol|units|feed|feeds|plant|planting|grow|growing|seeds?|leftover|"
    r"spend|spending|money|pay|paid|shop|shopping|"
    r"dressing|sauces?|mayo|mayonnaise|stock|dips?|"
    r"cream\s+sauces?|salad\s+cream|chutney|"
    r"left\s+over|weigh|weighs|weight|heavy|boards?|cheeseboards?|platters?|"
    r"powders?|spices?|seasoning|ground|flakes|granules|extracts?|essence|herbs?)\b")
_BAKING_PORTION = re.compile(
    r"\b(?:cake|cakes|sponge|cupcakes?|batter|meringues?|pavlova|yorkshire|pancakes?|crepes?|"
    r"pastry|dough|loaf|loaves|bread\s+and\s+butter)\b")
_PORTION_COUNT = re.compile(r"\bhow many (?:portions|servings|slices|pieces|bits|helpings)\b")
_PORTION_WORD = re.compile(r"\bportions?\b|\bservings?\b")
_SAID_PEOPLE = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight",
                9: "nine", 10: "ten", 11: "eleven", 12: "twelve"}
_PEOPLE_VALUE = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
                 "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12}


_TABLE_GROUPS = re.compile(
    r"\b(\d{1,3}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|a dozen)\s+"
    r"(?:adults?|grown[\s-]?ups?|pensioners?|teenagers?|kids?|children|child|toddlers?|"
    r"babies|baby|guests?|people|persons?|heads|of\s+us)\b", re.I)
_GROUP_VALUE = dict(_PEOPLE_VALUE, **{"a dozen": 12})


def people_in_groups(text):
    total = 0
    for raw in _TABLE_GROUPS.findall(str(text or "").lower()):
        count = int(raw) if raw.isdigit() else _GROUP_VALUE.get(raw)
        if count:
            total += count
    return total or None


def _people_asked(clean):
    if re.search(r"\bbetween\s+us\b", clean):
        return 2
    grouped = people_in_groups(clean)
    found = _PEOPLE_COUNT.search(clean)
    if not found:
        return grouped
    raw = next((part for part in found.groups() if part), "")
    said = int(raw) if raw.isdigit() else _PEOPLE_VALUE.get(raw)
    if grouped and (not said or grouped > said):
        return grouped
    return said


def _people_before(memory, statements_only=False, asked_for_an_amount=False):
    if not isinstance(memory, dict):
        return None
    try:
        from .. import memory as mem
        lines = mem.last_user(memory, 2)
        earlier = mem.last_user(memory, 6)
    except Exception:
        return None
    if isinstance(lines, str):
        lines = [lines]
    said = [" ".join(str(line or "").lower().split()) for line in lines or []]
    said = [text for text in said if text
            and not (statements_only and _AN_ASK.search(text))]
    for text in reversed(said):
        if not (_PEOPLE_WORD.search(text) or _PEOPLE_COUNT.search(text)) \
                and not CORRECTING.search(text):
            continue
        if not _a_table_without_people(text):
            continue
        found = _people_asked(text)
        if not found and CORRECTING.search(text):
            found = _a_corrected_figure(text)
        if found:
            return found
    if statements_only or not asked_for_an_amount:
        return None
    older = [" ".join(str(line or "").lower().split()) for line in (earlier or [])][:-2]
    return _a_count_that_still_stands(older)


def _a_count_that_still_stands(older):
    for text in reversed(older):
        if _AN_ASK.search(text):
            continue
        if _PEOPLE_WORD.search(text) or _PEOPLE_COUNT.search(text):
            found = _people_asked(text)
            if found:
                return found
            return None
        if CORRECTING.search(text):
            found = _people_asked(text) or _a_corrected_figure(text)
            if found:
                return found
    return None


_A_FIGURE = re.compile(r"\b(\d{1,3}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\b"
                       + NOT_A_TABLE)


_A_CLOCK = re.compile(r"\bin the (?:morning|afternoon|evening)\b|\bat night\b|"
                      r"\bo ?clock\b|\b[ap]\.?m\.?\b")


def _a_corrected_figure(text):
    if _A_CLOCK.search(text):
        return None
    found = _A_FIGURE.search(text)
    if not found:
        return None
    raw = found.group(1)
    return int(raw) if raw.isdigit() else _PEOPLE_VALUE.get(raw)


def _a_table_without_people(text):
    if _PEOPLE_WORD.search(text) or CORRECTING.search(text):
        return True
    found = _BARE_FOR_COUNT.search(text)
    if not found:
        return False
    before = text[:found.start()].split()
    if not before:
        return True
    return before[-1].strip(".,!?;:").lower() not in _NOT_A_TABLE_BEFORE


def _per_person(clean, memory=None):
    if not re.search(r"\bhow (?:much|many|big|large)\b|\bwhat size\b|"
                     r"\bi (?:need|want)\b|\bi(?:'?m| am) (?:cooking|making)\b", clean):
        return None
    if re.search(r"\b(?:minutes?|mins?|hours?|hrs?|seconds?)\b", clean):
        return None
    if re.search(r"\bi (?:need|want)\s+(?:a|an|one|some)\b", clean):
        return None
    if _COMPONENT.search(clean) or _PORTION_AVOID.search(clean):
        return None
    if _BAKING_PORTION.search(clean) and re.search(r"\begg", clean):
        return None
    people = _people_asked(clean)
    if people is None:
        people = _people_before(
            memory, asked_for_an_amount=bool(re.search(r"\bhow (?:much|many)\b", clean)))
        stated = people is not None and _people_before(memory, statements_only=True) == people
    else:
        stated = True
    if people is None and not _PEOPLE_WORD.search(clean) and not _PORTION_WORD.search(clean):
        for phrase in _WHOLE_PIECE:
            if re.search(rf"\b{re.escape(phrase)}\b", clean):
                return None
    if not _PEOPLE_WORD.search(clean) and people is None and not _PORTION_WORD.search(clean):
        return None
    if _PORTION_COUNT.search(clean) and people is None and not _PEOPLE_WORD.search(clean):
        return None
    best = None
    counted = PER_PERSON_WHEN_COUNTED if (stated and not _CONTAINER.search(clean)) else ()
    for names, amount, kind, noun in PER_PERSON + counted:
        for name in names:
            if re.search(rf"(?<![\w.]){re.escape(name)}(?![\w])"
                         r"(?!\s+(?:dressing|sauce|dip|oil|mayo|mayonnaise|vinaigrette|juice))",
                         clean):
                if best is None or len(name) > len(best[0]):
                    best = (name, amount, kind, noun)
    if not best:
        if people is not None and stated and _PORTION_WORD.search(clean):
            return ("A main is about 300 g a head, a plate of pasta or rice 75 to 100 g dry and "
                    "a buffet six to eight pieces a guest, so for "
                    f"{_said_people(people)} plan on "
                    f"{_mass_of(300 * people)} of the main dish. Tell me what you are cooking "
                    "and I will do the sum for the shopping.")
        return None
    _name, amount, kind, noun = best
    if (noun in MADE_NOT_MEASURED
            and re.search(r"\bi (?:need|want)\s+to\b"
                          r"|\bi(?:'?m| am) (?:cooking|making|baking|roasting|prepping)\b", clean)
            and not re.search(r"\bhow (?:much|many|big|large)\b|\bwhat size\b", clean)):
        return None
    if _name in _BIRDS and re.search(r"\bhow (?:big|large)\b|\bwhat size\b", clean):
        amount, noun = BIRD_GRAMS, _name
    if kind == "each":
        bunch = noun if noun.endswith("s") or " " in noun else noun + "s"
        said = f"{amount} {bunch}" if amount > 1 else f"1 {noun}"
        if people:
            total = (f"{amount * people:g} {bunch}" if amount > 1
                     else f"{_SAID_PEOPLE.get(people, people)} {bunch}")
            return f"About {said} each, so {total} for {_said_people(people)}."
        if not _PEOPLE_WORD.search(clean):
            return f"A portion is about {said}."
        return f"About {said} each."
    if kind == "bottle":
        per = "half a bottle" if amount == 0.5 else f"{amount:g} bottles"
        if not people:
            return f"Allow about {per} of {noun} a guest."
        bottles = int(math.ceil(amount * people))
        return (f"Allow about {per} of {noun} a guest, so {bottles} "
                f"{'bottle' if bottles == 1 else 'bottles'} for {_said_people(people)}.")
    if kind == "ml":
        if people:
            return (f"About {amount} ml of {noun} each, so "
                    f"{_litres_of(amount * people)} for {_said_people(people)}.")
        if not _PEOPLE_WORD.search(clean):
            return f"A portion of {noun} is about {amount} ml."
        return f"About {amount} ml of {noun} each."
    if people:
        return (f"About {_grams(amount)} g of {noun} each, so "
                f"{_mass_of(amount * people)} for {_said_people(people)}.")
    if not _PEOPLE_WORD.search(clean):
        return f"A portion of {noun} is about {_grams(amount)} g."
    return f"About {_grams(amount)} g of {noun} each."


def _said_people(people):
    return _SAID_PEOPLE.get(people, str(people))


def _mass_of(grams):
    if grams >= 1000:
        kilos = f"{grams / 1000:.1f}".rstrip("0").rstrip(".")
        return f"{kilos} kg"
    return f"{_grams(grams)} g"


def _litres_of(ml):
    if ml >= 1000:
        litres = f"{ml / 1000:.1f}".rstrip("0").rstrip(".")
        return f"{litres} litres"
    return f"{ml} ml"


LAND_PLAIN = {
    "acre": "An acre is 4,047 square metres, or 4,840 square yards: a square about 64 metres "
            "on each side, a little under half a hectare, and roughly half a football pitch.",
    "hectare": "A hectare is 10,000 square metres: a square 100 metres on each side, two and a "
               "half acres, or about one and a half football pitches.",
    "sq mile": "A square mile is 2.59 square kilometres, or 640 acres.",
    "sq km": "A square kilometre is a square 1 kilometre on each side: 100 hectares, or about "
             "0.39 of a square mile.",
    "sq m": "A square metre is a square 1 metre on each side, about 10.8 square feet.",
    "sq ft": "A square foot is 144 square inches, or about 0.09 square metres: a square 30cm "
             "on each side.",
    "sq yd": "A square yard is 9 square feet, or about 0.84 square metres: a square 91cm on "
             "each side.",
}

_LAND_ASK = re.compile(r"\bhow (?:big|large|long|wide)\b|\bsize of\b|\bwhat size\b"
                       r"|\bwhat(?:'s| is)\b|\bhow much (?:land|ground|space)\b")


_AREA_PICTURES = (
    ("parking space", "parking spaces", 12.5),
    ("doubles tennis court", "doubles tennis courts", 260.0),
    ("football pitch", "football pitches", 7140.0),
)
_WORD_SHARE = (("three quarters", 0.75), ("two thirds", 2 / 3.0), ("three quarters of", 0.75),
               ("two thirds of", 2 / 3.0), ("a third", 1 / 3.0), ("a quarter", 0.25),
               ("a half", 0.5), ("half", 0.5), ("quarter", 0.25), ("third", 1 / 3.0))
_A_SIZE_JUDGEMENT = re.compile(
    r"\b(?:big|large|small|huge|tiny|sizeable|decent|reasonable|enough)\b"
    r"|\bhow much (?:land|ground|space)\b|\bis that a lot\b")


def _count_said(ratio):
    whole = int(ratio)
    part = ratio - whole
    if part < 0.25:
        return "%d" % whole
    if part < 0.75:
        return ("%d and a half" % whole) if whole else "half"
    return "%d" % (whole + 1)


def _area_pictures(square_metres):
    for name, plural, size in _AREA_PICTURES:
        ratio = square_metres / size
        if ratio < 5 or size == _AREA_PICTURES[-1][2]:
            break
    if ratio < 0.4:
        return "less than half a " + name
    if ratio < 0.75:
        return "about two thirds of a " + name
    if ratio < 1.15:
        return "about a " + name
    if ratio < 1.85:
        return "a bit more than a " + name
    return "about %s %s" % (_count_said(ratio), plural)


def _share_before(clean, start):
    text = clean[:start]
    found = re.search(r"(\d+(?:\.\d+)?)\s*(?:of\s+)?(?:an?\s+)?$", text)
    if found:
        return float(found.group(1))
    for word, value in _WORD_SHARE:
        if re.search(r"\b" + re.escape(word) + r"\s*(?:of\s+)?(?:an?\s+)?$", text):
            return value
    return None


def _land_in_pictures(value, unit, clean=""):
    table = {name: size for name, _, size in UNITS["area"]}
    square_metres = value * table[unit]
    if square_metres < 1:
        return None
    if abs(value - 1) < 1e-9:
        said = "One " + SAID_ONE[unit]
    elif abs(value - round(value)) < 1e-9:
        said = "%d %s" % (round(value), SAID[unit])
    else:
        said = "%s %s" % (_fmt(value), SAID[unit])
    body = "%s is about %s square metres - %s" % (
        said, _fmt(round(square_metres)), _area_pictures(square_metres))
    if square_metres >= 400 and "garden" in clean:
        body += ", which is a generous garden for a house"
    if abs(value - 1) < 1e-9:
        return body + "."
    return body + ". " + LAND_PLAIN[unit]


def _land_size(clean, mentions):
    if len(mentions) != 1:
        return None
    start, end, family, unit = mentions[0]
    if family != "area" or unit not in LAND_PLAIN:
        return None
    if _A_SIZE_JUDGEMENT.search(clean):
        counted = _share_before(clean, start)
        if counted is not None:
            pictured = _land_in_pictures(counted, unit, clean)
            if pictured:
                return pictured
    before = clean[max(0, start - 14):start]
    if not _LAND_ASK.search(clean):
        return None
    if re.search(r"\d\s*$", before) or re.search(r"\b(?:two|three|four|five|ten|twenty)\s+$",
                                                   before):
        return None
    if _UNIT_WORD.search(clean[end:]) or _TARGET.search(clean[:start].strip()):
        return None
    return LAND_PLAIN[unit]


def _height(clean, mentions):
    if not any(unit in ("cm", "m") for _, _, _, unit in mentions):
        return None
    match = (re.search(r"(\d)\s*(?:'|’|ft|foot|feet)\s*(\d{1,2})\s*(?:\"|''|in|inch|inches)?",
                       clean)
             or re.search(r"(\d)\s*(?:ft|foot|feet)\s+(\d{1,2})\b", clean))
    if not match:
        return _metres_in_feet(clean)
    feet, inches = int(match.group(1)), int(match.group(2))
    if not 2 <= feet <= 8 or inches > 11:
        return None
    total = feet * 12 + inches
    return (f"{feet} feet {inches} is about {round(total * 2.54)} cm, or "
            f"{total * 0.0254:.2f} m.")


_ASKS_FEET = re.compile(r"\b(?:feet|foot|ft|tall)\b")

_SAYS_OWN_HEIGHT = re.compile(
    r"\b(?:i'?m|i am|im|my height is|my height's|my height)\b", re.I)
_HEIGHT_METRES = re.compile(r"(?<![\w.])(\d(?:\.\d{1,2})?)\s*(?:m|metres?|meters?)(?!\w)", re.I)
_HEIGHT_CM = re.compile(r"(?<![\w.])(\d{2,3}(?:\.\d)?)\s*(?:cm|centimetres?|centimeters?)(?!\w)",
                        re.I)
_HEIGHT_FEET = re.compile(
    r"(?<![\w.])([2-7])\s*(?:'|\u2019|ft|foot|feet)\s*(\d{1,2})\s*(?:\"|''|in|inch|inches)?(?!\w)",
    re.I)
_HEIGHT_FEET_WORD = re.compile(r"(?<![\w.])([2-7])\s*(?:ft|foot|feet)\s+(\d{1,2})\b", re.I)
_NOT_A_HEIGHT = re.compile(
    r"\b(?:away|from|apart|long|wide|deep|of rope|of wood|of cable|of string|of pipe|of cord)\b",
    re.I)


def _is_a_distance(clean):
    return bool(_NOT_A_HEIGHT.search(clean)) and not re.search(r"\btall\b", clean, re.I)


_ASKS_ELSEWHERE = re.compile(
    r"\b(?:what|which|where|who|whose|should|shall|could|would|can|need|needs|looking for"
    r"|look for|recommend|suggest|ideas|advice|buy|buying|wear|choose|pick|worth|fit|fits)\b",
    re.I)
_A_MEASURE_QUESTION = re.compile(
    r"\b(?:cm|centimetres?|centimeters?|m|metres?|meters?|feet|foot|ft|inches?|inch|tall|height"
    r"|that|this|it|in|convert|converted)\b", re.I)


_A_COMPLAINT = re.compile(
    r"\b(?:hurt|hurts|hurting|ache|aches|aching|achy|sore|pain|painful|kills?|killing"
    r"|blister|blisters|swollen|numb|too (?:small|tight|big|long|short|loose)"
    r"|doesn'?t fit|don'?t fit|does not fit|do not fit|rubbed|rubbing)\b", re.I)


_ASKS_HOW_MANY = re.compile(r"\bhow\s+(?:many|much)\s+(?P<thing>[a-z]+)", re.I)
_A_MEASURE_SAID_ANOTHER_WAY = frozenset(("hand", "hands", "pace", "paces", "span", "spans"))


def _asks_something_else(clean):
    if _A_COMPLAINT.search(clean):
        return True
    for match in _ASKS_HOW_MANY.finditer(clean):
        thing = match.group("thing").lower()
        if not _UNIT_WORD.fullmatch(thing) and thing not in _A_MEASURE_SAID_ANOTHER_WAY:
            return True
    for match in _ASKS_ELSEWHERE.finditer(clean):
        tail = " ".join(clean[match.end():].split()[:5])
        if not _A_MEASURE_QUESTION.search(tail):
            return True
    return False


def _own_height(clean):
    if not _SAYS_OWN_HEIGHT.search(clean):
        return None
    if _is_a_distance(clean):
        return None
    if _asks_something_else(clean):
        return None
    metres, said = None, ""
    found = _HEIGHT_METRES.search(clean)
    if found:
        metres, said = float(found.group(1)), f"{found.group(1)} m"
    if metres is None:
        found = _HEIGHT_CM.search(clean)
        if found:
            metres, said = float(found.group(1)) / 100, f"{found.group(1)} cm"
    if metres is not None:
        if not 1.2 <= metres <= 2.2:
            return None
        total = metres / 0.0254
        feet = int(total // 12)
        inches = round(total - feet * 12)
        if inches == 12:
            feet, inches = feet + 1, 0
        return f"{said} is about {feet} foot {inches} ({total / 12:.1f} feet)."
    match = _HEIGHT_FEET.search(clean) or _HEIGHT_FEET_WORD.search(clean)
    if not match:
        return None
    feet, inches = int(match.group(1)), int(match.group(2))
    if inches > 11:
        return None
    cm = round((feet * 12 + inches) * 2.54)
    return (f"{feet} foot {inches} is about {cm} cm, or {cm / 100:.2f} m.")


def _metres_in_feet(clean):
    if not _ASKS_FEET.search(clean):
        return None
    metres, said = None, ""
    found = re.search(r"(?<![\w.])(\d(?:\.\d{1,2})?)\s*(?:m|metres?|meters?)(?!\w)", clean)
    if found:
        metres, said = float(found.group(1)), f"{found.group(1)} m"
    else:
        found = re.search(r"(?<![\w.])(\d{2,3}(?:\.\d)?)\s*(?:cm|centimetres?|centimeters?)"
                          r"(?!\w)", clean)
        if found:
            metres, said = float(found.group(1)) / 100, f"{found.group(1)} cm"
    if metres is None or not 1.2 <= metres <= 2.2:
        return None
    total = metres / 0.0254
    feet = int(total // 12)
    inches = round(total - feet * 12)
    if inches == 12:
        feet, inches = feet + 1, 0
    return f"{said} is about {feet} foot {inches} ({total / 12:.1f} feet)."


def _cup_of_something(clean):
    if _PER_CUP.search(clean):
        return None
    measure, share = "cup", 1.0
    if re.search(r"\bmugs?\b", clean):
        measure, share = "mug", 240 / 250
    elif _names_unit(clean, "tbsp"):
        measure, share = "tablespoon", 16.0
    elif _names_unit(clean, "tsp"):
        measure, share = "teaspoon", 48.0
    elif _names_unit(clean, "dessertspoon"):
        measure, share = "dessertspoon", 24.0
    text = "a " + measure
    if measure in ("tablespoon", "teaspoon", "dessertspoon"):
        spoon = [(food, grams) for food, grams in GRAMS_PER_TSP
                 if re.search(rf"\b{re.escape(food)}\b", clean)]
        if spoon:
            food, grams = max(spoon, key=lambda row: len(row[0]))
            amount = grams * (240.0 / share) / 5.0
            return f"A {measure} of {food} is about {_fmt(amount)} g."
    named = _food_named(clean)
    if named and _asks_for_weight(clean):
        food, grams = named
        amount = grams if share == 1.0 else max(1, round(grams / share))
        said = AS_KITCHEN_SAYS.get(food, food)
        return f"A {measure} of {said} is about {_grams(amount)} g."
    if _WEIGH.search(clean) or re.search(r"\b(grams?|g|oz|ounces?|kg)\b", clean):
        return ("It depends what is in " + text + ": flour is about 120 g, sugar about 200 g, "
                "butter 227 g. By volume a cup is 240 ml, which is 8 fluid ounces.")
    return None


def _handful(clean):
    if not re.search(r"\bhandfuls?\b", clean):
        return None
    if not (_asks_for_weight(clean) or re.search(r"\bhow much\b", clean)):
        return None
    if re.search(r"\b(?:cost|costs|costing|price|prices|priced|cheap|cheaper|expensive)\b", clean):
        return None
    food = _food_named(clean)
    if food:
        name, grams_per_cup = food
        said = AS_KITCHEN_SAYS.get(name, name)
        return (f"A handful of {said} is about {_grams(round(grams_per_cup / 4))} g, "
                f"since a handful is roughly a quarter of a cup.")
    stuff = ""
    said_food = re.search(r"\bhandfuls?\s+(?:of\s+)?"
                          r"(?!of\b|it\b|them\b|these\b|those\b|that\b)"
                          r"([a-z]+(?:\s+[a-z]+)?)", clean)
    if said_food:
        stuff = " ".join(word for word in said_food.group(1).split() if word not in _NOT_A_FOOD)
    if stuff:
        return (f"A handful of {stuff} is about a quarter of a cup, but the weight depends on "
                "what is in it: 35 g of nuts against 8 g of spinach.")
    return ("A handful is about a quarter of a cup, which comes to roughly 35 g of nuts, "
            "30 g of raisins or 25 g of crisps.")


_NOT_A_FOOD = frozenset((
    "in", "is", "are", "of", "for", "grams", "gram", "g", "kg", "oz", "ounce", "ounces", "lb",
    "lbs", "cups", "cup", "ml", "litre", "litres", "per", "weight", "weigh", "weighs", "cost",
    "costs", "price", "prices", "each", "person", "people", "portion", "serving", "worth"))


_POUNDS_IS_MONEY = re.compile(
    r"(?:£\s*\d|\b\d+(?:\.\d+)?\s*(?:pounds?|quid|pence|p\b|gbp))"
    r"[^.?!]*?\b(?:a lot|lot for|expensive|cheap|cheaper|cheapest|dear|dearer|overpriced|"
    r"rip.?off|worth it|worth the|too much|reasonable|fair|good price|bad price|a rip|what price)",
    re.I)


def _asks_for_weight(clean):
    if _POUNDS_IS_MONEY.search(clean):
        return False
    if _WEIGH.search(clean):
        return True
    return bool(re.search(r"\b(?:grams?|g|kg|kilograms?|oz|ounces?|pounds?|lbs?)\b", clean))


def _names_unit(clean, unit):
    for _, items in UNITS.items():
        for name, words, _ in items:
            if name == unit and any(re.search(rf"\b{re.escape(word)}\b", clean)
                                    for word in words):
                return True
    return False


def _frac(clean):
    def unit_and_a_half(match):
        count = match.group("count") or "one"
        whole = _SAID_WHOLE.get(count) or int(count) if count.isdigit() else _SAID_WHOLE[count]
        return f"{whole + 0.5:g} {match.group('unit')}"

    clean = _UNIT_AND_A_HALF.sub(unit_and_a_half, clean)

    def mixed(match):
        value = _FRACTION.get((match.group(2), match.group(3)))
        if not value:
            return match.group(0)
        return f"{int(match.group(1)) + value:g}"

    clean = _MIXED.sub(mixed, clean)
    clean = _AND_A_HALF.sub(lambda m: f"{(_SAID_WHOLE.get(m.group(1)) or int(m.group(1))) + 0.5:g}",
                            clean)
    for word_fraction, value in _WORD_FRACTION:
        clean = word_fraction.sub(value, clean)

    def slash(match):
        value = _FRACTION.get((match.group(1), match.group(2)))
        return f"{value:.4f}".rstrip("0").rstrip(".") if value else match.group(0)

    return _SLASH.sub(slash, clean)


_HOW_TO = re.compile(r"(?:how\s+do\s+i|how\s+to|how\s+can\s+i|how\s+do\s+you|convert|"
                     r"change|work\s+out|turn)\b")


def _rule_sentence(family, from_unit, to_unit):
    source = _factor(family, from_unit)
    target = _factor(family, to_unit)
    if not source or not target or abs(source - target) < 1e-9:
        return None
    factor = source / target
    said_from = SAID.get(from_unit, from_unit)
    said_to = SAID.get(to_unit, to_unit)
    if factor >= 1:
        rule = f"multiply the {said_from} by {_fmt(factor)}"
    else:
        rule = f"divide the {said_from} by {_fmt(1 / factor)}"
    amount = 1
    for candidate in (1, 10, 100, 1000, 10000):
        amount = candidate
        if candidate * factor >= 1:
            break
    example = (f"{_fmt(amount)} {_say(amount, from_unit, one=amount == 1)} is "
               f"{_fmt(amount * factor)} {_say(amount * factor, to_unit)}")
    return f"To go from {said_from} to {said_to}, {rule}: {example}."


_BARE_JOIN = frozenset((
    "to", "in", "into", "as", "convert", "converting", "how", "do", "i", "many", "much", "is",
    "are", "there", "and", "the", "a", "an", "what", "s"))


def _is_bare_pair(clean, mentions):
    if len(mentions) < 2:
        return False
    rest = clean
    for start, end, _family, _unit in reversed(mentions):
        rest = rest[:start] + " " + rest[end:]
    rest = re.sub(r"\d+(?:\.\d+)?", " ", rest)
    words = re.findall(r"[a-z]+", rest)
    return bool(words) and all(word in _BARE_JOIN for word in words)


def _the_ounce_pair(family, unit, other_family, other_unit):
    if unit == "ounce" and other_family == "volume":
        return "volume", "fl oz", other_family, other_unit
    if other_unit == "ounce" and family == "volume":
        return family, unit, "volume", "fl oz"
    if unit == "fl oz" and other_family == "mass":
        return "mass", "ounce", other_family, other_unit
    if other_unit == "fl oz" and family == "mass":
        return family, unit, "mass", "ounce"
    return family, unit, other_family, other_unit


def _how_to_convert(clean, mentions):
    if not _HOW_TO.search(clean) and not _is_bare_pair(clean, mentions):
        return None
    if _NUMBER.search(clean) or any(_number_before(clean, start) is not None
                                    for start, _end, _f, _u in mentions):
        return None
    for position, (start, _end, family, unit) in enumerate(mentions):
        for other_start, _oend, other_family, other_unit in mentions[position + 1:]:
            family, unit, other_family, other_unit = _the_ounce_pair(
                family, unit, other_family, other_unit)
            if other_family != family or other_unit == unit:
                continue
            return _rule_sentence(family, unit, other_unit)
    return None


_ASKING_AFTER_MEASURE = re.compile(
    r"\b(should|shall|can|could|will|would|may|might|must|need|needs|needed|"
    r"do|does|did|don't|doesn't|didn't|have to|has to|had to|ought|supposed to|allowed|"
    r"is it|is that|are there|enough|normal|healthy|safe|too much|too many|until|till)\b")


def _tail_is_about_the_measure(tail):
    return not _ASKING_AFTER_MEASURE.search(tail.lower())



_SHARE = re.compile(
    r"\b(?P<word>three[\s-]quarters?|two[\s-]thirds?|one[\s-](?:third|quarter|half)|"
    r"a[\s-](?:third|quarter|half|fifth|sixth)|half|\d\s*/\s*\d)\s*(?:of\s+)?(?:an?\s+)?"
    r"(?P<unit>cups?|tablespoons?|tbsp|teaspoons?|tsp)\b")
_SHARE_VALUE = {"three quarters": 0.75, "three quarter": 0.75, "three-quarters": 0.75,
                "three-quarter": 0.75, "two thirds": 2 / 3, "two third": 2 / 3,
                "two-thirds": 2 / 3, "two-third": 2 / 3, "one third": 1 / 3,
                "one-third": 1 / 3, "one quarter": 0.25, "one-quarter": 0.25,
                "one half": 0.5, "one-half": 0.5, "a third": 1 / 3, "a-third": 1 / 3,
                "a quarter": 0.25, "a-quarter": 0.25, "a half": 0.5, "a-half": 0.5,
                "a fifth": 0.2, "a-fifth": 0.2, "a sixth": 1 / 6, "a-sixth": 1 / 6,
                "half": 0.5}
_SHARE_FRACTION = re.compile(
    r"\b(?:three[\s-]quarters?|two[\s-]thirds?|one[\s-](?:third|quarter|half)|"
    r"a[\s-](?:third|quarter|half|fifth|sixth)|half|\d\s*/\s*\d)\b")
_SHARE_SAID = {"three quarters": "three quarters", "three-quarter": "three quarters",
               "two thirds": "two thirds", "two-third": "two thirds", "one third": "a third",
               "one-quarter": "a quarter", "one half": "half", "half": "half"}
_SHARE_ASK = re.compile(r"\b(?:what\s+is|whats|what's|how\s+much\s+is|how\s+much|"
                        r"how\s+many|how\s+big\s+is)\b")
_NOT_ABOUT_A_MEASURE = re.compile(
    r"\bgrams?\b|\bg\b|\bml\b|\bmillilitres?\b|\bmilliliters?\b|\blitres?\b|\bliters?\b|"
    r"\bounces?\b|\boz\b|\bpounds?\b|\blbs?\b|\bpints?\b|\bquarts?\b|\bcelsius\b|"
    r"\bfahrenheit\b|\bdegrees?\b|\bcalories?\b")


def _share_value(word):
    if word in _SHARE_VALUE:
        return _SHARE_VALUE[word]
    slash = re.fullmatch(r"(\d)\s*/\s*(\d)", word)
    if slash and int(slash.group(2)):
        return int(slash.group(1)) / int(slash.group(2))
    return None


def _share_name(value):
    for known, name in ((0.25, "a quarter"), (0.5, "half"), (0.75, "three quarters"),
                        (1 / 3, "a third"), (2 / 3, "two thirds"), (0.2, "a fifth"),
                        (1 / 6, "a sixth"), (1 / 8, "an eighth"), (0.125, "an eighth")):
        if abs(value - known) < 0.001:
            return name
    return None


def _share_spoons(value, per):
    spoons = value * per
    whole = int(spoons)
    rest = round((spoons - whole) * 3)
    if rest >= 3:
        whole, rest = whole + 1, 0
    if not whole:
        return "a teaspoon" if rest == 1 else f"{rest} teaspoons"
    said = f"{whole} tablespoon" if whole == 1 else f"{whole} tablespoons"
    if not rest:
        return said
    return said + (" and a teaspoon" if rest == 1 else f" and {rest} teaspoons")


def _share_of_a_measure(clean, tail=True):
    if not _SHARE_ASK.search(clean) or _NOT_ABOUT_A_MEASURE.search(clean):
        return None
    match = _SHARE.search(clean)
    if not match:
        return None
    word = " ".join(match.group("word").split())
    value = _share_value(word)
    if not value:
        return None
    said = _share_name(value) or word
    before = _SHARE_FRACTION.findall(clean[:match.start()]) if \
        re.search(r"\bof\s*$", clean[:match.start()]) else []
    if before:
        outer_word = " ".join(before[-1].split())
        outer = _share_value(outer_word)
        if outer:
            value *= outer
            said = f"{_share_name(outer) or outer_word} of {said}"
    unit = match.group("unit")
    rest = (clean[:match.start()] + " " + clean[match.end():])
    if re.search(r"\b(?:cups?|tablespoons?|tbsp|teaspoons?|tsp)\b", rest):
        return None
    if unit.startswith(("cup",)):
        millilitres = round(value * 240)
        lead = "Half a cup" if said == "half" else f"{said[0].upper()}{said[1:]} of a cup"
        advice = ": spoons are the easy way to cut a cup down." if tail else "."
        return f"{lead} is {_share_spoons(value, 16)}, about {millilitres} ml{advice}"
    said = f"{said[0].upper()}{said[1:]}"
    if unit.startswith(("tablespoon", "tbsp")):
        millilitres = round(value * 15)
        return (f"{said} of a tablespoon is "
                f"{_tsp_phrase(value * 3)}, about {millilitres} ml.")
    millilitres = round(value * 5)
    return f"{said} of a teaspoon is about {millilitres} ml."


def _tsp_phrase(count):
    if abs(count - round(count)) < 0.05:
        whole = round(count)
        return f"{whole} teaspoons" if whole != 1 else "a teaspoon"
    return f"about {round(count, 1)} teaspoons"



_TIME_SMALLER = {"hour": (60, "minutes"), "minute": (60, "seconds"), "day": (24, "hours"),
                 "week": (7, "days")}
_TIME_ARTICLE = {"hour": "an hour", "minute": "a minute", "day": "a day", "week": "a week"}
_TIME_UNIT = {"hour": "hour", "hours": "hour", "hr": "hour", "hrs": "hour",
              "second": "second", "seconds": "second", "sec": "second", "secs": "second",
              "minute": "minute", "minutes": "minute", "min": "minute", "mins": "minute",
              "day": "day", "days": "day", "week": "week", "weeks": "week"}
_NUMERAL = {"a": 1, "an": 1, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
            "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
            "fifteen": 15, "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50}
_DENOMINATOR = {"half": 2, "halves": 2, "third": 3, "thirds": 3, "quarter": 4, "quarters": 4,
                "fifth": 5, "fifths": 5, "sixth": 6, "sixths": 6, "eighth": 8, "eighths": 8,
                "tenth": 10, "tenths": 10, "twelfth": 12, "twelfths": 12, "twentieth": 20,
                "twentieths": 20, "twenty-fourth": 24, "twenty-fourths": 24}
_A_FRACTION = (r"(?:(?:a|an|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|\d+)"
               r"[\s-]+(?:halves?|thirds?|quarters?|fifths?|sixths?|eighths?|tenths?|twelfths?"
               r"|twentieths?|twenty[\s-]fourths?)"
               r"|half|\d+\s*/\s*\d+|\d*\.\d+)")
_A_TIME_SHARE = re.compile(
    r"(?<![\w.])(?P<word>" + _A_FRACTION + r")\s*(?:of\s+)?(?:an?\s+|one\s+)?"
    r"(?P<unit>hours?|hrs?|minutes?|mins?|days?|weeks?)\b")
_A_MIXED_SPAN = re.compile(
    r"\b(?P<whole>a|an|one|two|three|four|five|six|seven|eight|nine|ten|\d+(?:\.\d+)?)\s+"
    r"(?P<unit>hours?|hrs?|days?|weeks?)\s+(?:and\s+)?"
    r"(?P<rest>a\s+half|half|(?P<n>\d+|one|two|three|four|five|six|seven|eight|nine|ten|"
    r"fifteen|twenty|thirty|forty|forty five|fifty)\s+(?P<small>minutes?|mins?))\b")
_A_FRACTION_OF_A_MIXED = re.compile(
    r"(?<![\w.])(?P<word>" + _A_FRACTION + r")\s*(?:of|out\s+of)\s+(?P<span>.+)$")
_A_HALF_SPAN = re.compile(
    r"\b(?P<whole>a|an|one|two|three|four|five|\d+)\s+and\s+a\s+half\s+"
    r"(?P<unit>hours?|hrs?|days?)\b")
_A_FRACTION_OF = re.compile(
    r"\b(?:what|which|how\s+much)\s+(?:a\s+)?fraction\s+of\s+(?:an?\s+|one\s+)?"
    r"(?P<unit>hour|day|week|minute)\s+(?:is|of)\s+"
    r"(?P<amount>\d+(?:\.\d+)?|a|an|one)\s*(?P<small>minutes?|mins?|hours?|hrs?|"
    r"seconds?|secs?|days?)\b")
_A_FRACTION_AS = re.compile(
    r"\b(?P<amount>\d+(?:\.\d+)?|a|an|one)\s*"
    r"(?P<small>minutes?|mins?|hours?|hrs?|seconds?|secs?|days?)\s+(?:as\s+)?(?:a\s+)?"
    r"fraction\s+of\s+(?:an?\s+|one\s+)?(?P<unit>hour|day|week|minute)\b")
_A_SPAN_ASK = re.compile(r"\b(?:what\s+is|whats|what's|how\s+much|how\s+many|how\s+long|"
                         r"how\s+big)\b")
_A_FRACTION_ASK = re.compile(r"\b(?:what(?:s|'s)?|which|how\s+much|how\s+many)\b")
_A_TARGET_UNIT = re.compile(
    r"\b(?:in|to|into)\s+(?:minutes?|mins?|seconds?|secs?|hours?|hrs?|days?|weeks?)\b")
_A_UNIT_ASKED = re.compile(
    r"\b(?:how\s+many|how\s+much|in|to|into)\s+(?:a\s+|an\s+|one\s+)?"
    r"(minutes?|mins?|seconds?|secs?|hours?|hrs?|days?|weeks?)\b")
_TIME_SECONDS = {"second": 1, "minute": 60, "hour": 3600, "day": 86400, "week": 604800}
_TIME_PLURAL = {"second": "seconds", "minute": "minutes", "hour": "hours", "day": "days",
                "week": "weeks"}


def _a_fraction_value(word):
    word = " ".join(str(word).replace("-", " ").split()).lower()
    slash = re.fullmatch(r"(\d+)\s*/\s*(\d+)", word.replace(" ", ""))
    if slash and int(slash.group(2)):
        value = int(slash.group(1)) / int(slash.group(2))
        return value if value < 1 else None
    if re.fullmatch(r"\d*\.\d+", word):
        value = float(word)
        return value if value < 1 else None
    parts = word.split()
    if parts == ["half"]:
        return 0.5
    if len(parts) == 2:
        numeral = _NUMERAL.get(parts[0])
        if numeral is None and parts[0].isdigit():
            numeral = int(parts[0])
        denominator = _DENOMINATOR.get(parts[1])
        if numeral and denominator:
            value = numeral / denominator
            return value if value < 1 else None
    return None


def _a_fraction_name(value):
    name = _share_name(value)
    if name:
        return name
    for numerator, denominator, said in ((1, 7, "a seventh"), (1, 9, "a ninth"),
                                         (2, 7, "two sevenths"), (1, 10, "a tenth"),
                                         (1, 12, "a twelfth"), (1, 24, "a twenty-fourth"),
                                         (5, 6, "five sixths"),
                                         (5, 8, "five eighths"), (3, 8, "three eighths"),
                                         (7, 8, "seven eighths"), (1, 20, "a twentieth")):
        if abs(value - numerator / denominator) < 0.001:
            return said
    return None


def _a_span_amount(amount, name):
    if abs(amount - round(amount)) < 0.0001:
        whole = int(round(amount))
        return f"{whole:,} {name}" if whole != 1 else f"one {name[:-1]}"
    if abs((amount % 1) - 0.5) < 0.0001:
        return f"{int(amount)} and a half {name}"
    return f"{amount:g} {name}"


def _a_number_word(number):
    words = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven",
             8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve"}
    return words.get(int(number), f"{int(number)}")


def _a_share_of_a_unit(value, unit):
    article = _TIME_ARTICLE[unit]
    plural = article.split()[-1] + "s"
    if abs(value - 0.5) < 0.0001:
        return f"Half {article}"
    if value > 1 - 0.0001:
        whole = int(value)
        rest = round(value - whole, 4)
        if abs(rest) < 0.0001:
            if whole == 1:
                return article[0].upper() + article[1:]
            return f"{_a_number_word(whole)} {plural}"
        if abs(rest - 0.5) < 0.0001:
            if whole == 1:
                return f"{article[0].upper()}{article[1:]} and a half"
            return f"{_a_number_word(whole)} and a half {plural}"
        if whole == 1:
            rest_name = _a_fraction_name(rest) or f"{rest:g}"
            return f"{article[0].upper()}{article[1:]} and {rest_name}"
        return f"{_a_number_word(whole)} {plural} and {_a_share_of_a_unit(rest, unit).lower()}"
    name = _a_fraction_name(value) or f"{value:g}"
    if name.startswith("a "):
        return f"A {name[2:]} of {article}"
    if name.startswith("an "):
        return f"An {name[3:]} of {article}"
    return f"{name[0].upper()}{name[1:]} of {article}"


def _a_fraction_of_a_time_unit(clean):
    for pattern in (_A_FRACTION_OF, _A_FRACTION_AS):
        match = pattern.search(clean)
        if not match:
            continue
        unit = match.group("unit")
        small = _TIME_UNIT.get(match.group("small"))
        amount = match.group("amount")
        count = _NUMERAL.get(amount)
        if count is None and re.fullmatch(r"\d+(?:\.\d+)?", amount):
            count = float(amount)
        per_small = {"hour": {"minute": 60}, "day": {"hour": 24}, "week": {"day": 7},
                     "minute": {"second": 60}}.get(unit, {}).get(small)
        if not count or not per_small:
            continue
        plural = {"minute": "minutes", "hour": "hours", "second": "seconds",
                  "day": "days"}[small]
        said = _a_span_amount(count, plural)
        name = _a_fraction_name(count / per_small)
        if not name:
            percent = round(100 * count / per_small)
            return f"{said[0].upper()}{said[1:]} is about {percent}% of {_TIME_ARTICLE[unit]}."
        return f"{said[0].upper()}{said[1:]} is {name} of {_TIME_ARTICLE[unit]}."
    return None


_A_WHOLE_UNIT = re.compile(
    r"^\s*(?:how\s+long\s+is|how\s+long's|what\s+is|what's|whats)\s+"
    r"(?:an?|one|1)\s+(?P<unit>hours?|days?|weeks?|minutes?)\s*$")


def _the_span_said(span_seconds, unit, clean):
    factor, name = _TIME_SMALLER[unit]
    asked = _A_UNIT_ASKED.search(clean)
    if asked:
        wanted = _TIME_UNIT.get(asked.group(1))
        if wanted and _TIME_SECONDS[wanted] < _TIME_SECONDS[unit]:
            return _a_span_amount(span_seconds / _TIME_SECONDS[wanted], _TIME_PLURAL[wanted])
    return _a_span_amount(span_seconds / (_TIME_SECONDS[unit] / factor), name)


def _a_mixed_parts(match):
    unit = _TIME_UNIT[match.group("unit")]
    whole = _NUMERAL.get(match.group("whole"))
    if whole is None:
        whole = float(match.group("whole"))
    if "rest" not in match.groupdict() or match.group("rest").strip() in ("a half", "half"):
        return unit, whole, 0.5
    said_n = _NUMERAL.get(match.group("n"))
    return unit, whole, (said_n if said_n is not None else float(match.group("n"))) / 60


def _a_span_of_time(clean):
    if not isinstance(clean, str) or not clean or len(clean) > 200:
        return None
    asks = _A_SPAN_ASK.search(clean)
    target = _A_TARGET_UNIT.search(clean)
    if (not asks and not target and not _A_FRACTION_ASK.search(clean)
            and not _A_FRACTION_AS.search(clean)):
        return None
    if re.search(r"\bfractions?\b", clean):
        said = _a_fraction_of_a_time_unit(clean)
        if said:
            return said
    share = _A_FRACTION_OF_A_MIXED.search(clean)
    if share:
        late = _A_MIXED_SPAN.search(share.group("span")) or _A_HALF_SPAN.search(share.group("span"))
        value = _a_fraction_value(share.group("word"))
        if late and value:
            late_unit, late_whole, late_extra = _a_mixed_parts(late)
            part = (late_whole + late_extra) * value
            return (f"{_a_share_of_a_unit(part, late_unit)} is "
                    f"{_the_span_said(part * _TIME_SECONDS[late_unit], late_unit, clean)}.")
    mixed = _A_MIXED_SPAN.search(clean)
    half_first = _A_HALF_SPAN.search(clean) if not mixed else None
    if mixed or half_first:
        unit, whole, extra = _a_mixed_parts(mixed or half_first)
        if abs(extra - 0.5) < 0.0001:
            said = _a_share_of_a_unit(whole + 0.5, unit)
        else:
            plural = _TIME_ARTICLE[unit].split()[-1] + "s"
            head = (_TIME_ARTICLE[unit][0].upper() + _TIME_ARTICLE[unit][1:] if whole == 1
                    else f"{_a_number_word(whole)} {plural}")
            said = f"{head} and {_a_span_amount(extra * 60, 'minutes')}"
        said = said[0].upper() + said[1:]
        return f"{said} is {_the_span_said((whole + extra) * _TIME_SECONDS[unit], unit, clean)}."
    if target:
        return None
    if not asks:
        return None
    whole = _A_WHOLE_UNIT.match(clean)
    if whole:
        unit = _TIME_UNIT[whole.group("unit")]
        return f"{_a_share_of_a_unit(1, unit)} is {_the_span_said(_TIME_SECONDS[unit], unit, clean)}."
    match = _A_TIME_SHARE.search(clean)
    if not match:
        return None
    unit = _TIME_UNIT[match.group("unit")]
    value = _a_fraction_value(match.group("word"))
    if not value:
        return None
    if re.match(r"\s*and\s+a\s+half\b", clean[match.end():match.end() + 14]):
        value += 0.5
    return (f"{_a_share_of_a_unit(value, unit)} is "
            f"{_the_span_said(value * _TIME_SECONDS[unit], unit, clean)}.")


_SHARE_THAT = re.compile(
    r"\b(?P<word>three[\s-]quarters?|two[\s-]thirds?|one[\s-](?:third|quarter|half)|"
    r"a[\s-](?:third|quarter|half|fifth|sixth)|half)\s+(?:of\s+)?(?:that|it|the same)\b")
_SHARE_LEAD = re.compile(r"^(?:and|so|then|ok|okay|what|how|about|much|is|whats|what's)\b")


def _share_carried(clean, memory):
    match = _SHARE_THAT.search(clean)
    if not match:
        return None
    rest = clean[:match.start()] + " " + clean[match.end():]
    rest = rest.strip(" ?.!,andso")
    while _SHARE_LEAD.match(rest):
        rest = _SHARE_LEAD.sub("", rest).strip(" ?.!,andso")
    if rest:
        return None
    for turn in reversed(list((memory or {}).get("turns") or [])[-4:]):
        line = str(turn.get("user") or "").strip().lower()
        share = _SHARE.search(line)
        if not share:
            if line:
                return None
            continue
        said = " ".join(match.group("word").split())
        return _share_of_a_measure("what is " + said + " of " + line[share.start():], tail=False)
    return None


def convert(clean, memory=None):
    reply = _answer(clean, memory)
    if reply:
        return reply
    if memory:
        return (_share_carried(clean, memory) or _carried_weight(clean, memory)
                or _carried_measure(clean, memory)
                or _carried_people(clean, memory))
    return None


_WEIGHT_SAID = re.compile(r"\b(\d+(?:\.\d+)?)\s*(kg|kilo|kilos|kilogram|kilograms|g|gram|"
                          r"grams|gramme|grammes)\b")
_PORTIONS_ASK = re.compile(
    r"\bportions?\b|\bservings?\b|\bserves?\b|\bfeed(?:s|ing)?\b|\benough for\b|"
    r"\bi need\b|\bi've got\b|\bi have\b(?!\s+to\b)|\bi bought\b|\bhow many\b|\bfor how many\b")


_A_COUNT = re.compile(r"\b(\d+)\s+(?:\w+\s+){0,2}?"
                      r"(?P<food>[a-z][a-z' ]*)\b")


def _count_in_a_line(clean):
    if not _PORTIONS_ASK.search(clean):
        return None
    best = None
    for names, amount, kind, noun in PER_PERSON:
        if kind != "each" or not amount:
            continue
        for name in names:
            found = re.search(rf"\b(\d+)\s+(?:[a-z]+\s+)?{re.escape(name)}(?![\w])", clean)
            if found and (best is None or len(name) > len(best[0])):
                best = (name, int(found.group(1)), amount, noun)
    if not best:
        return None
    _name, count, amount, noun = best
    if count <= 0 or count > 200:
        return None
    portions = count / amount
    halves = round(portions * 2) / 2
    piece = noun if noun.endswith("s") or " " in noun else noun + "s"
    each = "one" if amount == 1 else f"{amount:g}"
    if halves <= 1:
        return (f"{count} {piece} is about one portion: {each} a person is the usual "
                f"allowance.")
    return (f"{count} {piece} is about {halves:g} portions: {each} a person is the usual "
            f"allowance.")


def _portions_in_a_weight(clean):
    if not isinstance(clean, str) or not clean:
        return None
    match = _WEIGHT_SAID.search(clean)
    if not match:
        counted = _count_in_a_line(clean)
        if counted:
            return counted
    if match:
        grams = float(match.group(1))
        unit = match.group(2).lower()
    else:
        bare = re.search(r"\b(half\s+)?(?:a|an|one)?\s*(kg|kilo|kilos|kilogram|kilograms|"
                         r"gram|grams|gramme|grammes)\b", clean)
        if not bare:
            return None
        grams = 0.5 if bare.group(1) else 1.0
        unit = bare.group(2).lower()
    if unit.startswith(("k", "kilo")):
        grams *= 1000
    if grams < 20 or grams > 20000:
        return None
    if not _PORTIONS_ASK.search(clean):
        return None
    if _PORTION_WORD.search(clean) and _PEOPLE_WORD.search(clean):
        return None
    best = None
    for names, amount, kind, noun in PER_PERSON:
        if kind != "g" or not amount:
            continue
        for name in names:
            if re.search(rf"(?<![\w.]){re.escape(name)}(?![\w])", clean):
                if best is None or len(name) > len(best[0]):
                    best = (name, amount, noun)
    if not best:
        return None
    _name, amount, noun = best
    weight = f"{grams / 1000:g} kg" \
        if unit.startswith(("k", "kilo")) and grams >= 1000 else f"{grams:g} g"
    portions = grams / amount
    if portions < 0.75:
        return (f"{weight} of {noun} is not a full portion on its own: allow about "
                f"{amount:g} g a person.")
    halves = round(portions * 2) / 2
    said = f"{halves:g}".replace(".5", " and a half")
    if halves <= 1:
        return (f"{weight} of {noun} is about one portion: the usual allowance is "
                f"{amount:g} g a person.")
    return (f"{weight} of {noun} is about {said} portions: the usual allowance is "
            f"{amount:g} g a person, so it feeds {said}.")


WHOLE_THING_SERVES = (
    (("chicken", "chickens"), "about 1.8 to 2kg", 4, 6,
     "two 1.5 to 1.8kg birds rather than one big one: they cook evenly and fit a normal tin",
     500, "500g a person on the bone", ", and the picked frame gives another two meals' worth"),
    (("duck", "ducks"), "about 2kg", 4, None, "two birds", 500, "500g a person on the bone", ""),
    (("leg of lamb", "lamb leg", "leg of mutton"), "about 2kg", 6, 8,
     "a leg and a shoulder", 300, "300g a person on the bone", ""),
    (("shoulder of lamb", "lamb shoulder"), "about 1.75kg", 6, 8,
     "a shoulder and a leg", 250, "250g a person on the bone", ""),
    (("gammon joint", "ham joint", "gammon", "whole ham"), "about 1.5kg", 8, 10,
     "two 1kg joints, or a bigger one for sandwiches after", 200, "200g a person",
     ", and the end of it sandwiches the week"),
    (("whole salmon", "side of salmon"), "about 1.5kg", 8, None,
     "two sides, or a side and a couple of fillets", 180, "180g a person", ""),
)
_A_CUT_NOT_A_BIRD = re.compile(
    r"\b(?:breasts?|thighs?|wings?|drumsticks?|fillets?|nuggets?|strips?|tenders?|mince|"
    r"sausages?|joints?\s+of\s+meat|chops?|steaks?)\b")
_FEEDS_ASK = re.compile(
    r"\benough\b|\bfeed(?:s|ing)?\b|\bserves?\b|\bgo(?:es)?\s+round\b|\bhow\s+far\b|"
    r"\bdo\s+for\b|\bhow\s+many\s+(?:people|persons?|of\s+us|adults?|guests?)\b")
_NOT_A_TABLE_QUESTION = re.compile(
    r"\b(?:how long|how do i|how to|temperature|oven|roast it|bake|reheat|fridge|freezer|"
    r"freeze|keep|keeps|lasts?|calories|kcal|protein|carbs?|fat|healthy|cost|costs|price|"
    r"cheap|expensive|buy|shopping|shopping list|defrost|thaw|stuffing|recipe|meals?)\b")
_KEEPING_HENS = re.compile(
    r"\b(?:hens?|coop|run|pellets|layers?|laying|eggs?|broody|cockerel|chicks?|"
    r"feed my|keeping chickens?)\b")
_WHOLE_WEIGHT = re.compile(r"\b(\d+(?:\.\d+)?)\s*(kg|kilo|kilos|kilogram|kilograms)\b")


_PLURAL_BIRDS = "|".join(
    name for names, *_rest in WHOLE_THING_SERVES for name in names if name.endswith("s"))
_PEOPLE_WORD_TO_TWENTY = {13: "thirteen", 14: "fourteen", 15: "fifteen", 16: "sixteen",
                          17: "seventeen", 18: "eighteen", 19: "nineteen", 20: "twenty"}


def _a_table_word(count):
    return _SAID_PEOPLE.get(count) or _PEOPLE_WORD_TO_TWENTY.get(count) or str(count)


_COUNT_OF_BIRDS = re.compile(
    r"\b(how many|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|\d{1,2})\s+"
    r"(?:whole\s+)?(" + _PLURAL_BIRDS + r")\b")


def _birds_for_a_table(clean):
    if not isinstance(clean, str) or not clean or len(clean) > 200:
        return None
    found = _COUNT_OF_BIRDS.search(clean)
    if not found:
        return None
    if _NOT_A_TABLE_QUESTION.search(clean) or _KEEPING_HENS.search(clean):
        return None
    wanted = _people_asked(clean)
    if wanted is None:
        return None
    word, name = found.group(1), found.group(2)
    for names, size, feeds, stretch, more, grams_each, allowance, keeps in WHOLE_THING_SERVES:
        if name in names:
            break
    else:
        return None
    meat = names[0]
    one = grams_each * feeds
    said = _a_table_word(wanted)
    needs = -(-wanted * grams_each // one)
    if word == "how many":
        kilos = wanted * grams_each / 1000.0
        if needs == 1:
            return (f"For {said} people you want about {kilos:g}kg of {meat} on the bone, and one "
                    f"bird of {size} is enough.")
        return (f"For {said} people you want about {kilos:g}kg of {meat} on the bone: "
                f"{_a_table_word(needs)} birds of {size} each.")
    have = _people_in_a_count(word)
    if not have or have < 2:
        return None
    feeds_had = int(have * one // grams_each)
    many = _a_table_word(have)
    had = "is" if have == 1 else "are"
    kilos = have * one / 1000.0
    if feeds_had == wanted:
        return (f"{many.capitalize()} {name} {had} about {kilos:g}kg on the bone, which is exactly "
                f"enough for {said}.")
    if feeds_had > wanted:
        return (f"{many.capitalize()} {name} {had} about {kilos:g}kg on the bone, enough for "
                f"{_SAID_PEOPLE.get(feeds_had, str(feeds_had))} - so yes for {said}.")
    return (f"{many.capitalize()} {name} feed about "
            f"{_SAID_PEOPLE.get(feeds_had, str(feeds_had))}, so {said} wants "
            f"{_SAID_PEOPLE.get(needs, str(needs))} birds.")


def _people_in_a_count(word):
    if not word:
        return None
    if word.isdigit():
        return int(word)
    return _PEOPLE_VALUE.get(word)


def _a_whole_thing_feeds(clean, memory=None):
    if not isinstance(clean, str) or not clean or len(clean) > 200:
        return None
    if not _FEEDS_ASK.search(clean):
        return None
    if _NOT_A_TABLE_QUESTION.search(clean) or _KEEPING_HENS.search(clean):
        return None
    if _A_CUT_NOT_A_BIRD.search(clean):
        return None
    best = None
    for names, size, feeds, stretch, more, grams_each, allowance, keeps in WHOLE_THING_SERVES:
        for name in names:
            found = re.search(
                r"\b(?:one|1|a|an|the|single)\s+(?:whole\s+)?(?:\d+(?:\.\d+)?\s*kg\s+)?"
                + re.escape(name) + r"\b"
                r"|\bwhole\s+(?:\d+(?:\.\d+)?\s*kg\s+)?" + re.escape(name) + r"\b", clean)
            if found and (best is None or len(name) > len(best[0])):
                best = (name, size, feeds, stretch, more, grams_each, allowance, keeps)
    if not best:
        return None
    name, size, feeds, stretch, more, grams_each, allowance, keeps = best
    noun = "an " + name if name[0] in "aeiou" else "a " + name
    weighed = _WHOLE_WEIGHT.search(clean)
    if weighed:
        kilos = float(weighed.group(1))
        grams = kilos * 1000
        feeds = max(1, round(grams / grams_each))
        size = f"{kilos:g}kg"
        stretch = round(feeds * 1.5) if stretch else None
    smaller = _SAID_PEOPLE.get(feeds, str(feeds))
    wanted = _people_asked(clean)
    if wanted is None:
        found = re.search(r"\b(?:feed|feeds|serve|serves|enough for)\s+(\d{1,2}|one|two|three|"
                          r"four|five|six|seven|eight|nine|ten|eleven|twelve)\b", clean)
        wanted = _people_in_a_count(found.group(1)) if found else None
    if wanted is None:
        stretched = f", {_SAID_PEOPLE.get(stretch, str(stretch))} at a stretch with plenty of " \
                   "sides" if stretch else ""
        return (f"One {name}, {size}, feeds {smaller} people{stretched}{keeps}. "
                f"A bigger table is {more}.")
    said = _SAID_PEOPLE.get(wanted, str(wanted))
    if wanted <= feeds:
        return (f"One {name}, {size}, feeds {smaller} people as a roast - so one is enough for "
                f"{said}. Allow {allowance} if you are buying another.")
    if stretch and wanted <= stretch:
        reached = _SAID_PEOPLE.get(stretch, str(stretch))
        return (f"One {name}, {size}, feeds {smaller} comfortably and {reached} at a stretch "
                f"with plenty of sides - so one is enough for {said} if you lay on the sides. "
                f"Otherwise {more}.")
    return (f"One {name}, {size}, feeds {smaller}, so for {said} you want {more}. "
            f"That is the {allowance} figure.")


def _answer(clean, memory=None):
    if not isinstance(clean, str) or not clean or len(clean) > 200:
        return None
    whole = _a_whole_thing_feeds(clean, memory) or _birds_for_a_table(clean)
    if whole:
        return whole
    measured = _the_thing_measured_by_itself(clean)
    if measured:
        return _answer(measured, memory)
    if _COMPONENT.search(clean) and not _the_component_is_the_whole_measure(clean):
        return None
    share = _share_of_a_measure(clean)
    if share:
        return share
    span = _a_span_of_time(clean)
    if span:
        return span
    portions = _portions_in_a_weight(clean)
    if portions:
        return portions
    temperature = _oven(clean) or _temperature(clean) or _temperature_rule(clean)
    if temperature:
        return temperature
    butter = _butter(clean)
    if butter:
        return butter
    if _PEOPLE_COUNT.search(clean) or _PEOPLE_WORD.search(clean):
        dish = _a_dish_for_a_table(clean)
        if dish:
            return dish
        portion = _per_person(clean, memory)
        if portion:
            return portion
    pack = _pack(clean)
    if pack:
        return pack
    counted = _pack_count(clean)
    if counted:
        return counted
    loose = _loose(clean)
    if loose:
        return loose
    weight = _object_weight(clean)
    if weight:
        return weight
    piece = _piece_weight(clean)
    if piece:
        return piece
    liquid = _liquid_weight(clean)
    if liquid:
        return liquid
    portion = _per_person(clean, memory)
    if portion:
        return portion
    clean = _SAY_K.sub(r"\1 km", clean)
    clean = _frac(clean)
    clean = _JOINED.sub(" ", clean)
    handful = _handful(clean)
    if handful:
        return handful
    own = _own_height(clean)
    if own:
        return own
    mentions = _mentions(clean)
    if not mentions:
        return None
    rule = _how_to_convert(clean, mentions)
    if rule:
        return rule
    height = _height(clean, mentions)
    if height:
        return height
    land = _land_size(clean, mentions)
    if land:
        return land

    measured = []
    for start, end, family, unit in mentions:
        value = _number_before(clean, start)
        if value is not None:
            measured.append((value, family, unit, end))

    weighed = _named_ingredient(clean, mentions, measured)
    if weighed:
        return weighed

    for value, family, unit, end in measured:
        rest = clean[end:]
        for match in _UNIT_WORD.finditer(rest):
            text = match.group(0)
            before = rest[:match.start()]
            if text == "in" or not (_TARGET.search(before)
                                    or re.search(r"how (?:many|much)\s+$", before)):
                continue
            family, unit, to_family, to_unit = _the_ounce_pair(
                family, unit, *_NAMES[text])
            if to_family != family or to_unit == unit:
                continue
            if _UNIT_WORD.search(rest[match.end():]):
                break
            return _sentence(value, family, unit, to_unit)

    wanted_match = re.search(r"how (?:many|much)\s+(?P<want>[a-z/'’ ]+?)\s+"
                             r"(?:are there\s+)?(?:in|to|into|is|as)\s+(?P<rest>.+)$", clean)
    if wanted_match:
        want = _named_unit(wanted_match.group("want"))
        source = next(((value, family, unit, end) for value, family, unit, end in measured
                       if end > wanted_match.start("rest")), None)
        if source and not _tail_is_about_the_measure(clean[source[3]:]):
            source = None
        if want and source:
            want_family, want_unit, source_family, source_unit = _the_ounce_pair(
                want[0], want[1], source[1], source[2])
            want = (want_family, want_unit)
            source = (source[0], source_family, source_unit, source[3])
        if want and source and want[0] == source[1] and want[1] != source[2]:
            if source[1] == "mass" and source[2] in ("cup", "tbsp", "tsp"):
                return _cup_of_something(clean)
            return _sentence(source[0], source[1], source[2], want[1], in_phrase=True)
        if want and source and want[1] in ("cup", "tbsp", "tsp", "dessertspoon") \
                and source[1] == "volume":
            return _cup_of_something(clean)
    if re.search(r"\b(cups?|mugs?|tablespoons?|tbsp|teaspoons?|tsp|"
                 r"dessertspoons?|dsp)\b", clean):
        return _cup_of_something(clean)
    return None


_TRAILING_JOIN = re.compile(r"\s+(?:then|please)\s*$")
_CARRIED_LEAD = re.compile(
    r"^(?:and\s+(?:then\s+|what\s+about\s+|how\s+about\s+)?|what\s+about\s+|"
    r"how\s+about\s+|or\s+|then\s+|also\s+|how\s+much\s+|how\s+many\s+)")
_ASKED_MEASURE = re.compile(r"how\s+(?:many|much)\s+(?P<want>[a-z]+)")
_CARRIED_FILLER = frozenset((
    "in", "to", "of", "a", "an", "the", "one", "and", "so", "what", "about", "how", "many",
    "much", "then", "big", "size", "is", "that", "it", "same", "for", "per", "please", "s",
    "gram", "grams", "g", "ml", "mls", "litre", "litres", "ounce", "ounces", "oz", "pound",
    "pounds", "lb", "lbs", "kilo", "kilos", "kilogram", "kilograms", "kg", "cup", "cups",
    "mug", "mugs", "tablespoon", "tablespoons", "tbsp", "teaspoon", "teaspoons", "tsp",
    "dessertspoon", "dessertspoons", "dsp", "pint", "pints", "fl", "fluid"))


def _unit_words(text):
    return [(match.group(0), _NAMES[match.group(0)])
            for match in _UNIT_WORD.finditer(text)]


def _bare_measure(text):
    text = _CARRIED_LEAD.sub("", str(text or "").strip().lower()).strip(" ?.!,")
    if not text or re.search(r"\d", text):
        return None
    said = _unit_words(text)
    if not said:
        return None
    spare = set(text.replace(",", " ").split())
    spare -= _CARRIED_FILLER
    for word, _ in said:
        spare -= set(word.split())
    food = _food_named(text)
    if food:
        spare -= set(food[0].split())
    if spare:
        return None
    return said, food


def _previous_measure(memory):
    for turn in reversed(list((memory or {}).get("turns") or [])[-4:]):
        line = str(turn.get("user") or "").strip().lower()
        if not line:
            return None
        if _answer(line):
            return line
        if _bare_measure(line) is None:
            return None
    return None


_CARRIED_PEOPLE = re.compile(
    r"^(?:for\s+)?(?P<count>\d{1,3}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|"
    r"twelve)(?:\s+(?:people|persons?|guests|adults|heads|of\s+us))?$")


_CORRECTION = re.compile(r"\b(?:i meant|i mean|sorry|actually|no wait|make that|"
                         r"on second thoughts|i said|not\s+\d)")


def _previous_portion(memory):
    for turn in reversed(list((memory or {}).get("turns") or [])[-3:]):
        line = str(turn.get("user") or "").strip().lower()
        if not line:
            return None
        if _PEOPLE_COUNT.search(line) and _per_person(line):
            return line
        if _bare_measure(line) is None:
            return None
    return None


def _carried_people(clean, memory):
    text = str(clean or "").strip().lower()
    if _CARRIED_NOW.match(text.strip(" ?.!,")):
        return _portion_after_correction(memory)
    for _ in range(3):
        stripped = _TRAILING_JOIN.sub("", _CARRIED_LEAD.sub("", text)).strip(" ?.!,")
        if stripped == text.strip(" ?.!,"):
            break
        text = stripped
    text = text.strip(" ?.!,")
    match = _CARRIED_PEOPLE.match(text)
    if not match:
        return None
    previous = _previous_portion(memory)
    if not previous:
        return None
    found = _PEOPLE_COUNT.search(previous)
    if not found:
        return None
    old = next((group for group in found.groups() if group), None)
    if old is None:
        return None
    rebuilt = previous[:found.start()] + found.group(0).replace(old, match.group("count"), 1) \
        + previous[found.end():]
    return _answer(rebuilt)


_NEW_WEIGHT_THEN = re.compile(
    r"^(?:and\s+|ok\s+|okay\s+|so\s+|but\s+)?(?:(?:can|could)\s+you\s+)?"
    r"(?:(?:make|change|do|set|use)\s+(?:it|that|them|this)\s+(?:to\s+|at\s+|as\s+)?"
    r"|what\s+about\s+|how\s+about\s+|and\s+)?"
    r"(?P<amount>(?:\d+(?:\.\d+)?)\s*(?:kg|kilo|kilos|kilogram|kilograms|g|gram|grams|"
    r"gramme|grammes)|half\s+a\s+(?:kilo|kg)|a\s+(?:kilo|kg)|one\s+(?:kilo|kg))"
    r"(?:\s+(?:instead|then|please|now|of\s+that))?$")


def _carried_weight(clean, memory):
    text = " ".join(str(clean or "").lower().split()).strip(" ?.!,")
    match = _NEW_WEIGHT_THEN.match(text)
    if not match:
        return None
    previous = _previous_portion(memory)
    if not previous:
        return None
    found = re.search(r"\b(\d+(?:\.\d+)?)\s*(kg|kilo|kilos|kilogram|kilograms|g|gram|grams|"
                      r"gramme|grammes)\b", match.group("amount"))
    if found:
        grams = float(found.group(1))
        unit = found.group(2)
        if unit.startswith(("k", "kilo")):
            grams *= 1000
    else:
        grams = 500.0 if match.group("amount").startswith("half") else 1000.0
    best = None
    for names, amount, kind, noun in PER_PERSON + PER_PERSON_WHEN_COUNTED:
        if kind != "g" or not amount:
            continue
        for name in names:
            if re.search(rf"(?<![\w.]){re.escape(name)}(?![\w])", previous):
                if best is None or len(name) > len(best[0]):
                    best = (name, amount, noun)
    if not best:
        return None
    _name, amount, noun = best
    weight = f"{grams:g} g" if grams < 1000 or "kg" not in match.group("amount") \
        else f"{grams / 1000:g} kg"
    portions = grams / amount
    people = _people_asked(previous)
    halves = round(portions * 2) / 2
    said = f"{halves:g}".replace(".5", " and a half")
    if people and abs(halves - people) < 0.75:
        return (f"{weight} of {noun} is about right for {people}: the usual allowance is "
                f"{amount:g} g a person.")
    if people:
        side = "a little more" if halves > people else "a little less"
        return (f"{weight} of {noun} is about {said} portions, {side} than the {people} you "
                f"asked about: the usual allowance is {amount:g} g a person.")
    if halves <= 1:
        return f"{weight} of {noun} is about one portion: the usual allowance is {amount:g} g a person."
    return (f"{weight} of {noun} is about {said} portions: the usual allowance is "
            f"{amount:g} g a person, so it feeds {said}.")
_CARRIED_NOW = re.compile(
    r"^(?:so |ok |okay |and |but |then )*(?:how much|how many|what about|and)"
    r"(?: of (?:it|that|them|those|these))?(?: now| then| again)?$")


def _names_a_portion_food(line):
    for names, _amount, _kind, _noun in PER_PERSON + PER_PERSON_WHEN_COUNTED:
        for name in names:
            if re.search(rf"(?<![\w.]){re.escape(name)}(?![\w])", line):
                return True
    return False


def _portion_after_correction(memory):
    portion = None
    count = None
    for turn in reversed(list((memory or {}).get("turns") or [])[-4:]):
        line = " ".join(str(turn.get("user") or "").lower().split())
        if not line:
            break
        if portion is None and _AN_ASK.search(line) and _names_a_portion_food(line):
            portion = line
            break
        if portion is None and _CORRECTION.search(line):
            found = _people_asked(line)
            if found is not None:
                count = found
                continue
        break
    if portion is None or count is None:
        return None
    found = _PEOPLE_COUNT.search(portion)
    if not found:
        return _answer(f"{portion} for {count} people")
    old = next((group for group in found.groups() if group), None)
    if old is None:
        return None
    rebuilt = portion[:found.start()] + found.group(0).replace(old, str(count), 1) \
        + portion[found.end():]
    return _answer(rebuilt)


def _carried_measure(clean, memory):
    bare = _bare_measure(clean)
    if bare is None:
        return None
    said, food = bare
    previous = _previous_measure(memory)
    if not previous:
        return None
    want = _ASKED_MEASURE.search(previous)
    if not want:
        return None
    want_family = _named_unit(want.group("want"))
    unit_word, unit = said[-1]
    previous_units = _unit_words(previous)
    source = None
    for word, named in previous_units:
        if want_family is None or named[1] != want_family[1]:
            source = (word, named)
    if not food:
        food = _food_named(previous)
    of_food = (" of " + food[0]) if food else ""
    if want_family and unit[1] == want_family[1] and source:
        rebuilt = f"how many {unit_word} in a {source[0]}{of_food}"
    else:
        rebuilt = f"how many {want.group('want')} in a {unit_word}{of_food}"
    return _answer(rebuilt)


_FRACTIONS = {0.25: "a quarter cup", 0.5: "half a cup", 0.75: "three quarters of a cup",
              1 / 3: "a third of a cup", 2 / 3: "two thirds of a cup",
              1.5: "one and a half cups", 2.5: "two and a half cups"}


def _a_or_an(word):
    word = str(word)
    if word[:1].lower() in "aeiou" or word.lower().startswith("hour"):
        return "an " + word
    return "a " + word


def _amount_phrase(value, unit):
    if unit in _SHARE_OF_CUP:
        said = _cups_phrase(value, unit)
        if said != f"{_fmt(value)} {_say(value, unit, one=False)}":
            return said
    if value in (0.25, 0.5, 0.75) and unit in SAID_ONE:
        word = {0.25: "a quarter of", 0.5: "half", 0.75: "three quarters of"}[value]
        return f"{word} {_a_or_an(SAID_ONE[unit])}"
    return f"{_fmt(value)} {_say(value, unit)}"


def _cups_phrase(amount, unit, spoons=False):
    if unit == "cup":
        for value, said in _FRACTIONS.items():
            if abs(amount - value) < 0.06:
                return said
        if abs(amount - 1) < 0.06:
            return "1 cup"
        if spoons and 0 < amount < 0.5:
            spoons = amount * 16
            if spoons < 2:
                return f"{_spoons(spoons * 3)} teaspoons"
            if spoons < 10:
                return f"{_spoons(spoons)} tablespoons"
        if amount >= 0.1:
            amount = round(amount, 1)
    return f"{_fmt(amount)} {_say(amount, unit, one=False)}"


def _spoons(count):
    nearest = round(count * 2) / 2
    if nearest == int(nearest):
        return str(int(nearest))
    return f"{int(nearest)} 1/2"


_SPECIFIC = re.compile(r"\b(gas mark|fan oven|fan|cooking|recipe|stick of butter|sticks? of butter)\b")


def answers_more_than_a_pair(clean):
    if not isinstance(clean, str):
        return False
    if _SPECIFIC.search(clean):
        return True
    return _food_named(clean) is not None


def _food_named(clean):
    best = None
    for name, grams in GRAMS_PER_CUP:
        if re.search(rf"\b{re.escape(name)}\b", clean):
            if best is None or len(name) > len(best[0]):
                best = (name, grams)
    return best


def _named_ingredient(clean, mentions, measured):
    food = _food_named(clean)
    if not food:
        return None
    food_name, grams_per_cup = food
    said_food = AS_KITCHEN_SAYS.get(food_name, food_name)
    wanted = [unit for _, _, family, unit in mentions if unit in _SHARE_OF_CUP]
    if not wanted:
        return None
    for value, family, unit, _ in measured:
        if unit in _SHARE_OF_CUP:
            grams = value * grams_per_cup * _SHARE_OF_CUP[unit]
            source = _amount_phrase(value, unit) + f" of {said_food}"
            source = source[0].upper() + source[1:]
            wanted_mass = [u for _, _, fam, u in mentions if fam == "mass"]
            if not wanted_mass:
                continue
            target = wanted_mass[0]
            if target in _SHARE_OF_CUP:
                continue
            amount = grams / _factor("mass", target)
            said = _grams(amount) if target == "g" else _fmt(amount)
            return f"{source} is about {said} {SAID[target]}."
        if family == "mass":
            grams = value * _factor("mass", unit)
            target = wanted[0]
            amount = grams / (grams_per_cup * _SHARE_OF_CUP[target])
            source = _amount_phrase(value, unit) + f" of {said_food}"
            source = source[0].upper() + source[1:]
            return f"{source} is about {_cups_phrase(amount, target, spoons=True)}."
    return None


def _plural_of(name):
    head, _, tail = name.partition(" ")
    if head.endswith("y") and len(head) > 1 and head[-2] not in "aeiou":
        head = head[:-1] + "ies"
    elif head.endswith(("o", "ch", "sh", "s", "x")):
        head += "es"
    else:
        head += "s"
    return head + (" " + tail if tail else "")


def _a(name):
    return ("an " if name[0] in "aeiou" else "a ") + name


_SAID_COUNT = {2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six"}


def _counted_as(word):
    word = " ".join(word.replace("-", " ").split())
    fractions = {"half": 0.5, "a half": 0.5, "quarter": 0.25, "a quarter": 0.25,
                 "three quarters": 0.75, "a third": 1 / 3, "two thirds": 2 / 3}
    if word in fractions:
        return fractions[word]
    whole_and_a_half = re.fullmatch(r"(one|two|three|four) and a half", word)
    if whole_and_a_half:
        return _SAID_WHOLE[whole_and_a_half.group(1)] + 0.5
    if re.fullmatch(r"\d+(?:\.\d+)?", word):
        return float(word) if "." in word else int(word)
    return _SAID_WHOLE[word]


def _piece_named(clean):
    if _UNCOUNTED.search(_WHOLE_THING.sub("", clean)):
        return None
    if _MEASURE_AFTER_PIECE.search(clean):
        return None
    best = None
    for name, grams in PIECE_GRAMS:
        for words in (name, _plural_of(name)):
            match = re.search(rf"(?<![\w.]){re.escape(words)}(?![\w])"
                              r"(?=\s*(?:$|[,?]|of\b|weigh|weighs|weighed|about|in grams?|in g\b|to grams|is\b))",
                              clean)
            if not match:
                continue
            counted = _COUNT.search(clean[:match.start()])
            if not counted:
                continue
            if best is None or len(name) > len(best[0]):
                best = (name, grams, _counted_as(counted.group(1)))
    return best


def _piece_weight(clean):
    if not _asks_for_weight(clean):
        return None
    piece = _piece_named(clean)
    if not piece:
        return None
    for start, _end, _family, _unit in _mentions(clean):
        if _number_before(clean, start) is not None:
            return None
    name, grams, count = piece
    amount = _mass_of(grams * count)
    if count == 1:
        return f"{_a(name).capitalize()} is about {amount}."
    said, plural = _count_phrase(count)
    if not plural:
        return f"{said} {_a(name)} is about {amount}."
    return f"{said} {_plural_of(name)} weigh about {amount}."


def _count_phrase(count):
    fractions = {0.25: "A quarter of", 1 / 3: "A third of", 0.5: "Half",
                 2 / 3: "Two thirds of", 0.75: "Three quarters of"}
    for share, said in fractions.items():
        if abs(count - share) < 0.01:
            return said, False
    if count != int(count):
        whole = int(count)
        word = "One" if whole == 1 else _SAID_COUNT.get(whole, _fmt(whole))
        return f"{word} and a half", True
    if count in _SAID_COUNT:
        return _SAID_COUNT[count], True
    return _fmt(count), True


def _named_unit(text):
    best = None
    for match in _UNIT_WORD.finditer(text):
        if best is None or len(match.group(0)) > best[2]:
            best = _NAMES[match.group(0)] + (len(match.group(0)),)
    return (best[0], best[1]) if best else None
