import re

OTHERS = frozenset((
    "he", "she", "him", "her", "his", "hers", "they", "them", "their", "theirs",
    "mum", "mam", "mom", "mummy", "dad", "daddy", "father", "mother", "parent", "parents",
    "son", "daughter", "child", "kid", "kids", "baby", "toddler", "teenager", "boy", "girl",
    "husband", "wife", "partner", "boyfriend", "girlfriend", "fiance", "fiancee",
    "nan", "nana", "gran", "granny", "grandma", "grandad", "grandpa", "grandparents",
    "brother", "sister", "sibling", "aunt", "uncle", "cousin", "nephew", "niece",
    "friend", "mate", "flatmate", "housemate", "neighbour", "neighbor", "colleague",
    "boss", "manager", "carer", "dog", "cat", "puppy", "kitten", "pet", "pup",
))

SAID = re.compile(r"\b(?:said|says|say|told\s+me|reckons|quoted|quotes)\b")

SELF_SAID = re.compile(r"\bi\s+(?:said|say|says|told)\b")

YOU_SAID = re.compile(r"\byou\s+(?:said|says|say|told\s+me)\b")

CARE = frozenset((
    "doctor", "doctors", "gp", "nurse", "consultant", "physio", "physiotherapist",
    "midwife", "paramedic", "hospital", "clinic", "surgery", "radiographer",
    "optician", "podiatrist", "chiropodist", "dietician", "dietitian", "111", "nhs",
    "dentist", "dentists", "optometrist", "optometrists",
))

TRADE = frozenset((
    "plumber", "mechanic", "garage", "garages", "roofer", "builder", "electrician", "engineer",
    "locksmith", "dealer", "fitter", "joiner", "tiler", "plasterer", "decorator", "glazier",
    "man", "tradesman", "contractor", "boiler", "drain", "drains", "surveyor",
))

OFFICE = frozenset((
    "council", "bank", "landlord", "landlady", "insurer", "insurance", "dwp", "jobcentre",
    "school", "teacher", "college", "university", "letting", "agent", "mortgage", "broker",
    "solicitor", "conveyancer", "planning", "housing", "ombudsman", "tribunal", "assessment",
    "assessor", "office", "authority",
))

EMERGENCY = re.compile(r"\b(?:999|911|112|116\s*123|ambulance|a\s*&\s*e|a\s+and\s+e|casualty|"
                       r"resus|crash\s+team|blue\s+light)\b")

ASKED = re.compile(r"\?|\b(?:should\s+i|shall\s+i|is\s+(?:that|it|this)|is\s+\d|how\s+(?:much|long)"
                   r"|worth\s+it|about\s+right|too\s+much|fair|reasonable|can\s+i|could\s+i)\b")

A_TIME = re.compile(r"\b(?:would\s+take|will\s+take|takes\s+(?:\w+\s+)?(?:weeks?|months?|days?)"
                    r"|(?:two|three|four|five|six|seven|eight|nine|ten|twelve|\d+)\s+"
                    r"(?:weeks?|months?|days?|fortnights?)"
                    r"|(?:in|for|of|after)\s+an?\s+(?:week|fortnight|month|day|few\s+days)"
                    r"|(?:coming|due|here|back|round|in)\s+(?:on\s+|at\s+|in\s+|by\s+)?(?:the\s+)?"
                    r"(?:mon|tues|wednes|thurs|fri|satur|sun)day"
                    r"|(?:coming|due|here|back)\s+(?:on\s+|at\s+|in\s+)?(?:the\s+)?"
                    r"(?:morning|afternoon|evening|weekend|afternoon|\d{1,2}(?:[.:]\d\d)?\s*(?:am|pm)?)\b"
                    r"|(?:coming|due|here|back)\s+(?:tomorrow|tonight|today|next\s+\w+|this\s+\w+)"
                    r"|be\s+here\s+(?:between|at|on|in|by)|sometime\s+(?:next|this)\s+week"
                    r"|(?:come|comes|coming|call|call\s+in|turn\s+up)\s+(?:back\s+)?"
                    r"(?:in\s+the\s+|this\s+)?(?:morning|afternoon|evening)"
                    r"|first\s+week\s+of\s+\w+)\b")

A_PLAN = re.compile(r"\b(?:come\s+back|coming\s+back|go\s+back|come\s+in\s+again|refer\w*|"
                    r"review\w*|follow\s*-?\s*up|check\s*-?\s*up|wait\w*|"
                    r"keep\s+an\s+eye|monitor\w*|bloods?|scan\w*|x-?rays?|prescription|"
                    r"appointment|another\s+look|see\s+how\s+\w+\s+goes)\b")

A_TREATMENT = re.compile(
    r"\b(?:crown|crowns|filling|fillings|root\s+canal|extraction|implant|implants|bridge|"
    r"dentures?|braces|invisalign|scale\s+and\s+polish|glasses|lenses|varifocals|"
    r"needs?\s+(?:doing|replacing|seeing\s+to)|has\s+to\s+come\s+out)\b")
A_CHANGE = re.compile(
    r"\b(?:changed|worse|a\s+bit\s+high|borderline|not\s+where\s+it\s+should\s+be|"
    r"something\s+there|wants?\s+watching)\b")

ALL_CLEAR = re.compile(r"\b(?:is|are|was|were|come|comes|came)\s+(?:back\s+)?(?:all\s+)?"
                       r"(?:fine|ok|okay|normal|clear|negative|healthy|nothing)\b"
                       r"|\bnothing\s+(?:wrong|to\s+worry|sinister|serious)\b|\ball\s+clear\b")

DONE = re.compile(r"\b(?:fixed|sorted|done|finished|put\s+right|all\s+working|working\s+now"
                  r"|no\s+charge|on\s+the\s+mend)\b")

PRAISE = re.compile(r"\b(?:thanks?|thank\s+you|cheers|ta|well\s+done|good\s+(?:work|job)|"
                    r"lovely|great|brilliant|excellent|fantastic|perfect|happy|pleased|"
                    r"delighted|ready|no\s+charge|free\s+of\s+charge)\b")

GOOD_NEWS = re.compile(r"\bsaid\s+(?:that\s+)?(?:i|we|you)\s+(?:can|could|will|may)\s+have\b"
                       r"|\b(?:approved|accepted|went\s+through)\b")

MY_MAN = re.compile(r"\b(?:my|our|her|his|their)\s+(?:man|bloke|guy|fella|chap)\b")

TRADE_REPLIES = (
    "Get it in writing, with the parts and the labour apart, and one more quote before you say "
    "yes - two prices is the whole trick. Tell me the figure and I'll say whether it's in the "
    "usual range for the job.",
    "Ask what the cheapest version is that would still fix it, and what happens if it turns out to "
    "be something else once it's open. Put the figure to me and I'll tell you whether it's the "
    "going rate.",
    "Then ask for it in writing and price the job two ways - the whole lot, and the least that "
    "would get you through the year. If you give me the number I'll say whether it's fair.",
)

CARE_REPLIES = (
    "Ring back before then if it gets worse - you don't have to sit out the wait for the date. "
    "Keep a short note of what changes day to day so the next appointment is worth having.",
    "Then go with the plan, and ring the surgery the moment something changes rather than waiting "
    "for the date. Write down what you want to ask so the ten minutes aren't wasted.",
    "That's the plan, then. Ask what would make them bring it forward, and keep a note of what "
    "happens between now and then - that note is what makes the next appointment quick.",
)

CARE_PLAN_REPLIES = (
    "Then do as they said and keep a short note of what changes - what you noticed, when, and "
    "what made it better or worse. That note is exactly what they will ask for next time.",
    "Keep it simple and written down: date, what you noticed, and anything that made a "
    "difference. If it changes before you are seen again, ring and say so rather than waiting.",
    "Then watch for the change they named, and write down the first day you see it. A date and a "
    "description is what turns a worry into something they can act on.",
)

CARE_TREATMENT_REPLIES = (
    "Ask them two things before anything is agreed: what it means in plain words, and what "
    "happens if you do nothing for a while. If it is treatment, get the price both ways - on the "
    "NHS band and privately.",
    "Get it in plain words first: what changes if you have it done, what happens if you wait, and "
    "what it costs either way. Write the answers down while they are fresh.",
    "Worth asking what the next step is and when it would need doing by. If money comes into it, "
    "ask for the price on the NHS and privately before you book anything.",
)

OFFICE_REPLIES = (
    "Ask for it in writing, and ask what the next step in their own process is - most of these "
    "have a form or an appeal with a deadline, and whoever answers the phone will say which. "
    "Tell me what the letter says and I'll help you answer it.",
    "Get their reason in writing and ask what would change the answer. That reply is what an "
    "appeal or a second go hangs on, and I'll help you word it.",
    "Then ask them to confirm it in writing and how long the next step takes. Once you have their "
    "words I'll help you put your side of it.",
)

WAITING_REPLIES = (
    "Then keep the time clear and have what they need where they can get at it - paperwork, the "
    "boiler cupboard, the car keys on the table. Ring the office if nobody has turned up by the "
    "end of the slot; that call is what moves it.",
    "Put the day aside rather than the hour, and ring the office the moment the slot goes by "
    "without a word. If it slips again, ask them to hold the next appointment for you there and "
    "then.",
    "Then plan as if it happens and ring early if it doesn't - people who chase on the day get "
    "moved up the list. Have the details they will ask for written down: the job, the reference, "
    "and your number twice.",
)

A_SPAN = re.compile(r"\b(?:take|takes|took|taking|would\s+take|will\s+take)\b[^.]{0,20}?"
                    r"\b(?:two|three|four|five|six|seven|eight|nine|ten|twelve|\d+)\s+"
                    r"(?:weeks?|months?|days?|fortnights?)\b"
                    r"|\b(?:a|an|one)\s+(?:week|month|fortnight|day)\b"
                    r"|\b(?:in|for|of|after|another)\s+(?:two|three|four|five|six|\d+)\s+"
                    r"(?:weeks?|months?)\b")
A_WINDOW = re.compile(r"\b\d{1,2}(?::\d\d)?\s*(?:am|pm)\b|\bbetween\s+\d+|"
                      r"\bin\s+the\s+(?:morning|afternoon|evening)\b|"
                      r"\bany\s+time\s+after\b|\bo'?clock\b")

SPAN_REPLIES = (
    "Ask when they start, not when they finish - a start date in writing is the only part anyone "
    "can be held to, and everything after it follows. Then agree what happens if the weather or "
    "the scaffold puts it back, and keep the last payment until the work is signed off.",
    "Get the start date and the end date in writing, with what counts as a delay and who pays for "
    "it. A job that long is worth a short weekly update by text, in one line, so nothing drifts "
    "without you knowing.",
    "Then put the dates in your diary and ask them to confirm the start in writing a week before. "
    "If it slips, ask for a new date there and then rather than ringing back later - the date they "
    "say out loud is the one that sticks.",
)

POOLS = ((CARE, CARE_REPLIES), (TRADE, TRADE_REPLIES), (OFFICE, OFFICE_REPLIES))


def _words(text):
    return re.findall(r"[a-z0-9'&]+", str(text or "").lower())


def _the_subject(clean):
    head = SAID.split(clean, 1)[0]
    return _words(head)


def _the_pool(words):
    named = set(words)
    for parties, pool in POOLS:
        if named & parties:
            return pool
    return None


PRONOUN = re.compile(r"\b(?:he|she|him|her|they|them|his|their)\b")


def _last_party(game):
    if not isinstance(game, dict):
        return None
    said = []
    for turn in (game.get("turns") or [])[-4:]:
        if isinstance(turn, dict):
            if turn.get("user"):
                said.append(str(turn["user"]))
    for text in reversed(said):
        pool = _the_pool(_words(text))
        if pool is TRADE_REPLIES:
            return pool
    return None


def _recent_bot_lines(memory):
    said = []
    if isinstance(memory, dict):
        for turn in (memory.get("turns") or [])[-4:]:
            if isinstance(turn, dict) and turn.get("bot"):
                said.append(" ".join(str(turn["bot"]).lower().split()))
        if memory.get("bot"):
            said.append(" ".join(str(memory["bot"]).lower().split()))
    return [line for line in said if line]


def _choose(pool, memory):
    recent = _recent_bot_lines(memory)
    for line in pool:
        head = " ".join(line.lower().split())[:40]
        if not any(head in said for said in recent):
            return line
    return pool[0]


ABOUT_SOMEONE_ELSE = re.compile(
    r"\b(?:said|says|say|told\s+me)\s+(?:that\s+)?"
    r"(?:he|she)(?:'?s|'?ll|'?d)?\b|\b(?:said|says|say|told\s+me)\s+(?:that\s+)?my\s+[a-z]+\b")

CARER_REPLIES = (
    "Ask what it is for, who does it, and what changes in the meantime - and ask them to put the "
    "answer in an email so you have it.",
    "Ask which one they mean and who runs it, then when you would hear - a name and a date stop "
    "it being a guess.",
    "Ask what happens if you decide to wait before agreeing to it. That is a fair question and "
    "they should be able to answer it in plain words.",
)

CARER_ON_THE_DAY_REPLIES = (
    "Put the date in your phone, and ask now what they need from you beforehand, and who to ring "
    "if it moves.",
    "Ask what to bring and whether anything changes between now and then, and keep the number of "
    "the department that rang you.",
)


_CLEAR_WORDS = (
    r"doing\s+(?:well|great|fine|brilliantly)|all\s+clear|"
    r"(?:is|are|was|were|looks|look|seems|seem|sounds|sound)\s+(?:all\s+)?"
    r"(?:fine|ok|okay|alright|sound|clear|good|healthy|safe|solid)|"
    r"its\s+(?:fine|ok|okay|alright|sound)|"
    r"nothing\s+(?:wrong|to\s+worry\s+about|serious|to\s+do|to\s+pay)|"
    r"no\s+(?:problems?|issues?|faults?|damage)|"
    r"is\s+(?:well|better)|got\s+the\s+all\s+clear"
)
CLEARED = re.compile(r"\b(?:" + _CLEAR_WORDS + r")\b")
A_GOOD_SAID = re.compile(r"\b(?:" + _CLEAR_WORDS + r"|happy|pleased|proud|through\s+it|"
                         r"can\s+(?:have|stay|go|come\s+home)|is\s+allowed|well\s+done)\b")


def answer_for(text, memory):
    clean = " ".join(str(text or "").lower().split())
    if not clean or not SAID.search(clean):
        return None
    if (EMERGENCY.search(clean) or ASKED.search(clean) or SELF_SAID.search(clean)
            or YOU_SAID.search(clean)):
        return None
    if (DONE.search(clean) or ALL_CLEAR.search(clean)) and not A_TIME.search(clean):
        return None
    if PRAISE.search(clean) and not (A_TIME.search(clean) or A_PLAN.search(clean)):
        return None
    if MY_MAN.search(clean) or GOOD_NEWS.search(clean):
        return None
    if CLEARED.search(clean) and not (A_TIME.search(clean) or A_PLAN.search(clean)):
        return None
    words = _words(clean)
    pool = _the_pool(_the_subject(clean))
    if not pool:
        if not PRONOUN.search(clean):
            return None
        pool = _last_party(memory)
        if not pool:
            return None
    if pool in (CARE_REPLIES, OFFICE_REPLIES) and (set(words) & OTHERS):
        if (ABOUT_SOMEONE_ELSE.search(clean) and pool is OFFICE_REPLIES
                and not A_GOOD_SAID.search(clean)):
            if A_TIME.search(clean):
                return _choose(CARER_ON_THE_DAY_REPLIES, memory)
            return _choose(CARER_REPLIES, memory)
        return None
    if pool is CARE_REPLIES:
        if A_TIME.search(clean):
            return _choose(CARE_REPLIES, memory)
        if A_PLAN.search(clean):
            return _choose(CARE_PLAN_REPLIES, memory)
        if A_TREATMENT.search(clean) or A_CHANGE.search(clean):
            return _choose(CARE_TREATMENT_REPLIES, memory)
        return None
    if pool is not CARE_REPLIES and A_SPAN.search(clean) and not A_WINDOW.search(clean):
        return _choose(SPAN_REPLIES, memory)
    if pool is not CARE_REPLIES and A_TIME.search(clean):
        return _choose(WAITING_REPLIES, memory)
    return _choose(pool, memory)
