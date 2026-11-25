import re

from ..understanding.kinds import VERB_FORMS, VERBISH
from ..understanding.normalize import TIME_WORDS, possessive_me
from . import facts, resize, topics
from .filler import without_filler
from .facts import COUNTRIES, DETERMINERS, NOT_PLACES, MONTHS, PREPOSITIONS
from .topics import (PERSON_TROUBLE, trouble)
from .topics import (KIND_ASK, WHO_SAID, a_detail_of_the_thing_we_hold, about, action,
                     already_said, answer_in_hand,
                     asks_only, bare_question, content, context, current,
                     entry_answer, expand, forms, followup_reading, gist, has_time,
                     introduction_question, is_follow_up, key_subject, keywords, left_for_a_blank,
                     meal_follow_up, note, person, person_named, remember_answer, resumed,
                     return_target, said_again, answer_about, answers_about_another_creature,
                     same_as_before, sized_reply, stem, subject, the_animal_the_subject_is,
                     the_ask_about_the_thing_it_points_at, the_thing_a_detail_belongs_to,
                     the_step_back_takes_its_words_back, the_thing_it_is, topic_text,
                     written_out)

LIST_FACTS = ("places", "allergies", "people", "plans", "condition")

PETS_KEPT = 12


def user(memory):
    facts_ = memory.get("user")
    if not isinstance(facts_, dict):
        facts_ = memory["user"] = {}
    return facts_


def log(memory):
    entries = memory.get("facts_log")
    if not isinstance(entries, list):
        entries = memory["facts_log"] = []
    return entries


def others(memory):
    seen = memory.get("others")
    if not isinstance(seen, list):
        seen = memory["others"] = []
    return seen


ANOTHER_ONE = frozenset("""other another second third fourth youngest eldest oldest first middle
last""".split())


def _said_another(text, who):
    word = str(who or "").strip().lower()
    words = re.findall(r"[a-z']+", str(text or "").lower())
    if not word or not words:
        return False
    for index, one in enumerate(words):
        if one != word and one.rstrip("s") != word.rstrip("s"):
            continue
        if any(earlier in ANOTHER_ONE for earlier in words[max(0, index - 2):index]):
            return True
    return False


def _another_of_them(entry, known, text):
    if entry.get("name") or known.get("name"):
        return False
    age, held = entry.get("age"), known.get("age")
    if not isinstance(age, int) or not isinstance(held, int) or age == held:
        return False
    return _said_another(text, known.get("who") or entry.get("who"))


def remember_other(memory, entry, text=""):
    if not isinstance(entry, dict) or not any(entry.values()):
        return
    who = entry.get("who") or ""
    named = str(entry.get("name") or "").strip().lower()
    if not who and named:
        same = [one for one in others(memory)
                if str(one.get("name") or "").strip().lower() == named]
        if len(same) != 1:
            return
        return _fold_into(memory, same[0], entry, text)
    for known in others(memory):
        if known.get("who") != who:
            continue
        if (entry.get("name") and known.get("name")
                and str(entry["name"]).lower() != str(known["name"]).lower()):
            continue
        if _another_of_them(entry, known, text):
            continue
        return _fold_into(memory, known, entry, text)
    kept = {key: list(value) if isinstance(value, (list, tuple)) else value
            for key, value in entry.items()}
    others(memory).append(kept)
    log(memory).append({"key": "other", "value": kept, "turn": len(memory.get("turns") or []),
                        "text": text})


def _fold_into(memory, known, entry, text=""):
    for key, value in entry.items():
        if key in ("who", "pronoun"):
            continue
        if key == "ages":
            known["ages"] = list(value)
            known.pop("age", None)
            known.pop("to_come", None)
            known.pop("turns", None)
            continue
        if key == "age" and known.get("ages"):
            known.pop("ages", None)
            known["age"] = value
            known.pop("months", None)
            known.pop("to_come", None)
            known.pop("turns", None)
            continue
        if key == "age" and isinstance(value, int) and isinstance(known.get("age"), int):
            ahead = entry.get("turns") or ""
            knew = known.get("turns") or ""
            if ahead and not knew:
                known["to_come"], known["turns"] = value, ahead
                continue
            if knew and not ahead:
                if not isinstance(known.get("to_come"), int) and known.get("age") != value:
                    known["to_come"] = known["age"]
                known["age"] = value
                if isinstance(known.get("to_come"), int) and known["to_come"] <= value:
                    known.pop("to_come", None)
                    known.pop("turns", None)
                continue
            if ahead and knew and value != known["age"]:
                known["to_come"], known["turns"] = value, ahead
                continue
        if not isinstance(value, (list, tuple)):
            known[key] = value
            continue
        have = known.setdefault(key, [])
        if isinstance(have, list):
            have.extend(item for item in value if item not in have)
    return known


COUNT_HEAD = re.compile(
    r"^\W*(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|a few|several|"
    r"lots of|\d+)\b", re.I)


QUESTION_OPEN = re.compile(
    r"^\W*(?:what|how|why|when|where|who|which|whose|should|shall|do|does|did|can|could|is|are|"
    r"was|were|will|would|any)\b", re.I)


def reads_as_a_plan(value, text=""):
    value = " ".join(str(value).split())
    if len(value.split()) < 2:
        return False
    if COUNT_HEAD.match(value):
        return False
    said = " ".join(str(text or "").split())
    if said and (said.endswith("?") or QUESTION_OPEN.match(said)):
        return False
    return True


WHEN_WORDS = frozenset("""january february march april may june july august september october
november december jan feb mar apr jun jul aug sep sept oct nov dec
monday tuesday wednesday thursday friday saturday sunday weekend
next this coming tomorrow tonight morning afternoon evening week month year the of on in at
for and on""".split())


def _the_thing_the_plan_is(plan):
    words = [word for word in re.findall(r"[a-z']+", str(plan or "").lower())
             if word not in WHEN_WORDS]
    return " ".join(words) if len(words) > 1 else ""


def remember(memory, key, value, text=""):
    if value in (None, "", [], {}):
        return
    known = user(memory)
    if isinstance(value, list):
        value = [without_filler(one) if isinstance(one, str) else one for one in value]
    if key in ("plan", "plans"):
        if not isinstance(value, list):
            value = without_filler(value)
    if key == "plans":
        for one in (value if isinstance(value, list) else [value]):
            if not reads_as_a_plan(one, text):
                continue
            plans = known.get("plans")
            if not isinstance(plans, list):
                plans = []
            if one in plans:
                continue
            thing = _the_thing_the_plan_is(one)
            if thing:
                plans = [kept for kept in plans if _the_thing_the_plan_is(kept) != thing]
            plans.append(one)
            known["plans"] = plans[-6:]
        log(memory).append({"key": key, "value": value, "turn": len(memory.get("turns") or []),
                            "text": text})
        return
    if key == "pets":
        pets = known.get("pets")
        if not isinstance(pets, list):
            pets = []
        value = [pet for pet in value if not (isinstance(pet, dict) and pet.get("not_theirs"))]
        if not value:
            return
        one_animal = len(value) == 1
        for pet in value:
            if not isinstance(pet, dict):
                continue
            already_named = [p for p in pets if p.get("animal") == pet.get("animal")
                             and p.get("name") == pet.get("name")]
            rename = (one_animal and pet.get("name") and not pet.get("another")
                      and not already_named
                      and (pet.get("count") or 0) <= 1
                      and [p for p in pets if p.get("animal") == pet.get("animal")
                           and p.get("name") and p.get("name") != pet.get("name")
                           and not (p.get("count") or 0) > 1])
            if rename and len(rename) == 1:
                renamed = rename[0]
                log(memory).append({"key": "pet", "value": pet,
                                    "turn": len(memory.get("turns") or []), "text": text})
                renamed["name"] = pet["name"]
                if pet.get("age") and pet.get("age") != renamed.get("age"):
                    renamed["age"] = pet["age"]
                    renamed.pop("unit", None)
                    if pet.get("unit"):
                        renamed["unit"] = pet["unit"]
                continue
            counted = next((p for p in pets if p.get("animal") == pet.get("animal")
                            and (p.get("count") or 0) > 1 and not p.get("name")), None)
            same = next((p for p in pets if p.get("animal") == pet.get("animal") and
                         (p.get("name") == pet.get("name")
                          or not pet.get("another") and (not p.get("name")
                                                         or not pet.get("name"))
                          or counted is not None and p is counted)), None)
            if same is None and not pet.get("another") and (pet.get("count") or 0) <= 1:
                kind = facts.ANIMAL_KINDS.get(str(pet.get("animal") or "").lower(), "")
                if pet.get("breed") and not pet.get("name"):
                    same = next((p for p in pets if p.get("coming") and kind
                                 and facts.ANIMAL_KINDS.get(
                                     str(p.get("animal") or "").lower(), "") == kind), None)
            if same is not None:
                if pet.get("name") and not same.get("name"):
                    same["name"] = pet["name"]
                    log(memory).append({"key": "pet", "value": pet,
                                        "turn": len(memory.get("turns") or []), "text": text})
                if pet.get("breed") and not same.get("breed"):
                    same["breed"] = pet["breed"]
                    log(memory).append({"key": "pet", "value": pet,
                                        "turn": len(memory.get("turns") or []), "text": text})
                elif pet.get("count") and pet.get("count") != same.get("count"):
                    same["count"] = pet["count"]
                    log(memory).append({"key": "pet", "value": pet,
                                        "turn": len(memory.get("turns") or []), "text": text})
                if pet.get("age") and pet.get("age") != same.get("age"):
                    same["age"] = pet["age"]
                    same.pop("unit", None)
                    if pet.get("unit"):
                        same["unit"] = pet["unit"]
                    log(memory).append({"key": "pet", "value": pet,
                                        "turn": len(memory.get("turns") or []), "text": text})
                if pet.get("breed") and pet.get("breed") != same.get("breed"):
                    same["breed"] = pet["breed"]
                    log(memory).append({"key": "pet", "value": pet,
                                        "turn": len(memory.get("turns") or []), "text": text})
                continue
            pets.append(pet)
            log(memory).append({"key": "pet", "value": pet, "turn": len(memory.get("turns") or []),
                                "text": text})
        known["pets"] = pets[-max(PETS_KEPT, len(value)):]
        return
    if key == "tastes":
        tastes = known.get("tastes")
        if not isinstance(tastes, list):
            tastes = []
        for taste in value if isinstance(value, (list, tuple)) else [value]:
            if not isinstance(taste, dict) or not taste.get("thing"):
                continue
            thing = " ".join(str(taste.get("thing") or "").lower().split())
            same = next((t for t in tastes
                         if " ".join(str(t.get("thing") or "").lower().split()) == thing), None)
            if same is not None:
                if same.get("how") != taste.get("how"):
                    same["how"] = taste.get("how")
                    log(memory).append({"key": "taste", "value": taste,
                                        "turn": len(memory.get("turns") or []), "text": text})
                continue
            tastes.append(taste)
            log(memory).append({"key": "taste", "value": taste,
                                "turn": len(memory.get("turns") or []), "text": text})
        known["tastes"] = tastes[-6:]
        return
    if key == "owns":
        held = known.get("owns")
        if not isinstance(held, dict):
            held = {}
        for thing, name in (value or {}).items() if isinstance(value, dict) else []:
            if not thing or not name:
                continue
            if held.get(thing) == name:
                continue
            held[thing] = name
            log(memory).append({"key": "owns", "value": {thing: name},
                                "turn": len(memory.get("turns") or []), "text": text})
        known["owns"] = held
        return
    if key in LIST_FACTS:
        seen = known.get(key)
        if not isinstance(seen, list):
            seen = []
        for item in value if isinstance(value, (list, tuple)) else [value]:
            if item and item not in seen:
                seen.append(item)
                log(memory).append({"key": key, "value": item, "turn": len(memory.get("turns") or []),
                                    "text": text})
        known[key] = seen[-8:]
        return
    if known.get(key) == value:
        return
    known[key] = value
    log(memory).append({"key": key, "value": value, "turn": len(memory.get("turns") or []),
                        "text": text})


def forget(memory, key, values, why=None):
    known = user(memory)
    wanted = values if isinstance(values, (list, tuple, set)) else [values]
    doomed = {str(value).strip().lower() for value in wanted if str(value).strip()}
    had = known.get(key)
    if key == "pets":
        if not isinstance(had, list) or not doomed:
            return []
        everything = "*" in doomed
        records = [value for value in wanted if isinstance(value, dict)]
        kept, gone = [], []
        for pet in had:
            if not isinstance(pet, dict):
                continue
            worded = (str(pet.get("animal") or "").strip().lower() in doomed
                      or str(pet.get("name") or "").strip().lower() in doomed)
            named = pet in records
            if not (everything or worded or named):
                kept.append(pet)
                continue
            if named and not everything and not worded and (pet.get("count") or 1) > 1:
                pet["count"] = int(pet["count"]) - 1
                if pet["count"] <= 1:
                    pet.pop("count", None)
                kept.append(pet)
                continue
            gone.append(pet)
        known[key] = kept
        if not kept:
            known.pop(key, None)
        if gone:
            past = [pet for pet in (known.get("pets_gone") or []) if isinstance(pet, dict)]
            for pet in gone:
                if not isinstance(pet, dict):
                    continue
                if pet not in past:
                    past.append(dict(pet, gone=why or "gone"))
            known["pets_gone"] = past
        return gone
    if key in LIST_FACTS:
        if not isinstance(had, list) or not doomed:
            return []
        left = [value for value in had if str(value).strip().lower() not in doomed]
        known[key] = left
        return [value for value in had if str(value).strip().lower() in doomed]
    if had is None or not doomed:
        return []
    if str(had).strip().lower() in doomed:
        del known[key]
        return [had]
    return []


def there_is_a_chat(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    for turn in turns or ():
        if isinstance(turn, dict) and str(turn.get("user") or "").strip():
            return True
    return False


def recent(memory, n=6):
    if not memory:
        return []
    turns = memory.get("turns")
    if not isinstance(turns, list):
        return []
    return turns[-n:]


def last_user(memory, n=1):
    lines = [turn.get("user", "") for turn in recent(memory, n)]
    return lines if n > 1 else (lines[-1] if lines else "")


def last_bot(memory):
    turns = recent(memory, 1)
    return turns[-1].get("bot", "") if turns else ""


def last_module(memory):
    turns = recent(memory, 1)
    return turns[-1].get("module") if turns else None


def name(memory):
    facts_ = user(memory)
    value = facts_.get("name")
    return value if isinstance(value, str) else ""


PLAN_OPENS = frozenset("""i i'm im i've i'll ill we we're were we've weve we'll well my our me""".split())
JOINED_SUBJECT = re.compile(r"^(?:[a-z'\u2019]+\s+){0,3}and\s+(?:i|me)\b", re.I)
PLAN_VERBS = frozenset("""planning going trying aiming hoping intending looking""".split())


APPOINTMENT_PLAN = re.compile(
    r"^(?:the\s+)?(?P<thing>[a-z][a-z0-9' \-]{1,28}?)\s+(?P<when>at\s+[\w:.]+(?:\s*(?:am|pm))?"
    r"(?:\s+on\s+[a-z0-9 \-]+)?|on\s+[a-z0-9 \-]+)$", re.I)


APPOINTMENT_DOING = frozenset("""
arrange bake book bring buy call clean collect cook deliver do drop email fetch finish fix get
go have hire make meet message order pay phone pick post put renew rent ring see send set sort
start submit take text tidy visit write
""".split())
APPOINTMENT_A_DETERMINER = frozenset("""
a an the my your our their his her its this that these those some any
""".split())


APPOINTMENT_A_PERSON_VERB = frozenset("""
meet call ring text phone message email see visit collect fetch
""".split())
APPOINTMENT_A_QUANTITY = frozenset("""
bread money rent cash milk water petrol diesel fuel shopping washing ironing laundry food
""".split())
APPOINTMENT_A_PLURAL = re.compile(r"^[a-z]{3,}(?:s|es)$")
APPOINTMENT_NOT_A_PLURAL = ("ss", "us", "is", "ous")


def _takes_a_thing(word):
    if word in APPOINTMENT_A_QUANTITY:
        return True
    return bool(APPOINTMENT_A_PLURAL.match(word)
                and not word.endswith(APPOINTMENT_NOT_A_PLURAL))


def _a_doing(thing):
    words = [word.strip(",.;:") for word in thing.lower().split()]
    if not words:
        return False
    if words[0].endswith("ing") and len(words[0]) > 4:
        return False
    if words[0] in APPOINTMENT_A_PERSON_VERB:
        return True
    if any(word in APPOINTMENT_A_DETERMINER for word in words[1:]):
        return True
    return (len(words) > 1 and words[0] in APPOINTMENT_DOING
            and _takes_a_thing(words[1]))


_WEEKDAY_NAMES = frozenset(("monday", "tuesday", "wednesday", "thursday", "friday", "saturday",
                            "sunday", "christmas", "easter"))
_DATE_LEADS = frozenset(("in", "of", "by", "from", "until", "till", "til", "early", "late", "mid",
                         "towards", "before", "after"))
_A_DAY_NUMBER = re.compile(r"^\d{1,2}(?:st|nd|rd|th)?$")


def named_days(said):
    words = str(said or "").split()
    out = []
    for index, word in enumerate(words):
        bare = word.lower().strip(",.;:!?")
        before = words[index - 1].lower().strip(",.;:!?") if index else ""
        after = words[index + 1].lower().strip(",.;:!?") if index + 1 < len(words) else ""
        if (bare in _WEEKDAY_NAMES
                or (bare in MONTHS and (before in _DATE_LEADS or _A_DAY_NUMBER.match(before)
                                        or _A_DAY_NUMBER.match(after)))):
            word = word.replace(bare, bare[:1].upper() + bare[1:], 1)
        out.append(word)
    return " ".join(out)


def _a_name_at_the_front(text):
    words = str(text or "").split()
    if not words or not words[0][:1].isupper():
        return False
    return words[0].lower().strip(",.!?") not in ("a", "an", "the")


WHOSE_IT_IS = frozenset(("his", "her", "hers", "their", "theirs", "your", "yours"))

A_THING_DOES_BARE = frozenset("""go come start end begin finish close open reopen run happen
arrive leave return fly land depart move switch change rise set turn shut take last break
break up go back come round""".split())
A_THING_DOES_S = frozenset("""is are was were due goes comes starts ends begins finishes closes
opens reopens runs happens arrives leaves returns flies lands departs moves switches changes
rises sets turns shuts takes lasts breaks""".split())


def _a_plural(word):
    word = str(word or "").lower()
    return word.endswith("s") and not word.endswith(("ss", "us", "is"))


def _has_its_own_verb(thing):
    words = [word.strip(",.;:!?") for word in str(thing or "").lower().split()]
    if len(words) < 2:
        return False
    for index, word in enumerate(words[1:], 1):
        if word in A_THING_DOES_S:
            return True
        if _a_plural(words[index - 1]) and word in A_THING_DOES_BARE:
            return True
    return False


def appointment_sentence(text):
    found = APPOINTMENT_PLAN.match(" ".join(str(text or "").split()).strip(" .!?,"))
    if not found:
        return ""
    thing = _the_possessive_a_relation_means(found.group("thing").strip())
    when = found.group("when").strip()
    if not thing or thing.split()[0].lower() in (
            "i", "im", "i'm", "we", "were", "we're", "my", "our", "to", "it", "its", "he", "she",
            "they", "you"):
        return ""
    when = named_days(when)
    if _a_doing(thing):
        said = "You're planning to " + thing[:1].lower() + thing[1:] + " " + when
        return said[:1].upper() + said[1:]
    if thing.split()[0].lower() in ("a", "an"):
        said = "You've got " + thing[:1].lower() + thing[1:] + " " + when
        return said[:1].upper() + said[1:]
    if thing.split()[0].lower() in WHOSE_IT_IS:
        said = thing + ("" if _has_its_own_verb(thing) else " is") + " " + when
        return said[:1].upper() + said[1:]
    said = "Your " + thing + ("" if _has_its_own_verb(thing) else " is") + " " + when
    return said[:1].upper() + said[1:]


JOURNEY_LINE = re.compile(
    r"\b(?:i|im|i'm|ive|i've|we|were|we're|weve|we've|they|hes|he's|shes|she's)\s+"
    r"(?:am\s+|are\s+|is\s+)?(?:going|off|flying|fly|moving|driving|heading|travell?ing|"
    r"cycling|walking|jetting|sailing|back)\b", re.I)


def _a_journey_line(said_line):
    return bool(JOURNEY_LINE.search(str(said_line or "")))


def plan_sentence(plan, said_line=None):
    return named_days(_the_plan_said_back(plan, said_line))


def _the_plan_said_back(plan, said_line=None):
    text = without_filler(" ".join(str(plan or "").split())).strip(" .!?,")
    text = re.sub(r"^(?:and\s+)?(?:also|oh|plus|by the way|btw|anyway|anyways|so|well|right|ok|"
                  r"okay|hey|and)\b[\s,]*", "", text, flags=re.I).strip(" .!?,")
    text = re.sub(r"^to\s+", "", text, flags=re.I)
    if not text:
        return ""
    said_sentence = facts.no_tone(
        without_filler(" ".join(str(said_line or "").split()))).strip(" .!?,")
    theirs = bool(said_sentence) and (said_sentence.split()[0].lower() in PLAN_OPENS
                                      or bool(JOINED_SUBJECT.match(said_sentence)))
    appointment = ("" if (_a_journey_line(said_line) or _a_name_at_the_front(text))
                   else appointment_sentence(text))
    if appointment:
        if theirs and text.lower() in said_sentence.lower():
            out = _mid(you(said_sentence)).rstrip(" .")
            return out[:1].upper() + out[1:]
        return appointment
    text = re.sub(r"^to\s+", "", text, flags=re.I)
    text = re.sub(r"^plans?\s+to\s+", "planning to ", text, flags=re.I)
    first = text.split()[0].lower().strip(",.;:")
    if first in PLAN_VERBS:
        phrase = _mid(you(text))
        return ("You're " + phrase[:1].lower() + phrase[1:]).rstrip(" .")
    if first in PLAN_OPENS or JOINED_SUBJECT.match(text):
        said = re.sub(r"\b(?:im|ive|ill)\b", lambda m: "i'" + m.group(0)[1:], text, flags=re.I)
        said = re.sub(r"\bwere\b", "we're", said, flags=re.I)
        said = re.sub(r"\bweve\b", "we've", said, flags=re.I)
        out = _mid(you(said)).rstrip(" .")
        return out[:1].upper() + out[1:]
    if said_sentence and theirs:
        return plan_sentence(said_sentence)
    phrase = you(text)
    phrase = phrase[:1].lower() + phrase[1:]
    if first.endswith("ing") and len(first) > 4:
        return ("You're " + phrase).rstrip(" .")
    if first in DETERMINERS or first in COUNTRIES or first in NOT_PLACES \
            or (first in _places() and first not in _not_places()):
        return ("You're planning " + phrase).rstrip(" .")
    if phrase.lower().startswith("to "):
        return ("You're planning " + phrase).rstrip(" .")
    return ("You're planning to " + phrase).rstrip(" .")


def _mid(text):
    return re.sub(r"(?<=[\s,])You\b", "you", text)


SAYS_TO_A_PERSON = frozenset("""
told tell telling tellin says said asks asked ask asking calls called call calling rang ring
ringing texted texting texts text emailed emailing emails email phoned phoning phones phone
messaged messaging message thanked thanking thanks thank blamed blaming blame ignored ignoring
ignore hurt hurting hurts missed missing miss loved loving love needed needing need trusted
trusting trust woke woken woke saw seeing seen heard hearing hear helped helping help sent
sending send showed showing show shown gave giving give given paid paying pay owed owing owe met
meeting meet noticed noticing notice picked picking pick chose chosen choose chose kissed
kissing kiss hugged hugging hug
""".split())
DONE_TO_A_PERSON = frozenset("""
to at with for about on from of around near towards toward into over behind beside against
across
""".split())
SUBJECT_HEADS = frozenset(("i", "i'm", "i've", "i'll", "i'd", "im", "ive", "ill", "we", "we're",
                           "we've", "we'll", "we'd", "were", "me", "my", "mine", "us", "our",
                           "ours", "you", "your", "yours", "yourself", "he", "she", "it", "they",
                           "him", "her", "them", "his", "their", "theirs"))
FIRST_PERSON_HEADS = frozenset(("i", "i'm", "i've", "i'll", "i'd", "im", "ive", "ill", "we",
                                "we're", "we've", "we'll", "we'd", "were"))
_BOT_ME, _BOT_MY = "\x00m", "\x00M"


def _to_the_bot(text):
    words = re.findall(r"[a-z']+", text.lower())
    head = next((word for word in words if word in SUBJECT_HEADS), "")
    if head not in FIRST_PERSON_HEADS:
        return text
    def mark(match):
        word = match.group(2)
        if match.group(1).lower() not in SAYS_TO_A_PERSON | DONE_TO_A_PERSON:
            return match.group(0)
        if match.group(1).lower() in ("thank", "thanks"):
            after = re.match(r"[\s,]*([a-z']+)", match.string[match.end():])
            if not after or after.group(1).lower() not in ("for", "again", "so", "too"):
                return match.group(0)
        new = "my" if word.lower() == "your" else "me"
        marker = _BOT_MY if new == "my" else _BOT_ME
        return match.group(1) + " " + (marker.upper() if word[:1].isupper() else marker)
    return re.sub(r"\b([a-z']+) +\b(you|your)\b", mark, text, flags=re.I)


def _from_the_bot(text):
    return text.replace(_BOT_ME, "me").replace(_BOT_MY, "my")

def _places():
    try:
        from ..understanding.topics import PLACES
    except ImportError:
        return frozenset()
    return PLACES


def _not_places():
    try:
        from ..understanding.topics import NOT_PLACES
    except ImportError:
        return frozenset()
    return NOT_PLACES


APOSTROPHE = {
    "im": "I'm", "ive": "I've", "dont": "don't", "cant": "can't",
    "doesnt": "doesn't", "didnt": "didn't", "isnt": "isn't", "wasnt": "wasn't",
    "arent": "aren't", "werent": "weren't", "havent": "haven't", "hasnt": "hasn't",
    "hadnt": "hadn't", "wouldnt": "wouldn't", "couldnt": "couldn't", "shouldnt": "shouldn't",
    "mustnt": "mustn't", "neednt": "needn't", "aint": "ain't", "shes": "she's",
    "hes": "he's", "thats": "that's", "whats": "what's", "theres": "there's",
    "heres": "here's", "theyre": "they're", "youre": "you're", "youve": "you've",
    "youll": "you'll", "youd": "you'd",
}
APOSTROPHE_WORD = re.compile(r"\b(" + "|".join(sorted(APOSTROPHE, key=len, reverse=True)) +
                             r")\b", re.I)


QUOTED = re.compile(r'"[^"]*"|\u201c[^\u201d]*\u201d|(?<!\w)' + "'" + r"[^']*" + "'" + r'(?!\w)')


def _outside_quotes(text, repair):
    if not text or not QUOTED.search(text):
        return repair(text)
    out, last = [], 0
    for found in QUOTED.finditer(text):
        out.append(repair(text[last:found.start()]))
        out.append(found.group(0))
        last = found.end()
    out.append(repair(text[last:]))
    return "".join(out)


def without_the_apostrophe(text):
    if not text:
        return text
    def put_back(match):
        word = match.group(0)
        other = APOSTROPHE.get(word.lower(), word)
        return other[:1].upper() + other[1:] if word[:1].isupper() else other
    return _outside_quotes(text, lambda part: APOSTROPHE_WORD.sub(put_back, part))
NOT_OWNED = (frozenset("""are were is was am and or but nor too either""".split())
             | VERB_FORMS | VERBISH)
WITH_SOMEBODY = frozenset("""see saw seen seeing visit visited visiting meet met meeting missed
    missing miss call called calling ring rang ringing text texted texting phone phoned phoning
    email emailed emailing thank thanked thanking hug hugged hugging kiss kissed kissing help helped
    helping bother bothered bothering visit stay stayed staying""".split()) | {"with"}
WHEN_OR_WHERE = TIME_WORDS | PREPOSITIONS | DETERMINERS | frozenset("""next last later soon
    earlier afterwards afterward today tomorrow tonight week weekend morning evening night day
    month year couple few""".split())


def _the_relation_possessive(text):
    def own(match):
        whole, relation, thing = match.group(0), match.group(2), match.group(3)
        if relation[:-1].lower() not in facts.RELATIONS or thing.lower() in NOT_OWNED:
            return whole
        if thing.lower() in WHEN_OR_WHERE and _with_somebody(text, match.start()):
            return whole
        return match.group(1) + " " + relation[:-1] + "'s " + thing
    return re.sub(r"\b((?:[Mm]y|[Oo]ur)) ([a-z]+s) ([A-Za-z0-9']+)", own, text)


def _the_possessive_a_relation_means(phrase):
    match = re.match(r"([A-Za-z]+s)\s+([A-Za-z0-9']+)", str(phrase or "").strip())
    if not match:
        return phrase
    relation, owned = match.group(1), match.group(2)
    if relation[:-1].lower() not in facts.RELATIONS or owned.lower() in NOT_OWNED:
        return phrase
    if owned.lower() in WHEN_OR_WHERE:
        return phrase
    return relation[:-1] + "'s " + phrase.strip()[len(relation):].lstrip()


def _with_somebody(text, start):
    before = text[:start].rstrip().split()
    return bool(before) and before[-1].lower() in WITH_SOMEBODY


def you(text):
    return _outside_quotes(
        text, lambda part: _flip_to_the_second_person(_the_relation_possessive(part)))


def _flip_to_the_second_person(text):
    swaps = {"i'm": "you're", "i am": "you are", "i've": "you've", "i have": "you have",
             "i'll": "you'll", "we'll": "you'll",
             "im": "you're", "ive": "you've",
             "i was not": "you were not", "i wasn't": "you weren't", "i wasnt": "you weren't",
             "i was": "you were", "i were": "you were", "we was": "you were",
             "we wasnt": "you weren't",
             "my": "your", "mine": "yours", "myself": "yourself", "me": "you", "we": "you",
             "our": "your", "ourselves": "yourselves", "us": "you", "i": "you"}
    def swap(match):
        word = match.group(0)
        other = swaps.get(word.lower(), word)
        return other[:1].upper() + other[1:] if word[:1].isupper() else other
    text = _the_relation_possessive(text)
    text = _to_the_bot(text)
    words = re.findall(r"[a-z']+", text.lower())
    mine = possessive_me(words)
    said_me = [index for index, word in enumerate(words) if word == "me"]
    owns = {place for place, index in enumerate(said_me)
            if index < len(mine) and mine[index] == "my"}
    owns -= {place for place, found in enumerate(re.finditer(r"\bme\b", text, re.I))
             if re.match(r"\s*,", text[found.end():])}
    if owns:
        seen = [-1]
        def yours(match):
            seen[0] += 1
            word = match.group(0)
            if seen[0] in owns:
                return "Your" if word[:1].isupper() else "your"
            return word
        text = re.sub(r"\bme\b", yours, text, flags=re.I)
    text = re.sub(r"\b(i'm|i am|i've|i have|i was not|i wasn't|i wasnt|i was|i were|we wasnt|"
                  r"we was|im|ive|my|mine|myself|me|we|our|ourselves|us|i)\b", swap, text, flags=re.I)
    return without_the_apostrophe(_from_the_bot(text))


ASK_WORDS = frozenset("""how what when where who why which whose should shall can could do does did
is are was were will would am""".split())
ASK_TAIL = re.compile(r",\s*(?:and\s+)?(?:" + "|".join(sorted(ASK_WORDS)) + r")\b", re.I)


WERE_DOING = re.compile(r"we[r']?e?\s+\w+ing\b|were\s+\w+ing\b", re.I)


def _statement(text):
    line = " ".join(str(text or "").split()).strip(" .!?,")
    words = line.split()
    if (words and words[0].lower().strip(",.;:") in ASK_WORDS
            and not WERE_DOING.match(line)):
        return ""
    cut = ASK_TAIL.search(line)
    if cut:
        line = line[:cut.start()]
    return line.strip(" .,!?")


def plan_line(memory, plan):
    wanted = " ".join(str(plan or "").lower().split())
    if not wanted:
        return None
    for entry in reversed(log(memory)):
        if entry.get("key") not in ("plan", "plans"):
            continue
        if " ".join(str(entry.get("value") or "").lower().split()) != wanted:
            continue
        said_line = _statement(entry.get("text"))
        if said_line:
            return said_line
    return None


def said(memory, key):
    for entry in log(memory):
        if entry.get("key") == key:
            return entry.get("value"), entry.get("turn")
    return None, None


__all__ = [
    "action", "already_said", "asks_only", "context", "you", "current", "entry_answer", "expand", "facts",
    "followup_reading", "gist", "has_time", "introduction_question", "is_follow_up",
    "answer_in_hand",
    "key_subject", "keywords", "last_bot", "last_module", "last_user", "left_for_a_blank", "log",
    "meal_follow_up", "name", "note", "plan_line", "plan_sentence", "recent", "remember",
    "remember_answer", "resumed", "return_target", "said", "said_again", "same_as_before",
    "answer_about", "answers_about_another_creature", "the_animal_the_subject_is",
    "sized_reply", "stem", "subject", "the_ask_about_the_thing_it_points_at", "topic_text",
    "the_step_back_takes_its_words_back", "topics", "user", "bare_question", "written_out",
]
