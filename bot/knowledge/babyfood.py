def _the_water_ask(understood):
    text = " " + _text(understood) + " "
    if " water " not in text and not text.endswith(" water "):
        return False
    if any(word in text for word in ("i drink", "should i drink", " a day ", "litre", "liter",
                                     "pint", "eight glasses", "2 litres", "2 liters")):
        return False
    return any(word in text for word in ("give", "giving", "offer", "when can", "how much",
                                         "how often", "sips"))


"""Baby feeding: weaning, first foods, and what a baby can have.

The answers lane owns this domain. This is the food end of parenting: the questions people ask
in the first two years, over and over and usually in a hurry - what do I start with, what can
they eat at this age, can my baby have this thing, how do I bring in an allergen. The facts are
mainstream weaning guidance, kept as data so one fact answers every way of asking for it: "can
my baby have yogurt", "is yoghurt ok for a 7 month old" and "can i give my baby yoghurt" all
reach the same row.

Three tables carry the domain:

- `STAGES` is the age table: what a baby eats and how much of it, from before weaning to a year
  old. One row answers "what can they eat", "how many meals a day" and "how much" alike,
  because all three are the same stage, and the age is read off the line when the answer is
  built rather than keyed three times.
- `FOODS` is the verdict table: one row per food people ask about, each with the answer as it
  would be said - the verdict first, then the age, then the one thing that matters. A food with
  no row is not answered here at all.
- `NOT_A_MENU` and `NOT_A_BABY` are the stand-downs. A baby with a cold, a cot, a car seat or a
  baby shower is not a baby with a menu, and a puppy is not a baby at all. Every row here stands
  down for those, because a food table that answers "my baby has petechiae on her legs" is worse
  than no table.

The other half of the same care is in the keys: a row needs a word of *eating*, not just a baby
and an ask. "what can i give a neighbour who just had a baby" and "how deep should the water be
for a baby bath" have a baby and a question in them and nothing to do with food, and they are
left to the rows that answer them.
"""
import re

from .lookup import entry, not_the_heat_of_an_argument

ANSWERS = ("family-and-parenting", "food-and-drink")

_BABY = ("baby", "baby's", "babys", "babies", "infant", "infants", "little one",
         "little ones", "newborn", "newborns", "breastfed baby", "bottle fed baby",
         "weaning", "weaned")

AGE = ("month old", "months old", "week old", "weeks old", "newborn", "newborns",
       "1 year old", "one year old", "a year old", "eighteen month", "18 month",
       "two year old", "three year old", "four year old", "five year old", "six year old",
       "seven year old", "eight year old", "nine year old", "ten year old",
       "toddler", "toddlers",
       "month", "months", "baby is")

BABY = _BABY + AGE

_UNIT_WITHOUT_FIGURE = ("month", "months")

EATING = ("eat", "eats", "eating", "feed", "feeds", "feeding", "food", "foods", "solids",
          "meals", "meal", "wean", "weaning", "weaned", "diet", "portion", "portions",
          "puree", "purees", "finger food", "finger foods", "breakfast", "lunch", "tea",
          "supper", "snack", "snacks", "drink", "drinks", "milk", "menu")

_THE_REFUSAL_WORDS = ("spits", "spit", "spat")

NOT_A_MENU = (
    "not breathing", "isnt breathing", "isn't breathing", "stopped breathing", "choking",
    "choked", "limp", "floppy", "unresponsive", "wont wake", "won't wake", "blue", "pale",
    "breathing", "breathe", "breathes", "breathless", "wheezing", "wheeze", "grunting",
    "grunt", "sucking in", "under the ribs",
    "fever", "temperature", "rash", "petechiae", "hives", "swollen", "swelling", "vomiting",
    "throwing up", "sick", "diarrhoea", "diarrhea", "constipation", "constipated",
    "blood", "reaction",
    "ill", "unwell", "poorly", "off her food", "off his food", "off their food", "off food",
    "allergic reaction", "anaphylaxis", "a&e", "ambulance", "999", "111", "hospital", "doctor",
    "gp", "health visitor", "refusing feeds", "not feeding", "isnt feeding", "isn't feeding",
    "losing weight", "not putting on weight", "how often", "how many times",
    "wont eat", "won't eat", "not eating", "isnt eating", "isn't eating", "refuses", "refusing",
    "fussy", "picky", "hates", "spits", "throwing food", "throws food", "only eats",
    "cold", "cough", "blocked nose", "ear infection", "colic", "colicky", "windy", "wind",
    "gripe", "reflux", "possetting", "thrush", "eczema", "teething", "teeth", "jab", "jabs",
    "immunisation", "immunisations", "vaccination", "vaccinations", "calpol", "paracetamol",
    "ibuprofen", "dose", "doses", "medicine", "medicines", "tongue tie", "cradle cap",
    "bath", "bathing", "bathwater", "swim", "swimming", "pool", "cot", "crib", "moses",
    "pram", "buggy", "pushchair", "car seat", "carseat", "highchair", "high chair", "bib",
    "sterilise", "steriliser", "formula", "dummy", "nappy", "nappies", "wipes", "nap", "naps",
    "sleep", "sleeping", "crying", "unsettled", "routine", "nursery", "childminder", "creche",
    "pregnant", "pregnancy", "expecting", "labour", "birth", "born", "shower", "christening",
    "gift", "present", "neighbour", "neighbor", "my sister", "my brother", "my cousin",
    "my friend", "my niece", "my nephew", "grandchild", "grandson", "granddaughter",
    "wont drink", "won't drink", "refuses to drink", "temp", "in a bottle", "in the bottle",
    "how much water", "how much juice",
)

_HOW_MUCH_MILK = (
    "how many feeds", "how many feed", "how many bottles", "how many ounces", "how many oz",
    "how many ml", "how many mls", "feeds a day", "bottles a day", "ounces of milk",
    "ml of milk", "how much formula", "how much expressed", "how much should i feed",
    "how much to feed", "how much should i be feeding", "how much should i give my baby",
    "how much milk", "how much breastmilk", "how much breast milk",
)

NOT_A_BABY = ("puppy", "pup", "puppies", "dog", "dogs", "kitten", "kittens", "cat", "cats",
              "vet", "hamster", "guinea", "rabbit", "rabbits", "litter", "crate", "animal",
              "pets", "lamb", "calves", "foal", "chick", "parrot", "fish tank")

WEANING_ELSEWHERE = ("wean", "weans", "weaned", "weaning", "finger food", "finger foods")

A_BODY_LUMP = ("a lump", "has a lump", "had a lump", "found a lump", "under the skin",
               "armpit", "armpits", "neck", "groin", "head", "breast", "testicle", "testicles",
               "scrotum", "gum", "gums", "cheek", "swollen", "swelling", "bump", "bumps",
               "back", "bottom", "tummy", "leg", "thigh", "shoulder", "chest", "forehead",
               "under the arm", "in the nappy area", "skin")

NOT_AN_AGE = ("contract", "contracts", "membership", "memberships", "subscription",
              "subscriptions", "tenancy", "lease", "warranty", "insurance", "loan", "loans",
              "instalment", "instalments", "repayments", "gym", "phone contract",
              "mobile contract", "broadband", "cancellation", "notice period",
              "without an r", "with an r", "time of year")

SPICE_NAMES = ("cinnamon", "cumin", "turmeric", "paprika", "nutmeg", "coriander", "cardamom",
               "saffron", "curry powder", "chilli powder", "chili powder", "black pepper",
               "white pepper", "mixed spice", "allspice", "garam masala", "spices", "spice",
               "herbs", "herb", "mild curry")

NOT_ABOUT_WATER = ("dehydrate", "dehydrates", "dehydrated", "dehydration", "dehydrating",
                   "hydration", "diuretic", "electrolytes")

JOB_WORDS = ("job", "jobs", "my job", "new job", "job offer", "leave a job", "leaving a job",
             "left a job", "quit my job", "quitting my job", "boss", "employer", "employee",
             "career", "resign", "resigning", "resignation", "hand in my notice",
             "handing in my notice", "notice period", "interview", "salary", "my salary")

STAND_DOWN = (NOT_A_MENU + _HOW_MUCH_MILK + NOT_A_BABY + WEANING_ELSEWHERE + NOT_AN_AGE
              + SPICE_NAMES + NOT_ABOUT_WATER + JOB_WORDS)

BOOK_WORDS = ("book", "books", "novel", "picture book", "story", "stories", "read to",
              "reading to", "read aloud")

STAGES = (
    {"from": 0, "until": 5,
     "reply": "Milk is all a baby needs before about six months, and food before four months "
              "is not recommended at all. If they seem hungrier, more milk is the answer - ask "
              "your health visitor before starting anything early."},
    {"from": 6, "until": 8,
     "reply": "At this age milk is still the main food, so treat eating as practice: two or "
              "three small goes a day of soft food they can hold - cooked carrot or broccoli, "
              "toast fingers, banana, plain yoghurt, mashed lentils. One new food at a time, a "
              "few days apart, so a reaction is easy to spot."},
    {"from": 9, "until": 11,
     "reply": "By now it is three meals a day plus milk, and what they eat starts to matter: "
              "chopped versions of your own meal, soft meat or fish with the bones out, pasta, "
              "beans and lentils, fruit, full-fat dairy. No added salt or sugar, and no honey "
              "before the first birthday."},
    {"from": 12, "until": None,
     "reply": "From one they can eat what the rest of the family eats: three meals and two "
              "snacks, whole cows milk as a drink at about 350 to 400ml a day, and no added "
              "salt. Honey is fine from now on."},
)

_NUMBER_WORDS = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
                 "ten", "eleven", "twelve")

FOODS = (
    {"names": ("yogurt", "yoghurt", "yoghurts", "yogurts", "fromage frais", "greek yogurt",
               "greek yoghurt", "kefir", "skyr"),
     "reply": "Yes, plain full-fat yoghurt is fine from six months. Buy natural or Greek rather "
              "than the children's fruit pots, which are mostly sugar - stir in mashed fruit "
              "instead - and give it with a meal rather than as a drink."},
    {"names": ("cheese", "cheddar", "cheeses", "parmesan", "mozzarella", "cream cheese",
               "brie", "camembert", "blue cheese", "stilton", "gorgonzola", "roquefort",
               "mould ripened", "mold ripened", "soft cheese", "goats cheese", "feta"),
     "reply": "Yes, from six months, in small amounts, because cheese is salty: about 25g a day "
              "is plenty for a little one. Stick to pasteurised cheese - brie, camembert and "
              "blue cheese are the ones to leave raw, and they are fine once cooked until "
              "steaming hot."},
    {"names": ("egg", "eggs", "scrambled egg", "boiled egg", "omelette"),
     "reply": "Yes, well cooked, from six months: scrambled egg, a hard-boiled egg mashed with "
              "a fork, or omelette cut into fingers. An egg with the red lion stamp can be given "
              "runny because those hens are vaccinated; without the stamp, cook it until white "
              "and yolk are both solid."},
    {"names": ("strawberry", "strawberries", "raspberry", "raspberries", "blueberry",
               "blueberries", "berries", "blackberries"),
     "reply": "Yes, from six months - cut them in half or quarters, because a round berry is a "
              "choking shape. Berries are acidic, so they can bring on a red nappy rash, and "
              "that is not an allergy; a rash round the mouth that fades on its own is usually "
              "the same thing."},
    {"names": ("peanut butter", "peanut", "peanuts", "nut butter", "almond butter",
               "nut", "nuts", "almonds", "cashews", "almond"),
     "reply": "Yes, and early is better than late: from six months, a thin smear of smooth "
              "peanut butter on toast or stirred into porridge. Never a spoonful on its own and "
              "never a whole nut - those are choking shapes, so use ground or butter only. "
              "Offer it on a day they are well, in the morning, then keep it in their week."},
    {"names": ("raisins", "raisin", "sultanas", "sultana", "dried fruit", "dried apricots",
               "prunes", "dates", "currants", "cranberries", "dried cranberries"),
     "reply": "Yes, from six months, but chop them: a whole raisin is the shape that blocks a "
              "small throat and it is sticky enough to sit on the teeth, so cut each one in "
              "half, give them with a meal rather than as a snack on their own, and keep them "
              "to a small handful a day. Dried fruit counts as one of the five a day, so it is "
              "not a substitute for fresh fruit - and never dried fruit with added sugar or "
              "yoghurt coating."},
    {"names": ("tea", "teas", "green tea", "herbal tea", "camomile tea", "chamomile tea",
               "peppermint tea", "fruit tea", "coffee", "cola", "coke", "energy drink",
               "energy drinks", "caffeine", "fizzy drink", "fizzy drinks", "diet coke"),
     "extra": ("child", "children", "kid", "kids", "toddler", "toddlers", "teen", "teens",
               "teenager", "teenagers", "school", "year old", "12", "under 12", "10", "14",
               "dehydrat", "dehydrate", "dehydrates", "dehydrated", "dehydrating",
               "dehydration", "hydrate", "hydrated", "hydration"),
     "bias": 3,
     "reply": "No, not as a drink: tea and coffee both carry caffeine a small body does not "
              "need, and the tannins in tea stop iron being absorbed, which matters most in the "
              "first two years. Cola, energy drinks and fizzy drinks are the same answer with "
              "sugar on top, and herbal teas are no better for a baby. Milk and water are the "
              "drinks: breast milk or formula before one, whole cows milk from one, and water "
              "in an open cup with meals from six months."},
    {"names": ("liver", "lamb's liver", "chicken liver", "kidney", "pate", "liver pate", "paté"),
     "reply": "Liver is fine from six months, but once a week at most: it is packed with vitamin A "
              "and iron, and too much vitamin A builds up. Cook it through, mash or blend it into "
              "something they already eat, and count liver, liver pate and cod liver oil as the "
              "same thing in that week. Pate itself is salty, so leave that until after the first "
              "birthday and then keep it to a thin scrape."},
    {"names": ("crisps", "crisp", "chips", "wotsits", "quavers", "cheese puffs"),
     "reply": "No, not before one, and rarely after: crisps are salty and they are a choking "
              "shape, and the same goes for chips with salt on. A handful of soft veg sticks, "
              "toast fingers or a bit of cheese is the same idea without the salt."},
    {"names": ("wheat", "soya", "soy", "sesame", "gluten"),
     "reply": "Yes, from six months, and early is the point: wheat, soya and sesame are three of "
              "the allergens to give in the first year, one at a time, on a day they are well and "
              "in the morning. Bread, pasta, cereal, tofu and tahini all count, and once a food "
              "is in, keep giving it a couple of times a week rather than stopping."},
    {"names": ("cows milk", "cow's milk", "whole milk", "full fat milk", "semi skimmed milk"),
     "reply": "Not as a drink before twelve months: it has too little iron and too much salt "
              "and protein for a baby. You can cook with it, or put a splash on cereal, from six "
              "months. From one, give whole milk, about 350 to 400ml a day."},
    {"names": ("water", "juice", "fruit juice", "squash", "cordial", "orange juice",
               "apple juice", "smoothie", "smoothies", "milkshake", "milkshakes"),
     "own_ask": _the_water_ask,
     "extra": ("toddler", "toddlers", "litre", "litres", "2 year", "3 year", "4 year",
               "5 year", "child", "children", "kids", "i drink", "should i drink",
               "how much should i"),

    "reply": "Not before six months - milk is all they need, and extra water can upset their "
              "salts. From six months, water is the drink to offer in an open cup with meals, and "
              "juice or squash is not needed at any age: if you give it, wait until twelve months, "
              "dilute it, and keep it to a meal in a cup rather than a bottle."},
    {"names": ("salt", "salty", "stock cube", "stock cubes", "gravy", "bacon", "ham",
               "sausages", "sausage", "salted", "marmite", "yeast extract", "bovril",
               "soy sauce", "baked beans", "beans on toast", "tomato ketchup", "ketchup",
               "brown sauce", "mayonnaise", "mayo", "soup", "soups", "gravy granules",
               "stock", "salted butter"),
     "reply": "No salt at all in their food before one, and very little after: a baby's kidneys "
              "cannot cope with it. That rules out stock cubes, gravy granules, bacon, ham, "
              "sausages and most sauces - cook their portion separately and season yours."},
    {"names": ("sugar", "sweets", "chocolate", "biscuits", "biscuit", "cake", "cakes",
               "jelly", "jam", "marmalade", "rice pudding", "custard"),
     "reply": "There is no need for sugar at all before two, and it is worth keeping it that "
              "way while you can, because it is what makes them prefer sweet food later. Fruit "
              "is the sweet thing to give, and cheese or toast makes a better snack than a "
              "biscuit."},
    {"names": ("grapes", "grape", "cherry tomatoes", "cherries", "olives", "hot dog", "hot dogs"),
     "reply": "Yes, but cut them: grapes, cherry tomatoes and olives go lengthways into "
              "quarters and sausages lengthways into strips, because the round shape is what "
              "blocks a small throat. Whole grapes are the food toddlers choke on most, and "
              "popcorn is not one to give before about four."},
    {"names": ("popcorn", "pop corn", "puffed corn", "corn snacks"),
     "reply": "No, not before about four: popcorn is light, hard and the exact shape that lodges "
              "in a small airway, and it is the food toddlers choke on most after grapes. Puffed "
              "corn snacks are the same shape and salty as well, so leave those too, and keep "
              "crisps for an occasional treat after one, sitting down."},
    {"names": ("rice cake", "rice cakes", "corn cake", "corn cakes", "oat cake", "oat cakes",
               "crackers", "cracker", "breadsticks", "bread sticks", "rusks", "rusk"),
     "reply": "Yes, from six months, and they are good for the pincer grip - but read the packet "
              "first, because they are often the saltiest thing in the baby aisle. Unsalted rice "
              "cakes, plain oatcakes and no-salt breadsticks are the ones to pick; a rusk is "
              "mostly sugar, so treat it as a biscuit rather than a food."},
    {"names": ("cucumber", "cucumbers", "tomato", "tomatoes",
               "bell pepper", "bell peppers", "red pepper", "green pepper", "sweet pepper",
               "lettuce", "celery", "radish", "radishes",
               "spring onion", "spring onions", "beetroot", "raw carrot", "carrot sticks"),
     "reply": "Yes, from six months, raw or cooked: cucumber and tomato cut into finger-length "
              "batons or quarters are two of the easiest first finger foods, because a baby can "
              "hold them and gum them. Cherry tomatoes and olives go lengthways into quarters, "
              "and celery strings are worth peeling off before you hand it over."},
    {"names": ("tofu", "bean curd", "edamame", "soya bean", "soy bean", "tempeh"),
     "reply": "Yes, from six months, cooked through: tofu cut into strips is soft enough to gum, "
              "and it takes on whatever it is cooked in. It is soya, so introduce it the way you "
              "would peanut - a little on its own the first time, then watch for two hours - and "
              "keep it plain rather than in a salty marinade."},
    {"names": ("quorn", "mycoprotein", "quorn mince", "quorn pieces", "meat free mince",
               "veggie mince", "vegetarian mince"),
     "reply": "Yes, from six months, cooked through and chopped small: Quorn is mycoprotein, a "
              "fungal protein rather than soya, and the plain mince and pieces are low in salt "
              "and fine for a baby. It is a protein swap rather than a whole food, so give it "
              "with something iron-rich - lentils, beans or a little meat - and read the packet "
              "on the breaded and ready-made versions, which are salty."},
    {"names": ("sushi", "sashimi", "raw fish", "raw prawns", "smoked salmon", "smoked mackerel",
               "gravadlax", "gravalax", "cured fish", "oysters"),
     "reply": "Sushi is fine once the fish in it is cooked: a cooked prawn or salmon roll, or a "
              "vegetable one, is a good finger food from six months. Raw fish and raw shellfish "
              "wait until they are five, because of the parasites and the bones. Smoked salmon "
              "is cured rather than cooked and it is salty, so a flake now and then is the most "
              "of it.",
     "bias": 2},
    {"names": ("fish", "salmon", "tuna", "cod", "prawns", "shellfish", "prawn", "mussels"),
     "reply": "Yes, well cooked and with every bone out - flake it and check between your "
              "fingers first. Oily fish like salmon once or twice a week is worth having. Leave "
              "out shark, swordfish and marlin, and keep tuna to about one small tin a week."},
    {"names": ("toast", "bread", "crumpet", "pitta", "cracker", "crackers", "chapati",
               "chapatis", "naan", "roti", "wrap", "wraps", "bagel", "bagels", "scone",
               "scones", "teacake"),
     "reply": "Yes, from six months - toast fingers are one of the easiest first foods because "
              "a baby can hold them. White, wholemeal or a mix is fine; bread has salt in it "
              "already, which is a reason not to add more, not a reason to wait.",
     "pronoun": True,
     "extra": ("a toast", "raise a glass", "raise the glass", "speech", "speeches",
               "wedding", "best man", "eulogy", "few words", "say a few words")},
    {"names": ("banana", "bananas"),
     "reply": "Yes, from six months, and it is one of the easiest first foods: mash it or cut it "
              "into finger-length pieces a baby can hold. It is sweet and soft, so it goes down "
              "on a day when nothing else does."},
    {"names": ("avocado", "avocados", "guacamole", "avocado pear"),
     "reply": "Yes, from six months: ripe avocado mashed on toast fingers, or in a wedge they can "
              "hold with the skin as a handle. The fat in it is the kind a growing baby needs, "
              "and its blandness sits well next to a stronger taste."},
    {"names": ("broccoli", "cauliflower", "courgette", "carrot", "carrots", "sweet potato",
               "butternut squash", "parsnip", "peas", "green beans", "spinach", "kale",
               "leeks", "swede", "turnip", "asparagus", "plantain", "mushroom", "mushrooms",
               "mange tout", "sugar snap peas", "runner beans", "cabbage", "brussels sprouts",
               "cauliflower cheese"),
     "reply": "Yes, from six months, cooked soft enough to squash between your fingers - a whole "
              "floret or a stick of carrot is a handle a baby can hold and gum. Keep offering "
              "the ones they refuse: it can take ten tries before a vegetable is eaten."},
    {"names": ("potato", "potatoes", "mash"),
     "reply": "Yes, from six months: mashed potato with a little of their usual milk or unsalted "
              "butter, or soft roast potato in strips. No salt in the water or on top, and skip "
              "chips and crisps, which are salty and hard to manage."},
    {"names": ("pasta", "fusilli", "penne", "macaroni", "spaghetti", "noodles"),
     "reply": "Yes, from about six months once they can pick things up: shapes like fusilli or "
              "penne are easier to hold than spaghetti, and cook them a minute past the packet "
              "so they are soft. Cut long pasta, and keep the sauce low in salt."},
    {"names": ("rice", "couscous", "quinoa", "bulgur"),
     "reply": "Yes, from six months, cooked soft - as a mash, or pressed into a sticky ball they "
              "can pick up. No salt in the water. Cooked rice is the one to be careful with: cool "
              "it fast, fridge it within the hour, and reheat it once, hot all through."},
    {"names": ("hummus", "houmous", "chickpeas"),
     "reply": "Yes, from six months: spread it thin on toast fingers or let them dip a finger of "
              "pitta in it, and it counts as a portion of protein. Shop hummus can be salty, so "
              "a plain one or your own is better."},
    {"names": ("lentils", "dhal", "daal", "beans", "kidney beans", "chick pea", "pulses"),
     "reply": "Yes, from six months: red lentils cook down into a thick dhal they can eat from a "
              "spoon or with bread, and mashed beans go into a sauce the same way. Pulses are a "
              "good source of iron, and a squeeze of lemon or some tomato helps the iron go in."},
    {"names": ("mango", "melon", "watermelon", "peach", "pear", "plum", "nectarine",
               "blueberries", "raspberries", "kiwi", "kiwis", "pineapple", "coconut",
               "grated coconut", "strawberry", "strawberries", "blackberries", "cherries",
               "apricot", "apricots", "papaya", "fig", "figs", "orange", "satsuma",
               "mandarin", "clementine"),
     "reply": "Yes, from six months: soft ripe fruit in strips or wedges they can hold, and a "
              "wedge with the skin on makes a handle to gnaw. Round fruit is the one to cut - "
              "berries in half, grapes lengthways - and stay with them while they eat it."},
    {"names": ("chicken", "beef", "lamb", "pork", "mince", "meat"),
     "reply": "Yes, from six months: soft cooked meat in strips they can hold, or minced into a "
              "sauce, and it is the best source of the iron a baby uses up at about six months. "
              "A strip of well-cooked chicken or a lamb chop bone is a good thing to gnaw, with "
              "the gristle and small bones taken out."},
    {"names": ("porridge", "oats", "cereal", "baby rice"),
     "extra": ("bottle", "bottles", "in a bottle", "in the bottle", "bottle feed"),
     "reply": "Yes, from six months, and ordinary porridge oats made with their usual milk are "
              "as good as any baby cereal, with no added sugar or salt. Baby rice is almost all "
              "starch, so it fills them up without feeding them much."},
)

_FIRST_FOODS = (
    "Start with soft food they can hold themselves rather than something on a spoon: cooked "
    "carrot or broccoli, toast fingers, ripe pear, banana, avocado, or a spoon of plain "
    "yoghurt. One food at a time, a few days apart, so a reaction is easy to spot, and milk "
    "first so they are not too hungry to try. How much is a few spoonfuls or a few sticks at "
    "the start, half a fist by nine months and about a fist at a year. Around six months is the "
    "age, unless a health visitor has said otherwise.")

_WHAT_TO_FEED = ("what can", "what should", "what do", "what to", "what shall", "what could",
                 "what will", "what food", "what foods", "what food do i", "how much", "how many",
                 "how often", "when can", "when should", "when do", "is it ok to", "can i give",
                 "can i feed", "can i start", "can they have", "can she have", "can he have",
                 "where do i start")


def _text(understood):
    words = understood.get("words") if isinstance(understood, dict) else None
    if isinstance(words, (list, tuple)) and words:
        return " ".join(str(word) for word in words).lower()
    return str((understood or {}).get("clean") or "").lower()


_AGE_FIGURE = re.compile(r"\b(\d{1,2})\s*-?\s*(month|months|mth|mths|year|years|yr|yrs)\b")


def _age_in_the_chat(memory, understood):
    words = {str(word).lower() for word in (understood.get("words") or ())}
    if not words & set(_THE_CHILD):
        return None
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return None
    said_now = str(understood.get("clean") or "").strip().lower()
    for turn in reversed(turns):
        if not isinstance(turn, dict):
            continue
        text = str(turn.get("user") or "").strip().lower()
        if not text or text == said_now:
            continue
        numbers = [{"value": int(match.group(1)), "unit": match.group(2)}
                   for match in _AGE_FIGURE.finditer(text)]
        age = _age_in_months({"clean": text, "words": text.split(), "numbers": numbers})
        if age is not None:
            return age
    return None


def _age_in_months(understood):
    for number in understood.get("numbers") or ():
        if not isinstance(number, dict):
            continue
        value = number.get("value")
        if not isinstance(value, int) or value < 0:
            continue
        unit = str(number.get("unit") or "").lower()
        if unit.startswith("month"):
            return value
        if unit.startswith("year"):
            return 12 * value
        if unit.startswith("week"):
            return 0
    said = _text(understood)
    if re.search(r"\bbaby is (one|1)\b", said) or re.search(r"\b(one|1) year old\b", said):
        return 12
    for words in _NUMBER_WORDS:
        if re.search(r"\b%s\s+months?\b" % words, said):
            return _NUMBER_WORDS_AT[words]
        if re.search(r"\b%s\s+years?[\s-]*old\b" % words, said):
            return 12 * _NUMBER_WORDS_AT[words]
    if any(re.search(r"\b%s\b" % word, said) for word in _OLDER_CHILD_WORD):
        bare = re.search(r"\b(?:%s)\s+(?:is\s+|are\s+|aged\s+|at\s+|of\s+)?(\d{1,2})\b"
                         r"(?!\s*(?:month|months|mth|mths|week|weeks|wk|wks|day|days|stone|"
                         r"kilos|kilo|kg|lbs|pounds)\b)"
                         % "|".join(_OLDER_CHILD_WORD), said)
        if bare and 2 <= int(bare.group(1)) <= 19:
            return 12 * int(bare.group(1))
    if re.search(r"\b(toddler|toddlers)\b", said):
        return 12
    if re.search(r"\b(newborn|newborns)\b", said):
        return 0
    return None


_NUMBER_WORDS_AT = {word: index + 1 for index, word in enumerate(_NUMBER_WORDS)}


def _stage(understood):
    age = _age_in_months(understood)
    if age is None:
        return None
    for stage in STAGES:
        until = stage["until"]
        if age >= stage["from"] and (until is None or age <= until):
            return stage["reply"]
    return None


_MILK_WORDS = ("milk", "breastmilk", "breast milk", "expressed milk", "expressed")
_MILK_HOW_MUCH = ("how much", "how many", "how often", "much milk", "much breastmilk",
                  "many ounces", "how many oz",
                  "what milk", "which milk", "what kind of milk", "what type of milk",
                  "best milk", "right milk")
_NOT_A_BABY_MILK = ("toddler", "toddlers", "2 year", "two year", "3 year", "three year",
                    "4 year", "four year", "5 year", "five year", "child", "children", "kids",
                    "should i drink", "i drink", "i have", "can i have", "adult", "pump",
                    "pumping", "recipe", "latte", "cappuccino", "protein", "calcium")

_A_DRINK = ("drink", "drinks", "drinking", "have", "has", "need", "needs", "take", "takes")

_A_COUNT = ("how many ounces", "how many oz", "how many ml", "how many mls", "ounces", "oz",
            "ml", "mls")

_THE_CHILD = ("he", "she", "him", "her", "they", "them")

_MILK_UNDER_SIX = (
    "Milk is the whole diet before six months, so there is no set amount: eight to twelve "
    "feeds in 24 hours, on demand, day and night. Six or more wet nappies a day and a baby who "
    "settles after a feed mean they are getting enough, and the scales settle it better than the "
    "ounces. Nothing else goes in the bottle - no cereal, no water unless it is hot.")
_MILK_SIX_TO_TWELVE = (
    "About 500 to 600ml (17 to 20oz) of breast milk or formula a day from six to twelve months, "
    "in four or five feeds, and food goes alongside it rather than instead of it: milk is still "
    "the main drink until the first birthday, and the wet nappies still say whether it is enough.")
_MILK_OVER_ONE = (
    "About 350 to 400ml (12oz) a day of whole cows milk from one, in a cup rather than a bottle: "
    "that much covers the calcium without filling them up before meals, and more than about "
    "500ml crowds out the iron in food.")


_WATER_UNDER_SIX = (
    "Under six months, none: milk is all they need and extra water can upset the salts in a "
    "small body. From six months, offer a little water in an open cup with meals - a few sips is "
    "enough, and they will take what they need rather than a set amount. From one, water with "
    "every meal and between meals as they ask for it, and that is when a cup measuring roughly a "
    "litre a day starts to make sense.")
_WATER_OVER_ONE = (
    "Water with every meal and between meals whenever they ask for it: a cup measuring roughly a "
    "litre a day is the toddler figure, and the milk they drink counts towards it. Leave the cup "
    "where they can reach it and refill it without a fuss. Under six months it was none, because "
    "extra water upsets the salts in a small body, so do not go back to that unless a doctor says "
    "so.")
_WATER_NO_AGE = (
    "Under six months, none: milk is all they need and extra water can upset the salts in a "
    "small body. From six months, offer a little water in an open cup with meals - a few sips is "
    "enough, and they will take what they need rather than a set amount. From one, water with "
    "every meal and between meals as they ask for it, and that is when a cup measuring roughly a "
    "litre a day starts to make sense.")
_WATER_JUICE = (
    " Juice and squash are not needed at any age: if you give juice at all, wait until twelve "
    "months, dilute it, and keep it to a meal in a cup.")


def _how_much_water(memory, understood):
    age = _age_in_months(understood)
    if age is None:
        age = _age_in_the_chat(memory, understood)
    if age is not None and age < 6:
        return _WATER_UNDER_SIX + _WATER_JUICE
    if age is not None and age >= 12:
        return _WATER_OVER_ONE + _WATER_JUICE
    return _WATER_NO_AGE + _WATER_JUICE


def _milk_volume(memory, understood):
    age = _age_in_months(understood)
    if age is None:
        age = _age_in_the_chat(memory, understood)
    if age is not None and age < 6:
        return _MILK_UNDER_SIX
    if age is not None and age < 12:
        return _MILK_SIX_TO_TWELVE
    if age is not None:
        return _MILK_OVER_ONE
    return _MILK_UNDER_SIX + " " + _MILK_SIX_TO_TWELVE + " " + _MILK_OVER_ONE


_DRINK_UNDER_SIX = (
    "Milk is the only drink before six months - breast milk or formula, on demand, and nothing "
    "else in the bottle, not even water.")
_DRINK_SIX_TO_TWELVE = (
    "Milk is still the main drink at this age: breast milk or formula on demand, and water in an "
    "open cup with meals from six months. A free-flow cup or a straw cup is better than a bottle "
    "from six months, since the sucking is what makes the fuss. Juice and squash are not needed "
    "at any age; if you give juice at all, wait until twelve months, dilute it, and keep it to a "
    "meal.")
_DRINK_OVER_ONE = (
    "About a litre a day for a one-year-old, and the milk they drink counts towards it: whole "
    "cows milk at roughly 350 to 400ml of that, in a cup rather than a bottle, and water with "
    "every meal and whenever they ask. Leave the cup where they can reach it and refill it "
    "without a fuss. Juice and squash are not needed; if you give juice, dilute it and keep it "
    "to a meal in a cup.")


def _what_a_baby_drinks(memory, understood):
    age = _age_in_months(understood)
    if age is None:
        age = _age_in_the_chat(memory, understood)
    if age is not None and age < 6:
        return _DRINK_UNDER_SIX
    if age is not None and age < 12:
        return _DRINK_SIX_TO_TWELVE
    if age is not None:
        return _DRINK_OVER_ONE
    return _DRINK_UNDER_SIX + " " + _DRINK_SIX_TO_TWELVE + " " + _DRINK_OVER_ONE


_SNACK = ("snack", "snacks", "snacking", "a snack", "between meals", "in between meals",
          "little and often")
_SNACK_CHILD = _BABY + AGE + ("child", "children", "kid", "kids", "1 year old", "2 year old",
                              "3 year old", "4 year old", "school age")
_NOT_A_SNACK = ("party", "parties", "buffet", "guests", "film", "films", "movie", "match",
                "half time", "picnic", "me", "myself", "adult", "adults", "for the adults",
                "recipe", "make ahead", "christmas", "birthday", "wedding", "work")

_SNACK_UNDER_SIX = (
    "No snacks before six months: milk is the whole of it, and a baby that young does not need "
    "anything between feeds, only more milk.")
_SNACK_SIX_TO_TWELVE = (
    "From six months, two or three small goes a day at set times rather than all day long, and "
    "the best snacks are the ones they can hold: toast fingers, soft fruit, cooked veg sticks, "
    "plain yoghurt, a little cheese, oatcakes. Keep away from the choking shapes - whole grapes, "
    "whole nuts, popcorn - and sit them down while they eat.")
_SNACK_OVER_ONE = (
    "Two snacks a day between meals is right from one: fruit, plain yoghurt, toast, oatcakes, "
    "cheese, veg sticks. Keep them at set times rather than in the hand all afternoon, because a "
    "child who grazes does not sit down for the meal, and keep the choking shapes - whole grapes, "
    "whole nuts, popcorn - for later.")


def _snacks(memory, understood):
    age = _age_in_months(understood)
    if age is None:
        age = _age_in_the_chat(memory, understood)
    if age is not None and age < 6:
        return _SNACK_UNDER_SIX
    if age is not None and age < 12:
        return _SNACK_SIX_TO_TWELVE
    if age is not None:
        return _SNACK_OVER_ONE
    return _SNACK_SIX_TO_TWELVE + " " + _SNACK_OVER_ONE


def _says_what_they_eat(understood):
    said = _text(understood)
    padded = " %s " % said
    return any(" %s " % word in padded for word in EATING)


_PLANT_MILK_BABY = (
    "Not as their main drink, no. A baby under a year needs breast milk or first infant formula, "
    "and a plant milk does not have the protein, fat, calcium or vitamins to stand in for it. In "
    "cereal, porridge or cooking from six months it is fine - choose one with no sugar and with "
    "calcium and vitamin D added."
)
_PLANT_MILK_RICE = (
    "Rice milk is the one to leave out completely before five years: it has arsenic in it, which "
    "a small body clears slowly, and a child drinking it daily can take in too much. Oat, soya or "
    "coconut milk, unsweetened and fortified, are the better swaps over one."
)
_PLANT_MILK_CHILD = (
    "Yes, as a drink now - unsweetened and with calcium and vitamin D added, and it does not "
    "replace their food. Soya is the only one with protein close to cows milk, so it is the usual "
    "swap; rice milk still waits until five."
)


def _plant_milk(memory, understood):
    age = _age_in_months(understood)
    if age is None:
        age = _age_in_the_chat(memory, understood)
    said = _text(understood)
    rice = "rice" in said
    if age is None:
        return _PLANT_MILK_BABY + " " + _PLANT_MILK_RICE
    if age < 12:
        return _PLANT_MILK_BABY + (" " + _PLANT_MILK_RICE if rice else "")
    if rice:
        return _PLANT_MILK_RICE
    return _PLANT_MILK_CHILD


def _by_age(memory, understood):
    if not _says_what_they_eat(understood):
        return None
    return _stage(understood) or _FIRST_FOODS


_VERDICT_ASK = ("have", "has", "give", "gives", "giving", "eat", "eats", "eating", "feed",
                "drink", "drinks", "try", "ok", "safe", "allowed", "much", "many", "any",
                "can i give", "can i feed", "can i put", "can i try", "am i allowed",
                "is it ok to", "should i give", "ok to give", "safe to give",
                "when can", "when should")


_A_CHILD = ("son", "sons", "daughter", "daughters", "child", "children", "kid", "kids",
            "boy", "boys", "girl", "girls", "little boy", "little girl", "grandchild",
            "grandchildren", "grandson", "granddaughter", "stepson", "stepdaughter")


_NAMES_A_BABY = tuple(word for word in BABY if word not in _UNIT_WITHOUT_FIGURE) + _A_CHILD

_FOR_A_GROWN_UP = ("adult", "adults", "grown up", "grown ups", "grownup", "grownups",
                   "for a grown up", "for adults", "is it ok for me", "safe for me")

_NOT_A_BABY_NAME = ("baby rice", "baby porridge", "baby cereal", "baby food", "baby foods",
                    "baby jar", "baby jars", "baby pouch", "baby pouches", "baby porridge pot")


def _names_no_baby(text):
    low = " %s " % text
    for name in _NOT_A_BABY_NAME:
        low = low.replace(" %s " % name, " thing ")
    return low


_A_RATE_IN_MONTHS = re.compile(r"\b(?:a|per|each|every|the)\s+month\b", re.I)


def _a_baby_is_named(understood):
    low = " " + _text(understood) + " "
    if _AGE_FIGURE.search(low):
        return True
    hit = [word for word in _NAMES_A_BABY if (" " + word + " ") in low]
    if hit and all(word in ("month", "months") for word in hit) and _A_RATE_IN_MONTHS.search(low):
        return False
    return bool(hit)


_A_BABY_TILL = 36


_A_CHILD_PRONOUN = ("he", "she", "him", "her", "his", "hers")

_A_ORGAN = r"(?:liver|kidneys?|hearts?)"
_A_CONDITION = re.compile(
    r"\b(" + _A_ORGAN + r")\b(?:\W+\w+){0,2}?\W+"
    r"(?:problems?|conditions?|disease|failure|infections?|damage|stones?|transplants?|"
    r"surgery|operation|disorder|dialysis|reflux)\b", re.I)


def _a_condition_of_this_food(names, understood):
    text = _text(understood)
    match = _A_CONDITION.search(text)
    if match is None:
        return False
    organ = match.group(1).lower()
    if organ.endswith("s"):
        organ = organ[:-1]
    low = " " + text.lower() + " "
    if not any(organ in str(name).lower() for name in names):
        return False
    rest = _text({"clean": text[:match.start()] + " " + text[match.end():]})
    if _A_CONDITION.search(rest):
        return False
    for name in names:
        word = str(name).lower()
        if re.search(r"(?<!\w)" + re.escape(word) + r"(?!\w)", rest.lower()):
            return False
    return True


_AN_ADULT = ("mum", "mummy", "mom", "mommy", "mother", "dad", "daddy", "father", "nan", "nana",
             "gran", "granny", "grandma", "grandmother", "grandad", "granddad", "grandpa",
             "grandfather", "husband", "wife", "partner", "boyfriend", "girlfriend", "aunt",
             "auntie", "uncle", "carer", "neighbour", "neighbor", "friend", "mam", "sister",
             "brother", "boss", "colleague")

_A_TABLE_WORD = ("lump", "lumps", "lumpy", "wean", "weans", "weaning", "weaned", "puree",
                 "purees", "mash", "mashes", "mashed", "spoon", "spoons", "spoonful", "bottle",
                 "bottles", "sippy", "finger food", "solids", "texture", "textures")

_A_TABLE_FOOD = frozenset(name for food in FOODS for name in food["names"])


def _a_table_word_is_named(understood):
    low = " " + _text(understood) + " "
    if any((" " + word + " ") in low for word in _A_TABLE_WORD):
        return True
    return any((" " + name + " ") in low for name in _A_TABLE_FOOD)


def _a_pronoun_is_in_the_line(understood):
    low = " " + _text(understood) + " "
    if not any((" " + word + " ") in low for word in _A_CHILD_PRONOUN):
        return False
    if _a_table_word_is_named(understood):
        return True
    return not any((" " + word + " ") in low for word in _AN_ADULT)


def _a_baby_or_a_pronoun(understood):
    if _a_baby_is_named(understood):
        return True
    low = " " + _text(understood) + " "
    if not any((" " + word + " ") in low for word in _A_CHILD_PRONOUN):
        return False
    return not any((" " + word + " ") in low for word in _AN_ADULT)


_OLDER_CHILD_WORD = ("kid", "kids", "child", "children", "son", "daughter", "boy", "girl",
                     "teenager", "teenagers", "teen", "lad", "lass")
_A_BARE_YEAR_FIGURE = re.compile(
    r"\b(?:is|are|aged|at)\s+(?:two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|\d{1,2})\b"
    r"(?!\s*(?:month|months|week|weeks|wk|wks|mth|mths|day|days))")


def _an_age_of_a_year_or_more(understood):
    age = _age_in_months(understood)
    return age is not None and age >= 12


def _of_weaning_age(understood):
    return not _an_age_of_a_year_or_more(understood)


_SELF_PRONOUN = ("i", "i'm", "im", "me", "we", "we're", "you", "you're", "my", "our")
_OWN_EATING = ("eat", "eats", "eating", "ate", "have", "has", "having", "had", "drink", "drinks",
               "drinking", "drank", "cook", "cooks", "cooking", "make", "makes", "making",
               "try", "tries", "trying", "buy", "buying")
_FOR_ME = ("bad for you", "good for you", "healthy for you", "unhealthy for you",
           "for me", "my lunch", "my dinner", "my breakfast", "my tea", "on my plate")

_BABY_ACT = ("breastfeed", "breastfeeds", "breastfeeding", "breast feed", "breast feeding",
             "formula", "wean", "weans", "weaning", "weaned", "milk feed", "milk feeds",
             "drop a feed", "drop a milk feed", "a cup", "open cup", "sippy", "solids",
             "dummy", "teat", "sterilise", "sterilising", "puree", "baby rice", "first foods",
             "finger food", "finger foods", "introduce water", "introduce a cup",
             "introducing water", "introduce solids", "introduce allergens", "first tastes",
             "the first taste",
             "mash", "mashed", "mashing", "mashed up", "squash it", "fork mash")

_INTRODUCES_A_FOOD = re.compile(
    r"\b(?:introduc(?:e|ing|ed)|first\s+(?:taste|try|time\s+giving)|start(?:ing)?\s+giving)\b")
_NOT_MY_DIET = ("diet", "into my", "to my diet", "for me", "myself", "my own")


_A_FEEDING_PHRASE = ("jars or pouches", "jars and pouches", "jars as good", "pouches as good",
                     "jars or homemade", "pouches or homemade", "own purees", "purees or",
                     "puree or jars", "buy jars", "shop bought", "shop-bought",
                     "ready made pots", "ready-made pots", "rusk", "rusks",
                     "how much milk should i give",
                     "jar", "jars", "pouch", "pouches", "puree", "purees", "pureed")
_GIVING_WATER = ("give water", "giving water", "give them water", "give him water",
                 "give her water", "start giving water")
_GIVING_WATER_ASKS = frozenset("when can should how howmuch age what".split())
_GIVING_WATER_OUT = frozenset("""plant plants cactus cacti garden gardens flower flowers tree trees
    grass lawn shrub shrubs seedling seedlings houseplant houseplants dog dogs puppy puppies cat
    cats kitten kittens pet pets vet hamster rabbit bird birds fish pond""".split())


_WHILE_SHE_FEEDS = re.compile(
    r"\bwhile (?:breastfeeding|breast feeding|nursing|lactating|chestfeeding)\b"
    r"|\bwhen (?:breastfeeding|breast feeding|nursing|lactating)\b"
    r"|\bbreastfeeding (?:can|should|could|may|is|and)\b", re.I)
_HER_OWN_EATING = re.compile(
    r"\b(?:can|should|could|may|do) i (?:eat|drink|have|avoid|skip|cut out)\b"
    r"|\bis it (?:ok|okay|safe|fine) to (?:eat|drink|have)\b"
    r"|\banything i (?:cant|can't|shouldnt|shouldn't) (?:eat|drink|have)\b"
    r"|\bwhat can i (?:eat|drink|have)\b", re.I)


def _says_the_speaker_is_eating(words, said):
    if any(phrase in said for phrase in _FOR_ME):
        return True
    for index, word in enumerate(words):
        if word in _SELF_PRONOUN:
            if index + 1 < len(words) and words[index + 1] in _A_CHILD + BABY:
                continue
            if any(later in _OWN_EATING for later in words[index + 1:index + 4]):
                return True
    return False


def _the_line_feeds_somebody(understood, memory):
    word_list = [str(word).lower() for word in (understood.get("words") or ())]
    words = set(word_list)
    said = _text(understood)
    padded = " %s " % said
    if (understood.get("topic") == "pets" or understood.get("topic_own") == "pets"):
        if not _a_baby_is_named(understood) and _age_in_months(understood) is None:
            return False
    if any(cue in padded for cue in _FOR_A_GROWN_UP):
        return False
    stripped = _names_no_baby(said)
    names_a_baby = (any((" %s " % word) in stripped for word in _NAMES_A_BABY)
                    or bool(_AGE_FIGURE.search(stripped)))
    feeds = any(phrase in padded for phrase in _A_FEEDING_PHRASE)
    if not feeds and len(word_list) >= 3 and words & _GIVING_WATER_ASKS:
        if any(phrase in padded for phrase in _GIVING_WATER):
            feeds = not any((" %s " % word) in padded for word in _GIVING_WATER_OUT)
    if not feeds and _INTRODUCES_A_FOOD.search(padded) and not any(
            cue in padded for cue in _NOT_MY_DIET) and any(
            (" " + word + " ") in padded for word in _ALLERGEN_FOOD - {"bottle", "formula"}):
        feeds = True
    if not names_a_baby and not feeds and _says_the_speaker_is_eating(word_list, said):
        return False
    if (not names_a_baby and _WHILE_SHE_FEEDS.search(said)
            and _HER_OWN_EATING.search(said)):
        return False
    if _a_baby_is_named(understood):
        return True
    if _age_in_months(understood) is not None:
        return True
    if feeds:
        return True
    if words & {"he", "she", "him", "her", "his", "hers", "they"}:
        return not _the_pronoun_is_an_animal(understood)
    if _says_the_speaker_is_eating(word_list, said):
        return False
    if any(" %s " % act in padded for act in _BABY_ACT):
        return True
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return False
    said_now = said.strip().lower()
    for turn in reversed(turns):
        if not isinstance(turn, dict):
            continue
        text = str(turn.get("user") or "").strip().lower()
        if not text or text == said_now:
            continue
        earlier = " %s " % text
        if _AGE_FIGURE.search(earlier):
            return True
        if any(" %s " % word in earlier for word in _NAMES_A_BABY):
            return True
    return False


_ALLERGEN_ROW = (
    "Give the common allergens early and often rather than late: from six months, one at a "
    "time, on a day they are well and in the morning - peanut, egg, milk, wheat, fish, "
    "shellfish, sesame and soya. Once a food is in, keep giving it a couple of times a "
    "week, because stopping is what raises the risk. With severe eczema or a reaction "
    "already, ask a GP before starting.")

_ALLERGEN_FOOD = frozenset((
    "allergen", "allergens", "allergy", "allergies", "peanut", "peanuts", "peanut butter",
    "egg", "eggs", "milk", "cows milk", "wheat", "fish", "shellfish", "sesame", "soya", "soy",
    "nuts", "nut butter", "dairy", "cheese", "yoghurt", "yogurt", "strawberry",
    "strawberries", "kiwi", "tomato", "food", "foods", "finger food", "finger foods", "solids",
    "weaning", "wean", "puree", "purees", "reaction", "rash", "hives", "eczema", "reflux",
    "formula", "meal", "meals", "breakfast", "lunch", "dinner", "spoon", "lumps"))
_INTRODUCING_PEOPLE = re.compile(
    r"\bintroduc(?:e|ing|ed)\b.*?\bto (?:a|an|the|my|our|her|his|their|each)\b")


def _the_allergen_row(memory, understood):
    text = " " + _text(understood) + " "
    if _INTRODUCING_PEOPLE.search(text) and not any(
            (" " + word + " ") in text for word in _ALLERGEN_FOOD):
        return ""
    return _ALLERGEN_ROW
_GROWN_UP = ("mum", "mums", "mom", "moms", "mother", "mam", "dad", "dads", "father", "stepdad",
             "stepmum", "stepmom", "gran", "grans", "granny", "grandma", "grandad", "grandpa",
             "nana", "nan", "pop", "husband", "wife", "partner", "boyfriend", "girlfriend",
             "brother", "brothers", "sister", "sisters", "friend", "friends", "neighbour",
             "neighbor", "colleague", "boss", "aunt", "auntie", "uncle", "cousin", "housemate",
             "flatmate", "roommate", "carer", "client", "customer", "patient", "man", "woman",
             "lady", "gentleman", "fella", "guy", "bloke", "she", "he", "her", "him")


_ANIMAL = ("dog", "dogs", "puppy", "puppies", "pup", "pups", "cat", "cats", "kitten",
           "kittens", "rabbit", "rabbits", "hamster", "hamsters", "guinea", "pig", "pigs",
           "parrot", "bird", "birds", "horse", "horses", "pet", "pets", "vet")


def _the_pronoun_is_an_animal(understood):
    places = []
    ref = understood.get("ref")
    if isinstance(ref, dict):
        places.extend(value for key, value in ref.items()
                      if key in ("he", "she", "they", "him", "her") and isinstance(value, str))
    leans = understood.get("leans_on")
    if isinstance(leans, dict):
        places.extend(str(leans.get(key) or "") for key in ("subject", "text"))
    for place in places:
        words = [word for word in re.split(r"[^a-z']+", place.lower()) if word]
        if any(word in _ANIMAL for word in words):
            return True
    return False


def _the_pronoun_is_a_grown_up(understood):
    ref = understood.get("ref")
    if not isinstance(ref, dict):
        return False
    for key in ("he", "she", "they", "him", "her"):
        place = ref.get(key)
        if not isinstance(place, str) or not place.strip():
            continue
        words = [word for word in re.split(r"[^a-z']+", place.lower()) if word]
        if any(word in _BABY or word in _A_CHILD_PRONOUN or word in ("one", "baby", "child")
               for word in words):
            continue
        if any(word in _GROWN_UP for word in words):
            return True
    return False


def _verdict(names, reply, extra=(), bias=0, own_ask=None, pronoun=False):
    def answer(memory, understood):
        if _a_condition_of_this_food(names, understood):
            return ""
        if own_ask is not None and own_ask(understood):
            return reply
        if _a_baby_is_named(understood):
            return reply
        if _a_pronoun_is_in_the_line(understood):
            age = _age_in_the_chat(memory, understood)
            if age is not None:
                return reply if age <= _A_BABY_TILL else ""
            if _the_pronoun_is_a_grown_up(understood) and not _a_table_word_is_named(understood):
                return ""
            return reply
        age = _age_in_the_chat(memory, understood)
        if age is not None and age <= _A_BABY_TILL:
            return reply
        leans = understood.get("leans_on")
        if isinstance(leans, dict) and isinstance(leans.get("words"), list):
            before = " " + " ".join(w for w in leans["words"] if isinstance(w, str)) + " "
            if any((" " + word + " ") in before for word in _BABY + _A_CHILD_PRONOUN):
                return reply
        return ""

    child = BABY + _A_CHILD_PRONOUN if pronoun else BABY
    return entry("babyfood-" + re.sub(r"[^a-z0-9]+", "-", names[0]),
                 (names, child, _VERDICT_ASK), answer, ask=_VERDICT_ASK, bias=bias,
                 avoid=STAND_DOWN + extra)


_SEASON_OF_A_SHOW = re.compile(
    r"\b(?:season\s*(?:\d+|one|two|three|four|five|six)|this season|next season|last season"
    r"|new season|the season|final season|first season|episodes?|series|box set|binge"
    r"|football|cricket|rugby|premier league|the league|league|fixtures?|match|matches"
    r"|team|teams|gym|the show|on tv|netflix)\b")


def _not_a_season_of_a_show(understood):
    low = " " + _text(understood) + " "
    if any((" " + word + " ") in low for word in _BABY + _A_CHILD):
        return True
    return not _SEASON_OF_A_SHOW.search(low)


def _a_child_is_in_the_line(understood):
    low = " " + _text(understood) + " "
    if any((" " + word + " ") in low for word in BABY + _A_CHILD) or _AGE_FIGURE.search(low):
        return True
    if _SEASON_OF_A_SHOW.search(low):
        return False
    return any((" " + word + " ") in low for word in _A_CHILD_PRONOUN)


_WAKE_TO_FEED_KEY = (
    ("should i wake", "shall i wake", "do i need to wake", "do i have to wake", "can i wake",
     "could i wake", "how do i wake", "how often should i wake", "how long should i let",
     "wake my baby", "wake my newborn", "wake the baby", "wake a baby",
     "wake up for a feed", "wake a sleepy baby", "wake a sleepy newborn", "wake a sleepy",
     "sleepy for a feed", "too sleepy to feed"),
    BABY + ("feed", "feeds", "feeding", "night", "nights", "sleep", "sleeping",
            "slept", "through the night", "should i", "do i need to", "how often",
            "how long"))
_WAKE_TO_FEED_WORDS = frozenset(
    word for part in _WAKE_TO_FEED_KEY for word in part)
ENTRIES = [
    entry("babyfood-by-age", (_WHAT_TO_FEED, AGE, EATING), _by_age, ask=AGE, bias=1,
          guard=_a_baby_or_a_pronoun,
          avoid=STAND_DOWN + ("drink", "drinks", "drinking", "drank", "thirsty", "fluids",
                              "hydrate", "hydrated")),
    entry("babyfood-family-food",
          (_BABY + ("child", "children", "kid", "kids", "toddler", "toddlers", "1 year old",
                    "one year old"),
           ("what we eat", "what you eat", "our food", "our dinner", "our meals", "family food",
            "family meal", "family meals", "the same as us", "same as us", "adult food",
            "grown up food", "eat what we eat", "eat what i eat", "eat the same")),
          "From about a year they can have what the rest of the family eats, with two changes: "
          "take their portion out before the salt goes in, and cut it small - no whole grapes, "
          "whole nuts or popcorn before about four. Before one the food is practice, and milk is "
          "still the meal, so the family dinner is offered alongside it rather than instead of it.",
          bias=1, avoid=NOT_A_MENU + NOT_A_BABY),
    entry("babyfood-finger-foods",
          (("finger food", "finger foods", "fingerfoods", "finger foods for"),
           ("what", "which", "ideas", "list", "good", "best", "options", "suggest", "suggestions")),
          "Sticks and strips they can pick up and hold: cooked carrot, broccoli or green beans, "
          "toast fingers with a thin smear of peanut butter, ripe pear or banana, soft cheese, "
          "scrambled egg, well-cooked chicken or pasta shapes. Cut grapes and cherry tomatoes "
          "lengthways into quarters, cook hard vegetables until they squash between your fingers, "
          "and always have them sitting down while they eat.",
          bias=1, avoid=NOT_A_MENU + NOT_A_BABY + ("when", "how old", "age", "choking", "gagging")),
    entry("babyfood-a-spoon",
          (("spoon", "spoons", "loaded spoon", "cutlery", "fork", "forks",
            "her own spoon", "his own spoon",
            "feed herself", "feed himself", "feed themselves", "feeding herself",
            "feeding himself"),
           BABY + ("give", "gives", "giving", "hold", "holds", "use", "using", "when", "start",
                   "started", "first", "should", "eat", "eating")),
          "From the very first meals, at six months: put a loaded spoon in their hand and let "
          "them get it to their mouth, however badly, while you load another. They will grip it "
          "in a fist at first and get more on the floor than in, and that is the learning, not a "
          "failure. Until they have the pincer grip, around eight or nine months, the spoon works "
          "best with thick things - porridge, mash, yoghurt - and finger food does the rest. Let "
          "them decide when the meal is over, and never shovel a spoon in while they are crying, "
          "because that is how a baby learns to dread the highchair. A children's fork with "
          "rounded prongs is fine too from around nine months, and it does the one job a spoon "
          "cannot - stabbing the piece they have decided they want.",
          bias=3, avoid=NOT_A_MENU + NOT_A_BABY
          + ("cutlery set", "wedding", "christening", "gift", "present", "silver", "antique",
             "my dinner", "i eat", "restaurant")),

    entry("babyfood-refusing-a-cup",
          (("wont drink from a cup", "won't drink from a cup", "wont take a cup",
            "won't take a cup", "refuses a cup", "refuses the cup", "refuses a beaker",
            "will not drink from a cup", "wont drink from a beaker", "wont use a cup",
            "hates the cup", "spits out the cup", "not drinking from a cup",
            "refuses to drink", "wont drink", "won't drink", "refuses milk",
            "wont drink milk", "will not drink"),
           BABY + ("cup", "beaker", "drink", "drinks", "drinking", "water", "milk", "wont",
                   "won't", "refuses", "should", "do", "i")),
          "Keep offering it and don't make it a fight: a little water in an open cup at every "
          "meal, your own cup in your hand at the same time, and no bottle as a fallback in "
          "between. Free-flow beakers and straw cups are worth trying, because a valve bottle "
          "teaches a different suck. Milk is still the main drink until a year, so a baby who "
          "takes only a few sips from a cup is not going short - the cup is practice, and most "
          "get there between nine months and a year.",
          bias=5,
          avoid=NOT_A_BABY
          + tuple(word for word in NOT_A_MENU
                  if word not in ("wont drink", "won't drink", "refuses to drink", "refuses",
                                  "refusing", "refused", "refuse"))
          + ("bottle", "bottles", "teat", "teats", "formula", "breast", "breastfeeding",
             "food", "foods", "eat", "eats", "eating", "solids", "meals")),

    entry("babyfood-stopping-formula",
          (("stop formula", "stop having formula", "stop giving formula", "stop the formula",
            "come off formula", "off formula", "switch to cows milk", "move to cows milk",
            "change to cows milk", "when do i stop formula", "follow on milk", "follow-on milk",
            "stage 2 milk", "hungrier baby milk", "growing up milk"),
           BABY + ("formula", "milk", "when", "stop", "stopped", "switch", "change", "give",
                   "giving", "should", "do i")),
          "First infant milk until the first birthday, then whole cows milk in a cup. There is no "
          "need to move to a follow-on or hungry-baby milk: they are the same kind of thing with "
          "a different label, and the labels are marketing rather than a stage. Do not switch to "
          "cows milk as the main drink before twelve months, because it has too little iron. If "
          "you are stopping breastfeeding rather than formula, drop one feed at a time, about a "
          "week apart, and leave the bedtime one until last.",
          bias=3,
          avoid=NOT_A_BABY + tuple(word for word in NOT_A_MENU if word != "formula")),

    entry("babyfood-which-formula",
          (("formula", "formula milk", "baby formula", "infant formula",
            "first infant milk", "infant milk", "hungry baby milk", "hungry baby",
            "follow on milk", "follow-on milk", "stage 2 milk", "stage 3 milk",
            "growing up milk", "brand of formula", "formula brand", "formula brands"),
           ("which", "what", "best", "better", "switch", "switching", "switched",
            "change", "changing", "changed", "try", "trying", "brand", "brands", "use",
            "using", "buy", "buying", "choose", "choosing", "recommend", "worth", "need",
            "mix", "mixing", "suit", "suits", "baby", "babies", "baby's", "babys",
            "newborn", "infant", "bottle", "bottles", "feed", "feeds", "feeding",
            "milk", "colic", "colicky", "reflux")),
          ("Every first infant milk sold has to meet the same standard, so the brand matters much "
           "less than the price and the tin you can get hold of: pick one first infant milk and "
           "stay with it. Hungry-baby and follow-on milks are the same kind of thing under a "
           "different label, and moving to them is marketing rather than a stage, so there is no "
           "need to change when a baby seems hungrier - offer a little more of the same milk "
           "first, because it is usually volume and not the powder. If you do want a different "
           "brand, change straight over rather than mixing two powders in one bottle, and give it "
           "a few days: a bit of wind, looser nappies or more posseting on a new milk usually "
           "settles, while blood in the nappy, forceful vomiting, a rash or eczema that will not "
           "settle is worth a word with the health visitor about a milk-free trial."),
          avoid=("how much", "how many", "how often", "ml", "oz", "ounces", "scoop",
                 "scoops", "make up", "making up", "made up", "prepare", "preparing",
                 "sterilise", "sterilising", "steriliser", "kettle", "70c", "70 c",
                 "cool it", "left out", "left over", "two hours", "reheat", "warm up",
                 "bottle warmer", "how long", "how do i make", "cows milk", "whole milk",
                 "temperature", "how hot", "hot water", "boiling", "boil the kettle", "warm it",
                 "the formula for", "formula for the", "area", "circle", "triangle",
                 "equation", "quadratic", "maths", "math", "algebra", "percentage",
                 "spreadsheet", "sheet", "excel", "cell", "cells", "calculate", "gcse",
                 "homework",
                 "column", "columns", "row", "rows", "numbers", "number", "sum", "autosum",
                 "breast", "breastfeeding", "breastfeed", "breastfed", "breast milk",
                 "breastmilk", "expressed", "expressing"),
          ask=("which", "what", "buy", "buying", "brand", "best", "better", "switch", "change",
               "use", "try", "mix", "mixing", "worth", "recommend", "need", "needs", "does",
               "do", "is", "are", "should", "suit", "suits", "right", "good"),
          bias=3),

    entry("babyfood-introducing-a-cup",
          (("introduce water", "introduce a cup", "introduce the cup", "introduce a beaker",
            "introduce a sippy cup", "introduce an open cup", "first cup", "first water",
            "start water", "start a cup", "offer water", "offer a cup", "offer a beaker"),
           ("do i", "i", "we", "should", "when", "how", "baby", "cup", "beaker", "water",
            "drink", "sips")),
          "Water in an open cup, from six months and with meals: a few sips is the whole point, "
          "and an open cup or a free-flow beaker teaches the sip that a valve bottle never does. "
          "Hold the cup with them at first, or use a small one they can get both hands round, and "
          "expect it down the front for a week or two. Milk stays the main drink until a year, so "
          "water is offered rather than pushed, and juice or squash is not needed at all.",
          bias=3, avoid=NOT_A_MENU + NOT_A_BABY
          + ("partner", "boyfriend", "girlfriend", "my son", "my daughter", "new man",
             "new woman", "family", "child to", "to my child", "to my kids")),

    entry("babyfood-butter-and-oil",
          (("butter", "oil", "spread", "margarine", "ghee", "lard", "fats", "fat"),
           BABY + ("have", "has", "eat", "give", "cook", "cooking", "add", "put", "use", "ok",
                   "safe", "can", "should", "in", "on", "for")),
          "Yes, in the amounts you would use yourself: a little unsalted butter or a teaspoon of "
          "rapeseed or olive oil in their mash, on toast, or to cook their vegetables in. Fat is "
          "not the enemy at this age - it carries the vitamins and it is most of what makes a "
          "small stomach feel fed - so do not go for low-fat spreads or skimmed anything before "
          "two. Salt is the thing to watch, and butter is salty, so keep it to a scrape.",
          bias=3, ask=BABY + ("puree", "purees", "mash", "mashed", "solids", "spoon", "bowl",
                              "baby food", "food", "foods"),
          avoid=NOT_A_MENU + NOT_A_BABY
          + ("frying", "deep fry", "fryer", "chip pan", "oven", "car", "engine", "bike",
             "chain", "central heating", "radiator", "boiler", "hair", "skin", "essential oil",
             "drain", "drains", "sink", "plughole", "toilet", "loo", "pipes", "grease",
             "freeze", "freezer",
             "frozen", "thaw", "shelf life", "use by", "go off", "gone off",
             "peanut butter", "peanut", "peanuts", "nut butter", "almond butter", "nuts")),
    entry("babyfood-spices-and-herbs",
          (SPICE_NAMES + ("spice rack", "spicy", "seasoning", "pepper", "chilli", "chili",
                          "garlic", "ginger", "curry", "curries", "mild curry"),
           BABY),
          "Yes, and earlier is better than later: mild spices and herbs - cumin, cinnamon, "
          "turmeric, garlic, ginger, parsley, coriander - from six months, in the food you cook "
          "for the family. A baby who meets flavour early is usually the one who eats more widely "
          "at two. What to leave out is the heat and the salt: no chilli heat, no salt, no stock "
          "cubes. Black pepper in cooking is fine; a hot dish is not, because it is painful "
          "rather than dangerous.",
          bias=3, avoid=NOT_A_MENU + NOT_A_BABY
          + ("grow", "growing", "plant", "sow", "garden", "windowsill", "recipe", "bake",
             "spice rack", "where to buy", "grind",
             "in the eye", "in her eye", "in his eye", "in their eye", "in my eye",
             "eye is", "eyes are", "eye hurts", "eyes hurt", "eyeball", "screaming",
             "breastfeeding", "breast feeding", "breast-feeding", "nursing", "lactating",
             "while im feeding", "while breastfeeding"),
          guard=_a_child_is_in_the_line),

    entry("babyfood-eczema-and-egg",
          (("eczema", "dry skin", "flaky skin", "hives", "my baby has eczema", "baby eczema",
            "eczema and egg", "egg and eczema"),
           ("egg", "eggs", "peanut", "peanuts", "peanut butter", "milk", "dairy", "wheat",
            "soya", "soy", "sesame", "fish", "nut", "nuts", "allergen", "allergens", "allergy",
            "shellfish", "give", "start", "try", "introduce")),
          "Yes, and don't put it off because of the eczema: a baby with eczema is the one most "
          "likely to react, and early, regular tastes of egg and peanut lower the chance of a "
          "real allergy rather than raising it. Give a small amount in the morning, at home, on "
          "a day you are not going out, and keep it in their diet a couple of times a week once "
          "it is fine. If the eczema is bad or already infected, ask the GP or health visitor "
          "before you start, and if there is a reaction - hives, swelling, vomiting, wheeze - "
          "stop and call 999 if the breathing changes.",
          bias=8, ask=("give", "start", "try", "introduce", "have", "eat", "can i"),
          avoid=NOT_A_BABY + tuple(word for word in NOT_A_MENU if word != "eczema")
          + ("my eczema", "i have eczema", "my skin", "itchy", "flare", "cream", "emollient",
             "steroid", "bad", "worse", "infected", "weeping", "oozing")),

    entry("babyfood-which-milk",
          (("what milk", "which milk", "what kind of milk", "what type of milk", "best milk"),
           BABY + AGE + ("give", "giving", "should", "for", "to", "use", "buy")),
          _milk_volume, ask=BABY + AGE + ("give", "giving", "should", "use"),
          bias=3, avoid=NOT_A_MENU + NOT_A_BABY + WEANING_ELSEWHERE + _NOT_A_BABY_MILK),
    entry("babyfood-plant-milks",
          (("rice milk", "rice drink", "oat milk", "oat drink", "almond milk", "soya milk",
            "soy milk", "soya drink", "coconut milk", "coconut drink", "plant milk",
            "plant based milk", "hemp milk", "cashew milk", "pea milk", "milk alternative"),
           BABY + AGE + ("have", "has", "give", "giving", "drink", "drinks", "drinking", "ok",
                         "safe", "use", "cook", "cooking", "instead", "can", "should")),
          _plant_milk, ask=("have", "has", "give", "giving", "drink", "drinks", "drinking",
                            "ok", "safe", "use", "cook", "cooking", "instead", "can", "should"),
          bias=4, avoid=NOT_A_MENU + NOT_A_BABY + WEANING_ELSEWHERE),
    entry("babyfood-how-much-milk", (_MILK_WORDS, _MILK_HOW_MUCH, _A_DRINK),
          _milk_volume, ask=BABY + AGE + _THE_CHILD, bias=2,
          avoid=NOT_A_MENU + NOT_A_BABY + WEANING_ELSEWHERE + _NOT_A_BABY_MILK),
    entry("babyfood-what-a-baby-drinks",
          (BABY, ("what can my baby drink", "what can a baby drink", "what can babies drink",
                  "what should my baby drink", "what can my baby have to drink",
                  "how much should my baby drink", "how much should a baby drink",
                  "how much can my baby drink", "how much should babies drink",
                  "how much can a baby drink",
                  "straw", "straws", "sippy cup", "open cup",
                  "drink", "drinks", "drinking")),
          _what_a_baby_drinks,
          bias=4, ask=BABY + AGE,
          avoid=NOT_A_MENU + NOT_A_BABY + _NOT_A_BABY_MILK + _A_COUNT),
    entry("babyfood-getting-enough",
          (BABY, ("enough", "getting enough", "fed", "feeding well", "putting on weight")),
          "The signs are the answer, not an amount: six or more wet nappies a day, dirty nappies "
          "that turn from black to yellow in the first week, steady weight along their own line, "
          "and a baby who settles after a feed and is alert when awake. A baby who is drowsy, "
          "has fewer wet nappies or is not back to birth weight by two weeks needs to be seen.",
          bias=2,
          avoid=NOT_A_MENU + NOT_A_BABY
          + ("toddler", "toddlers", "how much", "iron", "vitamin", "vitamins", "vitamin d",
             "calcium", "protein", "calories", "fibre", "fiber", "sleep", "sleeping",
             "i put on", "i have put on", "ive put on", "i've put on", "i gained",
             "lose weight", "losing weight", "lose the baby weight", "weight loss",
             "baby weight", "my own weight", "back to my old weight", "slimming")),
    entry("babyfood-ready-for-solids",
          (BABY + _A_CHILD_PRONOUN,
           ("ready", "readiness", "start solids", "starting solids",
                  "start on solids", "starting on solids", "first tastes",
                  "the signs", "signs of", "any signs", "any sign", "a sign", "show signs",
                  "shows signs", "showing signs", "signs that", "signs should", "signs to",
                  "introduce solids", "introducing solids", "introduce food",
                  "introducing food", "give solids", "when to wean",
                  "solids", "solid food", "solid foods",
                  "too young", "too early", "old enough", "young for solids",
                  "young for food", "early for solids",
                  "start giving", "start food", "starting food", "start on food",
                  "give food", "giving food", "ready for food", "food ready",
                  "give her food", "give him food", "first food")),
          "Three signs, all at once, and around six months: sitting up with little or no "
          "support, steady head control, and swallowing food rather than pushing it back out "
          "with the tongue. Reaching for your plate or waking at night is not a sign on its "
          "own. Before four months is too early, and by six months it is time - waiting longer "
          "makes the iron and the chewing harder.",
          guard=_a_baby_or_a_pronoun,
          bias=1, avoid=STAND_DOWN + BOOK_WORDS),
    entry("babyfood-what-to-feed", (_WHAT_TO_FEED, BABY + _A_CHILD_PRONOUN), _FIRST_FOODS,
          guard=lambda u: _a_baby_or_a_pronoun(u) and _of_weaning_age(u),
          ask=EATING + ("give", "gives", "giving", "first", "start", "starting"),
          avoid=STAND_DOWN + ("breakfast", "lunch", "dinner", "supper", "snack", "snacks",
                             "bottle", "bottles", "teat", "teats", "cup", "cups", "sippy",
                             "night feed", "night feeds", "night feeding", "off the bottle",
                             "sterilise", "sterilising", "formula")),
    entry("babyfood-baby-led-weaning",
          (("baby led weaning", "baby-led weaning", "blw", "babyled weaning"),
           ("what", "how", "is", "explain", "mean", "means", "safe", "better", "start",
            "started", "starting")),
          "Baby-led weaning means skipping spoon-fed purees and letting them pick up soft "
          "finger food themselves from about six months. It is safe at that age and no more of "
          "a choking risk than spoon feeding, and you do not have to choose: most people end up "
          "doing a mix of both.", bias=1, avoid=NOT_A_MENU + NOT_A_BABY),
    entry("babyfood-puree",
          (BABY, ("puree", "purees", "pureed", "blend", "blended", "lumps", "lumpy", "smooth")),
          "You do not have to: soft finger food is safe from six months and teaches chewing "
          "sooner. If you do puree, keep it thick rather than watery and move on to lumps and "
          "finger food by about eight or nine months - a baby still on smooth food at one is "
          "the one who struggles with texture later.",
          bias=2, avoid=STAND_DOWN + A_BODY_LUMP),
    entry("babyfood-allergens",
          (BABY,
           ("allergen", "allergens", "allergy", "allergies", "sensitive", "sensitivities",
            "introduce", "introducing")),
          _the_allergen_row, bias=3, avoid=STAND_DOWN),
    entry("babyfood-first-taste",
          (("introduce", "introducing", "introduced", "first taste", "first tastes",
            "first time giving", "start giving", "start on"),
           ("egg", "eggs", "milk", "cow's milk", "cows milk", "peanut", "peanuts",
            "peanut butter", "nut butter", "wheat", "fish", "sesame", "soya", "nuts", "dairy",
            "cheese", "yoghurt", "yogurt", "strawberry", "kiwi", "food", "foods", "finger food",
            "solids", "allergen", "allergens", "puree", "lumps")),
          ("One new food at a time, in the morning on a day they are well: a teaspoon is a first "
           "taste, then watch for twenty minutes, and a rash, swelling or sickness means stop and "
           "ring 111. Once a food is in, keep giving it a couple of times a week, because stopping "
           "is what raises the risk. Peanut and egg are the ones worth doing early rather than "
           "late, and with severe eczema or a reaction already, ask a GP before starting."),
          bias=2, avoid=STAND_DOWN + ("bottle", "bottles", "bottle feed", "formula", "dummy")),
    entry("babyfood-snacks", (_SNACK, _SNACK_CHILD), _snacks, bias=1,
          avoid=NOT_A_MENU + NOT_A_BABY + _NOT_A_SNACK),
    entry("babyfood-shop-bought",
          (("jar", "jars", "pouch", "pouches", "shop bought", "shop-bought", "ready made",
            "ready-made", "baby food", "commercial", "supermarket"),
           ("ok", "fine", "good", "safe", "healthy", "buy", "worth", "reheat", "warm", "use",
            "best", "better", "any good", "have", "give", "can")),
          "Jars, pouches and ready-made pots are fine, and the rules on them are the same as on "
          "anything else: no salt, no sugar, no honey before one. Read the stage on the front "
          "against what they are managing now, decant it into a bowl rather than feeding from the "
          "pouch, and throw away what the spoon has been in. Warm it by standing the bowl in hot "
          "water, never in the pouch or the jar, and check it is not hot in the middle.",
          bias=2, avoid=NOT_A_MENU + NOT_A_BABY
          + ("fridge", "freezer", "keep", "last", "left out", "defrost", "batch")),
    entry("babyfood-ice-cream",
          (("ice cream", "icecream", "ice lolly", "ice lollies", "lolly", "lollies", "gelato"),
           BABY + ("toddler", "child", "children", "kid", "kids", "1 year old", "one year old")),
          "A taste of plain ice cream from six months is fine, and it is the sugar rather than the "
          "cold that is the reason not to make it a habit: the shop stuff is mostly sugar, and the "
          "cones are a choking shape for a baby. Frozen yoghurt, a frozen banana or a lolly made "
          "from fruit puree gives the same thing with less sugar in it.",
          bias=1, avoid=NOT_A_MENU + NOT_A_BABY),
    entry("babyfood-only-milk",
          (("only wants milk", "only wants Breast milk", "only drinks milk", "no interest in food",
            "not interested in food", "won't eat", "wont eat", "will not eat", "refuses food",
            "refusing food", "won't take food", "wont take food", "spits it out",
            "pushed the spoon away", "pushes the spoon away", "pushed the spoon", "spoon away",
            "pushed it away", "pushes it away", "pushes the food away", "pushed the food away",
            "spat it out", "spat the food out", "spat out", "turns her head away",
            "turns his head away", "turns away from the spoon", "turns away from food",
            "closes her mouth", "closes his mouth", "shakes her head", "shakes his head",
            "wont take the spoon", "won't take the spoon", "wont open her mouth",
            "won't open his mouth",
            "spits the food out", "spitting the food out", "spits food out", "spitting food out",
            "keeps spitting the food out", "keeps spitting food out", "spitting it out",
            "keeps spitting it out", "spits it all out", "spitting it all out",
            "spits his food out", "spits her food out", "spat the food out"),
           BABY + _A_CHILD_PRONOUN
           + ("child", "children", "kid", "kids", "toddler", "toddlers")),
          "That is normal for the first weeks: milk is still their food, and eating is practice. "
          "Keep offering one or two teaspoons once a day without coaxing, put them in the chair "
          "with you eating at the same time, and let them see the food rather than putting it in "
          "their mouth. Go to the health visitor if they are past nine months and still taking "
          "almost nothing, if they are dropping weight, or if they gag and cough on every texture.",
          bias=1,
          guard=lambda u: _a_baby_is_named(u) or _a_pronoun_is_in_the_line(u),
          avoid=tuple(word for word in NOT_A_MENU + NOT_A_BABY
                      + ("ill", "unwell", "poorly", "temperature", "fever", "sick")
                      if word not in _THE_REFUSAL_WORDS)
                  + ("toddler", "toddlers", "child", "children", "kid", "kids")),
    entry("babyfood-lumpy-food",
          (("refuses lumpy food", "refusing lumpy food", "won't eat lumpy food",
            "lumpy food", "lumpy foods", "lumpy", "refuses lumps", "hates lumps", "lumps",
            "lumpier", "texture", "textures", "chewy",
            "bits of food", "bits of it", "the bits", "spits the bits", "chunks"),
           _BABY + _THE_CHILD
           + ("refuse", "refuses", "refusing", "refused", "hates", "hate", "won't", "wont",
              "will not", "spits", "gags", "struggles", "too early", "have", "has", "try",
              "start", "move on", "when", "can")),
          "Do not blend it back: the window for lumps is about seven to nine months, and a baby "
          "who stays on smooth food gets crosser about texture later. Mash rather than puree, "
          "leave soft lumps you can squash with a fork, and give finger food next to the spoon so "
          "they are practising chewing whatever the spoon does. Gagging while they learn is normal "
          "and it is not choking - stay calm, sit them up, and let them bring it forward.",
          bias=4,
          guard=lambda u: (_a_baby_is_named(u) or _a_pronoun_is_in_the_line(u)) \
          and not_the_heat_of_an_argument(u),
          avoid=NOT_A_BABY + WEANING_ELSEWHERE + _HOW_MUCH_MILK
          + ("nails", "nail", "fingernails", "fingernail", "nail biting", "cuticles",
             "choking", "choke", "first aid", "fever", "temperature", "rash", "ill", "unwell",
             "poorly", "not feeding", "isnt feeding", "breathing", "hospital", "999", "111",
             ) + A_BODY_LUMP),
    entry("babyfood-lump-in-mouth",
          (("lump in his mouth", "lump in her mouth", "lump in their mouth", "lump in the mouth",
            "lump in his gums", "lump on his gums", "lump on her gums", "lump on the gum",
            "lump on his gum", "lump on her gum", "lump in his cheek", "lump on his cheek",
            "lump on her cheek", "lump on the cheek", "lump inside his cheek",
            "lump under his tongue", "lump on his tongue", "lump on his lip", "lump on her lip",
            "lump on the roof of his mouth", "bump in his mouth", "bump on his gum",
            "bump on his cheek", "white lump in his mouth", "lump inside his mouth"),
           ("baby", "babies", "newborn", "month old", "months old", "year old", "toddler",
            "child", "son", "daughter", "kid", "what", "why", "should", "worried", "is it",
            "normal", "check", "how", "have", "has", "got", "noticed", "found", "there is")),
          "Most lumps in a baby's mouth are harmless: the little white pearls on the gums of a "
          "newborn, a mucocele from a bite on the lip, or a firm bony bump on the roof of the "
          "mouth. Leave it alone, do not squeeze it, and keep the mouth clean. Show it to the "
          "health visitor, a dentist or a GP within two weeks if it is still there after three "
          "weeks, or if it is hard, bleeding, growing, or comes with a fever or with a baby who "
          "will not feed - that is a check, not an emergency. A lump on the outside of the cheek "
          "is a skin lump and is usually harmless too; the ones that need a look are the same "
          "ones, plus anything that is hot and spreading.",
          bias=4,
          avoid=NOT_A_BABY + WEANING_ELSEWHERE + _HOW_MUCH_MILK
          + ("tooth", "teeth", "teething", "toothache", "dentist appointment", "brace", "braces",
             "ulcer", "ulcers", "cold sore", "blister", "blisters", "hand foot and mouth",
             "chickenpox", "measles", "mumps", "tonsil", "tonsils", "tongue tie")),

    entry("babyfood-food-reaction",
          (BABY + ("child", "children", "kid", "kids", "toddler", "toddlers", "1 year old",
                   "one year old"),
           ("reaction", "reacted", "reacts", "reacting", "allergic", "allergy", "hives",
            "swollen", "swelling", "rash round the mouth", "sick after eating")),
          "Stop giving that food and watch them for the next two hours. A rash, hives, swelling "
          "round the mouth, vomiting or a runny tummy is worth a same-day call to the GP or 111, "
          "and write down what they ate, how much and how long it took. Swelling of the lips or "
          "tongue, a hoarse cry, noisy breathing, or going pale and floppy is 999 - that is "
          "anaphylaxis and it needs an ambulance, not a wait. Do not try that food again until "
          "you have been told it is safe to.",
          bias=4,
          avoid=NOT_A_BABY
          + ("breathing", "wheeze", "floppy", "limp", "unresponsive", "999", "ambulance",
             "epipen", "epi pen", "tongue", "hay fever", "hayfever", "vaccine", "vaccination",
             "jab", "jabs", "mmr", "immunisation", "nappy rash", "teething", "covid")),
    entry("babyfood-dropping-feeds",
          (("drop a milk feed", "drop a feed", "drop feeds", "dropping feeds",
            "stop breastfeeding", "stop breast feeding", "stop nursing", "stop feeding",
            "wean off the breast", "give up breastfeeding", "finish breastfeeding",
            "dropping milk feeds", "drop a bottle", "drop the bottle", "dropping bottles",
            "cut down feeds", "cut down bottles", "cut down on bottles", "fewer feeds",
            "fewer bottles", "give up a feed", "stop a feed", "stopping feeds", "reduce feeds",
            "reduce milk", "less interested in milk", "feeding less"),
           BABY + ("milk", "bottles", "bottle", "feeds", "feed", "bf", "breastfeeding",
                   "child", "children", "kid", "kids", "toddler", "toddlers")),
          "One feed at a time, about a week apart, and start with the one they are least "
          "bothered about - usually the mid-morning or mid-afternoon bottle rather than the first "
          "or the bedtime one. Offer a cup and a snack at the time you dropped, expect a few "
          "grumpy days, and keep the bedtime feed longest because it is doing the most work. Milk "
          "falling as food rises is the plan, not a problem: by a year three meals, two snacks "
          "and about 350 to 400ml of milk a day is enough.",
          bias=3,
          avoid=NOT_A_MENU + NOT_A_BABY + _HOW_MUCH_MILK
          + ("newborn", "newborns", "neonate", "weeks old", "week old", "1 month old",
             "2 month old", "3 month old", "one month old", "two month old", "three month old",
             "not feeding", "isnt feeding", "isn't feeding", "refusing feeds", "not taking feeds",
             "too sleepy")),
    entry("babyfood-what-to-avoid",
          (("what foods to avoid", "foods to avoid", "what food to avoid", "what not to give",
            "foods not to give", "what not to feed", "foods not to feed",
            "what should i not give", "what should i not feed", "what shouldnt i give",
            "what shouldn't i give", "what should i avoid", "foods should i avoid",
            "avoid giving", "foods to avoid giving", "what to avoid giving",
            "not feed my baby", "not feed a baby", "not give my baby", "should i not feed",
            "foods are unsafe",
            "unsafe foods", "what is unsafe to give", "what is unsafe to feed",
            "what cant my baby eat", "what can't my baby eat", "what can a baby not eat",
            "what cant a baby eat", "what can't a baby eat"),
           BABY + AGE + _THE_CHILD,
           ("avoid", "unsafe", "not", "give", "giving", "feed", "feeding", "eat", "eating",
            "food", "foods", "should", "what", "can")),
          "No salt and no sugar, and no honey at all before the first birthday. No whole nuts, "
          "whole grapes, popcorn or anything hard and round, because those are the shapes that "
          "block a small throat - cut grapes and cherry tomatoes into quarters lengthways. Skip "
          "low-fat and diet foods, unpasteurised cheese, raw or runny egg without the red lion "
          "stamp, and shark, swordfish and marlin. Cow's milk as a drink waits until twelve "
          "months, though in cooking it is fine from six; tea, coffee, cola and juice are not "
          "needed at any age.",
          bias=5,
          avoid=NOT_A_MENU + NOT_A_BABY + WEANING_ELSEWHERE
          + ("water", "juice", "squash", "milk", "drink", "drinks", "drinking", "thirsty",
             "bottle", "bottles", "cup",
             "breastfeeding", "breast feeding", "breast-feeding", "nursing", "lactating",
             "chestfeeding", "while im feeding"),
          ask=("avoid", "not", "unsafe", "give", "giving", "feed", "feeding", "eat", "eating")),
    entry("babyfood-how-much-water",
          (("how much water", "how much water should", "how much water can",
            "how much juice", "how much squash"),
           BABY + ("child", "children", "kid", "kids", "drink", "drinks", "day")),
          _how_much_water,
          bias=4,
          guard=lambda u: _a_baby_is_named(u) or _a_pronoun_is_in_the_line(u),
          avoid=NOT_A_BABY
          + tuple(word for word in NOT_A_MENU
                  if word not in ("how much water", "how much juice"))
          + ("toddler", "toddlers", "child", "children", "kids", "2 year", "3 year", "4 year",
             "5 year", "i drink", "should i drink")),
    entry("babyfood-wake-to-feed",
          _WAKE_TO_FEED_KEY,
          "No, not once they are back to their birth weight and gaining: a baby who sleeps is "
          "allowed to sleep, and night waking is normal for the first months. Wake them for a "
          "feed only if they are under two weeks old, were early or small, are jaundiced, are not "
          "yet back to their birth weight or are too sleepy to take a full feed - then offer every "
          "two to three hours, and make it worth their while: change the nappy first, undress them "
          "to the vest, and stroke a cool flannel over the hands and face.",
          bias=3,
          avoid=tuple(word for word in NOT_A_MENU
                      if word not in _WAKE_TO_FEED_WORDS)
          + ("alarm", "alarm clock", "wake up early", "wake up tired", "wake up at night",
             "cant sleep", "can't sleep", "insomnia", "tired all the time", "wake up",
             "woken up by", "wake me up", "for the wake", "funeral")),
] + [_verdict(row["names"], row["reply"], row.get("extra", ()), row.get("bias", 0),
                 row.get("own_ask"), row.get("pronoun", False))
     for row in FOODS]


def _a_line_that_feeds_a_baby(understood):
    if _the_line_feeds_somebody(understood, {}):
        return True
    leans = understood.get("leans_on") if isinstance(understood, dict) else None
    words = leans.get("words") if isinstance(leans, dict) else None
    if not isinstance(words, list):
        return False
    carried = " %s " % " ".join(str(word).lower() for word in words if isinstance(word, str))
    if _AGE_FIGURE.search(carried):
        return True
    return any((" %s " % word) in carried for word in _NAMES_A_BABY)


def _only_for_a_baby(row):
    reply = row.reply

    def gated(memory, understood):
        if not _the_line_feeds_somebody(understood, memory):
            return None
        return reply(memory, understood) if callable(reply) else reply

    row.reply = gated
    if getattr(row, "guard", None) is None:
        row.guard = _a_line_that_feeds_a_baby
    return row


ENTRIES = [_only_for_a_baby(row) for row in ENTRIES]
