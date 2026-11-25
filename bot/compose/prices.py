
import re

PRICE_ASK = re.compile(
    r"\bwhat\s+(?:do|does|did|would|will|should|might)\b[^?.!,]{0,36}?\bcost"
    r"|\bwhat(?:'s|s)?\s+(?:the\s+)?(?:cost|price|going\s+rate|damage|ballpark)\b"
    r"|\bhow\s+much\s+(?:does|do|would|will|should|might|can)\b[^?.!,]{0,36}?"
    r"\b(?:cost|charge|set\s+me\s+back|come\s+to)\b"
    r"|\bhow\s+(?:much|expensive)\s+(?:is|are|was|were)\b"
    r"|\bhow\s+much\s+(?:should|shall|ought\s+to)\b[^?.!,]{0,24}?\b(?:spend|pay)\b"
    r"|\bhow\s+much\s+(?:do|would|will)\s+(?:i|we|you)\s+(?:need\s+to\s+)?"
    r"(?:spend|pay|budget|expect)\b"
    r"|\bhow\s+much\s+for\s+(?:a|an|one|the)\b"
    r"|\b(?:fair|normal|reasonable|typical|sensible|going|right)\s+(?:price|rate|money|cost)\b"
    r"|\bhow\s+much\b[^?.!,]{0,16}\b(?:roughly|in\s+total|altogether|all\s+in)\b"
    r"|\b(?:roughly|about)\s+how\s+much\b")

PRICE_ASK_HEADLESS = re.compile(
    r"^(?:and\s+|but\s+)?(?:ow\s+much|much)\s+(?:is|are|was|were|do|does|would)\b")

PRICE_OF_A_JOB = (
    "I can't price a job from here, sorry - it comes down to who does it and what they find when "
    "they open it up. Two quotes will give you a real range, and I can help you weigh them up.",
    "No figure from me on a job like that, sorry: it is a quote rather than a price list. Ring "
    "two firms and compare what each one covers, not just the total.",
)
A_JOB_JUDGED = (
    "A quote is only normal against another one: ring a second firm for the same job and compare "
    "what each one covers, not just the total, because who does it and what they find when they "
    "open it up is why two figures for the same job come out apart.",
    "What tells you whether that figure is normal is a second quote for the same job, in writing, "
    "compared on what each one includes rather than the total alone. The range moves with who does "
    "it and what they find, so the second quote is the only real test of the first.",
)
JOB_WORDS = frozenset("""
plumber plumbing builder builders decorator decorating electrician electrics joiner carpenter
plasterer tiler roofer handyman mechanic garage servicing fitted fitting installation install
labour quote quotes quoted repair repairs service gardener locksmith removals surveyor mot
fix fixing fixed mend mending rewire rewiring replumb
""".split())

PRICE_OF_A_THING = (
    "What decides it is the same thing priced in more than one place, and what each one includes: "
    "two or three quotes for the same job tell you whether a figure is normal. Today's prices move "
    "with where you are, so I can't see them from here.",
    "Two or three places, the same thing, and compare what each one includes rather than the total "
    "alone - that is what answers whether a price is fair. The figures themselves move with where "
    "you are and when you go, so they are not mine to see.",
)

PRICE_JUDGEMENT = re.compile(
    r"\bis\s+(?:that|this|it)\s+(?:about\s+)?(?:fair|normal|reasonable|right|about\s+right|"
    r"steep|a\s+lot|too\s+(?:much|dear|expensive))\b")

A_FAIRNESS_JUDGEMENT = re.compile(
    r"\b(?:fair|normal|reasonable|typical|sensible|going|right|steep|good|ok|decent)\s+"
    r"(?:price|prices|rate|rates|quote|quotation|cost|money|fee|charge)\b"
    r"|\b(?:that|this|it)\s+(?:about\s+)?right\b[^?.!]{0,14}\b(?:price|pay|paid|charge)\b")
MONEY_JUDGEMENT = re.compile(
    r"\b(?:is|are|isn'?t|aren'?t|was|were)\s+(?:that|this|it|they|those|these)"
    r"(?:\s+[a-z']+){0,2}\s+(?:so|very|really|too|quite|pretty)?\s*"
    r"(?:expensive|pricey|dear|overpriced|costly|cheap|good\s+value)\b"
    r"|\b(?:that|this|it|they|those|these)\s+(?:sounds|seems|looks)\s+(?:so\s+|very\s+|really\s+)?"
    r"(?:expensive|pricey|dear|steep|a\s+lot|overpriced)\b"
    r"|\b(?:expensive|pricey|cheap)\s+(?:to|for)\s+(?:fix|repair|mend|replace|service|run|insure|"
    r"install|fit|clean|heat)\b"
    r"|(?:[\u00a3$\u20ac]\s?\d+|\b\d+\s?(?:pounds?|quid|euros?|dollars?|bucks))\s+"
    r"(?:a\s+lot|too\s+much|expensive|steep)\b")
A_MONEY_CUE = re.compile(
    r"[\u00a3$\u20ac]|\b\d{2,}\b|\b(?:quid|quotes?|quoted|charged|charges?|price|prices|"
    r"cost|costs|bill|invoice|fee|fees|paid|pay)\b")

FOOD_SAID_BEFORE = re.compile(
    r"\b(?:flour|salt|sugar|bread|loaf|loaves|dough|batter|yeast|rice|pasta|butter|milk|eggs?|"
    r"cheese|mince|meat|chicken|beef|pork|lamb|fish|potato(?:es)?|onions?|carrots?|tomato(?:es)?|"
    r"vegetables?|stock|oats|noodles|lentils|beans|yoghurt|yogurt|sauce|spices?|pepper|garlic|"
    r"cake|biscuits?|pastry|porridge|soup|curry|roast|recipe|oven|bake|baking|loaf tin)\b")
A_PRICE_WORD = re.compile(
    r"\b(?:cost|costs|price|prices|priced|charge|charges|charged|quid|cheapest|expensive|cheaper|"
    r"pound|pounds|dollars?|euros?|fee|bill)\b|[\u00a3$\u20ac]")

NOT_A_PRICE = re.compile(
    r"\b(?:dose|dosage|ml|millilitres?|mg|tablets?|capsules?|spoons?|teaspoons?|calpol|"
    r"paracetamol|ibuprofen|nurofen|medicine|medication|painkillers|insulin|vitamin\s+[a-z])\b"
    r"|\bhow\s+much\s+(?:longer|time|sleep|salt|sugar|fibre|protein|water|sun|light|noise|"
    r"space|of)\b"
    r"|\bhow\s+(?:much|many)\s+(?:is|are|of)\s+(?:a|an|one|two|\d+)?\s*"
    r"(?:grams?|grammes?|kilos?|ounces?|cups?|tablespoons?|handfuls?|portions?|servings?)\b"
    r"\s*(?:[?.!]|$)"
    r"|\b(?:rice|pasta|mince|potato(?:es)?|meat|chicken|cheese|flour|sugar|butter|milk|"
    r"lentils|beans|oats|noodles|batter|yoghurt|yogurt)\b[^?.!,]{0,18}\b(?:each|per\s+person|"
    r"per\s+head|for\s+(?:two|three|four|five|six|seven|eight|\d+))\b"
    r"|\bfeed(?:ing)?\b[^?.!,]{0,30}\b(?:family|families|kids|children|household|of us|"
    r"for us|four|five)\b"
    r"|\bwhat (?:does|do) (?:a|the) (?:week|month)(?:'s)? (?:food|shop|groceries|shopping)\b"
    r"|\b(?:should|shall|can|could|do|does)\b[^?.!,]{0,24}\b(?:save|saving|savings|"
    r"put\s+(?:away|by|aside)|overpay|pay\s+off|pay\s+down)\b"
    r"|\bis\s+(?:that|this|it)\s+(?:about\s+)?(?:fair|right)\s+(?:on|of|to|for|that)\b"
    r"|\bfair\s+enough\b"
    r"|\b(?:you|u)\s+charge\b")


BALANCE_ASK = re.compile(
    r"\bhow\s+much\s+(?:is|are|was|were|have|has)\b[^?.!,]{0,32}?\b(?:left|remaining)\b"
    r"|\bhow\s+much\s+(?:is|are|was|were)\s+(?:on|in)\s+(?:my|our|the|your|their)\b"
    r"|\b(?:left|remaining)\s+(?:on|in)\s+(?:my|our|the|your)\b"
    r"|\bmoney\s+(?:left|remaining)\b")
BALANCE_CARRIER = re.compile(
    r"\b(?:card|cards|voucher|vouchers|account|balance|wallet|gift|pass|pot|points|credit)\b")


def _a_balance_ask(clean):
    return bool(BALANCE_ASK.search(clean) and BALANCE_CARRIER.search(clean))


A_BUDGET_ASK = re.compile(
    r"\b(?:is|would|will)\b[^?.!,]{0,14}?(?:[\u00a3$\u20ac]\s?)?\d[\d,]*(?:\.\d+)?\s*"
    r"(?:a|per|/)\s*(?:month|week|fortnight|year)\b[^?.!,]{0,28}"
    r"\b(?:enough|doable|affordable|liveable|livable|realistic|feasible|manageable|possible|"
    r"ok|okay|alright)\b"
    r"|\b(?:is|would|will)\s+(?:it|that|this)\s+(?:be\s+)?(?:doable|affordable|enough|realistic|"
    r"manageable|feasible)\b[^?.!,]{0,14}?(?:[\u00a3$\u20ac]\s?)?\d[\d,]*\s*"
    r"(?:a|per)\s*(?:month|week|fortnight|year)\b"
    r"|\b(?:is|would|will)\b[^?.!,]{0,14}?\d+(?:\.\d+)?\s?k\b[^?.!,]{0,28}"
    r"\b(?:enough|doable|affordable|liveable|livable|realistic|feasible|manageable)\b"
    r"|\bcan\s+(?:i|we|you)\s+(?:do\s+(?:it|this|that)|live|manage|afford|survive|cope|get\s+by)"
    r"\b[^?.!,]{0,20}?\d[\d,]*\s*(?:a|per)\s*(?:month|week|fortnight|year|day)\b"
    r"|\blive\s+on\s+(?:[\u00a3$\u20ac]\s?)?\d[\d,]*\s*(?:a|per)\s*(?:week|month|year)\b"
    r"|\benough\s+to\s+live\s+on\b"
    r"|\bget\s+by\s+on\s+(?:[\u00a3$\u20ac]\s?)?\d[\d,]*\s*(?:a|per)\s*(?:week|month)\b")

WORTH_AN_AMOUNT = re.compile(
    r"\bworth\s+(?:[\u00a3$\u20ac]\s?\d{2,}|\d+(?:\.\d+)?\s*(?:pounds?|quid|euros?|dollars?|bucks)\b"
    r"|\d{3,}\b)"
    r"|\bworth\s+(?:the|that|this|its|their|his)\s+(?:price|cost)\b")
WORTH_IT = re.compile(
    r"\b(?:are|is|was|were)\s+(?:they|those|these|it|that|this)\s+worth\s+it\b")
A_BARE_BUDGET_JUDGEMENT = re.compile(
    r"\b(?:is|would|will)\s+(?:that|this|it)\s+(?:be\s+)?(?:doable|affordable|realistic|enough|"
    r"manageable|feasible|possible|ok|okay|alright)\b"
    r"|\b(?:is|would|will)\s+(?:[\u00a3$\u20ac]\s?)?\d[\d,]*\s+(?:be\s+)?(?:doable|"
    r"affordable|enough|realistic|manageable|feasible|possible)\b")
A_MONEY_NEARBY = re.compile(
    r"[\u00a3$\u20ac]|\b\d{3,}\b|\b(?:money|quid|price|prices|cost|costs|pay|paid|paying|"
    r"pounds?|dollars?|euros?|bucks|cheaper|cheap|expensive|value)\b")

A_BUDGET_IS_THEIR_OWN_SUM = (
    "Housing, council tax and energy are the three that decide whether a month stretches, and the "
    "first two are fixed for the year - your council's site has your band and what it comes to. "
    "Add those, take them off the figure, and what is left is what has to cover food and travel. "
    "I can't see your bills from here, so tell me if the rent is already inside that figure.",
    "Most of a month goes on housing, council tax, energy and food. The first three are written "
    "down somewhere - the band is on your council's site and the energy figure is on the bill - "
    "and food you can judge from one week's shop. Put those against it and the rest is "
    "arithmetic; the bills are the part I can't see, so I can't do that sum from here.")


def _bounded(phrase):
    return re.compile(r"(?<![a-z0-9])" + re.escape(phrase) + r"(?![a-z0-9])")


def _has(clean, phrases):
    return any(_bounded(phrase).search(clean) for phrase in phrases)


def the_price_reply(clean, phrases, before, options):
    if NOT_A_PRICE.search(clean) or _a_balance_ask(clean):
        return None
    if before and FOOD_SAID_BEFORE.search(before) and not A_PRICE_WORD.search(clean):
        return None
    if A_BUDGET_ASK.search(clean) or (A_BARE_BUDGET_JUDGEMENT.search(clean)
                                     and A_MONEY_NEARBY.search(before or "")):
        return A_BUDGET_IS_THEIR_OWN_SUM
    judged = bool(MONEY_JUDGEMENT.search(clean) or PRICE_JUDGEMENT.search(clean)
                  or A_FAIRNESS_JUDGEMENT.search(clean))
    worth = bool(WORTH_AN_AMOUNT.search(clean)) or bool(
        WORTH_IT.search(clean)
        and (A_MONEY_NEARBY.search(clean) or A_MONEY_NEARBY.search(before or "")))
    asked = (_has(clean, phrases) or PRICE_ASK.search(clean) or worth
             or PRICE_ASK_HEADLESS.match(clean)
             or (judged and (A_MONEY_CUE.search(clean) or A_MONEY_CUE.search(before)
                             or MONEY_JUDGEMENT.search(clean))))
    if not asked:
        return None
    if _has(clean, JOB_WORDS) or (judged and _has(before or "", JOB_WORDS)):
        return A_JOB_JUDGED if judged else PRICE_OF_A_JOB
    if judged or worth:
        return PRICE_OF_A_THING
    return options
