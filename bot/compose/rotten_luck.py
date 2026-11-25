import re

from . import pick

THEIR_PLACE = (r"(?:my|our|the)\s+(?:[a-z']+\s+)?(?:house|flat|place|home|kitchen|bathroom|cellar|basement|loft|"
               r"garage|shed|garden|hall|hallway|landing|roof|bedroom|attic|utility|conservatory)")

THEIR_THING = r"(?:my|our)\s+(?:[a-z']+\s+){0,2}"

NOT_GOOD = tuple(re.compile(pattern) for pattern in (
    rf"\b(?:we|i|they)\s+(?:just\s+)?had\s+(?:a|an)\s+(?:flood|flooding|leak|burst\s+pipe|"
    r"burst\s+radiator|break[- ]?in|burglary|fire)\b",
    rf"{THEIR_PLACE}[^.!?,]{{0,24}}\b(?:flooded|flooding|is flooding|has flooded|caught fire|"
    r"went on fire|is leaking|was leaking|has water coming in|came through the ceiling)\b",
    r"\b(?:got|been|were|was)\s+(?:burgled|broken into|robbed|vandalised|vandalized|"
    r"smashed up|turned over)\b",
    rf"{THEIR_THING}\b(?:got|was|were|has been|had been|is|are|got\s+)\s*(?:keyed|scratched|"
    r"dented|clamped|towed(?:\s+away)?|smashed|nicked|stolen|vandalised|vandalized|"
    r"broken into|pinched|slashed|punctured|kicked in|wrenched off|snapped off|ripped|torn|"
    r"torched|set (?:on )?fire to)\b",
    r"\b(?:someone|somebody|a kid|the kids|next door|a neighbour|a neighbor|my neighbours?|"
    r"our neighbours?|the neighbours?)\s+"
    r"(?:keyed|scratched|dented|smashed|nicked|pinched|stole|took|vandalised|vandalized)\s+"
    r"(?:my|our)\b",
    rf"{THEIR_THING}\b(?:son|daughter|kid|child|boy|girl|lad|lass|teenager|eldest|youngest)\b"
    r"[^.!?,]{0,30}\b(?:suspended|excluded|expelled)\b",
    rf"{THEIR_THING}\b(?:visa|application|claim|mortgage|loan|benefits?|pip|dla|passport|"
    r"offer|request)\b[^.!?,]{0,24}\b(?:refused|rejected|turned down|declined|denied|"
    r"turned me down|turned them down)\b",
    r"\bcame off\s+(?:my|his|her|the|a|their)\s+(?:bike|motorbike|moped|scooter|e-scooter|"
    r"cycle|horse|ladder|roof|skateboard|board)\b",
    rf"{THEIR_THING}\b(?:car|van|bike|motorbike)\b[^.!?,]{{0,20}}\b(?:got|was|were)\s+"
    r"(?:clamped|towed(?:\s+away)?|keyed|scratched|dented|scraped)\b",
    r"\bpranged\b|\bscraped the (?:car|van|wing mirror)\b",
    rf"(?:{THEIR_PLACE}|\b(?:ceiling|roof|fence|gate|wall|greenhouse|tree|branch|tiles?|"
    r"guttering|gutter|chimney pot|carport|awning))\b[^.!?,]{0,24}\b(?:came down|collapsed|"
    r"caved in|blew (?:away|down|off|over)|got blown (?:away|down|off))\b",
))

NOT_GOOD_DESPITE = re.compile(
    r"\bflood(?:ed)?\s+(?:of|with)\b|\bfire\s+(?:drill|alarm|test|work|escape|station|place|"
    r"pits?)\b|\bkeyed\s+in\b|\bstole\s+the\s+(?:show|limelight|scene)\b|"
    r"\bnicked\s+(?:off|out)\b|\brobbed\s+(?:blind|us of)\b|\be?xcluded\s+from\s+the\s+pub\b")

GLAD_OPENER = re.compile(
    r"^(?:nice one|good to hear|sounds alright|well done|that'?s good|lovely|glad to hear|"
    r"how was it, overall)\b")

BLANK_OR_THIN = re.compile(
    r"^(?:got it\b|thanks for telling me|i'?m listening|noted:|right\.|okay\.|ok\.|"
    r"rotten luck\.?$|that'?s a pain\.?$|that'?s rough\.?$|fair enough\b|"
    r"ugh, that'?s annoying\.?$|that'?s annoying\.?$)")
GLAD_ANYWHERE = re.compile(
    r"\b(?:how did the rest of it go|what was the best bit|anything good in it|"
    r"are you pleased with it|is it what you were after|how did that feel)")

_A_SAID_NO = re.compile(
    r"\b(?:she|he|they|my\s+[a-z]+|our\s+[a-z]+|the\s+[a-z]+|his\s+[a-z]+|her\s+[a-z]+|"
    r"their\s+[a-z]+|mum|dad|boss|landlord|manager|school|council|bank|surgery|gp|doctor|"
    r"nurse|hr)\b"
    r"(?:\s+[a-z']+){0,4}?\s(?:said|says|saying|told\s+me|telling\s+me)\s+(?:me\s+)?no\b",
    re.I)
_A_REFUSED = re.compile(
    r"\b(?:she|he|they|my\s+[a-z]+|our\s+[a-z]+|the\s+[a-z]+|his\s+[a-z]+|her\s+[a-z]+|"
    r"their\s+[a-z]+|mum|dad|boss|landlord|manager|school|council|bank|surgery|gp|doctor|hr)\b"
    r"(?:\s+[a-z']+){0,3}?\s(?:refused|has\s+refused|had\s+refused|"
    r"turned\s+(?:it|me)\s+down|won'?t\s+(?:budge|have\s+it|agree|allow|consider|do\s+it|move|"
    r"shift|bend)|isn'?t\s+keen|wasn'?t\s+keen|is\s+not\s+keen|said\s+(?:it|that)\s+"
    r"(?:isn'?t|wasn'?t|is\s+not|was\s+not)\s+(?:possible|allowed|an\s+option|on))\b",
    re.I)
A_NO_ALREADY = (
    "Then you know where you stand, and that is worth something. Was the no to that exact ask, "
    "or to the idea of it?",
    "Then the answer is no for now. What would have to change for it to be a yes?",
    "Ask once more with your reason in the same sentence, and take the second no as the answer.",
    "One no is worth hearing again only if something has changed since. Say what has, in a line, "
    "and go back with it.",
    "That is a no to the ask as you put it, which is not a no to you. Change one thing about it "
    "and try again.",
    "Go for the smallest version of it that would still help, and build from that if it comes.",
)
A_NO_FROM = (
    "Then {who} has given you an answer. Was it a no to that ask, or to the whole thing?",
    "{who} has said no once, so ask for the smallest version of it that would still help.",
    "A no from {who} is worth one more ask, with what you want and why in a single line - then "
    "leave it with them.",
    "Go back to {who} with what has changed since and nothing else. That is what moves a no.",
    "What would {who} have said yes to? People who refuse usually know.",
)
_MINE = re.compile(r"\b(?:my|our)\b", re.I)
_A_NO_STILL_BEING_WEIGHED = re.compile(
    r"\b(?:what\s+if|if\s+(?:she|he|they|my|the|it)|suppose|supposing|in\s+case|unless|"
    r"should\s+i|shall\s+i|do\s+you\s+think|would\s+they|will\s+they)\b", re.I)
_A_REFUSAL_IN_THE_PASSIVE = re.compile(
    r"\b(?:was|were|got|been|is|are|being)\s+(?:refused|turned\s+down|rejected|turned\s+away|"
    r"declined|knocked\s+back)\b", re.I)

RESOLVED = re.compile(
    r"\b(?:but|and|although|though)\s+(?:\w+\s+){0,3}?(?:sorted|sorted out|fixed|resolved|"
    r"dried out|paid out|refunded|replaced|recovered|got it back|got them back|got them|"
    r"back at school|back to normal|back home|all fine|all ok|ok now|okay now|fine now|"
    r"im fine|i'?m fine|was fine|no harm|nobody hurt|no one hurt|nothing was taken|"
    r"only a scratch|turned out (?:fine|ok)|got it on appeal|won the appeal|"
    r"appeal worked|only took (?:a|the|my|our|one)\b)\b")

DAMAGED_OR_TAKEN = (
    "Rotten luck. What needs sorting first?",
    "That's a rotten one. How bad is it?",
    "Ugh, that's the last thing you needed. Is it sorted, or still going on?",
    "That's a mess to land on you. What's the damage?",
)
A_BLOW_FROM_SOMEONE = (
    "That's a blow. Sorry to hear it.",
    "Ugh, that's harsh. That's a rotten thing to have land on you.",
    "That's a rotten thing to land on you.",
)
A_FALL = (
    "That's a shock. Are you alright?",
    "Ouch. Are you hurt?",
    "That would rattle anyone. Are you alright?",
)

A_FALL_ELSE = (
    "That's a shock. Are they alright?",
    "That's a bad one. How are they doing?",
    "That's a shock to hear. Is everyone alright?",
)
_SOMEONE_ELSE = re.compile(r"\b(?:my|our|his|her|their)\s+(?:brother|sister|son|daughter|mum|mom|"
                           r"dad|husband|wife|partner|mate|friend|neighbour|neighbor|nephew|"
                           r"niece|grandad|granddad|grandma|gran|nan|colleague|boss|cousin|little "
                           r"(?:boy|girl|lad|one))\b|\b(?:he|she|they)\s+(?:came off|fell)\b")
_FALL = re.compile(r"\bcame off|\bpranged\b|\bscraped the (?:car|van|wing mirror)\b|\bclamped\b|"
                   r"\btowed\b")

MISHAP = (r"(?:fell|fall|fallen|slipped|slip|tripped|trip|came\s+off|come\s+off|knocked\s+off|"
          r"knocked\s+(?:me|us)\s+off|hit\s+(?:me|us|by)|ran\s+(?:me|us)\s+over|run\s+over|"
          r"drove\s+(?:into|at)\s+(?:me|us)|clipped\s+(?:me|us)|collided|crashed|crash|"
          r"went\s+over|tumbled|skidded|smashed\s+into)\b")
NEAR_MISS = re.compile(
    r"\b(?:nearly|almost|close\s+to|just\s+missed|just\s+about)\b[^.!?,]{0,26}\b" + MISHAP +
    r"|\b(?:near\s+miss|close\s+call|narrow\s+escape|just\s+missed\s+(?:me|us))\b")
FRIGHT = re.compile(
    r"\b(?:shaken\s+up|shaken|shook\s+up|shook\s+(?:me|us)|shakes\s+(?:me|us)\s+up|shaking\s+(?:me|us)\b|"
    r"shaking\s+(?:me|us)\s+up|still\s+shaking|shaking\s+a\s+bit|"
    r"(?:got|had|gave\s+me)\s+a\s+fright|a\s+fright|bit\s+of\s+a\s+scare|scared\s+me|"
    r"frightened\s+me|spooked\s+me|in\s+shock)\b")
NOT_A_FRIGHT = re.compile(
    r"\b(?:shaking\s+with\s+laughter|shaken\s+not\s+stirred|shaking\s+like\s+a\s+leaf\s+of\s+lettuce|"
    r"(?:scared|afraid|frightened|terrified)\s+(?:of|to|about|that|it\s+would)\b|"
    r"scared\s+(?:of|to|about)\b|frightened\s+(?:of|to)\b|in\s+shock\s+that\b)")

_A_PLAN_THAT_FELL_THROUGH = re.compile(
    r"\bf(?:ell|all|allen|alling)\s+through\b(?!\s+(?:the\s+)?(?:ice|floor|roof|glass|window|"
    r"boards?|ceiling|decking|net|crust|hole)\b)")
_A_BARE_NEAR_MISS = re.compile(r"\b(?:near\s+miss|close\s+call|narrow\s+escape)\b")
_A_BODY_CAN_BE_HURT = re.compile(
    r"\b(?:bike|cycle|bicycle|car|van|lorry|truck|bus|coach|train|tram|taxi|cab|scooter|motorbike|"
    r"road|motorway|roundabout|kerb|junction|crossing|pavement|street|stairs|staircase|steps|"
    r"ladder|scaffolding|roof|balcony|wall|window|glass|ice|snow|kitchen|bath|shower|pool|sea|"
    r"cliff|horse|path|track|ferry|boat)\b")
_A_THING_WITH_NO_BODY = re.compile(
    r"\b(?:deadline|deal|sale|plan|plans|trip|booking|offer|order|mortgage|application|interview|"
    r"contract|flight|agreement|purchase|quote|bid|tender|funding|visa|exam|essay|project|"
    r"launch)\b")

A_FRIGHT = (
    "Glad you're okay. That stays with you for a while.",
    "That gets the heart going. Sit down for a minute if you can.",
    "A fright like that sits in the body for a while. Are you okay now?",
    "God, that shakes you up. Do you want to sit down for a minute?",
)
A_NEAR_MISS = (
    "Close one. Are you hurt at all?",
    "God, a near miss like that shakes you up. Are you alright?",
    "That gets the heart going. Sit down for a minute if you can.",
    "Glad you're in one piece. That sort of thing stays with you.",
)
A_FRIGHT_ELSE = (
    "That shakes anyone up. Are they alright?",
    "A fright like that stays with you. How are they now?",
    "That gets the heart going. Is everyone alright?",
)
A_NEAR_MISS_ELSE = (
    "Close call. Is everyone alright?",
    "Glad they're in one piece. That sort of thing shakes you up.",
    "That would rattle anyone. Are they hurt at all?",
)
_FROM_SOMEONE = re.compile(r"\b(?:suspended|excluded|expelled|refused|rejected|turned down|"
                           r"declined|denied)\b")


A_THING_THAT_DID_NOT_WORK = (
    "That's annoying. What does it do when you try it?",
    "Ugh, one of those. Where are you up to with it now?",
    "That's a pain. What have you got in front of you at the moment?",
    "Rotten. Does it do the same thing every time?",
)
A_WAIT_THAT_WENT_ON = (
    "That's a long time to sit there. Did you get seen in the end?",
    "Ugh, two hours of that. Was it worth staying for?",
    "That's a lot of waiting. Did anyone tell you what was going on?",
)
A_REMARK_THAT_STUNG = (
    "That would sting. What did they say?",
    "Ugh, that's not a kind thing to say. How did you take it?",
    "That's the sort of thing that sits with you. Did you say anything back?",
)
A_BILL_THAT_SAYS_OTHERWISE = (
    "That's worth checking before you pay again. What does the bill say?",
    "Ugh. What does their paperwork say you owe?",
    "That's easily done on their side. Have you got the receipt?",
)
A_MEAL_THEY_WENT_WITHOUT = (
    "That's a day with a hole in the middle of it. Is it no time to stop, or nothing in?",
    "A day with a meal missing in it drags from there on. What stopped you - the day, or the "
    "cupboard?",
    "Ugh, that leaves you running on nothing. Get something in you now if you can - even toast "
    "counts.",
    "That's a miserable way to get through a day. Get something in you soon, whatever is quickest.",
)
_A_JOB_NEEDED = re.compile(
    r"\b(?:my|our|the)\s+(?:[\w']+\s+){0,2}?(?:needs?|needed)\s+"
    r"(?:a\s+|an\s+|some\s+)?(?:new\s+[\w']+|doing|fixing|replacing|repairing|painting|"
    r"servicing|cleaning|sorting|resurfacing|cutting|work|doing\s+up|service|look|quote|check|"
    r"part|parts|job)\b"
    r"|\b(?:said|says|told\s+me)\s+(?:it|the\s+[\w']+)\s+(?:needs?|would\s+need)\b")
_NOT_A_TRADE = re.compile(
    r"\b(?:homework|schoolwork|coursework|essay|essays|dissertation|revision|assignment|assignments|"
    r"reading|forms?|paperwork|admin|tax\s+return|shopping|washing|laundry|ironing|dishes|"
    r"washing[-\s]?up|sink|hoovering|vacuuming|tidying|housework|cleaning|bins|bin|cv|"
    r"applications?|invoices?|accounts|bookkeeping|packing|unpacking|bathroom|bedroom|beds?|"
    r"cooking|dinner|tea|supper|lunch|inbox|emails?|photos?|backups?)\b")
_A_PERSON_NEEDING = re.compile(
    r"\b(?:my|our|the|his|her|their)\s+(?:mum|mom|mother|dad|father|son|daughter|kid|kids|child|"
    r"children|wife|husband|partner|baby|boy|girl|mate|friend|boss|brother|sister|nan|gran|"
    r"grandad|grandma|dog|cat|puppy|kitten|teeth|tooth|gums|hair|nails|knee|back|hip|shoulder|"
    r"ankle|wrist|elbow|neck|eyes|skin)\b\s+(?:needs?|needed|wants?|has|have)\b")
_A_JOB_THAT_IS_SORTED = re.compile(
    r"\b(?:sorted|done|fixed|replaced|booked|arranged|coming\s+(?:on|tomorrow|next)|"
    r"quoted|priced|paid\s+for|had\s+a\s+quote|got\s+a\s+quote|got\s+a\s+price|"
    r"had\s+a\s+price|been\s+quoted)\b")
A_CHORE_WAITING = (
    "It is one job rather than a day's work. Ten minutes on it now, and stop when the timer goes - "
    "starting is the part that was making it feel bigger than it is.",
    "Give it a quarter of an hour and see where you are. One job of that size fits in an evening, "
    "and whatever is left of it will keep until tomorrow.",
    "Put a timer on and do the part you can see. It is one thing, not a verdict on your week, and "
    "you can stop at ten minutes with it half done.",
)
A_CHORE_PILE = (
    "One of those jobs that never gets shorter. Pick the one you would notice most if it were done "
    "and do that first; the rest will still be there tonight, and that is allowed.",
    "That sort of pile is normal and it is not a moral failing. Do the smallest one on the list "
    "now, while the kettle boils, and it stops feeling like a wall.",
    "Nothing broken, just a pile. Write them down, do the one that takes ten minutes, and leave "
    "the rest for a day when you have the energy.",
)
_PILE_WORDS = re.compile(
    r"\b(?:pile|piles|mountain|backlog|list|mess|state|everything|all\s+of\s+it|loads|"
    r"loads\s+of|lots|chores|housework|catch(?:ing)?\s+up|behind\s+on)\b")
_CHORE_THINGS = re.compile(
    r"\b(?:homework|schoolwork|coursework|essays?|dissertation|revision|assignments?|"
    r"forms?|paperwork|admin|shopping|washing|laundry|ironing|dishes|washing[-\s]?up|"
    r"hoovering|vacuuming|tidying|cleaning|bins?|cv|applications?|invoices?|packing|"
    r"unpacking|bathroom|bedroom|beds?|cooking|inbox|emails?|photos?|backups?)\b")


def _a_pile_of_chores(clean):
    if _PILE_WORDS.search(clean):
        return True
    return len(set(_CHORE_THINGS.findall(clean))) > 1
A_JOB_SOMEBODY_ELSE_DOES = (
    "That's a job for a trade rather than a guess. Ask for the price in writing first, and what "
    "it includes.",
    "Worth two quotes on that one. The written quote that says what is included is the one to "
    "compare.",
    "That's a cost to land on you. Have you had a price for it yet, or is that the next step?",
    "Ugh, one of those. Get what they would do and what it costs in writing before anybody starts.",
)
_TRIED_AND_IT_DID_NOT = re.compile(
    r"\b(?:ive|i'?ve|we'?ve|weve|i|we)\s+(?:already\s+)?(?:tried|attempted)\b"
    r"|\btried\s+(?:everything|it all|all of it|that|this|it|both|two|three|\w+\s+\w+(?:es|s))\b"
    r"|\bnothing\s+(?:works|worked|has worked|i try|i do)\b"
    r"|\b(?:didn'?t|doesn'?t|won'?t|wont|not)\s+work(?:ed)?\b"
    r"|\bno\s+luck\b|\bstill\s+(?:nothing|not|the same|doing it|happening)\b"
    r"|\bkeeps?\s+(?:doing|going|coming back|happening)\b"
    r"|\bgave up on it\b")
_STILL_NO = re.compile(r"\bstill\s+(?:no\s+[a-z]|without\s+[a-z]|not\s+got\b|havent\b|"
                       r"haven'?t\b|waiting\b)")
A_LACK_THAT_IS_STILL_GOING = (
    "That's dragging on. How are you holding up with it?",
    "That's a long stretch of waiting for it. Is anything moving on it at all?",
    "Still nothing, then. That wears you down - what's the part you can move?",
    "That's hard going. Is it something you can chase, or does it just take time?",
)
_A_WAIT = re.compile(
    r"\b(?:i|we|he|she|they)\s+(?:was|were|have been|had been)?\s*wait(?:ed|ing)?\b"
    r"|\bqueue(?:d|ds|ing|s)?\b|\bin\s+the\s+queue\b|\bsat\s+in\s+(?:a|the)\s+waiting\b")
_A_LONG_WAIT = re.compile(r"\b(?:hours?|hrs?|ages|half an hour|an hour|two hours|all morning|"
                          r"all afternoon|\d+\s*(?:hours?|hrs?))\b")
_A_REMARK = re.compile(
    r"\bpassed\s+(?:a\s+)?(?:comment|remark|comments|remarks)\b"
    r"|\b(?:had|having)\s+(?:a\s+)?go\s+at\s+me\b"
    r"|\b(?:moaned|went on|nagged|lectured)\s+(?:at|to)\s+me\b"
    r"|\bsaid\s+something\s+(?:about|on)\s+my\b"
    r"|\bmade\s+a\s+(?:comment|remark|face)\s+about\b")
_A_DISPUTED_CHARGE = re.compile(
    r"\bbut\s+i\s+(?:thought|was\s+told|understood|believed)\b[^.!?]{0,44}"
    r"\b(?:paid|pay|included|free|covered|booked|settled|refund(?:ed)?)\b"
    r"|\b(?:they|it)\s+says?\s+i\s+owe\b|\bcharged\s+me\s+again\b"
    r"|\bi\s+was\s+told\s+it\s+was\s+(?:free|included)\b")
_A_MEAL_MISSED = re.compile(
    r"\b(?:went|gone|go|going|was)\s+without\s+(?:my\s+|any\s+|a\s+|the\s+|our\s+)?"
    r"(?:lunch|dinner|tea|breakfast|supper|food|a\s+meal|meals|my\s+meal)\b"
    r"|\b(?:skipped|missed|skipping|missing)\s+(?:my\s+|a\s+|the\s+|our\s+|any\s+)?"
    r"(?:lunch|dinner|tea|breakfast|supper|a\s+meal|meals)\b"
    r"|\bno\s+(?:lunch|dinner|tea|breakfast|proper\s+meal)\b[^.!?]{0,14}"
    r"\b(?:again|today|yesterday|either)\b"
    r"|\b(?:worked|working)\s+through\s+(?:my\s+|a\s+|the\s+)?(?:lunch|dinner)\b"
    r"|\bforgot\s+(?:to\s+eat|my\s+(?:lunch|dinner|tea|breakfast|food))\b"
    r"|\bdidn'?t\s+(?:get|have|manage)\s+(?:any\s+|a\s+|my\s+)?(?:lunch|dinner|tea|breakfast|"
    r"(?:proper\s+)?meal)\b")
_A_MEAL_ON_PURPOSE = re.compile(
    r"\b(?:on\s+purpose|deliberately|on\s+purpose|by\s+choice|fasting|fast\s+day|intermittent|diet(?:ing)?|"
    r"cutting\s+(?:out|down)|trying\s+to\s+(?:lose|lose\s+weight)|skipping\s+meals\s+to)\b")
_SOMEBODY_ELSES_MEAL = re.compile(
    r"\b(?:the\s+kids?|the\s+children|my\s+(?:son|daughter|boy|girl|lad|lass|husband|wife|partner|mum|mom|"
    r"dad|brother|sister|friend|mate|flatmate|housemate)|he|she|they)\b")
_MINE_OR_OURS = re.compile(r"\b(?:i|ive|i'?m|im|i'?ve|we|weve|we'?ve|myself)\b")


_AN_ASK_OPENING = re.compile(
    r"^(?:what|how|why|when|where|which|who|whose|is|are|was|were|do|does|did|can|could|should"
    r"|would|will|shall|am|may|might|any\s+chance|isnt|arent|doesnt|dont|didnt)\b")


def reads_as_stuck_with_it(clean):
    if not clean or "?" in clean or NOT_GOOD_DESPITE.search(clean):
        return False
    if _AN_ASK_OPENING.match(clean):
        return False
    if _A_DISPUTED_CHARGE.search(clean):
        return True
    if _A_REMARK.search(clean):
        return True
    if _TRIED_AND_IT_DID_NOT.search(clean):
        return True
    return bool(_A_WAIT.search(clean) and _A_LONG_WAIT.search(clean))


def reads_as_not_good(clean):
    if not clean or NOT_GOOD_DESPITE.search(clean):
        return False
    if reads_the_shake(clean):
        return True
    return any(pattern.search(clean) for pattern in NOT_GOOD)


def reads_the_shake(clean):
    if not clean or NOT_A_FRIGHT.search(clean):
        return False
    if _A_PLAN_THAT_FELL_THROUGH.search(clean):
        return False
    if (_A_BARE_NEAR_MISS.search(clean) and _A_THING_WITH_NO_BODY.search(clean)
            and not _A_BODY_CAN_BE_HURT.search(clean)):
        return False
    return bool(NEAR_MISS.search(clean) or FRIGHT.search(clean))


_SHAKE_IS_THEIRS = re.compile(r"^\s*(?:he|she|they|him|them|his|her|their)\b")


def reads_the_shake_of_someone_else(clean):
    if not reads_the_shake(clean):
        return False
    return bool(_SOMEONE_ELSE.search(clean) or _SHAKE_IS_THEIRS.match(clean))


def reads_as_glad(reply):
    if not reply:
        return False
    line = reply.strip().lower()
    return bool(GLAD_OPENER.match(line) or GLAD_ANYWHERE.search(line)
                or BLANK_OR_THIN.match(line))


def reads_as_a_meal_missed(clean):
    if not clean or "?" in clean:
        return False
    if _A_MEAL_ON_PURPOSE.search(clean):
        return False
    if not _A_MEAL_MISSED.search(clean):
        return False
    return bool(_MINE_OR_OURS.search(clean) or not _SOMEBODY_ELSES_MEAL.search(clean))


def reads_as_a_no_they_had(clean):
    if not clean or "?" in clean:
        return False
    if len(str(clean).split()) > 14:
        return False
    if _A_NO_STILL_BEING_WEIGHED.search(str(clean)):
        return False
    if re.match(r"^(?:i|we)\b", str(clean)) and not re.search(
            r"\b(?:she|he|they|my|our|the)\b", str(clean)):
        return False
    return bool(_A_SAID_NO.search(str(clean)) or _A_REFUSED.search(str(clean)))


def _who_said_no(clean, memory):
    if _A_REFUSAL_IN_THE_PASSIVE.search(str(clean or "")):
        return ""
    who = ""
    match = re.search(r"\b((?:my|our|the)\s+[a-z]+|mum|dad)\b", str(clean or ""))
    if match:
        who = match.group(1)
    if not who:
        lean = ((memory or {}).get("understood") or {}).get("leans_on") or {}
        subject = str(lean.get("subject") or "").strip().lower()
        if subject and lean.get("subject_type") == "person":
            who = subject
    if not who:
        return ""
    return " ".join(_MINE.sub("your", who, count=1).split())


def answer_for(text, memory=None, reply=None):
    if not reads_as_glad(reply):
        return None
    memory = memory or {}
    clean = ((memory.get("understood") or {}).get("clean") or text or "").lower()
    clean = " ".join(clean.split())
    if reads_the_shake(clean):
        if reads_the_shake_of_someone_else(clean):
            mine = A_NEAR_MISS_ELSE if NEAR_MISS.search(clean) else A_FRIGHT_ELSE
        elif NEAR_MISS.search(clean):
            mine = A_NEAR_MISS
        else:
            mine = A_FRIGHT
        return pick(list(mine), memory, clean)
    if RESOLVED.search(clean):
        return None
    if reads_as_a_meal_missed(clean):
        return pick(list(A_MEAL_THEY_WENT_WITHOUT), memory, clean)
    if (_A_JOB_NEEDED.search(clean) and not _A_PERSON_NEEDING.search(clean)
            and not _A_JOB_THAT_IS_SORTED.search(clean)):
        if _NOT_A_TRADE.search(clean):
            pool = A_CHORE_PILE if _a_pile_of_chores(clean) else A_CHORE_WAITING
            return pick(list(pool), memory, clean)
        return pick(list(A_JOB_SOMEBODY_ELSE_DOES), memory, clean)
    if _STILL_NO.search(clean) and not _A_WAIT.search(clean):
        return pick(list(A_LACK_THAT_IS_STILL_GOING), memory, clean)
    if reads_as_stuck_with_it(clean):
        if _A_DISPUTED_CHARGE.search(clean):
            pool = A_BILL_THAT_SAYS_OTHERWISE
        elif _A_REMARK.search(clean):
            pool = A_REMARK_THAT_STUNG
        elif _A_WAIT.search(clean) and _A_LONG_WAIT.search(clean):
            pool = A_WAIT_THAT_WENT_ON
        else:
            pool = A_THING_THAT_DID_NOT_WORK
        return pick(list(pool), memory, clean)
    if not reads_as_not_good(clean):
        if not reads_as_a_no_they_had(clean):
            return None
        who = _who_said_no(clean, memory)
        pool = A_NO_FROM if who else A_NO_ALREADY
        line = pick(list(pool), memory, clean + "|" + who)
        return line.format(who=who) if who else line
    if _FALL.search(clean):
        pool = A_FALL_ELSE if _SOMEONE_ELSE.search(clean) else A_FALL
    elif _FROM_SOMEONE.search(clean):
        pool = A_BLOW_FROM_SOMEONE
    else:
        pool = DAMAGED_OR_TAKEN
    return pick(list(pool), memory, clean)
