import re

A_MOVING = re.compile(
    r"\b(?:exchange|interest|mortgage|savings|base|bank) ?rates?\b|"
    r"\brate of exchange\b|\bfuel prices?\b|\b(?:petrol|diesel) prices?\b|"
    r"\bprice of (?:petrol|diesel|fuel)\b|\bhow much is (?:petrol|diesel|fuel)\b", re.I)
MOVING_LINES = (
    "That figure is republished every day and two places rarely quote the same one, because each "
    "adds its own margin or terms on top: compare two of them and go with the one whose small "
    "print fits what you are actually doing, checking the date printed with the number.",
    "Nobody keeps that number in their head - it moves daily and the version printed next to it "
    "is the only one that counts. Read two offers rather than one, and add on the fee or the "
    "terms before you decide which is really cheaper.",
)
A_PRICE = re.compile(
    r"\bhow much\b|\bwhat(?:'s| is| does| would| will)?\b[^.?!]*\bcosts?\b|"
    r"\bcost of\b|\bprice of\b|\bprices?\b|\bcheaper\b|\bcheapest\b|\bset me back\b|"
    r"\bbudget for\b|\bgoing rate\b|\bthe rate for\b|\bwhat do you pay for\b", re.I)
NAME_ONLY_ASK = re.compile(
    r"^\s*(?:the\s+)?(?:price|cost)s?\s+(?:of|for)\b|\bgoing rate\b|\bthe rate for\b", re.I)
NOT_A_PRICE = re.compile(
    r"\bhow much\b[^.?!]{0,32}\b(?:weigh|weighs|weight|sleep|eat|drink|take|give|feed|exercise|"
    r"water|milk|protein|salt|sugar|fibre|calories|units|grams|ml|litres|paracetamol|ibuprofen|"
    r"is safe|are safe|is too much|is normal|is enough)\b|"
    r"\bhow much\b[^.?!]{0,20}\b(?:can|should|could) i\b", re.I)
A_REPEATED_SPEND = re.compile(
    r"\b(?:\d+|one|two|three|four|five|six|seven|twice|three times|four times|every|each)\b"
    r"[^.?!]{0,24}?\b(?:a|per|each|every)\s+(?:day|week|month)\b", re.I)
A_LONGER_SPAN = re.compile(
    r"\b(?:in|over|for|across)\s+a\s+year\b|\ba\s+year\b|\bper\s+year\b|\bannual(?:ly)?\b|"
    r"\bin\s+(?:twelve|12)\s+months\b", re.I)
ASKS_A_COST = re.compile(
    r"\bhow much\b|\bcosts?\b|\bcosting\b|\bspend\b|\bspent\b|\bafford\b|"
    r"\bexpensive\b|\bset me back\b|\bcome to\b|\bcomes to\b", re.I)
AN_AMOUNT_ALREADY = re.compile(
    r"[£$]|\b\d+\s*(?:p|pence|pounds?|quid|bucks|euros?)\b|\b(?:fiver|tenner|twenty)\b|"
    r"\b(?:one|two|three|four|five|six|seven|eight|nine|ten)\s+(?:pounds?|quid)\b", re.I)
A_COUNT_IN_A_SPAN = re.compile(
    r"\b(\d+|one|two|three|four|five|six|seven|twice|three times|four times|five times)\s*"
    r"(?:days?|times|nights?|lunches|cups?|pints?|cigarettes?|takeaways?|journeys?|trips?|"
    r"rides?|lessons?|bottles?|coffees?)?\s*(?:a|per|each|every)\s+(day|week|month)\b", re.I)
A_EVERY_SPAN = re.compile(r"\b(?:every|each)\s+(day|week|month)\b", re.I)
COUNT_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
               "twice": 2, "three times": 3, "four times": 4, "five times": 5}
A_YEAR = {"day": 365, "week": 52, "month": 12}
EXAMPLE = 5


def times_a_year(clean):
    if not ASKS_A_COST.search(clean):
        return None, None
    if AN_AMOUNT_ALREADY.search(clean):
        return None, None
    if not A_LONGER_SPAN.search(clean):
        return None, None
    found = A_COUNT_IN_A_SPAN.search(clean)
    if not found:
        plain = A_EVERY_SPAN.search(clean)
        if not plain:
            return None, None
        return A_YEAR[plain.group(1).lower()], " ".join(plain.group(0).split())
    said, span = found.group(1).lower(), found.group(2).lower()
    count = int(said) if said.isdigit() else COUNT_WORDS.get(said)
    if not count:
        return None, None
    return count * A_YEAR[span], " ".join(found.group(0).split())


def sum_lines(clean):
    times, said = times_a_year(clean)
    if not times:
        return None
    figure = times * EXAMPLE
    written = said[:1].upper() + said[1:]
    return (
        "{w} is {n:,} a year. Put your own price on one - £5 each is £{fig:,} - and that is the "
        "figure to weigh against cutting it back.".format(w=written, n=times, fig=figure),
        "{w} is {n:,} times a year, so put a price on one: at a fiver each that is £{fig:,}, "
        "which is what the habit really costs.".format(w=written, n=times, fig=figure),
    )


def a_sum_through_the_year(clean):
    return bool(times_a_year(clean)[0])

PRICE_LINES = (
    "There is no list price for that: what it comes to depends on the size of the job, the state "
    "of the thing and when you want it, so ask two firms to price the same description in writing "
    "and compare what each one leaves out rather than the total.",
    "The figure comes from a quote or a listing, not from me: get the same description from two "
    "places, in writing, and check what each one includes - the parts, the labour, the call-out "
    "and the VAT.",
)

A_RATE = re.compile(
    r"\b(?:parking|car ?park|to park|park there|entry|admission|tickets?|fares?|day pass|"
    r"week pass|season ticket|"
    r"membership|toll|ferry|crossing|per night|a night|per hour|per day|day rate|hourly rate)\b",
    re.I)
RATE_LINES = (
    "That is a published rate rather than a quote: whoever runs the place sets it, it moves with "
    "the day and the season, and a cap or a longer stay usually costs less per hour. Their own "
    "page or listing has today's, so ask what the whole stretch comes to rather than the headline "
    "figure.",
    "The headline rate is only half of it: an evening or weekend price, a day cap, a return or a "
    "longer booking often costs less than paying by the hour, and the operator's own page lists "
    "them all. Check today's figure there before you pay.",
)

A_WORTH = re.compile(
    r"\bworth it\b|\bworth the money\b|\bworth buying\b|\bworth the extra\b|"
    r"\bworth paying\b|\bworth the price\b|\bgood buy\b|\bis it worth\b", re.I)
A_REPAIR_OR_BUY = re.compile(
    r"\b(?:fix|fixes|fixing|fixed|mend|mends|mending|mended|repair|repairs|repairing|repaired|"
    r"service|services|servicing|serviced|replace|replaces|replacing|replacement|replaced|"
    r"new one|second hand|secondhand|refurb(?:ish|ished)?|upgrade|upgrading|claim|claims|"
    r"claiming|claimed|install|installs|installing|buy|buys|buying|bought|"
    r"worth the money|worth buying|good buy|worth paying|worth the price|"
    r"paying extra|pay extra)\b", re.I)
A_BROKEN_THING = re.compile(
    r"\b(?:broken|breaking|broke|not working|stopped working|gone wrong|last legs|leaking|"
    r"faulty|dead|dead as|knackered|worn out|on the blink|cracked|rusting|needs? a repair|"
    r"needs? fixing|needs? replacing|needs? a service|mend it|fix it|replace it|repair it)\b",
    re.I)


def not_about_one_owned_thing(clean):
    return not (A_REPAIR_OR_BUY.search(clean) or A_BROKEN_THING.search(clean))

WORTH_LINES = (
    "What decides it is the condition, what it would cost to put right and what the new one "
    "costs: if the repair comes to more than about half of new, it usually is not worth it. Get "
    "the repair cost in writing first, then compare that with the price of a new one.",
    "It earns its price when what it needs doing comes to less than replacing it, and a second "
    "one of the same age has its own faults. Ask for the repair cost in writing, and price the "
    "new one before you decide rather than after.",
)

A_CHOICE = re.compile(
    r"\bwhich is better\b|\bwhich one is better\b|\bbetter to (?:get|buy|go for)\b|"
    r"\bor should i\b|\bshould i (?:get|buy|go for)\b[^.?!]{0,40}\bor\b|\bvs\b|"
    r"\b(?:pick|choose|decide|select) between\b", re.I)
CHOICE_LINES = (
    "Both work for somebody, so it comes down to what you would miss if you had to give the other "
    "one back, and which of them fits the week you actually have. Write down what each one is "
    "for before you compare what they cost, and the one you have to keep justifying is usually "
    "the answer.",
    "The way to settle it is which one you would still be glad of in a year, and whether either "
    "of them brings a running cost with it - so list what you would use each one for, then "
    "compare the whole cost rather than the price on the ticket.",
)

A_DISTANCE = re.compile(
    r"\bhow far\b|\bmiles? from\b|\bmiles? to\b|\bhow long is the (?:drive|journey|walk)\b|"
    r"\bdistance (?:from|to|between)\b", re.I)
DISTANCE_LINES = (
    "The straight-line miles and the road miles are two different numbers, and the time bends "
    "with the hour you travel, so put both ends into a map app and read the route it gives: it "
    "carries the miles, the time and the way round the slow bit.",
    "For a journey by road that is a map app, and for one by train it is the operator's own "
    "planner: both give the miles or the connections for the hour you would actually go, which "
    "is the part a rough figure from anyone else gets wrong.",
)

A_DURATION = re.compile(
    r"\bhow long (?:does|do|will|would|should|until|before|after)\b|\bhow long until\b|"
    r"\btakes? how long\b|\bhow soon\b|"
    r"\bhow many (?:hours|days|weeks|months|years)\b[^.?!]{0,20}\b(?:does|do|will|until|"
    r"before|after|should i wait)\b", re.I)
BARE_DURATION = re.compile(
    r"^(?:and |so |but |ok |okay )?(?:how long|how soon)\b[\s\w]{0,24}?"
    r"\b(?:it|that|this|they|them|one)\b[\s\w]{0,10}?\??$", re.I)
A_QUEUE = re.compile(
    r"\b(?:claim|claims|application|apply|form|forms|paperwork|order|delivery|courier|"
    r"post|posting|post office|queue|backlog|repair|repairs|service|servicing|mot|"
    r"survey|surveyor|solicitor|conveyanc|completion|exchange of contracts|offer|"
    r"mortgage|valuation|passport|licence|license|visa|council|benefit|benefits|"
    r"universal credit|pip|esa|refund|return|returns|dispute|appeal|hearing|decision|"
    r"assessment|builder|builders|plasterer|electrician|plumber|joiner|installer|install|"
    r"installation|dispatch|boiler|house move|sale|sell|selling|buying|purchase|probate|"
    r"will|tenancy|landlord|deposit|dbs|background check|bank|payment|transfer|clearing|"
    r"money|clears|clearing|wait|waits|waiting)\b", re.I)


def NOT_A_QUEUE(text):
    if BARE_DURATION.search(text):
        return True
    if re.search(r"\b(?:how long|how soon) (?:do|should|shall|can|will) (?:i|we) "
                 r"(?:wait|hold|hang|leave|give|keep|sit)\b", text):
        return True
    return not A_QUEUE.search(text)


DURATION_LINES = (
    "How long that takes depends on the queue, how much there is to do and the time of year, so "
    "ask the body that runs it for their current wait and whether the date they give includes "
    "the slow part at the end - a range from them beats any single figure.",
    "The honest answer is a range: the size of it and how busy they are move it by weeks, so ask "
    "whoever handles it what they are running at now, and treat the earliest date they give as "
    "the best case rather than the promise.",
)

A_LOAD = re.compile(
    r"\b\d+\s*-?\s*amp\b|\bextension lead\b|\bplug socket\b|\bfuse\b|"
    r"\btripp(?:ed|ing)\b|\btrips?\b\s+(?:the\s+|a\s+|our\s+|my\s+|your\s+)?"
    r"(?:fuse|circuit|breaker|mcb|rcd|socket|supply|switch|electric\w*|mains|ring)\b|"
    r"\b(?:off|from|on|into)\s+(?:one|the same|a single)\s+(?:socket|plug|circuit|extension)\b",
    re.I)
LOAD_LINES = (
    "The labels settle it: the watts are printed on the base of each thing, and a 13-amp socket "
    "gives about 3,000 watts in total, so the sum is what counts rather than the number of "
    "plugs. Add up the labels and keep the total under that - a kettle or a heater on its own "
    "takes most of it.",
    "Add up the watts on the labels of everything that would be on at once and keep the total "
    "under about 3,000 for a 13-amp socket, because a heater or a kettle alone takes most of the "
    "headroom. The rating is usually moulded into the plug or the base, not on the box.",
)

A_FIT = re.compile(
    r"\b(?:will|would|does|do|can)\b[^?!]{0,30}\b(?:fit|fits)\b|"
    r"\b(?:work|works|go) with\b[^.?!]{0,20}\b(?:battery|charger|drill|hose|part|filter|"
    r"attachment|unit|set|kit)\b|"
    r"\bwhich\s+(?:size|model|part|one)\b[^?!]{0,20}\bdo i need\b|\bwhat size\b|"
    r"\bis (?:it|this|that) compatible\b", re.I)
FIT_LINES = (
    "The size and the model on the label decide it rather than the picture: the model number is "
    "usually on a plate underneath, in the manual or on the maker's page for it. Read that "
    "before anything is ordered, because the same name comes in more than one size.",
    "It is the measurements and the model number that settle it, and both are on the thing "
    "itself, so note them down and match them against the spec on the maker's own page for the "
    "part - that is where the fit is stated rather than guessed at.",
)

A_RULE = re.compile(
    r"\bam i allowed\b|\bare we allowed\b|\bis it legal\b|\bis that legal\b|\bdo i need (?:a |an |"
    r"permission|to )\b|\bcan i be made to\b|\bcan they make me\b|\bhave i got the right\b|"
    r"\bwhat are my rights\b|\bdo i have to\b|\bam i entitled\b|\bis it against the law\b|"
    r"\bcan my (?:landlord|employer|boss)\b", re.I)
NOT_A_RULE = re.compile(
    r"\b(?:uno|monopoly|chess|poker|scrabble|darts|snooker|board game|"
    r"bishop|knight|rook|pawn|checkmate|the pieces)\b", re.I)
A_DO_I_NEED = re.compile(r"\bdo i need (?:a |an |to )\b|\bdo i have to\b|\bdo we need to\b", re.I)
A_RULE_SUBJECT = re.compile(
    r"\b(?:licen[cs]e|licen[cs]ed|permit|permission|visa|insurance|insurer|mot\b|"
    r"tax|taxed|deposit|notice|contract|landlord|tenant|letting agent|employer|boss|\bhr\b|"
    r"council|council tax|hmrc|gov\.uk|government|court|probate|benefits?|universal credit|"
    r"housing benefit|claim|claiming|form|forms|declaration|statement|registration|register|"
    r"passport|inspection|consent|referral|prescription|legal|law|rights|entitled|mortgage|"
    r"solicitor|conveyanc\w*|certificate|crime number|vet\b|policy|warranty|guarantee|"
    r"refund|return it|duty|obliged|obligation)\b", re.I)


def not_a_bare_procedure(clean):
    return bool(A_DO_I_NEED.search(clean)) and not A_RULE_SUBJECT.search(clean)


def not_a_rule(clean):
    return bool(NOT_A_RULE.search(clean)) or not_a_bare_procedure(clean)
RULE_LINES = (
    "Whether that is allowed turns on the rules as they stand this year and on your own case, so "
    "the current wording decides it rather than what anyone has heard. GOV.UK has the national "
    "version and your council's site the local one, and the office that runs it will put the "
    "conditions for your situation in writing - keep that letter.",
    "It depends on what your own agreement says and on the version of the rules in force, and "
    "the gap between those two is usually the whole answer. The issuing office's own page has "
    "the current wording, and one call to them settles the case the page does not cover.",
)

A_STAT = re.compile(
    r"\bhow many (?:people|residents|households|of them|are there)\b|"
    r"\bwhat percentage\b|\bwhat proportion\b|"
    r"\bwhat(?:'s|s| is)?\s*(?:is\s+)?the population\b|\bpopulation of\b", re.I)
STAT_LINES = (
    "Figures like that come from whoever counts them, and the year and the boundary change the "
    "answer: \"the town\" and \"the wider area\" are two different numbers. The official "
    "statistics page or the council's own figures have the current one, with the year it is for "
    "printed beside it.",
    "That number moves every year and it depends where the line is drawn, so the body that "
    "publishes it is the one to quote: the national statistics site has it with the year, and "
    "the local council publishes its own for the area it covers.",
)

A_HOWTO = re.compile(
    r"\bhow (?:do|can|should|could|would) (?:i|you|we)\b|\bhow to\b|"
    r"\bbest way to\b|\bany (?:tips|advice) (?:for|on)\b|\bwhat should i do about\b|"
    r"\bwhere do i start\b|\bhow would you go about\b", re.I)
A_TROUBLE = re.compile(
    r"\b(?:stuck|stubborn|tight|seized|jammed|wedged|won'?t|wont|not working|stopped working|"
    r"broke|broken|leak|drip|damp|mould|mold|smell|stink|stain|crease|creak|squeak|squeal|"
    r"rattl|wobbl|vibrat|noisy|block|blocked|slow|stiff|rust|scratch|burn|fade|crack|chip|"
    r"snap|worn|tangled|knotted|fog|cloudy|flat|dead|flicker|trip|overflow|"
    r"keeps (?:going|coming|stopping|turning))", re.I)
A_PROCESS = re.compile(
    r"\b(?:will|probate|benefits?|universal credit|council tax|licence|license|permit|"
    r"passport|visa|tax return|self assessment|pension|redundancy|redundant|"
    r"apply|application|appeal|complain|complaint|refund|return|cancel|cancelling|"
    r"mortgage|insurance|insure|claim|registration|register|deregister|"
    r"loyalty|warranty|guarantee|bill|bills|direct debit|standing order|"
    r"switch|switching|comparison|quote|quotes|contract|agreement|tenancy|deposit|"
    r"moving house|house move|move house|solicitor|notary|deed|title|land registry)\b", re.I)
A_HOWTO_HAS_A_SHAPE = re.compile(
    A_TROUBLE.pattern + "|" + A_PROCESS.pattern, re.I)
NOT_A_HOWTO = re.compile(
    r"\b(?:feel|feeling|feelings|anxious|anxiety|depressed|depression|panic|grief|grieving|"
    r"lonely|loneliness|scared|worried|worry|miscarriage|divorce|separating)\b|"
    r"\b(?:tell|talk to|speak to|say to|ask|apologise to|apologize to|comfort|support|help|"
    r"explain to|break it to|be there for|deal with|do about)\b[^?!]{0,24}"
    r"\b(?:my|his|her|their)\s+(?:mum|mom|dad|son|daughter|wife|husband|partner|boyfriend|"
    r"girlfriend|friend|brother|sister|boss|child|kid|parents|family)\b", re.I)
def NOT_A_HOW_TO(text):
    return bool(NOT_A_HOWTO.search(text)) or not A_HOWTO_HAS_A_SHAPE.search(text)


HOWTO_LINES = (
    "The first steps are the same for most of these: work out what is actually causing it before "
    "you treat what you can see, change one thing at a time, and give each change a day before "
    "the next so you know which one worked. Write down what you tried and when.",
    "Do it in the order that costs least first: what you already have in the cupboard or the "
    "shed, then the cheap part or product, then the trade. Before you buy anything, check the "
    "manual or the maker's page for the exact model, because it says what is safe on that one "
    "and what is not.",
)

A_RECORD = re.compile(
    r"\b(?:deposit|deeds?|title plan|land registry|warrant(?:y|ies)|guarantee|receipt|invoice|"
    r"policy|insurance|cover note|booking|reservation|tenancy agreement|assured shorthold|"
    r"certificate|statement|reference number|reference|paperwork|the small print|terms|"
    r"boundary|boundaries)\b",
    re.I)
NOT_A_RECORD = re.compile(
    r"\b(?:whats|what is|what are|what does|what do|meaning of)\s+(?:a|an)\b|"
    r"\bwhat\s+(?:does|do|is|are|did|can)\s+(?:the|this|that)\b[^.?!]{0,40}"
    r"\b(?:mean|means|meaning|stand for|definition)\b|"
    r"\b(?:how do i|how to|should i (?:take out|buy|get)|worth (?:getting|it)|"
    r"cheapest|cancel my|switch my|compare)\b|"
    r"\bwhats? the point of\b|\bwhat is the point of\b|\bsick of\b|\bfed up\b|"
    r"\bdrowning in\b|\bcan'?t be (?:bothered|arsed)\b", re.I)

A_LOOSE_KIND_WORD = re.compile(
    r"\b(?:policy|policies|statement|statements|terms|paperwork|insurance|boundar(?:y|ies)|"
    r"contract|agreement)\b", re.I)
THEIR_OWN_PAPER = re.compile(r"\b(?:my|our|his|her|their|your|yours|ours|theirs)\b", re.I)
A_NAMED_DOCUMENT = re.compile(
    r"\b(?:terms and conditions|terms of (?:the|my|our|their|his|her|your)\b|"
    r"insurance polic(?:y|ies)|policy wording|policy document|policy schedule|"
    r"bank statement|statement of (?:the|my|our|their)\b|"
    r"tenancy agreement|assured shorthold|contract of employment|the small print)\b", re.I)


def _not_a_record(said):
    if NOT_A_RECORD.search(said):
        return True
    if A_NAMED_DOCUMENT.search(said) or THEIR_OWN_PAPER.search(said):
        return False
    return bool(A_LOOSE_KIND_WORD.search(said))
RECORD_LINES = (
    "What settles that is the entry itself rather than the general rule - the date on it, the "
    "terms that were in force then, and the name it is in. The office or firm that holds it can "
    "read it back to you, so ask for it in writing and quote the reference on it: the answer that "
    "counts is the one on paper, not the one given over the phone.",
    "That turns on the wording of the document, not on what is usually done: what it says, what "
    "date it came into force and whose name is on it. Whoever issued it keeps the record, and the "
    "one thing worth doing first is asking them to confirm in writing what their copy says.",
    "Nobody can answer that from the description of it, because the answer is in the paperwork - "
    "the date, the terms and the name on it. Ask the body holding it for the entry in writing with "
    "the reference on it, and keep what they send: a written answer is the one that can be relied "
    "on later.",
)

NOT_HERE = re.compile(
    r"\b(?:999|911|112|111|ambulance|a&e|emergency|bleeding|not breathing|chest pain|"
    r"overdose|suicide|kill myself|end my life|self harm|"
    r"died|death|funeral|buried|cremation|passed away|grief|grieving)\b", re.I)
ASKS_SOMETHING = re.compile(
    r"\b(?:how|whats?|what's|which|when|where|who|why|can|could|should|would|will|is|are|was|"
    r"were|do|does|did|am|has|have|had|may|might|shall)\b", re.I)

KINDS = (
    ("choice", A_CHOICE, CHOICE_LINES, None),
    ("howto", A_HOWTO, HOWTO_LINES, NOT_A_HOW_TO),
    ("worth", A_WORTH, WORTH_LINES, not_about_one_owned_thing),
    ("distance", A_DISTANCE, DISTANCE_LINES, None),
    ("load", A_LOAD, LOAD_LINES, None),
    ("fit", A_FIT, FIT_LINES, None),
    ("rule", A_RULE, RULE_LINES, not_a_rule),
    ("figure", A_STAT, STAT_LINES, None),
    ("moving", A_MOVING, MOVING_LINES, None),
    ("rate", A_RATE, RATE_LINES, None),
    ("price", A_PRICE, PRICE_LINES, (NOT_A_PRICE, a_sum_through_the_year)),
    ("duration", A_DURATION, DURATION_LINES, NOT_A_QUEUE),
    ("record", A_RECORD, RECORD_LINES, _not_a_record),
)


A_POINTER = re.compile(
    r"\ba quick search\b|\bsearch online\b|\bsearching for it\b|\bquick look\b|"
    r"\ba search\b|\blook (?:it|that) up\b|\bwikipedia\b|\bprice comparison\b|"
    r"\bpaste what it says\b|"
    r"\b(?:official|seller'?s|their|its|the)\b[^.?!]{0,20}?\b(?:site|page|listing|app)\b"
    r"[^.?!]{0,24}?\b(?:will|has|have)\b", re.I)


def names_only_a_page(reply):
    said = " ".join(str(reply or "").lower().split())
    return bool(said) and bool(A_POINTER.search(said))


THE_PAPER_ITSELF = re.compile(
    r"\bthe (?:receipt|deed|deeds|wording|document|documents|paperwork|certificate|policy|"
    r"contract|agreement|statement|invoice|booking|label|manual|terms)\b|"
    r"\b(?:date|name|reference|number) on it\b", re.I)


def names_the_paper(reply):
    said = " ".join(str(reply or "").lower().split())
    return bool(said) and bool(THE_PAPER_ITSELF.search(said))


def reads(text):
    clean = " ".join(str(text or "").lower().split())
    if not clean or NOT_HERE.search(clean):
        return None, None
    if not (ASKS_SOMETHING.search(clean) or NAME_ONLY_ASK.search(clean)):
        return None, None
    for kind, pattern, lines, guard in WORRY_SHAPES + KINDS + PROCEDURE_SHAPES:
        if pattern.search(clean):
            if guard:
                guards = guard if isinstance(guard, tuple) else (guard,)
                if any(g(clean) if callable(g) else g.search(clean) for g in guards):
                    continue
            return kind, lines
    return None, None


def pool(clean, memory=None):
    summed = sum_lines(clean)
    if summed:
        return summed
    return reads(clean)[1]


A_NEED_TO = re.compile(r"\bdo (?:i|we) need (?:to |a |an )\b", re.I)
NEED_TO_LINES = (
    "Depends what it is for. Say the thing you are doing and I will tell you what it takes - and "
    "where a rule rather than common sense decides it, who to ask.",
    "It turns on the thing itself and on what it is for - a trip, a form, a job and a pan of "
    "something all want different things. Tell me which it is and I will give you the short "
    "version, rather than the general one that fits none of them.",
    "That depends on the thing itself and what you are doing with it. Say which and I will tell "
    "you, rather than guess at it.",
)
PROCEDURE_SHAPES = (("needto", A_NEED_TO, NEED_TO_LINES, None),)

A_WORRY_ASK = re.compile(
    r"\bdo (?:i|we) (?:need|have) to\b[^.?!]{0,24}\b(?:worry|panick?\w*|stress\w*|be anxious|"
    r"be scared|be (?:worried|afraid)|fret)\b", re.I)
WORRY_LINES = (
    "Worry about what? Tell me what is coming up and I will say whether there is anything to do "
    "about it, because most of what people brace for turns out to be somebody else's rule.",
    "Say what it is and I will tell you straight whether there is anything to do about it. If "
    "there is, it is usually one form or one call, and if there is not, you can stop carrying it.",
)
WORRY_SHAPES = (("worried", A_WORRY_ASK, WORRY_LINES, None),)
