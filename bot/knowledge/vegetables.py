
import re

from .lookup import entry, tokens

ANSWERS = ("cooking", "food-and-drink")


def _phrase_in(text, phrase):
    return bool(re.search(r"(?<![a-z])" + re.escape(phrase) + r"(?![a-z])", text))


VEG_TIME = (
    (("cauliflower",),
     "6 to 8 minutes for florets in already boiling salted water, 12 to 15 for a whole small "
     "one, and it is done when a knife goes into the stalk with no resistance. Steamed, give it "
     "2 or 3 minutes more."),
    (("carrot",),
     "10 to 15 minutes for thick coins, 8 for thin ones, 20 for whole carrots, in already "
     "boiling salted water. They are done when a knife slides in easily - a little bite is "
     "better than soft, and they go on cooking once drained."),
    (("cabbage",),
     "5 to 8 minutes for shredded cabbage in already boiling salted water, and less for the "
     "loose outer leaves. It is done when it has wilted and lost its raw edge but still has "
     "some bite; overcook it and it turns sweet and grey."),
    (("swede",),
     "25 to 30 minutes in 3cm chunks in boiling salted water, or 40 to 50 minutes whole. The "
     "knife test is the one that counts: it should go in with no resistance at all, because "
     "slightly underdone swede is hard and watery."),
    (("leek",),
     "6 to 8 minutes in thick rings, 3 to 4 if you slice them thin, in boiling salted water. "
     "Rinse the grit out from between the layers first - leeks hold soil better than any other "
     "vegetable - and stop while they still hold their shape."),
    (("courgette",),
     "3 to 4 minutes in boiling salted water, and no more: it is mostly water, so it goes from "
     "just right to mush fast. Better still, fry thick slices in a little oil for the same time "
     "- boiled courgette tastes of very little."),
    (("asparagus",),
     "3 to 5 minutes depending on thickness, standing up in a pan with the tips out of the "
     "water if you can, or in a wide pan. It is done when a knife goes into the stalk - bend one "
     "and it should still have some spring."),
    (("globe artichoke", "globe artichokes", "artichoke", "artichokes"),
     "25 to 35 minutes whole in already boiling salted water, standing up in a deep pan with the "
     "tips out of the water if they fit. It is done when a leaf near the middle pulls away "
     "easily; drain it upside down so the water runs out of the leaves."),
    (("jerusalem artichoke", "jerusalem artichokes", "sunchoke", "sunchokes"),
     "10 to 12 minutes in already boiling salted water, scrubbed and cut into even pieces, and it "
     "is done when a knife goes in with no resistance at all. Roasting suits it better than "
     "boiling - 25 to 30 minutes at 200C (180C fan) - because it goes sweet and nutty at the "
     "edges."),
    (("sweetcorn", "corn on the cob", "corn cob"),
     "5 to 8 minutes for a cob in boiling unsalted water (salt makes the kernels tough), 4 to 5 "
     "from frozen. It is done when the kernels are bright yellow and a sharp knife cuts one "
     "easily."),
    (("spinach",),
     "1 to 2 minutes, and that is generous: put it in boiling water, push it under, and take it "
     "out as soon as it has wilted. Spinach is nearly all water, so longer only means losing "
     "it - squeeze it out and season it after."),
    (("kale",),
     "3 to 5 minutes in boiling salted water, stalky pieces first, and 6 to 8 if you want it "
     "soft enough for a soup. Strip the tough stems out before it goes in, and drain it well - "
     "kale holds a lot of water."),
    (("butternut squash", "squash"),
     "15 to 20 minutes in 3cm chunks in boiling salted water, or 25 to 30 in bigger pieces. It "
     "is done when a knife slides in with no resistance; roast it instead if you want it sweet "
     "and caramelised rather than watery."),
    (("celeriac",),
     "15 to 20 minutes in 2cm chunks in boiling salted water with a squeeze of lemon, which "
     "keeps it pale. It is done when a knife slides in easily, and it makes a good mash with "
     "butter and plenty of pepper."),
    (("mange tout", "mangetout", "sugar snap"),
     "2 to 3 minutes in boiling salted water, then straight into cold water so they stay "
     "bright. They are done when they are hot through and still squeak when you bite one - the "
     "pod is the point."),
    (("french beans", "green beans", "runner beans", "string beans"),
     "4 to 6 minutes for french beans, 5 to 7 for runner beans, in boiling salted water. They "
     "are done when a bean bends without snapping; top and tail them and string the runners "
     "first."),
    (("broad beans", "broad bean", "fava beans"),
     "2 to 3 minutes for small ones and 4 to 5 for big ones, in boiling salted water, then slip "
     "the grey skins off if they are big. They are done when a bean is tender and tastes sweet, "
     "not floury."),
    (("kohlrabi",),
     "12 to 15 minutes in wedges or 20 to 25 whole, peeled, in boiling salted water - it is "
     "done when a knife slides into the middle with no resistance. Steaming takes the same time "
     "and keeps more of the sweetness."),
    (("beetroot",),
     "45 to 60 minutes whole and unpeeled in boiling water, 25 to 30 if you cut it into wedges. "
     "A knife should slide in with no resistance, and the skin rubs off under cold water once "
     "it is cool enough to handle."),
    (("turnip",),
     "15 to 20 minutes in 3cm chunks in boiling salted water, and 25 to 30 whole. It is done "
     "when a knife goes in easily; drain it well, because turnip holds water and a wet mash is "
     "a sad mash."),
    (("fennel",),
     "8 to 10 minutes in wedges in boiling salted water, cut through the root so they hold "
     "together. It is done when a knife goes into the thickest part; boiled fennel goes sweet "
     "and soft, and a squeeze of lemon at the end keeps it fresh."),
    (("pak choi", "pak choy", "bok choy"),
     "2 to 3 minutes, halved lengthways, in boiling salted water - the leaves wilt almost at "
     "once. Better in a hot pan with a little oil, garlic and soy for the same 3 minutes."),
    (("spring greens", "collard", "greens"),
     "4 to 6 minutes shredded in boiling salted water, stalky bits first. They are done when "
     "they are tender but still green; drain them well and dress with butter or a little oil."),
)

VEG_HOW = {
    "carrot": "peel or just scrub them, cut into batons, and boil or steam for 6 to 8 minutes "
              "until a knife goes in easily. Roast batons at 200C (180C fan) for 25 to 30 "
              "minutes with oil and a little honey. Whole small ones take 10 to 12 minutes "
              "boiled, and older carrots are sweeter and take longer.",
    "cabbage": "shred it and cook it briefly, or it goes grey and soft: boil or steam 4 to 5 "
               "minutes, or fry it in butter for 5 to 6 with a splash of water and the lid on "
               "for the first half. Salt at the end. Red cabbage is the exception and wants a "
               "slow braise of 45 minutes or more, with vinegar and something sweet.",
    "spinach": "it needs seconds, not minutes: wash it, put it in a hot pan with a knob of "
               "butter and stir for 1 to 2 minutes until it has just collapsed, then drain off "
               "the water it gives. Boiling it makes it slimy; squeeze it dry and dress it with "
               "butter, nutmeg or a little garlic.",
    "asparagus": "snap off the woody end of each spear (it breaks where it should), then boil "
                 "or steam 3 to 4 minutes for thin spears or 5 to 6 for fat ones, or roast at "
                 "200C (180C fan) for 10 to 12 minutes with oil, salt and lemon. It is done when "
                 "a knife goes in with no crunch left.",
    "leek": "slice it first, then wash it: grit hides between the layers, so swill the slices in "
            "a bowl of water and lift them out. Sweat them in butter with the lid on for 8 to 10 "
            "minutes, stirring now and then, until soft but not browned, and a splash of water "
            "stops them catching. They go sweet, and they are the base of potato and leek soup.",
    "courgette": "slice them about 1cm thick, salt them for 10 minutes and pat them dry if you "
                 "want them firm, then fry in a hot pan for 3 to 4 minutes a side until golden. "
                 "To roast, toss in oil and bake at 200C (180C fan) for 20 minutes. Don't crowd "
                 "the pan: they steam rather than brown.",
    "kale": "strip the leaves off the stalks, then either steam 4 to 5 minutes until tender, or "
            "toss with oil and salt and roast at 180C (160C fan) for 12 to 15 minutes until the "
            "edges crisp. Raw kale is fine in a salad if you massage it with oil and lemon for a "
            "minute first, which softens it.",
    "swede": "peel and cube it, then boil for 20 to 25 minutes until it mashes easily, and mash "
             "it with butter, salt and pepper - a little cream or a knob of butter takes away the "
             "sharpness. It roasts well too, in 2cm cubes at 200C (180C fan) for 30 to 35 "
             "minutes.",
    "globe artichoke": "cut the top inch off, snip the points off the outer leaves, and boil or "
                       "steam 25 to 35 minutes until a leaf near the middle pulls away easily. "
                       "Eat the leaves dipped in butter or vinaigrette, then scrape out the "
                       "fuzzy choke and eat the heart. To roast, halve them, oil the cut sides "
                       "and pack them cut down in a dish at 200C (180C fan) for 25 to 30 "
                       "minutes with a splash of water and a lid for the first half.",
    "jerusalem artichoke": "scrub them instead of peeling, since the skin is thin, and roast "
                           "them 25 to 30 minutes at 200C (180C fan) in oil, or boil 10 to 12 "
                           "minutes and mash them with butter like potato: they go sweet and "
                           "nutty fast, so test early. A squeeze of lemon or a splash of vinegar "
                           "keeps them from discolouring, and start with a small portion, "
                           "because they earn their other name.",
}

VEG_HOW_EXTRA = (
    (("green beans", "runner beans", "french beans", "string beans", "fine beans"),
     "top and tail them, and slice runner beans thinly, then boil or steam 4 to 5 minutes for "
     "green beans or 5 to 7 for runner beans: they should still squeak. Drain them and toss with "
     "butter or a little garlic. Old runner beans have strings and hard seeds, so slice them "
     "fine and cook them a few minutes longer."),
    (("mushroom", "mushrooms", "button mushrooms", "chestnut mushrooms"),
     "get the pan hot and add them dry first for a minute so they give up their water, then add "
     "butter or oil and cook 4 to 5 more minutes until golden. Wipe or rinse them quickly and "
     "dry them - either is fine - and don't crowd the pan or they boil in their own juice. "
     "Season at the end, not the start."),
)

VEG_HOW_ASKS = ("cook", "cooking", "cooked", "prepare", "prep", "prepare", "boil", "boiled",
                "boiling", "steam", "steamed", "steaming", "best way", "method", "properly")

VEG_NAMED_METHOD = ("roast", "roasted", "roasting", "oven", "bake", "baked", "baking", "fry",
                    "fried", "frying", "grill", "grilled", "air fryer", "airfryer",
                    "microwave", "barbecue", "bbq", "slow cooker", "pressure cooker")

VEG_OTHER = (
    "roast", "roasted", "roasting", "oven", "bake", "baked", "baking", "fry", "fried",
    "frying", "grill", "grilled", "air fryer", "microwave", "barbecue", "bbq", "soup",
    "puree", "mash", "fridge", "freezer", "keep", "keeps", "last", "leftovers",
    "leftover", "calories", "calorie", "healthy", "health", "protein", "carb", "carbs",
    "vitamin", "vitamins", "iron", "dog", "dogs", "cat", "cats", "rabbit", "plant",
    "plants", "planting", "grow", "growing", "garden", "allotment", "seed", "seeds",
    "buy", "buying", "cost", "price", "cheap", "shop", "supermarket", "market",
    "recipe", "allergy", "allergic", "baby", "weaning", "blw", "diet", "diabetes",
    "sugar", "barely", "raw", "purple", "yellow", "brown", "mouldy", "gone off",
    "gone soft", "went soft", "gone limp", "limp", "bendy", "rubbery", "sprouting",
    "sprouted", "wilted", "wilt", "slimy",
    "spaghetti squash", "acorn squash", "pattypan",
)

VEG_TIME_WORDS = ("how long", "long", "minutes", "mins", "minute", "time", "times", "hour",
                  "hours", "tender", "done", "ready", "take", "takes", "need", "needs")

VEG_NOT_FOR_US = (
    "fridge", "keep", "keeps", "keeping", "last", "lasts",
    "leftovers", "leftover", "calories", "calorie", "healthy", "health", "protein", "carb",
    "carbs", "vitamin", "vitamins", "iron", "dog", "dogs", "cat", "cats", "rabbit", "plant",
    "plants", "planting", "grow", "growing", "garden", "allotment", "seed", "seeds", "buy",
    "buying", "bought", "cost", "price", "cheap", "shop", "supermarket", "market", "allergy",
    "allergic", "baby", "weaning", "diet", "diabetes", "sugar", "mouldy", "gone off",
    "gone soft", "went soft", "gone limp", "limp", "bendy", "rubbery", "wilted", "wilting",
    "slimy",
    "are sprouting", "is sprouting", "have sprouted", "has sprouted", "gone to seed",
    "harvest", "harvesting", "pick", "picking", "picked", "ripe", "ripen", "ripened",
    "when are", "are my", "are they ready", "ready to pick",
    "soak", "soaks", "soaking", "soaked", "overnight", "dried", "dry",
    "dont like", "don't like", "do not like", "doesnt like", "doesn't like",
    "do not like them", "do not like it", "does not like them", "hate", "hates", "hated",
    "cant stand", "can't stand", "not a fan", "fussy",
    "wont eat", "won't eat", "will not eat", "wont touch", "won't touch",
)

VEG_ASK_BETWEEN = ("how", "long", "time", "times", "minutes", "mins", "take", "takes")

VEG_FILLER = ("take", "takes", "took", "to", "for", "in", "on", "the", "a", "an", "oven",
              "when", "at", "should", "i", "you", "do", "need", "long", "how")
VEG_COOK = ("boil", "boiled", "boiling", "steam", "steamed", "steaming", "cook", "cooked",
            "cooking", "fry", "fried", "frying", "grill", "grilled", "simmer", "simmered")


def _takes_to(words, position, spot):
    between = words[position + 1:spot]
    if not between or not all(word in VEG_FILLER for word in between):
        return False
    if any(word in VEG_COOK for word in between):
        return False
    return any(word in ("take", "takes", "took") for word in between)


VEG_ASKS = ("boil", "boiled", "boiling", "steam", "steamed", "steaming", "cook",
            "cooked", "cooking", "how long", "long", "time", "times", "minutes",
            "mins", "tender", "done", "ready", "take",
            "prepare", "prep", "best way", "method", "properly")

def _near(text, phrase):
    wanted = str(phrase).lower()
    for index, word in enumerate(str(text).lower().replace("'", " ").split()):
        if word == wanted or word == wanted + "s" or word + "s" == wanted:
            return index
    return None


def _a_word(text, word):
    have = tokens(text)
    if not have:
        return False
    for one in have:
        if one == word or one == word + "s" or one + "s" == word:
            return True
        if one.endswith("es") and one[:-2] == word:
            return True
    return False


def _name_in(text, name):
    wanted = tokens(name)
    have = tokens(text)
    if not wanted or not have:
        return False
    last = len(wanted) - 1
    for i in range(len(have) - len(wanted) + 1):
        run = have[i:i + len(wanted)]
        if run[:last] == wanted[:last] and _a_word(" ".join(run[last:]), wanted[last]):
            return True
    return False


RULE_OUT = ("no", "not", "without", "dont", "don't", "doesnt", "doesn't", "didnt", "didn't",
            "hate", "hates", "hated", "dislike", "dislikes", "allergic", "intolerant",
            "avoid", "avoids", "avoiding", "free", "off", "skip", "skipping", "except")
_RULE_OUT_REACH = 4


def _ruled_out(text, names):
    words = str(text or "").lower().replace("'", " ").split()
    if not words:
        return False
    for name in names:
        wanted = str(name).lower().replace("'", " ").split()
        if not wanted:
            continue
        for start in range(len(words) - len(wanted) + 1):
            run = words[start:start + len(wanted)]
            if run[:-1] != wanted[:-1] and run != wanted:
                continue
            if not _a_word(" ".join(run[-1:]), wanted[-1]):
                continue
            before = words[max(0, start - _RULE_OUT_REACH):start]
            if any(word in RULE_OUT for word in before):
                return True
    return False


def _typed_line(memory, understood):
    if isinstance(memory, dict):
        now = memory.get("understood")
        if isinstance(now, dict) and now.get("text"):
            return now["text"]
    if isinstance(understood, dict):
        return understood.get("text") or ""
    return ""


def _reply_for(names, said, how=None):
    def answer(memory, understood):
        text = _typed_line(memory, understood)
        if not text:
            return None
        if not any(_a_word(text, word) for word in VEG_ASKS):
            return None
        if _ruled_out(text, names):
            return None
        how_asked = (how is not None
                     and any(_a_word(text, word) for word in VEG_HOW_ASKS)
                     and not any(_phrase_in(text, word) for word in VEG_TIME_WORDS)
                     and not any(_a_word(text, word) for word in VEG_NAMED_METHOD))
        if not how_asked and not any(_phrase_in(text, word) for word in VEG_TIME_WORDS):
            return None
        if any(_a_word(text, word) for word in ("freezer", "freeze", "freezing")) and not \
                any(_a_word(text, word) for word in ("boil", "boiling", "steam", "steaming",
                                                     "cook", "cooking", "blanch")):
            return None
        where = None
        for name in sorted(names, key=len, reverse=True):
            if _name_in(text, name):
                where = name
                break
        if where is None:
            return None
        if any(_phrase_in(text, phrase) for phrase in ("in the oven", "in an oven",
                                                       "in my oven", "in the air fryer", "in a hot oven")):
            return None
        position = _near(text, where.split()[-1])
        words = str(text).lower().replace("'", " ").split()
        for word in VEG_OTHER:
            if not _phrase_in(text, word):
                continue
            if where in word.split():
                return None
            spot = _near(text, word)
            if position is None or spot is None:
                continue
            if spot < position:
                between = words[spot + 1:position]
                if not any(ask in between for ask in VEG_ASK_BETWEEN):
                    return None
            elif spot > position and _takes_to(words, position, spot):
                return None
            elif spot - position <= 2:
                return None
        head = where[0].upper() + where[1:]
        if how_asked:
            if _a_word(text, "frozen"):
                return (head + ", from frozen: straight into already boiling water and take 2 "
                        "minutes off - " + how)
            return head + ": " + how
        if not said:
            return head + ": " + how
        if _a_word(text, "frozen"):
            return (head + ", from frozen: go straight into already boiling water and take 2 "
                    "minutes off - " + said)
        return head + ": " + said
    return answer


ROAST_MINUTES = {
    "carrot": ("25 to 30", "halved lengthways or cut into batons"),
    "parsnip": ("30 to 35", "cut into wedges, and they want a little honey or sugar to brown"),
    "leek": ("25 to 30", "halved lengthways and laid cut side down"),
    "cabbage": ("25 to 30", "cut into wedges through the core so they hold together"),
    "sprouts": ("25 to 30", "halved and laid cut side down"),
    "brussels sprouts": ("25 to 30", "halved and laid cut side down"),
    "green beans": ("12 to 15", "kept whole"),
    "french beans": ("12 to 15", "kept whole"),
    "runner beans": ("12 to 15", "kept whole"),
    "broccoli": ("15 to 18", "cut into florets with the stalk split"),
    "courgette": ("18 to 20", "halved lengthways"),
    "onion": ("30 to 35", "cut into wedges through the root"),
    "beetroot": ("50 to 60", "left whole and unpeeled in foil"),
    "swede": ("35 to 40", "cut into 3cm chunks"),
    "squash": ("30 to 35", "cut into 3cm chunks"),
    "butternut squash": ("30 to 35", "cut into 3cm chunks"),
    "pepper": ("20 to 25", "cut into thick strips"),
    "peppers": ("20 to 25", "cut into thick strips"),
    "fennel": ("25 to 30", "cut into wedges through the root"),
    "kohlrabi": ("30 to 35", "cut into wedges"),
    "turnip": ("30 to 35", "cut into 3cm chunks"),
    "celeriac": ("30 to 35", "cut into 3cm chunks"),
    "artichoke": ("25 to 30", "halved, oiled on the cut side and packed cut down in a dish"),
    "globe artichoke": ("25 to 30", "halved, oiled on the cut side and packed cut down in a dish"),
    "jerusalem artichoke": ("25 to 30", "scrubbed, halved if large, in a single layer"),
    "jerusalem artichokes": ("25 to 30", "scrubbed, halved if large, in a single layer"),
    "kale": ("10 to 12", "torn off the stalk and tossed in oil, for the crispness rather than a side"),
    "aubergine": ("25 to 30", "cut into 3cm chunks"),
    "tomato": ("15 to 20", "halved, cut side up"),
    "red onion": ("30 to 35", "cut into wedges through the root"),
    "mushroom": ("15 to 20", "left whole if small and halved if large, with room between them "
                             "because crowded mushrooms steam instead of browning"),
    "mushrooms": ("15 to 20", "left whole if small and halved if large, with room between them "
                              "because crowded mushrooms steam instead of browning"),
    "asparagus": ("10 to 12", "kept whole; they brown rather than bend"),
    "sweetcorn": ("25 to 30", "cobs turned once half way; loose kernels take 12 to 15"),
    "corn on the cob": ("25 to 30", "cobs turned once half way; loose kernels take 12 to 15"),
    "shallots": ("25 to 30", "left whole and unpeeled, or halved through the root"),
    "garlic": ("25 to 30", "a whole head with the top sliced off and wrapped in foil, then "
                           "squeezed out of its skins"),
    "radish": ("15 to 20", "halved - the heat goes and they come out sweet and mild"),
    "romanesco": ("20 to 25", "cut into florets like a cauliflower, and quicker because the "
                              "florets are smaller"),
    "spring onion": ("8 to 10", "kept whole; they scorch at the tips before the middle softens"),
    "spring onions": ("8 to 10", "kept whole; they scorch at the tips before the middle softens"),
    "pak choi": ("8 to 10", "halved lengthways and laid cut side down"),
    "tenderstem broccoli": ("12 to 15", "kept whole, stalks and all"),
    "chicory": ("20 to 25", "halved through the root so the leaves hold together"),
    "okra": ("12 to 15", "left whole with the tops trimmed, and dry so it does not go slimy"),
    "mangetout": ("8 to 10", "kept whole and turned once; they are done when the pods blister"),
}

ROAST_WORDS = ("roast", "roasted", "roasting", "roasts", "oven", "baked", "baking", "bake",
               "air fryer", "in the oven", "in an oven", "in my oven", "tray bake")

ROAST_NOT_FOR_US = ("boil", "boiled", "boiling", "steam", "steamed", "steaming", "parboil",
                    "parboiled", "blanch", "blanched", "microwave", "fry", "fried", "frying",
                    "grill", "grilled", "soup", "mash", "puree", "fridge", "freezer", "freeze",
                    "keep", "keeps", "last", "calories", "plant", "plants", "grow", "growing",
                    "dog", "dogs", "cat", "cats", "buy", "cost", "price", "cheap", "shop",
                    "gone soft", "gone limp", "mouldy", "slimy", "wilted", "sprouting")


def _roast_reply(memory, understood):
    text = _typed_line(memory, understood)
    if not text:
        return None
    if not any(_phrase_in(text, word) for word in ROAST_WORDS):
        return None
    lowered = str(text).lower()
    if any(_a_word(text, word) for word in ROAST_NOT_FOR_US):
        return None
    if _ruled_out(text, tuple(ROAST_MINUTES)):
        return None
    where = None
    for name in sorted(ROAST_MINUTES, key=len, reverse=True):
        if _name_in(text, name):
            where = name
            break
    if where is None:
        return None
    minutes, how = ROAST_MINUTES.get(where, ("25 to 30", "cut into even pieces"))
    head = where[0].upper() + where[1:]
    return (head + ": " + minutes + " minutes in the oven at 200C (180C fan), " + how +
            ", in a single layer with a little oil so it browns rather than steams. It is done "
            "when the edges are browned and a knife goes into the thickest piece easily.")



VEG_EXTRA_AVOID = {
    "globe artichoke": ("jerusalem", "jerusalem artichoke", "jerusalem artichokes",
                        "sunchoke", "sunchokes"),
}


def _slug(name):
    return "veg-" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


ENTRIES = tuple(
    entry(_slug(names[0]), (names, VEG_ASKS), _reply_for(names, said, VEG_HOW.get(names[0])),
          avoid=VEG_NOT_FOR_US + VEG_EXTRA_AVOID.get(names[0], ()), bias=2)
    for names, said in VEG_TIME) + tuple(
    entry(_slug(names[0]), (names, VEG_ASKS), _reply_for(names, None, how),
          avoid=VEG_NOT_FOR_US, bias=2)
    for names, how in VEG_HOW_EXTRA)

ENTRIES = ENTRIES + (
    entry("veg-roast", (tuple(ROAST_MINUTES),
                        ("in the oven", "oven", "roast", "roasted", "roasting", "bake", "baked",
                         "baking", "air fryer", "how long", "long", "minutes", "time",
                         "roasting time", "roast time", "time in the oven", "oven time",
                         "how long in the oven")),
          _roast_reply,
          avoid=VEG_NOT_FOR_US, bias=1),
)

ENTRIES = ENTRIES + (
    entry("veg-chips-crisp",
          (("chips", "chip", "fries", "french fries", "oven chips", "homemade chips",
            "chips and fries", "wedges", "potato wedges", "wedge"),
           ("soggy", "soft", "limp", "floppy", "crispy", "crisp", "crispier", "crisp up",
            "go crispy", "not crispy", "not crisp", "wont crisp", "won't crisp")),
          "Soggy chips are a steam problem, so the fix is dry and hot: pat fresh-cut chips dry "
          "(rinse the starch off first if you cut them yourself) and put frozen ones in straight "
          "from the freezer, then get the oven and the tray properly hot - 200C (180C fan) - and "
          "spread them in one layer with space around each chip, because a crowded tray steams "
          "instead of crisping. Salt them as they come out and not before, since salt pulls water "
          "to the surface. If they still come out limp, cook them twice: 10 minutes at 160C to "
          "soften the middle, then 8 minutes at 190C to crisp the outside, with a few minutes "
          "resting in between.",
          avoid=("how long", "minutes", "temperature", "how much", "portion", "portions",
                 "price", "calorie", "calories", "healthy", "unhealthy", "freeze", "refreeze",
                 "defrost", "reheat", "leftover", "left over", "goes with", "with what",
                 "chip shop", "takeaway", "roast potato", "roast potatoes", "roasties",
                 "chicken", "fish", "prawn", "prawns", "halloumi", "tofu", "nugget", "nuggets",
                 "goujon", "goujons", "schnitzel", "katsu", "scotch egg", "onion ring",
                 "onion rings", "spring roll", "spring rolls", "batter", "battered", "breaded",
                 "breadcrumb", "breadcrumbs", "panko", "tempura"),
          bias=2),
    entry("fried-crisp",
          (("chicken", "fish", "prawn", "prawns", "halloumi", "nugget", "nuggets",
            "goujons", "schnitzel", "katsu", "scotch egg", "onion rings", "spring rolls",
            "batter", "battered", "coated", "panko", "tempura", "fried"),
           ("crispy", "crisp", "crunchy", "crunch", "soggy", "soft", "limp", "goes soft",
            "gone soft", "not crispy", "wont crisp", "won't crisp", "stay crisp", "keep crisp")),
          "Three things keep a fried coating crisp: a dry surface, oil that is hot enough, and "
          "air under it once it is out. Pat the food dry and flour it before the egg and crumbs, "
          "because a wet surface steams from the inside; fry at about 175C to 180C, which is a "
          "cube of bread browning in 60 seconds, since cooler oil soaks in and hotter oil browns "
          "the outside before the middle is done. Drain it on a rack over a tray rather than on "
          "kitchen paper, which traps the steam against the underside, and never put a lid or "
          "foil over the plate: serve it straight away, or hold it uncovered in a 100C oven on a "
          "rack, which keeps the coating dry for about 20 minutes. If you are cooking in "
          "batches, do not pile the finished pieces on top of each other.",
          avoid=("how long", "minutes", "temperature", "how much", "portion", "portions",
                 "calorie", "calories", "healthy", "unhealthy", "freeze", "refreeze", "defrost",
                 "reheat", "leftover", "left over", "goes with", "chip", "chips", "fries",
                 "roast potato", "roast potatoes", "pizza", "recipe", "marinade", "marinate",
                 "bake", "roast", "air fryer", "sous vide", "raw", "pink", "safe", "done",
                 "tofu", "pressed tofu",
                 "freezer", "frozen", "freeze", "thaw", "thawed", "thawing", "defrost",
                 "defrosted", "defrosting", "refreeze", "refrozen", "last night", "still ok",
                 "still okay", "safe to eat", "gone off", "went off"),
          bias=5),
)

WATER_WORDS = ("soggy", "going soggy", "goes soggy", "gone soggy", "went soggy", "go soggy",
               "soggy when", "watery", "watery when", "leaking water", "leaks water",
               "gives up water", "let out water", "mushy", "wet")

WATER_FAMILIES = (
    (("courgette", "courgettes", "zucchini"),
     "Courgette goes soggy because it is mostly water, so the water has to come out before it "
     "hits the pan: slice it about 1cm thick, salt it for 10 to 15 minutes, pat it dry, then "
     "cook it in a wide hot pan in one layer with no lid, or roast it at 220C spread out. "
     "Crowding the pan steams it, and a lid guarantees it - and if it is going in a salad, salt "
     "it and drain it first rather than dressing it early."),
    (("cucumber", "cucumbers"),
     "Cucumber goes soggy because salt and dressing pull the water out of it: slice it, salt it "
     "for 10 minutes and drain it on kitchen paper, or scoop the watery middle out with a "
     "teaspoon, and dress it at the table rather than an hour before. For a sandwich it wants to "
     "be patted dry and kept away from the bread until you eat."),
    (("aubergine", "aubergines", "eggplant", "eggplants"),
     "Aubergine goes soggy when it soaks up oil: salt the slices for 20 minutes, pat them dry, "
     "then fry in hot oil in one layer, or brush them with oil and roast at 200C until the edges "
     "colour. It is done when it collapses and looks glossy, not when it is merely soft."),
    (("mushroom", "mushrooms"),
     "Mushrooms go soggy when they are crowded or covered: they are mostly water, so give them a "
     "wide hot pan with a little oil, one layer, no lid, and let the water cook off before you "
     "turn them. Salt only at the end, or they give up their water early and stew."),
    (("tomato", "tomatoes", "cherry tomatoes"),
     "Tomato goes watery when it is cooked with the lid on or with too much salt early: halve "
     "them, salt them in a colander for 10 minutes and let the juice run off, then roast them cut "
     "side up at 200C, or cook them uncovered so the water reduces instead of pooling."),
    (("pepper", "peppers", "bell pepper", "bell peppers"),
     "Peppers go soft and watery when they are cooked fast in a crowded pan: cut them into strips "
     "of the same size and give them a hot wide pan in one layer, or roast them at 200C until the "
     "skins blister - then they are sweet rather than wet."),
    (("butternut squash", "squash", "pumpkin"),
     "Squash goes soggy when it is steamed rather than roasted: cut it into 3cm chunks, toss in "
     "oil, spread it in one layer and roast at 200C for 30 to 35 minutes, turning once. Boiled or "
     "covered, it holds on to the water and turns to mush."),
)

ENTRIES = ENTRIES + (
    entry("veg-watery", (tuple(name for names, _fix in WATER_FAMILIES for name in names),
                         WATER_WORDS),
          lambda memory, understood: _watery_veg(understood),
          avoid=("freezer", "freeze", "frozen", "thawed", "thaw", "thawing", "defrosted",
                 "defrost", "how long", "last", "lasts", "leftovers",
                 "leftover", "reheat", "calories", "calorie", "healthy", "protein", "vitamin",
                 "plant", "plants", "planting", "grow", "growing", "garden", "allotment",
                 "seed", "seeds", "harvest", "pick", "picking", "ripe", "buy", "buying",
                 "cost", "price", "cheap", "supermarket", "allergy", "allergic", "baby",
                 "weaning", "diabetes", "mouldy", "gone off", "wilted", "wilting", "slimy",
                 "limp"),
          bias=5),
)


def _watery_veg(understood):
    words = understood.get("words") if isinstance(understood, dict) else None
    text = " ".join(str(word) for word in (words or ())) or str(
        (understood or {}).get("clean") or "")
    text = text.lower()
    best = None
    for names, fix in WATER_FAMILIES:
        for name in names:
            if _phrase_in(text, name) and (best is None or len(name) > best[0]):
                best = (len(name), fix)
    return best[1] if best else None


VEG_SOFT_FAULTS = ("soggy", "limp", "floppy", "mushy", "slimy", "watery", "overcooked",
                   "over cooked", "too soft", "went soft", "gone soft", "gone soggy",
                   "going soggy", "gone limp", "went limp", "not crisp", "not crispy",
                   "wont crisp", "won't crisp", "soft and wet")

VEG_SOFT_NAMES = (tuple(name for names, _said in VEG_TIME for name in names)
                  + tuple(name for names, _how in VEG_HOW_EXTRA for name in names)
                  + tuple(VEG_HOW)
                  + ("vegetables", "veg", "veggies", "mixed veg", "stir fry veg", "roast veg",
                     "leafy greens", "broccoli", "peas", "sprouts", "sprout", "parsnip",
                     "parsnips", "romanesco", "broccolini", "spring onions", "shallot",
                     "shallots", "butternut", "pumpkin", "aubergine", "aubergines"))

VEG_ROASTED = ("roast", "roasted", "roasting", "oven", "baked", "baking", "air fryer",
               "airfryer", "tray", "traybake", "grill", "grilled")

VEG_WET = ("courgette", "courgettes", "zucchini", "aubergine", "aubergines", "marrow",
           "tomato", "tomatoes", "squash", "butternut squash", "butternut", "pumpkin")
VEG_LEAVES = ("spinach", "kale", "chard", "cavolo nero", "spring greens", "greens",
              "leafy greens", "collard")
VEG_PODS = ("peas", "mange tout", "mangetout", "sugar snap", "green beans", "runner beans",
            "french beans", "string beans", "broad beans", "broad bean", "fava beans")
VEG_RAW_FAULTS = ("gone soft", "went soft", "gone limp", "went limp", "gone floppy",
                  "gone bendy", "gone rubbery", "gone wrinkly", "gone leathery", "lost its crunch",
                  "lost their crunch", "gone dry", "dried out")

VEG_PREVENTION = ("how do i stop", "how can i stop", "how to stop", "how do i keep", "how can i keep",
                  "how do i prevent", "how do i make sure", "how long", "how do i cook",
                  "how do i boil", "how do i steam", "how do i roast", "how do i fry",
                  "stop it going", "stop them going", "stop it from going", "stop them from going",
                  "keep it from", "keep them from", "so it doesnt go", "so they dont go",
                  "so it doesn't go", "so they don't go")

VEG_GENERIC = ("veg", "vegetables", "veggie", "veggies", "mixed veg", "stir fry veg", "root veg",
               "veg mix", "veg of", "some veg")

VEG_COOKED = ("roast", "roasted", "roasting", "boil", "boiled", "boiling", "steam", "steamed",
              "fry", "fried", "frying", "cook", "cooked", "cooking", "oven", "pan", "microwave",
              "air fryer", "stir fry", "stir fried", "grill", "grilled", "bake", "baked")

VEG_BRASSICAS = ("broccoli", "cauliflower", "cabbage", "sprouts", "sprout", "romanesco",
                 "broccolini", "pak choi", "pak choy", "bok choy", "kalettes", "savoy",
                 "kohlrabi", "turnip")


def _soft_veg(text, understood=None):
    if not isinstance(text, str) or not text:
        return None
    if not any(_name_in(text, name) for name in VEG_SOFT_NAMES) and isinstance(understood, dict):
        said = str(understood.get("text") or "").lower()
        if said and said != text:
            text = said
    if any(_phrase_in(text, word) for word in ("slimy", "smelly", "sour", "gone off")):
        return ("A raw vegetable that is slimy and smells is going off, so bin the affected leaves "
                "or the whole bag: that slime is bacteria, not water, and cooking will not make it "
                "safe to eat. Slime on a cooked vegetable is the harmless kind - it means too long "
                "in the water - so drain it, press the water out and dress it with oil and lemon.")
    if (any(_phrase_in(text, word) for word in VEG_RAW_FAULTS)
            and not any(_phrase_in(text, word) for word in VEG_COOKED)):
        return ("A raw vegetable that has gone limp has lost water, not flavour: it is still safe to "
                "eat, and half an hour in a bowl of iced water firms it up again for a salad. After "
                "that, cook it - roast it at 200C, or put it in a soup or a stir-fry - because a "
                "limp one will not crisp back on its own. For the next lot, a bag or a lidded tub in "
                "the salad drawer keeps it firm for weeks, and cutting the green tops off carrots "
                "stops them pulling the water out of the root.")
    if (any(_phrase_in(text, word) for word in VEG_PREVENTION)
            and not any(_name_in(text, word) for word in VEG_GENERIC)):
        return None
    if any(_name_in(text, name) for name in VEG_PODS):
        return ("Peas and beans go from squeaky to mushy in about a minute: 2 minutes for frozen "
                "peas straight into boiling water, 4 to 5 for green beans, and drain them the "
                "moment they are bright. If they are already soft, toss them in butter with a "
                "squeeze of lemon and serve them as they are - a soft pea will not firm up - or "
                "let them cool into a salad or a soup.")
    if any(_name_in(text, name) for name in VEG_LEAVES):
        return ("Spinach, kale and other leaves go slimy in a pan of water, so cook them in "
                "almost none: a hot pan with a knob of butter and a spoon of water, 1 to 2 "
                "minutes until they have just collapsed, then press the water out. Raw leaves "
                "that have only gone limp come back in 15 minutes in iced water; cooked ones that "
                "are slimy were in too much water, so squeeze them dry and dress them with butter "
                "or a little vinegar, or fold them into a sauce.")
    if any(_name_in(text, name) for name in VEG_BRASSICAS):
        return ("Broccoli, cauliflower and cabbage go soft and grey from too long at a rolling "
                "boil: 4 to 5 minutes for broccoli florets, 6 to 8 for sprouts or shredded "
                "cabbage, 12 to 15 for a whole cauliflower, then straight into a colander with "
                "the lid off, because it goes on cooking in its own steam. If it has already gone grey and sulphury, give it a "
                "minute in a hot pan with butter and garlic, or put it in a gratin or a soup.")
    if any(_name_in(text, name) for name in VEG_WET):
        return ("Courgette, aubergine and tomato are mostly water, so that water has to come out "
                "before the heat goes on: slice them, salt them for 10 minutes and pat them dry, "
                "then fry or roast in one layer in a hot pan and do not crowd it, because a crowded "
                "pan steams them instead of browning. Already limp: turn the heat up to drive the "
                "water off, or put them in a sauce or a soup.")
    if any(_phrase_in(text, word) for word in VEG_ROASTED):
        return ("A vegetable that comes out of the oven soft was steamed rather than roasted: it "
                "went in wet, or the tray was crowded. Dry it, toss it in oil, spread it in one "
                "layer with air between the pieces, and give it 200C (180C fan) with the door "
                "shut. Already limp: turn the heat up for the last 10 minutes to colour what you "
                "can, and serve it with something sharp - it will not crisp back.")
    return ("A vegetable goes limp and wet from too long in the water, from a lid left on so the "
            "steam cannot escape, or from a pan too small for the amount: cook it in a shallow "
            "layer with a splash of water rather than a deep panful, taste it a minute before "
            "the time in the recipe, and drain it the second a knife slides in, lid off. If it "
            "is already soft, drive the water off in a hot dry pan with a little butter, or put "
            "it in a soup or a sauce, because it will not crisp again. A raw vegetable gone limp "
            "in the fridge is the same rescue: it has lost water rather than been overcooked, so "
            "roast it at 200C or put it in a soup within the day.")


ENTRIES = ENTRIES + (
    entry("veg-gone-soft",
          (VEG_SOFT_NAMES, VEG_SOFT_FAULTS),
          lambda memory, understood: _soft_veg(_typed_line(memory, understood), understood),
          avoid=("chips", "chip", "fries", "wedges", "roasties", "salad", "lettuce",
                 "apple", "fruit", "pasta", "rice", "noodles", "bread", "cake",
                 "pastry", "meat", "chicken", "beef", "pork", "lamb", "fish", "egg", "soup",
                 "sauce", "gravy", "curry", "stew", "pie", "pizza", "freezer", "freeze",
                 "frozen", "fridge", "keep", "keeps", "calories", "healthy", "recipe",
                 "use up", "use it up", "what can i do", "can i do with", "left over",
                 "leftover", "leftovers", "meal idea", "meal ideas"),
          bias=2),
)
