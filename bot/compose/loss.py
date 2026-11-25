import re
try:
    from ..memory import dream as _dream
except Exception:
    _dream = None

from ..understanding import normalise
from ..understanding.topics import is_a_machine_word

PEOPLE = frozenset((
    "mum", "mom", "mam", "mother", "dad", "father", "nan", "nana", "gran", "granny",
    "grandma", "grandmother", "grandad", "granddad", "grandpa", "grandfather", "grandparents",
    "parents", "son", "daughter", "child", "children", "kid", "kids", "baby", "boy", "girl",
    "brother", "sister", "wife", "husband", "partner", "friend", "friends", "mate", "mates",
    "neighbour", "neighbor", "neighbours", "neighbors", "colleague", "colleagues", "aunt",
    "auntie", "uncle", "cousin", "niece", "nephew", "family", "relative", "relatives",
    "stepdad", "stepmum", "godmother", "godfather", "in-laws", "mil", "fil",
    "parent", "sibling", "siblings", "spouse", "spouses", "boyfriend", "girlfriend",
    "boyfriends", "girlfriends", "fiance", "fiancee", "fianc\u00e9", "fianc\u00e9e", "fiances",
    "halfbrother", "halfsister", "ex",
    "stepson", "stepsons", "stepdaughter", "stepdaughters", "stepchild", "stepchildren",
    "stepbrother", "stepsister", "godson", "godsons", "goddaughter", "goddaughters",
    "godchild", "godchildren", "grandson", "grandsons", "granddaughter", "granddaughters",
    "grandchild", "grandchildren", "grandkids", "twin", "twins", "carer", "carers",
    "caregiver", "caregivers", "childminder", "guardian", "flatmate", "flatmates",
    "housemate", "housemates", "lodger",
    "dog", "dogs", "cat", "cats", "puppy", "kitten", "rabbit", "hamster", "budgie", "parrot",
    "horse", "pony", "pet", "pets", "tortoise", "ferret", "guinea",
    "fish", "fishes", "goldfish", "snake", "lizard", "gerbil",
))

CLOSE_PEOPLE = frozenset((
    "carer", "carers", "caregiver", "caregivers", "nurse", "nurses", "doctor", "doctors",
    "gp", "gps", "surgeon", "surgeons", "midwife", "midwives", "therapist", "therapists",
    "counsellor", "counsellors", "counselor", "counselors", "physio", "physiotherapist",
    "psychiatrist", "childminder", "childminders", "babysitter", "babysitters", "nanny",
    "nannies", "cleaner", "cleaners", "lodger", "lodgers", "housemate", "housemates",
    "flatmate", "flatmates", "classmate", "classmates", "schoolfriend", "tutor", "tutors",
    "teacher", "teachers", "manager", "managers", "priest", "vicar", "pastor", "rabbi",
    "imam", "barber", "hairdresser", "warden", "mentor", "worker", "workers",
))
ROLE_PHRASE = re.compile(
    r"\b(?:home\s+(?:help|carer)|care\s+assistant|foster\s+carer|support\s+staff|"
    r"(?:duty|night|live-in)\s+(?:nurse|carer))\b")
PEOPLE = PEOPLE | CLOSE_PEOPLE

THING_ROLE = re.compile(
    r"\b(?:vacuum|oven|drain|steam|carpet|dishwasher|pipe|grill|barbecue|bbq|floor|gutter|jet|"
    r"pressure|upholstery|chimney)\s+cleaners?\b|\bnanny\s+goats?\b")
TWO_WAY_ROLES = frozenset(("cleaner", "cleaners", "nanny", "nannies"))
THEIRS = frozenset((
    "badge", "badges", "card", "cards", "allowance", "funding", "letter", "letters", "note",
    "notes", "form", "forms", "paperwork", "payment", "payments", "appointment", "appointments",
    "referral", "referrals", "rota", "timesheet", "pass", "application", "number", "budget",
    "assessment", "plan", "diary", "file", "files", "folder", "prescription", "receipt",
    "invoice", "statement", "booking", "bookings", "certificate", "report", "results", "record",
    "records", "pin", "login", "password", "email", "address", "ticket", "tickets",
))

PLAIN = re.compile(
    r"\b(passed away|funeral|funerals|burial|cremation|cremated|cremate|"
    r"grief|grieving|grieve|bereaved|bereavement|widow|widowed|mourning|condolence|"
    r"condolences|eulogy|memorial service|post mortem|in memoriam)\b")

A_PRICE = re.compile(
    r"\b(?:cost|costs|costing|price|prices|pricing|cheap|cheapest|expensive|afford|affordable|"
    r"budget|pay|quote|quotes)\b|\bhow\s+much\b")
PROCEEDINGS_ASK = re.compile(r"\b(?:how|what|which|can|could|should|do|does|any|tips?|ideas?)\b")
THIS_ONE = re.compile(r"\b(?:the|this|that|our|their|his|her|its|today|tomorrow|yesterday)\s+"
                      r"(?:\w+\s+){0,2}(?:funeral|burial|cremation|wake|service|viewing)\b")
A_DEATH_HAPPENED = re.compile(
    r"\b(?:died|dying|dies|dead|death|deaths|passed\s+away|passed\s+on|gone|killed|lost|"
    r"losing|buried|bury|burying|ashes|widow|widowed|bereaved|bereavement|grief|grieving|"
    r"mourning|condolence|condolences|eulogy|sympathy|miss|missing)\b")


CORRECTS = re.compile(
    r"^\W*(?:(?:no|nope|sorry|apologies|actually|wait|hold on|oops)[\s,.!-]+)*"
    r"(?:i\s+(?:mean|meant|said)(?:\s+to\s+say)?|(?:you\s+)?mean|i\s+did\s+mean)[\s,.!-]+"
    r"(?P<rest>\S.*)$", re.I)


def _only_a_new_subject(line):
    found = CORRECTS.match((line or "").strip())
    if not found:
        return False
    rest = found.group("rest").strip(" .!?,")
    return bool(rest) and len(rest.split()) <= 3 and not DIED.search(rest)


def _only_the_proceedings(clean, words):
    if A_DEATH_HAPPENED.search(clean) or _has_person(words):
        return False
    if _unnamed_person(words, clean) or THIS_ONE.search(clean):
        return False
    if ASK_WORDS.search(clean) or CARD_WORD.search(clean):
        return False
    return bool(A_PRICE.search(clean) or PROCEEDINGS_ASK.search(clean))


WAKE = re.compile(
    r"\b(?:his|her|their|the|a|mum's|dad's|nan's|grandad's|gran's)\s+wake(?!\s*(?:up|me|him|"
    r"her|them|you|us|at|before|earlier|by|and|of)\b)\b")

BURIED = re.compile(r"\bburied\b")
BURIED_OBJECT = ("a", "an", "the", "some", "old", "new", "these", "those", "his", "her", "my",
                 "our", "their", "your")
BURIED_ADJECTIVE = ("old", "poor", "little", "beloved", "dear", "sweet", "big", "lovely", "late",
                    "much", "loved", "own", "first", "precious", "wee", "new")

DEATH_NOUN = re.compile(
    r"\b(?:a|the|this|that|his|her|their|your|my|our)\s+deaths?\b|"
    r"\b[a-z]+(?:'s|s'|s)\s+deaths?\b|"
    r"\b(?:two|three|several)\s+deaths\b")
OWN_DEATH = re.compile(
    r"\b(?:my|his|her|their|your|our)\s+(?:[a-z]+(?:'s|s'|s)\s+)?deaths?\b|"
    r"\b([a-z]+)(?:'s|s'|s)\s+deaths?\b")
DEATH_CUE = re.compile(
    r"\b(?:guilty|cope|coping|cant stop|get over|getting over|anniversary|funeral|grief|"
    r"grieving|sudden|suddenly|wasnt there|wasn't there|angry|sad|numb|miss|misses|missed|"
    r"cry|crying|cried|wake|ashes|burial|memorial|condolence|mourning|hit me|hit him|hit her|"
    r"in the family|on the news|normal to feel|keep thinking|cant sleep|to terms|how do i|"
    r"what do i say|still)\b")
DEATH_COMPOUND = re.compile(
    r"\bdeath\s+(?!(?:of|was|is|in|at|on|has|had|came|come|hit|hits|left|changed|anniversary|"
    r"day|days|month|months|year|years|certificate|notice|and|or|itself|row|toll|threat|"
    r"bed|i|we|he|she|they|you|my|our|his|her|their|me|us|them|really|just|still|so|but|if|"
    r"when|while|after|before|because|that|this|everything|nothing)\b)[a-z]+")
FICTION = re.compile(
    r"\b(?:film|films|movie|movies|book|books|novel|play|episode|series|documentary|"
    r"characters?|scene|plot|chapter|show|netflix|tv|actor|actress|game|anime|comic|season|"
    r"trailer|storyline)\b")
OWN_WORRY = re.compile(
    r"\b(?:my|your|our)\s+(?:own\s+)?death\b|\bdeath anxiety\b|\bfear of death\b|"
    r"\b(?:scared|afraid) of death\b|\bdeath itself\b|\bthink(?:ing)? about death\b|"
    r"\b(?:what|when)\s+(?:is|comes after|happens after)\s+death\b|\bis death\b")
THINGS = frozenset((
    "laptop", "laptops", "phone", "phones", "car", "cars", "battery", "batteries", "boiler",
    "fridge", "freezer", "telly", "tv", "printer", "houseplant", "houseplants", "plant", "plants",
    "tree", "trees", "lawn", "garden", "business", "career", "job", "pub", "shop", "club",
    "brand", "game", "team", "band", "party", "project", "dream", "holiday", "marriage",
    "engine", "phone", "internet", "radio", "cinema", "print", "high",
))
PET_DEATH = re.compile(
    r"\b(?:cat|cats|dog|dogs|puppy|puppies|kitten|kittens|rabbit|rabbits|hamster|hamsters|"
    r"budgie|budgies|parrot|parrots|horse|horses|pony|ponies|guinea|goldfish|fish|pet|pets)"
    r"(?:'s|s'|s)?\s+deaths?\b")
THING_DEATH = re.compile(
    r"\b(?:" + "|".join(sorted(THINGS)) + r")(?:'s|s'|s)?\s+deaths?\b")
DEATH_OF_OWNER = re.compile(
    r"\bdeaths?\s+of\s+(?:the|my|our|a|an|his|her|their|your)\s+((?:[a-z]+\s+){0,2}[a-z]+)\b")

DIED = re.compile(r"\b(died|dying|dead|dies)\b")
DYING = re.compile(r"\b(died|dies)\b")
PUT_DOWN = re.compile(
    r"\bput\s+(?:her|him|it|(?:my|our|the)\s+\w+)\s+(?:down|to sleep)\b|"
    r"\bputting\s+(?:her|him|it|(?:my|our|the)\s+\w+)\s+(?:down|to sleep)\b|"
    r"\bput\s+(?:down|to sleep)\b|"
    r"\bhad\s+(?:\w+\s+){0,3}?put\s+(?:down|to sleep)\b|"
    r"\b(?:was|were|been)\s+put\s+(?:down|to sleep)\b")
PET_WORDS = frozenset((
    "dog", "dogs", "cat", "cats", "puppy", "puppies", "kitten", "kittens", "rabbit", "hamster",
    "budgie", "parrot", "horse", "pony", "pet", "pets", "tortoise", "ferret", "guinea", "hen",
    "chicken", "rat", "mouse", "gerbil", "lurcher", "greyhound", "collie", "labrador",
    "fish", "fishes", "goldfish", "snake", "lizard",
))
PEOPLE_PHRASES = (("other", "half"), ("other", "halves"), ("support", "worker"),
                  ("support", "workers"), ("care", "worker"), ("care", "workers"),
                  ("significant", "other"), ("home", "carer"), ("home", "carers"))


HUMAN_WORDS = PEOPLE - PET_WORDS
DEATHABLE = PEOPLE | PET_WORDS
MACHINE_ANIMALS = frozenset(("mouse", "mice"))
MISADVENTURE = re.compile(
    r"\b(?:was|were|is|are|got|been|being|had been)\s+(?:run\s+over|knocked\s+(?:down|over)|"
    r"drowned)\b|"
    r"\b(?:run|knocked)\s+(?:over|down)\s+by\s+(?:a|the|an)?\s*\w+|"
    r"\bdrowned\b|"
    r"\b(?:was|were|got|been)\s+electrocuted\b(?=[^.?!]{0,45}\b(?:died|dead|killed|"
    r"didn'?t\s+make\s+it|did\s+not\s+make\s+it|passed\s+(?:away|on)|funeral|buried|"
    r"pronounced)\b)|"
    r"\bdied\s+(?:in|after)\s+(?:a\s+|the\s+)?(?:accident|crash|fire|fit|seizure)\b")
SURVIVED = re.compile(
    r"\bsurvived\b|\bstill alive\b|\b(?:is|was|seems|doing)\s+(?:ok|okay|alright|fine)\b|"
    r"\bbut\s+(?:he|she|they|it|we|i)(?:'s|s| is| was)?\s+(?:ok|okay|alright|fine|alive)\b|"
    r"\bin (?:the )?hospital\b|\brecovering\b|\bstable\b|\bjust bruises\b|"
    r"\bbroke (?:his|her|their|a|my)\b|\bstitches\b|"
    r"\bwalked\s+(?:away|off)\b|\bno\s+harm\b|\bunhurt\b|\bnot\s+(?:a\s+)?scratch\b|"
    r"\bnot\s+(?:hurt|injured|serious)\b|\bno\s+(?:injuries|injury|damage)\b")
LOSS_CONTEXT = ("had to", "have to", "put to sleep", "vet", "euthanis", "last week", "last night",
                "yesterday", "we had", "i had", "it was time")

OWNED = re.compile(r"\b(?:my|our|his|her|their)\s+((?:\w+\s+){0,2}\w+)")
VERB_OBJECT = re.compile(
    r"\b(?:drowned|run\s+over|knocked\s+(?:down|over))\s+(?:her|his|my|our|their|its?|the|a|an)\b")
KNOCKED_BY = re.compile(r"\b(?:run\s+over|knocked\s+(?:down|over))\s+by\s+(?:a|the|an)\b")
DEATH_SAID = re.compile(
    r"\b(?:died|dead|killed|didn'?t\s+make\s+it|did\s+not\s+make\s+it|lost|passing|passed|"
    r"gone|funeral|put\s+to\s+sleep|euthanis\w*)\b")

LOST = re.compile(r"\b(lost|we lost|i lost|he lost|she lost|they lost)\s+"
                  r"(?:my|our|his|her|their)\s+([a-z]+)")
LOST_BARE = re.compile(r"\b(?:i|we|he|she|they)\s+lost\s+"
                       r"(?!(?:my|our|his|her|their|the|it|a|an|that|this|him|them)\b)([a-z]+)\b")
LOSE_A_PERSON = re.compile(
    r"\b(?:lose|loses)\s+(?:(?:my|our|his|her|their|the|a|an|this|that)\s+)?([a-z]+)")
LOST_FORMS = ((LOST, 2), (LOST_BARE, 1), (LOSE_A_PERSON, 1))
LOSS_OF = re.compile(r"\b(?:the\s+|a\s+|any\s+)?loss\s+of\s+(?:my|our|his|her|their)\s+([a-z]+)")
LOSING = re.compile(r"\blosing\s+(?:my|our|his|her|their|a|an|the)\s+([a-z]+)")
CLOSE = frozenset((
    "mum", "mom", "mam", "mother", "dad", "father", "nan", "nana", "gran", "granny",
    "grandma", "grandmother", "grandad", "granddad", "grandpa", "grandfather",
    "son", "daughter", "child", "baby", "brother", "sister", "wife", "husband", "partner",
    "stepdad", "stepmum", "aunt", "uncle", "cousin", "niece", "nephew", "parents",
))
NEWS_OF = re.compile(
    r"\b(?:news|thought)\s+of\s+(?:my|our|his|her|their)\s+([a-z]+)[^.]{0,24}?"
    r"\b(?:hit|hits|hurt|hurts|broke|breaks|is\s+hard|was\s+hard)\b")
LOSS_GRIEF_CUE = re.compile(
    r"\b(?:since|after|still|every|cant|couldnt|miss|missed|cry|crying|cried|grief|grieving|"
    r"funeral|bereave\w*|yesterday|anniversary|"
    r"last\s+(?:year|month|week|night|christmas|summer|winter)|"
    r"(?:in|at|on)\s+(?:january|february|march|april|may|june|july|august|september|october|"
    r"november|december|christmas|christmas\s+eve|boxing\s+day|easter|new\s+year))\b")
LOST_IN_A_PLACE = re.compile(
    r"\b(?:in|at|on|into|inside|outside|near|round|around)\s+(?:the\s+|a\s+|an\s+)?([a-z]+)")
PLACES = frozenset("""
supermarket shop shops store town city park parks playground beach seafront street streets
road motorway station airport bus train tube metro queue market mall museum gallery zoo fair
festival concert woods forest hill hills garden gardens pool lido crowd crowds field fields
arcade campsite caravan centre center precinct pier promenade high street roundabout bus stop
coach tram ferry harbour harbor dock docks
""".split())
UNNAMED = frozenset(("someone", "somebody", "anyone", "everyone", "people", "person"))
MEDIA = frozenset(("show", "shows", "film", "films", "movie", "movies", "series", "episode",
                   "episodes", "game", "games", "book", "books", "soap", "documentary", "telly",
                   "tv"))

LOST_SELF = frozenset(("appetite", "sleep", "confidence", "interest", "motivation", "energy",
                       "joy", "focus", "weight", "voice", "self", "myself", "herself",
                       "himself", "themselves"))
PREY = re.compile(r"\b(?:a\s+|the\s+|another\s+)?(?:dead|dying|half\s+dead)\s+"
                  r"(?:bird|birds|mouse|mice|rat|rats|vole|voles|rabbit|rabbits|squirrel|"
                  r"squirrels|pigeon|pigeons|frog|frogs|hedgehog|hedgehogs|sparrow|sparrows|"
                  r"blackbird|blackbirds|chick|chicks|goldfish|fish)\b")
HUNTING = re.compile(r"\b(bring|brings|bringing|brought|drag|drags|dragging|dragged|catch|"
                     r"catches|catching|caught|kill|kills|killed|killing|left|leaves|leaving|"
                     r"found|finds|dropping|dropped|deposit|deposits|present|presents)\b")
LOST_THE = re.compile(r"\b(?:we|i|he|she|they)\s+lost\s+the\s+([a-z]+)\b")
LOST_THE_FOUND = re.compile(
    r"\b(?:found|got)\s+(?:him|her|them)\b|\b(?:in|at|near|outside|inside|by)\s+the\s+"
    r"(?:shop|shops|park|supermarket|street|station|queue|mall|woods|beach|playground|"
    r"car\s*park|bus|train|airport|market)\b")
STILL_CRY = re.compile(r"\b(?:still|always|every|keep|keeps)\b[^.]{0,24}\b(?:cry|crying|cries|"
                       r"tears|gutted)\b")
OTHER_WEEPS = re.compile(
    r"\b(?:my|our|his|her|their|the)\s+(?:[a-z']+\s+){0,2}"
    r"(?:keeps?|kept|is|are|was|were|has|have|had|still|always|constantly|every|starts?|started|"
    r"won'?t|wont)\b"
    r"(?:(?!\b(?:i|we)\b)[^.]){0,40}\b(?:cry|crying|cries|tears|sob\w*)\b", re.I)
THEIR_TEARS_IN_A_CLAUSE = re.compile(
    r"\b(?:and|so|but|then)\s+(?:he|she|they|it|the\s+[a-z]+)\b[^.]{0,24}"
    r"\b(?:cry|cries|cried|crying|sob\w*|weeps?|weeping|tears)\b", re.I)
DEATH_AS_A_THING = re.compile(r"\b(?:a|any|the)\s+death\b|\b[a-z]+'?s\s+death\b|"
                              r"\b(?:his|her|their|your|my|our)\s+death\b")
NOT_A_DEATH = re.compile(
    r"\bdeath\s+(?:penalty|row|metal|stare|trap|wish|cab|valley|rate|rates|bed|note|star|toll|"
    r"scene|threat|match|laptop|phone|duty|tax|benefit|certificate|notice|inquest|camp)\b|"
    r"\bto\s+death\b|\bdeath of (?:me|him|her|us|them|a\s+salesman)\b|\bblack death\b|"
    r"\bsudden death\b|\bdeath in (?:paradise|venice)\b|"
    r"\b(?:death|deaths)\s+(?:per|rate|rates|toll|count|figures)\b|"
    r"\bdeath of (?:the|my|our|a)\s+(?:[a-z]+\s+){0,2}?(?:high street|cinema|print|telly|tv|"
    r"radio|music|pub|shop|business|club|scene|brand|houseplant|plant|tree|lawn|car)\b")
TOOK = re.compile(r"\b(took|taken|take)\s+(?:his|her|their)\s+own life\b")
KILLED = re.compile(r"\b(?:was|were|got|been|being|is|are|had been)\s+killed\b"
                    r"|\bkilled\s+(?:in|by)\b")
KILLED_IN = re.compile(r"\bkilled\s+(?:in|on|during|at)\b")

STORY_MEDIUM = frozenset("""film films movie movies book books novel novels play episode
    episodes series documentary scene chapter show netflix tv game games anime comic comics
    season trailer storyline soap cartoon quiz""".split())
STORY_INCIDENT = frozenset("""crash accident road motorway car bike motorbike lorry truck bus
    train plane bomb blast explosion shooting shot stabbing stabbing attack fire house
    hospital childbirth home work""".split())
GAME_TITLES = re.compile(
    r"\b(?:call\s+of\s+duty|fortnite|minecraft|roblox|fifa|halo|overwatch|zelda|mario|"
    r"pokemon|among\s+us|gta|grand\s+theft\s+auto|world\s+of\s+warcraft|league\s+of\s+"
    r"legends|apex\s+legends|counter\s+strike|pubg|rocket\s+league|skyrim|tetris|"
    r"pac\s*man|street\s+fighter|mortal\s+kombat)\b")


def _killed_in_a_story(clean):
    if GAME_TITLES.search(clean):
        return True
    found = KILLED_IN.search(clean)
    if not found:
        return False
    for word in clean[found.end():].split()[:4]:
        if word in STORY_INCIDENT:
            return False
        if word in STORY_MEDIUM:
            return True
    return False


WOULD_HAVE_BEEN = re.compile(r"\bwould(?:'ve| have)\s+been\s+(?:\d{1,3}|(?:her|his|their)\s+"
                             r"\d{1,3})\b")

PASSED_ON = "passed on"
PASSED_ON_SUBJECT = frozenset(("he", "she", "they", "him", "her", "them"))
PASSED_ON_OBJECT = frozenset((
    "the", "a", "an", "my", "your", "his", "her", "their", "our", "this", "that",
    "these", "those", "it", "them", "some", "any", "all", "another", "one", "to",
))
MONTHS = frozenset((
    "january", "february", "march", "april", "may", "june", "july", "august",
    "september", "october", "november", "december",
))

PASSED_ALONE = "passed"
PASSED_ALONE_TAIL = frozenset(("away", "on", "out", "by", "over", "up", "back"))
PASSED_ALONE_HANDED = frozenset(("me", "him", "her", "us", "them", "it", "you"))
PASSED_ALONE_NOUN = frozenset((
    "gas", "wind", "water", "blood", "comment", "comments", "remark", "remarks",
    "judgement", "judgment", "sentence", "motion", "muster", "note", "notes", "word",
    "words", "message", "messages", "memo", "review", "stone", "stones", "ball", "balloon",
    "duty", "laws", "law", "bill", "act", "exam", "exams", "test", "tests",
))
PASSED_A_RESULT = frozenset((
    "results", "result", "exam", "exams", "test", "tests", "interview", "course", "grade",
    "grades", "marks", "finals", "mocks", "driving", "theory", "gcse", "gcses", "alevels",
    "a-levels", "degree", "dissertation", "viva", "audition", "assessment", "inspection",
    "mot", "physical", "boards", "revision", "resit",
))

PASSED_DATE = frozenset((
    "jan", "january", "feb", "february", "mar", "march", "apr", "april", "may", "jun", "june",
    "jul", "july", "aug", "august", "sep", "sept", "september", "oct", "october", "nov",
    "november", "dec", "december", "christmas", "easter", "spring", "summer", "autumn",
    "winter", "the",
))
PASSED_TIME = frozenset((
    "morning", "afternoon", "evening", "night", "week", "weekend", "month", "year", "monday",
    "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
))

OBJECTS = frozenset((
    "phone", "phones", "battery", "car", "engine", "laptop", "computer", "pc", "tv", "telly",
    "boiler", "wifi", "router", "tablet", "console", "watch", "camera", "mower", "lawnmower",
    "plant", "plants", "tree", "tree", "hedge", "weed", "weeds", "flower", "flowers", "fire",
    "signal", "connection", "internet", "broadband", "radio", "speaker", "speakers", "bulb",
    "fuse", "printer", "headphones", "earphones", "remote", "kettle", "toaster", "washer",
    "dishwasher", "fridge", "freezer", "oven", "hoover", "vacuum", "scooter", "bike", "van",
))

BEDTIME = ("at night", "through the night", "all night", "every night", "bedtime", "bed time",
           "sleep through", "sleeps through", "sleeping through", "nap")

DEAD_IDIOM = frozenset((
    "against", "tired", "easy", "end", "ends", "battery", "silent", "pan", "weight", "set",
    "right", "on", "last", "by", "to", "heat", "centre", "center", "line", "bolt", "cert",
    "beat", "loss", "lift", "straight", "funny", "wrong", "certain", "serious", "stop",
    "cheap", "ahead", "slow", "cheerful", "glad", "lucky", "proud", "good", "bad", "keen",
    "jealous", "happy", "sure", "tricky", "hard", "quiet", "boring", "rude", "funny",
))
DEAD_PREDICATE = frozenset("""
a an the this that these those my your his her its our their
and or but so if because when while after before since until till
in on at by for to from with without about of into onto over under
is was are were be been being am
now today already still yet again too also just only even ever never always here there
every any some no not nothing nobody none all both each other else
""".split())


def _dead_is_not_a_death(words, index):
    if index + 1 >= len(words):
        return False
    following = words[index + 1]
    return following in DEAD_IDIOM or following not in DEAD_PREDICATE


GOING_TO_DIE = re.compile(
    r"\b(?:going\s+to|gonna|about\s+to|soon\s+to|will|won'?t|wont|isn'?t\s+going\s+to)\s+"
    r"(?:die\b(?!\s+(?:laughing|of\s+(?:laughter|boredom|embarrassment|shame|excitement)))|"
    r"pass\s+away|make\s+it\b(?!\s+(?:to\s+the|in\s+time|home))|be\s+put\s+(?:down|to\s+sleep))")
CONDITIONAL_TAIL = re.compile(
    r"\b(?:going\s+to|gonna|about\s+to|will|wont|won'?t|shall)\b[^.?!]{0,30}?"
    r"\b(?:die|dies|be\s+put\s+(?:down|to\s+sleep))\b[^.?!]{0,40}?"
    r"\b(?:if|unless|when|before|otherwise|or\s+else|without)\b")

LAUGHING = ("died laughing", "die laughing", "dying to", "died of embarrassment",
            "die of embarrassment", "nearly died", "almost died", "i could have died",
            "would die", "died down", "die down", "legs are dead", "arm is dead",
            "legs were dead", "arms are dead", "feet are dead", "hands are dead",
            "is dead to me", "drop dead gorgeous", "dead on my feet", "dead on time")

A_RELATION_IN_A_HARD_TIME = re.compile(
    r"\bmy\s+(?:mum|mom|mam|mother|dad|father|nan|nana|gran|granny|grandma|grandad|"
    r"granddad|grandpa|sister|brother|son|daughter|wife|husband|partner|friend|mate|neighbour|"
    r"neighbor|aunt|auntie|uncle|cousin|niece|nephew|parents|family)\b"
    r"[^.?!]{0,40}?\b(?:is|are|seems?|has\s+been|have\s+been|keeps?\s+(?:being|getting)|"
    r"gets?|got)\b[^.?!]{0,25}?"
    r"\b(?:lonely|alone|on\s+(?:his|her|their)\s+own|by\s+(?:him|her|them)self|withdrawn|"
    r"not\s+(?:him|her|them)self|low|down|miserable|unhappy|quiet|stuck\s+at\s+home)\b",
    re.IGNORECASE)

THEIR_HARD_TIME_REPLIES = (
    "That's a heavy thing for them to carry, and it lands on you too. What helps is a standing "
    "date they can count on - the same walk or the same coffee each week - rather than \"let me "
    "know if you need anything\". What do they like doing most?",
    "The quiet after a death is what does the damage, so keep the invitation concrete and keep "
    "making it: \"Tuesday, I'll pick you up at ten\" lands where \"I'm here if you need me\" "
    "does not. Are they eating and sleeping all right?",
    "Ring rather than text, at the same time each week, and keep asking after a no - that is "
    "what stops somebody going days without hearing a voice. Is there anyone else close by, or "
    "are you it?",
)

SOMEONE_ELSES = re.compile(
    r"\b(?:my|our|a|an|the|one of my)\s+(?:friend|friends|mate|mates|colleague|colleagues|"
    r"neighbour|neighbors|"
    r"neighbours|neighbor|boss|landlord|girlfriend|boyfriend|ex|coworker|workmate)"
    r"(?:'s|s)?\s+(?:(?:of mine|of ours)\s+)?(?:whose\s+|with\s+|who\s+has\s+)?"
    r"(?:\w+\s+){0,2}?"
    r"(?:mum|mom|mother|dad|father|son|daughter|wife|husband|partner|nan|gran|grandma|"
    r"grandad|grandpa|brother|sister|aunt|uncle|cousin|child|baby|family)\b")
HIS_HERS = re.compile(
    r"\b(?:his|her|their)\s+(?:mum|mom|mother|dad|father|son|daughter|wife|husband|partner|"
    r"nan|gran|grandma|grandad|grandpa|brother|sister|aunt|uncle|cousin|child|baby|dog|cat|"
    r"funeral|wake|memorial|service|viewing|burial)\b")

SOMEONE_ELSES_OWN = re.compile(
    r"\b(?:my|our)\s+[a-z]+(?:'s|s'|s)\s+(?:[a-z]+\s+){0,2}?(?P<who>"
    + "|".join(sorted(PEOPLE)) + r")\b")

A_STRANGERS_ANIMAL = re.compile(
    r"\b(?:the|a|an|this|that)\s+(?:[a-z]+\s+){0,2}?(?:"
    + "|".join(sorted(PET_WORDS)) + r")s?\s+(?:[a-z]+\s+){0,4}?\b"
    r"(?:next door|over (?:the )?road|upstairs|downstairs|"
    r"in (?:our|the|my) (?:street|road|close|lane|block|crescent|estate))\b")

CARD = re.compile(r"\b(card|cards|condolence|sympathy|note|letter|message|text|msg)\b")
EULOGY_WORD = re.compile(r"\b(eulogy|eulogies)\b")
EULOGY_ASK = re.compile(
    r"\b(write|writing|wrote|help|helped|how|draft|start|starting|opening|open|begin|example|"
    r"examples|template|structure|length|long|short|words|word|minutes|include|say|saying|"
    r"nervous|stuck)\b")


CARD_TO_WRITE = re.compile(r"\b(card|cards|condolence|condolences|sympathy|note)\b")
WRITE_WORD = re.compile(
    r"\b(write|writing|wrote|put|say|saying|sign|signing|send|sending|word|words|something|"
    r"anything|line|lines)\b")
WEAR = re.compile(r"\b(?:what|which)\s+(?:do|should|can|could)\s+i\s+(?:wear|put on)\b|"
                  r"\bwhat\s+to\s+wear\b|\bdress\s+code\b")
ASK_WORDS = re.compile(
    r"\b(what do i (?:say|write|put|tell)|what to (?:say|write|put)|what should i (?:say|write|"
    r"put|tell)|what can i say|how do i (?:say|comfort|help|write|tell)|how to (?:comfort|"
    r"write|word)|any ideas for what to say|words for|what do you say)\b")
QUESTION = re.compile(
    r"\b(is it normal|is that normal|why do i|why am i|how long (?:does|will|do)|does it "
    r"(?:get|ever)|will it (?:get|ever)|cant sleep|can't sleep|keep (?:crying|waking)|"
    r"still (?:cry|crying|hurts|gutted|struggling)|when does it)\b")

GRIEF_ASK_FORM = re.compile(
    r"\b(is it normal|is that normal|why do i|why am i|how long (?:does|will|do)|does it "
    r"(?:get|ever)|will it (?:get|ever)|when does it)\b")
PRACTICAL = re.compile(
    r"\b(cost|costs|price|prices|pricing|cheap|cheapest|expensive|afford\w*|"
    r"pay|pays|paid|paying|payment|payments|cover|covers|covered|"
    r"how much (?:is|are|was|were|does|do|will|did)|"
    r"probate|paperwork|document\w*|register|registered|registering|certificate|death certificate|"
    r"wills|estate|insurance|solicitor|lawyer|undertaker|funeral director|coffin|crematorium|"
    r"cook|cooking|cooks|food|sandwiches|buffet|catering|caterer|drinks|flowers|order|book|booking|"
    r"berea\w+ leave|time off|back to work|allowance|benefit|benefits|grant|quotes?|forms?)\b")
GRIEF_CUE = re.compile(
    r"\b(feel|feels|feeling|feelings|cope|coping|sleep|sleeping|crying|cry|normal|miss|missing|"
    r"heartbroken|numb|empty|guilt|guilty|angry|lonely)\b")

SOMEONE_DYING = (
    "I'm sorry you are facing this. The waiting is the hardest part of it: ask the doctors what to "
    "expect and what will keep them comfortable, say what you would regret not saying, and let "
    "people help you - this is not a thing to carry on your own.",
    "I'm sorry. Being there is most of it: sit with them, keep the room calm, and let them talk "
    "about it or not. Ask about the pain relief and who you ring at night, so you know what to do "
    "when the time comes.",
    "I'm sorry. Spend the time on what they want rather than on what you think you should be "
    "doing. Tell the people around you what is happening - you will need them, and most of them "
    "will want to help.",
    "I'm sorry. Ask the doctor to explain what the next few weeks look like, in plain words, and "
    "write it down - it is hard to hold in your head. Then let the rest go and be with them.",
)


THE_DAYS_BEFORE = (
    "I'm sorry the time is coming. Make the days they have left good ones: their favourite food "
    "and company, their usual routine as far as they can still enjoy it. Ask the vet what will "
    "keep them comfortable and what the last day will be like - knowing that is what makes it "
    "bearable.",
    "I'm sorry. The waiting is the hard part now: ask the vet to walk you through the day itself "
    "before it comes, so nothing about it is a surprise, and spend the time you have with them.",
    "I'm sorry you are facing this. Say the things you want to say while they can still hear them, "
    "spoil them a little, and be there at the end if you can bear it - most people are glad they "
    "were. Tell the vet now that you want to be there, so nobody has to ask you on the day.",
    "I'm sorry. You are doing the last kind thing for them, and a day too early is kinder than a "
    "day too late. Keep them comfortable and close, and tell the vet you want each step explained "
    "before it happens.",
)

FIRST_DAYS_PERSON = (
    "Nothing has to be sorted today. When you are ready it is the register office first - within "
    "five days in England and Wales - and then the funeral director, who takes it from there and "
    "tells you what to bring. Ask someone to sit with you for the forms.",
    "The practical list is shorter than it looks: the doctor or coroner gives you the medical "
    "certificate, you register the death at the local register office, and the funeral director "
    "handles what comes next. Tell Us Once covers the tax office, the council and benefits in one "
    "go. Everything else can wait.",
    "Take it in the order it comes. Register the death - five days, in England and Wales - and the "
    "register office gives you the certificates for the bank and the insurers and a Tell Us Once "
    "code. The rest of it, the house and the belongings and the letters, none of that is this "
    "week's job.",
)

FIRST_DAYS_PET = (
    "Nothing has to be decided today. Ring the vet when you can face it and they will explain "
    "cremation or a home burial, and what you can keep - a paw print, a lock of fur. The rest of "
    "the day can just be quiet.",
    "The vet does the practical part, so the one thing to think about is what you would like done "
    "with their body, and whether you want them back home afterwards. Everything else can wait, "
    "and asking for a paw print or a clipping of fur is worth doing if you might want it.",
    "There is no rush to decide anything. The vet will talk you through the choices when you ring "
    "them, and they are used to being asked to wait while you think. Take the day slowly - people "
    "often find the first one is the hardest.",
)

AT_THE_END = re.compile(
    r"\bat\s+the\s+end\b"
    r"(?=\s*(?:[,.!?;]|$)|\s+of\s+(?:his|her|its|their)\s+(?:life|days|time))"
    r"|\bon\s+(?:his|her|its|their)\s+last\s+legs\b"
    r"|\bfading\s+(?:away|fast|now)\b"
    r"|\b(?:is|are|seems?|looks?)\s+fading\b(?=\s*(?:[,.!?;]|$))"
    r"|\bnothing\s+more\s+(?:they|we|the\s+vet|the\s+doctors?|anyone)\s+can\s+do\s+"
    r"for\s+(?:me|us|him|her|them|my|our|his|their)\b"
    r"|\b(?:vets?|doctors?|consultants?|specialists?|oncologists?|surgeons?|hospital|hospice|"
    r"nurses?)\b[^.?!]{0,30}\bnothing\s+more\b(?=\s*(?:[,.!?;]|$))")

DYING_NOW = re.compile(
    r"\b(?:is|are|am|was|were|isn'?t|aren'?t|isnt|arent)\s+(?:\w+\s+)?dying\b"
    r"(?!\s+(?:to|for|my|her|his|their|your|our|the|a|an)\b)"
    r"|\bdying\s+of\s+(?:cancer|the\s+cancer|dementia|alzheimers|alzheimer'?s|"
    r"motor\s+neurone|mnd|huntingtons?|parkinsons?|copd|heart\s+failure|kidney\s+failure|"
    r"liver\s+failure|aids|leukaemia|leukemia|a\s+brain\s+tumour|a\s+tumour|covid)\b"
    r"|\b(?:(?:is|are|was|were)\s+(?:now\s+)?terminal|terminally\s+ill|"
    r"end\s+of\s+life|palliative|"
    r"weeks\s+to\s+live|months\s+to\s+live|days\s+to\s+live|"
    r"(?:is|are|was|were)\s+(?:now\s+)?(?:in|at)\s+(?:a\s+)?hospice|"
    r"on\s+(?:her|his|their)\s+way\s+out)\b")
ANTICIPATED = re.compile(
    r"\b(?:palliative|terminally\s+ill|(?:is|are|was|were)\s+terminal|end\s+of\s+life|"
    r"weeks\s+to\s+live|"
    r"months\s+to\s+live|days\s+to\s+live|"
    r"(?:is|are|was|were)\s+(?:now\s+)?(?:in|at)\s+(?:a\s+)?hospice)\b")
DYING_ALREADY = re.compile(
    r"\b(?:died|has\s+died|had\s+died|passed\s+away|was\s+buried|the\s+funeral|"
    r"the\s+death\b|my\s+late\b)\b")


def is_dying_now(text):
    said = text if isinstance(text, str) else " ".join(words_of(text))
    said = _spoken(said)
    clean = _tight(said)
    words = words_of(said)
    if not (DYING_NOW.search(clean) or _the_end_is_near(clean, words)
            or AT_THE_END.search(clean)):
        return False
    if DYING_ALREADY.search(clean):
        return False
    if _WORKING_WITH_THE_DYING.search(clean) and not _SAID_DYING.search(clean):
        return False
    if _the_end_is_near(clean, words) and not DYING_NOW.search(clean):
        return True
    if _the_family_is_told(clean):
        return True
    return (bool(set(words) & (HUMAN_WORDS | PET_WORDS | _PEOPLE_PRONOUNS))
            or _a_role_phrase(clean))


_WORKING_WITH_THE_DYING = re.compile(
    r"\b(?:works?|worked|working|volunteers?|volunteering)\s+(?:in|at|for|with)\b"
    r"|\b(?:is|are|was|were|am)\s+(?:a\s+|an\s+|the\s+|my\s+|our\s+)?"
    r"(?:\w+\s+){0,2}?(?:nurse|nurses|doctor|doctors|gp|carer|carers|consultant|registrar|"
    r"paramedic|paramedics)s?\b")
_SAID_DYING = re.compile(r"\bdying\b")


def dying_in_the_chat(memory, turns=6):
    history = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(history, list):
        return False
    for said in history[-turns:]:
        text = said.get("user") if isinstance(said, dict) else None
        if isinstance(text, str) and is_dying_now(text):
            return True
    return False


def _a_pet_of_ours(line, words=None):
    if words is None:
        words = words_of(line)
    said = set(words)
    return bool(said & PET_WORDS) and not bool(said & HUMAN_WORDS)


def _the_end_is_near(tight, words=None):
    if words is None:
        words = words_of(tight)
    who = bool(CARE_WHO.search(tight))
    if who and (NOTHING_MORE_TO_DO.search(tight) or TREATMENT_STOPPED.search(tight)
                or (NOT_WORKING.search(tight) and SERIOUS_CARE.search(tight))):
        if not NOTHING_MORE_TO_DO.search(tight) or _the_give_up_is_about_somebody(tight, words):
            return True
    if _the_give_up_without_a_care_word(tight, who):
        return True
    if MEDICATION_STOPPED.search(tight) and SERIOUS_CARE.search(tight):
        return True
    if says_the_last_drug(tight):
        return True
    somebody = (_has_person(words) or _has_pet(words) or "she" in words or "he" in words
                or bool(HUMAN_WORDS & set(words)))
    if FINAL_DAYS.search(tight):
        return True
    if not somebody and not who:
        return _the_family_is_told(tight)
    if DAYS_LEFT.search(tight) and not NOT_THE_END.search(tight):
        return True
    if COULD_BE_DAYS.search(tight) and not NOT_THE_END.search(tight):
        return (not DAYS_WAIT_FOR.search(tight)
                and (who or _has_person(words) or _has_pet(words)))
    if LAST_STAGES.search(tight):
        return True
    if NOT_GETTING_BETTER.search(tight):
        return True
    if GIVEN_UP_ON.search(tight) and who:
        return True
    if PREPARE.search(tight) and who and not PREPARE_OTHERWISE.search(tight):
        return True
    if OFF_LIFE_SUPPORT.search(tight) and not OFF_SUPPORT_WELL.search(tight):
        return True
    if HOSPICE_CARE.search(tight) and not HOSPICE_JOB.search(tight):
        return True
    if (PALLIATIVE_ITSELF.search(tight) and not asks_anything(tight)
            and not _WORKING_WITH_THE_DYING.search(tight)):
        return True
    return False


def _the_family_is_told(tight):
    serious = bool(SERIOUS_CARE.search(tight))
    if serious and (NOT_WORKING.search(tight) or PREPARE.search(tight)):
        return not PREPARE_OTHERWISE.search(tight)
    if (PALLIATIVE_ITSELF.search(tight) and not asks_anything(tight)
            and not _WORKING_WITH_THE_DYING.search(tight)):
        return True
    if COULD_BE_DAYS.search(tight) and TOLD_US.search(tight):
        return not DAYS_WAIT_FOR.search(tight)
    if OFF_LIFE_SUPPORT.search(tight) and not OFF_SUPPORT_WELL.search(tight):
        return True
    if HOSPICE_CARE.search(tight) and not HOSPICE_JOB.search(tight):
        return True
    return False


def _the_vet_said_it(tight, words):
    return ("vet" in tight.split() or "vets" in tight.split()) and not (
        set(words) & HUMAN_WORDS)


THE_GIVE_UP_NAMES = re.compile(
    r"\b(?:do|done|doing|try|trying|offer|suggest)\s+(?:about|for|with|on|to)\s+(.{0,40})")
PEOPLE_AFTER_A_GIVE_UP = frozenset((
    "she", "he", "her", "him", "his", "hers", "them", "their", "us", "me", "mum", "mum's",
    "mums", "mom", "mom's", "moms", "dad", "dad's", "dads", "nan", "nan's", "nans", "gran",
    "gran's", "grans", "mother", "father", "parents", "son", "daughter", "husband", "wife",
    "sister", "brother", "child", "baby", "friend", "partner"))


def _the_give_up_is_about_somebody(tight, words, third_person_only=False):
    named = THE_GIVE_UP_NAMES.search(tight)
    if not named:
        return not third_person_only
    subject = named.group(1)
    if SERIOUS_CARE.search(subject):
        return True
    named_words = words_of(subject)
    if not named_words:
        return not third_person_only
    last = named_words[-1]
    if third_person_only and last in ("me", "us", "i", "mine", "ours"):
        return False
    return last in PEOPLE_AFTER_A_GIVE_UP or _has_person([last])


SAID_IT = re.compile(r"\b(?:said|says|say|told|tells|telling)\b")
NOT_A_CARE_GIVER = re.compile(
    r"\b(?:schools?|council|boss|manager|bank|landlord|letting\s+agent|employer|work|hr|"
    r"university|college|nursery|garage|mechanic|dealer|insurers?|insurance|dwp|benefits|"
    r"union|lawyers?|solicitors?|social\s+services|court|police|jobcentre|agent|unions?|"
    r"customers?\s+service|the\s+office)\b")


def _the_give_up_without_a_care_word(tight, who):
    if who or not NOTHING_MORE_TO_DO.search(tight) or not SAID_IT.search(tight):
        return False
    if NOT_A_CARE_GIVER.search(tight):
        return False
    return _the_give_up_is_about_somebody(tight, None, third_person_only=True)


DYING_REPLIES = SOMEONE_DYING + (
    "I'm sorry. That's a hard thing to be living with - is there help coming in, or is most of it "
    "on you?",
    "I'm sorry. It is happening now rather than after, and that is the part nobody prepares you "
    "for. Who is looking after you while you look after them?",
)

PUT_DOWN_REGRET_REPLIES = (
    "I'm so sorry. Wanting it back is not the same as having done it wrong, and it is the last "
    "call anyone wants to make. When you feel up to it the vet can arrange the cremation or a "
    "home burial, and you can ask them for a paw print.",
    "I'm sorry. That is the heaviest kind of decision to be carrying. You do not have to sort "
    "anything today; when you are ready the vet will handle the cremation, and they can take a "
    "paw print for you.",
    "I'm really sorry. Regret is what love looks like afterwards, and it does not mean you got "
    "it wrong. The practical bit can wait a day or two - the vet arranges the cremation, and ask "
    "them about a paw print if you would want one.",
)

LOSS_REPLIES = (
    "I'm so sorry to hear that. It's a hard thing to carry — I'm here if you want to talk "
    "about it, or if anything practical would help.",
    "I'm really sorry. Be gentle with yourself today, and tell me if there's anything you "
    "want to talk through.",
    "That's such sad news, I'm sorry. Some days will be heavier than others — I'm here if you "
    "want to talk about it, or about anything else.",
    "I'm sorry, that's a real loss. Take today slowly, and shout if there's anything I can "
    "help you sort out.",
)

DYING_SAY_REPLIES = (
    "Say the plain things while they can hear them: that you love them, one memory you both "
    "laugh at, and that you will be all right. Nothing clever is needed.",
    "Skip the big speech and tell them one specific thing you are grateful for. It is easier to "
    "say than \"I love you\" out loud, and it is what people remember being told.",
    "Ask them what they want to talk about, and follow that. If they want the ordinary stuff - "
    "the garden, the football - that is not avoiding it, that is the visit.",
    "Bring them something to decide or to hear: how the family is, what the doctor said, the "
    "small gossip. Being useful is how most people say it.",
)

DYING_GRIEF_REPLIES = (
    "Grieving someone who is still here is normal, and it is not a rehearsal for the real thing: "
    "it is the real thing, starting early. It comes in waves in the same way.",
    "That heaviness before the death is common - it is called anticipatory grief, and it does not "
    "make the later grief smaller or bigger, it is just its own thing. Talk to someone about it.",
    "It is normal to be tired, snappy and forgetful while someone is dying, and it is not a "
    "failing. If it is stopping you sleeping or eating for more than a fortnight, tell your GP.",
    "You can be grieving and relieved and guilty in the same hour, and none of that makes you "
    "bad. Most people who are where you are say the same.",
)

GETTING_THROUGH_REPLIES = (
    "One piece at a time is the only way anyone does it. Pick the next thing - a shower, a "
    "sandwich, one phone call - and let the rest wait until that is done.",
    "Keep the shape of the day: up at the usual time, food at the usual times, bed at night. "
    "The routine carries you on the days you cannot carry yourself.",
    "Tell one person how you are actually doing today and let them do one job for you. Most "
    "people want to help and do not know how to ask.",
    "The first days are the hardest and they are not a forecast of the rest. If you cannot eat "
    "or sleep, or you cannot see a way forward, tell your GP - they can help with that.",
)

GETTING_THROUGH_DYING_REPLIES = (
    "An hour at a time, and the ordinary things - food, a shower, going to work - are not a "
    "break from it, they are how you keep going.",
    "Take one day's jobs and no more, tell people what is happening so it is not all on you, "
    "and let the visits that do not matter drop.",
    "You do not have to be all right while this is going on. If you cannot sleep or eat, or you "
    "are carrying it with nobody to say it to, tell your GP.",
)

REMEMBER_REPLIES = (
    "Do it smaller rather than skip it: the same lunch or the same cake, with one or two people, "
    "and say out loud why you are having it. A day you have planned for is easier than one that "
    "just arrives.",
    "Keep the ritual and shrink it: the food they loved, their place at the table, and one story "
    "about them told to whoever is there. Doing something is what marks the day.",
    "Pick one thing to do at the time you would normally have spent together - the lunch, a walk, "
    "a visit - and tell someone you are doing it, so you are not carrying it on your own.",
    "Cook their dish or get their favourite in, and raise a glass to them: the point is to mark "
    "the day on purpose instead of letting it hit you sideways.",
    "Make the day about them: the meal they would have chosen, the people they liked, and the one "
    "thing you would have told them. If it all feels too heavy, do a small version and stop "
    "there.",
)

MISLAID_REPLIES = (
    "Tell a member of staff straight away — shops can call it out over the tannoy and watch the "
    "doors, which beats searching on your own.",
    "Go back to the last place you saw them and tell the nearest member of staff what they're "
    "wearing, so everyone is looking for the same person.",
    "Ask staff to put a call out and cover the exits. If it's a child, or someone vulnerable, "
    "ring 999 once it's more than a few minutes.",
)

SAY_REPLIES = (
    "Keep it plain and warm: \"I'm so sorry\". Use the person's name, don't rush to fill the "
    "silence, and offer one concrete thing — a lift, a meal, covering a shift.",
    "You don't need the perfect words. \"I'm so sorry\" and then listening is most of it; add "
    "one specific offer of help this week.",
    "Say you're sorry, name them if you can, and offer something practical. \"I'll bring "
    "dinner on Thursday\" helps far more than \"let me know if you need anything\".",
)

NAMED_LOSS_SAY_REPLIES = (SAY_REPLIES[0], SAY_REPLIES[2])

CARD_REPLIES = (
    "Keep it short and warm: \"I'm so sorry for your loss. Thinking of you and your family.\" "
    "If you knew them, add one small memory — that is the part people keep.",
    "Two or three lines is plenty: name the person, say you are sorry, and add a practical "
    "offer — a meal, a lift, a hand with the children.",
)

GRIEF_REPLIES = (
    "That is normal after a loss, and it eases slowly for most people. If it is still this "
    "heavy, your GP is the right person to talk to.",
    "Most people find the same, and it does get easier. Be gentle with yourself — and see your "
    "GP if it has not lifted.",
    "That is part of grief for most people. If it stays like this, tell your GP; there is real "
    "help for it.",
)

PET_GRIEF_REPLIES = (
    "It does get easier, and slowly. Losing a {animal} takes something out of every day, so the "
    "quiet is loudest in the first weeks; if it is still this heavy after a month, your GP is the "
    "right person to talk to.",
    "It's real grief, and it eases the same way a person's does - slowly. Losing {article} "
    "{animal} leaves a gap in the day, so be gentle with yourself, and see your GP if it has not "
    "lifted in a few weeks.",
    "Most people find it eases, and no timetable is right. If it stays this heavy, tell your GP: "
    "grief for {article} {animal} counts, and there is real help for it.",
)

FUNERAL_REPLIES = (
    "Go if you can, even just for the service: turning up matters far more than anything you "
    "say. Take a card, say the plain thing, and leave when you need to.",
    "If you can make it, go — families remember who came. You don't have to speak; sitting "
    "with them is the thing.",
)


FUNERAL_COST_COMPARE_REPLIES = (
    "Cremation usually comes out cheaper than burial: the plot, the grave being dug and often a "
    "headstone are what the difference is made of. Ask two funeral directors for a written, "
    "itemised quote and compare the coffin, the cars and the cremation fee as separate lines.",
    "Cremation, yes - a burial adds the plot, the digging and usually a headstone, and that is "
    "where the difference is. The rest of the bill is much the same either way, so ask for the "
    "itemised quote and look at the coffin first.",
    "A cremation with no service is the cheapest of the lot, and a burial is the dearest: the "
    "plot and the headstone are the difference. Prices move a lot by area, so get two itemised "
    "quotes in writing before you decide.",
)

FUNERAL_COST_ELSE = re.compile(
    r"\b(?:flowers?|wreath|bouquet|music|songs?|hymns?|buffet|sandwiches|catering|drinks?|"
    r"order of service|programme|cards|outfit|clothes|suit|dress|shoes|tie|travel|fare|fares|"
    r"flights?|petrol|coach|taxi)\b"
    r"|\b(?:go|get|going|getting) to (?:the|his|her|their) funeral\b")

_A_DAY_PART = (r"(?:music|songs?|hymns?|tunes?|readings?|reads?|recit(?:e|ed|ing)|poems?|"
               r"psalms?|flowers?|wreaths?|"
               r"bouquets?|order of service|kids?|children|child|baby|toddler|grandchildren|"
               r"grandkids)")
A_PART_OF_THE_DAY = re.compile(
    r"\b(?:what|which|any)\b(?:\W+\w+){0,5}\W+" + _A_DAY_PART + r"\b"
    r"|\b(?:should|shall|can|could|do)\s+(?:i|we|you)\b(?:\W+\w+){0,6}\W+" + _A_DAY_PART
    + r"\b"
    r"|\b(?:should|shall|can|could|do|does)\s+(?:(?:i|we|you|a|the|any|my|our)\s+)?"
    r"(?:kids?|children|child|baby|toddler|grandchildren|grandkids)\b"
    r"|\b(?:good|nice|right|best|suitable)\s+(?:songs?|hymns?|tunes?|music|readings?|poems?|"
    r"psalms?)\b"
    r"|\b(?:should|shall|can|could)\s+(?:my|our)\b(?:\W+\w+){0,4}\W+" + _A_DAY_PART + r"\b"
    r"|\bhow\s+long\s+(?:is|does|do|are|will|would)\b(?:\W+\w+){0,4}\W+(?:funeral|service|"
    r"cremation|burial|wake|memorial)\b"
    r"|\bhow\s+long\s+(?!until|till|to|before)\w*(?:\W+\w+){0,6}\W+\bfuneral\b"
    r"|\bhow\s+many\s+(?:days|weeks)\b(?:\W+\w+){0,6}\W+\bfuneral\b"
    r"|\bhow\s+soon\b(?:\W+\w+){0,4}\W+\bfuneral\b"
    r"|\bis\s+it\s+(?:ok|okay|fine|alright)\b(?:\W+\w+){0,6}\W+" + _A_DAY_PART + r"\b",
    re.I)
SAY_THE_WORDS = re.compile(
    r"\b(?:what to say|what do i say|what can i say|what should i say|what shall i say|"
    r"say at|say to|words for|eulogy|eulogies|speech)\b", re.I)

_DEATH_IN_LINE = re.compile(
    r"\b(?:died|dies|dying|dead|death|passed away|passed on|passed|killed|cremated|"
    r"buried|widow|widower)\b")

_FUNERAL_NOUN = r"(?:funerals?|cremations?|cremation|crematoriums?|cremate|burials?|bury|buried|"
_FUNERAL_NOUN += r"undertakers?|funeral directors?)"
_COST_NOUN = r"(?:cost|costs|costing|price|prices|priced|expensive|cheaper|cheapest|cheap|"
_COST_NOUN += r"afford|affordable|pay|paid|paying|fee|fees|money|budget|quote|quotes|"
_COST_NOUN += r"how much)"
FUNERAL_COST = re.compile(
    r"\b" + _FUNERAL_NOUN + r"\b[^.?!]{0,30}?\b" + _COST_NOUN + r"\b"
    r"|\b" + _COST_NOUN + r"\b[^.?!]{0,30}?\b" + _FUNERAL_NOUN + r"\b")

_THE_ESTATE = re.compile(r"\b(?:estate|probate|inheritance|the will)\b")
FUNERAL_HELP = re.compile(
    r"\b" + _FUNERAL_NOUN + r"\b[^.?!]{0,30}?\b(?:help|afford|claim|payment|pay for|council|"
    r"benefits?|dwp|social fund|charity|charities)\b"
    r"|\b(?:help|afford|claim|payment|pay for|council|benefits?|dwp|social fund|charity|"
    r"charities)\b[^.?!]{0,30}?\b" + _FUNERAL_NOUN + r"\b")
HELP_ASK = re.compile(r"\b(?:help|claim|claiming)\b|can'?t afford|cannot afford|cant pay|"
                      r"can'?t pay|no money|nothing to pay")
FUNERAL_HELP_REPLIES = (
    "There is help with it: the DWP funeral expenses payment covers part of the bill if you are "
    "on certain benefits, and you claim it after the funeral, within six months. Keep every "
    "receipt, and ring the council as well - they have a fund of their own for people who cannot "
    "pay.",
    "Claim the DWP funeral expenses payment within six months of the funeral: it covers the "
    "cremation or burial fees and some of the rest, and it goes to whoever arranged it. If you "
    "are on a low income, ask the council too - they pay for a funeral when there is no money at "
    "all.",
    "You can apply for the funeral expenses payment from the DWP after the funeral - within six "
    "months, and only on certain benefits - so tell the funeral director to invoice you and keep "
    "the receipts. The council's bereavement service has a separate fund, and Citizens Advice "
    "will help you fill the forms in.",
)
QUIETER_ASK = re.compile(r"\b(?:which|cheaper|cheapest|how much|prices?)\b")
FUNERAL_COST_COMPARE = re.compile(
    r"\b(?:cheaper|cheapest|more expensive|less expensive|costs? more|costs? less|vs|versus|"
    r"instead of|or a burial|or burial|or cremation|or a cremation|worth it)\b")
_BURIAL_SIDE = re.compile(r"\b(?:burials?|bury|buried|burying|graves?|plots?|headstones?|coffins?)\b")
_CREMATION_SIDE = re.compile(r"\b(?:cremations?|cremate|cremated|crematoriums?|ashes|urns?)\b")


_PRONOUN_MONEY_ASK = re.compile(
    r"\b(?:help|pay|paying|paid|afford|claim|claiming|cost|costs|costing|money|cheaper|"
    r"how much)\b[^.?!]{0,24}?\b(?:it|that|this|them)\b"
    r"|\b(?:it|that|this|them)\b[^.?!]{0,24}?\b(?:cost|costs|pay|paid|afford|expenses?|"
    r"expensive|cheap)\b")
_BILL_SUBJECT = re.compile(
    r"\b(?:funerals?|cremations?|cremation|crematoriums?|burials?|bury|buried|coffins?|"
    r"undertakers?|funeral directors?)\b")
_BILL_MONEY = re.compile(
    r"\b(?:cost|costs|price|prices|quote|quotes|pay|paid|paying|fee|fees|afford|bill|"
    r"dwp|benefit|benefits|cheapest|cheaper)\b|\u00a3|\bthousands?\b")

_NOT_A_BILL_THREAD = frozenset(("safety", "urgent"))


def _the_bill_was_the_last_turn(memory):
    turns = [t for t in ((memory or {}).get("turns") or []) if isinstance(t, dict)]
    if not turns:
        return False
    last = turns[-1]
    if last.get("module") in _NOT_A_BILL_THREAD:
        return False
    said = str(last.get("bot") or "").lower()
    return bool(_BILL_SUBJECT.search(said) and _BILL_MONEY.search(said))

LOSS_STILL_THE_THREAD = 3


def _loss_is_the_thread(memory):
    record = (memory or {}).get("loss")
    if not isinstance(record, dict):
        return False
    turns = (memory or {}).get("turns") or ()
    return len(turns) - int(record.get("turn") or 0) <= LOSS_STILL_THE_THREAD


def arrangement_cost_pool(line, tight=None, memory=None):
    tight = _tight(line) if tight is None else tight
    if FUNERAL_COST_ELSE.search(tight) or _DEATH_IN_LINE.search(tight):
        return None
    if _PRONOUN_MONEY_ASK.search(tight) and _the_bill_was_the_last_turn(memory):
        if FUNERAL_COST_COMPARE.search(tight) and not HELP_ASK.search(tight):
            return FUNERAL_COST_COMPARE_REPLIES
        return FUNERAL_HELP_REPLIES
    if _loss_is_the_thread(memory):
        return None
    if not (FUNERAL_COST.search(tight) or FUNERAL_HELP.search(tight)):
        return None
    if not (asks_anything(line, tight) or QUIETER_ASK.search(tight)
            or FUNERAL_COST_COMPARE.search(tight) or HELP_ASK.search(tight)):
        return None
    if FUNERAL_HELP.search(tight) and not _THE_ESTATE.search(tight):
        return FUNERAL_HELP_REPLIES
    if (FUNERAL_COST_COMPARE.search(tight) and _BURIAL_SIDE.search(tight)
            and _CREMATION_SIDE.search(tight)):
        return FUNERAL_COST_COMPARE_REPLIES
    return None

ACKNOWLEDGE = re.compile(
    r"\b(?:sorry (?:to hear|for your loss)|such sad news|condolences|my sympathy|sympathies|"
    r"real loss|hard(?:est)? days?|nothing prepares you)\b")


OWN_STATE = re.compile(
    r"\b(?:i|i'm|im|i've|ive|me|my|we|we're|were|us)\b[^.]*\b(?:cry|crying|cried|tears|"
    r"guilty|guilt|miss|missing|struggling|broken|heartbroken|devastated|numb|angry|lonely|"
    r"sad|empty|numb|cant stop|can't stop|cannot stop|keep thinking|nightmares?|feel awful|"
    r"feel terrible|feel lost|feel sick)\b")


OWN_PET = re.compile(r"\b(?:my|our)\s+(?:(?:old|poor|little|beloved|lovely|sweet|baby|family|"
                     r"best)\s+)?(?:" + "|".join(sorted(PET_WORDS)) + r")\b")

CLAUSE = re.compile(r"[;,]|\b(?:and|but|then|so|because|although|though|while|after|before|"
                    r"which|who)\b")


PUTTING_REGRETTED = re.compile(
    r"\b(?:regrets?|regretted|regretting|wish)\b[^.?!]{0,24}?"
    r"\bputting\s+(?:\w+\s+){0,3}?(?:to sleep|down)\b")

NOT_YET = re.compile(
    r"\b(?:is|are|am)\s+being\s+(?:put|euthanis\w*)"
    r"|\b(?:will|would|going to|about to|has to|have to|needs? to|got to|due to)\s+"
    r"(?:be\s+)?(?:put|euthanis\w*)"
    r"|\b(?:have|has|need|needs|got)\s+to\s+(?:put|be put)\b"
    r"|\b(?:have|has|need|needs|got)\s+to\s+have\s+(?:\w+\s+){0,3}?(?:put|euthanis\w*)"
    r"|\bputting\s+(?:\w+\s+){0,3}?(?:to sleep|down)\b"
    r"|\b(?:is|are|am|was|were)\s+dying\b"
    r"|\b(?:mum|mom|mam|dad|father|mother|nan|nana|gran|granny|grandad|grandma|brother|sister|"
    r"wife|husband|partner|friend|son|daughter)s\s+dying\b"
    r"|\b(?:isn'?t|isnt|not|never|won'?t|wont|is not)\s+going\s+to\s+(?:make\s+it|last)\b"
    r"|\b(?:has|had|have|say|says|said|told)\s+(?:\w+\s+){0,4}?"
    r"(?:a\s+few|a\s+couple\s+of|another|one|two|three|four|five|six|a\s+matter\s+of)\s+"
    r"(?:days?|weeks?|months?)\s+(?:left|to\s+go|or\s+so)\b"
    r"|\b(?:gave|given|gives)\s+(?:\w+\s+){0,4}?"
    r"(?:a\s+few|a\s+couple\s+of|another|one|two|three|four|five|six|a\s+matter\s+of)\s+"
    r"(?:days?|weeks?|months?)\b"
    r"|\b(?:days?|weeks?|months?)\s+(?:left|to\s+go)\b"
    r"(?!\s+(?:of|in|on|until|till|before|for))")
ESTIMATE = re.compile(
    r"\b(?:has|had|have|say|says|said|told)\s+(?:\w+\s+){0,4}?"
    r"(?:a\s+few|a\s+couple\s+of|another|one|two|three|four|five|six|a\s+matter\s+of)\s+"
    r"(?:days?|weeks?|months?)\s+(?:left|to\s+go|or\s+so)\b"
    r"|\b(?:gave|given|gives)\s+(?:\w+\s+){0,4}?"
    r"(?:a\s+few|a\s+couple\s+of|another|one|two|three|four|five|six|a\s+matter\s+of)\s+"
    r"(?:days?|weeks?|months?)\b")
NOTHING_MORE_TO_DO = re.compile(
    r"\b(?:nothing|not\s+much|not\s+anything)\s+(?:more|else|further|left)\b"
    r"[^.!?]{0,40}?\b(?:do|done|try|trying|offer|suggest)\b")
TREATMENT_STOPPED = re.compile(
    r"\b(?:stopped|stopping|stop|cease[ds]?|halted|withdrawn\s+from|taken\s+off|came\s+off|"
    r"no\s+longer\s+(?:having|on))\s+(?:\w+\s+){0,3}?"
    r"(?:treatment|chemo|chemotherapy|radiotherapy|dialysis)\b"
    r"|\bno\s+(?:more|further)\s+(?:treatment|chemo|chemotherapy|radiotherapy|options)\b"
    r"|\b(?:treatment|chemo|chemotherapy|radiotherapy|dialysis)\s+"
    r"(?:has|have|had|is|are|was|were)\s+(?:been\s+)?(?:stopped|halted|withdrawn)\b")
MEDICATION_STOPPED = re.compile(
    r"\b(?:stopped|stopping|stop|cease[ds]?|halted|no\s+longer\s+(?:having|on)|taken\s+off)\s+"
    r"(?:\w+\s+){0,3}?(?:medication|meds|drugs|tablets|pills|painkillers)\b"
    r"|\b(?:medication|meds|drugs|tablets|pills|painkillers)\s+"
    r"(?:has|have|had|is|are|was|were)\s+(?:been\s+)?(?:stopped|halted|withdrawn)\b")
LAST_DRUG = (r"morphine|diamorphine|midazolam|fentanyl|oxycodone|alfentanil|levomepromazine|"
             r"syringe\s+driver|palliative\s+sedation|end\s+of\s+life\s+(?:meds|medication|drugs)")
ON_THE_LAST_DRUG = re.compile(
    r"\b(?:put|puts|putting|started|starting|starts?|switched|moved)\s+(?:\w+\s+){0,3}?"
    r"(?:on|onto)\s+(?:a\s+|the\s+|her\s+|his\s+|their\s+)?(?:" + LAST_DRUG + r")\b"
    r"|\b(?:he|she|they|mum|dad|nan|gran|grandad|grandma|grandpa|husband|wife|son|daughter|"
    r"mother|father|brother|sister|friend|mate)\b[^.!?,]{0,12}?\b(?:is|are|was|were)\s+"
    r"(?:now\s+)?(?:on|getting)\s+(?:a\s+|the\s+)?(?:" + LAST_DRUG + r")\b")
SELF_ON_THE_DRUG = re.compile(
    r"\b(?:i|i'?m|im|i'?ve|i\s+have|i\s+was|i\s+got|i'?d|me|my\s+(?:back|knee|hip|leg|arm|"
    r"shoulder|teeth|tooth|wrist|ankle))\b[^.!?]{0,20}?\b(?:" + LAST_DRUG + r")\b")


def says_the_last_drug(tight):
    if not ON_THE_LAST_DRUG.search(tight):
        return False
    return not SELF_ON_THE_DRUG.search(tight)


CARE_WHO = re.compile(
    r"\b(?:doctors?|doctor'?s|gps?|consultants?|surgeons?|specialists?|oncologists?|oncology|"
    r"hospitals?|hospice|ward|icu|intensive\s+care|nurses?|palliative|vets?|clinic|"
    r"treatment|chemo|chemotherapy|radiotherapy|dialysis|cancer|tumours?|tumors?|leukaemia|"
    r"leukemia|dementia|motor\s+neurone|parkinsons?)\b")
DAYS_LEFT = re.compile(
    r"\b(?:days?|weeks?|months?)\s+left\b"
    r"(?!\s+(?:of|in|on|at|with|before|until|for)\b)(?!\s+to\b(?!\s+live\b))"
    r"|\b(?:days?|weeks?|months?)\s+to\s+live\b"
    r"|\b(?:not\s+)?long\s+(?:left|to\s+go)\b"
    r"|\b(?:a|only\s+a)\s+matter\s+of\s+(?:time|days|weeks|hours)\b")
NOT_THE_END = re.compile(
    r"\b(?:left|to\s+go)\s+(?:of|in|on|at|with|before|until|for)\b"
    r"|\b(?:left|to\s+go)\s+to\s+(?!live\b|be\b)")
FINAL_DAYS = re.compile(
    r"\b(?:her|his|their|my|our)\s+final\s+(?:days|weeks|months)\b"
    r"|\bfinal\s+(?:days|weeks|months)\s+of\s+(?:her|his|their|my|our)\s+life\b")
COULD_BE_DAYS = re.compile(
    r"\b(?:could|might|may|probably)\s+be\s+(?:a\s+)?(?:few\s+|couple\s+of\s+)?"
    r"(?:days|weeks|hours)\b")
DAYS_WAIT_FOR = re.compile(
    r"\b(?:days?|weeks?|hours?)\s+(?:for|until|till|til|before|by|of)\s+"
    r"(?!the\s+(?:end|worst)\b|his\s+end\b|her\s+end\b|she\s+goes\b|he\s+goes\b|"
    r"it\s+happens\b)")
LAST_STAGES = re.compile(
    r"\b(?:the\s+)?(?:last|final|end)\s+(?:days|weeks|stages?)\b"
    r"|\bin\s+(?:the\s+)?(?:final|end)\s+stages?\b"
    r"|\b(?:final\s+)?stages?\s+of\s+(?:her|his|their|my|our)\s+(?:cancer|illness|disease|life)\b")
NOT_GETTING_BETTER = re.compile(
    r"\b(?:isnt|isn'?t|wont|won'?t|never\s+going\s+to|not\s+going\s+to|will\s+not)\s+"
    r"(?:will\s+)?(?:going\s+to\s+)?get\s+(?:any\s+)?better\b"
    r"|\bno\s+longer\s+going\s+to\s+get\s+better\b")
GIVEN_UP_ON = re.compile(r"\bgiven\s+up\s+on\b|\bhave\s+given\s+up\b|\bgive\s+up\s+on\b")
PREPARE = re.compile(
    r"\bprepare\s+(?:ourselves|yourself|yourselves|the\s+family|them)\b")
PREPARE_OTHERWISE = re.compile(
    r"\b(?:results?|exams?|tests?|interviews?|inspections?|audit|inspection|wedding|move|visit|"
    r"appointment|flight|holiday|winter|storm|review|scans?|x-?rays?)\b")
OFF_LIFE_SUPPORT = re.compile(
    r"\b(?:taken|taking|took|take|came|come|coming|coming\s+off)\s+(?:\w+\s+){0,2}?"
    r"off\s+(?:the\s+)?(?:ventilator|ventilation|life\s+support|breathing\s+machine)\b")
OFF_SUPPORT_WELL = re.compile(
    r"\b(?:on\s+(?:his|her|their)\s+own|breathing\s+(?:on|by)|himself|herself|awake|talking)\b")
TOLD_US = re.compile(
    r"\b(?:we'?ve\s+been\s+told|we\s+were\s+told|they'?ve\s+told\s+us|they\s+told\s+us|"
    r"they\s+(?:have\s+)?said|doctors?\s+(?:have\s+)?said|consultants?\s+(?:have\s+)?said)"
    r"\b")
NOT_WORKING = re.compile(
    r"\b(?:isnt|isn'?t|not|stopped|no\s+longer)\s+working\b"
    r"|\b(?:has|have|had)\s+stopped\s+working\b")
SERIOUS_CARE = re.compile(
    r"\b(?:oncologists?|oncology|consultants?|specialists?|palliative|hospices?|"
    r"cancer|tumours?|tumors?|leukaemia|leukemia|dementia|motor\s+neurone|parkinsons?|mnd|"
    r"end\s+of\s+life|morphine|syringe\s+driver|last\s+stages)\b")
HOSPICE_CARE = re.compile(
    r"\bhospice\s+care\b"
    r"|\b(?:in|at)\s+(?:a\s+|the\s+|her\s+|his\s+|their\s+)?hospice\b"
    r"|\b(?:moved|moving|transferred|gone|went|going|admitted|taken|took)\b"
    r"(?:\s+\w+){0,3}?\s+(?:in)?to\s+(?:a\s+|the\s+|her\s+|his\s+|their\s+)?hospice\b"
    r"|\b(?:into|onto)\s+(?:a\s+|the\s+|her\s+|his\s+|their\s+)?hospice\b"
    r"|\bhospice\s+(?:is\s+being\s+arranged|has\s+been\s+arranged|at\s+home)\b")
HOSPICE_JOB = re.compile(
    r"\b(?:jobs?|works?|worked|working|volunteers?|volunteering|nurse\s+there|manager|staff|"
    r"shifts?|sponsors?|sponsored|sponsoring|fundrais\w*|raise\s+(?:money|funds)|raising\s+money|"
    r"collecting|collection|donate|donating|donations?|cake\s+sale|charity|justgiving|marathon|"
    r"walk|run|cycle|ride|quiz|raffle|tombola|bring\s+and\s+buy|open\s+day)\b")
PALLIATIVE_ITSELF = re.compile(r"\bpalliative\b")

DYING_OTHER = re.compile(
    r"\bdying\s+(?:for|to)\b"
    r"|\bdying\s+(?:my|her|his|their|our|your|the)\s+"
    r"(?:hair|beard|roots|eyebrows|eyebrow|nails|lashes)\b"
    r"|\bdying\s+it\b")

ASK_BARE = re.compile(r"\b(?:is|was|isn'?t|wasn'?t)\s+(?:it|that|this)\b")


def asks_about_the_remains(line, tight=None):
    line = str(line or "")
    tight = _tight(line) if tight is None else tight
    if not PET_ARRANGEMENT.search(tight):
        return False
    return bool(asks_anything(line, tight) or ASK_WE.search(tight) or ASK_TAIL.search(line)
                or ASK_BARE.search(tight))


def a_pet_died(line):
    text = str(line or "").lower().replace("\u2019", "'")
    if NOT_YET.search(text) and not PUTTING_REGRETTED.search(text):
        return False
    for clause in CLAUSE.split(text):
        if not OWN_PET.search(clause):
            continue
        words = _plain(clause)
        if words and reads_as_loss(clause, words):
            return True
    return False


PRACTICAL_ASK = re.compile(
    r"\b(?:what|who|where|when|how)\s+(?:do|does|should|shall|can|could|now|next)\b"
    r"|\b(?:do|should|shall|can|could|need)\s+(?:we|i)\s+\w+"
    r"|\b(?:is|was|isn'?t|wasn'?t)\s+(?:\w+\s+){0,3}(?:expensive|costly|cheap)\b"
    r"|\bhow\s+(?:much|expensive)\b")


ADMINISTRATION = re.compile(
    r"\b(?:funerals?|cremation|crematorium|burial|coffin|headstone|probate|wills?|estate|"
    r"solicitors?|coroner|register(?:ing)? the death|death certificate|medical certificate|"
    r"bank accounts?|insurance|pension|bereavement|inheritance|funeral directors?|grave|"
    r"chapel of rest|quotes?|cheapest)\b", re.I)


def asks_the_administration(line):
    text = " ".join(str(line or "").lower().replace("\u2019", "'").split())
    return bool(ADMINISTRATION.search(text))


ADMINISTRATION_KEYS = (
    ("accounts", r"\b(?:bank\s+)?accounts?\b|\bbereavement team\b"),
    ("registration", r"\bregist(?:er|ering|ration)(?:\s+(?:the|a|his|her|their))?\s+death\b"
                     r"|\bregister office\b"),
    ("death certificate", r"\bdeath certificate\b|\bmedical certificate\b"),
    ("probate", r"\bprobate\b|\bletters of administration\b"),
    ("inheritance", r"\binheritance(?: tax)?\b|\biht\d*\b"),
    ("estate", r"\bestate\b|\bexecutor\b"),
    ("will", r"\bwills?\b"),
    ("funeral", r"\bfunerals?\b|\bfuneral directors?\b|\bchapel of rest\b"),
    ("cremation", r"\bcremat(?:ion|orium|e|ed)\b"),
    ("burial", r"\bburials?\b|\bbury\b|\bburied\b|\bgrave(?:side)?\b"),
    ("coffin", r"\bcoffins?\b|\bheadstones?\b"),
    ("solicitor", r"\bsolicitors?\b"),
    ("coroner", r"\bcoroners?\b"),
    ("insurance", r"\binsurance\b|\blife cover\b"),
    ("pension", r"\bpensions?\b"),
)


def administration_keys(text):
    lowered = " ".join(str(text or "").lower().replace("\u2019", "'").split())
    return frozenset(key for key, pattern in ADMINISTRATION_KEYS
                     if re.search(pattern, lowered))


DEFINES = re.compile(r"^\s*(?:a|an|the)\s+[\w'-]+\s+(?:says|means|is)\b", re.I)

THE_DEATH = re.compile(
    r"\b(?:died|dies|dying|death|dead|deceased|passed away|bereave\w*|widow\w*|widower\w*|"
    r"estate|executor|next of kin|funeral|cremation|burial)\b", re.I)


def is_about_the_paperwork(reply, line):
    if not (administration_keys(line) & administration_keys(reply)):
        return False
    text = str(reply or "")
    if DEFINES.match(text) or not THE_DEATH.search(text):
        return False
    return True


OPEN_ASK = re.compile(
    r"^\s*(?:(?:and|so|ok|okay|but|well|right)\s*,?\s*)*"
    r"(?:what\s+(?:do|should|shall|can|could)\s+(?:i|we)\s+(?:do|now|next)(?:\s+(?:now|next|today))?"
    r"|what\s+(?:now|next|happens\s+now|do\s+i\s+do\s+now)"
    r"|now\s+what|where\s+do\s+(?:i|we)\s+(?:start|begin)(?:\s+now)?"
    r"|what\s+am\s+i\s+supposed\s+to\s+do(?:\s+now)?)"
    r"(?:\s+about\s+(?:it|that|this|him|her|them|all this|all of it))?"
    r"\s*[.?!]*$")

GET_THROUGH = re.compile(
    r"\bget(?:ting)?\s+through\s+(?:it|this|that|today|tonight|the\s+"
    r"(?:day|days|night|nights|week|weeks|weekend|first\s+few\s+days|first\s+week))\b"
    r"|\bhow\s+(?:am|do|will|can)\s+i\s+(?:supposed\s+to\s+)?"
    r"(?:get\s+through|carry\s+on)"
    r"(?:\s+(?:it|this|that|today|tonight|the\s+"
    r"(?:day|days|night|nights|week|weeks|weekend|first\s+few\s+days|first\s+week)))?"
    r"\s*[.?!]*$")
GET_THROUGH_TO = re.compile(r"\bget(?:s|ting)?\s+through\s+to\b")
GET_THROUGH_DAY = re.compile(
    r"\bget(?:ting)?\s+through\s+(?:christmas|the\s+holidays?|new\s+year|easter|"
    r"(?:his|her|their|my\s+(?:mums?|dads?|nans?|grans?|sons?|daughters?))\s+birthday|"
    r"birthdays?|the\s+anniversary|our\s+anniversary|mothers?\s+day|fathers?\s+day)\b")

GET_THROUGH_OBJECT = re.compile(r"\bget(?:ting)?\s+through\s+([a-z' ]{1,60})")
GET_THROUGH_FILLER = frozenset((
    "the", "a", "an", "this", "that", "these", "those", "my", "his", "her", "their", "our",
    "your", "of", "at", "in", "on", "to", "with", "without", "and", "for", "by", "from", "s",
    "too", "as", "well", "again", "now", "still", "just", "all", "every", "first", "next",
    "last", "few", "couple", "up", "through", "it", "him", "them", "us", "me", "i", "if", "when",
    "while", "til", "until", "alone", "so", "very", "much", "more", "each", "any", "some",
))
GET_THROUGH_THE_LOSS = frozenset((
    "day", "days", "night", "nights", "week", "weeks", "weekend", "weekends", "month",
    "months", "year", "years", "hour", "hours", "evening", "evenings", "morning", "mornings",
    "afternoon", "afternoons", "today", "tonight", "tomorrow", "time", "times",
    "christmas", "xmas", "easter", "new", "birthday", "birthdays", "anniversary", "wedding",
    "funeral", "wake", "holiday", "holidays", "mothers", "fathers", "mother", "father", "mum",
    "mums", "dad", "dads", "nan", "nans", "gran", "grans", "son", "sons", "daughter",
    "daughters", "valentines", "death", "dying", "loss", "grief", "sorrow", "mourning",
    "missing", "absence", "empty", "quiet", "silence", "sad", "hard", "hardest", "worst", "bad",
    "dark", "lonely", "pain", "ache", "rest", "everything", "bit", "part", "piece", "pieces",
    "one", "two", "three", "it", "them", "him", "her",
    "work", "office", "colleagues", "people",
))


def _a_thing_of_its_own_to_get_through(line):
    found = GET_THROUGH_OBJECT.search(line)
    if not found:
        return False
    for word in words_of(found.group(1)):
        if word in GET_THROUGH_FILLER or word in GET_THROUGH_THE_LOSS:
            continue
        return True
    return False


def asks_for_a_decision(line):
    text = " ".join(str(line or "").lower().replace("\u2019", "'").split())
    return bool(PRACTICAL_ASK.search(text))


BODY_FEELING = re.compile(
    r"\b(?:is|was|feels|seems|sounds)\s+(?:\w+\s+){0,3}"
    r"(?:cremat\w*|burial|burying|ashes|coffin|casket|urn|grave|euthanasi\w*)\s+"
    r"(?:\w+\s+){0,3}"
    r"(?:sad|hard|difficult|awful|grim|brutal|expensive|cheap|costly|right|wrong|ok|okay|"
    r"easy|quick|painful|kind|better)\b"
    r"|\b(?:cremat\w*|burial|burying|ashes|coffin|casket|urn|grave|euthanasi\w*)\s+"
    r"(?:is|was|feels|seems|sounds)\s+(?:\w+\s+){0,2}"
    r"(?:sad|hard|difficult|awful|grim|brutal|expensive|cheap|costly|right|wrong|ok|okay|"
    r"easy|quick|painful|kind|better)\b")

def feeling_about_the_body(line):
    return bool(BODY_FEELING.search(" ".join(str(line or "").lower().split())))


def names_a_feeling(line):
    text = " ".join(str(line or "").lower().split())
    return bool(OWN_STATE.search(text) or ABSENCE.search(text))


def acknowledges(reply):
    return bool(ACKNOWLEDGE.search(" ".join(str(reply or "").lower().split())))


WHEN_ASK = re.compile(r"\b(what time|what day|what date|which day|when is|when's|whens|"
                      r"how long until|how long till|what time does)\b")
FUNERAL_WHEN_REPLIES = (
    "The time and place are on the family's notice or the funeral director's page — ask a family "
    "member or the funeral director if you can't find it, nobody minds being asked.",
    "Check the notice the family put out, or ring the funeral director: they will tell you the "
    "time and where to meet. Ask whether to go straight to the crematorium or meet at the house.",
    "Ask a relative or the funeral director for the time and the meeting place — most services "
    "are at the church or chapel first, then the crematorium — and get there a little early.",
)


def _when_asked(tight):
    return bool(WHEN_ASK.search(tight))


def a_part_of_the_day_asked(tight):
    if not A_PART_OF_THE_DAY.search(tight):
        return False
    return not SAY_THE_WORDS.search(tight)


ASKS_ABOUT_THE_FEELING = re.compile(
    r"\bis\s+(?:it|that|this)\s+(?:normal|weird|wrong|bad|ok|okay|common|selfish|strange|odd|"
    r"awful)\s+(?:to\s+)?(?:feel|be)\b"
    r"|\bis\s+(?:it|that)\s+(?:normal|weird|wrong|bad|ok|okay|common|selfish|strange|odd)\s+"
    r"(?:that|if)\s+i\s+(?:feel|felt|am)\b"
    r"|\bis\s+that\s+a\s+(?:normal|bad|selfish|strange)\s+thing\b"
    r"|\bwhy\s+do\s+i\s+(?:still\s+)?(?:feel|keep\s+feeling)\b"
    r"|\bdoes\s+(?:it|that)\s+(?:make\s+me|mean\s+i'?m)\b", re.I)


def _asks_about_the_feeling(tight):
    return bool(ASKS_ABOUT_THE_FEELING.search(tight))

SYMPATHY = re.compile(r"\b(sympathy|condolence|condolences|bereavement)\b")
CARD_WORD = re.compile(r"\b(card|cards|message|note|letter|text)\b")
ASK_FORM = re.compile(r"\b(should i|do i|can i|how do i|shall i|would you)\b")
ASK_WE = re.compile(r"\b(should we|can we|do we|how do we|shall we|where do we|what do we|"
                    r"when do we|who do we)\b")
ASK_TAIL = re.compile(r",\s*(?:is|are|was|were|do|does|did|should|can|how|what|where|when|who|"
                      r"will|would|shall)\b")
PET_ARRANGEMENT = re.compile(
    r"\b(bury|buried|burying|burial|body|bodies|dead|ashes|cremat\w*|cremate|urn|plot|grave|graveside|"
    r"headstone|memorial|paw\s?print|lock\s+of\s+(?:fur|hair)|coffin|casket|collect\w*|"
    r"pick\w*\s+(?:\w+\s+){0,2}up|collect\s+\w+\s+from\s+the\s+vet)\b")
PET = re.compile(r"\b(cat|dog|puppy|kitten|rabbit|hamster|guinea\s?pig|horse|pony|budgie|parrot|"
                 r"pet|pets|ferret|gerbil|rat|mouse|tortoise|snake|lizard|fish|goldfish)\b")
PET_HAS_HAD_ENOUGH_AFTER = (
    r"has\s+had\s+enough"
    r"(?=\s*(?:[,.!?;]|$)"
    r"|\s*,?\s*(?:of\s+)?(?:it|this|life|everything|it\s+all|all\s+of\s+it)\b"
    r"|\s*,?\s*(?:of\s+)?(?:the|his|her|their)\s+"
    r"(?:pain|suffering|treatment|chemo|medication|operations|surgery|seizures|incontinence)\b"
    r"|\s*,?\s+(?:he|she|it|they)?\s*(?:is|are|s)?\s*(?:not\s+eating|stopped\s+eating|"
    r"cant\s+eat|cant\s+get\s+up|cant\s+walk|cant\s+stand|in\s+pain|suffering|giving\s+up)\b"
    r"|\s+(?:now|today|already)\b)")
PET_HAS_HAD_ENOUGH = re.compile(
    r"\b(?:wants?\s+to\s+die|wants?\s+to\s+be\s+put\s+to\s+sleep|no\s+will\s+to\s+live|"
    r"doesn'?t\s+want\s+to\s+live|does\s+not\s+want\s+to\s+live|no\s+quality\s+of\s+life|"
    + PET_HAS_HAD_ENOUGH_AFTER + r")\b")
SPEAKER_HAS_HAD_ENOUGH = re.compile(
    r"\b(?:i|me|myself)\b[^.?!]{0,24}\b(?:die|dying|kill\s+myself|end\s+it|go\s+on)\b|"
    r"\b(?:so\s+(?:do|will|would|can|am|are|have|has)\s+i|me\s+too)\b")
SPEAKER_TOO = re.compile(
    r"\b(?:and\s+)?so\s+(?:am|do|have|has|will|would|can|are|is)\s+i\b"
    r"|\b(?:and\s+)?i(?:'m|\s+am|\s+do|\s+have|\s+will|\s+would|\s+can)\s+(?:too|as\s+well)\b"
    r"|\b(?:me\s+too|same\s+here|i\s+feel\s+the\s+same|i\s+feel\s+it\s+too|"
    r"neither\s+(?:do|am|have)\s+i)\b")
WISH_FRAME = re.compile(
    r"\b(?:want|wants|wanted|wanna|wish|wishes|wished|plan|plans|planning|tempted|urge|"
    r"thinking\s+(?:of|about)|thought\s+about)\b|\b(?:going|gonna)\s+to\b")
SPEAKER_TOO_REPLIES = (
    "You are carrying their ending and your own in the same breath, and that is more than one "
    "person should hold. Tell someone today - a GP, a friend, or a crisis line on 116 123 in the "
    "UK or 988 in the US - and let them take a share of it.",
    "That is two of you at the end at once, and you should not be managing it on your own. Ring a "
    "crisis line today (116 123 in the UK, 988 in the US), or tell someone close so they can be "
    "with you while you say the rest.",
    "I'm sorry. Both at once is more than one person can carry quietly: say it out loud to someone "
    "today - a friend, your GP, or a crisis line on 116 123 in the UK or 988 in the US - and let "
    "them help with the next bit.",
    "You matter in this too, not only the one you are losing. Please tell someone today - a crisis "
    "line is 116 123 in the UK and 988 in the US - and let them sit with you while you say it.",
)
PET_AT_THE_END = re.compile(
    r"\b(?:is|are|seems?|looks?)\s+done\b(?=\s*(?:[,.!?;]|$))"
    r"|\bready\s+to\s+go\b(?=\s*(?:[,.!?;]|$))"
    r"|\btelling\s+me\s+(?:its|it'?s|his|her)\s+time\b"
    r"|\bi\s+think\s+(?:its|it'?s)\s+time\b")

FILLERS = frozenset(("actually", "really", "even", "just", "exactly", "honestly",
                     "literally", "basically", "anyway", "still", "perhaps", "maybe"))
FEELING_WORDS = {
    "guilty": "guilt", "guilt": "guilt", "ashamed": "guilt", "shame": "guilt",
    "angry": "anger", "anger": "anger", "furious": "anger", "rage": "anger",
    "numb": "numb", "relieved": "relief", "relief": "relief",
}
FEELING_REPLIES = {
    "guilt": (
        "Guilt turns up with grief for most people, whether or not there is anything to be "
        "guilty about. Say the thing you keep going over out loud to someone who knew them; "
        "it weighs less that way.",
        "That guilt is a common part of it, and it is rarely fair. Tell one person who knew "
        "them what you keep turning over — you do not have to carry it on your own.",
    ),
    "anger": (
        "Anger is part of grief for most people, and it does not have to make sense. Let it "
        "out somewhere safe, then tell someone who knew them what you are angry about.",
        "Being angry at them, or at the world, or at whoever was there is common after a "
        "death. Say it out loud to one person you trust rather than keeping it in.",
    ),
    "numb": (
        "That numb feeling is common early on; it is not coldness. Be gentle with yourself "
        "today, and tell me or one person close to you if it stays like this.",
        "Numb is one of the ways grief shows up first. Nothing has to be decided today — "
        "just keep eating and sleeping, and let someone know how you are.",
    ),
    "relief": (
        "Relief after a death is more common than people admit, and it does not cancel the "
        "grief. Say it to someone who will not judge it — that is usually enough to make it "
        "sit easier.",
        "Feeling relief does not make you cold. If they were ill for a long time it is a "
        "normal thing to feel, and it can sit alongside missing them.",
    ),
}


def _feeling(tight):
    for word in tight.split():
        if word in FEELING_WORDS:
            return FEELING_WORDS[word]
    return ""


HELLO_ON_ITS_OWN = re.compile(
    r"^(?:hi+|hey+|hello+|hiya+|yo|howdy|morning|good morning|afternoon|good afternoon|evening|"
    r"good evening|greetings)\b[\s,!.]*"
    r"(?:(?:again|there|all|everyone|everybody|folks|you|mate|love|both)\b[\s,!.]*)*"
    r"(?:(?:how are (?:you|things|you doing|you keeping)|how'?s it going|hows it going|"
    r"how are we|you ok|you alright|hope you'?re well|its me)\b[\s,.!?]*)*$")

HELLO_AFTER = (
    "Hello again. I'm still here - how are you doing today?",
    "Hi. No need to say anything in particular - how are you holding up?",
    "Hello. I'm here whenever you want to talk about it, or about anything else.",
    "Hi again. How has the day been?",
)
TIME_SINCE_REPLIES = (
    "The calendar is a poor measure of it. However long the gap is, it takes the time it takes.",
    "Dates like that come round whether you are ready or not. Whatever it is like on the day, it "
    "is allowed to be like that.",
    "Most people around you will have stopped counting long before you did. That is not you doing "
    "it wrong.",
    "However long it has been, this is not something you are meant to be over by now. Be as "
    "gentle with yourself about it as you would with anybody else.",
    "It tends to come back in waves rather than fade in a straight line. What has it been like "
    "for you lately?",
)
ENDING_SINCE_REPLIES = (
    "The calendar is not the measure of this. However long it has been, it is not a deadline you "
    "are behind on.",
    "Most people are still in pieces at this point and telling nobody. You are not late.",
    "It does not fade in a straight line, so a bad morning now does not mean you went backwards.",
    "Being able to say how long it has been is its own kind of progress, even on a day that hurts.",
    "However long it has been, you are allowed to still mind. That is not you doing it wrong.",
)
_THE_ONE_WHO_LEFT = (
    r"(?:he|she|they|my\s+(?:wife|husband|partner|girlfriend|boyfriend|fiance|fiancee|ex|"
    r"other\s+half|missus|man|woman))")
AN_ENDING = re.compile(
    r"\b(?:broke\s+up\s+with|(?:i|we|they|he|she)\s+(?:just\s+|finally\s+|recently\s+)?broke\s+up|"
    r"break\s+up|breaking\s+up|split\s+up|splitting\s+up|dumped\s+me|"
    r"got\s+dumped|divorced\s+(?:me|him|her)|got\s+divorced|getting\s+divorced|"
    r"walked\s+out\s+on\s+me|" + _THE_ONE_WHO_LEFT + r"\s+left\s+me|"
    r"ended\s+it\s+with\s+me|we\s+are\s+through|we\s+are\s+over)\b", re.I)
A_FEELING_BETTER_ASK = re.compile(
    r"\b(?:how\s+long|when\s+will|(?:will|does|is|can)\s+it(?:\s+ever)?)\b"
    r".{0,45}?\b(?:feel|get|be|stop)\s+(?:better|over\s+it|myself\s+again|back\s+to\s+normal|"
    r"hurting|easier|normal|right|ok|okay)\b", re.I)
ENDING_FEELINGS_REPLIES = (
    "The worst of it usually eases over a few weeks and then comes back in shorter waves. A bad "
    "day a month from now is part of it, not a step back.",
    "There is no set time, and anybody who gives you one is guessing. The mornings usually lift "
    "before the evenings do, and the odd day still catches you.",
    "Most people find the sharp edge goes within a few weeks and the flat days last longer than "
    "the crying ones. If months go by with no good day in them, that is worth talking to someone "
    "about.",
)

_SPAN_COUNT = (
    r"a|an|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|\d{1,2}|few|couple"
    r"|several")
A_SPAN = re.compile(
    r"\b(?:(?:%s)(?:\s+and\s+a\s+half)?\s+(?:day|week|month|year)s?"
    r"(?:\s+and\s+a\s+half)?|half\s+an?\s+(?:day|week|month|year)s?)\b"
    % _SPAN_COUNT, re.I)
A_SPAN_NO_NUMBER = re.compile(
    r"\b(?:a (?:long|good|fair) (?:time|while)|(?:quite )?a while)\b", re.I)
A_SPAN_LEAD = re.compile(
    r"\b(?:been|nearly|almost|just over|over|about|only|coming up|nearly a|a year this week)\b", re.I)
A_SPAN_TAIL = re.compile(
    r"\b(?:now|this week|today|on|ago|already|next week|coming up|marks?\b|marking)\b", re.I)
A_SPAN_ELSEWHERE = re.compile(
    r"\b(?:since|started|stopped|quit|gave up|off work|signed off|been doing|been on|sober|"
    r"smoking|drinking|diet|gym|job|course|school|married|together|moved|live|living|"
    r"rent|paying|treatment|therapy|sober)\b", re.I)


def _how_long_since(tight, words):
    if not tight or len(tight.split()) > 9:
        return False
    if ASK_FORM.search(tight) or "?" in tight:
        return False
    if A_SPAN_ELSEWHERE.search(tight):
        return False
    span = A_SPAN.search(tight)
    if not span:
        span = A_SPAN_NO_NUMBER.search(tight)
    if not span:
        return False
    rest = (tight[:span.start()] + " " + tight[span.end():]).strip()
    if len(rest.split()) + 2 > 6:
        return False
    if not (A_SPAN_LEAD.search(rest) or A_SPAN_TAIL.search(rest) or len(rest.split()) <= 2):
        return False
    return True

MISS_REPLIES = (
    "Of course you do. It goes in waves, and the waves get further apart.",
    "The ones we miss are the ones who mattered. Say as much or as little as you like.",
    "That ache is real, and it doesn't keep office hours. Say more whenever you want to.",
    "Missing like that makes sense. Those days can be long ones — I'm around if talking would "
    "help.",
    "Some days the missing is louder than others. No need to do anything with it here; I'm just "
    "listening.",
)
MISS_SUBJECT = (r"(?:i|we|i'm|im|i've|ive|we're|were|we've|weve)")
MISS_VERB = re.compile(r"\b" + MISS_SUBJECT +
                       r"\s+(?:really\s+|so\s+much\s+|just\s+|properly\s+)?"
                       r"(?:have\s+|been\s+|am\s+|are\s+)?(?:miss|missing)\b"
                       r"|\bmissing\s+(?:my|our)\b", re.I)
MISS_PEOPLE = PEOPLE | frozenset((
    "boyfriend", "girlfriend", "fiance", "fiancee", "twin", "twins", "stepdad", "stepmum",
    "ex", "husband", "wife", "partner", "mates", "flatmate", "roommate", "bestie",
))
MISS_NOUN = re.compile(r"\b(?:my|our|his|her|their)\s+(?:[a-z]+\s+){0,2}(?:" +
                       "|".join(sorted(MISS_PEOPLE, key=len, reverse=True)) + r")\b", re.I)
MISS_NOT_BETWEEN = re.compile(r"\b(?:before|after|without|since|from|during|when|until|like|"
                              r"around|away)\b", re.I)
MISS_TAIL = re.compile(r"^\s*(?:$|[.,;:!?]|\b(?:today|tonight|so much|a lot|loads|terribly|"
                       r"badly|every day|still|again|now|already|lots|heaps|more than ever|"
                       r"like mad|to bits|awfully)\b|\band\b|\bbut\b|\bso\b)", re.I)
MISS_ANIMALS = frozenset("""dog dogs cat cats puppy kitten rabbit hamster budgie parrot horse pony
pet pets tortoise ferret guinea""".split())
MISS_ANIMAL_NOUNS = frozenset("""walker walkers sitter sitters food bed beds bowl bowls lead leads
collar collars toy toys treat treats vet vets breeder breeders groomer groomers blanket blankets
basket baskets door doors lead name""".split())
MISS_PRONOUN = re.compile(r"\b" + MISS_SUBJECT +
                          r"\s+(?:really\s+|so\s+much\s+|just\s+)?"
                          r"(?:have\s+|been\s+|am\s+|are\s+)?(?:miss|missing)\s+"
                          r"(?:him|her|them|mum|dad|nan|gran)\b", re.I)
MISS_NOT = re.compile(r"\b(?:miss|missing)\s+(?:having|being|doing|going|work|working|school|"
                      r"home|the|a|an|me|you)\b", re.I)
ASK_AT_START = re.compile(r"^\s*(?:do|does|will|would|did|are|is|have|has|can|could|should)\b", re.I)


def _missing_someone(text):
    if not MISS_VERB.search(text):
        return False
    if ASK_AT_START.match(text) or "?" in text:
        return False
    noun = MISS_NOUN.search(text)
    if noun and MISS_NOT_BETWEEN.search(noun.group(0)):
        noun = None
    if not (noun or MISS_PRONOUN.search(text)):
        return False
    if MISS_NOT.search(text):
        return False
    found = noun or MISS_PRONOUN.search(text)
    if noun and not MISS_TAIL.match(text[found.end():]):
        rest = text[found.end():].strip()
        animal = found.group(0).split()[-1].lower() in MISS_ANIMALS
        named = re.match(r"([A-Za-z]+)([.!?]?)(.*)$", rest)
        if not (animal and named and named.group(1).lower() not in MISS_ANIMAL_NOUNS
                and MISS_TAIL.match(named.group(3))):
            return False
    return True


FEELING_STATES = frozenset((
    "guilt", "guilty", "ashamed", "shame", "sad", "sadness", "angry", "anger", "furious", "rage",
    "numb", "relief", "relieved", "lonely", "empty", "hopeless", "anxious", "anxiety", "worried",
))
FEELING_ASK = re.compile(r"\bhow (?:do|can|could|should) i (?:stop|deal with|cope with|get rid of|"
                         r"handle|manage)\b|\bi (?:just |really |still |keep )?feel(?:ing)?\b", re.I)
FEELING_ONLY_WORDS = frozenset("""how do does can could should would i me my im am is are was
what when it this that the a an so really still just very much anymore again now bad worse better
feel feels feeling stop deal with cope get rid of handle manage about over like why""".split())


FEELING_PERSON_WORDS = frozenset((
    "he", "she", "him", "her", "hers", "they", "them", "their", "theirs", "his", "who",
)) | MISS_PEOPLE


def _a_question_about_the_feeling(line, words):
    if not FEELING_ASK.search(line):
        return False
    if not (words & FEELING_STATES):
        return False
    return not (words - FEELING_STATES - FEELING_ONLY_WORDS - FEELING_PERSON_WORDS)


GRIEF_SELF = frozenset((
    "hard", "hardest", "tough", "rough", "bad", "awful", "horrible", "heavy", "hurts", "hurt",
    "sleep", "sleeping", "sleepless", "slept", "bed", "nights", "night", "wake", "wakes",
    "woke", "tired", "exhausted", "weird", "strange", "stuck", "empty", "quiet", "silent",
    "silence", "coping", "cope", "eating", "appetite", "mornings", "morning",
    "struggling", "struggle", "breaking", "broken", "withdrawn", "shut", "drinking",
    "unbearable",
))
FAMILY = frozenset(("mum", "mom", "mam", "dad", "mother", "father", "brother", "sister",
                    "son", "daughter", "wife", "husband", "partner", "nan", "nana", "grandad",
                    "grandma", "grandpa", "granny", "gran", "uncle", "aunt", "auntie", "cousin",
                    "family", "parents", "kids", "children", "baby"))
SELF_OPENERS = (
    "i ", "i'", "im ", "ime ", "ive ", "id ", "some days", "some nights", "most days",
    "most nights", "every night", "at night", "lately", "these days", "it ", "it's ", "its ",
    "that ", "that's ", "this ", "they ", "we ", "we're ",
)
SELF_NOUNS = frozenset(("sleep", "night", "nights", "mornings", "mood", "head", "appetite",
                        "grief", "sadness", "coping"))
WHEN_WORDS = frozenset(("this", "last", "next", "tomorrow", "yesterday", "every", "one", "that"))
GRIEF_REFERRING = ("is that normal", "is it normal", "is this normal", "does it get better",
                   "will it get better", "does it ever stop", "when does it stop",
                   "how long does it last", "does it get easier", "will it always",
                   "feel lost", "so lost", "feel empty", "feel numb")
GRIEF_POINTS_BACK = re.compile(
    r"^(?:so\s+|and\s+|but\s+)?"
    r"(?:does|did|will|would|is|was|am"
    r"|when\s+(?:does|did|will|would|is|am)"
    r"|how\s+long\s+(?:does|did|will|would|is|am))"
    r"\s+(?:it|that|this|i|things|the\s+pain|the\s+ache|this\s+pain)\b"
    r"(?:\s+(?:ever|always|still|really|actually|never|not))?\s*"
    r"(?:stop|end|ease|pass|fade|last|go\s+away|let\s+up|get\s+easier|get\s+better|"
    r"feel\s+better|feel\s+normal|feel\s+like\s+myself|"
    r"hurt|hurts|hurting|normal|better|easier|forever)"
    r"(?:\s+(?:hurting|aching))?\b"
    r"(?:\s+(?:so|then|eventually|now|at\s+some\s+point|after\s+a\s+while|for\s+ever"
    r"|some\s*day))?\s*[.?!]*$",
    re.I)
GRIEF_OBJECTS = ("without her", "without him", "without them", "her things", "his things",
                 "the house", "the flat", "her room", "his room", "empty house", "quiet house")
REFERS_TO_THEM = re.compile(r"\b(?:him|her|them|his|hers|their)\b")
IDEA_ASK = re.compile(r"^(?:what|how|where|which)\b.*\b(?:do|does|could|should|can|would|shall)\b")
THREAD_TOPICS = frozenset(("feelings", "grief", "loss", "small-talk", "sleep", "pets"))

THEM = (r"(?:him|her|them|he|she|they|hes|shes|theyre|his|hers|their|mum|mom|mam|dad|father|"
        r"mother|nan|gran|granny|nana|grandad|granddad|grandma|grandpa|son|daughter|brother|"
        r"sister|wife|husband|partner|baby|friend|uncle|aunt|cousin|dog|cat|puppy|kitten)")
ABSENCE = re.compile(
    r"\b(?:keep|keeps|kept|still)\s+(?:expecting|expect|looking|look|waiting|wait|listening|"
    r"listen|hearing|hear|seeing|see|reaching|reach|thinking|think|setting|set|saving|saved)\b"
    r"[^.]{0,30}\b" + THEM + r"\b|"
    r"\b(?:habit|instinct|reflex|second nature)\b|"
    r"\b(?:house|home|flat|kitchen|bed|place|room)\s+(?:feels|felt|is|was)\s+"
    r"(?:so\s+|too\s+|very\s+)?(?:empty|quiet|silent|big|strange|wrong)\b|"
    r"\b(?:set|laid|lay|set out|lay out)\s+(?:the\s+|a\s+)?table for (?:two|three|four)\b|"
    r"\bfor(?:got|get|gets|getting)\b[^.]{0,30}\b(?:gone|dead|not here|isnt here|wouldnt be"
    r" here)\b|"
    r"\b(?:hear|hearing|smell|smelling)\s+(?:his|her|their)\b")
STILL_LAYING = re.compile(
    r"\b(?:set|setting|lay|laying|laid)\s+(?:out\s+)?(?:the\s+|a\s+)?table\s+for\s+"
    r"(?:two|three|four)\b|"
    r"\b(?:lay|laying|laid|set|setting|put|putting)\s+(?:out\s+)?(?:\w+\s+){0,3}"
    r"(?:place|places|bowl|bowls|plate|plates|cup|cups)\b(?:\s+\w+){0,4}\s+for\s+(?:two|three)\b|"
    r"\b(?:keep|keeps|still)\s+(?:\w+\s+){0,2}(?:set|setting|put|putting|lay|laying|buy|buying)\b"
    r"[^.]{0,24}\b(?:bowls?|places?|plates?|cups?|mugs?|glasses|food|biscuits?|treats?)\b|"
    r"\b(?:keep|keeps|kept|still)\s+(?:\w+\s+){0,3}"
    r"(?:make|making|made|pour|pouring|poured|buy|buying|bought|cook|cooking|cooked|dish|"
    r"dishing|fill|filling|cut|cutting|butter|buttering|boil|boiling)\b"
    r"[^.]{0,24}\b(?:two|three|both)\b|"
    r"\b(?:two|three|both)\s+(?:cups?|mugs?|teas?|coffees?|plates?|bowls?|portions?|"
    r"helpings?|sandwiches?|glasses)\b[^.]{0,24}\b(?:for (?:us|two|both of us)|still)\b", re.I)
STILL_WITHOUT = re.compile(
    r"\b(?:empty|quiet|silent)\s+without\s+(?:my|our|him|her|them)\b", re.I)
STILL_CRYING = re.compile(
    r"\b(?:cry|cries|cried|crying)\s+(?:over|about|for)\s+(?:my|our|him|her|them)\b|"
    r"\b(?:cant|cannot|can'?t)\s+stop\s+(?:cry\w*|think\w*)\s+(?:about|over|for)\s+"
    r"(?:my|our|him|her|them)\b", re.I)
STILL_AT_THE_DOOR = re.compile(
    r"\b(?:keep|keeps|kept|still)\s+(?:\w+\s+){0,2}"
    r"(?:looking|look|listening|listen|waiting|wait|reaching|reach|expecting|expect|setting|set)\b"
    r"[^.]{0,30}\b(?:door|doorbell|phone|key|keys|ring(?:ing)?|places?|table|seat)\b", re.I)
STILL_SEEING = re.compile(
    r"\b(?:keep|keeps|kept|still)\s+(?:\w+\s+){0,3}"
    r"(?:expect\w*|looking|look|waiting|wait|listening|listen|hearing|hear|seeing|see|"
    r"reaching|reach|saving|saved)\b[^.]{0,30}\b" + THEM + r"\b", re.I)
THE_ROUTINE_REPLIES = (
    "The hands keep the routine for a while - the second bowl, the place at the table. That is "
    "muscle memory, not madness, and you can let it go when it stops being a comfort.",
    "Laying it out for them is the routine still running. Put it away when you want to, not "
    "because anyone says it is time.",
    "Half of it is the small jobs your hands still do. There is nothing wrong with any of them.",
)
THE_JOBS_FOR_THEM_REPLIES = (
    "The jobs you did for them do not stop on the day. The hands keep going for a while, and that "
    "is not a sign you are stuck.",
    "Some part of the day is still theirs. Doing the job anyway is how a lot of people get "
    "through the first year, and there is nothing wrong with it.",
    "A habit that was for them takes a while to notice as a habit. Do it, or stop, whichever "
    "comes first - neither is a betrayal of them.",
)
THE_HOUSE_REPLIES = (
    "An empty house is the hardest part of the day to fill. It does get less loud, and the quiet "
    "is not a measure of anything.",
    "The quiet is the whole of it, and it is worst in the evenings. Nobody gets to tell you there "
    "is a timetable for that.",
    "A house with one fewer person in it feels wrong before it feels like anything else. Be slow "
    "with it.",
)
THE_CANNOT_STOP_REPLIES = (
    "Crying over them, or thinking of nothing else, is the plainest way of saying they mattered. "
    "It comes in waves - let it, and be kind to yourself after.",
    "If that is all you can do today, it is enough for today. It eases, and it keeps its own "
    "timetable.",
    "That is grief doing its work, and it is not something to get on top of. I am here for as "
    "much of it as you want to say.",
)
THE_HABIT_REPLIES = (
    "Seeing them out of the corner of your eye is the habit outliving them. Most people who have "
    "lost someone do it for months, and it says nothing about how you are.",
    "Seeing them, hearing them, waiting for them - it is a habit that had years to set. It fades "
    "slowly, and it is not a sign you are losing them.",
    "That reflex is the shape of them still in your day. There is nothing to do about it, and it "
    "goes with how much of the day they were in.",
)


def _an_ask_in_the_line(line):
    if ASK_AT_START.match(line):
        return True
    return bool(re.search(r"\b(?:should|shall|do|does|did|can|could|would|will|is|are|was|were|"
                          r"why|how|what|when|where|who)\s+(?:i|we|you|he|she|they|it)\b", line))


STILL_DOING_FOR_THEM = re.compile(
    r"\b(?:keep|keeps|kept|still)\s+(?:\w+\s+){0,3}"
    r"(?:make|making|pour|pouring|buy|buying|cook|cooking|dish|dishing|lay|laying|set|setting|"
    r"put|putting|save|saving|leave|leaving|wash|washing|iron|ironing|fold|folding|"
    r"call|calling|text|texting|ring|ringing|phone|phoning|greet|greeting|kiss|kissing|"
    r"say|saying|check|checking|fill|filling|clean|cleaning|top|topping|pay|paying|paid|"
    r"do|doing)\b"
    r"[^.]{0,30}\b(?:his|her|their|him|them|hers|theirs)\b", re.I)


HABIT_PATTERNS = ((STILL_LAYING, THE_ROUTINE_REPLIES),
                  (STILL_DOING_FOR_THEM, THE_JOBS_FOR_THEM_REPLIES),
                  (STILL_WITHOUT, THE_HOUSE_REPLIES),
                  (STILL_CRYING, THE_CANNOT_STOP_REPLIES),
                  (STILL_SEEING, THE_HABIT_REPLIES),
                  (STILL_AT_THE_DOOR, THE_HABIT_REPLIES))
def _still_here(line, words):
    if "?" in line or QUESTION.search(line):
        return None
    if _an_ask_in_the_line(line):
        return None
    if MISS_NOT.search(line) or _a_thing_of_theirs(words):
        return None
    if _only_the_proceedings(" ".join(words), words):
        return None
    for pattern, pool in HABIT_PATTERNS:
        if pattern.search(line):
            return pool
    return None


def _a_habit_in(line):
    return any(pattern.search(line) for pattern, _pool in HABIT_PATTERNS)


AFTER_REPLIES = (
    "I'm here. Take your time with it — tell me what it has been like, if you want to.",
    "There's no rush to talk about it. I'm here when you want to say more.",
    "That sounds heavy to be carrying. I'm listening, however much or little you want to say.",
    "I'm glad you said that out loud. Say as much or as little as you like — I'm here.",
)
GRIEF_FEELINGS = frozenset((
    "miss", "missing", "cry", "crying", "cried", "tears", "numb", "sad", "lonely", "angry",
    "guilty", "guilt", "grief", "grieving", "mourning", "funeral", "ashes", "grave",
    "anniversary", "reminded", "memories", "remember", "shock", "shocked", "unreal",
    "bereaved", "gutted",
    "waves",
    "dream", "dreams", "dreamt", "dreamed", "dreaming", "voice", "smell", "doorbell",
    "photo", "photos",
))
GRIEF_SELF = frozenset((
    "hard", "hardest", "tough", "rough", "bad", "awful", "horrible", "heavy", "hurts", "hurt",
    "sleep", "sleeping", "sleepless", "slept", "bed", "nights", "night", "wake", "wakes",
    "woke", "tired", "exhausted", "weird", "strange", "stuck", "empty", "quiet", "silent",
    "silence", "coping", "cope", "eating", "appetite", "mornings", "morning",
    "struggling", "struggle", "breaking", "broken", "withdrawn", "shut", "drinking",
    "unbearable",
))
FAMILY = frozenset(("mum", "mom", "mam", "dad", "mother", "father", "brother", "sister",
                    "son", "daughter", "wife", "husband", "partner", "nan", "nana", "grandad",
                    "grandma", "grandpa", "granny", "gran", "uncle", "aunt", "auntie", "cousin",
                    "family", "parents", "kids", "children", "baby"))
SELF_OPENERS = (
    "i ", "i'", "im ", "ime ", "ive ", "id ", "some days", "some nights", "most days",
    "most nights", "every night", "at night", "lately", "these days", "it ", "it's ", "its ",
    "that ", "that's ", "this ", "they ", "we ", "we're ",
)
SELF_NOUNS = frozenset(("sleep", "night", "nights", "mornings", "mood", "head", "appetite",
                        "grief", "sadness", "coping"))
WHEN_WORDS = frozenset(("this", "last", "next", "tomorrow", "yesterday", "every", "one", "that"))
GRIEF_REFERRING = ("is that normal", "is it normal", "is this normal", "does it get better",
                   "will it get better", "does it ever stop", "when does it stop",
                   "how long does it last", "does it get easier", "will it always",
                   "feel lost", "so lost", "feel empty", "feel numb")
GRIEF_POINTS_BACK = re.compile(
    r"^(?:so\s+|and\s+|but\s+)?"
    r"(?:does|did|will|would|is|was|am"
    r"|when\s+(?:does|did|will|would|is|am)"
    r"|how\s+long\s+(?:does|did|will|would|is|am))"
    r"\s+(?:it|that|this|i|things|the\s+pain|the\s+ache|this\s+pain)\b"
    r"(?:\s+(?:ever|always|still|really|actually|never|not))?\s*"
    r"(?:stop|end|ease|pass|fade|last|go\s+away|let\s+up|get\s+easier|get\s+better|"
    r"feel\s+better|feel\s+normal|feel\s+like\s+myself|"
    r"hurt|hurts|hurting|normal|better|easier|forever)"
    r"(?:\s+(?:hurting|aching))?\b"
    r"(?:\s+(?:so|then|eventually|now|at\s+some\s+point|after\s+a\s+while|for\s+ever"
    r"|some\s*day))?\s*[.?!]*$",
    re.I)
GRIEF_OBJECTS = ("without her", "without him", "without them", "her things", "his things",
                 "the house", "the flat", "her room", "his room", "empty house", "quiet house")
REFERS_TO_THEM = re.compile(r"\b(?:him|her|them|his|hers|their)\b")
IDEA_ASK = re.compile(r"^(?:what|how|where|which)\b.*\b(?:do|does|could|should|can|would|shall)\b")
THREAD_TOPICS = frozenset(("feelings", "grief", "loss", "small-talk", "sleep", "pets"))

THEM = (r"(?:him|her|them|he|she|they|hes|shes|theyre|his|hers|their|mum|mom|mam|dad|father|"
        r"mother|nan|gran|granny|nana|grandad|granddad|grandma|grandpa|son|daughter|brother|"
        r"sister|wife|husband|partner|baby|friend|uncle|aunt|cousin|dog|cat|puppy|kitten)")
ABSENCE = re.compile(
    r"\b(?:keep|keeps|kept|still)\s+(?:expecting|expect|looking|look|waiting|wait|listening|"
    r"listen|hearing|hear|seeing|see|reaching|reach|thinking|think|setting|set|saving|saved)\b"
    r"[^.]{0,30}\b" + THEM + r"\b|"
    r"\b(?:habit|instinct|reflex|second nature)\b|"
    r"\b(?:house|home|flat|kitchen|bed|place|room)\s+(?:feels|felt|is|was)\s+"
    r"(?:so\s+|too\s+|very\s+)?(?:empty|quiet|silent|big|strange|wrong)\b|"
    r"\b(?:set|laid|lay|set out|lay out)\s+(?:the\s+|a\s+)?table for (?:two|three|four)\b|"
    r"\bfor(?:got|get|gets|getting)\b[^.]{0,30}\b(?:gone|dead|not here|isnt here|wouldnt be"
    r" here)\b|"
    r"\b(?:hear|hearing|smell|smelling)\s+(?:his|her|their)\b")
REASSURING = re.compile(
    r"\b(?:the right (?:thing|call|decision)|did the (?:right|kindest|best) thing|for the best|"
    r"the kindest thing|no other choice|"
    r"(?:he|she|they) had a good (?:life|innings)|would(?:'ve| have) wanted|at peace|"
    r"no more pain|not in pain|out of (?:his|her|their) pain|no longer suffering)\b")

PEACE_IS_MINE = re.compile(
    r"\b(?:i|we)(?:'?m|'?ve|\s+am|\s+are|\s+have|\s+feel|\s+feeling|\s+felt)?\s+"
    r"(?:now\s+|so\s+|really\s+|quite\s+|a bit\s+|more\s+)*at (?:peace|rest)\b")
WOULD_HAVE = re.compile(
    r"\bwould\s+(?:have|ve)\s+(?:been|turned)\s+(?:\d{1,3}\b|twenty|thirty|forty|fifty|"
    r"sixty|seventy|eighty|ninety)")
OCCASION = re.compile(
    r"\b(birthday|birthdays|xmas|christmas|anniversary|anniversaries|mothers day|mothering "
    r"sunday|fathers day|new year|new years|easter|the day itself|her day|his day|their day)\b")
WITHOUT = re.compile(r"\bwithout\s+(?:my|our|his|her|them|him|mum|dad)\b")
TRADITION = re.compile(
    r"\b(we always|always did|always had|every year|used to|tradition|same as always|instead|"
    r"what do i do|dont know what to do|don t know what to do|nothing feels right)\b")
STILL_KEEP = re.compile(
    r"\b(?:should i|shall i|do you think i should|am i supposed to|is it (?:ok|okay|alright|"
    r"wrong) (?:to|if i))\s+still\s+"
    r"(?:do|have|bake|cook|make|put|keep|send|host|hang|light|set out|visit)\b"
    r"|\bis it (?:ok|okay|alright|wrong) to (?:put up|put|do|keep|hang) (?:the|a|our) "
    r"(?:tree|decorations|lights|wreath|cake|cards?)\b")
DAY_THING = re.compile(
    r"\b(cakes?|tree|dinner|lunch|meal|roast|turkey|cards?|presents?|gifts?|decorations|wreath|"
    r"flowers|party|tradition|toast|grave|christmas|xmas|birthday|anniversary)\b")
DAY_QUESTION = re.compile(r"\b(?:what|how)\s+(?:should|do|can|could)\s+(?:i|we)\s+"
                          r"(?:do|mark|handle|spend|keep)\b")
KEEPS = (TRADITION, STILL_KEEP)

FUNERAL = re.compile(r"\b(funeral|memorial|service|viewing|burial|cremation)\b")

FUNERALS = re.compile(r"\b(?:funerals|memorials|burials|cremations|crematoria|crematorium|"
                      r"graveside|gravesides)\b")

TELL_CHILD = re.compile(
    r"\b(?:tell|telling|explain|explaining|talk to|talking to)\b([\w\s]{0,24}?)"
    r"\b(?:child|children|kid|kids|son|daughter|toddler|boy|girl|baby|teenager)\b")
YEAR_OLD = re.compile(r"\d+\s*(?:year|yr)s?[\s-]*old")


def _telling_a_child(tight):
    found = TELL_CHILD.search(tight)
    if not found:
        return bool(YEAR_OLD.search(tight) and re.search(r"\b(?:tell|explain)\w*\b", tight))
    between = found.group(1) or ""
    if re.search(r"\b(?:about|of|people|everyone|office|work|boss)\b", between):
        return False
    return True


PRONOUN = frozenset(("he", "she", "they", "him", "her", "them"))


def marks_a_day(text, known=False):
    if isinstance(text, str):
        raw = " ".join(_plain(text))
        words = raw.split()
    else:
        words = list(text or ())
        raw = " ".join(words)
    tight = " ".join(word for word in words if word not in FILLERS)
    subject = _has_person(words) or bool(set(words) & PRONOUN)
    if WOULD_HAVE.search(tight):
        return subject
    day_named = bool(DAY_THING.search(raw) or OCCASION.search(tight) or _has_person(words))
    if known and ((TRADITION.search(tight) and day_named)
                  or (STILL_KEEP.search(raw) and DAY_THING.search(raw))
                  or (DAY_QUESTION.search(tight) and day_named)):
        return True
    if not OCCASION.search(tight):
        return False
    if WITHOUT.search(tight):
        return True
    return False


ASKS_ABOUT_THE_DAY = re.compile(
    r"\b(what (?:do|should|can|could) i|what (?:do|would) we|should i|shall i|how do i|how can i|"
    r"should we|shall we|do we|would we|can we|could we|how do we|"
    r"any ideas?|what to do|instead|nothing feels right|dont know|don t know|do you think|"
    r"is it (?:ok|okay|alright|wrong)|am i supposed to)\b")


def asks_what_to_do(text):
    if isinstance(text, str):
        raw = " ".join(_plain(text))
        words = raw.split()
    else:
        words = list(text or ())
        raw = " ".join(words)
    if "?" in str(text or ""):
        return True
    return bool(ASKS_ABOUT_THE_DAY.search(raw))


def _plain(text):
    text = str(text or "").lower().replace("\u2019", "'")
    return [word.strip(".,!?;:\"'()") for word in text.split()]


def _about_them(line):
    text = (line or "").strip()
    if text.startswith(SELF_OPENERS):
        return True
    words = text.split()
    return len(words) > 1 and words[0] == "my" and words[1].strip(",.!?") in SELF_NOUNS


def _about_family(words):
    return len(words) > 1 and words[0] in ("my", "his", "her", "their", "our") and any(
        word.strip(",.!?") in FAMILY for word in words[1:3])


def _own_state(words):
    for index, word in enumerate(words):
        if word in GRIEF_SELF and not (index and words[index - 1] in WHEN_WORDS):
            return True
    return False


TIME_OF_DAY = re.compile(r"^\s*the\s+(?:mornings?|nights?|evenings?|weekends?|days?)\b")
STATE_TAIL = frozenset((
    "and", "but", "or", "so", "too", "all", "at", "in", "on", "to", "with", "when", "since",
    "because", "today", "tonight", "now", "still", "lately", "already", "again", "yet", "just",
    "quite", "very", "really", "bit", "as", "like", "about", "for", "of", "that", "it", "i",
    "im", "i'm", "this", "these", "some", "most", "every", "days", "day", "weeks", "week",
    "months", "time", "times", "though", "honestly", "actually", "sometimes", "if", "than",
    "without", "after", "before", "anymore", "any", "more", "less", "enough",
))


def _state_describes_them(words):
    for index, word in enumerate(words):
        if word in GRIEF_SELF and (index + 1 >= len(words) or words[index + 1] in STATE_TAIL):
            return True
    return False


BODY_STATE = frozenset((
    "eat", "eats", "ate", "eating", "appetite", "hungry", "food", "meal", "meals",
    "drink", "drinks", "drank", "drinking", "alcohol", "wine",
    "sleep", "sleeps", "sleeping", "slept", "weight", "cry", "crying",
))
THEMSELVES = re.compile(r"\b(?:i|im|i'm|me|my|myself)\b")
ASK_NORMAL = re.compile(r"^is (?:it|that) normal\b")
NORMAL_TO_FEEL = re.compile(r"^is (?:it|that|this) (?:normal|ok|okay|common|usual) to feel\b")
QUANTITY = re.compile(r"\bhow (?:much|many)\b")


def _the_body_is_theirs(tight, words):
    if QUANTITY.search(tight):
        return False
    if NORMAL_TO_FEEL.match(tight):
        return True
    if not (THEMSELVES.search(tight) or ASK_NORMAL.match(tight)):
        return False
    words = tuple(words)
    for index, word in enumerate(words):
        if word in BODY_STATE and (index + 1 >= len(words) or words[index + 1] in STATE_TAIL):
            return True
    return False


MEASURE_TOPICS = frozenset(("maths-and-numbers",))


BODY_ANSWER = frozenset((
    "eat", "eats", "ate", "eating", "appetite", "hungry", "food", "meal", "meals",
    "drink", "drinks", "drank", "drinking", "thirsty",
    "sleep", "sleeps", "sleeping", "slept", "wake", "wakes", "waking", "woke", "awake",
    "insomnia", "tired", "weight",
))


def _a_body_with_its_own_answer(tight, words):
    if QUANTITY.search(tight):
        return False
    if not THEMSELVES.search(tight):
        return False
    return any(word in BODY_ANSWER for word in words)


def _names_a_subject(topics):
    if not isinstance(topics, (list, tuple)) or not topics:
        return False
    return bool(set(topics) - THREAD_TOPICS - MEASURE_TOPICS)


def _own_subject(topics):
    if not isinstance(topics, (list, tuple)) or not topics:
        return False
    return bool(set(topics) - THREAD_TOPICS)


STILL_ABOUT_THEM = re.compile(
    r"\b(?:he|she|him|her|they|them|his|hers|their|theirs)\b"
    r"|\b(?:keep|keeps|kept|still|always|expect|expecting|used to|every (?:day|night|year)|"
    r"last (?:week|month|year)|anniversary|birthday|that (?:day|night|song|photo|place))\b", re.I)


ABOUT_THEM_OPENS = re.compile(
    r"^\s*(?:(?:and|but|so|yeah|yes|oh|well|then|also|plus|too|god|honestly)\b[\s,]*)*"
    r"(?:he|she|they|him|her|his|their|them|theyre|he's|she's|he'd|she'd|they'd|hes|shes)\b",
    re.I)
MISSING_SAID_AGAIN = re.compile(
    r"\b(?:miss|missed|misses|missing|cry|cried|crying|tears|sad|sadness|ache|aches|aching|"
    r"keep|keeps|kept|still|always|expect|expecting|hard|hardest|heavy|hurts?)\b", re.I)


def _hands_over_a_detail(tight):
    return bool(ABOUT_THEM_OPENS.match(tight) and not MISSING_SAID_AGAIN.search(tight))


def _thread_pool(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    if not turns:
        return None
    last = str(turns[-1].get("bot") or "")
    if not last:
        return None
    if last in SAY_REPLIES:
        return SAY_REPLIES
    if last in MISS_REPLIES:
        return MISS_REPLIES
    return None


_CONTRACTED = re.compile(
    r"\b(\w+)['\u2019]?s\s+(?=(?:dying|terminal|terminally|palliative|"
    r"in\s+(?:a\s+)?hospice)\b)")
_PEOPLE_PRONOUNS = frozenset(("she", "he", "they", "someone", "anyone", "everyone", "nobody",
                              "who"))
DYING_TO = re.compile(r"\bdying\s+to\b|\bdying\s+for\b|\bdying\s+of\s+(?:boredom|"
                      r"embarrassment|laughter|curiosity|shame|excitement|a\s+cold)\b")
_NOT_A_CONTRACTION = frozenset(("is", "was", "has", "does", "this", "its", "his", "hers", "ours",
                                "theirs"))
_CAN_BE_DYING = frozenset(PEOPLE) | _PEOPLE_PRONOUNS


def _spoken(text):
    def spell(match):
        base = match.group(1).lower()
        if base in _CAN_BE_DYING and base + "s" not in _NOT_A_CONTRACTION:
            return match.group(1) + " is "
        return match.group(0)

    return _CONTRACTED.sub(spell, text)


def _tight(text):
    return " ".join(word for word in _plain(text) if word not in FILLERS)


def _their_thing_after(clean, start):
    rest = clean[start:].split()
    return bool(rest) and rest[0] in (OBJECTS | THEIRS)


def _another_person(words, clean):
    if set(words) & (HUMAN_WORDS - TWO_WAY_ROLES):
        return True
    return bool(ROLE_PHRASE.search(clean))


def _a_thing_of_theirs(words):
    for index, word in enumerate(words):
        if index + 1 >= len(words) or words[index + 1] not in (OBJECTS | THEIRS):
            continue
        stem = word[:-2] if word.endswith("'s") else (word[:-1] if word.endswith("s") else word)
        if word not in PEOPLE and stem not in PEOPLE:
            continue
        others = [other for place, other in enumerate(words)
                  if place != index
                  and (other in PEOPLE
                       or (len(other) > 2 and other.endswith("s") and other[:-1] in PEOPLE))]
        if not others:
            return True
    return False


def _a_role_phrase(clean):
    return bool(ROLE_PHRASE.search(clean))


def _has_person(words):
    for word in words:
        if word in PEOPLE:
            return True
        if word.endswith("'s") and word[:-2] in PEOPLE:
            return True
        if word.endswith("s") and word[:-1] in PEOPLE:
            return True
    for first, second in PEOPLE_PHRASES:
        for index, word in enumerate(words[:-1]):
            if word == first and words[index + 1] == second:
                return True
    return _a_role_phrase(" ".join(words))


def _object_died(words):
    for index, word in enumerate(words):
        if word in ("died", "dies", "dead", "dying") and index:
            if words[index - 1] in OBJECTS:
                return True
            if index > 1 and words[index - 2] in OBJECTS and words[index - 1] in ("is", "was",
                                                                                "has", "had"):
                return True
    return False


FINDABLE = (r"keys?|key ?ring|phone|mobile|wallet|purse|handbag|backpack|rucksack|bag|passport|"
            r"tickets?|(?:(?:bank|debit|credit|travel|id|library) )?cards?|glasses|specs|"
            r"headphones|earphones|earbuds|airpods|charger|laptop|tablet|mouse|umbrella|"
            r"coat|jacket|scarf|glove|hat|shoes|trainers|book|file|documents?|parcel|package|"
            r"remote|toy|teddy")
LOST_THING_TO_FIND = re.compile(
    r"\b(?:i|we|ive|i've|he|she|they|you|my [a-z]+|our [a-z]+)\s+"
    r"(?:have\s+|had\s+)?(?:lost|losing)\s+"
    r"(?:my|our|his|her|their|your|the|a|an)\s+(?:" + FINDABLE + r")\b")
CANT_FIND_THING = re.compile(
    r"\b(?:(?:i|we|he|she|they)\s+)?(?:can ?not|can't|cant|couldn't|could not)\s+"
    r"(?:find|see)\s+"
    r"(?:my|our|his|her|their|the|a|an)\s+(?:" + FINDABLE + r")\b")
LEFT_THING = re.compile(
    r"\b(?:i|we|he|she|they)(?:\s+think i)?\s+(?:left|forgot|lost track of)\s+"
    r"(?:my|our|his|her|their|the|a|an)\s+(?:" + FINDABLE + r")\b")
REMEMBER_NOT_WHERE = re.compile(
    r"\b(?:forgot|forget|can ?not remember|can't remember|cant remember|do not remember|"
    r"don't remember|dont remember|no idea|not sure|no clue)\s+where\s+(?:i|we|he|she|they)\s+"
    r"(?:have\s+|had\s+)?(?:put|left|laid|placed)\s+"
    r"(?:my|our|his|her|their|the|a|an)\s+(?:" + FINDABLE + r")\b")
KEEP_LOSING_THING = re.compile(
    r"\b(?:i|we)\s+keep\s+(?:losing|misplacing)\s+(?:my|our|the)\s+(?:" + FINDABLE + r")\b")
KEPT_GOING_MISSING = re.compile(
    r"\b(?:my|our|his|her|their|the)\s+(?:" + FINDABLE + r")\s+"
    r"(?:keeps?|kept)\s+(?:going\s+missing|disappearing|vanishing|getting\s+lost|walking)\b")
GONE_THING = re.compile(
    r"\b(?:my|our|his|her|their)\s+(?:" + FINDABLE + r")\s+(?:is|are|has gone|have gone)\s+"
    r"(?:gone|missing|nowhere)\b")
WHERE_IS_THING = re.compile(
    r"\b(?:where(?:'s| is| are)|where has|where have|where did i (?:put|leave)|"
    r"where have i put|have you seen|has anyone seen|"
    r"did you see|any sign of)\s+(?:my|our|his|her|their|the|a|an)\s+(?:" + FINDABLE + r")\b")
WHERE_I_PUT_IT = re.compile(
    r"\bwhere\s+(?:did|have|has|had)\s+i\s+(?:put|leave)\b"
    r"(?:\s+(?:my|our|his|her|their|the|a|an))?")
NOT_MISLAID = PEOPLE | frozenset((
    "job", "jobs", "shift", "shifts", "foot", "feet", "finger", "fingers", "hand", "hands",
    "mind", "way", "place", "bins", "bin", "rubbish", "washing", "recycling", "ironing",
    "football", "weight", "effort", "record", "case"))
NOT_A_THING_NEXT = frozenset((
    "out", "away", "back", "down", "off", "and", "but", "or", "so", "then", "i", "it", "was",
    "were", "is", "are", "that", "this", "for", "to", "in", "on", "at", "with", "from", "again",
    "somewhere", "before", "after", "today", "yesterday", "last", "now", "though", "honestly",
    "probably", "right", "anyway"))


def _where_i_put_it(said):
    for match in WHERE_I_PUT_IT.finditer(said):
        rest = said[match.end():].split()
        if rest and rest[0] in NOT_MISLAID:
            if len(rest) == 1 or rest[1] in NOT_A_THING_NEXT:
                continue
        return True
    return False
WHERE_IS_THING_BARE = re.compile(
    r"^\s*(?:so |ok |okay |and |but )?where\s+(?:my|our|his|her|their|the|a|an)\s+(?:"
    + FINDABLE + r")\s*$")


LOCKED_OUT = re.compile(
    r"\b(?:locked out|lock(?:ed)? (?:me|myself|us) out|shut out of (?:the|my|our) "
    r"(?:flat|house|home|car|van)|keys? (?:are |is )?(?:still )?(?:in|inside) (?:the|my) "
    r"(?:door|lock|ignition)|lock(?:ed)? (?:my|the) keys? (?:in|inside) (?:the|my) "
    r"(?:car|van|house|flat|boot|door)|no spare key)\b")
NOT_A_DOOR = re.compile(
    r"\b(?:account|email|e-mail|bank|banking|online|app|website|site|password|login|log in|"
    r"profile|facebook|instagram|twitter|whatsapp|icloud|google|netflix|laptop|computer|"
    r"phone|tablet|xbox|playstation|steam|psn|system|server|admin|router|wifi|"
    r"cat|dog|puppy|kitten|pet|bird|hen|chicken|rabbit|hamster)\b")
CAR_LOCK_OUT = re.compile(r"\b(?:car|van|boot|ignition|keys? (?:are |is )?in the (?:car|van))\b")


def locked_out(text):
    said = " ".join(words_of(text))
    if not LOCKED_OUT.search(said):
        return False
    return not NOT_A_DOOR.search(said)


def locked_out_of_the_car(text):
    return bool(CAR_LOCK_OUT.search(" ".join(words_of(text))))


def _readable(text):
    try:
        read = normalise(str(text or ""))
    except Exception:
        return str(text or "")
    return " ".join(read.get("norm") or []) or str(text or "")


def lost_thing_to_find(text):
    said = " ".join(words_of(_readable(text)))
    return bool(LOST_THING_TO_FIND.search(said) or CANT_FIND_THING.search(said)
                or WHERE_IS_THING.search(said) or _where_i_put_it(said)
                or WHERE_IS_THING_BARE.search(said)
                or LEFT_THING.search(said)
                or GONE_THING.search(said) or KEEP_LOSING_THING.search(said)
                or REMEMBER_NOT_WHERE.search(said))


FOUND_WHAT_WAS_LOST = re.compile(
    r"\b(?:found (?:them|it|ours|his|hers|mine|my [a-z]+)|(?:it|they|he|she|my [a-z]+) "
    r"(?:has |have )?(?:turned up|was in|were in|was under|were under|was behind|were behind|"
    r"was on|were on|was at|were at|showed up))\b")


def keeps_losing_thing(text):
    said = " ".join(words_of(text))
    return bool(KEEP_LOSING_THING.search(said) or KEPT_GOING_MISSING.search(said))


def found_what_was_lost(text):
    return bool(FOUND_WHAT_WAS_LOST.search(" ".join(words_of(text))))


def lost_in_a_place(text):
    clean = " ".join(words_of(text))
    for pattern, group in LOST_FORMS:
        found = pattern.search(clean)
        if not found or found.group(group) not in DEATHABLE:
            continue
        place = LOST_IN_A_PLACE.search(clean, found.end())
        return bool(place) and place.group(1) in PLACES
    return False


SHED = re.compile(r"\s+(?:weight|fat|pounds|stone|belly|blubber|tummy|tummies|inches|waist|"
                       r"middle|kilos?|kilograms?)\b")


def _shed_after(clean, start):
    return bool(SHED.match(clean, start))


FEARED_NOT_YET = re.compile(
    r"\b(?:dont|don't|do not|doesnt|doesn't|never|hope|hoping|hoped|scared|afraid|worried|"
    r"worry|worrying|dread|dreading|if|unless|before|hate|bear)\b"
    r"[^.!?]{0,24}?\b(?:lose|loses|losing)\b", re.I)


def _feared_not_done(clean, start):
    for frame in FEARED_NOT_YET.finditer(clean):
        if frame.start() <= start and 4 <= frame.end() - start <= 6:
            return True
    return False


def _lost_in_a_place_after(clean, start):
    place = LOST_IN_A_PLACE.search(clean, start)
    return bool(place) and place.group(1) in PLACES


def _can_die(clean):
    if is_a_machine_word(clean):
        return DEATHABLE - MACHINE_ANIMALS
    return DEATHABLE


def lost_a_thing(text):
    words = words_of(text)
    clean = " ".join(words)
    deathable = _can_die(clean)
    if re.search(r"\blost\s+it\b", clean):
        return True
    for pattern, group in LOST_FORMS:
        found = pattern.search(clean)
        if not found:
            continue
        thing = found.group(group)
        if thing in deathable or thing in LOST_SELF:
            return False
        return True
    if re.search(r"\b(?:lost|losing|lose)\s+the\s+([a-z]+)", clean):
        return True
    return False


def words_of(text):
    return _plain(text)


PET_DIED = re.compile(r"\b(?:died|dying|dead|dies|passed away|passed on|put down|"
                      r"put to sleep|euthanised|euthanized|pts)\b")


def _brought_in_prey(clean, words):
    if not (_has_pet(words) and PREY.search(clean) and HUNTING.search(clean)):
        return False
    return not PET_DIED.search(PREY.sub(" ", clean))


IT_DIED = re.compile(r"\bit\s+(?:just\s+|has\s+|had\s+|finally\s+)?(?:died|dies)\b")


def _a_pronoun_is_what_died(words, clean):
    if not IT_DIED.search(clean):
        return False
    return any(word in THINGS for word in words)


def a_thing_stopped(text, words=None):
    if words is None:
        words = words_of(text)
    if not words:
        return False
    if _object_died(words):
        return True
    return any(word == "dead" and _dead_is_not_a_death(words, place)
               for place, word in enumerate(words))


def reads_as_loss(text, words=None, a_pet=False):
    if words is None:
        words = words_of(text)
    if not words:
        return False
    deathable = _can_die(" ".join(words))
    clean = " ".join(words)
    if any(phrase in clean for phrase in LAUGHING):
        return False
    if lost_in_a_place(clean):
        return False
    if WOULD_HAVE_BEEN.search(clean) and (_has_person(words) or _unnamed_person(words, clean)):
        return True
    if _brought_in_prey(clean, words):
        return False
    if _a_thing_of_theirs(words):
        return False
    if _a_pronoun_is_what_died(words, clean):
        return False
    person = _has_person(words) or _unnamed_person(words, clean)
    if _the_end_is_near(clean, words):
        return True
    if _only_the_proceedings(clean, words):
        return False
    if person and THING_ROLE.search(clean) and not _another_person(words, clean):
        person = False
    if PLAIN.search(clean):
        return True
    if _passed_alone(clean, person) or _passed_on(clean, person) or _death_noun(clean, words, person):
        return True
    if WAKE.search(clean):
        return True
    if _buried_person(clean, words, person):
        return True
    if SYMPATHY.search(clean) and CARD_WORD.search(clean):
        return True
    if TOOK.search(clean):
        return True
    if (KILLED.search(clean) and not _killed_in_a_story(clean)
            and (person or set(words) & set(PASSED_ON_SUBJECT))):
        return True
    if _put_down(clean, words):
        return True
    if (person and STILL_CRY.search(clean) and not OTHER_WEEPS.search(clean)
            and not THEIR_TEARS_IN_A_CLAUSE.search(clean)):
        return True
    if DEATH_AS_A_THING.search(clean) and not NOT_A_DEATH.search(clean):
        if OWN_WORRY.search(clean) or THING_DEATH.search(clean) or PET_DEATH.search(clean):
            return False
        if FICTION.search(clean) and not person:
            return False
        if DEATH_COMPOUND.search(clean):
            return False
        owner = DEATH_OF_OWNER.search(clean)
        if owner and owner.group(1).split()[-1] in THINGS and not person:
            return False
        return True
    lost_the = LOST_THE.search(clean)
    if (lost_the and lost_the.group(1) in deathable and lost_the.group(1) not in PET_WORDS
            and not LOST_THE_FOUND.search(clean)):
        return True
    for pattern, group in LOST_FORMS:
        found = pattern.search(clean)
        if found and found.group(group) in deathable:
            if _their_thing_after(clean, found.end()):
                continue
            if (_lost_in_a_place_after(clean, found.end())
                    or _shed_after(clean, found.end())
                    or _feared_not_done(clean, found.start())):
                continue
            return True
    for pattern in (LOSS_OF, NEWS_OF):
        found = pattern.search(clean)
        if found and found.group(1) in deathable:
            if pattern is LOSS_OF and _lost_in_a_place_after(clean, found.end()):
                continue
            return True
    losing = LOSING.search(clean)
    if (losing and losing.group(1) in deathable
            and (losing.group(1) in CLOSE or LOSS_GRIEF_CUE.search(clean))
            and not _shed_after(clean, losing.end())
            and not _feared_not_done(clean, losing.start())
            and not _lost_in_a_place_after(clean, losing.end())):
        return True
    if marks_a_day(clean):
        return True
    if CONDITIONAL_TAIL.search(clean) and not (set(words) & HUMAN_WORDS):
        return False
    a_pronoun = bool(set(words_of(_spoken(clean))) & _PEOPLE_PRONOUNS)
    if (ANTICIPATED.search(_spoken(clean)) and (person or a_pronoun) and not _object_died(words)
            and not (_WORKING_WITH_THE_DYING.search(clean)
                     and not _SAID_DYING.search(clean))):
        return True
    if (not person and a_pronoun and DYING_NOW.search(_spoken(clean))
            and not _object_died(words) and not DYING_TO.search(clean)):
        return True
    if GOING_TO_DIE.search(clean) and (person or a_pronoun) and not _object_died(words):
        return True
    if (a_pet and (DYING.search(clean) or DIED.search(clean))
            and not _object_died(words) and not NOT_A_DEATH.search(clean)):
        return True
    if _accident_death(clean):
        return True
    if (DYING.search(clean) or DIED.search(clean)) and person and not _object_died(words):
        for index, word in enumerate(words):
            if word == "dead" and _dead_is_not_a_death(words, index):
                continue
            if word in ("died", "dies", "dead", "dying"):
                return True
    return False


def _accident_death(clean):
    if not MISADVENTURE.search(clean) or SURVIVED.search(clean):
        return False
    if NOT_A_DEATH.search(clean):
        return False
    if VERB_OBJECT.search(clean):
        return False
    victim = _owned_deathable(clean)
    if not victim:
        return False
    if victim not in PET_WORDS and KNOCKED_BY.search(clean) and not DEATH_SAID.search(clean):
        return False
    return True


def _owned_deathable(clean):
    for owner in OWNED.finditer(clean):
        for word in owner.group(1).split():
            if word in DEATHABLE:
                return word
    return None


def _passed_on(clean, person):
    if PASSED_ON not in clean:
        return False
    before, _, after = clean.partition(PASSED_ON)
    if not person and not set(before.split()[-3:]) & PASSED_ON_SUBJECT:
        return False
    rest = after.split()
    if not rest:
        return True
    if rest[0] not in PASSED_ON_OBJECT:
        return True
    if rest[0] == "the" and len(rest) > 1 and (rest[1] in MONTHS or rest[1][:1].isdigit()
                                               or rest[1] in ("1st", "2nd", "3rd")):
        return True
    return False


def _passed_alone(clean, person):
    words = clean.split()
    if PASSED_ALONE not in words:
        return False
    for i, word in enumerate(words):
        if word != PASSED_ALONE:
            continue
        if not person and not set(words[max(0, i - 4):i]) & PASSED_ON_SUBJECT:
            continue
        if set(words[:i]) & PASSED_A_RESULT:
            continue
        rest = words[i + 1:]
        if not rest:
            return True
        head = rest[0]
        nxt = rest[1] if len(rest) > 1 else ""
        if head in PASSED_ALONE_TAIL:
            continue
        if head in ("in", "on", "at", "last", "this", "that", "back"):
            if head == "at":
                if nxt in PASSED_TIME:
                    return True
                continue
            if nxt in PASSED_DATE or nxt in PASSED_TIME or nxt[:1].isdigit():
                return True
            continue
        if head == "it" and nxt in ("was", "is", "has", "had"):
            return True
        if head in PASSED_ON_OBJECT or head in PASSED_ALONE_HANDED or head in PASSED_ALONE_NOUN:
            continue
        return True
    return False


def _death_noun(clean, words, person):
    if not DEATH_NOUN.search(clean) or NOT_A_DEATH.search(clean):
        return False
    if THING_DEATH.search(clean) or PET_DEATH.search(clean):
        return False
    if DEATH_COMPOUND.search(clean):
        return False
    if FICTION.search(clean) and not person:
        return False
    if OWN_WORRY.search(clean):
        return False
    if person:
        return True
    owned = OWN_DEATH.search(clean)
    if owned:
        owner = clean[owned.start():owned.end()].split()[0]
        if owner in ("my", "his", "her", "their", "your", "our"):
            return True
        stem = owner.rstrip("s").rstrip("'")
        if stem in PEOPLE or owner in PEOPLE:
            return True
    return bool(DEATH_CUE.search(clean))



def _unnamed_person(words, clean):
    if not any(word in UNNAMED for word in words):
        return False
    if any(word in MEDIA for word in words):
        return False
    return bool(ASK_WORDS.search(clean))


PASSIVE_AUX = ("be", "being", "been", "get", "gets", "getting", "got", "is", "was", "are",
               "were", "will", "to")
REMAINS = ("ashes", "body", "bodies", "coffin", "coffins", "casket", "caskets", "urn", "urns",
           "remains", "grave", "graves", "plot", "plots")

BURIABLE = ("post", "posts", "fence", "fences", "fencing", "panel", "panels", "gate", "gates",
            "cable", "cables", "wire", "wires", "pipe", "pipes", "hose", "hosepipe", "drain",
            "drains", "treasure", "bulb", "bulbs", "seed", "seeds", "tank", "tub", "rubbish",
            "waste", "compost", "manure", "sand", "gravel", "rubble", "shed", "trampoline")


def _buried_person(clean, words, person=False):
    if not BURIED.search(clean):
        return False
    for index, word in enumerate(words):
        if word not in ("buried", "bury"):
            continue
        if index and words[index - 1] in PASSIVE_AUX:
            if person or _has_pet(words) or set(words) & set(REMAINS):
                return True
            return not (set(words) & set(BURIABLE))
        rest = words[index + 1:index + 5]
        while rest and rest[0] in BURIED_ADJECTIVE:
            rest = rest[1:]
        if rest and rest[0] in ("him", "her", "them"):
            return True
        if rest and rest[0] in BURIED_OBJECT:
            rest = rest[1:]
            while rest and rest[0] in BURIED_ADJECTIVE:
                rest = rest[1:]
            if not rest:
                return False
            return rest[0] in PEOPLE
        return True
    return False


def _put_down(clean, words):
    if not PUT_DOWN.search(clean):
        return False
    if any(phrase in clean for phrase in BEDTIME) and not any(
            phrase in clean for phrase in LOSS_CONTEXT):
        return False
    if _has_pet(words):
        return True
    return any(phrase in clean for phrase in LOSS_CONTEXT)


def _names_a_stored_pet(text, memory):
    known = (memory or {}).get("user") or {}
    pets = list(known.get("pets") or []) + list(known.get("pets_gone") or [])
    said = set(words_of(text))
    for pet in pets:
        if not isinstance(pet, dict):
            continue
        name = str(pet.get("name") or "").strip().lower()
        if name and len(name) > 2 and name in said:
            return True
    return False


def _has_pet(words):
    return any(word in PET_WORDS for word in words)


def _a_person_dying(tight):
    words = [word.strip(",.?!") for word in tight.split()]
    if any(word in ("he", "she", "they", "him", "her", "them") for word in words):
        return True
    return _has_person(words)


def _a_hard_time_that_is_theirs(line):
    text = str(line or "").lower().replace("\u2019", "'")
    if not A_RELATION_IN_A_HARD_TIME.search(text):
        return False
    if not DEATH_WORD.search(text):
        return False
    return not the_animal(text)


CHILDS_OWN_LOSS = re.compile(
    r"\b(?:my|our)\s+(?:son|sons|daughter|daughters|child|children|kid|kids|boy|girl|lad|lass|"
    r"teenager|baby|toddler|stepsons?|stepdaughters?|stepchildren)\b[^.]{0,40}"
    r"\b(?:his|her|their)\s+(?:dad|daddy|mum|mummy|father|mother|parent|parents|brother|"
    r"sister|grandad|grandads|granddad|grandma|grandmas|gran|grans|nan|nans|grandpa|grandparents)\b",
    re.I)


def whose(clean):
    if CHILDS_OWN_LOSS.search(clean) and not A_STRANGERS_ANIMAL.search(clean):
        return "own"
    if (SOMEONE_ELSES.search(clean) or HIS_HERS.search(clean)
            or SOMEONE_ELSES_OWN.search(clean) or A_STRANGERS_ANIMAL.search(clean)):
        return "someone"
    return "own"


RELATIVE_PET_REPLIES = (
    "Oh, that's hard on them. A {one} is family to the person who had it — say straight out "
    "that you're sorry, and ask how they're doing.",
    "That's a real loss for them, not a small one. Say it plainly (\"I'm so sorry about the "
    "{animal}\"), then check in again in a week or so.",
    "Pets are family, so treat it the way you would a family death for them: say you're sorry "
    "about the {animal}, and offer one concrete thing if you're close enough.",
)

STRANGER_ANIMAL_REPLIES = (
    "That's sad. A {one} you only see over the fence is still part of the day, and the street "
    "is quieter without it.",
    "Sorry to hear that. You don't have to own a {one} to miss one — it's a real gap when one "
    "that was always about goes.",
    "Oh no. Even a neighbour's {animal} leaves a quiet patch behind it, and noticing that isn't "
    "silly.",
)

TWO_WORD_PETS = (("guinea", "pig"), ("guinea", "pigs"))
PLURAL_PAIRS = {"cats": "cat", "dogs": "dog", "rabbits": "rabbit", "bunnies": "bunny",
                "hamsters": "hamster", "budgies": "budgie", "parrots": "parrot", "horses": "horse",
                "ponies": "pony", "ferrets": "ferret", "rats": "rat", "tortoises": "tortoise",
                "snakes": "snake", "lizards": "lizard", "gerbils": "gerbil",
                "chinchillas": "chinchilla", "cockatiels": "cockatiel", "guinea pigs": "guinea pig",
                "puppies": "puppy", "kittens": "kitten", "fish": "fish", "mice": "mouse"}


def one_of(animal):
    return PLURAL_PAIRS.get(animal, animal)


DEATH_WORD = re.compile(
    r"\b(?:died|dies|dying|dead|death|passed|put\s+down|put\s+to\s+sleep|euthanised|"
    r"euthanized|killed|pts|gone|loss|lost)\b")


def the_animal(line):
    text = str(line or "").lower().replace("\u2019", "'")
    words = words_of(text)
    named = [word for word in words if word in PET_WORDS]
    if not named:
        return ""
    death = DEATH_WORD.search(text)
    if death:
        before = [word for word in words_of(text[:death.start()]) if word in PET_WORDS]
        named = before or named
    for first, second in TWO_WORD_PETS:
        if first in words and second in words:
            return f"{first} {second}"
    return named[-1]


def named_animal(replies, line):
    animal = the_animal(line) or "pet"
    return tuple(reply.format(animal=animal, one=one_of(animal)) for reply in replies)


def a_relative_pet(line):
    match = SOMEONE_ELSES_OWN.search(str(line or "").lower().replace("\u2019", "'"))
    return bool(match and match.group("who") in PET_WORDS)


def a_strangers_animal(line):
    return bool(A_STRANGERS_ANIMAL.search(str(line or "").lower().replace("\u2019", "'")))


SWAP_ASK = re.compile(r"^(?:and|but|also|what\s+about|how\s+about|what\s+(?:of|say)|and\s+what\s+about)\b")
SWAP_MOST_WORDS = 8
ASKS = re.compile(
    r"\?|\b(?:what|which|how|when|where|who|why|should|shall|can|could|do|does|did|is|are|"
    r"was|were|will|would|must|have|has)\b", re.I)
A_SWAP_INHERITS = re.compile(
    r"\b(?:wear|wearing|put\s+on|bring|brings|take|give|send|order|buy|cook|make|pack|"
    r"choose|pick|pay|cost|costs)\b")


def _a_swap_of_the_question_before(text, memory):
    tight_line = _tight(text)
    if not SWAP_ASK.match(tight_line):
        return False
    if len(_plain(text)) > SWAP_MOST_WORDS:
        return False
    previous = ""
    for turn in reversed([t for t in (memory.get("turns") or []) if isinstance(t, dict)][:8]):
        line = str(turn.get("user") or "")
        if not line.strip() or _plain(line) == _plain(text):
            continue
        if ASKS.search(" ".join(_plain(line))):
            previous = line
            break
    if not previous or not _plain(previous):
        return False
    return bool(A_SWAP_INHERITS.search(_tight(previous)))


def _still_ahead(memory):
    record = memory.get("loss")
    if isinstance(record, dict) and record.get("ahead"):
        pool = THE_DAYS_BEFORE if record.get("pet") else SOMEONE_DYING
        return _less_what_was_said(pool, [t for t in (memory.get("turns") or [])
                                          if isinstance(t, dict)])
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    for turn in reversed(turns[-4:]):
        line = str(turn.get("user") or "")
        tight_line = _tight(line)
        if not line or QUESTION.search(line) or not NOT_YET.search(tight_line):
            continue
        if _has_pet(_plain(line)):
            return _less_what_was_said(THE_DAYS_BEFORE, turns)
        if _a_person_dying(tight_line):
            return _less_what_was_said(SOMEONE_DYING, turns)
    last = str(turns[-1].get("bot") or "") if turns else ""
    if last and last in THE_DAYS_BEFORE:
        return _less_what_was_said(THE_DAYS_BEFORE, turns)
    if last and last in SOMEONE_DYING:
        return _less_what_was_said(SOMEONE_DYING, turns)
    return None


_HELPERS = re.compile(r"\b(?:doctor|doctors|gp|gps|consultant|nurse|nurses|vet|vets|"
                      r"hospice|hospital|carers?)\b", re.I)


def _less_what_was_said(pool, turns):
    said = [str(t.get("bot") or "").strip() for t in turns or [] if str(t.get("bot") or "").strip()]
    if not said:
        return pool
    kept = [line for line in pool
            if line.strip() not in said
            and not (_HELPERS.search(line) and any(_HELPERS.search(one) for one in said))]
    return tuple(kept) or pool


KEEPING_JUDGED = re.compile(
    r"\b(?:cruel|cruelty|unkind|wrong|selfish|unfair|mean|nasty)\b[^.?!]{0,60}?"
    r"\b(?:keep|keeping|kept)\b(?=[^.?!]{0,50}\b(?:going|alive)\b)"
    r"|\b(?:keep|keeping|kept)\b(?:\s+\w+){0,4}\s+(?:going|alive)\b[^.?!]{0,50}?"
    r"\b(?:cruel|cruelty|unkind|wrong|selfish|unfair)\b"
    r"|\b(?:cruel|cruelty|unkind|wrong|selfish|unfair)\b[^.?!]{0,60}?"
    r"\b(?:put|putting|having\s+(?:\w+\s+){0,3}put)\b(?:\s+\w+){0,4}\s+(?:down|to\s+sleep)\b"
    r"|\b(?:cruel|cruelty|unkind|wrong|selfish|unfair)\b[^.?!]{0,60}?\blet\s+(?:\w+\s+)?go\b")
ENDING_ASKED = re.compile(
    r"^(?:(?:and|so|but|oh|god|honestly|now|then|ok|okay)\s+)*"
    r"(?:should|shall|ought|when|how|do|does|is|will)\b(?![^.?!]{0,40}\b(?:bed|bedtime|"
    r"crate|kennel|lead|garden|room|downstairs|upstairs|outside|night|nights|nap|naps)\b)"
    r"[^.?!]{0,40}?\b(?:put|putting|have\s+(?:\w+\s+){0,3}put|let\s+(?:\w+\s+)?go)\b"
    r"(?:\s+\w+){0,4}\s+(?:down|to\s+sleep)\b"
    r"|^(?:(?:and|so|but|oh|honestly|now|then)\s+)*(?:when|how)\b[^.?!]{0,30}?"
    r"\b(?:know|tell|decide|sure)\b[^.?!]{0,30}?\b(?:its|it's|the)\s+(?:time|right\s+time|end)\b"
    r"|^(?:(?:and|so|but|oh|honestly|now|then)\s+)*is\s+it\s+(?:the\s+|the\s+right\s+)?time\b"
    r"[^.?!]{0,20}\b(?:to\s+)?(?:let|put|say\s+goodbye|stop|end)\b")
KEEPING_GOING_REPLIES = (
    "Not cruel, no. Wanting to keep a pet with you is the ordinary way love behaves, and asking "
    "the question is what someone who is still looking after them does. What helps is a written "
    "week - did they eat, settle, sleep, enjoy one thing - because a change is easier to see over "
    "a fortnight than in one bad night.",
    "That is not selfish, and it is not a vote. Ask the vet what they would do with their own "
    "animal and ask them to be blunt about pain and appetite, then keep a note of the good days "
    "against the bad ones - most people find the answer is in that note rather than in the guilt.",
    "Asking it says most of what needs saying: you have not stopped looking after them. Whether "
    "keeping on is fair depends on the animal, not on you - eating, drinking, pain, one thing "
    "still enjoyed. Take that list to the vet and let them tell you what the next weeks look "
    "like, rather than working it out alone.",
    "No, not cruel. There is no scoreboard for this, and the person who is doing it for the "
    "animal's sake is usually the one who feels worst about it. The useful thing is the vet's "
    "honest view plus a normal week written down: food, drink, sleep, pain, one good thing a day.",
)
IS_IT_TIME_REPLIES = (
    "There is no single day, and waiting for a sign that everyone agrees on is what makes this "
    "the hardest part. What people use: more bad days than good, no interest in food or in the "
    "things they loved, pain the vet cannot get on top of. Ask the vet to go through a "
    "quality-of-life list with you - it turns a guess into something you can look at.",
    "Only you and the vet can say, and the vet has done this far more often than you have. Write "
    "down a normal day for the next week - eating, drinking, moving, sleeping, one thing they "
    "still enjoy - and take that to the appointment; a fortnight of it usually makes the call "
    "clearer than any single bad night.",
    "It is a judgement rather than a date, and the ones that go wrong are the ones made in a "
    "panic at 2am. Book a talk with the vet about quality of life and ask them plainly: would "
    "they wait, and what would make them stop waiting?",
)


def _an_animal_in_the_chat(memory, turns=6):
    history = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(history, list):
        return False
    for turn in history[-turns:]:
        said = turn.get("user") if isinstance(turn, dict) else None
        if isinstance(said, str) and PET.search(_tight(said)):
            return True
    return False


def _keeping_going(tight, words, memory):
    judged = bool(KEEPING_JUDGED.search(tight))
    if not judged and not ENDING_ASKED.search(tight):
        return None
    where = KEEPING_GOING_REPLIES if judged else IS_IT_TIME_REPLIES
    if _has_pet(words):
        return where
    if _has_person(words):
        return None
    if _an_animal_in_the_chat(memory):
        return where
    return None


def _first_days(memory):
    record = memory.get("loss")
    pet = isinstance(record, dict) and record.get("pet")
    return FIRST_DAYS_PET if pet else FIRST_DAYS_PERSON
SAY_GOODBYE = re.compile(
    r"\b(?:say\s+good\s?bye|good\s?bye\s+to\s+(?:him|her|them)|last\s+words|"
    r"what\s+(?:do|should|can)\s+i\s+say\b|what\s+to\s+say\b|"
    r"how\s+(?:do|can)\s+i\s+say\b)")
SAY_TO_WHO = re.compile(r"\b(?:say|talk)\s+to\s+"
                        r"(?:(?:the|my|our|his|her|their|your)\s+)?(\w+)")
VISIT_TARGETS = frozenset(("him", "her", "them", "himself", "herself", "themselves"))


def _the_visit_ask(clean):
    if not SAY_GOODBYE.search(clean):
        return False
    for found in SAY_TO_WHO.finditer(clean):
        if found.group(1) not in VISIT_TARGETS:
            return False
    return True


def _the_animal_of(text, memory):
    animal = the_animal(text)
    if animal:
        return animal
    record = (memory or {}).get("loss") if isinstance(memory, dict) else None
    if isinstance(record, dict):
        return the_animal(str(record.get("who") or ""))
    return ""


def _grief_replies(line, memory):
    if whose(line) == "someone":
        return GRIEF_REPLIES
    animal = _the_animal_of(line, memory)
    if not animal:
        return GRIEF_REPLIES
    if animal.endswith("s"):
        singular = animal[:-1]
        if singular in PET_WORDS or singular.endswith(" pig"):
            animal = singular
    article = "an" if animal[:1] in "aeiou" else "a"
    return tuple(reply.format(animal=animal, article=article) for reply in PET_GRIEF_REPLIES)


def _a_colour_is_worn(line):
    try:
        from ..knowledge import lookup
        return lookup.a_colour_is_worn(line)
    except Exception:
        return False


def reply_for(text, memory, clean=None, topics=None, mood=None):
    words = words_of(text)
    line = clean if isinstance(clean, str) and clean else " ".join(words)
    tight = _tight(line)
    if _a_colour_is_worn(line) and not A_DEATH_HAPPENED.search(tight):
        return None
    if _dream is not None and _dream.SETTLED_IT.search(line) \
            and _dream.told_in_the_turn_before(memory):
        return None
    if _dream is not None and _dream.a_dream_is_not_happening(line) \
            and not _dream.a_death_came_first(line):
        return None
    if _only_a_new_subject(line):
        return None
    if DYING_OTHER.search(tight):
        return None
    if SPEAKER_TOO.search(tight) and not WISH_FRAME.search(tight):
        rest = SPEAKER_TOO.sub(" ", tight).strip()
        animal = bool(PET.search(rest)) and _a_pet_of_ours(rest, words)
        if (is_dying_now(rest) or _the_end_is_near(rest, words)
                or (animal and (AT_THE_END.search(rest) or PET_AT_THE_END.search(rest)
                                or PET_HAS_HAD_ENOUGH.search(rest)))):
            return SPEAKER_TOO_REPLIES
    if (PET_HAS_HAD_ENOUGH.search(tight) and PET.search(tight)
            and _a_pet_of_ours(line, words) and not SPEAKER_HAS_HAD_ENOUGH.search(tight)):
        return THE_DAYS_BEFORE
    if (PET_AT_THE_END.search(tight) and PET.search(tight)
            and _a_pet_of_ours(line, words) and not SPEAKER_HAS_HAD_ENOUGH.search(tight)):
        return THE_DAYS_BEFORE
    if AT_THE_END.search(tight) and not SPEAKER_HAS_HAD_ENOUGH.search(tight):
        if is_dying_now(tight):
            if PET.search(tight) and _a_pet_of_ours(line, words):
                return THE_DAYS_BEFORE
            if "?" in line or ASK_WORDS.search(tight) or line.startswith(
                    ("what", "how", "should", "can", "do", "does", "is", "why", "when")):
                return DYING_SAY_REPLIES
            return DYING_REPLIES
    if _the_visit_ask(tight) and dying_in_the_chat(memory):
        return DYING_SAY_REPLIES
    asking = "?" in line or bool(ASK_FORM.search(tight)) or bool(ASK_WORDS.search(tight)) or line.startswith(
        ("what", "how", "should", "can", "do", "does", "is", "why", "when"))
    if EULOGY_WORD.search(tight) and EULOGY_ASK.search(tight):
        return None
    if WEAR.search(tight):
        return None
    if _a_swap_of_the_question_before(text, memory):
        return None
    if _a_gift_for_someone_in_care(tight):
        return None
    if _telling_a_child(tight):
        return None
    cost_pool = (arrangement_cost_pool(line, tight, memory)
                 or arrangement_cost_pool(text, tight, memory))
    if cost_pool:
        return cost_pool
    if is_practical_ask(line, tight) or is_practical_ask(text, tight):
        return None
    if (not QUESTION.search(line) and not ASK_WORDS.search(tight)
            and not NOT_THE_END.search(tight) and (
                ESTIMATE.search(tight) or _the_end_is_near(tight, words))) and (
            _has_pet(words) or _a_person_dying(tight) or CARE_WHO.search(tight)):
        pet = _has_pet(words) or _the_vet_said_it(tight, words)
        return THE_DAYS_BEFORE if pet else SOMEONE_DYING
    if OPEN_ASK.match(tight):
        ahead = _still_ahead(memory)
        if ahead is not None:
            return ahead
    if lost_in_a_place(text):
        return MISLAID_REPLIES
    if (GET_THROUGH.search(tight) or GET_THROUGH_DAY.search(tight)) \
            and not GET_THROUGH_TO.search(tight):
        ahead = bool(is_dying_now(tight) or dying_in_the_chat(memory) or _still_ahead(memory))
        if _a_thing_of_its_own_to_get_through(tight):
            return None
        if ahead or continues(memory) or reads_as_loss(
                text, words, _names_a_stored_pet(text, memory)):
            if GET_THROUGH_DAY.search(tight):
                return REMEMBER_REPLIES
            if ahead:
                return GETTING_THROUGH_DYING_REPLIES
            return GETTING_THROUGH_REPLIES
    if not continues(memory) and _an_ending_in_the_chat(memory):
        if _how_long_since(tight, tight.split()) and not _names_a_subject(topics):
            return ENDING_SINCE_REPLIES
        if (A_FEELING_BETTER_ASK.search(tight)
                and not (set(topics or ()) - THREAD_TOPICS - MEASURE_TOPICS - {"health"})):
            return ENDING_FEELINGS_REPLIES
    keeping = _keeping_going(tight, words, memory)
    if keeping:
        return keeping
    if reads_as_loss(text, words, _names_a_stored_pet(text, memory)):
        if CARD.search(tight) and (ASK_WORDS.search(tight) or asking
                                   or (CARD_TO_WRITE.search(tight) and WRITE_WORD.search(tight))):
            return CARD_REPLIES
        ahead_now = (is_dying_now(line) or _the_end_is_near(tight, words)
                     or (dying_in_the_chat(memory)
                         and (TREATMENT_STOPPED.search(tight)
                              or NOTHING_MORE_TO_DO.search(tight))))
        if ahead_now and not (FUNERAL.search(tight) or WAKE.search(tight)):
            if _a_pet_of_ours(line, words) or _the_vet_said_it(tight, words):
                return THE_DAYS_BEFORE
            if ASK_WORDS.search(tight):
                return DYING_SAY_REPLIES
            if QUESTION.search(line):
                return DYING_GRIEF_REPLIES
            return DYING_REPLIES
        if ASK_WORDS.search(tight):
            return SAY_REPLIES
        if (NOT_YET.search(tight) and not PUTTING_REGRETTED.search(tight)
                and not QUESTION.search(line)):
            if PET.search(tight):
                return THE_DAYS_BEFORE
            if _a_person_dying(tight):
                return SOMEONE_DYING
        if (FUNERAL.search(tight) or WAKE.search(tight)) and (
                asking or whose(line) == "someone") and not _feeling(tight):
            if _when_asked(tight):
                return FUNERAL_WHEN_REPLIES
            return FUNERAL_REPLIES
        if marks_a_day(tight) and asks_what_to_do(tight):
            return REMEMBER_REPLIES
        feeling = _feeling(tight)
        if feeling and _asks_about_the_feeling(tight):
            return FEELING_REPLIES[feeling]
        if QUESTION.search(line):
            return _grief_replies(line, memory)
        if feeling:
            return FEELING_REPLIES[feeling]
        if whose(line) == "someone":
            if a_relative_pet(line):
                return named_animal(RELATIVE_PET_REPLIES, line)
            if a_strangers_animal(line):
                return named_animal(STRANGER_ANIMAL_REPLIES, line)
            if set(words_of(line)) & CLOSE:
                return NAMED_LOSS_SAY_REPLIES
            return SAY_REPLIES
        if PUTTING_REGRETTED.search(tight):
            return PUT_DOWN_REGRET_REPLIES
        habit = _still_here(line, words or tight.split())
        if habit:
            return habit
        if _a_hard_time_that_is_theirs(tight) and whose(line) == "own":
            return THEIR_HARD_TIME_REPLIES
        return LOSS_REPLIES
    if not continues(memory):
        if _missing_someone(tight):
            return MISS_REPLIES
        return None
    if dying_in_the_chat(memory) and (QUESTION.search(line) or _feeling(tight)):
        return DYING_GRIEF_REPLIES
    if dying_in_the_chat(memory) and _the_visit_ask(tight):
        return DYING_SAY_REPLIES
    if (_thread_pool(memory) is MISS_REPLIES
            and not GRIEF_ASK_FORM.search(line) and not REFERS_TO_THEM.search(tight)
            and not _DEATH_IN_LINE.search(tight)
            and _a_body_with_its_own_answer(tight, tight.split())):
        return None
    if HELLO_ON_ITS_OWN.match(tight):
        return HELLO_AFTER
    if OPEN_ASK.match(tight):
        return _still_ahead(memory) or _first_days(memory)
    if marks_a_day(line, known=True) and asks_what_to_do(line):
        return REMEMBER_REPLIES
    if (not asking and _a_habit_in(tight + " " + line)
            and (continues(memory)
                 or _thread_pool(memory) in (MISS_REPLIES, AFTER_REPLIES, THE_HABIT_REPLIES))):
        habit = _still_here(line, tight.split())
        if habit:
            return habit
    if (_thread_pool(memory) is MISS_REPLIES and not asking
            and STILL_ABOUT_THEM.search(tight)
            and not _a_question_about_the_feeling(line, set(tight.split()))
            and not _hands_over_a_detail(tight)):
        return AFTER_REPLIES
    if RITUAL.search(tight) and RITUAL_PERSON.search(tight):
        return AFTER_REPLIES
    if lost_a_thing(line):
        return None
    if CARD.search(tight) and (ASK_WORDS.search(tight)
                               or (CARD_TO_WRITE.search(tight) and WRITE_WORD.search(tight))):
        return CARD_REPLIES
    if ASK_WORDS.search(tight):
        return SAY_REPLIES
    if (FUNERAL.search(tight) or WAKE.search(tight)) and asking and not _feeling(tight):
        if _when_asked(tight):
            return FUNERAL_WHEN_REPLIES
        return FUNERAL_REPLIES
    if GRIEF_POINTS_BACK.match(tight):
        return _grief_replies(line, memory)
    words_now = tight.split()
    if QUESTION.search(line) and not (_names_a_subject(topics)
                                      and not _state_describes_them(words_now)
                                      and not _the_body_is_theirs(tight, words_now)):
        return _grief_replies(line, memory)
    said = set(words_now)
    if said & GRIEF_FEELINGS:
        if _a_question_about_the_feeling(line, said):
            return None
        return AFTER_REPLIES
    if _about_family(words_now) and said & GRIEF_SELF:
        return AFTER_REPLIES
    if REFERS_TO_THEM.search(tight) and _about_them(tight) and mood != "positive":
        if IDEA_ASK.search(tight) or (asking and _own_subject(topics)):
            return None
        if _thread_pool(memory) is SAY_REPLIES:
            return SAY_REPLIES
        return AFTER_REPLIES
    if ABSENCE.search(line) and not asking:
        return AFTER_REPLIES
    if (REASSURING.search(tight) and not asking and not _own_subject(topics)
            and not PEACE_IS_MINE.search(tight)):
        return AFTER_REPLIES
    if _how_long_since(tight, words_now) and not _names_a_subject(topics):
        return TIME_SINCE_REPLIES
    if _own_subject(topics) and not _state_describes_them(words_now):
        return None
    if (_about_them(tight) or TIME_OF_DAY.search(tight)) and _own_state(words_now):
        return AFTER_REPLIES
    if any(phrase in tight for phrase in GRIEF_REFERRING + GRIEF_OBJECTS):
        return AFTER_REPLIES
    if mood == "negative":
        return AFTER_REPLIES
    if ABSENCE.search(line):
        return AFTER_REPLIES
    if isinstance(topics, (list, tuple)) and topics:
        if not set(topics) - {"feelings", "health", "sleep"}:
            return _grief_replies(line, memory)
    if _missing_someone(tight):
        return MISS_REPLIES
    return None


RITUAL = re.compile(r"\b(?:we (?:always|used to)|every year|her birthday|his birthday|"
                    r"their birthday|anniversary|(?:first )?(?:christmas|birthday|mothers day|"
                    r"fathers day) without)\b")
RITUAL_PERSON = re.compile(r"\b(?:her|his|their|mum|mom|mam|dad|mother|father|nan|nana|gran|"
                           r"granny|grandad|grandma|grandpa|husband|wife|partner|son|daughter|"
                           r"brother|sister|birthday|anniversary|christmas)\b")

THREAD_TURNS = 6


def asks_anything(line, tight=None):
    line = str(line or "")
    tight = _tight(line) if tight is None else tight
    return ("?" in line or bool(ASK_FORM.search(tight))
            or line.startswith(("what", "how", "should", "can", "do", "does", "is", "why",
                                "when", "where")))


PAPER_ASK = re.compile(
    r"\b(probate|grant of probate|letters of administration|estate|paperwork|solicitor|"
    r"wills|(?:the|his|her|their|my|our|a) will|inheritance tax|death certificate|"
    r"register (?:the |his |her |their )?death)\b")



GIFT_THING_ASK = re.compile(
    r"\bwhat (?:to|should i|shall i|can i|could i|do i|would you|should we|can we|do we)\s+"
    r"(?:buy|bring|get|take|give|make)\b"
    r"|\bwhat (?:do|would|could|should) you\s+(?:buy|bring|get|take|give)\b"
    r"|\b(?:dont|don't|do not|not)\s+know what to\s+(?:buy|bring|get|take|give)\b"
    r"|\b(?:gift|present)\s+(?:idea|ideas)\b"
    r"|\b(?:a|any) gift\b")
IN_CARE = re.compile(r"\b(?:hospice|hospital|ward|icu|hdu|hospice bed)\b")


NOT_A_BEDSIDE = re.compile(r"\b(funeral|funerals|wake|burial|cremation|memorial|service|"
                           r"church|grave|graveside|scattering)\b")


def _a_gift_for_someone_in_care(tight):
    return bool(GIFT_THING_ASK.search(tight) and IN_CARE.search(tight)
                and not NOT_A_BEDSIDE.search(tight))


def is_practical_ask(line, tight=None):
    line = str(line or "")
    tight = _tight(line) if tight is None else tight
    asking = (asks_anything(line, tight)
              or bool(re.match(r"\s*(?:who|who's|whos|whose|where|which)\b", tight)))
    opened_late = bool(ASK_WE.search(tight)) or bool(ASK_TAIL.search(line))
    if (FUNERAL.search(tight) or FUNERALS.search(tight)
            or WAKE.search(tight)) and a_part_of_the_day_asked(tight):
        return True
    if (asking or opened_late) and PET_ARRANGEMENT.search(tight) and PET.search(tight):
        return True
    if opened_late and PAPER_ASK.search(tight) and not GRIEF_CUE.search(tight):
        return True
    return bool(asking and PRACTICAL.search(tight) and not GRIEF_CUE.search(tight)
                and not ASK_WORDS.search(tight))

POOLS = (LOSS_REPLIES, SAY_REPLIES, CARD_REPLIES, GRIEF_REPLIES, FUNERAL_REPLIES,
         FUNERAL_COST_COMPARE_REPLIES, FUNERAL_HELP_REPLIES,
         REMEMBER_REPLIES, FUNERAL_WHEN_REPLIES, AFTER_REPLIES, HELLO_AFTER,
         MISS_REPLIES, THE_ROUTINE_REPLIES, THE_HOUSE_REPLIES, THE_CANNOT_STOP_REPLIES,
         THE_HABIT_REPLIES, THE_JOBS_FOR_THEM_REPLIES,
         GETTING_THROUGH_REPLIES) + tuple(FEELING_REPLIES.values())


SAFETY_MODULES = ("safety",)
FALLBACK_MODULES = ("greeting",)


ENDING_TURNS = 3


def _an_ending_in_the_chat(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    stepped = 0
    while turns and stepped < ENDING_TURNS:
        said = str(turns[-1].get("user") or "")
        if AN_ENDING.search(said):
            return True
        if str(turns[-1].get("module") or "") not in ("loss", "grief"):
            return False
        turns, stepped = turns[:-1], stepped + 1
    return False


def continues(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    if not turns:
        return False
    looked_past = False
    stepped = 0
    while turns and stepped < THREAD_TURNS:
        if str(turns[-1].get("module") or "") in SAFETY_MODULES:
            turns, looked_past = turns[:-1], True
            continue
        if is_practical_ask(turns[-1].get("user")):
            turns, looked_past, stepped = turns[:-1], True, stepped + 1
            continue
        break
    if not turns:
        if not looked_past:
            return False
        return any(reads_as_loss(str(turn.get("user") or ""))
                   for turn in (memory.get("turns") or []) if isinstance(turn, dict))
    last = str(turns[-1].get("bot") or "")
    if last and any(last in pool for pool in POOLS):
        return True
    module = str(turns[-1].get("module") or "")
    return bool(module) and module not in FALLBACK_MODULES + SAFETY_MODULES and reads_as_loss(
        str(turns[-1].get("user") or ""))
