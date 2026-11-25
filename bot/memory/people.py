import re

HIM = frozenset("""son dad father daddy papa husband brother nephew grandad grandpa granddad
grandfather stepdad stepson uncle boyfriend fiance grandson godson""".split())
HER = frozenset("""daughter mum mom mam mummy mumma mother wife sister niece nan nana gran
granny grandma grandmother stepmum stepdaughter aunt auntie girlfriend fiancee granddaughter
goddaughter""".split())

HIM_SAID = re.compile(r"\b(?:him|his|he)\b", re.I)
HER_SAID = re.compile(r"\b(?:her|hers|she)\b", re.I)
THEM_SAID = re.compile(r"\b(?:them|they|theirs|their)\b", re.I)


def _the_age_of_the_group(memory):
    theirs = memory.get("their_age") if isinstance(memory, dict) else None
    if isinstance(theirs, dict):
        age = theirs.get("age")
        if isinstance(age, int) and 0 < age < 120:
            return age
    return None


def _with_an_age(record):
    if not isinstance(record, dict):
        return False
    if isinstance(record.get("age"), int) and record.get("age") > 0:
        return True
    return any(isinstance(age, int) and age > 0 for age in record.get("ages") or ())


def _age(record):
    if isinstance(record.get("age"), int):
        return record["age"]
    for age in record.get("ages") or ():
        if isinstance(age, int):
            return age
    return None


def a_person_with_an_age(memory, understood=None):
    from . import others
    from .topics import person

    reading = understood if isinstance(understood, dict) else {}
    line = str(reading.get("clean") or reading.get("text") or "")
    people = [one for one in others(memory) if isinstance(one, dict) and one.get("who")]
    if not people:
        return _the_group_record(memory, line)
    named = person(line)
    if named:
        for one in people:
            if str(one.get("who") or "").lower() == named and _with_an_age(one):
                return one
    if named:
        return None
    said_him = bool(HIM_SAID.search(line))
    said_her = bool(HER_SAID.search(line))
    if said_him == said_her and THEM_SAID.search(line):
        return _the_ones_a_them_points_at(people)
    if said_him == said_her:
        return _the_group_record(memory, line)
    wanted = HIM if said_him else HER
    found = [one for one in people
             if str(one.get("who") or "").lower() in wanted and _with_an_age(one)]
    if len(found) != 1:
        return None
    return found[0]


def _the_group_record(memory, line):
    if not THEM_SAID.search(line or ""):
        return None
    age = _the_age_of_the_group(memory)
    if not age:
        return None
    return {"who": "them", "age": age}


def _the_ones_a_them_points_at(people):
    with_an_age = [one for one in people if _with_an_age(one)]
    if not with_an_age:
        return None
    ages = {_age(one) for one in with_an_age}
    if len(ages) != 1:
        return None
    return with_an_age[0]


CHILD_OF_THE_FAMILY = frozenset("""son daughter grandson granddaughter nephew niece stepson
    stepdaughter grandchild""".split())


def the_people(memory):
    from . import others

    found = [one for one in others(memory) if isinstance(one, dict) and one.get("who")]
    one = memory.get("person") if isinstance(memory, dict) else None
    if isinstance(one, dict) and one.get("who") and one not in found:
        found.append(one)
    return found


def a_child_the_chat_is_about(memory, understood=None):
    from .topics import person

    reading = understood if isinstance(understood, dict) else {}
    line = str(reading.get("clean") or reading.get("text") or "")
    people = the_people(memory)
    named = person(line)
    if named:
        if named not in CHILD_OF_THE_FAMILY:
            return False
        for one in people:
            if str(one.get("who") or "").lower() != named:
                continue
            age = _age(one)
            if age is not None and age >= 18:
                return False
        return True
    said_him = bool(HIM_SAID.search(line))
    said_her = bool(HER_SAID.search(line))
    wanted = HIM if said_him and not said_her else HER if said_her and not said_him else None
    ages = {}
    for one in people:
        who = str(one.get("who") or "").lower()
        age = _age(one)
        if age is not None:
            ages[who] = age
    if wanted is not None:
        of_that_kind = {str(one.get("who") or "").lower() for one in people
                        if str(one.get("who") or "").lower() in wanted}
        if len(of_that_kind) > 1:
            return False
    for one in people:
        who = str(one.get("who") or "").lower()
        if who not in CHILD_OF_THE_FAMILY:
            continue
        if wanted is not None and who not in wanted:
            continue
        age = ages.get(who)
        if age is not None and age >= 18:
            continue
        return True
    return False


def the_age_of_the_person_they_mean(memory, understood=None):
    found = a_person_with_an_age(memory, understood)
    if found:
        return _age(found)
    reading = understood if isinstance(understood, dict) else {}
    line = str(reading.get("clean") or reading.get("text") or "")
    if not THEM_SAID.search(line) or HIM_SAID.search(line) or HER_SAID.search(line):
        return None
    held = memory.get("their_age") if isinstance(memory, dict) else None
    if isinstance(held, dict) and _with_an_age(held):
        return _age(held)
    return None
