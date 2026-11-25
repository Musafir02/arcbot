import re

from .dishes import cook_ask
from .lookup import A_HOURS_ASK, entry

ANSWERS = ("home-and-diy", "technology")

RID = ("get rid", "rid of", "dispose", "disposal", "throw away", "throw out", "throwing away",
       "donate", "donated", "donating", "donation", "donations", "give away", "giving away",
       "gave away", "charity", "charity shop", "charity shops", "free ad", "free ads",
       "freecycle", "pass on",
       "where do i take", "where can i take", "where do i put", "where can i put",
       "drop off", "get shot of", "throw", "throwing", "toss",
       "chuck", "chuck out", "chucking out", "bin", "bins", "the tip", "to the tip", "tip it",
       "recycling centre", "recycle", "recycling", "kerbside", "waste", "dump", "scrap",
       "skip", "get shot", "household waste", "council collection", "collection",
       "do with")

BIN_WORDS = ("bin", "bins", "the tip", "to the tip", "recycling", "recycle", "kerbside",
             "household waste")
BIN_ASK = ("put", "throw", "chuck", "dump", "dispose", "get rid", "go in", "goes in", "go",
           "goes", "belong", "belongs", "which", "where")

CURING_ASIDE = ("without pills", "without tablets", "without medicine", "without medicines",
                "without medication", "without antibiotics", "without painkillers",
                "without any pills", "without any tablets", "without any medicine",
                "without drugs", "without meds")

MEDICINE_DISPOSAL = (
    "old", "unused", "unwanted", "leftover", "left over", "expired", "out of date", "past it",
    "no longer", "stopped taking", "dont need", "don't need", "not taking", "off them",
    "bin", "bins", "tip", "recycling", "recycle", "dispose", "throw", "throwing", "chuck",
    "pharmacy", "chemist", "where do i", "where can i", "where should i", "what do i do with",
    "get rid of the tablets", "get rid of the pills", "get rid of the medicine",
    "get rid of the medicines", "get rid of my tablets", "get rid of my pills",
    "get rid of my medicine", "get rid of my medicines", "get rid of these tablets",
    "get rid of these pills", "get rid of all the tablets", "get rid of all these pills",
    "get rid of pills", "get rid of tablets", "get rid of medicine", "get rid of medicines",
    "rid of old pills", "rid of leftover tablets",
)

NOT_RUBBISH = ("waste of money", "waste of time", "wasted money", "wasting money",
               "worth the money", "worth it", "any point in", "money well spent",
               "a good buy", "a bad buy")

ITEMS = (
    ("pizza-box",
     ("pizza box", "pizza boxes", "greasy cardboard", "oily cardboard", "dirty cardboard",
      "takeaway box", "takeaway boxes", "chip box", "food box", "food boxes", "cardboard box",
      "cardboard boxes", "greasy box"),
     "Tear off the clean lid and put that in the recycling; the greasy base goes in the general "
     "waste, or in the food waste if your council takes that. Cheese and oil soaked into card "
     "spoil the load at the sorting plant, so a soaked box is the one thing worth separating.",
     ("leftover pizza", "cold pizza", "reheat", "reheating", "eat", "freeze", "freezing",
      "how long", "order", "delivery", "delivered", "arrived", "takeaway pizza", "slice")),
    ("cardboard-boxes",
     ("cardboard", "cardboard box", "cardboard boxes", "moving boxes", "moving box",
      "packing boxes", "delivery boxes", "delivery box", "packaging", "boxes", "box",
      "cartons", "carton", "empty boxes", "pile of boxes"),
     "Flatten them and keep them dry: clean cardboard goes out with the kerbside recycling, cut "
     "down to the size your council takes, and tape, polystyrene and any food grease keep a box "
     "out of it. More than the bin will take is a bulky collection or a trip to the recycling "
     "centre, and removal boxes in good nick go fast on a local free-and-wanted group.",
     ("pizza", "greasy", "oily", "dirty", "takeaway", "chip box", "food box", "leftover",
      "gift", "present", "cereal", "hamper", "batteries", "cat", "litter", "pack", "packing",
      "packed", "label", "tape", "flat pack", "flatpack", "shadow", "cardboard cutout"),
     2),
    ("car-battery",
     ("car battery", "car batteries", "van battery", "leisure battery", "motorcycle battery"),
     "A garage will take the old one when it fits a new one, and a scrap dealer or a metal "
     "merchant buys it by weight, so it is worth a few pounds rather than a trip to the tip - "
     "which takes them too. Never put it in the bin or leave it in the garage for years: it holds "
     "acid and lead.",
     ("flat", "flat battery", "wont start", "won't start", "jump", "jump start", "charging",
      "charge", "charger", "dies", "dying", "last", "lasts", "life", "how long", "replace",
      "replacement", "test", "cold weather", "warning light")),
    ("medicines",
     ("medicine", "medicines", "tablets", "pills", "capsules", "old medicine", "unused medicine",
      "medical waste", "syringe", "inhaler", "antibiotics", "painkillers", "antidepressants",
      "old tablets", "leftover tablets", "unused tablets", "expired tablets", "old pills",
      "leftover medicine", "insulin pen", "epipen"),
     "Take them back to a pharmacy: every pharmacy takes unwanted medicines for safe disposal, and "
     "you do not need to explain. Don't flush them and don't bin them - they reach the water "
     "supply, and a child or a pet can find them. Leave them in their packet with the label on, "
     "and put a used inhaler in with them rather than in the bin.",
     ("im going to", "going to", "gonna", "plan to", "skip", "skips", "skipping", "stopped",
      "stopping", "stop taking", "come off", "coming off", "cut down", "cutting down", "halve",
      "halving", "half", "reduce", "reducing", "increase", "increasing", "double", "doubling",
      "extra dose", "change my dose", "my dose", "taper", "wean", "instead of",
      "can i take", "should i take", "safe to take", "ok to take", "take one", "take two",
      "take them", "take it", "take with", "take for", "still taking", "dose", "dosage",
      "side effect", "side effects", "how many", "overdose", "missed", "forgot", "forget",
      "headache", "headaches", "head ache", "migraine", "migraines", "ache", "aches", "aching",
      "pain", "pains", "painful", "sore", "toothache", "tooth ache", "stomach ache", "earache",
      "back pain", "period pain", "cramp", "cramps", "hurt", "hurts", "ill", "unwell",
      "symptom", "symptoms", "cure", "relief", "relieve", "ease", "calm down",
      "cold", "flu", "cough", "colds", "infection", "sick", "sickness", "fever", "temperature",
      "hangover", "allergy", "allergies", "hayfever", "hay fever", "insect bite", "sting")),
    ("mattress",
     ("mattress", "mattresses", "old bed", "bed frame", "divan", "headboard"),
     "Book a bulky waste collection with your council - most charge twenty to forty pounds and "
     "collect from the doorstep - or take it to the recycling centre, where it is stripped for its "
     "springs. Charity shops rarely take one for hygiene reasons, so a free-ad site is the other "
     "realistic route if it is clean and you say collection only.",
     ("cost", "costs", "price", "prices", "buy", "buying", "best", "which", "decent", "clean",
      "cleaning", "stain", "stains", "wash", "smell", "smells", "size", "firm", "soft")),
    ("fridge",
     ("fridge", "freezer", "fridge freezer", "chest freezer"),
     "A fridge or freezer holds refrigerant gas that has to be taken out by someone equipped for "
     "it, so it can never go out with the rubbish. The shop selling you the new one has to take the "
     "old one away on a like-for-like basis, often free or for a small fee, and the recycling "
     "centre takes it. Take the doors off before it leaves the kitchen if children or pets will be "
     "near it.",
     ("cold", "not cold", "freezing", "repair", "fix", "fixing", "smells", "smell",
      "noisy", "noise", "frost", "temperature", "ice", "not working", "wont", "won't", "leaking",
      "installing", "install", "second hand",
      "cheese", "butter", "yoghurt", "yogurt", "leftovers", "bacon", "ham",
      "eggs", "raw meat")),
    ("white-goods",
     ("washing machine", "washer", "tumble dryer", "dryer", "dishwasher", "oven", "cooker",
      "microwave", "hob", "fridge unit"),
     "The shop delivering a new one has to take the old one away on a like-for-like basis, and "
     "some charge a small fee for it, so ask when you buy. Otherwise the tip has a skip for white "
     "goods, or a scrap dealer collects for the metal - and a machine that still works will go on "
     "a free-ad site in a day. Unplug it, drain the water out of the filter, and tape the door "
     "shut before it leaves the kitchen.",
     ("clean", "cleaning", "descale", "limescale", "smell", "smells", "smelly", "musty", "filter",
      "mould", "mold", "mouldy", "moldy", "mildew", "black mould", "black mold",
      "not draining", "wont drain", "won't drain", "not spinning", "wont spin", "won't spin",
      "repair", "fix", "faulty", "not working", "broken", "error", "install", "installing",
      "plumb", "plumbing", "leaking", "leak", "noisy", "banging",
      "grind", "grinds", "grinding", "scrap", "scrapes", "scraping", "rattle", "rattles",
      "rattling", "squeak", "squeaks", "squeaking", "squeal", "squeals", "squealing",
      "thump", "thumping", "knock", "knocking", "vibrate", "vibrating", "shaking",
      "how often", "which", "best",
      "buy", "buying", "bake", "baking", "roast", "cook", "cooking", "preheat", "temperature",
      "fan oven", "self clean"),
     2),
    ("bulbs",
     ("light bulb", "light bulbs", "bulb", "bulbs", "halogen", "fluorescent", "cfl", "led bulb",
      "led bulbs", "strip light", "tube light"),
     "Old-style filament and halogen bulbs are just glass and wire, so they go in the bin. The "
     "coiled low-energy ones hold a little mercury: take those to the tip or to a shop that sells "
     "them. If one breaks, air the room for fifteen minutes, don't vacuum, and wipe it up with a "
     "damp paper towel. LEDs are electronics, so they belong with the small appliances at the tip.",
     ("change", "changing", "replace", "replacement", "fitting", "watt", "watts", "bright",
      "brighter", "dimmable", "flicker", "flickering", "not working", "blown", "which", "best",
      "warm white", "energy")),
    ("electricals",
     ("tv", "television", "telly", "laptop", "computer", "pc", "monitor", "printer", "kettle",
      "toaster", "hoover", "vacuum cleaner", "phone", "mobile", "mobile phone", "old phone",
      "iphone", "tablet", "ipad", "charger", "cable", "electricals", "electronics", "appliance",
      "appliances", "game console", "xbox", "playstation"),
     "Anything with a plug, a battery or a cable is electrical waste and can't go in the bin. A "
     "shop that sells you a new one has to take the old one back, like for like, and the tip has a "
     "small-appliance skip. Wipe a phone or laptop and take the SIM and memory card out first; a "
     "charity shop or a repair cafe can make use of one that still works.",
     ("limescale", "scale", "descale", "furred", "virus", "viruses", "pop up", "popup", "malware",
      "spyware", "adware", "software", "app", "apps", "update", "browser", "email", "wifi",
      "program", "programs", "uninstall", "uninstalling", "uninstalled", "reinstall",
      "wi-fi", "speed", "slow", "taking ages", "taking so long", "taking long", "is taking",
      "takes ages", "takes forever", "took a", "took one", "took it", "took my",
      "swallow", "swallowed", "pill", "pills",
      "headache", "headaches", "migraine", "migraines", "toothache", "earache", "sore throat",
      "stomach ache", "cramp", "cramps", "nausea", "rash", "itching", "pain", "pains", "aching",
      "hurts", "hurting", "fever",
      "medicine", "dose", "dies", "dying", "lunchtime", "battery life", "cushion", "cushions",
      "tablets", "painkillers", "paracetamol", "ibuprofen", "prescription", "headache",
      "migraine", "symptom", "symptoms", "without tablets", "without pills",
      "contract", "contracts", "bill", "bills", "tariff", "upgrade", "unlock", "network", "sim",
      "number", "account", "cracked", "screen", "not working", "repair", "fix", "warranty",
      "no signal", "slow", "storage", "battery life", "charge", "charging", "watch", "channel",
      "channels", "remote", "print", "printing", "cartridge", "boil", "boiling", "toast",
      "vacuum", "hoovering",
      "recycle bin", "recycling bin", "trash can", "trash", "empty the trash", "deleted",
      "delete", "folder", "folders", "files", "desktop",
      "dust", "dusty", "dusted", "cobweb", "cobwebs", "settling", "smear", "smears",
      "smudges", "fingerprints", "polish", "polishing", "wipe", "wiping", "cleaning",
      "clean the")),
    ("clothes",
     ("clothes", "clothing", "old clothes", "shoes", "trainers", "coats", "jumpers", "textiles",
      "rags", "bedding", "duvet", "pillows", "towels",
      "socks", "sock", "pants", "underwear", "knickers", "bras", "gloves", "scarves", "hats",
      "sheets", "curtains", "fabric", "linen", "blankets", "slippers", "boots", "sandals"),
     "Charity shops, the clothes banks in car parks and the textile skip at the tip take anything "
     "wearable. Worn-out fabric still earns its place in a textile bank, where it becomes rags or "
     "stuffing, so a bag of split trousers is not waste. Wash it first, put shoes in pairs, and a "
     "duvet or pillow that is past it goes to the textile bank rather than the bin.",
     ("dog", "dogs", "cat", "cats", "pet", "pets", "died", "dies", "passed away", "gone",
      "kid", "kids", "child", "children", "baby", "hospital", "his", "her bed",
      "wash", "washing", "shrink", "shrank", "stain", "stains", "iron", "ironing", "fit", "size",
      "wear it", "wear them", "to wear",
      "smell", "smells", "dry", "drying", "hole", "holes", "repair", "refashion",
      "style", "outfit", "what to wear",
      "static", "static electricity", "clinging", "cling", "moth", "moths", "mothball",
      "mothballs", "lint", "bobbles", "bobbling", "pilling", "pills",
      "chewing gum", "gum", "oil", "grease", "paint", "ink", "blood", "wine", "coffee", "tea",
      "chocolate", "mud", "grass", "marker", "pen", "sick", "vomit", "wee", "urine",
      "out of my", "off my", "off the", "out of the",
      "flower bed", "flower beds", "flowerbed", "garden", "gardens", "lawn", "lawns", "border",
      "borders", "allotment", "allotments", "weed", "weeds", "weeding", "plant", "plants",
      "shrub", "shrubs", "rose", "roses", "tomato", "tomatoes", "greenhouse", "compost")),
    ("furniture",
     ("sofa", "couch", "settee", "armchair", "wardrobe", "table", "chairs", "bookcase",
      "furniture", "sideboard", "dresser", "desk", "cabinet"),
     "Three routes: a council bulky waste collection (usually charged), the tip if you can drive it "
     "there, or a charity that collects - the British Heart Foundation takes sofas and wardrobes "
     "free if they have their fire labels and can come down the stairs. A free-ad site clears most "
     "furniture within a week if you say collection only.",
     ("cushion", "cushions", "new", "replacement", "cover", "covers", "which", "start",
      "not comfortable", "uncomfortable", "wobbly", "squeaks", "squeaking",
      "moths", "moth", "mice", "mouse", "rats", "ant", "ants", "flies", "bedbugs", "woodworm",
      "mould", "mold", "damp", "silverfish", "cockroach", "spiders",
      "mark", "marks", "water mark", "water marks", "ring", "rings", "heat mark", "scratch",
      "scratches", "dent", "dents", "gouge", "chipped", "polish", "polishing",
      "clean", "cleaning", "stain", "stains", "smell", "smells", "upstairs", "delivery",
      "assemble", "assembling", "flat pack", "cover", "repair", "buy", "buying", "best",
      "which", "arrange", "layout", "small room")),
    ("books",
     ("book", "books", "old books", "paperback", "paperbacks", "novels", "textbooks",
      "magazines", "comics", "encyclopaedias", "encyclopedias", "cookbooks", "book shelf",
      "bookshelf", "bookcase full of books"),
     "Ring the charity shop before you load the car: most take a bag or two of books and say no "
     "to a bootful, and a book bank at the tip or a supermarket car park takes as many as you "
     "have. Paperbacks go down well at a hospital, a care home or a phone box library, and a "
     "school fair clears children's books. Anything mouldy, damp or water-damaged goes in the "
     "paper recycling, not to a shop.",
     ("book a", "book the", "reserve", "reservation", "table", "hotel",
      "flight", "flights", "train", "tickets", "appointment", "read", "reading", "reads",
      "recommend", "recommendation", "recommendations", "what book", "which book", "good book",
      "best book", "books for", "book for", "kindle", "e reader", "e-reader", "audiobook",
      "library", "borrow", "store", "storage", "shelf", "shelves", "display")),
    ("toys",
     ("toy", "toys", "old toys", "lego", "duplo", "playmobil", "teddy", "teddies",
      "cuddly toys", "soft toys", "dolls", "action figures", "train set", "board games",
      "jigsaws", "puzzles", "childrens toys", "kids toys"),
     "Charity shops take toys only if they are complete and clean, so a nursery, a sure start "
     "centre or a refuge will take what a shop will not, and a free-ad site clears a box of lego "
     "in a day. Wash what you have and put the pieces back in their boxes first. A car seat or a "
     "cot is the exception: charity shops cannot take them, so it goes to the tip unless a "
     "friend wants it, and broken plastic is general waste.",
     ("buy", "buying", "best", "which", "for a 3", "for a 2", "for a 4", "for a 5",
      "year old", "years old", "gift", "present", "birthday", "christmas", "play with",
      "clean", "cleaning", "sterilise", "wash", "smell", "recall", "safety", "choking",
      "store", "storage", "tidy", "organise", "floor")),
    ("bikes",
     ("bike", "bikes", "bicycle", "bicycles", "old bike", "kids bike", "childs bike",
      "mountain bike", "push bike"),
     "A bike project or a charity that refurbishes them takes one that does not ride: Re-Cycle "
     "and most city bike workshops want frames and parts, and a free-ad listing marked "
     "collection only clears one in a day. A scrap dealer buys the frame by weight, and the tip "
     "takes it with the metal. Charity shops rarely take bikes, so ring the project first.",
     ("ride", "riding", "rider", "buy", "buying", "which", "best", "cheap", "repair",
      "fix", "mend", "puncture", "tyre", "tyres", "chain", "brakes", "gears", "saddle",
      "lock", "helmet", "lights", "electric", "e-bike", "how far", "how long", "train",
      "lose weight", "fitness", "commute", "storage", "store", "shed", "carrier")),
    ("polystyrene",
     ("polystyrene", "styrofoam", "packaging", "packing peanuts", "bubble wrap"),
     "The white beaded stuff (expanded polystyrene) is not collected at the kerbside in most "
     "places, so it goes in the general waste - break it up so it takes less room, and put the "
     "pieces in a bag so they don't blow about. A few tips take it if you check your council's A "
     "to Z page, and the hard plastic trays often go in with the plastics.",
     ("cook", "cooking", "food", "insulate", "insulation", "sound", "noise", "craft", "paint",
      "glue", "fix", "filler")),
    ("oil",
     ("cooking oil", "used oil", "frying oil", "old oil", "chip pan", "deep fryer", "fat",
      "grease", "lard", "turkey fat", "bacon fat"),
     "Let it cool, pour it into a bottle or a tub, and put that in the general waste - never down "
     "the sink, where it sets with wipes into a blockage. A little fat can go in the food waste "
     "caddy if your council collects one, and a recycling centre takes larger amounts of used "
     "cooking oil.",
     ("belly", "lose", "losing", "burn", "burning", "diet", "weight", "body", "stomach", "abs",
      "waist", "tummy", "thigh", "thighs", "hips", "flabby", "fat around", "fat round",
      "bingo wings", "muffin top", "spot reduce", "calories",
      "reduce", "cut down", "best", "healthy", "healthiest", "which oil", "olive", "rapeseed",
      "smoke point", "temperature", "how hot", "calories", "reuse", "reusing", "use again",
      "sink", "blocked", "drain", "smell",
      "clothes", "clothing", "shirt", "shirts", "trousers", "jeans", "dress", "dresses",
      "jumper", "jumpers", "top", "tops", "t shirt", "tshirt", "hoodie", "cardigan", "coat",
      "jacket", "fabric", "carpet", "rug", "sofa", "settee", "couch", "upholstery", "floor",
      "tiles", "wall", "walls", "worktop", "drive", "driveway", "patio", "shoes", "trainers")),
    ("garden-waste",
     ("garden waste", "grass cuttings", "prunings", "hedge cuttings", "branches",
      "fallen leaves", "dead leaves", "autumn leaves", "leaves in the garden",
      "leaves in my garden", "leaves from the garden", "leaves from my garden",
      "leaves on the lawn", "leaves on my lawn", "rake the leaves", "raked leaves",
      "leaf litter", "bag of leaves", "bags of leaves", "get rid of leaves",
      "lawn clippings", "green waste", "compost",
      "green bin", "green bins", "in the green bin", "brown bin", "brown bins",
      "in the brown bin", "green wheely bin", "garden waste bin"),
     "The council's green bin is the cheapest route if you have one - many charge for the "
     "subscription and collect fortnightly - and the tip has a green waste skip. Grass, leaves and "
     "prunings can go in a compost bin at home too, but leave out cooked food, weeds in seed and "
     "anything diseased.",
     ("compost bin", "how to compost", "composting", "bin smells", "smell", "rats", "flies",
      "what goes in", "what can go in", "what can i put in", "recycling", "card and paper",
      "when to cut", "cut back", "prune", "pruning", "mow", "mowing", "lawn",
      "brown tips", "brown at the tips", "tips of the leaves", "leaf edges", "houseplant",
      "houseplants", "indoor plant", "pot plant", "yellow leaves", "yellowing")),
    ("christmas-tree",
     ("christmas tree", "real tree", "xmas tree", "old christmas tree"),
     "Councils collect real trees in the first couple of January weeks and shred them for mulch - "
     "check the day on the council's site, and strip the decorations and the stand first. Garden "
     "centres often take them back, and one that still has its roots in a pot can be planted out "
     "instead.",
     ("decorate", "decorating", "lights", "when should i put up", "take down", "artificial",
      "which tree", "buy", "best", "price", "cost", "needle", "needles", "drop", "dropping")),
    ("chemicals",
     ("chemicals", "weedkiller", "bleach", "white spirit", "thinners", "paint thinner",
      "pesticide", "antifreeze", "drain cleaner", "caustic soda", "ammonia", "old petrol",
      "paraffin", "gas bottle", "gas canister", "camping gas"),
     "Anything with a hazard symbol on it is household chemicals, and the tip's hazardous waste "
     "skip is where it goes - most sites take it from householders, and a few councils run set "
     "days, so ring before you drive over. Keep it in its own labelled container, never mix two "
     "together, and never pour it down the drain or into the bin. A gas bottle goes back to the "
     "shop that sells them.",
     ("mix", "mixing", "how much", "dose", "use", "using", "safe", "dangerous", "fumes", "smell",
      "kill", "weeds", "mould", "mold", "clean", "cleaning", "drain", "blocked", "unblock",
      "stain", "stains", "toilet", "sink", "shower", "grout")),
    ("mirror",
     ("mirror", "mirrors", "pyrex", "glass dish", "drinking glass", "window glass", "broken glass",
      "vase", "ceramic", "crockery", "plate"),
     "Mirrors, Pyrex and drinking glasses are not bottle-bank glass: they are made to take heat, so "
     "they melt at a different temperature and spoil the batch. Wrap it so nobody cuts themselves "
     "and put it in the general waste, or take it to the tip.",
     ("clean", "hang", "hanging", "mount", "steam", "streak", "smear", "smears", "crack", "chipped",
      "replace", "which glass", "wine glass", "bake", "baking", "ovenproof", "cut", "cutting")),
    ("aerosols",
     ("aerosol", "aerosols", "spray can", "spray cans", "deodorant can", "hairspray", "paint spray",
      "wd40", "wd-40"),
     "An empty aerosol can go in the kerbside recycling with the tins in most areas - check the "
     "council's list, and don't pierce or crush it. One that still has something in it is not "
     "rubbish: it goes to the tip, and a spray paint or a solvent goes to the hazardous waste.",
     ("use", "using", "safe", "dangerous", "explode", "heat", "hot", "cold", "spray",
      "spraying", "paint", "paint the", "squeak", "squeaky", "hinge", "rust", "lock")),
)

BIN_DAY = (
    "Your council's bin-day page will say: put your postcode in and it gives the day for your "
    "street, and that is the only place that is right, because bank holidays and ice move a round "
    "by a day or two and the paper calendar on the fridge goes stale. If it says tomorrow, put it "
    "out tonight; either way it has to be out by about 6.30 in the morning, so the night before is "
    "safest, and it comes back in the same day. If it is missed, report it on the council's "
    "missed-bin form that day rather than ringing - it is free and the round usually comes back "
    "within two working days."
)

BIN_DAY_KEY = (
    ("bin day", "bins out", "bin out", "the bins out", "put my bin out", "put the bin out",
     "put the bins out", "put my bins out", "put the rubbish out", "put my rubbish out",
     "put the recycling out", "put the green bin out", "bins go out", "bin goes out",
     "collection day", "collection days", "bin collection", "bins collected",
     "bin collected", "bins are collected", "bin is collected", "bins emptied",
     "bin emptied", "bins are emptied", "bin men", "bin lorry", "bin round", "bin crew",
     "wheelie bin day", "recycling collected", "recycling is collected", "recycling emptied",
     "recycling collection", "rubbish collected", "rubbish is collected", "rubbish collection",
     "refuse collection", "garden waste collection", "my recycling", "my rubbish"),
    ("when", "what time", "what day", "which day", "what days", "how often", "find out",
     "check", "due", "should i put", "do i put", "am i supposed to put", "is it",
     "are they", "know",
     "changed", "changes", "has changed", "have changed", "change of",
     "has moved", "moved to", "moved day", "collection moved", "bin day moved",
     "swapped", "rescheduled", "new day", "different day", "which morning", "what morning"),
)

BIN_DAY_AVOID = (
    "smell", "smells", "smelly", "stink", "stinks", "maggots", "wash", "clean", "cleaning",
    "rats", "rat", "mice", "mouse", "fox", "foxes", "seagull", "seagulls", "cat", "cats",
    "missed", "wasnt collected", "wasn't collected", "not collected", "didnt collect",
    "didn't collect", "havent collected", "haven't collected", "still there", "overflowing",
    "where do i put", "where can i put", "which bin", "what goes in", "what can i put in",
    "can i put", "how do i get rid", "get rid of", "tip", "recycling centre", "lid", "bags",
    "bin bags", "bin bag", "lock", "key", "replace", "buy", "size", "how big",
)

WHICH_BIN = (
    "That depends on the item: anything with a plug or a battery goes back to a shop or the tip, "
    "chemicals go to the tip's hazardous skip, and bulky things are a council collection. Which "
    "item is it?"
)

ITEM_ROUTES = (
    ("tins", ("tin", "tins", "tin can", "tin cans", "cans", "drink can", "drink cans",
              "food tin", "food tins", "baked bean tin", "soup tin", "pet food tin", "aluminium"),
     "Tins and cans go in the kerbside recycling: rinse them, leave them whole and push the lid "
     "inside, and do not flatten them - the plant sorts steel from aluminium, and a flattened tin "
     "can be read as the wrong metal. An aerosol is the one can that goes back to a shop or the "
     "tip if it still has something in it."),
    ("foil", ("foil", "tin foil", "kitchen foil", "foil tray", "foil trays", "foil container",
              "bacofoil"),
     "Clean foil goes in the kerbside recycling, scrunched into a ball about the size of a fist so "
     "the machine can pick it out - loose foil and a foil tray with food stuck to it do not get "
     "sorted, and a greasy one goes in the general waste."),
    ("jars and bottles", ("jar", "jars", "glass jar", "glass jars",
                          "glass bottle", "glass bottles", "wine bottle", "beer bottle",
                          "jam jar", "sauce jar"),
     "Glass jars and bottles go in the kerbside recycling: empty and rinsed, lids off, and the "
     "lids go in with the metal if they are metal. Drinking glasses, Pyrex and ovenware are a "
     "different glass and go in the general waste, because they melt at the wrong temperature."),
    ("paper and card", ("paper", "newspaper", "newspapers", "card", "cardboard", "carton",
                        "cartons", "junk mail", "envelope", "envelopes", "magazine",
                        "magazines", "cereal box", "cereal boxes"),
     "Paper and card go in the kerbside recycling, flattened and dry: envelopes with a window, "
     "cereal boxes and junk mail all go in. A food carton or a tetra pak is only collected where "
     "the council says so, and a greasy pizza box goes in the general waste apart from its clean "
     "lid."),
    ("plastic bottles and tubs", ("plastic bottle", "plastic bottles", "bottle", "bottles",
                                  "tub", "tubs", "yoghurt pot", "yoghurt pots", "margarine tub",
                                  "plastic tub", "plastic tubs", "milk bottle", "shampoo bottle"),
     "Plastic bottles and tubs go in the kerbside recycling: rinse them, squash the bottles, and "
     "leave the lids on or off as your council says, because both are collected in most places "
     "now. A black plastic tray is the one that is often not sorted, and your council's A to Z "
     "page will say."),
    ("soft plastic", ("crisp packet", "crisp packets", "carrier bag", "carrier bags",
                      "plastic bag", "plastic bags", "bread bag", "film lid", "cling film",
                      "bubble wrap", "soft plastic", "padded envelope"),
     "Soft plastic - carrier bags, crisp packets, bread bags, film lids, bubble wrap - is not "
     "collected at the kerbside in most places. The big supermarkets take it in a bin by the door, "
     "and the collected plastic is turned into bin bags and pellets. A padded envelope is the "
     "same, and it is worth keeping a bag by the door for it."),
    ("polystyrene", ("polystyrene", "styrofoam", "packing peanuts", "meat tray", "meat trays",
                     "takeaway box", "takeaway boxes"),
     "Polystyrene goes in the general waste, not the recycling: expanded foam is mostly air, and "
     "no kerbside service takes it. A clean meat tray is the exception in some areas because some "
     "trays are the recyclable kind - squeeze it, and if it springs back it is foam and goes in "
     "the bin."),
    ("nappies", ("nappy", "nappies", "diaper", "diapers", "baby wipes", "wet wipes",
                 "sanitary", "sanitary pad", "sanitary pads", "tampon", "tampons", "incontinence"),
     "Nappies, wipes, pads and tampons all go in the general waste - nothing absorbent is "
     "recycled, and a wet wipe is not flushable however the packet reads, because it does not "
     "break down and it is most of what blocks a sewer. Bag it and bin it; a nappy bin with a lid "
     "keeps the room livable."),
    ("clothes and textiles", ("clothes", "clothing", "old clothes", "textiles", "textile",
                              "shoes", "old shoes", "curtains", "bedding", "duvet", "duvets",
                              "towels", "rags"),
     "Clothes, shoes, bedding and curtains do not go in the kerbside bin: the charity bank or the "
     "textile bank at the supermarket car park takes them, even worn ones, and they are sorted into "
     "resale, rags and fibre. A duvet and a pillow are the awkward ones - most banks will not take "
     "them, so ring the council for a bulky collection or take them to the tip's textile container."),
)


def _the_item_named(line):
    words = " %s " % str(line or "").lower().replace("\u2019", "'")
    for name, spellings, said in ITEM_ROUTES:
        if any((" %s " % spelling) in words for spelling in spellings):
            return said
    return None


def _a_bin_for_the_item(memory, understood):
    if isinstance(understood, dict):
        said = _the_item_named(understood.get("text") or understood.get("clean") or "")
        if said:
            return said
    return WHICH_BIN


WHICH_BIN_AVOID = (
    "collection", "collected", "collection day", "missed", "empty", "emptied", "smell", "smells",
    "rats", "mice", "fox", "foxes", "seagull", "seagulls", "bags", "lid", "wheelie",
    "what goes in", "how often", "bins out", "bin out", "put the bins", "the bins out",
    "bin day", "what time", "tonight", "tomorrow", "this morning", "last night",
    "recycling bin",
    "tips of", "brown tips", "white tips", "split ends", "dry tips",
    "fingertips", "finger tips", "nails", "hair", "plant", "plants", "leaves",
)

RECYCLE = (
    "Roughly: flattened card and paper, glass jars and bottles, tins and cans, plastic bottles and "
    "tubs, and clean foil - rinsed, loose rather than bagged, because a bag of the right things "
    "still goes to waste. Soft plastic (carrier bags, crisp packets, film lids) is not collected "
    "at the kerbside in most places: the big supermarkets take it in a bin by the door. For "
    "anything odd, the council's A to Z page has a line for it."
)

RECYCLE_AVOID = (
    "first aid", "kit", "sandwich", "lunch", "lunchbox", "picnic", "stocking", "stockings",
    "hamper", "hospital bag", "empty", "emptied", "computer", "laptop", "windows", "mac",
    "file", "files", "desktop", "disk", "drive", "deleted", "delete", "restore", "email",
    "folder", "folders", "phone",
    "hard drive", "bin day", "bins out", "put the bins", "collection day", "what time",
    "bin smells", "smell", "smells", "limescale", "phone contract",
) + A_HOURS_ASK

TIP = (
    "Load it so it can be tipped in one go, and put the awkward things on top: a car load usually "
    "drives straight in, but many sites ask for proof of address, and a van or a trailer is often "
    "booked. Paint, chemicals, gas bottles, batteries and anything with a screen go to a staffed "
    "container or to a steward rather than into a skip, so ask at the gate. Soil, rubble and "
    "plasterboard are usually limited to a few bags a visit."
    " If you cannot drive it there, the council's bulky waste collection is the other route: "
    "usually charged, booked online or by phone, and they take it from the doorstep."
)

TIP_AVOID = (
    "any tips", "tips for", "tip in", "tip on", "the waiter", "waitress", "restaurant", "pub",
    "percent", "gratuity", "tidy", "garden tip",
    "work out a tip", "work out the tip", "work out a service", "work out the service",
    "how do i tip", "how to tip", "how should i tip",
    "buried", "bury", "burying", "instead of", "ended up",
    "how much", "cost", "charge", "price", "open", "closing", "opening", "what time", "close",
    "calculate a tip", "calculate the tip", "calculate a service", "calculate the service",
    "how much should i tip", "how much do i tip",
    "nearest", "where is", "council tax", "holiday", "bank holiday",
    "tips of", "brown tips", "white tips", "split ends", "dry tips",
    "fingertips", "finger tips", "nails", "hair", "plant", "plants", "leaves",
)

def _not_a_cook_ask(understood):
    return not cook_ask(understood)



_CONTAINERS = sorted({name for item in ITEMS for name in item[1]}, key=len, reverse=True)
PUT_INTO = re.compile(
    r"\b(?:put|puts|putting|place|places|placing|keep|keeps|keeping|store|stores|storing|add|"
    r"adding|load|loading|pour|pouring|stick|sticking|poke|poking|stand|standing)\b"
    r"[^.;?!]{0,40}?\b(?:in|into|inside|on|onto|under|behind|beside|near)\s+"
    r"(?:the\s+|my\s+|our\s+|a\s+|an\s+|your\s+|its\s+)?(?:%s)\b"
    % "|".join(re.escape(name) for name in _CONTAINERS))


def _said(understood):
    if not isinstance(understood, dict):
        return ""
    return str(understood.get("plain") or understood.get("clean")
               or understood.get("norm_text") or "")


def _not_a_container(understood):
    return not PUT_INTO.search(_said(understood).lower())


PLACEMENT = re.compile(
    r"\bwhere\s+(?:do|does|can|could|should|shall|would)\s+(?:i|we|you|it)\s+put\b"
    r"|\bwhere\s+to\s+put\b|\bwhere\s+i\s+put\b")
ONLY_A_MACHINE = ("rinse aid", "rinse-aid", "fabric softener", "descaler")
A_MACHINE = re.compile(r"\b(?:dishwasher|dish washer|washing machine|washer|washer dryer|"
                       r"washer-dryer|dishdrawer|dish drawer|tumble dryer|tumble drier|dryer)\b")
CONSUMABLE = ("salt", "tablet", "tablets", "powder", "detergent", "rinse aid", "rinse-aid",
              "pod", "pods", "capsule", "capsules", "softener", "descaler")


def _a_consumable_is_placed(understood):
    said = _said(understood).lower()
    if not PLACEMENT.search(said):
        return False
    if any(word in said for word in ONLY_A_MACHINE):
        return True
    return bool(A_MACHINE.search(said)) and any(word in said for word in CONSUMABLE)


def _disposal_guard(understood):
    return (_not_a_cook_ask(understood) and _not_a_container(understood)
            and not _a_consumable_is_placed(understood))


ENTRIES = [
    entry("dispose-" + item[0], (item[1], RID), item[2],
          avoid=item[3] + CURING_ASIDE + NOT_RUBBISH,
          bias=item[4] if len(item) > 4 else 1, guard=_disposal_guard,
          ask=item[5] if len(item) > 5 else ())
    for item in ITEMS
] + [
    entry("dispose-which-bin", (BIN_WORDS, BIN_ASK), _a_bin_for_the_item,
          avoid=WHICH_BIN_AVOID, bias=-1),
    entry("recycle-what-goes-where",
          (("recycle", "recycling", "recycled", "what goes in", "landfill"),
           ("what", "which", "how", "sort", "sorting", "goes", "go in", "in the", "can i",
            "do i")),
          RECYCLE, avoid=RECYCLE_AVOID, bias=-1),
    entry("bin-day", BIN_DAY_KEY, BIN_DAY, avoid=BIN_DAY_AVOID, bias=2),
    entry("dispose-tip-visit",
          (("the tip", "a tip", "to the tip", "tip run", "recycling centre", "household waste site",
            "the dump",
            "council tip", "council dump", "council recycling centre", "council recycling center"),
           ("what", "take", "bring", "need", "allowed", "can i", "how", "load", "van",
            "go", "goes", "going", "collection", "bulky", "worth")),
          TIP, avoid=TIP_AVOID, bias=2),
    entry("find-your-tip",
          (("local tip", "my local tip", "nearest tip", "closest tip", "tip near me",
            "council tip near me", "where is the council tip", "wheres the council tip",
            "where is my council tip", "the council tip near me",
            "the tip near me", "tip local to me", "where is the tip", "where is my tip",
            "where is the dump", "the dump near me", "local dump", "nearest dump",
            "local recycling centre", "local recycling center", "nearest recycling centre",
            "nearest recycling center", "recycling centre near me", "recycling center near me",
            "closest recycling centre", "household waste site near me", "household waste near me",
            "find a tip", "find the tip", "find a recycling centre", "find the recycling centre",
            "find the dump", "which tip", "which recycling centre", "my nearest tip",
            "dump near me"),
           ("where", "how", "find", "nearest", "closest", "local", "near me", "near",
            "look up", "search", "which", "is my", "the")),
          ("Put your postcode into your council's recycling centre page - searching your "
           "postcode and \"recycling centre\" lands on it, and gov.uk links every council's site "
           "finder - and that page has the opening hours, what the site takes and whether you "
           "have to book. Take something that proves you live in the area, because most sites "
           "check it at the gate, and book a slot first if your council runs a booking system, "
           "which the busiest ones do at weekends."), bias=3,
          avoid=("any tips", "tips for", "tip in", "tip on", "the waiter", "waitress",
                 "restaurant", "pub", "percent", "gratuity", "work out a tip", "how do i tip",
                 "how to tip", "how should i tip", "how much", "cost", "charge", "price",
                 "open", "closing", "opening", "what time", "close", "council tax", "holiday",
                 "bank holiday", "service charge", "tattoo", "barber", "hairdresser",
                 "closed", "is closed", "is shut", "shut",
                 "says", "said", "told me", "they say", "they said", "reckons", "apparently")),
    entry("tip-charges",
          (("the tip", "a tip", "to the tip", "tip run", "recycling centre", "household waste",
            "the dump", "council tip"),
           ("cost", "costs", "charge", "charges", "charged", "free", "pay", "how much", "price",
            "fees", "fee", "rubble", "tyres", "tyre", "plasterboard", "soil", "hardcore",
            "diy", "van", "trailer", "permit")),
          ("Household rubbish is free at a council tip; what they charge for is the DIY waste - "
           "rubble, soil, plasterboard, old tyres and sometimes garden waste - and the price is "
           "set by your council, so check its page for your site before you load the car. Vans "
           "and trailers usually need a permit booked in advance, and a few sites want proof you "
           "live in the area."), bias=3,
          avoid=("any tips", "tips for", "how much to tip", "should i tip", "the waiter",
                 "restaurant", "percent", "gratuity",
                 "service charge", "discretionary", "difference between", "same as a tip",
                 "is a tip", "the bill", "on the bill", "tattoo", "hairdresser", "barber",
                 "sofa", "settee", "couch", "armchair", "furniture", "wardrobe", "mattress",
                 "bed", "table", "chairs", "bulky", "charity", "fridge", "freezer",
                 "washing machine", "cooker", "tumble dryer", "dishwasher",
                 "can i take", "can i bring", "can i put", "what can i take", "what can i bring",
                 "allowed", "am i allowed", "what goes", "what do you take", "will they take",
                 "do they take", "accept")),
]
