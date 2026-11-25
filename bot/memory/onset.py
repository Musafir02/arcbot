import re

from ..compose import pick

ONSET = re.compile(
    r"(?:\b(?:it|this|that|they|these|those|everything|the\s+\w+)\s+)?"
    r"\b(?:all\s+)?(?:started|started\s+off|began|begun|kicked\s+off|came\s+on|set\s+off)\b"
    r"\s*(?:off\s+)?(?:"
    r"(?:when|after|around|about|in|since|because|following|with|from|last|this)\b"
    r"|(?=\d+|a\b|an\b|one\b|two\b|three\b|four\b|five\b|six\b|seven\b|eight\b|nine\b|"
    r"ten\b|eleven\b|twelve\b|a\s+couple\b|a\s+few\b|several\b))"
)

BODY = (
    r"\b(?:back|knee|knees|shoulder|hip|leg|arm|neck|wrist|ankle|foot|feet|hand|hands|head|"
    r"stomach|chest|tooth|teeth|elbow|thigh|calf|joint|muscle)\b(?:'s)?\b"
    r"|\b(?:hurts?|hurting|ache|aches|aching|pain|painful|sore|swollen|injured|sprain\w*)\b",
)

THE_PERSON = (
    r"\b(?:sleep|sleeps|sleeping|slept|insomnia|wake|wakes|waking|awake|asleep|nightmare|"
    r"nightmares|nap|naps|napping|tired|exhausted|knackered|drained|weary)\b"
    r"|\b(?:anxious|anxiety|worried|worry|worrying|panic|panicking|stressed|stress|tense|"
    r"down|low|depressed|depression|miserable|tearful|weepy|crying|hopeless|flat|numb|"
    r"overwhelmed|burnt\s+out|burned\s+out)\b"
    r"|\b(?:cant\s+sleep|can'?t\s+sleep|not\s+sleeping|feel\s+(?:\w+\s+)?(?:low|down|awful))\b",
)

MOVED = (
    r"\b(?:moved|moving|move)\b.{0,24}\b(?:house|home|flat|place|out|in|abroad|country|city|town)\b"
    r"|\b(?:moved\s+in|house\s+move|new\s+(?:house|flat|place|home))\b",
)
JOB_LOST = (
    r"\b(?:lost|loss|losing|lose)\b.{0,16}\b(?:job|work|position|role)\b"
    r"|\b(?:made\s+redundant|redundancy|redundant|got\s+the\s+sack|sacked|laid\s+off|fired|"
    r"out\s+of\s+work|unemployed)\b",
)
BABY = (
    r"\b(?:had|having|born|arrived|came\s+home\s+with)\b.{0,20}\b(?:baby|babies|twins|child|"
    r"newborn|son|daughter)\b"
    r"|\b(?:new\s+baby|newborn|pregnan\w+)\b",
)
DIED = (
    r"\b(?:died|dying|passed\s+away|death|funeral|bereave\w*)\b"
    r"|\blost\s+(?:my\s+)?(?:mum|mom|mother|dad|father|husband|wife|partner|son|daughter|"
    r"brother|sister|friend|gran|nan|grandad|grandma|child)\b",
)
SPLIT = (
    r"\b(?:split\s+up|splitting\s+up|broke\s+up|broken\s+up|break\s+up|breaking\s+up|divorce\w*|"
    r"separated|separation|left\s+me|walked\s+out|kicked\s+me\s+out)\b",
)
MONEY = (
    r"\b(?:debts?|arrears|overdraft|rent|mortgage|bills?|money|cost\s+of\s+living|"
    r"can'?t\s+pay|cant\s+pay|council\s+tax|evict\w*|repossess\w*)\b",
)
OTHER = (
    r"\b(?:accident|fell|fall|surgery|operation|operated|hospital|diagnos\w*|chemo|treat\w*|"
    r"illness|ill\b|unwell|pregnan\w*|menopause|hormones?|birth|new\s+shift|night\s+shift|"
    r"shift\s+work|kids?|children|caring|carer|made\s+homeless|eviction)\b",
)

CAUSES = (
    ("move", MOVED),
    ("job", JOB_LOST),
    ("baby", BABY),
    ("died", DIED),
    ("split", SPLIT),
    ("money", MONEY),
    ("other", OTHER),
)

NAMED = (
    r"\b(?:christmas|new\s+year|easter|summer|winter|spring|autumn|last\s+(?:year|summer|winter)|"
    r"the\s+summer|the\s+winter)\b",
)
NAMED_DAYS = 30

LENGTH = re.compile(
    r"\b(?:about|around|nearly|almost|over|just\s+over|a\s+good|at\s+least)?\s*"
    r"(\d+|a|an|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|a\s+few|a\s+couple|"
    r"several|many)\s+(?:of\s+)?(day|days|week|weeks|month|months|year|years)\b"
)
BARE_UNIT = re.compile(
    r"^(day|days|week|weeks|month|months|year|years)\b")

NUMBER_WORDS = {"a": 1, "an": 1, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
                "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
                "a few": 3, "a couple": 2, "several": 4, "many": 30}



MOVED_REPLIES = (
    "Moving is one of the biggest upheavals there is - new room, new noises, a head full of boxes - "
    "so this is the usual bill for it. Hold on to your normal routine as far as you can and give "
    "it a few weeks.",
    "A house move unsettles people for a while: everything that used to be familiar is not. That "
    "is worth knowing, because it means this is a reaction to a change rather than something "
    "wrong with you.",
    "Nobody sleeps properly in the first weeks of a move - the room, the noises and the unpacking "
    "all keep the night shallow. It settles as the place becomes yours.",
)
JOB_REPLIES = (
    "Losing a job is exactly the kind of worry that keeps people awake and on edge, and that is "
    "the situation rather than anything wrong with you. Give the routine a few weeks; if it is "
    "still bad after a month, take it to a GP.",
    "A job going is a shock to the routine as much as the money, and it takes weeks for the days "
    "to settle again. Keep the wake-up time where it was - it is the part that holds the rest.",
    "That is a blow, and it lands on sleep and mood first. Being kind about the basics - food, "
    "daylight, someone to talk to - does more in the first weeks than trying to fix it all.",
)
BABY_REPLIES = (
    "A baby rewrites your nights, and that is the baby rather than a fault in you. Sleep when you "
    "can rather than when it is bedtime, and take any offer of help with the nights while it is "
    "offered.",
    "The first months with a baby are broken nights by design, so this is the shape of it rather "
    "than something to fix. If it is still this bad once they sleep through, then it is worth "
    "looking at yours.",
)
DIED_REPLIES = (
    "Losing someone close changes sleep and mood for months, and that is grief doing its work "
    "rather than a fault in you. Be gentle with the basics, and tell your GP if it is not "
    "shifting - they can help without turning it into a diagnosis.",
    "That kind of loss sits in the body as well as the head, so broken sleep and a low week are "
    "the usual shape of it. Company and daylight help more than anything clever, and a GP is "
    "there if it stays bad.",
)
SPLIT_REPLIES = (
    "A break-up turns everything over, and sleep and mood are the first things to go with it. It "
    "eases as the new shape of the days settles - which it does, though not in a straight line.",
    "That is the sort of upheaval that keeps people awake and swinging between angry and low. Keep "
    "the routine steady where you can; the rest catches up.",
)
MONEY_REPLIES = (
    "Money worry is the kind that keeps people awake at 3am, and it is the worry rather than the "
    "sum that does it. Getting the numbers written down in one place usually makes the night "
    "quieter, and the free debt advice services are there for exactly this.",
    "That is a real weight, and it sits on sleep before it sits on anything else. One thing at a "
    "time - the smallest bill or the first call - is worth more than a plan you cannot start.",
)
OTHER_REPLIES = (
    "That is the sort of thing that would do it - a change like that unsettles sleep and mood for "
    "a few weeks before it settles.",
    "That would unsettle anyone for a while, and it is the change rather than you. Give it a few "
    "weeks and keep the routine as steady as you can.",
)

BODY_REPLIES = (
    "That is the usual way to do it - a day of lifting, twisting and carrying is harder on a joint "
    "than it looks. Keep moving gently rather than resting it, and it usually eases over a couple "
    "of weeks.",
    "Strains like that come from exactly this kind of day, and the muscle settles faster if you "
    "keep gently active than if you sit still. Warmth and a painkiller are fine while it does.",
)

LENGTH_REPLIES = (
    "This long is long enough that waiting for it to pass is not a plan: if it has not eased by "
    "now, that is worth taking to a GP, and saying when it started is the useful bit.",
    "Since it has been going on this long, it is worth asking someone rather than sitting with "
    "it - a GP can check the ordinary causes, and being able to say how long it has been going "
    "on helps.",
)

BY_CAUSE = {"move": MOVED_REPLIES, "split": SPLIT_REPLIES, "money": MONEY_REPLIES}

LEAVE_IT = ("job", "baby", "died")

LONG_ENOUGH = 14

UNIT_DAYS = {"day": 1, "days": 1, "week": 7, "weeks": 7, "month": 30, "months": 30,
             "year": 365, "years": 365}


def _clean(line):
    return str(line or "").lower().strip()


def _pattern(found):
    return found[0] if isinstance(found, (tuple, list)) else found


def _days(match):
    word = re.sub(r"\s+", " ", match.group(1).strip())
    count = NUMBER_WORDS.get(word)
    if count is None:
        try:
            count = int(word)
        except (TypeError, ValueError):
            return None
    return count * UNIT_DAYS.get(match.group(2), 1)


def _clause(line):
    found = ONSET.search(line)
    if not found:
        return ""
    return line[found.end():].strip(" .,!;:-")


def reads_as_onset(line):
    clean = _clean(line)
    if not clean or "?" in clean:
        return None
    clause = _clause(clean)
    if not clause:
        return None
    found = ONSET.search(clean)
    if found is not None and found.end() == found.start():
        unit = BARE_UNIT.match(clause)
        if unit:
            return "time", UNIT_DAYS.get(unit.group(1), 1)
        length = LENGTH.search(clause)
        if length and _days(length) is not None:
            return "time", _days(length)
        return None
    for name, pattern in CAUSES:
        if re.search(_pattern(pattern), clause):
            return name, None
    if re.search(_pattern(NAMED), clean):
        return "time", NAMED_DAYS
    unit = BARE_UNIT.match(clause)
    if unit:
        return "time", UNIT_DAYS.get(unit.group(1), 1)
    length = LENGTH.search(clause)
    if length and _days(length) is not None:
        return "time", _days(length)
    return None


def _body_before(memory):
    try:
        turns = memory.get("turns") if isinstance(memory, dict) else None
    except AttributeError:
        return False
    if not isinstance(turns, list) or not turns:
        return False
    said = _clean((turns[-1] or {}).get("user"))
    return bool(re.search(_pattern(BODY), said))


def _the_person_before(memory):
    try:
        turns = memory.get("turns") if isinstance(memory, dict) else None
    except AttributeError:
        return False
    if not isinstance(turns, list) or not turns:
        return False
    said = _clean((turns[-1] or {}).get("user"))
    if not said:
        return False
    return bool(re.search(_pattern(BODY), said) or re.search(_pattern(THE_PERSON), said))


def _answered_before(memory):
    try:
        turns = memory.get("turns") if isinstance(memory, dict) else None
    except AttributeError:
        return False
    if not isinstance(turns, list) or not turns:
        return False
    said = str((turns[-1] or {}).get("bot") or "")
    return len(said.strip()) >= 60


def reply(line, memory):
    reading = reads_as_onset(line)
    if reading is None:
        return None
    if not _answered_before(memory):
        return None
    cause, days = reading
    if cause in LEAVE_IT:
        return None
    if _body_before(memory):
        return pick(BODY_REPLIES, memory, line) if cause != "time" else None
    if cause == "time":
        if days is None or days < LONG_ENOUGH:
            return None
        if not (_body_before(memory) or _the_person_before(memory)):
            return None
        return pick(LENGTH_REPLIES, memory, line)
    pool = BY_CAUSE.get(cause) or OTHER_REPLIES
    return pick(pool, memory, line)
