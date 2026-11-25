import re

from . import pick

_HOW = re.compile(
    r"^\s*(?:(?:so|and|but|ok|okay|well|then|just|right|anyway|oh|hmm|yeah|yes|alright)\s*,?\s+)*"
    r"(?P<ask>(?:any\s+idea|do\s+you\s+know)?\s*(?:how|what)\s*"
    r"(?:(?:was|were|did|have|has|is|are)\s+)?)(?P<rest>.*)$", re.I)
_THING = re.compile(
    r"^\s*(?:(?:the|your|his|her|their|my|our)\s+)?(?:(?:new|first|last|old|big)\s+)?"
    r"(?:night out|first day|last day|day out|trip|holiday|honeymoon|wedding|weekend|break|party|"
    r"dinner|meal|lunch|flight|journey|drive|move|interview|exam|exams|test|tests|scan|"
    r"appointment|match|game|play|concert|show|meeting|presentation|shift|course|day|week|"
    r"morning|afternoon|evening|night|kids|children|boys|girls|family|mum|mom|dad|sister|"
    r"brother|son|daughter|baby|dog|cat|puppy|kitten|vet|doctor|dentist|hospital|school|"
    r"nursery|work|job|uni|house|flat|viewing|results|date|today|yesterday|session|class|lesson|"
    r"stay|audition|driving test|theory test|appraisal|surgery|procedure|operation|court|hearing)\b",
    re.I)
_AFTER = (r"(?:\s+(?:yet|now|today|tomorrow|though|then|again|back|at all|about it|with that|with it"
          r"|hear|heard|reply|replied|get back|got back|call back|ring back|phone back|to you"
          r"|these days|so far|alright|ok|okay|fine|good|in the end|anything|something|either"
          r"|at the vets|at the hospital|at the doctor"
          r"|about\s+(?:him|her|them|it|that|this|me|us|the\s+\w+)"
          r"|at\s+(?:school|nursery|work|home|uni|college)"
          r"|with\s+(?:the|his|her|their|my|our)\s+\w+)){0,2}\s*[?.!]*$")
_TAIL = re.compile(
    r"^(?:\s+(?:go|went|do|going|get on|got on|get along|turn out|end up|come out|hold up)\b)?"
    r"(?:\s+(?:today|tonight|yesterday|last night|last week|then|though|so far|in the end|again|"
    r"yet|all right|alright|ok|okay|fine|good)){0,2}"
    r"(?:\s+with\s+(?:the|his|her|their|my|our|your)\s+\w+)?\s*[?.!]*$", re.I)
_PRONOUN = re.compile(
    r"^\s*(?:and\s+|so\s+|but\s+|ok\s+|okay\s+|well\s+)?"
    r"how\s+(?:did|was|were)\s+(?:it|that|this|they|he|she)"
    r"(?:\s+(?:go|went|get on|got on|get along|turn out|come out|work out)\b[^?]*"
    r"|(?:\s+(?:then|though|today|tonight|last night|in the end|overall|really|so far)){0,2})"
    r"[?.!]*$", re.I)
_PEOPLE = (
    r"vet|doctor|dentist|optician|physio|counsel\w*|consultant|nurse|midwife|surgeon|"
    r"plumber|electrician|builder|roofer|locksmith|mechanic|garage|glazier|decorator|"
    r"engineer|delivery\s*(?:man|driver)?|courier|driver|agent|estate\s+agent|letting\s+agent|"
    r"(?:boiler|gas|window|bathroom|kitchen|damp|carpet)\s*(?:man|lady|fitter|guy|person|"
    r"people|firm|company)|"
    r"recruit\w*|agency|recruitment\s+agency|employer|manager|boss|hr|payroll|"
    r"hospital|school|nursery|college|university|uni|council|job\s*centre|dwp|hmrc|"
    r"passport\s+office|dvla|care\s+home|social\s+worker|bank|building\s+society|landlord|"
    r"solicitor|conveyanc\w*|broker|insurer|insurance|mortgage\s+(?:man|adviser|advisor)?"
)
_STATE = re.compile(
    r"^(?:is|are|were|was|did|does|do|has|have)\s+(?:(?:the|your|my|our)\s+)?"
    r"(?:kids|children|boys|girls|family|mum|mom|dad|sister|brother|son|daughter|baby|dog|cat|"
    r"puppy|kitten|" + _PEOPLE + r"|"
    r"scan|appointment|interview|exam|test|"
    r"results|party|wedding|trip|flight|match|game|bank|council|landlord|solicitor|"
    r"boiler|car|washing\s+machine|parcel|parcels|order|delivery|package|"
    r"roof|fence|extension|bathroom|kitchen|drive|driveway|paving|patio|garden|shed|loft|"
    r"wall|floor|flooring|door|doors|window|windows|radiator|gutter|gutters|drain|drains|"
    r"chimney|damp\s*course)\b"
    r"\s+(?:ok|okay|all right|alright|fine|good|bad|home|yet|back|there|asleep|awake|ring|call|"
    r"phone|say|said|come|came|turn up|turned up|show|go|went|do|done|arrive|arrived|land|landed"
    r"|got back|get back|hear|heard|reply|replied|say anything|say something|got there"
    r"|show up|showed up|show up yet|turn up yet|come yet|came yet|got to (?:school|work|the "
    r"hospital|the vets?|nursery)|get to (?:school|work)|hear back|heard back|ring back|call back"
    r"|phone back|been in touch|get in touch|get back to (?:you|me)|got back to (?:you|me)"
    r"|confirmed|come through|come back|come back ok|got sorted|been round|been out"
    r"|hold up|held up|get done|got done|get home|got home|go ok|go alright|been done)\b"
    + _AFTER, re.I)
_STATE_BARE = re.compile(
    r"^(?:is|are|were|was|did|has|have)\s+"
    r"(?:(?:they|he|she)\s+(?:ok|okay|all right|alright|fine|good|bad|home|yet|back|there|asleep"
    r"|awake|ring|call|phone|say|said|come|came|turn up|turned up|arrive|arrived|land|landed|show"
    r"|go|went|do|done|got back|got there)"
    r"|it\s+(?:ok|okay|all right|alright|fine|good|bad|home|yet|back|there|asleep|awake|ring|call"
    r"|phone|said|came|turned up|arrived|landed|got back|got there))\b" + _AFTER, re.I)
_NAMES = re.compile(r"^(?:were|was)\s+[a-z']+(?:\s+and\s+[a-z']+)?\s+there\b[^?]*[?.!]*$", re.I)
_HEARD_BACK = re.compile(
    r"^\s*(?:and\s+|so\s+)?(?:did|do|does|have|has|had)\s+"
    r"(?:you|they|he|she|we|anybody|anyone|somebody|someone|nobody)\s+"
    r"(?:hear|heard|get|got|have|had)\s+(?:back|anything|something|any\s+news|a\s+reply|"
    r"an\s+answer|word)\b[^?]*[?.!]*$", re.I)
_SAID = re.compile(
    r"^\s*(?:and\s+)?what\s+(?:did|do|does)\s+(?:(?:the|your|my|our)\s+)?"
    r"(?:" + _PEOPLE + r"|teacher|head|she|he|they)\s+"
    r"(?:say|said|tell you)\b[^?]*[?.!]*$", re.I)
_ABOUT_THE_BOT = re.compile(
    r"^\s*(?:how|what)\s+(?:was|is|were|did|does|do|has|have|'s|s|'d|d)?\s*yours?(?:elf)?\b",
    re.I)
LINES = (
    "You tell me - {ask}?",
    "I wasn't there, so you know better than me - {ask}?",
    "Only you know that one. {Ask}?",
    "No way for me to know that from here - {ask}?",
)
CARE_LINES = (
    "I have no way of knowing, and I would rather ask than guess - {ask}?",
    "That is yours to tell me, and I am listening - {ask}?",
    "I hope it went as well as it could. {Ask}?",
)


from . import fallback_data as _data

WHO_TO_ASK = tuple(sorted(
    {who for _words, who in _data.WHO_TO_ASK}
    | {value for name, value in vars(_data).items()
       if name.endswith("_WHO") and isinstance(value, str)}
))


def pool_for(text, care=False):
    ask = reads(text)
    if not ask:
        from ..understanding import understand
        ask = reads(understand(text).get("plain") or "")
    if not ask:
        return None
    said_back = ask[:1].upper() + ask[1:]
    return tuple(line.format(ask=ask, Ask=said_back) for line in (CARE_LINES if care else LINES))


def reads(clean, repaired=None):
    text = " ".join(str(clean or "").lower().replace("\u2019", "'").split())
    if not text or len(text.split()) > 14:
        return None
    plain = " ".join(str(repaired or "").lower().replace("\u2019", "'").split())
    match = " ".join(re.sub(r"\bhow'd\b|\bhowd\b", "how did",
                            re.sub(r"\bhow's\b|\bhows\b", "how is", plain or text)).split())
    if _ABOUT_THE_BOT.match(text) or _ABOUT_THE_BOT.match(plain) or _ABOUT_THE_BOT.match(match):
        return None
    ask = re.sub(r"^hows\b", "how's", re.sub(r"^howd\b", "how'd", text)).strip().rstrip("?.! ")
    how = _HOW.match(match)
    if how:
        rest = how.group("rest")
        thing = _THING.match(rest)
        if thing and _TAIL.match(rest[thing.end():]):
            return ask
    for pattern in (_STATE, _STATE_BARE, _SAID, _HEARD_BACK, _PRONOUN, _NAMES):
        if pattern.match(match):
            return ask
    return None



OWN_FIGURE = ("rent", "mortgage", "council tax", "bill", "bills", "premium", "tariff",
              "direct debit", "payment", "payments", "balance", "deposit", "service charge",
              "arrears", "fee", "fees", "subscription", "charges", "salary", "wage", "wages",
              "pension", "loan", "overdraft", "interest", "standing order", "outgoings")
OWN_DATE = ("holiday", "holidays", "appointment", "appointments", "booking", "bookings", "flight",
            "renewal", "mot", "service", "deadline", "contract", "tenancy", "delivery", "check-in",
            "checkin", "expiry", "expires", "collection", "pick up", "pickup", "completion",
            "install", "installation", "viewing", "moving date", "move date", "end", "ends",
            "ending", "runs out", "run out", "run out date")
OWN_POLICY = ("insurance", "policy", "policies", "cover", "covered", "covers", "covering",
              "warranty", "guarantee", "excess", "claim", "claims", "protected", "included",
              "excluded")
OWN_FIGURE_LINES = (
    "I can't see your account, sorry. That figure is on your last statement or in the app for it, "
    "and the provider will read it out if you ring.",
    "Nothing of yours is in front of me. Your statement or that provider's app has the exact "
    "amount; if it looks wrong, they are the ones to ring.",
    "I've no way to check your own bills. The last email or statement has it, and the payments in "
    "your banking app usually show it too.",
)
OWN_POLICY_LINES = (
    "I can't read your policy from here, sorry. What it covers is in the schedule or the policy "
    "document, and the insurer will confirm it on the phone in a couple of minutes.",
    "Nothing of yours is in front of me. The policy wording has it under what is covered; a call "
    "settles it faster than reading it.",
    "I can't check a policy I can't see. The schedule that came with it lists what is covered and "
    "what the excess is, and the insurer can read it back to you.",
)
OWN_DATE_LINES = (
    "I can't see your diary, sorry. It will be in the confirmation email or the text they sent "
    "when you booked - tell me what it says and I'll help you plan around it.",
    "No way to see your own dates from here. The booking email or the calendar on your phone has "
    "it, and whoever you booked with can confirm it in a minute if not.",
    "I can't look at your own diary. The confirmation email is the first place: it is in there "
    "nine times out of ten.",
)
_A_LIFE_CHOICE = re.compile(
    r"(?:\b(?:my|our)\s+(?:\w+\s+){0,2}(?:job|jobs|work|career|boss|team|school|college|uni|"
    r"university|course|degree|flat|house|home|town|city|country|area|class|gym|club|hobby|"
    r"subject|placement|apprenticeship|business|role|position)\b"
    r"|\bwhere\s+i\s+(?:live|work|am)\b)")
_OWN_TASTE = re.compile(
    r"\b(?:do|would|will|am|did)\s+i\s+(?:even\s+)?(?:like|love|hate|enjoy|prefer)\s+"
    r"(?!it\b|that\b|this\b|them\b|those\b|these\b|one\b|him\b|her\b)")
OWN_LIFE_LINES = (
    "Only you can say, and I don't want to guess at it for you. What is making you wonder?",
    "That one is yours to answer. What would make it better for you - more of something, or less "
    "of something?",
)
OWN_TASTE_LINES = (
    "You know that one better than I do - taste is the one thing nobody can check for you. The "
    "worst case is one mouthful.",
    "Only you can say. Have it and see - what you fancy is not something anyone can tell you.",
    "That is yours to know. Taste changes, too, so the last time is worth trying again.",
)
_ASKS_FOR_ADVICE = re.compile(
    r"^\s*(?:(?:so|and|ok|okay|well|then|right|but)\s*,?\s+)?"
    r"(?:how\s+(?:do|can|could|should|would|to|might)\b|what\s+(?:should|could|can|do)\s+i\b|"
    r"where\s+(?:can|do|should|could)\s+i\b|any\s+(?:advice|ideas|tips)\b|"
    r"is\s+it\s+(?:ok|okay|worth|better|cheaper|cheapest|possible)\b|"
    r"am\s+i\s+(?:better|allowed|able)\b)")
_ASKS = re.compile(r"\?|\b(?:what|whats|what's|when|where|which|how|is|are|was|were|do|does|did|"
                   r"has|have|can|could|should|am)\b", re.I)
_MINE_AND_THING = re.compile(r"\b(?:my|our)\s+(?P<thing>[a-z][a-z' ]{0,40})")
_A_COMPOSITION = re.compile(r"\b(?:comes?\s+out\s+of|coming\s+out\s+of|deduct\w*|(?:take|takes|taken|taking)\s+(?:\w+\s+){0,2}off|"
                            r"added\s+(?:on|to)|on\s+top\s+of|worked\s+out|calculated)\b")
_AN_IDENTIFIER = re.compile(r"\b(?:numbers?|sort\s+code|reference|ref|licence|license|pin|"
                            r"username|password|log\s?in)\b")
_A_WHEN = re.compile(r"\b(?:when|what\s+date|which\s+date|how\s+long|how\s+soon|due)\b")
_NOT_A_DIARY = re.compile(r"\b(?:due|baby|pregnan\w*|midwife|scan|test results|biopsy)\b")
_A_DEPOSIT = re.compile(r"\bdeposits?\b")


def own_fact(text, memory=None):
    line = " ".join(str(text or "").lower().replace("\u2019", "'").split())
    if not line or len(line.split()) > 14:
        return None
    if _ASKS_FOR_ADVICE.match(line) or not _ASKS.match(" ".join(line.split()[:3])):
        return None
    if _A_LIFE_CHOICE.search(line):
        return ("life", "")
    if _OWN_TASTE.search(line):
        return ("taste", "")
    mine = _MINE_AND_THING.search(line)
    if not mine:
        return None
    thing = mine.group("thing")
    if _NOT_A_DIARY.search(line):
        return None
    if _A_DEPOSIT.search(line):
        return None
    if _AN_IDENTIFIER.search(line):
        return None
    order = (("policy", OWN_POLICY), ("figure", OWN_FIGURE), ("date", OWN_DATE))
    if _A_WHEN.search(line):
        order = (("date", OWN_DATE), ("policy", OWN_POLICY), ("figure", OWN_FIGURE))
    for kind, words in order:
        if not any(re.search(r"(?<![a-z])" + re.escape(word) + r"(?![a-z])", thing)
                   for word in words):
            continue
        if kind == "figure" and _A_COMPOSITION.search(line):
            return None
        return (kind, "")
    return None


def own_fact_for(text, memory=None):
    read = own_fact(text)
    if not read:
        return None
    kind = read[0]
    pool = {"figure": OWN_FIGURE_LINES, "date": OWN_DATE_LINES, "policy": OWN_POLICY_LINES,
            "taste": OWN_TASTE_LINES, "life": OWN_LIFE_LINES}[kind]
    return pick(pool, memory or {}, str(text or "").lower())
