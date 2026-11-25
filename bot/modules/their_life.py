import re

PRIORITY = 100

_PLACES = (
    "{Where} - what's it like there?",
    "How long have you been there?",
    "{Where}, then. Is it handy for what you need?",
)

_ONE_PET = (
    "{Pet} - what's their name?",
    "How long have they been with you?",
    "{Pet} - who spoils them most?",
)

_PETS = (
    "{Pets} - do they get on?",
    "{Pets} - what are their names?",
    "{Pets} - who spoils them most?",
)

_NUMBER_WORDS = {"two": "Two", "three": "Three", "four": "Four", "five": "Five", "six": "Six"}

_NOT_A_SHAPE = re.compile(
    r"\b(?:pain|pains|painful|hurt|hurts|hurting|ill|sick|poorly|dying|died|dead|death|"
    r"cancer|chemo|radiotherapy|tumour|tumor|dementia|alzheimers|alzheimer's|stroke|"
    r"hospital|hospice|funeral|buried|passed away|lost|loss|bereave\w*|griev\w*|"
    r"depress\w*|anxious|anxiety|panic|suicid\w*|self harm|crisis|emergency|"
    r"broken|leaking|damp|mould|flood\w*|evicted|eviction|arrears|debt|bailiff\w*|"
    r"divorce|separated|affair|abusive|violent|police|social services)\b", re.I)

_STORY = re.compile(
    r"\b(?:that|which|who|and|but|because|so|when|while|if|keeps?|kept|started|stopped|"
    r"barking|bites|bit|chewed|escaped|ran|went|got|needs?|needed|wants?|made|makes|"
    r"cost|costs|comes?|came|goes?|going|has|have|had|is|are|was|were|will|would|can|could)\b",
    re.I)

_TONE = re.compile(
    r"(?:\s+(?:tbh|tho|though|now|anyway|actually|really|literally|honestly|i\s+suppose|"
    r"i\s+guess|still|also|too|by\s+the\s+way|btw|atm|at\s+the\s+moment|lol|ha|haha|lmao|"
    r"so\s+yeah|yeah|innit|mate|dude|as\s+well))+$", re.I)

_LIVE = re.compile(
    r"^(?P<who>i|we)\s+(?:live|stay)\s+"
    r"(?P<where>(?:in|near|on|by|above|below|behind|next\s+to|opposite|at)\s+"
    r"(?:a|an|the|my|our|their|his|her)?\s*[a-z][a-z' -]{0,24})$")

_PLACE_KINDS = re.compile(
    r"^(?:in|near|on|by|above|below|behind|next\s+to|opposite|at)\s+"
    r"(?:a|an|the|my|our)?\s*(?:flat|house|home|place|bungalow|cottage|farm|boat|caravan|"
    r"car park|park|river|canal|sea|coast|beach|woods|wood|common|high\s+street|"
    r"village|town|city|estate|council\s+estate|block|tower\s+block|camper|motorhome|"
    r"shop|pub|office|station|hospital\s+car\s+park|school|church|allotment)$")

_PET = re.compile(
    r"^(?P<who>i|we)(?:'ve\s+got|\s+(?:have|got|own))\s+"
    r"(?P<num>a|an|one|two|three|four|five|six|\d+|\d+\s+)?\s*"
    r"(?P<pet>dogs?|cats?|puppies|puppy|kittens?|kitten|rabbits?|hamsters?|budgies?|parrots?|"
    r"horses?|pony|guinea\s+pigs?|tortoises?|snakes?|lizards?|geckos?|fish|gerbils?|ferrets?|"
    r"chickens?|hens?|ducks?|goats?|bees)$")


_SIBLINGS = re.compile(
    r"^(?P<who>i|we)(?:'ve\s+got|\s+(?:have|got))\s+(?P<what>"
    r"(?:(?:a|an|one|two|three|four|five|six|seven|eight|\d+|older|younger|little|big|twin|"
    r"step|half)[\s-]+)*(?:brother|sister|brothers|sisters)"
    r"(?:\s*(?:,|and)\s*)?"
    r"(?:(?:a|an|one|two|three|four|five|six|seven|eight|\d+|older|younger|little|big|twin|"
    r"step|half)[\s-]+)*(?:brothers?|sisters?)?)$")

_SIBLING_LINES = (
    "{What} - older or younger than you?",
    "{What} - do you see much of them?",
    "{What}, and do you get on?",
)

_AGE = re.compile(
    r"^(?:im|i'm|i\s+am)\s+(?P<age>\d{1,2})(?:\s*(?:years?\s+old|yrs?\s+old|y/?o|yo|now|"
    r"today))?$")

_NOT_AN_AGE = re.compile(
    r"\b(?:weeks?|days?|months?|pregnan\w*|kilos?|kg|stone|pounds?|lbs?|miles?|minutes?|"
    r"hours?|degrees?|percent|%|cm|feet|foot|ft)\b", re.I)

_AGE_LINES = (
    "{Age} - how's this year treating you?",
    "{Age}, then. Anything you'd like to be different by {Next}?",
    "{Age} - a good age to be, or not?",
)

_RELATION = (
    r"mother\s+in\s+law|father\s+in\s+law|son\s+in\s+law|daughter\s+in\s+law|"
    r"sister\s+in\s+law|brother\s+in\s+law|"
    r"step\s?mum|stepmum|step\s?dad|stepdad|step\s?daughter|stepdaughter|step\s?son|"
    r"stepson|"
    r"mum|mom|mother|mam|dad|father|gran|granny|grandma|nan|nana|grandad|grandpa|grandfather|"
    r"sister|brother|son|daughter|aunt|auntie|uncle|cousin|niece|nephew|wife|husband|partner|"
    r"boyfriend|girlfriend|grandson|granddaughter|grandchild"
)

_SOMEONE = re.compile(r"^(?P<who>my|our)\s+(?P<rel>" + _RELATION + r")\s+(?P<rest>[a-z0-9 ']+)$")

_SOMEONE_WORK = re.compile(
    r"^works?\s+(?:in|at|for)\s+(?:a|an|the)?\s*(?P<place>[a-z][a-z' ]{1,24})$")

_SOMEONE_HOURS = re.compile(
    r"^works?\s+(?P<hours>nights?|days?|night\s+shifts?|shifts|weekends?|evenings?|weekdays|"
    r"part\s+time|full\s+time|(?:two|three|four|five|six)\s+days\s+a\s+week|"
    r"long\s+hours|away\s+a\s+lot)$")

_SOMEONE_AGE = re.compile(
    r"^is\s+(?P<age>\d{1,2})(?:\s*(?:years?\s+old|yrs?\s+old|y/?o|yo|now|today))?$")

_AGE_READ_ELSEWHERE = frozenset((
    "son", "daughter", "kid", "kids", "child", "children", "boy", "girl", "eldest", "youngest",
    "grandson", "granddaughter", "grandchild", "grandchildren", "grandkids",
    "stepson", "stepdaughter", "step son", "step daughter", "son in law", "daughter in law",
    "niece", "nephew",
))

_SOMEONE_KIDS = re.compile(
    r"^has\s+(?P<num>\d+|one|two|three|four|five|six|seven|eight)\s+"
    r"(?P<kids>kids|children|child|boys?|girls?|sons?|daughters?|twins?)$")

_HER = frozenset((
    "mum", "mom", "mother", "mam", "gran", "granny", "grandma", "nan", "nana", "sister",
    "daughter", "aunt", "auntie", "niece", "wife", "girlfriend", "stepmum", "step mum",
    "stepdaughter", "step daughter", "mother in law", "daughter in law", "sister in law",
    "granddaughter",
))
_HIM = frozenset((
    "dad", "father", "grandad", "grandpa", "grandfather", "brother", "son", "uncle", "nephew",
    "husband", "boyfriend", "stepdad", "step dad", "stepson", "step son", "father in law",
    "son in law", "brother in law", "grandson",
))

_SOMEONE_WORK_LINES = (
    "A {Place}, then. What's that like for {them}?",
    "{Place} - is that new for {them}?",
    "A {Place}, then. Do you hear much about it from {them}?",
)

_SOMEONE_HOURS_LINES = (
    "{Hours} - does that leave much time for {them}?",
    "{Hours}, then. What's that like for {them}?",
    "{Hours} - does it suit {them}?",
)

_SOMEONE_AGE_LINES = (
    "{Age} - do you see {them} much?",
    "{Age}, then. Do you get to see {them} often?",
    "{Age} - how often do you get to see {them}?",
)

_SOMEONE_KIDS_LINES = (
    "{Num} kids - how old are they?",
    "{Num} kids, then. Do they live near you?",
    "{Num} kids - what are they into?",
)

_NUMBER_WORD = {"1": "One", "2": "Two", "3": "Three", "4": "Four", "5": "Five", "6": "Six",
                "7": "Seven", "8": "Eight"}

_MORE_THAN_ONE = frozenset(("two", "three", "four", "five", "six"))


def _more_than_one(num):
    said = str(num or "").strip()
    if said in _MORE_THAN_ONE:
        return True
    return said[:1].isdigit() and said not in ("0", "1")


def _line(text):
    said = str(text or "").replace("\u2019", "'").strip().lower()
    said = said.strip(" .,!;:-\"'")
    said = re.sub(r"\s+", " ", said)
    while True:
        trimmed = _TONE.sub("", said)
        if trimmed == said:
            return said
        said = trimmed


def _a_fact_about_their_life(said):
    if not said or "?" in said or _NOT_A_SHAPE.search(said):
        return None
    lived = _LIVE.match(said)
    if (lived and _PLACE_KINDS.match(lived.group("where"))
            and not _STORY.search(lived.group("where"))):
        return "place"
    siblings = _SIBLINGS.match(said)
    if siblings and not _STORY.search(said[siblings.end():]):
        what = _TONE.sub("", siblings.group("what")).strip(" ,")
        if what:
            return "siblings:" + what
    age = _AGE.match(said)
    if age and not _NOT_AN_AGE.search(said) and 13 <= int(age.group("age")) <= 99:
        return "age:" + age.group("age")
    pet = _PET.match(said)
    if pet and not _STORY.search(said[pet.end():]):
        num = (pet.group("num") or "").strip()
        kind = "two_pets" if _more_than_one(num) else "pet"
        return kind + ":" + num + ":" + pet.group("pet")
    someone = _SOMEONE.match(said)
    if someone:
        detail = _a_detail_about_someone(someone.group("rel"), someone.group("rest"))
        if detail:
            return "someone:" + someone.group("rel") + ":" + detail
    return None


def _a_detail_about_someone(rel, rest):
    said = (rest or "").strip()
    if not said:
        return None
    worked = _SOMEONE_WORK.match(said)
    if worked and not _STORY.search(worked.group("place")):
        return "work:" + worked.group("place").strip()
    hours = _SOMEONE_HOURS.match(said)
    if hours:
        return "hours:" + hours.group("hours").strip()
    age = _SOMEONE_AGE.match(said)
    if age and 1 <= int(age.group("age")) <= 99:
        if (rel or "").strip() not in _AGE_READ_ELSEWHERE:
            return "age:" + str(int(age.group("age")))
    kids = _SOMEONE_KIDS.match(said)
    if kids:
        return "kids:" + kids.group("num").strip()
    return None


def _their_pronoun(rel):
    said = re.sub(r"\s+", " ", (rel or "").strip())
    if said in _HER:
        return "her"
    if said in _HIM:
        return "him"
    return "them"


def _where_words(said):
    lived = _LIVE.match(said)
    where = lived.group("where") if lived else said
    return where[:1].upper() + where[1:]


def respond(text, memory):
    said = _line(text)
    found = _a_fact_about_their_life(said)
    if not found:
        return None
    kind, _, rest = found.partition(":")
    if kind in ("siblings", "age", "someone"):
        num, animal = rest, ""
    elif kind in ("pet", "two_pets"):
        num, animal = rest.split(":", 1)
    else:
        num, animal = "", ""
    from ..compose import fallback
    if (fallback._the_thread_is_heavy(memory) or fallback._reads_as_heavy_news(said)
            or _THE_LINE_BEFORE_IS_HEAVY.search(_the_line_before(memory))):
        return None
    return _the_fact(kind, num, animal, said, memory)


_THE_LINE_BEFORE_IS_HEAVY = re.compile(
    r"\b(?:ill|unwell|poorly|sick|dying|died|death|passed away|funeral|bereave\w*|griev\w*|"
    r"cancer|chemo\w*|radiotherap\w*|tumou?r|dementia|alzheim\w*|stroke|sepsis|surgery|"
    r"operation|transplant|hospice|palliative|terminal|hospital|icu|ambulance|diagnos\w*|"
    r"bully\w*|bullied|depress\w*|suicid\w*|self harm|miscarr\w*|stillborn|addict\w*|"
    r"relapse\w*|overdose\w*|sectioned|in pain|suffering)\b", re.I)


def _the_line_before(memory):
    turns = [turn for turn in ((memory or {}).get("turns") or []) if isinstance(turn, dict)]
    return str(turns[-1].get("user") or "") if turns else ""


def _the_fact(kind, num, animal, said, memory):
    if kind == "siblings":
        what = num[:1].upper() + num[1:]
        return _pick(_SIBLING_LINES, memory).replace("{What}", what)
    if kind == "age":
        line = _pick(_AGE_LINES, memory)
        return line.replace("{Age}", num).replace("{Next}", str(int(num) + 1))
    if kind == "place":
        return _pick(_PLACES, memory).replace("{Where}", _where_words(said))
    if kind == "someone":
        rel, _, detail = num.partition(":")
        return _the_someone_line(rel, detail, memory)
    if kind == "two_pets":
        line = _pick(_PETS, memory)
        count = _NUMBER_WORDS.get(num, "The")
        return line.replace("{Pets}", count + " " + _plural(animal))
    line = _pick(_ONE_PET, memory)
    return line.replace("{Pet}", ("An " if animal[:1] in "aeiou" else "A ") + animal)


def _the_someone_line(rel, detail, memory):
    kind, _, said = detail.partition(":")
    them = _their_pronoun(rel)
    if kind == "work":
        line = _pick(_SOMEONE_WORK_LINES, memory)
        place = said.capitalize() if line.startswith("{Place}") else said
        return line.replace("{Place}", place).replace("{them}", them)
    if kind == "hours":
        line = _pick(_SOMEONE_HOURS_LINES, memory)
        return line.replace("{Hours}", said.capitalize()).replace("{them}", them)
    if kind == "age":
        line = _pick(_SOMEONE_AGE_LINES, memory)
        return line.replace("{Age}", said).replace("{them}", them)
    line = _pick(_SOMEONE_KIDS_LINES, memory)
    num = _NUMBER_WORD.get(said, said.capitalize())
    return line.replace("{Num}", num)


def _plural(word):
    said = str(word or "")
    if said.endswith("s") or said in ("fish", "sheep", "deer"):
        return said
    if said.endswith("y"):
        return said[:-1] + "ies"
    return said + "s"


def _pick(pool, memory):
    said = set()
    for turn in (memory.get("turns") or []):
        if isinstance(turn, dict) and isinstance(turn.get("bot"), str):
            said.add(turn["bot"].strip())
    for line in pool:
        if line not in said:
            return line
    return pool[0]
