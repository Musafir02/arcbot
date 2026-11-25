
from .lookup import entry

ANSWERS = ("cooking", "food-and-drink", "family-and-parenting")

ENTRIES = []

DRINK_COOLING_NAMES = ("tea", "coffee", "cuppa", "brew", "hot chocolate", "mug", "cup", "drink",
                       "kettle", "teapot")

DRINK_COOLING_ASKS = ("to cool", "takes to cool", "take to cool", "cool down", "cooling down",
                      "cool off", "cooling off", "cool enough", "too hot to drink",
                      "too hot to sip", "cool before drinking", "cool before you drink",
                      "cool before i drink", "let it cool", "let my tea cool", "let my coffee cool",
                      "let the tea cool", "let the coffee cool", "let a cup", "let my cup",
                      "let the cup", "let it cool down")

ENTRIES.append(
    entry("a-drink-cooling", (DRINK_COOLING_NAMES, DRINK_COOLING_ASKS),
          "Five to ten minutes in an ordinary room: a drink comes off the kettle at about 90C "
          "and is comfortable to sip at about 60C, and a splash of cold milk takes it down at "
          "once. A wide mug cools faster than a tall narrow one, and standing the mug in a bowl "
          "of cold water does it in a couple of minutes - stir it and test it with your lip, not "
          "a finger. A lid on the mug keeps the heat in, so take it off if you want it sooner.",
          ask=DRINK_COOLING_ASKS,
          avoid=("soup", "stew", "curry", "casserole", "broth", "gravy", "porridge", "chilli",
                 "leftover", "leftovers", "in the fridge", "before the fridge", "freezer",
                 "ice", "iced", "cold brew", "ice cream", "fizzy", "soda", "beer", "wine"),
          bias=6))

HOT_THING_COOLING = ("to cool", "takes to cool", "take to cool", "cool down", "cooling down",
                     "cool off", "cooling off", "cool enough", "too hot", "how long until it is",
                     "how long before it is", "cools", "cool before", "cool for")

ENTRIES.append(
    entry("a-hot-water-bottle-cooling", (("hot water bottle", "hottie", "hot water bottles",
                                          "wheat bag", "heat pack"),
                                         HOT_THING_COOLING),
          "A hot water bottle stays warm for four to six hours under the covers, and it is only "
          "too hot for the first twenty minutes or so. If you want it gentler from the start, "
          "fill it from the hot tap rather than the kettle and wrap it in a towel or a pillowcase "
          "- running it under the cold tap for a few seconds does the same. Never fill it with "
          "boiling water for a child or an older person, and check the stopper and the rubber for "
          "cracks before each winter.",
          ask=HOT_THING_COOLING,
          avoid=("cost", "price", "much", "buy", "worth", "last", "lasts", "burst", "leak",
                 "smell", "rubber", "how often", "replace", "how do i cool", "how to cool",
                 "how can i cool", "ways to cool", "make it cooler", "cool it down quickly"),
          bias=6))

ENTRIES.append(
    entry("boiled-water-for-a-feed-cooling", (("boiled water", "kettle water", "water for the "
                                               "formula", "water for a feed", "water for the bottle",
                                               "formula water", "sterilised water"), HOT_THING_COOLING),
          "Make the feed within 30 minutes of boiling: the water should still be at least 70C when "
          "it goes onto the powder, because that is what kills anything in it. Then cool the "
          "bottle under a running cold tap or stand it in a jug of cold water - about 10 to 15 "
          "minutes, and shake a drop onto the inside of your wrist to test it. Water that has been "
          "boiled once and left to cool is fine for drinking, but make a fresh feed rather than "
          "reheating an old one.",
          ask=HOT_THING_COOLING,
          avoid=("bath", "bathwater", "hot water bottle", "washing up", "tap water", "hard water",
                 "filter", "kettle limescale", "descale"),
          bias=6))

ENTRIES.append(
    entry("a-pot-of-rice-cooling", (("rice", "cooked rice", "leftover rice"), HOT_THING_COOLING),
          "Spread the rice out on a tray or a wide plate and it is cool enough for the fridge in "
          "about 20 to 30 minutes - a shallow layer, not a deep pan with the lid on. Get it into "
          "the fridge within the hour, keep it no more than a day, and reheat it once, until it is "
          "steaming hot all through. Rice left standing at room temperature is the one to bin, "
          "because of the spores that survive cooking.",
          ask=HOT_THING_COOLING,
          avoid=("how long to cook", "take to cook", "simmer", "boil", "boiling", "absorption",
                 "cup", "grams", "portion", "water ratio", "rice cooker", "pilau", "risotto"),
          bias=6))

