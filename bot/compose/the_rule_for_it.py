import re

PRICE_RULE = (
    "What a figure like that turns on is which one it is, where you buy it and the day, so two "
    "or three sellers compared all-in will beat any one number you see. The current figures are "
    "on their own pages, and bring them back and I will work out what they come to a month.",
    "A job is priced by the quote, not by a list: the same job gets two or three quotes on the "
    "same spec, in writing, and that is the number worth comparing. A thing on a shelf is the "
    "seller's own page, all in with delivery - tell me what you find and I will do the sums.",
    "Prices move by exactly what you are buying and by where, so one number from one seller is "
    "not an answer to it. Two sellers, what it comes to all in, and then the part I am good at: "
    "what it leaves you a month.",
)
PRICE_ASK = re.compile(
    r"\bhow much (?:is|are|was|were|does|do|did|would|will|should|might)\b[^?.!,]{0,40}?"
    r"\b(?:cost|costs|charge|charge for|worth|set me back|come to|pay|paying|spend)\b"
    r"|\bhow much (?:should|shall|ought to|do|would)\b[^?.!,]{0,24}?\b(?:pay|spend|be paying)\b"
    r"|\bwhat (?:does|do|did|would|will|should)\b[^?.!,]{0,36}?\bcost\b"
    r"|\bwhat(?:'s|s)? the (?:cost|price|going rate|damage|ballpark)\b"
    r"|\bwhat about the cost\b|\bthe cost of\b|\bprice of (?:a|an|the)\b"
    r"|\bhow much (?:is|are) (?:a|an|the)\b"
    r"|\bis (?:that|it|this) (?:a )?(?:fair|good|normal|about right) (?:price|money)\b"
    r"|\bis (?:that|it|this) (?:too )?(?:expensive|dear|cheap)\b"
    r"|\bcan i get (?:it|that|one) (?:any )?cheaper\b"
    r"|\bwhat would that cost\b|\bhow much would that (?:be|cost)\b"
    r"|\bhow much (?:would|will|might|could) (?:a|an|the|one)\b[^?.!]{0,30}?\bbe\b"
    r"|\bhow much (?:is|are|was|were)\b(?!\s*(?:enough|too\b|left|more|of\b|in\b|there\b|"
    r"it\b|that\b|this\b|going\b))",
    re.I)
PRICE_VERDICT = re.compile(
    r"\b(?:is|are|was|were|will|would|does|do)\b(?!\s*(?:you|u)\b)[^?.!,]{0,40}?"
    r"\b(?:expensive|pricey|costly|spenny|overpriced)\b"
    r"|\b(?:is|are|was|were)\b[^?.!,]{0,40}?\b(?:too|so|very|quite|really|that|a bit|dead|"
    r"bloody)\s+dear\b"
    r"|\bdear(?:er)?\s+than\b"
    r"|\b(?:is|are)\s+(?!you\b|she\b|he\b|they\b|we\b|i\b)(?:[a-z']+\s+){1,3}(?:too\s+)?"
    r"dear\b", re.I)
A_DEAR_AS_A_NAME = re.compile(
    r"\b(?:my|your|our|his|her|their|the|a|an)\s+dear\b", re.I)
A_FARE_OR_A_TICKET = re.compile(
    r"\b(?:trains?|flights?|buses|coach|ferry|tubes?|parking|park|"
    r"tickets?|entry|admission|petrol|fuel|diesel|delivery|shipping|car hire|hire car)\b", re.I)
FARE_PRICE_RULE = (
    "The day is what sets that one, not the seller: the same trip off-peak on a Tuesday can be a "
    "fraction of the peak on a Monday, and booking further ahead is nearly always cheaper than "
    "booking late. The operator's own page has today's figure - bring it back and I will work out "
    "what it comes to for you.",
    "Booked far enough ahead, a fare is a different number from the one a week before, so compare "
    "the same journey on the day you actually go rather than the first figure you see. Tell me "
    "the route and the dates and I will do the sums against the money you have.",
    "That price turns on the day, the time and how far ahead you book, and on a fare it is the "
    "time of day that moves it most. The figure is on the operator's own page; bring it back "
    "with what you can spend and I will tell you whether it stacks up.",
)
A_CAB_OR_A_LIFT = re.compile(
    r"\b(?:taxis?|cabs?|minicabs?|private hire|black cab|ubers?|lyft|a cab|a taxi)\b", re.I)
CAB_FARE_RULE = (
    "A cab is metered, so it is the clock and the traffic that set the price, not the seller: the "
    "same trip at 8 in the morning and at 11 at night are different numbers. Ring the firm with "
    "the pickup, the drop-off and the time and ask for a fixed quote - most will give one, and "
    "that quote is the number worth comparing.",
    "A taxi fare is the meter, so the time of day and the traffic move it; there is nothing to "
    "book further ahead. Ask two firms for a fixed price for your trip and compare those, and ask "
    "whether the quote covers waiting and the return.",
)
PRICE_VERDICT_RULE = (
    "Whether that is dear depends on which one and where from: the same thing is a different "
    "number in two places and on two days. Two prices, all in, is the comparison - bring them "
    "back and I will tell you which one leaves you better off at the end of the month.",
    "There is no one price for it. What it comes to turns on the size, the seller and the day, so "
    "the useful thing is two quotes for the same thing with everything included. Tell me the two "
    "figures and I will work out what each leaves you.",
    "That is impossible to call from one number: what it costs moves with which one you pick, "
    "where you get it and when. Find two prices for the same thing, all in, and the difference "
    "between them is the part worth acting on.",
)
A_AN_OCCASION = re.compile(
    r"\b(?:weddings?|funerals?|christenings?|baptisms?|namings?|birthdays?|birthday party|"
    r"part(?:y|ies)|anniversar(?:y|ies)|honeymoons?|stag do|stag night|hen do|hen night|"
    r"graduations?|receptions?|eating out|eating away|meals out|meal out|dinner out|"
    r"restaurants?|takeaways?|catering|caterers?)\b", re.I)
OCCASION_PRICE_RULE = (
    "That one is priced by the head and by the day rather than by the seller: how many people, "
    "which day, and what is inside the price - the meal, the drinks, the extras. Two quotes on "
    "the same numbers is the only comparison worth making; tell me yours and I will do the sums.",
    "What it comes to turns on the count and the date, so fix the guest list and the day first, "
    "then ask two or three places for the same thing all in. Bring the figures back and I will "
    "work out what it leaves you a month.",
    "Every one of these is quoted per person and moves with the day of the week, so one figure "
    "from one place says little on its own. The same count and the same extras asked of two "
    "places is the comparison - and the venue's own page has today's numbers.",
)

NOT_ABOUT_A_PRICE = re.compile(
    r"\bmy (?:account|balance|bill|invoice|statement|payment|direct debit|order|parcel|quote|"
    r"refund|payslip|wage|salary|pension|mortgage|rent|card|loan|overdraft|credit)\b"
    r"|\b(?:up front|deposit|instal?ments?|per month|a month|a week|per hour|pay off|paid off|overdue)\b",
    re.I)

AMOUNT_FEEDING_RULE = (
    "That one is arithmetic rather than knowledge: a portion each, times how many you are "
    "feeding, and a little more if it is the only dish. The pack, the butcher or the recipe you "
    "are using carries the per-head figure - give me the count and I will turn it into a total.",
    "Work it from the number of people, not from the whole: what one person gets, multiplied, "
    "and a bit on top if it is the only thing being served. Tell me how many and I will do the "
    "sum with you.",
    "How much you need is per head, and whether it is the main thing or one of several decides "
    "which per-head figure: the pack or the recipe has that half. Bring me the numbers and I "
    "will work out what to buy.",
)
AMOUNT_COVER_RULE = (
    "That one is a coverage sum rather than a fact: how far one pack, tin or scoop goes, times "
    "the size of the job. How far it goes is on the label, and the size of the job is yours to "
    "measure - tell me it and I will work out how many you need.",
    "How much you need comes from how much one of them covers and how big the job is, so start "
    "with the coverage figure on the label and then it is arithmetic. Give me the measurements "
    "and I will do the working.",
    "The label says what one pack covers and the rest is a multiplication: that, times the area "
    "or the number of loads you are doing. Tell me the two numbers and I will turn them into how "
    "much to buy.",
)
AMOUNT_ASK = re.compile(
    r"\bhow (?:much|many)\b[^?.!]{0,40}?\b(?:do|should|would|will|might|can|shall)\b[^?.!]{0,12}?"
    r"\b(?:i|we|you) (?:need|use|buy|get|make|cook|add|put|give|take|order|hire)\b"
    r"|\bhow (?:much|many) (?:do|does) (?:i|we|you) need\b"
    r"|\bhow (?:much|many)\b[^?.!]{0,30}?\bfor (?:two|three|four|five|six|seven|eight|nine|ten|"
    r"twelve|twenty|\d+)\b"
    r"|\bhow (?:heavy|big|large|thick) should\b"
    r"|\bhow many (?:portions|servings|heads)\b"
    r"|\bhow much per (?:person|head|portion)\b|\bper (?:head|person)\b"
    r"|\bhow much\b[^?.!]{0,28}?\b(?:goes|goes in|goes into)\b",
    re.I)
FEEDING = re.compile(
    r"\b(?:people|person|persons|head|heads|portion|portions|serving|servings|guests?|kids?|"
    r"children|adults?|family|each|everyone|for (?:two|three|four|five|six|seven|eight|nine|ten|"
    r"twelve|twenty|\d+))\b"
    r"|\b(?:eat|eating|feed|feeding|dinner|lunch|supper|tea|buffet|barbecue|bbq)\b"
    r"|\b(?:meat|chicken|beef|pork|lamb|mince|rice|pasta|potato|potatoes|veg|vegetables?|"
    r"salad|soup|sauce|gravy|stuffing|bread|pastry|cheese|milk|cream|fruit|berries|cake|"
    r"biscuits?|pudding|dessert|starter|curry|stew|lasagne|lasagna|pie|quiche|sausages?|bacon|"
    r"eggs?|fish|salmon|prawns|prawn|prawns|cheese|butter|flour|sugar|oats|yoghurt|yogurt|"
    r"beans?|lentils?|chickpeas|nuts?|spuds|chips|roast|joint|turkey|duck|ham|tofu|hummus)\b",
    re.I)
MATERIAL = re.compile(
    r"\b(?:paint|primer|undercoat|gloss|emulsion|wallpaper|paste|tiles?|grout|adhesive|"
    r"sealant|filler|plaster|cement|mortar|sand|gravel|bark|chippings|soil|compost|mulch|"
    r"feed|fertiliser|fertilizer|weedkiller|seeds?|grass seed|oil|varnish|stain|lacquer|"
    r"thinner|white spirit|bleach|detergent|washing powder|liquid|tablets|conditioner|"
    r"softener|disinfectant|cleaner|shampoo|foil|cling film|bin bags?|kitchen roll|cat litter|"
    r"litter|screws?|nails?|rawlplugs|dowels?|cable|wire|rope|string|tape)\b", re.I)
MONEY_ON_A_JOB = re.compile(
    r"\b(?:up front|deposit|pay|paid|paying|money|afford|budget|cost|costs|price|[£$€])\b", re.I)

STILL_GOOD_RULE = (
    "Whether it is still good turns on two things: how long it has been and how cold it stayed. "
    "The date on the pack is the line - past it, or warm for hours, it goes - and I will say what "
    "I would do with the details: which it is, and when it went in.",
    "Two things decide that, and neither is on my side of the screen: how long, and how it has "
    "been kept. The pack's own date is the limit; inside it and cold all along is fine, and past "
    "it or out for half a day is not worth the risk. The date on it is the one to read, and tell "
    "me that and when it went in and I will say what I would do.",
    "That is a keeping question rather than a recipe one: the date to go by is the one on the "
    "pack, and how it has been kept since decides the rest. Tell me when it went in and how it "
    "has been stored, and I will say what I would do.",
)
GONE_OFF_ASK = re.compile(
    r"\bgone off\b|\bout of date\b|\b(?:use by|best before|sell by)\b", re.I)
STILL_ASK = re.compile(
    r"\bstill\b[^?.!]{0,40}?\b(?:ok|okay|fine|safe|alright|good|eat|eaten|use|using|keep|have|"
    r"drink|give|serve|cook|reheat|freeze|edible)\b"
    r"|\b(?:it|that|this|they|these)\b[^?.!]{0,30}?\bstill\b"
    r"|\bgone off\b|\bout of date\b|\bpast (?:its|the|their) (?:date|use by|best before)\b"
    r"|\buse by\b|\bbest before\b"
    r"|\bhow long (?:does|do|will|can|would)\b[^?.!]{0,30}?\b(?:keep|last|stay good|"
    r"stay fresh)\b",
    re.I)
KEEP_ASK = re.compile(
    r"\bhow long (?:does|do|will|can|would)\b[^?.!]{0,30}?\b(?:keep|stay fresh|stay good)\b",
    re.I)
OFF_ASK = re.compile(
    r"\bis it (?:ok|okay|fine|safe|alright|good) (?:to|for)\b"
    r"|\bcan i (?:eat|use|keep|drink|have|give|serve|freeze|reheat|cook)\b"
    r"|\bis (?:it|that|this) (?:ok|okay|fine|safe|alright)\b"
    r"|\bwill (?:it|that|they|these) be (?:ok|okay|fine|alright|safe)\b", re.I)
NOT_A_KEEPING_QUESTION = re.compile(
    r"\b(?:medicine|medicines|tablets?|pills?|capsules?|dose|doses|dosage|paracetamol|ibuprofen|"
    r"calpol|antibiotics?|inhaler|insulin|syrup|prescription|allergy|allergic)\b", re.I)
KEEPING_HAS_NO_DATE = re.compile(
    r"\b(?:freeze|freezes|freezer|freezers|freezing|frozen|thaw|thaws|thawed|thawing|defrost|"
    r"defrosted|refreeze|re-freeze)\b"
    r"|\b(?:i|we) (?:made|make|baked|cooked|roasted|prepared|whipped up)\b", re.I)
ABOUT_A_PERSON_OR_AN_ANIMAL = re.compile(
    r"\b(?:baby|babies|infant|newborn|toddler|child|children|boy|girl|son|daughter|kid|kids|"
    r"pup|puppy|kitten|dog|cat|months? old|years? old|weigh|weighs|weight|stone|kg|lbs|"
    r"pounds)\b", re.I)
FOOD_OR_PACK = re.compile(
    r"\b(?:chicken|beef|pork|lamb|turkey|duck|ham|bacon|mince|sausage|sausages|fish|salmon|"
    r"prawns|shellfish|rice|pasta|noodles|potato|potatoes|veg|vegetables?|salad|soup|sauce|"
    r"gravy|bread|toast|pastry|cheese|milk|cream|yoghurt|yogurt|butter|eggs?|fruit|berries|"
    r"cake|quiche|pie|pudding|leftovers?|takeaway|curry|stew|lasagne|lasagna|sandwich|meat|"
    r"food|pack|packet|tin|jar|bottle|carton|use by|best before|date on it|label)\b", re.I)


TIME_RULE = (
    "A time is a rate times a size: minutes per kilo, hours per coat, days a chapter. Whoever "
    "sets the rate - the recipe, the course, the trade - says what it is, and give me your size "
    "and I will do the multiplication.",
    "How long it takes comes from how big the job is and how fast it goes, so the number to find "
    "is the rate rather than the total, and the rate is published - on the pack, in the recipe, "
    "or by whoever does the work. Tell me the two figures and I will work out the time.",
    "Time is the part I can work out but cannot know: the size of the job, times the rate it goes "
    "at. Bring me the rate from whoever does it and the size of yours, and I will turn it into a "
    "finish time you can plan round.",
)
TIME_ASK = re.compile(
    r"\bhow long (?:will|would|does|do|should|shall|can|could|might|must)\b[^?.!]{0,44}?"
    r"\b(?:take|takes|last|lasts|go in|sit|rest|stay in|be in|preheat|defrost|chill|set|rise|"
    r"prove|boil|simmer|roast|cook|bake|fry|grill|steam|soak|marinate|dry|run|walk|drive|train|"
    r"learn|build|fit|paint|decorate)\b"
    r"|\bhow long (?:is|would be) (?:it|that|this)\b[^?.!]{0,30}?\b(?:before|until|to)\b"
    r"|\bhow long (?:until|before)\b[^?.!]{0,40}?\b(?:done|ready|cooked|finished|it is|its)\b",
    re.I)
TIME_NOT_THIS = re.compile(
    r"\b(?:ago|been|queue|waiting list|on hold|does it keep|how long have)\b", re.I)
A_COOKING_TIME = re.compile(
    r"\b(?:roast|roasting|cook|cooking|bake|baking|boil|boiling|simmer|fry|frying|grill|grilling|"
    r"steam|steaming|poach|oven|go in|goes in|be in|sit in|stay in|rest|barbecue|bbq|"
    r"air fryer|slow cooker|pressure cooker|pan)\b", re.I)
A_FOOD = re.compile(
    r"\b(?:lamb|beef|chicken|turkey|duck|goose|pork|ham|gammon|bacon|sausages?|mince|steak|"
    r"joint|bird|casserole|stew|pie|tart|cake|sponge|bread|loaf|scones?|biscuits?|pudding|"
    r"potatoes?|chips?|veg|vegetables?|carrots?|parsnips?|onions?|rice|pasta|lasagne|lasagna|"
    r"eggs?|fish|salmon|trout|cod|prawns?|tofu|halloumi|mushrooms?|tomatoes?|peppers?"
    r"|dough|batter|pastry)\b", re.I)


def the_rule_for_it(clean, repaired=None):
    for line in (clean, repaired):
        said = " ".join(str(line or "").lower().split())
        if not said:
            continue
        if NOT_A_KEEPING_QUESTION.search(said):
            return None
        if ABOUT_A_PERSON_OR_AN_ANIMAL.search(said):
            return None
        if not KEEPING_HAS_NO_DATE.search(said):
            if KEEP_ASK.search(said) or GONE_OFF_ASK.search(said):
                return STILL_GOOD_RULE
            if STILL_ASK.search(said) and FOOD_OR_PACK.search(said):
                return STILL_GOOD_RULE
            if OFF_ASK.search(said) and FOOD_OR_PACK.search(said):
                return STILL_GOOD_RULE
        if AMOUNT_ASK.search(said) and not MONEY_ON_A_JOB.search(said):
            if MATERIAL.search(said) and not FEEDING.search(said):
                return AMOUNT_COVER_RULE
            if FEEDING.search(said):
                return AMOUNT_FEEDING_RULE
        if (PRICE_VERDICT.search(said) and not NOT_ABOUT_A_PRICE.search(said)
                and not A_DEAR_AS_A_NAME.search(said)):
            if A_CAB_OR_A_LIFT.search(said):
                return CAB_FARE_RULE
            if A_AN_OCCASION.search(said):
                return OCCASION_PRICE_RULE
            if A_FARE_OR_A_TICKET.search(said):
                return FARE_PRICE_RULE
            return PRICE_VERDICT_RULE
        if PRICE_ASK.search(said) and not NOT_ABOUT_A_PRICE.search(said):
            if A_CAB_OR_A_LIFT.search(said):
                return CAB_FARE_RULE
            if A_AN_OCCASION.search(said):
                return OCCASION_PRICE_RULE
            return PRICE_RULE
        if TIME_ASK.search(said) and not TIME_NOT_THIS.search(said):
            if A_COOKING_TIME.search(said) and A_FOOD.search(said):
                return COOKING_TIME_RULE
            return TIME_RULE
    return None


A_CARE_WORD = re.compile(
    r"\b(?:operation|surgery|theatre|hospital|hospitalised|ward|vets?|vet's|recovery|recovering"
    r"|rehab|treatment|chemo|chemotherapy|dialysis|scans?|consultant|nurse|nurses"
    r"|doctor|doctors|gp|111|a&e|icu|hospice|palliative|dementia|carer|carers"
    r"|in labour|due date|pregnant|pregnancy)\b")


A_MONEY_WORD = re.compile(
    r"\b(?:credit card|credit cards|card|cards|apr|loan|loans|mortgage|mortgages|overdraft"
    r"|debt|debts|interest|repayments?|overpay|overpaying|arrears|rent arrears|invoice"
    r"|bailiffs?|iva|ccj|payday|minimum payment|balance)\b")


COOKING_TIME_RULE = (
    "Oven times go by weight and heat: minutes per 500g at a set temperature, and both are on the "
    "pack or in the recipe. Tell me the weight and the heat and I will work out the clock time for "
    "you.",
    "That one is a minutes-per-500g job at a set heat, and the figure for the thing you are "
    "cooking is on the pack, the recipe or the book. How heavy is it, and what heat are you "
    "using?",
    "The weight and the oven heat decide it, and the rate for that joint or bird is written down "
    "somewhere you already have - the pack, the recipe, or the shop's own guide. Bring me the "
    "weight and I will do the arithmetic.",
)
RULE_POOLS = (PRICE_RULE, PRICE_VERDICT_RULE, FARE_PRICE_RULE, CAB_FARE_RULE,
              OCCASION_PRICE_RULE,
              AMOUNT_FEEDING_RULE,
              AMOUNT_COVER_RULE, STILL_GOOD_RULE, COOKING_TIME_RULE, TIME_RULE)
RULE_HEADS = tuple(line[:40] for pool in RULE_POOLS for line in pool)
