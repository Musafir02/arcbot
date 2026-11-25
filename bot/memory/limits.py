import re

from ..compose import pick

_PERSON = (
    r"(?:i|we|my \w+|mum|mom|mother|dad|father|nan|nana|gran|granny|grandma|grandad|grandpa|"
    r"partner|husband|wife|oh|other half|daughter|son|sister|brother|aunt|uncle|cousin|"
    r"friend|mil|fil|she|he|they|her|his|their)"
)
_CANNOT = (
    r"(?:can'?t|cannot|can not|isnt able to|isn'?t able to|not able to|dont|doesn'?t|"
    r"do not|does not|struggles? (?:to|with)|struggling (?:to|with)|finds? it hard to|"
    r"find it hard to|has trouble|have trouble|bad (?:on|at|with))"
)
_WALK = (
    r"(?:walk(?:ing)? (?:far|much|long distances|very far|any distance)|"
    r"manage (?:the )?stairs|do (?:the )?stairs|climb (?:the )?stairs|stairs|"
    r"stand (?:for long|up for long|for very long|about for long|for more than \w+ minutes?)|"
    r"get (?:about|around) (?:much|easily|well)|"
    r"(?:walk|move) (?:as )?(?:well|easily) as (?:she|he|they) used to)"
)
_LIMIT_VERB = re.compile(
    r"\b" + _PERSON + r"\s+" + _CANNOT + r"\s+(?:really |even |anymore |any more )?" + _WALK +
    r"\b", re.I)
_AID = re.compile(
    r"\b(?:uses?|using|needs?|has|got|with|on|in)\s+(?:a |an |his |her |their |my )?"
    r"(?:wheelchair|mobility scooter|scooter|walking stick|stick|walking frame|zimmer|"
    r"rollator|walking aid|walker|crutches)\b", re.I)
_IN_A_CHAIR = re.compile(
    r"\b(?:is in|are in|in|into) a wheelchair\b|\bwheelchair[- ]?(?:user|bound)\b"
    r"|\bon crutches\b|cant walk at all|can'?t walk at all|non[- ]?weight ?bearing\b", re.I)
_FLAT = re.compile(
    r"\bsomewhere flat\b|\bflat(?:ter)? (?:ground|walk|walking|paths?|route|town|city|seafront|"
    r"promenade|terrain|streets?)\b|\bneed(?:s)? (?:it|somewhere|the ground) flat\b"
    r"|\bkeep (?:it|to) (?:the )?flat\b", re.I)
_NO_WALKS = re.compile(
    r"\b(?:no|nothing|not|never|nowt)\s+"
    r"(?:(?:that\s+)?(?:needs?|involves?|involving|means|with)\s+)?"
    r"(?:too\s+|very\s+|much\s+|any\s+|more\s+)*"
    r"(?:long\s+|proper\s+|big\s+|far\s+|steep\s+|many\s+)?(?:walks?|walking|hikes?|hiking|"
    r"hills?|stairs|steps|climbing)\b", re.I)
_RULE_LEAD = re.compile(
    r"^(?:(?:and|so|but|then|also|oh|plus|ok|okay|well|just|actually|honestly|now|right)\b[^a-z]*)*",
    re.I)
_RULE_TAIL = re.compile(
    r"^[\s,.;:!-]*(?:(?:please|thanks|ta|then|either|though|too|really|honestly|sadly|unfortunately|today|"
    r"tomorrow|tonight|now|though|any ?more|at all|this time|for (?:me|us)|on (?:this|the) trip|"
    r"i think|i suppose)\b[^a-z]*)*$", re.I)
_STAIRS_SAID = re.compile(r"\b(?:stairs|steps|climbing)\b", re.I)
_REFUSES_AID = re.compile(
    r"\b(?:wont|won'?t|will not|would not|refuses?|refused|refusing|hates?|hated|"
    r"doesn'?t want|dont want|does not want|do not want)\b[^.]{0,25}\b(?:stick|frame|zimmer|"
    r"rollator|walker|wheelchair|scooter|aid|rail|handle|crutch(?:es)?)\b", re.I)
_DISLIKES_THE_WALK = re.compile(
    r"\b(?:hates?|hated|dislikes?|can'?t stand|cannot stand|cant stand|doesn'?t like|don'?t like|"
    r"do not like|isn'?t keen on|not keen on|would rather not|prefers? not to)" + r"\b[^.]{0,24}"
    r"\b(?:walk(?:ing)?|hikes?|hiking|rambl(?:e|ing)|hills?|steps?|stairs)\b"
    r"|\brather sit\b|\bsit in a pub\b", re.I)
_PUSHCHAIR = re.compile(
    r"\b(?:pushchair|pram|buggy|stroller|car ?seat|carrycot|cot|highchair)\b", re.I)
_FLAT_IS_A_HOME = re.compile(
    r"\b(?:to live|to rent|to buy|to move to|a flat|flat to|ground floor flat|bungalow)\b", re.I)

_ILLNESS = re.compile(
    r"\b(?:pain|painful|hurts?|hurting|swollen|swelling|fell|fallen|fall|falls|dizzy|numb|weak|"
    r"unwell|ill|poorly|blood|bleed|bleeding|bruise|broken|fracture|sore|stiff|"
    r"doctor|gp|nurse|hospital|a&e|ambulance|111|999|since (?:her|his|the)|getting worse|"
    r"arthritis|dementia|alzheimers|parkinsons|ms|stroke|surgery|operation|replacement|"
    r"physio|physiotherapy|chemo|cancer|diagnosis|tablets?|medication|prescribed)\b", re.I)
_PET = re.compile(
    r"\b(?:dog|dogs|puppy|pup|cat|cats|kitten|pet|pets|rabbit|hamster|guinea|horse|pony|"
    r"ferret|parrot)\b", re.I)
_ASKS = re.compile(
    r"^\s*(?:what|where|when|why|how|which|who|can|could|do|does|did|is|are|was|were|will|"
    r"would|should|shall|any|anyone|anybody)\b", re.I)

_A_TRIP = re.compile(
    r"\b(?:trip|trips|holiday|holidays|city break|weekend|days? away|nights? away|day out|days out|"
    r"flight|flights|flying|abroad|visit(?:ing)?|sightsee\w*|tour(?:ing)?|museums?|galleries|"
    r"castles?|cathedral|hotels?|somewhere to stay|what should we see|where should we go|"
    r"things to do|days in|nights in|weeks in|a week|a few days|\d+ (?:days|nights)|"
    r"taking \w+(?: \w+)? (?:to|off)|off to|going to|booked|booking|somewhere to stay|"
    r"seaside|beach|coast|countryside|shopping|old town|town cent(?:re|er))\b", re.I)


def _the_trip_is_on(clean, memory):
    if _A_TRIP.search(clean):
        return True
    if _FLAT.search(clean) and not _FLAT_IS_A_HOME.search(clean):
        return True
    known = (memory or {}).get("user") if isinstance(memory, dict) else None
    if isinstance(known, dict):
        if [place for place in (known.get("places") or []) if str(place).strip()]:
            return True
        if _A_TRIP.search(str(known.get("plan") or "")):
            return True
    for turn in _turns(memory)[-4:]:
        if isinstance(turn, dict) and _A_TRIP.search(str(turn.get("user") or "")):
            return True
    return False


WALK_REPLIES = (
    "Then plan for benches. One big thing a morning, a sit-down after it, and a taxi or a bus for "
    "the long hops - two sights close together beats four across town.",
    "Good to know. Keep the days short and stop before the legs give out rather than after, and "
    "check the step-free way into the one place you most want to see.",
    "That shapes the trip more than the sights do: one thing a day, short walks between, and no "
    "shame in a taxi for the last stretch.",
    "Then build the day around a sit-down every hour or so, and pick your two must-sees rather "
    "than a list. Most museums have a step-free entrance if you ask before you go.",
    "Fair enough - short hops, a stop for a coffee in the middle, and somewhere to sit at the end. "
    "That is a better trip than a marathon of churches anyway.",
)
STAIRS_REPLIES = (
    "Ask about lifts and step-free entrances before you book anything: most big places have them, "
    "and it is usually not the front door.",
    "Then ring ahead for the ones you care about - a lift to the good floors and a loo you can get "
    "to are the two questions worth asking.",
    "Old towns are the hard part, so keep to the flatter streets and take the bus between the bits "
    "at the top of the hill.",
)
CHAIR_REPLIES = (
    "Then ask about the step-free entrance for each place before you go - most big museums have "
    "one. Cobbles and the oldest streets are the thing to plan around.",
    "Ring ahead for the ones that matter: step-free entry, a lift to the good floors, and an "
    "accessible loo. Most places will tell you straight if you ask.",
    "Plan around the ground rather than the sights: smooth pavements, a bus or a taxi between "
    "stops, and one thing a day is plenty.",
)


def _kind(clean):
    if _IN_A_CHAIR.search(clean):
        return "chair"
    if _AID.search(clean):
        aid = _AID.search(clean).group(0).lower()
        if "wheelchair" in aid or "scooter" in aid:
            return "chair"
        return "walk"
    if _LIMIT_VERB.search(clean):
        said = _LIMIT_VERB.search(clean).group(0).lower()
        if "stairs" in said:
            return "stairs"
        return "walk"
    if _DISLIKES_THE_WALK.search(clean):
        return "walk"
    if _FLAT.search(clean):
        return "walk"
    lead = _RULE_LEAD.match(clean)
    rule = _NO_WALKS.match(clean, lead.end() if lead else 0)
    if rule and _RULE_TAIL.match(clean[rule.end():]):
        return "stairs" if _STAIRS_SAID.search(rule.group(0)) else "walk"
    return None


def names_a_limit(text):
    return _kind(" ".join(str(text or "").replace("\u2019", "'").split()))


def reply(text, memory):
    clean = " ".join(str(text or "").replace("\u2019", "'").split())
    if not clean or len(clean.split()) > 18:
        return None
    if (_PET.search(clean) or _ILLNESS.search(clean) or _REFUSES_AID.search(clean)
            or _PUSHCHAIR.search(clean)):
        return None
    kind = _kind(clean)
    if not kind:
        return None
    if clean.rstrip().endswith("?") or _ASKS.match(clean):
        return None
    if not _the_trip_is_on(clean, memory):
        return None
    kept = {"kind": kind, "text": clean, "turn": len(_turns(memory))}
    if isinstance(memory, dict):
        limits = memory.get("limits")
        if not isinstance(limits, list):
            limits = []
        limits.append(kept)
        memory["limits"] = limits[-6:]
    pool = {"walk": WALK_REPLIES, "stairs": STAIRS_REPLIES, "chair": CHAIR_REPLIES}[kind]
    return pick(pool, memory, seed_text=str(text or ""))


def _turns(memory):
    turns = (memory or {}).get("turns") if isinstance(memory, dict) else None
    return turns if isinstance(turns, list) else []


def said(memory):
    limits = (memory or {}).get("limits") if isinstance(memory, dict) else None
    if isinstance(limits, list) and limits:
        last = limits[-1]
        if isinstance(last, dict):
            return last
    return None
