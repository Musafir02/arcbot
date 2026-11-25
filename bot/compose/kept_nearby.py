import re

from .fallback_data import THE_PLACE_ASK, UNKNOWN, the_place_the_answer_is_kept

PLAIN_HEADS = tuple(line[:40] for line in UNKNOWN)

LEANING = re.compile(
    r"^(?:(?:and|also|so|but|ok|okay|then|plus)\b"
    r"|\W*(?:what|how|where|when|who|which|is|are|do|does|can|could|should|shall|will|would|"
    r"have|has|did)\b)", re.I)

SHORT = 11

ASKING = frozenset("""
a an the and or but so then if is are was were be been being am do does did done have has had
i you we they he she it me us them him her my your our their its this that these those there
what which who whom whose where when why how whether
can could would should shall will may might must need needs needed
one ones each both either any some all more most much many few less least other else also too
still just only again ever never not no yes ok okay please thanks
long far often soon old big heavy quick fast early late near
to of in on at for from with about into over under up down out off back by as than
itn t ll re ve don doesnt didnt isnt arent wasnt wont cant couldnt shouldnt wouldnt
get gets got give gives gave put puts take takes keep keeps save saves share shares use uses
buy buys pay pays book books order orders renew renews change changes try tries go goes come
comes help helps tell tells say says ask asks know knows work works start starts stop stops
do make makes fix fixes clean cleans wash washes cut cuts add adds pour pours boil boils
cook cooks freeze freezes store stores wear wears eat eats drink drinks run runs walk walks
wait waits ring rings call calls check checks send sends bring brings
anything something everything nothing anyone someone anyone nobody none somewhere anywhere
elsewhere whichever whatever whenever however lot lots bit bits piece pieces way ways
""".split())

A_METHOD = re.compile(
    r"^\W*(?:how\s+(?:do|can|could|should|would|shall)\s+(?:i|you|we)\b|how\s+to\b"
    r"|(?:what|whats|what'?s)\s+the\s+(?:best|easiest|quickest|right)\s+way\b"
    r"|the\s+(?:best|easiest|quickest|right)\s+way\s+to\b)", re.I)

BAGGAGE = re.compile(
    r"\b(?:baggage|luggage|hand luggage|cabin bag|carry[- ]on|hold bag|checked bag|holdall"
    r"|suitcase|allowance|weight limit|kilos?|kilograms?|oversize|oversized|extra bag"
    r"|bag drop|legroom)\b", re.I)
BAGGAGE_POOL = (
    "That is your airline's rather than mine, sorry - the allowance is set by the fare, so two "
    "people on the same plane can have different ones. Your booking's own page shows the kilos "
    "you have paid for, and adding a bag before the airport is always the cheaper way. Tell me "
    "what it says and I'll help you pack to it.",
    "The airline sets that and the fare decides it, sorry, so it is your booking that answers it: "
    "open it and look for the baggage line rather than the airline's general page. Bring me the "
    "figure and I'll help you fit everything in.",
    "I can't call that one - it belongs to the ticket rather than to the plane, sorry. Your "
    "booking shows what you have paid for and the desk weighs it to the kilo; tell me the number "
    "and I'll help you sort the rest.",
)


def _turns(memory):
    return [t for t in (memory or {}).get("turns") or [] if isinstance(t, dict)]


def _clean(text):
    return " ".join(str(text or "").lower().split())


def _without_plurals(line):
    words = []
    for word in line.split():
        if len(word) > 3 and word.endswith("s") and not word.endswith(("ss", "us", "is")):
            words.append(word[:-1])
        else:
            words.append(word)
    return " ".join(words)


def is_the_plain_hedge(said):
    return str(said or "")[:40] in PLAIN_HEADS


def _inheritable(pool):
    return not any("council" in line.lower() for line in pool)


def _the_kind(line, borrowable=False):
    for said in (line, _without_plurals(line)):
        pool = the_place_the_answer_is_kept(said)
        if pool:
            if borrowable and not _inheritable(pool):
                continue
            return pool
        if BAGGAGE.search(said):
            return BAGGAGE_POOL
    return None


def answer_for(text, memory=None):
    line = _clean(text)
    if not line:
        return None
    if the_place_the_answer_is_kept(line):
        return None
    if BAGGAGE.search(line):
        return BAGGAGE_POOL
    if not LEANING.search(line):
        return None
    if A_METHOD.search(line):
        return None
    said = [w for w in re.split(r"[^a-z']+", line) if w]
    if len(said) > SHORT:
        return None
    if any(word not in ASKING for word in said):
        return None
    turns = _turns(memory)
    if not turns:
        return None
    near = [turns[-1].get("user")]
    if len(turns) > 1 and LEANING.search(_clean(turns[-1].get("user"))):
        near.append(turns[-2].get("user"))
    for said in near:
        said = _clean(said)
        if not said or said == line:
            continue
        pool = _the_kind(said, borrowable=True)
        if pool:
            return pool
    return None
