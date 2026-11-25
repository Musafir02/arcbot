import re

from . import fallback, pick

A_METHOD = re.compile(
    r"\bhow (?:do|can|could|should|would) i\b|\bhow to\b|\bwhats the best way\b|"
    r"\bwhat is the best way\b|\bhow do you\b")
A_TIME = re.compile(
    r"\bwhat time\b|\bwhat day\b|\bwhich day\b|\bhow soon\b|\bwhat date\b|\bwhen\b|"
    r"\bhow long (?:till|until|before|after|to)\b|\bopen (?:today|tomorrow|on)\b")
A_PLACE = re.compile(r"\bwhere\b")
A_FREQUENCY = re.compile(r"\bhow (?:often|frequently)\b|\bhow many times\b")
A_FIGURE = re.compile(
    r"\bhow (?:much|many|long|often|far|big|heavy|hot|old|deep|tall|wide)\b|"
    r"\bhow much\b|\bwhat (?:size|weight|percentage)\b|\bhow much does\b")
A_REASON = re.compile(r"\bwhy\b")

PART_WORD = {
    "frequency": "the schedule",
    "figure": "the figure",
    "time": "the timing",
    "place": "the right place",
    "method": "the exact steps",
    "reason": "the reason",
}

KINDS = (
    ("clinical", re.compile(
        r"\b(?:tens|nebulisers?|nebulizers?|cpap|bipap|inhalers?|spacers?|crutches?|"
        r"walking (?:frame|stick|aid)|zimmer|catheters?|stoma|insulin|blood pressure monitor|"
        r"glucose meter|hearing aids?|compression (?:stocking|stockings|sleeve|sock|socks|tights)|"
        r"oxygen concentrator|feeding tube|peg tube)\b")),
    ("animal", re.compile(
        r"\b(?:dog|dogs|puppy|pup|cat|cats|kitten|rabbit|hamster|guinea pig|budgie|parrot|fish|"
        r"horse|pony|chickens?|hens?|ducks?|tortoise|snake|lizard|pet|pets|puppies|kittens)\b")),
    ("plant", re.compile(
        r"\b(?:plants?|trees?|shrubs?|roses?|tomato(?:es)?|potato(?:es)?|grass|lawn|hedge|"
        r"seedlings?|houseplants?|orchids?|cactus|fern|bulbs?|flowers?|vegetables?|herbs?|"
        r"garden|cuttings?|compost)\b")),
    ("appliance", re.compile(
        r"\b(?:boiler|kettle|washer|washing machine|dishwasher|oven|cooker|hob|fridge|freezer|"
        r"fridge freezer|radiators?|heaters?|hoover|vacuum|dryer|tumble dryer|extractor|shower|"
        r"taps?|sink|mowers?|lawnmower|drill|microwave|toaster|iron|mattress|"
        r"humidifiers?|dehumidifiers?|air fryer|slow cooker|pressure cooker|bread maker|"
        r"breadmaker|coffee machine|blender|mixer|food processor|sewing machine|stitch|"
        r"strimmer|hedge trimmer|chainsaw|sander|pressure washer|jet wash|air conditioner|"
        r"air con|heat pump|fan|extractor fan|freezer|tumble|washer dryer|water softener|"
        r"\w+(?:ifier|ator|iser|izer))\b")),
    ("device", re.compile(
        r"\b(?:phone|laptop|tablet|computer|pc|router|wifi|broadband|console|smart watch|app|"
        r"account|email|password|website|browser|spreadsheet|software|printer|speaker|telly|tv|"
        r"television|privacy settings?)\b")),
    ("paper", re.compile(
        r"\b(?:bill|statement|letter|form|invoice|receipt|contract|ticket|warranty|guarantee|"
        r"passport|licence|license|payslip|tenancy|policy|quote|estimate|certificate|"
        r"application|booking|reservation|reference number)\b")),
    ("place", re.compile(
        r"\b(?:museum|castle|cathedral|minster|gallery|theatre|theater|zoo|park|beach|market|"
        r"library|station|airport|hotel|cafe|restaurant|pub|shop|store|supermarket|swimming pool|"
        r"leisure centre|farm|stadium|arena|church|abbey|palace|pier|harbour|harbor|city|town|"
        r"village|island|venue|exhibition)\b")),
    ("eyewear", re.compile(
        r"\b(?:glasses|specs|spectacles|contact lenses?|lenses|varifocals?|sunglasses)\b")),
    ("service", re.compile(
        r"\b(?:gp|doctor|dentist|vet|bank|council|school|nursery|surgery|hospital|insurance|"
        r"landlord|letting agent|solicitor|builder|plumber|electrician|garage|post office|"
        r"jobcentre|university|college)\b")),
)

WHERE_IT_LIVES = {
    "animal": (
        "The vet or the practice's own page has it for the breed and the age, and the rehoming "
        "charity that matches the breed prints a figure too."),
    "plant": (
        "The label that came with that one has it, and the grower's or the RHS page keeps one by "
        "plant name and the time of year."),
    "appliance": (
        "The maker's own page has it for the model number on the rating plate, and the manual "
        "says it in the specification pages."),
    "device": (
        "The maker's support page has it for the model, and the settings screen on the thing "
        "itself shows what it is set to now."),
    "paper": (
        "The paperwork has it: the figure, the date and the reference are printed on the "
        "document itself, and the number to ring is on the back."),
    "place": (
        "The venue's own page or its map listing has it, and it changes with the day, so today's "
        "is the one that counts."),
    "eyewear": (
        "The optician who fitted them has it, and the practice's own page says what to expect and "
        "when to go back."),
    "service": (
        "The organisation's own page has it, and the number on your last letter from them reaches "
        "the desk that decides."),
    "part": (
        "The manual or the fitting sheet for the thing it belongs to has the step for that part, "
        "and the maker's page has it for the model number, which is on the rating plate or the "
        "paperwork that came with it."),
    "bought": (
        "The label or the paperwork that came with it is where its own numbers are, and the shop "
        "that sold it will tell you over the phone what it is and what it wants."),
    "living": (
        "The people who keep them have it rather than a maker: the local association, the supplier "
        "you got them from, or a keeper a few years in will tell you the calendar for your area."),
    "clinical": (
        "Whoever prescribed or fitted it has it: the plan is written on the sheet they gave you, "
        "and the clinic or the pharmacist on that sheet answers a question about it."),
}

HOLDS = {
    "animal": frozenset(("figure", "frequency", "method", "reason")),
    "part": frozenset(("method", "figure", "place")),
    "plant": frozenset(("figure", "frequency", "method", "reason", "time")),
    "appliance": frozenset(("figure", "frequency", "method", "reason")),
    "device": frozenset(("figure", "frequency", "method", "reason")),
    "paper": frozenset(("figure", "time")),
    "place": frozenset(("figure", "time", "place")),
    "eyewear": frozenset(("figure", "frequency", "method", "reason", "time")),
    "service": frozenset(("figure", "time", "place", "method")),
    "bought": frozenset(("figure", "frequency", "method", "reason")),
    "living": frozenset(("frequency", "method", "reason", "time")),
    "clinical": frozenset(("frequency", "method", "reason", "time")),
}

COOKING = re.compile(
    r"\b(?:cook|cooks|cooked|cooking|roast|bake|boil|fry|grill|eat|eating|edible|recipe|oven|"
    r"marinade|defrost|reheat|serve|serving|portion|dinner|lunch|tea|pie|soup|stock|stuffing)\b")
A_PURCHASE = re.compile(
    r"\b(?:new one|a new|to buy|buy|buys|buying|cheapest|price of|replace|replacement|"
    r"cost of a new|how much is|how much are)\b")

MADE = frozenset(("appliance", "device", "part"))

GENERAL_BY_PART = {
    "method": (
        "the first step is nearly always the same one - turn it off, wait, and start again from "
        "the beginning of the maker's own instructions",
        "the order matters more than the steps: the maker's list is written to be done from the "
        "top, and skipping ahead is what leaves a job half finished"),
    "frequency": (
        "how often it needs doing depends on how hard it works, so the busier it is the shorter "
        "the gap",
        "there is a usual interval and it moves with how much it is used, with the sign you are "
        "behind showing as a change you notice rather than a number"),
    "figure": (
        "the figure is set by the model and the size, so two of the same kind of thing can differ "
        "by a lot",
        "the number on the thing itself - the plate, the box, the letter - is the one that decides "
        "it, not the one in the advert"),
    "time": (
        "the timing is set by the calendar rather than by the person, so the season or the day is "
        "what to go by",
        "there is usually one date that matters and everything else is worked back from it"),
    "place": (
        "the usual place is the one that already does that job, rather than a special trip",
        "anywhere that sells or services the thing will know who locally does the rest"),
    "reason": (
        "there are usually two or three common causes, and which one it is shows in when it "
        "happens and what changes with it",
        "the way to tell the causes apart is to change one thing at a time and watch what "
        "changes"),
}

BY_KIND = {
    ("bought", "frequency"): (
        "there is no number that fits every one of them: what it is made of, how much it is used "
        "and where it is kept all move it",
        "the sign you are behind shows in the thing itself rather than on a date - how it sounds, "
        "smells or looks changes before anything else does"),
    ("clinical", "frequency"): (
        "how often it is used is set by whoever prescribed it and by how you are doing, not by a "
        "number that fits everyone: the plan on their sheet is the one that counts",
        "the dose of it is the part that changes, so the gap between uses comes from the review "
        "rather than from the instruction leaflet"),
    ("clinical", "method"): (
        "the way to use it is the way it was shown to you, and the sheet or the clinic will show "
        "you again rather than leave you guessing",
        "the settings are the part to get right, so it is worth a phone call to the clinic rather "
        "than a guess at the dial"),
    ("clinical", "time"): (
        "how long you keep using it is theirs to say, and it is looked at again at the review they "
        "booked",
        "the length of it is set by how the thing it is for is healing rather than by the calendar"),
    ("living", "frequency"): (
        "how often it needs doing is set by the season and by how the animals are doing rather "
        "than by a maker: a look most weeks in the busy months and less in the cold, with the "
        "sign you are behind showing in them rather than in a number",
        "the calendar follows the year - the swarming months, the cold, the hungry gap - so two "
        "keepers in two places will not do it on the same week"),
    ("plant", "time"): (
        "garden jobs go by the season more than the calendar: sow while the soil is warm, plant "
        "bare-root things while they are dormant, prune most shrubs after they flower",
        "the soil and the weather decide the week, and the packet holds the variety and the "
        "depth"),
    ("plant", "frequency"): (
        "watering goes by the compost rather than the day: dry an inch down means water, damp "
        "means wait",
        "a feed every couple of weeks in the growing season is the usual, and nothing in winter"),
    ("part", "method"): (
        "the order is what matters: isolate it first - water off at the valve, or unplugged - then "
        "take the old part out and match it, because it comes out one way and goes back the same "
        "way",
        "the old part is the pattern: take it to the shop and match it rather than trusting a "
        "model number alone, since the same model can be made with two different fittings"),
    ("animal", "frequency"): (
        "how much and how often is set by the age and the weight more than the breed, and the two "
        "things worth watching are the weight and what is left in the bowl",
        "the amount goes up with age and down with age again, and a vet weighs the animal rather "
        "than guessing"),
    ("animal", "figure"): (
        "the figure is set by the age and the size of the animal rather than by the breed name",
        "the two numbers that matter are the weight and the amount, and the bag or the tin prints "
        "both"),
    ("appliance", "method"): (
        "nearly every appliance has a reset that the maker built in: off at the wall for a "
        "minute, then back on and let it finish starting up",
        "the model number is the thing to have in front of you - it is on the rating plate or "
        "inside the door - because the maker's steps are written for that model and not the one "
        "beside it"),
    ("device", "method"): (
        "the first step on nearly all of them is the same: restart it, then look for the setting "
        "the message named rather than changing several at once",
        "the settings screen shows what it is set to now, which is usually the thing that is "
        "wrong"),
    ("eyewear", "time"): (
        "most people are told a week or two to settle into new glasses, and the first thing to "
        "check is that they sit straight and level",
        "the first days are the ones that feel wrong, and a headache that lasts past that is "
        "worth going back with"),
    ("paper", "figure"): (
        "the document carries the figure, the date and a reference, and that reference is what "
        "unlocks the answer on the phone",
        "the number to ring is printed on the letter rather than found on a website"),
    ("place", "time"): (
        "opening hours move with the season, the day and the odd refurbishment, so the day itself "
        "is the one to check",
        "the hours on a listing are a snapshot, and the venue's own page is the one that is kept "
        "current"),
    ("service", "method"): (
        "the first step with any of them is to ask in writing and quote the reference, because "
        "that is what makes a record",
        "the desk that decides is reached by the number on their own letter, not the switchboard"),
    ("bought", "method"): (
        "the sheet, label or card that came with it is the shortest route, and the shop that sold "
        "it will tell you the way it is normally done",
        "the first step is the one written on whatever came in the box or on the label, and it is "
        "written for that thing rather than for its kind"),
}

TAIL = {
    "frequency": (
        "Say how it has been going so far and I will tell you what the usual is.",
        "Tell me what you have been doing with it and I will say whether that is enough.",),
    "figure": (
        "Tell me the number you are working from and I will do the arithmetic with you.",
        "Say what you are comparing it with and I will help you weigh it."),
    "time": (
        "Tell me when you need it by and I will work the timing back from that.",
        "Say what you are working around and I will lay out the order to do things in."),
    "place": (
        "Tell me which one you have in mind and I will say what to ask them.",),
    "method": (
        "Tell me what you have already tried and I will go through the next step with you.",),
    "reason": (
        "Tell me what you have noticed and I will say what usually causes it.",),
}

A_PERSON = re.compile(
    r"\b(?:mum|mom|mother|dad|father|son|daughter|kid|kids|child|children|baby|toddler|"
    r"boss|manager|partner|husband|wife|boyfriend|girlfriend|friend|neighbour|neighbor|sister|"
    r"brother|gran|granny|nan|aunt|uncle|cousin|teacher|carer)\b")
NOT_A_THING = frozenset("""
a an the it this that these those there here me you him her us them my your his its our their
something anything nothing everything one ones any some all more most less much many
thing things stuff
time times day days week weeks month months year years hour hours minute minutes
somebody anybody nobody everyone
new old secondhand second-hand little big small large same other good bad broken first next last
decent proper nice cheap expensive
got get gets got bought buy buying buyed ordered order arrived delivered picked treated
had have has want wants need needs keep keeps make makes made put puts use uses used
clean cleans cleaned fix fixes fixed change changes take takes took give gives gave
how what when where why which who whose often much many long soon till until
can could should would will shall may might must does did is are was were be been being am
about around anything something
at in on from with for to of by under over into near beside behind inside outside after before
during than like as per via onto upon within without across along towards toward through
""".split())
GOT_IT = re.compile(
    r"\b(?:(?:i|we|he|she|they|mum|dad)\s+(?:have\s+|had\s+|just\s+|finally\s+)?"
    r"(?:got|bought|ordered|won|were given|was given|picked up|treated myself to)"
    r"|(?:it|they|this|that|the [a-z]+)\s+(?:has\s+|had\s+)?(?:arrived|come|turned up)"
    r"|\bdelivered\b)")


def _parts_of(said):
    for name, rule in (("method", A_METHOD), ("time", A_TIME), ("place", A_PLACE),
                       ("frequency", A_FREQUENCY), ("figure", A_FIGURE),
                       ("reason", A_REASON)):
        if rule.search(said):
            return name
    return ""


ANIMAL_AS_A_SOURCE = re.compile(
    r"\b(?:pets?|dogs?|cats?|puppy|puppies|kitten|kittens|rabbit|hamster|horse|pony|tortoise|"
    r"parrot|budgie)\s+(?:'s\s+)?(?:hair|hairs|fur|fluff|moult|moulting|mess|poo|poop|poos|"
    r"wee|sick|vomit|smell|stink|stain|stains|mud|slobber|drool|spit|paw prints?|"
    r"footprints?|blanket|bed|basket|cage|hutch|litter|tray|toy|toys|lead|leash|collar|"
    r"bowl|bowls|food|biscuits|hairbrush|brush)\b")


def _kind_of(said):
    if ANIMAL_AS_A_SOURCE.search(said):
        return ""
    for kind, rule in KINDS:
        if rule.search(said):
            return kind
    return ""


SINGULAR_BUT_ENDS_IN_S = frozenset("""
mattress glass address gas bus dress class canvas tennis business harness lens iris
press stress boss mess
""".split())


REFERS_BACK = re.compile(
    r"\b(?:it|its|them|they|those|that one|this one|the one|that|this)\b")
A_DETERMINER = re.compile(r"\b(?:my|our|the|this|these|a|an)\s+[a-z]")


def _that(thing):
    if thing.endswith("s") and thing not in SINGULAR_BUT_ENDS_IN_S:
        return "those"
    return "that"


A_BUYING_NOW = re.compile(
    r"\b(?:after an?|in the market|looking at an?|thinking (?:of|about) (?:buying|getting)|"
    r"should i (?:buy|get)|shall i (?:buy|get)|is it worth buying|which one (?:shall|should) i)\b")
NUTRITION = re.compile(
    r"\b(?:calorie|calories|kcal|protein|protien|carbs?|carbohydrate|vitamins?|fibre|fiber|"
    r"nutrients?|how many grams|grams? of)\b")


MODIFIERS = frozenset("""
new old older newer secondhand second-hand used brand little small big large long short tall wide
narrow round square tiny huge giant same other another good bad poor decent proper nice cheap
expensive pricey posh fancy rubbish rubbishy broken faulty dodgy spare extra main whole front back
top bottom side inner outer left right first second third last next previous electric electrical
manual digital smart wooden metal plastic glass stainless steel leather cotton woolen woollen
furry fluffy heavy light hard soft dark bright white black grey gray red blue green yellow pink
purple brown orange silver gold clear empty full wet dry hot cold warm cool clean dirty
""".split())


PARTICLES = frozenset("""
off on out up down back away apart over in into loose together around about through round
please again now then too also as well
""".split())


def _without_a_particle(phrase):
    words = phrase.split()
    while words and words[-1] in PARTICLES:
        words.pop()
    return " ".join(words)


def _a_thing_from(said, determiner_only=False):
    for match in re.finditer(
            r"\b(?:my|our|the|this|these|a|an)\s+([a-z][a-z'-]+(?:\s+[a-z][a-z'-]+){0,3})", said):
        words = match.group(1).split()
        while words and words[0] in MODIFIERS:
            words.pop(0)
        kept = []
        for word in words:
            if word in MODIFIERS or word in NOT_A_THING:
                break
            kept.append(word)
            if len(kept) == 2:
                break
        kept = _without_a_particle(" ".join(kept)).split()
        if kept:
            return " ".join(kept)
    if determiner_only:
        return ""
    words = re.findall(r"[a-z][a-z'-]+", said)
    run = []
    best = ""
    for word in words:
        if word in NOT_A_THING:
            if run:
                best = " ".join(run[-2:])
                run = []
            continue
        run.append(word)
    if run:
        best = " ".join(run[-2:])
    best = _without_a_particle(best.strip())
    if len(best) < 3 or not all(word.isalpha() for word in best.split()):
        return ""
    return best


CORRECTION = re.compile(
    r"\b(?:i mean|i meant|i mean't|sorry i mean|no i mean|rather than|not that,?|"
    r"i should have said|what i mean is)\b")


def _thing_named_in(text):
    text = str(text or "")
    mark = CORRECTION.search(text)
    if mark:
        corrected = _a_thing_from(text[mark.end():], determiner_only=True)
        if corrected:
            return corrected
    return _a_thing_from(text)


def _the_thing(read, said, memory):
    before = _the_line_before(memory)
    before_text = str((before or {}).get("text") or "") if isinstance(before, dict) else ""
    named_before = _thing_named_in(before_text) if before_text else ""
    back = REFERS_BACK.search(said)
    points_back = bool(back) and not A_DETERMINER.search(said[:back.start()])
    if points_back and named_before:
        return named_before
    mark = CORRECTION.search(said)
    if mark:
        corrected = _a_thing_from(said[mark.end():], determiner_only=True)
        if corrected:
            return corrected
    named_now = _a_thing_from(said, determiner_only=True)
    if named_now:
        return named_now
    if isinstance(read, dict):
        subject = str(read.get("subject") or "").strip().lower()
        if subject and subject not in NOT_A_THING:
            return subject
        for ent in read.get("entities") or ():
            if not isinstance(ent, dict):
                continue
            text = str(ent.get("text") or "").strip().lower()
            if text and text not in NOT_A_THING:
                return text
    before = _the_line_before(memory)
    if isinstance(before, dict):
        subject = str(before.get("subject") or "").strip().lower()
        if subject and subject not in NOT_A_THING:
            return subject
        for ent in before.get("entities") or ():
            if not isinstance(ent, dict):
                continue
            text = str(ent.get("text") or "").strip().lower()
            if text and text not in NOT_A_THING:
                return text
        named = _thing_named_in(str(before.get("text") or ""))
        if named:
            return named
    return ""


def before_text_from(memory):
    return str((_the_line_before(memory) or {}).get("text") or "")


def _the_line_before(memory):
    now = str((memory.get("understood") or {}).get("text") or "").strip().lower()
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    for turn in reversed(turns):
        said = str(turn.get("user") or "").strip()
        if said and said.lower() != now:
            return {"text": said}
    return None


LIVING = re.compile(
    r"\b(?:beehive|bee hive|hive|colony|nuc|bees|wormery|worms|compost|pond|aquarium|"
    r"fish tank|hens|chickens|quail|mushroom kit|starter|terrarium)\b")


NOT_AN_OBJECT = frozenset("""
hair hairs head face back neck shoulder shoulders knee knees leg legs foot feet arm arms hand hands
finger fingers thumb skin eye eyes ear ears tooth teeth mouth tongue jaw stomach tummy belly gut
chest cough breath voice sleep mood temper day days week weeks weekend month months year years
time life job work shift shifts money rent bill bills debt weight appetite headache head cold
toenail nails toothache backache stress anxiety energy patience brain memory
""".split())


OWNED_ANYWAY = re.compile(
    r"\b(?:the|my|our)\s+[a-z][a-z' -]{0,26}?\b(?:is|are|was|were|has|have|had|keeps|kept|"
    r"went|gone|goes|stopped|stops|broke|broken|won't|wont|doesn't|doesnt|isn't|isnt|smells?|"
    r"makes?|making|sounds?|leaks?|leaking|arrived|turned up)\b")


ON_THE_BODY = re.compile(
    r"\b(?:wounds?|cuts?|grazes?|grazed|burns?|scalds?|blisters?|bruises?|rashes?|sores?|spots?|"
    r"ulcers?|abscess|scar|scars|stitches|staples|sutures|tattoos?|piercings?|fillings?|"
    r"crowns?|dentures?|denture|retainers?|aligners?|implants?|bridges?|veneer|veneers|"
    r"dentist|gums?|tooth|teeth|stump|amputation|prosthes[ie]s|prosthetic|stoma|colostomy|"
    r"dressings?|bandages?|plasters?|splints?|casts?|wig|wigs|toupee|hairpiece|"
    r"injection|injections|insulin pen|catheter|drip|line|port|pacemaker|coil|implant)\b")


CLINICAL = re.compile(
    r"\b(?:tens|tens machine|tens unit|nebuliser|nebulizer|cpap|bipap|inhaler|spacer|"
    r"crutch|crutches|walking (?:frame|stick|aid)|zimmer|catheter|stoma|insulin|"
    r"blood pressure monitor|blood sugar|glucose meter|hearing aid|hearing aids|"
    r"compression (?:stocking|stockings|sleeve|sock|socks|tights)|"
    r"oxygen|oxygen concentrator|feeding tube|peg tube|syringe driver)\b")


PART_OF_SOMETHING = frozenset("""
head seal seals filter filters drawer lid cap hose belt blade blades tray element washer valve
aerator spout handle handles sole soles heel heels zip zipper button buttons strap buckle wick
filament plug plugs gasket bearing impeller pump thermostat cartridge cartridges hinge catch latch
knob dial flange nut bolt screw screws
""".split())


def _kind_from_the_owning_line(memory, thing, said=""):
    if not thing:
        return ""
    sources = [(memory or {}).get("understood") or {}, _the_line_before(memory) or {},
               {"text": said}]
    for source in sources:
        text = str(source.get("text") or "").lower() if isinstance(source, dict) else ""
        if thing not in text:
            continue
        if all(word in NOT_AN_OBJECT for word in thing.split()):
            continue
        if ("my " + thing in text or "our " + thing in text or GOT_IT.search(text)
                or OWNED_ANYWAY.search(text)):
            if LIVING.search(thing):
                return "living"
            if CLINICAL.search(thing):
                return "clinical"
            if ON_THE_BODY.search(thing):
                return ""
            return "bought"
    return ""


BOUGHT_GENERAL = {
    "figure": (
        "the number on the thing itself, or on the label or paperwork that came with it, is the "
        "one that decides it rather than the one in the advert",
        "the size and the make are what the figure follows from, so two of the same kind of thing "
        "can differ by a lot"),
    "reason": (
        "there are usually two or three common causes, and which one it is shows in when it "
        "happens and what changes with it",
        "the way to tell the causes apart is to change one thing at a time and watch what "
        "changes"),
}


def _known(kind, part):
    if (kind, part) in BY_KIND:
        return BY_KIND[(kind, part)]
    if kind in MADE:
        return GENERAL_BY_PART.get(part) or ()
    if kind == "bought":
        return BOUGHT_GENERAL.get(part) or ()
    return ()


def reply_for(text, memory=None, reply=""):
    if not fallback.is_a_hedge(reply):
        return None
    if fallback.in_a_safety_thread(memory or {}):
        return None
    said = str(text or "").lower()
    if not said.strip():
        return None
    if A_PERSON.search(said):
        return None
    if fallback._thread_is_about_the_body(memory or {}):
        return None
    read = (memory or {}).get("understood") if isinstance(memory, dict) else None
    read = read if isinstance(read, dict) else {}
    if (COOKING.search(said) or A_PURCHASE.search(said) or NUTRITION.search(said)
            or A_BUYING_NOW.search(before_text_from(memory or {}))):
        return None
    if ANIMAL_AS_A_SOURCE.search(said):
        return None
    thing = _the_thing(read, said, memory or {})
    if not thing:
        return None
    if ANIMAL_AS_A_SOURCE.search(thing):
        return None
    if A_PERSON.search(thing):
        return None
    kind = "part" if all(word in PART_OF_SOMETHING for word in thing.split()) else ""
    kind = kind or _kind_of(said) or _kind_of(thing)
    if not kind:
        before = _the_line_before(memory or {}) or {}
        kind = _kind_of(str((memory or {}).get("understood", {}).get("text") or ""))
        if not kind:
            kind = _kind_of(str(before.get("text") or ""))
    if not kind:
        kind = _kind_from_the_owning_line(memory or {}, thing, said)
    if not kind:
        return None
    part = _parts_of(said)
    if not part:
        return None
    if part not in HOLDS.get(kind, frozenset()):
        return None
    where = WHERE_IT_LIVES.get(kind)
    knowns = _known(kind, part)
    word = PART_WORD.get(part)
    tails = TAIL.get(part)
    if not where or not knowns or not word or not tails:
        return None
    options = tuple(
        "I can't check {word} for {dem} {thing}, sorry. What I can say is that {known}. "
        "{where} {tail}".format(
            word=word, dem=_that(thing), thing=thing, known=known, where=where, tail=tail)
        for known in knowns for tail in tails)
    return pick(options, read, said)
