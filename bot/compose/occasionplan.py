import random
import re

_DAY_TO_COME = re.compile(
    r"\b(?:on\s+)?(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday|"
    r"tonight|tomorrow|today|this weekend|this saturday|the weekend|"
    r"next week|next weekend|next month|next year|"
    r"in \d+ (?:days?|weeks?|months?)|"
    r"\d{1,2}(?:st|nd|rd|th)? (?:of )?(?:january|february|march|april|may|june|july|august|"
    r"september|october|november|december)|"
    r"(?:january|february|march|april|may|june|july|august|september|october|november|"
    r"december)(?: \d{1,2}(?:st|nd|rd|th)?)?|"
    r"(?:on )?the \d{1,2}(?:st|nd|rd|th))\b")

_ASKS_FOR_A_PLAN = re.compile(
    r"\b(?:plan|plans|planning|arrange|arranging|organi[sz]e|organi[sz]ing|ideas?|"
    r"something|anything|celebrate|throw (?:her|him|them|a)|do (?:for|to mark))\b|"
    r"\b(?:what|how) (?:should|shall|can|could) (?:we|i) do\b|\bwhat do (?:we|i) do\b")

_OWN_SUBJECT = re.compile(
    r"\b(?:diet|workout|exercise|training|budget|money|finances?|meals?|food|tea|dinner|"
    r"lunch|breakfast|shopping|garden|shed|loft|move|moving|house|holiday|trip|route|journey|"
    r"revision|study|work|job|business|wedding|funeral|birth|baby|contract|rota|shift|"
    r"packing|pack|list|calendar|week|month|year|term)\b")

_NOT_A_PLAN_ASK = re.compile(
    r"\b(?:what day|which day|when is|when's|where is|where's|how old|what time|who is|"
    r"how much|how many|why|what do you mean|what did you mean)\b"
    r"|\bwould (?:actually |really )?(?:like|love|enjoy|prefer|want)\b")

PLANS = (
    "For {day}, book the one thing that needs a table or a ticket, because "
    "everything else on the night can be decided on the spot. Then send the time and place to "
    "everyone you want there today, so nobody is left waiting to hear.",
    "Get one firm thing in the diary for {day} first - a table for the group at "
    "seven, or tickets - and keep the rest of it loose. Send the details round today; a birthday "
    "falls apart at the 'so what are we doing' stage, not on the night.",
    "The thing that makes {day} work is one booking with a time on it: a table at "
    "seven, then somewhere with music after. Text the people you want there today with both, and "
    "ask them who else they would want in the group.",
    "For {day}, put a time on it and tell people today: a table booked for seven, "
    "and a second place to go after that needs no booking. Ask what they would actually like to "
    "eat first, so the booking is somewhere they want rather than somewhere free.",
)

CHILD_PLANS = (
    "For {day}, book the thing that fills up first - a hall, a soft play slot, a "
    "bowling lane - and send the invitations the same day, because a children's party is decided "
    "by who can come. Order the cake when you book, so it is not the thing left to Friday.",
    "Get the slot booked for {day} before you think about anything else: the "
    "weekend ones go first. Then ask them which two friends matter most, invite those and a few "
    "more, and keep it to two hours - that is as long as a party that size lasts.",
    "For {day}, one booked place and a short guest list beats a big plan: a hall or "
    "a soft play slot for two hours, food that is easy to hand round, and a cake ordered today. "
    "Ask the parents to stay if the children are small.",
)

_SOON = re.compile(r"\b(?:tonight|tomorrow|today|this weekend|this saturday|in \d+ days?)\b")
SOON_PLANS = (
    "It is close, so keep it small and certain for {day}: book a table for the "
    "people who can actually come, tell them the time today, and let the rest be drinks after. "
    "A short-notice birthday works on who turns up, not on the plan.",
    "For {day}, ring the place rather than booking online - a table for six at "
    "short notice is usually a phone call - and send one message with the time and the address "
    "to everyone today.",
)


def _ordinal(age):
    if 10 <= age % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(age % 10, "th")
    return "%d%s" % (age, suffix)


def _whose(who):
    who = str(who or "").strip()
    if not who:
        return ""
    low = who.lower()
    if low.startswith(("your ", "my ")):
        low = low.split(" ", 1)[1]
    if who[:1].isupper():
        return who + "'s"
    return "your " + low + ("'" if low.endswith("s") else "'s")


_A_MONTH_ON_ITS_OWN = re.compile(
    r"january|february|march|april|may|june|july|august|september|october|november|december")

_BIRTHDAY_IN_PLAN = re.compile(
    r"\b(?:birthday|bday|turning|turns?|\d{1,2}\s*-?\s*(?:this|next)\s*(?:month|week|year))\b"
    r"|\b(?:i'?m|im|i am) (?:\d{1,2}|turning \d{1,2})\b|\bmy \d{1,2}(?:st|nd|rd|th)\b")

_TURNS_AGE = re.compile(r"\bturns? (\d{1,2})\b|\bturning (\d{1,2})\b"
                        r"|\bmy (\d{1,2})(?:st|nd|rd|th)\b"
                        r"|\b(\d{1,2})(?:st|nd|rd|th)\s+(?:birthday|bday)\b")


def _the_day(when):
    when = " ".join(str(when or "").lower().split())
    found = _DAY_TO_COME.search(when)
    if not found:
        return ""
    phrase = _DAY_SAID.sub(_cap, found.group(0).strip())
    if _A_MONTH_ON_ITS_OWN.fullmatch(phrase.lower()):
        return "in " + phrase
    if not phrase.startswith(("on ", "in ", "next ", "this ", "the ", "tomorrow", "tonight",
                              "today", "monday", "tuesday", "wednesday", "thursday", "friday",
                              "saturday", "sunday")):
        phrase = "on " + phrase
    return phrase


def _the_age(text):
    found = _TURNS_AGE.search(text or "")
    if not found:
        return None
    for group in found.groups():
        if group:
            age = int(group)
            if 1 < age < 120:
                return age
    return None


_STILL_TALKING_ABOUT = 6


def _said_how_long_ago(memory, who=None, markers=""):
    turns = memory.get("turns") if isinstance(memory.get("turns"), list) else []
    now = len(turns) - 1
    best = None
    for entry in memory.get("facts_log") or []:
        if not isinstance(entry, dict) or not isinstance(entry.get("turn"), int):
            continue
        value, text = entry.get("value"), str(entry.get("text") or "")
        if who is not None:
            if entry.get("key") != "other" or not isinstance(value, dict):
                continue
            if str(value.get("who") or "").lower() != str(who).lower():
                continue
        else:
            if entry.get("key") not in ("plan", "plans", "other", "people", "birthday"):
                continue
            if markers and not markers.search(text.lower()):
                continue
        gap = now - entry["turn"]
        best = gap if best is None else min(best, gap)
    return best


RELATIONS = frozenset((
    "mum", "mom", "mam", "mother", "dad", "father", "son", "daughter", "boy", "girl", "baby",
    "kid", "child", "husband", "wife", "partner", "boyfriend", "girlfriend", "sister", "brother",
    "friend", "mate", "nephew", "niece", "cousin", "aunt", "auntie", "uncle", "nan", "granny",
    "gran", "grandma", "grandad", "grandpa", "boss", "colleague", "neighbour", "neighbor",
    "flatmate", "housemate", "lass", "lad", "fella", "eldest", "youngest", "twins",
))

_SPOKEN_FOR = {"half": "partner", "one": "child"}

_MINE_BEFORE_THE_DAY = re.compile(
    r"\bmy\s+(?:[a-z]{2,12}\s+){0,2}"
    r"(?P<who>(?!(?:is|are|was|will|turns?|turning)\b)[a-z]{2,12})(?:'s|s)?\s+"
    r"(?:(?:is|are)\s+)?(?:\d{1,2}(?:st|nd|rd|th)\s+)?"
    r"(?:birthday|bday|turns?\b|turning\b)")

_A_POSSESSIVE_BEFORE_THE_DAY = re.compile(
    r"\b(?P<who>[a-z]{2,12})(?:'s|s)\s+(?:\d{1,2}(?:st|nd|rd|th)\s+)?(?:birthday|bday|turns?\b)")

_A_NAME_BEFORE_THE_DAY = re.compile(
    r"\bmy\s+[a-z]{2,12}(?:'s|s)?\b[^.!?]{0,24}\b"
    r"(?:birthday|bday|turn(?:s|ing)?\s+\d{1,2}\b)")

_SOMEONE_ELSES_DAY = re.compile(r"\b(?:his|her|their|its)\s+(?:birthday|bday)\b")


def _the_person(said):
    low = " ".join(str(said or "").lower().replace("\u2019", "'").split())
    if _SOMEONE_ELSES_DAY.search(low):
        return ""
    for shape in (_MINE_BEFORE_THE_DAY, _A_POSSESSIVE_BEFORE_THE_DAY):
        found = shape.search(low)
        if not found:
            continue
        who = found.group("who").strip("'")
        if who in _SPOKEN_FOR:
            return _SPOKEN_FOR[who]
        if who in RELATIONS:
            return who
        if who.endswith("'s") and who[:-2] in RELATIONS:
            return who[:-2]
        if who.endswith("s") and who[:-1] in RELATIONS:
            return who[:-1]
        return "" if _A_NAME_BEFORE_THE_DAY.search(low) else None
    return "" if _A_NAME_BEFORE_THE_DAY.search(low) else None


def _the_recent_age(memory, upto=6):
    ages, turns = set(), 0
    for last in reversed(memory.get("turns") or []):
        if not isinstance(last, dict):
            continue
        turns += 1
        if turns > upto:
            break
        text = str(last.get("user") or "").lower()
        for found in _TURNS_AGE.finditer(text):
            age = next((g for g in found.groups() if g), "")
            if age:
                ages.add(int(age))
    if len(ages) == 1:
        age = ages.pop()
        if 1 < age < 120:
            return age
    return None


def _the_occasion(memory):
    if not isinstance(memory, dict):
        return None
    told = ""
    for last in reversed(memory.get("turns") or []):
        if isinstance(last, dict) and last.get("user"):
            told = str(last.get("user"))
            break
    met = []
    for one in memory.get("others") or []:
        if not isinstance(one, dict) or one.get("pronoun"):
            continue
        who = one.get("who") or _the_person(told)
        if not who:
            continue
        age, when = one.get("age"), _the_day(one.get("turns"))
        if not when:
            birthday = str(one.get("birthday") or "")
            when = _the_day(birthday)
            if when:
                age = _the_age(birthday)
        if not when:
            continue
        if isinstance(age, bool) or not isinstance(age, int) or not 1 < age < 120:
            age = None
        gap = _said_how_long_ago(memory, who=who)
        if gap is not None and gap > _STILL_TALKING_ABOUT:
            continue
        met.append(("another", who, age, when))
    mine = memory.get("user") if isinstance(memory.get("user"), dict) else {}
    if not met and mine:
        plans = mine.get("plans") if isinstance(mine.get("plans"), list) else []
        said = " ".join(str(p) for p in plans[-1:]) or str(mine.get("plan") or "")
        when = _the_day(said) if _BIRTHDAY_IN_PLAN.search(said) else ""
        who = _the_person(said + " " + told) if when else None
        if when and who == "":
            return None
        if when:
            age = mine.get("age")
            if isinstance(age, bool) or not isinstance(age, int) or not 1 < age < 120:
                age = _the_age(said) or _the_recent_age(memory)
            gap = _said_how_long_ago(memory, markers=_BIRTHDAY_IN_PLAN)
            if gap is None or gap <= _STILL_TALKING_ABOUT:
                met.append(("you", who or None, age, when))
    return met[0] if len(met) == 1 else None


def _cap(match):
    return match.group(0)[:1].upper() + match.group(0)[1:]


_DAY_SAID = re.compile(
    r"\b(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday|january|february|"
    r"march|april|may|june|july|august|september|october|november|december)\b")


_ANOTHER_PERSON = re.compile(
    r"\bfor (?:my|our|his|her|their|the) (?:[a-z]+ )?(?:mum|mom|dad|father|mother|sister|brother|"
    r"wife|husband|partner|son|daughter|friend|mate|nan|gran|grandma|grandad|boss|colleague|"
    r"neighbours?|kids?|children)\b")


def _reads_as_a_plan_ask(said, memory):
    said = " ".join((said or "").lower().split())
    if not said:
        return False
    words = said.replace("?", " ").replace("!", " ").replace(".", " ").split()
    if len(words) > 10:
        return False
    if not _ASKS_FOR_A_PLAN.search(said):
        return False
    if _NOT_A_PLAN_ASK.search(said):
        return False
    subject = _OWN_SUBJECT.findall(said)
    if subject:
        return False
    if _ANOTHER_PERSON.search(said):
        return False
    return True


def takes_as_it_comes(text, memory):
    return reply_for(text, memory) is not None


def reply_for(text, memory):
    occasion = _the_occasion(memory)
    if occasion is None:
        return None
    if not _reads_as_a_plan_ask(text, memory):
        return None
    kind, who, age, when = occasion
    if kind == "you":
        whose = _whose(who) if who else "your"
    else:
        whose = _whose(who)
        if not whose:
            return None
    day = " ".join(part for part in (whose, _ordinal(age) if age else "birthday", when) if part)
    if age is not None and age < 16:
        pool = CHILD_PLANS
    elif _SOON.search(when):
        pool = SOON_PLANS
    else:
        pool = PLANS
    turns = memory.get("turns") if isinstance(memory.get("turns"), list) else []
    seed = len(turns) * 7919 + sum(ord(c) for c in " ".join(str(text or "").lower().split()))
    line = random.Random(seed).choice(pool)
    return line.replace("{day}", day)
