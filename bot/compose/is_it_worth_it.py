import re

from . import fallback, pick

FIX_OR_REPLACE = re.compile(
    r"\bworth (?:fix(?:ing|in)|mend(?:ing|in)|repair(?:ing|in)|servic(?:ing|in)|descal(?:ing|in)|"
    r"clean(?:ing|in)|a service|the service|replac(?:ing|in)(?: it| them)?|"
    r"get(?:ting|tin) it (?:fixed|repaired|serviced|seen to|looked at)|a repair|the repair)\b")
A_TRADE = re.compile(
    r"\bworth (?:getting someone (?:in|out|round)|getting a (?:plumber|electrician|builder|"
    r"roofer|joiner|painter|decorator|gardener|handyman|mechanic)|getting it (?:done|put in)|"
    r"having someone (?:in|out|round))\b"
    r"|\bworth (?:getting|having) (?:my|our|the) \w+ (?:rotated|serviced|checked|done|"
    r"replaced|cleaned|fixed)\b"
    r"|\b(?:a|the) (?:main )?(?:dealer|garage|mechanic)\b[^.?]{0,20}\bworth\b")
A_SUGGESTIONS = re.compile(
    r"\b(?:whats?|what is|what are|anything|something)\b[^.?]{0,20}\bworth "
    r"(?:doing|seeing|a look|the trip)\b|\bworth (?:doing|seeing) there\b")
A_VISIT = re.compile(
    r"\bworth (?:visiting|a visit|the trip|the journey|the drive|going to see|seeing)\b")
PLACE_WORD = re.compile(
    r"\b(?:castle|cathedral|minster|abbey|church|museum|gallery|exhibition|show|tour|"
    r"zoo|safari park|theme park|aquarium|baths|spa|gardens?|park|palace|tower|ruins?|"
    r"monument|attraction|distillery|brewery|stadium|theatre|theater|opera|festival)\b")
A_PURCHASE = re.compile(
    r"\bworth (?:it|the money|the price|buy(?:ing|in)|get(?:ting|tin)|"
    r"paying (?:more|that|extra) for|the extra)\b")
A_SMALL_THING = re.compile(
    r"\b(?:kettle|toaster|iron|hoover|vacuum|microwave|phone|mobile|laptop|tablet|ipad|"
    r"printer|blender|air fryer|coffee machine|hair dryer|hairdryer|straighteners|fan|heater|"
    r"keyboard|monitor|headphones|earbuds|watch|remote|shredder|mower|strimmer|treadmill)\b")
A_NAMED_THING = re.compile(
    r"\bworth (?:get(?:ting|tin)|buy(?:ing|in)|having|paying [^.?]{0,14}for|a|an) "
    r"(?:a|an|the|some) "
    r"(?!new\b|another\b|one\b|it\b)\w+")
A_REPLACE_WORD = re.compile(
    r"\b(?:a new one|new one instead|replace|replacing|get another|bin it|throw it out)\b")
A_APPLIANCE = re.compile(
    r"\b(?:boiler|washing machine|dishwasher|tumble dryer|fridge|freezer|oven|hob|"
    r"central heating|radiators?|immersion|water tank|car|van|motorbike|bike|bicycle|roof|"
    r"(?<!rice )(?<!slow )cooker|"
    r"gutter|window|door|fence|drive|patio|damp|shower|toilet|tap|sink|chimney)\b")
A_MONEY = re.compile(r"£\s?\d[\d,]*(?:\.\d{2})?|\b\d[\d,]{2,}(?:\.\d{2})?\b")
A_RESALE_THING = re.compile(
    r"\b(?:car|van|motorhome|campervan|caravan|bike|bicycle|motorbike|scooter|moped|"
    r"guitar|violin|cello|piano|keyboard|drum ?kit|amp|amplifier|watch|jewellery|jewelry|"
    r"ring|gold|silver|coins?|antiques?|furniture|sofa|table|wardrobe|"
    r"console|playstation|xbox|nintendo|switch|camera|lens|drone|telescope|"
    r"sewing machine|mower|ride on|tractor|boat|kayak|canoe|surfboard|"
    r"phone|iphone|laptop|macbook|tablet|ipad|pc|desktop|gpu|graphics card|"
    r"tools?|drill|saw|welder|compressor|generator)\b")
A_MINE = re.compile(r"\b(?:my|our)\b")
A_USED_MARK = re.compile(
    r"\b(?:miles|mileage|second ?hand|used|pre-owned|reg|registration|\d{4} reg|"
    r"\d+ years old|year old|old|vintage|antique)\b")
A_SALE_ASK = re.compile(
    r"\b(?:about right|too cheap|too much|too little|fair price|a fair|that fair|is that fair|"
    r"good price|a good|should i (?:accept|take|sell)|worth)\b")
A_NEW_PRICE = re.compile(
    r"\b(?:paying|pay|buy|buying|get|getting|a new one|new|brand new|extra|more|deal|offer|"
    r"quote|quotes|someone|trade|garage|dealer|repair|fix|service|servicing)\b")

AN_APPEAL = re.compile(
    r"\bworth (?:appealing|challenging|disputing|arguing|taking it further|fighting)\b")

THEIR_OWN_LIFE = re.compile(
    r"\b(?:job|jobs|offer|career|course|degree|uni|university|college|apprenticeship|"
    r"relationship|marriage|him|her|them|us|we|we're|being friends|staying friends|"
    r"moving|move house|emigrat\w*|quitting|going part time|full time|office|"
    r"redundancy|settlement|watching|reading|the book|the film|the series|netflix)\b")
A_LIVING_THING = re.compile(
    r"\b(?:goldfish|fish|dog|puppy|cat|kitten|rabbit|hamster|guinea pig|horse|pony|pet|"
    r"reptile|lizard|snake)\b")
STAND_DOWN = re.compile(
    r"\b(?:afford|cant afford|can't afford|owe|owed|debt|debts|arrears|loan|overdraft|"
    r"bleed\w*|bloods?|pain|ache\w*|sore|lump|rash|symptom\w*|doctor|gp|hospital|111|999|"
    r"scan|x-?ray|surgery|pregnant|baby|pension|annuity|retire\w*|im \d\d already)\b")

A_FIX_REPLY = (
    "Whether it is worth fixing comes down to the quote against what a replacement would cost, "
    "and a garage, a repair shop or the engineer for that trade will give you that figure "
    "for nothing. Ask them what else is "
    "likely to go in the next year or two as well - that is usually what decides it. How old is "
    "it, and what else has gone wrong lately?",
    "That one is the quote against a new one, and nobody can call it without the quote. Every "
    "garage, repair shop or engineer for that trade will price the work for free, and it is "
    "worth asking what they would "
    "check next while it is in. What would you do with it if you did not fix it?",
)
A_SMALL_THING_REPLY = (
    "These are the ones where the two sums sit close together: a new one off the shelf against "
    "the part or the cleaner and an hour of your own time. The shop's page has the new price, and "
    "the maker's page or a repair video for that exact model names what the part is. How old is "
    "it, and does it still do the job apart from that?",
    "Nothing here can price either side of that, and for something this size the two prices are "
    "usually nearer than people expect: the shelf price of a new one against the part and an "
    "hour of your own time. The shop's page has the one; the maker's page or a parts site has "
    "the other. What is it doing wrong?",
)
A_DAY_OUT_REPLY = (
    "I cannot see what is on near you, so the listings for the day are the first stop - the "
    "venue's own page has the times and whether it needs booking, and the newest reviews say "
    "whether people thought it was worth the trip. What sort of day are you after - a walk, "
    "something indoors, or food?",
    "Nothing here can see what is on there, and a guess at a name would be worthless. Start from "
    "what is on that day and check each place's own page for the price and the hours; the recent "
    "reviews are what tell you if it was worth the trip. Outside or indoors?",
)
A_TRADE_REPLY = (
    "That comes down to the quotes: two or three of them, in writing, for the same job, and what "
    "each one leaves out. Ask what is not included as well as what is, since that is where the "
    "cheap quote earns its money back. How big is the job?",
    "Nobody here can price work in your area, and one quote is a price rather than a market. Two "
    "or three written quotes for the same job, and the same question to each about what they would "
    "not do, tells you what it is worth. What needs doing?",
)
A_VISIT_REPLY = (
    "Only you can weigh that, and it comes down to the ticket price against how long you would "
    "stay. The place's own page has the price and the opening times, and the newest reviews are "
    "the ones that say how long people actually spend inside. What else is on the list that day?",
    "That is the price against the time, and nothing here can see either. Its own page carries "
    "the ticket price and the hours; the recent reviews say whether people were in and out in an "
    "hour. Are you going for the place itself, or to fill a day?",
)
A_PURCHASE_REPLY = (
    "Whether it is worth it comes down to the price against how much you would use it, and that "
    "part is yours. The shop's or the maker's page has the price and the spec; reviews from the "
    "last few months are the ones that say what it is like once the newness wears off. What would "
    "you use it for most?",
    "Nobody can price that for you from here. What decides it is the price against the use: its "
    "own page has the figure, and the recent reviews are where the faults show up. How often "
    "would you use it?",
)
A_VALUATION_REPLY = (
    "What a thing like that is worth is set by the ones that actually sold, not the ones still "
    "up for sale: condition, age and whatever needs doing all move it, and sold or completed "
    "listings for the same model are the figures that count, with a dealer's trade-in price as "
    "the other end of it. What is it, and what sort of state is it in?",
    "That figure is a market rather than a fact, so the ones that sold are what answers it - the "
    "same model, close to the same condition, on the sold or completed listings, and a second "
    "source such as a dealer's trade-in offer to check it against. What condition is it in?",
)
AN_APPEAL_REPLY = (
    "There is little to lose but the time, and the letter itself says how to ask for a review and "
    "by when - that date is the thing to find first. Citizens Advice will go through the ground "
    "you have for free, and they are quicker than the appeal is. What reason did they give?",
    "That is usually worth the letter it takes, and the decision letter says how to challenge it "
    "and by when. Citizens Advice or the scheme named at the bottom of the letter will check "
    "whether you have a ground for it, free. What did they say the reason was?",
)


A_TRIP = re.compile(
    r"\b(?:trip|holiday|weekend away|day out|visiting|on our way|travel(?:l)?ing to|"
    r"staying in|booked (?:a|the)|half term|bank holiday|\b(?:in|to) [a-z]+ for (?:a|the) "
    r"(?:week|weekend|few days|fortnight|day)\b|\b(?:going|off) to [a-z]+ (?:next|this) week\b"
    r"|\b(?:weekend|week|few days|day|break|holiday|time) (?:in|at) [a-z]"
    r"|\b(?:think(?:ing)? about|fancy|planning) (?:a|the) (?:trip|weekend|visit|day out)"
    r")")
A_GOING = re.compile(
    r"\b(?:go|goes|going|went|head(?:ing)?|off|fly|flying|drive|driving|travel\w*|get) to "
    r"(?:the |a |my |our )?([a-z][a-z']*)")
GOING_ANYWAY = frozenset((
    "the", "a", "my", "our", "work", "bed", "school", "college", "uni", "town", "shop", "shops",
    "supermarket", "gym", "bank", "loo", "toilet", "pub", "doctor", "doctors", "dentist", "dentists",
    "hospital", "surgery", "pharmacy", "chemist", "tip", "dump", "office", "vets", "vet", "park",
    "post", "library", "council", "court", "airport", "station", "bus", "train", "sleep", "home",
    "sleep", "it", "them", "hell", "potty", "bath", "shower", "kitchen", "garage", "garden",
    "loft", "attic", "cellar", "skip", "bin", "bins", "charity", "car", "van", "motorway",
))


A_TROUBLE_THREAD = re.compile(
    r"\b(?:marriage|on the rocks|fell out|not speaking|row(?:ed)? with|split up|divorce|"
    r"relationship|cheating|affair|he left|she left|walked out|last legs)\b")
A_BODY_THREAD = re.compile(
    r"\b(?:back|knee|hip|shoulder|ankle|wrist|neck|spine|leg|arm|foot|stomach|chest|tooth|"
    r"teeth|blood|skin|eye|ear|throat|joint)\b[^.?]{0,24}"
    r"\b(?:hurt\w*|ache\w*|sore|pain\w*|keeps? going|bad|injur\w*|stiff|swollen|ill|"
    r"infection|broke\w*)\b")
A_DEAL_THREAD = re.compile(
    r"\b(?:tariff|supplier|energy|switch(?:ing)? (?:supplier|tariff|deal)|fixed for two years|"
    r"pension|annuity|retire\w*|isa|savings account|mortgage deal)\b")
A_STUDY = re.compile(
    r"\b(?:degree|uni|university|masters|phd|doctorate|course|courses|college|apprenticeship|"
    r"tuition|fees|a level|a levels|night class|night school|qualification|diploma|student)\b")
A_PAID_PERSON = re.compile(
    r"\bworth (?:getting|having|seeing|using) (?:a|an|the) (?:personal )?(?:trainer|coach|tutor|"
    r"cleaner|accountant|lawyer|solicitor|dentist|plumber|electrician|carer|nanny|"
    r"childminder|therapist|counsellor)\b")
NOT_AN_ASK = re.compile(
    r"^\s*(?:(?:it|is|was|itnt|isnt|isn t|wasnt|this|that|really|still|even|then|though|just|"
    r"life)\s+)*worth (?:it|the (?:bother|effort|pain|hassle)|anything)\s*[.!]?$")
A_REPORT = re.compile(
    r"\b(?:says?|said|reckons|thinks|told me)\b[^.?]{0,30}\bworth\b|\bnot worth\b")


def _a_destination(said):
    for word in A_GOING.findall(said):
        if word not in GOING_ANYWAY and len(word) > 2:
            return word
    return ""


def _a_trip_in_the_thread(memory):
    turns = [t for t in ((memory or {}).get("turns") or []) if isinstance(t, dict)]
    said = " ".join(str(t.get("user") or "") for t in turns[-4:]).lower()
    return bool(A_TRIP.search(said))


def _the_thread(memory, back=2):
    turns = [t for t in ((memory or {}).get("turns") or []) if isinstance(t, dict)]
    return " ".join(str(t.get("user") or "") for t in turns[-back:]).lower()


def _is_it_worth_it(text, memory, reply):
    if not reply or not fallback.is_a_hedge(reply):
        return None
    said = " ".join(str(text or "").lower().split())
    if not said or not A_SALE_ASK.search(said) or len(said.split()) > 12:
        return None
    if STAND_DOWN.search(said):
        return None
    if (A_MONEY.search(said) and not A_NEW_PRICE.search(said)
            and not A_STUDY.search(said + " " + _the_thread(memory))
            and (A_RESALE_THING.search(said)
                 or A_RESALE_THING.search(_the_thread(memory)))):
        return pick(A_VALUATION_REPLY, memory, said)
    if THEIR_OWN_LIFE.search(said):
        return None
    if A_STUDY.search(said + " " + _the_thread(memory)) and not A_RESALE_THING.search(said):
        return None
    if A_LIVING_THING.search(said) or A_PAID_PERSON.search(said) or NOT_AN_ASK.match(said) or A_REPORT.search(said):
        return None
    around = _the_thread(memory)
    if (A_TROUBLE_THREAD.search(around) or A_BODY_THREAD.search(around)
            or A_DEAL_THREAD.search(around)):
        return None
    if fallback.in_a_safety_thread(memory):
        return None
    if (A_MONEY.search(said) and not A_NEW_PRICE.search(said)
            and not A_STUDY.search(said + " " + _the_thread(memory))
            and (A_MINE.search(said) or A_USED_MARK.search(said))):
        return pick(A_VALUATION_REPLY, memory, said)
    if A_TRADE.search(said):
        return pick(A_TRADE_REPLY, memory, said)
    reads_thread = not A_NAMED_THING.search(said)
    small = A_SMALL_THING.search(said) or (reads_thread and A_SMALL_THING.search(around))
    appliance = A_APPLIANCE.search(said) or (reads_thread and A_APPLIANCE.search(around))
    if (small or appliance) and (FIX_OR_REPLACE.search(said) or A_PURCHASE.search(said)
                                 or A_REPLACE_WORD.search(said)):
        return pick(A_SMALL_THING_REPLY if small else A_FIX_REPLY, memory, said)
    if FIX_OR_REPLACE.search(said):
        return pick(A_FIX_REPLY, memory, said)
    if A_TRADE.search(said):
        return pick(A_TRADE_REPLY, memory, said)
    if AN_APPEAL.search(said):
        return pick(AN_APPEAL_REPLY, memory, said)
    if A_SUGGESTIONS.search(said):
        return pick(A_DAY_OUT_REPLY, memory, said)
    a_place = (A_VISIT.search(said) or PLACE_WORD.search(said)
               or _a_trip_in_the_thread(memory)
               or (reads_thread and (PLACE_WORD.search(around) or _a_destination(around))))
    if a_place:
        return pick(A_VISIT_REPLY, memory, said)
    if A_PURCHASE.search(said):
        return pick(A_PURCHASE_REPLY, memory, said)
    return None

A_FAULT_ALREADY_SAID = re.compile(
    r"\b(?:furred|scaled|limescale|broken|stopped|stopping|keeps (?:stopping|cutting)|cutting out|"
    r"leaking|leaks|dripping|due (?:a|its) service|due a mot|making a noise|noisy|worn|worn out|"
    r"faulty|patchy|not working|won't|wont|doesn't|doesnt|died|dead|stiff|sticking|squeaking)\b")
LAST_ASK = re.compile(r"\s+(?:What needs doing|What is it doing wrong|How big is the job|"
                      r"What is it doing|What sort of day are you after[^?]*|Outside or indoors|"
                      r"How often would you use it)\?$")


def _with_what_they_said(reply, memory, said):
    if not reply:
        return reply
    before = " ".join(str(t.get("user") or "") for t in (memory.get("turns") or [])[-2:]
                      if isinstance(t, dict)).lower()
    if A_FAULT_ALREADY_SAID.search(said + " " + before):
        stripped = LAST_ASK.sub("", reply)
        if stripped and stripped != reply and stripped.endswith("."):
            return stripped
    return reply


def is_it_worth_it(text, memory, reply):
    said = " ".join(str(text or "").lower().split())
    return _with_what_they_said(_is_it_worth_it(text, memory, reply), memory, said)
