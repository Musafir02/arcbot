import re

from ..understanding.car_glass import a_window_on_a_car_is_not_a_damage
from ..understanding.cars import no_broken_car, no_broken_car_or_none
from .lookup import asks_how_often, entry as _raw_entry, the_line

REPAIR_COST = ("Garage labour is usually £50 to £90 an hour, and a job is priced by the hours "
               "the book allows rather than by what the car is worth: a clutch is £300 to £800 "
               "fitted, a cambelt £250 to £500, a wheel bearing £150 to £300. Ask for the price "
               "in writing with parts and labour split, and get a second quote for anything over "
               "£300.")


PARKING_TICKET = ("Do not ignore it. If it is a council Penalty Charge Notice, challenge it "
                  "informally within 14 days with photos and the reason, and if that fails make a "
                  "formal representation within 28 days of the Notice to Owner. Paying within 14 "
                  "days usually gets a 50% discount. Keep every letter and use the council's own "
                  "form, not a paid appeals firm.")

PARKING_TICKET_IS = ("A penalty charge notice is a council ticket for breaking a parking or "
                     "traffic rule - no ticket, overstaying, a bus lane, a box junction - and it "
                     "is a civil matter, so it is argued with the council's own process rather "
                     "than in a court. " + PARKING_TICKET)


ROAD_CHARGE = ("A congestion charge zone is a flat daily charge for driving into a set area, "
               "not a toll for each crossing: in London the Congestion Charge is £15 a day, "
               "07:00-18:00 Monday to Friday and 12:00-18:00 at weekends and on bank holidays, "
               "with nothing to pay between 25 December and 1 January. A petrol car older than "
               "Euro 4 or a diesel older than Euro 6 also pays the ULEZ, £12.50 a day, every day "
               "except Christmas Day.")

ROAD_CHARGE_PRICE = ("£15 a day for the London Congestion Charge, from 07:00 to 18:00 Monday to "
                     "Friday and 12:00 to 18:00 at weekends and on bank holidays, and nothing "
                     "between 25 December and 1 January. A car that is not ULEZ compliant pays "
                     "another £12.50 a day on top of that.")

ROAD_CHARGE_ULEZ_PRICE = ("£12.50 a day for the London ULEZ, every hour of every day except "
                          "Christmas Day, and only for a car that misses the standard - petrol "
                          "older than Euro 4, diesel older than Euro 6. A compliant car pays "
                          "nothing.")

ROAD_CHARGE_WHO_PAYS = ("The registered keeper of a non-exempt vehicle pays it, and the cameras "
                        "read the number plate, so there is no barrier and nothing to pay at the "
                        "roadside. Exemptions are narrow - a disabled tax class, some historic "
                        "vehicles - and a compliant car pays no ULEZ, so the answer for your own "
                        "car is the TfL checker with its registration.")

ROAD_CHARGE_EXEMPT = ("Only a few vehicles are exempt: a car in the disabled tax class, some "
                      "historic and military vehicles, and whatever the day's rule names - "
                      "everything else pays, so a car pays £15 a day for the Congestion Charge "
                      "and £12.50 for the ULEZ if it misses the standard. TfL lists the "
                      "exemptions, and the checker there reads your own plate.")

ROAD_CHARGE_HOW_TO_PAY = ("Pay by midnight on the third day after the drive, on the TfL site, the "
                          "app or the phone line, or set up Auto Pay so a day in the Congestion "
                          "Charge costs £14 instead of £15.")

ROAD_CHARGE_BIKES = ("Motorbikes and mopeds pay nothing for the London Congestion Charge - they are "
                     "exempt - but the ULEZ does apply, to a motorcycle that is not Euro 3 or "
                     "newer, so a bike still needs checking on the TfL site.")

ROAD_CHARGE_NOT_ALL_DAY = ("No: the London Congestion Charge runs 07:00-18:00 Monday to Friday and "
                           "12:00-18:00 at weekends and on bank holidays, and there is nothing to "
                           "pay outside those hours or between 25 December and 1 January.")

ROAD_CHARGE_CAZ = ("A clean air zone is set by each city, not one national scheme: each council "
                   "picks its own charge, hours and vehicles, usually a flat day rate for a car "
                   "that misses that city's emissions standard, and some cities charge nothing "
                   "for a car and only for vans and lorries. London's ULEZ at £12.50 a day is "
                   "London's alone, so a Birmingham, Bristol or Bath journey is priced by that "
                   "city's zone - each council publishes a checker for the registration.")

ROAD_CHARGE_MISSED = ("A charge missed becomes a penalty charge notice, and that is the expensive "
                      "version: £160 for the London Congestion Charge, £80 if it is paid within 14 "
                      "days, and £180 for the ULEZ, £90 within 14 days. Pay or challenge it in "
                      "writing inside that window with the journey and any proof, and do not "
                      "ignore the letter - the penalty doubles if it is left.")

TOLL = ("A crossing toll is per vehicle, per crossing, and the price depends on the road: the "
        "Dartford Crossing is £2.50 for a car, paid online or by phone by midnight the day "
        "after, the M6 Toll charges at the barrier, about £9 for a car at peak, and the small "
        "Severn and Humber bridges take card or cash at the booth. An unpaid crossing becomes a "
        "penalty notice for the registered keeper.")


_ROAD_CHARGE_MISS_WORDS = ("happens", "if i dont", "if i don't", "dont pay", "don't pay",
                           "missed", "miss", "forgot", "forget", "ignore", "avoid", "fine",
                           "penalty", "pcn", "caught", "late", "not paid", "unpaid")


_ROAD_CHARGE_OTHER_CITIES = ("clean air zone", "clean air zones", "caz", "cazs", "birmingham",
                             "bristol", "bath", "sheffield", "bradford", "portsmouth",
                             "newcastle", "tyneside", "manchester", "glasgow", "edinburgh",
                             "dundee", "aberdeen", "scotland", "oxford", "leeds", "nottingham",
                             "leicester", "caerphilly", "cardiff", "southampton", "brighton",
                             "norwich", "coventry", "york")

_ROAD_CHARGE_PRICE_WORDS = ("how much", "cost", "costs", "price", "prices", "how expensive",
                            "cheapest", "per day", "a day", "daily rate")

_ROAD_CHARGE_PAY_WORDS = ("how do i pay", "how to pay", "how can i pay", "how do you pay",
                          "where do i pay", "when do i pay", "when do i have to pay",
                          "by when", "pay by", "pay for it", "pay it", "auto pay", "autopay",
                          "set up auto", "pay online", "pay by phone", "make a payment")

_ROAD_CHARGE_WHO_WORDS = ("who pays", "who has to", "who needs to", "who is charged",
                          "do i have to", "do i need to", "have to pay", "need to pay",
                          "must i", "should i pay", "do i pay", "who pays", "am i exempt",
                          "is it free", "free", "motorbike", "motorbikes", "motorcycle",
                          "moped", "van pay", "does a van")


def _road_charge(memory, reading):
    said = " ".join(str((reading or {}).get("clean") or "").lower().split())
    if any(word in said for word in ("toll", "dart charge", "dartford crossing", "m6 toll")):
        return TOLL
    if any(word in said for word in ("motorbike", "motorbikes", "motorcycle", "motorcycles",
                                     "moped", "mopeds", "scooter", "scooters")):
        return ROAD_CHARGE_BIKES
    if any(word in said for word in ("24 hours", "24 hour", "all day", "all night", "overnight",
                                     "at night", "through the night")):
        return ROAD_CHARGE_NOT_ALL_DAY
    if any(word in said for word in _ROAD_CHARGE_OTHER_CITIES):
        return ROAD_CHARGE_CAZ
    if any(word in said for word in _ROAD_CHARGE_MISS_WORDS):
        return ROAD_CHARGE_MISSED
    if any(word in said for word in _ROAD_CHARGE_PAY_WORDS):
        return ROAD_CHARGE_HOW_TO_PAY
    if any(word in said for word in _ROAD_CHARGE_PRICE_WORDS):
        if "ulez" in said and "congestion charge" not in said:
            return ROAD_CHARGE_ULEZ_PRICE
        return ROAD_CHARGE_PRICE
    if any(word in said for word in ("exempt", "exemption", "exemptions", "exempt from")):
        return ROAD_CHARGE_EXEMPT
    if any(word in said for word in _ROAD_CHARGE_WHO_WORDS):
        return ROAD_CHARGE_WHO_PAYS
    if "ulez" in said and "congestion charge" not in said:
        return ROAD_CHARGE_ULEZ_PRICE
    return ROAD_CHARGE


def _parking_ticket(memory, reading):
    asks = (reading or {}).get("asks") or ()
    said = " ".join(str((reading or {}).get("clean") or "").lower().split())
    if "definition" in asks and not any(word in said.split() for word in ("my", "our")):
        return PARKING_TICKET_IS
    return PARKING_TICKET

ANSWERS = ("cars",)

_NOT_BUYING_SALE = ("sell", "selling", "sold", "seller", "buyer", "buyers", "viewing",
                    "test drive", "test-drive", "bank transfer", "paypal", "pay pal",
                    "cash on collection", "screenshot", "overpaid", "paid too much",
                    "paid me too much", "courier", "collection only", "marketplace",
                    "trade it in", "trade in", "part exchange", "px")

_NOT_BUYING = ("buy", "buying", "bought", "sell", "selling", "seller", "dealer",
               "second-hand", "second hand", "used", "budget", "finance", "lease",
               "worth", "insurance", "quote", "premium",
               "van hire", "hire a van", "hiring a van", "van to hire", "removal van",
               "removals", "hire cost", "hire price")

ADVISORY_PASS = ("passed", "pass", "advisory", "advisories", "failed nothing",
                 "no advisories", "without advisories")

NOT_BIKE = ("bike", "bikes", "bicycle", "bicycles", "cycle", "cycling", "cyclist", "motorbike",
            "motorbikes", "motorcycle", "moped", "scooter", "e-bike", "ebike",
                 "gcse", "gcses", "college", "sixth form", "a levels", "a level", "school",
                 "university", "ucas")

_NOT_A_TYRE = ("boiler", "boilers", "radiator", "radiators", "heating", "central heating",
               "pipe", "pipes", "pipework", "plumber", "plumbers", "hot water", "tap", "taps",
               "shower", "showers", "immersion", "thermostat", "pressure gauge")

VEHICLE = ("van", "vans", "vehicle", "vehicles", "camper")

MODELS = (
    "ford", "vauxhall", "toyota", "nissan", "volkswagen", "vw", "audi", "bmw", "mercedes",
    "merc", "peugeot", "renault", "citroen", "honda", "hyundai", "kia", "skoda", "volvo",
    "mazda", "suzuki", "fiat", "dacia", "tesla", "lexus", "jaguar", "land rover",
    "range rover", "alfa romeo", "mg",
    "fiesta", "corsa", "astra", "clio", "micra", "punto", "qashqai", "juke", "yaris",
    "picanto", "fabia", "octavia", "passat", "megane", "twingo", "captur", "kuga",
    "mondeo", "jetta", "scirocco", "tiguan", "touran", "sandero", "kangoo", "almera",
    "primera", "berlingo", "lupo", "ibiza", "leon", "cayenne", "defender", "pajero",
)

LEASE_OR_BUY = ("lease or buy", "buy or lease", "lease vs buy", "buy vs lease", "lease versus",
                "lease or purchase", "purchase or lease", "hire purchase or", "or hire purchase",
                "rent or buy", "or pcp", "pcp or", "or a pcp")

DASH_CAM_WHAT = (
    "A dash cam is a small camera on the windscreen that records the road ahead in a loop and "
    "saves the clip on impact, so you have proof after a bump that is not your word against "
    "theirs. Fit one high behind the mirror, feed it from a 12V socket, and use a high-endurance "
    "micro SD card labelled U3 - a cheap card dies after months of constant writing. Many "
    "insurers knock a little off the premium if you tell them you have one.")
DASH_CAM_BUY = (
    "A dash cam records the road ahead in a loop, wiping the oldest clip, so you only keep a "
    "crash by pressing the button or by it saving on impact. For the card: a high-endurance "
    "micro SD of 64GB or 128GB, labelled U3, because a cheap card dies after a few months of "
    "constant writing - that endurance word matters more than the size.")
DASH_CAM_FIT = (
    "Mount it high on the windscreen behind and below the mirror so it sees both kerbs and "
    "does not block your view, run the cable along the headlining and down the door pillar to a "
    "12V socket or a hardwire kit, and keep the lens clean. Check it records after every "
    "service, and tell your insurer - many give a discount for one.")


def _dash_cam(memory, understood):
    text = " ".join(str(part or "") for part in (understood.get("text"),
                                                 understood.get("clean"))).lower()
    if any(word in text for word in ("card", "memory", "sd", "size", "buy", "best", "recommend",
                                     "which", "worth")):
        return DASH_CAM_BUY
    if any(word in text for word in ("what is", "whats a", "what are", "explain", "used for",
                                     "do they do", "how does it work")):
        return DASH_CAM_WHAT
    return DASH_CAM_FIT




WILD_ON_THE_ROAD = ("fox", "foxes", "badger", "badgers", "deer", "pheasant", "pheasants",
                    "hedgehog", "hedgehogs", "hare", "hares", "owl", "owls", "swan", "swans",
                    "squirrel", "squirrels")
LEGAL_ON_THE_ROAD = ("dog", "dogs", "horse", "horses", "cattle", "cow", "cows", "sheep", "pig",
                     "pigs", "goat", "goats", "donkey", "donkeys")
ALL_ON_THE_ROAD = WILD_ON_THE_ROAD + LEGAL_ON_THE_ROAD
ANIMAL_ON_THE_ROAD = tuple(
    phrase % animal
    for animal in ALL_ON_THE_ROAD
    for phrase in ("hit a %s", "ran over a %s", "run over a %s", "%s was hit", "%s was run over",
                   "%s run over", "%s hit by", "knocked a %s", "knocked down a %s", "dead %s"))

_STRUCK = ("hit", "hits", "hitting", "ran", "run", "running", "struck", "dead", "killed",
           "knocked", "caught")


def _an_animal_struck(line):
    said = " %s " % str(line or "").lower()
    if not any(" %s " % animal in said for animal in ALL_ON_THE_ROAD):
        return False
    return any(" %s " % cue in said for cue in _STRUCK)


def _not_a_bike_chat(understood):
    if not isinstance(understood, dict):
        return True
    above = str(((understood.get("leans_on") or {}).get("text")) or "").lower()
    if "cable" not in above:
        return True
    if not any(word in above for word in ("bike", "bicycle", "cycle", "pushbike")):
        return True
    said = str(understood.get("clean") or understood.get("text") or "").lower()
    return any(word in said for word in ("car", "cars", "van", "mot", "motor", "engine",
                                        "vehicle", "lorry", "truck"))


_SELLING_RIVAL = re.compile(r"\b(keep|keeping|fix|fixing|repair|repairing|mend|mending|scrap|"
                            r"scrapping|buy|buying|replace|replacing|new car|another car|get rid)\b")
_SELLING_BILL = (" of work ", " needs work ", "failed its mot", "failed the mot", "mot failure",
                 "worth selling", "worth keeping")


def _the_selling_is_the_decision(understood):
    text = " " + (understood.get("clean") or understood.get("plain") or "") + " "
    if any(w in text for w in _SELLING_BILL):
        return False
    if not (" or " in text or "should i" in text):
        return True
    return _SELLING_RIVAL.search(text) is None


def _entry(name, keys, reply, avoid=(), **kw):
    ask = kw.get("ask")
    if ask:
        kw["ask"] = tuple(ask) + MODELS
    bike_words = () if kw.pop("bikes", False) else NOT_BIKE
    return _raw_entry(name, tuple(keys) + (VEHICLE, MODELS), reply,
                      avoid=tuple(dict.fromkeys(tuple(avoid) + bike_words + LEASE_OR_BUY)), **kw)


_A_HOUSE_SURFACE = ("window", "windows", "wall", "walls", "ceiling", "kitchen", "bathroom",
                    "bedroom", "living room", "hall", "landing", "cupboard", "wardrobe",
                    "skirting", "conservatory", "porch")

_A_CAR_ONLY = ("car", "cars", "van", "boot", "footwell", "foot well", "cabin", "air con",
               "aircon", "air conditioning", "windscreen", "seats", "headlining", "sunroof",
               "spare wheel", "dashboard", "rear window", "wing mirror") + tuple(MODELS)


_A_DRIVING_WORD = re.compile(
    r"\b(?:driv(?:e|es|er|ers|ing|en)|car|cars|road|roads|motorway|motorways|dual carriageway|"
    r"roundabout|junctions?|headlights?|headlamps?|main beam|full beam|high beam|dipped|dip|dazzl\w*|"
    r"windscreen|wing mirror|mirrors?|lane|laning|traffic|vehicle|van|lorry|lorries|truck|"
    r"steer(?:ing)?|wheel|brakes?|braking|gear|gears|gearstick|clutch|accelerator|"
    r"park(?:ed|ing)?|revers(?:e|ing)|overtak\w*|tailgat\w*|aquaplan\w*|skid(?:s|ded|ding)?|"
    r"mot|dashboard|petrol|diesel|engine|bonnet|boot|tyres?|horn)\b",
    re.IGNORECASE)


def _a_car_is_in_the_line(understood):
    if not isinstance(understood, dict):
        return True
    said = " ".join(str(part) for part in (
        understood.get("text"), understood.get("clean"), understood.get("raw"),
        " ".join(str(word) for word in (understood.get("words") or ()))) if part).lower()
    if not said.strip():
        return True
    if _A_DRIVING_WORD.search(said):
        return True
    return any(" %s " % part in " %s " % said for part in _A_CAR_ONLY + tuple(MODELS))
_THE_LINE_NAMES_THE_TEST = (" mot", " mots", "before the test", "for the test", "the mot test",
                            "take it in", "take the car in", "goes in", "go in")


def _the_line_names_the_test(understood):
    if not isinstance(understood, dict):
        return False
    said = understood.get("text") or understood.get("clean") or ""
    if not said:
        said = " ".join(str(word) for word in (understood.get("words") or ()))
    said = " " + str(said).lower().replace(",", " ").replace(".", " ") + " "
    return any(part in said for part in _THE_LINE_NAMES_THE_TEST)


def _a_room_not_a_car(understood):
    said = " %s " % str(understood.get("text") or "").lower()
    if any(" %s " % part in said for part in _A_CAR_ONLY):
        return True
    return not any(" %s " % surface in said for surface in _A_HOUSE_SURFACE)


LEARNING = ("learning to drive", "learner driver", "learner", "driving lesson", "driving lessons",
            "driving instructor", "driving test", "stalling at junctions", "keep stalling")

_NOT_A_THING_TO_MOVE = ("radiator", "radiators", "boiler", "boilers", "heating", "central heating",
                        "wardrobe", "wardrobes", "piano", "furniture", "fridge", "freezer",
                        "bed", "table", "cupboard", "cupboards", "shelf", "shelves", "sideboard",
                        "removals", "moving house", "movers", "house", "flat", "floor")
CLEANING = ("gum", "chewing gum", "sofa", "settee", "couch", "carpet", "rug", "mattress",
            "shirt", "jumper", "duvet", "washing machine", "dishwasher", "kettle", "bath",
            "blockage", "drain", "mould", "mildew", "stain", "stains", "gravy", "ink",
            "paintbrush", "skirting", "grout", "bin", "wheelie")


_SOMEBODY_ELSES_HOME = re.compile(
    r"\b(?:care|nursing|residential|retirement|children'?s|funeral|hostel)\s+home\b"
    r"|\bmov(?:e|ed|es|ing)\s+(?:house|flat|home)\b"
    r"|\bmov(?:e|ed|es|ing)\s+(?:into|to)\s+(?:a|an|the|my|our|her|his|their)?\s*"
    r"(?:care|nursing|residential|retirement)?\s*home\b", re.IGNORECASE)


def _a_machine_and_not_a_person(understood):
    if not isinstance(understood, dict):
        return True
    said = understood.get("text") or " ".join(understood.get("words") or ())
    return not _SOMEBODY_ELSES_HOME.search(str(said))


def _learning(memory):
    turns = (memory or {}).get("turns") or []
    for turn in turns[-6:]:
        if isinstance(turn, dict):
            said = (turn.get("user") or "").lower()
            if any(phrase in said for phrase in LEARNING):
                return True
    return False


def _stalling(memory, understood):
    if _learning(memory):
        return None
    return ("A car that stalls when you stop is usually a dirty throttle body, a vacuum leak or "
            "an idle control fault, and the engine light often comes on with it. It is not usually "
            "dangerous but it is worth a garage soon, because it can leave you without power "
            "steering or brakes at a junction.")


def _brakes_cost(memory, understood):
    understood = understood or {}
    line = " ".join(str(understood.get(key) or "") for key in ("clean", "norm_text", "text")).lower()
    if not line:
        turns = (memory or {}).get("turns") or []
        if turns and isinstance(turns[-1], dict):
            line = (turns[-1].get("user") or "").lower()
    asked_life = any(word in line for word in ("last", "mileage", "life", "how often",
                                               "how long", "how many miles"))
    if asked_life:
        return ("Front pads usually last 25,000 to 50,000 miles, or about three to five years of "
                "ordinary driving, and rears last far longer - up to twice that. Town driving, "
                "towing and a heavy right foot wear them sooner, and a full car makes it worse. "
                "What ends their life is the friction material, not the miles: a wear indicator "
                "light, a squeal that starts when you brake, or a pedal that needs more travel "
                "means have them checked within a few hundred miles. Fitted, front pads are "
                "usually £100 to £200, and discs add £80 to £150 a pair.")
    return ("Front pads fitted are usually £100 to £200 and discs add £80 to £150 a pair, so a front "
            "set with discs is roughly £200 to £350; rears last longer and cost a bit less. Pads are a "
            "wear item, so this is normal upkeep rather than a fault, and any garage can quote you in "
            "five minutes.")


_CATALYTIC = ("A catalytic converter is the box in the exhaust that turns the harmful gases into "
              "harmless ones: carbon monoxide, unburnt fuel and nitrogen oxides go in, and carbon "
              "dioxide, water and nitrogen come out, over a honeycomb coated in platinum, palladium "
              "and rhodium. It has no moving parts and normally lasts the life of the car, but it "
              "only works once it is hot, so most of its cleaning happens after the first couple of "
              "miles. It is destroyed by a misfire, by burning oil or coolant, and by leaded fuel or "
              "the wrong additive, and it is stolen for those three metals - a car that suddenly "
              "gets much louder has usually had it cut out, which is a garage job, not something to "
              "drive on.")


MIST_REPLY = ("Clear the screen before you set off, because it is a legal requirement: front demist "
              "on, air conditioning on (it dries the air), heat up and the air on fresh rather "
              "than recirculate. A clean inside windscreen stops the mist coming back; shaving "
              "foam polished off works for a week.")

OIL_LEVEL = ("With the engine off and the car on level ground, pull the dipstick, wipe it, push it "
             "back in and read it: the level should sit between the marks. Top up a little at a "
             "time with the grade in the handbook, and never overfill. Check it monthly and before "
             "a long trip.")
OIL_INTERVAL = ("Most cars want an oil and filter change every 12 months or 10,000 to 12,500 "
                "miles, whichever comes first, and long-life oil on some newer cars stretches "
                "that to 20,000. Go by the handbook's schedule for yours, and shorten it if most "
                "of your driving is short town trips or towing.")
OIL_CHECK_FREQUENCY = ("Once a month, and before a long trip. With the engine off and the car on "
                       "level ground, pull the dipstick, wipe it, push it back in and read it: "
                       "the level should sit between the marks. Top up a little at a time with "
                       "the grade in the handbook, and never overfill.")
OIL_AMOUNT = ("Most cars take 4 to 5 litres from empty to full, including the filter, and the "
              "handbook gives the exact figure for yours. Buy the grade it names, add a little at "
              "a time and read the dipstick between goes rather than pouring in a whole can.")
_OIL_CHECK_WORDS = ("check", "checks", "checking", "oil level", "the level", "dipstick",
                    "top up", "top-up", "topup", "topping up", "top it up", "topped up",
                    "how do i know", "is my oil low", "oil low", "oil pressure light",
                    "low oil light")
_OIL_INTERVAL_WORDS = ("how often", "how long", "how many miles", "how frequently",
                       "when should i change", "when do i change", "when to change",
                       "when should i get it changed", "when should it be changed", "interval",
                       "how regularly",
                       "get the oil changed", "get my oil changed", "get it changed",
                       "oil changed", "oil needing changing", "need changing", "needs changing",
                       "an oil change", "oil change due", "due an oil change",
                       "get an oil change", "need an oil change", "needs an oil change",
                       "should i get an oil", "should i have an oil", "when is my oil",
                       "oil change is due", "change is due", "due for an oil",
                       "due for a change")
_OIL_AMOUNT_WORDS = ("how much oil", "much oil", "capacity", "litres", "liters",
                     "how many litres", "how many liters", "how much do i need")
_OIL_GRADE_WORDS = ("which oil", "what oil", "what grade", "oil grade", "which grade",
                    "viscosity", "5w", "0w", "10w", "15w", "fully synthetic", "semi synthetic",
                    "mineral oil", "synthetic oil", "oil spec", "specification")
OIL_GRADE = ("Buy the grade the handbook names - a modern petrol or diesel is usually a 5W-30 or "
             "0W-20 fully synthetic, and the spec code (VW 507 00, dexos, A5/B5) matters more than "
             "the brand. A higher or lower number is not \"better\": the first figure is how thick "
             "it is cold and the second how thick at running temperature, and the maker picked "
             "both.")
_OIL_COST_WORDS = ("cost", "costs", "price", "prices", "how much does an oil change",
                   "much for an oil change", "cheap", "cheapest", "expensive")
OIL_COST = ("An oil and filter change is around £60 to £120 at an independent garage and £90 to "
            "£180 at a main dealer, depending on the car and how much oil it takes; the oil is £25 "
            "to £45 and the filter £5 to £15 if you do it yourself. A dealer's 'interim service' "
            "is usually this plus a look round, so ask what the price includes before you book.")
_OIL_FILTER_WORDS = ("oil filter", "oil filters")
OIL_FILTER = ("Change the oil filter at every oil change: it is £5 to £15 and it is holding the "
              "soot and metal the old oil carried. A spin-on can comes off with a strap or a "
              "socket, a cartridge sits in a housing on top of the engine with a new seal in the "
              "box - and the new one goes on hand tight with a smear of oil on the rubber, because "
              "a filter tightened with a wrench is the one nobody can get off.")
_OIL_JOB_WORDS = ("what does oil do", "what does engine oil do", "what is oil for",
                  "what is engine oil for", "why does an engine need oil", "why do engines need oil",
                  "why does my car need oil", "job of the oil", "what does the oil do",
                  "what is the oil for", "why is oil important")
OIL_JOB = ("Oil does three jobs at once: it holds a film between the moving parts so metal never "
           "touches metal, it carries heat away from the bearings, and it keeps soot and wear "
           "particles in suspension until the filter takes them out. The grade on the can is what "
           "keeps that film the right thickness when it is hot, which is why the handbook's "
           "number matters more than the brand.")
_OIL_OVERFILL_WORDS = ("overfill", "overfills", "overfilled", "overfilling", "over fill",
                       "over filled", "too much oil", "too full", "over the max",
                       "over the mark", "above the max", "above the top mark")
OIL_OVERFILL = ("A little over the top mark is not a disaster - the level is read cold on level "
                "ground, so a warm engine can show high for a few minutes - but well over it, or "
                "smoke and rough running, means drain some out before you drive far: too much oil "
                "foams, the crank whips it into the breather and the seals leak. A garage drains "
                "a bit from the sump plug in minutes, and a suction pump from the top is the "
                "no-spanner way.")

TYRE_PRESSURE = ("Find the right pressures on the sticker inside the driver's door frame or the "
                 "fuel flap, not on the tyre, and check them cold before you drive: warm tyres "
                 "read a few psi high. Most cars want about 30 to 35 psi, a bit more when fully "
                 "loaded. Top up every couple of weeks, because under-inflated tyres wear the "
                 "edges, cost fuel and make the car feel vague.")
TYRE_PRESSURE_FREQUENCY = ("Every couple of weeks and before a long run, and always with the tyres "
                           "cold, because warm ones read a few psi high. Find the right pressures "
                           "on the sticker inside the driver's door frame or the fuel flap, not "
                           "on the tyre: most cars want about 30 to 35 psi, a bit more when fully "
                           "loaded. Under-inflated tyres wear the edges, cost fuel and make the "
                           "car feel vague, so it is worth the two minutes at the pump.")


def _tyre_pressure_reply(memory, understood):
    if asks_how_often(understood):
        return TYRE_PRESSURE_FREQUENCY
    return TYRE_PRESSURE


def _the_abs_is_in_a_car(understood):
    text = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    if not re.search(r"\babs\b", text):
        return True
    return bool(re.search(r"\b(?:light|lights|lit|warning|symbol|dash|dashboard|cars?|brake|"
                          r"brakes|braking|mot|garage|wheel|wheels|sensor|comes?|came|"
                          r"flashing|flashes|flickering)\b", text))


_DASH_LIGHT_TEXTS = (
    (("brake light", "brake warning", "handbrake", "parking brake", "brake fluid"),
     "A red brake light usually means the handbrake is still on or the fluid is low, so check "
     "the lever first, then the fluid level under the bonnet. If the light stays on with the "
     "lever down, or the pedal feels soft, do not drive it: that is the brakes, and it needs "
     "looking at before you go anywhere."),
    (("abs light", "abs warning", "anti-lock", "anti lock"),
     "An ABS light means the anti-lock system has shut itself off, so the ordinary brakes still "
     "work and you can drive gently to a garage - it is what stops the wheels locking in a skid, "
     "so do not leave it for months. The usual causes are a wheel sensor or its ring, and the "
     "garage reads the fault code to say which."),
    (("dpf light", "dpf warning", "particle filter", "diesel particle", "exhaust filter"),
     "A DPF light means the diesel particle filter is part blocked; a steady light often clears "
     "after a 20-minute run at 50 mph or so in a lower gear, which gets it hot enough to burn the "
     "soot off. If it stays on, or the engine light joins it, drive to a garage instead of "
     "carrying on - a filter that cannot regenerate is an expensive part."),
    (("airbag light", "air bag", "srs light", "airbag"),
     "An airbag light means the system has a fault and the bags may not fire, so the car drives "
     "but the crash protection is not there; get the code read within a few weeks. The common "
     "causes are a connector under a seat or the clock spring in the steering wheel, and both are "
     "cheap compared with the alternative."),
    (("battery light", "battery", "charging", "alternator"),
     "A battery light on while you drive means the alternator is not charging, so you are running "
     "on what the battery holds - 20 or 30 miles at most with the lights off. Switch off anything "
     "electric, drive straight to a garage or stop somewhere safe and call for help."),
    (("tyre pressure light", "tpms", "tyre light", "tire pressure", "tire light", "flat tyre",
      "flat tire", "tyre pressure", "tyre", "tire"),
     "A tyre pressure light means one tyre is below where it should be: check all four and the "
     "spare with a gauge and pump them to the figures on the sticker inside the driver's door. A "
     "light that comes back within a day is a slow puncture, not a sensor."),
    (("power steering", "steering light"),
     "A power steering light means the assistance has dropped out or is failing, so the wheel "
     "will feel heavy at parking speed; drive gently to a garage. If the car has a hydraulic "
     "system, check the fluid first - on an electric one, only a fault code will say which part "
     "has gone."),
    (("traction light", "traction control", "esp light", "esc light", "skid light", "slippery"),
     "A traction light that flashes and then goes out is the system working on a slippery road; "
     "one that stays on means it has switched itself off with a fault. The car still drives, but "
     "without that safety net, so book it in rather than waiting for a wet morning."),
    (("glow plug", "glowplug", "preheat"),
     "A glow plug light that stays on or flashes means the pre-heat system or the engine "
     "management has a fault, and on many diesels a flashing one means limp mode. Get the code "
     "read rather than revving through it, especially in cold weather when the plugs are doing "
     "the starting."),
    (("adblue", "ad blue", "urea light"),
     "An AdBlue light means the tank is getting low, so top it up at a pump or with a can - and "
     "do not let the countdown reach zero, because many cars then refuse to restart. Use the "
     "grade the handbook names, and wipe up any spills, since the fluid is corrosive to metal."),
    (("service light", "spanner", "service indicator", "service due"),
     "A spanner or service light is the car counting down to a service, not a fault, so it is "
     "safe to drive until the work is done. If the car has just been serviced, the garage forgot "
     "to reset it, and the handbook shows the button sequence."),
    (("washer fluid", "washer warning", "screen wash", "washer light"),
     "That symbol is the screen wash running low: top it up with screen wash and water, not "
     "washing-up liquid, which foams and clogs the jets. It is fine to drive, but do it before a "
     "salty motorway run rather than after."),
    (("seatbelt", "seat belt", "belt light"),
     "A seatbelt light that stays on means the car thinks a belt is unbuckled, so check the "
     "passenger seats and anything heavy left on them - a bag sets it off. If every belt is "
     "clipped and it is still lit, the buckle sensor is the part to look at."),
    (("brake pad", "pad wear", "wear indicator"),
     "A brake pad light means a sensor has worn through, so the pads are near the end of their "
     "life and want changing within a few hundred miles. Book it in now; waiting for the grinding "
     "noise means new discs as well as pads."),
    (("key symbol", "immobiliser", "immobilizer", "key light", "key warning"),
     "A key symbol light is the immobiliser not recognising the key - try the spare first. If the "
     "spare works, the first key's chip or battery is the problem, and a new key is cheaper from a "
     "locksmith than from the dealer."),
)


CAR_NOUNS = ("car", "cars") + VEHICLE + MODELS


CAR_PARTS = ("gear", "gears", "gearbox", "gearboxes", "brake", "brakes", "braking", "engine",
             "engines", "suspension", "exhaust", "clutch", "cambelt", "timing belt", "tyre",
             "tyres", "tire", "tires", "wheel", "wheels", "headlight", "headlights", "bumper",
             "windscreen", "windshield", "alternator", "starter motor", "shock absorber",
             "shocks", "spring", "springs", "bearing", "bearings")
CAR_WEAR = ("wing mirror", "wing mirrors", "side mirror", "door mirror", "mirror", "mirrors",
            "dent", "dents", "scratch", "scratches", "scratched", "aircon", "air con",
            "air conditioning", "stone chip", "stone chips", "paintwork", "bodywork",
            "number plate", "number plates", "sunroof", "headlamp", "headlamps",
            "indicator", "indicators", "wiper", "wipers", "alloy", "alloys", "battery",
            "batteries", "seat belt", "seats", "upholstery", "bumper", "panel", "panels")

HOME_SURFACE = ("wall", "walls", "plaster", "plasterboard", "drywall", "skirting", "ceiling",
                "worktop", "worktops", "floor", "floors", "floorboard", "floorboards",
                "door frame", "fridge", "freezer", "bath", "bathroom", "sink", "cabinet",
                "cupboard", "table", "chair", "stairs", "window frame", "fence", "fences",
                "shed", "decking", "paving", "roof", "tiles", "radiator", "boiler", "oven",
                "washing machine", "washer", "dishwasher", "tumble dryer", "hoover", "vacuum",
                "garden", "gate")

GARAGE_TRADE = CAR_NOUNS + CAR_PARTS + (
    "garage", "garages", "mechanic", "mechanics", "labour", "dealership", "dealerships",
    "bodyshop", "mot", "mot test")


def _the_trade_is_named(understood):
    if str((understood or {}).get("topic") or "") == "cars":
        return True
    said = " ".join(str(value) for value in ((understood or {}).get(key)
                                             for key in ("clean", "norm_text", "plain"))
                    if isinstance(value, str)).lower()
    if _words_name_the_trade(said):
        return True
    leaned = str(((understood or {}).get("leans_on") or {}).get("text") or "")
    if leaned and _words_name_the_trade(leaned):
        return True
    return not (_names_the_house(said) or _names_the_house(leaned))


HOUSE_TRADE = HOME_SURFACE + (
    "tap", "taps", "leak", "leaks", "leaking", "leaked", "plumbing", "plumber", "pipe", "pipes",
    "toilet", "toilets", "shower", "showers", "drain", "drains", "gutter", "gutters", "fuse",
    "fuses", "socket", "sockets", "wiring", "electrician", "builder", "carpenter", "handyman",
    "door", "doors", "window", "windows", "lock", "damp", "mould", "central heating", "heating",
    "thermostat", "hob", "cooker", "microwave", "fridge freezer", "tumble drier", "vacuum cleaner")


def _names_the_house(text):
    said = " " + " ".join(str(text or "").split()) + " "
    return any((" " + word + " ") in said for word in HOUSE_TRADE)


def _words_name_the_trade(text):
    said = " " + " ".join(str(text or "").split()) + " "
    house = any((" " + word + " ") in said for word in HOME_SURFACE)
    if not house and any((" " + word + " ") in said for word in CAR_WEAR):
        return True
    return any((" " + word + " ") in said for word in GARAGE_TRADE)


def _dash_light_reply(memory, understood):
    said = the_line(understood)
    for words, text in _DASH_LIGHT_TEXTS:
        if any(word in said for word in words):
            return text
    return ("Most dash lights are a warning to check something rather than a breakdown: an amber "
            "one means get it looked at soon, a red one means stop when it is safe. Tell me which "
            "symbol it is, or what shape it has, and I will say what it stands for.")



def _oil_reply(memory, understood):
    said = the_line(understood)
    if any(word in said for word in _OIL_COST_WORDS):
        return OIL_COST
    if any(word in said for word in _OIL_FILTER_WORDS):
        return OIL_FILTER
    if any(word in said for word in _OIL_GRADE_WORDS):
        return OIL_GRADE
    if any(word in said for word in _OIL_JOB_WORDS):
        return OIL_JOB
    if any(word in said for word in _OIL_OVERFILL_WORDS):
        return OIL_OVERFILL
    if any(word in said for word in _OIL_AMOUNT_WORDS):
        return OIL_AMOUNT
    if any(word in said for word in _OIL_CHECK_WORDS):
        if asks_how_often(said):
            return OIL_CHECK_FREQUENCY
        return OIL_LEVEL
    if any(word in said for word in _OIL_INTERVAL_WORDS):
        return OIL_INTERVAL
    turns = (memory or {}).get("turns") or []
    last = turns[-1].get("bot") if turns and isinstance(turns[-1], dict) else ""
    if isinstance(last, str):
        for answer in (OIL_INTERVAL, OIL_AMOUNT):
            if answer.split(".")[0] in last:
                return answer
    return OIL_LEVEL


NO_MOT_FINE = ("Driving a car with no MOT can cost up to £1,000, and the insurance usually counts "
               "as invalid too, so a crash becomes your bill. You can drive to a pre-booked MOT or "
               "repair appointment without one, and nowhere else. Check the date free at gov.uk with "
               "the number plate, because there is no grace period.")
NO_MOT_TO_A_TEST = ("Yes - to a pre-booked MOT or repair appointment, and nowhere else. Any other "
                    "journey with no MOT can cost up to £1,000 and usually leaves the insurance "
                    "invalid, so a crash becomes your bill, and there is no grace period. Check the "
                    "date free at gov.uk with the number plate.")
TO_A_TEST = ("drive to", "drive it to", "driving to", "take it to", "get it to", "drive it there",
             "to the garage", "to the test", "to a pre", "to a booked", "to an mot", "to the mot",
             "to my mot", "to its mot")
LEGAL_ASK = ("legal", "allowed", "permitted", "am i able", "can i", "may i", "could i", "ok to")

_A_SEAT_OR_A_CHILD = re.compile(
    r"\b(seat|seats|isofix|car|cars|child|children|kid|kids|toddler|baby|son|daughter|"
    r"height|135|law|legal|rear facing|backless|high backed|high-backed|front seat|cushion|"
    r"maxi)\w*")


def _a_seat_is_what_it_is_about(understood):
    line = " ".join(str(word) for word in ((understood or {}).get("words") or ()))
    if _A_SEAT_OR_A_CHILD.search(line):
        return True
    lean = (understood or {}).get("leans_on") or {}
    return bool(_A_SEAT_OR_A_CHILD.search(" ".join(str(word) for word in lean.get("words") or ())))


def _no_mot(memory, understood):
    line = (understood.get("clean") or understood.get("text") or "").lower()
    if any(word in line for word in TO_A_TEST) and any(word in line for word in LEGAL_ASK):
        return NO_MOT_TO_A_TEST
    return NO_MOT_FINE

_A_BICYCLE = ("bike", "bikes", "bicycle", "bicycles", "pushbike", "cycling", "cyclist",
              "cyclists", "inner tube", "inner tubes", "handlebars", "chainring", "pannier",
              "panniers")

_TYRE_PRICE = ("A budget tyre fitted is about £55 to £80 a corner, mid-range £75 to £120 and "
               "premium £120 to £200, with fitting, balancing and disposal £15 to £25 of that. "
               "Read the size off the sidewall - 205/55 R16 - and ring two or three fitters with "
               "it: the same tyre can differ by £40. Two at a time is fine, new pair on the back, "
               "and change them at 3mm of tread.")


def _tyre_price(memory, understood):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    said = " ".join(str(turn.get("user") or "") for turn in (turns or [])[-4:]
                    if isinstance(turn, dict)).lower()
    if any(word in said for word in _A_BICYCLE):
        return ""
    return _TYRE_PRICE


MOT_FAIL_CLOCK = (
    "You have 10 working days from the fail to get the repair done and take the car back for a "
    "partial retest - free if it goes back by the end of the next working day - and after that the "
    "test starts again from scratch. ")
MOT_FAIL_REPLY = (
    "Sorry to hear it, and it is usually fixable. Read the fail sheet: 'dangerous' means don't "
    "drive it at all, a 'major' needs fixing before it can pass, and an advisory is a warning for "
    "next time. Many garages do the repair and the free partial retest in one go if you leave the "
    "car with them.")


def _mot_fail_reply(memory, understood):
    asks = set((understood or {}).get("asks") or ())
    if "how_long" in asks or "how_much" in asks:
        return MOT_FAIL_CLOCK + MOT_FAIL_REPLY
    return MOT_FAIL_REPLY


def _money_against_value(memory, understood):
    figures = []
    for number in understood.get("numbers") or ():
        value = number.get("value")
        if isinstance(value, (int, float)) and value >= 150:
            figures.append(int(value))
    if len(figures) == 1:
        figure = figures[0]
        return ("£%s of work is the number to judge it by: if the car would sell for less than "
                "about £%s, the repair is the bigger number, so let it go. Scrap value is only "
                "£150 to £400, and a 'dangerous' MOT item like brakes, steering or rust near a "
                "mounting is not worth fixing on a cheap car; tyres, a clutch or a cambelt on an "
                "otherwise sound car usually are." % (format(figure, ","), format(figure * 2, ",")))
    return ("Money against value: if the quote is more than the car is worth, or more than half of it "
            "in one go on an old car, let it go. A 'dangerous' MOT item like brakes, steering or rust "
            "near a mounting is not worth fixing on a cheap car; tyres, a clutch or a cambelt on an "
            "otherwise sound car usually are. Scrap value is only £150 to £400.")


ENTRIES = [
    _entry("battery-flat", (("car",), ("battery",), ("flat", "dead", "going flat", "keeps going flat",
                                                   "dies", "dying", "drain", "drained", "draining")),
          "A car battery that keeps going flat is usually either old (they last 3 to 5 years) or "
          "being drained by something left on, a stuck boot light or a failing alternator. Get the "
          "battery and charging system tested free at most tyre or battery places; if it is the "
          "original battery and the car is five or more, replace it.",
          avoid=_NOT_BUYING + ("cost", "costs", "price", "prices", "how much",
                               "phone", "phones", "laptop", "tablet", "ipad", "iphone", "android",
                               "macbook", "mac book", "notebook", "computer", "pc", "desktop",
                               "chromebook",
                               "watch", "headphones", "earbuds", "camera", "drill", "torch",
                               "hoover", "vacuum", "charger", "power bank", "smoke alarm",
                               "fob", "keyfob", "key fob", "remote", "keyless", "car key",
                               "spare key",
                               "mouse", "mice", "keyboard", "wireless", "bluetooth", "usb",
                               "trackpad", "touchpad", "cursor",
                               "phone", "iphone", "android", "mobile", "laptop", "macbook",
                               "tablet", "ipad", "drains", "draining", "battery health",
                               "battery care", "look after"),
          ask=("battery", "batteries", "flat battery", "charge", "charging", "alternator", "jump",
               "car", "van", "vehicle", "engine", "ignition", "bonnet", "motorhome", "camper",
               "motorbike", "does not start", "doesnt start", "will not start", "wont start",
               "is flat", "is dead", "going flat", "gone flat", "battery light", "dashboard",
               "warning light",
               "lights on", "left the lights", "headlights", "interior light", "dome light",
               "boot light", "radio on", "left on", "left the radio")),
    _entry("jump-start", (("jump start", "jump-start", "jumper leads", "jump leads"), ("car", "battery", "leads")),
          "Park the two cars so the leads reach and both engines are off. Red lead to the flat "
          "battery's positive, other end to the good battery's positive; black to the good battery's "
          "negative, then to a bare metal bolt on the dead car away from the battery. Start the good "
          "car, wait a minute, start the dead one, then take the leads off in the reverse order.",
          avoid=_NOT_BUYING),
    _entry("wont-start", (("won't start", "wont start", "wouldn't start", "wouldnt start",
                          "will not start", "not starting", "doesn't start", "does not start",
                          "won't turn over", "wont turn over", "won't fire", "wont fire",
                          "slow to start", "slow starting", "slow turning over",
                          "takes a while to start", "takes ages to start", "takes long to start",
                          "struggles to start", "struggling to start", "hard to start",
                          "reluctant to start"),
                         ("car", "engine", "morning", "cold", "click", "clicking")),
          "Listen to what it does: a click or nothing at all is the battery or its connections, a slow "
          "groaning crank is a flat battery, and a fast crank that won't fire is fuel or ignition. "
          "Try a jump start first; if that works, the battery or alternator is the problem, not the "
          "engine.",
          avoid=_NOT_BUYING),
    _entry("starter-motor", (("starter motor", "starter motors", "starter"),
                             ("test", "testing", "check", "click", "clicks", "clicking",
                              "whirr", "whirring", "spins", "spinning", "turns over",
                              "not turning", "replace", "replacement", "change",
                              "is it the starter", "is it my starter", "is it a starter",
                              "is it the starter motor", "is it my starter motor",
                              "faulty", "gone", "dead", "failed", "problem",
                              "problems", "wrong", "noise", "noisy")),
          "Check the battery before blaming the starter: switch the headlights on and crank, and if "
          "they stay bright while nothing turns over, the starter is the suspect. One loud click that "
          "repeats is the solenoid or a flat battery, a starter that whirs without turning the engine "
          "needs a garage, and a replacement is £150 to £300 fitted.",
          avoid=_NOT_BUYING + ("mower", "lawnmower", "sourdough", "sour dough", "dough", "bread",
                               "flour", "yeast", "loaf", "loaves", "ferment", "fermentation",
                               "levain", "hooch", "jar", "bubbling", "bubbles", "bubbly",
                               "mould", "mold", "mouldy", "moldy", "kahm", "fur",
                               "furry", "fuzz", "fuzzy", "starter culture",
                               "starter culture", "feed", "feeding", "plant", "plants",
                               "cuttings", "cutting", "seed", "seeds", "compost", "garden",
                               "greenhouse", "sow", "sowing", "seedling", "seedlings")),
    _entry("battery-change", (("battery", "batteries"), ("replace", "replacement", "change", "new one",
                                                        "how long", "last", "cost", "how much",
                                                        "price", "cheapest")),
          "Batteries last about 3 to 5 years and cost roughly £70 to £150 fitted, more with "
          "stop-start. Match the size and the cold-cranking rating in the handbook, and note that "
          "many newer cars need the new battery coded to the car, so a garage is easier than doing "
          "it yourself.",
          avoid=("phone", "laptop", "tablet", "remote", "hearing"),
          ask=("car", "cars", "vehicle", "van")),

    _entry("tyre-pressure", (("tyre", "tyres", "tire", "tires"),
                             ("pressure", "psi", "bar", "inflate", "pump", "soft", "squashy",
                              "low", "check", "checking", "gauge", "correct", "underinflated",
                              "loaded")),
          _tyre_pressure_reply,
          avoid=_NOT_BUYING + NOT_BIKE),
    _entry("tyre-tread", (("tread", "tyres", "tyre", "tires", "tire"), ("worn", "wearing", "bald",
                                                                        "legal", "limit", "depth",
                                                                        "1.6", "check", "20p")),
          "The legal minimum is 1.6mm across the middle three-quarters of the tyre; push a 20p coin "
          "into the tread and if the outer band is hidden you are still legal. In the wet, replace "
          "them nearer 3mm, because grip falls off a cliff below that. Also check the sidewalls for "
          "cuts and bulges.",
          avoid=_NOT_BUYING + NOT_BIKE),
    _entry("tyre-puncture", (("puncture", "flat tyre", "flat tire", "nail in", "nail out",
                             "nail out of", "nail from", "screw from", "nail stuck",
                             "from my tyre", "from the tyre", "from a tyre", "from my tire",
                             "from the tire", "from a tire", "in the tyre", "in the tire",
                             "nail in my tyre", "screw in my tyre",
                             "screw in my tire", "screw in the tyre", "screw in the tire",
                             "going down",
                             "going flat", "losing air", "losing pressure", "keeps going down",
                             "tyres flat", "tyre flat", "tires flat", "tire flat",
                             "flat tyres", "flat tires", "tyres are flat", "tyre is flat"),
                            ("tyre", "tyres", "tire", "tires", "wheel", "repair", "spare",
                             "sealant", "fix", "car", "plug", "slow", "causes", "cause")),
          "A flat while you are out: pull over somewhere safe, hazards on, and put the spare on (or "
          "use the sealant kit), keeping under 50mph to the nearest garage. If it is still up, drive "
          "slowly to a tyre place instead: a nail in the middle of the tread can be plugged for "
          "around £20 to £30, while sidewall damage cannot and needs a new tyre.",
          avoid=_NOT_BUYING + NOT_BIKE + _NOT_A_TYRE),
    _entry("tyre-life", (("tyre", "tyres", "tire", "tires"), ("last", "how long", "wear", "worn",
                                                              "mileage", "age", "old", "replace",
                                                              "change", "need", "new")),
          "A set of tyres lasts roughly 20,000 to 40,000 miles, and 5 to 6 years from the date on the "
          "sidewall even if the tread looks fine, because the rubber hardens. Change them when the "
          "tread reaches 3mm for wet grip, or sooner if the sidewalls crack. All four together is "
          "best; if you replace a pair, put the new ones on the back.",
          avoid=_NOT_BUYING + NOT_BIKE),
    _entry("tyre-price", (("tyre", "tyres", "tire", "tires"),
                          ("cost", "costs", "price", "prices", "how much", "expensive", "cheap",
                           "cheapest", "budget for", "pay", "fitted", "each", "a corner",
                           "per tyre", "set of four", "four new", "new set",
                           "new tyre", "new tyres", "needs new tyres", "need new tyres",
                           "needs tyres", "need tyres", "replace the tyres", "replacing the tyres",
                           "tyres need replacing", "tyre needs replacing")),
          _tyre_price,
          bias=2, avoid=NOT_BIKE + _NOT_A_TYRE + _NOT_BUYING_SALE +
          ("mot", "mot test", "fail sheet", "failed its mot")),
    _entry("tyre-pressure-light", (("tyre pressure", "pressure warning", "tpms"),
                                  ("light", "on", "came on", "warning", "reset", "flashing")),
          "That light means one tyre is below the pressure it should be, so check all four cold and "
          "inflate to the figures on the door sticker; the light usually clears itself after a few "
          "minutes of driving. On most cars there is a reset button or a menu item. If one tyre keeps "
          "losing pressure, there is a slow puncture to find.",
          avoid=NOT_BIKE),
    _entry("tyre-change", (("change a tyre", "change a wheel", "change the tyre", "how do i change",
                           "how to change", "spare wheel", "wheel nuts", "jack up", "put the spare on"),
                          ("tyre", "wheel", "spare", "jack", "blowout")),
          "Loosen the wheel nuts half a turn while the car is still on the ground, then jack it at "
          "the marked point, take the nuts off, lift the wheel away and put the spare on. Nip the "
          "nuts up in a star pattern, lower it, then tighten properly with the brace. Keep under "
          "50mph on a space saver and check its pressure every few months.",
          bias=1, avoid=NOT_BIKE),
    _entry("winter-tyres", (("winter tyres", "winter tyre", "snow tyres", "snow tyre",
                             "all season tyres", "all-season tyres", "all weather tyres"),
                            ("tyres", "tyre")),
          "In the UK they are rarely worth it unless you drive on ungritted country roads or in "
          "Scotland: winter tyres grip much better below 7°C, but most people do fine on good "
          "all-season tyres. If you do fit them, put all four on and swap back in spring, because "
          "they wear fast in the warm.",
          ask=("winter", "tyres", "tyre", "season", "snow", "ice", "icy", "cold", "grip", "uk",
               "need", "worth", "should", "when", "fit", "change", "swap", "buy", "get", "use",
               "best", "whether", "if", "drive", "driving"),
          avoid=NOT_BIKE),
    _entry("van-hire", (("rent a van", "renting a van", "hire a van", "hiring a van",
                         "borrow a van", "borrowing a van", "van rental", "van hire",
                         "book the van", "book a van", "booking a van", "booking the van"),
                        ("should i", "worth", "better", "cheaper", "or", "instead", "need",
                         "want", "move", "moving", "house", "insurance", "covered")),
          "Hiring is usually the better call for a move: the van comes with insurance and a "
          "mileage cap, so a scratch costs you the excess rather than the repair, and you are not "
          "relying on someone else's mood or policy. Borrowing is fine for one light load, but "
          "check the owner's insurance covers other drivers before you fill it.",
          avoid=NOT_BIKE + ("buy", "buying", "purchase", "lease", "leasing", "finance",
                            "second hand", "secondhand", "van for sale",
                            "licence", "license", "entitlement", "c1")),
    _entry("van-licence", (("licence", "license", "entitlement"),
                           ("van", "vans", "hire", "hiring", "rent", "rental", "luton",
                            "3.5", "tonne", "tonnes", "bigger")),
          "An ordinary full UK licence covers a van up to 3.5 tonnes, so a standard Transit or a "
          "short-wheelbase Luton is fine to hire. Anything heavier needs the C1 entitlement, which "
          "you get by passing a separate test; the hire firm will ask for your licence and a "
          "second proof of address.",
          avoid=("test", "lessons", "theory", "provisional", "points", "banned", "revoked")),
    _entry("tyre-noise", (("tyre", "tyres"), ("noise", "noisy", "hum", "rumbling", "roar")),
          "Tyre noise that grows with speed is usually uneven wear, a cheap aggressive tread or a "
          "wheel bearing on its way out. Run a hand round the inside edge of each tyre for scalloped "
          "high and low spots, and have a garage spin the wheels to check the bearings.",
          avoid=_NOT_BUYING + NOT_BIKE),

    _entry("mot-cost", (("mot",), ("cost", "how much", "price", "fee", "expensive", "charge")),
          "A car MOT costs up to £54.85 in England, Scotland and Wales and £30.50 in Northern "
          "Ireland, and plenty of garages charge less; the fee is the same whether it passes or "
          "fails. Repairs are extra, and you can ask for the price before they start.",
          avoid=_NOT_BUYING),
    _entry("mot-due", (("mot",), ("due", "when", "pass", "book", "check", "expire", "expires",
                                  "reminder", "how often", "how long", "every year", "first",
                                  "need", "needs", "valid")),
          "A car needs its first MOT at three years old, then every year. The test covers lights, "
          "tyres, brakes, steering, suspension, seatbelts, emissions and the windscreen, and the "
          "maximum fee is £54.85 for a car. You can drive to a pre-booked test without a current "
          "MOT, but not otherwise. The only exemption for a car is a historic vehicle: over 40 "
          "years old, not substantially changed, and taxed in the historic class - the DVLA form "
          "for that is free, and without it the car still needs its test.",
          avoid=_NOT_BUYING),
    _entry("mot-prep",
           (("mot", "mot test", "the test"),
            ("prepare", "preparing", "before", "ready", "get it ready", "check", "checking",
             "anything i should", "what should i do", "what do i need to do"),
            ("before an mot", "before the mot", "before the test", "before it goes in")),
           "Ten minutes first: tyres at the right pressure with 1.6mm of tread across the middle "
           "three quarters, every light working including the number plate lamp, wipers clearing, "
           "screenwash topped up and the horn sounding. Clear the warning lights off the dash, "
           "empty the boot of anything a tester would have to move, and take the V5C or the "
           "reference the centre has on file.",
           bias=2,
           guard=_the_line_names_the_test,
           ask=("prepare", "preparing", "get it ready", "ready for it", "ready for the",
                "anything i should", "what should i do", "what do i need to do", "what to check",
                "want to check", "should i check", "checks"),
           avoid=("cost", "price", "much", "fee", "cheap", "how long", "due", "valid", "expire",
                  "fail", "failed", "fails", "retest", "dangerous", "advisory", "passed",
                  "every year", "how often", "first mot", "three years",
                  "sell", "selling", "sold", "worth", "value", "buy", "buying", "trade in",
                  "we go", "before we", "trip", "holiday",
                  "test drive", "test-drive", "test driving",
                  "what does the mot", "do they check", "test check", "tester look")),
    _entry("car-service-time",
           (("service", "serviced", "servicing", "full service", "interim service",
             "oil change", "oil and filter"),
            ("how long", "take", "takes", "taking", "half a day", "a day", "morning", "hours",
             "how many hours", "waiting", "wait")),
           "A full service usually means leaving the car for the day, and an oil and filter "
           "change or an interim service is two or three hours, so ask for a while-you-wait slot "
           "if you need the car. Get the price in writing with the parts listed, and have the "
           "book or the app stamped, because the service history is what a buyer checks.",
           bias=1,
           avoid=("customer service", "phone", "mobile", "broadband", "internet", "wifi", "bus",
                  "bus service", "train", "tram", "funeral", "christening", "church", "mass",
                  "restaurant", "waiter", "table service", "room service", "gas", "boiler",
                  "central heating", "heating", "tv", "telly", "streaming", "netflix",
                  "insurance", "pension", "nhs", "health service", "social services", "council",
                  "cost", "price", "much", "how often", "interval", "mileage", "miles", "worth",
                  "need", "needs", "required", "annual")),
    _entry("mot-fail", (("mot", "mot test"), ("failed", "fail", "fails", "failure", "failures",
                                              "retest", "dangerous", "fail sheet",
                                              "what happens", "what happens now", "what now",
                                              "what are my options", "my options", "what do i do",
                                              "next step", "next steps")),
          bias=2,
          reply=_mot_fail_reply,
          avoid=_NOT_BUYING + ("appeal", "appeals", "appealing", "dispute", "disputing",
                               "challenge", "dvsa", "tester")),
    _entry("mot-fail-dangerous",
          (("mot",), ("brake", "brakes", "brake pipe", "brake pipes", "brake pads",
                      "brake pad", "brake disc", "brake discs", "brake fluid", "brake hose",
                      "steering", "suspension", "spring", "springs", "shock", "shocks",
                      "shock absorber", "subframe", "corrosion", "rust", "rusty", "sill", "sills",
                      "structural",
                      "chassis", "tyre", "tyres", "wheel", "wheels", "dangerous")),
          "On an MOT a fault in the brakes, the steering, the suspension, the structure or a tyre "
          "is normally marked 'dangerous', and a dangerous fail means the car must not be driven "
          "on the road at all - not even to the garage. Book recovery or ask the garage to collect "
          "it, and take it back the next working day, when the partial retest is free. If the "
          "sheet says 'major' instead, you can drive it to the garage or to a pre-booked test.",
          bias=2,
          avoid=_NOT_BUYING + ADVISORY_PASS + ("squeak", "squeaking", "squeal", "squealing",
                                              "grinding", "worn", "wear", "how much", "cost",
                                              "price", "quote", "replace", "replacing", "change",
                                              "changing", "fix", "bleed", "soft pedal", "spongy",
                                              "handbrake")),
    _entry("mot-fail-major",
          (("mot",), ("light", "lights", "headlight", "headlights", "indicator", "indicators",
                      "brake light", "brake lights", "number plate light", "wiper", "wipers",
                      "washer", "washers", "horn", "exhaust", "windscreen", "mirror",
                      "mirrors", "number plate", "seatbelt", "seatbelts", "emissions")),
          "A fault like that is usually a 'major', not a 'dangerous' one: you can drive it to the "
          "garage or to a pre-booked test and nowhere else, and taking it back the next working "
          "day makes the partial retest free. Read the sheet before you move it; only "
          "'dangerous' means the car must not be driven at all. Put a bulb, a wiper, a number "
          "plate or a tyre right yourself in a few minutes; brakes, steering, suspension and "
          "anything rusted through are the garage's.",
          bias=2, avoid=_NOT_BUYING + ADVISORY_PASS),
    _entry("mot-appeal",
           (("appeal", "appeals", "appealing", "dispute", "disputing", "disagree",
             "disagreed", "complain about the mot", "wrong mot", "unfair mot", "challenge",
             "not happy with the mot", "think it should have passed"),
            ("mot", "mot test", "test result", "fail", "failed", "failure", "tester",
             "test centre", "dvsa", "garage")),
           "Appealing goes to the DVSA rather than the garage: ask them for the appeal form "
           "(VT17) within 14 days of the test, and it costs nothing. Do not have the repairs done "
           "before you decide, because an appeal is only worth it while the car is as it was "
           "tested - if the fault is real and the argument is only about how serious it is, the "
           "cheaper route is to ask the test centre to explain the sheet and then have the work "
           "done and the partial retest, which is free within 10 working days.",
           bias=3, avoid=_NOT_BUYING + NOT_BIKE + ADVISORY_PASS + ("parking", "ticket", "fine",
                                                                   "speeding", "points",
                                                                   "licence", "benefits",
                                                                   "bill", "quote", "quoted",
                                                                   "charge", "charged", "cost",
                                                                   "overcharged", "refund")),
    _entry("mot-fail-bill",
           (("failed", "fails", "fail", "failure", "fail sheet", "failed its mot", "mot failure",
             "mot fail", "failed the mot"),
            ("quote", "quoted", "bill", "cost", "costs", "how much", "price", "priced", "pay",
             "worth", "expensive", "garage wants", "they want", "wants to charge", "cheapest",
             "scrap", "scrapping", "write it off", "fix it", "repair", "repairs", "a lot",
             "too much", "hundreds", "thousand", "four figures")),
           "Get the fail sheet priced line by line, in writing, and ask which items are the "
           "failure and which are advisories they would like to do - a garage will often quote "
           "for the lot and only the failure is compulsory. A second quote is normal and free, "
           "and the partial retest is free if the work is back within 10 working days. Then "
           "weigh it against the car: a bill over about a third of what the car would sell for "
           "is the point to ask whether the money is better spent on a replacement, and a garage "
           "will tell you what it would buy the car for as it stands.",
           bias=2, avoid=_NOT_BUYING + NOT_BIKE + ADVISORY_PASS + ("how much is an mot",
                                                                  "mot cost", "mot fee",
                                                                  "test fee", "sold", "selling",
                                                                  "buy", "buying", "lease",
                                                                  "insurance", "tyre", "tyres",
                                                                  "too heavy", "thats a lot",
                                                                  "that's a lot", "rip off",
                                                                  "ripped off", "overcharged",
                                                                  "overpriced", "estimate",
                                                                  "written quote", "receipt")),
    _entry("can-i-drive-it",
          (("drive", "driving", "move", "take it", "get it", "limping", "limp",
            "can i drive it", "can i drive", "is it safe to drive", "safe to drive",
            "should i drive it", "should i drive", "am i ok to drive", "is it ok to drive",
            "drivable", "still drive", "keep driving", "carry on driving"),
           ("garage", "to the garage", "home", "it there", "it home", "take it there",
            "drive it there", "get it there", "the garage",
            "mot", "mot test", "the test", "to the test", "to the mot",
            "drive it", "anywhere", "at all", "on the road",
            "miles", "tonight", "tomorrow", "overheat", "overheating", "noise",
            "rattle", "smoke")),
          "Only if the fault is not brakes, steering, a tyre or an overheating engine: those four "
          "need recovering, because a short drive can turn a cheap repair into a dangerous one, "
          "and a car with a 'dangerous' MOT fail must not be on the road at all. Anything else - a "
          "lamp, a wiper, an exhaust blow, a noisy bearing - can be driven to the garage or to a "
          "pre-booked test, slowly, with half an eye on the temperature gauge.",
          bias=1,
          guard=_a_machine_and_not_a_person,
          avoid=_NOT_BUYING + LEARNING + CLEANING + _NOT_A_THING_TO_MOVE + (
                                         "my test", "test is", "test in",
                                         "driving test", "theory", "provisional",
                                         "one pint",
                                         "two pints", "drink", "drunk", "alcohol", "points",
                                         "licence", "leave from", "park",
                                         "warning light", "engine light", "amber light",
                                         "red light", "orange light", "dashboard", "dash",
                                         "disk space", "storage", "phone", "laptop",
                                         "downloads", "space saver", "spacesaver",
                                         "spare wheel", "hire", "rental",
                                         "passport", "photo", "photos", "licence photo",
                                         "visa", "boarding pass",
                                         "moving back", "move back", "moved back", "moves back",
                                         "moving home", "back home", "homecoming",
                                         "back in with", "moving in with", "move in with",
                                         "moving house", "moving flat",
                                         "moving away from home")),
    _entry("mot-advisory", (("mot", "mot pass"), ("passed", "pass", "advisory", "advisories",
                                                 "but", "needs", "recommended")),
          "An advisory is not a fail, so you can keep driving while you sort it, but it is the "
          "garage telling you what will fail next year. Tyres, brakes and a leaking shock are worth "
          "doing in the next few weeks rather than at the last minute, and any garage will quote "
          "from the sheet.",
          bias=1, avoid=_NOT_BUYING + ("how often", "how long", "every year", "first mot",
                                       "first time", "expires", "expiry", "valid",
                                       "this year", "exempt", "exemption", "historic",
                                       "do i need", "still need", "need an mot", "needs an mot")),
    _entry("sell-my-car", (("sell", "selling", "sold", "sale", "sell it", "sell my car",
                            "selling my car", "part exchange", "trade in", "trade it in",
                            "buyer", "buyers", "bank transfer", "paypal", "pay pal",
                            "overpaid", "paid me too much", "paid too much for", "courier",
                            "screenshot", "difference back", "money back"),
                           ("car", "cars", "vehicle", "van", "motorbike", "motorcycle",
                            "buyer", "buyers", "viewing", "test drive", "advert", "autotrader",
                            "v5c", "log book", "logbook", "keys", "collection")),
          ("Sell it on the photos and the price: every side and the inside, washed, and the "
           "mileage, year and MOT date in the first line, priced against what the same car is "
           "actually selling for. Take a bank transfer and wait until the money is in your "
           "account - a screenshot of a payment is not a payment - before you hand over the keys; "
           "nobody genuine overpays and asks for the difference back, and nobody genuine sends a "
           "courier. Sign the V5C/2 slip over to the buyer, keep the rest of the log book, and "
           "tell DVLA online the same day or the tax and any fines stay yours."),
          avoid=("repair", "repairs", "repairing", "fix", "fixing", "garage", "mechanic",
                 "labour", "mot", "service", "clutch", "cambelt", "tyre", "tyres", "battery",
                 "exhaust", "worth fixing", "worth it", "scrap", "buy a", "buying a",
                 "i paid", "i bought", "paid for", "sold to me", "dealer sold",
                 "insurance", "tax it", "how much is", "price of", "cost of"),
          ask=("how", "where", "what", "should", "can i", "do i", "someone", "buyer", "paid",
               "pay", "paying", "payment", "transfer", "advert", "sell", "selling"),
          guard=_the_selling_is_the_decision),
    _entry("repair-or-scrap", (("car", "cars", "mot", "garage", "mileage", "vehicle", "mechanic"),
                              ("scrap", "scrapping", "scrap it", "scrapped", "worth fixing",
                               "write it off", "written off", "fix it",
                               "worth it", "worth the money", "worth mending", "fixing it",
                               "keep spending", "keep throwing", "get rid of it", "get rid",
                               "worth a repair", "bother",
                               "fix mine", "fixing mine", "repair mine", "car or fix",
                               "fix the old", "fix my old", "fixing the old", "keep fixing",
                               "keep repairing", "keep it going", "buy a new one",
                               "buy another", "get a new one", "get another one",
                               "replace it", "replace the old", "fix or replace",
                               "repair or replace", "replace or repair", "fix or buy",
                               "repair or buy", "buy or fix", "time to replace",
                               "worth repairing", "worth keeping",
                               "fix mine", "fix my own", "mend mine", "or fix", "buy a new car or",
                               "new car or", "or keep",
                               "sell it", "sell her", "or sell", "sell or", "keep it",
                               "keep or sell", "sell or keep", "sell it as is", "sell as is",
                               "fix it first", "sell it first", "should i sell", "should i scrap",
                               "scrap it", "scrap my car", "scrapping my car", "scrapyard",
                               "needs work", "needs 800", "needs 900", "needs 1000",
                               "needs a lot of work", "of work", "spend money on",
                               "put money into", "spend on it")),
          _money_against_value,
          bias=1,
          ask=("worth it", "worth the money", "worth repairing", "worth fixing", "worth mending",
               "worth a repair", "shall i", "should i", "scrap", "scrapping", "get rid", "new one",
               "new car", "replace", "replacing", "bother", "keep fixing", "keep repairing",
               "keep spending", "keep throwing", "keep it going", "fixing or", "repair or",
               "or repair", "or replace", "fix or", "buy or", "write it off", "buy a new",
               "or fix", "fix mine", "fixing mine", "repair mine", "car or fix",
               "time to replace",
               "sell it", "or sell", "sell or", "keep it", "or keep", "keep or sell",
               "sell or keep", "should i sell", "should i scrap", "scrap it", "scrapyard",
               "needs work", "needs 800", "needs 900", "of work", "spend money on"),
          avoid=("phone", "laptop", "boiler", "fridge", "washing machine", "sofa", "dishwasher",
                 "telly", "tv", "computer", "bike", "bicycle", "pushbike",
                 "inspection", "inspections", "inspecting", "checked over", "pre purchase",
                 "pre-purchase", "aa check", "rac check", "vehicle check", "vehicle inspection",
                 "history check", "hpi", "hpi check", "buyers report", "buyer's report",
                 "vehicle history", "test drive",
                 "door", "doors", "roof", "roofing", "shed", "gate", "gates", "opener",
                 "battery", "batteries", "tyre", "tyres", "tire", "tires", "puncture",
                 "windscreen", "windshield", "chip", "scratch", "scratches", "scratched",
                 "paint", "radio", "stereo", "speaker", "speakers", "alloy", "alloys",
                 "cambelt", "cam belt", "timing belt", "timing chain", "wiper", "wipers",
                 "how do i", "how to", "how can i", "myself", "yourself", "diy",
               "trade in", "trade-in", "part exchange", "privately", "private sale",
               "we buy any car", "webuyanycar", "autotrader", "dealer", "dealership")),
    _entry("scrap-my-car", (("scrap", "scrapping", "scrapped", "scrapyard", "scrap yard",
                             "breaker", "breakers", "certificate of destruction",
                             "authorised treatment", "atf", "weigh it in", "weighing it in",
                             "get rid of", "getting rid of", "rid of my", "rid of the",
                             "get rid of my car", "get rid of the car",
                             "how do i scrap", "how to scrap", "how can i scrap",
                             "where can i scrap", "where do i scrap", "scrapping a car",
                             "scrap a car", "scrap my car", "scrap my old car",
                             "to the scrapyard",
                             "dispose of", "disposing of", "do with an old car",
                             "do with my old car", "get rid of an old car"),
                            ("car", "cars", "vehicle", "van", "motorbike", "motorcycle",
                             "paperwork", "dvla", "v5c", "log book", "logbook", "plates",
                             "number plate", "private plate", "keys", "wheels", "tyres")),
          ("Take it to an Authorised Treatment Facility - a scrapyard that takes whole cars and "
           "gives you a Certificate of Destruction - because that certificate is the proof the "
           "car is gone. Hand over the V5C and the keys, keep the certificate, and tell DVLA "
           "yourself the same day so the tax, the insurance and any fines stop with you. Empty "
           "everything out first, and take a private plate off before it goes on the truck. "
           "Expect £150 to £400 for a small car, paid by weight."),
          ask=("how", "where", "what do i", "paperwork", "dvla", "can i", "do i", "want to",
               "need to", "plan to", "going to", "take", "taking", "get rid"),
          avoid=("should i", "worth", "worth it", "how much will", "how much do i get",
                 "how much is", "better", "or sell", "or keep", "or fix", "or repair",
                 "or buy", "fix or", "sell or", "keep or", "my car is worth"),
          bias=2),
    _entry("repair-cost", (("car", "cars", "vehicle", "garage", "garages", "mechanic", "repair",
                            "repairs", "fix", "fixing", "job on", "job done", "mend", "mending"),
                           ("cost", "costs", "much", "price", "prices", "priced", "charge",
                            "charged", "charging", "quote", "quoted", "estimate", "labour",
                            "hour", "rate", "pay", "spend", "roughly", "typical", "average")),
          REPAIR_COST,
          bias=1,
          ask=("repair", "repairs", "repairing", "fix", "fixing", "fixed", "job on",
               "job done", "garage", "garages", "mechanic", "labour", "goes wrong", "work done"),
          guard=_the_trade_is_named,
          avoid=_NOT_BUYING_SALE + (
                 "roof", "roofs", "roofing", "roofer", "roofers", "gutter", "gutters", "chimney",
                 "fence", "fencing", "patio", "driveway", "conservatory", "loft", "extension",
                 "plaster", "plastering", "render", "brick", "brickwork", "wall", "walls",
                 "ceiling", "tiling", "tiles", "damp", "plumber", "plumbers", "electrician",
                 "electricians", "builder", "builders", "decorator", "decorators", "drain",
                 "drains", "socket", "sockets", "wiring", "fuse board", "radiator", "radiators",
                 "garden", "shed", "kitchen", "bathroom",
                 "tap", "taps", "faucet", "faucets", "leak", "leaks", "leaking", "leaked",
                 "sink", "sinks",
                 "toilet", "toilets", "cistern", "flush", "flushes", "shower",
                 "showers", "bath", "baths", "plug", "plughole", "plumbing", "pipe", "pipes",
                 "stopcock", "blockage", "blocked", "unblock", "grout", "skirting", "door handle",
                 "mot", "service", "clutch", "cambelt", "timing belt", "exhaust", "tyre", "tyres",
                 "tire", "tires", "battery", "insurance", "road tax", "tax", "fuel", "petrol",
                 "diesel", "running cost", "a year", "per year",
                 "boiler", "washing machine", "fridge", "dishwasher", "oven", "phone", "laptop",
                 "computer", "telly", "tv", "bike", "bicycle",
                 "mortgage", "remortgage", "lender", "loan", "energy", "tariff", "price cap",
                 "fixed rate", "variable rate", "fixed tariff", "variable tariff",
                 "energy rate", "on a fixed", "fix my rate", "fix the rate", "fixing my rate",
                 "unit rate", "standing charge", "kwh",
                 "savings", "isa", "pension", "insurance premium",
                 "should i charge", "charge for a job", "charge for my", "for my work",
                 "my day rate", "day rate",
                 "self employed", "self-employed", "freelance", "my hourly", "a job",
                 "take the job", "taking the job", "accept the job", "accepted the job",
                 "job offer", "job offers", "offered the job", "offered a job",
                 "longer hours", "more hours", "extra hours", "fewer hours", "less hours",
                 "shift work", "night shift", "my boss", "my manager", "my employer",
                 "promotion", "career change", "quit my job", "leave my job",
                 "notice period", "salary", "my job is", "my job's", "my jobs",
                 "new job", "job pays", "job that pays", "jobs that pay")),
    _entry("repair-cost-follow-up",
           ("cost", "costs", "costing", "much", "price", "priced", "roughly", "quote",
            "quoted", "estimate", "charge", "charged", "pay"),
           REPAIR_COST,
           bias=1,
           guard=no_broken_car_or_none,
           avoid=("sell", "selling", "sold", "sale", "worth", "buy", "buying", "bought",
                  "trade in", "part exchange", "insurance", "insured", "tax", "road tax",
                  "mot", "service", "servicing", "fuel", "petrol", "diesel", "lease",
                  "hire purchase", "pcp", "scrap", "scrappage", "write off", "written off",
                  "roof", "boiler", "washing machine", "laptop", "phone", "mortgage",
                  "energy", "tariff")),
    _entry("service-due", (("service", "servicing", "oil change", "full service"),
                           ("car", "due", "interval", "mileage", "year", "cost", "book", "when",
                            "how often", "charge", "charges", "price", "much", "full")),
          "Most cars want a service every 12 months or 10,000 to 12,500 miles, whichever comes "
          "first, and an oil and filter change is the part that matters most. A minor service is "
          "usually £150 to £250; the handbook's schedule is the one to follow, not the garage's "
          "upsell.",
          avoid=("customer", "train", "bus", "restaurant", "hotel", "boiler", "central heating",
                 "gas", "combi", "furnace", "warranty", "washing machine", "dishwasher"),
          ask=("car", "cars", "van", "garage", "vehicle", "mot", "mileage", "handbook", "mile",
               "full service")),
    _entry("oil-check", (("oil", "oil change", "oil level", "oil filter", "oil grade"),
                         ("dipstick", "level", "low", "empty", "check", "top up", "topping",
                          "light", "warning", "change", "black", "dark", "dirty", "milky",
                          "foamy",
                          "engine", "how often", "how long",
                          "when", "interval", "miles", "mileage", "much", "need",
                          "capacity", "litres", "liters", "every", "overfill",
                          "overfilled", "overfilling", "too full", "do", "does",
                          "job", "why", "for", "which", "grade", "synthetic",
                          "filter", "viscosity", "spec", "cost", "costs", "price",
                          "expensive", "cheap")),
          _oil_reply,
          avoid=("cooking", "fry", "frying", "cake", "olive", "salad", "hair", "essential",
                 "lawnmower", "mower", "motorbike", "motorcycle", "bike", "chainsaw", "boat",
                 "breadmaker", "bread maker",
                 "chips", "chip", "chip pan", "fries", "batter", "doughnut", "donut",
                 "frying pan", "deep fry", "deep fryer", "deep-fat", "oil for chips"),
          ask=("car", "engine", "dipstick", "bonnet", "van", "my oil", "the oil", "check my oil",
               "oil level", "top up my oil", "how much oil", "oil change", "change my oil",
               "change the oil", "oil needs changing")),
    _entry("oil-light", (("oil light", "oil warning", "oil pressure light", "oil pressure",
                          "oil pressure warning light"),
                         ("on", "came on", "stop", "flashing", "flickers", "red",
                          "mean", "means", "what", "why")),
          "A red oil light means stop as soon as it is safe and switch the engine off: it is oil "
          "pressure, and driving even a mile can wreck the engine. Check the level once it has "
          "cooled; if the level is fine and the light is still on, it needs a tow, not a drive.",
          avoid=("tyre", "tyres", "tire", "tires", "puncture", "punctures", "tread", "tpms",
                 "tpm", "wheel", "wheels", "brake", "brakes", "coolant", "washer",
                 "screen wash", "fuel", "power steering"),
          bias=3),

    _entry("engine-light", (("engine light", "engine warning light", "warning light", "management light",
                            "check engine", "engine management"),
                           ("on", "came on", "flashing", "amber", "orange", "mean", "means", "what",
                            "dash", "dashboard")),
          "A steady amber engine light means 'get it checked soon' and the car is usually fine to "
          "drive gently; a flashing one means stop, because a misfire can wreck the catalytic "
          "converter. Before panicking, check the fuel cap is tight and on properly: it is the "
          "cheapest cause there is. A garage reads the code for £20 to £50.",
          avoid=_NOT_BUYING + ("boiler", "furnace", "heating")),

    _entry("dash-light",
           (("brake light", "brake warning light", "handbrake light", "handbrake warning light",
             "parking brake light", "brake fluid light",
             "abs light", "abs warning light", "abs warning", "anti-lock light", "anti lock light",
             "dpf light", "dpf warning", "particle filter light", "diesel particle light",
             "exhaust filter light",
             "airbag light", "airbag warning", "air bag light", "srs light",
             "airbag warning light",
             "battery light", "battery warning light", "charging light", "alternator light",
             "tyre pressure light", "tyre light", "tpms light", "tire pressure light",
             "tyre pressure warning", "flat tyre light", "flat tire light",
             "power steering light", "power steering warning", "steering light",
             "traction light", "traction control light", "esp light", "esc light",
             "skid light", "slippery light",
             "glow plug light", "glowplug light", "preheat light",
             "adblue light", "ad blue light", "adblue warning", "urea light",
             "service light", "spanner light", "service due light", "service indicator",
             "washer fluid light", "screen wash light", "washer warning", "washer fluid",
             "screen wash warning",
             "seatbelt light", "seat belt light", "seatbelt warning", "belt light",
             "brake pad light", "pad wear light", "brake pad warning", "wear indicator",
             "key light", "key symbol", "immobiliser light", "immobilizer light",
             "key warning light",
             "abs", "dpf", "airbag", "adblue", "tpms"),
            ("light", "lights", "lit", "warning", "symbol", "dash", "dashboard", "on",
             "came on", "comes on", "come on", "stays on", "staying on", "flashing",
             "flashes", "flickering", "mean", "means", "what", "why", "glowing")),
          _dash_light_reply,
          guard=_the_abs_is_in_a_car,
          avoid=_NOT_BUYING + ("engine light", "engine warning", "management light",
                               "oil light", "oil pressure", "oil warning", "oil level",
                               "overheating", "overheat", "temperature gauge", "coolant",
                               "boiler", "central heating", "smoke alarm", "washing machine",
                               "dishwasher", "phone", "laptop", "mower", "lawnmower",
                               "bike", "bicycle", "motorbike", "motorcycle", "puncture repair",
                               "tread depth", "how much tread",
                               "bulb", "bulbs", "blown", "is out", "are out", "went out",
                               "not working", "dont work", "doesnt work",
                               "do not work", "does not work", "arent working",
                               "isnt working", "failed", "fail", "mot", "mot test"),
          bias=3),
    _entry("overheating", (("overheat", "overheating", "temperature gauge", "steam", "hot"),
                          ("engine", "car", "coolant", "radiator", "gauge", "bonnet")),
          "Pull over, switch the engine off and let it cool for at least 20 minutes; never open the "
          "coolant cap while it is hot, because it will scald you. Once cool, check the coolant level "
          "and look for a leak or a split hose; if it overheats again, stop driving and get it "
          "recovered, because a warped head is a very expensive repair.",
          avoid=("oven", "pan", "boiler", "radiator valve", "bleed", "house", "bedroom",
                 "central heating",
                 "steaming up", "steamed up", "steam up", "steams up", "steamy windows",
                 "windscreen", "windshield", "demist", "demisting", "fogged", "fogging",
                 "misted", "condensation"),
          ask=("engine", "car", "coolant", "bonnet", "gauge", "motorway", "van"),
          guard=lambda understood: not any(
              word in (understood.get("clean") or "") for word in
              ("dog", "dogs", "puppy", "pup", "cat", "cats", "kitten", "pet", "pets"))),
    _entry("heater-blows-cold",
           (("heater", "heating", "blowers", "blower", "hot air", "demist", "vents"),
            ("blows cold", "blowing cold", "blow cold", "only cold", "all cold", "cold air",
             "not warm", "no heat", "no hot air", "warm air", "lukewarm", "luke warm")),
          "With the engine up to temperature, cold air from the vents is nearly always the coolant "
          "level or an airlock in the heater matrix: check the level when the engine is cold and "
          "top it up to the mark, then run it with the heater on full and the cap off to bleed it. "
          "If the level keeps dropping there is a leak to find, which is the overheating job first. "
          "On a car that holds its coolant, the suspects in order are the thermostat stuck open, a "
          "blocked heater matrix and the blend flap not moving, which a garage diagnoses in an "
          "hour or two.",
          ask=("heater", "heaters", "blowers", "blower", "vents", "demist", "hot air", "car")
              + ("heat my car", "heat my van", "heat the car", "heat the van",
                 "heating my car", "heating my van", "heating the car", "heating the van",
                 "warm my car", "warm my van", "warm the car", "warm the van",
                 "warm up my car", "warm up my van")
              + MODELS,
          avoid=NOT_BIKE + ("boiler", "boilers", "central heating", "radiator", "radiators",
                            "house", "home", "room", "bedroom", "living room", "kitchen",
                            "thermostat at home", "heat pump", "underfloor", "towel rail",
                            "log burner", "wood burner", "fireplace", "tumble dryer")),
    _entry("coolant-low", (("coolant", "antifreeze"), ("level", "top up", "check", "low", "add",
                                                       "mix", "water", "reservoir", "use", "what")),
          "Top the coolant up when the engine is cold, to between the min and max marks, using the "
          "mix in the handbook (usually 50/50 antifreeze and water). If you are topping it up more "
          "than once in a few months, there is a leak to find before it strands you."),
    _entry("engine-noise", (("engine", "car"), ("noise", "noisy", "rattle", "rattling", "knocking",
                                                "tapping", "whine", "loud")),
          "Note when the noise happens before you take it in: tapping when cold that fades is often "
          "the oil being slow to circulate, a rattle over bumps is usually a heat shield or "
          "exhaust mount, and a whine that rises with speed is a bearing or gearbox. A metallic "
          "knock or grinding means stop driving and get it looked at.",
          avoid=_NOT_BUYING + ("brake", "brakes", "braking", "steering", "clutch", "exhaust",
                               "wipers", "window", "door", "tyre", "tyres",
                               "clicking noise bad", "click noise bad", "clunking noise bad",
                               "knocking noise bad")),
    _entry("cooling-fan-runs-on", (("fan", "cooling fan", "radiator fan", "fan noise",
                                    "engine keeps running", "engine keeps going", "engine runs on",
                                    "engine wont stop", "engine won't stop", "motor keeps running"),
                                   ("keeps", "keeping", "running", "runs", "run on", "runs on",
                                    "after", "turn off", "turned off", "switched off", "switched it off",
                                    "switch off", "stay on", "stays on", "wont stop", "won't stop")),
          "That is normal: the cooling fan runs on for a few minutes after you switch off, to pull "
          "the heat out of the engine bay, and it can start by itself on a hot day even when the car "
          "has been parked a while. Ten or fifteen minutes then silence is fine. If it runs much "
          "longer than that, runs every time you stop, or leaves you with a flat battery, the "
          "coolant or the fan switch needs looking at.",
          ask=("car", "engine", "van", "motor", "radiator", "bonnet"),
          avoid=("bathroom", "extractor", "shower", "kitchen", "cooker", "oven", "hob",
                 "laptop", "pc", "computer", "desktop", "console", "playstation", "xbox",
                 "boiler", "bedroom", "ceiling", "house")),
    _entry("exhaust-noise",
           (("exhaust", "exhausts", "back box", "backbox", "silencer", "exhaust pipe",
             "exhaust system"),
            ("loud", "louder", "noisy", "noise", "blowing", "blow", "blown", "rattling",
             "rattle", "banging", "bangs", "booming", "droning", "droning noise", "hole",
             "leak", "leaking", "hanging", "hanging down", "fell off", "fallen off", "came off",
             "why", "suddenly", "got louder", "sounds like", "sounds awful",
             "louder than", "louder now", "louder this week",
             "fix", "fixed", "repair", "repairs", "replace", "replacing", "weld")),
          "A suddenly louder exhaust is nearly always a hole or a blown joint: the back box, the "
          "flange where two sections meet, or a pipe rusted through, and it booms loudest when you "
          "accelerate. It is not an emergency, but fumes can get into the cabin, so keep a window "
          "open and never sit with the engine running in a garage. A garage can sleeve or weld a "
          "small hole, or fit just that section, for far less than a whole system, and one hanging "
          "loose wants doing before it drops off. Down on power too, or the engine light on, means "
          "the manifold or a sensor wants a look.",
          ask=("car", "cars", "van", "engine", "exhaust", "back box", "silencer", "motorway"),
          lead=("yesno", "It is not an emergency"),
          avoid=_NOT_BUYING + ("boiler", "flue", "chimney", "extractor", "cooker", "oven", "hob",
                               "bathroom", "fan", "house", "smoke", "smoking", "fumes", "smell",
                               "fragrance", "perfume", "aerial", "roof rack", "sound system",
                               "speaker", "speakers", "stereo", "music", "radio", "heater",
                               "heating", "aircon", "air con", "suspension", "wheel bearing",
                               "battery", "tyre", "tyres",
                               "illegal", "legal", "the law", "law", "mot", "fail",
                               "make it louder", "make my exhaust louder",
                               "make my car louder", "louder on purpose", "sportier",
                               "sporty", "sound better", "louder exhaust",
                               "a louder", "get a louder", "how loud")),

    _entry("exhaust-and-the-law",
           (("exhaust", "exhausts", "silencer", "back box", "muffler", "tailpipe"),
            ("illegal", "legal", "the law", "law", "mot", "fail", "fails", "fail the mot",
             "too loud", "allowed", "permitted", "police", "fine", "ticket", "complaint",
             "neighbour", "neighbours", "make it louder", "make my exhaust louder",
             "make my car louder", "louder on purpose", "sportier", "sporty", "sound better",
             "sounds better", "better sound", "nicer sound", "louder exhaust", "a louder",
             "get a louder", "how loud", "noise limit", "decibels", "too much noise",
             "neighbour", "neighbours", "neighbor", "neighbors")),
          "Not illegal as such: what is checked is that the exhaust is secure, gas-tight and no "
          "noisier than the car was built to be, so a hole, a blown joint or a missing baffle "
          "fails an MOT and wants mending, while an exhaust that has simply got loud with age is a "
          "repair rather than an offence. Making one deliberately louder is where people get "
          "caught - it can fail the test and a police officer can ask for it to be put right - so "
          "a replacement that stays within the standard noise is the only safe way to get a "
          "better note.",
          ask=("car", "cars", "van", "mot", "exhaust", "silencer", "muffler"),
          avoid=_NOT_BUYING + ("boiler", "flue", "chimney", "extractor", "cooker", "oven", "hob",
                               "bathroom", "fan", "house", "smoking", "fumes", "smell",
                               "fragrance", "perfume", "heater", "heating", "aircon", "air con",
                               "how much", "cost", "price", "cheaper", "noisy neighbour",
                               "noisy neighbours", "music", "stereo", "speaker")),
    _entry("exhaust-smoke", (("smoke", "smoking"), ("exhaust", "car", "engine", "white", "blue", "black")),
          "Black smoke is too much fuel, blue smoke is burning oil, and thick white smoke that "
          "doesn't clear is coolant getting into the engine. A puff of white on a cold morning is "
          "just steam and is normal; the other three want a garage soon."),

    _entry("driving-test-failed",
           (("failed my driving test", "fail my driving test", "failing my driving test",
             "failed my test", "failed the driving test", "failed my driving exam",
             "didnt pass my driving test", "didn't pass my driving test",
             "keep failing my driving test", "keep failing my test",
             "failed again", "failed my second test", "failed my third test"),
            ("what", "how", "should", "do i", "next", "again", "advice", "help", "now",
             "failed", "fail", "failing", "test", "todays test", "today", "gutted", "keep")),
           "Sorry to hear it - it is a common day and it is not a verdict. Book the next test as "
           "soon as the ten clear working days are up, and take the sheet the examiner gave you "
           "to your instructor: it lists every fault as a driving, serious or dangerous one, and "
           "the serious and dangerous ones are what failed you. Spend the "
           "lessons between now and then on those two or three things only, and one extra lesson "
           "in the week of the test rather than ten. Most people pass on the second or third go, "
           "so a fail is a date, not a verdict.",
           avoid=("how many lessons", "how long does it take", "renew", "renewal", "expired",
                  "provisional", "theory test", "before my test", "first test", "book my test",
                  "test date", "test booked")),

    _entry("book-driving-test",
           (("driving test", "practical test", "theory test", "driving test booking",
             "test booking", "driving exam"),
            ("book", "booking", "booked", "cost", "much", "price", "how", "when", "where",
             "change", "cancel", "cancel it", "earlier", "sooner", "wait", "waiting", "slot",
             "rearrange", "move it", "date", "failed", "fail")),
           "Book the theory test first at gov.uk - it is £23 and the pass lasts two years - and "
           "the practical only after it, because a practical booking needs the theory pass "
           "number. The practical is £62 on a weekday and £75 for an evening, weekend or bank "
           "holiday, and the test centre slots come up 6 to 24 weeks out by area, so take the "
           "first one that has a warm-up lesson the day before rather than holding out for a "
           "perfect date. Cancelling or moving it needs five clear working days or you lose the "
           "fee; the car has to be taxed, insured for the test and have a second mirror for the "
           "examiner, and the licence goes with you.",
           avoid=("how many lessons", "how long does it take", "how many hours", "hours of",
                  "nervous", "nerves", "terrified", "scared", "panic", "anxious",
                  "after failing", "i failed", "failed my", "failed the", "gutted",
                  "is it worth", "too old", "too late", "what age")),

    _entry("giving-up-driving",
           (("give up driving", "giving up driving", "gave up driving", "given up driving",
             "give up my driving", "give up the car", "giving up the car", "give up my licence",
             "giving up my licence", "gave up my licence", "given up my licence",
             "stopped driving", "stop driving", "stopping driving", "had to stop driving",
             "cant drive anymore", "cant drive any more", "can't drive anymore",
             "can't drive any more", "cannot drive anymore", "cannot drive any more",
             "not driving anymore", "no longer drive", "no longer driving",
             "cant drive now", "cant drive again", "cant drive at night",
             "cant drive in the dark", "cant drive because", "cant drive since",
             "doctor says i cant drive", "doctor said i cant drive", "says i cant drive",
             "told i cant drive", "not safe to drive", "not allowed to drive",
             "surrendered my licence", "surrender my licence", "surrender my driving licence",
             "hand back my licence", "hand in my licence", "handed back my licence",
             "too old to drive now"),
            ("drive", "driving", "car", "licence", "license", "road", "anymore", "any more",
             "no longer", "stopped", "stop", "give up", "giving up", "gave up", "surrender",
             "hand back", "hand in", "doctor", "eyes", "eyesight", "dark", "night", "since",
             "again")),
           "Giving up driving is three jobs, and doing them in this order makes it much easier. "
           "First the official side: if the reason is medical, tell the DVLA, because a licence "
           "you should not be using is not valid for insurance, and tell your insurer either way. "
           "Second, the money: insurance, tax, MOT, servicing and fuel usually add up to enough "
           "for a taxi or two a week, so that sum becomes the new travel budget instead of "
           "disappearing quietly. Third, the alternatives, arranged before the keys go rather "
           "than after: a bus pass, the local dial-a-ride or community car scheme, and a rota of "
           "two or three people for the trips that matter, because one lift is easier to ask for "
           "than a favour you think you cannot repay. Keep the car a month if you can, so the "
           "first week is not also the week you learn the bus.",
           avoid=("how many", "how long", "lessons", "lesson", "instructor", "theory",
                  "provisional", "learn to drive", "learning to drive", "passed my test",
                  "failed", "fail", "nervous", "at 17", "at 18", "first car", "buy a car",
                  "cheap car", "insurance quote", "mot", "tax", "parking", "clutch", "brakes",
                  "golf", "slice", "slicing", "hook", "swing", "tee", "irons", "driver",
                  "birthday", "present", "gift", "what should i get")),

    _entry("learn-to-drive-hours", (("driving lessons", "driving lesson", "driving test",
                                     "learn to drive", "learning to drive", "driving instructor",
                                     "theory test", "provisional licence", "provisional",
                                     "drive", "drive a car"),
                                    ("how many", "how long", "take", "takes", "hours", "cost",
                                     "40", "50", "60", "later", "old", "need", "start",
                                     "nervous", "fail", "book",
                                     "how to learn", "how do i learn", "how can i learn",
                                     "how do i start", "how do i get",
                                     "begin", "beginners", "get started", "first",
                                     "want to", "i want", "cant", "can't", "cannot",
                                     "never learnt", "never learned")),
           "Most people need around 45 hours of lessons plus 20 hours of private practice before "
           "they pass, so two lessons a week gets you there in about six months at 40 just as at "
           "18. Lessons run 25 to 40 pounds an hour, and a block with one instructor beats single "
           "lessons with three. Do the theory test early, because the pass lasts two years, and ask "
           "the price of a test-day car hire before you book the test.",
           guard=no_broken_car,
           avoid=("fuel", "mpg", "petrol", "diesel", "electric", "charging", "parking", "park",
                  "motorway", "roundabout", "snow", "ice", "fog", "insurance", "tax", "mot",
                  "tyre", "tyres", "oil", "engine", "battery", "brakes", "clutch", "gears",
                  "drive to", "drive from", "the drive", "drive be", "drive there", "traffic",
                  "route", "journey", "how far", "miles", "roadworks",
                  "lesson horse", "riding lesson", "swimming lesson", "piano lesson", "failed",
                  "fail", "failing", "gutted", "today", "nervous", "nerves", "scared",
                  "worried", "anxious", "panic", "terrified",
                  "units", "unit", "pint", "pints", "drunk", "alcohol", "beer", "wine",
                  "lager", "vodka", "breathalyser", "over the limit", "drink driving",
                  "drink-driving", "sober up",
                  "theory", "hazard perception", "multiple choice", "dvsa", "revision",
                  "revise",
                  "how do i drive in", "how do i drive on", "how do i drive at",
                  "how do i drive through", "how do i drive with", "how to drive in",
                  "how to drive on", "how to drive at", "how do i drive an",
                  "driving in the rain", "driving at night", "driving on a dual",
                  "driving on the motorway", "drive an automatic", "drive an electric")),

    _entry("brakes-noise", (("brake", "brakes", "braking"), ("squeal", "squealing", "squeak",
                                                            "grinding", "metal", "noise", "noisy",
                                                            "soft", "spongy", "pedal", "warning light")),
          "Grinding means the pads are down to metal: stop driving and get them changed, or you will "
          "score the discs too. A squeal is often the wear indicator or glazed pads, and a pedal that "
          "feels soft or sinks means air or a fluid leak, which is a garage-now job. Front pads "
          "fitted are usually £100 to £200.",
          avoid=_NOT_BUYING + ("bike", "bicycle", "cycle", "trampoline")),
    _entry("motorway-driving",
           (("motorway", "motorways", "dual carriageway", "dual carriageways", "m6", "m25", "m1"),
            ("how do i", "how can i", "first time", "drive", "driving", "join", "joining",
             "slip road", "lane", "lanes", "overtake", "overtaking", "exit", "junction",
             "nervous", "scared", "tips", "advice", "learner", "speed", "fast")),
           "Join on the slip road at the speed of the traffic already there, because arriving slowly "
           "is the thing that makes it frightening: mirror, indicate, then match the lorries in the "
           "left lane. Keep left unless you are overtaking, leave a two-second gap to the car in "
           "front (double it in rain, and further in spray at night), and do not sit alongside a "
           "lorry where the driver cannot see you. Plan the exit a mile ahead - the countdown "
           "markers start at three - and slow down on the slip road, not in the left lane. If you "
           "miss it, carry on to the next junction; there is no reversing on a motorway.",
           avoid=("service station", "services", "toll", "tolls", "dart charge", "fuel at",
                  "parking at", "hotel", "travelodge", "stop on the way", "road trip",
                  "breakdown cover", "recovery", "kids", "children", "toddler")),
    _entry("roundabouts",
           (("roundabout", "roundabouts", "round about", "mini roundabout",
             "mini-roundabout"),
            ("how do i", "how can i", "use", "using", "drive", "driving", "negotiate", "lane",
             "lanes", "which lane", "left", "right", "signal", "signalling", "indicate",
             "mirror", "first time", "nervous", "scared", "tips", "advice")),
           "Pick your lane on the approach and stay in it: left for the first exit or straight on, "
           "right-hand lane for anything past twelve o'clock, and use the left lane again for the "
           "last exit. Mirror, then signal left just after the exit before yours, and give way to "
           "traffic already on the roundabout - it comes from your right, but on a roundabout the "
           "give-way line is the rule, not a right of way. On a mini roundabout you still go round "
           "the white circle, not over it, and if you miss your exit carry on round again.",
           avoid=("route", "directions", "sign", "signs", "closed", "accident", "crash",
                  "congestion", "traffic", "lane closed", "m25", "m6", "m1", "a road",
                  "double roundabout", "magic roundabout")),
    _entry("driving-in-rain",
           (("rain", "raining", "wet road", "wet roads", "wet", "spray", "spraying",
             "heavy rain", "downpour", "flood", "flooded", "flooding", "puddle", "puddles",
             "wet leaves", "standing water", "aquaplane", "aquaplaning",
             "storm", "storms", "thunderstorm", "thunderstorms", "gale", "gales", "gusts"),
            ("drive", "driving", "how do i", "how can i", "tips", "advice", "nervous",
             "car", "road", "roads", "stop", "skid", "skidding", "brake", "braking", "slow",
             "speed", "mist", "spray", "first time")),
           "Slow down before the water, not in it: at 50mph a tyre has to shift a bucketful of "
           "water a second, and above about 60mph it can start to float, which is aquaplaning. "
           "Leave double the gap you would leave dry, put the lights on so the spray behind you "
           "shows up, and brake gently and earlier - a wet road takes much longer to stop on. If "
           "the steering goes light, ease off the accelerator and hold the wheel straight until "
           "the tyres grip again; do not brake hard. A road under water deeper than the tyre's "
           "tread is worth turning round for, and wet leaves at a junction are as slick as ice.",
           avoid=("in my car", "in the car", "inside the car", "footwell", "footwells",
                  "got wet", "soaked", "damp", "musty", "mouldy",
                  "roof", "leak", "leaking", "gutter", "gutters", "washing", "laundry", "dog",
                  "coat", "jacket", "boots", "shoes", "window", "windows misted", "demist",
                  "wipers", "windscreen", "train", "bus", "ferry", "flight", "holiday",
                  "forecast", "umbrella", "picnic", "bbq", "barbecue", "garden", "lawn")),
    _entry("hill-start",
           (("hill start", "hill starts", "hill", "hills", "slope", "incline", "steep hill",
             "up a hill", "on a hill"),
            ("start", "starting", "how do i", "how can i", "drive", "driving", "pull away",
             "pulling away", "roll back", "rolling back", "stall", "stalls", "clutch",
             "tips", "advice", "test")),
           "Set the handbrake, bring the clutch up to the biting point until the bonnet lifts a "
           "little, then add a touch more gas and release the handbrake as the car starts to pull - "
           "that order is what stops the roll back. On a steep hill use more gas and let the clutch "
           "out more slowly, and if it stalls put the handbrake on before you restart. Going up a "
           "long hill, change down early: a lower gear holds the speed better than more throttle "
           "in a high one. Going down, use the same lower gear to hold the speed and brake gently, "
           "rather than riding the brakes all the way.",
           avoid=("park", "parking", "parked", "wheel", "wheels", "handbrake on a hill",
                  "walk", "walking", "hike", "hiking", "house", "garden", "driveway", "roof")),
    _entry("driving-a-van",
           (("van", "vans", "transit", "luton", "campervan", "motorhome"),
            ("drive", "driving", "how do i", "first time", "tips", "advice", "reverse",
             "reversing", "park", "parking", "different", "like", "nervous")),
           "A van up to 3.5 tonnes drives on an ordinary full licence and much like a big car, but "
           "it is wider, taller and has no rear window in most panel vans, so you drive it on the "
           "two side mirrors. Set both mirrors out a little further before you move, take corners "
           "wider than feels natural because the back wheels cut inside, and reverse slowly with a "
           "second person behind you if there is one. Remember the height: a standard van is often "
           "over two metres, so check the barrier or car-park limit before you drive in.",
           avoid=("hire", "hiring", "rent", "rental", "buy", "buying", "buy one", "for sale",
                  "licence", "license", "insurance", "cost", "how much", "weight", "tonnes",
                  "moving house", "removal", "sleep in", "camping", "electric",
                  "into a van", "into the van", "in the van", "in the back of the van",
                  "onto a van", "on the van", "into my van", "sofa", "couch", "armchair",
                  "fridge", "freezer", "washing machine", "washer", "tumble dryer",
                  "mattress", "wardrobe", "piano", "table", "sideboard", "bookcase",
                  "sack truck", "tail lift", "straps", "ratchet")),
    _entry("driving-in-fog",
           (("fog", "foggy", "mist", "misty", "fog lights", "fog light", "visibility",
             "hazard lights", "hazards"),
            ("drive", "driving", "how do i", "how can i", "use", "when", "should", "tips",
             "advice", "car", "light", "lights", "front", "rear", "back", "speed", "slow")),
           "In fog use dipped headlights and, only when visibility is under about 100 metres, your "
           "rear fog light - and switch it off as soon as it clears, because a bright rear light "
           "in thinning fog dazzles the driver behind and hides your brake lights. Slow down so "
           "you can stop within the distance you can see, leave a big gap, and do not follow the "
           "tail lights in front too closely, since they lead you into the same crash. Hazard "
           "lights are for a stopped queue, not for moving in fog.",
           avoid=("windscreen", "windows", "window", "car misted", "steamed", "demist", "mirror",
                  "glasses", "spectacles", "halloween", "machine", "smoke", "smoking",
                  "vape", "steam", "kettle", "bathroom", "headlights not working", "bulb")),
    _entry("automatic-car",
           (("automatic", "automatics", "automatic car", "auto", "automatic gearbox",
             "automatic transmission", "paddle shift", "flappy paddle"),
            ("drive", "driving", "how do i", "how do you", "different", "tips", "advice",
             "gear", "gears", "brake", "pedals", "left foot", "first time", "learn")),
           "An automatic has two pedals and no clutch, so your left foot does nothing at all - keep "
           "it on the floor and use only the right foot for go and stop, or you will ride the brake "
           "without knowing. Select D and the car creeps forward when you release the brake, which "
           "is what makes it easy in traffic; P is for parking, R for reverse, and N is almost "
           "never needed. Going down a long hill, drop to a lower gear (often marked L, 2 or a "
           "manual mode) to hold your speed back instead of braking all the way.",
           avoid=("licence", "license", "test", "lessons", "buy", "buying", "cost", "cheaper",
                  "insurance", "automatic doors", "washing machine", "car wash", "gearbox fault",
                  "gearbox oil", "not changing gear")),
    _entry("country-road-driving",
           (("country road", "country roads", "narrow road", "narrow roads", "single track",
             "single-track", "rural", "country lane", "country lanes", "lane driving",
             "b road", "b roads", "unlit road"),
            ("drive", "driving", "how do i", "tips", "advice", "safe", "narrow", "pass",
             "passing", "overtake", "tractor", "horse", "horses", "nervous", "first time")),
           "Assume there is something round the next bend - a tractor, a horse or a walker - so "
           "drive at a speed you could stop from within what you can see, which on a hedge-lined "
           "lane is often 30mph or less. On a single-track road use the passing places: pull in on "
           "your left to let oncoming traffic through, and do not park in one. Give horses a wide "
           "berth and pass them slowly, watch for mud and slurry on the surface after a tractor, "
           "and dip your headlights for oncoming cars at night rather than lighting up the bend.",
           avoid=("walk", "walking", "hike", "hiking", "cottage", "pub", "getaway", "holiday",
                  "move to", "house", "village", "farm", "buy a house")),
    _entry("driving-instructor",
           (("driving instructor", "driving instructors", "instructor", "instructors",
             "driving school", "learner driver", "find an instructor"),
            ("find", "choose", "choosing", "how do i", "good", "best", "recommend",
             "recommendation", "change", "change my", "how much", "cost", "should i")),
           "Ask three or four people who have just passed and book a single lesson with the one "
           "they liked most - a good instructor is the thing that makes lessons worth the money, "
           "and one lesson tells you more than any advert. Look for someone approved by the DVSA "
           "(an ADI badge on the windscreen), a quiet manner, and a lesson plan rather than being "
           "driven round for two hours. Prices are usually £30 to £45 an hour, and if you are not "
           "getting on, change early: it is normal, and a good instructor will not mind.",
           avoid=("theory", "test", "how many", "how long", "hours", "failed", "fail",
                  "yoga", "gym", "swim", "dance", "piano", "music", "school", "university")),
    _entry("driving-at-night",
           (("at night", "night time", "nighttime", "in the dark", "driving in the dark",
             "when its dark", "when it is dark", "gets dark", "after dark",
             "night driving", "driving at night", "headlights", "high beam", "main beam",
             "dazzled", "dazzle", "full beam"),
            ("drive", "driving", "driver", "road", "roads", "car", "cars", "van", "motor",
             "headlights", "headlight", "main beam", "high beam", "full beam", "dazzle",
             "dazzled", "dipped", "motorway", "lane", "lanes")),
           "Dip your headlights as soon as another car is in sight - a main beam left on dazzles "
           "the driver coming towards you for several seconds - and drop your speed, because you "
           "can only stop within the distance your lights light up. Look towards the left edge of "
           "the road when someone comes the other way with lights on, so your eyes are not fixed "
           "on theirs, and keep the windscreen and mirrors clean inside as well as out, since "
           "smears scatter oncoming light into a glare. If you are dazzled, slow down and, if you "
           "cannot see, stop where it is safe until the car has passed.",
           guard=_a_car_is_in_the_line,
           avoid=("sleep", "insomnia", "wake", "waking", "woke", "night shift", "nightmare",
                  "fall", "falls", "falling", "fell", "fallen", "trip", "trips", "tripped",
                  "tripping", "unsteady", "wobbly", "balance", "hip", "hips", "grandad",
                  "grandma", "gran", "grandpa", "nan", "nana", "mum", "mums", "dad", "dads",
                  "mother", "father", "toilet", "loo", "stairs", "stairlift", "commode",
                  "bed", "bedroom", "baby", "toddler", "child", "dog", "cat", "hotel",
                  "flight", "train", "bus", "star", "stars", "moon", "sky", "curtain",
                  "blackout", "heater", "boiler",
                  "greenhouse", "greenhouses", "polytunnel", "allotment", "allotments",
                  "garden", "gardening", "plants", "plant", "seedlings", "shed", "conservatory",
                  "greenhouse heater", "water butt", "house plants", "houseplant",
                  "feed", "feeds", "feeding", "breast", "breastfeed", "breastfeeding",
                  "bottle", "bottles", "wean", "weaning", "nappy", "nappies", "formula",
                  "ringing me", "ring me", "rang me",
                  "rings me", "calling me", "calls me", "phoning me", "texting me", "texts me",
                  "someone ringing", "someone calling", "someone phoning", "nuisance calls",
                  "blocked number", "phone", "smartphone",
                  "first night", "keep out", "moving house", "moving in", "move house",
                  "new house", "new home", "unpack", "boxes", "box", "kettle", "toilet roll",
                  "cough", "coughing", "cold", "flu", "sore", "sick", "ill", "illness",
                  "pain", "pains", "ache", "aches", "aching", "hurt", "hurts", "cramp",
                  "cramps", "itch", "itchy", "itching", "pee", "wee", "toilet", "sweat",
                  "sweats", "sweating", "heartburn", "reflux", "breathe", "breathing",
                  "breathless", "asthma", "teeth", "grind", "grinding", "snore", "snoring",
                  "anxiety", "anxious", "panic", "restless", "period", "pregnant", "feed",
                  "feeding", "fever", "temperature", "hot flushes", "nausea", "thirsty",
                  "numb", "numbness", "tingling", "tingle", "pins and needles", "hand",
                  "hands", "fingers", "arm", "arms", "leg", "legs", "foot", "feet", "knee",
                  "shoulder", "back", "stiff", "stiffness", "swollen", "swelling", "bruise",
                  "full beam", "main beam", "high beam",
                  "clean my headlights", "cleaning my headlights", "clean the headlights",
                  "clean headlights", "polish my headlights", "polishing my headlights",
                  "restore my headlights", "headlight restoration", "headlights are foggy",
                  "headlights look foggy", "headlight is foggy", "cloudy headlights",
                  "cloudy headlight", "milky headlights", "milky headlight", "yellow headlights",
                  "yellow headlight", "yellowed", "dull headlights", "lens is", "lenses",
                  "split", "splitting", "share", "sharing", "divide", "halves", "fare",
                  "taxi", "cab", "uber", "petrol", "fuel", "who pays", "who owes",
                  "each pay", "chip in")),
    _entry("catalytic-converter",
           (("catalytic converter", "catalytic", "cat converter", "catalyst"),
            ("what is", "whats", "what does", "what do", "do", "does", "how does", "why",
             "cost", "expensive", "replace", "stolen", "stole", "gone", "rattling", "rattle",
             "clogged", "blocked", "failed", "fail", "mot", "loud", "noisy", "light", "work")),
           _CATALYTIC,
           avoid=("enzyme", "enzymes", "chemistry", "gcse", "reaction", "catalyst in", "pet",
                  "pets", "kitten", "puppy", "dog", "cat food", "litter", "feline")),
    _entry("brakes-click", (("brake", "brakes", "braking", "pedal"), ("click", "clicking", "clunk",
                                                                     "clunking", "knock", "knocking",
                                                                     "pop", "popping")),
          "A click as you press the pedal is usually the brake light switch or a dry pedal bush, a "
          "small fix rather than a safety one. A clunk when you let the pedal off is often a worn "
          "caliper slide or a loose pad; a knock over bumps is more likely a suspension bush. A click "
          "alone is fine for a few days, but have it looked at sooner with grinding or a sinking pedal.",
          bias=1,
          avoid=_NOT_BUYING + ("bike", "bicycle", "cycle", "trampoline", "knee", "hip", "back",
                               "ankle", "joint")),
    _entry("brake-vibration", (("brake", "brakes", "braking"), ("shakes", "shaking", "judder",
                                                               "juddering", "vibrate", "shudder",
                                                               "pulsing", "pulls", "pulling")),
          "A shake or pulse through the pedal or wheel when you brake is usually a warped or worn "
          "disc, and a car that pulls to one side under braking has a sticking caliper or a "
          "collapsed hose. Either way it is a garage job soon, and the discs and pads on that axle "
          "are usually replaced together, about £150 to £300.",
          bias=1, avoid=_NOT_BUYING + ("bike", "bicycle", "cycle")),
    _entry("brakes-cost", (("brake", "brakes", "pads", "discs", "disc"), ("cost", "price", "how much",
                                                                       "replace", "change", "how long",
                                                                       "expensive", "new", "need",
                                                                       "worn", "last", "mileage",
                                                                       "miles", "often", "life")),
          _brakes_cost,
          guard=_not_a_bike_chat,
          avoid=_NOT_BUYING + ("shorts", "padded shorts", "cycling shorts", "leggings",
                               "tights", "trousers", "jersey", "bib", "chamois",
                               "saddle", "knee", "knees", "elbow", "elbows", "shoulder",
                               "shoulders", "chest", "helmet", "gloves", "glove",
                               "knee pads", "elbow pads", "shoulder pads",
                               "bulb", "bulbs", "lamp", "lamps")),
    _entry("brake-life", (("brake pad", "brake pads", "pads", "brake disc", "brake discs", "brakes"),
                          ("how often", "how long do", "how long will", "how long should",
                           "how many miles", "last", "lasts", "lifespan", "how often should")),
          "Front pads usually last 25,000 to 50,000 miles and rears about twice that, so most cars "
          "want a front set every three to five years; town driving with a lot of braking wears them "
          "sooner, and motorway miles stretch them. Discs normally go every other pad change, or "
          "whenever they are scored or below the minimum thickness in the handbook. A wear indicator "
          "light, or a squeal on light braking that stops when you press harder, means book it in "
          "now rather than at the mileage.",
          bias=1,
          avoid=_NOT_BUYING + ("bike", "bicycle", "cycle", "shorts", "padded shorts", "leggings",
                               "tights", "trousers", "jersey", "bib", "chamois",
                               "saddle", "knee", "knees", "elbow", "elbows", "shoulder",
                               "shoulders", "chest", "helmet", "gloves", "glove",
                               "knee pads", "elbow pads", "shoulder pads",
                               "bulb", "bulbs", "lamp", "lamps")),
    _entry("clutch-slip", (("clutch", "pull away", "pulling away", "pulling off"), ("slip", "slipping",
                                        "bite", "high", "revs", "burn", "smell", "replace", "judder",
                                        "juddering", "shudder", "shuddering")),
          "If the revs rise but the speed doesn't, or the bite point is right at the top of the "
          "pedal, the clutch is on its way out; a judder as you pull away is the flywheel or an "
          "engine mount. A replacement is usually £300 to £800 depending on the car, and it is "
          "cheaper to do before it fails completely. Stop riding the clutch in traffic to make it "
          "last.",
          avoid=_NOT_BUYING),
    _entry("clutch-cost", (("clutch",), ("quote", "quoted", "fair", "cost", "price", "expensive",
                                        "how much", "garage", "reasonable")),
          "A clutch replacement is usually £300 to £800 fitted, and towards the top of that on cars "
          "with a dual-mass flywheel, because the flywheel often gets done at the same time. A quote "
          "in that range is normal; it is cheap only if the garage is not touching the flywheel or "
          "the release bearing, so ask what is included.",
          bias=2, avoid=_NOT_BUYING),
    _entry("clutch-pedal", (("clutch pedal", "clutch", "pedal"), ("soft", "spongy", "sinks", "floor",
                                                                 "sticking", "stuck", "squeaky",
                                                                 "creak")),
          "A clutch pedal that feels soft, sinks or needs pumping has air or a leak in the hydraulic "
          "side: check the fluid level in the small reservoir by the brake one and have the slave or "
          "master cylinder looked at. It usually creeps up on you, so book it in before the pedal "
          "goes to the floor at a junction.",
          bias=1, avoid=_NOT_BUYING),
    _entry("cambelt", (("cambelt", "cam belt", "timing belt", "timing chain"), ("change", "changed",
                                                                             "replace", "when", "due",
                                                                             "cost", "need", "interval",
                                                                             "snapped", "broken",
                                                                             "matter", "never")),
          "A cambelt is usually due at 5 years or 60,000 to 100,000 miles, whichever comes first, "
          "and it is not a job to stretch: if it snaps the engine is often wrecked. Expect £300 to "
          "£600 with the water pump, and check the handbook because some cars have a chain that only "
          "gets changed when it gets noisy.",
          avoid=_NOT_BUYING),
    _entry("key-fob", (("car key", "key fob", "keyfob", "fob", "remote"), ("not working", "stopped working",
                                                                         "won't work", "wont work",
                                                                         "isnt working", "isn't working",
                                                                         "is not working", "not work",
                                                                         "doesnt work", "doesn't work",
                                                                         "dead", "battery", "range",
                                                                         "lock", "unlock", "start")),
          "Start with the fob battery: a coin cell (CR2032 on most cars) behind the cover, two "
          "minutes and about £2. If the fob is fine, try the spare, and hold the fob against the "
          "start button on keyless cars, which is the emergency way to start. A fob that has lost "
          "its coding needs a garage or a locksmith.",
          ask=("car", "key", "fob", "keyfob", "remote"),
          avoid=("tv", "telly", "television", "soundbar", "sound bar", "channel", "channels",
                 "freeview", "sky", "cable box", "fire stick", "volume",
                 "remote control", "zapper", "tv remote", "telly remote", "sky remote",
                 "remote for the tv")),
    _entry("battery-light", (("battery light", "battery warning", "alternator", "charging"), ("on", "came on",
                                                                                            "while driving",
                                                                                            "flashing",
                                                                                            "red",
                                                                                            "not charging",
                                                                                            "mean", "means", "what")),
          "That light means the alternator is not charging, not that the battery is flat, so the car "
          "is running on what is left in it: turn off the radio, lights and air con and drive "
          "straight to a garage or home, because it will stop when the battery runs down. An "
          "alternator is usually £250 to £500 fitted.",
          bias=1, ask=("car", "battery light", "battery warning", "alternator", "dashboard", "driving")),
    _entry("oil-leak", (("oil leak", "leaking oil", "leaks oil", "oil patch", "oil under", "oil on"),
                       ("car", "drive",
                                                                                            "driveway",
                                                                                            "engine",
                                                                                            "drip",
                                                                                            "dripping",
                                                                                            "smell")),
          "A few spots under a car can be old spillage or a leaking rocker cover gasket, which is "
          "cheap; a puddle that comes back overnight needs looking at. Check the dipstick each week "
          "and top up, put cardboard under it to see where the drip lands, and get it looked at "
          "before it reaches the clutch or the cambelt.",
          avoid=("cooking", "olive", "fry")),
    _entry("brake-fluid", (("brake fluid", "brake reservoir"), ("check", "level", "low", "top up",
                                                               "how", "change", "colour", "dark")),
          "The brake fluid reservoir is the small pot near the back of the engine bay, marked with a "
          "circle in brackets; the level should sit between min and max. Do not open it to top up "
          "unless it is low, and if it is low there is a leak or worn pads, so get it checked. It "
          "gets changed every two years because it takes in water."),
    _entry("tyre-wear", (("worn", "wearing", "bald", "scrubbed", "uneven"), ("edge", "edges", "inside",
                                                                           "outside", "middle",
                                                                           "one side")),
          "Wear on the inside or outside edge is the tracking or camber, so get a four-wheel "
          "alignment, about £30 to £60, after the new tyres. Wear in the middle is too much pressure "
          "and wear on both edges is too little, so check them monthly cold. A bald patch on one "
          "spot is a locked wheel or a bad shock.",
          ask=("tyre", "tyres", "tire", "tires"), avoid=NOT_BIKE),
    _entry("steering-pull", (("pulling", "pulls", "steering", "tracking", "alignment"),
                            ("left", "right", "one side", "straight", "tyres", "worn", "wheel")),
          "Check the tyre pressures first, because one soft tyre pulls the car. If the pressures are "
          "right, it is the tracking or a worn suspension part: a four-wheel alignment is about £30 "
          "to £60 and stops the tyres scrubbing away."),
    _entry("wheel-vibration", (("vibration", "shakes", "shaking", "wobble", "juddering"),
                              ("speed", "steering", "wheel", "braking", "motorway", "car")),
          "A shake that appears at one speed and fades above it is usually wheel balance, about £10 "
          "to £15 a wheel to fix. A judder only when braking points to warped discs, and a wobble "
          "over bumps is usually a worn bush or a buckled alloy."),

    _entry("handbrake-loose",
           (("handbrake", "hand brake", "parking brake"),
            ("loose", "slack", "slacken", "high", "too far", "comes up", "pulls up", "creeps",
             "not holding", "doesnt hold", "doesn't hold", "rolls", "adjust", "adjusting",
             "tighten", "tightening", "cable", "mot", "fail", "fails")),
          "A handbrake that comes up a long way is a stretched cable, adjusted at the balance bar "
          "under the car or at the lever, and a garage does it in half an hour for £30 to £60. The "
          "cable is only half of it: the rear brake shoes or the caliper mechanism behind it is "
          "usually out of adjustment too, which is why the lever crept up in the first place. "
          "Until it is done, park it in gear and turn the wheels towards the kerb, and treat it as "
          "urgent - a handbrake that does not hold is an MOT fail, and a car that rolls is how "
          "people get hurt.",
          ask=("handbrake", "hand brake", "parking brake", "brake", "brakes", "car")),
    _entry("headlight-out", (("headlight", "headlights", "bulb", "lights",
                              "brake light", "brake lights", "tail light", "tail lights",
                              "rear light", "rear lights", "number plate light",
                              "reverse light", "reverse lights", "indicator", "indicators"),
                             ("not working", "blown", "out", "dim", "foggy",
                              "replace", "change", "yellow",
                              "how much", "cost", "price", "expensive",
                              "dont work", "doesnt work", "do not work", "does not work",
                              "arent working", "isnt working", "wont work", "went out",
                              "broken", "faulty", "blown out")),
          "A failed lamp is a bulb, and the job is the same all round the car. Change bulbs in pairs, because the other one is usually the same age and about to go. Half "
          "an hour with the handbook and a £10 to £20 bulb is normal DIY, though some cars need the "
          "battery or the wheel arch liner out. A lamp that looks milky or yellow rather than dark "
          "is the plastic lens fogging, not the bulb, and the cloudy-headlight card covers that.",
          avoid=_NOT_BUYING + ("pilot", "pilot light", "boiler", "gas", "cooker", "hob", "oven",
                               "fire", "fireplace", "thermocouple", "flame", "caravan",
                               "foggy", "cloudy", "clouded", "milky", "yellowed", "hazy",
                               "dull", "dulled", "restore", "restoring", "polish", "polishing",
                               "toothpaste", "sand", "sanding", "kit", "clean", "cleaning",
                               "wipe", "condensation inside", "misty", "steamy",
                               "ceiling", "lampshade", "pendant", "downlight", "spotlight",
                               "light fitting", "bayonet", "screw fitting", "gu10", "edison",
                               "led bulb", "hall", "landing",
                               "bedroom", "bathroom", "kitchen", "living room", "lamp",
                               "switch", "switches", "fuse", "fuses", "relay", "wiring",
                               "earth", "connection")),
    _entry("headlight-cloudy",
           (("headlight", "headlights", "headlamp", "headlamps", "head light", "head lights",
             "lens", "lenses"),
            ("foggy", "cloudy", "clouded", "milky", "yellow", "yellowed", "dull", "dulled",
             "hazy", "misty", "restore", "restoring", "restoration", "polish", "polishing",
             "buff", "buffing", "sand", "sanding", "toothpaste", "kit", "clean", "cleaning",
             "wipe", "scratch", "scratched", "scuffed", "see at night", "dimmer", "dimmer than",
             "cant see", "can't see", "mot", "condensation", "condensation inside", "water inside",
             "wet inside", "how")),
           "Wipe the outside with soapy water and dry it first, because the cheap fix for a milky "
           "lens is a polish: a £10 to £20 headlight kit with 800, 1500 and 3000 wet-and-dry "
           "paper, then the polish pad, then the sealing wipe, and half an hour a side. Toothpaste "
           "on a rag gets much of it off if the kits are not handy. Water or mist on the inside is "
           "a cracked lens or a perished seal, so dry it out and reseal or it will come back, and a "
           "lamp too dull to show a clean beam can fail the MOT.",
           avoid=_NOT_BUYING + ("blown", "not working", "has gone", "stopped working", "bulb",
                                "fuse", "dip my headlights", "main beam", "full beam", "high beam",
                                "dazzle", "dazzled", "ceiling", "lampshade", "pendant", "kitchen",
                                "bedroom", "bathroom", "living room", "oven", "fridge",
                                "phone", "camera", "glasses", "spectacles"),
           bias=1),
    _entry("windscreen-chip", (("windscreen", "windshield"), ("chip", "crack", "cracked", "stone",
                                                              "repair", "replace", "hole")),
          "A chip smaller than a pound coin can usually be repaired for £20 to £40, and many "
          "insurance policies do it free because it saves them a new screen. Cover it with clear "
          "tape so dirt stays out and get it done before it spreads. A crack in the driver's line of "
          "sight fails the MOT.",
          bias=1),
    _entry("car-side-window", (("car window", "car windows", "window on the car",
                                "windows on the car", "side window", "rear window",
                                "back window"),
                               ("chip", "crack", "cracked", "stone", "hole", "repair", "replace",
                                "replaced", "pane", "glass")),
          "A side or rear window is toughened glass, so a chip or a crack in it is a new pane "
          "rather than a repair: a glass company or a mobile fitter supplies and fits it, £60 to "
          "£150 for most cars and more for a window with a heated rear element. Give them the "
          "registration or the VIN, because the glass is cut to the car. Check the door seals, the "
          "central locking and the window motor work before they leave, and cover the gap with "
          "plastic and tape rather than driving with broken glass in the door.",
          bias=1),
    _entry("wipers", (("wipers", "wiper", "windscreen wiper"), ("smear", "smearing", "squeak",
                                                                "squeaky", "judder", "juddering",
                                                                "chatter", "chattering", "skip",
                                                                "skipping", "grabbing", "streak",
                                                                "replace", "change", "blades",
                                                                "rubber", "noisy", "need")),
          "Smearing and squeaking blades are a sign the rubber has gone hard: replace both front "
          "blades once a year, about £15 to £25 for the pair, and clean the glass properly at the "
          "same time. Wipers are easy to clip on yourself and the handbook shows the size."),
    _entry("demist", (("demist", "demisting", "fogged", "foggy", "misted", "condensation"),
                     ("windscreen", "windows", "car", "screen", "up")),
          MIST_REPLY,
          ask=("car", "windscreen", "screen", "van", "driving", "drive", "set off", "motorway")),
    _entry("car-misted", (("steaming", "steamed up", "steam up", "steams up", "fogging",
                          "fogging up", "misting", "misting up", "misty", "blurred", "hazy",
                          "clear the windscreen", "clear my windscreen", "clear windscreen",
                          "clear the windshield", "clear my windshield",
                          "clear the car windows", "clear my car windows",
                          "clear the screen", "clearing the windscreen"),
                         ("windscreen", "windshield", "windows", "window", "screen", "glass",
                          "mirror", "inside")),
          MIST_REPLY,
          ask=("car", "windscreen", "screen", "van", "driving", "drive", "set off", "motorway"),
          avoid=("phone", "laptop", "computer", "monitor", "tv", "telly", "ipad", "tablet",
                 "inbox", "email", "history", "cache", "table", "counter")),
    _entry("aircon-warm", (("air con", "aircon", "air conditioning", "air-conditioning"),
                          ("not cold", "only cool", "cool not cold", "not very cold", "warm",
                           "smell", "regas", "service", "cold", "hot", "not working",
                           "stopped working", "blowing warm")),
          "Air con loses a little gas every year, so if it is only cool, get it regassed: about £50 "
          "to £80 and best done by a garage. Run it for ten minutes a week all year to keep the "
          "seals from drying out. A musty smell means new cabin filter and an antibacterial clean."),
    _entry("car-wax", (("wax", "waxing", "waxed", "polished", "polish", "clay", "claying"),
                       ("car", "cars", "van", "bodywork", "paintwork", "paint")),
          "Wash and dry it first, then wax one panel at a time in the shade: a thin coat on a "
          "foam pad, let it haze, and buff it off before it goes chalky, turning the cloth as it "
          "loads up. A paste wax lasts about six months and a liquid one about three, and two "
          "coats a year is plenty for a car kept outside. Do not wax in sun or on a hot panel, and "
          "keep it off black plastic trim, where it dries white.",
          ask=("car", "cars", "van", "bodywork", "paintwork"),
          avoid=_NOT_BUYING + ("car wash", "hand car wash", "cost", "price", "how much",
                               "dishes", "dish", "plate", "plates", "mug", "cup", "clothes",
                               "laundry", "washing machine", "hair", "face", "hands", "dog",
                               "floor", "window", "windows", "shoes", "scratch", "scratches")),
    _entry("scratches", (("scratch", "scratches", "scuffed", "scuff"), ("car", "paint", "remove",
                                                                        "repair", "fix", "polish",
                                                                        "keyed")),
          "If a fingernail doesn't catch on it, the scratch is in the lacquer: clean it, polish with "
          "a cutting compound, then wax, and it will mostly vanish. If your nail catches, a paint "
          "pen for £10 to £20 stops the rust and makes it much less obvious, and only a bodyshop "
          "will make it perfect.",
          avoid=_NOT_BUYING + ("wall", "walls", "skirting", "wallpaper", "plaster", "brick",
                               "floor", "floors", "floorboard", "floorboards", "laminate",
                               "glasses", "spectacles", "lenses", "lens", "goggles", "oven",
                               "hob", "mirror", "phone", "screen", "watch", "table", "tables",
                               "furniture", "windscreen", "windshield",
                               "wood", "wooden", "wood floor", "wooden floor", "floor", "floors",
                               "flooring", "skirting board", "desk", "dresser", "cupboard",
                               "sideboard", "worktop", "veneer", "decking")),

    _entry("burning-smell", (("burning", "burnt", "smell", "smells"), ("car", "clutch", "brakes",
                                                                      "engine", "drive", "driving",
                                                                      "oil", "plastic")),
          "Work out when it happens: a hot, acrid smell after hard braking is the brakes, a slipping "
          "clutch smells like burning paper, and a sweet smell with steam is coolant on something "
          "hot. A burning rubber smell is usually a belt, and an electrical, fishy smell means stop "
          "and get out. If you can't place it, stop somewhere safe and look under the bonnet.",
          avoid=("toast", "cake", "cooking", "oven", "dinner", "pan", "saucepan", "rice", "food",
                 "petrol", "diesel", "fuel", "filling", "fill up", "filled up",
                 "carpet", "carpets", "rug", "rugs", "mattress", "sofa", "settee", "curtain",
                 "curtains", "wardrobe", "bedroom", "kitchen", "bathroom", "pet", "pets", "dog",
                 "dogs", "cat", "cats", "urine", "pee")),
    _entry("car-damp", (("damp", "dampness", "musty", "mouldy", "mould", "mildew", "moisture",
                         "smell of damp", "damp smell", "musty smell", "mouldy smell",
                         "mildew smell", "smells damp", "damp smells", "smells musty",
                         "condensation", "wet inside", "wet patch", "water in the",
                         "water in", "water", "wet"),
                        ("car", "cars", "van", "boot of", "in the boot", "boot floor",
                         "boot space", "boot lid", "boot seal", "boot well", "trunk",
                         "footwell", "foot well", "interior",
                         "inside the car", "cabin", "seats", "headlining",
                         "air con", "aircon", "air conditioning", "blower", "leather",
                         "spare wheel", "back of the car")),
          "A musty car is water: lift the mats and press a hand into both footwells and the boot "
          "floor, and check the spare-wheel well, because that is where a leak collects first. "
          "Clear the drains under the windscreen, check the door and sunroof seals and the boot "
          "seal for splits, and dry the car out with the heater on and a window open on a long "
          "drive, not with a bowl of vinegar. If the smell comes on when the blower runs, it is "
          "the air con: change the cabin filter, have the evaporator cared for by a garage, and "
          "run it for a few minutes every week so the drain does not stay damp.",
          bias=2, guard=_a_room_not_a_car,
          avoid=("petrol", "diesel", "fuel", "filled up", "filling", "fumes", "oil", "burning",
                 "burnt", "smoke", "smoking", "brakes", "braking", "clutch", "exhaust", "gas",
                 "rotten eggs", "sulphur", "sulfur", "not cold", "warm air", "heater not",
                 "exhaust", "fire", "leaking water", "coolant", "puddle under", "overheating",
                 "house", "home", "room", "bedroom", "cellar", "wall", "walls", "basement",
                 "mattress", "wardrobe", "curtain", "curtains", "sofa",
                 "jam jar", "jam jars", "jar of jam", "marmalade jar", "pickle jar",
                 "kilner jar", "jar of pickle", "jar of chutney", "jam",
                 "dog", "dogs", "cat", "cats", "pet", "pets", "puppy", "kitten", "wet dog",
                 "sweat", "sick", "vomit", "urine", "pee", "wee", "milk", "baby",
                 "bag", "bags", "handbag", "purse", "wallet", "coat", "coats", "jacket",
                 "jackets", "shoe", "shoes", "trainers", "cupboard", "cupboards", "drawer",
                 "drawers", "closet", "bedding", "pillow", "pillows", "duvet",
                 "battery", "washer", "screen wash", "radiator", "coolant", "topping up",
                 "drinking water", "bottle")),
    _entry("car-smoke-smell",
           (("smoke", "smoking", "cigarette", "cigarettes", "smoky", "smoke smell",
             "smell of smoke", "smells of smoke", "stinks of smoke", "smoked in"),
            ("car", "cars", "van", "vehicle", "seats", "seat", "upholstery", "headlining",
             "cabin", "interior", "inside the car")),
           "Open every window, drive with the fan on fresh air (not recirculate) for twenty "
           "minutes to clear what is in the air, wipe the glass, dashboard and door cards with warm "
           "water and a splash of white vinegar, then shampoo or steam the seats, carpets and "
           "headlining and fit a new cabin (pollen) filter, which is behind the glovebox on most "
           "cars. That order is the job, because the film on the glass and the soft stuff hold the "
           "smoke; bowls of bicarbonate of soda or fresh coffee grounds overnight help a bit, and a "
           "car smoked in for years needs an ozone treatment from a valeter.",
           avoid=("exhaust", "white smoke", "blue smoke", "black smoke", "engine", "bonnet",
                  "fire", "alarm", "burning", "burnt", "toast", "barbecue", "bbq", "wood",
                  "smoke alarm", "vape", "smoking ban", "in the car while driving")),
    _entry("petrol-smell", (("petrol", "diesel", "fuel", "petrolly", "gasoline",
                             "gas at the pump", "gas from the pump", "gas at the station",
                             "gas on my hands", "gas pump"),
                            ("smell", "smells", "smelling",
                                                                     "smelly", "filling", "fill up",
                                                                     "filled up", "pump", "inside",
                                                                     "strong", "fumes", "whiff")),
          "A light whiff while filling up is normal; a strong petrol smell after is not. Do not "
          "smoke or start the engine, and check the filler cap is on properly and not cross-threaded. "
          "If the smell is inside the car or stays after a few miles, stop and get it looked at, "
          "because a leak near a hot engine is a fire risk.",
          avoid=("buy", "buying", "should i get", "worth buying", "cost of", "wrong fuel", "misfuel",
                 "misfuelled", "wrong diesel", "petrol in a diesel", "diesel in a petrol",
                 "wrong", "mistake", "by accident",
                 "filled my", "filled with", "car with diesel", "car with petrol",
                 "put diesel", "put petrol")),
    _entry("wrong-fuel", (("wrong fuel", "misfuel", "misfuelled", "misfuelling",
                          "petrol in a diesel", "diesel in a petrol",
                          "petrol", "diesel"),
                         ("filled", "fill", "fill up", "put", "put in", "drove", "tank",
                          "in my", "in a petrol car", "in a diesel car", "in my petrol car",
                          "in my diesel car")),
          "Do not start the engine: even a few minutes spreads the wrong fuel through the pump and "
          "injectors and turns a drain into a repair. Leave the ignition off, put it in neutral and "
          "push it clear of the pump, then ring the station or your breakdown cover for a drain and "
          "flush. That is around 150 to 250 pounds against a few thousand for new injectors.",
          avoid=_NOT_BUYING + ("cheaper", "cheaper to run", "better", "worse", "which is",
                               "or a diesel", "or a petrol", "running costs", "fuel economy",
                               "mpg", "compare", "comparison",
                               "put in", "chip in", "split", "share", "each pay", "contribute",
                               "how much should", "who owes", "between us")),
    _entry("stalling", (("stalling", "stalls", "stalled", "cut out", "cuts out", "dies"),
                       ("car", "engine", "stop", "stopping", "idle", "junction", "traffic")),
          _stalling,
          avoid=_NOT_BUYING + ("learning", "learner", "instructor", "lessons", "test",
                               "nervous")),
    _entry("fuel-economy", (("mpg", "fuel", "petrol", "diesel"), ("save", "improve", "better",
                                                                  "economy", "efficient", "low",
                                                                  "drink", "sip", "expensive")),
          "The four that give the most back: tyres at the right pressure, nothing heavy in the boot, "
          "gentle acceleration and a steady 50 to 60mph instead of 70-plus on the motorway. Air con "
          "costs you fuel at low speed, so use the window around town and the air con on the "
          "motorway.",
          avoid=("which is better", "diesel or petrol", "petrol or diesel", "or a diesel",
                 "or a petrol", "which fuel", "should i buy", "should i get")),
    _entry("diesel-or-petrol",
           (("diesel", "petrol", "fuel"),
            ("or a diesel", "or a petrol", "diesel or petrol", "petrol or diesel", "which fuel",
             "which is better", "which one", "should i buy", "should i get", "worth it",
             "cheaper to run", "better", "worse", "compare", "high mileage", "miles a year",
             "town driving", "motorway driving", "for town", "short trips", "long runs",
             "lots of motorway", "mostly motorway")),
           "Diesel only pays if you do long, steady runs: as a rule of thumb over 12,000 miles a "
           "year with most of it motorway, and fewer than that if the car is also doing short "
           "hops. Below that the diesel costs more to buy, more to service and its filter clogs "
           "on short trips, so a petrol car is the cheaper buy. Mostly town driving, cold starts "
           "and trips under twenty minutes are petrol, or a hybrid if the budget reaches one.",
           avoid=("filled", "fill", "put petrol", "put diesel", "wrong fuel", "misfuelled",
                  "mpg", "save", "improve", "economy", "smell", "smells", "smelly",
                  "wont start", "won't start", "not starting", "stall", "noise", "warning light",
                  "tax", "insurance", "sell", "selling", "price of",
                  "electric", "electric car", "ev", "hybrid", "plug in", "plug-in",
                  "battery", "charge", "charging", "charge point")),
    _entry("fuel-type", (("what fuel", "which fuel", "what petrol", "which petrol",
                          "unleaded", "fuel does my car take", "fuel should i put",
                          "petrol or diesel", "diesel or petrol", "fuel does it take"),
                         ("my car", "my car take", "car take", "car use", "put in", "use",
                          "takes", "take", "petrol", "diesel", "unleaded", "mine")),
          "It is written on the car: the inside of the fuel flap, the inside of the fuel cap and "
          "the handbook all say 'unleaded 95' or 'diesel' in so many words, and the filler neck is "
          "the backstop, because a diesel nozzle will not fit into a petrol car. Most petrol cars "
          "want standard unleaded (E10, 95 RON) and the handbook only asks for 98 if the engine "
          "needs it - putting 95 in a car that wants 98 costs a little power and economy, which is "
          "not the same as damage. Petrol in a diesel is the expensive one: stop before you start "
          "it and it is a drain and flush, start it and it is a fuel pump.",
          ask=("fuel", "petrol", "diesel", "unleaded") + MODELS,
          avoid=_NOT_BUYING + ("should i buy", "should i get", "which is better", "better",
                              "worth it", "cheaper", "buy a car", "buying a car", "new car",
                              "second hand", "secondhand", "mpg", "save", "economy",
                              "filled", "fill", "wrong fuel", "misfuelled", "put petrol",
                              "put diesel", "smell", "smells", "tax", "insurance")),
    _entry("breakdown", (("breakdown", "broken down", "broke down", "break down", "breaks down",
                          "breaking down", "conked out", "died",
                          "cut out", "stalled"),
                         ("motorway", "call", "recovery", "hard shoulder", "stranded", "road",
                          "car", "van")),
          "On a motorway get onto the hard shoulder, put your hazards on, and get everyone out to "
          "the left and up behind the barrier before you call anyone. On a smart motorway where the "
          "shoulder is a live lane, stay in the car with belts on and ring 999. Then call your "
          "breakdown service or insurer. A broken-down car is not worth changing a tyre beside "
          "moving traffic for.",
          avoid=_NOT_BUYING + ("learning", "learner", "instructor", "lessons", "test",
                               "phone", "iphone", "mobile", "handset", "on calls", "on a call",
                               "call quality", "dropping calls", "wifi", "wi fi", "signal",
                               "broadband", "router",
                               "call keeps", "calls keep", "the call", "my call", "phone call",
                               "during calls", "cant hear", "can't hear", "breaking up")),
    _entry("cancel-car-insurance",
           (("car insurance", "motor insurance", "my insurance", "insurance policy",
             "insurance renewal", "car insurance renewal", "my policy", "comprehensive"),
            ("cancel", "cancelling", "cancelled", "get a refund", "refund", "money back",
             "switch", "switching", "cheaper elsewhere", "gone up", "too much", "dont need",
             "don't need", "sold the car", "not using", "swap", "change insurer",
             "cancel my policy", "cancel the policy", "leaving")),
           "Start the new cover before you cancel the old one - being uninsured for even a day is "
           "an offence and a gap pushes the next premium up - and cancel from the day the new "
           "policy starts. Ring the insurer, or use their app, and ask for the cancellation date "
           "and the refund figure in writing: expect a pro-rata refund of the unused months less "
           "an admin fee of about £25 to £50, and nothing back if you have claimed. In the first "
           "14 days of a new policy you can cancel for a full refund minus a small fee. Ask for "
           "proof of your no-claims years in writing for the new insurer, and remember a policy "
           "paid monthly is a credit agreement, so the instalments can carry on after the cover "
           "stops - settle it and get the letter.",
           avoid=("phone", "mobile", "gadget", "travel", "holiday", "home insurance", "buildings",
                  "contents", "life insurance", "pet insurance", "boiler", "washing machine",
                  "gym", "landlord", "claim", "claiming", "accident", "wrote off", "written off",
                  "renew", "renewal", "renewing", "when i move", "moving house", "new address",
                  "change of address", "move house")),

    _entry("road-tax", (("road tax", "car tax", "tax", "ved"), ("car", "due", "how much", "pay",
                                                                "renew", "check", "cost", "monthly",
                                                                "disabled")),
          "Road tax is now on the car, not the windscreen, so you can check it at gov.uk's 'check if "
          "a vehicle is taxed' page from the number plate. The amount depends on the first "
          "registration date, the CO2 figure and the list price, and it can be paid monthly by "
          "direct debit. Driving untaxed should mean the car is on a SORN and off the road.",
          avoid=_NOT_BUYING, ask=("car", "road", "vehicle", "van", "motorbike")),

    _entry("speed-limits", (("speed limit", "speed limits", "how fast"), ("motorway", "dual",
                                                                          "carriageway", "built up",
                                                                          "built-up", "town",
                                                                          "national", "mph",
                                                                          "drive", "driving",
                                                                          "country road")),
          "The national limits for cars are 30mph where there are street lights (unless signed "
          "otherwise), 60mph on a single carriageway and 70mph on a dual carriageway or motorway. "
          "They are a ceiling, not a target: on a narrow country lane 40mph is often too fast for "
          "the bends, and a lower sign overrides the national limit."),
    _entry("mot-history", (("mot history", "mot record", "check the mot", "mot check"),
                          ("car", "check", "online", "gov.uk", "free", "history", "buying", "before")),
          "Put the number plate into gov.uk's free 'check the MOT history of a vehicle' page: it "
          "lists every test since 2005 with the mileage at each one and the reasons for any failure "
          "or advisory. A jump in mileage, a long gap, or the same advisory year after year tells you "
          "more about a car than the seller will.",
          bias=1, avoid=("mot due", "when is my mot")),
    _entry("drink-driving", (("drink", "drinking", "pint", "alcohol", "beer", "wine",
                              "units", "unit"),
                            ("drive", "driving", "legal", "limit", "safe")),
          "There is no safe number of drinks before driving. The England and Wales limit is 35 "
          "micrograms of alcohol per 100ml of breath, and two people can be over on the same "
          "amount because it depends on your size, whether you have eaten, and how fast you get "
          "through them. The only reliable rule is none if you are driving, and none the morning "
          "after a heavy night.",
          bias=2,
          ask=("drive", "driving", "driven", "driver", "drink driving", "drink-drive",
               "before driving", "on the road", "breathalyser", "legal limit", "alcohol limit",
               "legal alcohol limit", "legal drink drive limit",
               "limit for driving", "licence", "license",
               "over the limit", "under the limit", "over the drink drive limit",
               "how many pints before", "how many drinks before", "how many units before",
               "units before", "how many units can i drink and drive"),
          avoid=("breathalyser", "test i have to", "course", "ban", "water", "tap water",
                 "bottled water", "the water in",
                 "pregnant", "pregnancy", "expecting a baby", "breastfeeding", "nursing",
                 "trying to conceive",
                 "paracetamol", "ibuprofen", "painkiller", "painkillers", "antibiotic",
                 "antibiotics", "penicillin", "amoxicillin", "metronidazole", "tablets",
                 "medicine", "medication", "pills", "prescription", "antihistamine",
                 "antidepressant", "statins", "codeine",
                 "a week", "per week", "weekly", "week", "14",
                 "bring home", "bring back", "bring in", "bringing back", "customs", "duty free",
                 "duty-free", "from abroad", "from spain", "from france", "from portugal",
                 "in my suitcase", "in the car from")),
    _entry("child-seats", (("child seat", "car seat", "booster", "booster seat", "car seats",
                           "face forward", "forward facing", "forward-facing", "rear facing",
                           "rear-facing", "front seat"),
                          ("law", "rules", "need", "must", "height", "age", "child", "children",
                           "baby", "toddler", "when",
                           "ok", "safe")),
          "By law a child under 12 and under 135cm tall needs the right car seat or booster, and it "
          "has to be the one made for their weight or height, fitted properly. A rear-facing seat "
          "goes in the back if there is an active airbag in front. Above 135cm or 12 years old they "
          "use the adult belt.",
          bias=1, avoid=("cheap", "best", "recommend", "buy", "which",
                        "dog", "dogs", "puppy", "puppies", "cat", "cats", "kitten", "kittens",
                        "pet", "pets", "vet", "jab", "jabs", "vaccination", "vaccinations",
                        "vaccine", "boosters for dogs", "horse", "rabbit",
                         "coat", "coats", "pramsuit", "pram", "blanket", "fleece",
                         "snowsuit", "all in one", "wearing", "wrap",
                         "jabbed", "vaccines", "immunisation", "immunization", "covid", "flu",
                         "tetanus", "booster jab", "booster shot"),
          guard=_a_seat_is_what_it_is_about),
    _entry("road-charge", (("congestion charge", "ulez", "ultra low emission zone",
                           "low emission zone", "clean air zone", "emission zone",
                           "dart charge", "dartford crossing", "toll", "tolls", "toll road",
                           "toll bridge", "m6 toll", "road charge", "road charges",
                           "emissions charge", "emission charge", "congestion zone",
                           "charge for driving into", "charge to drive into",
                           "charge for driving in", "cost of driving into",
                           "cost to drive into", "cost for driving into",
                           "how much to drive into", "how much does it cost to drive into",
                           "driving into london charge", "charge for driving in london"),
                          ("how much", "cost", "costs", "pay", "paying", "paid", "price",
                           "have to", "have i got to", "need to", "must i", "do i", "should i",
                           "worth", "fine", "penalty", "avoid", "cheaper", "free", "daily",
                           "every day", "each day", "weekend", "weekends", "sunday", "saturday",
                           "bank holiday", "christmas", "night", "what happens", "missed",
                           "what is", "whats", "what's", "how much is", "how much does",
                           "forgot", "forget", "ignore", "not paid", "dont pay", "don't pay",
                           "twice", "again",
                           "motorbike", "motorbikes", "motorcycle", "motorcycles", "moped",
                           "mopeds", "scooter", "scooters", "24 hours", "24 hour", "all day",
                           "all night", "overnight",
                           "exempt", "exemption", "exemptions", "exempt from",
                           "explain", "explained", "meaning", "means",
                           "is there", "are there", "is it", "who pays", "who has to",
                           "who needs to")),
          _road_charge,
          bias=1,
          bikes=True,
          avoid=("nose", "blocked", "bunged", "stuffy", "sinus", "cold", "cold symptoms",
                 "flu", "chest", "cough", "headache", "sink", "drain", "drains", "toilet",
                 "sewer", "pipe", "pipes",
                 "phone", "laptop", "battery", "charger", "charging my phone",
                 "phone is charging", "phone charging", "tablet", "headphones", "steam", "wet",
                 "train", "trains", "rail", "bus", "buses", "fare", "fares",
                 "compliant", "compliance", "check my car",
                 "pay for my car", "for my cars", "my cars cost", "running my cars",
                 "tax my cars", "insure my cars")),
    _entry("parking-ticket-appeal", (("parking ticket", "penalty charge", "penalty charge notice",
                                     "pcn", "clamp", "clamped"),
                                    ("appeal", "appealing", "appeal it", "challenge", "pay",
                                     "unfair", "wrong", "got", "received", "contest", "cancel",
                                     "worth", "what is", "what does", "mean", "means", "notice",
                                     "letter", "fine", "explain",
                                     "get out of", "get out of it", "get rid of", "fight it",
                                     "fight", "dispute it", "refuse to pay", "dont pay",
                                     "don't pay", "not pay")),
          _parking_ticket,
          bias=2, avoid=_NOT_BUYING),
    _entry("no-mot-fine", (("mot", "no mot", "without an mot", "mot expired", "mot ran out",
                           "mot out of date", "mot has run out", "mot lapsed", "mot renewal",
                           "mot is up"),
                          ("fine", "penalty", "illegal", "drive", "driving", "penalty points",
                           "drove", "still drove", "drove anyway", "drove it", "been driving",
                           "driving without", "driving it", "last week", "last month",
                           "yesterday", "anyway", "ran out", "expires", "expired", "lapsed",
                           "pulled over", "stopped by the police", "police stopped",
                           "renew", "renewed", "renewal", "forgot", "forgot to renew", "missed",
                           "i missed", "overdue", "not renewed", "need to renew", "should have")),
          _no_mot,
          bias=2,
          avoid=("failed", "fails", "fail", "sheet", "refusal", "refused", "advisory",
                 "advisories", "appeal", "appealed", "appealing", "retest", "re-test", "retested",
                 "dangerous", "not roadworthy", "unsafe", "school bus", "bus",
                 "every year", "each year", "how often", "how frequent", "annually", "once a year")),
    _entry("licence-renew-70", (("licence", "license"), ("70", "seventy", "pensioner",
                                                        "turns 70", "turning 70", "birthday")),
          "From 70 the licence is renewed every three years, and it is free. You declare your "
          "medical conditions and eyesight each time, and if you only drive a car you do not need a "
          "medical unless the DVLA asks. There is no upper age limit and no retest, but you must be "
          "able to read a number plate 20 metres away.",
          ask=("70", "seventy", "pensioner", "turns", "turning", "birthday", "over 70"), bias=2),
    _entry("hit-an-animal", (ANIMAL_ON_THE_ROAD + ("hit an animal", "ran over", "dead animal"),
                            ("car", "road", "police", "report", "insurance", "damage", "what do i do",
                             "what should i", "should i have", "on the way home")),
          "Stop if it is safe and put your hazards on, and keep yourself off the road rather than "
          "standing in it. You must tell the police if you hit a dog, horse, cattle, pig, goat, sheep or "
          "donkey, and if you cannot find the owner it must be reported; any other wild animal - "
          "a deer, a fox, a badger - does not have to be reported. An animal that is alive and hurt "
          "is the RSPCA on their animal rescue line, and a dead one in the road is the council's "
          "to clear, reported with the location on their website. If you hit it, tell your insurer "
          "too, because a deer strike is usually a comprehensive claim.",
          bias=1, shape=(_an_animal_struck,),
          avoid=("dog bit", "my dog", "cat", "rabbit", "bird", "nearly", "almost", "just missed",
                 "near miss", "missed a")),
    _entry("aspects", (("sorn", "off the road", "declare off road", "not using the car"),
                      ("how", "need", "tax", "garage", "road", "when", "do i", "my car",
                       "what is", "what does", "whats", "mean", "means", "meaning", "explain",
                       "definition")),
          "A SORN is free at gov.uk and it means the car is taxed as off the road: no vehicle tax, "
          "no MOT needed while it stays off public roads. The car has to be on a drive or in a "
          "garage, not on the street, and a SORN ends as soon as you tax it again to drive it. If "
          "you are not the registered keeper the DVLA will not take the declaration.",
          bias=1,
          avoid=("licence", "license", "entitlement", "luton", "hire", "hiring", "renting",
                 "raise money", "raise funds", "raise the money", "funding", "investor",
                 "investors", "startup", "business plan", "crowdfund", "seed round",
                 "loan", "loans", "finance", "financing", "borrow", "borrowing", "afford",
                 "monthly payments", "deposit")),
    _entry("dvla-moved", (("dvla", "the dvla", "tell the dvla", "with the dvla", "notify the dvla",
                          "v5c", "log book",
                          "registered keeper", "vehicle registration", "driving licence",
                          "driving license", "licence", "license"),
                         ("moved", "moving", "new address", "change of address", "update", "address")),
          "You have to tell the DVLA when you move, and it is free. Update the V5C log book online "
          "(the address on it is what the police and the fines go to), and update your driving "
          "licence too - the two are separate records. You will not get a new V5C in the post for a "
          "licence change, so keep a note of the date you did it.",
          bias=2),
    _entry("tax-new-car", (("tax", "taxed", "taxing", "vehicle tax"), ("just bought", "bought",
                                                                      "new keeper", "new car",
                                                                      "second hand", "seller",
                                                                      "collect", "drive it home")),
          "Tax it before you drive it away: with the new keeper slip from the seller's V5C you can "
          "tax it at gov.uk in a couple of minutes, and the tax does not transfer from the old "
          "keeper. Insurance has to be in place first, and you need the MOT if the car is over three "
          "years old. The old keeper gets a refund for the rest of their tax automatically.",
          bias=1),
    _entry("driving-others-car", (("drive", "driving", "borrow"), ("someone else's", "someone elses",
                                                                 "another car", "a mates car",
                                                                 "my mates car", "my mum's car",
                                                                 "mums car", "friends car",
                                                                 "friend's car", "courtesy car",
                                                                 "hire car", "insured")),
          "Only if your own policy says so. Many comprehensive policies give 'driving other cars' "
          "cover, but it is usually third party only, often limited to drivers over 25, and some "
          "policies have dropped it altogether, so check the certificate before you drive. The car "
          "also needs its own insurance for someone to drive it, and the owner's permission is not "
          "cover by itself.",
          bias=1),
    _entry("space-saver", (("space saver", "spacesaver", "spare wheel", "spare tyre",
                            "spare wheels", "on the spare", "on a spare", "the spare wheel",
                            "temporary tyre", "get you home"),
                          ("how long", "how fast", "how far", "drive", "mph", "motorway", "far",
                           "miles", "speed", "70", "50")),
          "About 50 miles, or an hour at 50mph, which is enough for the trip to a tyre place and "
          "not a motorway run of a hundred miles: keep to 50mph, drive gently and go straight "
          "there. Check its pressure every few months, because they are often flat when you need "
          "them, and it does not count as a spare for a car with different size wheels at the "
          "front.",
          ask=("how long", "how fast", "how far", "mph", "motorway", "miles", "speed", "70", "50",
               "can i drive", "safe to drive", "is it safe", "safe", "ok to drive",
               "get me home", "to the garage"),
          bias=3),
    _entry("car-damaged-unattended",
           (("wing mirror", "wing mirrors", "wingmirror", "side mirror",
             "knocked off my car", "knocked my mirror", "mirror knocked off", "mirror got knocked off",
             "keyed", "keyed my car", "been keyed", "car got keyed",
             "smashed my window", "smashed the window", "smashed a window", "window smashed",
             "my car window", "the car window", "car window",
             "broken into", "broke into", "break in", "break-in",
             "vandalised my car", "vandalized my car", "car vandalised", "car vandalized",
             "damaged my car", "damage to my car", "car got damaged",
             "scratched my car", "scraped my car", "someone scraped", "someone scratched",
             "reversed into my parked car", "reversed into my car", "reversed into me",
             "hit and run", "someone hit my car", "car was stolen", "car got stolen",
             "car stolen", "my cars been stolen", "car was taken", "car got nicked",
             "nicked my car", "nicked from my car", "stolen from my car", "my car radio",
             "my catalytic converter", "wheels were stolen", "my number plate was stolen"),
            ("someone", "somebody", "parked", "car park", "last night", "this morning",
             "yesterday", "at the weekend", "while i was", "when i came back", "came back",
             "drove off", "the car", "my car", "cars", "keyed", "stolen", "broken into", "badly",
             "knocked off", "broken off", "smashed off", "hanging off", "off the car", "took it",
             "taken", "gone", "missing",
             "what do", "what now", "should i", "police", "report")),
          "Nobody was hurt, so this is a report and a claim rather than an emergency: ring 101 "
          "for a crime or incident number, photograph the damage before you clean or repair "
          "anything, and tell your insurer the same day even if you mean to pay for it yourself. "
          "Check the excess before you decide, because a wing mirror or a window often costs less "
          "than the claim would; if the car itself has gone, ring 999 while it is happening and "
          "give the insurer the crime number.",
          avoid=("bathroom", "bedroom", "kitchen", "hallway", "hall", "landing", "lounge",
                 "living room", "wall", "walls", "front door", "back door", "garage door",
                 "house window", "house", "flat", "shed", "conservatory", "keyboard",
                 "keyed in", "typed", "password", "login", "account", "phone", "laptop",
                 "lock", "locks", "lock barrel", "keyhole", "key sticks", "key sticking",
                 "key in the lock", "key will not turn", "key wont turn", "sticking", "sticks",
                 "insurance", "insurer", "insurers", "claim", "claims", "claiming", "policy",
                 "excess", "loss adjuster", "no claims", "payout", "pay out", "cover it",
                 "will they pay", "will insurance",
                 "key fob", "keyfob", "fob", "fob battery", "key battery", "key not working",
                 "scrap", "scrapping", "scrapped", "scrapyard", "sell", "selling", "sold",
                 "trade in", "part exchange", "worth fixing", "worth repairing", "repair or",
                 "fix or", "or sell", "keep it", "of work", "needs work", "spend money on",
                 "keys are", "keys is", "keys were", "keys was", "where his keys",
                 "where her keys", "where my keys", "where the keys", "forgot where",
                 "forgetting where", "keeps forgetting", "keeps losing",
                 "the key", "the keys", "my key", "my keys", "a key", "spare key", "spare keys",
                 "lost my", "lost the key", "without the key", "without a key",
                 "without my keys"),
          guard=a_window_on_a_car_is_not_a_damage, report=True, bias=1),
    _entry("crash", (("crash", "crashed", "accident", "collision", "prang", "bumped into",
                     "hit a car", "rear ended", "rear-ended", "went into the back of me",
                     "someone hit me", "hit me at", "shunt", "shunted", "hit my car",
                     "my car was hit", "dented my car", "dent in my car",
                     "bumped into a car", "bumped a car", "scraped a car", "someone scraped",
                     "clipped a parked car", "hit a parked car", "reversed into a parked car",
                     "bumped a parked car", "scraped a parked car", "scraped a parked",
                     "hit a bollard", "clipped a bollard", "reversed into a bollard",
                     "crashed into a wall", "hit a gatepost", "hit the gatepost",
                     "drove into the back", "drove into my car", "drove into me",
                     "drove into the back of my car", "went into the back of my car",
                     "hit me from behind", "hit from behind", "rear ended me",
                     "went into the back of me", "someone went into me",
                     "went into the back of us", "into the back of us", "into the back of me",
                     "rear ended us", "rear-ended us", "shunted us", "shunted me", "shunted",
                     "hit us from behind", "drove into us", "ran into the back of",
                     "came off the road", "the car behind", "car behind me",
                     "hit a cyclist", "hit cyclists", "hit a pedestrian", "hit a person",
                     "hit someone", "hit somebody", "hit a man", "hit a woman", "hit a kid",
                     "hit a child", "hit a boy", "hit a girl", "hit a dog", "hit a cat",
                     "hit someone on a bike", "hit a man on a bike", "hit a woman on a bike",
                     "hit a person on a bike", "hit a cyclist on",
                     "knocked a cyclist", "knocked a pedestrian", "knocked a person",
                     "knocked someone off", "knocked somebody off", "knocked a man off",
                     "knocked a woman off", "knocked the cyclist off", "knocked him off",
                     "knocked her off", "knocked them off", "knocked a kid off",
                     "knocked a child off", "knocked a dog",
                     "clipped a cyclist", "clipped a pedestrian", "clipped someone",
                     "clipped a person", "clipped a man", "clipped a kid", "clipped a woman",
                     "ran into a cyclist", "ran into a pedestrian", "ran into someone",
                     "ran into a person", "collided with a cyclist", "collided with a pedestrian",
                     "collided with someone", "caught a cyclist", "caught a pedestrian",
                     "caught someone on", "went into a cyclist", "went into a pedestrian",
                     "hit them with my car", "hit him with my car", "hit her with my car"),
                    ("what do", "what now", "should i", "insurance", "police", "details", "claim",
                     "other driver", "car park", "scratched", "roundabout", "junction",
                     "parked", "road", "another car",
                     "someone", "somebody", "another driver", "the driver", "a driver",
                     "a van", "a lorry", "a truck", "the other car",
                     "behind", "behind me", "the car behind", "lights", "traffic", "queue",
                     "lane", "motorway", "slip road", "this morning",
                     "cyclist", "cyclists", "pedestrian", "pedestrians", "bike", "bicycle",
                     "on a bike", "on the ground", "crossing", "zebra", "pelican", "someone",
                     "somebody", "person", "child", "kid", "dog", "cat", "hurt", "injured",
                     "ambulance", "alright", "ok", "breathing", "what now", "what do i do")),
          "Stop, switch the engine off and put your hazards on, then check nobody is hurt and ring "
          "999 if they are. Swap names, addresses, phone numbers, insurers and policy numbers with "
          "the other driver, and photograph the cars, the road and the damage. If you did not "
          "exchange details you must report it to the police within 24 hours, and tell your insurer "
          "the same day even if you are not claiming.",
          report=True,
          bias=1,
          bikes=True,
          avoid=("market", "markets", "stock market", "share prices", "shares", "stocks",
                 "portfolio", "my investments", "house prices", "property prices",
                 "laptop", "computer", "pc", "phone", "iphone", "tablet", "app", "apps",
                 "software", "program", "browser", "windows", "game", "games", "console",
                 "server", "website", "wifi", "broadband", "printer", "android")),
    _entry("points", (("points", "penalty points", "endorsement", "driving ban", "tote"),
                     ("licence", "ban", "lose", "how many", "12", "6", "new driver", "revoked")),
          "Twelve points within three years and the court bans you for at least six months. A new "
          "driver loses the licence at six points within two years of passing, and then has to pass "
          "both tests again. Points stay on the licence for four years from the offence, or eleven "
          "for drinking and dangerous driving.",
          bias=1, avoid=("loyalty", "loyalty card", "loyalty points", "reward", "rewards",
                         "reward card", "nectar", "clubcard", "club card", "store card",
                         "boots card", "tesco", "coffee", "free coffee", "free drink", "voucher",
                         "vouchers", "supermarket", "shop", "shopping", "air miles", "my card",
                         "f1", "formula 1", "formula one", "grand prix", "motogp", "lap",
                         "laps", "fastest lap", "championship", "podium", "pole position",
                         "try", "tries", "goal", "goals", "touchdown", "conversion",
                         "rugby", "football", "soccer", "cricket", "netball", "basketball",
                         "hockey", "tennis", "league", "match", "game", "games", "score",
                         "scored", "scoring", "table", "season", "team", "teams",
                         "uni", "university", "ucas", "college", "sixth form", "a level",
                         "a-level", "alevel", "alevels", "a levels", "gcse", "gcses", "btec",
                         "degree", "entry requirements", "entry grades", "semester", "maths",
                         "math", "gcse maths", "a level maths")),
    _entry("red-light", (("red light", "amber", "traffic light", "traffic lights"),
                        ("stop", "go", "turn", "legal", "must", "allowed", "junction", "mean",
                         "means", "rules")),
          "Red means stop, and there is no turning left on red in the UK, whatever the road you are "
          "joining. Amber also means stop unless you are so close that stopping would be dangerous. "
          "Jumping a red is three points and a £100 fine, and cameras catch it whether or not anyone "
          "else is there.",
          bias=1, avoid=("christmas", "fairy", "rear", "bike", "bicycle", "cycle")),

    _entry("skid", (("skid", "skids", "skidded", "skidding", "lost control", "lost grip",
                    "lost the back", "spun", "spinning", "slide", "sliding", "slides",
                    "drive", "driving", "drives", "car", "van", "road", "roads", "motorway",
                    "tyre", "tyres", "pull away", "pulling away", "gear", "gears", "second gear",
                    "accelerator", "accelerate"),
                   ("ice", "icy", "black ice", "snow", "snowy", "sleet", "slush", "wet",
                    "slippery", "grit", "gritted", "ungritted", "winter", "frost", "freezing")),
          "Take your foot off the accelerator and off the brake, and steer gently where you want "
          "the front of the car to go: the tyres grip again by themselves, and pressing either "
          "pedal hard is what keeps a skid going. On ice, brake early and lightly in a straight "
          "line before the bend rather than in it, leave three or four times the usual gap, and "
          "pull away in second gear if the wheels spin. Anything under 7C and wet is worth "
          "slowing down for, because that is when ice forms without looking like it.",
          ask=("ice", "icy", "black ice", "snow", "snowy", "sleet", "slush", "skid",
               "skidded", "skidding", "slippery", "lost control", "lost grip", "winter",
               "wet", "gritted", "ungritted", "frost", "freezing"),
          avoid=_NOT_BUYING + NOT_BIKE + (
              "ice cream", "ice lolly", "ice lollies", "ice cube", "ice cubes", "ice bath",
              "freezer", "fridge", "ice rink", "skating", "ice hockey", "fish", "drink",
              "cocktail", "playground", "water slide", "slide show", "flood", "flooded",
              "leak", "leaking", "washing machine", "spin cycle", "condensation", "misted",
              "damp", "wet inside", "leaking in", "wet patch", "patch", "footwell",
              "carpet", "seats", "seat", "headlining", "roof", "ceiling", "inside the car",
              "windscreen", "windshield", "car window", "car windows", "side windows",
              "demist", "de-ice", "de ice", "defrost", "scraper", "scrape", "door lock",
              "frozen lock", "locked out", "frozen shut")),
    _entry("car-frost", (("windscreen", "windshield", "car window", "car windows", "side windows",
                          "screen", "mirrors", "car", "van"),
                         ("frost", "frosty", "frosted", "frosting", "iced", "icing", "icing up",
                          "icy", "ice", "de ice", "de-ice", "deice", "defrost", "frozen",
                          "freezing", "scrape", "scraping", "scraper", "clear the ice",
                          "clear ice", "clearing ice", "get the ice off", "ice off", "thaw")),
          "Don't pour boiling water on it: the glass can crack and the water refreezes. Spray a "
          "de-icer and scrape with a plastic scraper, work the heater and front demist, and clear "
          "the whole screen, the mirrors and the lights before you set off, because driving with a "
          "peephole is an offence. To stop it coming back, cover the screen overnight with an old "
          "towel or a mat, lift the wipers off the glass, and park facing east if you can.",
          ask=("car", "van", "windscreen", "windshield", "screen", "window", "windows", "mirror",
               "drive", "driving", "set off", "morning"),
          avoid=("oven", "freezer", "fridge", "cake", "chips", "shop window", "window cleaner",
                 "phone", "iphone", "android", "handset", "smartphone", "laptop", "macbook",
                 "computer", "pc", "mac", "monitor", "display", "tablet", "ipad",
                 "tv", "telly", "television", "screen is frozen", "screen has frozen",
                 "frozen screen", "not responding", "unresponsive", "app", "browser",
                 "scrap my car", "scrap a car", "scrap the car", "scrap my old car",
                 "scrap value", "scrapyard", "scrap yard", "breaker", "breakers",
                 "certificate of destruction", "get rid of the car", "get rid of my car",
                 "part exchange it", "we buy any car", "webuyanycar")),
    _entry("car-door-frozen", (("car door", "car doors", "car lock", "car window", "car windows",
                                "side windows", "door", "doors", "lock", "locks", "door lock",
                                "door seal", "seals", "handbrake", "wipers", "windscreen", "car"),
                               ("frozen", "freezing", "froze", "frozen shut", "stuck shut", "iced",
                                "ice", "frost", "wont open", "won't open", "stuck")),
          "Don't force the handle or the key: warm the key in your hand, put a little de-icer in the "
          "lock and push the door with the flat of your hand to break the seal round the rubber. "
          "Wipe the door seals with silicone spray or vaseline in autumn and they will not stick next "
          "time. Never pour hot water on a frozen lock or screen, because it refreezes straight "
          "away.",
          ask=("car", "van", "vehicle", "windscreen", "windshield", "car door", "car doors",
               "driving", "drive", "parked"),
          avoid=("front door", "back door", "kitchen door", "house", "home", "at home", "shed",
                 "gate", "garage door", "banging", "bangs", "slam", "slams", "hinge", "hinges",
                 "window cleaner", "inside of my windows", "windows at home",
                 "gear", "gears", "gearbox", "clutch", "revs", "revving", "neutral")),
    _entry("car-warm-up", (("car", "engine", "van", "vehicle", "diesel"),
                           ("warm up", "warming up", "warm it up", "warm my car",
                            "warm the car", "warm the engine", "warm my engine",
                            "how long should i warm", "let it warm", "idle", "idling",
                            "run the engine", "running the engine", "before driving",
                            "before i drive", "cold morning", "cold weather", "left running")),
          "Thirty seconds to a minute is plenty: an engine warms up by being driven gently, and "
          "idling for ten minutes just wastes fuel and dilutes the oil. Clear the windows, drive "
          "off keeping the revs low for the first couple of miles, and don't leave it running "
          "unattended to defrost, which is an offence on a public road and the easiest way to lose "
          "the car.",
          avoid=("slow to start", "takes a while to start", "takes ages to start",
                 "takes long to start", "struggles to start", "struggling to start",
                 "hard to start", "reluctant to start", "won't start", "wont start",
                 "won't fire", "wont fire", "won't turn over", "wont turn over"),
          ask=("car", "van", "engine", "diesel", "drive", "driving", "morning")),
    _entry("car-wash", (("wash a car", "wash the car", "wash my car", "washing a car",
                         "washing the car", "washing my car", "clean a car", "clean the car",
                         "clean my car", "car wash", "valet a car", "valet the car",
                         "valet my car", "valeting"),
                        ("how", "best way", "properly", "by hand", "should i", "jet wash",
                         "what do i need", "products", "soap", "shampoo", "worst", "tips")),
          "Two buckets, and the rinse bucket is the one that stops the scratches: soapy water in "
          "one, clean water in the other, and rinse the mitt after every panel. Work top down and "
          "do the wheels last with their own cloth, because brake dust drags grit across paint. "
          "Rinse before the soap dries, dry with a microfibre towel rather than letting it air dry, "
          "and do it out of direct sun. A coat of wax twice a year makes the next wash easier.",
          avoid=("scratch", "scratches", "scratched", "dent", "dents", "dented", "chip", "chips",
                 "bird", "tree sap", "tar", "rust", "paint", "repaint", "respray", "polish",
                 "machine polish", "swirl", "swirls", "cost", "price", "how much", "near me",
                 "seats", "interior", "inside", "alloy", "alloys", "carpet", "mat", "mats"),
          ask=("wash", "washing", "clean", "cleaning", "valet", "valeting", "soap", "shampoo")),
    _entry("tar-and-sap", (("tar", "tarmac", "bitumen", "tree sap", "sap", "resin", "pine resin",
                            "sticky stuff"),
                           ("car", "cars", "paint", "paintwork", "bodywork", "bonnet", "roof",
                            "wing", "door", "windscreen", "windshield", "screen", "bumper",
                            "boot", "mirror", "panel", "off", "remove", "removing", "get rid",
                            "clean", "cleaning"),
                           ("off", "remove", "removing", "get rid", "clean", "cleaning", "stuck")),
          "Soften it first: hold a cloth soaked in white spirit, petrol or a tar remover on the "
          "spot for a minute, then wipe, never a fingernail or a scourer, which lift the lacquer. "
          "Tree sap wants warm soapy water and then methylated spirit. On glass use a plastic "
          "scraper. Wash the panel and wax it again afterwards, because the solvent strips the "
          "wax too.",
          ask=("car", "cars", "paint", "paintwork", "bodywork", "bonnet", "roof", "wing", "door",
               "windscreen", "windshield", "screen", "bumper", "boot", "mirror", "panel"),
          avoid=("tariff", "tariffs", "tarragon", "tartan", "tart", "tartare", "sapphire",
                 "mustard", "road", "drive", "driveway", "path", "patio", "hands", "hair",
                 "clothes", "clothing", "carpet", "sole of my shoe")),
    _entry("car-seats", (("car seats", "car seat", "seats in my car", "car upholstery", "upholstery",
                          "fabric seats", "interior of my car",
                          "inside of my car", "car interior", "car mats", "car carpet",
                          "seats of my car"),
                         ("clean", "cleaning", "stain", "stains", "smell", "smells", "shampoo",
                          "valet", "spill", "spilled", "spilt", "vomit", "sick", "milk",
                          "coffee", "dirty", "scrub", "wash", "smelly", "stinks")),
          "Vacuum first, then use a weak mix of washing-up liquid and warm water: spray a small "
          "patch, work it in with a soft brush, and blot it out with a towel rather than soaking it, "
          "because water under the foam is what makes a car smell damp for weeks. Do the whole seat "
          "in patches so it dries evenly, and leave the windows open overnight. A leather car seat "
          "is the other job - saddle soap and a conditioner, never washing-up liquid - and it has "
          "its own answer.",
          avoid=("baby", "child", "children", "child seat", "booster", "isofix", "toddler",
                 "newborn", "infant", "fit", "fitting", "fits", "which", "best", "buy", "buying",
                 "price", "cost", "how much", "back seat", "rear facing", "forward facing",
                 "mat", "mats", "carpet", "boot", "floor", "floormats", "floor mats",
                 "leather"),
          ask=("clean", "cleaning", "stain", "stains", "smell", "smells", "vomit", "spill",
               "spilled", "spilt", "shampoo", "valet", "dirty", "stinks", "wash", "washing")),
    _entry("car-leather-seats", (("leather car seats", "leather car seat", "leather seats in my car",
                                  "leather seats in the car", "leather seats in a car",
                                  "car leather", "leather upholstery", "leather interior",
                                  "leather in my car"),
                                 ("clean", "cleaning", "condition", "conditioner", "crack",
                                  "cracked", "cracking", "crease", "creases", "stain", "stains",
                                  "dirty", "care", "look after", "dry", "shiny", "scuff", "scuffs")),
          "Saddle soap on a barely damp cloth, wiped over and left to dry away from the sun, then a "
          "thin layer of leather conditioner worked in while the leather is still slightly damp: "
          "that is the whole job, and never washing-up liquid, which strips the oils out and is what "
          "cracks a seat. No scrubbing either - a soft cloth and patience, and a cotton bud of "
          "rubbing alcohol for an ink mark. Condition twice a year, and more often if the car sits "
          "in the sun.",
          avoid=("sofa", "sofas", "jacket", "coat", "boots", "shoes", "bag", "handbag", "chair",
                 "chairs", "suite", "suede", "nubuck", "faux", "child", "children", "baby",
                 "toddler", "booster", "isofix", "fit", "fitting", "which", "best", "buy",
                 "price", "cost", "how much", "repair", "replace", "replacement", "cover",
                 "covers", "seat cover", "seat covers"),
          ask=("clean", "cleaning", "condition", "conditioner", "crack", "cracked", "stain",
               "stains", "dirty", "care", "look after")),
    _entry("car-wheels", (("alloy wheels", "alloy wheel", "alloys", "wheel trims", "hubcaps",
                           "brake dust", "wheels on my car", "the wheels on my car"),
                          ("clean", "cleaning", "wash", "washing", "polish", "seal", "sealing",
                           "kerbed", "kerb", "scuffed", "stained", "stubborn", "black", "dirty",
                           "get off", "get rid", "remove", "removing", "how")),
          "Brake dust is the black coating, and the mistake is letting it sit: it is mildly "
          "caustic once wet and it eats the lacquer. Use a wheel cleaner made for the job - the "
          "acid-free ones are safe on painted alloys - leave it a couple of minutes, then agitate "
          "the spokes with a soft brush and rinse. Never use the sponge that touches your paint, "
          "and wash wheels last or with their own bucket. A sealant or a wax twice a year makes the "
          "next wash a rinse.",
          avoid=("kerbed", "kerbside", "scratch", "scratched", "dent", "dented", "cracked",
                 "crack", "vibrating", "vibration", "wobble", "wobbling", "hot", "binding",
                 "squealing", "squeak", "tyre", "tyres", "pressure", "buy", "price", "cost",
                 "how much", "replace", "repair"),
          ask=("clean", "cleaning", "wash", "washing", "brake dust", "polish", "seal", "stained")),
    _entry("car-oil-use", (("using so much oil", "using oil", "burning oil", "oil use",
                            "oil consumption", "losing oil", "oil going down", "oil level drops",
                            "drinking oil", "uses oil", "oil disappearing", "blue smoke"),
                           ("car", "engine", "van", "why", "how much", "normal", "worry",
                            "problem", "is it", "should i", "topping up", "top up")),
          "An engine that uses a litre every 1,000 miles or so is within what most makers call "
          "normal, and many use more than people expect. Beyond that it is worn valve seals or "
          "piston rings, or a leak that only shows when it is hot: park over cardboard overnight "
          "and look for drips, and check the coolant for an oily film and the exhaust for blue "
          "smoke on start-up. Keep it topped up and get it looked at; running it low is what turns "
          "a cheap fix into a new engine.",
          avoid=("oil light", "oil warning", "oil change", "engine oil", "which oil", "what oil",
                 "how much oil", "olive", "cooking", "fryer", "frying", "hair", "skin", "castor",
                 "essential", "engine oil for", "cbd", "massage", "boiler", "central heating",
                 "radiator", "olives",
                 "cake", "cakes", "baking", "brownies", "brownie", "muffins", "sponge",
                 "biscuits", "pastry", "dough"),
          ask=("oil", "using", "burning", "smoke", "litre", "quart", "top up", "topping up")),
    _entry("driving-theory-test",
           (("theory test", "driving theory", "theory exam", "theory revision",
             "hazard perception", "multiple choice", "theory questions", "theory app"),
            ("pass", "passing", "passed", "revise", "revision", "study", "practise",
             "practice", "prepare", "book", "questions", "how", "tips", "hard", "ready")),
           "Fifty multiple-choice questions in 57 minutes and you need 43 right, then 14 "
           "hazard-perception clips where you click as the hazard develops and you need 44 out "
           "of 75. Learn from the official DVSA bank rather than a free app, practise the clips "
           "on a big screen, and book the test once practice scores sit in the high forties.",
           avoid=("failed", "fail", "failing", "gutted", "nervous", "scared", "anxious",
                  "worried", "panic", "test drive", "eye test", "blood test", "mot test")),
    _entry("dash-cam",
           (("dash cam", "dashcam", "dash cams", "dash cameras", "dash camera",
             "dash cam card", "front and rear camera", "car camera"),
            ("what", "whats", "which", "best", "recommend", "should", "buy", "card", "memory",
             "sd", "size", "fit", "fitted", "install", "wire", "power", "worth", "need",
             "how much", "do i need")),
           _dash_cam,
           ask=("what is a dash cam", "whats a dash cam", "which memory card", "which sd card",
                "what sd card", "which card", "what card", "what size", "how big", "how much",
                "best", "recommend", "should i buy", "worth it", "how do i fit", "how do i wire",
                "fit a dash cam", "install", "do i need", "what do i need"),
           bias=2),
]

from .costs import time_entries
ENTRIES += time_entries("tyres", "car-service")

ENTRIES.append(_entry(
    "keys-locked-in-the-car",
    (("keys in the car", "keys locked in", "keys locked inside", "keys are locked in",
      "keys are locked inside", "key is locked in", "keys are in the car", "key locked in",
      "locked my keys",
      "locked the keys in", "keys inside the car", "keys are in the car", "locked out of the car",
      "get keys out", "keys in the boot", "keys in the ignition", "keys stuck in the car",
      "keys locking", "keys keep locking", "key keeps locking", "keys lock inside",
      "keys locking inside", "locking itself in", "locks itself in", "car key keeps locking"),
     ("car", "van", "boot", "ignition", "locked", "lock", "how", "what", "do i", "help",
      "out", "inside")),
    ("A spare set is the first call, then breakdown cover - most policies include a lockout callout "
     "- and then a car locksmith, at about 50 to 120 pounds, who opens it with a wedge and a long "
     "rod in a few minutes without damage; an ordinary house locksmith often has nothing that fits "
     "a car door. Don't break a window unless someone is in danger, and if you must, a door glass "
     "is far cheaper than the windscreen or a rear quarter light. If the key is in the ignition "
     "with the engine running, stay with the car and do not let the tank run dry."),
    avoid=("lost my keys", "lost the keys", "where are my keys", "find my keys", "house key",
           "front door", "key fob", "key battery", "fob battery", "remote key", "immobiliser",
           "key won't turn", "key wont turn", "key will not turn", "key stuck in the ignition",
           "ignition lock", "steering lock", "keys not working", "spare key cost"),
    bias=1))

ENTRIES.append(_entry(
    "car-losing-power",
    (("car", "engine", "motor"),
     ("losing power", "loses power", "loss of power", "no power", "lacks power",
      "down on power", "sluggish", "gutless", "misfiring", "misfire", "misses a beat",
      "hesitates", "hesitation", "hesitant", "stuttering", "struggles uphill",
      "struggling uphill", "wont pull", "won't pull", "wont rev", "won't rev",
      "feels slow", "feels weak", "flat spot", "underpowered", "not accelerating")),
    "Start with the cheapest things and with what the car tells you: a misfire that shakes the "
    "whole car and puts the engine light on is usually a spark plug, a coil pack or a plug lead, "
    "and a garage reads the fault code for about 30 to 50 pounds and names which cylinder it is. "
    "A diesel that goes flat only when you ask for power is often a blocked fuel filter or a "
    "clogged particulate filter, and a petrol car that pulls less hard than it did but runs "
    "smoothly is usually a dirty air filter, a failing air-flow sensor or a sticking brake "
    "caliper. Check the tyre pressures first, because four soft tyres feel exactly like a sick "
    "engine, and if a warning light is on, have the codes read before replacing anything.",
    avoid=_NOT_BUYING + ("how fast", "top speed", "0 to 60", "more power", "remap", "tune",
                         "turbo upgrade", "electric", "ev", "battery range", "charger",
                         "noise", "noisy", "rattle", "knocking", "drone", "whine",
                         "light is on", "dashboard", "warning light"),
    bias=2))

ENTRIES.append(_entry(
    "park-in-a-tight-space",
    (("park", "parking", "parked", "parallel park", "parallel parking", "tight space",
      "tight spot", "small space", "reversing", "reverse park", "reverse into", "bay"),
     ("how do i", "how to", "how can i", "best way", "easier", "tips", "struggle",
      "always", "cant", "can't", "bad at", "nervous", "tight", "narrow", "small",
      "without hitting", "kerb", "curb")),
    "Parallel parking is three moves with the mirrors: pull up level with the car in front, about "
    "half a metre away with your back wheels level with theirs, then reverse slowly on full lock "
    "towards the kerb until your car sits at about 45 degrees, straighten the wheels to slide "
    "back past their bumper, and turn away from the kerb to swing the front in. Watch the mirrors "
    "and the back window rather than twisting round, and stop as soon as the back bumper is near: "
    "a 60cm gap is a comfortable park, and reversing into a bay is easier than driving into one "
    "because the back wheels turn tighter. If it goes wrong, pull out and start again - that is "
    "what the space in front is for.",
    avoid=_NOT_BUYING + ("parking ticket", "parking fine", "parking charge", "parking permit",
                         "neighbour", "neighbor", "neighbours", "neighbors", "in my space",
                         "in my spot", "my driveway", "blocking me", "blocking my",
                         "blocked in", "blocked my", "won't move", "wont move", "next door",
                         "someone else's car", "somebody's car",
                         "car park cost", "parking app", "clamp", "clamped", "tow", "towed",
                         "residents parking", "parking space to rent", "blue badge",
                         "disabled bay", "bay number",
                         "bay leaf", "bay leaves", "bay tree", "bay trees", "laurel",
                         "bay window", "bay windows",
                         "how do i dry", "drying", "dried",
                         "caravan", "caravans", "motorhome", "motor home", "camper", "trailer",
                         "towing", "tow a", "lorry", "truck", "hgv", "bus",
                         "grow", "growing", "grows", "plant", "plants", "planting", "soil",
                         "seed", "seeds", "sow", "pot", "pots", "window", "windowsill",
                         "balcony", "garden", "greenhouse", "veg", "vegetable", "vegetables",
                         "herbs",
                         "diabetes", "diabetic", "pre-diabetes", "prediabetes",
                         "blood sugar", "hba1c",
                         "medical condition", "medical conditions", "health condition",
                         "health conditions", "heart condition", "heart conditions",
                         "skin condition", "skin conditions", "thyroid condition",
                         "my condition", "thyroid", "disease", "illness", "diagnosis",
                         "surgery", "operation", "treatment",
                         "hair", "hairline", "hair loss", "bald", "balding", "thinning",
                         "grey", "gray", "greying", "wrinkles", "ageing", "aging",
                         "payment", "payments", "charge", "charges", "chargeback",
                         "refund", "refunds", "transaction", "transactions", "direct debit",
                         "standing order", "standing orders", "transfer",
                         "my bank", "bank account", "bank accounts", "bank transfer",
                         "bank statement", "bank charge", "bank charges", "bank payment",
                         "invoice", "bill", "bills", "decision", "decisions", "policy", "ruling",
                         "ban", "suspension", "eviction", "conviction", "verdict",
                         "email", "letter", "text message", "snapshot", "string", "undo",
                         "polarity", "battery", "batteries", "wiring", "motor",
                         "hill", "hills", "slope", "slopes", "on a hill", "on a slope",
                         "round a corner", "around a corner", "corner"),
    bias=1))

ENTRIES.append(_entry(
    "where-to-park",
    (("park", "parking", "parked", "park the car", "car park", "multi storey", "multistorey",
      "park and ride", "park & ride", "free parking", "parking space",
      "leave the car", "leave my car", "leaving the car", "leave the car near",
      "park the car", "put the car"),
     ("where", "wheres", "weres", "whers", "best place", "good place", "place to park",
      "anywhere", "somewhere", "is there", "near", "nearby", "round here", "around here",
      "near me", "near the station", "town", "town centre", "city centre", "cheap",
      "cheapest", "free", "closest", "leave")),
    "The side streets five to ten minutes further out are where the free and cheap spaces are: "
    "read the sign at the entrance, because a residents' bay or a one-hour limit is what the "
    "tickets come from. For a station or a town centre, the station car park or a park and ride "
    "is usually cheaper than the multi-storey, and the parking apps (RingGo, PayByPhone, JustPark) "
    "show the live price and let you top up from your phone. Photograph the bay number and the "
    "sign before you walk off.",
    avoid=_NOT_BUYING + ("parallel", "reverse", "reversing", "tight space", "tight spot",
                         "how do i park", "how to park", "parking ticket", "parking fine",
                         "in gear", "handbrake", "when parked", "parked on a hill",
                         "penalty charge", "appeal", "clamped", "towed", "blue badge",
                         "disabled bay", "residents permit", "parking permit", "neighbour",
                         "neighbor", "driveway", "blocking", "blocked in", "caravan",
                         "motorhome", "camper", "trailer", "lorry", "truck", "hgv",
                         "remember", "remembering", "forgot", "forget", "where i parked",
                         "where did i park", "did i park", "parked it",
                         "lost my car", "cant find my car", "can't find my car",
                         "available", "availability", "hotel", "guest", "book with",
                         "sunday", "sundays", "saturday", "saturdays", "bank holiday",
                         "high street", "on street", "on-street", "yellow line", "yellow lines",
                         "allowed", "can i park on", "how long can i", "maximum stay",
                         "is it free", "after 6", "after 6pm", "evening",
                         "is parking free", "parking free", "free parking at", "free at",
                         "how much is parking", "how much for parking", "parking cost",
                         "cost of parking", "price of parking", "parking prices",
                         "is parking", "is there parking"),
    bias=1))

ENTRIES.append(_entry(
    "hybrid-worth-it",
    (("hybrid", "hybrids", "hybrid car", "hybrid cars", "plug in hybrid", "plug-in hybrid",
      "self charging hybrid"),
     ("worth", "worth it", "should i", "buy", "buying", "get", "better", "cheaper", "run",
      "running", "cost", "costs", "save", "saving", "economy", "mpg", "petrol", "diesel",
      "or petrol", "than petrol", "new car", "second hand")),
    ("A hybrid is worth it for town and stop-start driving and not for the motorway: the motor "
     "does the pulling away, the engine does the cruising, and the battery is refilled by "
     "braking, so the saving comes from the slow work where a petrol engine is thirstiest. "
     "Expect 15 to 25% less fuel in town and very little at a steady 70. A self-charging hybrid "
     "costs a few thousand more than the same petrol car, so count how many years of that saving "
     "it takes to pay the difference. A plug-in hybrid is a different bet: it only pays if your "
     "normal day fits inside its 20 to 40 miles of electric range and you plug it in at home, "
     "because one running on an empty battery is heavier than the petrol car it replaced."),
    avoid=("working", "work from home", "office", "pattern", "job", "employer", "bike",
           "teabag", "hybrid tea", "rose")))
ENTRIES.append(_entry(
    "car-dent",
    (("dent", "dents", "dented", "ding", "dinged", "dinge", "creased", "crease",
      "dinner plate", "sucked in", "pushed in", "pushed the panel in"),
     ("car", "cars", "van", "door", "doors", "panel", "panels", "bumper", "wing", "wings",
      "bonnet", "bodywork", "paint", "paintwork", "parking", "hit", "reversed into")),
    "A dent with unbroken paint in a flat steel door or wing is a job for paintless dent removal: "
    "a mobile specialist works the metal back from behind and keeps the original paint, for about "
    "60 to 150 pounds a panel, which is half what a bodyshop charges to fill and spray it. A "
    "plastic bumper dent is often pushed back out by hand from behind after warming it with a "
    "hairdryer or a bucket of hot water, and a 10 to 20 pound suction puller lifts a shallow "
    "dinner-plate dent in a flat panel. If the paint has cracked, or the crease is sharp, the "
    "metal is stretched and only a bodyshop will make it right. Claims are rarely worth it - the "
    "excess is usually more than the repair, and the premium rises for three years.",
    avoid=_NOT_BUYING + ("dentist", "dental", "denture", "dentures", "tooth", "teeth", "gum",
                         "table", "tables", "floor", "floorboard", "skirting", "wall", "walls",
                         "plaster", "wood", "wooden", "furniture", "doorframe", "door frame",
                         "tin", "tins", "can", "cans", "saucepan", "pan", "pan lid", "suitcase",
                         "washing machine", "fridge", "freezer", "dryer", "guitar", "drum",
                         "hat", "hats", "helmet", "pride", "confidence", "ego", "reputation",
                         "insurance", "claim", "excess", "write off", "write-off", "sell",
                         "value", "buy", "buying", "price", "cost", "how much",
                         "front door", "back door",
                         "internal door", "bedroom door", "kitchen door", "bathroom door",
                         "cupboard door", "wardrobe door", "garage door", "hinge", "hinges",
                         "latch", "mortice", "gloss", "undercoat", "primer", "primer", "plane",
                         "planing", "sanding", "spindle", "skirting", "wardrobe", "cupboard",
                         "cabinet", "usual door", "kitchen cupboard"),
    bias=1))

ENTRIES.append(_entry(
    "car-paint",
    (("paint", "painted", "paintwork", "lacquer", "clear coat", "clearcoat", "top coat",
      "topcoat", "respray", "chips", "chipped", "chipping", "peeling", "peeled", "flaking",
      "flaked", "blistering", "bubbling", "coming off", "came off", "stone chip",
      "stone chips", "scuff", "scuffs", "scuffed", "scrape", "scrapes", "scraped",
      "touch up", "touch-up", "touch in", "touched up"),
     ("car", "cars", "van", "vans", "bonnet", "bumper", "bumpers", "bodywork", "paintwork",
      "wing mirror", "sill", "tailgate", "wheel arch", "alloy", "alloys", "boot lid",
      "door card", "quarter panel")),
    "That is a paint repair rather than a polish. A stone chip smaller than a fingernail is a "
    "touch-in pen and a blob of clear lacquer, done within a week or two because bare metal rusts; "
    "clean it and dry it first, and keep the wax off the bare patch. Lacquer that has lifted in "
    "sheets - usually on a bonnet or a roof that has had sun - cannot be polished back: it has to "
    "be flattened and repainted, which is 200 to 400 pounds a panel at a body shop or rather less "
    "for a smart repair on one panel. Do not use a machine polisher on a peeling patch, because "
    "it lifts the edge and takes the paint with it. A scuffed bumper is usually paint transfer "
    "and comes off with a cutting compound before anything needs spraying.",
    avoid=("seat", "seats", "interior", "dent", "dents", "dented", "scratch", "scratches",
           "scratched", "how much", "cost", "price", "quote", "insurance", "claim",
           "alloy scuff", "alloy scuffs",
           "window", "windows", "glass", "windscreen", "windshield", "windscreen chip",
           "scrap", "scraps", "scrapped", "scrapping", "write it off", "write off",
           "worth fixing", "worth repairing", "worth keeping", "replace it", "new car",
           "get rid", "keep fixing", "mend it", "let it go", "breakers"),
    bias=2))

ENTRIES.append(_entry(
    "screen-wash-top-up",
    (("screen wash", "screenwash", "washer fluid", "windscreen washer", "windscreen washers",
      "washer bottle", "washer jet", "washer jets", "washers", "wash bottle"),
     ("top up", "topup", "top it up", "fill", "refill", "how do i", "how to", "where do i",
      "how much", "mix", "concentrate", "dilute", "running low", "empty", "ran out",
      "not working", "wont spray", "won't spray", "nothing comes out", "weak spray",
      "frozen", "smear", "smearing")),
    "Open the bonnet and look for the cap with the windscreen-and-spray symbol on it - usually "
    "blue, and never the yellow one, which is coolant. Mix screen wash concentrate with water as "
    "the bottle says: about one part wash to four parts water in summer, one to one in winter, and "
    "neat in a hard frost, because the alcohol in it is what stops the bottle freezing and the "
    "smear on a gritty screen. Never use washing-up liquid - it foams, smears and blocks the "
    "jets. Fill to the neck, and if the spray is still weak, push a pin into the jet and adjust "
    "the aim with a needle.",
    avoid=_NOT_BUYING + ("light", "lights", "warning", "symbol", "dash", "dashboard",
                         "comes on", "came on", "stays on", "mot", "advisory", "leak",
                         "washing machine", "dishwasher", "washer smells", "washer smell",
                         "smell", "smells", "smelly", "musty", "mould", "mold", "drum",
                         "laundry", "clothes", "cycle", "spin", "filter", "limescale",
                         "leaking", "pump", "motor", "fuse", "cost", "price", "how much does",
                         "dealer", "garage", "service"),
    bias=1))

ENTRIES.append(_raw_entry(
    "fuel-price",
    (("petrol", "diesel", "unleaded", "fuel", "petrol price", "petrol prices", "diesel price",
      "diesel prices", "litre of petrol", "litre of diesel", "gallon of petrol", "fuel prices"),
     ("how much", "how much is", "price", "prices", "cost", "costs", "per litre", "a litre",
      "per gallon", "a gallon", "going rate", "average", "cheapest", "expensive", "much is",
      "much does", "at the moment", "now", "today")),
    "There is no fixed figure: the forecourt sign is the only price that matters and it moves "
    "week to week. As I write, unleaded sits near 1.35 to 1.50 pounds a litre and diesel a few "
    "pence above it, with motorway services the dearest and the big supermarkets the cheapest. "
    "The PetrolPrices app or the government fuel-price finder shows every station near you, and "
    "a supermarket loyalty card often takes a few pence off.",
    avoid=("smell", "smells", "smelt", "smelling", "on my hands", "on my skin", "on my clothes",
           "spilt", "spilled", "misfuel", "wrong fuel", "petrol in a diesel", "diesel in a",
           "mpg", "economy", "fuel economy", "how many litres", "tank", "tank size", "range",
           "lawnmower", "lawn mower", "strimmer", "generator", "heater", "paraffin",
           "to fill up", "fill up", "road tax", "insurance", "an mot", "mot", "service",
           "how much does it cost to run", "per mile", "per month",
           "split", "splitting", "share", "sharing", "halves", "go halves", "divide",
           "between us", "between the two of us", "who pays", "who owes", "each pay",
           "chip in", "chipped in", "petrol money", "fuel money", "money for petrol",
           "money for fuel", "towards petrol", "towards fuel",
           "put in for", "put in", "put towards", "going towards", "between us"),
    bias=2))

ENTRIES.append(_entry(
    "washer-jets",
    (("washer jet", "washer jets", "screen wash jet", "screen wash jets", "windscreen washer",
      "washer nozzle", "washer nozzles", "jet", "jets", "washers", "washer"),
     ("blocked", "blockage", "clogged", "not working", "wont spray", "won't spray",
      "not spraying", "weak", "one side", "only one", "nothing comes out", "no water", "stuck",
      "how do i clear", "clear", "unblock", "smear")),
    "Pop the jet out, or unscrew it if it is the fixed sort, and soak it in warm water with a drop "
    "of vinegar, then push a pin through the nozzle in the direction the water comes out - not "
    "against it, which pushes the grit back in. Aim the jet at the middle of the windscreen with "
    "the same pin while the bonnet is open, since a blocked jet that is refitted crooked just "
    "smears. If every jet is weak at once, the filter in the bottle or the pump is the part, not "
    "the nozzles.",
    avoid=("light", "warning", "symbol", "dashboard", "top up", "car wash", "wash the car",
           "price", "cost", "buy", "replace the windscreen", "windscreen wipers", "frozen")))

A_CAR_IS_NAMED = ("car", "cars", "van", "vans", "vehicle", "motor", "motorbike", "motorcycle",
                  "suv", "estate", "hatchback", "saloon", "pickup", "4x4", "camper", "caravan",
                  "engine", "boot", "bonnet", "dashboard", "wipers") + tuple(MODELS)


def _a_car_is_named(understood):
    read = understood if isinstance(understood, dict) else {}
    words = set(_words_of_a_car_line(read))
    return any(word in words or (" " in word and word in " ".join(words)) for word in A_CAR_IS_NAMED)


def _words_of_a_car_line(read):
    clean = str(read.get("clean") or read.get("text") or "").lower()
    clean = re.sub(r"[^a-z0-9% ]", " ", clean)
    return [word for word in clean.split() if word]


ENTRIES.append(_raw_entry(
    "car-transfer-name",
    (("transfer", "transferring", "put it in my name", "put the car in my name",
      "change of owner", "change the owner", "change of keeper", "change the keeper",
      "registered keeper", "log book", "v5c", "v5", "new keeper", "green slip", "in my name",
      "into my name", "to my name", "ownership", "dvla"),
     ("car", "van", "vehicle", "motorbike", "motorcycle", "bike", "motor", "it")),
    "Fill in the buyer's details on the V5C, tear off the green slip (V5C/2) and give that to "
    "them, then send the rest of the log book to DVLA at SA99 1BA - or do both online with the "
    "reference number on the front. Keep the yellow slip: it is your proof you told them. The new "
    "keeper needs the green slip to tax the car, and their own insurance from the moment they "
    "drive it away, so do the paper at the handover rather than later: until DVLA has the change "
    "on record, a parking ticket or a camera fine is still yours.",
    avoid=("insurance", "insure", "no claims", "no-claims", "ncb", "policy", "premium",
           "warranty", "extended warranty", "finance", "lease", "leasing", "hire purchase",
           "breakdown cover", "gap insurance"),
    guard=_a_car_is_named))

ENTRIES.append(_raw_entry(
    "car-battery-health",
    (("battery health", "battery healthy", "keep the battery healthy",
      "keep my battery healthy", "look after the battery", "look after my battery",
      "battery last longer", "battery lasts longer", "make the battery last",
      "make my battery last", "maintain the battery", "battery care", "healthy", "look after",
      "last longer", "longer life", "keep it going"),
     ("battery", "batteries"),
     ("car", "van", "vehicle", "engine", "12v", "under the bonnet", "it")),
    "A car battery dies from short trips rather than age: a five-minute run never puts back what "
    "the starter took, so give it a twenty-minute drive every couple of weeks, or a smart charger "
    "once a month through the winter. If there is white fur on the terminals, pour warm water over "
    "them, brush it off and smear a little grease on, and check both clamps are tight - a loose one "
    "cranks like a flat battery. Most last three to five years, and a garage can test one in five "
    "minutes; a slow crank and lights that dim at idle are the signs it is going.",
    avoid=("phone", "iphone", "android", "laptop", "tablet", "macbook", "settings", "smoke alarm",
           "fire alarm", "doorbell", "aa battery", "aaa battery", "remote", "controller",
           "hearing aid", "watch", "ebike", "e bike", "scooter"),
    bias=1, guard=_a_car_is_named))

ENTRIES.append(_raw_entry(
    "car-alarm-going-off",
    (("alarm", "alarm going off", "keeps going off", "keeps sounding", "going off on its own",
      "wont stop", "won't stop", "sounding", "siren", "immobiliser", "beeping"),
     ("car", "van", "vehicle", "boot", "bonnet", "doors", "fob", "key", "it")),
    "Three things cause most of these, in this order: a car battery that is going flat (low "
    "voltage reads to the alarm as someone tampering with it), a boot or bonnet switch that is not "
    "quite shut, and an interior sensor picking up a moth, a pet or a lorry going past. Charge or "
    "test the battery first, push every door and the boot shut firmly, and lock it with the key in "
    "the door rather than the fob - if it stays quiet that way, the fob or its battery is the "
    "fault. A garage can read the alarm's fault code, which names the sensor that triggered it.",
    avoid=("clock", "wake up", "waking", "snooze", "morning", "get up", "sleep", "smoke alarm",
           "fire alarm", "burglar alarm", "house alarm", "doorbell", "phone", "iphone", "android",
           "reminder", "work"),
    guard=_a_car_is_named))

ENTRIES.append(_raw_entry(
    "car-roof-load",
    (("mattress", "mattresses", "sofa", "sofas", "settee", "couch", "wardrobe", "fridge",
      "freezer", "washing machine", "table", "ladder", "christmas tree", "tree",
      "kayak", "canoe", "paddleboard", "surfboard", "timber", "plank", "planks", "plywood",
      "bike", "bikes", "bicycle", "bicycles", "roof box", "roof rack", "roof racks",
      "roof bars", "roof bar", "ratchet strap", "ratchet straps", "tie down", "tied down",
      "tying down", "lash down"),
     ("roof", "roof box", "roof rack", "roof racks", "roof bars", "roof rails", "car", "cars",
      "van", "strap", "straps", "strapped", "rope", "ropes", "tie", "tied", "rack", "carrier",
      "transport", "carry", "carrying", "load")),
    "On the bars, never on the roof skin: two straps over the load and two through its own frame "
    "or handles, pulled until you cannot shift it by hand, with a half twist in any flat strap so "
    "it does not hum at speed. Most roof bars take 50 to 75 kg, so put the heavy end forward and "
    "keep it low, and stay inside the overhang rules - nothing past the front, 305 mm on each side "
    "and a metre behind at most, with something bright tied to the end that does. A mattress or a "
    "sheet of board wants a roof bag or a box, or it will flap, drink water and tear at the straps.",
    avoid=("into a van", "into the van", "in the van", "in the back", "back of the van",
           "into the car", "into my car", "into the boot", "in the boot", "inside the car",
           "house", "home", "flat roof", "roof tile", "roof tiles", "tiles", "chimney",
           "gutter", "gutters", "leak", "leaking", "attic", "loft", "shed", "insulation",
           "felt", "shingles", "slate", "slates",
           "plant", "planting", "grow", "growing", "dig", "roots", "prune", "pruning",
           "sap", "tree sap", "bird", "birds", "pollen", "fallen leaves",
           "upstairs", "downstairs", "up the stairs", "down the stairs", "stair", "stairs",
           "landing", "through the door", "doorway", "through the hall", "hallway",
           "into the house", "into my flat", "on my own", "by myself", "on your own",
           "two people", "two of us",
           "train", "trains", "tube", "underground", "platform", "platforms", "bus", "buses",
           "coach", "ferry", "plane", "flight", "flights", "airport", "tram", "trams",
           "tow bar", "towbar", "tow ball", "towball", "trailer", "boot rack", "rear rack",
           "fix", "broken", "replace", "not working", "won't open", "wont open",
           "how much", "cost", "costs", "price", "prices", "cheapest", "buy", "buying",
           "lease", "hire", "for sale", "second hand"),
    bias=2))

ENTRIES.append(_entry(
    "what-a-handbrake-is-for",
    (("handbrake", "hand brake", "parking brake", "electronic handbrake", "handbrakes"),
     ("what", "how", "use", "used", "when", "should", "hill", "park", "parked", "pull",
      "button", "light", "hold")),
    "The handbrake holds the car still while you are stopped, so pull it up firmly (or press the "
    "electronic button) every time you park, and check the red brake light on the dashboard. Use "
    "it for hill starts instead of holding the car on the clutch, which wears the plate. A "
    "handbrake is not for slowing down at speed - that is the footbrake - and on a steep hill "
    "leave it in gear as well.",
    avoid=("how many lessons", "learn to drive", "loose", "weak", "not holding", "slip",
           "fails", "mot", "cable", "adjust", "cost", "price", "repair")))

ENTRIES.append(_entry(
    "reading-a-tyre-size",
    (("tyre size", "tyre sizes", "tire size", "numbers on the tyre", "numbers on my tyre",
      "tyre markings", "sidewall", "205", "195", "tyre number", "what do the numbers"),
     ("tyre", "tyres", "tire", "tires", "mean", "means", "read", "reading", "size", "buy",
      "replace", "new tyre", "what does", "explain")),
    "The size is moulded into the sidewall as three numbers and a letter, for example 205/55 R16 "
    "91V: 205 is the width in millimetres, 55 is the sidewall height as a percentage of that "
    "width, 16 is the wheel diameter in inches, and 91V is the load index and speed rating. Match "
    "all four when you buy, and check the tyre placard inside the driver's door or fuel flap for "
    "the size and pressures the car was built for.",
    avoid=("cost", "price", "cheap", "best", "winter", "tread depth", "1.6mm", "legal")))

ENTRIES.append(_entry(
    "what-a-clutch-is",
    (("clutch", "clutches", "manual gearbox", "clutch pedal"),
     ("what is", "what's a", "whats a", "what does", "explain", "mean", "means",
      "definition", "what is a", "purpose")),
    "The clutch is the pedal that disconnects the engine from the gearbox, so you can change gear "
    "and pull away without the engine stalling: press it all the way down to change, then bring "
    "it up slowly as you add a little accelerator. Hold the car on the handbrake rather than on "
    "the clutch at a junction, because slipping it for long wears the plate out.",
    avoid=("slipping", "slip", "burning", "smell", "cost", "price", "replace", "replacement",
           "how long", "last", "bleed", "fluid", "pedal", "judder", "noise", "noisy",
           "went", "gone", "failed", "fault", "how do i", "how to", "pull away",
           "biting point", "riding the clutch", "change gear", "manual car", "stalling")))

ENTRIES.append(_entry(
    "driving-an-electric-car",
    (("electric car", "electric cars", "ev", "evs", "e-car", "electric vehicle",
      "electric van", "one pedal", "regenerative braking", "regen"),
     ("drive", "driving", "how", "different", "first time", "range", "battery", "charging",
      "brake", "pedal", "gear", "start")),
    "An electric car drives like an automatic with one difference: when you lift off the "
    "accelerator it slows itself down and puts charge back in the battery, so you brake with the "
    "right pedal for most stops and use the left one only for a hard stop. Treat the range as "
    "about 70% of the official figure in winter, charge to 80% for everyday use and 100% only "
    "before a long run, and check the car's own route planner for chargers rather than arriving "
    "on 5%.",
    avoid=("cost", "price", "buy", "lease", "worth", "grant", "charge at home", "charger",
           "how long does it take to charge", "charging point", "salary sacrifice", "tax",
           "insurance", "range of the", "battery health", "hybrid")))

WRONG_WITH_IT = (
    "stuck", "is stuck", "stuck in", "seized", "jammed", "wont go into", "won't go into",
    "hard to get into", "overheat", "overheating", "overheated", "steam", "temperature",
    "smells", "smell", "smoking", "leak", "leaking", "warning light", "light on the dash",
    "grinding", "judder", "juddering", "slipping", "squeal", "squealing", "squeak", "noise",
    "noisy", "rattling", "rattle", "vibrat", "shakes", "shaking", "pulls to", "pulls a bit",
    "pulling to", "cuts out", "cutting out", "cut out", "keeps stalling", "keeps cutting",
    "needs a", "needs new", "needs replacing", "replace", "replacing", "replacement",
    "cost", "costs", "price", "how much", "on ice", "in ice", "icy", "snow", "skid", "slippery",
    "wet road", "crash", "crashed", "accident", "collision", "rear ended", "rear-ended",
)


def _says_something_is_wrong(understood):
    line = " " + ((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    return any(shape in line for shape in WRONG_WITH_IT)


def _how_to(reply):

    def answer(memory, understood):
        if _says_something_is_wrong(understood):
            return None
        return reply

    return answer


DRIVING_A_WAY = ("drive", "driving", "driven", "learn", "learning", "how", "to do", "control")

ENTRIES.append(_entry(
    "clutch-biting-point",
    (("manual", "manual car", "manual gearbox", "clutch", "biting point", "biting-point",
      "first gear", "stop stalling", "stop the car stalling", "stalling when i pull away",
      "pull away", "pull off", "set off"),
     DRIVING_A_WAY + ("smoothly", "pull away", "pull off", "move off", "gas", "revs", "pedal",
                      "car", "start")),
    _how_to("A manual car goes because the clutch reaches the biting point before any gas: clutch down, "
     "first gear, then let the pedal up slowly until the bonnet lifts and the revs dip, hold it "
     "there, and add a little gas as you let it up the rest of the way. Practise finding that "
     "point five or ten times on a flat quiet road, because pulling away is only that point held "
     "while the car moves. Take your foot right off the pedal once you are moving - riding it is "
     "what wears a clutch out."),
    avoid=("how much", "cost", "costs", "price", "replace", "replacing", "replacement",
           "worn", "slipping", "slips", "smell", "burning", "noise", "noisy", "judder",
           "fluid", "hydraulic", "cable",
           "licence", "license"))),

ENTRIES.append(_entry(
    "change-gear-smoothly",
    (("change gear", "changing gear", "gear change", "gear changes", "change up", "change down",
      "gears"),
     ("smooth", "smoothly", "jerky", "jerk", "lurch", "kangaroo", "how", "when", "revs", "rpm",
      "clutch", "drive", "driving", "car")),
    _how_to("Change up at about 2,000 to 2,500 revs in a petrol car, or 1,800 to 2,000 in a diesel, and "
     "let the clutch up to the biting point before you add gas. The lurch is a mismatch between "
     "engine speed and road speed, so on a downward change give the revs a small blip as the "
     "clutch comes up. Guide the lever gently through the gate instead of yanking it: the gearbox "
     "only has one way in."),
    avoid=("gearbox", "automatic", "won't go into gear", "wont go into gear", "sticks in gear",
           "grinding", "crunch", "oil", "fluid", "replace", "cost", "noise", "whine"))),

ENTRIES.append(_entry(
    "three-point-turn",
    (("three point turn", "3 point turn", "three-point turn", "turn in the road",
      "turn the car round", "turn the car around", "turn round in the road"),
     ("turn", "road", "car", "how", "do", "drive", "kerb", "reverse")),
    _how_to("Left lock across to the far kerb, reverse back on right lock, then forward on left lock "
     "again - three moves and you are round, which is why it is usually called a turn in the "
     "road now. Every move starts with a mirror and a shoulder check, and the kerb is a limit "
     "rather than a target. Keep it slow on the clutch: speed is what makes a turn in the road "
     "go wrong."),
    avoid=("sat nav", "satnav", "route", "motorway", "roundabout", "junction", "no u turn",
           "u-turn", "u turn sign", "banned"))),

ENTRIES.append(_entry(
    "driving-in-the-dark",
    (("in the dark", "at night", "night driving", "after dark", "headlights", "headlight",
      "full beam", "dipped beam", "main beam", "high beam"),
     ("drive", "driving", "car", "road", "glare", "oncoming", "see", "visibility", "dazzled",
      "dazzle", "use", "when")),
    _how_to("At night on an unlit road with nothing in front, use full beam; dip the moment a "
     "car appears, because a main beam left on dazzles the driver coming towards you. Drive so "
     "you could stop within the distance your lights actually show, which is usually slower than "
     "in daylight."),
    avoid=("back", "knee", "shoulder", "neck", "hip", "leg", "ankle", "wrist",
           "night light", "leave a light", "light on", "child", "children", "kid", "kids",
           "toddler", "scared of the dark", "bedtime", "bed", "bulb", "not working", "broken",
           "dim", "fog", "foggy", "mist", "xenon", "led bulb", "convert",
           "sees things", "things in the dark", "monsters", "scared", "afraid", "frightened",
           "he says", "she says", "my son", "my daughter", "wont sleep", "won't sleep"))),

ENTRIES.append(_entry(
    "parking-on-a-hill",
    (("park on a hill", "parking on a hill", "park on a slope", "parked on a hill",
      "parking on a slope", "facing downhill", "facing uphill", "wheels turned", "turn the wheels"),
     ("hill", "hills", "slope", "park", "parking", "parked", "kerb", "curb", "handbrake",
      "how", "should", "which way")),
    ("Park facing downhill with the front wheels turned into the kerb, and facing uphill with "
     "them turned away from it, so the car rolls into the kerb rather than into the road if it "
     "moves. Leave it in first gear facing uphill, reverse facing downhill, and pull the "
     "handbrake up hard. On a steep hill put a chock or a brick behind a wheel if you have one, "
     "and on an automatic use P, which locks the gearbox."),
    avoid=("hill start", "stalling", "clutch", "rolling back", "biting point", "junction",
           "hill walking", "hills to walk", "walk up", "climb")))

ENTRIES.append(_entry(
    "reversing-round-a-corner",
    (("reverse round a corner", "reversing round a corner", "reverse around a corner",
      "reversing around a corner", "reverse round the corner", "reversing round the corner"),
     ("reverse", "reversing", "how", "drive", "driving", "mirror", "mirrors", "check",
      "should", "corner")),
    ("Pull up just before the corner on the left and stop, then look over your left shoulder "
     "through the back window and check the right mirror for anything coming. Reverse slowly, "
     "slipping the clutch, and steer so the back of the car follows the kerb round the corner in "
     "a smooth arc about half a metre out, straightening as it comes; stop before you swing the "
     "front out into the road and look again, because the front of the car sweeps wide."),
    avoid=("parallel park", "park in a tight", "tight space", "bay", "reverse park",
           "reverse into a space")))


def _the_click_on_a_turn(memory, understood):
    clean = (understood.get("clean") or understood.get("text") or understood.get("plain") or "")
    clean = clean if isinstance(clean, str) else " ".join(str(part) for part in clean)
    clean = clean.lower()
    if any(shape in clean for shape in _A_DEFINITION_ASK):
        return _CV_JOINT_DEFINITION
    return _THE_CLICK_ON_A_TURN_REPLY


_A_DEFINITION_ASK = ("what is a cv", "what is a drive", "what is cv joint", "whats a cv",
                     "whats a driveshaft", "what does a cv", "what does a drive",
                     "what is the cv joint", "what does a cv joint do", "what is that cv")
_THE_CLICK_ON_A_TURN_REPLY = (
           "A click or clunk that keeps time with the steering is usually a CV joint on the "
           "driveshaft: the rubber boot splits, the grease comes out and the joint wears. Look "
           "behind the front wheels for a torn boot and grease sprayed round the inside of the "
           "arch. A garage replaces the joint or the shaft, an hour or two of work, and it is "
           "worth doing before it fails - a joint that lets go leaves the car with no drive. A "
           "single clunk on full lock can also be a top mount or a drop link, which is cheaper.")
_CV_JOINT_DEFINITION = (
           "A CV joint - constant velocity joint - is the flexible coupling at each end of a "
           "driveshaft, so the shaft can turn the wheel while the suspension moves and the wheel "
           "steers. It is packed with grease and wrapped in a rubber boot; when the boot splits "
           "the grease goes, grit gets in and it starts clicking on turns. Outer joints sit "
           "behind each front wheel, the inner ones at the gearbox.")
ENTRIES.append(
    _entry("clicking-on-a-turn",
           (("click", "clicks", "clicking", "clunk", "clunks", "knocking", "knock", "tapping",
             "tap", "popping", "cv joint", "driveshaft", "drive shaft"),
            ("turn", "turns", "turning", "steering", "steering wheel", "full lock", "on lock",
             "corner", "corners", "cornering", "round a bend", "when i steer", "wheel when i",
             "what is a cv", "whats a cv", "what does a cv", "what is a drive", "drive shaft")),
           _the_click_on_a_turn,
           ask=("car", "cars", "van", "vehicle", "wheel", "wheels", "steering", "brake",
                "driveshaft", "axle"),
           avoid=("brake", "brakes", "braking", "pedal", "knee", "knees", "jaw", "shoulder",
                  "hip", "ankle", "neck", "back", "finger", "fingers", "wrist", "elbow",
                  "joint pain", "clicky", "mouse", "laptop", "phone", "remote", "heater",
                  "clicking noise bad", "click noise bad"),
           bias=3))
