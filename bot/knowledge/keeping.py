import re

from .cooking import COOKED_WORDS, COOKING_WORDS, KEEP_WORDS, USE_UP_WORDS
from .dishes import KEEP_QUALITY_WORDS
from .lookup import DISH_ASK, PACK_DATE, entry

ANSWERS = ("cooking", "food-and-drink")

KEEP_NOT_KEEPING = ("healthy", "unhealthy", "good for you", "bad for you", "fattening",
                    "calories", "carbs", "carbohydrates", "protein", "vitamins", "nutrition",
                    "nutritious", "diet", "dieting", "superfood",
                    "keep me up", "keeps me up", "keep you up", "keeps you up",
                    "keep me awake", "keeps me awake", "keep you awake", "keeps you awake",
                    "awake at night", "stay awake", "cant sleep", "can't sleep")

OATS_BAG = (
    "Porridge oats keep about 6 months in an airtight jar in a cool, dry cupboard, and a sealed "
    "bag that has stayed dry is still fine a year past the date on it. Ground oats and oat bran "
    "go off sooner, about 3 months, because the oils in them turn: smell the bag, and oats that "
    "smell dusty or taste bitter have gone. Cooked porridge is a keep-two-days food, cooled "
    "quickly and reheated with a splash of milk.")
OATS_COOKED = (
    "Cooked porridge keeps 2 days in the fridge in a covered bowl, and reheat it once with a "
    "splash of milk or water over a low heat, because it sets solid as it cools - the same two "
    "days cooked rice gets, and for the same reason. Dry oats in the bag keep about 6 months in "
    "an airtight jar in a cool, dry cupboard, and longer if the bag stays sealed.")


def _oats_kept(memory, understood):
    said = " ".join(str((understood or {}).get(key) or "")
                    for key in ("clean", "norm_text", "norm")).lower()
    if "cooked" in said or "made" in said or ("porridge" in said and "oats" not in said):
        return OATS_COOKED
    return OATS_BAG


ROWS = (
    (("flour", "plain flour", "self raising flour", "self-raising flour", "bread flour"),
     "Flour keeps 6 months in a sealed jar in a cool cupboard and a year in the freezer; wholemeal "
     "and brown flour go off sooner, 3 months, and smell of old paint when they do. Put a bay "
     "leaf in the jar and the weevils leave it alone."),
    (("coffee", "ground coffee", "coffee beans", "instant coffee", "coffee granules"),
     "Ground coffee is at its best in the 2 weeks after opening: keep it in an airtight tin in a "
     "dark cupboard rather than the fridge, which is damp and smells of everything else. Beans "
     "keep a month, and more than a month's worth is better frozen and ground from frozen."),
    (("spices", "spice", "ground spices", "paprika", "cumin", "turmeric", "cinnamon"),
     "Ground spices fade in about 6 months and whole ones last 2 to 3 years: small airtight jars, "
     "away from the hob and the light. Sniff a spoonful - if it smells of nothing it will taste of "
     "nothing, and toasting what is left brings it back a little."),
    (("oil", "olive oil", "cooking oil", "vegetable oil", "sunflower oil", "rapeseed oil"),
     "Oil keeps about a year once opened, often past the date on the bottle if it stays cool and "
     "dark: the cupboard rather than beside the hob, with the cap on. Rancid oil smells of crayons "
     "or old nuts and tastes of them too, so bin it."),
    (("fruit", "fruits"),
     "Most fruit keeps 3 to 7 days in the salad drawer, and it is worth knowing the spread: "
     "berries and ripe stone fruit a day or two, apples, oranges and pears a week or more, and "
     "anything already cut 3 days in a sealed tub. Bananas, whole melons and tomatoes keep their "
     "flavour better out of the fridge."),
    (("celery", "celery sticks", "head of celery", "stick of celery"),
     "A head of celery keeps 2 weeks wrapped in foil in the fridge, which keeps it crisp where a "
     "plastic bag makes it slimy. Limp sticks come back in 20 minutes in iced water, so shave the "
     "dry bottom off first."),
    (("lettuce", "lettuces", "iceberg", "little gem", "romaine"),
     "Lettuce keeps about a week in the fridge: wash and dry the leaves, wrap them in kitchen "
     "paper inside a bag and dress them only at the table, because wet leaves and early dressing "
     "are what wilt a salad. Keep the bag in the salad drawer rather than at the back, where it "
     "freezes; limp leaves come back in iced water for 10 minutes."),
    (("cucumber", "cucumbers"),
     "Cucumber keeps about a week in the fridge, wrapped in a tea towel or a paper bag in the "
     "salad drawer: cling film traps the water and that is what makes it slimy. A soft one is "
     "still fine cooked, and the cut end dries first, so shave that off."),
    (("nuts", "walnuts", "almonds", "cashews", "peanuts", "pine nuts", "pecans"),
     "Nuts keep 3 to 6 months in an airtight jar in a cool cupboard and a year in the freezer; "
     "shelled or chopped ones go rancid sooner, and walnuts and pine nuts fastest. Taste one: a "
     "bitter or soapy taste means the oils have turned, and toasting hides it but does not fix it."),
    (("chocolate", "dark chocolate", "milk chocolate", "chocolate bar"),
     "Chocolate keeps about a year in a cool, dry cupboard, not the fridge, where condensation "
     "brings out a white bloom. The bloom is sugar or fat rather than mould, so it is still fine "
     "to eat; a bar that has been warm goes grey and grainy and is only good for melting."),
    (("bacon", "bacon rashers", "streaky bacon", "smoked bacon"),
     "Bacon keeps about a week in the fridge once the pack is open, sealed in a bag, and 3 "
     "months in the freezer, rashers separated with paper so you can take one at a time. It goes "
     "slimy and smells sharp when it is off; the cure keeps it pink long after that."),
    (("pasta", "dried pasta", "spaghetti", "penne", "macaroni", "fusilli"),
     "Dried pasta keeps about 2 years past the date on the packet in a sealed jar in a cupboard, "
     "and longer if it stays dry. Cooked pasta keeps 3 days in the fridge, tossed with a little "
     "oil so it does not clump, and reheats once in the sauce."),
    (("oats", "oat", "porridge oats", "rolled oats", "oat groats", "jumbo oats", "oatmeal",
      "oat bran", "porridge"),
     _oats_kept),
    (("overnight oats", "soaked oats", "bircher", "bircher muesli", "overnight porridge"),
     "Overnight oats keep 3 days in the fridge in a lidded jar, and they are better after the "
     "first night than they are after an hour: 40g of oats to about 100ml of milk or yoghurt, "
     "left covered overnight, keeps in the fridge for three breakfasts."),
    (("porridge", "cooked porridge", "oatmeal", "ready brek"),
     "Cooked porridge keeps 2 days in a lidded tub in the fridge: cool it quickly, then reheat it "
     "with a splash of milk or water and a stir, because cold porridge sets solid. Porridge left "
     "out on the side overnight goes in the bin."),
    (("cereal", "breakfast cereal", "cornflakes", "corn flakes", "muesli", "granola",
      "rice krispies", "weetabix"),
     "An opened box keeps 2 to 3 months in an airtight container and goes soft before it goes "
     "off, so taste rather than sniff it. The date on the box is for the sealed bag inside; "
     "stale cereal comes back crisp in a 150C oven for 5 minutes, spread out on a tray."),
    (("dried fruit", "sultanas", "raisins", "dried apricots", "dates", "prunes", "cranberries"),
     "Dried fruit keeps 6 months in a sealed jar and a year in the fridge, and past that it "
     "hardens rather than spoils. Bring it back in 10 minutes in a bowl of hot water, or leave a "
     "slice of bread in the jar overnight. White crystals on the outside are sugar, not mould."),
    (("guacamole", "guac", "avocado dip", "mashed avocado"),
     "Guacamole keeps 1 to 2 days in the fridge in a tub with cling film pressed right onto the "
     "surface, and the lime in it is what slows the browning. Brown on top is oxygen, not rot: "
     "stir it in and it is fine. After two days it tastes flat and watery, so eat it first."),
    (("mashed potato", "mashed potatoes", "mash", "leftover mash"),
     "Mashed potato keeps 2 days in the fridge, less than the potatoes it came from, because the "
     "butter and milk in it turn first. Warm it in a pan with a splash of milk over a low heat "
     "and stir, rather than in the microwave on high, which makes it gluey. It freezes for a "
     "month and comes back a little looser, so beat a knob of butter through it."),
    (("batter", "pancake batter", "crepe batter", "yorkshire pudding batter", "waffle batter"),
     "Batter keeps 1 to 2 days in the fridge in a jug with a lid, and stir it before it goes in "
     "the pan because the flour sinks. One with baking powder in it loses its lift after a day, "
     "so use it the same day for pancakes. Crepe batter is better after half an hour's rest, and "
     "a batter that smells sour or has grey on top goes down the sink."),
    (("quiche", "quiches", "a quiche", "leftover quiche", "savoury tart"),
     "Quiche keeps 3 days in the fridge, covered, and eat it cold or reheat it to piping hot all "
     "the way through rather than warm. A quiche freezes for 2 months, cut in slices and wrapped: "
     "thaw it in the fridge overnight and warm it through. Once the egg custard smells sour or "
     "the top has a sheen of water, it is done."),
    (("sausage rolls", "sausage roll", "leftover sausage rolls"),
     "Sausage rolls keep 2 days in the fridge, in a tub or a paper bag rather than cling film, or "
     "they go soft. Reheat them at 180C for 8 to 10 minutes to get the pastry crisp again, and "
     "eat them hot rather than warm. They freeze well for 2 months unbaked or baked, and the "
     "pastry is what goes first: a soggy bottom means it was wrapped while it was still warm."),
    (("smoked salmon", "smoked salmon slices", "lox"),
     "Smoked salmon keeps 3 days in the fridge once the pack is opened, wrapped tight, and it is "
     "cured rather than cooked so the date on the pack matters more than the days. It freezes for "
     "a month in portions, though the texture goes softer. Eat it within 24 hours once it is out "
     "on a plate, and bin it if it smells sharp or feels tacky."),
    (("coconut milk", "tinned coconut milk", "tin of coconut milk", "coconut cream"),
     "An opened tin of coconut milk keeps 4 to 5 days in the fridge in a tub or a jug, and the "
     "thick cream separates to the top, so stir it back in. An unopened tin keeps a year in the "
     "cupboard. Freeze what is left in an ice-cube tray and drop the cubes into a curry."),
    (("lemon curd", "curd", "homemade lemon curd"),
     "Lemon curd keeps 2 weeks in a jar in the fridge once it is opened, and homemade curd the "
     "same, though eat homemade within a week if you did not sterilise the jar. It freezes for 3 "
     "months and thaws in the fridge. Curd that has separated, or smells of nail varnish, goes "
     "in the bin - the egg in it is what spoils."),
)

PROBLEM_ONLY = ("soft", "gone soft", "bendy", "mouldy", "mould", "moldy", "dried out", "dry out",
                "wilt", "wilted", "limp", "rot", "rotten", "green", "greening", "sprout",
                "sprouts", "sprouting")

LONG_WORDS = ("how long", "how long does", "how long do", "how much longer", "keep for",
              "still ok", "still good", "ok to use", "ok to eat", "out of date", "use by",
              "past its date", "past its best",
              "the day after", "day after", "day later", "a day later", "the following day",
              "next day", "the next day", "day after that", "in the fridge", "out of the fridge")

KEEPING_KEY = tuple(word for word in KEEP_WORDS + LONG_WORDS if word not in PROBLEM_ONLY)

COOK_LINE_WORDS = ("cook", "cooking", "cooked through", "boil", "boiling", "minute", "minutes",
                   "al dente", "recipe", "recipes",
                   "take", "takes", "taking",
                   "simmer", "simmering", "simmered", "fry", "fries", "frying", "fried",
                   "roast", "roasting", "roasted", "bake", "baking", "baked", "grill",
                   "grilling", "grilled", "steam", "steaming", "steamed", "saute", "sauteed",
                   "stir fry", "stir frying", "air fryer", "hob", "sear", "searing",
                   "caramelise", "caramelize", "reduce it", "reduce the")

FOLLOW_UP_WORDS = ("it take", "it takes", "does it take", "that take", "will it take",
                   "long does it take", "long will it take", "how long does that take")

FLOP_WORDS = ("limp", "limpy", "wilted", "wilting", "soggy", "floppy", "gone soft", "sad")

_MUSH_VERDICT = ("A little slimy is still fine - it is water, not rot: wipe them and cook them "
                 "soon. A sour smell, brown patches or a sticky feel that stays after wiping means "
                 "bin them, because that is decay and no amount of cooking puts it right.")
_MUSH_FIX = ("A slimy mushroom is a wet one: they are about 90% water and a closed plastic bag "
             "traps the sweat that makes the surface slippery. Tip them into a paper bag in the "
             "fridge, wipe rather than wash them, and cook them soon in a hot dry pan.")
_EATING_WORDS = ("eat", "eaten", "ok", "okay", "safe", "still", "bin", "throw", "throwing",
                 "use", "useable", "usable", "edible", "bad", "off", "risky", "cook with")


def _slimy_mushrooms(memory, understood):
    said = " ".join(str((understood or {}).get(k) or "")
                    for k in ("clean", "norm_text", "text")).lower()
    if any(word in said for word in _EATING_WORDS):
        return _MUSH_VERDICT + " " + _MUSH_FIX
    return _MUSH_FIX + " " + _MUSH_VERDICT


FIX_FIRST = {
    "celery": "Limp celery comes back in 20 minutes in iced water, so shave the dry bottom off "
              "first: a head keeps 2 weeks wrapped in foil in the fridge, which keeps it crisp "
              "where a plastic bag turns it slimy.",
    "lettuce": "Plunge limp lettuce into iced water for 10 minutes and it comes back crisp; dry "
               "the leaves, wrap them in kitchen paper inside a bag in the salad drawer and they "
               "keep about a week. Dress them at the table, since wet leaves and early dressing "
               "are what wilted them in the first place.",
}

KEEP_NOT_MEDICINE = ("inhaler", "inhalers", "tablet", "tablets", "pill", "pills", "medicine",
                     "medicines", "medication", "medications", "prescription", "prescriptions",
                     "insulin", "epipen", "epi pen", "epipens", "eye drops", "eyedrops",
                     "antibiotic", "antibiotics", "paracetamol", "ibuprofen", "painkiller",
                     "painkillers", "calpol", "nurofen", "cough syrup", "antihistamine",
                     "antihistamines", "steroid", "steroids", "vaccine", "jab", "wound dressing",
                     "plasters", "bandage", "ointment", "eye ointment", "contact lens",
                     "contact lenses", "nose drops", "ear drops", "vitamin", "vitamins",
                     "supplement", "supplements", "test strip", "test strips")

KEEP_NOT_SLEEP = ("before bed", "before sleep", "before bedtime", "keep me awake",
                  "keeps me awake", "wake me up", "keeps me up", "last coffee", "last cup",
                  "stop drinking", "stop caffeine", "sleep better", "cant sleep", "can't sleep",
                  "to sleep", "fall asleep")

DISH_WORDS = ("soup", "soups", "stew", "stews", "broth", "broths", "chowder",
              "minestrone", "casserole", "casseroles", "tagine", "goulash")

GROWING_WORDS = ("slug", "slugs", "snail", "snails", "caterpillar", "caterpillars", "aphid",
                 "aphids", "greenfly", "blackfly", "whitefly", "pests", "pest", "eaten",
                 "eating my", "eating the", "ate my", "holes in", "nibbled", "infestation",
                 "allotment", "greenhouse", "raised bed", "vegetable patch", "veg patch",
                 "in the garden", "my garden", "growing", "grow", "sowed", "sow", "planted",
                 "seedling", "seedlings", "crop", "harvest")

FEEDING_WORDS = ("breastfeeding", "breast feeding", "breast-feeding", "nursing", "lactating",
                 "chestfeeding", "while im feeding")

_STAND_DOWN = (tuple(COOKED_WORDS) + USE_UP_WORDS + COOKING_WORDS + COOK_LINE_WORDS
               + KEEP_NOT_KEEPING + FOLLOW_UP_WORDS + KEEP_NOT_SLEEP + KEEP_NOT_MEDICINE
               + KEEP_QUALITY_WORDS + GROWING_WORDS + DISH_WORDS + FEEDING_WORDS)

CALENDAR_DATE = PACK_DATE + ("the date", "its date", "their date", "by date", "dates on",
                             "date said")

DATING_DATE = ("first date", "second date", "third date", "blind date", "date night",
               "on a date", "out on a date", "a date with", "date tomorrow", "the date went",
               "after a date", "calling after",
               "before texting", "after texting", "texting", "text her", "text him",
               "text them", "asking her out", "asking him out")

ROW_STAND_DOWN = {
    "smoked salmon": ("cooked", "bake", "baked", "roast", "roasted", "fillets"),
    "fruit": ("cake", "cakes", "juice", "smoothie", "dried", "tinned", "tin", "can", "jar", "jam",
              "wine", "crumble", "tart", "salad", "chutney", "yoghurt", "yogurt", "grapefruit",
              "pie", "pies", "pastry",
              "kiwi", "flies", "fly", "bowl", "tree", "trees", "grow", "growing", "plant",
              "plants", "pick", "picking", "ripen", "ripening", "ripe", "buying", "choose",
              "choosing", "healthy", "calories", "sugar", "portion", "portions"),
    "pasta": ("fridge", "refrigerator", "fridge freezer", "freezer", "frozen", "cold",
              "in the fridge", "left in the fridge",
              "stick", "sticks", "sticking", "stuck", "clump", "clumps", "clumping",
              "for tomorrow", "until tomorrow", "for the next day", "next day", "overnight",
              "ok tomorrow", "okay tomorrow", "still ok tomorrow", "tomorrow ok",
              "ok overnight", "okay overnight", "still ok overnight", "ok the next day",
              "okay the next day",
              "the day after", "day after", "a day after", "day later", "a day later",
              "the following day", "following day", "yesterday", "last night",
              "sauce", "pasta sauce", "tomato sauce", "marinara", "passata", "bolognese",
              "macaroni cheese", "mac and cheese", "mac n cheese", "cauliflower cheese",
              "cheese sauce", "pasta bake", "lasagne", "cannelloni"),
    "oats": ("to soak", "soak oats", "soaking oats", "soak them", "soaking oats", "oat milk",
             "oatmilk", "oat drink",
             "oat cakes", "oatcake", "oatcakes", "oat biscuits", "oat biscuit", "oat bars",
             "oat bar", "oat crackers", "flapjacks", "granola", "muesli", "oatly",
             "porridge pot", "porridge pots"),
    "overnight oats": ("to soak", "how long to soak", "soaking time"),
    "dried fruit": CALENDAR_DATE + DATING_DATE,
    "houmous": ("make", "making", "recipe", "recipes", "blend", "blitz", "healthy", "healthier",
                "calories", "protein", "good for you", "brown", "browns", "browning",
                "going brown", "stop it going brown", "thick", "thins", "watery", "lumpy",
                "dance", "dancing", "class", "classes", "swim", "swimming", "dip in",
                "dipped", "dipping", "what to dip", "with bread", "with carrots",
                "with crisps", "starter", "party"),
    "porridge": ("microwave", "microwaved", "simmer", "stir", "make", "how long to cook",
                 "how long do i cook"),
    "oil": ("oil change", "oil changes", "change the oil", "change my oil", "changing the oil",
            "between oil", "engine", "car", "cars", "van", "dipstick", "mot", "mileage",
            "garage", "mechanic", "gearbox"),
}

ROW_COOK_FORMS = {
    "oats": ("how do i cook", "how do you cook", "how long to cook", "how long do i cook",
             "how long should i cook", "cooking time", "cook for", "cook it", "boil", "boiling",
             "simmer", "simmering", "stirring", "microwave", "minute", "minutes", "take",
             "takes", "taking", "recipe", "recipes", "porridge oats to"),
    "guacamole": ("make", "making", "recipe", "recipes", "blend", "blitz", "mash it",
                  "dance", "dancing", "dip for", "what to dip"),
    "mashed potato": ("make", "making", "recipe", "recipes", "how do i make", "how to make",
                      "lumpy", "gluey", "butter", "cream in", "beat it",
                      "reheat", "reheats", "reheating", "reheated"),
    "batter": ("make", "making", "recipe", "recipes", "how do i make", "how to make",
               "thin", "thick", "lumpy", "mix", "whisk", "rest"),
    "lemon curd": ("make", "making", "recipe", "recipes", "how to make", "set", "setting",
                   "runny", "split", "why is my", "why did my"),
    "quiche": ("make", "making", "recipe", "recipes", "how do i make", "how to make", "bake",
               "baking", "oven", "pastry", "line the tin", "blind bake", "custard"),
    "sausage rolls": ("make", "making", "recipe", "recipes", "how do i make", "how to make",
                      "bake", "baking", "oven", "pastry", "puff", "rough puff"),
    "coconut milk": ("make", "making", "open", "opening", "shake", "separate", "separates",
                     "curdle", "curdles", "thick", "thin"),
}
COOKED_IN_THE_ROW = tuple(ROW_COOK_FORMS)

COOKED_VEG_NAMES = ("cooked vegetables", "cooked veg", "leftover vegetables", "leftover veg",
                    "left over vegetables", "left over veg", "roast vegetables", "roast veg",
                    "roasted vegetables", "roasted veg", "roast veggies", "cooked mushrooms",
                    "fried mushrooms", "cooked broccoli", "cooked cauliflower", "cooked carrots",
                    "cooked greens", "cooked cabbage", "cooked courgette", "cooked courgettes",
                    "cooked peppers", "stir fried vegetables", "stir fried veg")

COOKED_VEG_COOK_WORDS = ("how do i cook", "how do you cook", "how long to cook",
                         "how long do i cook", "how long should i cook", "cooking time",
                         "how do i roast", "how long do i roast", "how long in the oven",
                         "oven temperature", "what temperature", "how do i make",
                         "how do i fry", "how long to roast", "how long to boil",
                         "boil them", "boil it", "recipe", "recipes")

COOKED_VEG_REPLY = (
    "Cooked vegetables keep 3 days in the fridge in a covered box, and roast veg 3 to 4 days, "
    "because the oven has already taken the water out of them. Get them in there within 2 hours "
    "of coming off the heat, in a box rather than on a plate, and reheat once, piping hot. "
    "Cooked mushrooms and courgette go first, in 2 days, and anything slimy or sour goes in the "
    "bin, because the bugs that make you ill have no smell.")

KEEP_TECHNIQUE = ("keep warm", "keeps warm", "keeping warm", "keep it warm", "keep them warm",
                  "keep it hot", "keep them hot", "from sticking", "from going soggy",
                  "from drying", "drying out", "does not stick", "doesnt stick",
                  "moist", "juicy", "tender", "crisp", "crispy",
                  "warm", "hot", "sticking")

COOKED_VEG_STAND_DOWN = tuple(
    word for word in _STAND_DOWN
    if word not in COOKED_WORDS and word not in COOK_LINE_WORDS and word not in COOKING_WORDS)

_DAY_AFTER = ("the day after", "day after", "a day after", "day later", "a day later",
              "the following day", "following day", "the day later", "two days later",
              "2 days later", "the morning after")

_DAY_AFTER_FOODS = ("chicken", "rice", "prawn", "prawns", "ham", "beef", "pork", "lamb",
                    "fish", "salmon", "cod", "turkey", "mince", "curry", "stew", "soup",
                    "bolognese", "casserole", "noodles", "couscous", "quiche", "pizza",
                    "sausage", "sausages", "egg", "eggs", "beans", "lentils", "tofu",
                    "shepherds pie", "cottage pie", "lasagne", "leftovers", "leftover")

_DAY_AFTER_AVOID = ("workout", "work out", "training", "gym", "run", "running", "exercise",
                    "race", "match", "surgery", "operation", "dentist", "hospital", "vaccine",
                    "jab", "drinking", "drink", "hangover", "night out", "wedding", "funeral",
                    "flight", "interview", "exam", "period", "pill", "morning after pill",
                    "birth", "death", "died", "died", "holiday", "moving", "exam", "results")

FREEZE_WORDS = ("freeze", "freezes", "freezing", "freezer", "freezers", "frozen",
                "in the freezer", "in a freezer", "in my freezer", "put in the freezer",
                "put it in the freezer", "goes in the freezer", "go in the freezer")

FREEZE_SWEETS = (
    (("cheesecake", "cheesecakes", "baked cheesecake", "new york cheesecake",
      "no bake cheesecake"),
     "Yes, and a cheesecake freezes better than almost any other pudding: slice it first and "
     "wrap each slice, or double-wrap the whole tin, and it keeps 1 to 2 months. Thaw the slices "
     "in the fridge overnight rather than on the side, because a warm thaw makes the cheese weep."),
    (("birthday cake", "sponge cake", "sponge", "victoria sponge", "victoria sandwich",
      "madeira cake", "layer cake", "cake", "cakes"),
     "Yes: cool it completely, leave the icing off, wrap the sponge in two layers and it keeps "
     "2 to 3 months. Thaw it still wrapped in the fridge overnight, then ice it, because a cake "
     "iced before it goes in comes out with the icing stuck to the paper."),
    (("trifle", "trifles"),
     "No, and this is the pudding to eat fresh: jelly weeps, cream splits and the sponge goes "
     "soggy as it thaws, so what comes out is watery at the bottom and grainy on top. Make it the "
     "day before at most and keep it in the fridge."),
    (("panna cotta", "panna cottas"),
     "No: the gelatine weeps as it thaws and the cream sets grainy, so a frozen one never comes "
     "back to that just-set wobble. Make it the day before and keep it in the fridge, where it "
     "holds 2 to 3 days."),
    (("tiramisu", "tiramisus"),
     "It freezes, though it is better fresh: cover the dish and it keeps up to 2 months, then "
     "thaw it in the fridge overnight. Expect the sponge to come back a little wetter and dust "
     "the cocoa on after it thaws, not before."),
    (("custard", "home made custard", "custard sauce"),
     "Yes, in portions for up to 3 months, and cornflour in it is what makes it survive: a plain "
     "egg custard can look watery or grainy once thawed. Thaw it in the fridge and then warm it "
     "gently in a pan, whisking, rather than in the microwave, which splits it."),
    (("chocolate mousse", "mousse", "mousses", "lemon mousse", "chocolate pot",
      "chocolate pots"),
     "Yes, up to 2 months: freeze it in the pots or in a tub with the surface pressed flat, and "
     "thaw it in the fridge for a few hours. A mousse weeps a little as it thaws, so stir it "
     "through before you serve it and nobody can tell."),
    (("milk", "a pint of milk", "semi skimmed milk", "skimmed milk", "whole milk",
      "breast milk", "formula", "goats milk"),
     "Yes, and it keeps about a month in the freezer: pour off a little first, because milk "
     "expands and splits the bottle. Thaw it in the fridge and shake it well, since the fat and "
     "water separate; it is fine for cooking and on cereal, a bit thinner to drink."),
)

FREEZE_SWEET_NAMES = tuple(name for names, _ in FREEZE_SWEETS for name in names)

FREEZE_SWEET_AVOID = ("recipe", "recipes", "how do i make", "how to make", "homemade",
                      "from scratch", "how do i cook", "how long to bake", "cooking time",
                      "healthy", "unhealthy", "fattening", "calories", "good for you",
                      "pregnant", "pregnancy", "breastfeeding", "nursing", "weaning",
                      "allergy", "allergic", "lactose", "how much milk", "ounces",
                      "keep", "keeps", "keeping", "last", "lasts", "use by",
                      "out of date", "past the date", "still ok", "still good",
                      "defrost", "thaw", "thawed", "thawing", "refreeze",
                      "ice cream", "ice lolly", "ice lollies",
                      "power cut", "broken", "stopped working", "left out", "out of the freezer")


def _freeze_a_sweet(memory, understood):
    said = " " + str((understood or {}).get("clean")
                      or (understood or {}).get("text") or "").lower() + " "
    best = None
    for names, reply in FREEZE_SWEETS:
        for name in names:
            if " %s " % name in said or said.startswith(name + " "):
                if best is None or len(name) > best[0]:
                    best = (len(name), reply)
                break
    return best[1] if best else None


_DAY_AFTER_ENTRY = entry("keep-the-day-after", (_DAY_AFTER_FOODS, _DAY_AFTER),
          "Cooled within two hours and put straight in the fridge, cooked chicken, meat, fish and "
          "pasta keep two days and cooked rice one, and that is the whole rule - the date on the "
          "pack does not stretch it. After that it is a reheat question rather than a keep one: "
          "reheat it once, all the way through, until it is steaming hot, and never reheat rice "
          "twice. Bin anything that smells, feels slimy or was left out overnight.",
          avoid=_DAY_AFTER_AVOID, bias=1)

PASTA_SAUCE_WORDS = ("pasta sauce", "tomato sauce", "sauce for pasta", "marinara", "passata",
                     "bolognese sauce", "pasta sauce jar", "jar of pasta sauce", "chilli sauce",
                     "tomato and basil sauce", "arrabbiata")
SAUCE_KEEPING_WORDS = ("keep", "keeps", "keeping", "kept", "store", "stores", "storing", "stored",
                       "last", "lasts", "lasting", "how long", "still ok", "still good",
                       "gone off", "go off", "off yet", "next day", "the day after", "tomorrow",
                       "open jar", "opened", "once opened", "leftover", "left over", "batch",
                       "in the fridge", "out of date", "use by",
                       "freeze", "freezes", "freezing", "freezer", "freezers", "frozen")


def _pasta_sauce_keep(memory, understood):
    line = " " + (understood.get("clean") or "") + " "
    if any(word in line for word in (" freeze", " freezer", " frozen", " freezing")):
        return ("Sauce freezes well: cool it quickly, then freeze it in meal-sized portions for "
                "about 3 months, and reheat it once until it is steaming hot. A jar of sauce keeps "
                "5 days in the fridge once it is opened, and sauce you made keeps 3 to 4 days - so "
                "if there is more than you will use, the freezer is the better place for it.")
    if any(word in line for word in (" carton", " cartons", " tub", " fresh pasta sauce",
                                     " chilled sauce", " fresh sauce")):
        return ("A fresh or chilled carton of pasta sauce keeps 3 to 4 days in the fridge once it "
                "is opened, and it is worth transferring it out of the carton into a tub with a "
                "lid. It freezes well in portions for about 3 months; reheat it once, until it is "
                "steaming hot, and bin it if it smells sour or has mould on the surface.")
    if any(word in line for word in (" homemade", " made it", " made my own", " made this",
                                     " batch", " i made", " my own sauce", " left over from",
                                     " from scratch")):
        return ("Sauce you made keeps 3 to 4 days in the fridge in a lidded tub, or 3 months in "
                "the freezer in portions, and it is better for being cooled quickly and put away "
                "while it is still warm rather than left out. Reheat it once, all the way through, "
                "and bin it if it smells sour, fizzes or has mould on top.")
    return ("A jar of pasta sauce keeps 5 days in the fridge once it is opened, with the lid back "
            "on, and until the date on the jar while it is still sealed: the label's use-by is for "
            "the sealed jar, not for the open one. Sauce you made yourself keeps 3 to 4 days, and "
            "either freezes for about 3 months in portions - reheat it once, all the way through.")




DATES_OWN = entry(
    "keep-dates-own",
    (("eat dates", "dates past", "dates after", "dates last", "store dates", "dates keep",
      "dates go off", "do dates go off", "how long do dates"),
     ("past the date", "past its date", "past their date", "after the date", "out of date",
      "use them up")),
    "Dates keep 6 months in a sealed jar and a year in the fridge, and past the date on the pack "
    "they harden rather than spoil: the soft medjool in a tub go first, and the dry baking ones "
    "last longest. Ten minutes in a bowl of hot water brings a hard one back. White crystals on "
    "the outside are sugar, not mould.",
    bias=1,
    avoid=("use by", "best before", "sell by", "expiry", "expires", "expired", "date on"),
)

YOGHURT = entry(
    "keep-yoghurt",
    (("yoghurt", "yogurt", "greek yoghurt", "greek yogurt", "natural yoghurt", "natural yogurt",
      "plain yoghurt", "plain yogurt"), KEEPING_KEY),
    "An unopened tub keeps about a week past the date on the lid, and once a spoon has been in it "
    "keep it 3 to 5 days - the date is for the sealed pot. Plain yoghurt "
    "that has separated with a little water on top is fine - stir it back in. Bin it if there is "
    "mould on the surface, or if it smells sour or fizzy rather than tangy.",
    bias=2,
    ask=KEEPING_KEY,
    avoid=("go off", "goes off", "gone off", "off", "smell", "smells", "smelly", "sour",
           "mould", "mouldy", "mold", "moldy", "fizzy", "safe", "separated", "separation",
           "separating", "watery", "water on top", "curdled", "lumpy", "runny"),
)

DATE_ASK = ("past the date", "past its date", "past their date", "after the date", "out of date",
            "use by", "use by date", "best before", "ok to eat", "safe to eat", "eat it",
            "eat them", "still ok", "still good")

DATE_ROWS = [
    (("spinach", "baby spinach", "bag of spinach", "spinach leaves"),
     "A bag of spinach keeps about 5 days in the salad drawer and a whole unopened bag a week "
     "longer, and the date on the bag is the day to finish it by rather than a day it is still "
     "good after. Pick out anything slimy before it spreads, don't wash the leaves until you use "
     "them, and a bag that has only gone limp is fine wilted into a curry or an omelette."),
    (("rice", "white rice", "basmati rice", "long grain rice", "brown rice"),
     "Dry rice keeps for years in a sealed jar in a cupboard, and the date on the bag is a "
     "best-before rather than a use-by. Cooked rice is the one to be strict about: cool it within "
     "an hour, box it, and keep it no more than 24 hours in the fridge - reheating does not kill "
     "the spores that grow in rice left warm."),
    (("guacamole", "taramasalata", "tarama", "tzatziki", "soured cream dip", "onion dip"),
     "Once opened, a tub of tzatziki or taramasalata keeps about 3 days in the fridge and "
     "guacamole a day or two, because avocado browns and sours fastest: the date on the lid is for "
     "the sealed pot, so judge it by look and smell after that. Press cling film down onto "
     "guacamole to keep the air off it, keep all of them cold, and bin anything that smells sour, "
     "fizzes or has mould.",
     ("next day", "the next day")),
    (("hummus", "houmous", "humous"),
     "Hummus keeps about a week in the fridge in a sealed tub, and 3 to 4 days once a spoon has "
     "been in it: the date on the lid is for the sealed pot, so a couple of days past it is usually "
     "fine. A film of water on top is normal, so stir it in. Bin it if it smells sour or fizzy, or "
     "if there is mould.",
     ("next day", "the next day")),
]

STORECUPBOARD_KEEP = (
    (("soy sauce", "light soy", "dark soy", "shoyu"),
     "Soy sauce keeps for years in the cupboard, and about a year once it is opened, because the "
     "salt stops anything growing in it. It darkens and a salt crust can form at the neck, and "
     "neither is spoilage; bin it only if it smells sour or has a film on top."),
    (("vinegar", "malt vinegar", "white vinegar", "balsamic", "cider vinegar", "wine vinegar"),
     "Vinegar does not go off: it keeps for years, opened or not, because it is already acid. A "
     "cloudy stringy blob in the bottle is the mother, which is harmless - strain it out and carry "
     "on - and a weaker taste after a couple of years is the only thing that changes."),
    (("tea", "tea bags", "teabags", "tea bag", "loose leaf", "green tea", "earl grey",
      "pg tips", "chamomile tea", "peppermint tea"),
     "Tea does not go off, it goes stale: about six months past the date in a sealed tin, and a "
     "year for loose leaf, after which the flavour fades rather than spoils. Keep it in a tin away "
     "from the light and the kettle's steam, and it is safe to drink long after it has lost its "
     "best."),
    (("peanut butter", "peanut butter jar", "nut butter", "almond butter"),
     "An opened jar of peanut butter keeps about three months in the cupboard, or six in the fridge "
     "if you want it to last. The oil that separates on top is normal - stir it back in rather than "
     "pouring it off - and the sign to bin it is a smell of paint or old oil, which is the nuts "
     "going rancid.",
     "Peanut butter freezes well: a jar keeps about six months in the freezer and thaws overnight "
     "in the fridge, though it may need stirring again afterwards."),
    (("ham", "sliced ham", "cooked ham", "wafer thin ham", "honey roast ham"),
     "An opened pack of cooked ham keeps two to three days in the fridge, sealed in a box, and the "
     "use-by date on the pack only holds while it is unopened. It should feel dry and smell of "
     "nothing much; sliminess or a sour smell means bin it, and do not re-wrap it and hope.",
     "Cooked ham freezes for about one to two months: wrap it in portions, because it goes watery "
     "and salty once thawed and will not slice thin again. Thaw it in the fridge overnight and use "
     "it in a cooked dish rather than a sandwich."),
    (("ketchup", "tomato ketchup", "brown sauce", "hp sauce"),
     "Opened ketchup keeps about a month in the cupboard and six months in the fridge, and the date "
     "on the bottle only counts while it is sealed. A dark colour or a little watery liquid is "
     "normal; a fizzy smell or mould at the neck means bin it."),
    (("marmite", "vegemite", "bovril"),
     "Marmite keeps for years - a couple of years past the date, easy - because it is salty and "
     "dark and nothing grows in it. It can dry out and go stiff in the jar; a spoonful of hot water "
     "stirred in brings it back, and it is safe to finish either way."),
    (("golden syrup", "treacle", "black treacle", "maple syrup"),
     "Golden syrup and treacle keep for years in the cupboard, and black treacle improves for the "
     "first year. Maple syrup is the one that needs the fridge once opened, about six months, and "
     "it is the only one here that can grow mould on top."),
    (("worcestershire sauce", "worcester sauce", "tabasco", "hot sauce", "chilli sauce",
      "sriracha", "franks"),
     "Worcestershire sauce and vinegar-based hot sauces keep for years in the cupboard, and about a "
     "year once opened; a hot sauce can darken and thicken, which is fine. The ones to refrigerate "
     "are the fresh chilli sauces and anything with fruit in it, which keep about three months."),
    (("salt", "table salt", "sea salt", "rock salt"),
     "Salt does not go off at all: it is a mineral and nothing grows in it, so the date means "
     "nothing. It clumps in damp air - a few grains of rice in the cellar, or a quick dry in a warm "
     "oven - and that is the only thing that changes."),
    (("baking powder", "bicarbonate of soda", "bicarb", "baking soda"),
     "Baking powder keeps about six months once the tin is opened, and bicarbonate of soda about a "
     "year, because they lose their fizz rather than spoil. Test it: a teaspoon in a cup of hot "
     "water should foam at once, and if it does not, the cake will not rise."),
    (("cornflour", "corn flour", "custard powder"),
     "Cornflour keeps about a year in a sealed tub in the cupboard, and custard powder about six "
     "months once opened, because both take up damp and go lumpy. It does not go mouldy or unsafe - "
     "it stops thickening properly, which is the sign to replace it."),
    (("ice cream", "ice cream tub", "vanilla ice cream", "gelato", "sorbet"),
     "Ice cream keeps about two to three months in the freezer before it dries out and goes icy, "
     "though it is safe far longer. Press a sheet of cling film onto the surface or keep the "
     "cardboard lid tight, and do not refreeze a tub that has melted, because that is when it turns "
     "grainy and grows ice crystals."),
)

SC_KEEP_ASKS = ("keep", "keeps", "keeping", "kept", "last", "lasts", "lasting", "go off",
                "goes off", "gone off", "going off", "how long", "store", "stores", "stored",
                "storing", "storage", "out of date", "past its date", "past its best",
                "use by", "still good", "still ok", "still safe", "shelf life", "expire",
                "expires", "expired",
                "in the fridge", "in the cupboard", "in a cupboard", "need to be in the fridge",
                "need to be refrigerated", "refrigerate", "refrigerated",
                "gone hard", "going hard", "gone stiff",
                "stale", "stales", "gone stale", "goes stale", "going stale", "went stale")

_LAST_TIME = ("last week", "last night", "last time", "last month", "last year", "last summer",
              "last winter", "last spring", "last autumn", "last fall", "last christmas",
              "last easter", "last weekend", "last sunday", "last monday",
              "last tuesday", "last wednesday", "last thursday", "last friday", "last saturday")

_CLEANING_WITH_IT = ("wash", "washing", "washed", "washing machine", "dishwasher",
                     "smell", "smells", "smelly", "smelled", "stink", "stinks", "stinking",
                     "odour", "odor", "musty", "limescale", "hard water")

SC_KEEP_AVOID = _LAST_TIME + _CLEANING_WITH_IT + (
                 "recipe", "recipes", "make", "making", "homemade", "from scratch",
                 "how do i make",
                 "how do i cook", "how much", "per person", "calories", "good for you", "healthy",
                 "diet", "marinade", "marinate", "substitute", "instead of", "brand", "cheapest",
                 "buy", "price", "offer", "clean", "cleaning", "descale", "kettle", "sink",
                 "drain", "wasp", "ant", "weed", "pickle", "pickling", "chutney",
                 "left out", "leave it out", "left on the side", "sitting out", "out of the fridge",
                 "defrost", "thaw", "thawed", "refreeze", "re-freeze",
                 "brew", "brewing", "brew it", "steep", "steeping", "steeped", "mash",
                 "tea bag in", "teabag in", "the bag in", "leave the bag", "leaving the bag",
                 "cuppa", "milk in first", "teapot",
                 "infuse", "infusing",
                 "cool", "cooling", "cool down", "cools down", "too hot to drink",
                 "how long for", "how many minutes",
                 "cook", "cooking", "roast", "roasting", "boil", "boiling", "joint", "gammon",
                 "take to cook", "how long to cook", "in the oven", "air fryer", "slow cooker",
                 "dog", "dogs", "puppy", "pups", "cat", "cats", "kitten", "kittens",
                 "rabbit", "rabbits", "hamster", "hamsters", "budgie", "budgies",
                 "guinea pig", "guinea pigs", "pet", "pets", "vet")


def _storecupboard_keep(memory, understood):
    said = " " + str((understood or {}).get("clean")
                     or (understood or {}).get("text") or "").lower() + " "
    frozen = any(word in said for word in ("freezer", "freeze", "frozen", "defrost", "thaw"))
    best = None
    for row in STORECUPBOARD_KEEP:
        names, reply = row[0], row[1]
        if frozen and len(row) > 2:
            reply = row[2]
        for name in names:
            if " %s " % name in said or said.startswith(name + " "):
                if best is None or len(name) > best[0]:
                    best = (len(name), reply)
                break
    if best:
        return best[1]
    return ("Most of these keep far longer than the date on the packet: soy sauce and vinegar for "
            "years, tea for about six months past its date, and an opened jar of peanut butter for "
            "about three months. The date is a quality date on most of them, not a safety one.")


SC_KEEP_NAMES = tuple(name for row in STORECUPBOARD_KEEP for name in row[0])

DATED_STAND_DOWN = {
    "rice": ("leftover", "leftovers", "left over", "reheat", "reheated", "reheating",
             "next day", "the next day", "the day after", "day after", "day later",
             "days later", "yesterday", "in the fridge", "out of the fridge", "takeaway"),
}


def _kept_a_while(reading):
    return bool(reading.get("kept"))


def _dated_row(row):
    names, reply = row[0], row[1]
    asks = DATE_ASK + tuple(row[2] if len(row) > 2 else ())
    return entry("keep-%s-dated" % names[0], (names, asks), reply, bias=1,
                 avoid=DATED_STAND_DOWN.get(names[0], ()),
                 guard=lambda reading: not _kept_a_while(reading))


ENTRIES = [_DAY_AFTER_ENTRY, DATES_OWN, YOGHURT] + [
    _dated_row(row) for row in DATE_ROWS
] + [
    entry("keep-cooked-veg", (COOKED_VEG_NAMES, KEEPING_KEY), COOKED_VEG_REPLY, bias=1,
          avoid=COOKED_VEG_STAND_DOWN + COOKED_VEG_COOK_WORDS + USE_UP_WORDS + FLOP_WORDS
          + KEEP_TECHNIQUE),
] + [
    entry("keep-%s" % names[0], (names, KEEPING_KEY), reply, bias=1,
          avoid=(tuple(word for word in _STAND_DOWN
                       if not (names[0] in COOKED_IN_THE_ROW
                               and (word in COOKED_WORDS
                                    or word in COOK_LINE_WORDS)))
                 + ROW_COOK_FORMS.get(names[0], ())
                 + FLOP_WORDS + KEEP_TECHNIQUE + ROW_STAND_DOWN.get(names[0], ())))
    for names, reply in ROWS
] + [
    entry("keep-%s-limp" % names[0], (names, FLOP_WORDS), FIX_FIRST[names[0]],
          bias=2, ask=FLOP_WORDS, avoid=_STAND_DOWN)
    for names, _reply in ROWS if names[0] in FIX_FIRST
] + [
    entry("keep-mushroom-slimy",
          (("slimy", "slimey", "slimier", "slimiest", "soggy", "sweaty", "wet"),
           ("mushroom", "mushrooms", "button mushrooms", "chestnut mushrooms", "closed cup",
            "portobello", "shiitake")),
          _slimy_mushrooms,
          bias=2,
          avoid=("wash", "washing", "washed", "recipe", "recipes", "sauce", "soup", "risotto",
                 "pizza", "lasagne", "stew", "pie", "curry", "pickle", "dry", "dried",
                 "grow", "growing", "forage", "foraging", "magic")),
    entry("guacamole-browns",
          (("guacamole", "guac", "avocado dip", "avocado mash"),
           ("brown", "browns", "browning", "going brown", "goes brown", "go brown",
            "green", "stay green", "keep green", "fresh", "stop", "prevent", "why")),
          "It is the air, not the lime: a cut avocado browns where oxygen reaches it, and the "
          "greenest guacamole is the one with the least air in it. Press cling film right onto "
          "the surface in a shallow tub, keep the stones in if you like, and a squeeze of lime "
          "plus a pinch of salt slows it. If it has already browned it is still fine to eat - "
          "stir the top layer in and it looks green again.",
          bias=2,
          avoid=("has gone", "have gone", "went", "turned", "recipe", "recipes", "make",
                 "making", "freeze", "frozen", "calories", "how much")),
]

CUT_WORDS = ("power cut", "power cuts", "power went off", "power goes off", "power has gone off",
             "power is off", "power was off", "power failure", "power outage", "power out",
             "lost power", "lose power", "losing power", "no power", "without power",
             "electricity went off", "electricity was off", "electricity is off", "no electricity",
             "without electricity", "lost the electricity", "freezer went off", "freezer was off",
             "freezer is off", "freezer has been off", "cut out", "cut off",
             "power goes", "power go", "power went", "power came back", "power is back",
             "when the power goes", "if the power goes", "if the power cuts")

CUT_OUT_FOR = re.compile(r"\bcut out (?:for|to)\b", re.I)


def _cut_out_for_is_an_aptitude(understood):
    said = str((understood or {}).get("clean") or (understood or {}).get("norm_text") or "")
    return bool(CUT_OUT_FOR.search(said))


WHEN_WORDS = ("last night", "yesterday", "overnight", "this morning", "today", "hours", "hour",
              "day", "days", "two days", "3 days", "four hours", "6 hours", "since", "meanwhile",
              "still", "think", "worried", "safe", "ok", "fine", "food", "freezer", "fridge",
              "shut", "closed", "opened", "cold")

THAW_WORDS = ("thawed out", "thawed", "thaw", "thawing", "defrosted out", "defrosted",
              "defrost", "defrosting", "melted out", "melted",
              "unfrozen", "no longer frozen",
              "gone soft in the freezer", "soggy in the freezer", "soggy from the freezer",
              "soggy out of the freezer", "soggy after the freezer")

REFREEZE_WORDS = ("refreeze", "refrozen", "refroze", "re-freeze", "re freeze", "refreezing",
                  "put it back in the freezer", "back in the freezer", "freeze it again")

TIMES_A_THAW = re.compile(r"\b(?:defrost|thaw)\w*\b", re.I)
ASKS_HOW_LONG = re.compile(r"\bhow (?:long|many (?:hours|minutes|days)|soon)\b", re.I)


def _a_thaw_that_is_a_job(understood):
    said = str((understood or {}).get("clean") or (understood or {}).get("norm_text") or "")
    if not TIMES_A_THAW.search(said):
        return False
    return bool(ASKS_HOW_LONG.search(said))



COLD_NOT = ("tariff", "economy 7", "economy seven", "night rate", "day rate", "bill", "bills",
            "supplier", "suppliers", "standing charge", "direct debit", "kwh", "unit rate",
            "cheaper", "cheapest", "worth it", "should i buy", "buy a freezer", "chest or upright",
            "chest freezer or", "upright", "running cost", "energy use", "how much electricity",
            "switch", "solar", "battery", "generator", "camping",
            "pregnant", "pregnancy", "trimester", "weeks pregnant")

COLD_REPLIES = {
    "cut": "Keep the doors shut and most of it is fine: a full freezer holds its cold for about "
           "48 hours, a half-full one about 24, and a fridge about 4. Do not open them to look - "
           "that is what lets the cold out. When the power is back, cook and eat the thawing "
           "things first and leave the rest frozen.",
    "thawed": "Judge it on ice crystals rather than on how long it sat: food that is still firm "
              "and icy can be cooked and eaten or refrozen, and meat that thawed in the fridge can "
              "always go back in. Anything soft and warm goes in the bin - meat, fish, shellfish, "
              "cooked rice and milk most of all - and do not taste it to check. Melted ice cream "
              "is binned whatever it feels like.",
    "fridge": "Food in a fridge whose door stayed shut is safe for about 4 hours, and after that "
              "the perishables go: milk, soft cheese, cooked meat, cooked rice and leftovers, "
              "and anything past its date. Butter, hard cheese, jam, pickles and most fruit and "
              "veg come through a warm day, so a full clear-out is not needed.",
    "icecream": "It is safe but it will be grainy: melting and refreezing separates the ice cream, "
                "so it goes icy and slushy rather than creamy. Eat it now rather than keep it. If "
                "the tub was actually warm for hours, bin it - dairy that has been warm is not "
                "worth the risk.",
}

CHEESE_NAMES = ("cheddar", "parmesan", "brie", "camembert", "feta", "stilton", "mozzarella",
                "gruyere", "gorgonzola", "blue cheese", "goats cheese", "goat cheese",
                "cream cheese", "cottage cheese", "halloumi", "red leicester", "wensleydale")
STORE_ASKS = ("store", "stores", "storing", "stored", "how do i store", "how should i store",
              "how to store", "how do you store", "best way to store", "where do i keep",
              "where should i keep", "wrap", "wrapped", "wrapping", "once opened")
MOULD_WORDS = ("mould", "mouldy", "mold", "moldy", "moulds", "fuzzy", "furry", "gone mouldy",
               "green bits", "white bits", "spots", "speckled", "fur",
               "blue bits", "blue spots", "blue spot", "bits of blue")

SOFT_CHEESES = ("cream cheese", "cottage cheese", "brie", "camembert", "mozzarella", "feta",
                "goat cheese", "goats cheese", "mascarpone", "ricotta")
BLUE_CHEESES = ("blue cheese", "stilton", "gorgonzola", "roquefort", "dolcelatte")


def _cheese_mould(memory, reading):
    said = (reading or {}).get("clean") or ""
    words = " %s " % said.lower()
    for name in BLUE_CHEESES:
        if name in words:
            return ("The blue in %s is meant to be there. Green or white fuzz on it is not, so a "
                    "blue cheese that has grown it goes in the bin." % name)
    for name in SOFT_CHEESES:
        if name in words:
            return ("Mould on %s means the whole piece goes in the bin: the threads run all the "
                    "way through a soft cheese, so there is nothing to cut back to." % name)
    return ("Cut the mould off hard cheese an inch past it and the rest is fine. Soft cheese, "
            "cream cheese and anything already grated or sliced goes in the bin, because the "
            "threads reach further than you can see.")

ENTRIES += [
    entry("cold-cut", (CUT_WORDS, WHEN_WORDS), COLD_REPLIES["cut"], bias=2, ask=CUT_WORDS,
          guard=lambda understood: not _cut_out_for_is_an_aptitude(understood),
          avoid=COLD_NOT),
    entry("cold-thawed", (THAW_WORDS, WHEN_WORDS + ("meat", "chicken", "food", "freezer")),
          COLD_REPLIES["thawed"], bias=5, ask=THAW_WORDS,
          guard=lambda understood: not _a_thaw_that_is_a_job(understood),
          avoid=COLD_NOT + ("how do i defrost", "how to defrost", "how do you defrost",
                            "how can i defrost", "defrost my freezer", "defrost the freezer",
                            "defrost a freezer", "defrosting a freezer", "best way to defrost",
                            "way to defrost",
                            "needs defrosting", "needs a defrost", "frosting up", "should i defrost",
                            "shall i defrost", "do i defrost it", "defrost it now")
          + REFREEZE_WORDS + ("again", "second time")),
    entry("soggy-from-the-freezer", (("soggy", "soggyish", "mushy"),
                                     ("frozen", "freezer", "froze", "ice", "icy", "ice crystals")),
          COLD_REPLIES["thawed"], bias=4, ask=("soggy", "mushy"),
          avoid=("pan", "salad", "batter", "breaded", "sauce", "risotto", "soup", "chips",
                 "fries", "roast", "cooked")),
    entry("cold-kept-shut", (("freezer", "fridge", "food"),
                             ("stayed shut", "kept it shut", "kept the door shut", "didnt open",
                              "did not open", "stayed closed", "not opened", "still cold",
                              "still frozen")),
          COLD_REPLIES["cut"], bias=4,
          ask=("stayed shut", "kept it shut", "kept the door shut", "didnt open", "did not open",
               "stayed closed", "not opened"),
          avoid=COLD_NOT + ("wont stay shut", "wont shut", "wont close", "will not stay shut",
                            "will not shut", "will not close", "keeps opening", "pops open",
                            "keeps popping open", "door gap", "not shutting properly")),
    entry("cold-door-open",
          (("freezer", "fridge", "freezer door", "fridge door"),
           ("door", "left open", "left it open", "left the door open", "was left open",
            "got left open", "door was open", "door open", "open all night", "open overnight",
            "open all day", "ajar", "didnt shut", "did not shut",
            "didnt close", "not closed properly", "stayed open", "open for hours",
            "left ajar")),
          ("Check for ice crystals rather than counting the hours: anything still firm and icy "
           "can be cooked and eaten or put back, and nothing needs binning for the door alone. "
           "What went soft and warm goes in the bin - meat, fish, shellfish, cooked rice and milk "
           "most of all - and do not taste it to check. A fridge is the stricter one: milk, cooked "
           "meat, cooked rice and leftovers go if the door was open for more than about four "
           "hours, while butter, hard cheese, jam and pickles come through it. Melting ice cream "
           "is binned whatever it feels like, and a freezer that was open all night is worth "
           "running for an hour before you trust the ice."),
          bias=3,
          ask=("left open", "left it open", "left the door open", "was left open",
               "got left open", "door was open", "door open", "open all night", "open overnight",
               "ajar", "didnt shut", "did not shut", "stayed open"),
          avoid=COLD_NOT + ("seal", "seals", "gasket", "thermostat", "temperature setting",
                            "too cold", "not cold enough", "frost", "freezing up", "ice box",
                            "how do i defrost", "how to defrost", "defrost my freezer",
                            "defrost the freezer")
          + REFREEZE_WORDS),
    entry("cold-clear-out", (("freezer", "fridge freezer"),
                             ("everything", "all of it", "throw out", "throw away", "bin it all",
                              "clear out", "chuck out", "whole lot")),
          COLD_REPLIES["thawed"], bias=3,
          ask=("throw out", "throw away", "bin it all", "bin everything", "clear out",
               "chuck out", "should i bin"), avoid=COLD_NOT),
    entry("cold-fridge", (("fridge was off", "fridge is off", "fridge has been off",
                           "fridge went off", "fridge was warm", "fridge has been warm",
                           "fridge is warm", "fridge off", "fridge"),
                          WHEN_WORDS + ("off", "warm", "warmth", "all day", "hours")),
          COLD_REPLIES["fridge"], bias=5, ask=CUT_WORDS + ("fridge was off", "fridge is off",
                                                           "fridge went off", "fridge off",
                                                           "warm fridge", "fridge warm"),
          avoid=COLD_NOT + ("fridge freezer",)),
    entry("cold-ice-cream", (("ice cream", "icecream", "ice lolly", "ice lollies", "gelato",
                              "frozen yogurt"),
                             THAW_WORDS + REFREEZE_WORDS + ("ok", "safe", "still", "bin")),
          COLD_REPLIES["icecream"], bias=4,
          ask=("ice cream", "icecream", "ice lolly", "ice lollies", "gelato"), avoid=COLD_NOT),
]


UNDER_RIPE = ("green", "still green", "too green", "very green", "so green", "green as",
              "not ripened", "hasnt ripened", "hasn't ripened", "didnt ripen", "didn't ripen",
              "wont ripen", "refusing to ripen")
RIPEN_WORDS = UNDER_RIPE + (
               "ripe", "riper", "ripen", "ripens", "ripening", "unripe", "underripe",
               "overripe", "hard", "firm", "still hard", "ready", "ready to eat",
               "soft enough", "tell if", "know if", "how do i tell", "how can i tell",
               "when is it ready", "sweet enough",
               "softer", "soften", "sour", "not ripe", "too hard", "rock hard", "tasteless",
               "soft", "squishy", "soft at the bottom", "soft on the bottom", "gone soft",
               "getting soft",
               "pick a good", "pick good", "picking a good", "pick the best", "pick a ripe",
               "pick ripe", "choose a good", "choosing a good", "choose the best",
               "choose a ripe", "choosing a ripe", "good one", "good ones", "best one",
               "how do i pick", "how do i choose", "how to pick", "how to choose",
               "which one to pick", "which one to choose", "which to pick", "which to choose",
               "pick one", "choose one")

RIPEN_TABLE = (
    (("mango", "mangoes", "mangos"),
     "A ripe mango gives slightly under a gentle press, like a ripe peach, and smells sweet at "
     "the stem end; the red blush says nothing, so a green one can still be ready.",
     "A hard one ripens on the counter in 2 to 4 days, faster in a paper bag with a banana, "
     "since the banana gives off the gas that does the work.",
     "Once it gives, it keeps about 5 days in the fridge, and a cut mango keeps 3 days in a "
     "sealed tub."),
    (("melon", "melons", "cantaloupe", "honeydew", "galia"),
     "A ripe melon feels heavy for its size, and the end opposite the stem gives a little under "
     "your thumb; a cantaloupe smells sweet there too.",
     "A whole one softens on the counter in 2 or 3 days, quicker in a paper bag, but once it is "
     "cut it will not ripen any further.",
     "Wrap cut melon and keep it 3 days in the fridge; a whole ripe one keeps about a week there."),
    (("watermelon", "watermelons"),
     "A ripe watermelon is heavy for its size, has a creamy yellow patch where it lay on the "
     "ground, and gives a hollow thud when you tap it.",
     "It will not ripen once it is off the vine, so a pale one stays pale and the only thing to "
     "do is keep it cool and eat it.",
     "Whole, it keeps a week or two in a cool room, and cut watermelon keeps 3 days in the "
     "fridge in a sealed tub."),
    (("peach", "peaches", "nectarine", "nectarines"),
     "A ripe peach gives to a gentle press and smells sweet at the stem, and the skin between "
     "the red patches is cream rather than green.",
     "Peaches ripen in a paper bag on the counter in 1 to 3 days, and the fridge is what stops "
     "them and turns them mealy.",
     "Once they give, keep them in the fridge for 3 to 5 days and take them out an hour before "
     "you eat them."),
    (("plum", "plums", "apricot", "apricots", "greengage", "greengages"),
     "A ripe plum gives slightly under the thumb and smells sweet at the stem, and its skin "
     "should be tight rather than wrinkled.",
     "Plums and apricots ripen in a paper bag on the counter in 2 to 4 days.",
     "Once ripe they keep about a week in the fridge, and 3 days in a fruit bowl."),
    (("cherry", "cherries"),
     "A ripe cherry is firm and shiny, dark all over for its variety, with a green stem that "
     "bends rather than snaps.",
     "Cherries do not ripen after picking, so a pale, soft one stays pale and soft.",
     "Keep them unwashed in the fridge for about a week and wash them just before you eat, "
     "because a wet cherry splits and moulds."),
    (("pear", "pears"),
     "A ripe pear gives a little at the neck, just under the stem, and a pear that is soft in "
     "the belly is already past its best.",
     "Pears ripen from the inside out, so buy them firm and leave them on the counter for 2 to 4 "
     "days, or in a paper bag with a banana.",
     "Once the neck gives, they keep about 5 days in the fridge and go floury left out in the "
     "bowl."),
    (("kiwi", "kiwis", "kiwifruit"),
     "A ripe kiwi gives under a gentle press, the way a ripe avocado does.",
     "Hard kiwis ripen on the counter in 3 to 5 days, faster in a paper bag with an apple or a "
     "banana.",
     "Once soft, they keep about 2 weeks in the fridge, and apart from other fruit if you want "
     "them to stay firm."),
    (("pineapple", "pineapples"),
     "A ripe pineapple smells sweet at the base, feels heavy for its size, and a leaf from the "
     "middle of the crown pulls out easily. Softening at the bottom is part of it ripening, so a "
     "firm one with a soft base is ready rather than wrong.",
     "A pineapple gets no sweeter once it is picked, only softer, and it starts at the base, so "
     "the one you buy is as good as it will get.",
     "Whole, it keeps about a week on the counter, and cut pineapple keeps 3 to 4 days in the "
     "fridge in its own juice. One that is soft all over and smells of wine is overripe: eat it "
     "today or freeze it."),
    (("fig", "figs"),
     "A ripe fig is soft all over, droops at the neck and often has a bead of syrup at the eye.",
     "Figs do not ripen once they are picked, so a hard one stays hard.",
     "Keep them 2 or 3 days in the fridge, laid on a plate rather than piled up, and they taste "
     "best at room temperature."),
    (("grape", "grapes", "bunch of grapes"),
     "Ripe grapes are firm and come away from the bunch easily, with a dusty bloom on the skin "
     "rather than a sticky one.",
     "Grapes do not ripen after picking, so a sour bunch stays sour.",
     "Keep them unwashed in a bag in the fridge for a week or more, and wash them just before "
     "eating."),
    (("tomato", "tomatoes"),
     "A tomato is ready when it feels heavy and gives slightly in the hand, smells of tomato "
     "where the stalk was, and the colour is deep and even; a hard, pale one that smells of green "
     "is not there yet.",
     "They ripen off the vine in a bowl on the counter, quicker with a banana or an apple beside "
     "them, and the fridge is what stops that and kills the flavour.",
     "Keep them out of the fridge for up to a week on the counter, and a cut tomato in a tub for "
     "2 days."),
    (("lemon", "lemons", "lime", "limes"),
     "Citrus is picked ripe, so the test is weight rather than colour: a lemon or lime that feels "
     "heavy for its size and gives slightly under a thumb is full of juice, and a light, rock-hard "
     "one is dry inside.",
     "Nothing ripens them at home - a hard one softens a little on the counter in a few days, and "
     "a soft one goes straight in the fridge.",
     "Keep them a week or two in the bowl and a month in the fridge, and a lemon going soft is "
     "still good for juice and zest."),
    (("orange", "oranges", "satsuma", "satsumas", "clementine", "clementines", "tangerine",
      "tangerines"),
     "An orange or a satsuma is ready when it feels heavy for its size, which is juice rather than "
     "thick skin, and smells sweet at the stem; the small thin-skinned ones are usually the "
     "sweeter.",
     "Citrus does not ripen any further once it is picked, so a pale, dry one stays that way.",
     "Keep them a week or two in the bowl and a month in the fridge, and a clementine that is "
     "light and hollow-feeling has dried out at the ends."),
    (("apple", "apples", "braeburn", "cox", "gala", "granny smith"),
     "Apples are picked ripe and keep, so judge by feel: firm, heavy, a clean apple smell and a "
     "fresh green stem.",
     "There is nothing to ripen - a soft or mealy one has been off the tree too long and will not "
     "come back.",
     "Keep them for weeks in the fridge, far longer than on the counter, and away from other fruit "
     "because an apple gives off the gas that ripens everything beside it."),
    (("coconut", "coconuts"),
     "Shake it: a fresh coconut sloshes with liquid, and a silent one has dried out inside. Pick "
     "one heavy for its size with no cracks or damp patches at the eyes.",
     "A coconut is picked ripe, so there is nothing to do at home but open it.",
     "Drink the water the day it is opened, keep the flesh 3 to 4 days in a tub in the fridge, and "
     "freeze what you will not eat."),
    (("papaya", "papayas", "pawpaw", "pawpaws"),
     "A papaya is ready when the skin is mostly yellow-orange rather than green, it gives slightly "
     "under a thumb and smells faintly sweet rather than green.",
     "A green one ripens on the counter in 2 or 3 days, faster in a paper bag, and the fridge "
     "holds it once it is soft.",
     "Eat a ripe one within 2 days, and a cut one within 2 days from the fridge."),
    (("strawberry", "strawberries"),
     "Strawberries do not ripen after picking, so look for deep red right up to the tip under the "
     "leaves, a sweet smell and a dry, bright green cap.",
     "There is nothing to ripen at home and a pale one will not colour up; take them out of the "
     "fridge half an hour before you eat them, which is the only thing that improves them.",
     "Keep them 3 to 5 days in the fridge, unwashed and spread on kitchen paper, since washing "
     "them early is what turns them soft."),
    (("blueberry", "blueberries", "raspberry", "raspberries", "blackberry", "blackberries"),
     "Ripe berries are deep in colour all over with a dusty bloom, plump and only just soft, and a "
     "shrunken or leaking one is past it; taste one, because a punnet is better judged by flavour "
     "than by colour.",
     "Berries do not ripen once they are picked, so a pale one stays pale and sharp.",
     "Keep them 3 to 5 days in the fridge, spread on a plate lined with kitchen paper rather than "
     "heaped in a bag."),
    (("pomegranate", "pomegranates"),
     "A ripe pomegranate is heavy for its size, has square-ish sides rather than a round ball, and "
     "leathery, slightly scuffed skin rather than a shiny one.",
     "Pomegranates are picked ripe and do not ripen further, so a pale, light one stays sharp.",
     "Keep them for weeks in a cool cupboard, the seeds sweetest the day it is opened."),
)

KEEP_ASKS = ("keep", "keeps", "store", "storing", "storage", "last", "lasts", "how long",
             "fridge", "freezer", "freeze", "frozen", "how much longer")
RIPEN_ASKS = UNDER_RIPE + (
              "ripen", "ripens", "ripening", "hurry", "faster", "speed it up",
              "speed them up", "softer", "soften", "still hard", "rock hard", "hard as",
              "too hard", "not ripe", "unripe", "still firm", "sour", "tasteless", "no flavour",
              "no flavor", "get it ripe", "get them ripe", "make it ripe", "make them ripe",
              "hard", "sour", "tasteless", "bland")
TELL_ASKS = ("tell if", "know if", "how do i tell", "how can i tell", "how to tell",
             "is it ready", "is it ripe", "when is it", "when are they", "ready to eat",
             "supposed to be", "supposed to", "should it be", "should they be", "meant to be",
             "is it normal", "is that normal",
             "press", "squeeze", "smell", "feel like")

RIPEN_ASIDE = ("pizza", "hawaiian", "topping", "toppings", "juice", "smoothie", "jam",
               "chutney", "pie", "tart", "crumble", "cake", "salad", "salsa", "sauce",
               "recipe", "recipes", "curry", "muffin", "loaf", "grow", "growing", "grew",
               "plant", "plants", "planted", "vine", "vines", "tree", "trees", "blight",
               "greenhouse", "allotment", "seed", "seeds", "sow", "sowing", "compost",
               "peel", "peeled", "peeling", "deseed", "stone", "stoned", "core", "cored",
               "cut up", "chop", "chopped",
               "tin", "tins", "tinned", "tin of", "tins of", "can of", "cans of", "jar", "jars",
               "opened", "in syrup", "dried", "dried fruit", "sundried",
               "in a can", "out of a can", "from a can", "in a jar", "out of a jar")


def _ripen_lead(text):
    if any(word in text for word in TELL_ASKS):
        return "test"
    if any(word in text for word in RIPEN_ASKS):
        return "trick"
    if any(word in text for word in KEEP_ASKS):
        return "keep"
    return "test"


def _ripens(test, trick, keep):
    def reply(memory, understood):
        read = understood if isinstance(understood, dict) else {}
        text = str(read.get("clean") or read.get("text") or "").lower()
        lead = _ripen_lead(text)
        leans = read.get("leans_on")
        if lead == "test" and not any(word in text for word in TELL_ASKS):
            if isinstance(leans, (list, tuple)):
                leans = " ".join(str(word) for word in leans)
            if leans:
                lead = _ripen_lead(text + " " + str(leans).lower())
        if lead == "keep":
            return keep
        if lead == "trick":
            return trick + " " + test
        return test + " " + trick
    return reply


ENTRIES += [
    entry("ripen-%s" % names[0], (names, tuple(KEEPING_KEY) + RIPEN_WORDS),
          _ripens(test, trick, keep), bias=2,
          avoid=_STAND_DOWN + RIPEN_ASIDE)
    for names, test, trick, keep in RIPEN_TABLE
]

UNRIPE_STATED = UNDER_RIPE + (
                 "hard", "hard as", "as hard as", "rock hard", "still hard", "so hard",
                 "unripe", "not ripe", "nowhere near ripe", "too hard", "firm as", "as firm as",
                 "like a stone", "like stones", "as stones", "as a stone", "sour", "tasteless",
                 "no flavour", "no flavor", "won't ripen", "wont ripen", "will not ripen",
                 "not softening", "refuses to ripen")

_RIPEN_ASIDE_KEEPING = ("pizza", "hawaiian", "topping", "toppings", "juice", "smoothie", "jam",
                        "chutney", "pie", "tart", "crumble", "cake", "salad", "salsa", "sauce",
                        "recipe", "recipes", "curry", "muffin", "loaf", "grow", "growing",
                        "grew", "plant", "plants", "planted", "vine", "vines", "tree", "trees",
                        "blight", "greenhouse", "allotment", "seed", "seeds", "sow", "sowing",
                        "compost", "tin", "tins", "tinned", "tin of", "tins of", "can of",
                        "cans of", "jar", "jars", "opened", "in syrup", "dried", "dried fruit",
                        "sundried", "in a can", "out of a can", "from a can", "in a jar",
                        "out of a jar")


_STAND_DOWN_HARD = tuple(
    word for word in _STAND_DOWN
    if not any(dish in word or word in dish for dish in DISH_ASK))


def _ripen_haystack(understood, memory):
    read = understood if isinstance(understood, dict) else {}
    parts = [str(read.get("clean") or read.get("text") or "")]
    leans = read.get("leans_on")
    if isinstance(leans, dict):
        parts.append(str(leans.get("text") or ""))
    elif isinstance(leans, (list, tuple)):
        parts.append(" ".join(str(word) for word in leans))
    turns = (memory or {}).get("turns")
    if isinstance(turns, list) and turns and isinstance(turns[-1], dict):
        for turn in turns[-3:]:
            said = turn.get("user")
            if isinstance(said, str):
                parts.append(said)
    return " ".join(parts).lower()


def _ripen_row_for(text):
    for row in RIPEN_TABLE:
        names = row[0]
        for name in names:
            if re.search(r"\b%s\b" % re.escape(name), text):
                return row
    return None


def _ripen_from_the_chat(memory, understood):
    row = _ripen_row_for(_ripen_haystack(understood, memory))
    if row is not None:
        return row[2] + " " + row[1]
    return ("Most fruit ripens on the counter in 2 to 4 days, and a paper bag with a banana in it "
            "halves that; the fridge is what stops it, so leave them out until they give. Once "
            "they give, they keep a few days in the fridge.")


ENTRIES += [
    entry("ripen-stated-%s" % names[0], (names, UNRIPE_STATED),
          _ripens(test, trick, keep), bias=2,
          avoid=_STAND_DOWN_HARD + _RIPEN_ASIDE_KEEPING)
    for names, test, trick, keep in RIPEN_TABLE
]

_NOT_A_FRUIT = ("carrot", "carrots", "potato", "potatoes", "new potato", "new potatoes",
                "parsnip", "parsnips", "swede", "swedes", "turnip", "turnips", "beetroot",
                "cabbage", "cabbages", "broccoli", "cauliflower", "sprout", "sprouts",
                "onion", "onions", "leek", "leeks", "celery", "courgette", "courgettes",
                "aubergine", "aubergines", "pumpkin", "squash", "butternut", "sweet potato",
                "sweet potatoes", "green bean", "green beans", "runner bean", "runner beans",
                "pea", "peas", "sweetcorn", "spinach", "kale", "chard", "fennel", "asparagus",
                "artichoke", "artichokes", "mushroom", "mushrooms", "pepper", "peppers",
                "shallot", "shallots", "spring onion", "spring onions", "chestnut", "chestnuts",
                "lentil", "lentils", "chickpea", "chickpeas", "bean", "beans", "chickpeas",
                "pasta", "rice", "noodle", "noodles", "couscous", "quinoa", "barley",
                "stock", "stew", "soup", "curry", "casserole", "mince", "chicken", "beef",
                "lamb", "pork", "sausage", "sausages", "egg", "eggs")

ENTRIES.append(
    entry("ripen-from-the-chat",
          (("ripen", "ripen them", "ripening", "ready", "soften", "ripe"),
           ("will they", "will it", "will these", "do they", "do these", "they ripen",
            "it ripen", "them ripen", "these ripen", "let them", "let these", "leave them",
            "how long", "until", "till they", "get them", "make them")),
          _ripen_from_the_chat, bias=3,
          avoid=("bread", "cake", "cheese", "banana bread", "yoghurt", "yogurt", "milk",
                 "chicken", "meat", "fish", "wine", "beer", "sourdough", "dough", "starter",
                 "breast", "bump", "pregnancy", "pregnant", "nappy", "nappies", "potty")
          + _NOT_A_FRUIT))

ENTRIES += [
    entry("cheese-store-by-name", (CHEESE_NAMES, STORE_ASKS),
          "Hard cheese keeps about 2 weeks in the fridge once it is opened and soft cheese about "
          "a week. Wrap it in paper rather than cling film, which sweats it, and keep it in the "
          "drawer at the bottom rather than the door.",
          bias=2, ask=STORE_ASKS,
          avoid=("how much", "per person", "cheeseboard", "board", "recipe", "what can i make",
                 "melt", "melted", "stringy", "grate", "grated", "good for you", "calories",
                 "healthy", "freeze", "freezer", "slimy", "gone hard", "gone dry",
                 "dried out") + MOULD_WORDS),
    entry("cheese-mould-by-name", (CHEESE_NAMES + SOFT_CHEESES + BLUE_CHEESES,
                                   MOULD_WORDS + ("eat", "safe", "ok", "cut", "around it",
                                                  "bin", "throw")),
          _cheese_mould, bias=3, ask=MOULD_WORDS),
    entry("pasta-sauce-keep", (PASTA_SAUCE_WORDS, SAUCE_KEEPING_WORDS),
          _pasta_sauce_keep, bias=2, ask=SAUCE_KEEPING_WORDS,
          avoid=("make", "making", "recipe", "recipes", "cook", "cooking", "how do i cook",
                 "simmer", "simmering", "simmered", "boil", "boiling", "fried", "fry", "fries",
                 "frying", "hob", "pan", "stir", "minutes", "how many minutes", "tinned tomatoes",
                 "chopped tomatoes", "tin of tomatoes",
                 "how do i make", "lasagne", "lasagna", "pizza", "pasta bake", "what can i make",
                 "what can i do", "serve", "serving", "saucepan", "ketchup", "soy sauce",
                 "hot sauce", "worcestershire", "apple sauce", "cranberry sauce", "mint sauce",
                 "bbq sauce", "barbecue sauce", "how much", "per person", "portion", "portions",
                 "bolognese", "left out", "leave it out", "leaving it out", "left on the side",
                 "stay out", "stays out", "sitting out", "out of the fridge",
                 "on the counter", "overnight")),
    entry("storecupboard-keep", (SC_KEEP_NAMES, SC_KEEP_ASKS),
          _storecupboard_keep, bias=1, ask=SC_KEEP_ASKS, avoid=SC_KEEP_AVOID),
    entry("jam-mould", (("jam", "marmalade", "preserve", "preserves", "chutney", "chutneys",
                         "jam jar", "jam jars", "jar of jam", "marmalade jar", "kilner jar"),
                        ("mould", "mouldy", "mold", "moldy", "fluff", "fluffy", "furry", "fur",
                         "fuzz", "fuzzy", "spots", "speckled", "bloom", "white", "green",
                         "blue", "black", "bits")),
          ("Mould on the top of a jam lifts off: take a spoon and the patch plus a good centimetre "
           "around it, and the rest is fine if it smells and tastes normal. Bin the jar instead if "
           "it is a low-sugar or homemade jam, if the mould runs down the side of the jar, or if "
           "it smells fermented - and never spoon it back in."),
          bias=2,
          avoid=("lid is", "lid has", "peanut butter", "bread", "loaf", "cheese", "meat",
                 "ham", "yoghurt", "jam roly", "doughnut", "sponge", "cake", "tart", "recipe")),
]

_CRUNCH_FOODS = ("crisps", "crisp", "potato crisps", "biscuits", "biscuit", "crackers",
                 "cracker", "cereal", "cereals", "cornflakes", "muesli", "granola", "nuts",
                 "crispbread", "pretzels", "tortilla chips", "breadsticks",
                 "bread sticks", "oatcakes", "corn chips", "rice cakes", "pork scratchings",
                 "peanuts", "cashews", "almonds", "walnuts")

_CRUNCH_STATE = ("gone soft", "soft", "gone stale", "stale", "chewy", "soggy", "damp",
                 "rubbery", "lost its crunch", "not crunchy", "no crunch")

_CRUNCH_OWN = ("crisps", "crisp", "potato crisps", "crackers", "cracker", "crispbread",
               "pretzels", "tortilla chips", "breadsticks", "bread sticks", "oatcakes",
               "corn chips", "rice cakes", "pork scratchings")

_CRUNCH_VERDICT = ("Still fine to eat: soft is damp, not spoilage, and heat takes the damp back "
                   "out. Bin them instead if there is mould on any of them, or if they smell of "
                   "old paint or crayons, which is the oil in them going rancid.")

_CRUNCH_FIX = ("Soft, not spoilt: they have taken damp out of the air. Spread them on a tray and "
               "give them 4 to 5 minutes at 150C, then leave them to cool - they crisp as they "
               "cool, not in the oven. Popped corn and nuts take the same and 3 minutes is "
               "enough; a biscuit that has gone chewy comes back the same way.")

_CRUNCH_KEEP = ("To keep the crunch, tip them into a jar or a tin with a tight lid rather than "
                "leaving them in the bag, which breathes, and keep them in a cupboard rather than "
                "the fridge, which is damp. A piece of kitchen paper in the box takes up the damp "
                "the same way.")

_YOGHURT_WHEY = ("That clear liquid is whey, and it belongs to the yogurt: stir it back in. "
                 "Yogurt that has separated into curds and watery liquid and smells sharp, fizzy "
                 "or of alcohol is the one to bin.")

_YOGHURT_FIX = ("Yogurt separates as the whey rises, and spooning from the same spot makes it "
                "happen sooner: take from the side and stir the tub before you serve it. Plain "
                "yogurt keeps about a week past the date once it is open, and stirring is all a "
                "watery tub needs; a sharp or fizzy smell is when to bin it.")

_SALT_CLUMPS = ("Clumped salt has taken damp, not gone off: break it up with the back of a spoon "
                "and it still tastes of salt and works the same in cooking. A few grains of rice "
                "or a piece of dry cracker in the jar keeps it running, and a lidded jar in a dry "
                "cupboard keeps it clump-free where the paper packet does not.")

_FLOUR_LUMPS = ("Lumps in flour are damp, not spoilage: sift it and it is fine to bake with. If "
                "it also smells musty or sour, or the lumps are moving, bin the bag - that is "
                "mites - wipe the shelf out and keep the next bag in a sealed jar.")

_FLOUR_MITES = ("Those are flour mites or weevils and that bag has to go: seal it and bin it, then "
                "go through the dry cupboard - rice, oats, cereal, pasta, dried fruit - and bin "
                "anything open that has them in. Wipe the shelf out, and keep flour in a sealed "
                "jar from then on. They are not a health risk once cooked, but nothing worth "
                "keeping is left in that bag.")


def _said_anything(understood, words):
    said = " ".join(str((understood or {}).get(k) or "")
                    for k in ("clean", "norm_text", "text")).lower()
    return any(word in said for word in words)


_CRUNCH_SAFE = ("safe", "still eat", "still ok", "still good", "can i eat", "ok to eat",
                "edible", "bin", "throw", "off", "bad", "risky", "ill")


def _crunch_reply(memory, understood):
    if _said_anything(understood, _CRUNCH_SAFE):
        return _CRUNCH_VERDICT + " " + _CRUNCH_FIX
    return _CRUNCH_FIX + " " + _CRUNCH_VERDICT


def _yoghurt_reply(memory, understood):
    if _said_anything(understood, ("keep", "keeping", "stop", "runny", "watery", "separate")):
        return _YOGHURT_FIX + " " + _YOGHURT_WHEY
    return _YOGHURT_WHEY


def _flour_reply(memory, understood):
    if _said_anything(understood, ("weevil", "weevils", "mite", "mites", "bug", "bugs",
                                   "worm", "worms", "moving", "insects", "maggots")):
        return _FLOUR_MITES
    return _FLOUR_LUMPS


_STATE_NOT_FOOD = KEEP_NOT_KEEPING + ("recipe", "recipes", "how do i make", "how do you make",
                                      "make my own", "homemade", "buy", "buying", "shop",
                                      "supermarket", "brand", "brands", "best", "cheapest",
                                      "where can i", "calories")

ENTRIES += [
    entry("keep-crunch-gone", (_CRUNCH_FOODS, _CRUNCH_STATE),
          _crunch_reply, bias=2,
          ask=("soft", "stale", "chewy", "soggy", "damp", "rubbery", "crunch",
               "crunchy", "gone", "lost"),
          avoid=_STATE_NOT_FOOD + ("dip", "dips", "recipe", "chocolate", "cake", "bread",
                                   "loaf", "sandwich", "butter", "roast", "salted nuts",
                                   "nut allergy", "allergic", "peanut butter")),
    entry("keep-crunch-fresh", (_CRUNCH_OWN, ("fresh", "freshness", "stay fresh",
                                              "keep them fresh", "keeps them fresh")),
          _CRUNCH_KEEP + " " + _CRUNCH_FIX, bias=2,
          ask=("fresh", "freshness"),
          avoid=_STATE_NOT_FOOD + ("dip", "dips", "chocolate", "cake", "sandwich", "butter",
                                   "roast", "salted nuts", "nut allergy", "allergic")),
    entry("keep-yoghurt-whey",
          (("yogurt", "yoghurt", "yogurts", "yoghurts", "greek yogurt", "greek yoghurt",
            "natural yogurt", "natural yoghurt", "plain yogurt", "plain yoghurt"),
           ("water on top", "water at the top", "water in it", "watery", "runny", "separated",
            "separating", "split", "whey", "liquid on top", "liquid in it", "curdled",
            "water out", "get the water out", "drain", "drain it", "sieve", "strain")),
          _yoghurt_reply, bias=2,
          ask=("water", "watery", "runny", "separated", "split", "whey", "liquid", "curdled",
               "keep", "stop", "drain", "strain", "sieve"),
          avoid=_STATE_NOT_FOOD + ("starter", "culture", "make my own", "how do i make")),
    entry("keep-salt-clumps",
          (("salt", "sea salt", "table salt", "rock salt", "kosher salt", "salt cellar",
            "salt shaker", "salt jar"),
           ("clumpy", "clumped", "lumpy", "stuck together", "caked", "caking", "gone hard",
            "hard", "damp", "block", "solid")),
          _SALT_CLUMPS, bias=2,
          ask=("clumpy", "clumped", "lumpy", "stuck", "caked", "caking", "hard", "damp",
               "block", "solid"),
          avoid=KEEP_NOT_KEEPING + ("bath", "bath salts", "epsom", "road", "grit", "lamp",
                                    "salt water", "sea water", "gargle", "blood pressure",
                                    "recipe", "bread", "dough", "brine", "rub", "seasoning",
                                    "how much salt")),
    entry("keep-flour-lumps",
          (("flour", "plain flour", "self raising flour", "self-raising flour", "bread flour",
            "wholemeal flour", "white flour"),
           ("lumpy", "lumps", "clumpy", "clumps", "weevils", "weevil", "mites", "mite", "bugs",
            "worms", "moving", "damp", "sour")),
          _flour_reply, bias=2,
          ask=("lumpy", "lumps", "clumpy", "clumps", "weevils", "weevil", "mites", "mite",
               "bugs", "worms", "moving", "damp", "sour"),
          avoid=KEEP_NOT_KEEPING + ("bread", "loaf", "cake", "recipe", "recipes", "how do i make",
                                    "bake", "baking", "sauce", "thicken", "roux", "how much")),
]


OFF_BERRIES = ("strawberry", "strawberries", "raspberry", "raspberries", "blueberry",
               "blueberries", "blackberry", "blackberries", "gooseberry", "gooseberries",
               "cherry", "cherries", "grapes", "grape", "berry", "berries", "punnet",
               "punnet of", "soft fruit", "stone fruit")
OFF_LEAVES = ("lettuce", "spinach", "salad leaves", "leaves", "rocket", "watercress", "kale",
              "cabbage", "bag of salad", "salad bag", "salad", "coleslaw mix")
OFF_SOFT = ("cucumber", "cucumbers", "courgette", "courgettes", "zucchini", "tomato", "tomatoes",
            "pepper", "peppers", "aubergine", "aubergines", "avocado", "avocados", "mango",
            "mangoes", "peach", "peaches", "nectarine", "nectarines", "plum", "plums", "fig",
            "figs", "melon", "melons", "squash", "pumpkin", "mushy fruit")
OFF_CITRUS = ("orange", "oranges", "lemon", "lemons", "lime", "limes", "clementine",
              "clementines", "satsuma", "satsumas", "tangerine", "tangerines", "grapefruit",
              "mandarin", "mandarins")
OFF_FIRM = ("apple", "apples", "pear", "pears", "carrot", "carrots", "swede", "turnip",
            "beetroot", "parsnip", "parsnips", "ginger", "cabbage head", "cauliflower",
            "broccoli")
OFF_ANY = ("fruit", "fruits", "veg", "vegetables", "produce", "punnet", "the drawer",
           "salad drawer", "veg drawer", "crisper", "greengrocer", "the shopping")
OFF_WORDS = ("mould", "mouldy", "molds", "mold", "moldy", "fuzzy", "furry", "fuzz", "fur",
             "going mouldy", "gone mouldy", "mould on it", "mould on them", "fluff on",
             "fluffy", "slimy", "slime",
             "slimey", "slimier", "gone off", "gone bad", "rotting", "rotten", "rot",
             "gone rotten", "going off", "gone past it", "on the turn")
OFF_AVOID = ("plant", "plants", "on the plant", "growing", "grow", "grew", "garden", "gardener",
             "allotment", "crop", "crops", "vine", "vines", "greenhouse", "polytunnel", "tree",
             "soil", "compost", "mulch", "water", "watering", "watered", "harvest", "pick",
             "picking", "picked them", "seedling", "seedlings", "bush", "fertiliser",
             "fertilizer", "feed", "blossom", "blossom end", "slug", "slugs", "snail", "snails",
             "sow", "sowing", "sowed", "transplant", "prune", "pruning", "planted",
             "recipe", "recipes", "cook", "cooking", "bake", "baking", "juice", "juicing",
             "smoothie", "jam", "chutney", "pie", "crumble", "muffin", "muffins", "cake",
             "compost bin", "food waste", "bin day", "wheelie",
             "mildew", "powdery", "powder", "white powder", "white mould", "grey mould",
             "gray mould", "on the leaves", "on the fruit", "on the stem",
             "cooked", "cooking water", "baked", "bake", "baked potato", "jacket", "jacket potato",
             "boiled", "boiling", "roast", "roasted", "mashed", "mash", "chips", "fries", "fried",
             "soup", "stew", "curry", "pie", "tart", "casserole", "leftover", "leftovers",
             "reheat", "reheated", "microwave", "salad dressing", "dressed",
             "shop", "shops", "supermarket", "sold", "sell", "selling", "refund", "receipt",
             "money back", "take it back", "took it back", "return it", "complaint", "complain",
             "council", "use by", "best before", "label", "packet", "packaging", "delivery",
             "stop", "stops", "stopping", "prevent", "preventing", "how do i keep", "keep them",
             "keep it from", "keep them from", "last longer", "make them last", "make it last",
             "so they dont go", "so it doesnt go", "so they don't go", "so it doesn't go")


OFF_NAMES = OFF_BERRIES + OFF_LEAVES + OFF_CITRUS + OFF_SOFT + OFF_FIRM + OFF_ANY


def _produce_is_named(understood):
    low = " %s " % " ".join(str((understood or {}).get("clean")
                                or (understood or {}).get("text") or "").lower().split())
    return any((" %s " % name) in low for name in OFF_NAMES)


_OFF_GROUP_WORDS = frozenset((
    "berry", "berries", "punnet", "punnet of", "soft fruit", "stone fruit", "fruit", "fruits",
    "veg", "vegetables", "produce", "the drawer", "salad drawer", "veg drawer", "crisper",
    "greengrocer", "the shopping", "mushy fruit", "leaves", "salad", "bag of salad",
    "salad bag", "salad leaves", "coleslaw mix",
))


def _off_one(name):
    if name.endswith("ies"):
        return name[:-3] + "y"
    for ending in ("oes", "ches", "shes", "sses"):
        if name.endswith(ending):
            return name[:-2]
    if name in ("leaves", "leafes"):
        return "leaf"
    if name.endswith("s") and not name.endswith("ss"):
        return name[:-1]
    return name


def _produce_gone_off(memory, reading):
    said = " %s " % (((reading or {}).get("clean") or "").lower())

    def thing(group, categories=False):
        hit = None
        for name in sorted(group, key=len, reverse=True):
            if (" %s " % name) in said or said.strip().startswith(name + " "):
                if name in _OFF_GROUP_WORDS:
                    return name if categories else None
                hit = name
                break
        return hit

    def phrase(name):
        if name is None:
            return None, False
        one = _off_one(name)
        return "the " + name, one != name

    berries = phrase(thing(OFF_BERRIES))
    leaves = phrase(thing(OFF_LEAVES, categories=True))
    citrus = phrase(thing(OFF_CITRUS))
    soft = phrase(thing(OFF_SOFT))
    firm = phrase(thing(OFF_FIRM))

    if berries[0]:
        return ("Bin every %s with fuzz on it and the ones touching it, then wash the rest and eat "
                "them today. On a berry the mould threads run under the skin where you cannot see "
                "them, so there is nothing to cut back to, and a closed punnet passes it on fast. "
                "Spread what is sound on kitchen paper in the fridge and it will hold a day or "
                "two." % _off_one(berries[0][4:]))
    if leaves[0]:
        return ("Pick out the slimy or furry leaves and bin them: that slime is bacteria, not "
                "water, and cooking will not make it safe to eat. Wash the rest well and eat or "
                "cook them today, because in a closed bag it spreads to whatever touches it. Dry "
                "the next lot in a tea towel and keep them in a bag with a sheet of kitchen "
                "paper, because wet leaves in a sealed bag are what went wrong in the first place.")
    if citrus[0]:
        return ("Bin %s and check the rest of the bag. Mould on citrus starts on the skin and the "
                "flesh under it is soft and wet, so there is nothing worth cutting back to - and "
                "dry the drawer and the bag, because a damp one passes it on. The sound ones keep "
                "a couple of weeks loose in the fridge." % citrus[0])
    if soft[0]:
        return ("Bin %s. %s mostly water, so the mould threads run right through %s and there is "
                "nothing to cut back to, and cooking does not make it safe again. A soft patch "
                "with no mould on it is just older - trim that away and cook the rest today."
                % (soft[0], "They are" if soft[1] else "It is",
                   "them" if soft[1] else "it"))
    if firm[0]:
        return ("Cut the mould off with an inch to spare and use the rest, unless the flesh under "
                "it is soft or smells wrong. A firm fruit or root does not carry the threads deep, "
                "so a small patch on an apple or a carrot is not the whole of it - and bin %s, "
                "because it spreads to what it touches in a drawer." % firm[0])
    return ("Anything soft and wet - a berry, a tomato, a leaf - goes in the bin once it has fuzz "
            "on it, and the sound ones it touched are washed and eaten today. A firm fruit or root "
            "can have the patch cut away with an inch to spare, unless the flesh underneath is "
            "soft or smells off.")


ENTRIES.append(
    entry("produce-gone-off",
          (OFF_BERRIES + OFF_LEAVES + OFF_CITRUS + OFF_SOFT + OFF_FIRM + OFF_ANY, OFF_WORDS),
          _produce_gone_off, bias=4, ask=OFF_WORDS, avoid=OFF_AVOID,
          guard=_produce_is_named))


ENTRIES.append(
    entry("freeze-sweet", (FREEZE_SWEET_NAMES, FREEZE_WORDS), _freeze_a_sweet, bias=3,
          ask=FREEZE_SWEET_NAMES, avoid=FREEZE_SWEET_AVOID))
