import re

from .lookup import entry, the_appliance_swallows_the_name

_COST = ("how much", "how many pounds", "cost", "costs", "costing", "charge", "charges",
         "charging", "price", "prices", "priced", "quote", "quotes", "quoted", "fee", "fees",
         "hourly rate", "day rate", "call out fee", "callout", "what should i pay", "worth paying",
         "is it worth", "expensive", "cheaper", "afford", "budget for", "typical price",
         "going rate", "fair price", "rip off", "ripped off", "overcharged", "how much is",
         "is it free", "free on the nhs", "free on the health service", "do i pay",
         "free in england", "free in scotland", "free in wales", "free in northern ireland",
         "are they free", "are prescriptions free", "is it free in", "free of charge",
         "free for children", "free for pensioners", "free for over 60",
         "do i have to pay", "nhs free", "does the nhs pay", "covered by the nhs",
         "too much", "too expensive", "too dear", "about right", "sound right", "sounds right",
         "reasonable", "over the odds", "is that fair", "is this fair", "fair amount",
         "is that about right",
         "worth it", "why am i paying", "am i paying", "paying for my", "do i have to pay for",
         "get free", "get them free")

_A_VISIT_FEE = ("just to come out", "just to come round", "just to come over",
                "just to come and look", "just to look", "just to have a look",
                "just to turn up", "just to show up", "just to pop round", "just to call out")
_VISIT_FEE_JOBS = frozenset((
    "plumber", "electrician", "boiler-service", "washing-machine-repair", "drains", "locksmith",
    "handyman", "decorator", "gardener", "oven-clean", "carpet-clean", "gutter-clean", "vet",
    "dentist", "eye-test", "smoke-alarm", "dog-groomer"))

_PRICE = ("how much", "how many pounds", "cost", "costs", "costing", "charge", "charges",
          "price", "prices", "quote", "quotes", "what should i pay", "going rate", "call out",
          "callout", "hourly rate", "pay for")

_DIY = ("how do i", "how can i", "myself", "my own", "diy", "step by step",
        "tip", "tips", "tipping", "gratuity", "tipped")

_HOW_TO = re.compile(r"\bhow\s+to\b|\bhow\s+2\b")


def _not_a_steps_ask(understood):
    text = understood.get("clean") or understood.get("text") or ""
    return not _HOW_TO.search(str(text).lower())


_STEPS_ASK = re.compile(
    r"\b(how do i|how can i|how to|how 2|what do i need|what do you need|what do i take|"
    r"do i need|can i renew|can i apply|can i do it|where do i|when should i|what happens if)\b")
_PRICE_ASK = re.compile(
    r"\b(how much|how many pounds|cost|costs|costing|price|prices|priced|fee|fees|charge|"
    r"charges|pays|pay|paid|pence|cheapest|expensive)\b")


def _a_steps_ask_with_no_price(understood):
    text = str(understood.get("clean") or understood.get("text") or "").lower()
    return bool(_STEPS_ASK.search(text)) and not bool(_PRICE_ASK.search(text))


APPLIANCES = ("washing machine", "dishwasher", "tumble dryer", "dryer", "oven", "fridge freezer",
              "fridge", "freezer")


def _repair_phrases(name):
    article = "an" if name[0] in "aeiou" else "a"
    return tuple(f"{verb} {article} {name}" for verb in ("fix", "repair")) + (
        f"fix the {name}", f"repair the {name}", f"fix my {name}", f"repair my {name}",
        f"repair on the {name}", f"fix on the {name}", f"repair on a {name}",
        f"{name} repair", f"{name} repairs", f"{name} fix",
        f"get the {name} fixed", f"get my {name} fixed", f"get {article} {name} fixed",
        f"get the {name} repaired", f"get my {name} repaired",
        f"have the {name} fixed", f"have my {name} fixed", f"have {article} {name} fixed",
        f"have the {name} repaired", f"have my {name} repaired",
        f"have {article} {name} repaired",
        f"{name} fixed", f"{name} repaired",
        f"{name} looked at", f"look at the {name}", f"look at my {name}")


APPLIANCE_REPAIRS = tuple(phrase for name in APPLIANCES for phrase in _repair_phrases(name))

_SMALL_THING = ("tap", "taps", "mirror", "mirrors", "tile", "tiles", "tiling", "retile",
                "retiling", "grout", "sealant", "silicone", "shower head", "toilet seat",
                "cistern", "radiator", "extractor", "fan", "lino", "vinyl", "flooring",
                "splashback", "cupboard", "cupboards", "shelves", "worktop", "worktops",
                "panel", "panels", "clean", "cleaning", "deep clean", "cleaner", "cleaners")

_PAINT_ROOMS = ("bedroom", "bedrooms", "hallway", "hall", "landing", "lounge", "living room",
                "front room", "dining room", "kitchen", "bathroom", "nursery", "box room",
                "spare room", "study", "office", "stairs", "stairwell", "ceiling", "flat",
                "whole house", "house inside", "one room", "room")

_BIGGER_JOB = ("extension", "extensions", "kitchen extension", "bathroom extension", "loft",
               "loft conversion", "conservatory", "or move", "cheaper to move", "rather than move",
               "instead of moving", "moving house", "or sell", "sell up", "or buying",
               "worth doing")

def _boiler_service_answer(memory, reading):
    asks = set(reading.get("asks") or ())
    if "how_often" not in asks and asks & {"yesno", "recommend"}:
        return ("Yes, once a year: a boiler service is usually £60 to £120 depending on where you "
                "are, it keeps the warranty valid, catches a failing part before it strands you in "
                "winter, and landlords are legally required to have one. Book it in late summer, "
                "when engineers are quiet and the price is lower.")
    return ("A boiler service is usually £60 to £120 once a year, and a gas safety check on top is "
            "£50 to £90 if you rent the place out. It is a check, not a repair: the engineer "
            "cleans and tests the boiler and tells you what is wearing out, so it is the cheap way "
            "to avoid a winter breakdown. Ask whether the price includes the gas safety certificate "
            "if you need one.")


JOBS = {
    "plumber": {
        "names": ("plumber", "plumbers", "plumbing"),
        "thing": "a plumber",
        "reply": "Most plumbers charge £50 to £100 to turn up and then £40 to £80 an hour, so a "
                 "small job like a dripping tap or a leaking joint comes to £100 to £200. An "
                 "emergency at night or at a weekend roughly doubles it, and parts are on top. "
                 "Ask whether the call-out includes the first hour before you book, and get a "
                 "second quote for anything over a few hundred pounds.",
    },
    "electrician": {
        "names": ("electrician", "electricians", "sparky"),
        "thing": "an electrician",
        "reply": "An electrician is usually £40 to £70 an hour, with a call-out of £50 to £100 "
                 "that often covers the first hour. A new socket or a light fitting is a one-hour "
                 "job; a fuse board or any work in a bathroom or kitchen needs a certificate, "
                 "which adds £50 to £150. Ask for the certificate in the quote, because a "
                 "landlord or a buyer will want it.",
    },
    "boiler": {
        "names": ("boiler", "boilers", "combi boiler"),
        "thing": "a new boiler",
        "reply": "A new combi boiler fitted in place of an old one is usually £1,800 to £3,000, and "
                 "£3,000 to £4,500 if the pipework has to change or a tank comes out. A service is "
                 "£60 to £120 once a year. Get two or three quotes on the same boiler model, "
                 "because the price is mostly the fitter's day and a cheap boiler with a poor "
                 "warranty costs more later; ask how long the warranty runs and who honours it.",
    },
    "heat-pump": {
        "names": ("heat pump", "heat pumps", "air source heat pump", "air source",
                  "ground source heat pump", "heat pump cost", "heat pump price"),
        "thing": "a heat pump",
        "bias": 2,
        "avoid": ("to run", "cost to run", "costs to run", "run a heat pump", "running cost",
                  "running costs", "per year", "a year", "per month", "a month", "electricity",
                  "units of", "how much electricity",
                  "cheaper than", "than a boiler", "than gas", "compare", "compared", "vs",
                  "versus", "better than", "instead of a boiler",
                  "worth", "worthwhile", "should i", "should we", "would you recommend",
                  "recommend", "any point", "a good idea", "good idea", "sensible"),
        "reply": "An air source heat pump is usually £10,000 to £14,000 fitted, and the Boiler "
                 "Upgrade Scheme takes £7,500 off, so most people pay £2,500 to £6,500. Running "
                 "it costs less than gas for the same heat if the house is insulated and the "
                 "radiators are big enough for the lower flow temperature, so a draughty house "
                 "with small radiators eats the saving. Ask for two quotes, each with a heat loss "
                 "survey of your own house, because that survey is what the price turns on.",
    },
    "heat-pump-running": {
        "names": ("heat pump", "heat pumps", "air source heat pump", "ground source heat pump"),
        "thing": "a heat pump",
        "bias": 3,
        "ask": ("run", "runs", "running", "to run", "per year", "a year", "a month",
                "electricity", "kwh", "kilowatt", "units", "cost to run", "running cost"),
        "avoid": ("worth", "worthwhile", "should i", "should we", "recommend", "any point",
                  "a good idea", "good idea", "sensible"),
        "reply": "A well-fitted heat pump uses about a third of the electricity of panel heaters "
                 "for the same warmth: a typical three-bedroom house runs one for roughly £700 to "
                 "£1,100 a year at today's electricity price, against £900 to £1,200 on gas, and "
                 "the gap widens as gas gets dearer. It needs radiators big enough for a 45 to "
                 "55C flow temperature and a well-insulated house to hit that; in a draughty house "
                 "with small radiators the running cost climbs above gas. Ask the installer for "
                 "the figure off their own room-by-room design, not the brochure's.",
    },
    "wood-burner": {
        "names": ("wood burner", "woodburner", "wood burning stove", "woodburning stove",
                  "log burner", "logburner", "multi fuel stove", "multifuel stove",
                  "wood stove", "log stove", "stove", "stoves"),
        "thing": "a wood burner",
        "bias": 2,
        "avoid": ("camping", "tent", "gas", "cooker", "cookers", "oven", "hob", "ring",
                  "plate", "kitchen", "backpacking", "trangia", "calor", "bottle",
                  "worth", "worthwhile", "should i", "should we", "recommend", "any point",
                  "a good idea", "good idea", "sensible"),
        "reply": "A wood burning stove is usually £400 to £1,500 for the stove itself and £1,500 "
                 "to £3,000 to line the chimney and fit it, so budget £2,000 to £4,500 done "
                 "properly. It has to be fitted by a Hetas-registered installer, or signed off by "
                 "building control, and only an Ecodesign stove can be sold new now. Ask whether "
                 "the chimney is yours to use and whether the house is in a smoke control area "
                 "before you buy: both change what you can fit.",
    },
    "boiler-service": {
        "names": ("boiler service", "boiler servicing", "service the boiler",
                  "service my boiler", "service a boiler", "service our boiler",
                  "annual boiler service", "gas safety check", "boiler serviced",
                  "get the boiler serviced", "get my boiler serviced",
                  "get a boiler service", "boiler safety check"),
        "thing": "a boiler service",
        "bias": 2,
        "reply": _boiler_service_answer,
    },
    "skip": {
        "names": ("a skip", "skip hire", "hire a skip", "skip permit", "skip bag",
                  "a builder's skip", "skip", "skips", "skip cost", "skip price",
                  "skip prices", "skip size", "skip sizes", "size skip", "yard skip"),
        "avoid": ("gears", "gear", "chain", "chains", "cassette", "derailleur", "sprocket",
                  "pedal", "pedals", "bike", "bikes", "bicycle", "cycl", "breakfast", "brunch",
                  "meal", "meals", "lunch", "dinner", "tea", "homework", "class", "school",
                  "serviced", "servicing", "tune up", "tuneup", "overhaul", "mechanic"),
        "thing": "a skip",
        "reply": "A builder's skip is usually £150 to £300 for a week, and a permit on a public "
                 "road adds £30 to £60. Soil, rubble and hardcore cost more than household "
                 "rubbish because of the weight, and a mattress or a fridge often cannot go in at "
                 "all without a surcharge. Ask what the price includes and what happens if it is "
                 "overfull, since a second skip is the usual surprise.",
    },
    "removals": {
        "names": ("removal firm", "removals", "removal company", "removal van", "removal men",
                  "moving firm"),
        "thing": "removals",
        "reply": "Two movers and a van are usually £400 to £700 for a local day, and a one-bedroom "
                 "flat moved locally comes in around £300 to £500. A three-bedroom house is "
                 "£800 to £1,500, more if there are stairs or a long carry, and packing as well "
                 "roughly doubles it. Ask whether the quote is fixed or hourly, whether insurance "
                 "covers breakage, and whether the price changes if the move runs into a second "
                 "day.",
    },
    "van-hire": {
        "names": ("van hire", "hire a van"),
        "thing": "hiring a van",
        "reply": "A transit-sized van is usually £40 to £80 a day, plus a deposit of £150 to £300 "
                 "held against damage. Mileage and a young-driver surcharge are the two things "
                 "that turn a cheap ad into an expensive day, and the excess on the insurance is "
                 "often £1,000 unless you pay extra. Ask for the total with mileage and the excess "
                 "before you book, and photograph the van all round before you drive it away.",
    },
    "cleaner": {
        "names": ("cleaner", "cleaners", "cleaner charge", "housekeeper", "domestic cleaner"),
        "avoid": ("steam cleaner", "steam cleaners", "steam mop", "steam mops",
                  "vacuum cleaner", "vacuum cleaners", "hoover", "oven cleaner",
                  "drain cleaner", "pressure washer", "jet washer", "pool cleaner",
                  "robot cleaner", "dry cleaner", "dry cleaners",
                  "window", "windows", "window cleaner", "window cleaners",
                  "carpet cleaner", "carpet cleaners"),
        "thing": "a cleaner",
        "reply": "A cleaner is usually £12 to £18 an hour, so a two-hour weekly visit is £25 to "
                 "£40, and a one-off deep clean of a three-bedroom house is £60 to £120. An "
                 "agency costs more than someone working for themselves but covers insurance, tax "
                 "and holidays. Ask what is included (inside the oven and the fridge usually are "
                 "not), and whether you supply the products.",
    },
    "decorator": {
        "names": ("decorator", "decorators", "painter", "painters", "painting and decorating",
                  "paint a room", "paint the room", "paint my room", "paint a wall",
                  "paint the walls", "paint my walls", "painting a room", "decorate a room",
                  "decorating a room", "get a room painted", "have a room painted",
                  "hang wallpaper", "wallpapering", "wallpaper a room", "wallpapering a room",
                  "wallpaper one room", "wallpapering one room", "decorate the flat",
                  "get the room decorated", "have a room decorated", "have the room decorated",
                  "paint the flat", "decorating a flat", "painting the house inside")
                  + tuple("paint a " + room for room in _PAINT_ROOMS)
                  + tuple("paint the " + room for room in _PAINT_ROOMS)
                  + tuple("decorate a " + room for room in _PAINT_ROOMS)
                  + tuple("decorate the " + room for room in _PAINT_ROOMS)
                  + tuple("wallpaper a " + room for room in _PAINT_ROOMS)
                  + tuple("get a " + room + " painted" for room in _PAINT_ROOMS)
                  + tuple("get the " + room + " painted" for room in _PAINT_ROOMS)
                  + tuple("get a " + room + " decorated" for room in _PAINT_ROOMS),
        "avoid": ("do i need", "will i need", "how many rolls", "rolls of wallpaper",
                  "how much wallpaper", "how much paint do i need", "how much paint will i need",
                  "how much wall", "coverage", "square metres of", "per square metre"),
        "thing": "a decorator",
        "reply": "A decorator is usually £150 to £250 a room for walls and ceiling, or £20 to £40 "
                 "an hour, with paint and materials on top. Emulsion on sound walls is the cheap "
                 "end; filling, lining paper, gloss woodwork and high ceilings push it up. Ask "
                 "whether the price includes the paint, how many coats, and who moves the "
                 "furniture.",
    },
    "handyman": {
        "names": ("handyman", "handymen", "odd job man", "odd jobs"),
        "thing": "a handyman",
        "reply": "A handyman is usually £25 to £45 an hour with a minimum of one or two hours, so "
                 "a morning of small jobs is £100 to £150. Jobs that need a certificate - gas, "
                 "electrics in a bathroom, anything structural - are not handyman work whatever "
                 "the advert says. Ask for the hourly rate, the minimum charge and whether they "
                 "take the rubbish away.",
    },
    "carpenter": {
        "names": ("carpenter", "carpenters", "joiner", "joiners", "carpentry", "woodwork",
                  "cabinet maker", "cabinetmaker", "fitted wardrobes", "fitted furniture"),
        "thing": "a carpenter",
        "reply": "A carpenter is usually £150 to £250 a day, or £30 to £50 an hour for small jobs "
                 "with a one-hour minimum, and a joiner hanging an internal door is £60 to £120 "
                 "each. Fitted wardrobes and shelving are priced as a whole: £1,000 to £3,000 for "
                 "a run of built-in wardrobes with the materials in. Ask for the day rate, whether "
                 "the price is fixed or an estimate, and get the material allowance in writing.",
    },
    "plasterer": {
        "names": ("plasterer", "plasterers", "plastering", "skim a wall", "skim a ceiling",
                  "skimming", "plasterboard"),
        "thing": "a plasterer",
        "reply": "A plasterer is usually £150 to £250 a day, or £15 to £25 a square metre for "
                 "skimming: a whole room's walls and ceiling is £300 to £600, and patching a "
                 "ceiling after a leak is £80 to £150. Boarding over old plaster adds £200 to "
                 "£400 a room. Ask whether the price includes the boards and the finishing coat, "
                 "and how long it takes to dry before paint.",
    },
    "tiler": {
        "names": ("tiler", "tilers", "tiling", "tile a bathroom", "tile a kitchen", "retile",
                  "re-tile"),
        "thing": "a tiler",
        "reply": "A tiler is usually £150 to £250 a day, or £25 to £45 a square metre for labour: "
                 "a small bathroom's walls and floor is £500 to £900, and a kitchen splashback "
                 "£150 to £300. Tiles themselves are £15 to £60 a square metre on top. Ask "
                 "whether the price includes taking the old tiles off, the adhesive and the "
                 "grouting, because that is where two quotes differ most.",
    },
    "gas-engineer": {
        "names": ("gas engineer", "gas safe", "gas safe engineer", "heating engineer",
                  "boiler engineer", "boiler service", "service the boiler", "boiler repair",
                  "gas boiler", "gas fire", "gas hob fitting"),
        "thing": "a Gas Safe engineer",
        "reply": "A boiler service is £60 to £120, and a repair is £80 to £250 including the "
                 "common parts, with the first hour often £50 to £90. Out of hours or a "
                 "breakdown in winter costs £100 to £150 before parts. Check the engineer is on "
                 "the Gas Safe register, and ask whether the repair is a fixed price before they "
                 "start.",
    },
    "glazier": {
        "names": ("glazier", "glaziers", "double glazing repair", "broken window", "new window "
                  "pane", "replace a window pane", "sealed unit", "window glass", "cracked window"),
        "thing": "a glazier",
        "reply": "A single pane of ordinary glass is £60 to £120 fitted, and a sealed double-glazed "
                 "unit is £100 to £250, with a big or toughened one £250 to £500. A broken window "
                 "boarded up the same day is £100 to £200. Ask whether the frame is sound, because "
                 "a rotten frame means a whole new window at £400 to £1,000, and check whether "
                 "your home insurance covers the glass.",
    },
    "window-cleaner": {
        "names": ("window cleaner", "window cleaners", "clean the windows", "window cleaning",
                  "fascia cleaning"),
        "thing": "a window cleaner",
        "bias": 2,
        "reply": "A window cleaner is usually £10 to £25 for a small house and £25 to £40 for a "
                 "larger one, inside usually not included, and a four-weekly round is cheaper "
                 "than a one-off. Gutter clearing is £60 to £150 for a house, and fascia cleaning "
                 "£100 to £250. Ask whether they use pure water and a pole or ladders, and "
                 "whether the price covers the frames and the sills.",
    },
    "chimney-sweep": {
        "names": ("chimney sweep", "chimney sweeps", "sweep the chimney", "sweeping the chimney",
                  "flue sweep", "sweep the flue"),
        "thing": "a chimney sweep",
        "reply": "A chimney sweep is usually £50 to £90 for an ordinary chimney, and £90 to £150 "
                 "if it is lined, thatched or needs a camera. A wood burner wants sweeping once a "
                 "year before the season and twice if it is your main heat, and a gas appliance "
                 "needs a Gas Safe service rather than a sweep. Ask for a certificate, because "
                 "your insurer may ask for one after a chimney fire.",
    },
    "surveyor": {
        "names": ("surveyor", "surveyors", "survey", "surveys", "house survey", "building survey",
                  "homebuyer report", "structural survey", "condition survey", "valuation"),
        "thing": "a surveyor",
        "bias": 2,
        "reply": "A survey is £400 to £700 for a HomeBuyer report and £600 to £1,200 for a full "
                 "building survey, on a typical house; a flat is at the lower end and a big or old "
                 "house at the top. The lender's valuation is not a survey and only tells the "
                 "lender the house is worth the loan. Get the survey before you exchange, and "
                 "ring the surveyor afterwards to ask what actually matters.",
        "avoid": ("worth it", "is it worth", "worth", "do i need", "should i", "instead of",
                  "which level", "what level", "came back", "come back", "found", "flagged",
                  "says", "damp", "the survey said", "had the survey", "got the survey"),
    },
    "pest-control": {
        "names": ("pest control", "pest controller", "pest control company", "exterminator",
                  "rat catcher", "get rid of rats", "wasp nest removal", "bed bug treatment",
                  "mouse treatment"),
        "thing": "pest control",
        "reply": "A pest controller is usually £80 to £150 for a wasp nest and £100 to £250 for "
                 "rats or mice, which usually covers two visits and the bait. Bed bugs are the "
                 "expensive one at £300 to £800 for a flat, sometimes with a second treatment. "
                 "Your council may do rats and mice cheaper, so ring them first, and ask whether "
                 "the price includes the follow-up visit.",
    },
    "architect": {
        "names": ("architect", "architects", "architectural drawings", "planning drawings",
                  "building regs drawings", "structural engineer"),
        "thing": "an architect",
        "reply": "Drawings for an extension are usually £1,000 to £2,500, and a full service is 8 "
                 "to 15% of the build cost, so a £60,000 extension is £5,000 to £9,000 in fees. A "
                 "structural engineer's calculations are £400 to £1,000 on top when a wall is "
                 "coming out. Ask what the fee covers - planning, building regs, and site visits "
                 "during the build are separate jobs.",
    },
    "gardener": {
        "names": ("gardener", "gardeners", "landscaper", "lawn care"),
        "thing": "a gardener",
        "reply": "A gardener is usually £20 to £35 an hour, and a fortnightly cut of a small lawn "
                 "is £30 to £50 a visit. One-off clearances, hedges and anything with a skip are "
                 "priced by the job instead. Ask whether green waste is taken away or left for "
                 "you, because that is often the difference between two quotes.",
    },
    "washing-machine-repair": {
        "names": ("washing machine repair", "tumble dryer repair", "dishwasher repair",
                  "appliance repair", "get the washing machine fixed") + APPLIANCE_REPAIRS,
        "thing": "repairing an appliance",
        "ask": _PRICE,
        "reply": "A repair is usually £60 to £120 including the first hour, with parts on top, so "
                 "expect £100 to £200 for a common fault. On a machine more than eight years old, "
                 "compare the quote with a new one: a £150 repair on a ten-year-old machine is "
                 "often money down. Ask for the call-out charge and whether it comes off the "
                 "repair if you go ahead.",
    },
    "drains": {
        "names": ("drain", "drains", "blocked drain", "drain unblocking", "sewer",
                  "drain company", "drain companies", "drainage company", "drains company",
                  "sewer company", "drain clearing", "clear a drain", "clear the drain"),
        "avoid": ("battery", "batteries", "phone", "iphone", "ipad", "android", "laptop",
                  "computer", "tablet", "charger", "charge it", "charge my",
                  "charge the phone", "charge overnight", "battery drain",
                  "draining fast", "drains fast", "drains so fast"),
        "thing": "clearing a drain",
        "reply": "Clearing a blocked drain is usually £80 to £200 with rods or a pressure jet, and "
                 "a camera survey to find the cause is £150 to £300 on top. Roots and collapsed "
                 "pipework are the expensive cases. Ask whether the price includes the survey and "
                 "the waste removal, and if the blockage is in the pipe the water company owns, "
                 "ring them first because they clear it free.",
    },
    "locksmith": {
        "names": ("locksmith", "locksmiths", "lock change", "locked out"),
        "thing": "a locksmith",
        "reply": "A locksmith is usually £60 to £120 to let you back in during the day, and £120 to "
                 "£250 at night or at a weekend, with a new lock £80 to £150 fitted. The cheap "
                 "quote on a van is often the call-out only, with the rest added on the doorstep. "
                 "Ask for the total price on the phone, before they come out, and pay by card so "
                 "there is a record.",
    },
    "storage": {
        "names": ("storage unit", "self storage", "storage"),
        "avoid": ("phone", "iphone", "ipad", "android", "laptop", "computer", "mac", "macbook",
                  "pc", "tablet", "disk", "hard drive", "hard disk", "gb", "mb", "memory",
                  "space left", "storage left", "left on my", "storage do i have",
                  "ssd", "hdd", "hard drive", "hard disk", "disk space", "photos on",
                  "pictures", "512gb", "256gb", "128gb", "500gb", "1tb", "2tb", "ps5",
                  "console", "steam", "laptop", "tablet", "ipad", "macbook",
                  "cloud", "icloud", "the cloud", "google drive", "google one", "onedrive",
                  "dropbox", "backup", "back up", "backed up", "photos", "subscription",
                  "paying for"),
        "thing": "a storage unit",
        "reply": "A storage unit is usually £60 to £150 a month for 25 to 50 square feet, which "
                 "holds a one-bedroom flat, and the first month is often half price. The price "
                 "creeps up after the intro offer, and insurance is either included or pushed at "
                 "you on the day. Ask what the rate is in month four, the notice period, and "
                 "whether you need your own padlock.",
    },
    "sofa": {
        "names": ("sofa", "sofas", "couch", "settee", "armchair"),
        "avoid": ("clean", "cleaning", "cleaned", "wash", "washing", "stain"),
        "thing": "a sofa",
        "reply": "A mid-range three-seater is usually £600 to £1,200, with £300 to £500 at the "
                 "cheap end and £1,500 upwards for a good frame and fabric. The frame, the filling "
                 "and the fabric are what the money buys, and delivery, assembly and a stain "
                 "guard are usually extra. Sit on it in the shop for ten minutes and ask what the "
                 "frame is made of and how long the cover is guaranteed.",
    },
    "mattress": {
        "names": ("mattress", "mattresses"),
        "thing": "a mattress",
        "reply": "A decent double mattress is usually £300 to £700, with £150 to £250 at the cheap "
                 "end and £900 upwards for pocket springs or a good foam. Firmness matters more "
                 "than price, and a mattress that is too soft is the common mistake. Ask about the "
                 "trial period and whether the guarantee covers sagging, and take the old one away "
                 "as part of the deal if you can.",
        "avoid": ("clean", "cleaning", "cleaned", "stain", "stains", "smell", "smells",
                  "wash", "washing", "vacuum", "hoover", "water"),
    },
    "driving-lessons": {
        "names": ("driving lesson", "driving lessons", "driving instructor", "learner driver"),
        "thing": "driving lessons",
        "reply": "Lessons are usually £30 to £45 an hour, and a block of ten is often £270 to £400. "
                 "Most people need 40 to 50 hours of lessons plus practice, so the total lands "
                 "around £1,500 to £2,000 with the tests. Ask whether the car is used for the test "
                 "and what that costs, and whether the instructor is on the official register.",
    },
    "vet": {
        "names": ("vet", "vets", "vet visit", "veterinary", "vet bill"),
        "thing": "a vet visit",
        "reply": "A consultation is usually £40 to £70, and anything done in it - a jab, a blood "
                 "test, an x-ray - is on top, so a first visit often lands at £80 to £150. Out of "
                 "hours is £150 or more before treatment. Ask for the estimate in writing before "
                 "you agree to treatment, and ask what insurance would have covered, because the "
                 "cost of a dog or cat is mostly these bills.",
    },
    "dentist": {
        "names": ("dentist", "dentists", "dental", "check up", "checkup"),
        "thing": "a dentist",
        "avoid": ("free", "is it free", "do i pay", "do i have to pay", "covered", "qualify",
                  "exempt"),
        "reply": "A private check-up is usually £40 to £80, with a hygienist visit £40 to £70 and a "
                 "filling £80 to £200. On the NHS in England you pay a fixed band charge set "
                 "nationally, which covers the check-up and any work in that band, and Wales, "
                 "Scotland and Northern Ireland have their own charges. Ask which band your "
                 "treatment falls in before you agree to it.",
    },
    "glasses": {
        "names": ("glasses", "spectacles", "eyeglasses", "eye glasses"),
        "avoid": ("eye test", "eye tests", "contact lens", "contact lenses", "optician",
                  "glass of", "glasses of",
                  "water", "milk", "juice", "squash", "cola", "beer", "wine", "drink",
                  "drinks"),
        "thing": "glasses",
        "reply": "A pair of glasses is usually £100 to £300 with standard lenses, and varifocals or "
                 "thin lenses push it to £300 to £500. The frame is where the money goes, and the "
                 "two-for-one offers usually mean two pairs of a cheap lens. Ask what the lenses "
                 "cost on their own, and ask for your prescription and pupillary distance so you "
                 "can compare anywhere.",
    },
    "eye-test": {
        "names": ("eye test", "eye tests", "sight test", "optician"),
        "thing": "an eye test",
        "bias": 2,
        "reply": "An eye test is usually £25 to £45 on the high street, and free on the NHS if you "
                 "qualify - over 60, diabetic, glaucoma in the family, or on certain benefits. A "
                 "retina photo or a scan is often offered as an extra £10 to £25. Ask what the "
                 "test includes and whether the prescription is yours to take away.",
    },
    "contact-lenses": {
        "names": ("contact lenses", "contact lens", "daily lenses", "monthly lenses"),
        "thing": "contact lenses",
        "bias": 2,
        "reply": "Contact lenses are usually £15 to £35 a month on a supply plan, and the "
                 "fitting appointment at the start is £30 to £60. Daily disposables cost more per "
                 "day than monthlies and need no cleaning, and the aftercare visit is often "
                 "included in the plan. Ask what the plan includes, how often the checks are, and "
                 "whether you can stop whenever you like.",
    },
    "oven-clean": {
        "names": ("oven clean", "oven cleaning", "clean the oven", "clean my oven",
                  "extractor clean"),
        "thing": "an oven clean",
        "reply": "An oven clean by a professional is usually £50 to £90, and the hob and the "
                 "extractor are often £15 to £30 extra each. It takes an hour or two and the "
                 "difference is mostly how long since it was last done. Ask whether the price "
                 "includes the shelves and the door glass, and whether they use a dip tank for the "
                 "racks - the good ones do.",
    },
    "carpet-clean": {
        "names": ("carpet clean", "carpet cleaning", "clean a carpet", "clean my carpets",
                  "clean the carpets", "clean the carpet", "rug clean", "sofa clean",
                  "clean a sofa", "clean my sofa", "sofa cleaning", "clean the sofa",
                  "clean my couch"),
        "thing": "a carpet clean",
        "reply": "A carpet clean is usually £25 to £40 a room, or £100 to £200 for a whole flat, "
                 "with stairs and stubborn stains priced separately. A sofa or a rug is £40 to "
                 "£100. Ask whether the price includes the stairs and a stain treatment, and "
                 "whether they move the furniture, because two quotes that look different usually "
                 "differ on those two things.",
    },
    "kitchen": {
        "names": ("new kitchen", "kitchen fitter", "kitchen units", "fitted kitchen",
                  "kitchen", "kitchen refit", "refit a kitchen", "redo the kitchen",
                  "kitchen refurb", "kitchen renovation"),
        "thing": "a new kitchen",
        "avoid": _SMALL_THING + _BIGGER_JOB,
        "reply": "A mid-range kitchen is usually £5,000 to £15,000 fitted, and £20,000 or more with "
                 "appliances, worktops and building work. Roughly a third units, a third worktop "
                 "and appliances, a third fitting. Get three quotes on the same written scope and "
                 "ask what happens if the walls are not square, which is where the price moves.",
    },
    "worktop": {
        "names": ("worktop", "worktops", "kitchen worktop", "kitchen worktops", "countertop",
                  "counter top", "countertops", "counter", "counters", "butcher block"),
        "thing": "a worktop",
        "avoid": ("clean", "cleaning", "wipe", "disinfect", "oil", "oiling", "stain",
                  "stains", "scratch", "scratches", "scratched", "burn", "burnt", "chip",
                  "chips", "chipped", "repair", "replace myself", "how do i fit",
                  "how to fit", "fit it myself", "seal", "sealing", "shine", "polish"),
        "reply": "A laminate worktop is usually £60 to £120 a metre, solid wood £150 to £400, and "
                 "quartz, granite or sintered stone £250 to £600. Fitting is £200 to £500 for a "
                 "straight run, and more where it has to be cut round a sink, a hob or a corner. "
                 "Ask whether the price is per metre or for the length you need, whether cutting "
                 "and sealing the edges is included, and have it templated on site rather than "
                 "from your own measurements.",
    },
    "smoke-alarm": {
        "names": ("smoke alarm", "smoke alarms", "smoke detector", "smoke detectors"),
        "thing": "a smoke alarm",
        "avoid": ("where", "place", "placing", "put", "position", "how many", "install",
                  "installing", "fitted", "beep", "beeps", "beeping", "chirp", "chirping",
                  "false alarm", "goes off", "battery", "batteries", "test", "testing",
                  "hard of hearing", "landlord", "wired", "wiring", "heat detector"),
        "reply": "A battery smoke alarm is usually £10 to £25, and £30 or so with a sealed "
                 "ten-year battery. A mains one with a backup battery is £25 to £40 plus an "
                 "electrician, and three linked so they all sound together is £60 to £120. Test "
                 "it monthly and change the battery once a year even if it has not chirped, and "
                 "ask your landlord about the mains one in a rented flat, since fitting and "
                 "checking it is their job rather than yours.",
    },
    "bathroom": {
        "names": ("new bathroom", "bathroom fitter", "bathroom suite", "bathroom",
                  "bathroom refit", "refit a bathroom", "redo the bathroom", "bathroom refurb",
                  "bathroom renovation", "shower room"),
        "thing": "a new bathroom",
        "avoid": _SMALL_THING + _BIGGER_JOB,
        "reply": "A new bathroom is usually £3,000 to £7,000 fitted, and £8,000 to £12,000 with the "
                 "bath moved, the walls tiled and the plumbing changed. Tiling and moving the "
                 "toilet or the bath account for most of the difference. Ask for the scope written "
                 "down, including who makes good the walls, and agree what happens if the floor "
                 "under the old suite is rotten.",
    },
    "gutter-clean": {
        "names": ("gutter", "gutters", "gutter clean", "gutter cleaning"),
        "thing": "cleaning gutters",
        "reply": "Gutter clearing is usually £60 to £150 for a house, more for three storeys or a "
                 "lot of access problems. A repair or a new run of gutter is a separate job, "
                 "priced by the metre. Ask whether the price includes the downpipes and a check "
                 "for leaks, and whether they clear up what comes out.",
    },
    "haircut": {
        "names": ("haircut", "hair cut", "barber", "hairdresser", "salon"),
        "avoid": ("tip", "tips", "tipping", "gratuity",
                  "to charge", "charge for", "should i charge", "what to charge", "my prices",
                  "price list", "self employed", "self-employed", "my rate", "my rates",
                  "charge per"),
        "thing": "a haircut",
        "reply": "A cut is usually £15 to £35 in a salon and £10 to £20 at a barber, with colour "
                 "from £60 to £150 depending on how much work it is. A senior stylist costs more "
                 "than a junior, and a dry cut is often cheaper. Ask for the price of the cut and "
                 "the blow dry separately, because the blow dry is the surprise on the bill.",
    },
    "dog-groomer": {
        "names": ("dog groomer", "groomer", "groomers", "dog grooming", "groom my dog",
                  "groom a dog", "groom the dog", "grooming my dog", "grooming a dog", "dog groom",
                  "get my dog groomed", "get the dog groomed", "dog bathed", "dog clipped",
                  "dog trimmed", "dog hand stripped", "grooming cost", "dog grooming cost",
                  "cost of grooming", "grooming for a dog"),
        "thing": "a dog groomer",
        "reply": "A dog groomer is usually £30 to £60 depending on the size and coat, with a "
                 "hand-strip or a matted coat costing more. Ask what happens if your dog is "
                 "matted, because some charge by the hour to sort it out, and book four to six "
                 "weeks apart for a coat that keeps its shape.",
    },
    "neutering": {
        "names": ("neuter", "neutering", "neutered", "spay", "spaying", "spayed", "castrate",
                  "castrating", "castrated", "get my dog done", "get my cat done"),
        "thing": "neutering",
        "avoid": ("rabbit", "rabbits", "bunny", "bunnies", "hamster", "hamsters", "guinea pig",
                  "guinea pigs", "gerbil", "gerbils", "ferret", "ferrets",
                  "why", "worth it", "is it worth", "worth doing", "worth getting", "benefit",
                  "benefits", "point of", "point in", "pros", "pros and cons",
                  "cons and pros", "should i", "should we",
                  "good idea", "advice"),
        "reply": "Neutering is usually £150 to £300 for a dog and £60 to £120 for a cat, with a "
                 "bitch or a female cat at the top of the range because the operation is bigger. "
                 "Many charities run low-cost schemes, and the price usually includes pain relief "
                 "and a check-up. Ask whether the quote covers a follow-up visit, and most are "
                 "home the same day and back to normal within a few days.",
    },
    "dog-walker": {
        "names": ("dog walker", "dog walkers", "dog walking", "walk my dog", "walk the dog",
                  "dog walk", "someone to walk my dog", "dog walker cost", "walking cost",
                  "dog walking cost", "cost to walk a dog", "cost of a dog walker"),
        "avoid": ("groom", "groomer", "grooming", "clip", "trim", "bath"),
        "thing": "a dog walker",
        "reply": "A dog walker is usually £10 to £18 for a half-hour walk and £15 to £25 for an "
                 "hour, less per dog if they walk a group of four or five. Solo walks cost the "
                 "most, and a walker who is insured and does a first meet-and-greet at your house "
                 "is worth a pound or two more. Ask what happens on a wet day and how many dogs "
                 "go out at once.",
    },
    "builder": {
        "names": ("builder", "builders", "building work"),
        "thing": "a builder",
        "reply": "A builder is usually £150 to £300 a day for one person, or £200 to £350 for two, "
                 "and the big jobs are priced as a whole rather than by the day. Scaffolding, skips, "
                 "and any work that needs building regulations add to it, and a quote should name "
                 "all three if they apply. Ask for the price with the materials listed separately, "
                 "and ask what happens if the job runs over, because that is where the total moves.",
    },
    "fence": {
        "names": ("fence", "fencing", "garden fence", "fence panels"),
        "thing": "a fence",
        "avoid": ("pay half", "half the cost", "go halves", "split the cost", "who pays",
                  "who should pay", "who has to pay", "who owns", "whose fence",
                  "who is responsible", "responsible for", "my neighbour", "my neighbor",
                  "boundary", "deeds", "blew down", "blown down", "fell down", "repair",
                  "rotten", "rotted", "treat", "treating", "stain", "how tall", "how high",
                  "how deep", "deep enough", "depth", "in the ground", "into the ground",
                  "buried", "foot down", "feet down",
                  "do i need", "will i need", "post hole", "posthole", "postcrete",
                  "cement", "concrete", "ballast", "mortar", "bags of"),
        "reply": "A new closeboard fence is usually £50 to £90 a metre supplied and fitted, so 20 "
                 "metres of garden is £1,000 to £1,800. Concrete posts and a trellis or a gate push "
                 "it up, and taking the old one away is often extra. Ask whether the price includes "
                 "the posts and the removal of the old panels, and check the height limit before "
                 "you order.",
    },
    "patio": {
        "names": ("patio", "patios", "block paving", "driveway"),
        "thing": "a patio or driveway",
        "avoid": ("do i need", "will i need", "bags of", "tonnes of", "tons of", "cubic",
                  "how deep", "how thick",
                  "how much sand", "sand and cement", "how much cement", "how much ballast",
                  "patio base", "base for a patio", "base for the patio", "sand base",
                  "sub base", "sub-base", "type 1", "type one", "bulk bag",
                  "mortar", "mortar mix", "sharp sand", "building sand", "what mix",
                  "mix ratio", "what ratio"),
        "reply": "A patio is usually £60 to £120 a square metre laid, so a small 15 square metre "
                 "patio is £900 to £1,800, and block paving for a driveway £80 to £150 a square "
                 "metre. The base and the drainage are what separate a good job from a cheap one. "
                 "Ask what depth of sub-base they are laying, and whether the price includes the "
                 "skip and the sealing.",
    },
    "conservatory": {
        "names": ("conservatory", "conservatories", "orangery", "garden room"),
        "thing": "a conservatory",
        "reply": "A conservatory is usually £8,000 to £20,000 depending on size and whether it has "
                 "a solid roof, and an orangery with the same footprint is £20,000 to £40,000. A "
                 "solid roof and underfloor heating cost more but make the room usable all year. "
                 "Ask whether the price includes the foundations, the electrics and building "
                 "regulations sign-off, because those are the three that get left out of a quote.",
    },
    "loft-conversion": {
        "names": ("loft conversion", "loft", "attic conversion", "extension", "house extension"),
        "thing": "a loft conversion or extension",
        "avoid": ("someone out", "someone in", "get someone", "call someone", "an engineer",
                  "engineer", "callout", "call out", "boiler", "hot water", "repaired",
                  "repair it", "broken", "isnt working", "is not working",
                  "insulate", "insulation", "lagging", "mineral wool", "loft insulation",
                  "board out", "boarding"),
        "reply": "A loft conversion is usually £25,000 to £60,000 depending on the type, and a "
                 "single-storey extension £1,800 to £2,500 a square metre. A dormer and a "
                 "bathroom in the roof are the two things that move it most, and structural "
                 "engineers, party wall agreements and building regulations are all extra. Ask "
                 "whether the quote is fixed, what it excludes, and who is managing the "
                 "inspections.",
    },
    "roof": {
        "names": ("roof", "roofs", "roofing", "roofer", "roofers", "re-roof", "reroof",
                  "roof repair", "roof leak", "roof leaks", "leaking roof", "roof tiles",
                  "ridge tiles", "flat roof", "felt roof", "gutter", "gutters"),
        "thing": "a roof repair",
        "avoid": ("car", "cars", "van", "vans", "sunroof", "windscreen", "convertible",
                  "how do i", "how to", "myself", "clear the", "clearing", "unblock"),
        "reply": "A roofer is usually £200 to £300 a day, and the small jobs are priced whole: a "
                 "patch or a few slipped or broken tiles is £150 to £400, a flat roof on a garage "
                 "£1,500 to £3,000. A whole roof - a full re-roof or a new roof on a three-bed "
                 "semi - is £5,000 to £15,000, and scaffolding is £800 to £1,500 of that on its "
                 "own. Ask whether the quote includes the scaffolding, the disposal of the old "
                 "covering and a guarantee on the workmanship, and get three quotes on the same "
                 "written description of the job.",
    },
    "shed": {
        "names": ("shed", "summerhouse", "log cabin", "garden office"),
        "thing": "a shed",
        "reply": "A decent 6 by 8 foot shed is usually £400 to £900, and a garden office £3,000 to "
                 "£10,000. The base is the part people forget: a shed on grass or soil will never "
                 "sit square, so £100 to £200 on a paved or timber base is money well spent. Ask "
                 "whether the price includes the base, delivery and the treatment, and how thick "
                 "the timber is - thin boards are the cheap shed's secret.",
    },
    "passport": {
        "names": ("passport", "passports", "passport renewal", "new passport"),
        "thing": "a passport",
        "fence_how_to": True,
        "avoid": ("expires", "expiry", "six months", "6 months", "lost", "stolen", "damaged",
                  "travel with", "valid", "photo", "track"),
        "reply": "An adult passport is about £95 and a child's about £62, done on gov.uk, and "
                 "about £12 more each if you post the paper form instead. Do it on gov.uk "
                 "itself: the websites that charge £20 to fill the same form in for you are "
                 "charging for a service the site gives away, and a Post Office check-and-send "
                 "is about £16 on top for checking the photo. The fee goes up each April, and "
                 "it usually takes about three weeks, longer in the summer.",
    },
    "driving-licence": {
        "names": ("driving licence", "driving license", "provisional licence",
                  "provisional license", "photocard licence"),
        "thing": "a driving licence",
        "fence_how_to": True,
        "avoid": ("points", "banned", "revoked", "medical", "address", "change of address",
                  "lost", "stolen", "photo", "driving test", "lessons"),
        "reply": "A first provisional licence is £34 online, or £43 on the paper form, and "
                 "renewing the photocard is £14 online, or £17 on paper. The tests are separate: "
                 "about £23 for the theory and £62 for the practical, £75 at an evening or "
                 "weekend slot. Book all of it on gov.uk, and do the provisional first - you "
                 "cannot book a test without the number.",
    },
    "prescription": {
        "names": ("prescription", "prescriptions", "prescription charge",
                  "prescription charges", "nhs prescription",
                  "prepayment certificate", "prescription prepayment certificate",
                  "prescription prepayment", "prescription prepayment certificate", "ppc",
                  "prescriptions free", "are prescriptions free", "free prescriptions",
                  "prescription fee", "prescription fees", "prescription cost",
                  "prescription costs"),
        "thing": "a prescription",
        "diy": False,
        "shapes": ("prepayment", "prepayment certificate", "prescription prepayment",
                   "certificate", "how do i pay", "apply for", "ppc"),
        "avoid": ("tablet", "tablets", "pill", "pills", "antibiotic", "antibiotics", "dose",
                  "side effect", "side effects", "refill", "repeat prescription", "repeat",
                  "order my", "order a", "ordering", "how do i order", "how do i get a repeat",
                  "how to order", "how do i reorder", "reorder", "ran out", "run out",
                  "has run out", "pharmacy", "chemist", "my dog", "my cat", "the vet",
                  "for the dog", "for my dog", "for the cat", "for my cat", "puppy", "kitten"),
        "reply": "A prescription in England is £9.90 an item, and it is free in Scotland, Wales "
                 "and Northern Ireland. Check the exemptions before you pay, because a lot of "
                 "people pay and should not: under 16, 16 to 18 in full-time education, over 60, "
                 "pregnant or with a baby under 12 months, or on a benefit, and some long-term "
                 "conditions are exempt. If you pay for more than about 12 items a year, a "
                 "prepayment certificate is about £33 for three months or £115 for a year and "
                 "covers everything on it. Get one on the NHS website or at a pharmacy counter, "
                 "and it starts the day you pay, so buy it before the next item rather than "
                 "after it.",
    },
    "speeding-fine": {
        "names": ("speeding fine", "speeding ticket", "speeding penalty", "speeding offence",
                  "speeding"),
        "thing": "a speeding fine",
        "avoid": ("how do i", "how to", "appeal", "points on my licence", "insurance",
                  "caught", "camera", "notice"),
        "reply": "A speeding ticket is usually £100 and three points, or a speed awareness "
                 "course instead at about £100 if you were not far over the limit and have not "
                 "done one recently. If it goes to court the fine is means-based and up to "
                 "£1,000, or £2,500 on a motorway, and the points can be more. Pay within the 28 "
                 "days and tell your insurer: the policy nearly always asks, and finding out "
                 "later costs more than the fine.",
    },
    "tool-hire": {
        "names": ("hire a breaker", "breaker hire", "hire a kango", "kango hire",
                  "hire a drill", "drill hire", "hire an sds drill", "sds drill hire",
                  "hire a hammer drill", "hire a ladder", "ladder hire",
                  "hire a step ladder", "hire a scaffold tower", "scaffold tower hire",
                  "tower hire", "hire a floor sander", "floor sander hire", "hire a sander",
                  "hire a carpet cleaner", "carpet cleaner hire",
                  "hire a wallpaper stripper", "hire a tile cutter", "tile cutter hire",
                  "hire a pressure washer", "pressure washer hire",
                  "hire a hedge trimmer", "tool hire", "hire shop", "hire a tool",
                  "hiring a tool", "hire tools", "hire some tools"),
        "thing": "a hired tool",
        "reply": "Most tools are £10 to £35 for the first day at a hire shop: a breaker or a big "
                 "drill £15 to £30, a step ladder £10 to £20, a carpet cleaner £20 to £35, a "
                 "floor sander £35 to £60 and a scaffold tower £40 to £80, and a weekend rate is "
                 "often the price of one day. The deposit, not the day rate, is the figure that "
                 "adds up at the counter, usually £50 to £200 and back when the tool comes back "
                 "clean, and a late return is charged as another day. Ask two shops for the day "
                 "rate with the damage waiver included before you book.",
    },
    "photographer": {
        "names": ("photographer", "wedding photographer", "photo shoot"),
        "thing": "a photographer",
        "reply": "A wedding photographer is usually £1,000 to £2,500 for the day, and a family "
                 "shoot £150 to £400 including some prints. The package matters more than the "
                 "day rate: ask how many hours, how many edited images, and whether you get the "
                 "files to print yourself.",
    },
}

ENTRIES = [
    entry("cost-" + key,
          (data["names"],
           _COST + (_A_VISIT_FEE if key in _VISIT_FEE_JOBS else ()))
          + ((data["shapes"],) if data.get("shapes") else ()),
          data["reply"],
          avoid=(_DIY if data.get("diy", True) else ())
          + ("cheaper at", "or a", "instead of", "which is better", "best buy")
          + data.get("avoid", ()),
          ask=data.get("ask", ()),
          guard=lambda understood, names=data["names"], fence=data.get("fence_how_to", False): (
              _not_a_steps_ask(understood)
              and not (fence and _a_steps_ask_with_no_price(understood))
              and not the_appliance_swallows_the_name(understood, names)),
          bias=data.get("bias", 1))
    for key, data in JOBS.items()
]

ENTRIES.append(entry("cost-plumber-sink",
      (("sink", "sinks", "fix a sink", "repair a sink", "sink repair", "sink leak",
        "a leaking sink", "fit a sink", "fitting a sink", "install a sink", "a new sink"),
       _COST + ("fix", "fixes", "repair", "repairs", "repairing", "replace", "replacing", "fit",
                "fitting", "install", "installing")),
      JOBS["plumber"]["reply"],
      avoid=_DIY + ("basin", "sink unit", "sink waste", "sink plug", "buy a sink", "cheapest",
                    "best buy", "blocked", "blockage", "unblock", "smell", "smells", "clean",
                    "cleaning", "drain", "drains", "tap", "taps"),
      bias=2))


_PRICE_SHAPE = re.compile(
    r"\bhow\s+much\s+(?:is|are|was|were|for|would|will)\b"
    r"|\b(?:cost|costs|costing|price|prices|priced)\b", re.IGNORECASE)
_AMOUNT_SHAPE = re.compile(
    r"\bhow\s+many\b|\bper\s+(?:person|head|serving|portion|adult|child|kg|kilo)\b"
    r"|\bportions?\b|\bgrams?\b|\bcalories\b|\bprotein\b|\bper\s+day\b|\ba\s+day\b"
    r"|\bfor\s+(?:\d+|two|three|four|five|six|seven|eight)\b|\bpeople\b|\bserves?\b"
    r"|\bhow\s+long\b|\bkeep\b|\bfreez(?:e|es|ing)\b|\bleft\s?overs?\b"
    r"|\bshould\s+i\s+(?:use|eat|have|drink|cook|add|give|feed|take|put|make|buy)\b"
    r"|\b(?:should|shall)\s+(?:i|we)\s+(?:use|eat|have|drink|cook|add|give|feed|take|put|make)\b"
    r"|\bplant|\bplants|\bseed\b|\bseeds|\bseedlings?|\bgrow|\bgrows|\bgrowing|\bgrew\b"
    r"|\bgrown\b|\bvariet(?:y|ies)|\bharvest|\bsow\b|\bsow(?:ed|ing)\b|\bplanting\b"
    r"|\bsoup\b|\bsoups\b|\bpie\b|\bpies\b|\bpuddings?\b|\bsandwich|\btoast\b"
    r"|\bjacket\b|\bmash\b|\bmashed\b|\bcurry|\bcasseroles?\b|\bstew|\broast\b"
    r"|\bjar\b|\bjars\b|\bsalad\b|\bbake\b|\bbaked\b|\btopping|\bfilling|\bpizza"
    r"|\bcake\b|\bbiscuits?\b|\bbread\b|\bpot\b|\bpots\b", re.IGNORECASE)


def _a_price_for_the_shop(understood):
    if not isinstance(understood, dict):
        return False
    line = (understood.get("clean") or understood.get("text") or "").lower()
    if not line or _AMOUNT_SHAPE.search(line):
        return False
    return bool(_PRICE_SHAPE.search(line))


GROCERIES = {
    "water": {
        "names": ("bottle of water", "bottled water", "pack of water", "case of water",
                  "water in a shop", "still water", "sparkling water"),
        "reply": "A 500ml bottle of water is about £1 in a shop and £2 or more at a station, "
                 "while a 6-pack of 1.5 litre bottles is about £3 to £4 in a supermarket. Tap "
                 "water is the same stuff and costs nothing, so the bottle is for the day out.",
    },
    "cheese": {
        "names": ("cheese", "block of cheese", "block of cheddar", "cheddar", "400g of cheese",
                  "packet of cheese"),
        "reply": "A 400g block of cheddar is about £3.50 to £5, and the same weight of a named "
                 "farmhouse one £4 to £6. Mature costs a little more than mild, and the deli "
                 "counter is dearer than the block.",
    },
    "butter": {
        "names": ("butter", "block of butter", "packet of butter", "tub of butter"),
        "reply": "A 250g block of butter is about £2.20 to £3, and a tub of spread about £1.50. "
                 "Own-brand butter is the cheapest, and it freezes well, so buy it when it is on "
                 "offer.",
    },
    "pasta": {
        "names": ("pasta", "bag of pasta", "packet of pasta", "spaghetti", "penne"),
        "reply": "A 500g bag of dried pasta is about 75p to £1.50, and a fresh one £2 to £3. "
                 "Dried is a fifth of the price a portion, and the shape does not change the "
                 "price much.",
    },
    "rice": {
        "names": ("rice", "bag of rice", "kilo of rice", "basmati", "long grain rice"),
        "reply": "A kilo of long-grain rice is about £1 to £2.50 and a kilo of basmati £2 to "
                 "£3.50. It keeps for months in a cupboard, so the bigger bag is usually the "
                 "better buy.",
    },
    "bacon": {
        "names": ("bacon", "pack of bacon", "packet of bacon", "rashers", "smoked bacon"),
        "reply": "A 300g pack of bacon is about £2.50 to £4. Dry-cured costs more than the kind "
                 "that is pumped with water, which shrinks in the pan, and the 2-for deals are "
                 "usually the cheapest way to buy it.",
    },
    "salmon": {
        "names": ("salmon", "salmon fillets", "side of salmon", "piece of salmon"),
        "reply": "Two salmon fillets are about £5 to £7, and a whole side £15 to £25. The frozen "
                 "fillets are often half the price of the fresh counter for the same fish.",
    },
    "bananas": {
        "names": ("bananas", "banana", "bunch of bananas"),
        "reply": "Bananas are about 15p to 25p each, so a bunch of five is roughly £1. Loose ones "
                 "are cheaper than a pre-packed bag, and the ripe ones on the reduce shelf are "
                 "the bargain.",
    },
    "apples": {
        "names": ("apples", "apple", "bag of apples"),
        "reply": "Six apples are about £1.50 to £2.50 and a kilo about £2. Loose ones let you "
                 "pick the size, and a bag of the smaller ones is usually the cheapest way.",
    },
    "tomatoes": {
        "names": ("tomatoes", "tomato", "pack of tomatoes", "punnet of tomatoes", "cherry tomatoes"),
        "reply": "A 400g pack of salad tomatoes is about £1 to £2, and a punnet of cherry ones "
                 "£1.50 to £2.50. Loose ones are usually cheaper than a punnet, and in August "
                 "they are half the winter price.",
    },
    "mince": {
        "names": ("mince", "beef mince", "pack of mince", "minced beef"),
        "reply": "500g of beef mince is about £4 to £6, with the 5% fat one a pound or two more "
                 "than the 20%. Turkey and pork mince are cheaper, and a bigger pack is usually "
                 "the better price a kilo.",
    },
    "sausages": {
        "names": ("sausages", "sausage", "pack of sausages", "pork sausages"),
        "reply": "Six to eight sausages are about £2.50 to £4, and a butcher's £4 to £6. The "
                 "cheapest are mostly rusk and water, so read the meat percentage on the pack.",
    },
    "cereal": {
        "names": ("cereal", "box of cereal", "cornflakes", "box of cornflakes", "muesli"),
        "reply": "A box of cereal is about £2 to £3.50, and the shop's own version of a branded "
                 "one about half the price. A big bag of own-brand flakes is the cheapest "
                 "breakfast there is a bowl.",
    },
    "yoghurt": {
        "names": ("yoghurt", "yogurt", "pot of yoghurt", "tub of yoghurt", "greek yoghurt"),
        "reply": "A four-pack of yoghurt is about £1.50 to £2.50, and a 1kg tub £2 to £3, which "
                 "is much cheaper a portion. Greek-style costs more than natural, and the big "
                 "tub is the one to buy if you eat it every day.",
    },
    "peas": {
        "names": ("peas", "frozen peas", "bag of peas", "kilo of peas"),
        "reply": "A kilo of frozen peas is about £1.50 to £2 and lasts months. Fresh peas in "
                 "season are sweeter but cost three or four times as much for a much smaller "
                 "bag.",
    },
}

ENTRIES += [
    entry("shop-" + key,
          (data["names"], _PRICE),
          data["reply"],
          avoid=("per person", "per head", "portion", "portions", "recipe", "recipes",
                 "to make", "to bake", "how to make", "how do i make", "from scratch",
                 "too much", "splash", "splash of", "a dash", "dash of", "a drop", "drop of",
                 "glug", "a bit", "how much is left", "left over",
                 "bigger", "larger", "smaller",
                 "calories", "protein", "how many", "a day", "substitute", "instead of",
                 "allergy", "allergic", "baby", "toddler", "freeze", "freezer", "defrost"),
          ask=("how much", "cost", "costs", "price", "prices", "much does", "much is",
               "much are", "much for"),
          bias=2,
          guard=_a_price_for_the_shop)
    for key, data in GROCERIES.items()
]

_TIME = ("how long", "how many hours", "how much time", "long does", "long will",
         "hours does", "minutes does", "how many days", "how many minutes")

_A_WAIT = ("how long before", "how long after", "how long till", "how long until",
           "how long should i leave", "how long do i leave", "how long to wait",
           "how long do i wait", "should i wait", "leave it before", "before should i",
           "how long do i have to wait", "how long will i have to wait",
           "how long will we have to wait", "how long do you have to wait",
           "have to wait", "how long is the wait", "how long the wait", "how long a wait",
           "the wait for", "wait to see", "waiting list", "how long would i wait",
           "how long is the waiting")

A_AGE_OWNED = ("how long have i had", "how long have i been", "how long have i owned",
               "how long have i kept", "how long have you had", "how long have you been",
               "how long have you owned", "how long have you kept", "how long have we had",
               "how long have we been", "how long have we kept", "how long have they had",
               "how long have they been", "how long has it been", "how long has he had",
               "how long has she had", "how long did i have", "how long did you have",
               "how long has my", "how long has our", "how long has this", "how long has the",
               "how long has that", "how long has she been", "how long has he been",
               "how long have my", "how long have our", "how long have these",
               "how long have those", "how long have the")

_A_CAREER = ("school", "vet school", "med school", "training", "train", "trained", "degree",
             "study", "studying", "university", "college", "qualify", "qualified", "qualifying",
             "become", "becoming", "career", "get into", "to be a", "how do i", "myself")

_NOT_A_CAR = ("bike", "bikes", "bicycle", "bicycles", "cycling", "cyclist", "motorbike",
              "motorbikes", "motorcycle", "motorcycles", "scooter", "scooters")

JOB_TIMES = {
    "dentist": {
        "names": ("dentist appointment", "dentist appointments", "dental appointment",
                  "check up at the dentist", "dentist check up", "dentist checkup",
                  "appointment at the dentist", "dentist", "dentists",
                  "dentist take", "dentist takes", "dentist taking"),
        "bare": ("dentist", "dental"),
        "reply": "A check-up is about 20 minutes. A filling is 30 to 45 minutes, and a crown or a "
                 "root canal is usually one longer visit or two, so book the morning for one of "
                 "those and do not plan anything straight after.",
        "bias": 1,
        "avoid": ("register", "registering", "find a dentist", "nhs dentist", "emergency",
                  "pain", "toothache", "tooth hurts", "cost", "costs", "much", "price", "free",
                  "brace", "braces", "implant", "child", "children", "baby", "become",
                  "training", "degree", "study", "how do i", "myself"),
    },
    "eye-test": {
        "names": ("eye test", "eye tests", "eye exam", "appointment at the optician",
                  "optician appointment"),
        "bare": ("eye test"),
        "reply": "An eye test is about 20 to 30 minutes, and longer if you are choosing glasses "
                 "afterwards. Say at the start if you drive or use a screen all day, because the "
                 "test and the prescription are read with that in mind.",
        "avoid": ("cost", "costs", "much", "price", "free", "glasses", "contact lens",
                  "contacts", "child", "children", "baby", "how do i", "myself", "valid",
                  "good for", "prescription", "last", "lasts"),
    },
    "gp-appointment": {
        "names": ("gp appointment", "doctor appointment", "doctor's appointment",
                  "appointment with the doctor", "appointment with a doctor", "see the doctor",
                  "see a doctor"),
        "bare": ("gp", "doctor"),
        "reply": "A standard GP appointment is 10 minutes, so it is worth naming the one problem "
                 "that matters most and what you need from it. If there are several things, say "
                 "so when you book and ask for a double slot rather than trying to fit them in.",
        "avoid": ("register", "registering", "find a doctor", "out of hours", "emergency",
                  "urgent", "999", "111", "cost", "costs", "much", "price", "how do i",
                  "myself", "letter", "fit note", "sick note",
                  "referral", "referred", "refer", "waiting", "wait", "available", "booking",
                  "book", "to see", "get seen", "appointment come through", "hear back"),
    },
    "physio": {
        "names": ("physio appointment", "physiotherapy appointment", "physio session",
                  "physiotherapy session", "appointment with the physio",
                  "appointment with a physio", "see the physio", "see a physio"),
        "bare": ("physio", "physiotherapy"),
        "reply": "A first physiotherapy appointment is usually 30 to 45 minutes, because it "
                 "starts with the history and an examination, and the follow-ups are 20 to 30. "
                 "Ask what the plan is and how many sessions they expect before you pay for a "
                 "block, and whether you need to bring shorts or a vest to move in.",
        "avoid": ("cost", "costs", "much", "price", "nhs", "refer", "referred", "referral",
                  "how do i", "myself", "exercises", "worth",
                  "to work", "before it works", "start working", "helps", "help", "recover",
                  "recovery", "sessions will i need", "how many sessions", "how many"),
    },
    "haircut": {
        "names": ("haircut", "hair cut", "cut my hair", "hairdresser", "hairdressers", "barber",
                  "hair appointment", "hair appointments", "salon appointment", "highlights",
                  "colour my hair", "dye my hair"),
        "bare": ("haircut"),
        "reply": "A cut is 30 to 45 minutes; colour, highlights or a restyle is one and a half to "
                 "two and a half hours. If it is your first colour at a salon they will want a "
                 "patch test 48 hours before, so ring ahead and get that done.",
        "avoid": ("cost", "costs", "much", "price", "style", "which", "child", "children",
                  "baby", "myself", "how do i", "last", "lasts", "lasted", "grow out",
                  "how often"),
    },
    "house-survey": {
        "names": ("house survey", "home survey", "building survey", "homebuyer report",
                  "homebuyers report", "structural survey", "surveyor", "survey"),
        "bare": ("survey"),
        "reply": "A valuation is 20 to 30 minutes on site, a homebuyer's report two to three "
                 "hours, and a full building survey four to six. The written report usually "
                 "follows within a few days, so ask when you will have it before you book, "
                 "because your lender and your solicitor may both be waiting on it.",
        "avoid": ("garden", "soil", "land", "cost", "costs", "much", "price", "quote",
                  "choose", "find a surveyor", "how do i", "myself", "satisfaction"),
    },
    "vet": {
        "names": ("vet appointment", "appointment at the vet", "appointment with the vet",
                  "vet visit", "see the vet",
                  "vet take", "vet takes", "vet taking"),
        "bare": ("vet"),
        "reply": "A routine consultation is 15 to 20 minutes; a procedure, a scan or a dental is "
                 "longer and the practice will tell you how long when you book. Ask for an "
                 "estimate before they start, and for the out-of-hours number on the way out.",
        "avoid": ("cost", "costs", "much", "price", "quote", "insurance", "put down", "euthan",
                  "how do i", "myself"),
    },
    "tyres": {
        "names": ("tyre fitting", "fit tyres", "fit a tyre", "fit two tyres", "fitting tyres",
                  "new tyres", "puncture repair", "puncture", "change a tyre", "change my tyres",
                  "tyre", "tyres"),
        "bare": ("tyre", "tyres"),
        "reply": "Two tyres take about 30 to 45 minutes, and a puncture repair 20 to 30. Most "
                 "places take walk-ins, but ring first if you need a particular tyre, and check "
                 "the pressures again a day or two later.",
        "avoid": ("last", "lasts", "lasted", "life", "wear", "worn", "miles", "tread",
                  "pressure", "which", "winter", "snow", "best", "cheap", "cost", "costs",
                  "much", "price", "how do i", "myself", "spare") + _NOT_A_CAR,
    },
    "car-service": {
        "names": ("car service", "service my car", "service the car", "car servicing",
                  "full service", "major service"),
        "bare": ("car service"),
        "reply": "A car service is usually two to three hours for an interim or a full service, "
                 "and a major service with plugs and filters can take most of the day. Ask when "
                 "you book whether they keep the car or you wait, and whether the price includes "
                 "the MOT if it is due.",
        "avoid": ("cost", "costs", "much", "price", "quote", "which", "worth", "due",
                  "how do i", "myself") + _NOT_A_CAR,
    },
}

def time_entries(*keys):
    rows = []
    for key in keys:
        data = JOB_TIMES[key]
        bare = data.get("bare", ())
        names = data["names"] + ((bare,) if isinstance(bare, str) else tuple(bare))
        rows.append(entry("time-" + key,
                          (names, _TIME),
                          data["reply"],
                          avoid=_A_WAIT + _A_CAREER + A_AGE_OWNED + _DIY + data.get("avoid", ()),
                          bias=max(data.get("bias", 0), 3)))
    return rows

ANSWERS = ("home-and-diy", "shopping", "money", "pets", "garden-and-plants")


SUBSCRIPTIONS = {
    "gym": {
        "names": ("gym", "gyms", "gym membership", "leisure centre", "leisure center"),
        "thing": "a gym",
        "span": (20, 45),
        "visit": (6, 12),
        "uses": "A gym is only worth it per visit: at eight visits a month that is {eighth} a "
                "visit, at four it is {quarter}.",
        "advice": "Watch the joining fee and the 12-month contract, and ask them to drop the "
                  "joining fee - a council gym or a pay-as-you-go swim usually beats the chain.",
    },
    "phone": {
        "names": ("phone", "mobile", "sim", "sim only", "sim-only", "handset", "contract",
                  "iphone", "smartphone"),
        "thing": "a phone deal",
        "span": (5, 30),
        "uses": "A SIM-only deal is £5 to £25 a month and a contract that includes the handset is "
                "£20 to £45, so it is only the handset part that is dear.",
        "advice": "Buying the phone outright and taking a cheap SIM usually costs less over two "
                  "years, and you are not tied in when the next one comes out.",
    },
    "broadband": {
        "names": ("broadband", "fibre", "internet", "wifi", "wi-fi"),
        "thing": "a broadband deal",
        "span": (25, 40),
        "uses": "There is no per-use test here, so the thing to compare is the speed you actually "
                "use: a 100Mb line is enough for two people streaming.",
        "advice": "The price almost always goes up out of contract, so diarise the end date - the "
                  "retention price on a call is usually £5 to £10 a month less than the renewal.",
    },
    "tv": {
        "names": ("netflix", "streaming", "sky", "now tv", "disney", "prime", "tv package",
                  "tv licence", "subscription"),
        "thing": "a TV service",
        "span": (6, 20),
        "uses": "Two services at once is where this gets expensive, so count how many you pay for "
                "and when you last watched each.",
        "advice": "Pick one at a time and cancel the one you are not watching: they all let you "
                  "restart it in a month, and the yearly price of two is the price of a holiday.",
    },
    "magazine": {
        "names": ("magazine", "magazines", "newspaper", "paper", "journal"),
        "thing": "a magazine",
        "span": (4, 12),
        "uses": "The issue price is £4 to £7 in a shop, so a monthly one is a small saving.",
        "advice": "The library app gives most UK magazines away free with a library card, which is "
                  "the cheapest way to read them.",
    },
    "electricity": {
        "names": ("electricity", "electric bill", "electricity bill", "electric", "power bill",
                  "electricity prices"),
        "thing": "electricity for a typical home",
        "span": (60, 120),
        "uses": "That range is a two- or three-bedroom home on a standard tariff: a one-bed flat "
                "can be half of it, and electric heating or charging a car at home doubles it.",
        "advice": "The standing charge is fixed whatever you use, so the levers are the unit rate "
                  "and what runs the heat: a smart meter display shows what each appliance costs, "
                  "and a timer on the immersion is usually the first saving.",
    },
    "gas": {
        "names": ("gas bill", "gas", "gas prices", "heating bill", "gas heating"),
        "thing": "gas for a typical home",
        "span": (45, 100),
        "uses": "Gas is heating and hot water, so it swings with the weather: much more in "
                "January and almost nothing in July, which is what the yearly average smooths out.",
        "advice": "Turning the boiler's flow temperature down to 55 to 60C, and the room "
                  "thermostat down by one degree, are the two cheapest savings.",
    },
    "energy": {
        "names": ("dual fuel", "energy bill", "energy bills", "energy", "gas and electric",
                  "gas and electricity"),
        "thing": "gas and electricity together",
        "span": (110, 210),
        "uses": "That is both fuels averaged over the year, which is what a direct debit is "
                "spread across.",
        "advice": "Check the unit rate against the price cap and the standing charge against the "
                  "rest, take a fixed deal when the cap is about to rise, and read the meter on "
                  "the day you switch.",
    },
    "class": {
        "names": ("class", "classes", "lesson", "lessons", "swimming lessons", "yoga", "pilates",
                  "dance", "tutor", "tutoring", "club"),
        "thing": "a class",
        "span": (8, 30),
        "visit": (8, 15),
        "uses": "At four classes a month that is {quarter} a class, at eight it is {eighth}, and "
                "a block of ten is usually cheaper than ten singles.",
        "advice": "A leisure centre class is a good deal cheaper than a studio one, and the first "
                  "session is usually free, so try it before you pay for a term.",
    },
}

_PERIODS = (
    (re.compile(r"\b(?:a|per|each|every|one)\s*month\b|\bmonthly\b|\bpcm\b|\bp/m\b|"
                r"/\s*(?:mo|mth|month)\b", re.I), 12.0),
    (re.compile(r"\b(?:a|per|each|every)\s*(?:week|wk)\b|\bweekly\b", re.I), 52.0),
    (re.compile(r"\b(?:a|per|each|every)\s*year\b|\bannual(?:ly)?\b|\bpa\b|\bp\.a\.", re.I), 1.0),
    (re.compile(r"\b(?:a|per|each|every)\s*(?:day|night)\b|\bdaily\b", re.I), 365.0),
)
_SUM = re.compile(r"(\d[\d,]*(?:\.\d+)?)\s*(k\b)?", re.I)
_TOO_MUCH = re.compile(
    r"\b(?:too much|too expensive|too dear|rip[\s-]?off|ripped off|over the odds|steep|"
    r"overpriced|bad value|a lot of money|a lot|that much|expensive)\b", re.I)
_WORTH_IT = re.compile(r"\b(?:worth it|worth paying|good value|value for money)\b", re.I)
_ABOUT_RIGHT = re.compile(
    r"\b(?:about right|sound right|sounds right|reasonable|fair price|normal|"
    r"the going rate|about the rate|ok|okay|fair)\b", re.I)
_FIXED_FEE = re.compile(
    r"\b(?:licence|license|council tax|road tax|car tax|vat|duty|fine|penalty|mot|prescription|"
    r"passport|stamp duty|tuition|fee for|application fee|standing charge|court fee)\b", re.I)
_JUST_A_PAYMENT = frozenset(("subscription", "subscriptions", "contract", "package", "deal",
                             "bill", "bills"))
_NOT_POUNDS = re.compile(r"[$]|\bdollars?\b|\bbucks\b|\beuros?\b|\u20ac", re.I)
_SHORT_PERIOD = re.compile(
    r"\b(?:a|per|each|every)\s*(?:day|night|week|wk)\b|\bdaily\b|\bweekly\b|"
    r"/\s*(?:day|wk|week)\b|\bp/w\b", re.I)
_ONE_OCCASION = re.compile(
    r"\b(?:lesson|lessons|class|classes|session|sessions|swim|swims|visit|visits|"
    r"appointment|appointments|treatment|treatments|haircut|haircuts|massage|massages|"
    r"clean|cleans|round of golf|court booking)\b", re.I)
_NOT_A_BILL = re.compile(
    r"\b(?:electric|electrical) (?:car|vehicle|bike|scooter|van|blanket|shower|toothbrush|"
    r"razor|guitar|heater|fire)\b|\bev\b|\be-?bike\b", re.I)
_COUNT = {"once": 1, "twice": 2, "three times": 3, "four times": 4, "five times": 5,
          "six times": 6, "seven times": 7}
_USES_IT = re.compile(
    r"\b(once|twice|three times|four times|five times|six times|seven times|\d+ times)\b"
    r"(?:\s*(?:a|per|each|every|a week|a month)\s*(week|month|day|fortnight)\b)?", re.I)


_NOT_GOING = re.compile(
    r"\bnever (?:go|goes|use|used|been|attend|make it)\b|\bdon'?t (?:go|use|used)\b|"
    r"\bdo not (?:go|use)\b|\bnot (?:using|going|been)\b|\bhaven'?t (?:been|used|gone)\b|"
    r"\bstopped going\b", re.I)


def _visits_a_month(text):
    match = _USES_IT.search(text)
    if not match:
        return 0
    said = match.group(1).lower()
    count = _COUNT.get(said)
    if count is None:
        digits = re.match(r"(\d+)", said)
        count = int(digits.group(1)) if digits else 0
    if not count:
        return 0
    period = (match.group(2) or "").lower()
    if not period:
        return -1
    if period in ("month",):
        return count
    if period in ("day",):
        return count * 30
    if period in ("fortnight",):
        return count * 2
    return count * 52.0 / 12.0


def _sum_and_per_month(text):
    for match in _SUM.finditer(text):
        amount = float(match.group(1).replace(",", ""))
        if match.group(2):
            amount *= 1000
        if amount < 1:
            continue
        for pattern, a_year in _PERIODS:
            if pattern.search(text[match.end():match.end() + 22]):
                return amount, amount * a_year / 12.0
    return 0.0, 0.0


def _pounds(figure):
    return "£%s" % format(int(round(figure)), ",")


def _verdict(monthly, low, high, text, thing):
    if _WORTH_IT.search(text):
        if monthly < (low + high) / 2.0:
            return "Yes, that is good value for %s" % thing
        if monthly <= high:
            return "Yes, that is about the going rate for %s" % thing
        return "No, that is dear for %s" % thing
    if _ABOUT_RIGHT.search(text):
        if monthly <= high:
            return "Yes, that is about right for %s" % thing
        return "No, it is above the usual range for %s" % thing
    if monthly < low:
        return "No, that is below the usual range for %s" % thing
    if monthly <= high:
        return "No, that is normal for %s" % thing
    if monthly <= high * 1.6:
        return "No, though it is at the top of the range for %s" % thing
    return "Yes, that is well above the range for %s" % thing


def _sum_a_month_reply(understood):
    read = understood or {}
    text = str(read.get("clean") or read.get("text") or "")
    if not (_TOO_MUCH.search(text) or _WORTH_IT.search(text) or _ABOUT_RIGHT.search(text)):
        return None
    if _FIXED_FEE.search(text) or _NOT_A_BILL.search(text) or _NOT_POUNDS.search(text):
        return None
    uses = _visits_a_month(text)
    amount, monthly = _sum_and_per_month(text)
    if not monthly:
        return None
    where = " ".join(str(word) for word in (read.get("words") or ())).lower() or text.lower()
    named = []
    for data in SUBSCRIPTIONS.values():
        matched = [name for name in data["names"]
                   if re.search(r"\b%s\b" % re.escape(name), where)]
        thing_named = [name for name in matched if name not in _JUST_A_PAYMENT]
        if thing_named:
            named.append((1, max(len(name) for name in thing_named), data))
        elif matched:
            named.append((0, max(len(name) for name in matched), data))
    for _, __, data in sorted(named, key=lambda row: (-row[0], -row[1])):
        low, high = data["span"]
        if _NOT_GOING.search(text) and data.get("visit"):
            visit_low, visit_high = data["visit"]
            return ("Yes, that is too much for something you do not use: %s a month is %s a year "
                    "for nothing. Cancel it in writing and keep the date you sent it, because most "
                    "gyms want a month's notice, and pay as you go when you do go - about %s to "
                    "%s a visit." % (_pounds(monthly), _pounds(monthly * 12), _pounds(visit_low),
                                     _pounds(visit_high)))
        if _NOT_GOING.search(text):
            return None
        if uses >= 1 and data.get("visit"):
            per_visit = monthly / uses
            visit_low, visit_high = data["visit"]
            if per_visit <= visit_high:
                verdict = "No, that works out at a fair price a visit"
            elif per_visit <= visit_high * 1.6:
                verdict = "No, though it is dear per visit at the rate you go"
            else:
                verdict = "Yes, that is too much for how often you go"
            count = int(round(uses))
            return ("%s. %d visit%s a month at %s a month is %s a visit, and paying as you go is "
                    "usually %s to %s a visit. %s"
                    % (verdict, count, "" if count == 1 else "s", _pounds(monthly),
                       _pounds(per_visit),
                       _pounds(visit_low), _pounds(visit_high), data["advice"]))
        if uses != 0:
            return None
        if (data.get("visit") and _SHORT_PERIOD.search(text)
                and _ONE_OCCASION.search(text)):
            return None
        return ("%s. %s a month is %s a year, and %s is usually %s to %s a month. %s %s"
                % (_verdict(monthly, low, high, text, data["thing"]), _pounds(monthly),
                   _pounds(monthly * 12), data["thing"], _pounds(low), _pounds(high),
                   data["uses"].format(quarter=_pounds(monthly / 4),
                                       eighth=_pounds(monthly / 8),
                                       day=_pounds(monthly / 22),
                                       week=_pounds(monthly * 12 / 52)),
                   data["advice"]))
    return None


def _a_sum_a_month(memory, understood):
    return (_sum_a_month_reply(understood)
            or _sum_a_month_reply({"clean": SUM_A_MONTH_SAMPLE}))


_SUM_A_MONTH_KEY = (
    ("too much", "too expensive", "too dear", "rip off", "rip-off", "ripped off",
     "over the odds", "worth it", "worth paying", "about right", "sound right", "sounds right",
     "reasonable", "good value", "bad value", "steep", "a lot of money", "overpriced",
     "normal", "the going rate", "ok", "okay", "fair",
     "a lot", "that much", "too much money", "expensive"),
    tuple(name for data in SUBSCRIPTIONS.values() for name in data["names"]),
)

SUM_A_MONTH_ID = "cost-a-sum-a-month"
SUM_A_MONTH_SAMPLE = "is 40 a month for a gym too much"

ENTRIES.append(entry(
    SUM_A_MONTH_ID,
    _SUM_A_MONTH_KEY,
    _a_sum_a_month,
    guard=lambda understood: bool(_sum_a_month_reply(understood)),
    bias=2))
