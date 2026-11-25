import re

PRIORITY = 7001
ANSWERS = ("geography-and-travel",)

VEHICLE = re.compile(
    r"\b(?:bus|buses|train|trains|tube|tram|trams|coach|coaches|ferry|ferries|flight|flights)\b",
    re.I)
TIME = re.compile(
    r"\b(?:when|what\s+time|how\s+soon|next|on\s+time|delayed|cancelled|canceled|running|due|"
    r"leaves?|departs?|comes?|arrives?|platform|replacement|engineering\s+works?)\b", re.I)
STATUS = re.compile(
    r"\b(?:on\s+time|delayed|cancelled|canceled|running|due|replacement|engineering\s+works?)\b",
    re.I)
PLATFORM = re.compile(r"\b(?:platform|station|stop|interchange|departure\s+board)\b", re.I)
PLACE_OPENING = re.compile(
    r"\b(?:train|bus|coach|tram|tube)\s+(?:station|stop)\b[^?.]{0,25}"
    r"\b(?:open|opens|opening|close|closes|closed|shut|shuts|hours)\b", re.I)
MONEY = re.compile(
    r"\b(?:worth|cost|costs|price|prices|fare|fares|cheap|cheaper|expensive|refund|refunds|"
    r"compensation|money|claim|claims|insurance|voucher|rebook|rebooking|delay\s+repay|pass|"
    r"rights?|entitled|entitlement|owed)\b",
    re.I)
ADVICE = re.compile(
    r"\b(?:what\s+if|should\s+(?:i|we)|what\s+time\s+should|how\s+(?:do|can|should)\s+(?:i|we)|"
    r"how\s+early|how\s+long\s+before|what\s+happens\s+if|do\s+(?:i|we)\s+need)\b", re.I)
DELAYED = re.compile(
    r"\b(?:delayed|delays?|running|on\s+time|disruption|disrupted)\b", re.I)
BOARD_ASK = re.compile(
    r"\b(?:next|last|first|when|what\s+time|how\s+soon|platform|departure\s+board|"
    r"station|stop|leaves?|departs?)\b", re.I)
FLIGHT_LIVE = re.compile(
    r"\b(?:next|last|first|running|on\s+time|delayed|cancelled|canceled|platform|leaves?|"
    r"departs?|replacement|engineering\s+works?)\b", re.I)
ASK = re.compile(
    r"^(?:when|what|how|is|are|was|were|has|have|did|does|do|can|could|will|would|any|next|"
    r"which)\b", re.I)
WHEN_ASK = re.compile(
    r"^\s*when\s+(?:is|are|was|were|does|do|did|will|would|should|can|could)\b", re.I)
NEWS = re.compile(
    r"\b(?:strike|strikes|striking|walkout|walk\s*out|industrial\s+action|union|ballot|"
    r"announcement|news)\b", re.I)
SERVICE = re.compile(
    r"\b(?:(?P<clock>[0-9]{1,2}(?::[0-9]{2})?\s*(?:o'?clock)?)\s+)?"
    r"(?:(?P<qual>next|night|last|first|early|late|morning|evening|midnight)\s+)?"
    r"(?P<vehicle>bus|train|tube|tram|coach|ferry|flight)\b"
    r"(?:\s+(?P<via>to|into|from)\s+"
    r"(?P<dest>[a-z][a-z'-]*(?:\s+[a-z][a-z'-]*){0,4}))?", re.I)


def _service_named(clean):
    match = SERVICE.search(clean)
    if not match:
        return None
    words = [part for part in (match.group("clock"), match.group("qual"),
                               match.group("vehicle")) if part]
    name = " ".join(words)
    if match.group("dest"):
        dest = re.split(r"\b(?:cancelled|canceled|delayed|running|tomorrow|today|tonight|"
                        r"please|leave|leaves|go|goes|departs?|arrives?)\b",
                        match.group("dest"))[0]
        dest = re.sub(r"(?:\s*\b(?:of|the|and|a|an|to|from|in|on|at|for|by)\b)+$", "",
                      dest.strip(), flags=re.I).strip()
        if dest:
            name += " " + match.group("via") + " " + dest
    return name


CLOCK = re.compile(
    r"\b\d{1,2}[:.]\d{2}\s*(?:am|pm)?\b|"
    r"\b\d{1,2}\s*(?:am|pm|o'?clock)\b|"
    r"\b(?:at|by|around|about|before|after|from|until|till)\s+\d{1,2}\b|"
    r"\b\d{1,2}\s+(?:tomorrow|today|tonight)\b|"
    r"\b(?:this\s+)?(?:morning|afternoon|evening|noon|midnight)\b", re.I)
VEHICLE_STEM = {"buses": "bus", "trains": "train", "trams": "tram", "coaches": "coach",
                "ferries": "ferry", "flights": "flight"}
def _their_own_time(clean, memory):
    if re.search(r"\b(?:next|last|first|night|early|late|platform|station|stop|running|on\s+time|"
                 r"delayed|cancelled|canceled|replacement)\b", clean):
        return False
    found = VEHICLE.search(clean)
    if not found:
        return False
    word = found.group(0).lower()
    stem = VEHICLE_STEM.get(word, word)
    try:
        turns = list(memory.get("turns") or ())
    except AttributeError:
        return False
    for turn in reversed(turns[-3:]):
        said = str(turn.get("user") or "").lower() if isinstance(turn, dict) else ""
        if re.search(r"\b" + re.escape(stem) + r"s?\b", said) and CLOCK.search(said):
            return True
    return False


def _clean(text):
    return " ".join(str(text or "").lower().split())


def respond(text, memory):
    clean = _clean(text)
    if not clean or not VEHICLE.search(clean) or not TIME.search(clean):
        return None
    if MONEY.search(clean) or NEWS.search(clean) or PLACE_OPENING.search(clean) or \
            ADVICE.search(clean) or _their_own_time(clean, memory):
        return None
    if DELAYED.search(clean) and not BOARD_ASK.search(clean):
        return None
    flight = re.search(r"\b(?:flight|flights|plane)\b", clean) or (
        re.search(r"\bairport\b", clean) and not VEHICLE.search(clean))
    if flight and not FLIGHT_LIVE.search(clean):
        return None
    if not ASK.search(clean) and not str(text or "").strip().endswith("?"):
        return None
    if not re.search(r"\bnext\b", clean) and not STATUS.search(clean) and \
            not PLATFORM.search(clean) and not re.search(r"\bwhat\s+time\b", clean) and \
            not WHEN_ASK.search(clean):
        return None
    service = _service_named(clean)
    lead = "For the " + service + ": " if service else ""
    found = SERVICE.search(clean)
    vehicle = found.group("vehicle").lower() if found else ""
    if re.search(r"\b(?:replacement|engineering\s+works?)\b", clean):
        return ("A replacement is the operator's own announcement: their app or site says where it "
                "leaves from and when, and the station's board carries it on the day.")
    if vehicle == "flight" or (not vehicle and re.search(r"\b(?:flight|flights|plane|airport)\b",
                                                         clean)):
        return lead + _the_wording(memory, FLIGHT)
    if vehicle == "ferry":
        return lead + _the_wording(memory, FERRY)
    if vehicle in ("train", "tube", "tram", "coach") or \
            re.search(r"\b(?:trains|trams|coaches)\b", clean):
        named = VEHICLE_STEM.get(vehicle, vehicle)
        if not named:
            found_plural = re.search(
                r"\b(?:" + "|".join(sorted(VEHICLE_STEM)) + r")\b", clean)
            named = VEHICLE_STEM.get(found_plural.group(0), found_plural.group(0)) \
                if found_plural else "train"
        return lead + _the_wording(memory, RAIL).format(
            vehicle=named, where=THE_BOARD_THAT_KEEPS_THEM.get(named, "the board at the station"))
    return lead + _the_wording(memory, BUS)


BUS = (
    "I can't see live bus times from here. The operator's app, or the timetable at the stop, has "
    "the next one; where the stop has a code, a text to it brings the times back. A journey "
    "planner puts the whole trip together.",
    "The next one is live, so nothing here can see it. The bus operator's app, or the timetable "
    "printed at the stop, has the time - text the stop's code where it has one - and a journey "
    "planner joins the trip up.",
)
THE_BOARD_THAT_KEEPS_THEM = {
    "train": "the board at the station",
    "tube": "the board on the platform",
    "tram": "the board at the stop",
    "coach": "the board at the coach station",
}
RAIL = (
    "I can't see live {vehicle} times from here. The operator's app, or {where}, has "
    "the next one and any delay or cancellation; a journey planner puts the whole trip together.",
    "That one is a live departure, so the operator's app, or {where}, is where the "
    "next one and any delay or cancellation show up. A journey planner puts the whole trip together.",
)
TRAIN = tuple(text.format(vehicle="train", where="the board at the station") for text in RAIL)
FLIGHT = (
    "I can't see live flights from here. The airline's app, or the airport's own departures board, "
    "has the gate and any delay; the booking reference brings it up.",
    "The gate and any delay are live, and I can't see them from here. The airline's app, or the "
    "airport's own departures board, has them, and the booking reference brings the booking up.",
)
FERRY = (
    "I can't see live ferry times from here. The operator's app, or the port's own departure board, "
    "has the next sailing and any delay; a journey planner puts the whole crossing together.",
    "That sailing is a live one, and I can't see it from here. The ferry operator's app, or the "
    "board at the port, has the next one and any delay; a journey planner joins the crossing up.",
)


def _the_wording(memory, wordings):
    try:
        turns = memory.get("turns") or ()
    except AttributeError:
        turns = ()
    return wordings[len(turns) % len(wordings)]


def TAKES_AS_IT_COMES(text, memory=None):
    return respond(text, memory) is not None
