import re

from . import pick, trouble
from .fallback_data import A_THING_TAKEN
from ..memory import facts
from ..understanding.kinds import OTHER_PEOPLE
from ..understanding.normalize import without_leaders

PLAN = (
    "planning", "plan to", "planning to", "book a", "save up",
    "saving up", "saving for", "applying", "apply for",
)
BOOKED = re.compile(r"\bbook(?:ed|ing)\b")
STEP_NOUNS = frozenset((
    "venue", "venues", "hall", "reception", "caterer", "caterers", "band", "dj",
    "photographer", "tickets", "flights", "flight", "hotel", "room", "table", "minibus",
))
BIGGER_PLAN = frozenset((
    "wedding", "weddings", "venue", "honeymoon", "holiday", "trip", "course", "reception",
    "mortgage", "house", "move", "moving", "exam", "exams",
))
ARRANGEMENT = frozenset(("visit", "visiting", "visits"))
GOING_TO = ("going to ", "gonna ", "want to ", "wanting to ", "would like to ", "hoping to ",
            "thinking of ", "thinking about ")
PLANNED_VERBS = frozenset((
    "start", "move", "save", "buy", "learn", "book", "travel", "visit", "change",
    "quit", "sell", "apply", "build", "train", "study", "open", "join",
    "switch", "retrain", "volunteer", "emigrate", "adopt", "redecorate",
    "renovate", "downsize", "sort", "fix", "paint", "clear", "declutter", "budget",
    "insulate", "convert", "rent", "plant", "grow", "write",
))
NOT_PLAIN = frozenset((
    "died", "dying", "dead", "death", "passed", "funeral", "buried", "miscarriage",
    "cancer", "tumour", "tumor", "diagnosis", "hospital", "icu", "hospice", "suicide",
    "overdose", "abuse", "beaten", "assaulted", "attacked", "emergency", "ambulance",
    "bleeding", "chest", "stroke", "seizure", "unconscious", "miscarried", "grieving",
    "miscarrying", "divorce", "custody",
    "abortion", "abortions", "termination", "terminations", "crematorium", "cremation",
    "cremations", "stillbirth", "ectopic", "coffin",
    "scan", "appointment", "consultant", "clinic", "surgery", "gp", "doctor", "midwife",
    "chemo", "treatment", "results", "biopsy", "operation", "ward",
    "petrol", "gas", "gas leak", "fumes", "smoke", "smoking", "burning", "carbon",
    "monoxide", "sparks", "wiring", "fire",
    "breath", "breathless", "breathing", "breathlessly", "wheeze", "wheezing", "cough",
    "coughing", "dizzy", "faint", "palpitations", "pain", "hurts", "aching", "sore",
))
COUNTERFACTUAL = (
    "would have been", "would've been", "would have turned", "wouldve been",
    "should have been", "never got to", "if only",
)
MARKED_DATE = frozenset(("anniversary", "birthday", "birthdays", "remembrance", "memorial"))
CRISIS = (
    "want to die", "wanna die", "kill myself", "end it all", "end my life", "no point",
    "hurt myself", "self harm", "not worth living", "better off dead", "be here anymore",
    "dont want to be here", "don't want to be here", "dont want to wake up",
    "better off without me", "no way out", "tired of living", "cant go on", "overdosing",
)

ASKS = frozenset((
    "what", "whats", "which", "why", "how", "when", "where", "who", "whos", "ideas", "idea",
    "suggest", "suggestions", "recommend", "advice", "tips", "anyone", "anybody", "shout",
))
DOUBT = (
    "dont know", "don't know", "not sure", "unsure", "whether", "if i", "should i",
    "no idea", "in two minds", "not certain",
    "dont want", "don't want", "do not want", "dont fancy", "don't fancy",
    "leaving my husband", "leaving my wife", "leaving my partner", "leave my husband",
    "leave my wife", "leave my partner", "keep thinking about leaving", "thinking of leaving",
    "leaving him", "leaving her", "walking out on", "keep planning", "always planning",
    "never do", "never follow through", "things i never",
)
BARRIER = (
    "but", "except", "only", "never", "dont have", "don't have", "havent got",
    "haven't got", "cant", "can't", "no money", "no time", "too late", "already tried",
)
PLAN_REPLIES_PLAIN = (
    "Good. What's the first step you're unsure about?",
    "Sounds like a good plan. What's the bit you're least sure about?",
)

PLAN_REPLIES = (
    "Good. What's the first step you're unsure about?",
    "Nice — worth doing properly. What would you want sorted out first?",
    "Worth deciding what the first step is, and what you'd count as done.",
    "Sounds like a good plan. What's the bit you're least sure about?",
)


DEPENDANT = frozenset("""
son daughter child children kid kids toddler teenager teen lad boy girl baby grandson
stepson stepdaughter granddaughter mum mom mother father dad wife husband partner grandchild
nephew niece
""".split())
DEPENDANT_WANT = re.compile(
    r"\b(?:my|our|his|her|their)\s+(?:" + "|".join(sorted(DEPENDANT)) + r")\b[^.!?]*?\b(?:"
    r"wants?|wanted|needs?|would\s+like|would\s+love|is\s+desperate\s+for|keeps\s+asking\s+for|"
    r"is\s+asking\s+for)\b", re.I)
ASKED_OF_THE_PERSON = re.compile(r"\b(?:wants?|needs?|would\s+like)\s+(?:me|us)\b", re.I)
WANTS_TO_BE = re.compile(r"\bwants?\s+to\s+be\b", re.I)
A_WEAPON = frozenset("""
gun guns shotgun shotguns pistol pistols handgun handguns revolver revolvers firearm firearms
airgun airguns rifle rifles crossbow crossbows machete machetes taser tasers knuckleduster
""".split())
WEAPON_WORDS = frozenset(("knife", "knives", "blade", "blades", "sword", "swords"))
NOT_A_WEAPON = (
    "cooking", "cook", "chef", "kitchen", "carving", "whittling", "craft", "fishing",
    "camping", "garden", "bread", "sharpening", "cutlery",
)
A_LOSS_IN_THE_LINE = re.compile(
    r"\b(?:died|dying|death|dead|passed\s+away|funeral|hospice|terminal|bereave\w*|widow\w*|"
    r"cancer)\b", re.I)
A_CONDOLENCE = re.compile(
    r"\bi(?:'m|\s+am)\s+(?:really\s+|so\s+|very\s+)?sorry\b|\bsorry\s+for\s+your\s+loss\b",
    re.I)

DEPENDANT_WANT_REPLIES = (
    "Then start with what it would really take - the price, and what the rules allow - before "
    "anyone says yes or no. What has been looked at so far?",
    "The asking is the easy half. Price it and check the rules first, because those two decide it "
    "more often than the wanting does.",
    "Ask what it is really for first - the thing itself and what it gets them are different "
    "problems. What has been said so far?",
)



SETBACK = re.compile(
    r"\b(?:was|were|got|went|kept|had)\s+(?:\w+\s+){0,2}?"
    r"(?:late|shut|closed|cancell?ed|delayed|sold\s+out|broken|bust|packed\s+in|"
    r"refused|rejected|declined|postponed|overbooked|queueing|queuing|back\s+in|"
    r"let\s+(?:me|us)\s+down)\b"
    r"|\b(?:broke\s+down|packed\s+in|gave\s+up\s+the\s+ghost|ran\s+out|"
    r"fell\s+through|let\s+(?:me|us)\s+down|missed\s+(?:the|my|a|our)\s+\w+)\b")
RISE = re.compile(r"\b(?:went|gone|goes|has\s+gone|have\s+gone|has\s+went|have\s+went)\s+up\b")
PRICE = frozenset("""
rent price prices gas electric electricity bill bills rate rates cost costs fare fares interest
mortgage insurance heating petrol fuel diesel food shopping council tax stamp fees fee nursery
""".split())
MISSED = re.compile(r"\bmissed\s+(?:the|my|a|our|his|her|their)?\s*(\w+)")
OWN_SLIP = re.compile(r"\bmissed\s+(?:the|my|a|our)\s+"
                      r"(?:deadline|deadlines|cut-?off|interview)\b")
DEADLINE_LATER = re.compile(r"\b(?:accounts|confirmation\s+statement|companies\s+house|"
                            r"annual\s+return|self\s+assessment|statutory\s+accounts|"
                            r"filing|court|hearing|tribunal)\b")
PRESENT_SETBACK = re.compile(
    r"\b(?:is|are|keeps?|kept)\s+(?:\w+\s+){0,2}?"
    r"(?:broken|shut|closed|cancell?ed|delayed|off|down|out\s+of\s+order|full|sold\s+out)\b")
BURGLED = re.compile(r"\b(?:burgled|burglary)\b"
                     r"|\b(?:broken\s+into|broke\s+into|broken\s+in\s+and|break-?in\b)", re.I)
BURGLED_HOME = re.compile(r"\b(?:house|home|flat|apartment|place|maisonette|bedsit|caravan|"
                          r"bungalow|cottage|rented|landlady|landlord)\b", re.I)
NOT_A_BREAK_IN = frozenset((
    "shed", "garage", "gate", "cupboard", "door", "doors", "lock", "window", "windows",
    "boot", "car", "van", "bike", "motorbike", "bicycle", "allotment", "container",
    "bin", "suitcase", "locker", "box", "wardrobe", "safe", "parcel", "packet",
))
BURGLED_SOMEONE_ELSE = re.compile(
    r"\b(?:my|his|her|their|our|the)\s+(?:mum|mom|dad|sister|brother|son|daughter|friend|mate|"
    r"nan|gran|grandma|grandad|granny|aunt|uncle|cousin|partner|husband|wife|boyfriend|"
    r"girlfriend|parents?|neighbours?|in-laws?|family|in-laws?)\b"
    r"|\b(?:a\s+mate|a\s+friend)\b"
    r"|\bthey\s+(?:were|got|have\s+been|had\s+been)\s+(?:burgled|broken\s+into)\b", re.I)
BURGLED_NOT_THEIRS = re.compile(
    r"\b(?:on\s+(?:our|my|the)\s+(?:street|road|estate|avenue|close)|next\s+door|"
    r"round\s+the\s+corner|down\s+the\s+road|in\s+the\s+area|locally|nearby)\b", re.I)
BARE_SETBACK = re.compile(
    r"\b(?:shut|closed|cancell?ed|delayed|sold\s+out)\s+"
    r"(?:early|late|today|yesterday|again|on\s+me|before\s+(?:i|we)\s+(?:got|arrived))\b"
    r"|\bnever\s+(?:turned\s+up|showed\s+up)\b"
    r"|\b(?:(?:was|were|got|has|have|had)\s+(?:been\s+)?"
    r"(?:nicked|stolen|pinched))\b")
NEVER_CAME_SUBJECT = re.compile(
    r"\b(?:i|you|he|she|we|they|him|her|them|mum|mom|dad|my\s+(?:mum|mom|dad|sister|brother|"
    r"son|daughter|friend|mate|partner|husband|wife|boyfriend|girlfriend))\s+never\s+"
    r"(?:turned\s+up|showed\s+up)\b")
DONE_TO_ME = re.compile(
    r"\b(?:got|was|were|has been|have been|had been)\s+(?:\w+\s+){0,2}?"
    r"(?:pickpocketed|pick-?pocketed|keyed|scratch(?:ed)?|dented|chipped|cracked|smashed|"
    r"slashed|vandalised|vandalized|damaged|towed|clamped)\b"
    r"|\b(?:my|our)\s+(?:\w+\s+){0,3}?"
    r"(?:ran off|ran away|bolted|escaped|got out|wandered off|went missing|gone missing|"
    r"disappeared|vanished|cracked|stopped working|packed in)\b"
    r"|\bi\s+(?:chipped|cracked|broke|knocked out|lost)\s+(?:a|an|my|one of my|two)\s+\w+\b")
SMASHED = re.compile(r"\bsmashed\b")
SMASHED_OF_A_THING = re.compile(
    r"\b(?:my|our|the|his|her|their|its)\s+(?:\w+\s+){0,3}?"
    r"(?:got|was|were|has\s+been|had\s+been|smashed|broken|shattered)\b")
A_GROUP_OF_PEOPLE = re.compile(
    r"\b(?:my|our|the|his|her|their)\s+(?:team|side|club|lot|lads|boys|girls|mates|friends|"
    r"family|kids|children|crowd|opposition|squad|band)\b")


A_PERSON_OF_THEIRS = re.compile(
    r"\b(?:my|our)\s+(?:boss|manager|mum|mom|mother|dad|father|son|daughter|boy|girl|kid|kids|"
    r"child|children|husband|wife|partner|boyfriend|girlfriend|ex|brother|sister|mate|mates|"
    r"friend|friends|colleague|colleagues|coworker|coworkers|nana|nan|gran|grandad|"
    r"grandma|grandpa|aunt|uncle|cousin|neighbour|neighbor|landlord|landlady|flatmate|housemate|"
    r"teenager|baby|toddler)\b")
A_PERSON_LOST = re.compile(r"\b(?:went\s+missing|gone\s+missing|disappeared|vanished)\b")
CRACKED_A_JOKE = re.compile(
    r"\bcracked\s+(?:a|up|his|her|their|its)\s*(?:joke|smile|grin|laugh|voice|wise)"
    r"|\bcracked\s+(?:on|it)\b")
A_THING_CARRIED_OFF = re.compile(
    r"\b(?:ran|ran\s+off|ran\s+away|got\s+out|escaped|went\s+off|cracked|smashed|broke)\s+"
    r"(?:with|out)\s+(?:my|our|the)\b"
    r"|\b(?:cracked|smashed|broke|dented|scratched|chipped)\s+(?:open\s+)?(?:my|our)\b")


A_NIGHT_OUT = re.compile(
    r"\b(?:party|pub|night\s+out|works\s+do|wedding|stag|hen|club|bar|drinks|round|celebration)\b")


def _a_good_night_out(clean):
    if not SMASHED.search(clean):
        return False
    if not SMASHED_OF_A_THING.search(clean):
        return True
    if A_GROUP_OF_PEOPLE.search(clean):
        return bool(A_NIGHT_OUT.search(clean))
    return False


def done_to_me(clean):
    if not DONE_TO_ME.search(clean) or _a_good_night_out(clean) or CRACKED_A_JOKE.search(clean):
        return False
    if A_PERSON_OF_THEIRS.search(clean) and not A_PERSON_LOST.search(clean) \
            and not A_THING_CARRIED_OFF.search(clean):
        return False
    return True

REPORT_BODY = frozenset((
    "sick", "ill", "unwell", "poorly", "vomit", "vomiting", "sickness", "fever", "temperature",
    "flu", "cough", "cold", "bug", "hospital", "ambulance", "a&e", "999", "111", "doctor",
    "gp", "nurse", "midwife", "pain", "hurts", "hurting", "ache", "aching", "sore", "swollen",
    "bleeding", "blood", "dizzy", "faint", "fainted", "breathless", "seizure", "fit", "rash",
    "chest", "stroke", "allergic", "reaction", "concussion", "wound", "burn", "burnt",
))
STARTED_VERDICT = re.compile(
    r"\b(?:was|is|went|were|been|going|getting|seems|looks)\s+(?:\w+\s+){0,2}?"
    r"(?:fine|good|great|ok|okay|well|alright|amazing|lovely|brilliant|easy|hard|tough|"
    r"awful|terrible)\b")

STARTED_GONE_BADLY = re.compile(
    r"\b(?:problem|problems|trouble|troubles|teething|snag|snags|hiccup|hiccups|issue|issues)\b"
    r"|\b(?:hate|hates|hating|dread|dreading)\b"
    r"|\b(?:going|gone|went|is|was|been|getting|feels?)\s+(?:\w+\s+){0,2}?"
    r"(?:badly|bad|awful|terrible|horrible|rough|hard|tough|stressful|draining|exhausting|"
    r"rubbish|pants)\b")
AGAIN = re.compile(r"\b(?:again|again\s+today|again\s+this\s+(?:week|morning|time)|"
                   r"third\s+time|second\s+time|every\s+\w+\s+now|once\s+more)\b")
STARTED = re.compile(
    r"\bstart(?:ed|ing)?\s+(?:a\s+|my\s+|his\s+|her\s+|their\s+|the\s+)?(?:new\s+)?"
    r"(?:job|work|course|college|uni|university|school|placement|apprenticeship|shift|"
    r"contract|role|internship|training)\b"
    r"|\bnew\s+(?:job|role|position)\b"
    r"|\bfirst\s+(?:day|week|shift)\b")
_AHEAD_DAY = (r"(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday|"
              r"january|february|march|april|may|june|july|august|september|october|november|"
              r"december)")
START_AHEAD = re.compile(
    r"\b(?:(?:on|next|this)\s+" + _AHEAD_DAY + r"|"
    r"(?:next|this)\s+(?:week|weekend|month|year|term|afternoon|evening)|"
    r"tomorrow|tonight|soon|"
    r"in\s+(?:a|an|one|two|three|four|five|six|seven|eight|nine|ten|\d+)\s+"
    r"(?:day|days|week|weeks|month|months)|"
    r"in\s+" + _AHEAD_DAY + r"|"
    r"(?:is|are)\s+(?:on\s+|this\s+|next\s+)?" + _AHEAD_DAY + r"|"
    r"(?:is|are)\s+(?:tomorrow|tonight))\b", re.I)
START_PAST = re.compile(r"\b(?:started|began|begun)\b", re.I)
START_PRESENT = re.compile(r"\b(?:start|starts|starting|begin|begins|beginning)\b", re.I)
START_CLOCK = re.compile(r"\bat\s+\d{1,2}(?::\d{2})?\b|\b\d{1,2}\s*o'?clock\b", re.I)
REPORT_FEELING = frozenset((
    "happy", "glad", "sad", "gutted", "scared", "afraid", "worried", "angry", "furious",
    "annoyed", "frustrated", "upset", "excited", "proud", "relieved", "tired", "exhausted",
    "fed", "sick", "awful", "terrible", "worst", "great", "brilliant", "amazing", "love",
    "hate", "cried", "crying", "tears", "worst", "nightmare", "disaster", "stress",
    "stressed", "anxious", "panic", "worst", "sorry", "unfortunately", "gutted",
))

TAKEN_FROM_THEM = re.compile(
    r"\b(?:(?:my|our|his|her|their|the)\s+\w+\s+(?:was|were|got|has|have|had)\s+"
    r"(?:been\s+)?(?:nicked|stolen|swiped|pinched|lifted|thieved|snaffled|taken))\b"
    r"|\bi\s+had\s+(?:my|our|his|her|their)\s+\w+\s+"
    r"(?:nicked|stolen|swiped|pinched|lifted|thieved|snaffled|taken)\b"
    r"|\b(?:someone|somebody|some\s+(?:lad|bloke|kid|guy|person|scrote)|they)\s+"
    r"(?:nicked|stole|swiped|pinched|lifted|took|thieved|snaffled)\b")

NOT_A_LOSS = re.compile(
    r"\b(?:table|seat|seats|place|places|order|orders|turn|call|name|names|number|photo|photos|"
    r"picture|pictures|temperature|blood|bloods|details|booking|form|form\s+in|payment|"
    r"space|spaces|spot|spots|parking|slot|slots)\b")

TOOK_IT_IN = re.compile(r"\b(?:took|taken|takes|take)\b[^.]{0,25}\bin\b(?!\s+(?:the\s+)?"
                        r"(?:night|morning|afternoon|evening|day|daylight|hours|town|time|future|"
                        r"error|haste|early|late|later)\b)")


def _a_thing_taken(clean):
    text = " ".join(str(clean or "").lower().split())
    if not text or not TAKEN_FROM_THEM.search(text):
        return False
    return not NOT_A_LOSS.search(text) and not TOOK_IT_IN.search(text)


LOSS_FOLLOW = re.compile(
    r"\bcards?\b|\bcash\b|\bmoney\b|\bkey|\bkeys\b|\bphone\b|\bwallet\b|\bpurse\b|"
    r"\bbag\b|\bbike\b|\bpassport\b|\binsurance\b|\binsurer\b|\bclaim\b|\bpolice\b|"
    r"\bblock|\bfreez|\bcancel|\bbank\b|\blaptop\b|\bcar\b|\bvan\b|\btools?\b")
LOSS_FOLLOW_REPLIES = (
    "Then stop the cards before anything else - most banking apps freeze them in one tap, and it "
    "is quicker than the phone queue. Ring 101 for a crime reference number and keep it, because "
    "the bank and the insurer both ask for it by name.",
    "Money and cards are the urgent part: freeze them in the app now, then ring the bank and say "
    "taken, not lost. A stolen card is handled differently from one left on a bus, and the "
    "difference is the crime reference.",
    "Insurance next, while it is fresh. The insurer wants the crime reference, a list of what "
    "went, and whatever receipts or photos you can find - and anything else damaged wants "
    "photographing before it is tidied up.",
)


def _the_loss_was_asked(memory):
    turns = [t for t in ((memory or {}).get("turns") or []) if isinstance(t, dict)]
    last = str((turns[-1] if turns else {}).get("bot") or "").strip()
    return last in A_THING_TAKEN


def _the_answers_take_it(clean):
    try:
        from ..modules import answers

        return answers.respond(clean, {}) is not None
    except Exception:
        return False


SETBACK_REPLIES = (
    "Oh, that's a nuisance.",
    "That's a pain.",
    "Rotten luck.",
    "Ugh, that's annoying.",
)
AGAIN_REPLIES = (
    "Again? That's a pain.",
    "Again - that's annoying.",
    "Again. That's a nuisance.",
    "That keeps happening, then. Do you know why?",
    "Again? Has it been like that a while?",
)
STARTED_REPLIES = (
    "Nice. How's it going so far?",
    "Good. How were the first days?",
    "Nice one. How's it treating you?",
    "Good luck with it - how has the first week been?",
)
STARTED_AHEAD_REPLIES = (
    "Good luck with it - how are you feeling about it?",
    "Nice. What are you looking forward to?",
    "Good luck on the day. Anything you want sorted before then?",
    "A fresh start, then. What is the first thing you will do?",
    "Nice one. Are you looking forward to it, or dreading it a bit?",
)
BURGLED_REPLIES = (
    "That's a horrible thing to come back to. Ring the police first and get a crime reference "
    "number - the insurer asks for it - and tell the insurer before you clear anything up.",
    "I'm sorry. Report it and get a crime reference number, then ring the insurer: they want to "
    "know before anything is tidied away, and they ask for that number first.",
    "Awful. The order that matters is the police for a crime reference number, then the insurer, "
    "before you touch anything.",
)
BURGLED_FOR_SOMEONE_REPLIES = (
    "That's a horrible thing to happen to them. Are they all right, and is someone with them?",
    "Awful for them. Do they have somebody there with them tonight?",
    "That's a nasty thing to go through. How are they holding up?",
)
SLIP_REPLIES = (
    "Deadlines do that. How much time is left?",
    "It happens. What can you still get in?",
    "Easy to lose track of one. What is left to do?",
)
STARTED_FINE_REPLIES = (
    "Good - glad it's going all right.",
    "Nice one. Sounds like a good start.",
    "Good to hear it.",
)
STARTED_BADLY_REPLIES = (
    "That's a rough start. What's going wrong with it?",
    "Sorry it's been like that. What's the worst of it?",
    "Ah, that's a shame this early on. What's not working?",
    "A rough first stretch. What would make it easier?",
)


def _missed_a_person(clean):
    for match in MISSED.finditer(clean):
        if match.group(1) in OTHER_PEOPLE:
            return True
    return False


def reads_as_report(clean, words):
    if not clean or "?" in clean:
        return None
    if set(words) & REPORT_FEELING or set(words) & REPORT_BODY:
        return None
    if _missed_a_person(clean):
        return None
    if _reads_as_a_break_in(clean, words):
        return "burgled"
    if STARTED.search(clean):
        return "started"
    if OWN_SLIP.search(clean):
        return "slip"
    if MISSED.search(clean) and DEADLINE_LATER.search(clean):
        return "slip"
    if BARE_SETBACK.search(clean) and NEVER_CAME_SUBJECT.search(clean):
        return "again" if AGAIN.search(clean) else None
    if (SETBACK.search(clean) or BARE_SETBACK.search(clean) or done_to_me(clean)
            or (RISE.search(clean) and set(words) & PRICE)):
        return "again" if AGAIN.search(clean) else "setback"
    if AGAIN.search(clean) and PRESENT_SETBACK.search(clean):
        return "again"
    return None


def _still_to_come(clean):
    if START_PAST.search(clean) or START_CLOCK.search(clean):
        return False
    return bool(START_AHEAD.search(clean) or START_PRESENT.search(clean))


STARTED_WELL = re.compile(
    r"\b(?:fine|good|great|ok|okay|well|alright|amazing|lovely|brilliant|easy)\b")
FIRST_STRETCH = re.compile(r"\bfirst\s+(?:day|week|shift|month)\b")


def _started_badly(clean):
    bad = STARTED_GONE_BADLY.search(clean)
    if not bad:
        return False
    return STARTED_WELL.search(clean, bad.end()) is None


def _reads_as_a_break_in(clean, words):
    if not BURGLED.search(clean):
        return False
    if BURGLED_NOT_THEIRS.search(clean) and not BURGLED_SOMEONE_ELSE.search(clean):
        return False
    if re.search(r"\b(?:burgled|burglary)\b", clean, re.I):
        return True
    if set(words) & NOT_A_BREAK_IN:
        return False
    return bool(BURGLED_HOME.search(clean)) or bool(
        re.search(r"\b(?:i|we|they)\s+(?:was|were|got|have\s+been|had\s+been)\s+"
                  r"(?:broken\s+into|broken\s+in)\b", clean))


def break_in_reply_for(clean, words, memory):
    if not _reads_as_a_break_in(clean, words):
        return None
    pool = (BURGLED_FOR_SOMEONE_REPLIES if BURGLED_SOMEONE_ELSE.search(clean)
            else BURGLED_REPLIES)
    return pick(pool, memory, clean)


def report_reply_for(clean, words, memory):
    if set(words) & NOT_PLAIN or _has_phrase(clean, CRISIS):
        return None
    if _has_phrase(clean, COUNTERFACTUAL) or set(words) & MARKED_DATE:
        return None
    if set(words) & ASKS or _has_phrase(clean, DOUBT):
        return None
    shape = reads_as_report(clean, words)
    if shape == "burgled":
        return break_in_reply_for(clean, words, memory)
    if _a_thing_taken(clean) and not _the_answers_take_it(clean):
        return pick(A_THING_TAKEN, memory, clean)
    if _the_loss_was_asked(memory) and not set(words) & ASKS and LOSS_FOLLOW.search(clean):
        return pick(LOSS_FOLLOW_REPLIES, memory, clean)
    if not shape:
        return None
    if shape != "started" and trouble.reads_as_trouble(clean, words, clean):
        return None
    if shape == "started" and _started_badly(clean):
        if FIRST_STRETCH.search(clean):
            return None
        return pick(STARTED_BADLY_REPLIES, memory, clean)
    if shape == "started" and STARTED_VERDICT.search(clean):
        return pick(STARTED_FINE_REPLIES, memory, clean)
    if shape == "started" and _still_to_come(clean):
        return pick(STARTED_AHEAD_REPLIES, memory, clean)
    pool = {"setback": SETBACK_REPLIES, "again": AGAIN_REPLIES,
            "started": STARTED_REPLIES, "slip": SLIP_REPLIES}[shape]
    if _asked_last(memory) and shape != "started":
        pool = tuple(o for o in pool if not o.endswith("?")) or pool
    return pick(pool, memory, clean)


REGRET = re.compile(r"""
    \bregrets?\b | \bregretted\b | \bregretting\b
  | \bwish\s+(?:i|we)\s+(?:had|did)\s*(?:n'?t|nt| not)\b
  | \bwish\s+(?:i|we)\s+had\s+(?!a\b|an\b|the\b|more\b|enough\b|some\b|any\b|no\b
                                     |another\b|my\b|your\b|his\b|her\b|their\b|our\b
                                     |one\b|two\b|three\b|\d)\w+\b
  | \b(?:not|never)\s+sure\s+(?:i|we)\s+(?:should|ought\s+to)\b
""", re.VERBOSE)
NO_REGRET = frozenset((
    "died", "dying", "dead", "death", "funeral", "passed", "buried", "hospital", "cancer",
    "diagnosis", "chemo", "miscarriage", "stillbirth",
))
REGRET_LINES = (
    "That's the thing about hindsight - it always turns up after. What would you do differently?",
    "Regret is worth listening to. If you could undo it, what would you do instead?",
    "That sounds like it has been sitting with you. What happened?",
    "A decision can turn out wrong without you being wrong to make it. What would you change?",
    "That is a fair thing to feel. What is the part you keep going back to?",
    "Easy to see it now. Would you do it differently next time?",
)
REGRET_LINES_PLAIN = (
    "Hindsight is always clearer than the decision was.",
    "That is a lot to carry without it being a mistake.",
    "Regret usually means the thing mattered to you.",
    "You can tell me the part that keeps coming back.",
)


FIRST_PERSON = re.compile(
    r"\b(?:i|im|ive|we|weve)\b"
    r"(?:\s+(?:really|so|only|just|still|already|now|also|kind\s+of|sort\s+of|do|did|dont|absolutely))*"
    r"\s+(?:regret|regrets|regretted|regretting|wish)\b")

PRACTICAL_ASK = re.compile(
    r"\b(?:can|could|should|shall|may)\s+(?:i|we)\s+\w+|"
    r"\bhow\s+do\s+(?:i|we)\s+\w+|\bhow\s+can\s+(?:i|we)\s+\w+|"
    r"\bwhere\s+do\s+(?:i|we)\s+\w+|\bwhat\s+do\s+(?:i|we)\s+do\b|"
    r"\bis\s+it\s+worth\b|\b(can|could)\s+(?:i|we)\s+(?:still\s+)?"
    r"(?:return|refund|exchange|cancel|sell|fix|claim|complain|change|get\s+(?:out|rid))\b")
POLITE = re.compile(
    r"\bregret\s+to\s+(?:say|tell|inform|report|announce|admit|hear|learn|let)\b"
    r"|\bregret\s+(?:that\s+)?(?:i|we)\s+(?:cant|can'?t|cannot|wont|won'?t|am\s+unable"
    r"|are\s+unable|am\s+not\s+able|must\s+miss)\b")

FUTURE_REGRET = re.compile(
    r"\b(?:going to|gonna|will|won'?t|wont|shall)\s+(?:\w+\s+){0,2}?regret\b"
    r"|\bregret\s+(?:this|it)\s+(?:tomorrow|in the morning|later|after)\b"
    r"|\byou(?:'?ll|ll|\s+will)\s+regret\b")

SHOULDNT_HAVE = re.compile(
    r"\bshould(?:n'?t|nt|\s+not)\s+have(?!\s+to\b)\s+"
    r"(?:\w+ed|said|told|bought|gone|done|left|taken|kept|booked|paid|sent|agreed|started|moved|"
    r"quit|sold|given|made|let|put|drunk|eaten|spent|worn|seen|heard|written|driven|known)\b"
    r"|\bshould\s+have\s+(?:said|told|bought|gone|done|kept|booked|paid|sent|left|taken|"
    r"stayed|waited|asked|listened|started|stopped|quit|held|walked|stood)\b")

PUT_DOWN = re.compile(
    r"\b(?:put|putting)\s+(?:\w+\s+){0,2}?(?:down|to\s+sleep)\b|\b(?:euthanis|euthaniz)\w*")


_OWN_SHOULD = re.compile(r"^\s*(?:[a-z]+,?\s+){0,2}(?:i|we)(?:'?ve|ve)?\s+should")
_HARM_AT_PERSON = re.compile(
    r"\b(?:shout(?:ed|ing)?|snapp(?:ed|ing)|yell(?:ed|ing)|swore|screamed|scream(?:ed|ing)|"
    r"lied|lash(?:ed)?\s+out|sulk(?:ed)?|was\s+(?:horrible|awful|mean|cruel|nasty))\s+"
    r"(?:at|to)\s+(?:my|his|her|our|your|the)\s+\w+")

WISH_I = re.compile(r"^\s*wish\s+(?:i|we)\b")


def reads_as_regret(clean, words=()):
    if not clean or "?" in clean:
        return False
    if re.match(r"(?:do|does|did|would|have|are|is|was|were|can|could)\s+(?:you|u)\b", clean):
        return False
    if set(words) & NO_REGRET or set(words) & NOT_PLAIN:
        return False
    if _has_phrase(clean, CRISIS) or _has_phrase(clean, COUNTERFACTUAL):
        return False
    if not (FIRST_PERSON.search(clean) or WISH_I.search(clean)
            or (_OWN_SHOULD.search(clean) and SHOULDNT_HAVE.search(clean))):
        return False
    if POLITE.search(clean):
        return False
    if PRACTICAL_ASK.search(clean):
        return False
    if FUTURE_REGRET.search(clean):
        return False
    if PUT_DOWN.search(clean):
        return False
    if _HARM_AT_PERSON.search(clean):
        return False
    if re.search(r"\b(?:no|dont|don't|never|not)\s+regrets?\b", clean):
        return False
    if re.search(r"\bregrets?\s+(?:nothing|none)\b", clean) or "regret a thing" in clean:
        return False
    return bool(REGRET.search(clean) or SHOULDNT_HAVE.search(clean))


def regret_reply_for(clean, words, memory, repaired=""):
    said = clean
    words = words or clean.split()
    if not reads_as_regret(clean, words):
        if not (repaired and repaired != clean and reads_as_regret(repaired,
                                                                  repaired.split())):
            return None
        said = repaired
        words = repaired.split()
    if set(words) & ASKS or _has_phrase(said, DOUBT):
        return None
    pool = REGRET_LINES_PLAIN if _asked_last(memory) else REGRET_LINES
    return pick(pool, memory, said)


THEIR_PERSON = (r"(?:mum|mom|mam|mother|dad|father|parents|sister|brother|son|daughter|kid|"
                r"kids|child|children|boy|girl|eldest|youngest|"
                r"baby|baby boy|baby girl|little one|little boy|little girl|little man|"
                r"little lad|little miss|oldest|firstborn|toddler|"
                r"gran|granny|nan|grandma|"
                r"grandmother|grandad|grandpa|grandfather|grandparents|nana|aunt|uncle|"
                r"cousin|partner|husband|wife|niece|nephew|grandson|granddaughter|"
                r"grandchildren|grandkids|grandsons|granddaughters|stepson|stepdaughter|"
                r"folks|inlaws|in-laws|friend|friends|mate|mates|best friend|best mate|"
                r"boss|colleague|workmate|neighbour|neighbor|neighbours|neighbors|"
                r"flatmate|housemate|roommate)")
THEIR_QUALIFIER = (r"(?:other|eldest|oldest|youngest|little|big|small|wee|first|second|third|"
                   r"middle|baby|grown up|grownup|step|adopted|foster) ")
THEIR_CHILD = (r"(?:son|daughter|kid|kids|child|children|boy|girl|eldest|youngest|niece|"
               r"baby|baby boy|baby girl|little one|little boy|little girl|little man|"
               r"little lad|little miss|oldest|firstborn|toddler|"
               r"nephew|grandson|granddaughter|grandkids|grandchildren|stepson|"
               r"stepdaughter|baby|babies|toddler|toddlers|newborn|newborns|infant|infants|"
               r"little one|little lad|little man|little fella|little fellow|little girl|"
               r"little boy|wee one|wee man|wee lad|small one)")
THEIR_NAME_AGE = re.compile(
    r"^my (?:" + THEIR_QUALIFIER + r")?(?P<person>" + THEIR_CHILD + r")(?:'?s)? (?:is called|is named|name is|name's|called|named) "
    r"(?P<name>[a-z][a-z'-]{1,14})(?: and |, )?(?:she|he|they|it)(?:'?s| is| are) "
    r"(?:just |only |nearly )?(?P<age>\d{1,2})$")
THEIR_NAME = re.compile(
    r"^my (?P<person>" + THEIR_PERSON + r")(?:'?s)? (?:is called|is named|name is|name's) "
    r"(?P<name>[a-z][a-z'-]{1,14})$")
AGE_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
             "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12}
THEIR_AGE = re.compile(
    r"^(?:my|our|the) (?:" + THEIR_QUALIFIER + r")?(?P<person>" + THEIR_CHILD + r")(?:'?s)? (?:is|are|is now|just turned|turns?) "
    r"(?:just |only |nearly |about )?(?P<n>\d{1,2}|" + "|".join(AGE_WORDS) + r")"
    r"(?:\s?(?:years?|yrs?\.?|y/o|yo|months?|mths?\.?|mth)(?:[ -]?old)?| old| now)?$")
BABY_WORDS = frozenset(("baby", "babies", "newborn", "newborns", "infant", "infants"))
YEAR_UNIT = re.compile(r"\b(?:years?|yrs?)\b|\d\s*(?:years?|yrs?|y/o|y\.o|yo|yr)\b")
THEIR_PLACE = re.compile(
    r"^my (?P<person>" + THEIR_PERSON + r")(?:'?s)? (?:live|lives|are living|is living|are based|"
    r"lives away) (?:in|near|up in|down in) (?P<place>[a-z][a-z '\-]{1,24}?)$")
THEIR_JOB = re.compile(
    r"^my (?P<person>" + THEIR_PERSON + r")(?:'?s)? (?:is|works as) (?:a |an )?"
    r"(?P<phrase>[a-z][a-z '\-]{2,28})$")
THEIR_JOB_LINES = (
    "{Job}. What does a normal day look like for {them}?",
    "{Job} \u2014 how long has {they} been at it?",
    "{Job}. Does {they} work nights, or is it days?",
    "{Job}. Is that what {they} always wanted to do?",
)
THEIR_ELDER = (r"(?:nan|nana|gran|granny|grandma|grandmother|grandad|granddad|grandpa|"
               r"grandfather|great gran|great nan|great grandma|great grandad|great aunt|"
               r"great uncle)")
THEIR_ELDER_AGE = re.compile(
    r"^my (?P<person>" + THEIR_ELDER + r")(?:'?s)? (?:is|is now|just turned|turns?) "
    r"(?:just |only |nearly |about )?(?P<n>\d{2,3})"
    r"(?: (?:years? old|year old|now))?$")
THEIR_ELDER_LINES = (
    "{n} \u2014 that is a good innings. Does {they} still live on {their} own?",
    "{n}. Do you get over to see {them} much?",
    "{n} \u2014 good going. What does {they} put it down to?",
)
NOT_A_NAME_AFTER_CALLED = frozenset("""one two three four five six seven eight nine ten
    eleven twelve once twice thrice again times in out round over back by up off through""".split())
THEIR_CALLED = re.compile(
    r"^my (?P<person>" + THEIR_PERSON + r")s? (?:is |are )?(?:called|named) "
    r"(?P<names>[a-z][a-z'\-]{1,14}(?: and [a-z][a-z'\-]{1,14})?)"
    r"(?: and (?:she|he|they)(?:'?s| is| are) (?:just |only |nearly )?(?P<age>\d{1,2}))?$")
THEIR_NAME_SO = re.compile(
    r"^my (?:" + THEIR_QUALIFIER + r")?(?P<person>" + THEIR_CHILD + r") (?P<name>[a-z][a-z'\-]{1,14}) "
    r"(?:is|is now|just turned|turns?) (?:just |only |nearly )?(?P<age>\d{1,2})$")
THEIR_LIKING = re.compile(
    r"^my (?P<person>" + THEIR_PERSON + r")(?:'?s)? "
    r"(?:really |absolutely |totally |just |properly |so )?"
    r"(?:loves?|adores?|likes?|enjoys?|collects?|is into|is really into|is mad about|"
    r"is big on|is obsessed with|is a fan of|is a big fan of|is addicted to) "
    r"(?P<thing>[a-z][a-z '\-]{1,30})$")
NOT_A_THING = frozenset((
    "it", "this", "that", "them", "these", "those", "me", "you", "us", "him", "her", "his",
    "hers", "mine", "yours", "life", "everything", "anything",
))
THE_THING_IS_A_CLAUSE = (" when ", " when", " if ", " if", " because", " but ", " that ",
                         " until ", " after ", " before ")

THEIR_DISLIKE = re.compile(
    r"^my (?P<person>" + THEIR_PERSON + r")(?:'?s)?(?: really | absolutely | actually )?"
    r" (?:doesnt|does not|don'?t|do not|didnt|did not|wont|will not|wouldnt|never|"
    r"can'?t|cannot|refuses to|refused to)"
    r" (?:like|eat|touch|drink|have|take|stand|finish|wear|try|watch|read|go to|get on with)"
    r" (?P<thing>[a-z][a-z '\-]{1,30})$")
THEIR_HATE = re.compile(
    r"^my (?P<person>" + THEIR_PERSON + r")(?:'?s)?(?: really | absolutely | actually )?"
    r" (?:hates?|loathes?|detests?|can'?t stand|cannot stand|is not keen on|"
    r"isn'?t keen on|is scared of|is frightened of)"
    r" (?P<thing>[a-z][a-z '\-]{1,30})$")
NOT_A_TASTE_AS_A_THING = frozenset("""
    baby boy brother child children cousin dad daughter father gran grandad grandma grandpa
    granny husband kid kids mam mom mother mum nan nana nephew niece partner sister son wife
    job school work boss teacher shift money house home bed bedtime bath mornings nights
    mondays tuesdays wednesdays thursdays fridays saturdays sundays
""".split())
TASTE_TOO_LONG = 4
THEIR_DISLIKE_LINES = (
    "{Thing} \u2014 noted. Good to know for {them}.",
    "Fair enough \u2014 {thing} is not for {them}.",
    "{Thing} \u2014 noted, and {they} can steer round it.",
)
THEIR_HATE_LINES = (
    "{Thing} \u2014 fair enough, and {they} can steer round it.",
    "Hating {thing} is allowed, and {they} {are} in good company.",
    "{Thing} \u2014 noted, with sympathy for {them}.",
)


def _a_taste_they_refuse(clean, memory):
    if not isinstance(clean, str) or "?" in clean:
        return None
    for pattern, pool in ((THEIR_DISLIKE, THEIR_DISLIKE_LINES), (THEIR_HATE, THEIR_HATE_LINES)):
        match = pattern.match(clean)
        if not match:
            continue
        thing = " ".join(match.group("thing").lower().split())
        bare = re.sub(r"^(?:the|a|an|his|her|their|its) ", "", thing)
        if any(hang in " " + thing + " " for hang in THE_THING_IS_A_CLAUSE):
            continue
        if not bare or len(bare.split()) > TASTE_TOO_LONG:
            continue
        if bare in NOT_A_THING or set(bare.split()) & NOT_A_TASTE_AS_A_THING:
            continue
        if bare.split()[0] in AGE_WORDS or bare.isdigit():
            continue
        thing = re.sub(r"\b(?:my|our)\b", "your", thing)
        person = match.group("person").strip()
        return _pick_filled(pool, memory, clean,
                            lambda line, thing=thing, person=person: fill_person(
                                line.replace("{Thing}", thing[:1].upper() + thing[1:])
                                    .replace("{thing}", thing), person))
    return None


SHE_PEOPLE = frozenset((
    "mum", "mom", "mam", "mother", "sister", "daughter", "wife", "niece", "gran", "granny",
    "nan", "nana", "grandma", "grandmother", "granddaughter", "aunt", "stepdaughter", "girl",
    "little girl",
))
HE_PEOPLE = frozenset((
    "dad", "father", "brother", "son", "husband", "nephew", "grandad", "grandpa", "grandfather",
    "grandson", "uncle", "stepson", "boy", "little boy", "little lad", "little man",
    "little fella", "little fellow", "wee man", "wee lad",
))
THEY_PERSON = ("they", "them", "their", "do", "are")
SHE_PERSON = ("she", "her", "her", "does", "is")
HE_PERSON = ("he", "him", "his", "does", "is")


def person_pronouns(person_word):
    word = str(person_word or "").strip().lower()
    if word in SHE_PEOPLE:
        return SHE_PERSON
    if word in HE_PEOPLE:
        return HE_PERSON
    return THEY_PERSON


def fill_person(line, person_word):
    they, them, their, do, are = person_pronouns(person_word)
    filled = (line.replace("{they}", they).replace("{them}", them).replace("{their}", their)
                  .replace("{do}", do).replace("{are}", are)
                  .replace("{They}", they.capitalize()).replace("{Them}", them.capitalize())
                  .replace("{Their}", their.capitalize()).replace("{Do}", do.capitalize())
                  .replace("{Are}", are.capitalize()))
    return filled


THEIR_MOOD_WITH_YOU = re.compile(
    r"\b(?:(?:my|our)\s+(?:\w+\s+){0,2}?)?(?:mum|mom|mam|mother|dad|father|husband|wife|partner|"
    r"boyfriend|girlfriend|sister|brother|son|daughter|friend|mate|boss|manager|colleague|"
    r"flatmate|housemate|neighbour|neighbor|nan|nana|gran|granny|grandma|grandad|grandpa|aunt|"
    r"uncle|cousin|he|she|they)\s+(?:was|were|is|are|has been|had been|'s been|been)\s+"
    r"(?:being\s+)?(?:funny|off|short|sharp|snappy|offhand|cold|cool|distant|offish|surly|cross|"
    r"irritable|grumpy|moody|brusque|abrupt|weird|odd|strange)\s+with\s+(?:me|us)\b"
    r"|\b(?:he|she|they|my\s+\w+)\s+snapped\s+at\s+me\b"
    r"|\b(?:he|she|they|my\s+\w+)\s+blanked\s+me\b"
    r"|\bgave\s+me\s+the\s+cold\s+shoulder\b", re.I)
THEIR_MOOD_WITH_YOU_LINES = (
    "Being funny with you and not saying why is unsettling. Do you know what set {them} off?",
    "That is an odd way to be with you. Is it a one-off, or has it been like this a while?",
    "You are left guessing when {they} {do} that. Did {they} say anything at all?",
    "Being got at without knowing why wears you down. What happened just before it?",
)


GOING_ON = re.compile(
    r"^(?:(?:it|that|this)s?\s+)?(?:all|most|every)\s+(?:the\s+)?"
    r"(?:time|weeks?|weekends?|days?|nights?)\b"
    r"|\bits\s+been\s+(?:going\s+on|like\s+that|happening)\s+(?:for|since|all|most|every)\b"
    r"|\b(?:it|that|this|she|he|they)s?\s+(?:been|has\s+been|'s\s+been)\s+like\s+(?:that|this)\s+"
    r"(?:all|for|since)\b"
    r"|(?:it|that|this|she|he|they)\s+(?:happens|happened|does\s+(?:it|that)|is\s+like\s+that|"
    r"has\s+been\s+like\s+(?:that|this)|keeps?\s+happening|goes?\s+on)[^.!?]{0,26}?"
    r"\b(?:most|every|all)\s+(?:single\s+|other\s+)?(?:weeks?|weekends?|days?|nights?|mornings?|time|the\s+time)\b"
    r"|\b(?:she|he|they|it)\s+(?:has\s+been|had\s+been|'s\s+been|was|is)\s+like\s+(?:that|this)\s+"
    r"(?:all|for|since)\b"
    r"|\b(?:it|this|that)\s+(?:has\s+been|had\s+been|'s\s+been)\s+going\s+on\s+(?:for|since)\b"
    r"|\b(?:it|this|that)\s+(?:has\s+been|had\s+been|'s\s+been)\s+for\s+"
    r"(?:about\s+)?(?:\d+|a|an|two|three|four|five|six|seven|eight|nine|ten|a\s+few|"
    r"a\s+couple\s+of|several)\s+(?:weeks?|months?|years?|days?)\b"
    r"|\b(?:for|since)\s+(?:about\s+)?(?:\d+|a|an|two|three|four|five|six|seven|eight|nine|ten|"
    r"a\s+few|a\s+couple\s+of|several)\s+(?:weeks?|months?|years?|days?)\b"
    r"|\bsince\s+(?:january|february|march|april|may|june|july|august|september|october|"
    r"november|december|christmas|last\s+(?:week|month|year|summer|autumn|winter|spring))\b",
    re.I)
GOING_ON_LINES = (
    "That long is a lot of guessing. Have you asked {them} straight out?",
    "Being off with you for that long stops being a mood and starts being a habit. Have you said "
    "anything to {them}?",
    "If it has been going on that long, it is worth saying to {them}, not sitting on. "
    "What would you want to say?",
)


def their_mood_going_on_reply_for(clean, memory):
    if not clean or "?" in clean:
        return None
    kept = (memory or {}).get("mood_with_you")
    if not isinstance(kept, dict):
        return None
    turns = (memory or {}).get("turns") or []
    if not 0 <= len(turns) - int(kept.get("at") or 0) <= 2:
        return None
    if not GOING_ON.search(clean):
        return None
    if _has_phrase(clean, CRISIS):
        return None
    person = _pronoun_person(kept.get("person") or "")
    return _pick_filled(GOING_ON_LINES, memory, clean,
                        lambda line: fill_person(line, person))


def _pronoun_person(person):
    return {"he": "husband", "she": "wife", "they": ""}.get(person, person)


def their_mood_with_you_reply_for(clean, words, memory):
    if not clean or "?" in clean:
        return None
    match = THEIR_MOOD_WITH_YOU.search(clean)
    if not match:
        return None
    said = " ".join(clean.split())
    if _has_phrase(said, CRISIS) or _has_phrase(said, NOT_PLAIN):
        return None
    person = ""
    for word in ("mum", "mom", "mam", "mother", "dad", "father", "husband", "wife", "partner",
                 "boyfriend", "girlfriend", "sister", "brother", "son", "daughter", "friend",
                 "mate", "boss", "manager", "colleague", "flatmate", "housemate", "neighbour",
                 "neighbor", "nan", "nana", "gran", "granny", "grandma", "grandad", "grandpa",
                 "aunt", "uncle", "cousin", "he", "she", "they"):
        if re.search(r"\b" + word + r"\b", said):
            person = word
            break
    person = _pronoun_person(person)
    if isinstance(memory, dict):
        memory["mood_with_you"] = {"person": person, "at": len(memory.get("turns") or [])}
    return _pick_filled(THEIR_MOOD_WITH_YOU_LINES, memory, clean,
                        lambda line: fill_person(line, person))


THEIR_NAME_LINES = (
    "{name} — that is a good one. Where did it come from?",
    "{name}. Do you call {them} {name} all the time, or does it get shortened?",
    "{name}. Who picked it?",
)
THEIR_NAME_GROWN_LINES = (
    "{name} — that's a lovely name. Is it a family one?",
    "{name}. {Do} {they} get called anything for short?",
    "{name} — nice. Is there a story behind it?",
)
A_CHILD_NAMED = frozenset(THEIR_CHILD.strip("(?:)").split("|"))
THEIR_NAME_AGE_LINES = (
    "{name} at {n} — that is a good age. What {are} {they} into at the moment?",
    "{name}, {n}. What {are} {they} like just now?",
)
THEIR_NAMES_LINES = (
    "{names} — two good names. How old are they?",
    "{names}. What are they like, the pair of them?",
    "{names} — a houseful, then. How old are they?",
)
THEIR_BABY_LINES = (
    "{m} — are you getting any sleep?",
    "{m} old. Is it the nights that are hardest, or the days?",
    "{m} — that is the age everything goes in the mouth. Is that where you are?",
)
THEIR_SMALL_LINES = (
    "{n} is a busy age. What {are} {they} into at the moment?",
    "{n} — that is the age of asking why about everything. Does that sound right?",
    "{y}. Is it easier than the baby stage, or harder?",
)
THEIR_CHILD_LINES = (
    "{n} is a good age. What {are} {they} into at the moment?",
    "{y}. Is school going all right for {them}?",
    "{n} — what are the days like with {them} just now?",
)
THEIR_TEEN_LINES = (
    "{n} — is that a good age or a hard one?",
    "{y}. What {are} {they} like just now?",
    "{n} — do you get much of a look in these days?",
    "{n} — {do} {they} still want you around, or are you embarrassing now?",
)
THEIR_GROWN_LINES = (
    "{n} — grown, then. Still at home?",
    "{n} is a proper landmark. What {are} {they} doing now?",
    "{y}. {Do} {they} still let you fuss over {them}?",
)
THEIR_PLACE_LINES = (
    "{place}. How often do you get to see {them}?",
    "{place} — {do} {they} ever come to you instead?",
    "{place}. Do you get up there much, or is it {them} coming to you?",
)
THEIR_LIKING_LINES = (
    "{thing}. What got {them} into it?",
    "{thing} \u2014 good one. Is it a long-standing thing with {them}?",
    "{thing}. Do you get roped into it with {them} at all?",
)


PLACE_CODES = {"us": "US", "usa": "USA", "uk": "UK", "uae": "UAE", "eu": "EU", "nz": "NZ",
               "nyc": "NYC", "drc": "DRC"}


def name_a_place(said):
    place = " ".join(said.split())
    lead = ""
    if place.lower().startswith("the ") and len(place) > 4:
        lead, place = "The ", place[4:]
    return lead + " ".join(PLACE_CODES.get(word.lower(), word.title()) for word in place.split())


def fill_age(line, n, months=False):
    years = f"{n} year{'s' if n != 1 else ''} old"
    count = f"{n} month{'s' if n != 1 else ''}" if months else years
    return line.replace("{y}", years).replace("{m}", count).replace("{n}", str(n))


def _age_pool(n, months=False):
    if months and n <= 30:
        return THEIR_BABY_LINES
    if n < 5:
        return THEIR_SMALL_LINES
    if n < 13:
        return THEIR_CHILD_LINES
    if n < 18:
        return THEIR_TEEN_LINES
    return THEIR_GROWN_LINES


def _the_job_in(phrase):
    words = [w for w in re.split(r"[\s'-]+", str(phrase or "").strip()) if w]
    if not words or len(words) > 2:
        return None
    if not set(words) & facts.JOB_WORDS:
        return None
    return " ".join(words).title()


def _pick_filled(lines, memory, clean, fill):
    return pick([fill(line) for line in lines], memory, clean)


A_HELD_NAME_AND_AN_AGE = re.compile(
    r"^(?P<name>[a-z][a-z'\-]{1,19}) (?:is|is now|will be|turns|just turned) "
    r"(?:just |only |nearly |about )?(?P<n>\d{1,2}|" + "|".join(AGE_WORDS) + r")"
    r"(?:\s?(?:years?|yrs?\.?|y/o|yo|months?|mths?\.?|mth)(?:[ -]?old)?| old| now)?$")
A_MILESTONE_TAIL = re.compile(r"\b(?:next|on|this|in)\s+(?:week|month|year|monday|tuesday|wednesday|"
                              r"thursday|friday|saturday|sunday|january|february|march|april|"
                              r"may|june|july|august|september|october|november|december)\b")
AGE_PUT_RIGHT = (
    "{name} at {n} now — I had {old}.",
    "{name}'s {n}, then, not {old} — got it.",
    "{name} at {n}. I had {old}, so that is the one thing I will change.",
)
AGE_FIRST_TOLD = (
    "{name} at {n}, then.",
    "{name}, {n} — good to know.",
    "{name} at {n}. That is one to remember.",
)
AGE_ALREADY_HAD = (
    "{name} at {n} — that is what I had.",
    "{name}, {n}. I had that already, so nothing changes.",
)


def _the_people_in(memory, name):
    held = memory if isinstance(memory, dict) else {}
    found = []
    for entry in held.get("others") or []:
        if isinstance(entry, dict) and str(entry.get("name") or "").strip().lower() == name:
            found.append(entry)
    theirs = held.get("user") if isinstance(held.get("user"), dict) else {}
    for entry in theirs.get("pets") or []:
        if isinstance(entry, dict) and str(entry.get("name") or "").strip().lower() == name:
            found.append(entry)
    return found


def _the_age_i_had(name, memory):
    held = memory if isinstance(memory, dict) else {}
    old = None
    for fact in held.get("facts_log") or []:
        value = fact.get("value") if isinstance(fact, dict) else None
        if not isinstance(value, dict):
            continue
        if str(value.get("name") or "").strip().lower() != name:
            continue
        if isinstance(value.get("age"), int) and value["age"]:
            old = value["age"]
    return old


def _an_age_put_right(clean, memory):
    if A_MILESTONE_TAIL.search(clean or ""):
        return None
    match = A_HELD_NAME_AND_AN_AGE.match(clean or "")
    if not match:
        return None
    name = match.group("name")
    found = _the_people_in(memory, name)
    if not found:
        return None
    said = match.group("n")
    n = int(said) if said.isdigit() else AGE_WORDS[said]
    if not n or n > 120:
        return None
    spelled = str(found[0].get("name") or name).strip().title()
    old = _the_age_i_had(name, memory)
    if not isinstance(old, int) or not old:
        return pick(AGE_FIRST_TOLD, memory, clean).format(name=spelled, n=n)
    if old == n:
        return pick(AGE_ALREADY_HAD, memory, clean).format(name=spelled, n=n)
    return pick(AGE_PUT_RIGHT, memory, clean).format(name=spelled, n=n, old=old)


def their_people_reply_for(clean, words, memory):
    if not clean or "?" in clean:
        return None
    clean = without_leaders(clean) or clean
    if set(words) & NOT_PLAIN or _has_phrase(clean, CRISIS):
        return None
    refused = _a_taste_they_refuse(clean, memory)
    if refused:
        return refused

    put_right = _an_age_put_right(clean, memory)
    if put_right:
        return put_right
    match = THEIR_ELDER_AGE.match(clean)
    if match:
        said = match.group("n")
        n = int(said) if said.isdigit() else AGE_WORDS[said]
        return _pick_filled(THEIR_ELDER_LINES, memory, clean,
                            lambda line: fill_person(fill_age(line, n), match.group("person")))
    match = THEIR_JOB.match(clean)
    if match:
        job = _the_job_in(match.group("phrase"))
        if job:
            return _pick_filled(THEIR_JOB_LINES, memory, clean,
                                lambda line: fill_person(line.replace("{Job}", job),
                                                         match.group("person")))
    match = THEIR_PLACE.match(clean)
    if match:
        place = name_a_place(match.group("place"))
        return _pick_filled(THEIR_PLACE_LINES, memory, clean,
                            lambda line: fill_person(line.replace("{place}", place),
                                                     match.group("person")))
    match = THEIR_NAME_AGE.match(clean)
    if match:
        name = match.group("name").strip().title()
        n = str(int(match.group("age")))
        return _pick_filled(THEIR_NAME_AGE_LINES, memory, clean,
                            lambda line: fill_person(line.replace("{name}", name)
                                                         .replace("{n}", n),
                                                     match.group("person")))
    match = THEIR_AGE.match(clean)
    if match:
        months = bool(re.search(r"months?|mths?|\bmth\b", match.group(0)))
        said = match.group("n")
        n = int(said) if said.isdigit() else AGE_WORDS[said]
        if (not months and said.isdigit() and match.group("person") in BABY_WORDS
                and not YEAR_UNIT.search(match.group(0))):
            if n > 24:
                return None
            months = True
        return _pick_filled(_age_pool(n, months), memory, clean,
                            lambda line: fill_person(fill_age(line, n, months),
                                                     match.group("person")))
    match = THEIR_NAME.match(clean)
    if match:
        name = match.group("name").strip().title()
        person = (match.group("person") or "").strip().lower()
        pool = THEIR_NAME_LINES if person in A_CHILD_NAMED else THEIR_NAME_GROWN_LINES
        return _pick_filled(pool, memory, clean,
                            lambda line: fill_person(line.replace("{name}", name),
                                                     match.group("person")))
        line = pick(THEIR_NAME_LINES, memory, clean).replace("{name}", name)
        return fill_person(line, match.group("person"))
    match = THEIR_NAME_SO.match(clean)
    if match:
        name = match.group("name").strip()
        if facts.a_name_could_be(name.lower()):
            line = pick(THEIR_NAME_AGE_LINES, memory, clean)
            line = (line.replace("{name}", name.title())
                        .replace("{n}", str(int(match.group("age")))))
            return fill_person(line, match.group("person"))
    match = THEIR_CALLED.match(clean)
    if match:
        names = [word.strip() for word in match.group("names").split(" and ")]
        if all(facts.a_name_could_be(word.lower())
               and word.lower() not in NOT_A_NAME_AFTER_CALLED
               and not word.isdigit() for word in names):
            said = " and ".join(word.title() for word in names)
            if len(names) == 2:
                return pick(THEIR_NAMES_LINES, memory, clean).replace("{names}", said)
            if match.group("age"):
                line = pick(THEIR_NAME_AGE_LINES, memory, clean)
                return (fill_person(line, match.group("person"))
                        .replace("{name}", said)
                        .replace("{n}", str(int(match.group("age")))))
            line = pick(THEIR_NAME_LINES, memory, clean).replace("{name}", said)
            return fill_person(line, match.group("person"))
    match = THEIR_LIKING.match(clean)
    if match:
        thing = match.group("thing").strip()
        if thing.split()[0] in NOT_A_THING:
            return None
        if any(word in f" {thing} " for word in THE_THING_IS_A_CLAUSE):
            return None
        said = thing[:1].upper() + thing[1:]
        return _pick_filled(THEIR_LIKING_LINES, memory, clean,
                            lambda line: fill_person(line.replace("{thing}", said),
                                                     match.group("person")))
    return None



OWN_HAVE = re.compile(
    r"^(?:i|we)(?:'ve|ve)\s+got\s+(?P<one>.+)$"
    r"|^(?:i|we)\s+(?:have|has)\s+(?:got\s+)?(?P<two>[^?]+)$")
OWN_SPACES = frozenset("""
room bedroom kitchen garage greenhouse shed garden allotment plot patch balcony patio loft cellar
basement workshop study conservatory hut outbuilding yard driveway orchard pond
""".split())
OWN_KIT = frozenset("""
piano guitar keyboard drums telescope bike bikes motorbike car caravan boat canoe kayak
netflix projector printer turntable bench washing machine dishwasher
""".split())
OWN_KIT_NAMES = frozenset(("drum kit", "record player", "sewing machine", "hot tub",
                           "log burner", "solar panels", "summer house"))
OWN_FACTS = {
    "room": "{A} {thing} earns its keep as a bed, a desk or storage, and it is cheapest left "
            "as two of those",
    "bedroom": "a spare bedroom earns its keep as a bed, a desk or storage",
    "kitchen": "{A} {thing} earns its space back: a good surface and one heavy pan do more than "
               "a cupboard of gadgets",
    "garage": "{A} {thing} is a store that can also take a car, and most of them end up too full "
              "for one",
    "greenhouse": "{A} {thing} buys weeks at both ends of the season - tomatoes ripen in it and "
                  "seedlings stop going leggy on a windowsill",
    "shed": "{A} {thing} is where the tools stop rusting and the mower stops being in the way",
    "garden": "{A} {thing} is the cheapest ground you will ever get for potatoes, beans and "
              "salad",
    "allotment": "{A} {thing} is hard work the first year while the ground is cleared, and much "
                 "less after that",
    "plot": "{A} {thing} is hard work the first year while the ground is cleared, and much less "
            "after",
    "patch": "{A} {thing} that size grows salad, herbs and a few beans, which is most of what "
             "people actually eat",
    "balcony": "{A} {thing} grows more than people expect: tomatoes, herbs and salad all do well "
               "in pots out there",
    "patio": "{A} {thing} earns its keep in pots - tomatoes and herbs do better against a warm "
             "wall",
    "loft": "{A} {thing} is the cheapest storage a house has, as long as the damp stays out of it",
    "cellar": "{A} {thing} keeps a steady cool temperature, which is what potatoes, squash and "
              "wine want",
    "basement": "{A} {thing} keeps a steady cool temperature, which is what potatoes and squash "
                "want",
    "workshop": "{A} {thing} is worth having for the bench more than the tools",
    "study": "{A} {thing} is mostly a door that shuts: a desk and a quiet hour do the rest",
    "conservatory": "{A} {thing} gets hot in summer and cold in winter, so it works best with "
                    "plants in it and a chair",
    "piano": "{A} {thing} is the easiest instrument to start from nothing on, and an acoustic one "
             "wants tuning about once a year",
    "guitar": "{A} {thing} is the one you can pick up for ten minutes and put down again, which "
              "is how people actually learn",
    "keyboard": "{A} {thing} is the quiet way to practise - headphones and nobody in the house "
                "hears it",
    "drums": "drums are the loudest hobby a house can hold, so an electric kit and headphones "
             "keep the neighbours onside",
    "drum kit": "drums are the loudest hobby a house can hold, so an electric kit and headphones "
                "keep the neighbours onside",
    "bike": "{A} {thing} beats the car for anything under a couple of miles once parking is "
            "counted",
    "bikes": "bikes beat the car for short trips once parking is counted, and two of them fit "
             "where one car will not",
    "motorbike": "{A} {thing} is the cheap way through traffic and the expensive way to stay warm "
                 "and dry",
    "caravan": "{A} {thing} saves the hotel bill and costs you the towing, which is why most of "
               "them sit for months at a time",
    "boat": "{A} {thing} is a hobby in itself - the upkeep is the part nobody warns you about",
    "canoe": "a canoe gets you on water a boat cannot reach, and it goes on the roof of a car",
    "kayak": "a kayak gets you on water a boat cannot reach, and it goes on the roof of a car",
    "netflix": "the good part of netflix is that a film night costs nothing past the "
               "subscription, and you can stop halfway and finish it tomorrow",
    "projector": "{A} {thing} turns a blank wall into a big screen, and it wants the room "
                 "properly dark",
    "sewing machine": "{A} {thing} pays for itself on repairs - a hem or a zip costs more to have "
                      "done than the machine did",
    "printer": "{A} {thing} earns its space on the parts nobody sells any more, not on ornaments",
    "record player": "records are the format that makes you listen to a whole side",
    "turntable": "records are the format that makes you listen to a whole side",
    "pond": "{A} {thing} brings frogs and birds in and then more or less runs itself once the "
            "plants are in",
    "bench": "{A} {thing} is where a hobby gets done properly, and one good vice is worth more "
             "than the rest of it",
    "car": "{A} {thing} costs more to keep than people plan for, and the short trips are what "
           "wear it hardest",
    "washing machine": "{A} {thing} is worth mending once before it is replaced - the pump and "
                       "the door seal are the two that go, and both are cheap parts",
    "dishwasher": "{A} {thing} uses less water than washing up by hand, and the salt is the part "
                  "people forget",
    "hot tub": "{A} {thing} costs more to run than to buy - the heater and the chemicals are the "
               "bill nobody plans for",
    "log burner": "{A} {thing} heats the one room it is in well, and it wants dry wood or the "
                  "chimney soots up",
    "solar panels": "solar panels pay back over something like ten years on a roof that "
                    "faces the sun, and much less on one that does not",
    "summer house": "{A} {thing} is a room the garden gets three months out of, so treat it like a "
                    "shed and keep the damp out",
}
OWN_SPACES_PLAIN = ("{A} {thing} takes the mess and the work out of the middle of the house, "
                    "which is what makes it worth having")
OWN_KIT_PLAIN = "{A} {thing} is worth owning rather than borrowing, which is the point of it"
OWN_ELECTRIC = re.compile(r"\b(?:electric|electrical|ev|hybrid)\b")
OWN_ELECTRIC_CAR = ("{A} {thing} is cheapest on the short trips that wear a petrol one out, and "
                    "the cold and a motorway run are what use the charge up fastest")
OWN_ASKS = (
    "What do you use it for?",
    "What have you done with it so far?",
    "Is it doing the job you wanted?",
    "What would you change about it?",
)
OWN_KIT_ASKS = (
    "Does it get much use?",
    "How long have you had it?",
    "Is it what you hoped for?",
    "Has it been worth what it cost?",
)
OWN_NOT_THE_THING = re.compile(
    r"\b(?:problem|idea|lot|few|bit|chance|job|question|go|look|word|feeling|guess|break|"
    r"rest|while|minute|moment|day|week|month|year|time|filo|hint|tip|note|deal|point|reason|"
    r"choice|decision|say|think|try|best|crack|go)\b")
OWN_TWO_THINGS = re.compile(
    r"\b(?:and|or|plus|also|with)\b|&|/|,|"
    r"\b(?:but|no|not|never|without|except|apart from|instead of|rather than)\b")
OWN_FAULT = re.compile(
    r"\b(?:leak\w*|broken|broke\w*|cracked|cracks|blocked|faulty|fault|stopped working|"
    r"not working|dead|damp|mould|mold|smell\w*|flood\w*|noisy|rattl\w*|jammed|stuck|"
    r"cold|flu|bug|temperature|cough|sore|ache|pain|migraine|rash|infection|sick)\b")
OWN_TIME = re.compile(
    r"\b(?:today|tonight|tomorrow|morning|afternoon|evening|night|weekend|monday|tuesday|"
    r"wednesday|thursday|friday|saturday|sunday|week|month|year|o'clock)\b")
OWN_ARTICLE = ("a ", "an ", "the ", "one ", "two ", "three ", "four ", "some ", "another ")
OWN_TAIL = re.compile(
    r"\s+(?:by the .*|at the .*|in the .*|out the .*|out back|in back|upstairs|downstairs|"
    r"out front|round the .*|down the .*)$")


def _the_thing_they_have(clean):
    said = " ".join(str(clean or "").lower().strip().rstrip(".!,").split())
    if not said or "?" in said:
        return None
    match = OWN_HAVE.match(said)
    if not match:
        return None
    thing = (match.group("one") or match.group("two") or "").strip()
    for article in OWN_ARTICLE:
        if thing.startswith(article):
            thing = thing[len(article):]
            break
    thing = OWN_TAIL.sub("", thing).strip()
    words = thing.split()
    if not words or len(words) > 4:
        return None
    if OWN_NOT_THE_THING.search(thing) or OWN_FAULT.search(thing) or OWN_TIME.search(thing):
        return None
    if OWN_TWO_THINGS.search(thing):
        return None
    key = _the_class_word(thing)
    if not key:
        return None
    return thing, ("space" if key in OWN_SPACES else "kit")


def _the_class_word(thing):
    words = str(thing or "").split()
    for size in (3, 2, 1):
        if len(words) >= size:
            tail = " ".join(words[-size:])
            if (tail in OWN_SPACES or tail in OWN_KIT or tail in OWN_KIT_NAMES
                    or tail in OWN_FACTS):
                return tail
    return ""


def _article(thing):
    word = str(thing or "").strip().lower()
    if not word:
        return "A"
    if word[0] in "aeiou" and not word.startswith(("one", "uni", "use", "euro")):
        return "An"
    return "A"


def _the_fact_about(thing, kind):
    article = _article(thing)
    key = _the_class_word(thing) or ""
    fact = OWN_FACTS.get(key)
    if key == "car" and OWN_ELECTRIC.search(thing):
        fact = OWN_ELECTRIC_CAR
    if not fact:
        fact = OWN_SPACES_PLAIN if kind == "space" else OWN_KIT_PLAIN
    fact = fact.replace("{A}", article).replace("{thing}", thing)
    return fact


def _capped(line):
    return line[0].upper() + line[1:] if line else line


def a_thing_of_theirs_reply_for(clean, words, memory):
    if not clean or "?" in clean:
        return None
    if set(words) & NOT_PLAIN or _has_phrase(clean, CRISIS):
        return None
    found = _the_thing_they_have(clean)
    if not found:
        return None
    thing, kind = found
    fact = _capped(_the_fact_about(thing, kind))
    asks = OWN_ASKS if kind == "space" else OWN_KIT_ASKS
    return _pick_filled([f"{fact}. {ask}" for ask in asks], memory, clean, lambda line: line)

_RELATION_PERSON = (r"(?:mum|mom|mam|mother|dad|father|son|daughter|child|kid|partner|husband|"
                    r"wife|boyfriend|girlfriend|fiance|fiancee|ex|sister|brother|best friend|"
                    r"bestie|friend|flatmate|housemate|mother in law|father in law|in laws)")
MARRIAGE_IN_TROUBLE = re.compile(
    r"\b(?:my|our)\s+(?:marriage|relationship)\s+(?:is|has|feels)\s+(?:on the rocks|rocky|"
    r"in trouble|in a bad way|falling apart|a mess|not in a good place|over|dead)\b")
BAD_WITH_THEM = re.compile(
    r"\bthings (?:are|have been|arent|are not|aint)\s+(?:bad|rough|hard|rubbish|terrible|awful|"
    r"not good|not great|not the same)\s+(?:with|between)\s+(?:my|our)\s+(%s)\b" % _RELATION_PERSON)
QUIET_BETWEEN_THEM = re.compile(
    r"\b(?:me and|i and|myself and)\s+(?:my|our)\s+(%s)\s+(?:barely|hardly|never)\s+"
    r"(?:talk|speak)\b"
    r"|\b(?:my|our)\s+(%s)\s+and\s+i\s+(?:barely|hardly|never|dont|don't|do not)\s+"
    r"(?:talk|speak|get on)\b"
    r"|\bwe\s+(?:barely|hardly|never)\s+(?:talk|speak)\b"
    r"|\b(?:my|our)\s+(%s)\s+(?:is|has been|seems|feels|sounds)\s+(?:distant|cold|withdrawn|"
    r"off with me|cold with me|distant with me)\b"
    % (_RELATION_PERSON, _RELATION_PERSON, _RELATION_PERSON))
ROWS_BETWEEN_THEM = re.compile(
    r"\b(?:me and|i and)\s+(?:my|our)\s+(%s)\s+(?:keep\s+)?(?:argue|arguing|row|rowing|fight|"
    r"fighting|bicker|bickering)\b"
    r"|\b(?:my|our)\s+(%s)\s+and\s+i\s+(?:keep\s+)?(?:argue|arguing|row|rowing|fight|"
    r"fighting|bicker|bickering)\b"
    r"|\bwe\s+(?:keep\s+)?(?:argue|arguing|row|rowing)\b"
    % (_RELATION_PERSON, _RELATION_PERSON))
RELATION_GONE_WRONG = re.compile(
    r"\b(?:my|our)\s+(%s)\s+and\s+i\s+(?:dont|don't|do not)\s+get on\b"
    r"|\b(?:dont|don't|do not)\s+get on with\s+(?:my|our)\s+(%s)\b"
    r"|\bwe (?:are|keep|have been)\s+(?:growing|drifting) apart\b"
    % (_RELATION_PERSON, _RELATION_PERSON))
NOT_A_RELATION_TROUBLE = re.compile(
    r"\b(?:hurt|hurts|hurting|injur\w*|hospital|ambulance|a and e|stroke|seizure|fit|fits|"
    r"collapsed|collapse|bleeding|blood|overdose|cancer|tumour|tumor|dementia|alzheimer\w*|"
    r"chemo\w*|died|dying|death|funeral|drink|drinks|drinking|alcohol|drunk|hit|hits|hitting|"
    r"punch\w*|knife|gun|police|threat\w*|abuse\w*|affair|cheat\w*|divorce|cheated)\b")
THE_QUIET_LINES = (
    "That is a lonely way to live. When did {pair} last have a proper talk?",
    "Sorry to hear it. What is an evening at home like for {pair} now?",
    "That is hard going. What happened the last time {pair} tried to talk?",
)
THE_ROWS_LINES = (
    "That wears a person down. What do the rows tend to be about?",
    "That is exhausting. Is there one thing that sets it off with {who}?",
    "Nothing I can fix from here, but I can listen. What was the last row about?",
)
THE_RELATION_LINES = (
    "That is a hard place to be. What has changed with {who}?",
    "Sorry to hear it. What has gone wrong with {who} lately?",
    "That is a heavy thing to carry. What does a bad week look like for {pair}?",
)


def the_two_of_them(clean, memory=None):
    if not clean or "?" in clean:
        return None
    if NOT_A_RELATION_TROUBLE.search(clean):
        return None
    pool = None
    if QUIET_BETWEEN_THEM.search(clean):
        pool = THE_QUIET_LINES
    elif ROWS_BETWEEN_THEM.search(clean):
        pool = THE_ROWS_LINES
    elif MARRIAGE_IN_TROUBLE.search(clean) or BAD_WITH_THEM.search(clean) \
            or RELATION_GONE_WRONG.search(clean):
        pool = THE_RELATION_LINES
    if not pool:
        return None
    found = re.search(r"\b(?:my|our)\s+(%s)\b" % _RELATION_PERSON, clean)
    who = "your " + found.group(1) if found else "the two of you"
    pair = "you and your " + found.group(1) if found else "the two of you"
    return _pick_filled(pool, memory, clean,
                        lambda line: line.replace("{who}", who).replace("{pair}", pair))



def _has_phrase(clean, phrases):
    return any(f" {phrase} " in f" {clean} " for phrase in phrases)


def _planned_word(word):
    if word in PLANNED_VERBS:
        return True
    for verb in PLANNED_VERBS:
        if word in (verb + "ing", verb[:-1] + "ing", verb + "s", verb + "d",
                    verb + verb[-1] + "ing", verb[:-1] + "ed"):
            return True
    return False


THOUGHT_OBJECT = frozenset((
    "it", "this", "that", "them", "they", "everything", "anything", "nothing", "myself",
    "me", "him", "her", "past", "life", "death", "everything", "people", "someone",
    "somebody", "anyone", "anybody", "childhood", "then", "before",
)) | OTHER_PEOPLE


def _going_to_plan(clean):
    for opener in GOING_TO:
        at = clean.find(opener)
        if at < 0:
            continue
        rest = clean[at + len(opener):].split()
        if len(rest) > 1 and rest[0] in ("work", "working", "works"):
            return rest[1] == "on"
        if rest and _planned_word(rest[0]):
            return True
        if len(rest) > 1 and rest[0] in ("going", "getting") and rest[1] == "back":
            return True
        if opener.strip() in ("thinking of", "thinking about") and not set(rest[:3]) & THOUGHT_OBJECT:
            return True
    return False


def reads_as_plan(clean):
    if set(clean.split()) & ARRANGEMENT:
        return _has_phrase(clean, PLAN)
    if _has_phrase(clean, PLAN) or _going_to_plan(clean):
        return True
    return bool(BOOKED.search(clean) and set(clean.split()) & STEP_NOUNS
                and set(clean.split()) & BIGGER_PLAN)


def _asked_last(memory):
    turns = memory.get("turns") or []
    last = str((turns[-1] if turns else {}).get("bot") or "").strip()
    return last.endswith("?")


def a_want_said_back(said_back, clean):
    if A_LOSS_IN_THE_LINE.search(str(clean or "")) or A_CONDOLENCE.search(str(said_back or "")):
        return False
    from ..memory import repeat
    return repeat.only_said_it_back(clean, said_back)


def dependant_want_reply_for(clean, words, memory):
    if not clean or not DEPENDANT_WANT.search(clean):
        return None
    if set(words) & NOT_PLAIN or _has_phrase(clean, CRISIS):
        return None
    if ASKED_OF_THE_PERSON.search(clean) or WANTS_TO_BE.search(clean):
        return None
    if set(words) & A_WEAPON:
        return None
    if set(words) & WEAPON_WORDS and not _has_phrase(clean, NOT_A_WEAPON):
        return None
    if set(words) & ASKS or _has_phrase(clean, DOUBT):
        return None
    if _has_phrase(clean, COUNTERFACTUAL):
        return None
    options = DEPENDANT_WANT_REPLIES
    if _asked_last(memory):
        options = tuple(o for o in options if not o.endswith("?")) or options
    return pick(options, memory, clean)


def reply_for(clean, words, memory, topics=()):
    if not clean or set(words) & NOT_PLAIN or _has_phrase(clean, CRISIS):
        return None
    if _has_phrase(clean, COUNTERFACTUAL) or set(words) & MARKED_DATE:
        return None
    if set(words) & ASKS or _has_phrase(clean, DOUBT):
        return None
    if not reads_as_plan(clean):
        return None
    options = PLAN_REPLIES_PLAIN if _has_phrase(clean, BARRIER) else PLAN_REPLIES
    if _asked_last(memory):
        options = tuple(o for o in options if not o.endswith("?")) or options
    return pick(options, memory, clean)


ARRANGED = re.compile(
    r"\b(?:i|we|i'?ve|we'?ve|ive|weve)\s+(?:(?:have|had|just|finally|only|already)\s+)*booked\b"
    r"|\b(?:i'?m|im|we'?re|were)\s+booking\b"
    r"|\b(?:is|are|was|were|it's|its)\s+(?:now\s+|all\s+|already\s+|finally\s+)?booked\b"
    r"|\b[a-z][a-z'\u2019-]*(?:\s+[a-z][a-z'\u2019-]*){0,2}\s+booked\s+"
    r"(?:for|on|at|in|next|this|tomorrow|today|tonight|yesterday|[0-9])\b")
DOUBLE_BOOKED = re.compile(r"\b(?:double|over|re)[- ]?book\w*")
WENT_WRONG = re.compile(
    r"\b(?:wrong|cancel(?:s|led|ling|lation)?|refund(?:s|ed|ing)?|charges?|charged|"
    r"overcharged|expired|expires|can'?t|cant|cannot|unable|couldn'?t|couldnt|didn'?t|didnt|"
    r"doesn'?t|doesnt|won'?t|wont|never|lost|missed|regret(?:s|ted|ting)?|dread(?:ing)?|"
    r"fell\s+through|mucked\s+up)\b")
TURNED = re.compile(r"\b(?:but|though|although|except|only)\b|\band\s+(?:now|then)\b")

BOOKED_REPLIES = (
    "Good - that's one off the list. When is it?",
    "Nice one. Is it soon, or have you got a while yet?",
    "Sorted. Is there anything left to sort before it?",
    "Good - that's one off the list.",
)
ALREADY_DATED = {
    "Good - that's one off the list. When is it?": "Good - that's one off the list.",
    "Nice one. Is it soon, or have you got a while yet?": "Nice one. Anything left to sort before then?",
}


QUESTION_FIRST = re.compile(
    r"^\W*(?:is|are|was|were|do|does|did|can|could|should|shall|will|would|have|has|am)\b", re.I)
THE_PERSON_WITH_IT = re.compile(r"^(?:i|we|i'?m|im|i'?ve|ive|we'?re|were|we'?ve|weve)\b", re.I)
HAD_IT_BOOKED = re.compile(r"\bhad\b(?:\s+\w+){0,5}\s+booked\b", re.I)


def reads_as_arranged(clean):
    if not clean or "?" in clean:
        return False
    if DOUBLE_BOOKED.search(clean):
        return False
    if WENT_WRONG.search(clean):
        return False
    booked = ARRANGED.search(clean)
    if booked and TURNED.search(clean[booked.start():]):
        return False
    if HAD_IT_BOOKED.search(clean):
        return False
    if booked and QUESTION_FIRST.match(clean) and not THE_PERSON_WITH_IT.match(clean[booked.start():]):
        return False
    return bool(booked)


def _says_when_it_is(clean):
    return bool(clean and facts.FUTURE.search(clean)) or bool(
        set(str(clean or "").lower().replace(",", " ").replace(".", " ").split())
        & (facts.DAYS | facts.MONTHS))


def arranged_reply_for(clean, words, memory):
    if set(words) & NOT_PLAIN or _has_phrase(clean, CRISIS):
        return None
    if _has_phrase(clean, COUNTERFACTUAL) or set(words) & MARKED_DATE:
        return None
    if set(words) & ASKS or _has_phrase(clean, DOUBT):
        return None
    if not reads_as_arranged(clean):
        return None
    options = BOOKED_REPLIES
    if _says_when_it_is(clean):
        options = tuple(ALREADY_DATED.get(o, o) for o in options)
    if _asked_last(memory):
        options = tuple(o for o in options if not o.endswith("?")) or options
    return pick(options, memory, clean)


INTEREST_DOING = (
    "How's it going with the {thing}?",
    "{Thing} - how long have you been at it?",
    "What got you into {thing}?",
    "How are you finding the {thing}?",
    "How's {thing} treating you?",
)
INTEREST_STARTED = (
    "How are the first weeks of the {thing} going?",
    "Nice one - what have you got so far with the {thing}?",
    "Are you going to a class for the {thing}, or working it out yourself?",
    "What made you start {thing}?",
    "Good luck with the {thing}. How are you finding it?",
)
INTEREST_DOING_PLAIN = (
    "There's a lot in the {thing} worth talking about, so say more when you want to.",
    "Good thing to be into. I'm happy to talk about the {thing} any time.",
)
INTEREST_STARTED_PLAIN = (
    "The first few weeks of the {thing} are the hard part. Say how it goes.",
    "Good luck with the {thing} - it gets easier once it is a habit.",
)
INTEREST_BACK = (
    "What got you back into {thing}?",
    "Welcome back to it - what made you pick {thing} up again?",
    "How's the {thing} going the second time round?",
)
INTEREST_BACK_PLAIN = (
    "Good to hear you're back at it. Say how the {thing} goes.",
    "Nice that you went back to the {thing} - it comes back faster the second time.",
)
NOT_AN_INTEREST = frozenset("""work job jobs shift shifts nights overtime rota house home
    cleaning ironing washing shopping money trouble debt him her them you me it this that
    everything anything nothing something trouble bother fights arguments""".split())


def _named(template, thing):
    said = template.replace("{thing}", thing)
    return said.replace("{Thing}", thing[0].upper() + thing[1:])


def interest_reply_for(interest, memory):
    if not isinstance(interest, dict):
        return None
    thing = str(interest.get("text") or "").strip()
    if not thing or any(word in NOT_AN_INTEREST for word in thing.split()):
        return None
    started = interest.get("shape") == "started"
    back = bool(interest.get("back"))
    asked_last = _asked_last(memory)
    if back:
        options = INTEREST_BACK_PLAIN if asked_last else INTEREST_BACK
    else:
        options = INTEREST_STARTED_PLAIN if started else INTEREST_DOING_PLAIN
        if not asked_last:
            options = INTEREST_STARTED if started else INTEREST_DOING
    return pick(tuple(_named(template, thing) for template in options), memory, thing)
