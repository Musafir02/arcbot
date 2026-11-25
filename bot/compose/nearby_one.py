import re

THE_PRONOUN_ASK = re.compile(
    r"(?<![a-z])(?:is|are)\s+there\s+(?:one|any)\s+"
    r"(?:near(?:\s+(?:me|here|us))?|nearby|close\s+by|close\s+to\s+(?:me|us|here)"
    r"|round\s+here|around\s+here|in\s+(?:my|the|our)\s+(?:area|town|village|end|city))\b"
    r"|(?<![a-z])(?:is|are)\s+there\s+(?:one|any)\s+(?:close\s+by|nearby)\b"
    r"|(?<![a-z])where(?:'s|\s+is)\s+the\s+(?:nearest|closest)\s+one\b"
    r"|(?<![a-z])(?:where|how)\s+(?:can|do|would|should)\s+i\s+(?:find|get|locate)\s+(?:one|any)\b"
    r"|(?<![a-z])(?:can|could|will)\s+you\s+(?:find|point\s+me\s+to|tell\s+me\s+where\s+to\s+find)"
    r"\s+(?:one|any)\b",
    re.I)

THE_FRAME = re.compile(
    r"(?<![a-z])(?:"
    r"i\s*(?:'m|m)?\s*(?:looking\s+for|after|in\s+need\s+of|trying\s+to\s+find)"
    r"|i\s+(?:really\s+)?(?:need|want|would\s+like|am\s+after)"
    r"|i\s+could\s+(?:really\s+)?(?:do\s+with|use|find)"
    r"|(?:im|i\s+am)\s+(?:desperate|dying)\s+for"
    r"|looking\s+for"
    r"|(?:where|how)\s+(?:can|do|would)\s+i\s+(?:get|find|buy|locate)"
    r"|(?:is|are)\s+there\s+(?:a|an|any)"
    r"|(?:can|could)\s+you\s+(?:find|recommend|point\s+me\s+to)"
    r"|ive\s+been\s+(?:trying\s+to\s+find|looking\s+for|desperate\s+for)"
    r"|(?:do\s+you\s+know\s+(?:where|of)\s+(?:a|an|any)?)"
    r"|(?:any\s+idea|any\s+suggestions?)\s+(?:where|of|for)\s+"
    r"(?:i\s+(?:can|could|might)\s+(?:find|get|buy))?"
    r")",
    re.I)
THE_END = frozenset("""
for from that which who whom to in on at into onto with without near nearest nearby around round
about before after because but and or so as if when while during since until by through over under
between among per via than then there here this these those some any all my your our their his her
its it me us them him week weekend today tomorrow tonight morning afternoon evening night time
month year day hour minute minute please thanks thank soon asap now later
""".split())
THE_ARTICLE = frozenset("a an the some another any other one two three couple few".split())
THE_ADJECTIVE = frozenset("""
good nice decent cheap local proper reliable great best better closest nearest nearby quick
half-decent real actual special favourite favorite little big small large new old open
""".split())
A_VERB = frozenset("""
get stop be boil cover drink eat give go keep leave learn move order register reinstall remember
service shower sleep switch change use wake water cry open buy find start try make save spend
sort fix call book check
""".split())
NOT_A_THING = frozenset("""
midwifery series batteries battery account card induction session job clothes course degree
""".split()) | frozenset("""
one any it thing something anything anyone someone everything nothing
lonely tired exhausted sad happy angry upset worried anxious stressed ill sick unwell better worse
ok okay fine well hungry thirsty bored cold hot warm busy free awake asleep asleep dead alive
working broken fixed sorted ready done finished lost stuck late early right wrong sure certain
true false real possible likely easy hard difficult cheap expensive worth allowed legal illegal
allowed normal strange weird fair unfair safe dangerous
good bad great nice best worst better worse
somewhere anywhere nowhere everywhere someplace anyplace
""".split())

NEARBY_ONE_POOL = (
    "Nothing here knows what is around you, sorry - no map, no local list. A map app search for "
    "{thing} near you is the quickest way to one, and the reviews on the listing beat anything I "
    "could recall about a place I have never been.",
    "I can't see your area, sorry. Put \"{thing}\" and your town into a map app and it shows what "
    "is close, with the opening hours and the distance; the place's own page or a phone call "
    "settles anything else about it.",
)
NOT_A_PLACE = frozenset("""
chance news way idea reason point need risk history proof difference problem question law rule
lift taxi bus train tram coach tube flight ferry delivery parcel refund appointment cure treatment
vaccine price cost quote answer opinion view
list colour color salary wage pay jewellery jewelry trousers pants jeans shoes shirt coat
""".split())

PLACE_HEADS = frozenset("""
store stores station stations stop stops office offices garage garages bank banks centre center
market yard park pool hall hotel cafe pub clinic surgery pharmacy chemist hospital library
supermarket launderette launderettes laundrette tip depot studio salon agency firm company gym
takeaway barber hairdresser optician
""".split())
A_CHORE = frozenset("shop shops store stores market markets".split())
A_TRADE = frozenset("""
plumber electrician decorator plasterer roofer builder joiner carpenter painter gardener cleaner
locksmith glazier tiler bricklayer mechanic groomer vet dentist doctor nurse optician physio
physiotherapist chiropodist podiatrist therapist counsellor psychotherapist solicitor barrister
accountant surveyor architect tutor instructor tuner cutter tailor barber hairdresser chef
caterer photographer director midwife osteopath acupuncturist notary
""".split())
PLACE_TAILS = ("ette", "ettes", "ery", "ary", "eum", "eums")
PLACE_STEMS = ("shop", "store", "market", "station", "garage", "cafe", "park", "hall", "bank",
               "pool", "clinic", "centre", "center", "chemist", "pub", "hotel", "studio", "salon",
               "agency", "firm", "gym", "kiosk", "stall", "chippy", "chippie", "deli", "caff",
               "diner", "grill", "bistro", "launderette", "laundrette", "hospital", "surgery")
CASH_POINT = frozenset(("cash point", "cash points", "cashpoint", "cashpoints", "cash machine",
                        "cash machines", "atm", "atms"))
NEAR_ME_PAIR = frozenset(("post box", "postbox", "pillar box", "phone box", "bottle bank",
                          "recycling point", "public toilet", "public toilets", "litter bin",
                          "lost property office", "petrol station", "bus stop", "taxi rank"))


def _the_thing(line):
    found = THE_FRAME.search(line)
    if not found:
        return ""
    words = line[found.end():].split()
    if words and words[0].strip(".,!?;:'\"()").lower() == "to":
        return ""
    kept = []
    for word in words:
        bare = word.strip(".,!?;:'\"()").lower()
        if not bare:
            continue
        if bare in THE_END or bare in THE_ARTICLE:
            if kept:
                break
            continue
        if bare in THE_ADJECTIVE and not kept:
            continue
        if not re.match(r"^[a-z][a-z'&-]*$", bare):
            break
        kept.append(bare)
        if len(kept) == 3:
            break
    if not kept:
        return ""
    if kept[0] in NOT_A_THING or " ".join(kept) in NOT_A_THING:
        return ""
    if kept[0] in A_VERB:
        return ""
    if " ".join(kept) in CASH_POINT or " ".join(kept) in NEAR_ME_PAIR:
        return " ".join(kept)
    if set(kept) & NOT_A_PLACE:
        return ""
    if set(kept) & NOT_A_THING:
        return ""
    if not _a_place(kept):
        return ""
    return " ".join(kept)


def _a_place(kept):
    last = kept[-1]
    if len(kept) == 1 and last in A_CHORE:
        return False
    if last in PLACE_HEADS or last in A_TRADE:
        return True
    if last.endswith(PLACE_STEMS) or last.endswith(PLACE_TAILS):
        return True
    return False


def _the_thread_thing(memory, cleaned):
    turns = (memory or {}).get("turns") or []
    seen = 0
    for turn in reversed(turns):
        if not isinstance(turn, dict):
            continue
        said = (turn.get("user") or "").strip().lower()
        if not said or said == cleaned or THE_PRONOUN_ASK.search(said):
            continue
        seen += 1
        if seen > 4:
            break
        if not THE_FRAME.search(said):
            continue
        return _the_thing(said)
    return ""


def _pick(pool, line):
    if not pool:
        return ""
    return pool[sum(ord(letter) for letter in line) % len(pool)]


def reply_for(line, memory=None):
    if not line:
        return None
    cleaned = " ".join(line.lower().split())
    if not THE_PRONOUN_ASK.search(cleaned):
        return None
    thing = _the_thread_thing(memory, cleaned)
    if not thing:
        return None
    return _pick(NEARBY_ONE_POOL, cleaned).format(thing=thing)
