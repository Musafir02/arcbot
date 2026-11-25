import re

from .lookup import entry
from .swaps import SWAP_ASK

ANSWERS = ("cooking", "food-and-drink", "home-and-diy")

NO_KIT_ASK = SWAP_ASK + (
    "dont have", "don't have", "havent got", "haven't got", "havent any", "haven't any",
    "dont own", "don't own", "without", "no", "none", "only have", "only got", "just have",
    "just got", "all i have", "all ive got", "all i've got", "left with", "nothing but",
    "missing", "lost", "make do", "make-do", "improvise", "bodge", "borrow", "lend",
    "what can i use", "what do i use", "what should i use", "what else can i use",
    "anything else", "something else", "what else", "alternative", "replacement",
    "substitute", "instead", "swap", "replace", "ran out", "run out", "out of",
)

NOT_A_SHORTAGE = ("broken", "broke", "not working",
                  "stopped working", "stopping working",
                  "wont work", "won't work", "doesnt work", "doesn't work", "repair", "fix",
                  "fixing", "mend", "mending", "faulty", "spare part", "warranty", "guarantee",
                  "buy", "buying", "bought", "which one", "best", "cheapest", "recommend",
                  "clean", "cleaning", "wash", "washing", "store", "storing", "storage",
                  "limescale", "furred", "chalky", "full of scale", "scaled up",
                  "build up of scale", "buildup of scale", "scale in the", "scale on the",
                  "what is", "what are", "whats the", "what's the", "what is a", "whats a",
                  "what's a", "how do i use", "how to use",
                  "paint", "paints", "gloss", "emulsion", "varnish", "primer", "undercoat",
                  "tip", "recycling", "dump", "skip", "waste",
                  "sharpen", "reviews", "review", "price",
                  "out of the",
                  "oven", "ovens", "microwave", "microwaves", "slow cooker", "rice cooker",
                  "pressure cooker", "air fryer", "cooker hood",
                  "out of the fridge", "out of the freezer", "out of the oven", "out of the pan",
                  "out of the window", "out of the cupboard",
                  "temperature", "temperatures", "fever", "feverish", "feverishness")

STAND_IN = (
    ("colander", ("colanders", "strainer", "strainers"),
     "A clean tea towel, or the pan's own lid held a little open over the sink: pour slowly and "
     "the water runs out between the two. A sieve over a bowl does it for rice and small pasta, "
     "and a tray of ice in a bowl of water stops it cooking on if you want the pasta cold."),
    ("sieve", ("sieves", "sifter", "sifters"),
     "A fine colander or a tea strainer does it, and if you have neither, whisk the flour round a "
     "wide bowl for half a minute: the whisk breaks the lumps and lets the air in the same way "
     "sifting does."),
    ("whisk", ("whisks", "balloon whisk", "hand whisk", "electric whisk"),
     "A fork beats eggs and cream, just slower: keep the bowl deep and the wrist loose, and for "
     "cream chill both bowl and cream first. A clean jam jar with the lid on will whip a small "
     "amount of cream in about a minute of shaking."),
    ("rolling pin", ("rolling pins",),
     "Any smooth heavy cylinder does it: a wine bottle, a tall glass or a cold milk bottle, all "
     "of them dusted with flour. Chill the bottle first and the pastry stays cold, which keeps "
     "it short."),
    ("grater", ("graters", "box grater", "cheese grater"),
     "A vegetable peeler makes shavings of hard cheese and chocolate, and a knife does for "
     "anything going into a sauce. For parmesan or zest, a fine Microplane is the tool worth "
     "buying; until then, chop it as small as you can and it melts the same."),
    ("blender", ("blenders", "liquidiser", "liquidizer"),
     "A stick blender in a deep jug does most of it, and a food processor does the rest. A "
     "masher then a sieve gets you a smooth soup without either, and a jar with a tight lid "
     "shaken hard will dress a small amount of sauce."),
    ("food processor", ("food processors", "processor", "magimix"),
     "A stick blender for anything wet, a box grater for anything hard, and a knife for "
     "anything rough. Chopping an onion small by hand takes two minutes; a blender turns it to "
     "water, so keep the blade out of it."),
    ("measuring jug", ("measuring jugs", "jug", "measuring cup"),
     "A mug is about 250 to 300 ml, and a tablespoon is 15 ml and a teaspoon 5. Anything you "
     "would weigh, weigh in grams instead: for water and milk a millilitre is a gram, so 200 ml "
     "is 200g on the scales."),
    ("tin opener", ("tin openers", "can opener", "can openers"),
     "For a ring-pull, slide a spoon handle under the ring and lever it up. For a plain tin, "
     "the back of a heavy spoon or a stiff knife pressed down on the rim and worked round the "
     "top will open it - slowly, and the edges are sharp, so hold it with a cloth."),
    ("corkscrew", ("corkscrews", "bottle opener", "bottle openers"),
     "For a cork, push it in with the handle of a wooden spoon and then pour through a small "
     "sieve, or put the bottle in a shoe and tap the base against a wall (the cork walks out). "
     "For crown caps, a coin or the back of a lighter under the edge does it."),
    ("potato masher", ("mashers", "potato mashers"),
     "A fork for anything soft, and the end of a wooden spoon for potatoes. A ricer or a sieve "
     "and the back of a spoon gives a smoother mash than a masher ever does, which is what you "
     "want for gnocchi."),
    ("cake tin", ("cake tins", "round tin", "springform tin", "tins"),
     "A roasting tin lined with paper works: bake it as a traybake at the same temperature, "
     "checking five minutes earlier, and cut it into squares. A deep frying pan with a lid will "
     "bake a shallow cake on the hob if the lid goes on and the heat stays low."),
    ("loaf tin", ("loaf tins", "bread tin"),
     "A roasting tin or a deep ovenproof saucepan lined with baking paper. Free-standing bread "
     "bakes perfectly well on a lined tray; the tin is there for the shape, and a round loaf "
     "tastes the same."),
    ("baking parchment", ("parchment", "greaseproof paper", "baking paper", "silicon paper"),
     "Grease the tin well with butter and dust it with flour, or use a silicone mat, or foil "
     "brushed with oil. Parchment and greaseproof paper are not the same thing: greaseproof "
     "sticks to a cake, so grease it again on top if that is all you have."),
    ("cling film", ("clingfilm", "plastic wrap", "saran wrap"),
     "A plate over the bowl, or a clean damp tea towel, keeps a surface from drying. For dough "
     "left to rise, an upturned bowl over the whole thing is better than film anyway."),
    ("muslin", ("muslins", "cheesecloth", "jelly bag"),
     "A clean tea towel, a new J-cloth or a pair of clean tights works for jelly and for "
     "straining yoghurt. Scalding the cloth first with boiling water keeps it from tasting of "
     "soap, and hang it over a bowl with the corners tied to a cupboard handle."),
    ("piping bag", ("piping bags", "icing bag"),
     "A freezer bag with a corner snipped off, or a sheet of baking paper rolled into a cone and "
     "taped. A good zip-lock bag will take a star nozzle if you cut the corner to its width."),
    ("skewers", ("skewer", "kebab sticks", "bamboo skewers"),
     "Rosemary stems stripped of their leaves make fine skewers for lamb and chicken, and metal "
     "kebab sticks or a cake tester do the testing job. To test a cake, a knife blade or a "
     "strand of dry spaghetti works as well as a skewer."),
    ("thermometer", ("thermometers", "meat thermometer", "sugar thermometer"),
     "For meat, press the thickest part with a finger: springy and firm is done, soft is not. A "
     "knife pushed in and pulled out shows the juice running clear for chicken, and for sugar "
     "the old test is a drop in cold water - a soft ball for fudge, a hard crack for toffee."),
    ("funnel", ("funnels",),
     "A corner of baking paper, or the top half of a plastic bottle cut off and turned upside "
     "down. For jam into a jar, a jug with a spout and a steady hand beats both."),
    ("mortar and pestle", ("pestle and mortar", "mortar", "pestle"),
     "A bowl and the end of a rolling pin crushes spices, or put them in a bag and roll over it "
     "with a tin. Whole spices toasted in a dry pan first crush far more easily, whatever you "
     "crush them with."),
    ("slotted spoon", ("slotted spoons",),
     "A fork, or a normal spoon held back against the side of the pan as you lift, drains the "
     "same. A fish slice with holes does the job for anything bigger than a pea."),
    ("tongs", ("tongs", "tongs"),
     "Two forks back to back, or a spatula and a spoon. Chopsticks are the best stand-in there "
     "is for turning small things in a hot pan."),
    ("pastry brush", ("pastry brushes", "basting brush"),
     "Your fingertips for milk or egg wash, the back of a spoon for oil, and a scrunched piece "
     "of kitchen paper for glazing a pie. None of them shed bristles, which is the one thing "
     "the brush is for."),
    ("fridge", ("fridges", "refrigerator", "refrigerators"),
     "Buy little and often and keep what has to stay cold in the coolest place you have: a lidded "
     "box in the garage, a bucket of cold water with a cloth over it for milk, and a windowsill "
     "on the shady side in winter. Cooked food is the one thing not to push - eat it the day you "
     "make it, and keep the shopping to what fits in one bag."),
    ("freezer", ("freezers", "freezer compartment"),
     "Cook for the day rather than the week and keep nothing back: without freezing, leftovers "
     "are good for two days in the coldest spot you have and then they go. A cool box with ice "
     "packs buys you a day for meat, and a bag of ice in a bowl does for chilling a drink."),
    ("kettle", ("kettles", "electric kettle"),
     "A saucepan of water on the hob boils in about the same time, and a microwave does a mug in "
     "ninety seconds. For tea, pour the pan water while it is still at a rolling boil; a thermos "
     "keeps a litre hot for hours if you want it ready."),
    ("hob", ("hobs", "stove", "stovetop"),
     "A hob alone cooks more than people think: pasta, rice, stews, curries and anything in a "
     "covered pan, plus a great deal of fish and veg. What it cannot do is brown a crust, so "
     "finish under the grill if there is one - a tray bake is the other way to get an oven-ish "
     "result with no oven."),
    ("plunger", ("plungers", "sink plunger", "toilet plunger"),
     "Fill the bowl with enough water to cover the cup and use the flat of your hand, or a "
     "flat-bottomed cup held upside down, in short hard pushes over the plughole. Seal the "
     "overflow with a wet cloth first or the push escapes up it; if the water is not draining "
     "at all, go straight to the trap underneath with a bucket."),
    ("mop", ("mops", "floor mop"),
     "A cloth and a bucket: work backwards to the door, wringing as you go, and a dry towel "
     "under your feet dries the last of it. On a small floor a sponge and a bowl is quicker "
     "than a mop anyway."),
    ("hoover", ("hoovers", "vacuum", "vacuum cleaner", "vacuums"),
     "A broom or a stiff brush for a hard floor, and a damp rubber glove or a damp cloth for "
     "hair on carpet - it gathers in one swipe. A lint roller lifts crumbs and pet hair off a "
     "sofa or a stair carpet."),
    ("stepladder", ("stepladders", "step ladder", "ladder", "ladders"),
     "Borrow a proper ladder rather than stand on a chair, a bucket or a table: a fall from "
     "kitchen-counter height is how most DIY injuries happen, and the ceiling can wait. A "
     "neighbour, a friend or a hire shop for the afternoon is the cheap version."),
    ("drill", ("drills", "power drill", "cordless drill"),
     "Self-adhesive hooks take anything light, and a bradawl or a strong nail and a hammer "
     "starts a hole in plasterboard and soft wood. For masonry, borrow a drill: a nail in "
     "brick either bends or takes a lump of the wall with it."),
    ("hammer", ("hammers", "mallet", "mallets"),
     "A block of scrap wood or the heel of a heavy shoe taps in panel pins and small tacks "
     "without marking the surface. For anything bigger than that, wait, or borrow one: a "
     "saucepan is heavier than it looks and dents both the pan and the wall."),
    ("spirit level", ("level", "levels", "bubble level"),
     "A phone has a level in it, and a clear bottle half full of water on its side reads the "
     "same way: the bubble sits between the two marks. For a shelf, measure down from the "
     "ceiling at both ends - a shelf that matches the ceiling looks level even when it isn't."),
    ("stud finder", ("stud finders", "stud detector"),
     "Knock along the wall with a knuckle: a hollow tap is plasterboard with nothing behind it "
     "and a dull thud is a stud. A small magnet run across the wall finds the screws holding "
     "the board, and the stud is either side of them."),
    ("garden strimmer", ("strimmer", "strimmers", "weed whacker", "weed trimmer"),
     "Shears, or a pair of long-handled edging shears, cut the same grass at the edges and cost "
     "nothing to run. Cut little and often rather than letting it get long - long grass wraps "
     "round any machine, including the borrowed one."),
)


def _words(reading):
    words = (reading or {}).get("words")
    if isinstance(words, (list, tuple)):
        return [str(word).lower() for word in words]
    text = str((reading or {}).get("clean") or "").lower()
    return text.split()


def _the_word_for(row):
    return row[0]


def _no_kit(memory, reading):
    text = " " + str((reading or {}).get("clean") or "").lower() + " "
    words = set(_words(reading))
    best = None
    for row in STAND_IN:
        for name in (row[0],) + row[1]:
            if " " in name:
                if name in text and (best is None or len(name) > best[0]):
                    best = (len(name), row)
            elif name in words and (best is None or len(name) > best[0]):
                best = (len(name), row)
    if best is None:
        return ""
    return best[1][2]


_WITHOUT_A_MANNER = re.compile(r"\bwithout\s+(?:\w+ly\s+)?([a-z]+ing)\b")
_A_TOOL_IS_STILL_MISSING = frozenset((
    "using", "having", "needing", "buying", "owning", "spending", "paying", "borrowing",
))


def _is_a_shortage(reading):
    text = " " + str((reading or {}).get("clean") or "").lower() + " "
    manners = [match.group(1) for match in _WITHOUT_A_MANNER.finditer(text)]
    if not manners:
        return True
    return not all(word not in _A_TOOL_IS_STILL_MISSING for word in manners)


ENTRIES = [
    entry("no-kit",
          (tuple(name for row in STAND_IN for name in row[1]), NO_KIT_ASK),
          _no_kit,
          avoid=NOT_A_SHORTAGE,
          guard=_is_a_shortage,
          bias=2),
]
