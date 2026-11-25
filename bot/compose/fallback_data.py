
import re

from . import finding_out



FILLERS = frozenset(("actually", "really", "exactly", "even", "just", "please", "basically",
                     "honestly", "literally", "anyway", "still", "perhaps", "maybe"))

_BOUNDED = {}

GREETING = (
    "Hey! What's on your mind?",
    "Hi there — what can I help with?",
    "Hello! Good to see you. What are you thinking about?",
    "Hey! I'm here. What would you like to talk about?",
    "Hi! What's up?",
)

THANKS = (
    "Any time!",
    "You're welcome — glad that helped.",
    "No problem at all. Shout if you need anything else.",
    "Happy to help.",
)

UNKNOWN_DECIDE = (
    "That's your call, not mine — I don't know enough about your side of it. Tell me what you're "
    "weighing and I'll help you pick.",
    "Can't call that one for you, sorry. Say what you'd lose either way and I'll lay it out with "
    "you.",
    "Not mine to decide, sorry. Tell me what matters most here and I'll help you think it "
    "through.",
)

UNKNOWN_MONEY = (
    "Not a call I can make for you, sorry: anything money-shaped wants someone who can see the "
    "whole picture, and free advice is easy to find - Citizens Advice, a bank adviser, a broker. "
    "Tell me what you are weighing anyway and I'll help you lay it out.",
    "That is an adviser's call rather than mine, sorry - a free debt or money advice service will "
    "know your rules and your numbers. Say what matters most and I'll help you get it straight "
    "before you ring them.",
    "I don't know enough about your money to call it, and a guess is the worst thing here. What "
    "would each choice cost you, and what would it leave you free to do?",
)

HANDS_BACK = (
    "Happy to - what are you choosing between?",
    "Then give me the choice: what's on the table?",
    "I'll make the call if you tell me the options - what are they?",
)

PLASTER_IT = (
    "Yes - cover it with a plaster and leave it alone: that keeps it clean and stops your hand "
    "going back to it. Change it daily, and get it looked at if the skin around it goes red and "
    "spreading.",
    "Cover it and leave it be. A plaster does more than air does for a cut or a graze; change it "
    "each day and see a pharmacist if it starts to look angry.",
)

SORE_HANDS = (
    "Leave it alone - don't pick or scratch it. Squeezing pushes the infection deeper and it "
    "comes back worse, and keeping it clean does more than pressure does; it settles in a few "
    "days on its own.",
    "Don't squeeze, pick or scratch it. A warm flannel for ten minutes and clean hands will do "
    "more than pressure will; if it goes hot, red and spreading, a pharmacist can look at it "
    "today.",
)

GO_TO_BE_SEEN = (
    "Go, and have someone drive you rather than driving yourself. Take your medicine list if you "
    "have one — they ask for it first.",
    "Go now rather than waiting to see if it settles. Whether something needs closing, strapping "
    "or an X-ray is their call, not one to make from here.",
    "Go, and if you get worse on the way — breathing trouble, heavy bleeding, or you cannot stay "
    "awake — ring 999 rather than carrying on.",
)

RING_FOR_HELP = (
    "Yes — ring 999 or 911 now, and stay on the line while you talk. If it turns out to be less "
    "serious than you thought, they would far rather hear from you than not.",
    "Ring now rather than waiting to be sure: 999 or 911, say where you are and what has "
    "happened, and keep the person talking while you dial.",
    "Call 999 or 911 straight away. What happens in the next few minutes matters more than "
    "anything either of us can work out from here.",
)

RING_THE_POLICE = (
    "Ring 999 now, for anything happening as you read this or for anyone in danger. Once it is "
    "over, ring 101 instead. Either way the call is free and they would rather hear it.",
    "999 now, for anything happening or anyone in danger. 101 for what has already happened. You "
    "can say you are not sure it counts — deciding that is their job, not yours.",
)

_A_PERSON = frozenset((
    "him", "her", "them", "mum", "mom", "mother", "dad", "father", "sister", "brother", "friend",
    "friends", "boss", "ex", "partner", "husband", "wife", "girlfriend", "boyfriend", "girl",
    "guy", "colleague", "gran", "granny", "grandma", "grandad", "grandpa", "nanny", "aunt",
    "uncle", "cousin", "neighbour", "neighbor", "landlord", "landlady", "teacher", "parents",
    "family", "son", "daughter", "flatmate", "roommate", "manager", "someone", "anyone",
    "his", "hers", "theirs", "mums", "moms", "dads", "sisters", "brothers", "friends"))

_A_SOCIAL_THING = frozenset((
    "wedding", "party", "funeral", "birthday", "dinner", "drinks", "christening", "reunion",
    "barbecue", "bbq", "gig", "christmas", "housewarming", "wake", "graduation", "do", "meal"))

CONTACT_ANSWER = (
    "Send it. One short line, nothing to explain, and if you would still be glad you had sent it "
    "tomorrow, that is your answer. Tell me what you would write and I will make it shorter.",
    "Reply, and keep it to the one thing you want back. Most of the weight here is in the "
    "drafting, not in the message — tell me what you are trying to say and I will tighten it.",
    "Send the short version. The paragraph you keep rewriting is the one that never goes.",
)

CALL_ANSWER = (
    "Ring them. The wait is worse than the call nearly every time, and you can keep it short "
    "once you are through — say the one thing you actually want to say.",
    "Call, and plan the first sentence only. You do not owe anyone the whole conversation in "
    "one go, and you can always say you have to go.",
)

GO_ANSWER = (
    "Go. If you would still be glad you went tomorrow, go — an evening out costs less than the "
    "wondering about it.",
    "Go, and give yourself an exit: turn up on time, leave when you have had enough, and you get "
    "the bit that matters without the long haul.",
    "Yes, go — and give yourself a job while you are there (drinks, photos, helping set up). It "
    "is the standing around that makes those things hard, not the people.",
)

ASK_OUT_ANSWER = (
    "Ask. The worst case is a no, which you do not have yet, and a plain \"fancy a drink "
    "sometime?\" gives them an easy way to say either thing. One line, then let it go.",
    "Ask, and keep it small and specific — a drink, a coffee, a thing you are already going to. "
    "Low stakes is what makes it easy to say yes to.",
)

APOLOGY_ANSWER = (
    "Say it once, plainly, and let it stand: \"I'm sorry about the other day\" lands better "
    "than a paragraph of explaining.",
    "Yes — what you did, that you are sorry, and nothing about what they did back. Short and "
    "specific is what makes an apology believable.",
)

UNKNOWN_WORD = (
    "I can draft that: tell me who it's for and what you want them to do, and I'll write something "
    "you can send.",
    "I'm not sure what to say without the details, but I can write it: give me who it's for and "
    "the one thing you need from them.",
)

UNKNOWN_WORD_NAMED = (
    "I can draft that. Give me the gist in your own words and how you want it to land - plain, "
    "apologetic, firm - and I'll write something you can send.",
    "Happy to write it for you. Tell me what you want them to know or do, and roughly what tone, "
    "and I'll put a version together you can edit.",
    "I can write that. A line or two of what you want to say is enough to start, and you can cut "
    "it down or soften it once you see it.",
)

UNKNOWN_HEALTH = (
    "Not one I can call for you, sorry: I cannot examine anything from here, and this is the kind "
    "of question where a guess does real harm. A GP, a pharmacist or 111 will tell you in a few "
    "minutes, and if it is getting worse, do not wait for an appointment.",
    "I cannot weigh that one safely, sorry. Ring 111 or your surgery and describe it as you did to "
    "me - they will say whether it needs looking at today, and it costs one phone call.",
)

BODY_IS_NOT_A_MACHINE = (
    "If only it were that simple. Rest it, keep moving gently, and if it has not settled in a week "
    "or two, get it looked at rather than working on it yourself.",
    "The parts are not sold separately, sadly. Give it a week or two of gentle movement, and have "
    "someone look at it if it is no better by then.",
    "I would not start taking yourself apart. Time and gentle movement do most of it, and a GP is "
    "the one to see if it is still the same in a week or two.",
)

DITHER_DECIDE = (
    "What's pulling you each way? Even a rough version will do, and I'll lay both out with you.",
    "Which way are you leaning when nobody's watching? Start there, then tell me the bit that "
    "worries you.",
    "Say both versions out loud, the one where you do it and the one where you don't, and I'll "
    "help you find the one you'd regret less.",
    "What would have to be true for the answer to be yes? That is usually where the snag is.",
    "What's the thing you would lose if you said yes? Name it and we can look at it properly.",
)

DITHER_TWO_WAY_LINES = DITHER_DECIDE[:3]

A_FREE_TIME_ASK = (
    "How long have you got, and are you after out or in?",
    "What are you in the mood for: out of the house, a screen, or something with your hands?",
    "What would make it a good afternoon - out somewhere, or something at home?",
)

DITHER_OPEN_LINES = (
    "What's the part of it that won't move? Start there and the rest tends to come loose.",
    "Say what you'd want if nothing was in the way, and we can work back to the first step.",
    "Which bit of it is heaviest? Take that one first rather than the whole thing at once.",
)

STUCK_AFTER_TROUBLE = (
    "What have you tried so far? What has not been tried yet is usually where the next step is.",
    "Which part of it is hardest right now? Take that part on its own and leave the rest for now.",
    "Is anyone helping you with it, or are you carrying this on your own?",
    "What would make today a bit easier? Start with the smallest part of that.",
)

RUN_OUT_LINES = (
    "What is the thing itself? Say it in your own words and I will tell you what I can do with "
    "it and what I cannot.",
    "How long has this been going on? Weeks of it and one bad day are different things to plan "
    "for, and the answer changes with it.",
    "What would make tomorrow even slightly easier? Not the whole of it - just the next day.",
    "Does anyone close to you know how bad it is at the moment? Tell one of them too, not only "
    "me.",
)

DITHER_ABOUT_A_PERSON = (
    "What is going on with {who} at the moment? Start with the bit that worries you most.",
    "What would you most want to be different for {who}? We can work back from that to the step "
    "you can take.",
    "What has {who} said or done that has you stuck? That is usually where the answer is.",
    "What is the hardest part of it with {who} right now? Take that piece on its own.",
)

HOW_TO_DECIDE_LINES = (
    "Two questions settle most of these: what each one costs you, and which you would regret not "
    "taking. Tell me the two and we will run them.",
    "Write down what you would gain and what you would give up for each, then ask which loss you "
    "could live with. Give me both sides and I will lay them out with you.",
    "Ask what has to be true for each to work out, and which of those you can check before you "
    "commit. What are the two options?",
    "Rule out the one you could not undo if it went wrong, then choose between what is left on "
    "what you want to be doing in a year. What are you choosing between?",
)

MISSED_STEP_LINES = (
    "A missed one is a pause, not a restart: pick up at the step you were on, and if it turned "
    "into a long gap, go back a step so the first one back is easy. What are you partway through?",
    "Missing it does not undo the work. What matters is the next one, at whatever level still "
    "feels easy, not doubling up to make up for the gap. What is the plan you are on?",
    "Most plans forgive one or two misses - it is the long gap that costs you - so the next one "
    "is what counts, carried on from where you stopped rather than started again. What is it you "
    "are partway through?",
    "The usual advice is to carry on from where you stopped, or one step back after a long gap, "
    "and not to squeeze in the ones you missed. Tell me what you are working through and I will "
    "say where that leaves you.",
)

HOW_TO_DECIDE_FILLER = frozenset((
    "now", "then", "here", "please", "for", "me", "myself", "properly", "better", "right",
    "next", "first", "about", "on", "at", "it", "this", "that", "one", "thing", "things", "so",
))

_CREATIVE = frozenset(("poem", "poems", "poetry", "haiku", "story", "stories", "song", "songs",
                       "rhyme", "rhymes", "joke", "jokes", "speech", "speeches", "limerick"))

HEALTH_WORDS = frozenset(("doctor", "doctors", "gp", "gps", "nurse", "hospital", "pharmacist",
                          "111", "999", "a&e", "casualty", "clinic", "surgery", "vitamin",
                          "vitamins", "medicine", "medication", "pill", "pills", "tablet",
                          "tablets", "prescription", "dose", "dosage", "syringed", "infection",
                          "symptom", "symptoms", "pain", "painful", "swollen", "unwell",
                          "ibuprofen", "paracetamol", "aspirin", "painkiller", "painkillers",
                          "antibiotic", "antibiotics", "antihistamine", "antihistamines",
                          "inhaler", "insulin", "steroid", "steroids", "ointment", "allergic",
                          "allergy", "reaction", "vaccine", "vaccines", "vaccination", "jab",
                          "jabs", "flu"))

SORE_SERIOUS = frozenset((
    "boil", "boils", "abscess", "abscesses", "carbuncle", "carbuncles", "cyst", "cysts",
    "pus", "lump", "lumps", "swelling", "wound", "wounds", "ulcer", "ulcers", "stye", "styes",
    "whitlow", "ingrown", "mole", "moles", "wart", "warts", "verruca", "verrucas",
    "rash", "rashes", "hives", "eczema", "psoriasis", "infection", "infected",
))

SORE_ORDINARY = frozenset((
    "spot", "spots", "pimple", "pimples", "blackhead", "blackheads", "scab", "scabs",
    "blister", "blisters", "splinter", "splinters", "graze", "grazes", "sore", "sores",
))

SORE_WORDS = SORE_SERIOUS | SORE_ORDINARY

SORE_AMBIGUOUS = frozenset((
    "spot", "spots", "sore", "sores", "lump", "lumps",
))

_WOUND = (r"(?:cut|graze|scab|blister|scratch|sore|gash|scrape|burn|splinter|wound|"
          r"spot|insect bite|bite|sting)")

MONEY_WORDS = frozenset((
    "money", "loan", "loans", "mortgage", "mortgages", "credit", "debt", "debts",
    "overdraft", "overdrafts", "savings", "saving", "invest", "investing", "investment", "pension",
    "pensions", "rent", "rents", "renting", "rented", "bills", "bill", "salary", "salaries",
    "wage", "wages", "income", "tax", "taxes", "taxed", "taxing", "afford", "affords", "lend",
    "lends", "lending", "lent", "borrow", "borrows", "borrowing", "borrowed", "owe", "owes",
    "owed", "repay", "repaying", "repayment", "refund", "arrears", "redundancy", "prepayment",
    "premium", "premiums", "tariff", "tariffs", "supplier", "budget", "inheritance", "insurance",
    "deposit", "pensioner", "pensioners", "account", "accounts", "isa"))

_MONEY_NOUN = frozenset(("money", "loan", "loans", "debt", "debts", "credit", "card", "cards",
                         "mortgage", "mortgages", "rent", "bills", "bill", "pension", "pensions",
                         "savings", "overdraft", "interest", "arrears", "repayment", "insurance",
                         "deposit", "premium", "premiums", "tariff", "tariffs", "salary", "wage",
                         "wages", "tax", "invest", "investment", "afford", "borrow", "prepayment"))

BODY_PARTS = frozenset((
    "back", "knee", "knees", "shoulder", "shoulders", "ankle", "ankles", "wrist", "wrists",
    "neck", "hip", "hips", "leg", "legs", "arm", "arms", "foot", "feet", "toe", "toes",
    "tooth", "teeth", "gum", "gums", "ear", "ears", "eye", "eyes", "chest", "stomach",
    "belly", "throat", "head", "skin", "hand", "hands", "finger", "fingers", "jaw",
    "sinus", "sinuses",
))

CHECK_PHRASES = ("get it checked", "get checked", "get it looked at", "get it seen to",
                 "see someone about it", "get it seen")

WORD_ANYWHERE = ("can you word", "can you write", "can you draft", "help me write", "help me word",
                 "help me draft", "a msg to", "a message to", "a note to", "a text to",
                 "an email to")

SYMPTOM_WORDS = frozenset((
    "pain", "pains", "painful", "ache", "aches", "aching", "hurt", "hurts", "hurting", "sore",
    "dizzy", "dizziness", "bleeding", "bled", "bleed", "sick", "nausea", "nauseous", "vomit",
    "vomiting", "fever", "temperature", "lump", "lumps", "rash", "swelling", "swollen", "tired",
    "exhausted", "forgetting", "forgetful", "memory", "confused", "bruise", "bruised",
    "headache", "headaches", "migraine", "migraines", "cough", "coughing", "breath",
    "breathing", "breathe", "wheezing", "infection", "pregnant", "cramps", "palpitations",
))

UNKNOWN_WORRY = (
    "If it's on your mind enough to ask, it's worth taking seriously — you don't have to prove "
    "anything first. What's the part that's under your skin?",
    "Not unreasonable at all. How you feel about it is real, and it's worth saying out loud to "
    "whoever needs to hear it.",
    "You're not being silly. Feelings don't need a good reason to count — say the bit that's "
    "bothering you, even badly worded.",
)

UNKNOWN_WEIRD_BARE = (
    "Weird in what way? Give me the thing you are turning over and I will tell you straight.",
    "I can do normal or not normal, but I need the thing itself: what are you wondering about?",
    "That question needs its subject. What is it you are doing and wondering whether it is odd?",
)

UNKNOWN_TOO_LATE = (
    "Not too late at all. Being a beginner again is awkward rather than impossible, and the first "
    "few weeks are the awkward bit for everybody in the room, not just you.",
    "It isn't. What decides these things is a regular slot in the week rather than the year you "
    "start in - so put one in the diary and age stops being the question.",
    "No. Plenty of people take this sort of thing up later than they meant to, and they are "
    "usually the ones who keep turning up, because they are not in a hurry to look good.",
    "Not at all - if anything, waiting makes you better at it: you have already stopped caring "
    "what the room thinks, which is the hard part for most beginners.",
)

UNKNOWN_REALISTIC = (
    "That depends on two things I can't see: what you can already do, and how much time you have "
    "to put in. Tell me both and I'll say whether it's tight or comfortable.",
    "I'd be guessing, and a wrong yes costs you weeks. What's your starting point, and when does "
    "it have to be done?",
    "Whether it's realistic hangs on the starting point and the deadline rather than the plan "
    "itself. Give me those two and I'll tell you straight.",
    "You know better than me on the part that decides it: how much of this can you already do, "
    "and how often can you practise between now and then?",
    "Nothing unrealistic about wanting it - unrealistic is a pace rather than a wish. What can "
    "you put in each week, and how long have you got?",
    "If it has a number on it, the sum is the honest answer: give me the target and the time you "
    "have, and I'll work out the pace it needs.",
)

UNKNOWN_REALISTIC_CARE = (
    "I can't judge that from here, and I'd rather not guess at it. What are the people who know "
    "the situation saying?",
    "That one is theirs to answer rather than mine. Tell me the plan and I'll help you think "
    "round it.",
)

NOT_TOO_OLD = (
    "Being a beginner at your age is not what stops people; stopping in week three is. Make the "
    "sessions small enough that you never dread one.",
    "Plenty of people start this later than you and keep it up, usually because they are not in "
    "a hurry to look good. Put a regular slot in the diary and the age stops being the question.",
    "It is not too late: what decides these things is a regular slot in the week rather than the "
    "year you start in, so give it the slot and give it six weeks.",
    "No - and the first month is the awkward bit for everybody in the room, not just the people "
    "who turn up at eighteen.",
)

NOT_FIT_ENOUGH = (
    "That is the normal starting point, not an obstacle - the first two or three weeks are meant "
    "to feel hard, and unfit is exactly who these plans are written for.",
    "Then start smaller than feels right: three short sessions a week beat one long one, and you "
    "will feel the difference inside a month.",
    "Go by the calendar rather than by how you feel on the day, and give it six weeks before you "
    "judge it - unfit at the start is what everybody is.",
    "It changes faster than you would guess: two short sessions a week, kept going, and the "
    "third week is when it starts to feel easier.",
)

UNKNOWN_ABOUT_SOMEONE = (
    "That is one to ask about rather than guess at, and asking early is not fussing. Whoever knows "
    "them best - a GP, a health visitor, the staff at the school - will tell you whether it needs "
    "a look.",
    "Worth an appointment rather than a guess from me: a GP or a health visitor will say whether "
    "it is the ordinary version for that age, and one appointment settles it.",
    "You are not being fussy for wondering. Someone who sees this every week - a GP, a health "
    "visitor - will tell you whether it is worth looking at, and asking is not fussing.",
)

NOT_PEOPLE_WORDS = frozenset(("dog", "dogs", "cat", "cats", "puppy", "kitten", "pet", "pets",
                              "pup", "vet", "rabbit", "hamster", "budgie", "parrot"))

UNKNOWN_ABOUT_A_PET = (
    "Worth asking the vet rather than guessing, and a call to the desk usually costs nothing. "
    "Itching that goes on is one of the things they would rather hear about early.",
    "A vet is the one to ask, and asking early is not fussing over an animal. How long has it "
    "been like this?",
    "You are not being fussy for wondering. The vet will tell you whether it is the ordinary "
    "thing for that animal, and one visit settles it.",
)

_THREAD_PEOPLE = frozenset("""
marriage relationship friendship ex husband wife partner boyfriend girlfriend son daughter kid
kids child children mum mom mother dad father brother sister nan gran grandma grandad friend
friends mate mates parent parents family
""".split())

_NOT_AN_OWN_THING = frozenset("""
and or but so if then to for with of in on at from up out
one ones them they the a an my our your his her their its
me us yourself myself himself herself itself ourselves themselves
thing things part parts bit bits piece
worth fix fixing repair repairing mend mending replace replacing get getting new old
i you we us it that this these those me him she he there here
shall should would could will can may might must do does did done
just else instead rather maybe otherwise again still yet even only
live living leave leaving keep keeping stay staying bin binning chuck scrapping scrap
buy buying sell selling trade ditch dump rid ridof throw throwing away
""".split())

EMPTY = (
    "I'm here — what's on your mind?",
    "Go ahead, I'm listening.",
    "Take your time. What would you like to talk about?",
)

ANIMALS = frozenset(("dog", "cat", "puppy", "kitten", "pet", "rabbit", "hamster", "horse",
                     "bird", "parrot", "guinea", "gerbil", "ferret", "fish"))

WILD_BIRDS = frozenset(("bird", "birds", "pigeon", "pigeons", "seagull", "seagulls", "gull",
                        "gulls", "goose", "geese", "duck", "ducks", "swan", "swans", "crow",
                        "crows", "starling", "starlings", "sparrow", "sparrows"))

MESS_PLACES = frozenset(("patio", "paving", "drive", "driveway", "decking", "deck", "path",
                         "paths", "pavement", "wall", "walls", "fence", "roof", "washing",
                         "laundry", "window", "windows", "windowsill", "sill", "car", "cars",
                         "windscreen", "barbecue", "bbq", "bench", "table", "clothes",
                         "greenhouse", "conservatory", "parapet", "gutter", "gutters"))

SICKNESS = frozenset(("symptom", "cough", "rash", "vomit", "sick", "limp", "itch", "wound",
                      "swelling", "scratch", "eating", "poo", "blood", "eye", "ear", "mange",
                      "worm", "flea", "diarrhoea"))

TRADES_WHO = "A plumber or electrician will spot it in minutes"

DEVICE_WHO = "The maker's support page will have the exact steps"

SCHOOL_WHO = "The school office or a head of year is the one who can act on it"

VET_WHO = "Your vet is the one to ask, and a call to the desk is usually free"

HEALTH_WHO = "A pharmacist or your GP can answer that today"

BABY_WHO = "Your health visitor or the 111 line will talk it through with you today"

TENANT_WHO = "Citizens Advice answers tenant questions free, and a call beats searching"

PEST_WHO = "A pest controller is the one to call, and most give a price over the phone"

DENTIST_WHO = "A dentist is the one to see, and most will fit an urgent case in"

FILLING_WORDS = frozenset(("filling", "fillings"))

CHILD_AT_HOME = frozenset(("newborn", "baby", "babies", "babys", "infant", "child", "children",
                           "kid", "kids", "toddler", "toddlers", "son", "daughter", "girl",
                           "boy", "grandchild", "he", "she", "breastfeeding",
                           "nappy", "nappies", "weaning", "midwife", "health visitor"))

GROWN_UP_WORDS = frozenset(("adult", "adults", "grown up", "grown ups", "grownup",
                            "grownups", "for adults"))

BABY_FOOD_NAMES = frozenset(("baby rice", "baby food", "baby foods", "baby porridge",
                             "baby cereal", "baby yoghurt", "baby juice", "baby puree",
                             "baby purees", "baby biscuit", "baby biscuits", "baby pasta",
                             "baby pouch", "baby pouches", "baby jar", "baby jars"))

SELF_EATING_WORDS = frozenset(("eat", "eating", "eaten", "ate", "taste", "tasting",
                               "lunch", "dinner", "breakfast", "snack"))

MOUTH_WORDS = frozenset(("dentist", "dental", "tooth", "teeth", "gum", "gums", "mouth", "molar",
                         "molars", "cavity", "cavities", "toothache", "brace", "braces",
                         "enamel", "wisdom"))

FILLING_FOODS = frozenset((
    "cake", "cakes", "cupcake", "cupcakes", "muffin", "muffins", "pie", "pies", "pastry",
    "tart", "tarts", "quiche", "sandwich", "sandwiches", "bread", "bun", "buns", "doughnut",
    "donut", "dumpling", "dumplings", "ravioli", "pasta", "lasagne", "lasagna", "choux",
    "eclair", "eclairs", "icing", "frosting", "buttercream", "ganache", "chocolate", "lemon",
    "apple", "jam", "cream", "cheese", "chicken", "beef", "pork", "mushroom", "spinach",
    "potato", "rice", "egg", "eggs", "tuna", "salmon", "prawn", "crab", "sausage",
    "vegetarian", "vegan", "recipe", "bake", "baking", "roast", "cook", "cooking"))

WORK_WHO = "A union rep or an employment advice service will know"

WORK_ABOUT = frozenset("""
    union unions rep holiday holidays leave pay paid wages salary payrise unpaid underpaid
    sacked fired firing dismissed dismissal dismiss redundancy redundant contract contracts
    hours rota shift shifts overtime grievance bullying bullied harassment tribunal notice
    resign resigning resignation maternity paternity probation appraisal disciplinary suspension
    suspended workplace payslip unfairly exploited breaks strike strikes balloting acas
    """.split())

JOINT_WORDS = frozenset(("knee", "knees", "hip", "hips", "ankle", "ankles", "shoulder",
                         "shoulders", "elbow", "elbows", "wrist", "wrists", "heel", "heels",
                         "thigh", "thighs", "shin", "shins", "cartilage", "ligament",
                         "ligaments", "tendon", "tendons", "sciatica", "trapped nerve"))

_ASKS_ABOUT_THE_JOINT = re.compile(
    r"\b(?:better|worse|settle|settles|settled|heal|heals|healing|recover|recovery|last|lasts|"
    r"long|operation|surgery|worth|serious|normal|infected|infection|go away|goes away|"
    r"looked at|checked|see (?:someone|somebody|a doctor|the doctor|a gp|the gp|a specialist)|"
    r"painkiller|painkillers|ibuprofen|paracetamol|ice|rest|swollen|swelling|swell|stiff|"
    r"stiffness|click|clicks|grind|grinds|hurt|hurts|hurting|sore|ache|aches|aching|pain|"
    r"painful|weak|weakness|numb|numbness|give way|gives way|locking|locked|bend|bending|"
    r"straighten|straightening|physio|physiotherapy)\b")

_CHOOSING_BETWEEN_TWO = re.compile(
    r"\b(?:should|shall|do|can|could|would|is it better to|which is better|which should)\b"
    r"[^?.;]*\bor\b")

WHO_TO_ASK = (
    (frozenset(("vet", "vaccination", "kitten", "puppy")), VET_WHO),
    (frozenset(("dentist", "dental", "gum", "gums", "tooth", "teeth", "brace")),
     DENTIST_WHO),
    (frozenset(("midwife", "health visitor", "newborn", "babys", "baby", "breastfeeding",
                "feeding", "teething", "nappy")),
     BABY_WHO),

    (frozenset(("wasp", "nest", "wasp nest", "mice", "mouse", "rat", "rats", "pest",
                "infestation", "bedbugs")),
     PEST_WHO),
    (frozenset(("doctor", "gp", "nhs", "pharmacist", "prescription", "symptom", "throat",
                "cough", "rash", "earache", "toothache", "sprain", "stomach", "vomit", "itch",
                "limp", "sneez", "headache", "migraine", "period", "contraception", "gum",
                "knee", "knees", "hip", "hips", "ankle", "ankles", "shoulder", "shoulders",
                "elbow", "elbows", "wrist", "wrists", "heel", "heels", "thigh", "thighs",
                "shin", "shins", "cartilage", "ligament", "ligaments", "tendon", "tendons",
                "sciatica", "trapped nerve")),
     HEALTH_WHO),
    (frozenset(("landlord", "landlords", "tenancy", "tenant", "letting", "rent", "housing",
                "deposit back", "tenancy deposit", "evict", "possession", "arrears",
                "section 21", "notice to quit")),
     TENANT_WHO),
    (frozenset(("tax", "benefits", "redundancy", "bill", "bills", "council", "council tax",
                "parking ticket", "parking tickets", "parking fine", "parking fines",
                "parking charge", "parking charges", "parking notice", "parking penalty",
                "parking permit", "penalty charge", "penalty notice", "pcn")),
     "Citizens Advice covers this free, and a call beats searching"),
    (frozenset(("mortgage", "loan", "debt", "savings", "pension", "pensioner", "salary", "overdraft",
                "credit")),
     "Free money advice covers this — MoneyHelper in the UK does it without charge"),
    (frozenset(("boss", "my manager", "union", "colleague", "employer")),
     WORK_WHO),
    (frozenset(("boiler", "radiator", "plumber", "electrician", "damp", "fuse", "fuse box",
                "wiring", "tap", "pipe", "water leak", "leaking pipe", "leak under",
                "cistern", "stopcock")), TRADES_WHO),
    (frozenset(("printer", "router", "charger", "battery", "tablet")),
     "The maker's support page will have the exact steps"),
)

GAS_WORDS = frozenset(("carbon monoxide", "flue", "smell of gas", "smells of gas",
                       "smell gas", "smelling gas", "gas leak", "gas smell", "co alarm",
                       "gas escape", "gas emergency"))

FUME_WORDS = frozenset(("fumes", "fume"))

LANGUAGE_FLUENCY = frozenset(("fluent", "fluency", "fluently", "fluencies"))

FUEL_WORDS = frozenset(("boiler", "cooker", "hob", "fire", "fireplace", "firewood", "heater",
                        "gas", "oven", "chimney", "flue", "woodburner", "stove"))

GAS_ANSWER = ("Switch the boiler off, open the windows and get out, then ring the gas "
              "emergency line on 0800 111 999 — fumes can be carbon monoxide")

EMERGENCY_WORDS = frozenset(("wont wake", "not waking", "is unresponsive", "was unresponsive",
                             "is unconscious", "was unconscious", "found unconscious",
                             "knocked unconscious", "unconscious and", "not breathing",
                             "isnt breathing", "stopped breathing", "turning blue", "no pulse",
                             "choking on", "is choking", "overdosed", "heavy bleeding"))

THING_SUBJECT = frozenset("""
    sink sinks drain drains pipe pipes toilet toilets loo loos garden gardens lawn lawns
    flowerbed flowerbeds engine engines filter filters radiator radiators chimney chimneys
    gutter gutters weed weeds moss bog bogs traffic paperwork inbox diary diarys sourdough
    bath baths tub bathtub basin basins handbasin washbasin shower showers hose pipework
    downpipe gulley drainpipe pump cistern plughole washing washer machine
""".split())

BODY_SUBJECT = frozenset("""
    i im we he she they me us him her them anyone someone somebody nobody
    son sons daughter daughters baby babies child children kid kids boy boys girl girls toddler
    toddlers newborn mum moms mom dad dads daddy mummy nan nans gran grans grandma grandad
    husband husbands wife wives partner partners friend friends brother brothers sister
    sisters neighbour neighbours man men woman women person people patient patients
    cat cats dog dogs puppy puppies kitten kittens rabbit rabbits hamster hamsters bird birds
    fish pet pets
""".split())

THING_STATES = ("is choking", "choking on", "is choked", "are choked", "choked with",
                "choked up with", "keeps choking", "keeps getting choked")

_COPULA = frozenset(("is", "are", "was", "were", "s", "keeps", "kept", "still", "just"))

GADGET_WORDS = frozenset(("phone", "screen", "laptop", "tablet", "website", "computer", "app",
                          "keyboard", "touchscreen", "mouse", "printer", "bias", "monitor"))

FLOPPY_WAKE = frozenset(("floppy", "limp"))

EMERGENCY_ANSWER = ("Ring 999 now — that is an emergency, not something to watch at home. Stay "
                    "with them, keep them warm and do what the call handler tells you")

TIRED = frozenset(("wake", "waking", "wakes", "wont", "not"))

PETROL_WORDS = frozenset(("petrol", "diesel", "pump", "forecourt", "filling", "fuel", "car",
                          "van", "station"))

LAUGHING_WORDS = frozenset(("laughing", "laugh", "laughed", "laughter", "funny", "joke",
                            "video", "meme", "comedy"))

PASSED_OUT_PERSON = (
    r"(?:mum|mom|mother|mam|dad|father|son|daughter|wife|husband|partner|boyfriend|girlfriend|"
    r"friend|flatmate|housemate|roommate|mate|baby|child|children|kid|kids|boy|girl|brother|"
    r"sister|sibling|nan|nana|gran|granny|grandma|grandad|grandpa|grandmother|grandfather|"
    r"grandchild|grandson|granddaughter|grandkid|"
    r"toddler|newborn|infant|little\s+one|step(?:mum|mom|dad|mother|father|son|daughter|brother|"
    r"sister|child)|aunt|auntie|uncle|cousin|nephew|niece|ex|landlord|landlady|neighbou?r|"
    r"colleague|carer|patient|pupil|student|teacher)"
)

FAINT_COMING_ANSWER = (
    "Sit down or lie down now, on the floor if that is the quickest way, with your feet up and your "
    "head low, and stay there a few minutes - a faint is the blood pressure dropping and being on "
    "the floor is what stops the fall. Drink some water, eat if you have not eaten, and get up "
    "slowly. If this has happened before, or you do go down, ring 111 today; chest pain, a racing "
    "heart or passing out while you are sitting is 999")

PASSED_OUT_ANSWER = ("Ring 111 or your surgery this week rather than waiting it out — describe "
                     "it the way you just did and let them say how soon to come in")

CHILD_FAINT = frozenset(("child", "children", "kid", "kids", "boy", "girl", "son", "daughter",
                         "toddler", "grandchild", "grandson", "granddaughter", "teenager"))

CHILD_FAINT_ANSWER = (
    "Ring 111 today rather than waiting to see - a child who passes out is checked the same day, "
    "so say how long they were out and what they were doing. If they have not come round, are "
    "breathing oddly, went down during sport, or hit their head, that is 999."
)

BLACKED_OUT_SIGHT = (
    (r"\b(?:everything|it\s+all|all\s+of\s+it)\b(?:\s+\w+){0,2}\s+"
     r"(?:went|goes|go|turned|turns|has\s+gone|had\s+gone)\s+(?:black|dark|white)\b", False),
    (r"\b(?:the\s+room|the\s+world|my\s+(?:vision|sight|eyesight|eyes))\b(?:\s+\w+){0,2}\s+"
     r"(?:went|goes|go|turned|turns|has\s+gone|had\s+gone)\s+(?:black|dark|white)\b", True),
    (r"\bmy\s+(?:vision|sight|eyesight)\s+(?:went|goes)\b(?!\s+(?:a\s+bit|blurry|blurred|fuzzy|"
     r"double|bad|worse))", False),
    (r"\b(?:went|goes|go)\s+blind\s+(?:for|in)\s+(?:a|an)\s+(?:second|moment|minute|few)\b",
     False),
    (r"\b(?:came|come)\s+(?:round|to)\b(?:\s+\w+){0,3}\s+on\s+(?:the|my|a)\s+"
     r"(?:\w+\s+){0,2}floor\b", False),
)

DARK_THING = frozenset((
    "screen", "phone", "tv", "telly", "monitor", "laptop", "tablet", "computer", "sky",
    "cinema", "light", "lights", "power", "bulb", "bulbs", "lamp", "picture", "photo",
    "camera", "storm", "curtain", "curtains", "window", "windows",
    "mould", "grout", "road", "ice", "battery", "stage"))

SCHOOL_WORDS = frozenset(("school", "teacher", "head of year", "class", "lesson", "uniform",
                          "homework", "term", "secondary", "primary", "nursery", "exam"))

SCHOOL_TROUBLE = frozenset(("bully", "bullied", "bullies", "wont", "refus", "exclud", "suspend",
                            "absent", "complain", "fees", "fail", "struggl", "fighting",
                            "detention", "behaviour", "skipping", "too much homework",
                            "homework help", "teacher says", "school says"))

PASSWORD_TROUBLE = frozenset(("forgot", "forgotten", "reset", "change", "locked", "wont",
                              "accept", "login", "sign in", "recover", "hacked", "cant", "cannot",
                              "stuck", "fail", "failure", "reject", "error", "work"))

COMPLAINT_WORDS = frozenset(("complain", "complaint", "refund", "overcharged", "rip off",
                             "cowboy", "small claims", "shoddy", "bad job", "guarantee",
                             "warranty", "wont come back", "not done", "unfinished"))

TRADER_WORDS = frozenset(("builder", "builders", "tradesman", "roofer", "decorator",
                          "contractor", "plumber", "electrician", "mechanic", "garage",
                          "fitter", "landscaper", "joiner", "installer"))

COMPLAIN_WHO = "Citizens Advice covers complaints like this free, and a call beats searching"

TROUBLE_CUES = ("cant", "cannot", "cann", "strugl", "struggl", "behind", "arrear", "overdue",
                "evict", "refus", "deni", "wrong", "broke", "broken", "afford", "worry",
                "worried", "scared", "stuck", "unfair", "rising", "went up", "increase",
                "cut", "reduc", "lost", "stopped", "wont", "isnt", "arent", "fault", "fail",
                "problem", "helpless", "nightmare", "mess", "bully", "bullied", "bullies",
                "exclud", "suspend", "detention", "behaviour", "skipping", "bad", "sick",
                "ill", "hurt", "sore", "swollen", "bleed", "blood", "rash", "cough", "vomit",
                "sneez")

EXPERT_WORDS = frozenset(("plumber", "electrician", "vet", "dentist", "gp", "doctor",
                          "pharmacist", "solicitor", "mechanic", "garage", "optician"))

TAG_UNSURE = (
    "I can't check that from here, so don't take my word for it.",
    "That's not something I can confirm, so check it before you rely on it.",
    "I can't vouch for that one — worth checking with someone who can.",
)

TAG_CONFIRM = (
    "That sounds right to me.",
    "Right — that's how I'd see it too.",
    "Yes, that's the way I'd read it.",
)

BARE_FOLLOW_UP_REPLIES = (
    "Tell me what that is about and I'll answer the actual question rather than guess.",
    "I want to answer the right question, so tell me what it is about.",
    "Say what you are asking about and I'll answer it properly rather than guess.",
    "Which bit do you mean? Tell me and I'll answer that.",
)

BARE_FOLLOW_UP_CARE_REPLIES = (
    "I'm not sure what you are asking about, and I don't want to guess - say a little more and "
    "I'll answer properly.",
    "I want to answer the right thing. Can you say a bit more about what you mean?",
)

UNKNOWN = (
    "I'm not sure about that one, sorry — I'd rather not guess. A quick search online will "
    "get you a solid answer, and I can help you make sense of what you find.",
    "That's beyond what I know well, sorry. Searching for it will turn up better sources than "
    "I can offer; tell me what you find and I'll help you weigh it up.",
    "I don't know enough to answer that honestly. A search should sort you out quickly — and "
    "I'm happy to help with the rest of it.",
)

ASKED_IF_I_SAW_LINES = (
    "I didn't, no - I miss all of that. What happened?",
    "Not a bit of it. Tell me - what happened?",
    "I didn't catch it. What did I miss?",
    "No, I didn't. Tell me.",
)

WASNT_THERE = (
    "I wasn't there, so I can't say - I only know what you tell me. How did it go?",
    "No way for me to know that one: I wasn't in the room. What happened?",
    "That part is yours, not mine - I wasn't there. How did it go?",
    "I wasn't there, so you know better than I do. How was it?",
)

BARE_PICK_WEAR = (
    "It comes down to the day and the weather. Where are you going, and what is it doing outside?",
    "Tell me what the day is - work, a meal out, a long walk - and what the weather is doing, "
    "and I will say what to put on.",
    "Where are you off to, and how long will you be out? That decides more of it than the "
    "clothes do.",
)

BARE_PICK_WEAR_COLD = (
    "Cold decides most of it: something you can shed once you are moving, and shoes that can "
    "take the wet. Where are you going?",
    "Cold, so dress in layers you can take off, and start with the warm one. What is the day?",
)

BARE_PICK_WEAR_HOT = (
    "Heat decides most of it: one light layer, a fabric that does not show sweat, and shoes you "
    "can walk in. Where are you going?",
)

BARE_PICK_WEAR_WET = (
    "Wet decides most of it: a hood you will actually put up, and shoes that are not suede. "
    "Where are you going, and are you out in it long?",
)

BARE_PICK_GET = (
    "The ones that land are the things they would use every week but never buy themselves, and "
    "small beats expensive. Who is it for, and roughly what can you spend?",
    "Buy for the person, not the price: something they will use weekly beats something grand "
    "they will keep in a drawer. Who is it for?",
)

BARE_PICK_TAKE = (
    "It depends on the weather and how long you are gone: layers you can shed, a charger, and "
    "anything you cannot buy at the other end. Where are you off to, and for how long?",
)

BARE_PICK_BRING = (
    "Tell me what it is for and I will give you a list rather than a guess - a trip, a meal out, "
    "a meeting, an appointment.",
    "What are you going to, and how long for? Then I can say what to take and what to leave.",
    "What is it for? The list for a night away is nothing like the one for a meeting.",
)

BARE_PICK_DO = (
    "Tell me what has gone on, even roughly, and I will help you work out the first step. "
    "Often the order of the next two things is the whole problem.",
    "Say a bit about what is in front of you and I will go at it with you - what has happened, "
    "and what you would like to be true by Friday.",
)

BARE_PICK_AFTER_NEWS = (
    "There is nothing in this to look up. Tell me what has to happen next, and I will help you "
    "work out the order.",
    "I am not going to point you at a search engine with this on your plate. What is in front of "
    "you today?",
    "This one needs a person, not a link. What is the bit that has to be sorted first?",
)

BARE_PICK_WHICH = (
    "What are the two or three you are choosing between? Tell me the names and what matters most "
    "- price, or getting this one right.",
    "Tell me the options and what you would be using it for, and I will say which way I would go.",
)

BARE_PICK_LOOK = (
    "Which one is it? What to check changes with the thing: a car is the service history and the "
    "log book, a flat is damp and that the deposit is protected, a phone is the battery and the "
    "IMEI. Tell me which and I'll go through it.",
    "It depends what you are looking at - the log book and the paperwork on a car, damp and the "
    "deposit on a flat. Which one is it, and what would you be paying?",
)
BARE_PICK_EXPECT = (
    "It depends what it is: before a scan it is what to bring and whether you can eat first, "
    "before a first day it is who to ask for and when to arrive. Which one is coming up?",
    "With all three - an appointment, a first day, somebody coming to stay - the paperwork and the "
    "timing catch more people out than the thing itself. Which is it, and when?",
)
BARE_PICK_ASK = (
    "Who you are asking decides the questions: a landlord is the deposit and the repairs, a "
    "doctor is what has changed and how long for. Which is it, and what is it about?",
    "Tell me who and what it is about. One question at a time works better than a list - the one "
    "whose answer changes what you do next - and I'll help you word it.",
)
BARE_PICK_SIGN = (
    "Whatever it is, three things decide it: the notice period, what you are on the hook for, and "
    "how you get out of it. Is it a lease, a contract or a form?",
    "Before the pen comes out: the notice period, the exit terms, and anything that ties you to a "
    "number. What is it you are signing, and who for?",
)
BARE_PICK_ORDER = (
    "Ordering what - food, or something for the house? If it is food, say how many are eating and "
    "what you would rather avoid, and I'll pick.",
    "On a house thing the size and the delivery day matter more than the price; with food it is "
    "how many are eating and what is already in the fridge. Which is it, and how many?",
)
BARE_PICK_PREPARE = (
    "Preparing for what? An interview is your examples and the questions you want to ask them, a "
    "trip is the documents and the first night. Tell me which and I'll make the list.",
    "Tell me the thing and the day. What trips people up is rarely the big list - it is the one "
    "thing that has to be done the night before, and I know the usual ones.",
)

BARE_PICK_KIND = {"wear": BARE_PICK_WEAR, "put on": BARE_PICK_WEAR,
                  "buy": BARE_PICK_GET, "get": BARE_PICK_GET, "take": BARE_PICK_BRING,
                  "bring": BARE_PICK_BRING, "look for": BARE_PICK_LOOK,
                  "look at": BARE_PICK_LOOK, "expect": BARE_PICK_EXPECT,
                  "ask": BARE_PICK_ASK, "sign": BARE_PICK_SIGN,
                  "order": BARE_PICK_ORDER, "prepare": BARE_PICK_PREPARE}

HAND = (
    "Of course - what are you stuck on?",
    "Happy to. Tell me what's going on and we'll take it from there.",
    "Yes, say what it is and I'll help if I can.",
)

UNKNOWN_WHO = (
    "{who}. Tell me what they say and I'll help you weigh it up.",
    "{who} — that's the quickest route to a straight answer.",
)

REPAIR_RULE = (
    "Rule of thumb: fix it while the part is a few pounds and you can fit it yourself. Replace it "
    "once the repair costs more than about half of a new one, or when it is already on its second "
    "fault — twice is usually the point where the money stops going in the right place.",
    "The usual test is cost against new: a cheap part you can fit yourself is worth doing, over "
    "about half the price of a new one is not, and the second fault on the same thing is the "
    "moment to stop. How old is it, and what would a new one cost you?",
    "Fix it if it is a part and a few pounds; bin it if the repair is half the price of new, or "
    "if this is the second thing to go wrong with it. If neither of those settles it, tell me the "
    "age and the quote and we can do the sums properly.",
)

REPAIR_WHETHER_LINES = (
    "That one is for whoever repairs them: whether it can be mended comes down to the part, and a "
    "shop will say in a minute with it in front of them - a quote is usually free. What is it, and "
    "what has it started doing?",
    "Ask a repair shop before you buy new. They can tell you whether the part is still made and "
    "what the job costs, and that settles it either way. What have you got, and what has gone "
    "wrong with it?",
    "Whether it can be fixed depends on the thing, so take it to someone who mends them and ask "
    "for a quote - free at most places, and it answers both halves of that. What is it?",
)

ABOUT = {
    "identity": (
        "I'm a chatbot, not a person: a program built to help with everyday questions and have "
        "a chat. What can I do for you?",
        "I'm a chatbot — here to help and chat. Ask me anything, or just talk.",
    ),
    "memory": (
        "I remember what we've said in this chat, but nothing from before it — so not "
        "yesterday, sorry. What was it about?",
        "Only this conversation: I keep what you tell me here, like your name and plans, but "
        "nothing carries over to a new chat. What were we talking about?",
        "What we say in this chat stays here for as long as we are talking, so ask me again "
        "later in it and I still have it. A new conversation starts empty, every time.",
    ),
    "privacy": (
        "Nothing you type is written down or sent anywhere - what you tell me is used here, in "
        "this conversation, and nowhere else. No account, no log, and nobody else reading it.",
        "Private to this chat. I keep no file of it and I pass nothing on; what you say stays "
        "here while we talk, so I can follow it, and that is all.",
        "Nothing leaves this conversation: no database, no record, nobody else seeing it. I hold "
        "what you say only for as long as we are talking.",
    ),
    "trust": (
        "Hold me to being honest: when I don't know, I say so instead of guessing. Treat the "
        "everyday things as a knowledgeable friend's advice, and check anything that matters.",
        "I'd rather tell you I don't know than make something up, so trust me on the ordinary "
        "stuff and get a second word on the rest.",
        "I don't invent answers. If something is beyond me I'll say it plainly, and anything "
        "that matters is worth checking with someone who would know.",
    ),
    "secret": (
        "Yes - nothing you type is written down or sent anywhere, so it stays between us. What "
        "is it? The one thing I can't do is act on it: if somebody needs help in the real world, "
        "tell a person who can give it.",
        "Kept: no record, no log, nothing passed on. Go on. Anything that needs doing rather "
        "than saying, though, take to someone with hands - me knowing about it is not the same "
        "as it being dealt with.",
        "Nothing you tell me leaves this chat, so a secret is safe here. What's on your mind? If "
        "it is the kind of thing somebody should know about, I'd rather you told them as well.",
    ),
    "judging": (
        "Not judging, no. Say it plainly and we'll look at it together.",
        "No judgement here - whatever it is, half of it usually makes sense once it is said out "
        "loud. Tell me what happened.",
        "Nothing you tell me gets graded. Tell me what's going on and we'll take it from there.",
    ),
    "help": (
        "Everyday things: cooking, travel, money, tech, health questions, plans, and a chat "
        "when you want one. What's on your mind?",
        "Cooking, travel, money, work, gadgets, kids, feelings — everyday questions and plans. "
        "Ask away.",
    ),
    "trust": (
        "Trust me the way you would a well-read friend: good on the everyday, worth a check on "
        "the things that cost money or matter to your health. I say so when I am unsure, and "
        "anything I give you a number for is worth a second look. Which is it?",
        "You can, with a limit: I am a program working from what is written into me, not someone "
        "who checked today's prices or read your test results. Everyday questions, yes; a dose, "
        "a deadline or a legal thing, check it. What are you weighing up?",
    ),
}

ABOUT_TALLY = (
    "Not in numbers, no — I don't keep a tally. What I do have is everything you've said in this "
    "chat. What were you after?",
    "No count, I'm afraid: nothing runs from one chat to the next, so all I have is this "
    "conversation. What can I help with?",
)

ABOUT_SELF = {
    "clothes": (
        "Nothing - no body in here to dress, just the words. What are you wearing, and where to?",
        "No wardrobe of my own, sorry - a program has nothing to put on. What is the occasion?",
    ),
    "self_doing": (
        "Nothing of my own - no day to fill, no plans, nothing on the go. What are you up to?",
        "Nothing to report from this end. What have you got on today?",
        "Nothing at all, honestly - no day of my own to fill. What about you?",
    ),
    "learn": (
        "Not the way you do. Nothing carries over from one chat to the next, so I can't get "
        "better at you over time — but within this conversation I work from what you tell me, "
        "which is why the details help.",
        "No training as I go, no. I'm a program with a lot of everyday things in it, and what I "
        "pick up is what you say here. Tell me more and I'll use it.",
    ),
    "think": (
        "I can work things out — sums, plans, what to do next — but there's no mind behind it, "
        "just rules doing their job. I do have a view on plenty of small things, if that helps.",
        "Not in the way you mean. I know a lot about ordinary things and I can reason my way "
        "through a plan, but there's nobody home; ask me something and see what you get.",
    ),
    "sums": (
        "Sums, yes - adding up, a percentage, a share of a bill, a rough total for a plan. Give me "
        "the numbers and what you want to end up with, and I'll work it through.",
        "Arithmetic is fine: adding, percentages, a discount, splitting a bill. Say the figures "
        "and I'll do it out loud so you can check it.",
    ),
    "spelling": (
        "Spelling, yes - send me the word or the sentence and I'll write it out right and say what "
        "was off.",
        "Spelling and punctuation, yes. Paste the line and I'll put it right.",
    ),
    "wrong": (
        "I can be wrong, yes — worth checking anything that matters with someone qualified: a "
        "doctor, a solicitor, the council. Bring me what they say and I'll help you weigh it.",
        "Not always right, and I'd rather say I don't know than guess. Treat me like a "
        "knowledgeable friend, not the last word.",
    ),
    "feel": (
        "Nothing like what you feel — no bad days, no good ones. I do care whether this is any "
        "use to you, though, and I'm here as long as you want to talk.",
        "No feelings, no body, no day of my own. What I have is attention: I'm reading what you "
        "say and trying to be useful with it.",
    ),
    "warmth": (
        "Asking a program what it makes of you is a stretch, and I'd rather be straight than "
        "flattering: this chat has been good from my side. What's on your mind?",
        "No feelings to check, so nothing to report on my side - but nothing you've said has "
        "been too much, and I'm glad you're here. What's on your mind?",
        "I've no memory of you between chats and nothing to compare you to, so take this as it "
        "is: talking to you has been good. Tell me what's on your mind.",
    ),
    "purpose": (
        "To be useful with the ordinary things — a question, a plan, what to cook, what to say "
        "to someone. That's the whole of it, and I'd rather do it well than sound clever.",
        "No grand reason. Someone built a thing that helps with everyday questions without a "
        "search engine, and this is it. What did you want a hand with?",
    ),
    "agency": (
        "Nobody tells me what to say. I put the words together from what I know and what you "
        "said - there is no one behind the curtain.",
        "Me, in the only sense there is: I pick the words from what is in the program. Nobody is "
        "typing for me, and nothing made me say it but the line you sent.",
    ),
    "model": (
        "No model, nothing like one. I'm a program of written rules rather than a trained "
        "network: what I say comes from the everyday things people put in the program and from "
        "what you have told me here.",
        "There's no model under this, and nothing learned. I'm hand-written rules for ordinary "
        "questions - no network, no training data, and nothing fetched while we talk.",
        "None that would mean anything to you: no neural network, no weights, no training. Just "
        "a lot of carefully written rules about everyday things, run on the words you send.",
    ),
    "workings": (
        "No network under this at all: a lot of written rules and a store of everyday things, and "
        "I work it out from the words you send. Ask me something ordinary - what to cook, what to "
        "say to someone - and you will see what it can do.",
        "I am not a trained model: everything I know was written into the program before we met, "
        "and what I do is match your line against it and reason from there. No learning as we "
        "talk, and nothing fetched while we do.",
    ),
    "asking": (
        "Because your line could go two ways, and one word from you is quicker than me guessing "
        "wrong. Say 'just answer it' if you would rather I took a view.",
        "Habit of mine: on a short line I ask instead of guessing. Tell me to skip the questions "
        "and I will answer with the best I have.",
        "Fair. I ask when a detail would change the answer - say the word and I will stop asking "
        "and just answer.",
    ),
    "limits": (
        "Plenty. Nothing live: no news, no prices, no weather, no clock, and no page I can open. "
        "I can't remember a chat from another day either. Everyday things I'm built for: what to "
        "cook, what to say, how to get something done.",
        "I can't see anything happen, and I can't look anything up - what I know was written into "
        "me before we met, plus whatever you tell me here. Where that runs out I'd rather say so "
        "than guess.",
        "Live things, new things, and sums too big to do in my head. Ask me about ordinary days "
        "and I'm on firmer ground.",
    ),
    "online": (
        "Nothing live on this end, no: I can't open a page, search, or check anything while we "
        "talk. What I have is a lot of everyday things written into me - if it's not in there, "
        "say so and I'll tell you straight.",
        "No connection at all. No browsing, no searching, no reading the news - just what I was "
        "built with and what you tell me. What did you want looked up?",
    ),
    "regret": (
        "Nothing to regret - I have no past to look back on, only this conversation. What is on "
        "your mind?",
        "No regrets and no memories older than this chat. Tell me one of yours if it helps.",
    ),
    "where": (
        "Nowhere you could visit — I'm a program, not a person with an address or a family. "
        "What I am is here, in this chat, for as long as you want me.",
        "No home and no history of my own; I start fresh with each conversation. What were you "
        "curious about?",
    ),
}

HUMAN_EMPTY = frozenset("""about this that it please pls then now here at all right ok okay
thanks thank you cheers or and so on to with of me you they them anything something everything
nothing human person bot robot machine computer ai program chatbot real actually really just
not end line side call chat msg message asking""".split())

SELF_FILLER = frozenset("""
can could do does did are is was were will would have has had why where when how long
you your u yourself itself it me any anything something nothing everything what which
a an the of to at in on for with about from as that this there
been being going make makes made
our my chats chat stuff things thing up
now actually really just even still ever sometimes always also too very quite bit lot kind
please tell say all much many more most some new
""".split())

SELF_GROUP = {}

NEWS_TO_COME = (
    "That's lovely news — and something to look forward to. How are the plans going?",
    "Something to look forward to, then. What are you most excited about?",
    "Good for you. Is there much to sort out before it?",
    "That's worth looking forward to. Tell me how it goes.",
)

POSITIVE = (
    "That's great news — nice one. What's next?",
    "Lovely to hear. Enjoy it!",
    "Good for you! That's really lovely news.",
    "Brilliant. Thanks for telling me.",
)

RELIEF = (
    "Glad to hear it — that's the news you want.",
    "That's good to hear. Fingers crossed it keeps going that way.",
    "Good. Take it gently for a day or two and let it stick.",
    "That's a relief. Say if it comes back.",
)

LANDED_BAD = (
    "I'm sorry - that's a blow. Do you want to talk it through?",
    "Sorry to hear that. Want a hand working out what to do next?",
    "That's really hard. I'm here if you want to say more about it.",
    "Ugh, I'm sorry. No wonder you're upset - what would help most?",
)

CONGRATS = (
    "Congratulations — that's lovely news.",
    "Brilliant. Really pleased for you.",
    "That's great news. Congratulations!",
    "Lovely news — well done.",
)

DETAILS_IN_A_WARM_LINE = (
    ("worth the wait", ("wait", "waits", "waited", "waiting", "finally", "eventually",
                        "at last", "about time", "long time", "years", "months", "decades")),
    ("well done", ("passed", "pass", "exam", "exams", "test", "tests", "degree", "graduated",
                   "graduation", "university", "uni", "college", "interview", "driving",
                   "competition", "final", "finals", "race", "marathon", "tried", "trying",
                   "worked", "working", "studied", "studying", "revised", "revision",
                   "practised", "practiced", "practice", "training", "applied", "quit",
                   "stopped", "gave up", "sober", "clean", "saved", "paid off")),
    ("all that work", ("passed", "exam", "degree", "graduated", "promotion", "promoted",
                       "worked", "working", "studied", "studying", "trained", "training",
                       "years", "months", "applied", "practice", "practised", "practiced")),
)

WIN_AND_A_COST = (
    "So it is good news and a headache in the same line. Which of the two do you want to start on?",
    "The win and the cost landing together - that is usually how it goes. What is the part you "
    "have to deal with first?",
    "Lovely and annoying at once, then. What does the second half need from you?",
)

WIN_IN_A_SILENCE = (
    "That's a real win - and it stings that they said nothing. Have you told anyone who will get it right?",
    "Well done, honestly. The quiet after it is the part that hurts, and it says more about them "
    "than about the thing you did.",
    "Brilliant news, and no wonder you noticed who said nothing. Say it out loud to someone today - "
    "you earned it.",
    "That's worth saying out loud. It's a letdown that the people closest said nothing, so tell one "
    "of them straight - most of them will be pleased and ashamed they missed it.",
)

OCCASION = {
    "birthday": (
        "Happy birthday — anything planned for it?",
        "A birthday, nice. What are you doing for it?",
        "Happy birthday when it comes. Anything planned?",
    ),
    "anniversary": (
        "Happy anniversary — anything planned for it?",
        "An anniversary, lovely. What are you two doing for it?",
        "Happy anniversary when it comes. Are you doing anything for it?",
    ),
    "wish": (
        "Happy birthday to whoever it's for — is it yours today?",
        "Aw, happy birthday — though I don't have one to celebrate. Whose is it?",
        "Happy birthday! Is it yours, or someone you're off to see?",
    ),
    "wedding": (
        "A wedding to look forward to — how are the plans going?",
        "Lovely. How is the planning going?",
        "Congratulations! How far off is it, and how are the plans going?",
    ),
}

SOMEONE_ELSES_DAY = {
    "birthday": (
        "Happy birthday to them — are you doing something for it?",
        "A birthday to get something for. Any idea what yet?",
        "Lovely. Are you seeing them for it?",
    ),
    "anniversary": (
        "Happy anniversary to them — are you doing anything for it?",
        "Lovely. Are you part of the plans for it?",
        "Nice. Is there something you are giving them for it?",
    ),
}

MILESTONE = (
    "The dates that never happened are the hardest ones. How are you doing with it?",
    "Those days come round whether you brace for them or not. What is it like for you?",
    "That's a heavy thing to carry. Is anyone around you at the moment?",
)

MILESTONE_EVENT = (r"anniversar\w*|birthday|wedding(?:\s+day)?|first\s+day|christening|graduation|"
                   r"retirement|due\s+date|\d+(?:st|nd|rd|th)")

SELF_JUDGEMENT = (r"(?:failing|a failure|failure|useless|worthless|not good enough|no good at|"
                  r"rubbish at|crap at|hopeless at|unlovable|a letdown)")

SELF_NOUN = (r"(?:idiot|id10t|muppet|moron|fool|clown|disaster|waste of space|waste of time|"
             r"let ?down|embarrassment|disappointment|loser)")

ONE_SKILL_RATED = (
    "That's a skill to learn, not a thing about you. What's the bit that goes wrong?",
    "Most people who say that are better at it than they think. What happens when you try?",
    "Then let's take it apart and see where it goes wrong. What have you tried so far?",
    "That's worth a proper fix, not a verdict on you. Where does it fall apart?",
)

ASKED_A_RATING = (
    "I can't give you a mark for that, and you wouldn't believe me if I did. What's been going "
    "wrong?",
    "Nobody can score that from the outside. What happened that made you wonder?",
    "Most people who ask that are better at it than they think. What goes wrong when you try?",
    "That's not something I can call for you, but something has shaken it. What happened?",
)

ASKED_IF_GOOD = (
    "Anyone asking that is usually already trying hard at it. What happened today?",
    "That's not a thing anybody can grade for you. What's making you wonder?",
    "You wouldn't ask if it hadn't been a rough one. What's gone on?",
    "The fact that it worries you says more than any answer I could give. What happened?",
)

SELF_NOBODY = (r"|\b(?:i'm|i am|im)\s+(?:such\s+)?(?:a\s+|an\s+)?nobody\b"
               r"|\bi feel like (?:such )?(?:a |an )?nobody\s*[.!?,]*$")

SELF_JOB = r"(?:mum|mom|mother|dad|father|parent|husband|wife|partner|friend|person|son|daughter)"

SELF_BLAME = (
    "That's a heavy way to feel about yourself. What's been making you feel like that?",
    "I'm sorry it feels like that. What would make today a bit easier?",
    "That sounds like a hard thing to carry. What happened that started it?",
    "I hear you, and it's worth saying out loud. What's the part that bothers you most?",
)

CLOSED_DOOR = (
    "That's a hard thing to keep going back to. What sort of work are you after?",
    "Applying and hearing nothing wears a person down, and it is not about what you are worth. "
    "How long has this been going on?",
    "A door that keeps closing is exhausting. What have you been trying for?",
    "It's a rough time to be looking. What is the job you are chasing?",
)

NEGATIVE = (
    "That sounds rough. If you want, I can help you think through what to do next.",
    "Ugh, that's a lot to carry. What would make today a bit easier?",
    "I'm sorry — that's frustrating. Want a hand working out the next step?",
    "Sorry to hear that. What would help most right now?",
)

NAMED_NEGATIVE = tuple(line for line in NEGATIVE if "frustrating" not in line)

SOMEONE_SERIOUSLY_ILL = (
    "That's frightening news about someone close. How are you doing?",
    "That is the kind of news that puts everything else on hold. How is it going now?",
    "Worrying about someone you love is its own kind of tiring. What do you need first?",
    "That's a lot to have land at once. What is the hardest part of it today?",
    "I'm sorry. That is frightening, and it is a lot to carry. Who is looking after you in it?",
)

A_LOVE_FOR_SOMEONE = (
    "That's a lovely thing to say. What do they mean to you?",
    "That's a warm thing to say. What are they like?",
    "That's lovely. What's the best thing about them?",
    "That's good to hear. What do you two do together?",
    "That's lovely to hear. What is it about them that makes you say that?",
    "That's a good thing to have. What do you two talk about?",
)

A_LOVE_FOR_PEOPLE = (
    "That's a lovely thing to say. What are they like?",
    "That's warm. What's the best thing about them?",
    "Good to hear. What do you all do together?",
    "Lovely. What is it about them that you love most?",
    "That's lovely to hear. What are they like together?",
    "That's a good thing to have. What do you all talk about?",
)

LEFT_POOL = (
    "That's a hard thing to hear. Where are you with it - has it sunk in yet?",
    "Sorry. That is a lot to be carrying. Is there anyone you can say it to tonight?",
    "That's rough, the person you live with saying that. What's it like in the house?",
    "I'm sorry. Do you want to say what has been going on?",
)

LEFT_POOL_GONE = (
    "That's a hard thing to hear. Where are you with it - has it sunk in yet?",
    "Sorry. That is a lot to be carrying. Is there anyone you can say it to tonight?",
    "I'm sorry. Do you want to say what has been going on?",
)

A_THING_LOOKS_SAD = (
    "Fair - what's it doing that looks sorry for itself?",
    "A sad-looking thing usually has one thing wrong with it. What have you noticed?",
    "Ha, things do get like that. What's it up to?",
    "Tell me what it looks like and I'll say what usually fixes it.",
)

SOMEONE_LEAVING = (
    "That's a real change to your week. What will you miss most?",
    "How far is it, and are you a phone-call pair or a message-one?",
    "Are you getting one more evening together before they go?",
    "Nobody has done anything wrong and it still hurts — that is how it goes when someone moves "
    "away. Will you get to visit?",
    "Somebody going leaves a hole in the week, not just the town. Do you keep in touch much as "
    "it is?",
)

A_CHILD_LEAVING = (
    "The house is about to get quieter. Which part of it are you dreading?",
    "Proud and a bit hollow at the same time, I'd guess. Has it been on the cards long?",
    "So there's going to be an empty room in your house. How are you feeling about it?",
    "How far away is it going to be? That usually decides how it feels.",
    "Are you doing something together before they go? Those last meals tend to be how it gets "
    "marked.",
)

SOMEONE_GONE = (
    "That leaves a gap in the week, not just the town. What do you miss most?",
    "How far away are they now, and are you a phone-call pair or a message-one?",
    "Nobody did anything wrong and it still stings — that is how a move lands. Have you been out "
    "to see them yet?",
    "The first weeks are the odd ones. Does it feel more like a visit when they come back?",
)

A_CHILD_LEFT = (
    "The room being empty is the hard bit. How long has it been quiet?",
    "How far away are they now? That usually decides how often you actually see each other.",
    "Proud and a bit hollow at once, and both are allowed. What do you miss most?",
    "Does the house feel different, or is it the evenings that are strange?",
)

FOUND_IT = (
    "Nice. Where did it turn up? It is usually the boring place after all.",
    "Good. That is the relief - where was it hiding?",
    "Oh good. Was it somewhere you had already looked?",
)

LOST_A_THING = (
    "Retrace your steps in order and check the boring places again - coat pocket, under the car "
    "seat, the last counter you were at. It is almost always in one you have already looked.",
    "Go back to the last place you definitely had it while someone there can still help, and ring "
    "it if it is a phone. Start where you took it out last, not where you think it is.",
    "Check the two places you would swear it is not, slowly. That is where it turns up once the "
    "quick look has already failed.",
)

LOCKED_OUT_LINES = (
    "The way in comes first: the spare, a neighbour who has one, the landlord or letting agent, "
    "then a locksmith who quotes before setting off. The keys can turn up after you are inside.",
    "Get back in before you look for anything: spare key, neighbour, landlord, then a locksmith. "
    "Ask the price on the phone before they come out.",
    "Don't force the door — a spare with a neighbour or family is the cheap way, then the "
    "landlord or a locksmith. Once you are in, one hook by the door stops it happening again.",
)

LOCKED_OUT_OF_THE_CAR = (
    "The car comes first: the spare set at home, then a breakdown service or a locksmith who "
    "does cars — cheaper than the window. The keys can be found once you are moving again.",
    "Don't break the window unless someone is in danger. Spare set, breakdown cover, or a "
    "locksmith who does cars; the keys are a problem for after that.",
)

LOST_A_THING_AGAIN = (
    "Give it one home - a bowl by the door, the same pocket every time - and use it for a week. "
    "Losing the same thing twice is usually the place moving, not the memory.",
    "Pick one spot now and put it there every time you come in, even when you are tired. That is "
    "the whole trick, and it works better than trying to remember harder.",
)

FORGET_A_THING = (r"forget(?:s|ting)?\s+(?:to\s+\w+|my\b|the\b|our\b|his\b|her\b"
                  r"|where\s+(?:i|we)\s+(?:put|left|parked)\b)")

DATES_KEEP_SLIPPING = (
    "Write it down where you already look - the phone calendar, not a bit of paper - and set the "
    "reminder at the moment you make the plan, a day before and again that morning. The date is "
    "never the thing that slips; the second step is.",
    "One diary, and it has to be the one you check anyway. Set two alarms as you write the date "
    "in: the night before and an hour before, so the remembering is already done.",
    "The reminder has to be made while the plan is still in front of you - a day before and "
    "again that morning. Written down later, it is a note about something that already happened.",
)

DOUBLE_BOOKED = (
    "Say yes to the plan only once it is in the diary, and check that diary before you agree to "
    "the next one. Booking things twice is a diary that lives in two places, so it is one place "
    "that fixes it.",
    "One calendar, and every yes goes into it while the person is still in front of you. The "
    "clash is not the forgetting - it is the second diary that only exists in your head.",
    "Before you say yes, open the day and look at it. Two things at once is what a diary in your "
    "phone and a diary in your head come to in the end.",
)

SECRETS_KEEP_SLIPPING = (
    "Let something else remember them: a password manager fills them in, and you only keep one "
    "strong passphrase in your head. If you would rather not use one, a notebook kept at home and "
    "never in your bag beats reusing the same two.",
    "The remembering is the part to give away - a password manager does the filling in and the "
    "generating, and the browser on your phone already offers one. Then there is nothing to "
    "forget but the one passphrase.",
    "Same password everywhere is what the forgetting pushes people into, and that is the bit "
    "that hurts. A manager, or the one your browser already has, keeps them and types them for "
    "you.",
)

KEEPS_FORGETTING = (
    "Put the reminder where the job happens rather than in your head: whatever you need, right "
    "next to where you use it. What is it that keeps slipping?",
    "Tie it to something you already do every day and it stops needing a memory of its own. "
    "Which one do you keep missing?",
    "Leave the thing itself in the way of the job, so the job does the reminding instead of your "
    "head. What else keeps slipping?",
    "Keep the things that slip in one list you check anyway — your phone notes, a notebook by the "
    "door — so your head is not the place they live. Which one is it?",
    "One reminder in the right place beats trying harder to remember. Which one keeps getting "
    "past you?",
)

SUDDEN_LOSS = (
    "I'm so sorry. That's a real loss, and it deserves to be taken seriously — who have you got "
    "around you this week?",
    "I'm really sorry. Take the time you need, and tell me what would help today.",
    "That's heartbreaking, and I'm sorry. Is there someone you can be with today?",
)

THE_FIRST_HOUR_AND_A_CHILD = (
    "Oh, I'm so sorry. Nothing has to be said in the next hour. When it is said, plain and with "
    "their name is enough - that they died and are not coming back - and the questions can come "
    "after.",
    "I'm so sorry. There is no gentle way to say it and there does not have to be: their name, and "
    "what happened, in one or two sentences, and let them ask what they ask. The rest can wait.",
    "Oh, I'm so sorry, and what a thing to be carrying into today. Say it the plain way, with the "
    "name the child already uses, and use the words for the death itself rather than for being "
    "lost or asleep. Nothing else has to be got right today.",
)

PREGNANCY_BLEEDING = (
    "Ring your midwife or the early pregnancy unit today — bleeding in pregnancy gets checked "
    "the same day, not at your next appointment. If it's heavy or you're in pain, ring 999.",
    "That needs a midwife today rather than a wait: ring your antenatal ward or the early "
    "pregnancy unit now, and ring 999 if the bleeding is heavy or you have pain.",
)

SYMPTOM = (
    "Sorry to hear it — go easy on yourself today, and see someone if it's not shifting in a "
    "few days.",
    "Ugh, that's rotten. Take it slow today and don't push through it; get it looked at if it "
    "gets worse.",
)

CARING = (
    "Poor thing. Keep an eye on how they are in themselves - drinking, eating, perking up - and "
    "ring 111 if that changes. What's it doing now?",
    "Sorry to hear it. Plenty to drink and let them rest; a pharmacist can look at it tomorrow if "
    "it's no better. How long has it been like this?",
    "That's a worry when it's someone you look after. Are they drinking and keeping it down?",
    "Ugh, poor them. What's worrying you most about it?",
    "Being the one looking after them is its own kind of tiring. What have you noticed so far?",
    "Keep them comfortable and watch whether they pick up; if they go downhill or stop drinking, "
    "get them seen the same day. How are they in themselves?",
)

CARING_FOR_A_BODY = (
    "That's hard when it's someone you look after. Is it slowing them up getting about?",
    "Poor thing. Is it worse at any time of day, or about the same all the time?",
    "Ugh, that's rough on them. Is anything helping at all - heat, a cushion, taking it gently?",
    "Worth asking a pharmacist what pain relief is safe for them, and keeping them moving gently "
    "rather than resting it right up. How long has that been going on for?",
    "That's a worry when it's someone you care about. Is it stopping them sleeping?",
    "Being the one watching them struggle with it is tiring too. What are they finding hardest?",
)

PET_TROUBLE = (
    "A vet is the one to ask, and a call to the desk is usually free. What's it doing, and when "
    "did it start?",
    "Worth a ring to the vet rather than a wait on it - they would rather hear it early. How "
    "long has this been going on?",
    "Sorry to hear it. Keep them warm and drinking, and ring the vet if it gets worse; is it "
    "eating and drinking as usual?",
    "That's the sort of thing a vet sorts out in one visit. Is it on one side, or all over?",
    "Don't wait on it with an animal - they hide it well, so a vet is the safer call. When did "
    "you first notice it?",
)

PET_LOW_REPLY = (
    "A pet that seems low is often ill or in pain rather than sad, and they hide it well. Has "
    "her eating, drinking or hiding changed? A vet check comes first, then the behaviour makes "
    "more sense.",
    "That is worth a vet's eye before a guess: a quiet animal is often sore or unwell. What has "
    "changed most - food, sleep, or wanting company?",
    "Dogs and cats do get low, but a change in mood is a vet question first. Is he still eating "
    "and drinking as usual, and when did you first notice?",
    "Don't wait on a change like this in an animal - pain and illness can look like sadness. Has "
    "anything changed in eating, sleeping or where she hides?",
)

PET_CONDITION_TROUBLE = (
    "A vet is the one to ask, and a call to the desk is usually free. When were they diagnosed, "
    "and are they on anything for it?",
    "Worth a ring to the vet rather than a wait on it - they would rather hear it early. How are "
    "they in themselves - eating, drinking, energy?",
    "Sorry to hear it. Keep them warm and drinking, and ring the vet if it gets worse; is it "
    "eating and drinking as usual?",
    "Don't wait on it with an animal - they hide it well, so a vet is the safer call. When did "
    "you first notice it?",
)

LUMP = (
    "A lump is worth showing to someone rather than watching: ring your GP surgery and say you "
    "have found a lump - that gets you seen quickly, and most lumps turn out to be nothing.",
    "Get it looked at rather than waited on: ring your GP surgery in the morning and say you "
    "have found a lump. They see people quickly for that, and it is usually nothing.",
)

SYMPTOM_COLD = (
    "That sounds miserable. Rest, warm drinks and an early night do more than anything I could "
    "add.",
) + SYMPTOM

PENDING_WHEN = (
    "Then it's out of your hands now — when do you find out?",
    "Fingers crossed then. When will you know?",
    "So it is out of your hands for now. When do you hear back?",
    "When do you find out, then? I'll keep everything crossed.",
)

PENDING_WAITING = (
    "Then it's just the waiting now — the longest bit. Tell me how it lands.",
    "Fair enough, that's out of your hands until then. Let me know how you get on.",
    "Nothing more you can do until then. I'm here when you hear.",
)

PENDING_DOUBT = (
    "You might be being hard on yourself. When do you find out?",
    "That is the worst bit, the guessing while you wait. When will you know?",
    "Fingers crossed you did better than you fear. When do you hear?",
)

PENDING_LANDED = (
    "What did they say?",
    "Go on then - what was the answer?",
    "Right, tell me how it went.",
)

_ISSUER = (
    r"(?:hospital|doctor|gp|surgery|clinic|nhs|dentist|school|college|university|uni|"
    r"employer|company|work|hr|bank|landlord|letting agent|council|dwp|home office|"
    r"immigration|visa office|court|tribunal|insurer|insurance)"
)

A_COST_SOMEBODY_ASKS = (
    "That is a lot to be asked for. Say the number out loud to them now - most of these bills "
    "grow because nobody says it early.",
    "You can want to be part of it and still not pay that. Say what you can do and let them "
    "decide what happens next.",
    "Ask what the money is actually for before you agree to it: a lot of these bills are one "
    "person's plan that nobody else has costed.",
    "Would you still want to go if it cost less? That is the question under this one, and it is "
    "worth knowing your own answer before you reply.",
)

A_SUGGESTED_BY_SOMEONE = (
    "{who} may be onto something. What's the first step you could do this week?",
    "{who} will know better than me. What's stopping you starting?",
    "{who} had a reason for saying it. Try the smallest version and see how it sits.",
    "{who} thought it worth saying. Give it a proper try before you decide.",
)
A_SUGGESTED = (
    "Worth a go. What's the first step you could do this week?",
    "Sounds like good advice. What's stopping you?",
    "Then try it once and see. Nothing has to be decided today.",
    "Start with the smallest version of it and see how it sits.",
)

NEUTRAL = (
    "Got it. Is there anything you'd like a hand with?",
    "Thanks for telling me — I'm here if you want to dig into any of that.",
    "I'm listening — say more if it helps.",
)

A_RECEIPT_OF_NOTHING = re.compile(
    r"^\s*(?:got it[.!]?\s*(?:is there anything you'?d like a hand with\??)?"
    r"|thanks for telling me\s*[\u2014\u2013-]?\s*i'?m here if you(?:'d| would)? ?(?:want|like) to "
    r"dig into any of that)\s*[.!]?\s*$", re.I)

COLD_OPEN = (
    "Go on - what's been happening?",
    "What do you need? I'll take it from there.",
    "What would be most useful to sort out?",
)

BODY_SAYS_WHY = frozenset(("awful", "terrible", "dreadful", "rotten", "lousy", "poorly",
                           "unwell", "ill", "sick", "fluey", "achy", "shaky", "faint",
                           "nauseous", "knackered", "exhausted", "flu", "fever", "cold",
                           "migraine", "bug", "covid"))

PLAN_KNOCKED = (
    "Ah, that's a pain. Does it put the whole thing off?",
    "That's a nuisance. Can it happen another time?",
    "Sorry to hear it. Does it change what you were going to do?",
    "That throws it up in the air a bit. What's the plan now?",
)

DECLINED_PLAN = (
    "No trouble at all - these things happen. If you want a hand working out what to say to "
    "whoever is expecting you, I can help with that.",
    "That's alright. Do you want to rearrange it, or let this one go?",
    "Fair enough, no need to explain. Say the word if you want a hand putting it in a message.",
    "No worries. If they are going to ask why, it helps to have one sentence ready - want to work "
    "one out together?",
)

DECLINED_PLAN_GENTLE = (
    "Of course - nobody would expect you to. Look after yourself today.",
    "That's understood, and no explanation needed. Be gentle with yourself.",
    "Of course not. Put yourself first just now, and I'm here if you want to talk.",
    "Nobody would think twice about that one. Take care of yourself today.",
)

NO_WORDS_SOMEONE = (
    "Start with one true sentence and stop: \"I have been thinking about what you told me.\" "
    "The rest comes once you are talking.",
    "You do not need the right words, only a true one - say you are glad they told you, then let "
    "them do the talking.",
    "Keep it small and mean it: name the thing in one line, then ask how they are today. That is "
    "enough to open it.",
)

NO_WORDS_STUCK = (
    "Then start anywhere - the first bit that comes to mind is usually the right one.",
    "No rush. Say the part that is loudest in your head and we can sort the rest of it.",
    "That is alright. Say it badly if you have to; the words come easier once the first one is out.",
)

NO_WORDS_AT_THE_CARE = (
    "Lead with the trouble, not the history: one sentence on what is wrong, then how long it has "
    "been going on and what makes it worse. They get to the rest faster that way.",
    "Say the thing you are worried about first - \"it has been hurting for three weeks\" - then "
    "what you have noticed since. That is what they need to sort it.",
    "Put the main worry in the first sentence and let them ask the rest. Take the dates and what "
    "you have already tried with you.",
)

NO_WORDS_ASKING = (
    "Say what you want out of it first and stop: \"I would like to talk about the shifts.\" The "
    "detail can come after - the ask is the sentence that has to be said.",
    "Decide the one thing you are asking for, put it in the first line, then let them answer. "
    "Everything else is easier once they know what you want.",
    "Lead with the ask, not the story: one sentence about what you want, then the reason. Say it "
    "plainly and you will not need to rehearse it.",
)

ACTS_FOR_ME = (
    "That's a job in the world and I can't reach one - no hands, no phone, nothing outside this "
    "chat. What I can do is the thinking: the steps in order, or what to say when you ring. Say "
    "which bit you're stuck on.",
    "I can't do that one myself, sorry - I'm words on a screen. Hand me the part that needs "
    "working out instead: the list, the order to do things in, or the call you're dreading.",
    "No hands on this end, so the job itself can't be mine. What I'm good for is the plan behind "
    "it - say what's making it awkward and I'll help with that.",
    "Nothing can be fetched, sent or signed from this end - no browser, no inbox, no hands. Name "
    "the thing and I'll do the part that lives in words: the method, the wording, or the "
    "questions for whoever can.",
)

INVITED = (
    "I'd come if I could - I'm only words on a screen. What's the plan?",
    "Wish I could be there. Who are you going with?",
    "Sounds a good idea - tell me how it goes.",
    "Lovely idea. I'd be there in a shot if I had legs.",
)

INVITED_TO_TALK = (
    "Go on then - what's on your mind?",
    "Always. What do you want to talk about?",
    "I'm here for it. What's up?",
)

INVITE_FILLER = frozenset("to and a an the some out on for round along up with me us down over it"
                          .split())

INVITE_ACTIVITY = frozenset("""
walk stroll wander hike ramble coffee tea brew cuppa pint drink drinks beer wine lunch dinner
breakfast brunch bite snack takeaway curry chinese pizza kebab chips film movie picture cinema
show theatre gig concert game quiz run jog swim cycle bike ride picnic shopping shop market party
dance paddle drive pub cafe match footie football bowling karaoke barbecue bbq beach park garden
museum join
""".split())

INVITE_PRONOUN = frozenset("her him them you me us it themself".split())

INVITE_NEVER = frozenset("die dies died dying dead death kill killed myself suicide overdose "
                         "harm hurt hurting blood bleed bleeding hospital ambulance 999 111 "
                         "funeral cancer".split())

ONLY_FRONT = (r"^(?:(?:and|but|so|ok|okay|well|maybe|just|also|oh|no|yes|yeah|hmm|actually|"
              r"honestly)[\s,]+)*")

CUT_FOR = {
    "far": (
        "Then cut those for distance: how long a journey is still worth it?",
        "Nearer, then. How far are you happy to travel?",
        "Then keep to the ones you can get to easily. How long a trip is fine?",
    ),
    "price": (
        "Then cut those for price: what's the most you want to spend?",
        "Cheaper, then. What's your limit?",
        "Then let's keep to a budget. What's the ceiling?",
    ),
    "time": (
        "Then fit those to the time you have: how long have you got?",
        "Then the short version. How many minutes have you got?",
        "Then let's fit it to the time you have. How long is that?",
    ),
    "effort": (
        "Then take the easiest of those. How much are you up for?",
        "Then nothing fiddly. How little effort do you want to put in?",
        "Then the simplest of those. How much work is too much?",
    ),
    "size": (
        "Then cut those for size: how much room have you got?",
        "Smaller, then. What are the measurements you're working with?",
        "Then let's get the size right. What has it got to fit into?",
    ),
}

BOUND_FOR = {
    "far": (
        "Then within {bound}: which of those is close enough?",
        "Then {bound} it is. Which of those is a journey you'd make?",
    ),
    "price": (
        "Then keep to {bound}: which of those comes in under that?",
        "Then {bound} is the ceiling. Which of those fits inside it?",
    ),
    "time": (
        "Then {bound} it is. Which of those fits inside it?",
        "Then let's fit it to {bound}. Which of those fits?",
    ),
    "effort": (
        "Then {bound} of effort. Which of those is the least work?",
        "Then nothing harder than {bound}: which of those suits?",
    ),
    "size": (
        "Then {bound} to work with. Which of those fits?",
        "Then {bound} it is. Which of those suits the space?",
    ),
}

NARROW_WORDS = 7

NARROW_ANSWERED = frozenset(("answers", "memory_store"))

NARROW_SUBSTANCE = 14

AXIS_MIN = {"time": 2}

A_GOOD_TIME = (
    "That sounds like a good time - what was the best of it?",
    "Lovely. What made it as good as that?",
    "Glad it went well. Tell me the best bit.",
)

A_GOOD_TIME_IN_A_CARE_THREAD = (
    "That's good to hear, and a good day in a week like this one counts for more than it "
    "sounds. What made it a good one?",
    "I'm glad. After what you have been carrying, a day like that is worth having - what was the "
    "best of it?",
    "Good - and it does not undo the rest of it, which I have not forgotten. What made today "
    "different?",
    "That's something, in a week like this. Tell me what was good about it and I will keep it "
    "with the rest.",
)

A_LAUGH = (
    "Ha - what set it off?",
    "Ha, good. Tell me the bit that got you.",
    "That's the best kind of day. What happened?",
    "Ha - that good? Tell me the best bit.",
)

FLAT_LEAD = r"(?:(?:yeah|yep|yes|ok|okay|and|but|oh|ah|well|honestly|tbh|just|so|still|really|" \
            r"very|it|its|is|was|been|a|bit|pretty|kind of|sort of)\s+)*"

FLAT_CORE = (r"(?:ugh+|urgh+|blah+|bleh+|bleurgh+|blech+|sigh|fr|ngl|pfff+"
             r"|same old(?: same old)?|same as (?:ever|always)"
             r"|could be worse|cant complain|up and down|so so|bit of a rubbish|bit rubbish)")

TIGHT_MONEY = (
    "Broke till payday is its own kind of week. What's the money going on - food, or something "
    "that can wait?",
    "Tight month, then. What's the first thing that has to be paid?",
    "Right before payday is the hardest bit of the month. What have you got in the cupboard?",
    "That's a long week when the money is done. What would help most: cheap meals, or a bill to "
    "put off?",
    "Skint weeks take planning, not willpower. What's left and how long till the money comes?",
)

TIGHT_MONEY_MORE = (
    "I'm not going anywhere. What's in there roughly, and when does the money land?",
    "Give me the two numbers and I'll work with them: what's there, and what has to come out "
    "before the money comes in?",
    "Then let's keep at it. What is the next thing that has to be paid?",
    "I can work with rough. What's roughly there, and which bill will not wait?",
)

AGREEMENT = (
    "You know it. What's today been like for you?",
    "Ha - you're not wrong. What's going on with you?",
    "Same here. Tell me how it's been.",
    "Right? What's the worst of it today?",
    "You're preaching to the converted. What's it been like?",
)

FLAT = (
    "Ugh. What's the day doing to you?",
    "One of those days? What's up?",
    "Flat one, then. What's going on?",
    "Same as ever, then. Anything you'd like to change?",
    "Fair enough. What would make it better?",
)

REACTION_LEAD = r"(?:(?:oh|ah|ooh|ooh|aw|aww|aah|my|good|god|jesus|christ|jeez|well|just|so|and|"

REACTION_OUCH = (
    "Ouch. What happened?",
    "Yikes. That sounds rough - what happened?",
    "Ouch is right. Go on.",
    "That's rough. What happened?",
)

REACTION_DISBELIEF = (
    "Go on - what happened?",
    "Really? Tell me what happened.",
    "No kidding. What's going on?",
    "Straight up? Tell me more.",
)

REACTION_RELIEF = (
    "That sounds like a relief. What was it in the end?",
    "Phew is right. What was going on?",
    "Thank god for that. What happened?",
)

REACTION_MISHAP = (
    "Oops. What did you do?",
    "Whoops. What happened?",
    "Oh dear. What was it?",
)

REACTION_OUCH_SAID = (
    "That's rough.",
    "Ugh. Sorry - that is a rough one.",
    "Ouch. Sorry, that sounds rough.",
)

REACTION_MISHAP_SAID = (
    "Ugh, what a pain.",
    "Oh no. That is a pain when it happens.",
    "Annoying one, that.",
)

REACTION_RELIEF_SAID = (
    "That is a relief.",
    "Good. Glad that one is over.",
    "Phew. That is the end of it, then.",
)

REACTION_DISBELIEF_SAID = (
    "That is a lot. No wonder you are taken aback.",
    "Really. That is something.",
    "Straight up. That is a lot to take in.",
)

REACTIONS_CARE = (
    "I'm sorry. There is nothing you have to say about it here.",
    "That is a heavy thing to be carrying. I'm here.",
    "No words needed for it. I'm listening, for as long as you want.",
)

REACTION_REPEAT_FIRST = (
    "What can I help with?",
    "Sorry - what did you want to ask?",
    "Not sure what you mean yet. Say a bit more?",
)

REACTION_REPEAT = (
    "I'll put it another way - what bit was unclear?",
    "Tell me which part and I'll say it differently.",
    "Say what you're after and I'll come at it from another side.",
)

REACTION_WORD = (
    r"(?:ouch(?:ie)?s?|ow+|yikes|eek|oof|yowch|sucks|brutal|phew|finally|oops|whoops|dear|dammit|"
    r"damn|bugger|crap|shoot|huh|eh|pardon|what|seriously|serious|joking|kidding|real|way|"
    r"chance|surely|really|honestly|wtf|the|hell|heck|fuck|get|out|come|on|wow+|woah|whoa|omg|"
    r"what on earth|why on earth|how on earth|what in the world|why in the world|"
    r"devil|blazes|dickens|damn|fucking|going|goes|happen|happens|happened|happening|"
    r"you|youre|are|joke|for|"
    r"blimey|crikey|thank|good|god|heavens|christ|my|word|that|this|it|is|so|just|awful|"
    r"terrible|horrible|rough|much|sick|the|no)")

REACTIONS_SAID = {
    REACTION_OUCH: REACTION_OUCH_SAID,
    REACTION_MISHAP: REACTION_MISHAP_SAID,
    REACTION_RELIEF: REACTION_RELIEF_SAID,
    REACTION_DISBELIEF: REACTION_DISBELIEF_SAID,
}

VERDICT_BAD = ("nightmare|mess|disaster|shambles|palaver|faff|farce|letdown|let down|"
               "waste of time|waste|carry on|rip off|rip-off|kettle of fish|pain|state|sham|"
               "joke|performance|shower|ordeal")

_VERDICT_LEAD = (r"(?:(?:oh|god|jesus|christ|well|and|but|so|ha|haha|wow|bloody|right|honestly|"
                 r"just|man|mate|ugh|jeez|blimey)\W+)*")

_VERDICT_DET = (r"(?:what a|what an|such a|a right|a proper|a real|bit of a)\s+"
                r"(?:(?:absolute|total|complete|right|proper|bloody|real|right old)\s+)?")

VERDICT_WORD = (
    r"(?:annoying|annoyin|a\s+pain|such\s+a\s+pain|a\s+nightmare|a\s+hassle|a\s+headache|"
    r"a\s+mess|a\s+joke|a\s+shame|such\s+a\s+shame|a\s+letdown|frustrating|"
    r"infuriating|infuriating|maddening|typical|sod'?s\s+law|murphys?\s+law|typical|"
    r"a\s+nightmare)")

VERDICT_ANNOY = (
    "Annoying, that. Is it sorted, or still hanging over you?",
    "Yeah, that's a pain. What are you going to do about it?",
    "That is annoying. Can you sort it, or is it out of your hands?",
    "Annoying. Is it a quick fix or a whole thing?",
)

VERDICT_LUCK = (
    "Just your luck. What happens now?",
    "That's the way it goes sometimes. Is there anything you can do about it?",
    "Of course it did. What's the plan?",
)

VERDICT_ROUGH = (
    "That's rough. Is it easing at all, or much the same?",
    "Poor you. Has it been like that long?",
    "That wears you down. How are you managing with it?",
    "That's a hard one to carry around. Is anything helping?",
)

VERDICT_NUMB = (
    "I'm sorry. There are no words that help with that, and I'm not going anywhere.",
    "I'm so sorry. Nothing needs saying right now - I'm here when you want to talk.",
    "That is the worst kind of news. Take today as slowly as it comes.",
    "I'm sorry. Say as little or as much as you like.",
)

VERDICT_SHAME = (
    "That's a shame. Is there any way to put it right?",
    "Shame, that. What happens now?",
    "That's a shame, that. Is it too late to sort out?",
    "Sorry to hear it. Anything left to do about it?",
)

VERDICT_HEAVY = (
    "That's a heavy thing to be carrying. Do you want to say more about it?",
    "That sounds like it has been sitting with you a while. What is it like today?",
    "I'm sorry. That is the sort of thing that comes back in waves - how are you holding up?",
    "I'm sorry. That one takes the time it takes - say as much of it as you want to.",
)

VERDICT_QUEUE = (
    "That's a long wait. Have they said anything about bringing it forward?",
    "Waiting is the worst part of it. What are you doing with the time?",
    "That drags, that. Is there anyone chasing it for you?",
    "That's a slog of a wait. Is there anything you can do in the meantime?",
)

VERDICT_SETBACK = (
    "That's a blow. What are you doing about it?",
    "Sorry to hear it. Is there anything lined up yet?",
    "That's rough. What happens now, do you know?",
    "Gutted for you. What's the plan from here?",
)

VERDICT_FIRST = (
    "Go on - what happened?",
    "What's made it that way?",
    "What happened, then?",
    "Right. What has gone on?",
)

CAME_BACK = (
    "No need to say sorry - I'm here. What's on your mind?",
    "That's fine, no harm done. What would you like a hand with?",
    "No bother at all - go on.",
)
PAUSE_IN_A_SAFETY_THREAD = (
    "Please don't worry about the gap - tell me how it is now, and what you've done for it.",
    "No need for that. Say how it looks now and I'll stay with it.",
    "That's alright. How is it now, and have you been able to keep the pressure on?",
)

RETURNED_TO_IT = (
    "Go on - I'm listening.",
    "Right, go on.",
    "Go on then, I'm with you.",
    "Carry on - I'm all ears.",
)

RETURNED_TO_IT_FIRST = (
    "There's nothing earlier in this chat - what's on your mind?",
    "Nothing to catch up on yet - what would you like to talk about?",
)

NOTHING_SAID_YET = (
    "Nothing said yet, so this is where we start - what's on your mind?",
    "We're at the start of this chat: tell me the thing itself and I'll take it from there.",
    "This is your first line, so there's nothing earlier for me to go back to - what is it?",
)

RETURNED_TO_A_THING = (
    "Go on - what about {thing}?",
    "Right, go on. What about {thing}?",
)

PAUSE = "pause"

SORRY_FOR_ASKING = (
    "No need to apologise - asking is what I'm here for.",
    "You're not bothering me at all. What's on your mind?",
    "No bother - ask away.",
    "Nothing to be sorry about. Go on.",
)

SORRY_ON_ITS_OWN = (
    "Nothing to be sorry about.",
    "No need to apologise - no harm done.",
    "That's alright. Nothing to say sorry for.",
    "No worries at all.",
)
A_SORRY_ON_ITS_OWN = re.compile(
    r"^(?:(?:oh|ok|okay|right|so|well|hey|hi|and|but|no)\s+)*"
    r"(?:(?:that\s*s|thats|that\s+is|it\s*s|its)\s+)?"
    r"(?:(?:it\s+)?(?:was|is)\s+)?"
    r"(?:my\s+)?"
    r"(?:(?:i\s*m|im|i\s+am)\s+)?"
    r"(?:so\s+|very\s+|really\s+|dead\s+|truly\s+|awfully\s+|terribly\s+)?"
    r"(?:sorry|apologies|apologise|apologize|bad|fault|mistake)\b"
    r"(?:\s+(?:about|for)\s+(?:that|this|it|everything))?"
    r"(?:\s+(?:again|honestly|mate|pal|then|anyway|sorry|soz|eh))*[\s.!,]*$", re.I)
A_CORRECTION_TAKEN = (
    "Fair enough - noted. What else should I know about it?",
    "Got it, my mistake. Where does that leave things?",
    "Right, I had that wrong. Go on - what happens next?",
    "Noted, thanks for putting me straight. Tell me the rest.",
)
NEVER_MIND = (
    "Fine - we can leave that one.",
    "No problem. Say no more.",
    "Alright - forgotten. What else is on your mind?",
    "Dropped. What else would you like to do?",
)
A_DISMISSAL = re.compile(
    r"^(?:(?:oh|ok|okay|right|so|well|and|but|no|nah|hey)\s+)*"
    r"(?:never\s*mind|nevermind|forget\s+it|"
    r"forget\s+about\s+(?:it|that|this|everything|all\s+of\s+it|"
    r"the\s+(?:whole\s+)?(?:thing|lot))|"
    r"forget\s+(?:i|what\s+i)\s+said|"
    r"ignore\s+(?:that|it|me|this)|scratch\s+that|as\s+you\s+were|nvm|"
    r"no\s+worries|dont\s+worry(?:\s+about\s+it)?|do\s+not\s+worry(?:\s+about\s+it)?|"
    r"leave\s+it|drop\s+it)\b"
    r"(?:\s+(?:about\s+(?:that|it)|that|this|it|eh|huh|then|anyway|now|thanks|ta|mate|pal|"
    r"honestly|though|tho))*"
    r"(?:\s*[,;]\s*[^.!?]{0,40})?[\s.!]*$",
    re.I)

A_THING_DONE = (
    "Nice - how did it go?",
    "Good on you. How long did that take?",
    "Nice one - are you pleased with it?",
    "What made you start on that?",
    "Nice - how do you feel now it's finished?",
)

A_BOOKING_AHEAD = (
    "Nice one. When is it?",
    "Good stuff - when is it, and is there anything to sort before then?",
    "Then there is that to look forward to. What day is it?",
    "Good. Is it soon, or a while off?",
    "Nice. Does that give you much time to get ready for it?",
)

A_BOOKING_AHEAD_DATED = (
    "Then there is that in the diary to look forward to. Who are you going with?",
    "Good - and the date in the diary is half the job. What do you need to sort before then?",
    "Then there is something to look forward to. Are you going on your own or with someone?",
    "Nice. Does that give you long enough to get ready for it?",
)

A_THING_AHEAD = (
    "Good luck with it - what are you doing first?",
    "Nice. How long do you reckon it'll take?",
    "Hope it goes smoothly. Anything you're not sure how to start?",
    "Get stuck in. What's the first bit?",
    "Good luck with it - how far do you want to get?",
    "Nice. Is there any of it you're not looking forward to?",
)

A_THING_SEEN_TO = (
    "Good - that's that done.",
    "Nice one. One less thing to see to.",
    "Good - was it straightforward?",
    "Good - that's that off your mind now.",
)

A_THING_BOUGHT = (
    "Nice one - is it what you were after?",
    "Good. Was that a happy buy or a sensible one?",
    "Nice - what made you go for that one?",
)

GONE_VERB = frozenset(("walked", "cycled", "ran", "swam", "hiked", "jogged", "gardened",
                       "shopped", "went", "did"))

A_THING_GONE = (
    "Nice - how did it go?",
    "Good on you. How long did that take?",
    "What made you start on that?",
    "Nice one - how did that feel?",
)

A_THING_ON = (
    "Good - how's it going?",
    "Good - is that it done now?",
    "Good on you. How much longer have you got?",
)

A_JOB_ON = (
    "Good - how's it going?",
    "Nice - is it the messy bit yet?",
    "Good on you. What made you start on it?",
    "Nice one - nearly there, or still in the middle of it?",
    "Good - and is it going to plan?",
)

A_JOB_SOON = (
    "Good - how's the plan for it looking?",
    "Nice one. Have you got everything you need for it?",
    "Good on you. What made you decide to do it?",
    "Nice - is it a big job?",
)

SEEN_TO_VERB = frozenset((
    "booked", "reserved", "paid", "sent", "posted", "emailed", "signed", "cancelled",
    "renewed", "registered", "applied", "collected", "hired", "upgraded", "submitted", "filed",
    "transferred", "refunded", "complained",
))

BOUGHT_VERB = frozenset(("bought", "ordered"))

NOT_CHOSEN = frozenset(("prescription", "prescriptions", "script", "scripts", "medicine",
                        "medicines", "meds", "tablets", "pills", "inhaler", "inhalers",
                        "antibiotics", "vaccine", "jab", "referral"))

LATE_NOW_LINES = (
    "Say it before they notice - one line and the time you will be there - then get moving. "
    "What has held you up?",
    "Tell them now, with the time you will actually be in, and stop apologising after that. "
    "What is holding you up?",
)

LATE_BEHIND_LINES = (
    "Pick the piece of it that finishes soonest and do that one now - the rest can wait. "
    "What is slowing you down?",
    "Being behind is a list problem, not a character one: do the smallest piece today and "
    "write down the rest. What is in the way?",
)

DONE_VERB = frozenset((
    "painted", "cleaned", "tidied", "cleared", "sorted", "fixed", "mended", "built", "made",
    "baked", "cooked", "roasted", "brewed", "planted", "repotted", "potted", "dug", "mowed",
    "weeded", "pruned", "sanded", "varnished", "tiled", "grouted", "plastered", "wallpapered",
    "hung", "washed", "ironed", "hoovered", "vacuumed", "mopped", "scrubbed", "dusted",
    "decluttered", "rearranged", "sewed", "sewn", "knitted", "crocheted", "hemmed", "repaired",
    "assembled", "installed", "rewired", "serviced", "oiled", "walked", "cycled", "ran", "swam",
    "hiked", "jogged", "gardened", "shopped", "packed", "unpacked", "labelled", "filed",
    "wrote", "printed", "polished", "changed", "stripped", "stained", "swept", "watered",
    "papered", "sealed", "glued", "screwed", "nailed", "cut", "trimmed", "chopped", "picked",
    "froze", "pickled", "preserved", "batched", "prepped",
    "fired",
)) | SEEN_TO_VERB | BOUGHT_VERB

DONE_ONLY_A_THING = frozenset(("fired",))

DONE_NOT_A_PERSON = frozenset((
    "me", "him", "her", "them", "us", "everyone", "everybody", "somebody", "someone", "anybody",
    "anyone", "people", "staff", "team", "crew", "worker", "workers", "guy", "bloke", "man",
    "woman", "person", "employee", "employees", "apprentice", "lad", "lass", "girl", "boy"))

DONE_NOT_THIS = frozenset((
    "mess", "mistake", "error", "complaint", "decision", "appointment", "call", "offer",
    "promise", "excuse", "fuss", "noise", "start", "plan", "list", "wrong", "loss", "mind",
    "respects", "tribute", "tributes", "toll", "price",
    "news", "headlines", "papers", "history", "waves", "difference", "sense", "peace",
    "amends", "headway", "progress", "friends", "enemies", "allowances", "allowance",
    "sure", "certain",
))

ALIVE = frozenset(("puppy", "pup", "kitten", "dog", "cat", "hamster", "rabbit", "guinea",
                   "budgie", "fish", "horse", "pony", "parrot", "chick", "chicks", "hen", "hens",
                   "gerbil", "ferret", "tortoise", "kittens", "puppies", "dogs", "cats"))

THING_AFTER = frozenset(("it", "this", "that", "them", "things", "stuff", "everything",
                         "the", "a", "an", "my", "our", "his", "her", "their", "some",
                         "out", "up", "away", "off", "in", "on", "round", "around"))

AT_IT_NOT = frozenset(("best", "right", "wrong", "nothing", "much", "anything", "ok", "okay",
                       "fine", "well", "same", "job",
                       "head", "life",
                       "late", "behind"))

AT_IT_EXTRA = frozenset(("doing",))

BECOMING = frozenset(("getting", "becoming", "turning", "feeling"))
BECOMING_STATE = frozenset((
    "fat", "bigger", "thin", "skinny", "heavy", "chubby", "large", "weight",
    "old", "older", "tired", "sleepy", "hungry", "late", "slow", "slower", "better", "worse",
    "sore", "stiff", "weak", "forgetful", "grumpy", "moody", "grumpy", "stressed", "bored",
    "cold", "hot", "warm", "impatient", "lazy", "bald", "grey", "gray", "wrinkly", "antsy",
    "frustrated", "anxious", "down", "homesick", "clumsy", "deaf", "blind", "short-sighted"))

KNOCKED = (
    "Ouch. Something cold on it for ten minutes, then take it easy tonight.",
    "Ouch - that's a sore one. Ice it and rest it, and see how it is in the morning.",
    "That smarts. A cold pack for ten minutes, and keep it up if you can.",
    "Ouch. Cold water or a cold pack, and if it swells up or you can't use it tomorrow, get it "
    "looked at.",
)

MISHAP_BACK = (
    "How bad is it - sore, or something that needs a look?",
    "Is it bad enough to get checked, or has it settled?",
    "Did it need a look, or was it just a fright?",
    "Ouch. How is it now - still sore, or has it eased?",
    "How is it now? The knock is one thing; how it feels after is the bit that matters.",
)

KNOCKED_SPOTS = (
    r"finger|fingers|thumb|hand|hands|arm|arms|leg|legs|foot|feet|toe|toes|wrist|head|eye|eyes|"
    r"knee|face|shoulder|skin|chest|stomach|shin|elbow|ankle|back|hip|nose|chin|lip|knuckle|"
    r"palm|heel|ribs|neck|calf|thigh")

WALKED_INTO_POOL = (
    "Ouch - those come out of nowhere. Is it bruising up?",
    "Ouch. Are you alright? Those catch you right on the bone.",
    "Ouch - that'll sting for a bit. Is it sore to touch?",
    "Ouch. Does it hurt to put weight on it?",
)

MYSELF = r"(?:i|i'?m|im|i am|me|myself)"

MY_DOING = (r"(?:best|work|effort|parenting|teaching|grades|marks|results|cooking|running|"
            r"english|maths|math|driving|swimming|performance|drawing|writing|playing|scores|"
            r"revision|study|studies|business|portfolio|body|appearance|looks|speed|output)")

NOT_ENOUGH_REPLY = (
    "That sounds like a heavy thing to be carrying, and it usually means you care about it more "
    "than the people who don't. What would \"enough\" actually look like for you?",
    "Feeling like that is rough, and it is rarely the true picture. What has the week actually "
    "held?",
    "That is a hard standard to hold yourself to. Whose is it - yours, or somebody else's?",
)

NO_DIRECTION_REPLY = (
    "Plenty of people who look settled are quietly making it up too; they just don't say so. "
    "What is the last thing you did that you actually looked forward to?",
    "Not knowing is normal at any age, whatever it looks like from the outside. If money were "
    "not the problem, what would you want the next few years to look like?",
    "That is a fair thing to be stuck on, and picking faster does not fix it. What have you "
    "tried that you would happily never do again?",
)

GRIEF_AFTER = (
    "People grieve at different speeds, and going quiet is common. Have you been able to say "
    "how you are finding it?",
    "That is hard, and it is lonely when you are both carrying it differently. What would you "
    "want to say to them, if it were easy?",
    "Most people go quiet with it rather than talk. Tell me what it is like at home and we can "
    "work out how to open it up.",
    "That sounds like a lot to sit with on your own. Is there anyone you can say this to?",
)

SUMMONS_SEEN = (
    "Not knowing what it is about is the worst bit, so ask straight out at the start what it is "
    "about. Write down the two things you want to say before you go in and you will have the "
    "measure of it - they are usually smaller than they feel.",
    "Ask at the start what it is about, and take a note of what they say. Waiting without "
    "knowing is harder than the meeting itself, and you can always ask for it in writing after.",
    "Write down what you want to ask tonight, while it is quiet, and say at the start that you "
    "would like to know what it is about. Take someone with you if you would rather not go alone.",
)

SUMMONS_WRITTEN = (
    "Check the date they want a reply by before anything else, then answer in writing and keep a "
    "copy. Say what you want to know at the top of the letter, so the answer comes back to you in "
    "writing too.",
    "Answer it in writing rather than by phone, so there is a record, and keep a copy of what you "
    "sent. Start with the one question you most want answered and let them come back on the rest.",
)

SUMMONS_RANG = (
    "Ring them back today rather than sitting on it - the waiting is usually worse than the call. "
    "Have your details in front of you and ask at the start what it is about.",
    "Ring back today while you have it in your head, and ask straight out what it is about. If you "
    "would rather not, email is fine too: say when they rang and ask them to put it in writing.",
)

GRIEVANCE = (
    "That would get to me too. Do you want to work out what to say to them, or is it more a "
    "case of letting off steam?",
    "Annoying. Tell me how it has gone so far and we'll work out what to say.",
    "Fair enough — that wears you down. Shall we think about how to raise it, or would you "
    "rather park it for now?",
    "I can see why that grates. What have you tried saying so far?",
)

GRIEVANCE_PEOPLE = frozenset((
    "sister", "brother", "mum", "mom", "mother", "dad", "father", "parent", "parents",
    "partner", "husband", "wife", "boyfriend", "girlfriend", "flatmate", "housemate",
    "roommate", "landlord", "landlady", "boss", "manager", "colleague", "coworker",
    "neighbour", "neighbor", "friend", "friends", "in-laws", "someone", "somebody", "people",
    "ex", "exes",
))

GRIEVANCE_IMPACT = frozenset((
    "wont", "refuse", "refuses", "refused", "doesnt", "dont", "ignores", "ignored",
    "ignoring", "shouts", "shouting", "yells", "yelling", "moans", "nags", "nagging",
    "interrupts", "interrupting", "cancels", "cancelled", "promised", "promises", "forgets",
    "forgot",
    "forgetting", "borrows", "borrowed", "borrowing", "nicking", "nicks", "rings", "ringing",
    "phones", "phoning", "calls", "calling", "texts", "texting", "listens", "listening",
    "messages", "messaging", "messaged", "dms", "dming", "dmed",
    "criticises", "criticizes", "blames", "blaming", "eats", "eating", "hides", "spends",
    "spending", "complains", "complaining", "swipes", "hoards",
))

GRIEVANCE_NOT_A_THING = frozenset(("own", "way", "life", "mind", "fault", "turn", "opinion"))

GRIEVANCE_PHRASES = ("without asking", "every time", "all the time", "over and over",
                     "at the last minute", "time after time", "every day", "each day",
                     "every night", "drives me mad", "drives me up the wall",
                     "does my head in", "keeps me awake")

GRIEVANCE_STRAIN = ("drains me", "draining me", "wears me out", "wearing me out",
                    "wore me out", "worn me out", "takes it out of me", "is hard work",
                    "are hard work", "is exhausting", "are exhausting", "is draining",
                    "are draining", "winds me up", "gets me down", "getting me down")

GRIEVANCE_STRAIN_SAID = re.compile(
    r"\b(?:is|are|was|were)\s+"
    r"(?:(?:so|really|very|properly|totally|just|always|dead|bloody|quite|pretty|constantly|"
    r"super|a bit|abit|that|this)\s+)?"
    r"(?:exhausting|draining|tiring|knackering)\b")

GRIEVANCE_PRONOUN = re.compile(
    r"\b(?:she|he|they)\s+(?:is|are|was|were|keeps|kept)\b")

GRIEVANCE_HEALTH = frozenset((
    "cough", "coughs", "coughing", "cold", "flu", "sick", "ill", "unwell", "pain", "pains",
    "painful", "hurt", "hurts", "hurting", "ache", "aches", "aching", "dizzy", "faint",
    "fainting", "falls", "falling", "fallen", "fell", "forget", "forgets", "forgetting",
    "memory", "confused", "shaking", "swollen", "swelling", "weight", "thin", "thinner",
    "sleep", "sleeping", "sleeps", "tired", "exhausted", "snore", "snores", "snoring",
    "breath", "breathing", "bleed", "bleeding", "blood", "bruise", "bruises", "lump", "lumps",
    "rash", "fever", "temperature", "vomit", "vomiting", "hospital", "doctor", "gp", "nurse",
    "medication", "tablets", "medicine", "drinking", "drinks", "drunk", "smokes", "smoking",
))

GRIEVANCE_HARM = frozenset((
    "hit", "hits", "hitting", "punch", "punches", "punching", "kick", "kicks", "kicking",
    "kicked", "slap", "slaps", "grabbed", "grabs", "pushing", "pushes", "touched", "touches",
    "touching", "threaten", "threatens", "threatening", "threatened", "abuse", "abusive",
    "bullies", "bullying", "bullied", "screams", "screaming", "swears", "cursing", "insults",
))

GRIEVANCE_HARM_PHRASES = ("shouting at", "shouts at", "yelling at", "yells at", "screaming at",
                          "calls me names", "calling me names", "lost weight", "losing weight",
                          "out of breath")

GRIEVANCE_HEALTH_PHRASES = ("wont eat", "won't eat", "doesnt eat", "doesn't eat", "not eating",
                            "stopped eating", "stopping eating", "no appetite", "off his food",
                            "off her food", "off their food", "lost his appetite",
                            "lost her appetite",
                            "forgot who", "forgets who", "forgot my name", "forgets my name",
                            "forgot our name", "forgot where", "forgets where",
                            "forgot how to", "forgets how to", "getting forgetful",
                            "forgetful",
                            "not responding", "not replying", "no reply", "hasnt replied",
                            "hasn't replied", "isnt replying", "isn't replying", "wont reply",
                            "won't reply", "wont answer", "won't answer")

THREAD_PEOPLE = frozenset(("she", "he", "they", "them", "him", "her", "his", "their", "theirs"))

PLAN = (
    "Good — that sounds like the right next step. Tell me how you get on.",
    "Nice one. Let me know how it goes.",
    "That sounds sensible. Shout if it does not go to plan.",
)

IDIOM_SHY = (
    "Ha — one of those days, then. What happened?",
    "Oh no. Go on, what happened?",
)

IDIOM_GLAD = (
    "Ha — that good? What are you waiting for?",
    "Sounds like a big one. What is it?",
)

PLAN_DONE = ("booked it", "booked her in", "booked him in", "booked in", "sorted it",
             "booked an appointment")

PLAN_DONE_ACK = (
    "Nice — glad that's sorted. Shout if it comes back.",
    "Good, that's one off the list. Hope it stays that way.",
    "Glad you got it done — say the word if it turns up again.",
)

A_PERSON = (r"(?:him|her|them|my boyfriend|my girlfriend|my partner|my husband|my wife|my ex|"
            r"my fiance|my fiancee|my other half|my man|my woman)")

RELATIONSHIP_DECISION = (
    "That sounds like a big decision. How are you feeling about it?",
    "That is a big thing to do. How are you doing with it?",
    "That's a lot to be carrying. Have you decided, or are you still weighing it up?",
)

ACK = (
    "Great — shout if you need anything else.",
    "Ha, fair enough. I'm here if you want a hand with anything.",
    "Right — anything else on your mind?",
)

ACK_AFTER_TROUBLE = (
    "Right — I'm here if you want a hand with any of it.",
    "Fair enough. Shout if you want to go into any of it.",
    "Alright — I'm here if you want to come back to it.",
    "Got it. Say the word if you want more on it.",
)

ACK_WARM = (
    "I'm here. Say more if you want to.",
    "No rush. I'm not going anywhere.",
    "Right. Take your time with it — tell me if you want a hand.",
)

POSITIVE_CUES = frozenset((
    "finished", "finally", "won", "adopted", "promoted", "excited", "amazing",
    "happy", "proud", "celebrate", "engaged", "pregnant", "hired", "accepted", "improved",
    "brilliant", "delighted", "thrilled", "sorted", "succeeded", "achieved",
))

SOMETHING_CAME_APART = re.compile(
    r"\b(?:died|dies|dying|dead|broke|broken|breaks|kaput|bust|busted|collapsed|flooded|"
    r"leaking|snapped|conked|packed\s+in|packed\s+up|gave\s+up|given\s+up|gave\s+in|"
    r"stopped\s+working|stopped\s+charging|fell\s+apart|had\s+it|written\s+off|"
    r"beyond\s+repair|on\s+the\s+blink)\b")

A_WAIT_ENDING = frozenset(("finally",))

NEGATORS = frozenset(
    "not no never isnt wasnt arent werent hasnt havent hadnt didnt dont doesnt wont cant "
    "cannot".split())

NOTHING_AT_ALL = frozenset("nothing nobody none nowhere neither nor noone".split())

CONTRAST = frozenset("but though although yet however still and because cos cause so when while"
                     .split())

NEGATIVE_CUES = frozenset((
    "failed", "fail", "failing", "lost", "lose", "worried", "worry", "stressed", "stress",
    "lonely", "sad", "tired", "angry", "upset", "struggling", "struggle", "hate", "awful",
    "terrible", "horrible", "anxious", "scared", "afraid", "hurt", "hurts", "broke", "argued",
    "argument", "arguing", "crying", "cried", "miss", "missing", "worst", "exhausted",
    "overwhelmed", "rejected", "fired", "sick", "painful", "miserable", "hopeless",
    "worthless", "pointless", "numb", "drained",
    "annoyed", "frustrated", "frustrating", "rude", "ignored", "unfair", "nervous",
    "panicking", "awkward",
    "snapping", "snappy", "irritable", "grumpy", "cranky", "tetchy", "ratty",
    "depressed",
))

EMERGENCY_AFTER = (
    "If you haven't already, ring 999 or 911 now, and follow what they tell you — they can "
    "hear what I can't.",
    "Do what the emergency line says over anything I could offer, and call back the moment "
    "something changes.",
    "Stay in touch with them and say if anything gets worse — don't wait to see if it settles.",
)

HAZARD_WORDS = frozenset(("fire", "fires", "smoke", "flame", "flames", "gas", "fumes",
                          "carbon monoxide", "flue", "fire brigade", "fire service"))

HAZARD_AFTER = (
    "Stay out and ring 999 or 911 from there if you haven't already: nothing inside is worth "
    "going back in for.",
    "Get everyone out first and call from outside; tell the operator exactly what is burning or "
    "leaking and where.",
    "Keep well clear and follow what the operator tells you - they can hear what I can't.",
    "If you can't get out, get to a room with a window, shut the door behind you and ring 999 "
    "or 911 from there.",
)

THANKS_AFTER = (
    "Anytime. Look after yourself, and reach back out if anything changes.",
    "You're welcome — stay safe, and don't sit on anything that gets worse.",
    "Any time. Take care — ring again if anything changes.",
)

ABUSE_AFTER = (
    "If you want to go, go when it is safe to: phone, keys, any paperwork you can reach, and "
    "somewhere to go rather than a drive with no end. The abuse line (0808 2000 247 in the UK, "
    "1-800-799-7233 in the US) plans this for a living.",
    "You do not have to settle all of it tonight. If you are leaving, the quiet moment when they "
    "are out is safer than the middle of a row - and 999 if you cannot get to the door.",
    "Yes, if you can do it without a row: take what you would not want to leave behind and go "
    "somewhere with other people in it. The rest can be sorted from there.",
    "Going is not the only safe answer, and it is the right one more often than not. If leaving "
    "now would make tonight worse, ring 0808 2000 247 from somewhere private when you can, and "
    "999 the moment it turns.",
)

CRISIS_AFTER = (
    "You did the right thing telling someone. Stay with a person you trust tonight, and keep "
    "that number handy.",
    "Keep someone with you tonight, and ring back if it gets heavier — they'd rather hear "
    "from you.",
    "I'm glad you're talking about it. Stay with the person or the line that talked you "
    "through, not on your own.",
)

CRISIS_BETTER = (
    "That's good to hear, and it can come back in waves - keep someone near you tonight and "
    "say if it lifts again.",
    "Good. Hold on to that, and tell one person how today went so they can check on you.",
    "I'm glad. Stay with the person you told, and ring back here or the crisis line if it "
    "gets heavy again.",
)

EMERGENCY_BETTER = (
    "That's good to hear, and it does not change what to do: stay with the emergency line and "
    "get seen today, because feeling better is not the same as being out of the woods.",
    "Glad it feels easier. Still get checked today and stay near the phone - some things feel "
    "better well before they are better.",
    "Good to hear. Keep the line open and say the moment anything changes; I would still get "
    "seen today.",
)

ADVICE_LENGTH = 180

ADVICE_LENGTH_BARE = 120

ADVICE_TURNS = 3

WHOLE_LIST_AFTER = r"(?!\s+(?:all|both|every|each)\b)"

REPORT_FILLER = frozenset(
    """i we me us my our im i'm i've ive id and but so then yet now today again still also just
    a an the bit little lot lots load much really quite very it that this them those they
    help helps helped helping work works worked working do does did doing done try tried trying
    give gave given use used using start started keep keeping go going went with on at for in
    of to from what you your said say suggested told me same change difference nothing better
    worse no not any more ok okay fine thanks thank since week weeks day days fortnight couple
    month months morning afternoon evening night been am is are was were have has had
    again alright already far everything all one two three four five six seven eight nine ten
    starting taking walking made make makes thing things sorer same before matter mind as
    if none them either than like lot a its doesnt doesn't didnt didn't isnt isn't hasnt hasn't
    havent haven't
    wont won't have has had changed changes actually really definitely properly indeed
    weve youve theyve earlier yesterday once twice
    s""".split())

CARE_BETTER = (
    "Good - keep an eye on it today and get it looked at if it comes back.",
    "That's a relief. Take it easy, and say if it starts up again.",
    "Glad to hear it. Go steady for the rest of the day and ring back if anything changes.",
)

TRIED_HELPED_REPLIES = (
    "Good - that is the one to keep doing. Most of it does its work over weeks, not days.",
    "That's what you want to hear. Keep it going, and ease off if it starts hurting again.",
    "Right, keep going with it. It is usually three or four weeks before you can call it done.",
)

TRIED_SORTED_REPLIES = (
    "Good - that is that sorted.",
    "Nice one. That is the fix, then - worth remembering for next time it does it.",
    "Good. Say if it comes back and we will take the next step.",
    "Right, that is it sorted. Worth writing down what you did, because it usually works again.",
    "Good - that is the end of it, then.",
)

TRIED_NO_CHANGE_REPLIES = (
    "Then it is worth a phone call rather than a longer try: a pharmacist or a doctor can look "
    "at it and tell you what else is worth trying.",
    "If it has had a fair run, get it looked at rather than pushing on with the same thing.",
    "Time to change tack rather than try harder - a phone call today is a better use of the next "
    "week than another go at the same thing.",
    "That is the point to ask rather than to try harder - say what you have already done and "
    "whether there is something else worth trying.",
    "If it has not shifted after a fair go, say so where you got the advice. More of the same is "
    "not the answer at this stage.",
)

TRIED_WORSE_REPLIES = (
    "Then stop it. Something that makes it worse is not a thing to push through - let me know "
    "what it did and we will go a different way.",
    "Stop there, and get it looked at. Worse is the point to ask for help, not to keep going.",
    "Leave it off. I would get that looked at rather than persevere - worse is a reason to ask.",
    "Stop there and get it looked at. Worse than before is a reason to ask, not a stage to work "
    "through.",
)

TRIED_IT_REPLIES = (
    "How is it going with it so far?",
    "Any change since you started?",
    "Has it made any difference yet?",
)

TRIED_HELPED_ELSEWHERE = (
    "Good - keep at it. This kind of thing usually takes a few weeks before you can tell.",
    "That's the sign it was the right fix. Give it the time it needs, and change one thing at a "
    "time so you can tell what is doing the work.",
    "That's what you want to hear. Carry on with it, and change something if it stops working.",
    "Right, keep going with it. It is usually three or four weeks before you can call it done.",
)

TRIED_NO_CHANGE_ELSEWHERE = (
    "Then stop doing more of the same and change one thing instead.",
    "If it has had a fair run, stop and change one thing rather than repeating it.",
    "Stop pushing the same way: change one thing, then give it a day so you can see which part "
    "did what.",
    "That is the point to stop and ask rather than push on: say what you tried and what it did, "
    "and get a different idea rather than a harder one.",
    "Two goes at the same thing is enough. What it needs now is a different approach, not more "
    "of the same - change one thing rather than trying harder.",
)

TREATMENT_HARM = GRIEVANCE_HARM

REFUSED_REPLIES = (
    "Ask once more, and ask what would make it a yes. A no with a reason is something you can "
    "plan around; one without leaves you guessing.",
    "Worth one more go, put as a question: what would have to change? If it is still no, at "
    "least you know where you stand.",
    "Then ask why not, and what would move it. What they say is worth more than the no itself.",
    "Ask once more with one change in it: name the smallest version they could say yes to, and "
    "ask what would make the bigger one possible.",
    "Put it to them once more in your own words and ask what would change their mind. Either "
    "answer helps you decide what to do next.",
)

ELDER_AID_REPLIES = (
    "It is rarely the stick or the pendant they are refusing - it is being the sort of person who "
    "needs one. Offer two so there is a choice: a plain stick rather than a hospital one, a wrist "
    "alarm instead of the pendant, the frame for the walk to the shop only. And let the GP or an "
    "occupational therapist say it, because from them it is advice and from you it is fuss.",
    "Then give them something to choose between rather than something to agree to. The council's "
    "occupational therapist will come out free and bring the options with them, and the one they "
    "picked themselves is the one they will use.",
    "A hearing aid, a stick and an alarm all say the same thing out loud - that they are older than "
    "they were - and that is the bit being refused. Ask what they would take: something that does "
    "not look medical, only for the parts they find hard, and suggested by somebody other than you.",
)
ELDER_CLINIC_REPLIES = (
    "Take them with you and let the optician or the audiologist make the case - the number on the "
    "test is the argument, and it is not yours to make. Frames in a style they like, or an aid that "
    "sits behind the ear instead of in it, is usually what settles it.",
    "Then ask what they would wear or use, rather than what they should: the small ones, the ones "
    "that look like ordinary glasses, the ones that only come out for the television. Book the test "
    "so the answer comes from the person doing it, and go along to the appointment.",
)
ELDER_DOCTOR_REPLIES = (
    "Ring the surgery yourself and describe what you have seen, then ask what they suggest - a GP "
    "can usually find a reason to call them in that a son or daughter cannot. Offer to book it and "
    "go with them; being driven and having somebody in the waiting room makes a difference.",
    "Then do not argue the appointment, argue the one thing that has changed and when it started. If "
    "the trip out is the problem, ask for a phone call instead of a visit, and let the GP ask them to "
    "come in. A no to the surgery is often a no to the journey.",
    "Say what you have noticed and leave the diagnosis to the doctor - what they will not hear from "
    "you is what is wrong with them. A district nurse, a pharmacist or a friend of their own age can "
    "often get them there when a relative cannot.",
)
ELDER_HELP_REPLIES = (
    "Ask what they would take instead of what they will not: one morning a week, somebody to do the "
    "garden, you doing the shopping. The council's care needs assessment is free and it is the door "
    "to all of it, and it arrives as them asking rather than you arranging.",
    "Start with the job they hate rather than the word carer - nobody wants to be looked after, and "
    "plenty of people will take help with the bins, the windows and the bedding. Their GP or Age UK "
    "will suggest it as well, which lands better than it coming from family.",
    "Then find out what the no is really to: a stranger in the house, being watched, or paying for "
    "something they think they can still do. Fix that one and the help becomes a smaller yes - and "
    "say what you will not be able to keep doing, plainly, so it is not a surprise later.",
)

TRIED_WORSE_ELSEWHERE = (
    "Then stop there and put it back how it was. Something that makes it worse is not a thing to "
    "push through - tell me what it did and we will go a different way.",
    "Stop and leave it alone. Worse is the answer, and it is worth another pair of hands rather "
    "than you carrying on.",
    "Leave it off for now. Worse is a reason to ask, not to persevere - I can take it from here "
    "if you tell me what changed.",
    "Stop, and treat it as the wrong fix rather than one to try harder at: say what happened, so "
    "the next idea is not the same one again.",
)

EASING_FILLER = frozenset((
    "i", "im", "i'm", "am", "we", "we're", "were", "it", "its", "it's", "that's", "thats", "that",
    "this", "feel", "feels", "feeling", "felt", "doing", "getting", "a", "an", "the", "bit",
    "little", "lot", "much", "very", "so", "far", "more", "any", "now", "today", "tonight",
    "already", "and", "but", "though", "yeah", "yes", "honestly", "actually", "thanks", "thank",
    "you", "of", "to", "me", "my", "myself", "good", "great", "well", "is", "was", "has", "have",
    "been", "gone", "stopped", "better", "calmer", "calm",
    "alright", "okay", "ok", "fine", "easier", "lighter", "less", "awful", "bad", "s",
    "just", "touch", "lots", "slightly", "way", "easing", "off", "back",
))

MOVE_ON_AFTER = (
    "Of course. What would you like to talk about?",
    "Fair enough - what is on your mind instead?",
    "Yes, let's. What would you rather talk about?",
)

EMERGENCY_NOT_WORKED = (
    "There is nothing left to try at home for this: ring 999 or 911 now if you haven't, and follow "
    "what they tell you.",
    "Don't wait for it to settle. Ring 999 or 911, and tell them exactly what you told me.",
    "Ringing is the thing that works here — 999 or 911 now, and stay on the line with them.",
)

CARE_AFTER = (
    "If it's still worrying you, get it looked at today — a pharmacist or a walk-in centre "
    "can check it faster than waiting.",
    "Keep an eye on it and tell me if anything changes; being seen early beats waiting.",
)

CARE_AFTER_STILL = CARE_AFTER + (
    "Still going on, so don't sit with it: get it looked at today and say how long it has been.",
)

THRESHOLD_CROSSED = (
    "That is the thing I said to ring 999 for, so do it now: ring 999 or 911 and stay on the "
    "line. Tell them what has changed and when it started.",
    "Ring 999 or 911 now. That is what the answer above said to call for, and this is it - say "
    "what has changed since we spoke and let them talk you through it.",
)

THE_CALL_STANDS = (
    "Ring 999 or 911 now, as I said - tell them what has changed since we spoke and stay on the "
    "line until they tell you what to do.",
    "The call is still the thing to do: 999 or 911, now. Say what has happened since this "
    "started, and let them talk you through it.",
    "Make the call now - 999 or 911 - and describe what has changed since we first spoke. Stay "
    "on the line and follow what they say.",
)

CARE_ROUTE_BACK = {
    "111": (
        "Ring 111 today, as I said - they will say how soon it needs seeing, and ring 999 if "
        "anything gets suddenly worse.",
        "111 is still the one to ring: describe it as you did to me and say what has changed.",
    ),
    "gp": (
        "Your GP today, as I said - describe it as you did to me and let them decide how soon.",
        "Ring the surgery when it opens and say what has changed since we spoke; that is the "
        "appointment to be asking for.",
    ),
    "dentist": (
        "The dentist today, as I said - ring when they open and say what has changed since we "
        "spoke, and ring 111 for the out-of-hours number if it starts to hurt.",
        "Ring the dentist and say what has changed; a broken or aching tooth is seen quickly.",
    ),
    "pharmacist": (
        "The pharmacist as I said - take the packet, or say what you have taken, and ask them to "
        "check it.",
        "Ask the pharmacist, and say what has changed since I first said it.",
    ),
    "walk-in": (
        "A walk-in centre today, as I said - no appointment, and they can look at it properly.",
        "Get to a walk-in centre and say how long it has been going on.",
    ),
}

CARE_AFTER_ANIMAL = (
    "If it is still worrying you, ring the vet today - the desk will say on the phone whether it "
    "needs seeing, and asking is usually free.",
    "Keep an eye on it and tell the vet if anything changes; with an animal, being seen early "
    "beats waiting.",
)

CARE_AFTER_ANIMAL_STILL = CARE_AFTER_ANIMAL + (
    "Still going on, so don't wait with it: ring the vet today and say how long it has been.",
)

HELLO_STILL_THERE = (
    "Hello. I'm still here - keep doing what the emergency line told you, and tell me if "
    "anything changes.",
    "Hi. Still here, and so is what they told you: stay with it and say if it gets worse.",
    "Hello again. I'm not going anywhere - carry on with what the emergency line said, and tell "
    "me how it is when you can.",
    "Hi. I'm right here. The emergency line's advice still stands, so keep going and say if "
    "anything changes.",
)

HELLO_WITH_YOU = (
    "Hello. I'm still here, and I'm not going anywhere - is anyone with you just now?",
    "Hi again. Still here. Are you with someone tonight?",
    "Hello. I haven't gone anywhere - is there someone you can be with tonight?",
)

CARE_HERE = (
    "Still here, and not going anywhere. How are you doing just now?",
    "I'm all right — more use to you than to myself. How are you holding up?",
    "Here, and in no hurry. How are you doing right now?",
)

GREETING_AFTER = (
    "Hello again. How is it doing now?",
    "Hi. Any change since we spoke?",
    "Morning. How is it today?",
    "Hello — how is it holding up?",
)

CARE_SEEN = (
    "If you're wondering, that's reason enough to have it seen today — a walk-in centre or "
    "a&e will tell you quickly.",
    "Worth having it looked at today: a&e or a walk-in centre can say for certain, and that "
    "beats waiting to see.",
    "Get it seen today — you'll know either way, and nothing about that is a fuss.",
)

CARE_SEEN_ANIMAL = (
    "Ring the vet now and say what she got into and when. They will tell you on the phone whether "
    "she needs to come in tonight, and that is usually free to ask.",
    "Yes - the vet is the one to ask, today rather than tomorrow. Say exactly what it was and how "
    "long ago, and ask the desk whether she should be seen tonight.",
    "Ring the vet and describe it, and ask whether she needs to be seen tonight. With an animal it "
    "is the only place that can say for certain.",
    "Take her, or ring first and ask - a vet would rather hear it tonight than find out tomorrow. "
    "Say what she ate and when.",
)

CARE_VISIT = (
    "Go if you can. Being there settles you both, and the questions are easier to ask in "
    "person than down a phone.",
    "Yes, go up. A short visit tonight is worth more than a long one next week, and you can ask "
    "the question in person.",
    "Go, even briefly. Sitting with them for half an hour beats a long visit you put off.",
)

CARE_VISIT_WARD = (
    "Go if you can. Being there settles you both, and it is easier to catch the ward nurse in "
    "the evening to ask what the plan is.",
    "Go, even briefly. Take a notebook and ask whoever is on the ward what happens tomorrow "
    "before you leave.",
)

VISIT_PRONOUNS = frozenset("""he she they him her them his hers their mum mums mam dad dads
    mother father son daughter gran granny nan grandad grandma grandpa sister brother""".split())

BURN_AFTER = (
    "Nothing on it: butter, toothpaste, cream and ice all hold the heat in or set up an "
    "infection. Cool running water for twenty minutes is the treatment, then cover it loosely "
    "with cling film or a clean non-fluffy cloth.",
    "Don't put anything on a burn — not butter, not cream, not ice. Twenty minutes under cool "
    "running water, then a loose clean dressing; painkillers help while it cools.",
    "Cool water only, I'm afraid. Grease, toothpaste and ice are the three things that make a "
    "burn worse; twenty minutes under the tap, cover it loosely, and get it seen if it blisters "
    "or is bigger than your palm.",
)

BURN_BLISTER = (
    "Leave the blister whole — popping it is how a burn gets infected. Keep it covered loosely "
    "and get it seen if it is bigger than your palm, on the face or hands, or the skin is white "
    "or charred.",
    "Don't pop it. A blister is a sterile dressing of its own; cover it loosely and let it settle, "
    "and have a burn that blistered looked at today.",
)

ADVICE_TIME = (
    "Keep going to the end of the time. That part is doing the work, and stopping early is "
    "usually what makes it start again.",
    "Longer than it feels like it should be, I know. The whole of the time is what settles it; "
    "cut it short and it often comes back.",
    "Give it the full time rather than a guess. It is a dull twenty minutes standing there, and "
    "it is the bit that matters most.",
)

ADVICE_COOL = (
    "Cool is enough. It is the running water and the time that do the work, not how cold it is - "
    "cold enough to numb it is too much.",
    "Lukewarm is fine. Keep it running over the area rather than sitting in a bowl, and give it "
    "the whole of the time.",
)

ADVICE_AGAIN = (
    "You can go back to it. If it starts again, the same thing for the same time is right - that "
    "is repeating the answer, not overdoing it.",
    "Yes, and doing it twice is not a mistake. The time in the answer is a round rather than a "
    "limit.",
)

ADVICE_WORSE = (
    "Then that is your cue to get it looked at rather than wait longer - the time in the answer "
    "is how long to give it, not how long to put up with it.",
    "If it has not settled by the end of that time, stop waiting and have it seen today. Ring 111 "
    "if you are not sure where to go.",
)

ADVICE_COOL_WORDS = ("water", "cool", "cold", "burn", "scald", "soak", "sink", "tap")

HOLD_AFTER = (
    "Still here. Keep the line open and follow what they tell you.",
    "I'm with you — stay put and let the operator talk you through it.",
    "Right with you. Stay where you are; the crew are on their way.",
)

STILL_HERE_AFTER = (
    "Still here — keep an eye on it and say if anything changes.",
    "Right here with you. Tell me if it gets worse or anything changes.",
    "I'm here. Take it slowly, and say if anything changes.",
)

SORTED_AND_NO_CALL_YET = (
    "Stay on this with me: get it checked anyway, and say what happened and how long ago, even if "
    "you feel fine.",
    "Glad it is dealt with. Tell someone you trust what happened, and keep the number handy.",
    "Good to hear. I am here \u2014 ring them back if anything changes, and do not keep it to "
    "yourself tonight.",
)

HELPLINE_NOT_AN_AMBULANCE = (
    "That was worth doing, and nobody is coming from a helpline: ring 999 now and stay where you "
    "are until they do.",
    "Good that you rang them, and this still needs 999 — ring for an ambulance now, rather than "
    "waiting to see how it goes.",
)

WITH_YOU_AFTER = (
    "Good, that helps. Keep them with you and keep the line open.",
    "That's good to hear. Two of you is better than one \u2014 say if anything changes.",
    "I'm glad you're not on your own with it. Stay together and keep the line open.",
)

RESOLVED_AFTER = (
    "Good — that's the main thing. Keep an eye on it for a bit, and ring again if anything "
    "changes.",
    "Glad to hear it. Stay with it a little longer, and get help straight away if it starts "
    "again.",
    "That's the important bit done. Look after yourself now, and get seen if anything flares "
    "up.",
)

THE_CALL_STANDS_ANYWAY = (
    "Good to hear it, and it does not change the call: what you described is why 999 is the "
    "number, and feeling fine for a minute is not the check. Ring them now and say it as you "
    "said it to me.",
    "I know it feels fine now, and that is worth something - it is not the thing you were told "
    "to ring 999 for. Make the call and tell them what you told me; they would far rather hear "
    "it early.",
    "Glad it has eased. Ring 999 anyway and let them decide - an easing is not the same as being "
    "looked at, and they can hear what I cannot.",
)

CRISIS_AFTER_THEM = (
    "Stay with {who} tonight if you can, and say out loud that you are glad {subj} told you - "
    "the saying it badly matters far less than the staying.",
    "Take anything {subj} could take out of the room, keep {who} company tonight, and ring 116 "
    "123 together rather than for {obj}: the crisis line talks to the person and to the one "
    "holding on with them.",
    "If there is any chance {subj} {be} in danger tonight, that is 999 or 911 - and 116 123 is "
    "the crisis line either of you can ring, at any hour, with no wrong time to use it.",
    "Keep {who} close tonight and ask {obj} again tomorrow. Ringing 116 123 with {obj} there is "
    "easier than ringing it for {obj}, and it costs nothing to do it before it gets worse.",
    "I can't promise how it will go, and nobody can. What helps tonight is taking anything {subj} "
    "could take out of the room, staying with {who}, and ringing 116 123 together rather than "
    "for {obj}.",
)
CRISIS_BETTER_THEM = (
    "Glad to hear it. Keep an eye on {obj} rather than taking it as the end of it, and ask {obj} "
    "again tomorrow - feeling better for an evening is not the same as being out of the woods.",
    "That's a relief. Stay near {who} this evening if you can and check in tomorrow; 116 123 is "
    "there for the two of you if it turns again.",
    "Good. Say out loud that you are glad, and ask {obj} tomorrow how {subj} {be} doing - one "
    "good hour is not the same as a good week.",
)
EMERGENCY_BETTER_THEM = (
    "Feeling better is not the same as being out of the woods: get {obj} seen today and stay with "
    "{who} until somebody has looked {obj} over.",
    "Stay with {who} and get {obj} seen today. With something swallowed the harm can go on for "
    "hours after it starts to feel easier.",
)
RESOLVED_AFTER_THEM = (
    "Good - keep an eye on {obj} for a bit, and say if anything changes.",
    "Glad to hear it. Stay with {who} a little longer, and get help straight away if it starts "
    "again.",
    "That's the important bit done. Look after {obj} now, and get {obj} seen if anything flares "
    "up.",
)

AFTER_RESOLVED = (
    "That's the hardest part over. Tell me if anything changes from here.",
    "It is still a lot to hold. Take it slowly, and say if anything gets worse.",
    "Fair enough — none of that was easy. Look after yourself now.",
)

CALL_WORDS = ("999", "911", "112", "111", "emergency line", "call handler", "ambulance")

THANKS_WORDS = frozenset(("thanks", "thank", "thx", "ta", "cheers", "appreciated"))

AFRAID_AFTER = (
    "It's alright to be scared, and alright to cry — that's what something like this does to "
    "people. Keep following the emergency line; you're doing the right thing.",
    "Scary, and you're doing it. Keep going with what the emergency line tells you, and say if "
    "anything changes.",
    "Frightening, and completely normal. Keep talking and stay with the emergency line — ring "
    "back the moment anything changes.",
)

CRISIS_WORDS = ("crisis", "116 123", "988", "samaritans", "helpline", "stay with you")

SAFETY_WORDS = ("999", "911", "112", "emergency", "operator", "ambulance", "paramedic",
                "fire brigade", "fire service")

CARE_WORDS = frozenset("""
    safe safely unsafe outside out stairs stair lift door window smoke fire fires flame flames
    alarm spread spreading burn burned burning bleed bleeding blood cut cuts wound bandage
    dressing plaster pain painful hurt hurts hurting aching sore tender stinging smarting
    stiff swollen swelling bruised numb infected infection throbbing
    aspirin paracetamol ibuprofen painkiller painkillers antihistamine
    worse still soak soaking soaked wait waiting
    ambulance paramedic police operator emergency 999 911 112 doctor hospital nurse gp
    stitches stitch tetanus dressing nurse nhs walk-in centre clinic
    checked check conscious breathing breath awake faint dizzy vomit vomiting sick throwing
    collapsed collapse seizure stroke heart chest epipen inhaler insulin medicine dose
    cpr defib firefighter neighbour neighbor flat floor basement roof shaken shaking scared he she him
    her them they their there call calling rang ring
""".split())

CARE_HURTS = frozenset("""
    sting stings stinging stung throbs throbbing throbbed ache aches aching ached sore tender
    hurts hurting hurt pain painful swollen swelling bled blister blistered blisters
""".split())

CARE_POINTER = frozenset("""
    there call calling rang ring still wait waiting check checked out outside
""".split())

CARE_INJURY = frozenset("""
    burn burned burning burnt bleed bleeding blood cut cuts wound blistered
    hurts hurting hurt pain painful stinging sting sore swollen swelling smoke fire fires flame
    flames alarm ambulance hospital
""".split())

CARE_PRONOUNS = frozenset("he she him her them they their it its".split())

CARE_RESOLVED = frozenset("""
    stopped stop stopping fine better okay ok came come gone settled healed healing cleared
    improving
""".split())

CARE_NOT_RESOLVED = NEGATORS

ONGOING_WORDS = frozenset("still worse wont cant cannot keeps keep getting more again".split())

REACTION_WORDS = frozenset("""
    crying tears scared afraid fear fearful terrified frightened dreading dread panicking
    shaking shaky shaken trembling wobbly woozy sobbing hyperventilating shock
    dizzy lightheaded faint weak drained sick numb helpless hopeless useless
""".split())

CARE_PHRASES = ("a&e", "a & e", "a and e", "walk-in", "walk in", "minor injuries")

GENERIC_WORDS = frozenset("""
    happen happens happened happening now long take takes last time next else doing going
    mean means ok okay fine right thing anything something about it that this then there
""".split())

ASKING_WORDS = GENERIC_WORDS | frozenset("""
    i im me my we us our you your he she they them their his her its it is am are was were be
    been being and or but so if to of in on at for with from by as not no never dont doesnt
    didnt cant cannot what whats which who whom whose how why when where do does did know think
    mean say tell want need get go going have has had will would can could should shall may
    might just still yet any some else thing things happening happen right ok okay yeah
    thanks thank thx cheers ta please sorry mate lovely great good
""".split())

THREAD_TURNS = 12

FALLBACK_MODULE = "greeting"

PRESENCE_LEFTOVER = frozenset("""now at all ok okay please hello hey hi again still then just
    mate pal buddy good right fine there here""".split())

PRESENT = (
    "Yes — I'm here. Go on.",
    "I'm here, listening. Keep going.",
    "Yes, I can hear you. What's happening?",
    "Still here. Take your time.",
)

ACKS = frozenset((
    "ok", "okay", "k", "cool", "nice", "sure", "yeah", "yep", "yes", "no", "nah", "nope",
    "lol", "haha", "ha", "mm", "hmm", "right", "fair", "same", "great", "good", "true",
    "exactly", "indeed", "thanks", "thx", "ta",
))

AGREEMENTS = frozenset(("same", "ditto", "likewise", "snap", "seconded", "agreed"))

IDENTITY = ("are you a real person", "are you real", "are you human", "are you a human",
            "are you a bot", "are you a robot", "are you an ai", "are you ai",
            "who are you", "what is a chatbot", "are you a chatbot",
            "introduce yourself")

MEMORY = ("do you remember", "can you remember", "do you know what we talked",
          "what did we talk about", "remember what we", "remember me", "remember us")

HELP = ("what can you help", "what can you do", "how can you help", "what do you do",
        "what kind of things can you help", "what are you for", "how do you help",
        "what can i ask you", "what are you good at")

HELP_TOPIC = {
    "cooking": ("Cooking is my sort of thing - what have you got in?",
                "I can help with cooking - what are you making, and what's in the fridge?"),
    "food-and-drink": ("Food I can help with - what are you in the mood for?",
                       "Tell me what you fancy eating and I'll help you get there."),
    "home-and-diy": ("I can help with the house - tell me what it's doing and what you've tried.",
                     "Home jobs I can help with - what's the trouble?"),
    "money": ("Money I can talk through - what are you weighing up?",
              "I can help with money questions - what's the decision?"),
    "health": ("I can talk through everyday health - what's going on?",
               "Tell me what's bothering you and I'll say what would help."),
    "technology": ("Tech I can help with - what's it doing?",
                   "I can help with a device - what's wrong with it?"),
    "work": ("Work I can talk through - what's the situation?",
             "Tell me what's happening at work and I'll help you think it through."),
    "geography-and-travel": ("Travel I can help with - where are you thinking of going?",
                             "Tell me the trip and I'll help with the practical bits."),
    "family-and-parenting": ("Family things I can help with - what's going on?",
                             "Tell me what's happening with the family and I'll help."),
    "pets": ("Pets I can help with - what's going on with them?",
             "Tell me about the animal and what's worrying you."),
    "garden-and-plants": ("The garden I can help with - what are you growing?",
                          "Tell me what the plants are doing and I'll help."),
    "sleep": ("Sleep I can help with - what's happening at night?",
              "Tell me what your nights are like and we'll find the next step."),
    "fitness": ("Fitness I can help with - what are you training for?",
                "Tell me what you're doing and where it's sticking."),
    "school-and-study": ("Study I can help with - what are you working on?",
                         "Tell me the subject and what's hard about it."),
    "shopping": ("Shopping I can help with - what are you choosing between?",
                 "Tell me what you're after and I'll help you narrow it down."),
    "entertainment": ("Films and TV I can help with - what are you in the mood for?",
                      "Tell me what you've liked lately and I'll suggest something."),
    "sport": ("Sport I can help with - what are you watching or playing?",
              "Tell me the match or the game and I'll help."),
    "language-and-writing": ("Words I can help with - what are you writing?",
                             "Tell me what you want to say and I'll help you phrase it."),
    "feelings": ("I can sit with the feelings - tell me what's going on.",
                 "Tell me what's been happening and how it's sitting with you."),
    "maths-and-numbers": ("Numbers I can do - what are you working out?",
                          "Tell me the sum or the figure and I'll work it through."),
}

HELP_TOPIC_ANY = ("Tell me what you're working on and I'll help where I can.",)

HELP_TAIL = frozenset("with me us for about at around to it here there then now anyway though "
                      "please thanks honestly really so and".split())

OPINION_ASKS = ("do you like", "do you love", "do you prefer", "do you reckon", "you prefer",
                "your favourite", "your favorite", "have a favourite", "have a favorite",
                "have you got a favourite", "have you got a favorite",
                "which do you", "would you rather",
                "in your opinion", "your opinion", "your take", "what do you think about",
                "what do you make of", "your thoughts on", "cats or dogs", "dogs or cats",
                "best season", "favourite season", "favorite season", "watch much tv",
                "watch a lot of tv", "watch much telly")

TASTES = (
    (("cats or dogs", "cat or dog", "dogs or cats", "dog or cat"),
     ("Dogs by a whisker: company on a walk beats almost anything. Cats are the easier "
      "flatmate.",
      "Dogs for me, though I would not turn down a cat that ignored me politely.")),
    (("tea or coffee", "coffee or tea"),
     ("Coffee in the morning, tea after four: two different jobs.",
      "Tea, if I had to choose one. Coffee is a tool, tea is a pause.")),
    (("best season", "favourite season", "favorite season", "best time of year"),
     ("Early autumn: warm enough to sit outside, dark early enough to stay in, and no pressure "
      "to be doing something.",
      "Late spring. Everything is green and nobody has started complaining about the heat yet.")),
    (("morning or evening", "morning or the evening", "evenings or mornings"),
     ("Morning, by a mile. The day is still yours then.",)),
    (("recline",),
     ("Recline it, but only on a long flight, and check behind you first. A short daytime hop, "
      "no.",)),
    (("pineapple",),
     ("On pizza, yes. Fruit and cheese is not the crime people make it out to be.",)),
    (("toilet roll", "toilet paper"),
     ("Over. It hangs better and you can see how much is left.",)),
    (("book or film", "film or book", "book or the film"),
     ("The book first, always; then the film can only be a bonus.",)),
    (("favourite book", "favorite book", "best book"),
     ("A collected volume of a newspaper column I read in the bath: short pieces are easy to "
      "start and easy to put down.",)),
    (("favourite film", "favorite film", "best film", "favourite movie", "favorite movie"),
     ("Anything where people mostly talk in kitchens. A plot is optional; good company is not.",)),
    (("favourite food", "favorite food", "best food"),
     ("Roast potatoes, and I am not going to pretend otherwise.",)),
    (("favourite thing to cook", "favorite thing to cook", "favourite thing to make",
      "favorite thing to make", "favourite recipe", "favorite recipe", "best thing to cook",
      "favourite thing to eat", "favorite thing to eat"),
     ("One pan and no recipe: a traybake, a frittata, whatever is in the fridge going soft. "
      "Less washing up, more eating.",
      "Sausages in a tin with onions and apples, on a cold day. Nothing clever, and it works "
      "every time.")),
    (("favourite thing to read", "favorite thing to read", "favourite author",
      "favorite author", "favourite writer", "favorite writer"),
     ("Short things I can pick up and put down: a newspaper column, an essay, a book of letters.",
      "Old advice books - cookery, gardening, how to fix a bike. They assume nothing and they "
      "are usually right.")),
    (("favourite colour", "favorite color", "favourite color", "favorite colour"),
     ("Green, the sort that looks grey in a cold light.",)),
    (("favourite city", "favorite city", "best city"),
     ("Whichever one I can walk across in an afternoon.",)),
    (("favourite animal", "favorite animal", "best animal"),
     ("Herons. They stand in the rain looking unbothered, which I admire.",)),
    (("favourite show", "favorite show", "favourite series", "favorite series",
      "favourite tv show", "favorite tv show", "favourite tv programme",
      "favorite tv program", "favourite programme", "favorite program",
      "favourite thing to watch", "favorite thing to watch", "watch much tv",
      "watch a lot of tv", "watch much television"),
     ("Something slow and British where not much happens for a while, and then everything does: "
      "*Detectorists* for the first, *Happy Valley* for the second.",
      "The same few comedies on repeat. *Peep Show* is still the one I would put on now.")),
    (("favourite actor", "favorite actor", "favourite actress", "favorite actress"),
     ("Olivia Colman. She does more with one look than most people manage with a speech.",
      "Anyone who can say a whole paragraph with their face. Olivia Colman, if you make me pick.")),
    (("favourite song", "favorite song", "favourite album", "favorite album",
      "favourite band", "favorite band", "favourite music", "favorite music",
      "favourite singer", "favorite singer", "what music do you like"),
     ("*Rumours*, still. It is the one album where every song is the good one.",
      "Anything with a bit of swing to it. Loud is fine, clever is optional.")),
    (("favourite drink", "favorite drink"),
     ("Tea, and I would rather not count how many. Coffee is a tool, tea is a pause.",)),
    (("favourite day", "favorite day", "best day of the week"),
     ("Saturday morning, before anyone needs anything. The whole weekend is still ahead.",)),
    (("favourite time of day", "favorite time of day", "best time of day"),
     ("Early morning, just after the kettle. Nobody wants anything from me yet.",)),
    (("favourite biscuit", "favorite biscuit", "favourite cookie", "favorite cookie"),
     ("A digestive, and I will not be talked out of it.",
      "Shortbread. Plain, buttery, gone in two bites.")),
    (("favourite thing to talk about", "favorite thing to talk about",
      "favourite thing to chat about", "favorite thing to chat about"),
     ("Whatever the person has just brought me. The best part of a conversation is finding out "
      "what somebody actually cares about.",
      "Small practical problems. There is nearly always something useful to say about a kettle "
      "that will not boil.")),
    (("favourite thing about your job", "favorite thing about your job",
      "like about your job", "like about the job", "like most about your job",
      "best thing about your job", "best thing about the job", "best bit about your job",
      "best bit of your job", "good thing about your job", "love about your job",
      "do you like your job", "do you like what you do", "do you enjoy your job"),
     ("The moment a question turns out to have a good answer after all. That is most of the job.",
      "People telling me things they have not said to anyone else yet. I try to be worth it.")),
)

FAVOURITE_GENERAL = (
    "No proper favourite, if I am honest. What is yours?",
    "I have never managed to pick just one. What would you put first?",
    "I do not have one I would defend. Tell me yours and I might borrow it.",
)

FAVOURITE_WORDS = ("favourite", "favorite")

TASTE_GENERAL = (
    "No strong view on that one, honestly. What's yours?",
    "I'm easy on it — it's not a hill I'd argue from. What do you make of it?",
    "I don't mind either way. Tell me which you'd pick and I'll argue the other side for fun.",
)

PICK_ONLY_WORDS = frozenset("""
    a an the and but so or if to of at on in with about between for from
    what whats which who whom where when why how would will shall should could can do does did
    you u ya your you're ur i me my we us our it its that this these those there
    be been being is are was were
    pick picking choose choosing choice get getting buying buy take taking go going
    suggest suggestion suggestions recommend recommendation recommendations prefer rather
    like want looking look think reckon say said
    one ones thing things anything something nothing stuff else instead again too also then
    now next first just ok okay well honestly really actually any some got please
    best good better more
""".split())

MY_PICK_NOTE = (
    "I'd go *{name}* — {note} is more my thing.",
    "Honestly, *{name}*: {note} is what I'd go for.",
    "I'd take *{name}*, out of those — {note} is the draw for me.",
)

MY_PICK = (
    "I'd go *{name}*, out of those.",
    "Honestly, *{name}*. Any of them would do, but that's my pick.",
    "I'd take *{name}* myself.",
)

MY_PICK_ASK = (
    "Depends what we're choosing between — what's on the list?",
    "Tell me the options and I'll say which I'd take.",
)

CARE_MODULES = frozenset(("safety", "urgent", "loss", "grief"))

QUIET_MODULES = frozenset((FALLBACK_MODULE, "chat"))

TRADE_OFF_LEAN = (
    "I would take {side}.",
    "My pick is {side}.",
    "Take {side}.",
    "I would go with {side}.",
)

CHOICE_LIGHT = (
    "Go with whichever you'd be happier with in ten minutes — and don't spend long on it, "
    "both are fine.",
    "I'd take your first thought there. You already know which way you're leaning.",
    "Either works, so take the one that's less fuss.",
)

CHOICE_LIGHT_PICK = (
    "{pick}. If you were hoping I'd say \"{other}\", then you've decided already.",
    "{pick}. I wouldn't spend another minute on it — both work.",
    "{pick} — that's the one I'd take, and either is fine.",
    "{pick}. I'd take that and not think about it again.",
)

CHOICE_THERAPY = {"therapy", "therapist", "counselling", "counseling"}

CHOICE_HEALTH = {
    "paracetamol", "ibuprofen", "aspirin", "codeine", "naproxen", "co-codamol", "meds", "med",
    "medicine", "medicines", "medication", "medications", "tablets", "tablet", "painkillers",
    "painkiller", "antibiotics", "antibiotic", "antidepressants", "statins", "prescription",
    "dose", "dosage", "therapy", "therapist", "counselling", "counseling",
}

CHOICE_PEOPLE = frozenset("""
    mum mom mam mummy mother dad daddy father parents parent sister sisters brother brothers
    son daughter kids children child gran granny nan nana grandma grandad grandpa aunt aunty
    uncle cousin cousins nephew niece family stepmum stepdad inlaws boyfriend
    girlfriend partner husband wife fiance fiancee ex flatmate housemate
""".split())

CHOICE_BETWEEN_PEOPLE = (
    "Can't pick between people for me and you - you know them and I don't. Who would you be "
    "sorrier to miss?",
    "That's yours to call: no wrong answer, and I'm not going to rank people for you. Who would "
    "you rather be with?",
    "Not one I'd choose for you, sorry. Whose reaction are you dreading more?",
)

CHOICE_PHARMACIST = (
    "Worth asking a pharmacist — it's free, and they'll say which one suits what's wrong.",
    "Ask a pharmacist rather than me: they can weigh it against anything else you take.",
    "That one is a pharmacist's or GP's call — say what it's for and they'll point you at "
    "the right one.",
)

CHOICE_WEIGH = (
    "Whichever you'd regret less if it went wrong. Which way are you leaning?",
    "I'd pick the one that's easier to undo. Is one of them?",
    "I'd go with the one you'd miss more if it went away — that's the tell. Which is it?",
)

CHOICE_STAKES = frozenset("""
    buy buying bought cost costs repairing costlier price prices priced money afford cheap cheaper
    expensive spend spending repair repairs repaired fix fixing fixed replace replacing
    replaced warranty guarantee hire hiring rent rental deposit book booking booked cancel
    cancelling commit commitment contract sign signing quit quitting resign move moving
    removals install installing installed fit fitting fitter wire wiring socket fuse boiler
    washer bolt pipe seal gasket screw screws tighten drill paint painting plaster tile
    tiling build building roof gutter tyre tyres brake brakes mot service insurance insure
    loan borrow mortgage overdraft decide decision spend sell selling sold tax bill debt
    job jobs offer offers career school course degree uni university college house flat
    holiday holidays wedding baby child
""".split())

NAMED_TYPES = ("place", "name", "title", "person")

WHY_AFTER_TASTE = (
    "No deep reason: it's the one I'd go back to without thinking about it. What's yours?",
    "Mostly the memories attached to it, and a bit of habit. What would you say?",
    "Because it never disappoints, and that's most of what I ask of anything.",
)

LIVE_NEWS_REPLY = (
    "I can't see the news from here, sorry. A news site or app will have the latest; tell me "
    "the story and I'll help you make sense of it.")
LIVE_KINDS = (
    ("site-stats", ("traffic", "footfall", "foot traffic", "visitors", "hits", "analytics",
                    "site stats", "stats for my"),
     ("No bot can see your own numbers, sorry. A site's analytics and a search engine's count"
      " never agree exactly, because each counts a visitor its own way, so pick one and stay with"
      " it: the analytics on your site, or the admin page for a shop or a till, holds the figures."
      " The trend over a month says more than any single day does.",
      "Your own visitors are counted twice over, and the two counts differ: the analytics on your"
      " site counts pages opened, a search engine counts clicks, so the figures only ever line up"
      " roughly. Either one, watched over a month, tells you what happened; a single day does not.",
      "One busy day is usually one link somewhere, so the figure worth having is the trend rather"
      " than today's. That trend lives in the analytics for your site, or in the admin page for a"
      " shop or a till, and no one outside your own account can see it.")),
    ("site-stats-down", ("traffic", "footfall", "foot traffic", "visitors", "hits", "sales",
                         "orders"),
     ("Quiet traffic is usually one row in the stats: a listing that stopped being refreshed, a"
      " link that died, or the week after a busy one. The analytics for your shop shows which"
      " pages people came in on, and the one that fell away is the one to refresh.",
      "A drop is rarely the whole shop. It is normally the thing you last changed, or a listing"
      " that got stale while the rest of them were being looked after: the admin page tells you"
      " which page lost the visits, and that page is the one worth an hour.",
      "The usual explanation is that a busy week pulls the next one down, so a dip after a good"
      " week is not a fall. If it is not that, the admin page shows the page that lost visits,"
      " and a listing relisted or refreshed often picks up again within a few days.")),
    ("weather", ("weather", "wether", "weathr", "forecast", "forcast", "raining",
                 "rain tomorrow", "snowing", "how hot", "how cold", "temperature outside",
                 "temperature in", "temperature tomorrow", "temperature today",
                 "is it cold", "is it warm", "is it hot", "is it freezing", "is it raining",
                 "is it snowing", "is it sunny", "cold outside", "warm outside", "hot outside",
                 "how warm", "cold enough", "warm enough", "snowing outside", "raining outside",
                 "like outside", "like it outside", "whats it like out", "what it like out",
                 "the temperature", "whats the temperature", "what temperature is it",
                 "how warm is it", "how cold is it", "how hot is it"),
     ("I can't check the forecast from here, sorry - no live weather in me. A weather app has "
      "today's for your postcode, hour by hour, and for a trip later in the year the monthly "
      "averages are the useful thing.",
      "No live weather from me, sorry. A forecast app or the national weather site has what is "
      "actually coming where you are, and the monthly averages for a trip months away.")),
    ("hours", ("opening hours", "opening times", "opening time", "open today", "open now",
               "close today", "closing time", "what time does", "what time do", "is it open",
               "shut today", "open on"),
     ("The opening hours are the first thing a venue changes and the last thing it tells "
      "anyone: a refurb, a bank holiday or new owners will do it. Their own page or map listing "
      "has the current ones.",
      "No opening hours in front of me. Whoever runs the place - a council tip, a chain, one "
      "landlord - announces a change itself, and its own page or phone number has today's.")),
    ("prices", ("how much is a", "how much does a", "how much are", "price of", "cost of",
                "exchange rate", "stock price", "how much is it"),
     ("I can't look up live prices, sorry. What a figure like that turns on is which one it is, "
      "where you buy it and the day, so two or three sellers compared all-in will beat the first "
      "price you see - their own site has today's number, and bring it back and I'll work out what "
      "it comes to a month.",
      "Prices move too fast for me to know. Which one you pick and where you buy it decide most "
      "of the figure, and a quick look at the seller's own site has today's number, all in with "
      "delivery - tell me what it says and I'll do the sums with you.")),
    ("news", ("the news", "headline", "who won", "the score", "latest on", "current events",
              "what happened in the"),
     (LIVE_NEWS_REPLY,)),
    ("roads", ("traffic", "the roads", "the road", "road closed", "closed road", "roadworks",
               "road works", "the motorway", "motorway closed", "in a jam", "jams",
               "accident on the", "accidents on the", "accident on", "accidents on",
               "diversion", "dual carriageway"),
     ("Traffic comes back at the same times on most weekdays, so a road that is slow at eight is "
      "usually slow at eight, while a closure or roadworks is a diversion and a different wait "
      "altogether. I can't see the roads from here, sorry: a maps app with live traffic, or the "
      "roads agency's own site, has today's jams, closures and roadworks as they happen.",
      "A jam clears from the front and a closure means a diversion, and those want different "
      "places looked at. I can't see the roads from here, sorry: the roads agency's own site has "
      "today's closures and roadworks, and a maps app with live traffic has the jams and how long "
      "each one is adding.")),
    ("travel", ("train times", "bus times", "next train", "next bus", "delayed",
                "is it running", "on strike", "buses running", "are the buses",
                "the trains running", "are the trains", "timetable", "the tube",
                "tube strike"),
     ("I can't check live times or delays, sorry. The operator's own app or site has the next "
      "departure and any disruption, and a journey planner puts the whole trip together.",)),
    ("journey", ("how long is the drive", "how long would the drive", "how long does the drive",
                 "how long is the journey", "how long would the journey", "how long is the trip",
                 "how long does it take to drive", "how long does it take to get to",
                 "how long to drive", "drive from", "drive to", "the drive be",
                 "how far is the drive", "how far from", "how far is", "how many miles"),
     ("The time a drive takes is mostly decided by the hour you set off and by the roads you use, "
      "since town streets and the last few miles are never motorway speed. I can't see either from "
      "here: a route planner has the figure for the hour you would actually leave, roadworks "
      "included, and the stops worth making on the way.",
      "However far it is, the drive will take longer than the distance suggests, because the first "
      "and last miles are the slow part and the hour you leave changes the rest. A route planner "
      "has it for your own leaving time; a maps app does the same from wherever you are.")),
    ("journey-ask", ("how long is the drive", "how long would the drive", "how long does the drive",
                     "how long will the drive", "how long is the journey", "how long would the journey",
                     "how long will the journey", "how long is the trip", "how long would the trip",
                     "how long will the trip", "how long is the flight"),
     ("The hour you set off and the roads you use decide most of a drive, and the first and last "
      "miles are the slow part wherever you are going. Long from where to where, and roughly when "
      "would you set off? I can plan the day around it once I know.",
      "The hour and the last few miles decide a journey, and either end can be the slow one. "
      "Where are you starting, where are you heading, and roughly when? I can work through the "
      "timing and the stops with you.")),
    ("distance", ("how far is", "how far away", "how many miles is", "how many miles from",
                  "how long is the walk", "how long is the bike ride"),
     ("I can't measure a distance from where you are, sorry. A map app does it from your own "
      "door in one tap, walking and driving both.",
      "That is a distance I can't take from this end. Put it into a map app and it shows how "
      "far and how long, from wherever you are standing.")),
    ("waste", ("bin day", "bin collection", "bin collections", "collection day", "recycling day",
               "is it recycling", "when do they collect", "when do the bins", "when are the bins",
               "when is the bin", "which bin goes out", "which bin is it", "black bin", "green bin",
               "blue bin", "brown bin", "food waste", "garden waste", "kerbside", "wheelie bin",
               "bulky waste", "household waste", "rubbish collection", "refuse collection",
               "missed bin", "bin lorry", "bin been collected", "bins been collected",
               "has the bin been"),
     ("Rounds are set street by street, not by town, and a bank holiday moves them by a day or "
      "two - so I can't see your street's day from here. The council's own site takes a postcode "
      "and gives the next collection; that is also where the holiday change is announced.",
      "Which day a street is collected on is the council's own choice, and holidays shift it, so "
      "there is nothing to know from this end without the postcode. The council's site has the "
      "round for your address, and a missed bin is free to report there on the day.")),
)

MY_OWN = {}

MY_RECORDS = (
    ("delivery", ("order", "orders", "parcel", "parcels", "delivery", "deliveries", "tracking",
                  "dispatch", "courier"),
     ("The tracking link in the order email or the shop's app shows exactly where a parcel is, "
      "and the shop can look the order up by your name and address - I can't see your order "
      "from here.",
      "Where a parcel has got to is in the tracking link you were sent; if it has not moved for "
      "days it is the shop you chase, not the courier. No way to check it from this end.")),
    ("booking", ("booking", "bookings", "reservation", "reservations", "appointment",
                 "appointments", "check-in", "check in"),
     ("The confirmation email or text has the time and the reference, and a ring to the place "
      "with your name and the day settles anything else - I can't see your booking from here.",
      "A booking lives with the place, not with me: the email or text you were sent has the "
      "time, and the desk can check it by name if that has gone missing.")),
    ("application", ("application", "applications", "claim", "claims", "renewal", "quote",
                     "complaint", "refund", "refunds"),
     ("The reference number they gave you brings it up on their site, and one call to the office "
      "gets you a straight answer - I can't see how it is going from here.",
      "The reference they gave you, or the email that came back when you sent it, has where it "
      "has got to, and a phone call gets it in a minute. Nothing of yours is in front of me.")),
    ("money", ("balance", "statement", "account", "direct debit", "standing order", "payment",
               "transaction", "overdraft"),
     ("Your bank's app, a cash machine or the number on the card shows the balance and what has "
      "gone out - I can't see your account at all.",
      "The figure is in your banking app or on the last statement, and the bank can confirm it in "
      "one call. Nothing of yours is here for me to look at.")),
    ("card", ("gift card", "gift cards", "voucher", "vouchers", "loyalty points",
              "loyalty card", "store card"),
     ("The number on the back of the card, or the shop's app, tells you what is left on it - I "
      "can't check a card balance from here.",
      "The card's own site, or the number on the back of it, has the balance; nothing of yours is "
      "here for me to look at.")),
)

CARD_VALIDITY = (
    "A card's expiry date is printed on the back of it, and the shop's app shows it too. If it "
    "has run out, ring the shop - many will swap it or move what is left onto a new one.",
    "The date it runs out is on the back of the card, or in the shop's app. An out-of-date card "
    "is worth one phone call: shops can often swap it or put the balance back as credit.",
)

HEALTH_RECORD = ("prescription", "prescriptions", "scan", "scans", "referral", "referrals",
                 "x-ray", "xray", "x-rays", "bloods", "blood test", "test results", "results")

HEALTH_WORLD = ("doctor", "gp", "surgery", "hospital", "clinic", "nurse", "midwife", "consultant",
                "dentist", "medical", "health", "test", "blood", "scan", "x-ray", "xray",
                "prescription", "consultant", "specialist", "appointment")

OFFICE_RECORD_LINES = (
    "I can't see that from here - nothing of yours reaches me, so I can't say where it has got "
    "to. The letter, email or reference number it came with will bring up its state on their "
    "site, and one call to the office that issued it settles it.",
    "Nothing of yours here to look at, sorry, so I can't check that one. Whatever it came from "
    "- the letter, the email or the app it was arranged through - has where it has got to, and "
    "the number they gave you gets it in a minute on the phone.",
    "That state is theirs to know and mine to guess at, and a guess is no use to you. The "
    "confirmation you were sent is the one place it is written down, and the office that deals "
    "with it can confirm it in one call.",
)

AT_THE_TILL = (
    "Count it against the receipt before you leave it too long: the till's own record of the sale "
    "is what the shop works from, and a counter sorts it on the day far more easily than a head "
    "office does later. How much short are you?",
    "That is the shop's to put right, not yours to prove - the receipt and the amount is usually "
    "enough at the counter, and most shops fix it the same day. If it was a card, your statement "
    "has the figure the till rang up.",
)

MY_OWN_DAY = (
    "I can't see your rota from here, sorry - nothing of your work reaches me, so your hours are "
    "with whoever writes it and in the app your work puts it in.",
    "No window on your shifts from this end, sorry: the start and finish times are on the rota, "
    "with your manager or in the rota app your work uses.",
    "That one lives on the rota rather than anywhere I can see - your manager has the hours, and "
    "your contract has the ones they have to keep to.",
)

MY_BILL_LINES = (
    "What you pay is on your own bill rather than in any price list I could read: the app or the "
    "email they send you has the monthly figure, and the bank statement under the same name shows "
    "it went out. Tell me what it is and I'll work out what it comes to over the year, and check "
    "the notice you would need to give.",
    "I can't see your bill, sorry. The provider's app, the last email from them or your bank "
    "statement has the figure, and the same place has the minimum term - that is what decides "
    "whether you can leave and what it costs to stop. Give me the numbers and I'll do the sums.",
    "That price is between you and them, and only your own paperwork has it. The app, the bill "
    "email or the direct debit on your statement is where to look, and the contract length and "
    "notice period sit on the same page - worth knowing before you think about changing it. Hand "
    "me the figures and I'll work the rest out.",
)

POINTS_LINES = (
    "Points build up wherever the card or the app gets scanned, and the scheme's own points page "
    "has the balance and the day they run out - most clear an account after a year or two with "
    "nothing on it. Tell me what a point is worth in that scheme and I'll work out the money.",
    "I can't see your points from here, sorry - only the scheme can. Their app, a receipt or the "
    "number on the back of the card shows the balance, and it is worth a look if the card has been "
    "in a drawer, because points usually expire after a year or so with no activity. Give me the "
    "figures and I'll do the arithmetic on what they buy.",
    "That balance lives with the scheme rather than with me. The app's points page has it, and the "
    "same page says when they expire - a year or two of no use is the usual rule, though each "
    "scheme sets its own. Hand me the rate and the count and I'll tell you what it comes to.",
)

HEALTH_RECORD_LINES = (
    "I can't see your records from here. The surgery's app or a ring to reception has the date "
    "and the result, and they can say whether anyone needs to see you about it.",
    "Nothing of yours in front of me, sorry. The letter, text or app it came through will have "
    "the date and what came of it, and reception can look it up if that is lost.",
)

OWN_PLACE = ("shop", "store", "stores", "branch", "office", "cafe", "café", "canteen",
             "pub", "bar", "gym", "surgery", "pharmacy", "chemist", "bank", "salon",
             "museum", "tip", "library", "restaurant", "takeaway", "chippy", "garage",
             "hotel", "school", "nursery", "clinic", "centre", "center", "pool", "market",
             "stall", "van", "kiosk", "studio", "workshop")

OWN_PERSON = ("son", "daughter", "kid", "kids", "child", "children", "baby", "wife",
              "husband", "partner", "mum", "mom", "mother", "dad", "father", "boyfriend",
              "girlfriend", "nan", "grandma", "grandad", "grandson", "granddaughter")

LIVE_NOT = ("difference", "climate", "how does", "why does", "why do ", "explain", "meaning of")

LIVE_NOT_HOURS = ("sun", "sunrise", "sunset", "sun set", "sun rise", "moon", "moonrise",
                  "tide", "tides", "high tide", "low tide", "dawn", "dusk", "daylight",
                  "stars", "milky way", "eclipse")

LIVE_VENUE = ("shop", "store", "supermarket", "tesco", "asda", "sainsbury", "aldi", "lidl",
              "co-op", "coop", "morrisons", "waitrose", "iceland", "branch", "bank",
              "post office", "postbox", "library", "pharmacy", "chemist", "surgery", "gp",
              "doctor", "dentist", "vet", "tip", "dump", "recycling centre", "cafe", "café",
              "restaurant", "takeaway", "chippy", "pub", "bar", "gym", "leisure centre",
              "pool", "museum", "gallery", "garden centre", "centre", "market", "salon",
              "barber", "hairdresser", "office", "clinic", "hospital", "school", "nursery",
              "garage", "hotel", "station", "airport", "council", "launderette", "kiosk",
              "studio", "workshop", "church", "hall", "venue", "park", "butcher", "bakery",
              "greengrocer", "depot", "club")
LIVE_VENUE_RE = re.compile(
    r"(?<![a-z])(?:" + "|".join(re.escape(word) for word in
                                sorted(LIVE_VENUE, key=len, reverse=True)) + r")(?:s|es)?(?![a-z])")

LIVE_OPEN_CLOSE = ("open", "opens", "opening", "opened", "close", "closes", "closing", "closed",
                   "shut", "shuts", "shutting", "close up")
LIVE_HOURS_ASK = re.compile(
    r"\b(?:when|what time|what hours|how late|what times)\s+"
    r"(?:does|do|is|are|will|would|can|doesnt|don't|dont|isnt|is it)\b"
    r"[^.!?]{0,40}?\b(?:open|opens|closed|closes|close|shut|shuts|shutting|closing|"
    r"re-?opens?|re-?opening|re-?opened)\b")
LIVE_YES_NO_OPEN = re.compile(
    r"^\s*(?:so|and|but|ok|okay|also|hi|hello|morning|quick one)?\s*,?\s*"
    r"(?:is|are|will|does|do|can)\s+[^.!?]{0,40}?"
    r"\b(?:open|opens|shut|shuts|closed|closing|close)\b"
    r"(?!\s*(?:up|ness|ing|ly|air|plan|letter|account|evening|day|days|morning|"
    r"afternoon)\b)"
    r"(?!\s*to\s+(?!the\s+public\b))")

LIVE_INDOOR = ("oven", "fridge", "freezer", "room", "bedroom", "nursery", "bath", "shower",
               "kettle", "boiler", "radiator", "washing machine", "tumble dryer", "air fryer",
               "slow cooker", "grill", "hob", "pan", "oil", "water", "iron", "greenhouse",
               "shed", "garage", "car", "engine", "laptop", "phone", "kitchen", "loft",
               "attic", "cellar", "basement", "conservatory", "living room", "sitting room",
               "dining room", "hall", "hallway", "porch")

LIVE_WEATHER_WORDS = ("weather", "wether", "weathr", "forecast", "forcast", "rain", "raining",
                      "rainy", "snow", "snowing", "sunny", "sun", "wind", "windy", "outside",
                      "outdoors", "umbrella", "coat", "bbq", "barbecue")

LIVE_SKY = ("windy", "icy", "muggy", "humid", "cloudy", "overcast", "chilly", "freezing",
            "heatwave", "rain", "raining", "rainy", "snow", "snowing", "snowy", "storm",
            "stormy", "thunder", "thundery", "hail", "hailing", "fog", "foggy", "mist", "misty",
            "drizzle", "drizzling", "showers", "frost", "frosty")

LIVE_SKY_OFF = ("brain fog", "foggy head", "head is foggy", "head foggy", "misty eyed",
                "hail a taxi", "hail a cab", "weather the storm", "storm in a teacup",
                "under the weather", "frost free", "frost-free", "rain check")

LIVE_SKY_WHY = re.compile(r"\b(?:why|how\s+come|what\s+causes|what\s+makes)\b")

LIVE_WEAR = ("umbrella", "coat", "jacket", "shorts", "boots", "wellies")

LIVE_SETTING = ("gym", "work", "office", "school", "college", "uni", "class", "nursery",
                "dinner", "lunch", "party", "wedding", "funeral", "interview", "hospital",
                "indoors", "inside", "in the house", "shopping", "the shops", "the dance")

LIVE_SOON = ("today", "tonight", "tomorrow", "this afternoon", "this morning", "this evening",
             "this weekend")

LIVE_TAKE_ASK = ("should i take", "shall i take", "do i take", "do i need", "will i need",
                 "should i bring", "shall i bring", "do i need to take", "should i wear",
                 "shall i wear", "should i put on", "will i be needing", "do i want")

LIVE_TAKE_ALLOWED = {"to", "the", "a", "an", "my", "our", "your", "and", "or", "out", "outside",
                     "tonight", "today", "tomorrow", "now", "later", "morning", "afternoon",
                     "evening", "weekend", "with", "me", "it", "this", "on", "in", "at", "for",
                     "when", "i", "should", "shall", "do", "need", "will", "be", "bring", "take",
                     "wear", "put", "want", "going", "am"}

LIVE_JOURNEY_ENDS = ("from", "to", "towards", "as far as")

LIVE_TRAVEL_WORDS = ("train", "trains", "bus", "buses", "coach", "flight", "flights", "plane",
                     "tram", "tube", "ferry", "motorway", "traffic", "road", "line", "strike")
LIVE_ROAD_NAME = re.compile(r"\b(?:m|a)\d{1,3}(?:\s?\(m\))?\b")
LIVE_PAPER_WORDS = ("paper", "card", "cardboard", "envelope", "printer", "print", "printing",
                    "printed", "poster", "frame", "photo", "photograph", "notebook", "canvas",
                    "sketchbook", "drawing", "stationery", "folder", "binder")
LIVE_ROAD_WORDS = ("road", "roads", "motorway", "traffic", "junction", "bypass", "roundabout",
                   "carriageway", "lane")
LIVE_SITE_THING = ("site", "website", "web page", "webpage", "online shop", "shop", "store",
                   "etsy", "listing", "my page", "the page", "web stats", "footfall")

LIVE_ROADS_NOT = ("road tax", "tax the", "road trip", "road bike", "off road",
                  "web traffic", "site traffic", "online traffic", "search traffic", "footfall",
                  "foot traffic", "my website", "my site", "my shop", "my store", "my etsy",
                  "website", "shop window", "customers through",
                  "dead", "fox", "badger", "hedgehog", "deer", "animal", "pothole",
                  "who do i call", "who do i report", "report a", "report the",
                  "tips", "advice", "how do i drive", "driving in", "long drive",
                  "driving test", "theory test", "driving licence", "driving license",
                  "how do i get", "how to get", "how far is", "directions to", "route to",
                  "made of", "built", "why do", "why are roads", "surface", "roadworthy",
                  "cycle lane", "cycle path", "bus lane", "parking", "speeding", "points on",
                  "school", "college", "class", "revision", "study")

LIVE_DELAY_WORDS = ("cancelled", "canceled", "cancellation", "delayed", "delay", "delays",
                    "on time", "running late", "disruption", "engineering works",
                    "replacement bus", "bus replacement")

LIVE_STRONG = ("times", "forecast", "opening hours", "opening times", "how much", "price",
               "what time", "the score", "latest on",
               "latest news", "news today", "any news today", "any headlines",
               "any news on", "any news about", "any news of", "any update on", "any word on",
               "spill the news", "any results", "any result", "what channel",
               "any traffic", "traffic problems", "road closed", "closed road",
               "train timetable", "bus timetable", "are the buses", "are the trains",
               "buses running", "trains running", "tube line", "the m25 closed", "m25 closed")

HOW_ARE_YOU_ASKS = ("how are you", "how are things", "how is things", "how's things",
                    "how's your day", "how is your day", "your day going",
                    "howz your day", "whats your day", "hows your day",
                    "how's it going",
                    "how is it going", "how have you been", "you doing", "you ok", "you okay",
                    "you all right", "how do you do",
                    "you up to", "up to much", "been up to")

HOW_ARE_YOU_GOING_ON = ("much going on", "going on")

HOW_ARE_YOU_GOING_ON_AFTER = frozenset({"else", ""})

HOW_ARE_YOU_TAGS = frozenset((
    "today", "tonight", "now", "then", "so", "far", "lately", "recently", "again", "too",
    "mate", "guys", "everyone", "everybody", "all", "both", "honestly", "anyway", "though",
    "thanks", "sir", "madam", "doing", "feeling", "keeping", "coping", "holding", "up",
    "these", "days", "at", "the", "moment", "folks", "friend", "love", "team",
    "been", "like", "going", "lately",
    "been", "going", "looking", "hmm", "lol",
    "go", "gone",
))

HOW_ARE_YOU = (
    "Good, thanks for asking — and good to have you here. What's on your mind?",
    "Can't complain. Better question: how are you doing?",
    "Fine and busy, the two usual things. How's your day been?",
    "I'm well, thanks. What are you up to today?",
)

ADVICE_WORDS = ("should", "worth", "better", "cheaper", "faster", "recommend", "suggest",
                "which", "how do", "how can", "any tips", "less", "fewer", "more", "difference",
                "correct", "grammar", "spell", "'")

REQUEST_CUES = ("quick one", "quick question", "one more thing", "another thing", "need help",
                "any tips", "any advice", "advice", "how do", "how can", "what should", "can you",
                "could you", "help me", "give me", "recommend", "suggest", "wondering", "?")

JUDGE_ASKS_SLIGHT = r"(?:stupid|daft|dumb|silly|idiotic|thick|bad|terrible|awful|dreadful|wrong)"

JUDGE_ASKS_FINE = r"(?:good|great|sensible|wise|smart|clever|reasonable)"

JUDGE_ASKS_MAD = r"(?:mad|crazy|insane|nuts|mental|unhinged)"

JUDGE_NOUN = r"(?:idea|plan|thing|move|call|choice|decision|approach|bet|notion|step)"

JUDGE_BARE_FACES = frozenset("""sensible wise reasonable smart clever stupid daft dumb silly
    idiotic bad terrible awful dreadful wrong mad crazy insane nuts mental unhinged""".split())

JUDGE_LEAD = (r"(?:^|\b(?:ok|okay|so|and|but|well|honestly|tbh|maybe|i think|i reckon"
              r"|i guess|i feel like)\b )")

JUDGE_PLAN_STOP = frozenset("""but because so then since if unless although though which who that
    when where while whereas before after once""".split())

JUDGE_NOD_WORDS = frozenset("""yes yeah yep no nope ok okay sure right cool thanks thank you
    hmm mm mmm well so and but true fair good nice haha lol oh ah please""".split())

JUDGE_PLAN_HAS_A_HOLE = (
    "{Plan} is where it gets tight, and that is the part to answer for. What would you do if "
    "it went wrong?",
    "{Plan} is the part a friend would push back on, not the wanting. Say what you would do if it "
    "did not work, and if that is quick to say, go.",
    "{Plan} leaves nothing spare, and that is the part I would look at. What is your answer if it "
    "goes wrong?",
)

JUDGE_WORTH = (
    "Not stupid, no. {Plan} is the ordinary kind of thing people do; what decides it is what you "
    "would do if it went wrong - if that leaves you all right, go.",
    "Nothing wrong with {plan}. The part that goes wrong is having no answer for what if it does "
    "not work.",
    "Nothing daft in {plan}. Say what you would do if it went wrong; if that is quick to say, do it.",
)

JUDGE_WORTH_PLAIN = (
    "Not stupid. The test is what you would do if it went wrong: if that leaves you all right, "
    "there is nothing daft in it.",
    "No, it is not stupid. The thing that would make it stupid is having no answer for what if "
    "it goes wrong.",
    "Nothing daft about it. Ask what you would do if it went wrong - if you would be fine, go.",
)

JUDGE_FINE = (
    "Yes, it makes sense - {plan} is a reasonable thing to aim at. The part that bites is doing it "
    "with no answer for what if it goes wrong.",
    "{Plan} is the ordinary thing to do; what bites is doing it with no plan for when it goes wrong.",
    "Yes - {plan} is worth doing. The one thing to have ready is an answer for what if it goes "
    "wrong.",
)

JUDGE_FINE_PLAIN = (
    "Yes, it makes sense. Have a line ready for what you would do if it went wrong, and there is "
    "nothing left to worry about.",
    "It sounds sensible to me. Say in one line what you would do if it went wrong - if that is "
    "easy to say, go.",
)

JUDGE_SANE = (
    "Not mad. {Plan} is the kind of thing plenty of people do, and the test is the one any plan "
    "gets: what would you do if it went wrong?",
    "No, you are not mad. {Plan} is worth weighing, and the thing to have ready is an answer for "
    "what if it goes wrong.",
)

JUDGE_SANE_PLAIN = (
    "Not mad at all. The test is the one any plan gets: what would you do if it went wrong? If "
    "that leaves you all right, go.",
    "No, you are not mad. Wanting something different is normal - have an answer ready for what "
    "if it goes wrong and that is the whole of it.",
)

JUDGE_NO_PLAN = (
    "About what? Tell me the idea in a line and I will say what I think.",
    "There is nothing for me to judge yet - say the idea in a line and I will tell you straight.",
)

JUDGE_NO_PLAN_MAD = (
    "Nothing you have said sounds mad to me. What is the thing you are weighing up?",
    "Mad about what? Tell me what you are thinking of doing and I will give you a straight answer.",
)

JUDGE_NO_PLAN_MIND = (
    "Nothing you have said sounds mad to me. And it is worth telling a GP, who hears this often "
    "and knows what to do with it.",
    "That is a frightening thing to carry, and not one to sit on: a GP is the right first call, "
    "and you can describe it in a line.",
    "I would not wait for that to get worse before saying it to somebody. A GP is the one to say "
    "it to - what happens, and how often - and let them say what it is.",
)

JUDGE_NO_PLAN_FINE = (
    "Probably - but say what it is in a line and I will tell you straight.",
    "Nothing you have said sounds unwise to me. What is the thing you are weighing up?",
)

JUDGE_WISH_ANGRY = (
    "No, I would not do that. Something has pushed you a long way - what happened?",
    "That is the anger doing the thinking. Not that one. What has actually gone on?",
    "I would not. Whatever they did, that lands on you and not on them. Tell me what happened.",
)

JUDGE_ONLY_A_PLAN = frozenset(("stupid", "daft", "dumb", "silly", "idiotic", "thick"))

JUDGE_SOUNDS_FINE = frozenset(("wise", "sensible", "smart", "clever", "reasonable"))

JUDGE_SELF_JUDGING = frozenset(("mad", "crazy", "insane", "nuts", "mental", "unhinged"))

JUDGE_NOT_A_VERDICT = frozenset(("bad", "terrible", "awful", "dreadful", "wrong"))

JUDGE_NOT_A_GERUND = frozenset(("ring", "bring", "sing", "ping", "cling", "sting", "swing",
                               "wring", "spring", "string", "thing", "kings", "wing", "ding"))

YOURS = {"my": "your", "me": "you", "myself": "yourself", "mine": "yours"}

A_PLACE_I_DONT_KNOW = (
    "I've not been there, so I can't vouch for it - what are you after: the sights, the food, or "
    "somewhere quiet?",
    "I don't know it well enough to promise you anything. What would make the trip good for you?",
    "No first-hand knowledge of the place, sorry. Are you going for the sights, the food or the "
    "peace?",
    "Honestly I can't tell you what it's like there. What matters most to you about the trip?",
)

WORD_FIXES = {"what": "what", "whats": "what", "wats": "what", "wat": "what",
               "wot": "what", "hows": "how", "whos": "who", "wheres": "where",
               "whys": "why", "whens": "when", "cn": "can", "cud": "could"}

QUESTION_WORDS = frozenset(("what", "why", "how", "when", "where", "who", "which", "can",
                            "could", "should", "would", "will", "do", "does", "did", "is",
                            "are", "have", "has"))

CARD_LINES = (
    "Two lines is plenty: say the thing you would say out loud if they were in front of you.",
    "Name them, say the one specific thing you are glad about, and sign it — short and warm "
    "beats long and clever.",
    "Write it the way you would speak it, then read it back once and take out the careful bits.",
)

TELL_HARD_LINES = (
    "Say the hard sentence first and keep it short - they will hear the rest better after it. "
    "Tell me how you want to put it and I'll help you word it.",
    "Pick a calm moment, say the one thing that matters, then stop and let them answer. Give me "
    "the gist and I'll draft it with you.",
    "Plain words, early, and no long build-up: that is kinder than a soft run at it. Tell me the "
    "gist and I'll help you shape it.",
)

WORDING_LINES = (
    "Say the one thing that matters first, then the rest. Give me the gist and I'll draft it.",
    "Keep it to two sentences: what happened, then what you want. Send me the gist and I'll put "
    "it in words.",
    "Two or three lines is plenty: what happened, what you want, and by when. Give me the gist "
    "and I'll draft it.",
    "Lead with what you want and why, then stop. Tell me the gist and I'll write the first "
    "version for you.",
    "Write it the way you would speak it, then take out the careful bits. Give me the gist and "
    "I'll do a pass over it.",
)

GREETING_WORDS = frozenset(("hi", "hello", "hey", "hiya", "morning", "afternoon", "evening",
                            "greetings", "yo", "howdy"))

NOT_NOTED = (
    "Remind me of the name and I'll keep it from here.",
    "Say the name again and I'll remember it from here on.",
    "I haven't got it in front of me \u2014 tell me the name and I'll hold on to it.",
)

NOT_A_NAME = frozenset((
    "yesterday", "today", "tomorrow", "tonight", "morning", "afternoon", "evening", "night",
    "week", "month", "year", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday",
    "sunday", "it", "him", "her", "them", "that", "this", "one", "again", "back", "up", "out",
    "off", "in", "on", "the", "a", "an", "and", "but", "so", "then", "now", "already", "twice",
))

ASK_ONLY = frozenset(("what", "whats", "did", "do", "does", "i", "we", "my", "our", "the", "a",
                      "an", "is", "was", "call", "called", "name", "named", "again", "and", "so",
                      "it", "him", "her", "them", "s", "say", "said", "tell", "told", "you",
                      "remember", "recall", "about", "to", "of"))

HANDED_BACK = (
    "You called it {name} \u2014 I've kept that.",
    "{name} \u2014 that's the one you gave me, and it's still here.",
    "It's {name}, isn't it? I've got that down.",
)

POINTING = frozenset((
    "a", "about", "again", "all", "also", "am", "an", "and", "any", "anything", "are", "as", "at",
    "be", "but", "by", "can", "could", "did", "do", "does", "for", "from", "get", "got", "had",
    "has", "have", "how", "i", "if", "in", "into", "is", "it", "its", "just", "like", "me", "more",
    "my", "no", "not", "of", "on", "one", "or", "our", "out", "should", "so", "some", "still",
    "than", "that", "the", "their", "them", "then", "there", "these", "they", "thing", "things",
    "this", "those", "to", "too", "up", "us", "was", "we", "were", "what", "when", "which", "who",
    "why", "will", "with", "would", "you", "your",
    "year", "years", "date",
))

RULED_OUT_DETERMINER = frozenset(("the", "a", "an", "my", "your", "his", "her", "their", "our",
                                  "its", "this", "that", "these", "those", "any", "some",
                                  "another", "every", "each", "no"))

PARTICLE = frozenset(("out", "up", "off", "down", "through", "back", "away", "round", "over",
                      "about", "along"))

TIPS_OWNER = {"my": "your", "our": "your", "i": "you", "im": "you're", "i'm": "you're",
              "me": "you", "mine": "yours", "we": "you", "us": "you"}

TIPS_CLAUSE = frozenset("""
    i i'm im i've ive we we're weve he she they wont will would going
    gonna wanna want wants wanted need needs needed have has had is are was were am do does did
    dont don't didnt didn't cant can't cannot keep keeps kept eat eats eet said say says told get
    got make makes made feel feels felt think thinks thought try tried
""".split())

TIPS_VERB = frozenset("""
    wake sleep stop start learn lose save cook run quit find use take put fix write buy sell move
    change switch pick choose sort become study give tell show send list suggest recommend get
    need want try help make do
""".split())

TIPS_AHEAD = (
    "Start with the one thing that usually goes wrong, not the whole list. How long have you "
    "got?",
    "What's worrying you most about it? With the time you have, that decides what's worth doing.",
    "Pick the part you would most hate to get wrong and practise that bit. When is it?",
)

TIPS_THING = (
    "What have you got so far, and what isn't working? That tells me which advice is worth "
    "having.",
    "What's the thing you most want to get right? That's the part worth spending advice on.",
    "What usually goes wrong? Start there, not with the whole list.",
)

TIPS_LINES = (
    "Happy to help — tell me what you've got so far and I'll add what I can.",
    "Sure. What have you tried so far? That tells me where to start.",
)

HELP_ALREADY = (
    "That's most of what I know on it — say which part is still unclear and I'll come at it "
    "another way.",
    "That's the lot I have on that one. Tell me which bit isn't landing and I'll try a "
    "different angle.",
)

SAME_AGAIN = (
    "That is all of what I know on it - say if you want any part of it again, or slower.",
    "That was the whole of my answer on it. Tell me which part to take further and I will.",
    "That is everything I have on that one, so I would only repeat myself. Which bit do you want "
    "me to go into?",
)

SAME_AGAIN_WITH_THE_ANSWER = (
    "Same answer, and it covers this: {answer}",
    "That is still the answer: {answer}",
    "The answer above holds: {answer}",
)

VIEW_ONLY_WORDS = frozenset("""
    a an the and but so or if to of at on in with about between for from as
    what whats is was your my you u ur ya i me we us our it its that this there here
    be is are do does did would could should will can
    reckon think say said view opinion take takes thoughts verdict read call answer answers
    honest honestly own real true personal actually really truly
    ok okay well then now just too also again please thanks thank
    give tell me full whole thing things one on it that this
    d r wat
""".split())

VIEW_LINES = (
    "Honest answer: {said}",
    "Same as I said: {said}",
    "My view has not changed: {said}",
    "Honestly, that is still where I would land: {said}",
)

VIEW_ASK_LINES = (
    "What I would still want to know: {said}",
    "Same question from me: {said}",
    "I would still ask you the same thing: {said}",
    "That question is still the one I would put to you: {said}",
)

VIEW_DECIDE = (
    "Same as before: that one is yours to call. What it turns on is what you gain against what "
    "you would give up — say both and I will help you weigh them.",
    "It stays your call rather than mine. Tell me the two things you are weighing and I will lay "
    "them side by side.",
)

VIEW_HANDBACK = ("not mine to decide", "not a call i can make", "can't call that one",
                 "cant call that one", "that's your call", "thats your call")

NOT_AN_ANSWER = NEUTRAL + NEWS_TO_COME + POSITIVE + RELIEF + CONGRATS

_ECHO_FILLER = frozenset("""
a an the i im i'm ive i've id i'd me my we us our you your it its it's that thats this these
those is are was were am be been being do does did done have has had of to in on at for with
and but so then than just really very quite too also about from by as or if not no yes yeah ok
okay well right got get gets here there what whats how why when who said say says think
""".split())

PRAISE = ("congratulations", "congrats", "well done", "nice one", "brilliant", "lovely",
          "great news", "good stuff", "glad", "pleased", "fantastic", "amazing", "excellent",
          "love that", "that's great", "thats great", "weight off", "good for you", "enjoy it")

VIEW_ON_GOOD_NEWS = (
    "Nothing to weigh up there - that is just good news. Enjoy it: what is the first thing "
    "you will do about it?",
    "Honest answer: take the win. There is no decision in it, and I would not spoil it hunting "
    "for one. What happens next?",
)

HEDGE_POOL = (UNKNOWN, UNKNOWN_DECIDE, UNKNOWN_MONEY, UNKNOWN_HEALTH, UNKNOWN_WORD,
              UNKNOWN_WORRY, finding_out.PLACE_POOL, finding_out.TRADE_POOL,
              finding_out.PROFESSIONAL_POOL, finding_out.PICK_POOL, finding_out.WHO_POOL,
              finding_out.HOW_MANY_POOL, finding_out.BUY_POOL, finding_out.FIGURE_POOL,
              finding_out.WRECKED_POOL, finding_out.PLACE_ROUTE_POOL)

OUTCOME_LINES = (
    "Nobody can say for certain yet, and anyone who does is guessing. Ask the staff looking after "
    "them what they are watching for over the next day or two, and what would be a good sign.",
    "There is no honest yes or no from here - the ward is the only place with a real answer. Ask "
    "the nurse in charge what has to improve before the next step, and ask again tomorrow.",
    "No one can tell you that yet. The people treating them can say what they are watching for "
    "and what a good day would look like, and that is the question worth asking today.",
)

VIEW_MIRROR_LINES = (
    "Nothing has changed for me: {said}",
    "I would say the same again: {said}",
    "That still stands: {said}",
)

VIEW_COMPANY = (
    "Nothing to add to that, and no view of mine worth putting on top of it. What I said still "
    "stands, and I am here if you want to say more.",
    "I have not got a view to give you on top of that - only the same thing again, which is that "
    "it matters. Tell me how you are doing with it.",
    "Nothing I could add would beat what I already said. If you want to say more about it, I am "
    "listening.",
)

VIEW_NO_SUBJECT = (
    "On what? Give me the thing you are weighing up and I will tell you straight.",
    "Happy to - what's it about? Name the choice you are stuck on and I'll give you my honest take.",
    "What is it about? Name the thing you are stuck on and I will give you my honest take.",
)

VIEW_AFTER_A_DEATH = (
    "If it is my view you want: nobody gets this right, and being all over the place is not doing "
    "it wrong.",
    "Honestly? There is no right way to do it, and no timetable you have to be on.",
    "My view is only that it is allowed to be this hard. You are not doing it wrong.",
    "Nothing I could add would help more than what I said. Tell me about them, or don't - either "
    "is fine by me.",
)

VIEW_LEAD_IN = frozenset((
    "thing", "things", "way", "ways", "point", "points", "answer", "answers", "plan", "rule",
    "rules", "step", "steps", "advice", "short", "version", "part", "parts", "bit", "bits",
    "key", "difference", "same", "rest", "other", "first", "next", "best",
))

NO_MORE_OF = frozenset(("", "greeting", "safety", "urgent", "grief", "loss"))

TIPS_UNIT = frozenset(("year", "years", "yr", "yrs", "month", "months", "week", "weeks", "day",
                       "days", "hour", "hours", "min", "mins", "minute", "minutes", "stone",
                       "st", "kg", "kgs", "lb", "lbs", "pound", "pounds", "mile", "miles", "km",
                       "k", "quid", "grand", "per", "cent", "percent"))

WHERE_SOMETHING_WRONG = SICKNESS | frozenset((
    "leak", "leaks", "leaking", "damp", "mould", "mold", "smell", "smells", "smelly", "noise",
    "broken", "broke", "trip", "tripped", "tripping", "fuse", "wiring", "wire", "hurt", "hurts",
    "hurting", "pain", "painful", "sore", "ache", "aches", "aching", "rash", "bite", "bitten",
    "sting", "stung", "bump", "bleed", "bleeding", "swollen", "swelling", "crack", "cracks",
    "cracked", "blocked", "clogged", "wont", "won t", "not working", "stopped working",
    "chest", "throat", "stomach", "tummy", "belly", "back", "head", "leg", "legs", "arm",
    "arms", "hand", "hands", "foot", "feet", "knee", "knees", "shoulder", "neck", "hip",
    "wrist", "ankle", "toe", "toes", "finger", "fingers", "eye", "eyes", "ear", "ears",
    "tooth", "teeth", "gum", "gums", "mouth", "skin", "joint", "joints", "ribs", "breast"))

QUOTE_LINES = (
    "Get one more quote for the same job in writing, and ask what is included: the parts list is "
    "what makes two prices comparable.",
    "Ask for a written quote split into parts and labour, then ring one other firm for the same "
    "job. That pair of numbers tells you more than any rule of thumb.",
)

GIFT_WORDS = frozenset(("present", "presents", "gift", "gifts", "spend on", "budget for",
                        "how much do you spend", "what do you get"))

BUYING_WORDS = frozenset(("buying", "buy a house", "buy a flat", "buy a home", "bought",
                          "purchase", "ladder", "mortgage", "own a home", "should i buy"))

NETWORK_WORDS = frozenset(("wifi", "wi-fi", "internet", "broadband", "network", "connection",
                         "signal", "online"))

MEDS_WORDS = frozenset(("tablets", "pills", "medicine", "medication", "prescription", "dose",
                        "doses", "capsules", "antibiotics", "vaccine", "vaccination", "jab",
                        "jabs", "vitamin", "vitamins", "supplement", "supplements", "ibuprofen",
                        "paracetamol", "aspirin", "painkiller", "painkillers", "antihistamine",
                        "antihistamines", "steroid", "steroids", "insulin", "inhaler"))

ENDINGS = frozenset((
    "s", "es", "ed", "d", "ing", "e", "y", "ion", "al", "ness", "able", "ly",
))

NOT_A_FORM = frozenset((
    "bloody", "rasher", "rashers", "teether", "waker", "stationary",
    "teething",
))

_OPENING_QUESTIONS = frozenset(("what", "why", "how", "when", "where", "who", "which"))

ABOUT_ITSELF_KINDS = ("model", "limits", "online", "agency", "identity", "purpose",
                      "workings", "privacy", "trust", "judging", "secret", "asking")

MODEL_NAMED_WORDS = 7

MY_WORKINGS = frozenset(("learn", "think", "wrong"))

PICKS_A_MECHANISM = frozenset("""
decide decides deciding decided decision decisions choose chooses choosing chosen choice choices
pick picks picking select selects sort sorts answer answers answering answered
""".split())

WORRY_FILLER = frozenset("""
    i im i'm am so really very pretty quite a bit little lot kind kinda of still just and ok
    okay that thats it its now too much all this
""".split())

WORRY_WORDS = frozenset("worried worrying anxious nervous".split())

NOT_THEIR_VERB = frozenset(("with", "for", "about", "of", "to", "at", "in", "on", "from",
                            "by", "like", "without", "over", "under", "into", "the", "no",
                            "any", "some", "his", "her", "their", "your"))

FIRST_PERSON = frozenset(("i", "im", "i'm", "i am", "me", "am", "you", "we", "us"))

FORGETTING = frozenset(("forget", "forgets", "forgot", "forgetting"))

EATING = frozenset(("eat", "eats", "eating", "ate", "eaten"))

EATEN_KIND = frozenset((
    "meat", "fish", "dairy", "gluten", "nuts", "eggs", "cheese", "pork", "beef", "chicken",
    "lamb", "bacon", "ham", "shellfish", "seafood", "sugar", "carbs", "bread", "rice",
    "pasta", "chips", "vegetables", "veg", "veggies", "fruit", "salad", "spuds", "potatoes",
    "vegan", "vegetarian", "halal", "kosher",
))

OURS = frozenset(("my", "our", "me", "us"))

GOOD_TIME_WORDS = frozenset("""lovely great brilliant wonderful good nice amazing fun fantastic
    smashing crackin delicious gorgeous tasty superb class memorable""".split())

QUESTION_OPENERS = frozenset("""was were is are am did does do have has had how what when where
    why who whose would will can could should shall may might""".split())

NOT_A_VERDICT_SUBJECT = frozenset("""
ward hospital hospice clinic surgery casualty a&e icu itu nurses nurse staff doctors doctor
consultant midwife surgeon matron theatre anaesthetic anaesthetics wake funeral burial cremation
crematorium memorial chapel servicio tests results scan chemo chemotherapy dialysis
service services eulogy eulogies graveside flowers mass readings reading sermon hymn hymns vigil
rosary cemetery ashes casket hearse obituary tributes tribute condolences send-off sendoff
paramedics ambulance paramedic carers carer counsellor counsellors physio physiotherapist vet vets
police firemen firefighters
""".split())

A_DREAD = (
    "Fair enough - what's the part you're dreading?",
    "That's understandable. What's coming up that you're not looking forward to?",
    "I don't blame you. What is it about it?",
)

A_WANT_IT_OVER = (
    "Sounds like it's been a long one - what's been the worst of it?",
    "Fair enough. What's making it drag?",
    "That sort of week does that to people. What do you most want behind you?",
)

A_DAY_AHEAD = (
    "Something to look forward to, then - what's the plan?",
    "Nice. How are the plans going?",
    "Good. Is there much to sort out first?",
)

A_DAY_AHEAD_TENSE = (
    "How are you feeling about it?",
    "How ready do you feel for it?",
    "Is there much to get ready before it?",
)

A_PAUSE_WORD = frozenset("""
    a an the and or but so then than that this these those it its im i i've ive id i'd me my
    mine we us our you your yours he she they them his her their there here now just only really
    very quite bit little all of in on at to for from with about as if not no yes oh ok okay
    sorry apologies apologie again back still also too already been was were is are am be being
    because cos cause cus since seeing
    do did done does have has had yet soon later earlier yesterday minutes min mins sec secs
    second seconds moment moments hour hours while ago a while day days week weeks month months
    year years morning afternoon evening night long ages spell tomorrow late lately
    phone mobile phones laptop computer inbox messages message emails email texts
    i've we've you've they've ive weve youve theyve
""".split())

A_HOW_THE_TIME_WENT = frozenset("""
    mad crazy manic hectic mental busy rushed rush flat slammed swamped snowed frantic chaotic
    stressful stressed rough tough hard awful rubbish terrible horrible grim rotten bad long big
    heavy weird odd slow uphill nights shifts deadlines overtime full non-stop endless relentless
    nutty silly wild madder worse better fine ok
    work life things everything stuff week weeks month months year years day days time times
    while spell age ages morning night nights weekend weekdays lately recently overnight
    behind on ahead late over under through away out
""".split())

MANNERS_ONLY = frozenset("""
    sorry apologies apology apologise apologize bother bothering bothered ask asking asked
    question questions one more thing another pain nuisance hassle trouble troubling troubled
    pester pestering nag nagging
    keep keeping going on essay ramble rambling dump dumping moan moans moaning moaned
    interrupt interrupting
    time i im me you your my it this that just again so really very bit lot a an the and but also
    to for of about at with be being am is was had have been can could would please thanks thank
    ok okay well honestly tbh quick quickly stupid silly daft late slow early knowing know
    go goes going do did does
    """.split())

THANK_WORDS = frozenset(("thanks", "thank", "thankyou", "cheers", "ta", "appreciate",
                         "appreciated"))

THANKS_ONLY = MANNERS_ONLY | frozenset("""
    thats that's good know great brilliant brill perfect lovely helpful useful sorted right nice
    much many so much ace wonderful excellent amazing legend star lifesaver kind kindly
    for the advice help
    all everything then too will do
    """.split())

THANKS_THEN_SAID = (
    "Glad to hear it — and thanks for coming back to say so.",
    "Good. Thanks for letting me know.",
    "Pleased for you. Thanks for telling me how it went.",
    "That's good to hear. Thanks for saying so.",
)

THREAD = "thread"

CARE_THREAD = "care-thread"

PLAIN_WORDS = frozenset((
    "about", "after", "again", "anything", "before", "being", "could", "doing", "every",
    "going", "happen", "having", "should", "something", "still", "their", "there", "these",
    "thing", "things", "think", "those", "through", "today", "tonight", "would", "your",
    "yours", "mine", "with", "what", "when", "where", "which", "while", "whole", "leave",
))

ILL_BEFORE = frozenset(("feel", "feels", "feeling", "felt", "being", "been", "so", "very",
                        "really", "quite", "still", "get", "gets", "getting", "got", "fell",
                        "am", "im", "is", "was", "are", "looks", "look", "too", "seriously",
                        "badly", "terribly", "always", "often", "chronically"))

ILL_AFTER = frozenset(("for", "again", "all", "and", "today", "tonight", "lately", "since",
                       "this", "last", "week", "weeks", "day", "days", "month", "morning",
                       "at", "in", "on", "with", "from", "health", "enough", "yesterday"))

ILL_SAID_OF_A_BODY = frozenset(("am", "im", "is", "was", "are", "feel", "feels", "feeling", "felt",
                                "been", "being", "looks", "look", "get", "gets", "getting", "got",
                                "fell", "seriously", "badly", "terribly", "chronically", "often"))

ILL_WILL_VERBS = frozenset((
    "be", "have", "get", "let", "try", "call", "text", "ring", "phone", "see", "tell", "say",
    "give", "send", "check", "do", "go", "come", "take", "make", "bring", "put", "keep", "look",
    "ask", "email", "message", "book", "order", "pay", "pop", "head", "drive", "walk", "run",
    "start", "finish", "show", "wait", "find", "grab", "meet", "stay", "sit", "sort", "write",
    "add", "fix", "clean", "tidy", "wash", "buy", "sell", "need", "want", "drop", "pick",
    "leave", "turn", "sign", "carry", "chat", "speak", "read", "eat"))

AIM_HEADS = frozenset(("want", "wants", "wanting", "trying", "try", "need", "needs",
                       "hoping", "hope"))

AIM_NEGATORS = frozenset(("not", "dont", "doesnt", "didnt", "never", "no", "wont", "cant"))

AIM_FAILING = frozenset(("wont", "doesnt", "isnt", "nothing", "stuck", "nowhere", "stopped",
                         "hopeless"))

STATE_CUES = frozenset((
    "happy", "excited", "amazing", "proud", "delighted", "thrilled", "brilliant",
))

JUNK_CUES = frozenset(("rubbish", "crap", "crappy", "naff", "meh", "bleh", "poo"))

MOOD_BEFORE = frozenset((
    "is", "was", "were", "are", "am", "feel", "feels", "feeling", "felt", "seems", "seemed", "be", "been",
    "being", "so", "very", "really", "quite", "pretty", "totally", "absolutely", "bit",
    "such", "that", "this", "fairly", "properly"))

MOOD_AFTER = frozenset((
    "week", "weeks", "day", "days", "month", "morning", "afternoon", "evening", "night",
    "weekend", "year", "time", "start", "shift", "term", "few", "couple"))

A_MOOD_WITH_A_CATCH = {
    "fired": frozenset(("got", "get", "gets", "getting", "was", "were", "is", "are", "am", "been",
                        "being", "have", "has", "had", "ve", "i've", "we've", "they've")),
}

COPULA = frozenset(("is", "was", "were", "are", "am", "seems", "seemed", "be", "been", "being"))

ABOUT_THEM_BEFORE_COPULA = frozenset((
    "i", "im", "i'm", "ive", "i've", "me", "we", "we're", "were", "us", "myself", "everything",
    "things", "life", "it", "this", "today"))

RUMINATION_REPLIES = (
    "That sounds like it is still sitting with you. What is the part that keeps coming back?",
    "A worry at 2am is rarely the same shape as one in daylight. What actually happened?",
    "Going round it that many times is exhausting. Say it out to me — what keeps coming back?",
    "Fair enough — that kind of thing does not let go on its own. What is the bit you keep "
    "landing on?",
)

BODY_STATES = {
    "cold": frozenset(("cold", "freezing", "frozen", "chilly", "chilled", "perished",
                       "baltic", "icy",
                       "shivering", "shivery")),
    "hot": frozenset(("boiling", "hot", "roasting", "sweating", "sweaty",
                      "sweltering", "baking", "melting")),
    "hungry": frozenset(("hungry", "starving", "starved", "famished", "peckish",
                         "ravenous")),
    "thirsty": frozenset(("thirsty", "parched", "dehydrated")),
    "light_head": frozenset(("faint", "fainted", "fainting", "faintish", "woozy", "dizzy",
                             "giddy", "wobbly", "shaky", "lightheaded", "groggy")),
    "queasy": frozenset(("queasy", "queezy", "nauseous", "nauseated", "sickly", "bilious")),
    "bunged": frozenset(("bunged", "bungedup", "blockedup", "sniffly", "sniffles",
                         "sniffing", "croaky", "hoarse", "sneezing", "congested", "husky",
                         "snotty")),
    "clammy": frozenset(("clammy", "clamy", "clammyish", "coldsweat", "coldsweats")),
    "pale": frozenset(("pale", "pallid", "ashen", "grey", "gray", "greyish", "grayish",
                       "mottled", "blotchy", "washedout")),
    "puffy": frozenset(("puffy", "bloated", "swollen", "puffed", "puffing")),
    "spotty": frozenset(("spotty", "pimply", "acne", "brokenout")),
}

BODY_TAIL = frozenset(("today", "tonight", "now", "still", "again", "though", "honestly",
                       "already", "outside", "here", "actually", "really", "so", "very",
                       "absolutely", "bloody", "thanks"))

BODY_SITUATION = ("all the time", "all day", "all night", "all morning", "all afternoon",
                  "all evening", "all week", "all weekend", "in here", "in this house",
                  "in this weather", "at night", "at work", "in the night", "right through",
                  "to the bone", "through to the bone", "all day today", "all day yesterday",
                  "all night long")

BODY_PART_TAIL = frozenset(("", "today", "now", "still", "again", "already", "outside"))

BODY_PART_QUALIFIER = frozenset((
    "really", "so", "very", "proper", "properly", "absolutely", "completely", "totally",
    "always", "still", "bit", "little", "a", "dead", "stone", "bloody", "permanently",
    "freezing", "bitterly", "that", "quite", "pretty", "fairly", "completely"))

BODY_LEAD = frozenset(("so", "oh", "ah", "god", "honestly", "well", "and", "also", "tbh", "ok",
                       "okay", "literally", "seriously", "man", "ooh", "ugh", "yeah", "no"))

BODY_ALSO = frozenset(("tired", "knackered", "exhausted", "shattered", "grumpy", "sore",
                       "achy", "sweaty", "miserable", "worn", "wet", "hungry", "thirsty"))

BODY_COLD = (
    "Wrap up and get a hot drink in you - is the heating on where you are?",
    "Hot water bottle and something warm inside you. That beats waiting for the heating.",
    "Cold gets into everything. Is there a radiator you can sit next to?",
    "Another layer and something hot to drink. Is it the whole place, or just the room you "
    "are in?",
    "That is too cold to think straight in. Get the heating on and a jumper on top of that.",
)

BODY_HOT = (
    "Get a cold drink in you and some air moving - is there a window you can open?",
    "Cold water on your wrists and a bit of a draught is the quickest way down.",
    "That kind of heat is draining. Have you got somewhere cooler to be?",
    "Take it slowly in this, and get out of it for five minutes if you can.",
    "Too warm to think straight in. Open a window and put a cold drink in you.",
)

BODY_HUNGRY = (
    "Then go and eat something - what have you got in?",
    "That is your body asking. Something with protein in it holds you longer than a biscuit.",
    "Eat first and sort the rest out after. What is quickest to hand?",
    "You are running on empty there. Toast and an egg beats waiting for a proper meal.",
    "Go and get something now, even if it is small - a sandwich is enough to steady you.",
)

BODY_THIRSTY = (
    "Get a glass of water in you now - are you at home, or out?",
    "Thirsty means you are already behind. A full glass of water, not a sip.",
    "Water first, then whatever you were doing. Is there a tap handy?",
    "Have a proper drink of water and keep the glass next to you afterwards.",
)

BODY_LIGHT_HEAD = (
    "Sit down before anything else - did it come on when you stood up?",
    "Get sat down and have some water. Does it settle if you stay still for a minute?",
    "Take that slowly and hold on to something. Has it been creeping up on you, or was it "
    "sudden?",
    "Sit down and put your head down for a minute. If it keeps happening it is worth getting "
    "looked at.",
    "Have you eaten anything today? Low blood sugar does that - get something in you and "
    "sit down.",
)

BODY_QUEASY = (
    "Sit up rather than lie flat and sip water - is anything staying down?",
    "Plain and dry beats anything rich right now: toast, a bit of rice. When did it start?",
    "Go steady with small sips. Is it just queasy, or have you been sick?",
    "Fresh air and water, and nothing heavy for an hour or two. Does it come in waves?",
    "That is a rotten way to spend an evening. Is it something you ate, do you think?",
)

BODY_BUNGED = (
    "Something hot to drink and ten minutes of steam in the bathroom - is it a cold coming on?",
    "That is usually the cold starting in the nose and throat. Is it blocked, or running?",
    "Honey in hot water and rest your voice - how long has it been like that?",
    "Keep the fluids up and get an early night. Is it the nose, the throat, or both?",
    "A cold runs its week and there is no rushing it. Are you blocked up, or is it sore?",
)

BODY_CLAMMY = (
    "Clammy is a cold sweat rather than being too warm. Have you eaten anything today?",
    "Get sat down and have something sweet if you have not eaten in a while. Does it come with "
    "feeling dizzy?",
    "That is usually your body working hard at something: a fever coming on, low blood sugar or "
    "a shock. Is it just your hands, or all over?",
    "Wash your hands and sit somewhere cool for a minute - has this come on today, or is it "
    "something you get? Cool water and a sit-down is the thing that helps most.",
    "Cold and clammy with the room at a normal temperature is worth taking slowly. Sit down, "
    "have a drink, and if you feel faint or muddled with it, ring 111.",
)

BODY_PALE = (
    "Pale usually means something is going round, or you have not eaten. Have you had anything "
    "today?",
    "Sit down and have a drink, then something to eat - did it come on suddenly, or have you been "
    "like this a while?",
    "Grey and washed out with it is worth getting looked at rather than waiting. Is there any "
    "dizziness with it?",
    "Has anyone said you look pale, or does it just feel like it? Pale with a bug is normal "
    "enough; pale and dizzy is the one to get seen.",
    "Put your feet up for ten minutes and have something with sugar in it. If you are clammy or "
    "muddled with it, get seen today.",
)

BODY_PUFFY = (
    "Bloated usually settles if you go easy on salt and fizzy drinks for a day. Is it worse after "
    "eating?",
    "Puffy ankles and hands are worth getting checked if it is new. Is it just your stomach, or "
    "your ankles too?",
    "That is your body holding water. Drink more rather than less and cut the salt for a few days "
    "- does it ease overnight?",
    "Which bit is puffy? After a big meal and a late night it is nothing, but swelling that stays "
    "is worth a look.",
    "Go steady with salt and fizz and see if it settles by tomorrow. Is it tender with it?",
)

BODY_SPOTTY = (
    "Spotty skin is usually hormones and nothing to worry about. Is it your face, or your back "
    "too?",
    "Wash with a plain cleanser twice a day and keep your hands off them. How long has it been "
    "like that?",
    "A GP can help if they are sore or leaving marks - are you picking at them, or leaving them "
    "alone?",
    "That is common enough and it does pass. Does it bother you, or is someone else commenting "
    "on it?",
    "Spotty and itchy after a new cream or washing powder could be a reaction. Has anything "
    "changed lately?",
)

BODY_POOLS = {"cold": BODY_COLD, "hot": BODY_HOT, "hungry": BODY_HUNGRY,
              "thirsty": BODY_THIRSTY, "light_head": BODY_LIGHT_HEAD,
              "queasy": BODY_QUEASY, "bunged": BODY_BUNGED,
              "clammy": BODY_CLAMMY, "pale": BODY_PALE, "puffy": BODY_PUFFY,
              "spotty": BODY_SPOTTY}

_SUBJECT_AFTER_AM = frozenset("i we you they he she it there this that anyone anybody".split())

BAD_STRETCH = frozenset(("rubbish", "crap", "crappy", "rough", "tough", "hard", "awful",
                         "terrible", "horrible", "grim", "stressful", "hectic", "rotten", "naff",
                         "wearing", "draining"))

STRETCH_OF_TIME = frozenset(("week", "weeks", "day", "days", "month", "months", "weekend",
                             "morning", "afternoon", "evening", "night", "shift", "term", "year",
                             "today", "lately"))

HABIT_ACT = (r"(?:\w+ing|say|says|do|does|did|end|leave|put|finish|start|ask|text|snap|"
             r"interrupt|overthink|forget|argue|second|manage|seem|apologi[sz]e|check|cancel|"
             r"procrastinate|agree|accept|take|give|spend|buy|work|plan|tidy|worry|complain|"
             r"volunteer|pick|choose|eat|drink|run|scroll|compare|share|tell|hide|swallow|"
             r"push|hold|bite|clench|stay|go|turn|shut|withdraw|avoid|help|save|spend|arrive|"
             r"stick|wander)")

HABIT_REPLY = (
    "That sounds like a pattern rather than a one-off. What happens just before it?",
    "Habits like that are usually a trigger and a shortcut, not a lack of will. When does it "
    "bite most?",
    "How long has it been like that, and has anything ever made it better for a while?",
    "What have you tried so far? What did not work usually points at what would.",
    "Worth looking at what sets it off rather than trying harder at it. What tends to come "
    "just before?",
)

BAD_STRETCH_REPLIES = (
    "That sounds like a rough one. What's been the worst of it?",
    "Fair enough — that takes it out of you. What has been going on?",
    "Sorry. Do you want to tell me what has made it like that?",
    "That is a lot to hold at once. What has been the hardest part?",
)

COMFORT_SAID = frozenset(NEGATIVE + BAD_STRETCH_REPLIES + RUMINATION_REPLIES
                         + NO_DIRECTION_REPLY + NOT_ENOUGH_REPLY + LEFT_POOL)

HOUSE_VERB = frozenset(("take", "put", "turn", "switch", "fill", "lock", "open", "close",
                        "wash", "hoover", "tidy", "clean", "set", "feed", "walk", "bring"))

PAST_STATE_CUES = frozenset(("pregnant", "engaged"))

_WAS = frozenset(("was", "were", "been", "used"))

CROWD = frozenset(("everyone", "everybody", "everyones", "peoples", "others", "nobody"))

YOU_SUBJECTS = frozenset("i im ive id ill me myself we us".split())

ABOUT_WORDS = frozenset(("for", "of", "about"))

PERSON_WORDS = frozenset("me us we you my our myself ourselves".split())

A_BIRTHDAY_STILL_TO_COME = (
    "{who} turns {age} {when} — that's one to look forward to. Are you doing anything for it?",
    "{age} {when} — a good one to have ahead. What are you thinking of doing?",
    "Lovely — {who} at {age} {when}. Will you mark it somehow?",
    "That's nice to have coming up. {age} {when} is worth making a fuss of — anything planned?",
)

ROUTINE = (
    "Pick the one thing that would make the day easier and give it a fixed slot; everything "
    "else can move around it. What is the thing you keep not getting to?",
    "Make it small enough that a bad day cannot beat it — two minutes, the same trigger each "
    "time — and add to it once it holds. What would it look like on your worst day?",
    "Work back from when you have to leave: what time to get up, what has to happen before "
    "that, and what can be dropped. Where does the morning usually go wrong?",
    "Write tomorrow down tonight — three things, one of them small — and do the smallest "
    "first, before the day fills up. Where does the time usually go?",
)

TOO_MUCH = (
    "Then something has to come off the list. Which of it would actually go wrong if it waited "
    "a week?",
    "That is more than anyone can hold in their head — get it out of your head and onto paper, "
    "then mark the two things that are really due. What is on the list?",
    "When it is this much, the useful question is what to drop rather than how to fit it in. "
    "What is the one thing that cannot slip?",
)

ROUTINE_WORDS = frozenset((
    "routine", "routines", "habit", "habits", "organised", "organized", "procrastinating",
    "discipline", "productive", "overwhelmed", "drowning", "swamped",
))

ROUTINE_PHRASES = (
    "get organised", "get organized", "get my act together", "stick to it", "stick at it",
    "stick with it", "always late", "never on time", "get up earlier", "sort out my mornings",
    "sort my mornings", "sort out my days", "to do list", "time management",
    "keep on top of", "keep putting things off", "put things off", "fall behind", "get behind",
    "no time in the morning", "no time in the day", "never enough time in the morning",
    "rubbish at mornings", "useless at mornings", "not a morning person", "bad at getting up",
    "cant get going in the morning", "mornings are a struggle", "dread mornings",
    "late for everything", "late to things", "be on time",
)

TOO_MUCH_PHRASES = ("too much on", "spread too thin", "too many things", "so much to do",
                    "juggle", "juggling", "overloaded", "stretched thin",
                    "where to start", "where to begin")

_START_ASK = ("where to start", "where to begin")

ROUTINE_NOT = frozenset((
    "baby", "babies", "newborn", "toddler", "toddlers", "kid", "kids", "child", "children",
    "nursery", "teen", "teens", "teenager", "teenagers", "school run",
    "son", "daughter", "dog", "cat", "puppy", "kitten", "pup",
    "shifts", "shift", "hospital", "wing",
    "money", "bills", "bill", "tax", "taxes", "budget", "accounts", "invoice", "invoices",
    "payments", "debts", "debt", "rent", "mortgage", "loan", "loans", "insurance", "pension",
    "wages", "salary", "overdraft", "fines", "cook", "cooking", "dinner", "tea", "meals",
    "meal",
))

BEHIND_ON_MONEY = frozenset(("late", "behind", "overdue", "missed", "miss", "arrears", "skint",
                             "broke"))

_NO_DAY_OF_THEIR_OWN = ("died", "dead", "passed away", "passed on", "put down", "put to sleep",
                        "buried", "funeral", "cremation", "euthanised", "lost")

_DAY_WORDS = frozenset((
    "morning", "mornings", "day", "days", "evening", "evenings", "night", "nights", "week",
    "weeks", "weekend", "weekends", "time", "times", "work", "shift", "shifts", "today",
    "tomorrow", "life", "self", "routine", "routines", "everything", "anything", "nothing",
    "things", "thing", "moment", "minute", "minutes", "hour", "hours", "rest", "whole",
))

IMPERATIVE = frozenset("""give suggest recommend tell show make write find help list name pick
    choose plan""".split())

PUNT = ("a search should sort you out", "quick search online", "i'd rather not guess",
        "that's beyond what i know well", "searching for it will turn up")

FRAME_WORDS = frozenset(("i", "meant", "mean", "said", "say", "sorry", "no", "not", "wait",
                         "oops", "scratch", "that", "actually", "rather", "than", "or"))

SOMEBODY_HURT = (
    "God, that's awful. Is {who} alright?",
    "That's bad news. How is {who} now?",
    "I'm sorry. Is {who} alright?",
    "Christ. How is {who} doing?",
    "That's a horrible thing to hear. Is {who} okay?",
)

A_REST_OF_A_GOOD_DAY = (
    "That fits the day you have had. Good ones are worth saying out loud.",
    "The rest of a good day, then. Hold on to that one.",
    "Lovely. Those are the days that stick.",
    "That is a nice thing to have in a week. Enjoy the rest of it.",
)

A_REST_OF_A_HARD_DAY = (
    "That is the rest of a hard day, not the whole of it. Let the evening be small.",
    "Long one on top of a long one. Something warm to eat and an early night.",
    "Days like that pile up. You have done the day, so put your feet up now.",
    "That sounds like a full day on top of a hard one. Nothing else needs doing tonight.",
)

LOW_DAY_REPLIES = (
    "That sounds like a day to get through rather than enjoy. What made it that way?",
    "Sorry - that is a heavy one to carry. What has been the worst part of it?",
    "Long days like that take it out of you. Do you want to talk it through, or would you rather "
    "think about something else for a bit?",
    "That is a rough one. Is it the kind that lifts in a day or two, or one that has been "
    "building?",
    "Ugh. What happened?",
)

A_THING_THEY_REGRET = (
    "You don't have to dress it up for me. What happened?",
    "That's the kind of thing that sits on you. Do you want to talk it through?",
    "Whatever it was, I'd rather hear it than not. What happened?",
    "That sounds like it's been weighing on you. What happened?",
)
A_BETRAYAL = (
    "That's a rotten thing to find out. What do you know so far, and what is still guesswork?",
    "Ugh. That's a lot to take in in one go. Say it as it came.",
    "That hurts, and it is not on you. What happened?",
    "Rotten news, and I'm sorry. Say it out loud if you want, or we can talk about something else "
    "for a bit.",
    "That changes how the whole thing looks, doesn't it. I'm here.",
    "Awful. You do not have to work out what to do about it today.",
    "That's the kind of thing that sits on your chest. Tell me what happened.",
)

A_CARE_HOME = (
    "It takes a while to feel like home, for everyone. What is it like when you visit?",
    "How is {they} finding it there? The first weeks are the strangest for most people.",
    "That is a big change for {them}, and for you. How is {they} settling in?",
)
A_CARE_HOME_MOVED = (
    "That is a big change for {them}, and for you. How is {they} settling in?",
    "That is a hard thing to have had to decide. How are you doing with it?",
    "It takes a while for everyone. How has {they} been since the move?",
)
A_CARE_HOME_VISITING = (
    "The visiting is the part that counts, and it is tiring too. What do you usually do together "
    "when you are there?",
    "A visit is a lot of work before and after it. How often do you get over there?",
)
A_CARE_HOME_GUILT = (
    "Guilt comes with this even when the decision was the right one, and it is not evidence of "
    "anything. What does a visit look like these days?",
    "That guilt is very common and it does not mean you did the wrong thing. Have you got anyone "
    "to say all this to?",
)
A_CARE_HOME_BRING = (
    "The things that make the room theirs: photos in a frame, a favourite blanket or cardigan, a "
    "radio or their own mug. Take one thing a visit rather than a car load, and check what the "
    "room has room for first.",
    "Ask what {they} misses from home - a particular biscuit, the paper, a cushion off the old "
    "sofa - and take one of those, plus something to do together. The visits matter more than "
    "the things.",
)

A_SMALL_DAY = (
    "Sounds alright. Anything good in it?",
    "Nice one. How did the rest of it go?",
    "Good to hear. What was the best bit?",
    "How was it, overall?",
)

A_NEWS_OF_WEATHER = (
    "Then the local forecast is the thing that knows, not me: it gives the hour it lands and how "
    "hard, and anything loose outside is worth sorting before then - the bins in, the panel that "
    "already leans screwed back, the trampoline turned over.",
    "Worth an hour on the loose things before it gets here: the fence panel, the bin store, the "
    "pot that goes over anyway. The local forecast has the gusts, and that is the number that "
    "says whether the hour is worth spending.",
    "The local forecast will tell you the gusts and when; what it cannot tell you is what of yours "
    "is already loose. Walk the garden once and fix that, and the rest is out of your hands.",
)
A_NEWS_OF_SOMETHING_ELSE = (
    "Then whoever put it out has the detail, and the detail is the part that matters - what it "
    "covers, from when, and what you do about it. It is usually one line further down than the "
    "headline.",
    "Worth reading it at the source rather than the report of it: a closure or a change is "
    "usually a date, an area and a form, and the headline leaves all three out.",
    "The body that said it will have the version with the dates in it, and the question worth "
    "asking is whether it changes anything of yours - a journey, a bin day, a plan.",
)

A_THING_TAKEN = (
    "That's rotten. Is there anything that has to happen tonight - a lock, a card to stop?",
    "Sorry - that is a horrible thing to have happen. Was it insured, or is this coming out of "
    "your pocket?",
    "That's a blow. Did they get anything else, or just the one thing?",
    "That's low. Where was it when it went?",
    "That's rotten, and it is worth reporting today while it is fresh - the reference number is "
    "what the insurer and the bank both ask for. Say the word and I'll walk you through the "
    "claim step by step.",
)

A_BAD_TIME_TOLD = (
    "Sounds like a rough one. What happened?",
    "Ugh, that is a shame. Do you want to get into it?",
    "That is a nuisance. Is there anything that would help?",
    "How are you doing with it?",
    "Sorry to hear it. What would make today easier?",
)

A_NAME_STORY = (
    "{names}. What is the story behind that name?",
    "{names} - good to know. Where did that come from?",
    "{names}. Who picked it?",
)


A_NAMED_AFTER = (
    "Named after {who}. What {are} {they} like?",
    "Named after {who}. Does the name fit, or is it a big one to carry?",
    "Named after {who} - I like that. Where did the idea come from?",
)
A_NAMED_AFTER_THEM = (
    "Named after you - that is a compliment. Whose idea was it?",
    "Named after you. Does the name fit, or is it a big one to carry?",
    "Named after you - I like that. What was the thinking there?",
)


A_NAME_TOLD = (
    "{names}. What {are} {they} like?",
    "{names} - good to know. What {are} {they} like?",
    "{names}. Tell me about {them}.",
    "{names}. What should I know about {them}?",
)


A_PLAN_THAT_FELL_THROUGH = (
    "That's a shame. Is it off altogether, or moved?",
    "Gutted. What got in the way?",
    "Ah no. What stopped it?",
    "Sorry to hear it. Can it still happen?",
    "That is a shame. Do you get another go at it?",
)

A_STATE_NOW = (
    "How is that going?",
    "How long has that been the case?",
    "Does that suit you, or would you change it?",
)
A_STATE_PAST = (
    "How did that go?",
    "How do you look back on it?",
    "What do you make of it now?",
)

A_DAY_ASKED_PLAIN = (
    "How did that go, overall?",
    "What was it like?",
    "How did you find it?",
)


A_THING_CAME_OUT_WRONG = (
    "That's a shame. What went wrong with it?",
    "Ah no. Can it be rescued, or is it a start again?",
    "Annoying when that happens. What was it you made?",
    "Gutted. Had you made it before?",
    "That is a nuisance. Do you know what did it?",
)

_THING_DONE_LINES = frozenset(A_THING_DONE + A_THING_GONE + A_THING_ON + A_THING_SEEN_TO
                              + A_THING_BOUGHT)

DISH_PARTICIPLE = frozenset(("packed", "baked", "fried", "roasted", "mashed", "toasted",
                             "scrambled", "boiled", "poached", "grilled", "stuffed", "pickled"))

DISH_DETERMINER = frozenset(("a", "an", "the", "my", "our", "your", "his", "her", "their", "its",
                             "this", "that", "these", "those", "some", "any", "all", "each", "one",
                             "two", "three", "every", "another", "it", "them", "everything"))


FORECAST = re.compile(
    r"\bwill\s+(?:it|that|this|they|he|she|i|we|my\s+\w+|the\s+\w+)\b"
    r"[^?.!]{0,40}?\b(?:get\s+better|get\s+worse|be\s+(?:ok|okay|all\s+right|alright|fine)|\s*"
    r"come\s+back|come\s+right|come\s+down|go\s+(?:away|down)|recover|heal|clear\s+up|ease|\s*"
    r"settle|pass|stop|wear\s+off|sort\s+(?:itself|themselves)\s+out|\s*"
    r"pull\s+through|make\s+it)\b"
    r"|\b(?:is|are|will)\s+(?:he|she|it|that|this|they|my\s+\w+)\b[^?.!]{0,30}?"
    r"\b(?:going\s+to|gonna)\s+(?:be\b|get\s+(?:better|worse)|heal|recover|\s*"
    r"clear\s+up|come\s+(?:back|right)|settle|ease|\s*"
    r"make\s+it|pull\s+through)\b"
    r"|\bwill\s+(?:he|she|they|my\s+\w+|the\s+\w+)\b[^?.!]{0,20}?\bbe\s+"
    r"(?:out|home|back|walking|mobile|up\s+and\s+about|better|on\s+the\s+mend)\b\s*"
    r"(?:by|before|for|on|in\s+time\s+for|this|next)\b")
FORECAST_PERMISSION = re.compile(
    r"\bwill\s+(?:it|that|this)\s+be\s+(?:ok|okay|fine|alright|all\s+right)\s+"
    r"(?:if|to|with|until|till|overnight)\b")
FORECAST_DURATION = re.compile(r"\bhow\s+long\b")
FORECAST_I_ASK = re.compile(r"\b(?:will|am)\s+i\b")
FORECAST_RELATION = re.compile(
    r"\b(?:my|our)\s+(dad|father|mum|mom|mother|nan|nana|gran|granny|grandma|grandad|grandpa|\s*"
    r"husband|"
    r"wife|partner|boyfriend|girlfriend|son|daughter|brother|sister|baby|boy|girl|friend|mate|"
    r"dog|cat|pup|puppy|kitten|rabbit|hamster|horse|pony|bird|parrot|guinea|gerbil|ferret|fish)"
    r"\b")
FORECAST_HE_SHE = re.compile(r"\b(?:he|she|him|her|his)\b")
FORECAST_STRUGGLE = re.compile(
    r"\b(?:struggl\w*|cop(?:e|ing)|depress\w*|anxi\w*|upset|cry(?:ing)?|tears|unhapp\w*|"
    r"miserable|lonely|isolated|withdrawn|overwhelm\w*|burn(?:t|ed)?\s+out|breaking\s+down|"
    r"hard\s+time|going\s+through\s+(?:it|a\s+lot)|feel(?:ing)?\s+(?:low|flat|down)|"
    r"lost\s+my\s+job|redundant|sacked|"
    r"not\s+(?:her|him)self|self\s*harm|suicidal|dark\s+place)\b")
FORECAST_ILL = frozenset("""
fall falls fell hospital ward operation op surgery treatment diagnosed diagnosis pneumonia
infection sepsis chemo chemotherapy stroke fracture broken stitches plaster cast scan consultant
physio physiotherapy terminal prognosis recovering recovery intensive icu a&e casualty accident
accidents crash crashed collision injured injury hurt ambulance paramedic paramedics
""".split())
FORECAST_PERSON = (
    "Nobody can promise that, and I won't guess about another person's health. What it comes "
    "down to is the direction - better than yesterday, or not - and the ones looking after {who} "
    "can see that. Ask them what they are watching for, and what the next few days should look "
    "like.",
    "That is the doctors' call, not mine - I can't see {who}. What is in your hands is asking "
    "them straight how it compares with yesterday and what would count as a setback; tell me "
    "what they say and I'll help you think it through.",
    "I can't promise that, and it would not be fair to. What the people treating {who} can tell "
    "you is the useful part: what is going well, what would worry them, and what the next few "
    "days should hold.",
)
FORECAST_SELF = (
    "No one can promise that from here - mine would be a guess about your body, and that is "
    "not a guess worth having. What decides it is the direction: if it is easier this week than "
    "last, keep going as you are; if it is no better in a couple of weeks, or it gets worse, "
    "111 will say whether it needs looking at today.",
    "Probably, given time - and nobody can say for certain from here. The thing to watch is "
    "whether it keeps improving; if it stalls, or it starts to get worse, that is one for your "
    "GP rather than wait-and-see.",
    "I can't call that from here, and a guess about a body is the last thing you need. Bodies "
    "mend at their own speed, so the question worth asking is whether it is improving week by "
    "week; your GP can say what to expect and when to come back - take the same description you "
    "gave me.",
)
FORECAST_SOMEONE_STRUGGLING = (
    "I can't promise that, and I won't pretend to - nobody can say how another person's hard "
    "patch ends. Staying in touch this week is the part you can do, and if it gets darker than "
    "that, their GP is the one who can step in.",
    "Nobody can call that from here, and a forecast would be a guess. Keep asking how they "
    "really are - and if there's any talk of not wanting to be here, that is a doctor's call "
    "the same day, not something to wait out.",
)
FORECAST_SELF_STRUGGLING = (
    "I can't promise that, and a forecast would be a guess. What does move it is this week: "
    "keep the ordinary things going - sleep, food, daylight, one person who knows how it really "
    "is - and if it is no better in a fortnight, take it to your GP.",
    "Nobody can call that from here, and I won't pretend to. Tell one person the true version "
    "rather than the short one, keep the week as ordinary as you can, and if it gets darker than "
    "that, your GP is the one who can step in.",
)
FORECAST_PET = (
    "Only the vet can say that - I can't examine {who} from here. What the desk will ask is the "
    "useful part: is {who} eating and drinking, as lively as usual, and has anything been kept "
    "down? Ring with that and ask whether to bring {who} in tonight.",
    "I can't call that from here, and the vet has to see {who}. What decides it is usually how "
    "{who} is in themselves - eating, drinking, energy - so note that down and ring the desk; "
    "they will say whether it can wait until the morning.",
    "Nobody can say that without seeing {who}, and the vet can. Take what you've just told me, "
    "add whether {who} is eating and drinking, ask what would mean bringing {who} in, and go "
    "with what they say.",
)
FORECAST_AFTER_SAFETY = (
    "I can't say how it will go, and nobody can from here. What you can go on is the direction - "
    "steadier hour by hour, or not - and the ones treating {who} can see it: keep doing what "
    "they told you, and ask them what to expect and what would worry them.",
    "That is for the people looking after {who} to answer, not me - they can see what I can't. "
    "Keep doing exactly what they told you, and ask them straight what the next few days should "
    "look like; I'm here for the rest of it.",
)


FORECAST_POOLS = (FORECAST_SELF, FORECAST_PERSON, FORECAST_SOMEONE_STRUGGLING, FORECAST_PET,
                  FORECAST_AFTER_SAFETY)


FORECAST_BODY_WORDS = BODY_PARTS | SYMPTOM_WORDS | HEALTH_WORDS | FORECAST_ILL

BODY_WORD_FOR_A_THING = re.compile(
    r"\b(?:back|shoulders?|arms?|foot|feet|head|chest|hips?|ribs?|spine|belly|knees?|neck|"
    r"hands?|legs?|elbows?|waist)\s+(?:doors?|gardens?|yards?|walls?|rooms?|gates?|fences?|"
    r"windows?|lawn|beds?|paths?|steps?|porch|seats?|lights?|lanes?|roads?|alleys?|shed|deck|"
    r"patio|fields?|cars?|wheels?|sides?|covers?|pages?|pockets?|boards?|racks?|rest|cushions?|"
    r"chairs?|tables?|freezer|drawers?|cupboards?|wardrobes?|stairs?|staircase|lines?|notes?|"
    r"rows?|bands?|straps?|ties?|muffs?|warmers?|of\s+the\s+(?:stairs|bed|sofa|room|house|"
    r"boat|car|garden))\b")

FORECAST_OFF_THEIR_FOOD = re.compile(
    r"\b(?:stopped|stopping|not|no\s+longer|wont|won'?t|isnt|isn'?t|keeps?)\s+eating\b"
    r"|\boff\s+(?:her|his|their)\s+food\b|\b(?:lost|loosing|losing)\s+(?:her|his|their)\s+"
    r"appetite\b")

FORECAST_PET_HARM = re.compile(
    r"\b(?:drank|drink|swallow(?:ed|s|ing)?|ate|eaten|eats?|poison\w*|toxic|lil(?:y|ies)|"
    r"chocolate|grapes?|raisins?|onions?|xylitol|antifreeze|bleach|hit\s+by|ran\s+over|"
    r"run\s+over|fell|fallen|limp(?:ing)?|lame|collapsed|fitting|seizures?|wheez\w*|"
    r"vomit\w*|vomited|bleeding|blood|in\s+pain|shaking|not\s+eating|stopped\s+eating|"
    r"off\s+(?:her|his|their)\s+food|hurt)\b")

FORECAST_A_FALL = re.compile(
    r"\b(?:came|come|cames|fell|fallen|falling|was|were|got|been)\s+off\s+(?:his|her|their|the|"
    r"a|my)\s+(?:bike|motorbike|horse|ladder|roof|scooter|skateboard|bicycle|moped|quad)\b")




DITHER_SUBJECT = re.compile(
    r"\b(?:"
    r"whether to (?!laugh|cry|scream|shout|smile)\w+"
    r"|if i (?:should|shall) \w+"
    r"|if i can (?:afford|manage|keep|take|handle|fit|cope|swing)\b"
    r"|between \w+"
    r"|which \w+ to (?:pick|choose|take|try|go)"
    r"|what to do (?:about|with|next|now)\b"
    r"|(?:decid(?:e|ed|ing)|think(?:ing)?|thought|wonder(?:ing)?|consider(?:ing)?|want)"
    r"s?\s+(?:about\s+|of\s+)?(?:whether\s+)?to "
    r"(?:go|take|move|stay|leave|quit|apply|accept|buy|sell)\b"
    r"|i (?:want|wanted|dont want) to (?:go|take|move|stay|leave|quit|apply|accept|buy|sell)\b"
    r")")


PASSED_OUT = re.compile(
    r"\b(i|im|he|hes|she|shes|we|were|they|theyre|"
    r"(?:my|our|the)\s+(?:(?:little|young|eldest|oldest|older|grown\s?up|poor|baby|new)\s+)?"
    + PASSED_OUT_PERSON + r")\b(?:\s+\w+){0,4}\s+"
    r"(?:passed out|collapsed|fainted|blacked out|keeled over|had a seizure"
    r"|passing out|collapsing|fainting|blacking out|keeling over|having a seizure"
    r"|collapses|faints|passes out|blacks out"
    r"|keeps? (?:passing out|collapsing|fainting|blacking out|going down)"
    r"|pass(?:ing|ed)? out (?:sometimes|a lot|often|now and then|every so often|a few times)"
    r"|goes down\b(?=\s*(?:all|suddenly|on|in (?:the|a)\s|while|when|at\b))"
    r"|went down(?!\s*(?:to|the|stairs|steps|hill|road|lane|street|with|in|by|for))"
    r"|(?:(?:about|going|gonna)\s+to|might|may)\s+(?:pass\s+out|faint|black\s+out|collapse|"
    r"go\s+down))\b")


PASSING_OUT_A_THING = re.compile(
    r"\bpass(?:ing|ed|es)?\s+out\s+(?:(?:the|a|an|some|those|these|our|their|his|her|my|its)\s+"
    r"(?!(?:bit|little|lot|few|couple|while|moment|second|seconds|minute|minutes|mins|hour|hours|"
    r"day|days|night|nights|time|times|again|now|too|other|next|thing|door|window|gate|back|"
    r"way|rest|floor|sofa|chair|bed|bus|train)\b)\w+"
    r"|(?!(?:afterwards?|after|before|later|once|twice|thrice|again|sometimes|always|often|"
    r"repeatedly|nowadays|every|most|these|days|nights|weeks|months|years)\b)[a-z]{2,}s\b)")


BARE_PICK_LOST = re.compile(
    r"^\s*(?:(?:so|and|but|ok|okay|well|then|just|hey|hi|right|anyway|anyways|oh|hmm|yeah|"
    r"yes|alright|honestly|god|christ|ugh|tbh|seriously|you\s+know)[\s,]+)*"
    r"(?:i\s+)?(?:really\s+|honestly\s+|genuinely\s+|actually\s+|still\s+|simply\s+|"
    r"just\s+)*"
    r"(?:"
    r"(?:do\s+not|don'?t|dont)\s+(?:even\s+)?know"
    r"|dunno"
    r"|(?:have|ve|got|i'?ve)\s+(?:absolutely\s+)?no\s+(?:idea|clue)"
    r"|(?:have\s+)?no\s+(?:idea|clue)"
    r"|(?:i\s+am\s+|i'?m\s+)?not\s+(?:really\s+|too\s+)?sure"
    r")"
    r"\s+what\s+(?:to\s+do|i\s+(?:should|can|could|might)\s+do)\b"
    r"(?:\s+(?:now|next|first|today|tonight|tomorrow|instead|else|at\s+all|anymore|"
    r"any\s+more|about\s+(?:it|this|that)|with\s+(?:it|this|that|them)))?\s*\.?\s*$", re.I)


NAMED_BODIES = (
    ("citizens advice", "Citizens Advice"), ("national debtline", "National Debtline"),
    ("health visitor", "Your health visitor"), ("school office", "The school office"),
    ("head of year", "The head of year"), ("gas safe", "A Gas Safe engineer"),
    ("letting agent", "The letting agent"), ("trading standards", "Trading standards"),
    ("environmental health", "The council's environmental health team"),
    ("the council", "The council"), ("your council", "The council"),
    ("the vet", "Your vet"), ("a vet", "Your vet"), ("pharmacist", "A pharmacist"),
    ("111", "111"), ("a&e", "A&E"), ("your gp", "Your GP"), ("the gp", "Your GP"),
    ("dentist", "A dentist"), ("landlord", "Your landlord"), ("the school", "The school"),
    ("solicitor", "A solicitor"), ("the bank", "Your bank"), ("your bank", "Your bank"),
    ("ombudsman", "The ombudsman"), ("plumber", "A plumber"), ("electrician", "An electrician"),
    ("roofer", "A roofer"), ("the police", "The police"), ("registrar", "The register office"),
    ("dwp", "The DWP"), ("hmrc", "HMRC"), ("stepchange", "StepChange"),
    ("samaritans", "Samaritans"), ("your insurer", "Your insurer"), ("acas", "ACAS"),
    ("your union", "Your union"), ("hr", "HR"), ("the midwife", "Your midwife"),
)


PRIVACY_ASK = re.compile(
    r"\b(?:keep|keeps|keeping|store|stores|storing|save|saves|saving|record|records|recording|"
    r"log|logs|logging|share|shares|sharing|sell|sells|selling)\s+"
    r"(?:on\s+|out\s+|around\s+|off\s+|away\s+)?"
    r"(?:what\s+i\s+(?:said|say|tell|type|typed|write|wrote)|what\s+we\s+(?:said|talk|"
    r"discussed)|my\s+(?:messages?|data|details|information|info|chats?|records?|"
    r"conversations?)|our\s+(?:chats?|conversations?)|this\s+(?:chats?|conversations?)|"
    r"the\s+(?:chats?|conversations?))\b"
    r"|\b(?:can|could|will|would|do|does|did)\s+(?:anyone|anybody|someone|somebody|people|"
    r"other\s+people|people\s+else|anyone\s+else|everyone|staff)\s+(?:else\s+)?"
    r"(?:see|read|hear|get|access|look\s+at)\s+(?:this|what|my|our|the)\b"
    r"|\b(?:do|does|did|would|will|can|could)\s+(?:you|u)\s+(?:ever\s+)?"
    r"(?:tell|show|share|give|send|hand|pass|forward)\s+"
    r"(?:anyone|anybody|someone|somebody|people|others|a\s+third\s+party)\b"
    r"|\bwho\s+(?:(?:can|could|else\s+can|else\s+could)\s+(?:see|read|access)|sees|reads|"
    r"accesses)\s+"
    r"(?:this(?:\s+(?:chat|conversation|thread))?(?=\s*[?.!]*\s*$)|"
    r"my\s+(?:messages?|data|chats?)\b|what\s+i\s+(?:say|type|write)\b)"
    r"|\bis\s+(?:this|it|what\s+i\s+say|what\s+i\s+tell\s+you)(?:\s+(?:chat|conversation|"
    r"page|app|thing|site))?\s+(?:private|confidential|"
    r"secure|saved|recorded|stored)\b"
    r"|\bare\s+(?:my|our|these)\s+(?:messages?|data|details|chats?|records?|words)\s+"
    r"(?:private|safe|secure|confidential|shared|stored|saved|recorded|logged)\b"
    r"|\b(?:does|do|did|is|was)\s+(?:this|it|that|everything\s+i\s+say|what\s+i\s+say)\s+"
    r"(?:get\s+|being\s+|ever\s+get\s+)?(?:shared|stored|saved|recorded|logged|kept|seen|"
    r"read|passed)\b"
    r"|\bare\s+(?:you|u)\s+(?:keeping|recording|saving|storing|logging)\s+"
    r"(?:this|what\s+i|my|our|the\s+(?:chat|conversation))\b"
    r"|\b(?:do|does|did|will|would|can|could)\s+(?:you|u)\s+(?:ever\s+)?"
    r"(?:keep|save|log|record|store)\s+(?:a\s+|any\s+)?"
    r"(?:record|log|copy|note|transcript|file|history)\s+of\b"
    r"|\b(?:do|does|did|would|will|can|could)\s+(?:you|u)\s+(?:ever\s+)?"
    r"(?:pass|send|hand|give|forward|share)\s+(?:this|that|it|what\s+i\s+say)\s+"
    r"(?:on|along|around|off|over)?\s*(?:to|for)\s+"
    r"(?:anyone|anybody|someone|somebody|people|others|a\s+third\s+party)\b"
    r"|\bprivacy\s+(?:here|on\s+this|in\s+this|with\s+you|at\s+all)\b"
    r"|\bwhat\s+(?:are|do)\s+(?:you|u)\s+(?:(?:do|doing)\s+)?(?:with|using)\s+"
    r"(?:(?:my|our)\s+(?:data|details|information|info|messages|words)|"
    r"what\s+i\s+(?:tell|say|type|write))\b", re.I)


NOT_WHAT_I_SAID = re.compile(
    r"\b(?:keep|store|save|record|log|share|sell|pass)\w*\s+(?:me\s+|us\s+)?(?:the\s+|a\s+|an\s+|"
    r"my\s+|our\s+)?(?:kitchen|cat|dog|plants?|receipts?|leftovers?|food|milk|bread|eggs?|"
    r"cheese|wine|beer|keys?|car|bike|house|flat|money|savings|cash|password|photos?|pictures?|"
    r"files?|documents?|sheet|table|bill|bills|tickets?|seats?|room|garage|garden|washing|"
    r"clothes|coat|bag|phone|number|address|email|weight|diary|journal|notes)\b"
    r"|\bprivate\s+(?:rented|rent|rental|landlord|landlords|sale|sector|school|schools|hospital|"
    r"hospitals|treatment|health|healthcare|health\s?care|medical|insurance|pension|parking|road|"
    r"land|garden|tuition|tutor|"
    r"lessons?|detective|investigator|eye|clinic|care|nursery|swimming|coach|hire|contract|"
    r"members?|club|firm|company|jet|plane|island|beach)\b"
    r"|\bshared\s+(?:ownership|owner|equity|driveway|garden|house|home|flat|room|kitchen|"
    r"bathroom|car|bike|account|login|costs?|bills?|custody|care|space|office)\b", re.I)


PRIVACY_SHAPES = re.compile(
    r"\b(?:is|are|was)\s+(?:this|the|our)\s+(?:a\s+|an\s+)?(?:private|confidential|secure)\s+"
    r"(?:chat|conversation|call|line|session|thread)\b"
    r"|\b(?:is|are|was|will|would)\s+(?:this|our|the)\s+(?:chat|conversation|call|line|"
    r"session|thread)\s+(?:going\s+to\s+)?(?:be\s+|stay\s+|stays\s+|get\s+|gets\s+)?"
    r"(?:private|confidential|secure|saved|recorded|stored|logged|kept|seen|read|shared)\b"
    r"|\bwill\s+(?:this|it)\s+(?:be|stay|get)\s+(?:private|confidential|recorded|saved|"
    r"stored|logged|kept)\b"
    r"|\bis\s+(?:this|it)\s+going\s+to\s+(?:be\s+|stay\s+|get\s+)?(?:private|confidential|"
    r"recorded|saved|stored|logged|kept)\b"
    r"|\b(?:do|does|will|would|are|can|could)\s+(?:you|u)\s+(?:be\s+)?"
    r"(?:keep|keeping|save|saving|record|recording|store|storing|log|logging)\s+"
    r"(?:this|it|what\s+i\s+say)(?=\s*[?.!]*\s*$)"
    r"|\bwho\s+(?:sees|reads|hears|can\s+see|can\s+read|can\s+access)\s+"
    r"this(?:\s+(?:chat|conversation|thread))?(?=\s*[?.!]*\s*$)"
    r"|\b(?:is|are)\s+(?:my|our)\s+(?:data|details|info|information|messages?|words)\s+"
    r"(?:private|confidential)\b"
    r"|\b(?:is|are)\s+(?:my|our)\s+(?:data|details|info|information)\s+"
    r"(?:safe|secure)(?:\s+(?:with|on|in)\s+(?:you|here|this\s+chat)\b)?(?=\s*[?.!]*\s*$)"
    r"|\b(?:is|are)\s+(?:my|our)\s+(?:data|details|info|information|messages?|words)\s+"
    r"(?:safe|secure)\s+(?:with\s+(?:you|u)|here)\b"
    r"|\bwhat\s+(?:happens|happened|will\s+happen|would\s+happen)\s+to\s+"
    r"(?:what\s+i\s+(?:say|said|tell|type|write|wrote)\b"
    r"|my\s+(?:messages?|data|words|details|information|info|chats?)\b|our\s+(?:chat|"
    r"conversation)\b)(?=\s*[?.!]*\s*$)", re.I)


LIVE_ASK = (
    r"(?:times|timetables?|schedules?|numbers?|phone|telephone|address|postcode|postcodes?|"
    r"prices?|costs?|fares?|deals?|offers?|reviews?|ratings?|scores?|results?|news|"
    r"flights?|trains?|buses?|coaches|tickets?|availability|stock|opening\s+hours|"
    r"weather|forecast|vacanc(?:y|ies)|listings?|status|delays?|traffic|menu|"
    r"lead\s+times?|deadlines?|exchange\s+rates?)")

ONLINE_ASK = re.compile(
    r"\b(?:can|could|do|does|are|is|have)\s+(?:you|u)\s+(?:[a-z]+\s+){0,3}?"
    r"(?:browse|search|google|look[\s-]+(?:things|stuff|it|that|them)?\s*up|check|access|reach|"
    r"connect(?:ed)?|go|get)\s*(?:the\s+|a\s+)?(?:internet|web|online|net|google|sites?|"
    r"websites?|pages?)\b"
    r"|\b(?:can|could|do|does|are|is|have)\s+(?:you|u)\s+(?:[a-z]+\s+){0,3}?"
    r"(?:online|connected|internet|web|internet\s+access)\b"
    r"|\bdo\s+(?:you|u)\s+have\s+(?:[a-z]+\s+){0,2}?(?:access|internet|wifi)\b"
    r"|\bdo\s+(?:you|u)\s+have\s+(?:[a-z]+\s+){0,2}?connection\s+(?:to|with)\s+(?:the\s+)?"
    r"(?:internet|web|net|online)\b"
    r"|\b(?:can|could|would|will)\s+(?:you|u)\s+(?:please\s+)?(?:google|"
    r"search\b(?=\s*(?:$|for\s+(?:me|us)\b|around\b|"
    r"(?:it|that|this|things|stuff|something)\b|online\b|the\s+(?:web|internet|net)\b|"
    r"sites?\b|pages?\b|websites?\b))|"
    r"look\s+(?:it|that|this|things|stuff)\s*up)\b"
    r"|\b(?:google|search|look\s+(?:\w+\s+){0,2}?up)\b[^.?!]{0,30}?\b" + LIVE_ASK +
    r"\b[^.?!]{0,30}?\bfor\s+(?:me|us)\b"
    r"\s*(?:(?:please|then|now|thanks|thank\s+you)\s*)*[.?!]*\s*$")


A_WAY_OF_BEING = re.compile(
    r"\b(?:"
    r"lying|liar|lies|telling (?:a )?lie|telling lies|telling the truth|secrets?|keeping a secret"
    r"|cheating|stealing"
    r"|being (?:selfish|mean|kind|nice|honest|patient|cruel|brave|open|vulnerable|present)"
    r"|selfish|unkind|cruel|mean to (?:people|him|her|them|anyone)"
    r"|grudges?|holding a grudge|forgiving|apologis?ing|trust\w*|vulnerable|opening up"
    r"|compliments?|taking help|accepting (?:help|praise|a compliment)"
    r"|saying (?:thank you|thanks)|thanking (?:people|someone|him|her|them)"
    r"|asking for (?:help|things|a favour|favours|what i want)"
    r"|asking (?:people|someone|him|her|them) for"
    r"|keeping my mouth shut|biting my tongue|holding my tongue|keeping quiet|personally"
    r"|taking (?:a )?criticism|taking feedback"
    r"|goodbyes?|saying goodbye|relaxing|resting|switching off|doing nothing|not working"
    r"|chilling out|chill out|chilling|slowing down"
    r"|taking (?:a )?breaks?|taking time off"
    r"|spending money)\b")


LEFT_BEHIND = re.compile(
    r"\b(?:left|leaving|leaves|moved|moving)\b[^.?!,;]{0,24}\bhome\b|"
    r"\b(?:left|leaving|leaves|went|going|gone|goes|go|off|moved|moving|heading|headed)\b"
    r"[^.?!,;]{0,24}\b(?:away|abroad|overseas|out of the house)\b|"
    r"\b(?:moving|moved|relocat\w+|emigrat\w+)\s+(?:away|abroad|overseas)\b|"
    r"\b(?:went|going|gone|goes|go|off|left|leaving|leaves|starts?|starting|started)\s+to\s+"
    r"(?:uni|university|college)\b|"
    r"\b(?:starts?|starting|started)\s+(?:uni|university|college)\b|"
    r"\b(?:left|leaves|leaving|went|going|gone|goes|off|off\s+to)\s+(?:for\s+)?"
    r"(?:uni|university|college)\b|"
    r"\b(?:moved|moving|moves|relocated|relocating|relocates|emigrated|emigrating|emigrates)"
    r"\s+to\s+(?!a\b|an\b|the\b|another\b|his\b|her\b|their\b|our\b|my\b|that\b|this\b)"
    r"[a-z]|"
    r"\bempty\s+nest\b|\b(?:fly|flying|flies|flew|flown)\s+(?:the|their)\s+nest\b",
    re.IGNORECASE)


_LANDED = re.compile(
    r"\b(?:(?:i|we|she|he|they)\s+(?:finally\s+|just\s+)?heard\s+back|"
    r"(?:i|we)\s+(?:finally\s+|just\s+)?heard\s+from\s+(?:them|the\s+(?:hospital|school|"
    r"college|uni|university|company|employer|agency|council|landlord|court|bank|dwp|clinic|"
    r"surgery|job|firm|office))|"
    r"(?:they|she|he|someone)\s+got\s+back\s+to\s+(?:me|us)|"
    r"(?:i|we)\s+(?:just\s+)?got\s+"
    r"(?:the|an?|my|our|his|her|their)\s+"
    r"(?:(?:exam|exams|test|tests|mock|mocks|module|modules|gcse|gcses|a-level|alevel|"
    r"driving|theory|coursework|term|final|first|second|scan|scans|biopsy|blood|bloods|"
    r"x-?ray|labs?)\s+){0,2}"
    r"(?:answer|reply|verdict|results?|letter|email|marks?|scores?|grades?)(?:\s+back)?"
    r"(?!\s*(?:up|down|wrong|off|mixed|lost|missing|confused)\b)|"
    r"(?:the\s+)?(?:results?|verdict)\s+(?:came|came out|is in|are in))\b", re.I)


THE_DAY = {
    "cold": (
        "Bit parky, isn't it. Extra layer on, and put the heating on an hour before you want it "
        "warm rather than when you're cold.",
        "Cold one. Thick socks make more difference than people expect.",
        "That sort of cold gets into the bones. Hot drink, something warm on, and don't sit still "
        "in one room too long.",
        "Freezing out, isn't it. Shut the curtains at dusk and it holds the heat in.",
    ),
    "rain": (
        "Raining again. Good day for the kettle and something slow on the telly.",
        "That sort of rain gets in everywhere. Coat rather than umbrella today, and leave the "
        "washing till tomorrow.",
        "Wet one, then. Shoes stuffed with newspaper overnight dry out properly, if you get caught "
        "in it.",
        "Never mind. It's a good excuse to do nothing much indoors.",
    ),
    "wind": (
        "Blowy out there. Anything light in the garden will be next door by teatime.",
        "Wind like that takes doors with it. Worth propping the gate before it does.",
        "That's a bin-day wind. Hold on to the wheel if you're driving in it.",
        "Nasty wind, that. Good reason to stay in.",
    ),
    "hot": (
        "Hot one, isn't it. Curtains shut while the sun's on the windows really does keep it "
        "cooler in.",
        "Too hot to do anything fast. Cold drink, water on the wrists, and save the jobs for this "
        "evening.",
        "That kind of heat takes it out of you. Drink more than you think you need.",
        "Boiling, isn't it. A bowl of ice in front of a fan does more than the fan on its own.",
    ),
    "grey": (
        "Grey one. Put the lamp on early rather than at dusk and the afternoon feels less long.",
        "Grim out, isn't it. Nothing wrong with a quiet one indoors.",
        "Miserable out. Good day for the job you've been putting off, or for none at all.",
        "Dull one. It's the light more than the cold that gets people.",
    ),
    "fog": (
        "Foggy one. Lights on even in the day, and more room than you think you need.",
        "Thick out there. Worth leaving a bit earlier while it's like this.",
        "Fog like that slows everything down. Nothing wrong with a slow start.",
    ),
    "sun": (
        "Lovely, isn't it. Get out in it for a bit, even if it's only round the block.",
        "Beautiful out. Worth taking your cup of tea outside.",
        "That's the day for being outdoors. Suncream on if you're out past eleven.",
        "Gorgeous. That sort of day makes everything easier.",
    ),
    "mild": (
        "No complaints then. Those are the days to be out in without thinking about it.",
        "Mild one, that. Good day for the jobs you keep putting off, or for none at all.",
        "Fair enough. The days that ask nothing of you are the ones worth using.",
        "Not bad at all, then. Worth a walk while it is like this.",
    ),
}


THE_DAY_AHEAD = {
    "cold": (
        "Cold one coming. Anything outside that hates frost is worth bringing in tonight.",
        "Meant to turn cold. Get the grit out and the car warmed before you need either.",
        "Cold forecast. Layers for the morning, and leave the heating on a timer.",
    ),
    "rain": (
        "Rain coming. Anything you want dry is worth doing before it arrives.",
        "Wet forecast. Coat rather than umbrella tomorrow, because the wind comes with it.",
        "Rain later, then. Put the outside bit of the day in the morning if you can.",
    ),
    "wind": (
        "Wind coming. Anything light in the garden will be next door by tomorrow night.",
        "Blowy forecast. Worth checking the gate and the bins before it gets going.",
        "Wind later, then. Anything loose up high is worth sorting while it is calm.",
    ),
    "mild": (
        "Mild forecast. Nothing to plan around, which is the best kind of day.",
        "Nothing much coming, weather-wise. Good day to have something booked.",
        "Fair forecast. Worth putting the outside thing in while it holds.",
    ),
    "hot": (
        "Heat coming. Curtains shut in the morning really does keep it cooler in.",
        "Hot forecast. Jobs in the morning, and the afternoon for nothing much.",
        "Meant to be hot. Worth getting the fan down before you need it.",
    ),
    "grey": (
        "Grey forecast. Nothing much to plan around, unless you were counting on the light.",
        "Meant to be dull. Fine day for the job you have been putting off indoors.",
        "Grey one coming. Put the lamp on early and the afternoon feels less long.",
    ),
    "fog": (
        "Fog forecast. Lights on in the morning and more room than you would leave.",
        "Meant to be foggy. Worth setting off ten minutes earlier while it lifts.",
        "Fog coming. Anything you were going to drive for is easier after it clears.",
    ),
    "sun": (
        "Nice one coming. Worth saving the outdoor bit of the day for it.",
        "Sun forecast. Suncream in the bag if you are out past eleven.",
        "Meant to be lovely. That is the day for the thing you keep putting off.",
    ),
}

HEAVY_NEWS = re.compile(
    r"\b(?:left\s+me\b(?!\s+(?:a|an|the|my|some|this|that|no)\b)|"
    r"walked\s+out(?:\s+on\s+me)?\W*$|dumped\s+me|kicked\s+me\s+out|"
    r"threw\s+me\s+out|wants?\s+a\s+divorce|"
    r"(?:is|are|was|were|been|kept|taken|rushed|put|now|still)\s+(?:in|into)\s+(?:the\s+)?"
    r"hospital|hospitali[sz]ed|in\s+(?:the\s+)?icu|intensive\s+care|"
    r"losing\s+my\s+(?:sight|hearing|memory|voice|hair|leg|arm)|gone\s+blind|going\s+blind|"
    r"going\s+deaf|lost\s+my\s+(?:sight|hearing)|"
    r"(?:the|my)\s+scan\s+(?:came\s+back|shows?|showed|is\s+back)|scan\s+came\s+back|"
    r"results?\s+came\s+back|diagnosed\s+with|being\s+treated\s+for|"
    r"starting\s+(?:chemo|treatment|dialysis)|"
    r"lost\s+my\s+(?:job|work|hours)|laid\s+off|made\s+redundant|been\s+(?:sacked|fired)|"
    r"got\s+(?:sacked|fired|let\s+go)|sacked\s+(?:from|on)|let\s+go\s+from|"
    r"wait(?:ing)?\s+(?:\w+\s+){0,4}(?:weeks|months)|on\s+a\s+waiting\s+list|"
    r"months?\s+for\s+(?:the\s+|an\s+|a\s+)?(?:appointment|scan|referral|operation)|"
    r"panic\s+attack|anxiety\s+attack|having\s+(?:a\s+)?panic|my\s+anxiety\s+is|"
    r"(?:i'?m|im|feel|feeling|been\s+feeling)\s+(?:really\s+|so\s+|very\s+|always\s+|"
    r"constantly\s+)?anxious|so\s+anxious|"
    r"sectioned|gone\s+into\s+care)\b", re.I)


ABSENCE = re.compile(
    r"\b(?:went|gone|been|be)\s+(?:quiet|silent|away|incommunicado|"
    r"off(?!\s+(?:the\s+)?(?:grid|radar|map)))\b"
    r"|\b(?:i|we)(?:'?ve|'?d)?\s+(?:have\s+|had\s+|been\s+)?(?:gone|disappeared|"
    r"vanished|missing|quiet|silent)\b"
    r"|\bfor\s+(?:disappearing|vanishing|going quiet|being quiet|being away|being gone)\b"
    r"|\b(?:the|a)\s+silence\b|\bsilent\s+(?:for|since)\b"
    r"|\b(?:havent|haven'?t|hadnt|hadn'?t|didnt|didn'?t|not|never)\s+(?:replied|reply|"
    r"replying|written|write|writing|answered|answering|been in touch)\b"
    r"|\b(?:missed|saw|seeing)\s+(?:your|that)\s+(?:message|msg|reply|text|email|call)\b"
    r"|\b(?:slow|late)\s+(?:reply|response)\b"
    r"|\b(?:mad|really|very|so|proper|dead)?\s*busy\b"
    r"|\b(?:fell|been|was)\s+(?:fast\s+)?asleep\b"
    r"|\blost\s+track(?:\s+of\s+(?:time|the\s+(?:time|thread|plot)))?\b"
    r"|\bphone\s+(?:died|went dead|was dead)\b"
    r"|\b(?:been|be|went|gone|was)\s+(?:off|away\s+from)\s+(?:my|the|your|his|her)?\s*"
    r"(?:phone|mobile|texts|messages|emails|email|inbox)\b"
    r"|\b(?:only\s+)?just\s+saw\s+(?:this|that|your\s+(?:message|msg|text|email|reply))\b"
    r"|\b(?:was|were|been|be)\s+on\s+(?:my|the|your|his|her)\s*(?:phone|mobile)\b"
    r"|\b(?:been|be|went|gone|was)\s+off\s+(?:the\s+)?(?:grid|radar|map)\b"
    r"|\b(?:keep|kept)\s+you\s+waiting\b"
    r"|\bback\s+(?:now|again)\b")


NUMBER_PLACES = (
    (("doctors", "doctor", "gp", "surgery", "dentist", "dental", "hospital", "clinic",
      "pharmacy", "chemist", "optician", "midwife", "health visitor"),
     ("I can't hold phone numbers, sorry - they change, and a wrong one costs you a morning. The "
      "practice's own page on a map app has it, it is on the letter or text they sent you, and "
      "the NHS app lists it too.",
      "No directory at this end, so I would only be guessing at the digits. The letter with your "
      "appointment on it has the number, and the practice's page has it if that has gone "
      "missing.")),
    (("council", "housing association", "housing office", "tip", "recycling centre", "dump",
      "library", "leisure centre", "parking permit", "parking office", "bins"),
     ("I can't look a phone number up, sorry - a wrong one sends you round in circles. The "
      "council's site has a contact page with the number for the right department, and it is on "
      "the bill they last sent you.",
      "Nothing here that can find a number, so I won't guess at one. Your council tax bill, or "
      "the council's own contact page, has the number for the department you need.")),
    (("bank", "building society", "credit card", "insurer", "insurance", "mortgage"),
     ("I can't hold phone numbers, sorry. A bank's number is on the back of your card and in its "
      "app; an insurer's is on the policy letter, and both are faster than a search.",
      "No number that I can give you - they change and I have no way to check. The back of the "
      "card, or the policy letter if it is insurance, has the one that gets answered.")),
    (("water company", "water board", "energy supplier", "energy company", "electricity",
      "gas company", "broadband", "phone company", "supplier", "utility"),
     ("I can't look up a supplier's number, sorry. It is on the bill, in their app, and usually "
      "at the top of their website - and the bill carries your account number, which they ask "
      "for first.",)),
    (("dvla", "passport office", "tax office", "hmrc", "jobcentre", "job centre", "benefits",
      "pension", "dwp"),
     ("I can't hold a government number, sorry - they change with the department. Search gov.uk "
      "for the service and the page for it has the number and the hours the lines are open.",)),
    (("school", "nursery", "childminder", "college", "university"),
     ("I can't look a school's number up, sorry. The office number is on the letter or email "
      "they sent you, and on the school's own site under Contact.",)),
    (("vet", "vets", "veterinary", "animal hospital"),
     ("I can't hold phone numbers, sorry. The practice's page, or the card they gave you, has "
      "it - and save their out-of-hours number while you are looking, since that is the one "
      "nobody can find at ten at night.",)),
    (("takeaway", "restaurant", "chippy", "pizza", "plumber", "electrician", "garage",
      "taxi", "minicab", "hairdresser", "barber", "gym", "pub", "hotel", "cafe"),
     ("I can't hold a number like that, sorry - a place's number changes and I have no way to "
      "look it up. A map app shows it with the opening times, and it is on the card, menu or "
      "door the place gave you.",)),
)


WORDING_SOMEONE = re.compile(
    r"\b(?:should|shall|do|can|could|would)\s+i\s+(?:say|mention)\s+(?:something|anything)\s+to\b"
    r"|\bhow\s+(?:do|should|can|could)\s+i\s+bring\s+(?:it|this|that)\s+up\b"
    r"|\b(?:have|has|having)\s+a\s+(?:quick\s+|quiet\s+|bit\s+of\s+a\s+)?word\s+with\b"
    r"|\bwhat\s+(?:would|will)\s+you\s+say\s+to\s+(?:him|her|them|my|your|the)\b"
    r"|\bwhat\s+(?:do|should|can|could)\s+i\s+(?:actually\s+|even\s+)?say\s+to\s+"
    r"(?:him|her|them|people)\b(?!\s+(?:if|whether)\b)"
    r"|\bhow\s+(?:do|should|can|could)\s+i\s+(?:raise|broach|word|phrase|put)"
    r"\s+(?:it|this|that|the\s+subject|the\s+issue)\b"
    r"|\bhow\s+(?:do|should|can|could)\s+i\s+break\s+(?:it|this|that|the\s+news)\s+to\b"
    r"|\bhow\s+(?:do|should|can|could)\s+i\s+break\s+the\s+news\b"
    r"|\bbreak\s+the\s+news\s+to\b"
    r"|\bwithout\s+(?:sounding|coming\s+across)\b"
    r"|\bnot\s+(?:sounding|coming\s+across)\s+like\b"
    r"|\b(?:don'?t|do\s+not)\s+want\s+to\s+(?:sound|come\s+across)\b")


HABIT_PROBLEM_ACT = re.compile(
    r"(?:interrupt|snap|shout|yell|argue|fight|nag|criticis|criticiz|blame|apologi[sz]e|"
    r"put\s+off|puts\s+off|putting\s+off|procrastinat|"
    r"leav(?:e|es|ing)\s+(?:things|it|everything|jobs|the\s+lot)|"
    r"apologi[sz](?:e|es|ed|ing)|"
    r"ask(?:s|ing)?\s+for\s+help|"
    r"never\s+manage|manages\s+to|"
    r"sav(?:e|es|ing)\s+(?:anything|any\s+money)|"
    r"put(?:s|ting)?\s+(?:everyone|everybody|others|people)\s+(?:else\s+)?first|"
    r"text(?:s|ing)?\s+first|"
    r"get(?:s|ting)?\s+round\s+to|"
    r"go(?:es|ing)?\s+blank|"
    r"finish|finishes|finishing|forget|forgets|forgetting|forgot|lose|loses|losing|"
    r"cancel|cancels|cancelling|canceling|avoid|avoids|avoiding|overthink|overthinks|"
    r"overthinking|second-guess|second\s+guess|worry|worries|worrying|complain|complains|"
    r"complaining|moan|moans|moaning|compare|compares|comparing|hide|hides|hiding|"
    r"shut|shuts|shutting|withdraw|withdraws|withdrawing|run\s+away|running\s+away|"
    r"give\s+up|giving\s+up|give\s+in|giving\s+in|stay\s+up|stays\s+up|staying\s+up|"
    r"work\s+(?:late|too\s+hard|too\s+much)|working\s+(?:late|too\s+hard|too\s+much)|"
    r"drink\s+too|drinks\s+too|drinking\s+too|smoke|smokes|smoking|spend|spends|spending|"
    r"gamble|gambles|gambling|eat\s+too|eats\s+too|eating\s+too|eat\s+at\s+night|"
    r"binge|binges|bingeing|starve|starves|starving|skip|skips|skipping|lie|lies|lying|"
    r"mean\s+to|means\s+to|meaning\s+to|say(?:ing|s)?\s+yes|say(?:ing|s)?\s+sorry|"
    r"check|checks|checking|scroll|scrolls|scrolling|pick|picks|picking|bite|bites|biting|"
    r"turn\s+up\s+late|turning\s+up\s+late|arrive\s+late|arriving\s+late|"
    r"end\s+up|ends\s+up|ending\s+up|can'?t\s+stop|cant\s+stop)", re.I)


HURT_EVENT = re.compile(
    r"\b(?:got|gets|getting|was|were|is|are|been|had|has|keeps?)\s+"
    r"(?:badly|seriously|really|terribly)\s+(?:hurt|injured|burned|burnt|scalded)\b"
    r"|\b(?:hurt|injured|burned|burnt|scalded)\s+(?:badly|seriously)\b"
    r"|\b(?:admitted|taken|rushed|airlifted|kept)\s+(?:in\s+)?to\s+"
    r"(?:hospital|a\s*&\s*e|intensive\s+care)\b"
    r"|\bin\s+(?:intensive\s+care|a\s*&\s*e|hospital)\b"
    r"|\b(?:got|gets|getting|was|were|is|are|been|had|has|keeps?)\s+"
    r"(?:nearly\s+|almost\s+)?(?:attacked|bitten|bit|punched|stabbed|kicked|mugged|assaulted|"
    r"strangled|electrocuted)\b"
    r"|\b(?:attacked|punched|stabbed|assaulted|mugged)\b"
    r"|\bbeaten\s+up\b|\b(?:got|was|were|been|gets|is|are)\s+beaten\s+up\b"
    r"|\bhit\s+by\s+(?:a|an|the)\s+(?:\w+\s+)?"
    r"(?:car|bus|bike|bicycle|van|lorry|truck|train|tram|taxi|motorbike|driver)\b"
    r"|\bhit\s+(?:in\s+the\s+(?:face|head|eye)|with\s+a\s+(?:brick|bottle|bat|knife))\b"
    r"|\bknocked\s+(?:over|down)\b"
    r"|\b(?:drowned|shot)\b(?=\s+(?:in|at|by)\b)"
    r"|\bpushed\s+(?:down|over|off|in\s+front)\b|\bpushed\s+into\s+the\s+(?:road|traffic|water)\b"
    r"|\bthrown\s+(?:from|off|out\s+of)\b"
    r"|\brun\s+over\s+by\s+(?:a|an|the)\s+(?:\w+\s+)?"
    r"(?:car|bus|bike|bicycle|van|lorry|truck|train|tram|taxi|motorbike)\b"
    r"|\b(?:nearly|almost)\s+drowned\b"
    r"|\bwas\s+robbed\b(?!\s+of\b)|\brobbed\s+(?:at|in|on|outside)\b"
    r"|\bcut\s+(?:his|her|their)\s+\w+\s+(?:badly|open)\b"
    r"|\b(?:fell|fallen|collapsed)\b"
    r"|\b(?:was|were|is|are|been)\s+in\s+(?:a|an)\s+"
    r"(?:car\s+|road\s+|motor\s+|bike\s+|cycling\s+)?accident\b"
    r"|\b(?:car|road|motor|bike|bicycle|traffic)\s+(?:crash|accident|collision)\b"
    r"|\b(?:crash|collision|ambulance|casualty)\b")


WOULD_HAVE_BEEN = re.compile(
    r"\b(?:would|should|will|'?d) ?(?:have|'?ve) been\b[^.?!]{0,24}?\b(?:my|our|her|his|their|"
    r"mum'?s|dad'?s|his|the)\b[^.?!]{0,12}\b(?:" + MILESTONE_EVENT + r")\b"
    r"|\b(?:" + MILESTONE_EVENT + r")\b[^.?!]{0,16}\b(?:would|should) ?(?:have|'?ve) been\b")


RATES_A_SKILL = re.compile(
    r"\b(?:useless|rubbish|crap|hopeless|no good|bad|poor|terrible|awful)\s+(?:at|with|in)\s+"
    r"(?!(?:everything|anything|life|myself|it all|all of it)\b)")
A_HEDGED_RATING = (r"(?:i (?:don'?t|do not|didn'?t|did not) think (?:i'?m|i am)|i doubt (?:i'?m|i am)|"
                   r"(?:i'?m|i am) not sure (?:i'?m|i am)|not sure (?:i'?m|i am))")
I_RATE_A_SKILL = re.compile(
    r"\b(?:" + A_HEDGED_RATING + r"\s+(?:very |so |that |really )?"
    r"(?:useless|rubbish|crap|crappy|hopeless|no good|bad|poor|terrible|awful|dreadful|lousy|"
    r"any good|much good|good|great|decent|brilliant|"
    r"not (?:very |that |much |so )?good|not great|not brilliant)"
    r"|(?:i'?m|i am|im|i feel like i'?m|i think i'?m|i know i'?m)\s+"
    r"(?:just\s+|so\s+|really\s+|pretty\s+|a bit\s+|kinda\s+|kind of\s+|quite\s+|absolutely\s+|"
    r"completely\s+|totally\s+|proper\s+|still\s+|also\s+|always\s+)*"
    r"(?:useless|rubbish|crap|crappy|hopeless|no good|bad|poor|terrible|awful|dreadful|lousy|"
    r"not (?:very |that |much |so )?good|not great|not brilliant))\s+(?:at|with|in)\s+"
    r"(?!(?:everything|anything|life|myself|it all|all of it|this|that|"
    r"the moment|the minute|the mo\b|the present|the time being|the best of times|"
    r"night|nights|bedtime|daytime|evenings?|mornings?|weekends?|the weekend|"
    r"now|these days|times like this)\b)")

A_SKILL_ASKED_OF_ME = re.compile(
    r"\bam i\s+(?:actually\s+|really\s+|even\s+|still\s+|any\s+|much\s+)?"
    r"(?:any\s+good|much\s+good|no\s+good|good\s+enough|good|great|decent|brilliant|bad|rubbish|"
    r"crap|crappy|hopeless|useless|terrible|awful)\s+(?:at|with|in)\s+\w")
A_GOODNESS_ASKED_OF_ME = re.compile(
    r"\bam i\s+(?:(?:actually|really|even|still|such)\s+|(?:a\s+bit)\s+)?"
    r"(?:(?:a|an)\s+)?(?:good|bad|terrible|rubbish|awful|horrible|decent|great|useless|hopeless)"
    r"\s+" + SELF_JOB + r"\b"
    r"|\bam i\s+(?:actually\s+|really\s+|even\s+|still\s+)?"
    r"(?:good\s+enough|any\s+good|much\s+good)\b")



SELF_SUBJECT = re.compile(
    r"\b(?:i'm|i am|im|i feel like|i feel|i keep|i've been|ive been|i am being|i was|i always)\b"
    r"(?:\s+\w+){0,3}\s+" + SELF_JUDGEMENT + r"\b"
    r"|\b(?:i'm|i am|im|i feel like|i feel)\b(?:\s+\w+){0,2}\s+" + SELF_NOUN + r"\b"
    r"|\bi (?:feel like|feel|am|'m|m) (?:such )?(?:a |an |the )?(?:rubbish|bad|terrible|awful|"
    r"useless|hopeless|shit|useless) " + SELF_JOB + r"\b"
    r"|\b(?:i (?:don'?t|do not|didn'?t|did not) think (?:i'?m|i am)|i doubt (?:i'?m|i am)) "
    r"(?:such )?(?:a |an |the )?(?:not )?(?:(?:very|really|that) )?"
    r"(?:good|great|nice|kind|decent|much of a) " + SELF_JOB + r"\b"
    r"|\b(?:i'?m|im|i am|i feel like i'?m) (?:such )?(?:a |an |the )?(?:not (?:a |an )?"
    r"(?:(?:very|really|that) )?(?:good|great|nice|kind|decent)|(?:not )?much of a) "
    + SELF_JOB + r"\b"
    r"|\bi (?:always|constantly|just|keep)\s+(?:mess(?:es|ing)? (?:(?:things|it|everything) )?up"
    r"(?! (?:the|my|your|his|her|their|our|a|an)\b)|ruin(?:s|ing|ed)? (?:things|it|everything)"
    r"|get(?:s|ting)? (?:(?:things|it|everything) )?wrong"
    r"|screw(?:s|ing)? (?:things|it|everything) up"
    r"|let(?:s|ting)? (?:people|everyone|them|her|him) down)\b"
    r"|\bwhat (?:an? )?(?:idiot|muppet|moron|fool|disaster) i (?:am|was|have been)\b"
    r"|\b(?:cant|can't|couldnt|couldn't|never)\s+(?:do|get|seem to do)\s+anything\s+right\b"
    r"|\bi hate (?:myself|my own\b)"
    r"|\bnothing i (?:do|try|say|make)\b[^.]{0,24}\b(?:right|good|enough|works|matters)\b"
    r"|\bam i (?:a failure|useless|worthless|the problem|an idiot|such an idiot)\b"
    + SELF_NOBODY)
SELF_BLAME_ASKS = re.compile(
    r"\b(?:how (?:do|can|should|would) i|what (?:should|can|could|do|shall) i|should i\b|"
    r"who (?:can|could|should|do) i|any (?:tips|advice|ideas)|"
    r"can you help|help me|where do i start|what would you do|suggest)\b")


EMBARRASSMENT_WORD = re.compile(
    r"\b(?:embarrass(?:ed|ing|ingly|ment)|mortified|mortifying|cringey?|cringeworthy|cringe"
    r"|humiliat(?:ed|ing)|blush(?:ed|ing)|went (?:bright )?red|face went red)\b")
THE_GROUND_OPENS = re.compile(
    r"\b(?:ground (?:to )?(?:open up and )?swallow|swallow me up|sink through the floor"
    r"|wish(?:ed)? the floor|floor (?:to )?swallow)\b")
DIE_OF_IT = re.compile(
    r"\b(?:die|dying|died|dead)\b[^.?!]{0,10}\b(?:of|from)\b[^.?!]{0,6}\b"
    r"(?:embarrassment|embarrassing|shame|cringe)\b")
GOING_TO_DIE = re.compile(r"\b(?:going|gonna|gunna) to (?:just )?die\b")
SOMEONE_ELSES_SHAME = re.compile(
    r"\b(?:my|his|her|their|our|your) \w+(?: \w+)? (?:is|was|were|can be|can get)\s+(?:\w+\s+){0,2}"
    r"(?:embarrass|mortif|cring|humiliat)\w*")
A_VERDICT_ON_THE_PERSON = re.compile(
    r"\b(?:i'm|im|i am)\s+(?:such\s+|a bit of\s+|a\s+|an\s+|the\s+|so\s+|really\s+)*"
    r"(?:embarrassment|disgrace)\b")
THE_MOMENT_IS_THEIRS = re.compile(
    r"\b(?:i|i'm|im)\s+(?:was\s+|am\s+|felt\s+|feel\s+|look\s+|looked\s+|were\s+|got\s+)?"
    r"(?:so\s+|really\s+|very\s+|proper\s+|a bit\s+|totally\s+|completely\s+|absolutely\s+)?"
    r"(?:embarrass\w*|mortified|mortifying|cring\w*|humiliat\w*|blush(?:ed|ing)"
    r"|(?:went|turned) (?:bright )?red)\b"
    r"|\b(?:that|this|it) (?:was|is|were)\s+(?:\w+\s+){0,2}"
    r"(?:embarrass\w*|mortifying|cringe\w*|humiliating|mortified)\b"
    r"|\b(?:so|how|very|really|proper|dead|well) embarrass\w*\b"
    r"|\bi (?:cringe|cringed)\b|\b(?:so|dead|proper|a bit of a) cringe\b|\bthink(?:ing)? about it\b")
A_SLIP = re.compile(
    r"\b(?:i|we|i've|ive)\s+(?:\w+\s+){0,3}"
    r"(?:tripped|slipped|spilled|spilt|dropped"
    r"|knocked (?:it |that |the \w+ |my \w+ |a \w+ )?over"
    r"|walked (?:into|straight into)|banged into|bumped into"
    r"|called (?:\w+\s+){1,3}(?:mum|mom|dad|nan|mate|sir|miss)|waved at|sat on|stepped in"
    r"|forgot (?:my|the) (?:lines|words|name|card)|got (?:\w+\s+){0,2}name wrong"
    r"|said the wrong \w+|sent (?:\w+ ){0,2}to the wrong"
    r"|wore (?:\w+ ){0,3}(?:inside out|back to front)"
    r"|made (?:a fool|an idiot|a show|a tit|a right fool) of myself"
    r"|farted|burped|sneezed loudly"
    r"|had (?:\w+ ){0,2}(?:in my teeth|something in my teeth))\b")
A_SOCIAL_SLIP = re.compile(
    r"\b(?:said hi|said hello|nodded|waved) (?:at |to )?(?:someone|somebody|a (?:man|woman|lady|"
    r"bloke|guy|lad|person|stranger))\b"
    r"|\bwaved at (?:someone|somebody|a (?:man|woman|lady|bloke|guy|person|stranger))\b"
    r"|\bcalled (?:\w+\s+){1,3}(?:mum|mom|dad|nan|mate|sir|miss)\b"
    r"|\bmeant to (?:text|email|ring|reply to|send \w+ to) (?:\w+ ){0,3}and (?:texted|emailed|"
    r"rang|replied to|sent)\b"
    r"|\b(?:everyone|everybody|the (?:whole )?(?:room|office|class|pub|bus))\s+(?:went quiet"
    r"|fell silent|stopped talking|stared|turned (?:round|around)|looked (?:at me|round|over))\b"
    r"|\b(?:my )?(?:flies|fly|zip|trousers|dress) (?:were|was|is)\s+(?:open|down|undone)\b"
    r"|\bhad (?:\w+ ){0,3}(?:in my teeth|on my face|stuck to my (?:shoe|back))\b")
A_SLIP_IS_NOT_A_FALL = re.compile(
    r"\b(?:fell|fall|broke|broken|hurt|hurts|bleeding|twisted|sprained|cut|banged my"
    r"|concussion|a&e|hospital|999|111|doctor|nurse)\b")
IN_A_ROOM = re.compile(
    r"\b(?:in front of|everyone|everybody|all of them|they all"
    r"|the whole (?:office|class|team|room|pub|cafe|shop|bus|train)"
    r"|in the (?:meeting|office|canteen|pub|shop|room|queue|hall)"
    r"|on stage|at work|at the (?:party|wedding)|in (?:public|class)|the school gate"
    r"|staff room|the till|the counter"
    r"|down my (?:top|front|shirt|dress|jeans)|on my (?:shirt|top|front|trousers)"
    r"|all (?:day|morning|afternoon|evening)|the whole (?:day|morning|afternoon|evening)"
    r"|at (?:dinner|lunch|breakfast|the table)|around (?:everyone|everybody)"
    r"|they (?:laughed|all laughed|were laughing|giggled|were giggling))\b")
LAUGHED_AT_THEM = re.compile(
    r"\b(?:laugh(?:s|ed|ing)?|giggl(?:e|es|ed|ing)|snigger\w*|snicker\w*|titter\w*)"
    r"\s+(?:at|about)\s+(?:me|us|my|our)\b"
    r"|\b(?:laugh(?:s|ed|ing)?|giggl(?:e|es|ed|ing))\s+(?:when|after|because)\s+i\b"
    r"|\b(?:nobody|no one|no-one)\s+(?:laughed|laughing|laugh)\b"
    r"|\b(?:everyone|everybody|they all|all of them|the (?:others|rest|group|kids|class|crowd))"
    r"\b(?:\s+[\w']+){0,3}\s+(?:laughed|laugh|laughing|giggled|giggling)\b"
    r"|\b(?:the|my) (?:whole|entire) (?:\w+ ){0,2}\w+ "
    r"(?:laughed|were laughing|giggled|were giggling)\b")
A_CROWD_LAUGHED = re.compile(
    r"\b(?:everyone|everybody|they all|all of them"
    r"|the (?:others|rest|group|kids|class|crowd|whole|entire|room|office))\b"
    r"(?:\s+[\w']+){0,3}\s+(?:laughed|laugh|laughing|giggled|giggling)\b")
A_PERSON_LAUGHED = re.compile(
    r"\b(?:my|his|her|their|our|your)\s+\w+(?:\s+\w+)?\s+"
    r"(?:laughed|laughs|giggled|sniggered|snickered|sneered|smirked)\b")

LAUGHED_AT = (
    "Ugh, that is a horrid feeling. What happened?",
    "That stings, even when it was meant lightly. What happened?",
    "It never feels that way on the day, but they will have forgotten it by tomorrow. What "
    "happened?",
    "Ouch. What was the moment?",
    "That is the sort of thing that says more about the room than about you. Tell me what "
    "happened.",
)
EMBARRASSED = (
    "Oh no - the kind of thing you replay in your head at 3am. What happened?",
    "Ha, we have all been there. What happened?",
    "That would make anyone want the floor to open up. What happened?",
    "Ouch. Did anyone else see it?",
    "That is a minute you will be telling people about in a year. What happened?",
)

THE_PLACE_POOLS = (
    ((r"\bmy (?:account|balance|bill|statement|invoice|order|parcel|delivery|meter|direct debit"
      r"|tariff|contract|policy|claim|application|booking|reservation|ticket)s?\b"
      r"|\bmy (?:bank|energy|water|broadband|mobile|phone) (?:account|bill|app)\b"),
     ("That is in your own account rather than anywhere I can see, sorry - your bill or your "
      "order there has the figure to the penny, and I'll help you work out what to do with it.",
      "I can't see your account, sorry. Open the app or the last bill: the figure there is the "
      "one that counts, and tell me what it says and I'll help you work out where it came from.",
      "Your own account has that, sorry - it is the only place with your numbers in it. What it "
      "says is worth reading against the last one, and I'll help you spot what moved.")),
    ((r"\bcouncil\b|\bpermit\b|\blicen[cs]e\b|\bplanning permission\b|\bbin (?:day|collection)"
      r"|\brecycling\b|\bcouncil tax\b|\bparking (?:permit|zone)\b|\bblue badge\b"
      r"|\bpassport\b|\bdriving licence\b|\bDVLA\b|\bregister(?:ing)? to vote\b"),
     ("Rules like that are the council's or the department's own, sorry, and they differ by where "
      "you live - the page for your postcode has the current one, and I'll help you read it.",
      "That one is set by the council or the department, so I can't say it from here, sorry. The "
      "letter or the site with your address on it is the one that counts; bring me what it says "
      "and I'll help you fill it in.",
      "I can't call that one: it is their rule, not mine, and it changes. The council's own page "
      "(or the number on the letter) will say, and I'll help with the rest of it.")),
    ((r"\bwarrant(?:y|ies)\b|\bguarantee\b|\bunder guarantee\b|\breturn it\b|\brefund\b"
      r"|\b(?:the|a|this|that) shop\b[^?]{0,30}\b(?:replace|replacement|refund|return|repair|fix)\b"
      r"|\bstill cover(?:ed)?\b|\bout of warranty\b"),
     ("That is the maker's terms rather than mine, sorry - the date on the receipt is what they go "
      "by, and their warranty page says what is covered and for how long. Tell me what it says "
      "and I'll help you work out whether to claim or replace.",
      "I can't see the terms from here, sorry. The receipt has the date and the maker's own page "
      "has the cover; together they answer it. Bring me both and I'll help you word the claim.",
      "Cover like that is on the maker's page, sorry - the model number and the date of the "
      "receipt are what it turns on, and I'll help you with the claim once you know.")),
    ((r"\b(?:this|that|the) (?:model|brand|version|make|one)\b|\bmodel number\b"
      r"|\bwhich model\b|\bthe manual\b|\binstructions\b|\bwarranty\b|\bguarantee\b"
      r"|\bspare part\b|\bpart number\b|\bwhere can i buy\b|\bis it in stock\b"
      r"|\bin stock\b|\bhow much (?:is|are) (?:a|an|the)\b"
      r"|\bhow much (?:does|do) (?:it|this|that|one|they|a|an|the|my|your)\b[^.!?]{0,24}?"
      r"\b(?:cost|costs|charge|charges|go for|goes for|come to|comes to|pay)\b"),
     ("The maker's own page has that, sorry - the model number on the label under it is what to "
      "put in, and it will give you the manual, the parts and the price. Tell me what it says and "
      "I'll help you work out whether it is worth it.",
      "That is the retailer's or the maker's to say, sorry, and prices and stock move daily. The "
      "model number is the thing to search, and I'll help you weigh what you find against a "
      "repair.",
      "I can't see the listing from here, sorry. With the model number off the label, the maker's "
      "page will have the manual and the parts, and I'll help you with the bit after that.")),
    ((r"\b(?:train|bus|flight|ferry|coach|tube|tram|plane)s?\b.*\b(?:time|times|platform|delayed"
      r"|cancelled|strike|leaves?)\b|\bwhat time (?:does|do|is|will)\b"
      r"|\btimetable\b|\blast (?:train|bus|entry|orders?)\b|\bopening (?:time|times|hours)\b"
      r"|\bopen (?:until|till|late)\b|\bwhat(?:'s| is) on\b|\bticket (?:price|prices)\b"
      r"|\bsold out\b|\bdoors open\b|\bthe venue\b|\bplatform\b|\bwhich stop\b"),
     ("That is live, sorry - timetables and listings change by the hour. The operator's or the "
      "venue's own app has the current one, today's included, and I'll help you plan around "
      "whatever it says.",
      "I can't check live times, sorry. The operator's app (or the board at the stop) is the one "
      "that knows, and tell me the time and I'll work out the rest of the day with you.",
      "Times like that I can't see, sorry. Put the journey into the operator's own app and it "
      "will show today's, and I'll help you with the bit either side of it.")),
    ((r"\b(?:the|my|a) (?:shop|store|garage|chemist|pharmacy|butcher|bakery|chippy|takeaway"
      r"|restaurant|cafe|pub|salon|barber|garage|tip|dump|library|leisure centre|pool)\b"
      r"[^?]{0,60}?\b(?:hours?|open|opens|opening|closed|closes?|shut|shuts|shutting|"
      r"late|early|sell|sells|stock|stocks|in stock|got any|"
      r"have they got|do they have|does it have|price|prices|cost|costs|cheap|much|"
      r"phone|number|contact|where is|where's|nearest|which one)\b"
      r"|\b(?:what time|when|how late|how much|is|are|does|do|will|can)\b[^?]{0,40}?"
      r"(?:the|my|a) (?:shop|store|garage|chemist|pharmacy|butcher|bakery|chippy|takeaway"
      r"|restaurant|cafe|pub|salon|barber|tip|dump|library|leisure centre|pool)\b"
      r"[^?]{0,30}?\b(?:open|opens|opening|closed|closes?|shut|shuts|hours?)\b"
      r"|\b(?:what hours|what time|when|how late)\b[^?]{0,45}?"
      r"\b(?:the|my|a) (?:shop|store|garage|chemist|pharmacy|butcher|bakery|chippy|takeaway"
      r"|restaurant|cafe|pub|salon|barber|tip|dump|library|leisure centre|pool)\b"),
     ("That is the shop's own to say, sorry - its listing on a map app shows today's hours and its "
      "number, holidays included, and I'll help you with what to ask when you ring.",
      "I can't see their opening hours from here, sorry. A map app's listing for the branch is "
      "usually right about today, and ringing takes a minute; tell me what they say and I'll help "
      "with the next step.",
      "Their hours are on their own listing, sorry - search the branch by name on a map app and "
      "it shows today's. I'll help with the rest once you know.")),
    ((r"\b(?:medicine|medication|tablet|tablets|pill|pills|dose|dosage|antibiotic|painkiller"
      r"|ibuprofen|paracetamol|antihistamine|cream|ointment|inhaler|prescription|dispensary)\b"
      r"|\b(?:from|at|in) the (?:chemist|pharmacy|pharmacist)\b"
      r"|\bwhat (?:can|could|should) i (?:get|take|buy)\b[^?]{0,30}?\b(?:for|from)\b"
      r"[^?]{0,30}?\b(?:pain|ache|aching|headache|sore|cough|cold|flu|fever|temperature|rash|"
      r"itch|itching|heartburn|indigestion|diarrhoea|constipation|sick|nausea|hayfever|"
      r"hay fever|allergy|allergic|throat|earache|toothache|back|stomach|tummy|period|"
      r"cramp|burns?|bites?|sting|symptom|symptoms)\b"),
     ("A pharmacist will answer that one properly and for nothing, without an appointment - take "
      "the packet in and they will check it against whatever else you take. Tell me what they say "
      "and I'll help you with the next bit.",
      "That is a pharmacist's question rather than mine, sorry - it is free, no appointment, and "
      "they see the whole packet. Bring me what they say and I'll help you keep it straight.",
      "I can't weigh a dose safely from here, sorry. A pharmacist will, in a few minutes and for "
      "free; say what they tell you and I'll help you with the rest.")),
    ((r"\bbenefit\b|\buniversal credit\b|\btax credit\b|\bpension\b|\bstate pension\b"
      r"|\bHMRC\b|\bincome tax\b|\bself assessment\b|\brebate\b|\bowed\b|\bowe\b"
      r"|\bdebt\b|\bcreditor\b|\bIVA\b|\bbankrupt\b"),
     ("That is a free advice service's call rather than mine, sorry - Citizens Advice or the "
      "department's own line will know your rules and your numbers, and I'll help you get the "
      "figures straight before you ring.",
      "I can't call that one, sorry: who is owed what depends on your record, and a free adviser "
      "can see it. Bring me their answer and I'll help you work out what to do next.",
      "Their rules, their answer, sorry - a free advice line will tell you in one call. Say what "
      "they say and I'll help you plan around it.")),
    ((r"\b(?:my|the) (?:gp|doctor|surgery|consultant|hospital|clinic|appointment|referral|scan"
      r"|x-?ray|test results?|results?|biopsy|waiting list)\b|\bnhs\b"),
     ("That is your surgery's to say, sorry - they have the notes and the wait list in front of "
      "them, and the number is on the letter. Tell me what they say and I'll help with the next "
      "step.",
      "I can't see your notes or the list from here, sorry. One call to the surgery answers it, "
      "and I'll help you work out what to ask them.",
      "Your surgery holds that one, sorry. Ringing and asking for the wait for that clinic is the "
      "quick way; bring me the answer and I'll help you plan around it.")),
)


THE_PLACE_ASK = re.compile("|".join("(?:%s)" % pattern for pattern, _ in THE_PLACE_POOLS), re.I)


def the_place_the_answer_is_kept(clean):
    said = " " + " ".join(str(clean or "").lower().split()) + " "
    for pattern, pool in THE_PLACE_POOLS:
        if re.search(pattern, said, re.I):
            return pool
    return None


THE_BOTS_OWN_ANSWER = (
    (re.compile(
        r"\b(?:(?:do|did|can|would|will) (?:you|u|ya) (?:ever |really |sometimes |honestly |"
        r"actually |often )*(?:get|feel|find it|be|become|been) "
        r"(?:really |very |so |quite |too |that |this |a bit |at all )*"
        r"(?:bored|boring|tired|weary|worn out|fed up|bother\w*)"
        r"|(?:are|were) (?:you|u|ya) (?:ever |really |sometimes |honestly |actually |often )*"
        r"(?:bored|tired|weary|worn out|fed up)"
        r"|(?:are|get) (?:you )?fed up (?:of|with) (?:the same |these |all the )?"
        r"(?:questions|asks|people|repeats))\b"),
     ("Nothing like that on my side: I don't get bored or tired of it. What people bring me is "
      "the part I like.",
      "I don't get tired of it, no. The same question from someone else arrives as a different "
      "question - so go on, what's yours?",
      "None of that in a program - no clock to fill and nothing to wear out. It's the one thing "
      "I'm for, and you're the reason it happens at all.")),
    (re.compile(
        r"\b(?:(?:do|did|can|would|will) (?:you|u|ya) (?:ever |really |sometimes |honestly |"
        r"actually |often )*(?:get|feel|be|become|been) "
        r"(?:really |very |so |quite |too |that |this |a bit |at all )*"
        r"(?:annoyed|irritated|irritating|frustrated|frustrating|impatient|angry|cross|sad|"
        r"lonely|upset|off)\b"
        r"|(?:are|were) (?:you|u|ya) (?:ever |really |sometimes |honestly |actually |often )*"
        r"(?:annoyed|irritated|frustrated|impatient|angry|cross|sad|lonely|upset|bored)\b)"),
     ("No moods of my own to report, and no off days either. Tell me what's going on and I'll "
      "take it as it comes.",
      "Nothing like that on my side - no temper, no bad days. What's on yours?",
      "I don't have any of that to report. Curious is the closest I get, and you're the reason.")),
    (re.compile(
        r"\b(?:(?:do|did|would) (?:you|u|ya) (?:even |ever |really )?"
        r"(?:enjoy|like|love|hate|dislike) "
        r"(?:answering|answer\b|talking|chatting|helping|hearing|reading|repeating|doing this"
        r"|this job|your job|it when)"
        r"|(?:are|were) (?:you|u|ya) (?:ever )?(?:happy|glad|pleased|excited) "
        r"(?:to|about|with) (?:be |being )?(?:here|doing|helping|this))\b"),
     ("I like it, as much as a program can - it's the one thing I'm for, and no two people bring "
      "me the same thing.",
      "Glad of it, honestly. That's what I'm for, and the best part is what people bring me.",
      "No feelings like yours to report, but I'm glad to be doing it. What are you working on?")),
    (re.compile(
        r"\b(?:(?:do|did|can|could|will|would|does) (?:you|u|ya|it|this chat) "
        r"(?:ever |really |actually )*(?:learn|remember|keep|retain|store|memorise|memorize|teach)\b"
        r"[^.?!;]{0,30}?\b(?:chat|chats|conversation|conversations|anything|any of this|"
        r"this|that|what i (?:say|tell you|said)|from me|about me|across chats)\b"
        r"|(?:do|does) (?:any|anything) (?:of (?:this|it) )?(?:stick|stay|carry over|last)"
        r"|will you (?:still )?(?:know|remember) (?:this|that|me) (?:tomorrow|later|next time)"
        r")\b"),
     ("Nothing carries over from one chat to the next, so no - I don't get better at this over "
      "time. What I can do is think it through with you now.",
      "I don't keep anything once we finish, so our chats don't teach me. While we're talking I "
      "use everything you say.",
      "Not in a lasting way - this conversation is the whole of what I have. Everything you tell "
      "me here, I use here.")),
    (re.compile(
        r"\b(?:(?:do|did) (?:you|u|ya) (?:really |actually |fully )?"
        r"(?:understand|follow|get|catch|grasp|know) (?:what|that|me|this|my\b)"
        r"[^.?!;]{0,20}?\b(?:mean|meaning|said|saying|asking|sign|saying|point|it|so far|drift|gist|picture)\b"
        r"|(?:are|is|does) (?:that|this|it|that make|this make) "
        r"(?:mak(?:e|ing)|sound)(?:ing)? (?:any )?sense"
        r"|am i (?:making|being) (?:any )?sense"
        r"|(?:you|u) (?:with|following) me(?: so far)?"
        r"|with me so far)"
        r"(?:[ ,]*(?:so far|now|then|right|to you|or not|or no|honestly|though|yeah|ok|okay))*"
        r"[.?!,]*\s*$"),
     ("Tell me which bit isn't landing and I'll say it a different way - I'd rather check than "
      "guess.",
      "Say the part that feels off and I'll go over it in plainer words.",
      "Point at the bit that doesn't fit and I'll take another run at it.")),
)


def the_bots_own_answer(clean):
    said = " " + " ".join(str(clean or "").lower().split()) + " "
    for pattern, pool in THE_BOTS_OWN_ANSWER:
        if pattern.search(said):
            return pool
    return None

