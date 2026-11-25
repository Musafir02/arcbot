
import re

PRIORITY = 7000

ANSWERS = ("pets", "family-and-parenting")

RECALL_HINTS = ("say", "said", "saying", "remember", "recall", "again", "told", "tell", "know",
                "what's", "whats", "what")

SELF = ("you", "your", "we", "i")

NOT_THE_PLAN = r"(?!\s+for\b)"

ON_A_MEDIUM_OR_AT_A_VENUE = (
    r"telly|tv|television|radio|bbc|itv|channel|netflix|amazon|prime|disney|iplayer|now\s?tv|"
    r"sky|spotify|youtube|cinema|cinemas|pictures|theatre|theater|matinee|gig|gigs|concert|"
    r"concerts|arena|playhouse|"
    r"phone|phones|mobile|screen|screens|monitor|laptop|laptops|computer|computers|pc|"
    r"tablet|tablets|ipad|kindle|speaker|speakers|headphones|earphones|earbuds|device")
NOT_ON_A_MEDIUM = (r"(?!\s*(?:(?:at|in)\s+)?(?:the\s+|a\s+|my\s+|our\s+)?(?:"
                   + ON_A_MEDIUM_OR_AT_A_VENUE + r")\b)")

REPEAT_ADVERB = (r"(?:again|slower|slowly|step by step|once more|clearer|simply|for me|"
                 r"please|thanks|in order)")

LIMITS = ("allergies", "diet", "condition")

DENIAL_SAY = {"allergies": "{Thing} back on the table, then.",
              "condition": "Right, no {thing} \u2014 that makes things easier, then.",
              "diet": "Right \u2014 meat is back on the table, then.",
              "pets": "Right \u2014 no {thing}, then."}

CORRECTED_SAY = {"allergies": "{Thing}, not {old} \u2014 got it.",
                 "condition": "Right, {thing} now, not {old} \u2014 got it."}

RETRACT_SAY = {"allergies": "the allergy note", "condition": "the health note",
               "diet": "the diet note", "budget": "the budget", "job": "the job",
               "city": "the place you live", "from": "where you\u2019re from",
               "born": "where you were born", "age": "your age", "height": "your height",
               "name": "your name", "places": "that place"}

NOT_RETRACTED = ("taste", "other", "people", "pet", None)

_FACT_SLOT = ("(?:job|work|name|budget|allerg\\w*|pets?|cats?|dogs?|kittens?|pupp(?:y|ies)|"
             "animals?|salary|birthday|age|partner|husband|wife|kids?|children|son|daughter|"
             "mum|mom|dad|sister|brother|car|address|postcode)")

PET_AGE_FIX_WORDS = 8

OTHER_SAID = (("name", "is called"), ("allergies", "is allergic to"), ("condition", "has"),
              ("diet", "is"), ("diet", "eats"))

OTHER_KIND_SAY = {"name": "{v}, got it.",
                  "allergies": "{v} it is, then \u2014 I'll keep your {who} off those.",
                  "condition": "{v} it is, then \u2014 I'll keep that in mind for your {who}.",
                  "diet": "{v} it is, then \u2014 that's what I'll go with for your {who}."}

AGE_FIX_WORDS = 8

NAME_FIX_WORDS = 9

NAME_GIVEN_WORDS = 5

UNIT_FAMILY = {"pound": "money", "pounds": "money", "quid": "money", "euro": "money",
               "euros": "money", "dollar": "money", "dollars": "money", "k": "money",
               "kilo": "weight", "kilos": "weight", "kg": "weight", "kgs": "weight",
               "kilogram": "weight", "kilograms": "weight", "stone": "weight",
               "stones": "weight", "st": "weight", "lb": "weight", "lbs": "weight",
               "gram": "weight", "grams": "weight", "g": "weight",
               "cm": "weight", "centimetre": "weight", "centimetres": "weight",
               "centimeter": "weight", "centimeters": "weight", "foot": "weight",
               "feet": "weight", "ft": "weight", "inch": "weight", "inches": "weight",
               "litre": "volume", "litres": "volume", "liter": "volume", "liters": "volume",
               "mile": "distance", "miles": "distance", "km": "distance",
               "minute": "time", "minutes": "time", "min": "time", "mins": "time",
               "hour": "time", "hours": "time", "day": "time", "days": "time",
               "week": "time", "weeks": "time", "month": "time", "months": "time",
               "year": "time", "years": "time"}

FACT_FAMILY = {"budget": "money", "pay": "money", "salary": "money", "wage": "money",
               "rent": "money", "price": "money", "spend": "money",
               "weight": "weight", "height": "weight", "distance": "distance"}

NOT_A_UNIT = (r"in|on|at|for|by|before|after|and|then|this|next|of|to|from|until|till|or|but|so|"
              r"with|without|the|a|an")

AMOUNT_WORD = (r"(?:an?|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve"
               r"|half\s+an?|half|a\s+couple\s+of|a\s+few|a\s+bit\s+of"
               r"|\d+(?:[.,]\d+)?)")

SPELLING_APART = 3

CORRECTION_SAY_DROP = {"allergies": "Got it — no {v}."}

DROP_LISTS = ("allergies",)

CORRECTION_SAY = {"budget": "{v} — got it, I'll work to that.",
                  "pet": "{v} — got it, I'll call the {a} {v}.",
                  "pets_count": "{v} — got it.",
                  "kids": "{v} — got it.",
                  "name": "{v} — got it, I'll call you {v}.",
                  "person_name": "{v} — got it, I'll say {v}.",
                  "age": "{v} — got it, {v} it is.",
                  "weight": "{v} — got it, you weigh {v}.",
                  "city": "{v} — got it, I'll say {v}.",
                  "places": "{v} — got it, I'll say {v}.",
                  "job": "{v} — got it, I'll say {v}.",
                  "plan": "Got it — {v}.",
                  "allergies": "{v} — got it, I'll keep that out of anything I suggest.",
                  "birthday": "Got it — your birthday is {v}.",
                  "line": "{v} — got it."}

CORRECTION_SAY_PAIR = {"plan": "{v}, not {w} — got it."}

PET_RENAMED_SAY = (
    "{v}, not {w} — got it. How's {v} settling in?",
    "Right — {v}, not {w}. That's the name I'll use.",
    "{v}, not {w} — noted. {v} it is from now on.",
    "{v}, not {w}; glad you said. How's {v} getting on?",
)

BARE_ECHO_ONLY = "{v} — got it."

CORRECTION_BACK = 4

AT_TIME_VALUE = (r"(?:\d{1,2}(?:[:.]\d{2})?(?!\d)"
                r"|(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\b"
                r"|noon|midday|midnight)(?:\s*(?:am|pm|o'?clock))?")

KIN_ASK = r"[a-z]+(?:[ \t]*-?[ \t]*in[ \t]*-?[ \t]*laws?)?"

IN_LAW_AFTER_TEXT = r"[ \t]*-?[ \t]*in[ \t]*-?[ \t]*laws?\b"

PRONOUN_FITS = {"his": ("he",), "him": ("he",), "he": ("he",),
                "her": ("she",), "she": ("she",),
                "their": ("he", "she"), "them": ("he", "she"), "they": ("he", "she")}

CHILD_RELATIONS = ("son", "daughter", "child", "kid", "boy", "girl", "stepson", "stepdaughter",
                   "twins")

_ABOUT_WHO = (r"(?:my|our)\s+[a-z]+\b|the\s+(?:kids?|children|child)\b|her\b|him\b|"
              r"them\b|she\b|he\b|they\b")

CHILD = ("son", "daughter", "twins", "baby", "child", "kid", "boy", "girl", "youngest", "eldest",
         "oldest")

CHILD_OF = {"children": "child", "kids": "kid", "childs": "child", "babies": "baby",
            "boys": "boy", "girls": "girl", "sons": "son", "daughters": "daughter"}

FAMILY_GROUP = {
    "parents": ("parent", "mother", "mum", "mom", "mam", "mummy", "mommy", "father", "dad",
                "daddy", "papa", "stepmother", "stepfather"),
    "grandparents": ("grandparent", "grandmother", "grandma", "gran", "nan", "nana", "granny",
                     "grandfather", "grandad", "granddad", "grandpa"),
    "siblings": ("sibling", "brother", "sister", "half brother", "half sister"),
    "brothers": ("brother", "half brother"),
    "sisters": ("sister", "half sister"),
    "kids": CHILD,
    "children": CHILD,
    "twins": ("twin", "son", "daughter", "child", "kid"),
    "boys": ("son", "boy", "child", "kid"),
    "girls": ("daughter", "girl", "child", "kid"),
    "grandchildren": ("grandson", "granddaughter", "grandchild"),
    "uncles": ("uncle",),
    "aunts": ("aunt",),
    "cousins": ("cousin",),
}

FOOD_PHRASES = {
    "nuts": ("peanut butter", "satay sauce", "nut butter", "nut roast", "almond milk"),
    "peanuts": ("peanut butter", "satay sauce", "nut butter"),
    "dairy": ("ice cream", "ice-cream", "milk chocolate", "double cream", "sour cream",
              "cream cheese"),
    "gluten": ("soy sauce", "stock cube", "stock cubes"),
    "wheat": ("soy sauce", "stock cube", "stock cubes"),
}

ADVICE_MODULES = ("answers", "chat")

SLOT_KEY = {
    "name": ("name",),
    "job": ("job",),
    "city": ("city", "town", "from"),
    "budget": ("budget",),
    "allergy": ("allergies", "allergy"),
    "pets": ("pets",),
    "age": ("age",),
}

BARE_SLOTS = (
    ("allergy", r"\ballerg"),
    ("budget", r"\bbudget"),
    ("pets", r"\b(?:dog|cat|pet|animal)s?\b"),
    ("job", r"\b(?:job|work)\b"),
    ("city", r"\b(?:city|place|town)\b"),
    ("name", r"\bname\b"),
    ("age", r"\bage\b"),
)

WHERE_ASK = r"where(?:abouts| abouts)?"

KIN = (r"mum|mom|mother|dad|father|son|daughter|child|kid|wife|husband|partner|brother|sister"
       r"|gran|granny|nan|nana|grandma|grandad|grandpa|grandmother|grandfather|friend|mate|baby"
       r"|children|kids|nephew|niece|aunt|uncle|cousin|stepson|stepdaughter")

BAD_NEWS = (
    r"(?:is|are|was|were|has been|have been|had been|got|has got|have got|got taken"
    r"|has ended up|ended up)?\s*(?:really\s+|very\s+|quite\s+|so\s+)?"
    r"(?:in hospital|in the hospital|in a coma|on a ventilator|unwell|(?:ill|sick)(?!\s+of\b)"
    r"|poorly|dying"
    r"|struggling|getting worse|worse)"
    r"|(?:was|got|has been|had been)?\s*(?:diagnosed|taken into hospital)"
    r"|has cancer|had cancer|has had a fall|had a fall|took a fall|is terminal")

_UNIT_SAID = {"minutes": ("minute", "minutes"), "hours": ("hour", "hours"),
              "steps": ("step", "steps"), "litres": ("litre", "litres"),
              "glasses": ("glass", "glasses"), "km": ("km", "km"),
              "miles": ("mile", "miles"), "days": ("day", "days"), "weeks": ("week", "weeks"),
              "nights": ("night", "nights"), "a week": ("session a week", "sessions a week"),
              "a day": ("session a day", "sessions a day")}

_AMOUNTS = (
    ("a week", r"(?:(?:times?|sessions?|runs?|workouts?|walks?)\s+)?(?:a|per|each)\s+week"),
    ("a day", r"(?:(?:times?|sessions?|glasses?)\s+)?(?:a|per|each)\s+day"),
    ("minutes", r"minutes?|mins?"),
    ("hours", r"hours?|hrs?"),
    ("litres", r"litres?|liters?|l\b"),
    ("glasses", r"glasses?"),
    ("steps", r"steps?"),
    ("km", r"km\b|kilometres?|kilometers?|k\b"),
    ("miles", r"miles?|mi\b"),
    ("days", r"days?"),
    ("weeks", r"weeks?"),
    ("nights", r"nights?"),
    ("grams", r"grams?|grammes?|g\b"),
    ("calories", r"calories|cals?\b|kilocalories|kcals?"),
    ("micrograms", r"micrograms?|microgrammes?|mcgs?|\u00b5g|ug\b"),
    ("milligrams", r"milligrams?|milligrammes?|mgs?"),
)

_AMOUNT_WORDS = {"once": 1, "twice": 2, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
                 "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11,
                 "twelve": 12}

_COUNT_WORD = r"\b(?:\d+(?:,\d{3})*(?:\.\d+)?|(?:once|twice|one|two|three|four|five|six" \
              r"|seven|eight|nine|ten|eleven|twelve)\b)"

_CONVERT = {("minutes", "hours"): 60.0, ("hours", "minutes"): 1 / 60.0,
            ("km", "miles"): 0.621371, ("miles", "km"): 1.609344}

_WEEKLY = "a week"

FIGURE_UNITS = {
    "week": ("week", "weeks", "fortnight", "fortnights"),
    "day": ("day", "days"),
    "month": ("month", "months"),
    "year": ("year", "years"),
    "hour": ("hour", "hours"),
    "minute": ("minute", "minutes"),
    "second": ("second", "seconds"),
    "mile": ("mile", "miles"),
    "km": ("km", "kilometre", "kilometres", "kilometer", "kilometers"),
    "kilo": ("kilo", "kilos", "kg", "kilogram", "kilograms"),
    "stone": ("stone", "stones"),
    "pound": ("pound", "pounds", "lb", "lbs"),
}

FIGURE_TIME = ("week", "day", "month", "year", "hour", "minute", "second")

FIGURE_NUMBER = (r"(?:\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?|a|an|one|two|three|four|five"
                 r"|six|seven|eight|nine|ten|eleven|twelve|fifteen|twenty|thirty|forty|fifty"
                 r"|sixty|ninety|hundred)")

FIGURE_QUALIFIER = (r"(?:about|around|roughly|nearly|almost|up to|at least|over|under|just|only"
                    r"|maybe|probably|another)")

LOOK_BACK_FIGURE = 3

FIGURE_ANSWER_LEN = 120

COUNT_WORD = (r"(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen"
              r"|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty"
              r"|hundred|dozen|couple|few|several|lot|lots|plenty|number)")

PLACE_NOT = ("the|a|an|my|his|her|their|our|your|its|it|this|that|these|those|order|time|general"
             "|total|all|front|charge|public|private|fact|mind|particular|future|past|advance"
             "|june|july|may|march|april|august|september|october|november|december|january"
             "|february|monday|tuesday|wednesday|thursday|friday|saturday|sunday|home|work|bed"
             "|town|touch|least|once|twice|night|morning|evening|afternoon|weekend|month|year"
             "|between|case|some|any|no|one|two|first|last|next|same|other|else|person|people")

TURNED = {"we": "you", "our": "your", "my": "your", "us": "you", "me": "you",
          "im": "you are", "i": "you", "ive": "you've"}

PART_HELD = {
    "job": "job", "jobs": "job", "work": "job", "role": "job", "shift": "job", "shifts": "job",
    "hours": "job", "pay": "job", "salary": "job", "boss": "job", "colleagues": "job",
    "son": "people", "daughter": "people", "kid": "kids", "kids": "kids", "child": "kids",
    "children": "kids", "mum": "people", "dad": "people", "mother": "people",
    "father": "people", "sister": "people", "brother": "people", "partner": "people",
    "wife": "people", "husband": "people", "family": "people", "parents": "people",
    "dog": "pets", "cat": "pets", "puppy": "pets", "kitten": "pets", "pets": "pets",
    "car": "owns", "bike": "owns", "phone": "owns", "laptop": "owns", "house": "city",
    "flat": "city", "home": "city", "garden": "city", "town": "city", "area": "city",
    "name": "name", "age": "age", "budget": "budget", "diet": "diet",
}

PART_KEYS = ("job", "people", "kids", "pets", "owns", "city", "places", "name", "age",
             "budget", "diet", "allergies")

KEPT_THINGS = ("job", "people", "owns", "kids", "pets", "name", "age", "budget", "diet")

NAMED_BY = {
    "name": r"\bname\b|\bcalled\b",
    "age": r"\bold\b|\bage\b|\d",
    "job": r"\bjob\b|\bwork\b|\bliving\b|\bam i an?\b|\bwas i an?\b",
    "city": r"\bliv(?:e|es|ing)\b|\bhome\b|\bcity\b|\btown\b",
    "from": r"\bfrom\b|\bhometown\b|\bgrew up\b|\bborn\b",
    "allergies": r"\ballerg",
    "budget": r"\bbudget\b|\bspend\b|\bafford\b|\d",
    "diet": r"\bvegetarian\b|\bvegan\b|\bdiet\b|\beat\b|\bfood\b",
    "pets": r"\bdog\b|\bcat\b|\bpet\b|\bhamster\b|\brabbit\b|\bfish\b|\bbird\b|\bhorse\b",
}

RESTATED_KEYS = ("name", "age", "job", "city", "from", "diet", "budget", "allergies", "pets")

SWAPPABLE = ("city", "places", "job", "diet", "plan", "plans")

_TENS_WORDS = ("", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty",
               "ninety")

CORRECTED_AGAIN = ("{Value}, not {was} \u2014 got it.",
                   "{Value}, then \u2014 your {who} is {value} now.",
                   "Not {was} \u2014 {value}. Got it.")

CORRECTED_AGAIN_WHO = ("{Value} \u2014 got it, your {who} is {value} from now on.",
                       "{Value}, then \u2014 I have your {who} down as {value}.")

CORRECTED_WHICH_PERSON = (
    "{Value} \u2014 your {who}, not your {was_who}. Got it.",
    "Ah, it's your {who} who is {value} \u2014 I had that with your {was_who}.",
    "{Value} goes with your {who}, then, not your {was_who}. Noted.",
    "Your {who}, not your {was_who} \u2014 I've moved that over.",
)

CAT_NAMES = ("Miso", "Pepper", "Juniper", "Biscuit", "Saffron", "Marmalade", "Clover", "Smudge",
             "Willow", "Pip")

DOG_NAMES = ("Finn", "Nell", "Bramble", "Otto", "Rufus", "Tilly", "Ziggy", "Juno", "Alfie",
             "Moss")

SMALL_NAMES = ("Pip", "Peanut", "Willow", "Nibbles", "Bramble", "Squeak", "Poppy", "Titch")

NAME_ADVICE = (
    "Pick the one you would not mind calling across a park at night - that rules more names out "
    "than anything else.",
    "Say each one out loud first: a name you shorten anyway is the one you will end up using.",
    "Two syllables carries best, and use only the chosen one for the first fortnight, so it "
    "learns its own name quickly.",
    "The right answer is usually the one everybody in the house can spell and shout.",
)

RESUME = (
    "Back to {thing}, then. What did you want to know about it?",
    "OK, back to {thing}. Where were we?",
    "Right, {thing} again. Go on.",
    "Back to {thing} it is. I'm still here.",
    "Righto, {thing}. What's the question?",
    "Back to {thing}. I've still got what you told me about it.",
)

NO_PLANS_REPLY = ("You haven't told me about anything coming up yet. What's on?",
                  "Nothing so far — you haven't mentioned anything coming up. What have you got?")

WEEK = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")

TAIL_WINDOW = 40

PLURAL_PEOPLE = ("children", "people", "parents", "kids", "twins", "boys", "girls", "friends",
                 "mates", "flatmates", "housemates", "colleagues")

DIET_RULES_OUT = {
    "vegan": ("meat, fish, dairy or eggs", ""),
    "plant-based": ("meat, fish, dairy or eggs", ""),
    "plant based": ("meat, fish, dairy or eggs", ""),
    "vegetarian": ("meat or fish", ""),
    "veggie": ("meat or fish", ""),
    "veg": ("meat or fish", ""),
    "pescatarian": ("meat", " (fish is fine)"),
    "gluten-free": ("gluten", ""),
    "dairy-free": ("dairy", ""),
    "lactose-free": ("dairy", ""),
    "wheat-free": ("wheat", ""),
    "sugar-free": ("sugar", ""),
    "low-carb": ("carbohydrates", ""),
}

DENIAL_WORDS = {
    "diet": ("diet", "diets", "dieting", "eat", "eats", "eating", "food", "meal", "meals",
             "vegan", "vegetarian", "veggie", "pescatarian", "keto", "paleo"),
    "budget": ("budget", "budgets", "afford", "affording", "save", "saving", "savings", "wage",
               "wages", "salary", "income", "earn", "earns", "earning", "cash"),
    "allergy": ("intolerant", "intolerance", "react", "reaction", "epipen", "coeliac", "celiac",
                "anaphylaxis", "anaphylactic"),
    "job": ("job", "jobs", "work", "works", "working", "worked", "role", "career", "employer",
            "employed", "office", "shift", "shifts", "boss", "manager", "colleagues"),
}

DENIAL_STEMS = {"allergy": ("allerg",)}

CHILD_RELATIONS = ("son", "daughter", "child", "kid", "baby", "twin", "boy", "girl",
                   "stepson", "stepdaughter", "teenager", "lad", "lass")

GROUP_OF = {
    "children": CHILD_RELATIONS, "childs": CHILD_RELATIONS, "kids": CHILD_RELATIONS,
    "parents": ("mum", "dad", "parent", "stepmum", "stepdad"),
    "siblings": ("brother", "sister", "half-brother", "half-sister"),
    "brothers": ("brother",), "sisters": ("sister",),
    "grandparents": ("grandma", "grandad", "grandparent"),
    "grandchildren": ("grandson", "granddaughter", "grandchild"),
    "aunts": ("aunt",), "uncles": ("uncle",), "cousins": ("cousin",),
}

RELATION_ALIKE = {"mother": "mum", "mom": "mum", "mam": "mum", "mummy": "mum",
                  "father": "dad", "daddy": "dad",
                  "nana": "grandma", "nan": "grandma", "granny": "grandma",
                  "gran": "grandma",
                  "grandmother": "grandma", "grandpa": "grandad", "grandfather": "grandad",
                  "auntie": "aunt", "kid": "child", "childs": "child", "kids": "child"}

MONTH_ORDER = ("january", "february", "march", "april", "may", "june", "july", "august",
               "september", "october", "november", "december")

HAVE_ANY_WORDS = ("brothers", "sisters", "siblings", "children", "kids", "childs", "parents",
                  "grandchildren", "grandparents", "aunts", "uncles", "cousins", "family",
                  "brother", "sister", "child", "kid", "sons", "daughters", "mums", "dads",
                  "parents", "son", "daughter", "mum", "dad", "parent", "grandson",
                  "granddaughter", "aunt", "uncle", "cousin")

HER_WORD = {"sister": "her", "daughter": "her", "mum": "her", "granddaughter": "her",
            "aunt": "her", "brother": "him", "son": "him", "dad": "him",
            "grandson": "him", "uncle": "him"}

DIET_FOOD = {"vegetarian": ("meat", "fish"), "veggie": ("meat", "fish"),
             "vego": ("meat", "fish"), "pescatarian": ("meat",),
             "pescetarian": ("meat",),
             "vegan": ("meat", "fish", "dairy", "eggs"),
             "plant based": ("meat", "fish", "dairy", "eggs"),
             "plantbased": ("meat", "fish", "dairy", "eggs")}

PERSON_GROUP = {
    "children": CHILD_RELATIONS, "childs": CHILD_RELATIONS, "kids": CHILD_RELATIONS,
    "brood": CHILD_RELATIONS,
    "boys": ("son", "boy", "stepson"),
    "girls": ("daughter", "girl", "stepdaughter"),
    "parents": ("mum", "mother", "dad", "father", "stepmum", "stepdad", "parent"),
    "siblings": ("brother", "sister", "stepbrother", "stepsister"),
    "grandchildren": ("grandson", "granddaughter", "grandchild"),
    "grandkids": ("grandson", "granddaughter", "grandchild"),
    "grandparents": ("nan", "nana", "gran", "granny", "grandma", "grandad", "grandpa"),
    "twins": ("twins", "son", "daughter"),
}

PLURAL_PEOPLE = ("children", "childs", "kids", "twins", "babies")

OWNED_BY_THE_VERB = (("drive", "car"), ("ride", "bike"))

PREGNANT_SAY = (
    "Noted — your {who} is pregnant, so nothing alcoholic for her. Say if you want a hand with "
    "what to cook or what to plan.",
    "Your {who} being pregnant is worth knowing — I'll keep drink out of anything I suggest.",
)

PREGNANT_WEEKS_SAY = (
    "Noted — your {who} is {weeks} weeks pregnant, so nothing alcoholic for her. Say if you want "
    "a hand with what to cook or what to plan.",
    "Your {who} at {weeks} weeks — I'll keep drink out of anything I suggest, and say if a meal "
    "plan would help.",
)

PREGNANT_OWN_SAY = (
    "Lovely news — {weeks} weeks. Nothing alcoholic in anything I suggest, and say if you want a "
    "hand with meals or with what to plan.",
    "That's lovely news — {weeks} weeks in, and I'll keep the drink out of anything I suggest. "
    "Say the word if a meal plan would help.",
)

LIMIT_SAY = (
    "Noted, your {who} doesn't drink — I'll not put wine in the plan.",
    "Good to know your {who} isn't drinking; I'll leave it out of what I suggest.",
)

FEEDING_SAY = (
    "Noted — your {who} is breastfeeding, so I'll keep the drink out of what I suggest and keep the "
    "ideas to food.",
    "Good to know your {who} is breastfeeding; I'll leave anything with drink in it off the list.",
)

STATE_WAS_SAY = (
    "Noted - I'll take that as something that was, not something now. Tell me what you'd like a "
    "hand with and I'll pick it up from there.",
    "Thanks for telling me. I'll keep that in the past rather than reading it as news now.",
)

PET_WORDS = r"dog|puppy|cat|kitten|rabbit|hamster|parrot|goldfish|fish|horse|pet"

PRONOUN_PEOPLE = ("she", "he", "they", "him", "her", "them")

SAME_FACT_THEIR_OWN = ("allergies", "diet", "condition", "age", "job", "name", "budget", "pets",
                       "places", "plan")

CONDITION_RULES_OUT = {
    "coeliac": "gluten",
    "celiac": "gluten",
    "gluten intolerant": "gluten",
    "lactose intolerant": "dairy",
}

CONDITION_KEEPS_DOWN = {
    "diabetic": "sugar and white carbs",
    "high cholesterol": "saturated fat and fried food",
    "high blood pressure": "salt",
}

CAR_CAPS = {"bmw": "BMW", "vw": "VW", "mg": "MG", "gti": "GTI", "tdi": "TDI", "mpv": "MPV"}

NUMBER_WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight",
                9: "nine", 10: "ten"}

_SUBJECT_KEYS = {"pet": "pets", "allergy": "allergies", "budget": "budget", "job": "job",
                 "name": "name", "city": "city", "limit": "limits"}

PLURAL_PETS = {"cat": "cats", "dog": "dogs", "puppy": "puppies", "kitten": "kittens",
               "rabbit": "rabbits", "bunny": "bunnies", "hamster": "hamsters", "fish": "fish",
               "bird": "birds", "horse": "horses", "pony": "ponies", "parrot": "parrots",
               "mouse": "mice", "guinea pig": "guinea pigs", "tortoise": "tortoises"}

COUNT_WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight",
               9: "nine", 10: "ten"}

A_SHORT_ANSWER = 14

KEY_SLOT = {"name": "name", "job": "job", "city": "city", "from": "from", "diet": "diet",
            "budget": "budget", "allergy": "allergies", "allergies": "allergies", "age": "age",
            "pet": "pet", "pets": "pets", "limit": "allergies", "height": "height"}

CONCEPTS = {}

POSSESSIVE = r"(?:(?:'s|s'|s)(?!\s+(?:the|a|an)\b))?"

QUOTE_LEADS = ("You said: ", "Your own words were: ", "This is what you told me: ",
               "You put it like this: ")

ASKED_LEADS = ("You asked: ", "Your question was: ", "What you said was a question: ")

NOTHING_STARTED = (
    "We haven't really started yet — you go first.",
    "Nothing yet: there's nothing of yours to look back on. Where would you like to begin?",
    "So far it's just been hellos, so there's nothing to go back over. What's on your mind?",
    "We're still at the beginning — you haven't given me anything to hold onto yet.",
)

POINTS_BACK_NOTHING = (
    "There's nothing before this chat for that to be, so I've no 'before' to go on. What is it "
    "you want?",
    "We've only just started, so there's nothing before this to point at — say the thing itself "
    "and I'll answer it.",
    "Nothing said yet for that to be. Tell me the thing in a word or two and I'll take it from "
    "there.",
    "You haven't said the thing itself yet — what is it?",
    "‘The usual’ is what you'd say to someone who already knows. I don't yet — what is it?",
)

POINTING_WORD_NOTHING = (
    "There's nothing before this chat for that to be. What are we working on?",
    "I haven't got anything for that to point at yet — give me the thing in a few words and "
    "I'll answer for it.",
    "That's the first thing you've said, so I've nothing in hand for it to mean. What is it?",
    "Nothing said yet for that to be: tell me the thing itself in a word or two and I'll take it "
    "from there.",
)

WHAT_I_SAID_NOTHING = (
    "Nothing yet — you haven't told me anything, so there's nothing for that to be. What was on "
    "your mind?",
    "You haven't said yet, so I'd be making it up. Tell me what it was and I'll keep it.",
)

RESTRICT_OPENS = (
    "cut", "reduce", "shorten", "lower", "drop", "halve", "taper", "ease", "ease off",
    "keep it", "keep to", "keep the", "keep your", "go easy", "take it", "skip", "swap",
    "switch", "replace", "rest", "ice", "warm up", "stretch", "cut back", "fewer", "less",
    "lighter", "gentler", "shorter", "slower",
)

CALL_LEADS = (
    "Yes, but {limit}. And {condition}.",
    "Keep going, but {limit}. And {condition}.",
    "Yes — {limit}. And {condition}.",
    "Go on, but {limit}. And {condition}.",
)

LENGTH = (r"(?:half\s+an\s+hour|an\s+hour|"
          r"(?:\d+|an?|a\s+couple\s+of|a\s+few|"
          r"one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|fifteen|twenty|"
          r"thirty|forty|forty-five|fifty|sixty|ninety)\s*"
          r"(?:minutes?|mins?|hours?|hrs?))")

WORD_NUMBERS = {"a": 1, "an": 1, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
                "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11,
                "twelve": 12, "fifteen": 15, "twenty": 20, "thirty": 30, "forty": 40,
                "forty-five": 45, "fifty": 50, "sixty": 60, "ninety": 90}

UNIT_SECONDS = {"second": 1, "sec": 1, "minute": 60, "min": 60, "hour": 3600, "hr": 3600}

BUDGET_FITS = (
    "{part}. {budget} covers that.",
    "{part}. That fits inside {budget}.",
    "{part}. {budget} is enough for that.",
)

BUDGET_MORE = (
    "{part}. {budget} is more than enough for the steps of it.",
    "{part}. That is more than enough time for the steps of it, one at a time.",
    "{part}. Nothing in it needs longer than {budget}, so there is more than enough there.",
)
ANY_FIGURE = re.compile(
    r"\b(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|fifteen|twenty"
    r"|thirty|forty|fifty|sixty|ninety|hundred)\b", re.I)

BUDGET_TIGHT = (
    "{part}. That wants longer than {budget}, but it is still the answer.",
    "{part}. It takes longer than {budget}, but this is still it.",
)

HELD_THREAD = ("crisis", "suicide", "overdose", "call an ambulance", "999 now", "111 now",
               "hospital now", "call someone with you")

GRIEF_WORDS = ("died", "passed away", "funeral", "sorry for your loss", "cancer", "hospice",
               "in hospital", "grief", "miss him", "miss her", "miss them")

CLOSE_PLAIN = (
    "Fair enough — we'll leave it there. I'm here if you want to come back to it.",
    "Alright, dropped. Say the word if you pick it up again later.",
    "That's fine by me. I'm not going anywhere if you change your mind.",
)

CLOSE_HEAVY = (
    "Of course. You don't have to talk about it with me — I'm here either way.",
    "That's alright. It can wait, and so can I.",
    "Understood. Nothing more from me on it unless you bring it up.",
)

CHANGE_PLAIN = (
    "Yes. Food, films, or something to do at the weekend — pick one and I'll run with it.",
    "Sure. Give me a subject — cooking, telly, plans — and I'll take it from there.",
    "Of course. Tell me what you'd rather chew on: dinner, a film, the weekend?",
)

CHANGE_HEAVY = (
    "Yes, gladly. Anything you'd rather think about — a film, dinner, the weekend?",
    "Of course. We can leave that where it is — something light instead, like dinner or a film?",
    "Happily. Something light, then — a film, dinner, or the weekend?",
)

CHECK_NOTHING_SAID = (
    "Nothing came through before that one — say it again and I'll take it from there.",
    "I don't have a line from you before this one. Go on, and I'll pick it up.",
)

CHECK_A_FEELING = (
    "Yes — I've got it.",
    "I heard you, and I'm still here.",
    "Yes, that came through.",
)

CHECK_A_QUESTION = (
    "Yes — I've got the question.",
    "Yes, I have it — anything else on it?",
    "Got it, I have your question.",
)

CHECK_PLAIN = (
    "Yes — {said}.",
    "Got it — {said}.",
    "Yes, that's what I have: {said}.",
)

CLOCK_SAID = (r"(?:half (?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)"
              r"|quarter (?:past|to) (?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)"
              r"|(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)"
              r"(?: (?:thirty|fifteen|forty-five))?"
              r"|(?:1[0-2]|0?[1-9])(?:[:. ][0-5]\d)?\s*(?:am|pm)?"
              r"|noon|midday|midnight)")

ROUTINE_SUBJECT = r"(?:i|we|im|i'm|i am|we're|we are)"

ROUTINE_SAY_BACK = {"get up": "You're up at {at}.",
                    "go to bed": "You go to bed at {at}.",
                    "start work": "You start work at {at}.",
                    "finish work": "You finish work at {at}.",
                    "leave": "You leave at {at}.",
                    "get home": "You get home at {at}."}
