
import re

from . import findout, for_the_day, waited_for
from .fallback_data import (
    MISSED_STEP_LINES, REPAIR_WHETHER_LINES, the_bots_own_answer,
    the_place_the_answer_is_kept,
)
from .the_rule_for_it import A_CARE_WORD, A_MONEY_WORD, TIME_RULE, the_rule_for_it
from .fallback import (
    method_ask_pool,
    ANIMALS, ASKED_IF_I_SAW_LINES, A_PERSON_IN_A_CRISIS, A_STEP_ASK, BARE_FOLLOW_UP,
    BARE_FOLLOW_UP_CARE_REPLIES, BARE_FOLLOW_UP_REPLIES, BARE_PICK_AFTER_NEWS,
    BODY_IS_NOT_A_MACHINE, BODY_PARTS, CARE_HERE, CARE_MODULES, CRISIS_ASK,
    DITHER_OPEN_LINES,
    EXPERT_WORDS, HANDED_BACK, HEALTH_WORDS, HELP_ALREADY, HOW_TO_DECIDE,
    HOW_TO_DECIDE_LINES, LEAVING_IN_THE_LINE, LIFE_DIRECTION, NEUTRAL, NOT_A_TIPS_ASK,
    NOT_NOTED, POINTING_LINES, REALISTIC, REALISTIC_ABOUT_ME, REPAIR_BARE_IT,
    who_settles,
    REPAIR_DECISION, REPAIR_PERSON,
    REPAIR_RULE, REPAIR_TARIFF, REPAIR_TRADE, REPAIR_WHAT_IT_IS_WORTH, REPAIR_WHETHER,
    SAME_AGAIN, SAME_AGAIN_WITH_THE_ANSWER, SYMPTOM_WORDS, TAG_CAN,
    TAG_CONFIRM, TAG_UNSURE, TIPS_ASKS, TIPS_LINES, TOO_LATE, UNKNOWN,
    UNKNOWN_ABOUT_A_PET, UNKNOWN_ABOUT_SOMEONE, UNKNOWN_DECIDE, UNKNOWN_HEALTH,
    UNKNOWN_REALISTIC, UNKNOWN_REALISTIC_CARE, UNKNOWN_TOO_LATE, UNKNOWN_WORD,
    UNKNOWN_WORD_NAMED,
    UNKNOWN_WORRY, VIEW_AFTER_A_DEATH, VIEW_ASK_LINES, VIEW_COMPANY, VIEW_DECIDE,
    VIEW_HANDBACK, VIEW_LINES, VIEW_MIRROR, VIEW_MIRROR_LINES, VIEW_NAMES_SOMEBODY,
    VIEW_NO_SUBJECT, VIEW_ON_GOOD_NEWS, WASNT_THERE, WHO_FOR_IT, _a_bare_worry,
    _a_dead_end, _a_plan_doubt, _a_plan_in_the_thread, _a_price_wants_a_verdict,
    _a_care_home_line, _a_question_about_the_person, _a_repair_already_spoken_of,
    _a_subject_above, _a_switch_off_asked,
    _a_thing_they_started, _a_thing_was_named, _advisor, _after_a_colon,
    _answered_already, _answered_recently, _asked_about_the_day_they_had,
    _asks_a_name_back, _asks_for_a_person_to_talk_to, _bare_pick, _choose,
    _forecast_pool, _grief_thread, _hedged_recently, _in_a_care_thread,
    _in_a_crisis_thread, _in_a_loss_thread, _in_a_pool, _is_a_hedge, _is_a_tips_ask,
    _is_a_view_ask, _name_given_before, _names_its_own_thing, _news_above,
    _nothing_to_choose, _nothing_to_stand_behind, _only_a_reaction, _only_the_floor,
    _points_at_nothing, _reads, _reads_as_a_claim, _reads_as_taste,
    _says_it_already, _the_answer_above, _the_answer_in_reply, _the_line_before,
    _the_pool_for_a_worry_about_them, _the_thread_is_heavy, _the_view_of,
    _the_weird_ask_pool, _their_own_day, _thread_is_about_a_person,
    _thread_is_about_a_pet, _thread_is_about_someone_else,
    _offers_to_fix_themselves, _thread_is_about_the_body, _thread_names_a_machine, _tips,
    _who_for_the_thread, ack, asks_for_more,
    finding_out, in_a_safety_thread, no_eyes, reads_as_if_i_saw, the_lost_ask_reply,
    unknown_pool,
)


def _the_repeat_answer(memory):
    answer = " ".join(str(_the_answer_above(memory) or "").split())
    if not answer:
        return ""
    sentences = re.split(r"(?<=[.!?])\s+", answer)
    return " ".join(sentences[:2]) if len(sentences) > 2 else answer


def _drafting_pool(clean):
    if no_eyes.names_the_addressee(clean):
        return UNKNOWN_WORD_NAMED
    return UNKNOWN_WORD


def _a_care_thread(memory, look_back=3):
    if _thread_is_about_a_pet(memory):
        return True
    turns = [t for t in ((memory or {}).get("turns") or []) if isinstance(t, dict)]
    for turn in turns[-look_back:]:
        if A_CARE_WORD.search(str(turn.get("user") or "").lower()):
            return True
    return False


def _a_money_thread(memory, look_back=3):
    turns = [t for t in ((memory or {}).get("turns") or []) if isinstance(t, dict)]
    for turn in turns[-look_back:]:
        if A_MONEY_WORD.search(str(turn.get("user") or "").lower()):
            return True
    return False


def _the_rule_for_it_for_the_turn(clean, repaired, memory):
    if (in_a_safety_thread(memory) or _grief_thread(memory) or _in_a_loss_thread(memory)
            or _in_a_care_thread(memory) or _thread_is_about_the_body(memory)
            or _a_care_thread(memory)):
        return None
    words = (set(re.findall(r"[a-z']+", str(clean or "").lower()))
             | set(re.findall(r"[a-z']+", str(repaired or "").lower())))
    if words & (BODY_PARTS | SYMPTOM_WORDS | HEALTH_WORDS):
        return None
    pool = the_rule_for_it(clean, repaired)
    if pool is TIME_RULE and _a_money_thread(memory):
        return None
    return pool

MISSED_STEP = re.compile(
    r"\bwhat (?:if|happens if) (?:i|we|you) (?:miss|skip|dont do|cant do|cannot do)\b"
    r"|\bwhat (?:if|happens if) (?:i|we) (?:have to )?(?:miss|skip)\b")
MISSED_STEP_PLAN = re.compile(
    r"\b(?:a|an|one|two|three|four|\d+|a couple of|a few|couple of|few)?\s*"
    r"(?:days?|weeks?|fortnight|months?|sessions?|runs?|rides?|swims?|classes?|lessons?|"
    r"workouts?|practice|training)\b")
MISSED_STEP_KEEPS = re.compile(
    r"\b(?:pills?|doses?|drops|tablets?|meds|medication|medications|prescriptions?|insulin|"
    r"inhalers?|injections?|jabs?|appointments?|periods?|contracepti\w*|antidepressants?|"
    r"antibiotics?|lenses?|dressing|dressings)\b")


def _a_missed_step(clean, repaired, memory, words):
    if not MISSED_STEP.search(clean):
        if repaired == clean or not MISSED_STEP.search(repaired):
            return None
    plan = MISSED_STEP_PLAN.search(clean) or MISSED_STEP_PLAN.search(repaired)
    if plan is None:
        return None
    if MISSED_STEP_KEEPS.search(clean) or MISSED_STEP_KEEPS.search(repaired):
        return None
    if set(words) & HEALTH_WORDS or set(words) & BODY_PARTS:
        return None
    if (in_a_safety_thread(memory) or _grief_thread(memory) or _in_a_loss_thread(memory)
            or _thread_is_about_the_body(memory) or _thread_is_about_a_pet(memory)
            or _thread_is_about_someone_else(memory)):
        return None
    return MISSED_STEP_LINES


def _unknown(understood, memory, clean):
    repaired = understood.get("plain") or clean
    own_day = _their_own_day(clean)
    if own_day:
        return _choose(own_day, memory, clean)
    body_lines = no_eyes.look_at_a_body_lines(clean, repaired, memory)
    if body_lines:
        return _choose(body_lines, memory, clean)
    cannot_see = no_eyes.cannot_see_your_thing(clean)
    if cannot_see:
        return _choose(cannot_see, memory, clean)
    described = no_eyes.what_they_described(clean, memory)
    if described:
        return _choose(described, memory, clean)
    in_the_room = no_eyes.a_thing_in_the_room(clean)
    if in_the_room:
        return _choose(in_the_room, memory, clean)
    if no_eyes.writes_the_message(clean):
        return _choose(_drafting_pool(clean), memory, clean)
    if _in_a_crisis_thread(memory) and (_asks_for_a_person_to_talk_to(clean)
                                        or CRISIS_ASK.search(clean)
                                        or WHO_FOR_IT.match(clean)):
        return _choose(A_PERSON_IN_A_CRISIS, memory, clean)
    lost = the_lost_ask_reply(memory, clean, repaired)
    if lost:
        return lost
    if _asks_a_name_back(clean, understood.get("words") or []):
        given = _name_given_before(clean, memory)
        if given:
            return _choose([line.format(name=given) for line in HANDED_BACK], memory, clean)
        return _choose(NOT_NOTED, memory, clean)
    forecast = _forecast_pool(clean, repaired, memory)
    if forecast:
        return _choose(forecast, memory, clean)
    if reads_as_if_i_saw(clean, memory):
        return _choose(ASKED_IF_I_SAW_LINES, memory, clean)
    if (_asked_about_the_day_they_had(clean) and not in_a_safety_thread(memory)
            and not _grief_thread(memory) and not _in_a_loss_thread(memory)):
        return _choose(WASNT_THERE, memory, clean)
    how_to = HOW_TO_DECIDE.search(clean)
    how_line = clean
    if how_to is None and repaired != clean:
        how_to = HOW_TO_DECIDE.search(repaired)
        how_line = repaired
    if (how_to is not None and not _reads(LIFE_DIRECTION.search, clean, repaired)
            and _nothing_to_choose(how_line[how_to.end():])):
        said_words = " " + re.sub(r"[^a-z0-9']", " ", how_line) + " "
        plain = said_words.replace("'", "").split()
        if not (set(plain) & HEALTH_WORDS or set(plain) & EXPERT_WORDS
                or set(plain) & BODY_PARTS
                or any(w in ANIMALS or w.rstrip("s") in ANIMALS for w in plain)):
            return _choose(HOW_TO_DECIDE_LINES, memory, clean)
    if _reads_as_taste(clean, understood.get("words") or []):
        return _choose(UNKNOWN, memory, clean)
    if (_reads(REPAIR_WHETHER.search, clean, repaired)
            and not _reads(REPAIR_WHAT_IT_IS_WORTH.search, clean, repaired)
            and not who_settles(clean, memory)
            and not _a_repair_already_spoken_of(memory)):
        return _choose(REPAIR_WHETHER_LINES, memory, clean)
    if (_reads(REPAIR_DECISION.search, clean, repaired)
            and not _reads(REPAIR_TRADE.search, clean, repaired)
            and not _reads(REPAIR_PERSON.search, clean, repaired)
            and not (_reads(LEAVING_IN_THE_LINE.search, clean, repaired)
                     and _thread_is_about_a_person(memory))
            and not _reads(REPAIR_TARIFF.search, clean, repaired)):
        if in_a_safety_thread(memory) or _grief_thread(memory) or _in_a_loss_thread(memory):
            return _choose(CARE_HERE, memory, clean)
        own_thing = _names_its_own_thing(clean) or _names_its_own_thing(repaired)
        line_words = (set(re.findall(r"[a-z']+", clean))
                      | set(re.findall(r"[a-z']+", repaired)))
        no_thing_named = (_reads(REPAIR_BARE_IT.search, clean, repaired)
                          and not _thread_names_a_machine(memory))
        if not own_thing and ((_thread_is_about_the_body(memory)
                               and not _thread_names_a_machine(memory))
                              or line_words & (BODY_PARTS | SYMPTOM_WORDS | HEALTH_WORDS)):
            if _offers_to_fix_themselves(clean):
                return _choose(BODY_IS_NOT_A_MACHINE, memory, clean)
            return _choose(UNKNOWN_HEALTH, memory, clean)
        if not no_thing_named and (not _thread_is_about_a_person(memory) or own_thing
                                   or _a_thing_was_named(memory)):
            return _choose(REPAIR_RULE, memory, clean)
        return _choose(UNKNOWN_DECIDE, memory, clean)
    if (_reads(TOO_LATE.search, clean, repaired) and _a_thing_they_started(memory)
            and not _hedged_recently(memory) and not _thread_is_about_the_body(memory)):
        return _choose(UNKNOWN_TOO_LATE, memory, clean)
    if (_a_plan_doubt(REALISTIC.search, clean, repaired)
            or (_a_plan_doubt(REALISTIC_ABOUT_ME.search, clean, repaired)
                and _a_plan_in_the_thread(clean, memory))) and not _hedged_recently(memory):
        pool = UNKNOWN_REALISTIC_CARE if _the_thread_is_heavy(memory) else UNKNOWN_REALISTIC
        return _choose(pool, memory, clean, clean + " " + _the_line_before(memory))
    said = " " + re.sub(r"[^a-z0-9']", " ", clean) + " "
    words = said.replace("'", "").split()
    waited = waited_for.for_the_ask(clean, repaired, memory)
    if waited is not None and waited is not waited_for.NOTHING_HELD and BARE_FOLLOW_UP.match(clean):
        return _choose(waited, memory, clean)
    if BARE_FOLLOW_UP.match(clean):
        pool = BARE_FOLLOW_UP_CARE_REPLIES if _the_thread_is_heavy(memory) else BARE_FOLLOW_UP_REPLIES
        return _choose(pool, memory, clean, clean + " " + _the_line_before(memory))
    switched = _a_switch_off_asked(memory, clean)
    if switched:
        return _choose(switched, memory, clean + " " + _the_line_before(memory))
    if _points_at_nothing(clean, memory, repaired):
        return _choose(POINTING_LINES, memory, clean)
    weird = _the_weird_ask_pool(clean, memory) if not _hedged_recently(memory) else None
    if weird is not None:
        return _choose(weird, memory, clean)
    pool = unknown_pool(clean, words)
    if pool is UNKNOWN and repaired != clean:
        said = " " + re.sub(r"[^a-z0-9']", " ", repaired) + " "
        words = said.replace("'", "").split()
        pool = unknown_pool(repaired, words)
    if pool is UNKNOWN or pool is UNKNOWN_DECIDE:
        missed = _a_missed_step(clean, repaired, memory, words)
        if missed is not None:
            return _choose(missed, memory, clean)
    if pool is UNKNOWN_WORRY and _a_bare_worry(clean) and _thread_is_about_the_body(memory):
        pool = UNKNOWN_HEALTH
    elif (pool is UNKNOWN_WORRY and _a_bare_worry(clean) and _thread_is_about_a_pet(memory)):
        pool = UNKNOWN_ABOUT_A_PET
    elif (pool is UNKNOWN_WORRY and _a_bare_worry(clean)
            and _thread_is_about_someone_else(memory)):
        pool = UNKNOWN_ABOUT_SOMEONE
    if pool is UNKNOWN or pool is UNKNOWN_DECIDE:
        if waited and (pool is UNKNOWN or waited is not waited_for.NOTHING_HELD):
            return _choose(waited, memory, clean)
    if (pool is UNKNOWN or pool is UNKNOWN_WORRY) and not _hedged_recently(memory):
        worry = _the_pool_for_a_worry_about_them(clean, memory)
        if worry:
            return _choose(worry, memory, clean)
    if pool is UNKNOWN_WORD:
        return _choose(_drafting_pool(clean), memory, clean)
    if asks_for_more(said, memory) and not _hedged_recently(memory):
        if _answered_recently(memory):
            return _choose(HELP_ALREADY, memory, clean)
    if pool is UNKNOWN:
        routed = finding_out.for_the_ask(clean, repaired, understood)
        if routed:
            said = _choose(routed, memory, clean)
            if said:
                return said
        day = for_the_day.for_the_ask(clean, repaired)
        if day:
            said = _choose(day, memory, clean)
            if said:
                return said
    named = _advisor(memory, clean, said, words)
    if named:
        return named
    for_the_thread = _who_for_the_thread(memory, clean, understood)
    if for_the_thread:
        return _choose(for_the_thread, memory, clean)
    if (_reads(_is_a_tips_ask, clean, repaired)
            or (understood.get("help_ask") and not NOT_A_TIPS_ASK.search(clean))):
        tips = _tips(memory, clean, repaired)
        if tips:
            return tips
        if (understood.get("help_ask") and not _reads(TIPS_ASKS.search, clean, repaired)
                and _hedged_recently(memory)):
            return _choose(pool, memory, clean)
        if _answered_already(memory):
            return _choose(HELP_ALREADY, memory, clean)
        return _choose(TIPS_LINES, memory, clean)
    if understood.get("tag"):
        if _answered_already(memory) and not TAG_CAN.search(clean):
            return _choose(TAG_CONFIRM, memory, clean)
        return _choose(TAG_UNSURE, memory, clean)
    if pool is UNKNOWN and _says_it_already(clean, list(understood.get("words") or []),
                                            memory):
        answer = _the_repeat_answer(memory)
        if answer:
            return _choose(SAME_AGAIN_WITH_THE_ANSWER, memory, clean).format(answer=answer)
        return _choose(SAME_AGAIN, memory, clean)
    pick = _bare_pick(clean, memory) or _bare_pick(repaired, memory)
    if pick:
        return _choose(pick, memory, clean)
    if (_a_dead_end(clean) and not _in_a_care_thread(memory)
            and not (_news_above(memory) or _a_subject_above(memory))):
        return _choose(DITHER_OPEN_LINES, memory, clean)
    about_a_person = _a_question_about_the_person(clean, memory)
    if about_a_person:
        return about_a_person
    if pool is UNKNOWN and A_STEP_ASK.match(str(clean or "").strip()) and _news_above(memory):
        return _choose(BARE_PICK_AFTER_NEWS, memory, clean)
    if pool is UNKNOWN:
        care = _a_care_home_line(understood, memory)
        if care:
            return care
    price = _a_price_wants_a_verdict(clean, memory)
    if price and pool is UNKNOWN:
        return _choose(price, memory, clean)
    if pool is UNKNOWN:
        mine = the_bots_own_answer(clean)
        if mine is None and repaired != clean:
            mine = the_bots_own_answer(repaired)
        if mine is not None:
            return _choose(mine, memory, clean)
        rule = _the_rule_for_it_for_the_turn(clean, repaired, memory)
        if rule is not None:
            return _choose(rule, memory, clean)
        place = None if findout.reads_as_crowd(clean) else the_place_the_answer_is_kept(clean)
        if place is None and repaired != clean and not findout.reads_as_crowd(clean):
            place = the_place_the_answer_is_kept(repaired)
        if place is not None:
            return _choose(place, memory, clean)
    if pool is UNKNOWN or pool is UNKNOWN_WORRY:
        from . import own_ask
        own = own_ask.answer(clean, memory)
        if own:
            return _choose([own], memory, clean)
    if pool is UNKNOWN:
        method = method_ask_pool(clean, memory)
        if method is None and repaired != clean:
            method = method_ask_pool(repaired, memory)
        if method is not None:
            return _choose(method, memory, clean)
    counted = _a_countdown_in_a_care_thread_(memory, clean, repaired, understood)
    if counted:
        return counted
    return _choose(pool, memory, clean)


def _a_countdown_in_a_care_thread_(memory, clean, repaired, understood):
    from .fallback_chain import _a_countdown_in_a_care_thread
    return _a_countdown_in_a_care_thread(memory, clean, repaired, understood)


def _the_view_asked_for(clean, memory):
    if not _is_a_view_ask(clean):
        return None
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    if not turns:
        if VIEW_NAMES_SOMEBODY.search(clean):
            return None
        return _choose(VIEW_NO_SUBJECT, memory, clean)
    last = turns[-1]
    said = str(last.get("bot") or "").strip()
    if not said:
        return None
    if _only_the_floor(said):
        answered = [t for t in (memory.get("turns") or [])
                    if isinstance(t, dict) and str(t.get("bot") or "").strip()
                    and t is not last and turns.index(t) < turns.index(last)]
        if not answered:
            return None
        last = answered[-1]
        said = str(last.get("bot") or "").strip()
        if _nothing_to_stand_behind(said):
            return None
    if not (ack.reads_as_a_receipt(said) or _in_a_pool(said, (NEUTRAL,))):
        said = _the_answer_in_reply(last.get("user"), said) or said
    while ack.reads_as_a_receipt(said) or _in_a_pool(said, (NEUTRAL,)):
        answered = [t for t in (memory.get("turns") or [])
                    if isinstance(t, dict) and str(t.get("bot") or "").strip()
                    and t is not last and turns.index(t) < turns.index(last)]
        if not answered:
            return None
        last = answered[-1]
        said = str(last.get("bot") or "").strip()
    if _only_a_reaction(last.get("module"), said):
        return _choose(VIEW_ON_GOOD_NEWS, memory, clean)
    if str(last.get("module") or "") in CARE_MODULES:
        if str(last.get("module") or "") in ("loss", "grief"):
            return _choose(VIEW_AFTER_A_DEATH, memory, clean)
        return None
    if any(phrase in said.lower() for phrase in VIEW_HANDBACK):
        return _choose(VIEW_DECIDE, memory, clean)
    if _is_a_hedge(said):
        return None
    if VIEW_MIRROR.match(said.lower()) and not _reads_as_a_claim(said) \
            and not _the_view_of(said)[0]:
        return _choose(VIEW_COMPANY, memory, clean)
    if not _reads_as_a_claim(said):
        first = re.split(r"(?<=[.!?])\s+", said.strip())[0].strip().lower()
        if not (VIEW_MIRROR.match(first) and _the_view_of(said)[0]):
            return None
    headline, mirrored = _the_view_of(said)
    if not headline:
        if mirrored:
            return _choose(VIEW_COMPANY, memory, clean)
        return None
    if headline.endswith("?"):
        lines = VIEW_ASK_LINES
    elif mirrored:
        lines = VIEW_MIRROR_LINES
    else:
        lines = VIEW_LINES
    return _choose(tuple(line.format(said=_after_a_colon(headline)) for line in lines),
                   memory, clean)
