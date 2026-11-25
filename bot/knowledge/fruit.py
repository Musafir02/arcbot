import re

from .lookup import entry

ANSWERS = ("cooking", "food-and-drink")

FRUIT_METHODS = (
    (("pomegranate", "pomegranates", "pomegranate seeds"),
     "Cut the crown off and score the skin down the ridges, then pull it apart over a big bowl of "
     "water: the seeds sink, the white pith floats, and nothing sprays your shirt. For a whole one "
     "in a hurry, hold a half cut-side down over a bowl and whack the back with a wooden spoon and "
     "the seeds drop out in a minute."),
    (("mango", "mangoes", "mangos"),
     "Slice a cheek off each side of the flat stone, score the flesh in a grid without cutting "
     "through the skin, then push the skin inside out and slice the cubes off. The stone and the "
     "flesh round it are the cook's, and a peeler takes the skin off the two cheeks if you would "
     "rather have slices."),
    (("pineapple", "pineapples"),
     "Cut the top and the base off flat so it stands up, then slice the skin off in strips from "
     "top to bottom, following the curve, and take the eyes out with the tip of the knife. Quarter "
     "it lengthways and cut the woody core out of each quarter."),
    (("kiwi", "kiwis", "kiwifruit"),
     "Top and tail it, then either run a vegetable peeler round it or cut it in half and scoop the "
     "flesh out with a teaspoon, which goes round the skin in one movement. A kiwi that is soft "
     "enough to eat peels with a spoon and no knife at all."),
    (("peach", "peaches", "nectarine", "nectarines", "plum", "plums", "apricot", "apricots",
      "cherry", "cherries"),
     "Run the knife round the seam, all the way round rather than through the stone, then twist the "
     "halves apart. A ripe peach or plum gives its stone up with a thumb; a clingstone that will "
     "not, cut it into quarters round the stone and flick it out. A cherry wants a bottle neck or "
     "a paperclip pushed into the dimple."),
    (("lemon", "lemons", "lime", "limes"),
     "Roll it hard on the counter with your palm first to break the cells inside, then cut it "
     "across the middle rather than end to end and squeeze with the cut face out, so the pips stay "
     "in your hand. A fork twisted in the half gets more juice out than a squeeze does, and half a "
     "minute in a microwave gets more again."),
    (("coconut", "coconuts"),
     "Three soft eyes sit at one end: push a screwdriver or a clean nail through the softest, drain "
     "the water into a glass, then hit round the equator with the back of a heavy knife or a "
     "hammer, turning it as you go, until it cracks in two. The flesh comes out with a knife run "
     "between it and the shell."),
    (("avocado", "avocados"),
     "Run the knife round the stone lengthways, twist the two halves apart, then whack the stone "
     "with the blade and twist it out, or push a spoon in behind it. Slip a spoon between the skin "
     "and the flesh to peel a half, and cut it only when you are about to eat it."),
    (("apple", "apples"),
     "Quarter it round the core with a knife and cut the core out of each quarter at an angle, or "
     "push an apple corer straight down over the stalk. A peeled or cut apple browns in minutes, so "
     "toss it in a little lemon juice if it has to wait."),
    (("melon", "melons", "watermelon", "watermelons", "cantaloupe", "honeydew"),
     "Cut it in half through the middle rather than end to end, scoop the seeds out with a spoon, "
     "then stand each half on its flat face and slice the skin off downwards in strips. A melon "
     "baller on a halved one is quicker than cubing, and watermelon gives up its seeds the same "
     "way, with a fork to flick out the stragglers."),
    (("orange", "oranges", "grapefruit", "grapefruits", "tangerine", "tangerines",
      "satsuma", "satsumas", "clementine", "clementines"),
     "Cut the top and the bottom off so it stands, then slice the peel and pith off in strips down "
     "the sides, following the curve, until no white is left. Cut the segments out between the "
     "membranes over a bowl to catch the juice, which beats peeling a grapefruit with your fingers "
     "and still finding pith."),
)

JUICE_WORDS = ("juice", "juiced", "juicing", "squeeze", "squeezing", "squeeze it")
JUICE_ASKS = ("how do i juice", "how do you juice", "how to juice", "how can i juice",
              "how would i juice", "how should i juice", "how do i squeeze", "how do you squeeze",
              "how to squeeze", "how can i squeeze", "how do i get the juice",
              "how do you get the juice", "how to get the juice", "get the juice out",
              "get more juice", "get more juice out", "get the most juice", "get all the juice",
              "get juice out of", "best way to juice", "easiest way to juice", "way to juice", "way to squeeze",
              "juice a", "juice an", "juice the", "juice some", "juice it", "juice them",
              "juicing a", "juicing the", "squeeze a", "squeeze an", "squeeze the", "squeeze it",
              "squeeze them", "squeezing a", "squeezing an", "squeezing the", "no juicer",
              "without a juicer", "by hand")
CITRUS = ("lemon", "lemons", "lime", "limes", "orange", "oranges", "grapefruit", "grapefruits",
          "tangerine", "tangerines", "satsuma", "satsumas", "clementine", "clementines")
JUICING = ("Roll it hard on the counter with your palm first to break the cells inside, then cut "
           "it across the middle rather than end to end and squeeze with the cut face out, so the "
           "pips stay in your hand. A fork twisted in the half gets more out than a squeeze does, "
           "and half a minute in a microwave gets more again. Sieve it if the pips and pith would "
           "spoil what it goes in.")

PREP_WORDS = ("cut", "cutting", "peel", "peeling", "core", "coring", "segment", "segments",
              "supreme", "stone", "stoned", "destone", "de-stone", "deseed", "de-seed", "deskin",
              "open", "opening", "prep", "prepping",
              "prepare", "preparing", "slice", "slicing", "chop", "chunks", "wedges", "top and tail",
              "get the seeds out", "take the stone out", "get the stone out")


def _said(understood):
    text = str(understood.get("clean") or understood.get("text") or "").lower()
    return " " + re.sub(r"[^a-z0-9' ]+", " ", text) + " "


def _holds(line, word):
    return (" " + word + " ") in line


def _fruit_prep(memory, understood):
    line = _said(understood or {})
    if any(_holds(line, word) for word in JUICE_WORDS):
        if not any(_holds(line, word) for word in JUICE_ASKS):
            return None
        return JUICING if any(_holds(line, word) for word in CITRUS) else None
    if not any(_holds(line, word) for word in PREP_WORDS):
        return None
    for words, method in FRUIT_METHODS:
        if any(_holds(line, word) for word in words):
            return method
    return None


NEED_TO_PEEL = re.compile(
    r"\b(?:do|does|should|must|need|needs|have|has|ought|would|will)\s+(?:i|we|you|they|it)\s+"
    r"(?:really\s+|actually\s+|even\s+)?(?:need\s+to\s+|have\s+to\s+|has\s+to\s+)?"
    r"(?:be\s+)?peel(?:ed)?\b"
    r"|\bpeel\s+(?:the\s+|my\s+|these\s+|those\s+)?(?:apples?|pears?|plums?|peaches|kiwis?|"
    r"grapes?)\s+(?:before|first|or not)\b"
    r"|\bis it necessary to peel\b|\bnecessary to peel\b|\bworth peeling\b"
    r"|\bmust be peeled\b|\bneeds peeling\b|\bneed peeling\b"
    r"|\b(?:is|is it|isn't it|would it be|is it not)\s+(?:better|best|worth|fine)\s+to\s+peel\b"
    r"|\bbetter to peel\b|\bbest to peel\b|\bstill worth peeling\b"
    r"|\b(?:do|does|would|should)\s+(?:you|people|most people|anyone|everyone)\s+"
    r"(?:usually\s+|always\s+|normally\s+|even\s+|bother to\s+)?peel\b")
SKIN_IN_A_DISH = re.compile(
    r"\b(?:crumble|cobblers?|pies?|pie filling|tarts?|cake|cakes|muffins?|loaf|loaves|bread|"
    r"brownies?|porridge|baked|baking|roast|roasted|stewed|stew|soup)\b")


def _skin_reply(memory, reading):
    said = (reading.get("clean") or reading.get("text") or "").lower()
    lead = "No need to peel - " if NEED_TO_PEEL.search(said) else "Yes - "
    in_a_dish = bool(SKIN_IN_A_DISH.search(said))
    dish = (" For a crumble, a pie or a cake, leave it on: the skin softens as it bakes and holds "
            "the fruit together, and peel only if you want the filling perfectly smooth."
            if in_a_dish else "")
    if "kiwi" in said or "kiwifruit" in said:
        body = ("kiwi skin is edible, and it holds more fibre and vitamin C than the green "
                "flesh, so scrub it under the tap and eat it if the fuzz does not put you off: "
                "the skin is thin, and rubbing it under water takes most of the hairiness off. A "
                "ripe kiwi eaten skin and all tastes the same, only tarter near the skin.")
        if lead.startswith("No need"):
            return lead + body
        return "Yes - " + body
    if any(word in said for word in ("grape", "grapes")):
        return (lead + "grape skins are food - that is where the colour, the tannin and much of "
                "the fibre sit - so wash them and eat them, and only peel a grape for a small "
                "child or someone who cannot manage the skin. A white bloom on the skin is "
                "natural yeast, not spoilage, so rinse it rather than peel it.")
    if any(word in said for word in ("peach", "peaches", "plum", "plums")):
        return (lead + "a peach or a plum is eaten with the skin on, and washing it is enough: "
                "the skin holds the colour and much of the fibre, and peeling only matters for a "
                "smooth chutney or for somebody who finds the fuzz unpleasant. Pour boiling water "
                "over a peach for 30 seconds and the skin slips off if you do want it off." + dish)
    return (lead + "apple and pear skin is the best part of it: the fibre, the colour and the "
            "quercetin that gives the skin its job are all in there, so wash the fruit and eat it "
            "as it is. Peeling loses about a third of the fibre and most of the vitamin C, and "
            "the only ones worth peeling are a waxed one if the wax bothers you, or fruit for a "
            "small child who cannot chew the skin." + dish +
            " The one case where the answer is cook it: if raw apple or pear makes your mouth "
            "itch or tingle, heat settles that - stewed, baked or in a crumble the protein that "
            "does it is broken down, and peeled is usually fine too.")


def _bruise_reply(memory, reading):
    said = (reading.get("clean") or "").lower()
    if "banana" in said:
        return ("A bruised banana is fine to eat: the bruise is the flesh knocked and oxidising, "
                "not rot, and a brown-spotted banana is sweeter because the starch has turned to "
                "sugar, which is why it is the one for banana bread. Cut out a soft black patch "
                "if you do not like the look of it, and bin the fruit only if the skin has split "
                "and it smells fermented or has mould on it.")
    return ("A bruise on fruit is a knock, not spoilage: the cell walls are broken and the flesh "
            "browns as it oxidises, which is why an apple or a peach browns where it was dropped. "
            "Cut the patch out if the texture bothers you, or eat it - the rest of the fruit is "
            "unchanged. Bin it only when the bruise is wet and sour-smelling or there is mould, "
            "because a soft bruise is the way in for rot.")

PIPS_AND_STONES = ("pip", "pips", "pippin", "pippins", "seed", "seeds", "stone", "stones",
                   "kernel", "kernels", "nut", "pit", "pits")

GROWN_FROM_A_PIP = ("apple", "apples", "pear", "pears", "plum", "plums", "peach", "peaches",
                    "nectarine", "nectarines", "cherry", "cherries", "apricot", "apricots",
                    "damson", "damsons", "avocado", "avocados", "lemon", "lemons", "lime",
                    "limes", "orange", "oranges", "clementine", "clementines", "satsuma",
                    "satsumas", "tangerine", "tangerines", "grapefruit", "grapefruits",
                    "fig", "figs", "olive", "olives", "pomegranate", "pomegranates",
                    "mango", "mangoes", "apple tree", "fruit tree", "cherry tree",
                    "peach tree", "lemon tree", "orange tree", "plum tree", "pear tree")

SHOP_SEED_VEG = ("tomato", "tomatoes", "cherry tomato", "cherry tomatoes", "beefsteak tomato")

STONE_FRUIT_PIPS = ("apple", "apples", "pear", "pears", "cherry", "cherries", "plum", "plums",
                    "peach", "peaches", "apricot", "apricots", "nectarine", "nectarines",
                    "damson", "damsons", "bitter almond", "almond", "almonds", "fruit pip",
                    "fruit pips", "apple pip", "apple pips", "apple seed", "apple seeds")

SEED_SOURCE = ("shop", "shops", "supermarket", "supermarkets", "store", "stores", "store bought",
               "store-bought", "from a tomato", "from the tomato", "from tomatoes", "in a tomato",
               "in the tomato", "in tomatoes", "seeds in", "seeds from", "seed from", "seed in",
               "saved seed", "save seed", "save the seed", "saving seed", "save", "saves",
               "saving", "saved", "harvest", "harvesting", "harvested", "keep the seed",
               "keeping seed", "kept seed", "collected", "collect the seed", "left over",
               "leftover", "last year", "next year", "from my own", "from our own")

PLANT_WORDS = ("plant", "plants", "planted", "planting", "grow", "grows", "growing", "grew",
               "sow", "sows", "sowing", "sprout", "sprouts", "sprouting", "germinate",
               "germinating", "propagate", "seedling", "seedlings", "sapling", "saplings",
               "from seed", "from a seed", "from a pip", "from pips", "from a stone",
               "from stones", "from a kernel", "will it grow", "can it grow",
               "save", "saves", "saving", "saved", "keep the seed", "keeping seed",
               "harvest", "harvesting", "collect the seed", "collecting seed", "store seed",
               "store the seed", "next year")

EAT_WORDS = ("eat", "eats", "eating", "eaten", "swallow", "swallowed", "swallowing",
             "chew", "chewed", "chewing", "poison", "poisonous", "toxic", "dangerous",
             "harmful", "hurt me", "bad for me", "deadly", "cyanide", "safe to", "safe",
             "should i eat", "can i eat", "is it ok to eat", "is it okay to eat",
             "kill", "kills", "killed", "die", "died", "dying", "fatal", "how many would",
             "would kill", "would die", "make me ill", "make me sick", "how many are safe",
             "how many kernels", "how many pips", "how many seeds")


TENDER_FRUIT = (
    (("fig", "figs"), (
        "A fig seed does come up in two or three weeks in warmth, but almost nobody grows figs "
        "from seed: the seedling is a lottery, it takes four to six years to fruit, and it may "
        "never fruit at all in a cool climate. Take a cutting instead - a 15cm piece of last "
        "year's wood in late winter, pushed into free-draining compost, roots in about six "
        "weeks. Figs also fruit best with their roots fenced in, which is why they do so well in "
        "a pot against a sunny wall.")),
    (("pomegranate", "pomegranates"), (
        "A pomegranate seed does grow, and it comes fairly true to the fruit it came from, but it "
        "is a Mediterranean tree: five years or more to the first fruit, a hot sheltered wall, and "
        "in a cool summer the fruit can stay hard and sour. Sow it fresh in spring at about 21C. "
        "Cuttings are quicker and are how the named varieties are sold, and a bought plant fruits "
        "in two or three years.")),
    (("mango", "mangoes", "mangos"), (
        "A mango stone will sprout on a windowsill - take the stone out of its hairy husk, stand "
        "it on its edge in damp compost with the top third showing, and it comes up in two or "
        "three weeks - but it is a tropical tree. It wants 25C and more, it grows into something "
        "far too large for a room, and it will not fruit in a temperate house. It is a good plant "
        "to grow for the leaves, not for fruit.")),
)

CITRUS_NAMES = ("grapefruit", "grapefruits", "lemon", "lemons", "lime", "limes", "orange",
                "oranges", "clementine", "clementines", "satsuma", "satsumas", "tangerine",
                "tangerines", "citrus")


def _the_fruit(line, words):
    for word in words:
        if _holds(line, word):
            return word[:-1] if word.endswith("s") and not word.endswith("ss") else word
    return "citrus"


def _growing_from_a_pip(memory, understood):
    line = _said(understood or {})
    if any(_holds(line, word) for word in ("avocado", "avocados")):
        return ("An avocado stone sprouts easily and almost never gives you avocados: push three "
                "cocktail sticks into the fat end and sit it over a glass so the base is just in "
                "the water, and roots show in four to six weeks. Pot it in free-draining compost "
                "when the shoot is 15cm, keep it in bright light and pinch the top out to make it "
                "bushy. It is a handsome houseplant that wants a bigger pot each year; fruit "
                "needs a mature tree, two of them for cross-pollination, and a warm climate.")
    if any(_holds(line, word) for word in SHOP_SEED_VEG):
        if not any(_holds(line, word) for word in SEED_SOURCE):
            return None
        lead = ("Yes, and it is worth doing: " if any(
            _holds(line, word) for word in ("can i", "could i", "is it possible", "will it",
                                            "would it", "does it"))
                else "Save the seed first: ")
        return (lead +
                "scoop the seeds and their jelly into a glass, add a little water and leave them "
                "three or four days until a film of mould sits on top - that ferment kills the "
                "germination inhibitor in the jelly - then rinse them, dry them on paper and sow "
                "them indoors from late February at 18-21C, about 6mm deep. A supermarket tomato "
                "is often a hybrid, so the fruit may come smaller or uneven, but it grows and it "
                "fruits, and dry seed in a paper envelope still comes up three or four years "
                "later.")
    if any(_holds(line, word) for word in CITRUS):
        return (f"A {_the_fruit(line, CITRUS_NAMES)} seed from the fruit bowl does grow, and comes closer to the "
                "parent than an apple pip does, but it is slow: expect five to fifteen years "
                "before fruit, and a plant that wants a sunny windowsill in winter and a spot "
                "outside in summer. Sow it fresh, before the seed dries out, in moist seed "
                "compost at about 21C, and pot it on as it grows. A named variety comes as a "
                "grafted tree, which fruits in two or three years and is what most people want.")
    for words, said in TENDER_FRUIT:
        if any(_holds(line, word) for word in words):
            return said
    if any(_holds(line, word) for word in ("peach", "peaches", "nectarine", "nectarines",
                                           "plum", "plums", "cherry", "cherries", "apricot",
                                           "apricots", "damson", "damsons", "olive", "olives")):
        return ("A stone will grow, but it needs a winter first: clean the flesh off, mix the stone "
                "with damp compost in a sealed bag and keep it in the fridge for six to ten "
                "weeks, then pot it and wait - plums and peaches come up in a couple of months "
                "after that. Expect four to eight years before fruit, and the fruit will not be "
                "the variety you ate, because a stone fruit is cross-pollinated. For fruit you "
                "can count on, buy a bare-root tree from November to March and plant it where it "
                "gets sun.")
    if not any(_holds(line, word) for word in ("apple", "apples", "pear", "pears", "apple tree",
                                               "pear tree", "fruit tree", "fruit pip",
                                               "fruit pips")):
        return None
    return ("An apple or pear pip does grow, but it will not give you the apple you ate: pips are "
            "crossed with whatever tree pollinated the flower, so the fruit is a lottery, often "
            "hard and sour, and it takes five to ten years to find out. If you want to try, keep "
            "the pips damp in the fridge for six to eight weeks - they need cold to break "
            "dormancy - then sow them in compost on a windowsill, where they come up in three "
            "to four weeks, and pot them on. For eating "
            "apples, buy a named variety: a bare-root tree planted between November and March "
            "fruits in three or four years and tastes of something.")


KERNEL_FRUIT = ("apricot kernel", "apricot kernels", "bitter kernel", "bitter kernels",
                "bitter apricot", "bitter almonds", "bitter almond", "apricot seeds",
                "apricot seed", "kernels", "kernel")


def _a_pip_to_eat(memory, understood):
    line = _said(understood or {})
    if any(_holds(line, word) for word in KERNEL_FRUIT):
        return ("Careful with these ones: a bitter apricot kernel holds about forty times the "
                "amygdalin of an apple pip, and amygdalin releases cyanide when it is chewed. One "
                "or two do most adults no harm; around ten to twenty bitter kernels have caused "
                "poisoning and deaths, and a child needs far fewer, so a child should have none "
                "at all. Bitter almonds are the same thing under another name, and the 'vitamin "
                "B17' sold as a cancer cure is laetrile, which is the same cyanide story and does "
                "not treat cancer. If someone has eaten a handful, ring 999 - headache, dizziness, "
                "vomiting, a flushed face or confusion after eating them is an emergency - and "
                "ring 111 if they feel well but you are unsure. Sweet kernels from a labelled "
                "packet are much lower, but an unlabelled bag is not worth the risk.")
    if (re.search(r"\bhow many\b", line)
            and any(_holds(line, word) for word in ("pip", "pips", "seed", "seeds", "stone",
                                                    "stones", "kernel", "kernels"))
            and re.search(r"\b(?:in|inside|does|has|have|are there)\b", line)):
        if _holds(line, "apple") or _holds(line, "apples"):
            return ("Usually five to ten, in two rows in the core: an apple has five seed "
                    "chambers and each holds one or two pips. A big apple has more pips than a "
                    "small one, and a pippin is simply an apple grown from a pip. None of them "
                    "will grow into the apple you ate, because the tree they came from was "
                    "pollinated by another one nearby.")
        if _holds(line, "lemon") or _holds(line, "lemons") or _holds(line, "lime") or \
                _holds(line, "limes") or _holds(line, "orange") or _holds(line, "oranges"):
            return ("A lemon or a lime has about eight to ten seeds, an orange about the same, "
                    "and they sit in the segments rather than in a core. A citrus seed is more "
                    "likely to grow than an apple pip, and it still takes a few years and a "
                    "sunny windowsill to become a plant worth keeping.")
    if any(_holds(line, word) for word in ("dog", "dogs", "puppy", "cat", "cats", "kitten",
                                           "pet", "pets", "bird", "birds", "parrot")):
        return ("The pips and stones of apples, pears, cherries, plums, peaches and apricots are "
                "worse for a dog or a cat than for you: they hold amygdalin, which releases "
                "cyanide when one is crushed and chewed, and a small animal needs much less than "
                "a person does. A couple swallowed whole usually pass straight through, but call "
                "the vet if a pet has chewed a handful, and keep the cores and stones out of the "
                "bowl you put down.")
    return ("Fine, in the amounts anyone eats by accident: the pips and kernels of apples, pears, "
            "cherries, plums, peaches and apricots hold amygdalin, which releases a little cyanide "
            "when the pip is crushed and chewed - but you would have to chew a cupful at once to "
            "be in trouble. A pip swallowed whole comes out the other end intact, so a child who "
            "ate two or three is not an emergency; watch for a sore tummy and ring 111 if you are "
            "worried. The flesh is the part to eat, and the pips are best left in the core.")


ENTRIES = [
    entry("juice-yield",
          (("much juice", "juice in", "juice from", "how many lemons",
            "how many limes", "how many oranges", "how many grapefruit", "cup of juice",
            "tablespoons of juice", "ml of juice"),
           CITRUS + ("how much", "how many", "much", "many", "cup", "cups", "tablespoon",
                     "tablespoons", "ml")),
          "A lemon gives about 3 tablespoons of juice, 45ml, and a lime about 2, 30ml. A big "
          "orange gives about half a cup (120ml) and a small one a third of a cup; a grapefruit "
          "gives about two thirds of a cup. So a cup of lemon juice is four or five lemons, and "
          "rolling them hard on the counter before squeezing gets a little more out of each.",
          avoid=("get the juice out", "get the juice", "get more juice", "get the most juice",
                 "squeeze", "squeezing", "juice a", "juice an", "juice the", "how do i juice")),
    entry(
        "prepare-fruit",
        (tuple(word for words, _method in FRUIT_METHODS for word in words),
         PREP_WORDS + JUICE_WORDS),
        _fruit_prep,
        avoid=("pizza", "pizzas", "hawaiian", "curry", "chutney", "crumble", "tart", "cake",
               "shell went in", "shell in", "grow", "growing", "tree", "trees", "plant", "plants",
               "buy", "buying", "price", "cost", "shop", "supermarket", "ripe", "ripen",
               "ripening", "smoothie", "juice bar", "how many calories", "healthy", "frozen",
               "tomato", "tomatoes",
               "how do i store", "how do i keep", "how do you store", "how do you keep",
               "store a cut", "keep a cut", "keeping it", "store it", "keep it", "goes brown",
               "going brown", "stays green", "stay green",
               "hard as a stone", "hard as stone", "hard as stones", "hard as a rock",
               "hard as rocks", "rock hard", "rock-hard", "still hard", "so hard", "too hard",
               "hard as", "unripe", "not ripe", "nowhere near ripe", "sour and hard",
               "firm as a stone", "like a stone"),
        ask=PREP_WORDS + JUICE_WORDS,
        bias=1,
    ),
    entry("fruit-skin-edible",
          (("kiwi", "kiwis", "kiwifruit", "peach", "peaches", "plum", "plums", "apple",
            "apples", "pear", "pears", "grape", "grapes"),
           ("skin", "skins", "peel"),
           ("eat", "eating", "edible", "safe", "ok", "okay", "have to", "need to", "should i",
            "can i", "do i", "with the skin", "leave the skin", "unpeeled")),
          _skin_reply,
          avoid=("apple sauce", "applesauce", "cranberry sauce", "gooseberry sauce",
                 "how do i peel", "how to peel", "how do i cut", "how to cut", "how do i prepare",
                 "freeze", "freezer", "freezing", "frozen", "defrost", "defrosting",
                 "cut a", "cut an", "cut the", "slice", "slicing", "deseed", "core",
                 "juicing", "juice", "calories", "how many", "ripe", "ripen", "buy",
                 "hard", "hard as", "still hard", "rock hard", "unripe", "not ripe", "sour",
                 "tasteless", "no flavour", "no flavor", "soften", "softer",
                 "price", "grow", "growing", "tree", "allergy", "allergic", "reaction",
                 "itch", "itches", "itching", "itchy", "tingle", "tingles", "tingling",
                 "rash", "rashes", "hives", "raw", "sore mouth", "mouth is sore",
                 "oven", "cook", "cooked", "cooking", "do i bake", "to bake", "bake them",
                 "bake it", "bake a", "bake an", "bake the", "bake for", "how long to bake",
                 "bake at", "roast", "roasted", "roasting", "grill", "grilled", "poach",
                 "poached", "stew", "stewed", "microwave",
                 "how long", "minutes", "temperature", "gas mark",
                 "keep", "keeps", "keeping", "store", "stores", "storing", "storage", "fresh",
                 "fresher", "freshest", "last", "lasts", "lasting", "fridge", "counter",
                 "going off", "gone off", "bruise", "bruised", "bruises",
                 "shrivel", "shrivelled", "wrinkled", "mouldy", "mould", "moldy", "mold",
                 "pregnant", "pregnancy", "breastfeeding", "dog", "dogs", "cat", "cats",
                 "kitten", "puppy", "pet", "pets", "vet", "toddler", "baby", "weaning",
                 "going brown", "goes brown", "go brown", "gone brown", "turn brown",
                 "turns brown", "turning brown", "brown quickly", "stop it going",
                 "stop them going", "from browning", "from going brown", "not go brown",
                 "rabbit", "rabbits", "bunny", "bunnies", "hamster", "hamsters", "guinea pig",
                 "guinea pigs", "guineapig", "guineapigs", "budgie", "budgies", "parrot",
                 "parrots", "tortoise", "tortoises", "horse", "horses", "pony", "ponies",
                 "chinchilla", "chinchillas", "gerbil", "gerbils", "ferret", "ferrets",
                 "apple id", "apple account", "apple watch", "apple pay", "apple music",
                 "apple tv", "apple store", "applecare", "apple care", "apple support",
                 "apple pencil", "apple inc", "icloud", "iphone", "ipad", "macbook",
                 "airpods", "app store", "apple id password", "apple id locked",
                 "pick a", "pick the", "how do i pick", "how to pick", "which ones", "which one",
                 "which apple", "which apples", "choose", "choosing", "best apple", "best apples",
                 "good apple", "good apples", "ripe one", "ripest",
                 "how long", "how many minutes", "how long in", "how hot", "gas mark",
                 "what temperature", "temperature", "degrees", "180c", "200c", "mins"),
          bias=1),
    entry("bruised-fruit",
          (("banana", "bananas", "apple", "apples", "pear", "pears", "peach", "peaches", "plum",
            "plums", "avocado", "avocados", "mango", "mangoes", "fruit", "nectarine",
            "nectarines", "tomato", "tomatoes"),
           ("bruised", "bruise", "bruises", "brown spot", "brown spots", "black spot",
            "black spots", "brown patch", "brown patches", "brown inside", "gone brown",
            "went brown", "soft spot", "soft spots", "knocked", "dropped", "dented")),
          _bruise_reply,
          avoid=("my leg", "my arm", "my knee", "my shin", "my thigh", "my back", "my ribs",
                 "my hand", "my foot", "my ankle", "my wrist", "my shoulder", "my head",
                 "i fell", "i bumped", "fell over", "bumped into", "after a fall", "hit my",
                 "icing", "ice it", "swollen", "swelling", "child", "toddler", "baby",
                 "bleeding", "nosebleed", "growing", "grow", "tree", "plant", "tree is",
                 "dropping", "dropping fruit", "falling off", "falls off", "off the tree",
                 "on the tree", "june drop",
                 "why do i bruise", "bruise easily", "bruises easily", "recipe", "bake",
                 "bread", "muffin", "loaf"),
          bias=4),
    entry("grow-from-a-pip",
          (GROWN_FROM_A_PIP + SHOP_SEED_VEG, PIPS_AND_STONES, PLANT_WORDS),
          _growing_from_a_pip,
          avoid=("how do i stone", "how to stone", "destone", "de-stone", "get the stone out",
                 "take the stone out", "remove the stone", "without the pips", "pips out",
                 "seeds out", "deseed", "de-seed", "recipe", "recipes", "cake", "cakes",
                 "chutney", "jam", "pie", "crumble", "smoothie", "juice", "juicing",
                 "eat", "eating", "eaten", "poison", "poisonous", "toxic", "cyanide",
                 "kill", "die", "fatal", "how many would", "harm", "harmful", "safe",
                 "dangerous", "ill", "sick", "hospital",
                 "hard", "hard as", "as hard as", "rock hard", "still hard", "unripe",
                 "not ripe", "ripe", "ripen", "ripening", "soft", "soften", "softer", "squishy",
                 "tasteless", "no taste", "sour", "bland", "watery",
                 "healthy", "calories", "price", "cost", "how much does", "buy", "buying",
                 "sainsbury", "tesco", "asda", "aldi", "lidl", "waitrose",
                 "support", "supporting", "stake", "stakes", "prune", "pruning", "blight",
                 "yellow leaves", "water them", "watering", "feed", "feeding", "fertiliser",
                 "personal independence payment", "benefit", "benefits", "claim",
                 "dla", "esa", "universal credit"),
          ask=PIPS_AND_STONES),
    entry("pips-to-eat",
          (STONE_FRUIT_PIPS, PIPS_AND_STONES, EAT_WORDS),
          _a_pip_to_eat,
          avoid=("plant", "plants", "planted", "planting", "grow", "grows", "growing",
                 "grew", "sow", "sowing", "sprout", "sprouting", "seedling", "sapling",
                 "from seed", "from a pip", "from a stone", "tree", "trees", "garden",
                 "allotment", "compost", "pot them", "pot it", "germinate",
                 "how do i stone", "how to stone", "destone", "de-stone", "get the stone out",
                 "take the stone out", "remove the stone", "deseed", "de-seed",
                 "recipe", "cake", "chutney", "jam", "pie", "crumble", "smoothie",
                 "personal independence payment", "benefit", "benefits", "claim",
                 "dla", "esa", "universal credit",
                 "itch", "itches", "itching", "itchy", "tingle", "tingles", "tingling",
                 "rash", "rashes", "hives", "sore mouth"),
          ask=PIPS_AND_STONES + EAT_WORDS),
]

