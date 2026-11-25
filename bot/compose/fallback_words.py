import re

WHO_FOR_IT = re.compile(
    r"^(?:(?:so|and|ok|okay|right|but|then|now|hi|hey|hello|please)\s+)*"
    r"who\s+(?:do|should|can|could|would|must|will)\s+(?:i|we)\s+"
    r"(?:call|ring|phone|contact|tell|ask|chase|see|use|get|speak\s+to|talk\s+to|go\s+to"
    r"|report(?:\s+it)?\s+to)"
    r"(?:\s+(?:out|in|around|round))?"
    r"(?:\s+(?:to\s+)?(?:look\s+at|fix|check|sort|deal\s+with))?"
    r"(?:\s+(?:it|that|this|them))?"
    r"(?:\s+about\s+(?:it|that|this|them))?"
    r"(?:\s+(?:first|next|now|then|please|again))?"
    r"\s*[.?!]*$")
CRISIS_ASK = re.compile(
    r"\b(?:who|someone|somebody|anyone|anybody)\b[^.!?]{0,30}?\b(?:talk|speak|chat|text|listen)\b"
    r"|\b(?:need|want|like)\b[^.!?]{0,12}?\b(?:someone|somebody|anyone|a\s+person)\b"
    r"[^.!?]{0,20}?\b(?:talk|speak|listen|there)\b")
A_PERSON_IN_A_CRISIS = (
    "Ring 116 123 - Samaritans, free, any hour, and they will stay on the line as long as you "
    "need. If you are in danger right now, 999. I am still here too, for as long as you want to "
    "type.",)
WHO_FOR_IT_SAID = (
    "{who}. Ring them about what you were just saying, and give the one line: what it is, since "
    "when, and what you want done.",
    "{who}. Same call as a moment ago, so ring them with the details ready - what it is, when it "
    "started, any reference - and tell me what they say.",
)
WHO_FOR_IT_SAID_VOICE = (
    "{who}. Talk to them about what you were just saying in your own words and ask what they "
    "would do - there is nothing to prepare.",
    "{who}. Same person as a moment ago, so talk to them about it: what it is, since when, and "
    "how much it is on your mind.",
)
WHO_NAMED_BEFORE = (
    "{who} - the one the last answer pointed at. Ring them, say the one line, and ask what "
    "happens next.",
    "{who}. You have the rest of it from a moment ago, so that is the call to make.",
)
WHO_FOR_IT_BODY = (
    "A body is not something I can look at, so the person to ring is your GP - and 111 tonight if "
    "it is getting worse. Give them the one line: what it is, when it started, and what you are "
    "afraid it might be.",
    "Your GP is the one who can look at it, or 111 if it cannot wait until morning. Write down "
    "when it started first - that is the first thing they will ask.",
)
WHO_FOR_IT_ROUTES = (
    "It depends what it is, so give me the one line and I will point you at the right person: "
    "money, housing or a company that will not play ball is Citizens Advice; a job is a union rep "
    "or ACAS; a body or a medicine is a pharmacist or the GP; a leak, gas, the electrics or a "
    "broken appliance is a plumber, a gas engineer or an electrician.",
    "There is no one answer to that, so tell me what it is about - money, a repair, a body, a "
    "pet, a form - and I will name whose job it is.",
)
WHO_TO_TALK_ASK = re.compile(
    r"\b(?:who|anyone|anybody|someone|somebody)\b[^.!?]{0,40}?\b(?:talk|speak|chat)\b"
    r"|\b(?:need|want)\b[^.!?]{0,15}?\b(?:someone|somebody|anyone|a\s+person)\b"
    r"[^.!?]{0,20}?\b(?:talk|speak|listen)\b")
WHO_TO_TALK_TO = (
    "Who you can talk to is the one thing I have no record of, so say what it is about - a class, "
    "a job, a repair, a body - and I will name the kind of person worth asking, then help you "
    "word the first message.",
    "I cannot pick the person for you, because I only have what you type. Tell me what it is "
    "about and I will say which kind of person knows, and what to say to them first.",
)
WHO_TO_TALK_TO_A_BAD_STRETCH = (
    "Who you can talk to is the one thing I have no record of, so it has to be your people: "
    "whoever you would ring at eleven at night, and if that is nobody this week, the GP is not "
    "only for a body - say it is too much and they can get you talking to someone properly. I "
    "can help you word the first message if you tell me who it is.",
    "I cannot pick the person for you, because I only have what you type. The ordinary way in is "
    "one person who already knows you, and one sentence about how things actually are; if it is "
    "bigger than a bad week, your GP can put you in front of somebody trained for it. Say who "
    "you have in mind and I will help you work out what to say.",
)

REPAIR_DECISION = re.compile(
    r"\b(?:worth|bother)\s+(?:fixing|repairing|mending|replacing|getting\s+(?:it|that|this)"
    r"\s+(?:fixed|repaired|mended))\b"
    r"|\bfix(?:ing)?\s+(?:it\s+)?or\s+(?:replace|replacing|replacement|live|bin|chuck|"
    r"buy\s+(?:a\s+)?new|buying\s+(?:a\s+)?new)\b"
    r"|\brepair\s+or\s+replace\b"
    r"|\b(?:fix|repair|mend)\s+(?:it|that|this)\s+or\s+(?:live\s+with\s+it|"
    r"replace\s+it|leave\s+it|buy\s+(?:a\s+)?new)\b"
    r"|\bshall\s+i\s+(?:live\s+with\s+it|just\s+(?:fix|replace)\s+it)\b"
    r"|\b(?:is|would)\s+it\s+be\s+(?:better|cheaper)\s+to\s+(?:fix|repair|replace)\b"
    r"|\b(?:worth|bother)\s+(?:servicing|getting\s+(?:it|that|this|them)\s+serviced"
    r"|a\s+service|paying\s+(?:for\s+)?(?:a\s+)?(?:service|repair|fix))\b"
    r"|\b(?:worth|bother)\s+getting\s+(?:a\s+)?new\s+one\b"
    r"|\b(?:get|getting)\s+(?:it|that|this)\s+serviced\s+or\s+(?:replace|replacing|bin|"
    r"leave|keep)\b"
    r"|\bservice\s+(?:it|that|this)\s+or\s+(?:replace|bin|scrap|chuck)\b"
    r"|\bkeep\s+(?:it|that|this|them)\s+or\s+(?:replace|replacing|bin|chuck|get\s+rid|"
    r"buy\s+(?:a\s+)?new|trade\s+(?:it\s+)?in)\b"
    r"|\b(?:write|writing)\s+(?:it|that|this)\s+off\s+or\s+(?:fix|repair|mend|keep)\b"
    r"|\bor\s+should\s+i\s+just\s+(?:replace|bin|chuck)\s+(?:it|that|this)\b"
    r"|\b(?:should|shall)\s+i\s+(?:just\s+)?(?:bin|chuck|scrap)\s+(?:it|that|this)\b"
    r"|\b(?:should|shall|do)\s+i\s+just\s+write\s+(?:it|that|this)\s+off\b")
REPAIR_WHETHER = re.compile(
    r"\bcan\s+(?:it|they|this|that|these|those)\s+(?:be\s+)?(?:get\s+)?"
    r"(?:fixed|repaired|mended|restored|salvaged)\b"
    r"|\bcan\s+i\s+get\s+(?:it|them|this|that|these|those|mine)\s+"
    r"(?:fixed|repaired|mended|restored)\b"
    r"|\bis\s+(?:it|this|that|my|our|the)\s+(?:[a-z']+\s+){0,2}"
    r"(?:fixable|repairable|mendable|salvageable)\b")
REPAIR_WHAT_IT_IS_WORTH = re.compile(r"\b(?:worth|bother|cheaper)\b")
REPAIR_BARE_IT = re.compile(
    r"\b(?:bin|chuck|scrap|ditch|replace|write|throw)\s+(?:it|that|this|them)\b"
    r"|\bkeep\s+(?:it|that|this|them)\s+or\b"
    r"|\bor\s+should\s+i\s+just\s+(?:replace|bin|chuck|scrap)\b")
REPAIR_TRADE = re.compile(r"\b(?:plumber|electrician|engineer|"
                          r"handyman|someone|somebody|tradesman|professional|garage)\b")
REPAIR_PERSON = re.compile(
    r"\b(?:marriage|relationship|friendship|ex|husband|wife|partner|boyfriend|girlfriend|"
    r"son|daughter|kids?|children|mum|mom|mother|dad|father|brother|sister|nan|gran|grandma|"
    r"grandad|friend|friends|mate|mates|parents?|family|hair|skin|teeth|credit)\b"
    r"|\bthings?\s+(?:with|between)\s+(?:my|his|her|their|us)\b")
LEAVING_IN_THE_LINE = re.compile(
    r"\bor\s+(?:shall|should)\s+i\s+(?:just\s+)?(?:leave|walk\s+away|split\s+up|end\s+it|"
    r"call\s+it\s+a\s+day|move\s+out|divorce)\b")
REPAIR_TARIFF = re.compile(
    r"\b(?:supplier|tariffs?|energy|electricity|gas and electric|price cap|standing charge|"
    r"mortgage|remortgag\w*|contract|deal|policy|premium|insurance|price|prices|rate|rates|"
    r"fix(?:ed|ing)?\s+(?:it\s+)?for\s+(?:one|two|three|four|five|six|a|an|\d+)\s*"
    r"(?:year|years|month|months))\b", re.I)

TRUST_ASK = re.compile(
    r"\b(?:can|could|should|would)\s+i\s+trust\s+(?:you|what\s+you|your\s+\w+|"
    r"the\s+(?:answers?|advice|things?)\s+you)\b"
    r"|\btrust\s+(?:what\s+you\s+(?:say|tell)|your\s+answers?|you\s+with)\b"
    r"|\bare\s+you\s+(?:safe|reliable|trustworthy|honest)\b"
    r"|\bis\s+(?:it|this)\s+safe\s+to\s+(?:talk|chat|speak)\s+(?:to\s+)?you\b"
    r"|\bhow\s+do\s+i\s+know\s+(?:you|that\s+you|what\s+you\s+(?:say|tell))\b"
    r"[^?!.]{0,30}?\b(?:right|true|correct|honest|telling|lying|making)\b"
    r"|\bcan\s+you\s+be\s+(?:wrong|trusted)\b|\bare\s+you\s+making\s+(?:this|that|it)\s+up\b",
    re.I)
PRIVACY_NOT_THIS = re.compile(
    r"\b(?:eat|eaten|eating|cook|cooked|cooking|freezer|fridge|left\s+out|defrost|reheat|"
    r"mouldy|moldy|smell|shelf|use\s+by|best\s+before|baby|child|kid|toddler|pregnan\w*|"
    r"drink|water|ibuprofen|paracetamol|medicine|dose|tablet|drive|driving|swim)\b", re.I)


REFERS_BACK = re.compile(
    r"\b(?:did|do|does|were|was|had|have)\s+(?:you|u)\s+(?:say|said|tell|told|mention|mean)\b|"
    r"\byou\s+(?:said|says|told|mentioned)\b")
NAMES_THE_BOT = re.compile(
    r"\b(?:ai|a\.i\.|bot|robot|chatbot|machine|computer|program|programme|algorithm|model|"
    r"human|person|people|alive|sentient|conscious|real)\b")
A_VIEW_ASKED_FOR = re.compile(
    r"^\s*(?:(?:and|so|but|ok|okay|well|honestly|then|right|also)\s+)*"
    r"(?:do|does|did|would|will)\s+(?:you|u)\s+(?:think|reckon|believe|say)\b(.*)$")
SELF_ASK = re.compile(r"\b(?:can|could|do|does|did|are|is|was|were|will|would|have|has|why|"
                      r"where|when|how\s+long)\s+(?:you|u)\b")
HUMAN_ASK = re.compile(
    r"\b(?:am i|are we|is anyone|is somebody) (?:talking|speaking|chatting|typing) (?:to|with) "
    r"(?:a |an |a real |some )*(?:human|person|real person|bot|robot|machine|computer|ai|"
    r"program)\b|"
    r"\bis (?:this|it) (?:a |an |really )*(?:real )?(?:human|person|bot|robot|machine|ai|"
    r"program|computer)\b|"
    r"\b(?:real person|actual person|human being) (?:on|at) the (?:other|end)\b")
HUMAN_TAIL = re.compile(
    r"^(?:\s*(?:or|and|not|just|really|actually|so|then|please|pls|though|right|then)\b)*"
    r"\s*(?:a |an |the )?(?:human|person|bot|robot|machine|computer|ai|program|real person|"
    r"program|chatbot|chat bot|thing|it)?\s*(?:or (?:a |an )?(?:human|person|bot|robot|"
    r"machine|computer|ai|program|chatbot|chat bot|thing))?\s*"
    r"(?:on here|in here|in this chat|on this|here|end|line|side|thanks|thank you|cheers|ok|"
    r"okay)?\s*[.!?]*\s*$")

HUMAN_HELPS = re.compile(
    r"^\s*(?:who|that|which)?\s*(?:can|could|will|would|is able to|to)\s+"
    r"(?:help|answer|sort|deal with|look at|explain|tell me|check)\b|"
    r"^\s*(?:i can (?:talk|speak|ask) to|to (?:talk|speak) (?:to|with))\b")
HUMAN_LEAD = re.compile(
    r"^\s*(?:(?:hi|hiya|hey|hello|ok|okay|so|but|and|also|sorry|wait|right|just|quick|"
    r"question|one|more|thing|to|check|first|then|is|are|am|was|were|do|does|did|there|"
    r"any|anyone|anybody|somebody|this|that|a|an|the|real|actually|really)\b[ ,]*)*$")


HUMAN_QUOTED = re.compile(r"\b(?:says|said|asks|asked|wants to know|is asking|was asking|"
                          r"keeps asking|texted)\s*$")
TRIED_THE_LOT = re.compile(
    r"^(?:(?:ok|okay|alright|right|so|well|yeah|yep|yes|cool|fine|and|but|then|i|we|ive|i've|"
    r"weve|we've)\s+)*"
    r"(?:(?:have|had|did)\s+)?(?:tried|been trying|done|did)\s+"
    r"(?:them all|it all|everything|the lot|all of (?:it|them|those|these)|both)\b")
DONE_IT = re.compile(
    r"^(?:(?:ok|okay|alright|right|so|well|yeah|yep|yes|cool|fine|and|but|then|"
    r"i|we|ive|i've|weve|we've)\s+)*"
    r"(?:(?:have|had)\s+)?(?:done|did)\s+(?:it|that|this|them)\b")


REFUSED = re.compile(
    r"\b(?:said|says|saying|told\s+me)\s+no\b"
    r"|\b(?:turned|turns)\s+(?:me|it|us|him|her|them)\s+down\b"
    r"|\b(?:knocked|knocks)\s+(?:me|it|us|them)\s+back\b"
    r"|\bno\s+(?:for\s+an\s+answer|was\s+the\s+answer)\b"
    r"|\b(?:he|she|they|we|the\s+\w+|my\s+\w+)\s+refused\b"
    r"|\b(?:wouldnt|wouldn't|wont|won't)\s+(?:budge|bend|agree|have\s+it|do\s+it|come\s+round)\b",
    re.I)
REFUSED_NOT = re.compile(
    r"\b(?:doctor|gp|nurse|consultant|midwife|surgeon|physio\w*|pharmacist|chemist|dentist|"
    r"hospital|surgery|clinic|111|a&e|ae|paramedic\w*)\b", re.I)
OWN_NO = re.compile(
    r"\b(?:i|we|ive|i've|weve|we've)\b[^.!?]{0,12}?\b(?:said|says|told|tells?|turned|refused|"
    r"knocked)\b[^.!?]{0,12}?\bno\b"
    r"|\b(?:i|we)\b[^.!?]{0,12}?\b(?:refused|turned\s+\w+\s+down)\b", re.I)
REFUSED_FAMILY = re.compile(
    r"\b(?:husband|wife|partner|boyfriend|girlfriend|fiance|fiancee|ex|exes|mum|mom|mother|dad|"
    r"father|son|daughter|sister|brother|mate|friend|flatmate|housemate|roommate|stepdad|"
    r"stepmum|stepmother|stepfather|gran|granny|nan|nana|grandad|grandpa|grandma|"
    r"uncle|aunt|auntie|cousin|in-law|in\s+laws)\b", re.I)
REFUSED_PARTY = re.compile(
    r"\b(?:boss|manager|managers|employer|employers|hr|personnel|bank|banks|building\s+society|"
    r"council|councils|landlord|landlady|letting\s+agent|jobcentre|job\s+centre|dwp|"
    r"panel|committee|board|union|university|uni|college|school|nursery|shop|store|retailer|"
    r"seller|supplier|insurer|insurance|agent|agency|recruiter|firm|company|office|"
    r"department|court|tribunal|ombudsman|clinic|hospital|charity|club|gym|council\s+tax|"
    r"mortgage\s+company|housing\s+association|benefits\s+office)\b", re.I)
REFUSED_NO_OBJECT = re.compile(
    r"\b(?:said|says|saying|told\s+me)\s+no\s+(?!(?:way|chance|deal|thanks|thank|worries|"
    r"problem|dice|objection|to|about|on|again|twice|either|yet|at|for\s+now|so|and|but|then|"
    r"though|after|before|last|this|it|because|when|until|unless)\b)[a-z]", re.I)
AN_ANSWER_ABOUT_A_NO = re.compile(
    r"\b(?:dispute[ds]?|disputing|appeal|complain\w*|complaint\w*|ombudsman|tribunal|"
    r"small\s+claims|letter\s+before\s+action|trading\s+standards|protection\s+scheme|"
    r"escalate|raise\s+it\s+with\s+the\s+council)\b", re.I)
ASKS_WHY = re.compile(r"^(?:why|how|what|when|where|who|did|does|do|is|are|was|were|can|could|"
                      r"should|would|will|any\s+idea)\b", re.I)
HYPOTHETICAL = re.compile(
    r"\b(?:what\s+if|if|suppose|supposing|supposed|in\s+case|unless|should|were\s+to|may|might|"
    r"would|what\s+happens\s+(?:if|when)|when)\b(?:\s+\w+){0,5}\s*$", re.I)


FEELS_BETTER = re.compile(
    r"\b(?:i|im|i'?m|we|we'?re|feeling|feel|doing|getting|its|it'?s)\b[^.?!]{0,24}"
    r"\b(?:better|calmer|calm|alright|okay|ok|fine|easier|lighter|less\s+(?:awful|bad))\b"
    r"|\b(?:better|calmer)\s+(?:now|today|tonight|thanks)\b"
    r"|\b(?:(?:just\s+)?a\s+(?:bit|little|touch|lot)|lots|much|slightly|way|far)\s+"
    r"(?:better|calmer|easier|lighter)\b"
    r"|\b(?:its|it'?s|it is)\s+easing\b")
FEELS_NOT_BETTER = re.compile(
    r"\b(?:don'?t|doesn'?t|not|never|still|worse|no better|not any)\b")
MOVE_ON = re.compile(r"\b(?:something else|something different|change the subject|move on|"
                     r"different topic|another topic|talk about anything|talk about something|"
                     r"nothing else)\b")

STILL_GOING = re.compile(r"\b(?:still|keeps?|kept|stopped|stops|worse|worsening|again|"
                         r"hasn't|has not|haven't|have not|won't)\b")

CARE_SEEN_ASKS = re.compile(
    r"\b(?:should|shall|do|does|need|needs|have to|got to) (?:i|we|it|this)\b[^.?!]*"
    r"\b(?:go|a&e|stitches|checked|seen|hospital|doctor|walk-in|later|tonight)\b"
    r"|\bdo (?:i|we) need\b|\bam i being (?:silly|daft)\b")
IN_HOSPITAL = re.compile(
    r"\b(?:hospital|ward|casualty|admitted|admission|intensive care|icu|hdu|hospice|"
    r"a\s*&\s*e|a and e|aande|ambulance|in for tests|in for an operation|"
    r"having an operation|on a drip|taken in)\b")
VISIT_ASK = re.compile(
    r"\b(?:go|come|get) (?:up|over|round|across|down)\b"
    r"|\bgo (?:and )?see\b|\bvisit(?:ing)?\b")
NOT_A_VISIT = re.compile(
    r"\b(?:go|come|get|walk|climb|run)\s+(?:up|down)\s+(?:and\s+(?:down|up)\s+)?"
    r"(?:the\s+|a\s+|my\s+|these\s+|those\s+)?"
    r"(?:stairs?|staircase|steps?|ladder|hill|slope|ramp|stile|loft|scaffold)\b"
    r"|\b(?:go|get|come)\s+up\s+(?:to\s+)?(?:bed|my room|the bedroom)\b")
MEDICAL_PLACE = re.compile(
    r"\b(?:hospital|casualty|ward|clinic|surgery|doctor|doctors|gp|walk[\s-]?in|out of "
    r"hours|a\s*&\s*e|a and e|aande|ae|999|111)\b")
BURN_ON_IT = re.compile(
    r"\b(?:put|rub|smear|spread|dab)\b[^.?!]{0,30}\b(?:on|over) (?:it|them|that|there)\b"
    r"|\b(?:cover|wrap|dress|bandage)\b[^.?!]{0,20}\b(?:it|them|that|the burn)\b")
BURN_THING = re.compile(r"\b(?:cream|ointment|antiseptic|butter|toothpaste|ice|ice ?pack|"
                        r"plaster|dressing)\b")
BURN_ASK = re.compile(r"\b(?:should|can|could|do|would|will|is|are)\s+(?:i|we|it|they)\b"
                      r"|\?")
BURN_BLISTER_LINE = re.compile(
    r"\b(?:pop|piercing|pierce|burst|drain|squeeze|lance)\b[^.?!]{0,20}\b(?:blister|bubble)\b"
    r"|\bblister\b[^.?!]{0,20}\b(?:pop|burst|drain|squeeze)\b")
BURN_WORD = re.compile(r"\b(?:burns?|burnt|burned|burning|scald(?:s|ed|ing)?|"
                       r"sunburn(?:s|ed|t)?|sunburnt)\b")
POP_A_BARE_IT = re.compile(r"\b(?:pop|pierce|burst|drain|lance|squeeze)\b[^.?!]{0,12}"
                           r"\b(?:it|that|them|this)\b")
ADVICE_TIME_ASK = re.compile(
    r"\b(?:is|are|was)\s+(?:\d+|one|two|three|four|five|ten|fifteen|twenty|thirty|forty)\s*"
    r"(?:min|mins|minutes?|secs?|seconds?)\s+(?:enough|too\s+(?:long|short|much|little)|"
    r"ok|okay|fine)\b"
    r"|\bis\s+(?:that|this|it)\s+long\s+enough\b"
    r"|\bhow\s+long\s+(?:should|shall|do|can|must|need)\s+(?:i|we)\s+"
    r"(?:hold|keep|leave|stay|run|do|press|put)\b"
    r"|\bhow\s+long\s+does\s+it\s+(?:need|take|have\s+to\s+be)\b"
    r"|\bdoes\s+it\s+have\s+to\s+be\s+that\s+long\b"
    r"|\b(?:can|could|should)\s+i\s+stop\s+(?:early|now|sooner)\b")
ADVICE_COOL_ASK = re.compile(
    r"\b(?:lukewarm|tepid)\b"
    r"|\b(?:cold|cool|warm|hot)\s+water\b"
    r"|\bdoes\s+it\s+have\s+to\s+be\s+(?:cold|cool|warm)\b"
    r"|\bis\s+(?:cold|cool|warm)\s+(?:ok|okay|fine|enough)\b")
ADVICE_TIME_WORDS = re.compile(
    r"\b(?:\d+|one|two|three|five|ten|fifteen|twenty|thirty)\s*"
    r"(?:minutes?|mins?|seconds?|secs?)\b")
ADVICE_AGAIN_ASK = re.compile(
    r"\b(?:can|could|should|shall|do)\s+i\s+(?:do|have|start|try|run|hold|press)\s+"
    r"(?:it|that|this)\s+(?:again|twice)\b"
    r"|\bdo\s+i\s+need\s+to\s+(?:do|start|repeat)\s+(?:it|that)\s+again\b"
    r"|\b(?:can|could|should)\s+i\s+(?:do|have|run)\s+(?:another|a\s+second)\b")
ADVICE_WORSE_ASK = re.compile(
    r"\bwhat\s+if\s+(?:it|that|this|the\s+bleeding|the\s+pain)\s+"
    r"(?:doesnt|does\s+not|didnt|wont|won't|still\s+doesnt)\s+"
    r"(?:stop|work|settle|ease|help|go\s+away|slow)\b"
    r"|\bwhat\s+if\s+(?:it|that)\s+keeps?\s+(?:going|bleeding|hurting|burning)\b")
