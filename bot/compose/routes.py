import re

INSURANCE_WORD = re.compile(
    r"\b(?:insurance|insurer|insured|insure|insures|policy|policies|excess|excesses|claim|"
    r"claims|cover note)\b")
TERMS_THING = re.compile(
    r"\b(?:insurance|policy|cover note|pass|railcard|ticket|tickets|warranty|guarantee|"
    r"membership|subscription|tariff|contract|lease|tenancy|terms|small print|conditions|"
    r"excess|excesses|deposit|exclusions|breakdown|breakdown cover|recovery|roadside|contents "
    r"cover|gadget cover|extended warranty)\b")
PRICE_THING = re.compile(
    r"\b(?:price|prices|rate|rates|cost|costs|booking|room|rooms|hotel|holiday|package|deal|"
    r"hire|fee|fees|quote|breakfast|meals?|parking|wifi|transfer|transfers|extras?|tax|taxes|"
    r"vat|service charge|delivery|postage and packing|p&p)\b")
INCLUDED_ASK = re.compile(
    r"\b(?:is|are|was|were|does|do)\b[^?]{0,35}\b(?:include|includes|included|extra|"
    r"free with|come with|comes with)\b")

COVERED_PHRASE = re.compile(
    r"\b(?:am i|are we|are they|is it|is that|is this|is my|is our|is the|is that phone|"
    r"are my)\b[^?]{0,30}\bcovered\b")
TERMS_ASK = re.compile(
    r"\b(?:cover|covers|covered|include|includes|included|excluded|excludes|apply|applies|"
    r"count|counts|valid|honour|honoured|pay out|payout|work|works|worked|accepted|accept|"
    r"any use|use it|use on)\b")

WORKING_OUT = re.compile(r"\bwork(?:s|ed|ing)?\s+out\b")

ALLOWED_ASK = re.compile(
    r"\b(?:is|are|was|were|am i|are we|can i|can we|could i|may i)\b[^?]{0,30}"
    r"\b(?:allowed|permitted|legal|against the rules)\b")
TAKE_ON = re.compile(
    r"\b(?:can|could|may|am i allowed to|are we allowed to)\s+(?:i\s+|we\s+)?(?:take|bring|carry|"
    r"pack|board with)\b[^?]{0,60}\b(?:on|onto|into|in|aboard)\b")

TAKE_TO = re.compile(
    r"\b(?:can|could|may)\s+(?:i|we)\s+(?:bring|take|carry)\b[^?]{0,60}\bto\b")

NEEDED_THING = re.compile(
    r"\b(?:licen[cs]e|licen[cs]es|licen[cs]ing|licen[cs]ed|permit|permits|visa|visas|register|"
    r"registration|registered|certificate|certification|medical|inspection|qualification|"
    r"qualifications|background check|dbs check|crhb|health and safety|passport|passports)\b")
NEEDED_ASK = re.compile(
    r"\b(?:need|needs|needed|require|requires|required|have to|has to|must|renew|renewing|"
    r"speed up|speed it up|expedite|fast track|pay extra|pay more)\b")

AGREEMENT_WORD = re.compile(
    r"\b(?:tenancy|tenant|lease|landlord|letting agent|contract|membership|gym|subscription|"
    r"phone|mobile|broadband|internet|insurance|policy|booking|holiday|rental|hire|course)\b")
NOT_AN_AGREEMENT = re.compile(
    r"\b(?:card|meeting|dinner|lunch|reservation|restaurant|appointment|appointments|plans?|"
    r"party|birthday|barbecue|bbq)\b")
LEAVING_ASK = re.compile(
    r"\b(?:cancel(?:ling)?\s+early|leave\s+early|break the contract|end the contract|"
    r"charge\w*\s+me\s+to\s+(?:leave|cancel|go)|how much to cancel|notice period|"
    r"early termination)\b")
GET_OUT_OF = re.compile(r"\bget(?:ting)?\s+out\s+of\b")
SHIFT_WORD = re.compile(r"\b(?:rota|shift|shifts|boss|manager|supervisor)\b")
LEAVE_EARLY = re.compile(r"\bleav(?:e|ing)\s+early\b")
CANCEL_TERMS = re.compile(
    r"\b(?:cancellation (?:fee|fees|charge|charges|policy)|how much to cancel|"
    r"fee to cancel|cost to cancel|charge to cancel|refund policy)\b")

HARM_NOUN = re.compile(
    r"\b(?:damage|damaged|flood|flooding|flooded|storm|storms|wind|water|fire|theft|thief|"
    r"thieves|stolen|stole|accidental|accident|liquid|injury|injuries|illness|subsidence|burst|"
    r"vermin)\b")
TERM_SHAPE = re.compile(
    r"\bhow long\b[^?]{0,30}\b(?:warranty|guarantee|guaranteed|cover|policy|contract|lease|"
    r"tenancy|membership|subscription|protection)\b"
    r"|\b(?:cancellation|refund|returns?|claims?|exchange) polic(?:y|ies)\b"
    r"|\binsur(?:e|ed|es|ing|ance)\b"
    r"|\b(?:what|which|whos|who) (?:is |are )?(?:not )?cover(?:ed|s)?\b")
PRICE_ASK = re.compile(
    r"\b(?:how much|how many|cheapest|cheaper|quote|quotes?|priced?|prices?|cost|costs|costly|"
    r"roughly|budget)\b")
TERM_WORD = re.compile(
    r"\b(?:policy|policies|excess|excesses|claim|claims|terms|small print|conditions|"
    r"exclusions|warranty|guarantee|deposit|premium|premiums)\b")

COUNT_AS = re.compile(r"\bcount(?:s|ed|ing)?\s+(?:towards|toward|as)\b")
ALLOWANCE_WORD = re.compile(
    r"\b(?:luggage|baggage|allowance|limit|weight|fare|fares|ticket|tickets|quota|carry on|"
    r"cabin bag|hand luggage|bag|bags|pushchair|buggy|pram)\b")

NAMED_OBJECT = re.compile(r"\b(?:take|bring|carry|pack|board with)\s+(?:it|this|that|them|those|one)\b")

VENUE_WORDS = re.compile(
    r"\b(?:ferry|plane|flight|train|bus|coach|tube|tram|boat|cruise|hotel|restaurant|cafe|pub|"
    r"camping|campsite|camp site|festival|stadium|ground|museum|gallery|cinema|pool|park|beach|"
    r"venue|abroad|airport|airline|airlines|on board|carry on|cabin bag|hand luggage|luggage|"
    r"baggage|suitcase|arena|theatre|gig|club|conference|showground|racecourse)\b")

CONTRACT_WORDS = re.compile(
    r"\b(?:landlord|letting agent|tenancy|tenant|deposit|notice|contract|employer|employee|boss|"
    r"redundancy|dismissed|sacked|refund|fined|fine|penalty|course of action|small claims|"
    r"rent|evict|evicted|eviction|housing|mortgage|arrears|work|working|job|jobs|shift|shifts|"
    r"annual leave|time off|day off|holiday ?pay|sick pay|maternity|paternity|overtime|rota)\b")

ISSUER = (
    "A licence, a permit or a visa is granted on conditions the issuing body writes, and most "
    "publish them as a short list: what you need, what it costs, how long it takes. The council "
    "grants licences and permits, and the government's site has passports, visas and driving "
    "licences. Their page first, their phone line if your own case is unusual.",
    "Conditions come from whoever grants the permission, and they are on its own site rather than "
    "in the form. The same body can tell you whether your own case needs one at all, and a phone "
    "call about that is usually quicker than filling anything in.",
)

LOCAL = (
    "Council rules are written for a street or a postcode, which is exactly why nobody else can "
    "answer them for you: a parking permit, the bin day, what the tip takes and planning are all on "
    "your own council's site. Their phone line gets you a straight answer about your address.",
    "Parking, bins, a permit, a hedge, planning: the council writes those rules and enforces them, "
    "and they are on its site under those headings. A ring with your address sorts out which one "
    "applies to you.",
)

QUESTION = re.compile(
    r"^\s*(?:is|are|was|were|does|do|did|will|would|can|could|should|shall|may|am|have|has|"
    r"what|whats|which)\b"
    r"|\b(?:is it|is that|is this|is she|is he|is my|is the|are they|are we|does it|does my|"
    r"does the|do they|do i|will it|will my|would it|can i|can we|should i)\b"
    r"|\bhow (?:much|long|do i|can i|does|would)\b")

WARD = re.compile(
    r"\b(?:hospital|ward|icu|hdu|itu|nicu|scbu|intensive care|high dependency|patient|patients|"
    r"ward sister|nurse in charge)\b")
VISITOR = re.compile(r"\b(?:visitors?|visiting|visit)\b")
SOMEONES_PERSON = re.compile(
    r"\b(?:my|his|her|our|their)\s+(?:mum|mom|mam|dad|mother|father|nan|nana|gran|granny|"
    r"son|daughter|sister|brother|wife|husband|partner|friend|aunt|uncle|cousin|neighbour|"
    r"neighbor|grandad|grandpa|grandma)\b")

LAW_NAMED = re.compile(
    r"\b(?:the law|in law|against the law|legal|illegal|legally|unlawful|statute|statutory|"
    r"consumer rights|gov\.?uk|offence|offense|criminal|solicitor|lawyers?)\b")

CARRYING = re.compile(r"\b(?:take|taking|bring|bringing|carry|carrying|come in|walk in|get in)\b")
TO_INSIDE = re.compile(r"\b(?:into|inside|on board|aboard|through security|in the cabin)\b")

PERSON_ALLOWED = re.compile(
    r"\b(?:she|he|my son|my daughter|my kid|my kids|my child|my boy|my girl|the kids)\b"
    r"[^?]{0,20}\ballowed\b")

COURT_ARM = re.compile(
    r"\b(?:summons|summoned|magistrate|court date|court hearing|tribunal|prosecut\w*|"
    r"penalty charge notice|pcn|fixed penalty|fine notice|appeal the fine|contest the fine)\b")

LOCAL_WORDS = re.compile(
    r"\b(?:parking|parked|park on|permit|pavement|kerb|dropped kerb|bins?|bin day|fly tip|"
    r"fly tipping|recycling|planning permission|noise|neighbour's hedge|footpath|right of way|"
    r"council|tip|skip permit|dog fouling|street light)\b")

SERVICE_WORDS = re.compile(
    r"\b(?:bins?|wheelie|recycling|bulky waste|household waste|garden waste|the tip(?! of)"
    r"|recycling cent(?:re|er)|street lights?|street lamps?|potholes?|kerbs?|gritting"
    r"|fly ?tipping|(?:parking|resident|visitor) permits?|planning permission"
    r"|planning application|allotments?|council tax)\b")

NOISE = re.compile(r"\bnoise\b|\bnoisy\b")
COMPLAINT = re.compile(
    r"\b(?:neighbours?|next door|loud music|nuisance|complain\w*|report\w*"
    r"|environmental health|council)\b")

NOT_A_SERVICE = re.compile(
    r"\bbin(?:ned|ning)?\s+(?:it|that|this|them|those|these)\b"
    r"|\b(?:should|shall|do|can)\s+(?:i|we)\s+bin\b"
    r"|\b(?:bread|kitchen|pedal|nappy|compost|diaper|sensor|swing) bins?\b|\brecycle bin\b"
    r"|\brecycling bin\b|\bwindows?\b|\blaptop\b|\bdesktop\b")

ASKING_SHAPE = re.compile(
    r"\b(?:what|how|where|who|when|why|which|can|could|should|do|does|did|is|are|will|would)\b"
    r"|\?")

BODY_STATE = re.compile(
    r"\b(?:on an empty stomach|empty stomach|with food|with water|before food|after food|"
    r"before eating|after eating|on antibiotics|with alcohol|on a full stomach)\b")

COVER_IT = re.compile(r"\b(?:should|shall|do|can)\s+(?:i|we)\s+(?:cover|covering)\b")

COVERED_IN = re.compile(r"\bcovered\s+(?:in|with)\b")

TERMS = (
    "Cover sits in a section headed what is included and what is excluded, and the exclusions "
    "are often the longer list. That section is the one that counts; if the page is vague, the "
    "letter or email they sent you repeats the same words, and asking them in writing leaves you "
    "with an answer you can point to.",
    "This turns on one clause: what the policy calls the thing, and whether your loss is on its "
    "list of exclusions. Find that section before you rely on it, and ask them to confirm it in "
    "writing, because a written answer is the one you can hold them to.",
    "What applies is what the wording says, and it is written in the same three places: the "
    "section on what is included, the exclusions, and the letter they sent when you took it out. "
    "A call to whoever sold it you settles the last doubt, and their answer in writing settles it "
    "for good.",
)

INCLUDED = (
    "What a price covers is written where it is sold: the booking page lists what comes with it, "
    "and anything it does not list is charged on top, often at the desk rather than before. Ask "
    "for the total in writing before you pay, and keep that email for the day itself.",
    "Included and not included are two lists, and the second is the one that costs you: it is on "
    "the page you book on, then at the desk, where the extras get added. Read the first list "
    "before you book and ask for the total by email, because that is the version they have to "
    "honour.",
    "A room, a package or a rate names what comes with it in its own terms, and whatever it does "
    "not name is charged separately - parking, breakfast and the wifi are the usual three. Check "
    "that list before you book, and ring to confirm what applies to your own booking.",
)

LOCAL_SERVICE = (
    "Bins, the tip, permits, a street light, a complaint about noise: each one is your local "
    "authority's own service, decided for a whole street at a time and published by the council or "
    "town hall that runs it. Their site takes your postcode and gives the page for your address, "
    "and their phone line with the address answers faster than a search will. Tell me what they "
    "say and I'll help with the next step.",
    "That one is settled per address rather than in general, so I can't see your street from here: "
    "the council or town hall for your address decides it for its own postcodes, and publishes "
    "what it wants from you - the address, the date, and usually one photo. Their page first, then "
    "their phone line if your case does not fit it. What is it you are trying to get done?",
    "Your council or town hall runs that service and writes the rule for it street by street, so "
    "its site with your postcode in it is the only place that is right for your address. Ring them "
    "if the page does not cover your case - they answer for one address faster than a search will. "
    "What have you got so far?",
)

TICKET_WORD = re.compile(
    r"\b(?:railcard|rail pass|ticket|tickets|season ticket|oyster|travelcard|travel card|"
    r"boarding pass|day pass|bus pass|fare|fares|rover|interrail)\b")

OPERATOR = (
    "A ticket usually names on its face the route, the operator and the times it is good for, and "
    "the full conditions live on the operator's page rather than at the station. Check the ticket, "
    "then their page on what the fare covers; the guard on board checks the one you have.",
    "What a pass is good on is set by the operator whose buses or trains it is for, and their page "
    "on what is included lists it by name: the routes, the times and the extras. A call to them "
    "settles your own ticket in a few minutes.",
    "Fares and passes come with conditions written by the company that runs the service, and they "
    "are published with the timetable rather than with the ticket. Their page on what the fare "
    "covers is the one that counts, and the guard on the day has the last word.",
)

INSURER = (
    "A policy is decided by its own wording and its list of exclusions, not by the kind of claim "
    "it sounds like. Read the exclusions first, then ring the insurer to confirm your own case "
    "before you claim or pay for anything: they have to tell you, and that answer is the one that "
    "counts.",
    "Insurers decide this from the wording in your schedule, which is written when the policy is "
    "taken out and does not change with the claim. Their claims line will tell you straight away, "
    "and it is worth asking for it by email so you have it in writing.",
    "Whether a claim is met is the policy's own test: what is included, then what is excluded, "
    "then the excess. The insurer is the only one who can apply that to your case, and asking "
    "before you spend anything is the cheap way round.",
)

ALLOWED = (
    "Places and companies write these rules down, usually under a heading like what you can bring "
    "or what is not allowed, and the person on the door has the last word on the day. Find that "
    "page, then ask them by email so you have the answer to show.",
    "This is somebody else's rule to make, and they are the only ones who can apply it to your "
    "case. An email asking whether it is allowed is worth more than a phone call, because you can "
    "point to it later.",
    "Rules like this are set by whoever runs the thing rather than by the law or by me, and they "
    "are written where you book. If the page is vague, ring before you set off: being turned away "
    "at the door is the expensive way to find out.",
)

VENUE = (
    "A ferry, an arena, a campsite: whoever runs the place writes what you can bring on, and it is "
    "on their own page about what is allowed in, not in the booking email. Worth a call before you "
    "travel if the page is vague.",
    "What you can bring on with you is decided by whoever runs the place, and it is written for "
    "travellers rather than for lawyers - on their page about what is allowed in. A quick call "
    "settles it before you pack.",
    "Their rule, written where you book: most places publish what is allowed in and what has to go "
    "in the hold or be left at the door. The page first, then a ring to confirm your own case.",
)

CONTRACT = (
    "That is set by what you agreed to: the section on notice and fees says what it costs to end "
    "it early, and it is usually a fixed sum or the rest of the term. If it is a tenancy or a job, "
    "Citizens Advice, or ACAS for work, will read it beside you for free.",
    "The notice and the fee are on the paper you signed, or in the account page if you joined "
    "online, and it is usually one short section headed ending the agreement. Ask them for the "
    "figure in writing, because that is the one you can hold them to.",
    "Leaving early usually costs a fixed sum or the rest of the term, and the section that says "
    "which is in the terms you agreed. If the wording is not clear, Citizens Advice will go "
    "through a tenancy or an employment contract with you for free.",
)

A_PLACE = re.compile(
    r"\b(?:hotel|guest ?house|b\s?and\s?b|hostel|campsite|caravan park|holiday park|cottage|"
    r"villa|apartment|airport|station|venue|concert hall|leisure cent(?:re|er)|swimming pool|"
    r"gym|restaurant|pub|club|theatre|cinema|hospital|surgery|office|rooms?|bedrooms?|the flat|"
    r"the house|the cottage|the caravan|flat we(?:ve| have) booked|the building|building|"
    r"the premises|the shop|the salon|the clinic|the garage)\b")
A_FACILITY = re.compile(
    r"\b(?:parking|car park|wifi|wi-?fi|internet|pool|gym|spa|sauna|breakfast|air ?con(?:ditioning)?|"
    r"kitchen(?:ette)?|lift|elevator|shower|bath|towels?|hairdryer|hair dryer|kettle|microwave|"
    r"fridge|freezer|washing machine|iron|tv|television|safe|balcony|room service|charger|"
    r"plug sockets?|"
    r"toaster|crockery|cutlery|pans|a cot|cot bed|high ?chair|towels|bedding|linen|"
    r"accessible|wheelchair|dog friendly|disabled access)\b")
A_ROOM_FACILITY = re.compile(
    r"\b(?:parking|car park|wifi|wi-?fi|internet|air ?con(?:ditioning)?|kitchen(?:ette)?|lift|"
    r"elevator|shower|bath|towels?|hairdryer|hair dryer|kettle|microwave|fridge|washing machine|"
    r"iron|tv|television|a safe|the safe|balcony|toaster|a cot|cot bed|high ?chair|"
    r"plug sockets?|room service)\b")
A_HAS_ASK = re.compile(
    r"\b(?:is there|are there|is there any|do they have|does (?:it|this|that|the [a-z]+) have|"
    r"have (?:they|you) got|does it come with|will there be|is it got|got a|"
    r"do (?:the|these|those|your) [a-z]+ have)\b")
NOT_A_HAS = re.compile(
    r"\b(?:open|opens|opening|closed?|closing|hours|what time|how much|price|cost|charge|fee|"
    r"parking permit|bus|train|tube|tram|roadworks|traffic)\b")

THE_OLD_ONE = re.compile(
    r"\b(?:the|my|our|that|this|these|those) old (?:one|ones|unit|units|boiler|fridge|freezer|"
    r"fridge ?freezer|washing machine|dishwasher|tumble dryer|cooker|oven|hob|bath|shower|toilet|"
    r"radiators?|windows?|doors?|carpets?|sofa|settee|bed|mattress|tyres?|batteries|cupboard|"
    r"wardrobe|kitchen|bathroom|fire|fireplace|water tank|tank)\b")
MOVING_THE_OLD = re.compile(
    r"\b(?:keep|keeping|take\b[^,.;]{0,30}\baway|getting? rid|get rid|dispose|"
    r"disposal|recycl\w*|scrap\w*|trade ?in|remove|removed|removal|throw (?:it|them) out|"
    r"skip|tip|leave (?:it|them)|what happens to)\b")
NOT_THE_OLD_ONE = re.compile(
    r"\b(?:rice|potatoes?|bread|milk|chicken|meat|curry|soup|leftovers?|stock|pasta|veg|"
    r"cat|dog|horse|rabbit|hamster|fish)\b")

A_PLACE_HAS = (
    "Whether a place has a thing is decided by that place and not by its name: the same chain "
    "differs from one branch to the next, and a station, an office and a hotel each answer for "
    "themselves. Its own site or the page you book on lists what comes as standard and what costs "
    "extra, and one call to the place confirms what the page leaves out - ask for it in writing if "
    "it matters on the day.",
    "Facilities belong to whoever runs the place, so the current list is on their own page rather "
    "than anywhere general, and anything charged for usually sits on a line of its own, so look for "
    "both before you decide. If the page is silent, the place itself is the one that knows.",
    "That turns on the building rather than the name above the door, and the people there know it "
    "exactly. Ring or email the place itself and ask them to confirm it for the day you are going, "
    "so you have it in writing if it turns out not to be there.",
)

THE_OLD_ONE_POOL = (
    "The old one is usually the fitter's to take: whoever installs the new one carries the old "
    "away for a small fee if you ask when the job is quoted, and a shop that only delivers will "
    "not touch it. Ask about it with the quote and it is one less thing on the day.",
    "Whether you can keep it turns on who owns it now: bought outright it is yours, and rented or "
    "on finance it is not - that is in the agreement, not on any page. If it is yours and nobody "
    "wants it, the council's own site lists the bulky collection, what they take and what it "
    "costs.",
    "Two things settle it: who owns it after the swap, and who will move it. The installer "
    "answers the first when they quote, and a scrap merchant or the council's bulky waste service "
    "answers the second - both are worth asking before the day rather than on it.",
)

def options(clean):
    if not isinstance(clean, str) or not clean:
        return None
    if COVER_IT.search(clean):
        return None
    if COVERED_IN.search(clean):
        return None
    if PERSON_ALLOWED.search(clean) or WORKING_OUT.search(clean) or BODY_STATE.search(clean):
        return None
    if VISITOR.search(clean) and (WARD.search(clean) or SOMEONES_PERSON.search(clean)):
        return None
    asking = bool(QUESTION.search(clean))
    if re.match(r"\s*(?:was|were)\b", clean):
        return None
    if asking and THE_OLD_ONE.search(clean) and MOVING_THE_OLD.search(clean) \
            and not NOT_THE_OLD_ONE.search(clean):
        return THE_OLD_ONE_POOL
    if asking and (A_PLACE.search(clean) or A_ROOM_FACILITY.search(clean)) \
            and A_FACILITY.search(clean) and A_HAS_ASK.search(clean) \
            and not NOT_A_HAS.search(clean):
        return A_PLACE_HAS
    if asking and CANCEL_TERMS.search(clean):
        return TERMS
    if asking and HARM_NOUN.search(clean) and re.search(r"\bcover(?:ed|s)?\b", clean):
        return INSURER
    if asking and TERM_SHAPE.search(clean):
        if PRICE_ASK.search(clean) and not TERM_WORD.search(clean):
            return None
        if INSURANCE_WORD.search(clean) or HARM_NOUN.search(clean):
            return INSURER
        if TICKET_WORD.search(clean):
            return OPERATOR
        if CONTRACT_WORDS.search(clean):
            return CONTRACT
        return TERMS
    terms = TERMS_THING.search(clean) or COVERED_PHRASE.search(clean)
    if asking and not terms and INCLUDED_ASK.search(clean) and PRICE_THING.search(clean):
        return INCLUDED
    if COURT_ARM.search(clean):
        return None
    if asking and terms and TERMS_ASK.search(clean):
        if INSURANCE_WORD.search(clean):
            return INSURER
        if TICKET_WORD.search(clean):
            return OPERATOR
        return TERMS
    early_exit = re.search(r"\bearly\b", clean) and AGREEMENT_WORD.search(clean)
    leaving = (LEAVING_ASK.search(clean) or early_exit
               or (GET_OUT_OF.search(clean) and AGREEMENT_WORD.search(clean)))
    if leaving and LEAVE_EARLY.search(clean) and SHIFT_WORD.search(clean):
        leaving = False
    if leaving and not NOT_AN_AGREEMENT.search(clean):
        return CONTRACT
    if COUNT_AS.search(clean) and ALLOWANCE_WORD.search(clean):
        return VENUE
    if asking and NEEDED_THING.search(clean) and NEEDED_ASK.search(clean):
        return ISSUER
    taking = (not NAMED_OBJECT.search(clean)
              and (TAKE_ON.search(clean)
                   or (TAKE_TO.search(clean) and VENUE_WORDS.search(clean))))
    if ALLOWED_ASK.search(clean) or taking:
        if LOCAL_WORDS.search(clean):
            return LOCAL
        if LAW_NAMED.search(clean) and not (CARRYING.search(clean) and TO_INSIDE.search(clean)):
            return None
        if VENUE_WORDS.search(clean):
            return VENUE
        if CONTRACT_WORDS.search(clean):
            return CONTRACT
        return ALLOWED
    if (ASKING_SHAPE.search(clean) and not NOT_A_SERVICE.search(clean)
            and (SERVICE_WORDS.search(clean)
                 or (NOISE.search(clean) and COMPLAINT.search(clean)))):
        return LOCAL_SERVICE
    return None
