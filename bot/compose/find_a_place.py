import re

from . import fallback_data, finding_out, pick

WHERE_TO_GET = re.compile(
    r"\bwhere (?:can|could|do|would|should|might) (?:i|we) (?:get|buy|find|hire|pick up|source)\b"
    r"|\bwhere(?:'s| is| are)? (?:the )?(?:best|nearest|closest)\b"
    r"|\bwhere (?:can|could) (?:i|we) (?:get|find) (?:somebody|someone)\b"
    r"|\bwho (?:does|sells|fixes|repairs|makes|can) (?:this|that|it|them)?\b")
THERE_IS = re.compile(
    r"\b(?:is|are) there (?:a|an|any|anywhere|somewhere|any good|any decent|a good|a decent)\b"
    r"|\bany (?:good|decent|half decent|nice)\b"
    r"|\banywhere (?:i can|that|round here|near|to get|to buy)\b")
NEARBY = re.compile(
    r"\b(?:near me|near here|near us|nearby|round here|around here|round the corner|close by|"
    r"locally|in the area|in town|near york|near my|nearest)\b")
A_RECOMMEND = re.compile(
    r"\b(?:can|could|would) (?:you|anybody|anyone) (?:recommend|suggest)\b"
    r"|\b(?:do|did) you know (?:a|an|any|anyone|anybody|someone|somebody|of a|of any)\b"
    r"|\bknow (?:a|an|any) (?:good|decent|reliable|half decent|trustworthy)\b"
    r"|\banyone know (?:a|an|any)\b"
    r"|\bwho (?:would|could) you (?:recommend|suggest)\b"
    r"|\b(?:recommend|recommendation|recommendations) (?:for|of) (?:a|an|someone|somebody)\b")
A_ASKING_MY_OPINION = re.compile(
    r"\b(?:recommend|suggest) (?:i|we|me|that i|that we)\b"
    r"|\bwould you (?:recommend|suggest) (?:seeing|going|trying|taking|using|booking|getting)\b")
A_NAME_FOR_SOMEBODY = re.compile(
    r"\b(?:plumber|electrician|builder|joiner|carpenter|roofer|roofing|gardener|landscaper|"
    r"decorator|painter|mechanic|garage|locksmith|glazier|chimney sweep|pest control|removals|"
    r"handyman|odd job|surveyor|architect|cleaner|window cleaner|solicitor|lawyer|conveyancer|"
    r"accountant|bookkeeper|dentist|orthodontist|hygienist|hairdresser|barber|vet|optician|"
    r"physio|physiotherapist|osteopath|chiropractor|chiropodist|podiatrist|tutor|childminder|"
    r"dog walker|dog groomer|nanny|carer|interpreter|translator|tailor|seamstress|upholsterer|"
    r"tiler|plasterer|drainage|gas engineer|boiler engineer|heating engineer)\b")
HOURS = re.compile(
    r"\bopen\b|\bopening\b|\bclosed\b|\bshut\b|\blate\b|\bsunday\b|\bsaturday\b|\btonight\b|"
    r"\bnow\b|\btoday\b|\bbank holiday\b|\bweekend\b|24 hour|24-hour")
SOMEBODY = re.compile(r"\b(?:someone|somebody|a man|a person|anyone|who can|who could)\b")
A_TRADE = re.compile(
    r"\b(?:plumber|electrician|builder|joiner|carpenter|roofer|roofing|gardener|landscaper|"
    r"decorator|painter|mechanic|garage|locksmith|glazier|chimney sweep|pest control|"
    r"removals|man with a van|gas engineer|boiler engineer|heating engineer|tiler|plasterer|"
    r"drainage|drain man|odd job|handyman|surveyor|architect|cleaner|window cleaner)\b")
A_JOB_ON_A_THING = re.compile(
    r"\b(?:fix|fixes|fixed|repair|repairs|repaired|mend|mends|mended|service|services|serviced|"
    r"install|installs|installed|fit|fits|fitted|replace|replaces|replaced|unblock|unblocks|"
    r"unblocked|bleed|bleeds|bleeding|rewire|plaster|tile|decorate|assemble|"
    r"put up|take down|cut back|trim|fell|haul|clear out|check over|mot|valet)\b")
A_LEAD = re.compile(r"^(?:a|an|the|some|any|my|our|his|her|their)\s+")
A_TAIL = re.compile(
    r"\s+(?:from|from a|near me|near here|nearby|round here|around here|round the corner|"
    r"close by|locally|in the area|in town|please|then|today|now|cheaply|cheap|asap|"
    r"at all|if possible)$")
NO_THING = frozenset((
    "it", "its", "it's", "one", "ones", "them", "that", "this", "those", "these", "the part",
    "the bit", "the thing", "the other one", "the right one", "the same one", "a new one",
    "the rest", "some", "more", "the stuff", "stuff", "something", "anything", "part", "bit",
    "piece", "number", "spare", "the spare", "new one", "the new one", "a replacement",
))
NOT_A_PLACE = re.compile(
    r"\b(?:setting|settings|option|menu|button|box|tick|toggle|app|website|web ?site|site|"
    r"internet|online|account|profile|password|page|link|file|folder|form|email|e-mail|"
    r"number|answer|word|phrase|name of|symbol|icon|tab|code|pin|receipt|invoice|statement|"
    r"advice|help|support|information|info|idea|ideas|inspiration|motivation|energy|time|"
    r"money|cash|courage|willpower|confidence|strength|protein|fibre|fiber|iron|calcium|"
    r"vitamin|vitamins|carbs|calories|fat|nutrient|nutrients|hydration|sleep|"
    r"results|result|prescription|referral|appointment|test|tests|tested|screening|screened|"
    r"vaccinated|jab|jabbed|vaccine|vaccination|voucher|gift card|"
    r"refund|compensation|complaint|report|permission|licence|license|visa|change|connection|"
    r"platform|route|directions|ticket|bus|buses|train|trains|tube|taxi|tram|coach|get off|"
    r"get on|get out|stop)\b")
BARE_ANY = re.compile(r"^(?:any|anywhere|somewhere)\b")
ANY_ABSTRACT = re.compile(
    r"\b(?:advice|help|news|luck|update|updates|chance|word|ideas?|points?|sign|signs|"
    r"problems?|trouble|issues?|questions?|objection|preference|reasons?|differences?|"
    r"changes?|time|space|room|evidence|proof|complaints?|feedback|progress|"
    r"better|worse|easier|harder|nicer|cheaper|different|new|same|"
    r"news|warning|warnings)\b")
CASH_MACHINE = re.compile(
    r"\b(?:cash machine|cash point|cashpoint|cashline|cash dispenser|atm|hole in the wall)\b")
ALREADY_A_PLAN = re.compile(
    r"\b(?:i'll|i will|im going|i'm going|we're going|were going|the council already)\b")


A_NOD = frozenset(fallback_data.NEUTRAL + fallback_data.A_SMALL_DAY)


ALREADY_A_ROUTE = re.compile(
    r"\b(?:own finder|own register|official (?:finder|register|list)|profession'?s own|"
    r"professional body|trade body|lists? them by area|find a (?:solicitor|lawyer|vet|dentist|"
    r"physio|accountant|plumber|electrician)|taking new (?:people|patients|clients))\b",
    re.I)
A_HAD_IT = re.compile(r"\b(?:has|have|had|who'?s|whos|that'?s|whose)\s+(?:also\s+)?had\b")
A_THING_TO_HELP_WITH = re.compile(
    r"\b(?:van|trailer|ladder|ladders|generator|marquee|tables? and chairs|chairs|"
    r"skip|pressure washer|trolley)\b")


ROUTE_POOLS = tuple(getattr(finding_out, name) for name in
                    ("BUY_POOL", "TRADE_POOL", "PROFESSIONAL_POOL", "PLACE_ROUTE_POOL")
                    if hasattr(finding_out, name))
_ROUTE_HEADS = frozenset(line.split("{")[0].strip()[:34] for pool in ROUTE_POOLS
                         for line in pool)


def already_a_route(reply):
    said = str(reply or "")
    if ALREADY_A_ROUTE.search(said):
        return True
    return any(head and said.startswith(head) for head in _ROUTE_HEADS)


def _clean(text):
    return " ".join(str(text or "").lower().replace("\u2019", "'").split()).strip(" ?.!,")


def _a_thing(thing):
    thing = str(thing or "").strip()
    while True:
        trimmed = A_TAIL.sub("", thing).strip()
        if trimmed == thing:
            break
        thing = trimmed
    if not thing or thing in NO_THING or len(thing.split()) > 4:
        return None
    return thing


def _the_thing(clean):
    found = re.search(r"\b(?:that|which|who) (?:does|sells|fixes|repairs|makes|keeps|stocks)\s+"
                      r"([a-z][a-z' ]{1,28})$", clean)
    if found:
        return _a_thing(found.group(1))
    found = re.search(
        r"\b(?:get|buy|find|hire|pick up|source)\s+(?:hold of\s+)?(?:a|an|the|some|any|my|our)?\s*"
        r"([a-z][a-z' ]{1,28}?)(?:\s+(?:from|near|round|around|close|locally|in|please|then|"
        r"today|now|cheaply|cheap|asap)$|\s*$)", clean)
    if found:
        return _a_thing(A_LEAD.sub("", found.group(1).strip()))
    found = re.match(r"(?:any|some)\s+([a-z][a-z' ]{1,28}?)(?:\s+(?:near|round|around|open|"
                     r"in|that|to|please|today|now|locally)\b|$)", clean)
    if found:
        return _a_thing(A_LEAD.sub("", found.group(1).strip()))
    found = re.search(r"\b(?:nearest|closest)\s+([a-z][a-z' ]{1,28}?)(?:\s+(?:near|to|for|in|"
                      r"that|please|today|now|open)\b|$)", clean)
    if found:
        thing = _a_thing(A_LEAD.sub("", found.group(1).strip()))
        if thing and thing not in ("place", "one", "spot"):
            return thing
    found = re.search(r"\b(?:is|are) there (?:a|an|any|somewhere|anywhere|any good|a decent)"
                      r"\s+([a-z][a-z' ]{1,28}?)(?:\s+(?:near|round|around|close|open|"
                      r"locally|in|that|to)\b|$)", clean)
    if found:
        return _a_thing(A_LEAD.sub("", found.group(1).strip()))
    return None


NO_MAP = (
    "No map on this side, so I can't see what's near you. \"{thing} near me\" in a map app lists "
    "the closest with their hours, and the branch's own page says whether they keep it.",
    "I can't see what's near you, so a pick from me would be a guess. Put \"{thing}\" into "
    "a map app with your town in the search, then ring before you go if it's a bus ride away.",
    "There's no list of places here. A map app search for \"{thing}\" and your town shows "
    "the nearest ones and what time they shut, which is the part I can't tell you.",
)
NO_MAP_UNNAMED = (
    "No map on this side, so I can't point you at anywhere near you. A map app with the name of "
    "the thing and your town is the quickest way, and a phone call settles whether they keep it.",
    "I can't see what's near you, so any shop I named would be a guess. Search it in a map app "
    "with your town added, and ring first: that saves the trip if they haven't got it.",
)
A_HAND = (
    "I can't recommend anyone - I've no way to see who's near you or how their work turns out. "
    "Two neighbours who've had the same job done is the best source for a name, then check it on "
    "the trade's register (Gas Safe for anything gas) before you book.",
    "Nobody I can name for that, and I won't guess with somebody's livelihood. Ask on a local "
    "group or two neighbours, check the name on the trade body's list, and get the price in "
    "writing before they start.",
)
THE_HOURS = (
    "No live opening times here. A map app will show today's hours for the ones near you, and for "
    "a pharmacy the NHS pharmacy finder lists which are open.",
    "I can't see what's open near you today. A map app with \"open now\" in the search is the "
    "quick way, and the branch's own page is the one that's kept right.",
)


def _a_person_for_the_job(clean):
    if SOMEBODY.search(clean) or A_TRADE.search(clean):
        return True
    return bool(A_JOB_ON_A_THING.search(clean) and re.search(r"\b(?:my|our|the)\b", clean))


def answer_for(text, memory):
    clean = _clean(text)
    if not clean:
        return None
    words = clean.split()
    if len(words) < 3 or len(words) > 16:
        return None
    bare_any = bool(BARE_ANY.match(clean))
    for_the_place_test = CASH_MACHINE.sub("cash_machine", clean)
    if bare_any and not THERE_IS.search(clean) and ANY_ABSTRACT.search(for_the_place_test):
        return None
    if NOT_A_PLACE.search(for_the_place_test) or ALREADY_A_PLAN.search(clean):
        return None
    asking_where = bool(WHERE_TO_GET.search(clean))
    asking_if_there_is = bool((THERE_IS.search(clean) or bare_any) and NEARBY.search(clean))
    if bare_any and not asking_if_there_is:
        asking_if_there_is = bool(HOURS.search(clean))
    asking_for_a_name = (bool(A_RECOMMEND.search(clean))
                         and not A_ASKING_MY_OPINION.search(clean)
                         and not A_HAD_IT.search(clean)
                         and (bool(A_NAME_FOR_SOMEBODY.search(clean))
                              or bool(A_TRADE.search(clean))
                              or bool(A_THING_TO_HELP_WITH.search(clean))
                              or (bool(SOMEBODY.search(clean))
                                  and bool(A_JOB_ON_A_THING.search(clean)))))
    if not asking_where and not asking_if_there_is and not asking_for_a_name:
        return None
    if asking_for_a_name:
        return pick(list(A_HAND), memory, clean)
    who_does = re.search(r"\bwho (?:does|sells|fixes|repairs|makes)\b", clean) and NEARBY.search(clean)
    if asking_where and not who_does and not re.search(
            r"\b(?:get|buy|find|hire|pick up|source)\b", clean) and not NEARBY.search(clean):
        return None
    if HOURS.search(clean):
        return pick(list(THE_HOURS), memory, clean)
    if _a_person_for_the_job(clean):
        return pick(list(A_HAND), memory, clean)
    thing = _the_thing(clean)
    if thing:
        return pick(list(NO_MAP), memory, clean).format(thing=thing)
    return pick(list(NO_MAP_UNNAMED), memory, clean)
