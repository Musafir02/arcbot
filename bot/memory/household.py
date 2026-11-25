import re

from ..compose import pick
from . import counts

WHO_LIVES = re.compile(
    r"\bwho (?:else )?(?:lives|live|living|is living) (?:with (?:you|u|us|me)|there|here|at home)\b"
    r"|\bwho (?:do|does) (?:you|u) live with\b|\bwho am i living with\b"
    r"|\bwho (?:do|did) i live with\b"
    r"|\banyone (?:else )?(?:live|living|lives) (?:with (?:you|u|us|me)|there|here|at home)\b"
    r"|\banybody (?:else )?(?:live|living|lives) (?:with (?:you|u|us|me)|there|here)\b"
    r"|\bdoes anyone (?:else )?live with (?:you|u)\b"
    r"|\bwho(?:'s| is| s) (?:at home|there with you|living there)\b"
    r"|\bwho else is (?:at home|there)\b"
    r"|\bhow many of (?:you|us) (?:are|is) there\b", re.I)

JUST_ME_AND = re.compile(
    r"^(?:well |ok |okay |so |and )*(?:its |it's |it is )?(?:just |only )?"
    r"(?:me|us) (?:and|&) (?:my |our )?(?P<who>[a-z]+(?: [a-z]+)?)"
    r"(?: and (?:my |our )?(?P<more>[a-z]+(?: [a-z]+)?))?"
    r"(?: at home| living here| here)?$", re.I)
JUST_ME = re.compile(
    r"^(?:well |ok |okay |so |and )*(?:its |it's |it is )?(?:just |only )?"
    r"(?:me|the two of us|the three of us|us)(?: at home| here| on my own)?$", re.I)
ON_MY_OWN = re.compile(
    r"\bi (?:live|am living|'m living|m living) (?:on my own|by myself|alone)\b"
    r"|\bi (?:live|'m|am) (?:on my own|by myself)\b|\bliving alone\b", re.I)

SHOULD_I_MORE = re.compile(
    r"\bshould i\s+(?:\w+\s+){0,2}(?:more|more often|again|every day|every week)\b", re.I)

YES_AND_NO = re.compile(
    r"(?:yes|yeah|yep|yup|she does|he does|they do|she lives alone|he lives alone"
    r"|no|nope|not really|she doesnt|she doesn't|he doesnt|he doesn't|they dont|they don't"
    r"|she isnt|she isn't|he isnt|he isn't|they arent|they aren't)\b", re.I)

THEIR_HOUSE_ASK = re.compile(
    r"\b(?:does|do|is|are)\s+(?P<who>she|he|they|your\s+[a-z]+)(?:\s+still)?\s+"
    r"(?:live|living|be\s+living)\b[^?]*?\b"
    r"(?:alone|on\s+(?:her|his|their)\s+own|by\s+(?:her|him|their)self)\b"
    r"|\b(?:is|are)\s+(?P<who2>she|he|they|your\s+[a-z]+)(?:\s+still)?\s+"
    r"(?:on\s+(?:her|his|their)\s+own|alone|by\s+(?:her|him|their)self)\b", re.I)

THEIR_ALONE_SAID = re.compile(
    r"\bmy (?P<who>mum|mom|mam|dad|father|mother|gran|granny|nan|nana|grandma|grandad|grandpa|"
    r"sister|brother|aunt|uncle|cousin|friend|neighbour|neighbor|wife|husband|partner)\s+"
    r"(?:lives|living|is living|'s living|s living)\s+"
    r"(?:on (?:her|his|their) own|alone|by (?:her|him|their)self)\b", re.I)

THEIR_HOUSE_WHO = re.compile(
    r"\bwho (?:does|do) (?P<who>she|he|they|your\s+[a-z]+)(?:\s+actually)?\s+live with\b"
    r"|\bwho (?:is|'s|s) (?P<who2>she|he|they|your\s+[a-z]+) living with\b"
    r"|\b(?:does|do) (?:anyone|anybody|someone|somebody)(?:\s+else)?\s+live with "
    r"(?P<who3>her|him|them)\b", re.I)

THEIR = "{who}"

WITH_SOMEONE = (
    "As far as you've told me, it's you and {who}.",
    "You and {who} \u2014 that's who you've mentioned.",
    "Just you and {who}, the way you told me.",
)
ALONE = (
    "On your own, you told me.",
    "Just you, then \u2014 I'm glad of the company.",
    "You live on your own, as far as I know.",
)
NOT_SAID = (
    "You haven't said who lives with you \u2014 who's there?",
    "I don't know that yet. Who do you live with?",
)

THEIR_HOUSE = (
    "Just you and {who}, then \u2014 noted.",
    "You and {who}, then. What's an average evening like there?",
    "{Who} and you, then \u2014 that's the household.",
)

THEIRS_NOT_SAID = (
    "I can't tell from here \u2014 but if {who} is living alone, a standing call or visit beats "
    "a one-off grand gesture.",
    "You'd know better than me. If {who} is living alone and it's getting harder, the council's "
    "free needs assessment is the first thing to ask about.",
    "I don't know that one. If you're worried about {who} living alone, it's the small regular "
    "contact that helps most.",
)
THEIRS_NOT_SAID_WHO = (
    "I don't know \u2014 you haven't told me who lives with {who}.",
    "Not something you've said. If it's company for {who} you're wondering about, a weekly class "
    "or club is the usual way in.",
)

SHOULD_MORE = (
    "Little and often beats long and rare: a short call on the same day each week is easier to "
    "keep than a long one whenever there is time, and it is the one that gets counted on.",
    "Yes \u2014 the regular short one does more than the long catch-up. Put it in the diary for the "
    "same day each week and let it be dull; dull is what makes it last.",
)

THEN_ALONE = (
    "Then a standing time to ring {who} is worth more than a long catch-up now and then \u2014 "
    "the same day each week, ten minutes, and it becomes a fixture rather than a good intention.",
    "That is the hard part, the ordinary week on their own. A short call at the same time each "
    "week does more than a long one whenever it can be fitted in.",
)

THEN_NOT_ALONE = (
    "That is good \u2014 then it is the ordinary days that want the visits rather than the "
    "occasions, and a standing one is the easiest kind to keep.",
    "Good. Then what helps most is turning up on a dull Tuesday rather than a birthday \u2014 "
    "the ordinary days are the ones that get long.",
)

THEIRS_WITH = (
    "You said so yourself \u2014 someone lives with {who}.",
    "You told me \u2014 {who} has company.",
)

THEIRS_ALONE = (
    "You told me \u2014 {who} lives alone.",
    "You said so yourself: {who} lives alone.",
)


def _who_said(who):
    said = " ".join(str(who or "").split()).strip().lower()
    if not said:
        return ""
    return "your " + said


def _who_asked(who, memory):
    said = " ".join(str(who or "").split()).strip().lower()
    if said.startswith("your "):
        return said, said[5:]
    held = memory.get("others") if isinstance(memory, dict) else None
    if isinstance(held, list):
        for person in reversed(held):
            name = person.get("who") if isinstance(person, dict) else None
            if isinstance(name, str) and name.strip():
                name = name.strip().lower()
                return "your " + name, name
    alone = _their_households(memory)
    if len(alone) == 1:
        only = next(iter(alone))
        return "your " + str(only), str(only)
    return said, ""


_OBJECTS = {"she": "her", "he": "him", "they": "them"}


def _who_held(who, key):
    return who if key else _OBJECTS.get(who, who)


THE_ANSWER_ASKED = re.compile(
    r"\b(?:does|do|is|are) (?P<who>she|he|they|your\s+[a-z]+)(?:\s+still)?\s+"
    r"(?:live|living|alone|on (?:her|his|their) own)\b", re.I)


def _the_ask_it_answers(said, memory):
    if not YES_AND_NO.match(said):
        return None
    turns = memory.get("turns") or []
    last = turns[-1] if turns and isinstance(turns[-1], dict) else {}
    asked = memory.get("household_asked")
    if (isinstance(asked, dict) and asked.get("ask") == "alone"
            and last.get("module") == "household"):
        return asked
    found = THE_ANSWER_ASKED.search(last.get("bot") or "")
    if not found:
        return None
    who, key = _who_asked(found.group("who"), memory)
    return {"who": who, "key": key, "ask": "alone"}


def _their_households(memory):
    held = memory.get("their_households") if isinstance(memory, dict) else None
    return held if isinstance(held, dict) else {}


def _held(memory):
    held = memory.get("household") if isinstance(memory, dict) else None
    if not isinstance(held, dict):
        return None
    people = [person for person in held.get("people") or [] if isinstance(person, str) and person]
    if not people and not held.get("alone"):
        return None
    return {"people": people, "alone": bool(held.get("alone"))}


def observe(text, memory):
    if not isinstance(text, str) or not isinstance(memory, dict):
        return
    said = " ".join(text.lower().split()).strip(" .!,")
    if not said:
        return
    for theirs in THEIR_ALONE_SAID.finditer(said):
        kept = memory.setdefault("their_households", {})
        if isinstance(kept, dict):
            kept[theirs.group("who").lower()] = True
    if ON_MY_OWN.search(said):
        memory["household"] = {"people": [], "alone": True, "said": said}
        return
    found = JUST_ME_AND.match(said)
    if found:
        people = [_who_said(found.group("who"))]
        more = found.group("more")
        if more:
            second = _who_said(more)
            if second and second not in people:
                people.append(second)
        memory["household"] = {"people": people, "alone": False, "said": said}
        return
    if JUST_ME.match(said):
        memory["household"] = {"people": [], "alone": True, "said": said}


def answer(text, memory):
    if not isinstance(text, str) or not isinstance(memory, dict):
        return None
    said = " ".join(text.lower().split()).strip(" .!,")
    if not said:
        return None
    asked = _the_ask_it_answers(said, memory)
    if asked:
        memory.pop("household_asked", None)
        yes = not (said.startswith(("no", "nope", "not"))
                   or " doesnt" in said or " doesn't" in said or " dont" in said
                   or " don't" in said or " isnt" in said or " isn't" in said
                   or " arent" in said or " aren't" in said)
        kept = memory.setdefault("their_households", {})
        if isinstance(kept, dict) and asked.get("key"):
            kept[asked["key"]] = yes
        who = _who_held(asked.get("who") or "them", asked.get("key") or "")
        return pick(THEN_ALONE if yes else THEN_NOT_ALONE, memory,
                    seed_text=text).format(who=who)
    if SHOULD_I_MORE.search(said):
        turns = memory.get("turns") or []
        last = turns[-1] if turns and isinstance(turns[-1], dict) else {}
        if last.get("module") == "household":
            return pick(SHOULD_MORE, memory, seed_text=text)
    found = THEIR_HOUSE_WHO.search(said)
    if found:
        named = found.group("who") or found.group("who2")
        if named:
            who, key = _who_asked(named, memory)
            them = _who_held(who, key)
        else:
            them = found.group("who3")
        memory["household_asked"] = {"who": who if named else them,
                                     "key": key if named else "",
                                     "ask": "who"}
        return pick(THEIRS_NOT_SAID_WHO, memory, seed_text=text).format(who=them)
    found = THEIR_HOUSE_ASK.search(said)
    if found:
        who, key = _who_asked(found.group("who") or found.group("who2") or "", memory)
        held = _their_households(memory).get(key) if key else None
        if held is True:
            return pick(THEIRS_ALONE, memory, seed_text=text).format(who=who)
        if held is False:
            return pick(THEIRS_WITH, memory,
                        seed_text=text).format(who=_who_held(who, key))
        memory["household_asked"] = {"who": who, "key": key, "ask": "alone"}
        return pick(THEIRS_NOT_SAID, memory, seed_text=text).format(who=who)
    if WHO_LIVES.search(said):
        held = _held(memory)
        if held is None:
            if counts.answer(said, memory):
                return None
            return pick(NOT_SAID, memory, seed_text=text)
        if held["alone"]:
            return pick(ALONE, memory, seed_text=text)
        people = held["people"]
        if len(people) == 1:
            who = people[0]
        elif len(people) == 2:
            who = people[0] + " and " + people[1]
        else:
            who = ", ".join(people[:-1]) + " and " + people[-1]
        return pick(WITH_SOMEONE, memory, seed_text=text).format(who=who)
    found = JUST_ME_AND.match(said) or JUST_ME.match(said)
    if found and not (found.groupdict().get("who") or ""):
        return None
    if found:
        who = _who_said(found.groupdict().get("who"))
        if not who:
            return None
        return pick(THEIR_HOUSE, memory, seed_text=text).format(
            who=who, Who=who[:1].upper() + who[1:])
    return None


def takes_as_it_comes(text, memory):
    if not isinstance(text, str):
        return False
    said = " ".join(text.lower().split()).strip(" .!,")
    if WHO_LIVES.search(said):
        return not counts.answer(said, memory)
    if THEIR_HOUSE_ASK.search(said) or THEIR_HOUSE_WHO.search(said):
        return True
    if _the_ask_it_answers(said, memory):
        return True
    if SHOULD_I_MORE.search(said):
        turns = memory.get("turns") or []
        last = turns[-1] if turns and isinstance(turns[-1], dict) else {}
        return last.get("module") == "household"
    found = JUST_ME_AND.match(said) or JUST_ME.match(said)
    return bool(found) and bool(found.groupdict().get("who"))
