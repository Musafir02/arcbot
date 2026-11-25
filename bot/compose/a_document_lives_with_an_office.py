import re

from . import pick

AN_ASK = re.compile(
    r"\b(?:where|who)\b[^.!?]{0,40}?\b(?:get|gets|got|hold|holds|find|order|apply|request|"
    r"obtain|keep|keeps|stored|copy)\b"
    r"|\bhow\s+(?:do|can|could|would|should)\s+i\s+(?:get|find|order|apply|request|obtain|"
    r"replace)\b"
    r"|\bhow\s+to\s+(?:get|find|order|apply|request|obtain)\b"
    r"|\bcan\s+i\s+(?:get|find|order|request|obtain|replace)\b"
    r"|\bwhere\s+(?:is|are)\s+[^.!?]{0,30}?\b(?:kept|held|stored|filed)\b",
    re.IGNORECASE)

A_LOST = re.compile(
    r"\b(?:lost|losted|misplaced|mislaid|can'?t\s+find|cannot\s+find|can\s+not\s+find|"
    r"cant\s+find|need\s+(?:a\s+)?(?:new|replacement|another)\s+copy|"
    r"need\s+a\s+copy)\b",
    re.IGNORECASE)

A_PERSON_LOST = re.compile(
    r"\b(?:baby|babies|mum|mums|mom|mother|dad|father|son|daughter|child|children|boy|girl|"
    r"husband|wife|partner|brother|sister|gran|granny|grandma|grandad|grandpa|nana|friend|"
    r"mate|colleague|neighbou?r|pup|puppy|kitten|dog|cat|horse|pet)\b",
    re.IGNORECASE)

THE_OFFICE_NAMES = {
    "deeds": re.compile(r"land\s+registry|registers\s+of\s+scotland|title\s+register",
                        re.IGNORECASE),
    "logbook": re.compile(r"\bdvla\b|\bv5c\b", re.IGNORECASE),
    "will": re.compile(r"solicitor|probate\s+service|probate\s+record", re.IGNORECASE),
    "lease": re.compile(r"landlord|managing\s+agent|solicitor", re.IGNORECASE),
    "certificate": re.compile(r"register\s+office|general\s+register\s+office",
                              re.IGNORECASE),
    "probate": re.compile(r"probate\s+service|gov\.uk|solicitor", re.IGNORECASE),
    "records": re.compile(r"\bgp\b|surgery|practice", re.IGNORECASE),
}

THE_KINDS = (
    ("probate", re.compile(
        r"\b(?:probate|grant\s+of\s+probate|letters\s+of\s+administration|"
        r"probate\s+(?:record|records|copy|papers?))\b", re.IGNORECASE)),
    ("logbook", re.compile(
        r"\b(?:log\s?book|logbook|v5c|v5\s?c|registration\s+document)\b", re.IGNORECASE)),
    ("deeds", re.compile(
        r"\b(?:deeds?|title\s+(?:register|deeds?|plan)|land\s+registry|"
        r"title\s+number)\b", re.IGNORECASE)),
    ("will", re.compile(
        r"\b(?:a|the|my|his|her|their|our|your)\s+will\b"
        r"|\b[\w'’]*s['’]?\s+will\b"
        r"|\b(?:grant\s+of\s+)?probate\s+copy\b", re.IGNORECASE)),
    ("lease", re.compile(
        r"\b(?:lease|leases|tenancy\s+agreement|assured\s+shorthold)\b", re.IGNORECASE)),
    ("certificate", re.compile(
        r"\b(?:birth\s+certificate|marriage\s+certificate|death\s+certificate|"
        r"certified\s+copy)\b", re.IGNORECASE)),
    ("records", re.compile(
        r"\b(?:medical\s+records?|health\s+records?|my\s+records?|gp\s+records?|"
        r"patient\s+records?)\b", re.IGNORECASE)),
)

THE_OFFICE = {
    "deeds": (
        "The deeds are the title register, and HM Land Registry holds it for England and Wales "
        "(Registers of Scotland north of the border). Their own service will sell you a copy "
        "from the property's address, and that copy is the one that counts.",
        "What people call the deeds is now the title register at HM Land Registry, so there is "
        "nothing to ask a solicitor for first: search their service by the property's address, "
        "pay a few pounds, and the copy comes as a download.",
    ),
    "logbook": (
        "The log book is the V5C and the DVLA issues it - no shop has one. If yours is lost or "
        "damaged, apply for a replacement on gov.uk with the car's details and the green slip "
        "you kept from the sale.",
        "That one comes from the DVLA, not a counter in town: a replacement V5C is applied for "
        "on gov.uk, and the car's registration number plus the details of the keeper is what "
        "the form asks for.",
    ),
    "will": (
        "The will itself is with whoever drew it up or kept it - usually the solicitor - and "
        "once probate is granted a copy goes on the public record at the Probate Service. Ask "
        "the solicitor first, then search the Probate Service's own record.",
        "Start with the solicitor named on it, or the person who kept the original, because a "
        "will is not registered anywhere while the person is alive. After probate it is a "
        "public document and the Probate Service will sell you a copy.",
    ),
    "lease": (
        "The lease is held by the landlord or their managing agent, and if you bought the "
        "flat your solicitor will have kept a copy - that is usually a phone call and an email. "
        "A managing agent will send one for a small fee if the solicitor cannot find it.",
        "Ask the landlord or the managing agent for a copy, and check your own paperwork first: "
        "anyone who has bought a leasehold flat was sent one at completion, and the solicitor "
        "who did the buying keeps it on file.",
    ),
    "certificate": (
        "A certificate comes from the register office for the district where the birth, "
        "marriage or death was registered, or from the General Register Office for older ones. "
        "Their own site takes the order - have the date and the place ready.",
        "The register office for the district where it happened holds it, and the General "
        "Register Office holds the older records. Order through their own site with the date "
        "and the place, and the certificate comes by post.",
    ),
    "probate": (
        "A grant of probate comes from the Probate Service, through gov.uk, and it is the "
        "court's copy rather than the will. An estate with a house, shares or a disagreement in "
        "it is worth a solicitor doing that part.",
        "Probate is the Probate Service's, applied for on gov.uk, and it is worth checking "
        "whether the estate is small enough for the simpler form. If there is property or a "
        "will being argued over, hand it to a solicitor.",
    ),
    "records": (
        "Your medical records sit with the GP surgery you are registered at, and you can ask "
        "for a copy in writing - the surgery has to answer, usually within a month.",
        "Ask the GP surgery that has you registered: a written request gets you a copy of the "
        "records, and the reception will say what they need from you to prove it is you.",
    ),
}

A_MAP_LINE = re.compile(
    r"^(?:No map on this side|I can't see what's near you|There's no list of places here|"
    r"No stock lists here|I can't check stock or shops near you)",
    re.IGNORECASE)


def a_map_app_line(reply):
    return bool(reply) and bool(A_MAP_LINE.match(str(reply).strip()))


def _the_kind(clean):
    for name, pattern in THE_KINDS:
        if pattern.search(clean):
            return name
    return ""


def _names_the_office(reply, kind):
    pattern = THE_OFFICE_NAMES.get(kind)
    return bool(reply and pattern and pattern.search(str(reply)))


def a_lost_record(text, reply=None):
    clean = " ".join(str(text or "").lower().split())
    if not clean or not A_LOST.search(clean) or A_PERSON_LOST.search(clean):
        return False
    kind = _the_kind(clean)
    if not kind:
        return False
    return not _names_the_office(reply, kind)


def answer_for(text, memory=None, reply=None):
    clean = " ".join(str(text or "").lower().split())
    if not clean:
        return None
    asked = bool(AN_ASK.search(clean))
    lost = bool(A_LOST.search(clean))
    if not asked and not lost:
        return None
    kind = _the_kind(clean)
    if not kind:
        return None
    if lost and A_PERSON_LOST.search(clean):
        return None
    if lost and not asked and _names_the_office(reply, kind):
        return None
    return pick(THE_OFFICE[kind], memory, clean)
