import datetime
import random
import re
from ..compose import pick
from ..compose import ruledout
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
from ..memory import when as a_when
from ..memory import cause as a_reason
from ..memory import pending
from ..memory import another as second_half
from ..memory import choice as choose
from ..memory import condition
from ..memory import decided
from ..memory import company
from ..memory import spent
from ..memory import surname as family_name
from ..memory.filler import without_filler
from ..memory import guest
from ..memory import plans
from ..memory.taste import ASKS_ABOUT_A_TASTE, ASKS_FOR_TASTES, TASTE_ASKED_ABOUT
from ..memory.taste import read_all as read_tastes
from ..memory import facts as extract
from ..knowledge import cooking
from ..knowledge import units
from ..knowledge.maths import solve
from ..memory import counts as how_many
from ..memory import rates as rates_reader
from ..memory.times import answer as _the_time_they_said
from ..memory import history
from ..memory import narrow
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
from ..memory.repeat import a_narrowing_and_its_line as _a_narrowing_and_its_line
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
                          the_pronoun_said_with_a_name,
                          _the_group_word, _the_names_a_pronoun_gave,
                          _the_names_of_the_group, _the_names_they_typed, _their_job,
                          _their_taste, _they_like_sentence, _tidy_name,
                          _whether_they_have, _with_article)
from ..modules.memory_tables import (
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


def _a_count_ask(low):
    match = COUNT_ANIMAL.match(low)
    if match:
        word = match.group(1).lower().rstrip("s")
        return "pet" if word in ("pet", "puppie", "kitten", "bunnie", "horsie") else word
    if COUNT_BARE.match(low):
        return "any"
    return None

ASKED_ALL = re.compile(
    r"(?<!not )(?<!isnt )(?<!wasnt )\bwhat did i (?:just )?(?:ask|want to know)\b"
    r"(?![^.?!]*\babout\b(?!\s+(?:me|it|that|this|them|us|earlier|before|just now|first|"
    r"originally|already|so far|last time|the other day|that time)\b))"
    r"|\bwhat was it i asked\b"
    r"|(?<!not )(?<!isnt )(?<!wasnt )\bwhat i (?:just )?(?:asked|want to know)\b"
    r"(?=\s*(?:about\s*)?(?:\?|$|again\b|please\b|before\b|earlier\b|just now\b|first\b|"
    r"then\b|so far\b|already\b|the other day\b))")

MORE_OF_IT = re.compile(r"\b(what|anything|everything)\s+(?:else|more|other(?: things?)?)\b")

FIRST_ASK_BARE = re.compile(
    r"\bwhat i (?:asked|said|tell|told)(?: you)?(?: \w+){0,2} (?:first|at the (?:very )?start|"
    r"at the (?:very )?beginning|in the (?:very )?beginning)\s*\??$"
    r"|\bwhere (?:we|it|this|the (?:chat|conversation)) (?:all )?(?:started|began)\s*\??$"
    r"|\bwhich (?:question|thing) (?:did i|i) (?:ask|asked|say|said|start with|started with|"
    r"begin with|began with)\s*(?:you\s*)?(?:first|with)?\s*\??$")

FIRST_ASK = re.compile(
    FIRST_ASK_BARE.pattern + r"|"
    r"\bwhat did i (?:ask|say|tell)(?: you)?(?: \w+){0,2} (?:first|at the (?:very )?start|"
    r"at the (?:very )?beginning|in the (?:very )?beginning)\s*\??$"
    r"|\bwhat (?:was|were) (?:the |my )?(?:very )?first (?:thing|question|message|line|one)"
    r"(?: (?:i|you) (?:asked|said)(?: you)?)?\s*\??$"
    r"|\b(?:how|where) did (?:we|(?:this|our|the) (?:chat|conversation)) (?:start|begin|get started)\b"
    r"(?=$|[?.!,]| (?:it|this|here|that|off|talking|chatting|the chat|this chat|the "
    r"conversation|this conversation)\b)"
    r"|\bwhat did i say (?:at |in )?the (?:start|beginning)\s*\??$"
    r"|\bdo you remember what i (?:asked|said)(?: you)? first\s*\??$"
    r"|\bwhat did i (?:ask|say) first\s*\??$"
    r"|\b(?:can|could|do|did|would) you remember what i (?:asked|said|told)(?: you)?(?: \w+){0,2}"
    r" (?:first|at the start|at the beginning)\s*\??$"
    r"|\bwhat i (?:asked|said|told|mentioned)(?: you)?(?: \w+){0,3}?\s+"
    r"(?:very |the )?(?:first|start|beginning|begin)\b\s*\??$"
    r"|\bmy first (?:question|message|line|words)\b\s*\??$"
    r"|\bwhat did i (?:ask|say|tell)(?: you)? when we (?:started|began|first)\s*\??$"
    r"|\bremind me how (?:this|we|the chat|the conversation) (?:started|began)\b"
    r"|^(?:and |so |but )?(?:how|where) (?:did )?(?:this|the chat|our conversation|it)"
    r" (?:start|started|begin|began)\s*[?.!]*$")

REPEAT_TAIL = re.compile(r"\b" + REPEAT_ADVERB + r"\b", re.I)

REPEAT_ASK = re.compile(
    r"\b(?:say|said|repeat|tell me|read|hear|catch)(?: it| that| this)? again\b"
    r"|\bwhat did you (?:just )?say\b"
    r"|\bwhat did you tell me(?: (?:just )?now| earlier| before| so far)?\b"
    r"|\bwhat you (?:just )?(?:said|told me)\b"
    r"|\bcan you (?:repeat|say) (?:that|it)(?: again)?\b"
    r"|\bsay (?:that|it) once more\b"
    r"|\b(?:please\s+)?repeat\b(?!\s+(?:after|myself|yourself))"
    r"|\bsay (?:that|it) (?:again|once more|slower|slowly|simpler|clearer)\b"
    r"|\bexplain (?:it|that|this)(?: (?:again|once more|slower|more slowly|simply|more simply))?\b"
    r"|\b(?:go|walk|talk)(?: me)? (?:over|through) (?:it|that|this)\b"
    r"|\brun (?:it|that|this) by me\b"
    r"|\brun (?:it|that|this) (?:again|once more)\b"
    r"|\bthe (?:last|final) (?:bit|part)\b"
    r"|\b(?:you(?:'ve| have)? lost me|i lost you)\b"
    r"|\bwhat was that\b"
    r"|\bcome again\b"
    r"|\bpardon\b"
    r"|\bi missed (?:that|it)\b"
    r"|\bone more time\b"
    r"|\b(?:how long|how much|how many|how often|how soon|what time|when|where)\s+"
    r"did you (?:just )?say\b"
    + r"|\brepeat (?:that|it|this)(?:\s+" + REPEAT_ADVERB + r"){0,2}\s*[.!?]*$")

LAST_LINE_ASK = re.compile(
    r"\bwhat did you just say\b|\bwhat was that\b|\bpardon\b|\bcome again\b"
    r"|\bi missed (?:that|it)\b|\bdid(?:n't|nt) catch\b", re.I)

REPEAT_WORDS = frozenset("""
say said repeat again tell told speak word pardon missed catch hear one time just last line
remind reminded you please sorry thanks thank cheer cheers ta come that this it me now thing
slower slowly simpler clearer bit
explain explained go going through walk talk run ran by part parts lose lost there
how long much many often soon when where time
earlier ago previously minute moment before already so far up to now until now
""".split())

WHOLE_ASK = re.compile(
    r"^(?:(?:and|so|but|ok|okay|oh|right|well|yes|yeah|ta|please|then)\s+)*"
    r"(?:"
    r"in full|in the full|in full please|the full (?:thing|version|answer)"
    r"|the whole (?:thing|answer|lot|of it)|the whole of it please"
    r"|all of (?:it|that|this)|all of it please|both of (?:them|those)"
    r"|the lot|the lot please"
    r"|from the (?:top|start|beginning)|from the very (?:top|start|beginning)"
    r"|start (?:again )?from the (?:top|start|beginning)"
    r"|(?:say|tell me|give me) (?:it all|it in full|all of it|all of that|the lot)"
    r")"
    r"(?:[\s,]+(?:please|then|now|thanks|ta))*[\s.,!?]*$", re.IGNORECASE)

REPEAT_START = re.compile(
    r"^(?:(?:and|so|but|ok|okay|oh|then|well|right|hmm|um)\s+)*"
    r"(?:say|repeat|tell|read|hear|catch|can|could|would|will|what|sorry|pardon|please|thanks|"
    r"thank you|cheers|ta|come|again|"
    r"how|when|where|remind|reminded|one more|i missed|i didn't catch|i didnt catch|"
    r"explain|go|walk|talk|run|the|you|i lost|"
    r"didn't catch|didnt catch|do you|excuse me)\b")

REMINDER_MID = re.compile(
    r"\b(?:please |can you |could you |would you )?(?:remind me|tell me again|ask me again)"
    r"(?: again)?\b[\s,]*"
    r"|^\W*(?:do|did|can|could) (?:you|u) (?:still |actually |even |really )?"
    r"(?:know|remember|recall)\b[\s,]*")

REMINDER_HEAD = re.compile(
    r"^(?:(?:and|but|so|ok|okay|oh|also|right|well|sorry|hi|hey|just|quick|one more)\b[\s,]*)+")

REMINDER_TAIL = re.compile(r"(?:[\s,]*\b(?:again|please)\b)+$")

ABOUT_HEAD = re.compile(r"^(?:(?:and|but|so)\s+)?what about\s+")

ACTIVITY_ASK = re.compile(
    r"(?:\bwhat (?:was|am|were) i (?:making|cooking|baking|planning|doing|up to)|"
    r"\bwhat i (?:(?:just )?said )?(?:i )?was (?:doing|up to|making|cooking|baking|planning)|"
    r"\bwhat was i (?:going to|meant to) do)\b"
    r"(?!\s*(?:wrong|badly|bad|differently|silly|stupid|right|here|now))"
    r"(?![^.?!]*\b(?:this|next|coming)\s+(?:week|weekend|month|year|monday|tuesday|wednesday|"
    r"thursday|friday|saturday|sunday)\b|\btonight\b|\btomorrow\b|\bcoming up\b)")

PLAN_WORDS = re.compile(r"\bwhat (?:am i|are we) planning\b|\bwhat (?:have|has) (?:i|we) got\b|"
                        r"\bwhat do (?:i|we) have\b|\bcoming up\b|\bon for (?:me|us)\b")

UP_TO_ASK = re.compile(r"\bwhat (?:am i|are we) (?:planning|up to)\b|"
                       r"\bwhat (?:was|were) (?:i|we) (?:planning|up to)\b"
                       r"(?!\s*(?:wrong|badly|bad|differently|silly|stupid|right))")

NAMED_ACTIVITY = re.compile(r"\bwhat (?:was|am|were) i (?:making|cooking|baking)\b|"
                           r"\bwhat (?:was|am) i planning to\b")

ACTIVITY_WORDS = re.compile(
    r"\b(?:making|cooking|baking|roasting|preparing|building|painting|writing|sorting|"
    r"fixing|mending|planning|organising|organizing|packing|knitting|sewing|decorating|"
    r"gardening|going to|off to|about to|having|doing)\b", re.I)

ACTIVITY_LOOSE = re.compile(
    r"\b(?:want|wanted|need|needed|thinking of|plan|plans|planned|trying|meant|going) to "
    r"(?:make|cook|bake|roast|prepare|build|paint|write|sort|fix|mend|plan|organise|organize|"
    r"pack|do|have)\b", re.I)

ASK_LINE = re.compile(r"^\s*(?:so |and |but )?(?:what|which|who|when|where|why|how|can|could|"
                      r"would|should|do|did|does|is|are|was|were|will|shall|have|has|remind|"
                      r"tell|any)\b", re.I)

DETAIL_START = re.compile(
    r"^(?:he|hes|she|shes|they|theyre|it|its|it's|his|her|hers|their|theirs|them|the|this|that|"
    r"these|those|my|our|also|plus|and|but|so|yes|yeah|no|nope|ok|okay|sorry|thanks|right|true)\b",
    re.I)

STOPWORDS = frozenset("""the and but for with that this have has had was were are been being its
it's they them their there here about into from just only also very really quite then than when
what which who how why where some any all one two three four five six seven eight nine ten""".split())

def _bare(folded):
    asked = REMINDER_MID.search(folded or "")
    bare = REMINDER_MID.sub(" ", folded or "")
    bare = ABOUT_HEAD.sub("", bare)
    bare = REMINDER_HEAD.sub("", bare)
    bare = REMINDER_TAIL.sub("", bare)
    bare = CHAT_TAIL.sub("", bare).strip(" ,.;:!?")
    bare = " ".join(bare.split())
    flipped = WHEN_INVERTED.match(bare)
    if flipped:
        bare = f"when {flipped.group(3)} {flipped.group(1)} {flipped.group(2)}"
    elif asked:
        subject = WHEN_INVERTED_SUBJECT.match(bare)
        if subject:
            bare = f"when {subject.group(2).split()[0]} {subject.group(1)} " \
                   f"{' '.join(subject.group(2).split()[1:])}".strip()
    return bare

def _the_limits_on(entry):
    if not isinstance(entry, dict):
        return {}
    return {key: entry[key] for key in LIMITS if entry.get(key) not in (None, "", [], {})}

def _the_limit_they_share(text, memory):
    who = extract.the_limit_they_share(text)
    if not who or not isinstance(memory, dict):
        return None
    turns = memory.get("turns") or []
    before = str((turns[-1] or {}).get("user") or "") if turns else ""
    if not before:
        return None
    said = extract.extract(before)
    if not isinstance(said, dict):
        return None
    about_them = [(str(entry.get("who") or ""), _the_limits_on(entry))
                  for entry in (said.get("others") or []) if isinstance(entry, dict)]
    about_them = [(relation, limits) for relation, limits in about_them if relation and limits]
    about_me = _the_limits_on(said)
    if who == "i":
        if not about_them:
            return None
        relation, limits = about_them[-1]
        for key, value in limits.items():
            remember(memory, key, value, text)
        return _said_of_a_shared_limit(limits, "", memory)
    if who == extract.LAST_PERSON:
        named = [str(word) for word in (said.get("people") or []) if isinstance(word, str)]
        who = named[-1] if named else ""
        if not who:
            person = memory.get("person")
            who = str((person or {}).get("who") or "") if isinstance(person, dict) else ""
        if not who:
            return None
    if not about_me:
        return None
    remember_other(memory, dict(about_me, who=who), text)
    return _said_of_a_shared_limit(about_me, who, memory)

def _is_or_are(words):
    if len([word for word in words if str(word).strip()]) > 1:
        return "are"
    last = str(words[-1]).split()[-1] if words else ""
    return "are" if last.endswith("s") and not last.endswith("ss") else "is"

def _the_things(words):
    said = [str(word).strip() for word in words if str(word).strip()]
    if not said:
        return ""
    if len(said) == 1:
        return said[0]
    return ", ".join(said[:-1]) + " and " + said[-1]

def _said_of_a_shared_limit(limits, who, memory):
    things = list(limits.get("allergies") or [])
    if things:
        named = _the_things(things)
        if who:
            return pick(("Then " + named + " " + _is_or_are(things) + " off " + _their_own(who)
                         + "'s plate too — I'll keep both of you in mind.",
                         "Right, " + named + " out for " + _their_own(who) + " as well, then.",
                         "So " + named + " " + _is_or_are(things) + " off the table for "
                         + _their_own(who) + " too. Both of you, then."), memory, ())
        return pick(("Then " + named + " " + _is_or_are(things) + " off your plate too — I'll "
                     "answer for both of you.",
                     "Right, " + named + " out for you as well, then.",
                     "So " + named + " " + _is_or_are(things) + " off the table for you too."),
                    memory, ())
    diet = limits.get("diet")
    if diet:
        if who:
            return ("Then " + str(diet) + " for " + _their_own(who) + " as well — I'll plan around "
                    "the two of you.")
        return pick(("Then " + str(diet) + " for you as well — I'll plan around the two of you.",
                     "Same for you, then: " + str(diet) + ". I'll keep that straight."),
                    memory, ())
    condition = limits.get("condition")
    if condition:
        named = _the_things(condition if isinstance(condition, (list, tuple)) else [condition])
        if who:
            return pick(("Then " + _their_own(who) + " " + _is_or_are([named]) + " " + named
                         + " too — I'll keep it in mind for both of you.",
                         "Right, " + named + " for " + _their_own(who) + " as well, then. Both of "
                         "you.",
                         "So " + _their_own(who) + " has that too. I'll keep the two of you in "
                         "mind."), memory, ())
        return pick(("Then you have the same thing, " + named + " — I'll keep that in mind.",
                     "Same condition for you too, then: " + named + "."), memory, ())
    return None

def _their_own(who):
    word = str(who or "").strip().lower()
    return "your " + word if word and word not in ("i", "me") else "your"

MEATLESS_DIET = re.compile(r"vegetarian|vegan|veggie|plant|pescatarian|flexitarian", re.I)

def _the_back_this_turn(text, memory):
    done = memory.get("reversal") if isinstance(memory, dict) else None
    if not isinstance(done, dict) or done.get("said") != " ".join(str(text or "").lower().split()):
        return None
    who = str(done.get("who") or "")
    food = str(done.get("food") or "").strip()
    if not food:
        return None
    theirs = "your " + who if who in extract.RELATIONS else "them"
    if done.get("kind") == "taste":
        return pick(["Right \u2014 " + food + " back on the yes list for " + theirs + ", then.",
                     "Got it \u2014 " + theirs + " likes " + food + ", then.",
                     "Noted \u2014 " + food + " for " + theirs + " from now on, then."],
                    memory if isinstance(memory, dict) else {})
    return pick(["Right \u2014 " + food + " back on the plate for " + theirs + ", then.",
                 "Got it \u2014 " + food + " is back on the menu for " + theirs + ", then.",
                 "Fair enough \u2014 nothing off " + theirs + "'s plate, then."],
                memory if isinstance(memory, dict) else {})

def _still_holding(memory, animals):
    held = {str((pet or {}).get("animal") or "").strip().lower()
            for pet in ((memory.get("user") or {}).get("pets") or []) if isinstance(pet, dict)}
    return any(str(animal).lower() in held for animal in animals)

def _kind(item):
    return str(item.get("animal") or "") if isinstance(item, dict) else str(item)

SIZE_UNITS = {
    "kg": "kg", "kilo": "kg", "kilos": "kg", "kilogram": "kg", "kilograms": "kg",
    "g": "g", "gram": "g", "grams": "g", "lb": "lb", "lbs": "lb", "pound": "lb",
    "pounds": "lb", "oz": "oz", "ounce": "oz", "ounces": "oz", "pint": "pint",
    "pints": "pint", "litre": "litre", "litres": "litre", "liter": "litre",
    "liters": "litre", "ml": "ml", "cm": "cm", "mm": "mm", "inch": "inch", "inches": "inch",
}

A_SIZE = re.compile(r"\b(\d+(?:\.\d+)?)\s*(" + "|".join(sorted(SIZE_UNITS, key=len, reverse=True))
                    + r")\b", re.I)

SIZE_LINE_FILLER = frozenset((
    "its", "it", "is", "about", "around", "roughly", "mine", "ours", "the", "a", "an", "one",
    "weighs", "weigh", "weight", "of", "say", "like", "just", "not", "much", "more", "less",
    "over", "under", "approx", "approximately", "i", "have", "got", "ive", "thats", "that",
    "s", "and", "so", "yeah", "yes", "ok", "okay", "sorry", "actually", "probably", "think",
    "guess", "pretty", "already", "exactly", "nearly", "almost", "only", "total",
    "altogether", "definitely", "ish", "now", "still", "bought", "buy", "brought", "used",
    "was", "were", "we", "they", "it",
))

A_TIME = re.compile(r"\b\d+(?:\.\d+)?\s*(?:hour|hours|hr|hrs|minute|minutes|min|mins)\b",
                    re.I)

def _a_size(text):
    found = A_SIZE.search(str(text or ""))
    if not found:
        return None
    return found.group(1) + SIZE_UNITS[found.group(2).lower()]

def _only_names_the_size(text):
    flat = " ".join(str(text or "").lower().split())
    found = A_SIZE.search(flat)
    if not found or len(flat.split()) > 8:
        return False
    rest = (flat[:found.start()] + " " + flat[found.end():]).split()
    return all(word.strip(",.!?") in SIZE_LINE_FILLER for word in rest)

def _the_clause_that_works_it_out(answer, size):
    for clause in re.split(r"[,;.]", str(answer or "")):
        flat = " ".join(clause.split())
        if not flat or not A_TIME.search(flat) or _a_size(flat) != size:
            continue
        flat = re.sub(r"^(?:(?:and|so|then|which means|that means)\b[\s,]*)+", "", flat, flags=re.I)
        if flat:
            return flat[0].upper() + flat[1:] + "."
    return None

FEEDING_ASK = re.compile(
    r"\b(?:enough(?:\s+(?:for|to\s+feed))?|feed|feeds|serve|serves|do|does)\s+"
    r"(?:the\s+|it\s+|that\s+|this\s+|all\s+|all\s+of\s+)?"
    r"(\d{1,3}|a couple|a few|a dozen|half a dozen|two|three|four|five|six|seven|eight|nine"
    r"|ten|eleven|twelve)\b", re.I)

HEAD_COUNTS = {"a couple": 2, "a few": 3, "a dozen": 12, "half a dozen": 6}

HEAD_WORDS = {"two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
              "nine": 9, "ten": 10, "eleven": 11, "twelve": 12}

SIZE_GRAMS = {"kg": 1000.0, "g": 1.0, "lb": 453.59, "oz": 28.35}

BIRDS = frozenset(("chicken", "turkey", "duck", "goose"))

ANSWER_PORTION = re.compile(
    r"\b(\d{2,4})\s*g\b[^.,;]{0,24}?\b(?:each|a person|per person|per head|a head)\b", re.I)

SO_A_SIZE = re.compile(r"\bso\s+(?:an?\s+)?(\d+(?:\.\d+)?)\s*(" +
                       "|".join(sorted(SIZE_UNITS, key=len, reverse=True)) + r")\b", re.I)

def _the_people_that_size_feeds(text, memory):
    if not isinstance(memory, dict):
        return None
    said = " ".join(str(text or "").lower().split())
    found = FEEDING_ASK.search(said)
    if not found:
        return None
    count = HEAD_COUNTS.get(found.group(1).lower()) or HEAD_WORDS.get(found.group(1).lower())
    if not count:
        try:
            count = int(found.group(1))
        except (TypeError, ValueError):
            return None
    if not 2 <= count <= 40:
        return None
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    held = said + " " + " ".join(str(turn.get("user") or "").lower() for turn in turns[-3:])
    answers = " ".join(str(turn.get("bot") or "").lower() for turn in turns[-2:])
    portion = _the_portion_for_the_food(held, answers)
    if not portion:
        return None
    size = _a_size(text) or _the_size_on_the_screen(turns)
    if not size:
        return None
    return _the_portion_reply(size, portion, count)

MADE_ONLY = re.compile(r"\b(?:only|just)\s+(?:made|cooked|done|got|had|bought|used|managed|"
                       r"did|knocked)", re.I)

FOR_A_COUNT = re.compile(
    r"\bfor\s+(?:the\s+)?(\d{1,2}|two|three|four|five|six|seven|eight|nine|ten|eleven"
    r"|twelve)\b", re.I)

def _the_amount_they_made(text, memory):
    if not isinstance(memory, dict):
        return None
    said = " ".join(str(text or "").lower().split())
    if not MADE_ONLY.search(said):
        return None
    size = _a_size(text)
    if not size:
        return None
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    answer = " ".join(str(turn.get("bot") or "").lower() for turn in turns[-2:])
    counted = FOR_A_COUNT.search(str(turns[-1].get("bot") or "").lower()) if turns else None
    if not counted:
        return None
    count = HEAD_COUNTS.get(counted.group(1)) or HEAD_WORDS.get(counted.group(1))
    if not count:
        try:
            count = int(counted.group(1))
        except (TypeError, ValueError):
            return None
    if not 2 <= count <= 40:
        return None
    held = said + " " + " ".join(str(turn.get("user") or "").lower() for turn in turns[-3:])
    portion = _the_portion_for_the_food(held, answer)
    if not portion:
        return None
    return _the_portion_reply(size, portion, count)

def _the_portion_reply(size, portion, count):
    per, unit, noun, bone = portion
    if unit != "g":
        return None
    grams = _size_in_grams(size)
    if not grams:
        return None
    feeds = int(grams // per)
    if feeds < 1:
        return None
    line = "{size} of {noun}{bone}is about {per}g a person, so it feeds {feeds}".format(
        size=size, noun=(noun + " ") if noun else "", bone="on the bone " if bone else "",
        per=("%g" % per), feeds=_a_number_word(feeds))
    if feeds >= count:
        if feeds > count:
            return line + " \u2014 enough for {count}, with a second helping in it.".format(
                count=_a_number_word(count))
        return line + "."
    wanted = count * per
    wants = ("%gkg" % (wanted / 1000.0)) if wanted >= 1000 else ("%gg" % wanted)
    return line + ", and {count} wants about {wants}.".format(
        count=_a_number_word(count), wants=wants)

def _the_portion_for_the_food(held, answers):
    best = None
    for names, amount, unit, noun in units.PER_PERSON + units.PER_PERSON_WHEN_COUNTED:
        for name in names:
            if not re.search(r"\b" + re.escape(name) + r"\b", held):
                continue
            score = len(name) + (2 if re.search(r"\b" + re.escape(name) + r"\b", answers) else 0)
            if best is not None and score <= best[0]:
                continue
            if name in BIRDS:
                best = (score, (float(units.BIRD_GRAMS), "g", name, True))
            else:
                best = (score, (float(amount), unit, noun, False))
    if not best:
        return None
    per, unit, noun, bone = best[1]
    if unit != "g":
        return best[1]
    stated = ANSWER_PORTION.search(answers)
    if stated:
        return float(stated.group(1)), "g", noun, "on the bone" in answers
    return per, unit, noun, bone

def _the_size_on_the_screen(turns):
    for turn in list(reversed(turns))[:3]:
        size = _a_size(turn.get("user"))
        if size:
            return size
    for turn in list(reversed(turns))[:2]:
        worked = SO_A_SIZE.search(str(turn.get("bot") or ""))
        if worked:
            return worked.group(1) + SIZE_UNITS[worked.group(2).lower()]
    return None

def _size_in_grams(size):
    found = A_SIZE.match(str(size or ""))
    if not found:
        return None
    grams = SIZE_GRAMS.get(found.group(2).lower())
    if not grams:
        return None
    try:
        return float(found.group(1)) * grams
    except (TypeError, ValueError):
        return None

def _the_figure_for_the_size_they_named(text, memory):
    if not isinstance(memory, dict):
        return None
    size = _a_size(text)
    if not size or not _only_names_the_size(text):
        return None
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    if not turns:
        return None
    for turn in turns:
        if _a_size(turn.get("user")) == size:
            return None
    worked = SO_A_SIZE.search(str(turns[-1].get("bot") or ""))
    if worked and worked.group(1) + SIZE_UNITS[worked.group(2).lower()] == size:
        return None
    return _the_clause_that_works_it_out(turns[-1].get("bot"), size)

def _denial_this_turn(text, memory):
    gone = memory.get("denial") if isinstance(memory, dict) else None
    if not isinstance(gone, dict) or gone.get("said") != " ".join(str(text or "").lower().split()):
        return None
    others = ("allergies", "condition", "diet")
    if gone.get("who"):
        items = [str(item) for item in (gone.get("allergies") or []) if str(item)]
        if not items:
            return None
        who = str(gone.get("who"))
        theirs = "your " + who if who in extract.RELATIONS else "them"
        things = items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]
        return pick(["Right \u2014 " + things + " back on the table for " + theirs + ", then.",
                     "Good \u2014 no allergy to " + things + " for " + theirs + ", then.",
                     "Noted \u2014 " + things + " back on for " + theirs + "."],
                    memory if isinstance(memory, dict) else {})
    if gone.get("pets_died") and not any(gone.get(key) for key in others):
        return None
    kept = extract.extract(text)
    if gone.get("pets_given") and not any(gone.get(key) for key in others + ("pets",)):
        return None
    for key in ("allergies", "condition", "diet", "pets"):
        value = gone.get(key)
        if value:
            if key == "pets":
                given_line = ack.pet_given_away(text, memory)
                if given_line:
                    return given_line
                animals = sorted({str(pet.get("animal") or "pet")
                                  for pet in value if isinstance(pet, dict)})
                if not gone.get("pets_all") and animals and _still_holding(memory, animals):
                    continue
                shown = "pets" if gone.get("pets_all") else " or ".join(animals) or "pets"
            else:
                shown = ", ".join(str(item) for item in
                                   (value if isinstance(value, list) else [value]))
            fresh = kept.get(key)
            if fresh and key in CORRECTED_SAY:
                now = ", ".join(str(item) for item in
                                (fresh if isinstance(fresh, list) else [fresh]))
                return CORRECTED_SAY[key].format(thing=now, Thing=now[:1].upper() + now[1:],
                                                old=shown)
            if key == "diet" and not MEATLESS_DIET.search(shown):
                put_back = _a_diet_put_back(shown)
                if put_back:
                    return pick(["Right \u2014 " + put_back + " again, then.",
                                 "Got it \u2014 " + put_back + " again, then.",
                                 "Fair enough \u2014 " + put_back + " again, then."],
                                memory if isinstance(memory, dict) else {})
                label = "dieting" if str(shown).strip().lower() == "on a diet" \
                    else _diet_words(shown)
                return pick(["Right \u2014 no more " + label + ", then.",
                             "Right, " + label + " is off, then.",
                             "Fair enough \u2014 no more " + label + ", then."],
                            memory if isinstance(memory, dict) else {})
            return DENIAL_SAY.get(key, "{Thing} \u2014 scratch that, then.").format(
                thing=shown, Thing=shown[:1].upper() + shown[1:])
    return None

def _retraction_this_turn(text, memory):
    gone = memory.get("retraction") if isinstance(memory, dict) else None
    if not isinstance(gone, dict) or gone.get("said") != " ".join(str(text or "").lower().split()):
        return None
    keys = gone.get("keys") or []
    shown = [item for item in (gone.get("shown") or []) if item]
    if "pets" in keys and shown:
        thing = " and ".join(shown[:2])
        return pick(["Right \u2014 " + thing + " is off the record, then.",
                     "Taken back \u2014 no " + thing + " on my list any more."], memory)
    if "plans" in keys and not [key for key in keys if key != "plans"]:
        return pick(["Right \u2014 that plan is off the record, then.",
                     "Taken back: I\u2019ve nothing about that trip from you now.",
                     "Scratch that, then \u2014 the plan is out."], memory)
    phrase = RETRACT_SAY.get(keys[0]) if keys else None
    if phrase:
        return pick(["Right \u2014 " + phrase + " is off the record, then.",
                     "Dropped. " + phrase[:1].upper() + phrase[1:] + " is gone.",
                     "Taken back \u2014 I\u2019ve nothing from you on record about it now."],
                    memory)
    return pick(["Right, that\u2019s off the record then.",
                 "Taken back \u2014 I\u2019ve nothing on record about it now."], memory)

THEIR_NAMES = re.compile(
    r"\b(?:they|them|their|the\s+(?:two|three|four))\b[^.?]{0,20}?"
    r"\b(?:call|calls|called|calling|name|names|named)\b"
    r"|\b(?:call|called|name|named|callin)\s+(?:them|the\s+(?:two|three|four))\b", re.I)

ASKS_IT_BACK = re.compile(r"\b(?:again|remind me|remind|did i|earlier|told you|told me)\b", re.I)

def _told_readers():
    return {"allergies": lambda memory: _fact_reply(memory, "allergic to"),
            "budget": lambda memory: _fact_reply(memory, "budget"),
            "diet": lambda memory: _diet_reply(memory),
            "age": lambda memory: _age_reply(memory),
            "name": lambda memory: _name_reply(memory, "my name"),
            "job": lambda memory: _job_reply(memory),
            "plan": lambda memory: _plans_reply(memory, "what am i planning"),
            "places": lambda memory: _places_reply(memory, "where do i live"),
            "pets": _told_pet_reply,
            "family": _animal_family,
            "kids": lambda memory: _kids_reply(memory, "how many kids do i have") or ""}

OWN_ANIMAL_LINE = re.compile(
    r"\b(?:my|our)\s+(?:[a-z'\u2019-]+\s+){0,2}(?:dogs?|pupp(?:y|ies)|cats?|kittens?|pets?|"
    r"rabbits?|bunn(?:y|ies)|hamsters?|fish|horses?|pon(?:y|ies)|parrots?|guinea\s+pigs?)\b"
    r"|\b(?:i|we)\s+(?:have|had|got|keep|kept|'ve|ve|also\s+have|also\s+got)\b")

NOT_THEIR_ANIMALS = re.compile(
    r"\b(?:my|our)\s+(?:sister|brother|mum|mother|dad|father|friend|neighbour|neighbor|aunt|"
    r"uncle|cousin|gran|grandma|grandad|grandpa|colleague|boss|son|daughter|wife|husband|"
    r"partner|niece|nephew|flatmate|roommate|landlord)\b[^.!?]*\b(?:has|have|had|got|keeps?|"
    r"wants?|wanted)\b"
    r"|\b(?:in|at|from)\s+the\s+(?:park|rescue|shelter|centre|center|vet)\b"
    r"|\bthe\s+(?:rescue|shelter|breeder|neighbour|neighbor)\b[^.!?]*\b(?:had|has|have)\b"
    r"|\b(?:i|we)\s+(?:met|saw|passed|watched)\b")

def _the_line_before_is_their_own_animal(memory, back=3):
    for turn in reversed(list(memory.get("turns") or [])[-int(back):]):
        said = str(turn.get("user") or "").strip().lower()
        if not said:
            continue
        if NOT_THEIR_ANIMALS.search(said):
            return False
        if OWN_ANIMAL_LINE.search(said):
            return True
        if re.search(r"\b(?:dogs?|cats?|kittens?|pupp\w*|animals?|pets?|rabbits?|hamsters?|"
                     r"fish|horses?)\b", said):
            return False
    return False

def _the_names_again(folded, low, memory):
    if not isinstance(low, str) or not low.strip():
        return ""
    if not ASKS_IT_BACK.search(str(folded or low)) or not THEIR_NAMES.search(low):
        return ""
    pets = [pet for pet in (user(memory).get("pets") or []) if isinstance(pet, dict)]
    if not pets:
        return ""
    if not _the_line_before_is_their_own_animal(memory):
        return ""
    return _fact_reply(memory, "what are my pets called", "pet")

def _the_one_animal_with_a_name(memory):
    pets = [pet for pet in (user(memory).get("pets") or [])
            if isinstance(pet, dict) and pet.get("name")]
    if len(pets) != 1:
        return ""
    animal = str(pets[0].get("animal") or "pet")
    return _fact_reply(memory, "what is my " + animal + " called")

def _told_pet_reply(memory, animal):
    pets = [pet for pet in (user(memory).get("pets") or []) if isinstance(pet, dict)
            and _animal_family(str(pet.get("animal") or "")) == animal]
    if not pets:
        return ""
    if any(pet.get("name") for pet in pets):
        return _fact_reply(memory, "what is my " + animal + " called")
    return _fact_reply(memory, "how many " + animal + "s do i have")

NO_RECORD = re.compile(
    r"^(?:you haven'?t told me|you (?:didn'?t|did not) tell me|i don'?t have|"
    r"there'?s nothing|i haven'?t got)\b", re.I)

ASK_AND_PERSON = frozenset("""what which who is are was were does do did can could would should
she he they them their her his him my our mum mom mother dad father son daughter sister brother
kid kids child children wife husband partner parents gran nan grandma granny aunt uncle cousin
baby stepmum stepdad mother father baby allergic allergy allergies allergie diet eat eats eating
eaten food foods drink drinks allergic had has have anything else one""".split())

def _says_more_than_the_ask(low):
    for word in re.findall(r"[a-z']+", str(low or "").lower()):
        if len(word) < 3 or word in ASK_AND_PERSON or word in GENERIC_WORDS:
            continue
        if word.rstrip("s") in ASK_AND_PERSON:
            continue
        return True
    return False

GENERIC_WORDS = frozenset("""the and but for with that this these those there here about into
from just only also very really quite then than when what which who whom whose why how some any

not dont doesnt didnt im ive its it's youre youve like want need know tell told say said again
please thanks ok okay""".split())

HOW_FAR_ALONG = re.compile(
    r"\bhow far (?:along|gone)\b|\bhow many weeks (?:is|are|am|along|pregnant|gone|in)\b"
    r"|\bwhat week (?:is|are|am) (?:she|he|they|it|i|i in)\b|\bhow many weeks (?:pregnant|along)\b",
    re.I)

OWN_LENGTH_ASK = re.compile(r"\b(?:am i|i am|im|i'm|do i|did i)\b", re.I)

def _how_far_along(memory, low):
    said = str(low or "")
    if not HOW_FAR_ALONG.search(said):
        return None
    holding = [entry for entry in others(memory)
               if isinstance(entry, dict) and isinstance(entry.get("weeks"), int)]
    named = [entry for entry in holding
             if re.search(r"\b" + re.escape(str(entry.get("who") or "")) + r"\b", said)]
    if len(named) == 1:
        holding = named
    elif OWN_LENGTH_ASK.search(said):
        own = user(memory) or {}
        if isinstance(own.get("weeks"), int):
            return _a_number_word(int(own["weeks"])).capitalize() + " weeks."
        if own.get("pregnant"):
            return ("You didn't say how many weeks — tell me and I'll keep it, so the meal plans "
                    "fit where you are.")
    if not holding:
        return None
    if len(holding) > 1:
        who = _person_from_pronoun(said, memory)
        if who:
            holding = [entry for entry in holding
                       if str(entry.get("who") or "").lower() == who] or holding[-1:]
    weeks = int(holding[-1]["weeks"])
    return _a_number_word(weeks).capitalize() + " weeks."

def _a_length_i_have(memory, low):
    said = str(low or "")
    if not HOW_FAR_ALONG.search(said):
        return False
    holding = [entry for entry in others(memory or {})
               if isinstance(entry, dict) and isinstance(entry.get("weeks"), int)]
    named = [entry for entry in holding
             if re.search(r"\b" + re.escape(str(entry.get("who") or "")) + r"\b", said)]
    if len(named) == 1:
        return True
    if OWN_LENGTH_ASK.search(said):
        own = user(memory or {}) or {}
        return isinstance(own.get("weeks"), int) or bool(own.get("pregnant"))
    return bool(holding)

def _a_limit_kept_for_them(low, memory):
    who = _someone_else_named(low, memory)
    for known in others(memory):
        if known.get("who") != who:
            continue
        return bool(known.get("condition") or known.get("diet"))
    return False

PET_NAME_AGAIN = re.compile(
    r"\bwhat(?:'s|s| is| was)\s+(?:his|her|its|their)\s+name\b"
    r"|\bwhat\s+(?:is|was|are|were)\s+(?:he|she|it|they)\s+called\b"
    r"|\bwhat\s+(?:did|do)\s+(?:i|we)\s+(?:call|name)\s+(?:him|her|it|them)\b", re.I)

PET_NAME_SETTLED = re.compile(
    r"\bwhat\s+(?:shall|should|will|would)\s+(?:i|we)\s+(?:call|name)\s+(?:him|her|it|them)\b",
    re.I)

NAME_PICKED_AGAIN = re.compile(
    r"\b(?:what|which)\s+name\s+(?:did|do|have)\s+(?:i|we)\s+"
    r"(?:pick|picked|choose|chose|go for|settle on|settled on|end up with)\b"
    r"|\b(?:what|which)\s+(?:did|do|have)\s+(?:i|we)\s+"
    r"(?:pick|picked|choose|chose|go for|settle on|settled on|end up with)\b", re.I)

def _the_pick_asked_again(text, memory):
    low = " ".join(str(text or "").lower().replace("\u2019", "'").split())
    if not low or not NAME_PICKED_AGAIN.search(low):
        return None
    if re.search(r"\b(?:" + "|".join(extract.RELATIONS) + r")\b", low):
        return None
    named = [pet for pet in (user(memory).get("pets") or [])
             if isinstance(pet, dict) and pet.get("name")]
    if not named:
        return None
    pet = named[-1]
    name = str(pet.get("name") or "")
    animal = str(pet.get("animal") or "pet")
    if "name" not in low:
        subject = str(topic_subject(memory) or "").lower().split()
        if not subject or (animal.lower() not in subject and name.lower() not in subject):
            return None
        turns = memory.get("turns") if isinstance(memory, dict) else None
        recent = [str((one or {}).get("user") or "")
                  for one in (turns[-3:] if isinstance(turns, list) else [])]
        said = [(extract.bare_name(line) or "").lower() for line in recent]
        if not name or name.lower() not in said:
            return None
    return _vary((
        _called(name) + " \u2014 that is the one you picked for your " + animal + ".",
        "You went for " + _called(name) + ". I have it written down.",
        _called(name) + ". That is your " + animal + "'s name.",
    ), memory)

def _what_the_pet_is_called(text, memory):
    low = " ".join(str(text or "").lower().replace("\u2019", "'").split())
    if not low or not (PET_NAME_AGAIN.search(low) or PET_NAME_SETTLED.search(low)):
        return None
    if re.search(r"\b(?:" + "|".join(extract.RELATIONS) + r")\b", low):
        return None
    named = [pet for pet in (user(memory).get("pets") or [])
             if isinstance(pet, dict) and pet.get("name")]
    if not named:
        if PET_NAME_SETTLED.search(low):
            return None
        animal = _the_animal_of_the_pick(memory)
        if not animal or animal == "pet":
            return None
        return "You haven't told me a name for your " + animal + " yet."
    pet = named[-1]
    name = _called(str(pet.get("name")))
    animal = str(pet.get("animal") or "pet")
    return _vary((
        name + " \u2014 that is what you settled on for your " + animal + ".",
        "Your " + animal + " is called " + name + ".",
        name + ". I have that one written down.",
    ), memory)

def _the_name_they_picked(text, memory):
    said = extract.pet_name_only(text)
    if not said and _offered_here(memory):
        said = _name_they_answered(text, memory)
    if not said:
        return None
    pet = None
    for one in reversed(user(memory).get("pets") or []):
        if isinstance(one, dict) and str(one.get("name") or "").lower() == said.lower():
            pet = one
            break
    if pet is None:
        return None
    name = _called(str(pet.get("name") or said))
    animal = str(pet.get("animal") or "pet")
    return _vary((
        name + " it is. I'll remember that for your " + animal + ".",
        name + " \u2014 good choice, and easy to shout across a park.",
        "Right, " + name + ". That is the one from here on.",
    ), memory)

def _offered_here(memory):
    offered = extract.names_offered(memory)
    if not offered:
        return None
    return {"animal": _animal_family(offered["animal"]), "names": offered["names"]}

def _name_they_answered(text, memory):
    return extract.a_name_picked(text, memory)

def _the_animal_of_the_pick(memory):
    offered = _offered_here(memory)
    if offered and offered.get("animal"):
        return offered["animal"]
    turns = memory.get("turns") or []
    for turn in reversed(turns[-3:]):
        line = str((turn or {}).get("user") or "").lower()
        for word in re.findall(r"[a-z']+", line):
            if word in extract.ANIMALS:
                return _animal_family(word)
    pets = user(memory).get("pets") or []
    for pet in pets:
        if isinstance(pet, dict) and pet.get("animal"):
            return _animal_family(pet.get("animal"))
    return None

PLAN_LOW_START = frozenset("""in on the a an my our their his her its we i it that this there
you your you're youre you've you'll youd you'd i'm im we're save book get go see buy run start
finish take visit move learn do make find call pay email sort fix get see meet try keep""".split())

def _correction_this_turn(text, memory):
    fixed = memory.get("correction") if isinstance(memory, dict) else None
    if not isinstance(fixed, dict):
        return None
    if fixed.get("said") != " ".join(str(text or "").lower().split()):
        return None
    return _correction_said(fixed, memory) or None

def _the_second_pet_said(fixed, memory):
    animal = str((fixed or {}).get("animal") or "").strip().lower()
    pets = [pet for pet in (user(memory or {}).get("pets") or ()) if isinstance(pet, dict)]
    named = [str(pet.get("name") or "") for pet in pets
             if str(pet.get("animal") or "").strip().lower() == animal and pet.get("name")]
    if len(named) < 2:
        return ""
    named = [name[:1].upper() + name[1:] for name in named]
    thing = (_many(len(named), animal)[:1].upper() + _many(len(named), animal)[1:]
             + ", " + _a_list_of_names(named))
    return pick(ack.PET_TAIL_MANY, memory or {},
                str((fixed or {}).get("said") or "")).format(Thing=thing)

def _correction_said(fixed, memory=None):
    if not isinstance(fixed, dict):
        return ""
    if fixed.get("key") == "pets_more":
        return _the_second_pet_said(fixed, memory)
    if fixed.get("note"):
        return str(fixed["note"])
    value = fixed.get("value")
    if not value:
        return ""
    if fixed.get("key") == "job":
        note = _job_note(str(value), user(memory) if isinstance(memory, dict) else None)
        if note:
            return note
    in_a_sentence = fixed.get("key") in ("budget", "plan", "birthday") and fixed.get("sentence")
    if in_a_sentence:
        value = " ".join(str(fixed["sentence"]).split())
        unframed = ack.without_the_frame(value)
        if unframed and unframed != value:
            value = unframed
            if fixed.get("key") == "plan":
                bare = str(fixed.get("value") or "").strip()
                if bare and " ".join(value.split()).lower() in (
                        bare.lower(), "on " + bare.lower(), "in " + bare.lower(),
                        "at " + bare.lower()):
                    value = bare
        if fixed.get("key") == "plan":
            value = you(value)
            value = value[:1].lower() + value[1:]
        value = value.rstrip(" .!?")
    shown = str(value)[:1].upper() + str(value)[1:]
    wrong = str(fixed.get("wrong") or "").strip()
    if wrong:
        if fixed.get("key") == "pet":
            return pick(PET_RENAMED_SAY, memory,
                        str(fixed.get("said") or "")).format(v=shown, w=wrong)
        shape = CORRECTION_SAY_PAIR.get(fixed.get("key"), "{v}, not {w} — got it.")
        return shape.format(v=shown, w=wrong)
    if fixed.get("dropped"):
        shape = CORRECTION_SAY_DROP.get(fixed.get("key"), "Not {v} — got it.")
        said = str(value)
        return shape.format(v=said[:1].lower() + said[1:])
    if in_a_sentence:
        first, _, rest = shown.partition(" ")
        if first.lower() in PLAN_LOW_START:
            shown = first.lower() + (" " + rest if rest else "")
    if fixed.get("key") is None:
        return BARE_ECHO_ONLY.format(v=shown)
    shape = CORRECTION_SAY.get(fixed.get("key"), "{v} — got it, I'll go with {v}.")
    if "{a}" in shape:
        return shape.format(v=shown, a=str(fixed.get("animal") or "pet"))
    return shape.format(v=shown)

def _job_note(value, known):
    frame = str((known if isinstance(known, dict) else {}).get("job_frame") or "").strip()
    if frame == "work":
        return "Got it \u2014 your job is " + _a(str(value)) + "."
    if frame.split(" ")[0] not in ("at", "in", "for", "as"):
        return ""
    said = _job_said({"job": value, "job_frame": frame})
    if not said:
        return ""
    return "Got it \u2014 " + said[:1].lower() + said[1:] + "."

NOT_THE_SAME = re.compile(
    r"^(?:(?:and|but)\s+)?(?:my|our)\s+(?P<who>[a-z]+(?:[ -]in[ -]law)?)\s+"
    r"(?P<no>isnt|isn['\u2019]?t|is\s+not|doesnt|does\s+not|wasnt|was\s+not)$", re.I)

def _the_limit_the_last_line_gave(memory):
    said = " ".join(str(last_user(memory) or "").lower().split())
    if not said:
        return None
    for entry in reversed(memory.get("facts_log") or []):
        if not isinstance(entry, dict):
            continue
        if " ".join(str(entry.get("text") or "").lower().split()) != said:
            continue
        value = entry.get("value")
        if entry.get("key") in ("allergies", "diet"):
            return user(memory)
        if entry.get("key") in ("other", "others") and isinstance(value, dict) \
                and (value.get("allergies") or value.get("diet")):
            return value
    return None

def _not_the_same_reply(memory, low):
    if not isinstance(low, str):
        return None
    match = NOT_THE_SAME.match(" ".join(low.split()))
    if not match:
        return None
    who = _canon_relation(extract.a_person_word(match.group("who")))
    if who not in extract._A_WORD_FOR_A_PERSON:
        return None
    if not _the_limit_the_last_line_gave(memory):
        return None
    said = "your " + who
    return _vary(["Got it \u2014 " + said + " isn't.",
                  "Good to know \u2014 " + said + " isn't, then.",
                  "Right, so it's not " + said + " \u2014 noted."], memory)

_RELATION = "|".join(sorted(extract.RELATIONS, key=len, reverse=True))

OTHER_ASK = re.compile(
    r"\b(?:what|which|who)\b[^?]{0,40}?\b(?:my|your)\s+(?:"
    + _RELATION + r")\b|"
    r"\b(?:does|did|is|was)\s+(?:my|your)\s+(?:" + _RELATION + r")\b|"
    r"\bwhat (?:does|did) (?:she|he|they) eat\b|"
    r"\bwhat(?:'s|s| is| was)\s+(?:she|he|they)\s+(?:allerg\w*|not eat|eat)\b|"
    r"\bis (?:she|he|they)\s+allerg\w*\b|"
    r"\bwhat did i say (?:she|he|they|my|your)\b[^?]{0,30}?\b(?:eat|allerg\w*)\b|"
    r"\b(?:does|did) (?:she|he|they)\b[^?]{0,20}?\beats?\b", re.I)

OTHER_FACT = re.compile(r"allerg\w*", re.I)

WHO_IS_NAME_ASK = re.compile(
    r"\bwho(?:'s|s| is| was)\s+(?P<name1>[a-z][a-z'\-]{1,20})\b"
    r"|\bdo\s+(?:i|you)\s+(?:know|remember)\s+(?:a\s+|an\s+)?(?P<name2>[a-z][a-z'\-]{1,20})\b"
    r"|\bis\s+(?P<name3>[a-z][a-z'\-]{1,20})\s+(?:my|our)\s+(?P<who3>[a-z]+)"
    r"|\b(?P<name4>[a-z][a-z'\-]{1,20})\s+is\s+(?:my|our)\s+(?P<who4>[a-z]+)\s*[?.]?\s*$", re.I)

NAME_ASK_TAIL = frozenset("again then though please now too already anyway".split())

THEM = re.compile(r"\b(?:she|he|her|they|them|their|hers|his|him)\b", re.I)

OTHER_NAME_ASK = re.compile(
    r"\bwhat(?:'s|s| is| was| are)?\s+(?:do|did)?\s*(?:i|you)\s+call\s+(?:my|our)\s+"
    r"(?P<who1>" + KIN_ASK + r")\b"
    r"|\bwhat(?:'s|s| is| was)\s+(?:my|our)\s+(?P<who2>" + KIN_ASK + r")(?:'s|s')?\s+name\b"
    r"|\bwhat\s+(?:is|was|are|were)\s+(?:my|our)\s+(?P<who5>" + KIN_ASK + r")\s+called\b"
    r"|\bwhat\s+are\s+(?:my|our)\s+(?P<who3>" + KIN_ASK + r")\s+called\b"
    r"|\bm(?:y|ine)\s+(?P<who4>" + KIN_ASK + r")(?:'s|s')?\s+names?\s*(?:again)?\s*\??\s*$"
    r"|\b(?:do|did)\s+(?:you|u)\s+(?:remember|know)\s+(?:my|our)\s+(?P<who6>" + KIN_ASK + r")(?:'s|s')?\s+name\b"
    r"|\b(?:do|did)\s+(?:you|u)\s+(?:remember|know)\s+what\s+(?:my|our)\s+(?P<who7>" + KIN_ASK + r")\s+"
    r"(?:is|was|are|were)\s+called\b"
    r"|\bremind\s+me\s+(?:what\s+)?(?:my|our)\s+(?P<who8>" + KIN_ASK + r")\s+(?:is|was|are|were)\s+called\b"
    r"|\bremind\s+me\s+what\s+(?:my|our)\s+(?P<who9>" + KIN_ASK + r")(?:'s|s')?\s+name\s+is\b"
    r"|\bwhat\s+(?:my|our)\s+(?P<who10>" + KIN_ASK + r")\s+(?:is|was|are|were)\s+called\b"
    r"|\bwho(?:'s|s| is| was)\s+(?:my|our)\s+(?P<who11>" + KIN_ASK + r")\s*(?:called|again)?[\s?.!]*$",
    re.I)

PRONOUN_NAME_ASK = re.compile(
    r"\bwhat(?:'s|s| is| was)\s+(?P<pos>his|her|their)\s+name\b"
    r"|\bwhat\s+(?:are|were)\s+(?P<pos4>his|her|their)\s+names?\b"
    r"|\bwhat\s+(?:is|was|are)\s+(?P<sub>he|she|they)\s+called\b"
    r"|\bwhat\s+(?:do|did)\s+(?:i|you)\s+(?:call|say)\s+(?P<obj>him|her|them)\b"
    r"|\b(?:do|did)\s+(?:you|u)\s+(?:remember|know)\s+(?P<pos2>his|her|their)\s+name\b"
    r"|\b(?:do|did)\s+(?:you|u)\s+(?:remember|know)\s+what\s+(?P<sub2>he|she|they)\s+"
    r"(?:is|was|are)\s+called\b"
    r"|\bremind\s+me\s+what\s+(?P<obj2>him|her|them)\s+(?:is|was)\s+called\b"
    r"|\bwhat\s+(?P<pos3>his|her|their)\s+name\s+(?:is|was)\b", re.I)

def _with_an_in_law(who, low):
    if not who:
        return who
    if extract.an_in_law(who):
        return extract.a_person_word(who)
    if re.search(r"\b" + re.escape(who) + r"s?" + IN_LAW_AFTER_TEXT, low or "", re.I):
        return who + " in law"
    return who

KIDS_ASK = re.compile(
    r"\bhow many (?:kids?|children|child)\b|"
    r"\bdo (?:i|we) have (?:any )?(?:kids?|children)\b|"
    r"\b(?:have|did) (?:i|we) (?:got|have) (?:any )?(?:kids?|children)\b", re.I)

KIDS_SOMEONE_ELSE = re.compile(
    r"^\W*(?:do|does|did|has|have|had|is|are|was|were)\s+"
    r"(?:my|our|his|her|their|your|you|the|she|he|they|them|it)\b", re.I)

KIDS_A_DECISION = re.compile(r"\b(?:should|shall|worth|afford|too many|enough|ok|okay|normal)\b",
                             re.I)

def _kids_ask(low):
    match = KIDS_ASK.search(low) if isinstance(low, str) else None
    if not match:
        return False
    if KIDS_SOMEONE_ELSE.match(low[match.end():]):
        return False
    return not KIDS_A_DECISION.search(low)

ABOUT_A_NAME = re.compile(
    r"\b(?:what|anything|everything|much|else)\b[^?]{0,30}?\b(?:know|knows|knew|remember|"
    r"told|tell|said|say|mention|mentioned)\b[^?]{0,25}?\babout\s+([a-z][a-z'-]{1,20})\b|"
    r"\b(?:do|did|can)\s+(?:you|i)\s+(?:ever\s+)?(?:know|remember|tell|told|mention|say|said)\b"
    r"[^?]{0,30}?\babout\s+([a-z][a-z'-]{1,20})\b", re.I)

CHILDREN_ABOUT = re.compile(r"\b(?:kids?|children|child|boys?|girls?|sons?|daughters?|"
                            r"twins?|lads?|lasses|youngest|eldest|oldest)\b", re.I)

ABOUT_PERSON_MORE = re.compile(r"\b(?:else|other|more|anything)", re.I)

EAT_ASK = re.compile(r"\b(?:eat|eats|eating|diet|vegan|vegetarian|pescatarian)\b", re.I)

FOOD_ASK = re.compile(r"\b(?:eat|eats|eating|eaten|food|foods|drink|drinks|drinking|diet|"
                      r"meal|meals|breakfast|lunch|dinner|snack|cook|cooking)\b", re.I)

DIET_ASK = re.compile(r"\bmy diet\b|\bwhat (?:do|did) i eat\b|\bwhat am i eating\b|"
                      r"\b(?:what|which) diet (?:am i|do i|did i|was i)\b|"
                      r"\bwhat (?:can|can't|cant|could) i (?:not )?(?:eat|have)\b|"
                      r"\bwhat do i not eat\b|\bam i (?:vegetarian|vegan|pescatarian|on a diet)\b",
                      re.I)

DIET_HOW_TO = re.compile(r"\bhow (?:do|does|can|could|should|would|might|to)\b|"
                         r"\bany (?:tips|advice|ideas|suggestions|ways)\b|"
                         r"\bways? to\b|\bwhat can i do\b|\bhelp me\b|\btips for\b", re.I)

DIET_FACT_ASK = re.compile(
    r"\bmy diet\b|"
    r"\bwhat do i not eat\b|"
    r"\bwhat (?:can't|cant|couldn't|could not|can not) i (?:eat|have)\b|"
    r"\bwhat (?:can|could) i not (?:eat|have)\b|"
    r"\bam i (?:vegetarian|vegan|pescatarian|on a diet)\b", re.I)

ASK_WORD = re.compile(r"\b(?:what|which)\b", re.I)

HELP_ASK = re.compile(r"\b(?:should|could|can|shall|cook|make|recipe|recipes|meal|meals|dinner|"
                      r"lunch|breakfast|snack|safe|help|suggest|ideas?)\b", re.I)

CANT_HAVE = re.compile(
    r"\b(?:can(?:not|\s+not|'?t)|could(?: not\b|n'?t)|must(?: not\b|n'?t)|"
    r"should(?: not\b|n'?t)|may not)\b[^?!.]{0,14}?\b(?:have|eat|drink)\b"
    r"|\bwhat\b[^?!.]{0,30}?\b(?:to )?avoid\b|\b(?:things?|foods?|stuff)\s+to avoid\b", re.I)

CAN_HAVE = re.compile(r"\bwhat\b[^?!.]{0,30}?\b(?:can|could)\s+\w+\s+(?:have|eat|drink)\b", re.I)

CAN_THEY_HAVE = re.compile(
    r"\b(?:can|could|should|may)\s+(?:he|she|they|him|her|them)\s+(?:have|eat|drink)\b"
    r"|\bis\s+[a-z][a-z'\u2019 -]{1,24}?\bok\s+(?:for|with)\s+(?:him|her|them)\b"
    r"|\bdoes\s+(?:he|she|they)\s+(?:eat|drink|have)\b", re.I)

CAN_THEY_HAVE_A_FOOD = re.compile(
    r"\b(?:can|could|should|may)\s+(?:he|she|they|him|her|them)\s+(?:have|eat|drink)\s+"
    r"(?!(?:for|with|at|on|in|to|instead)\b)[a-z]", re.I)

FOOD_HAS = {
    "dairy": frozenset("""milk cheese butter cream yoghurt yogurt custard latte cappuccino
        cheddar mozzarella feta parmesan brie ice cream ice-cream milkshake ghee paneer""".split()),
    "gluten": frozenset("""bread pasta flour wheat cereal biscuit biscuits cake pastry
        couscous cracker crackers noodles pizza baguette toast bun buns pitta pita rye barley""".split()),
    "wheat": frozenset("""bread pasta flour cereal biscuit biscuits cake pastry noodles
        couscous cracker crackers pizza baguette toast bun buns pitta pita""".split()),
    "sugar": frozenset("""cake chocolate sweets sweets biscuits jam honey syrup pudding
        ice cream ice-cream fizzy juice cola""".split()),
    "nuts": frozenset("""peanuts pesto satay muesli granola almond almonds cashew
        cashews hazelnut hazelnuts walnut walnuts pecan pecans pistachio pistachios
        marzipan praline nutella""".split()),
    "peanuts": frozenset("""peanuts pesto satay""".split()),
    "shellfish": frozenset("""prawns prawn shrimp shrimps crab lobster mussels scallops
        shellfish seafood""".split()),
    "fish": frozenset("""salmon tuna cod haddock sardines mackerel anchovy anchovies
        trout prawns""".split()),
    "eggs": frozenset("""egg mayonnaise mayo meringue omelette omelette frittata
        custard""".split()),
    "soya": frozenset("""tofu edamame soy soya miso tempeh""".split()),
    "sesame": frozenset("""tahini hummus sesame houmous""".split()),
}

STATED_THEN_ASKED = re.compile(r",\s*(?=(?:what|which|how|why|when|where|who|should|can|could|"
                               r"would|will|is|are|do|does|any)\b)", re.I)

ASKS_WITH_WH = re.compile(r"\b(?:what|which|how|why|when|where|who)\b", re.I)

def _the_ask_after_a_statement(low, memory=None):
    text = str(low or "")
    read = memory.get("understood") if isinstance(memory, dict) else None
    if isinstance(read, dict):
        clauses = read.get("clauses")
        focus = read.get("focus")
        if isinstance(clauses, list) and len(clauses) > 1 and focus:
            asked = " ".join(str(word) for word in focus if str(word or "").strip()).strip()
            first = " ".join(str(word) for word in (clauses[0] or ()))
            if asked and asked != text.strip() and asked != first.strip():
                return asked
    parts = STATED_THEN_ASKED.split(text, 1)
    if len(parts) < 2 or ASKS_WITH_WH.search(parts[0]):
        return text
    asked = parts[1].strip()
    return asked or text

def _asks_about_someone(low, text, memory=None):
    whole = str(low or "")
    if not _asks_the_line(whole, text):
        return False
    ask = _the_ask_after_a_statement(whole, memory)
    if ask.strip() == whole.strip():
        return True
    return _asks_the_line(ask, text)

def _asks_the_line(low, text):
    low = str(low or "")
    if OTHER_ASK.search(low):
        return True
    if _asks_for_a_limit_not_advice(low) and (
            ASK_WORD.search(low) or ASK_START.search(low)
            or str(text or "").strip().endswith("?")):
        return True
    if DIET_ASK.search(low) and not DIET_HOW_TO.search(low):
        return False
    if not (EAT_ASK.search(low) or CANT_HAVE.search(low) or CAN_HAVE.search(low)
            or CAN_THEY_HAVE.search(low) or OTHER_FACT.search(low)):
        return False
    return bool(ASK_WORD.search(low) or ASK_START.search(low) or CAN_THEY_HAVE.search(low)
                or str(text or "").strip().endswith("?"))

THE_CHAT_ASK = re.compile(
    r"\bwhat (?:were|are|was) (?:we|i|you) (?:talking|chatting|saying|on) about\b|"
    r"\bwhat (?:were|are|was) (?:we|i) (?:on|up to)\b|"
    r"\bwhat (?:were|was) you (?:on|up to)\b|\bwhat are you on about\b|"
    r"\bwhat (?:were|was) you saying\b|"
    r"\bwhat (?:have|had|did) (?:we|you) (?:talked|spoken|chatted|covered|discussed) about\b|"
    r"\bwhat (?:were|are|was) (?:we|i|you) saying\b|"
    r"\bwhere (?:were we|are we)(?=\s*[?.!,]|\s*$)|"
    r"\bwhere did we (?:leave|get to|stop)\b|\bwhere we (?:got to|left off)\b|"
    r"\bwhat was i (?:saying|on about|telling you|mentioning)\b|\bcatch me up\b|\brecap\b|"
    + MISSED_CATCH_UP.pattern + r"|"
    r"\bwhat have i been (?:saying|telling you)\b|"
    r"\bremind me (?:what|where|how)\b|\bsum (?:up )?what we\b|"
    r"\bwhat we (?:have|had) (?:covered|talked|discussed|done|said|been on)\b|"
    r"^(?:and |but |so |ok |okay |also |now )?what we "
    r"(?:covered|talked|discussed|done|said|been on)\b"
    r"(?=\s*(?:[?.!,]|$|again\b|so far\b|before\b|earlier\b|today\b|already\b))|"
    r"\bwhat we (?:talked|spoke|spoken|chatted|covered|discussed) about\b|"
    r"\bwhat we were (?:on|up to)\b", re.I)

def _about_the_bot_here(memory):
    reading = memory.get("understood") if isinstance(memory, dict) else None
    if not isinstance(reading, dict):
        return False
    if the_manners_question(reading.get("norm") or []):
        return True
    if not reading.get("about_bot"):
        return False
    return reading.get("about_bot_kind") != "memory"

def _about_this_chat(text, memory=None):
    if _about_the_bot_here(memory):
        return False
    if history.asked(text):
        return True
    if recall.ask(text) == "me":
        return True
    if reminded.about_a_thing_they_said(text, memory):
        return True
    folded = _folded(text, memory)
    low = MORE_OF_IT.sub(r"\1", _bare(folded))
    if _a_count_ask(low) is not None:
        return True
    if memory is not None and _a_length_i_have(memory, low):
        return True
    checks = (
        r"\b(?:what|which)\b.*\bmy name\b|\bwho am i\b|\b(?:know|remember) my name\b|"
        r"\bwhat did (?:i|u|you) (?:say|tell me) my name was\b|^my name$|\bwhat my name (?:is|was)\b",
        r"\bwhere do (?:i|we) (?:live|work|come from)\b",
        r"\bwhat did i say my job\b|\bwhat(?:'s| is| was) my job\b|\bwhere do (?:i|we) work\b|"
        r"\bwhat did i say i (?:do|did)\b|\bwhat do i work as\b|\bwhat do i do for (?:a )?living\b",
        PLACES_ASK.pattern + r"|\bwhere do (?:i|we) work\b",
        r"\bwhat(?:'s| is| was) my (?:dog|cat|pet)(?:'?s)?\b|"
        r"\bwhat did i say my (?:dog|cat|pet)(?:'?s)?\b|"
        r"\bremember my (?:dog|cat|pet)(?:'?s)?\b|\bwhat do i call my (?:dog|cat|pet)(?:'?s)?\b|"
        r"\bwhat did i call my (?:dog|cat|pet)(?:'?s)?\b|"
        r"\bwhat(?:'s| is| was) my (?:dog|cat|pet)(?:'?s)? called\b|"
        r"\bwhat are my (?:pets|dogs|cats) called\b|\bwhat are my (?:pets|dogs|cats)\b|"
        r"\bwhat did i say my (?:pets|dogs|cats) (?:were|are) called\b|"
        r"\bwhat my (?:dog|cat|pet)(?:'?s)?\b|^my (?:dog|cat|pet)(?:'?s)?$",
        r"\bwhat (?:am|was) i allergic to\b|\bwhat i (?:am|was) allergic to\b|"
        r"\bwhat did i say i (?:am|was) allergic to\b|"
        r"\bwhat(?:'s| is| was)? my budget\b|\bmy budget again\b|\bwhat did i say my budget was\b|"
        r"^my budget$",
        r"\bmy diet\b|\bwhat do i not eat\b|"
        r"\bwhat (?:do|did) i eat\b(?=\s*[?.!,]|\s*$)|"
        r"\bwhat am i (?:eating|not eating)\b",
        THE_CHAT_ASK.pattern,
        r"\bwhat did i (?:just )?(?:ask|want to know)\b"
        r"(?![^.?!]*\babout\b(?!\s+(?:me|it|that|this|them|us)\b))|"
        r"\bwhat did i (?:just )?say\b(?!\s+(?:about|to|when|in|on|wrong)\b)|"
        + ACTIVITY_ASK.pattern + "|" + PLAN_MINE.pattern,
        r"\bwhat have i told you\b|\bwhat do you (?:know|remember) about me\b|"
        r"\bwhat did i (?:tell|say)(?: you)? about me\b|\bwhat do you know about me\b|"
        r"^what i (?:told|said)(?: you)?$|^what have i (?:told|said)(?: you)?$",
        r"\bremember what we talked about\b|\bdo you remember (?:what|our|yesterday|me)\b",
        WHAT_I_SAID.pattern + r"|\bwhat was it i said\b|"
        r"\bwhat (?:was|were) (?:i|we) (?:telling you|mentioning|on about)\b|"
        r"\bwhat have i been (?:saying|telling you)\b|"
        r"\b(?:what|anything) (?:i|we) (?:said|told you|mentioned|asked)"
        r"|\bwhere (?:we|it|this|the (?:chat|conversation)) (?:all )?(?:started|began)\b"
        r"|\bwhich (?:question|thing) (?:did i|i) (?:ask|asked|say|said|start with|started with)\b"
        r"(?=\s*(?:\?|$|again\b|please\b|about\b|i\b|my\b|the\b|that\b|"
        r"to (?:me|you)\b|before\b|earlier\b))|"
        r"\b(?:do|can|could|did) (?:you|u) remember what i\b",
        r"^what i (?:do|did)$|\b(?:remind me|tell me|can you (?:remind me|tell me)) what i (?:do|did)\b|"
        r"\bwhat did i say my age\b|\bhow old am i\b|\bwhat(?:'s| is| was)? my age\b|"
        r"\bmy age again\b|\bhow old did i say\b|"
        r"\bhow old i (?:am|was)\b",
        r"\bwhat (?:am i|are we) (?:planning|up to)\b|\bwhat (?:am i|are we) doing\b(?!\s+wrong)\b|"
        r"\bwhat(?:'s| is|s)?\s+(?:coming up|on for (?:me|us))\b|"
        r"\bwhat (?:have|has) (?:i|we) got (?:coming up|on|planned)?\b|"
        r"\bwhat do (?:i|we) have (?:coming up|on|planned)\b|"
        r"\banything (?:planned|coming up)\b|\banything on\b" + NOT_ON_A_MEDIUM +
        r"|\bwhat am i looking forward to\b|"
        r"\bwhat (?:was|were) (?:i|we) (?:planning|saving|saving up)\b|"
        r"\bwhat (?:am i|are we|is) (?:saving|saving up)\b|"
        r"\bwhat i (?:was|am) (?:planning|saving)\b|"
        r"\bwhat(?:'s| is| was) my plan\b" + NOT_THE_PLAN + r"|"
        r"\bwhat was (?:the|my) plan\b" + NOT_THE_PLAN + r"|"
        r"\bwhat was i going to do\b(?:\s*then)?\s*[?.!,]*$|"
        r"\bwhere (?:are|were|was|am) (?:we|i) (?:going|off|headed|heading|away)\b|"
        r"\bwhen (?:are|were|was|am) (?:we|i) (?:off|going|away|moving|flying|travelling)\b|"
        r"\b(?:which|what) (?:month|day|week|date) (?:are|am|is) (?:we|i)\b|"
        r"\bremind me where\b",
    )
    if ASKED_ALL.search(low):
        return True
    if any(re.search(pattern, low) for pattern in checks):
        return True
    if TOPIC_ASK.search(low) or ASK_WITHOUT_MY.search(low):
        return True
    if _summary_ask(low):
        return True
    named = THING_AGAIN.match(low)
    if named and _said_word(named.group(1), memory):
        return True
    if _which_thing_was_it(low, memory):
        return True
    if _an_attribute_they_gave(low):
        return True
    if _an_open_attribute_ask(low, memory):
        return True
    if re.search(r"^my (?:job|work|name|budget)$", low) and _recall_in_progress(memory):
        return True
    if FIRST_ASK.search(low) or SAID_ASK.search(low) or _repeat_ask(text, folded):
        return True
    if memory is not None and spent.PRESENT_ASK.search(text or "") and spent.answer(text, memory):
        return True
    if not re.search(r"\bwhat do i do\b", low) or len(low.split()) > 7:
        return False
    if MEMORY_POINTER.search(folded) or _recall_in_progress(memory):
        return True
    return _job_just_said(memory, low)

ASK_TAIL_FILLER = frozenset("""then now again here today tonight please thanks ok okay so also
just really honestly exactly mate actually""".split())

ASK_ABOUT_JOB = re.compile(
    r"^(?:at work|for a living|for work|for a job|all day|day to day|in the week|"
    r"when i(?:'m| am) at work|in my job|at the moment|these days)$")

def _ask_about_the_job(ask):
    found = re.search(r"\bwhat do i do\b(.*)$", " ".join(str(ask or "").lower().split()))
    if not found:
        return True
    tail = " ".join(word for word in re.findall(r"[a-z']+", found.group(1))
                    if word not in ASK_TAIL_FILLER)
    return not tail or bool(ASK_ABOUT_JOB.match(tail))

def _job_just_said(memory, ask=""):
    me = user(memory) or {}
    job = me.get("job")
    line = last_user(memory) or ""
    if not job or not line:
        return False
    said = " ".join(str(job).lower().split())
    place = " ".join(str(me.get("workplace") or "").lower().split())
    if not (said in " ".join(line.lower().split()) or _job_words_seen(job, line)):
        if not (place and _the_place_said(place, line)):
            return _a_work_detail(line) and _ask_about_the_job(ask)
    if not _only_the_job(line, job, place):
        return False
    return _ask_about_the_job(ask)

SELF_DO_AGAIN = re.compile(
    r"\bwhat (?:do|should|shall|can) i do again\b|"
    r"\bwhat i (?:do|did) again\b")

def _doing_again(text, memory):
    folded = _folded(text or "", memory)
    if not SELF_DO_AGAIN.search(folded):
        return False
    if _recall_in_progress(memory):
        return False
    job = (user(memory) or {}).get("job")
    line = last_user(memory) or ""
    if job and (str(job).lower() in line.lower() or _job_words_seen(job, line)):
        return False
    return not _job_just_said(memory, "what do i do again")

WORK_WORDS = frozenset("""
    work works working worked job jobs shift shifts rota office shop store school site floor
    till ward class classes year years teach teaches teaching taught lesson lessons pupil pupils
    student students manage managing manager boss team colleagues employer staff run running look looking after
    stack stacking shelf shelves serve serving customers clients patients drive driving nurse
    nursing clean cleaning cook cooking chef sort sorting stock sell selling till fix fixing
    build building repair study studying train training paperwork spreadsheets meetings meeting
    emails email calls call desk counter kitchen warehouse factory clinic hospital
""".split())

NOT_A_DETAIL = frozenset("""
    hurt hurts hurting ache aches aching pain pains ill sick unwell tired exhausted stressed
    worry worried anxious sad low fed depressed killing killed broke broken leaking wrong
    problem problems cross upset angry cry crying lost quit quitting leaving left fired sacked
    bullying bullied
    hate hates hated love loves fancy stole stealing short complaint complained warned blamed
    mistake mistakes accident incident busy rush
    today tonight tomorrow morning mornings evening evenings afternoon afternoons later soon
    every each weekly daily
""".split())

def _a_work_detail(line):
    low = " ".join(str(line or "").lower().split())
    if not low.startswith(("i ", "im ", "i'm ", "we ", "we're ")):
        return False
    words = {word.strip(",.!?;:'\"()") for word in low.split()}
    words.discard("")
    if len(words) > 10 or "?" in low:
        return False
    if words & NOT_A_DETAIL:
        return False
    if not words & WORK_WORDS:
        return False
    for word in words:
        if word in WORK_WORDS or word in JOB_ONLY or word.isdigit():
            continue
        return False
    return True

def _job_words_seen(job, line):
    mine = set(content(job))
    for word in str(job).split():
        mine |= forms(word)
    seen = set(content(line))
    return bool(mine & seen) or any(mine & forms(word) for word in seen)

JOB_ONLY = frozenset("""
    i im am a an the my me and but so oh also too now just still actually really always
    sometimes only since ago these days day days night early late full part time hour hours
    week weeks month months year years shift shifts work working works job started start new
    mostly usually lots few two three four five
    as at in for on of to do doing it that this
    changed change changes switched switching switch job jobs role career quit quits left leaving
    packed gave lost moved got get getting have had
    today tomorrow soon next monday tuesday wednesday thursday friday saturday sunday january
    february march april may june july august september october november december spring summer
    autumn winter
""".split())

def _the_place_said(place, line):
    words = set(content(place))
    if not words:
        words = {word.strip(",.!?;:'\"()") for word in str(place).lower().split()}
        words -= PLACE_LITTLE
    if not words:
        return False
    said = {word.strip(",.!?;:'\"()") for word in str(line).lower().split()}
    return words <= (set(content(line)) | said)

PLACE_LITTLE = frozenset("a an the in at on of to for my our their".split())

def _only_the_job(line, job, place=""):
    line = extract.TAKE_BACK_SPLIT.split(str(line), 1)[0]
    left = {word.strip(",.!?;:'\"()") for word in
            " ".join(str(line).lower().split()).split()}
    left.discard("")
    mine = set()
    for word in str(job).lower().split():
        mine.add(word)
        mine |= {form.lower() for form in forms(word)}
    mine |= {word.lower() for word in content(str(job))}
    for word in str(place or "").lower().split():
        mine.add(word)
        mine |= {form.lower() for form in forms(word)}
    mine |= {word.lower() for word in content(str(place or ""))}
    return all(word in JOB_ONLY or word in mine for word in left)

TALKED_ABOUT = re.compile(
    r"\bwhat (?:did|have|had) we (?:talk|talked|chat|chatted|speak|spoken|discuss|discussed)"
    r" about\b|\bwhat (?:did|have|had) we (?:cover|covered|discuss|discussed|talk about)\b|"
    r"\b(?:talk|walk|run|take) (?:me )?through (?:what|everything) (?:we|i) (?:said|covered|talked)"
    r"\b|\bwhere (?:did|have) we (?:get to|got to|left it|ended up)\b")

SUMMARY_WORD = re.compile(r"\b(?:summar\w+|sum up|recap|rundown)\b|\bsummary\b")

CHAT_WORD = re.compile(r"\b(?:chat|conversation|talk(?:ed|ing)?|we|us|it all)\b")

SUMMARY_ASK_FILLER = re.compile(
    r"\b(?:can|could|would|will|you|u|please|pls|give|me|us|a|an|the|quick|brief|short|just|"
    r"and|so|then|again|now|ok|okay|of|it|all|that|this|our|your|chat|conversation|talk|we|"
    r"so far|today|everything|sum|up|for|to|on)\b")

def _summary_ask(low):
    line = str(low or "")
    if TALKED_ABOUT.search(line):
        return True
    if not SUMMARY_WORD.search(line):
        return False
    if CHAT_WORD.search(line):
        return True
    return not SUMMARY_ASK_FILLER.sub(" ", SUMMARY_WORD.sub(" ", line)).split()

THING_AGAIN = re.compile(
    r"^(?:and |so |but |also )?(?:what was|whats|what is|what's) the ([a-z]{3,})(?: again)?\??$")

WHICH_WAS = re.compile(
    r"^(?:and |so |but |also |oh |ok |okay )?which ([a-z][a-z' ]{2,24}?)\s*"
    r"(?:was it|is it|was that|did i say|did i tell you)\s*[?.!]*$")

ATTRIBUTE_SAID = re.compile(
    r"^(?:and |so |but |also |oh |ok |okay )?what (?:day|date|time|size|colour|color|number|"
    r"price|cost|amount|brand|make|model|year|month) (?:did i|have i) "
    r"(?:just )?(?:say|tell you|mention)\b")

NOT_A_THING_NAMED = frozenset(('one', 'thing', 'things', 'bit', 'bits', 'part', 'parts',
                              'point', 'way', 'kind', 'sort', 'time', 'other', 'else'))

def _an_attribute_they_gave(low):
    if not ATTRIBUTE_SAID.match(low or ""):
        return False
    after = re.search(r"\b(?:say|said|tell you|told you|mention|mentioned)\b(.*)$", low)
    return bool(after and content(after.group(1)))

ATTRIBUTE_KIND = re.compile(
    r"^(?:and |so |but |also |oh |ok |okay )?(?:what|which)\s+([a-z][a-z' ]{1,24}?)\s+"
    r"(?:did i|have i|was it i|is it i|was that i)\s+(?:just )?"
    r"(?:say|said|tell you|told you|mention|mentioned)\b")

NOT_A_KIND = frozenset(('i', 'you', 'it', 'that', 'this', 'the', 'a', 'an', 'my', 'your', 'we',
                        'they', 'he', 'she', 'was', 'is', 'much', 'many', 'long', 'often', 'else',
                        'other', 'time', 'thing', 'one', 'day', 'now', 'then', 'about'))

def _an_open_attribute_ask(low, memory):
    part = ATTRIBUTE_KIND.match(low or "")
    if not part:
        return ""
    kind = " ".join(part.group(1).split())
    if not kind or kind.split()[0] in NOT_A_KIND or len(kind.split()) > 3:
        return ""
    after = re.search(r"\b(?:say|said|tell you|told you|mention|mentioned)\b(.*)$", low)
    words = content(after.group(1)) if after else set()
    words = {word for word in (words or content(kind)) if len(word) > 2}
    if not words:
        return ""
    best, score = "", 0
    for turn in _every_line(memory):
        line = turn.get("user") or ""
        if not line or _asks(line):
            continue
        seen = _seen(line)
        found = sum(1 for word in words if _alike(word, seen))
        if found and found >= score:
            best, score = line, found
    return _recall_quote(best, memory) if best else ""

def _which_thing_was_it(low, memory):
    part = WHICH_WAS.match(low or "")
    if not part:
        return None
    thing = " ".join(part.group(1).split())
    if thing in NOT_A_THING_NAMED or not content(thing):
        return None
    if not _said_word(thing, memory):
        return None
    return thing

A_WHEN = re.compile(
    r"\b(?:all|most|some|any|each|every|next|last|this|that|another|half|plenty\s+of|lots\s+of|"
    r"a\s+(?:long|short|little|bit\s+of|lot\s+of)|the\s+whole|the\s+entire)\s+(?:the\s+)?time\b"
    r"|\b(?:at|in|on|before|after|by|of)\s+the\s+time\b"
    r"|\btime\s+(?:to|for)\b"
    r"|\b(?:all|most|some|any|each|every|the\s+whole|these|those)\s+"
    r"(?:day|days|night|nights|week|weeks|month|months|year|years|morning|evening|afternoon)\b"
    r"|\b(?:right|just)\s+now\b")


def _without_the_when(line):
    return A_WHEN.sub(" ", line)


A_CLOCK_ASK = re.compile(
    r"^(?:and |so |but |oh |right |ok |okay |hi |hello |sorry )*"
    r"(?:(?:whats|what's|what is|whats?) the time"
    r"|what\s+time\s+is\s+it"
    r"|(?:have|has|do|did)\s+(?:you|u)\s+(?:got|have|know)\s+the\s+time"
    r"|(?:got|know)\s+the\s+time)\b")


def _a_clock_ask(line):
    return bool(A_CLOCK_ASK.match(str(line or "").strip().lower()))


def _said_word(word, memory):
    mine = forms(word)
    for turn in recent(memory, 8):
        said = str(turn.get("user") or "")
        if not said.strip() or _asks(said):
            continue
        line = _without_the_when(said)
        if not line.strip():
            continue
        if any(mine & forms(seen) for seen in content(line)):
            return True
    return False

def _recall_in_progress(memory):
    if not isinstance(memory, dict):
        return False
    before = " ".join((last_user(memory) or "").lower().split())
    if before and (FIRST_ASK.search(before) or SAID_ASK.search(before)
                   or _repeat_ask(before, before)):
        return False
    if last_module(memory) == "memory_store":
        return True
    return bool(before) and _about_this_chat(before)

def _elided_ask(text, memory, low=""):
    if not isinstance(memory, dict):
        return "", False
    line = " ".join(str(low or text or "").lower().split()).strip(" .,!?;:-")
    if not line or set(line.split()) - ELIDED_WORDS:
        return "", False
    raw = " ".join(str(text or "").lower().split())
    if not (ELIDED_ASK.search(line) or ELIDED_ASK.search(raw)
            or (ELIDED_AGAIN.search(line) and "again" in raw)):
        return "", False
    turns = memory.get("turns") or []
    named = _named_slots(line)
    fits = named | {"name", "pets"} if {"name", "pets"} & named else named
    stated = _stated_slot(memory, turns)
    if stated and (not named or stated in fits):
        return stated, True
    stated = _stated_slot(memory, turns, back=2)
    if stated and (not named or stated in fits):
        return stated, True
    asked = memory.get("asked")
    if isinstance(asked, dict) and asked.get("slot"):
        try:
            asked_turn = int(asked.get("turn") or 0)
        except (TypeError, ValueError):
            asked_turn = None
        slot = str(asked["slot"])
        if asked_turn is not None and len(turns) - asked_turn <= 2 and (not named or slot in fits):
            return slot, False
    return "", False

def _named_slots(line):
    return {slot for slot, pattern in ELIDED_NAMES if pattern.search(str(line or ""))}

def _stated_slot(memory, turns, back=1):
    user_lines = [turn for turn in list(turns or []) if isinstance(turn, dict)]
    window = list(reversed(user_lines[-max(1, int(back)):]))
    for offset, turn in enumerate(window):
        said = turn.get("user") or turn.get("text") or ""
        if not isinstance(said, str) or not said.strip():
            continue
        if offset == 0 and int(back) > 1 and not _asks(said):
            return ""
        found = extract.extract(said, question=False)
        kinds = [slot for key, slot in (
            ("name", "name"), ("city", "city"), ("age", "age"),
            ("budget", "budget"), ("allergies", "allergy"), ("pets", "pets")) if found.get(key)]
        if len(kinds) > 1:
            return ""
        if kinds:
            return kinds[0]
    return ""

def _remember_asked(memory, slot):
    if not isinstance(memory, dict) or not slot:
        return
    memory["asked"] = {"slot": slot, "turn": len(memory.get("turns") or [])}

def _the_case_they_just_gave(text, memory):
    clean = " ".join(str(text or "").split())
    if not clean or "?" in clean:
        return None
    if _asks(clean):
        return None
    if last_module(memory) not in ADVICE_MODULES:
        return None
    said = str(last_bot(memory) or "").strip()
    if not said:
        return None
    consequence = condition.chosen(clean, said)
    if not consequence:
        if not condition.refused(clean, said):
            return None
        gave = ack.said_back(clean, memory).strip(" .")
        return gave[:1].upper() + gave[1:] + "." if gave else None
    case = ack.said_back(clean, memory)
    if not case:
        return None
    body = consequence.strip(" ,;:-\u2014.")
    if not body:
        return None
    body = body[0].upper() + body[1:]
    line = "%s. %s, then." % (case.strip(" .").capitalize(), body)
    if _same_as_last(line, memory):
        return None
    return line

COUNT_IN_AN_ANSWER = re.compile(
    r"\b(?:one|two|three|four|five|six|seven|eight|nine|ten|both|couple|pair)\b", re.I)

def _said_another_way(reply):
    text = str(reply or "").strip()
    match = re.match(r"^(?:Your|My) (name|job|budget) is (.+)$", text)
    if match:
        slot, value = match.group(1), match.group(2).rstrip(".")
        if slot == "budget":
            return "You said " + value + "."
        if slot == "name":
            return "I have you as " + value + "."
        if slot == "job":
            return "You told me it is " + value + "."
    match = re.match(r"^You told me you(?:'re| are) (.+)$", text)
    if match:
        return "You said you're " + match.group(1).rstrip(".") + "."
    match = re.match(r"^You've got (.+)$", text)
    if match:
        animals = match.group(1).rstrip(".")
        if animals.count("called") > 1:
            return None
        named = re.search(r"\bcalled (.+)$", animals)
        if named:
            return "Still called " + named.group(1) + "."
        if not COUNT_IN_AN_ANSWER.search(animals):
            return None
        return "Still " + animals + "."
    match = re.match(r"^You (?:live|'re|are)(?: in| from)? (.+)$", text)
    if match:
        return "You said " + match.group(1).rstrip(".") + "."
    return None

def _slot_words(slot, memory=None):
    if slot == "pets" and isinstance(memory, dict):
        pets = [p for p in (user(memory).get("pets") or []) if isinstance(p, dict)]
        animals = [str(p.get("animal") or "") for p in pets]
        if animals and animals.count(animals[-1]) == 1:
            return "what is my " + animals[-1] + " called"
    return {
        "name": "what is my name",
        "age": "how old am i",
        "job": "what is my job",
        "city": "which city do i live in",
        "budget": "what is my budget",
        "allergy": "what am i allergic to",
        "pets": "what are my pets called",
    }.get(slot, "what have i told you")

def _slot_of(low):
    for slot, pattern in (
            ("allergy", r"\ballerg"),
            ("car", r"\bwhat (?:do|did) i drive\b|\bcar\b"),
            ("budget", r"\bbudget"),
            ("pets", r"\b(?:dog|cat|pet)s?\b"),
            ("job", r"\bmy (?:job|work)\b|\bwhat do i do\b|\bwhere do i work\b"),
            ("city", r"\b(?:city|place|country)\b|\bwhere do i (?:live|come from)\b"),
            ("name", r"\bmy name\b|\bwho am i\b")):
        if re.search(pattern, low):
            return slot
    return ""

BARE_MINE = re.compile(
    r"^(?:and |so |ok |okay |but |well |also |what about |how about |again )*"
    r"(?:my|our)\s+([a-z][a-z' -]{0,24}?)$")

SLOT_NOUNS = {
    "name": frozenset("name".split()),
    "job": frozenset("job work".split()),
    "city": frozenset("city place town".split()),
    "budget": frozenset("budget".split()),
    "allergy": frozenset("allergy allergies allergen".split()),
    "pets": frozenset("pet pets dog dogs cat cats animal animals".split()),
    "age": frozenset("age".split()),
}

SLOT_FILLER = frozenset("""again now then please too as before though tho also still anyway
i told you said say remember""".split())

def _slot_named_in(low):
    for slot, pattern in BARE_SLOTS:
        if re.search(pattern, str(low or "")):
            return slot
    return ""

def _slot_held(slot, memory):
    keys = SLOT_KEY.get(slot)
    if not keys:
        return False
    known = user(memory) or {}
    return any(known.get(key) for key in keys)

def _bare_ask_naming_a_fact(low, memory):
    found = BARE_MINE.match(str(low or "").strip(" .!?;,"))
    if not found:
        return ""
    words = set(found.group(1).split())
    slot = _slot_named_in("my " + found.group(1))
    if not slot or not _slot_held(slot, memory):
        return ""
    if words - SLOT_NOUNS.get(slot, frozenset()) - SLOT_FILLER:
        return ""
    if slot == "pets":
        named = words - SLOT_FILLER - {"pet", "pets", "animal", "animals"}
        held = set()
        for pet in (user(memory) or {}).get("pets") or []:
            if isinstance(pet, dict):
                held |= forms(str(pet.get("animal") or ""))
        if named and not any(forms(one) & held for one in named):
            return ""
    return slot

PLACES_ASK = re.compile(
    r"\b(?:which|what) (?:city|place|country|town)\b"
    r"|\b(?:which|what) (?:area|suburb|neighbourhood|neighborhood|county|village|"
    r"part of (?:the|this) country) (?:of (?:the|this) (?:country|city|town) )?"
    r"(?:do|does|did|am|was|are|were) (?:i|we)\b"
    r"|\b" + WHERE_ASK + r" (?:am|was) i (?:going|from|living)\b(?! with\b)|"
    r"\bmy hometown\b|\b" + WHERE_ASK + r" am i from originally\b|"
    r"\b" + WHERE_ASK + r" (?:was|were) (?:i|we) born\b|\b" + WHERE_ASK + r" are (?:i|we) from\b|"
    r"\b" + WHERE_ASK + r" do (?:i|we) (?:live|come from)\b|\b" + WHERE_ASK + r" are we "
    r"(?:living|based)\b|"
    r"\b" + WHERE_ASK + r" (?:do|does) my \w+ (?:live|come from)\b|"
    r"\b" + WHERE_ASK + r" is my \w+ (?:living|based)\b|"
    r"\bwhere (?:did|do|does) (?:i|we) (?:grow|grew|grown) up\b|"
    r"\bwhere (?:was|were) (?:i|we) (?:raised|brought up|brung up)\b|"
    r"\bwhere did (?:i|we) (?:live|grow up) (?:before|originally|as a kid|as a child|growing up)\b|"
    r"\bwhere (?:did|do|does) (?:i|we) (?:move|moved) (?:here |over |away )?from\b|"
    r"\b(?:which|what) (?:city|town|place|county|country) did (?:i|we) move (?:from|away from)\b")

SELF_WORD = re.compile(r"\b(?:i|i'm|im|i've|ive|i'd|id|me|my|mine|we|we're|us|our|ours)\b")

PLACE_ADVICE = re.compile(
    r"\b(?:should|shall|recommend\w*|worth|visit\w*)\b"
    r"|\bbest (?:place|city|country|town|part)\b")

PLACE_RECALLED = re.compile(
    r"\b(?:did i (?:say|tell|mention)|i (?:said|mentioned|told)|remember|again)\b")

GROWN_UP_ASK = re.compile(
    r"\b(?:grow|grew|grown) up\b|\b(?:raised|brought up|brung up)\b"
    r"|\bwhere (?:i|we) (?:lived|was living|were living)\b")

FEELING_ALONE = re.compile(
    r"^(?:and |but |so |also |honestly |yeah |yes |god |oh |well |still |im |i'm |i am |i feel"
    r"|i just feel |feel |im just |im getting |getting |a bit |really |very |quite |so )*"
    r"(scared|nervous|worried|anxious|terrified|petrified|frightened|panicking|dreading|dreading it)"
    r"(?: (?:about it|of it|about that|about this|about the whole thing|now|today|already"
    r"|honestly|a lot|so much|quite a lot|tbh|tbf|again|about it now"
    r"|for (?:him|her|them|it|us|you)))?$", re.I)

COMING_UP = re.compile(
    r"\b(?:tomorrow|tonight|later today|this (?:morning|afternoon|evening|week|weekend|month)"
    r"|next (?:week|month|year|monday|tuesday|wednesday|thursday|friday|saturday|sunday|weekend)"
    r"|on (?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)"
    r"|at the weekend|in (?:january|february|march|april|may|june|july|august|september|october"
    r"|november|december)|soon|in a (?:few|couple of) (?:days|weeks))\b", re.I)

A_DAY = re.compile(
    r"\b(?:tomorrow|tonight|later today|this (?:morning|afternoon|evening|weekend)"
    r"|next (?:week|monday|tuesday|wednesday|thursday|friday|saturday|sunday|weekend)"
    r"|on (?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)|at the weekend)\b", re.I)

def _is_a_question(previous):
    if previous.rstrip().endswith("?"):
        return True
    try:
        return understand(previous).get("kind") == "question"
    except Exception:
        return True

TREATMENT = re.compile(
    r"\b(?:chemo|chemotherapy|radiotherapy|radiation therapy|dialysis|biopsy|palliative|hospice"
    r"|terminally ill)\b", re.I)

A_PERSON_IN_TROUBLE = re.compile(
    r"\b(?:my|our)\s+(?:" + KIN + r")\b(?:'s|s)?[^.?!]*?\b(?:" + BAD_NEWS + r")\b", re.I)

WHO_IS_IN_TROUBLE = re.compile(r"\b(?:my|our)\s+((?:" + KIN + r"))\b", re.I)

SHE = frozenset("""mum mom mother daughter wife sister gran granny nan nana grandma grandmother
                   aunt niece stepdaughter""".split())

HE = frozenset("""dad father son husband brother grandad grandpa grandfather uncle nephew
                  stepson""".split())

def _again(who):
    word = str(who or "").lower()
    if word in SHE:
        return "her"
    if word in HE:
        return "him"
    return "them"

def _the_thing_before_the_feelings(memory):
    seen = 0
    for turn in reversed((memory.get("turns") or [])[-6:]):
        if not isinstance(turn, dict):
            break
        line = str(turn.get("user") or "").strip()
        if not line:
            continue
        if FEELING_ALONE.match(line.lower().rstrip("!.,")):
            continue
        seen += 1
        if seen > 1:
            break
        return line
    return ""

def _a_feeling_about_what_they_said(memory, low):
    match = FEELING_ALONE.match(str(low or "").strip().rstrip("!.,"))
    if not match:
        return None
    previous = _the_thing_before_the_feelings(memory)
    if not previous or len(previous.split()) < 4:
        return None
    if _is_a_question(previous):
        return None
    if TREATMENT.search(previous):
        return None
    if not re.search(r"\b(?:i|we|my|our|me)\b|\bim\b|\bive\b", previous.lower()):
        return None
    trouble = A_PERSON_IN_TROUBLE.search(previous)
    if not (COMING_UP.search(previous) or trouble):
        return None
    if trouble:
        who = WHO_IS_IN_TROUBLE.search(previous)
        if who:
            recent = " ".join(str(t.get("bot") or "") for t in (memory.get("turns") or [])[-5:]
                              if isinstance(t, dict))
            said_for = re.search(r"\b(?:for|about)\s+(him|her|them)\b", str(low or ""), re.I)
            again = _again(who.group(1))
            if said_for:
                theirs = said_for.group(1).lower()
                if again == "them" or theirs == again:
                    again = theirs
            said_bodies = [body.format(who="your " + who.group(1).lower(), again=again)
                           for body in (
                "That is a lot to be carrying, and being frightened for {who} does not make you "
                "any less help to {again}.",
                "It is all right to be frightened for {who}. You do not have to be the calm one "
                "all the time.",
                "Scared for {who} is one of the heaviest things to carry, and you are allowed to "
                "say so.",
                "Being frightened for {who} is the honest reaction, and saying it out loud once "
                "usually takes some of the weight off.",
            )]
            fresh = [body for body in said_bodies if body not in recent] or said_bodies
            seed = len(memory.get("turns") or []) + sum(map(ord, who.group(1)))
            return random.Random(seed).choice(fresh)
    said = thread.restate(previous)
    if not said or len(said.split()) < 3:
        return None
    said = said[0].upper() + said[1:]
    feeling = match.group(1).lower()
    if feeling in ("worried", "anxious"):
        bodies = ["That is a fair thing to have on your mind, and most of it is the not-knowing.",
                  "Worrying about it makes sense. Is there one thing you could check that would "
                  "settle it?",
                  "That kind of worry is tiring to carry, and saying the worst version out loud "
                  "usually shrinks it.",
                  "Worry about something coming up is the mind rehearsing it. Is there one thing "
                  "you could check that would settle it?"]
    elif A_DAY.search(previous):
        bodies = ["Nerves before something like that are normal, and it is usually worse in the "
                  "days before than on the day.",
                  "Of course you are - most of it is the not-knowing. What is the first thing that "
                  "happens?",
                  "That is a fair thing to be nervous about. Tell me the part of it that keeps "
                  "coming back.",
                  "That is a nervous-making thing to have coming, and it says nothing bad about "
                  "how ready you are.",
                  "Nerves are usually worse in the days before than on the day. What is the first "
                  "thing that happens?"]
    else:
        bodies = ["That is a fair thing to be nervous about, and it is all right to say so.",
                  "Nerves about it make sense, and naming the worst version out loud usually "
                  "shrinks it.",
                  "That is a lot to be carrying around. Is there one part of it you could start "
                  "on?",
                  "Saying the thing you dread out loud is usually the worst part of it, and the "
                  "rest is smaller than it looks.",
                  "Most of the nerves is the not-knowing. What is the part that keeps coming "
                  "back?"]
    recent = " ".join(str(t.get("bot") or "") for t in (memory.get("turns") or [])[-5:]
                      if isinstance(t, dict))
    body = _vary([b for b in bodies if b[:40] not in recent] or bodies, memory)
    if any(_said_back_already(str(turn.get("bot") or ""), said)
           for turn in (memory.get("turns") or [])[-2:] if isinstance(turn, dict)):
        standing = [b for b in bodies if not OPENS_ON_THE_SENTENCE.match(b)]
        return _vary([b for b in standing if b[:40] not in recent] or standing or bodies, memory)
    return said + ". " + body

OPENS_ON_THE_SENTENCE = re.compile(
    r"^(?:of course|of course you are|that\b|this\b|those\b|these\b|such\b"
    r"|(?:nerves|worry|worrying|fear|stress|panic) about it\b)", re.I)

def _said_back_already(reply, said):
    words = {w for w in keywords(said) if len(w) > 3}
    if not words:
        return False
    return len(words & {w for w in keywords(reply) if len(w) > 3}) >= max(2, len(words) - 1)

ANSWER_MODULES = frozenset(("answers", "memory_store"))

def _the_bot_name(memory, low):
    known = str(user(memory).get("bot_name") or "").strip()
    if not known or not extract.BOT_NAME_ASK.search(low):
        return None
    return pick(["You call me " + known + ".", known + " \u2014 you named me that.",
                 "I'm " + known + ", since you named me."], memory)

def _the_store_reply(text, memory):
    if asks_what_today_is(text):
        return None
    behind = _behind_a_remembering_frame(text)
    if behind:
        remembered = _remembers_fact(text, memory)
        if remembered:
            return remembered
        answered = _the_store_reply(behind, memory)
        if answered:
            return answered
    followed = _the_followed_check(text, memory)
    if followed:
        return followed
    closed = _the_close(text, memory)
    if closed:
        return closed
    shared = _the_limit_they_share(text, memory)
    if shared:
        return shared
    how_it_went = thread.went(text, memory)
    if how_it_went:
        return how_it_went
    timed = _the_time_they_said(text, memory)
    if timed:
        return timed
    took = memory.pop("pet_age", None) if isinstance(memory, dict) else None
    if isinstance(took, dict) and isinstance(took.get("age"), int):
        return "Noted: " + _pet_named(took) + " is " + _a_pet_age(took) + "."
    call = _the_call_from_the_advice(text, memory)
    if call:
        return call
    given = extract.bot_name(text)
    if given:
        return pick([given + " it is \u2014 I'll answer to that.",
                     given + " \u2014 noted, I'll answer to it.",
                     "I'll be " + given + " then."], memory)
    settled = choose.the_decision(text, memory)
    if settled:
        return settled
    budget = _the_budget_on_the_answer(text, memory)
    if budget:
        return budget
    made = _the_amount_they_made(text, memory)
    if made:
        return made
    fed = _the_people_that_size_feeds(text, memory)
    if fed:
        return fed
    sized = _the_figure_for_the_size_they_named(text, memory)
    if sized:
        return sized
    folded = _folded(text, memory)
    low = _bare(folded)
    undeclared = _the_person_still_in_hand(low, memory)
    if undeclared:
        one_more = _other_person_reply(memory, low)
        if one_more:
            return one_more
    named_back = _the_bot_name(memory, low)
    if named_back:
        return named_back
    names = _the_names_again(folded, low, memory)
    if names:
        return names
    counted = how_many.answer(low, memory)
    if counted:
        return counted
    same = _the_same_fact_about_someone(text, memory)
    if same:
        said, note = same
        if note:
            remember_other(memory, dict(note))
        return said
    about_it = _a_feeling_about_what_they_said(memory, low)
    if about_it:
        return about_it
    kept = _the_fact_just_asked(memory, low)
    if kept:
        return kept
    slot, guessed = _elided_ask(text, memory, low)
    if slot:
        reply = _respond(_slot_words(slot, memory), memory)
        if not reply or (guessed and ELIDED_NOT_SURE.search(reply)):
            reply = _respond(text, memory)
            if reply:
                _remember_asked(memory, _slot_of(low))
            return reply
        if _same_as_last(reply, memory):
            return _said_another_way(reply) or reply
        return reply
    taken = _the_case_they_just_gave(text, memory)
    if taken:
        return taken
    named = _bare_ask_naming_a_fact(low, memory)
    if named:
        reply = _respond(_slot_words(named, memory), memory)
        if reply and not ELIDED_NOT_SURE.search(reply):
            _remember_asked(memory, named)
            if _same_as_last(reply, memory):
                return _said_another_way(reply) or reply
            return reply
    part_asked = a_hurting_part.the_part_asked(memory, low)
    if part_asked:
        return part_asked
    reply = _respond(text, memory)
    if not reply:
        reply = a_repair.the_thing_they_meant(text, memory)
    if not reply:
        reply = about_the_choice.the_subject_in_the_condition(text, memory)
    if not reply:
        reply = about_the_choice.the_verdict_in_the_chat(text, memory)
    if not reply:
        reply = about_the_choice.the_quality_in_the_chat(text, memory)
    if not reply:
        reply = about_the_choice.the_limit_in_the_chat(text, memory)
    if reply:
        _remember_asked(memory, _slot_of(low))
        if _same_as_last(reply, memory):
            return _said_another_way(reply) or reply
    if not reply:
        reply = _pet_part_reply(memory, low)
    if not reply:
        reply = a_hurting_part.the_part_asked(memory, low)
    if not reply:
        reply = rates_reader.answer(text, memory)
    if not reply:
        reply = _detail_they_left_out(memory, low)
    if not reply:
        reply = a_reason.answer_for(text, memory)
    if not reply:
        reply = _the_part_it_never_said(memory, low)
    return reply

DETAIL_ASKS = (
    (re.compile(r"\bhow much\b|\bwhat did (?:it|that|it all|they) cost\b"
                r"|\bwhat(?:'s|s| is| was)? (?:the |was the )?(?:pay|price|salary)\b"), "money"),
    (re.compile(r"\bhow long (?:did|was)\b|\bhow long did (?:it|that|they)\b"),
     "time"),
    (re.compile(r"\bhow many\b|\bhow often\b"), "count"),
    (re.compile(r"\bwhere (?:is|are|was|were|did)\b|\bwhich (?:hotel|flight|one)\b"), "place"),
    (re.compile(r"\bwhat time\b|\bwhen (?:is|are|was|were|do|did)\b"), "when"),
    (re.compile(r"\bwhich (?:area|part|place|school|club|team|course|country|city|kind|sort|type"
                r"|one|ones)\b|\bwhat (?:kind|sort|type) of\b"), "which"),
    (re.compile(r"\bwhat (?:was|is|were) (?:it|they|that|he|she) called\b"
                r"|\bwhat(?:'s|s| is) (?:it|he|she|they) called\b|\bwhat was (?:the )?name\b"),
     "called"),
    (re.compile(r"\bhow (?:far|old|big|tall|heavy|long ago)\b"), "measure"),
    (re.compile(r"\bwhat (?:was|is|were) (?:it|that|they|he|she) (?:about|like)\b"
                r"|\bwhat(?:'s|s) it (?:about|like)\b"), "about"),
)

DETAIL_LEAN = re.compile(r"\b(?:it|that|this|they|them|those|we|you|your|he|she|him|her)\b", re.I)

BARE_MEASURE = re.compile(r"\bhow (?:much|many|long|old)\b", re.I)

MONEY_SAID = re.compile(r"£\s?\d|\b\d[\d,.]*\s*(?:pounds?|quid|euros?|dollars?)\b", re.I)

LOOK_BACK_ANSWER = 3


def _the_answer_already_gives(detail, memory):
    if detail != "money":
        return False
    said = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    for turn in reversed(said[-LOOK_BACK_ANSWER:]):
        if turn.get("module") not in ANSWER_MODULES:
            continue
        reply = " ".join(str(turn.get("bot") or "").split())
        if not reply or reply.rstrip().endswith("?"):
            continue
        return bool(MONEY_SAID.search(reply))
    return False

ASK_OPENER = re.compile(
    r"\A(?:how|what|whats|when|where|which|why|who|whose|is|are|was|were|can|could|should"
    r"|shall|do|does|did|will|would|have|has|am|may|might|any|whose)\b", re.I)

HOW_LONG_IT_TAKES = re.compile(
    r"\bhow long (?:does|do|will|would|is|are|should|can|could)\b[^?]{0,25}?\b(?:take|takes|taking)\b",
    re.I)

WANTING = re.compile(r"\b(?:want|wants|wanting|need|needs|needed|hoping|hope to|planning"
                     r"|plan to|trying to|thinking of|thinking about|would like|i'd like"
                     r"|looking to|saving up|saving for)\b", re.I)

DETAIL_VERBS = frozenset("""
it that this they them those we you your he she him her is are was were did do does
have has had be been cost costs pay paid take taken took last lasted stay staying
go going went get got buy bought end give given much long many where when what time
whats salary price a an the and but so to for in on at of from with about then again
there here
""".split())

DETAIL_KNOWN = {
    "money": re.compile(r"£|\d|\bpounds?\b|\bdollars?\b|\beuros?\b|\bquid\b", re.I),
    "time": re.compile(r"\d+\s*(?:minutes?|mins?|hours?|hrs?|days?|weeks?|months?)"
                       r"|\b(?:" + COUNT_WORD + r")\s+(?:minutes?|mins?|hours?|hrs?|days?"
                       r"|weeks?|months?|years?)|\ban hour\b", re.I),
    "count": re.compile(r"\b\d+\b|\b" + COUNT_WORD + r"\b", re.I),
    "when": re.compile(r"\b\d|\b(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday|january"
                       r"|february|march|april|may|june|july|august|september|october|november"
                       r"|december|tomorrow|tonight|next week|next month|at \d)\b", re.I),
    "place": re.compile(r"\b(?:in|to|at) [A-Z]|\bhotel\b|\bstaying (?:in|at)\b"
                        r"|\b(?:in|to|at) (?!(?:" + PLACE_NOT + r")\b)[a-z]{3,}\b"),
    "which": re.compile(r"\b(?:in|to|at|near|around) \w+|\bcalled\b|\bnamed\b", re.I),
    "called": re.compile(r"\b(?:called|named)\b", re.I),
    "measure": re.compile(r"\b\d|\bmiles?\b|\bkilomet\w+\b|\bkm\b|\bmetres?\b|\bminutes?\b"
                          r"|\bhours?\b", re.I),
}

PLACE_NARROWER = re.compile(r"\b(?:staying|sleeping|eating|hotel|hostel|accommodation|campsite"
                            r"|airport|flight|parking|venue|school|office|shop)\b", re.I)

SHAPE_WORDS = frozenset("""
area part place area school club team course country city town kind sort type one ones called
named name about like
far many much often tall heavy big old long wide
""".split())

def _turned(question):
    words = str(question or "").rstrip(" ?!.").split()
    said = " ".join(TURNED.get(word.lower(), word) for word in words)
    for long_form, short in (("what is the", "what's the"), ("what is it", "what is it"),
                             ("it is", "it's"), ("you are", "you're"),
                             ("where is the", "where's the")):
        said = re.sub(r"\b" + long_form + r"\b", short, said)
    return said

def _a_choice_from_what_was_said(line, memory):
    try:
        from ..modules.answers import CHOICE_ASK, _the_one_to_pick
    except Exception:
        return False
    clean = " ".join(str(line or "").lower().split())
    if not CHOICE_ASK.match(clean):
        return False
    try:
        return bool(_the_one_to_pick(clean, memory))
    except Exception:
        return False

def _detail_they_left_out(memory, low):
    line = str(low or "").strip()
    if not line or len(line.split()) > 9:
        return None
    if _a_clock_ask(line) and not a_when.EVENT_WORD.search(str(last_user(memory) or "")):
        return None
    if _about_the_bot_here(memory):
        return None
    if _a_choice_from_what_was_said(line, memory):
        return None
    if not re.search(r"\b(?:how|whats?|where|when|which|whos?)\b", line):
        return None
    detail = None
    for pattern, kind in DETAIL_ASKS:
        if pattern.search(line):
            detail = kind
            break
    if detail is None:
        return None
    spare = [word for word in re.findall(r"[a-z']+", line)
             if word not in DETAIL_VERBS and word not in SHAPE_WORDS
             and word not in ("how", "what", "where", "when", "which", "why", "s")]
    if spare:
        return None
    if not DETAIL_LEAN.search(line) and not re.search(r"\bthe (?:pay|price|salary)\b", line):
        if detail in ("money", "count", "time") or BARE_MEASURE.search(line):
            return None
    try:
        from ..memory import named as _named
        if _named.a_faulty_thing(memory):
            return None
    except Exception:
        pass
    previous = str(last_user(memory) or "").strip()
    if not previous or previous.endswith("?") or len(previous.split()) < 3:
        return None
    if ASK_OPENER.match(previous.lower()):
        return None
    if not re.search(r"\b(?:i|we|my|our|me)\b|\bive\b|\bim\b", previous.lower()):
        return None
    if WANTING.search(previous.lower()):
        return None
    known = DETAIL_KNOWN.get(detail)
    narrower = detail == "place" and PLACE_NARROWER.search(line)
    if known is not None and not narrower and known.search(previous):
        return None
    if detail == "time" and HOW_LONG_IT_TAKES.search(line):
        return None
    if _the_answer_already_gives(detail, memory):
        return None
    if detail == "money" and re.search(r"\bcost\b", line):
        return "You didn't say what it cost - how much was it?"
    ask = _turned(line)
    if not ask:
        return None
    return "You haven't said - " + ask + "?"

PART_ASK = re.compile(
    r"\b(?:what|which|who|where|when)\b[^?.!]{0,40}?\b(?:do|does|did|is|are|was|were|can)\b"
    r"|\bhow (?:much|many|old|long|big|far|often|tall|heavy)\b", re.I)

PART_MINE = re.compile(r"\b(?:my|our)\s+([a-z']+)", re.I)

PART_POINTS = re.compile(r"\b(?:it|its|he|she|they|them|their|there|his|her)\b", re.I)

RECORD_PART = re.compile(
    r"\b(?:earn|earns|earning|paid|pay|wage|wages|salary|hours|shifts?|boss|manager"
    r"|colleagues?|coworkers?|uniform|(?:do|doing|did) there|work with|working with|works with|work for"
    r"|school|nursery|childminder|called|names?|named|model|make|year|colour|color|reg"
    r"|brand|mileage|breed)\b", re.I)

PART_ADVICE = re.compile(r"\b(?:should|shall|recommend|suggest|best|better|worth|instead|advice"
                         r"|ideas?|how do i|how can i|can i|could i|would you)\b", re.I)

PART_HELP = re.compile(r"\b(?:what|how) (?:do|can|should|could|would) i do (?:about|with|for|to|next"
                       r"|now|then)\b", re.I)

PART_OF = (
    ("job", re.compile(r"\b(?:earn|earns|earning|paid|wages?|salary|shifts?|boss"
                       r"|colleagues?|coworkers?|uniform)\b")),
    ("city", re.compile(r"\b(?:live|lives|moved|grew up)\b")),
    ("pets", re.compile(r"\b(?:dogs?|cats?|pets?|puppy|kitten|rabbit|hamster)\b")),
    ("people", re.compile(r"\b(?:son|daughter|mum|dad|mother|father|sister|brother"
                          r"|partner|wife|husband|kids?|children)\b")),
    ("owns", re.compile(r"\b(?:car|bike|laptop|phone|van)\b")),
)

JOB_PART = re.compile(
    r"\b(?:do|doing|did|work|working|works) there\b"
    r"|\bwho (?:do|does|did) (?:i|we) (?:\w+ )?(?:with|for)\b"
    r"|\b(?:what|which) (?:are )?(?:the )?(?:hours|shifts?|pay|uniform)\b"
    r"|\bhow (?:much|many|long) (?:do|does|did) (?:i|we)\b", re.I)

def _a_held_part(memory, line):
    known = user(memory)
    for key, pattern in PART_OF:
        if pattern.search(line) and known.get(key):
            return True
    return False

def _a_part_of_the_job_never_said(memory, low):
    line = str(low or "").strip()
    if not line or len(line.split()) > 8:
        return None
    if not (user(memory) or {}).get("job"):
        return None
    if PART_ADVICE.search(line) or PART_HELP.search(line) or re.search(r"\d", line):
        return None
    if not JOB_PART.search(line):
        return None
    ask = _turned(line)
    if not ask:
        return None
    return "You haven't said - " + ask + "?"

def _holds_nothing(known):
    return not any(known.get(key) for key in PART_KEYS)

def _a_thing_it_keeps(memory, mine):
    known = user(memory)
    if _holds_nothing(known):
        return None
    key = PART_HELD.get(str(mine or "").lower())
    if key is None:
        return None
    if key == "people":
        return key if (known.get("people") or known.get("others")
                       or known.get("kids")) else None
    if key == "city":
        return key if (known.get("city") or known.get("home")
                       or known.get("places")) else None
    return key if known.get(key) else None

def _the_part_it_never_said(memory, low):
    line = str(low or "").strip()
    if not line or len(line.split()) > 8:
        return None
    if PART_ADVICE.search(line) or PART_HELP.search(line) or re.search(r"\d", line):
        return None
    if not PART_ASK.search(line) or not RECORD_PART.search(line):
        return None
    mine = PART_MINE.search(line)
    if mine:
        if not _a_thing_it_keeps(memory, mine.group(1)):
            return None
    elif not (PART_POINTS.search(line)
              or (re.search(r"\b(?:i|im)\b", line) and _a_held_part(memory, line))):
        return None
    if not _a_kept_thing_behind(memory):
        return None
    ask = _turned(line)
    if not ask:
        return None
    return "You haven't said - " + ask + "?"

def _a_kept_thing_behind(memory):
    from bot.memory import facts as kept

    for turn in reversed(recent(memory, 5)):
        said = str(turn.get("user") or "").strip()
        if not said or said.endswith("?"):
            continue
        if not re.search(r"\b(?:i|we|my|our|im|ive)\b", said.lower()):
            continue
        try:
            found = kept.extract(said)
        except Exception:
            return False
        if not isinstance(found, dict):
            return False
        if any(found.get(key) for key in KEPT_THINGS):
            return True
    return False

DRINK_DIET = frozenset("""alcohol booze wine wines beer beers lager lagers cider spirits gin
vodka whisky whiskey rum prosecco champagne cocktails cocktail sherry brandy""".split())

def _diet_how(diet):
    words = set(re.split(r"[ ,]+", str(diet or "")[3:].strip().lower()))
    return "drink" if words & DRINK_DIET else "eat"

REMEMBER_IT = re.compile(
    r"^(?:and |so |ok |okay |but |well )*(?:do |did )?you (?:still )?(?:remember|recall)"
    r"(?: (?:it|that|this|that one))?(?: (?:yes or no|or not|right|then))?$"
    r"|^(?:do|did) you (?:still )?(?:remember|recall) (?:it|that|this)$")

def _the_fact_just_asked(memory, low):
    if not isinstance(memory, dict) or not REMEMBER_IT.match(str(low or "").strip()):
        return None
    asked = memory.get("asked")
    if not isinstance(asked, dict) or not asked.get("slot"):
        return None
    turns = memory.get("turns") or []
    try:
        asked_turn = int(asked.get("turn") or 0)
    except (TypeError, ValueError):
        return None
    if not turns or len(turns) - asked_turn > 2:
        return None
    if last_module(memory) != "memory_store":
        return None
    reply = _respond(_slot_words(str(asked["slot"]), memory), memory)
    if not reply or ELIDED_NOT_SURE.search(reply):
        return None
    return _yes_then(reply)

def _yes_then(reply):
    text = str(reply or "").strip()
    if re.match(r"^(?:You|Your|It)\b", text):
        text = text[:1].lower() + text[1:]
    return "Yes \u2014 " + text

CONFIRM_FRAMES = (
    (re.compile(r"^(?:am|was) i\s+(?:not\s+)?(.+)$"), "i am "),
    (re.compile(r"^(?:do) i\s+(?:still\s+|really\s+|actually\s+)?(.+)$"), "i "),
    (re.compile(r"^(?:have) i\s+(?:got\s+|really\s+|actually\s+)?(.+)$"), "i have "),
)

YES_NO_ASK = re.compile(
    r"^\W*(?:is|are|was|were|does|did|do|can|could|has|have|had|will|would|should|may|might)\s+"
    r"(?:she|he|they|his|her|their|my|your)\b", re.I)

YES_NO_FRAME = re.compile(
    r"^\W*(?:is|are|was|were|does|did|do|can|could|has|have|had|will|would|should|may|might)\s+"
    r"[^?.!;]*[?.!;]+\s*", re.I)

TELLING_AFTER_ASK = re.compile(
    r"\b(?:he|she|they|it|we|my\s+(?:" + _RELATION + r"))\s+"
    r"(?:is|are|was|were|doesnt|does not|dont|do not|cant|cannot|wont|will not|has|have|had"
    r"|likes?|loves?|eats?|drinks?|never|always|usually|only|really|prefers?|hates?)\b", re.I)

def _after_the_yes_no_frame(text):
    line = " ".join(str(text or "").split())
    match = YES_NO_FRAME.match(line)
    if match:
        return line[match.end():].strip()
    opened = YES_NO_ASK.match(line)
    if not opened:
        return ""
    after_who = line[opened.end():]
    telling = TELLING_AFTER_ASK.search(after_who)
    if not telling:
        return ""
    return after_who[telling.start():].strip()

def _statement(text):
    low = " ".join(text.lower().split()).strip(" ?!.")
    low = re.sub(r"^(?:sorry|hey|hi|ok|okay|so|but|and|well|quick one)[, ]+", "", low)
    for pattern, lead in CONFIRM_FRAMES:
        match = pattern.match(low)
        if match:
            return lead + match.group(1)
    match = re.match(r"^(?:is|was) my\s+(\S+)\s+(.+)$", low)
    if match and (re.match(r"^(?:called |named )?\S+$", match.group(2))
                  or match.group(2).startswith("called ")):
        return "my " + match.group(1) + " is " + match.group(2)
    return None

def _same(left, right):
    return " ".join(str(left).lower().split()) == " ".join(str(right).lower().split())

def _clause(key, value, known=None):
    if key == "name":
        return "you're " + str(value)
    if key == "age":
        return "you're " + str(value)
    if key == "job":
        known = known if isinstance(known, dict) else {}
        frame = str(known.get("job_frame") or "").strip()
        if frame and _same(value, known.get("job")):
            said = _job_said({"job": str(value), "job_frame": frame})
            return said[:1].lower() + said[1:]
        return "you're " + _a(str(value))
    if key == "city":
        return "you live in " + str(value)
    if key == "car":
        return "you drive " + str(value)
    if key == "from":
        return "you're from " + str(value)
    if key == "allergies":
        return "you're allergic to " + ", ".join(value)
    if key == "budget":
        return "your budget is " + str(value)
    if key == "diet":
        diet = str(value)
        return ("you don't " + _diet_how(diet) + " " + diet[3:] if diet.startswith("no ")
                else "you're " + diet)
    if key == "pets":
        pets = value if isinstance(value, list) else [value]
        parts = [_a_pet(p) for p in pets]
        return "you've got " + " and ".join(parts)
    return ""

def _their_allergy(who, theirs):
    return ("You haven't told me one \u2014 the allergy to " + ", ".join(theirs)
            + " is your " + who + "'s, not yours.")

DIET_ANY = re.compile(r"^(?:on\s+)?(?:a\s+)?diet(?:ing)?$", re.I)

def _said_matches(key, said, known):
    if key == "name":
        return _same(said, known) if known else False
    if key == "age":
        return known is not None and str(said) == str(known)
    if key == "diet" and DIET_ANY.match(str(said).strip()):
        return None
    if key in ("job", "city", "from", "diet"):
        return _same(said, known) if known else False
    if key == "budget":
        mine = re.sub(r"[^0-9]", "", str(said))
        theirs = re.sub(r"[^0-9]", "", str(known or ""))
        return bool(mine) and mine == theirs
    if key == "allergies":
        stored = {str(a).lower() for a in (known or [])}
        return bool(said) and all(str(a).lower() in stored for a in said)
    if key == "pets":
        for pet in known or []:
            if _animal_family(pet.get("animal")) != _animal_family(said.get("animal")):
                continue
            if not said.get("name") or _same(pet.get("name"), said.get("name")):
                return True
        return False
    return None

def _names(key, text):
    pattern = NAMED_BY.get(key)
    return bool(pattern) and bool(re.search(pattern, text))

DUTY_ASK = re.compile(
    r"\b(?:need|needs|needed|have|has|had) to\b|\bshould\b|\bshouldn't\b|\bmust\b|"
    r"\bgot time\b|\bworth\b|\bhow (?:often|much|long)\b|\bbetter\b")

REMEMBERING_FRAME = re.compile(
    r"^(?:(?:and|but|so|ok|okay|right|well|oh|ah|quick one|sorry|hi|hiya|hey|hello|just|also)"
    r"[\s,]+)*"
    r"(?:"
    r"(?:(?P<aux>do|did|does|can|could|would|will|have|has)\s+)?(?:you|u)\s+"
    r"(?:still\s+|even\s+)?(?P<verb>remember|recall|know|remembered|noticed)"
    r"|(?P<bare>remember|recall)\b"
    r")"
    r"(?:\s+(?:that|this|it|me|about that|about it|all that))?", re.I)

RESTATED = re.compile(r"^(?:i|im|i'm|ive|i've|id|i'd|ill|i'll|my|we|we're|weve|we've|our)"
                      r"\b", re.I)

CONFIRM_TAG = re.compile(r"[\s,]+(?:right|tho|though|yes|yeah|yep|ok|okay|lol|ha|haha|innit|"
                         r"correct)\s*$", re.I)

def _restated(text, typed=None):
    low = " ".join(str(text or "").lower().split()).strip()
    tagged = bool(CONFIRM_TAG.search(low))
    low = CONFIRM_TAG.sub("", low).strip(" ?!.,")
    frame = REMEMBERING_FRAME.match(low)
    if not frame:
        return None
    question = "?" in str(text if typed is None else typed)
    asking = (question or tagged or frame.group("aux") or frame.group("bare")
              or (frame.group("verb") or "").startswith(("remember", "recall")))
    if not asking:
        return None
    rest = low[frame.end():].strip(" ?!.,")
    if not rest or not RESTATED.match(rest):
        return None
    return rest

def _behind_a_remembering_frame(text):
    low = " ".join(str(text or "").lower().split()).strip(" ?!.,")
    frame = REMEMBERING_FRAME.match(low)
    if not frame:
        return None
    questioning = ("?" in str(text or "") or frame.group("aux") or frame.group("bare")
                   or (frame.group("verb") or "").startswith(("remember", "recall")))
    if not questioning:
        return None
    rest = low[frame.end():].strip(" ?!.,")
    if not rest or rest == low:
        return None
    if not SAYS_SOMETHING.search(rest):
        return None
    if extract.extract(rest):
        return rest
    return None

SAYS_SOMETHING = re.compile(
    r"\b(?:is|are|was|were|am|im|i'm|been|be|s|have|has|had|got|called|named|live|lives|"
    r"move|moved|moving|start|starts|started|work|works|eat|eats|need|needs|want|wants|like|"
    r"likes|love|loves|prefer|prefers)\b", re.I)

def _remembers_fact(text, memory):
    said = _restated(_folded(text, memory), text)
    if not said:
        return None
    found = extract.extract(said) or {}
    known = user(memory)
    yes, no = [], []
    for key in RESTATED_KEYS:
        value = found.get(key)
        if not value:
            continue
        stored = known.get(key)
        if not stored:
            continue
        if key == "pets":
            value = [p for p in value if isinstance(p, dict) and (p.get("name") or p.get("animal"))]
            if not value:
                continue
            value = value[0]
        matches = _said_matches(key, value, stored)
        said_back = _clause(key, stored, known)
        if not said_back:
            continue
        if matches:
            yes.append(said_back)
        elif matches is not None:
            no.append(said_back)
    if yes:
        fact = yes[0]
        return pick(["Yes \u2014 " + fact + ".",
                     fact[:1].upper() + fact[1:] + " \u2014 I have that.",
                     "That's right \u2014 " + fact + "."], memory)
    if no:
        fact = no[0]
        return pick(["You told me " + fact + ".", "Not quite \u2014 " + fact + "."], memory)
    kept = _someone_said_back(said, memory)
    if kept:
        return kept
    return None

def _someone_said_back(said, memory):
    words = " ".join(str(said or "").lower().split())
    if not words:
        return None
    found = extract.extract(said) or {}
    said_about = [other for other in (found.get("others") or []) if isinstance(other, dict)]
    for entry in others(memory):
        if not isinstance(entry, dict):
            continue
        who = str(entry.get("who") or "").strip().lower()
        if not who or not re.search(r"\b" + re.escape(who) + r"\b", words):
            continue
        if "name" in entry:
            called = _called(str(entry.get("name") or "").strip())
            if called:
                return "Your " + who + " is called " + called + "."
            continue
        age = entry.get("age")
        if age in (None, "", [], {}):
            continue
        given = [other.get("age") for other in said_about
                 if str(other.get("who") or "").lower() == who]
        if str(age) in [str(one) for one in given]:
            return "Your " + who + " is " + str(age) + "."
    return None

FOOD_CATEGORIES = (
    ("meat", ("meat", "chicken", "beef", "pork", "lamb", "bacon", "ham", "sausage", "sausages",
              "steak", "mince", "turkey", "burger", "burgers", "veal", "venison")),
    ("fish", ("fish", "salmon", "tuna", "prawn", "prawns", "shellfish", "cod")),
    ("dairy", ("dairy", "milk", "cheese", "butter", "cream", "yoghurt", "yogurt")),
    ("eggs", ("egg", "eggs")),
    ("gluten", ("gluten", "wheat", "bread", "pasta", "flour")),
    ("nuts", ("nut", "nuts", "peanut", "peanuts")),
    ("alcohol", ("alcohol", "beer", "wine", "booze", "spirits", "cider")),
)
NOT_THE_FOOD = frozenset((
    "red", "white", "processed", "raw", "cooked", "fresh", "any", "more", "much", "some", "the",
    "a", "bit", "of", "lot", "still", "either", "anymore", "again", "now", "it", "that", "this",
    "at", "all",
))
A_DIET_RULES_OUT = {
    "vegetarian": ("meat",),
    "vegan": ("meat", "fish", "dairy", "eggs"),
    "pescatarian": ("meat",),
    "no meat": ("meat",),
    "no dairy": ("dairy",),
    "dairy free": ("dairy",),
    "dairy-free": ("dairy",),
    "gluten free": ("gluten",),
    "gluten-free": ("gluten",),
    "no alcohol": ("alcohol",),
}
A_CONDITION_RULES_OUT = {
    "coeliac": ("gluten",),
    "celiac": ("gluten",),
    "coeliac disease": ("gluten",),
    "lactose intolerant": ("dairy",),
}
EATING_ASK = re.compile(
    r"^\W*do\s+i\s+(?:still\s+|really\s+|actually\s+|now\s+|ever\s+)?"
    r"(?:eat|drink)\s+(.+)$", re.I)
LEAD_IN = re.compile(r"^(?:so|and|but|ok|okay|well|sorry|hey|right|quick one)[, ]+", re.I)


def _the_food_named(rest):
    said = [word for word in re.findall(r"[a-z']+", str(rest or "").lower())
            if word not in NOT_THE_FOOD]
    if not said:
        return ""
    for category, words in FOOD_CATEGORIES:
        if all(any(word == one or word == one.rstrip("s") or word.rstrip("s") == one.rstrip("s")
                   for one in words) for word in said):
            return category
    return ""


def _the_rule_that_rules_it_out(known, category):
    diet = " ".join(str(known.get("diet") or "").lower().split())
    taken = list(A_DIET_RULES_OUT.get(diet) or ())
    if known.get("no_meat") and "meat" not in taken:
        taken.append("meat")
    if category in taken:
        if diet:
            return "No \u2014 " + _clause("diet", known.get("diet")) + "."
        return "No \u2014 you don't eat meat."
    for allergy in known.get("allergies") or []:
        said = str(allergy).lower()
        if any(said == one or said.rstrip("s") == one.rstrip("s")
               for one in dict(FOOD_CATEGORIES)[category]):
            return "No \u2014 " + _clause("allergies", known.get("allergies")) + "."
    for condition in known.get("condition") or []:
        word = " ".join(str(condition).lower().split())
        if category in (A_CONDITION_RULES_OUT.get(word) or ()):
            return "No \u2014 you've told me you're " + word + ", so " + category + " is out."
    return ""


def _a_rule_on_eating(text, memory):
    line = " ".join(str(text or "").lower().split())
    match = EATING_ASK.match(LEAD_IN.sub("", line))
    if not match:
        return None
    category = _the_food_named(match.group(1).strip(" ?!."))
    if not category:
        return None
    known = user(memory)
    if not isinstance(known, dict):
        return None
    rule = _the_rule_that_rules_it_out(known, category)
    return rule or None


def _confirmation(text, memory):
    statement = _statement(text)
    if not statement:
        return None
    if DUTY_ASK.search(statement):
        return None
    inverted = bool(re.search(r"\b(?:not|n't)\b", " ".join(text.lower().split())))
    found = extract.extract(statement)
    if not found:
        return None
    known = user(memory)
    yes, no, elsewhere = [], [], []
    for key, value in found.items():
        if key not in ("name", "age", "job", "city", "from", "diet", "budget", "allergies",
                       "pets"):
            continue
        stored = known.get(key)
        if key == "pets":
            value = [p for p in value if p.get("name") or p.get("animal")]
            if not value:
                continue
            value = value[0]
        if not stored:
            theirs_who, theirs = _other_fact(memory, key)
            if theirs_who and theirs:
                elsewhere.append((key, theirs_who, theirs))
            continue
        matches = _said_matches(key, value, stored)
        if matches is None:
            continue
        if matches:
            yes.append(_clause(key, stored or value, known))
        elif _names(key, " ".join(text.lower().split())):
            said_back = _clause(key, stored if stored else value, known)
            if said_back:
                no.append(said_back)
    if inverted:
        yes, no = no, yes
    if not yes and not no:
        for key, who, theirs in elsewhere:
            if key == "allergies":
                return _their_allergy(who, theirs)
        return None
    if no and not yes:
        if re.search(r"\bor\b", " ".join(text.lower().split())):
            return no[0][:1].upper() + no[0][1:] + "."
        return pick(["No — " + no[0] + ".", "Not quite — " + no[0] + "."], memory)
    said = "; ".join(yes[:2]) if yes else ""
    if no and yes:
        return pick(["Yes on one thing, no on another: " + said + ", but " + no[0] + ".",
                     "Partly — " + said + ", though " + no[0] + "."], memory)
    return pick(["Yes — " + said + ".", "That's right — " + said + ".",
                 "Yes, you told me — " + said + "."], memory)

def _old_values(memory, told):
    out = []
    entries = memory.get("facts_log")
    if not isinstance(entries, list):
        return out
    for entry in reversed(entries):
        if not isinstance(entry, dict):
            continue
        if " ".join(str(entry.get("text") or "").lower().split()) != told.lower():
            continue
        if entry.get("key") not in SWAPPABLE:
            continue
        for word in re.split(r"[\s,]+", str(entry.get("value") or "")):
            low = word.lower().strip("'-.!?")
            if (len(low) > 2 and low not in MONTHS and low not in extract.DAYS
                    and low not in STOPWORDS and low not in out
                    and re.search(r"\b" + re.escape(low) + r"\b", told, re.I)):
                out.append(low)
    return out

PUTTING_BY = re.compile(r"\b(?:save|saves|saving|saving up|put away|put by|set aside|put aside)\b",
                        re.I)

def _a_figure(word):
    return bool(re.fullmatch(r"\d[\d,]*(?:\.\d+)?\s*(?:k|grand|thousand|pounds?|quid)?",
                             str(word or "").strip(), re.I))

def _swapped_lines(memory, fixed):
    if not isinstance(fixed, dict):
        return []
    if fixed.get("dropped"):
        return []
    value = str(fixed.get("value") or "").strip()
    said = last_user(memory, 3) or []
    if isinstance(said, str):
        said = [said]
    mine = " ".join(str(fixed.get("said") or "").lower().split())
    said = [x for x in said if " ".join(str(x).lower().split()) != mine]
    told = " ".join(str(said[-1] if said else "").split())
    if not value or not told:
        return []
    out = []
    moved = _the_time_that_moved(told, fixed, value)
    if moved:
        return [moved]
    olds = _old_values(memory, told)
    if _a_figure(fixed.get("from")) and _a_figure(value):
        olds = [old for old in olds if _a_figure(old)]
    out.extend(re.sub(r"\b" + re.escape(old) + r"\b", value, told, count=1, flags=re.I)
               for old in olds)
    resized = resize.rewritten(str(fixed.get("said") or ""), memory)
    if resized:
        out.append(resized)
    out = [line for index, line in enumerate(out) if line not in out[:index]]
    if _a_figure(fixed.get("from")) and re.search(r"\d", value):
        gone = re.compile(r"\b" + re.escape(str(fixed["from"]).replace(",", "")) + r"\b")
        out = [line for line in out if not gone.search(line.replace(",", ""))]
    return out

def _the_time_that_moved(told, fixed, value):
    wrong = str(fixed.get("from") or "").strip()
    relative = RELATIVE_MONTH.fullmatch(wrong) if wrong else None
    if relative is not None:
        day, month = _date_said(str(fixed.get("value") or "").lower())
        if not month or not re.search(r"\b" + re.escape(wrong) + r"\b", told, re.I):
            return None
        said = _date_word_case(month)
        said = ("on the {day} of {said}".format(day=day, said=said) if day else "in " + said)
        return re.sub(r"\b" + re.escape(wrong) + r"\b", said, told, count=1, flags=re.I)
    was, now = _date_word(wrong), _date_word(value)
    if not was or not now or was.lower() == now.lower():
        return None
    if (was.lower() in MONTHS) != (now.lower() in MONTHS):
        return None
    if not re.search(r"\b" + re.escape(wrong) + r"\b", told, re.I):
        return None
    return re.sub(r"\b" + re.escape(wrong) + r"\b", now, told, count=1, flags=re.I)

def _a_rate_changed(text, memory):
    rewritten = resize.rewritten(text, memory)
    if not rewritten or resize.rate(rewritten) is None:
        return False
    return bool(PUTTING_BY.search(rewritten))

def _answer_the_new_one(memory, fixed):
    if isinstance(fixed, dict) and fixed.get("quiet"):
        return None
    lines = _swapped_lines(memory, fixed)
    if not lines:
        return None
    before = memory.get("understood")
    from ..modules import answers
    from ..memory import again as same_again
    try:
        for line in lines[:4]:
            memory["understood"] = understand(line, memory)
            reply = answers.respond(line, memory)
            if not isinstance(reply, str) or not reply.strip():
                continue
            if same_again.unframed(reply):
                return None
            return reply
    finally:
        if before is None:
            memory.pop("understood", None)
        else:
            memory["understood"] = before
    return None

def _name_fixed_this_turn(text, memory):
    fixed = memory.get("name_fixed") if isinstance(memory, dict) else None
    if not isinstance(fixed, dict) or fixed.get("said") != " ".join(str(text or "").lower().split()):
        return None
    memory.pop("name_fixed", None)
    name = str(fixed.get("name") or "")
    before = str(fixed.get("from") or "")
    if not name:
        return None
    if before and before.lower() != name.lower():
        return "{Name}, not {Before} \u2014 got it.".format(
            Name=name[:1].upper() + name[1:], Before=before[:1].upper() + before[1:])
    return "{Name} \u2014 got it.".format(Name=name[:1].upper() + name[1:])

_NUMBER_WORDS = (
    "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen "
    "fifteen sixteen seventeen eighteen nineteen").split()

def _a_number_word(number):
    try:
        number = int(number)
    except (TypeError, ValueError):
        return str(number)
    if number < 0:
        return str(number)
    if number < len(_NUMBER_WORDS):
        return _NUMBER_WORDS[number]
    if number < 100:
        tens, ones = divmod(number, 10)
        return _TENS_WORDS[tens] + ("-" + _NUMBER_WORDS[ones] if ones else "")
    if number < 1000:
        hundreds, rest = divmod(number, 100)
        said = _NUMBER_WORDS[hundreds] + " hundred"
        return said if not rest else said + " and " + _a_number_word(rest)
    return str(number)

def _fact_moved_this_turn(text, memory):
    moved = memory.get("fact_moved") if isinstance(memory, dict) else None
    if not isinstance(moved, dict) or moved.get("said") != " ".join(str(text or "").lower().split()):
        return None
    memory.pop("fact_moved", None)
    who = str(moved.get("who") or "").strip()
    was_who = str(moved.get("was_who") or "").strip()
    value = moved.get("value")
    if moved.get("kind") == "age":
        number = _a_number(value)
        if not number:
            return None
        said_value = _a_number_word(number)
    elif isinstance(value, str):
        said_value = value
    else:
        return None
    if not (who and was_who and said_value):
        return None
    return pick(CORRECTED_WHICH_PERSON, memory, seed_text=text).format(
        Value=said_value[:1].upper() + said_value[1:], value=said_value, who=who,
        was_who=was_who)

def _fact_fixed_this_turn(text, memory):
    fixed = memory.get("fact_fixed") if isinstance(memory, dict) else None
    if not isinstance(fixed, dict) or fixed.get("said") != " ".join(str(text or "").lower().split()):
        return None
    memory.pop("fact_fixed", None)
    who = str(fixed.get("who") or "").strip()
    was = fixed.get("was")
    value = fixed.get("value")
    new_number, old_number = (_a_number(value), _a_number(was))
    if fixed.get("kind") == "age" and new_number and old_number:
        value_said = _a_number_word(new_number)
        was_said = _a_number_word(old_number)
        said = pick(CORRECTED_AGAIN, memory, seed_text=text).format(
            Value=value_said[:1].upper() + value_said[1:], was=was_said,
            were=was_said[:1].upper() + was_said[1:], who=who,
            value=value_said)
    elif isinstance(value, str) and isinstance(was, str):
        said = pick(CORRECTED_AGAIN_WHO, memory, seed_text=text).format(
            Value=value[:1].upper() + value[1:], who=who or "you", value=value)
    else:
        return None
    return said

def _respond(text, memory):
    low_here = " ".join(str(text or "").lower().split())
    if _summed_up(low_here):
        if not any(str(value or "").strip() for value in user(memory).values()):
            return _vary(NOTHING_STARTED, memory)
        return _summary_reply(memory)
    renamed = _name_fixed_this_turn(text, memory)
    if renamed:
        return renamed
    put_right = _fact_fixed_this_turn(text, memory)
    if put_right:
        return put_right
    moved = _fact_moved_this_turn(text, memory)
    if moved:
        return moved
    corrected = _correction_this_turn(text, memory)
    if corrected:
        more = _answer_the_new_one(memory, memory.get("correction"))
        if isinstance(more, str) and more.strip():
            if _a_rate_changed(text, memory):
                return more.strip()
            return corrected.rstrip() + " " + more.strip()
        return corrected
    denied = _denial_this_turn(text, memory)
    if denied:
        return denied
    back = _the_back_this_turn(text, memory)
    if back:
        return back
    retracted = _retraction_this_turn(text, memory)
    if retracted:
        return retracted
    moved_town = _a_town_moved(memory, text)
    if moved_town:
        return moved_town
    left_out = pending.answer(text, memory) if isinstance(text, str) else None
    if left_out:
        return left_out
    named = family_name.reply_for(text, memory)
    if named:
        return named
    picked = _the_name_they_picked(text, memory)
    if picked:
        return picked
    called = _what_the_pet_is_called(text, memory)
    if called:
        return called
    picked_again = _the_pick_asked_again(text, memory)
    if picked_again:
        return picked_again
    folded = _folded(text, memory)
    low = MORE_OF_IT.sub(r"\1", _bare(folded))
    told = _a_diet_told(text, memory, low)
    if told:
        return told
    own = _a_pregnancy_of_their_own(text, memory, low)
    if own:
        return own
    stated = _a_state_told(text, memory, low)
    if stated:
        return stated
    was = _a_state_that_was(text, memory, low)
    if was:
        return was
    disliked = _a_dislike_told(text, memory)
    if disliked:
        return disliked
    named = _a_name_for_the_pet(text, memory, low)
    if named:
        return named
    compared = _age_compare(memory, low)
    if compared:
        return compared
    along = _how_far_along(memory, low)
    if along:
        return along
    ordered = _which_comes_first(memory, low)
    if ordered:
        return ordered
    settled = decided.answer(text, memory)
    if settled:
        return settled
    coming = company.answer(text, memory)
    if coming:
        return coming
    theirs = _relation_reply(memory, low)
    if theirs:
        return theirs
    called_back = told_about.callback(text, memory, facts=_told_readers(),
                                      plain=lambda asked: _respond(asked, memory),
                                      claims=lambda: bool(_about_this_chat(text, memory)))
    if called_back:
        return called_back
    remembered = told_about.answer(text, memory, facts=_told_readers(),
                                    plain=lambda asked: _respond(asked, memory),
                                    claims=lambda: bool(_about_this_chat(text, memory)))
    if remembered:
        return remembered
    if WHERE_PLAN.search(low):
        asked = _plans_reply(memory, low)
        if asked:
            return asked
        gone = user(memory).get("plan_dropped")
        if isinstance(gone, str) and gone:
            if SAID_AS_A_SENTENCE.match(gone):
                return pick(["That plan is off, then \u2014 where are you going?",
                             "Right, that one is off the record \u2014 where are you headed?",
                             "Scratch that trip, then \u2014 where is it now?"], memory)
            shown = gone[:1].upper() + gone[1:]
            return pick([shown + " is off, then \u2014 where are you going?",
                         "Not " + shown + ", then. Where are you headed?",
                         "Right, " + shown + " is dropped \u2014 where is it now?"], memory)
        return None
    whose = _a_persons_birthday_reply(memory, low)
    if whose:
        return whose
    said_until = until_answer(text, memory)
    if said_until:
        return said_until
    from ..compose.own_facts import said_back
    the_line_back = said_back(text, memory)
    if the_line_back:
        return the_line_back
    said_side = already_answer(text, memory)
    if said_side:
        return said_side
    said_when = when_answer(text, memory)
    a_birthday_ask = recall.ask(text) == "birthday" or recall.ask(low) == "birthday"
    if (WHEN_ASKS.search(low) or WHEN_THING.search(low) or TIME_ASKS.search(low)
            or TIME_THING.search(low) or TIME_IT.search(low) or DAY_THING.search(low)
            or DAY_IT.search(low) or DAY_ASKS.search(low) or WHEN_PLAN.search(low)
            or WHEN_THING_VERB.search(low)) and not a_birthday_ask:
        prep = _the_prep_day(memory, low)
        if prep:
            return prep
        asked = _plans_reply(memory, low)
        if asked:
            return asked
        if said_when:
            return said_when
        if (WHEN_ASKS.search(low) or TIME_ASKS.search(low) or WHEN_THING_VERB.search(low)
                or DAY_ASKS.search(low)):
            part = plans.follow_up(text, memory)
            if part:
                return part
            return None
    elif said_when and not a_birthday_ask:
        return said_when
    planned = plans.answer(text, memory)
    if planned:
        return None
    part = plans.follow_up(text, memory)
    if part:
        return part
    if not folded:
        return None
    asked = history.asked(text, memory)
    if asked == "first":
        return _first_reply(memory)
    if asked == "first_bot":
        return _first_bot_reply(memory)
    if asked == "said_about":
        said = _what_i_said_about(memory, history.the_thing_named(text))
        if said:
            return said
    if asked == "topics":
        if _summary_ask(low) or TALKED_ABOUT.search(low):
            return _topic_reply(memory, low)
        return _topics_reply(memory)
    handed_back = choose.reply_for(text, memory)
    if handed_back:
        return handed_back
    enough = enough_reply(text, memory)
    if enough:
        return enough
    another_of_them = turned_down.reply_for(text, memory)
    if another_of_them:
        return another_of_them
    other = second_half.other_option(text, memory)
    if other:
        return other
    back = _return_reply(text, memory)
    if back:
        return back
    remembered = _remembers_fact(text, memory)
    if remembered:
        return remembered
    ruled_out = _a_rule_on_eating(text, memory)
    if ruled_out:
        return ruled_out
    confirmed = _confirmation(text, memory)
    if confirmed:
        return confirmed
    if ASKS_FOR_TASTES.search(low):
        liked = _tastes_said(memory)
        if liked:
            return liked
    if TASTE_ASK.search(low):
        said = _taste_reply(memory, low)
        if said:
            return said

    spend_tally = spent.answer(text, memory) or spent.answer(folded, memory)
    if spend_tally:
        return spend_tally
    general = _general_recall(text, memory) or _general_recall(folded, memory)
    asks_about_someone = _asks_about_someone(low, text, memory)
    if asks_about_someone:
        told = None
        if _other_person_reply(memory, low):
            told = _other_person_reply(memory, _the_ask_after_a_statement(low, memory))
        telling = _after_the_yes_no_frame(text) if isinstance(text, str) else ""
        if told and not (NO_RECORD.search(told) and telling
                         and _says_more_than_the_ask(telling)):
            return told
    who_asked = _named_person(low, memory)
    if not who_asked and re.search(r"\b(?:she|her|he|him)\b", low):
        who_asked = _person_from_pronoun(low, memory)
    if not who_asked and AGE_ASK.search(low):
        pointed = _a_pronoun_age(memory, low)
        if pointed:
            return pointed
    aged = _ages_reply(memory, low, folded)
    if aged:
        return aged
    place = _their_place(low)
    if place:
        return pick(["I can\u2019t see inside your " + place + ", so tell me what\u2019s in there and "
                     "I\u2019ll tell you what it will make",
                     "I\u2019ve no way of knowing what\u2019s in your " + place + ": say what\u2019s in "
                     "it and I\u2019ll find you something to cook",
                     "Nothing in your " + place + " I can see from here. Tell me what\u2019s in it and "
                     "I\u2019ll work something out"], memory).rstrip(".") + "."
    counted = _kids_reply(memory, low)
    if counted:
        return counted
    called = _a_relations_name_reply(memory, low, text)
    if called:
        return called
    owned = _a_thing_i_own_reply(memory, low)
    if owned:
        return owned
    about_person = _about_a_person_reply(memory, low, text)
    if about_person:
        return about_person
    whom = _who_is_the_name_reply(memory, low)
    if whom:
        return whom
    if (_asked_person(memory, low)
            and not (PLACE_ADVICE.search(low) and not PLACE_RECALLED.search(low))):
        return _places_reply(memory, low)
    refused = _not_the_same_reply(memory, low)
    if refused:
        return refused
    if not _about_this_chat(text, memory) and not _a_why_line_they_have_answered(text, memory):
        return general or _about_what_they_said(text, memory)
    if re.search(r"\b(?:what|which)\b.*\bmy name\b|\bwho am i\b|^my name$|\bwhat my name\b|"
                 r"\b(?:know|remember) my name\b|\bwhat did (?:i|u|you) (?:say|tell me) my name was\b",
                 low):
        return _name_reply(memory, low)
    if re.search(r"\bmy job\b|\bmy work\b|\bwhat do i do\b|\bwhere do i work\b|"
                 r"\bwhat do i work as\b|\bwhat i (?:do|did)\b|\bfor a living\b", low) \
            or (WHERE_WORK.search(low) and not _doing_again(text, memory)):
        if _doing_again(text, memory) or (SAID_ABOUT.search(low) and _names_its_thing(low)):
            asked = _topic_reply(memory, low)
            if asked and not _a_denial(asked):
                return asked
        part = _a_part_of_the_job_never_said(memory, low)
        if part:
            return part
        return _job_reply(memory, where=bool(WHERE_WORK.search(low)))
    if re.search(r"\b(?:remember|recall|know)\b[^.]{0,18}\bwhat i (?:do|did)\b\W*$", low):
        return _job_reply(memory)
    if (PLACES_ASK.search(low) and SELF_WORD.search(low)
            and not (PLACE_ADVICE.search(low) and not PLACE_RECALLED.search(low))):
        return _places_reply(memory, low)
    if recall.ask(text) == "limit":
        limit = _limit_reply(memory, low)
        if limit:
            return limit
    if (_asks_for_a_fact(low, text, memory) or (DIET_ASK.search(low) and not DIET_HOW_TO.search(low))
            or _a_count_ask(low) is not None):
        return _fact_reply(memory, low)
    if PLAN_MINE.search(low):
        return _plans_reply(memory, low)
    if FIRST_ASK.search(low):
        return _first_reply(memory)
    if _repeat_ask(text, folded):
        return _repeat_reply(memory, text)
    if SAID_ASK.search(low):
        return _said_reply(memory)
    if re.search(r"^what i (?:told|said)(?: you)?$|^what have i (?:told|said)(?: you)?$", low):
        return _summary_reply(memory)
    if re.search(r"\babout me\b|\bof me\b", low):
        return _summary_reply(memory)
    kind_said = _an_open_attribute_ask(low, memory)
    if kind_said:
        return kind_said
    if WHAT_I_SAID.search(low) or re.search(
            r"\bwhat was it i said\b|^what i (?:said|told you|mentioned)\b|"
            r"^what we (?:said|told you|mentioned)\s+(?:about|on|regarding)\b|"
            r"^anything i (?:said|told you|mentioned)\b|"
            r"\bi (?:cant|cannot|can not|dont|do not) (?:really |quite )?remember "
            r"what i (?:said|told you|mentioned)\b|"
            r"\b(?:do|can|could|did) (?:you|u) remember what i\b", low) \
            or THING_AGAIN.match(low) or reminded.the_thing(text, memory) \
            or _which_thing_was_it(low, memory) or _an_attribute_they_gave(low):
        said = _recall_reply(memory, low, text)
        if said:
            return said
        earlier = [line for line in last_user(memory, 4)
                   if " ".join(str(line or "").split()).lower()
                   != " ".join(str(text or "").split()).lower()]
        if earlier and _a_place_new_to_the_chat(memory, low):
            return general or _about_what_they_said(text, memory)
    if re.search(r"\bmy age\b|\bhow old am i\b|\bhow old did i say\b|"
                 r"\bhow old (?:i am|i was|we are|i(?:'m| am) gon(?:na|e) to be)\b", low):
        theirs = re.search(r"\b(?:she|her)\b|\b(?:he|him)\b", low)
        if theirs and not _person_from_pronoun(low, memory):
            return ("You haven't told me how old she is." if re.search(r"\b(?:she|her)\b", low)
                    else "You haven't told me how old he is.")
        return _age_reply(memory)
    pet = _pet_part_reply(memory, low)
    if pet:
        return pet

    if ASKED_ALL.search(low):
        return _asked_reply(memory)
    if not _about_the_bot_here(memory) and (
            THE_CHAT_ASK.search(low) or TOPIC_ASK.search(low)
            or ACTIVITY_ASK.search(low) or TALKED_ABOUT.search(low)):
        if ACTIVITY_ASK.search(low) and (PLAN_WORDS.search(low) or _plan_was_corrected(memory)
                                         or (UP_TO_ASK.search(low)
                                             and _the_line_before_was_a_plan(memory))):
            asked = _plans_reply(memory, low)
            if asked:
                return asked
        else:
            asked = _topic_reply(memory, low, again=bool(ASKING_AGAIN.search(folded)))
            if asked:
                return asked
    if _summary_ask(low):
        return _topic_reply(memory, low)
    if re.search(r"\bwhat have i told you\b|\bwhat do you (?:know|remember) about me\b|"
                 r"\babout me\b|^what i (?:told|said)(?: you)?$|^what have i (?:told|said)(?: you)?$",
                 low):
        return _summary_reply(memory)
    if PLAN_ASKS.search(low):
        asked = _plans_reply(memory, low)
        if asked:
            return asked
    if "remember" in low and "yesterday" in low:
        return _topic_reply(memory, low)
    return general or _about_what_they_said(text, memory)

def _a_place_new_to_the_chat(memory, low):
    named = {word.lower() for word in re.findall(r"[a-z][a-z'\-]+", " ".join(str(low or "").split()))}
    places = {word for word in named if word in PLACES or word in extract.COUNTRIES}
    if not places:
        return False
    said = " ".join(" ".join(str(line or "").lower().split())
                    for line in last_user(memory, 12))
    return not any(place in said for place in places)

OWN_ASK = re.compile(
    r"^\W*(?:do|did|does|am|are|is|was|were|have|has|had|can|could)\s+(?:i|we)\b", re.I)

ASK_FILLER = frozenset("""do did does am are is was were have has had can could i we me my
know think say said tell told remember recall really still actually ever even just
much many again any anything something""".split())

NO_THING = frozenset("""you your the and for not out all any get got let put see use try buy pay
one two new old bad big top end way day now why how what who can see say ask own had his her its
our ours mine they them there here then than that this these those very too just also even still
yet ever some but nor same such with from into onto over under off ago lot bit""".split())

def _about_what_they_said(text, memory):
    low = " ".join(str(text or "").lower().split()).strip(" ?!.,")
    if not OWN_ASK.match(low) or len(low.split()) > 9:
        return None
    words = {stem(word) for word in re.findall(r"[a-z']+", low)}
    words = {word for word in words
             if len(word) > 3 and word not in ASK_FILLER and word not in NO_THING}
    words |= {word for word in re.findall(r"\b[a-z]{3}\b", low) if word not in NO_THING
              and word not in ASK_FILLER}
    if not words:
        return None
    said_before = [str(turn.get("user") or "") for turn in (memory.get("turns") or [])
                   if isinstance(turn, dict)]
    newest = " ".join((said_before[-1] if said_before else "").lower().split()).strip(" ?!.,")
    for line in reversed(said_before):
        said = {stem(word) for word in re.findall(r"[a-z']+", str(line or "").lower())}
        if not words <= said:
            continue
        phrase = _told_phrase(line)
        if phrase:
            phrase = phrase.replace("can not", "cannot")
            flat = " ".join(str(line or "").lower().split()).strip(" ?!.,")
            if flat != newest:
                return pick(["Earlier you said " + phrase + " - still the case?",
                             "You said " + phrase + ", earlier in this chat - still the case?"],
                            memory)
            return pick(["You told me " + phrase + ".", "You said " + phrase + "."], memory)
        return None
    return None

AVOID_ADVICE = re.compile(r"\b(?:what|which|anything)\b[^.!?]{0,24}"
                          r"\b(?:avoid|avoids|watch out for|stay away from|stay off)\b", re.I)

BARE_WHAT_I_DO = re.compile(r"^(?:so |and |but )?what (?:do|did) i (?:actually |really |even )?"
                            r"(?:do|say)(?: again)?$", re.I)

def _the_job_was_just_said(memory):
    job = str(user(memory).get("job") or "").strip().lower()
    if not job:
        return False
    for turn in reversed(memory.get("turns") or []):
        if not isinstance(turn, dict):
            continue
        said = str(turn.get("user") or "").strip()
        if not said:
            continue
        if BARE_WHAT_I_DO.match(_bare(said)):
            continue
        return job in said.lower() and _nothing_but_the_job(said, job, memory)
    return False

JOB_LINE_WORDS = frozenset("""i im am is was be being job jobs work works working as in at on for
with of and the a an it its s my our to here so yeah yes ok okay""".split())

def _nothing_but_the_job(said, job, memory):
    rest = str(said).lower().replace(job, " ")
    frame = str(user(memory).get("job_frame") or "").strip().lower()
    if frame:
        rest = rest.replace(frame, " ")
    return not [word for word in re.findall(r"[a-z']+", rest)
                if len(word) > 2 and word not in JOB_LINE_WORDS]

AVOID_REST = re.compile(r"\b(?:avoid|avoids|watch out for|stay away from|stay off)\b(.*)$",
                        re.I | re.S)

EATING = re.compile(r"\b(?:eat|eats|eating|ate|food|foods|meal|meals|cook|cooking|cooked|recipe|"
                    r"recipes|dish|dishes|dinner|lunch|tea\b|breakfast|snack|snacks|restaurant|"
                    r"menu|takeaway|take-away|buffet|party|barbecue|bbq|gluten|dairy|nuts?|"
                    r"allerg\w*|intoleran\w*)\b", re.I)

ALLERGY_SAID = re.compile(r"\b(?:allerg\w*|intoleran\w*|coeliac|celiac)\b", re.I)

def _the_allergy_is_what_is_asked(text, memory):
    rest = AVOID_REST.search(text)
    tail = " ".join(rest.group(1).split()) if rest else ""
    if tail and not EATING.search(tail):
        return False
    said = " ".join(text.split())
    before = last_user(memory)
    if ALLERGY_SAID.search(said) or ALLERGY_SAID.search(before or ""):
        return True
    return not before

def _general_recall(text, memory):
    low = " ".join(text.lower().split())
    if AVOID_ADVICE.search(text) and user(memory).get("allergies") \
            and _the_allergy_is_what_is_asked(text, memory):
        return _limit_reply(memory, low) or _fact_reply(memory, low, "allergy")
    if BARE_WHAT_I_DO.match(low) and user(memory).get("job") and _the_job_was_just_said(memory):
        return _job_reply(memory)
    spent_reply = spent.answer(text, memory)
    if spent_reply:
        return spent_reply
    left_reply = spent.what_is_left(text, memory)
    if left_reply:
        return left_reply
    key = recall.ask(text)
    if not key:
        return None
    if SAID_ABOUT.search(low) and _names_its_thing(low) and not _the_fact_is_kept(key, memory):
        return None
    if key == "name":
        return _name_reply(memory, low)
    if key == "job":
        part = _a_part_of_the_job_never_said(memory, low)
        if part:
            return part
        return _job_reply(memory, where=bool(WHERE_WORK.search(low)))
    if key == "city":
        return _places_reply(memory, low)
    if key in ("birthday", "weight", "height"):
        return _fact_reply(memory, low, key)
    if key == "diet":
        return _diet_reply(memory, low)
    if key in ("allergy", "budget", "pet", "car"):
        return _fact_reply(memory, low, key)
    if key == "limit":
        return _limit_reply(memory, low)
    if key == "me":
        return _summary_reply(memory)
    return None

NAME_ASK = re.compile(
    r"\b(?:what|which)\s+(?:shall|should|would|could|do|can|will|might)\s+(?:i|we|you)\s+"
    r"(?:call|name)\s+(?:it|him|her|them|this|that|the\s+[\w']+)\b"
    r"|\b(?:any|some)\s+(?:good|nice|ideas?|thoughts?)?\s*(?:for\s+)?(?:a\s+)?names?\b"
    r"|\bnames?\s+(?:ideas?|suggestions?)\b"
    r"|\b(?:name|naming)\s+(?:ideas?|suggestions?)\b"
    r"|\b(?:suggest|give me|throw me|help me (?:pick|choose|find|think of)?)\s*(?:me\s+)?"
    r"(?:a\s+|some\s+)?names?\b"
    r"|\bwhat\s+(?:would|do)\s+you\s+(?:call|name)\b"
    r"|\bhelp me name\b", re.I)

def _pet_names(family):
    if family == "cat":
        return CAT_NAMES
    if family in ("rabbit", "hamster", "fish", "parrot"):
        return SMALL_NAMES
    return DOG_NAMES

POINTING = re.compile(r"\b(?:this|that|the|my|our|your|his|her|their|a|an)\s+"
                      r"(?:(?:new|little|baby|poor|first|next|wee|small|own)\s+)?"
                      r"([a-z][a-z']{1,})", re.I)

POINTING_ANY = frozenset("""pet pet's baby name names one thing it him her them pup kit
animal""".split())

def _points_at_something_else(low):
    for word in POINTING.findall(low or ""):
        if word in extract.ANIMALS or word in POINTING_ANY:
            continue
        return True
    return False

def _the_pet_in_play(low, memory):
    named = [word for word in re.findall(r"[a-z']+", low) if word in extract.ANIMALS]
    if named:
        return _animal_family(named[0])
    for turn in reversed((memory.get("turns") or [])[-3:]):
        line = str((turn or {}).get("user") or "").lower()
        said = [word for word in re.findall(r"[a-z']+", line) if word in extract.ANIMALS]
        if said:
            return _animal_family(said[0])
    pets = user(memory).get("pets") or []
    if pets and isinstance(pets[0], dict) and pets[0].get("animal"):
        return _animal_family(pets[0].get("animal"))
    return None

def _a_pet_of_theirs_is_named(low, family, memory):
    if not re.search(r"\b(?:it|him|her|them|this one|that one)\b", low or ""):
        return False
    for pet in user(memory).get("pets") or []:
        if (isinstance(pet, dict) and pet.get("name")
                and _animal_family(pet.get("animal")) == _animal_family(family)):
            return True
    return False

def _a_name_for_the_pet(text, memory, low):
    if not NAME_ASK.search(low or ""):
        return None
    family = _the_pet_in_play(low, memory)
    if not family or family == "pet":
        return None
    if _points_at_something_else(low):
        return None
    if _a_pet_of_theirs_is_named(low, family, memory):
        return None
    pool = list(_pet_names(family))
    seed = len(memory.get("turns") or []) * 7919 + sum(ord(c) for c in str(text).lower())
    shuffled = random.Random(seed).sample(pool, 3)
    advice = NAME_ADVICE[seed % len(NAME_ADVICE)]
    animal = _a(family)
    return ("For " + animal + ": " + ", ".join(shuffled[:-1]) + " or " + shuffled[-1] + ". "
            + advice)

def _count_of_a_kind(pets):
    said = [int(p.get("count") or 0) for p in pets if int(p.get("count") or 0) > 1]
    if said and max(said) >= len(pets):
        return max(said)
    return sum(int(p.get("count") or 1) for p in pets)

def _return_reply(text, memory):
    record = resumed(memory)
    if not record or record.get("asks"):
        return None
    thing = (record.get("asked") or "").strip()
    if not thing or len(thing.split()) > 4:
        return None
    return pick([line.format(thing=_same_case(thing, text)) for line in RESUME], memory)

def _same_case(thing, text):
    for word in text.split():
        if word.strip(" ,.!?").lower() == thing.lower() and word[:1].isupper():
            return thing[:1].upper() + thing[1:]
    return thing

def _name_reply(memory, low=""):
    who = name(memory)
    plan = user(memory).get("plan") or ""
    if who and plan and re.search(r"\bplan(?:ning|s)?\b|\bdoing\b|\bup to\b", low):
        first, rest = plan[:1], plan[1:]
        clause = first.lower() + rest if not rest[:1].isupper() else plan
        return "You're " + who + ", and you're planning " + clause.rstrip(".") + "."
    if not who:
        memory["asked_for"] = "name"
        return pick(["You haven't told me your name yet.", "I don't know it yet — you haven't said."],
                    memory)
    return pick(["You're " + who + ".", who + " — you told me.", "Your name's " + who + "."], memory)

def _the_day_of(plan):
    said = str(plan or "").lower()
    found = WEEKDAY_WORD.search(said)
    if found:
        return "On " + found.group(0).capitalize() + "."
    number = DAY_OF_MONTH.search(said)
    if number:
        return "On the " + number.group(1) + "."
    return ""

def _at_the_clock(plan):
    found = AT_TIME.search(str(plan or ""))
    if not found:
        return ""
    said = " ".join(found.group(0).split())
    return "At " + said[3:] + "." if said.lower().startswith("at ") else ""

POINTS_BACK_AT_IT = re.compile(
    r"\b(?:for|to|about|with|on|before|after|from|into|of|at)\s+(?:it|that|this)\b", re.I)

SETTING_OUT = re.compile(
    r"\b(?:leave|leaves|leaving|left|set off|setting off|set out|setting out|travel|travelling|"
    r"traveling|head off|heading off|go|going|get going)\b", re.I)

STUDY_PLAN = re.compile(
    r"\b(?:exam|exams|revision|revise|revising|revised|past paper|past papers|mock|mocks)\b",
    re.I)

def _the_day_before(plan):
    low = " ".join(str(plan or "").lower().split())
    found = [day for day in WEEK if re.search(r"\b" + day + r"\b", low)]
    if len(found) != 1:
        return None
    if MONTH_WORD.search(low) or DATE_PHRASE.search(low):
        return None
    day = found[0]
    return day, WEEK[WEEK.index(day) - 1]

def _the_prep_day(memory, low):
    if not POINTS_BACK_AT_IT.search(low) or not _a_plan_answers(memory, low):
        return None
    back = POINTS_BACK_AT_IT.search(low)
    if SETTING_OUT.search(low[max(0, back.start() - TAIL_WINDOW):back.start()]):
        return None
    known = user(memory)
    plans = [p for p in (known.get("plans") or []) if isinstance(p, str) and p.strip()]
    latest = known.get("plan")
    if isinstance(latest, str) and latest.strip() and latest not in plans:
        plans.append(latest)
    for plan in reversed(plans):
        if STUDY_PLAN.search(plan):
            continue
        dated = _the_day_before(plan)
        if not dated:
            continue
        day, before = dated
        said = plan_sentence(plan, plan_line(memory, plan)).rstrip(".")
        return (said + ", so " + before.title() + " is the day for the prep \u2014 keep " + day
                + " itself for the last bits.")
    return None

def _a_plan_answers(memory, low):
    for pattern in (WHEN_ASKS, WHEN_THING, TIME_ASKS, TIME_THING):
        found = pattern.search(low)
        if not found:
            continue
        if _names_something_of_its_own(low, found.end()):
            return False
        reply = _plans_reply(memory, low)
        return bool(reply) and reply not in NO_PLANS_REPLY
    return False

def _the_date_behind_that(memory, low, plans):
    if not THAT_DATE.search(low) or not CALENDAR_SAID.search(str(last_bot(memory) or "")):
        return None
    for plan in reversed(plans):
        day = WEEKDAY_WORD.search(plan.lower())
        if day:
            worked = solve("what date is " + day.group(0), {}, memory)
            if worked:
                return worked
    return None

_A_DATE_AT_THE_END = re.compile(
    r"^(?P<subject>.*?)\s+(?P<date>(?:in|on|at|next|this)\s+[a-z0-9' ]+\.?)$", re.I)

def _the_whole_word_in(text, word):
    if not word:
        return -1
    found = re.search(r"(?<![\w'])" + re.escape(word) + r"(?![\w'])", str(text or ""))
    return found.start() if found else -1


def _third_person(word):
    word = str(word or "").strip(".,!?;:")
    if not word or not word.isalpha():
        return word
    if word.endswith(("s", "x", "z", "ch", "sh")):
        return word + "es"
    if word.endswith("o") and len(word) > 1 and word[-2] not in "aeiou":
        return word + "es"
    if word.endswith("y") and len(word) > 1 and word[-2] not in "aeiou":
        return word[:-1] + "ies"
    return word + "s"

def _the_line_that_said(memory, plan):
    wanted = " ".join(str(plan or "").lower().split())
    if not wanted:
        return None
    for line in reversed(last_user(memory, 6) if isinstance(last_user(memory, 6), list) else []):
        if wanted in " ".join(str(line).lower().split()):
            return line
    return None

def _the_verb_from_the_line(plan, line):
    wanted = " ".join(str(plan or "").lower().split())
    text = " ".join(str(line or "").split())
    if not wanted or not text:
        return ""
    for piece in re.split(r"\s+and\s+|,|;", text):
        clause = " ".join(piece.split()).strip(" ,.;:-!")
        if not clause or " ".join(clause.lower().split()) == wanted:
            continue
        match = _A_DATE_AT_THE_END.match(clause)
        if not match:
            continue
        before = match.group("subject").split()
        if len(before) < 3 or before[0].lower() not in ("my", "our", "the", "his", "her", "their"):
            continue
        body = " ".join(before[2:]).strip(" ,")
        words = body.split()
        if not words or len(words) > 4 or not words[0].isalpha():
            continue
        words = [_a_number_word(word) if word.isdigit() and len(word) < 3 else word
                 for word in words]
        body = " ".join(words)
        if words[0].lower() in ("is", "are", "was", "were", "am"):
            continue
        return body
    return ""

def _the_verb_they_asked(plan, low, line=""):
    text = " ".join(str(plan or "").split())
    match = _A_DATE_AT_THE_END.match(text)
    if not match:
        return plan
    subject = match.group("subject")
    if subject.split()[-1] in ("is", "are", "was", "were"):
        subject = " ".join(subject.split()[:-1])
    asked = " ".join(str(low or "").split()).strip("?.! ")
    at = _the_whole_word_in(asked, subject)
    if at < 0:
        return plan
    rest = asked[at + len(subject):].strip()
    if not rest or rest in ("again", "now", "this year", "next year"):
        borrowed = _the_verb_from_the_line(plan, line)
        if borrowed:
            return subject + " " + borrowed + " " + match.group("date")
        return plan
    words = rest.split()
    if len(words) > 4:
        return plan
    doing = ("birthday", "bday", "dob", "date of birth", "name")
    if words[0].lower() in doing:
        return subject + " " + rest + " is " + match.group("date")
    if words[0].lower().endswith("ing") and len(words[0]) > 4:
        return subject + " is " + " ".join(words) + " " + match.group("date")
    if words[0].lower() in ("is", "are", "was", "were", "will", "would", "can", "could",
                            "has", "had", "does", "did"):
        return subject + " " + " ".join(words) + " " + match.group("date")
    if words[0].lower().endswith("s") and not words[0].lower().endswith("ss"):
        return plan
    words[0] = _third_person(words[0])
    return subject + " " + " ".join(words) + " " + match.group("date")

def _plans_reply(memory, low):
    known = user(memory)
    plans = [p for p in (known.get("plans") or []) if isinstance(p, str) and p.strip()]
    latest = known.get("plan")
    if isinstance(latest, str) and latest.strip() and latest not in plans:
        plans.append(latest)
    worked = _the_date_behind_that(memory, low, plans)
    if worked:
        return worked
    if WHERE_PLAN.search(low) or WHEN_PLAN.search(low):
        if plans:
            said = plan_line(memory, plans[-1])
            part = the_part_asked(plans[-1], low, said, _a_place)
            if part and content(part) != content(str(last_bot(memory) or "")):
                return part
            return plan_sentence(plans[-1], said) + "."
        return None
    clock = TIME_ASKS.search(low)
    if clock:
        plan = _the_one_asked([p for p in plans if _says_the_verb(p, clock.group(1))],
                              low[clock.end():])
        if plan:
            return _at_the_clock(plan) or plan_sentence(plan, plan_line(memory, plan)) + "."
        return None
    hour = TIME_THING.search(low)
    if hour:
        plan = _the_one_asked([p for p in plans if _names_the_thing(p, hour.group(1))],
                              low[hour.end():])
        if plan:
            return _at_the_clock(plan) or plan_sentence(plan) + "."
        return None
    pointed_clock = TIME_IT.search(low)
    if pointed_clock:
        if plans:
            return _at_the_clock(plans[-1])
        return None
    day_asked = DAY_ASKS.search(low)
    if day_asked:
        plan = _the_one_asked([p for p in plans if _says_the_verb(p, day_asked.group(1))],
                              low[day_asked.end():])
        if plan:
            return _the_day_of(plan) or plan_sentence(plan, plan_line(memory, plan)) + "."
        return None
    day = DAY_THING.search(low)
    if day:
        plan = _the_one_asked([p for p in plans if _names_the_thing(p, day.group(1))],
                              low[day.end():])
        if plan:
            return _the_day_of(plan) or plan_sentence(plan, plan_line(memory, plan)) + "."
        return None
    pointed_day = DAY_IT.search(low)
    if pointed_day:
        if plans:
            return _the_day_of(plans[-1])
        return None
    when = WHEN_ASKS.search(low)
    if when:
        plan = _the_one_asked([p for p in plans if _says_the_verb(p, when.group(1))],
                              low[when.end():])
        if plan:
            day = _the_day_of(plan)
            if day and _the_day_is_the_whole_date(plan) and _the_plan_was_just_said_back(memory, plan):
                return day
            return plan_sentence(_the_verb_they_asked(plan, low, plan_line(memory, plan)
                                        or _the_line_that_said(memory, plan)),
                                 plan_line(memory, plan)) + "."
        halves = [p for p in plans if _the_verb_they_asked(p, low) != p]
        plan = _the_one_asked(halves, "") if halves else None
        if plan:
            return plan_sentence(_the_verb_they_asked(plan, low, plan_line(memory, plan)
                                        or _the_line_that_said(memory, plan)),
                                 plan_line(memory, plan)) + "."
        if SAYS_A_TRIP.search(low):
            for plan in reversed(plans):
                if _about_kind("trip", plan, memory, phrase=True):
                    return plan_sentence(plan, plan_line(memory, plan)) + "."
        return None
    thing = _when_thing(low, wide=not plans)
    if thing:
        asking = [p for p in plans if _names_the_thing(p, thing, memory)]
        if _asks_the_end(low) or _asks_the_start(low):
            asking = [p for p in asking if _answers_the_end_asked(p, low)]
        plan = _the_one_asked(asking, "")
        if plan:
            day = _the_day_of(plan)
            if day and _the_day_is_the_whole_date(plan) and _the_plan_was_just_said_back(memory, plan):
                return day
            return plan_sentence(_the_verb_they_asked(plan, low, plan_line(memory, plan)
                                        or _the_line_that_said(memory, plan)),
                                 plan_line(memory, plan)) + "."
        return None
    if WHEN_THING.search(low) and re.search(r"\b(?:bank|public)\s+holiday", low):
        return None
    if _thing_is_a_quality(low):
        return None
    if not plans:
        if _a_time_for_the_job_itself(low):
            return None
        return pick(list(NO_PLANS_REPLY), memory)
    if _the_answer_about_it_is_on_the_screen(memory, plans[-1], low):
        return None
    said = [plan_sentence(plan, plan_line(memory, plan)) for plan in plans[-2:]][::-1]
    if len(said) == 1:
        return with_a_tail(said[0] + ".", memory)
    return said[0] + ". And " + said[1][:1].lower() + said[1][1:] + "."

THEIR_PLACES = frozenset("fridge freezer cupboard cupboards pantry larder".split())

IN_A_PLACE = re.compile(r"\bwhat (?:have|has) (?:i|we) got (?:in|on) (?:the|my|our)\s+(\w+)")

IN_MY_PLACE = re.compile(r"\bwhat(?:'s| is|s)?\s+(?:in|on) (?:the|my|our)\s+(\w+)")

FOR_A_MEAL = re.compile(r"\bwhat (?:have|has) (?:i|we) got (?:for|in) (?:dinner|lunch|tea|supper|"
                        r"breakfast)\b|\bwhat(?:'s| is|s)\s+for (?:dinner|lunch|tea|supper)\b")

def _their_place(low):
    for pattern in (IN_A_PLACE, IN_MY_PLACE):
        found = pattern.search(low)
        if found and found.group(1) in THEIR_PLACES:
            return found.group(1)
    if FOR_A_MEAL.search(low):
        return "fridge"
    return None

def _naming_words(text):
    return [word for word in _topics.words(text or "")
            if word not in _topics.STOPWORDS and len(word) > 2]

def _the_day_is_the_whole_date(plan):
    low = str(plan or "").lower()
    if _at_the_clock(plan):
        return False
    return not any(re.search(r"\b" + name + r"\b", low) for name in extract.MONTHS)

def _the_plan_was_just_said_back(memory, plan):
    mine = set(re.findall(r"[a-z']+", str(plan or "").lower()))
    if len(mine) < 3:
        return False
    said = set(re.findall(r"[a-z']+", str(last_bot(memory) or "").lower()))
    return len(mine & said) >= max(3, -(-len(mine) * 7 // 10))

def _the_answer_about_it_is_on_the_screen(memory, plan, text):
    mine = {word for word in str(plan or "").lower().split()
            if word.isalpha() and len(word) > 2 and word not in _topics.STOPWORDS}
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not mine or not isinstance(turns, list) or not turns:
        return False
    asked = set(_naming_words(text))
    if not asked:
        return False
    screen = set()
    for turn in reversed(turns):
        if not isinstance(turn, dict):
            continue
        on_screen = str(turn.get("bot") or "").strip()
        if not on_screen:
            continue
        if _topics.only_acknowledges(on_screen):
            continue
        screen = set(_naming_words(on_screen))
        break
    if not screen:
        return False
    for turn in reversed(turns):
        if not isinstance(turn, dict):
            continue
        named = mine & set(_topics.keywords(str(turn.get("user") or "")))
        if not (len(named) >= 2 and len(named) * 2 >= len(mine)):
            continue
        answer = str(turn.get("bot") or "").strip()
        if not answer:
            continue
        if (_HEDGE.search(answer) or answer.endswith("?")
                or len(answer.split()) <= _topics.SHORT_TURN):
            return False
        if not asked & set(_naming_words(answer)):
            return False
        return bool(screen) and bool(screen & set(_naming_words(answer)))

def _a_time_for_the_job_itself(low):
    for pattern in (WHEN_THING, TIME_THING):
        found = pattern.search(low)
        if not found:
            continue
        said = re.findall(r"[a-z][a-z'-]*", found.group(1))
        if said and all(word in WHEN_QUALITY for word in said):
            return True
    return False

def _thing_is_a_quality(low):
    found = WHEN_THING.search(low)
    if not found:
        return False
    said = [word for word in re.findall(r"[a-z][a-z'-]*", found.group(1))]
    if not said or any(word not in WHEN_QUALITY for word in said):
        return False
    return _names_something_of_its_own(low, found.end())

def _names_something_of_its_own(low, start):
    for word in re.findall(r"[a-z][a-z'-]*", low[start:]):
        if (word in STOPWORDS or word in WHEN_VERB or word in POINTS_BACK or word in WHEN_QUALITY
                or word in WHEN_VAGUE or len(word) < 3):
            continue
        return True
    return False

def _when_thing(low, wide=False):
    found = WHEN_THING.search(low) or WHEN_THING_VERB.search(low)
    if not found:
        return ""
    said = keywords(found.group(1))
    if wide and said and all(word in WHEN_VAGUE for word in said):
        for word in re.findall(r"[a-z][a-z'-]*", low[found.end():])[:4]:
            words = keywords(word)
            if not words:
                continue
            if words[0] in WHEN_VAGUE:
                return ""
            said = words
            break
    for word in said:
        if word not in WHEN_VAGUE:
            return word
    return ""

def _the_one_asked(matching, rest):
    asked = content(rest) if rest else []
    if asked:
        for plan in reversed(matching):
            if any(_names_the_thing(plan, word) for word in asked):
                return plan
    return matching[-1] if matching else ""

def _ask_verb(low):
    found = WHEN_THING_VERB.search(low)
    return found.group(2) if found else ""

def _asks_the_end(low):
    verb = _ask_verb(low)
    return bool(verb) and stem(verb) in WHEN_END_ASK

def _asks_the_start(low):
    verb = _ask_verb(low)
    return bool(verb) and stem(verb) in WHEN_START_ASK

def _says_the_end(plan):
    return any(word.strip(".,!?;:").lower() in WHEN_END_WORD
               or stem(word.strip(".,!?;:")) in WHEN_END_WORD for word in (plan or "").split())

def _answers_the_end_asked(plan, low):
    verb = _ask_verb(low)
    if verb and _says_the_verb(plan, verb):
        return True
    if _asks_the_end(low):
        return _says_the_end(plan)
    return not _says_the_end(plan)

def _names_the_thing(plan, thing, memory=None):
    for word in content(plan):
        for key in [thing] + content(thing):
            if key == word or key in forms(word) or word in forms(key):
                return True
    return _about_kind(thing, plan, memory, phrase=True)

def _says_the_verb(plan, verb):
    verb = verb.lower()
    forms = {verb, verb + "s", verb + "ing", verb + "ed"}
    if verb.endswith("e"):
        forms |= {verb[:-1] + "ing", verb + "d"}
    if verb.endswith("y"):
        forms.add(verb[:-1] + "ied")
    if verb.endswith(("s", "x", "z", "ch", "sh")):
        forms.add(verb + "es")
    for other in VERB_ALSO.get(verb, ()):
        forms |= {other, other + "s", other + "ing", other + "ed"}
        if other.endswith("e"):
            forms |= {other[:-1] + "ing", other + "d"}
    return any(word.strip(".,!?;:").lower() in forms for word in plan.split())

VERB_ALSO = {
    "start": ("begin", "began", "beginning"),
    "begin": ("start", "starts", "starting", "started", "began"),
    "end": ("finish", "finishes", "finishing", "finished"),
    "finish": ("end", "ends", "ending", "ended", "finishes", "finishing", "finished"),
}

WHERE_WORK = re.compile(r"\bwhere\b[^.!?]*\bwork\b|\b(?:which|what)\s+(?:place|company|shop|"
                        r"school|hospital|office|site)\s+do\s+i\s+work\b", re.I)

def _job_reply(memory, where=False):
    known = user(memory)
    job, city = known.get("job"), known.get("city")
    place = str(known.get("workplace") or "").strip()
    if where and place:
        return "You work " + _place_phrase(place) + "."
    if job and city:
        said = _job_said(known)
        return pick([said + " in " + city + ".",
                     "You're in " + city + " — " + said[:1].lower() + said[1:] + "."],
                    memory)
    if job:
        return _job_said(known) + "."
    if city and where:
        return "You said you live in " + city + "."
    return _deny(memory, "job", pick(["You haven't told me what you do yet.",
                                      "I don't know your job — you haven't said."], memory))

def _yours(value):
    out = []
    for word in value.split():
        low = word.lower().strip(".,!?")
        out.append({"myself": "yourself", "my": "your", "me": "you", "i": "you",
                    "myself.": "yourself.", "our": "your", "us": "you"}.get(low, word))
    return " ".join(out)

WORK_CIRCUMSTANCE = frozenset("""
    part full time hours overtime nights days evenings weekends shifts days off call early late
    two three four five six seven all every a few several both
""".split())

def _a_circumstance(job):
    words = re.findall(r"[a-z0-9']+", job.lower())
    if not words:
        return True
    if any(word in WORK_CIRCUMSTANCE for word in words):
        return True
    last = words[-1]
    return last.endswith("s") and not last.endswith("ss")

def _job_said(known):
    job = _yours(str(known.get("job") or "").strip())
    frame = str(known.get("job_frame") or "").strip()
    preposition = frame.split(" ")[0]
    if frame == "was":
        if _a_circumstance(job):
            return "You did " + job
        return "You were " + _a(job)
    if frame == "work":
        if _a_circumstance(job):
            return "You work " + job
        return "You're " + _a(job)
    if preposition in ("in", "for", "on", "with"):
        return "You work " + frame + " " + job
    if preposition == "as":
        return "You work " + frame + " " + job
    if preposition == "at":
        if frame == "at":
            return "You work at " + job[:1].upper() + job[1:]
        return "You work " + frame + " " + job
    return "You told me you're " + _a(job)

def _place_phrase(place):
    place = str(place or "").strip()
    head, _, rest = place.partition(" ")
    if (head.lower() == "at" and rest and rest.lower() == rest
            and rest.split()[0].lower() not in ("the", "a", "an")):
        return "at " + rest[:1].upper() + rest[1:]
    return place

def _job_phrase(known):
    said = _job_said(known)
    low = said[:1].lower() + said[1:]
    head = "you told me "
    if low.startswith(head):
        low = low[len(head):]
    return low

def _places_reply(memory, low):
    known = user(memory)
    who = _asked_person(memory, low)
    if who:
        hers = _other_place(memory, who)
        if hers:
            return hers
        return ("You haven't said where your " + who
                + (" live." if who.lower().endswith("s") else " lives."))
    city = known.get("city")
    if re.search(r"\bborn\b", low):
        born = known.get("born")
        if isinstance(born, str) and born:
            return pick(["You were born in " + born + ".", born + " — you were born there."],
                        memory)
        origin = known.get("from")
        if isinstance(origin, str) and origin:
            return pick(["You haven't told me where you were born — you're from " + origin + ".",
                         "I don't know where you were born. You told me you're from " + origin + "."],
                        memory)
        return pick(["You haven't told me where you were born.",
                     "I don't know that one — you haven't said where you were born."], memory)
    if re.search(r"\bhometown\b", low):
        return _from_reply(memory)
    if GROWN_UP_ASK.search(low):
        return _grown_up_reply(memory)
    going = re.search(r"\bgoing\b|\btrip\b|\bholiday\b|\btravel", low)
    if (isinstance(city, str) and city and known.get("home") and not going
            and not re.search(r"\bfrom\b", low)):
        said_with = known.get("home")
        return "You live in " + (said_with if isinstance(said_with, str) else city) + "."
    if re.search(r"\bfrom\b|\bcome from\b", low):
        return _from_reply(memory)
    places = [p for p in (known.get("places") or []) if isinstance(p, str)]
    if going:
        away = [p for p in places if isinstance(city, str) and p != city] or places
        places = away
    if "city" in low or "town" in low:
        cities = [p for p in places if p.lower() not in extract.COUNTRIES]
        if cities:
            places = cities
    if not places:
        return _deny(memory, "place", "You haven't mentioned a place yet.")
    if re.search(r"\bwhere (?:do|does) (?:i|we) live\b|\bwhere am i (?:living|based)\b", low):
        origin = known.get("from")
        if isinstance(origin, str) and origin:
            return pick(["You haven't told me where you live — I know you're from " + origin + ".",
                         "I don't know where you live. You're from " + origin + ", that I do know."],
                        memory)
        return ("You haven't told me where you live. You mentioned " + places[0] + "."
                if len(places) == 1 else
                "You haven't told me where you live. You mentioned " + places[0] + ", then "
                + ", ".join(places[1:]) + ".")
    first = places[0]
    rest = [p for p in places[1:] if p != first]
    if rest:
        return "You said " + first + " first, then " + ", ".join(rest) + "."
    return "You mentioned " + first + "."

def _grown_up_reply(memory):
    known = user(memory)
    origin, city = known.get("from"), known.get("city")
    if isinstance(origin, str) and origin:
        return pick(["You grew up in " + origin + ".",
                     origin + " — that's where you grew up."], memory)
    if isinstance(city, str) and city:
        return pick(["You haven't said where you grew up — I know you live in " + city + ".",
                     "Not sure where you grew up. You mentioned " + city + " though."], memory)
    return pick(["You haven't said where you grew up yet.",
                 "I don't know that one — you haven't told me where you grew up."], memory)

def _from_reply(memory):
    known = user(memory)
    origin, city = known.get("from"), known.get("city")
    if origin and city and origin.lower() != city.lower():
        return pick(["You're from " + origin + " originally, and you live in " + city + " now.",
                     "You said you're from " + origin + ", and you're in " + city + " now."],
                    memory)
    if origin:
        return pick(["You're from " + origin + ".", origin + " — you told me you're from there."],
                    memory)
    if city:
        return pick(["You haven't said where you're from — I know you live in " + city + ".",
                     "Not sure where you're from. You mentioned " + city + " though."], memory)
    return pick(["You haven't said where you're from yet.",
                 "I don't know that one — you haven't said."], memory)

def _is_are(who):
    return " are " if _plural_person(who) else " is "

def _eats(who):
    return " eat" if _plural_person(who) else " eats"

def _does_not(who):
    return " don't" if _plural_person(who) else " doesn't"

def _they(who):
    low = str(who or "").lower().strip()
    if low in extract.SHE:
        return "she"
    if low in extract.HE:
        return "he"
    return "they"

def _a_diet_predicate(who, diet):
    said = str(diet or "").strip()
    if said.startswith("eats "):
        return (_eats(who) + " " + said[5:]).strip()
    if said.startswith("no "):
        return (_does_not(who) + " " + _diet_how(said) + " " + said[3:]).strip()
    return (_is_are(who) + said).strip()

def _their_pronoun(who):
    low = str(who or "").lower().strip()
    hers, his = low in extract.SHE, low in extract.HE
    if hers and not his:
        return "her"
    if his and not hers:
        return "him"
    return "them"

def _no_diet(who):
    if str(who or "").strip().lower() == "baby":
        return None
    return ("You haven't told me what " + (("your " + who) if who else "they") + _eats(who)
            + " \u2014 tell me and I'll plan the meals round it.")

def _a_condition_rules_out(condition):
    kept = condition if isinstance(condition, (list, tuple)) else [condition]
    return any(ack.CONDITION_FOOD.get(str(word).strip().lower()) for word in kept)

def _both_food_facts(who, allergies, diet):
    said = _allergy_is_their_food(who, allergies, only=False)
    them = _they(who)
    them = them[:1].upper() + them[1:]
    rest = _diet_sentence(who, diet)
    for lead in ((("Your " + who) if who else "They"), "They"):
        if rest.startswith(lead):
            rest = them + rest[len(lead):]
            break
    return said + " " + rest

def _allergy_is_their_food(who, allergies, only=True, low=""):
    owner = ("Your " + who) if who else "They"
    said = [str(a) for a in allergies if str(a).strip()]
    for one in said:
        named, thing = _what_the_food_has(str(low or ""), one) if low else ("", "")
        if named:
            return (named[:1].upper() + named[1:] + " has " + thing + " in it, so it's off the "
                    "table for " + _their_pronoun(who) + ".")
    ruled = said[0] if len(said) == 1 else "any of " + ", ".join(said)
    tail = ("" if only else "")
    if only:
        tail = " \u2014 that's all I have on food for " + _their_pronoun(who)
    return (owner + _is_are(who) + "allergic to " + ", ".join(said) + ", so nothing with "
            + ruled + " in it" + tail + ".")

def _what_the_food_has(low, ruled):
    for thing in re.split(r"\s*(?:,|\bor\b|\band\b)\s*", str(ruled or "")):
        thing = thing.strip().lower()
        if not thing:
            continue
        for phrase in FOOD_PHRASES.get(thing, ()):
            if re.search(r"\b" + re.escape(phrase) + r"s?\b", low):
                return phrase, thing
        for word in sorted(FOOD_HAS.get(thing, ()), key=len, reverse=True):
            if word == thing:
                continue
            if re.search(r"\b" + re.escape(word) + r"s?\b", low):
                return word, thing
    return "", ""

def _diet_is_their_food(who, diet, low="", plain=False):
    said = " ".join(str(low or "").lower().split())
    diet_low = " ".join(str(diet or "").lower().split())
    owner = ("Your " + who) if who else "They"
    if diet_low.startswith("no "):
        if plain:
            return None
        return (owner + " can't have " + diet_low[3:] + " \u2014 that's all I have on food for "
                + _their_pronoun(who) + ".")
    ruled = DIET_RULES_OUT.get(diet_low)
    if not ruled or (plain and re.search(r",|\bor\b|\band\b", ruled[0])):
        return None
    named, thing = _what_the_food_has(said, ruled[0]) if said else ("", "")
    if named:
        return (named[:1].upper() + named[1:] + " has " + thing + " in it, and " + owner.lower()
                + _is_are(who) + diet_low + ".")
    return (owner + _is_are(who) + diet_low + ", so nothing with " + ruled[0] + " in it"
            + ruled[1] + " \u2014 that's all I have on food for " + _their_pronoun(who) + ".")

def _other_fact(memory, key):
    for entry in others(memory):
        values = entry.get(key)
        if isinstance(values, list) and values:
            return entry.get("who") or "", values
    return "", []

DISLIKE_ASK = re.compile(
    r"\?|\b(?:what|how|which|any|ideas?|recipes?|give)\b", re.I)

def _last_answer(memory):
    turns = memory.get("turns")
    if not isinstance(turns, list) or not turns:
        return ""
    last = turns[-1]
    if not isinstance(last, dict) or last.get("module") != "answers":
        return ""
    reply = last.get("bot")
    return reply if isinstance(reply, str) else ""

def _one_half_of_the_dish(food, taste):
    if not isinstance(taste, dict):
        return False
    thing = str(taste.get("thing") or "").strip().lower()
    food = str(food or "").strip().lower()
    if not thing or not food or thing == food:
        return False
    joined = re.match(r"^(?P<one>.+?)\s+(?P<how>and|with|&)\s+(?P<two>.+)$", thing)
    if not joined:
        return False
    return bool(re.search(r"\b" + re.escape(food) + r"\b",
                          joined.group("one") + " " + joined.group("two")))

def _dislikes_here(text):
    out = []
    for food, at in guest.found(text):
        kind, who = extract.subject(text, at)
        out.append((food, kind or "user"))
    return out

def _a_dislike_told(text, memory):
    if not isinstance(text, str) or DISLIKE_ASK.search(text):
        return None
    if _about_this_chat(text, memory):
        return None
    tastes = read_tastes(text)
    if len(tastes) > 1:
        return None
    found = _dislikes_here(text)
    if any(_one_half_of_the_dish(food, taste) for food, _ in found for taste in tastes):
        return None
    foods = [food for food, kind in found if kind in ("user", "other")]
    alone = []
    if not foods and _last_answer(memory):
        alone = guest.turned_down_alone(text)
        foods = alone
    if not foods:
        return None
    previous = _last_answer(memory)
    if previous:
        revised = guest.revise(previous, foods)
        if revised:
            return revised
        try:
            if ruledout.takes_as_it_comes(text, memory):
                return None
        except Exception:
            pass
    a_pair = len(foods) > 1
    own = [guest.plain(food, a_pair) for food, kind in found if kind == "user"]
    own = own or [guest.plain(food) for food in alone]
    own = [food for food in own if food]
    if own:
        return guest.left_out(own)
    return None

STOPPED_SAID = re.compile(
    r"^(?:i|we)(?:'ve|ve|\s+have|\s+had)?\s+"
    r"(?:stopped|quit|gave up|given up|packed in|came off|gone off|got off|went off)\b", re.I)

NEGATED_SAID = re.compile(
    r"\b(?:not|never|no longer|any ?more|off|without)\b|n't\b", re.I)

def _the_take_back(memory, key):
    for turn in reversed(memory.get("turns") or []):
        line = str((turn or {}).get("user") or "") if isinstance(turn, dict) else ""
        if not line.strip():
            continue
        gone = (extract.denials(line) or {}).get(key)
        if gone:
            record = memory.get("denial") or {}
            if " ".join(line.split()) == str(record.get("said") or ""):
                dropped = record.get(key)
                if isinstance(dropped, list) and dropped:
                    gone = dropped[0]
                elif dropped:
                    gone = dropped
            return " ".join(line.split()), str(gone)
    return "", ""

def _a_take_back_said_back(line, gone):
    said = " ".join(str(line or "").split())
    if STOPPED_SAID.match(said):
        rest = re.sub(r"^(?:i|we)(?:'ve|ve|\s+have|\s+had)?\s+", "", said, flags=re.I)
        return "You told me you " + " ".join(rest.split()) + "."
    if str(gone).strip().lower() in ("diet", "dieting", "on a diet"):
        return "You told me you're not on a diet any more."
    if NEGATED_SAID.search(said):
        return _a_negation_said_back(gone, said)
    if gone in WAY_OF_EATING:
        return "You told me you stopped being " + _diet_words(gone) + "."
    if gone in PLAN_DIETS:
        return "You told me you stopped doing " + _diet_words(gone) + "."
    return "You told me you stopped " + _diet_words(gone) + "."

ANY_MORE = re.compile(r"\b(?:any ?more|anymore|no longer)\b", re.I)

def _a_negation_said_back(gone, line=""):
    value = str(gone or "").strip().lower()
    tail = " any more" if ANY_MORE.search(str(line or "")) else ""
    if not value:
        return "You told me you're not on a diet" + tail + "."
    if value.startswith("no "):
        return "You told me you don't " + _diet_how(value) + " " + value[3:] + tail + "."
    if value in WAY_OF_EATING:
        return "You told me you're not " + _diet_words(value) + tail + "."
    if value in PLAN_DIETS:
        return "You told me you're not doing " + _diet_words(value) + tail + "."
    return "You told me you're not " + _diet_words(value) + tail + "."

def _says_the_fact(line, key):
    if (extract.extract(line) or {}).get(key):
        return True
    low = " ".join(str(line or "").lower().split())
    if ASKING_ABOUT_IT.search(low) or PLANNING_IT.search(low):
        return False
    if A_CLAIM_OF_TELLING.match(low):
        return False
    return True

A_CLAIM_OF_TELLING = re.compile(
    r"^\W*(?:and\s+|also\s+|so\s+|but\s+|ok(?:ay)?\s+|look\s+|listen\s+|hey\s+)?"
    r"(?:i|we)\s+(?:already\s+|just\s+|did\s+|have\s+|had\s+|definitely\s+)?"
    r"(?:told|tell|mentioned|mention|said|say|talked|talk|spoke)\s+(?:you|u)\b", re.I)

ASKING_ABOUT_IT = re.compile(
    r"^(?:how|what|when|where|which|who|why|do|does|did|can|could|should|would|am|are|is|have|"
    r"has|will|if)\b|\?$|\b(?:do i|should i|can i|am i|did i|have i|will i)\b", re.I)

PLANNING_IT = re.compile(
    r"\b(?:we|i|you)\s+(?:need|needs|want|wants|ought|have to|has to|should)\s+to\b|"
    r"\b(?:thinking about|planning to|going to try|might|maybe|hoping to)\b", re.I)

def _the_line_about(memory, key, own=None):
    words = DENIAL_WORDS.get(key) or ()
    stems = DENIAL_STEMS.get(key) or ()
    if not words and not stems:
        return ""
    parts = [r"\b" + re.escape(word) + r"\b" for word in words]
    parts += [r"\b" + re.escape(stem) for stem in stems]
    wanted = re.compile("|".join(parts))
    for turn in reversed(memory.get("turns") or []):
        line = str((turn or {}).get("user") or "") if isinstance(turn, dict) else ""
        found = " ".join(re.findall(r"[a-z']+", line.lower()))
        if not found:
            continue
        if not wanted.search(found):
            continue
        if key in (extract.denials(line) or {}):
            continue
        if not _says_the_fact(line, key):
            continue
        if _said_of_someone_else(line, wanted):
            continue
        if own is not None and not own(line):
            continue
        return " ".join(line.split())
    return ""

def _said_of_someone_else(line, wanted):
    kinds = []
    for match in wanted.finditer(line):
        try:
            kinds.append(extract.subject(line, match.start())[0])
        except (ValueError, IndexError):
            return False
    return bool(kinds) and all(kind == "other" for kind in kinds)

def _deny(memory, key, denial, own=None):
    said = _the_line_about(memory, key, own)
    if said:
        return "You said: \"" + said + "\""
    return denial

def _their_own_diet(line):
    if extract.extract(line).get("diet") or extract.denials(line).get("diet"):
        return True
    if DIET_NOT_THEIRS.search(line):
        return False
    return bool(re.search(r"\b(?:i|we)\b[^.?!]*\b(?:eat|eats|eating|drink|drinks|diet)\w*\b",
                          line, re.I))

PLAN_DIETS = frozenset("""keto paleo atkins mediterranean low-carb slimming-world
weight-watchers intermittent-fasting whole30 whole-30 omad carnivore dukan south-beach fast-800
5:2 16:8 4:3""".split())

WAY_OF_EATING = frozenset("""vegan vegetarian veggie pescatarian flexitarian plant-based
raw gluten-free dairy-free""".split())

def _diet_words(value):
    return str(value).replace("-", " ")

DIET_NEGATED = re.compile(r"^(?:not|no|never|without|off)\s+(.{2,60})$", re.I)

def _a_diet_put_back(shown):
    bare = DIET_NEGATED.match(" ".join(str(shown or "").split()))
    if not bare:
        return None
    thing = bare.group(1).strip()
    words = thing.split()
    if not words or len(words) > 4 or words[0].lower() in ("more", "longer", "any", "the"):
        return None
    return thing

DIET_NOT_THEIRS = re.compile(
    r"\b(?:my|our|his|her|their)\s+[a-z]+\s+(?:is|was|are|were|has|had)\b|"
    r"\b(?:he|she|they)\b[^.?!]*\b(?:diet|keto|paleo|vegan|vegetarian)\b|"
    r"\b(?:i|we)\s+(?:was|were)\b|\bused to\b|\b(?:last|few)\s+(?:year|years|month|months)\b|"
    r"\byears?\s+ago\b|\b(?:thinking (?:about|of)|considering|might|maybe|planning to|going to try|"
    r"want to try)\b", re.I)

MEAL_WANTED = re.compile(
    r"\bwhat (?:do|should|shall|can|could|will) i (?:eat|have|cook|make|do for dinner)\b|"
    r"\bwhat'?s for (?:dinner|lunch|tea|supper|breakfast)\b|"
    r"\bwhat can we (?:eat|have|cook|make)\b|"
    r"\b(?:give|suggest|recommend) me something to eat\b", re.I)

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

AGE_COMPARE = re.compile(
    r"\bwho(?:'s|s| is| was)?\s+(?:the\s+)?(?:older|younger|eldest|oldest|youngest)\b|"
    r"\bwhich(?:\s+one|\s+of\s+(?:them|those|the\s+two))?\s+(?:is\s+|was\s+)?(?:the\s+)?"
    r"(?:older|younger|eldest|oldest|youngest)\b|"
    r"\b(?:am|is|are|was|were)\b[^.!?]{0,40}\b(?:older|younger) (?:than )?\b|"
    r"\bhow (?:much|many years)\s+(?:older|younger)\b|"
    r"\b(?:older|younger) (?:than )?(?:me|him|her|them)\b", re.I)

BARE_AGE_WHO = re.compile(
    r"^\W*(?:so|and|ok|okay|but|well)?[\s,]*who(?:'s|s| is| was)?\s+(?:the\s+)?"
    r"(?:older|younger|oldest|youngest|eldest)\b[^.?!]*$", re.I)

THE_AGE_GAP = re.compile(r"\bhow (?:much|many years)\s+(?:older|younger)\b", re.I)


WHICH_ONE_AGE_WHO = re.compile(
    r"^\W*(?:so|and|ok|okay|but|well)?[\s,]*which(?:\s+one|\s+of\s+(?:them|those|the\s+two))?"
    r"(?:'s|s| is| was)?\s+(?:the\s+)?(?:older|younger|oldest|youngest|eldest)\b[^.?!]*$", re.I)

PEOPLE_WORDS = re.compile(r"\b(?:she|her|hers|he|him|his|they|them|us|we|me|i|myself|mine)\b", re.I)

SOMEONE_ELSE = re.compile(r"\b(?:she|her|hers|he|him|his|they|them|us)\b", re.I)

def _about_people(low):
    if not (BARE_AGE_WHO.match(low) or PEOPLE_WORDS.search(low)):
        return False
    if re.search(r"\bthan\b", low):
        return bool(SOMEONE_ELSE.search(low))
    return True

def _age_compare(memory, low):
    if not AGE_COMPARE.search(low):
        return None
    said = memory.get("understood") or {}
    if said.get("kind") not in (None, "question"):
        return None
    aged = [e for e in others(memory) if e.get("age") is not None and e.get("who")]
    by_who = {}
    for entry in aged:
        by_who.setdefault((entry.get("who") or "").lower(), entry)
    kin = getattr(extract, "KIN", extract.RELATIONS)
    words = [w.lower() for w in
             re.findall(r"\b(?:my|our)\s+(" + "|".join(kin) + r")(?:'s|s)?\b", low)]
    if [w for w in words if w not in by_who]:
        return None
    if [w for w in re.findall(r"\bmy\s+([a-z']+)", low) if w not in kin]:
        return None
    named = []
    for word in words:
        if by_who[word] not in named:
            named.append(by_who[word])
    mine = user(memory).get("age")
    me = {"who": "", "age": mine} if mine is not None else None
    if len(named) >= 2:
        sides = named[:2]
    elif named and me is not None:
        sides = [me, named[0]]
    elif not named and me is not None and aged and _about_people(low):
        pointed = _pointed_at(aged, low)
        if pointed is None:
            return None
        sides = [me, pointed]
    elif (not named and me is None and len(by_who) == 2
          and not re.search(r"\b(?:me|myself|mine|i|im)\b", low)
          and (BARE_AGE_WHO.match(low) or WHICH_ONE_AGE_WHO.match(low))):
        sides = list(by_who.values())
    elif (not named and me is None and len(by_who) == 2 and THE_AGE_GAP.search(low)
            and not re.search(r"\b(?:me|myself|mine)\b", low)
            and _the_pronoun_is_one_of_the_two(by_who, low)):
        sides = list(by_who.values())
    else:
        return None
    try:
        ages = [int(s.get("age")) for s in sides]
    except (TypeError, ValueError):
        return None
    first, second = sides
    if ages[0] == ages[1]:
        if not first.get("who"):
            return "Neither of you - you're both " + str(ages[0]) + "."
        return "Neither of them - your " + str(first["who"]) + " and your " + str(second["who"]) + " are both " + str(ages[0]) + "."
    younger = re.search(r"\b(?:younger|youngest)\b", low) is not None
    winner, other = (0, 1) if (ages[0] > ages[1]) != younger else (1, 0)
    win, lose = sides[winner], sides[other]
    gap = abs(ages[0] - ages[1])
    years = "year" if gap == 1 else "years"
    if re.search(r"\bhow (?:much|many years)\s+(?:older|younger)\b", low):
        if not first.get("who"):
            return str(gap) + " " + years + ": you're " + str(ages[0]) + " and your " + str(second["who"]) + " is " + str(ages[1]) + "."
        return str(gap) + " " + years + ": your " + str(first["who"]) + " is " + str(ages[0]) + " and your " + str(second["who"]) + " is " + str(ages[1]) + "."
    theirs = "your" if not lose.get("who") else "your " + str(lose["who"]) + "'s"
    said = re.search(r"\b(youngest|eldest|oldest)\b", low)
    if said:
        word = "the " + said.group(1)
    else:
        word = "older" if ages[winner] > ages[other] else "younger"
    if not win.get("who"):
        return "You're " + word + " - " + str(ages[winner]) + " to " + theirs + " " + str(ages[other]) + "."
    return "Your " + str(win["who"]) + "'s " + word + " - " + str(ages[winner]) + " to " + theirs + " " + str(ages[other]) + "."

WHICH_FIRST_ASK = re.compile(
    r"\b(?:which|who|whose|what)\s+(?:one\s+|ones\s+|of\s+them\s+|of\s+those\s+|of\s+the\s+two\s+)?"
    r"(?:is\s+|are\s+|comes?\s+|come\s+|happens?\s+|happen\s+|would\s+be\s+|will\s+be\s+)?"
    r"(?:up\s+)?(?:first|sooner|earliest|earlier)\b", re.I)

WHICH_FIRST_WORDS = frozenset("""which who whose what one ones of them those the two is are come
    comes happen happens would will be up first sooner earliest earlier next then so do does you
    think again now really actually please and but well hmm oh ah then just it that this both""".split())

MONTH_SAID = re.compile(
    r"\b(?:in|on|of|by|until|till|before|after|from|during|early|late|mid|next|this|that|the)\s+"
    r"(?:" + MONTH_ALT + r")\b|\b(?:" + MONTH_ALT + r")\s+\d{1,2}(?:st|nd|rd|th)?\b|"
    r"\b\d{1,2}(?:st|nd|rd|th)?\s+(?:of\s+)?(?:" + MONTH_ALT + r")\b", re.I)

def _the_day_a_plan_names(plan):
    low = " ".join(str(plan or "").lower().split())
    today = datetime.date.today()
    found = MONTH_SAID.search(low)
    if found:
        short = MONTH_WORD.search(found.group(0))
        name = [m for m in MONTH_ORDER if m.startswith(short.group(0)[:3])] if short else []
        if not name:
            return None
        index = MONTH_ORDER.index(name[0]) + 1
        day = 1
        near = (re.search(r"\b(\d{1,2})(?:st|nd|rd|th)?\b[^.?!]{0,12}" + re.escape(name[0]),
                          low)
                or re.search(re.escape(name[0]) + r"\b[^.?!]{0,12}?\b(\d{1,2})(?:st|nd|rd|th)?\b",
                             low))
        if near and 1 <= int(near.group(1)) <= 31:
            day = int(near.group(1))
        for year in (today.year, today.year + 1):
            try:
                when = datetime.date(year, index, day)
            except ValueError:
                continue
            if when >= today:
                return (when - today).days
        return None
    day = WEEKDAY_WORD.search(low)
    if day and not DATE_PHRASE.search(low):
        return (WEEK.index(day.group(0)) - today.weekday()) % 7
    return None

def _the_plans_in_date_order(memory):
    known = user(memory)
    held = [p for p in (known.get("plans") or []) if isinstance(p, str) and p.strip()]
    latest = known.get("plan")
    if isinstance(latest, str) and latest.strip() and latest not in held:
        held.append(latest)
    for entry in others(memory):
        who = str(entry.get("who") or "").strip()
        day = str(entry.get("birthday") or "").strip()
        if not (who and day):
            continue
        if any("birthday" in plan.lower() and re.search(r"\b" + re.escape(who) + r"s?\b",
                                                        plan.lower())
               for plan in held):
            continue
        link = "on " if re.search(r"\d", day) else "in "
        held.append("my " + who + "s birthday is " + link + day)
    dated = []
    seen = set()
    for plan in held:
        days = _the_day_a_plan_names(plan)
        if days is None:
            continue
        said = plan_sentence(plan, plan_line(memory, plan)).rstrip(" .!?")
        if not said:
            continue
        key = (days, said.lower())
        if key in seen:
            continue
        seen.add(key)
        dated.append((days, said))
    dated.sort(key=lambda pair: pair[0])
    return dated

def _which_comes_first(memory, low):
    found = WHICH_FIRST_ASK.search(low)
    if not found:
        return None
    said = memory.get("understood") or {}
    if said.get("kind") not in (None, "question"):
        return None
    rest = (low[:found.start()] + " " + low[found.end():])
    if [w for w in re.findall(r"[a-z']+", rest) if w not in WHICH_FIRST_WORDS]:
        return None
    dated = _the_plans_in_date_order(memory)
    if len(dated) < 2:
        return None
    first = dated[0][1]
    later = [said[:1].lower() + said[1:] for _, said in dated[1:4]]
    if dated[1][0] == dated[0][0]:
        return "Both land on the same day: " + first[:1].lower() + first[1:] + " and " + \
            later[0] + "."
    tail = ", then ".join(later)
    return first + ", so that one is first \u2014 then " + tail + "."

def _the_pronoun_is_one_of_the_two(by_who, low):
    if re.search(r"\b(?:she|her|hers)\b", low):
        fits = extract.SHE
    elif re.search(r"\b(?:he|him|his)\b", low):
        fits = extract.HE
    else:
        return True
    return any((entry.get("who") or "").lower() in fits for entry in by_who.values())


def _pointed_at(aged, low):
    fits = None
    if re.search(r"\b(?:she|her|hers)\b", low):
        fits = extract.SHE
    elif re.search(r"\b(?:he|him|his)\b", low):
        fits = extract.HE
    if fits:
        for entry in reversed(aged):
            if (entry.get("who") or "").lower() in fits:
                return entry
        return None
    return aged[-1]

LIMIT_LIKE = re.compile(
    r"\b(?:pregnan\w*|expecting|we'?re having a baby|having a baby)\b"
    r"|\ballerg\w*|\bintoleran\w*|\bcoeliac\b|\bceliac\b|\bibs\b|\bcrohn'?s?\b"
    r"|\bdiabet\w*|\bgout\b|\breflux\b|\bhigh cholesterol\b|\bkidney\b"
    r"|\bvegan\b|\bvegetarian\b|\bpescatarian\b|\bon a diet\b|\b\w+[- ]free\b"
    r"|\b(?:can'?t|cannot|can not|don'?t|dont|do not|never|no longer|stopped|avoid\w*)\b"
    r"[^.!?]{0,24}?\b(?:eat|drink|have|haveing|having|touch|take|dairy|meat|gluten|sugar|"
    r"alcohol|salt)\b", re.I)

MORE_FOODS = frozenset("""sesame soya soy soya-bean mustard celery sulphites lupin molluscs
shellfish kiwi strawberry strawberries banana bananas pineapple tomato tomatoes chocolate
sugar caffeine msg sulphite""".split())

def _a_food(value):
    word = str(value or "").strip().lower()
    if not word:
        return False
    if word in MORE_FOODS:
        return True
    if any(word in family for family in cooking.FAMILIES.values()):
        return True
    if word in cooking.CHEESES or re.search(r"\b" + cooking.FOOD + r"\b", word):
        return True
    return False

def _diet_food(diet):
    low = str(diet or "").strip().lower()
    if low in DIET_FOOD:
        return DIET_FOOD[low]
    if low.startswith("no "):
        return (low[3:].strip(),) if low[3:].strip() else ()
    if low.endswith(" free"):
        return (low[:-5].strip(),) if low[:-5].strip() else ()
    return ()

def _said_a_limit(memory):
    known = user(memory)
    if known.get("allergies") or known.get("condition") or known.get("diet"):
        return True
    for turn in (memory.get("turns") or [])[-12:]:
        said = str((turn or {}).get("user") or "")
        if said and LIMIT_LIKE.search(said):
            return True
    return False

def _said_list(items):
    items = [str(item) for item in items]
    if not items:
        return ""
    if len(items) < 2:
        return items[0]
    if len(items) == 2:
        return items[0] + " and " + items[1]
    return ", ".join(items[:-1]) + " and " + items[-1]

def _limit_reply(memory, low=""):
    known = user(memory)
    allergies = [str(a) for a in (known.get("allergies") or []) if str(a).strip()]
    conditions = known.get("condition") or []
    if isinstance(conditions, str):
        conditions = [conditions]
    conditions = [str(c) for c in conditions if str(c).strip()]
    diet = str(known.get("diet") or "").strip()
    foods = [allergy for allergy in allergies if _a_food(allergy)]
    if not foods and not conditions and not diet:
        if not FOOD_ASK.search(low):
            return None
        if _said_a_limit(memory):
            return None
        return ("You haven't told me anything you can't have. Say what to keep out of your food "
                "and I'll stick to it.")
    clauses = []
    if foods:
        clauses.append("nothing with " + _said_list(foods) + " in it \u2014 you're allergic to "
                       + ("them" if len(foods) > 1 or foods[0].endswith("s") else "it"))
    if conditions:
        ruled = [ack.CONDITION_FOOD.get(condition.lower()) for condition in conditions]
        if ruled and all(ruled):
            clauses.append("nothing with " + _said_list(ruled) + " in it \u2014 you're "
                           + _said_list(conditions))
        else:
            clauses.append("you're " + _said_list(conditions))
    if diet:
        ruled = _diet_food(diet)
        if ruled and all(ruled) and not diet.lower().startswith("no "):
            clauses.append("nothing with " + _said_list(ruled) + " in it \u2014 you're " + diet)
        else:
            clauses.append("you don't " + _diet_how(diet) + " " + diet[3:] if diet.startswith("no ") else
                           "you're " + diet)
    said = clauses[0]
    if len(clauses) == 2:
        said += ", and " + clauses[1]
    elif len(clauses) > 2:
        said += ", " + ", ".join(clauses[1:-1]) + ", and " + clauses[-1]
    said = said[:1].upper() + said[1:] + "."
    if _same_as_last(said, memory):
        said = _vary(["Still this: " + said[0].lower() + said[1:],
                      "That hasn't changed: " + said[0].lower() + said[1:],
                      "Same answer: " + said[0].lower() + said[1:]], memory)
    return said

AN_ASK_AT_THE_END = re.compile(
    r"(?:^|[\s,;])(?:what|which|how|where|when|who|why)\b[^.!?]*$"
    r"|(?:^|[\s,])(?:can|could|should|shall|would|will|do|does|did|is|are|am)\s+"
    r"(?:i|we|you|he|she|they|it)\b[^.!?]*$", re.I)

HEDGED = re.compile(
    r"\b(?:don'?t know enough|beyond what i know|not sure about that one|"
    r"rather not guess|a (?:quick )?search\b|searching for it|look it up)\b", re.I)


def _the_answer_the_ask_gets(text, memory):
    from ..modules import answers
    fresh = {"turns": [], "aside": True}
    for key in ("user", "others", "facts_log"):
        if key in memory:
            fresh[key] = memory[key]
    try:
        reply = answers.respond(text, fresh) or ""
    except Exception:
        return ""
    said = " ".join(str(reply).split())
    if not said or HEDGED.search(said):
        return ""
    return said


def _the_ask_beats_the_receipt(text, memory):
    if not isinstance(text, str) or "?" in text:
        return False
    if not AN_ASK_AT_THE_END.search(" ".join(text.split())):
        return False
    return bool(_the_answer_the_ask_gets(text, memory))


def _a_diet_told(text, memory, low):
    if not isinstance(text, str) or "?" in text:
        return None
    if _the_ask_beats_the_receipt(text, memory):
        return None
    if _about_this_chat(text, memory) or OTHER_ASK.search(low) or REMINDER_MID.search(low):
        return None
    found = extract.extract(text)
    if found.get("diet") or found.get("no_meat") or found.get("allergies"):
        return None
    named = [who for who in (found.get("people") or []) if isinstance(who, str)]
    for entry in found.get("others") or []:
        diet = entry.get("diet")
        if not diet:
            continue
        who = entry.get("who") or _person_from_pronoun(text, memory, named)
        return _diet_sentence(who, diet)
    return None

def _object_pronoun(who, known=None):
    said = _pronoun_for(who, known)
    return {"she": "her", "he": "him"}.get(said, "them")

def _who_the_pronoun_means(low, memory, pronoun):
    fits = PRONOUN_FITS.get(str(pronoun or "").lower(), ())
    allowed = set()
    for key in fits:
        allowed |= set(extract.HE if key == "he" else extract.SHE)
    if not allowed:
        return ""
    people = [who for who in (user(memory).get("people") or []) if isinstance(who, str)]
    people += [str(entry.get("who")) for entry in others(memory) if entry.get("who")]
    for who in reversed(people):
        if who in allowed:
            return who
    record = _topics.about(memory)
    if record is None:
        return ""
    who = str(record.get("who") or "")
    titled = ""
    for entry in others(memory):
        if str(entry.get("who") or "") != who:
            continue
        title = str(entry.get("name") or "").split(" ")[0].strip(".").lower()
        if title in extract.TITLE_GENDER:
            titled = extract.TITLE_GENDER[title]
    if titled:
        return who if titled in fits else ""
    if who and who not in extract.SHE and who not in extract.HE \
            and len({said for said in people if said}) == 1:
        return who
    return ""

def _a_relations_name_reply(memory, low, text=""):
    if not isinstance(low, str):
        return None
    match = OTHER_NAME_ASK.search(low)
    who = ""
    if match:
        groups = ("who1", "who2", "who3", "who4", "who5", "who6", "who7", "who8", "who9",
                  "who10", "who11")
        who = next((match.group(group) for group in groups
                    if match.groupdict().get(group)), "")
        who = (who or "").lower()
        if (who.endswith("s") and (who[:-1] in extract.KIN_WORDS
                                   or who[:-1] in extract.ALONE_PERSON)):
            who = who[:-1]
        who = _with_an_in_law(who, low)
        group = _the_group(who)
        if group:
            if who in A_ONE_PERSON_WORD:
                narrowed = _which_one_of_them(memory, who)
                if narrowed:
                    return narrowed
            together = _what_the_group_is_called(group, memory)
            if together:
                return together
            if _the_group_was_said(who, memory):
                return None
            return _vary(["You haven't told me what your " + _the_group_word(who) + " are called.",
                          "I don't have any names for your " + _the_group_word(who) + " yet.",
                          "You've not said what your " + _the_group_word(who)
                          + " are called."], memory)
        if (who not in extract.KIN_WORDS and who not in extract.ALONE_PERSON
                and not extract.an_in_law(who)):
            return None
        if (who not in extract.RELATIONS and not extract.an_in_law(who)
                and not _a_person_in_the_store(memory, who)):
            return None
    else:
        point = PRONOUN_NAME_ASK.search(low)
        if not point:
            return None
        pronoun = next((point.group(group) for group in
                        ("pos", "sub", "obj", "pos2", "sub2", "obj2", "pos3", "pos4")
                        if point.groupdict().get(group)), "")
        if pronoun in ("their", "they", "them"):
            together = _everyone_they_mean(memory)
            if together:
                return together
        who = _who_the_pronoun_means(low, memory, pronoun).lower()
        if not who:
            named_pet = _the_one_animal_with_a_name(memory)
            if named_pet:
                return named_pet
            return None
    told = others(memory)
    mine = [entry for entry in told if str(entry.get("who") or "").lower() == who]
    named = [entry for entry in mine if entry.get("name")]
    if named:
        name = _called(named[-1].get("name"))
        return _vary(["Your " + who + " is called " + name + ".",
                      name + " \u2014 your " + who + ", you told me.",
                      "You said your " + who + " is called " + name + "."], memory)
    for entry in told:
        pair = [word.strip() for word in str(entry.get("who") or "").lower().split(" and ")]
        pair_names = [str(one) for one in entry.get("names") or []]
        if ((len(pair) > 1 and who in pair) or _canon_relation(who) in _relations_of(
                entry.get("who"))) and len(pair_names) > 1:
            return ("You told me your " + str(entry["who"]) + " are "
                    + _a_list_of_names(pair_names) + " - which one is your " + who + "?")
    in_law_of_the_same = [entry for entry in told
                          if extract.an_in_law(entry.get("who"))
                          and str(entry.get("who") or "").lower().startswith(who + " in law")]
    if mine or in_law_of_the_same or who in [str(person).lower() for person in
                                             (user(memory).get("people") or [])]:
        return "You haven't told me your " + who + "'s name."
    return None

def _the_group(who):
    return PERSON_GROUP.get(_the_group_word(who), ())

def _in_group(who, group):
    who = str(who or "").lower()
    return (who in group or CHILD_OF.get(who, "") in group
            or (who.endswith("s") and who[:-1] in group))

def _the_people(entries):
    words = []
    counts = {}
    for entry in entries:
        who = str(entry.get("who") or "").lower()
        counts[who] = counts.get(who, 0) + 1
        if who not in words:
            words.append(who)
    spoken = []
    for word in words:
        if counts[word] > 1 and not word.endswith("s"):
            word += "s"
        spoken.append(word)
    return _and_list(spoken)

A_ONE_PERSON_WORD = frozenset("""child kid baby twin parent grandchild grandparent boy girl lad
lass teenager""".split())

def _which_one_of_them(memory, who):
    group = _relations_of(who)
    mine = [entry for entry in others(memory) if isinstance(entry, dict)
            and _in_the_group(entry.get("who"), group)]
    said = []
    for entry in mine:
        names = [str(one) for one in (entry.get("names") or []) if str(one).strip()]
        if len(names) > 1:
            said.extend(_called(one) for one in names)
        elif entry.get("name"):
            said.append(_called(str(entry["name"])))
    if len(said) < 2:
        return None
    return ("You told me your " + _the_people(mine) + " are "
            + _a_list_of_names(said) + " - which one do you mean?")

def _what_the_group_is_called(group, memory):
    mine = [entry for entry in others(memory)
            if isinstance(entry, dict) and _in_group(entry.get("who"), group)]
    if not mine:
        return None
    named = [entry for entry in mine if entry.get("name") or entry.get("names")]
    unnamed = [entry for entry in mine if not (entry.get("name") or entry.get("names"))]
    if not named:
        many = len(mine) > 1 or any(str(entry.get("who") or "").lower() in PLURAL_PEOPLE
                                    for entry in mine)
        return ("You've told me about your " + _the_people(mine) + ", not what "
                + ("they are" if many else "he or she is") + " called.")
    said = []
    paired = False
    for entry in named:
        names = [str(one) for one in (entry.get("names") or []) if str(one).strip()]
        if len(names) > 1:
            said.extend(_called(one) for one in names)
            paired = True
        else:
            said.append(_called(str(entry.get("name") or names[0])))
    names = _and_list(said)
    if paired and not unnamed:
        return "You told me your " + _the_people(mine) + " are called " + names + "."
    if not unnamed:
        if len(said) > 1:
            return names + " \u2014 your " + _the_people(mine) + "."
        return names + ", your " + _the_people(mine) + "."
    return names + ", and your " + _the_people(unnamed) + " you haven't named."

def _everyone_they_mean(memory):
    told = [entry for entry in others(memory) if isinstance(entry, dict)]
    if len(told) < 2 or not all(_in_group(entry.get("who"), CHILD_RELATIONS)
                                for entry in told):
        return None
    return _what_the_group_is_called(CHILD_RELATIONS, memory)

def _who_is_the_name_reply(memory, low):
    if not isinstance(low, str):
        return None
    match = WHO_IS_NAME_ASK.search(low)
    if not match:
        return None
    parts = match.groupdict()
    said = (parts.get("name1") or parts.get("name2") or parts.get("name3")
            or parts.get("name4") or "").strip().lower()
    asked_who = (parts.get("who3") or parts.get("who4") or "").strip().lower()
    if asked_who.endswith("s") and asked_who[:-1] in extract.RELATIONS:
        asked_who = asked_who[:-1]
    if not said:
        return None
    if parts.get("name1") or parts.get("name2"):
        group = "name1" if parts.get("name1") else "name2"
        tail = low[match.end(group):].strip(" \t?.,!;:'\"")
        if tail and not set(tail.split()) <= NAME_ASK_TAIL:
            return None
    for entry in reversed(others(memory) or []):
        if not isinstance(entry, dict):
            continue
        name = str(entry.get("name") or "").strip()
        who = str(entry.get("who") or "").strip().lower()
        if not name or not who or name.lower() != said:
            continue
        proper = _tidy_name(name)
        if asked_who:
            same = CONCEPTS.get(asked_who, asked_who) == CONCEPTS.get(who, who)
            if same:
                return _vary(["Yes - " + proper + " is your " + who + ".",
                              "That's right: " + proper + " is your " + who + "."], memory)
            return "No - " + proper + " is your " + who + "."
        return _vary([proper + " is your " + who + ".",
                      proper + " \u2014 your " + who + ", you told me.",
                      "That's " + proper + ", your " + who + "."], memory)
    for entry in reversed(others(memory) or []):
        if not isinstance(entry, dict):
            continue
        names = [str(one).strip() for one in (entry.get("names") or []) if str(one).strip()]
        who = str(entry.get("who") or "").strip().lower()
        if len(names) < 2 or not who or not any(one.lower() == said for one in names):
            continue
        proper = _tidy_name(next(one for one in names if one.lower() == said))
        if asked_who:
            same = CONCEPTS.get(asked_who, asked_who) in _relations_of(who)
            if same:
                return _vary(["Yes - " + proper + " is one of your " + who + ".",
                              "That's right: " + proper + " is among your " + who + "."],
                             memory)
            return proper + " is one of your " + who + ", not your " + asked_who + "."
        return _vary([proper + " is one of your " + who + " - you told me your " + who
                      + " are " + _a_list_of_names(names) + ".",
                      "One of your " + who + ": you said your " + who + " are "
                      + _a_list_of_names(names) + "."], memory)
    for pet in (user(memory).get("pets") or []):
        if not isinstance(pet, dict):
            continue
        name = str(pet.get("name") or "").strip()
        if not name or name.lower() != said:
            continue
        proper = _tidy_name(name)
        animal = str(pet.get("animal") or "pet").strip().lower()
        if asked_who:
            same = CONCEPTS.get(asked_who, asked_who) == CONCEPTS.get(animal, animal)
            if same:
                return _vary(["Yes - " + proper + " is your " + animal + ".",
                              "That's right - " + proper + " is your " + animal + "."],
                             memory)
            return proper + " is your " + animal + ", not your " + asked_who + "."
        return _vary([proper + " is your " + animal + ".",
                      "That's " + proper + ", your " + animal + "."], memory)
    return None

def _kids_reply(memory, low):
    if not _kids_ask(low):
        return None
    held = user(memory).get("kids")
    if isinstance(held, int) and held == 0 and not isinstance(held, bool):
        return _vary(["You told me you don't have any kids.",
                      "None \u2014 you said you don't have any.",
                      "You said you haven't got any kids."], memory)
    if held is None:
        named = [entry for entry in (others(memory) or [])
                 if isinstance(entry, dict) and str(entry.get("who") or "").lower()
                 in CHILD_RELATIONS]
        if not named:
            named = [{"who": who} for who in (user(memory).get("people") or [])
                     if str(who).lower() in CHILD_RELATIONS]
        if named:
            who = str(named[0].get("who") or "child").lower()
            return _vary(["You've mentioned your " + who
                          + " \u2014 how many have you got altogether?",
                          "I know about your " + who + ", but not a number. How many have you "
                          "got in all?"], memory)
        return _vary(["You haven't told me how many kids you have yet.",
                      "I don't have a number from you \u2014 how many have you got?",
                      "You haven't said how many children you've got."], memory)
    count = int(held)
    if count == 1:
        return _vary(["You've got one kid.", "One kid, as you told me.",
                      "You said you've got one kid."], memory)
    word = NUMBER_WORDS.get(count, str(count))
    kids = "children" if count == 2 else "kids"
    return _vary(["You've got " + word + " " + kids + ".",
                  word.capitalize() + " " + kids + " \u2014 that's what you told me.",
                  "You said you've got " + word + " " + kids + "."], memory)

def _and_list(words):
    words = [str(word) for word in words if word]
    if len(words) < 2:
        return "".join(words)
    return ", ".join(words[:-1]) + " and " + words[-1]

def _lines_a_person_moved(memory):
    last = {}
    moved = set()
    for entry in memory.get("facts_log") or ():
        if not isinstance(entry, dict):
            continue
        value = entry.get("value")
        if not isinstance(value, dict):
            continue
        who = str(value.get("who") or "").lower()
        if not who:
            continue
        text = " ".join(str(entry.get("text") or "").lower().split())
        if not text:
            continue
        for key, held in value.items():
            if key == "who" or isinstance(held, (list, dict)):
                continue
            slot = (who, key)
            older = last.get(slot)
            if older and older[0] != str(held).lower():
                moved.add(older[1])
            last[slot] = (str(held).lower(), text)
    return moved

def _only_a_pointer(flat):
    if SAME_FACT_ABOUT.match(flat):
        return True
    for shape in (SAME_FACT_AGAINST, SAME_FACT_AGAINST_PRONOUN):
        match = shape.match(flat)
        if not match:
            continue
        rest = (match.groupdict().get("rest") or "").strip(" ?!.")
        if not rest or rest.split()[0] in NEGATIVE_TAIL:
            return True
    return False

def _a_known_person(memory, who):
    family = _the_same_person(who)
    entry = {}
    for known in others(memory):
        if str(known.get("who") or "").lower() not in family:
            continue
        for key, value in known.items():
            if key == "who":
                continue
            if isinstance(value, list) and isinstance(entry.get(key), list):
                entry[key] += [item for item in value if item not in entry[key]]
            else:
                entry[key] = value
    pattern = _the_name_pattern(who)
    carried = re.compile(r"^\s*(?:and\s+|also\s+)?(?:she|he|they|her|him|them|his|hers|their)"
                         r"(?:'s|'re|s|re)?\b", re.I)
    lines = []
    moved = _lines_a_person_moved(memory)
    current = ""
    for turn in _every_line(memory):
        line = str(turn.get("user") or "")
        if not line:
            continue
        named_here = _a_relation_in(line)
        if named_here:
            current = named_here
        if _asks(line) or _about_this_chat(line) or ABOUT_PERSON_ASK.search(line.lower()):
            continue
        if ((pattern.search(line) and not A_PROGRAMME_IS_ON.search(line))
                or (current in family and carried.match(line))):
            flat = " ".join(line.lower().split()).strip(" ?!.")
            if flat in moved:
                continue
            if _only_a_pointer(flat):
                continue
            lines.append(line)
            given = _a_name_in_a_pronoun_line(line)
            if given and not entry.get("name"):
                entry["name"] = given
                lines = []
    if entry.get("name"):
        lines = [one for one in lines if not _only_the_name(one, entry["name"], who)]
    return entry, lines

def _only_the_name(line, named, who):
    person = set(_the_same_person(who))
    drop = ({"my", "our", "your", "the", "is", "was", "name", "names", "called", "and", "she",
             "he", "her", "his", "they", "their", "them", "also", "s"} | person)
    words = set(re.findall(r"[a-z0-9]+", str(line or "").lower()))
    words = {word[:-1] if word.endswith("s") and word[:-1] in (drop | person) else word
             for word in words}
    return words - drop == {str(named or "").lower()}

def _a_name_in_a_pronoun_line(line):
    match = re.match(r"^\s*(?:and\s+|also\s+)?(?:his|her|their)\s+names?\s*"
                     r"(?:'s|is\s+|are\s+)?(?P<name>[a-z]{2,})\b", str(line or ""), re.I)
    if not match:
        return ""
    name = match.group("name").lower()
    if name in NOT_A_NAME:
        return ""
    return name

NOT_A_NAME = frozenset("""a an the not no still same old different changed change hard difficult
important complicated long short funny strange odd weird right wrong fine ok okay good bad""".split())

def _named_back(who, line):
    def whose(match):
        word = match.group(0).lower()
        head = "your " + who
        if word.endswith("re"):
            return head + " are"
        if word.endswith("s") and not word.endswith("ss"):
            return head + " is"
        return head

    def belonging(match):
        return "your " + who + ("'" if _plural_person(who) else "'s")

    line = str(line or "")
    if not re.search(r"\byour\s+" + re.escape(who) + r"\b", line, re.I):
        line = re.sub(r"^(?:and\s+)?(?:she|he|they)(?:'s|'re|s|re)?\b", whose, line, re.I)
        line = re.sub(r"^(?:and\s+)?(?:his|her|their)\b", belonging, line, re.I)
    return line

def _a_relation_in(line):
    low = str(line or "").lower()
    for relation in extract.RELATIONS:
        for hit in re.finditer(r"\b" + relation + r"s?\b", low):
            rest = low[hit.end():]
            if rest.startswith("'s") or rest.startswith("s'"):
                rest = rest.split("'", 1)[1][1:]
            words = rest.split()
            if words and words[0].strip(".,!?;:") in extract.COMPOUND_AFTER:
                continue
            return relation
    return ""

def _person_clauses(who, entry):
    be = "are" if _plural_person(who) else "is"
    clauses = []
    age = entry.get("age")
    if isinstance(age, int) and not isinstance(age, bool):
        clauses.append(be + " " + str(age))
    allergies = [str(one) for one in (entry.get("allergies") or []) if one]
    if allergies:
        clauses.append(be + " allergic to " + _and_list(allergies))
    condition = entry.get("condition")
    if isinstance(condition, list):
        condition = str(condition[0]) if condition else ""
    if str(condition or "").strip():
        clauses.append(be + " " + str(condition).strip())
    diet = str(entry.get("diet") or "").strip()
    if diet:
        clauses.append(_a_diet_predicate(who, diet))
    dislikes = [str(one) for one in (entry.get("dislikes") or []) if one]
    if dislikes:
        clauses.append((_does_not(who) + " like " + _and_list(dislikes)).strip())
    return clauses

def _date_written_as_a_date(value):
    said = str(value or "")
    for month in extract.MONTHS:
        said = re.sub(r"\b" + month + r"\b", month[:1].upper() + month[1:], said, flags=re.I)
    ordinal = re.match(r"^(\d{1,2}(?:st|nd|rd|th))\s+([A-Z][a-z]+)$", said)
    if ordinal:
        said = "the %s of %s" % (ordinal.group(1), ordinal.group(2))
    return said

def _pronoun_person(text, memory):
    low = str(text or "").lower()
    if not re.search(r"\b(?:her|him|them|she|he|they)\b", low):
        return ""
    who = _person_from_pronoun(text, memory)
    if not who or _plural_person(who):
        return who
    if re.search(r"\b(?:her|she)\b", low) and who not in extract.SHE:
        return ""
    if re.search(r"\b(?:him|he)\b", low) and who not in extract.HE:
        return ""
    return who

def _a_line_about(memory, who):
    for turn in reversed(_every_line(memory)):
        line = str(turn.get("user") or "").strip()
        if (not line or "?" in line or _asks(line)
                or ABOUT_PERSON_ASK.search(line.lower())):
            continue
        if _only_a_pointer(" ".join(line.lower().split()).strip(" ?!.")):
            continue
        if _the_word_for_them(who).search(line):
            return line
    return None

OWNED_ASK = re.compile(
    r"\b(?:what|which)\s+(?P<a>[a-z][a-z-]*)\s+(?:do|did|does)\s+(?:i|u|you)\s+"
    r"(?:drive|ride|use|have|own)\b"
    r"|\b(?:what|which)\s+(?P<b>[a-z][a-z-]*)\s+(?:have|has)\s+(?:i|u|you)\s+"
    r"(?:got|had|have|owned|driven|ridden|used)\b"
    r"|\b(?:what|which)\s+(?P<c>[a-z][a-z-]*)\s+(?:is|was)\s+mine\b"
    r"|\b(?:what|which)\s+(?P<d>[a-z][a-z-]*)\s+am\s+i\s+"
    r"(?:driving|riding|using|in)\b"
    r"|\b(?:do|can|could|did)\s+(?:u|you)\s+(?:remember|recall|know)\s+(?:what|which)\s+"
    r"(?P<e>[a-z][a-z-]*)\s+(?:i|u|you)\s+(?:drive|ride|use|own|have)\b"
    r"|\b(?:what|which)\s+(?P<f>[a-z][a-z-]*)\s+(?:i|u|you)\s+(?:drive|ride|use|own)\b", re.I)

def _a_that_fits(name):
    first = str(name or "").split()[0] if str(name or "").split() else ""
    if len(first) > 1 and first.isupper():
        return "a"
    return "an" if first[:1].lower() in "aeiou" else "a"

def _a_thing_i_own_reply(memory, low):
    held = user(memory).get("owns")
    if not isinstance(held, dict) or not held:
        held = {}
    for match in OWNED_ASK.finditer(low):
        thing = next((word for word in match.groups() if word), "")
        thing = thing.replace("-", " ")
        if not thing:
            continue
        name = held.get(thing) or held.get(thing.rstrip("s"))
        if thing == "car" and not name:
            name = user(memory).get("car") or ""
        if thing == "car" and name:
            return car_line(name)
        said = {"bike": ("You ride ", "Your bike is "),
                "motorbike": ("You ride ", "Your motorbike is ")}.get(thing)
        if name:
            article = _a_that_fits(name)
            if said:
                return pick([said[0] + article + " " + name + ".",
                             said[1] + article + " " + name + "."], memory)
            if thing == "phone":
                return pick(["Your phone is " + article + " " + name + ".",
                             "You've got " + article + " " + name + "."], memory)
            return pick(["Your " + thing + " is " + article + " " + name + ".",
                         "You told me your " + thing + " is " + article + " " + name + "."],
                        memory)
        if thing in extract.OWNED:
            return pick(["You haven't told me the make of your " + thing,
                         "You've not said what your " + thing + " is"], memory) + "."
    return None

def _about_a_person_reply(memory, low, text=""):
    if not isinstance(low, str):
        return None
    called = _the_person_called(memory, low)
    match = (ABOUT_PERSON_ASK.search(low) or _continues_an_about_ask(memory, low)
             or (ABOUT_A_NAME.search(low) if called else None))
    if not match:
        return None
    who = _named_person(low, memory) or called
    if not who:
        who = _pronoun_person(text or low, memory)
    if not who:
        children = _about_the_children_reply(memory, low)
        if children:
            return children
        return None
    entry, lines = _a_known_person(memory, who)
    named = _called(entry.get("name")) if entry.get("name") else ""
    clauses = _person_clauses(who, entry)
    birthday = str(entry.get("birthday") or "").strip()
    if birthday and not clauses and not lines:
        return _vary(["Your " + who + "'s birthday is " + _date_written_as_a_date(birthday) + ".",
                      "You told me your " + who + "'s birthday is "
                      + _date_written_as_a_date(birthday) + "."], memory)
    if not clauses and named and not lines:
        return _vary(["Your " + who + " is called " + named + ".",
                      "Your " + who + " is " + named + "."], memory)
    if not clauses and not lines:
        named_line = _a_line_about(memory, who)
        if named_line:
            return ("You told me " + _named_back(who, you(named_line)).strip().rstrip(".") + "."
                    if not ABOUT_PERSON_MORE.search(str(text or ""))
                    else "That's all I have: " + _named_back(who, you(named_line))
                    .strip().rstrip(".") + ".")
        if ABOUT_PERSON_MORE.search(str(text or "")):
            return "You haven't told me anything about your " + who + " yet."
        return _vary(["You haven't told me anything about your " + who + " yet.",
                      "Nothing on your " + who + " so far \u2014 tell me and I'll keep it."],
                     memory)
    subject = "Your " + who + ((" " + named) if named and clauses else "")
    facts = ""
    if clauses:
        if len(clauses) == 1:
            facts = subject + " " + clauses[0]
        else:
            rest = [clause[3:] if clauses[0].startswith("is ") and clause.startswith("is ")
                    else clause for clause in clauses[1:]]
            facts = subject + " " + clauses[0] + " and " + _and_list(rest)
    said = ""
    if lines:
        line = you(lines[-1]).strip().rstrip(".")
        line = _named_back(who, line)
        if named:
            line = re.sub(r"\b" + re.escape(named) + r"\b", named, line, flags=re.I)
        said = line
    if said and (not facts or _covers(said, clauses)):
        if TELLING_ALREADY.match(said):
            answer = said[0].upper() + said[1:] + "."
        else:
            answer = _vary(["You told me " + said, "You said " + said], memory) + "."
    elif facts and said and _tokens(said) <= _tokens(facts):
        answer = facts + "."
    elif facts and said:
        answer = facts + ". You also said " + said + "."
    else:
        answer = (facts or "") + "."
    if ABOUT_PERSON_MORE.search(str(text or "")) and (
            _said_everything(answer, memory)
            or re.search(r"\b(?:everything you've told me|all I've got) (?:about|on) your "
                         + re.escape(who), last_bot(memory) or "", re.I)):
        return _vary(["That's everything you've told me about your " + who + ".",
                      "That's still all I've got on your " + who + "."], memory)
    if _said_everything(answer, memory):
        body = (facts or said or answer).strip().rstrip(".")
        return "Still: " + body[0].lower() + body[1:] + "."
    return answer

def _about_the_children_reply(memory, low):
    if not CHILDREN_ABOUT.search(str(low or "")):
        return None
    kept = [entry for entry in others(memory) if isinstance(entry, dict)
            and _in_the_group(entry.get("who"), CHILD_RELATIONS)]
    clauses = []
    for entry in kept[:4]:
        name = _called(str(entry.get("name") or "")) if entry.get("name") else ""
        names = [str(one) for one in (entry.get("names") or []) if str(one).strip()]
        if len(names) > 1:
            clauses.append("your " + str(entry.get("who") or "children") + " are called "
                           + _a_list_of_names([_called(one) for one in names]))
        elif entry.get("ages"):
            ages = [age for age in entry["ages"] if isinstance(age, int)]
            who = str(entry.get("who") or "children")
            said = (", ".join(str(age) for age in ages[:-1]) + " and " + str(ages[-1])
                    if len(ages) > 1 else str(ages[0]))
            clauses.append("your " + who + _is_are(who) + said)
        elif entry.get("months") and not entry.get("age"):
            clauses.append((name or ("your " + str(entry.get("who") or "child")))
                           + " is " + str(entry["months"]) + " months old")
        elif entry.get("age") or entry.get("turns"):
            clauses.append(_one_age(str(entry.get("who") or "child"), entry.get("age"),
                                    str(entry.get("turns") or ""), entry.get("to_come"),
                                    held=name).strip().rstrip("."))
        elif name:
            clauses.append("your " + str(entry.get("who") or "child") + " is called " + name)
    clauses = [clause[0].lower() + clause[1:] if clause.startswith("Your ") else clause
               for clause in clauses]
    if not clauses:
        typed = _the_group_names_typed("kids", memory) or _the_group_names_typed("children", memory)
        if typed:
            clauses = ["your kids are called " + _a_list_of_names([_called(one) for one in typed])]
    if not clauses:
        counted = (memory.get("user") or {}).get("kids")
        if isinstance(counted, int) and counted:
            return _vary(["You've told me you have " + _a_number_word(counted) + " "
                          + ("kid" if counted == 1 else "kids")
                          + ", and nothing more about them yet.",
                          "Just the count: " + _a_number_word(counted) + " kids, with no name or "
                          "age yet."], memory)
        return None
    one = (str(kept[0].get("who") or "") if len(kept) == 1 else "")
    about = _object_pronoun(one) if one else "them"
    if len(clauses) == 1:
        first = "You've told me " + clauses[0] + "."
        second = clauses[0][:1].upper() + clauses[0][1:] + " - that's all I've got on " \
            + about + "."
        return _vary([first, second], memory)
    facts = _a_list_of_clauses(clauses)
    answer = _vary([facts + " - that's what I've got on " + about + ".",
                    "That's everything I have on " + about + ": " + facts + "."], memory)
    return answer[:1].upper() + answer[1:]

def _a_list_of_clauses(clauses):
    said = [str(clause) for clause in clauses if str(clause)]
    if len(said) < 3:
        return " and ".join(said)
    return ", ".join(said[:-1]) + " and " + said[-1]

def _the_person_called(memory, line):
    for match in re.finditer(r"\babout\s+([a-z][a-z'-]{1,20})\b", str(line or ""), re.I):
        word = match.group(1).lower()
        if word in extract.RELATIONS or word in extract.ALONE_PERSON:
            continue
        for entry in others(memory):
            name = str(entry.get("name") or "").strip().lower()
            if name and name == word:
                return str(entry.get("who") or "")
    return ""

def _covers(said, clauses):
    seen = _tokens(said)
    return all(_tokens(clause) <= seen for clause in clauses)

def _tokens(text):
    words = set(content(text)) | set(re.findall(r"\d+", str(text or "")))
    return {word[:-1] if word.endswith("s") and word[:-1] in extract.RELATIONS else word
            for word in words}

def _said_everything(answer, memory):
    mine = _tokens(answer)
    if not mine:
        return False
    for turn in _every_line(memory):
        before = str(turn.get("bot") or "")
        if before and mine <= _tokens(before):
            return True
    return False

def _a_pregnancy_of_their_own(text, memory, low):
    if not isinstance(text, str) or "?" in text:
        return None
    if _about_this_chat(text, memory) or OTHER_ASK.search(low) or REMINDER_MID.search(low):
        return None
    found = extract.extract(text)
    if not found.get("pregnant"):
        return None
    if isinstance(found.get("weeks"), int):
        weeks = _a_number_word(int(found["weeks"]))
        return _vary([line.format(weeks=weeks) for line in PREGNANT_OWN_SAY], memory)
    return _vary(["Good to know — I'll keep the drink out of anything I suggest, and the weeks "
                  "are worth telling me if you want a meal plan that fits them.",
                  "Noted, and congratulations. Nothing alcoholic in anything I suggest; say if "
                  "you want a hand with what to cook."], memory)

def _a_state_told(text, memory, low):
    if not isinstance(text, str) or "?" in text:
        return None
    if _the_ask_beats_the_receipt(text, memory):
        return None
    if _about_this_chat(text, memory) or OTHER_ASK.search(low) or REMINDER_MID.search(low):
        return None
    found = extract.extract(text)
    if found.get("diet") or found.get("allergies") or found.get("pregnant"):
        return None
    named = [who for who in (found.get("people") or []) if isinstance(who, str)]
    for entry in found.get("others") or []:
        who = entry.get("who") or _person_from_pronoun(text, memory, named)
        if not who:
            continue
        if entry.get("pregnant") and isinstance(entry.get("weeks"), int):
            weeks = _a_number_word(int(entry["weeks"]))
            return _vary([line.format(who=who, weeks=weeks) for line in PREGNANT_WEEKS_SAY],
                         memory)
        if entry.get("pregnant"):
            return _vary([line.format(who=who) for line in PREGNANT_SAY], memory)
        if entry.get("breastfeeding"):
            return _vary([line.format(who=who) for line in FEEDING_SAY], memory)
        if entry.get("drinks") is False:
            return _vary([line.format(who=who) for line in LIMIT_SAY], memory)
    return None

WAS_A_STATE = re.compile(
    r"\b(?:was|were|had\s+been|has\s+been|have\s+been|used\s+to\s+be)\s+"
    r"(?:still\s+|also\s+|once\s+|again\s+)?"
    r"(?:pregnant|expecting(?:\s+a\s+baby)?|breastfeeding|nursing\s+a\s+baby)\b", re.I)

def _a_state_that_was(text, memory, low):
    if not isinstance(text, str) or "?" in text:
        return None
    if _about_this_chat(text, memory):
        return None
    if not WAS_A_STATE.search(" ".join(str(text or "").split())):
        return None
    return _vary(list(STATE_WAS_SAY), memory)

PET_PART_ASK = re.compile(
    r"\b(?:his|her|its|their|my|our|the)\s+(?:age|breed)\b"
    r"|\bhow old (?:is|was) (?:he|she|it|they)\b"
    r"|\bwhat (?:breed|kind|sort|type)\b|\bwhich breed\b", re.I)

BREED_WORD = re.compile(r"\bbreed\b|\bwhat (?:kind|sort|type)\b|\bwhich breed\b", re.I)

def _pet_part_reply(memory, low):
    if not PET_PART_ASK.search(low):
        return None
    if re.search(r"\bage\b|\bhow old\b", low):
        said = _pet_age_reply(memory, low)
        if said:
            return said
    return _pet_breed_reply(memory, low)

def _pet_breed_reply(memory, low):
    if not BREED_WORD.search(low):
        return None
    pets = [pet for pet in (user(memory).get("pets") or [])
            if isinstance(pet, dict) and str(pet.get("breed") or "").strip()
            and not pet.get("not_theirs")]
    if not pets:
        return None
    asked = []
    family = ""
    animal = PET_ASK.search(low)
    if animal:
        family = _animal_family(animal.group(1))
    if family:
        asked = [pet for pet in pets if _animal_family(pet.get("animal")) == family]
    if not asked:
        for pet in pets:
            name = str(pet.get("name") or "").strip()
            if len(name) > 2 and re.search(r"\b" + re.escape(name.lower()) + r"\b", low):
                asked.append(pet)
    if not asked and re.search(r"\b(?:she|he|it|they|his|her|its|their)\b", low):
        asked = [pets[-1]]
    if not asked:
        return None
    pet = asked[-1]
    breed = str(pet.get("breed") or "").strip()
    name = str(pet.get("name") or "").strip()
    if not name:
        return _vary(["A " + breed + " - that is what you said.",
                      "You said a " + breed + ".",
                      "A " + breed + "."], memory)
    name = _tidy_name(name)
    return _vary([name + " is a " + breed + ".",
                  "You told me " + name + " is a " + breed + ".",
                  "A " + breed + ", that one."], memory)

def _a_number(value):
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return value

def _a_pronoun_age(memory, low):
    match = re.search(r"\b(she|he|they)(?:'s|s|'re|re)?\b", str(low or ""))
    if not match:
        return None
    pronoun = match.group(1)
    lines = []
    for turn in recent(memory, 5):
        said = turn.get("user") if isinstance(turn, dict) else None
        lines.append(said if isinstance(said, str) else "")
    for i in range(len(lines) - 1, -1, -1):
        said = lines[i]
        if not said.strip():
            continue
        small = A_SMALL_UNIT.search(said.lower())
        if AN_ANIMAL.search(said) or (small and (AN_ANIMAL.search(lines[i - 1] if i else "")
                                                  or memory.get("pets"))):
            continue
        if small and _a_pronoun_word(said) == pronoun:
            was = "are" if pronoun == "they" else "is"
            return (pronoun + " " + was + " " + small.group(1) + " " + small.group(2)
                    + " old.").capitalize()
        for entry in extract.extract(said).get("others") or []:
            if not isinstance(entry, dict) or entry.get("who"):
                continue
            theirs = str(entry.get("pronoun") or "") or _a_pronoun_word(said)
            if theirs != pronoun:
                continue
            age = entry.get("age")
            if isinstance(age, str) and age.strip().isdigit():
                age = int(age.strip())
            if not isinstance(age, int):
                continue
            named = the_pronoun_said_with_a_name(memory, age)
            if named:
                return named
            return _one_age(pronoun, age, str(entry.get("turns") or ""))
    return None

AN_ANIMAL = re.compile(
    r"\b(?:cat|cats|kitten|kittens|dog|dogs|puppy|puppies|pup|rabbit|bunny|hamster|gerbil|"
    r"guinea pig|parrot|budgie|bird|fish|horse|pony|ferret|tortoise|snake|lizard|pets?)\b", re.I)

A_SMALL_UNIT = re.compile(r"\b(\d{1,2})\s*(weeks?|months?)\b", re.I)

def _a_pronoun_word(text):
    match = re.search(r"\b(she|he|they)(?:'s|s|'re|re)?\b", str(text or "").lower())
    return match.group(1) if match else ""

def _someone_else_named(low, memory):
    names = [str(known.get("who") or "").strip() for known in others(memory)]
    names = [name for name in names if name] + list(extract.RELATIONS)
    found = []
    flat = low.replace("'", "").replace("\u2019", "")
    for name in set(names):
        match = re.search(r"\b" + re.escape(name.replace("'", "").replace("\u2019", ""))
                          + r"s?\b", flat)
        if match:
            found.append((-len(name), -match.start(), name))
    if found:
        return min(found)[2]
    if THEM.search(low):
        return _person_from_pronoun(low, memory)
    return ""

_SAME_FACT_PERSON = _RELATION + "|kids|children|child|boys|girls"

SAME_FACT_ABOUT = re.compile(
    r"^(?:and |so |oh |but |ok |okay )*"
    r"(?:same for )?"
    r"(?:(?:my|our) (?P<who>" + _SAME_FACT_PERSON + r")"
    r"|(?:the )?(?P<more>" + _SAME_FACT_PERSON + r")s?)"
    r"(?: (?:is|are|does|do|has|have))?"
    r"(?: (?P<same>too|as well|also|the same|same|neither))?$", re.I)

NEGATIVE_TAIL = frozenset("""either at all as well really actually""".split())

SAME_FACT_AGAINST_PRONOUN = re.compile(
    r"^(?:and |so |oh |but |ok |okay |no,? |actually )*(?P<pron>she|he|they)"
    r"(?: is| are|'s|s)(?P<neg>nt|n't| not)\b(?P<rest>.*)$", re.I)

SAME_FACT_AGAINST = re.compile(
    r"^(?:and |so |oh |but |ok |okay )*(?:(?:my|our) (?P<who>" + _SAME_FACT_PERSON + r")"
    r"|(?P<more>" + _SAME_FACT_PERSON + r")s?) (?:is|are)"
    r"(?P<neg>nt|n't| not)\b(?P<rest>.*)$", re.I)

def _the_same_fact_about_someone(text, memory):
    if not isinstance(text, str) or not isinstance(memory, dict):
        return None
    low = " ".join(text.lower().split()).strip(" ?!.")
    if not low or len(low.split()) > 7:
        return None
    match = SAME_FACT_AGAINST.match(low)
    against = bool(match)
    by_pronoun = False
    if not match:
        match = SAME_FACT_AGAINST_PRONOUN.match(low)
        against = by_pronoun = bool(match)
    if not match:
        match = SAME_FACT_ABOUT.match(low)
    if not match:
        return None
    if by_pronoun:
        last = _the_person_last_given_a_fact(memory)
        if not last:
            return None
        who, kind, value = last
        if not _the_fact_said_against(kind, value, match.groupdict().get("rest") or ""):
            return None
        _take_the_fact_back(memory, who, kind)
        return (_ive_taken_it_back(who, kind, value), None)
    who = (match.group("who") or match.group("more") or "").strip()
    if who not in PLURAL_PEOPLE and who.endswith("s") and who[:-1] in extract.RELATIONS:
        who = who[:-1]
    if not who:
        return None
    same = (match.groupdict().get("same") or "").strip().lower()
    if not against and not same and not low.startswith("same for"):
        return None
    held = _the_fact_on_record(memory)
    if not held:
        return None
    given = extract.extract(text)
    if any(given.get(key) for key in SAME_FACT_THEIR_OWN):
        return None
    for known in others(memory):
        if known.get("who") == who and any(known.get(key) for key in SAME_FACT_THEIR_OWN):
            return None
    kind, value = held
    if against:
        if match.groupdict().get("same", "").lower() == "neither":
            return None
        if not _the_fact_said_against(kind, value, match.groupdict().get("rest") or ""):
            return None
        return (_isnt_this_too(who, kind, value), None)
    return (_this_too(who, kind, value), {kind: list(value) if isinstance(value, list) else value,
                                          "who": who})

def _the_fact_said_against(kind, value, rest):
    words = str(rest or "").strip(" ?!.").split()
    if not words:
        return True
    if words[0].lower() in NEGATIVE_TAIL:
        return all(word.lower() in NEGATIVE_TAIL for word in words)
    first = words[0].lower()
    if kind == "allergies":
        return first == "allergic"
    head = str(value[0] if isinstance(value, list) else value).lower()
    return bool(head) and (first == head or head.startswith(first))

def _the_person_last_given_a_fact(memory):
    for known in reversed(others(memory)):
        if not isinstance(known, dict) or not known.get("who"):
            continue
        for key in ("allergies", "diet", "condition"):
            if known.get(key):
                return str(known["who"]), key, known[key]
    return None

def _take_the_fact_back(memory, who, kind):
    for known in reversed(others(memory)):
        if not isinstance(known, dict) or known.get("who") != who:
            continue
        known.pop(kind, None)
        left = {key for key in known if key not in {"who", "name", "turns"}}
        if not left:
            others(memory).remove(known)
        return

def _ive_taken_it_back(who, kind, value):
    if kind == "allergies":
        said = "allergic to " + _and_list(value)
    elif isinstance(value, list):
        said = str(value[0])
    else:
        said = str(value)
    negative = " aren't " if _plural_person(who) else " isn't "
    return ("Your " + who + negative + said + ", then - I've taken that back off "
            + ("them" if _plural_person(who) else "her" if who in _SHE else
               "him" if who in _HE else "them") + ".")

_SHE = frozenset("""mum mom mother mum-in-law wife girlfriend sister daughter aunt grandma
    grandmother granny nan nana niece fiancee""".split())

_HE = frozenset("""dad father husband boyfriend brother son uncle grandad grandfather grandpa
    nephew fiance""".split())

def _the_fact_on_record(memory):
    them = user(memory) or {}
    for key in ("allergies", "diet", "condition"):
        value = them.get(key)
        if value:
            return key, value
    return None

def _both_of_you(who):
    return "all of you" if _plural_person(who) else "both of you"

def _this_too(who, kind, value):
    if kind == "allergies":
        return ("Your " + who + _is_are(who) + "allergic to "
                + _and_list(value) + " too, then - I'll keep it out for "
                + _both_of_you(who) + ".")
    if kind == "condition":
        return ("Your " + who + _is_are(who) + str(value[0] if isinstance(value, list) else value)
                + " too, then - I'll keep it in mind for " + _both_of_you(who) + ".")
    return ("Your " + who + _is_are(who) + str(value) + " too, then - I'll plan around "
            + _both_of_you(who) + ".")

def _isnt_this_too(who, kind, value):
    if kind == "allergies":
        said = "allergic to " + _and_list(value)
    elif isinstance(value, list):
        said = str(value[0])
    else:
        said = str(value)
    negative = " aren't " if _plural_person(who) else " isn't "
    return ("Your " + who + negative + said + ", then - good to know. It's just you I'll plan for.")

WHAT_ABOUT_A_FOOD = re.compile(
    r"^\W*(?:and\s+|what\s+about\s+|how\s+about\s+|ok\s+with\s+)?([a-z][a-z' -]{2,30})\s*\??$",
    re.I)

def _the_person_still_in_hand(low, memory):
    if not WHAT_ABOUT_A_FOOD.match(low):
        return ""
    person = memory.get("person") if isinstance(memory, dict) else None
    who = str((person or {}).get("who") or "").strip() if isinstance(person, dict) else ""
    if not who:
        return ""
    for known in others(memory):
        if known.get("who") == who and _a_food_word(low, known):
            return who
    return ""

def _a_food_word(low, entry):
    ruled = []
    condition = str(entry.get("condition") or "").lower()
    if condition in CONDITION_RULES_OUT:
        ruled.append(CONDITION_RULES_OUT[condition])
    diet = str(entry.get("diet") or "").lower()
    if diet in DIET_RULES_OUT:
        ruled.append(DIET_RULES_OUT[diet][0])
    return any(_what_the_food_has(low, thing)[0] for thing in ruled)

def _other_person_reply(memory, low):
    undeclared = _the_person_still_in_hand(low, memory)
    bare_limit_ask = _a_bare_limit_ask(low, memory)
    if not (undeclared or OTHER_FACT.search(low) or EAT_ASK.search(low)
            or CANT_HAVE.search(low) or CAN_HAVE.search(low) or CAN_THEY_HAVE.search(low)
            or bare_limit_ask):
        return None
    if CAN_THEY_HAVE_A_FOOD.search(low) and not _a_limit_kept_for_them(low, memory) \
            and not bare_limit_ask:
        return None
    who = _someone_else_named(low, memory) or undeclared
    entry = None
    for known in others(memory):
        if known.get("who") == who:
            entry = known
            break
    if entry is None:
        offered = _did_you_mean_the_person(memory, low)
        if offered:
            return offered
        if _a_bare_limit_ask(low, memory):
            return _nothing_kept_about_them(low)
        if HELP_ASK.search(low):
            return None
        if not who:
            if _nobody_else_kept(memory) and _the_pronoun_in(low) \
                    and _asks_for_a_limit_not_advice(low):
                return _nothing_kept_about_them(low)
            return None
        if OTHER_FACT.search(low):
            return "You haven't told me about an allergy of your " + who + "."
        return _no_diet(who)
    if OTHER_FACT.search(low):
        allergies = entry.get("allergies") or []
        owner = ("Your " + who) if who else "They"
        if not allergies:
            return ("You haven't told me about an allergy of " + (("your " + who) if who else "theirs")
                    + ".")
        return owner + _is_are(who) + "allergic to " + ", ".join(allergies) + "."
    diet = entry.get("diet")
    allergies = entry.get("allergies") or []
    condition = entry.get("condition")
    if condition and (undeclared or CANT_HAVE.search(low) or CAN_HAVE.search(low)
                      or EAT_ASK.search(low) or CAN_THEY_HAVE.search(low)):
        said = _condition_is_their_food(who, condition, low)
        if said:
            if diet and not allergies:
                return said + " " + _diet_sentence(who, diet)
            return said
    if diet and (undeclared or CANT_HAVE.search(low) or CAN_HAVE.search(low)
                 or CAN_THEY_HAVE.search(low) or EAT_ASK.search(low)):
        ruled = _diet_is_their_food(who, diet, low, plain=bool(EAT_ASK.search(low)))
        if ruled and not allergies:
            return ruled
    if diet and allergies:
        return _both_food_facts(who, allergies, diet)
    if not diet:
        allergies = entry.get("allergies") or []
        if allergies:
            return _allergy_is_their_food(who, allergies, low=low)
        condition = entry.get("condition") or []
        if condition and _a_condition_rules_out(condition):
            return None
        return _no_diet(who)
    return _diet_sentence(who, diet)

THE_PRONOUN = re.compile(r"\b(she|her|hers|he|him|his|they|them|their)\b", re.I)


A_LIMIT_NAMED = re.compile(r"\b(?:allerg\w*|allergies|vegan|vegetarian|pescatarian|coeliac|celiac|"
                           r"intolerant|intolerance|di(?:ae)?t|avoid\w*)\b", re.I)
ASKING_AGAIN = re.compile(r"\b(?:again|remind me|did i (?:say|tell|mention)|what did i (?:say|tell|"
                          r"mention)|what i (?:said|told|mentioned))\b", re.I)
ADVICE_NOT_A_FACT = re.compile(r"\bhow\b|\bwhat should\b|\bwhat can we\b|\bwhere\b|\bwhen\b"
                               r"|\bwhy\b|\bhow much\b", re.I)


A_HAVE_QUESTION = re.compile(r"\b(?:does|do|did)\s+\w+\s+(?:have|has|had|got)\b"
                             r"|\b(?:has|have)\s+(?:she|he|they|anyone|anybody|your)\b")
STATES_A_LIMIT = re.compile(r"\b(?:has|have|had|got)\b[^.!?]{0,24}?\ballerg\w*"
                            r"|\bis\s+allergic\b|\bare\s+allergic\b"
                            r"|\b(?:is|are|am)\s+(?:a\s+)?(?:vegan|vegetarian|coeliac|celiac)\b",
                            re.I)


A_ASK_FRAME = re.compile(r"\b(?:what|which|who|tell me|remind me|if|whether|wonder|know)\b"
                         r"[^.!?]{0,24}?\b(?:is|are|was|were|has|have|does|do|can)\b", re.I)


def _asks_for_a_limit_not_advice(low):
    text = str(low or "")
    if ADVICE_NOT_A_FACT.search(text):
        return False
    if STATES_A_LIMIT.search(text) and not A_HAVE_QUESTION.search(text) \
            and not A_ASK_FRAME.search(text):
        return False
    if re.search(r"\bnot\s+eat\b", text):
        return True
    if CANT_HAVE.search(text):
        return True
    return bool(A_LIMIT_NAMED.search(text) or ASKING_AGAIN.search(text))


def _the_pronoun_in(low):
    found = [m.group(1).lower() for m in THE_PRONOUN.finditer(str(low or ""))]
    for word in found:
        if word in ("she", "her", "hers"):
            return "she"
        if word in ("he", "him", "his"):
            return "he"
    for word in found:
        if word in ("they", "them", "their"):
            return "they"
    return ""


def _nobody_else_kept(memory):
    if not isinstance(memory, dict):
        return True
    kept = memory.get("others")
    return not (isinstance(kept, list) and kept)


A_MEAL_WORD = re.compile(r"\b(?:cook|cooking|cooked|recipe|recipes|meal|meals|dinner|tea|lunch|"
                         r"breakfast|snack|menu|shop|shopping|bake|baking)\b", re.I)


def _a_bare_limit_ask(low, memory):
    text = str(low or "")
    if A_MEAL_WORD.search(text):
        return False
    return bool(_nobody_else_kept(memory) and _the_pronoun_in(text)
                and _asks_for_a_limit_not_advice(text))


def _nothing_kept_about_them(low):
    pronoun = _the_pronoun_in(low)
    if OTHER_FACT.search(str(low or "")):
        theirs = {"she": "hers", "he": "his"}.get(pronoun, "theirs")
        return ("You haven't told me about an allergy of " + theirs
                + " yet \u2014 what is it? I'll keep it out of anything I suggest.")
    if pronoun in ("she", "he"):
        return ("You haven't told me how " + pronoun + " eats yet \u2014 what does " + pronoun
                + " avoid? I'll plan the meals round it.")
    return ("You haven't told me how they eat yet \u2014 what do they avoid? I'll plan the meals "
            "round it.")


def _did_you_mean_the_person(memory, low):
    held = [e for e in others(memory) if isinstance(e, dict) and e.get("who")]
    if len(held) != 1:
        return None
    if not THEM.search(low):
        return None
    who = str(held[0].get("who"))
    said = ""
    if OTHER_FACT.search(low) and held[0].get("allergies"):
        said = "Your " + who + _is_are(who) + "allergic to " + ", ".join(held[0]["allergies"]) + "."
    elif EAT_ASK.search(low) and held[0].get("diet"):
        said = _diet_sentence(who, held[0]["diet"])
    elif EAT_ASK.search(low) and held[0].get("allergies"):
        said = _allergy_is_their_food(who, held[0]["allergies"])
    if not said:
        return None
    gender = _gender_of(who)
    pronoun = "She" if gender == "she" else "He" if gender == "he" else "They"
    tail = said[len("Your " + who):]
    if pronoun == "They":
        tail = re.sub(r"^(\s+)is\b", r"\1are", tail)
        tail = re.sub(r"^(\s+)does not\b", r"\1do not", tail)
    ask_gender = _ask_gender(low)
    if ask_gender and gender and gender != ask_gender:
        him = "her" if gender == "she" else "him"
        return ("I've only got your " + who + " down, and " + pronoun.lower() + tail
                + " Did you mean " + him + "?")
    return "Did you mean your " + who + "? " + pronoun + tail

def _condition_is_their_food(who, condition, low=""):
    said = " ".join(str(low or "").lower().split())
    low = " ".join(str(condition or "").lower().split())
    owner = ("Your " + who) if who else "They"
    tail = " \u2014 that's all I have on food for " + _their_pronoun(who) + "."
    ruled = CONDITION_RULES_OUT.get(low)
    named, thing = _what_the_food_has(said, ruled) if (ruled and said) else ("", "")
    if named:
        return (named[:1].upper() + named[1:] + " has " + thing + " in it, and " + owner.lower()
                + _is_are(who) + low + ".")
    if ruled:
        return (owner + _is_are(who) + low + ", so nothing with " + ruled + " in it" + tail)
    watched = CONDITION_KEEPS_DOWN.get(low)
    if watched:
        return (owner + _is_are(who) + low + ", so keep the " + watched + " down" + tail)
    if low:
        return owner + _is_are(who) + low + tail
    return None

def _diet_sentence(who, diet):
    if str(diet).startswith("eats ") or str(diet).startswith("no "):
        if who:
            return "Your " + who + " " + _a_diet_predicate(who, diet) + "."
        return "They eat " + str(diet)[5:] + "." if str(diet).startswith("eats ") \
            else "They don't " + _diet_how(diet) + " " + str(diet)[3:] + "."
    if who:
        return "Your " + who + _is_are(who) + str(diet) + "."
    return "They're " + str(diet) + "."

A_BIRTHDAY_PLAN = re.compile(r"\b(?:birthday|bday|dob|date of birth)\s+(?:is\s+|was\s+|on\s+|in\s+)?"
                             r"([^,.;!?]{2,28})", re.I)

_A_RELATION = ("(?:" + "|".join(sorted(extract.RELATIONS, key=len, reverse=True)) + r")"
               + extract.IN_LAW)

A_RELATIONS_BIRTHDAY = re.compile(
    r"\b" + _A_RELATION + r"(?:'s|s)?\s+"
    r"(?:birthday|bday|dob|date of birth)\b", re.I)

NO_CAP = frozenset(("diesel", "petrol", "hybrid", "electric", "estate", "hatchback", "saloon",
                    "coupe", "convertible", "automatic", "manual", "classic"))

CAR_DESCRIBED = frozenset("""old new used secondhand second-hand little small big cheap tidy rusty
yellow red blue white black silver grey gray green other spare reliable""".split())

def car_line(car):
    said = " ".join(str(car or "").split())
    if not said:
        return ""
    words = said.split()
    if any(word.lower() in CAR_DESCRIBED for word in words):
        return "You drive " + _a(said) + "."
    if len(words) == 1 and said.lower() in NO_CAP:
        return "You drive " + _a(said) + "."
    shown = " ".join(CAR_CAPS.get(word.lower(),
                                  word[:1].upper() + word[1:] if word.islower() else word)
                     for word in words)
    return "You drive " + _a(shown) + "."

def _birthday_in_words(memory):
    for plan in reversed(user(memory).get("plans") or []):
        said = str(plan)
        match = extract.BIRTHDAY.search(said) or A_BIRTHDAY_PLAN.search(said)
        if not match or extract.subject(said, match.start())[0] == "other":
            continue
        if A_RELATIONS_BIRTHDAY.search(said):
            continue
        words = " ".join(match.group(1).lower().split()).rstrip(" .,;:")
        words = re.sub(r"^(?:in|on)\s+", "", words)
        if words:
            return words
    return ""

def _birthday_reply(memory):
    known = user(memory)
    date = known.get("birthday")
    words = _birthday_words(date) if date else _birthday_in_words(memory)
    if not words:
        return "You haven't told me your birthday yet."
    if words.startswith("in "):
        plain = words[:1].upper() + words[1:] + "."
    elif re.match(r"(?:the\s+)?\d", words):
        plain = "On " + words + "."
    else:
        plain = "Your birthday is " + words + "."
    if plain in {turn.get("bot") for turn in memory.get("turns") or []}:
        return _vary(["It's " + words + " — that's what you told me.",
                      "You said " + words + ".",
                      "Still " + words + "."], memory)
    return plain

WHOSE_BIRTHDAY = re.compile(
    r"\b(?:when|what\s+date)(?:'s|s)?\s+(?:is|was|are)?\s*(?:it\s+)?"
    r"(?:(?:my|our)\s+(?P<who>" + _A_RELATION + r")s?"
    r"|(?P<pronoun>his|her)"
    r"|(?P<name>[a-z][a-z'\u2019-]+)(?:'s|s))\s*"
    r"(?:birthday|bday|dob|date\s+of\s+birth)\b", re.I)

def _the_same_relative(one, other):
    one = str(one or "").lower()
    other = str(other or "").lower()
    if not one or not other:
        return False
    if one == other:
        return True
    return (other.endswith("s") and one == other[:-1]) or (one.endswith("s") and one[:-1] == other)

def _a_persons_birthday_reply(memory, low):
    asked = WHOSE_BIRTHDAY.search(low)
    if not asked:
        return None
    who = extract.a_person_word(asked.groupdict().get("who") or "")
    pronoun = (asked.groupdict().get("pronoun") or "").lower()
    named = (asked.groupdict().get("name") or "").lower()
    if who in ("birthday", "bday", "dob", "date"):
        return None
    known = None
    if who:
        known = next((entry for entry in others(memory)
                      if _the_same_relative(entry.get("who"), who)), None)
        if known is not None:
            who = str(known.get("who") or who)
    elif named:
        known = next((entry for entry in others(memory)
                      if _same_name(entry.get("name") or "", named)), None)
    elif pronoun:
        fits = extract.SHE if pronoun == "her" else extract.HE
        known = next((entry for entry in reversed(others(memory))
                      if (entry.get("who") or "").lower() in fits), None)
        if known is not None:
            who = str(known.get("who") or "")
            named = str(known.get("name") or "")
        else:
            word = "she" if pronoun == "her" else "he"
            known = next((entry for entry in others(memory)
                          if str(entry.get("pronoun") or "") == word and entry.get("birthday")),
                         None)
    if known is None or not known.get("birthday"):
        return None
    words = _birthday_words(known["birthday"])
    said_name = str(known.get("name") or named or "")
    if said_name and not who:
        said_name = said_name[:1].upper() + said_name[1:]
        return _vary([said_name + "'s birthday is " + words + ".",
                      "That's " + words + " for " + said_name + "."], memory)
    if not who:
        return None
    theirs = ("Your " + who + ("'" if _plural_person(who) else "'s") + " birthday is "
              + words + ".")
    return _vary([theirs,
                  "That's " + words + " for your " + who + ".",
                  "Your " + who + ("'" if _plural_person(who) else "'s") + " birthday: "
                  + words + "."], memory)

def _weight_reply(memory):
    known = user(memory)
    weight = known.get("weight")
    if not weight:
        return "You haven't told me what you weigh."
    plain = "You weigh " + weight + "."
    if plain in {turn.get("bot") for turn in memory.get("turns") or []}:
        return _vary(["Still " + weight + ".", "You said " + weight + ".",
                      "It's " + weight + " — that's what you told me."], memory)
    return plain

ALLERGY_IN_THE_WORLD = re.compile(r"\bwhy\s+(?:do|does|did|would|are|is|can)\b|"
                                  r"\bwhat\s+causes?\b|\bhow\s+common\b|"
                                  r"\bwhat\s+are\s+allergies\b", re.I)

A_HOW_TO_ASK = re.compile(r"^\s*(?:so|and|ok|okay|hi|hello)?[, ]*\s*"
                          r"(?:how (?:do|can|could|should|would|might|to)\b|"
                          r"ways? to\b|any (?:tips|advice|ideas|suggestions|ways)\b|"
                          r"tips for\b|help me\b|what can i do\b|what should i do\b)", re.I)
A_RECALL_WORD = re.compile(r"\bagain\b|\bremind me\b|\bdid i (?:say|tell|mention)\b|"
                           r"\bwhat did i say\b|\bdo you remember\b|\byou know my\b|"
                           r"\bwhat was my\b|\bwhats my\b|\bwhat's my\b|\bknow\b", re.I)

def _height_reply(memory):
    known = user(memory)
    height = str(known.get("height") or "").strip()
    if not height:
        return "You haven't told me how tall you are."
    plain = "You're " + height + "."
    if plain in {turn.get("bot") for turn in memory.get("turns") or []}:
        return _vary(["Still " + height + ".", "You said " + height + ".",
                      "It's " + height + " \u2014 that's what you told me."], memory)
    return plain

def _fact_reply(memory, low, key=None):
    if low and A_HOW_TO_ASK.search(str(low)) and not A_RECALL_WORD.search(str(low)):
        return None
    known = user(memory)
    if key == "allergy" or "allerg" in low:
        if ALLERGY_IN_THE_WORLD.search(str(low or "")):
            return None
        allergies = known.get("allergies") or []
        if allergies:
            said = ", ".join(allergies)
            plain = "You told me you're allergic to " + said + "."
            if plain in {turn.get("bot") for turn in memory.get("turns") or []}:
                return _vary(["It's " + said + " — that's what you said.",
                              "Still " + said + ".",
                              "Your allergy is " + said + "."], memory)
            return plain
        if "allergies" in known:
            fixed = memory.get("correction") if isinstance(memory, dict) else None
            gone = str((fixed or {}).get("value") or "").strip().lower()
            if gone and fixed.get("dropped"):
                return "Nothing on the list now — you took the " + gone + " one back."
            return "Nothing on the list now."
        who, theirs = _other_fact(memory, "allergies")
        if theirs and who:
            return _their_allergy(who, theirs)
        if theirs:
            return ("You haven't mentioned one for yourself \u2014 the allergy to "
                    + ", ".join(theirs) + " you mentioned was someone else's.")
        return _deny(memory, "allergy", "You haven't mentioned an allergy to me.")
    if key == "budget" or "budget" in low:
        budget = known.get("budget")
        if not budget:
            return _deny(memory, "budget", "You haven't told me a budget.")
        plain = "Your budget is " + budget + "."
        if plain in {turn.get("bot") for turn in memory.get("turns") or []}:
            return _vary(["It's " + budget + " — that's what you told me.",
                          "You said " + budget + ".", "Still " + budget + "."], memory)
        return plain
    if key == "birthday":
        return _birthday_reply(memory)
    if key == "weight":
        return _weight_reply(memory)
    if key == "height":
        return _height_reply(memory)
    if key == "diet" or (DIET_ASK.search(low) and not DIET_HOW_TO.search(low)):
        return _diet_reply(memory, low)
    if key == "car" or recall.DRIVE_ASK.search(low):
        car = known.get("car")
        if car:
            return car_line(car)
        return pick(["You haven't told me what you drive.",
                     "I don't know your car \u2014 you haven't said."], memory)
    pets = known.get("pets") or []
    gone = [p for p in (known.get("pets_gone") or []) if isinstance(p, dict)]
    asked = None
    for animal, words in (("dog", "dog puppy"), ("cat", "cat kitten"),
                          ("rabbit", "rabbit bunny"), ("hamster", "hamster"),
                          ("fish", "fish goldfish"), ("horse", "horse pony"),
                          ("parrot", "parrot bird")):
        if re.search(r"\b(?:" + words.replace(" ", "|") + r")s?\b", low):
            asked = animal
            pets = [p for p in pets if _animal_family(p.get("animal")) == animal]
            gone = [p for p in gone if _animal_family(p.get("animal")) == animal]
            break
    coming_only = [p for p in pets if isinstance(p, dict) and p.get("coming")]
    if coming_only and len(coming_only) == len(pets) and not re.search(r"\b(?:called|name)\b",
                                                                     low):
        pieces = []
        for pet in coming_only:
            count = pet.get("count") if isinstance(pet.get("count"), int) else 1
            pieces.append(_many(count, pet.get("animal") or "pet") if count > 1 else _a_pet(pet))
        due = _put_together(pieces)
        if due:
            return "You're getting " + due + "."
    counted = _a_count_ask(low)
    if pets and counted is not None:
        kinds = {_animal_family(p.get("animal")) for p in pets}
        total = _count_of_a_kind(pets)
        if len(kinds) == 1 and (counted in ("any", "pet") or kinds == {counted}):
            animal = _animal_family(pets[0].get("animal"))
            if total == 1:
                was = _called(pets[0].get("name"))
                if was:
                    return "You've got one " + animal + " \u2014 " + was + "."
                return "You've got " + _a(animal) + "."
            return "You've got " + _a_pet({"animal": animal, "count": total}) + "."
    if pets:
        if re.search(r"\b(?:called|name)\b", low) and not any(p.get("name") for p in pets):
            return "You haven't told me a name for your " + pets[0].get("animal", "pet") + " yet."
        together = _pets_together(pets)
        if together:
            return "You've got " + together + "."
        counted = bool(re.search(r"\bhow many\b", low))
        if counted and len(pets) == 1:
            pet = pets[0]
            animal = pet.get("animal") or "pet"
            number = pet.get("count") if isinstance(pet.get("count"), int) else 1
            number = max(int(number), 1)
            many = _many(number, animal) if number > 1 else "one " + animal
            was = _called(pet.get("name"))
            return "You've got " + many + (" — " + was + "." if was else ".")
        if counted and len(pets) > 1 and len({_animal_family(p.get("animal")) for p in pets}) == 1:
            top = max([p["count"] for p in pets if isinstance(p.get("count"), int)] or [0])
            if top >= len(pets):
                return "You've got " + _many(top, pets[0].get("animal") or "pet") + "."
        parts = [(_many(p["count"], p.get("animal") or "pet")
                  if counted and isinstance(p.get("count"), int) and p["count"] > 1
                  else _a_pet(p)) for p in pets]
        here = [part for pet, part in zip(pets, parts) if not pet.get("coming")]
        due = [part for pet, part in zip(pets, parts) if pet.get("coming")]
        said = []
        if here:
            said.append("You've got " + _put_together(here) + ".")
        if due:
            said.append("You're getting " + _put_together(due) + ".")
        if said:
            return " ".join(said)
    if gone:
        was_called = re.search(r"\b(?:was|were|did)\b", low) and re.search(
            r"\b(?:call|called|name|named)\b", low)
        named = [pet for pet in gone if pet.get("name")]
        if was_called and named:
            return _was_called(named)
        return _a_pet_that_is_gone(gone)
    if asked:
        theirs = [_a(p.get("animal", "pet")) + (" called " + _called(p.get("name"))
                  if p.get("name") else "") for p in (known.get("pets") or [])]
        if theirs:
            return ("I don't have " + _a(asked) + " from you \u2014 " + " and ".join(theirs)
                    + " is what I have.")
    return "You haven't told me about a pet yet."

def _was_called(named):
    if len(named) == 1:
        return ("Your " + str(named[0].get("animal") or "pet") + " was called "
                + _called(named[0].get("name")) + ".")
    parts = [str(pet.get("animal") or "pet") + " " + _called(pet.get("name")) for pet in named]
    return "You called them " + ", ".join(parts[:-1]) + " and " + parts[-1] + "."

def _a_pet_that_is_gone(gone):
    def one(pet):
        animal = str(pet.get("animal") or "pet")
        name = _called(pet.get("name"))
        return animal + " " + name if name else animal

    shown = [one(pet) for pet in gone]
    if len(shown) > 2:
        which = "any pets"
    elif len(shown) == 2:
        which = "your " + shown[0] + " or your " + shown[1]
    else:
        which = "your " + shown[0]
    if all(pet.get("gone") == "died" for pet in gone):
        return "I'm sorry \u2014 you told me " + which + " died."
    if not any(pet.get("gone") == "died" for pet in gone):
        return "You told me you don't have " + which + " any more."
    told_died = ["your " + shown[index] for index, pet in enumerate(gone)
                 if pet.get("gone") == "died"]
    return ("I'm sorry \u2014 you told me "
            + (" or ".join(told_died) if len(told_died) > 1 else told_died[0]) + " died.")

def _put_together(parts):
    parts = [part for part in parts if part]
    if not parts:
        return ""
    if len(parts) == 1:
        return parts[0]
    return ", ".join(parts[:-1]) + " and " + parts[-1]

def _pets_together(pets):
    animals = [(p.get("animal") or "pet") for p in pets]
    if len(pets) < 2 or len(set(animals)) != 1:
        return None
    if not all(not p.get("count") for p in pets):
        return None
    named = [p for p in pets if p.get("name")]
    nameless = [p for p in pets if not p.get("name")]
    if not named:
        return None
    animal = animals[0]
    many = animal if animal.endswith(("fish", "sheep", "deer")) else animal + "s"
    count = len(pets)
    names = [_called(p.get("name")) for p in named]
    if len(nameless) == 1:
        return (NUMBER_WORDS.get(count, str(count)) + " " + many + " \u2014 "
                + _put_together(names + ["one you haven't named"]))
    if len(nameless) > 1:
        return None
    return (NUMBER_WORDS.get(count, str(count)) + " " + many + " called "
            + ", ".join(names[:-1]) + " and " + names[-1])

def _a_pet(pet):
    animal = str(pet.get("breed") or pet.get("animal") or "pet")
    count = pet.get("count") or 1
    if pet.get("name"):
        try:
            many = int(count) > 1
        except (TypeError, ValueError):
            many = False
        if many:
            plural = animal if animal.endswith(("fish", "sheep", "deer")) else animal + "s"
            return (NUMBER_WORDS.get(int(count), str(count)) + " " + plural + ", one called "
                    + _called(pet.get("name")))
        return _a(animal) + " called " + _called(pet.get("name"))
    if int(count) > 1:
        many = animal if animal.endswith(("fish", "sheep", "deer")) else animal + "s"
        return NUMBER_WORDS.get(int(count), str(count)) + " " + many
    return _a(animal)

ADVICE_ASK = re.compile(
    r"\bdo i (?:need|have) to\b|\bshould i\b|\bhow (?:often|much|long|many)\b|"
    r"\bwhen (?:should|do|can|must) i\b|\bcan i\b|\bis it (?:ok|okay|fine|safe)\b|"
    r"\bwhat (?:should|can|could) i (?:do|feed|give|use|buy|get)\b|\bhow (?:do|can) i\b")

def _a_why_line_they_have_answered(text, memory):
    low = " ".join(str(text or "").lower().split())
    return bool(re.search(r"\bwhy\b", low)) and _holds_the_subject(memory, text)

def _holds_the_subject(memory, text):
    key = recall.ask(text, why=True)
    if not key:
        return False
    known = user(memory) or {}
    held = known.get(_SUBJECT_KEYS.get(key, key))
    if key == "limit":
        return bool(held or known.get("diet") or known.get("limits"))
    return bool(held)

def _asks_for_a_fact(low, text="", memory=None):
    if re.search(r"\bmy (?:dog|cat|pet)s?\b", low) and ADVICE_ASK.search(low):
        return False
    if re.search(r"\bwhy\b", low):
        return _holds_the_subject(memory, text)
    if re.search(r"\bmy (?:dog|cat|pet)s?\b|\ballerg\w*\b|\bmy budget\b", low):
        return True
    if re.search(r"\bwhat (?:did|have) i\b", low):
        return False
    return bool(ASK_WITHOUT_MY.search(low))

def _vary(options, memory):
    turns = memory.get("turns") or []
    recent = {t.get("bot") for t in turns[-5:]}
    fresh = [o for o in options if o not in recent] or list(options)
    return random.Random(len(turns)).choice(fresh)

def _turn_lines(memory):
    lines = []
    for turn in memory.get("turns") or []:
        if isinstance(turn, dict):
            lines.append((str(turn.get("user") or ""), str(turn.get("bot") or "")))
    return lines

def _repeat_ask(text, low, memory=None):
    if WHOLE_ASK.match(str(low or "").strip()):
        return True if memory is None else _a_whole_answer_to_hand_back(memory, text)
    if not REPEAT_ASK.search(low) or not REPEAT_START.match(low):
        return False
    return set(keywords(REPEAT_TAIL.sub(" ", low))) <= REPEAT_WORDS

FIGURE_REPEAT = re.compile(
    r"\b(?:how long|how many|how often|how soon|what time|what temperature|"
    r"which temperature|what setting|how hot|when)\b")

def asks_again(text, memory=None):
    low = str(text or "").strip().lower()
    return bool(low) and _repeat_ask(low, low, memory)


def _repeat_reply(memory, text=""):
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    said = [turn for turn in turns if str(turn.get("bot") or "").strip()]
    whole = bool(WHOLE_ASK.match(str(text or "").strip().lower()))
    if said and named_thing.takes_back(said[-1].get("user")):
        answered = [turn for turn in said[:-1]
                    if not named_thing.takes_back(turn.get("user"))]
        said = answered or said
    if not said:
        return _vary(["I haven't said anything yet — you go first.",
                      "Nothing from me so far. What would you like to talk about?"], memory)
    line = str((memory.get("understood") or {}).get("text") or "")
    about = _hearing_again(said, line)
    if whole and (about is None or about.get("module") not in ANSWER_MODULES):
        return None
    if about is None:
        return _vary(["Nothing from me on that yet. What were you asking about?",
                      "I haven't given you an answer on that yet. What is it you want to know?",
                      "Nothing of mine to give back there yet - what was the question?"], memory)
    if (FIGURE_REPEAT.search(str(text or "")) and not re.search(r"\d", str(about.get("bot") or ""))
            and about.get("module") not in ANSWER_MODULES):
        return _vary(["I haven't said a length yet - what are you timing?",
                      "Nothing with a time in it from me so far. What are you looking at?"], memory)
    last = str(about.get("bot") or "")
    from ..memory import again as same_again
    base = same_again.unframed(last) or last
    base = re.sub(r"^(?:sure|again|of course)\s*[—-]\s*|^here it is again:\s*", "", base,
                  flags=re.I)
    if FIGURE_REPEAT.search(str(text or "")):
        figure = narrow.narrow(str(base), str(text or ""))
        if isinstance(figure, str) and figure.strip():
            base = figure.strip()
    if about.get("module") not in ANSWER_MODULES:
        return base
    if WHOLE_ASK.match(str(text or "").strip().lower()):
        return _vary(["All of it: " + base, "Here it is in full: " + base,
                      "The whole of it, then: " + base], memory)
    return _vary(["Sure — " + base, "Again — " + base, "Here it is again: " + base, base],
                 memory)

ANSWER_MODULES = frozenset(("answers", "loss", "grief", "safety", "urgent"))

def _a_whole_answer_to_hand_back(memory, text=""):
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    said = [turn for turn in turns if str(turn.get("bot") or "").strip()]
    if not said:
        return False
    if named_thing.takes_back(said[-1].get("user")):
        said = [turn for turn in said[:-1]
                if not named_thing.takes_back(turn.get("user"))] or said
    about = _hearing_again(said, str(text or ""))
    return about is not None and about.get("module") in ANSWER_MODULES

def _carries_something(turn):
    reply = str(turn.get("bot") or "").strip()
    if not reply:
        return False
    if _about_this_chat(str(turn.get("user") or "")):
        return False
    return turn.get("module") in ANSWER_MODULES or len(reply.split()) >= 8

NOD_WORDS = frozenset("""thanks ta thx ty thank you cheers much so very really that this helps
                         helped for the lot got it ok okay k kk great nice brilliant awesome
                         perfect lovely cool fair enough right alright indeed yes yeah yep
                         sure fine good ah oh""".split())

def _only_a_nod(line):
    found = re.findall(r"[a-z']+", str(line or "").lower())
    if not found or len(found) > 4:
        return False
    return all(word in NOD_WORDS for word in found)

def _hearing_again(said, line):
    if LAST_LINE_ASK.search(str(line or "")):
        return said[-1]
    live = [turn for turn in said if not _only_a_nod(turn.get("user"))]
    if live and len(live) < len(said):
        said = live
    answered = [turn for turn in said if not _about_this_chat(str(turn.get("user") or ""))]
    if answered and len(answered) < len(said):
        said = answered
    if not thread.thin(str(said[-1].get("user") or "")):
        return said[-1]
    answering = [turn for turn in said if turn.get("module") in ANSWER_MODULES]
    if answering:
        return answering[-1]
    carrying = [turn for turn in said if _carries_something(turn)]
    if carrying:
        return carrying[-1]
    return None

HELLO_FILLER = frozenset("""there all everyone everybody both you folks guys again friend
friends mate team""".split())

def _just_a_hello(line):
    if "?" in line:
        return False
    found = re.findall(r"[a-z']+", line.lower())
    return bool(found) and any(w in GREET for w in found) and all(
        w in GREET or w in ACKS or w in HELLO_FILLER for w in found)

def _worth_reporting(line):
    return bool(line) and not _just_a_hello(line) and not history.not_a_subject(line)

def _first_reply(memory):
    lines = _turn_lines(memory)
    if not lines or not lines[0][0]:
        return _vary(["You haven't said anything yet, so this is the start.",
                      "We're just beginning — you go first."], memory)
    said = [line for line, _ in lines if _worth_reporting(line)]
    if not said:
        return _vary(["We've only just started — nothing of yours to look back on yet.",
                      "Only hellos so far: your first proper line is still to come.",
                      "Nothing of yours to report back yet — you've only said hello."], memory)
    first = said[0]
    options = ["You started with: \"" + _trim(first) + "\"",
               "Your first line was: \"" + _trim(first) + "\"",
               "That's how we opened: \"" + _trim(first) + "\""]
    if len(said) <= 1:
        options.append("This chat opened with: \"" + _trim(first) + "\" — not much else yet.")
    return _vary(options, memory)

def _what_i_said_about(memory, thing):
    words = {word for word in keywords(thing or "") if word not in STOPWORDS}
    if not words:
        return None
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    for turn in reversed(turns):
        if str(turn.get("module") or "") in ("safety", "urgent", "grief", "loss"):
            return None
        said = str(turn.get("bot") or "").strip()
        asked = str(turn.get("user") or "")
        if not said:
            continue
        opening = re.split(r"(?<=[.!?])\s+", said)[0]
        in_answer = words <= {word for word in keywords(opening)}
        in_question = words <= {word for word in keywords(asked)}
        if not _carries_something(turn) or not _adds_something(said, asked):
            continue
        if not (in_answer or in_question):
            continue
        parts = re.split(r"(?<=[.!?])\s+", said)
        sentence = parts[0].strip()
        if len({word for word in keywords(sentence)} - NOD_WORDS) <= 2 and len(parts) > 1:
            sentence = sentence + " " + parts[1].strip()
        if not sentence or len(sentence.split()) > 45:
            sentence = " ".join(sentence.split()[:45]).rstrip(",;:") + "..."
        name = " ".join((thing or "").split())
        return pick(["On " + name + ": " + sentence,
                     "I said: " + sentence,
                     "What I said about " + name + ": " + sentence], memory)
    if len(words) <= 4:
        name = " ".join((thing or "").split())
        return pick(["I don't think we've been over " + name + " yet - what do you want to know?",
                     "We haven't got to " + name + " yet. Ask me and I'll say what I know.",
                     name[:1].upper() + name[1:] + " hasn't come up yet - ask away."], memory)
    return None

def _adds_something(said, asked):
    said_words = {word for word in keywords(said)} - NOD_WORDS
    asked_words = {word for word in keywords(asked)}
    return bool(said_words - asked_words)

def _first_bot_reply(memory):
    first = _first_sentence(history.first_bot_line(memory))
    if not first:
        return "I haven't said anything yet — you go first."
    return _vary(["I opened with: \"" + first + "\"",
                  "My first line was: \"" + first + "\"",
                  "I started with: \"" + first + "\""], memory)

def _asked_and_answered(memory):
    for seen in reversed(recent(memory, 8)):
        line = str(seen.get("user") or "")
        if line and not _about_this_chat(line):
            return line, str(seen.get("bot") or "").strip()
    return "", ""

THEIR_OWN_ASK = re.compile(r"\b(?:i|me|my|mine|we|our|ours)\b", re.I)

def _said_reply(memory):
    last = last_user(memory)
    if not last:
        return "That was your first line — there's nothing before it."
    real = _last_real(memory)
    if real and _just_a_hello(real):
        real = ""
    if real:
        last = real
    elif _asks(last):
        asked, mine = _asked_and_answered(memory)
        if not asked:
            for seen in reversed(recent(memory, 2)):
                line = str(seen.get("user") or "")
                if line and not SAID_ASK.search(line.lower()) and not FIRST_ASK.search(line.lower()):
                    asked, mine = line, str(seen.get("bot") or "").strip()
                    break
        again = _about_this_chat(last)
        nothing_yet = not real and (bool(history.not_a_subject(asked))
                                    or bool(THEIR_OWN_ASK.search(asked or "")))
        if mine and (nothing_yet or (not _just_a_hello(asked)
                                     and (again or len(mine.split()) > A_SHORT_ANSWER))):
            asked = _trim(asked).rstrip(" .!?")
            first = re.split(r"(?<=[.!?])\s+", mine)[0].strip()
            return _vary(["You asked: \"" + asked + "\" — I said: " + first,
                          "That one was your question: \"" + asked + "\". My answer: " + first,
                          "You asked \"" + asked + "\", and what I said was: " + first],
                         memory)
        return None
    else:
        return _summary_reply(memory)
    fixed = memory.get("correction") if isinstance(memory, dict) else None
    fixed_words = " ".join(str((fixed or {}).get("sentence") or (fixed or {}).get("value") or "")
                           .split())
    if isinstance(fixed, dict) and fixed_words \
            and fixed.get("said") == " ".join(str(last).lower().split()):
        said = fixed_words.rstrip(" .!?")
        return _vary(["You said " + said + " — you put me right on it.",
                      "You said " + said + ", and that is the version I am going with.",
                      "\"" + said + "\" — your first line, put right a moment later."], memory)
    return _vary(["You said: \"" + _trim(last) + "\"",
                  "Your last line was: \"" + _trim(last) + "\"",
                  "That was: \"" + _trim(last) + "\""], memory)

ASKS_IN_LINE = re.compile(r"[,;:\u2013\u2014-]\s*(?:what|whats|why|how|hows|when|where|wheres|who|"
                          r"which|whose|can|could|should|would|do|does|did|is|are|was|were|will|"
                          r"shall|have|has)\b", re.I)

CORRECTS = re.compile(r"\b(?:rather than|instead of|scratch that|or rather)\b|"
                      r"\bi (?:meant|mean)\b|\bnot\s+(?:the\s+)?\w+\s*[.!]?$", re.I)

def _corrects(line):
    return bool(CORRECTS.search(" ".join((line or "").lower().split())))

def _last_real(memory):
    for seen in reversed(recent(memory, 8)):
        line = seen.get("user") or ""
        if line and not _about_this_chat(line) and not _asks(line):
            return line
    return ""

SAID_ABOUT = re.compile(
    r"\bwhat (?:was|were|am|are) (?:i|we) (?:saying|talking|chatting|on)\b[^.?!]*\babout\b",
    re.I)

DENIAL = re.compile(
    r"\bhaven't said anything\b|\bhaven't mentioned\b|\bnothing comes to mind\b", re.I)

def _the_fact_is_kept(key, memory):
    slot = KEY_SLOT.get(key)
    return bool(slot and user(memory).get(slot))

def _a_denial(reply):
    return bool(reply) and bool(DENIAL.search(reply))

def _names_its_thing(low):
    after = re.search(r"\babout\b\s+(.+)$", low or "")
    if not after:
        return False
    thing = re.sub(r"\b(?:again|before|earlier|please|so far|up to now|until now)\b",
                   "", after.group(1)).strip(" ?!.,")
    if not content(thing) or thing in ("it", "that", "this", "them", "that one"):
        return False
    return True

def _say_back(line, memory=None):
    said = (thread.restate(line) or _recap(line) or "").strip().rstrip(".")
    if not said:
        return _recall_quote(line, memory)
    said = said[:1].lower() + said[1:]
    return _vary(["You said " + said + ". Want to carry on?",
                  "You said " + said + "."], memory)

REFLEXIVE = frozenset(("myself", "yourself", "ourselves", "themselves"))

def _recall_reply(memory, low, text="", spoken=False):
    hurt = a_hurting_part.what_is_hurting_reply(memory, low)
    if hurt:
        return hurt
    about = re.search(r"\babout\b(.*)$", low)
    part = None if about else _which_thing_was_it(low, memory)
    if about:
        thing = about.group(1)
    elif part:
        thing = part
    else:
        after = re.search(r"\b(?:say|said|tell you|told you|mention)\b(.*)$", low)
        thing = after.group(1) if after else ""
    mine = re.search(r"\babout\b(.*)$", text or "", re.I)
    shown = (mine.group(1) if mine else thing).strip(" ?!.,")
    thing = re.sub(r"\b(?:again|before|earlier|please|so far|up to now|until now)\b",
                   "", thing).strip(" ?!.,")
    if thing.lower() in REFLEXIVE:
        return None
    if not content(thing):
        named = THING_AGAIN.match(low)
        if named:
            thing = named.group(1)
        else:
            reminded_thing = reminded.the_thing(text or low, memory)
            if reminded_thing:
                thing = reminded_thing
    if re.match(r"to\s+(?!me\b|you\b)", thing):
        return None
    if recall.LIVING.search(thing):
        return None
    words = content(thing)
    if not words or thing in ("it", "that", "this", "them", "that one"):
        real = _last_real(memory)
        if real:
            return _recall_quote(real, memory)
        record = current(memory)
        if record and record.get("text") and not _about_this_chat(record["text"]):
            return _recall_quote(record["text"], memory, asked=_asks(record["text"]))
        return pick(["You haven't told me anything about that yet.",
                     "Nothing comes to mind \u2014 you haven't said."], memory)
    hits, asked, fixed, claims = [], [], [], []
    for turn in _every_line(memory):
        line = turn.get("user") or ""
        if not line or _about_this_chat(line):
            continue
        seen = _seen(line)
        question = _asks(line)
        if all(_alike(word, seen) or (not question and _about_kind(word, line, memory))
               for word in words):
            (asked if _asks(line) else fixed if _corrects(line) else
             claims if A_CLAIM_OF_TELLING.match(" ".join(line.lower().split())) else
             hits).append(line)
    if not hits and claims:
        hits = claims
    if hits:
        stated = [line for line in hits if not ASKS_IN_LINE.search(line)]
        if stated:
            hits = stated
        if not spoken:
            put_right = _put_right_after_it(hits[-1], memory)
            if put_right:
                return put_right
            moved = _a_figure_put_right(hits[-1], memory)
            if moved:
                return moved
            narrowed = _a_narrowing_put_after(hits[-1], memory)
            if narrowed:
                return narrowed
        return _say_back(hits[-1], memory) if spoken else _recall_quote(hits[-1], memory)
    if asked:
        return _recall_quote(asked[-1], memory, asked=True)
    if fixed:
        return _recall_quote(fixed[-1], memory)
    naming = [word for word in words if word not in JUDGING and word not in A_ROLE]
    if naming and naming != words:
        naming_hits, naming_asked = [], []
        for turn in recent(memory, 8):
            line = turn.get("user") or ""
            if not line or _about_this_chat(line):
                continue
            seen = _seen(line)
            if all(_alike(word, seen) for word in naming):
                (naming_asked if _asks(line) else naming_hits).append(line)
        if naming_hits:
            return _recall_quote(naming_hits[-1], memory)
        if naming_asked:
            return _recall_quote(naming_asked[-1], memory, asked=True)
    if not naming and PRONOUN_ASK.search(thing):
        real = _last_real(memory)
        if real and len(content(real)) > 1:
            return _recall_quote(real, memory)
    if not about:
        return None
    said = re.sub(r"^my\b", "your", shown).strip()
    return pick(["You haven't said anything to me about " + said + " yet.",
                 "You haven't mentioned " + said + " \u2014 say it and I'll keep it."], memory)

JUDGING = frozenset((
    "wrong", "bad", "good", "best", "worst", "right", "nice", "like", "dislike", "much", "many",
    "long", "often", "soon", "far", "big", "small", "else", "other", "another", "next", "first",
    "last", "again", "exactly", "actually", "really", "truly"))

A_ROLE = frozenset((
    "guest", "guests", "person", "people", "someone", "somebody", "man", "woman", "guy",
    "bloke", "lad", "friend", "colleague", "member", "kid", "child", "children", "folk"))

PRONOUN_ASK = re.compile(r"\b(?:it|its|that|this|them|those)\b")

TAGS = (
    ("holiday", re.compile(r"\b(?:going|gone|flew|flying|off|travell?ing|travel)\s+to\s+"
                          r"(?!the\b|a\b|an\b|my\b|our\b|his\b|her\b|their\b|work\b)"
                          r"|\babroad\b|\bholiday\b", re.I)),
)

def _tagged(line):
    low = str(line or "")
    return {concept for concept, pattern in TAGS if pattern.search(low)}

def _the_same_person(who):
    who = str(who or "").strip().lower()
    if not who:
        return []
    concept = CONCEPTS.get(who)
    words = [who]
    if concept:
        words += [word for word, its in CONCEPTS.items() if its == concept and word != who]
    return words

A_PROGRAMME_IS_ON = re.compile(
    r"\b(?:is|was|are|were)\s+(?:on|back on)\s+(?:tonight|now|tv|telly|later|this evening|"
    r"last night|tomorrow|at \d|bbc|itv|channel|netflix|prime)\b", re.I)

def _the_name_pattern(who):
    called = "(?:" + "|".join(re.escape(word) for word in _the_same_person(who)) + ")"
    not_a_relation = r"(?!\s*-?\s*in\s*-?\s*law)"
    return re.compile(r"\b(?:my|our)\s+" + called + not_a_relation + POSSESSIVE + r"\b|"
                      r"(?:^\s*|[,;]\s*|\b(?:and|but|also|then)\s+)" + called
                      + not_a_relation + POSSESSIVE + r"\b", re.I)

PERSON_STANDS = re.compile(
    r"(?:^\s*|[,.;:!?)—]|\b(?:is|are|was|were|has|have|had|does|do|did|can|could|will|would|"
    r"shall|should|might|must|needs?|needed|wants?|wanted|says?|said|said|called|rang|phoned|"
    r"texted|loves?|likes?|hates?|came|comes?|coming|went|goes|going|got|gets|getting|thinks?|"
    r"thought|knows?|knew|feels?|felt|feeling|worried|ill|unwell|poorly|sick|poor|well|fine|"
    r"who|that|which|and|too|as|again|now)\b|$)", re.I)

def _the_word_for_them(who):
    words = "|".join(re.escape(word) for word in _the_same_person(who))
    return re.compile(r"\b(?:" + words + r")" + POSSESSIVE + r"\s*" + PERSON_STANDS.pattern, re.I)

KINDS = (
    ("trip", frozenset("trip trips holiday holidays vacation getaway break travel journey flight"
                        " abroad".split())),
    ("job", frozenset("job jobs work career shift shifts employment".split())),
    ("food", frozenset("food foods diet meals meal dinner tea supper lunch breakfast eating"
                       " cooking".split())),
    ("home", frozenset("live lives living home house city town address moved move moves"
                       " moving".split())),
)

SAYS_A_TRIP = re.compile(r"\b(?:holidays?|vacation|getaway|abroad|trips?|travell?ing|flight|flying|"
                         r"cruise|week away)\b", re.I)

NOT_A_PLACE_IN = frozenset("""bed pain limbo prison hospital hospice traction tears denial
hiding isolation quarantine plaster shock mourning""".split())

SAYS_A_STAY = re.compile(
    r"\b(?:a |the )?(?:few |couple of |two |three |four |five )?(?:days?|nights?|weeks?|weekend)"
    r"\s+(?:away\s+)?in\s+(?:(?:the|a|an)\s+)?(?P<place>[a-z]{3,})", re.I)

def _a_stay_in_a_place(text):
    for found in SAYS_A_STAY.finditer(text):
        word = found.group("place").lower()
        if word in extract.NOT_PLACES or word in NOT_A_PLACE_IN:
            continue
        return True
    return False

SAYS_A_JOB = re.compile(r"\b(?:job|jobs|work|working|career|shift|shifts|office|employ\w*|"
                        r"promotion|interview|colleagues?)\b", re.I)

SAYS_FOOD = re.compile(
    r"\b(?:eat|eats|eating|eaten|ate|drink|drinks|drinking|drank)\b|"
    r"\b(?:vegetarian|vegan|pescatarian|diet|allerg\w+|intoleran\w+|gluten|dairy|sugar|meat|"
    r"fish|carbs?|keto|fasting|booze|alcohol)\b|"
    r"\b(?:cook|cooks|cooking|cooked|bake|baking|roast|recipe)\b", re.I)

SAYS_THE_KIND = {
    "trip": SAYS_A_TRIP,
    "job": SAYS_A_JOB,
    "food": SAYS_FOOD,
}

def _kind(thing):
    for kind, words in KINDS:
        if thing in words:
            return kind
    return ""

def _says_where_they_live(text):
    if not isinstance(text, str) or not text.strip():
        return False
    try:
        found = extract.extract(text)
    except Exception:
        return False
    return bool(found.get("home"))

def _a_place_they_go(text):
    found = extract.PLACE_LOWER.search(text or "")
    if not found:
        return ""
    word = found.group(1).lower()
    if word in extract.NOT_PLACES or word in extract.PLACE_VERBS:
        return ""
    return word

def _about_kind(thing, text, memory=None, phrase=False):
    kind = _kind(thing)
    if not kind or not isinstance(text, str) or not text.strip():
        return False
    said = SAYS_THE_KIND.get(kind)
    if kind == "job":
        return bool(said.search(text))
    if kind == "home":
        return _says_where_they_live(text)
    if kind == "trip" and (SAYS_A_TRIP.search(text) or _a_stay_in_a_place(text)
                            or _a_place_they_go(text)):
        return True
    if said is not None and said.search(text):
        return True
    if not phrase:
        return False
    known = (user(memory).get("places") or []) if isinstance(memory, dict) else []
    low = text.lower()
    return any(str(place).lower() in low for place in known if isinstance(place, str) and place)

def _seen(line):
    words = set(content(line))
    plain = normalise(line or "")
    plain = plain.get("norm_text") if isinstance(plain, dict) else ""
    if plain and plain != line:
        words |= set(content(plain))
    return words | _tagged(line)

def _alike(word, seen):
    want = CONCEPTS.get(word)
    mine = forms(word)
    for other in seen:
        if word == other:
            return True
        if mine & forms(other):
            return True
        if want and want == CONCEPTS.get(other):
            return True
        if len(word) >= 4 and len(other) >= 4 and (word.startswith(other)
                                                  or other.startswith(word)):
            return True
        if len(word) >= 5 and len(other) >= 5 and word[:5] == other[:5]:
            return True
    return False

def _recall_quote(line, memory=None, asked=False):
    said = "\"" + _trim(line, 120) + "\""
    if asked:
        return ASKED_LEADS[(len(recent(memory, 8)) if memory else 0) % len(ASKED_LEADS)] + said
    if memory is None:
        return QUOTE_LEADS[0] + said
    asked = sum(1 for turn in recent(memory, 8)
                if re.search(r"\bwhat (?:did|have) i\b", (turn.get("user") or ""), re.I))
    return QUOTE_LEADS[asked % len(QUOTE_LEADS)] + said

TELLING_ALREADY = re.compile(r"^you (?:told me|said to me|mentioned to me)\b")


A_BARE_PUT_RIGHT = re.compile(
    r"^\s*(?:sorry|no|nah|actually|oh|wait|hang on|hold on|i mean|my mistake|silly me|"
    r"correction)[\s,]*"
    r"(?:(?:its|it's|it was|make that|make it|i mean|should be|thats|that is)\s+)?"
    r"(?:about\s+|only\s+|just\s+)?"
    r"(?P<value>\d[\d,]*(?:\.\d+)?"
    r"(?:\s+and\s+(?:an?\s+)?(?:half|quarter))?)"
    r"(?:\s*(?:%|percent|per\s?cent|pounds?|quid|grand|k|stone|kg|miles?|mph|hours?|"
    r"minutes?|mins?|a\s+(?:month|week|year|day|night|person|guest|head))s?)?"
    r"\s*(?:[,!.]|\b(?:sorry|thanks|actually|i got it wrong|got it wrong|my mistake|silly me|"
    r"i think|i mean|then|right)\b)*\s*$", re.I)

A_FIGURE = re.compile(r"(?<![\w.,£$])(\d[\d,]*(?:\.\d+)?)")

def _a_figure_put_right(line, memory):
    if not isinstance(memory, dict):
        return ""
    said = " ".join(str(line or "").split())
    figures = A_FIGURE.findall(said)
    if len(figures) != 1:
        return ""
    lines = [" ".join(str(turn.get("user") or "").split()) for turn in _every_line(memory)]
    places = [index for index, text in enumerate(lines) if text == said]
    if not places:
        return ""
    for after in lines[places[-1] + 1:places[-1] + 2]:
        found = A_BARE_PUT_RIGHT.match(after.strip())
        if not found:
            continue
        value = found.group("value").strip().rstrip(",")
        if not value or value == figures[0]:
            continue
        return (_recall_quote(line, memory).rstrip()
                + " \u2014 then you put it right: " + value + ".")
    return ""

def _a_narrowing_put_after(line, memory):
    if not isinstance(memory, dict):
        return ""
    pair = _a_narrowing_and_its_line(line, memory)
    if not pair:
        return ""
    before, after = pair
    return (_recall_quote(before, memory).rstrip()
            + " \u2014 then \"" + _trim(after, 80) + "\".")

def _put_right_after_it(line, memory):
    fixed = memory.get("correction") if isinstance(memory, dict) else None
    if not isinstance(fixed, dict):
        return ""
    said_back = " ".join(str(fixed.get("said") or "").lower().split())
    sentence = " ".join(str(fixed.get("sentence") or "").split()).rstrip(" .!?")
    if not (said_back and sentence):
        return ""
    lines = [" ".join(str(turn.get("user") or "").lower().split())
             for turn in _every_line(memory)]
    quoted = " ".join(str(line or "").lower().split())
    if said_back not in lines or quoted not in lines:
        return ""
    if lines.index(quoted) >= lines.index(said_back):
        return ""
    if not (_content_words(line) & _content_words(sentence)):
        return ""
    tail = sentence[0].lower() + sentence[1:]
    return _recall_quote(line, memory).rstrip() + " \u2014 then you put it right: " + tail + "."

def _age_reply(memory):
    age = user(memory).get("age")
    if not age or not 1 <= age <= 120:
        return pick(["You haven't told me your age yet.", "I don't know it — you haven't said."],
                    memory)
    return pick(["You told me you're " + str(age) + ".", str(age) + " — you said."], memory)

def _content_words(line):
    return {word for word in re.findall(r"[a-z']+", line.lower())
            if len(word) > 3 and word not in STOPWORDS}

def _the_line_before_was_a_plan(memory):
    plan = (user(memory) or {}).get("plan")
    if not isinstance(plan, str) or not plan.strip():
        return False
    told = plan_line(memory, plan)
    if not told:
        return False
    return (" ".join(told.lower().split())
            == " ".join(str(last_user(memory) or "").lower().split()))

def _plan_was_corrected(memory):
    changed = memory.get("correction") if isinstance(memory, dict) else None
    if not isinstance(changed, dict):
        return False
    if changed.get("key") in ("plan", "plans"):
        return True
    value = " ".join(str(changed.get("value") or "").lower().split())
    plan = " ".join(str((user(memory) or {}).get("plan") or "").lower().split())
    return bool(value) and bool(plan) and value in plan

def _about_the_same(line, line_words):
    return bool(DETAIL_START.search(line)) or bool(_content_words(line) & line_words)

def _activity_line(memory):
    lines = [" ".join(str(turn.get("user") or "").split()) for turn in recent(memory, 4)]
    changed = memory.get("correction") if isinstance(memory, dict) else None
    fixed = " ".join(str(changed.get("said") or "").split()) if isinstance(changed, dict) else ""
    for wanted in (ACTIVITY_WORDS, ACTIVITY_LOOSE):
        for index in range(len(lines) - 1, -1, -1):
            line = lines[index]
            if not line or ASK_LINE.search(line) or ACTIVITY_ASK.search(line):
                continue
            if not wanted.search(line):
                continue
            words = _content_words(line)
            newer = [later for later in lines[index + 1:] if later]
            if any(fixed and later == fixed for later in newer):
                return ""
            if all(ASK_LINE.search(later) or ACTIVITY_ASK.search(later)
                   or _about_the_same(later, words) for later in newer):
                return line
            return ""
    return ""

ASKING_AGAIN = re.compile(r"\bagain\b|\bremind me\b", re.I)

def _the_making_line_they_said(memory, back=8):
    for turn in reversed(recent(memory, back)):
        line = " ".join(str(turn.get("user") or "").split())
        if not line or ASK_LINE.search(line) or ACTIVITY_ASK.search(line):
            continue
        if ACTIVITY_WORDS.search(line) or ACTIVITY_LOOSE.search(line):
            return line
    return ""

def _recap(line):
    flat = " ".join(str(line or "").split()).strip(" .")
    planned = re.match(r"^(?:im|i'm|i am|ive|i've|were|we're|we are)\s+(\S.*)$", flat, re.I)
    if planned:
        body = "you're " + planned.group(1)
    else:
        wanted = re.match(r"^i\s+(?:want|need|plan)\s+to\s+(\S.*)$", flat, re.I)
        if not wanted:
            return ""
        body = "you want to " + wanted.group(1)
    body = _tidy_words(you(body))
    return body[:1].upper() + body[1:]

def _tidy_words(text):
    ORDINARY = ("a", "an", "the", "my", "your", "our", "his", "her", "their", "this", "that")
    BOTH = frozenset(("turkey", "china", "bath", "hull", "york", "goa"))
    TRAVEL = ("to", "in", "from", "at", "near", "visit", "visiting", "into")

    def keep(match):
        word = match.group(0)
        if word not in extract.COUNTRIES and word not in extract.MONTHS and word not in PLACES:
            return word
        before = text[:match.start()].split()
        if before and before[-1].lower() in ORDINARY:
            return word
        if word in BOTH and not (before and before[-1].lower() in TRAVEL):
            return word
        return word[:1].upper() + word[1:]
    return re.sub(r"[a-z]+", keep, text)

def _a_thing(name):
    words = str(name or "").split()
    if not words:
        return False
    head = words[-1].lower().strip(".,;:!?")
    if not head:
        return False
    if head.endswith(("ing", "ed", "ish")):
        return False
    return head not in thread.QUALITY and head not in thread.NON_NOUN

THING_POINTER = frozenset(
    "the a an my your our their his her its it this that of on in at for to with about".split())

def _says_the_thing(said, thing):
    named = {w for w in re.findall(r"[a-z']+", str(thing or "").lower()) if w not in THING_POINTER}
    return bool(named) and bool(named & set(re.findall(r"[a-z']+", str(said or "").lower())))

def _a_description(thing):
    words = str(thing or "").strip().split()
    if len(words) < 2:
        return False
    return words[0].lower() in ("the", "a", "an")

def _the_fixed_fact(memory):
    fixed = memory.get("correction") if isinstance(memory, dict) else None
    if not isinstance(fixed, dict):
        return None
    key = str(fixed.get("key") or "").strip()
    value = str(fixed.get("value") or "").strip()
    said = str(fixed.get("said") or "").strip()
    if not key or not value:
        return None
    if said and last_user(memory).strip().lower() != said.lower():
        return None
    sentence = _fact_reply(memory, " ".join(_slot_words(key, memory).split()), key=key)
    sentence = str(sentence or "").strip()
    if not sentence.startswith(("Your ", "You ")):
        return None
    return sentence[:1].lower() + sentence[1:].rstrip(".")

def _the_line_named(memory, low):
    about = re.search(r"\babout\s+(.*)$", low or "")
    if not about:
        return ""
    words = content(about.group(1))
    if not words:
        return ""
    for seen in reversed(recent(memory, 8)):
        line = seen.get("user") or ""
        if not line or _about_this_chat(line):
            continue
        have = set(content(line))
        if have and all(_alike(word, have) for word in words):
            return line
    return ""

def _topic_reply(memory, low, again=False):
    record = current(memory)
    real = _last_real(memory)
    if real:
        record = {"text": real}
    last = last_user(memory)
    on_that_line = _the_line_named(memory, low)
    said_again = (_the_fixed_fact(memory)
                  or (thread.restate(on_that_line) if on_that_line else "")
                  or thread.last_said(memory, _about_this_chat))
    if said_again and len(said_again.split()) < 2:
        said_again = None
    if "yesterday" in low:
        said = (" In this one, you last said " + said_again + "." if said_again else "")
        return "I don't keep yesterday's chat, sorry — each conversation starts fresh for me." + said
    if _names_its_thing(low):
        by_name = _recall_reply(memory, low, spoken=True)
        if by_name and not _a_denial(by_name):
            return by_name
    named = NAMED_ACTIVITY.search(low or "")
    carried = _activity_line(memory) if ACTIVITY_ASK.search(low or "") else ""
    if not carried and named and again:
        carried = _the_making_line_they_said(memory)
    if not carried and named:
        return None
    if carried:
        said_plan = _recap(carried) or ("You said: \"" + _trim(carried) + "\"")
        said_plan = said_plan.rstrip(".") + "."
        return _vary([said_plan + " Want to carry on with it?",
                      said_plan + " Where did you get to with it?",
                      said_plan], memory)
    thing = thread.about(memory, _about_this_chat)
    if not _a_thing(thing):
        thing = None
    ask = "" if on_that_line else thread.last_ask(
        memory, _about_this_chat,
        not_before=thread.topic_index(memory, _about_this_chat))
    if thing and ask and not (_a_description(thing) and (
            _says_the_thing(said_again, thing) or _says_the_thing(ask, thing))):
        return _vary(["We were on " + thing + " — you asked " + ask + ". Want to carry on?",
                      "Still on " + thing + ": you asked " + ask + ".",
                      "The last thing we got into was " + thing + ", and you asked " + ask + "."],
                     memory)
    if ask and said_again:
        return _vary(["You said " + said_again + ". You asked " + ask + ". Want to carry on?",
                      said_again[:1].upper() + said_again[1:] + " - and you asked " + ask
                      + ". Want to carry on?"], memory)
    if ask:
        return _vary(["You asked " + ask + ". Want to carry on?",
                      "You were asking " + ask + "."], memory)
    if said_again:
        return _vary(["You said " + said_again + ". Want to carry on?",
                      "You last said " + said_again + ".",
                      "You'd told me " + said_again + "."], memory)
    if thing:
        return _vary(["We were on " + thing + ".", "Still " + thing + "."], memory)
    if record and not thread.thin(record["text"]) and thread.carries_subject(record["text"]):
        plain = thread.restate(record["text"])
        if plain and _a_thing(plain):
            return "We were on " + plain + "."
    asked_of_me = _the_last_ask_about_the_bot(memory)
    if asked_of_me:
        return _vary(["You asked " + asked_of_me + " - that is all we have been into so far. "
                      "What else is on your mind?",
                      "So far you have asked " + asked_of_me + ". Tell me something of your own "
                      "and I will keep it.",
                      "You asked " + asked_of_me + ". That is about all so far - what else are "
                      "you wondering about?"], memory)
    return _vary(NOTHING_STARTED, memory)

def _the_last_ask_about_the_bot(memory):
    for text, reading in reversed(list(thread.user_lines(memory))):
        if not (isinstance(reading, dict) and reading.get("about_bot")):
            return None
        asked = thread.restate(text)
        if asked:
            return asked
    return None

def _asked_reply(memory):
    ask = thread.last_ask(memory, _about_this_chat)
    if ask:
        return "You asked " + ask + "."
    said = thread.last_said(memory, _about_this_chat)
    if said:
        return "You didn't ask me anything — you said " + said + "."
    asked_of_me = _the_last_ask_about_the_bot(memory)
    if asked_of_me:
        return "You asked " + asked_of_me + "."
    return "You haven't asked me anything yet."

SMALL_TALK_ONLY = frozenset("""hi hello hey morning afternoon evening night thanks thank cheers
bye goodbye ok okay cool nice great good fine yeah yes no nah lol haha hmm well anyway
brilliant lovely""".split())

SUMMARY_FILLER = frozenset("""you your yours i me my mine and so but it its it's is was are were
be been am do did does have has had to of in on at for with that this these those the a an
too also just really very quite still now then there here""".split())

def _last_told(memory):
    record = current(memory)
    candidates = [str((record or {}).get("text") or "")]
    candidates += [str(line or "") for line in reversed(last_user(memory, 3))]
    for text in candidates:
        if recall.ask(text) == "me":
            continue
        phrase = _told_phrase(text)
        if phrase:
            return phrase
    return ""

NAME_SAID = re.compile(r"\b(?:called|named|name(?:'s)? is|goes by)\s+([A-Za-z][\w'\u2019-]*)", re.I)

NOT_A_NAME = frozenset("""a an the that this it him her them me you us someone something
somebody anyone anybody everyone nobody""".split())

def _as_repaired(word):
    return fix_typo(str(word or "").lower()) or str(word or "")

def _with_the_name(said, raw):
    names = []
    for match in NAME_SAID.finditer(raw or ""):
        name = match.group(1).strip("'\u2019-")
        if name.lower() in NOT_A_NAME or len(name) < 2 or name in names:
            continue
        names.append(name)
    if not names or not said:
        return said
    words = said.split()
    for name in names:
        spelled = name[:1].upper() + name[1:]
        wanted = {name.lower(), _as_repaired(name)}
        for at, word in enumerate(words):
            core = word.strip(".,!?;:")
            if core.lower() in wanted:
                words[at] = word.replace(core, spelled)
                break
    return " ".join(words)

SAY_BACK_VAGUE_TAIL = frozenset("""haha hehe hahaha lol lmao hmm ah oh eh yeah yep nope ok okay
    aye mate hun x xx xxx""".split())

SAY_BACK_CORRECTION = re.compile(r"^you (?:meant|mean)\b|\bno wait\b|^you said (?:actually|sorry)\b")

SAY_BACK_VAGUE = frozenset("""
    there here it that this them those these one ones thing things stuff
    like loves love hate hates want wants need needs think thinking thought
    going get got getting be been being said say told tell
""".split())

DENIAL_LINE = re.compile(r"^(?:no|nah|nope)\b.{0,40}\b(?:isnt|isn't|wasnt|wasn't|not)\b"
                         r"|\bno (?:wait|actually)\b|\bsorry,? (?:i )?(?:mean|meant)\b"
                         r"|^(?:actually|sorry|no|nope|wait)\b[^?]{0,40}?\b(?:called|named|"
                         r"name is)\b")

A_NEW_PERSON = re.compile(r"\b(?:my|our|your)\s+\w+")

def _reads_as_a_correction(line):
    text = " ".join(str(line or "").lower().split())
    if not text:
        return False
    if DENIAL_LINE.search(text) and A_NEW_PERSON.search(text) and not re.search(
            r"\b(?:isnt|isn't|wasnt|wasn't|not)\b", text):
        return bool(extract.extract(line).get("correction"))
    return bool(DENIAL_LINE.search(text)) or bool(extract.extract(line).get("correction"))

def _lines_that_moved(memory):
    entries = [entry for entry in (memory.get("facts_log") or [])
               if isinstance(entry, dict) and entry.get("key")]
    framed = {(str(entry["key"])[:-len("_frame")], entry.get("turn")) for entry in entries
              if str(entry["key"]).endswith("_frame")}
    moved = set()
    last = {}
    for entry in entries:
        key = str(entry["key"])
        if key.endswith("_frame") or isinstance(entry.get("value"), (list, dict)):
            continue
        text = " ".join(str(entry.get("text") or "").lower().split())
        older = last.get(key)
        if older and older != text:
            if _reads_as_a_correction(entry.get("text")) or (key, entry.get("turn")) not in framed:
                moved.add(older)
        last[key] = text
    return moved

SUMMARY_KEYS = frozenset(("name", "age", "job", "city", "shift", "workplace", "from", "pets",
                          "kids", "tastes", "allergies", "diet", "condition", "budget",
                          "plan", "plans"))

def _the_summary_already_says(memory, flat):
    known = user(memory)
    keys = set()
    for entry in memory.get("facts_log") or []:
        if not isinstance(entry, dict) or not entry.get("key"):
            continue
        if " ".join(str(entry.get("text") or "").lower().split()) != flat:
            continue
        key = entry["key"]
        then, now = entry.get("value"), known.get(key)
        if isinstance(now, (list, dict)) or isinstance(then, (list, dict)):
            continue
        if then is None or now is None or str(then).lower() != str(now).lower():
            return False
        keys.add(key)
    return bool(keys) and keys <= SUMMARY_KEYS

def _safety_lines(memory):
    out = set()
    for turn in memory.get("turns") or []:
        if not isinstance(turn, dict):
            continue
        if turn.get("module") not in ("safety",):
            continue
        out.add(" ".join(str(turn.get("user") or "").lower().split()))
    return out

CHANGE_WORD = re.compile(r"\b(?:now|new|again|instead|anymore|any more|no longer|these days|"
                         r"moved to|switched to|changed to)\b", re.I)

NEGATIVE_LINE = re.compile(r"\b(?:i|we)\s*(?:dont|don't|do not|didnt|didn't|did not|cant|can't|"
                            r"cannot|never|havent|haven't|have not|am not|im not|i'm not|wasnt|"
                            r"wasn't|was not|wont|won't|will not)\b", re.I)

AN_ATTITUDE = re.compile(r"\b(?:i|we)\s*(?:dont|don't|do not|didnt|didn't|did not)\s+"
                          r"(?:really\s+|actually\s+)?(?:like|love|enjoy|want|fancy|prefer|hate|"
                          r"eat|drink|need|mind|watch|read|believe|trust|care)\b", re.I)

def _shape(line):
    words = str(line or "").split()
    if not words:
        return ""
    if words[0] in ("im", "i'm", "ive", "i've", "iam"):
        return words[0]
    if len(words) > 1 and words[0] == "i" and words[1] in (
            "am", "have", "got", "dont", "do", "cant", "cannot", "was", "were", "live", "work"):
        return " ".join(words[:2])
    return words[0]

def _out_of_date_lines(memory):
    lines = [" ".join(str(line or "").lower().split()) for line in last_user(memory, 8)]
    logged = {" ".join(str(entry.get("text") or "").lower().split())
              for entry in (memory.get("facts_log") or []) if isinstance(entry, dict)}
    out = set()
    for index, line in enumerate(lines):
        if not CHANGE_WORD.search(line):
            continue
        changed = {word for word in re.findall(r"[a-z0-9']+", line)
                   if len(word) > 2 and word not in STOPWORDS
                   and not CHANGE_WORD.fullmatch(word)}
        for older in lines[:index]:
            if older in logged:
                continue
            knew = {word for word in re.findall(r"[a-z0-9']+", older)
                    if len(word) > 2 and word not in STOPWORDS}
            if changed & knew or _shape(older) == _shape(line):
                out.add(older)
    for index, older in enumerate(lines):
        if not NEGATIVE_LINE.search(older) or AN_ATTITUDE.search(older):
            continue
        knew = [_root(word) for word in re.findall(r"[a-z']+", older)
                if len(word) > 2 and word not in STOPWORDS]
        for later in lines[index + 1:]:
            if (not re.match(r"^(?:i|ive|i've|im|i'm|we|weve) ", later)
                    or NEGATIVE_LINE.search(later) or later.endswith("?")):
                continue
            there = [_root(word) for word in re.findall(r"[a-z']+", later)
                     if len(word) > 2 and word not in STOPWORDS]
            if any(_one_word(a, b) for a in knew for b in there):
                out.add(older)
                break
    return out

def _root(word):
    word = str(word or "").lower().strip("'")
    for suffix in ("ing", "ers", "er", "ed", "es", "s", "ly"):
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            word = word[:-len(suffix)]
            break
    if len(word) > 3 and word[-1] == word[-2] and word[-1] not in "aeiou":
        word = word[:-1]
    if len(word) > 3 and word.endswith("e"):
        word = word[:-1]
    return word

def _one_word(first, second):
    return first == second or (_root(first) == _root(second) and len(_root(first)) >= 3)

SELF_JUDGEMENT = re.compile(
    r"^\W*(?:(?:and|but|so|oh|also|well|yeah|yep|ok|okay|right|honestly|tbh)\W+)*"
    r"(?:i'?m|i\s+am|im|i\s+feel(?:\s+like)?|i\s+was(?:\s+being)?)\b"
    r"(?:\s+(?:being|such|a|an|the|complete|total|absolute|right|proper|bit\s+of\s+a))*\s+"
    r"(?:idiot|muppet|moron|fool|clown|disaster|loser|failure|letdown|let\s?down|"
    r"embarrassment|disappointment|waste\s+of\s+space|useless|worthless|hopeless|"
    r"no\s+good|not\s+good\s+enough|"
    r"(?:rubbish|bad|terrible|awful|useless|hopeless)\s+(?:mum|mom|mother|dad|father|parent|"
    r"husband|wife|partner|friend|person|son|daughter))"
    r"(?:\s+(?:at|with|in)\s+(?:everything|anything|life|myself|all\s+of\s+it|this|that)\b"
    r"(?:\s+\w+){0,4})?"
    r"\s*[.!]*$"
    r"|^\W*what\s+an?\s+(?:idiot|muppet|moron|fool|disaster)\s+i\s+(?:am|was|have\s+been)\b"
    r"|^\W*i\s+hate\s+myself\b"
    r"|^\W*i\s+(?:always|constantly|just|keep|keeps)\s+"
    r"(?:mess(?:es|ing)?\s+(?:things|it|everything)?\s*up"
    r"|ruin(?:s|ing)?\s+(?:things|it|everything)"
    r"|screw(?:s|ing)?\s+(?:things|it|everything)\s+up)\s*[.!]*$", re.I)

SELF_WORST = re.compile(
    r"^\W*(?:(?:and|but|so|oh|also|well|yeah|yep|ok|okay|right|honestly)\W+)*"
    r"(?:i'?m|i\s+am|im)\s+(?:the\s+|literally\s+|such\s+|an?\s+)*(?:worst|worse)\s*"
    r"[.!]*$", re.I)

def _judging_themselves(line):
    said = " ".join(str(line or "").lower().split())
    return bool(said) and bool(SELF_JUDGEMENT.match(said) or SELF_WORST.match(said))

def _recent_told(memory, limit=3):
    out, seen = [], set()
    newest = ""
    if _topics.in_a_safety_thread(memory):
        return out
    moved = _lines_that_moved(memory)
    care = _safety_lines(memory)
    record = current(memory)
    lines = [str(line or "") for line in reversed(last_user(memory, 8))]
    if not lines:
        lines = [str((record or {}).get("text") or "")]
    newest = " ".join(lines[0].lower().split())
    for index, line in enumerate(lines):
        flat = " ".join(str(line or "").lower().split())
        if flat in moved or flat in _out_of_date_lines(memory):
            continue
        if flat in care or _judging_themselves(flat):
            continue
        if _reads_as_a_correction(line):
            if not _a_figure_the_store_could_not_keep(line, memory):
                break
            continue
        if ack.the_rest_of_a_question(
                line, lines[index + 1] if index + 1 < len(lines) else ""):
            continue
        if A_CLAIM_OF_TELLING.match(flat) and not extract.extract(line):
            continue
        if recall.ask(flat) == "me":
            continue
        if _the_summary_already_says(memory, flat):
            continue
        phrase = " ".join(_told_phrase(extract.no_tone(line)).split())
        while phrase and phrase.split()[-1].lower() in SAY_BACK_VAGUE_TAIL:
            phrase = " ".join(phrase.split()[:-1])
        phrase = phrase.replace("can not", "cannot")
        words = {w for w in _summary_words(phrase)}
        if not words or words <= SAY_BACK_VAGUE or SAY_BACK_CORRECTION.search(phrase):
            continue
        key = phrase.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append((phrase, flat == newest))
        if len(out) >= limit:
            break
    return out

AGREEMENT_ONLY = frozenset("""
know knew knows knowing agree agreed guess suppose supposed admit honestly seriously swear trust
believe promise really truly sure right true yes yeah no nah mean means meant said say saying
tell told think thought feel felt do did does done that this it everything anything much
""".split())

def _all_about_the_bot(memory):
    from ..compose.fallback import about_the_bot
    lines = [str(line or "").strip() for line in last_user(memory, 8)]
    lines = [line for line in lines if line]
    if not lines:
        return False
    return all(about_the_bot(" ".join(line.lower().split())) for line in lines)

def _a_figure_the_store_could_not_keep(line, memory):
    if (memory.get("correction") or {}).get("key"):
        return False
    found = extract.extract(line).get("correction") or {}
    value = " ".join(str(found.get("to") or "").split())
    return bool(value) and bool(ANY_NUMBER.fullmatch(value))

def _the_thing_the_chat_is_on(memory):
    if _all_about_the_bot(memory):
        return ""
    record = current(memory) or {}
    text = " ".join(str(record.get("text") or "").split()).lower()
    if not text:
        return ""
    theirs = re.search(r"\b(?:i|im|i'm|my|we|our|me|us|mine)\b", text)
    to_the_bot = re.search(r"\b(?:you|your|youre|you're|u)\b", text)
    if not (theirs or (_asks(text) and not to_the_bot)):
        return ""
    return " ".join(str(_about_the_chat(memory) or "").split())

def _a_fact_of_its_own(clause):
    words = {word.strip(".,!?;:'\"") for word in str(clause).lower().split()} - SUMMARY_FILLER
    return bool(words) and not words <= AGREEMENT_ONLY

def _told_phrase(text):
    if not text:
        return ""
    reading = understand(text, {})
    if (reading.get("kind") in ("question", "greeting", "thanks")
            or reading.get("intent") in ("question", "request", "greeting", "thanks")
            or reading.get("intent") == "feeling"
            or reading.get("asks")):
        return ""

    if reading.get("about_bot"):
        return ""
    if extract.is_a_judgement(text):
        rest = [part.strip() for part in re.split(r"\s*(?:[,;.]|\bbut\b|\band\b)\s*", text)
                if part and part.strip()]
        text = next((part for part in rest
                     if not extract.is_a_judgement(part) and _a_fact_of_its_own(part)), "")
        if not text:
            return ""
    said = _with_the_name(thread.restate(without_filler(text)) or "", text)
    words = [word for word in said.split() if word.strip(".,!?;:")]
    body = {word.strip(".,!?;:").lower() for word in words} - SUMMARY_FILLER
    if not body or body <= SMALL_TALK_ONLY or len(words) > 14:
        return ""
    return " ".join(words)

def _expanded(text):
    text = str(text).lower().replace("\u2019", "'")
    for pattern, word in ((r"n't\b", " not"), (r"'re\b", " are"), (r"'ve\b", " have"),
                          (r"'ll\b", " will"), (r"'d\b", " would"),
                          (r"\bi'm\b", "i am"), (r"\bim\b", "i am"),
                          (r"\bive\b", "i have"), (r"\byoure\b", "you are"),
                          (r"\bdont\b", "do not"), (r"\bdoesnt\b", "does not"),
                          (r"\bim\b", "i am")):
        text = re.sub(pattern, word, text)
    return text

NUMBER_AS_A_WORD = dict(zip(
    "1 2 3 4 5 6 7 8 9 10 11 12 20 30 40 50 100".split(),
    "one two three four five six seven eight nine ten eleven twelve twenty thirty forty fifty "
    "hundred".split()))

def _a_judgement_was_said(memory):
    for turn in (memory.get("turns") or []):
        if not isinstance(turn, dict):
            continue
        line = turn.get("user")
        if isinstance(line, str) and extract.is_a_judgement(line):
            return True
    return False

FACT_FRAME_WORDS = frozenset("""i im ive the a an my our at with for to of in on and
got get gotten job jobs start started starting new began""".split())

def _plain_words(text):
    return set(re.findall(r"[a-z0-9']+", str(text or "").lower().replace("-", " ")))

def _says_nothing_new(phrase, told_words, body_words):
    body = _summary_words(body_words)
    if told_words <= body:
        return True
    rest = _plain_words(phrase) - FACT_FRAME_WORDS
    if not rest:
        return False
    return rest <= _plain_words(body_words)

def _summary_words(text):
    words = set()
    for word in _expanded(text).replace(";", " ").replace(",", " ").split():
        word = stem(word.strip(".,!?;:'"))
        word = NUMBER_AS_A_WORD.get(word, word)
        if not word.isdigit():
            word = stem(extract.DIET_NAMES.get(word, word))
        if word and (word.isdigit() or len(word) > 2) and word not in SUMMARY_FILLER \
                and word not in SMALL_TALK_ONLY:
            words.add(word)
    return words

def _already_said(words, said):
    said = _summary_words(said)
    if not said:
        return False
    if not words:
        return True
    for word in words:
        same = [other for other in said
                if other == word or (len(word) >= 4 and len(other) >= 4
                                     and other[:4] == word[:4])]
        said.difference_update(same)
    return len(said) < max(1, len(words) // 2)

TASTE_ASK = ASKS_ABOUT_A_TASTE

_TASTE_LEFT = TASTE_ASKED_ABOUT

def _taste_reply(memory, low):
    left = _TASTE_LEFT.split(str(low or ""), maxsplit=1)
    asked = left[-1] if len(left) > 1 else ""
    asked = re.sub(r"\b(?:again|still|actually|really|now|any ?more)\b", "", asked).strip(" ?!.,")
    if not asked:
        return None
    wanted = [stem(word) for word in content(asked)]
    if not wanted:
        return None
    for taste in reversed(user(memory).get("tastes") or []):
        thing = str(taste.get("thing") or "").lower()
        bare = thing[5:] if thing.startswith("your ") else thing
        said = [stem(word) for word in content(bare)]
        if not said:
            continue
        if sum(1 for word in wanted if word in said) < max(1, len(wanted) - 1):
            continue
        how = str(taste.get("how") or "yes")
        named = bare if not thing[5:].strip() or not thing.lower().startswith("your ") else thing
        if how == "no":
            return "You don't, you told me you're not keen on " + named + "."
        if how == "unsure":
            return "You weren't sure about " + named + ", that's all you've said."
        return "You do, you told me you like " + named + "."
    return None

def _tastes_said(memory):
    liked, other = [], []
    for taste in user(memory).get("tastes") or []:
        thing = str((taste or {}).get("thing") or "").strip()
        if not thing:
            continue
        how = str(taste.get("how") or "yes")
        if how == "no":
            other.append("You're not keen on " + thing + ".")
        elif how == "unsure":
            other.append("You're not sure about " + thing + ".")
        else:
            liked.append(thing)
    said = []
    if liked:
        joined = liked[0] if len(liked) == 1 else ", ".join(liked[:-1]) + " and " + liked[-1]
        said.append("You like " + joined + ".")
    said.extend(other)
    return " ".join(said) if said else None

AGE_SAID_IN_WORDS = re.compile(
    r"\b(?:(?:i(?:'m| am)|im|you(?:'re| are)|youre|we(?:'re| are)|were|they(?:'re| are)))\s+"
    r"(?:\d{1,3}|a hundred|one|two|three|four|five|six|seven|eight|nine|"
    r"ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|"
    r"thirty|forty|fifty|sixty|seventy|eighty|ninety)\b", re.I)

def _without_the_age(line):
    without = AGE_SAID_IN_WORDS.sub("", str(line or ""), count=1).strip(" .,;:!?-")
    return re.sub(r"^(?:and|also|plus)\s+", "", without, flags=re.I).strip()

def _the_words_of_a_fact(value):
    if isinstance(value, bool):
        return ""
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return " ".join(_the_words_of_a_fact(part) for part in value.values())
    if isinstance(value, (list, tuple, set)):
        return " ".join(_the_words_of_a_fact(part) for part in value)
    return ""


def _a_fact_the_recap_does_not_say(memory, phrase, body_words):
    said = _summary_words(body_words)
    for entry in memory.get("facts_log") or []:
        if not isinstance(entry, dict) or not entry.get("key"):
            continue
        text = " ".join(str(entry.get("text") or "").lower().split())
        if " ".join(_told_phrase(extract.no_tone(text)).split()) != phrase:
            continue
        words = _summary_words(_the_words_of_a_fact(user(memory).get(entry["key"])))
        if words - said:
            return True
    return False


def _kids_told(memory):
    told = user(memory).get("kids")
    if isinstance(told, bool):
        return 0
    if isinstance(told, int):
        return told if told > 0 else 0
    if isinstance(told, str) and told.strip().isdigit():
        return int(told.strip())
    return 0


def _a_child_is_described(memory):
    for entry in others(memory):
        who = str(entry.get("who") or "").rstrip("s")
        if who and who in CHILD and (entry.get("name") or entry.get("age") or entry.get("ages")):
            return True
    return False


def _a_few_children(count):
    if count == 1:
        return "one child"
    in_words = {number: word for word, number in extract.KID_NUMBERS.items()}
    return in_words.get(count, str(count)) + " kids"


SUMMED_UP = re.compile(
    r"^(?:ok |okay |right |so |and |but |also |well |quick |just )*(?:"
    r"what (?:have|did) we (?:got|get|have|decided|decide|settled|settle|agreed|agree|know)|"
    r"what do we (?:know|have|got)|"
    r"what(?:'s|\u2019s|s)? (?:our|the) plan|what is (?:our|the) plan|"
    r"tell me what we(?:'ve|\u2019ve|ve)? (?:agreed|decided|settled)|"
    r"walk me through what we (?:decided|agreed|settled)|"
    r"what(?:'s|\u2019s|s)? (?:the )?state of play|what is (?:the )?state of play|"
    r"how far (?:have|did) we (?:got|get)|"
    r"what(?:'s|\u2019s|s)? decided|what is decided"
    r")(?: so far| then| now| again| already| on)*\s*[?.!]*$")


def _summed_up(low):
    return bool(SUMMED_UP.match(str(low or "").strip()))

def _summary_reply(memory):
    known = user(memory)
    parts = []
    if known.get("name"):
        parts.append("you're " + known["name"])
    if known.get("age"):
        age = str(known["age"])
        if parts and parts[0].startswith("you're ") and "," not in parts[0]:
            parts[0] += ", " + age
        else:
            parts.append("you're " + age)
    if known.get("job"):
        said = _job_phrase(known)
        if known.get("city"):
            said += " in " + known["city"]
        parts.append(said)
    elif known.get("city"):
        parts.append("you live in " + known["city"])
    shift = str(known.get("shift") or "").strip()
    if shift:
        parts.append("you work " + shift)
    place = str(known.get("workplace") or "").strip()
    if place:
        parts.append("you work " + _place_phrase(place))
    origin = known.get("from")
    if origin and str(origin).lower() != str(known.get("city") or "").lower():
        parts.append("you're from " + origin)
    said_things = set()
    for pet in known.get("pets") or []:
        parts.append("you've got " + _a_pet(pet))
        said_things.update(str(pet.get(k) or "").lower().rstrip("s") for k in ("animal", "name"))
    for taste in known.get("tastes") or []:
        thing = str(taste.get("thing") or "").strip()
        if not thing:
            continue
        bare = thing.lower()
        bare = bare[5:] if bare.startswith("your ") else bare
        if bare in said_things or bare.rstrip("s") in said_things:
            continue
        how = str(taste.get("how") or "yes")
        if how == "no":
            parts.append("you're not keen on " + thing)
        elif how == "unsure":
            parts.append("you're not sure about " + thing)
        else:
            parts.append("you like " + thing)
    if known.get("allergies"):
        parts.append("you're allergic to " + ", ".join(known["allergies"]))
    named = set()
    for entry in others(memory):
        who = entry.get("who")
        p_allergic = entry.get("allergies") or []
        if who and p_allergic:
            parts.append("your " + who + _is_are(who) + "allergic to " + ", ".join(p_allergic))
            named.add(who)
        p_name = str(entry.get("name") or "")
        p_age = str(entry.get("age") or "")
        p_ages = [age for age in entry.get("ages") or [] if isinstance(age, int)]
        p_diet = str(entry.get("diet") or "")
        if who and p_name and who.rstrip("s") in CHILD and p_age:
            parts.append(_called(p_name) + " is " + p_age)
            named.add(who)
        elif who and p_name:
            said = "your " + who + " is called " + _called(p_name)
            if p_age:
                said += " and is " + p_age
            parts.append(said)
            named.add(who)
        elif who and p_ages:
            said_ages = (", ".join(str(age) for age in p_ages[:-1]) + " and " + str(p_ages[-1])
                         if len(p_ages) > 1 else str(p_ages[0]))
            parts.append("your " + who + _is_are(who) + said_ages)
            named.add(who)
        elif who and p_age and who.rstrip("s") in CHILD:
            parts.append("you've got a " + p_age + " year old")
            named.add(who)
        elif who and p_age:
            parts.append("your " + who + " is " + p_age)
            named.add(who)
        if who and p_diet:
            parts.append("your " + who + " " + _a_diet_predicate(who, p_diet))
            named.add(who)
    told_kids = _kids_told(memory)
    if told_kids and not _a_child_is_described(memory):
        if parts and parts[-1].startswith("you've got "):
            parts[-1] += " and " + _a_few_children(told_kids)
        else:
            parts.append("you've got " + _a_few_children(told_kids))
    if known.get("diet"):
        diet = str(known["diet"])
        parts.append("you don't " + _diet_how(diet) + " " + diet[3:] if diet.startswith("no ")
                     else "you're " + diet)
    if known.get("condition"):
        parts.append("you're " + ", ".join(str(c) for c in known["condition"]))
    if known.get("budget"):
        parts.append("your budget is " + str(known["budget"]))
    plans = list(known.get("plans") or [])
    if known.get("plan") and known["plan"] not in plans:
        plans.append(known["plan"])
    last_plan = str(plans[-1]) if plans else ""
    told = _last_told(memory)
    in_tastes = " ".join(str(t.get("thing") or "").lower() for t in known.get("tastes") or [])
    people = [p for p in (known.get("people") or [])
              if p not in named and str(p).lower() not in last_plan.lower()
              and str(p).lower() not in told.lower()
              and str(p).lower() not in in_tastes]
    if people:
        parts.append("you mentioned your " + ", ".join(people[:3]))
    if plans:
        plan = plan_sentence(plans[-1], plan_line(memory, plans[-1]))
        plan = plan[:1].lower() + plan[1:]
        if known.get("age") and AGE_SAID_IN_WORDS.search(plan):
            plan = _without_the_age(plan)
        if plan and plan.lower() not in " ".join(parts).lower():
            parts.append(plan)
    body_words = "; ".join(parts)
    subject = topic_subject(memory).lower()
    head = subject.split()[-1] if subject else ""
    facts_body = "; ".join(parts)
    said_back = 0
    for phrase, from_current in _recent_told(memory, limit=4):
        body_words = "; ".join(parts)
        told_words = _summary_words(phrase)
        covered = bool(told_words) and _says_nothing_new(phrase, told_words, body_words)
        if not covered and told.startswith("you work ") and "you work " in body_words:
            covered = True
        anchor_word = ""
        for word in phrase.split():
            if len(word) > 3 and word.lower() not in SAY_BACK_VAGUE:
                anchor_word = word.lower()
        on_topic = (from_current and head and head in facts_body.lower()
                    and not _a_fact_the_recap_does_not_say(memory, phrase, body_words))
        if (covered or _already_said(told_words, body_words)
                or (anchor_word and _summary_words(anchor_word) & _summary_words(body_words))
                or on_topic):
            continue
        parts.append(("you said " if not said_back else "") + phrase)
        said_back += 1
        if said_back >= 2:
            break
    if people and said_back:
        said_lines = " ".join(part for part in parts
                              if not part.startswith("you mentioned your ")).lower()
        parts = [part for part in parts
                 if not (part.startswith("you mentioned your ")
                         and any(word in said_lines for word in part.split()[3:]))]
    if not parts:
        if _a_judgement_was_said(memory):
            return pick(["I've got that you're being hard on yourself, and no facts about you yet. "
                         "What should I know?",
                         "I have that you're being hard on yourself - and nothing about your life "
                         "yet that I can say back.",
                         "You've told me how you're feeling about yourself, and nothing about your "
                         "life yet. What should I know?"], memory)
        about = _the_thing_the_chat_is_on(memory)
        if about:
            return pick([
                "Nothing about you yet — so far it's been " + about + ". What should I know?",
                "I've got no facts about you yet; we've been on " + about + ". What should I "
                "know?",
                "No notes about you so far — you've had me on " + about + ". What should I know?"],
                memory)
        return "Not much yet — you haven't told me about yourself. What should I know?"
    body = "; ".join(parts)
    return pick(["So far I know " + body + ".",
                 "Here's what you've told me: " + body + ".",
                 "You've told me " + body + "."], memory)

def _quote(text, limit=90):
    text = " ".join(str(text).split())
    if len(text) > limit:
        cut = text[:limit - 1]
        if not cut.endswith(" ") and " " in cut:
            cut = cut[:cut.rfind(" ")]
        text = cut.rstrip(" ,;:-") + "…"
    return "\"" + text.rstrip(" .!?") + "\""

HEAVY_TOPIC = re.compile(
    r"\b(?:died|dying|death|funeral|passed away|buried|cremation|"
    r"kill myself|killing myself|killed myself|suicide|suicidal|end it all|take my own life|"
    r"hurt myself|hurting myself|self harm|self-harm|cut myself|overdose|"
    r"miscarriage|stillborn|terminal|diagnosed with cancer|beat me|beats me|abuses?d? me|"
    r"bullied|bullying|hit me|hits me|assaulted)\b",
    re.I)

def _heavy(line):
    return bool(HEAVY_TOPIC.search(" ".join(str(line or "").split())))

def _topics_reply(memory):
    lines = history.topic_lines(memory)
    light = [line for line in lines if not _heavy(line)]
    if not lines:
        return pick(NOTHING_STARTED, memory)
    if not light:
        return pick(["We've been on something heavy, and I won't read it back to you. It is "
                     "still here if you want to talk about it.",
                     "What we've been on is heavy, so I'd rather not put it in quotation marks. "
                     "Say more about it whenever you want."], memory)
    said = "; ".join(_quote(line, 60) for line in light)
    if len(light) < len(lines):
        return pick(["We've been on " + said + ", and on something heavy I won't read back.",
                     "Mostly " + said + ". There was something heavier too, and I have not "
                     "forgotten it."], memory)
    return pick(["We've been on " + said + ".",
                 "Mostly " + said + ".",
                 "Covered so far: " + said + "."], memory)

def _first_sentence(text, limit=70):
    text = " ".join(str(text).split())
    end = len(text)
    for mark in (". ", "? ", "! "):
        at = text.find(mark)
        if 0 < at < end:
            end = at + 1
    text = text[:end].strip()
    if len(text) > limit:
        cut = text[:limit - 1]
        if " " in cut:
            cut = cut[:cut.rfind(" ")]
        text = cut.rstrip(" ,;:-") + "…"
    return text.rstrip(" .!?")

CALL_ASK = re.compile(
    r"^\W*(?:and\s+|so\s+|but\s+)?(?:should|shall)\s+(?:i|we)\b"
    r"|^\W*(?:and\s+|so\s+|but\s+)?(?:is|would)\s+(?:it|that)\s+"
    r"(?:safe|ok|okay|alright|fine|worth|sensible|wise|a good idea|a bad idea|too (?:late|soon))\b"
    r"|^\W*(?:and\s+|so\s+|but\s+)?(?:do|must)\s+(?:i|we)\s+(?:need to|have to|really need to)\b"
    r"|^\W*(?:and\s+|so\s+|but\s+)?(?:can|could)\s+(?:i|we)\s+(?:still|keep|go)\b")

CARRY_ON = re.compile(
    r"\b(?:keep|keeps|keep on|carry on|carrying on|go on|going|continue|continuing|"
    r"start|starting|start again|go back|back to|train|training|run|running|walk|walking|"
    r"drive|driving|ride|riding|cycle|cycling|swim|swimming|lift|lifting|play|playing|"
    r"work out|exercise|"
    r"push on|push through|try|it|that)\b", re.I)

STOP_IT = re.compile(
    r"\b(?:stop|stopping|quit|quitting|give up|giving up|lay off|rest|resting|take a break)\b",
    re.I)

STOP_CONDITION = re.compile(
    r"^(?:and\s+)?(?:see|ask|call|ring|go to|get|speak to|talk to|tell|stop|if)\b", re.I)

CLAUSE_SPLIT = re.compile(r":\s+|(?<=[.!?])\s+|,\s+(?:and|but|so)\s+")

SEE_SOMEONE = re.compile(
    r"\b(?:see|sees|seeing|call|calling|ring|ringing|go to|going to|get|getting|book|booked|"
    r"visit|visiting|speak to|speaking to|talk to|talking to|check|checked|checked out)\s+"
    r"(?:\w+\s+){0,2}(?:someone|somebody|anyone|a doctor|the doctor|my doctor|doctor|gp|physio|"
    r"nurse|hospital|a&e|ae|surgery|specialist|professional|it checked|this checked|that checked)\b",
    re.I)

HALF_AN_HOUR = re.compile(r"\bhalf\s+an\s+hour\b", re.I)

TIME_LENGTH = re.compile(
    r"\b(?P<count>\d+|an?|a\s+couple\s+of|a\s+few|"
    r"one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|fifteen|twenty|"
    r"thirty|forty|forty-five|fifty|sixty|ninety)\s*-?\s*"
    r"(?P<unit>minutes?|mins?|hours?|hrs?)\b", re.I)

LENGTH_FILLER = frozenset(
    "a an the about roughly around give take or and plus maybe depending on it takes that this is "
    "of to for at least more less just only or so too up each per in all altogether total tops "
    "time".split())

LEAD_LABEL = re.compile(r"^[A-Za-z][A-Za-z' -]{0,14}:\s*")

SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")

SPLIT_MOVES = re.compile(r";\s+|\s+-\s+|\s+\u2014\s+|,\s+or\s+|;\s*or\s+")

BUDGET = re.compile(
    r"^\W*(?:(?:and|but|so|oh|also|well|yeah|yep|ok|okay|right|alright)\W+)*"
    r"(?:i|we|ive|i\'ve|weve|we\'ve)\s+"
    r"(?:(?:really|only|just|literally|maybe|probably|actually)\s+)*"
    r"(?:get|got|have|had|make|leave|take|need|needs|fancy)\s+"
    r"(?:(?:only|just|maybe|about|altogether|in total|tops|roughly)\s+)*"
    r"(?P<length>" + LENGTH + r")\b", re.I)

A_HORIZON = re.compile(
    r"\b(?:for|after|over|in|within)\s+(?:the\s+)?(?:first\s+|next\s+|following\s+)?"
    r"(?:\d+|a|an|one|two|three|four|five|six|seven|eight|nine|ten|few|couple(?:\s+of)?)"
    r"\s+(?:days?|weeks?|months?)\b", re.I)

def _sentences(answer):
    return [part.strip() for part in SENTENCE_SPLIT.split(" ".join(str(answer or "").split())) if part.strip()]

def _halves(sentence):
    parts = []
    for part in SPLIT_MOVES.split(sentence):
        part = LEAD_LABEL.sub("", part.strip(" .;,"))
        if part:
            parts.append(part)
    return parts

def _says_something(part):
    left = TIME_LENGTH.sub(" ", " ".join(str(part or "").split()))
    left = HALF_AN_HOUR.sub(" ", left)
    words = [word for word in re.findall(r"[a-z']+", left.lower())
             if word not in LENGTH_FILLER and len(word) > 1]
    return len(words) >= 2

def _seconds(said):
    text = " ".join(str(said or "").split())
    if not text:
        return None
    half = HALF_AN_HOUR.search(text)
    found = TIME_LENGTH.search(text)
    if half and (not found or half.start() < found.start()):
        return 1800
    if not found:
        return None
    count = found.group("count").lower()
    if count.startswith("a couple"):
        number = 2
    elif count.startswith("a few"):
        number = 3
    elif count.isdigit():
        number = int(count)
    else:
        number = WORD_NUMBERS.get(count)
    unit = found.group("unit").lower().rstrip("s")
    if not number or unit not in UNIT_SECONDS:
        return None
    return number * UNIT_SECONDS[unit]

def _names_minutes(said):
    return any(match.group("unit").lower().startswith("min")
               for match in TIME_LENGTH.finditer(" ".join(str(said or "").split())))

def _longest(said, bare=False):
    text = " ".join(str(said or "").split())
    if not text:
        return None
    half = HALF_AN_HOUR.search(text)
    if half:
        text = text[:half.start()] + " 30 minutes " + text[half.end():]
    found = [match.group(0) for match in TIME_LENGTH.finditer(text)]
    lengths = [n for n in (_seconds(part) for part in found) if n]
    if bare or any(second <= 3600 for second in lengths):
        for bare in re.finditer(r"\bin\s+(\d{1,2})\b", text, re.I):
            minutes = int(bare.group(1))
            if 0 < minutes <= 90:
                lengths.append(minutes * 60)
    return max(lengths) if lengths else None

A_LENGTH_AS_THE_SUBJECT = re.compile(
    r"^(?:(?:so|and|but|well|ok|okay)\s+)?"
    r"(?:(?P<length>" + LENGTH + r")\s*(?:left\b|,|\bis\b|\bwas\b|\bfeels\b|\bsounds\b)"
    r"|that\s+wants\s+(?:longer|more)\s+than\s+" + LENGTH + r"\b"
    r"|it\s+takes\s+longer\s+than\s+" + LENGTH + r"\b)", re.I)

def _a_remark_about_a_length(answer):
    remarked = False
    for sentence in _sentences(answer):
        if _longest(sentence) is None:
            continue
        if not A_LENGTH_AS_THE_SUBJECT.search(" ".join(sentence.split())):
            return False
        remarked = True
    return remarked

def _moves(answer):
    names = _names_minutes(answer)
    out = []
    for at, sentence in enumerate(_sentences(answer)):
        for part in _halves(sentence):
            if not _says_something(part):
                continue
            out.append((part, _longest(part, bare=names), at))
    return out

def _up_to_the_move(answer, part):
    want = " ".join(str(part or "").split())
    sentences = _sentences(answer)
    for at, sentence in enumerate(sentences):
        for half in _halves(sentence):
            if " ".join(half.split()) == want:
                if not at:
                    return want
                return " ".join(sentences[:at + 1]).strip()
    return None

def _the_move_that_fits(moves, room):
    best, best_sentence, best_seconds = None, None, -1
    over, over_sentence = None, None
    for part, took, sentence in moves:
        if took is None:
            continue
        if took > room:
            if over is None:
                over, over_sentence = took, sentence
            continue
        if took > best_seconds:
            best, best_sentence, best_seconds = part, sentence, took
    step = over if (best is not None and over is not None and over_sentence < best_sentence) else None
    return best, step

def _left_out(moves, room):
    return any(took is not None and took > room for _part, took, _at in moves)

def _the_lead(answer):
    for sentence in _sentences(answer):
        part = LEAD_LABEL.sub("", sentence.strip(" .;,"))
        if _says_something(part):
            return part
    return None

A_RATE_OF = re.compile(
    r"\b(?P<length>\d[\d,.]*|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|fifteen|"
    r"twenty|thirty|forty|forty[- ]five|fifty|sixty|ninety|half\s+an|an?)\s*"
    r"(?P<unit>minutes?|mins?|hours?|hrs?)\s+(?:a|per|each)\s+(?:day|week)\b", re.I)

def _a_rate_of_the_same_length(answer, room):
    for found in A_RATE_OF.finditer(str(answer or "")):
        if _seconds(found.group("length") + " " + found.group("unit")) == room:
            return True
    return False

def _the_budget_on_the_answer(text, memory):
    if not isinstance(text, str) or not isinstance(memory, dict):
        return None
    said = " ".join(text.split())
    if not said or "?" in said or len(said.split()) > 11:
        return None
    found = BUDGET.match(said)
    if not found:
        return None
    tail = said[found.end():].strip(" .!,;")
    if len(tail.split()) > 4:
        return None
    if re.match(r"^of\b", tail, re.I):
        return None
    room = _seconds(found.group("length"))
    if room is None:
        return None
    longer = None
    for answer in _recent_answers(memory):
        if _a_rate_of_the_same_length(answer, room):
            return None
        if room < 86400 and A_HORIZON.search(answer):
            lead = _the_lead(answer)
            if lead:
                return pick(BUDGET_TIGHT, memory).format(
                    budget=_theirs(found.group("length"), mid=True), part=_tidy(lead))
            continue
        if _a_remark_about_a_length(answer):
            continue
        longest = _longest(answer)
        if longest is None:
            continue
        moves = _moves(answer)
        part, over = _the_move_that_fits(moves, room)
        if over is not None:
            lead = _the_lead(answer)
            if lead:
                return pick(BUDGET_TIGHT, memory).format(
                    budget=_theirs(found.group("length"), mid=True), part=_tidy(lead))
        if part:
            if _left_out(moves, room):
                shorter = _up_to_the_move(answer, part)
                if shorter and len(shorter.split()) <= 90 and _says_something(shorter):
                    part = shorter
                shape = BUDGET_FITS
            else:
                kept = None
                if len(ANY_FIGURE.findall(answer)) == 1:
                    shorter = _up_to_the_move(answer, part)
                    if shorter and len(shorter.split()) <= 45 and _says_something(shorter):
                        kept = shorter
                if kept:
                    part = kept
                else:
                    lead = _the_lead(answer)
                    if lead and len(lead.split()) <= 90 and _says_something(lead):
                        part = lead
                shape = BUDGET_MORE
            return pick(shape, memory).format(budget=_theirs(found.group("length")),
                                              part=_tidy(part))
        if longer is None:
            longer = answer
    if longer is None:
        return None
    part = _the_lead(longer)
    if not part:
        return None
    return pick(BUDGET_TIGHT, memory).format(budget=_theirs(found.group("length"), mid=True),
                                             part=_tidy(part))

def _theirs(length, mid=False):
    text = " ".join(str(length or "").split()).strip(" .;,")
    if not text:
        return text
    if mid and not text[1:2].isupper():
        return text[:1].lower() + text[1:]
    return text[:1].upper() + text[1:]

def _tidy(part):
    text = " ".join(str(part or "").split()).strip(" .;,?!")
    if not text:
        return text
    return text[:1].upper() + text[1:]

def _clauses(reply):
    text = " ".join(str(reply or "").split())
    return [part.strip(" .;") for part in CLAUSE_SPLIT.split(text) if part.strip(" .;")]

def _the_limit(reply):
    for part in _clauses(reply):
        low = part.lower()
        if len(part.split()) > 24:
            continue
        if any(low == word or low.startswith(word + " ") for word in RESTRICT_OPENS):
            return part
    return None

def _the_condition(reply):
    for part in _clauses(reply):
        low = part.lower()
        if len(part.split()) > 26:
            continue
        if STOP_CONDITION.match(low) and " if " in low:
            return part
    for part in _clauses(reply):
        low = part.lower()
        if re.search(r"\b(?:means stop|stop driving|do not drive|don't drive)\b", low):
            return part
    return None

def _recent_answers(memory, back=3):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns:
        return []
    said = []
    for turn in turns[-back - 1:][::-1]:
        if not isinstance(turn, dict):
            continue
        reply = turn.get("bot")
        if isinstance(reply, str) and reply.strip():
            said.append(reply.strip())
        if len(said) >= back:
            break
    return said

def _shares_a_word(low, said):
    def words(text):
        return {stem(word) for word in keywords(str(text).lower())}
    return bool(words(low) & words(said))

def _the_call_from_the_advice(text, memory):
    if not isinstance(text, str) or not isinstance(memory, dict):
        return None
    low = _bare(_folded(text, memory))
    if not low or len(low.split()) > 9 or " you " in " " + low + " ":
        return None
    if not CALL_ASK.match(low) or not CARRY_ON.search(low):
        return None
    if SEE_SOMEONE.search(low):
        return None
    limit = condition = None
    for said in _recent_answers(memory):
        if not _shares_a_word(low, said):
            continue
        found, if_half = _the_limit(said), _the_condition(said)
        if found and if_half:
            limit, condition = found, if_half
            break
    if not limit or not condition:
        return None
    rest_or_go = re.search(r"\b(?:keep|keep going|carry on|continue|still|go on)\b", low)
    if STOP_IT.search(low) and rest_or_go:
        return None
    if STOP_IT.search(low):
        return ("Not all the way: " + limit[0].lower() + limit[1:] + ". And "
                + condition[0].lower() + condition[1:] + ".")
    return pick(CALL_LEADS, memory).format(limit=limit[0].lower() + limit[1:],
                                           condition=condition[0].lower() + condition[1:])

def _trim(text, limit=90):
    text = " ".join(str(text).split())
    return text if len(text) <= limit else text[:limit - 1].rstrip() + "…"

FOOD_CONDITION = frozenset(("coeliac", "celiac", "diabetic", "diabetes", "ibs",
                            "irritable bowel", "crohns", "crohn's", "lactose intolerant",
                            "fructose intolerant", "allergic"))

def _food_facts(memory):
    mine = user(memory)
    kept = []
    allergies = mine.get("allergies")
    if isinstance(allergies, str):
        allergies = [allergies]
    if isinstance(allergies, (list, tuple)):
        for item in allergies:
            item = str(item).strip()
            if item:
                kept.append("allergic to " + item)
    condition = mine.get("condition")
    if isinstance(condition, str):
        condition = [condition]
    if isinstance(condition, (list, tuple)):
        for item in condition:
            item = str(item).strip()
            if item and item.lower() in FOOD_CONDITION:
                kept.append(item)
    return kept

def _the_food_a_condition_rules_out(condition):
    wanted = cooking.CONDITION_BANS.get(str(condition or "").lower().strip())
    if not wanted:
        return ""
    for name, family in cooking.FAMILIES.items():
        if set(family) == set(wanted):
            return name
    return ""

def _what_a_dinner_has_to_leave_out(memory):
    mine = user(memory)
    left_out, said_so = [], []
    allergies = mine.get("allergies")
    if isinstance(allergies, str):
        allergies = [allergies]
    if isinstance(allergies, (list, tuple)):
        kept = [str(name).strip() for name in allergies if str(name).strip()]
        if kept:
            left_out.extend(kept)
            said_so.append("you're allergic to " + _all_of_them(len(kept)))
    condition = mine.get("condition")
    if isinstance(condition, str):
        condition = [condition]
    if isinstance(condition, (list, tuple)):
        for item in condition:
            named = str(item).strip()
            if not named or named.lower() not in FOOD_CONDITION:
                continue
            food = _the_food_a_condition_rules_out(named)
            said_so.append("you're " + named)
            if food and food not in left_out:
                left_out.append(food)
    return left_out, said_so

def _all_of_them(count):
    if count == 1:
        return "them"
    if count == 2:
        return "both"
    return "all of them"

def _say_a_list(items):
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return items[0] + " and " + items[1]
    return ", ".join(items[:-1]) + " and " + items[-1]

INTENSIFIER = r"(?:really|honestly|actually|even|ever|particularly|especially|much)"

CLOSE_SUBJECT = re.compile(
    r"\bi (?:just )?(?:want|wanna|would rather|'?d rather|need) to "
    r"(?:forget|drop|leave|skip) (?:it|that|this|all of it|all that)\b|"
    r"\bi(?:'?d|\s+would)?\s+(?:" + INTENSIFIER + r"\s+)?rather\s+not\s+"
    r"(?:say|talk about it|go into it|get into it)\b|"
    r"\bi\s+(?:do\s+not|don'?t|dont)\s+(?:" + INTENSIFIER + r"\s+)?"
    r"(?:want|wanna|need)\s+(?:" + INTENSIFIER + r"\s+)?to\s+"
    r"(?:(?:talk|think|speak|hear)\s+about\s+|(?:go|get)\s+into\s+)(?:it|that|this)\b|"
    r"\bi\s+(?:can'?t|cannot|couldn'?t|won'?t|will not)\s+"
    r"(?:go|get)\s+into\s+(?:it|that|this)\b|"
    r"\b(?:can|could|would) (?:we|you) (?:just )?not (?:talk|speak) about (?:it|that|this)\b|"
    r"\b(?:let'?s|lets) not (?:talk|speak) about (?:it|that|this)\b|"
    r"\bnot (?:going to|gonna) talk about (?:it|that)\b|"
    r"\b(?:drop|forget) (?:it|that)\b|"
    r"\bnever\s*mind(?:\s+(?:that|this|it|then|now|anyway|about (?:it|that|this)))?\b|"
    r"\bnevermind(?:\s+(?:that|this|it|then|now|anyway))?\b|"
    r"\bnvm(?:\s+(?:that|this|it))?\b|"
    r"\b(?:it )?(?:does not|doesn'?t|didnt|didn'?t) matter\b|"
    r"\b(?:ignore|skip|scrap|scratch) (?:it|that|this)\b|"
    r"\bnot important\b|"
    r"\bforget (?:i|what i) (?:said|asked)\b|"
    r"\bno more (?:about|on) (?:it|that)\b")

CHANGE_SUBJECT = re.compile(
    r"\b(?:talk|speak|chat) about (?:something|anything) (?:else|different)\b|"
    r"\b(?:change|switch|move) (?:the subject|the topic|to a different|to another|"
    r"onto something else|on to something else)\b|"
    r"\b(?:talk|speak|chat) about another (?:topic|subject|thing)\b|"
    r"\b(?:change|switch) (?:the )?(?:subject|topic)\b|"
    r"\bsomething (?:else|different) (?:for a bit|instead|to talk about)\b")

CARRIES_ON_AFTER = re.compile(
    r"\b(?:it|that|this|all of it|all that)\s+"
    r"(?:(?:in|into|on|onto|for|to|from|with|about|between|among|and|then|when|if|after|before|"
    r"until|till|while|overnight|so|because|as)\b"
    r"|at\b(?!\s+all\b))")

ASKS_WHETHER_TO = re.compile(r"\b(?:should|shall|can|could|would|do|does|did)\s+i\b|\bi should\b")

ASKS_FOR_HELP = re.compile(r"\b(?:can you help|help me|is it (?:wrong|bad|ok|okay|normal)|"
                           r"what should i|do you think i should|am i wrong)\b")

HOLDS_FOR_NOW = re.compile(
    r"\b(?:at|for)\s+(?:the\s+)?(?:all|moment|minute|time\s+being|now)\b"
    r"|\b(?:right|just)\s+now\b|\bany\s?more\b|\bagain\b|\byet\b")
CLOSE_FILLER = frozenset("""and but so ok okay right then well anyway anyhow also now just
please thanks thank you for a bit moment second though too as if that this at all never mind let
lets we you i me my of on in to the good fine fair enough alright still only really can could
would will shall not oh ah hmm yeah yes no actually wait it its
today tonight now anymore any more again yet later tomorrow moment minute time being""".split())
CLOSE_FILLER_ALWAYS = CLOSE_FILLER - frozenset(
    "today tonight now anymore any more again yet later tomorrow".split())

CHECK_FOLLOWED = re.compile(
    r"^(?:(?:did|do|have|has|were|are)\s+(?:you|u)\s+"
    r"(?:get|got|see|saw|catch|caught|read|hear|heard|note|noted|follow|following"
    r"|have|got|keep|kept|take|taken|remember)"
    r"|(?:you|u)\s+(?:get|got|catch|caught|see|saw|read|hear|heard|follow|following)\b"
    r"|got\s+(?:that|it|this))\s*"
    r"(?:that|it|this|it\s+all|all\s+of\s+that|all\s+of\s+it|all\s+that|everything"
    r"|any\s+of\s+that|any\s+of\s+it|the\s+lot|the\s+whole\s+lot|my\s+message"
    r"|my\s+last\s+message|the\s+message|what\s+i\s+said|what\s+i\s+sent"
    r"|the\s+last\s+bit)?\s*$")

BARE_ACKNOWLEDGEMENT = re.compile(
    r"^(?:(?:so|ok|okay|right|ah|oh|yeah|and|well|great|good|nice|cheers|perfect|loud and clear)"
    r"\s+)*got(?:\s+(?:that|it|this|ya|yas|you))$")

SAID_TO_THE_BOT = re.compile(r"\b(?:you|u|your|yours|urs|yourself)\b")

A_MOOD_LINE = re.compile(
    r"\b(?:sad|sadly|upset|miserable|depressed|low|down|angry|furious|annoyed|gutted|stressed"
    r"|fed up|knackered|exhausted|tired|worn out|lonely|bored|happy|glad|pleased|excited"
    r"|nervous|worried|anxious|scared|frightened|terrified|dreading|overwhelmed|burnt out)\b")

def _reads_as_the_invitation(text, memory):
    try:
        from ..compose import fallback
        return bool(fallback.reads_as_if_i_saw(text, memory))
    except Exception:
        return False

SAFETY_MODULES = frozenset(("safety", "urgent"))

def _the_module_behind(memory, said):
    low = _plain_line(said)
    for turn in reversed([t for t in (memory.get("turns") or []) if isinstance(t, dict)]):
        if _plain_line(turn.get("user")) == low:
            return str(turn.get("module") or "")
    return ""

def _the_line_before_the_check(memory, line):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)][-6:]
    for turn in reversed(turns):
        said = str(turn.get("user") or "").strip()
        if not said:
            continue
        if CHECK_FOLLOWED.match(_plain_line(said)):
            continue
        if line and _plain_line(said) == line:
            continue
        return said
    return ""

def _a_check_choice(options, memory, salt):
    turns = memory.get("turns") or []
    recent = " ".join(str(t.get("bot") or "") for t in turns[-4:] if isinstance(t, dict))
    fresh = [option for option in options if option[:30] not in recent] or list(options)
    return fresh[(len(turns) + salt) % len(fresh)]

def _a_check_came_before(memory, line):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)][-6:]
    said_before = [_plain_line(str(turn.get("user") or "")) for turn in turns]
    if (said_before and line and said_before[-1] == line
            and not str(turns[-1].get("bot") or "").strip()):
        said_before = said_before[:-1]
    for said in reversed(said_before):
        if not said:
            continue
        return bool(CHECK_FOLLOWED.match(said))
    return False

def _the_followed_check(text, memory):
    if not isinstance(text, str) or not isinstance(memory, dict):
        return None
    as_said = _folded(text, memory)
    low = _plain_line(as_said)
    if _reads_as_the_invitation(low, memory):
        return None
    if not CHECK_FOLLOWED.match(low):
        return None
    if BARE_ACKNOWLEDGEMENT.match(low) and "?" not in str(text):
        return None
    previous = _the_line_before_the_check(memory, low)
    if previous and _the_module_behind(memory, previous) in SAFETY_MODULES:
        return None
    salt = len(low) + 3 * len([t for t in (memory.get("turns") or []) if isinstance(t, dict)])
    if previous:
        if (FEELING_ALONE.match(previous.lower().rstrip("!.,"))
                or A_MOOD_LINE.search(previous.lower())
                or A_PERSON_IN_TROUBLE.search(previous)
                or TREATMENT.search(previous)
                or any(word in previous.lower() for word in GRIEF_WORDS)):
            return _a_check_choice(CHECK_A_FEELING, memory, salt)
        if _is_a_question(previous):
            return _a_check_choice(CHECK_A_QUESTION, memory, salt)
        if SAID_TO_THE_BOT.search(_plain_line(previous)):
            return _a_check_choice(CHECK_A_FEELING, memory, salt)
        said = thread.restate(previous)
        if said and len(said.split()) >= 3:
            checked_before = _a_check_came_before(memory, low)
            if not checked_before:
                return _a_check_choice(CHECK_PLAIN, memory, salt).format(said=said)
            return _a_check_choice(CHECK_A_FEELING, memory, salt)
        return _a_check_choice(CHECK_A_FEELING, memory, salt)
    record = current(memory)
    kept = str((record or {}).get("text") or "") if isinstance(record, dict) else ""
    if kept and not _is_a_question(kept):
        said = thread.restate(kept)
        if said and len(said.split()) >= 2:
            return _a_check_choice(CHECK_PLAIN, memory, salt).format(said=said)
    return _a_check_choice(CHECK_NOTHING_SAID, memory, salt)

def _plain_line(text):
    low = " ".join(str(text or "").lower().split())
    return " ".join(re.sub(r"[^a-z0-9' ]+", " ", low).split())

DECLINE_A_SUBJECT = re.compile(
    r"\bi\s+(?:do\s+not|don'?t|dont)\s+(?:" + INTENSIFIER + r"\s+)?"
    r"(?:want|wanna|need)\s+(?:" + INTENSIFIER + r"\s+)?to\s+"
    r"(?:talk|speak|think|hear)\s+about\s+(?P<subject>.+)$|"
    r"\bi(?:'?d|\s+would)\s+(?:" + INTENSIFIER + r"\s+)?rather\s+not\s+"
    r"(?:talk|speak)\s+about\s+(?P<rather>.+)$|"
    r"\b(?:let'?s|lets|can\s+we|could\s+we)\s+not\s+(?:talk|speak)\s+about\s+"
    r"(?P<let>.+)$")

NOT_A_SUBJECT = frozenset("""but and so because cos with without to about for then if when while
    though although or yet also plus as since unless until before after once""".split())


def _a_subject_to_leave_alone(low):
    for found in DECLINE_A_SUBJECT.finditer(low):
        subject = (found.group("subject") or found.group("rather")
                   or found.group("let") or "").strip()
        words = subject.split()
        if not words or len(words) > 4:
            continue
        if len(words) > 1 and words[0] in ("it", "that", "this"):
            continue
        if any(word in NOT_A_SUBJECT for word in words):
            continue
        before = low[:found.start()].split()
        if not all(word in CLOSE_FILLER for word in before):
            continue
        return True
    return False


def _closes_the_subject(text):
    low = _plain_line(text)
    if not low or len(low.split()) > 12:
        return False
    if re.match(r"(?:what|how|why|when|where|who|which)\b", low):
        return False
    if ASKS_WHETHER_TO.search(low) or ASKS_FOR_HELP.search(low):
        return False
    if CARRIES_ON_AFTER.search(HOLDS_FOR_NOW.sub(" ", low)):
        return False
    if _closes_by_a_frame(low):
        return True
    return _a_subject_to_leave_alone(low)


def _closes_by_a_frame(low):
    for pattern in (CLOSE_SUBJECT, CHANGE_SUBJECT):
        for found in pattern.finditer(low):
            rest = (low[:found.start()] + " " + low[found.end():]).split()
            if all(word in CLOSE_FILLER for word in rest):
                return True
    return False

def _a_plain_frame_closes(low):
    for pattern in (CLOSE_SUBJECT, CHANGE_SUBJECT):
        for found in pattern.finditer(low):
            if re.search(INTENSIFIER, found.group(0)):
                continue
            rest = (low[:found.start()] + " " + low[found.end():]).split()
            if all(word in CLOSE_FILLER_ALWAYS for word in rest):
                return True
    return False


def _held_thread(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)][-3:]
    for turn in turns:
        if turn.get("module") == "safety":
            return True
        said = str(turn.get("bot") or "").lower()
        if any(word in said for word in HELD_THREAD):
            return True
    return False

def _gentle_subject(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)][-4:]
    for turn in turns:
        if turn.get("module") in ("loss", "grief"):
            return True
        if any(word in str(turn.get("bot") or "").lower() for word in GRIEF_WORDS):
            return True
        if any(word in str(turn.get("user") or "").lower() for word in GRIEF_WORDS):
            return True
    return False

def _can_close(text, memory):
    if not _closes_the_subject(text):
        return False
    if not current(memory) and not recent(memory, 2):
        return False
    if _held_thread(memory):
        return False
    if _gentle_subject(memory) and not _a_plain_frame_closes(_plain_line(text)):
        return False
    return True

def _the_close(text, memory):
    if not isinstance(text, str) or not isinstance(memory, dict):
        return None
    if not _can_close(text, memory):
        return None
    low = _plain_line(text)
    gentle = _gentle_subject(memory)
    if CHANGE_SUBJECT.search(low):
        return pick(CHANGE_HEAVY if gentle else CHANGE_PLAIN, memory, low)
    return pick(CLOSE_HEAVY if gentle else CLOSE_PLAIN, memory, low)
