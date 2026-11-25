
import copy
import datetime
import random
import re

from ..compose import pick
from ..compose.recall import with_a_tail
from ..memory import (content, current, forget, forms, is_follow_up, keywords, last_bot,
                      last_module, last_user, log, name, note, others, plan_line, plan_sentence,
                      recent, remember, remember_answer, remember_other, resumed, return_target,
                      stem, thread, user, you)
from ..memory import ack
from ..memory.places import (A_QUESTION_ASKED, NOT_A_PLACE_VALUE, OTHER_PLACE, OTHER_PLACE_PRONOUN,
                             PLACE_ENDS, _a_place, _a_town_moved, _asked_person, _other_place,
                             _said_places, _the_place_alone)
from ..memory import change as a_change
from ..memory import cause as a_reason
from ..memory.spoken import _spoken_as_numbers
from ..memory import pending
from ..memory import another as second_half
from ..memory import choice as choose
from ..memory import condition
from ..memory import decided
from ..memory import company
from ..memory import spent
from ..memory import surname as family_name
from ..memory.filler import without_filler, without_the_end_shrug
from ..memory import guest
from ..memory import plans
from ..memory.named import carries_a_name
from ..memory.taste import ASKS_ABOUT_A_TASTE, ASKS_FOR_TASTES, TASTE_ASKED_ABOUT
from ..memory.taste import read_all as read_tastes
from ..memory import facts as extract
from ..knowledge import cooking
from ..knowledge import units
from ..knowledge.maths import solve
from ..memory import counts as how_many
from ..memory import rates as rates_reader
from ..memory.times import keep as _keep_the_times
from ..memory.times import answer as _the_time_they_said
from ..memory.times import is_a_time_ask as _a_plain_time_ask
from ..memory import history
from ..memory import narrow
from ..memory import hours as hours_after
from ..memory import named as named_thing
from ..memory import recall
from ..memory import reminded
from ..memory import carry as about_the_choice
from ..memory import resize
from ..memory import reject as turned_down
from ..memory import repair as a_repair
from ..memory import told as told_about
from ..memory import whathurts as a_hurting_part
from ..memory.when import (already_answer, asks_what_today_is, the_part_asked, until_answer,
                             when_answer)
from ..memory.topics import ACKS, GREET, STOPWORDS
from ..memory import topics as _topics
from ..memory.repeat import HEDGE as _HEDGE
from ..memory import repeat as repeat_the_line
from ..memory.topics import subject as topic_subject
from ..memory.thread import about as _about_the_chat
from ..understanding import breeds, understand
from ..understanding.normalize import fix_typo, normalise
from ..understanding.kinds import the_manners_question
from ..understanding.topics import PLACES


from ..memory.store_lines import (
    PRIORITY,
    ANSWERS,
    RECALL_HINTS,
    SELF,
    NOT_THE_PLAN,
    NOT_ON_A_MEDIUM,
    REPEAT_ADVERB,
    LIMITS,
    DENIAL_SAY,
    CORRECTED_SAY,
    RETRACT_SAY,
    NOT_RETRACTED,
    _FACT_SLOT,
    PET_AGE_FIX_WORDS,
    OTHER_SAID,
    OTHER_KIND_SAY,
    AGE_FIX_WORDS,
    NAME_FIX_WORDS,
    NAME_GIVEN_WORDS,
    UNIT_FAMILY,
    FACT_FAMILY,
    NOT_A_UNIT,
    AMOUNT_WORD,
    SPELLING_APART,
    CORRECTION_SAY_DROP,
    DROP_LISTS,
    CORRECTION_SAY,
    CORRECTION_SAY_PAIR,
    PET_RENAMED_SAY,
    BARE_ECHO_ONLY,
    CORRECTION_BACK,
    AT_TIME_VALUE,
    KIN_ASK,
    IN_LAW_AFTER_TEXT,
    PRONOUN_FITS,
    CHILD_RELATIONS,
    _ABOUT_WHO,
    CHILD,
    CHILD_OF,
    FAMILY_GROUP,
    FOOD_PHRASES,
    ADVICE_MODULES,
    SLOT_KEY,
    BARE_SLOTS,
    WHERE_ASK,
    KIN,
    BAD_NEWS,
    _UNIT_SAID,
    _AMOUNTS,
    _AMOUNT_WORDS,
    _COUNT_WORD,
    _CONVERT,
    _WEEKLY,
    FIGURE_UNITS,
    FIGURE_TIME,
    FIGURE_NUMBER,
    FIGURE_QUALIFIER,
    LOOK_BACK_FIGURE,
    FIGURE_ANSWER_LEN,
    COUNT_WORD,
    PLACE_NOT,
    TURNED,
    PART_HELD,
    PART_KEYS,
    KEPT_THINGS,
    NAMED_BY,
    RESTATED_KEYS,
    SWAPPABLE,
    _TENS_WORDS,
    CORRECTED_AGAIN,
    CORRECTED_AGAIN_WHO,
    CORRECTED_WHICH_PERSON,
    CAT_NAMES,
    DOG_NAMES,
    SMALL_NAMES,
    NAME_ADVICE,
    RESUME,
    NO_PLANS_REPLY,
    WEEK,
    TAIL_WINDOW,
    PLURAL_PEOPLE,
    DIET_RULES_OUT,
    DENIAL_WORDS,
    DENIAL_STEMS,
    CHILD_RELATIONS,
    GROUP_OF,
    RELATION_ALIKE,
    MONTH_ORDER,
    HAVE_ANY_WORDS,
    HER_WORD,
    DIET_FOOD,
    PERSON_GROUP,
    PLURAL_PEOPLE,
    OWNED_BY_THE_VERB,
    PREGNANT_OWN_SAY,
    PREGNANT_SAY,
    PREGNANT_WEEKS_SAY,
    LIMIT_SAY,
    FEEDING_SAY,
    STATE_WAS_SAY,
    PET_WORDS,
    PRONOUN_PEOPLE,
    SAME_FACT_THEIR_OWN,
    CONDITION_RULES_OUT,
    CONDITION_KEEPS_DOWN,
    CAR_CAPS,
    NUMBER_WORDS,
    _SUBJECT_KEYS,
    PLURAL_PETS,
    COUNT_WORDS,
    A_SHORT_ANSWER,
    KEY_SLOT,
    CONCEPTS,
    POSSESSIVE,
    QUOTE_LEADS,
    ASKED_LEADS,
    NOTHING_STARTED,
    POINTS_BACK_NOTHING,
    POINTING_WORD_NOTHING,
    WHAT_I_SAID_NOTHING,
    RESTRICT_OPENS,
    CALL_LEADS,
    LENGTH,
    WORD_NUMBERS,
    UNIT_SECONDS,
    BUDGET_FITS,
    BUDGET_MORE,
    BUDGET_TIGHT,
    ANY_FIGURE,
    HELD_THREAD,
    GRIEF_WORDS,
    CLOSE_PLAIN,
    CLOSE_HEAVY,
    CHANGE_PLAIN,
    CHANGE_HEAVY,
    CHECK_NOTHING_SAID,
    CHECK_A_FEELING,
    CHECK_A_QUESTION,
    CHECK_PLAIN,
    CLOCK_SAID,
    ROUTINE_SUBJECT,
    ROUTINE_SAY_BACK,
)
from ..memory.enough import enough_reply
from ..memory.enough import _amounts, _near_bare_range, _target
_enough_reply = enough_reply
from ..memory.relations import (ABOUT_PERSON_ASK, AGE_ADVERB, AGE_AGAIN, AGE_ASK,
                          AGE_AS_A_CAUSE, AGE_COPULA, AGE_DETERMINER, AGE_PERSON_WORD,
                          AGE_RULE_WORD, AGE_SAID, AGE_WORD, AGE_YOU_SAY, ANOTHER_PERSON,
                          BREED_ASK, CHAT_TAIL, CHILD_WORD, GROUP_ASK, GROUP_NAMES_TYPED,
                          GROUP_NAME_ASK, GROUP_WORDS, HAVE_ANY, NAME_AGAIN, PERSON_AFTER,
                          PET_ASK, PLURAL_ANIMAL, THEIR_AGE, THEIR_JOB, THEIR_NAME,
                          THEIR_TASTE_A_YES_NO, THEIR_TASTE_INTO, THEIR_TASTE_WHAT,
                          THEY_ARE_NAMED, THE_KIDS, _PET_WORD, _PLURAL, _a, _a_kept_person,
                          _a_list_of_names, _a_list_of_words, _a_or_any,
                          _a_person_in_the_store, _a_pet_age, _a_plural_list,
                          _a_word_the_store_knows, _age_is_about_a_person, _ages_reply,
                          _ages_sentence, _animal_family, _ask_gender, _called,
                          _canon_relation, _continues_an_about_ask, _did_you_mean,
                          _every_line, _folded, _gender_of, _in_the_group,
                          _just_gave_an_age, _kin_forms, _mentioned_the_group,
                          _more_than_one, _more_than_one_word, _named_person,
                          _newest_first, _one_age, _person_from_pronoun, _pet_age_reply,
                          _pet_ages, _pet_ages_sentence, _pet_named, _plural_person,
                          _pronoun_fits, _pronoun_for, _relation_reply, _relations_of,
                          _same_as_last, _same_name, _same_name_however_they_wrote_it,
                          _same_thing, _the_group_names_typed, _the_group_was_said,
                          _the_group_word, _the_names_a_pronoun_gave,
                          _the_names_of_the_group, _the_names_they_typed, _their_job,
                          _their_taste, _they_like_sentence, _tidy_name,
                          _whether_they_have, _with_article)

from .memory_tables import (
    ASK_WITHOUT_MY,
    CALENDAR_SAID,
    COUNT_ANIMAL,
    COUNT_BARE,
    DAY_ASKS,
    DAY_IT,
    DAY_OF_MONTH,
    DAY_THING,
    ELIDED_AGAIN,
    ELIDED_ASK,
    ELIDED_NAMES,
    ELIDED_NOT_SURE,
    ELIDED_WORDS,
    HOW_MANY_OF_MINE,
    MEMORY_POINTER,
    MISSED_CATCH_UP,
    PLAN_ASKS,
    PLAN_MINE,
    POINTS_BACK,
    SAID_ASK,
    SAID_AS_A_SENTENCE,
    THAT_DATE,
    TIME_ASKS,
    TIME_IT,
    TIME_THING,
    TOPIC_ASK,
    WEEKDAY_WORD,
    WHAT_I_SAID,
    WHEN_ASKS,
    WHEN_END_ASK,
    WHEN_END_WORD,
    WHEN_INVERTED,
    WHEN_INVERTED_SUBJECT,
    WHEN_PLAN,
    WHEN_QUALITY,
    WHEN_START_ASK,
    WHEN_THING,
    WHEN_THING_VERB,
    WHEN_VAGUE,
    WHEN_VERB,
    WHERE_PLAN,
)
















REMIND_QUESTION = re.compile(
    r"\bremind me\b[^.!?]{0,24}\b(?:what|when|where|who|whom|whose|how|which|why|if)\b|"
    r"\bremind me\b(?:[\s,]*(?:again|please))*[\s,]*$", re.I)


NOT_A_FACT = re.compile(r"\bhaven't (?:told|said|mentioned|given|got)\b|\bhaven't your\b"
                        r"|\bdon't know\b|\bnot sure\b|\bnothing comes to mind\b"
                        r"|\bdidn't say\b|\bnever told\b|\bno idea\b", re.I)


def _a_kept_fact_read(text, memory):
    if not isinstance(text, str) or not (user(memory) or {}):
        return False
    try:
        if not recall.ask(text):
            return False
        said = respond(text, copy.deepcopy(memory))
    except Exception:
        return False
    if not said or not str(said).strip():
        return False
    return NOT_A_FACT.search(str(said)) is None


def _their_own_line_ask(text, memory):
    try:
        low = _bare(text) or ""
        if PLAN_MINE.search(low):
            return bool((user(memory) or {}).get("plans") or (user(memory) or {}).get("plan"))
        if not ACTIVITY_ASK.search(low):
            return False
        return bool(_activity_line(memory))
    except Exception:
        return False






NOT_FROM_THE_REPAIR = frozenset("""plan plans drop retract correction""".split())


def _with_repaired(found, text, memory, kind):
    understood = memory.get("understood") if isinstance(memory, dict) else None
    plain = understood.get("plain") if isinstance(understood, dict) else None
    if not isinstance(plain, str) or not plain.strip():
        return found
    if plain == " ".join(str(text).split()):
        return found
    more = extract.extract(plain, question=(kind == "question")) or {}
    for key, value in more.items():
        if key not in NOT_FROM_THE_REPAIR and not found.get(key) and value:
            found[key] = value
    if found.get("others") and more.get("others"):
        for entry in more["others"]:
            if not isinstance(entry, dict) or not entry.get("who"):
                continue
            known = next((one for one in found["others"]
                          if isinstance(one, dict) and one.get("who") == entry["who"]), None)
            if known is None:
                found["others"].append(dict(entry))
                continue
            for key, value in entry.items():
                if key != "who" and not known.get(key):
                    known[key] = value
    return found


NOT_A_NAME_BEFORE = re.compile(r"(?:\b(?:a|an|the|some|another|his|her|their|our|your|my)\s+)$",
                               re.I)
THE_PLACE_IS_NAMED = re.compile(
    r"(?:^|[.!?;:]\s+|\n|\b(?:to|in|into|from|at|near|of|around|through|toward|towards|via|"
    r"going|coming|off|back|flying|travelling|traveling|moving|heading|headed|staying|visiting|"
    r"visit|bound|left)\s*(?:\d+|two|three|four|five|six|seven|eight|nine|ten)?\s*)$", re.I)


def _the_places_are_written_as_names(reply, memory):
    known = user(memory)
    if not isinstance(known, dict) or not isinstance(reply, str) or not reply.strip():
        return reply
    names = [name for name in (known.get("places") or []) if isinstance(name, str) and name.strip()]
    city = known.get("city")
    if isinstance(city, str) and city.strip() and city not in names:
        names.append(city)
    if not names:
        return reply
    out = reply
    for name in names:
        pattern = re.compile(r"(?<![\w'])" + re.escape(name) + r"(?![\w'])", re.I)

        def swap(match, name=name):
            before = match.string[max(0, match.start() - 28):match.start()]
            if NOT_A_NAME_BEFORE.search(before):
                return match.group(0)
            if not THE_PLACE_IS_NAMED.search(before):
                return match.group(0)
            return name

        out = pattern.sub(swap, out)
    return out


def note_the_hours(text, memory):
    if not isinstance(text, str) or not text.strip():
        return
    understood = memory.get("understood") if isinstance(memory, dict) else None
    if isinstance(understood, dict):
        topic = understood.get("topic")
        if topic and topic != "work":
            return
    try:
        from ..memory import ack
        family, _pool = ack._hours_family(text.lower())
    except Exception:
        return
    if family:
        hours_after.note(memory, family)


def _a_detail_does_not_replace_the_job(found, memory):
    if "job" not in found:
        return found
    held = (user(memory) or {}).get("job")
    held_frame = str((user(memory) or {}).get("job_frame") or "")
    said = found.get("job")
    if not held or not said or str(held) == str(said):
        return found
    said_frame = str(found.get("job_frame") or "")
    said_weight = extract.work_weight(said, said_frame)
    if said_weight < extract.work_weight(held, held_frame):
        kept = dict(found)
        kept.pop("job", None)
        kept.pop("job_frame", None)
        if said_weight == 2:
            kept["workplace"] = (said_frame + " " + str(said)).strip()
        else:
            kept["shift"] = said
        return kept
    if extract.is_a_place_of_work(held_frame) and found.get("job_frame") is None:
        if not (user(memory) or {}).get("workplace"):
            found["workplace"] = (held_frame + " " + str(held)).strip()
    if "job_frame" not in found:
        (user(memory) or {}).pop("job_frame", None)
    return found


ASK_OPENERS = frozenset("""what whats which when where who whose why how hows
do does did is are was were am can could should would will shall have has had
any anyone anything""".split())


def _without_the_shrug_at_the_end(text):
    said = " ".join(str(text or "").split())
    words = said.lower().strip(" .,!;:").split()
    if "?" not in said and not (words and words[0] in ASK_OPENERS):
        return said
    clean = without_the_end_shrug(said)
    return clean if clean and clean != said else said


def observe(text, memory):
    before = _the_pets_on_record(memory)
    memory["_pets_before"] = before
    hurt_before = a_hurting_part.before(memory)
    try:
        _observe(text, memory)
    finally:
        memory.pop("_pets_before", None)
    a_hurting_part.after(memory, hurt_before)
    _note_a_pet_that_is_new(text, memory, before)
    try:
        _the_limit_they_share(text, memory)
    except Exception:
        pass


def after(text, reply, memory):
    try:
        a_repair.keep_the_correction(text, memory)
    except Exception:
        pass


AGES_IN_WORDS = {int(number): word for word, number in extract.FIGURE_WORDS.items()}


def _the_ages_of_the_children(text, memory):
    if not isinstance(memory, dict):
        return ""
    held = user(memory).get("kids")
    if not isinstance(held, int) or held < 2:
        return ""
    if any(len(entry.get("ages") or ()) > 1
           for entry in others(memory) if isinstance(entry, dict)):
        return ""
    ages = extract.ages_said_one_by_one(text, held)
    if not ages:
        return ""
    if not (extract.the_ones_are_given_one_at_a_time(text) or _the_count_was_the_line_before(memory)):
        return ""
    remember_other(memory, {"who": "kids", "ages": ages}, text)
    words = [AGES_IN_WORDS.get(age, str(age)) for age in ages]
    said = ", ".join(words[:-1]) + " and " + words[-1] if len(words) > 2 else " and ".join(words)
    return pick(["{} — got it.".format(said[:1].upper() + said[1:]),
                 "Got it — {}.".format(said),
                 "{}.".format(said[:1].upper() + said[1:])], memory)


def _the_count_was_the_line_before(memory):
    said = str((memory.get("topic") or {}).get("text") or "")
    return bool(re.search(r"\b(?:kids?|children|child)\b", said, re.I))


def _the_pets_on_record(memory):
    held = set()
    if not isinstance(memory, dict):
        return held
    for pet in user(memory).get("pets") or ():
        if not isinstance(pet, dict):
            continue
        held.add((str(pet.get("animal") or "").strip().lower(),
                  str(pet.get("name") or "").strip().lower()))
    return held


def _note_a_pet_that_is_new(text, memory, before):
    if not isinstance(memory, dict):
        return None
    held = memory.get("correction")
    if isinstance(held, dict) and held.get("said") == " ".join(str(text or "").lower().split()):
        return None
    added = _the_pets_on_record(memory) - before
    pets = [pet for pet in (user(memory).get("pets") or ()) if isinstance(pet, dict)]
    for animal, name in sorted(added):
        if not animal or not name:
            continue
        same = [pet for pet in pets
                if str(pet.get("animal") or "").strip().lower() == animal and pet.get("name")]
        if len(same) < 2:
            continue
        memory["correction"] = {"key": "pets_more", "value": name, "animal": animal,
                                "said": " ".join(str(text or "").lower().split()),
                                "text": text}
        return memory["correction"]
    return None














def _observe(text, memory):
    from ..memory import not_this as ruled_out_place
    if ruled_out_place.the_place_ruled_out(text, memory):
        return
    understood = memory.get("understood")
    note_the_hours(text, memory)
    how_many.observe(text, memory)
    family_name.observe(text, memory)
    planned = plans.answer(text, memory) if isinstance(text, str) else None
    if planned:
        memory["plan_answer"] = {"text": planned, "user": text}
    kind = understood.get("kind") if isinstance(understood, dict) else None
    if not isinstance(text, str):
        return
    said = _behind_a_remembering_frame(text)
    if said:
        text = said
    if recall.ask(text) or _reads_the_store(text, memory):
        return
    if REMIND_QUESTION.search(text):
        return
    if _asks_about_someone_else(text):
        rest = _after_the_yes_no_frame(text)
        if not rest:
            return
        text = rest
    if isinstance(text, str) and _statement(text):
        return
    decided.observe(text, memory)
    company.observe(text, memory)
    memory.pop("pet_age", None)
    _keep_the_times(text, memory)
    rates_reader.keep(text, memory)
    found = extract.extract(text, question=(kind == "question"))
    if not found:
        found = extract.a_correction_without_a_subject(text, last_user(memory))
    if not found.get("name"):
        answered = _their_name_answered(text, memory)
        if answered:
            found["name"] = answered
    found = _with_repaired(found, text, memory, kind)
    if not found.get("kids"):
        counted = extract.count_of_the_people(text, memory)
        if counted:
            found["kids"] = counted
    if not found.get("budget"):
        folded = _folded(text, memory)
        if folded and folded != " ".join(text.lower().split()):
            budget = extract.extract(folded, question=(kind == "question")).get("budget")
            if budget:
                found["budget"] = budget
    if found.get("budget") and not re.search(r"[\u00a3$\u20ac]", found["budget"]):
        budget = str(found["budget"])
        sign = _budget_sign(text, budget)
        if sign:
            found["budget"] = sign + budget.lstrip()
    correction = found.pop("correction", None)
    if correction is None:
        correction = _a_correction_without_a_marker(text, memory)
    dropped = found.pop("drop", None)
    retracted = found.pop("retract", None)
    if not found.get("allergies"):
        more = extract.one_more(text)
        held = (memory.get("user") or {}).get("allergies") or []
        if more and held:
            found["allergies"] = [item for item in more if item not in held]
    named_here = [who for who in (found.get("people") or []) if isinstance(who, str)]
    _remember_dislikes(text, memory, named_here)
    second = _a_second_persons_limit(text, memory)
    if second:
        found.setdefault("others", []).append(second)
    for entry in found.pop("others", []) or []:
        pronoun = entry.pop("pronoun", None)
        if not entry.get("who"):
            if pronoun and pronoun not in ("she", "he"):
                age = _a_number(entry.get("age"))
                if age:
                    memory["their_age"] = {"age": age, "turns": entry.get("turns") or ""}
                continue
            who = _person_from_pronoun(text, memory, named_here)
            if pronoun:
                fits = extract.SHE if pronoun == "she" else extract.HE
                who = who if _pronoun_fits(who, fits) else ""
            if not who:
                if pronoun in ("she", "he") and isinstance(entry.get("months"), int):
                    entry["pronoun"] = pronoun
                    remember_other(memory, entry, text)
                continue
            entry["who"] = who
        if pronoun and "age" in entry and CORRECTING.search(str(text or "")):
            known = next((one for one in others(memory) if one.get("who") == entry["who"]), None)
            if not (known and "age" in known):
                continue
        was = next((dict(one) for one in others(memory)
                    if one.get("who") == entry.get("who")), None)
        remember_other(memory, entry, text)
        _note_a_corrected_fact(memory, text, entry, was)
        _note_a_fact_moved(memory, text, entry, was)
    found = _a_detail_does_not_replace_the_job(found, memory)
    held_name = str((memory.get("user") or {}).get("name") or "")
    for key, value in found.items():
        remember(memory, key, value, text)
    if (found.get("name") and held_name
            and str(found["name"]).lower() != held_name.lower()):
        memory["name_fixed"] = {"name": str(found["name"]), "from": held_name,
                                "said": " ".join(str(text or "").lower().split())}
    if found.get("job") and not found.get("job_frame"):
        (memory.get("user") or {}).pop("job_frame", None)
    _fix_a_pets_name(text, memory)
    if "pets" not in found:
        _name_the_last_pet(text, memory)
        _age_the_named_pet(text, memory)
        _age_they_answered(text, memory)
        _age_said_of_the_only_animal(text, memory)
        _fix_a_pets_age(text, memory)
    _fix_a_persons_age(text, memory)
    _fix_the_weeks_of_a_pregnancy(text, memory)
    fixed = _fix_a_persons_name(text, memory)
    if fixed:
        memory["name_fixed"] = dict(fixed, said=" ".join(str(text or "").lower().split()))
    if "owns" not in found:
        _fix_the_make_of_a_thing(text, memory)
    _the_name_they_gave_to_the_person_they_mean(text, memory)
    _a_trip_booked_named(text, memory)
    if correction:
        _apply_correction(memory, correction, text)
        _fix_a_pets_name(text, memory)
        return
    if dropped and _drop_value(memory, dropped, text):
        return
    if retracted and _retract_last(memory, text):
        return
    _forget_denied(text, memory)
    _the_back_on_the_plate(text, memory)
    if _about_this_chat(text, memory):
        return
    if told_about.a_callback_the_chat_has(text, memory):
        return
    if not _this_line_put_something_right(memory, text):
        note(memory, text, kind)


def _a_trip_booked_named(text, memory):
    from ..memory import trips
    place, when = trips.the_trip_they_booked(text)
    if not place:
        return
    known = user(memory)
    if not isinstance(known, dict):
        return
    place = place[:1].upper() + place[1:]
    plan = " ".join(f"{place} in {when}".split()) if when else place
    places = [str(one) for one in known.get("places") or [] if str(one).strip()]
    if place.lower() not in {one.lower() for one in places}:
        remember(memory, "places", place, text)
    if str(known.get("plan") or "").strip().lower() != plan.lower():
        remember(memory, "plan", plan, text)
        remember(memory, "plans", plan, text)


def _this_line_put_something_right(memory, text):
    said = " ".join(str(text or "").lower().split())
    if not said:
        return False
    for key in ("correction", "name_fixed"):
        kept = memory.get(key)
        if isinstance(kept, dict) and said == " ".join(str(kept.get("said") or "").split()):
            return True
    return False




def _on_record_before(memory, records):
    said = " ".join(str((turn or {}).get("user") or "").lower()
                    for turn in (memory.get("turns") or []) if isinstance(turn, dict))
    words = {stem(word) for word in re.findall(r"[a-z']+", said)}
    kept = []
    for record in records or []:
        if not isinstance(record, dict):
            continue
        for word in (record.get("animal"), record.get("name")):
            if word and stem(str(word).lower()) in words:
                kept.append(record)
                break
    return kept


def _forget_denied(text, memory):
    held = (memory.get("user") or {}).get("pets") or []
    denied = extract.denials(text, held)
    theirs = denied.pop("theirs", None) if isinstance(denied, dict) else None
    died = [pet for pet in _losses_taking(text, held, memory)
            if str(pet.get("animal") or "") not in
            [_kind(item) for item in (denied.get("pets") or [])]]
    given = [pet for pet in extract.given_away_one(text, held)
             if pet not in [item for item in (denied.get("pets") or []) if isinstance(item, dict)]]
    if not denied and not theirs and not died and not given:
        return None
    gone = {}
    for key, value in denied.items():
        if key == "diet":
            value = _the_diet_they_are_back_on(memory, value)
        dropped = forget(memory, key, value, "gone")
        if key == "pets":
            dropped = _on_record_before(memory, dropped)
        if dropped:
            gone[key] = dropped
            if key == "pets" and "*" in [str(item) for item in value]:
                gone["pets_all"] = True
    if died and forget(memory, "pets", died, "died"):
        gone["pets_died"] = True
    if given and forget(memory, "pets", given, "given away"):
        gone["pets_given"] = True
    for entry in theirs or []:
        taken = _off_their_list(memory, entry, text)
        if taken:
            gone.update(taken)
            break
    if not gone:
        return None
    gone["said"] = " ".join(str(text or "").lower().split())
    memory["denial"] = gone
    return gone


def _the_back_on_the_plate(text, memory):
    for said in extract.their_back(text):
        who = str(said.get("who") or "").strip() or _person_from_pronoun(text, memory)
        if not who:
            continue
        for record in others(memory):
            if str(record.get("who") or "").lower() != who.lower():
                continue
            kind = said.get("kind")
            food = str(said.get("food") or "").strip()
            if food.lower() in ("them", "it", "that"):
                food = _the_one_they_are_back_on(record, kind)
            if not food:
                continue
            if kind == "diet":
                held = str(record.get("diet") or "").lower()
                if held not in ("no " + food.lower(), "no " + food.lower() + "s"):
                    continue
                record["diet"] = "eats " + food
            else:
                gone = [str(item) for item in (record.get("dislikes") or [])]
                if food.lower() not in [item.lower() for item in gone]:
                    continue
                record["dislikes"] = [item for item in gone if item.lower() != food.lower()]
                likes = [str(item) for item in (record.get("likes") or [])]
                if food.lower() not in [item.lower() for item in likes]:
                    likes.append(food)
                record["likes"] = likes
            memory["reversal"] = {"who": who, "food": food, "kind": kind,
                                  "said": " ".join(str(text or "").lower().split())}
            return True
    return False


def _the_one_they_are_back_on(record, kind):
    if kind == "diet":
        held = str(record.get("diet") or "").strip()
        return held[3:].strip() if held.lower().startswith("no ") else ""
    gone = [str(item) for item in (record.get("dislikes") or [])]
    return gone[0] if len(gone) == 1 else ""




def _off_their_list(memory, entry, text):
    items = [str(item) for item in (entry.get("allergies") or []) if str(item)]
    if not items:
        return None
    who = str(entry.get("who") or "") or _person_from_pronoun(text, memory)
    if not who:
        return None
    taken = []
    for record in others(memory):
        if str(record.get("who") or "") != who:
            continue
        held = [str(item) for item in (record.get("allergies") or [])]
        left = [item for item in held if item.lower() not in {one.lower() for one in items}]
        if len(left) == len(held):
            continue
        taken.extend(item for item in held if item not in left)
        record["allergies"] = left
    return {"allergies": items, "who": who}


def _the_diet_they_are_back_on(memory, value):
    held = (memory.get("user") or {}).get("diet")
    said = " ".join(str(value or "").lower().split())
    if not isinstance(held, str) or not said:
        return value
    if said in " ".join(held.lower().split()):
        return held
    return value






def _the_last_line(memory):
    turns = (memory or {}).get("turns") or []
    if not turns:
        return ""
    return str((turns[-1] or {}).get("user") or "")































def _losses_taking(text, held, memory=None):
    said = str(text or "").lower()
    everything = bool(extract.LOSS_ALL.search(said))
    taken = []
    before = _the_last_line(memory)
    for kind in extract.losses(text, held, before):
        same = [pet for pet in held if isinstance(pet, dict)
                and _animal_family(pet.get("animal")) == _animal_family(kind)]
        if not same:
            continue
        if everything:
            taken.extend(pet for pet in same if pet not in taken)
            continue
        named = [pet for pet in same if pet.get("name") and
                 re.search(r"\b" + re.escape(str(pet["name"]).lower()) + r"\b", said)]
        taken.append(named[-1] if named else same[-1])
    return taken




def _last_stated(memory):
    said = " ".join(str(last_user(memory) or "").lower().split())
    if not said:
        return []
    kept = []
    for entry in log(memory):
        if not isinstance(entry, dict):
            continue
        if " ".join(str(entry.get("text") or "").lower().split()) != said:
            continue
        kept.append(entry)
    return kept


def _retract_last(memory, text=""):
    gone, shown = [], []
    for entry in _last_stated(memory):
        key = entry.get("key")
        value = entry.get("value")
        if key == "pet":
            known = user(memory)
            pets = [pet for pet in (known.get("pets") or []) if pet is not value and pet != value]
            if len(pets) != len(known.get("pets") or []):
                if pets:
                    known["pets"] = pets
                else:
                    known.pop("pets", None)
                gone.append("pets")
                animal = (value or {}).get("animal") or (value or {}).get("name") or "pet"
                shown.append(str(animal))
            continue
        if key == "plans":
            known = user(memory)
            if forget(memory, "plans", [value]):
                gone.append("plans")
                shown.append(str(value))
            if known.get("plan") == value:
                known.pop("plan", None)
            continue
        if key in NOT_RETRACTED:
            continue
        dropped = forget(memory, key, value)
        if dropped:
            gone.append(key)
            shown.extend(str(item) for item in dropped
                         if not isinstance(item, dict))
    if not gone:
        return None
    if any(key in ("plans", "places") for key in gone):
        user(memory)["plan_dropped"] = str(shown[0])
    memory["retraction"] = {"said": " ".join(str(text or "").lower().split()),
                            "keys": gone, "shown": shown}
    return memory["retraction"]




def _reads_the_store(text, memory=None):
    if not isinstance(text, str):
        return False
    low = _bare(_folded(text, memory))
    if NAMED_FACT_ASK.search(low) or TOPIC_ASK.search(low) or ASK_WITHOUT_MY.search(low) \
            or HOW_MANY_OF_MINE.search(low):
        return True
    if not (OTHER_FACT.search(low) or CANT_HAVE.search(low) or CAN_HAVE.search(low)
            or CAN_THEY_HAVE.search(low)
            or _a_bare_limit_ask(low, memory)):
        return False
    if not _asks_about_someone(low, text, memory):
        return False
    whole = " ".join(str(text or "").lower().split())
    if STATES_A_LIMIT.search(whole) and not A_HAVE_QUESTION.search(whole):
        return False
    said = _other_person_reply(memory or {}, low)
    return bool(said)



NAMED_FACT_ASK = re.compile(
    r"\bwhat(?:'s|s| is| are| was| were)?\s+my\s+" + _FACT_SLOT + r"\b|"
    r"\bwhat\s+(?:is|are|was|were)\s+my\s+" + _FACT_SLOT + r"\b|"
    r"\bwhere do i (?:work|live|come from)\b(?=\s*(?:[?.!,;:]|$)|\s+(?:now|again|then|at|from|"
    r"these|days|properly|though|honestly|anymore|either|oh|wait|sorry|hmm|actually|um|right|"
    r"please|thanks)\b)|\bwhat do i work as\b|\bwho am i\b|"
    r"\bhow old am i\b|\bwhat do i do for a living\b", re.IGNORECASE)
def _the_plan_they_took_back(text, memory):
    if not isinstance(memory, dict):
        return False
    gone = user(memory).get("plan_dropped")
    if not isinstance(gone, str) or not gone.strip():
        return False
    low = " ".join(str(text or "").lower().split())
    return bool(WHERE_PLAN.search(low))

def _the_clock_in_their_line(text, memory):
    try:
        low = text.lower()
        if not (TIME_ASKS.search(low) or TIME_THING.search(low) or TIME_IT.search(low)
                or DAY_THING.search(low) or DAY_IT.search(low)):
            return False
        return bool(_plans_reply(memory, low))
    except Exception:
        return False


ASK_ABOUT_THEM = re.compile(
    r"^\W*(?:is|are|does|do|did|was|were|can|could|has|have|will)\b|"
    r"\bwhat (?:does|do|did|can|could|is|are|was|were) "
    r"(?:he|she|they|your|my|his|her|their)\b|"
    r"\bwhat(?:'s|s| is| are)\s+(?:my|his|her|their|he|she|they)\b", re.I)


def _an_ask_about_someone_else(text, memory):
    if not isinstance(text, str) or not isinstance(memory, dict):
        return False
    if not ASK_ABOUT_THEM.search(text.strip()):
        return False
    keys = []
    if OTHER_FACT.search(text):
        keys.append("allergies")
    if EAT_ASK.search(text):
        keys.append("diet")
    if not keys:
        return False
    try:
        who = _someone_else_named(_bare(_folded(text, memory)), memory)
    except Exception:
        return False
    if not who:
        return False
    for known in others(memory):
        if known.get("who") == who:
            return any(known.get(key) for key in keys)
    return False


def _the_take_back_about_someone(text, memory):
    gone = memory.get("denial") if isinstance(memory, dict) else None
    if not isinstance(gone, dict) or not gone.get("who"):
        return False
    return gone.get("said") == " ".join(str(text or "").lower().split())


def _the_part_that_hurts_asked(text, memory):
    if not isinstance(memory, dict):
        return False
    low = " ".join(str(text or "").lower().split())
    return bool(low) and bool(a_hurting_part.the_part_asked(memory, low))


def _the_store_readings(text, memory=None):
    if (_reads_the_store(text, memory) or _their_own_line_ask(text, memory)
            or _the_part_that_hurts_asked(text, memory)
            or _their_fact_ask(text, memory)
            or _a_kept_fact_read(text, memory)
            or decided.asks(text)
            or told_about.ABOUT_THE_CHAT(text, memory)
            or told_about.A_CALLBACK(text, memory)):
        return True
    if WHOLE_ASK.match(str(text or "").strip().lower()) \
            and _a_whole_answer_to_hand_back(memory, text):
        return True
    if _a_state_that_was(text, memory, ""):
        return True
    if _a_feeling_about_their_own_news(text, memory):
        return True
    if _the_plan_they_took_back(text, memory):
        return True
    if _the_take_back_about_someone(text, memory):
        return True
    if _can_close(text, memory):
        return True
    if _the_call_from_the_advice(text, memory):
        return True
    if _asks_whether_we_followed(text, memory):
        return True
    if rates_reader.is_a_rate_ask(text, memory):
        return True
    if _a_plain_time_ask(text, memory):
        return True
    if _an_ask_about_someone_else(text, memory):
        return True
    if _the_group_size_ask(text, memory):
        return True
    if repeat_the_line.how_long_its_been(text) and repeat_the_line.the_figure_they_gave(
            text, memory):
        return True
    if _the_figure_the_answer_names(text, memory):
        return True
    if _the_budget_on_the_answer(text, memory):
        return True
    if _the_back_this_turn(text, memory):
        return True
    if _the_same_fact_about_someone(text, memory):
        return True
    try:
        if not isinstance(text, str) or not isinstance(memory, dict):
            return False
        line = _bare(_folded(text, memory))
        if (POINTS_BACK_AT_IT.search(line) or WORK_ON_IT.search(line)) \
                and not _the_prep_day(memory, line):
            return False
        if _the_clock_in_their_line(text, memory):
            return True
        if "when" not in text.lower():
            return _a_count_from_the_date(text, memory)
        return bool(when_answer(text, memory))
    except Exception:
        return False
        return False














PERSON_ADVICE_ASK = re.compile(
    r"^\W*(?:can|could|should|shall|would|will|may|might|is it (?:ok|okay|fine|safe)|"
    r"what can|what could|what should|how (?:do|can|should)|any (?:tips|ideas|advice|"
    r"suggestions|ways))\b", re.I)




















def _their_fact_ask(text, memory=None):
    if not isinstance(text, str):
        return False
    low = _bare(_folded(text, memory))
    if PERSON_ADVICE_ASK.match(low) and not (CAN_THEY_HAVE.search(low)
                                             and _a_limit_kept_for_them(low, memory)):
        return False
    undeclared = _the_person_still_in_hand(low, memory)
    if not (undeclared or OTHER_FACT.search(low) or EAT_ASK.search(low)
            or CANT_HAVE.search(low) or CAN_HAVE.search(low) or CAN_THEY_HAVE.search(low)):
        return False
    if not (undeclared or _asks(low) or "?" in text or _asks_about_someone_else(text)):
        return False
    if not (undeclared or THEM.search(low) or _named_person(low)
            or re.search(r"\bmy\s+(?:" + _RELATION + r")\b(?!'s|s\b)(?!s\b)", low)):
        return False
    if CAN_THEY_HAVE_A_FOOD.search(low) and not _a_limit_kept_for_them(low, memory):
        return False
    said = _other_person_reply(memory, low)
    if not said:
        return False
    if NO_RECORD.search(said):
        return False
    return True


def _name_the_last_pet(text, memory):
    if not isinstance(text, str):
        return
    pets = user(memory).get("pets")
    named = pets[-1] if isinstance(pets, list) and pets and isinstance(pets[-1], dict) else {}
    name = extract.pet_name_only(text, lower=bool(named)) or _name_they_answered(text, memory)
    if not name:
        return
    if not isinstance(pets, list) or not pets:
        animal = _the_animal_of_the_pick(memory)
        if not animal or animal == "pet":
            return
        remember(memory, "pets", [{"animal": animal, "name": name}], text)
        return
    last = pets[-1]
    if isinstance(last, dict) and not last.get("name"):
        last["name"] = name
        kept = {"animal": last.get("animal", "pet"), "name": name}
        if isinstance(last.get("count"), int) and last["count"] > 1:
            kept["count"] = last["count"]
        remember(memory, "pets", [kept], text)
        return
    if isinstance(last, dict) and str(last.get("name") or "").lower() != name.lower() \
            and (CORRECTS_A_NAME.match(text) or CORRECTS_A_NAME_POSSESSIVE.match(text)) \
            and not _names_a_pet_here(text, memory):
        before = str(last.get("name") or "")
        last["name"] = name
        log(memory).append({"key": "pet", "value": {"animal": last.get("animal"), "name": name},
                            "turn": len(memory.get("turns") or []), "text": text})
        if before and before.lower() != name.lower():
            was = [str(old) for old in (last.get("was") or []) if str(old).lower() != name.lower()]
            last["was"] = was + [before]
        if before:
            memory["correction"] = {"key": "pet", "value": name,
                                    "animal": last.get("animal") or "pet",
                                    "said": " ".join(str(text or "").lower().split())}


def _the_animals_named(text, memory):
    low = " ".join(str(text or "").lower().split())
    here = set()
    for pet in (user(memory).get("pets") or ()):
        if not isinstance(pet, dict) or not pet.get("animal"):
            continue
        animal = str(pet["animal"]).lower()
        if re.search(r"\b" + re.escape(animal) + r"s?\b", low):
            here.add(animal)
    return here


def _the_name_it_had(animal, said, memory):
    for entry in reversed(log(memory) or ()):
        value = entry.get("value") if isinstance(entry, dict) else None
        if not isinstance(value, dict):
            continue
        if str(value.get("animal") or "").lower() != animal:
            continue
        name = str(value.get("name") or "")
        if name and name.lower() != str(said or "").lower():
            return name
    return ""


def _names_a_pet_here(text, memory):
    low = " ".join(str(text or "").lower().split())
    for pet in (user(memory).get("pets") or ()):
        if not isinstance(pet, dict) or not pet.get("animal"):
            continue
        if re.search(r"\b" + re.escape(str(pet["animal"]).lower()) + r"s?\b", low):
            return True
    return False


CORRECTS_A_NAME = re.compile(r"^\W*(?:(?:no|nope|sorry|actually|oops|wait|hold on|correction)"
                             r"[,.]?\s+)", re.I)
CORRECTS_A_NAME_POSSESSIVE = re.compile(
    r"^\W*(?:his|her|its|their)\s+names?\s+(?:actually|really)\s+", re.I)


AGE_IN_WORDS = "|".join(sorted(extract.FIGURE_WORDS, key=len, reverse=True))


def _the_figure_said(match):
    said = str(match.group("age") or "").strip().lower()
    if not said:
        return None
    value = _a_number(extract.FIGURE_WORDS.get(said, said))
    return value if isinstance(value, int) else None


PET_NAME_AGE = re.compile(r"^\W*(?:[a-z][a-z'-]{2,20})\s+(?:is|was|are|were)\s+"
                          r"(?P<age>\d{1,2}|" + AGE_IN_WORDS + r")(?![\d.,]\d)(?!\s+of\b)"
                          r"(?!\s*(?:kg|kilo\w*|lbs?|pounds?|stone|st|cm|metres?|meters?|"
                          r"miles?|hours?|mins?|minutes?|percent|%))"
                          r"\s*(?P<unit>months?|weeks?)?\b", re.I)


PET_LEAD_IN = re.compile(r"^(?:and|also|oh|but|well|yeah|yes|no|sorry|actually|ok|okay|right|"
                         r"wait|god|hang on)\b[\s,]*", re.I)


def _without_a_lead_in(text):
    said = str(text or "").strip()
    for _ in range(4):
        shorter = PET_LEAD_IN.sub("", said, count=1)
        if shorter == said:
            break
        said = shorter.strip()
    return said


def _put_a_pets_age(pet, age, unit, text):
    if pet.get("age") == age and str(pet.get("unit") or "") == unit:
        return None
    pet["age"] = age
    pet.pop("unit", None)
    if unit:
        pet["unit"] = unit
    return {"key": "pet", "value": dict(pet), "text": text}












def _age_the_named_pet(text, memory):
    if not isinstance(text, str):
        return None
    low = _without_a_lead_in(text).lower()
    match = PET_NAME_AGE.match(low)
    if not match:
        return None
    age = _the_figure_said(match)
    if not 0 < age <= 30:
        return None
    unit = "months" if str(match.group("unit") or "").lower().startswith("month") else ""
    said = low.strip().split()[0].strip(".,!?") if low.strip() else ""
    pets = user(memory).get("pets")
    if not isinstance(pets, list):
        return None
    for pet in reversed(pets):
        if not isinstance(pet, dict) or str(pet.get("name") or "").lower() != said:
            continue
        return _put_a_pets_age(pet, age, unit, text)
    return None


def _fix_a_pets_age(text, memory):
    said = " ".join(str(text or "").lower().split())
    low = _without_a_lead_in(said)
    if not low or len(low.split()) > PET_AGE_FIX_WORDS or not CORRECTING.search(said):
        return None
    if _PET_WORD.search(low):
        return None
    match = AGE_FIX.search(low)
    if not match:
        return None
    age = _the_figure_said(match)
    if not 0 < age <= 30:
        return None
    who = _person_from_pronoun(low, memory)
    if who and any(str(known.get("who") or "") == who and "age" in known
                   for known in others(memory)):
        return None
    unit = "months" if re.search(r"\bmonths?\b", low) else ""
    aged = [pet for pet in (user(memory).get("pets") or [])
            if isinstance(pet, dict) and pet.get("age") is not None]
    if len(aged) != 1:
        return None
    return _put_a_pets_age(aged[0], age, unit, text)


PET_AGE_ANSWER = re.compile(r"^\W*(?:(?:he|she|it|they)(?:'s|s|\s+is|\s+are|\s+is\s+now)?\s+)?"
                            r"(?P<age>\d{1,2}|" + AGE_IN_WORDS + r")\s*"
                            r"(?P<unit>years?|months?|weeks?)?\s*(?:old)?\W*$", re.I)


def _age_said_of_the_only_animal(text, memory):
    said = " ".join(str(text or "").lower().split())
    if not said or len(said.split()) > 5:
        return None
    previous = " ".join(str(last_user(memory) or "").lower().split())
    pets = [pet for pet in (user(memory).get("pets") or []) if isinstance(pet, dict)]
    if len(pets) == 1:
        pet = pets[0]
    else:
        named = [one for one in pets
                 if len(str(one.get("name") or "").strip()) > 2
                 and re.search(r"\b" + re.escape(str(one["name"]).strip().lower()) + r"\b",
                               previous)]
        if len(named) != 1:
            return None
        pet = named[0]
    if int(pet.get("count") or 1) > 1:
        return None
    name = str(pet.get("name") or "").strip().lower()
    called = [str(pet.get(word) or "").strip().lower() for word in ("animal", "breed")]
    if not (_PET_WORD.search(previous)
            or (len(name) > 2 and name in previous)
            or any(len(word) > 2 and word in previous for word in called)):
        return None
    if not re.search(r"\b(?:he|she|it|they)(?:'s|s|\s+is|\s+are)?\b", said):
        return None
    match = PET_AGE_ANSWER.match(said)
    if not match:
        return None
    age = _the_figure_said(match)
    if not 0 < age <= 30:
        return None
    if _person_from_pronoun(said, memory):
        return None
    unit = str(match.group("unit") or "").lower()
    unit = "months" if unit.startswith("month") else ("weeks" if unit.startswith("week") else "")
    return _put_a_pets_age(pet, age, unit, text)


def _age_they_answered(text, memory):
    turns = memory.get("turns")
    if not isinstance(turns, list) or not turns or not isinstance(turns[-1], dict):
        return None
    asked = str(turns[-1].get("bot") or "")
    if "how old" not in asked.lower():
        return None
    pets = [pet for pet in (user(memory).get("pets") or []) if isinstance(pet, dict)]
    if not pets:
        return None
    names = [str(pet.get("name") or "").strip().lower() for pet in pets]
    if not (_PET_WORD.search(asked) or any(
            name and re.search(r"\b" + re.escape(name) + r"\b", asked.lower()) for name in names)):
        return None
    match = PET_AGE_ANSWER.match(str(text or ""))
    if not match:
        return None
    age = _the_figure_said(match)
    if not 0 < age <= 30:
        return None
    unit = str(match.group("unit") or "").lower()
    unit = "months" if unit.startswith("month") else ("weeks" if unit.startswith("week") else "")
    for pet in reversed(pets):
        if pet.get("age") == age and str(pet.get("unit") or "") == unit:
            return None
        pet["age"] = age
        pet.pop("unit", None)
        if unit:
            pet["unit"] = unit
        memory["pet_age"] = dict(pet)
        return {"key": "pet", "value": dict(pet), "text": text}
    return None


def _their_name_answered(text, memory):
    turns = memory.get("turns")
    if not isinstance(turns, list) or not turns or not isinstance(turns[-1], dict):
        return None
    if user(memory).get("name"):
        return None
    asked = str(turns[-1].get("bot") or "")
    if memory.get("asked_for") != "name" or not extract.USER_NAME_ASKED.search(asked):
        return None
    answered = extract.without_the_hedges(text)
    match = extract.NAME_ANSWER_ANNOUNCED.match(answered)
    if match:
        return extract.reads_as_a_name(match.group(1))
    last = extract.NAME_ANSWER_ANNOUNCED_LAST.search(answered)
    if last:
        return extract.reads_as_a_name(last.group(1))
    return extract.reads_as_a_name(answered)










from bot.memory.corrected import (
    AMOUNT,
    ANY_NUMBER,
    ASK_START,
    AT_TIME,
    A_DAY_BEFORE_A_MONTH,
    A_DAY_SAID_LONG,
    A_UNIT_SAID,
    BARE_HOUR,
    BARE_NEW_COUNT,
    CORRECTABLE,
    COUNT_SAID,
    CURRENCY,
    DATE_DAY,
    DATE_PHRASE,
    DAY_WORD,
    MADE_OF_A_VALUE,
    MONTHS,
    MONTH_ALT,
    MONTH_WORD,
    MONTH_WORDS,
    NAMING_VERB,
    NOT_A_FACT_OF_THEIRS,
    NO_SUBJECT_OF_ITS_OWN,
    NUMBER_DIGITS,
    NUMBER_VALUE,
    NUMBER_WORD,
    OTHER_BARE_NUMBER,
    RELATIVE_MONTH,
    STILL_THE_SAME_PERSON,
    _a_bare_hour,
    _a_birthday_for_somebody,
    _a_birthday_on_the_last_line,
    _a_count,
    _a_day_in_the_kind,
    _a_day_written_the_way_the_store_writes_it,
    _a_name_for_a_person,
    _a_name_the_store_keeps,
    _a_new_name_was_said,
    _a_relative_line,
    _a_relative_month,
    _a_spelling_of,
    _a_word_of_a_name,
    _an_amount_on_the_measure,
    _apply_correction,
    _asks,
    _birthday_words,
    _carries,
    _clock_key,
    _correct_a_persons_name,
    _correct_birthday,
    _correct_clock,
    _correct_count,
    _correct_date,
    _correct_fact,
    _correct_number,
    _correct_other,
    _correct_plan,
    _correct_the_count_on_the_table,
    _correct_their_birthday,
    _correct_when,
    _count_said,
    _date_in_plan,
    _date_said,
    _date_word,
    _date_word_case,
    _denies_and_names,
    _drop_wrong,
    _fact_naming,
    _keep_unit,
    _kind_of_value,
    _letters_apart,
    _make_corrects,
    _many,
    _measured_the_same,
    _names_a_half_of_the_day,
    _number_belongs_to_that_age,
    _number_in,
    _plan_saying,
    _plan_the_line_named,
    _plan_told_line,
    _stated_families,
    _stated_last,
    _stated_plan,
    _swap_in,
    _the_line_is_about_that_birthday,
    _the_person_the_plan_is_about,
    _the_plan_before,
    _the_plan_on_the_table,
    _the_topic_with_the_new_clock,
    _the_unit,
    _what_took_its_place,
    _without_the_naming_verb,
)
from bot.memory.store_replies import (A_HAVE_QUESTION, _a_bare_limit_ask, ACTIVITY_ASK, ANSWER_MODULES, ASK_WITHOUT_MY, BARE_WHAT_I_DO, CANT_HAVE, CAN_HAVE, CAN_THEY_HAVE, CAN_THEY_HAVE_A_FOOD, CHECK_FOLLOWED, DAY_IT, DAY_THING, EAT_ASK, FIRST_ASK, MONTHS, NO_RECORD, OTHER_FACT, PLAN_MINE, POINTS_BACK_AT_IT, THEM, TIME_ASKS, TIME_IT, TIME_THING, TOPIC_ASK, WHERE_PLAN, WHOLE_ASK, YES_NO_ASK, _RELATION, _a_feeling_about_what_they_said, _a_limit_kept_for_them, _a_number, _a_state_that_was, _a_thing, _a_whole_answer_to_hand_back, _about_the_bot_here, _about_this_chat, _activity_line, _after_the_yes_no_frame, _age_compare, _animal_family, _asks, _asks_about_someone, _at_the_clock, _bare, _behind_a_remembering_frame, _can_close, _canon_relation, _corrects, _count_of_a_kind, _diet_reply, _folded, _halves, _how_far_along, _is_or_are, _kind, _longest, _name_they_answered, _named_person, _names_its_thing, _names_minutes, _names_the_thing, _other_person_reply, _person_from_pronoun, _plain_line, _plans_reply, _reads_as_the_invitation, _remembers_fact, _repeat_ask, _restated, _says_something, _says_the_verb, _seconds, _sentences, _someone_else_named, _statement, _summary_reply, _swapped_lines, _the_animal_of_the_pick, _the_back_this_turn, _the_bot_name, _the_budget_on_the_answer, _the_call_from_the_advice, _the_condition, _the_job_was_just_said, _the_limit_the_last_line_gave, _the_limit_they_share, _the_person_still_in_hand, _the_plans_in_date_order, _the_prep_day, STATES_A_LIMIT, _the_same_fact_about_someone, _the_store_reply, _the_things, _told_phrase, _vary, _which_comes_first, _who_is_the_name_reply, _yours, ack, company, content, current, decided, enough_reply, extract, family_name, forget, guest, how_many, last_user, name, note, others, pick, plans, rates_reader, re, recall, recent, remember, remember_other, reminded, stem, thread, told_about, units, until_answer, user, when_answer, REPEAT_WORDS, asks_again)













AGE_FIX = re.compile(r"\b(?:he|she|they)(?:'s|s| is| are| was)\s+(?:now\s+)?"
                     r"(?P<age>\d{1,3}|" + AGE_IN_WORDS + r")\b(?!\s+of\b)",
                     re.I)
CORRECTING = re.compile(r"\b(?:actually|no|nope|sorry|wait|i mean|i meant|make it|makes it)\b",
                        re.I)


def _fix_a_persons_age(text, memory):
    low = " ".join(str(text or "").lower().split())
    if not low or len(low.split()) > AGE_FIX_WORDS or not CORRECTING.search(low):
        return None
    match = AGE_FIX.search(low)
    if not match:
        return None
    age = _the_figure_said(match)
    if not 0 <= age <= 120:
        return None
    who = _person_from_pronoun(low, memory)
    if not who:
        return None
    for known in others(memory):
        if known.get("who") == who and "age" in known:
            known["age"] = age
            known.pop("turns", None)
            log(memory).append({"key": "other", "value": dict(known),
                                "turn": len(memory.get("turns") or []), "text": text})
            return known
    return None


WEEKS_FIX = re.compile(r"\b(?P<weeks>\d{1,2})\s*(?:weeks?|wks?)\b", re.I)


def _fix_the_weeks_of_a_pregnancy(text, memory):
    low = " ".join(str(text or "").lower().split())
    if not low or len(low.split()) > 8:
        return None
    match = WEEKS_FIX.search(low)
    if not match:
        return None
    if PREGNANCY_SAID_AGAIN.search(low):
        return None
    weeks = int(match.group("weeks"))
    if not 1 <= weeks <= 45:
        return None
    if not (CORRECTING.search(low) or re.search(r"\b(?:now|today)\b", low)):
        return None
    said_mine = re.search(r"\b(?:im|i'm|i am|i)\b", low)
    said_theirs = re.search(r"\b(?:my|our|she|he|they|her|his|their|hers)\b", low)
    own = user(memory) or {}
    if said_mine and not said_theirs and own.get("pregnant"):
        remember(memory, "weeks", weeks, text)
        return dict(own, weeks=weeks)
    who = _person_from_pronoun(low, memory)
    if not who:
        return None
    for known in others(memory):
        if known.get("who") == who and known.get("pregnant") and "weeks" in known:
            known["weeks"] = weeks
            known.pop("turns", None)
            log(memory).append({"key": "other", "value": dict(known),
                                "turn": len(memory.get("turns") or []), "text": text})
            return known
    return None


PREGNANCY_SAID_AGAIN = re.compile(r"\b(?:pregnant|expecting)\b", re.I)


NAME_FIX = re.compile(
    r"\b(?:(?:he|she|they)(?:'s|s| is| was)?\s+(?:actually\s+|really\s+)?(?:called|named)"
    r"|(?:his|her|their)\s+names?\s+(?:is|was|actually|really))\s+"
    r"(?P<name>[a-z][a-z'\u2019-]{1,19})\b", re.I)
NAME_NOT_A_NAME = frozenset("""not called named now really also still a an the""".split())
A_NAME_AFTER_A_PRONOUN = re.compile(
    r"\b(?:he|she|they)(?:'s|s| is| was)\s+(?P<name>[a-z][a-z'\u2019-]{1,19})\s*[,.!]?$", re.I)

A_NAME_WITH_ITS_VERB = re.compile(r"\b(?:called|named)\s+(?P<name>[A-Za-z][A-Za-z'-]{1,19})\b",
                                  re.I)


def _fix_a_pets_name(text, memory):
    from ..memory import rename as pet_rename
    low = " ".join(str(text or "").lower().split())
    moves = pet_rename.moves(low)
    if not low or len(low.split()) > NAME_FIX_WORDS or not (CORRECTING.search(low) or moves):
        return None
    match = A_NAME_WITH_ITS_VERB.search(low)
    raw = ""
    if match:
        raw = match.group("name") or ""
    elif moves:
        raw = pet_rename.the_name_a_line_moved_on(
            low, user(memory).get("pets"), bool(extract.PETS.search(low)))
    if not raw:
        return None
    said = extract._finish(raw)
    if not said or extract._not_a_name(raw, strict_ly=False):
        return None
    pets = [pet for pet in (user(memory).get("pets") or ()) if isinstance(pet, dict)]
    named = [pet for pet in pets if pet.get("name")]
    target = None
    if _names_a_pet_here(text, memory):
        if _another_animal_is_named(text):
            return None
        for animal in sorted(_the_animals_named(text, memory)):
            kept = _pets_of(animal, pets)
            if not kept:
                continue
            filed = [pet for pet in kept if _a_pet_new_this_line(pet, memory)]
            older = [pet for pet in kept if not _a_pet_new_this_line(pet, memory)]
            if older:
                target = older[-1]
                if str(target.get("name") or "").lower() != said.lower():
                    target["name"] = said[:1].upper() + said[1:]
                    target.pop("turns", None)
                    was = _the_name_it_had(animal, said, memory)
                    if was and not (isinstance(memory.get("correction"), dict)
                                    and memory["correction"].get("said") == low):
                        memory["correction"] = {"key": "pet", "value": target["name"],
                                                "wrong": was[:1].upper() + was[1:],
                                                "animal": animal, "said": low, "text": text}
                for pet in filed:
                    if pet is not target and pet in (user(memory).get("pets") or ()):
                        user(memory)["pets"].remove(pet)
                return None
            for pet in filed:
                pet["name"] = said[:1].upper() + said[1:]
                was = _the_name_it_had(animal, said, memory)
                if was and not (isinstance(memory.get("correction"), dict)
                                and memory["correction"].get("said") == low):
                    memory["correction"] = {"key": "pet", "value": pet["name"],
                                            "wrong": was[:1].upper() + was[1:],
                                            "animal": animal, "said": low, "text": text}
            return None
    if _another_animal_is_named(text):
        return None
    here = [pet for pet in pets
            if pet.get("animal")
            and re.search(r"\b" + re.escape(str(pet["animal"]).lower()) + r"s?\b", low)]
    here = [pet for pet in here if str(pet.get("name") or "").lower() != said.lower()]
    if len(here) == 1:
        target = here[0]
    else:
        for key in ("name", "animal"):
            found = [pet for pet in named if _the_turn_before_said(pet.get(key), memory)]
            if found:
                target = found[-1]
                break
    if target is None:
        return None
    before = str(target.get("name") or "")
    if before.lower() == said.lower():
        return None
    target["name"] = said[:1].upper() + said[1:]
    target.pop("turns", None)
    kept_note = memory.get("correction")
    if not (isinstance(kept_note, dict) and kept_note.get("said") == low):
        memory["correction"] = {"key": "pet", "value": target["name"],
                                "wrong": before[:1].upper() + before[1:],
                                "animal": str(target.get("animal") or "pet"),
                                "said": low, "text": text}
    animal = str(target.get("animal") or "").lower()
    for other in list(pets):
        if other is target:
            continue
        if (str(other.get("animal") or "").lower() == animal
                and str(other.get("name") or "").lower() == said.lower()):
            pets.remove(other)
    user(memory)["pets"] = pets
    log(memory).append({"key": "pet", "value": dict(target),
                        "turn": len(memory.get("turns") or []), "text": text})
    return target


ANOTHER_ANIMAL = re.compile(r"\b(?:other|second|another|also|third)\b", re.I)


def _pets_of(animal, pets):
    return [pet for pet in pets if isinstance(pet, dict)
            and str(pet.get("animal") or "").strip().lower() == animal]


def _a_pet_new_this_line(pet, memory):
    held = memory.get("_pets_before") if isinstance(memory, dict) else None
    if not isinstance(held, set) or not isinstance(pet, dict):
        return False
    return (str(pet.get("animal") or "").strip().lower(),
            str(pet.get("name") or "").strip().lower()) not in held


def _another_animal_is_named(text):
    return bool(ANOTHER_ANIMAL.search(" ".join(str(text or "").lower().split())))


def _two_of_the_animal_are_kept(pets, animal):
    kept = [pet for pet in pets if isinstance(pet, dict)
            and str(pet.get("animal") or "").lower() == animal]
    return len(kept) > 1


def _the_turn_before_said(word, memory):
    turns = memory.get("turns")
    if not word or not isinstance(turns, list) or not turns:
        return False
    last = next((turn for turn in reversed(turns) if isinstance(turn, dict)), None)
    said = " ".join(str((last or {}).get("user") or "").lower().split())
    if not said:
        return False
    return bool(re.search(r"\b" + re.escape(str(word).lower()) + r"s?\b", said))


CORRECTS_A_MAKE = re.compile(
    r"\b(?:sorry|actually|no|i mean|make that|or)?[\s,]*(?:its|it's|it is)\s+"
    r"(?:actually\s+|really\s+|just\s+)?(?:a|an|the)\s+(?P<value>[a-z0-9][a-z0-9' .+-]{0,31})$",
    re.I)


def _fix_the_make_of_a_thing(text, memory):
    line = " ".join(str(text or "").strip().split())
    if not line or line.endswith("?") or len(line.split()) > 6:
        return
    match = CORRECTS_A_MAKE.search(line.lower())
    if not match:
        return
    held = user(memory).get("owns")
    if not isinstance(held, dict) or not held:
        return
    fits = {}
    for thing in held:
        name = extract._the_model(match.group("value"), thing)
        if name:
            fits[thing] = name
    if not fits:
        return
    last_said = []
    for entry in log(memory):
        if entry.get("key") == "owns":
            last_said.extend(entry.get("value") or {})
    thing = next((one for one in reversed(last_said) if one in fits), next(iter(fits), ""))
    name = fits.get(thing, "")
    if not name or name == held.get(thing):
        return
    remember(memory, "owns", {thing: name}, text)


def _fix_a_persons_name(text, memory):
    low = " ".join(str(text or "").lower().split())
    if not low or len(low.split()) > NAME_FIX_WORDS or not CORRECTING.search(low):
        return None
    match = NAME_FIX.search(low)
    bare = None
    if not match:
        bare = A_NAME_AFTER_A_PRONOUN.search(low)
        if not bare:
            return None
        word = bare.group("name").strip("'\u2019")
        if (word in extract.COMMON_WORDS or word in extract.JOB_WORDS
                or word in extract.KIN or extract._not_a_name(word, strict_ly=False)):
            return None
        match = bare
    said = match.group("name").strip("'\u2019")
    if not said or said in NAME_NOT_A_NAME or extract._not_a_name(said, strict_ly=False):
        return None
    name = extract._tidy(extract._finish(said) or "")
    if not name:
        return None
    about = re.sub(r"\bhis\b(\s+name)", r"he\1", low)
    about = re.sub(r"\bher\b(\s+name)", r"she\1", about)
    who = _person_from_pronoun(about, memory)
    if not who and bare:
        return None
    if not who:
        named = [entry for entry in others(memory) if entry.get("name")]
        if len(named) != 1:
            return None
        who = str(named[0].get("who") or "")
    for known in others(memory):
        if known.get("who") == who and known.get("name"):
            before = str(known.get("name") or "")
            if bare and before.lower() == extract._tidy(name).lower():
                return None
            known["name"] = extract._tidy(name)
            known.pop("turns", None)
            log(memory).append({"key": "other", "value": dict(known),
                                "turn": len(memory.get("turns") or []), "text": text})
            return {"who": who, "name": str(known["name"]), "from": before}
    return None


NAME_GIVEN = re.compile(
    r"\b(?:he|she|they)(?:'s|s| is| was)?\s+(?:called|named)\s+(?P<name>[a-z][a-z'\-]{1,19})\b"
    r"|\b(?:his|her|their)\s+name(?:'s|\s+is)\s+(?P<name2>[a-z][a-z'\-]{1,19})\b", re.I)
NOT_A_NAME_AFTER_CALLED = frozenset("""
in out off up down back away over round around about on at by for with without into onto
sick ill late busy tired poorly bad good home here there now soon again today tonight
tomorrow yesterday it them him her me us you one ones the a an
""".split())


def _the_name_they_gave_to_the_person_they_mean(text, memory):
    low = " ".join(str(text or "").lower().split())
    if not low or len(low.split()) > NAME_GIVEN_WORDS or "?" in low:
        return None
    match = NAME_GIVEN.search(low)
    if not match:
        return None
    raw = str(match.group("name") or match.group("name2") or "")
    name = raw.strip(" .,!")
    if not name or not extract._may_be_a_name(name) or name.lower() in NOT_A_NAME_AFTER_CALLED:
        return None
    if low[match.end():].strip(" .,!;:"):
        return None
    who = _person_from_pronoun(low, memory)
    if not who:
        return None
    for known in others(memory):
        if known.get("who") != who or not known.get("name"):
            continue
        if str(known.get("name")).lower() == name:
            return None
        known["name"] = extract._tidy(name)
        known.pop("turns", None)
        log(memory).append({"key": "other", "value": dict(known),
                            "turn": len(memory.get("turns") or []), "text": text})
        return known
    if extract.PETS.search(low):
        return None
    if re.search(r"\b(?:she|her)\b", low):
        fits = extract.SHE
    elif re.search(r"\b(?:he|his)\b", low):
        fits = extract.HE
    else:
        fits = None
    unnamed = [str(one.get("who")) for one in others(memory)
               if one.get("who") and not one.get("name")]
    kept = {str(one.get("who") or "") for one in others(memory)}
    unnamed += [str(word).lower() for word in (user(memory).get("people") or ())
                if isinstance(word, str) and str(word).lower() not in kept]
    unnamed = [word for word in dict.fromkeys(unnamed) if not fits or _pronoun_fits(word, fits)]
    if len(unnamed) != 1:
        return None
    for known in others(memory):
        if str(known.get("who") or "") == unnamed[0] and not known.get("name"):
            known["name"] = extract._tidy(name)
            known.pop("turns", None)
            log(memory).append({"key": "other", "value": dict(known),
                                "turn": len(memory.get("turns") or []), "text": text})
            return known
    remember_other(memory, {"who": unnamed[0], "name": extract._tidy(name)}, text)
    return {"who": unnamed[0], "name": extract._tidy(name)}










































NUMBER = re.compile(r"[£$€]?\d+(?:[.,]\d+)?(?:\s?(?:pounds|quid|euros?|dollars?|k))?(?![a-z])")









































































def _a_person(value):
    words = {word.rstrip("s") for word in re.findall(r"[a-z']+", str(value or "").lower())}
    return any(relation.rstrip("s") in words for relation in extract.RELATIONS)


PAIR_WITHOUT_A_MARKER = (
    re.compile(r"^\W*(?:(?:ok|okay|oh|well|so|and|hmm)[,. ]+)*"
               r"(?:(?:it'?s|its|that'?s|thats)\s+)?"
               r"(?P<to>[a-z0-9][a-z0-9'-]{0,19})\s*,?\s+not\s+"
               r"(?P<wrong>[a-z0-9][a-z0-9'-]{0,19})[.!]?\s*$", re.I),
    re.compile(r"^\W*(?:(?:ok|okay|oh|well|so|and|hmm)[,. ]+)*"
               r"not\s+(?P<wrong>[a-z0-9][a-z0-9'-]{0,19})\s*[,\u2013\u2014;-]\s*"
               r"(?:(?:it'?s|its|that'?s)\s+)?(?P<to>[a-z0-9][a-z0-9'-]{0,19})[.!]?\s*$",
               re.I),
    re.compile(r"^\W*(?:(?:ok|okay|oh|well|so|and|hmm|sorry|actually|no|nope)[,. ]+)*"
               r"(?:i'?m|i am|im|it'?s|its|it is|that'?s|thats|we'?re|we are)\s+not\s+"
               r"(?P<wrong>[a-z0-9][a-z0-9'.\-]{0,19})"
               r"[\s,;.!-]*(?:but\s+)?"
               r"(?:i'?m|i am|im|it'?s|its|it is|that'?s|thats|we'?re|we are)\s+"
               r"(?P<to>[a-z0-9][a-z0-9'.\-]{0,19})[.!]?\s*$", re.I),
)
NOT_A_NEW_VALUE = frozenset("""a an the me you it that this these those my your his her our their
thanks thank sure fair right wrong now then today tomorrow yesterday fine bad good great sorry
please yes yeah no not ok okay yet even both all much many one two three too so there here what
why how who when where true false""".split())


def _a_correction_without_a_marker(text, memory):
    said = str(text or "")
    if len(said.split()) > 6:
        return None
    for shape in PAIR_WITHOUT_A_MARKER:
        found = shape.match(said)
        if not found:
            continue
        right, wrong = extract._tidy(found.group("to")), extract._tidy(found.group("wrong"))
        if not right or not wrong or right.lower() == wrong.lower():
            continue
        if right.lower() in NOT_A_NEW_VALUE or wrong.lower() in NOT_A_NEW_VALUE:
            continue
        if not _fact_naming(memory, wrong) and not _a_person_called(memory, wrong):
            continue
        return {"to": right, "from": wrong}
    return None




def _a_person_called(memory, name):
    low = " ".join(str(name or "").lower().split())
    if not low:
        return False
    for entry in others(memory):
        if not isinstance(entry, dict):
            continue
        if str(entry.get("name") or "").strip().lower() == low:
            return True
        if any(str(old).strip().lower() == low for old in (entry.get("was") or [])):
            return True
    return False















def _stated_value(memory, key):
    said = " ".join(str(last_user(memory) or "").lower().split())
    entries = memory.get("facts_log")
    if not said or not isinstance(entries, list):
        return None
    for entry in reversed(entries):
        if not isinstance(entry, dict):
            continue
        if " ".join(str(entry.get("text") or "").lower().split()) != said:
            return None
        if entry.get("key") == key:
            return entry.get("value")
    return None








TOO_AS_WELL = re.compile(
    r"^(?:(?:and|also|but|plus)\s+)?(?:my|our)\s+(?P<who>[a-z]+(?:[ -]in[ -]law)?)\s+"
    r"(?P<agree>is\s+as\s+well|is\s+too|as\s+well|also|too)$", re.I)




def _a_second_persons_limit(text, memory):
    low = " ".join(str(text or "").lower().split())
    match = TOO_AS_WELL.match(low)
    if not match:
        return None
    who = _canon_relation(extract.a_person_word(match.group("who")))
    if who not in extract._A_WORD_FOR_A_PERSON:
        return None
    theirs = _the_limit_the_last_line_gave(memory)
    if not theirs:
        return None
    giving = {"who": who}
    allergies = theirs.get("allergies")
    if isinstance(allergies, (list, tuple)):
        foods = [str(one) for one in allergies if str(one).strip()]
        if foods:
            giving["allergies"] = foods
    diet = theirs.get("diet")
    if isinstance(diet, str) and diet.strip():
        giving["diet"] = diet
    if len(giving) < 2:
        return None
    return giving

















































def _drop_value(memory, value, text=""):
    known = user(memory)
    low = " ".join(str(value or "").lower().split())
    if not low:
        return None
    for key in DROP_LISTS:
        held = known.get(key)
        if not isinstance(held, list):
            continue
        left = [v for v in held if isinstance(v, str) and not _names_this(v, low)]
        if len(left) == len(held):
            continue
        known[key] = left
        memory["correction"] = {"key": key, "value": str(value), "dropped": True,
                                "said": " ".join(str(text or "").lower().split())}
        return memory["correction"]
    return _drop_from_plan(memory, value, text)


def _plan_names(plan, low):
    words = re.findall(r"[a-z0-9']+", str(plan or "").lower())
    for word in words:
        if word == low or (low.endswith("s") and word == low[:-1]) \
                or (word.endswith("s") and low == word[:-1]):
            return True
    return False


def _drop_from_plan(memory, value, text=""):
    known = user(memory)
    low = " ".join(str(value or "").lower().split())
    if not low:
        return None
    if low in MONTHS or low in extract.DAYS:
        return None
    plans = known.get("plans")
    held = [plan for plan in (plans if isinstance(plans, list) else []) if isinstance(plan, str)]
    current = known.get("plan")
    if isinstance(current, str) and current not in held:
        held.append(current)
    left = [plan for plan in held if not _plan_names(plan, low)]
    if len(left) == len(held):
        return None
    if left:
        known["plans"] = left[-6:]
        known["plan"] = left[-1]
    else:
        known.pop("plans", None)
        known.pop("plan", None)
    city = known.get("city")
    home = isinstance(city, str) and _plan_names(city, low)
    places = known.get("places")
    if isinstance(places, list) and not home:
        left_places = [place for place in places
                       if not (isinstance(place, str) and _plan_names(place, low))]
        if len(left_places) != len(places):
            if left_places:
                known["places"] = left_places
            else:
                known.pop("places", None)
    known["plan_dropped"] = low
    memory["correction"] = {"key": "plan", "value": str(value), "dropped": True,
                            "said": " ".join(str(text or "").lower().split())}
    return memory["correction"]


def _names_this(held, low):
    held = " ".join(str(held).lower().split())
    if held == low:
        return True
    for a, b in ((held, low), (low, held)):
        if b.endswith("s") and a == b[:-1]:
            return True
    return False
























































def _budget_sign(text, budget):
    number = re.sub(r"[^\d.,]", "", str(budget or ""))
    if not number:
        return ""
    for match in re.finditer(r"([\u00a3$\u20ac])\s?([\d][\d,.]*)", str(text or "")):
        if re.sub(r"[^\d.,]", "", match.group(2)) == number:
            return match.group(1)
    return ""










































OTHER_NOUNS = frozenset("""friend mate partner baby child kid children kids cousin parent parents""".split())












def _a_feeling_about_their_own_news(text, memory):
    try:
        return _a_feeling_about_what_they_said(memory, _bare(_folded(text, memory))) is not None
    except Exception:
        return False


def takes_as_it_comes(text, memory=None):
    if not isinstance(memory, dict):
        return False
    return _repeat_ask(text, _folded(text, memory), memory)



def _the_ask_about_how_it_went(text, memory):
    try:
        return thread.went(text, memory) is not None
    except Exception:
        return False




def _a_count_from_the_date(text, memory):
    try:
        return bool(until_answer(text, memory))
    except Exception:
        return False
FIGURE_MONEY = ("money",)

FIGURE_ASK = re.compile(
    r"^\W*(?:(?:and|but|so|ok|okay|right|then|oh|well)\W+)*"
    r"how\s+(?P<asked>many|much|long|far)\b(?P<rest>.*)$", re.I)
FIGURE_FILLER = frozenset("""a an the it its that this them those there here then now again
    roughly exactly approximately about around all told overall altogether total more less much
    many long do does did will would should can could you i we they he she reckon think suppose
    guess say again please for of in at on to be have has had is are was were and but so if
    when after before time times per each""".split())
FIGURE_AFTER = frozenset("""is are was were and or a an the in for of to on at by after before
    now then so but if when that from with without each every per of till until into about
    to around roughly or while than which where""".split())


def _the_unit_asked(line):
    found = FIGURE_ASK.match(" ".join(str(line or "").lower().split()))
    if not found:
        return None
    units = []
    for word in re.findall(r"[a-z']+", found.group("rest")):
        if word in FIGURE_FILLER:
            continue
        family = None
        for name, words in FIGURE_UNITS.items():
            if word in words:
                family = name
                break
        if family is None:
            return None
        if family not in units:
            units.append(family)
    per_week = re.match(
        r"^\W*(?:a|an|per|each)\s+(?:%s)\b" % "|".join(
            re.escape(word) for word in sorted(
                {word for family in FIGURE_TIME for word in FIGURE_UNITS[family]}, key=len,
                reverse=True)),
        found.group("rest") or "", re.I)
    if per_week and found.group("asked").lower() == "much" and set(units) <= set(FIGURE_TIME):
        return FIGURE_MONEY
    if not units and found.group("asked").lower() == "much":
        return FIGURE_MONEY
    if not units and found.group("asked").lower() == "many":
        return None
    return tuple(units) or FIGURE_TIME


ACTION_DURATION = re.compile(
    r"\bat a time\b|\bfor the first\b|\bfor the next\b|\bin a row\b|\beach time\b"
    r"|\bthe (?:first|next|last|coming|following|remaining|final)\b"
    r"|\b(?:once|twice|three times|a few times) a day\b|\ba day or two\b|\bper session\b",
    re.I)


ACTION_AMOUNT = re.compile(
    r"\b(?:whenever|when|if|once|each time|any time|every time|in case|unless)\b", re.I)


def _the_clause(said, start, end):
    left = max(said.rfind(mark, 0, start) for mark in ".;:")
    rights = [at for at in (said.find(mark, end) for mark in ".;:") if at >= 0]
    return said[left + 1:min(rights) if rights else len(said)]


A_MONEY_FIGURE = re.compile(
    r"(?:£|\$|€)\s*\d[\d,]*(?:\.\d+)?(?:\s*(?:to|-|or)\s*(?:£|\$|€)?\s*\d[\d,]*(?:\.\d+)?)?"
    r"|(?<![\d.,])\d[\d,]*(?:\.\d+)?(?:\s*(?:to|-|or)\s*\d[\d,]*(?:\.\d+)?)?\s*"
    r"(?:pounds?|quid|dollars?|euros?|pence)\b", re.I)


A_PERCENT_FIGURE = re.compile(
    r"(?<![\d.,])\d[\d,]*(?:\.\d+)?(?:\s*(?:to|-|or)\s*\d[\d,]*(?:\.\d+)?)?\s*"
    r"(?:per\s?cent|percent|%)", re.I)


def _the_money_figures(said):
    out = []
    for found in A_MONEY_FIGURE.finditer(said):
        if ACTION_AMOUNT.search(_the_clause(said, found.start(), found.end())):
            continue
        out.append((found.group(0).strip().rstrip(",;:"), True))
    if out:
        return out
    for found in A_PERCENT_FIGURE.finditer(said):
        if ACTION_AMOUNT.search(_the_clause(said, found.start(), found.end())):
            continue
        out.append((found.group(0).strip().rstrip(",;:"), True))
    return out


def _the_figures_in(said, units):
    if "money" in units:
        return _the_money_figures(said)
    words = sorted({word for unit in units for word in FIGURE_UNITS[unit]}, key=len, reverse=True)
    unit = r"(?-i:%s)" % "|".join(re.escape(word) for word in words)
    pattern = re.compile(
        r"(?<![\d,])\b(?P<qual>%s\s+)?(?P<num>%s)(?:\s*(?:-|to|or)\s*(?P<more>%s))?\s*"
        r"(?P<unit>%s)\b(?P<extra>\s+\d{1,3})?(?P<after>[^.;:!?,]*)" % (
            FIGURE_QUALIFIER, FIGURE_NUMBER, FIGURE_NUMBER, unit), re.I)
    out = []
    for found in pattern.finditer(said):
        after = found.group("after").strip().lower()
        next_word = (re.findall(r"[a-z']+", after) or [""])[0]
        unit_word = found.group("unit").lower()
        one = not unit_word.endswith("s") and unit_word not in ("km", "kg", "lb", "lbs")
        if one and next_word and next_word not in FIGURE_AFTER \
                and next_word not in {word for family in units for word in FIGURE_UNITS[family]}:
            continue
        pieces = [found.group("qual") or "", found.group("num"),
                  (("to " + found.group("more")) if found.group("more") else ""),
                  found.group("unit"), found.group("extra") or ""]
        said_figure = " ".join(piece.strip() for piece in pieces if piece.strip())
        if re.match(r"(?:a|an|per)\s+", after) or next_word == "per":
            continue
        if ACTION_DURATION.search(_the_clause(said, found.start(), found.end())):
            continue
        definite = found.group("num").lower() not in ("a", "an")
        if not definite:
            continue
        out.append((said_figure, definite))
    return out


def _the_figure_the_answer_names(text, memory):
    if not isinstance(memory, dict) or not isinstance(text, str):
        return None
    units = _the_unit_asked(text)
    if not units:
        return None
    theirs = repeat_the_line.the_figure_they_gave(text, memory)
    if theirs:
        return theirs
    rate_ask = bool(A_RATE_ASK.match(" ".join(text.lower().split())))
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    for back, turn in enumerate(reversed(turns[-LOOK_BACK_FIGURE:]), 1):
        if turn.get("module") not in ANSWER_MODULES:
            continue
        said = " ".join(str(turn.get("bot") or "").split())
        if not said or len(said) < FIGURE_ANSWER_LEN or said.rstrip().endswith("?"):
            continue
        if rate_ask and A_RATE_STATED.search(said):
            continue
        if LISTED_FIGURE.search(said):
            continue
        found = _the_figures_in(said, units)
        if not found:
            if _a_figure_of_those_units(said, units):
                return None
            continue
        stated = {(figure.lower()) for figure, _ in found}
        if len(stated) > 1:
            return None
        figure = found[0][0]
        return figure[:1].upper() + figure[1:] + "."
    return None


def _a_figure_of_those_units(said, units):
    if "money" in units:
        return bool(A_MONEY_FIGURE.search(said) or A_PERCENT_FIGURE.search(said))
    words = sorted({word for unit in units for word in FIGURE_UNITS[unit]}, key=len, reverse=True)
    if not words:
        return False
    unit = r"(?-i:%s)" % "|".join(re.escape(word) for word in words)
    pattern = re.compile(
        r"(?<![\d,])(?:%s|%s)\s*(?:-|to|or)?\s*%s\b" % (FIGURE_NUMBER, r"\d[\d,.]*", unit),
        re.I)
    return bool(pattern.search(said))


LISTED_FIGURE = re.compile(r"(?:,|;)\s*\d+(?:\s*(?:to|-|or)\s*\d+)?\s+for\b", re.I)

A_RATE_ASK = re.compile(
    r"how\s+much\b[^.?!]*\b(?:a|per|each|every)\s+(?:day|week|month|year)\b", re.I)
A_RATE_STATED = re.compile(
    r"(?:£|\bgbp\s*)?\d[\d,.]*\s*(?:pounds?\s+)?(?:a|per|each|every)\s+"
    r"(?:day|week|month|year)\b", re.I)



def _the_time_they_put_right(memory):
    fixed = memory.get("fixed_time")
    if not isinstance(fixed, dict):
        return None
    if int(fixed.get("turn") or -1) != len(memory.get("turns") or []):
        return None
    at = " ".join(str(fixed.get("at") or "").split())
    if not at:
        return None
    what = " ".join(str(fixed.get("what") or "").split())
    said_back = (ROUTINE_SAY_BACK.get(what) or "You {what} at {at}.").format(at=at, what=what)
    said_back = said_back.rstrip(" .")
    was = " ".join(str(fixed.get("from") or "").split())
    if was and was != at:
        said_back += ", not " + was
    return "Got it - " + said_back[0].lower() + said_back[1:] + "."


def respond(text, memory):
    from ..memory import again as same_again
    from ..memory import not_this
    from ..memory import trips
    text = _without_the_shrug_at_the_end(text)
    put_right = _the_time_they_put_right(memory)
    if put_right:
        return put_right
    pointed_at_nothing = _points_back_at_nothing(text, memory)
    if pointed_at_nothing:
        return pointed_at_nothing
    recall_frame = _a_recall_frame_about_nothing(text, memory)
    if recall_frame:
        return recall_frame
    ask_about_nothing = _an_ask_about_nothing(text, memory)
    if ask_about_nothing:
        return ask_about_nothing
    from ..memory import goals as _goals_progress
    going = _goals_progress.a_progress_asked(text, memory)
    if going:
        return going
    recall_about_nothing = _a_recall_about_nothing(text, memory)
    if recall_about_nothing:
        return recall_about_nothing
    behind = _the_ask_behind_the_recall(text)
    if behind:
        direct, attribute, possessive = behind
        answer = respond(direct, memory)
        if answer:
            return answer
        if _a_word_for_the_slot(memory, attribute):
            behind = None
        else:
            theirs = "your" if possessive in ("my", "our") else possessive
            return pick(["You haven't told me " + theirs + " " + attribute + ".",
                         "I don't have " + theirs + " " + attribute + " from you yet.",
                         "You haven't mentioned " + theirs + " " + attribute + " to me."], memory)
    ages_of_the_children = _the_ages_of_the_children(text, memory)
    if ages_of_the_children:
        return ages_of_the_children
    ruled_out = not_this.reply_for(text, memory)
    if ruled_out:
        return ruled_out
    told_about_the_trip = trips.reply_for(text, memory)
    if told_about_the_trip:
        return told_about_the_trip
    if repeat_the_line.A_BARE_DURATION_ASK.search(" ".join(str(text or "").lower().split())):
        theirs = repeat_the_line.the_figure_they_gave(text, memory)
        if theirs:
            return theirs
    if repeat_the_line.A_PAY_WORD.search(" ".join(str(text or "").lower().split())):
        theirs = repeat_the_line.the_figure_they_gave(text, memory)
        if theirs:
            return theirs
    if repeat_the_line.how_long_its_been(text):
        theirs = repeat_the_line.the_figure_they_gave(text, memory)
        if theirs:
            return theirs
    figure = _the_figure_the_answer_names(text, memory)
    if figure:
        return figure
    along = _how_far_along(memory, _bare(_folded(text, memory)))
    if along:
        return along
    theirs = repeat_the_line.asked_back(text, memory)
    if theirs:
        return theirs
    reply = _the_store_reply(text, memory)
    if not isinstance(reply, str) or not isinstance(memory, dict):
        return reply
    reply = _the_places_are_written_as_names(reply, memory)
    if not WHOLE_ASK.match(str(text or "").strip().lower()) \
            and not _asks_to_hear_it_again(text, memory):
        framed = same_again.instead(reply, text, memory)
        if framed:
            return framed
    return reply


def _asks_to_hear_it_again(text, memory):
    try:
        return _repeat_ask(text, _folded(text, memory))
    except Exception:
        return False





















































def _asks_about_someone_else(text):
    line = " ".join(str(text or "").split())
    return bool(YES_NO_ASK.match(line))






















































SAID_AGAIN = re.compile(r"\bi\s+(?:mean|meant)(?:\s+to\s+say)?\b", re.I)
SORRY_OPENS_A_CORRECTION = re.compile(r"\b(?:sorry|soz)\b", re.I)


def _note_a_corrected_fact(memory, text, entry, was):
    if not isinstance(was, dict) or not isinstance(entry, dict):
        return
    said = " ".join(str(text or "").lower().split())
    if not (SAID_AGAIN.search(said) or SORRY_OPENS_A_CORRECTION.search(said)):
        return
    for kind, value in entry.items():
        if kind in ("who", "pronoun", "turns") or value in ("", None):
            continue
        before = was.get(kind)
        if before in ("", None) or before == value:
            continue
        memory["fact_fixed"] = {"who": str(entry.get("who") or ""), "kind": kind,
                                "value": value, "was": before,
                                "said": " ".join(str(text or "").lower().split())}
        return


def _note_a_fact_moved(memory, text, entry, was):
    if not isinstance(entry, dict):
        return
    said = " ".join(str(text or "").lower().split())
    if not (SAID_AGAIN.search(said) or SORRY_OPENS_A_CORRECTION.search(said)):
        return
    who = str(entry.get("who") or "").strip()
    if not who:
        return
    if not re.search(r"\b" + re.escape(who) + r"\b", said):
        return
    for kind, value in entry.items():
        if kind in ("who", "pronoun", "turns") or value in ("", None):
            continue
        if isinstance(value, (list, dict)):
            continue
        if isinstance(was, dict) and was.get(kind) not in ("", None) and was.get(kind) != value:
            continue
        hold = [one for one in others(memory)
                if isinstance(one, dict) and one.get("who") and one.get("who") != who
                and one.get(kind) == value]
        if not hold:
            continue
        other = hold[0]
        memory["fact_moved"] = {"who": who, "was_who": str(other.get("who")), "kind": kind,
                                "value": value, "said": said}
        memory["moved_to_who"] = said
        other.pop(kind, None)
        return






RECALL_WRAPPER = re.compile(
    r"^\s*(?:and\s+|so\s+|but\s+|also\s+|again\s+)?"
    r"(?P<word>what|when|how\s+old)\s+(?:did|do)\s+(?:i|we)\s+"
    r"(?:say|call|tell\s+(?:you|u)|told\s+(?:you|u)|mention)\s+(?P<rest>.+?)\s*\??\s*$", re.I)
RECALL_SLOTS = (
    (re.compile(r"\b(?:names?|called)\b", re.I), "what", "name"),
    (re.compile(r"\b(?:birthday|bday|dob|date\s+of\s+birth)\b", re.I), "when", "birthday"),
    (re.compile(r"\b(?:ages?)\b", re.I), "how old", "age"),
    (re.compile(r"\b(?:budget|salary|wage|rent|target|savings?)\b", re.I), "what", None),
    (re.compile(r"\b(?:address|postcode|number|time|date)\b", re.I), "what", None),
)
RECALL_POSSESSIVE = re.compile(r"^\s*(?P<poss>my|our|his|her|their)\b", re.I)
RECALL_SLOTS_BY_POSSESSIVE = re.compile(
    r"^\s*(?:my|our|his|her|their)\s+(?P<attribute>names?|birthday|bday|dob|ages?|"
    r"budget|salary|wage|societys?|address|postcode)\??\s*$", re.I)
SHE_OR_HE = {"his": ("he", "is"), "her": ("she", "is"), "their": ("they", "are"),
             "my": ("i", "am"), "our": ("we", "are")}


SLOT_WORDS = {
    "age": re.compile(r"\b\d|\b(?:age|aged|old)\b", re.I),
    "name": re.compile(r"\b(?:name|called|named|calls)\b", re.I),
    "birthday": re.compile(r"\b(?:birthday|bday|dob|january|february|march|april|may|june|july|"
                           r"august|september|october|november|december)\b", re.I),
}


def _a_word_for_the_slot(memory, attribute):
    pattern = SLOT_WORDS.get(str(attribute or "").lower())
    if not pattern:
        return False
    return any(pattern.search(str(turn.get("user") or "")) for turn in recent(memory, 8))


def _the_ask_behind_the_recall(low):
    if not isinstance(low, str):
        return None
    wrapped = RECALL_WRAPPER.match(low)
    if not wrapped:
        return None
    rest = re.sub(r"\s+(?:was|is|were|are)\s*$", "", wrapped.group("rest").strip())
    said = wrapped.group("word").lower().replace("  ", " ")
    slot = next(((word, name) for pattern, word, name in RECALL_SLOTS
                 if pattern.search(rest)), None)
    if not slot:
        return None
    word, attribute = slot
    possessive = RECALL_POSSESSIVE.match(rest)
    if said.startswith("how old"):
        person = rest.strip().lower()
        if person not in SHE_OR_HE:
            return None
        who, verb = SHE_OR_HE[person]
        return "how old " + verb + (" i" if who == "i" else " " + who), "age", person
    if not possessive:
        return None
    person = possessive.group("poss").lower()
    plain = " ".join(re.sub(r"\b(?:was|is|were|are)\b", " ", rest).split())
    if not plain:
        return None
    word = "when is " if attribute == "birthday" else "what is "
    slot_word = RECALL_SLOTS_BY_POSSESSIVE.match(plain)
    only_slot = slot_word.group("attribute") if slot_word else None
    return word + plain, only_slot or (attribute or "answer"), person













def TAKES_AS_IT_COMES(text, memory=None):
    if not isinstance(text, str) or not isinstance(memory, dict):
        return False
    if memory.get("moved_to_who") == " ".join(text.lower().split()):
        return True
    if _the_store_readings(text, memory):
        return True
    if told_about.A_CALLBACK(text, memory):
        return True
    if _the_ask_about_how_it_went(text, memory):
        return True
    if _a_callback_that_names_its_thing(text, memory):
        return True
    if reminded.about_a_thing_they_said(text, memory):
        return True
    if not BARE_WHAT_I_DO.match(_bare(_folded(text, memory) or text)):
        return False
    return bool(user(memory).get("job")) and _the_job_was_just_said(memory)









































WORK_ON_IT = re.compile(r"\b[a-z]{3,}\s+it\b", re.I)






















































def _about_the_verb(plans, low, found):
    named = content(low[found.end():])
    if named:
        for plan in reversed(plans):
            if _says_the_verb(plan, found.group(1)) and any(
                    _names_the_thing(plan, word) for word in named):
                return plan
    for plan in reversed(plans):
        if _says_the_verb(plan, found.group(1)):
            return plan
    return None



































































def _remember_dislikes(text, memory, named_here=()):
    if not isinstance(text, str):
        return
    for food, at in guest.found(text):
        kind, who = extract.subject(text, at)
        if kind == "user":
            food = guest.plain(food)
            if food:
                remember(memory, "dislikes", [food], text)
            continue
        if kind != "other":
            continue
        who = who or _person_from_pronoun(text, memory, named_here)
        remember_other(memory, {"who": who, "dislikes": [food]}, text)



































def _diet_reply(memory, low=""):
    said = a_change.reported(low, "diet")
    if said:
        was = user(memory).get("diet")
        if said == "changed" and was:
            forget(memory, "diet", [was])
            user(memory)["diet_changed"] = was
        return a_change.reply(said, "diet", was=was)
    diet = user(memory).get("diet")
    if not diet:
        if str(low or "") and not DIET_FACT_ASK.search(str(low or "")) \
                and _food_facts(memory):
            left_out, said_so = _what_a_dinner_has_to_leave_out(memory)
            if left_out:
                return ("Nothing with " + _say_a_list(left_out) + " in it — " +
                        " and ".join(said_so) + ". Tell me what is in the fridge and I'll pick "
                        "a dinner around it.")
        kept = _food_facts(memory)
        if kept:
            return "You told me you're " + _say_a_list(kept) + "."
        if DIET_FACT_ASK.search(str(low or "")):
            kept = _food_facts(memory)
            if kept:
                return "You told me you're " + _say_a_list(kept) + "."
        who, theirs = _other_fact(memory, "diet")
        if theirs and who:
            return ("You haven't told me about yours \u2014 the diet you mentioned is your "
                    + who + "'s.")
        changed_from = user(memory).get("diet_changed")
        if changed_from and DIET_FACT_ASK.search(str(low or "")):
            was = str(changed_from).strip()
            was = ("not eating " + was[3:] if was.lower().startswith("no ")
                   else "being " + _diet_words(was))
            return "You told me your diet had changed from " + was + ". What is it now?"
        take_back, gone = _the_take_back(memory, "diet")
        if gone:
            return _a_take_back_said_back(take_back, gone)
        if MEAL_WANTED.search(str(low or "")) and not DIET_FACT_ASK.search(str(low or "")):
            return None
        return _deny(memory, "diet", "You haven't told me about your diet.",
                     own=_their_own_diet)
    diet = str(diet)
    if MEAL_WANTED.search(str(low or "")) and not DIET_FACT_ASK.search(str(low or "")):
        left_out, said_so = _what_a_dinner_has_to_leave_out(memory)
        if left_out:
            return ("Nothing with " + _say_a_list(left_out) + " in it \u2014 " +
                    " and ".join(said_so) + ". Tell me what is in the fridge and I'll pick a "
                    "dinner around it.")
        return None
    if diet.startswith("no "):
        return "You told me you don't " + _diet_how(diet) + " " + diet[3:] + "."
    if diet in WAY_OF_EATING:
        return "You told me you're " + _diet_words(diet) + "."
    if diet in PLAN_DIETS:
        return "You told me you're doing " + _diet_words(diet) + "."
    return "You told me you're " + diet + "."




























































































































































































































































































FACT_WORDS = frozenset((
    "name", "called", "age", "old", "job", "work", "works", "working", "city", "town", "live",
    "lives", "living", "moved", "moving", "from", "diet", "dieting", "eating", "food", "budget",
    "money", "afford", "allergy", "allergies", "allergic", "pet", "pets", "dog", "cat", "height",
    "tall"))


def _a_fact_word(low):
    after = re.search(r"\babout\b\s+(.+)$", low or "")
    words = set(re.findall(r"[a-z]+", (after.group(1) if after else "").lower()))
    return bool(words & FACT_WORDS)


def _a_callback_that_names_its_thing(text, memory):
    if not isinstance(text, str) or not isinstance(memory, dict):
        return False
    try:
        low = " ".join(text.lower().split())
        return bool(_names_its_thing(low) and _about_this_chat(text, memory))
    except Exception:
        return False














for _concept, _words in (
        ("mother", "mum mom mummy ma mam mother mumma"),
        ("father", "dad daddy pa papa father"),
        ("parent", "parent parents folks"),
        ("child", "kid kids child children baby toddler"),
        ("dog", "dog puppy pup dogs"),
        ("cat", "cat kitten kitty cats"),
        ("pet", "pet pets"),
        ("car", "car vehicle motor"),
        ("home", "home house flat apartment place"),
        ("party", "party birthday bday celebration bash"),
        ("job", "job work career"),
        ("food", "food dinner tea meal supper"),
        ("money", "money budget cash savings"),
        ("diet", "diet vegetarian vegan pescatarian"),
        ("doctor", "doctor gp surgery hospital"),
        ("wedding", "wedding weddings married marry marriage engaged engagement bride groom "
                    "fiance fiancee honeymoon"),
        ("holiday", "holiday holidays vacation trip trips break abroad travelling travel"),
        ("exam", "exam exams revision revise revising coursework dissertation thesis mock"),
        ("gym", "gym gyms fitter fitness exercise exercising workout workouts jogging running"),
        ("smoking", "smoking smoke smoker cigarettes cigarette fags vaping vape nicotine")):
    for _word in _words.split():
        CONCEPTS[_word] = _concept

for _country in extract.COUNTRIES:
    CONCEPTS.setdefault(_country.lower(), "holiday")





































































def _points_back_at_nothing(text, memory):
    if not thread.points_back(text) or not thread.nothing_said(memory):
        return None
    return _vary(POINTS_BACK_NOTHING, memory)


def _a_recall_about_nothing(text, memory):
    if not thread.asks_what_i_said(text) or not thread.nothing_said(memory):
        return None
    return _vary(WHAT_I_SAID_NOTHING, memory)


A_RECALL_IN_ANOTHER_SHAPE = re.compile(
    r"^(?:and|so|but|also|again|ok|okay|well)?\s*(?:"
    r"tell\s+me\s+what\s+(?:i|we)\s+(?:said|say|told\s+(?:you|u)|tell\s+(?:you|u)|mentioned?)\b"
    r"|(?:did|do)\s+(?:i|we)\s+(?:say|tell\s+(?:you|u)|told\s+(?:you|u)|mentioned?)\s+"
    r"(?:anything|something|much)\b"
    r"|what\s+(?:was|were)\s+(?:the\s+thing|that\s+thing|that)\s+(?:that\s+)?"
    r"(?:i|we)\s+(?:said|told\s+(?:you|u)|mentioned?)\b"
    r"|remind\s+me\s+what\s+(?:that|it|this|those|they)\s+(?:was|were|is|are)\b"
    r")", re.I)
RECALL_NAMES_NOTHING = frozenset("""it that this them those these one ones there anything something
much thing things about of on in at to for from with the a an was were is are be been being
i we you u he she they me us my our his her their said say told tell mention mentioned mentioning
and or so but also again then just really actually exactly then""".split())


def _names_nothing_in_a_recall(rest):
    words = re.findall(r"[a-z]+", str(rest or "").lower().replace("'", ""))
    return not [word for word in words if word not in RECALL_NAMES_NOTHING]


def _a_recall_frame_about_nothing(text, memory):
    if not thread.nothing_said(memory):
        return None
    low = " ".join(str(text or "").lower().replace("'", "").split()).strip(" .!?,")
    wrapped_low = " ".join(str(text or "").lower().split()).strip(" .!?,")
    another = A_RECALL_IN_ANOTHER_SHAPE.match(wrapped_low)
    if another and _names_nothing_in_a_recall(wrapped_low[another.end():]):
        return _vary(WHAT_I_SAID_NOTHING, memory)
    wrapped = RECALL_WRAPPER.match(wrapped_low)
    if not wrapped:
        return None
    rest = wrapped.group("rest")
    if not thread.POINTING_WORD.search(rest) or len(re.findall(r"[a-z]+", rest)) > 2:
        return None
    return _vary(WHAT_I_SAID_NOTHING, memory)


def _an_ask_about_nothing(text, memory):
    if not thread.points_at_a_word_alone(text) or not thread.nothing_said(memory):
        return None
    from ..compose import fallback
    if fallback._points_at_nothing(text, memory):
        return None
    return _vary(POINTING_WORD_NOTHING, memory)


def _the_last_ask_about_the_bot(memory):
    for text, reading in reversed(list(thread.user_lines(memory))):
        if not (isinstance(reading, dict) and reading.get("about_bot")):
            return None
        asked = thread.restate(text)
        if asked:
            return asked
    return None












































































































def _fits(answer, room):
    best, best_seconds = None, -1
    names = _names_minutes(answer)
    for sentence in _sentences(answer):
        for part in _halves(sentence):
            took = _longest(part, bare=names)
            if took is None or took > room or not _says_something(part):
                continue
            if took > best_seconds:
                best, best_seconds = part, took
    return best


























































def _asks_whether_we_followed(text, memory):
    if not isinstance(text, str):
        return False
    low = _plain_line(_folded(text, memory) if isinstance(memory, dict) else text)
    if not low:
        return False
    if low.endswith("?") :
        low = low[:-1].strip()
    if _reads_as_the_invitation(low, memory):
        return False
    return bool(CHECK_FOLLOWED.match(low))
























def _the_group_size_ask(text, memory):
    low = str(text or "").lower()
    if not (how_many.GROUP_ASK.search(low) or how_many.BARE_COUNT_ASK.search(low)):
        return False
    return bool(how_many.answer(text, memory))







