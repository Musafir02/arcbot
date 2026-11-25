
import re

from .dishes import a_plan_that_might_be_ruined, not_ruled_out
from .lookup import entry
from .cooking import JACKET_FILL, _crowd, _crowd_meal, _occasion

ANSWERS = ("cooking",)

ENTRIES = [
entry("bake-ideas",
      (("what can i bake", "what should i bake", "what shall i bake", "what can we bake",
        "what should we bake", "what to bake", "what can i bake today", "bake something",
        "something to bake", "baking ideas", "ideas for baking", "want to bake",
        "want to do some baking", "feel like baking", "fancy baking", "start baking",
        "get into baking", "getting into baking", "learn to bake", "what could i bake"),
       ("bake", "baking", "baked", "oven", "flour", "cake", "cakes", "biscuits", "cookies",
        "bread", "scones", "brownies", "easy", "quick", "simple", "today", "tonight",
        "weekend", "kids", "children", "beginner", "first time", "sweet", "something",
        "nothing", "banana", "bananas", "chocolate", "lemon")),
      "Scones take 15 minutes, flapjacks 25, a Victoria sponge 40 and banana bread an hour, so "
      "start with whichever time you have, and ripe bananas are the reason to make the last "
      "one. Weigh everything out before you start, cream the butter and sugar until the mixture "
      "is pale, and keep the oven door shut for the first two thirds of the time, because the "
      "cold air that gets in is what makes a cake sink.",
      avoid=("cake sale", "bake sale", "sale", "stall", "school fair", "fete", "fayre",
             "birthday", "wedding", "christening", "party", "celebration", "how many people",
             "tin size", "which tin", "how long", "temperature", "gas mark", "fan oven",
             "bake blind", "blind", "pastry", "shortcrust", "baked potato", "baked potatoes",
             "jacket potato", "baked beans", "bake beans", "no oven", "microwave", "air fryer",
             "sourdough", "yeast", "why did my", "why is my", "sank", "soggy", "burnt",
             "crumbly", "stodgy", "goes flat", "went flat", "pizza", "casserole",
             "one pot", "traybake chicken", "fish", "salmon", "chicken")),

entry("what-a-roux",
      (("roux", "beurre manie", "beurre manié"),
       ("what is", "whats a", "what's a", "what is a", "explain", "mean", "means",
        "definition", "difference", "used for", "for")),
      "A roux is equal weights of butter or oil and plain flour cooked together in a pan, and "
      "it is what thickens a white sauce, a gravy or a soup: melt 25g of butter, stir in 25g "
      "of plain flour and cook it a minute to take the raw flour taste off, then add the milk "
      "or stock a splash at a time, whisking. A pale roux thickens most, and the darker you "
      "cook it the less it thickens, which is why a brown roux for gravy needs more flour.",
      avoid=("without flour", "cornflour", "corn flour", "gluten free", "gluten-free",
             "cheese sauce", "white sauce", "bechamel", "béchamel")),

entry("bread-crumbly",
      (("bread", "loaf", "loaves", "sourdough", "buns", "roll", "rolls", "focaccia"),
       ("crumbly", "crumbles", "crumbling", "falls apart", "falling apart", "fall apart",
        "breaks up", "breaking up", "falls to pieces", "sandy", "stodgy and dry",
        "dry and crumbly", "wont hold together", "won't hold together")),
      "Crumbly bread is usually too little water or too much flour: the dough should be tacky "
      "and slightly sticky rather than dry enough to handle, so hold back a little of the "
      "flour and weigh it rather than scooping with a cup. Knead until a piece stretches thin "
      "enough to see light through it, which is what holds the crumb together, and let the "
      "loaf cool on a rack for an hour before cutting, because warm bread tears. If it is also "
      "pale and heavy, the oven was too cool or the loaf was under-proved.",
      avoid=("stale", "mouldy", "mould", "mold", "green", "rise", "rising", "flat", "yeast",
             "prove", "proof",
             "cake", "cakes", "sponge", "sponges", "muffin", "muffins", "cupcake", "cupcakes",
             "traybake", "tray bake", "brownie", "brownies", "scone", "scones")),

entry("freezer-full",
      (("freezer", "freezers", "freezer drawer", "chest freezer"),
       ("full", "full up", "too full", "packed", "overfull", "no room", "stuffed",
        "no space", "run out of room", "run out of space", "bursting")),
      "A freezer works best about three-quarters full: the frozen food holds the cold, but "
      "packed to the door it cannot move air and the food at the front starts to thaw. Freeze "
      "flat in bags with the air pressed out and stand them on edge like files, keep the "
      "oldest at the front so it goes first, and use the crush to cook from it - a full "
      "freezer is a week of dinners if you eat what is in it. A drawer that will not close "
      "means it is time for a clear-out, not more squeezing.",
      avoid=("defrost", "not working", "broken", "dead", "died", "faulty", "ice", "frost",
             "smell", "leak", "cold", "warm", "temperature")),
entry("cake-crumbly",
      (("cake", "cakes", "sponge", "sponges", "muffin", "muffins", "cupcake", "cupcakes",
        "loaf cake", "traybake", "tray bake", "brownies", "brownie", "victoria sponge"),
       ("crumbly", "crumbles", "crumbling", "falls apart", "falling apart", "fall apart",
        "falls to pieces", "sandy", "wont hold together",
        "won't hold together", "breaks up", "breaking up")),
      "A crumbly cake usually has too much flour or too little fat and egg, or it was beaten "
      "on after the flour went in: weigh the flour rather than scooping it with a cup, and stop "
      "mixing the moment the last streaks of flour disappear. Take it out a shade early rather "
      "than late, because five extra minutes dries a sponge and dry is what crumbles, and cool "
      "it in the tin for ten minutes before turning it out. Cut it cold: a cake cut warm breaks "
      "the crumb as the knife goes through.",
      avoid=("rise", "rises", "risen", "rising", "didnt rise", "not risen", "sinking", "sank",
             "sunken", "icing", "frosting", "buttercream", "tin size", "how long in the oven",
             "dry", "dried out", "overbaked", "over baked",
             "how do i make", "recipe", "bake a cake", "make a cake", "freeze", "freezing",
             "keep", "keeps", "keeping", "kept", "last", "lasts", "how long", "fridge",
             "refrigerate", "store", "storing", "stored", "stays fresh", "still good")),

entry("stock-cloudy",
      (("stock", "broth", "bouillon", "consomme", "consommé", "chicken stock", "beef stock",
        "vegetable stock", "bone broth"),
       ("cloudy", "clouded", "murky", "not clear", "unclear", "bits in it", "sediment",
        "how do i clear", "clear it", "make it clear", "looks cloudy")),
      "A cloudy stock boiled: once it comes to the boil the fat and protein break up into "
      "droplets that nothing will settle again, so keep it at the barest simmer with the lid "
      "off and skim the grey foam off the top in the first twenty minutes. To clear one that "
      "has already gone cloudy, whisk a lightly beaten egg white into the cold stock, bring it "
      "slowly to a simmer and let the white rise and set as a raft, then lift it out with the "
      "bits trapped in it. Strain through a sieve lined with kitchen paper, and do not stir it "
      "while it simmers or the raft breaks up.",
      avoid=("beer", "lager", "ale", "wine", "juice", "cider", "gravy", "sauce", "soup",
             "cloudy day", "weather", "sky", "rain", "urine", "water", "aquarium")),

entry("oil-in-a-cake",
      (("oil", "olive oil", "vegetable oil", "sunflower oil", "rapeseed oil", "cooking oil"),
       ("cake", "cakes", "sponge", "muffin", "muffins", "brownies", "brownie",
        "traybake", "tray bake", "carrot cake", "chocolate cake", "banana bread")),
      "Use 80g of oil for every 100g of butter the recipe asks for - about 4 to 5 tablespoons in "
      "a 20cm cake - and expect a slightly denser, moister crumb. Sunflower, vegetable or "
      "rapeseed gives a light plain cake; keep olive oil for a cake with a flavour of its own, "
      "like carrot or chocolate, where a good extra virgin is an asset rather than a taste you "
      "notice. Skip it where the method creams butter and sugar for air, and in pastry.",
      bias=5,
      ask=("how much", "how many", "how", "which", "what", "can i", "could i", "do i",
           "should i"),
      avoid=("instead of", "swap", "swapping", "replace", "replacing", "substitute",
             "recipe", "make a cake", "make the cake", "make my cake", "bake a cake",
             "icing", "frosting", "buttercream", "tin size", "how long in the oven",
             "store", "storing", "keep", "keeping", "go off", "goes off", "gone off", "last",
             "healthiest", "healthy", "calorie", "calories", "reuse", "reusing", "deep fat",
             "fry", "frying", "oil paint", "hair", "skin", "drizzle", "dressing",
             "butter or", "or butter",
             "cake tin", "cake tins", "loaf tin", "tin", "tins", "grease", "greasing",
             "greased", "line the tin", "lining the tin", "loaf of bread", "bread dough",
             "dough")),

entry("freeze-cooked-rice",
      (("rice", "basmati", "long grain rice", "white rice", "cooked rice", "leftover rice"),
       ("freeze", "freezes", "freezing", "frozen", "freezer", "can i freeze", "freeze it")),
      "Yes: cool it within the hour, box it while it is still warm rather than hot, and freeze "
      "it the same day - cooked rice keeps about a month in the freezer. Reheat it once until "
      "it is piping hot all the way through, and do not freeze it again after that.",
      ask=("freeze", "freezer", "frozen", "freezing"),
      bias=1,
      avoid=("fry", "fried", "stir fry", "bake", "boil", "cook it", "how do i cook",
             "how long does it take", "reheat", "microwave", "pudding", "risotto")),

entry("freeze-bread",
      (("bread", "loaf", "loaves", "sliced loaf", "sourdough"),
       ("freeze", "freezes", "freezing", "frozen", "freezer", "can i freeze", "freeze it")),
      "Slice it first, then bag it: bread keeps about three months in the freezer and the "
      "slices go straight into the toaster from frozen. Freeze it on the day you buy it, "
      "because a loaf frozen when it is already going stale thaws out stale.",
      ask=("freeze", "freezer", "frozen", "freezing"),
      bias=1,
      avoid=("fresh", "stale", "mouldy", "mould", "mold", "keep", "store", "last", "rise",
             "rising", "prove", "proof", "bake", "recipe", "crumbs", "sauce", "butter",
             "dough", "batter")),
entry("roast-dinner-menu",
      (("roast", "roast dinner", "sunday roast", "roasting joint", "roast lunch"),
       ("ideas", "menu", "what else", "what should i have", "what should i make",
        "what to serve", "what can i serve", "what goes with", "what to have with", "sides",
        "side dishes", "serve with", "have with", "cook with it")),
      "A roast is one joint, potatoes, two veg and gravy, and the veg is where you ring the "
      "changes: carrots and parsnips roasted round the meat for the last 45 minutes, greens or "
      "cabbage steamed, and peas with mint if it is lamb. Add Yorkshire puddings for beef, "
      "stuffing and apple sauce for pork, bread sauce for chicken or turkey. Work back from the "
      "meat, because the joint rests 20 minutes and that is when the potatoes go up to full "
      "heat.",
      avoid=("lamb", "beef", "chicken", "pork", "turkey", "gammon", "duck", "ham", "goose",
             "potato", "potatoes", "parsnip", "parsnips", "carrot", "carrots", "yorkshire",
             "how long", "temperature", "temp", "gas mark", "defrost", "frozen", "freeze",
             "leftover", "leftovers", "veg", "vegetables", "vegan", "vegetarian",
             "nut roast", "casserole", "slow cooker", "air fryer",
             "roast veg", "roast vegetables", "roasted veg", "roasted vegetables"),
      bias=1,
      guard=not_ruled_out("sunday-roast")),


entry("bread-without-flour",
      (("bread", "loaf", "loaves", "flatbread", "flatbreads", "soda bread", "naan", "pitta",
        "pita", "rolls", "buns", "bake", "baking", "make", "recipe", "recipes"),
       ("without flour", "with no flour", "no flour", "flourless", "out of flour",
        "ran out of flour", "run out of flour", "no bread flour",
        "none left of the flour", "no flour none left", "flour none left")),
      "With no flour at all, the quickest loaf is an oat one: blitz 300g porridge oats in a "
      "blender until they look like flour, then mix in 2 teaspoons of baking powder, 1 "
      "teaspoon of salt and 300g of thick yogurt or buttermilk, pour it into a lined loaf tin "
      "and bake at 180C for 40 to 45 minutes. For something in ten minutes, mash cold potato "
      "into a dough with 2 tablespoons of cornflour, salt and a knob of butter, pat it into "
      "flat rounds and fry them dry for three minutes a side. Ground almonds or a gluten-free "
      "bread flour blend also work cup for cup in a soda bread: 400g of either, 1 teaspoon of "
      "bicarbonate of soda, 350ml of buttermilk, 20 minutes at 200C.",
      ask=("without flour", "with no flour", "no flour", "flourless", "out of flour",
           "ran out of flour", "run out of flour", "no bread flour",
           "none left of the flour", "no flour none left", "flour none left"),
      avoid=("crumbly", "stale", "mouldy", "mould", "mold", "flat", "yeast", "sourdough",
             "cake", "cakes", "sauce", "gravy", "thicken", "roux", "batter", "pancake",
             "pancakes", "gluten free", "gluten-free", "bread machine",
             "pastry", "shortcrust", "short crust", "pie", "pies", "tart", "tarts", "quiche"),
      bias=4),
entry("keep-meat-juicy",
      (("chicken", "turkey", "beef", "pork", "lamb", "steak", "roast", "brisket", "meat",
        "duck", "gammon", "ham", "chops", "chop", "whole bird", "crown",
        "belly pork", "loin",
        "joint of beef", "joint of lamb", "joint of pork", "joint of meat", "roasting joint",
        "beef joint", "lamb joint", "pork joint",
        "shoulder of lamb", "shoulder of pork", "lamb shoulder", "pork shoulder",
        "rib of beef", "beef ribs", "pork ribs", "spare ribs", "rack of ribs", "lamb ribs",
        "chump", "rack of lamb"),
       ("juicy", "juicier", "juiciest", "moist", "moister", "tender", "tenderer", "succulent",
        "moisture", "not dry", "isnt dry", "isn't dry", "not go dry", "not dry out",
        "doesnt dry", "doesn't dry", "wont dry", "won't dry", "drying out", "dry out",
        "dries out", "not dried out", "from drying", "juices in", "stays moist",
        "comes out dry", "come out dry", "coming out dry", "turns out dry",
        "comes out tough", "comes out rubbery")),
      "Dry meat is overcooked meat, so keep it juicy with a thermometer and a rest rather than "
      "basting: chicken and pork come out of the oven at 74C, beef at 55C for medium rare or 65C "
      "for well done, and then sit on a warm board under foil for 10 to 20 minutes, which lets the "
      "juice settle back in instead of running onto the plate. A 2kg chicken wants 20 minutes per "
      "500g plus 20 at 190C, started breast down so the white meat sits in the fat. Basting mostly "
      "costs oven heat and changes little.",
      bias=3,
      avoid=(
             "chopping board", "cutting board", "wooden board", "wooden spoon", "spatula",
             "fridge", "freezer", "freeze", "freezes", "freezing", "frozen", "leftovers",
             "leftover", "how long", "days", "reheat", "reheating", "safe", "safely",
             "bacteria", "poisoning", "left out", "overnight", "thaw", "defrost", "marinade",
             "marinading", "marinating", "brine", "brining", "rub", "calories", "protein",
             "healthy", "healthier", "cheap", "price", "cost", "recipe", "air fryer",
             "slow cooker", "sous vide", "deep fry", "temperature to cook", "how long to cook",
             "what temperature", "breast", "breasts", "thigh", "thighs", "burgers", "mince",
             "meatballs", "stew", "casserole", "curry", "soup", "sandwich", "ribeye",
             "how do i cook", "how to cook", "how do i roast", "how to roast", "rest",
             "slow cook", "slow cooking", "slow-cooked", "slow roast", "rubbery", "rubber",
             "tough", "tougher", "toughest",
             "resting", "rest it", "how long in the oven", "roasting time", "cooking time",
             "knee", "knees", "hip", "hips", "ache", "aches", "aching", "achy", "pain", "pains",
             "painful", "sore", "soreness", "stiff", "stiffness", "injury", "injured", "sprain",
             "sprained", "arthritis", "physio", "physiotherapy", "muscle", "muscles", "sciatica",
             "slipped disc", "trapped nerve", "hamstring", "elbow", "wrist", "ankle", "neck",
             "my back", "bad back", "back pain", "shoulder pain", "neck pain", "joint pain",
             "my knee", "my shoulder", "my ribs", "my hip", "my elbow", "my wrist", "my ankle",
             "my knees", "my joints", "shoulder ache", "sore shoulder",
             "cod", "haddock", "trout", "mackerel", "tuna", "prawns",
             "seafood", "fishcakes", "fish cake", "fish cakes")),
entry("keep-fish-moist",
      (("fish", "salmon", "cod", "haddock", "trout", "mackerel", "seafood", "fishcakes",
        "fish cake", "fish cakes", "sea bass", "bass", "hake", "pollock", "sardines",
        "kippers", "monkfish", "fish fillet", "fish fillets",
        "tuna steak", "tuna steaks"),
       ("juicy", "juicier", "moist", "moister", "flakes", "rubbery", "stays moist",
        "keep it moist")),
      "Fish is done at 50 to 55C, or the moment a fork twists a flake and it just separates, and "
      "it keeps cooking off the heat, so take it out a touch early and rest it two minutes. Cook "
      "it through to 63C for anyone pregnant, elderly or with a weak immune system. A "
      "salmon fillet wants 4 to 6 minutes a side in a hot pan or 8 to 12 minutes at 200C, cod and "
      "haddock a minute or two more, a tuna steak only 1 to 2 minutes a side so the middle stays "
      "pink, and a whole fish 10 minutes per 2.5cm of thickness. Salt it "
      "15 minutes ahead or not at all and keep lemon off it until it is off the heat: both draw "
      "water out. Flakes that stay in soft pieces mean it was in long enough, so lift it then "
      "rather than waiting for it to look white all through.",
      bias=3,
      avoid=("fridge", "freezer", "freeze", "frozen", "leftovers", "how long", "days", "reheat",
             "safe", "safely", "bacteria", "poisoning", "left out", "overnight", "thaw",
             "defrost", "recipe", "healthy", "healthier", "protein", "calories", "cheap",
             "price", "cost", "buy", "shop", "mercury", "pregnant", "allergy", "allergic",
             "how do i cook", "how to cook", "how do i pan fry", "how to pan fry", "bake",
             "baking", "batter", "fish and chips", "breadcrumbs", "smoked", "smoking",
             "sushi", "raw", "shellfish", "prawn cocktail")),
entry("dinner-rut",
      (("bored", "bored of", "bored with", "same dinners", "same meals", "same old dinners",
        "dinner rut", "stuck in a rut", "run out of ideas", "running out of ideas",
        "tired of cooking", "tired of the same", "sick of the same", "sick of cooking",
        "fed up of cooking", "fed up with cooking", "cooking the same"),
       ("dinner", "dinners", "tea", "supper", "meals", "meal", "cooking", "cook", "food",
        "recipes", "ideas", "what can i try", "what can i make", "suggest", "weeknight")),
      "Try a traybake, a stir-fry and a pasta this week: change one of three things and the same "
      "dinner comes out new - the shape (traybake, stir-fry, pasta, curry, soup), the carb under "
      "it (rice, potatoes, couscous, bread, noodles) or the sauce that finishes it (tomato, "
      "yoghurt and lemon, a spice paste, gravy, pesto). Mince is a ragu, a chilli with rice, or a "
      "cottage pie. Keep five dinners you can cook without thinking and swap one of those each "
      "week.",
      avoid=("mince", "chicken", "beef", "pork", "lamb", "fish", "salmon", "pasta", "rice",
             "potato", "potatoes", "eggs", "vegetarian", "vegan", "gluten", "dairy",
             "calorie", "calories", "healthy", "budget", "cheap", "student", "kids",
             "family", "party", "how long", "minutes", "freeze", "leftover", "leftovers",
             "goes with", "meal prep", "batch"),
      bias=2),

entry("make-yoghurt",
      (("yoghurt", "yogurt", "yoghurt maker", "yogurt maker", "natural yoghurt", "live yoghurt"),
       ("make", "making", "home", "at home", "homemade", "myself", "starter", "culture",
        "ferment", "fermented", "set it", "from milk", "own yoghurt", "machine",
        "without a machine", "no machine")),
      "Warm a litre of milk to just below boiling - 85C, or small bubbles round the edge of the "
      "pan - then let it cool to about 43C, which is a finger in it feeling warm rather than hot. "
      "Stir in 3 tablespoons of live natural yoghurt, keep it at that warmth for 8 to 12 hours in "
      "a flask, a yoghurt maker or an airing cupboard, and chill it once it has set; keep 3 spoons "
      "back as the starter for the next lot. Long or warm and it turns sour and grainy, cool or "
      "short and it stays runny.",
      avoid=("how long", "keep", "keeps", "keeping", "gone off", "off", "bin", "use by",
             "healthy", "good for you", "bad for you", "calories", "sugar", "protein", "calcium",
             "dairy free", "lactose", "freeze", "frozen", "thick", "greek", "skin on")),
entry("whole-chicken-value",
      (("whole chicken", "whole chickens", "a whole bird", "whole birds", "whole chook",
        "buy a whole chicken", "buying a whole chicken", "chicken whole",
        "whole chicken or breast", "whole chicken or breasts", "whole chicken vs breasts"),
       ("cheaper", "cheapest", "cheap", "cost", "costs", "price", "prices", "worth it",
        "worth buying", "worth the money", "better value", "value", "more expensive",
        "expensive", "save", "saves", "saving", "save money", "money", "vs", "versus",
        "instead of breasts", "instead of fillets", "or breasts", "or fillets")),
      "A whole chicken is nearly always the cheaper way to buy chicken: a 1.5kg bird gives about "
      "700g of meat plus a carcass for stock, which is four portions for £4 to £5, where the same "
      "weight in breast fillets is £7 to £9. The catch is a third of the weight is bone and it "
      "takes 15 minutes to joint. Roast it whole for a Sunday, joint it for a curry or a traybake, "
      "and simmer the carcass for stock; buy fillets only when dinner has to be quick.",
      ask=("cheaper", "cheapest", "cheap", "cost", "costs", "price", "prices", "worth it",
           "worth buying", "worth the money", "better value", "value", "more expensive",
           "expensive", "save", "saves", "saving", "save money", "money", "vs", "versus",
           "instead of breasts", "instead of fillets", "or breasts", "or fillets"),
      avoid=("turkey", "turkeys", "stuffing", "defrost", "freeze", "freezing", "frozen")),

]

_FAULT = ("went wrong", "gone wrong", "went out wrong", "went badly", "gone badly",
          "turned out wrong", "messed up", "screwed up", "ruined", "is a disaster",
          "was a disaster", "didnt work out", "didn't work out", "not gone right",
          "didnt turn out", "didn't turn out", "did not turn out", "doesnt turn out",
          "turned out badly", "turned out wrong", "was a flop", "flopped", "failed")

entry_dish_went_wrong = entry(
    "dish-went-wrong",
    (_FAULT,
     ("curry", "stew", "casserole", "gravy", "soup", "broth", "sauce", "chilli", "chili",
      "risotto", "pasta", "lasagne", "lasagna", "bolognese", "ragu", "tagine", "dal", "daal",
      "stir fry", "stir-fry", "roast", "pie", "pudding", "porridge", "rice dish",
      "chicken", "rice", "fish", "salmon", "potatoes", "mash", "pizza", "noodles",
      "meatballs", "meatloaf", "takeaway", "food", "dinner", "dish", "meal",
      "supper")),
    "Nearly always one of four things: too thin (simmer it uncovered for ten minutes), too salty "
    "(bulk it out with more of what is already in it, not water), caught on the bottom (into a "
    "clean pan, without scraping the base), or bland (salt a little, then a squeeze of lemon or a "
    "splash of vinegar). Tell me which it is and I will give you the fix for that dish.",
    avoid=("cake", "cakes", "sponge", "bread", "loaf", "scone", "scones", "pastry", "biscuit",
           "biscuits", "cookie", "cookies", "brownie", "brownies", "muffin", "muffins",
           "oven", "fridge", "freezer", "dishwasher", "washing machine", "washer", "boiler",
           "microwave", "kettle", "blender", "toaster", "hob", "cooker",
           "pan", "evening", "date", "day", "weekend", "holiday", "meal out", "dinner out",
           "party", "parties", "guests", "hosting",
           "eggs", "egg", "scrambled", "poached", "boiled",
           "pizza", "pizzas"),
    guard=a_plan_that_might_be_ruined)

entry_bake_went_wrong = entry(
    "bake-went-wrong",
    (_FAULT,
     ("cake", "cakes", "sponge", "bread", "loaf", "loaves", "scone", "scones", "pastry",
      "biscuit", "biscuits", "cookie", "cookies", "brownie", "brownies", "muffin", "muffins",
      "bun", "buns", "yorkshire", "bake", "bakes", "baking", "sourdough", "dough",
      "pizza", "pizzas",
      "starter")),
    "Nearly always one of three: an oven running 20C cooler than it says (an oven thermometer "
    "pays for itself), too much mixing once the flour went in (stop as soon as no dry flour "
    "shows), or old raising agent - bicarbonate and baking powder lose their fizz about six "
    "months after opening. Tell me what it did - sank, dry, heavy, burnt - and I will give you "
    "the fix for it.",
    avoid=("oven", "fridge", "freezer", "dishwasher", "washing machine", "washer", "boiler",
           "microwave", "kettle", "blender", "toaster", "hob", "cooker", "pan", "pans",
           "evening", "date", "day", "weekend", "holiday", "recipe", "how do i make",
           "make a cake", "bake a cake", "without flour", "no flour", "freeze", "frozen",
           "keep", "keeping", "stale", "mouldy", "mould", "mold"),
    guard=a_plan_that_might_be_ruined)

entry_batter_went_wrong = entry(
    "batter-went-wrong",
    (_FAULT,
     ("pancake", "pancakes", "crepe", "crepes", "waffle", "waffles", "batter",
      "drop scones", "blini", "blinis", "yorkshire pudding batter")),
    "A batter that goes wrong is nearly always one of three: too thick (a splash more milk, until "
    "it runs off the whisk in a ribbon), the pan not hot enough (a drop should sizzle the moment "
    "it lands, so heat it a minute longer than feels right), or turned too early (wait for bubbles "
    "across the top and a dry-looking edge). Resting the batter fifteen minutes fixes half of "
    "them, and a pinch of baking powder lifts the thick American ones.",
    avoid=("recipe", "how do i make", "how to make", "how do you make", "shrove", "day",
           "fish", "chicken", "shop", "supermarket", "freeze", "frozen", "bought",
           "oven", "fridge", "freezer", "dishwasher", "washing machine", "microwave"))

ENTRIES.append(entry_dish_went_wrong)
ENTRIES.append(entry_bake_went_wrong)
entry_make_mayonnaise = entry(
      "make-mayonnaise",
      (("mayonnaise", "mayo", "aioli", "tartare sauce", "tartar sauce", "salad cream",
        "garlic mayo", "remoulade", "garlic aioli"),
       ("make", "making", "made", "own", "homemade", "recipe", "how do i", "how to",
        "what goes in", "from scratch", "without egg", "no egg", "egg free", "vegan")),
      "Whisk an egg yolk with a teaspoon of mustard and a pinch of salt, then add 250ml of oil in a "
      "thin thread to start with - drop by drop - and only pour faster once it has thickened; "
      "finish with a squeeze of lemon. If it splits, put a fresh yolk in a clean bowl and whisk the "
      "split batch in a spoonful at a time. Tartare sauce is mayonnaise with chopped capers, "
      "gherkins and parsley, aioli is the same with crushed garlic, and salad cream is mayonnaise "
      "loosened with vinegar and a pinch of sugar.",
      avoid=("buy", "brand", "shop", "price", "cost", "gift", "healthy", "calories", "calorie",
             "diet", "jar", "jars", "bottle", "bottles", "recycling", "bin", "keep", "keeping",
             "store", "fridge", "freeze", "gone off", "off", "split", "splits", "split sauce",
             "curdled", "sandwich", "burger", "chips"),
      bias=2)

entry_croutons = entry(
      "croutons-and-breadcrumbs",
      (("croutons", "crouton", "breadcrumbs", "bread crumbs", "panko", "toasted bread cubes"),
       ("make", "making", "own", "homemade", "from", "stale", "leftover", "left over",
        "how do i", "how to", "what can i do", "use up")),
      "Cut stale bread into cubes, toss them in olive oil with a little salt, and bake at 180C for "
      "8 to 10 minutes until they rattle in the tin - a halved garlic clove in the oil is the whole "
      "trick. For breadcrumbs, tear the bread up, blitz it or grate it on the coarse side, dry them "
      "in the same oven for 5 minutes, and they keep a month in a jar.",
      avoid=("revive", "soft again", "fresh again", "gone hard", "stuffing", "bread sauce",
             "pudding", "mouldy", "mould", "mold", "keep", "keeping", "freeze", "frozen",
             "toast", "toasted cheese"),
      bias=2)

_COUNT_WORDS = (("a dozen", 12), ("four", 4), ("five", 5), ("six", 6), ("seven", 7), ("eight", 8),
                ("nine", 9), ("ten", 10), ("eleven", 11), ("twelve", 12), ("sixteen", 16),
                ("twenty", 20))


def _spoken(line, word):
    return re.search(r"(?<![a-z0-9])" + re.escape(word) + r"(?![a-z0-9])", line) is not None


_THE_MEAL_NAMED = re.compile(
    r"\b(?:roast|sunday (?:lunch|dinner)|christmas dinner|xmas dinner|turkey dinner|"
    r"cooking (?:for|a meal)|doing the dinner)\b", re.I)
_THE_TABLE_NAMED = re.compile(
    r"\b(?:for\s+)?(?P<n>\d{1,2}|a dozen|one|two|three|four|five|six|seven|eight|nine|ten|"
    r"eleven|twelve|sixteen|twenty)\s*"
    r"(?:people|persons?|adults?|kids|children|guests?|of us|coming|eating)\b"
    r"|\broast(?:\s+is)?\s+for\s+(?P<only>\d{1,2}|a dozen|one|two|three|four|five|six|seven|eight|"
    r"nine|ten|eleven|twelve|sixteen|twenty)\b", re.I)
_TABLE_WORDS = {"a dozen": 12, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
                "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
                "sixteen": 16, "twenty": 20}
_A_TABLE_PUT_RIGHT = re.compile(r"\b(?:actually|no|nope|sorry|make it|change it|instead)\b", re.I)


def _the_table_the_chat_set(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return 0
    for turn in reversed(turns[-8:]):
        said = " ".join(str((turn or {}).get("user") or "").lower().split())
        if not said:
            continue
        found = _THE_TABLE_NAMED.search(said)
        if not found or not (_THE_MEAL_NAMED.search(said) or _A_TABLE_PUT_RIGHT.search(said)):
            continue
        raw = (found.group("n") or found.group("only") or "").lower()
        count = int(raw) if raw.isdigit() else _TABLE_WORDS.get(raw, 0)
        if 2 <= count <= 30:
            return count
    return 0


def _roast_head_count(line):
    for found in re.findall(r"(?<![a-z0-9])(\d{1,2})(?![a-z0-9])", line):
        count = int(found)
        if 4 <= count <= 30:
            return count
    for word, count in _COUNT_WORDS:
        if _spoken(line, word):
            return count
    return 0


def _kilos(count):
    grams = count * 250
    if grams % 1000 == 0:
        return "%dkg" % (grams // 1000)
    if grams % 500 == 0:
        return "%d.5kg" % (grams // 1000)
    return "%.2fkg" % (grams / 1000.0)


def _the_time_a_joint_needs(grams):
    minutes = int(grams / 25) + 20
    hours, minutes = divmod(minutes, 60)
    if hours > 1:
        return "%d hours %d minutes" % (hours, minutes) if minutes else "%d hours" % hours
    if hours == 1:
        return "an hour and %d minutes" % minutes if minutes else "an hour"
    return "%d minutes" % minutes


_NOT_THE_CROWD_CARD = (
    "chicken", "beef", "lamb", "pork", "turkey", "duck", "goose", "gammon", "ham",
    "joint", "potato", "potatoes", "carrot", "carrots", "parsnip", "parsnips",
    "yorkshire", "stuffing", "gravy", "temperature", "temp", "gas mark", "defrost",
    "frozen", "freeze", "leftover", "leftovers", "vegan", "vegetarian", "veggie",
    "plant based", "nut roast", "slow cooker", "air fryer", "roast veg", "roast vegetables",
    "roasted veg", "roasted vegetables", "soggy", "dry", "burnt", "bland", "recipe", "ideas",
    "what goes with", "menu", "sides")


def _the_dish_the_line_names(line):
    for word in _NOT_THE_CROWD_CARD:
        if re.search(r"(?<!\w)" + re.escape(word) + r"(?!\w)", line):
            return True
    from .dishes import dishes_ruled_out
    return "sunday-roast" in dishes_ruled_out(line)


def _roast_for_a_crowd(memory, understood):
    line = " " + re.sub(r"[^a-z0-9' ]+", " ", str((understood or {}).get("clean")
                                                 or (understood or {}).get("text")
                                                 or "").lower()) + " "
    if _the_dish_the_line_names(line):
        return None
    count = _roast_head_count(line) or _the_table_the_chat_set(memory)
    if not count:
        return (
            "Allow about 250g of raw meat each with the bone in, or 150g boneless: six people "
            "want a 2kg chicken or a 1.5kg joint. Work backwards from the time you want to eat: "
            "meat in at 190C (170C fan) " + _the_time_a_joint_needs(2000) + " before, because a 2kg bird "
            "is 20 minutes per 500g plus 20. Potatoes in an hour before, parboiled and "
            "rough in hot fat at 200C for 45 minutes. Stuffing and pigs in blankets 25 minutes "
            "before the end, greens 10. The meat comes out to rest 15 minutes under foil, and "
            "the gravy is made in the tin while it does.")
    kilos = _kilos(count)
    length = _the_time_a_joint_needs(count * 250)
    return (
        "For %d people allow about 250g of raw meat each with the bone in, or 150g boneless, so "
        "buy about %s in total: one joint that size, or two good-sized chickens. "
        "Work backwards from the time you want to eat: meat in at 190C (170C fan) %s "
        "before, because a joint is 20 minutes per 500g plus 20. Potatoes in an hour "
        "before, parboiled and rough in hot fat at 200C "
        "for 45 minutes. Stuffing and pigs in blankets 25 minutes before the end, greens 10. "
        "The meat comes out to rest 15 minutes under foil, and the gravy is made in the tin "
        "while it does." % (count, kilos, length))


entry_roast_for_a_crowd = entry(
      "roast-for-a-crowd",
      (("sunday roast", "roast dinner", "roast lunch",
        "sunday lunch", "sunday dinner", "roast", "roasting"),
       ("timings", "timing", "timetable", "what time", "when do i start", "when should i start",
        "work back", "work backwards", "for four", "for 4", "for five", "for 5", "for six", "for 6",
        "for seven", "for 7", "for eight", "for 8", "for nine", "for 9", "for ten",
        "for 10", "for eleven", "for 11", "for twelve", "for 12",
        "for six people", "for eight people", "for ten people",
        "how much meat", "how much should i buy", "quantity", "per head", "per person",
        "how many", "plan", "schedule", "order of things")),
      _roast_for_a_crowd,
      ask=("timing", "timings", "time", "timetable", "plan", "schedule", "when", "start",
           "how long", "much", "many", "order", "quantity", "per head", "per person",
           "for four", "for 4", "for five", "for 5", "for six", "for 6", "for seven", "for 7",
           "for eight", "for 8", "for nine", "for 9", "for ten", "for 10", "for eleven", "for 11",
           "for twelve", "for 12"),
      bias=1)


ENTRIES.append(entry_make_mayonnaise)
ENTRIES.append(entry(
    "whole-chicken-meals",
    (("whole chicken", "whole bird", "whole roast chicken", "a chicken"),
     ("how many meals", "how many people", "how many portions", "feed", "feeds", "serves",
      "go round", "goes round", "go far", "goes far", "how far", "far", "enough for", "last",
      "stretch")),
    "Two meals from a 1.5kg bird, three from a 2kg one: four roast portions, then enough "
    "stripped off the frame for two more in a curry, a stir-fry or sandwiches - about 600g of "
    "cooked meat from 1.5kg, because a third of the raw weight is bone, skin and water. The "
    "frame then gives roughly 2 litres of stock, which is a soup or a risotto, and the fat "
    "roasts the potatoes.",
    ask=("chicken", "bird"),
    avoid=("how long", "oven", "roast it", "temperature", "defrost", "frozen", "freeze",
           "cheaper", "cost", "price", "value", "worth", "per person", "grams", "kg",
           "how much chicken", "stock cube", "curry recipe", "leftover chicken",
           "breast", "breasts", "fillet", "fillets", "thigh", "thighs", "wing", "wings",
           "leg", "legs", "drumstick", "drumsticks", "mince", "diced", "strips",
           "in advance", "prepare", "prep", "keep", "fridge", "freezer", "cold", "raw",
           "how long", "safe", "reheat", "defrost")))

ENTRIES.append(entry_croutons)
ENTRIES.append(entry_batter_went_wrong)
ENTRIES.append(entry_roast_for_a_crowd)


_loaf_collapse_text = (
    "A loaf that collapses rose and then fell back, which is a prove that ran too long: the yeast "
    "has eaten its sugar and the gluten that held the bubbles gives way when the heat hits it. "
    "Shape it and prove it only until a floured finger pressed in leaves a dent that springs back "
    "slowly - if the dent stays, it is ready, and if it fills at once it is not. Bake it at 220C "
    "(200C fan) and leave the door shut for the first 20 minutes, and cut the water and yeast "
    "slightly next time; a loaf that also smells of alcohol went well past ready.")

entry_loaf_collapse = entry(
    "loaf-collapse",
    (("bread", "loaf", "loaves", "sourdough", "sourdough loaf", "buns", "roll", "rolls",
      "focaccia", "tin loaf", "white loaf", "wholemeal loaf"),
     ("collapse", "collapses", "collapsed", "collapsing", "caved in", "caves in",
      "fell in", "falls in", "fell", "deflated", "deflates", "shrunk", "shrinks")),
    _loaf_collapse_text,
    avoid=("dense", "sank", "sunken", "sinking", "flat", "didnt rise", "did not rise",
           "not rising", "wont rise", "won't rise", "crumbly", "stale", "mouldy", "mould",
           "mold", "freeze", "frozen", "recipe", "how do i make", "how long", "shelf life",
           "how to make", "oven temperature", "starter", "cake", "cakes",
           "banana", "malt", "soda"))
ENTRIES.append(entry_loaf_collapse)

entry_rises_then_drops = entry(
    "rises-then-drops",
    (("rise", "rises", "risen", "rising", "goes up", "went up", "puffs up", "puffed up",
      "comes up", "came up", "springs up", "sprung up", "proves up", "proved up"),
     ("drops", "dropped", "drops back", "dropped back", "falls", "fall", "fell", "fallen",
      "falls back", "fell back", "sinks", "sink", "sinking", "sank", "sunk", "collapses",
      "collapse", "collapsed", "collapsing", "deflates", "deflate", "deflated", "caves in",
      "cave in", "caved in", "flops", "flop", "flopped", "deflated")),
    _loaf_collapse_text,
    avoid=("cake", "cakes", "sponge", "souffle", "soufflé", "yorkshire", "pudding", "muffin",
           "muffins", "scone", "scones", "meringue", "how long", "keep", "keeps", "shelf life",
           "recipe", "freeze", "frozen", "starter", "flat"),
)
ENTRIES.append(entry_rises_then_drops)

entry_starter_dying = entry(
    "starter-dying",
    (("sourdough starter", "sour dough starter", "starter", "starters", "levain", "sourdough"),
     ("dying", "died", "dies", "dead", "killed", "killing", "not rising", "isnt rising",
      "isn't rising", "stopped rising", "stopped growing", "wont rise", "won't rise",
      "not bubbling", "stopped bubbling", "no bubbles", "flat and lifeless")),
    "A starter that has stopped rising is usually hungry, cold or both: give it equal weights of "
    "flour and water, about its own weight, at room temperature (20 to 25C) and it should double "
    "in four to eight hours. If it has gone quiet, feed it twice a day for three or four days "
    "without putting it back in the fridge, and use wholemeal or rye flour for one of those feeds, "
    "which wakes it faster than white. A dark liquid on top is alcohol, not death: pour it off and "
    "feed. Mould - pink, black or furry - is the only one to throw away.",
    avoid=("how do i make", "how to make", "start from scratch", "from scratch", "name",
           "call it", "recipe", "buy", "shop", "freeze", "frozen", "fridge",
           "mould", "mold", "pink", "black",
           "bread", "breads", "loaf", "loaves", "dough", "roll", "rolls", "boule", "batard"))
ENTRIES.append(entry_starter_dying)

_STARTER_NAMES = ("sourdough starter", "sour dough starter", "starter", "starters", "levain",
                  "sourdough", "sour dough")

entry_starter_mould = entry(
    "starter-mould",
    (_STARTER_NAMES,
     ("mould", "mold", "mouldy", "moldy", "fur", "furry", "fuzz", "fuzzy", "green", "black",
      "pink", "orange", "white film", "white layer", "skin on top", "gone off", "ruined")),
    "Look at the colour before you do anything. A white or creamy film on top, with no fur on it, "
    "is kahm yeast and the starter is fine: skim it off, move the jar to a clean one and feed it. "
    "Anything furry, or pink, orange, green or black, means mould has gone through the jar - "
    "throw it out and start again, because the spores are in the flour and not just on the "
    "surface. Wash the jar with hot soapy water before the next one, and keep the sides scraped "
    "down so nothing grows on the rim.",
    avoid=("bread", "breads", "loaf", "loaves", "cake", "cakes", "muffin", "muffins", "bun",
           "buns", "jam", "cheese", "yoghurt", "yogurt", "fruit", "freeze", "frozen", "name",
           "call it", "recipe", "how do i make", "how to make", "ratio"))

entry_starter_keeping = entry(
    "starter-keeping",
    (_STARTER_NAMES,
     ("keep", "keeping", "store", "storing", "fridge", "refrigerator", "how long", "last",
      "leave it", "leave my", "holiday", "holidays", "away", "two weeks", "a week", "month",
      "months", "travel", "forget", "forgot", "neglect")),
    "A starter in the fridge will sit for weeks without much harm and months if you feed it now "
    "and then: once a week is plenty in the cold, and a grey liquid on top is alcohol, which you "
    "pour off. Before you bake, take it out, feed it and let it double at room temperature, and "
    "feed it twice a day for two days if it has been in there a while. Going away for a month is "
    "fine - feed it thick, spread a spoonful on baking parchment, dry it and it can be woken up "
    "afterwards.",
    avoid=("how do i feed", "how to feed", "feed it", "feeding", "ratio", "flour and water",
           "mould", "mold", "mouldy", "moldy", "name", "call it", "recipe", "how do i make",
           "how to make", "not rising", "wont rise", "died", "dead", "milk", "cheese", "meat"))

entry_starter_smell = entry(
    "starter-smell",
    (_STARTER_NAMES,
     ("smell", "smells", "smelling", "smelly", "stinks", "stink", "whiff",
      "acetone", "nail polish", "nail varnish", "vinegar", "vinegary", "sharp",
      "sickly", "alcohol", "beery")),
    "Sniff it and match the smell: yoghurt or beer is a healthy starter at work and nothing needs "
    "doing; acetone or nail polish means it has run out of food and is making alcohol, so pour "
    "off any liquid on top and feed it twice a day until it smells of yoghurt again; vinegar or "
    "a sharp sourness is the same thing further along, so feed it more often than once a day "
    "and use a splash of it in a bake rather than a whole loaf.",
    avoid=("mould", "mold", "mouldy", "moldy", "fur", "fuzzy", "pink", "orange", "green film",
           "not rising", "wont rise", "stopped rising", "died", "dead", "how do i feed",
           "how to feed", "feeding ratio", "how do i make", "how to make", "name", "call it",
           "recipe", "milk", "cheese", "yoghurt pot", "yogurt pot", "bread", "loaf",
           "loaves"),
    bias=2)

ENTRIES.append(entry_starter_mould)
ENTRIES.append(entry_starter_keeping)
ENTRIES.append(entry_starter_smell)

entry_soup_curdle = entry(
    "soup-curdle",
    (("soup", "soups", "broth", "bisque", "chowder", "minestrone", "soup pot", "pot of soup"),
     ("curdle", "curdles", "curdled", "curdling", "split", "splits", "splitting",
      "separated", "separates", "separating", "grainy", "grainy bits")),
    "A creamy or egg-thickened soup curdles when it gets too hot or too sharp: keep it under a "
    "simmer - small bubbles at the edge, never a rolling boil - and stir the cream, yogurt or egg "
    "in off the heat at the very end. Acid does the same, so add wine, lemon or tomatoes early and "
    "let them cook down before the dairy goes in, and a pinch of bicarbonate of soda in a "
    "tomato soup stops the split. If it has already gone, take it off the heat and blend it smooth "
    "with a little cold cream, or whisk in a cornflour slurry and warm it gently.",
    avoid=("sauce", "sauces", "custard", "hollandaise", "mayonnaise", "cheesecake", "cake",
           "cream sauce", "gravy", "curry", "recipe", "how do i make", "how to make",
           "freeze", "frozen", "fridge", "how long", "shelf life"))
ENTRIES.append(entry_soup_curdle)

entry_no_eggs = entry(
      "baking-without-eggs",
      (("no eggs", "without eggs", "out of eggs", "no egg", "egg free", "eggless",
        "eggless"),
       ("bake", "baking", "cake", "cakes", "biscuits", "cookies", "muffins", "scones", "sweet",
        "dessert", "pudding", "traybake", "recipe", "what can i bake")),
      "Plenty bakes without eggs: shortbread, flapjack, a fruit crumble, icebox biscuits and most "
      "traybakes need none at all. If a recipe wants an egg for binding, a tablespoon of ground "
      "flaxseed in three of water stands in for one, and a tablespoon of yogurt or half a mashed "
      "banana does the same job in a cake. Add a splash more milk, because egg is liquid too.",
      avoid=("instead", "replace", "substitute", "swap", "swap out", "egg free cake",
             "dinner", "tea", "supper", "buy", "shop", "sainsbury", "tesco", "price", "cost",
             "calories", "vegan", "gluten", "sank", "sinking", "sunny border", "plant",
             "freeze", "keep", "cook", "dinner", "tea"),
      bias=3)

entry_bored_of_chicken = entry(
      "bored-of-chicken",
      (("chicken", "chicken breast", "chicken breasts", "chicken thigh", "chicken thighs",
        "chicken wing", "chicken wings", "chicken drumsticks", "roast chicken", "whole chicken",
        "chicken pieces"),
       ("bored", "boring", "bored of", "fed up", "sick of", "tired of", "every night",
        "every day", "same thing", "different", "something else", "ideas", "other ideas",
        "another way", "change",
        "not a roast", "no roast", "isnt a roast", "instead of a roast", "apart from a roast",
        "other than a roast", "besides a roast", "what can i make", "what can i cook",
        "what can i do", "what else can i make", "what else can i do", "something with chicken")),
      "The fastest change is the cut and the heat rather than a new recipe: thighs roasted hot "
      "with paprika and lemon (200C for 35 to 40 minutes), breasts bashed flat and griddled in "
      "four minutes, wings salted and roasted at 200C for 45, or the whole bird pulled into tacos "
      "with lime and yogurt. After that it is the sauce that stops it being the same dinner - a "
      "traybake with chorizo and chickpeas, a satay with peanut butter and soy, or a tray of "
      "thighs marinated in yogurt and curry powder.",
      avoid=("was lovely", "was delicious", "came out", "how long", "temperature", "calories",
             "healthy", "buy", "price", "raw", "frozen", "defrost", "freeze", "bone",
             "leftover", "leftovers", "left over", "cooked", "cold chicken", "sandwich",
             "sandwiches", "salad", "salads", "shred", "shredded", "use up", "using up",
             "can i eat", "ok to eat", "okay to eat", "safe to eat", "good for", "is chicken",
             "how often", "how much", "too much", "should i eat", "is it bad"),
      bias=3)

entry_bread_did_not_rise = entry(
      "bread-did-not-rise",
      (("bread", "loaf", "dough", "bread dough", "sourdough"),
       ("not rise", "not risen", "did not rise", "hasnt risen", "hasn't risen",
        "hasnt proved", "hasn't proved", "why did", "why has", "why is", "what went wrong",
        "what happened")),
      "Four things stop a loaf rising, in the order worth checking. The yeast is dead - test it in "
      "warm water with a pinch of sugar and it should foam in ten minutes; water over about 45C, or "
      "a tin past its date, kills it. The water was too hot or too cold, so the dough never got "
      "going. The salt went in on top of the yeast and stalled it - keep them apart until the flour "
      "is in. Or it simply had not had long enough somewhere warm: doubling takes 1 to 2 hours at "
      "25C and much longer in a cold kitchen. A dough that rose and then fell was left too long.",
      avoid=("how do i make bread rise", "how long to prove", "how long do i prove", "recipe",
             "how do i make bread", "stale", "mouldy", "keep", "freeze", "buy", "price",
             "gluten free", "no yeast", "without yeast", "sourdough",
             "sticky", "crumbly", "dense", "sank", "sunken", "pastry",
             "soggy in the middle", "wet in the middle", "doughy", "raw in the middle",
             "gummy", "wet inside", "stodgy",
             "not cooked in the middle", "not bake in the middle", "not cook in the middle",
             "collapse", "collapses", "collapsed", "collapsing", "caved", "deflated", "fell"),
      bias=2)

ENTRIES.append(entry_no_eggs)
ENTRIES.append(entry_bored_of_chicken)
ENTRIES.append(entry_bread_did_not_rise)

entry_score_the_loaf = entry(
      "score-the-loaf",
      (("bread", "loaf", "loaves", "sourdough", "dough", "boule", "batard", "baguette", "rolls",
        "buns", "focaccia"),
       ("score", "scored", "scoring", "scores", "slash", "slashed", "slashing", "slashes",
        "cut the top", "cut into the top", "snip the top", "top of the loaf", "top of the bread",
        "split at the side", "splits at the side", "burst at the side", "bursts at the side",
        "split down the side", "burst open", "bursts open", "split open", "splits open",
        "cracked open", "cracks open", "crack on top", "cracked on top", "split on top")),
      "Yes - one slash about 1cm deep at a shallow angle is what decides where the loaf opens, "
      "so it rises where you cut instead of tearing wherever the crust is thinnest. Do it with a "
      "wet blade just before the loaf goes in, not before the final prove, or the cut closes up "
      "again. A tin loaf needs no slash, because the tin holds the sides and the top is free to "
      "rise; a round loaf or a long one on a tray wants one slash along it or a cross on top.",
      avoid=("did not rise", "not risen", "not rise", "dense", "crumbly", "sank", "collapsed",
             "stale", "mouldy", "freeze", "recipe", "buy", "price", "calories", "sourdough starter",
             "cake", "cakes", "pastry", "score a goal", "score points", "score in", "test score",
             "credit score", "music", "sheet music", "film", "game", "match"))

ENTRIES.append(entry_score_the_loaf)
MAKE_AT_HOME = ("make", "making", "made", "home", "at home", "homemade", "home made", "myself",
                "own", "from scratch", "recipe", "churn", "churning", "ferment", "fermenting",
                "starter", "culture")

ENTRIES.append(entry(
    "make-butter",
    (("butter", "buttermilk"),
     MAKE_AT_HOME + ("cream", "double cream", "churn")),
    ("Churn double cream past whipped cream and it splits into butter and buttermilk: 300ml of "
     "double cream at room temperature, beaten in a food processor or shaken in a jar for 10 "
     "minutes, first goes thick, then grainy, then sloshes. Pour the buttermilk off, rinse the "
     "butter in ice-cold water and squeeze it dry with the back of a spoon, work in salt to "
     "taste, and it keeps 2 weeks in the fridge. The buttermilk is for scones or pancakes."),
    avoid=("keep", "keeps", "keeping", "gone off", "rancid", "freeze", "frozen",
           "peanut", "peanuts", "peanut butter", "almond butter", "cashew", "nut butter",
           "substitute", "instead", "replace", "swap", "healthy", "healthier", "bad for you",
           "calories", "cholesterol", "dairy free", "vegan", "how much", "how many", "grams",
           "price", "cost", "cheap", "buy", "salted or unsalted", "lurpak", "brand",
           "shortbread", "cake", "pastry", "toast", "sandwich"),
    bias=2))

ENTRIES.append(entry(
    "make-ice-cream",
    (("ice cream", "icecream", "gelato", "sorbet"),
     MAKE_AT_HOME + ("machine", "churn", "freezer", "without a machine", "no churn")),
    ("No machine needed: whip 300ml of double cream to soft peaks, fold in a 397g tin of "
     "condensed milk and whatever flavouring you like, and freeze it in a loaf tin for 4 hours, "
     "stirring it twice in the first hour. The creamier way is a custard - 4 yolks, 100g sugar "
     "and 500ml of milk and cream cooked to 80C - frozen in a tub and beaten every 30 minutes "
     "three times. Home-made ice cream wants eating within a fortnight."),
    avoid=("keep", "keeps", "keeping", "last", "lasts", "lasting", "still good",
           "use by", "go off", "gone off", "out of date",
           "melted", "melting", "soft", "scoop", "shop",
           "icy", "ice crystals", "crystals", "crystallised", "crystalised", "freezer burn",
           "grainy", "hard as a rock", "stops it going icy", "going icy", "went icy",
           "buy", "brand", "ben and jerrys", "healthy", "calories", "sugar", "dairy free",
           "vegan", "lactose", "milk free", "price", "cost", "vanilla ice cream",
           "strawberry ice cream", "which ice cream", "best ice cream"),
    bias=2))

ENTRIES.append(entry(
    "make-pasta",
    (("pasta", "tagliatelle", "fettuccine", "ravioli", "pappardelle"),
     MAKE_AT_HOME + ("dough", "flour", "egg", "eggs", "semolina", "fresh")),
    ("Fresh pasta is 100g of tipo 00 flour and one large egg per person, mixed to a stiff dough, "
     "kneaded 5 minutes and rested 30 minutes under a bowl, then rolled as thin as you can and "
     "cut. It cooks in 2 to 3 minutes in salted water, not the 10 a dried pasta takes. Semolina "
     "and water with no egg is the southern way, and it wants a rolling pin or a machine."),
    avoid=("how long", "cook", "cooking", "boil", "al dente", "sauce", "bake", "baked",
           "lasagne", "shape", "shapes", "gluten free", "instead", "substitute", "keep",
           "leftover", "calories", "healthy", "dried", "packet", "brand", "barilla",
           "price", "cost", "how much pasta", "portion", "grams per person",
           "too much", "made too much", "make too much", "left over", "left over pasta"),
    bias=2))

ENTRIES.append(entry(
    "make-soft-cheese",
    (("cottage cheese", "cream cheese", "soft cheese", "ricotta", "mascarpone", "quark",
      "paneer", "halloumi", "cheese"),
     MAKE_AT_HOME + ("milk", "vinegar", "lemon", "rennet", "curdle", "curds")),
    ("Warm 2 litres of whole milk to 80C - steaming, not boiling - stir in 3 tablespoons of "
     "lemon juice or white vinegar, and it separates into curds and whey. Strain it through a "
     "muslin for 20 minutes for a soft curd to eat that day, four hours for a cottage cheese, or "
     "overnight with a weight on it for a paneer you can fry. Add a pinch of salt and a splash "
     "of the whey back at the end, and keep it 5 days."),
    avoid=("keep", "keeps", "keeping", "gone off", "healthy", "calories", "protein",
           "instead", "substitute", "buy", "shop", "brand", "philadelphia", "price", "cost",
           "cake", "cheesecake", "on toast", "sauce", "melt", "melted", "grated", "toastie",
           "sandwich", "board", "baked", "macaroni", "pizza", "topping"),
    bias=2))

ENTRIES.append(entry(
    "make-kefir",
    (("kefir", "water kefir", "milk kefir"),
     MAKE_AT_HOME + ("grains", "milk", "culture", "starter", "ferment")),
    ("Milk kefir is 1 to 2 tablespoons of live kefir grains in a litre of whole milk in a jar "
     "with a loose lid, left out of the fridge for 24 hours and then strained: the grains go back "
     "in fresh milk and the kefir goes in the fridge. The grains grow, so give the extra away. "
     "With no grains, 2 tablespoons of live yoghurt or buttermilk starts it off, though it stops "
     "after a few lots. It keeps a week."),
    avoid=("keep", "keeps", "keeping", "healthy", "good for you", "gut", "probiotic",
           "buy", "shop", "brand", "price", "cost", "dairy free", "lactose", "calories",
           "where can i buy"),
    bias=2))

ENTRIES.append(entry(
    "make-ketchup",
    (("ketchup", "tomato ketchup", "catsup"),
     MAKE_AT_HOME + ("tomatoes", "tomato", "sauce", "sugar", "vinegar")),
    ("Simmer 1kg of tomatoes with an onion, 100g of sugar, 150ml of vinegar, a teaspoon of salt "
     "and a spice bag of cloves, peppercorns and a bay leaf for 45 minutes, then blend it and "
     "simmer it down until a spoon dragged across the pan leaves a line. Push it through a sieve "
     "and bottle it hot: it keeps a month in the fridge once opened. Tinned tomatoes and half the "
     "sugar make a thinner, sharper ketchup."),
    avoid=("keep", "keeps", "keeping", "healthy", "sugar", "calories", "instead",
           "substitute", "buy", "shop", "brand", "heinz", "price", "cost", "on chips",
           "with chips", "how much"),
    bias=2))

ENTRIES.append(entry(
    "make-peanut-butter",
    (("peanut butter", "nut butter", "almond butter", "cashew butter", "peanuts"),
     MAKE_AT_HOME + ("peanut", "peanuts", "nuts", "blitz", "roast")),
    ("Roast 300g of shelled peanuts at 180C (160C fan) for 10 minutes until they smell nutty, "
     "then blitz them in a food processor for 3 to 5 minutes, scraping down the sides: first it is "
     "crumbs, then a ball, then suddenly a smooth butter. Add a pinch of salt and a teaspoon of "
     "honey, and a spoon of oil if you want it looser. It keeps a month in a jar."),
    avoid=("keep", "keeps", "keeping", "healthy", "calories", "protein", "instead",
           "substitute", "buy", "shop", "brand", "price", "cost", "sandwich", "toast",
           "allergy", "allergic", "reaction", "dogs",
           "pregnant", "pregnancy", "expecting", "every day", "a day", "portion", "serving",
           "good for you", "good for me",
           "baby", "babies", "toddler", "toddlers", "my son", "my daughter", "weaning",
           "first foods", "first tastes", "highchair", "high chair",
           ),
    bias=2, ask=MAKE_AT_HOME))

ENTRIES.append(entry(
    "nut-butter-separates",
    (("peanut butter", "nut butter", "almond butter", "cashew butter"),
     ("separat", "separates", "separating", "separated", "oily", "oil on top", "stir",
      "stirring", "runny", "liquid", "grainy", "hard", "stiff", "fridge", "upside down",
      "store", "storing", "storage", "keep", "keeping", "keeps")),
    "Natural nut butter separates because there is nothing in it but nuts: the oil rises and the "
    "solids sink. Stir it back in with a knife, from the bottom of the jar upwards, and it comes "
    "together in a minute or two. A jar that has set hard mixes more easily if it stands upside "
    "down for a day first, and standing it in a bowl of warm water for five minutes softens it "
    "without cooking it. An opened jar keeps a few months in the cupboard and longer in the "
    "fridge, though cold makes it stiffer to spread.",
    avoid=("make", "making", "recipe", "blitz", "roast", "roasted", "homemade", "calories",
           "healthy", "allergy", "allergic", "baby", "sandwich", "toast", "brand", "best",
           "buy", "shop", "cost", "price", "cookie", "cake", "biscuit"),
    bias=2))
ENTRIES.append(entry(
    "make-ice-lollies",
    (("ice lollies", "ice lolly", "popsicles", "popsicle", "ice pops", "lolly", "lollies"),
     MAKE_AT_HOME + ("juice", "mould", "moulds", "molds", "sticks", "freezer", "fruit")),
    ("Blend or mash soft fruit with a little sugar and lemon - strawberries, mango, berries, or "
     "just orange juice - and pour it into moulds or paper cups with a stick in, leaving a "
     "centimetre at the top because water expands. Four to six hours in the freezer. A splash of "
     "yoghurt or milk makes them creamier, and a spoon of vodka stops them going rock hard."),
    avoid=("keep", "keeps", "keeping", "melted", "melting", "shop", "buy", "brand",
           "healthy", "sugar", "calories", "price", "cost", "toddler", "baby", "choking"),
    bias=2))

ENTRIES.append(entry(
    "make-baked-beans",
    (("baked beans", "beans on toast", "haricot beans", "cannellini beans"),
     MAKE_AT_HOME + ("tomato", "tomatoes", "sugar", "haricot", "dried")),
    ("Soak 250g of dried haricot beans overnight, boil them hard for 10 minutes then simmer for "
     "an hour until soft (or start from two tins). Simmer a tin of tomatoes with an onion, a "
     "tablespoon of black treacle or brown sugar, a teaspoon of mustard, a splash of vinegar and "
     "a pinch of salt for 20 minutes, stir the beans in and bake at 160C (140C fan) for 40 "
     "minutes. It keeps 4 days and freezes."),
    avoid=("keep", "keeps", "keeping", "healthy", "calories", "sugar", "instead",
           "substitute", "buy", "shop", "brand", "heinz", "price", "cost", "on toast",
           "how long do i cook", "tin of"),
    bias=2))

ENTRIES.append(entry(
    "make-sausages",
    (("sausages", "sausage meat", "sausagemeat"),
     MAKE_AT_HOME + ("mince", "meat", "pork", "casings", "skins", "seasoning")),
    ("Sausages are 70/30 lean pork to fat, minced coarse and kept cold: for 1kg of shoulder add "
     "18g of salt, a teaspoon of pepper, a teaspoon of sage and 100ml of iced water, mix it until "
     "it is sticky, and stuff it into soaked hog casings - or shape it into patties, which needs "
     "no casing at all. Fry a small piece to taste for salt before you stuff the rest. Eat them "
     "within 3 days or freeze them."),
    avoid=("keep", "keeps", "keeping", "healthy", "calories", "protein", "instead",
           "substitute", "buy", "shop", "brand", "price", "cost", "how long do i cook",
           "how do i cook", "in the oven", "air fryer", "barbecue", "bangers"),
    bias=2))

ENTRIES.append(entry(
    "yoghurt-fermenting",
    (("yoghurt", "yogurt", "yoghurt maker", "yoghurt pot"),
     ("ferment", "fermenting", "fermented", "incubate", "incubating", "incubator", "culture",
      "starter", "warm spot", "airing cupboard", "what temperature", "how warm", "set it",
      "how long do i leave", "how long to ferment", "didnt set", "did not set", "wont set")),
    ("Keep it at 43C for 8 to 12 hours: a yoghurt maker does it, an airing cupboard or an oven "
     "switched off with the light on is close enough, and a flask of it in a warm water bath "
     "works too. Below 40C it takes longer and tastes sourer, above 46C the culture dies and it "
     "stays milk. It is set when it pulls away from the side of the jar - then chill it for 4 "
     "hours before eating, which is when it firms up properly."),
    avoid=("keep", "keeps", "keeping", "use by", "past the date", "out of date", "gone off",
           "mould", "cheap", "buy", "brand", "calories", "protein", "dairy free", "lactose",
           "my starter", "the starter", "starter smells", "starter has",
           "starter is", "starter went", "starter gone"),
    bias=3))

ENTRIES.append(entry(
    "make-crisps",
    (("crisps", "potato crisps", "crisp"),
     MAKE_AT_HOME + ("potato", "potatoes", "sliced", "slices", "oven", "fry", "frying",
                     "salted", "salt", "crunchy", "crispy")),
    ("Slice floury potatoes about 2mm thin - a mandoline, or a peeler does one at a time - rinse "
     "the starch off in cold water, then dry the slices properly on a tea towel: a wet slice "
     "steams instead of crisping. Fry at 160C for 3 minutes, until the bubbling dies down, or "
     "toss them in a tablespoon of oil and bake at 200C for 15 to 20 minutes, turning once. Salt "
     "the moment they come out and cool them on kitchen paper. Dry slices and a steady "
     "temperature are the whole trick."),
    avoid=("roast", "roasts", "roasted", "roasting", "parboil", "parboiled", "parboiling",
           "sunday lunch", "yorkshire",
           "buy", "buying", "shop", "brand", "packet", "walkers", "which", "best", "healthy",
           "healthier", "bad for you", "calories", "sugar", "salt in", "how much salt",
           "baby", "toddler", "kids", "child", "keto", "air fryer", "keep", "keeps", "keeping",
           "pastry", "crumble", "apple", "shop bought", "multipack", "price", "cost", "cheap",
           "chip", "chips", "fries", "french fries", "oven chips", "chip shop",
           "roast", "roasted", "roasting", "roasties", "parboil", "parboiled", "sunday dinner"),
    bias=2))

ENTRIES.append(entry(
    "make-granola",
    (("granola", "muesli", "toasted oats", "breakfast cereal"),
     MAKE_AT_HOME + ("oats", "honey", "syrup", "nuts", "oven", "bake", "toast")),
    ("Toss 300g of oats with 100g of nuts and seeds, then stir in 3 tablespoons of oil, 3 of honey "
     "or maple syrup and a pinch of salt, and spread it thin on a lined tray. Bake at 160C (140C "
     "fan) for 20 to 25 minutes, stirring twice, until it is golden - it crisps as it cools. Add "
     "dried fruit after baking, or it burns. It keeps a month in a jar; muesli is the same mix "
     "untoasted."),
    avoid=("keep", "keeps", "keeping", "healthy", "calories", "sugar", "protein", "buy",
           "shop", "brand", "price", "cost", "which", "best", "toddler", "kids"),
    bias=2))

ENTRIES.append(entry(
    "shortbread-amounts",
    (("shortbread", "shortbreads", "shortbread fingers", "millionaires shortbread"),
     ("butter", "how much", "how many", "much", "ratio", "ratios", "flour", "sugar",
      "margarine")),
    ("Shortbread is one part sugar, two parts butter and three parts flour: for a 20cm round that "
     "is 60g caster sugar, 120g butter and 180g plain flour. Cream the butter and sugar, work in "
     "the flour without kneading it, press it into the tin, prick it, and bake at 150C (130C fan) "
     "for 35 to 40 minutes until it is pale gold rather than brown. It firms as it cools, so cut "
     "it into fingers while it is still warm."),
    avoid=("calories", "how many calories", "healthy", "diet", "buy", "shop", "supermarket",
           "brand", "price", "cost", "gluten", "vegan", "baby", "toddler", "child",
           "thermomix", "air fryer", "biscuit base", "cheesecake", "crumbly", "crumbs",
           "store", "storing", "keep", "keeps", "sealed", "freeze", "frozen",
           "food processor", "processor", "recipe", "recipes", "how do i make",
           "how long", "oven"),
    bias=2))

ENTRIES.append(entry(
    "make-fruit-jelly",
    (("apple jelly", "mint jelly", "redcurrant jelly", "crab apple jelly", "bramble jelly",
      "blackberry jelly", "quince jelly", "rowan jelly", "rosemary jelly", "damson jelly",
      "fruit jelly", "jelly", "jellies"),
     ("make", "making", "homemade", "from scratch", "how do i", "how to", "recipe",
      "apples", "apple", "mint", "redcurrants", "crab apples", "brambles", "blackberries",
      "quinces", "damsons", "strain", "muslin", "juice")),
    ("Cook the fruit with just enough water to stop it catching - apples and blackberries 20 "
     "minutes, redcurrants 10, mint as a strong vinegar infusion - then strain it through a "
     "muslin or a clean tea towel hung over a bowl and leave it overnight: squeeze it and the "
     "jelly goes cloudy. For every 600ml of juice weigh out 450g of sugar, warm them together "
     "until the sugar has gone, then boil hard to 104C (or until a drop on a cold plate "
     "wrinkles) and pot it hot. It sets in a day."),
    avoid=("didnt set", "did not set", "wont set", "won't set", "not set", "runny", "liquid",
           "how do i set", "how to set", "set a jelly", "set the jelly", "set it", "setting point",
           "when is it set", "is it set", "has it set", "how do i know when", "know when a jelly",
           "wobbly", "how long does", "keeps", "keeping", "out of date", "gone off", "mould",
           "calories", "sugar", "healthy", "buy", "shop", "brand", "price", "cost", "rowntrees",
           "hartley", "jam", "marmalade", "chutney", "crumble", "pie", "cake"),
    bias=2))

_CHILD_DRANK_IT = re.compile(
    r"\b(?:baby|babies|infant|toddler|toddlers|child|children|childs|kid|kids|boy|girl|son|"
    r"daughter|newborn|little one|grandchild|grandson|granddaughter)\b")
ENTRIES.append(entry(
    "milk-that-turned-was-drunk",
    (("milk",),
     ("drank", "drunk", "drank some", "swallowed", "sipped", "had some", "has had some",
      "gave him", "gave her", "gave my", "gave the", "off milk", "sour milk", "turned milk",
      "milk that was off", "milk that had gone off", "milk was off", "milk had gone off",
      "bad milk", "milk that turned", "curdled milk")),
    ("Sour milk is curdled and unpleasant, not poisonous: it will not give a child the food "
     "poisoning that undercooked meat does, and a mouthful or a cup is very unlikely to do "
     "anything. Offer water, and watch for vomiting or diarrhoea over the next few hours. Ring "
     "111 if the child is under one, cannot keep water down, or seems unwell rather than just "
     "cross about it. Then bin the bottle - the date is about quality, not safety."),
    avoid=("how do i know", "how can i tell", "how long", "keep", "keeps", "keeping",
           "use by", "date on the", "freeze", "frozen", "buy", "brand", "price", "cost",
           "calories", "protein", "lactose", "allergy", "allergic", "recipe", "sauce",
           "cheese", "yoghurt", "yogurt", "kefir", "breastfeeding", "formula", "cows milk",
           "which milk", "what milk", "oat milk", "soya milk", "almond milk"),
    guard=lambda understood: bool(_CHILD_DRANK_IT.search(
        " " + str((understood or {}).get("clean") or "").lower() + " ")),
    bias=3))

entry_rice_burnt = entry(
      "rice-keeps-burning",
      (("rice", "basmati", "long grain", "pilau", "risotto rice", "brown rice"),
       ("why", "keep burning", "keeps burning", "always burn", "always burning", "burning",
        "burns", "burn", "stop it burning", "stop burning", "prevent",
        "what am i doing wrong")),
      "Rice burns when there is no water left under it: the heat is too high, so the pan dries out "
      "before the grain is cooked and the bottom scorches. One mug of rice to one and a half of "
      "water, bring it to the boil with the lid on, then turn it down to the lowest ring for 10 to "
      "12 minutes without stirring - stirring rubs the starch off and makes it catch. A heavy pan "
      "and a lid that fits are most of the fix, and 5 minutes off the heat at the end finishes it.",
      ask=("why", "keep", "keeps", "always", "stop", "prevent", "wrong"),
      bias=2,
      avoid=("already burnt", "what can i do", "what do i do", "do with", "can i still eat",
             "still eat", "throw", "bin", "rescue", "save it", "burnt bits",
             "stick", "sticks", "sticking", "sticky", "stick to the pan", "catch", "catches",
             "crunchy", "crunch", "hard", "undercooked", "underdone", "raw", "mushy",
             "stodgy", "soggy", "wet", "dry", "slimy", "gluey",
             "rice pudding", "fried rice", "risotto", "paella", "sushi", "rice cooker",
             "how long", "calories", "healthy", "freeze", "reheat", "leftover rice", "buy",
             "price", "grow"))

ENTRIES.append(entry_rice_burnt)

ENTRIES.append(entry(
    "freeze-an-open-bag",
    (("freeze", "freezing", "frozen", "freezer", "thaw", "thawed", "thawing", "defrost",
      "defrosted", "defrosting"),
     ("refreeze", "re freeze", "re-freeze", "again", "twice", "already", "open", "opened",
      "bag", "packet", "pack", "opened bag", "half used", "half bag", "left out")),
    ("An open bag of frozen veg goes straight back in the freezer: press the air out, clip it, and "
     "use it within a month or two before it dries out or picks up ice. Re-freezing is the one with "
     "a rule: food that has fully thawed can be cooked and then frozen again, but not frozen raw a "
     "second time, because the thaw is when bacteria multiply and freezing does not kill them. "
     "Frozen peas that have half thawed in a warm kitchen are still peas - cook them now rather "
     "than put them back."),
    ask=("refreeze", "re freeze", "re-freeze", "again", "twice", "already", "open", "opened",
         "bag", "packet"),
    avoid=("mashed", "milk", "breast milk", "cakes", "cake", "bread", "meat", "chicken", "beef",
           "pork", "fish", "rice", "soup", "stock", "banana", "bananas", "avocado", "eggs",
           "potatoes", "cooked", "leftover", "leftovers", "put the heating", "pipes", "burst"),
    bias=2))

entry_potato_toppings = entry(
      "baked-potato-toppings",
      (("baked potato", "baked potatoes", "jacket potato", "jacket potatoes", "potato",
        "potatoes"),
       ("put on", "topping", "toppings", "top it", "fill", "filling", "fillings",
        "what can i put", "what do you put", "what should i put", "what goes on")),
      JACKET_FILL,
      ask=("put on", "topping", "toppings", "fill", "filling", "fillings", "goes on",
           "what can i put", "what do you put", "what should i put"),
      avoid=("how long", "oven", "temperature", "calories", "healthy", "buy", "price", "keep",
             "leftover", "leftovers", "freeze", "frozen", "reheat", "mash", "mashed", "chips",
             "wedges", "soup", "peel", "grow", "growing", "plant", "plants", "dog", "dogs",
             "sprout", "sprouts", "raw", "boil", "boiling", "microwave", "salad",
             "herb", "herbs", "spice", "spices", "seasoning", "rosemary", "thyme", "paprika",
             "cumin", "salt and pepper"))

ENTRIES.append(entry_potato_toppings)


_TIN_AREA = {
    "15cm": "about half",
    "18cm": "about a third less than a 20cm",
    "20cm": "the recipe's own",
    "23cm": "about a third more",
    "25cm": "about half again",
}


def _recipe_amount(memory, understood):
    said = " " + str((understood or {}).get("clean") or understood.get("text") or "").lower() + " "
    tin = any(word in said for word in (" tin ", " tins ", " sandwich tin", " cake tin"))
    other_size = any(phrase in said for phrase in
                     ("bigger", "larger", "smaller", "different size", "different tin",
                      "other tin", "wrong size", "too big", "too small", "deeper"))
    if tin and other_size:
        return ("Go by the area of the tin rather than the numbers on the page: a 23cm round holds "
                "about a third more than a 20cm, so the same batter fills it shallower and bakes "
                "5 to 10 minutes faster, and scaling the batter up by that third fills it to the "
                "same depth in the same time. Keep the oven temperature, fill to two-thirds, and "
                "check with a skewer 5 minutes before the recipe's time either way.")
    halving = any(phrase in said for phrase in
                  ("halve", "halving", "half the recipe", "half a recipe", "half this recipe",
                   "half batch", "smaller batch", "only two of us", "just for one",
                   "just me", "for two"))
    if halving:
        return ("Halve everything except the egg and the raising agent: beat the egg and weigh "
                "half of it, and keep the baking powder or yeast nearer two-thirds, because it "
                "does not scale down in a straight line. Use a smaller tin or pan so the depth "
                "stays the same, keep the temperature, and start checking 5 minutes earlier - a "
                "smaller batch comes up to heat and browns sooner.")
    return ("No - the time barely changes, the quantity does. Keep the oven or hob where it was "
            "and add 10 to 20 minutes for the extra volume to heat through and reduce, checking "
            "early rather than trusting the clock. Use a wider pot or two tins rather than a "
            "deeper one, swap two trays on their shelves halfway, and cut the liquid by about a "
            "tenth because less of it evaporates. Salt, chilli, stock and herbs do not double "
            "exactly: add three-quarters, taste, then top up.")


ENTRIES.append(entry(
    "recipe-amount",
    (("double the recipe", "double a recipe", "double this recipe", "doubling the recipe",
      "doubling a recipe", "doubling", "doubled the recipe", "double batch", "double the batch",
      "two batches", "twice as much", "make twice", "twice the recipe", "halve", "halving",
      "half the recipe", "half a recipe", "half this recipe", "half batch", "smaller batch",
      "bigger tin", "larger tin", "smaller tin", "different tin", "tin size", "bigger cake",
      "bigger dish", "smaller dish", "scale up", "scale down", "scale the recipe",
      "two at once", "cook two at once", "two at the same time", "cook two at the same time",
      "make two at once", "bake two at once", "two in the oven at once"),
     ("recipe", "recipes", "batch", "mixture", "batter", "dough", "ingredients", "quantities",
      "amount", "amounts", "tin", "tins", "cook", "cooking", "bake", "baking", "oven", "time",
      "longer", "freeze", "portion", "portions")),
    _recipe_amount,
    ask=("does", "do i", "can i", "should i", "how long", "how much", "will", "if i", "is it",
         "what", "longer", "time", "quantities", "i have", "ive got", "i've got", "i want",
         "i need", "i only", "im making", "i'm making"),
    avoid=("glazing", "glazed", "bed", "garage", "vision", "check", "checked", "dose", "doses",
           "tablets", "medicine", "paracetamol", "ibuprofen", "antibiotic", "insulin", "breast",
           "formula", "baby", "toddler", "dog", "cat", "air fryer", "slow cooker", "microwave",
           "yorkshire", "bread", "sourdough", "starter", "pizza", "roast potatoes", "turkey",
           "chicken", "chickens", "bird", "birds", "cake", "cakes", "sponge", "tray", "trays",
           "tin of", "dishes", "things", "christmas", "calories", "how many calories", "protein", "price", "cheaper", "buy",
           "supermarket", "pack", "keep", "keeps", "reheat", "leftover", "leftovers",
           "double cream", "single cream", "soured cream", "creme fraiche", "whipping cream",
           "extra thick cream", "double cream in", "a pot of cream", "cream cheese"),
    bias=1))
entry_joint_weight = entry(
      "joint-weight",
      (("joint", "joints", "roast"),
       ("what weight", "weight", "how heavy", "how big", "how much", "size", "per person",
        "each", "each person", "per head")),
      _roast_for_a_crowd,
      ask=("weight", "what weight", "how heavy", "how big", "how much", "size",
           "per person", "per head", "each"),
      avoid=("how long", "time", "timing", "timetable", "minutes", "oven", "temperature",
             "gas mark", "cook", "cooking", "done", "kilo", "kilos", "kg",
             "pound", "pounds", "lbs",
             "chicken", "turkey", "duck", "goose", "beef", "lamb", "pork", "gammon", "ham",
             "brisket", "shoulder", "leg of", "joint of", "mince", "slow cooker", "air fryer",
             "my joint", "joints hurt", "joint pain", "knee", "knees", "hip", "hips",
             "lift", "lifting", "dumbbell", "dumbbells", "barbell", "gym",
             "workout", "exercise", "squat", "squats", "press"))

ENTRIES.append(entry_joint_weight)

_PAN_THING = ("pan", "pans", "griddle", "griddle pan", "skillet", "frying pan", "wok",
              "saucepan", "non stick pan", "pan base", "flat pan", "cast iron pan")
_PAN_IS_HOT_ASK = ("hot", "hot enough", "properly hot", "up to heat", "ready", "heated",
                   "how do i know", "how can i tell", "how do you know", "when is it",
                   "when is the", "how long to heat", "how long does it take to heat",
                   "warm enough", "smoking hot")

ENTRIES.append(entry(
    "pan-heat-without-a-fat",
    (_PAN_THING, _PAN_IS_HOT_ASK),
    ("Three things, and any one of them is enough. Hold your hand an inch above the surface: it "
     "should feel properly hot after about two seconds, not straight away. Flick a few drops of "
     "water in and they should bead and skate across the pan rather than sit there and hiss. And "
     "the whole base should look faintly shimmering rather than wet. Give a heavy pan three or "
     "four minutes on a medium heat and a thin one two, and let it heat before you turn it up."),
    avoid=("oil", "oils", "butter", "fat", "lard", "ghee", "dripping", "smoke", "smoking",
           "smoke point", "season", "seasoning", "clean", "cleaning", "wash", "washed", "burnt",
           "stuck", "stick", "rust", "oven", "temperature of the oven", "gas mark", "air fryer",
           "chicken", "steak", "fish", "egg", "eggs", "pancake", "bacon", "onion", "bread",
           "buy", "price", "which pan", "what pan", "best pan", "induction", "hob", "hot plate",
           "hotplate", "barbecue", "bbq", "grill",
           "pan is hot", "wok is hot", "test the pan heat",
           "worktop", "worktops", "counter", "countertop", "work surface", "worksurface",
           "benchtop", "the table", "wooden table", "wood table", "the side", "on the side",
           "chopping board", "wooden board", "bread board", "trivet", "granite", "quartz",
           "marble", "laminate", "glass table", "stone worktop",
           "mark", "marks", "marked", "scorch", "scorched", "scorching", "stain", "stains",
           "stained", "white mark", "burn mark", "burnt the", "melted the",
           "cold water", "in water", "in the sink", "dunk", "dunking", "quench",
           "warp", "warped", "warping", "crack", "cracks", "cracked",
           "cool down", "cool the pan", "soak", "soaking"),
    bias=5))

_ORDER_ASK = re.compile(
    r"\b(?:pan|pans|wok|griddle|skillet|frying pan)\b[^.?!]{0,24}\bfirst\b"
    r"|\bfirst\b[^.?!]{0,24}\b(?:pan|oil|butter|fat)\b"
    r"|\bwhich\s+(?:one\s+)?first\b|\bpan\s+first\b|\boil\s+first\b", re.I)

ENTRIES.append(entry(
    "pan-then-oil",
    (("pan", "pans", "wok", "griddle", "skillet", "frying pan", "hot pan", "cold pan"),
     ("first", "which first", "pan first", "oil first", "butter first", "one first",
      "heat the pan", "heat the oil", "hot pan")),
    ("Pan first, then the oil. A dry pan heats evenly and you can judge its heat with your hand "
     "or a drop of water, and oil added to a pan that is already hot shimmers and moves at once "
     "instead of sitting in a cold pool. The exception is a marinade, a rub or a cold steak "
     "straight from the fridge, which goes into the hot oil rather than the bare pan."),
    avoid=("smoke", "smoking", "smoke point", "keep", "keeps", "store", "storing", "reuse",
           "reusing", "throw away", "get rid", "dispose", "drain", "oven", "air fryer",
           "first time", "my first", "first go", "first aid", "first birthday", "panini"),
    guard=lambda understood: bool(_ORDER_ASK.search(
        " " + str((understood or {}).get("clean") or "").lower() + " ")),
    bias=6))
_HERBS_GROWING = ("rosemary", "thyme", "sage", "bay", "bay leaf", "bay leaves", "oregano",
                  "mint", "basil", "coriander", "cilantro", "parsley", "dill", "chives",
                  "tarragon", "herb", "herbs")
_HERB_PLANT_WORDS = ("plant", "plants", "bush", "bushes", "tree", "pot", "pots", "flowerpot",
                     "herb pot", "patio", "window box", "garden", "allotment", "sprouting",
                     "come back", "coming back", "gone mad", "running riot", "taken over")
_HERB_USE_ASK = ("cook", "cooked", "cooking", "use", "uses", "using", "do with", "make", "made",
                 "making", "recipe", "recipes", "eat", "eating", "salad", "sauce", "pesto",
                 "stuffing", "roast", "roasting", "grill", "grilling", "bake", "baking")
_HERB_SURPLUS_WORDS = ("too much", "too many", "lots of", "loads of", "a lot of", "so much",
                       "plenty of", "glut", "glut of", "overgrown", "surplus")
_WOODY_HERB = frozenset(("rosemary", "thyme", "sage", "bay", "oregano"))


_HERB_OWNED = re.compile(r"\b(?:have|has|having|got|there's|there is|bought|given|gave)\b",
                         re.I)


def _herb_use_asked(understood):
    clean = " " + str((understood or {}).get("clean") or "").lower() + " "
    words = set(str(word).lower() for word in (understood or {}).get("words") or ())
    if words & set(_HERB_USE_ASK):
        return True
    if any(" " + word + " " in clean for word in _HERB_USE_ASK):
        return True
    if not any(" " + word + " " in clean for word in _HERB_PLANT_WORDS):
        return False
    return bool(_HERB_OWNED.search(clean))


def _herb_plant_reply(memory, understood):
    words = set(str(word).lower() for word in (understood or {}).get("words") or ())
    clean = " " + str((understood or {}).get("clean") or "").lower() + " "
    woody = bool(words & _WOODY_HERB) or any(" " + herb + " " in clean for herb in _WOODY_HERB)
    if woody:
        use = ("Use them at the start of the cooking, because heat is what opens them up: "
               "rosemary or thyme with potatoes, lamb, chicken or a tray of vegetables, sage "
               "with pork or in a brown butter, and a bay leaf in rice or a stew.")
        pick = ("Take a few sprigs from the tips rather than cutting back to the old wood, and a "
                "third off the top is the most a bush wants at once - it grows back from there. ")
    else:
        use = ("Use them at the end, off the heat, so the flavour stays - chopped into a green "
               "sauce with oil, lemon and garlic, torn over tomatoes or fish, or stirred into a "
               "soup just before it is served.")
        pick = ("Pinch the top few leaves and leave the stem, and the plant keeps going: a third "
                "off the top is plenty at once, and it grows back from the cuts. ")
    if _herb_use_asked(understood):
        return use + " " + pick.strip()
    return pick + use


ENTRIES.append(entry(
    "herb-plant-to-cook",
    (_HERBS_GROWING, _HERB_PLANT_WORDS + _HERB_SURPLUS_WORDS),
    _herb_plant_reply,
    bias=3,
    guard=_herb_use_asked,
    avoid=("grow", "grows", "growing", "grew", "propagate", "propagating", "seed", "seeds",
           "sow", "sowing", "cutting", "cuttings", "repot", "repotting", "potting", "wilt",
           "wilting", "wilts", "yellow", "yellowing", "brown", "dying", "died", "dead", "die",
           "prune", "pruning", "fertiliser", "fertilizer", "feed", "pests", "pest", "aphids",
           "frost", "winter", "indoor", "indoors", "sunlight", "shade", "soil", "compost",
           "buy", "where can i buy", "how do i keep", "keep it alive", "overwinter",
           "plugs", "seeds",
           "taken over", "take over", "taking over", "come back", "comes back", "coming back",
           "gone mad", "going mad", "running riot", "overgrown", "spreading", "spreads",
           "spread", "invasive", "taking hold",
           "safe", "unsafe", "can i eat", "is it safe", "dogs", "dog", "cats", "cat",
           "poison", "poisonous", "toxic", "pesticide", "pesticides", "kids", "toddler")))


ENTRIES.append(entry(
    "razor-clams",
    (("razor clam", "razor clams", "razor shell", "razor shells", "razor fish", "razorfish"),
     ("cook", "cooking", "prepare", "clean", "cleaning", "steam", "steaming", "grill",
      "grilling", "how do i", "how to", "what do i do", "eat", "serve", "recipe", "best way",
      "open", "shut", "sand", "grit")),
    ("Rinse them under cold water and leave them an hour in salty water so they spit out the "
     "sand, then steam or grill them for about four minutes, until the shells open. They have no "
     "beard to pull like a mussel, and any that will not open go in the bin. Garlic, chilli, "
     "lemon and parsley is all they need."),
    avoid=("shave", "shaving", "shaved", "blade", "blades", "burn", "bumps", "razor burn",
           "beard", "beard trimmer", "hair removal", "wax", "waxing", "razor blade")))


def _lined(memory, understood):
    return " " + " ".join(
        str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower().split()
    ) + " "


_CUP_OF = (
    ("flour", "plain flour", "self raising flour", "self-raising flour", "bread flour",
     "spelt", "wholemeal",
     "Spoon the flour into the cup and level it off with a knife - a scoop straight from the bag "
     "packs in up to a fifth more, which is the difference between a light cake and a heavy one. "
     "A cup of plain flour is about 120g, and a level tablespoon about 8g."),
    ("sugar", "caster sugar", "granulated", "brown sugar", "icing sugar", "muscovado",
     "Spoon white sugar into the cup and level it, and pack brown sugar down hard. A cup of caster "
     "or granulated sugar is about 200g, a cup of icing sugar about 120g, and a level tablespoon "
     "of caster sugar about 12g."),
    ("butter", "margarine", "lard", "shortening",
     "Butter is easiest by weight: a cup is about 225g, a stick about 113g, a level tablespoon "
     "about 14g. If you have a block in its wrapper, the paper is marked in 25g lines - cut on "
     "them and there is nothing to wash up. Soften it first, or it will not cream evenly."),
    ("oats", "porridge oats", "rolled oats",
     "A cup of rolled oats is about 90g, and 50g a person is a portion of porridge. Spoon them in "
     "and level rather than pressing them down, because oats settle and a packed cup can weigh half "
     "again as much."),
    ("cocoa", "cocoa powder",
     "A cup of cocoa powder is about 85g, and it is the one ingredient that really does want "
     "spooning and levelling: cocoa compacts badly and a scooped cup can be a third heavier."),
    ("honey", "syrup", "golden syrup", "treacle", "molasses",
     "Honey and syrup are measured in a jug at eye level, not a cup, because they do not settle "
     "flat - a cup of honey is about 340g. Warm the spoon or the jug in hot water first and it "
     "will run out clean."),
    ("milk", "water", "oil", "buttermilk",
     "Liquids go in a jug on the worktop, read at eye level with the jug standing still - a cup "
     "of milk or water is 240ml and a cup of oil about 225ml."),
)

_MEASURE_AWAY = ("rice", "basmati", "risotto", "pasta", "spaghetti", "noodles", "couscous",
                 "quinoa", "porridge", "soup", "gravy", "stock")


_MEASURING_TAIL = (
    "Spoon it into the cup and level it rather than scooping from the bag, because a cup is a "
    "volume and how much it holds depends on how the ingredient went in. With no scales at all, "
    "use one mug for everything in the recipe - the proportions matter more than the exact weight.")


def _measuring(memory, understood):
    line = _lined(memory, understood)
    if any(re.search(r"\b" + re.escape(w) + r"\b", line) for w in _MEASURE_AWAY):
        return None
    for words in _CUP_OF:
        for word in words[:-1]:
            if re.search(r"\b" + re.escape(word) + r"\b", line):
                return words[-1] + " " + _MEASURING_TAIL
    return _MEASURING_TAIL


_RECIPE_TERM = (
    (("divided", "divide", "half in the sauce", "reserve"),
     r"\bdivid(?:ed|e)\b",
     "'Divided' means the amount is split between stages: half the cheese in the sauce and half on "
     "top, or the butter half in the cake and half in the icing. Weigh or measure the whole lot "
     "out and set the second part aside in a bowl before you start, or it is easy to tip it all "
     "in at once."),
    (("until", "cue", "how do i know when it is done"),
     r"\buntil\b",
     "'Until' is a cue, not a time: until golden, until it comes away from the pan, until a "
     "skewer comes out clean. The recipe gives you the sign to look for because the clock cannot - "
     "ovens and tins differ - so trust your eyes and nose first and the timer second."),
    (("mise en place", "prep", "prepped", "prep ahead"),
     r"\bmise en place\b|\bprep\b",
     "Mise en place is everything weighed, chopped and set out in bowls before you turn the heat "
     "on - the French for 'in place'. It is the whole trick of the last five minutes of a recipe: "
     "most dishes go wrong there because the onion was not chopped yet. Read the ingredients as a "
     "shopping-and-chopping list and do all of it first."),
    (("cup", "cups", "what is a cup"),
     r"\bcups?\b",
     "A cup in a recipe is a volume: 240ml, or 8 US fluid ounces, which is a bit over half a pint. "
     "Most British recipes weigh in grams instead and a British teacup is not a US cup, so a "
     "recipe that says cups is written in American measures - and a cup of flour is about 120g, a "
     "cup of sugar about 200g."),
    (("serves", "makes", "how many does it serve"),
     r"\bserves\b|\bmakes\b|\bhow many\b",
     "'Serves four' usually means four as a main with something alongside, and the number is a "
     "guide rather than a promise - a hungry four will finish a dish written for six. Halve or "
     "double the weights if your table is smaller or bigger, and keep the tin size and the time "
     "in mind when you do."),
)


def _the_recipe_term(memory, understood):
    line = _lined(memory, understood)
    for words in _RECIPE_TERM:
        if re.search(words[1], line):
            return words[2]
    return None



ENTRIES.append(entry(
    "measure-ingredients",
    (("measure flour", "measuring flour", "weigh flour", "measure out flour",
      "measure sugar", "measuring sugar", "measure butter", "weigh butter",
      "measure with cups", "measuring cups", "cup measure", "cups to grams",
      "grams to cups", "measure ingredients", "measuring ingredients",
      "weigh ingredients", "weighing ingredients", "kitchen scales", "digital scales",
      "measure oil", "measure milk", "measure oats", "measure cocoa",
      "measure syrup", "measure honey", "ounces to grams", "oz to grams"),
     ("how do i", "how to", "how much", "what is", "weigh", "weighing", "measure",
      "measuring", "convert", "grams", "cups", "ounces", "oz", "accurate", "properly",
      "right", "best way", "scoop")),
    _measuring,
    avoid=("without scales", "no scales", "no weighing", "mug", "mugs",
           "rice", "basmati", "risotto", "pasta", "spaghetti", "noodles", "couscous", "quinoa",
           "porridge",
           "blood sugar", "diabetes", "diabetic", "insulin", "sugar intake", "how much sugar",
           "added sugar", "cut down on sugar", "sugar free", "portion", "portion size",
           "how many calories", "calories in", "protein", "carbs", "weight loss",
           "lose weight", "diet", "weigh myself", "bathroom scales", "scale says")))

ENTRIES.append(entry(
    "read-a-recipe",
    (("read a recipe", "read the recipe", "follow a recipe", "following a recipe",
      "reading a recipe", "recipe card", "recipe says", "recipe mean", "recipe means",
      "recipe tells", "in a recipe", "on a recipe", "understand a recipe",
      "how do recipes work", "recipe instructions", "mise en place", "prep ahead"),
     ("how do i", "how to", "understand", "read", "reading", "follow", "following",
      "mean", "means", "divided", "until", "prep", "prep time", "serves", "makes",
      "what does", "what is", "whats", "what's", "explain", "trick", "tips", "first")),
    lambda memory, understood: _the_recipe_term(memory, understood) or (
     "Read it twice, all the way through, before you touch anything: what it serves, the prep "
     "time and the cooking time separately, the oven setting, and whether anything has to chill, "
     "soak or rest. Then get every ingredient out and cut up, which is what the French call mise "
     "en place - most recipes go wrong in the last five minutes because the onion was not chopped "
     "yet. Two phrases to know: 'divided' means the amount is split between stages (half the "
     "cheese in the sauce, half on top), and 'until' is a cue rather than a time - until golden, "
     "until it comes away from the pan. Times in a recipe are for that oven and that tin; trust "
     "your eyes and nose first. Check the tin size too, because a wrong-sized tin changes the "
     "depth and with it the time."),
    avoid=("divide", "division", "divided by", "vitamin", "nutrition", "calories",
           "slimming", "restaurant", "takeaway", "meal plan", "meal idea", "what should i cook",
           "dinner idea")))

ENTRIES.append(entry(
    "halve-a-batch-keep-the-tin",
    (("halve a recipe", "halving a recipe", "half the recipe", "half a recipe",
      "double a recipe", "doubling a recipe", "scale a recipe", "scaling a recipe",
      "smaller batch", "bigger batch", "recipe for two", "recipe for one",
      "make half", "make double", "times the recipe"),
     ("how do i", "how to", "can i", "is it", "do i", "times", "oven", "tin", "pan",
      "same", "longer", "shorter", "easier")),
    ("Halve the weights but not quite everything: salt, spices and strong flavours go a little "
     "under half, because they do not scale with the rest, and a raising agent like baking powder "
     "goes to about three quarters of half, or the bake tastes of it. An egg is the awkward one, "
     "so weigh it beaten and use half by weight - about 25g of a large egg. The tin matters more "
     "than the time: half the batter in the same tin is a shallow cake that bakes fast and dries, "
     "so use a smaller tin and check it early rather than turning the oven down. Doubling is the "
     "same in reverse: double the tin's volume, not its width, or bake in two tins."),
    avoid=("half a portion", "half the price", "half price", "half of it", "freeze",
           "leftovers", "keep", "store", "reheat", "calories", "guests", "party")))

entry_bake_with_children = entry(
    "bake-with-children",
    (("bake", "baking", "what can i bake", "what should i bake", "what to bake", "what can we bake",
      "things to bake", "bake with kids", "bake with my kids", "bake with children",
      "bake with the kids", "baking with kids", "baking with children", "easy bake"),
     ("kids", "kid", "children", "child", "toddler", "grandchildren", "family", "my son",
      "my daughter", "with my kids", "with children", "with kids")),
    "Three that work with children, easiest first: flapjack (no oven hands, just stirring and a "
    "flat tin), fairy cakes (they can fill the cases and ice them once cool) and shortbread "
    "(three ingredients, and cutting shapes is the fun part). Give the little ones the measuring "
    "and the stirring and keep the oven and the hob to yourself, and expect it to take twice as "
    "long as it would alone.",
    avoid=("birthday", "went wrong", "sank", "flat", "burnt", "burned", "raw", "soggy", "vegan",
           "gluten", "dairy", "calories"),
    bias=3)
ENTRIES.append(entry_bake_with_children)

entry_bake_nothing_messy = entry(
    "bake-nothing-messy",
    (("mess", "messy", "messing", "mess-free", "no mess", "less mess", "much mess", "too much mess",
      "messiest", "minimal mess", "cleaning up", "clean up", "clear up", "clearing up",
      "washing up", "wash up", "one bowl", "fuss", "faff"),
     ("bake", "baking", "baked", "kids", "kid", "children", "child", "toddler", "grandchildren",
      "with the kids", "with kids", "with children", "cook", "cooking", "recipe",
      "recipes", "ingredients",
      )),
    "The least messy bakes are the ones with one bowl and no icing: a no-bake fridge cake "
    "(melted chocolate and butter, crushed biscuits, into a lined tin, an hour in the fridge), "
    "flapjack (one pan on the hob, one lined tin) and rocky road, which is the same thing with "
    "marshmallows. Shortbread and gingerbread shapes are tidy because the dough is stiff, and "
    "drop scones or pancakes make the mess in one jug. Three things that keep it small: weigh the "
    "ingredients out before anyone is called in, stand the bowl on a tray with the bin beside it, "
    "and line the tin with a sheet that overhangs so the whole bake lifts out.",
    avoid=("floor", "kitchen floor", "paint", "painting", "glitter", "playdough", "play dough",
           "sand", "mud", "garden", "house", "room", "bedroom", "car", "iron", "hoover",
           "washing machine", "laundry", "dishes", "grease", "burnt on", "after baking",
           "mess after", "clean the kitchen", "cleaning the kitchen", "tidy the kitchen",
           "tidy up", "wipe", "clear the kitchen", "clear away", "sink full"),
    bias=2)
ENTRIES.append(entry_bake_nothing_messy)

_POWDER_FOR_SODA = re.compile(
    r"\bbaking powder\b[^.?!]{0,24}?\b(?:instead of|in place of|for|substitute for|replace|"
    r"swap for|swap with)\b[^.?!]{0,16}?\b(?:baking soda|bicarbonate|bicarb|soda)\b", re.I)


def _powder_goes_in_for_soda(understood):
    read = understood if isinstance(understood, dict) else {}
    text = " " + str(read.get("clean") or read.get("text") or "").lower() + " "
    return bool(_POWDER_FOR_SODA.search(text))


entry_powder_for_soda = entry(
    "powder-in-place-of-soda",
    (("baking powder", "powder"),
     ("bicarbonate of soda", "bicarb", "baking soda", "soda"),
     ("instead of", "in place of", "for", "substitute", "replacement", "replace", "swap",
      "swapping", "use", "using", "can i", "could i")),
    "Use about three teaspoons of baking powder for each teaspoon of baking soda, and put the "
    "acid the recipe counted on - buttermilk, yoghurt, lemon juice - in some other way, or the "
    "rise goes flat. That is the easy direction, because baking powder already carries its own "
    "acid. The other way round is not a straight swap: bicarbonate is about four times stronger "
    "and needs an acid to work, so a quarter of a teaspoon with a teaspoon of lemon juice or "
    "vinegar stands in for each teaspoon of powder.",
    avoid=("difference", "different", "same", "vs", "versus", "what is baking powder",
           "what is bicarbonate", "soapy", "tastes of soap", "what does it do", "why do i need"),
    guard=_powder_goes_in_for_soda,
    bias=3)
ENTRIES.append(entry_powder_for_soda)

ENTRIES.append(entry(
    "pizza-base-soggy",
    (("pizza", "pizza base", "pizza bases", "pizza dough", "margherita"),
     ("soggy", "soggy bottom", "wet", "limp", "not crisp", "not crispy", "doughy in the middle",
      "raw in the middle", "went soggy", "goes soggy", "stodgy")),
    "A soggy pizza is three things at once: a cool oven, a thin tray and a wet topping. Heat the "
     "oven and the tray to its top setting for 20 minutes, roll the base thin and put it onto the "
     "hot tray, drain the mozzarella and pat any vegetables dry, and keep the sauce to a thin "
     "layer. Bake it high for 10 to 12 minutes, then finish it under the grill for a minute.",
     avoid=("recipe", "how do i make dough", "how do i make pizza dough", "dough recipe",
            "flour", "yeast", "takeaway", "delivery", "order", "frozen", "calories",
            "healthy", "how long does it", "freeze"),
     bias=2))

ENTRIES.append(entry(
    "raw-flour-taste",
    (("floury", "tastes of flour", "tastes floury", "raw flour", "raw flour taste",
      "chalky", "tastes like flour", "flour taste", "powdery taste"),
     ("sauce", "gravy", "soup", "stew", "curry", "roux", "white sauce", "cheese sauce",
      "casserole", "pie filling", "get rid of", "floury taste", "why does",
      "why is my sauce", "why has my sauce")),
    "A floury taste means the flour is still raw, and the fix is time on the heat, not more "
     "seasoning: simmer it 5 to 10 minutes longer, stirring, so the starch cooks through and "
     "loses the raw edge. A roux wants 2 or 3 minutes of bubbling before any liquid goes in, and "
     "if the sauce is already made, a splash of stock and a slow simmer takes it out. Milk, "
     "butter or cream rounds off what is left.",
     avoid=("bread", "bake", "cake", "batter", "pancake", "flourless", "which flour",
            "what flour", "how much flour", "grams", "cup", "self raising", "plain flour",
            "potato", "potatoes", "spud", "spuds", "old", "gone off", "off", "smell", "smells",
            "smelling", "musty", "rancid", "stale", "keep", "keeps", "last", "lasts")))

ENTRIES.append(entry(
    "metallic-taste-in-food",
    (("metallic", "metal", "tastes of metal", "taste of metal", "tastes metallic"),
     ("rice", "soup", "sauce", "stew", "pasta", "teapot", "tea", "water", "food", "dish",
      "curry", "pan", "kettle", "cook", "cooked", "boiled")),
    "A metal taste in food is usually the pan or the water rather than the food: an unlined "
     "aluminium or cast-iron pan with anything acidic, a metal spoon left in a tomato sauce, or "
     "a furred-up kettle. Cook acidic dishes in stainless steel, enamel or non-stick, move "
     "leftovers out of the pan into glass or plastic, and descale the kettle with a 50/50 mix of "
     "water and white vinegar.",
     avoid=("mouth", "in my mouth", "gum", "gums", "dentist", "medicine", "pregnant",
            "pregnancy", "sinus", "blood", "iron tablet", "coins", "coin", "pipe",
            "my kettle", "the kettle", "kettle tastes", "kettle smells", "from the kettle"),
     bias=2))

BURGER_APART = ("fell apart", "falling apart", "falls apart", "fall apart", "broke up",
                "breaking up", "breaks up", "crumbled", "crumbling", "crumbles", "wont hold",
                "won't hold", "not holding", "holds together", "hold together",
                "went to pieces", "slid apart", "disintegrated")
BURGER_APART_REPLY = (
    "It falls apart for three reasons: the mince is too lean, it was handled too much, or "
    "it was turned before it had a crust. Use mince with some fat in it (20 per cent is right), "
    "break it up with a fork rather than squeezing it, and add an egg and a couple of spoons of "
    "breadcrumbs per 500g if the meat is lean - then shape it loosely, press a shallow dip in the "
    "middle and chill it 20 minutes so it sets. Salt it just before it goes in the pan, cook it "
    "in a hot pan and leave it alone for 3 minutes before the first turn, and it will hold."
    .replace("a egg", "an egg"))


ENTRIES.append(entry(
    "burger-fell-apart",
    (("burger", "patty", "patties", "beefburger",
      "meatball", "meatballs", "meatloaf", "kofta", "koftas", "frikadellen"),
     BURGER_APART),
    BURGER_APART_REPLY,
    avoid=("how do i make", "recipe", "best burger", "veggie", "vegan", "bean burger",
           "tofu", "bun", "buns", "sauce", "cheese slice", "restaurant", "takeaway"),
    bias=1))

MEAL_SITUATIONS = (
    (("football match", "before a match", "before the match", "playing sport", "five a side",
      "swimming gala", "cross country", "sports day", "before training", "game tomorrow",
      "before football", "before rugby", "before a run", "before swimming",
      "rugby match", "netball match", "hockey match", "match tomorrow", "before the game",
      "before his match", "before her match", "match on saturday", "match on sunday",
      "football tomorrow", "swimming gala", "sports day"),
     "Feed them plain carbohydrate about three hours before, not straight before: a bowl of pasta "
     "with a little butter or cheese, a jacket potato, or toast and banana, plus water. Keep the "
     "fat and the fibre light so it is out of the stomach by kick-off, and have a banana or a "
     "flask of squash for after. A cold day wants a warm drink in a flask more than a bigger "
     "meal."),
    (("coeliac", "celiac", "gluten free", "gluten-free", "no gluten", "wheat allergy"),
     "Cook one dish that is gluten-free by nature rather than making a second version: chicken "
     "thighs roasted with potatoes and lemon, a chilli with rice, or a fish pie with a mashed "
     "top. Check the stock cube, the soy sauce and the sausages, because that is where the wheat "
     "hides, use a clean board, and put the bread in its own basket so nothing is cross-"
     "contaminated."),
    (("no oven", "oven is broken", "oven broke", "without an oven", "hob only", "just a hob",
      "oven is out", "no cooker", "microwave only", "moving house"),
     "Everything on the hob: pasta with a sauce made in the same pan, rice with a stir fry, "
     "tinned tomatoes with beans and eggs poached in them, or soup with bread. One pan and one "
     "hob ring is plenty if you add the pasta to the sauce with a ladle of its water, and a "
     "kettle fills in for hot water."),
    (("tight budget", "on a budget", "skint", "no money", "cheap meals", "cheap dinners",
      "money is tight", "cutting back", "cost of living"),
     "Build the week on eggs, lentils, beans, oats, frozen vegetables and chicken thighs: a "
     "lentil bolognese, a bean chilli, egg fried rice, a frittata and a soup covers five dinners "
     "for about the price of one takeaway. Frozen veg and tinned tomatoes cost less and waste "
     "less than fresh, and a whole chicken gives a roast plus a second meal from the carcass."),
    (("pregnant", "cant stand the smell", "can't stand the smell", "smell of cooking",
      "smells make me", "cooking makes me"),
     "Eat cold or barely cooked while the smell turns your stomach: sandwiches, cereal, yoghurt, "
     "fruit, cheese and crackers, or a plate of the dinner you cooked yesterday eaten cold. Cook "
     "once in the morning when the kitchen is fresher, open a window and use the extractor, and "
     "let somebody else do the frying - it is the smell of hot fat that carries."),
    (("chest infection", "no appetite", "lost my appetite", "recovering from flu", "got the flu",
      "been ill", "feeling ill", "off my food", "cant eat", "can't eat"),
     "Small and plain, eaten often: soup, toast, rice pudding, yoghurt, a banana, scrambled egg "
     "on a good day, and a drink beside you all day. Do not worry about a proper dinner while "
     "you are ill - calories and fluid are the job, and the appetite comes back with them."),
    (("my back", "back is bad", "bad back", "cant stand long", "can't stand for long",
      "standing hurts", "on my feet all day", "knee is bad", "cant stand up"),
     "One tray in the oven and one pot on the hob, done in about ten minutes of standing: "
     "chicken thighs or sausages with chopped veg and oil at 200C for 30 minutes, or a chilli "
     "you leave to simmer. Sit at the table to prep with everything within reach, use a stool at "
     "the hob, and cook double so tomorrow needs no standing at all."),
    (("camping", "in a tent", "in the tent", "no fridge", "campervan", "camper van",
      "festival", "no electricity"),
     "One pot, no fridge: pasta with tinned tomatoes, tinned beans and a chopped chorizo or a "
     "tin of tuna, or a curry from a jar with rice. Take food that keeps without cooling - tins, "
     "dried pasta, noodles, porridge oats, bread, hard cheese, apples - and a small gas ring "
     "plus matches in a plastic bag, because a wet night in a tent is when the cooking has to be "
     "simple."),
    (("packed lunch", "packed lunches", "take to work", "take for lunch", "lunch for work",
      "lunchbox", "lunch box", "back at work", "back to work", "school lunch", "dinner lady"),
     "Cook one extra portion of dinner and box it: rice, pasta or a grain with a protein and "
     "something sharp keeps a day in a cool bag and needs no microwave. If there is nothing "
     "left over, a flask of soup with bread, or a tub of couscous made with boiling water from a "
     "kettle and stirred with feta, tomato and herbs, takes five minutes the night before."),
    (("night shift", "night shifts", "eats at 3am", "at 3am", "works nights", "working nights",
      "night worker"),
     "Treat the shift as two meals: a proper one before you go in - rice, pasta or potato with "
     "protein and vegetables - then something light about two thirds of the way through, like a "
     "sandwich, yoghurt, fruit or cereal, rather than a full dinner at 3am. Heavy fat at that "
     "hour sits on the stomach and makes the last hours worse, and a flask of something warm "
     "helps more than coffee at the end of the shift."),
    (("pudding", "dessert", "to bring a cake", "bring a cake", "bring a dessert", "bbq",
      "barbecue", "pot luck", "bring something"),
     "Bring something that travels and needs no fridge: a lemon drizzle traybake, brownies, a "
     "fruit crumble in its dish, or an Eton mess carried as meringue, cream and fruit in three "
     "tubs to layer at the table. Cut it in the tin so it arrives whole, and take the serving "
     "spoon with you."),
    (("tiny kitchen", "no worktop", "small kitchen", "no space", "little space",
      "one hob ring", "no surface"),
     "One tray or one pan a night, prepped on a board balanced on the hob or the table: a "
     "traybake of chicken, potatoes and veg, a one-pot pasta where everything goes in together, "
     "or a stir fry chopped straight into the pan. Clear as you go so the board has a home, and "
     "cook double on the nights you have room, because the second meal needs no worktop at all."),
)
MEAL_ASK = ("what can i cook", "what can i make", "what should i cook", "what should i make",
            "what can we eat", "what shall i cook", "what shall i make", "what should i feed",
            "what can i feed", "what can i bring", "what should i bring", "what do i feed",
            "what do i cook", "what do i make", "what is quick", "whats quick", "what's quick",
            "what can i give", "what should i give", "what to cook", "what to make",
            "meal ideas", "dinner ideas", "what can i do for dinner", "what can i do for tea",
            "what should i take for lunch", "what do i take for lunch", "what to take for lunch",
            "what should i buy", "what do i buy", "what cake can i make", "what can i bake",
            "how do i prep", "prep a meal", "what should i eat", "what can i eat",
            "what should he eat", "what should she eat", "what should they eat")
DIABETES_WORDS = ("diabetic", "diabetics", "diabetes", "type 1", "type 2", "blood sugar",
                  "watching my sugar", "sugar free", "low sugar", "no sugar", "sugar diabetes")
SWEET_ASK = ("cake", "cakes", "bake", "baking", "biscuit", "biscuits", "pudding", "puddings",
             "dessert", "desserts", "something sweet", "sweet treat", "sweet things", "sweets",
             "sweetener", "sweeteners", "sugar substitute")
DIABETIC_BAKE = (
    "Bake something that is low in sugar by nature rather than swapping in sweeteners: an "
    "almond and olive oil cake, a carrot cake made with less sugar and more spice, or berries "
    "with cream and a little dark chocolate. Keep the portion small and have it after a meal "
    "rather than on its own, and put the fruit and the cream on the plate so the cake slice can "
    "be thinner.")
_A_MEAL_IS_NAMED = ("dinner", "dinners", "supper", "lunch", "main meal", "main course")
_ALLOWED_ASKS = ("is it ok", "is it okay", "is it alright", "allowed", "ok for", "okay for",
                 "bad for", "good for", "fine for", "suitable for")
_EATING_VERBS = (" eat ", " have ", " drink ")


def _asks_what_is_allowed(said):
    if any(phrase in said for phrase in _ALLOWED_ASKS):
        return True
    if not any(verb in said for verb in _EATING_VERBS):
        return False
    return any(word in said for word in (" can ", " could ", " should ", " is ", " are "))


def _a_bake_is_the_ask(understood):
    said = " " + str((understood or {}).get("clean") or "").lower() + " "
    if any(" %s " % word in said for word in _A_MEAL_IS_NAMED):
        return False
    return not _asks_what_is_allowed(said)


ENTRIES.append(entry(
    "a-bake-for-a-diabetic", (DIABETES_WORDS, SWEET_ASK), DIABETIC_BAKE, bias=2,
    guard=_a_bake_is_the_ask))

MEAL_SITUATION_WORDS = tuple(word for words, _reply in MEAL_SITUATIONS for word in words)
MEAL_ASK_WORDS = tuple(" ".join(phrase.split()) for phrase in MEAL_ASK)


def _meal_for_the_situation(memory, understood):
    said = str((understood or {}).get("clean") or "").lower()
    if not any(phrase in said for phrase in MEAL_ASK_WORDS):
        return ""
    for words, reply in MEAL_SITUATIONS:
        if any(word in said for word in words):
            return reply
    return ""


ENTRIES.append(entry(
    "meal-for-the-situation",
    (MEAL_SITUATION_WORDS, MEAL_ASK),
    _meal_for_the_situation,
    avoid=("gone off", "is it safe", "still ok", "eat the", "freezer broke", "nothing to eat",
           "should i eat", "how long does", "thaw", "defrost", "allergic", "allergy",
           "intolerant", "poisoning", "recipe for", "how do i make a"),
    bias=3))

_BAKE_NAMED = ("cake", "cakes", "biscuit", "biscuits", "cookie", "cookies", "bun", "buns",
               "muffin", "muffins", "loaf", "loaves", "bread", "sponge", "brownie", "brownies",
               "flapjack", "flapjacks", "traybake", "tray bake", "pie", "crumble", "pudding",
               "frosting", "icing", "buttercream", "recipe", "recipes", "bake", "baking",
               "baked", "batter", "dough", "meringue", "scone", "scones", "shortbread",
               "cheesecake", "swiss roll", "madeira", "victoria sandwich", "tin", "tins",
               "oven", "frosting", "ganache", "dessert")


def _a_bake_is_named(understood):
    said = understood.get("clean") if isinstance(understood, dict) else understood
    words = " " + str(said or "").lower() + " "
    return any((" " + name + " ") in words for name in _BAKE_NAMED)


ENTRIES.append(entry(
    "less-sugar-in-a-bake",
    (("sugar", "caster sugar", "granulated", "icing sugar", "brown sugar", "sweetener",
      "sweet"),
     ("less", "leave", "leaving", "leave out", "leaving out", "left out", "left",
      "take", "taking", "take out", "taking out", "cut", "cutting", "cut down",
      "cut the", "cut it", "reduce", "reducing", "halve", "halving", "half the", "omit",
      "skip", "skipping", "no sugar", "without sugar", "sugar free", "sugar-free",
      "too sweet", "less sweet", "not so sweet", "healthier", "healthy", "diet", "diabetic",
      "diabetes", "calories", "how little", "how much less")),
    "You can cut the sugar in most cakes and traybakes by a third to a half and still get a good "
     "bake, but not all of it: sugar keeps the crumb soft, browns the crust and holds the "
     "structure, so a cake with none bakes pale, dry and crumbly. Leave at least a quarter of "
     "what the recipe asks, add a splash of milk if the batter looks stiff, and eat it within a "
     "couple of days. Bread needs its teaspoon to get the yeast going, and jam and meringue are "
     "set by their sugar, so those cannot be cut.",
    guard=lambda said: _a_bake_is_named(said),
    avoid=("how much sugar", "how many calories", "calories in", "coke", "cola", "fizzy",
           "cereal", "yoghurt", "yogurt", "juice", "squash", "energy drink", "bad for",
           "addictive", "teeth", "blood sugar", "insulin", "type 2", "type 1",
           "double", "doubling", "half the recipe", "for two tins", "two tins",
           "keep", "keeps", "last", "lasts", "gone off", "fridge", "freeze"),
    bias=5))

_TABLE_AHEAD = (
    r"(?=[^.?!]{0,30}?\b(?:coming|come|round|over|due|arriving|invited|tonight|tomorrow|"
    r"this\s+weekend|next\s+week|"
    r"for\s+(?:dinner|lunch|tea|supper|brunch|christmas|a\s+meal|the\s+meal|a\s+party|"
    r"a\s+buffet|a\s+barbecue|a\s+bbq|a\s+birthday|sat|sun|fri|mon|tue|wed|thu)|"
    r"at\s+(?:my|our|a|the)\s+(?:party|do|barbecue|bbq|dinner|table|wedding|reception)|"
    r"on\s+(?:sat|sun|fri|mon|tue|wed|thu)\w*))")

_A_TABLE_OF_PEOPLE = re.compile(
    r"\b(?:having|have\s+got|feeding|catering\s+for|invited|inviting|cooking\s+for|"
    r"making\s+food\s+for|supper\s+for|dinner\s+for|lunch\s+for|tea\s+for|"
    r"table\s+for|seats?\s+for)\s+(?:\d{1,3}|a\s+dozen|twenty|thirty|forty|fifty)\b"
    + _TABLE_AHEAD +
    r"|\b(?:\d{1,3}|a\s+dozen|twenty|thirty|forty|fifty)\s+(?:people|guests|adults|folk|"
    r"of\s+us|grown\s*ups)\b" + _TABLE_AHEAD +
    r"|\b(?:people|guests|adults)\s+(?:coming|round|over|due|arriving)\b" + _TABLE_AHEAD,
    re.I)

_NOT_A_TABLE = (
    "how much", "how many", "per head", "per person", "per guest", "amount", "quantity",
    "kilos", " kg", "grams", "portions", "portion", "how big a", "how large a",
    "poison", "poisoning", "hygiene", "allergy", "allergic", "reaction", "ill", "sick",
    "waste", "bin", "bins", "food bank", "dog food", "cat food", "pet food", "baby food",
    "fast food", "menu", "seating", "seat", "plates", "cutlery", "chairs", "parking",
    "bbq", "barbecue", "barbeque", "buffet", "finger food", "party food", "canape",
    "nibbles", "crisps", "sausage rolls", "sandwiches", "picnic",
    "how many people does", "feeds", "feeding a",
    "plan", "planning", "meal plan", "the week", "cant cook", "can't cook", "cannot cook",
    "never cooked", "dont know how to cook", "don't know how to cook", "beginner",
)


def _a_table_announced(understood):
    read = understood if isinstance(understood, dict) else {}
    text = " " + str(read.get("clean") or read.get("text") or "").lower() + " "
    if not _A_TABLE_OF_PEOPLE.search(text):
        return False
    return not any(phrase in text for phrase in _NOT_A_TABLE)


_A_DIET = (("vegetarian", "meat"), ("vegan", "meat"), ("no meat", "meat"),
           ("nut allergy", "nuts"), ("gluten free", "gluten"), ("dairy free", "dairy"),
           ("lactose", "dairy"))


def the_table_of_people(memory, understood):
    read = understood if isinstance(understood, dict) else {}
    line = str(read.get("clean") or read.get("text") or "")
    text = line
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if isinstance(turns, list):
        text += " " + " ".join(str(turn.get("user") or "") for turn in turns[-4:]
                               if isinstance(turn, dict))
    text = text.lower()
    banned = set()
    for word, food in _A_DIET:
        if word in text:
            banned.add(food)
    return _crowd_meal(banned, _occasion(text), _crowd(text))


entry_a_table_of_people = entry(
    "a-table-of-people",
    (("people", "guests", "adults", "folk", "of us", "feeding", "cooking for", "catering"),
     ("coming", "round", "over", "for", "having", "feeding", "catering", "invited", "due",
      "arriving", "on saturday", "on sunday", "on friday", "on monday", "tonight", "tomorrow")),
    the_table_of_people,
    avoid=("how much", "how many", "per head", "per person", "per guest", "portion",
           "poison", "hygiene", "allergy", "allergic", "food bank", "menu", "seating",
           "chairs", "plates", "cutlery", "feed the dog", "feeding a baby"),
    guard=_a_table_announced,
    bias=1)
ENTRIES.append(entry_a_table_of_people)
