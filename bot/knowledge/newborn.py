import re

from .lookup import entry

ANSWERS = ("family-and-parenting",)

ENTRIES = []


_THE_FIRST_FORTNIGHT = (
    "Congratulations. The first fortnight is mostly feeding and sleep: eight to twelve feeds in "
    "24 hours, six or more wet nappies a day, and the midwife comes on day five for the heel-prick "
    "blood spot test. The cord drops off in about a week to a fortnight, and the birth weight, "
    "down by up to a tenth in the first days, is back by two weeks. Ring the midwife or 111 the "
    "same day if the baby is too sleepy to feed, has fewer wet nappies, or looks yellow.")

_CORD = (
    "The cord stump dries out and drops off on its own between about five days and a fortnight - "
    "clean and dry, water only, no cream or powder, and fold the nappy below it so air gets to "
    "it, and let it come away rather than pulling. A little bleeding at the very end is normal; a "
    "red, hot or smelly patch around the base, or pus, is a call to the midwife the same day. If "
    "it is still there at three weeks, mention it.")

_OUT_AND_ABOUT = (
    "You can take a newborn out from the first day: a pram or a sling, one more layer than you "
    "are wearing, and out of direct sun. Keep them out of crowded rooms and away from anyone with "
    "a cough or a cold for the first six weeks, and take the pram rather than passing a newborn "
    "round a room. Go out after a feed and you get the long sleep for it.")

_CLUSTER_FEEDING = (
    "An evening of non-stop feeding is cluster feeding, and it is normal in the first weeks: it "
    "is not a sign your milk is short, it is how the supply is built. Keep them on, swap sides, "
    "and get someone else to take them for an hour once they settle so you can sleep. A baby who "
    "is having six or more wet nappies a day and gaining along their line is getting enough - the "
    "scales at the clinic settle it better than the length of a feed.")

_BIRTH_WEIGHT = (
    "The average baby weighs about 3.5 kg (7 lb 8 oz) at birth, and anything from 2.5 to 4.5 kg "
    "is normal, so 3 kg (6 lb 10 oz) is a common and perfectly normal size. The figure to watch "
    "is the change: up to a tenth of it can go in the first few days, and it is back to birth "
    "weight by two weeks. A baby who has not got back to it by then is seen again, so keep the "
    "weigh-in appointments.")

_WEIGHT_SAID = re.compile(
    r"\b(?:weighed|weighs|weight|kilos?|kg|pounds?|lbs?)\b|\b\d+(?:\.\d+)?\s*(?:kilo|kg|lbs?|"
    r"pounds?)\b", re.I)
_DAYS_OLD = re.compile(r"\b(\d{1,2})\s+days?\s+old\b", re.I)
_WEEKS_OLD = re.compile(r"\b(\d{1,2})\s+weeks?\s+old\b", re.I)
_A_NEWBORN_WORD = re.compile(
    r"\b(?:newborn|newborns|newly born|just born|born last week|born yesterday|born this week|"
    r"born a week ago|first week|first fortnight|first few weeks|just had a baby|"
    r"just had the baby|had the baby|had our baby|gave birth|given birth|"
    r"born on (?:mon|tues|wednes|thurs|fri|satur|sun)day|born this morning|born today|"
    r"born at (?:the|home)|home birth)\b", re.I)
_NOT_THE_FORTNIGHT = (
    "temperature", "fever", "sick", "vomiting", "diarrhoea", "rash", "cold", "cough", "colic",
    "wind", "reflux", "nappy", "nappies", "poo", "sleep", "sleeps", "sleeping", "wont sleep",
    "wont feed", "wont take a feed", "not feeding", "isnt feeding", "breastfeed", "breastfeeding",
    "formula", "milk", "jab", "jabs", "vaccine", "vaccines", "vaccination", "cot", "cot death",
    "pram", "pushchair", "car seat", "bath", "teething", "jaundice", "pillow", "swaddle",
    "swaddling", "dummy", "weaning", "solids", "food", "name", "christening", "gift", "present",
    "visitors", "visiting", "nursery", "childminder", "weight gain", "not gaining", "losing",
    "early", "premature", "twins", "breath", "breathing", "cord around", "crying", "cries",
    "unsettled", "winding", "screen", "test", "hospital", "doctor", "gp", "health visitor",
    "what do i need", "need to buy", "need to get", "what to buy", "what do we need", "buy")


def _the_line_said(understood):
    for field in ("text", "clean", "plain"):
        said = (understood or {}).get(field)
        if isinstance(said, str) and said.strip():
            return " ".join(said.lower().split())
    return ""


_SOMEONE_ELSE_BABY = re.compile(
    r"\b(?:my|our)\s+(?:sister|sisters|friend|friends|neighbour|neighbor|colleague|boss|cousin|"
    r"niece|aunt|auntie|daughter-in-law|sister-in-law|brother|brother-in-law|stepdaughter)s?\b"
    r"|\b(?:a friend|her baby|his baby|their baby|she had a baby|she had her baby)\b", re.I)


def _the_line_is_the_news(understood):
    said = _the_line_said(understood)
    if not said:
        return False
    if re.search(r"\b(?:she|he|they)\s+(?:was|is|were|has been)\b", said) and not re.search(
            r"\b(?:my|our)\b", said):
        return False
    if _SOMEONE_ELSE_BABY.search(said) and not re.search(
            r"\b(?:my|our)\s+(?:baby|son|daughter|newborn)\b|\bi (?:had|gave)\b", said):
        return False
    if _is_an_older_baby(said):
        return False
    if any(word in said for word in _NOT_THE_FORTNIGHT):
        return False
    return True


def _is_an_older_baby(said):
    days = _DAYS_OLD.search(said)
    if days and int(days.group(1)) > 14:
        return True
    weeks = _WEEKS_OLD.search(said)
    if weeks and int(weeks.group(1)) > 2:
        return True
    return bool(re.search(r"\b(?:[2-9]|1[0-9]|2[0-4])\s+months?\s+old\b", said)) or bool(
        re.search(r"\byears?\s+old\b", said))


def _is_a_newborn(said):
    days = _DAYS_OLD.search(said)
    if days and int(days.group(1)) <= 14:
        return True
    weeks = _WEEKS_OLD.search(said)
    if weeks and int(weeks.group(1)) <= 2:
        return True
    return False


def _a_birth_just_happened(memory, understood):
    from .family import _BIRTH_IN_THE_CHAT
    said = [_the_line_said(understood)]
    for turn in (memory.get("turns") or [])[-2:] if isinstance(memory, dict) else []:
        if isinstance(turn, dict):
            said.append(str(turn.get("user") or "").lower())
    return bool(_BIRTH_IN_THE_CHAT.search(" ".join(said)))


def _the_birth_weight(memory, understood):
    said = _the_line_said(understood)
    if not said or not _WEIGHT_SAID.search(said):
        return None
    if "birth" in said or "at birth" in said:
        return _BIRTH_WEIGHT
    if _DAYS_OLD.search(said) or _WEEKS_OLD.search(said):
        days = _DAYS_OLD.search(said)
        weeks = _WEEKS_OLD.search(said)
        if (days and int(days.group(1)) > 21) or (weeks and int(weeks.group(1)) > 6):
            return None
    if not _a_birth_just_happened(memory, understood):
        return None
    return _BIRTH_WEIGHT



ENTRIES.append(entry("a-cord-stump",
                     (("cord", "umbilical cord", "cord stump", "belly button", "stump"),
                      ("fall", "falls", "falling", "off", "come off", "comes off", "drop",
                       "drops", "when", "how long", "still on", "heal", "heals", "clean")),
                     _CORD, bias=2))
ENTRIES.append(entry("a-newborn-out-and-about",
                     (("newborn", "baby", "babies", "born", "days old", "weeks old"),
                      ("go out", "going out", "out and about", "outside", "leave the house",
                       "first trip", "take him out", "take her out", "take them out",
                       "take the baby out", "when can we go", "when can i take")),
                     _OUT_AND_ABOUT,
                     avoid=("car", "car seat", "carseat", "pram", "pushchair", "sling",
                            "vaccine", "vaccines", "jab", "jabs", "swim", "swimming"),
                     bias=2))
ENTRIES.append(entry("cluster-feeding",
                     (("baby", "babies", "newborn", "feeding", "feeds", "feed"),
                      ("cluster", "cluster feeding", "constantly", "all evening", "all the time",
                       "all night", "feeds constantly", "feeding constantly", "wants to feed",
                       "non stop", "nonstop", "every hour")),
                     _CLUSTER_FEEDING,
                     avoid=("wont feed", "won't feed", "not feeding", "isnt feeding",
                            "isn't feeding", "refusing", "refuses", "formula", "supply",
                            "mastitis", "blocked duct", "tongue tie", "losing", "not gaining",
                            "wont take", "won't take", "how often", "how much milk",
                            "how many feeds", "ounces",
                            "cries", "crying", "cry", "settle", "settling", "sleep",
                            "sleeps", "sleeping", "waking", "awake", "unsettled", "whingey"),
                     bias=2))
ENTRIES.append(entry("a-birth-weight",
                     (("weighed", "weighs", "weigh", "weight", "kilo", "kilos", "kg", "pounds",
                       "lb", "lbs"),
                      ("birth", "born", "newborn", "baby", "babies", "gave birth", "days old",
                       "last week", "at birth")),
                     _the_birth_weight,
                     avoid=("month old", "months old", "years old", "centile", "percentile",
                            "percent", "%", "gain", "gaining", "put on", "lost", "losing",
                            "dropped", "too much", "too little", "diet"),
                     bias=2))
ENTRIES.append(entry("the-first-fortnight",
                     (("baby", "babies", "newborn", "newborns", "born", "birth", "gave birth"),
                      ("last week", "yesterday", "days old", "weeks old", "day old", "week old",
                       "first week", "first fortnight", "first few weeks", "what happens",
                       "what now", "next", "just had", "born on", "born this", "born a week",
                       "just born", "new arrival")),
                     _THE_FIRST_FORTNIGHT,
                     guard=_the_line_is_the_news,
                     avoid=_NOT_THE_FORTNIGHT + ("month old", "months old", "years old",
                                                 "does nothing", "doesnt help", "does not help",
                                                 "wont help", "won't help", "night feeds on my own",
                                                 "no help at night"),
                     bias=1))
