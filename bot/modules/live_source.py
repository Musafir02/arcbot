import re

PRIORITY = -998

BANK_HOLIDAY = ("bank holiday", "bank holidays", "public holiday")
TERM = ("school holidays", "school holiday",
            "term dates", "term date", "school term", "half term", "half-term", "inset day",
            "when do the schools", "when do schools", "when does term",
            "when do the kids break up", "when do they break up", "when do we break up",
            "school go back", "schools go back", "go back to school",
            "school start", "schools start", "school finish", "schools finish",
            "break up for", "summer holidays start", "summer holiday start", "school break up",
            "schools off", "schools are off", "school off", "is school off",
            "schools closed", "are schools closed")
CALENDAR = BANK_HOLIDAY + TERM
CALENDAR_NOT = ("ticketed", "ticket", "fine", "fine'd", "parking", "booked off", "my shift",
                "rota", "overtime", "day rate",
                "post", "postman", "deliveries", "delivery", "buses", "bus", "trains", "train",
                "timetable", "shops", "shop", "supermarket", "open", "closed", "close",
                "runs", "run on", "running", "collections", "collection",
                "bin", "bins", "rubbish", "tips", "the tip", "banks", "the bank",
                "pharmacy", "dentist", "doctor", "swimming", "pool")
CALENDAR_SCHOOL = ("school", "schools", "term", "half term", "half-term", "inset day",
                   "term time", "break up", "go back")
CALENDAR_OPEN = re.compile(r"^(?:when|what|which|is|are|do|does|will|should|how)\b")
CALENDAR_PLAN = re.compile(
    r"\b(?:what (?:can|should|could) (?:i|we|you) do|things to do|something to do|"
    r"ideas|activities|days out|day out|keep (?:the |them |my )?\w* ?busy|places to go)\b")

NATIONAL_DRAW = ("lottery", "lotto", "euromillions", "euro millions", "thunderball",
                 "scratchcard", "scratch card", "jackpot", "numbers come up", "my numbers",
                 "the balls", "lotto numbers")
TICKET = ("ticket win", "tickets win", "ticket won", "tickets won", "ticket come up",
          "tickets come up", "ticket a winner", "tickets a winner", "my ticket", "our ticket")
LOCAL_DRAW = ("raffle", "sweepstake", "sweepstakes", "tombola", "bingo", "the draw",
              "prize draw", "draw ticket", "draw tickets", "the raffle", "the tombola",
              "meat raffle", "bonus ball")
MONTHLY_DRAW = ("postcode lottery", "premium bonds", "premium bond", "premium bond draw")
DRAW = NATIONAL_DRAW + LOCAL_DRAW + MONTHLY_DRAW + TICKET
DRAW_ASK = re.compile(
    r"\b(?:did|do|does|are|is|have|has|any)\b[^?]{0,40}?"
    r"\b(?:win|won|winner|winners|winning|come up|came up|result|results|numbers|draw|drawn"
    r"|check)\b")

WAIT = ("queue", "queues", "wait", "waiting", "busy", "backed up", "how long")
AIRPORT = ("airport", "terminal", "security", "passport control", "check in", "check-in",
           "bag drop", "departures hall")
A_E = ("a and e", "a&e", "casualty", "accident and emergency", "emergency department",
       "minor injuries", "urgent care", "walk in centre", "walk-in centre")

LEAD_IN = re.compile(r"^(?:ok|okay|oh|so|and|but|also|anyway|anyways|btw|right|well|hmm|um|er|"
                     r"like|sorry|quick one|one more|then|now|hi|hey|yeah|yep|please)[\s,.!-]+")
ASKS = re.compile(r"^(?:when|what|which|who|whose|where|why|how|is|are|was|were|do|does|did|"
                  r"can|could|will|would|should|shall|may|might|have|has|had|any|am)s?\b")

BANK_LINES = (
    "In England and Wales the bank holidays are 1 January, Good Friday, Easter Monday, the first "
    "and last Mondays in May, the last Monday in August, then 25 and 26 December - so only the "
    "Easter ones and this year's May and August Mondays need looking up. Scotland adds 2 January "
    "and 30 November and has no Easter Monday, and Northern Ireland adds 17 March and 12 July; "
    "gov.uk's bank-holidays page has the exact date for each nation.",
    "The bank holidays that move are the Easter ones and the first and last Mondays in May and "
    "August; the rest are 1 January, 25 December and 26 December - in England and Wales. Scotland "
    "and Northern Ireland differ (2 January and St Andrew's Day, St Patrick's Day and the "
    "Twelfth), so I can't give one list for the UK: gov.uk's bank-holidays page has the date, "
    "nation by nation.",
)
TERM_LINES = (
    "English state schools run three terms - September to December, January to Easter, and "
    "Easter to July - with a week off in October, February and May and about six weeks in "
    "summer. The exact weeks are set locally, so the council's school-term-dates page or the "
    "school's own site has this year's.",
    "A school year in England is three terms with a week's half term in October, February and "
    "May, two weeks at Christmas and about six weeks in summer, with the summer break starting in "
    "the second half of July. Which week is which is the council's or the school's to publish, "
    "because it differs by area - and Scotland and private schools run to their own calendar.",
)
AIRPORT_LINES = (
    "Most airlines want you there two hours before a short-haul flight and three before a "
    "long-haul one, and security is the queue that eats the time - the airport's own site and "
    "the boards in the terminal show that wait live, and the airline's app has the gate.",
    "Two hours before a short-haul departure and three before long-haul is the check-in rule, "
    "and passport control is the queue that surprises people at peak times. The airport itself "
    "publishes both waits on its site and on the boards, because I can't see them from here.",
)
A_E_LINES = (
    "For anything that is not life-threatening, an urgent-care centre or a minor injuries unit "
    "usually sees you faster than A&E, and NHS 111 will say which one near you has room tonight "
    "as well as the A&E waits, which the hospital publishes itself.",
    "A&E is for the things that cannot wait, and everything else moves quicker at urgent care or "
    "a minor injuries unit. Ring 111 - it knows which of them near you is quietest tonight and "
    "what the A&E wait is - because that changes by the hour and I can't see it.",
)
NATIONAL_LINES = (
    "Lotto draws on Wednesday and Saturday evenings and EuroMillions on Tuesday and Friday, so a "
    "result that is not up yet usually is not in yet. Your numbers are on the ticket: the app or "
    "the terminal in the shop that sold it checks a ticket in a second.",
    "The draws are in the evening - Lotto on Wednesday and Saturday, EuroMillions on Tuesday and "
    "Friday - and the result goes up with the operator straight after. Checking is instant on "
    "the ticket's own app or at the shop terminal, because I can't see the draw from here.",
)
LOCAL_LINES = (
    "A raffle, a sweepstake or a tombola is the organiser's to confirm - they hold the numbers, "
    "and at a club the caller has them on the night or they go up on the board by the door. I "
    "can't see a draw I was not in, so whoever sold you the ticket is the one to ask.",
    "There is no page to look a local draw up on: the organiser keeps the numbers, and a work or "
    "club sweepstake is called out on the night or pinned up afterwards. The seller or the "
    "organiser is the person who can check a ticket, not me.",
)
TICKET_LINES = (
    "Whether a ticket won depends on what it is for: a Lotto or EuroMillions ticket checks itself "
    "in the Lotto app or at the shop terminal, and a raffle or sweepstake ticket is the "
    "organiser's to confirm. The numbers are on the ticket either way, and I can't see the draw.",
    "It depends on the kind of ticket - the national draws check in the Lotto app or at a shop "
    "terminal, and a raffle or a sweepstake is the organiser's to call. Your numbers are printed "
    "on it, which is the only part I could not see for you.",
)
MONTHLY_LINES = (
    "Premium Bonds are drawn at the start of each month and the Postcode Lottery through the "
    "month, and both check your numbers for you: NS&I's own site or app for the Bonds, the "
    "Postcode Lottery's site with your postcode. I can't see either draw from here.",
    "The monthly draws are the operator's - NS&I publishes each Premium Bonds prize and its "
    "holder on its own site, and the Postcode Lottery's site takes your postcode and shows "
    "whether it has come up. That is the only place a result is real.",
)

_BOUNDED = {}


def _bounded(phrase):
    pattern = _BOUNDED.get(phrase)
    if pattern is None:
        pattern = _BOUNDED[phrase] = re.compile(r"(?<![a-z])" + re.escape(phrase) + r"(?![a-z])")
    return pattern


def _has(clean, phrases):
    for phrase in phrases:
        if _bounded(phrase).search(clean):
            return True
    return False


def _pick(clean, lines):
    return lines[sum(clean.encode("utf-8")) % len(lines)]


def _clean(text):
    return " ".join(str(text or "").lower().split())


def _a_date_ask(clean):
    if not CALENDAR_OPEN.match(_without_lead_in(clean)):
        return ()
    if CALENDAR_PLAN.search(clean):
        return ()
    if _has(clean, CALENDAR_NOT) and not _has(clean, CALENDAR_SCHOOL):
        return ()
    if _has(clean, TERM):
        return TERM_LINES
    if _has(clean, BANK_HOLIDAY):
        return BANK_LINES
    return ()


def _without_lead_in(clean):
    said = clean
    while True:
        shorter = LEAD_IN.sub("", said, count=1)
        if shorter == said or not shorter.strip():
            return said
        said = shorter


def _a_draw_ask(clean):
    if not _has(clean, DRAW) or not DRAW_ASK.search(clean):
        return ()
    if _has(clean, MONTHLY_DRAW):
        return MONTHLY_LINES
    if _has(clean, LOCAL_DRAW) and not _has(clean, NATIONAL_DRAW):
        return LOCAL_LINES
    if _has(clean, NATIONAL_DRAW):
        return NATIONAL_LINES
    return TICKET_LINES


def _a_queue(clean):
    if not _has(clean, WAIT):
        return ()
    if _has(clean, A_E):
        return A_E_LINES
    if _has(clean, AIRPORT):
        return AIRPORT_LINES
    return ()


def respond(text, memory=None):
    clean = _clean(text)
    said = _without_lead_in(clean)
    if not clean or not (ASKS.match(said) or "?" in str(text or "")):
        return None
    lines = _a_queue(clean)
    if lines:
        return _pick(clean, lines)
    if _a_draw_ask(clean):
        return _pick(clean, _a_draw_ask(clean) or LOCAL_LINES)
    lines = _a_date_ask(clean)
    if lines:
        return _pick(clean, lines)
    return None
