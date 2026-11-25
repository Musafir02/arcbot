import re

from .lookup import DISH_ASK, RING_AS_A_CALL, entry

ANSWERS = ("garden-and-plants",)

_SMALL_PLACE = re.compile(r"\bsmall\b\s+(?:garden|gardens|space|plot|patio|balcony|yard|"
                          r"allotment|greenhouse|windowsill|window box|pot|pots|veg patch|"
                          r"vegetable patch|veg plot|back yard)")


def _a_small_place_ask(understood):
    reading = understood if isinstance(understood, dict) else {}
    line = " ".join(str(reading.get(key) or "") for key in ("clean", "norm_text", "plain")).lower()
    return not _SMALL_PLACE.search(line)


GONE_WILD = ("overgrown", "over growing", "out of control", "gone wild", "gone mad",
             "gone rampant", "gone berserk", "out of hand", "getting out of hand",
             "taking over", "taken over", "takes over", "took over", "taking it over",
             "rampant", "running riot", "gone everywhere", "spreading everywhere",
             "a mess", "is a jungle", "needs cutting back", "needs cutting",
             "needs trimming", "needs a cut", "needs taming", "needs bringing back",
             "getting too big", "got too big", "taken the garden over", "taking the garden over")

INDOORS = ("plant", "plants", "houseplant", "house plant", "house plants", "pot", "pots",
           "compost", "soil", "potting", "indoor", "indoors", "windowsill", "leaves", "leaf",
           "stems", "fern", "ferns", "orchid", "orchids", "monstera", "cactus", "cacti",
           "succulent", "succulents", "peace lily", "snake plant", "spider plant", "basil",
           "herb", "herbs", "calathea", "pothos", "aloe", "dracaena", "palm", "geranium",
           "african violet", "christmas cactus", "hoya", "amaryllis", "cyclamen")



_LAWN_MOW = ("Mow little and often in the growing season, not shorter than about 4cm, and leave the "
             "clippings off unless it is long.")
_LAWN_DEAD = ("A brown lawn is usually dormant rather than dead, so check before you dig it up: "
              "pull a tuft - if the roots hold and there is green at the base it will come back "
              "after a week of deep watering, and if the tuft lifts like a mat it has gone. Dead "
              "patches want the old grass raked out and reseeded in early autumn, when the ground "
              "is warm and the rain does the watering.")
_LAWN_COLOUR = ("Yellow or brown patches in dry weather are usually thirst - water deeply once a "
                "week in a dry spell rather than a sprinkle daily - and thin pale grass in spring "
                "wants a feed rather than a reseed.")
_LAWN_REST = ("Scarify and aerate in autumn, reseed bare patches, and water deeply once a week in "
              "dry spells rather than a sprinkle daily.")
_LAWN_GREEN = ("Deeper green comes from feeding and watering rather than from seed or a spray: a "
               "spring lawn feed with nitrogen in it, and a deep soak once a week in dry weather "
               "instead of a daily sprinkle.")
_LAWN_REST_SEED = "Scarify and aerate in autumn, and reseed the bare patches."
_LAWN_AERATE = ("Aerate once a year, in early autumn while the grass is still growing and the "
                "ground is soft: push a garden fork in about 10cm deep at 15cm intervals and rock "
                "it back, which is enough for most lawns, or hire a hollow-tine machine for "
                "compacted clay or a lawn that people walk on all summer. Brush sharp sand or a "
                "top dressing into the holes afterwards, leave the plugs on the grass to break "
                "down, and water it if the weather stays dry for a week. A lawn that is bad enough "
                "to want aerating twice a year wants the thatch scarified out first, a fortnight "
                "before.")
_LAWN_RESEED = ("Reseed in early autumn, or in spring once the soil has warmed up: fork the bare "
                "patch over to loosen it, rake it level, scatter the seed at the rate on the box, "
                "and press it in with a board or the back of a rake so it is in contact with the "
                "soil. Keep it damp for a fortnight - a light sprinkle morning and evening beats "
                "one soak - and keep off it until the new grass is about 5cm tall.")
_LAWN_SCARIFY = ("Scarify in early autumn, or in spring on a lawn that has gone spongy: set a "
                 "spring-tine rake or a machine to just touch the surface and pull the dead "
                 "thatch out in two passes, one way across the lawn and one up and down, taking "
                 "off no more than a centimetre at a time. Clear what comes up, water it if the "
                 "weather stays dry, and feed it a fortnight later rather than the same day. Once "
                 "a year is plenty, and a lawn with less than a centimetre of thatch does not "
                 "need it at all.")


_A_RAISED_BED_BOTTOM = ("bottom", "cheap", "cheaply", "cost", "fill it", "fill the", "filling",
                        "what goes in", "put in", "line", "line it", "lining", "cardboard",
                        "logs", "twigs", "leaves", "rubble", "gravel", "layer", "layers",
                        "newspaper", "free", "for free", "bulk")
_A_RAISED_BED_GRASS = ("grass", "lawn", "turf", "weeds", "dig", "digging", "no dig")
_A_RAISED_BED_PAVING = ("paving", "concrete", "patio", "slabs", "slab", "driveway", "decking",
                        "tarmac", "on the ground")
_A_RAISED_BED_GROW = ("what can i grow", "what to grow", "grow in", "plant in", "grow this",
                      "what will grow", "what should i grow", "crops", "vegetables in", "veg in")
_A_RAISED_BED_SOIL = ("soil", "compost", "topsoil", "loam", "mix", "manure", "grit", "sand",
                      "multipurpose")
_A_RAISED_BED_AMOUNT = ("how much", "how many bags", "how many litres", "volume", "calculate",
                        "work out", "cubic", "tonne", "tonnes", "bulk bag")
_A_RAISED_BED_DRY = ("dries out", "drying out", "dried out", "dry out", "water", "watering",
                     "water it", "wilt", "wilting", "mulch")
_A_RAISED_BED_BUILD = ("build", "make", "wood", "timber", "sleepers", "sleeper", "bricks",
                       "brick", "materials", "cost", "cheap", "should i use", "treated")


def _a_raised_bed(memory, understood):
    said = _words(understood)
    if any(_has(said, word) for word in _A_RAISED_BED_AMOUNT):
        return ("Work it out as a volume: length times width times depth, all in metres, and add "
                "a tenth for settling. Bulk loam-based compost from a builders' merchant is far "
                "cheaper than bags, and two parts topsoil to one part compost fills it better "
                "than pure compost, which sinks.")
    if any(_has(said, word) for word in _A_RAISED_BED_DRY):
        return ("A raised bed dries out much faster than the ground, because the roots are above "
                "it on all four sides: water when the top 2cm is dry, a good soak twice a week in "
                "summer rather than a daily sprinkle, and a mulch of compost or grass clippings "
                "holds it. Thirty centimetres of soil holds far longer than fifteen.")
    if any(_has(said, word) for word in _A_RAISED_BED_BOTTOM):
        return ("Line the bottom with cardboard to smother the weeds, then fill it free: logs, "
                "twigs, leaves and any garden waste you have, then two parts topsoil to one part "
                "compost on top. Skip rubble, gravel and plastic, and keep it no wider than about "
                "1.2m so you can reach the middle from both sides without standing on the soil.")
    if any(_has(said, word) for word in _A_RAISED_BED_GRASS):
        return ("Straight onto the grass with no digging: mow it short, lay cardboard or four "
                "layers of newspaper over the whole footprint, soak it, and fill on top - the "
                "grass dies underneath and the worms pull it in. Keep it no wider than about 1.2m "
                "so you can reach the middle from both sides.")
    if any(_has(said, word) for word in _A_RAISED_BED_PAVING):
        return ("On slabs or concrete it needs no cardboard and no digging: stand the frame on "
                "the paving, leave a gap at the bottom edge so water runs off, and be ready to "
                "water more, because a bed on slabs dries out faster than one on soil. Twenty "
                "centimetres of soil is enough for salad, herbs and dwarf beans.")
    if any(_has(said, word) for word in _A_RAISED_BED_GROW):
        return ("In twenty centimetres of soil: salad, herbs, radishes, dwarf beans, onions and "
                "carrots. Potatoes, tomatoes, courgettes and anything tall want forty or more, "
                "because their roots and their water need the depth. Keep it no wider than about "
                "1.2m so you can reach the middle from both sides without standing on the soil.")
    if any(_has(said, word) for word in _A_RAISED_BED_SOIL):
        return ("Fill it with a mix of topsoil and compost rather than pure compost, which dries "
                "out and sinks: two parts topsoil to one part compost, and a handful of grit if it "
                "holds water. Twenty centimetres is enough for salad, herbs and dwarf beans, "
                "thirty for carrots, onions and beetroot.")
    if any(_has(said, word) for word in _A_RAISED_BED_BUILD):
        return ("Untreated timber is fine and cheap and lasts about five years; tanalised timber "
                "8 to 10 years; old bricks or paving slabs cost nothing and last longer, and "
                "creosoted railway sleepers stay away from anything you eat. Keep it no wider than "
                "about 1.2m so you can reach the middle.")
    return ("Twenty centimetres deep does salad, herbs and dwarf beans; thirty for carrots, onions "
            "and beetroot; forty or more for potatoes and tomatoes. Untreated timber is fine and "
            "cheap, line the bottom with cardboard to smother the weeds, and fill it with a mix of "
            "topsoil and compost rather than pure compost, which dries out and sinks. Keep it no "
            "wider than about 1.2m so you can reach the middle from both sides without standing on "
            "the soil.")


def _words(understood):
    return " " + re.sub(r"[^a-z0-9' ]+", " ", str((understood or {}).get("clean")
                                                  or (understood or {}).get("text")
                                                  or "").lower()) + " "


def _has(line, word):
    return re.search(r"(?<![a-z0-9])" + re.escape(word) + r"(?![a-z0-9])", line) is not None


_WHEN_ASKS = ("when", "what month", "which month", "what time of year", "time of year",
              "best time", "what time", "month", "season", "what week",
              "how often", "how frequently", "how regularly", "when in the year")


def _asks_when(line):
    return any(_has(line, word) for word in _WHEN_ASKS)


def _cutting_reply(memory, understood):
    body = ("Cut a shoot about 8 to 10cm long just below a leaf joint, strip the bottom leaves "
            "off, and push it into a small pot of damp, gritty compost, then a clear bag over the "
            "top holds the moisture in. Bright light, out of direct sun, and most soft cuttings - "
            "geraniums, fuchsias, penstemons, herbs - root in two to four weeks; tug one gently and "
            "it holds when there are roots. Geraniums, busy lizzies and pothos also root in a glass "
            "of water changed every few days, and a spider plant does the job for you: the "
            "plantlets on the long runners are ready to pot up once they have roots 2cm long, "
            "still attached to the parent if you like.")
    if _asks_when(_words(understood)):
        return ("Late spring to early summer, when the new growth has firmed at the base but still "
                "bends - May and June for most shrubs. " + body)
    return body
_GARDEN_IN_THE_LINE = ("garden", "gardens", "border", "borders", "flowerbed", "flowerbeds",
                       "plot", "yard", "outdoor", "outdoors", "front", "back", "lawn",
                       "allotment", "outside", "flower bed", "flower beds")


def _names_the_garden(understood):
    said = " " + re.sub(r"[^a-z0-9' ]+", " ", str((understood or {}).get("text") or "").lower()) + " "
    return any(_has(said, word) for word in _GARDEN_IN_THE_LINE)


_KITCHEN_ROT = ("cheese", "bread", "loaf", "loaves", "toast", "jam", "meat", "ham",
                "bacon", "sausage", "mince", "chicken", "fish", "salmon", "milk",
                "butter", "cream", "yoghurt", "yogurt", "leftovers", "sandwich", "pasta",
                "rice", "soup", "sauce", "gravy", "cake", "biscuit")
_GROUND_THING = ("plant", "plants", "crop", "crops", "fruit", "fruits", "seedling",
                 "seedlings", "greenhouse", "allotment", "vine", "vines", "tree", "trees",
                 "leaf", "leaves", "root", "roots", "compost", "soil", "ground", "pot",
                 "pots", "bed", "beds", "garden", "flower", "flowers")


def _a_kitchen_thing(understood):
    line = _words(understood)
    if not any(_has(line, word) for word in _KITCHEN_ROT):
        return False
    return not any(_has(line, word) for word in _GROUND_THING)


_LEAF_WORDS = ("leaf", "leaves", "yellow", "yellowing", "yellowed", "pale", "veins",
               "curling", "curled", "curl", "limp", "drooping")
_A_FRUIT_THAT_ROTS = ("black", "brown", "rot", "rots", "rotting", "rotten", "sunken", "squashy",
                      "squishy", "mushy", "patch", "patches", "blossom end", "end rot", "eaten",
                      "hole", "holes")


def _a_leaf_problem_not_the_fruit(understood):
    line = _words(understood)
    if not any(_has(line, word) for word in _LEAF_WORDS):
        return False
    return not any(_has(line, word) for word in _A_FRUIT_THAT_ROTS)


def _lawn(memory, understood):
    line = " " + re.sub(r"[^a-z0-9' ]+", " ", str(understood.get("clean") or understood.get("text")
                                                        or "").lower()) + " "
    colour = ("yellow", "yellowing", "brown", "browning", "patchy", "patches", "dying",
              "dead", "died", "killed")
    green = ("green", "greener", "greenest", "lush", "thicker", "thick", "dull", "pale",
             "washed out", "faded", "tired", "yellowish", "pale green", "not very green", "thin",
             "feed", "feeding", "fertiliser", "fertilizer", "starved")
    if any(_has(line, word) for word in ("aerate", "aerating", "aeration", "aerated",
                                         "spiking", "spike", "hollow tine", "hollow tines",
                                         "compacted", "compaction")):
        return _LAWN_AERATE
    if any(_has(line, word) for word in ("scarify", "scarifying", "scarified", "scarifier",
                                         "dethatch", "dethatching", "thatch", "thatching",
                                         "spongy", "raking out")):
        return _LAWN_SCARIFY
    if any(_has(line, word) for word in ("reseed", "reseeding", "re seed", "oversow", "over sow",
                                         "sow grass", "grass seed")):
        return _LAWN_RESEED
    if any(_has(line, word) for word in green) and not any(_has(line, word) for word in colour):
        return " ".join((_LAWN_GREEN, _LAWN_MOW, _LAWN_REST_SEED))
    if any(_has(line, word) for word in ("patch", "patches", "patchy", "in places",
                                         "here and there")):
        return " ".join((_LAWN_COLOUR, _LAWN_MOW, _LAWN_REST_SEED))
    if any(_has(line, word) for word in ("dead", "died", "killed")):
        return " ".join((_LAWN_DEAD, _LAWN_REST_SEED))
    if any(_has(line, word) for word in colour):
        return " ".join((_LAWN_COLOUR, _LAWN_MOW, _LAWN_REST_SEED))
    return " ".join((_LAWN_MOW, _LAWN_REST))


BRASSICA_HARVEST = {
    "broccoli": ("Cut broccoli while the head is still tight and green, before any yellow shows: "
                 "about ten to twelve weeks after planting out for a summer kind. Cut the central "
                 "head first with 10cm of stem, then the side shoots over the weeks after."),
    "cauliflower": ("Cut a cauliflower when the curd is still tight and white, ten to sixteen weeks "
                    "after planting out: bend the outer leaves over the head to keep it white, and "
                    "cut it before the curd loosens or looks grainy."),
    "sprouts": ("Pick sprouts from the bottom of the stalk upwards from October, after a frost or "
                "two, twisting each one off when it is tight and walnut-sized. The stalk goes on "
                "producing upwards for weeks, and the tops are eaten as spring greens."),
    "kale": ("Pick kale leaf by leaf from the top of the plant, never more than a third at once, "
             "and it goes on cropping all winter; the young leaves at the crown are the tender "
             "ones."),
    "cabbage": ("Cut cabbages when the heart is firm: spring and summer kinds about three months "
                "after planting out, winter ones from October. Cut rather than pull, so the stump "
                "can throw a second small head."),
}


def _brassica_harvest(memory, understood):
    line = _words(understood)
    for crop in ("broccoli", "cauliflower", "sprouts", "sprout", "kale", "cabbage"):
        if _has(line, crop):
            return BRASSICA_HARVEST["sprouts" if crop == "sprout" else crop]
    return " ".join(BRASSICA_HARVEST[crop] for crop in ("cabbage", "sprouts", "kale"))


SOW_ASK = ("when", "plant", "planting", "planted", "sow", "sowing", "sowed", "month", "months",
           "time of year", "best time", "what time", "early", "late", "too late", "too early",
           "from seed", "seed potatoes", "seed potato")
SOW_NOT = ("yellow", "yellowing", "dying", "wilting", "drooping", "blight", "rot", "rotting",
           "mould", "mold", "pests", "slugs", "snails", "caterpillars", "holes", "eaten",
           "not growing", "failed", "tiny", "small", "came up", "come up", "no shoots",
           "not sprouted", "nothing sprouted", "rotten", "mouldy", "digging",
           "store", "storing", "chit", "chitting", "container", "pot", "pots",
           "indoor", "indoors", "windowsill", "greenhouse", "allotment", "raised bed")


COURGETTE_HARVEST = (
    "Pick courgettes from July when they are 10 to 15cm long, and go over the plants every day "
    "in warm weather: one left to swell to marrow size stops the plant producing. Cut them with "
    "a short stalk and eat them within a few days.")
PUMPKIN_HARVEST = (
    "Pumpkins and squash are ready in September or October, when the skin has hardened so a "
    "fingernail will not mark it and the stalk has gone corky: cut with a long handle, cure them "
    "in the sun for a week, and they keep for months somewhere dry.")
BEAN_HARVEST = (
    "Broad beans are ready when the pods bulge and the beans inside are the size of a thumbnail, "
    "from June: pick from the bottom of the plant upwards and pinch out the tops once the flowers "
    "set, to stop blackfly. Runner and french beans are ready from July, at 15cm, while they are "
    "slim and snap without a string: pick every couple of days or the plants stop setting.")


def harvest_crops():
    names = set()
    for words, _reply in HARVEST_MORE:
        names.update(words)
    for words, _sow in SOWING:
        if HARVEST.get(words[0]):
            names.update(words)
    return names


def _courgette_harvest(memory, understood):
    line = _words(understood)
    if _has(line, "pumpkin") or _has(line, "pumpkins") or _has(line, "squash"):
        return PUMPKIN_HARVEST
    return COURGETTE_HARVEST


def _bean_harvest(memory, understood):
    line = _words(understood)
    if _has(line, "broad") or _has(line, "broad bean") or _has(line, "broad beans"):
        return ("Broad beans are ready from June, when the pods bulge and the beans inside are "
                "the size of a thumbnail: pick from the bottom of the plant upwards, and pinch "
                "out the tops once the flowers have set to stop blackfly. Runner and french "
                "beans follow from July.")
    return ("Runner and french beans are ready from July: pick them at 15cm while they are slim "
            "and snap without a string. Broad beans are a month earlier, when the pods bulge. "
            "Pick every couple of days or the plants stop setting.")


HARVEST_ASK = ("harvest", "harvesting", "lift", "lifting", "dig up", "dig them up", "ready",
               "pick", "picking", "ripe", "when are", "how do i know", "pulling", "pull them",
               "cut", "cutting", "cut them", "cutting them")
HARVEST_KEYS = ("when", "time", "ready", "done", "month", "harvest", "harvesting", "lift",
                "lifting")
HARVEST = {
    "potato": ("Lift new potatoes in June and July, once the flowers open, and maincrops in "
               "September and October when the tops have died back. Fork well beside the row so "
               "you do not spear them, then leave them on the soil for an hour to dry before "
               "storing in paper sacks in the dark."),
    "carrot": ("Pull carrots from June, thinning as you go, and lift the main crop in October "
               "before the first hard frost. They are ready when the shoulder is 2cm across. "
               "Twist the tops off before storing, because leaves keep drawing water, and keep "
               "them in damp sand in a cool shed."),
    "onion": ("Lift onions in July and August when the tops fall over and start to yellow: bend "
              "the tops down, leave them a fortnight on the soil in dry weather, then store in "
              "nets somewhere airy. An onion that is not properly dried is the one that rots "
              "and takes the rest of the sack with it."),
    "lettuce": ("Cut lettuce about eight to twelve weeks after sowing, in the morning when it is "
                "cold and crisp, at the base with a knife, and it will often come again. A "
                "lettuce that has started to shoot up a stem has bolted: pick it at once and eat "
                "it that day, because it turns bitter."),
    "pea": ("Pick peas from June, when the pods are full but still bright green and snap "
            "cleanly, and go along the row every two or three days. Leaving them on the plant "
            "stops it flowering, and a pod left too long goes starchy and tough."),
    "bean": _bean_harvest,
    "beetroot": ("Beetroot is ready eight to ten weeks after sowing, at golf-ball size for "
                 "eating fresh and up to tennis-ball size for storing. Twist the leaves off "
                 "rather than cutting, so it does not bleed, and lift them before the first "
                 "hard frost."),
    "parsnip": ("Lift parsnips from October through to February, and leave them in the ground "
                "until after a frost: the cold turns starch to sugar and they taste far better. "
                "Fork underneath the root rather than pulling, because a parsnip snaps at the "
                "shoulder and the best part stays in the soil."),
    "leek": ("Leeks can be lifted from September and stand in the ground all winter, which is "
             "the point of them: dig as you need them, and they will take hard frost. Earth up "
             "the stems a few weeks before lifting if you want more white."),
    "cabbage": _brassica_harvest,
    "courgette": _courgette_harvest,
    "radish": ("Radishes are ready about four weeks after sowing, at marble size: pull one to "
               "check rather than waiting for the row. Left longer they go woody and hot, so sow "
               "little and often instead of one big row."),
    "swede": ("Swedes are lifted from October, and are better after a frost, which sweetens them "
              "the way it does parsnips; they will stand in the ground into winter. Turnips are "
              "quick - six to eight weeks - and are best pulled small, at 5 to 7cm across."),
}


HARVEST_MORE = (
    (("garlic",),
     "Lift garlic in July, when the bottom three leaves have yellowed and the rest are still "
     "green: stop watering a fortnight before, ease each bulb out with a fork, and dry them "
     "somewhere airy for two or three weeks before storing. Left in longer the bulbs split and "
     "they keep badly."),
    (("tomato", "tomatoes"),
     "Pick tomatoes from late July as they turn fully red, and take the whole truss in October "
     "before the first frost. Green ones left then will ripen on a windowsill next to a banana. "
     "A tomato is ready when it gives slightly in the hand and smells of tomato."),
    (("apple", "apples"),
     "Apples are ready from August for the earlies and October for the keepers: cup one and twist "
     "- ripe fruit comes away with the stalk on and the pips inside are brown. Pick in dry "
     "weather, use the windfalls first, and store only perfect fruit, in a cool dark place, not "
     "touching."),
    (("pear", "pears"),
     "Pick pears before they are ripe, from late August, while the flesh is still hard: lift one "
     "and twist, and when the stalk parts easily it is ready to finish indoors. A pear left to "
     "soften on the tree goes gritty and rotten at the core."),
    (("plum", "plums", "damson", "damsons"),
     "Plums are ready from August, when they colour up and give a little at the stalk end: pick "
     "with the stalk on and eat the soft ones first. A plum that comes away at a squeeze is over "
     "ripe, and the wasps find those the same day you do."),
    (("strawberry", "strawberries"),
     "Pick strawberries from June, when they are red all over including the tip, and pick with a "
     "short stalk in the cool of the morning. A berry that is pale at the tip will not sweeten "
     "after picking, and one left to rot takes the rest with it."),
    (("raspberry", "raspberries"),
     "Raspberries ripen from July: pick when the berry comes away from its core with no tug, and "
     "eat or freeze them the same day, because they keep a day at most. Autumn kinds crop on into "
     "October."),
    (("rhubarb",),
     "Pull rhubarb from April to the end of June, twisting each stalk out and leaving three on "
     "every crown, then stop: the plant needs the rest of the year to build up for next spring. "
     "Do not pull any in the first year after planting, and never eat the leaves."),
    (("sweetcorn", "sweet corn", "corn", "corn on the cob"),
     "Sweetcorn is ready in August and September: peel back a little husk and press a kernel with "
     "a fingernail - milky juice means ready, clear means wait, doughy means it has gone over. "
     "Cook it within the hour, because the sugar turns to starch fast."),
    (("chilli", "chillies", "chili", "chilies"),
     "Chillies are ready from late summer: pick green for a milder heat, or leave them on to turn "
     "red for the fullest flavour. Cut them with a short stalk and keep picking, because a plant "
     "left to ripen stops setting new fruit."),
    (("pumpkin", "pumpkins", "squash", "squashes"),
     "Pumpkins and squash are ready in September or October, when the skin has hardened so a "
     "fingernail will not mark it and the stalk has gone corky: cut with a long handle, cure them "
     "in the sun for a week, and they keep for months somewhere dry."),
)
DONE_NOT = ("cooked", "cooking", "boil", "boiled", "boiling", "roast", "roasted",
            "steam", "steamed", "soft", "tender", "mash", "mashed", "al dente")


EATEN_RAW = frozenset("""raspberry strawberry blackberry blackcurrant redcurrant gooseberry apple pear
plum damson cherry tomato""".split())


def _done_means_a_pan(crop):
    return () if crop in EATEN_RAW else ("done",)


def _harvest_entries():
    out = []
    for words, _sow in SOWING:
        reply = HARVEST.get(words[0])
        if not reply:
            continue
        out.append(entry("harvest-" + words[0], (words, HARVEST_KEYS),
                         reply, ask=HARVEST_ASK,
                         avoid=SOW_NOT + DONE_NOT + _done_means_a_pan(words[0]), bias=3))
    for words, reply in HARVEST_MORE:
        out.append(entry("harvest-" + words[0], (words, HARVEST_KEYS),
                         reply, ask=HARVEST_ASK,
                         avoid=SOW_NOT + DONE_NOT + _done_means_a_pan(words[0]), bias=3))
    return out

SOW_WINDOW = {
    "potato": (3, 4), "carrot": (3, 7), "onion": (3, 4), "lettuce": (3, 8),
    "pea": (3, 6), "bean": (4, 6), "beetroot": (4, 7), "parsnip": (2, 4),
    "leek": (3, 4), "cabbage": (3, 5), "courgette": (4, 6), "radish": (3, 9),
    "swede": (5, 6),
}

MONTH_NUMBER = {
    "january": 1, "february": 2, "march": 3, "april": 4, "june": 6, "july": 7,
    "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "jun": 6, "jul": 7, "aug": 8,
    "sep": 9, "sept": 9, "oct": 10, "nov": 11, "dec": 12,
}
MONTH_PHRASES = ("in may", "of may", "by may", "during may", "this may", "next may")


def _month_named(understood):
    line = _words(understood)
    for word, number in MONTH_NUMBER.items():
        if _has(line, word):
            return number
    if any(phrase in line for phrase in MONTH_PHRASES):
        return 5
    return None


SOW_MONTH = {
    1: ("Not much goes in this month: plant garlic and shallots if the ground is not frozen, and "
        "start broad beans under cloches from late January. Chit early potatoes on a windowsill "
        "and order the seed you want for spring."),
    2: ("Broad beans and parsnips from late February, and onion sets and shallots as soon as the "
        "ground is workable. Sow tomatoes and chillies indoors under cover, and chit the early "
        "potatoes."),
    3: ("The month the plot opens: potatoes, carrots, onions, lettuce, peas, leeks, radish and "
        "cabbages all go in from now. Sow a short row every few weeks rather than one big sowing, "
        "so the crop comes over months instead of all at once."),
    4: ("Potatoes by mid-April, then beetroot and beans, courgettes indoors, and more lettuce and "
        "radish every three weeks. Keep fleece to hand: a late frost is the thing that sets April "
        "back."),
    5: ("Once the frost has gone: beans, courgettes, sweetcorn, squash and swede go out, and keep "
        "sowing lettuce and radish for a steady supply. Harden everything off for a week first."),
    6: ("Last chance for runner and french beans, courgettes and swede; keep salad and radish "
        "going. Water in the morning and mulch, because this is the month everything bolts."),
    7: ("Sow for the winter now: spring cabbage, kale, winter salad and more radish and lettuce for "
        "autumn. Lift onions and garlic as the tops fall over."),
    8: ("Spring cabbage, overwintering onion sets and winter salad go in, and the ground cleared of "
        "potatoes can take a green manure. Keep watering the beans and courgettes."),
    9: ("Sow winter salad and land cress, plant overwintering onion sets and garlic, and clear the "
        "spent crops into the compost. This is the month that decides next spring."),
    10: ("Plant garlic and overwintering broad beans for the earliest crop next year, and put in "
         "onion sets and shallots. Outdoors there is little else to sow except winter salad under "
         "cover, so clear and mulch the beds."),
    11: ("Plant garlic and broad beans if the ground is not frozen, mulch the empty beds, and order "
         "seed potatoes to chit after Christmas. Nothing else goes in outdoors."),
    12: ("Nothing goes in outdoors except garlic in a mild spell. Plan next year's rotation, order "
         "your seed, and start chitting early potatoes indoors after Christmas."),
}


def _sowing_reply(crop, reply):
    early, late = SOW_WINDOW.get(crop, (1, 12))

    def answer(memory, understood):
        line = _words(understood)
        month = _month_named(understood)
        if month is not None and not early <= month <= late:
            return None
        if re.search(r"\btoo late\b|\btoo early\b|\blate for\b", line):
            return ("Later than the usual window it still grows, it just crops later and wants "
                    "watering while it catches up. " + reply)
        return reply

    return answer


NOW_WORDS = re.compile(r"\bnow\b|\bat the moment\b|\bthis month\b|\bcurrently\b|"
                       r"\bthese days\b|\bat the minute\b|\bthis time of year\b")
NEXT_MONTH_WORDS = re.compile(r"\bnext month\b|\bthe month after\b")
MONTH_NAMES = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
               7: "July", 8: "August", 9: "September", 10: "October", 11: "November",
               12: "December"}


SEASON_REPLY = {
    "spring": ("Spring is when the plot fills up: potatoes, carrots, onions, lettuce, peas, leeks "
               "and radish from March, beetroot and beans in April, and courgettes, sweetcorn "
               "and squash once the frost has gone in May. Sow a short row every few weeks "
               "rather than one big sowing."),
    "summer": ("In summer you are sowing for autumn and winter: more lettuce, radish and beetroot "
               "every three weeks, runner and french beans and courgettes until the end of June, "
               "then spring cabbage, kale and winter salad from July. Water in the morning and "
               "mulch, because this is when everything bolts."),
    "autumn": ("Autumn is the sowing for next year: plant garlic, overwintering broad beans and "
               "onion sets, and sow winter salad and land cress under cover. Clear the spent "
               "crops into the compost and mulch the empty beds, because this is the season that "
               "decides next spring."),
    "winter": ("Almost nothing goes in outdoors: garlic and broad beans in a mild spell, and "
               "everything else indoors. Sow tomatoes and chillies under cover from late winter, "
               "chit early potatoes on a windowsill after Christmas, and order the seed you want "
               "for the year."),
}
SEASON_WORDS = tuple(SEASON_REPLY)


def _this_month():
    try:
        import datetime
        return datetime.date.today().month
    except Exception:
        return None


def _sow_month(memory, understood):
    line = _words(understood)
    month = _month_named(understood)
    if month is not None:
        return SOW_MONTH[month]
    for season in SEASON_WORDS:
        if _has(line, season):
            if season == "winter" and re.search(r"\bfor (the )?winter\b|\bover ?winter\b|"
                                                r"\bfor christmas\b|\bbefore winter\b", line):
                return SEASON_REPLY["autumn"]
            return SEASON_REPLY[season]
    if not (NOW_WORDS.search(line) or NEXT_MONTH_WORDS.search(line)):
        return None
    month = _this_month()
    if month is None:
        return None
    if NEXT_MONTH_WORDS.search(line):
        month = month % 12 + 1
    return "It's %s, so here's what goes in. %s" % (MONTH_NAMES[month], SOW_MONTH[month])


SOWING = (
    (("potato", "potatoes", "spuds"),
     "Plant seed potatoes from late March to mid-April, once the soil is workable and no hard "
     "frost is forecast: 30cm apart in rows 60cm apart, 10cm deep, with the sprouts pointing up. "
     "Chit them on a windowsill first, in egg boxes, for six weeks. Earlies go in first, maincrops "
     "by mid-April, and a frost on the young shoots is what sets them back."),
    (("carrot", "carrots"),
     "Sow carrots from late March to July, a few seeds every three weeks rather than one big "
     "sowing, 1cm deep and 5cm apart once thinned. They want a light, stone-free soil: stones "
     "make them fork. Cover the row with fleece or a mesh barrier, because carrot fly finds them "
     "by smell and a barrier is what actually stops it."),
    (("onion", "onions", "shallot", "shallots", "onion sets"),
     "Plant onion sets from mid-March to mid-April, pushing them into firm soil so just the tip "
     "shows, 10cm apart with 30cm between rows. Birds pull them out, so a few short sticks or "
     "netting over the row saves them. Onions want firm ground: tread the bed before planting, "
     "not after, and keep it weeded."),
    (("lettuce", "lettuces", "salad leaves", "rocket", "spinach"),
     "Sow lettuce and salad leaves from March to August, a small pinch every two or three weeks "
     "for a steady supply, 1cm deep and 20cm apart for hearting kinds. They bolt in heat: water "
     "in the morning, shade the row in a hot spell, and pick leaves young. Cut-and-come-again "
     "salad is the easiest thing to grow in a pot."),
    (("pea", "peas", "mangetout", "sugar snap"),
     "Sow peas from March to early June, 5cm deep in a wide flat trench rather than a single "
     "line, 8cm apart, with a net or twiggy sticks up for them to climb. Mice take the seed, so "
     "start them in a gutter of compost if a row disappears. Pick pods every couple of days or "
     "the plants stop producing."),
    (("bean", "beans", "runner beans", "broad beans", "french beans"),
     "Sow runner and french beans from late April to June, once the soil has warmed, 5cm deep "
     "and 20cm apart, after the last frost. Broad beans go in earlier, from February to April, "
     "in a double row. Beans need a frame or cane wigwam from the start, and water at the base "
     "when they flower or the flowers drop."),
    (("beetroot", "beets", "beet"),
     "Sow beetroot from April to July, 2cm deep and 10cm apart, thinning to one plant per station "
     "because each seed cluster holds several. Water regularly: beetroot that dries out goes "
     "woody. You can start in April under cloche and sow again in June for small roots into "
     "autumn."),
    (("parsnip", "parsnips"),
     "Sow parsnips from late February to April, and only fresh seed: parsnip seed dies in a year, "
     "which is why a saved packet comes up empty. Sow 1cm deep, 15cm apart once thinned, on ground "
     "that has not been manured or they fork. They take three weeks to show, so mark the row."),
    (("leek", "leeks", "spring onion", "spring onions"),
     "Sow leeks from March to April in a seedbed, then move them to their final spot in June at "
     "20cm apart, dropping each one into a dibbed hole and watering it in rather than filling the "
     "hole with soil. Spring onions can be sown from March to July, a pinch every three weeks, "
     "and eaten small."),
    (("cabbage", "cabbages", "broccoli", "sprouts", "sprout", "kale", "cauliflower"),
     "Sow cabbage, kale and sprouts from March to May for a winter and spring crop, 1cm deep in a "
     "seedbed, then plant out 45cm apart once they have five or six leaves. Firm the soil hard "
     "around the stem. Net them straight away: pigeons strip a young brassica in a day, and "
     "cabbage white butterflies come later."),
    (("courgette", "courgettes", "zucchini", "squash", "pumpkin", "pumpkins"),
     "Sow courgettes from late April indoors and plant out in late May or June, once nights are "
     "above 10C, 90cm apart: one plant feeds a family. They need sun, rich soil and steady water. "
     "Pick them small, at 10-15cm, because a marrow-sized courgette stops the plant producing."),
    (("radish", "radishes"),
     "Sow radishes from March to September, a pinch every two weeks, 1cm deep and 2cm apart after "
     "thinning, and they are ready in about four weeks. They are the fastest thing in the veg "
     "patch and a good one to sow with children. Dry soil makes them hot and woody, so water "
     "them."),
    (("swede", "swedes", "turnip", "turnips"),
     "Sow swede in May to June and turnips from March to August, 1cm deep and 15cm apart once "
     "thinned; swede needs the whole summer to swell and is best lifted after the first frost. "
     "Club root is the risk in acid soil, so lime the bed the winter before if you have had it."),
    (("chilli", "chillies", "chillis", "chilli pepper", "chilli peppers", "hot pepper",
      "hot peppers", "jalapeno", "jalapenos", "scotch bonnet"),
     "Sow chillies indoors in February or March, half a centimetre deep, at 21C or more: cold seed "
     "does not come up at all, so a warm windowsill or a propagator is the whole trick. Pot them on "
     "as the roots fill the pot, pinch the top out at about 15cm to make a bush, and move them to "
     "the sunniest spot in June. Water when the top of the compost is dry and feed weekly with "
     "tomato feed once the flowers open; pick green for a milder chilli, or leave them to turn red."),
    (("pepper", "peppers", "sweet pepper", "sweet peppers", "bell pepper", "bell peppers",
      "pepper plant", "pepper plants"),
     "Sweet peppers want warmth and a long season: sow indoors in late February or March, half a "
     "centimetre deep, at 20C or more, and pot them on twice before planting out in June in the "
     "sunniest, most sheltered spot you have. Water regularly, because a plant that dries out drops "
     "its flowers, and feed weekly with tomato feed when the first fruit set. Pick them green, or "
     "wait for red, which is sweeter."),
    (("basil", "basil seed", "basil seeds", "basil plant", "basil plants"),
     "Sow basil indoors from late April to June, half a centimetre deep and barely covered, at "
     "20C or more: it sulks below 10C, so do not put it outside before June and even then keep it "
     "out of a cold wind. Pinch the tips out as it grows to keep it bushy, and sow a second pot in "
     "July so you have young plants when the first one goes woody."),
    (("parsley", "coriander", "cilantro", "dill", "chervil", "tarragon", "sage"),
     "Sow parsley, coriander and dill from March to July, 1cm deep, in a pot rather than a seedbed "
     "if you only want a windowsill's worth. Parsley is slow - two to three weeks - so keep the "
     "pot damp and be patient; coriander bolts in heat, so sow it little and often and pick the "
     "leaves young. Tarragon and sage are better bought as a plant."),
    (("mint", "mint plant", "mint plants", "mint root", "mint roots"),
     "Mint is not grown from seed: buy a plant, or pull up a piece of root with shoots on it in "
     "spring or autumn and pot it in fresh compost. Stand it in a pot with the rim above the soil, "
     "because a mint in a border takes over, and divide the pot every couple of years when the "
     "stems get thin."),
    (("rosemary", "thyme", "oregano", "oregano plant", "lavender"),
     "Rosemary, thyme and oregano are bought as small plants or grown from softwood cuttings in "
     "summer, not from seed: seed is slow and comes up uneven. They want sun, very free drainage - "
     "grit in the compost, or a gravel mulch - and far less water than basil; a woody herb in wet "
     "soil rots at the base."),
)

HERB_SOW_NOT = ("prune", "pruned", "pruning", "cut back", "cutting back", "cut", "cutting",
                "trim", "trimming", "pinch", "pinching", "pinch out", "pinching out", "deadhead",
                "deadheading", "woody", "leggy", "bolted", "bolting", "harvest", "harvesting",
                "look after", "looking after", "care", "care for", "caring", "keep alive",
                "keep it alive", "water", "watering", "watered",
                "keep", "keeps", "keeping",
                "repot", "repotting", "repotted", "pot on", "potting on", "potted on",
                "root bound", "rootbound", "pot bound", "potbound", "bigger pot")

PAN_VERBS = (
    "soak", "soaks", "soaked", "soaking",
    "rinse", "rinses", "rinsed", "rinsing",
    "defrost", "defrosts", "defrosted", "defrosting",
    "pickle", "pickles", "pickled", "pickling",
    "ferment", "ferments", "fermented", "fermenting",
    "mash", "mashes", "mashed", "mashing",
    "blitz", "blitzed", "blitzing",
    "stew", "stews", "stewed", "stewing",
    "curry", "curried",
    "grill", "grills", "grilled", "grilling",
    "barbecue", "barbecued", "barbecuing", "bbq",
    "preserve", "preserves", "preserved", "preserving",
    "chop", "chops", "chopped", "chopping",
    "grate", "grated", "grating",
    "stuff", "stuffed", "stuffing",
    "marinate", "marinates", "marinated", "marinating",
    "toast", "toasts", "toasted", "toasting",
)

PAN_KIT = (
    "oven", "ovens", "fan oven", "hob", "microwave", "microwaves", "microwave oven",
    "pressure cooker", "pressure cookers", "slow cooker", "slow cookers", "air fryer",
    "air fryers", "deep fat fryer", "deep fryer", "fryer", "fryers", "steamer", "steamers",
    "saucepan", "saucepans", "pan of water", "wok", "griddle", "grill pan", "soup maker",
    "rice cooker", "bread maker", "yoghurt maker", "thermomix", "halogen oven", "actifry",
    "sous vide", "casserole dish", "roasting tin", "baking tray", "tray bake",
)
A_PAN_LINE = PAN_VERBS + PAN_KIT

KITCHEN_WORDS = (
    "soup", "soups", "salad", "salads", "mash", "mashed", "roast", "roasted", "roasting",
    "boil", "boiled", "boiling", "fry", "fried", "frying", "chips", "crisps", "bake",
    "baked", "baking", "casserole", "curry", "stew", "pie", "gratin", "cream", "creamed",
    "creamy", "gravy", "sauce", "sauces", "salty", "bland", "tasty", "delicious", "grainy",
    "curdle", "curdled", "curdles", "recipe", "recipes", "cook", "cooked", "cooking",
    "dinner", "lunch", "supper", "side dish", "wedges", "puree", "pur\u00e9e", "saute",
    "sauteed", "steam", "steamed", "microwave", "air fryer", "overcooked", "undercooked",
    "went wrong", "too much", "not smooth",
    "soften", "softens", "softened", "softening", "tender", "tenderise", "tenderised",
    "simmer", "simmered", "simmering", "blanch", "blanched", "parboil", "parboiled",
    "brown in a pan", "brown the onions", "browned in", "browning in", "until crisp",
    "go crisp", "al dente", "stir fry",
    "stir fried", "saucepan", "pan", "pans", "hob", "drain", "drained", "draining",
    "piping hot", "portion", "portions", "side") + A_PAN_LINE

SOW_EXTRA_AVOID = {
    "basil": HERB_SOW_NOT,
    "parsley": HERB_SOW_NOT,
    "mint": HERB_SOW_NOT,
    "rosemary": HERB_SOW_NOT,
    "pepper": ("salt", "ground", "cracked", "black", "white", "peppercorn", "peppercorns",
               "add", "season", "seasoning", "stuffed", "sauce", "recipe", "recipes",
               "soup", "salad", "pizza", "roast", "cook", "cooking"),
    "chilli": ("sauce", "oil", "paste", "powder", "flakes", "con carne", "recipe",
               "recipes", "add", "season", "stuffed", "roast", "cook", "cooking",
               "too hot", "mild", "heat"),
}

_CROP_WEEKS = (
    (("spring onion", "spring onions"), "Spring onions are 8 to 10 weeks from seed."),
    (("sweetcorn", "sweet corn"), "Sweetcorn is 12 to 14 weeks from seed."),
    (("runner bean", "runner beans"), "Runner beans are 12 to 14 weeks from seed."),
    (("broad bean", "broad beans"), "Broad beans are 12 to 16 weeks from seed."),
    (("french bean", "french beans", "dwarf bean", "dwarf beans"),
     "French and dwarf beans are 10 to 12 weeks from seed."),
    (("salad leaves", "salad leaf", "salad"),
     "Salad leaves are 4 to 6 weeks from seed, and you pick the outer leaves as you go."),
    (("potato", "potatoes", "spud", "spuds", "tattie", "tatties"),
     "Potatoes are 10 to 12 weeks from planting for earlies and 18 to 20 for maincrop."),
    (("carrot", "carrots"), "Carrots are 12 to 16 weeks from seed."),
    (("parsnip", "parsnips"),
     "Parsnips are 22 to 24 weeks from seed, so they are most of a season."),
    (("beetroot",), "Beetroot is 10 to 12 weeks from seed."),
    (("radish", "radishes"), "Radishes are 4 to 6 weeks from seed, the quickest crop there is."),
    (("lettuce", "lettuces"),
     "Lettuce is 8 to 12 weeks from seed, and the cut-and-come-again leaves are 4 to 6."),
    (("spinach",), "Spinach is 6 to 10 weeks from seed, and it bolts in the heat of summer."),
    (("kale",), "Kale takes 10 to 12 weeks before the first pickings."),
    (("broccoli",), "Broccoli is 16 to 20 weeks from seed; sprouting broccoli takes a year."),
    (("cauliflower", "cauliflowers"), "Cauliflower is 16 to 20 weeks from seed."),
    (("cabbage", "cabbages"), "Cabbages are 16 to 20 weeks from seed, depending on the sort."),
    (("sprouts", "brussels", "brussel"), "Brussels sprouts are 20 to 24 weeks from seed."),
    (("swede",), "Swede is 20 to 24 weeks from seed."),
    (("turnip", "turnips"), "Turnips are 6 to 8 weeks from seed."),
    (("courgette", "courgettes", "marrow", "marrows"),
     "Courgettes are 10 to 12 weeks from seed, and then they do not stop."),
    (("pumpkin", "pumpkins", "squash"), "Pumpkins are 16 to 20 weeks from seed."),
    (("cucumber", "cucumbers"), "Cucumbers are 8 to 12 weeks from seed under cover."),
    (("tomato", "tomatoes"),
     "Tomatoes are 16 to 20 weeks from seed, or 12 to 16 from planting out."),
    (("chilli", "chillies", "chili", "chilis"),
     "Chillies are 16 to 20 weeks from seed, and they want warmth all of that time."),
    (("aubergine", "aubergines"), "Aubergines are 16 to 20 weeks, and want a warm summer."),
    (("pepper", "peppers"), "Peppers are 16 to 20 weeks from seed."),
    (("pea", "peas", "mangetout"), "Peas are 12 to 14 weeks from seed."),
    (("bean", "beans"), "Beans are 10 to 16 weeks from seed, the dwarf sorts quickest."),
    (("garlic",), "Garlic is about eight months from an autumn clove: plant in October and lift "
                  "in July."),
    (("strawberry", "strawberries"),
     "Strawberries fruit the summer after planting, so about a year from a new plant."),
    (("onion", "onions", "leek", "leeks", "shallot", "shallots"),
     "Onions and leeks are 20 to 24 weeks from seed, or about 20 weeks from sets."),
)

_CROP_WEEKS_REST = (
    "The others, from seed: salad leaves and radishes 4 to 6 weeks, beetroot 10 to 12, carrots "
    "and runner beans 12 to 16, peas 12 to 14, courgettes 10 to 12, sweetcorn 12 to 14, tomatoes "
    "16 to 20 from sowing (12 to 16 from planting out), cabbages and broccoli 16 to 20, parsnips "
    "22 to 24, and leeks or onions 20 to 24. Garlic takes about eight months from an autumn clove, "
    "and strawberries fruit the summer after planting. The seed packet is the tie-breaker, "
    "because a fortnight either way is normal."
)


def _crop_weeks_reply(memory, reading):
    said = " " + str(reading.get("plain") or reading.get("norm_text")
                     or reading.get("text") or "").lower() + " "
    words = set(reading.get("words") or ())
    for forms, lead in _CROP_WEEKS:
        if any(" " + form + " " in said for form in forms) or words & set(forms):
            return lead + " " + _CROP_WEEKS_REST
    return _CROP_WEEKS_REST


SOW_ENTRIES = [
    entry("sow-" + words[0], (words, SOW_ASK), _sowing_reply(words[0], reply),
          avoid=SOW_NOT + HARVEST_ASK + KITCHEN_WORDS + SOW_EXTRA_AVOID.get(words[0], ()), bias=1)
    for words, reply in SOWING
] + _harvest_entries() + [
    entry("sow-month", (("sow", "sowing", "sowed", "plant", "planting", "grow", "growing",
                         "seed", "seeds", "put in"),
                        tuple(MONTH_NUMBER) + ("in may", "of may", "by may", "during may",
                                               "this may", "next may", "now", "this month",
                                               "next month", "autumn", "spring", "winter",
                                               "summer", "next year",
                                               "at the moment", "at the minute",
                                               "these days", "this time of year",
                                               "in spring", "in the spring", "this spring",
                                               "next spring", "for spring", "of spring",
                                               "in summer", "in the summer", "this summer",
                                               "next summer", "for summer", "of summer",
                                               "in autumn", "in the autumn", "this autumn",
                                               "next autumn", "for autumn", "of autumn",
                                               "in winter", "in the winter", "this winter",
                                               "next winter", "for winter", "of winter",
                                               "over winter", "over the winter",
                                               "before winter", "for christmas")),
          _sow_month,
          ask=("what", "which", "can i", "could i", "anything", "what else", "when", "best",
               "now", "should i"),
          avoid=("harvest", "harvesting", "lift", "dig up", "pick", "picking", "cut", "ready",
                 "ripe", "prune", "pruning", "cutting", "cuttings", "lawn", "grass", "mow",
                 "weed", "weeds", "sick", "yellow", "yellowing", "dying", "blight", "frost",
                 "sprout", "flower", "flowers", "bulb", "bulbs", "rose", "roses", "tomato",
                 "tomatoes",
                 "herb", "herbs", "herb pot", "houseplant", "houseplants", "house plant",
                 "house plants", "indoor", "indoors", "inside", "windowsill", "window sill",
                 "greenhouse", "green house", "propagator", "patio", "balcony",
                 "window box", "window boxes", "hanging basket"),
          bias=2),
]


SOW_WINDOW.update({"daffodil": (9, 12), "hyacinth": (9, 12), "crocus": (9, 11),
                   "snowdrop": (1, 3), "allium": (9, 11), "tomato": (3, 6),
                   "grass seed": (3, 10), "strawberry": (3, 10), "sweet pea": (2, 11),
                   "clematis": (9, 11)})

PLANT_NOT = SOW_NOT + HARVEST_ASK + (
    "cut", "cutting", "prune", "pruning", "trim", "trimming", "mow", "mowing", "deadhead",
    "deadheading", "feed", "feeding", "fertilise", "fertiliser", "fertilizer", "stake", "staking",
    "blossom", "blossoms", "blossoming", "flower", "flowering", "flowers", "bloom", "blooms",
    "buds", "catkins", "pollen",
    "move", "moving", "moved", "transplant", "transplanting", "relocate", "relocating",
    "rash", "hives", "itch", "itchy", "itching", "allergic", "allergy", "allergies",
    "swollen", "swelling", "sick", "vomit", "vomiting", "diarrhoea", "stomach", "throat",
    "breathless", "bloated", "bloating", "reaction", "anaphylaxis", "cramps")

PLANTING = (
    (("daffodil", "daffodils", "hyacinth", "hyacinths", "crocus", "snowdrop", "snowdrops",
      "allium", "alliums", "spring bulbs"),
     "Spring bulbs go in from September to November while the soil is still warm: three times the "
     "bulb's own height deep, 10cm apart for daffodils and 8cm for crocuses, pointy end up. They "
     "need a cold spell to flower, so a mild autumn is fine. Leave the leaves on for six weeks "
     "after flowering and they come back every year."),
    (("sweet pea", "sweet peas"),
     "Sow sweet peas in October for the strongest plants, or February to March under cover, 2cm "
     "deep in deep pots so the root runs straight down. Pinch out the growing tip after two pairs "
     "of leaves, harden them off, and plant out in April. Keep picking, because once they set seed "
     "they stop flowering."),
    (("strawberry", "strawberries", "strawberry plants"),
     "Plant strawberries in late summer, August to September, for a full crop the next June - a "
     "spring planting gives you a handful the same year and nothing much the next. 45cm apart with "
     "the crown level with the soil and the roots spread, straw under the fruit, and replace the "
     "plants every three years, when the crop shrinks and virus builds up."),
    (("grass seed", "lawn seed", "grass"),
     "Sow grass seed in September, or early April if you missed it: warm damp soil, weeds not yet "
     "up, and enough time to root before winter. Scatter 35g to the square metre, rake it in "
     "lightly, and keep it damp for a fortnight with a light sprinkle morning and evening rather "
     "than a soak."),
    (("tomato", "tomatoes", "tomato plants"),
     "Sow tomatoes indoors in March or April and plant them out in early June, once nights stay "
     "above 10C: 45cm apart, or one to a grow bag, burying the stem up to its first leaves. "
     "Harden them off over a week first - a cold night sets a tomato back a month."),
    (("tree", "trees", "fruit tree", "bare root", "bare-root", "shrub", "shrubs", "hedge",
      "hedges", "clematis", "climber", "climbers", "wisteria"),
     "Bare-root trees and shrubs go in from November to March while they are dormant, and potted "
     "ones any time the ground is not frozen or waterlogged. Dig a square hole twice the width of "
     "the roots, keep the soil mark on the stem at the same level, firm it in well and water it "
     "through its first summer. Autumn planting beats spring: the roots work all winter."),
    (("rose", "roses", "bare root rose", "climbing rose", "shrub rose"),
     "Plant bare-root roses from November to March, while they are dormant, or potted ones any "
     "month the ground is not frozen: a hole wide enough to spread the roots, the graft union an "
     "inch below soil level, firmed in hard. They want sun and rich soil, and a feed in March and "
     "again in July is what keeps them flowering."),
)

PRUNE_NOT = SOW_NOT + HARVEST_ASK + (
    "blossom", "blossoms", "blossoming", "flower", "flowering", "flowers", "bloom", "blooms",
    "buds", "catkins", "pollen", "feed", "feeding", "plant", "planting", "planted", "move",
    "moving", "transplant", "transplanting")

PRUNE_APPLE = ("Prune apples and pears in January or February while they are dormant: dead, "
               "diseased and crossing branches out first, then the oldest third of the stems, "
               "and the middle kept open.")
PRUNE_STONE = ("Prune plums, cherries and damsons in June, not in winter: silver leaf gets in "
               "through a winter cut and kills a branch a year later. Cut back to a growing shoot "
               "and leave the pruning cuts open to the air rather than painting them.")


def _prune_reply(memory, understood):
    line = _words(understood)
    if re.search(r"\bplum|\bcherr|\bdamson", line):
        return PRUNE_STONE + " " + PRUNE_APPLE
    return PRUNE_APPLE + " " + PRUNE_STONE


PRUNE_BUDDLEIA = (
    "Cut a buddleia hard in March, back to about 30cm: it flowers on the shoots that grow from "
    "there, so the harder you cut the bigger the spikes. Do it every year, and take out any dead "
    "stems at the base at the same time. A neglected one can lose two thirds of its height at "
    "once and still come back.")

PRUNE_WISTERIA = (
    "Wisteria is pruned twice: in July or August shorten the long whippy shoots to five or six "
    "leaves, then in January cut those same shoots back to two or three buds. That is what turns "
    "growth into flowers. Leave any shoot you are training out longer, and do not feed it with "
    "nitrogen, which gives you leaves instead.")

PRUNE_HYDRANGEA = (
    "Leave the old flowers on over winter for frost protection, then in March cut each stem back "
    "to a fat pair of buds about 30cm up and take out the oldest stems at the base. Do not cut a "
    "mophead to the ground: it flowers on last year's wood. A paniculata kind is the exception "
    "and flowers best cut hard in spring.")

PRUNE_EVERGREEN = (
    "Trim an evergreen shrub in mid to late spring, once the frosts are over: bay, holly, laurel "
    "and box all take a tidy-up then, and bay takes a light trim in August too. Do not cut back "
    "into bare old wood, because most evergreens will not shoot again from it - a hard cut is "
    "better spread over two years.")

PRUNE_RASPBERRY = (
    "Summer-fruiting raspberries: cut the canes that fruited this year down to the ground in "
    "February and tie in the new ones. Autumn-fruiting ones are easier, because every cane is cut "
    "to the ground in February and the fruit comes on the new growth the same year. Take out the "
    "weak and crowded canes either way.")

PRUNE_LATER = (
    "Prune it in late winter or early spring, around March, while it is dormant: it flowers on the "
    "shoots that grow this year, so cutting it back then gives the strongest growth and the most "
    "flower. Take out dead and crossing stems first, then up to a third of the oldest stems at "
    "the base.")

PRUNE_EARLIER = (
    "Prune it straight after it has flowered, not in winter: it made this year's flower buds last "
    "summer, so a spring cut takes the flowers with it. Take the flowered shoots back by about a "
    "third as the blooms fade, and leave the rest of the growth alone until next year.")

PRUNE_NAMED = (
    (r"buddleia|buddleja", PRUNE_BUDDLEIA),
    (r"wisteria", PRUNE_WISTERIA),
    (r"hydrangea", PRUNE_HYDRANGEA),
    (r"raspberr", PRUNE_RASPBERRY),
    (r"\bbay\b|laurel|holly|box\b|evergreen|photinia|pieris", PRUNE_EVERGREEN),
    (r"forsythia|weigela|philadelphus|mock orange|deutzia|kerria|ribes", PRUNE_EARLIER),
    (r"cotoneaster|spirea|ceanothus|hebe|buddleia", PRUNE_LATER),
)


def _prune_shrub(memory, understood):
    line = _words(understood)
    for shape, reply in PRUNE_NAMED:
        if re.search(shape, line):
            return reply
    return ("Shrubs want one of two dates. If it flowers before midsummer, cut it just after "
            "flowering, because the buds were made last year. If it flowers later, cut it in "
            "March while it is dormant, because the flowers come on the new growth. Take out "
            "dead and crossing stems first, then a third of the oldest at the base.")


PLANT_AVOID = {
    "sow-tomato": PLANT_NOT + ("plant", "planting", "planted", "grow", "growing", "grown",
                               "pot", "pots", "grow bag", "greenhouse"),
    "sow-tree": tuple(word for word in PLANT_NOT if word != "small"),
}

PLANT_LATE = {
    "daffodil": ("November is the last good month, so go now: planted in December a bulb still "
                 "flowers, just later and smaller. "),
}


def _planting_reply(name, reply):
    answer = _sowing_reply(name, reply)
    late = PLANT_LATE.get(name)
    if not late:
        return answer

    def with_late(memory, understood):
        if re.search(r"\btoo late\b|\btoo early\b|\blate for\b", _words(understood)):
            return late + reply
        return answer(memory, understood)

    return with_late


SOW_PLANT_CARE = (
    ("monstera", ("monstera", "monsteras", "swiss cheese plant", "cheese plant"),
     "Water a monstera when the top 2 to 3cm of compost is dry, which is about once a week in "
     "summer and every two weeks in winter. Give it bright light out of direct sun, and don't "
     "worry when water drips from the leaf tips for an hour afterwards: that is the plant pushing "
     "out moisture, not a problem."),
    ("pothos", ("pothos", "devil's ivy", "devils ivy", "devil ivy"),
     "Water a pothos about once a week, when the compost is dry and the leaves are just starting "
     "to look limp: it forgives a missed week but rots in a pot that never dries. It grows in "
     "almost any light, and a cutting in a glass of water roots in a few weeks."),
    ("snake-plant", ("snake plant", "snake plants", "sansevieria", "mother in laws tongue"),
     "Water a snake plant every two to three weeks in summer and once a month or less in winter, "
     "and only when the compost is dry all the way down. It stores water in its leaves and rots "
     "in wet soil, so the surest way to kill one is to water it on a schedule."),
    ("spider-plant", ("spider plant", "spider plants"),
     "Water a spider plant about once a week, when the top of the compost is dry, and let the pot "
     "drain. Brown tips are usually tap water or dry air rather than a watering fault: trim them "
     "off and stand the pot somewhere less dry."),
    ("peace-lily", ("peace lily", "peace lilies", "spathiphyllum"),
     "Water a peace lily when the compost is just dry, about once a week, and it will tell you "
     "when it wants more by drooping: it picks itself up within a few hours of a drink. It likes "
     "a bright spot out of direct sun and brown leaf tips mean the water or the air is hard."),
    ("fiddle-leaf-fig", ("fiddle leaf fig", "fiddle fig", "fiddle leaf"),
     "Water a fiddle leaf fig when the top 3cm of soil is dry, which is about every ten days, and "
     "let it drain right through. It sulks if it is moved or sits in a draught, and brown blotches "
     "on the leaves are usually too much water rather than too little."),
    ("zz-plant", ("zz plant", "zz plants", "zamioculcas"),
     "Water a ZZ plant every two to three weeks in summer and once a month in winter. Its thick "
     "underground stems hold water, so it survives neglect far better than kindness: yellow "
     "leaves that fall off are the sign of too much."),
    ("aloe", ("aloe", "aloe vera"),
     "Water an aloe every two to three weeks in summer and once a month in winter, soaking the pot "
     "and then letting it dry out completely. Leaves going soft and pale at the base mean the "
     "compost has stayed wet."),
    ("cactus", ("cactus", "cacti", "cactuses"),
     "Water a cactus every two to three weeks in summer, and barely at all from November to "
     "March. Soak it, let it dry right out, and never leave the pot standing in water: more cacti "
     "die of watering than of neglect."),
    ("succulent", ("succulent", "succulents"),
     "Water a succulent by soaking the pot and then letting it dry out completely: every two to "
     "three weeks in summer, monthly in winter. The leaves going soft and see-through at the base "
     "is rot from wet compost, and shrivelled leaves are the sign it wants a drink."),
    ("orchid", ("orchid", "orchids", "moth orchid", "phalaenopsis"),
     "Water an orchid by standing the pot in tepid water for ten minutes once a week, then letting "
     "it drain: it lives in bark, not compost, so a normal watering can runs straight through. "
     "Roots that are silver want water and roots that are green have had enough."),
    ("fern", ("fern", "ferns", "boston fern", "maidenhair fern"),
     "Water a fern when the compost is barely dry, which is twice a week in summer, and stand the "
     "pot on pebbles in a saucer of water for the humidity. Crispy brown fronds are dry air, not "
     "thirst: a bathroom or a kitchen suits most ferns better than a windowsill."),
    ("rubber-plant", ("rubber plant", "rubber plants", "ficus elastica"),
     "Water a rubber plant every week to ten days, when the top 3cm of compost is dry, and wipe "
     "the leaves so the dust doesn't block the light. Dropping lower leaves one at a time is "
     "usually a cold draught or a sudden move."),
    ("jade-plant", ("jade plant", "jade plants"),
     "Water a jade plant every two to three weeks in summer and once a month in winter, and let "
     "the compost dry between waterings. It wants a sunny windowsill and shrivelled leaves mean "
     "thirst while soft, dropping leaves mean too much water."),
    ("calathea", ("calathea", "prayer plant"),
     "Water a calathea when the top of the compost is just dry, about twice a week in summer, and "
     "keep it out of direct sun. Curling leaves and brown edges are dry air: a tray of wet pebbles "
     "or a bathroom does more for it than more water does."),
)

PLANT_CARE = (
    ("monstera", ("monstera", "monsteras", "swiss cheese plant", "cheese plant"),
     "Water a monstera when the top 2 to 3cm of compost is dry, which is about once a week in "
     "summer and every two weeks in winter. Give it bright light out of direct sun, and don't "
     "worry when water drips from the leaf tips for an hour afterwards: that is the plant pushing "
     "out moisture, not a problem."),
    ("pothos", ("pothos", "devil's ivy", "devils ivy", "devil ivy"),
     "Water a pothos about once a week, when the compost is dry and the leaves are just starting "
     "to look limp: it forgives a missed week but rots in a pot that never dries. It grows in "
     "almost any light, and a cutting in a glass of water roots in a few weeks."),
    ("snake-plant", ("snake plant", "snake plants", "sansevieria", "mother in laws tongue"),
     "Water a snake plant every two to three weeks in summer and once a month or less in winter, "
     "and only when the compost is dry all the way down. It stores water in its leaves and rots "
     "in wet soil, so the surest way to kill one is to water it on a schedule."),
    ("spider-plant", ("spider plant", "spider plants"),
     "Water a spider plant about once a week, when the top of the compost is dry, and let the pot "
     "drain. Brown tips are usually tap water or dry air rather than a watering fault: trim them "
     "off and stand the pot somewhere less dry."),
    ("peace-lily", ("peace lily", "peace lilies", "spathiphyllum"),
     "Water a peace lily when the compost is just dry, about once a week, and it will tell you "
     "when it wants more by drooping: it picks itself up within a few hours of a drink. It likes "
     "a bright spot out of direct sun and brown leaf tips mean the water or the air is hard."),
    ("fiddle-leaf-fig", ("fiddle leaf fig", "fiddle fig", "fiddle leaf"),
     "Water a fiddle leaf fig when the top 3cm of soil is dry, which is about every ten days, and "
     "let it drain right through. It sulks if it is moved or sits in a draught, and brown blotches "
     "on the leaves are usually too much water rather than too little."),
    ("zz-plant", ("zz plant", "zz plants", "zamioculcas"),
     "Water a ZZ plant every two to three weeks in summer and once a month in winter. Its thick "
     "underground stems hold water, so it survives neglect far better than kindness: yellow "
     "leaves that fall off are the sign of too much."),
    ("aloe", ("aloe", "aloe vera"),
     "Water an aloe every two to three weeks in summer and once a month in winter, soaking the pot "
     "and then letting it dry out completely. Leaves going soft and pale at the base mean the "
     "compost has stayed wet."),
    ("cactus", ("cactus", "cacti", "cactuses"),
     "Water a cactus every two to three weeks in summer, and barely at all from November to "
     "March. Soak it, let it dry right out, and never leave the pot standing in water: more cacti "
     "die of watering than of neglect."),
    ("succulent", ("succulent", "succulents"),
     "Water a succulent by soaking the pot and then letting it dry out completely: every two to "
     "three weeks in summer, monthly in winter. The leaves going soft and see-through at the base "
     "is rot from wet compost, and shrivelled leaves are the sign it wants a drink."),
    ("orchid", ("orchid", "orchids", "moth orchid", "phalaenopsis"),
     "Water an orchid by standing the pot in tepid water for ten minutes once a week, then letting "
     "it drain: it lives in bark, not compost, so a normal watering can runs straight through. "
     "Roots that are silver want water and roots that are green have had enough."),
    ("fern", ("fern", "ferns", "boston fern", "maidenhair fern"),
     "Water a fern when the compost is barely dry, which is twice a week in summer, and stand the "
     "pot on pebbles in a saucer of water for the humidity. Crispy brown fronds are dry air, not "
     "thirst: a bathroom or a kitchen suits most ferns better than a windowsill."),
    ("rubber-plant", ("rubber plant", "rubber plants", "ficus elastica"),
     "Water a rubber plant every week to ten days, when the top 3cm of compost is dry, and wipe "
     "the leaves so the dust doesn't block the light. Dropping lower leaves one at a time is "
     "usually a cold draught or a sudden move."),
    ("jade-plant", ("jade plant", "jade plants"),
     "Water a jade plant every two to three weeks in summer and once a month in winter, and let "
     "the compost dry between waterings. It wants a sunny windowsill and shrivelled leaves mean "
     "thirst while soft, dropping leaves mean too much water."),
    ("calathea", ("calathea", "prayer plant"),
     "Water a calathea when the top of the compost is just dry, about twice a week in summer, and "
     "keep it out of direct sun. Curling leaves and brown edges are dry air: a tray of wet pebbles "
     "or a bathroom does more for it than more water does."),
)


PLANT_CARE_WORDS = ("water", "watering", "watered", "how often", "how much", "care",
                    "care for", "look after", "keep alive", "light", "sun", "repot", "root rot",
                    "overwatered", "overwatering", "underwatered", "soak", "soaking",
                    "keep", "keeping", "alive", "thriving", "healthy",
                    "dying", "die", "dies", "drooping", "droopy")

LIGHT_QUESTION = ("light", "sun", "sunlight", "sunny", "sunshine", "shade", "shady",
                           "bright", "direct sun", "low light", "dark", "window", "windowsill",
                           "south facing", "north facing", "east facing", "west facing",
                           "full sun", "part shade")


A_PERSON_CARED_FOR = (r"(?:mum|mums|mother|mothers|dad|dads|father|fathers|parent|parents|"
                      r"son|sons|daughter|daughters|child|children|kid|kids|baby|babies|"
                      r"newborn|newborns|infant|infants|toddler|husband|husbands|wife|wives|"
                      r"partner|partners|boyfriend|"
                      r"girlfriend|brother|brothers|sister|sisters|gran|grans|grandma|"
                      r"grandmas|grandad|grandads|nan|nans|aunt|aunty|auntie|uncle|uncles|"
                      r"cousin|cousins|friend|friends|neighbour|neighbours|relative|"
                      r"relatives|carer|carers|elderly|pensioner|pensioners)")
A_PERSON_CARED_FOR_BY_PRONOUN = re.compile(
    r"\b(?:care|cares|cared|caring|look|looks|looking|take|takes|taking|took)\s+"
    r"(?:after|for|of)\s+(?:me|us|him|her|them)\b")
CARE_FOR_A_PERSON = re.compile(
    r"\b(?:care|cares|cared|caring|look|looks|looking|take|takes|taking|took)\s+"
    r"(?:after|for|of)\s+(?:my|our|his|her|their|the|a|an)?\s*" + A_PERSON_CARED_FOR + r"\b"
    r"|" + A_PERSON_CARED_FOR_BY_PRONOUN.pattern)
A_PERSON_NEEDING_CARE = re.compile(
    r"\b(?:my|our|his|her|their)\s+" + A_PERSON_CARED_FOR
    + r"\b[^.!?]*\b(?:care|carers?|look after|looking after|help|needs help)\b")
A_PET_CARED_FOR = (r"(?:dog|dogs|puppy|puppies|pup|pups|cat|cats|kitten|kittens|kitty|moggy|"
                   r"rabbit|rabbits|bunny|bunnies|hamster|hamsters|guinea pig|guinea pigs|"
                   r"gerbil|gerbils|rat|rats|mouse|mice|parrot|parrots|budgie|budgies|"
                   r"fish|goldfish|horse|horses|pony|ponies|tortoise|tortoises|reptile|reptiles|"
                   r"snake|snakes|lizard|lizards|pet|pets|animal|animals|puppies)")
CARE_FOR_A_PET = re.compile(
    r"\b(?:care|cares|cared|caring|look|looks|looking|take|takes|taking|took)\s+"
    r"(?:after|for|of)\s+(?:my|our|his|her|their|the|a|an)?\s*" + A_PET_CARED_FOR + r"\b")
A_PLANT_IN_THE_LINE = re.compile(
    r"\b(?:plants?|house ?plants?|pot plants?|indoor plants?|monstera|orchid|fern|cactus|"
    r"succulent|peace lily|spider plant|snake plant|pothos|calathea|zz plant|dracaena|yucca|"
    r"fiddle leaf|rubber plant|poinsettia|cyclamen|amaryllis|african violet|aloe|jade plant|"
    r"anthurium|kalanchoe|begonia|hyacinth|flowers?|shrubs?|trees?|garden|compost|leaves|"
    r"seeds?|bulbs?|lawn|hedge)\b")


def _the_care_is_for_a_person(understood):
    said = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    said = said.replace("\u2019", "'")
    if A_PLANT_IN_THE_LINE.search(said):
        return True
    if CARE_FOR_A_PERSON.search(said):
        return False
    if CARE_FOR_A_PET.search(said):
        return False
    return not A_PERSON_NEEDING_CARE.search(said)


_A_GARDEN_THING = ("plant", "plants", "garden", "gardens", "greenhouse", "seedling",
                  "seedlings", "pot", "pots", "flower", "flowers", "shrub", "shrubs",
                  "bush", "bushes", "bedding", "tender", "cutting", "cuttings",
                  "allotment", "polytunnel", "grow bag", "grow bags", "basket", "baskets",
                  "veg", "vegetables", "crop", "crops", "tomato", "tomatoes", "tree",
                  "trees", "fern", "ferns", "citrus", "olive", "herb", "herbs",
                  "cloche", "cloches", "plot", "border", "borders", "hanging basket")


def _a_winter_pond_line(understood):
    line = _words(understood)
    return any(_has(line, word) for word in
               ("freeze", "freezes", "freezing", "frozen", "ice", "iced", "icy", "winter",
                "winters", "wintertime", "overwinter", "overwintering", "winterise",
                "winterised", "winterising", "winterize", "cold", "snow", "frost"))


def _a_christmas_tree(understood):
    line = _words(understood)
    if any(_has(line, word) for word in ("christmas", "xmas", "spruce", "fir", "nordmann",
                                         "needles", "needle", "tinsel", "decorations")):
        return True
    return not any(_has(line, word) for word in _A_GARDEN_THING)


def _garden_tree(memory, understood):
    line = _words(understood)
    if _has(line, "water") or _has(line, "watering") or _has(line, "how often") \
            or _has(line, "soak"):
        return ("A tree that is in its first two summers needs a proper soak of about ten litres "
                "a week, poured slowly round the roots so it sinks in, and more in a dry spell - "
                "a sprinkle from a hose wets the top inch and the roots stay shallow and thirsty. "
                "Water in the morning or the evening rather than in the middle of a hot day, and "
                "aim at the soil, not the leaves. After that a tree is on its own unless there "
                "are months without rain, when the leaves going dull and curling upwards is the "
                "sign it wants a drink. A potted tree dries out far faster and needs checking "
                "every few days in summer.")
    if _has(line, "prune") or _has(line, "pruning") or _has(line, "cut back") \
            or _has(line, "shape"):
        return ("Prune a tree in late winter while it is dormant, when the sap is down and the "
                "wound heals fast: take out the dead, the damaged and the crossing branches "
                "first, then any that rub or grow in towards the middle, and leave the rest. Do "
                "not top it or cut the leader out of the top, because that is what turns a tree "
                "into a bush of water shoots. Take out no more than a quarter of the crown in a "
                "year, cut back to a bud or a branch rather than leaving a stub, and leave "
                "anything that flowers on old wood - plum, cherry, magnolia - until just after "
                "it has flowered.")
    return ("Choose it for the space it will need in twenty years, not the one it needs now: the "
            "label gives a height and a spread, and most disappointment with trees is a tree "
            "planted at a third of its final width against a fence. Keep it well away from a "
            "house wall, the drains and the path, because roots go as wide as the branches, and "
            "check the soil and the light where it is going: a tree that wants acid soil sulks in "
            "chalk and one that wants sun goes thin in shade. Plant bare-root between November "
            "and March while it is dormant - it is cheaper, and it settles far better than a "
            "potted one in leaf. Dig a hole two or three times as wide as the roots and no "
            "deeper than the soil mark on the trunk, spread the roots, and put the stake in "
            "before the tree so the root ball is not speared. Firm it in, water it well, mulch "
            "round the base but leave a clear gap against the trunk, and give it a good soak "
            "every week or two through the first two summers, because that is what turns a "
            "stick into a tree.")


def _a_garden_tree(understood):
    line = _words(understood)
    if any(_has(line, word) for word in ("christmas", "xmas", "spruce", "fir", "nordmann")):
        return False
    return any(_has(line, word) for word in ("tree", "trees", "sapling", "saplings"))


def _a_summer_pond_line(understood):
    line = _words(understood)
    return not any(_has(line, word) for word in
                   ("freeze", "freezes", "freezing", "frozen", "ice", "iced", "icy", "winter",
                    "winters", "overwinter", "winterise", "winterize", "cold", "snow",
                    "frost"))


def _the_person_is_sad_too(understood):
    return str((understood or {}).get("state_owner") or "") != "self"


def _plant_entries():
    return [entry(f"plant-{name}", (aliases, PLANT_CARE_WORDS), reply, bias=1,
                  avoid=LIGHT_QUESTION, guard=_the_care_is_for_a_person)
            for name, aliases, reply in PLANT_CARE]


PLANT_ASK_EXTRA = {"sow-tree": ("bought", "buy", "buying", "picked up", "came home with",
                                "brought home", "arrived", "delivered", "new tree", "new shrub",
                                "in a pot", "bare root", "bare-root", "root ball"),
                   "sow-rose": ("bought", "buy", "buying", "picked up", "came home with",
                                "brought home", "arrived", "delivered", "new rose",
                                "in a pot", "bare root", "bare-root")}

SOW_ENTRIES = SOW_ENTRIES + [
    entry("sow-" + words[0],
          (words, SOW_ASK + PLANT_ASK_EXTRA.get("sow-" + words[0], ())),
          _planting_reply(words[0], reply),
          avoid=PLANT_AVOID.get("sow-" + words[0], PLANT_NOT), bias=1)
    for words, reply in PLANTING
]

SOW_ENTRIES.append(
    entry("sow-fruit-prune", (("apple tree", "apple", "apple trees", "pear", "pears", "pear tree",
                               "plum", "plums", "plum tree", "cherry", "cherries", "cherry tree",
                               "damson", "damsons", "fruit tree", "fruit trees"),
                              SOW_ASK),
          _prune_reply, avoid=PRUNE_NOT, bias=1))

SOW_ENTRIES.append(
    entry("roses-flower", (("rose", "roses", "rose bush", "rose bushes"),
                           ("flower", "flowers", "flowering", "bloom", "blooms", "in flower")),
          "Roses flower from June into the first frosts: a first flush in June, then waves if you "
          "keep deadheading. Cut each spent flower back to a strong shoot rather than just taking "
          "the petals, and a feed after the first flush is what brings the second one on.",
          bias=1))

BOUGHT_BUSH = ("blueberry", "blueberries", "blackberry", "blackberries", "blackcurrant",
               "blackcurrants", "redcurrant", "redcurrants", "whitecurrant", "whitecurrants",
               "gooseberry", "gooseberries", "raspberry", "raspberries", "loganberry",
               "loganberries", "tayberry", "tayberries", "honeyberry", "honeyberries",
               "bush", "bushes", "cane", "canes", "bare root", "bare-root", "root ball")
SOW_ENTRIES.append(
    entry("bought-fruit-bush", (BOUGHT_BUSH,
                                ("bought", "buy", "buying", "picked up", "came home with",
                                 "brought home", "arrived", "delivered", "got it home",
                                 "how do i plant", "how deep", "where do i plant",
                                 "planted", "planting", "going in")),
          "Plant it while the roots are still damp: stand the pot or the bare roots in a bucket of "
          "water for an hour, dig a hole twice as wide as the pot and the same depth, and set the "
          "plant so the old soil mark sits level with the ground. Blueberries and cranberries want "
          "ericaceous compost and rainwater rather than tap water; currants, gooseberries, "
          "raspberries and blackberries are happy in ordinary soil in sun or half shade. Firm it "
          "in with your heel, water it well, and pick the flowers off in the first year so the "
          "roots get going instead of the fruit.",
          avoid=("prune", "pruning", "pruned", "cut back", "dying", "dead", "died", "rot",
                 "rotting", "mould", "mold", "mildew", "jam", "cook", "recipe", "wine", "pie",
                 "crumble", "freeze", "glut"),
          bias=1))

GROW_ASK = ("how do i grow", "how to grow", "how do you grow", "how can i grow",
            "how should i grow", "how would i grow", "best way to grow", "way to grow",
            "want to grow", "trying to grow", "going to grow", "grow my own", "grow your own",
            "start growing", "start to grow", "can i grow", "could i grow", "do i grow",
            "to grow", "growing", "grow")
GROW_NOT = PLANT_NOT + (
    "not growing", "isnt growing", "isn't growing", "arent growing", "are not growing",
    "stopped growing", "no growth", "wont grow", "won't grow", "dont grow", "don't grow",
    "didnt grow", "didn't grow", "hasnt grown", "hasn't grown", "came up", "come up",
    "nothing came up", "faster", "quickly", "bigger", "taller", "more fruit",
    "shoots", "shooting", "chit", "chitting",
    "more fruit", "too big", "salt", "ground", "black pepper", "peppercorn", "peppercorns",
    "recipe", "recipes", "add", "season", "stuffed", "sauce", "soup", "salad", "roast",
    "cook", "cooking", "bake", "flakes", "oil", "paste", "powder", "buy", "price",
    "cost", "shop", "supermarket")
OTHER_CROPS = ("strawberry", "strawberries", "potato", "potatoes", "spud", "spuds",
               "courgette", "courgettes", "zucchini", "chilli", "chillies", "chilli pepper",
               "pepper", "peppers", "lettuce", "carrot", "carrots", "onion", "onions",
               "pea", "peas", "bean", "beans", "beetroot", "radish", "radishes", "kale",
               "cabbage", "broccoli", "cauliflower", "sprouts", "garlic", "parsnip",
               "parsnips", "leek", "leeks", "squash", "pumpkin", "pumpkins", "cucumber",
               "cucumbers", "herb", "herbs", "spinach", "rocket", "swede", "turnip",
               "turnips", "salad", "salad leaves", "cress", "basil", "mint", "parsley",
               "chard", "celery")

THE_DRY_WHY = (
    "A raised bed, a pot and a sandy border all lose water faster than a clay border does: the "
    "compost drains freely, sun and wind take it off the surface, and roots that have filled the "
    "pot drink what is left. Water until it runs out of the bottom and check a spade's depth down "
    "before deciding it is dry, then spread 5cm of compost or bark over the surface - that mulch "
    "is what stops the next lot evaporating, and a light sprinkle every day never reaches the "
    "roots at all.")
THE_DRY_HOW_OFTEN = (
    "Water deeply and less often, in the evening or early morning: a good soak twice a week "
    "in a dry spell beats a light sprinkle every day, because it reaches the roots instead of "
    "wetting the surface. Aim at the soil, not the leaves. Established shrubs, borders and "
    "perennials need nothing until the soil is dry a spade's depth down, while anything newly "
    "planted and anything in a pot is the exception and wants water every day or two in heat.")


_DRY_IS_A_VERB = re.compile(
    r"\b(?:how (?:do|can|should|would) i|how to|way to|best way to|want to|need to|trying to"
    r"|is it (?:ok|okay|safe) to|can i)\s+(?:dry|drying)\b(?!\s+out\b)")


def _a_bed_that_dries_out(memory, understood):
    said = _words(understood)
    if _DRY_IS_A_VERB.search(said):
        return None
    if re.search(r"\b(?:why|how come)\b", said):
        return THE_DRY_WHY
    return THE_DRY_HOW_OFTEN

GROW_SKIP = ("tomato",)
GROW_ENTRIES = [
    entry("grow-" + words[0], (words, GROW_ASK), reply, avoid=GROW_NOT)
    for words, reply in SOWING + PLANTING if words[0] not in GROW_SKIP
]


def _blight(memory, reading):
    line = _words(reading)
    if _has(line, "rose") or _has(line, "roses") or _has(line, "spot") or _has(line, "spots"):
        return ("Black spot is a fungus that overwinters on the fallen leaves, so pick every "
                "spotted leaf off the plant and off the ground and bin them - never the compost - "
                "and it comes back much less next year. Water at the base rather than over the "
                "leaves, leave space round the plant for air to move, and feed it: a rose or a "
                "tomato that is growing hard shakes it off. A fungicide is the last resort, and it "
                "has to go on early, before the spots are everywhere.")
    if _has(line, "potato") or _has(line, "potatoes"):
        return ("Blight on a potato crop shows as brown-black patches that spread fast in warm wet "
                "weather, and the spores wash down to the tubers: cut the tops off at ground level "
                "and bin them, then lift the potatoes a fortnight later so the skins set and the "
                "spores do not reach them. Do not compost the tops. Next year grow a blight-"
                "resistant variety and leave more space between rows, because a crop that dries "
                "quickly after rain gets it less.")
    return ("Brown-black patches with a pale edge that spread fast in warm wet weather are blight, "
            "and once it is on a tomato plant the aim is slowing it, not curing it: cut off and bin "
            "the affected leaves (not the compost), water at the base in the morning rather than "
            "over the leaves, and take out some side shoots so the plants dry quicker. Pick the "
            "fruit that is already ripening - a green tomato will ripen on a windowsill indoors - "
            "and a copper fungicide slows it if it is caught early. Next year grow a blight-"
            "resistant variety with more room between plants.")


ROT_CROPS = ("seedling", "seedlings", "cutting", "cuttings", "stem", "stems", "potato",
             "potatoes", "onion", "onions", "garlic", "apple", "apples", "pear", "pears",
             "plum", "plums", "courgette", "courgettes", "cucumber", "cucumbers", "tomato",
             "tomatoes", "pepper", "peppers", "melon", "melons", "aubergine", "aubergines",
             "squash", "pumpkin", "pumpkins", "strawberry", "strawberries", "plant", "plants",
             "crop", "crops", "fruit", "fruits", "dahlia", "dahlias", "tree", "trees", "vine",
             "vines", "bed", "beds", "greenhouse", "ground", "allotment", "blossom end",
             "flower end", "bottom")


def _earlier_words(memory, keep=3):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return ""
    said = " ".join(str(turn.get("user") or "") for turn in turns[-keep:]
                    if isinstance(turn, dict))
    return _words({"clean": said})


def _rot(memory, reading):
    line = _words(reading)
    if any(_has(line, w) for w in ("eat", "eating", "edible", "safe", "safe to eat",
                                   "still eat", "ok to eat", "use the rest", "use them")):
        if (_has(line, "potato") or _has(line, "potatoes") or _has(line, "onion")
                or _has(line, "onions") or _has(line, "garlic")):
            return ("Bin every soft, slimy or smelly one, because rot in a potato or an onion is "
                    "not something to cut round: the spores travel through the flesh and the "
                    "whole one tastes wrong. A green patch on a potato is solanine, so cut it off "
                    "with a wide margin or bin that potato, and never eat one that has sprouted "
                    "and gone soft.")
        return ("Cut out the brown with a good margin around it and the sound part is fine to eat; "
                "anything soft, wet or with grey fuzz on it goes in the bin, not on the plate and "
                "not in the compost. Wash what you keep and use it in the next day or two, "
                "because fruit that has started to go will not keep.")
    if not any(_has(line, word) for word in ROT_CROPS):
        line = line + " " + _earlier_words(memory)
    if (_has(line, "seedling") or _has(line, "seedlings") or _has(line, "cutting")
            or _has(line, "cuttings") or _has(line, "stem") or _has(line, "stems")):
        return ("A seedling that collapses at soil level has damping off: the stem goes thin and "
                "water-soaked and the plant keels over. It is a fungus in cold, wet compost, so "
                "sow into fresh compost, water from below and let the surface dry between "
                "waterings, keep the pots warm and move the survivors into the light. Air moving "
                "round them matters more than anything you can spray: take the lid off the "
                "propagator as soon as the seedlings are up, and bin the collapsed ones with "
                "their compost.")
    if (_has(line, "blossom end") or _has(line, "black at the bottom")
            or _has(line, "black at the end") or _has(line, "bottom is black")
            or _has(line, "bottom of the fruit is black") or _has(line, "flower end")
            or _has(line, "rot at the end") or _has(line, "rotting at the end")
            or _has(line, "end is rotting") or _has(line, "end rot")
            or _has(line, "rotting at the flower") or _has(line, "rot at the flower")):
        return ("A black sunken patch on the bottom end of a tomato, a pepper or a courgette is "
                "blossom end rot, and it is not an infection: the fruit could not get enough "
                "calcium because the plant's water swung about. Water deeply and evenly - a good "
                "soak twice a week rather than a sprinkle every day - and mulch to hold it, and "
                "do not add calcium to the soil, because the calcium is there and the water is "
                "what moves it. Take the marked fruit off so the plant stops feeding it, and the "
                "later trusses come through sound.")
    if (_has(line, "potato") or _has(line, "potatoes") or _has(line, "bulb")
            or _has(line, "bulbs") or _has(line, "onion") or _has(line, "onions")
            or _has(line, "garlic")):
        return ("Sort them out now: bin anything soft, slimy or smelly, because one rotting potato "
                "or onion takes the rest with it, and cut the bad bits out of the sound ones and "
                "use those first. If they are still in the ground, lift them rather than leaving "
                "them in wet soil, and dry them somewhere airy before they go into store. Next "
                "year plant in a bed that drains - a raised bed if the plot holds water - and "
                "never store a bruised one with the sound ones.")
    if (_has(line, "apple") or _has(line, "apples") or _has(line, "pear") or _has(line, "pears")
            or _has(line, "plum") or _has(line, "plums")):
        return ("Fruit rotting on the tree is usually brown rot, and the spores come from the "
                "mummified fruit left hanging and off the ground from last year. Pick and bin "
                "every rotten one - on the tree and under it - and do not compost them, thin the "
                "clusters so the fruit has air round it, and prune out crowded branches in winter. "
                "Wasps and birds start the holes, so a trap from August saves a lot of fruit.")
    return ("Rot on the plant is wet and still air, so pick off every affected fruit and bin it - "
            "not the compost - and take off the leaves touching the ground so air moves under the "
            "plant. Water at the base in the morning rather than over the leaves, and pick what is "
            "sound a little earlier than you would otherwise, since a ripe fruit on wet soil is "
            "what goes next. Take the fruit with a soft brown bruise at the stalk end off as soon "
            "as you see it, because it will not ripen and it spreads.")


PEST_NOUNS = (
    ("caterpillar", ("caterpillar", "caterpillars", "cabbage white", "cabbage whites",
                     "cabbage worm", "cabbage worms")),
    ("whitefly", ("whitefly", "white fly", "whiteflies")),
    ("aphid", ("aphids", "aphid", "greenfly", "green fly", "blackfly", "black fly")),
    ("weevil", ("vine weevil", "vine weevils", "weevil", "weevils", "notch", "notches")),
    ("scale", ("scale insect", "scale insects", "scale", "sticky leaves")),
    ("mealybug", ("mealybug", "mealybugs", "white fluff", "fluffy white")),
)


def _pest_named(text):
    for pest, words in PEST_NOUNS:
        for word in words:
            if _has(text, word):
                return pest
    return ""


def _pest_from_turns(memory, keep=3):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return ""
    for turn in reversed(turns[-keep:]):
        if isinstance(turn, dict):
            found = _pest_named(_words({"clean": str(turn.get("user") or "")}))
            if found:
                return found
    return ""


def _pests(memory, reading):
    line = _words(reading)
    pest = _pest_named(line) or _pest_from_turns(memory)
    if not pest:
        return None
    if pest == "caterpillar":
        return ("Caterpillars are easiest picked off by hand in the evening, when they come out to "
                "feed, and dropped in a bucket of water - check the undersides of the leaves for the "
                "yellow eggs and squash those too. A net over the crop from May to September is the "
                "real fix, because the cabbage white butterfly cannot get in to lay: keep it clear "
                "of the leaves and peg the edges down. Inspect every few days, since a small "
                "caterpillar becomes a big one fast.")
    if pest == "whitefly":
        return ("Whitefly sits under the leaves and flies up in a cloud when you touch the plant. "
                "Yellow sticky traps catch the adults, and a spray of soapy water - a teaspoon of "
                "washing-up liquid in a litre - on the undersides of the leaves kills the young "
                "ones; repeat every few days, because it does not touch the eggs. Badly hit leaves "
                "come off. Check new plants before they go in the greenhouse, which is where "
                "whitefly gets in.")
    if pest == "aphid":
        return ("Greenfly and blackfly are both aphids and get the same treatment: squash them by "
                "hand or spray the undersides of the leaves and the soft growing tips with soapy "
                "water - a teaspoon of washing-up liquid in a litre. Broad beans are the usual "
                "blackfly crop, and the tips are the first place to look: pinch the top few inches "
                "out once the flowers set. Ladybirds and their larvae will clear a lot for you, so "
                "leave a marigold or a poached egg plant nearby.")
    if pest == "weevil":
        return ("Vine weevil is a root grub with a beetle above ground, and the beetles notch the "
                "leaf edges at night. The grubs are what kills the plant: tip a pot out and look "
                "for fat white C-shaped ones in the compost, then bin that compost and repot in "
                "fresh. A nematode watered on in late summer or early autumn is the cleanest "
                "control, and going out with a torch after dark deals with the beetles.")
    if pest == "scale":
        return ("Scale insects sit on stems and the undersides of leaves as little brown or white "
                "shells you can flick off with a fingernail, and they leave sticky honeydew that "
                "turns the leaves black. Wipe them off with a cotton bud dipped in rubbing "
                "alcohol, or spray the plant with soapy water - a teaspoon of washing-up liquid in "
                "a litre - a few times over a month, because the shells protect the ones "
                "underneath. Check the plant that arrived last, which is usually where they came "
                "in.")
    if pest == "mealybug":
        return ("Mealybug is the white cotton-wool fluff in the leaf joints and along the stems, "
                "and it hides in the same places as scale. Paint it off with a cotton bud dipped "
                "in rubbing alcohol, or spray the plant with soapy water - a teaspoon of "
                "washing-up liquid in a litre - every week for a month, and take off the worst "
                "leaves. It thrives in warm, still air, so give the plant more room and check the "
                "plants either side of it.")
    return ("Squash the aphids by hand or spray them with soapy water - a teaspoon of washing-up "
            "liquid in a litre - and get the undersides of the leaves and the soft new tips, which "
            "is where they cluster. Ladybirds and their larvae will clear a lot for you, so plant a "
            "marigold or a poached egg plant nearby. A strong jet of water knocks them off, and "
            "check the plant every few days, because aphids multiply fast and curl the new leaves.")


def _mildew(memory, reading):
    return ("White powder on the leaves is powdery mildew, and it likes dry roots and still air: "
            "water thoroughly at the base rather than sprinkling the leaves, take off the worst of "
            "them, and open the plants up so the air moves. A spray of one part milk to nine parts "
            "water helps a little, and courgettes, cucumbers and roses usually carry on growing "
            "through it. Feed the plant and keep the water steady - mildew moves fastest on a "
            "plant that has been let dry out and then flooded.")
ROOT_NAMES = ((r"carrots?", "A carrot"), (r"beetroots?|beets?", "Beetroot"),
              (r"parsnips?", "A parsnip"), (r"radish(?:es)?", "A radish"),
              (r"turnips?", "A turnip"), (r"swedes?", "A swede"), (r"celeriac", "Celeriac"))
ROOT_ASKS = ("carrot", "carrots", "beetroot", "beetroots", "beet", "parsnip", "parsnips",
             "radish", "radishes", "turnip", "turnips", "swede", "swedes", "celeriac")


def _root_split(memory, understood):
    text = ((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    name = "A root crop"
    for pattern, said in ROOT_NAMES:
        if re.search(r"\b" + pattern + r"\b", text):
            name = said
            break
    if re.search(r"\bbolt(?:ed|ing)?\b|\brun to seed\b|\bgoing to seed\b|\bgone to seed\b"
                 r"|\bflower(?:ing|ed)?\b|\bwent up\b", text):
        first = (name + " runs to seed when a hot dry spell pushes it up in its first year, and "
                 "once the stem goes up the root stops swelling and turns woody in the ground.")
    elif re.search(r"\bfork(?:ed|ing)?\b|\btwo legs\b|\bdouble root", text):
        first = (name + " forks when the taproot meets a stone, a hard pan or fresh manure, or "
                 "when the seedlings were left crowded: the root splits in two to get round it.")
    elif re.search(r"\bwood(?:y|en)\b|\btough\b|\bpithy\b", text):
        first = (name + " goes woody when it is left in the ground too long, and in hot dry soil "
                 "it happens sooner: the root keeps growing and the middle turns hard and "
                 "stringy.")
    else:
        first = (name + " splits when it takes a drink after a dry spell: the root swells faster "
                 "than the skin keeps up, and too much feed does the same.")
    return (first + " Water little and often so the soil stays evenly damp rather than soaking it "
            "after a dry week, thin the seedlings so the roots have room, and lift them once they "
            "are a good size. The damaged ones are still fine to eat, so use those first.")

def _crop_setting_reply(memory, understood):
    text = ((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    if "bitter" in text:
        if any(word in text for word in ("courgette", "courgettes", "zucchini", "squash",
                                         "pumpkin", "pumpkins", "cucumber", "cucumbers")):
            return ("A bitter cucumber, courgette or squash is stress, not a bad seed. Heat, a dry "
                    "spell at the root and a plant left to grow huge all push the bitter compounds up, "
                    "and they sit mostly at the stalk end, so cut that inch off and taste the "
                    "rest. Water regularly at the base, pick the fruit small and often rather "
                    "than leaving it to swell, and shade the plant in a heatwave.")
        if any(word in text for word in ("tomato", "tomatoes")):
            return ("A bitter tomato is usually one picked before it is fully ripe, or a plant "
                    "that ran short of water while the fruit was swelling. Leave the rest on the "
                    "vine until it is deep red all over, water evenly at the base, and taste a "
                    "ripe one before you blame the variety.")
        if any(word in text for word in ("strawberry", "strawberries")):
            return ("A bitter strawberry is underripe: the sugar comes last, so pick only fruit "
                    "that is red all over and leave the pale shoulders to colour. Water at the "
                    "base and net them, because a stressed or bird-pecked fruit turns sharp.")
        return ("Bitterness in a home-grown crop is usually stress - a dry spell at the root, or "
                "fruit picked before it ripened. Water evenly at the base, pick when it is fully "
                "coloured, and taste a ripe one before blaming the seed.")
    if ("small" in text or "tiny" in text or "shrivelled" in text) and not any(
            word in text for word in ("strawberry", "strawberries", "plant", "plants",
                                      "seedling", "seedlings", "seed", "seeds", "leaf",
                                      "leaves")):
        return ("Small fruit on a plant that flowered means it has set more than its roots can "
                "fill. Water at the base so the soil stays evenly damp, feed a high-potash tomato "
                "feed once the first flowers open, and pick the fruit as soon as it is ready so "
                "the rest can swell. A dry spell while the fruit was setting is the commonest "
                "cause, and in a pot it can happen within a day or two.")
    if any(word in text for word in ("courgette", "courgettes", "zucchini", "squash", "pumpkin",
                                     "cucumber", "cucumbers")):
        return ("Courgettes, squashes and cucumbers carry male and female flowers on the same "
                "plant, and the female one has a tiny fruit behind the flower. If the little fruit "
                "goes yellow and drops off, the pollen never got to it - pick a male flower, peel "
                "the petals back and dab it into the middle of a female one early in the morning, "
                "when the flower is fresh. Cold nights under 10C and a very hot dry spell both stop "
                "the pollen working, and a plant fed hard on tomato feed grows leaves instead, so "
                "water at the base and wait for the weather to pass.")
    if any(word in text for word in ("runner", "french bean", "french beans", "broad bean",
                                     "broad beans", "beans")):
        return ("Runner beans set nothing when the soil dries out at the root, which is what makes "
                "the flowers drop before they are pollinated. Water at the base every evening in a "
                "dry spell, a good soaking rather than a sprinkle, and mulch round the plants to "
                "hold it. They also need bees, so leave a patch of flowers near the wigwam, and "
                "once the pods start pick them every couple of days because a bean left to swell "
                "stops the plant flowering.")
    if any(word in text for word in ("chilli", "chillies", "chili", "pepper", "peppers",
                                     "aubergine", "aubergines", "eggplant", "eggplants")):
        if "aubergine" in text or "eggplant" in text:
            crop = "An aubergine"
        elif "pepper" in text:
            crop = "A pepper"
        else:
            crop = "A chilli"
        return (crop + " drops its flowers for one of three reasons, and heat is the first. Pollen "
                "goes sterile above about 32C by day or 27C at night, so shade the plant from "
                "midday sun in a heatwave and keep the pot off hot paving. The second is feed - a "
                "plant given nitrogen grows leaves, so switch to a high-potash tomato feed once "
                "the first flowers open. The third is pollination, which barely happens in a "
                "greenhouse or on a windowsill, so tap the cane or the pot at midday and move "
                "pollen between the flowers with a soft brush. Nights below about 15C stop it "
                "setting as well, so do not put it outside before the nights are warm.")
    if any(word in text for word in ("tomato", "tomatoes")):
        return ("A tomato with no flowers at all is still growing rather than fruiting. Too much "
                "nitrogen, too little sun, and nights still below about 10C are the three usual "
                "reasons, so stop any high-nitrogen feed, keep the plant in full sun, and switch "
                "to a tomato feed once the first truss opens. If the flowers open and then drop, "
                "the pollen is what failed - tap the cane at midday to shake it loose, water "
                "evenly at the base rather than in fits, and damp the path down in a heatwave so "
                "the air is not bone dry. A truss that sets one or two fruits and drops the rest is "
                "usually a plant carrying more than its roots can fill.")
    if any(word in text for word in ("strawberry", "strawberries")):
        return ("Tiny strawberries are usually an old plant, and a strawberry bed is worth "
                "replanting every three years from fresh runners because the yield drops off after "
                "that. The other two causes are easy. Feed the plants with a high-potash feed as "
                "the flowers open rather than a nitrogen one, and cut off the runners instead of "
                "letting the plant spend its strength on new plants. Net them from the birds as the "
                "fruit colours, and water at the base so the fruit is not sitting wet.")
    return ("A vegetable that makes flowers and no fruit is usually a pollination problem before "
            "it is a feeding one. Leave the flowers for the bees, and hand-pollinate under cover "
            "with a soft brush or a dabbed male flower. Cold nights and very hot dry days both stop "
            "the pollen, and a plant fed on nitrogen grows leaves instead of fruit, so switch to a "
            "high-potash feed once the first flowers open. Water at the base and keep it even, "
            "because a plant that dries out drops its flowers before they set.")



SHADE_LEAVES = ("salad leaves, spinach, chard, kale, rocket, parsley, mint, rhubarb, beetroot, "
                "radish and leeks")
SHADE_SUN_CROPS = (("tomato", "Tomatoes"), ("tomatoes", "Tomatoes"),
                   ("courgette", "Courgettes"), ("courgettes", "Courgettes"),
                   ("zucchini", "Courgettes"), ("squash", "Squash"), ("pumpkin", "Pumpkins"),
                   ("pumpkins", "Pumpkins"), ("cucumber", "Cucumbers"),
                   ("cucumbers", "Cucumbers"), ("pepper", "Peppers"), ("peppers", "Peppers"),
                   ("chilli", "Chillies"), ("chillies", "Chillies"), ("chili", "Chillies"),
                   ("aubergine", "Aubergines"), ("aubergines", "Aubergines"),
                   ("bean", "Beans"), ("beans", "Beans"), ("pea", "Peas"), ("peas", "Peas"),
                   ("sweetcorn", "Sweetcorn"), ("corn", "Sweetcorn"),
                   ("strawberry", "Strawberries"), ("strawberries", "Strawberries"))


def _shade_crop_reply(memory, understood):
    text = ((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    if "potato" in text or "potatoes" in text:
        return ("Potatoes will crop in half shade, just smaller and later, so they are the one "
                "root that earns a place in a bed with morning sun and four hours of it. What "
                "they will not do is fill in deep shade, where the tops grow and the tubers stay "
                "marble-sized. The crops that do best out of the sun are the leaves: "
                + SHADE_LEAVES + ".")
    named = [word for word, said in SHADE_SUN_CROPS if word in text]
    if named:
        crop = dict(SHADE_SUN_CROPS)[named[0]]
        return (crop + " want six to eight hours of direct sun a day, and in shade they grow "
                "leaves and set nothing - so give them the sunniest strip you have, against a "
                "south wall or in a pot you can move. What does crop on three to four hours is "
                "the leaf and root list: " + SHADE_LEAVES + ". Sow those thinner than you would "
                "in the open, and keep the slugs off, because slow growth and still damp air are "
                "what slugs and mildew both like.")
    return ("For a shady bed, grow the leaf and root crops: " + SHADE_LEAVES + ", and they crop "
            "on three to four hours of sun a day, which is what shade gives. Sow them thinner "
            "than you would in the open and keep the slugs off, because slow growth and still "
            "damp air are what mildew and slugs like best. Anything that has to ripen wants six "
            "hours and more, so keep tomatoes, courgettes, peppers, beans, squash and sweetcorn "
            "for the sunniest strip you have.")
SOFT_HERBS = ("basil", "mint", "parsley", "coriander", "cilantro", "chives", "dill", "oregano",
              "thyme", "rosemary", "sage", "tarragon")
_HERB_PINCH = (
    "Pinch the top pair of leaves off each stem, just above the next pair down: every stem you tip "
    "sends out two sideshoots, so the plant bushes out instead of running up into one tall stem. "
    "Cut no lower than a leaf pair on basil, mint and coriander, because a stem cut back to bare "
    "wood usually does not come again. Pick from the top, a few stems at a time, and never strip a "
    "plant in one go. Rosemary, thyme and sage are the woody ones and are not pinched like basil: "
    "take the top third back in spring, once the worst of the frost has gone, and never cut into "
    "the old bare wood.")
_HERB_WOODY = (
    "A herb goes woody when it has been allowed to flower: the stems harden and it stops making "
    "leaf. Pinch the flower buds off as soon as they show, keep picking the tips, and cut a third "
    "of the oldest stems back to a low leaf pair in spring. Basil is the one that will not come "
    "back from old wood for long, so take cuttings in late summer or sow a fresh pot in June "
    "rather than fight it.")
_HERB_SPREAD = (
    "Mint spreads by runners just under the surface, so pulling it up makes it worse. Sink it in a "
    "pot with the rim 2cm above the soil, or a bottomless bucket, or grow it in a container away "
    "from the bed. In a border already taken over, fork out the runners in spring and again in "
    "autumn for two years, and cut the stems before they flower so it cannot seed.")
_HERB_LOOK = (
    "Soft herbs want sun, drainage and picking: water when the top of the soil is dry, feed weakly, "
    "and take the tips off often so the plant keeps growing leaf instead of stem. Basil and "
    "coriander are annuals, so a pot that lasts a season is normal; mint, thyme, oregano, sage and "
    "rosemary are perennials and want cutting back in spring.")
_SEEDLING_LEGGY = (
    "Seedlings go leggy for one reason: not enough light, which is worse indoors on a windowsill "
    "than in a greenhouse, and worse still too warm. Move them somewhere brighter and cooler, turn "
    "the tray each day so they do not lean, and prick them out deeper than they were - a tomato or "
    "a brassica will make roots along the buried stem. Next sowing, thin them out sooner and sow a "
    "little later in the year.")
_CACTUS_SOFT = (
    "A cactus or succulent that has gone soft is rotting from too much water: the tissue goes "
    "squishy and translucent from the base up, and it will not firm up again. Stop watering, take "
    "it out of the pot and cut away every soft part with a clean knife until the flesh is firm and "
    "clean, leave the cut to callous for a week, then set it on dry gritty compost. Water only "
    "when the compost is dry right through, and never leave the pot standing in water.")


_HERB_WINTER = (
    "Most soft herbs die down and come again rather than dying: chives and mint go to nothing and "
    "return from the roots in spring, parsley is a biennial so its second year is thin and woody, "
    "and thyme, sage, oregano and rosemary stay green through it. Before the first frost, move the "
    "pots against a wall and off the ground, cut the old stems down to about 5cm and mulch around "
    "the crowns. Then leave them alone: no feed, and water only when the compost has dried right "
    "out, because cold and wet kills more herbs than frost does.")
_HERB_WINTER_WORDS = ("winter", "winters", "overwinter", "overwintering", "frost", "frosts",
                      "frosty", "cold", "coming back", "come back", "comes back", "came back",
                      "survive", "survives", "survived", "dies back", "die back", "died back",
                      "dying back", "perennial", "perennials", "next year", "every year",
                      "keep going", "keeps going", "keep it going")


_HERB_WHEN_WOODY = (
    "Take the top third back in spring, once the worst of the frost has gone and before the plant "
    "starts into growth: that is the one hard cut rosemary, thyme, sage and oregano need, and it is "
    "what stops them going leggy and bare in the middle. Never cut into the old bare wood, because "
    "a stem cut back to it usually does not come again, and a light trim over the tips after "
    "flowering holds the shape in between.")
_HERB_WHEN_SOFT = (
    "Pick basil, mint, parsley, coriander and chives from the top all through the growing season, "
    "from June into September: pinch or snip the top pair of leaves every week or two and the plant "
    "bushes out instead of running up into one tall stem. There is no yearly hard cut for these - "
    "stop at a leaf pair, because a soft stem cut back to bare wood usually does not come again - "
    "and take a few stems at a time rather than stripping the plant in one go.")
_HERB_WOODY_NAMES = ("rosemary", "thyme", "sage", "oregano", "lavender")


def _herbs(memory, understood):
    line = _words(understood)
    named = any(_has(line, word) for word in SOFT_HERBS + ("herb", "herbs"))
    mint = _has(line, "mint")
    if (named and any(_has(line, word) for word in _HERB_WINTER_WORDS)
            and not any(_has(line, word) for word in ("grow", "growing", "plant", "planting",
                                                      "sow", "sowing"))):
        return _HERB_WINTER
    if mint and any(_has(line, word) for word in ("spread", "spreads", "spreading", "spread out",
                                                  "taken over", "took over", "taking over",
                                                  "everywhere", "invasive", "contain", "control",
                                                  "stop it", "keep it in", "border")):
        return _HERB_SPREAD
    if named and any(_has(line, word) for word in ("woody", "wooden", "leggy", "flowered",
                                                   "flowering", "flower", "flowers", "bolted",
                                                   "bolting", "gone to seed")):
        return _HERB_WOODY
    _cutting = ("prune", "pruning", "pinch", "pinching", "tip", "tips", "top", "topping",
                "trim", "trimming", "cut", "cutting", "snip", "snipping", "back", "harvest",
                "harvesting", "pick", "picking")
    if named and _asks_when(line) and any(_has(line, word) for word in _cutting):
        if any(_has(line, word) for word in _HERB_WOODY_NAMES):
            return _HERB_WHEN_WOODY
        return _HERB_WHEN_SOFT
    if named and any(_has(line, word) for word in _cutting):
        return _HERB_PINCH
    if named:
        return _HERB_LOOK
    return None


def _seedlings(memory, understood):
    line = _words(understood)
    if any(_has(line, word) for word in ("leggy", "spindly", "straggly", "stretched", "stretching",
                                         "tall and thin", "fallen over", "falling over", "flopped",
                                         "flopping")):
        return _SEEDLING_LEGGY
    return None


def _cactus_soft(memory, understood):
    line = _words(understood)
    if any(_has(line, word) for word in ("soft", "squishy", "soggy", "mushy", "translucent",
                                         "rotting", "rotted", "collapse", "collapsed")):
        return _CACTUS_SOFT
    return None

def _hydrangea(memory, reading):
    line = str(reading.get("clean") or reading.get("text") or "").lower()
    if any(word in line.split() for word in (
            "blue", "pink", "purple", "colour", "color", "colourful", "acid", "alkaline", "lime",
            "limy", "ph", "soil", "ericaceous")):
        return ("The colour is the soil rather than the plant: acid soil gives blue, limy soil "
                "gives pink, and a pot is whatever compost you fill it with. Water in sulphur or an "
                "ericaceous feed through the season for blue, or add garden lime for pink, and give "
                "it a year, because it is next season's flowers that change. Water it well in dry "
                "spells as well - wilting in the afternoon sun is thirst, and the buds for next "
                "year dry up if it is left.")
    return ("Water a hydrangea well in dry spells, because wilting in the afternoon sun is thirst "
            "and the buds for next year dry up if it is left. The colour is the soil: acid soil "
            "gives blue, limy soil gives pink, so water in a sulphur or ericaceous feed for blue, "
            "and add garden lime for pink. Prune a mophead in early spring, taking the old flower "
            "heads and about a third of last year's stems, and leave a lacecap and a climbing "
            "hydrangea alone apart from the dead heads.")


_AVOID_THE_STING = ("avoid", "avoiding", "prevent", "preventing", "not get stung",
                    "don't get stung", "dont get stung", "stop being stung", "keep them away",
                    "keep wasps away", "keep it away", "deter", "repel", "repellent",
                    "not sting me", "stop stinging me", "stop a wasp stinging me",
                    "stop it stinging", "wont leave me alone", "won't leave me alone")
STUNG = ("stung", "sting me", "bit me", "bitten", "got stung", "been stung", "i was stung",
         "swollen", "swelling", "hurts", "hurting", "sore", "itching",
         "wasp sting", "bee sting", "sting on", "sting is", "sting hurts", "sting doesnt",
         "sting doesn't", "sting swell", "first aid",
         "stood on", "stepped on", "trod on", "trodden on", "it hurts", "really sore")

_WASP_AVOID = ("Don't swat it and don't wave: stand still or step away slowly and it loses "
               "interest in a few seconds, because a wasp stings when it feels trapped or the "
               "nest is threatened. Outside, keep sweet drinks covered and look in the can "
               "before you sip. If it does sting, scrape the sting out sideways with a "
               "fingernail, wash it and hold something cold on it.")
_WASP_STUNG = ("Scrape the sting out sideways with a fingernail or the edge of a card rather "
               "than pinching it, wash the spot and hold something cold on it for ten minutes; "
               "a wasp sting hurts for an hour or two and calms down with an antihistamine. A "
               "swollen face or throat, wheezing, or feeling faint needs 999, because that is "
               "anaphylaxis and it moves fast.")


_AVOIDING_A_STING = re.compile(
    r"\b(?:avoid|prevent|stop getting stung|stop being stung|keep away|keep them away|"
    r"keep wasps? away|keep it away|not get stung|don'?t get stung|stings me|"
    r"if a (?:wasp|bee)|else stung)\b")


def _wasp_near(memory, understood):
    said = (understood.get("clean") or understood.get("norm_text") or "").lower()
    if _AVOIDING_A_STING.search(said):
        return _WASP_AVOID
    if any(word in said for word in _AVOID_THE_STING):
        return _WASP_AVOID
    if any(word in said for word in STUNG):
        return _WASP_STUNG
    return _WASP_AVOID
_A_ROOM_OR_WALL = (
    "bedroom", "bedrooms", "living room", "lounge", "hallway", "hallways", "bathroom",
    "bathrooms", "kitchen", "nursery", "landing", "stairs", "room", "rooms", "wall", "walls",
    "ceiling", "ceilings", "skirting", "woodwork", "feature wall", "wallpaper",
)
_SOMETHING_TO_GROW_IN = (
    "garden", "gardens", "border", "borders", "bed", "beds", "flower bed", "flower beds",
    "flower", "flowers", "plant", "plants", "planting", "planted", "grow", "grows", "growing",
    "pot", "pots", "planter", "planters", "container", "containers", "tub", "tubs", "trough",
    "basket", "baskets", "hanging basket", "window box", "windowbox", "window", "windows",
    "windowsill", "window sill", "sill", "shelf", "shelves", "shelving", "balcony", "patio",
    "yard", "lawn", "soil", "compost", "outdoor", "outdoors", "outside", "allotment",
    "climber", "climbers", "shrub", "shrubs", "tree", "trees", "rose", "rose bed",
)


def _says_one_of(said, words):
    tokens = set(re.findall(r"[a-z']+", said))
    return any((one in said) if " " in one else (one in tokens) for one in words)


def _has_something_to_grow_in(reading):
    reading = reading or {}
    said = " ".join(str(reading.get("clean") or reading.get("norm_text") or "").split()).lower()
    if not _says_one_of(said, _A_ROOM_OR_WALL):
        return True
    return _says_one_of(said, _SOMETHING_TO_GROW_IN)


COMPOST_MEANS = ("Compost is garden and kitchen waste left to rot down into crumbly dark stuff "
                 "you dig back into the soil, which feeds the plants and holds water. ")
COMPOST_JOB = ("Mix roughly half green waste (kitchen scraps, grass) with half brown (cardboard, "
               "dry leaves, twigs), keep it as damp as a wrung-out sponge, and turn it now and "
               "then. No cooked food or meat, which attracts rats.")
COMPOST_WHAT_IS = ("what is compost", "what is a compost heap", "what is composting",
                   "what is compost made of", "compost mean", "compost stand for")
COMPOST_AILING = (
    "rot", "rots", "rotting", "rotted", "breaking down", "break down", "broken down",
    "heating", "heating up", "heat up", "warm up", "not warm", "cold", "slow", "slowly",
    "stalled", "stopped", "slime", "slimy", "smell", "smells", "smelly", "smelling",
    "stinks", "stinking", "sour", "flies", "wet", "soggy", "dry", "nothing",
    "freeze", "freezes", "freezing", "frozen", "frost", "frosty",
)
COMPOST_SMELLY = ("smell", "smells", "smelly", "smelling", "stinks", "stinking", "sour",
                  "slime", "slimy", "soggy", "flies", "wet")
COMPOST_FROZEN = ("freeze", "freezes", "freezing", "frozen", "frost", "frosty", "snow",
                  "winter", "over winter")
COMPOST_IN_THE_COLD = (
    "The edges will freeze in a hard frost and the heap slows to nothing, which is normal - the "
    "middle keeps going and it picks up again in spring. To keep it working, fork it into one "
    "bigger heap, keep the lid on and lay a sheet of cardboard or an old compost bag over the "
    "top; a heap that is cold in mild weather is a different problem, and that one wants greens "
    "and more bulk.")
COMPOST_TOO_WET = ("That smell is a heap with no air in it: too much wet green and nothing to open "
                   "it up. Fork in torn cardboard or dry leaves until it is as damp as a "
                   "wrung-out sponge, turn it over, and keep cooked food and meat out - those are "
                   "what the flies come for.")
COMPOST_STALLED = (
    "A heap that has gone quiet is short of air, water or greens, and which one it is shows: "
    "bone dry means water it until it is like a wrung-out sponge, damp and cold means it wants "
    "greens - grass clippings, vegetable peelings - mixed through, and a heap that is damp and "
    "green but still doing nothing is too small to hold heat, so build it up to about a cubic "
    "metre. In winter it will slow right down and start again in spring, which is normal.")


NO_COOKED_FOOD = "No cooked food or meat, which attracts rats"
_NAMED_A_MATERIAL = re.compile(
    r"\b(?:cooked|meat|meats|bones?|food|foods|scraps?|bread|pasta|rice|dairy|cheese|milk|"
    r"fish|chicken|oil|oily|fat|fats|grease|gravy|cat food|dog food|pet food|leftovers?)\b",
    re.I)


def _the_no_cooked_food(understood):
    said = " ".join(str((understood or {}).get("clean")
                        or (understood or {}).get("text") or "").lower().split())
    return NO_COOKED_FOOD if _NAMED_A_MATERIAL.search(said) else ""


def compost_reply(memory, reading):
    line = str(reading.get("text") or reading.get("clean") or "").lower()
    for phrase in COMPOST_WHAT_IS:
        if phrase in line:
            return COMPOST_MEANS + COMPOST_JOB
    if _says_one_of(line, COMPOST_AILING):
        if _says_one_of(line, COMPOST_FROZEN):
            return COMPOST_IN_THE_COLD
        if _says_one_of(line, COMPOST_SMELLY):
            return COMPOST_TOO_WET
        return COMPOST_STALLED
    return COMPOST_JOB


_THE_GARDEN_IN_THE_COLD = (
    "plant", "plants", "planted", "planting", "pot", "pots", "seedling", "seedlings", "seed",
    "seeds", "sow", "sowed", "sowing", "garden", "gardener", "allotment", "border", "borders",
    "raised bed", "window box", "veg", "vegetable", "vegetables", "crop", "crops", "bedding",
    "shrub", "shrubs", "lawn", "grass", "flower", "flowers", "tree", "trees", "citrus", "olive",
    "banana plant", "tree fern", "hanging basket", "baskets", "greenhouse", "polytunnel",
    "cloche", "cold frame", "cuttings", "bulbs", "tender", "fleece", "compost", "herbs",
    "basil", "tomato", "tomatoes", "potatoes", "spuds", "geraniums", "dahlias", "agapanthus",
)


def _the_cold_is_the_garden_s(reading):
    reading = reading or {}
    said = " ".join(str(reading.get("clean") or reading.get("text") or "").split()).lower()
    return _says_one_of(said, _THE_GARDEN_IN_THE_COLD)


_BARE_STEMS = ("bare", "leggy", "spindly", "straggly", "skinny", "threadbare",
               "too tall", "long and thin", "thin and long", "tall and thin", "tall and leggy",
               "stretched", "stretching", "etiolated", "bushy", "cut back", "cut it back",
               "trim it back", "prune")
_BARE_LOSS = ("lost", "losing", "lose", "dropped", "dropping", "drops", "gone", "going",
              "no leaves", "nothing on", "stems with no")
_A_PART_OF_THE_PLANT = ("bottom", "lower", "middle", "base", "stem", "stems", "joint", "joints")


def _the_stems_are_what_is_bare(reading):
    reading = reading or {}
    said = " ".join(str(reading.get("clean") or reading.get("text") or "").split()).lower()
    if _says_one_of(said, _BARE_STEMS):
        return True
    return _says_one_of(said, _BARE_LOSS) and _says_one_of(said, _A_PART_OF_THE_PLANT)


_DIG_OVER_METHOD = (
    "One spade deep is enough for most beds: turn the soil over, break up the clods and fork a "
    "couple of buckets of compost or well-rotted manure into each square metre as you go. Pick out "
    "every white root of bindweed and nettle as it comes up, or it will be back within weeks. "
    "Autumn is the best time, because the frost breaks the clods down for you, and leave it alone "
    "if the soil is wet enough to ball in your hand - digging clay when it is wet turns it into "
    "brick.")
_DIG_OVER_WHEN = (
    "Autumn, from October into December, once the beds are emptying: dig it over then and the "
    "frost does the work of breaking the clods down over winter, so the soil is workable in "
    "spring. On heavy clay that is the one time it is worth doing, because digging wet clay turns "
    "it into brick and digging dry clay leaves the lumps like stones. If you have to do it in "
    "spring, fork it over rather than digging.")
_DIG_OVER_TARGETS = ("bed", "beds", "border", "borders", "plot", "allotment", "ground", "soil",
                     "patch", "veg", "vegetable", "garden")


_A_COLD_THAT_IS_AN_ILLNESS = re.compile(
    r"\b(?:get|getting|got|shift|shifting|shake|shaking|fight|fighting|beat|beating|knock|"
    r"kill|killing|cure|curing|treat|treating|stop|stopping|prevent|preventing|dodge|dodging|"
    r"catch|catching|caught|come down with|coming down with|battling|suffering from)\s+"
    r"(?:rid of\s+|off\s+|over\s+|through\s+)?(?:a|an|this|that|my|his|her|their|the|another)\s+"
    r"(?:head |chest |bad |heavy |stinking |rotten |nasty |proper |lingering |summer )?colds?\b"
    r"|\b(?:cold|flu)\s+(?:medicine|medicines|medication|tablets?|syrup|remedies?|cure)\b"
    r"|\b(?:medicine|medicines|medication|tablets?|syrup|remedy|remedies|lemsip)"
    r"\s+(?:for|against)\s+(?:a\s+|the\s+|my\s+|this\s+|that\s+)?colds?\b"
    r"|\b(?:sore throat|runny nose|blocked nose|stuffy nose|sneez\w*|cough|coughing|fever|"
    r"virus|flu|cold sore|cold sores|cold and flu|cold or flu)\b"
    r"|\b(?:feeling|feel|felt|been|am|is|are)\s+(?:\w+\s+){0,2}(?:ill|unwell|poorly|sick)\b"
    r"|\b(?:keep|keeping|ward|stave|stay)\s+(?:away from\s+|off\s+)?(?:the\s+)?colds?\b"
    r"|\b(?:hands?|fingers?|fingertips?|feet|foot|toes?|ears?|nose)\s+"
    r"(?:are\s+|is\s+|get\s+|gets\s+|getting\s+|go\s+|goes\s+|going\s+)?cold\b"
    r"|\bsymptoms?\b")


def _the_cold_is_not_an_illness(understood):
    line = " ".join(str((understood or {}).get("clean") or (understood or {}).get("text")
                        or "").lower().split())
    return not _A_COLD_THAT_IS_AN_ILLNESS.search(line)


def _dig_over_bed(memory, understood):
    line = _words(understood)
    if _asks_when(line) and _has(line, "dig"):
        return _DIG_OVER_WHEN
    return _DIG_OVER_METHOD


_FROST_COVER = entry(
    "frost-cover",
    (("cover", "covering", "protect", "protection", "fleece", "cloche", "frost", "frosts",
      "cold", "freezing", "snap", "hardy", "tender"),
     ("plants", "plant", "seedlings", "seedling", "shoots", "tender plants", "veg",
      "vegetables", "tomatoes", "tomato", "potatoes", "spuds", "flowers", "flower", "shrubs",
      "shrub", "baskets", "hanging basket", "garden", "allotment", "greenhouse", "outside")),
    "Cover tender plants when frost is forecast, which means a night at 2C or below at ground "
    "level: the forecast for the town is often two or three degrees warmer than the garden, so "
    "watch for a clear, still night. Fleece, an old sheet, a cloche or a bucket of water beside "
    "them is enough, and take it off in the morning. Bring pots and hanging baskets in, water "
    "before a frost rather than after, and lift any spuds still in the ground.",
    guard=_the_cold_is_not_an_illness,
    avoid=("insurance", "third party", "third-party", "policy", "car", "van", "vehicle",
           "motorbike", "phone", "mobile", "travel", "seat", "pram", "buggy", "pushchair",
           "cot", "quilt", "duvet", "sofa", "cushion", "mattress", "table", "bbq cover",
           "barbecue cover",
           "can i freeze", "can you freeze", "can we freeze", "could i freeze",
           "how do i freeze", "how to freeze", "how do you freeze", "should i freeze",
           "is it ok to freeze", "is it okay to freeze", "freezer", "defrost", "thaw",
           "cooked", "mashed", "leftover", "left over", "recipe", "batch cook"),
    bias=2)

ENTRIES = SOW_ENTRIES + GROW_ENTRIES + _plant_entries() + [_FROST_COVER, 

    entry("outdoor-flowers-dropping",
          (("outdoor plant", "outdoor plants", "outdoors", "garden plant", "garden plants",
            "border", "bush", "bushes", "shrub", "shrubs", "shrubbery", "hedge", "patio plant",
            "rockery", "climber", "clematis", "hydrangea", "hydrangeas", "wisteria", "lupin",
            "lupins", "dahlia", "dahlias", "hanging basket", "flower bed", "flowerbed",
            "bedding plant", "bedding plants", "perennial", "perennials", "outside",
            "roses", "rose bush", "climbing rose", "climbing roses", "lavender"),
           ("dropping", "dropped", "drops", "drop", "losing", "lost", "lose", "falling",
            "fallen", "fell", "shedding", "shed", "dying", "die", "flowers",
            "flower", "buds", "blooms")),
          ("Open flowers in a garden drop when their flush is over, so deadhead down to the next "
           "bud and most plants come again in a few weeks. Buds that fall before they open are a "
           "shock rather than age: dry roots are the commonest - water deeply once and mulch - "
           "then a cold night, strong wind, or greenfly and caterpillars, which you find by "
           "opening one fallen bud. Put that one thing right before you feed anything."),
          avoid=("houseplant", "house plant", "houseplants", "indoor", "windowsill",
                 "orchid", "orchids", "tomato", "tomatoes", "courgette", "courgettes",
                 "strawberry", "strawberries", "chilli", "chillies", "chili", "pepper",
                 "peppers", "cucumber", "cucumbers", "pumpkin", "pumpkins", "marrow",
                 "aubergine", "aubergines", "peas", "beans", "runner", "broad bean",
                 "leaves", "leaf", "yellow", "yellowing", "brown", "brown tips", "tips",
                 "wilting", "wilt", "mould", "mold", "seed", "seeds", "sow", "prune",
                 "cut back", "buy", "gift", "present",
                 "bread", "cake", "cakes", "dough", "loaf", "loaves", "sponge", "souffle",
                 "soufflé", "pastry", "bun", "buns", "scone", "scones", "meringue", "batter",
                 "risen", "proving", "proved", "the oven", "baked", "bake", "baking",
                 "no flowers", "not flowering", "no blooms", "no buds", "no flower",
                 "flowers died", "flower died", "blooms died", "is dead", "looks dead",
                 "dig", "digging", "dig over", "double dig", "spade", "spading", "fork",
                 "forking", "weed", "weeding", "hoe", "hoeing", "trowel", "turn the soil",
                 "frost", "frosts", "frosty", "cold spell", "cold snap", "cold night",
                 "cold weather", "protect from", "protect my", "fleece", "winter",
                 "frozen", "freezing", "froze"),
          bias=3),

    entry("herb-pruning",
          (("basil", "mint", "parsley", "coriander", "cilantro", "chives", "dill", "oregano",
            "thyme", "rosemary", "sage", "tarragon", "herb", "herbs"),
           ("prune", "pruning", "pinch", "pinching", "pinch out", "top", "topping", "trim",
            "trimming", "cut back", "woody", "wooden", "leggy", "flowered", "flowering",
            "bolted", "bolting", "gone to seed", "harvest", "harvesting", "keep it bushy",
            "stop it going woody", "going woody", "gone woody",
            "cut", "cutting", "snip", "snipping", "back",
            "winter", "winters", "over winter", "over the winter", "overwinter", "overwintering",
            "frost", "frosts", "coming back", "come back", "comes back", "survive", "survives",
            "die back", "dies back", "died back", "perennial", "perennials", "going over",
            "keep going", "keeps going", "keep it going")),
          _herbs,
          avoid=("keep alive", "keep it alive", "yellow", "yellowing", "wilt", "wilted", "wilting",
                 "drooping", "fridge", "freeze", "frozen", "dry them", "drying", "dried",
                 "pesto", "sauce", "recipe", "plant it out", "when do i sow",
                 "cuttings", "take cuttings", "taking cuttings", "propagate", "propagating",
                 "propagation", "root a cutting",
                 "rosemary bush", "thyme bush", "sage bush", "oregano bush", "lavender bush",
                 "herb bush", "bushes", "shrub", "shrubs", "hedge", "hedges",
                 "can i grow", "what can i grow", "what herbs can i", "which herbs", "grow in",
                 "growing in", "grow on", "growing on"),
          bias=1),
    entry("mint-spreading",
          (("mint", "mint plant", "mint plants"),
           ("spread", "spreads", "spreading", "taken over", "took over", "taking over",
            "everywhere", "invasive", "contain", "containing", "control", "stop it", "keep it in",
            "border", "pot", "bucket", "root barrier")),
          _HERB_SPREAD,
          avoid=("mint sauce", "mint tea", "mint julep", "recipe", "cocktail", "chocolate",
                 "dried", "fridge", "freeze"),
          bias=1),
    entry("seedlings-leggy",
          (("seedling", "seedlings", "seed", "seeds", "sowing", "sowed", "propagator",
            "windowsill", "tomato", "tomatoes", "cabbage", "lettuce", "cress"),
           ("leggy", "spindly", "straggly", "stretched", "stretching", "tall and thin",
            "fallen over", "falling over", "flopped", "flopping", "pale and tall",
            "thin and tall")),
          _seedlings,
          avoid=("damping off", "mould", "mold", "mice", "slugs", "snails", "not coming up",
                 "died", "dying", "yellow", "wilting", "yellow", "when do i sow", "how deep"),
          bias=1),
    entry("cactus-soft",
          (("cactus", "cacti", "succulent", "succulents", "aloe", "agave", "jade plant",
            "christmas cactus", "echeveria"),
           ("soft", "squishy", "soggy", "mushy", "translucent", "rotting", "rotted", "rot",
            "collapse", "collapsed", "leaning over", "brown at the base")),
          _cactus_soft,
          avoid=("yellow", "yellowing", "brown tips", "brown tip", "wrinkled", "shrivelled",
                 "shrivelled up", "thin", "not growing", "flower", "repot", "how often"),
          bias=2),
    entry("basil-yellow-leaves",
          (("basil", "basil plant", "basil plants"),
           ("yellow", "yellowing", "dying", "drooping", "wilted", "turning", "leaves", "brown",
            "overwatered", "overwatering", "alive", "keep", "care", "water", "watering", "limp",
            "look after", "looking after", "care for", "caring for", "keep it alive")),
          ("Yellow basil leaves are usually too much water and too little sun: it wants drainage, "
           "warmth and a sunny windowsill, and it hates sitting in a wet pot. Let the top of the soil "
           "dry out, move it somewhere brighter, and pinch the tops to keep it bushy."),
          avoid=("eating my", "eating the", "ate my", "eaten", "eats", "holes", "holes in",
                 "nibbled", "pest", "pests", "infestation", "greenfly", "blackfly", "aphid",
                 "aphids", "caterpillar", "caterpillars", "slug", "slugs", "snail", "snails",
                 "flies", "gnats", "mould", "mold", "not growing", "dropping", "dropped")),
    entry("houseplant-yellow-leaves",
          (("houseplant", "houseplants", "house plant", "house plants",
            "peace lily", "monstera", "spider plant", "orchid", "fern", "succulent", "cactus"),
           ("yellow", "yellowing", "leaves",
            "yellow leaves", "leaves are yellow", "leaves going yellow", "leaves turning yellow",
            "leaves are turning yellow", "leaves have gone yellow", "leaves go yellow")),
          "Overwatering is the usual cause: yellow, soft leaves on a plant in soggy compost means "
          "stop watering and let the top inch of soil dry out, and check the pot has holes. Yellow "
          "lower leaves that are dry and crisp are the other story — that is just age, or a plant "
          "that needs feeding.",
          avoid=("tomato", "tomatoes", "basil", "lawn", "grass", "tree", "rose", "roses",
                 "cucumber", "courgette", "pepper", "chilli", "outside", "garden bed",
                 "brown", "black tips", "crisp", "tips", "edges"),
          bias=2),
    entry("houseplant-light",
          (("light", "sunlight", "more light", "brighter", "bright", "sunny", "sun", "sunshine",
            "window", "windowsill", "window sill", "direct sun", "shade", "shady", "dark corner",
            "dark room", "corner", "where should i put"),
           ("monstera", "houseplant", "houseplants", "house plant", "house plants", "indoor plant",
            "indoor plants", "pot plant", "pot plants", "peace lily", "spider plant", "snake plant",
            "pothos", "orchid", "fern", "cactus", "succulent", "calathea", "zz plant", "dracaena",
            "yucca", "palm", "fiddle leaf", "rubber plant", "plant", "plants")),
          "Bright but out of direct midday sun is what most houseplants want: an east window, or a "
          "metre or two back from a south or west one. Move it closer to the glass if the stems "
          "are pale and stretched with gaps between the leaves, and further back if the leaves "
          "have brown scorched patches on the side facing the window. Turn the pot a quarter "
          "turn each time you water so it grows evenly, and give it a few weeks to settle - a "
          "plant moved into suddenly stronger light can scorch before it adjusts.",
          avoid=("tomato", "tomatoes", "basil", "lawn", "grass", "tree", "trees", "rose", "roses",
                 "cucumber", "courgette", "pepper", "chilli", "outside", "garden bed", "lamp",
                 "ceiling", "fairy", "light fitting", "light bulb", "headlight", "sun cream",
                 "sunscreen", "sunburn",
                 "garden", "gardens", "gardener", "border", "flowerbed", "flower bed",
                 "allotment", "outdoors", "outdoor", "back garden", "front garden", "veg patch",
                 "vegetable patch", "shrub", "shrubs", "hedge", "perennial", "perennials",
                 "flower bed", "flowerbed", "planting flowers", "plant flowers",
                 "plant some flowers", "planting out", "plant out", "seedlings",
                 "bed", "beds", "border", "borders", "flowerbed", "flower bed", "garden",
                 "soil", "ground", "allotment", "veg", "vegetable", "vegetables",
                 "plant shade", "plants shade",
                 "fell", "fallen", "falls", "dropped", "dropping", "knocked", "tipped",
                 "broke", "broken", "cracked", "smashed", "shattered", "spilled", "spilt",
                 "upside down", "on its side"),
          bias=2),
    entry("houseplant-brown-tips",
          (("houseplant", "houseplants", "house plant", "house plants", "plant", "plants", "tips",
            "leaf tips", "peace lily", "monstera", "spider plant", "orchid", "fern", "succulent",
            "cactus"),
           ("brown tips", "brown edges", "brown at the tips", "brown", "crisp", "black tips",
            "dried out edges",
            "brown at the tip", "going brown at the tips", "going brown at the tip",
            "browning at the tips", "tips turning brown", "tips are turning brown",
            "tips of the leaves", "tips of my leaves", "tips of my plant", "tips of my plants",
            "tips of my plant's leaves", "tips of the plant's leaves", "brown tips on",
            "brown round the edges",
            "brown around the edges", "crispy tips", "crispy leaf tips",
            "edges of the leaves are brown", "leaf edges are brown")),
          "Brown, crisp tips are usually the water: tap water left to stand overnight, or "
          "rainwater, takes the fluoride and salts out that build up at the leaf edges. Dry air "
          "and letting the compost go bone dry do the same, so check both and cut the tips off "
          "with a clean pair of scissors — the leaf keeps going.",
          avoid=("tomato", "tomatoes", "basil", "lawn", "grass", "tree", "rose", "roses",
                 "cucumber", "courgette", "pepper", "chilli", "outside", "garden bed",
                 "yellow", "bottom", "base of the plant"),
          bias=1),

    entry("balcony-vegetables", (("vegetables", "veg"), "balcony", ("pots", "easy", "growing")),
          ("Salad leaves, cherry tomatoes, chillies, herbs, radishes and dwarf beans all do well in "
           "pots. Use containers at least 30cm deep with drainage holes, and water daily in summer, "
           "because pots dry out fast."),
          avoid=("how long", "take to grow", "long to grow", "weeks", "months", "when will",
                 "when are", "when should", "when do", "harvest", "ready", "ripe",
                 "tomato", "tomatoes", "tomato plant", "tomato plants"),
          bias=1),
    entry("crop-weeks-named",
          (("potato", "potatoes", "spud", "spuds", "carrot", "carrots", "onion", "onions",
            "leek", "leeks", "parsnip", "parsnips", "beetroot", "radish", "radishes",
            "lettuce", "spinach", "kale", "cabbage", "broccoli", "cauliflower", "turnip",
            "turnips", "swede", "courgette", "courgettes", "marrow", "pumpkin", "pumpkins",
            "squash", "sweetcorn", "sweet corn", "pea", "peas", "bean", "beans",
            "runner bean", "runner beans", "broad bean", "broad beans", "french bean",
            "french beans", "dwarf bean", "dwarf beans", "tomato", "tomatoes", "chilli",
            "chillies", "chili", "chilis", "cucumber", "cucumbers", "garlic", "strawberry",
            "strawberries", "aubergine", "aubergines", "pepper", "peppers", "sprouts",
            "brussels", "spring onion", "spring onions", "salad leaves"),
           ("how long", "take to grow", "long to grow", "long before", "how many weeks",
            "weeks", "how soon", "time to grow", "grow", "ready", "harvest",
            "harvested", "pick", "picking", "crop", "cropping")),
          _crop_weeks_reply,
          avoid=("boil", "boiled", "boiling", "cook", "cooked", "cooking", "roast", "roasted",
                 "roasting", "mash", "mashed", "chips", "oven", "bake", "baked", "baking",
                 "steam", "steamed", "fry", "fried", "microwave", "recipe", "peel", "peeled",
                 "minutes", "jacket", "chit", "chitting", "chitted", "blight", "disease",
                 "rust", "mould", "rot", "this month", "month", "january", "february", "march",
                 "soften", "softens", "softened", "softening", "tender", "tenderise",
                 "simmer", "simmered", "blanch", "blanched", "parboil", "parboiled",
                 "brown in a pan", "brown the onions", "until crisp", "al dente", "stir fry",
                 "saucepan", "hob", "drain", "drained", "pan of", "in a pan",
                 "con carne", "con carni", "chilli con", "bolognese", "stew", "casserole",
                 ) + A_PAN_LINE + (
                 "april", "may", "june", "july", "august", "september", "october", "november",
                 "december", "when do i sow", "when should i sow", "when do i plant",
                 "when should i plant", "what month", "sow", "sowing", "plant out",
                 "spacing", "how far apart", "feed", "fertiliser", "compost", "pot", "pots",
                 "indoors", "windowsill", "greenhouse", "freeze", "frozen", "keep", "store",
                 "why", "yellow", "wilting", "holes", "died", "dying", "not growing",
                 "how do i grow", "how to grow", "how do you grow", "how can i grow",
                 "how should i grow", "growing tips", "tips for growing", "best way to grow",
                 "beginner", "beginners", "for beginners", "first time", "new to growing",
                 "start growing", "getting started",
                 "pick a good", "pick good", "picking a good", "pick the best", "pick a ripe",
                 "choose a good", "choosing a good", "choose the best", "choose a ripe",
                 "how do i pick", "how do i choose", "how to pick", "how to choose",
                 "which to pick", "which one to pick", "good one", "good ones", "best one"),
          bias=2),
    entry("crop-weeks",
          (("grow", "growing", "grown", "plant", "planted", "planting", "sow", "sowed", "sowing",
            "seed", "seeds", "crop", "crops", "vegetables", "veg"),
           ("how long", "take to grow", "long to grow", "weeks", "months", "how many weeks",
            "how many days", "time to", "how soon")),
          "Quick from seed: salad leaves and radishes in 4 to 6 weeks, spring onions 8, dwarf "
          "beans 10 to 12. Tomatoes, courgettes and chillies take 12 to 16 weeks from sowing, and "
          "new potatoes 10 to 12 from planting (maincrop 18 to 20). Check the seed packet for the "
          "variety, because a fortnight either way is normal, and sow a small row every three "
          "weeks so the crops arrive in a trickle rather than all at once.",
          avoid=("houseplant", "houseplants", "indoor", "monstera", "orchid", "orchids", "fern",
                 "cactus", "succulent", "basil", "cook", "cooking", "boil", "boiled", "roast",
                 "roasted", "oven", "steam", "steamed", "recipe", "eat", "keeping", "store",
                 "bean sprouts", "sprouts", "sprout", "beard", "hair", "business", "crystal",
                 "onion", "onions", "potato", "potatoes", "carrot", "carrots", "garlic", "tomato",
                 "tomatoes", "broccoli", "cabbage", "kale", "pea", "peas", "bean", "beans",
                 "beetroot", "lettuce", "lettuces", "radish", "radishes", "courgette",
                 "courgettes", "leek", "leeks", "parsnip", "parsnips", "spinach", "rhubarb",
                 "strawberry", "strawberries", "apple", "pear", "chilli", "chillies",
                 "cucumber", "pumpkin", "squash", "sweetcorn", "corn", "turnip", "swede",
                 "harvest", "harvested", "harvesting", "lift", "lifting", "ripe", "ready",
                 "grass", "lawn", "turf", "moss", "wildflower", "green manure",
                 "this month", "this week", "right now", "plant now", "planting now",
                 "sow now", "january", "february", "march", "april", "may", "june", "july",
                 "august", "september", "october", "november", "december", "month by month",
                 "bulb", "bulbs", "tulip", "tulips", "daffodil", "daffodils", "allium",
                 "alliums", "crocus", "snowdrop", "snowdrops", "bulb planting")),
    entry("tulip-bulbs", ("bulbs", "tulip", "planting"),
          ("Plant tulip bulbs in November, later than daffodils, which go in from September: a cold "
           "spell helps them flower well. Plant them three times their own depth and pointy end up.")),
    entry("allotment-overgrown",
          (("allotment", "allotments", "plot"),
           ("overgrown", "weeds", "weedy", "clear", "start", "look after", "care", "first",
            "new plot", "take on", "took on")),
          ("Cover most of it with cardboard and compost to kill the weeds while you work on one bed "
           "at a time, and start with the bit you can see from the gate. Clear, dig and plant that "
           "bed this month, then move on; trying to do the whole plot at once is how people give up.")),
    entry("houseplants-watering",
          (("houseplants", "house plants", "house plant", "houseplant", "indoor plants",
            "indoor plant", "pot plants", "pot plant", "care", "overwatering",
            "monstera", "peace lily", "spider plant", "snake plant", "pothos", "fern", "orchid",
            "calathea", "zz plant", "dracaena", "yucca", "fiddle leaf", "rubber plant",
            "poinsettia", "cyclamen", "amaryllis", "african violet", "aloe", "jade plant",
            "anthurium", "kalanchoe", "begonia", "hyacinth"),
           ("water", "watering", "how often", "how much", "look after", "care", "care for",
            "dying", "die", "dies", "dead", "drooping", "droopy", "yellow", "leaves", "light",
            "root rot",
            "keep", "keeping", "alive", "thriving", "healthy", "happy", "last",
            "look sad", "looks sad", "looking sad", "unhappy", "miserable",
            "sorry for itself", "sulking", "sulky")),
          ("Water when the top couple of centimetres of compost is dry, not on a fixed day, and let "
           "it drain away rather than sitting in water. Most houseplants die of too much water rather "
           "than too little: a pot with no drainage hole, or a saucer left full, rots the roots and "
           "the leaves go yellow and drop. If the compost smells sour, repot in fresh compost and "
           "water less; if it is bone dry and light, soak the pot in a bowl for ten minutes. Beyond "
           "that it is light - most want a bright spot out of direct sun - and a feed every few "
           "weeks in spring and summer only."),
           avoid=("lawn", "lawns", "grass", "mow", "mowing", "hanging basket",
                  "hanging baskets", "window box", "window boxes",
                  "border", "borders", "allotment", "plot", "beds", "roses", "rose",
                  "hydrangea", "lavender", "tomato", "tomatoes", "potato", "potatoes",
                  "tree", "trees", "shrub", "shrubs", "hedge", "hedges", "seeds", "seedlings",
                  "sow", "sowing", "greenhouse", "compost heap", "weeds", "slug", "slugs",
                  "snails", "cats", "cat", "dog", "dogs", "puppy", "puppies", "pup",
                  "kitten", "kittens", "rabbit", "hamster", "guinea pig", "budgie",
                  "tattoo", "tattoos"),
           guard=_the_care_is_for_a_person),
    entry("watering-plants",
          (("plants", "plant", "houseplants", "houseplant", "pots", "containers"),
           ("how often", "how much", "water", "watering", "away on holiday", "holiday",
            "every day", "daily")),
          ("Check the soil before you water, not the calendar: push a finger in and water only when "
           "the top few centimetres are dry, then water until it runs out of the bottom. Plants in "
           "pots need it far more often than plants in a border, and in hot weather a big soak twice "
           "a week beats a sprinkle every day, because it gets water down to the roots."),
          avoid=("yellow", "yellowing", "brown", "drooping", "droopy", "dying", "turning",
                 "photosynthesis", "basil", "hydrangea", "tomato", "tomatoes",
                 "drink", "drinks", "drinking", "absorb", "stems", "stem",
                 "feed", "feeds", "feeding", "fertiliser", "fertilizer", "plant food",
                 "nutrients")),
    entry("watering-garden",
          (("garden", "beds", "bed", "my beds", "the beds", "flower beds", "raised beds",
            "border", "borders", "shrubs", "shrub", "flowers",
            "new plants", "newly planted", "hanging baskets", "hanging basket",
            "why does my soil", "why is my soil", "why has my soil", "why are my beds",
            "soil dry out", "soil dries", "my ground", "allotment plot", "veg plot",
            "garden plot", "allotment", "planters",
            "planter"),
           ("how often", "how much", "water", "watering", "every day", "daily", "drought",
            "dry soil", "the dry soil", "soil dry",
            "hot weather", "heatwave", "hose", "hosepipe", "sprinkler", "ban",
            "dried out", "drying out", "dries out", "dry out", "dried up", "gone dry",
            "keeps drying", "bone dry", "parched", "cracked", "cracking",
            "dry", "too dry", "so dry", "is dry", "very dry", "dry and", "dries", "drying")),
          _a_bed_that_dries_out,
          avoid=("wash", "washing", "washed", "change", "changing", "sheets", "sheet", "duvet",
                 "pillow", "pillows", "pillowcase", "mattress", "linen", "laundry",
                 "washing machine", "tumble dryer", "quilt", "blanket",
                 "lawn", "grass", "turf", "mow", "mowing", "mow the", "weed", "weeds", "weeding",
                 "feed", "feeds", "feeding", "fertiliser", "fertilizer", "plant food",
                 "tomato", "tomatoes", "cactus", "succulent", "indoor", "houseplant",
                 "houseplants", "orchid", "monstera",
                 "gravel", "shingle", "chippings", "bark", "bark chippings", "mulch",
                 "topsoil", "top soil", "compost", "bags of", "tonnes of", "tons of",
                 "sheets", "sheet", "duvet", "pillow", "pillowcase", "pillowcases",
                 "mattress", "wash my bedding", "clean my bedding", "clean the bedding",
                 "cleaning the bedding", "bedding smells", "laundry", "washing machine",
                 "tumble dryer",
                 "pyjamas", "nightie", "linen",
                 "weigh", "weighs", "weighing", "how heavy", "kg", "kilos", "kilogram",
                 "kilograms", "lbs", "weight")),
    entry("repot-a-plant",
          (("repot", "repotting", "pot bound", "root bound", "bigger pot"),
           ("plant", "plants", "pot", "houseplant", "roots", "soil", "compost")),
          ("Move it up one pot size, no bigger: roots circling the bottom of the old pot, or water "
           "running straight through, mean it is ready, and a pot that is far too big holds water "
           "round the roots and rots them. Use fresh compost, tease the roots out a little, and keep "
           "it out of direct sun for a week after.")),
    entry("take-cuttings",
          (("take a cutting", "take cuttings", "taking cuttings", "cutting", "cuttings",
            "softwood cutting", "softwood cuttings", "stem cutting", "root a cutting",
            "root cuttings", "strike a cutting", "propagate", "propagating", "propagation",
            "root in water", "roots in water"),
           ("rose", "roses", "geranium", "geraniums", "pelargonium", "pelargoniums", "fuchsia",
            "fuchsias", "plant", "plants", "shrub", "shrubs", "lavender", "hydrangea",
            "houseplant", "houseplants", "house plant", "house plants", "indoor plant", "herb",
            "herbs", "busy lizzie", "impatiens", "begonia", "begonias", "salvia", "verbena",
            "penstemon", "hebe", "buddleia", "jasmine", "honeysuckle", "ivy", "trailing plant",
            "monstera", "pothos", "spider plant", "snake plant", "tradescantia"),
           ("water", "in water", "glass of water", "jar of water", "glass", "jar",
            "how do i take a cutting", "how do i take cuttings", "how to take a cutting",
            "how to take cuttings", "how do i root a cutting", "how do i root cuttings",
            "how to root a cutting", "how do i strike a cutting", "how do i propagate",
            "how to propagate", "propagate a plant", "how do you take cuttings",
            "how do you propagate", "when do i take cuttings", "when should i take cuttings",
            "when do you take cuttings", "best time to take cuttings",
            "best time to take a cutting", "can i propagate",
            "how do i take a softwood cutting", "how to take a softwood cutting",
            "how do i take a stem cutting", "how do i take root cuttings",
            "how do i take some cuttings", "how do i root some cuttings",
            "when do i take a cutting", "when to take cuttings", "when is the best time to take",
            "what time of year do i take cuttings", "what time of year should i take cuttings",
            "what month do i take cuttings")),
          _cutting_reply,
          avoid=("grass", "lawn", "mow", "mowing", "hedge", "hedges", "cost", "costs", "spending",
                 "budget", "cake", "cook", "cooking", "meat", "wood", "steel", "metal", "wire",
                 "hair", "out", "off", "down", "short", "fine",
                 "cut back", "cutting back", "cut it back", "prune", "pruning", "pruned",
                 "deadhead", "deadheading", "hard back", "trim", "trimming"),
          ),
    entry("divide-perennials",
          (("divide", "dividing", "division", "split", "splitting", "lift and divide",
            "how do i divide", "when do i divide", "when should i divide", "how do i split",
            "when do i split", "when should i split", "separate", "separating",
            "taking over", "taking it over", "taken over", "got huge", "grown huge",
            "too big", "outgrown", "outgrowing", "overcrowded"),
           ("perennial", "perennials", "hosta", "hostas", "daylily", "day lilies", "day lily",
            "clump", "clumps", "border plant", "border plants", "hardy geranium", "phlox",
            "crocosmia", "montbretia", "shasta daisy", "heuchera", "lily", "lilies", "sedge",
            "ornamental grass", "bamboo", "rhubarb", "strawberry", "strawberries", "plant", "plants",
            "shrub", "shrubs")),
          "Water the clump the day before, then fork it out on all sides and lever it up. Two "
          "forks back to back in the middle, pushed away from each other, part most clumps without "
          "cutting anything; a spade or an old bread knife does the rest. Shake off the loose "
          "soil, cut back the old foliage, and replant each piece at the depth it was growing, then "
          "water it in and keep it watered for a fortnight. Divide summer-flowering perennials in "
          "spring and spring-flowering ones in autumn, and hostas whenever they are in leaf but not "
          "in flower.",
          avoid=("bill", "bills", "money", "rent", "cost", "costs", "tax", "cheque", "by 2",
                 "by 10", "by ten", "sum", "sums", "maths", "math", "number", "fraction",
                 "decimal", "percentage", "long division", "divide by", "dividing numbers",
                 "up with", "from", "husband", "wife", "partner", "expenses",
                 "bamboo", "bamboos", "rhizome", "rhizomes"),
          ),
    entry("houseplant-compost",
          (("compost", "potting compost", "potting mix", "potting soil", "peat", "peat free",
            "perlite", "grit", "bark", "soil mix"),
           ("houseplant", "houseplants", "house plant", "house plants", "indoor plant",
            "indoor plants", "for my plant", "pot", "pots", "repot", "repotting", "best",
            "which one", "what kind", "what sort")),
          "Use a peat-free multi-purpose with a good third of perlite or grit stirred through for "
          "drainage, or a ready-made houseplant mix, which is the same thing in one bag. Garden "
          "soil in a pot sets like concrete and brings in pests, so leave it outside. Orchids want "
          "bark chips and cacti want gritty cactus compost; seedling compost is too light for a "
          "plant that lives in the same pot for years.",
          avoid=("heap", "bin", "kitchen", "food waste", "make your own", "make my own",
                 "turn the compost", "smells", "smell", "rats", "flies", "allotment"),
          ),
    entry("tomato-feed",
          (("tomato", "tomatoes", "tomato plant", "tomato plants", "tomato seedlings"),
           ("feed", "feeds", "feeding", "fertiliser", "fertilizer", "tomato feed", "potash",
            "food")),
          "Start feeding when the first truss of flowers has set fruit, then weekly: a high-potash "
          "tomato feed, diluted as the bottle says, watered onto damp soil rather than dry. Too much "
          "nitrogen before that gives you a big leafy plant and no tomatoes, and a plant in fresh "
          "grow bag compost usually needs nothing for the first six weeks.",
          ask=("tomato", "tomatoes"),
          avoid=("baby", "babies", "breast", "newborn", "ketchup", "sauce", "recipe", "recipes",
                 "chutney", "pizza")),
    entry("grow-in-a-pot",
          (OTHER_CROPS + ("tomato", "tomatoes"),
           ("pot", "pots", "container", "containers", "planter", "planters", "grow bag",
            "grow bags", "growbag", "bucket", "tub", "basket", "hanging basket", "window box",
            "windowbox", "raised bed", "raised beds", "compost bag", "size pot", "big pot",
            "growing bag", "growing bags", "potatoes in a bag", "potatoes in bags",
            "potato in a bag", "potato in bags", "trug")),
          ("The pot has to be deep enough and drain: 30cm deep with holes in the bottom for salad, "
           "herbs, radishes and dwarf beans, 40cm and 30 litres or more for potatoes, a courgette or "
           "a tomato, and strawberries are fine in a 20cm pot or a hanging basket. Use fresh "
           "multipurpose compost, water when the top finger-depth feels dry (twice a day in a "
           "heatwave, because a small pot dries out fast), and feed weekly once flowers open: "
           "bagged compost runs out of food in about six weeks."),
          ask=("grow", "growing", "grow my own", "plant", "planting", "sow", "sowing", "can i",
               "could i", "how", "what size", "which pot", "best", "good"),
          bias=1,
          avoid=("houseplant", "houseplants", "pot plant", "monstera", "orchid", "fern", "cactus",
                 "succulent", "peace lily", "repot", "repotting", "root bound", "rootbound",
                 "pot bound", "sick", "dying", "yellow", "wilting", "not growing", "isnt growing",
                 "isn't growing", "stopped growing", "recipe", "recipes", "cook", "cooking",
                 "roast", "soup", "salad dressing", "store", "storing",
                 "slimy", "going slimy", "keep fresh", "keeps fresh", "keep it fresh",
                 "keep them fresh", "stays fresh", "stay fresh", "last longer", "lasts longer",
                 "last a week", "goes off", "gone off", "go off", "fridge", "freezer", "freeze",
                 "waste", "wasting", "use up", "washed", "wash the leaves",
                 "keep a bag", "keep the bag", "keep a punnet", "how do i keep",
                 "keeping a bag", "make it last", "make them last")
          + DISH_ASK),
    entry("grow-tomatoes", ("tomatoes", "growing", "pots", ("plants")),
          ("Sow indoors in March or April and plant out in early June, once the nights stay above "
           "10C. Give them sun, a big pot or grow bag, and water at the base regularly, because "
           "irregular watering is what splits them. Pinch out side shoots on cordon varieties, "
           "feed weekly once the first truss sets, and pick as soon as they are ripe."),
          avoid=("pot plant", "pot plants", "houseplant", "houseplants", "indoor", "monstera",
                 "orchid", "fern", "cactus", "succulent", "peace lily", OTHER_CROPS,
                 "herb", "herbs", "basil", "rosemary", "thyme", "mint", "parsley", "chives",
                 "coriander", "cilantro", "oregano", "dill", "sage", "tarragon",
                 "not growing", "isnt growing", "isn't growing", "stopped growing", "no growth",
                 "wont grow", "won't grow", "not grown", "stunted",
                 "wilting", "wilted", "wilt", "drooping", "droopy", "limp", "flopping",
                 "blight", "blighted", "mildew", "mould", "mold", "rot", "rotting", "disease",
                 "diseased", "infected", "aphids", "blackfly", "whitefly", "spots", "spotting")),
    entry("lawn-care",
          (("lawn", "grass", "turf"),
           GONE_WILD + (
            "mow", "mowing", "cut", "cutting", "how often", "patchy", "patches", "bare", "bald",
            "care", "look after", "feed", "feeding", "level", "reseed", "scarify", "scarifying",
            "thatch", "thatching", "dethatch", "dethatching", "spiking", "spike", "compacted",
            "compaction", "hollow tine", "hollow tines", "aerated", "aeration", "raking out",
            "spongy", "reseeding", "oversow", "over sow", "sow grass",
            "aerate", "aerating", "autumn", "yellow", "yellowing", "brown",
            "browning", "dying",
            "dead", "died", "killed", "dead grass",
            "green", "greener", "greenest", "lush", "thick", "thicker",
            "dull", "pale", "pale green", "yellowish", "washed out", "faded", "tired", "thin",
            "not very green",
            "look good", "looking good", "looks good", "look nice", "looking nice",
            "looks nice", "look better", "looking better", "looks better", "nice lawn",
            "best lawn",
            "do about", "should i do", "what should i", "what can i", "can i do", "sort out",
            "sort", "improve", "fix", "advice", "help")),
          _lawn,
          avoid=("new lawn", "new grass", "new turf", "newly laid", "newly sown", "laid turf",
                 "turf laid", "seedbed", "grass seed", "just laid", "just turfed",
                 "moss", "mould", "mold", "weed", "weeds", "dandelion", "dandelions", "clover",
                 "daisy", "daisies", "ant", "ants", "mushroom", "mushrooms", "toadstool",
                 "mole", "moles", "dog", "fox", "foxes", "leatherjacket", "chafer", "worm",
                 "worms", "frost", "snow", "flooded", "waterlogged",
                 "mower", "mowers", "lawnmower", "lawnmowers", "lawn mower", "trimmer",
                 "trimmers", "strimmer", "strimmers", "scarifier", "robot", "hose",
                 "sprinkler", "blade", "blades", "roller", "edging", "edger")),
    entry("new-lawn-watering",
          (("new lawn", "new grass", "newly laid", "newly sown", "turf", "seedbed", "grass seed",
            "lawn from seed", "grass from seed", "sow a lawn", "sowing a lawn", "seed a lawn",
            "lawn seed"),
           ("water", "watering", "damp", "hose", "sprinkler", "often", "sow", "sowing", "seed",
            "care", "after", "keep", "walk", "grow", "growing", "start")),
          "Keep a new lawn damp, not soaked: a light sprinkle morning and evening for the first "
          "fortnight, then once a day, and once it is up, water deeply twice a week instead, which "
          "teaches the roots to go down. Do not let it dry out completely in that first month and "
          "do not walk on it; the first cut waits until it is about 5cm tall."),
    entry("tomato-watering",
          (("tomato", "tomatoes", "tomato plant", "tomato plants"),
           ("water", "watering", "watered", "how often", "every day", "daily", "twice a week",
            "once a week", "deeply", "when to water", "hosepipe", "hose",
            "wilting", "wilted", "wilt", "drooping", "droopy", "limp", "flopping")),
          "Water tomatoes deeply two or three times a week and let the top of the soil dry in "
          "between: a little every day keeps the roots shallow. Even watering is what stops split "
          "fruit and blossom end rot, and in a pot or grow bag in hot weather twice a day can be "
          "right. Water at the base in the morning, not over the leaves.",
          avoid=("yellow", "yellowing", "brown", "blight", "blossom end rot", "curling", "curl",
                 "split", "splitting", "feed", "feeds", "feeding", "fertiliser", "fertilizer",
                 "tomato feed", "potash", "ketchup", "sauce", "recipe", "recipes", "chutney",
                 "pizza", "pasta", "salad", "soup", "unripe", "ripen", "ripening", "green tomatoes",
                 "green tomato", "plant out", "pinch")),
    entry("lawn-watering",
          (("lawn", "grass", "turf"),
           ("water", "watering", "watered", "hose", "hosepipe", "sprinkler", "how often",
            "twice a week", "once a week", "every day", "daily", "drought", "dry spell",
            "heatwave", "hot weather"),
           ("water my lawn", "water the lawn", "water a lawn", "water lawn", "water my grass",
            "water the grass", "water grass", "watering my lawn", "watering the lawn",
            "watering grass", "water your lawn", "when to water")),
          ("Water a lawn deeply once a week rather than lightly every day: about a centimetre, or "
           "twenty minutes with a sprinkler, in the early morning. Grass roots follow the water "
           "down, so a weekly soak makes a lawn that shrugs off a dry spell, and in a real drought "
           "it is fine to let it go brown and come back."),
          avoid=("new lawn", "new grass", "new turf", "newly laid", "newly sown", "just laid",
                 "just turfed", "seedbed", "grass seed", "moss", "weeds", "mow", "mowing", "cut",
                 "cutting", "feed", "feeding", "patchy", "bare", "bald", "reseed", "scarify",
                 "aerate", "aerating", "aerated", "aeration", "spike", "spiking", "hollow tine",
                 "hollow tines", "thatch", "thatching", "top dress", "top dressing",
                 "laid turf", "we laid", "just turfed it", "turfed two", "new turf laid",
                 "scarifying", "scarified", "dethatch", "dethatching", "raking out", "spongy",
                 "compacted", "compaction", "reseeding", "oversow")),
    entry("lawn-moss",
          (("moss", "mossy"), ("lawn", "grass", "turf", "mow", "scarify", "spiking", "aerate")),
          ("Moss on a lawn means shade, drainage or compacted soil, not bad luck: rake or scarify it "
           "out, spike the lawn with a fork, and feed the grass so it thickens and takes the space "
           "back. Raise the mowing height and cut back whatever is shading it, and in autumn a "
           "forkful of grit in the worst spots keeps the surface draining.")),
    entry("moles",
          (("mole", "moles", "molehill", "molehills", "mole hill", "mole hills"),
           ("garden", "lawn", "grass", "turf", "flowerbed", "flower bed", "beds", "veg patch",
            "get rid", "rid of", "remove", "stop", "how do i", "they keep", "every day")),
          "Moles are after worms, so a lawn full of molehills is a sign of good soil: flatten the "
          "hills, mow the grass back over them and put the soil on a bed, and leave the traps and "
          "the mole catcher to a professional, because spring traps and poison are the only things "
          "that work and both are regulated. Sonic spikes, mothballs, windmills and chewing gum do "
          "nothing. They often move on by themselves once the worms go deeper in a dry spell.",
          avoid=("skin", "spot", "spots", "arm", "leg", "shoulder", "back", "face", "doctor",
                 "gp", "dermatologist", "melanoma", "check", "bean", "beans", "sauce",
                 "chocolate", "recipe", "cook", "eat", "edible", "salsa", "mole sauce",
                 "make mole", "make a mole", "mole poblano", "chicken mole", "turkey mole",
                 "mole negro", "mole verde", "mole amarillo",
                 "suspected", "spy", "police"), bias=1),
    entry("weeds",
          (("weed", "weeds", "weedy", "dandelion", "dandelions", "daisies", "clover", "plantain",
            "ragwort", "bindweed", "nettles", "brambles", "ground elder"),
           ("lawn", "grass", "turf", "patio", "path", "driveway", "gravel", "border", "bed",
            "beds", "garden", "allotment", "kill", "rid", "remove", "dig", "without chemicals",
            "come back", "keep coming", "return", "spread",
            "flower bed", "flower beds", "flowerbed", "flowerpot", "flowerpots", "flower",
            "flowers", "rose", "roses", "shrub", "shrubs", "choking", "choke", "choked",
            "smothering", "smothered", "strangling", "swamped", "taking over", "taken over",
            "overrun", "getting overrun", "everywhere", "springing up", "popping up")),
          ("Get the root, not the leaves: dandelions and plantains come back from a finger of "
           "taproot, and bindweed, ground elder and nettles from any white root left in the soil, so "
           "dig them out with a grubber or fork before they seed. On a lawn, feed and mow it properly "
           "and thick grass crowds them out; on a patio, path or gravel, hoe or flame them young, or "
           "pour boiling water over them. Cardboard and mulch starve a whole bed of them in a season, "
           "and a weedkiller is the last resort, never on a windy day."),
          avoid=("overgrown", "allotment", "allotments", "plot", "veg patch", "veggie patch",
                 "cat", "cats", "kitten", "kittens", "dog", "dogs", "puppy", "puppies",
                 "pet", "pets", "rabbit", "hamster",
                 "moss", "mossy", "algae", "lichen"),
          bias=1),
    entry("dig-a-hole",
          (("dig a hole", "digging a hole", "dug a hole", "dig the hole", "digging the hole",
            "how deep should i dig", "how wide should i dig", "dig", "digging", "dug"),
           ("hole", "holes", "planting hole", "plant", "plants", "shrub", "tree", "rose",
            "bush", "climber", "hedge", "bare root")),
          ("Dig it square rather than round, about twice as wide as the root ball and the same "
           "depth as the pot it came in: a round hole makes the roots circle, and a hole deeper "
           "than the root leaves the plant sitting in a sump that fills with water. Keep the top "
           "soil to one side, rough up the bottom and sides of the hole with a fork so the roots "
           "can get out, plant it so the old soil mark sits level with the ground, firm it in "
           "with your heel and water it well."),
          avoid=("pond", "ponds", "trench", "drain", "drainage", "grave", "post", "posts",
                 "fence", "gate", "over the", "dig over", "dig in", "dig out", "dig up",
                 "potato", "potatoes", "trampoline", "weed", "weeds"),
          bias=1),
    entry("dig-over-bed",
          (("dig over", "digging over", "dug over", "double dig", "double digging",
            "fork over", "dig in", "digging in", "dug in", "fork in", "turn over",
            "turning over", "dig", "digging", "dug", "fork", "forks", "forking", "turning"),
           ("bed", "beds", "border", "borders", "flower bed", "flower beds", "soil", "ground",
            "compost", "manure", "garden", "plot", "allotment", "veg", "vegetable", "patch",
            "over", "turned")),
          _dig_over_bed,
          avoid=("dizzy", "dizziness", "spins", "spinning", "spinning round", "vertigo",
                 "giddy", "light headed", "lightheaded", "nauseous", "nausea", "room spins",
                 "my back", "back hurts", "back ache", "backache", "aches", "aching",
                 "hip", "hips", "spine", "shoulder", "shoulders", "neck", "sore", "stiff",
                 "hurts", "hurting", "in bed", "at night", "wake", "wakes", "woke", "sleep",
                 "hole", "holes", "pond", "ponds", "trench", "trenches", "grave", "post", "posts",
                 "fence", "path", "patio", "foundation", "footings", "sandpit", "drain",
                 "drainage", "plotting")),
    entry("dig-out-shrub",
          (("dig out", "digging out", "dug out", "dig up", "digging up", "dug up",
            "how do i get rid of", "how do i remove"),
           ("shrub", "shrubs", "bush", "bushes", "tree", "stump", "conifer", "laurel",
            "hedge", "roots", "rootball", "root ball")),
          ("Cut the shrub down to about 30cm of stem first so you can see what you are doing, "
           "then dig a trench a spade's width outside the stems and cut straight down through "
           "the roots all the way round until the rootball rocks. Lever it out with the spade "
           "rather than pulling at it, and take the big roots with it - a laurel or a willow "
           "left with roots in the ground sends up suckers for years."),
          avoid=("stain", "smell", "rubbish", "tip", "council", "bins", "mould", "mildew",
                 "grind", "grinder", "stump grinder", "chemical", "weedkiller", "dead",
                 "from my", "off my"),
          bias=1),
    entry("dig-a-pond",
          (("dig", "digging", "dug", "build", "building", "make", "put in", "how deep",
            "how big", "how large", "how wide", "size", "depth"),
           ("pond", "ponds", "water feature", "wildlife pond", "water garden")),
          ("Dig it 60cm deep in the middle with a shelf 20 to 30cm deep and 30cm wide around "
           "the edge for marginal plants, and go at least a metre across - a pond shallower than "
           "that freezes solid and has nowhere for anything to live. The rim is the part people "
           "get wrong: keep it level all the way round, checked with a straight edge and a "
           "spirit level before the liner goes in, or the water shows one edge of it. Line it "
           "with butyl rather than cheap polythene, leave the liner to settle for a day, then "
           "fill it and let it stand a week before anything goes in."),
          bias=1),
    entry("prune-roses",
          (("roses", "rose", "rose bushes", "rose bush", "climbing rose"),
           GONE_WILD + ("prune", "pruning", "cut back", "cutting back", "deadhead",
                        "deadheading", "when", "winter", "spring", "shape", "leggy")),
          ("Prune roses in late winter, around February when the buds start to swell: cut out dead, "
           "thin and crossing stems first, then take the rest back by about a third, making each cut "
           "just above an outward-facing bud so the new shoot grows away from the middle. Deadhead "
           "through the summer down to the first strong leaf. Climbing roses are the exception - "
           "prune those after flowering, not in winter."),
          avoid=("vase", "vases", "bouquet", "bunch", "last longer", "cut flowers")),
    entry("foxes",
          (("fox", "foxes"), ("garden", "stop", "keep out", "keep them out", "deter", "coming",
                             "digging", "fence", "smell", "poo", "scared", "chickens",
                             "bin", "bins", "wheelie", "wheelie bin", "rubbish", "waste",
                             "food waste", "bin bag", "bin bags", "bags", "knocking over")),
          ("Take away the food and the easy way in: bins with clipped lids, no pet food or bird food "
           "left out overnight, and no fallen fruit under the tree. A 2m fence is not enough on its "
           "own, because a fox can clear it or dig under it, so fit a roller bar on top or a strip of "
           "paving on the ground line. Chilli powder and commercial repellents fade in the rain and "
           "have to be renewed; a dog is the only deterrent that works every night."),
          bias=1,
          avoid=("my dog", "the dog", "dogs", "puppy", "rolls in", "roll in", "rolling in",
                 "rolled in", "rolls on", "rolls over it", "rubs himself in", "rubs herself in",
                 "dead bird", "dead things", "licks", "licking", "ate", "eaten")),
    entry("garden-privacy",
          (("private", "privacy", "overlooked", "overlooking", "looked into", "looking in",
            "looks in", "nosey neighbour", "nosy neighbour", "neighbours can see", "screened",
            "screen", "screening", "block the view", "block out the view", "hide", "hiding",
            "cover up", "not see"),
           ("garden", "fence", "hedge", "tree", "trees", "plant", "grow", "window", "windows",
            "neighbours", "neighbor", "neighbors", "boundary", "patio", "decking", "balcony",
            "bin", "bins", "wheelie bin", "wheelie bins", "store", "shed", "oil tank", "heat pump")),
          ("Evergreen blocks a view all year, and yew, holly or laurel reach 2m in a few years: buy "
           "them bare-root in autumn, plant 60cm apart, and put a strip of membrane down so you are "
           "not weeding under them. Quicker than a hedge is a fence or a trellis to 2m at the back "
           "of a garden (1m is the usual limit at the front, and a listed building or a conservation "
           "area wants permission) with a climber over it - ivy, honeysuckle, a climbing rose. "
           "Pleached trees on stilts screen an upstairs window in one season, and a sail shade on "
           "posts does a patio straight away. Check whose fence it is before you build on it, and "
           "ask before taking a hedge down: a boundary hedge is often shared."),
          avoid=("fell down", "fallen down", "blown down", "broken", "repair", "replace",
                 "prune", "pruning", "cut back", "cutting", "trim", "trimming", "hotel", "room",
                 "booking", "refund", "cost", "price", "how much", "who owns", "my neighbour says")),
    entry("patio-sun",
          (("sun", "sunlight", "sunny", "glare", "too hot", "blazing", "shade"),
           ("patio", "decking", "deck", "garden", "terrace", "balcony", "table", "chairs",
            "outside", "sitting out", "barbecue", "bbq")),
          ("Shade the table, not the whole garden: a cantilever parasol is the one that works, "
           "because its base sits off to the side and the canopy reaches over the table without a "
           "pole in the middle. Second is a sail shade on three posts, set so it faces the afternoon "
           "sun and angled 20 to 30 degrees, with the fixings tight enough that it does not flap; "
           "take it down when it blows hard, because a sail in a gale pulls the posts out. If you "
           "have the room, a tree on the west side is the best of all in five years' time - a "
           "rowan, an amelanchier or a small crab apple, 3m from the fence."),
          bias=2),
    entry("lay-turf",
          (("turf", "turfing"), ("lay", "laying", "new lawn", "when", "how")),
          ("Lay turf in spring or early autumn, when the soil is warm and wet: clear and dig the "
           "ground, level it, tread it and rake it, then put a straight edge down and lay the rolls "
           "brick-fashion, butting them tight. Water the whole lawn as you go and keep it damp for a "
           "fortnight: the turf has no roots in the soil until it knits. Or order it early in the "
           "week and lay it the day it arrives - a roll left in the shade goes yellow in a day or two.")),
    entry("garden-start",
          (("garden", "back garden", "plot"),
           GONE_WILD + ("mess", "messy", "overgrown", "neglected", "jungle",
                        "where do i start", "where to start", "how do i start", "get started",
                        "starting point", "start on", "tidy up", "tidy", "sort out", "clear",
            "start a garden", "start gardening", "starting a garden", "start my garden",
            "starting gardening", "start the garden", "begin a garden")),
          ("Take one bed, not the garden: strim or mow the lot so you can see it, then clear a "
           "single rectangle the size of a rug, dig it over and plant something in it, and cover the "
           "rest with cardboard weighted down with compost or old bricks to kill the weeds while you "
           "work through it. Half an hour a day on one bed beats a lost weekend on all of them."),
          avoid=("allotment",)),
    entry("gardening-start",
          (("vegetable patch", "veg patch", "vegetable garden", "kitchen garden", "veg plot",
            "raised bed", "raised beds", "allotment", "garden", "gardening", "grow",
            "growing", "plant", "plants", "vegetables", "veg", "crops", "seed",
            "seeds"),
           ("get into", "getting into", "into gardening", "beginner", "beginners", "new to",
            "first year", "first time", "first garden", "never gardened", "where do i start",
            "where to start", "start with", "start off", "starting out", "begin", "start",
            "starting", "began", "set up", "setting up",
            "easy", "easiest", "small garden", "small space", "what should i grow",
            "what can i grow", "what to grow", "should i grow", "can i grow",
            "what should i plant", "what can i plant", "what to plant", "what grows")),
          ("Start with what you eat and what costs most in the shop. Salad leaves, radishes, "
           "courgettes, runner beans, potatoes and tomatoes are the forgiving six, plus a herb pot "
           "by the door. Take one bed about a metre by two, not the whole garden. Dig a bag of "
           "compost into it. Sow a small row of each from April, and again in June. Salad leaves "
           "are ready to cut in four weeks, which is what keeps a first year going."),
          avoid=("monstera", "orchid", "orchids", "fern", "ferns", "cactus", "cacti",
                 "succulent", "succulents", "peace lily", "aloe", "basil", "fiddle leaf",
                 "calathea", "jade plant", "rubber plant", "spider plant", "snake plant",
                 "pothos", "zz plant", "houseplant", "houseplants", "house plant",
                 "house plants", "indoor", "windowsill", "overgrown", "mess", "messy",
                 "neglected", "jungle", "beard", "hair", "nails", "taller", "height",
                 "business", "following", "followers", "muscle", "muscles", "weed",
                 "cannabis", "crystal", "crystals", "bacteria", "sourdough", "mould",
                 "mold", "moisture", "lawn", "grass", "hedge", "tree", "trees",
                 "shade", "shady", "shaded", "north facing", "north-facing", "sun", "sunny",
                 "full sun", "flower", "flowers", "colour", "color", "colours", "colors",
                 "bulbs", "hanging basket", "basket", "climber", "climbers", "shrub", "shrubs",
                 "perennial", "perennials", "annual", "annuals", "bedding",
                 "keep alive", "easy to keep", "hard to kill", "look after", "looking after",
                 "patio", "pots", "containers", "window box", "window boxes", "balcony",
                 "hanging basket", "grow bag", "grow bags", "in pots", "in a pot",
                 "in containers", "windowsill", "window sill",
                 "water", "watering", "watered", "how often", "how much water",
                 "january", "february", "march", "april", "may", "june", "july", "august",
                 "september", "october", "november", "december", "this month", "next month",
                 "this week", "next week",
                 "tomato", "tomatoes", "potato", "potatoes", "carrot", "carrots", "onion",
                 "onions", "garlic", "lettuce", "lettuces", "bean", "beans", "pea", "peas",
                 "cabbage", "broccoli", "kale", "spinach", "beetroot", "radish", "radishes",
                 "courgette", "courgettes", "cucumber", "chilli", "chillies", "pumpkin",
                 "squash", "sweetcorn", "leek", "leeks", "parsnip", "parsnips", "rhubarb",
                 "strawberry", "strawberries", "runner bean", "runner beans", "broad bean",
                 "broad beans", "herb", "herbs", "mint", "chives", "rosemary", "thyme",
                 "parsley", "coriander", "dill", "sage", "oregano",
                 "bulb", "bulbs", "tulip", "tulips", "daffodil", "daffodils", "allium",
                 "alliums", "crocus", "snowdrop", "snowdrops")),
    entry("size-of-a-plot",
          (("how big", "how large", "how wide", "how much space", "what size", "size of",
            "how many plants", "how long should the bed be", "how many beds",
            "what size allotment", "how big an allotment", "how big a plot", "what size plot",
            "how big a patch", "size of an allotment", "size of a plot", "size of a patch",
            "how much room do i need", "how much space do i need"),
           ("patch", "plot", "vegetable patch", "veg patch", "veg plot", "veg",
            "allotment", "raised bed", "raised beds", "flower bed", "flower beds",
            "garden", "grow", "growing")),
          ("A patch about three metres by two is the size most first plots are, and it feeds two "
           "people through a summer. Keep the bed no wider than 1.2m, so you can reach the middle "
           "from either side without standing on it, and work back from the plants rather than "
           "from the area: a tomato wants 45cm each way, a courgette a square metre to itself, and "
           "salad leaves 20cm apart. Two of each is plenty in the first year. A raised bed wants "
           "twenty centimetres of soil for salad, herbs and dwarf beans, and thirty for carrots, "
           "onions and tomatoes."),
          bias=1,
          avoid=(
                 "for a child", "for children", "for a kid", "for kids", "on a child", "child's",
                 "childs",
                 "mattress", "mattresses", "divan", "headboard", "duvet", "pillow", "pillows",
                 "sheet", "sheets", "bedroom", "king size", "super king", "double bed",
                 "single bed", "bunk", "cot", "sleep", "in bed", "to bed", "off to bed",
                 "my back", "back hurts", "back ache", "backache", "hip", "hips", "shoulder",
                 "shoulders", "sore", "stiff", "hurts", "hair", "scalp", "bald", "skin", "spot",
                 "spots", "rash", "damp", "mould", "mold", "ceiling", "wall", "walls", "eye",
                 "eyes", "tyre", "tyres", "tire", "tires", "plaster", "plasterboard", "hole",
                 "holes", "jeans", "trousers", "dress", "shirt", "nicotine", "smoke", "smoking",
                 "smoker", "quit", "vape", "gum", "pond", "ponds", "patio", "pots", "pot",
                 "container", "containers", "lawn", "dogs", "dog", "cat", "cats", "pet", "pets",
                 "hamster", "rabbit", "chicken", "chickens",
                 "shoe", "shoes", "bra", "dress size", "hat", "ring size", "clothes",
                 "jeans size", "trousers size", "waistcoat")),
    entry("easy-flowers",
          (("easy flowers", "easy colour", "easy color", "flowers for", "low maintenance",
            "low-maintenance", "flower bed", "flower beds", "border", "borders",
            "bedding plants", "bedding plant",
            "flowers", "flower", "colour", "colors"),
           ("garden", "plant", "planting", "easy", "easiest", "what should i", "what can i",
            "which", "start with", "summer", "winter", "spring", "autumn", "shade", "sun",
            "pots", "cheap", "look after themselves", "come back", "perennial", "low")),
          "Cosmos, lavender, hardy geranium, sedum, verbena and pot marigold flower for months "
           "with nothing but deadheading, and daffodil and allium bulbs do the spring. Buy "
           "perennials rather than bedding: they come back every year, so the border fills itself "
           "instead of being replanted each May. Put the tallest at the back, water them in their "
           "first fortnight and leave them alone after that.",
          avoid=("get her", "get him", "for my wife", "for my mum", "for my mom", "for my",
                 "girlfriend", "boyfriend", "husband", "wife", "anniversary", "birthday",
                 "wedding", "funeral", "sorry", "thank you", "valentine", "valentines",
                 "mothers day", "mother's day", "bouquet", "florist", "bunch", "gift",
                 "present", "rose", "roses", "tulip", "tulips", "daffodil", "sunflower",
                 "orchid", "houseplant", "houseplants", "indoor", "keep alive", "easy to keep",
                 "hard to kill", "cut flowers", "vase",
                 "winter", "christmas", "december", "january", "february",
                 "raised bed", "raised beds", "veg", "vegetable", "vegetables", "crops",
                 "crop", "edible", "edibles", "salad", "allotment", "kitchen garden",
                 "paint", "painting", "painted", "repaint", "repainting", "emulsion",
                 "paint colour", "paint colors", "wall colour", "decorating", "decorate"),
          guard=_has_something_to_grow_in),
    entry("slug-control", (("slugs", "snails"),
                             ("keep", "stop", "rid", "control", "eating", "lettuce", "lettuces",
                              "seedling", "what should i do", "what can i do", "what do i do",
                              "do about", "how do i", "deal with", "get rid", "problem",
                              "problems", "everywhere", "kill", "deter",
                              "garden", "plant", "plants", "getting", "holes", "deterrent")),
          ("Go out after dark with a torch and pick them off, which beats most products; copper tape "
           "round pots and a gritty barrier round seedlings help too. Encourage birds and frogs, and "
           "water in the morning rather than the evening.")),
    entry("pests-aphids", (("blackfly", "black fly", "greenfly", "green fly", "aphid", "aphids",
                            "whitefly", "white fly", "whiteflies", "blackflies", "greenflies",
                            "lice", "plant lice", "scale insect", "scale insects"),
                           ("rid", "get rid", "stop", "kill", "control", "spray", "soap", "wash",
                            "covered", "covered in", "infestation", "eating", "sucking", "roses",
                            "beans", "broad beans", "greenhouse", "plants", "plant", "help",
                            "problem", "deal")),
          ("Rub them off with your fingers or a strong jet of water, then spray with soapy water - "
           "a teaspoon of washing-up liquid in a litre, sprayed under the leaves in the evening - "
           "and repeat every three days for a fortnight, because the eggs keep hatching. Check "
           "for ants running up the stem: they farm the aphids and keep them there, so a sticky "
           "band round the pot stops the supply line. Ladybirds and hoverflies do the rest if you "
           "leave the flowers they feed on. On broad beans, pinch out the top 10cm once the "
           "flowers set, which is where blackfly gather.")),
    entry("pests-caterpillars", (("caterpillar", "caterpillars", "cabbage white", "cabbage whites",
                                  "brassica", "cabbage", "cabbages", "holes in the leaves",
                                  "holey leaves", "nibbled", "eaten leaves"),
                                 ("rid", "get rid", "stop", "kill", "control", "eating", "eaten",
                                  "holes", "chewed", "net", "cover", "spray", "picking", "plants",
                                  "help", "deal", "problem")),
          ("Net the crop and the butterflies cannot land: a fine mesh hooped over the rows from "
           "the day you plant, weighed down at the edges, is the whole answer for cabbages and "
           "brassicas. Without a net, look under the leaves for the yellow eggs in clusters and "
           "squash them, and pick off caterpillars in the cool of the morning, when they sit on "
           "the leaf instead of dropping. A plant that has lost every leaf to the lace pattern "
           "will usually grow back if you net it now.")),
    entry("tap-water-cloudy", (("tap water", "cold tap", "hot water", "water", "tap",
                                "from the tap", "out of the tap"),
                               ("cloudy", "milky", "white", "bubbles", "bubbly", "clouded")),
          ("Milky tap water is almost always air: fill a glass, and if it clears from the bottom up "
           "in a minute or two it is just bubbles from pressure in the main and it is safe to "
           "drink. If it stays cloudy, or runs brown, blue or green, run the cold tap for two "
           "minutes and then ring your water company - and drink bottled water until it clears."),
          avoid=("marks", "stains", "scale", "limescale", "furred", "chalky", "crusty", "crust",
                 "on the tap", "on my taps", "on the taps", "taps are", "tap is furred",
                 "around the tap", "shower head",
                 "kettle", "boiler", "bill", "bills", "meter", "pressure", "heating", "radiator",
                 "rain", "sea", "pool", "swimming", "plant", "plants", "garden", "leaking",
                 "pond", "ponds", "fish tank", "tank", "aquarium", "water butt", "green",
                 "laundry", "washing machine", "shirt", "clothes", "toilet",
                 "white stuff", "crust", "crusty", "on my taps", "on the taps", "on the tap",
                 "around the tap", "around the taps", "marks", "stains", "limescale", "scale"),
          bias=1),
    entry("tap-water-safe",
          (("tap water", "the tap", "water from the tap", "drinking water", "filtered water",
            "water tastes", "water smells", "water taste", "water smell"),
           ("safe", "safety", "drink", "drinking", "ok", "alright", "filter", "taste", "tastes",
            "chlorine", "smell", "smells", "hard")),
          ("Tap water in the UK is safe to drink - it is tested all the way to your kitchen - "
           "and the taste it sometimes has is chlorine, which is there to keep it safe: fill a "
           "jug, keep it in the fridge for an hour and the taste goes. A filter is for taste "
           "rather than safety, and it needs changing when the pack says. Old houses can still have lead "
           "pipes: run the cold tap for a minute first thing before drinking or making formula, "
           "and never use the hot tap for either. If the water is discoloured or smells of "
           "anything but chlorine, ring your water company - they test it for free - and drink "
           "bottled until they have."),
           avoid=("hard water stain", "hard water stains", "limescale", "scale", "scaled",
                  "white marks", "chalky", "stain", "stains",
                  "mark", "marks", "marks off", "hard water mark", "hard water marks",
                  "tooth", "teeth", "gums", "gum", "enamel", "dentist", "dentists",
                  "twinge", "toothache", "hurts to drink", "hurts when i drink",
                  "forget", "forgets", "forgetting", "keep forgetting", "struggle", "struggles",
                  "struggling", "remind", "reminds", "remember", "habit", "make myself",
                  "dont drink enough", "don't drink enough", "dont like water",
                  "don't like water", "cant drink", "can't drink", "hate water",
                  "never drink", "barely drink", "hardly drink", "rarely drink",
                  "seldom drink", "drink much", "drink any", "water at all", "much water",
                  "any water", "very little water", "hardly any water",
                  "cloudy", "milky", "brown", "leaking", "boiler", "radiator", "bill", "meter",
                  "dog", "dogs", "cat", "cats", "puppy", "puppies", "kitten", "kittens", "pup",
                  "pet", "pets", "vet", "hamster", "rabbit", "horse",
                  "vomit", "vomiting", "vomited", "being sick", "throwing up", "thrown up",
                  "throw up", "diarrhoea", "diarrhea", "stomach bug", "norovirus", "gastro",
                  "keep down", "keep water down", "keep anything down", "cant keep",
                  "cannot keep", "can't keep", "nausea", "nauseous",
                  "with meals", "with food", "with my meal", "with a meal", "during meals",
                  "before a meal", "before meals", "after a meal", "after meals", "while eating",
                  "abroad", "holiday", "holidays", "travelling", "travel",
                  "mexico", "turkey", "egypt", "spain", "greece", "india", "thailand",
                  "morocco", "tunisia", "cyprus", "portugal", "italy", "france", "usa",
                  "america", "bali", "vietnam", "peru", "kenya", "iceland")),
    entry("compost", (("compost", "composting", "compost heap", "compost bin"),
                     ("what is compost", "what is a compost heap", "what is composting",
                      "what is compost made of", "compost mean", "compost stand for",
                      "heap", "bin", "make", "start", "home", "kitchen", "garden",
                      "how", "caddy", "cooked food", "cooked", "meat", "bones",
                      "what can i put",
                      "not rotting", "rotting", "rot", "rotten", "breaking down",
                      "break down", "broken down", "not breaking", "not working",
                      "heating", "heating up", "heat up", "not heating", "cold",
                      "slow", "slowly", "stalled", "stopped", "slime", "slimy",
                      "smell", "smells", "smelly", "smelling", "stinks", "sour",
                      "flies", "dry", "soggy", "wet", "nothing",
                      "freeze", "freezing", "frozen", "frost", "winter")),
          compost_reply,
          lead=("yesno", _the_no_cooked_food),
          avoid=("houseplant", "houseplants", "house plant", "house plants", "potting",
                 "seed", "seedling", "seedlings", "orchid", "orchids", "cactus", "cacti",
                 "peat", "peat free", "peat-free", "multi purpose", "multi-purpose",
                 "best compost", "which compost", "what compost", "for my pots", "in a pot",
                 "raised bed", "border", "hanging basket", "grow bag", "growbag",
                 "mushroom", "comfrey")),
    entry("ants-in-the-kitchen", (("ants", "ant"), ("kitchen", "trail", "baited", "bait", "rid",
                                                      "cupboard", "sugar",
                                                      "stop", "get rid", "getting rid", "rid of",
                                                      "keep them", "keeping", "keep out", "house",
                                                      "home", "flat", "indoors", "everywhere",
                                                      "floor", "worktop", "counter", "sink",
                                                      "prevent", "off")),
          "Wipe the trail away with vinegar and water and put bait down close to it: they carry the "
          "bait back to the nest and that is what kills the colony, so do not spray the line they "
          "are following. Give the bait a week or two: the ants keep coming for the first few days "
          "and then the stream thins out and stops. Keep sugar and crumbs sealed for a fortnight "
          "and they stop coming. One "
          "ant is a scout; a stream means a nest under the floor or behind a skirting board.", report=True),
    entry("hydrangea-brown", ("hydrangea", ("hydrangeas", "brown", "browning", "dying", "wilting",
                                            "wilted", "wilt", "drooping", "droopy", "limp",
                                            "flowers", "water")),
          "Brown flowers on a hydrangea are almost always thirst, or simply old blooms: it has "
          "shallow roots and wants damp soil and shade from the hottest afternoon sun. Water it "
          "deeply twice a week in dry spells, mulch around the base, and cut the spent heads off so "
          "the plant puts its energy into next year's buds rather than seed.",
          avoid=("wont flower", "won't flower", "not flowering", "isnt flowering",
                 "isn't flowering", "no flowers", "no flower", "no blooms", "hasnt flowered",
                 "hasn't flowered", "never flowered", "didnt flower", "didn't flower",
                 "how do i get flowers", "not flowered", "no hydrangea flowers")),
    entry("tomato-blight", (("blight", "tomato blight", "potato blight", "blighted",
                             "black spot", "black spots", "leaf spot", "spots on the leaves"),
                            ("tomato", "tomatoes", "potato", "potatoes", "crop", "crops",
                             "plant", "plants", "leaves", "leaf", "greenhouse", "plot",
                             "rose", "roses", "bush", "shrub", "tree", "apple", "apples")),
          _blight, bias=2,
          avoid=("ready", "when are", "harvest", "lift", "pick them", "recipe", "cook", "eat",
                 "chutney", "sauce", "salad", "soup")),
    entry("plant-mildew",
          (("mildew", "powdery mildew", "white mould", "white mold", "grey mould", "gray mould",
            "white powder", "white dust", "white coating",
            "white patches", "white film", "grey powder", "gray powder"),
           ("plant", "plants", "leaves", "leaf", "courgette", "courgettes", "cucumber",
            "cucumbers", "squash", "pumpkin", "rose", "roses", "tomato", "tomatoes", "dahlia",
            "dahlias", "pea", "peas", "melon", "melons", "vine", "vines", "greenhouse",
            "apple", "apples", "tree", "trees", "shrub", "shrubs", "bush", "fruit")),
          _mildew, bias=2,
          avoid=("dishwasher", "dishwashers", "dish washer", "washing machine", "washer",
                 "dishes", "dish", "plates", "plate", "glasses", "glassware", "mugs", "cup",
                 "cups", "cutlery", "shower", "bath", "bathtub", "tiles", "sink", "smear",
                 "smears", "streaks", "kettle", "bathroom", "toilet", "tumble dryer",
                 "tumble drier")),
    entry("plant-rot",
          (("rot", "rots", "rotting", "rotted", "rotten", "going mouldy", "gone mouldy",
            "mouldy", "moldy", "blossom end", "black at the bottom", "going soft", "turning to mush",
            "grey mould", "brown rot", "damping off"),
           ("plant", "plants", "crop", "crops", "fruit", "fruits",
            "courgette", "courgettes", "cucumber", "cucumbers", "pepper", "peppers",
            "melon", "melons", "aubergine", "aubergines", "dahlia", "dahlias",
            "squash", "pumpkin", "pumpkins", "strawberry",
            "strawberries", "apple", "apples", "pear", "pears", "plum", "plums", "potato",
            "potatoes", "onion", "onions", "garlic", "seedling", "seedlings", "cutting",
            "cuttings", "stem", "stems", "tree", "vine", "vines", "greenhouse", "ground",
            "allotment", "bed", "beds")),
          _rot, bias=2,
          guard=lambda understood: not _a_kitchen_thing(understood),
          avoid=("fridge", "freezer", "cupboard", "store", "stored", "storing", "keep for",
                 "use by", "best before", "bin day", "wheelie", "wood", "fence", "decking",
                 "mould on", "mouldy soil", "mouldy compost", "mouldy pot", "white mould",
                 "white stuff", "furry mould", "fuzzy mould", "plant pot mouldy",
                 "on the soil", "on the compost", "pot of compost", "potting compost",
                 "potting", "houseplant", "house plant",
                 "deck", "shed", "window frame", "joist", "beam", "floorboard", "tooth", "teeth",
                 "tomato", "tomatoes", "tomato plant")),
    entry("plant-pests",
          (("aphids", "aphid", "greenfly", "green fly", "blackfly", "black fly", "whitefly",
            "white fly", "caterpillars", "caterpillar", "cabbage white", "cabbage whites",
            "vine weevil", "vine weevils", "scale insect", "scale insects", "mealybug",
            "mealybugs"),
           ("rose", "roses", "plant", "plants", "leaves", "leaf", "cabbage", "lettuce",
            "courgette", "courgettes", "tomato", "tomatoes", "bean", "beans", "broad beans",
            "brassica", "brassicas", "flowers", "greenhouse", "crop", "crops", "shoots",
            "get rid of", "rid of", "kill", "killing", "control", "spray", "deal with",
            "covered in", "on them", "on it",
            "on my", "on the", "in my", "under the", "all over", "everywhere", "infested")),
          _pests, bias=2),
    entry("plant-leaves-yellow",
          (("leaves", "leaf", "plant", "plants", "shrub", "foliage",
            "fern", "orchid", "mint", "cactus", "succulent", "spider plant", "money plant"),
           ("yellow", "yellowing", "yellowish", "brown", "browning", "turning brown", "going brown",
            "brown tips", "crispy", "dying", "drooping", "wilting",
            "limp", "floppy", "sagging",
            "sick", "poorly", "struggling", "unwell", "not looking well",
            "look sad", "looks sad", "looking sad", "look unhappy", "looks unhappy",
            "looking unhappy", "not happy", "miserable", "sorry for itself", "sulking",
            "sulky", "struggling",
            "sad")),
          ("Nine times in ten it is the roots, not the light: check the compost an inch down and the "
           "drainage holes, because yellowing leaves are usually too much water or a pot with nowhere "
           "for it to go. Let it dry out, tip the standing water away, and give it a brighter spot "
           "away from a radiator; feed it only once it is growing again. Is it in a pot indoors, or out "
           "in the garden?"),
          ask=("leaves", "leaf", "plant", "plants", "shrub", "brown", "yellow", "turning",
               "drooping", "wilting"),
          avoid=("houseplant", "houseplants", "house plant", "house plants", "indoor plant",
                 "indoor plants", "pot plant", "pot plants",
                 "tips", "tip", "brown edges", "crispy edges",
                 "mint", "parsley", "coriander", "cilantro", "chives",
                 "tomato", "tomatoes", "basil", "hydrangea", "lavender", "roses", "rose",
                 "lawn", "grass", "turf", "nettle", "garlic", "peace lily",
                 "tree", "trees", "apple tree", "oak", "maple", "birch", "willow", "hedge",
                 "i feel", "i am sad", "im sad", "i'm sad", "i am upset", "im upset", "i'm upset",
                 "i feel low", "i feel down", "feeling sad", "feeling low", "feeling down",
                 "made me sad", "makes me sad", "made me feel", "feel miserable",
                 "feel unhappy", "i am miserable", "i'm miserable", "feel like crying"),
          guard=_the_person_is_sad_too),
    entry("prune-lavender", ("lavender", ("prune", "pruning", "cut", "trim", "back", "woody",
                                          "leggy", "look after", "looking after", "care",
                                          "care for", "take care of", "need", "needs", "grow",
                                          "growing", "plant", "planted", "deadhead",
                                          "deadheading", "when do i", "how do i",
                                          "keep it", "keep them", "sun", "soil", "drainage")),
          "Trim it in late August, straight after flowering: take the flower stalks off plus about "
          "2.5cm of this year's leafy growth, and never cut into the bare brown wood, because it "
          "does not grow back. That keeps it dense and stops it going leggy, and leaving a little "
          "new growth on in autumn gives the plant something to shelter behind in winter. The other "
          "half of looking after it is the ground: full sun and sharp drainage, a gravelly or raised "
          "bed, because lavender rots in wet heavy soil in winter and that is the one thing that "
          "kills it. Water it for its first summer only - after that the rain is enough.",
          avoid=("cuttings", "propagate", "propagating", "from seed", "sow", "sowing",
                 "in a pot", "in pots", "in a container", "in containers", "transplant",
                 "root", "roots", "rooting",
                 "move", "moving", "moved", "relocate", "relocating", "dig up", "digging up",
                 "replant", "replanting", "split", "divide", "dividing",
                 "oil", "oils", "bag", "bags", "sachet", "sachets", "dry", "drying", "dried",
                 "harvest", "harvesting", "cooking", "baking", "recipe", "recipes",
                 "candle", "candles", "soap", "wreath", "bunch")),
    entry("potatoes-in-a-bag",
          (("potato", "potatoes", "spud", "spuds", "seed potatoes", "seed potato"),
           ("bag", "bags", "sack", "sacks", "grow bag", "grow bags", "growbag", "bucket",
            "tub", "container", "containers", "pot", "pots", "earthing up", "earth up",
            "earthing", "earth them up", "ridge", "ridges", "haulm", "trench", "trenches",
            "how many in a bag", "how many seed potatoes", "how deep in a bag",
            "how deep in a pot", "how deep to plant them",
            "in a bag", "in bags", "in a sack", "in a grow bag", "in a bucket", "in a tub",
            "in a pot", "in pots", "in a container", "in containers")),
          ("Chit the seed potatoes somewhere light and cool, in an egg box, until the sprouts are "
           "2-3cm long, then plant them from late March. A 40-litre bag or a 30cm pot takes three "
           "seed potatoes: 10-15cm of compost in the bottom, sit them on it, cover them with "
           "another 10cm and water. When the shoots are 15cm above the compost, earth them up - "
           "cover all but the top few centimetres with more compost - and keep doing that until "
           "the bag is nearly full, because tubers that form near the surface turn green in the "
           "light."),
          ask=("how", "how many", "how deep", "when", "best", "can i", "do i", "should i"),
          bias=2,
          avoid=("sweet potato", "sweet potatoes", "couch", "crisps", "chips", "mash", "recipe",
                 "cook", "cooking", "roast", "bake", "salad", "eat", "eat them", "green bin",
                 *DISH_ASK,
                 "peel", "store", "keeping", "chitting", "blight", "disease", "pest",
                 "harvest", "harvesting", "lift", "lifting", "dig up", "digging up", "ready",
                 "when are they ready")),

        entry("deadhead-flowers",
          (("dahlia", "dahlias", "sweet pea", "sweet peas", "cosmos", "geranium", "geraniums",
            "pelargonium", "pelargoniums", "petunia", "petunias", "rose", "roses", "begonia",
            "begonias", "calendula", "marigold", "marigolds", "nasturtium", "nasturtiums",
            "lupin", "lupins", "foxglove", "foxgloves", "penstemon", "delphinium", "salvia",
            "pansy", "pansies", "viola", "zinnia", "zinnias", "sunflower", "sunflowers",
            "flower", "flowers", "flowering", "blooms", "basket", "hanging basket"),
           ("deadhead", "deadheading", "dead heads", "spent flowers", "spent blooms",
            "spent flower heads", "old flowers", "faded flowers", "faded blooms",
            "pinch out", "pinching out", "more flowers", "flowering for longer",
            "stop flowering", "stopped flowering", "keep deadheading"),
           ("keep", "keeping", "longer", "more", "still", "wont", "won't", "stopped", "stop")),
          "Pick or snip the spent flower off with its stalk, down to the next bud or strong shoot, "
          "and do it every few days through the summer. That is the whole trick: once a plant is "
          "allowed to set seed it stops making flower, so cutting the dead heads off is what keeps "
          "it going until the frost. Dahlias, cosmos, sweet peas, geraniums and petunias all want "
          "it twice a week in a hot spell, and sweet peas must not be left to make pods, because a "
          "pod turns the plant woody and it stops. Annuals that are nearly over can be cut back "
          "hard, to 15cm, and they come again.",
          avoid=("sugar", "diet", "calories", "dessert", "carbs", "cut out", "cutting out",
                 "vase", "bouquet", "bunch", "cut flowers", "fresh", "last longer", "in water",
                 "dried out", "drying out", "dries out", "dry out", "dried up", "gone dry",
                 "has dried", "keeps drying",
                 "got flowers", "bought flowers", "gave me flowers", "flowers for my",
                 "them going", "them alive", "kept them", "keep them going",
                 "winter", "over winter", "in winter", "frost", "frosts", "cold",
                 "weed", "weeds", "grass", "lawn", "hedge", "tree", "trees",
                 "rose", "roses", "rose bush", "rose bushes",
                 "no flowers", "no flower", "no blooms", "no blossom", "not flowering",
                 "not flowered", "never flowered", "wont flower", "won't flower",
                 "hasnt flowered", "hasn't flowered", "didnt flower", "didn't flower", "blind"),
          ),
    entry("wasp-nest", ("wasp", ("wasps", "nest", "loft", "attic", "remove", "allergic", "shed")),
          "If it is somewhere nobody goes, leave it: a wasp nest dies in autumn and is never reused. "
          "If it is by a door or someone in the house is allergic, pay a local pest controller, "
          "usually 50 to 80 pounds, rather than going up a ladder with a spray - and do not block "
          "the entrance, because they will find another way into the house.",
          bias=1, report=True),
    entry("wasp-near-you", (("wasp", "wasps", "bee", "bees", "wasp sting", "bee sting",
                             "sting", "stings", "stung", "was stung", "been stung", "got stung",
                             "stung me"),
                            ("stinging", "stung", "sting", "stop", "away", "near", "near me",
                             "landing", "chasing", "buzzing", "bothering", "coming at",
                             "won't leave", "wont leave", "keep coming", "swat", "swatting",
                             "around me", "stood on", "stepped on", "trod on", "hurts",
                             "hurting", "sore", "first aid",
                             "keeps landing", "landing on me", "landing on my", "on me",
                             "hand", "hands", "foot", "feet", "leg", "legs", "arm", "arms",
                             "finger", "fingers", "thumb", "wrist", "ankle", "toe", "toes",
                             "palm", "cheek", "chin", "face", "neck", "shoulder", "ear", "ears",
                             "lip", "lips", "eye", "eyelid", "eyebrow", "head", "skin")),
          _wasp_near,
          bias=2,
          avoid=("nest", "nests", "loft", "attic", "shed", "colony", "swarm", "trap", "traps",
                 "allergic to", "allergy", "anaphylaxis", "epipen", "epi pen", "pest control",
                 "pest controller", "exterminator", "remove", "removing", "get rid",
                 "room", "rooms", "living room", "bedroom", "bathroom", "kitchen", "office",
                 "car", "van", "train", "bus", "indoors", "inside", "in the house",
                 "got in", "got into", "flew in",
                 "treat", "treating", "treatment", "after a sting", "swelling", "swollen",
                 "nettle", "nettles", "jellyfish", "scorpion", "ant", "ants", "mosquito",
                 "mosquitos", "mosquitoes", "horsefly", "tick", "ticks", "wasp beetle")),
    entry("plant-garlic", ("garlic", ("plant", "planting", "grow", "growing", "cloves", "when")),
          "Plant garlic cloves in autumn, October to early December: pointy end up, 15cm apart and "
          "about 2.5cm deep, in a sunny spot with soil that drains. It needs cold to split into a "
          "bulb, which is why autumn beats spring. Water it while it grows and stop a fortnight "
          "before you lift it, when the leaves start to yellow, in July.",
          avoid=("ate", "eat", "eats", "eaten", "eating", "swallowed", "licked", "dog", "dogs",
                 "cat", "cats", "puppy", "kitten", "pet", "pets", "poisonous", "toxic")),
     entry("cut-flowers",
          (("cut flowers", "flowers", "flower", "bouquet", "vase", "stems", "tulips", "daffodils",
            "roses"),
           ("last", "longer", "fresh", "keep fresh", "keep them", "keep it", "keep a",
            "keep my", "keep the", "keep alive", "alive", "looking good", "look good",
            "store", "storing", "stored", "change",
            "changing", "water", "droop",
            "drooping", "droopy", "dying", "wilt", "wilting", "vase", "days", "tips")),
          "Trim about 2cm off each stem at an angle with a sharp knife, strip any leaf that would "
          "sit in the water, and change the water every couple of days: the angle gives the stem a "
          "wide surface to drink through and the slime on old stems is what blocks it. Keep the "
          "vase out of direct sun and away from fruit, since ripening fruit gives off ethylene that "
          "ages flowers. Tulips and daffodils drink a lot, so top those up daily; daffodils go in "
          "their own vase because their sap shortens the life of other flowers.",
          avoid=("garden", "border", "grow", "growing", "planted", "bush", "shrub", "tree",
                 "lawn", "hydrangea", "basil", "tomato", "tomatoes", "lavender", "bulbs",
                 "water my", "water the", "feed", "feeding", "fertiliser", "fertilizer", "mulch",
                 "prune", "pruning", "deadhead", "deadheading",
                 "bloom", "blooms", "blooming",
                 "put sugar", "put bleach", "put aspirin", "add sugar", "add bleach",
                 "sugar in the vase", "bleach in the vase", "sugar in the water",
                 "bleach in the water", "in the vase water", "flower food", "flowerfood",
                 "conditioner")),
    entry("cut-flowers-vase-life",
          (("cut flowers", "flowers in a vase", "vase", "bouquet", "cut stems", "flowers in water"),
           ("how long", "how many days", "vase life", "last a week", "last two weeks",
            "last a fortnight")),
          "About a week is a fair bet for a mixed bouquet: tulips and roses give you around seven "
          "days, daffodils and sweet peas five, carnations and lilies ten to fourteen, and a "
          "bouquet of gypsophila or dried stems longer than that. The stems seal over within a "
          "day or two, so an angled cut and clean water every couple of days is what buys the "
          "extra days.",
          bias=1,
          avoid=("garden", "border", "grow", "growing", "planted", "bush", "shrub", "tree",
                 "lawn", "hydrangea", "basil", "tomato", "tomatoes", "lavender", "bulbs",
                 "heal", "wound", "bleeding", "stitches", "paper cut", "my finger", "my hand",
                 "bloom", "blooms", "blooming", "in the ground", "in the border", "water my",
                 "water the", "feed", "fertiliser", "fertilizer")),
    entry("flowers-cost",
          (("flowers", "flower", "bouquet", "bouquets", "buttonholes", "buttonhole", "stems",
            "florist", "florists"),
           ("spend", "spending", "much", "cost", "costs", "price", "prices", "budget", "afford",
            "cheaper", "cheap", "save", "worth", "wedding", "weddings")),
          "A florist bouquet is £25 to £45, a supermarket bunch £4 to £8, and dried or artificial "
          "stems sit in between and last years. For a wedding, flowers are usually 8 to 10 per cent "
          "of the budget: put the money into the bouquet and the buttonholes, which are in every "
          "photo, and use supermarket or dried stems for the tables and the aisle. For a funeral, a "
          "wreath or a casket spray is £30 to £100 and a tied sheaf £20 to £40. Buying the same "
          "flower in season, from a market rather than a florist, and arranging it yourself the day "
          "before is where the saving usually is.",
          ask=("spend", "much", "cost", "costs", "price", "budget", "afford", "cheaper", "worth",
               "wedding"),
          avoid=("last", "lasts", "longer", "fresh", "droop", "drooping", "wilt", "wilting",
                 "vase", "water", "garden", "grow", "growing", "plant", "planted", "bulbs",
                 "prune", "deadhead", "sow", "seed", "seeds", "corsage", "hair", "wrist",
                 "sun", "sunlight", "sunny", "shade", "light", "soil", "compost", "planting"),
          bias=2),

    entry("plant-brown-tips",
          (("brown tips", "brown tip", "tips going brown", "brown edges", "crispy edges",
            "crisp edges", "brown leaf tips", "tips are brown"),
           ("tips", "brown"),
           ("leaf", "leaves", "plant", "plant's", "houseplant", "houseplants", "foliage",
            "peace lily", "spider plant", "snake plant", "pothos", "monstera", "orchid", "fern",
            "dracaena", "yucca", "palm", "calathea", "zz plant")),
          "Brown tips are usually dry air, hard tap water or a plant that dried right out once: "
          "the leaf edges die first because they are furthest from the roots. Snip the brown off "
          "with scissors so it stops spreading, water it when the top of the compost is dry rather "
          "than in sips, move it off a radiator or a draughty windowsill, and use rainwater or "
          "left-out tap water if your water is hard.",
          avoid=("rose", "roses", "tomato", "tomatoes", "basil", "hydrangea", "lavender",
                 "lawn", "grass", "autumn", "winter", "tree", "trees")),
    entry("cactus-care",
          (("cactus", "cacti", "succulent", "succulents", "christmas cactus", "christmas cacti"),
           ("keep", "alive", "water", "watering", "care", "care for", "dying", "shrivel",
            "shriveled", "wrinkled", "wrinkly", "yellow", "droop", "limp", "leaves", "rot",
            "look after", "thriving")),
          "Cacti and succulents want a sunny windowsill, gritty compost and far less water than "
          "they get: soak the pot, let it dry right through, and that is every two to three weeks "
          "in summer and barely at all from November to March. A Christmas cactus is the "
          "exception - it is a forest cactus - so give it bright light out of full sun, water when "
          "the top half of the pot is dry, and cool nights in autumn, which is what sets the buds.",
          bias=2),
    entry("nettle-sting",
          (("nettle", "nettles", "stinging nettle", "stinging nettles"),
           ("sting", "stung", "put on", "relieve", "itch", "itchy", "rash", "hurts",
            "better")),
          "Cool it under running water or with an ice pack for ten minutes and put an "
          "antihistamine cream on it: a nettle sting is histamine plus tiny hairs, which is why a "
          "dock leaf does nothing except cool the skin as you rub it. It settles in a few hours. "
          "Get help if the swelling spreads well beyond the sting, or if they feel wheezy, sick "
          "or faint."),
    entry("dock-leaf",
          (("dock leaf", "dock leaves", "dockleaf", "dockleaves"),
           ("work", "works", "actually", "help", "helps", "do anything", "good", "true",
            "really", "sting", "stung", "nettle", "nettles", "why", "how")),
          "Not really: a dock leaf only helps because rubbing a cool, damp leaf on a sting cools "
          "the skin and takes your mind off it. Nettle stings are histamine plus tiny hairs, so "
          "run the sting under cool water for ten minutes and put an antihistamine cream on it; "
          "it settles in a few hours."),
    entry("tomato-end-rot",
          (("tomato", "tomatoes", "tomato plant", "tomato plants"),
           ("black", "bottom", "patch", "patches", "rot", "blossom end", "end", "squashy",
            "sunken")),
          "Those black sunken patches on the bottom are blossom end rot, and it is not a disease: "
          "the fruit cannot pull up enough calcium when watering swings from bone dry to soaked, "
          "so a dry spell then a flood sets it off. Water little and often at the base, mulch to "
          "hold the moisture, use a tomato feed, and take the marked fruit off because it will not "
          "recover.",
          guard=lambda understood: not _a_leaf_problem_not_the_fruit(understood)),
    entry("tomato-ripening",
          (("tomato", "tomatoes", "toms", "tomato plant", "tomato plants"),
           ("not ripening", "not turning red", "not turning", "wont ripen", "will not ripen",
            "still green", "stay green", "turning red", "ripening", "ripen",
            "still fruit", "will it fruit", "will they fruit", "fruit this year", "fruiting",
            "set fruit", "setting fruit", "still crop", "will it crop", "will they crop",
            "crop this year", "still produce", "get fruit")),
          "They ripen on warmth and the ethylene they give off themselves, so the two things that "
          "speed them up are heat and a crowd: keep them on the plant while the nights stay above "
          "about 10C, and once the weather turns pick the whole truss and bring it indoors. A ripe "
          "apple or a banana skin in the paper bag does the same job as a sunny windowsill. Green "
          "tomatoes on a plant that is dying back will not come good on it - ripen them off the "
          "plant, or cook them.",
          avoid=("chutney", "fry", "fried", "salsa", "salad", "pickle", "recipe", "cook",
                 "cooking", "roast", "split", "splits", "splitting", "crack", "cracks",
                 "cracked", "cracking")),
    entry("soft-fruit-rot",
          (("strawberry", "strawberries", "raspberry", "raspberries", "blackberry",
            "blackberries", "blueberry", "blueberries", "gooseberry", "gooseberries", "grapes",
            "currants"),
           ("rotting", "rot", "rotten", "mouldy", "moldy", "grey mould", "mushy", "going soft",
            "rots", "mould", "furry", "grey fuzz")),
          "That is grey mould, botrytis: it starts on a bruised or split berry and spreads by "
          "touch and by wet leaves, so pick and bin every affected fruit rather than leaving it "
          "on the plant. Water at the base in the morning rather than over the leaves, open the "
          "plant up so air gets through, and put straw or a mat under the fruit so it is not "
          "sitting on wet soil. It spreads in the fridge too, so do not store a mouldy punnet "
          "with sound ones.",
          avoid=("fridge", "freezer", "punnet", "carton", "shop", "supermarket", "keep",
                 "keeping", "recipe", "cook", "cooking", "roast", "bake", "jam", "smoothie")),
    entry("courgette-end-rot",
          (("courgette", "courgettes", "zucchini", "squash", "pumpkin", "marrow", "marrows"),
           ("rotting", "rot", "rotten", "soft end", "yellow end", "brown end", "tip", "tips",
            "end", "ends", "mushy", "going soft", "shrivelled")),
          "A courgette or squash that rots at the flower end is the same problem as blossom end "
          "rot in tomatoes: the fruit cannot pull up enough calcium when watering swings from "
          "bone dry to soaked, so the tip goes soft and brown. Water little and often at the base, "
          "mulch to hold the moisture, and take the affected fruit off because it will not "
          "recover - the plant then puts its energy into the next ones. A high-nitrogen feed "
          "makes it worse, so use a tomato feed instead.",
          avoid=("fridge", "freezer", "recipe", "cook", "cooking", "roast", "bake", "fry",
                 "pasta", "soup", "bread", "cake", "salad")),
    entry("tomato-yellow",
          (("tomato", "tomatoes", "tomato plant", "tomato plants"),
           ("yellow", "yellowing", "pale", "leaves", "leaf", "lime"),
           ("green veins", "between the veins", "between green veins", "veins")),
          "Yellow leaves on a tomato are usually a feeding or watering problem rather than a "
          "disease. If the yellow sits between green veins, that is magnesium: water evenly, "
          "mulch, and give a tomato feed with magnesium in it. If the lowest leaves go pale and "
          "drop off, the plant is short of nitrogen or the roots are waterlogged. Pick the yellow "
          "leaves off, feed weekly, and water little and often rather than in floods; brown "
          "blotches or black bottoms are a different problem.",
          avoid=("black bottom", "black bottoms", "black at the bottom", "bottom is black",
                 "bottoms are black", "blossom end", "sunken patch", "sunken patches",
                 "rot at the bottom", "rot", "brown tips", "brown tip", "fruit", "fruits",
                 "curl", "curls", "curled", "curling", "rolled", "rolling", "rolling up")),
    entry("pot-herb-yellow",
          (("mint", "parsley", "coriander", "cilantro", "chives", "supermarket herbs", "herb",
            "herbs", "basil", "rosemary", "thyme", "oregano", "dill", "sage"),
           ("yellow", "yellowing", "pale", "dying", "wilted", "wilting", "drooping", "keep",
            "alive", "last", "leaves", "leaf")),
          "A supermarket herb pot is a dozen seedlings crammed into one small pot, so it runs out "
          "of root room and food and starts going yellow within a fortnight. Split it into two or "
          "three pots with fresh compost now, keep it in good light, and water when the top dries "
          "out; leaving it crowded is what kills it, not your watering.",
          avoid=("eating my", "eating the", "ate my", "eaten", "eats", "holes", "holes in",
                 "nibbled", "pest", "pests", "infestation", "greenfly", "blackfly", "aphid",
                 "aphids", "caterpillar", "caterpillars", "slug", "slugs", "snail", "snails",
                 "mould", "mold", "disease", "fungus", "mildew")),
    entry("windowsill-herbs",
          (("herbs", "herb", "basil", "mint", "parsley", "chives", "coriander", "rosemary",
            "thyme", "oregano"),
           ("windowsill", "window sill", "kitchen window", "kitchen", "indoor", "indoors",
            "grow", "growing", "which", "easiest", "best", "dies", "dying")),
          "Basil, mint, chives and parsley are the ones that work indoors: a sunny windowsill, "
          "away from the draught of a window you open, and water when the top of the soil is dry "
          "rather than to a schedule. Mint needs its own pot or it swamps everything next to it. "
          "The supermarket pot dies because it is several seedlings crammed into one small pot, so "
          "either split it into a bigger one or expect two or three weeks and buy small plants "
          "from a garden centre instead.",
          avoid=("outdoor", "garden bed", "border", "lawn", "herbicide", "weedkiller",
                 "drying", "freeze", "frozen", "cooking with")),
    entry("prune-shrub",
    (("shrub", "shrubs", "bush", "bushes", "buddleia", "buddleja", "wisteria", "hydrangea",
      "bay tree", "bay", "laurel", "holly", "raspberry", "raspberries", "blackcurrant",
      "blackcurrants", "gooseberry", "gooseberries", "forsythia", "lilac", "philadelphus",
      "mock orange", "weigela", "spirea", "cotoneaster", "deutzia", "kerria", "viburnum",
      "hebe", "ceanthus", "ceanothus", "photinia", "pieris", "climbing plant", "climber"),
     GONE_WILD + ("prune", "pruning", "pruned", "cut back", "cutting back", "trim",
                  "trimming", "hard", "shape", "leggy", "how far back", "cut down",
                  "cut it back")),
    _prune_shrub,
    avoid=("rose", "roses", "lavender", "hedge", "hedges", "privet", "conifer", "apple",
           "apples", "pear", "pears", "plum", "plums", "cherry", "cherries", "damson", "fig",
           "lawn", "grass", "tomato", "tomatoes", "potato", "potatoes", "cuttings", "cutting",
           "take cuttings", "propagate", "deadhead", "deadheading", "flower", "flowers",
           "flowering", "bloom", "blooms", "blossom", "scent", "smell", "feed", "feeding",
           "fertiliser", "fertilizer", "plant", "planting", "sow", "sowing", "move",
           "transplant", "die", "dying", "died", "brown", "yellow", "drooping", "disease",
           "pick", "picking", "harvest", "harvesting", "ripe", "ripen", "ripening", "berries",
           "crop", "crops", "eat", "jam", "freeze", "freezing", "planting out",
           "black spot", "aphids", "not flowering", "no flowers"),
    bias=1),

    entry("prune-a-hedge",
    (("hedge", "hedges", "hedge trimming", "privet", "box hedge", "conifer",
      "leylandii", "beech hedge", "hornbeam"),
    GONE_WILD + ("prune", "pruning", "cut", "cutting", "trim", "trimming", "back", "when",
                 "shape", "neaten")),
    "Most hedges want one cut in late summer, from August, once the birds have finished "
    "nesting - it is against the law to disturb a nest in use, so check before you start. "
    "Box and privet take a cut in June as well. Trim so the sides slope in slightly at the "
    "top: a flat-sided hedge shades its own base and goes bare at the bottom. Leave the "
    "sides alone if you are cutting a conifer hard, because most will not regrow from old "
    "wood."),
    entry("plants-for-shade",
    (("shade", "shady", "shaded", "north facing", "north-facing", "no sun"),
    ("garden", "border", "bed", "plant", "plants", "grow", "growing", "what can i")),
    "For damp shade: ferns, hostas, astilbe, hydrangea, brunnera and foxgloves all cope and "
    "look after themselves. Dry shade under a tree is the hard one - hardy geranium, "
    "epimedium, vinca, lungwort and ivy are the ones that survive it. Whatever you plant, "
    "dig in leaf mould or compost first: shade plants fail more often from thin dry soil "
    "than from the lack of sun.",
    avoid=("lawn", "grass", "turf", "mow", "mowing", "mown", "seed", "seeds", "reseed",
           "houseplant", "houseplants", "house plant", "house plants", "indoor", "indoors",
           "windowsill", "pot", "pots", "conservatory",
           "vegetable", "vegetables", "veg", "crops", "crop", "salad", "edible", "edibles",
           "kitchen garden", "allotment", "tomato", "tomatoes", "potato", "potatoes", "basil",
           "lettuce", "carrot", "carrots", "beans", "peas", "onion", "onions", "garlic",
           "cabbage", "broccoli", "rhubarb", "courgette", "courgettes", "spinach", "kale"),
    ask=("grow", "growing", "bed", "beds", "border", "borders", "garden", "gardens",
         "soil", "allotment", "what should i plant", "what can i plant", "what to plant",
         "what can i grow",
         "plant shade", "plants shade"),
    bias=4),
    entry("lawn-in-shade",
          (("shade", "shady", "shaded", "shaded corner", "in the shade", "under the trees",
            "under trees", "under a tree", "north facing", "north-facing", "no sun", "dappled"),
           ("lawn", "grass", "turf", "mow", "mowing", "green", "thick", "patchy", "grow",
            "growing", "keep dying", "wont grow")),
          "Grass needs four hours of direct sun a day, so in deep shade it will always be thin: "
          "the fix is to take away the shading before you feed anything. Cut back the branches "
          "over the lawn or raise the canopy, and mow higher in shade - about 6cm rather than 4 - "
          "because longer blades catch what light there is. Feed lightly and water less often but "
          "deeply, since shade keeps the soil damp. If it stays bare, sow a shade mix of fescue "
          "and bent rather than ryegrass, or give that corner over to gravel, ferns or a bench: a "
          "lawn under a tree is a losing fight."),
    entry("veg-in-shade",
          (("shade", "shady", "shaded", "north facing", "north-facing", "no sun", "little sun",
            "half shade", "part shade", "under the trees", "under a tree", "under trees",
            "dappled"),
           ("vegetable", "vegetables", "veg", "crops", "crop", "salad", "edible", "edibles",
            "allotment", "kitchen garden", "greens", "what can i grow", "what should i grow",
            "what can i plant", "what should i plant", "tomato", "tomatoes", "potato",
            "potatoes", "lettuce", "carrot", "carrots", "cabbage", "broccoli", "rhubarb",
            "courgette", "courgettes", "beans", "peas", "garlic", "onion", "onions")),
          _shade_crop_reply,
          avoid=("houseplant", "houseplants", "house plant", "indoor", "indoors", "windowsill",
                 "conservatory", "lawn", "grass", "turf", "mow", "house plants", "pot", "pots"),
          bias=2),
    entry("sowing-seeds",
          (("sow seeds", "sowing seeds", "sow a seed", "seed tray", "seed trays",
            "from seed", "start seeds", "starting seeds", "grow from seed", "sow indoors",
            "sow inside", "sow in trays", "prick out", "pricking out", "pot on"),
           ("how", "when", "best way", "what do i", "indoors", "inside", "tray", "compost",
            "heat", "light", "water", "thin", "thin out", "transplant", "start", "grow",
            "growing", "should i")),
          "Fill a tray or small pot with seed compost, firm it, water it first, and sow on the "
          "surface at the depth on the packet - about twice the seed's own size, and barely at "
          "all for tiny seed. Keep it at 18 to 21C somewhere light, cover it with a clear lid or "
          "a plastic bag until the first shoots show, then take the cover off. Water from below "
          "by standing the tray in a little water rather than pouring on top, and move each "
          "seedling into its own pot once it has two true leaves, holding it by a leaf and not "
          "the stem. Tomatoes, chillies and peppers are started indoors in March and April; hardier "
          "things wait until April, six to eight weeks before they go outside.",
          avoid=("lawn", "grass", "turf", "sesame", "chia", "bird", "birds", "feed the",
                 "seedless", "sunflower seed", "pumpkin seed", "potato", "potatoes", "chit",
                 "chitting", "seed funding", "seed round", "investor", "business"),
          bias=1),
    entry("veg-watering",
    (("water", "watering", "watered", "how often should i water", "how often do i water",
      "how much water", "when should i water", "when do i water"),
     ("tomato", "tomatoes", "courgette", "courgettes", "bean", "beans", "runner bean",
      "runner beans", "potato", "potatoes", "pepper", "peppers", "chilli", "chillies",
      "cucumber", "cucumbers", "lettuce", "salad", "carrot", "carrots", "onion", "onions",
      "strawberry", "strawberries", "raspberry", "raspberries", "veg", "vegetable",
      "vegetables", "allotment", "greenhouse", "raised bed", "plot")),
    "Tomatoes want about two to three litres each, twice a week in dry weather, poured at the "
    "base in the morning so the leaves are dry by night. Anything in a pot needs water every day "
    "in summer, and beans, courgettes, cucumbers and potatoes want a good can each in a dry "
    "spell. Steady watering matters more than the exact amount: up and down watering is what "
    "splits tomatoes and causes blossom end rot. Rain of more than a few millimetres counts, and "
    "a mulch holds the moisture you have given them.",
    avoid=("rinse", "rinsing", "rinsed",
      "wash", "washed", "washing", "water runs clear", "runs clear",
      "houseplant", "houseplants", "house plant", "monstera", "peace lily", "snake plant",
           "cactus", "succulent", "orchid", "fern", "lawn", "grass", "hose", "watering can",
           "irrigation", "sprinkler", "butt", "water butt", "rain barrel", "feed", "fertiliser",
           "fertilizer", "tomato feed", "sow", "sowing", "plant out"),
    bias=2),
    entry("plants-for-sun",
    (("sun", "sunny", "full sun", "sunshine", "south facing", "south-facing", "hot border",
      "baking hot", "baking in the sun", "drought"),
    ("plant", "plants", "grow", "growing", "border", "borders", "bed", "beds", "flowerbed",
     "what can i", "what should i")),
    "For a sunny border: lavender, salvia, verbena, sedum, rudbeckia, cosmos and a grass or two "
    "give colour from June to October and take the heat. Plant in spring or early autumn and "
    "water them well through their first summer, because that is what makes them drought-proof "
    "later; after that, a mulch in spring is most of the work. Med-style plants want sharp "
    "drainage, so add grit to heavy soil rather than compost.",
    avoid=("houseplant", "houseplants", "house plant", "indoor", "window", "windowsill", "lawn",
           "grass seed", "tomato", "tomatoes", "basil", "potato", "potatoes", "veg",
           "vegetable", "vegetables", "greenhouse",
           "baking powder", "baking soda", "bicarbonate", "baking tray", "baking sheet",
           "baking tin", "baking dish", "baking paper", "parchment", "flour", "oven", "cake",
           "cakes", "biscuit", "biscuits", "bread", "scones", "muffins", "icing sugar",
           "banana", "bananas", "mash", "smoothie", "smoothies", "ripe", "overripe",
           "gone black", "gone brown",
           "egg", "eggs", "butter", "sugar", "milk", "yoghurt", "yogurt", "chocolate",
           "cocoa", "yeast", "vanilla", "frosting", "loaf", "dough", "pastry", "batter",
           "instead of", "substitute", "substitutes", "swap", "replace"),
    bias=3),
    entry("cats-in-the-garden",
    (("cat", "cats", "neighbour's cat", "neighbours cat", "next door's cat"),
    ("poo", "pooing", "pooping", "toilet", "mess", "messing", "digging", "dig", "scratching",
    "wee", "weeing", "garden", "beds", "flowerbed", "border")),
    ("They go for bare, dry soil, so take that away: mulch the beds, plant closer together, "
    "and lay short prickle cuttings or a few crossed sticks over newly dug ground. Give them "
    "somewhere better - a patch of gravel or sand out in the open, cleared now and then - "
    "because a cat will keep to one spot if it has it. A motion-triggered water spray "
    "settles the persistent ones, and citrus peel and coffee grounds only work for a few "
    "days."),
    avoid=("litter tray", "litter", "tray", "indoor", "inside the house", "pregnant",
    "cat bed", "dog bed", "cat basket", "dog basket", "her bed", "his bed",
    "toxoplasmosis", "carpet", "curtains", "indoors", "in the house", "in the flat",
    "sofa", "couch", "next to the tray", "outside the tray",
    "mouse", "mice", "rat", "rats", "vole", "voles", "dead mice", "dead bird", "prey",
    "bird", "birds", "pigeon", "pigeons", "brought in", "brings in", "dragged in",
    "on the bed", "in the bed", "on my bed", "on our bed", "on his bed",
    "on her bed", "bedroom", "duvet",
    "wet the bed", "wets the bed", "wetting the bed", "wet on the bed", "peed", "peed on",
    "peeing", "weed on", "wees on", "wetting",
    "under the bed", "under my bed", "under our bed", "under his bed", "under her bed",
    "hides", "hiding", "hiding under", "hides under", "wont come out", "won't come out"),
    ask=("garden", "gardens", "flower bed", "flower beds", "flowerbed", "flowerbeds",
    "border", "borders", "soil", "mulch", "lawn", "allotment", "beds", "bedding",
    "plants", "plant", "vegetable patch", "veg patch", "dug", "shrub", "shrubs")),

    entry("tomato-split",
          (("tomato", "tomatoes", "tomato plant", "tomato plants"),
           ("split", "splits", "splitting", "crack", "cracks", "cracking", "cracked", "burst",
            "bursting", "skin", "skins")),
          "Splitting is water, not disease: after a dry spell the roots take up water faster than "
          "the skin can stretch, so the fruit splits, and a heavy feed does the same. Water little "
          "and often at the base so the soil stays evenly damp, mulch to hold that moisture, and "
          "pick the split ones straight away because they rot where the skin is broken. In a wet "
          "spell pick the fruit a little under-ripe rather than leaving it to swell.",
          avoid=("black", "bottom", "bottoms", "blossom end", "rot", "yellow", "yellowing",
                 "leaves", "leaf", "green veins")),
    entry("root-split",
          (("carrot", "carrots", "beetroot", "beetroots", "beet", "parsnip", "parsnips",
            "radish", "radishes", "turnip", "turnips", "swede", "swedes", "celeriac"),
           ("split", "splits", "splitting", "crack", "cracks", "cracking", "cracked", "burst",
            "bursting", "forked", "forking", "woody", "holes", "tunnels",
            "bolted", "bolting", "gone to seed", "going to seed", "run to seed", "flowering",
            "flowered", "gone up")),
          _root_split,
          avoid=("knuckle", "knuckles", "joint", "joints", "back", "fingers", "bones",
                 "eaten", "eaten by", "holes in the leaves", "carrot fly", "rust fly"),
          ask=("carrot", "carrots", "beetroot", "beet", "parsnip", "parsnips", "radish",
               "radishes", "turnip", "turnips", "swede", "celeriac"),
          bias=2),
    entry("gone-to-seed",
          (("lettuce", "lettuces", "spinach", "rocket", "chard", "coriander", "cilantro",
            "basil", "parsley", "dill", "kale", "pak choi", "bok choy", "mustard greens",
            "leafy", "herbs", "herb"),
           ("bolted", "bolting", "bolt", "gone to seed", "going to seed", "run to seed",
            "running to seed", "ran to seed", "seeding", "flowering", "flowered", "shooting up",
            "gone up", "tall stem")),
          "Once a lettuce, a spinach or a herb sends up a stem it has run to seed, and the leaves "
          "turn bitter as it does: cut it now and eat what is still good, because it will not come "
          "back into leaf. It happens in heat and long days, so next time pick a slow-bolt variety, "
          "sow so the crop is ready before midsummer or after it, keep it watered, and shade it in "
          "a heatwave. Picking the outer leaves often keeps a plant in leaf longer.",
          avoid=("pollinat", "pollen", "stamen", "stigma", "how do flowers", "how does a flower",
                 "when do i sow", "when should i sow", "what month", "sow", "sowing",
                 "slugs", "snails", "caterpillars", "aphids", "eaten", "recipe", "salad",
                 "how do i cook", "what can i make"),
          ask=("lettuce", "lettuces", "spinach", "rocket", "chard", "coriander", "cilantro",
               "basil", "parsley", "dill", "kale", "pak choi", "bok choy", "herb", "herbs",
               "leafy"),
          bias=1),
    entry("fruit-drop",
          (("apple", "apples", "apple tree", "pear", "pears", "pear tree", "plum", "plums",
            "cherry", "cherries", "damson", "damsons", "greengage", "fruit tree", "fruit trees"),
           ("dropping", "dropped", "drops", "falling off", "fall off", "fell off", "coming off",
            "falls off", "dropping its fruit", "losing fruit", "losing its fruit", "june drop",
            "dropping fruit")),
          "Fruit that drops in June and early July is the tree thinning its own crop, and it is "
          "normal: it lets go of more than it can carry, and the apples that stay grow bigger for "
          "it. If it is later than that, or the whole crop goes, look at water and pollination "
          "first - a dry spell in summer, a wet cold week when the bees were out, or a heavy pest "
          "year. Water the tree deeply once a week in dry weather, pick up the fallen fruit so "
          "wasps and rot do not move in, and let it drop what it wants.",
          avoid=("phone", "battery", "dropped my", "dropped it", "damp", "wall", "paint",
                 "repaint", "ceiling", "patch", "mould", "mold", "wifi", "signal",
                 "out of the pram", "out of the cot"),
          ask=("apple", "apples", "pear", "pears", "plum", "plums", "cherry", "cherries",
               "damson", "damsons", "greengage", "fruit tree", "fruit trees", "tree",
               "trees"),
          bias=2),
    entry("what-is-compost",
          (("compost", "compost heap", "compost pile", "home made compost", "homemade compost"),
           ("what is", "whats", "what are", "made of", "made from", "made up of", "how do i make",
            "how do you make", "how is it made", "how to make", "mean", "explain", "difference")),
          "Compost is plant waste that has rotted down into dark crumbly stuff that smells of "
          "earth: layer green things like grass, peelings and weeds with brown things like "
          "cardboard, dead leaves and twiggy prunings, keep it as damp as a wrung-out sponge, "
          "and turn it now and then. Six months to a year and it is ready to spread on beds or "
          "dig in, and it feeds the soil rather than the plant. Bagged potting compost is a "
          "different thing - sterilised, and made light enough for roots in a pot.",
          avoid=("bin", "bins", "caddy", "smell", "smells", "smelly", "flies", "fruit flies",
                 "rat", "rats", "maggot", "maggots", "council", "collection", "food waste",
                 "not broken down", "not heating up", "is it ready", "when is it ready",
                 "best", "which", "buy", "bought", "houseplant", "houseplants", "potting",
                 "seed", "seeds", "seedling", "seedlings", "multipurpose", "peat", "drainage",
                 "for pots", "in a pot", "for cuttings", "for a lawn", "for the lawn"),
          bias=1),
    entry("easy-houseplants",
          (("houseplants", "house plants", "house plant", "houseplant", "indoor plants",
            "indoor plant", "plant", "plants"),
           ("easy", "easiest", "hard to kill", "kill", "beginner", "beginners", "forgiving",
            "neglect", "unkillable", "simple", "recommend", "start", "alive")),
          "Spider plant, snake plant, pothos and the ZZ plant are the ones to start with: they take "
          "low light, a missed watering and a radiator, and still look fine. Water them when the "
          "compost is dry rather than on a schedule, keep them out of the hottest sun, and they will "
          "outlive the ones that want fussing.",
          avoid=("monstera", "orchid", "orchids", "fern", "ferns", "cactus", "cacti",
                 "succulent", "succulents", "peace lily", "aloe", "basil", "fiddle leaf",
                 "calathea", "jade plant", "rubber plant", "spider plant", "snake plant",
                 "pothos", "zz plant", "garden", "gardens", "border", "borders", "allotment",
                 "vegetable", "veg", "flower bed", "beds", "lawn", "outside", "outdoors",
                 "shrub", "shrubs", "tree", "trees",
                 "mosquito", "mosquitoes", "mosquitos", "insect", "insects", "pest", "pests",
                 "bug", "bugs", "repel", "repels", "keep away", "keep mosquitoes",
                 "seed", "seeds", "sow", "sowing", "sowed", "from seed", "sow seeds",
                 "propagate", "propagation", "cutting", "cuttings")),
    entry("plant-dying",
          (("plant", "plants", "houseplant", "houseplants", "house plant", "house plants"),
           ("dying", "died", "drooping", "droopy", "wilted", "wilting", "limp", "sick", "wrong",
            "revive", "save", "alive", "stop", "failing", "looks bad", "not doing well")),
          "Feel the compost first: wet and smelly means too much water, so stop watering, let it "
          "drain and repot in fresh compost if the roots are brown and soft. Bone dry and light "
          "means the opposite, so soak the whole pot in a bowl for ten minutes. If it is neither, "
          "check the light and look under the leaves for tiny insects, and give it a few weeks "
          "before changing anything else: plants sulk slowly and recover slowly.",
          avoid=("frost", "frosts", "frosty", "freezing", "frozen", "cold snap", "cold night",
                 "cold nights", "sub zero",
                 "monstera", "orchid", "orchids", "fern", "ferns", "cactus", "cacti",
                 "succulent", "succulents", "peace lily", "aloe", "basil", "fiddle leaf",
                 "calathea", "jade plant", "rubber plant", "spider plant", "snake plant",
                 "pothos", "zz plant", "tomato", "tomatoes", "lawn", "grass", "hedge",
                 "hydrangea")),


    entry("leaf-drop",
          (("dropping leaves", "dropped leaves", "dropped its leaves", "losing leaves", "losing its leaves",
            "leaves dropping", "leaves falling off", "leaves falling", "leaves dropping off",
            "shedding leaves", "lost its leaves"),
           ("dropping", "falling", "dropped", "shedding"),
           ("plant", "houseplant", "house plant", "indoor", "pot", "monstera", "peace lily",
            "ficus", "rubber plant", "pothos", "succulent", "cactus", "orchid", "palm",
            "dracaena", "calathea", "fern")),
          ("Leaves dropping off a houseplant is usually too much water: compost that has stayed wet "
           "for a week or more, or a saucer left standing full. Feel the compost - wet means no "
           "water for a fortnight, dry means a good soak and a pot that drains. Otherwise it is "
           "reacting to a change, cold from a window or a move to a new spot: leave it where it is "
           "for a month, since moving it about is what keeps it dropping."),
          avoid=("autumn", "tree", "trees", "outside", "garden", "lawn", "tomato", "bee",
                 "bees", "caterpillar", "deer", "sheep", "hedge", "shrub", "allotment",
                 "flower", "flowers", "flowering", "bloom", "blooms", "bud", "buds",
                 "bonsai", "bonsais", "money tree", "juniper", "maples"),
          ask=INDOORS,
        ),

    entry("fungus-gnats",
          (("little black flies", "little flies", "tiny flies", "tiny black flies", "small black flies",
            "black flies", "fungus gnats", "gnats", "flies round my plant", "flies around my plant",
            "flies in my plant", "flies in the compost", "flies round the plant"),
           ("flies", "fly", "gnats", "tiny"),
           ("plant", "plants", "houseplant", "house plant", "pot", "pots", "compost", "soil",
            "potting", "indoor", "room", "windowsill", "kitchen windowsill")),
          ("Those little black flies are fungus gnats, and they are breeding in wet compost rather "
           "than eating the plant. Let the top 2-3cm dry right out between waterings, water from "
           "the bottom for a few weeks, and stand a yellow sticky trap in the pot; a layer of grit "
           "or sand on the surface stops them laying more. They are harmless to people and rarely "
           "kill a plant."),
          avoid=("fruit flies", "fruit fly", "bin", "drain", "kitchen sink", "sink", "wine",
                 "vinegar", "food waste", "caddy", "midge", "midges", "mosquito", "bite",
                 "bites", "sting", "wasps"),
          ask=INDOORS,
        ),

    entry("soil-mould",
          (("white mould", "white mold", "mould on the soil", "mould on the compost",
            "mould on top", "furry mould", "grey mould", "white stuff on the soil",
            "mould in the pot", "going mouldy", "gone mouldy", "mouldy", "moldy",
            "mouldy soil", "mouldy compost", "mouldy pot", "plant pot mouldy",
            "mould in my pot", "mould on the surface", "green mould", "algae", "slimy soil",
            "mould in a plant pot", "mould in a pot", "mould in my plant pot",
            "mould on a plant pot", "mould on my plant pot", "mould in the plant pot",
            "mould in the soil", "mould in the compost", "get rid of mould",
            "get rid of the mould", "mould in my soil"),
           ("mould", "mold", "white", "furry"),
           ("plant", "soil", "compost", "pot", "houseplant", "house plant", "indoor",
            "potting", "seedling", "seedlings")),
          ("White furry mould on the top of the compost is harmless: it is feeding on dead bits in "
           "compost that has stayed wet in still air. Scrape it off, water only when the top of the "
           "compost is dry, empty the saucer, and give the room some air - the plant does not need "
           "repotting."),
          avoid=("bread", "wall", "walls", "bathroom", "shower", "ceiling", "window", "grout",
                 "tile", "tiles", "cheese", "jam", "fridge", "food", "clothes", "washing",
                 "damp", "mushroom", "mushrooms",
                 "damping off", "damping", "collapsed", "collapsing", "collapses",
                 "pinched off", "pinched at", "thin stem", "stem has gone thin",
                 "fell over", "fallen over", "keeled over", "toppled",
                 "curry", "stew", "soup", "sauce", "rice", "pasta", "noodles", "risotto",
                 "casserole", "chilli", "chili", "broth", "gravy", "bolognese", "cooked",
                 "leftovers", "leftover", "takeaway", "slow cooker", "jam", "yoghurt", "yogurt"),
          ask=INDOORS,
        ),

    entry("spider-mites",
          (("spider mites", "spider mite", "fine webs", "tiny webs", "webbing", "little webs",
            "spider webs", "webs on the plant", "webs on my plant", "cobwebs on", "white speckles",
            "speckled leaves", "stippled leaves", "dusty leaves"),
           ("webs", "webbing", "mites", "speckled", "speckles", "stippled", "dusty"),
           ("plant", "leaves", "leaf", "houseplant", "house plant", "indoor", "pot", "underside",
            "under the leaves", "monstera", "palm", "calathea", "ficus", "fern", "schefflera",
            "ivy")),
          ("Fine webbing and leaves that look speckled and dusty mean spider mites, which thrive in "
           "hot, dry air. Take the plant to the sink or shower and wash both sides of every leaf, "
           "raise the humidity around it - group it with other plants, or stand the pot on a tray "
           "of wet pebbles - and wash it again every three or four days for a fortnight, because "
           "the eggs hatch in between. A plant that is badly covered is better thrown out than "
           "fought for."),
          avoid=("house spider", "cellar spider", "garden spider", "false widow", "spider bite",
                 "spiders in the", "big spider", "bathroom", "shed", "bite", "bites"),
          ask=INDOORS,
        ),

    entry("leggy-growth",
          (("gone leggy", "leggy", "tall and thin", "thin and straggly", "straggly", "spindly",
            "stretched out", "all stem"),
           ("leggy", "spindly", "straggly", "thin", "stretched"),
           ("plant", "houseplant", "house plant", "indoor", "leaves", "stems", "pot", "windowsill",
            "geranium", "pelargonium", "basil", "mint", "succulent")),
          ("A plant that has gone tall, thin and stretched is short of light, not ill: it is "
           "reaching for the window. Move it nearer the light and turn it a quarter turn each week "
           "so it grows evenly, then cut the straggly stems back by half - most houseplants send "
           "out two shoots from the cut, and the pieces you cut off will root in a glass of water."),
          ask=INDOORS,
        ),

    entry("orchid-water",
          (("orchid", "orchids", "moth orchid", "phalaenopsis"),
           ("water", "watering", "how often", "ice", "ice cubes", "roots", "bark", "soak",
            "droop", "drooping", "dying", "root rot", "shrivel", "wrinkled")),
          ("Water an orchid by soaking it: once a week, stand the pot in tepid water for ten "
           "minutes, let it drain right through, and put it back - never leave it standing in "
           "water, which rots the roots. They come in bark chips and a clear pot so you can see the "
           "roots: silvery-grey wants water, green is fine. Ignore the ice-cube trick; cold water "
           "on tropical roots does them no good."),
          ask=("water", "watering", "how often", "soak", "ice", "roots", "bark"),
          bias=2,
          avoid=("buy", "gift", "present", "flower shop", "wedding", "corsage")),

    entry("plant-bonsai",
          (("bonsai", "bonsais", "bonsai tree"),
           ("water", "watering", "how often", "care", "care for", "look after", "keep alive",
            "feed", "trim", "prune", "outside", "indoors", "inside", "pot", "soil", "dying",
            "brown", "leaves", "winter", "beginner", "start", "buy")),
          ("Most bonsai are outdoor trees kept small, so keep it outside - a windowsill indoors is "
           "usually too dry and too warm. Water when the top of the soil is starting to dry, which "
           "is most days in summer and every few days in winter: soak it until water runs out of "
           "the holes, then let it drain. Feed every two weeks in the growing season, trim the "
           "shoots back to two leaves, and give it a cool frost-free spot in winter. Only a "
           "tropical one such as ficus stays indoors."),
          avoid=("buy one", "gift", "present", "price", "cost", "to buy")),

    entry("orchid-reflower",
          (("orchid", "orchids", "moth orchid", "phalaenopsis"),
           ("flowers", "flower", "flowering", "reflower", "rebloom", "bloom", "spike", "buds",
            "bud", "dropped", "lost", "die", "died", "not flowering", "again")),
          ("An orchid drops its flowers when that show is over, not because it is dying: cut the "
           "bare spike an inch above the second node, keep it in bright light out of direct sun, "
           "and give it cooler nights - around 16 to 18C - because the drop in temperature is what "
           "sets new buds. It usually takes a couple of months, and the old spike left on often "
           "flowers again from the same stem."),
          bias=1, avoid=("buy", "gift", "present", "flower shop", "wedding")),

    entry("plant-pot-dropped",
          (("plant pot", "plant pots", "pot", "pots", "plant", "plants", "houseplant",
            "houseplants", "house plant", "indoor plant", "indoor plants", "windowsill",
            "compost", "soil", "potted plant", "root ball", "roots", "cutting"),
           ("dropped", "drop", "drops", "dropping", "fell", "fallen", "falls", "knocked",
            "knock", "knocked over", "tipped", "tipped over", "broke", "broken", "cracked",
            "cracks", "smashed", "shattered", "spilled", "spilt", "upside down", "on its side")),
          ("Sooner is better than tidy: lift the plant by its base rather than by the stem, keep as "
           "much of the root ball as will hold together, and shake off only the compost that has "
           "already come loose. Stand it in fresh compost in a pot with drainage holes - the same "
           "size or one up, never a big jump - firm the compost round the roots, water until it "
           "runs out of the bottom, and keep it out of direct sun for a week. White firm roots are "
           "fine and brown mushy ones can be trimmed off. A cracked pot will hold for a while, but "
           "slip it inside another pot or repot it, because a break under the rim gives way all at "
           "once."),
          ask=("pot", "pots", "plant pot", "plant pots", "root ball", "compost", "soil",
               "out of its pot", "out of the pot", "cracked", "crack", "smashed", "shattered",
               "broken", "broke", "on its side", "upside down", "knocked", "knock",
               "dropped it", "dropped my plant", "dropped the plant", "dropped a plant",
               "dropped mine", "off the shelf", "off the windowsill", "off the table",
               "off the sill",
               "tipped", "tipped over", "went over", "gone over", "went flying"),
          bias=2,
          avoid=("soup", "stew", "stock", "casserole", "saucepan", "pan", "rice", "pasta",
                 "boil", "boiled", "boiling", "cook", "cooking", "cooked", "kitchen", "hob",
                 "oven", "slow cooker", "pressure cooker", "chilli", "curry", "tea", "coffee",
                 "paint", "flower", "flowers", "bud", "buds", "bloom", "blooms", "petal",
                 "petals", "leaves", "leaf", "yellow", "yellowing", "drooping", "wilting",
                 "wilt", "brown")),

    entry("plant-dropping-its-flowers",
          (("houseplant", "house plant", "houseplants", "house plants", "peace lily",
            "peace lilies", "african violet", "african violets", "hoya", "cyclamen",
            "christmas cactus", "kalanchoe", "anthurium", "begonia", "fuchsia", "plant",
            "plants", "indoor plant", "indoor plants"),
           ("dropping", "dropped", "drops", "drop", "losing", "lost", "lose", "falling",
            "fallen", "fell", "shedding", "shed", "losing", "bare")),
          ("A houseplant drops its open flowers when that flush is simply over, and nothing needs "
           "doing beyond cutting the spent stems back to a leaf so the plant puts its energy into "
           "leaves and roots instead. Buds that drop before they open are a different thing: that "
           "is the plant shedding what it cannot hold, and it is usually one of four shocks - moved "
           "to a darker or draughtier spot, dried out or left standing in water, a sudden cold "
           "night by a window, or a bowl of ripening fruit nearby, whose ethylene makes buds fall. "
           "Pick one thing, put it right, and give it two or three weeks before changing anything "
           "else."),
          avoid=("orchid", "orchids", "moth orchid", "phalaenopsis", "outside", "garden",
                 "border", "lawn", "allotment", "veg patch", "vegetable", "tree", "trees",
                 "tomato", "tomatoes", "courgette", "courgettes", "strawberry", "strawberries",
                 "chilli", "chillies", "chili", "pepper", "peppers", "cucumber", "cucumbers",
                 "squash", "pumpkin", "pumpkins", "marrow", "aubergine", "aubergines",
                 "eggplant", "peas", "beans", "runner", "broad bean", "broad",
                 "leaves", "leaf", "yellow", "yellowing", "drooping", "wilting", "wilt",
                 "brown tips", "brown", "tips", "spotted", "mould", "mold",
                 "buy", "gift", "present", "shop", "wedding", "funeral", "cut flowers"),
          ask=("flower", "flowers", "flowering", "bloom", "blooms", "blooming", "blossom",
               "blossoms", "blossoming", "bud", "buds", "petal", "petals", "spike", "spikes"),
          bias=2),

    entry("houseplant-bare-at-the-bottom",
          (("houseplant", "house plant", "houseplants", "house plants", "indoor plant",
            "indoor plants", "plant", "plants", "geranium", "geraniums", "pelargonium",
            "pothos", "spider plant", "trailing plant", "palm", "fern",
            "lily", "lilies", "peace lily", "peace lilies"),
           ("bare", "leggy", "spindly", "straggly", "skinny", "lost", "losing", "dropped",
            "dropping", "gone", "going", "no leaves", "nothing on", "stems with no",
            "too tall", "long and thin", "thin and long", "tall and thin", "stretched",
            "stretching", "etiolated", "bushy", "cut back", "cut it back", "trim it back",
            "prune")),
          ("A plant that is bare at the bottom, or long and thin instead of bushy, is short of "
           "light: the leaves at the top are the ones getting it and the stems below have dropped "
           "theirs for want of it. Move it nearer a window out of direct midday sun, turn it a "
           "quarter turn each week so it grows evenly, and in spring cut the long leafless stems "
           "back by about a third - new shoots come from the joints just below the cut, and bare "
           "stems will not leaf up again on their own. To make it bush rather than climb, pinch out "
           "the top pair of leaves every few weeks. If it needs to be smaller, take a cutting from "
           "the top first."),
          avoid=("flower", "flowers", "flowering", "bloom", "blooms", "blossom", "bud", "buds",
                 "orchid", "orchids", "moth orchid", "phalaenopsis", "christmas cactus",
                 "yellow", "yellowing", "brown", "spots", "spotted", "mould", "mold",
                 "drooping", "wilting", "wilt", "limp",
                 "tomato", "tomatoes", "cucumber", "cucumbers", "courgette", "courgettes",
                 "chilli", "chillies", "chili", "pepper", "peppers", "strawberry",
                 "strawberries", "pea", "peas", "bean", "beans", "outside", "garden", "border",
                 "lawn", "allotment", "veg patch", "vegetable", "tree", "trees", "shrub",
                 "shrubs", "hedge", "compost", "cut flowers"),
          guard=_the_stems_are_what_is_bare,
          bias=1),

    entry("houseplant-feed",
          (("plant food", "fertiliser", "fertilizer", "feed", "feeding", "plant feed"),
           ("feed", "feeding", "fertiliser", "fertilizer", "food"),
           ("houseplant", "houseplants", "house plant", "house plants", "indoor", "pot", "pots",
            "plants", "winter", "growing")),
          ("Feed houseplants from March to September, about once a month at half the strength on "
           "the bottle, and not at all in winter: most of them stop growing then, and the food just "
           "builds up in the compost. Fresh compost feeds a plant for the first couple of months, "
           "so nothing is needed after repotting."),
          avoid=("tomato", "tomatoes", "cucumber", "courgette", "pepper", "chilli", "lawn",
                 "grass", "rose", "roses", "vegetable", "allotment", "outside", "garden bed",
                 "crop", "dog", "cat", "baby",
                 "bird", "birds", "feeder", "feeders", "bird food", "bird table", "squirrel",
                 "squirrels", "hedgehog", "hedgehogs", "fox", "foxes", "wildlife",
                 "photosynthesis", "make food", "makes food", "made food", "make their food",
                 "make their own food", "make its own food", "own food", "their food",
                 "get food", "gets food", "get energy", "feed themselves", "carbon dioxide",
                 "chlorophyll", "sunlight", "oxygen")),

    entry("misting",
          (("misting", "mist my", "mist the", "should i mist", "mist them"),
           ("mist", "misting", "misted"),
           ("plant", "plants", "houseplant", "houseplants", "leaves", "fern", "calathea", "orchid",
            "humidity")),
          ("Misting does very little: it lifts the humidity for a few minutes and does not fix "
           "brown tips or stop a plant crisping. For a fern or a calathea, group it with other "
           "plants, keep it out of draughts and stand the pot on a tray of wet pebbles that the "
           "water can evaporate from; for anything else, the odd mist is mostly for you."),
          ask=INDOORS,
        ),

    entry("leaf-spots",
          (("spots on the leaves", "brown spots", "black spots", "leaf spots", "spots on my plant",
            "spotted leaves", "patches on the leaves"),
           ("spots", "spot", "spots on", "patches"),
           ("leaves", "leaf", "plant", "houseplant", "house plant", "indoor", "pot", "monstera",
            "peace lily", "pothos", "fern", "palm", "calathea", "ficus", "dracaena")),
          ("Round brown or black spots on the leaves are usually a fungus getting in where the leaf "
           "stayed wet. Take off the worst leaves and stop misting and splashing the leaves; water "
           "the compost instead, in the morning, and give the plant more air. If the spots are soft, "
           "spreading fast, or there is a smell, take it out of the room - rot in a stem does not "
           "come back."),
          avoid=("tomato", "tomatoes", "potato", "rose", "roses", "lawn", "grass", "garden",
                 "apple", "skin", "face", "child", "dog", "cat", "mole", "moles", "spot cream",
                 "sunspot", "age spot"),
          ask=INDOORS,
          bias=1,
        ),

    entry("not-flowering",
          (("not flowering", "isnt flowering", "isn't flowering", "never flowers", "never flower",
            "no flowers", "wont flower", "won't flower", "no buds", "not bloomed", "isnt blooming",
            "stopped flowering", "flower again",
            "to flower", "to bloom", "get it to flower", "flowering", "blooming"),
           ("flowering", "blooming", "bloom", "buds", "bud", "again", "reflower"),
           ("plant", "houseplant", "house plant", "indoor", "peace lily", "orchid", "cactus",
           "christmas cactus", "hoya", "amaryllis", "cyclamen", "african violet", "pot")),
          ("A houseplant that will not flower is usually short of light or being fed too much: "
           "most of them need a bright spot with a few hours of sun a day to set buds, and a feed "
           "high in nitrogen grows leaves at the flowers' expense, so switch to a tomato feed with "
           "more potash in late summer. Peace lilies and Christmas cacti also want cooler nights "
           "and a slightly pot-bound root to be nudged into flower; African violets want the light "
           "and nothing else changed."),
          avoid=("dropped", "dropping", "losing", "lost", "fallen", "falling", "fell",
                 "outside", "garden", "border", "lawn", "tree", "bulbs", "daffodil", "tulip",
                 "bed", "beds", "flower bed", "flowerbed", "planting flowers", "plant flowers",
                 "allotment", "veg patch", "vegetable patch", "outdoors",
                 "cherry", "fruit tree", "allotment", "vegetable", "wedding", "funeral",
                 "tomato", "tomatoes", "tomato plants", "courgette", "courgettes", "squash",
                 "pumpkin", "cucumber", "cucumbers", "runner bean", "runner beans", "beans",
                 "broad beans", "french beans", "strawberry", "strawberries", "chilli",
                 "chillies", "pepper plants", "aubergine", "aubergines", "veg patch",
                 "gift", "present", "buy her", "get her", "for her", "for my mum", "for my wife",
                 "bouquet", "anniversary", "birthday", "valentine", "mothers day", "mother's day",
                 "flowers or a plant", "flowers or plant"),
          ask=INDOORS,
        ),


    entry("sour-compost",
          (("pot smells", "smells in the pot", "smelly compost", "sour smell", "smells sour",
            "smells of sewage", "smells rotten", "stinks", "smelly soil", "mouldy smell",
            "bad smell from the pot"),
           ("smells", "smell", "smelly", "stinks", "stink", "sour", "rotten", "sewage",
            "mouldy"),
           ("plant", "pot", "compost", "soil", "houseplant", "house plant", "indoor", "roots",
           "watered")),
          ("A pot that smells sour or of drains is waterlogged compost going anaerobic, and the "
           "roots are already suffering: stop watering, tip out any water in the saucer, and let "
           "it dry out for a week or two. If the smell stays, take the plant out, cut away any "
           "roots that are brown and mushy, and repot it in fresh compost in a pot with holes."),
          avoid=("bin", "kitchen", "sink", "drain", "dishwasher", "washing machine", "fridge",
                 "nappy", "baby", "dog", "cat", "toilet", "room", "house", "flat", "car",
                 "fridge", "freezer", "feet", "breath", "mouth"),
          ask=INDOORS,
        ),
    entry("small-garden",
          (("small garden", "small gardens", "tiny garden", "little garden", "patio garden",
            "courtyard garden", "small space", "small plot", "small veg patch", "little plot",
            "balcony", "balconies", "window box", "windowbox", "container", "containers",
            "grow bag", "grow bags", "roof terrace", "yard"),
           ("what can i grow", "grow", "plant", "ideas", "best crops", "what to grow",
            "in a small", "worth growing", "start with", "beginner",
            "south facing", "sunny", "sun", "windy", "wind", "sheltered")),
          "Grow what gives you a lot from a little: salad leaves, radishes, spring onions, dwarf "
          "beans, cherry tomatoes, chillies, one courgette plant, herbs in a pot by the door, and "
          "strawberries in a basket. Go upwards where you can - beans and cucumbers up a frame, "
          "tomatoes in a grow bag - and sow a few seeds every three weeks rather than everything "
          "at once, so you eat from June to October instead of facing a glut in August. On a "
          "balcony, weight the pots, keep the tall things against the wall out of the wind, and "
          "follow the sun before you buy: a south or west wall grows tomatoes and herbs, a north "
          "one wants leaves, mint and ferns.",
          avoid=("lawn", "grass", "mow", "fence", "shed", "decking", "patio clean", "pressure",
                 "wash", "paint", "design", "landscap", "astroturf", "artificial",
                 "tomato", "tomatoes", "potato", "potatoes", "courgette", "courgettes",
                 "zucchini", "bean", "beans", "chilli", "chillies", "pepper", "peppers",
                 "strawberry", "strawberries", "herb", "herbs", "spinach", "rocket",
                 "lettuce", "salad", "carrot", "carrots", "onion", "onions", "pea", "peas",
                 "cucumber", "cucumbers", "kale", "cabbage", "broccoli", "beetroot",
                 "radish", "radishes", "pumpkin", "squash", "rhubarb", "garlic", "leek",
                 "leeks", "parsnip", "chard", "celery", "aubergine", "sweetcorn", "corn",
                 "tree", "trees", "apple tree", "shrub", "shrubs", "hedge", "hedges",
                 "climber", "climbers", "fruit tree")),
    entry("hanging-basket",
          (("hanging basket", "hanging baskets", "hanging basket plants", "basket plants"),
           ("how", "plant", "fill", "what to plant", "which plants", "look after", "water",
            "watering", "best", "keep", "dying", "dead", "liners", "line", "put",
            "what to put", "go in", "look good", "plant up", "planting up")),
          "Line it with a coco mat, or a bin bag with a few holes punched in the bottom, and use a "
          "compost that holds water. In a 30cm basket put four or five plants: something upright in "
          "the middle and trailing lobelia, petunia, bidens or trailing begonia round the edge. "
          "Water it every day in summer and twice on hot days, because a basket dries out faster "
          "than anything in the ground, and feed it with tomato feed every fortnight until "
          "September.",
          avoid=("hamper", "gift", "wicker", "laundry", "shopping", "easter",
                 "winter", "winters", "wintering", "overwinter", "overwintering", "frost",
                 "first frost", "keep it over", "keep them over", "next year")),
    entry("hanging-basket-winter",
          (("hanging basket", "hanging baskets", "basket", "baskets"),
           ("winter", "winters", "wintering", "overwinter", "overwintering", "frost",
            "first frost", "keep over", "keep it over", "keep them over", "die off", "dies off",
            "next year", "autumn", "october", "november")),
          "Cut it back and stop feeding, then move it against a wall out of the worst of the "
          "frost: most summer bedding will not come back, so a spring refill is the honest plan. "
          "Empty a basket you are leaving out and stand it dry, or the compost freezes solid and "
          "cracks the liner.",
          avoid=("hamper", "gift", "wicker", "laundry", "shopping", "easter", "washing basket",
                 "clothes", "fruit")),
    entry("raised-bed",
          (("raised bed", "raised beds", "raised bed kit", "raised planter", "raised vegetable bed",
            "raised beds for vegetables"),
           ("how", "build", "make", "fill", "depth", "how deep", "what soil", "line", "should i",
            "cheap", "best wood", "size", "how high",
            "cheaply", "cost", "what goes in", "bottom", "line it", "put in", "fill it",
            "what to fill", "grass", "lawn", "turf", "paving", "concrete", "patio", "slabs",
            "driveway", "what compost", "topsoil", "how much soil", "how many bags", "volume",
            "dries out", "drying out", "water", "watering", "wood", "timber", "sleepers",
            "bricks", "materials", "grow in", "plant in")),
          _a_raised_bed,
          bias=3,
          avoid=("mattress", "duvet", "sheet", "sheets", "bedroom", "hospital", "care home",
                 "cot", "toddler", "pillow", "frame", "sleep", "hotel", "bunk", "bunk bed",
                 "frost", "frosts", "fleece", "cloche", "snow", "freezing", "cold snap",
                 "wide", "width", "big", "large", "space", "size", "how many")),

    entry("crop-not-fruiting",
          (("courgette", "courgettes", "zucchini", "squash", "pumpkin", "pumpkins", "cucumber",
            "cucumbers", "runner bean", "runner beans", "french beans", "broad beans", "beans",
            "strawberry", "strawberries", "tomato", "tomatoes", "tomato plant", "tomato plants",
            "pepper", "peppers", "chilli", "chillies", "chili", "aubergine", "aubergines",
            "eggplant", "eggplants"),
           ("not fruiting", "no fruit", "not setting", "no setting", "not producing", "nothing",
            "no flowers", "not flowering", "no flowering", "wont flower", "will not flower",
            "not flowered", "flowering", "flowers", "flower", "flowers dropping", "flowers drop",
            "wont fruit", "will not fruit", "not producing fruit", "wont", "won't", "will not",
            "never sets", "not set a thing",
            "not setting fruit", "arent fruiting", "aren't fruiting", "arent setting fruit",
            "not set", "havent set", "hasnt set", "haven't set", "hasn't set", "didnt set",
            "didn't set", "set nothing", "setting nothing", "no fruit set",
            "dropping its flowers", "falling"
            " off", "falls off", "tiny", "small", "shrivelled", "bitter", "empty", "bare")),
          _crop_setting_reply,
          avoid=("botanical", "botanically", "is it a fruit", "fruit or a vegetable", "black",
                 "bottom", "blossom end", "rot", "split", "splitting", "yellow leaves", "ready to"
                 " pick", "how do i cook", "recipe", "chutney"),
          bias=1, guard=_a_small_place_ask),
    entry("watering-holiday", (("holiday", "holidays", "on holiday", "away", "going away",
                                "away for a week", "away for a fortnight", "while im away",
                                "while i'm away", "week away", "weekend away", "trip",
                                "vacation"),
                               ("plants", "garden", "pots", "watered", "watering")),
          "Before a week away, move the pots into shade, soak everything, and stand them on trays "
          "of water; a plastic bottle with a pinhole in the lid, upside down in the compost, keeps "
          "a big pot going for days. Anything precious is worth asking a neighbour to look in.",
          bias=2),
    entry("sow-seed", (("seed", "seeds", "seedling", "seedlings", "sow", "sowing"),
                       ("germinate", "germinating", "sprout", "coming up", "not", "fail")),
          "Seeds fail from cold soil, drying out, or being buried too deep: keep them at about "
          "18-20C, cover the tray with a clear lid until they show, and water from below so the "
          "surface stays damp. Compost over them only as deep as the seed is wide."),
    entry("rose-black-spot", (("rose", "roses", "rose bush", "rose bushes"),
                              ("black spot", "blackspot", "black spots", "spots", "spotted",
                               "yellow leaves", "losing leaves", "bare stems")),
          "Black spot is a fungus that overwinters on fallen leaves and splashes up in the rain: "
          "pick off every spotted leaf and bin it - never the compost - clear the fallen ones "
          "from the soil, and water the roots rather than the plant. Feed it and mulch with "
          "compost so it grows away from the spots, and in a bad year spray a rose fungicide "
          "when the first spots show.",
          ask=("black spot", "blackspot", "black spots", "spots", "spotted", "yellow",
               "losing leaves", "what is", "whats", "how do i", "treat", "cure", "stop"),
          bias=3,
          avoid=("not flowering", "no flowers", "wont flower", "won't flower", "prune",
                 "pruning", "tomato", "tomatoes", "potato", "potatoes")),
    entry("chit-potatoes", (("chit", "chitting", "chitted", "chits"),
                            ("potato", "potatoes", "seed potatoes", "spuds", "sprout",
                             "sprouting", "sprouts")),
          "Stand the seed potatoes in a single layer, eyes up, in a cool bright place - a windowsill "
          "in an unheated room, not a warm kitchen - for about six weeks from late January, and "
          "rub off all but the two or three strongest sprouts. An egg box or a tray works, and "
          "greening is fine; long white spindly shoots mean too warm and too dark."),
    entry("improve-soil", (("soil", "compost", "topsoil", "clay", "sandy soil", "soil is"),
                            ("improve", "better", "condition", "lighten", "break up", "poor",
                             "heavy", "clay", "drain", "drains", "enrich", "feed", "how do i",
                             "what should i add")),
          "Add organic matter and let the worms do the rest: two or three barrowloads of garden "
          "compost or well-rotted manure per bed, spread on top in autumn and left for the worms "
          "to pull in. On clay, grit and compost together open it up; on sand, compost holds the "
          "water. Mulch every autumn, do not dig it in, and never walk on a wet bed - the "
          "compaction is what most soil problems actually are.",
          ask=("how do i", "how", "what", "should i", "can i", "improve", "better", "add",
               "my soil", "the soil", "heavy clay", "clay soil"),
          avoid=("soil ph", "test my soil", "ph test", "potting compost", "seed compost",
                 "which compost", "ericaceous",
                 "make compost", "making compost", "compost at home", "compost bin",
                 "compost heap", "compost pile", "composting", "compost maker", "heap")),
    entry("courgette-no-fruit", (("courgette", "courgettes", "zucchini", "squash", "pumpkin",
                                  "pumpkins", "cucumber", "cucumbers", "marrow"),
                                 ("no fruit", "got no fruit", "not fruiting", "flowers fall",
                                  "flowers drop", "flowering but", "flowers but",
                                  "flowers but no fruit", "flowering but no fruit",
                                  "flowers but no courgettes", "flowers are",
                                  "drop off", "dropping off", "not setting", "no courgettes")),
          'Flowers dropping with no fruit is nearly always pollination: courgettes have separate male and female flowers, and the female one has a tiny fruit behind it that shrivels if no pollen arrives. Pick a male flower, strip the petals and dab it into the centre of a female one in the morning, and leave some male flowers on for the bees.',
          bias=2,
          ask=("my", "why", "what", "how", "help", "fruit", "flowers")),
    entry("prune-fruit-tree", (("apple tree", "apple trees", "pear tree", "pear trees", "plum tree",
                                 "fruit tree", "fruit trees", "cherry tree"),
                                GONE_WILD + ("prune", "pruning", "cut back", "trim",
                                             "when should i prune", "winter pruning",
                                             "shape")),
          "Prune apples and pears in winter, when they are dormant and you can see the shape: take "
          "out dead, damaged and crossing branches first, then shorten the growth you left by "
          "about a third. Plums and cherries are the exception - prune those in June or July, "
          "because winter cuts let silver leaf in. A young tree wants a clear centre like a "
          "goblet; an old one that has gone mad can be brought back over two or three winters "
          "rather than all at once.",
          ask=("how do i", "when", "how", "should i", "can i", "best time",
               "overgrown", "out of control", "taking over", "taken over", "gone wild",
               "too big"),
          avoid=("apple crumble", "apple pie", "cook", "recipe", "store the apples", "how long do apples")),
    entry("rhubarb-green", (("rhubarb", "rhubarb stems", "rhubarb stalks"),
                            ("green", "turning green", "gone green", "not red", "pale", "why")),
          "Green rhubarb is not a problem: some varieties are green-stemmed (Timperley Early goes "
          "pink, Victoria stays greener), and stems that were forced or shaded go redder than the "
          "same plant left in the open. Colour is variety and light, not ripeness - pick on stem "
          "size, and stop picking by the end of June so the crown can build up for next year. "
          "Only the leaves are poisonous, so cut those off and compost them.",
          ask=("why", "my", "are", "is", "should i", "can i", "what")),
    entry("fungus-gnats-rid", (("fungus gnat", "fungus gnats", "gnat", "gnats"),
                               ("get rid", "rid", "kill", "stop", "control", "gone", "everywhere",
                                "how do i", "how to", "deal with", "infestation")),
          "Let the top 2-3cm of compost dry right out between waterings and water from the bottom "
          "for a few weeks: the larvae live in wet compost and dry compost kills them. Stand a "
          "yellow sticky trap in the pot for the adults, put a layer of grit on the surface so "
          "they cannot lay, and repot into fresh compost if it is bad. A half potato pushed into "
          "the soil overnight collects larvae you can throw away.",
          avoid=("kitchen", "bin", "bananas", "sink", "drain", "fruit bowl", "wine", "vinegar")),
    entry("move-a-shrub", (("move", "moving", "moved", "transplant", "transplanting", "dig up",
                            "relocate"),
                           ("shrub", "shrubs", "bush", "bushes", "rose", "roses", "plant", "tree",
                            "climber", "hedge")),
          "Move a shrub while it is dormant, from late autumn to early spring, and on a mild day "
          "when the soil is not frozen. Water it the day before, dig out a rootball as wide as the "
          "branches spread, lift it onto a tarpaulin rather than by the stem, and replant at the same "
          "depth with the roots spread out. Water it weekly through the first summer and do not feed "
          "it - new roots come before new growth.",
          ask=("when", "how", "should i", "can i", "best time", "is it too late", "now"),
          avoid=("tomato", "tomatoes", "seedling", "seedlings", "houseplant", "houseplants",
                 "outside", "hardening", "pot on", "grown from seed", "into the ground",
                 "shed", "house", "office", "flat"),
          bias=1),
    entry("lavender-cuttings", (("lavender", "lavenders"),
                                ("cutting", "cuttings", "take cuttings", "propagate", "propagating",
                                 "multiply", "grow more", "clone")),
          "Take lavender cuttings in late summer, from the soft new growth at the tip and never "
          "from the old woody stem: a piece about 10cm long, stripped of its lower leaves, pushed "
          "into a pot of gritty compost, and kept damp in a bright but shaded spot. They root in "
          "six to eight weeks, and a plastic bag over the pot for the first fortnight keeps them "
          "from wilting. Autumn cuttings are ready to plant out the following spring.",
          ask=("how do i", "how", "when", "can i", "should i", "best time")),
    entry("seedlings-disappear", (("seedlings", "seedling", "seedlings have gone", "rows",
                                   "gaps in the row", "sown"),
                                  ("disappeared", "disappearing", "have gone", "has gone",
                                   "all gone", "eaten", "vanished", "missing", "nothing came up",
                                   "nothing has come up", "werent there")),
          "Whole seedlings vanishing overnight is slugs or snails, and the answer is a night patrol "
          "with a torch plus a beer trap sunk to the rim, not pellets scattered wide. If the tops are "
          "cut off cleanly and the plant is left standing, it is a bird or a rabbit, so net the row. "
          "Mice take pea and bean seeds out of the ground, and a cloche or some fleece stops them.",
          ask=("why", "how do i", "what", "any", "stop", "help",
               "have", "has", "all", "overnight", "in the night", "chewed", "nibbled", "got",
               "keep", "keeps", "kept", "keeping", "are", "is", "went", "something"),
          avoid=("leggy", "tall", "straggly", "pale", "thin", "yellow", "leaves")),
    entry("garden-not-flowering", (("buddleia", "buddleja", "lavender", "clematis", "lilac", "peony",
                             "daffodil", "daffodils", "tulips", "fuchsia", "hydrangea",
                             "delphinium", "gladioli", "sweet pea", "sweet peas", "dahlia",
                             "dahlias", "camellia", "rhododendron", "azalea"),
                            ("no flowers", "no flower", "no blooms", "no blossom", "not flowering",
                             "not flowered", "hasnt flowered", "hasn't flowered", "havent flowered",
                             "haven't flowered", "never flowered", "wont flower", "won't flower",
                             "didnt flower", "didn't flower", "didnt come up", "didn't come up",
                             "nothing came up", "blind")),
          "Most of these are one of four things: it was pruned at the wrong time - a shrub that "
          "flowers on last year's wood (lavender, lilac, clematis, peony) loses its buds if you "
          "cut it in spring - it is too shaded, it got too much nitrogen and grew leaves instead, "
          "or a late frost took the buds. Bulbs that never came up were planted too shallow or too "
          "late. Give it sun, a high-potash feed and the right pruning time.",
          avoid=("wisteria", "prune", "pruning", "cut back", "when should i", "how do i prune",
                 "deadhead", "yellow leaves", "brown leaves", "houseplant", "house plant",
                 "indoor", "peace lily", "orchid", "christmas cactus", "african violet"),
          ask=("no flowers", "no flower", "no blooms", "no blossom", "not flowering", "not flowered",
               "hasnt flowered", "hasn't flowered", "never flowered", "wont flower", "won't flower",
               "didnt flower", "didn't flower", "didnt come up", "didn't come up", "nothing came up",
               "blind")),

    entry("garden-birds",
          (("attract birds", "birds to my garden", "birds in the garden", "feed the birds",
            "bird feeder", "bird feeders", "bird table", "bird bath", "nest box", "nesting box",
            "more birds", "birds come"),
           ("how", "what", "feed", "feeding", "attract", "encourage", "bring", "get more",
            "bath", "table", "box", "food", "seeds", "fat balls", "winter")),
          "Food, water and cover, in that order: a feeder with mixed seed or fat balls, a shallow "
          "dish of water with a stone in it, and a shrub or a hedge to bolt into. Put the feeder "
          "where a cat cannot sit under it, leave the seed heads on perennials over winter, and "
          "skip the tidy-up in autumn - the birds eat the insects in the stems.",
          avoid=("parrot", "budgie", "cockatiel", "canary", "chicken", "pet", "roast", "recipe",
                 "cook", "eat", "flight", "airport", "turkey",
                 "feed", "feeds", "feeding", "fed", "what to feed", "bird food", "food for birds",
                 "seeds", "seed", "fat balls", "mealworms", "bread", "leftovers")),
    entry("hydrangea-care",
          (("hydrangea", "hydrangeas", "mophead", "lacecap", "hortensia"),
           ("care", "water", "watering", "how often", "look after", "looking after", "prune",
            "pruning", "cut back", "deadhead", "colour", "color", "blue", "pink", "purple",
            "yellow", "brown", "wilting", "drooping", "not flowering", "flowering", "feed",
            "plant", "grow", "move", "soil", "acid", "alkaline", "ericaceous", "lime")),
          _hydrangea,
          avoid=("shop", "bouquet", "wedding", "gift", "fake", "artificial", "silk", "hair",
                 "lipstick", "nail",
                 "wilting", "wilted", "wilt", "brown", "browning", "drooping", "droopy", "dying",
                 "died", "dead", "prune", "pruning", "pruned", "cut back", "cutting back",
                 "deadhead", "deadheading", "spring", "march")),
    entry("aspidistra-care",
          (("aspidistra", "aspidistras", "cast iron plant", "cast-iron plant"),
           ("care", "water", "watering", "how often", "look after", "brown", "yellow", "dying",
            "drooping", "leaves", "leaf", "repot", "split", "feed", "light", "keep alive")),
          "An aspidistra wants the opposite of fuss: a spot out of direct sun, water only when "
          "the compost is dry to the touch, and almost nothing in winter. Brown tips and splitting "
          "leaves are dry air or a wet pot rather than hunger, so let it drain and stand it "
          "somewhere less dry rather than feeding it.",
          avoid=("fake", "artificial", "buy", "shop", "flower", "gift")),
    entry("paving-moss",
          (("moss", "mossy", "algae", "green", "greens up", "slippery", "slippy", "slick",
            "slime", "lichen", "weeds", "weed", "weeded"),
           ("paving", "patio", "path", "paths", "driveway", "drive", "block paving",
            "blockpaving", "pavers", "slabs", "slab", "blocks", "stepping stones", "bricks",
            "brick", "between the stones", "between the slabs", "between the paving",
            "between the flags", "joints", "gaps", "growing between", "growing through",
            "keep coming back", "come back every year", "decking", "deck", "concrete", "tarmac",
            "terrace", "yard", "steps", "stone flags", "flags", "gravel", "roof", "roofs")),
          "Moss on paving is damp plus shade, so the fix is to open up the joints and let them "
          "dry: scrape it out with a patio knife or a stiff brush, then refill the gaps with "
          "kiln-dried sand rather than soil. A pressure wash clears it in an afternoon but it "
          "comes back in the same damp corner, so if you want what is left dead rather than gone, "
          "biological washing powder or white vinegar on the paving, left half an hour and then "
          "scrubbed and rinsed, does that - nothing keeps it away while the joint stays wet. "
          "Weeds in the joints come out with a knife or an old screwdriver and a "
          "kettle of boiling water down the gap stops the next lot; on decking keep the jet low "
          "and go along the grain, because a hard one furries softwood.",
          bias=1,
          avoid=("lawn", "grass", "turf", "mow", "scarify", "roof", "gutter", "guttering",
                 "wall", "walls", "fence", "pond", "tank", "aquarium", "fish tank", "tree",
                 "trees", "shade", "flower bed", "borders", "hanging basket", "shed",
                 "oil", "oils", "diesel", "petrol", "grease", "fuel", "paint", "cement", "render",
                 "mortar", "resin", "tar spot", "blood", "vomit", "poo", "bird mess",
                 "snow", "snowed", "ice", "icy", "grit", "gritted", "salt",
                 "table", "tables", "chair", "chairs", "bench", "benches", "seat", "seats",
                 "umbrella", "umbrellas", "parasol", "parasols", "heater", "chiminea",
                 "planter", "planters", "pot", "pots", "trough", "troughs", "swing",
                 "hot tub", "door", "doors", "gate", "gates", "bbq", "barbecue")),
    entry("paving-slab",
          (("paving slab", "paving slabs", "patio slab", "patio slabs", "paving stone",
            "paving stones", "flagstone", "flag stone", "flagstones", "slab", "slabs",
            "block paving", "stepping stone", "stepping stones", "patio"),
           ("broken", "broke", "cracked", "crack", "cracks", "loose", "wobbly", "rocking",
            "rocks", "rock", "sunken", "sunk", "dipped", "uneven", "lift", "lifting", "lifted",
            "replace", "replacing", "repair", "fix", "how do i", "coming up", "came up")),
          "Lift it with a spade or two thin chisels and keep the pieces to match the colour, then "
          "bed it back on a full layer of sharp sand and mortar rather than four dabs at the "
          "corners, which is what lets a slab rock. Tap it down level with its neighbours with a "
          "rubber mallet, running a straight edge across the joints, and leave it 24 hours before "
          "you brush sand in. A slab cracked in two can be glued with exterior resin, but the "
          "crack will always show.",
          avoid=("moss", "mossy", "weed", "weeds", "weeding", "pressure wash", "pressure washing",
                 "clean", "cleaning", "stain", "oil", "algae", "slippy", "slippery",
                 "patio heater", "patio doors", "furniture", "table", "chairs")),

    entry("roof-moss",
          (("moss", "mossy"),
           ("roof", "roofs", "gutter", "gutters", "guttering", "downpipe", "downpipes", "tile",
            "tiles", "roof tiles", "slates", "shed roof", "chimney")),
          "Moss on a roof wants a scraper rather than a pressure washer: scrape it off dry, let "
          "the tiles air, and clear the gutters and downpipes so the rain runs away instead of "
          "feeding it. Don't pressure-wash an old roof - it strips the surface and finds leaks you "
          "did not have. If it comes back every year on a north-facing slope, a copper or zinc "
          "strip along the ridge kills it slowly as the rain washes over it.",
          bias=1),
    entry("bamboo-spread",
          (("bamboo", "bamboos", "running bamboo", "bamboo roots", "bamboo rhizomes"),
           ("spread", "spreading", "spreads", "contain", "containing", "containment",
            "take over", "taking over", "taken over", "control", "controlling", "stop",
            "stopping", "invasive", "everywhere", "rhizome", "rhizomes", "root barrier",
            "barrier", "neighbours", "neighbors", "get rid")),
          ("A running bamboo spreads with rhizomes just under the surface, so it is contained "
           "rather than pruned: a root barrier of thick polythene or HDPE, 60cm deep and set at a "
           "slight angle outwards, all the way round, with the top 2cm left showing above the soil "
           "so you can see a rhizome trying to hop it and cut that off. Never dump a dug-out "
           "rhizome on the compost heap: it roots."),
          avoid=("shoot", "shoots", "eat", "eating", "cook", "cooking", "stir fry", "stir-fry",
                 "recipe", "canes", "cane", "stakes", "plant support", "flooring", "blind",
                 "blinds", "mat", "mats", "towel", "sushi", "steamer", "basket"),
          bias=2),
    entry("bay-yellow",
          (("bay tree", "bay trees", "bay bush", "bay hedge", "bay plant", "bay leaf plant",
            "bay"),
           ("yellow", "yellowing", "going yellow", "gone yellow", "pale", "brown", "dropping",
            "dropping leaves", "losing leaves", "dying", "patchy")),
          "A bay that has gone yellow is usually water at the roots - it hates standing wet in "
          "winter and drying right out in summer - so check the drainage and water it in a dry "
          "spell. If the yellow leaves are on one side and feel sticky underneath, look for bay "
          "sucker or scale insects and wipe them off; a pale bay in a pot is often simply hungry, "
          "and a liquid feed through the summer greens it up.",
          avoid=("window", "windows", "bay window", "car", "parking", "park", "garage",
                 "recipe", "cook", "sauce", "soup", "stock", "dried", "supermarket", "buy")),
    entry("pots-drying",
          (("pots", "pot", "containers", "planters", "tubs", "window boxes"),
           ("drying out", "dry out", "dries out", "dried out", "water", "watering", "watered",
            "keep them watered", "hot weather", "heatwave", "holiday", "while i am away",
            "while im away")),
          "Group the pots together out of the wind, mulch the compost with gravel or bark, and "
          "stand them in a saucer so the water that runs through soaks back up. A big pot dries "
          "out far slower than a small one, so pot up rather than watering more, and in a heatwave "
          "check them morning and evening - a pot whose roots fill it can want water twice a day.",
          avoid=("dishes", "washing up", "cook", "cooking", "pan", "tea", "coffee", "yogurt",
                 "yoghurt", "jam", "supermarket", "buy", "shop", "sell", "money", "paint"),
          bias=1),
]

ENTRIES.append(entry(
    "hedge-gone-brown-at-the-base",
    (("hedge", "hedges", "privet", "box hedge", "conifer hedge", "leylandii", "laurel hedge",
      "beech hedge", "hornbeam", "yew", "yew hedge"),
     ("brown at the bottom", "brown at the base", "brown at the base", "gone brown",
      "bare at the bottom", "bare at the base", "bald at the bottom", "dead at the bottom",
      "bare patch", "bare patches", "patchy", "yellow", "yellowing", "yellowed", "thin",
      "sparse", "gaps", "gap", "not growing", "looks dead", "looking sorry", "sorry for itself",
      "looks bad", "looks sad", "dying", "died", "brown", "no leaves", "leaves falling",
      "dropping leaves", "bare", "bald", "bald patch", "bald patches", "patches", "patchy",
      "see through", "holes in it")),
    "Almost always the top has grown wider than the base, so the bottom sits in its own shade "
    "and the light never gets to it: cut the sides back so they slope in towards the top, take "
    "the height down a little at the same time, and feed and water the base - that is what makes "
    "it shoot again. Privet, yew, beech and hornbeam come back from old wood; leylandii and most "
    "conifers do not, so on those you cut only into green growth and accept the bare patch. If "
    "the brown is patchy and spreading with no shape to it, check for box blight or a vine weevil "
    "in the soil before you feed anything.",
    avoid=("neighbour", "neighbours", "neighbour's", "next door", "boundary", "blocking my light",
           "blocks my light", "right to light", "council", "too tall", "too high", "planning",
           "when should i cut", "when do i cut", "how often should i cut", "how do i cut",
           "what time of year"),
    bias=2))
ENTRIES.append(entry(
    "sunflowers",
    (("sunflower", "sunflowers", "sun flower", "sun flowers"),
     ("full sun", "sun", "sunny", "sunlight", "shade", "shaded", "north facing", "where",
      "plant", "planting", "sow", "sowing", "grow", "growing", "when", "how tall", "height",
      "stake", "stakes", "slugs", "snails", "yellow leaves", "drooping", "not flowering",
      "no flowers", "pot", "pots", "container", "variety", "varieties", "seeds", "seed",
      "from seed", "how far apart", "spacing")),
    "Six hours of direct sun, and shelter from the wind: in shade a sunflower grows tall and thin "
    "and then flops. Sow indoors in April or straight outside in May, 2cm deep and 45cm apart, "
    "and stake the tall varieties early rather than after they lean. Water and feed weekly once "
    "the bud shows, and put a slug barrier round them while they are small, because that is what "
    "takes them.",
    avoid=("eat", "eaten", "edible", "roast", "cook", "recipe", "oil", "seeds to eat")))

ENTRIES.append(entry(
    "tree-looks-dead",
    (("tree", "trees", "apple tree", "oak", "maple", "birch", "willow", "cherry tree", "plum tree",
      "pear tree", "fruit tree", "sapling", "conifer"),
     ("dead", "died", "dying", "looks dead", "not coming back", "no buds", "no new growth",
      "still alive", "is it alive", "brown", "bare branches", "snapped", "scratch", "revive")),
    "Scratch the bark on a young twig with a fingernail: green and damp underneath means that "
    "branch is alive, dry and brown means it is not, so do three or four round the tree rather "
    "than one. Wait until mid-spring before you write it off, because a hard winter, a late frost "
    "or a dry summer makes a healthy tree leaf out late or drop its leaves early, and a bud that "
    "is plump and firm in late winter is a tree that is still coming back. If most of the "
    "scratches are brown, look for the reason before you buy a replacement: waterlogged ground, "
    "mulch heaped against the trunk, the root flare buried when it was planted, or a strimmer "
    "wound at the base are what kill a garden tree rather than old age.",
    avoid=("prune", "pruning", "pruned", "cut back", "when should i cut", "how do i cut",
           "plant", "planting", "planted", "sow", "sowing", "grow", "growing", "hedge", "hedges",
           "privet", "leylandii", "cut down", "fell", "felling", "stump", "neighbour",
           "neighbours", "next door", "boundary", "planning", "council", "treehouse",
           "christmas tree", "family tree",
           "leaves are turning", "turning yellow", "turning brown in autumn", "losing leaves",
           "leaves falling")))

ROSE_NOT = ("vase", "vases", "bouquet", "bouquets", "cut flowers", "cut flower", "florist",
            "picked", "in water", "flower food", "mothers day", "mother's day", "valentine",
            "valentines", "wedding", "bunch",
            "greenfly", "blackfly", "aphid", "aphids", "black spot", "blackspot", "spot",
            "spots", "spotted", "rust", "mildew", "prune", "pruning", "pruned", "deadhead",
            "deadheading", "plant", "planting", "planted", "bare root", "sow", "sowing",
            "flower", "flowers", "flowering", "bloom", "blooms")


def _rose_care(memory, understood):
    line = _words(understood)
    if _has(line, "water") or _has(line, "watering") or _has(line, "how often") \
            or _has(line, "hosepipe"):
        return ("A rose in the ground wants a full watering can per plant each week in dry weather, "
                "poured at the base rather than over the leaves, and a rose in a pot wants that "
                "much every other day in summer, because a pot dries out far faster than the soil. "
                "Water in the morning, and give it a proper soak: a light sprinkle every evening "
                "only wets the top inch, and the roots stay shallow and thirsty.")
    if _has(line, "feed") or _has(line, "feeding") or _has(line, "fertiliser") \
            or _has(line, "fertilizer"):
        return ("Feed a rose with a rose feed, not a general one, from the first leaves in spring "
                "until the end of July: a handful of granules round the base in March and again in "
                "June, watered in, or a liquid feed every fortnight while it flowers. Stop by "
                "August so the new growth hardens before winter, and never feed a dry plant - "
                "water it first, or the feed burns the roots.")
    if not any(_has(line, w) for w in ("ground", "garden", "bush", "bushes", "border", "pot",
                                       "soil", "beds", "bed", "shrub", "climbing", "patio",
                                       "plotted", "planted", "allotment", "leaves", "leaf",
                                       "stems", "stem", "roots", "root", "buds", "bud",
                                       "shoots", "hedge")):
        return ("Cut roses die in a day or two for a simple reason: trim 2cm off each stem at an "
                "angle, strip any leaf that would sit in the water, change the water every other "
                "day and keep them out of sun. A rose in the ground that looks dead is usually "
                "thirsty or hungry instead: a full can a week at the base, a rose feed while it "
                "flowers, and cut the brown stems back to green wood - one dry fortnight drops "
                "every leaf before the plant is dead.")
    return ("A rose in the ground is nearly always thirsty, hungry or short of air: water it at the "
            "base, a full can a week in dry spells, more in a pot, and feed it with a rose feed "
            "while it flowers. Cut out the yellowing and spotted leaves and bin them rather than "
            "compost them, because black spot and rust live on the fallen leaves and splash back up "
            "in the rain. If the stems themselves are brown and dry, prune those back to green wood "
            "and water: a rose left dry for a fortnight drops its leaves and looks dead before it "
            "is.")


ENTRIES.append(entry(
    "rose-care",
    (("rose", "roses", "rose bush", "rose bushes", "climbing rose", "climbing roses",
      "shrub rose", "shrub roses", "rambling rose", "patio rose"),
     ("dying", "died", "wilting", "wilts", "wilted", "drooping", "droopy", "yellow", "yellowing",
      "brown", "no leaves", "losing leaves", "lost its leaves", "bare", "looking sad",
      "look sad", "looks sad", "looking poorly", "poorly", "not looking well", "sulking",
      "revive", "keeping alive", "keep alive", "look after", "looking after", "care", "care for",
      "water", "watering", "feed", "feeding", "fertiliser", "fertilizer", "how often")),
    _rose_care,
    avoid=ROSE_NOT,
    bias=2))

ENTRIES.append(entry(
    "frost-protection",
    (("frost", "frosts", "frosty", "freezing", "freeze", "frozen", "cold snap",
      "cold spell", "cold night", "cold nights", "sub zero", "minus", "cold weather", "cold",
      "winter", "winters", "overwinter",
      "warm", "warmer", "heat", "heating", "insulate", "overnight"),
     ("plant", "plants", "garden", "seedlings", "seedling", "veg", "vegetables",
      "flowers", "pots", "shrub", "shrubs", "bedding", "tender", "protect", "cover",
      "bed", "beds", "flower bed", "flower beds", "raised bed", "raised beds",
      "border", "borders", "allotment",
      "damage", "survive", "fleece", "greenhouse", "hanging basket", "baskets",
      "cuttings", "banana plant", "tree fern", "citrus", "olive",
      "greenhouses", "bubble wrap")),
    "Water the soil the day before: wet soil holds the day's heat and gives it back at night, "
    "and dry soil gives back nothing. At dusk, not at midnight, put fleece, an old net curtain "
    "or a doubled bedsheet over the plants and take it off in the morning, and push pots "
    "together against a house wall and off the ground, because the wall and the slab give out "
    "heat all night. In a greenhouse, bubble wrap the glass and cover the plants, and a paraffin "
    "heater or a hot water bottle under a cloche does the rest. Most damage shows up two days "
    "later as blackened leaves: leave them on until spring because they are insulation, and "
    "start watching the forecast from about 5C, which is when the tender things start to go.",
    avoid=("houseplant", "houseplants", "house plant", "house plants", "monstera", "orchid",
           "lawn", "grass", "mow", "pond", "ponds", "fish", "car", "windscreen",
           "windscreen cover", "pipes", "pipe", "boiler", "radiator",
           "snails", "slugs", "weeds", "prune", "pruning",
           "smelly", "brown and soft", "drooping", "wilted", "limp",
           "dog", "dogs", "puppy", "puppies", "cat", "cats", "kitten", "kittens",
           "rabbit", "rabbits", "hamster", "hamsters", "guinea pig", "budgie", "parrot",
           "pet", "pets", "animal", "animals", "horse", "chickens",
           "keep warm", "stay warm", "keep myself", "keep us warm", "keep the house",
           "house", "home", "flat", "living room", "bedroom", "room", "rooms",
           "in bed", "cold in bed", "feet", "foot", "hands", "hand", "fingers", "finger",
           "toes", "toe", "blanket", "duvet", "sleep", "sleeping",
           "my nan", "my mum", "my dad", "elderly", "heating bill", "energy bill",
           "bills", "bill", "thermostat", "radiator", "radiators", "boiler"),
    guard=_the_cold_is_the_garden_s))

ENTRIES.append(entry(
    "pond-in-winter",
    (("pond", "ponds", "fish", "goldfish", "koi"),
     ("freeze", "freezes", "freezing", "frozen", "ice", "iced over", "icing over",
      "winter", "overwinter", "winterise", "winterising", "the hole", "a hole", "keep a hole",
      "pump", "filter",
      "feed", "feeding", "fed", "fish", "bottom", "cover")),
    "Never smash the ice: the shock wave stuns and kills the fish. Float a ball on the surface "
    "so it keeps a hole open as it moves, or stand a pan of hot water on the ice until it melts "
    "through, and keep a hole open all winter so the gases can get out. Keep the pump and filter "
    "running, but turn off any fountain above the water because the splash chills the pond. Stop "
    "feeding once the water is below 10C, because the fish stop digesting and the food rots, and "
    "they sit together at the bottom where the water sits at about 4C. Net the leaves out in "
    "autumn, because a rotting layer on the bottom is what turns the water green in spring.",
    avoid=("green water", "algae", "blanket weed", "blanketweed", "filter not working",
           "tank", "tanks", "aquarium", "fish tank", "fish tanks", "fishbowl", "indoor",
           "in the house", "bedroom", "living room", "noisy", "rattling", "humming",
           "my fish is sick", "fish are dying", "build a pond", "dig a pond", "pond liner",
           "how big", "frogs", "frog", "newts", "tadpoles",
           "cook", "cooking", "recipe", "eat", "eating", "defrost", "thaw", "bake", "baked",
           "fry", "fried", "oven", "pan", "shop", "supermarket", "instead", "dinner",
           "fillets", "fillet", "fresh", "tin", "tinned", "fish fingers", "batter",
           "bought from", "is it safe",
           "can i freeze", "can i refreeze", "in the freezer", "the freezer", "freezer bag",
           "freeze it", "keep fish in the fridge", "how long can i keep"),
    guard=_a_winter_pond_line, bias=1))

ENTRIES.append(entry(
    "pond-in-summer",
    (("pond", "ponds", "goldfish", "koi"),
     ("green", "greener", "greenest", "pea soup", "cloudy", "murky", "mucky", "dirty",
      "algae", "alga", "blanket weed", "blanketweed", "weed", "sludge", "silt",
      "clear", "clearing", "clean", "cleaning", "spring clean", "filters", "filter",
      "pump", "leaves", "feed", "feeding", "how often", "how much", "oxygen",
      "water quality", "smell", "smells", "smelly")),
    "Green water is algae feeding on sunlight and on the nutrients in the water, so the fix is to "
    "take one of those away: put a water lily or floating plants over half the surface for shade, "
    "and plant up the margins so the water has less of the light and the feed it needs. Barley "
    "straw in a mesh bag slows blanket weed and is harmless to the fish, and a dark dye does the "
    "same job in a pond with no plants in it. Rinse the filter sponges in a bucket of pond water, "
    "never under the tap, because the chlorine kills the bacteria that keep the water clear, and "
    "clean them a little at a time so the pond never loses its whole filter in one afternoon. "
    "Feed the fish what they clear in five minutes, once a day in warm weather, and not at all "
    "below 10C, because the food they leave is what turns the water green. For blanket weed, "
    "twirl it out with a stick rather than reaching in, and net the leaves out in autumn before "
    "they sink, because the sludge on the bottom is next summer's algae.",
    avoid=("freeze", "freezes", "freezing", "frozen", "ice", "iced", "icy", "winter",
           "winters", "overwinter", "winterise", "winterize", "cold snap", "frost",
           "my fish is sick", "fish are dying", "fish is dying", "gasping", "ammonia",
           "build a pond", "dig a pond", "pond liner", "how big", "leaking", "leak",
           "frogs", "frog", "newts", "tadpoles", "heron", "tank", "aquarium", "bowl",
           "indoor", "tap water", "drinking water", "milk",
           "stopped working", "not working", "broken", "packed up", "stopped running",
           "isnt working", "isn't working", "tripping", "noisy",
           "feed", "feeds", "feeding", "fed", "food", "flakes", "flake", "pellets",
           "pellet", "overfeed", "overfeeding",
           "cook", "cooking", "recipe", "eat", "eating", "defrost", "thaw", "bake",
           "fry", "fried", "oven", "pan", "shop", "supermarket", "dinner", "fillets",
           "fillet", "fish fingers", "batter", "salad", "smoothie", "juice"),
    guard=_a_summer_pond_line))

_JOBS_IN_WINTER = (
    "The garden in winter is mostly tidying and waiting: clear the dead stems but leave seed "
    "heads and any hollow stalks standing, because insects shelter in them and the birds eat "
    "the seeds. Mulch bare soil with compost or bark, but only once the ground is not frozen, "
    "and stay off wet or frozen grass because footprints kill the blades under them. Prune apples "
    "and pears and any shrub that flowers on this year's wood, clean and sharpen the tools, and "
    "wash out the greenhouse with a mild disinfectant before spring sowing. Pots are what the "
    "cold kills, so move them against a wall, raise them onto feet so the drainage hole does not "
    "sit in water, and give tender plants a layer of bubble wrap. Check the stored produce and "
    "the dahlias every couple of weeks for rot, and order seeds in January, because the quiet "
    "months are the only time the garden has nothing urgent in it.")

JOBS_IN = {
    "spring": (
        "Spring goes in this order: rake the lawn and fork the beds once the soil has dried out "
        "enough not to clod, mulch the borders with compost before the weeds start, and prune "
        "the shrubs that flower on the wood they made last year - roses, buddleia, fuchsia - "
        "while they are still dormant. Sow the hardy veg outdoors, harden off anything you "
        "raised indoors for a week before it goes out, and feed the lawn once the grass is "
        "growing. Then watch the forecast, because a late frost is what takes the blossom and "
        "the new leaves, and a sheet of fleece over a flowering fruit tree earns its keep."),
    "summer": (
        "Summer is watering, feeding and picking: soak the beds in the evening rather than "
        "sprinkling them every day, mulch while the soil is damp to hold that water in, and "
        "water the things you planted this year first, because their roots are still shallow. "
        "Deadhead the flowers so they keep coming, feed anything in a pot every week or so, and "
        "cut the lawn a little higher rather than scalping it, which browns it in a dry spell. "
        "Pick courgettes, beans and salad small, because a plant left to swell stops making "
        "more, and get the weeds out before they set seed."),
    "autumn": (
        "Autumn is clearing and planting: pull the spent crops and annuals into the compost, "
        "plant bulbs and bare-root roses, fruit trees and hedging while the soil is still warm, "
        "and rake the leaves off the lawn and out of the pond. Cut back what has finished but "
        "leave the seed heads standing for the birds, mulch the beds, and give the lawn a late "
        "cut with an autumn feed rather than a short one. Then check what is stored - apples, "
        "onions, dahlias - for rot, and order next year's seed and bare-root plants, because "
        "the good varieties go early."),
    "winter": _JOBS_IN_WINTER,
}

_GARDEN_JOBS = (
    "jobs", "job", "what do i do", "what can i do", "what should i do", "what do i need to do",
    "what should i be doing", "what should i do next", "what needs doing", "whats to do",
    "what is there to do", "anything to do", "work to do", "tasks", "chores",
    "keep on top of", "tidy up",
)
_GARDEN_MONTHS = {
    1: "winter", 2: "winter", 3: "spring", 4: "spring", 5: "spring", 6: "summer",
    7: "summer", 8: "summer", 9: "autumn", 10: "autumn", 11: "autumn", 12: "winter",
}
_GARDEN_SEASON_WORDS = {
    "spring": ("spring", "springtime", "march", "april", "may", "early in the year"),
    "summer": ("summer", "summertime", "june", "july", "august", "the hot weather"),
    "autumn": ("autumn", "fall", "september", "october", "november"),
    "winter": ("winter", "winters", "wintertime", "december", "january", "february"),
}
_GARDEN_NOW = re.compile(r"\bnow\b|\bat the moment\b|\bthis month\b|\bcurrently\b|"
                         r"\bright now\b|\btoday\b|\bthis week\b|\bthis weekend\b|"
                         r"\bthis time of year\b|\bat the minute\b|\bthese days\b")
_GARDEN_THINGS = (
    "garden", "gardens", "lawn", "grass", "plot", "allotment", "allotments", "borders",
    "flowerbed", "flowerbeds", "flower bed", "flower beds", "beds", "bedding", "hedge",
    "hedges", "shrubs", "shrub", "veg", "vegetables", "veggie patch", "veg patch",
    "greenhouse", "pond", "compost", "beds and borders",
)


def _the_season_named(understood):
    line = _words(understood)
    for season in ("spring", "summer", "autumn", "winter"):
        if any(_has(line, word) for word in _GARDEN_SEASON_WORDS[season]):
            return season
    if _GARDEN_NOW.search(line):
        month = _this_month()
        if month is not None:
            return _GARDEN_MONTHS[month]
    return None


def _a_garden_line(understood):
    line = _words(understood)
    if any(_has(line, word) for word in _GARDEN_THINGS):
        return True
    topics = []
    for key in ("topic", "topics"):
        held = understood.get(key)
        if isinstance(held, str):
            topics.append(held)
        elif isinstance(held, (list, tuple, set)):
            topics.extend(str(one) for one in held)
    return "garden-and-plants" in topics


def _garden_jobs(memory, understood):
    line = _words(understood)
    if not any(_has(line, word) for word in _GARDEN_JOBS):
        return None
    if not _a_garden_line(understood):
        return None
    season = _the_season_named(understood)
    if season is None:
        return None
    return JOBS_IN[season]


def _an_ask_about_now(understood):
    line = _words(understood)
    if not _GARDEN_NOW.search(line):
        return False
    if not any(_has(line, word) for word in _GARDEN_JOBS):
        return False
    if not _a_garden_line(understood):
        return False
    for season in ("spring", "summer", "autumn", "winter"):
        if any(_has(line, word) for word in _GARDEN_SEASON_WORDS[season]):
            return False
    return _the_season_named(understood) is not None


def _not_about_now(understood):
    return not _an_ask_about_now(understood)


ENTRIES.append(entry(
    "garden-jobs-in-a-season",
    (_GARDEN_JOBS,
     ("spring", "springtime", "march", "april", "may", "summer", "summertime", "june", "july",
      "august", "autumn", "fall", "september", "october", "november", "winter", "winters",
      "wintertime", "december", "january", "february", "now", "at the moment",
      "this time of year", "today", "this week", "this weekend", "at the minute")),
    _garden_jobs,
    avoid=("frost", "frosts", "frosty", "forecast", "cold snap", "tonight", "fleece",
           "houseplant", "houseplants", "house plant", "monstera", "orchid", "pond",
           "mow", "mowing", "mower", "scarify", "scarifying", "scarifier", "prune my",
           "pruning", "sow", "sowing", "plant", "planting", "weeds", "weeding", "weed",
           "sick", "dying", "yellow", "yellowing", "disease", "pest", "pests", "slug",
           "snail", "snails", "christmas", "bedding", "hanging basket", "window box")))

ENTRIES.append(entry(
    "garden-in-winter",
    (("garden", "gardens", "plot", "allotment", "allotments", "borders", "flowerbeds"),
     ("winter", "winters", "wintertime", "december", "january", "february", "cold months",
      "wet", "quiet", "nothing to do", "jobs", "job", "tidy", "tidy up", "put to bed",
      "over winter", "this time of year", "dark", "rain")),
    JOBS_IN["winter"],
    avoid=("frost", "frosts", "frosty", "freezing", "frozen", "cold snap", "forecast",
           "tonight", "cover", "fleece", "greenhouse", "pond", "lawn", "mow", "mowing",
           "houseplant", "houseplants", "house plant", "monstera", "orchid", "prune my",
           "dead", "dying", "sick", "yellow", "christmas",
           "spring", "springtime", "march", "april", "may", "summer", "summertime", "june",
           "july", "august", "autumn", "september", "october", "november", "this spring",
           "this summer", "this autumn"),
    guard=_not_about_now,
    bias=1))

ENTRIES.append(entry(
    "christmas-tree",
    (("christmas tree", "christmas trees", "xmas tree", "the tree", "spruce", "fir",
      "nordmann", "norway spruce"),
     ("keep alive", "alive", "last", "longer", "drop", "dropping", "needles", "needle drop",
      "water", "watering", "look after", "care", "fresh", "dying", "best", "choose",
      "buy", "real tree", "stand", "base")),
    "A cut tree drinks about a litre a day, so stand it in a bucket of water, saw a couple of "
    "centimetres off the trunk first so it can take water up, and keep the base covered - a "
    "trunk that dries seals over and stops drinking. Keep it away from a radiator, a fire and "
    "the sunny window, and it will hold its needles for about four weeks instead of one. A "
    "Nordmann fir drops far less than a Norway spruce, which is the one that sheds as you bring "
    "it in. A potted tree with roots is a different animal: keep it cool and light in a porch "
    "or greenhouse, bring it in for no more than a week, and plant it out after Christmas.",
    avoid=("take it down", "take my tree down", "twelfth night", "5 january", "6 january",
           "12th night", "dispose", "recycle", "recycling", "tip", "chuck", "lights",
           "fairy lights", "decorations", "baubles", "tinsel", "star", "buy a tree",
           "how much does a tree cost", "real or fake", "fake tree", "artificial"),
    guard=_a_christmas_tree))

ENTRIES.append(entry(
    "garden-tree",
    (("tree", "trees", "sapling", "saplings", "fruit tree", "fruit trees", "apple tree",
      "pear tree", "plum tree", "cherry tree"),
     ("plant", "planting", "planted", "choose", "choosing", "pick", "picking",
      "water", "watering", "how often", "prune", "pruning", "feed", "feeding", "stake",
      "stake it", "staked", "bare root", "bare-root", "when", "how", "which", "what",
      "small garden", "pot", "growing", "grow", "move", "moving", "far from", "distance")),
    _garden_tree,
    avoid=("christmas", "xmas", "spruce", "fir", "nordmann", "norway spruce", "needles",
           "needle drop", "tinsel", "baubles", "decorations", "cut tree", "cut my tree",
           "dead", "dying", "died", "dying back", "brown", "wilted", "treehouse", "tree house",
           "family tree", "decision tree", "route", "syntax tree", "genealogy",
           "nut", "nuts", "tree nuts", "peanut", "peanuts", "allergic", "allergy",
           "allergies", "allergen", "intolerant"),
    guard=_a_garden_tree))

ENTRIES.append(entry(
    "citrus-in-a-pot",
    (("lemon tree", "lemon trees", "orange tree", "lime tree", "citrus", "citrus tree",
      "citrus trees", "calamondin", "kumquat", "lemon plant", "orange plant"),
     ("look after", "care", "cared", "keep alive", "alive", "indoors", "inside", "pot",
      "potted", "houseplant", "water", "watering", "overwater", "underwater", "feed",
      "feeding", "fertiliser", "fertilizer", "repot", "re-pot", "prune", "winter", "frost",
      "cold", "leaves", "leaf drop", "losing", "dropping", "yellow", "flower", "flowers",
      "fruit", "not fruiting", "no fruit", "best", "buy", "sun", "sunlight", "light",
      "compost", "soil", "sick", "dying")),
    'Lemons want the sunniest place you have - a south-facing windowsill, a conservatory or a '
    'patio against a warm wall - so give them six hours of direct light and turn the pot now and'
    'then so the whole plant grows evenly. Use a free-draining compost with a handful of grit or'
    'perlite, water when the top two or three centimetres of compost feels dry and far less in'
    'winter, and never stand it in a full saucer, because a potted lemon dies of soggy roots far'
    'more often than of thirst. Feed a citrus feed from March to September and nothing over the'
    'winter. Bring it indoors before the first frost, since it drops its leaves below about 5C,'
    'and prune lightly in spring once the fruit has set, because it flowers on new growth. A'
    'flower that opens indoors with no bees about wants a soft brush going over it by hand to'
    'set the fruit.',
    avoid=("recipe", "recipes", "juice", "juiced", "zest", "squeeze", "lemonade", "drizzle",
           "cake", "cakes", "curd", "marmalade", "how much", "price", "cost", "buy a lemon",
           "lemons cost", "bay leaf", "bay leaves", "olive oil", "tree surgeon")))

ENTRIES.append(entry(
    "season-firewood",
    (("firewood", "fire wood", "logs", "log pile", "logs pile", "wood pile", "woodpile",
      "rounds", "log", "wood", "hardwood", "softwood"),
     ("season", "seasoning", "seasoned", "when", "best time", "what time of year", "how long",
      "ready to burn", "dry out", "drying", "leave it", "how many months")),
    "Split it in late winter or early spring, before the sap rises: a log cut then has the whole "
    "summer of sun and wind to dry and is ready for the fire by the autumn. Hardwood such as oak, "
    "ash and beech wants about twelve months and softwood about six to nine, and a split log dries "
    "roughly four times faster than a whole round - which is the reason to split everything now "
    "and stack it, rather than leave the rounds in a heap until you need them.",
    avoid=("cost", "price", "cheap", "how much is", "stove", "burner", "best wood", "what wood",
           "nail", "nails", "nailed", "nailing", "pilot hole", "joist", "joists", "plank",
           "skirting", "floorboard", "floorboards",
           "which wood", "chainsaw", "axe", "hire", "kiln", "kiln dried", "delivered",
           "seasoning of a pan", "cast iron", "frying pan",
           "stain", "stains", "staining", "stained", "varnish", "varnishing", "varnished",
           "paint", "painting", "painted", "coats", "coat", "between coats")))

ENTRIES.append(entry(
    "wood-dry-enough",
    (("seasoned", "dry enough", "moisture", "wet wood", "damp wood", "green wood", "my wood",
      "the wood", "logs", "these logs", "firewood"),
     ("how do i know", "how can i tell", "is my", "are my", "ready", "dry", "wet", "damp",
      "meter", "moisture", "smoke", "smokes", "smoky", "smoking", "spitting", "hiss",
      "sizzle", "steam", "burn", "burning")),
    "Knock two split pieces together: well seasoned wood cracks like a bat on a ball, and green "
    "wood thuds. The ends of a dry log are pale, cracked and often dark-ringed, and a cheap "
    "moisture meter pushed into a freshly split face should read under 20 per cent. Burning wet "
    "wood is why a fire smokes, spits and blacks the glass, and it gives around half the heat, "
    "because most of the flame's energy goes on boiling the water out of the log instead of "
    "heating the room.",
    avoid=("store", "stack", "cover", "shed", "pallet", "buy", "price", "cost", "best wood",
           "which wood", "stove", "burner", "chimney", "flue")))

ENTRIES.append(entry(
    "store-firewood",
    (("firewood", "logs", "log pile", "wood pile", "woodpile", "kindling", "logs pile"),
     ("store", "storing", "stack", "stacking", "cover", "covered", "tarpaulin", "shed",
      "rain", "wet", "outside", "against the house", "keep dry", "how do i keep")),
    "Stack it off the ground on pallets or two rails, in a spot that gets sun and wind, and cover "
    "the top only - a tarpaulin over the whole pile holds the damp in and turns a drying pile into "
    "a rotting one. Keep it a wall's width away from the house so it is not a ladder for mice, and "
    "leave air gaps between the stacks rather than one solid wall of wood.",
    avoid=("cost", "price", "buy", "best wood", "which wood", "stove", "burner", "chimney",
           "season", "how long to dry", "dry enough", "moisture")))

ENTRIES.append(entry(
    "wood-for-a-burner",
    (("wood", "logs", "firewood", "timber", "log burner", "wood burner", "stove", "open fire"),
     ("best", "which", "what kind", "what sort", "what type", "should i burn", "good to burn",
      "safe to burn", "worth burning", "buy", "cheapest")),
    "Ash, oak, beech, hawthorn, hornbeam and birch are the best firewood: dense, slow burning, low "
    "in tar, and ash burns well even when it is not fully dry. Pine and other softwoods burn hot "
    "and fast and leave creosote in the flue, so they are for kindling rather than a night's burn, "
    "and never burn painted or treated timber, plywood, chipboard or driftwood - the fumes are "
    "poisonous and the salt and preservative wreck the flue.",
    avoid=("light", "lighting", "hard to light", "going out", "store", "stack", "season",
           "dry enough", "moisture", "price", "cost per", "chimney", "flue liner", "install")))

ENTRIES.append(entry(
    "sweep-the-chimney",
    (("chimney", "flue", "sweep", "sweeping", "soot", "creosote", "tar", "bird nest"),
     ("how often", "when", "how do i", "should i", "need", "worth", "cost", "price",
      "sweep", "swept", "clean", "cleaning", "blocked", "soot")),
    "Have the chimney swept once a year, before the heating season starts, and twice if it is your "
    "main heat or you burn wood - soot and creosote build up out of sight, and a blocked flue is "
    "how carbon monoxide gets into a room. A sweep costs about 40 to 80 pounds and gives you a "
    "certificate to keep for the insurance; while he is there, ask him to check the cowl and put a "
    "carbon monoxide alarm in the same room as the fire.",
    avoid=("how do i build", "chimney pot", "repoint", "render", "brick", "damp", "smoke test",
           "how do i stop it smoking", "fireplace", "install", "liner", "cost of a new")))

ENTRIES.append(entry(
    "light-the-fire",
    (("wood burner", "log burner", "woodburner", "stove", "open fire", "fireplace", "fire",
      "kindling"),
     ("light", "lighting", "lit", "light it", "keeps going out", "goes out", "wont stay in",
      "won't stay in", "hard to light", "struggle", "struggling", "smokes", "smoky")),
    "Lay it top-down: three or four split logs on the grate, a handful of kindling crossed on top, "
    "two firelighters, then light the kindling and leave the air control wide open for ten minutes "
    "before you close it down. A fire that will not catch is nearly always damp wood, kindling "
    "that is too big, or the air shut too early - small dry wood first, bigger on top, and heat "
    "the flue before you expect a flame.",
    avoid=("electrical fire", "chip pan", "house fire", "fire alarm", "smoke alarm", "firework",
           "wildfire", "campfire", "bonfire", "gas fire", "fire pit", "how do i put out",
           "extinguisher", "safety", "log burner cost", "install")))

ENTRIES.append(entry(
    "sharpen-an-axe",
    (("axe", "hatchet", "axe head", "splitting axe", "felling axe", "billhook"),
     ("sharpen", "sharpening", "sharpen it", "sharp", "blunt", "file", "filing", "hone",
      "grind", "grinding", "edge", "maintain")),
    "Clamp the head in a vice or hold the axe steady on a block and push a file away from the edge "
    "along the bevel, at the angle the bevel already has, until you feel a burr on the far side - "
    "then take two or three light strokes on that side to take it off. A file costs a few pounds "
    "and does less damage than a bench grinder, which heats the edge and takes the temper out of "
    "it; an axe only needs sharp enough to bite, not shaving sharp.",
    avoid=("chainsaw", "lawnmower", "mower blade", "secateurs", "shears", "knife", "chisel",
           "buy", "price", "cost", "which axe", "best axe", "handle", "rehandle")))

_WOOD_WORDS = re.compile(
    r"\b(?:logs?|timber|firewood|wood|wooden|piece of wood|log pile|posts?|stumps?|branches?|"
    r"branch|trunks?|rings?|chopping block)\b")
_SPLITTING = re.compile(
    r"\b(?:splits?|splitting|chopp?ing|chop|wedges?|maul|axe|axes|hatchet|stuck|log splitter|"
    r"sawing|saw)")


_RING_IS_NOT_WOOD = re.compile(
    r"\b(?:hob|hobs|cooker|cookers|stove|stoves|oven|ovens|burner|burners|element|elements"
    r"|ring main|wedding|engagement|wedding band|finger|fingers|jeweller|jewellery|jewelry"
    r"|gold|silver|diamond|tarnish|tarnished|worktop|worktops|counter|coffee table|cup|glass"
    r"|mug)\b")
_OTHER_WOOD = re.compile(
    r"\b(?:logs?|timber|firewood|wood|wooden|piece of wood|log pile|posts?|stumps?|branches?"
    r"|branch|trunks?|chopping block)\b")


def _splitting_a_log(understood):
    said = " ".join(str((understood or {}).get(key) or "")
                    for key in ("clean", "norm_text", "text")).lower()
    if re.search(r"\brings?\b", said) and not _OTHER_WOOD.search(said) \
            and _RING_IS_NOT_WOOD.search(said):
        return False
    if _WOOD_WORDS.search(said):
        return True
    return bool(_SPLITTING.search(said) and re.search(r"\brounds?\b", said))


ENTRIES.append(entry(
    "split-a-log",
    (("log", "logs", "log round", "log rounds", "rounds of wood", "logs i have",
      "piece of wood", "log pile", "firewood"),
     ("split", "splitting", "chop", "chopping", "wedge", "maul", "axe", "how do i", "how to",
      "best way", "how can i", "without an axe", "stuck", "wont split", "won't split",
      "hard to split", "easier to split", "log splitter")),
    "Stand the round on a chopping block - a big flat stump - and bring the axe down through the "
    "middle, not at the edge: the ground swallows the force of a blow and the block gives it back. "
    "Knotty or wide rounds go with two steel wedges tapped in along the end grain, and a stubborn "
    "one is easier after a few weeks of drying. No axe at all means a wedge and a club hammer, or "
    "drill a line of holes down the face and hit the wood with a mallet.",
    avoid=("cost", "price", "buy", "which axe", "best axe", "sharpen", "handle", "season",
           "how long to dry", "store", "stack", "firewood for sale", "chainsaw", "stump",
           "phone", "phones", "mobile", "mobiles", "ringtone", "ringtones", "voicemail",
           "landline", "missed call", "missed calls", "doorbell", "door bell", "at night",
"piercing", "piercings", "nose ring", "nose stud", "septum", "earring", "ear ring",
           "belly bar", "hoop earring", "tragus", "helix")
    + RING_AS_A_CALL,
    guard=_splitting_a_log))

ENTRIES.append(entry(
    "chimney-smokes",
    (("chimney", "flue", "open fire", "wood burner", "log burner", "stove", "fireplace",
      "the fire"),
     ("smokes", "smoking", "smoke comes", "smoke coming", "blows back", "blowing back",
      "back into the room", "in the room", "downdraught", "down draught", "draught",
      "wont draw", "won't draw", "not drawing", "drawing")),
    "Smoke into the room is a cold flue, a blocked one or a pressure problem at the top: hold a "
    "rolled-up newspaper torch at the opening for a minute to warm the flue before you light it, "
    "and open a window a crack. If it still smokes once the fire is going, stop using it and get "
    "the sweep out, because a blocked or cracked flue lets carbon monoxide into the room. Smoke "
    "only when it is windy means the chimney needs a cowl, and smoke in a sealed room with an "
    "extractor fan running means it needs an air vent.",
    avoid=("how do i build", "chimney pot", "repoint", "render", "brick", "damp", "install",
           "liner", "sweep", "how often", "cost", "price", "santa")))

_GREENHOUSE = ("greenhouse", "green house", "glasshouse", "polytunnel", "polytunnel")
_GREENHOUSE_ASK = ("temperature", "temperatures", "how warm", "how hot", "how cold", "warm",
                   "warmth", "heat", "heated", "heater", "heating", "degrees", "too hot",
                   "too cold", "vent", "vents", "venting", "ventilation", "frost", "frosts",
                   "freezing", "insulate", "bubble wrap", "minimum")

ENTRIES.append(entry(
    "greenhouse-temperature",
    (_GREENHOUSE, _GREENHOUSE_ASK),
    ("Aim for 15 to 25C by day: open the vents and the door at about 25C, and shut them again "
     "mid-afternoon so the heat is kept for the night, because a closed greenhouse is 5 to 10C "
     "warmer than the air outside. Tomatoes, cucumbers and peppers stop growing below about 12C "
     "and set no fruit below 15C, so a heater set to 10 to 12C keeps them alive rather than "
     "growing, and a max-min thermometer in the shade inside tells you what your own greenhouse "
     "is really doing."),
    bias=1,
    avoid=("water", "watering", "how often", "feed", "feeding", "fertiliser", "fertilizer",
           "whitefly", "aphid", "aphids", "red spider", "mould", "mouldy", "damping off",
           "clean", "cleaning", "wash", "glass", "pane", "panes", "broken", "repair", "paint",
           "lean-to", "conservatory", "windowsill", "houseplant", "houseplants", "recipe",
           "bake", "oven", "cook", "cooking", "grow", "growing", "sow", "sowing", "plant",
           "planting", "what can i grow")))
ENTRIES.append(entry(
    "ivy-taking-over",
    (("ivy", "english ivy", "common ivy", "climbing ivy", "ivy plant"),
     GONE_WILD + ("wall", "walls", "fence", "fences", "tree", "trees", "shed", "garage",
                  "house", "brick", "render", "gutter", "gutters", "roof", "window",
                  "windows", "get rid", "rid of", "control", "kill", "remove", "stop",
                  "growing", "spreading", "damage", "damaging", "mortar", "dangerous",
                  "pull it down", "pull down", "cut back")),
    "Ivy is cut off rather than pruned: saw through every stem where it meets the ground, leave "
    "the top to die back for a few weeks, then pull it off - pulling live ivy takes render and "
    "mortar with it. It comes back from any root left in the soil, so dig the stump out and pull "
    "up the new shoots. On a wall you want to keep it on, hold it back 30cm from the gutters, "
    "windows and the roofline, and it does the brick no harm at all.",
    avoid=("devil's ivy", "devils ivy", "devil ivy", "pothos", "houseplant", "houseplants",
           "house plant", "indoor", "pot", "pots", "windowsill", "poison ivy", "rash",
           "itchy", "ivy league", "ivy bridge", "my mate ivy", "called ivy"),
    bias=1))
ENTRIES.append(entry(
    "brambles-taking-over",
    (("bramble", "brambles", "blackberry bush", "blackberry patch", "blackberries growing",
      "thorny"),
     GONE_WILD + ("garden", "border", "bed", "beds", "fence", "hedge", "plot", "allotment",
                  "lawn", "back", "get rid", "rid of", "control", "kill", "remove", "clear",
                  "dig out", "dig up", "cut back", "cutting", "spread", "spreading")),
    "Brambles come back from the crown and from any tip that roots where it touches the soil, so "
    "cutting the tops only makes them shrubby. Cut the stems to the ground, dig the crown out "
    "with a fork and pull up the tips that have rooted further out, and do it before they flower "
    "so nothing seeds. Then keep cutting the regrowth every few weeks through the season: a "
    "bramble starved of leaves runs out of root by the second year.",
    avoid=("blackberry phone", "blackberry key", "phone", "iphone", "android", "sim",
           "picking blackberries", "bramble jelly", "bramble jam", "crumble", "recipe",
           "cook", "eat", "fruit"),
    bias=1))

_FROST_ALREADY = (
    "froze", "frozen", "frosted", "frostbitten", "frost bitten", "blackened", "black leaves",
    "burnt by the frost", "burnt by frost", "burnt by the cold", "hit by the frost",
    "hit by frost", "caught by the frost", "caught by frost", "the frost damaged",
    "frost damage to my", "any frost damage", "much frost damage",
    "damaged by the frost", "damaged by frost", "killed by the frost", "killed by frost",
    "frost has", "frost got", "frost got at", "got frosted", "got frost",
    "the frost took", "lost to the frost", "after the frost", "from the frost", "by the frost",
    "frost last night", "frost overnight", "the frost got", "died in the frost",
    "died back in the frost", "were in the frost", "was in the frost", "left in the frost",
    "left them in the frost", "sat in the frost", "stood in the frost",
)
_FROST_AFTERMATH = (
    "plant", "plants", "leaves", "leaf", "stem", "stems", "shoot", "shoots", "growth",
    "bud", "buds", "seedling", "seedlings", "flowers", "flower", "tomato", "tomatoes",
    "courgette", "courgettes", "potato", "potatoes", "beans", "bean", "basil", "herbs",
    "mint", "rosemary", "geraniums", "dahlias", "bedding", "shrubs", "shrub", "tree",
    "citrus", "olive", "banana plant", "tree fern", "succulents", "cacti", "garden",
    "my garden", "the garden", "allotment", "veg", "vegetables", "crop", "crops",
    "recover", "recovery", "survive", "come back", "come round", "dead", "died", "dying",
    "cut back", "cut it back", "prune", "pruning", "trim", "limp", "wilted", "drooping",
    "what now", "now what", "will it", "will they", "should i",
)
_FROST_AFTER_THE_FACT = (
    "Nothing today: leave the blackened leaves and soft stems alone, because a plant that looks "
    "dead after a frost often has live buds further down and cutting now tells you nothing. "
    "Give it about a fortnight, then scratch the stem or the bark with a fingernail - green "
    "underneath means it is alive and can be cut back to just above a live shoot, brown and dry "
    "means that part has gone. Water it, keep it out of the next cold night, and don't feed or "
    "repot something that is still in shock; new growth is the sign it is worth keeping."
)


def _the_frost_already_bit_something(understood):
    said = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    said = said.replace("\u2019", "'")
    return _says_one_of(said, _FROST_ALREADY) and _says_one_of(said, _FROST_AFTERMATH)


ENTRIES.append(entry(
    "frost-damage-already",
    (_FROST_ALREADY, _FROST_AFTERMATH),
    _FROST_AFTER_THE_FACT,
    avoid=("freezer", "frozen peas", "frozen veg", "frozen vegetables", "fridge", "thaw",
           "defrost", "refreeze", "open bag", "packet", "windscreen", "car", "cars", "pond",
           "fish", "beer", "glass",
           "freeze tomatoes", "freeze the", "can i freeze", "how do i freeze",
           "protect", "protecting", "cover", "covering", "fleece", "cloche", "bring them in",
           "bring it in", "keep them warm", "forecast", "tonight", "tomorrow night",
           "safe to eat", "can i eat", "is it safe", "still eat", "eat them", "eat it"),
    bias=2,
    guard=_the_frost_already_bit_something))


ENTRIES.append(entry(
    "garden-looks-tired",
    (("garden", "gardens", "back garden", "front garden", "borders", "flowerbeds", "plot",
      "yard", "outdoor space"),
     ("look better", "looks better", "look nicer", "look nice", "look good", "looks good",
      "improve it", "improve my", "improve the", "make it nicer", "make it look", "ideas",
      "what should i do", "cheap", "without spending", "pride")),
    "Tidy the outline first, because a garden reads as untidy at its edges before its middle: "
    "cut the lawn edge right round with a half-moon edger, clear the path, and weed the first "
    "foot of border. Then buy three plants and no more - something tall, something scented by "
    "the door, and something that flowers for months - in pots if the soil is poor. Bark or "
    "gravel over bare soil is the cheapest thing that makes a garden look finished.",
    ask=("look", "looks", "idea", "ideas", "what", "how", "where", "tidy", "improve", "make",
         "cheap", "start", "nice", "better"),
    guard=_names_the_garden,
    avoid=("weed", "weeds", "weeding", "dandelion", "nettle", "nettles", "bindweed", "moss",
           "lawn", "mow", "mowing", "mower", "turf", "grass seed", "re-seed", "scarify",
           "scarifying", "aerating", "frost", "frosts", "frozen", "cold snap", "winter",
           "snow", "pond", "fish", "fence", "fencing", "shed", "decking", "patio",
           "paving", "drive", "driveway", "raised bed", "greenhouse", "polytunnel",
           "slugs", "snails", "foxes", "fox", "rats", "squirrel", "deer", "cat", "cats", "dog",
           "dogs", "hire", "gardener", "how much", "cost", "price", "quote", "landscaper",
           "allotment", "allotments",
           "plant", "plants", "planting", "flower", "flowers", "shrub", "shrubs", "bulb",
           "bulbs", "hanging basket", "window box", "no garden", "without a garden",
           "flat", "balcony", "indoors", "inside the house",
           "hurts", "hurt", "aching", "ache", "aches", "pain", "painful", "sore", "back",
           "knees", "knee", "shoulder", "shoulders", "wrist", "sprain", "strain", "injury",
           "mess", "messy", "overgrown", "neglected", "jungle", "where do i start",
           "where to start", "how do i start", "get started", "tidy up", "tidy", "sort out",
           "clear",
           "sow", "sowing", "seed", "seeds", "plant out", "prune", "pruning", "cut back",
           "hedge", "hedges", "trim", "climbing", "climber", "vegetable", "veg", "potato",
           "tomato", "tomatoes", "grow", "growing", "compost", "bark", "mulch", "when should"))
)


ENTRIES.append(
    entry("plant-for-a-windowless-room",
          (("plant", "plants", "houseplant", "houseplants", "house plant", "house plants",
            "pot plant", "pot plants", "pothos", "fern", "ferns", "orchid", "orchids", "palm",
            "snake plant", "zz plant", "peace lily", "spider plant", "green"),
           ("bathroom", "bathrooms", "loo", "toilet", "en suite", "ensuite", "shower room",
            "hallway", "hall", "landing", "cellar", "basement", "cupboard", "shelf", "shelves",
            "no window", "no windows", "windowless", "without a window", "no natural light",
            "no light", "dark room", "dark corner", "dark hallway", "window in there")),
          "For a room with no window, take the plants that cope with low light: pothos, snake "
          "plant, ZZ plant, peace lily and spider plant will all hold on, and a bathroom's steam "
          "suits a fern. Everything slows down in the dark, so water far less than the label says "
          "- every two to three weeks, once the top of the compost is dry - or the roots rot. If "
          "there is no daylight at all, no plant will live there: a lamp left on for twelve hours "
          "is what keeps one going, and a good fake is the honest answer for a cellar.",
          ask=("bathroom", "loo", "toilet", "ensuite", "en suite", "shower room", "hallway",
               "hall", "landing", "cellar", "basement", "cupboard", "shelf", "shelves",
               "window", "windowless", "room", "corner", "flat", "house", "home"),
          avoid=("tomato", "tomatoes", "basil", "lawn", "grass", "tree", "trees", "rose", "roses",
                 "cucumber", "courgette", "pepper", "chilli", "outside", "garden", "gardens",
                 "border", "flowerbed", "flower bed", "allotment", "outdoor", "outdoors",
                 "shrub", "shrubs", "hedge", "hanging basket", "veg patch", "vegetable patch",
                 "yellow", "brown tips", "drooping", "wilted", "repot", "repotting",
                 "overwater", "overwatering", "root rot", "fungus gnat", "gnats",
                 "smell", "smells", "smelly", "damp", "mould", "mold", "condensation", "extractor",
                 "lamp", "ceiling light", "light bulb", "headlight", "grow light"),
          bias=2))
