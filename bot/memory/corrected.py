import re
from ..memory import facts as extract
from ..memory import current, keywords, last_user, log, name, note, others, plan_line, plan_sentence, remember, remember_other, stem, user
from ..memory.store_lines import AMOUNT_WORD, AT_TIME_VALUE, CORRECTION_BACK, COUNT_WORDS, FACT_FAMILY, NOT_A_UNIT, OTHER_KIND_SAY, OTHER_SAID, PLURAL_PETS, SPELLING_APART, UNIT_FAMILY
from ..memory import plans
from ..memory.named import carries_a_name
from ..memory.relations import _animal_family, _tidy_name


OTHER_BARE_NUMBER = re.compile(r"\d{1,3}")

def _number_belongs_to_that_age(memory):
    last = str(last_user(memory) or "").strip()
    if not last:
        return True
    stated = [entry for entry in memory.get("facts_log") or []
              if isinstance(entry, dict) and entry.get("key") == "other"]
    if stated and str(stated[-1].get("text") or "").strip() == last:
        return True
    fixed = memory.get("correction") or {}
    if isinstance(fixed, dict) and str(fixed.get("said") or "").strip() == last:
        said = str(fixed.get("line") or "")
        if said and (extract.extract(said).get("others") or []):
            return True
    return bool(_asks(last))

def _a_name_for_a_person(value):
    word = " ".join(str(value or "").split())
    low = word.lower()
    if not word or low in extract.MONTHS or low in extract.DAYS:
        return False
    if extract._not_a_name(word, strict_ly=False):
        return False
    if low in extract.NAMES_THAT_END_LIKE_A_VERB:
        return True
    return not low.endswith(extract.NOT_NAME_ENDING)

def _a_new_name_was_said(target, text):
    word = " ".join(str(target or "").split())
    if not word:
        return False
    if carries_a_name(text) or _denies_and_names(text):
        return True
    parts = word.split()
    if len(parts) == 2 and _a_word_of_a_name(parts[0]) and extract.a_name_could_be(parts[1]):
        return True
    return extract.a_name_could_be(word)

def _a_word_of_a_name(word):
    low = str(word or "").strip(".").strip().lower()
    if low in extract.TITLE_WORDS:
        return True
    return extract.a_name_could_be(low)

def _denies_and_names(text):
    if extract.a_name_is_taken_back(text):
        return False
    denial = extract.DENIAL_OF_A_VALUE.match(str(text or "").strip())
    return bool(denial and denial.group("says") and denial.group("value"))

def _correct_other(memory, target, text=""):
    known = [entry for entry in others(memory)
             if isinstance(entry, dict) and entry.get("who")]
    if not known:
        return None
    number = OTHER_BARE_NUMBER.match(str(target or "").strip())
    if number and not _number_belongs_to_that_age(memory):
        return None
    if number:
        for entry in reversed(known):
            if not isinstance(entry.get("age"), int):
                continue
            who = str(entry.get("who") or "").strip()
            age = int(number.group(0))
            if not who or not 0 <= age <= 120:
                return None
            remember_other(memory, {"who": who, "age": age})
            return {"line": "my %s is %d" % (who, age),
                    "note": "%d \u2014 got it, your %s is %d from now on." % (age, who, age)}
        return None
    for entry in reversed(known):
        who = str(entry.get("who") or "").strip()
        if not who:
            continue
        kept = [kind for kind, _ in OTHER_SAID if entry.get(kind)]
        for kind, saying in OTHER_SAID:
            if kept and kind not in kept:
                continue
            if kind == "name" and (not _a_name_for_a_person(target)
                                   or not _a_new_name_was_said(target, text)):
                continue
            line = "my %s %s %s" % (who, saying, target)
            found = extract.extract(line)
            mine = [item for item in (found.get("others") or [])
                    if isinstance(item, dict)
                    and str(item.get("who") or "").lower() == who.lower()]
            if not any(item.get(kind) for item in mine):
                continue
            entry.pop(kind, None)
            for item in mine:
                remember_other(memory, item, line)
            shown = str(target)[:1].upper() + str(target)[1:]
            shape = OTHER_KIND_SAY.get(kind, "{v} it is, then.")
            return {"line": line, "note": shape.format(v=shown, who=who)}

MADE_OF_A_VALUE = re.compile(
    r"^(?:[\u00a3$\u20ac]?\s?\d"
    r"|the\s+\d{1,2}(?:st|nd|rd|th)"
    r"|\d{1,2}(?::\d{2})?\s*(?:am|pm)"
    r"|(?:next\s+|this\s+|on\s+|until\s+|till\s+)?(?:mon|tues|wednes|thurs|fri|satur|sun)day"
    r"|(?:next\s+|this\s+|in\s+)?(?:january|february|march|april|may|june|july|august"
    r"|september|october|november|december))", re.I)

def _make_corrects(target, memory):
    if MADE_OF_A_VALUE.match(str(target or "").strip()):
        return True
    return bool(extract.extract(last_user(memory) or ""))

A_UNIT_SAID = re.compile(r"(?<![\w.])\d[\d,]*(?:\.\d+)?\s*([a-z]+)", re.I)

def _the_unit(text):
    match = A_UNIT_SAID.search(str(text or "").lower())
    if not match:
        return ""
    return UNIT_FAMILY.get(match.group(1), "")

def _stated_families(before):
    families = set()
    unit = _the_unit(before)
    if unit:
        families.add(unit)
    try:
        found = extract.extract(before or "")
    except Exception:
        found = {}
    for key in found if isinstance(found, dict) else ():
        family = FACT_FAMILY.get(key)
        if family:
            families.add(family)
    return families

def _measured_the_same(value, before):
    family = _the_unit(value)
    if not family:
        return True
    if any(_date_said(str(value or "").lower())):
        return True
    return family in _stated_families(before)

NAMING_VERB = re.compile(r"^(?:(?:called|named)\s+"
                         r"|(?:he|she|it|they)(?:'s|s|\s+is|\s+was|\s+are)\s+"
                         r"(?:(?:called|named)\s+)?)(?=\S)", re.I)

def _without_the_naming_verb(value):
    said = str(value or "").strip()
    fixed = NAMING_VERB.sub("", said)
    if fixed == said:
        return said
    return fixed[:1].upper() + fixed[1:]

def _the_plan_on_the_table(memory):
    if not isinstance(memory, dict):
        return None
    for key in ("plan",):
        value = (memory.get("user") or {}).get(key)
        if isinstance(value, str) and value.strip():
            return value
    for value in (memory.get("user") or {}).get("plans") or ():
        if isinstance(value, str) and value.strip():
            return value
    return None

def _the_plan_before(memory, plan_after):
    after = " ".join(str(plan_after or "").lower().split())
    for entry in reversed([e for e in (memory.get("facts_log") or ()) if isinstance(e, dict)]):
        if entry.get("key") not in ("plan", "plans"):
            continue
        value = entry.get("value")
        if not isinstance(value, str) or not value.strip():
            continue
        if " ".join(value.lower().split()) != after:
            return value
    return None

def _what_took_its_place(before, after, value):
    before = " ".join(str(before or "").lower().split())
    after = " ".join(str(after or "").lower().split())
    value = " ".join(str(value or "").lower().split())
    if not value or not before or not after or value not in before:
        return None
    start = before.index(value)
    end = start + len(value)
    head = 0
    while head < min(len(before), len(after)) and before[head] == after[head]:
        head += 1
    tail = 0
    while (tail < min(len(before), len(after)) - head
           and before[len(before) - 1 - tail] == after[len(after) - 1 - tail]):
        tail += 1
    change_start, change_end = head, len(before) - tail
    if change_end <= start or change_start >= end:
        return None
    kept_head = before[start:min(change_start, end)]
    kept_tail = before[max(change_end, start):end] if change_end < end else ""
    new_middle = after[change_start:max(change_start, len(after) - tail)]
    fixed = (kept_head + new_middle + kept_tail).strip()
    return fixed or None

NOT_A_FACT_OF_THEIRS = frozenset("""who pronoun names name""".split())

A_DAY_SAID_LONG = re.compile(r"^(?:the\s+)?(\d{1,2}(?:st|nd|rd|th)?)\s+(?:of\s+)?([a-z]+)$",
                             re.I)

def _a_day_written_the_way_the_store_writes_it(fact):
    text = " ".join(str(fact or "").split())
    found = A_DAY_SAID_LONG.match(text)
    if not found:
        return text
    return "%s %s" % (found.group(1), found.group(2))

def _the_person_the_plan_is_about(memory, correction, before=None):
    plan_after = correction.get("value") if isinstance(correction, dict) else None
    if not before:
        before = _the_plan_before(memory, plan_after)
    if not before:
        return 0
    sentence = str(correction.get("sentence") or "").strip()
    moved = 0
    for entry in others(memory) or ():
        if not isinstance(entry, dict):
            continue
        who = str(entry.get("who") or entry.get("pronoun") or entry.get("name") or "").strip()
        if not who or not re.search(r"\b" + re.escape(who.lower()) + r"\w*\b", before):
            continue
        if plan_after and not re.search(r"\b" + re.escape(who.lower()) + r"\w*\b",
                                       str(plan_after).lower()):
            continue
        for key, value in list(entry.items()):
            if key in NOT_A_FACT_OF_THEIRS:
                continue
            said = value if isinstance(value, str) else ""
            taken = _what_took_its_place(before, plan_after, said)
            if not taken or taken == " ".join(said.lower().split()):
                continue
            taken = _a_day_written_the_way_the_store_writes_it(taken)
            entry[key] = taken
            kept = {("who" if entry.get("who") else "pronoun"):
                    entry.get("who") or entry.get("pronoun"), key: taken}
            log(memory).append({"key": "other", "value": kept,
                                "turn": len(memory.get("turns") or []),
                                "text": sentence or " ".join(str(plan_after or "").split())})
            moved += 1
    return moved

def _a_correction_is_not_a_plan(memory, text):
    said = " ".join(str(text or "").lower().split())
    if not said:
        return
    body = " ".join(extract.CORRECTION_LEAD_RE.sub("", said).split())
    known = user(memory)
    plans = known.get("plans")
    if not isinstance(plans, list):
        return
    kept = [one for one in plans
            if " ".join(str(one).lower().split()) not in (said, body)]
    if len(kept) != len(plans):
        known["plans"] = kept


def _a_value_already_the_plans(memory, target, text=""):
    said = str(target or "").strip().lower()
    if not said:
        return False
    line = " ".join(str(text or "").lower().split())
    known = user(memory)
    plans = [p for p in (known.get("plans") or []) if isinstance(p, str) and p.strip()]
    latest = known.get("plan")
    if isinstance(latest, str) and latest.strip():
        plans.append(latest)
    for one in plans:
        held = " ".join(one.lower().split())
        if line and (held in line or line in held):
            continue
        if re.search(r"\b" + re.escape(said) + r"\b", held):
            return True
    return False


def _apply_correction(memory, correction, text=""):
    target = correction.get("to") if isinstance(correction, dict) else None
    if target:
        target = _without_the_naming_verb(target)
        correction["to"] = target
    wrong = correction.get("from") if isinstance(correction, dict) else None
    if not target:
        return
    if isinstance(correction, dict) and correction.get("applied"):
        return
    if _a_value_already_the_plans(memory, target, text):
        return
    if not wrong and not _measured_the_same(target, last_user(memory) or ""):
        return
    if isinstance(correction, dict) and correction.get("make") and not _make_corrects(target, memory):
        return
    both_numbers = bool(not extract.a_clock_time(target)
                        and NUMBER_VALUE.match(str(target or "").strip() or "-")
                        and NUMBER_VALUE.match(str(wrong or "").strip() or "-"))
    plan_on_the_table = _the_plan_on_the_table(memory)
    fixed = _correct_plan(memory, target, wrong, text)
    if not fixed and not (both_numbers and _stated_plan(memory)):
        fixed = (_correct_date(memory, target, text, wrong or "")
                 or _correct_clock(memory, target, text, wrong or "")
                 or _correct_number(memory, target, text)
                 or _correct_count(memory, target, text)
                 or _correct_fact(memory, target, wrong, text)
                 or _correct_a_persons_name(memory, target, text, wrong or "")
                 or _correct_when(memory, target, text)
                 or _correct_the_count_on_the_table(memory, target, text))
    if fixed and fixed.get("from") and not wrong:
        wrong = fixed["from"]
        correction["from"] = wrong
    said = " ".join(str(text or "").lower().split())
    other = None if fixed else _correct_other(memory, target, text)
    if other:
        other["said"] = said
        other["applied"] = True
        memory["correction"] = other
    if fixed:
        if fixed.get("key") == "plan":
            _the_person_the_plan_is_about(memory, fixed, plan_on_the_table)
            _a_correction_is_not_a_plan(memory, text)
        fixed["said"] = said
        fixed["applied"] = True
        memory["correction"] = fixed
    if not fixed and not wrong:
        return
    record = current(memory)
    if not record:
        return
    text = record["text"]
    moved_off_the_topic = bool(
        fixed and fixed.get("key") == "plan" and fixed.get("from")
        and not re.search(r"\b" + re.escape(str(fixed["from"])) + r"\b", text, flags=re.I))
    if moved_off_the_topic:
        line = " ".join(str(said or text).split())
        if line:
            fresh = {"turn": len(memory.get("turns") or []), "text": line,
                     "words": keywords(line)}
            memory["topic"] = fresh
            topics = memory.get("topics")
            if not isinstance(topics, list):
                topics = memory["topics"] = []
            if not topics or topics[-1].get("text") != line:
                topics.append(fresh)
        return
    elif other:
        text = other.get("line") or text
    elif fixed and fixed.get("line"):
        text = fixed["line"]
    elif wrong and re.search(r"\b" + re.escape(wrong) + r"\b", text, flags=re.I):
        text = text + " (mean " + target + ")"
    elif fixed and fixed.get("key") == "plan" and _the_topic_with_the_new_clock(
            text, str(user(memory).get("plan") or "")):
        text = _the_topic_with_the_new_clock(text, str(user(memory).get("plan") or ""))
    elif target.lower() not in text.lower():
        text = text + " (mean " + target + ")"
    record["text"] = text
    record["words"] = keywords(text)
    before = re.sub(r"\s*\(mean [^)]*\)\s*$", "", text, flags=re.I)
    stated = (_swap_in(before, target, wrong) if wrong else None) or before
    for entry in extract.extract(stated or text).get("others") or []:
        if not set(entry) - {"who", "pronoun"}:
            continue
        fresh = entry.get("birthday")
        theirs = next((one for one in others(memory)
                       if one.get("who") == entry.get("who")), None)
        kept = " ".join(str((theirs or {}).get("birthday") or "").lower().split())
        if fresh and wrong and kept:
            hated = [part for part in re.split(r"[^a-z0-9]+", str(wrong).lower())
                     if part and part not in ("the", "of", "on", "in")]
            if hated and not any(part in kept for part in hated):
                continue
        if fresh:
            held = next((one for one in others(memory)
                         if one.get("who") == entry.get("who")), None)
            before = str((held or {}).get("birthday") or "").lower()
            month = next((name for name in extract.MONTHS if name in before), None)
            if month and not any(name in str(fresh).lower() for name in extract.MONTHS):
                entry["birthday"] = "%s %s" % (fresh, month)
        remember_other(memory, dict(entry), stated or text)
    places = user(memory).get("places")
    if isinstance(places, list) and wrong and extract.place_value(target):
        if not any(str(place).lower() == target.lower() for place in places):
            places.append(target)
    topics = memory.get("topics")
    if isinstance(topics, list) and topics and topics[-1] is not record \
            and topics[-1].get("text", "").startswith(record["text"][:10]):
        topics[-1] = record
    note(memory, text)

NUMBER_VALUE = re.compile(r"^(\d+(?:\.\d+)?)\s*([a-z]+)?$", re.I)

def _stated_plan(memory):
    said = " ".join(str(last_user(memory) or "").lower().split())
    entries = memory.get("facts_log")
    if not said or not isinstance(entries, list):
        return None
    for entry in reversed(entries):
        if not isinstance(entry, dict):
            continue
        if " ".join(str(entry.get("text") or "").lower().split()) != said:
            return None
        if entry.get("key") in ("plan", "plans"):
            value = entry.get("value")
            return value if isinstance(value, str) and value.strip() else None
        return None
    return None

def _an_amount_on_the_measure(plan, target):
    words = re.findall(r"[a-z0-9']+", str(target or "").lower())
    if len(words) < 2:
        return None
    measure = words[-1]
    stem = measure[:-1] if measure.endswith("s") and len(measure) > 3 else measure
    if len(stem) < 3:
        return None
    found = re.search(r"(?<![\w])(" + AMOUNT_WORD + r"\s+)(" + re.escape(stem)
                      + r"(?:s|es)?)(?![\w])", str(plan or ""), re.I)
    if found is None:
        return None
    before = plan[:found.start()]
    said = str(target or "").strip()
    if before.strip():
        said = said[:1].lower() + said[1:]
    return {"plan": before + said + plan[found.end():], "value": str(target).strip(),
            "in_the_sentence": said, "was": found.group(0)}

def _correct_plan(memory, target, wrong, text=""):
    plan = _stated_plan(memory)
    if plan and not wrong:
        amount = _an_amount_on_the_measure(plan, target)
        if amount:
            fixed, shown = amount["plan"], amount["value"]
            known = user(memory)
            known["plan"] = fixed
            plans = known.get("plans")
            if isinstance(plans, list):
                known["plans"] = [fixed if p == plan else p for p in plans]
            note(memory, fixed)
            origin = plan_line(memory, plan)
            if origin:
                was = amount["was"]
                origin = re.sub(r"(?<![\w])" + re.escape(was) + r"(?![\w])",
                                amount["in_the_sentence"], origin, count=1, flags=re.I)
            sentence = plan_sentence(fixed, origin)
            return {"key": "plan", "value": shown, "sentence": sentence or fixed,
                    "line": origin or None, "quiet": True}
    right = NUMBER_VALUE.match(str(target or "").strip())
    if not plan or not right or not wrong:
        return None
    if extract.a_clock_time(target) or extract.a_clock_time(wrong):
        return None
    if not NUMBER_VALUE.match(str(wrong).strip()):
        return None
    number, unit = right.group(1), (right.group(2) or "").lower()
    pattern = r"(?<![\d.])" + re.escape(str(wrong).strip())
    if unit:
        pattern += r"(\s+" + re.escape(unit) + r"\b|\s+(?!" + NOT_A_UNIT + r"\b)[a-z]+\b)?"
    shown = []

    def swap(match):
        found = number + " " + unit if unit else number
        shown.append(found)
        return found

    fixed, count = re.subn(pattern, swap, plan, count=1, flags=re.I)
    if not count:
        return None
    if not unit:
        there = re.search(r"(?<![\d.])" + re.escape(number) + r"(\s+[a-z]+)?", fixed, re.I)
        if there and there.group(1):
            shown[0] = number + there.group(1)
    known = user(memory)
    known["plan"] = fixed
    plans = known.get("plans")
    if isinstance(plans, list):
        known["plans"] = [fixed if p == plan else p for p in plans]
    note(memory, fixed)
    return {"key": "plan", "value": shown[0], "wrong": str(wrong).strip()}

NUMBER_DIGITS = re.compile(r"[£$€]?\d+(?:[.,]\d+)?")

def _number_in(value):
    match = NUMBER_DIGITS.search(str(value or ""))
    return match.group(0).lstrip("£$€").strip() if match else ""

def _correct_a_persons_name(memory, target, text="", wrong=""):
    new = " ".join(str(target or "").split())
    if not new or not extract.NAME_WORD.match(new) or new.lower() in extract.NOT_A_NAME:
        return None
    taken_back = " ".join(str(wrong or "").strip().lower().split())
    if taken_back and taken_back != new.lower():
        moved = _a_name_the_store_keeps(memory, taken_back, new)
        if moved is not None:
            return moved
    said = str(last_user(memory) or "")
    named = [entry for entry in (extract.extract(said).get("others") or [])
             if isinstance(entry, dict) and entry.get("who") and entry.get("name")]
    if len(named) != 1:
        return None
    who = str(named[0]["who"])
    old = str(named[0]["name"])
    was = [str(one) for one in (named[0].get("was") or [])]
    if old.lower() == new.lower():
        return None
    taken_back = str(wrong or "").strip().lower()
    if (not _a_spelling_of(new, old) and taken_back != old.lower()
            and taken_back not in [one.lower() for one in was]
            and not (_a_new_name_was_said(new, text) and _a_name_for_a_person(new))):
        return None
    for entry in others(memory):
        if isinstance(entry, dict) and entry.get("who") == who and entry.get("name"):
            entry["name"] = new
            entry["was"] = [one for one in ([str(o) for o in (entry.get("was") or [])] + [old])
                            if one.lower() != new.lower()]
            said_back = old[:1].upper() + old[1:]
            return {"key": "person_name", "value": new, "wrong": said_back, "from": old}
    return None

def _a_spelling_of(new, old):
    one = str(new or "").strip().lower()
    other = str(old or "").strip().lower()
    if not one or not other or one[0] != other[0]:
        return False
    if one in extract.MONTHS or one in extract.DAYS:
        return False
    if one.startswith(other) or other.startswith(one):
        return True
    return _letters_apart(one, other) <= SPELLING_APART

def _letters_apart(one, other):
    if len(one) < len(other):
        one, other = other, one
    before = list(range(len(other) + 1))
    for i, letter in enumerate(one, 1):
        after = [i]
        for j, other_letter in enumerate(other, 1):
            after.append(min(before[j] + 1, after[j - 1] + 1,
                             before[j - 1] + (letter != other_letter)))
        before = after
    return before[-1]

def _correct_clock(memory, target, text="", wrong=""):
    new = extract.a_clock_time(target)
    bare = "" if new else _a_bare_hour(target)
    if not new and not bare:
        return None
    known = user(memory)
    plans = [p for p in (known.get("plans") or []) if isinstance(p, str) and p.strip()]
    latest = known.get("plan")
    if isinstance(latest, str) and latest.strip() and latest not in plans:
        plans.append(latest)
    if wrong:
        named = [p for p in plans if _clock_key(extract.the_clock_in(p)) == _clock_key(wrong)]
        plans = named or plans
    for plan in reversed(plans):
        found = extract.the_clock_in(plan)
        if not found:
            continue
        old = " ".join(found.group(0).split())
        if not new:
            if _names_a_half_of_the_day(old):
                continue
            new = bare
        if _clock_key(old) == _clock_key(new):
            return None
        fixed = (plan[:found.start()] + new + plan[found.end():]).strip()
        remember(memory, "plan", fixed, text)
        held = known.get("plans")
        if isinstance(held, list):
            known["plans"] = [fixed if str(p) == plan else p for p in held]
        return {"key": "plan", "value": fixed, "from": old}
    return None

def _the_topic_with_the_new_clock(text, plan_now):
    said = " ".join(str(text or "").lower().split())
    plan = " ".join(str(plan_now or "").lower().split())
    if not said or not plan:
        return None
    was, now = extract.the_clock_in(said), extract.the_clock_in(plan)
    if not was or not now or _clock_key(was.group(0)) == _clock_key(now.group(0)):
        return None
    def words(line, found):
        rest = " ".join((line[:found.start()] + line[found.end():]).split())
        return [word for word in rest.split()
                if word not in ("my", "your", "our", "the", "a", "an", "im", "i", "you",
                                "is", "are", "its", "at")]
    if words(said, was) != words(plan, now):
        return None
    fixed = (text[:was.start()] + now.group(0) + text[was.end():]).strip()
    return fixed

BARE_HOUR = re.compile(r"^(\d{1,2})$")

def _a_bare_hour(value):
    match = BARE_HOUR.match(str(value or "").strip())
    if not match or not 1 <= int(match.group(1)) <= 24:
        return ""
    return match.group(1)

def _names_a_half_of_the_day(clock):
    return bool(re.search(r"am|pm|o'?clock|noon|midday|midnight", str(clock or ""), re.I))

def _clock_key(clock):
    return re.sub(r"[^0-9a-z]", "", str(clock or "").lower())

def _correct_number(memory, target, text=""):
    new = " ".join(str(target or "").split())
    digits = _number_in(new)
    if not digits:
        return None
    if _names_a_date(new):
        return None
    said = " ".join(str(last_user(memory) or "").split())
    if not said or _a_birthday_on_the_last_line(memory):
        return None
    olds = [n for n in re.findall(r"\d+(?:[.,]\d+)?", said) if n != digits]
    if not olds:
        return None
    known = user(memory)
    for old in olds:
        for key in ("budget", "age", "height", "weight"):
            value = known.get(key)
            if value is not None and _number_in(value) == old:
                if isinstance(value, str) and re.search(r"\d", value):
                    same = re.sub(r"\d+(?:[.,]\d+)?", digits, value, count=1)
                else:
                    same = int(digits) if isinstance(value, int) else digits
                remember(memory, key, same, text)
                kept = known.get(key)
                shown = kept if kept not in (None, "") else same
                return {"key": key, "value": shown, "from": old}
        for key in ("plan", "job"):
            value = known.get(key)
            if isinstance(value, str) and old in value and digits not in value:
                fixed = re.sub(r"\b" + old + r"\b", digits, value, count=1)
                if fixed == value:
                    continue
                told = text
                if key == "plan":
                    origin = plan_line(memory, value)
                    told = (_swap_in(origin, digits, old) if origin else "") or text
                remember(memory, key, fixed, told)
                plans = known.get("plans")
                if key == "plan" and isinstance(plans, list):
                    known["plans"] = [fixed if str(p).lower() == value.lower() else p
                                      for p in plans]
                if key == "plan":
                    return {"key": "plan", "value": fixed, "sentence": told, "from": old}
                return {"key": "line", "value": fixed[:1].lower() + fixed[1:], "from": old}
    return None

COUNT_SAID = re.compile(r"\b(" + "|".join(sorted(extract.PET_COUNT_WORDS, key=len, reverse=True))
                         + r"|\d{1,2})\b", re.I)

def _count_said(text):
    match = COUNT_SAID.search(" ".join(str(text or "").lower().split()))
    if not match:
        return 0
    word = match.group(1).lower()
    if word.isdigit():
        return int(word)
    return int(extract.PET_COUNT_WORDS.get(word) or 0)

def _a_count(count, animal):
    animal = str(animal or "pet").strip().lower()
    if animal.endswith(("fish", "sheep", "deer")) or count == 1:
        many = animal
    else:
        many = animal + "s"
    return "{} {}".format(count, many)

def _correct_count(memory, target, text=""):
    new = _count_said(target)
    if new < 1 or new > 30:
        return None
    held = [pet for pet in (user(memory).get("pets") or []) if isinstance(pet, dict)]
    if not held:
        return None
    said = " ".join(str(last_user(memory) or "").lower().split())
    named = [str(pet.get("animal") or "") for pet in (extract.extract(str(target or ""))
                                                      .get("pets") or [])]
    if not named:
        named = [str(pet.get("animal") or "") for pet in (extract.extract(said).get("pets") or [])]
    named = [animal for animal in named if animal]
    if not named:
        return None
    told = [pet for pet in (extract.extract(said).get("pets") or []) if pet.get("count")]
    old = int(told[0]["count"]) if told else 0
    if not old or old == new:
        return None
    for pet in reversed(held):
        if _animal_family(pet.get("animal")) != _animal_family(named[0]):
            continue
        pet["count"] = new
        return {"key": "pets_count", "value": _a_count(new, pet.get("animal")),
                "from": _a_count(old, pet.get("animal"))}
    return None

ANY_NUMBER = re.compile(
    r"\b(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"\w+teen|twenty|thirty|forty|fifty|hundred)\b", re.I)

BARE_NEW_COUNT = re.compile(
    r"^\W*(?:(?:ok|okay|ah|oh|right)\b[,.]?\s*)*"
    r"(?:(?:no|nope|sorry|actually|oops|wait|hold\s+on|hold\s+up|hang\s+on)\b[,.]?\s*"
    r"|i\s+mean(?:t)?\s+|make\s+(?:that|it)\s+)+"
    r"(?:(?:just|only|about|around|roughly|nearly|exactly)\s+(?:the\s+)?)?"
    r"(?:(?:it'?s|its|that'?s|thats)\s+)?"
    r"(?P<count>\d{1,3}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|\w+teen)\b"
    r"\s*(?:now\b)?\s*[.!]?$", re.I)

def _correct_the_count_on_the_table(memory, target, text=""):
    line = BARE_NEW_COUNT.match(" ".join(str(text or "").split()))
    if not line:
        return None
    new = _count_said(line.group("count"))
    if not 0 < new <= 30:
        return None
    said = " ".join(str(last_user(memory) or "").split())
    if not said or len(ANY_NUMBER.findall(said)) > 1:
        return None
    known = user(memory)
    counted = extract.extract(said).get("kids")
    if not isinstance(counted, int) or not isinstance(known.get("kids"), int):
        return None
    if counted == new:
        return None
    old = known["kids"]
    remember(memory, "kids", new, text)
    return {"key": "kids", "value": _a_count(new, "kid"), "from": _a_count(old, "kid")}

A_JOURNEY_GOING = re.compile(
    r"\b(?:fly|flies|flying|flight|flights|travel|travels|travelling|traveling|trip|trips"
    r"|holiday|holidays|booking|booked|visit|visiting|journey|outing)\b", re.I)


def _a_fact_of_somebody_else(memory, plan):
    said = " ".join(str(plan or "").lower().split())
    if not said:
        return False
    for entry in (memory or {}).get("others") or []:
        who = str((entry or {}).get("who") or "").strip().lower()
        if not who:
            continue
        word = who.split()[0]
        if re.search(r"\b" + re.escape(word) + r"(?:'?s)?\b", said):
            return True
    return False


def _the_plans_a_journey_moves(memory, plans, text):
    if not A_JOURNEY_GOING.search(str(text or "")):
        return None
    return [one for one in plans if not _a_fact_of_somebody_else(memory, one)]


def _correct_when(memory, target, text=""):
    low = str(target or "").lower()
    if low not in extract.MONTHS and low not in extract.DAYS:
        return None
    known = user(memory)
    plans = [p for p in (known.get("plans") or []) if isinstance(p, str) and p.strip()]
    latest = known.get("plan")
    if isinstance(latest, str) and latest.strip() and latest not in plans:
        plans.append(latest)
    group = extract.MONTHS if low in extract.MONTHS else extract.DAYS
    journeys = _the_plans_a_journey_moves(memory, plans, text)
    if journeys is not None:
        if not journeys:
            return None
        plans = journeys
    for plan in reversed(plans):
        for word in re.findall(r"[a-z]+", plan.lower()):
            if word in group and word != low:
                fixed = re.sub(r"\b" + word + r"\b", target, plan, count=1, flags=re.I)
                told = _plan_told_line(memory, plan, fixed, text)
                remember(memory, "plan", fixed, told)
                plans_list = known.get("plans")
                if isinstance(plans_list, list):
                    known["plans"] = [fixed if str(p).lower() == plan.lower() else p
                                      for p in plans_list]
                read_back = plan_sentence(fixed, told)
                if read_back.lower().startswith("you're planning "):
                    read_back = ""
                return {"key": "plan", "value": fixed.rstrip(" ."),
                        "from": word[:1].upper() + word[1:], "sentence": read_back}
    return None

DATE_DAY = re.compile(r"\b(\d{1,2})(?:st|nd|rd|th)\b", re.I)

A_DAY_BEFORE_A_MONTH = re.compile(
    r"\b(?:the\s+)?(\d{1,2})\s+(?:of\s+)?(?:%s)\b" % "|".join(
        sorted((re.escape(name) for name in extract.MONTHS), key=len, reverse=True)), re.I)

def _date_said(low):
    day = DATE_DAY.search(low)
    month = None
    for name in sorted(extract.MONTHS, key=len, reverse=True):
        if re.search(r"\b" + name + r"\b", low):
            month = name
            break
    if day is None and month:
        bare = A_DAY_BEFORE_A_MONTH.search(low)
        if bare:
            return bare.group(1), month
    return day.group(0) if day else None, month

def _a_day_in_the_kind(old_day, day):
    number = re.match(r"(\d{1,2})", str(day or ""))
    if not number:
        return _date_word_case(day)
    if re.match(r"\d{1,2}(?:st|nd|rd|th)$", str(old_day or ""), re.I):
        count = int(number.group(1))
        suffix = "th" if 11 <= count % 100 <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(
            count % 10, "th")
        return number.group(1) + suffix
    return number.group(1)

def _date_word_case(value):
    text = str(value or "")
    return text[:1].upper() + text[1:] if text[:1].isalpha() else text

def _date_in_plan(plan):
    return _date_said(str(plan or "").lower())

WEEKDAY_IN_PLAN = re.compile(
    r"\b(?:(?:this|next|last|coming|the)\s+)?(?:" +
    "|".join(sorted(extract.DAYS - {"weekend"}, key=len, reverse=True)) + r")\b", re.I)

def _the_weekday_in(plan):
    return WEEKDAY_IN_PLAN.search(str(plan or ""))

def _names_a_date(value):
    day, month = _date_said(str(value or "").lower())
    return bool(day or month)

RELATIVE_MONTH = re.compile(r"\b(?:next|this|that|the\s+following|the\s+coming|the\s+next)\s+month\b",
                            re.I)

def _a_relative_month(plan, day, month):
    if not month or not isinstance(plan, str):
        return None
    found = RELATIVE_MONTH.search(plan)
    if found is None:
        return None
    said = _date_word_case(month)
    if day:
        said = "on the {day} of {month}".format(day=day, month=said)
    else:
        said = "in " + said
    fixed = (plan[:found.start()] + said + plan[found.end():]).strip()
    fixed = " ".join(fixed.replace(" ,", ",").split())
    return fixed, found.group(0).lower(), said

def _a_relative_line(memory, plan, was, said):
    told = plan_line(memory, plan)
    if not told or not was or not said:
        return None
    return re.sub(r"\b" + re.escape(was) + r"\b", said, told, count=1, flags=re.I)

def _plan_saying(memory, day, month):
    if not day and not month:
        return None
    plans = [p for p in ((memory.get("user") or {}).get("plans") or []) if isinstance(p, str)]
    for plan in reversed(plans):
        found_day, found_month = _date_in_plan(plan)
        if month and found_month != month:
            continue
        if day and found_day and found_day != day:
            continue
        return plan
    return None

def _correct_date(memory, target, text="", wrong=""):
    low = str(target or "").lower()
    day, month = _date_said(low)
    if not day and not month:
        return None
    if _a_birthday_on_the_last_line(memory):
        return None
    plan = _stated_plan(memory) or user(memory).get("plan")
    gone_day, gone_month = _date_said(str(wrong or "").lower())
    saying = _plan_saying(memory, gone_day, gone_month)
    if saying:
        plan = saying
    if not isinstance(plan, str) or not plan.strip():
        return None
    old_day, old_month = _date_in_plan(plan)
    fixed, moved = plan, []
    told = None
    if not old_day and not old_month:
        weekday = _the_weekday_in(plan)
        if day and month and weekday:
            said = "the {day} of {month}".format(day=_date_word_case(day),
                                                 month=_date_word_case(month))
            fixed = " ".join((plan[:weekday.start()] + said + plan[weekday.end():]).split())
            was = weekday.group(0).lower()
            moved.append(was)
        else:
            relative = _a_relative_month(plan, day, month)
            if relative is None:
                return None
            fixed, was, said = relative
            moved.append(was)
        told = _a_relative_line(memory, plan, was, said)
    if day and not old_day and old_month:
        with_a_day = re.compile(r"\b(in|on|for|by|until|till|from|around|before|after)\s+"
                                r"(?:the\s+)?" + re.escape(old_month) + r"\b", re.I)
        found = with_a_day.search(fixed)
        if found:
            join = "on" if found.group(1).lower() == "in" else found.group(1).lower()
            fixed = (fixed[:found.start()] + join + " the " + _date_word_case(day) + " of "
                     + _date_word_case(old_month) + fixed[found.end():])
            moved.append(old_month)
    if day and old_day and day.lower() != old_day.lower():
        fixed = re.sub(r"\b" + old_day + r"\b", _a_day_in_the_kind(old_day, day), fixed,
                       count=1, flags=re.I)
        moved.append(old_day)
    if month and old_month and month != old_month:
        fixed = re.sub(r"\b" + old_month + r"\b", _date_word_case(month), fixed, count=1, flags=re.I)
        moved.append(old_month)
    if fixed == plan:
        return None
    if told is None:
        told = _plan_told_line(memory, plan, fixed, text)
    remember(memory, "plan", fixed, told)
    known = user(memory)
    plans_list = known.get("plans")
    if isinstance(plans_list, list):
        known["plans"] = [fixed if str(p).lower() == plan.lower() else p for p in plans_list]
    read_back = plan_sentence(fixed, told)
    if read_back.lower().startswith("you're planning "):
        read_back = ""
    return {"key": "plan", "value": fixed.rstrip(" ."), "from": " ".join(moved),
            "sentence": read_back}

CORRECTABLE = frozenset(("name", "age", "city", "places", "job", "diet", "allergies", "height",
                         "weight", "budget", "pet", "pets", "plan", "birthday"))

def _a_name_the_store_keeps(memory, taken_back, new):
    for entry in others(memory):
        if not isinstance(entry, dict) or not entry.get("name"):
            continue
        if str(entry["name"]).strip().lower() != taken_back:
            continue
        if not _a_name_for_a_person(new):
            return None
        before = str(entry.get("name") or "")
        entry["name"] = new
        if before and before.lower() != new.lower():
            was = [str(old) for old in (entry.get("was") or []) if str(old).lower() != new.lower()]
            entry["was"] = was + [before]
        entry.pop("turns", None)
        log(memory).append({"key": "other", "value": dict(entry),
                            "turn": len(memory.get("turns") or []),
                            "text": "my %s is called %s" % (entry.get("who"), new)})
        return {"key": "person_name", "value": new,
                "wrong": taken_back[:1].upper() + taken_back[1:], "from": taken_back}
    return None

def _stated_last(memory):
    entries = memory.get("facts_log")
    if not isinstance(entries, list):
        return None
    by_line = {}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        said = " ".join(str(entry.get("text") or "").lower().split())
        by_line.setdefault(said, []).append(entry.get("key"))
    for line in reversed(last_user(memory, CORRECTION_BACK) or []):
        said = " ".join(str(line or "").lower().split())
        if not said:
            continue
        keys = by_line.get(said)
        if keys:
            for key in reversed(keys):
                if key in CORRECTABLE:
                    return key
            if not _asks(said):
                return None
            continue
        if not _asks(said):
            return None
    return None

AMOUNT = re.compile(r"(?:[£$\u20ac]\s?)?\d[\d,]*(?:\.\d+)?"
                     r"(?:\s*(?:(?:hundred|thousand|million|grand)(?![a-z])|k(?![a-z])))?",
                     re.I)

NUMBER_WORD = re.compile(r"(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
                         r"noon|midday|midnight)", re.I)

MONTHS = frozenset("january february march april may june july august september october november "
                   "december jan feb mar apr jun jul aug sep sept oct nov dec".split())

MONTH_WORD = re.compile(r"\b(?:" + "|".join(sorted(MONTHS, key=len, reverse=True)) + r")\b",
                        re.I)

MONTH_ALT = "|".join(sorted(MONTHS, key=len, reverse=True))

DATE_PHRASE = re.compile(
    r"\b(?:the\s+)?\d{1,2}(?:st|nd|rd|th)\b(?:\s+of\s+(?:" + MONTH_ALT + r"))?"
    r"|\b(?:the\s+)?\d{1,2}\s+(?:" + MONTH_ALT + r")\b"
    r"|\b(?:" + MONTH_ALT + r")\s+(?:the\s+)?\d{1,2}(?:st|nd|rd|th)?\b", re.I)

AT_TIME = re.compile(r"\bat\s+" + AT_TIME_VALUE, re.I)

DAY_WORD = re.compile(r"\b(?:" + "|".join(sorted(extract.DAYS, key=len, reverse=True))
                      + r")\b", re.I)

CURRENCY = re.compile(r"[£$\u20ac]\s?")

def _plan_told_line(memory, old, new, text=""):
    told = plan_line(memory, old)
    was, now = _date_word(old), _date_word(new)
    if not told or not was or not now or was.lower() == now.lower():
        return text
    return re.sub(r"\b" + re.escape(was) + r"\b", now, told, count=1, flags=re.I)

def _date_word(phrase):
    match = MONTH_WORD.search(str(phrase or "")) or DAY_WORD.search(str(phrase or ""))
    return match.group(0) if match else ""

def _kind_of_value(target, told):
    low = target.lower()
    if low in MONTHS:
        return "month"
    if low in extract.DAYS:
        return "day"
    if AMOUNT.fullmatch(target) and not AT_TIME.search(told):
        return "amount"
    if AT_TIME.search(told) and (AMOUNT.fullmatch(target) or NUMBER_WORD.fullmatch(target)):
        return "time"
    if DATE_PHRASE.search(target):
        return "date"
    return None

def _swap_in(told, target, wrong=None):
    if not isinstance(told, str) or not told.strip() or not target:
        return None
    target = str(target).strip()
    kind = _kind_of_value(target, told)
    if kind in ("month", "day"):
        wanted = MONTH_WORD if kind == "month" else DAY_WORD
        found = list(wanted.finditer(told))
        if not found:
            return None
        last = found[-1]
        return told[:last.start()] + target + told[last.end():]
    if kind == "amount":
        found = list(AMOUNT.finditer(told))
        if not found:
            return None
        last = found[-1]
        unit = CURRENCY.match(told[last.start():])
        tail = told[last.end():]
        if unit and not CURRENCY.match(target):
            target = unit.group(0).strip() + (" " if unit.group(0).endswith(" ") else "") + target
        elif CURRENCY.match(target):
            tail = re.sub(r"^\s*(?:pounds?|dollars?|euros?|quid|bucks?)\b", "", tail, count=1,
                          flags=re.I)
        return told[:last.start()] + target + tail
    if kind == "date":
        found = list(DATE_PHRASE.finditer(told))
        if not found:
            return None
        last = found[-1]
        said = target.lower() if target.lower().startswith(("the ", "a ", "an ")) else target
        return told[:last.start()] + said + told[last.end():]
    if kind == "time":
        found = list(AT_TIME.finditer(told))
        if not found:
            return None
        last = found[-1]
        said = last.group(0)
        half = re.search(r"(am|pm|o'?clock)\b", said, re.I)
        if half and not re.search(r"am|pm|o'?clock|noon|midday|midnight", target, re.I):
            target = target + ("" if target[-1:].isdigit() else " ") + half.group(1)
        rest = re.sub(r"^at\s+" + AT_TIME_VALUE, "at " + target, said, count=1, flags=re.I)
        return told[:last.start()] + rest + told[last.end():]
    if wrong:
        named = re.compile(r"\b" + re.escape(str(wrong).strip()) + r"\b", re.I)
        if not named.search(told):
            return None
        return named.sub(target, told, count=1)
    if not AMOUNT.fullmatch(target):
        return None
    found = list(AMOUNT.finditer(told))
    if not found:
        return None
    last = found[-1]
    return told[:last.start()] + target + told[last.end():]

def _plan_the_line_named(plans, told):
    low = " ".join(str(told or "").lower().split())
    if not low:
        return None
    for plan in plans:
        said = " ".join(str(plan).lower().split())
        if said and (said == low or said in low or low in said):
            return plan
    return None

def _carries(value, word):
    said = " ".join(str(value or "").lower().split())
    word = " ".join(str(word or "").lower().split())
    return bool(said and word and re.search(r"\b" + re.escape(word) + r"\b", said))

def _fact_naming(memory, wrong):
    value = " ".join(str(wrong or "").lower().split())
    entries = memory.get("facts_log")
    if not value or not isinstance(entries, list):
        return None
    pattern = re.compile(r"\b" + re.escape(value) + r"\b", re.I)
    for entry in reversed(entries):
        if not isinstance(entry, dict) or entry.get("key") not in CORRECTABLE:
            continue
        said = str(entry.get("text") or "")
        if pattern.search(said):
            return entry.get("key"), said
    return None

def _a_birthday_on_the_last_line(memory):
    said = " ".join(str(last_user(memory) or "").lower().split())
    if not said:
        return False
    for entry in reversed(memory.get("facts_log") or []):
        if not isinstance(entry, dict):
            continue
        if " ".join(str(entry.get("text") or "").lower().split()) != said:
            continue
        if entry.get("key") == "birthday":
            return True
    return False

def _correct_birthday(memory, target, text=""):
    known = user(memory)
    held = " ".join(str(known.get("birthday") or "").split())
    day, month = _date_said(" ".join(str(target or "").lower().split()))
    if not day and not month:
        return None
    old_day, old_month = _date_said(held.lower())
    day = day or old_day
    month = month or old_month
    if not day and not month:
        return None
    value = day + " of " + month if day and month else (month or day)
    if value.lower() == held.lower():
        return None
    told = text
    for entry in reversed(memory.get("facts_log") or []):
        if isinstance(entry, dict) and entry.get("key") == "birthday":
            told = entry.get("text") or text
            break
    remember(memory, "birthday", value, told)
    return {"key": "birthday", "value": value, "sentence": _birthday_words(value)}

def _a_birthday_for_somebody(memory):
    said = " ".join(str(last_user(memory) or "").lower().split())
    if not said or "birthday" not in said and "born" not in said:
        return None
    for entry in reversed(others(memory)):
        if not isinstance(entry, dict) or not entry.get("birthday"):
            continue
        who = str(entry.get("who") or "").strip().lower()
        if not who or not re.search(r"\b" + re.escape(who) + r"s?\b", said):
            continue
        return entry
    return None

NO_SUBJECT_OF_ITS_OWN = frozenset("""
a about actually ah all also am an and anyway as at be been but by can could did do does doing
for from get gets got had has have i i'd i'll i'm i've if in into is it it's its just like made
make makes me meant meanto maybe might my no nope not of oh ok okay on or own please probably
put puts rather right said say says so sorry than that that's thats the then there these think
this those to too um us was we well were what when where which who will with would yeah yeh yes
you your
""".split())

STILL_THE_SAME_PERSON = frozenset("""
birthday bday dob born her hers he him his she their them they
""".split())

def _the_line_is_about_that_birthday(text, held, target):
    value = set(re.findall(r"[a-z']+", str(target or "").lower()))
    left = [word for word in re.findall(r"[a-z']+", str(text or "").lower())
            if word not in NO_SUBJECT_OF_ITS_OWN and word not in value]
    if not left:
        return True
    who = str((held or {}).get("who") or "").strip().lower()
    theirs = {who, who + "s"} if who else set()
    return all(word in STILL_THE_SAME_PERSON or word in theirs for word in left)

def _correct_their_birthday(memory, target, wrong, text=""):
    held = _a_birthday_for_somebody(memory)
    if not held:
        return None
    low = " ".join(str(target or "").lower().split())
    day, month = _date_said(low)
    if not day and not month:
        return None
    known = " ".join(str(held.get("birthday") or "").lower().split())
    old_day, old_month = _date_said(known)
    if not old_day:
        bare = re.search(r"\b(\d{1,2})\b", known)
        old_day = bare.group(1) if bare else None
    gone_day, gone_month = _date_said(" ".join(str(wrong or "").lower().split()))
    if (gone_day or gone_month) and not ((gone_day and gone_day == old_day)
                                        or (gone_month and gone_month == old_month)):
        return None
    if not _the_line_is_about_that_birthday(text, held, target):
        return None
    day = day or old_day
    month = month or old_month
    value = (day + (" of " if " of " in known else " ") + month) if day and month else (month or day)
    if value.lower() == known.lower():
        return None
    who = str(held.get("who") or "").strip()
    entry = {"who": who, "birthday": value}
    if held.get("name"):
        entry["name"] = held.get("name")
    remember_other(memory, entry, last_user(memory) or text)
    line = "my " + who + "s birthday is " + ("on " if day else "in ") + value
    link = "on " if day else ""
    said_back = "your " + who + "s birthday is " + link + _birthday_words(value)
    return {"key": "birthday", "value": value, "from": known, "line": line,
            "note": "Got it — " + said_back + "."}

def _correct_fact(memory, target, wrong, text=""):
    theirs = _correct_their_birthday(memory, target, wrong, text)
    if theirs:
        return theirs
    known = user(memory)
    counted = extract.pet_counts(target)
    pets = [p for p in (known.get("pets") or []) if isinstance(p, dict)]
    if counted and pets:
        moved = ""
        for said in counted:
            for pet in pets:
                if _animal_family(pet.get("animal")) != _animal_family(said["animal"]):
                    continue
                if pet.get("count") == said["count"]:
                    continue
                pet["count"] = said["count"]
                moved = _many(said["count"], pet.get("animal") or "pet")
        if moved:
            known["pets"] = pets
            return {"key": "pets", "value": moved}
    named = _fact_naming(memory, wrong)
    key = named[0] if named else _stated_last(memory)
    if not key:
        return None
    if key in ("city", "places") and not extract.place_value(target):
        return None
    if key != "birthday" and _a_birthday_on_the_last_line(memory):
        key = "birthday"
    if key == "birthday":
        return _correct_birthday(memory, target, text)
    known = user(memory)
    if key in ("pet", "pets"):
        pets = known.get("pets")
        if not isinstance(pets, list):
            return None
        for pet in reversed(pets):
            if not isinstance(pet, dict) or not pet.get("name"):
                continue
            if wrong and str(pet.get("name")).lower() != wrong.lower():
                continue
            pet["name"] = _tidy_name(target)
            return {"key": "pet", "value": pet["name"], "animal": pet.get("animal") or "pet"}
        return None
    told = None
    held = known.get(key)
    if named and not _carries(held, wrong):
        told = named[1]
    if key in ("budget", "plan"):
        replaced = wrong
        if not replaced and key == "plan":
            places = [p for p in (known.get("places") or []) if isinstance(p, str)]
            replaced = places[-1] if places else None
        if key == "plan" and replaced and not extract.place_value(str(target)):
            return None
        old = told if told is not None else known.get(key)
        swapped = _swap_in(old, target, replaced)
        if swapped:
            said = text
            if key == "plan":
                origin = plan_line(memory, old)
                said = (_swap_in(origin, target, replaced)
                        or _plan_told_line(memory, old, swapped, text))
            remember(memory, key, swapped, said)
            if key == "plan":
                plans = [p for p in (known.get("plans") or []) if isinstance(p, str)]
                holder = _plan_the_line_named(plans, old)
                if holder is not None:
                    known["plans"] = [swapped if p == holder else p for p in plans]
                elif swapped not in plans:
                    known["plans"] = (plans + [swapped])[-6:]
                places = [p for p in (known.get("places") or []) if isinstance(p, str)]
                if replaced and _kind_of_value(target, old) is None \
                        and any(p.lower() == str(replaced).lower() for p in places) \
                        and not any(p.lower() == target.lower() for p in places):
                    known["places"] = places + [target]
            note = swapped
            if key == "plan":
                note = plan_sentence(swapped, said) or swapped
                if note.lower().startswith("you're planning "):
                    note = swapped
            return {"key": key, "value": target, "sentence": note}
    if isinstance(held, str) and _kind_of_value(target, held) is not None:
        return None
    found = extract.reread(target, key)
    if not found:
        return None
    if key in ("city", "places"):
        place = found.get("city") or (found.get("places") or [None])[0]
        if not place:
            return None
        known["places"] = [p for p in (known.get("places") or []) if isinstance(p, str)]
        remember(memory, "places", [place], text)
        remember(memory, "city", place, text)
        return {"key": "city", "value": place}
    value = found.get(key)
    if isinstance(value, list):
        value = value[0] if value else None
    if value in (None, "", [], {}):
        return None
    if key == "budget":
        value = _keep_unit(value, known.get("budget"))
    if key in ("allergies", "people", "conditions"):
        _drop_wrong(known, key, wrong, target)
    remember(memory, key, value, text)
    return {"key": key, "value": value, "from": wrong}

ASK_START = re.compile(r"^\W*(?:does|did|do|is|are|was|were|can|could|would|will|has|have)\b",
                       re.I)

def _keep_unit(value, was):
    value = str(value or "").strip()
    if not value or re.search(r"[a-z]", value):
        return value
    unit = re.search(r"([a-z]+)\s*$", str(was or "").strip(), re.I)
    return value + " " + unit.group(1).lower() if unit else value

def _drop_wrong(known, key, wrong, target):
    kept = [v for v in (known.get(key) or []) if isinstance(v, str)]
    if not kept:
        return
    doomed = {str(w).lower() for w in (wrong, target) if w}
    left = [v for v in kept if v.lower() not in doomed]
    if left == kept and len(kept) == 1:
        left = []
    known[key] = left

MONTH_WORDS = frozenset("""january february march april may june july august september october
november december""".split())

def _birthday_words(date):
    said = " ".join(str(date).split())
    parts = []
    for word in said.split():
        parts.append(word.capitalize() if word in MONTH_WORDS else word)
    said = " ".join(parts)
    if not re.search(r"\d", said):
        return "in " + said
    if not re.match(r"\d{1,2}(?:st|nd|rd|th)\b", said):
        return said
    if re.match(r"\d{1,2}(?:st|nd|rd|th)\s+[A-Z][a-z]+$", said):
        day, month = said.split()
        return "the %s of %s" % (day, month)
    return "the " + said

def _many(count, animal):
    noun = PLURAL_PETS.get(str(animal).lower(), str(animal) + "s")
    return COUNT_WORDS.get(count, str(count)) + " " + noun

ASK_START = re.compile(r"^\W*(?:(?:anyway|and|but|so|oh|right|ok|okay|sorry|just|also|well|then|"
                       r"actually|anyhow|plus)[\s,]+)*"
                       r"(?:what|whats|why|whys|how|hows|when|whens|where|wheres|who|whos|which|"
                       r"whose|can|could|should|would|do|does|did|is|are|(?:was|were)(?!\s+\w+ing\b)|"
                       r"will|shall|have|has|any\b|anyone|anything)\b",
                       re.I)

def _asks(line):
    return bool(ASK_START.match(line or ""))

