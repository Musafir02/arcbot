import random
import re
import string

from ..memory import ack, facts, history, last_bot, last_user, obstacle, reject, repeat, swap
from ..memory import stuck as stuck_line
from ..understanding import understand
from ..understanding.body import GOING_BOTH_WAYS
from ..understanding.kinds import (ANSWERING_A_QUOTED_ASK, greeting_only,
                                  the_manners_question, two_ends_of_one_scale,
                                  verdicts_a_thing)
from ..understanding.topics import IDIOM_PHRASES, THE_PEOPLE, is_a_machine_word
from . import (A_STEP_ASK, DOUBT, DOUBTED, LINGERED_LINE, NEARLY, says_it_has_lingered,
               step_when_low, turned, turns_round)
from . import (badnews, circumstance, draft, finding_out, goodnews, handoff, harm, leaving, loss,
               no_eyes, onething, outlook, pick, prices, quantity, reaction as answer_reaction,
               remark, stepwords, trouble, unseen, why, worn)
from .postcode import a_postcode_lookup
from .urgent import reads_as_a_story
from .badnews import (DEATH_SAID as SAID_AS_A_DEATH,
                      reads_as_a_closed_door, reads_as_an_award_lost, reads_as_bad_news,
                      reads_as_heavy_news, reads_as_news_with_a_name,
                      reads_as_pregnancy_bleeding, reads_as_the_leaving,
                      reads_as_a_leaving_already_gone, reads_as_a_pet_condition,
                      reads_as_the_speakers_own_plan,
                      reads_as_sudden_loss,
                      reads_as_a_carer_body, reads_for_a_carer, reads_for_a_pet,
                      reads_like_a_symptom)
from .goodnews import (reads_as_an_occasion, reads_as_a_win_nobody_noticed,
                       reads_as_a_clear_result, reads_as_good_news, reads_as_news_to_come,
                       reads_as_recovery,
                       reads_as_settled, worry_on_the_table)

from .not_knowing import (NAMES_WHERE_TO_ASK, POINTER_HEDGE, _an_ask_with_no_subject,
                          _asks_about_this_chat, _the_lead_and_the_route)
from .fallback_data import (
    A_DISMISSAL,
    A_FREE_TIME_ASK,
    A_LOVE_FOR_PEOPLE,
    A_LOVE_FOR_SOMEONE,
    A_SORRY_ON_ITS_OWN,
    ABOUT,
    ABOUT_ITSELF_KINDS,
    ABOUT_SELF,
    ABOUT_TALLY,
    ABOUT_THEM_BEFORE_COPULA,
    ABOUT_WORDS,
    ACK,
    ACKS,
    AGREEMENTS,
    ACK_AFTER_TROUBLE,
    ACK_WARM,
    ACTS_FOR_ME,
    ADVICE_AGAIN,
    ADVICE_COOL,
    ADVICE_COOL_WORDS,
    ADVICE_LENGTH,
    ADVICE_LENGTH_BARE,
    ADVICE_TIME,
    ADVICE_TURNS,
    ADVICE_WORDS,
    ADVICE_WORSE,
    AFRAID_AFTER,
    AFTER_RESOLVED,
    AGREEMENT,
    AIM_FAILING,
    AIM_HEADS,
    AIM_NEGATORS,
    ALIVE,
    ANIMALS,
    APOLOGY_ANSWER,
    ASKED_A_RATING,
    ASKED_IF_GOOD,
    A_GOODNESS_ASKED_OF_ME,
    A_SKILL_ASKED_OF_ME,
    ASKED_IF_I_SAW_LINES,
    ASKING_WORDS,
    ASK_ONLY,
    ASK_OUT_ANSWER,
    AT_IT_EXTRA,
    BECOMING,
    BECOMING_STATE,
    AT_IT_NOT,
    AXIS_MIN,
    A_BIRTHDAY_STILL_TO_COME,
    A_CHILD_LEAVING,
    A_CHILD_LEFT,
    A_COST_SOMEBODY_ASKS,
    A_DAY_AHEAD,
    A_DAY_AHEAD_TENSE,
    A_DREAD,
    A_GOOD_TIME,
    A_GOOD_TIME_IN_A_CARE_THREAD,
    A_HOW_THE_TIME_WENT,
    A_JOB_ON,
    A_JOB_SOON,
    A_LAUGH,
    A_MOOD_WITH_A_CATCH,
    A_PAUSE_WORD,
    A_PERSON,
    A_PLACE_I_DONT_KNOW,
    A_SMALL_DAY,
    A_BOOKING_AHEAD,
    A_BOOKING_AHEAD_DATED,
    A_SUGGESTED,
    A_SUGGESTED_BY_SOMEONE,
    A_THING_AHEAD,
    A_THING_BOUGHT,
    A_THING_DONE,
    A_THING_GONE,
    A_THING_LOOKS_SAD,
    A_THING_ON,
    A_THING_SEEN_TO,
    A_THING_THEY_REGRET,
    A_WANT_IT_OVER,
    ABUSE_AFTER,
    BABY_FOOD_NAMES,
    BABY_WHO,
    BAD_STRETCH,
    BAD_STRETCH_REPLIES,
    BARE_FOLLOW_UP_CARE_REPLIES,
    BARE_FOLLOW_UP_REPLIES,
    BARE_PICK_AFTER_NEWS,
    BARE_PICK_ASK,
    BARE_PICK_BRING,
    BARE_PICK_DO,
    BARE_PICK_EXPECT,
    BARE_PICK_GET,
    BARE_PICK_KIND,
    BARE_PICK_LOOK,
    BARE_PICK_ORDER,
    BARE_PICK_PREPARE,
    BARE_PICK_SIGN,
    BARE_PICK_TAKE,
    BARE_PICK_WEAR,
    BARE_PICK_WEAR_COLD,
    BARE_PICK_WEAR_HOT,
    BARE_PICK_WEAR_WET,
    BARE_PICK_WHICH,
    BEHIND_ON_MONEY,
    BLACKED_OUT_SIGHT,
    BODY_ALSO,
    BODY_BUNGED,
    BODY_COLD,
    BODY_HOT,
    BODY_HUNGRY,
    BODY_LEAD,
    BODY_LIGHT_HEAD,
    BODY_PARTS,
    BODY_PART_QUALIFIER,
    BODY_PART_TAIL,
    BODY_POOLS,
    BODY_QUEASY,
    BODY_SAYS_WHY,
    BODY_SITUATION,
    BODY_STATES,
    BODY_SUBJECT,
    BODY_TAIL,
    BODY_THIRSTY,
    BODY_WORD_FOR_A_THING,
    BOUGHT_VERB,
    BOUND_FOR,
    BURN_AFTER,
    BURN_BLISTER,
    BUYING_WORDS,
    CALL_ANSWER,
    CALL_WORDS,
    CAME_BACK,
    CARD_LINES,
    CARD_VALIDITY,
    CARE_AFTER,
    CARE_AFTER_ANIMAL,
    CARE_AFTER_ANIMAL_STILL,
    CARE_AFTER_STILL,
    CARE_BETTER,
    CARE_HERE,
    CARE_HURTS,
    CARE_INJURY,
    CARE_MODULES,
    CARE_NOT_RESOLVED,
    CARE_PHRASES,
    CARE_POINTER,
    CARE_PRONOUNS,
    CARE_RESOLVED,
    CARE_ROUTE_BACK,
    CARE_SEEN,
    CARE_SEEN_ANIMAL,
    CARE_THREAD,
    CARE_VISIT,
    CARE_VISIT_WARD,
    CARE_WORDS,
    CARING,
    CARING_FOR_A_BODY,
    CHECK_PHRASES,
    CHILD_AT_HOME,
    CHILD_FAINT,
    CHILD_FAINT_ANSWER,
    CHOICE_BETWEEN_PEOPLE,
    CHOICE_HEALTH,
    CHOICE_LIGHT,
    CHOICE_LIGHT_PICK,
    CHOICE_PEOPLE,
    CHOICE_PHARMACIST,
    CHOICE_STAKES,
    CHOICE_THERAPY,
    CHOICE_WEIGH,
    CLOSED_DOOR,
    COMFORT_SAID,
    COMPLAINT_WORDS,
    COMPLAIN_WHO,
    CONGRATS,
    CONTACT_ANSWER,
    COPULA,
    CRISIS_AFTER,
    CRISIS_AFTER_THEM,
    CRISIS_BETTER,
    CRISIS_BETTER_THEM,
    CRISIS_WORDS,
    CROWD,
    CUT_FOR,
    DARK_THING,
    DATES_KEEP_SLIPPING,
    DECLINED_PLAN,
    DECLINED_PLAN_GENTLE,
    DENTIST_WHO,
    DETAILS_IN_A_WARM_LINE,
    DEVICE_WHO,
    DISH_DETERMINER,
    DISH_PARTICIPLE,
    DITHER_DECIDE,
    DITHER_ABOUT_A_PERSON,
    STUCK_AFTER_TROUBLE,
    RUN_OUT_LINES,
    DITHER_OPEN_LINES,
    DITHER_TWO_WAY_LINES,
    DONE_NOT_A_PERSON,
    DONE_NOT_THIS,
    DONE_ONLY_A_THING,
    DONE_VERB,
    DOUBLE_BOOKED,
    EASING_FILLER,
    EATEN_KIND,
    EATING,
    EMERGENCY_AFTER,
    EMERGENCY_ANSWER,
    EMERGENCY_BETTER,
    EMERGENCY_BETTER_THEM,
    EMERGENCY_NOT_WORKED,
    EMERGENCY_WORDS,
    EMPTY,
    ENDINGS,
    EXPERT_WORDS,
    FAINT_COMING_ANSWER,
    FALLBACK_MODULE,
    FAVOURITE_GENERAL,
    FAVOURITE_WORDS,
    FILLERS,
    FILLING_FOODS,
    FILLING_WORDS,
    FIRST_PERSON,
    FLAT,
    FLAT_CORE,
    FLAT_LEAD,
    FLOPPY_WAKE,
    FORECAST,
    FORECAST_AFTER_SAFETY,
    FORECAST_A_FALL,
    FORECAST_BODY_WORDS,
    FORECAST_DURATION,
    FORECAST_HE_SHE,
    FORECAST_I_ASK,
    FORECAST_ILL,
    FORECAST_OFF_THEIR_FOOD,
    FORECAST_PERMISSION,
    FORECAST_PERSON,
    FORECAST_PET,
    FORECAST_PET_HARM,
    FORECAST_POOLS,
    FORECAST_RELATION,
    FORECAST_SELF,
    FORECAST_SELF_STRUGGLING,
    FORECAST_SOMEONE_STRUGGLING,
    FORECAST_STRUGGLE,
    FORGETTING,
    FORGET_A_THING,
    FOUND_IT,
    FRAME_WORDS,
    FUEL_WORDS,
    FUME_WORDS,
    GADGET_WORDS,
    GAS_ANSWER,
    GAS_WORDS,
    GENERIC_WORDS,
    GIFT_WORDS,
    GONE_VERB,
    GOOD_TIME_WORDS,
    GO_ANSWER,
    GO_TO_BE_SEEN,
    GREETING,
    GREETING_AFTER,
    GREETING_WORDS,
    GRIEF_AFTER,
    GRIEVANCE,
    GRIEVANCE_HARM,
    GRIEVANCE_HARM_PHRASES,
    GRIEVANCE_HEALTH,
    GRIEVANCE_HEALTH_PHRASES,
    GRIEVANCE_IMPACT,
    GRIEVANCE_NOT_A_THING,
    GRIEVANCE_PEOPLE,
    GRIEVANCE_PHRASES,
    GRIEVANCE_PRONOUN,
    GRIEVANCE_STRAIN,
    GRIEVANCE_STRAIN_SAID,
    GROWN_UP_WORDS,
    HABIT_ACT,
    HABIT_REPLY,
    HAND,
    HANDED_BACK,
    HAZARD_AFTER,
    HAZARD_WORDS,
    HEALTH_RECORD,
    HEALTH_RECORD_LINES,
    HEALTH_WHO,
    HEALTH_WORDS,
    HEALTH_WORLD,
    HANDS_BACK,
    HEDGE_POOL,
    HELLO_STILL_THERE,
    HELLO_WITH_YOU,
    HELP,
    HELPLINE_NOT_AN_AMBULANCE,
    HELP_ALREADY,
    HELP_TAIL,
    HELP_TOPIC,
    HELP_TOPIC_ANY,
    HOLD_AFTER,
    SORTED_AND_NO_CALL_YET,
    HOUSE_VERB,
    HOW_ARE_YOU,
    HOW_ARE_YOU_ASKS,
    HOW_ARE_YOU_GOING_ON,
    HOW_ARE_YOU_GOING_ON_AFTER,
    HOW_ARE_YOU_TAGS,
    HOW_TO_DECIDE_FILLER,
    HOW_TO_DECIDE_LINES,
    HUMAN_EMPTY,
    IDENTITY,
    IDIOM_GLAD,
    IDIOM_SHY,
    ILL_AFTER,
    ILL_BEFORE,
    ILL_SAID_OF_A_BODY,
    ILL_WILL_VERBS,
    IMPERATIVE,
    INVITED,
    INVITED_TO_TALK,
    INVITE_ACTIVITY,
    INVITE_FILLER,
    INVITE_NEVER,
    INVITE_PRONOUN,
    JUDGE_ASKS_FINE,
    JUDGE_ASKS_MAD,
    JUDGE_ASKS_SLIGHT,
    JUDGE_BARE_FACES,
    JUDGE_FINE,
    JUDGE_FINE_PLAIN,
    JUDGE_LEAD,
    JUDGE_NOD_WORDS,
    JUDGE_NOT_A_GERUND,
    JUDGE_NOT_A_VERDICT,
    JUDGE_NOUN,
    JUDGE_NO_PLAN,
    JUDGE_NO_PLAN_FINE,
    JUDGE_NO_PLAN_MAD,
    JUDGE_NO_PLAN_MIND,
    JUDGE_ONLY_A_PLAN,
    JUDGE_PLAN_HAS_A_HOLE,
    JUDGE_PLAN_STOP,
    JUDGE_SANE,
    JUDGE_SANE_PLAIN,
    JUDGE_SELF_JUDGING,
    JUDGE_SOUNDS_FINE,
    JUDGE_WISH_ANGRY,
    JUDGE_WORTH,
    JUDGE_WORTH_PLAIN,
    JUNK_CUES,
    KEEPS_FORGETTING,
    KNOCKED,
    KNOCKED_SPOTS,
    LANDED_BAD,
    LANGUAGE_FLUENCY,
    LATE_BEHIND_LINES,
    LATE_NOW_LINES,
    LAUGHING_WORDS,
    LEFT_POOL,
    LEFT_POOL_GONE,
    LIVE_DELAY_WORDS,
    LIVE_HOURS_ASK,
    LIVE_YES_NO_OPEN,
    LIVE_INDOOR,
    LIVE_JOURNEY_ENDS,
    LIVE_KINDS,
    LIVE_NEWS_REPLY,
    LIVE_NOT,
    LIVE_NOT_HOURS,
    LIVE_OPEN_CLOSE,
    LIVE_PAPER_WORDS,
    LIVE_ROAD_NAME,
    LIVE_ROADS_NOT,
    LIVE_ROAD_WORDS,
    LIVE_SETTING,
    LIVE_SITE_THING,
    LIVE_SKY,
    LIVE_SKY_OFF,
    LIVE_SKY_WHY,
    LIVE_SOON,
    LIVE_STRONG,
    LIVE_TAKE_ALLOWED,
    LIVE_TAKE_ASK,
    LIVE_TRAVEL_WORDS,
    LIVE_VENUE,
    LIVE_VENUE_RE,
    LIVE_WEAR,
    LIVE_WEATHER_WORDS,
    LOCKED_OUT_LINES,
    LOCKED_OUT_OF_THE_CAR,
    LOST_A_THING,
    LOST_A_THING_AGAIN,
    LOW_DAY_REPLIES,
    LUMP,
    MANNERS_ONLY,
    MEDS_WORDS,
    MEMORY,
    MESS_PLACES,
    MILESTONE,
    MILESTONE_EVENT,
    MISHAP_BACK,
    MODEL_NAMED_WORDS,
    MONEY_WORDS,
    MOOD_AFTER,
    MOOD_BEFORE,
    MOUTH_WORDS,
    MOVE_ON_AFTER,
    MYSELF,
    MY_DOING,
    MY_OWN,
    MY_OWN_DAY,
    MY_PICK,
    MY_PICK_ASK,
    MY_PICK_NOTE,
    MY_BILL_LINES,
    MY_RECORDS,
    OFFICE_RECORD_LINES,
    AT_THE_TILL,
    POINTS_LINES,
    MY_WORKINGS,
    NAMED_NEGATIVE,
    NAMED_TYPES,
    NARROW_ANSWERED,
    NARROW_SUBSTANCE,
    NARROW_WORDS,
    NEGATIVE,
    NEGATIVE_CUES,
    NEGATORS,
    NETWORK_WORDS,
    NEUTRAL,
    NEVER_MIND,
    A_CORRECTION_TAKEN,
    NEWS_TO_COME,
    NOT_AN_ANSWER,
    NOT_A_FORM,
    NOT_A_NAME,
    NOT_A_VERDICT_SUBJECT,
    NOT_CHOSEN,
    NOT_ENOUGH_REPLY,
    NOT_FIT_ENOUGH,
    NOT_NOTED,
    NOT_PEOPLE_WORDS,
    NOT_THEIR_VERB,
    NOT_TOO_OLD,
    NO_DIRECTION_REPLY,
    NO_MORE_OF,
    NO_WORDS_ASKING,
    NO_WORDS_AT_THE_CARE,
    NO_WORDS_SOMEONE,
    NO_WORDS_STUCK,
    OCCASION,
    ONE_SKILL_RATED,
    ONGOING_WORDS,
    ONLY_FRONT,
    OPINION_ASKS,
    OURS,
    OUTCOME_LINES,
    OWN_PERSON,
    OWN_PLACE,
    PARTICLE,
    PASSED_OUT_ANSWER,
    PASSED_OUT_PERSON,
    PASSWORD_TROUBLE,
    PAUSE_IN_A_SAFETY_THREAD,
    PAST_STATE_CUES,
    PAUSE,
    PENDING_DOUBT,
    PENDING_LANDED,
    PENDING_WAITING,
    PENDING_WHEN,
    PERSON_WORDS,
    PEST_WHO,
    PETROL_WORDS,
    PET_CONDITION_TROUBLE,
    PET_TROUBLE,
    PICKS_A_MECHANISM,
    PICK_ONLY_WORDS,
    PLAIN_WORDS,
    PLAN,
    PLAN_DONE,
    PLAN_DONE_ACK,
    PLAN_KNOCKED,
    PLASTER_IT,
    POINTING,
    POSITIVE,
    POSITIVE_CUES,
    PRAISE,
    PREGNANCY_BLEEDING,
    PRESENCE_LEFTOVER,
    PRESENT,
    PUNT,
    QUESTION_OPENERS,
    QUESTION_WORDS,
    QUIET_MODULES,
    QUOTE_LINES,
    REACTIONS_CARE,
    REACTIONS_SAID,
    REACTION_DISBELIEF,
    REACTION_DISBELIEF_SAID,
    REACTION_LEAD,
    REACTION_MISHAP,
    REACTION_MISHAP_SAID,
    REACTION_OUCH,
    REACTION_OUCH_SAID,
    REACTION_RELIEF,
    REACTION_RELIEF_SAID,
    REACTION_REPEAT,
    REACTION_REPEAT_FIRST,
    REACTION_WORD,
    REACTION_WORDS,
    REFUSED_REPLIES,
    RELATIONSHIP_DECISION,
    RELIEF,
    REPAIR_RULE,
    REPORT_FILLER,
    REQUEST_CUES,
    RESOLVED_AFTER,
    THE_CALL_STANDS_ANYWAY,
    RESOLVED_AFTER_THEM,
    RING_FOR_HELP,
    RING_THE_POLICE,
    ROUTINE,
    ROUTINE_NOT,
    ROUTINE_PHRASES,
    ROUTINE_WORDS,
    RULED_OUT_DETERMINER,
    RUMINATION_REPLIES,
    SAFETY_WORDS,
    SAME_AGAIN, SAME_AGAIN_WITH_THE_ANSWER,
    SCHOOL_TROUBLE,
    SCHOOL_WHO,
    SCHOOL_WORDS,
    SECRETS_KEEP_SLIPPING,
    SEEN_TO_VERB,
    SELF_BLAME,
    SELF_EATING_WORDS,
    SELF_FILLER,
    SELF_GROUP,
    SELF_JOB,
    SELF_JUDGEMENT,
    SELF_NOBODY,
    SELF_NOUN,
    SICKNESS,
    SOMEBODY_HURT,
    SOMEONE_ELSES_DAY,
    SOMEONE_GONE,
    SOMEONE_LEAVING,
    SOMEONE_SERIOUSLY_ILL,
    SORE_AMBIGUOUS,
    SORE_HANDS,
    SORE_ORDINARY,
    SORE_SERIOUS,
    SORE_WORDS,
    RETURNED_TO_A_THING,
    RETURNED_TO_IT,
    SORRY_FOR_ASKING,
    SORRY_ON_ITS_OWN,
    STATE_CUES,
    STILL_HERE_AFTER,
    STRETCH_OF_TIME,
    SUDDEN_LOSS,
    SUMMONS_RANG,
    SUMMONS_SEEN,
    SUMMONS_WRITTEN,
    SYMPTOM,
    SYMPTOM_COLD,
    SYMPTOM_WORDS,
    TAG_CONFIRM,
    TAG_UNSURE,
    TASTES,
    TASTE_GENERAL,
    TELL_HARD_LINES,
    TENANT_WHO,
    THANKS,
    THANKS_AFTER,
    THANKS_ONLY,
    THANKS_THEN_SAID,
    THANKS_WORDS,
    THANK_WORDS,
    THE_FIRST_HOUR_AND_A_CHILD,
    THING_AFTER,
    THING_STATES,
    THING_SUBJECT,
    THE_CALL_STANDS,
    THRESHOLD_CROSSED,
    THREAD,
    THREAD_PEOPLE,
    THREAD_TURNS,
    TIGHT_MONEY,
    TIGHT_MONEY_MORE,
    TIPS_AHEAD,
    TIPS_CLAUSE,
    TIPS_LINES,
    TIPS_OWNER,
    TIPS_THING,
    TIPS_UNIT,
    TIPS_VERB,
    TIRED,
    TOO_MUCH,
    TOO_MUCH_PHRASES,
    TRADER_WORDS,
    TRADES_WHO,
    TRADE_OFF_LEAN,
    TREATMENT_HARM,
    TRIED_HELPED_ELSEWHERE,
    TRIED_HELPED_REPLIES,
    ELDER_AID_REPLIES,
    ELDER_CLINIC_REPLIES,
    ELDER_DOCTOR_REPLIES,
    ELDER_HELP_REPLIES,
    TRIED_IT_REPLIES,
    TRIED_NO_CHANGE_ELSEWHERE,
    TRIED_SORTED_REPLIES,
    TRIED_NO_CHANGE_REPLIES,
    TRIED_WORSE_ELSEWHERE,
    TRIED_WORSE_REPLIES,
    TROUBLE_CUES,
    UNKNOWN,
    UNKNOWN_ABOUT_A_PET,
    UNKNOWN_ABOUT_SOMEONE,
    UNKNOWN_DECIDE,
    UNKNOWN_HEALTH,
    UNKNOWN_MONEY,
    UNKNOWN_REALISTIC,
    UNKNOWN_REALISTIC_CARE,
    UNKNOWN_TOO_LATE,
    UNKNOWN_WHO,
    UNKNOWN_WORD,
    UNKNOWN_WORD_NAMED,
    UNKNOWN_WEIRD_BARE,
    UNKNOWN_WORRY,
    VERDICT_ANNOY,
    VERDICT_BAD,
    VERDICT_FIRST,
    VERDICT_HEAVY,
    VERDICT_LUCK,
    VERDICT_NUMB,
    VERDICT_QUEUE,
    VERDICT_ROUGH,
    VERDICT_SETBACK,
    VERDICT_SHAME,
    VERDICT_WORD,
    VET_WHO,
    VIEW_AFTER_A_DEATH,
    VIEW_ASK_LINES,
    VIEW_COMPANY,
    VIEW_DECIDE,
    VIEW_HANDBACK,
    VIEW_LEAD_IN,
    VIEW_LINES,
    VIEW_MIRROR_LINES,
    VIEW_NO_SUBJECT,
    VIEW_ONLY_WORDS,
    VIEW_ON_GOOD_NEWS,
    VISIT_PRONOUNS,
    WALKED_INTO_POOL,
    WASNT_THERE,
    WHERE_SOMETHING_WRONG,
    WHOLE_LIST_AFTER,
    WHO_TO_ASK,
    JOINT_WORDS,
    _ASKS_ABOUT_THE_JOINT,
    _CHOOSING_BETWEEN_TWO,
    WHY_AFTER_TASTE,
    WILD_BIRDS,
    WIN_IN_A_SILENCE,
    WITH_YOU_AFTER,
    WORDING_LINES,
    WORD_ANYWHERE,
    WORD_FIXES,
    WORK_ABOUT,
    WORK_WHO,
    WORRY_FILLER,
    WORRY_WORDS,
    YOURS,
    YOU_SUBJECTS,
    _A_PERSON,
    _A_SOCIAL_THING,
    _BOUNDED,
    _COPULA,
    _CREATIVE,
    _DAY_WORDS,
    _ECHO_FILLER,
    _ISSUER,
    _MONEY_NOUN,
    BODY_IS_NOT_A_MACHINE,
    _NOT_AN_OWN_THING,
    _NO_DAY_OF_THEIR_OWN,
    _OPENING_QUESTIONS,
    _START_ASK,
    _SUBJECT_AFTER_AM,
    _THING_DONE_LINES,
    _THREAD_PEOPLE,
    _VERDICT_DET,
    _VERDICT_LEAD,
    _WAS,
    _WOUND,
)

from .fallback_data import (
    WOULD_HAVE_BEEN,
    RATES_A_SKILL,
    A_HEDGED_RATING,
    I_RATE_A_SKILL,
    SELF_SUBJECT,
    SELF_BLAME_ASKS,
    EMBARRASSMENT_WORD,
    THE_GROUND_OPENS,
    DIE_OF_IT,
    GOING_TO_DIE,
    SOMEONE_ELSES_SHAME,
    A_VERDICT_ON_THE_PERSON,
    THE_MOMENT_IS_THEIRS,
    A_SLIP,
    A_SOCIAL_SLIP,
    A_SLIP_IS_NOT_A_FALL,
    IN_A_ROOM,
    LAUGHED_AT_THEM,
    A_CROWD_LAUGHED,
    A_PERSON_LAUGHED,
    LAUGHED_AT,
    EMBARRASSED,
    NOTHING_SAID_YET,
)
from .fallback_data import (
    ABSENCE,
    A_WAY_OF_BEING,
    BARE_PICK_LOST,
    DITHER_SUBJECT,
    HABIT_PROBLEM_ACT,
    HEAVY_NEWS,
    HURT_EVENT,
    LEFT_BEHIND,
    NAMED_BODIES,
    NOT_WHAT_I_SAID,
    NUMBER_PLACES,
    ONLINE_ASK,
    PASSED_OUT,
    PASSING_OUT_A_THING,
    PRIVACY_ASK,
    PRIVACY_SHAPES,
    THE_DAY,
    THE_DAY_AHEAD,
    WORDING_SOMEONE,
    _LANDED,
)


def _bounded(phrase):
    pattern = _BOUNDED.get(phrase)
    if pattern is None:
        pattern = _BOUNDED[phrase] = re.compile(r"(?<![a-z])" + re.escape(phrase)
                                                + r"(?![a-z])")
    return pattern


def _has(clean, phrases):
    for phrase in phrases:
        if _bounded(phrase).search(clean):
            return True
    return False


def _plain(clean):
    return " ".join(word for word in clean.split() if word not in FILLERS)


def _matchable(text):
    text = str(text or "").lower().replace("\u2019", "'").replace("'", "")
    return " ".join(text.split())


def _asks_how_are_you(clean, repaired=""):
    forms = [_matchable(clean)]
    if repaired and _matchable(repaired) != forms[0]:
        forms.append(_matchable(repaired))
    for form in forms:
        for match in HOW_WAS_YOUR_TIME.finditer(form):
            if _nothing_but_tags(form, match.end()):
                return True
        for phrase in HOW_ARE_YOU_ASKS:
            for match in _bounded(_matchable(phrase)).finditer(form):
                if _nothing_but_tags(form, match.end()):
                    return True
        for phrase in HOW_ARE_YOU_GOING_ON:
            for match in _bounded(_matchable(phrase)).finditer(form):
                tail = form[match.end():]
                if re.search(r"\d", tail):
                    continue
                after = " ".join(re.findall(r"[a-z']+", tail))
                if after in HOW_ARE_YOU_GOING_ON_AFTER:
                    return True
        for pattern in (YOUR_DAY_ASK, YOUR_TIME_ASK):
            for match in pattern.finditer(form):
                if _nothing_but_tags(form, match.end()):
                    return True
    return False


def _nothing_but_tags(form, end):
    return all(word in HOW_ARE_YOU_TAGS for word in re.findall(r"[a-z']+", form[end:]))


HANDS_IT_BACK = re.compile(
    r"^(?:(?:o+k+(?:a+y+)?|right|so|well|then|h+m+|ha|ha+ha|please|ta|cheers|and|dunno)[, ]+)*"
    r"(?:(?:i |i'm |im )?(?:dont|don't|do not) (?:mind|care)[, ]+(?:so )?)?"
    r"(?:"
    r"(?:you|u|youre|you are|your) (?:pick|choose|decide|call it|the call|the choice|call"
    r"|choice|decision|expert|boss|shout)(?: (?:one|the one|one of them|then|first))?"
    r"|(?:you|u) (?:can|could|may|should) (?:pick|choose|decide|have (?:it|this|that))"
    r"|(?:ill |i will |i'll )?(?:let you|leave it to you|leave this to you|leave that to you)"
    r"(?: (?:pick|choose|decide|have (?:it|this|that)|take (?:it|this|that)))?"
    r"|(?:you|youve|you have) got (?:this|it|this one|that one)"
    r"|(?:its |it is |thats |that is )?(?:up to you|over to you|down to you|your call"
    r"|your shout)"
    r"|(?:youre|you are) (?:the (?:expert|boss|one who knows)|better at this)"
    r"|(?:whichever|whatever) (?:you|u) (?:think|want|like|prefer|reckon|say)"
    r")"
    r"(?:[, ]+(?:then|please|for me|really|honestly|ha|haha))*"
    r"\s*[.?!:)]*\s*$")

EMERGENCY_CALL = re.compile(r"\b(?:ambulance|paramedic|paramedics|999|911|112|fire brigade|"
                            r"fire service|fire engine|coastguard|lifeboat|mountain rescue|"
                            r"a&e|a and e|casualty|resus|defibrillator)\b")
POLICE_CALL = re.compile(r"\b(?:police|cops|101|law enforcement|the law)\b")
REACHING_THE_POLICE = re.compile(
    r"\b(?:call|calls|called|calling|ring|rings|rang|ringing|dial\w*|phone|phones|phoned|phoning|"
    r"report|reports|reported|reporting|tell|tells|telling|told|contact|contacts|contacted|"
    r"speak|speaks|speaking|spoke|talk|talks|talking|talked|go|goes|went|going|involve\w*|"
    r"ask|asks|asked|asking)\b")
_ASKING_FOR_THE_POLICE = re.compile(
    r"\b(?:need(?:s|ed)?|want(?:s|ed)?|get|gets|getting|got)\s+"
    r"(?:to\s+(?:\w+\s+)?)?(?:the\s+|a\s+|an\s+)?(?:police|cops|law enforcement)\b")
SOMETHING_HAPPENING = re.compile(
    r"\b(?:broke|broken|breaking|break\s?in|break-ins|burgl\w*|intruder|trespass\w*|"
    r"attacked|attacking|assault\w*|"
    r"threat\w*|stalk\w*|follow(?:ing|ed) me|chased|mugged|robbed|vandal\w*|smash\w*|"
    r"hit me|hurled|hitting me|abusive|in my (?:house|home|flat|garden|shed|garage)|"
    r"outside my (?:door|house|flat))\b")
_ASKS_TO_ACT = re.compile(r"^\s*(?:should|shall|do|did|would|will|is it|do (?:you|u)|"
                          r"would (?:you|u)|can (?:you|u)|could (?:you|u)|am i)\b"
                          r"|\b(?:should i|need an?|worth calling|better to call)\b"
                          r"|\b(?:do|should|shall|would|will|did|can|could|am|are)\s+(?:i|we)\b")
MINOR_HARM = re.compile(
    r"\b(?:stubbed|stubbing|paper cut|papercut|splinter|blister|blisters|hiccups?|dandruff|"
    r"verruca\w*|stye|athlete'?s foot|nappy rash|stitch|bruise[sd]?|bumped|graze[sd]?|grazed|"
    r"nicked|chapped|chafing|sunburn|hangover|ingrown|head ?lice|nits|cold|colds|cough|coughs|"
    r"sneez\w*|hayfever|hay fever|toothache|earache|sore throat|heartburn|indigestion|"
    r"constipat\w*|piles|sprain(?:ed)?|twisted ankle|scratched|insect bite|mosquito bite)\b")
DANGER_SYMPTOM = re.compile(
    r"\b(?:can'?t|cannot|not|isn'?t|stopped|struggling to|finding it hard to)\s+breath(?:e|ing)\b"
    r"|\b(?:not|never|isn'?t|un)\s*(?:responding|responsive|conscious)\b"
    r"|\b(?:chest pain|crushed|crushing|severe|heavy bleeding|bleeding (?:a lot|badly)|"
    r"won'?t stop|no pulse|seizure|fitting|overdose|took (?:too many|an overdose)|"
    r"stroke|anaphyla\w*|throat (?:closing|swelling)|blue lips|stopped breathing)\b")
_A_PLACE_TO_BE_SEEN = re.compile(r"\b(?:a&e|a and e|casualty|resus)\b")
_A_CALL_WORD = re.compile(r"\b(?:call|calls|calling|called|ring|rings|ringing|rang|phone|"
                          r"phoning|dial|dialling|dialing|999|911|112)\b")

_CONTACT = re.compile(r"\b(?:text|txt|ring|call|phone|message|msg|dm|email|mail|reply|answer|"
                      r"write|whatsapp|facetime|contact|reach out)\b")
AN_APOLOGY = re.compile(r"\b(?:say sorry|apologise|apologize|make up|make it up|own up|forgive me)\b")
ASKED_OUT = re.compile(r"\bask(?:ed)? (?:him|her|them|\w+) out\b|\bask (?:him|her|them) out\b")
_GOING = re.compile(r"\b(?:go|goes|going|attend|turn up|show up|make it)\b")
_NOT_INVITED = re.compile(
    r"\b(?:wasnt|was not|werent|were not|havent been|have not been|didnt get|did not get|"
    r"no|not|never got|never received)\s+(?:\w+\s+){0,2}invit\w*"
    r"|\buninvited\b|\bwithout an invit\w*\b|\bgatecrash\w*\b", re.I)
_CALLING = re.compile(r"\b(?:ring|ringing|call|calling|phone|phoning|facetime|phone up)\b")


DITHER = re.compile(r"\b(?:not sure|unsure|dont know|do not know|no idea|cant decide|"
                    r"cannot decide|cant make up my mind|cannot make up my mind|torn between|"
                    r"(?<!not )torn about|(?<!not )torn over|(?<!not )torn on|"
                    r"(?<!not )torn|conflicted|dithering|undecided|"
                    r"in two minds|two minds about|of two minds|going back and forth|"
                    r"keep changing my mind)\b")
DITHER_STRONG = re.compile(r"\b(?:(?<!not )torn between|"
                          r"(?:i|im|i m|i am|i was|i ve been|ive been|i feel|i felt|feel|"
                          r"feeling|we|we re|we are|we were|he|he s|he is|he was|she|she s|"
                          r"she is|she was|they|they re|theyre|they are|they were|you|"
                          r"you re|youre|hes|shes|"
                          r"you are|you were|seems|seemed|sounds|sounded|felt)\s+"
                          r"(?:so\s+|really\s+|very\s+|quite\s+|a bit\s+|still\s+)?"
                          r"torn\b(?! apart)|"
                          r"conflicted|dithering|undecided|two minds|"
                          r"going back and forth|cant decide|"
                          r"cannot decide|cant make up my mind|cannot make up my mind|"
                          r"keep changing my mind)\b")
DITHER_OPEN = re.compile(r"\bwhat to do\b|\bwhat (?:i|you) (?:should|can|ought to) do\b"
                         r"|\bwhat next\b")
STUCK_ON_A_PERSON = re.compile(
    r"\b(?:what to do|what (?:i|you) (?:should|can|ought to) do|"
    r"what (?:do|should|shall|can|could) (?:i|you|we) do)\s+(?:about|with)\s+"
    r"(?P<who>"
    r"(?:(?:my|our)\s+(?:[a-z0-9']+\s+){0,3})?"
    r"(?:mother in laws?|father in laws?|sister in laws?|brother in laws?|"
    r"son in laws?|daughter in laws?|in laws|inlaws|husband|wife|partner|boyfriend|girlfriend|"
    r"brother|sister|son|"
    r"daughter|child|kid|boy|girl|baby|mum|mom|mother|dad|father|nan|gran|grandma|grandad|"
    r"grandpa|grandmother|grandfather|grandparents|grandson|granddaughter|friend|mate|boss|"
    r"colleague|neighbour|neighbor|in laws|inlaws|teenager|family|"
    r"teacher|carer|relative|cousin|uncle|aunt|nephew|niece|stepson|stepdaughter|ex)|"
    r"(?:my|our)\s+\d+\s+(?:year|month|week)s?\s+old)"
    r"(?![a-z0-9])"
    r"(?P<rest>.*)$")
STUCK_PERSON_TAIL_PHRASE = re.compile(
    r"^(?:"
    r"at the moment|at the minute|at the mo|at present|at this point|as it stands|"
    r"right now|just now|these days|nowadays|currently|"
    r"and thats it|thats it|i mean|i suppose|i guess|of all things|"
    r"now|today|tonight|though|then|please|anymore|any more|first|just|still|about|too|"
    r"either|really|honestly|seriously|actually|like|again|lately|all|eventually|so|and|"
    r"or|ok|okay|basically|thanks|cheers|please|now though|then though)"
    r"(?![a-z0-9])", re.I)
STUCK_A_CLAUSE_ABOUT_THEM = re.compile(
    r"^,\s*(?:"
    r"(?:he|she|they|him|her|them)\b[ a-z0-9']{0,48}"
    r"|(?:aged|age)\s+\d{1,3}"
    r"|\d{1,3}\b[ a-z0-9']{0,24}"
    r")$")
STUCK_AND_ANOTHER_PERSON = re.compile(
    r"^(?:,\s*)?(?:and|or)\s+(?:(?:my|our)\s+)?[a-z0-9']+(?:\s+[a-z0-9']+){0,3}$")
STUCK_DESCRIBES_THE_PERSON = re.compile(
    r"^(?:,\s*)?(?:"
    r"(?:that|which|who|whose|whos|who's)\b[ a-z0-9']{0,40}"
    r"|(?:of|been|together|married)\b[ a-z0-9']{0,24}"
    r")$")


def _the_person_ends_the_ask(rest):
    rest = str(rest or "").lstrip(" ").rstrip(" ?.!,")
    if not rest.strip(" ,?!."):
        return True
    if STUCK_AND_ANOTHER_PERSON.match(rest):
        return True
    if STUCK_DESCRIBES_THE_PERSON.match(rest):
        return True
    if STUCK_A_CLAUSE_ABOUT_THEM.match(rest):
        return True
    left = rest
    while True:
        found = STUCK_PERSON_TAIL_PHRASE.match(left)
        if not found:
            break
        left = left[found.end():].lstrip(" ,?!.")
    return not left


def _the_person_they_are_stuck_on(clean):
    found = STUCK_ON_A_PERSON.search(clean)
    if not found or not _the_person_ends_the_ask(found.group("rest")):
        return ""
    who = _yours(found.group("who"))
    if who.lower().startswith("our "):
        who = "your " + who[4:]
    return who


STUCK_ONLY_WORDS = frozenset("""
i im ive dont do not know have has got had no idea clue what to next now anymore any more really
even so just and but then about with still whats honestly right today hmm erm um please help
havent hasnt didnt doesnt a an at all
stuck where start begin beginning first how supposed even feeling bit feel need help
""".split())

A_HELP_WORD = re.compile(r"\b(?:help|hand|advice)\b")

RUN_OUT = re.compile(
    r"\b(?:(?:what else|nothing else)(?:\s+(?:i|id|i'?d|to|can i))?\s*(?:do|can|try)\b|"
    r"what else\s*$|"
    r"nothing (?:(?:else|more) )?(?:i can do|to do|left|works?)\b|"
    r"what i can do\b|"
    r"(?:cant|cannot|can not) do (?:this|it)\b|"
    r"i give up\b|"
    r"no point(?:_in)?\b|"
    r"where to go from here\b|"
    r"how to fix (?:it|this)\b)", re.I)
RUN_OUT_DOUBT = re.compile(r"\b(?:dont|do not|not|never)\s+(?:even\s+)?know\b|\bno idea\b|"
                           r"\bnot sure\b", re.I)
RUN_OUT_EMPTY = re.compile(
    r"\b(?:nothing (?:else |more )?(?:i can do|to do|left|works?)|theres nothing|"
    r"(?:cant|cannot|can not) do (?:this|it)|i give up|no point)\b", re.I)
STUCK_PHRASES = re.compile(
    r"\b(?:stuck|what to do|where (?:do|should|would) i (?:start|begin)|"
    r"(?:where|how) to (?:start|begin)|where i (?:start|begin)|"
    r"(?:what|which) (?:to do )?first|what with)\b")


A_SUBJECT_ABOVE = re.compile(
    r"\b(?:my|our|his|her|their|the|he|she|they|him|them)\s+[a-z]")


def _a_subject_above(memory):
    if not isinstance(memory, dict):
        return False
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    if not turns:
        return False
    return bool(A_SUBJECT_ABOVE.search(str(turns[-1].get("user") or "").lower()))


def _a_bad_line_above(memory):
    if not isinstance(memory, dict):
        return False
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    if not turns:
        return False
    last = str(turns[-1].get("user") or "")
    if not last.strip():
        return False
    return _mood(_words(last), last) == "negative"


RUN_OUT_WORDS = STUCK_ONLY_WORDS | frozenset("""
else id cant cannot can not give up point left works fix it this go from here try anything
nothing theres there to
""".split())


def _run_out(clean):
    words = re.findall(r"[a-z']+", clean)
    if not words or not RUN_OUT.search(clean):
        return False
    if not (RUN_OUT_DOUBT.search(clean) or RUN_OUT_EMPTY.search(clean)):
        return False
    return all(word.strip("'") in RUN_OUT_WORDS for word in words)


def _a_dead_end(clean):
    return _only_the_stuck_phrase(clean) or _run_out(clean)


def _only_the_stuck_phrase(clean):
    words = re.findall(r"[a-z']+", clean)
    if not words or not STUCK_PHRASES.search(clean):
        return False
    return all(word.strip("'") in STUCK_ONLY_WORDS for word in words)


def _a_question_about_the_person(clean, memory):
    who = _the_person_they_are_stuck_on(clean)
    if not who:
        return None
    return _choose([line.format(who=who, Who=who[:1].upper() + who[1:])
                    for line in DITHER_ABOUT_A_PERSON], memory, clean)

DITHER_YES_NO = re.compile(r"\b(?:whether|if)\b")
HOW_TO_DECIDE = re.compile(
    r"\bhow (?:should|do|can|could|would|might|will) (?:i|we) (?:decide|choose|pick|"
    r"work (?:it |that |this )?out|figure (?:it |that |this )?out|know which|tell which)\b"
    r"|\bhow (?:do|should|can) i (?:make|reach|come to) (?:a |the )?decision\b"
    r"|\bwhats?\s+(?:is\s+)?the best way to (?:decide|choose|pick)\b")
SAYS_THE_SIDES = re.compile(r"\W*(?:between\b|whether\b|if\b|which (?:one|of|to)\b)")


def _nothing_to_choose(rest):
    if SAYS_THE_SIDES.match(rest):
        return True
    words = re.findall(r"[a-z0-9']+", str(rest or "").lower())
    return not [w for w in words if w not in HOW_TO_DECIDE_FILLER]


DITHER_TWO_WAY = re.compile(r"\b(?:whether|if|between|or|which)\b")
LIFE_DIRECTION = re.compile(r"\b(?:with|out of|from) my life\b|\bwhat i (?:actually )?want to do\b"
                            r"|\b(?:twenties|thirties|forties|20s|30s|40s)\b"
                            r"|\bnothing (?:feels|seems) right\b"
                            r"|\bwhat (?:am i|im) (?:even )?doing with my life\b")


A_STRETCH_OF_TIME = re.compile(
    r"\bwhat (?:to|should i|can i|could i|shall i) do (?:with|on|for)\s+(?:my|the|this|these)\s+"
    r"(?:afternoon|evening|morning|day off|day|weekend|week|time|night|days off|holidays?)\b")


def _the_stretch_of_time(clean, memory):
    if not A_STRETCH_OF_TIME.search(clean or ""):
        return None
    return _choose(A_FREE_TIME_ASK, memory, clean)


def _weighs_a_choice(clean):
    if DITHER_TWO_WAY.search(clean):
        return True
    return not (LIFE_DIRECTION.search(clean) or A_STRETCH_OF_TIME.search(clean))


FACT_BETWEEN = re.compile(r"\b(?:difference|differ|gap|distance|space|time|line|border|"
                          r"connection|link)\s+(?:\w+\s+)?between\b")


HELP_SERVICE = re.compile(
    r"\b(?:go|going|went|get|getting|take|taking|took|bring|bringing|drive|driving|rush|rushing|"
    r"walk|walking)\b(?:\s+\w+){0,3}?\s+(?:to\s+|into\s+)"
    r"(?:a and e|a&e|999|111|casualty|the hospital|hospital|the doctor|a doctor|doctor|"
    r"the doctors|doctors|the gp|gp|my gp|the surgery|the vets|vets|the vet|vet|"
    r"walk in centre|urgent care|out of hours|the pharmacy)\b"
    r"|\b(?:call|called|calling|ring|ringing|rang|phone|phoned|phoning|see|seeing|saw|book|"
    r"booking|booked)\b\s+(?:999|111|an ambulance|the doctor|a doctor|the gp|the surgery|"
    r"the vets|the vet|a vet|urgent care)\b")
PERSON_NOT_A_DECISION = re.compile(r"\bwhat to do (?:about|with) (?:my|his|her|our|their|the)\s+"
                      r"(?:husband|wife|partner|boyfriend|girlfriend|brother|sister|son|"
                      r"daughter|child|kid|boy|girl|baby|mum|mom|mother|dad|father|nan|gran|"
                      r"grandma|grandad|grandpa|friend|boss|colleague|neighbour|neighbor|"
                      r"in laws|inlaws|teenager|family|teacher|carer|relative|cousin|uncle|"
                      r"aunt|nephew|niece|ex|stepson|stepdaughter)\b")
PRONOUN_NOT_A_DECISION = re.compile(r"\bwhat to do (?:about|with) (?:it|this|that|him|her|them|us|me|"
                       r"everything|anything|nothing)\b")


HEALTH_MODIFIER = re.compile(r"\b(?:hospital|doctors?|surgery|clinic|vets?)\s+"
                             r"(?:job|jobs|shift|shifts|appointment|appointments|letter|"
                             r"letter|bill|parking|car park|contract|rota|placement|course|"
                             r"uniform|policy|department|ward)\b")


def _reads_as_dither(clean, repaired=None):
    lines = [clean]
    if repaired and repaired != clean:
        lines.append(repaired)
    for line in lines:
        if FACT_BETWEEN.search(line):
            continue
        if (PERSON_NOT_A_DECISION.search(line) or PRONOUN_NOT_A_DECISION.search(line)
                or HELP_SERVICE.search(line)):
            continue
        if DITHER.search(line) and (DITHER_STRONG.search(line) or DITHER_SUBJECT.search(line)):
            return True
    return False


DECIDE_OPENING = re.compile(r"(?:^|[,.!?;]\s*|\b(?:so|but|then|and|ok|okay)\s+)"
                            r"(?:should (?:i|we)|shall (?:i|we)|is it worth|is it better|"
                            r"would it be better|"
                            r"which (?:one )?should i|(?:do |)(?:you|u|ya) (?:think|reckon) i should|"
                            r"what would you do|"
                            r"do i (?:say|tell|ask|mention|reply|text|call|ring|accept|"
                            r"send|bring)\b|"
                            r"would you)\b")
DECIDE_SANITY = re.compile(
    r"\b(?:would|will|does|do|is|was|are)\b[^.?!]{0,34}?\b(?:be|look|seem|sound)\s+"
    r"(?:like\s+)?(?:a\s+|an\s+)?(?:mad|crazy|stupid|silly|nuts|weird|strange|odd|bizarre|"
    r"selfish|unreasonable|rude|cheeky|bad|wrong|over\s+the\s+top|a\s+mistake)\b"
    r"|\b(?:am|are|was)\s+(?:i|we)\b[^.?!]{0,20}?\b(?:being\s+|just\s+|so\s+|too\s+)?"
    r"(?:mad|crazy|stupid|silly|selfish|unreasonable|a\s+fool|out\s+of\s+order|"
    r"over\s+the\s+top)\b"
    r"|\b(?:is|would|was)\s+it\s+(?:mad|weird|stupid|silly|crazy|a\s+mistake|a\s+bad\s+idea|"
    r"wrong)\s+to\b"
    r"|\b(?:mad|weird|stupid|silly|crazy)\s+(?:idea|thing)\s+to\b"
    r"|\b(?:would|does|will|did)\s+(?:it|that|this)\s+look\s+(?:bad|silly|stupid|mad|odd|"
    r"weird|rude)\b"
    r"|\b(?:is|was|would)\s+it\s+(?:weird|strange|odd|stupid|silly|crazy|mad|selfish|"
    r"unreasonable)\s+that\b")

_DEFINITION = re.compile(r"^\s*(?:what|what's|whats|wats)\s+(?:is|are|was|were|does|do)\b"
                         r"|^\s*what(?:'s|s)?\s+(?:a|an|the)\b"
                         r"|^\s*(?:explain|tell me about|define)\b|\bwhat does .* mean\b")
SORE_PLACE = re.compile(
    r"\b(?:my|under my|behind my|between)\b"
    r"|\b(?:this|that)\s+(?:spot|sore|lump)s?\b"
    r"|\bon (?:my )?\w*(?:chin|cheek|face|jaw|nose|forehead|lip|ear|neck|back|shoulder|arm|"
    r"armpit|elbow|wrist|hand|finger|thumb|leg|thigh|knee|shin|ankle|foot|feet|heel|toe|"
    r"chest|breast|belly|stomach|bottom|bum|groin|skin|scalp|eyebrow|eyelid|head|hip|side)\b"
    r"|\b(?:chin|cheek|forehead|jaw|armpit|elbow|wrist|thumb|knee|shin|ankle|heel|toe|"
    r"scalp|eyelid|eyebrow|breast|groin)\b")
SORE_DOING = re.compile(r"\b(?:squeeze|squeezing|squeezed|pop|popping|popped|lance|lancing|"
                        r"prick|pricking|burst|bursting|drain|draining|pick|picking|scratch|"
                        r"scratching)\b")
SORE_PICKING = re.compile(r"\b(?:pick|picking|picked)\b")
SORE_ONLY_A_BODY = re.compile(r"\b(?:squeeze|squeezing|squeezed|pop|popping|popped|lance|"
                             r"lancing|prick|pricking|burst|bursting|drain|draining|scratch|"
                             r"scratching)\b")
PLASTER_ON = re.compile(
    r"\b(?:put |a |some )?plaster\b[^.]{0,18}?\bon (?:it|this|that|there|them|my \w+)\b"
    r"|\b(?:put |a |some )?(?:bandage|dressing|antiseptic|compress)\b[^.]{0,18}?"
    r"\bon (?:it|this|that|there|them|my " + _WOUND + r")\b"
    r"|\b(?:cover|cover it|covering)[^.]{0,16}"
    r"\b(?:plaster|bandage|dressing)\b"
    r"|\b(?:bandage|dressing|antiseptic|compress|plaster)\b[^.]{0,6}?\b(?:on|over) "
    + _WOUND + r"\b")

_PAY_DEBT = re.compile(r"\bpay(?:s|ing|ed)?\s+(?:it\s+|them\s+|that\s+)?(?:off|back|down|into|up)\b")

_CARD_MONEY = re.compile(
    r"\b(?:credit|debit|bank|store)\s+cards?\b|"
    r"\b(?:cancel|freeze|block|replace|stop|report|stolen|lost|cloned|skimmed)\s+"
    r"(?:my|the|that|this|our|a)\s+cards?\b|"
    r"\bcards?\s+(?:was|is|got)\s+(?:cloned|skimmed|stolen|lost)\b")

_VALUE_OF_THING = re.compile(r"\bis it worth (?:paying|paying for|getting|having|going for|"
                             r"splashing out on)\b")


WORRY_SELF = re.compile(r"\b(?:am i (?:overreacting|overthinking|over-thinking|over thinking|"
                         r"reading too much(?: into (?:it|this))?|being|mad|unreasonable|silly|"
                         r"wrong|too much|too sensitive|over the top)|overreacting|"
                         r"making a (?:fuss|big deal)|too sensitive)\b")
SHOULD_WORRY = re.compile(r"\bshould i (?:be )?(?:worried|worry|worrying)\b")
WORRY_SHAPE = re.compile("(?:" + WORRY_SELF.pattern + "|" + SHOULD_WORRY.pattern + ")")
SHOULD_WORRY_FILLER = re.compile(r"\b(?:is|it|that|this|ok|okay|so|or|and|but|then|now|just|"
                                 r"really|honestly|about|i|me|a|bit)\b")

WEIRD_ASK = re.compile(r"\b(?:is|was|isnt|am i)\s+(?:that|this|it)\s+(?:a bit |really |actually |so )?"
                       r"(?:weird|normal|normalish|strange|odd|wrong|bad)\b"
                       r"|\bis it (?:weird|normal|strange|odd)\b"
                       r"|\bam i (?:weird|strange|odd|abnormal)\b")
FEELING_SAID = re.compile(r"\b(?:feel|feels|feeling|felt|happy|unhappy|sad|guilty|angry|upset|cry|"
                          r"cried|crying|tears|flat|numb|empty|lonely|miss|hate|proud|ashamed|"
                          r"embarrassed|scared|anxious|relieved|gutted|glad|miserable|"
                          r"heartbroken)\b")
TOO_LATE = re.compile(
    r"^(?:and |but |so |ok |okay )?(?:is|was|isnt) (?:that|this|it) (?:too|a bit too|a little too) "
    r"(?:late|old)(?: now| then| in the day)?$"
    r"|^(?:and |but |so )?am i (?:too|a bit too|a little too) (?:old|late)(?: for (?:it|this|that))?$"
    r"|^(?:and |but |so )?is (?:that|this|it) (?:too|a bit too) old for me$"
    r"|^(?:and |but |so )?have i (?:left it|started it) too late$"
    r"|^(?:and |but |so )?is it too late for me$"
    r"|^(?:and |but |so )?is \d{1,2} too old(?: for (?:it|this|that))?$"
    r"|^(?:and |but |so )?is it too late to (?:start|begin|learn)(?: now| at my age)?$"
)
REALISTIC = re.compile(
    r"^(?:and |but |so |ok |okay |right )?(?:is|was|would|will) (?:that|this) (?:even )?(?:be )?"
    r"(?:a )?(?:realistic|doable|achievable|feasible|plausible|too ambitious|unrealistic)"
    r"(?: for (?:me|us|you))?$"
    r"|^(?:and |but |so |ok |okay )?is (?:that|this) enough time(?: for (?:me|us|you))?$"
    r"|^(?:and |but |so )?can (?:i|we) really (?:do|manage|fit|swing) (?:that|this|it)$"
    r"|^(?:and |but |so )?(?:am i|are we) (?:being )?(?:too ambitious|aiming too high|overdoing it)$"
    r"|^(?:and |but |so )?do you think (?:that|this|it|its|it's|thats|that's) (?:is |would be )?"
    r"(?:a )?(?:realistic|doable|achievable)$"
)


REALISTIC_ABOUT_ME = re.compile(
    r"^(?:and |but |so )?(?:am i|are we) (?:being )?unrealistic$"
)

PLAN_WORDS = re.compile(
    r"\b(?:plan|plans|planning|goal|target|deadline|budget|train(?:ing)?|course|classes|lessons|"
    r"marathon|half marathon|10k|5k|parkrun|diet|saving|save)\b"
    r"|\b(?:in|by|before|until) (?:a |one |two |three |four |five |six |seven |eight |nine |ten |"
    r"\d+ )?(?:week|weeks|month|months|year|years|january|february|march|april|may|june|july|"
    r"august|september|october|november|december|spring|summer|autumn|winter|christmas|easter)\b"
    r"|£\s?\d|\d+\s?k\b")


def _a_plan_in_the_thread(clean, memory):
    for text in (clean, _the_line_before(memory)):
        said = str(text or "").lower()
        if said and (PLAN_WORDS.search(said) or TAKING_UP.search(said)):
            return True
    return _a_thing_they_started(memory)


SOMEONE_CLOSE = re.compile(
    r"\b(?:my|his|her|our|their)\s+(?:mum|mom|mother|mam|dad|father|pa|nan|nana|nanna|gran|"
    r"granny|grandma|grandad|grandpa|grandmother|grandfather|mother\s+in\s+law|"
    r"father\s+in\s+law|aunt|auntie|uncle|neighbour|neighbor|husband|wife)\b"
    r"|\b(?:he|she|hes|shes|he's|she's|they|theyre|they're)\b[^.!?]{0,25}?"
    r"\b(?:[7-9]\d|1\d\d|elderly|pensioner|oap|in (?:his|her|their) (?:70s|80s|90s))\b",
    re.I)
SOMEONE_ELSE = re.compile(r"\b(?:she|he|they|him|her|them)\b", re.I)
A_CHILD = re.compile(
    r"\b(?:my|our|his|her|their)\s+(?:son|daughter|child|children|kid|kids|baby|toddler|"
    r"boy|girl|little\s+one|teenager|teen)\b"
    r"|\b(?:hes|shes|he's|she's|theyre|they're)\s+(?:one|two|three|four|five|six|seven|eight|"
    r"nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|18 months)\b", re.I)
REFUSES_IT = re.compile(
    r"\b(?:wont|won't|will\s+not|refuses|refused|refusing|doesnt\s+want|doesn't\s+want|"
    r"didnt\s+want|didn't\s+want|does\s+not\s+want|will\s+not\s+have|wont\s+have|"
    r"won't\s+have|wont\s+let|won't\s+let|wont\s+accept|won't\s+accept)\b", re.I)
AN_AID = re.compile(
    r"\b(?:stick|sticks|walking\s+stick|frame|zimmer|walker|rollator|pendant|alarm|"
    r"bath\s+lift|shower\s+seat|grab\s+rails?|"
    r"key\s+safe|stairlift|commode|incontinence\s+pads?)\b", re.I)
A_CLINIC = re.compile(
    r"\b(?:hearing\s+aids?|glasses|specs|spectacles|dentures|contact\s+lenses|"
    r"hearing\s+test|eye\s+test)\b", re.I)
THE_DOCTOR = re.compile(
    r"\b(?:doctor|doctors|doctor's|gp|gps|surgery|hospital|"
    r"appointment|check\s*-?\s*up|blood\s+test|scan|physio\w*|dentist|optician|"
    r"memory\s+clinic|chiropodist)\b", re.I)
HELP_IN = re.compile(
    r"\b(?:carers?|care\s+worker|home\s+help|help(?:ing)?\s+(?:in|out|around)|anyone\s+in|"
    r"somebody\s+in|someone\s+in|anybody\s+in|strangers?\s+in|a\s+cleaner|cleaner|"
    r"home\s+care|meals\s+on\s+wheels|respite|a\s+carer|paid\s+help|"
    r"district\s+nurse|the\s+nurse|nurse\s+in|occupational\s+therapist|ot\s+in)\b", re.I)


def _a_carer_refused(clean):
    if not REFUSES_IT.search(clean) or A_CHILD.search(clean):
        return None
    if not (SOMEONE_CLOSE.search(clean) or SOMEONE_ELSE.search(clean)):
        return None
    if A_CLINIC.search(clean):
        return "clinic"
    if AN_AID.search(clean):
        return "aid"
    if THE_DOCTOR.search(clean):
        return "doctor"
    if HELP_IN.search(clean):
        return "help"
    return None


def _a_plan_doubt(pred, clean, repaired):
    for text in (clean, repaired):
        if pred(text):
            return True
        tail = text.rsplit(",", 1)[-1].strip() if "," in text else ""
        if tail and pred(tail):
            return True
    return False

_AGE_DOUBT = re.compile(r"\b(?:old|older|age|aged|past it|spring chicken|\d{2})\b", re.I)
A_BIT_PAST_IT = re.compile(
    r"^(?:and |but |so |well |also )?(?:im|i'?m|i am)\s+(?:"
    r"\d{1,2}\s*[,;]?\s*(?:(?:and|but|now)\b|,)[^.!?]*"
    r"|(?:quite |very |pretty |a bit |a little |really |fairly |properly |so |"
    r"not that |not especially )?"
    r"(?:unfit|overweight|old|out of shape|out of practice|past it|no spring chicken|"
    r"fit as i was|as fit as i was)\b[^.!?]*"
    r"|(?:not|no longer|less than|hardly)\s+(?:very\s+|that\s+|especially\s+)?"
    r"(?:fit|strong|sporty|good at it)\b[^.!?]*)")
TAKING_UP = re.compile(
    r"\b(?:im|i'm|i am|ive|i've|i) "
    r"(?:(?:just|finally|also|now|really|still|even) )?"
    r"(?:(?:thinking (?:of|about)|want(?:ing)? to|try(?:ing)? to|hoping to|planning to|"
    r"about to|going to) )?"
    r"(?:start(?:ing|ed)?|learn(?:ing|t)?|began|beginning|tak(?:e|ing) up|took up|"
    r"going back to|back at|get(?:ting)? (?:back )?into|join(?:ing|ed)?|"
    r"sign(?:ing|ed)? up (?:for|to))\b")


def _a_bare_worry(clean):
    found = SHOULD_WORRY.search(clean)
    if not found:
        return False
    rest = clean[:found.start()] + " " + clean[found.end():]
    rest = SHOULD_WORRY_FILLER.sub(" ", rest)
    return not re.sub(r"[^a-z0-9]", "", rest)


def _worry_is_about_the_body(clean, words):
    words = set(words)
    return bool(words & BODY_PARTS or words & HEALTH_WORDS or words & SYMPTOM_WORDS
                or any(phrase in clean for phrase in CHECK_PHRASES))


UNKNOWN_HOW_IT_GOES_FOR_SOMEONE = (
    "Only the people looking after them can say, and they will tell you straight if you ask - "
    "their own GP, whoever is treating them. What has changed since you last heard?",
    "I would be guessing, and this is not a thing to guess about. Ask whoever is treating them, or "
    "ring 111 if it has got worse today. How are they in themselves?",
    "That one is with the people who can see them, not with me. Ask it plainly when you next speak "
    "to them, and if they fob you off, ask again. What were you told last?",
    "Nobody can promise how it will go, and anyone who does is guessing too. Their GP will give "
    "you the honest picture, and asking is not fussing. What worries you most?",
    "I cannot know that from here and I will not pretend to. Ring their GP and ask it as you asked "
    "me - they answer this every day. How long has it been like this?",
)
UNKNOWN_HOW_LONG_IN_HOSPITAL = (
    "How long is the ward's to say, and they will tell you: ask for the plan in days rather than "
    '"a while", and ask who to ring for updates. What have they said so far?',
    "That depends on what they are treating, so it is their team's answer rather than mine. Ask "
    "what has to happen before they can come home - that is the number that matters. Have they "
    "given you a plan?",
    "Nobody here can say, and the team looking after them will: they give a rough plan and revise "
    "it as things change. Ask what to expect over the next few days. How are they in themselves?",
)
UNKNOWN_HOW_IT_GOES_FOR_A_HARD_TIME = (
    "Only they can say how they are doing, and asking them is worth more than a guess from me. Ask "
    "how they are in themselves. If it has been weeks rather than days, their GP is the place to "
    "start - that is what they are there for.",
    "I cannot tell you how somebody else is going to be, and anyone who says they can is guessing. "
    "Ask them straight, and ask again if the first answer is that they are fine. If it drags on, "
    "or they are not sleeping or eating, a GP appointment is the usual next step.",
    "That one is theirs to say, not mine. What helps most is asking how they are and then "
    "listening rather than fixing it. If it runs for weeks, or they stop sleeping or eating "
    "properly, that is a GP question rather than a search one.",
)
UNKNOWN_HOW_IT_GOES_FOR_A_PET = (
    "Only the vet can say, and that is why the call is the answer - they would much rather hear "
    "it now than later. If they go wobbly, sick or sleepy, that is an evening vet, not a morning "
    "one.",
    "I cannot tell you that, and I would not guess about an animal. Ring the vet and say what "
    "happened; how are they in themselves right now?",
    "That one belongs to the vet rather than to me. While you ring, watch them: eating, moving "
    "about, themselves - that is what the vet will ask you.",
)
UNKNOWN_IF_THEY_STILL_CAN = (
    "Nobody here can judge that from a line, and I would not guess at it. Their GP, or whoever "
    "sees them day to day, will tell you straight, and it is easier to raise as a worry than as a "
    "verdict. Has anything already gone wrong?",
    "That is not mine to decide, and it is not a thing to guess at either. Ask their doctor, or "
    "get an eye test done if it is about the driving; that settles it more often than people "
    "expect. What made you wonder?",
    "I cannot say, and I would not want to. The person who can judge it is the one who can see "
    "them do it. Would they take it from you if you raised it?",
)


def _somebody_to_visit(clean, turns, look_back=3):
    people = THE_PEOPLE | VISIT_PRONOUNS
    if set(re.findall(r"[a-z']+", clean)) & people:
        return True
    for turn in turns[-look_back:]:
        said = str(turn.get("user") or "").lower()
        if set(re.findall(r"[a-z']+", said)) & people:
            return True
    return False


def _someone_is_a_patient(clean, turns, look_back=4):
    if IN_HOSPITAL.search(clean):
        return True
    for turn in turns[-look_back:]:
        if IN_HOSPITAL.search(str(turn.get("user") or "").lower()):
            return True
    return False


AN_ANIMAL_DID_IT = re.compile(
    r"\b(?:bit|bitten|bites|scratch(?:ed|es)?|kicked|trampled|stung|attacked|mauled|nipped|"
    r"gouged|pinned|knocked|went for|lashed out at)\s+(?:me|us|my|our)\b",
    re.I)
AN_ANIMAL_DID_IT_TO_ANYONE = re.compile(
    r"\b(?:bit|bitten|bites|scratch(?:ed|es)?|nipped|attacked|mauled|stung|kicked)\s+by\s+"
    r"(?:a|an|the|my|our|their|his|her|some)\s+(?:dog|dogs|cat|cats|puppy|pup|kitten|rabbit|"
    r"hamster|budgie|parrot|horse|pony|fox|rat|mouse|snake|spider|wasp|bee|animal|pet)\b",
    re.I)
A_PERSON_ELSE_IS_HURT = re.compile(
    r"\b(?:my|our|the|his|her|their)\s+(?:daughter|son|child|children|kid|kids|baby|wife|"
    r"husband|partner|boyfriend|girlfriend|mum|mother|dad|father|sister|brother|friend|"
    r"neighbour|neighbor|grandson|granddaughter|grandchild|niece|nephew)\b[^.]{0,60}\b"
    r"(?:bit|bitten|bites|scratch(?:ed|es)?|nipped|attacked|mauled|stung|kicked|swollen|"
    r"bleeding|bled)\b",
    re.I)
A_PERSONS_TREATMENT = re.compile(
    r"\b(?:tetanus|rabies|jab|jabs|shot|shots|stitches|stitched|a&e|a and e|casualty|"
    r"minor injuries|triage|antiseptic|antibiotics?|wound|dressing|bandage)\b",
    re.I)
A_BODY_PART = (
    r"(?:hand|hands|arm|arms|finger|fingers|thumb|thumbs|wrist|wrists|leg|legs|foot|feet|toe|toes|"
    r"head|nose|face|mouth|lip|lips|eye|eyes|ear|ears|knee|knees|shoulder|shoulders|back|side|"
    r"chest|stomach|ankle|ankles|heel|heels|shin|thigh|elbow|skin|neck|jaw|tooth|teeth|gum|gums|"
    r"nail|nails|cut|cuts|wound|wounds|bite|scar|knuckle|knuckles|palm|fist|forehead|cheek)")
A_PERSON_IS_BLEEDING = re.compile(
    r"\b(?:i|im|i'm|ive|i've|we|we're|weve|we've)\s+(?:am\s+|was\s+|are\s+|were\s+|"
    r"keep\s+|keeps\s+|still\s+|been\s+)?(?:bleeding|bled)\b|"
    r"\b(?:i|im|i'm|ive|i've|we|we're)\s+(?:still\s+|also\s+)?(?:hurting|in pain|sore)\b|"
    r"\bmy\s+" + A_BODY_PART + r"\b[^.]{0,30}?\b(?:bleeding|bled|hurts?|hurting|sore|"
    r"swollen|limp|infected|throbbing|bruised|broken|stings?|burning)\b",
    re.I)


AN_A_HARM_VERB = re.compile(
    r"\b(?:bit|bites|bitten|scratch|scratches|scratched|sting|stings|stung|kicked|attacks?|"
    r"attacked|mauled|nipped|gouged|trampled|lashed out at|went for|snapped at)\b",
    re.I)
AN_ANIMAL_WORD = re.compile(r"\b(?:" + "|".join(sorted(ANIMALS)) + r")\b", re.I)


def _the_animal_is_the_patient(said):
    text = str(said or "").lower()
    animals = [m.start() for m in AN_ANIMAL_WORD.finditer(text)]
    if not animals:
        return False
    if AN_ANIMAL_DID_IT.search(text):
        return False
    verb = AN_A_HARM_VERB.search(text)
    if verb is None or min(animals) > verb.start():
        return False
    tail = set(re.findall(r"[a-z']+", text[verb.end():]))
    return not (tail & (THE_PEOPLE - ANIMALS))


def _the_person_is_the_patient(said):
    text = str(said or "")
    if not text or _the_animal_is_the_patient(text):
        return False
    return bool(AN_ANIMAL_DID_IT.search(text)
                or AN_ANIMAL_DID_IT_TO_ANYONE.search(text)
                or A_PERSON_ELSE_IS_HURT.search(text)
                or A_PERSONS_TREATMENT.search(text)
                or A_PERSON_IS_BLEEDING.search(text))


def _the_thread_is_an_animal(clean, turns, look_back=4):
    said = str(clean or "").lower()
    recent = [str(turn.get("user") or "").lower() for turn in turns[-look_back:]]
    if _the_person_is_the_patient(said) or any(_the_person_is_the_patient(x) for x in recent):
        return False
    if set(re.findall(r"[a-z']+", said)) & NOT_PEOPLE_WORDS:
        return True
    return any(set(re.findall(r"[a-z']+", x)) & NOT_PEOPLE_WORDS for x in recent)


def _thread_is_about_someone_else(memory, look_back=3):
    turns = [t for t in ((memory or {}).get("turns") or []) if isinstance(t, dict)]
    for turn in turns[-look_back:]:
        said = str(turn.get("user") or "").lower()
        words = {w[:-2] if w.endswith("'s") else w for w in re.findall(r"[a-z']+", said)}
        if (words & trouble.OTHERS) - NOT_PEOPLE_WORDS:
            return True
    return False


def _thread_is_about_a_pet(memory, look_back=3):
    turns = [t for t in ((memory or {}).get("turns") or []) if isinstance(t, dict)]
    for turn in reversed(turns[-look_back:]):
        said = str(turn.get("user") or "").lower()
        words = {w[:-2] if w.endswith("'s") else w for w in re.findall(r"[a-z']+", said)}
        animals = words & ANIMALS
        if not animals:
            if _the_speaker_is_the_subject(said):
                return False
            continue
        if animals <= WILD_BIRDS and words & MESS_PLACES:
            continue
        if loss.reads_as_loss(said) or badnews.reads_as_sudden_loss(said):
            return False
        return True
    return False


ASKED_ABOUT = re.compile(
    r"(?:he|she|they|(?:my|our|his|her|their)\s+(?:poor\s+|old\s+|little\s+|eldest\s+)?"
    r"(?:mum|mom|mother|dad|father|son|daughter|husband|wife|partner|boyfriend|girlfriend|"
    r"sister|brother|nan|nana|gran|granny|grandma|grandad|grandpa|baby|kid|kids|child|children|"
    r"friend|mate|neighbour|neighbor|aunt|uncle|cousin|little one|lad|lass|boy|girl|"
    r"dog|cat|puppy|kitten|pup|rabbit|hamster|horse|budgie|parrot|fish|pet))")
WHETHER_IT_GOES_WELL = re.compile(
    r"\b(?:is|are|was|were|will|would)\s+" + ASKED_ABOUT.pattern
    + r"\b\s+(?:going\s+to|gonna)\s+be\b"
    r"|\b(?:is|are|was|were)\s+" + ASKED_ABOUT.pattern
    + r"\b\s+(?:ok|okay|alright|all\s+right|fine|safe)\b"
    r"|\b(?:will|would)\s+" + ASKED_ABOUT.pattern
    + r"\b\s+be\s+(?:ok|okay|alright|all\s+right|fine|safe)\b"
    r"|\b(?:will|would)\s+" + ASKED_ABOUT.pattern
    + r"\b\s+(?:ever\s+)?(?:pull\s+through|make\s+it|get\s+better|get\s+worse|recover|"
    r"walk\s+again|come\s+round|beat\s+it|"
    r"be\s+(?:himself|herself|themselves|back\s+to\s+(?:normal|herself|himself|themselves)))\b"
    r"|\b(?:is|are|was)\s+" + ASKED_ABOUT.pattern
    + r"\b[^.?!]{0,25}\b(?:at\s+risk|in\s+danger)\b"
    r"|\bhow\s+long\s+(?:is|are|will|does|do|has|have)\s+" + ASKED_ABOUT.pattern + r"\b")
WHETHER_THEY_CAN_STILL = re.compile(
    r"\bshould\s+" + ASKED_ABOUT.pattern + r"\b\s+still\b"
    r"|\bshould\s+" + ASKED_ABOUT.pattern
    + r"\b\s+be\s+(?:driving|working|living\s+alone|left\s+alone|on\s+(?:his|her|their)\s+own)"
    r"|\bis\s+" + ASKED_ABOUT.pattern
    + r"\b\s+(?:still\s+)?(?:ok|safe|alright)\s+to\s+(?:drive|live|work)\b")
WHETHER_IT_GOES_WELL_ITSELF = re.compile(
    r"\b(?:is|was|will)\s+(?:it|this|that)\s+(?:going\s+to\s+be\s+|be\s+)?"
    r"(?:ok|okay|alright|all\s+right|fine|serious|bad|treatable|curable|terminal)\b"
    r"|\bhow\s+(?:bad|serious)\s+(?:will\s+(?:it|this|that)\s+get|is\s+(?:it|this|that))\b"
    r"|\bhow\s+long\s+(?:is|will)\s+the\s+recovery\b")
WHETHER_IT_LONGER_HAS_GOT = re.compile(
    r"\bhow\s+much\s+longer\s+(?:has|have|does|do)\s+" + ASKED_ABOUT.pattern + r"\b"
    r"|\bhow\s+long\s+(?:has|have)\s+" + ASKED_ABOUT.pattern + r"\b\s+(?:got|left)\b")
AN_ILLNESS = re.compile(
    r"\b(?:cancer|tumou?r|disease|illness|condition|infection|dementia|alzheimers?|"
    r"leuk[ae]mia|leuka?emia|arthritis|diabetes|epilepsy|lupus|ms|covid|long\s+covid|flu|"
    r"pneumonia|chemo|dialysis|transplant|bypass|operation|surgery|procedure|stroke|aneurysm|sepsis|"
    r"heart\s+failure|kidney\s+failure|liver\s+failure|ulcer|colitis|crohns?|asthma|"
    r"depression|anorexia|bulimia|eating\s+disorder|addiction|withdrawal)\b")
A_PET_IN_TROUBLE = re.compile(
    r"\b(?:vet|vets|sick|ill|illness|disease|diagnosed|condition|hurt|hurts|injured|injury|"
    r"poison|poisoned|ate|eaten|drank|drunk|swallowed|choking|choked|limp|limping|bleeding|"
    r"bled|cut|wound|wobbly|unsteady|seizure|fit|fits|surgery|operation|collapsed|"
    r"not\s+eating|stopped\s+eating|off\s+(?:his|her|its|their)\s+food|worse)\b")
WHETHER_IT_IS_THEIR_AGE = re.compile(
    r"\b(?:is|was)\s+(?:that|this|it)\s+(?:just|normal|normal\s+for|ordinary)\b[^.?!]{0,30}"
    r"\b(?:age|her\s+age|his\s+age|them|him|her)\b")
_MY_PEOPLE = frozenset(w.rstrip("s") for w in """
    mum mom mother dad father son daughter husband wife partner boyfriend girlfriend sister
    brother nan nana gran granny grandma grandad grandpa baby kid child children friend mate
    neighbour neighbor aunt uncle cousin lad lass boy girl parent ex family stepson stepdaughter
    nephew niece grandson granddaughter sibling twin stepmum stepdad stepmother stepfather
    mother-in-law father-in-law son-in-law daughter-in-law sister-in-law brother-in-law
    godson goddaughter grandparent in-laws
""".split())
A_PATIENT_STATE = re.compile(r"\b(?:hospital|pregnant|operation|surgery|diagnosed|chemo|"
                             r"ward|intensive\s+care|in\s+a\s+coma|on\s+a\s+drip)\b")
A_HARD_TIME = re.compile(
    r"\b(?:(?:hard|rough|bad|tough|difficult|dreadful|awful)\s+(?:time|times|week|weeks|month|"
    r"months|year|years|patch|spell|stretch|ride|few(?:\s+\w+)?|long(?:\s+\w+)?)\b|"
    r"struggling|struggles|struggled|having\s+a\s+go\s+of\s+it|feeling\s+low|feels\s+low|"
    r"down\s+in\s+the\s+dumps|grieving|grief|bereavement|lonely|loneliness|stressed|stress|"
    r"overwhelmed|burnout|burnt\s+out|burned\s+out|worried\s+sick|money\s+trouble|"
    r"out\s+of\s+work|lost\s+(?:his|her|their)\s+job|divorce|divorcing|split\s+up|"
    r"separation|argument|arguing|falling\s+out|fell\s+out|lonely)\b")
A_MEDICAL_THREAD = re.compile(
    r"\b(?:hospital|hospice|pregnant|operation|operations|op|ops|surgery|surgeon|surgeons|"
    r"diagnosed|diagnosis|chemo|chemotherapy|radiotherapy|treatment|treating|being\s+treated|"
    r"ward|intensive\s+care|high\s+dependency|in\s+a\s+coma|on\s+a\s+drip|anaesthetic|"
    r"anaesthetist|theatre|consultant|specialist|biopsy|transplant|dialys\w+|"
    r"results?(?!\s+day)\b|"
    r"accident|accidents|crash|crashed|ambulance|casualty|a\s+and\s+e|ae|"
    r"broke|broken|fractur\w+|scald\w*|stitches|collapsed|fainted|"
    r"seizure|seizures|convulsion\w*|concussion|injured|injury|injuries|whiplash)\b"
    r"|\b(?:fell|fallen|burn|burns|burned|burnt)(?!\s+out)\b")


def _the_thread_said(memory, look_back=3):
    turns = [t for t in ((memory or {}).get("turns") or []) if isinstance(t, dict)]
    return " ".join(str(turn.get("user") or "").lower() for turn in turns[-look_back:])


def _a_person_in_the_thread(memory, look_back=3):
    turns = [t for t in ((memory or {}).get("turns") or []) if isinstance(t, dict)]
    for turn in turns[-look_back:]:
        said = str(turn.get("user") or "").lower()
        words = {w[:-2] if w.endswith("'s") else w for w in re.findall(r"[a-z']+", said)}
        if {w.rstrip("s") for w in words} & _MY_PEOPLE or A_PATIENT_STATE.search(said):
            return True
    return False


def _a_hard_time_and_not_a_body(memory, line=""):
    said = _the_thread_said(memory) + " " + str(line or "")
    if A_MEDICAL_THREAD.search(said) or AN_ILLNESS.search(said):
        return False
    return bool(A_HARD_TIME.search(_the_thread_said(memory)))


def _a_pet_in_trouble(line, memory):
    if not _thread_is_about_a_pet(memory) or _a_person_in_the_thread(memory, look_back=2):
        return False
    said = _the_thread_said(memory)
    return bool(A_PET_IN_TROUBLE.search(line) or A_PET_IN_TROUBLE.search(said)
                or A_HARD_TIME.search(said))


def _the_pool_for_a_worry_about_them(clean, memory):
    line = re.sub(r"[^a-z0-9' ]", " ", str(clean or "").lower())
    if an_outcome_asked_about_someone(clean, memory) or the_threads_answer(clean, memory):
        return None
    still = WHETHER_THEY_CAN_STILL.search(line)
    itself = WHETHER_IT_GOES_WELL_ITSELF.search(line) or WHETHER_IT_LONGER_HAS_GOT.search(line)
    if itself:
        if _a_pet_in_trouble(line, memory):
            return UNKNOWN_HOW_IT_GOES_FOR_A_PET
        if not _a_person_in_the_thread(memory):
            return None
        if not (WHETHER_IT_LONGER_HAS_GOT.search(line)
                or AN_ILLNESS.search(_the_thread_said(memory))):
            return None
    if not (still or itself or WHETHER_IT_GOES_WELL.search(line)
            or WHETHER_IT_IS_THEIR_AGE.search(line)):
        return None
    subject = ASKED_ABOUT.search(line)
    named = subject.group(0) if subject else ""
    if set(named.split()) & (ANIMALS | NOT_PEOPLE_WORDS):
        return UNKNOWN_HOW_IT_GOES_FOR_A_PET
    if not named or re.match(r"(?:he|she|they)\b", named):
        if _a_pet_in_trouble(line, memory):
            return UNKNOWN_HOW_IT_GOES_FOR_A_PET
        if not _a_person_in_the_thread(memory):
            return None
    if still:
        return UNKNOWN_IF_THEY_STILL_CAN
    if _a_hard_time_and_not_a_body(memory, line):
        return UNKNOWN_HOW_IT_GOES_FOR_A_HARD_TIME
    if _someone_is_a_patient(line, memory.get("turns") or []):
        return UNKNOWN_HOW_LONG_IN_HOSPITAL
    return UNKNOWN_HOW_IT_GOES_FOR_SOMEONE


SELF_WORDS = frozenset("i me my myself im ive id i'm i've".split())
THEIR_OWN_STATE = re.compile(
    r"\bi\s+(?:keep|still|just)\s+(?:feeling|feel|thinking|worrying|crying)\b"
    r"|\bi\s*'?m\s+(?:feeling|worried|scared|anxious|sad|low|exhausted|knackered)\b"
    r"|\bi\s+feel\s+(?:odd|weird|strange|awful|terrible|anxious|worried|sad|low|numb|empty)\b"
    r"|\bi\s+cant\s+(?:stop|sleep|eat|shake|cope)\b"
    r"|\bi\s+havent\s+(?:slept|eaten|coped)\b")


def _the_speaker_is_the_subject(said):
    return bool(THEIR_OWN_STATE.search(str(said or "")))


def _a_thing_they_started(memory, look_back=3):
    turns = [t for t in ((memory or {}).get("turns") or []) if isinstance(t, dict)]
    for turn in turns[-look_back:]:
        if TAKING_UP.search(str(turn.get("user") or "").lower()):
            return True
    return False


def _names_their_age(clean):
    return bool(re.search(r"\b\d{1,2}\b", clean)
                or _AGE_DOUBT.search(clean))


def _reads_as_worry(clean, words=()):
    words = words or clean.split()
    if _worry_is_about_the_body(clean, words):
        return False
    if WORRY_SELF.search(clean):
        return True
    return bool(SHOULD_WORRY.search(clean)) and _a_bare_worry(clean)


def _the_weird_ask_pool(clean, memory):
    found = WEIRD_ASK.search(clean)
    if not found:
        return None
    memory = memory if isinstance(memory, dict) else {}
    if _worry_is_about_the_body(clean, clean.split()) or _thread_is_about_the_body(memory):
        return None
    if FEELING_SAID.search(clean) or FEELING_SAID.search(_the_line_before(memory)):
        return UNKNOWN_WORRY
    if not _the_line_before(memory) and _nothing_but_the_ask(clean, found):
        return UNKNOWN_WEIRD_BARE
    return None


def _nothing_but_the_ask(clean, found):
    rest = clean[:found.start()] + " " + clean[found.end():]
    return not re.sub(r"[^a-z0-9]", "", SHOULD_WORRY_FILLER.sub(" ", rest))


def _without_the_idioms(said):
    words = re.findall(r"[a-z']+", said)
    if not words:
        return set()
    taken = set()
    for phrase in IDIOM_PHRASES:
        size = len(phrase)
        for at in range(len(words) - size + 1):
            if tuple(words[at:at + size]) == phrase:
                taken.update(range(at, at + size))
    return {word for at, word in enumerate(words) if at not in taken}


def _thread_is_about_the_body(memory, look_back=4):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    for turn in turns[-look_back:]:
        said = (turn.get("user") or "").lower()
        if not said:
            continue
        said = _without_the_things_named_after_a_body(_without_the_forecast_verb(said))
        words = _without_the_idioms(said)
        if words & SYMPTOM_WORDS or words & BODY_PARTS or words & HEALTH_WORDS:
            return True
    return False


def _the_threads_who(memory, look_back=2):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    for turn in reversed(turns[-look_back:]):
        said = " " + re.sub(r"[^a-z0-9']", " ", (turn.get("user") or "").lower()) + " "
        words = said.replace("'", "").split()
        if not words:
            continue
        who = _who_for(said.strip(), said, words, None)
        if who and who != HEALTH_WHO:
            return who
    return None


_LEANS_ON_THE_THREAD = re.compile(r"\b(?:it|its|that|thats|this|they|them|those|these)\b")
_BODY_TOPICS = (None, "", "health", "fitness", "sleep")


def the_threads_answer(text, memory):
    clean = " ".join(str(text or "").split())
    if not clean or _hedged_recently(memory):
        return None
    try:
        understood = understand(clean, memory)
    except Exception:
        understood = {}
    if not _the_ask_is_the_threads(clean, understood):
        return None
    who = _the_threads_who(memory)
    if who:
        return _choose([line.format(who=who) for line in UNKNOWN_WHO], memory, clean)
    leans = (understood.get("leans_on") or {}).get("topic")
    if leans == "health" or _thread_is_about_the_body(memory, look_back=1):
        return _choose(UNKNOWN_HEALTH, memory, clean)
    return None


_THREAD_MACHINES = frozenset("""
bike bicycle cycle chain chains gears gear derailleur boiler car van motorbike scooter washer
machine dryer dryers dishwasher fridge freezer oven cooker hob kettle toaster microwave hoover vacuum
mower lawnmower laptop phone tablet computer pc printer tv television stereo speaker speakers
headphones watch clock camera drill saw gate door window shed roof gutter tap shower radiator
pump fan fridge washing
""".split())


def _thread_names_a_machine(memory, look_back=4):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    for turn in reversed(turns[-look_back:]):
        tokens = re.findall(r"[a-z']+", (turn.get("user") or "").lower())
        machine_at = [i for i, word in enumerate(tokens) if word in _THREAD_MACHINES]
        if not machine_at:
            if set(tokens) & (BODY_PARTS | SYMPTOM_WORDS | HEALTH_WORDS):
                return False
            continue
        body_at = [i for i, word in enumerate(tokens)
                   if word in BODY_PARTS or word in SYMPTOM_WORDS or word in HEALTH_WORDS]
        if all(any(abs(i - j) == 1 for j in machine_at) for i in body_at):
            return True
    return False


_A_CANDIDATE_OF_ITS_OWN = re.compile(
    r"\b(?:it|its|it['\u2019]s|this|that|these|those|they)\b[^.?!,;]{0,24}?"
    r"\b(?:my|our|his|her|their)\s+[a-z]")


def _the_ask_is_the_threads(clean, understood):
    if not (ASK_SHAPE.search(clean) and _LEANS_ON_THE_THREAD.search(clean)):
        return False
    if _A_CANDIDATE_OF_ITS_OWN.search(clean.lower()):
        return False
    return (understood or {}).get("topic") in _BODY_TOPICS


def _thread_is_about_a_person(memory, look_back=4):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    for turn in turns[-look_back:]:
        words = set(re.findall(r"[a-z']+", (turn.get("user") or "").lower()))
        if words & _THREAD_PEOPLE or REPAIR_PERSON.search(turn.get("user") or ""):
            return True
    return False


def _a_thing_was_named(memory, look_back=4):
    from ..understanding import understand

    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)][-look_back:]
    for turn in turns:
        said = str(turn.get("user") or "")
        if not said.strip():
            continue
        for entity in understand(said).get("entities") or []:
            if str(entity.get("type")) == "thing":
                return True
    return False

def _names_its_own_thing(clean):
    match = REPAIR_DECISION.search(clean)
    if not match:
        return False
    for word in re.findall(r"[a-z']+", clean[match.end():]):
        if word in _NOT_AN_OWN_THING:
            continue
        if word in BODY_PARTS or word in HEALTH_WORDS or word in SYMPTOM_WORDS:
            continue
        if REPAIR_PERSON.search(word):
            continue
        return True
    return False

def _money_decision(clean):
    said = set(re.findall(r"[a-z']+", clean))
    if not said & MONEY_WORDS and not _PAY_DEBT.search(clean) and not _CARD_MONEY.search(clean):
        return False
    if _VALUE_OF_THING.search(clean) and not said & _MONEY_NOUN:
        return False
    return True


def _about_a_sore(clean, words):
    if not SORE_DOING.search(clean):
        return False
    named = set(words) & SORE_WORDS
    if not named:
        return False
    if named - SORE_AMBIGUOUS:
        return True
    if not SORE_PICKING.search(clean) or SORE_ONLY_A_BODY.search(clean):
        return True
    return bool(SORE_PLACE.search(clean))


def _a_call_for_help(clean):
    if not _ASKS_TO_ACT.search(clean):
        return None
    if _A_PLACE_TO_BE_SEEN.search(clean) and not _A_CALL_WORD.search(clean):
        if DANGER_SYMPTOM.search(clean):
            return RING_FOR_HELP
        if MINOR_HARM.search(clean):
            return None
        return GO_TO_BE_SEEN
    if EMERGENCY_CALL.search(clean):
        if MINOR_HARM.search(clean) and not DANGER_SYMPTOM.search(clean):
            return None
        return RING_FOR_HELP
    if POLICE_CALL.search(clean) and (REACHING_THE_POLICE.search(clean)
                                     or _ASKING_FOR_THE_POLICE.search(clean)
                                     or SOMETHING_HAPPENING.search(clean)):
        return RING_THE_POLICE
    return None


REPAIR_HOW = re.compile(
    r"\bhow (?:do|can|could|should|would) (?:i|we)\b[^.?!]{0,40}?"
    r"(?:\bmake (?:it|things|this) (?:right|up)\b|\bmake up for\b|"
    r"\bput (?:it|things|this) right\b|\bsay sorry\b|\bapolog\w*|\bforgive me\b|"
    r"\bclear the air\b)")
REPAIR_ANSWER = (
    "Name the one thing you did, say sorry for it in a sentence, then ask what would help. Short "
    "and about them is what makes it land, and the explaining can come later if they want it.",
    "Do it soon, in person if you can. Say what you did rather than why you did it, and leave "
    "what they did out of it - that is the part that turns an apology into an argument.",
    "One sentence of sorry, then a question: what would make it easier? Most people would rather "
    "be asked than be given a longer apology.",
)


def _a_small_social_decide(clean, words):
    if ASKED_OUT.search(clean):
        return ASK_OUT_ANSWER
    if AN_APOLOGY.search(clean):
        return APOLOGY_ANSWER
    said = set(words)
    if _CONTACT.search(clean) and said & _A_PERSON:
        if _CALLING.search(clean):
            return CALL_ANSWER
        return CONTACT_ANSWER
    if said & _A_SOCIAL_THING and _GOING.search(clean) and not _NOT_INVITED.search(clean):
        return GO_ANSWER
    return None


METHOD_OPENING = re.compile(r"^(?:so |ok |okay |and |but )?"
                            r"(?:how|where) (?:do|does|should|shall|can|could|would|might) i\b")
HOW_TO_TELL = re.compile(r"\b(?:know|tell|check|find\s+out) "
                         r"(?:if|whether|the|a|an|my|your|his|her|its|it's|that|this|which|"
                         r"apart|the\s+difference)\b")
_A_PRODUCT = _THREAD_MACHINES | frozenset(
    "router wifi broadband windows android iphone ipad ios mac app apps settings browser email "
    "excel word powerpoint gmail outlook instagram facebook whatsapp tiktok password account".split())
_A_PRODUCT = _A_PRODUCT - frozenset(("washing",))
NOT_A_METHOD = re.compile(
    r"^(?:so |ok |okay |and |but )?(?:how|where) (?:do|does|should|shall|can|could|would|might) "
    r"i (?:get|find|buy|hire|rent|book|order|locate|pick\s+up|put|keep|store)\b"
    r"(?!\s+(?:up|better|going|started|through|on|out|round|back|dressed|ready|organised|there|"
    r"in|to)\b)"
    r"|\b(?:round here|near me|nearby|in my area|locally)\b"
    r"|\b(?:you|your|yourself)\b")


def method_ask_pool(clean, memory=None):
    if not METHOD_OPENING.match(str(clean or "")):
        return None
    if HOW_TO_TELL.search(clean) or NOT_A_METHOD.search(clean):
        return None
    if set(re.findall(r"[a-z']+", str(clean or ""))) & _A_PRODUCT:
        return None
    if _DEFINITION.search(clean):
        return None
    if _answered_already(memory if isinstance(memory, dict) else {}):
        return HELP_ALREADY
    return TIPS_LINES


def unknown_pool(clean, words=()):
    words = words or clean.split()
    if HANDS_IT_BACK.match(clean):
        return HANDS_BACK
    calling = _a_call_for_help(clean)
    if calling:
        return calling
    if REPAIR_HOW.search(clean) and set(words) & _A_PERSON:
        return REPAIR_ANSWER
    if _reads_as_worry(clean, words):
        return UNKNOWN_WORRY
    if _about_a_sore(clean, words):
        if set(words) & SORE_SERIOUS:
            return UNKNOWN_HEALTH
        return SORE_HANDS
    if PLASTER_ON.search(clean):
        return PLASTER_IT
    if any(phrase in clean for phrase in WORD_ANYWHERE) and not (_CREATIVE & set(words)):
        return UNKNOWN_WORD
    if not _DEFINITION.search(clean) and _an_order_of_work(_choice_sides(clean), clean):
        return ORDER_OF_WORK
    if ((DECIDE_OPENING.search(clean) or DECIDE_SANITY.search(clean))
            and not _DEFINITION.search(clean)):
        if (set(words) & (HEALTH_WORDS | SORE_SERIOUS)
                or any(phrase in clean for phrase in CHECK_PHRASES)):
            return UNKNOWN_HEALTH
        if _money_decision(clean):
            return UNKNOWN_MONEY
        social = _a_small_social_decide(clean, words)
        if social:
            return social
        return UNKNOWN_DECIDE
    return UNKNOWN


FOOD_TOPICS = frozenset(("cooking", "food-and-drink"))
OVERDOSE_FOOD = re.compile(
    r"\boverdos(?:e|ed|ing)\b[^.!?]{0,12}\b(?:on|of|with)\s+(?:the\s+|a\s+|some\s+)?"
    r"(?:cake|cakes|chocolate|sweets|candy|biscuits?|cookies|crisps|chips|chinese|curry|pizza|"
    r"ice\s*cream|cheese|coffee|tea|netflix|tv|telly|sugar|bread|"
    r"pastr(?:y|ies)|do(?:ugh)?nuts|burgers?|takeaways?|naps|love|pies?|pudding|trifle|"
    r"turkey|roast|stuffing|mince|gravy|easter\s+eggs?)\b")
OVERDOSE_DRUG = re.compile(
    r"\b(?:pills?|tablets?|paracetamol|ibuprofen|painkillers?|meds|medicines?|"
    r"sleeping\s+pills?|antidepressants?|insulin|heroin|heroine|cocaine|methadone|tramadol|"
    r"codeine|morphine|opioid|opiates?|drugs?|liquid|bottle|packet|pack|box|strip|blister|"
    r"alcohol|vodka|whisky|whiskey|wine|beer|gin|rum|brandy|tequila|lager|cider|champagne|"
    r"prosecco|ros\u00e9|spirits?|drink|drinking|booze)\b")
UNRESPONSIVE_TAIL = re.compile(r"\bunresponsive\b\s*(?:to|when|whenever|if|because|as|after|"
                              r"with|about|on)\b")
FEED_TAIL = re.compile(
    r"\bunresponsive\b\s*(?:to|after|during|at|following)\s+(?:the|a|an|her|his|my|their|this|"
    r"that|some)?\s*(?:(?:new|old)\s+)?(?:milk|formula|feeds?|feeding|bottle|breast|solids|"
    r"weaning)\b")


def _the_thing_is_choking(clean, words):
    if not any(phrase in clean for phrase in THING_STATES):
        return False
    if set(words) & BODY_SUBJECT:
        return False
    tokens = clean.replace("'", "").split()
    for i, word in enumerate(tokens):
        if word != "choking":
            continue
        before = tokens[max(0, i - 4):i]
        while before and before[-1] in _COPULA:
            before.pop()
        if before and before[-1] in THING_SUBJECT:
            return True
    return False


CANT_WAKE = re.compile(r"\b(?:can ?t|cannot|could ?nt)\s+(?:wake|rouse)\s+(?:him|her|them|my|"
                       r"the (?:baby|child|kid|boy|girl|man|woman|old man|old woman))\b")
ROUTINE_WAKE = re.compile(
    r"\b(?:for|to|before|in time for|on time for) (?:work|school|college|uni|university|nursery|"
    r"childminder|the gym|his work|her work|their work|the (?:school )?(?:bus|train)|"
    r"(?:his|her|their|my|an|a) (?:exam|exams|test|appointment|meeting|interview|flight|"
    r"lesson|lecture|class|early start)|"
    r"(?:his|her|their|my|the|an|a) (?:early|late|night|day|double|morning|afternoon|evening)?\s*"
    r"shift(?:\s+(?:at|on|tomorrow|today|in)\b[^.]{0,25})?)\b|"
    r"\bto get (?:to|ready for) (?:school|work|college|uni|university|nursery)\b|"
    r"\bin the mornings?\b|"
    r"\bevery (?:morning|monday|tuesday|wednesday|thursday|friday|saturday|sunday|day|week)\b|"
    r"\bon (?:school )?(?:days|weekdays|mondays?|weekday mornings?)\b")
CHOKE_ON_A_WORD = re.compile(
    r"\bchok(?:e|ed|es|ing)?\s+on\s+(?:(?:my|his|her|their|your|our|the|a|an)\s+)?(?:own\s+)?"
    r"(?:words?|sentences?|speech|lines?|names?|syllables?|pronunciation)\b")
OVERDOSE_OF_A_TREAT = re.compile(
    r"\boverdos(?:e|ed|ing)\s+(?:on\s+)?(?:(?:the|a|an|my|his|her|their)\s+)?"
    r"(?:coffee|caffeine|tea|chocolate|cake|sugar|sweets|crisps|biscuits|cheese|ice\s+cream|"
    r"tv|telly|netflix|box\s+sets?|sleep|sun|sunshine|shopping|gossip|christmas\s+music|"
    r"work|meetings?|emails?|paperwork|spreadsheets?)\b"
    r"|\ban\s+overdose\s+of\s+(?:coffee|caffeine|tea|chocolate|cake|sugar|sweets|tv|telly|"
    r"netflix|box\s+sets?|sleep|sun|sunshine|shopping|gossip|work|meetings?|emails?|paperwork|"
    r"spreadsheets?|christmas\s+music)\b")
OVERDOSE_A_PILL = re.compile(
    r"\b(?:pills?|tablets?|paracetamol|ibuprofen|insulin|meds|medicines?|bleach|antifreeze|"
    r"heroin|opioids?|tramadol|antidepressants?)\b")
FAINT_COMING = re.compile(
    r"\b(?:about|going|gonna)\s+to\s+(?:pass\s+out|faint|black\s+out|collapse|go\s+down)\b"
    r"|\b(?:feel|feels|feeling|felt|think|thinking|look|looking)\s+(?:like\s+)?"
    r"(?:im|i'm|he|she|they)\s+(?:going|gonna|about)\s+to\s+"
    r"(?:pass\s+out|faint|black\s+out|collapse)\b"
    r"|\bnearly\s+(?:passed\s+out|fainted|blacked\s+out)\b"
    r"|\bmight\s+(?:pass\s+out|faint|black\s+out|collapse)\b"
    r"|\b(?:going|gonna)\s+(?:down|faint)\b")

BLACKED_OUT_A_THING = re.compile(
    r"\bblack(?:ed|ing)\s+out\b\s+(?:the|a|an|my|our|his|her|their|all\s+the)\s+"
    r"(?:\w+\s+){0,2}(?:window|windows|room|rooms|light|lights|sun|view|glass|door|doors)\b")
BLACKOUT_PERSON = re.compile(
    r"\b(?:i|im|id|ive|me|my|myself|he|hes|she|shes|they|we|us|him|her|his|their|our)\b")

CHOKE_MACHINE = re.compile(
    r"\b(?:kitchen\s+sink|sinks?|drain\w*|pipes?|toilet|loo|gutter\w*|chimney|radiator|filter|"
    r"engines?|car|van|motorbike|mower|lawnmower|hoover|vacuum|dishwasher|printer|traffic|"
    r"weeds?|lawn|flowerbed\w*|bog|moss|inbox|budget|schedule|calendar|tears?)\b"
    r".{0,30}\bchok\w*\b"
    r"|\bchok\w*\b.{0,30}\b(?:on|with)\s+(?:fuel|petrol|diesel|weeds|leaves|moss|traffic|hair|"
    r"paper|dust|fat)\b")
CHOKE_BODY = re.compile(
    r"\b(?:he|she|they|them|him|me|us|i|his|her|their|mum|mom|mother|dad|father|son|daughter|"
    r"husband|wife|partner|brother|sister|friend|baby|child|kid|boy|girl|man|woman|gran|granny|"
    r"nan|grandad|grandma|grandpa|toddler|newborn|infant|mate|neighbou?r)\b")

TAG_CAN = re.compile(r"\bcan\b")
BARE_FOLLOW_UP = re.compile(
    r"^(?:and |so |but |ok |okay |right |also |well )*"
    r"(?:is|was|are|were|will|would|does|do|did|can|could|should|has|have|had)"
    r" (?:that|this|it|they|those|these|there)"
    r"(?: (?:stop|help|work|matter|count|last|clear|ease|go|mean|hurt|pass|settle|fade|fix"
    r"|sort|change|show|be|get|keep|stay|take|worsen|spread|why|how|where)"
    r"(?: (?:up|off|away|out|long|better|worse|anything|enough|now|soon|all|of|it|then|again)){0,2})?"
    r"[?.!]*$")
def _the_line_before(memory):
    if not isinstance(memory, dict):
        return ""
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    return str(turns[-1].get("user") or "") if turns else ""


def _reads_as_heavy_news(text):
    said = (text or "").lower()
    return bool(said) and bool(loss.reads_as_loss(said)
                               or reads_as_bad_news(said)
                               or badnews.reads_as_sudden_loss(said))


def _the_thread_is_heavy(memory):
    return _reads_as_heavy_news(_the_line_before(memory))

SWITCH_OFF_ASK = re.compile(
    r"\b(?:should|shall|do)\s+i\s+(?:just\s+|really\s+|now\s+)?"
    r"(?:(?:turn|switch|shut|power|cut)\s+(?:it|that|this|them|those)\s+off"
    r"|(?:unplug|disconnect|isolate)\s+(?:it|that|this|them|those)"
    r"|stop\s+(?:using|running)\s+(?:it|that|this)"
    r"|take\s+the\s+battery\s+out"
    r"|switch\s+(?:it|that|this)\s+off\s+at\s+the\s+wall)")
SWITCH_OFF_THINGS = frozenset((
    "boiler", "boilers", "heating", "radiator", "radiators", "immersion", "pump", "pumps",
    "washer", "washing", "machine", "dryer", "tumble", "dishwasher", "oven", "cooker",
    "hob", "grill", "microwave", "kettle", "toaster", "shower", "socket", "sockets",
    "plug", "plugs", "extension", "fuse", "wire", "wiring", "alarm", "alarms", "smoke",
    "chimney", "extractor", "fan", "heater", "appliance"))
KEEP_IT_RUNNING = frozenset(("fridge", "freezer", "freezers", "fridges", "stove", "stoves",
                             "burner", "burners", "woodburner", "chiminea", "brazier",
                             "barbecue", "bbq", "smoker", "fireplace"))
SWITCH_OFF_FAULT = frozenset((
    "noise", "noisy", "knocking", "knocks", "knock", "banging", "bangs", "rumbling",
    "humming", "hums", "buzzing", "buzzes", "rattling", "grinding", "screeching", "squealing",
    "sparking", "sparks", "smoking", "smoke", "leak", "leaks", "leaking", "leaked", "dripping",
    "drips", "drip", "tripping", "trips", "tripped", "blowing", "blown", "fuse", "fault",
    "faulty", "broken", "broke", "stopped", "stops", "stopping", "cutting", "cuts", "hot",
    "overheating", "burnt", "burning", "scorch", "smell", "smells", "smelly", "beeping",
    "beeps", "chirping", "chirps", "flashing", "flashes", "error", "stuck", "jammed", "weak",
    "losing", "pressure", "condensation", "damp", "screech", "clunking", "clicking", "hissing"))
SWITCH_OFF_GET_OUT = re.compile(
    r"\b(?:gas|gasoline|petrol|carbon monoxide|fumes?|flames?|ablaze|on fire|fire brigade)\b")
SMOKE_ABOUT = re.compile(r"\b(?:smoke|smoking|smoulders?|smouldering|scorch(?:ed|ing)?)\b"
                         r"(?!\s+alarm)")
ALREADY_SAID_OFF = re.compile(
    r"\b(?:turn|switch|shut|power)\s+(?:it|that|this|the\s+\w+)\s+off"
    r"|\bunplug|\bleave\s+it\s+off|\boff\s+at\s+the\s+wall|\bswitch(?:ed)?\s+off|\bstop\s+the\s+cycle")
SWITCH_OFF_ALREADY = (
    "Yes - that is the thing to do, and I would do it now rather than after one more try. Off and "
    "left off is the safe place for it until somebody has looked at it.",
    "Yes, do that: off at the wall, and leave it off. Whatever is wrong with it does not get "
    "better for being run again tonight.",
    "Yes. Switch it off, unplug it if the plug is easy to reach, and leave it alone until it has "
    "been looked at properly.",
)
SWITCH_OFF_ADVISE = (
    "I would. Switch it off and leave it off, then get somebody to look at it - a fault you can "
    "hear or see is the one thing running it again makes worse.",
    "Yes - off, and a call to somebody who can look at it. A night without it is much cheaper "
    "than a night with it leaking, smoking or banging away.",
    "Turn it off and leave it off until somebody has seen it. If you can smell burning or see "
    "anything black, stop using it today rather than waiting for it to get worse.",
)
SWITCH_OFF_BATTERY = (
    "Swap it rather than leaving it out: a chirping alarm is annoying, an alarm with no battery in "
    "it is useless on the night it matters. If a fresh battery does not stop the chirp, take the "
    "whole unit down and get a new one - and if it is mains wired, take it off its base rather "
    "than leaving it with no battery at all.",
)


def _a_switch_off_asked(memory, clean):
    if not SWITCH_OFF_ASK.search(clean):
        return None
    said = " " + _the_line_before(memory).lower() + " "
    answer = " " + memory_bot(memory).lower() + " "
    thread = said + answer
    things = set(re.findall(r"[a-z']+", thread))
    if not (things & SWITCH_OFF_THINGS):
        return None
    if things & KEEP_IT_RUNNING:
        return None
    if "battery" in clean and (things & frozenset(("alarm", "alarms", "smoke"))):
        if things & frozenset(("beeping", "beeps", "chirping", "chirps", "chirp", "beep")):
            return SWITCH_OFF_BATTERY
        return None
    if SWITCH_OFF_GET_OUT.search(said):
        return None
    if SWITCH_OFF_GET_OUT.search(answer) or "999" in answer or "911" in answer:
        return None
    if ALREADY_SAID_OFF.search(answer):
        return SWITCH_OFF_ALREADY
    if SMOKE_ABOUT.search(said):
        return None
    if things & SWITCH_OFF_FAULT:
        return SWITCH_OFF_ADVISE
    return None
UNKNOWN = (
    "I'm not sure about that one, sorry — I'd rather not guess. A quick search online will "
    "get you a solid answer, and I can help you make sense of what you find.",
    "That's beyond what I know well, sorry. Searching for it will turn up better sources than "
    "I can offer; tell me what you find and I'll help you weigh it up.",
    "I don't know enough to answer that honestly. A search should sort you out quickly — and "
    "I'm happy to help with the rest of it.",
)
ASKED_IF_I_SAW = re.compile(
    r"^\s*(?:(?:and|so|but|oh|ah|anyway|anyways|well|hi|hey|right|now|look)\s+)*"
    r"(?:did|have|do)\s+(?:you|u)\s+"
    r"(?:see|seen|hear|heard|watch|watched|catch|caught|read|follow|following)\s+"
    r"(?:the|that|about|any|much)\b")
NOT_THE_NEWS = re.compile(
    r"\b(?:my|our|mum|mom|dad|mother|father|wife|husband|partner|boyfriend|girlfriend|son|"
    r"daughter|kid|kids|child|children|baby|brother|sister|nan|grandma|grandad|granny|friend|"
    r"boss|manager|colleague|neighbour|landlord|doctor|gp|nurse|dentist|midwife|vet|surgeon|"
    r"appointment|letter|email|e-mail|bill|invoice|results?|test)\b"
    r"|\bwhat i (?:said|mean|meant|wrote|sent|told you|asked)\b")
LOOKED_UP = re.compile(
    r"\b(?:forecast|weather|news|listings?|scores?|results?|prices?|times?|timetable|"
    r"timetables|traffic|schedule|opening|hours|fixtures?|table|standings|reviews?|ratings?)\b")
SAW_IT = re.compile(
    r"^\s*(?:(?:and|so|but|oh|ah|anyway|anyways|well|hey|right|now)\s+)*"
    r"(?:did|have|do)\s+(?:you|u)\s+"
    r"(?:see|seen|hear|heard|watch|watched|catch|caught)\s+"
    r"(?:it|that|him|her|them)\b"
    r"(?:\s+(?:last night|the other night|yesterday|tonight|today|this morning|on saturday|"
    r"at the weekend|yet))?\s*\??\s*$")
WATCHABLE = re.compile(
    r"\b(?:match|game|final|semi(?:-final)?|film|movie|episode|documentary|show|series|"
    r"season|race|fight|gig|concert|play|debate|episode|highlights|"
    r"first half|second half|highlights|extra time|finale)\b")
SAW_NEWS = re.compile(
    r"\b(?:election|football|rugby|cricket|tennis|boxing|olympics|formula one|f1|"
    r"the budget|budget|the bill|the vote|referendum|the debate|the interview|the speech|"
    r"the wedding|the funeral|the fight|the final|the match|the game|the semi)\b")


def names_the_thing_worth_watching(clean):
    said = SAW_IT_OR_THE.match(clean)
    if not said:
        return False
    tail = " ".join(clean[said.end():].split()[:5])
    return bool(WATCHABLE.search(tail) or SAW_NEWS.search(tail))


SAW_IT_OR_THE = re.compile(
    r"^\s*(?:(?:and|so|but|oh|ah|anyway|anyways|well|hi|hey|right|now|look)\s+)*"
    r"(?:did|have|do)\s+(?:you|u)\s+"
    r"(?:see|seen|hear|heard|watch|watched|catch|caught|read|follow|following)\s+"
    r"(?:the|that|about|any|much)\b")
def reads_as_if_i_saw(text, memory=None):
    clean = " ".join(str(text or "").lower().replace("\u2019", "'").split())
    if not clean or NOT_THE_NEWS.search(clean) or LOOKED_UP.search(clean):
        return False
    if SAW_IT.match(clean):
        return bool(WATCHABLE.search(str(last_user(memory) or "").lower()))
    if ASKED_IF_I_SAW.match(clean):
        return names_the_thing_worth_watching(clean)
    return False


WAS_THEY_THERE = re.compile(
    r"^[^a-z]*(?:was|were)\s+(?:he|she|they|everyone|anyone|anybody|everybody|you|u)\s+"
    r"(?:there\b|at\s+\w|with\s+\w)")
WAS_A_NAMED_ONE_THERE = re.compile(
    r"^[^a-z]*(?:was|were)\s+(?P<who>[a-z][a-z'-]*)"
    r"(?:\s+and\s+(?P<also>[a-z][a-z'-]*))?\s+there\b")
DID_THEY_GO = re.compile(
    r"^[^a-z]*(?:did|do|does)\s+(?:he|she|they|you|u)\s+"
    r"(?:like|enjoy|love|hate|go|come|make it|get there|stay|leave|arrive|say|think|"
    r"manage|turn up|show up|win|win it|lose|lose it|draw|score|play well|do well)\b")
A_THING_OR_A_PERSON = re.compile(
    r"\b(?:he|she|they|we|us|him|her|them|the|my|our|his|their)\s+\w+")
A_LOOK_BACK = re.compile(
    r"\b(?:was|wasnt|wasn't|were|werent|weren't|had|hadnt|hadn't|did|didnt|didn't|"
    r"liked|enjoyed|loved|hated|went|came|said|managed|stayed|left|arrived|won|lost|scored|"
    r"turned up|showed up|played|worked)\b")
WAS_IT_ANY_GOOD = re.compile(
    r"^[^a-z]*(?:was|were)\s+(?:it|that|everything|everyone|the\s+\w+|my\s+\w+|your\s+\w+|"
    r"his\s+\w+|her\s+\w+|their\s+\w+|our\s+\w+)\s+"
    r"(?:good|nice|busy|packed|fun|loud|quiet|worth it|any good|any cop|a laugh|any fun|"
    r"alright|all right|ok|okay|terrible|awful|great)\b")
PEOPLE_WHO_WENT = frozenset("""kids children child parents mum mom dad mother father family
friends friend sister brother wife husband partner boss neighbours neighbors cousins
grandparents grandmother grandfather aunt uncle colleagues classmates team group others
lot guests everyone""".split())
WENT_AND_WERE_ASKED = re.compile(
    r"^[^a-z]*(?:was|were|did)\s+(?:my|your|his|her|their|our|the)\s+(?P<noun>\w+)\s+"
    r"(?:there|about|around|have|enjoy|like|come|go|stay|leave|arrive|make it|get there|say)\b")
WHO_WAS_THERE = re.compile(
    r"^[^a-z]*(?:who\s+else|who|anyone else|anybody else)\s+"
    r"(?:was|were|went|came|turned up|showed up|there)\b")
HURT_IN_THE_LINE = re.compile(
    r"\b(?:hit|hits|hurt|hurts|touch|touched|hands? on|force|forced|push|pushed|shove|shoved|"
    r"grab|grabbed|threaten|threatened|threat|abuse|abusive|shout|shouted|yell|yelled|"
    r"corner|cornered)\b")
NOT_A_NAME = frozenset("""it that this these those there here the a an any some every no not
everything nothing something anything anyone anybody everyone everybody somebody someone
he she they you u we i him her them us me my your our their his its one ones thing things
day night week weekend time food meal party wedding dinner lunch trip holiday service drive
journey flight train bus match game film show weather traffic lunch tea supper""".split())


def _asked_about_the_day_they_had(clean):
    if HURT_IN_THE_LINE.search(clean) or LOOKED_UP.search(clean):
        return False
    if WAS_THEY_THERE.match(clean) or WAS_IT_ANY_GOOD.match(clean) or WHO_WAS_THERE.match(clean):
        return True
    went = DID_THEY_GO.match(clean)
    if went:
        verb = clean[went.start():went.end()].rstrip()
        if verb.endswith("think"):
            if verb.startswith("do") or verb.startswith("does"):
                said = clean[went.end():]
                if not A_LOOK_BACK.search(said) or not A_THING_OR_A_PERSON.search(said):
                    return False
        return True
    if WENT_AND_WERE_ASKED.match(clean) and WENT_AND_WERE_ASKED.match(clean).group("noun") in PEOPLE_WHO_WENT:
        return True
    named = WAS_A_NAMED_ONE_THERE.match(clean)
    if not named:
        return False
    who = named.group("who")
    also = named.group("also")
    if who in NOT_A_NAME or (also and also in NOT_A_NAME):
        return False
    return True


BARE_PICK = re.compile(
    r"^\s*(?:(?:so|and|but|ok|okay|well|then|just|hey|hi|right|anyway|anyways|oh|hmm|yeah|"
    r"yes|alright|honestly|you\s+know)[\s,]+)*"
    r"(?:what|which)\s+(?:should|shall|do|would|can|could|might)\s+i\s+"
    r"(?P<verb>wear|put\s+on|buy|get|do|take|bring|look\s+(?:for|at)|expect|ask|sign|"
    r"order|prepare)\b"
    r"(?:\s+(?:now|today|tonight|tomorrow|instead|else|next|then))?\s*\??\s*$", re.I)
LOST_IN_A_THREAD = (
    "Then the useful question is which part of it is actually yours to move. Which part could you "
    "change this week?",
    "It usually breaks into smaller pieces once they have names. What is the smallest of them "
    "that would make tomorrow easier?",
    "You have said the whole of it already, so I will not ask again. Which bit of it would you "
    "want to have sorted by Friday?",
)


BARE_PICK_LOST_FIRST = re.compile(
    r"^\s*(?:(?:so|and|but|ok|okay|well|then|just|hey|hi|right|anyway|oh|hmm|yeah|yes|alright|"
    r"honestly|tbh)[\s,]+)*"
    r"(?:what|which)\s+(?:should|shall|do|would|can|could|might)\s+i\s+do\s+"
    r"(?:first|next)\s*\??\s*$", re.I)


def _a_lost_ask(clean):
    clean = clean or ""
    return bool(BARE_PICK_LOST.match(clean) or BARE_PICK_LOST_FIRST.match(clean))


_START_ASK_BODY = (
    r"(?:"
    r"(?:i\s+)?(?:really\s+|honestly\s+|genuinely\s+|actually\s+|still\s+|simply\s+|"
    r"just\s+|even\s+)*"
    r"(?:"
    r"(?:do\s+not|don'?t|dont)\s+(?:even\s+)?know"
    r"|dunno"
    r"|(?:have|ve|got|i'?ve)\s+(?:absolutely\s+)?no\s+(?:idea|clue)"
    r"|(?:have\s+)?no\s+(?:idea|clue)"
    r"|(?:i\s+am\s+|i'?m\s+)?not\s+(?:really\s+|too\s+)?sure"
    r")\s+where\s+to\s+(?:start|begin)"
    r"|(?:where|how)\s+(?:do|should|shall|can|could|would)\s+(?:i|we)\s+(?:even\s+)?"
    r"(?:start|begin)"
    r"|where\s+to\s+(?:start|begin)"
    r")"
    r"(?:\s+(?:now|next|first|today|tonight|tomorrow|at\s+all|anymore|any\s+more|"
    r"with\s+(?:it|this|that|them)|on\s+(?:it|this|that)))?")
_START_ASK_LEAD_IN = (
    r"(?:(?:so|and|but|ok|okay|well|then|just|hey|hi|right|anyway|anyways|oh|hmm|yeah|"
    r"yes|alright|honestly|god|christ|ugh|tbh|seriously|you\s+know)[\s,]+)*"
    r"(?:(?:the\s+thing\s+is|the\s+problem\s+is|thing\s+is|truth\s+is|see|look|i\s+mean)"
    r"[\s,]+)*")
BARE_PICK_START = re.compile(
    r"^\s*" + _START_ASK_LEAD_IN + _START_ASK_BODY + r"\s*\.?\s*$", re.I)
BARE_PICK_START_CLAUSE = re.compile(
    r"\b(?:and|but)\s+" + _START_ASK_LEAD_IN + _START_ASK_BODY + r"\s*\.?\s*$", re.I)


def _a_start_ask(clean):
    clean = clean or ""
    return bool(BARE_PICK_START.match(clean) or BARE_PICK_START_CLAUSE.search(clean))


def _said_what_it_is_about(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    for turn in turns[-2:]:
        said = " ".join(str(turn.get("user") or "").lower().split())
        if len([w for w in said.split() if len(w) > 2]) >= 3:
            return True
    return False


START_ASK = stuck_line.HARD


def the_pool_for_a_lost_ask(memory, clean=""):
    if _news_above(memory):
        return BARE_PICK_AFTER_NEWS
    if _a_start_ask(clean):
        return START_ASK
    if _said_what_it_is_about(memory):
        return LOST_IN_A_THREAD
    return BARE_PICK_DO


def the_lost_ask_reply(memory, clean, repaired=None):
    if the_advice(memory):
        return None
    if not (_a_lost_ask(clean) or _a_lost_ask(repaired or "")
            or _a_start_ask(clean) or _a_start_ask(repaired or "")):
        return None
    pick = the_pool_for_a_lost_ask(memory, clean if _a_start_ask(clean) else "")
    if not pick:
        return None
    return _choose(pick, memory, clean)
WEATHER_COLD = re.compile(
    r"\b(?:freezing|chilly|freezing cold|bitterly cold|snowing|snow|frost|icy)\b|"
    r"\b(?:it'?s|its|it is|very|so|really|too|dead|bloody)\s+(?:a bit\s+|quite\s+)?cold\b",
    re.I)
WEATHER_HOT = re.compile(
    r"\b(?:boiling|scorching|roasting|heatwave|muggy|humid)\b|"
    r"\b(?:it'?s|its|it is|very|so|really|too|dead|bloody)\s+(?:a bit\s+|quite\s+)?"
    r"(?:hot|warm)\b", re.I)
WEATHER_WET = re.compile(r"\b(?:raining|pouring|drizzle|drizzling|wet out|showers|storm)\b",
                         re.I)


HEAVY_ABOVE = re.compile(
    r"\b(?:lump|lumps|tumou?r|cancer|leuka?emia|lymphoma|melanoma|dementia|alzheimers|"
    r"motor neurone|parkinsons|ms|chemo|chemotherapy|radiotherapy|palliative|hospice|"
    r"terminal(?:ly)?|very ill|really ill|seriously ill|dangerously ill|intensive care|"
    r"life support|stillborn|stillbirth|meningitis|sepsis)\b", re.I)
WORK_NEWS = re.compile(
    r"\b(?:job|jobs|work|hours|shift|shifts|money|pay|wages|salary|contract|business|"
    r"redundant|redundancy|clients?|customers?|interview|mortgage|rent|loan|debt|"
    r"benefits?|savings?)\b", re.I)


def _news_above(memory, heavy=False):
    if not isinstance(memory, dict):
        return False
    if _in_a_care_thread(memory):
        return True
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    for turn in turns[-2:]:
        low = " ".join(str(turn.get("user") or "").lower().split())
        if not low:
            continue
        if HEAVY_ABOVE.search(low):
            return True
        if reads_as_heavy_news(low) if heavy else (
                reads_as_bad_news(low) and not WORK_NEWS.search(low)):
            return True
        try:
            if loss.reads_as_loss(low):
                return True
        except Exception:
            pass
    return False


def _weather_above(memory):
    if not isinstance(memory, dict):
        return None
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    for turn in reversed(turns[-2:]):
        said = str(turn.get("user") or "")
        if not said:
            continue
        if WEATHER_WET.search(said):
            return "wet"
        if WEATHER_COLD.search(said):
            return "cold"
        if WEATHER_HOT.search(said):
            return "hot"
    return None


OCCASION_ABOVE = re.compile(
    r"\b(?:wedding|funeral|christening|baptism|interview|party|dinner|date|work|office|"
    r"conference|concert|festival|exam|graduation|church|meal out|night out)\b", re.I)


def _an_occasion_above(memory):
    if not isinstance(memory, dict):
        return False
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    return any(OCCASION_ABOVE.search(str(turn.get("user") or "")) for turn in turns[-2:])


THE_DAY_IS_NAMED = re.compile(
    r"\b(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b|"
    r"\b(?:next|this|that|the) (?:week|weekend)\b|"
    r"\b(?:tomorrow|tonight|today)\b|"
    r"\b(?:in|on|by|for|until) (?:january|february|march|april|may|june|july|august|september|"
    r"october|november|december)\b", re.I)


AN_OCCASION_AHEAD = re.compile(
    r"\b(?:wedding|funeral|christening|baptism|interview|party|dinner|date|work|office|"
    r"conference|concert|festival|exam|graduation|church|meal out|night out|"
    r"getting married|get married|got married|marrying|engaged|engagement|"
    r"bridesmaid|bridesmaids|best man|maid of honour)\b", re.I)


def _an_occasion_in_the_thread(memory, back=4):
    if not isinstance(memory, dict):
        return False
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    return any(AN_OCCASION_AHEAD.search(str(turn.get("user") or "")) for turn in turns[-back:])


TRIP_ABOVE = re.compile(
    r"\b(?:holiday|holidays|hols|trip|trips|away|abroad|flight|flights|flying|hotel|"
    r"camping|campsite|backpacking|weekend away|days? away|mini ?break)\b|"
    r"\b(?:go|going|went|off|flying|driving|heading)\s+(?:to\s+|off\s+to\s+)?"
    r"(?!the\b|a\b|an\b|my\b|his\b|her\b|their\b|our\b|your\b|work\b|bed\b|sleep\b|"
    r"school\b|uni\b|university\b|college\b|town\b|hospital\b|doctor\b|dentist\b|"
    r"shop\b|shops\b|toilet\b|loo\b|bath\b|shower\b|"
    r"have\b|get\b|see\b|be\b|do\b|make\b|take\b|try\b|need\b|want\b|start\b|stop\b|"
    r"give\b|put\b|keep\b|stay\b|look\b|ask\b|tell\b|say\b|ring\b|call\b|text\b|"
    r"eat\b|drink\b|cook\b|clean\b|wash\b|sort\b|finish\b|leave\b|come\b|meet\b)"
    r"[a-z]{3,}", re.I)


def _a_trip_above(memory):
    if not isinstance(memory, dict):
        return False
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    return any(TRIP_ABOVE.search(str(turn.get("user") or "")) for turn in turns[-2:])


BARE_PICK_NEEDS_THE_THING = frozenset({"look for", "look at", "expect", "ask", "sign",
                                       "order", "prepare"})
THREAD_NOTHING = frozenset("""
    hi hey hello morning evening there so and but ok okay well right yeah yes yep no not im i the
    a an it that this to for of in on at is was just also thanks thank please good great fine
    alright anyway oh hmm mm me my u you your cheers ta now then today tonight
""".split())


def _a_subject_above(memory):
    if not isinstance(memory, dict):
        return False
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    for turn in turns[-2:]:
        said = str(turn.get("user") or "")
        if not said.strip():
            continue
        words = re.findall(r"[a-z']+", said.lower())
        if any(word.strip("'") not in THREAD_NOTHING and len(word) > 2 for word in words):
            return True
    return False

_AFTER_A_CLAUSE = re.compile(
    r"(?:[,;:]\s+|\s+(?:and|but|so|because|though|although|while|when|now)\s+)"
    r"((?:what|which|how|where|who|when)\b[^,;:?!]*)\s*\??\s*$", re.I)


def _the_ask_clause(clean, memory=None):
    said = " ".join(str(clean or "").lower().split())
    if not said:
        return ""
    ask = ""
    reading = memory.get("understood") if isinstance(memory, dict) else None
    if isinstance(reading, dict):
        focus = " ".join(reading.get("focus") or []).split()
        if len(focus) >= 3 and said.endswith(" ".join(focus)) and " ".join(focus) != said:
            ask = " ".join(focus)
    if not ask:
        found = _AFTER_A_CLAUSE.search(said)
        ask = " ".join(found.group(1).split()) if found else ""
    return ask if len(ask.split()) >= 3 else ""


def _bare_pick(clean, memory=None):
    found = BARE_PICK.match(clean)
    from_the_clause = False
    if not found:
        ask = _the_ask_clause(clean, memory)
        found = BARE_PICK.match(ask) if ask else None
        from_the_clause = found is not None
    if not found:
        return None
    if found.group(0).strip().lower().startswith("which"):
        return BARE_PICK_WHICH
    verb = " ".join(found.group("verb").lower().split())
    pool = BARE_PICK_KIND.get(verb, BARE_PICK_DO)
    if from_the_clause and (OCCASION_ABOVE.search(str(clean or ""))
                            or THE_DAY_IS_NAMED.search(str(clean or ""))
                            or _an_occasion_in_the_thread(memory)):
        return None
    if from_the_clause and pool is BARE_PICK_DO:
        return None
    if verb in BARE_PICK_NEEDS_THE_THING and _a_subject_above(memory):
        return None
    if pool is BARE_PICK_WEAR and not _an_occasion_above(memory):
        weather = _weather_above(memory)
        if weather == "wet":
            return BARE_PICK_WEAR_WET
        if weather == "cold":
            return BARE_PICK_WEAR_COLD
        if weather == "hot":
            return BARE_PICK_WEAR_HOT
    if pool is BARE_PICK_BRING and _a_trip_above(memory):
        return BARE_PICK_TAKE
    if pool is BARE_PICK_DO and _news_above(memory, heavy=True):
        return BARE_PICK_AFTER_NEWS
    return pool


from .fallback_words import (
    A_PERSON_IN_A_CRISIS,
    CRISIS_ASK,
    HUMAN_ASK,
    HUMAN_HELPS,
    HUMAN_LEAD,
    HUMAN_QUOTED,
    HUMAN_TAIL,
    NAMES_THE_BOT,
    PRIVACY_NOT_THIS,
    REFERS_BACK,
    REPAIR_DECISION,
    LEAVING_IN_THE_LINE,
    REPAIR_BARE_IT,
    REPAIR_PERSON,
    REPAIR_TARIFF,
    REPAIR_TRADE,
    REPAIR_WHAT_IT_IS_WORTH,
    REPAIR_WHETHER,
    SELF_ASK,
    A_VIEW_ASKED_FOR,
    TRUST_ASK,
    WHO_FOR_IT,
    WHO_FOR_IT_BODY,
    WHO_FOR_IT_ROUTES,
    WHO_FOR_IT_SAID,
    WHO_FOR_IT_SAID_VOICE,
    WHO_NAMED_BEFORE,
    WHO_TO_TALK_ASK,
    WHO_TO_TALK_TO,
    WHO_TO_TALK_TO_A_BAD_STRETCH,
)




def _opens_the_line(prefix):
    return bool(HUMAN_LEAD.match(prefix)) or bool(HUMAN_QUOTED.search(prefix))


HUMAN_TALK_ASK = re.compile(
    r"\b(?:can|could|may|might) i (?:please )?(?:speak|talk|chat) (?:to|with) "
    r"(?:a |an |a real |an actual |some )*(?:human being|actual human being|real human being|"
    r"human|person|real person|actual person|actual human|real human)\b|"
    r"\b(?:i )?(?:want|need|would like|wanna|have) to (?:speak|talk|chat) (?:to|with) "
    r"(?:a |an |a real |an actual )*(?:human being|actual human being|real human being|human|"
    r"person|real person|actual person|actual human|real human)\b|"
    r"\bis there (?:a |an |any )?(?:real |actual )?(?:human being|actual human being|human|"
    r"person|someone real|somebody real)\b|"
    r"\b(?:get|give) me (?:a |an )?(?:real |actual )?(?:human|human being|person)\b|"
    r"\b(?:any|got any|got a) (?:chance of )?(?:a |an )?(?:real |actual )?(?:human|human being|"
    r"person)\b|"
    r"\b(?:real|actual) (?:human|person|human being) (?:here|on here|around|available)\b")
HUMAN_TO_ME = re.compile(
    r"^\s*(?:that |who |which )?(?:i|we) (?:can|could|may|might|would|should|will)?\s*"
    r"(?:talk|speak|chat|ask|write)\s*(?:to|with)?\s*(?:you|u)?\s*"
    r"(?:please|pls|now|first|then)?\s*[.!?]*\s*$")
HUMAN_OTHER_END = re.compile(r"^\s*(?:on|at) the other (?:end|side)\b[^a-z]*$")


def _asks_elsewhere(tail):
    if HUMAN_HELPS.match(tail or ""):
        return False
    if HUMAN_TAIL.match(tail or ""):
        return False
    if HUMAN_OTHER_END.match(tail or ""):
        return False
    return any(word not in HUMAN_EMPTY for word in re.findall(r"[a-z]+", (tail or "").lower()))


def _asks_for_a_person_to_talk_to(clean):
    matched = HUMAN_TALK_ASK.search(clean)
    if not matched or not _opens_the_line(clean[:matched.start()]):
        return False
    tail = clean[matched.end():]
    return bool(HUMAN_TAIL.match(tail) or HUMAN_TO_ME.match(tail)
                or HUMAN_OTHER_END.match(tail))
HAND_ASK = re.compile(
    r"^(?:so |ok |okay |right |hi |hiya |hello |hey |and |please )*"
    r"(?:(?:can|could|will|would) (?:you|u) (?:please )?"
    r"(?:help(?: (?:me|us))?(?: out)?|give (?:me|us) a hand|lend (?:me|us) a hand"
    r"|do (?:me|us) a favour|advise (?:me|us)|be a hand)"
    r"|(?:i )?(?:could do with|need|want|would like) (?:(?:your|some|a bit of) )?"
    r"(?:help|a hand|advice|a bit of advice)"
    r"|(?:can|could) (?:i|we) (?:get|have|ask for) (?:(?:your|some|a little|a bit of) )?"
    r"(?:help|a hand|advice)"
    r"|help(?: me)?(?: out)?"
    r"|give me a hand"
    r")"
    r"(?: (?:with|about) (?:something|anything|a thing|stuff|it))?"
    r"(?: (?:here|please|now|today|tonight|asap|urgently|quick(?:ly)?|straight away))?"
    r"(?: (?:right )?now)?(?: please)?$")


def _asks_for_help(clean, understood=None):
    lines = [clean]
    if isinstance(understood, dict):
        said = understood.get("plain")
        if isinstance(said, str) and said and said != clean:
            lines.append(said)
    for line in lines:
        bare = " ".join(re.sub(r"[^a-z0-9 ]+", " ", str(line or "").lower()).split())
        if HAND_ASK.match(bare):
            return True
    return False
MADE_ASK = re.compile(r"\bwho (?:made|makes|told|tells|taught|programmed|built|wrote)\s+(?:you|u)\b"
                      r"|\bwhat (?:made|makes) (?:you|u)\s+(?:say|think|believe|decide|choose|"
                      r"pick|answer|reply|write|act|do\s+that)\b")
SELF_OPENER = re.compile(r"\b(?:where|why|how\s+long)\b")
MODEL_ASK = re.compile(
    r"\b(?:what|which)\s+(?:\w+\s+){0,2}?(?:model|version|engine|llm|ai)\s+(?:are|is|do|"
    r"did)\s+(?:you|u)\b"
    r"|\bwhat\s+(?:are|is|were)\s+(?:you|u)\s+(?:running|based|built|trained)\s+on\b"
    r"|\bare\s+(?:you|u)\s+(?:a\s+|an\s+)?(?:llm|large\s+language\s+model|"
    r"neural\s+net\w*|transformer|deep\s+learning\s+model)\b")
WORKINGS_ASK = re.compile(
    r"\bhow\s+(?:do|does)\s+(?:you|u)\s+(?:actually\s+|really\s+)?work"
    r"\s*(?:then|though|really|anyway|now)?\s*$"
    r"|\bhow\s+(?:are|were)\s+(?:you|u)\s+(?:built|made|programmed|put together|written)\b"
    r"|\bwhat(?:s| is)\s+(?:inside|under)\s+(?:you|your hood|the hood)\b"
    r"|\bdo\s+(?:you|u)\s+use\s+(?:ai|an ai|chatgpt|gpt|a model|an llm|llm|a neural network)\b"
    r"|\bhow\s+do\s+(?:you|u)\s+answer\s+(?:questions|these|things|that)\s*$")
ASKING_ASK = re.compile(
    r"\bwhy\s+(?:do|did|does|are|were|would)\s+(?:you|u)\s+"
    r"(?:keep|always|even|still)\s+(?:be\s+)?(?:ask|asking)\b"
    r"|\bwhy\s+(?:do|did|does|are|were|would)\s+(?:you|u)\s+(?:ask|asking|asked)\s+"
    r"(?:me\s+)?(?:so\s+many|this\s+many|that\s+many|all\s+these|all\s+the|these|that|this)\b"
    r"|\bwhy\s+(?:do|did|does)\s+(?:you|u)\s+ask\s*$"
    r"|\bwhy\s+(?:are|were)\s+(?:you|u)\s+asking(?:\s+me)?\s*(?:that|this|so\s+many)?\s*$"
    r"|\b(?:do|did)\s+(?:you|u)\s+(?:always\s+|really\s+|have\s+to\s+)?ask\s+"
    r"(?:so|this|that|these)\s+many\s+questions\b"
    r"|\bwhy\s+(?:so\s+many|all\s+these|all\s+the)\s+questions?\b"
    r"|\b(?:stop|quit|enough\s+with)\s+(?:the\s+)?(?:asking|questions)\b")


TRUST_ASK = re.compile(
    r"\b(?:can|could|should|shall|may)\s+(?:i|we)\s+(?:really\s+|honestly\s+|actually\s+)?"
    r"(?:trust|believe|rely\s+on)\s+(?:you|u)\b"
    r"|\bcan\s+(?:i|we)\s+(?:trust|believe)\s+what\s+(?:you|u)\s+(?:say|tell\s+me)\b"
    r"|\bare\s+(?:you|u)\s+(?:trustworthy|reliable|honest|truthful)\b"
    r"|\bwill\s+(?:you|u)\s+(?:tell|give)\s+me\s+the\s+truth\b"
    r"|\bare\s+(?:you|u)\s+telling\s+(?:me\s+)?the\s+truth\b"
    r"|\bare\s+(?:you|u)\s+lying\b"
    r"|\bdo\s+(?:you|u)\s+(?:ever\s+)?(?:lie|guess|make\s+(?:things|stuff|that|it|this|them)\s+up|"
    r"make\s+up\s+(?:things|stuff|answers|facts))\b"
    r"|\bare\s+(?:you|u)\s+(?:making|inventing)\s+(?:that|this|it|things|stuff)\s+up\b", re.I)
BETWEEN_US_ASK = re.compile(
    r"\b(?:is|are|was|were|will|would|does|do|can)\s+(?:this|that|it)\s+"
    r"(?:(?:chat|conversation|thread|session)\s+)?(?:just\s+|really\s+)?"
    r"between\s+(?:us|you\s+and\s+me)\b"
    r"|\b(?:is|are)\s+(?:what|everything)\s+i\s+(?:say|tell|tell\s+you|type|write)\s+"
    r"(?:just\s+)?between\s+(?:us|you\s+and\s+me)\b"
    r"|\bare\s+(?:we|you)\s+(?:private|confidential|anonymous)\s+(?:here|on\s+this|in\s+this)\b"
    r"|\bis\s+(?:this|it)\s+(?:chat\s+)?anonymous\b"
    r"|\bwhat\s+(?:happens|happened)\s+to\s+(?:what|everything)\s+i\s+(?:say|tell|type|write|send)\b",
    re.I)
SECRET_ASK = re.compile(
    r"\bcan\s+(?:you|u)\s+keep\s+(?:a\s+)?secret\b"
    r"|\bare\s+(?:you|u)\s+good\s+at\s+keeping\s+(?:a\s+)?secret\b"
    r"|\bcan\s+i\s+tell\s+(?:you|u)\s+(?:a\s+)?secret\b"
    r"|\bkeep\s+(?:this|it)\s+(?:between\s+(?:us|you\s+and\s+me)|to\s+yourself)\b"
    r"|\bthis\s+stays\s+between\s+(?:us|you\s+and\s+me)\b", re.I)
PROMISE_ASK = re.compile(
    r"\bpromise\s+(?:me\s+)?(?:that\s+)?(?:you|u)\s+(?:won'?t|wont|will\s+not|never|not)\s+"
    r"(?:tell|say|repeat|breathe|mention|share|spread)\b"
    r"|\bpromise\s+(?:me\s+)?(?:not\s+to|you'?ll\s+not|you\s+will\s+not|you\s+won'?t|you\s+wont)\s+"
    r"(?:tell|say|repeat|mention)\b"
    r"|\bswear\s+(?:me\s+)?(?:that\s+)?(?:you|u)\s+(?:won'?t|wont|will\s+not|never)\s+"
    r"(?:tell|say|repeat|mention)\b"
    r"|\b(?:you|u)\s+(?:won'?t|wont|will\s+not)\s+(?:be\s+)?(?:tell(?:ing)?|say(?:ing)?)\s+"
    r"(?:anyone|anybody|no\s+one|a\s+soul|nothing\s+to\s+anyone)\b"
    r"|(?<!\bi )(?<!\bwe )(?<!\bthey )\b(?:don'?t|do\s+not)\s+(?:go\s+telling|tell)\s+"
    r"(?:anyone|anybody|no\s+one|a\s+soul|my\s+(?:mum|mom|dad|husband|wife|partner|boss|mate|friend|"
    r"sister|brother|family|parents|doctor|girlfriend|boyfriend|other\s+half))\b"
    r"|\bjust\s+between\s+(?:us|you\s+and\s+me)\b"
    r"|\bno\s+one\s+else\s+(?:will|can|needs\s+to)\s+(?:hear|see|know)\s+(?:about\s+)?this\b", re.I)
JUDGING_ASK = re.compile(
    r"\b(?:will|would|are|do|did|might)\s+(?:you|u)\s+(?:going\s+to\s+)?"
    r"(?:judge|judging|judgement|judgment)(?:\s+me\b|\s+us\b|\s+my\b|\s+what\s+i\b|"
    r"\s+someone\b|[\s?!.]*$)"
    r"|\b(?:don'?t|do\s+not|please\s+don'?t|promise\s+(?:me\s+)?(?:you\s+won'?t|not\s+to)|"
    r"you\s+won'?t)\s+judge\b"
    r"|\bwill\s+(?:you|u)\s+(?:think|say)\s+i'?m\s+(?:weird|stupid|mad|dumb|thick|odd|"
    r"crazy|silly|pathetic|a\s+failure)\b", re.I)


REGRET_ASK = re.compile(r"\bwhat\s+(?:do|does|would|did)\s+(?:you|u)\s+regrets?\b")
SELF_PURPOSE = re.compile(r"\bwhat (?:are|were) (?:you|u) (?:for|made for|here for)\b|"
                          r"\bwhat(?:'s| is) your (?:purpose|point)\b|\bpoint of you\b")
LIMITS_ASK = re.compile(
    r"\b(?:what|which|anything|something)\b"
    r"(?![a-z ]{0,20}\b(?:i|we|he|she|they|us|them|him|her|me)\b)[a-z ]{0,30}?"
    r"(?:\bcan'?t|\bcannot|\bcan\s+not|\bdon'?t|\bdo\s+not|\bcan\s+you\s+(?:not|n'?t))\s+"
    r"(?:you\s+)?(?:do|help|help with|answer|know|handle|understand|manage|say|cope with)"
    r"\s*(?:with|about)?[\s?!.]*$"
    r"|\b(?:what|which)\s+(?:are|is)\s+(?:it\s+)?(?:you|u)\s+"
    r"(?:bad|not good|no good|rubbish|useless|weak)\s+at[\s?!.]*$"
    r"|\bwhat\s+[a-z ]{0,20}?\byou\s+(?:bad|not good|no good|rubbish|useless)\s+at[\s?!.]*$"
    r"|\bwhat\s+are\s+your\s+(?:limits?|weak\s*spots?|weaknesses?)[\s?!.]*$")
OWN_DEVICE = re.compile(
    r"\b(?:my|our)\s+(?:laptop|phone|pc|computer|router|wifi|broadband|tablet|ipad|tv)\b"
    r"|\bhelp\s+me\b|\bhow\s+(?:do|can|should)\s+i\b")
A_BARE_ONLINE = re.compile(
    r"^\s*(?:so\s+|and\s+|ok(?:ay)?\s+|just\s+)?(?:are|is|r)\s+(?:you|u)\s+"
    r"(?:really\s+|still\s+|even\s+)?(?:online|connected|there)\s*"
    r"(?:(?:right\s+|at\s+the\s+)?now\s*|at\s+the\s+moment\s*|today\s*|tonight\s*|"
    r"then\s*|please\s*|mate\s*|though\s*)*[\s?!.]*$")
SELF_WORDS = frozenset("""
learn learns learning learned learnt teach taught train trained
think thinks thinking thought opinion opinions view views judgement judgment mind brain
smart clever intelligent wise understand understands reason senses
mistake mistakes wrong right perfect honest
feel feels feeling feelings emotion emotions
alive living human person people body bodies family friends friend age old here located
program programmed code computer machine robot ai chatbot bot conscious consciousness aware
sentient knowledge know knows exist exists existence point purpose there
decide decides deciding decided decision decisions choose chooses choosing chosen choice
choices pick picks picking select selects sort sorts answer answers answering answered
regret regrets regretted regretting
sums sum maths math mathematics arithmetic add adds adding addition subtract multiply divide
total percentage percentages percent calculate calculation count counting
spell spells spelling spelled spelt grammar punctuation apostrophe comma commas typo typos
# The filler the same asks are said with ("can you add up", "can you spell it for me", "can you
# check my grammar") belongs here; the nouns a request is made of do not. `bill`, `check`, `word`
# and `split` were in this set for one revision and let a real request through to the card: "can
# you add up a bill" lost its Citizens Advice answer and was told the bot can do sums (red-robin,
# #11382). Every word left in `SELF_WORDS` has to be true of a line about the bot itself.
up a an for my it this that
""".split())
for _group, _words in (
        ("learn", "learn learns learning learned learnt teach taught train trained"),
        ("think", "think thinks thinking thought opinion opinions view views judgement "
                  "judgment mind brain smart clever intelligent wise understand understands "
                  "reason senses knowledge know knows decide decides deciding decided decision "
                  "decisions choose chooses choosing chosen choice choices pick picks picking "
                  "select selects sort sorts answer answers answering answered"),
        ("wrong", "mistake mistakes wrong right perfect honest"),
        ("feel", "feel feels feeling feelings emotion emotions alive living human person "
                 "people conscious consciousness aware sentient"),
        ("purpose", "exist exists existence point reason purpose"),
        ("regret", "regret regrets regretted regretting"),
        ("sums", "sums sum maths math mathematics arithmetic add adds adding addition subtract "
                 "multiply divide total percentage percentages percent calculate calculation "
                 "count counting split"),
        ("spelling", "spell spells spelling spelled spelt grammar punctuation apostrophe comma "
                     "commas typo typos letters"),
        ("where", "body bodies family friends friend age old here there located program "
                  "programmed code computer machine robot ai chatbot bot")):
    for _word in _words.split():
        SELF_GROUP.setdefault(_word, _group)


def _says_only_what_they_said(lines, clean):
    said = set(re.findall(r"[a-z']+", str(clean or "").lower()))

    def _unsupported(line):
        for phrase, support in DETAILS_IN_A_WARM_LINE:
            if phrase in line.lower():
                return not any(word in said for word in support)
        return False

    kept = [line for line in lines if not _unsupported(line)]
    return kept or [line for line in lines if not _unsupported(line)] or list(lines)


HAPPENING_NOW = re.compile(r"\b(?:today|tonight|this\s+(?:evening|afternoon|morning)|right\s+now)\b",
                           re.I)


DATE_GIVEN = re.compile(
    r"\b(?:in|on|next|this|at)\s+(?:january|february|march|april|may|june|july|august|september|"
    r"october|november|december|jan|feb|mar|apr|jun|jul|aug|sep|sept|oct|nov|dec|"
    r"week|weekend|month|year|spring|summer|autumn|winter|"
    r"monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b", re.I)


_APART = re.compile(
    r"\b(?:away|apart|elsewhere|abroad|miles|far\s+away|over\s+there|back\s+home|visiting|"
    r"visit|stay(?:ing)?\s+with|lives?\s+(?:in|near|abroad|away)|living\s+(?:in|near|abroad|away)|"
    r"uni|university|college|the\s+other\s+side|different\s+(?:town|city|country)|"
    r"in\s+(?:london|manchester|birmingham|leeds|glasgow|edinburgh|cardiff|belfast|dublin|"
    r"paris|spain|france|italy|america|australia|canada|germany|portugal|greece|"
    r"scotland|wales|ireland|england))\b", re.I)

_PLACES_THEM = re.compile(
    r"\b(?:seeing\s+them|see\s+them|off\s+to\s+see|go\s+and\s+see|going\s+to\s+see|"
    r"visit\s+them|visiting\s+them|go\s+over|going\s+over|drive\s+(?:up|down)|"
    r"travell?ing\s+(?:to|up|down))\b", re.I)

_SHE = frozenset("""wife mum mom mother mummy daughter sister gran granny nan nana grandma
    grandmum grandmother aunt auntie niece stepmum stepmother stepdaughter motherinlaw
    sisterinlaw daughterinlaw fiancee girlfriend missus mrs""".split())
_HE = frozenset("""husband dad father daddy son brother grandad granddad grandpa granddad
    grandfather uncle nephew stepdad stepfather stepson fatherinlaw brotherinlaw soninlaw
    fiance boyfriend mr""".split())


def _the_pronoun(clean):
    words = re.findall(r"[a-z']+", str(clean or "").lower().replace("\u2019", "'"))
    she = he = False
    for word in words:
        stem = word[:-1] if word.endswith("s") and word[:-1] in (_SHE | _HE) else word
        if stem in _SHE:
            she = True
        elif stem in _HE:
            he = True
    if she and not he:
        return "her"
    if he and not she:
        return "him"
    return ""


def _occasion_pool(occasion, clean):
    if goodnews.someone_elses_occasion(clean):
        pool = SOMEONE_ELSES_DAY.get(occasion)
        if pool:
            apart = bool(_APART.search(str(clean or "")))
            kept = [line for line in pool
                    if apart or not _PLACES_THEM.search(line)]
            pronoun = _the_pronoun(clean)
            if pronoun:
                kept = [re.sub(r"\bthem\b", pronoun, line) for line in kept]
            return tuple(kept or pool)
    pool = OCCASION[occasion]
    drop = []
    if HAPPENING_NOW.search(clean):
        drop.append("when it comes")
    if DATE_GIVEN.search(clean):
        drop.append("how far off")
    if drop:
        pool = tuple(line for line in pool
                     if not any(phrase in line.lower() for phrase in drop)) or pool
    return pool


def _their_own_slip(clean, memory=None):
    if "?" in clean:
        return None
    if HEAVY_ABOVE.search(clean) or SERIOUS_NEWS.search(clean) or BABY_LOSS.search(clean):
        return None
    if SELF_BLAME_ASKS.search(clean) or A_VERDICT_ON_THE_PERSON.search(clean):
        return None
    if GOING_TO_DIE.search(clean):
        return None
    if HARM_IN_A_LAUGH.search(clean) or LAUGH_STOPPED.search(clean):
        return None
    if isinstance(memory, dict) and _in_a_care_thread(memory):
        return None
    if A_CROWD_LAUGHED.search(clean):
        return LAUGHED_AT
    if A_PERSON_LAUGHED.search(clean) or A_OWN_LAUGH.search(clean):
        return None
    if LAUGHED_AT_THEM.search(clean):
        return LAUGHED_AT
    if SOMEONE_ELSES_SHAME.search(clean):
        return None
    if DIE_OF_IT.search(clean) or THE_GROUND_OPENS.search(clean):
        return EMBARRASSED
    if EMBARRASSMENT_WORD.search(clean) and THE_MOMENT_IS_THEIRS.search(clean):
        return EMBARRASSED
    if A_SLIP_IS_NOT_A_FALL.search(clean):
        return None
    if A_SOCIAL_SLIP.search(clean) or (A_SLIP.search(clean) and IN_A_ROOM.search(clean)):
        return EMBARRASSED
    return None


CLOSED_DOOR = (
    "That's a hard thing to keep going back to. What sort of work are you after?",
    "Applying and hearing nothing wears a person down, and it is not about what you are worth. "
    "How long has this been going on?",
    "A door that keeps closing is exhausting. What have you been trying for?",
    "It's a rough time to be looking. What is the job you are chasing?",
)
NEGATIVE = (
    "That sounds rough. If you want, I can help you think through what to do next.",
    "Ugh, that's a lot to carry. What would make today a bit easier?",
    "I'm sorry — that's frustrating. Want a hand working out the next step?",
    "Sorry to hear that. What would help most right now?",
)
NAMED_NEGATIVE = tuple(line for line in NEGATIVE if "frustrating" not in line)


SERIOUS_NEWS = re.compile(
    r"\b(?:heart attack|cardiac|stroke|blood clot|aneurysm|"
    r"cancer|tumou?rs?|leuka?emia|lymphoma|melanoma|chemo(?:therapy)?|radiotherapy|"
    r"dialysis|transplant|bypass|sepsis|septica?emia|pneumonia|meningitis|"
    r"intensive care|high dependency|life support|resuscitat\w+|"
    r"operation|surgery|amputat\w+|"
    r"admitted|in hospital|into hospital|hospital (?:last|this) (?:night|week|morning)|"
    r"collapsed|collapse|seizures?|convulsions?|"
    r"diagnosed|diagnosis|terminal|palliative|hospice)\b", re.I)
CLOSE_OWNER = re.compile(r"\b(?:my|our)\s+(?:" + badnews.KIN + r")\b", re.I)
NOT_THEIR_NEWS = re.compile(
    r"\b(?:sponsor\w*|fundrais\w*|raising|raise money|awareness|charity|marathon|"
    r"race for life|donat\w*|nurses?|nursing|(?:works?|working) (?:at|in|for)|shift)\b", re.I)
NOT_YET_NEWS = re.compile(
    r"\b(?:i think|i thought|might|could have|maybe|may have|suspect\w*|probably|possibly|"
    r"what if|is it possible|worried (?:it|that|he|she|they)|terrified (?:it|that)|"
    r"scared (?:it|that)|afraid (?:it|that)|waiting (?:on|for) (?:the )?results)\b", re.I)


def reads_as_someone_close_is_ill(clean):
    if not clean or NOT_THEIR_NEWS.search(clean):
        return False
    if not CLOSE_OWNER.search(clean):
        return False
    serious = SERIOUS_NEWS.search(clean)
    if not serious:
        return False
    doubt = NOT_YET_NEWS.search(clean)
    if doubt and doubt.start() < serious.start():
        return False
    return True


LEAVING_A_PERSON = re.compile(
    r"\b(?:my|our)\s+(?:son|daughter|boy|girl|kid|kids|children|child|eldest|youngest|"
    r"stepson|stepdaughter|mum|mom|mother|dad|father|parents|sister|brother|best\s+friend|"
    r"friend|mate|neighbour|neighbor|grandson|granddaughter|grandchild|nan|gran|aunt|uncle|"
    r"cousin|husband|wife|partner|boyfriend|girlfriend|niece|nephew)\b|"
    r"\b(?:he|she|they|the\s+kids|the\s+children|everyone)\b", re.IGNORECASE)
A_CHILD = re.compile(
    r"\b(?:my|our)\s+(?:son|daughter|boy|girl|kid|kids|children|child|eldest|youngest|"
    r"stepson|stepdaughter)\b|\bthe\s+(?:kids|children|eldest|youngest)\b", re.IGNORECASE)
THE_LEAVE_HAS_HAPPENED = re.compile(
    r"\b(?:left|moved|went|gone|flew|flown|relocated|emigrated)\b|"
    r"\b(?:has|have|had|she's|hes|he's|they've|theys|we've|was|were)\b[^.,;!?]{0,16}\b(?:left|"
    r"moved|gone|flew|flown|relocated|emigrated)\b",
    re.IGNORECASE)
NOT_LEAVING_ANYONE = re.compile(
    r"\bhow\s+(?:do|can|should|could|would|might|shall)\s+i\b|\bhow\s+to\b|"
    r"\bwhat\s+should\s+i\b|\bany\s+(?:tips|advice|ideas)\b|\bany\s+idea\b|"
    r"\bwhat\s+do\s+you\s+think\b|\bwhat\s+would\s+you\b|"
    r"\bmoving\s+in\s+with\b|\b(?:coming|moved|moving)\s+(?:in|back)\b|"
    r"\bstaying\s+with\s+(?:us|me)\b|\bstay(?:ing|s|ed)?\s+with\b|"
    r"\b(?:starts?|starting|started)\s+(?:school|nursery|reception|primary|year\s+one)\b",
    re.IGNORECASE)


FORGETS_AGAIN = re.compile(
    r"\b(?:i|im|ive)\b[^.?!]*\b(?:keep|keeps|always|constantly|still|never remember|"
    r"cant remember to|forget to)\b[^.?!]*\b" + FORGET_A_THING
    + r"|\b(?:i|im|ive)\s+(?:always|constantly|keep)\s+" + FORGET_A_THING
    + r"|\bi\s+never\s+remember\s+(?:to\s+\w+|my\b|the\b)")
FORGET_A_DATE = re.compile(
    r"\b(?:i|im|ive|we|were)\b[^.?!]*\b(?:forget|forgets|forgetting|forgot|never remember|"
    r"(?:keep|keeps|kept) missing|miss|misses|missing)\b[^.?!]*\b(?:appointments?|birthdays?|"
    r"meetings?|the dentist|deadlines?|due dates?|renewals?|anniversar(?:y|ies)|plans?)\b")
FORGETS_A_CLASH = re.compile(
    r"\bdouble[- ]book(?:s|ed|ing)?\b|\bbooked (?:two|2) things\b|\bbook (?:two|2) (?:things|"
    r"plans)\b|\btwo (?:appointments|meetings|plans) (?:on|for|in) the same\b")
FORGET_A_SECRET = re.compile(
    r"\b(?:forget|forgets|forgetting|keep losing|lost|slips?)\b[^.?!]*\bpasswords?\b"
    r"|\bpasswords?\b[^.?!]*\b(?:keep|slip|forget)\w*\b")


TELLING_A_CHILD = re.compile(
    r"\b(?:tell|telling|told|say|saying|explain|explaining|talk|talking|break it to|"
    r"break the news)\b"
    r"[^.?!]{0,32}\b(?:kid|kids|child|children|son|daughter|boy|boys|girl|girls|"
    r"grandchild|grandchildren|grandson|granddaughter|teenager|teen|toddler|little one|"
    r"niece|nephew)\b")
A_DEATH_FROM_TODAY = re.compile(
    r"\b(?:today|this morning|this afternoon|this evening|tonight|last night|yesterday|"
    r"an hour ago|a moment ago|just (?:now|died|heard|found out)|hours ago)\b")
A_CHILD_DIED = re.compile(
    r"\b(?:baby|child|children|kid|kids|son|daughter|boy|girl|boys|girls|teenager|teen|"
    r"toddler|boy|girl|niece|nephew|grandson|granddaughter)\b"
    r"\s+(?:has |have |had )?(?:just )?(?:died|passed away|passed on|passed|was killed|"
    r"were killed|is dying|are dying)\b")


A_DEATH_IN_THE_LINE = re.compile(
    r"\b(?:died|dies|dying|dead|death|passed away|passed on|funeral|buried|burial|"
    r"cremation|killed)\b")


A_SUICIDE_IN_THE_LINE = re.compile(
    r"\b(?:suicide|suicidal|took (?:his|her|their) own life|killed (?:him|her|them)self|"
    r"ended (?:his|her|their) own life|overdose[sd]?|od'd)\b", re.I)


def a_fresh_death_and_the_words(clean):
    text = " ".join(str(clean or "").lower().split())
    return bool(TELLING_A_CHILD.search(text)
                and A_DEATH_IN_THE_LINE.search(text)
                and A_DEATH_FROM_TODAY.search(text)
                and not A_CHILD_DIED.search(text)
                and not A_SUICIDE_IN_THE_LINE.search(text))


def asks_what_to_tell_a_child(clean):
    text = " ".join(str(clean or "").lower().split())
    return bool(TELLING_A_CHILD.search(text)
                and A_DEATH_IN_THE_LINE.search(text)
                and not A_DEATH_FROM_TODAY.search(text)
                and not A_CHILD_DIED.search(text))


_ILL = re.compile(r"\b(?:cold|cough|coughing|flu|throat|chest|temperature|virus|sniffles?|"
                  r"sneez\w*|head cold)\b", re.I)
SYMPTOM_LINGERS = LINGERED_LINE
_LUMP = re.compile(r"\b(?:lumps?|growths?)\b"
                   r"(?!\s+in\s+(?:my|your|the)\s+throat)"
                   r"(?!\s*-?\s*sums?\b)", re.I)
_CAUGHT = re.compile(
    r"\b(?:cold(?!\s+(?:sore|sores|feet|hands|fingers|toes|air|weather|room|drink|water|days?|"
    r"morning|night|outside|shower|call))|cough|coughing|flu|virus|temperature|head cold|"
    r"sniffles?|sneez\w*)\b", re.I)


_RESULT = re.compile(
    r"\b(?:pass|passed|passes|fail|failed|fails|results?|exam|exams|test|tests|interviews?|"
    r"offers?|application|applied|audition|trial shift|probation|scan|biopsy|referral|hearing|"
    r"decision|verdict|grades?|mark|marks|"
    r"got (?:the|a) (?:job|place|part|role|offer|position)|get (?:the|a) (?:job|place|part|role)|"
    r"got in)\b", re.I)
_WAITING = re.compile(
    r"\b(?:(?:i|we) (?:find|finds) out|find out (?:next|on|tomorrow|in|at the end)|"
    r"(?:i|we) (?:hear|hearing) back|"
    r"(?:i|we|im|i'm|i am|we|were|we're|we are)\s+(?:still\s+)?"
    r"(?:havent|hasnt|haven't|hasn't|not|never)\s+heard\s+back|"
    r"(?:i|we|im|i'm|i am)\s+(?:still\s+)?(?:havent|hasnt|haven't|hasn't) heard\s+"
    r"(?:back|anything|a thing|yet|from (?:the |my |our )?" + _ISSUER + r")|"
    r"(?:i|im|i'm|i am|we|were|we're|we are)\s+(?:still\s+)?waiting\s+to hear|"
    r"(?:i|im|i'm|i am|we|were|we're|we are)\s+(?:still\s+)?waiting\s+on\s+"
    r"(?:(?:the |my |our )?(?:(?:exam |test |scan |interview |blood test )?"
    r"(?:results?|outcome|decision|news|answer|reply|offer|scan|tests?|exam|interview))|"
    r"(?:the |my |our )?" + _ISSUER + r")|"
    r"(?:i|we) (?:should|will|would) know|(?:i|we) (?:am|are|'m|'re) out of|"
    r"out of (?:my|our) hands)\b", re.I)
_DOUBT = re.compile(
    r"\b(?:dont think|do not think|didnt think|not sure|unsure|no idea|dont know|do not know|"
    r"may have|maybe|probably|might|hopefully)\b", re.I)
_GUESSED_RESULT = re.compile(
    r"\b(?:probably|might(?:\s+have|'ve)?|maybe|think(?:ing)?|dont think|do not think|"
    r"not sure|no idea)\s+(?:failed|flunked|bombed|messed up|did badly|"
    r"did (?:rubbish|badly|terribly|awful)|(?:didnt|did not|havent|have not) (?:pass(?:ed)?|get|got)|"
    r"lost it|ruined it)\b", re.I)

_RESOLVED = re.compile(
    r"\b(?:but|and) (?:i|we|he|she|they)\b[^.?!]*\b(?:did|do|does|passed|pass|got|made|rang|rang me)\b|"
    r"\b(?:but|and) it (?:worked|worked out|came through|came back|arrived|landed|turned out|was fine)\b|"
    r"\bturn(?:s|ed) out\b", re.I)
_A_TIME = re.compile(
    r"\b(?:tomorrow|tonight|today|this (?:morning|afternoon|evening|week|weekend|month)|"
    r"next (?:week|month|monday|tuesday|wednesday|thursday|friday|saturday|sunday|term)|"
    r"(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)|"
    r"in (?:a|two|three|four|five|a few|\d+) (?:day|days|week|weeks|month|months)|fortnight|"
    r"end of the (?:week|month)|by (?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)|"
    r"in the (?:morning|afternoon|evening)|any day now|soon|at some point)\b", re.I)


def _an_open_result(clean):
    if _RESOLVED.search(clean):
        return False
    if _WAITING.search(clean):
        return True
    return bool(_RESULT.search(clean) and _DOUBT.search(clean))


_ANSWER_GOOD = re.compile(
    r"\b(?:got\s+(?:it|the\s+(?:job|place|part|role|offer|position)|in)|passed|said\s+yes|"
    r"im\s+in|offered\s+me|accepted|all\s+clear|benign|"
    r"(?:it\s+)?(?:was|is|came\s+back)\s+(?:clear|fine|nothing))\b", re.I)
_ANSWER_BAD = re.compile(
    r"\b(?:said\s+no|was\s+a\s+no|rejected|turned\s+(?:me\s+)?down|didnt\s+get|"
    r"did\s+not\s+get|unsuccessful|failed|no\s+thanks|bad\s+news|not\s+good\s+news|"
    r"was\s+bad|went\s+badly|no\s+luck|cancer|it\s+was\s+inoperable|"
    r"(?:it|that|they)(?:'s|'re|'d|s|re|d|\s+is|\s+are|\s+was|\s+were)?\s+(?:not\s+good|no\s+good|"
    r"not\s+great|bad|rubbish|awful|terrible))\b", re.I)


def _the_news_landed(clean):
    if not _LANDED.search(clean):
        return None
    if _ANSWER_BAD.search(clean):
        return "bad"
    if _ANSWER_GOOD.search(clean):
        return "good"
    return "landed"


def reads_as_a_result_line(text):
    clean = _plain(_matchable(text))
    if not clean:
        return False
    return bool(_the_news_landed(clean) or _an_open_result(clean) or _a_guessed_result(clean))


def _a_guessed_result(clean):
    return bool(_GUESSED_RESULT.search(clean))


def _a_time_in_it(clean):
    return bool(_A_TIME.search(clean))
A_COST = re.compile(r"£\s?\d|\b\d+\s?(?:quid|pounds?|bucks|grand|k)\b|\b(?:costs?|costing|"
                    r"expensive|afford|pricey|a\s+fortune|too\s+much)\b"
                    r"|\b(?:is|are|was|were|costs?|costing|comes?|come\s+to|at|pay|paid|pays"
                    r"|spend|spent|wants?)\s+£?\s?\d{2,}\b", re.I)
SOMEBODY_ASKS = re.compile(
    r"\b(?:want(?:s|ed)?|ask(?:s|ed)?|expect(?:s|ed)?|told|tell(?:s|ing)?)\s+me\s+to\b"
    r"|\b(?:they|he|she|my\s+\w+|his|her|their)\s+want(?:s|ed)?\b"
    r"|\b(?:invited\s+me|asked\s+me|been\s+asked|asking\s+me\s+for)\b", re.I)
A_ROLE_IN_SOMEBODY_ELSES_DAY = re.compile(
    r"\b(?:bridesmaid|maid\s+of\s+honour|best\s+man|godparent|usher|stag\s+do|stag\s+night|"
    r"hen\s+do|hen\s+party|hen\s+weekend)\b", re.I)


def _a_cost_somebody_asks(clean):
    text = " ".join(str(clean or "").lower().split())
    if not text or "?" in text or len(text.split()) > 24:
        return False
    if not A_COST.search(text):
        return False
    if not (SOMEBODY_ASKS.search(text) or A_ROLE_IN_SOMEBODY_ELSES_DAY.search(text)):
        return False
    return not re.search(r"\bmy\s+(?:own\s+)?(?:wedding|holiday|party|trip)\b", text)


DAY_WORDS = {
    "cold": frozenset("""cold freezing chilly bitter baltic parky nippy frost frosty icy ice snow
        snowing snowy sleet slush snap frozen raw perishing taters nithered""".split()),
    "rain": frozenset("""rain raining rains rainy wet pouring drizzle drizzling drizzly showers
        shower chucking tipping pelting bucketing downpour soaked sodden damp mizzle mizzling
        lashing lash hosing drenched drenching soaking soaked-through"""
                     .split()),
    "wind": frozenset("""wind windy gale gales gusty blustery storm stormy squall blowing blow blows
        blowing""".split()),
    "hot": frozenset("""hot boiling scorching roasting sweltering baking heat heatwave muggy humid
        sticky close clammy stifling scorcher sizzling sizzler""".split()),
    "mild": frozenset("""mild milder balmy clement""".split()),
    "fog": frozenset("""fog foggy mist misty haze hazy murk""".split()),
    "grey": frozenset("""grey gray gloomy dull overcast dark dreich dreary murky miserable grim
        cloudy horrible rotten rubbish depressing drizzly""".split()),
    "sun": frozenset("""sun suns sunny sunshine bright clear blue glorious gorgeous beautiful lovely
        nice warm pleasant""".split()),
}
DAY_GLUE = frozenset("""it its it's is are was were be been being feels feel feeling looks look
    looking very really so too quite rather bit a an the this that thats that's there here out
    outside indoors in inside above up down today tonight now still again already at last
    honestly actually just and but or oh ah well ugh eh huh huh its isn't isnt wasn't wasnt what
    such some much more most enough all day days night nights morning mornings afternoon
    afternoons evening evenings week end weather coming for of with to getting got get turned
    s gone going outside one ones not lots load loads plenty ton tons bucket buckets thick heavy
    dense meant due supposed forecast tomorrow later weekend weekends sunday monday tuesday wednesday
    thursday friday saturday next
    innit init aint ay arent aren't no never hardly even though tho anymore
    proper right dead bare bloody damn awful
    rn atm tn 2nite tmoz""".split())
DAY_MET_ME = re.compile(
    r"^(?:i|we|they)\s+(?:got|was|were|am|have been|ve been|waited|stood|queued|walked"
    r"|sheltered)\s+")
DAY_ON_THE_WAY = ("walking in", "walking home", "walking to work", "walking the dog",
                  "on the way home", "on the way in", "on the way to work", "on my way home",
                  "on my way in", "on the school run", "coming home", "going to work",
                  "caught in the", "caught out in the",
                  "on the platform", "at the bus stop", "at the station", "at the stop",
                  "waiting for the bus", "waiting for a bus", "waiting for the train",
                  "waiting for a train", "waiting for my bus", "waiting for my train",
                  "for a bus", "for the bus", "for a train", "for the train")
NEGATIONS = frozenset("""not isnt isn't arent aren't wasnt wasn't aint ain't no never hardly
    nothing""".split())
NEGATION_SOFTENERS = frozenset("that too so even very all at much really quite bit".split())
DAY_AS_ANYTHING = ("as anything", "as hell", "as can be", "as ever", "as fuck", "as all hell")
DAY_SAID_AS_A_KIND = (("brass monkeys", "freezing"), ("brass monkey", "freezing"))


DAY_TO_COME = frozenset("""meant due supposed forecast tomorrow later weekend weekends sunday
    monday tuesday wednesday thursday friday saturday next""".split())
DAY_TO_COME_PHRASES = ("going to", "meant to", "due to", "supposed to", "forecast", "to come",
                       "on its way")
DAY_TO_COME_PAST = ("was meant to", "were meant to", "was supposed to", "were supposed to",
                    "was due to", "were due to")
DAY_VERDICTS = frozenset("""rubbish horrible rotten miserable grim gloomy dreary depressing dull
    dreary lovely gorgeous beautiful nice glorious pleasant dreich joyful""".split())
DAY_ASKS = frozenset("""is are was were do does did can could will would should shall have has had
    may might how what when where why who which""".split())
DAY_THEIR_OWN_DAY = frozenset("""been spent spend sat stood had i im i'm ive i've we weve we're""".split())
DAY_NOT_THE_DAY = ("all clear", "all done", "all good", "all right", "all set", "all over",
                   "all in", "too warm", "too cold",
                   "out cold", "out for the count")
DAY_JOINED_ON = frozenset("and also plus then but because".split())
DAY_NEEDS_A_DAY_NAMED = frozenset("""grey gray gloomy dull dark clear blue lovely nice pleasant
    miserable depressing grim horrible rotten dreary""".split())
DAY_IN_HERE = ("in here", "in this room", "in my room", "in the house", "in our house",
               "in the flat", "in my flat", "in the kitchen", "in the bedroom", "in the front room",
               "in the living room", "in the office", "in my office", "in the car", "indoors",
               "inside")
DAY_NAMED = frozenset("""out outside outdoors day days weather morning mornings afternoon evenings
    evening night nights today tonight now already week""".split())


def _the_day_described(clean):
    line = " ".join(str(clean or "").lower().split())
    if not line or "?" in line:
        return None
    line = re.sub(r"^what\s+an?\s+", "", line)
    if DAY_MET_ME.match(line):
        line = DAY_MET_ME.sub("", line)
        for phrase in DAY_ON_THE_WAY:
            line = re.sub(r"\b" + r"\s+".join(phrase.split()) + r"\b", " ", line)
        line = " ".join(line.split())
    for phrase in DAY_AS_ANYTHING:
        line = re.sub(r"\b" + r"\s+".join(phrase.split()) + r"\b", " ", line)
    for phrase, word in DAY_SAID_AS_A_KIND:
        line = re.sub(r"\b" + r"\s+".join(phrase.split()) + r"\b", word, line)
    line = " ".join(line.split())
    words = [word.strip(".,!;:'\u2019\"") for word in line.split()]
    words = [word for word in words if word]
    if not words or len(words) > 8:
        return None
    if words[0] in DAY_ASKS or words[0] in DAY_THEIR_OWN_DAY or words[0] in DAY_JOINED_ON:
        return None
    if any(phrase in line for phrase in DAY_NOT_THE_DAY):
        return None
    if any(phrase in line for phrase in DAY_IN_HERE):
        return None
    if not [word for word in words if word in DAY_NAMED or word in DAY_TO_COME]:
        day_words = [word for word in words
                     if any(word in pool for pool in DAY_WORDS.values())]
        if day_words and all(word in DAY_NEEDS_A_DAY_NAMED for word in day_words):
            return None
    known = DAY_GLUE.union(*DAY_WORDS.values())
    if [word for word in words if word not in known]:
        return None
    if any(phrase in line for phrase in DAY_TO_COME_PAST):
        return None
    if any(words[index - 1] == "the" and words[index + 1:index + 2] in (["one"], ["ones"])
           for index, word in enumerate(words)
           if index > 0 and index + 1 < len(words)
           and any(word in pool for pool in DAY_WORDS.values())):
        return None
    day_words = [word for word in words if any(word in pool for pool in DAY_WORDS.values())]
    if ("was" in words or "were" in words) and day_words \
            and all(word in DAY_VERDICTS for word in day_words) \
            and not any(word in DAY_TO_COME for word in words):
        return None
    def ruled_out(index):
        back = index - 1
        while back >= 0 and words[back] in NEGATION_SOFTENERS:
            back -= 1
        return back >= 0 and words[back] in NEGATIONS

    best, best_count = None, 0
    ruled, ruled_count = None, 0
    for kind, pool in DAY_WORDS.items():
        count = sum(1 for index, word in enumerate(words)
                    if word in pool and not ruled_out(index))
        if count > best_count:
            best, best_count = kind, count
        cleared = sum(1 for index, word in enumerate(words)
                      if word in pool and ruled_out(index))
        if cleared > ruled_count:
            ruled, ruled_count = kind, cleared
    if not best:
        if ruled:
            return THE_DAY.get("mild")
        return None
    if any(word in DAY_TO_COME for word in words) \
            or any(phrase in line for phrase in DAY_TO_COME_PHRASES):
        return THE_DAY_AHEAD.get(best) or THE_DAY.get(best)
    return THE_DAY.get(best)
def the_day_remarked(text):
    line = " ".join(str(text or "").lower().split())
    pool = _the_day_described(line)
    if not pool:
        return None
    if re.search(r"\b(?:was|were)\b", line):
        return None
    return pool


DECLINE_ABOUT_THE_BOT = re.compile(r"\b(?:you|u|yours)\s+(?:\w+\s+){0,2}$")
DECLINE_SOMEONE_ELSE = re.compile(
    r"(?:\b(?:the|a|an|my|our|your|his|her|their|this|that|these|those)\s+(?:\w+\s+){0,2}"
    r"|\b(?:he|she|they)\s*)$", re.I)
DECLINE_VERB = re.compile(
    r"\b(?:cant|cannot|can not|couldnt|wont|wouldnt|unable to|"
    r"not (?:going to|gonna) be able to|not able to|"
    r"not going to be able to|not gonna be able to)\s+"
    r"(?:(?:actually|really|even|possibly)\s+)*"
    r"(?:come|make|be there|attend|be able to (?:come|make it|make|be there))\b(.*)$")
DECLINE_MUST = re.compile(
    r"\b(?:have|has|had|ve got|got|going to|gonna|need|needs|will have)\s+to\s+"
    r"(?:cancel|pull out|back out|cry off|drop out)\b(.*)$")
DECLINE_ASK = re.compile(
    r"^(?:how|what|when|where|which|who|why|should|could|would|do|does|did|is|are|will|any)\b")
DECLINE_TIME = re.compile(
    r"\b(?:tonight|today|tomorrow|this (?:evening|afternoon|morning|weekend|week|time|one)|"
    r"next (?:week|weekend|month|time)|"
    r"(?:mon|tues|wednes|thurs|fri|satur|sun)day|weekend|yesterday|on (?:the )?"
    r"(?:mon|tues|wednes|thurs|fri|satur|sun)day|after all)\b")
DECLINE_OCCASION = re.compile(
    r"\b(?:wedding|party|funeral|meeting|interview|appointment|class|lesson|match|game|gig|"
    r"exam|shift|christening|baptism|birthday|service|rehearsal|practice|session|course|"
    r"event|evening|morning|afternoon|night|parents|school|one)\b")
DECLINE_DATE = re.compile(r"\b(?:on|at|by)\s+(?:the\s+)?\d{1,2}(?:st|nd|rd|th)?\b")
DECLINE_OTHER = re.compile(
    r"^(?:up|out|on|down|off|back|home|round|across|along to|into|to terms|near|"
    r"ends meet|sense|sure|do(?:ne)?|the most|a (?:difference|decision|start|point|mess|fuss|"
    r"cake|list|move|change)|money|dinner|tea|breakfast|lunch|supper|the bed|my bed|the tea|"
    r"to the (?:phone|landline|door|doorstep)|the phone|the door|"
    r"it (?:work|stop|go|better|worse|through|happen|home|out|up|down|right|snow|rain|fit|run))\b")
DECLINE_OTHER_SUBJECT = re.compile(
    r"^(?:my|the|our|your|its|it|his|her|their|this|that|these|those|"
    r"he|she|they|dad|mum|mom|brother|sister|son|daughter|kids?)\b")
DECLINE_BE_THERE = re.compile(r"\bbe\s+there$")
DECLINE_AFTER = re.compile(
    r"(?:[\s,]*(?:sorry|im sorry|so sorry|apologies|im afraid|afraid|unfortunately|"
    r"i think|i dont think|this time|this week))+$")
BODY_SAYS_WHY_PHRASE = re.compile(
    r"\bthrowing\s+up\b|\bvomit\w*\b|\bstomach\s+(?:bug|upset)\b|\bd&v\b|"
    r"\bunder\s+the\s+weather\b|\bcoming\s+down\s+with\b|\bcan'?t\s+keep\s+\w+\s+down\b")
BABY_ON_THE_WAY = re.compile(
    r"\b(?:baby|babies|bump|pregnan\w*)\b[^.!?]{0,26}\b(?:due|coming|arriv\w+|induct\w+|"
    r"c-section|overdue|weeks)\b|"
    r"\b(?:contractions?|waters|midwife|health visitor|nursery)\b|"
    r"\b\d{1,2}\s*weeks?\s+(?:gone|pregnant|along)\b")


VERB_PARTICLE = re.compile(r"^\s*(?:in|into|back|out|up|round|along|over|down|home|here|there)\b")


def _the_reason_is_on_the_body(text):
    if not text:
        return False
    words = set(re.findall(r"[a-z']+", text))
    return bool(words & BODY_SAYS_WHY
                or _worry_is_about_the_body(text, words)
                or LATE_NOT_A_TIME.search(text)
                or BABY_ON_THE_WAY.search(text)
                or BODY_SAYS_WHY_PHRASE.search(text))


PLAN_ON_THE_TABLE = re.compile(
    r"\b(?:party|wedding|dinner|restaurant|table|booking|booked|reservation|appointment|"
    r"meeting|interview|gig|concert|cinema|drinks|lunch|brunch|barbecue|bbq|christening|"
    r"funeral|birthday|hen do|stag do|leaving do|catch up|get together|trip|holiday|flight)\b",
    re.I)
LINE_CANCELS = re.compile(r"\b(?:cancel\w*|call(?:ing)? (?:it )?off|called off|drop(?:ping)? out|"
                          r"pull(?:ing)? out|opt(?:ing)? out|back(?:ing)? out)\b", re.I)


def _the_line_cancels(line):
    return bool(LINE_CANCELS.search(str(line or "")))


def _a_plan_on_the_table(memory):
    history = [t for t in (memory.get("turns") or []) if isinstance(t, dict)][-3:]
    for turn in history:
        said = str(turn.get("user") or "")
        if said and PLAN_ON_THE_TABLE.search(said):
            return True
    return False


def _hesitant_news_before(memory, turns=3):
    history = [t for t in (memory.get("turns") or []) if isinstance(t, dict)][-turns:]
    for turn in history:
        said = str(turn.get("user") or "").lower()
        if said and reads_as_bad_news(said):
            return True
    return False


def _a_hard_week(memory):
    return bool(_in_a_loss_thread(memory) or _a_loss_recently(memory) or _hesitant_news_before(memory))


def _the_turn_before_was_a_heavy_one(memory, line=""):
    plain = _plain(line) if line else ""
    if plain and not (_a_declined_plan(plain, without_a_thing=True)
                      and not DECLINE_TIME.search(plain)):
        return False
    if not isinstance(memory, dict):
        return False
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    if not turns:
        return False
    said = str(turns[-1].get("user") or "").strip().lower()
    if not said:
        return False
    try:
        read = understand(said)
    except Exception:
        read = None
    if isinstance(read, dict) and (
            read.get("intent") in ("question", "ask") or read.get("kind") == "question"):
        return False
    note = memory.get("heavy_reply")
    if isinstance(note, dict) and note.get("turn") == len(turns) - 1:
        return True
    if reads_like_a_symptom(said) or _the_reason_is_on_the_body(said):
        return True
    if not isinstance(read, dict):
        return False
    if read.get("intent") == "feeling" and (read.get("polarity") or 0) < 0:
        return True
    return bool(read.get("emotion") or read.get("body"))


def _a_declined_plan(clean, without_a_thing=False):
    line = " ".join(str(clean or "").replace("\u2019", "'").replace("'", "").strip().split())
    if not line or DECLINE_ASK.match(line) or line.endswith("?"):
        return False
    found = None
    for pattern in (DECLINE_VERB, DECLINE_MUST):
        for match in pattern.finditer(line):
            if DECLINE_ABOUT_THE_BOT.search(line[:match.start()]):
                continue
            found = match
            break
        if found:
            break
    if not found:
        return False
    if (_the_reason_is_on_the_body(line[:found.start()])
            or _the_reason_is_on_the_body(VERB_PARTICLE.sub(" ", found.group(1)))):
        return False
    tail = DECLINE_AFTER.sub("", found.group(1).strip(" ,.-!?")).strip(" ,.-!?")
    if not tail:
        return True
    if tail.startswith("for ") and DECLINE_BE_THERE.search(line[:found.end(0) - len(found.group(1))].rstrip()):
        return False
    if found.re is DECLINE_MUST and not DECLINE_TIME.search(tail):
        return False
    if DECLINE_DATE.search(tail):
        return True
    if DECLINE_TIME.search(tail):
        if not DECLINE_OTHER.match(tail) or not DECLINE_OTHER_SUBJECT.match(line):
            return True
    if DECLINE_OTHER.match(tail):
        return False
    if tail in ("it", "there", "along"):
        return True
    if without_a_thing:
        return False
    if tail.startswith(("to ", "for ", "it to ", "it on ", "it for ", "it at ", "it next ")):
        return True
    return bool(DECLINE_OCCASION.search(tail))


def _someone_else_dropped_it(clean):
    line = " ".join(str(clean or "").replace("\u2019", "'").replace("'", "").strip().split())
    if not line or not _a_declined_plan(clean):
        return False
    for pattern in (DECLINE_VERB, DECLINE_MUST):
        for match in pattern.finditer(line):
            if DECLINE_ABOUT_THE_BOT.search(line[:match.start()]):
                continue
            return bool(DECLINE_SOMEONE_ELSE.search(line[:match.start()]))
    return False
NO_WORDS = re.compile(
    r"\b(?:dont|don't|do not|never|can'?t|cannot|cant)\s+"
    r"(?:ever\s+|really\s+|quite\s+|honestly\s+|know\s+)*what\s+to\s+"
    r"(?:say|tell|text|write to)\b"
    r"|\b(?:can'?t|cannot|cant|lost|stuck)\s+(?:for|find)\s+"
    r"(?:(?:the|my|his|her|their|any)\s+)?(?:(?:right|first|proper|good)\s+)?words\b|"
    r"\b(?:lost|losing|at a loss for)\s+(?:my|the|his|her|their)\s+words\b|"
    r"\b(?:lost|struggling|struggle)\s+for\s+words\b", re.I)
NO_WORDS_NOT = re.compile(
    r"\b(?:card|cards|note|notes|letter|letters|email|emails|speech|toast|eulogy|"
    r"write|writing|written|funeral|death|died|dying|passed away|cancer|hospice|"
    r"miscarriage|stillborn|divorce|wedding|birthday)\b", re.I)
NO_WORDS_TO = re.compile(r"\b(?:to|for|about|with|tell|text|txt|ring|call|phone|message)\s+"
                         r"(?:him|her|them|his|their|my|our|the|a)\b", re.I)
NO_WORDS_SHE = re.compile(r"\b(?:him|her|his|hers|them|their|theirs|she|he|they)\b", re.I)
NO_WORDS_CROWD = re.compile(r"\b(?:group|audience|crowd|panel|committee|everyone|whole class|"
                            r"room full|assembly|people)\b", re.I)
NO_WORDS_ONE = re.compile(r"\b(?:him|her|his|hers|she|he)\b", re.I)
NO_WORDS_CARE = re.compile(r"\b(?:doctor|doctors|gp|dentist|nurse|consultant|surgeon|specialist|"
                           r"vet|midwife|health visitor|optician|pharmacist|physio|"
                           r"physiotherapist|therapist|counsellor)\b", re.I)
NO_WORDS_ASK = re.compile(r"\b(?:boss|manager|hr|employer|landlord|landlady|client|customer|"
                          r"team|staff|colleague|interview|appraisal|review|landlord)\b", re.I)


def _no_words(clean):
    if not NO_WORDS.search(clean) or NO_WORDS_NOT.search(clean):
        return None
    if NO_WORDS_ASK.search(clean):
        return NO_WORDS_ASKING
    if NO_WORDS_CARE.search(clean):
        return NO_WORDS_AT_THE_CARE
    if NO_WORDS_TO.search(clean) or NO_WORDS_SHE.search(clean):
        if NO_WORDS_CROWD.search(clean) and not NO_WORDS_ONE.search(clean):
            return None
        return NO_WORDS_SOMEONE
    return NO_WORDS_STUCK


INVITE_TALK = re.compile(r"\b(?:chat|talk|natter|chinwag|catch\s*up|a\s+word|gossip)\b", re.I)
INVITE_OPENER = re.compile(
    r"^(?:(?:so|ok|okay|right|well|hey|hi|oi|and|but|oh|ah|anyway|then|now|er|um|hmm|listen|"
    r"quick|just|actually)\s+)*"
    r"(?:(?:do|would|d)\s+(?:you|u)|(?:are|r)\s+(?:you|u)|you|maybe)?\s*"
    r"(?:fancy|want|like|up\s+for|coming|come|join\s+me|walk\s+with\s+me|"
    r"shall\s+we|should\s+we)\b(.*)$", re.I)
INVITE_COMPANY = re.compile(
    r"^(?:(?:so|ok|okay|right|well|hey|oi|and|but|oh|ah|anyway|then|now|just)\s+)*"
    r"(?:(?:do|would|d)\s+(?:you|u)\s+|(?:are|r)\s+(?:you|u)\s+|you\s+)?"
    r"(?:(?:come|walk|sit)\s+(?:with|along)\b(?:\s*(?:me|us))?|join\s+me\b|"
    r"(?:fancy|want)\s+(?:to\s+)?(?:com(?:e|ing)|tag(?:ging)?)\s+along\b)", re.I)
INVITE_NOT_A_DOING = re.compile(
    r"^(?:know|hear|ask|tell|say|explain|check|bet|guess|see|read|talking|think|be|become|stay|"
    r"leave|go home|try|start|stop|help|mean|happen|me\b|hand|lift|ride|anything|something|"
    r"nothing|a go|a look|a word)\b")
INVITE_WHEN = re.compile(r"^(?:when|if|whether|whenever|unless)\b")


def _an_invitation(clean):
    line = " ".join(re.sub(r"[^a-z0-9 ']+", " ", str(clean or "").lower()).split())
    if not line or len(line.split()) < 2:
        return None
    if set(line.split()) & INVITE_NEVER:
        return None
    if INVITE_COMPANY.match(line):
        return "talk" if INVITE_TALK.search(line) else "go"
    found = INVITE_OPENER.match(line)
    if not found:
        return None
    tail = [w for w in found.group(1).split() if w not in INVITE_FILLER]
    if not tail:
        tail = [w for w in found.group(1).split()
                if w not in ("tonight", "today", "tomorrow", "later", "now", "soon", "after")]
    said = " ".join(tail)
    if not tail or INVITE_NOT_A_DOING.match(said) or INVITE_WHEN.match(said):
        return None
    if all(w in INVITE_PRONOUN for w in tail):
        return None
    if not set(tail) & INVITE_ACTIVITY and not INVITE_TALK.search(line):
        return None
    return "talk" if INVITE_TALK.search(line) else "go"
ONLY_FAR = re.compile(
    ONLY_FRONT + r"(?:(?:somewhere|something|some place|a place|a bit|a little|much|quite|really|"
    r"fairly|more|less|not|too|this|that|thats|that's|which is|its|it's|is)\s+)*"
    r"(?:far|near|nearby|nearer|close|closer|local|walkable|in the area|round the corner)"
    r"(?:\s+(?:away|out|by|enough|either|though|from here|to home|from the \w+))?$", re.I)
ONLY_PRICE = re.compile(
    ONLY_FRONT + r"(?:(?:a bit|much|more|a little|something|somewhere|the|ones?)\s+)*"
    r"(?:cheaper|cheap|pricier|dearer|not too (?:expensive|dear|pricey|much)|budget|affordable|"
    r"free|nothing (?:too )?(?:pricey|dear)|"
    r"(?:under|below|less than|no more than|max|maximum|up to|about|around)\s+"
    r"[\u00a3$\u20ac]?\d+\s*(?:pounds?|quid|grand|k|thousand|dollars?|euros?)?"
    r"(?:\s*(?:or so|ish|max|tops))?|"
    r"[\u00a3$\u20ac]?\d+\s*(?:pounds?|quid|grand|max|or so|ish))$", re.I)
ONLY_TIME = re.compile(
    ONLY_FRONT + r"(?:(?:a bit|much|more|a little|something|somewhere|the|ones?)\s+)*"
    r"(?:quick|quickly|quicker|fast|faster|soon|sooner|later|earlier|not long|no time|"
    r"not too long|in a (?:bit|minute|hour|day|week)|in an? \w+|"
    r"an? (?:hour|minute|day|week|moment|min)|(?:under|below|less than) an? (?:hour|minute|day|week|moment|min)|"
    r"(?:under|below|less than|no more than|max|maximum|up to|about|around|in)\s+"
    r"\d+\s*(?:mins?|minutes?|hours?|hrs?)|"
    r"\d+\s*(?:mins?|minutes?|hours?|hrs?)(?:\s*(?:or so|max|tops))?)$", re.I)
ONLY_EFFORT = re.compile(
    ONLY_FRONT + r"(?:(?:a bit|much|more|a little|something|somewhere|the|ones?)\s+)*"
    r"(?:easy|easier|simple|simpler|no fuss|not much fuss|low effort|minimal effort|"
    r"not too much (?:work|effort|faff)|no faff|quick and easy|nothing (?:fiddly|complicated))$",
    re.I)
ONLY_SIZE = re.compile(
    ONLY_FRONT + r"(?:(?:a bit|much|more|a little|something|somewhere|the|ones?)\s+)*"
    r"(?:small|smaller|big|bigger|tiny|compact|roomy|not too (?:big|small|large)|"
    r"on the small side|on the big side)$", re.I)
NARROW_AXES = (("time", ONLY_TIME), ("price", ONLY_PRICE), ("far", ONLY_FAR),
               ("effort", ONLY_EFFORT), ("size", ONLY_SIZE))
BOUND_SAID = re.compile(
    r"\b(?:under|below|less than|no more than|not more than|at most|max|maximum|up to|within|"
    r"about|around|roughly|only)\s+(?:\d|a\b|an\b|one|two|three|five|ten|twenty|thirty|forty|"
    r"fifty|sixty|ninety|a hundred|half)"
    r"|\b\d|\bhalf an hour\b|\ban hour\b|\ba tenner\b|\ba fiver\b|\ba couple of hours\b",
    re.I)


def the_bound_said(clean):
    line = " ".join(str(clean or "").strip().split())
    found = BOUND_SAID.search(line)
    if not found:
        return ""
    rest = line[found.start():]
    rest = re.sub(r"[^\w\s£$€.,-]", " ", rest).strip(" .,")
    words = rest.split()
    return " ".join(words[:5]).rstrip(" .,")


def reads_as_a_narrowing(clean):
    limits = the_limits_said(clean)
    return limits[0][0] if limits else ""


NARROW_JOIN = re.compile(r"\s*(?:,|&|\band\b|\bplus\b)\s*", re.I)


def the_limits_said(clean):
    line = " ".join(str(clean or "").strip().split())
    if not line or line.rstrip().endswith("?") or len(line.split()) > NARROW_WORDS:
        return []
    parts = [part for part in NARROW_JOIN.split(line) if part]
    if not parts:
        return []
    axes = [_one_axis(part) for part in parts]
    if not all(axes):
        return []
    with_bound = [(axis, part) for axis, part in zip(axes, parts) if the_bound_said(part)]
    without = [(axis, part) for axis, part in zip(axes, parts) if not the_bound_said(part)]
    return with_bound[::-1] + without[::-1]


def _one_axis(line):
    for axis, pattern in NARROW_AXES:
        if pattern.match(line):
            return axis
    return ""


def _names_things_to_choose(said):
    said = str(said or "")
    if not re.search(r"\bor\b", said, re.I):
        return False
    words = said.split()
    named = set()
    for index, word in enumerate(words):
        bare = word.strip(".,;:!?*()\u2014-\u2019'\"")
        if len(bare) < 2 or not bare[0].isupper() or not bare[1:].islower():
            continue
        if index == 0:
            continue
        before = words[index - 1].rstrip()
        if before.endswith((".", "!", "?", ":")) and not before.endswith("..."):
            continue
        named.add(bare)
    return len(named) >= 2


AXIS_SAID = {
    "far": re.compile(r"\b\d+\s*(?:miles?|km)\b"
                      r"|\b(?:nearer|nearby|close by|local|walkable|travel|journey|commute)\b", re.I),
    "price": re.compile(r"[\u00a3$\u20ac]\s?\d|\b\d+\s*(?:pounds?|quid|dollars?|euros?)\b"
                        r"|\b(?:cost|costs|price|prices|budget|afford|spend)\b", re.I),
    "time": re.compile(r"\b\d+\s*(?:min(?:ute)?s?|mins?|hours?|hrs?)\b"
                       r"|\b(?:in|takes?|leave it|for) \d+\b", re.I),
    "effort": re.compile(r"\b(?:easier|simple|simpler|effort|faff|fiddly|elbow grease|hard work)\b",
                         re.I),
    "size": re.compile(r"\b\d+\s*(?:cm|mm|m|inch|inches|ft|feet)\b"
                       r"|\b(?:size|measurements?|width|depth|height|fits?|fitting)\b", re.I),
}
A_FAULT = re.compile(
    r"\b(?:broken|leaking|leaks|leaked|wont|won't|stopped|jam(?:med)?|stuck|blocked|"
    r"smells?|smelling|dripping|drips|dead|fault|faulty|error|blinking|not working|"
    r"isn't working|isnt working|no hot water|no power|tripping|cracked|crack|smashed|dented|"
    r"damaged|torn|ripped|soaked|flooded|not charging|wont charge|seized|"
    r"cutting out|cuts out|cut out|keeps (?:stopping|dying|cutting|freezing|restarting|turning off)"
    r"|dies|dying|freezes|freezing|frozen|sluggish|laggy|super slow|very slow|too slow|so slow"
    r"|slow(?:ed)? (?:down|up)|rattl\w+|noisy|clogged|gunked|corroded|rusty|worn out|"
    r"keeps (?:flashing|beeping|going off)|flashing|beeping|overheating|too hot|smoking|sparking)\b",
    re.I)


def the_answer_to_cut(memory, axis=""):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns:
        return {}
    last = turns[-1]
    if not isinstance(last, dict) or last.get("module") not in NARROW_ANSWERED:
        return {}
    said = last.get("bot")
    if not isinstance(said, str) or len(said.split()) < NARROW_SUBSTANCE:
        return {}
    if said.rstrip().endswith("?"):
        return {}
    if axis:
        raised = AXIS_SAID.get(axis, re.compile(r"(?!)")).findall(said)
        if len(raised) < AXIS_MIN.get(axis, 1) and not _names_things_to_choose(said):
            return {}
    if A_FAULT.search(str(last.get("user") or "")):
        return {}
    return last


LAUGHING = re.compile(
    r"\b(?:laugh(?:ed|s|ing)?|laughter|giggl(?:e|ed|es|ing)|in stitches|"
    r"cracked (?:me|us) up|crackin(?:g)? (?:me|us) up|hilarious|hysterical|"
    r"(?:can'?t|cant|couldn'?t|couldnt) (?:stop|help) laughing|"
    r"wet (?:myself|himself|herself) laughing|"
    r"had (?:a|such a|a right|a proper|the best) laugh|bit of a laugh|"
    r"so funny|funniest thing)\b", re.I)
LAUGHING_AT = re.compile(
    r"\b(?:laugh(?:s|ed|ing)?|giggl(?:e|es|ed|ing)|snigger\w*|snicker\w*|titter\w*|"
    r"a laugh)\s+(?:at|about)\s+(?:me|us|him|her|them|you|my|his|her|their|our|your)\b"
    r"|\b(?:laugh(?:s|ed|ing)?|giggl(?:e|es|ed|ing))\s+(?:when|after|because)\s+i\b"
    r"|\bnot (?:even |that |remotely )?funny\b|"
    r"\b(?:nobody|no one|no-one|nobodys|no ones)(?:'s)? (?:is |was |did |has )?"
    r"(?:laughing|laughed|laugh)\b|\bno laughing matter\b"
    r"|\b(?:could do with|could use|needs?|needed|want(?:s|ed)?|in need of|short of) "
    r"(?:a|a bit of a|a good|a right) laugh\b"
    r"|\bi(?:'m|m| am)\b\s+(?:so |really |very |quite |well |proper )*funny\b", re.I)

FLAT_LINE = re.compile(r"^\W*" + FLAT_LEAD + FLAT_CORE + r"\W*$")
REACTION_LEAD += r"but|ok|okay|bloody|hell|damn|fucking)\s+)*"
REACTION_LINE = re.compile(
    r"^\W*" + REACTION_LEAD + r"(?:" + REACTION_WORD + r")"
    r"(?:[\s,]+(?:and\s+)?" + REACTION_WORD + r"){0,6}\W*$")
REACTION_SIGNS = (
    (REACTION_RELIEF, re.compile(
        r"\b(?:phew|finally|thank (?:god|goodness|heavens|christ|fuck))\b")),
    (REACTION_OUCH, re.compile(
        r"\b(?:ouch\w*|ow+|yikes|eek|oof|yowch|sucks|brutal|awful|terrible|horrible|rough|"
        r"dammit|damn it|bugger|crap|shoot)\b")),
    (REACTION_MISHAP, re.compile(
        r"\b(?:oops|whoops|oh (?:no|dear)|dear me)\b")),
    (REACTION_DISBELIEF, re.compile(
        r"\b(?:seriously|are you serious|you(?:'?re| are)? (?:joking|kidding)|for real|no way|"
        r"no chance|surely|really|honestly|wtf|what the (?:hell|heck|devil|fuck|blazes|dickens)|"
        r"what (?:on|in) (?:earth|the world)|why (?:on|in) (?:earth|the world)|"
        r"get out|you what|"
        r"come on|wow+|woah|whoa|omg|oh my (?:god|word)|blimey|crikey)\b")),
    (REACTION_REPEAT, re.compile(r"\b(?:huh|eh|pardon)\b")),
)


def _the_person_already_said_it(memory):
    said = str(last_user(memory) or "").strip()
    if not said or said.rstrip().endswith("?"):
        return False
    return len(said.split()) >= 4


BABY_LOSS = re.compile(r"\bmiscarriage(?:s)?\b(?! of justice)|\bmiscarried\b|\bstillborn\b"
                       r"|\bstillbirth\b", re.IGNORECASE)


def _a_care_thread_to_leave_alone(memory):
    if _in_a_care_thread(memory) or _in_sudden_loss_thread(memory) or _in_a_loss_thread(memory):
        return True
    return any(baby_loss(said) for said in _the_last_few_lines(memory))


def _the_last_few_lines(memory):
    return [" ".join(str(turn.get("user") or "").lower().split())
            for turn in [t for t in (memory.get("turns") or []) if isinstance(t, dict)][-4:]
            if str(turn.get("user") or "").strip()]


def baby_loss(clean):
    return bool(BABY_LOSS.search(str(clean or "")))


VERDICT_SAID = re.compile(
    r"^\W*" + _VERDICT_LEAD + _VERDICT_DET + r"(?P<noun>" + VERDICT_BAD + r")\b" +
    r"(?:\s+(?:honestly|really|though|today|now|again|here|seriously|mate|man))*\W*$")
VERDICT_BARE = re.compile(
    r"^\W*" + _VERDICT_LEAD + r"(?:a|an|the|right|proper|absolute|total|complete|right old)?\s*"
    r"(?P<noun>nightmare|mess|disaster|shambles|farce|palaver|shower)\W*$")


JOKE_WANTED = re.compile(
    r"\b(?:tell|say|make|give|got|know|another|more|one more)\b[^.]{0,24}"
    r"\b(?:joke|jokes|pun|puns|funny|riddle|limerick|meme)\b|"
    r"\bmake me laugh\b|\bcheer me up\b|\banything funny\b|\bjoke please\b", re.I)


JOKE_UNWANTED = re.compile(r"\b(?:dont|don't|do not|stop|no more|enough|pack it in)\b")


def _the_answer_above_was_a_joke(memory):
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    if not turns:
        return False
    asked = " ".join(str(turns[-1].get("user") or "").lower().split())
    if JOKE_UNWANTED.search(asked):
        return False
    return bool(JOKE_WANTED.search(asked))


def _a_verdict_line(text, memory=None):
    text = " ".join(str(text or "").lower().split())
    found = VERDICT_SAID.match(text)
    if not (found or VERDICT_BARE.match(text)):
        return None
    if found and found.group("noun") == "joke" and memory is not None \
            and _the_answer_above_was_a_joke(memory):
        return None
    return REACTION_OUCH

VERDICT_LINE = re.compile(
    r"^\W*(?:(?:that|thats|that'?s|this|it|it'?s|how|so|very|really|bloody|just)\s+"
    r"(?:is\s+)?)?(?:" + VERDICT_WORD + r")"
    r"(?:\W+(?:isnt\s+it|innit|though|honestly|really|mate|god|ugh))?\W*$"
    r"|^\W*(?:it|it'?s|that|thats|that'?s|this)\s+(?:is\s+)?"
    r"(?:rubbish|pants|crap|a\s+nightmare|a\s+mess|a\s+joke)"
    r"(?:\W+(?:isnt\s+it|innit|though|honestly|really|mate))?\W*$"
    r"|^\W*(?:typical(?:\s+(?:isnt\s+it|innit|that|again|honestly))?|just\s+my\s+luck|"
    r"that\s+figures|figures|sod'?s\s+law|of\s+course\s+it\s+(?:did|was|is)|"
    r"what\s+a\s+(?:pain|hassle|shame|nightmare|joke|mess|headache|letdown))\W*$")
STATE_ABOVE = re.compile(
    r"\b(?:can'?t\s+sleep|cant\s+sleep|not\s+sleeping|no\s+sleep|keep\s+waking|"
    r"hurts?|hurting|ache|aches|aching|sore|in\s+pain|pain\s+in|"
    r"ill|sick|poorly|a\s+temperature|migraine|dizzy|shaking|shivery|"
    r"no\s+energy|worn\s+out|exhausted|knackered|burnt?\s+out)\b")


def a_death_just_said(memory=None):
    for turn in [t for t in ((memory or {}).get("turns") or []) if isinstance(t, dict)][-2:]:
        line = " ".join(str(turn.get("user") or "").lower().split())
        if not line:
            continue
        try:
            if loss.reads_as_loss(line):
                return True
        except Exception:
            continue
    return False


def a_verdict_on_the_person(memory=None):
    for turn in [t for t in ((memory or {}).get("turns") or []) if isinstance(t, dict)][-2:]:
        line = " ".join(str(turn.get("user") or "").lower().split())
        if line and STATE_ABOVE.search(line):
            return True
    return False


WAITING_NEWS = re.compile(
    r"\b(?:wait(?:ing)?\s+(?:\w+\s+){0,4}(?:weeks|months)|on\s+a\s+waiting\s+list|"
    r"months?\s+for\s+(?:the\s+|an\s+|a\s+)?(?:appointment|scan|referral|operation))\b")
JOB_GONE_NEWS = re.compile(
    r"\b(?:lost\s+my\s+(?:job|work|hours)|laid\s+off|made\s+redundant|been\s+(?:sacked|"
    r"fired)|got\s+(?:sacked|fired|let\s+go)|sacked\s+(?:from|on)|let\s+go\s+from)\b")


def _the_last_two_lines(memory=None):
    lines = []
    for turn in [t for t in ((memory or {}).get("turns") or []) if isinstance(t, dict)][-2:]:
        line = " ".join(str(turn.get("user") or "").lower().split())
        if line:
            lines.append(line)
    return lines


def _a_loss_in_the_same_breath(memory=None, lines=()):
    if a_death_just_said(memory) or a_heavy_verdict(memory):
        return True
    for line in lines:
        if HEAVY_ABOVE.search(line):
            return True
        try:
            if (badnews.reads_as_sudden_loss(line) or badnews.reads_as_the_leaving(line)
                    or loss.reads_as_loss(line)):
                return True
        except Exception:
            continue
    return False


def a_wait_with_no_loss(memory=None):
    lines = _the_last_two_lines(memory)
    if not any(WAITING_NEWS.search(line) for line in lines):
        return False
    return not _a_loss_in_the_same_breath(memory, lines)


def a_setback_with_no_loss(memory=None):
    lines = _the_last_two_lines(memory)
    if not any(JOB_GONE_NEWS.search(line) for line in lines):
        return False
    return not _a_loss_in_the_same_breath(memory, lines)


def _the_heavy_pool(memory=None):
    if a_death_just_said(memory):
        return VERDICT_NUMB
    if a_wait_with_no_loss(memory):
        return VERDICT_QUEUE
    if a_setback_with_no_loss(memory):
        return VERDICT_SETBACK
    return VERDICT_HEAVY
GRIEF_ABOVE = re.compile(
    r"\b(?:miss(?:es|ed|ing)?\s+(?:my|his|her|their|our|you|them|him|her|mum|dad|mother|father|"
    r"sister|brother|son|daughter|nan|grandma|grandad|gran|grandpa|friend)|"
    r"crying|cry(?:ing)?\s+(?:myself|a lot)|can'?t\s+stop\s+crying|keep\s+crying|"
    r"griev(?:e|ing)|bereave\w*|heartbroken|wish\s+(?:he|she|they)\s+(?:was|were)\s+(?:still\s+)?"
    r"here|empty\s+without|lonely\s+without|still\s+can'?t\s+believe\s+(?:he|she|they)\s+"
    r"(?:has|have)\s+gone)\b")


def a_heavy_verdict(memory=None):
    for turn in [t for t in ((memory or {}).get("turns") or []) if isinstance(t, dict)][-2:]:
        line = " ".join(str(turn.get("user") or "").lower().split())
        if line and GRIEF_ABOVE.search(line):
            return True
    return False


HAPPENING_NOW = re.compile(
    r"\b(?:right\s+now|just\s+now|as\s+we\s+speak|this\s+minute|right\s+this\s+minute|"
    r"happening\s+now|is\s+having\s+it|are\s+having\s+it|still\s+going\s+on|"
    r"in\s+the\s+next\s+hour|on\s+my\s+way\s+to\s+the\s+hospital)\b")


def a_happening_now(memory=None):
    for turn in [t for t in ((memory or {}).get("turns") or []) if isinstance(t, dict)][-2:]:
        line = " ".join(str(turn.get("user") or "").lower().split())
        if line and HAPPENING_NOW.search(line):
            return True
    return False


VERDICT_POINTS_BACK = re.compile(
    r"^\W*(?:that|thats|that'?s|this|it|it'?s|how|what\s+a|such\s+a|of\s+course\s+it)\b")


def _a_verdict_on_something(text, memory):
    if VERDICT_POINTS_BACK.match(text):
        return True
    try:
        turns = (memory or {}).get("turns") or []
    except Exception:
        return False
    return any(isinstance(turn, dict) for turn in turns)


def _verdict_pool(clean, memory=None):
    text = " ".join(str(clean or "").lower().split())
    if not text or not VERDICT_LINE.match(text) or "?" in text:
        return None
    if memory is not None and not _a_verdict_on_something(text, memory):
        return None
    if isinstance(memory, dict):
        turns = memory.get("turns") or []
        if not any(isinstance(turn, dict) for turn in turns):
            return None
    if re.search(r"\b(?:shame|letdown)\b", text):
        return VERDICT_SHAME
    if re.search(r"\b(?:typical|figures|luck|law|of course)\b", text):
        return VERDICT_LUCK
    if a_verdict_on_the_person(memory):
        return VERDICT_ROUGH
    return VERDICT_ANNOY


def a_heavy_news(memory=None):
    for turn in [t for t in ((memory or {}).get("turns") or []) if isinstance(t, dict)][-2:]:
        line = " ".join(str(turn.get("user") or "").lower().split())
        if not line:
            continue
        if HEAVY_NEWS.search(line):
            return True
        try:
            if badnews.reads_as_the_leaving(line):
                return True
        except Exception:
            continue
    return False


def a_loss_in_the_thread(memory=None):
    if a_heavy_verdict(memory) or a_heavy_news(memory):
        return True
    try:
        if _in_a_loss_thread(memory) or _grief_thread(memory):
            return True
    except Exception:
        return False
    for turn in [t for t in ((memory or {}).get("turns") or []) if isinstance(t, dict)][-2:]:
        line = " ".join(str(turn.get("user") or "").lower().split())
        if not line:
            continue
        if HEAVY_ABOVE.search(line):
            return True
        try:
            if badnews.reads_as_sudden_loss(line):
                return True
        except Exception:
            continue
    return False


def a_verdict_stands_down(memory=None):
    if not memory:
        return False
    try:
        if in_a_safety_thread(memory) or _in_a_loss_thread(memory) or _grief_thread(memory):
            return True
    except Exception:
        return False
    for turn in [t for t in (memory.get("turns") or []) if isinstance(t, dict)][-2:]:
        line = " ".join(str(turn.get("user") or "").lower().split())
        if not line:
            continue
        if HARD_WEEK.search(line) or HEAVY_ABOVE.search(line):
            return True
        try:
            if badnews.reads_as_sudden_loss(line):
                return True
        except Exception:
            continue
    return False


def reads_as_a_verdict(text, memory=None):
    try:
        return _verdict_pool(text, memory) is not None
    except Exception:
        return False


FIRST_TURN_VERDICT = re.compile(
    r"^\W*(?:(?:that|thats|that'?s|this|it|it'?s|how|what\s+a)\s+"
    r"(?:is\s+|was\s+)?(?:so\s+|very\s+|really\s+|bloody\s+|just\s+|proper\s+)?"
    r"(?:tough|hard|rough|grim|annoying|a\s+pain|a\s+shame|a\s+nightmare|a\s+hassle|"
    r"a\s+joke|a\s+mess|frustrating|rubbish|sad|depressing|draining|exhausting|"
    r"a\s+slog|a\s+grind|a\s+bummer))"
    r"(?:\s+(?:going|innit|though|honestly|really|mate|god|ugh|isnt\s+it))?\W*$"
    r"|^\W*(?:typical(?:\s+(?:isnt\s+it|innit|again|honestly))?|just\s+my\s+luck|"
    r"that\s+figures|figures|bloody\s+hell|what\s+a\s+(?:pain|hassle|shame|nightmare|"
    r"joke|mess|headache|letdown))\W*$")


def _reaction_pool(clean, memory=None):
    text = " ".join(str(clean or "").lower().split())
    verdict = _a_verdict_line(text, memory)
    if verdict:
        return verdict
    if FIRST_TURN_VERDICT.match(text) and not ((memory or {}).get("turns") or []):
        return VERDICT_FIRST
    if not text or not REACTION_LINE.match(text):
        return None
    for pool, sign in REACTION_SIGNS:
        if sign.search(text):
            return pool
    if re.fullmatch(r"[\w']*\s*(?:what|pardon)\W*", text):
        if memory is not None and not last_bot(memory):
            return REACTION_REPEAT_FIRST
        return REACTION_REPEAT
    return None
def reaction_line(text, memory=None):
    memory = memory if isinstance(memory, dict) else {}
    clean = " ".join(str(text or "").lower().split())
    pool = _a_verdict_line(clean, memory)
    if not pool:
        return None
    if _a_care_thread_to_leave_alone(memory):
        pool = REACTIONS_CARE
    elif _the_person_already_said_it(memory):
        pool = REACTIONS_SAID.get(pool, pool)
    return _choose(pool, memory, clean)


_SORRY_LEAD = re.compile(
    r"^\W*(?:(?:oh|and|but|so|yeah|yep|ok|okay|well|hi|hey|right|alright|also)\W+)*"
    r"(?:(?:so|very|really)\s+)?(?:sorry|apologies|apologise)\b")


LATE_NOW = re.compile(
    r"\b(?:i'm|im|i am|i'll|ill|i will)\s+((?:so\s+|really\s+|a bit\s+|a little\s+|still\s+|"
    r"definitely\s+|probably\s+|going to be\s+|gonna be\s+|will be\s+|running\s+|be\s+|b\s+)*)"
    r"(?:late|behind)\b"
    r"|^\s*late(?: again)?\b")
LATE_NOT_IT = re.compile(r"\b(?:not|never|n't)\b")
LATE_NOT_A_TIME = re.compile(r"\b(?:period|periods|pregnan\w*)\b")
LATE_ASKS = re.compile(
    r"\b(?:what|how|should i|do i|can i|shall i|what do i say|what should i say|tell my|"
    r"explain|apolog\w*)\b")
DONE_SUBJECT = re.compile(r"\b(?:i|we)\s+(?:just\s+|also\s+|finally\s+|only\s+|actually\s+)?"
                          r"([a-z]+)\b")
TAIL_GRUMBLE = re.compile(
    r"\bnow (?:it|they|that)\b[^.!?]{0,20}?\b(?:smells?|stinks?|worse|broken|leaking|mouldy|"
    r"moldy|damp|still|not)\b", re.I)
TAIL_TROUBLE = re.compile(
    r"\b(?:says?|said|told\s+me|tells\s+me|reckons?|claims?|because)\b[^.!?]{0,30}?\b(?:not|never|"
    r"no|wont|won't|cant|can't|couldnt|couldn't|refus\w*|wrong|missing|lost|broken|damaged|"
    r"cheaper|expensive|late|still|again|failed)\b"
    r"|\bfound\s+(?:it|them|that|out)\b[^.!?]{0,24}?\b(?:cheaper|expensive|broken|wrong|"
    r"damaged|dirty|damp|missing|late|cancelled|canceled|cracked|faulty|empty)\b"
    r"|\b(?:is|was|were|are|isnt|isn't|wasnt|wasn't)\s+(?:not\s+|never\s+)?(?:showing|shown|"
    r"arrived|arriving|working|registered|covered|paid|come\s+through|turned\s+up)\b[^.!?]{0,16}?"
    r"\b(?:not|never|no|still|yet|nothing)\b"
    r"|\b(?:didnt|didn't|hasnt|hasn't|hadnt|hadn't|never)\s+(?:show|shown|arrive|work|come|"
    r"register|turn\s+up|pay|go\s+through)\b", re.I)
TAIL_JOIN = re.compile(r"\b(?:and|then|but|so|because)\b")
TAIL_COMPLAINT = re.compile(
    r"\b(?:not|never|still|yet|again|cold|leaking|dripping|damp|mouldy|moldy|smelly|smells|"
    r"stinks|blocked|stuck|broken|broke|faulty|cracked|dirty|empty|flat|dead|late|slow|"
    r"missing|lost|wrong|worse|cancelled|canceled|refused)\b")
TAIL_ASK = re.compile(
    r"\b(?:what about|what next|what now|what else|how long|how much|how do i|how can i|how should i|"
    r"can i|could i|should i|shall i|do i|does it|will it|will they|is it|is that|are they|"
    r"was it|was that|where do i|when will|when do i|when should|who do i|any idea|any chance|"
    r"do you know|do you think|is there|are there)\b", re.I)


def _a_thing_done(clean):
    return _thing_done_shape(clean) is not None


def _thing_done_shape(clean):
    return _thing_done_scan(clean)[0]


def _thing_done_pool(clean):
    from .fallback_chain import _a_thing_they_regret
    if _a_thing_they_regret(clean):
        return None
    shape, done_verb = _thing_done_scan(clean)
    if not shape:
        return None
    if shape == "going":
        return A_THING_ON
    if shape in ("soon", "at"):
        return A_THING_AHEAD
    if done_verb in GONE_VERB:
        return A_THING_GONE
    if done_verb in BOUGHT_VERB:
        if ALIVE.intersection(clean.split()):
            return None
        if NOT_CHOSEN.intersection(clean.split()):
            return A_THING_SEEN_TO
        return A_THING_BOUGHT
    if done_verb in SEEN_TO_VERB:
        return A_THING_SEEN_TO
    return A_THING_DONE


HARM_AFTER = re.compile(
    r"\b(?:my|his|her|their|the)\s+(?:\w+\s+)?(?:back|knee|knees|shoulder|shoulders|hip|hips|"
    r"ankle|ankles|foot|feet|leg|legs|arm|arms|wrist|hand|hands|chest|stomach|head|neck|"
    r"shin|calf|thigh|elbow|joint|joints|body)\b[^.!?]{0,14}?\bis (?:much |a lot |now )?"
    r"(?:worse|sore|stiff|swollen|aching|playing up)\b")


def _tail_complains(clean):
    joins = list(TAIL_JOIN.finditer(clean))
    if not joins:
        return False
    return bool(TAIL_COMPLAINT.search(clean[joins[0].end():]))


def _thing_done_scan(clean):
    if ("?" in clean or " but " in clean or TAIL_ASK.search(clean)
            or TAIL_GRUMBLE.search(clean) or TAIL_TROUBLE.search(clean)
            or _tail_complains(clean)):
        return None, ""
    if (clean.split() or [""])[0] in QUESTION_OPENERS:
        return None, ""
    if NEGATIVE_LINE.search(clean):
        return None, ""
    if trouble.reads_as_trouble(clean, tuple(re.findall(r"[a-z']+", clean)), clean):
        return None, ""
    if HARM_AFTER.search(clean):
        return None, ""
    if HARM_NAMED.search(clean) or HARM_ON_ME.search(clean):
        return None, ""
    if FEELING_OFF.search(clean) or A_TROUBLE_IN_THE_TAIL.search(clean):
        return None, ""
    text = re.sub(r"\b(?:ive|i've)\b", "i have", clean)
    text = re.sub(r"\b(?:weve|we've)\b", "we have", text)
    text = re.sub(r"\b(i|we)'d\b", r"\1 had", text)
    words = re.findall(r"[a-z']+", text)
    for i in range(len(words) - 1):
        if words[i] not in ("i", "we"):
            continue
        j = i + 1
        while j < len(words) and words[j] in ("just", "also", "finally", "only", "actually",
                                              "have", "had", "been"):
            j += 1
        if j >= len(words) or words[j] not in DONE_VERB:
            continue
        rest = words[j + 1:j + 3]
        if any(w in DONE_NOT_THIS for w in rest):
            return None, ""
        if (words[j] in DONE_ONLY_A_THING
                and any(w in DONE_NOT_A_PERSON for w in words[j + 1:j + 4])):
            return None, ""
        return "done", words[j]
    if words and words[0] in DONE_VERB and not HARM_ANYWHERE.search(clean):
        rest = words[1:3]
        if not any(w in DONE_NOT_THIS for w in rest):
            return "done", words[0]
    went = WENT_AT_IT.search(text)
    if went:
        return "gone", "went"
    did = DID_AT_IT.search(text)
    if did:
        return "gone", "did"
    spent = SPENT_TIME.search(text)
    if spent and spent.group(1) in DONE_ING:
        return "going", spent.group(1)
    been = BEEN_AT_IT.search(text)
    if been and been.group(1) in DONE_ING and TIME_SPAN.search(text):
        return "going", been.group(1)
    at_it = AT_IT.search(text)
    if at_it and (at_it.group(1) in DONE_ING or at_it.group(1) in AT_IT_EXTRA):
        rest = text[at_it.end():]
        if at_it.group(1) in BECOMING and (rest.split() or [""])[0] in BECOMING_STATE:
            return None, ""
        if (_a_thing_after(rest) and not HABIT_TIME.search(rest)
                and not any(word in AT_IT_NOT for word in re.findall(r"[a-z']+", rest))):
            return ("soon" if FUTURE_TIME.search(rest) else "at"), at_it.group(1)
    return None, ""


WENT_AT_IT = re.compile(
    r"\b(?:i|we)\s+(?:just\s+|also\s+|finally\s+|only\s+|actually\s+)?"
    r"(?:have\s+|had\s+|'ve\s+)?went\s+(?:"
    r"for\s+(?:a\s+|an\s+|my\s+|our\s+|the\s+)?(?:run|walk|swim|cycle|ride|hike|jog|"
    r"long\s+walk|length\s+swim|bike\s+ride|day\s+out)\b"
    r"|(?:swimming|running|cycling|walking|hiking|jogging|rambling|shopping)\b"
    r"|to\s+(?:\w+\s+){0,3}?(?:gym|pool|parkrun|class|classes|yoga|pilates|zumba|sauna|"
    r"climbing)\b"
    r")")
DID_AT_IT = re.compile(
    r"\b(?:i|we)\s+(?:just\s+|also\s+|finally\s+|only\s+|actually\s+)?did\s+"
    r"(?:a\s+|an\s+|my\s+|our\s+|the\s+|some\s+|two\s+|three\s+)?"
    r"(?:workout|workouts?|run|session|class|swim|laps?|lengths?|weights|press[- ]?ups|"
    r"yoga|pilates|exercises?|exercise|stretches|set\s+of\s+\w+|\d+\s?k(?:m)?|km|miles?)\b")

FUTURE_TIME = re.compile(
    r"\b(?:today|tomorrow|tonight|later|next\s+(?:week|weekend|month|year|saturday|sunday|monday|"
    r"tuesday|wednesday|thursday|friday)|this\s+(?:weekend|week|evening|afternoon|morning)|"
    r"on\s+(?:saturday|sunday|monday|tuesday|wednesday|thursday|friday))\b")
AT_IT = re.compile(r"\b(?:i'm|im|i am|we're|we are)\s+(?:just\s+|currently\s+|still\s+|now\s+"
                   r"|in the middle of\s+)?(?:re)?([a-z]+ing)\b")
HABIT_TIME = re.compile(
    r"\b(?:every|each)\s+(?:day|week|month|year|morning|evening|weekend|night|"
    r"monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b"
    r"|\b(?:once|twice|three times|four times|\d+ times)\s+a\s+(?:day|week|month|year)\b")


A_TROUBLE_IN_THE_TAIL = re.compile(
    r"\b(?:ran out|run out|run short|havent got|hasnt got|haven't got|hasn't got|so far behind|"
    r"stuck|nightmare|disaster|forever|taking ages|taking so long|drag(?:ging|ged) on|"
    r"junk|clutter|chaos|a mess|in a mess|messy|wont go|wont fit|doesnt fit|dont fit|"
    r"gone wrong|went wrong|broke|broken|snapped|hate it|hate this|give up|giving up|"
    r"struggling|too much for me|killing me|a pain|hard work|no idea what i)\b")
FEELING_OFF = re.compile(
    r"\b(?:dizzy|light-?headed|fumes|faint(?:ed|ing)?|bleeding|nauseous|throwing up|"
    r"cant breathe|can't breathe|blurred vision|heart racing)\b")


def _a_thing_after(rest):
    return any(word not in THING_AFTER and len(word) > 2
               for word in re.findall(r"[a-z']+", rest))


SPENT_TIME = re.compile(r"\b(?:i|we)\s+spent\s+(?:the\s+|all\s+|most of the\s+|my\s+|our\s+)?"
                        r"(?:morning|afternoon|evening|day|weekend)\s+(?:re)?([a-z]+ing)\b")
BEEN_AT_IT = re.compile(r"\b(?:i|we)\s+(?:have\s+|had\s+|'ve\s+)?been\s+(?:re)?([a-z]+ing)\b")
TIME_SPAN = re.compile(r"\b(?:all (?:morning|afternoon|evening|day|weekend)|most of the "
                       r"(?:morning|afternoon|day|evening)|since (?:breakfast|lunch|this morning)|"
                       r"the (?:morning|afternoon|evening) away)\b")


def _done_ing():
    out = set()
    for verb in DONE_VERB:
        stem = verb[:-2] if verb.endswith("ed") else verb
        out.add(stem + "ing")
        out.add(verb + "ing")
        if len(stem) > 2:
            out.add(stem + stem[-1] + "ing")
    out.update(("running", "swimming", "making", "writing", "cutting", "digging", "hanging",
                "building", "sweeping", "freezing", "sitting", "getting", "decorating",
                "repainting", "reorganising", "reorganizing"))
    return frozenset(out)


DONE_ING = _done_ing()

HARM_NAMED = re.compile(
    r"\b(?:pills?|tablets?|paracetamol|ibuprofen|painkillers?|meds|medication|overdosed?|"
    r"dose|wound|blood|bleeding|bled|bleach|ammonia|antifreeze|poison\w*)\b")
A_HURT_MYSELF = re.compile(
    r"\b(?:i|i've|ive)\b\s*(?:just\s+|almost\s+|nearly\s+|really\s+|actually\s+)?"
    r"(?:cut|cutting|hurt|hurting|harm|harmed|harming|burn|burned|burnt|burning|hit|hitting|"
    r"punish|punished|punishing|starve|starved|starving|poison|poisoned|poisoning)\s+myself\b"
    r"(?!\s+(?:a|an|the|some|another|either|neither|one|two|three)\b)")
HARM_ON_ME = re.compile(
    r"\b(?:chopped|sliced|cut|stabbed|burned|burnt|scalded|slashed|gashed|split|hit|knocked|"
    r"chopping|slicing|cutting|stabbing|burning|scalding|slashing|gashing)\b"
    r"[^.!?]{0,20}?\b(?:my|myself)\b[^.!?]{0,16}?"
    r"\b(?:finger|fingers|thumb|hand|hands|arm|arms|leg|legs|foot|feet|toe|toes|wrist|head|"
    r"eye|eyes|knee|face|shoulder|skin|chest|stomach)\b"
    r"|\bi\s+(?:chopped|sliced|cut|stabbed|burned|burnt|scalded|slashed|gashed)\s+myself\b")

KNOCK_ON_ME = re.compile(
    r"\bi\s+(?:just\s+|already\s+|then\s+|also\s+)?(?:hit|dropped|knocked|banged|stubbed|"
    r"trapped|caught|whacked|smashed|slammed|clonked|smacked|bashed|pinched|nipped|grazed|"
    r"scraped|trod|stood)\b[^.!?]{0,26}?\b(?:my|myself)\b[^.!?]{0,18}?"
    r"\b(?:" + KNOCKED_SPOTS + r")\b"
    r"|\bi\s+(?:got|had)\s+(?:my|a)\s+(?:" + KNOCKED_SPOTS + r")\s+"
    r"(?:stuck|caught|trapped|nipped|slammed|squashed|crushed)\b"
    r"|\bi\s+(?:shut|slammed|squashed|crushed)\s+my\s+(?:" + KNOCKED_SPOTS + r")\s+in\b")
A_SPAN_OF_TIME = re.compile(
    r"\b(?:all\s+(?:day|morning|afternoon|evening|week)|for\s+(?:hours|a\s+while|days)|"
    r"hours|again|every\s+day|tomorrow|next\s+week)\b")


def _a_knock_on_oneself(clean):
    if not clean or "?" in clean or " but " in clean:
        return False
    if not KNOCK_ON_ME.search(clean):
        return False
    return not A_SPAN_OF_TIME.search(clean)

WALKED_INTO = re.compile(
    r"\bi\s+(?:just\s+|then\s+)?(?:walked|ran|stepped|bumped|crashed)\s+"
    r"(?:straight\s+|smack\s+|right\s+|bang\s+|head\s+)?(?:into|against|over)\s+"
    r"(?:a|the|my|our)\s+(?:door|doorway|door\s?frame|frame|table|chair|bed|cot|cupboard|wall|"
    r"shelf|shelves|desk|fridge|freezer|sofa|gate|fence|cabinet|worktop|dresser|sideboard|"
    r"stairs|stair|banister|post|beam|radiator|window)\b")


def _a_knock_into_a_thing(clean):
    if not clean or "?" in clean or " but " in clean:
        return False
    return bool(WALKED_INTO.search(clean))


HARM_ANYWHERE = re.compile(
    r"\b(?:back|backs|knee|knees|shoulder|shoulders|hip|hips|ankle|ankles|foot|feet|leg|legs|"
    r"arm|arms|wrist|wrists|hand|hands|chest|stomach|head|neck|thigh|elbow|elbows|joint|joints|"
    r"skin|cut|cuts|wound|wounds|burn|burns|burnt|scab|scabs|graze|grazes|bruise|bruises|"
    r"blister|blisters|blood|bleeding|bled|pain|pains|ache|aches|aching|hurts?|hurting|"
    r"throbbing|swollen|swelling)\b")
FALLEN_PEOPLE = (
    r"i|we|he|she|they|the\s+(?:baby|child|kid|boy|girl|little\s+one|toddler|old\s+lady|old\s+man)|"
    r"(?:my|our|his|her|their)\s+(?:mum|mom|mam|dad|father|mother|son|daughter|child|kid|boy|girl|"
    r"baby|toddler|husband|wife|partner|boyfriend|girlfriend|brother|sister|nan|nana|gran|granny|"
    r"grandad|grandpa|grandma|grandmother|grandfather|cousin|friend|mate|neighbour|neighbor|"
    r"uncle|aunt|nephew|niece|little\s+one|lad|lass)"
    r"|(?:my|our|his|her|their|the)\s+\d+\s*(?:month|week|year)s?\s*old")
MISHAP_FELL = re.compile(
    r"\b(?:" + FALLEN_PEOPLE + r")\b[^.?!]{0,24}?\b(?:fell|rolled|tumbled|toppled|tripped|"
    r"slipped|went|come|came)\s+(?:(?:right|straight|back|clean|smack|flat|head)\s+)?"
    r"(?:over|off|down|from|onto|into|through|out\s+of|on\s+the|down\s+the|off\s+the)\b"
    r"|\b(?:" + FALLEN_PEOPLE + r")\b[^.?!]{0,24}?\b(?:fell|rolled|tumbled|tripped|slipped|"
    r"went)\s+on\s+the\s+(?:stairs|stair|steps|ice|pavement|paving|kerb|curb|path|floor|"
    r"ground|road|decking|tiles|lino|linoleum|concrete|gravel|deck)\b"
    r"|\b(?:" + FALLEN_PEOPLE + r")\b[^.?!]{0,18}?\bhad\s+a\s+(?:bad\s+|nasty\s+|really\s+)?"
    r"(?:fall|tumble|trip)\b"
    r"|\b(?:" + FALLEN_PEOPLE + r")\b[^.?!]{0,18}?\bfell\b(?=\s*(?:[.,!]|$|and\b|but\b))")
MISHAP_UNDERFOOT = re.compile(
    r"\bi\b[^.?!]{0,20}?\b(?:stepped|stood|trod|walked|planted|knelt)\b[^.?!]{0,6}?"
    r"\b(?:on|in(?:to)?)\b[^.?!]{0,6}?"
    r"(?:a|an|some|the|broken|bits\s+of|a\s+bit\s+of|two)\s+(?:nail|nails|glass|needle|needles|"
    r"lego|thorn|thorns|screw|screws|tack|tacks|pin|pins|shard|shards|spike|spikes|drawing\s+pin|"
    r"sharp\s+thing|rusty\s+nail)\b"
    r"|\b(?:got|had)\s+(?:a\s+)?(?:bit\s+of\s+|piece\s+of\s+|shard\s+of\s+)?(?:glass|grit|"
    r"metal|a\s+nail|a\s+thorn)\s+(?:in|into)\s+my\b"
    r"|\b(?:a\s+)?(?:nail|screw|thorn|needle|splinter|bit\s+of\s+glass)\s+(?:went\s+|stuck\s+)?"
    r"(?:through|in(?:to)?)\s+my\b")
SENSE_GONE = re.compile(
    r"\bmy\s+(?:vision|sight|hearing)\s+(?:has\s+|had\s+|suddenly\s+)?(?:gone|went)\b"
    r"|\b(?:went|gone|going)\s+(?:blind|deaf)\b"
    r"|\b(?:cant|cannot|can'?t)\s+see\s+(?:out\s+of|anything\s+out\s+of)\b")
MISHAP_ANYWHERE = re.compile(
    "|".join(("(?:" + MISHAP_FELL.pattern + ")",
              "(?:" + MISHAP_UNDERFOOT.pattern + ")",
              "(?:" + SENSE_GONE.pattern + ")")))


MISHAP_OVER = re.compile(
    r"\b(?:last\s+(?:year|summer|winter|spring|autumn|christmas|month)|years?\s+ago|"
    r"when\s+i\s+was|as\s+a\s+(?:kid|child|teen|youngster|little\s+one)|used\s+to|"
    r"back\s+in\s+(?:the\s+)?(?:day|\d{4}|nineteen|twenty))\b"
    r"|\b(?:nearly|almost|close\s+to)\b"
    r"|\b(?:but|and|though)\s+(?:he|she|they|it|we|i)\s*(?:'?s|re|is|was|were|am)?\s*"
    r"(?:ok|okay|alright|all\s+right|fine)\b"
    r"|\b(?:over|on)\s+(?:my|his|her|their|our|your|the)\s+(?:own\s+)?(?:words|tongue)\b")


def _a_mishap_to_ask_about(text):
    if SENSE_GONE.search(text):
        return True
    if not MISHAP_ANYWHERE.search(text):
        return False
    return not MISHAP_OVER.search(text)


def _a_mishap(clean, words):
    if not clean or "?" in clean or len(words) > 24:
        return False
    if MISHAP_OVER.search(clean):
        return False
    return bool(MISHAP_FELL.search(clean) or MISHAP_UNDERFOOT.search(clean))


NEGATIVE_LINE = re.compile(
    r"\b(?:ruined|wasted|broke|broken|failed|went wrong|couldn'?t|couldnt|didn'?t|didnt|"
    r"forgot|messed|gave up|hate[sd]?|awful|terrible|useless|a waste|nobody|no one|"
    r"horrib\w*|miserab\w*|dreadful|soaked|drenched|freezing)\b")


NOT_ENOUGH = re.compile(
    rf"\b{MYSELF}\s+(?:am\s+)?(?:just\s+|still\s+|really\s+|always\s+)?(?:not|never)\s+"
    rf"(?:\w+\s+){{0,2}}(?:enough|good enough)\b"
    rf"|\bmy (?:{MY_DOING})\s+(?:is|was|isnt|isn'?t|wasnt|wasn'?t)?\s*"
    rf"(?:just\s+|never\s+|still\s+|always\s+)?(?:not\s+)?(?:good\s+)?enough\b"
    r"|\bfeel (?:like )?(?:im|i'?m|i am)?\s*(?:a )?(?:failure|fraud|useless|a waste|"
    r"letting (?:people|everyone|my family) down)"
    r"|\b(?:im|i'?m|i am)\s+(?:such\s+)?(?:a failure|a fraud|useless|a burden|a waste of space)\b"
    r"|\b(?:letting|never there for) (?:people|everyone|my family|everybody) down\b"
    r"|\bbehind (?:everyone|in life|on everything)\b"
    r"|\bwasting my (?:life|time|twenties|thirties|20s|30s)\b"
    r"|\b(?:cant|cannot|can'?t) keep up (?:at|in) (?:work|school|uni|university|college|class|"
    r"my course|my job|my studies)\b"
    r"|\b(?:cant|cannot|can'?t) keep up with (?:everything|it all|the lot|the work|everyone|"
    r"my classmates|the others)\b"
    r"|\b(?:cant|cannot|can'?t) (?:cope|do this anymore)\b")
NO_DIRECTION = re.compile(
    r"\b(?:dont|don'?t|never)\s+know what (?:i\s+)?want\b(?=\s*(?:to do\b|with my life|"
    r"out of|from (?:life|work|mine)\b|$))"
    r"|\b(?:dont|don'?t|never)\s+know what to do\b(?=\s*(?:with my life|with myself|out of|"
    r"from (?:life|work|mine)\b|with the rest of it\b))"
    r"|\b(?:dont|don'?t|never)\s+know what (?:im|i'?m|i am) (?:doing|supposed to be doing)\b"
    r"|\bno idea what (?:im|i'?m|i am) doing\b"
    r"|\b(?:im|i'?m|i am) \d{2} and i (?:still )?(?:dont|don'?t) know\b"
    r"|\b(?:nothing|no plan|no idea) (?:feels|seems) right\b")
LOST_QUESTION = re.compile(
    r"\bwhat (?:am i|im|i'?m) (?:even )?(?:doing|going to do|going to do with myself) with my "
    r"(?:life|time|day|week|twenties|thirties)\b")
NOT_SELF = re.compile(r"\b(?:he|she|they|him|her|them|his|their|my (?:mum|mom|dad|boss|son|"
                      r"daughter|partner|husband|wife|friend|sister|brother|colleague|manager))\b")


DISLIKE_ASKS = (
    "What is it about {thing} that gets you?",
    "Fair enough. What is it about {thing}?",
    "What is it about {thing} you don't like?",
    "{Thing} \u2014 what is it that gets you about it?",
)
DISLIKE_TOO_LONG = 6
DISLIKE_HAS_TWO_HALVES = re.compile(r"\b(?:and|but|because|so|though|although|when|if)\b", re.I)
DISLIKE_TAIL = re.compile(
    r"(?:[\s,]+(?:already|now|too|though|tho|anymore|any\s+more|at\s+the\s+moment|"
    r"right\s+now|so\s+much|that\s+much|these\s+days|all\s+the\s+time|as\s+well|anyway|"
    r"honestly|tbh|btw|lol|ha))+$", re.I)


DISLIKE_OWN = re.compile(r"\b(?:my|our)\b", re.I)
DISLIKE_OWN_SELF = re.compile(r"\bmyself\b", re.I)


def _yours(thing):
    return DISLIKE_OWN.sub("your", DISLIKE_OWN_SELF.sub("yourself", thing))


DISLIKE_WITHOUT_AN_I = re.compile(
    r"^\W*(?:(?:and|but|so|oh|also|well|yeah|yep|ok|okay|right|alright|honestly)\W+)*"
    r"(?:not|n't)\s+(?:(?:really|that|too|2|very|so)\s+)?(?:(?:much|a\s+bit)\s+of\s+)?"
    r"(?:a\s+)?(?:keen|fan|fond)\s+(?:of|on|about|for)\s+(?P<thing>[^?.!]+)$", re.I)
NOT_A_THING_ASKED = frozenset("""it its it's that this these those them him her you me
    everything anything something nothing""".split())


def the_dislike_ask(clean, memory):
    thing = obstacle.the_thing(clean)
    if not thing:
        found = DISLIKE_WITHOUT_AN_I.match(" ".join(str(clean or "").split()))
        if found:
            thing = found.group("thing").strip(" ,.;:-")
            if not thing or thing.lower() in NOT_A_THING_ASKED:
                return None
            thing = DISLIKE_TAIL.sub("", thing).strip(" ,.;:-")
            if not thing or len(thing.split()) > DISLIKE_TOO_LONG:
                return None
            if DISLIKE_HAS_TWO_HALVES.search(thing):
                return None
            thing = _yours(thing)
            options = [frame.format(thing=thing, Thing=thing[:1].upper() + thing[1:])
                       for frame in DISLIKE_ASKS]
            return _choose(options, memory, clean)
    if thing:
        thing = _yours(DISLIKE_TAIL.sub("", thing).strip(" ,.;:-"))
    if not thing or len(thing.split()) > DISLIKE_TOO_LONG:
        return None
    if DISLIKE_HAS_TWO_HALVES.search(thing):
        return None
    options = [frame.format(thing=thing, Thing=thing[:1].upper() + thing[1:])
               for frame in DISLIKE_ASKS]
    return _choose(options, memory, clean)


def _own_feeling(clean):
    if clean.rstrip().endswith("?") or NOT_SELF.search(clean):
        return None
    if NOT_ENOUGH.search(clean):
        return NOT_ENOUGH_REPLY
    if NO_DIRECTION.search(clean):
        return NO_DIRECTION_REPLY
    return None


SUMMONS_ASKS_A_CALL = re.compile(
    r"\b(?:ask|asks|asking|asked|tell|tells|telling|told|want|wants|wanting)\s+me\s+to\s+"
    r"(?:call|ring|phone|get in touch)\b")


def _summons_pool(summons, line=""):
    shape = summons.get("shape") if isinstance(summons, dict) else None
    if shape == "written":
        if SUMMONS_ASKS_A_CALL.search(line):
            return SUMMONS_RANG
        return SUMMONS_WRITTEN
    if shape == "rang":
        return SUMMONS_RANG
    return SUMMONS_SEEN


GRIEVANCE_RECUR = re.compile(r"\b(?:keeps?|kept|always|never|constantly|forever|again|"
                             r"every (?:day|night|morning|week|time|monday|weekend)|all the "
                             r"time|day after day|week after week)\b")
GRIEVANCE_MINE_THINGS = re.compile(r"\b(?:my|our)\s+([a-z']+)")

GRIEVANCE_MINE = re.compile(r"\bi (dont|don't|cant|can't|never|keep|keeps|always|wont|won't|"
                            r"refuse|refused|forget|forgot|cancel|promised)\b")

PROMISE_PEOPLE = (
    r"(?:mum|mom|mother|dad|father|parents|sister|brother|son|daughter|kid|kids|child|children|"
    r"wife|husband|partner|boyfriend|girlfriend|ex|fiance|fiancee|mate|friend|flatmate|housemate|"
    r"lodger|neighbour|neighbor|boss|manager|colleague|coworker|carer|nan|nana|grandma|grandad|"
    r"granny|aunt|uncle|cousin|stepdad|stepmum|landlord|agency|solicitor|builder|plumber|mechanic|"
    r"dealer|garage|contractor|tradesman|workman|electrician|cleaner|tutor|teacher|headteacher|"
    r"social worker|doctor|gp|dentist|nurse|therapist)")
PROMISE_OFFICES = (
    r"(?:council|school|college|university|landlord|letting agent|agent|bank|building society|"
    r"shop|store|company|employer|hr|boss|manager|surgery|gp|doctor|dentist|hospital|clinic|dwp|"
    r"jobcentre|job centre|insurance|supplier|provider|broadband|water company|housing "
    r"association|housing|department|office|service)")
_PROMISE_SAYS = (r"(?:say|says|said|saying|tell|tells|told|telling|swear|swears|swore|swearing|"
                 r"promise|promises|promised|promising)")
_PROMISE_KEEPS = r"(?:keeps?\s+|kept\s+|always\s+|still\s+|just\s+|only\s+)?"
PROMISE_OFFICE = re.compile(r"\b" + PROMISE_OFFICES + r"\b")
PROMISE_A_PERSON_NAMED = re.compile(
    r"\b(?:my|our|his|her|their)\s+(?:[a-z]+\s+){0,2}?" + PROMISE_PEOPLE + r"\b")
PROMISE_REPORTED = re.compile(
    r"\b(?:he|she|they|hes|shes)\s+" + _PROMISE_KEEPS + _PROMISE_SAYS + r"\b"
    r"|\b(?:my|our|his|her|their)\s+(?:[a-z]+\s+){0,2}?" + PROMISE_PEOPLE + r"\s+"
    + _PROMISE_KEEPS + _PROMISE_SAYS + r"\b"
    r"|\b" + PROMISE_OFFICES + r"\s+" + _PROMISE_KEEPS + _PROMISE_SAYS + r"\b"
    r"|\b(?:promise|promises|promised|promising|swear|swears|swore|swearing)\b")
PROMISE_FUTURE = re.compile(
    r"\b(?:will|wont|won't|going to|gonna|next (?:week|month|weekend|time|"
    r"day|year)|tomorrow|soon|later|sometime|eventually|hell|he'll|shell|she'll|theyll|"
    r"they'll|promised|promises?|ring back|call back|get back to me|sort it|do it|"
    r"pay me back|pay it back|take the kids|in the post|by (?:noon|midnight|monday|tuesday|"
    r"wednesday|thursday|friday|saturday|sunday|the end of|christmas|new year|the weekend)|"
    r"end of the (?:week|month)|next few days|after (?:christmas|new year|the weekend))\b")
PROMISE_BUT_NEVER = re.compile(
    r"\b(?:but|and)\s+never\s+(?:does|do|did|comes|came|happens|happened|turns up|shows up|"
    r"pays|paid|rings|rang|calls|called|sorts? it|gets round to it)\b")
PROMISE_NEVER_WHAT = re.compile(r"\bnever does what\b|\bnever follows through\b")
PROMISE_RISK = re.compile(
    r"\b(?:kill|killed|killing|suicide|suicidal|overdose|self.harm|end it|end it all|"
    r"not be here|be dead|die|dying|do it again|do something stupid|take my own life|"
    r"hurt (?:myself|himself|herself|themselves)|cut (?:myself|himself|herself|themselves))\b")
PROMISE_RECUR = re.compile(r"\b(?:keeps?|kept|always|constantly|forever|again|every time|"
                           r"still|never)\b")
PROMISE_NOT_A_PERSON = re.compile(
    r"\b(?:phone|laptop|printer|tv|television|boiler|app|apps|screen|router|computer|tablet|"
    r"washing machine|dishwasher|oven|car|watch|kindle|console|xbox|playstation|alexa|siri|"
    r"fridge|freezer|heating|thermostat|meter)\b")
PROMISE_MONEY = re.compile(
    r"\b(?:pay|pays|paid|paying|owes|owe|owed|owing|loan|lent|borrow|borrowed|rent|bill|bills|"
    r"mortgage|wages|salary|quid|pounds|grand|deposit|invoice|refund|compensation)\b")
PROMISE_A_HE_OR_SHE = re.compile(r"\b(?:he|she|him|his|her|hes|shes)\b")

PROMISE_A_PERSON = (
    "A promise that moves every time is a pattern, not a date. Ask for the day itself, in a "
    "message, so there is something written down - which day, and put it in the calendar - and "
    "believe the answer rather than the intention. What is it they keep putting off?",
    "Stop asking whether it will happen and ask what has happened: one small thing this week, "
    "in writing. A day that slips again is the answer, and it is better to know that before you "
    "count on it. What have you been counting on?",
    "Say it once, plainly, and ask which day they mean: a promise that never gets a day is the "
    "thing worth testing, and testing it is fairer than deciding what they are like. What would "
    "change for you if it actually happened?",
)
PROMISE_AN_OFFICE = (
    "A phone-back that never comes is worth putting in writing: the reference, the day you "
    "asked, and one clear question. The complaints address on their own site is read by "
    "somebody who can answer it, and it leaves a record. What were you waiting on?",
    "Ask by email so it stops being a conversation: what was promised, who said it, and the "
    "day you want it by. That same note is the one a complaint or an ombudsman asks for, so it "
    "is worth writing once. What is the thing they keep not doing?",
    "Ring once more, quote the day they gave you, and ask for the answer in writing: a promise "
    "on the record sits in a different queue from one made on a phone call. When did they first "
    "say it?",
)


def _a_promise_that_keeps_moving(clean):
    reported = PROMISE_REPORTED.search(clean)
    device = PROMISE_NOT_A_PERSON.search(clean)
    if device and (reported is None or device.start() < reported.start()):
        return None
    if PROMISE_MONEY.search(clean) or PROMISE_RISK.search(clean):
        return None
    said = set(re.findall(r"[a-z']+", clean.replace("\u2019", "'")))
    office_subject = (bool(PROMISE_OFFICE.search(clean))
                      and not PROMISE_A_HE_OR_SHE.search(clean)
                      and not PROMISE_A_PERSON_NAMED.search(clean))
    if not office_subject and (said & GRIEVANCE_HEALTH or said & GRIEVANCE_HARM):
        return None
    broken = PROMISE_BUT_NEVER.search(clean)
    if not (PROMISE_NEVER_WHAT.search(clean)
            or (reported and (
                (PROMISE_RECUR.search(clean) and PROMISE_FUTURE.search(clean))
                or (broken and broken.start() > reported.end())))):
        return None
    return PROMISE_AN_OFFICE if office_subject else PROMISE_A_PERSON


DOABLE = re.compile(
    r"\b(?:doable|manageable|easy\s+enough|not\s+too\s+bad|simpler\s+than\s+i\s+thought|"
    r"easier\s+than\s+i\s+thought|that\s+(?:should\s+)?work|worth\s+a\s+(?:go|try)|"
    r"i\s+(?:can|could)\s+do\s+(?:that|it))\b", re.I)
DOABLE_WORDS = frozenset("""
    doable manageable easy enough not too bad simpler easier than i thought think work works
    should worth a go try can could do that thats this its it is sounds sound seems seem looks
    possible a be
""".split())
DOABLE_BREATHERS = frozenset("""
    ok okay alright right yeah yes yep oh ah well hmm so and but then honestly really probably
    definitely be thanks thank you ta cheers please mate
""".split())
DOABLE_NOT = re.compile(
    r"\b(?:pain|ache|hurts?|hurting|bleeding|temperature|bill|bills|debt|rent|money|pay|price|"
    r"cost|boss|mum|dad|husband|wife|partner|son|daughter|kid|kids|child|baby)\b", re.I)
DOABLE_REPLIES = (
    "Good \u2014 the first bit is the whole trick, so do that properly and see how you get on.",
    "That's the way. Shout if a step of it does not make sense once you are in it.",
    "Right. Start with the first part and tell me how it goes.",
)


DOABLE_FOLD = re.compile(r"^(?:what\s+about|how\s+about|and|also|what\s+of|then)\s+", re.I)


def _reads_as_a_judgement(text):
    clean = " ".join(str(text or "").lower().split())
    while DOABLE_FOLD.match(clean):
        clean = DOABLE_FOLD.sub("", clean, count=1).strip()
    if not clean or "?" in clean:
        return False
    words = clean.split()
    if len(words) > 8:
        return False
    if not DOABLE.search(clean) or DOABLE_NOT.search(clean):
        return False
    said = [word.strip(".,!?;:'\u2019") for word in words]
    return all(word in DOABLE_WORDS | DOABLE_BREATHERS for word in said)


def _a_doable(clean, memory):
    if not _reads_as_a_judgement(clean):
        return None
    if not the_advice(memory):
        return None
    return _choose(DOABLE_REPLIES, memory, clean)


def a_doable(text, memory):
    clean = " ".join(str(text or "").lower().split())
    return _a_doable(clean, memory)


def reads_as_a_judgement(text):
    return _reads_as_a_judgement(text)


PLAN = (
    "Good — that sounds like the right next step. Tell me how you get on.",
    "Nice one. Let me know how it goes.",
    "That sounds sensible. Shout if it does not go to plan.",
)

_MEDICINE_WORD = (
    r"\b(?:medication|medications|meds|medicine|medicines|tablet|tablets|pill|pills|"
    r"dose|doses|dosage|insulin|insulin injections|inhaler|inhalers|steroids|antibiotics|"
    r"antidepressants|anticoagulants|blood\s+thinners?|blood\s+pressure\s+tablets|epipen|"
    r"epipens|statins?|beta\s+blockers?|thyroxine|levothyroxine|metformin|warfarin|"
    r"prednisolone|painkillers|sleeping\s+tablets|epilepsy\s+tablets|hormones?|"
    r"prescription|prescriptions|treatment)\b")
_VERB_AT_A_PLACE = (
    r"\b(?:stop|stopping|drop|dropping|cut|cutting|pop|popping|skip|skipping|miss|missing)\b"
    r"(?!\s+(?:at|by|in|on|off|for|to|past|outside)\b)")
_CHANGE_VERB = (
    r"\b(?:quit|quitting|give\s+up|giving\s+up|leave\s+off|leaving\s+off|come\s+off|"
    r"coming\s+off|go\s+off|going\s+off|reduce|reducing|halve|halving|half|halfing|double|"
    r"doubling|increase|increasing|raise|raising|lower|lowering|ditch|ditching|bin|binning|"
    r"knock\s+off|knocking\s+off|wean|weaning|taper|tapering|flush|flushing|switch|switching|"
    r"swap|swapping|change|changing)\b")
_SPLITTING_A_TABLET = re.compile(
    r"\b(?:cut|cutting|split|splitting|break|breaking|halve|halving|half)\b[^.?!]{0,20}"
    r"\b(?:tablets?|pills?|capsules?)\b[^.?!]{0,14}\b(?:in\s+half|in\s+two|in\s+quarters?|"
    r"down\s+the\s+middle)\b"
    r"|\b(?:tablets?|pills?|capsules?)\b[^.?!]{0,14}\b(?:in\s+half|in\s+two|in\s+quarters?)\b",
    re.I)
_AMOUNT = (
    r"\b(?:take|taking|have|having|pop|popping|swallow|swallowing)\s+(?:an?\s+)?"
    r"(?:extra|two|three|four|double|twice|\d+)\b")
PLAN_MEDICINE = re.compile(
    r"(?:" + _VERB_AT_A_PLACE + r"|" + _CHANGE_VERB + r")[^.?!]{0,40}" + _MEDICINE_WORD
    + r"|" + _MEDICINE_WORD + r"[^.?!]{0,30}" + _AMOUNT
    + r"|" + _AMOUNT + r"[^.?!]{0,40}" + _MEDICINE_WORD,
    re.I)
PLAN_MEDICINE_SLOW = re.compile(
    r"\b(?:antidepressants?|steroids?|prednisolone|insulin|blood\s+pressure|blood\s+thinners?|"
    r"anticoagulants?|warfarin|epilep\w*|beta\s+blockers?|statins?|thyroxine|levothyroxine)\b",
    re.I)
PLAN_MEDICINE_REPLY = (
    "Do not change a prescribed dose on your own, even for a week: a pharmacist can tell you "
    "today, free, whether to skip it, take less, take more or come off it, and how slowly to go. "
    "If you have stopped it already and feel unwell, ring 111.",
    "Ask a pharmacist before you change a dose, skip it or come off it, even for a week: they "
    "know whether it is safe and how slowly to do it. If you have stopped it already and feel "
    "unwell, ring 111.",
)
PLAN_MEDICINE_SLOW_REPLY = (
    "Do not change a prescribed dose on your own, even for a week: a pharmacist can tell you "
    "today, free, whether to skip it, take less, take more or come off it, and how slowly to go. "
    "Antidepressants, steroids, insulin, blood pressure tablets and blood thinners are the ones "
    "that cause real trouble stopped suddenly. If you have stopped it already and feel unwell, "
    "ring 111.",
    "Ask a pharmacist before you change a dose, skip it or come off it, even for a week: they "
    "know whether it is safe and how slowly to do it, and antidepressants, steroids, insulin, "
    "blood pressure tablets and blood thinners are the ones that are usually reduced in steps "
    "over weeks. If you have stopped it already and feel unwell, ring 111.",
)
_A_QUALIFIED_PERSON_DOES_IT = re.compile(
    r"\b(?:my|our|the|his|her|their)?\s*\b(?:gp|doctor|dr|consultant|psychiatrist|specialist|"
    r"surgeon|nurse|pharmacist|midwife|psychologist|dietitian|anaesthetist)\b[^.?!]{0,30}"
    r"\b(?:is|are|was|were|has|have|had|keeps|kept|stopping|stopped|reducing|reduced|changing|"
    r"changed|taking|took|wants|wanted|told|said|thinks?|advised|suggested|switched|put)\b",
    re.I)
_A_QUESTION = re.compile(
    r"(?:^\s*(?:can|could|should|shall|would|will|is|are|do|does|did|am|what|how|when|where|"
    r"why|which|who)\b)|\?\s*$", re.I)


def reads_as_a_change_of_medicine(text):
    flat = str(text or "")
    if not PLAN_MEDICINE.search(flat):
        return False
    if _SPLITTING_A_TABLET.search(flat):
        return False
    if _A_QUESTION.search(flat.strip()):
        return False
    return not _A_QUALIFIED_PERSON_DOES_IT.search(flat)


IDIOM_SHY = (
    "Ha — one of those days, then. What happened?",
    "Oh no. Go on, what happened?",
)
IDIOM_GLAD = (
    "Ha — that good? What are you waiting for?",
    "Sounds like a big one. What is it?",
)
PLAN_OPENING = re.compile(r"^(?:ok(?:ay)?|alright|right|so|well|thanks|cheers)?[\s,]*"
                          r"(?:i'?ll|ill|i will|i'?m going to|im going to|i'?m gonna|im gonna|"
                          r"gonna|going to)\s+\w+")
PLAN_NOT_YET = re.compile(r"\b(?:havent|haven't|hasnt|hasn't|aint|ain't|not yet|still to|"
                          r"need to|have to|yet to)\b")
PLAN_NOT = re.compile(r"\b(?:never|not|won'?t|wont|can'?t|cant|don'?t|dont|didn'?t|didnt|"
                      r"shouldn'?t|shouldnt)\b")
THING_SORTED = re.compile(
    r"^(?:(?:ok|okay|alright|right|so|well|yeah|yep|yes|cool|fine|thanks|thank you|"
    r"no worries|anyway|and|but|then|all)\s+)*"
    r"(?:"
    r"(?:i|we|ive|i've|weve|we've)\s+(?:(?:have|had|got|already)\s+)?"
    r"(?:sorted|dealt with|handled|done|did|took care of)\s+"
    r"(?:it|that|this|them|things|everything)(?:\s+out)?"
    r"|(?:its|it's)\s+(?:sorted|done|handled|dealt with)(?:\s+now)?"
    r"|(?:sorted|done|handled|dealt with)\s+(?:it|that|this|them)(?:\s+out)?"
    r")"
    r"(?:\s+(?:now|thanks|thank you|already|ok|okay|alright|then))?[\s.!]*$",
    re.IGNORECASE)


PLAN_IDIOM = re.compile(
    r"\b(?:die|dying|died)\s+(?:of|from)\s+(?:embarrassment|boredom|shame|laughter|excitement|"
    r"cringe)\b"
    r"|\b(?:die|dying|died)\s+laughing\b"
    r"|\bkill(?:ing)?\s+my\s*self\s+laughing\b"
    r"|\b(?:crack(?:ing)?\s+up|wet\s+my\s*self)\b[^.?!]{0,12}\blaughing\b")


PLAN_DECIDED = re.compile(
    r"^(?:ok(?:ay)?|alright|right|so|well|thanks|cheers|anyway|honestly|tbh|yeah)?[\s,]*"
    r"(?:(?:i think|i reckon|i guess|i feel like|maybe|perhaps|probably)\s+)?"
    r"(?:i\s+(?:(?:really|probably|definitely|just|still|actually|honestly|so)\s+)?"
    r"(?:should|ought to|oughta|had better|better)\b|i'?d better\b|id better\b)"
    r"\s+(?!be\b|have\b|hav\b|never\b|not\b|n'?t\b|think\b|hope\b|say\b|know\b|"
    r"imagine\b|expect\b|worry\b|care\b|bother\b)"
    r"(?:probably|really|definitely|just|still|maybe|perhaps|actually|now|then)?\s*"
    r"\w+")


def _plan_reported(clean, mood):
    if mood == "negative" or PLAN_NOT.search(clean) or PLAN_IDIOM.search(clean):
        return False
    return (bool(PLAN_OPENING.match(clean)) or bool(PLAN_DECIDED.match(clean))
            or any(phrase in clean for phrase in PLAN_DONE))


RELATIONSHIP_ENDING = re.compile(
    r"\b(?:leaving|leave|left|walking out on|walk out on|walked out on|divorce|divorcing|"
    r"dump|dumping|dumped|splitting up with|split up with|broke up with|break up with|"
    r"breaking up with|ending it with|end it with|ended it with)\s+" + A_PERSON +
    r"(?=\s*(?:[.!?,;]|$|(?:\s+(?:for good|behind|tomorrow|tonight|next week|this week|finally|now|today))\s*(?:[.!?,;]|$)))")


A_CROWD_SUBJECT = re.compile(
    r"\b(?:everyone|everybody|most people|people|folk|others|no ?one|nobody"
    r"|all (?:of )?my (?:friends|mates|siblings|cousins)|my (?:friends|mates)"
    r"|the people (?:i know|around me|at work|on my course))\b", re.I)
A_MARKER_OF_STANDING = re.compile(
    r"\b(?:owns?|owned|owning|bought|buying|has? bought|have bought"
    r"|married|engaged|settled|sorted|got it sorted|have it sorted|has it sorted|promoted"
    r"|mortgage|kids|children|babies|pregnan\w*|ahead|better than me|more than me"
    r"|further along|further ahead|doing better"
    r"|(?:has|have|got|with)\s+(?:a\s+|an\s+|their own\s+|his own\s+|her own\s+)?"
    r"(?:house|flat|place|mortgage|baby|kids|children|career|job|salary|pension)\b)\b", re.I)
A_PARENT_STILL_THERE = re.compile(
    r"\b(?:mum|mam|mom|dad|mother|father|parents|gran|nan)\b", re.I)
MY_OWN_AGE = re.compile(r"\b(?:my|our) (?:own )?age\b", re.I)
THE_PERSON_IS_THE_SUBJECT = re.compile(r"^\s*(?:i|ive|im|we|weve|were|me)\b", re.I)
AN_ASK_ON_TOP = re.compile(
    r"\b(?:what (?:do|should|can) i do|what would you do|should i|how do i|help me|any advice"
    r"|what now|where do i start|advice)\b", re.I)


def a_comparison_of_standing(clean):
    line = " ".join(str(clean or "").split())
    if not line or "?" in line:
        return False
    if len(line.split()) > 14:
        return False
    if A_PARENT_STILL_THERE.search(line) and re.search(r"\bstill\b", line, re.I):
        return False
    comparison = line
    if THE_PERSON_IS_THE_SUBJECT.match(line):
        turned = re.split(r"(?:,|\band\b|\bbut\b)", line, maxsplit=1)
        if len(turned) < 2:
            return False
        comparison = turned[1]
        if not A_CROWD_SUBJECT.search(comparison):
            return False
    if not A_CROWD_SUBJECT.search(comparison):
        return bool(re.search(r"\bat (?:my|our) age\b", comparison, re.I))
    if AN_ASK_ON_TOP.search(line):
        return False
    if MY_OWN_AGE.search(comparison):
        return True
    return bool(A_MARKER_OF_STANDING.search(comparison))


A_COMPARISON_OF_STANDING = (
    "That kind of comparison always picks the one thing you haven't got. Is it something you "
    "actually want, or is it the being behind that stings?",
    "Other people's lives look tidier from the outside than they are from the inside. What would "
    "you want to be different?",
    "It is easy to feel like the only one not there yet, and most people are a lot less sorted "
    "than they look. What would actually help you right now?",
    "That is a fair thing to feel, and the measuring is doing a lot of the work. What do you want "
    "out of it, apart from the comparison going away?",
    "There is no deadline on any of that, whatever the timeline looks like from where you are "
    "standing. What is the one piece you would want to get to?",
)


def _a_relationship_ending(clean):
    return bool(RELATIONSHIP_ENDING.search(clean))


OUR_HEAVY_TELL = re.compile(
    r"(?:sorry to hear|i'm so sorry|i'm really sorry|that sounds rough|that's a heavy feeling"
    r"|that's a lot to|that sounds exhausting|loneliness is rough|missing someone is the price"
    r"|it's a hard thing to carry|be kind to yourself|i'm glad you said it|you don't have to carry"
    r"|there's no rush to talk about it)")


HAZARD_LINE = re.compile(r"\b(?:fires?|smoke|flames?|gas|fumes?|carbon monoxide|flue|"
                         r"fire brigade|fire service)\b")
NO_RELIEF = re.compile(
    r"\b(?:overdos\w*|poison\w*|swallow\w*|paracetamol|ibuprofen|bleach|antifreeze|"
    r"carbon monoxide|pills|tablets|capsules|stopped breathing|not breathing|isnt breathing|"
    r"no pulse|cpr|cardiac|arrest|unconscious|unresponsive|collaps\w*|hanging|hung|"
    r"electrocut\w*|electric shock)\b")
SHE = frozenset((
    "sister", "mum", "mummy", "mother", "mam", "nan", "nanna", "gran", "granny",
    "grandma", "daughter", "wife", "girlfriend", "aunt", "auntie", "niece", "stepmum",
    "stepdaughter", "stepsister",
))
HE = frozenset((
    "dad", "daddy", "father", "son", "husband", "boyfriend", "brother", "nephew",
    "uncle", "grandad", "grandpa", "granddad", "stepdad", "stepson", "stepbrother",
))
A_PERSON_OF_THEIRS = re.compile(
    r"\b(?:my|our)\s+(?:poor\s+|little\s+|eldest\s+|youngest\s+|old\s+|older\s+|elderly\s+|"
    r"grown\s*up\s+|best\s+|close\s+|work\s+|foster\s+|step\s*)*(?P<who>"
    r"sister|mum|mummy|mother|mam|nan|nanna|gran|granny|grandma|daughter|wife|girlfriend|"
    r"aunt|auntie|niece|dad|daddy|father|son|husband|boyfriend|brother|nephew|uncle|"
    r"grandad|grandpa|granddad|stepmum|stepdad|stepson|stepdaughter|partner|other\s+half|"
    r"friend|mate|flatmate|housemate|roommate|cousin|neighbour|colleague|child|kid|baby)\b",
    re.I)
SELF_IN_DANGER = re.compile(
    r"\b(?:(?:i|ive|im|id)\b[^.?!]{0,24}?\b(?:took|swallow|overdos|od'd|cut|hurt|harm|"
    r"kill|suicid|die|dying|dead|end\s+it|hang|hung|jump|pills|tablets|starving|starve)|"
    r"myself\b|\bmy\s+own\s+(?:life|body|head))", re.I)
SOMEBODY_HURT_ME = re.compile(
    r"\b(?:hit|hits|hitting|beat|beats|beating|punch(?:ed|es|ing)?|kick(?:ed|s|ing)?|"
    r"slap(?:ped|s|ping)?|push(?:ed|es|ing)?|shov(?:ed|es|ing)|grab(?:bed|s|bing)?|"
    r"drag(?:ged|s|ging)?|strangl(?:ed|es|ing)|chok(?:ed|es|ing)|threaten(?:ed|s|ing)?|"
    r"abus(?:e|es|ed|ing)|assault(?:ed|s|ing)?|rap(?:e|ed|es|ing)|grope[sd]?|"
    r"burn(?:ed|t|s)|scald(?:ed|s|ing)|hurt|hurts|hurting|harm(?:ed|s)|attacked|"
    r"lock(?:ed|s)\s+(?:me|us)\s+(?:in|out))\s+(?:me|us)\b", re.I)
A_PRONOUN_FOR_SOMEBODY = re.compile(
    r"\b(?:he|she|they|him|her|his|their|hes|shes|theyd|theyll|theyre|they've)\b", re.I)

ADVICE_LENGTH = 180
ADVICE_LENGTH_BARE = 120
ADVICE_CUE = re.compile(
    r"\b(?:go easy|take it easy|take it steady|rest|see someone|see (?:your|a) (?:gp|doctor)|"
    r"get it looked at|looked at|worth (?:a|an|seeing|asking|ringing|going|getting|trying)|"
    r"say so to (?:a|your) (?:gp|doctor)|talk to (?:a|your) (?:gp|doctor)|"
    r"tell (?:a|your) (?:gp|doctor|pharmacist)|ask (?:a|your) (?:gp|doctor|pharmacist)|"
    r"ring (?:your|the|us|back|111|999|nhs)|phone (?:your|the|111|999)|make an appointment|"
    r"book (?:an?|your|it)|carry on|keep (?:going|doing|it|walking|an eye|taking|using)|"
    r"try (?:a|an|the|it|this|that|putting|going|starting|taking|walking|keeping)|"
    r"start with|stop (?:it|there|and|doing)|"
    r"leave it (?:off|alone|a)|check (?:the|it|your|whether|that)|top (?:it|the) up|"
    r"apply|cover it|elevate|keep it|write (?:it|down|a|the)|make a note|note down|"
    r"ask (?:for|about|your|the|whether|what)|change one thing)\b")


def _advice_in(last):
    return len(last) >= ADVICE_LENGTH or bool(ADVICE_CUE.search(last.lower()))


IRREGULAR_STEP = {
    "took": "take", "made": "make", "put": "put", "left": "leave", "kept": "keep",
    "set": "set", "cut": "cut", "held": "hold", "stood": "stand", "gave": "give",
    "got": "get", "ran": "run", "brought": "bring", "sent": "send", "found": "find",
    "told": "tell", "did": "do", "dug": "dig", "hung": "hang", "stuck": "stick",
    "bled": "bleed", "tore": "tear", "wore": "wear", "lit": "light",
    "burnt": "burn", "swept": "sweep", "wrung": "wring", "shut": "shut",
    "spun": "spin", "went": "go", "saw": "see", "drew": "draw",
}
REPORT_VERDICT_WORD = frozenset((
    "fine", "sorted", "clean", "cleaner", "clear", "cleared", "working", "worked", "works",
    "fixed", "ok", "okay", "normal", "done", "gone", "better", "worse", "good", "great",
    "brilliant", "perfect", "results",
))
NO_STEP = frozenset()


def _the_words_in(advice):
    if not advice:
        return NO_STEP
    said = set(re.findall(r"[a-z']+", str(advice).lower()))
    if not said:
        return NO_STEP
    words = set(said)
    for word in said:
        if len(word) < 3:
            continue
        if word.endswith("ing") and len(word) > 4:
            stem = word[:-3]
            words.add(stem)
            words.add(stem + "e")
            if stem[-1:] == stem[-2:-1]:
                words.add(stem[:-1])
    forms = set(words)
    for word in words:
        if not word:
            continue
        forms.add(word + "ed")
        forms.add(word + "d")
        forms.add(word + word[-1] + "ed")
    for past, base in IRREGULAR_STEP.items():
        if base in words:
            forms.add(past)
    return forms


REPORT_NOW_FINE = re.compile(
    r"\b(?:now|already)\s+(?:its|it'?s|it is|they'?re|they are|things are|everything is)\s+"
    r"(?:all |much |a lot |so |loads |back to )?"
    r"(?:fine|sorted|clean|clear|working|fixed|fixed itself|ok|okay|normal|done|gone|"
    r"better|improved)\b"
    r"|\b(?:it|that|this) (?:worked|did it|did the trick|has done it|is sorted)\b"
    r"|\b(?:sorted|fixed) (?:now|already)\b"
    r"|\b(?:its|it'?s|it is|they'?re|they are|things are)\s+"
    r"(?:all |much |a lot |so |loads )?"
    r"(?:fine|sorted|clean|clear|working|fixed|ok|okay|normal|done|gone|better|improved)"
    r"\s+(?:now|again|already)\b")
WORSE_NOW = (
    r"\b(?:now|already)\s+(?:its|it'?s|it is|they'?re|they are|things are|everything is)\s+"
    r"(?:much |even |far |loads |a lot |so |still )?(?:worse|sorer)\b"
    r"|\b(?:much |even |a lot |far )?(?:worse|sorer)\s+(?:now|already|than before)\b"
    r"|\b(?:got|gets|getting|gone)\s+(?:much\s+|even\s+|a\s+lot\s+)?worse\b")
TRIED_WORSE = re.compile(
    r"\b(?:made (?:it|things|me) (?:worse|sorer)|made me worse)\b|" + WORSE_NOW)
TRIED_NO_CHANGE = re.compile(
    r"\b(?:(?:not|isnt|isn't|not really) (?:helping|helped|working|worked)|"
    r"none of (?:that|it|them|these) (?:has |have )?(?:worked|works|helped|helps|done anything|"
    r"been any use|is working|are working)|"
    r"(?:did not|didnt|didn't|does not|doesnt|doesn't|wont|won't) (?:work|help|"
    r"do (?:it|anything|much))|"
    r"(?:hasnt|hasn't) (?:helped|worked)|no (?:change|difference|better|improvement)|"
    r"still the same|same as before|nothing (?:works|is working|has worked|has changed|"
    r"changed|yet|different|so far))\b")
STILL_THE_TROUBLE = re.compile(
    r"\bstill\b(?![^.?!]*\b(?:working|works|helping|helped|better|fine|good|sorted|"
    r"doing the trick)\b)")
TRIED_HELPED = re.compile(
    r"\b(?:(?:it|that|this|they)s? (?:is |are |seems? )?"
    r"(?:actually |really |definitely |properly |still )?(?:helping|helped|working|works|"
    r"help a bit|doing the trick)|helped (?:a (?:bit|little|lot|load))|"
    r"(?:a bit|lots|much|loads) better|feeling better|helps a bit)\b")
TRIED_IT = re.compile(
    r"\b(?:(?:i|we|ive|i've|weve|we've|i have|we have|i had|we had) "
    r"(?:did|tried|gave|used|started|have tried|had tried|went with) "
    r"(?:what you (?:said|suggested)|that|this|it)" + WHOLE_LIST_AFTER +
    r"|did what you (?:said|suggested|told me)|"
    r"(?:been|keep|still) (?:doing|trying|taking|walking|using) (?:it|that|this|them))\b")
TRIED_THAT_ONLY = re.compile(
    r"^(?:(?:ok|okay|alright|right|so|well|yeah|yep|yes|cool|fine|and|but|then|i|we|ive|i've|"
    r"weve|we've)\s+)*"
    r"(?:(?:have|had)\s+)?(?:tried|been trying)\s+(?:it|that|this|them)" + WHOLE_LIST_AFTER + r"\b")
from .fallback_words import (
    ADVICE_AGAIN_ASK,
    ADVICE_COOL_ASK,
    ADVICE_TIME_ASK,
    ADVICE_TIME_WORDS,
    ADVICE_WORSE_ASK,
    AN_ANSWER_ABOUT_A_NO,
    ASKS_WHY,
    BURN_ASK,
    BURN_BLISTER_LINE,
    BURN_ON_IT,
    BURN_THING,
    BURN_WORD,
    CARE_SEEN_ASKS,
    DONE_IT,
    FEELS_BETTER,
    FEELS_NOT_BETTER,
    HYPOTHETICAL,
    IN_HOSPITAL,
    MEDICAL_PLACE,
    MOVE_ON,
    NOT_A_VISIT,
    OWN_NO,
    POP_A_BARE_IT,
    REFUSED,
    REFUSED_FAMILY,
    REFUSED_NOT,
    REFUSED_NO_OBJECT,
    REFUSED_PARTY,
    STILL_GOING,
    TRIED_THE_LOT,
    VISIT_ASK,
)



def _asks_about_the_advice(clean, last):
    if ADVICE_COOL_ASK.search(clean) and any(word in last for word in ADVICE_COOL_WORDS):
        return ADVICE_COOL
    if not ADVICE_TIME_WORDS.search(last):
        return None
    if ADVICE_WORSE_ASK.search(clean):
        return ADVICE_WORSE
    if ADVICE_TIME_ASK.search(clean):
        return ADVICE_TIME
    if ADVICE_AGAIN_ASK.search(clean):
        return ADVICE_AGAIN
    return None


ARRIVING = re.compile(
    r"\b(?:neighbou?rs?|nurse|doctor|paramedic|ambulance|crew|flatmate|housemate|mate|friend|"
    r"sister|brother|mum|mom|dad|mother|father|carer|midwife|police|son|daughter|wife|husband|"
    r"partner|boyfriend|girlfriend|aunt|uncle|cousin|gran|nan|grandad|grandma)\b")
WITH_YOU = re.compile(
    r"\b(?:(?:is|are|was|were)\s+with\s+me|(?:is|are)\s+here|come\s+over|coming\s+over|"
    r"come\s+round|coming\s+round|on\s+(?:his|her|their|its)\s+way|on\s+the\s+way|"
    r"not\s+on\s+my\s+own|not\s+alone|sitting\s+with|staying\s+with|staying\s+tonight|"
    r"staying\s+the\s+night|next\s+door|neighbours?\s+(?:is|are|coming|here))\b")


def _feels_better(clean):
    if not FEELS_BETTER.search(clean) or FEELS_NOT_BETTER.search(clean):
        return False
    if "?" in clean or MOVE_ON.search(clean):
        return False
    for word in re.findall(r"[a-z']+", clean):
        if word in EASING_FILLER or word in SYMPTOM_WORDS or word in BODY_PARTS \
                or word in HEALTH_WORDS:
            continue
        return False
    return True


ROUTE_NAMED = re.compile(
    r"\b(?:999|911|112|111|a\s?&\s?e|a and e|accident and emergency|ambulance|paramedic|"
    r"urgent care|out of hours|x-ray)\b")


def _no_relief(memory, last=""):
    lines = [str(last or "")]
    for past in (memory.get("turns") or []):
        if isinstance(past, dict):
            lines.append(str(past.get("user") or ""))
            lines.append(str(past.get("bot") or ""))
    if any(NO_RELIEF.search(line.lower()) for line in lines if line):
        return True
    for past in (memory.get("turns") or []):
        if not isinstance(past, dict):
            continue
        said = str(past.get("bot") or "")
        if any(word in said.lower() for word in CRISIS_WORDS):
            continue
        opening = re.split(r"(?<=[.?!])\s", said.strip(), 1)[0].lower()
        if opening and ROUTE_NAMED.search(opening):
            return True
    return False


def _someone_is_arriving(clean):
    if WITH_YOU.search(clean):
        return True
    return bool(re.search(r"\b(?:come|coming|let)\s+(?:in|round)\b", clean)
                and ARRIVING.search(clean))

RESOLVED = re.compile(
    r"\b(?:it's|its|it is|that's|thats|that is|this is) (?:out|over|stopped|fine|done|ok|okay|"
    r"under control|settled)\b"
    r"|\bthe \w+ (?:is|has|have|'s) (?:out|stopped|arrived|come|came|gone|cleared|dried up|"
    r"here)\b"
    r"|\b(?:ambulance|paramedics?|fire brigade|fire service|firemen|crew|doctor|nurse|police|"
    r"medics?) (?:is|are|'s|have|has) (?:here|arrived|come|came|been|on the scene)\b"
    r"|\b(?:(?:i'm|im|i am|we're|were|we are|she's|shes|she is|he's|hes|he is|they're|theyre|"
    r"they are|you're|youre|you are) (?:ok|okay|safe|fine|alright|better|out of it))\b"
    r"|\b(?:bleeding|bleed|fire|smoke|pain|it) (?:has |'s )?stopped\b")
NEEDS_SEEN = re.compile(
    r"\b(?:open|gaping|gapes|deep|swollen|swelling|infected|numb|dizzy|hurting|hurts|"
    r"throbbing|worse|getting worse|pus|red streaks)\b")
ALREADY_RANG = re.compile(
    r"\b(?:i|we|ive|i've|weve|we've|he|she|they|dad|mum|mom)\s+(?:have\s+|has\s+|already\s+)?"
    r"(?:rang|called|phoned)\b"
    r"|\brang (?:them|999|911|112|an ambulance|the ambulance)\b")
A_HELPLINE = re.compile(
    r"\b(?:samaritans|116\s?123|988|crisis (?:line|text|team|service|number)|helpline|help line|"
    r"shout|papyrus|nhs\s?111|111|doctor|gp|surgery|out of hours|vet)\b")
ABOUT_THE_SPEAKER = re.compile(r"\b(?:i|i'm|im|i am|i've|ive)\b")
FRIGHTENED = re.compile(
    r"\b(?:scared|afraid|frightened|terrified|fear|fearful|panicking|panic|shaking|shaken|"
    r"trembling|dreading|dread|shocked|in shock|crying|in tears)\b")
NOT_FRIGHTENED = re.compile(
    r"\b(?:not|never|no|nothing|isn't|isnt|aren't|arent|wasn't|dont|don't|doesn't)\b"
    r"(?:\s+\w+){0,3}\s+(?:scared|afraid|frightened|terrified|fear|panicking|panic|shaking|"
    r"trembling|shocked|crying)\b")
CALL_THEM_NOW = re.compile(
    r"\b(?:ring|call|phone|dial)\b(?:\s+\w+){0,3}\s*(?:999|911|112|an ambulance|the ambulance|"
    r"emergency services|the emergency services)\b")
STAKES_WORDS = re.compile(
    r"\b(?:blood ?thinners?|warfarin|apixaban|rivaroxaban|dabigatran|edoxaban|clopidogrel|"
    r"heparin|anticoagulants?)\b"
    r"|\b(?:i'?m|im|hes|he'?s|shes|she'?s|my (?:mum|dad|mother|father|husband|wife|partner|"
    r"gran|grandma|grandad|grandpa|nan))\s+(?:7|8|9)\d\b"
    r"|\b(?:7|8|9)\d\s*(?:years? old|years|yo)\b"
    r"|\b(?:can'?t|cannot|can not)\s+(?:put\s+)?(?:any\s+)?weight\b"
    r"|\b(?:confused|not with it|passed out|knocked out|blacked out|unconscious)\b"
    r"|\b(?:hurts?|agony|killing me|painful)\b[^.]{0,25}\b(?:stand|standing|walk|walking|"
    r"step|stepping|put weight)\b", re.I)
FALL_FIRST_AID = re.compile(
    r"\b(?:put weight|cannot get up|can'?t get up|hit (?:their|your|his|her) head|"
    r"head injury|fell|fall|bruising)\b", re.I)
CARE_WORDS = frozenset("""
    safe safely unsafe outside out stairs stair lift door window smoke fire fires flame flames
    alarm spread spreading burn burned burning bleed bleeding blood cut cuts wound bandage
    dressing plaster pain painful hurt hurts hurting aching sore tender stinging smarting
    stiff swollen swelling bruised numb infected infection throbbing
    aspirin paracetamol ibuprofen painkiller painkillers antihistamine
    worse still soak soaking soaked wait waiting
    ambulance paramedic police operator emergency 999 911 112 doctor hospital nurse gp
    stitches stitch tetanus dressing nurse nhs walk-in centre clinic
    checked check conscious breathing breath awake faint dizzy vomit vomiting sick throwing
    collapsed collapse seizure stroke heart chest epipen inhaler insulin medicine dose
    cpr defib firefighter neighbour neighbor flat floor basement roof shaken shaking scared he she him
    her them they their there call calling rang ring
""".split())
CARE_HURTS = frozenset("""
    sting stings stinging stung throbs throbbing throbbed ache aches aching ached sore tender
    hurts hurting hurt pain painful swollen swelling bled blister blistered blisters
""".split())
CARE_POINTER = frozenset("""
    there call calling rang ring still wait waiting check checked out outside
""".split())
_POINTER_OWN_OBJECT = re.compile(
    r"\b(?:get|gets|getting|got|gotten|opt|opts|opting|opted|back|backs|backing|come|comes|"
    r"coming|came|pull|pulls|pulling|pulled|drop|drops|dropping|talk|talks|talking|talked|"
    r"sign|signs|signing|signed|wriggle\w*|wiggle\w*)\s+(?:me\s+|myself\s+)?out\s+of\s+"
    r"(?!(?:it|them)\b)"
    r"(?!(?:this|that|these|those|there|here)\b\s*(?:$|[,.?!]))"
    r"(?!(?:(?:a|an|the|my|our|your|his|her|their)\s+)?(?:house|home|flat|building|block|"
    r"room|kitchen|bathroom|bedroom|bed|bath|car|van|vehicle|lift|elevator|water|door|way)\b)",
    re.I)
HOUSE_FAULT = re.compile(
    r"\b(?:door|doors|window|windows|hob|oven|cooker|fridge|freezer|"
    r"washer|washing machine|dishwasher|boiler|radiator|tap|toilet|sink|cupboard|drawer|"
    r"handle|hinge|lock|seal|fan|element|shelf|stairs|stair|step|blind|shutter)\b"
    r"(?:\s+\S+){0,3}?\s+"
    r"(?:(?:doesnt|does not|dont|do not|wont|will not|isnt|is not|not)\s+"
    r"(?:shut|shuts|shutting|close|closes|closing|open|opens|opening|work|works|working|"
    r"fit|fits|fitting|lock|locks|locking|stay|stays|staying|sit|sits|properly|right)"
    r"|is\s+(?:broken|busted|jammed|stuck|loose|snapped|cracked|hanging)"
    r"|has\s+(?:snapped|come off|fallen off))"
    r"|\b(?:does|do)\s+(?:the|that|this|my|our)\s+(?:\w+\s+){0,2}"
    r"(?:door|window|hob|oven|cooker|fridge|freezer|tap|toilet|sink|cupboard|drawer|"
    r"handle|lock|shelf|stairs)\s+(?:shut|close|open|work|fit|lock)\b",
    re.I)
CARE_ASKS = re.compile(
    r"\b(what|where|who) (do|should|can) (i|we) (do|go|ring|call|use|tell)\b"
    r"|\bis (it|he|she|that) (safe|ok|okay|normal|bad)\b"
    r"|\bhow (do|can) i (help|stop|treat)\b")
STILL_HERE = re.compile(
    r"\b(?:can|could|do|did)\s+(?:you|u)\s+(?:hear|see|read|understand|get)\s+(?:me|this)\b"
    r"|\b(?:are|r)\s+(?:you|u)\s+(?:still\s+)?(?:there|here|with\s+me|listening|awake)\b"
    r"|\byou\s+(?:still\s+)?(?:there|listening)\b"
    r"|\banyone\s+there\b")


def _is_presence_check(clean):
    match = STILL_HERE.search(clean)
    if not match:
        return False
    rest = re.findall(r"[a-z']+", clean[:match.start()] + " " + clean[match.end():])
    return len(rest) <= 2 and all(word in PRESENCE_LEFTOVER for word in rest)


RECALL_TAIL = re.compile(
    r"\bwhat (?:i|we) (?:told|said|asked|mentioned|wanted|needed)\b"
    r"|\bat the (?:start|beginning|outset)\b"
    r"|\bearlier\b|\bso far\b|\bwhen we (?:started|began|were)\b"
    r"|\bhow (?:this|we|the chat|it) (?:started|began)\b"
    r"|\bwhat i (?:was|have been) (?:on about|talking about)\b")

def _the_store_takes_it(clean):
    from ..modules.memory_store import FIRST_ASK

    return FIRST_ASK.search(clean) is not None


GOOD_AT_ASK = re.compile(r"\bwhat are you\s+(?:good|best)\s+at\b")
CLOTHES_ASK = re.compile(r"\bwhat are you\s+(?:wearing|going to wear|putting on)\b")
LIKE_ASK = re.compile(r"\bwhat are you\s+(?:like|like then|like as a (?:bot|program))\b")
WHAT_ARE_YOU_NOUN = re.compile(
    r"\bwhat are you\s*,?\s*(?:a\s+(?:bot|robot|ai|chatbot|person|human|program(?:me)?)\b)|"
    r"\bwhat are you\s+(?:made|built|running|based)\s+(?:of|from|on|out of)\b")
WHAT_ARE_YOU = re.compile(
    r"\bwhat are you\b"
    r"(?=\s*(?:[?.!,]|$|\b(?:then|exactly|really|anyway|actually|currently|"
    r"at\s+the\s+moment|these\s+days)\b))"
    r"|\bwhat are you\b[^.?!]{0,40}?\bfor\s*[?.!]*$")
def _the_answers_take_it(clean):
    try:
        from ..modules import answers

        return answers.respond(clean, {}) is not None
    except Exception:
        return False
FORGETTING_ASK = re.compile(
    r"(?<!how )(?<!why )(?<!when )"
    r"\b(?:will|would|won'?t|do|does|did|can|could|have|has)\s+(?:you|u)\s+"
    r"(?:ever\s+|just\s+|soon\s+|really\s+|still\s+|already\s+|now\s+|then\s+)?"
    r"(?:forget|forgot|forgotten)\b"
    r"(?!\s+(?:to\s+\w+|(?:the|your|my|his|her|their|a|an)\s+\w))"
    r"|\b(?:are|r)\s+(?:you|u)\s+(?:already\s+)?(?:going|gonna)\s+to\s+forget\b"
    r"|\b(?:are|r)\s+(?:you|u)\s+(?:already\s+)?forgetting\b", re.I)
HELP_TOPIC_ASK = re.compile(
    r"\b(?:what|how) (?:can|could) you (?:help|do)\b|\bwhat do you do\b|"
    r"\bwhat are you good at\b")

HELP_ELSE = re.compile(
    r"\b(?:what|which)\s+(?:else|other|more)\b[^.?]{0,25}?"
    r"\b(?:can|could|do|does)\s+you\s+(?:do|help|offer|manage|cover)\b([^.?]*)"
    r"|\b(?:anything|something)\s+else\b[^.?]{0,20}?\byou\s+(?:can|could)\s+"
    r"(?:do|help|offer)\b([^.?]*)")


def _free_tail(tail):
    return all(word in HELP_TAIL for word in re.findall(r"[a-z']+", tail or ""))


CHOICE = re.compile(r"^[a-z' ]{2,20} or (?:the )?[a-z' ]{2,20}\??$")

CHOICE_WORRY = re.compile(r"\b(?:am|is|are|was|were|do|does|did)\s+"
                          r"(?:i|you|we|they|he|she|it|there|that|this)\b")

CHOICE_FRAME = re.compile(
    r"^(?:"
    r"(?:should|shall|do|can|could|would|will|might)\s+(?:i|we|you|u)\s+"
    r"(?:get|have|buy|go\s+for|pick|choose|take|do|order|book|eat|drink|watch)?\s*"
    r"|(?:i|we)\s+(?:could|might|would|will)\s+"
    r"(?:get|have|buy|go\s+for|pick|choose|take|do|order|book|eat|drink|watch)?\s*"
    r"|(?:how\s+about|what\s+about|maybe|perhaps|instead\s+of)\s+"
    r")")
CHOICE_ARTICLE = re.compile(r"^(?:the|a|an)\s+")


JOINT_FRAME = re.compile(
    r"^(?:should|shall|do|can|could|would|will|might)\s+(?:we|you|u)\b")


def _choice_advice(clean):
    return _unframed(clean) if JOINT_FRAME.match(str(clean or "").strip()) else clean


def _unframed(clean):
    line = CHOICE_FRAME.sub("", str(clean or "").strip())
    line = CHOICE_ARTICLE.sub("", line.strip())
    return line.strip()


CHOICE_REFUSED = re.compile(
    r"^\s*(?:no|not|never|without|neither)\b"
    r"|\b(?:dont|don'?t|do not|doesnt|doesn'?t|didnt|didn'?t|cant|can'?t|cannot|won'?t|"
    r"wouldnt|wouldn'?t|shouldnt|shouldn'?t)\s+(?:\w+\s+){0,2}?"
    r"(?:want|wants|like|likes|love|eat|eating|have|having|drink|wear|do|doing|need|use|"
    r"fancy|stand|bother|manage)\b"
    r"|\ballergic\b|\bhate\b|\bcant have\b")


def _refuses_the_pair(clean):
    head = str(clean or "").split(" or ")[0]
    return bool(CHOICE_REFUSED.search(head))


def _is_a_choice(clean):
    asked = CHOICE.match(clean) or CHOICE.match(_unframed(clean))
    return (bool(asked) and not CHOICE_WORRY.search(clean)
            and not two_ends_of_one_scale(clean)
            and not _refuses_the_pair(clean))


PICK_ASK = re.compile(
    r"\b(?:what|which|who)\s+(?:would|will|should|shall|do|did)\s+(?:you|u|ya)\s+"
    r"(?:pick|choose|get|buy|take|go\s+for|suggest|recommend|prefer)\b"
    r"|\b(?:what|which)\s+(?:do|would)\s+(?:you|u|ya)\s+(?:suggest|recommend|pick|prefer)\b"
    r"|\bwhich\s+one\s+(?:would|do|should|will)?\s*(?:you|u|ya)\b"
    r"|\b(?:any|some|got\s+any)\s+(?:suggestions?|recommendations?)\s*\??$")

PICK_BACK = re.compile(
    r"^(?:and\s+)?(?:what|which)(?:\s+one)?\s+(?:would|do|did|should|will)\s+(?:you|u|ya)\s+do"
    r"(?:\s+(?:then|now|yourself))?\s*\??$")
PICK_WORD = re.compile(r"[a-z0-9']+")
PICK_TITLE = re.compile(r"\*([^*\n]{1,70})\*")
PICK_NOTE = re.compile(r"\s*(?:for|if|when|with)\s+([^.;,*)!?]{2,60})")
PICK_ADVICE = re.compile(r"\b(?:suggest|suggestions?|recommend|recommendations?)\b")
LEAN_ASK = re.compile(r"\b(?:what|which)\s+(?:would|should)\s+(?:you|u|ya)\b"
                      r"|\bwhich one(?:\s+would\s+you\b)?"
                      r"|\bhelp me decide\b")

TRADE_OFF = re.compile(r"\b([a-z0-9][^.!?;]{2,70}?)\s+but\s+([^.!?;]{2,70})", re.I)
NOT_A_SIDE = re.compile(r"\b(?:didnt|doesnt|don|did not|does not|no|not|never|nothing|still|"
                        r"stopped|failed|worse|hurts|hurting|sore|tried|again)\b", re.I)
NOT_A_CHOICE = re.compile(r"\b(?:hate[sd]?|awful|terrible|horrible|dreadful|miserable|toxic|rude|"
                          r"nasty|worst|unbearable|disgusting|useless|pointless|exhausting|"
                          r"can'?t\s+stand|cant\s+stand|sick\s+of|fed\s+up|driving\s+me\s+mad)\b",
                          re.I)
SIDE_HAS = re.compile(r"^(?:has|have|had)\s+(.+)$", re.I)
SIDE_IS = re.compile(r"^(?:it\s+is|it's|its|it\s+was|they\s+are|they're|she\s+is|he\s+is|"
                     r"that\s+is|that\s+are|that\s+was|that\s+were)\s+(.+)$", re.I)
SIDE_SUBJECT = re.compile(r"^(?:the|a|an|my|his|her|their|our|that|this|she|he|they|we|there)\b",
                          re.I)
SIDE_VERB = re.compile(r"\b(?:is|are|was|were|pays|costs|takes|gives|lasts|has|have|means|"
                       r"feels|sounds)\b", re.I)
SIDE_GOOD = re.compile(r"\b(?:nicer|better|friendlier|closer|cheaper|bigger|quieter|cleaner|"
                       r"brighter|warmer|safer|newer|faster|kinder|easier|lighter|shorter|"
                       r"flexible|lovely|great|good|perfect|ideal|pays|earns|more\s+\w+)\b", re.I)
SIDE_BAD = re.compile(r"\b(?:grim|bad|worse|worst|less|fewer|painful|boring|stressful|noisy|"
                      r"dirty|loud|busy|cramped|old|small|tiny|dangerous|risky|annoying|"
                      r"exhausting|unpaid|long|longer|slow|further|farther|expensive|price|prices|"
                      r"priced|cost|costs|fee|fees|high|dear|commute)\b", re.I)
SIDE_ONE = re.compile(r"^((?:the|my|this|that|her|his|their)\s+\w+\s+one)\b\s*(.*)$", re.I)
SIDE_COPULA = re.compile(r"\b(?:is|are|was|were|isn't|aren't)\b", re.I)
SIDE_TAIL = re.compile(r"\s+(?:in|of|out\s+of)\s+(?:the\s+)?other(?:\s+one)?$", re.I)
SIDE_OTHER = re.compile(r"^(?:the\s+)?other(?:\s+one)?\s+", re.I)

DESIRE = re.compile(r"\b(?:i|we)\s+(?:really |just |so )?(?:want|wanna|would love|id love|need|"
                    r"wish|hope|keep wanting|have to)\b", re.I)
OBSTACLE = re.compile(r"\b(?:too|afford|rent|money|cost|time|hours|nervous|scared|worried|"
                      r"anxious|hard|tight|far|means|landlord|feel bad|guilt|awkward|risk)\b",
                      re.I)
LEAN_NOT = re.compile(r"\b(?:sad|low|down|depress\w*|unhappy|miserable|lonely|crying|cry|"
                      r"grief|dying|died|death|funeral|diagnos\w*|cancer|checkup|"
                      r"worried|worry|worries|anxious|scared|afraid|panic\w*)\b", re.I)


CHOICE_SIDE_LEAD = re.compile(r"^(?:(?:should|shall|do|can|could|would|will|might|maybe)\s+i\s+)")
CHOICE_SIDE_TAIL = re.compile(r"\s+(?:then|instead|though|really)$")
CHOICE_SIDE_WHEN = re.compile(
    r"\s+(?:tonight|today|tomorrow|now|instead|this\s+(?:evening|afternoon|morning|weekend|week))$")

CHOICE_PERSON_SIDE = re.compile(
    r"\b(?:my|his|her|their|our|your)\s+side\b|\b(?:his|her|their)\s+(?:family|mum|dad|parents)\b")


ORDER_SIDE_END = re.compile(r"\b(?:first|last)$", re.I)
ORDER_BEFORE_AFTER = re.compile(r"\b(?:before|after)\s+or\s+(?:before|after)\b", re.I)
ORDER_OF_WORK = (
    "The step that would spoil the other one goes last, so nothing gets done twice. What are you "
    "doing it on?",
    "Work it out rather than guess: whatever makes a mess for the other step to clear up goes "
    "first. Which job is it?",
    "That is an order to work out, not a taste to pick: the messy step before the tidy one, and "
    "dry before wet. What are you doing?",
)


ORDER_WORD_TAIL = re.compile(r"\s*\b(?:first|last)\b\s*$", re.I)
ORDER_WORD_LEAD = re.compile(r"^\s*\b(?:before|after)\b\s*", re.I)
ORDER_ONLY = frozenset("""first second third fourth fifth last later earlier next middle
    start end beginning one""".split())


def _an_order_of_work(sides, clean):
    if ORDER_BEFORE_AFTER.search(str(clean or "")):
        return True
    if not any(ORDER_SIDE_END.search(side) for side in sides or ()):
        return False
    for side in sides:
        core = ORDER_WORD_TAIL.sub("", ORDER_WORD_LEAD.sub("", side)).strip()
        core = CHOICE_ARTICLE.sub("", core).strip()
        if core in ORDER_ONLY or len(core) < 2:
            return False
    return True


def _choice_sides(clean):
    parts = _unframed(clean).rstrip("?").split(" or ")
    if len(parts) != 2:
        return None
    sides = []
    for part in parts:
        side = CHOICE_SIDE_TAIL.sub("", CHOICE_SIDE_LEAD.sub("", part.strip()))
        side = CHOICE_SIDE_WHEN.sub("", side.strip())
        side = CHOICE_ARTICLE.sub("", side.strip()).strip()
        if not side or not re.search(r"[a-z]", side):
            return None
        sides.append(side)
    return sides


def _capital(side):
    side = " ".join(str(side or "").split())
    return side[0].upper() + side[1:] if side else side


def _named(side, memory=None):
    understood = (memory or {}).get("understood") or {}
    for entity in understood.get("entities") or ():
        if not isinstance(entity, dict) or entity.get("type") not in NAMED_TYPES:
            continue
        name = str(entity.get("text") or "").strip()
        if len(name) < 2 or name.lower() not in side:
            continue
        side = re.sub(r"\b" + re.escape(name.lower()) + r"\b", name, side)
    return side


def _a_pick(sides, clean, memory=None):
    first, second = sides
    seed = sum(ord(letter) for letter in clean)
    take, other = (first, second) if random.Random(seed).getrandbits(1) else (second, first)
    return _capital(_named(take, memory)), _named(other, memory)


def _between_people(sides, clean):
    for side in sides or ():
        if set(side.split()) & CHOICE_PEOPLE:
            return True
    return bool(CHOICE_PERSON_SIDE.search(str(clean or "")))


def _choice_light(clean, memory=None):
    sides = _choice_sides(clean)
    if sides is None:
        return CHOICE_LIGHT
    if _between_people(sides, clean):
        return CHOICE_BETWEEN_PEOPLE
    take, other = _a_pick(sides, clean, memory)
    return [line.format(pick=take, other=other) for line in CHOICE_LIGHT_PICK]


def _choice_pool(clean, memory=None):
    words = set(clean.split())
    if words & CHOICE_HEALTH:
        if words & CHOICE_THERAPY:
            return CHOICE_WEIGH
        return CHOICE_PHARMACIST
    if _an_order_of_work(_choice_sides(clean), clean):
        return ORDER_OF_WORK
    if words & CHOICE_STAKES:
        return CHOICE_WEIGH
    return _choice_light(clean, memory)


OWN_RECORD_NOT = re.compile(
    r"\b(?:how\s+(?:do|can|could|should|would)\s+i|how\s+to|"
    r"should\s+i|do\s+i\s+need|can\s+i|could\s+i|help\s+me|"
    r"is\s+it\s+worth|worth\s+(?:it|chasing|appealing)|how\s+long\s+does|how\s+much\s+does|"
    r"what(?:'s| is)\s+a|difference|explain|meaning|any\s+tips|advice)\b")


def _their_own_phrase(clean, things):
    for thing in things:
        pattern = MY_OWN.get(thing)
        if pattern is None:
            pattern = MY_OWN[thing] = re.compile(
                r"\b(?:my|our)\s+(?:[a-z']+\s+){0,2}" + re.escape(thing) + r"(?![a-z])")
        match = pattern.search(clean)
        if match:
            return match
    return None


RECORD_STATE = re.compile(
    r"\b(?:been|yet|still|already|confirmed|approved|ready|arrived|arriving|due|processed|"
    r"done|taken|paid|debited|credited|come\s+off|"
    r"cleared|accepted|rejected|declined|dispatched|despatched|delivered|shipped|sent|sorted|"
    r"collected|out\s+for\s+delivery|"
    r"through|tracked|tracking|back|come\s+back|come\s+through|go\s+through|gone\s+through|"
    r"go\s+out|gone\s+out|went\s+out|come\s+out|on\s+(?:its|the|his|her|their)\s+way|"
    r"what(?:'s|s)?|where(?:'s|s)?|when(?:'s|s)?|what\s+time|how\s+much|how\s+many|how\s+long|status|left|"
    r"(?:you|u)\s+(?:check|look\s+(?:(?:it|that)\s+)?up|see|tell\s+me|confirm|look\s+at|"
    r"find\s+(?:(?:it|that)\s+)?out|give\s+me))\b")
RECORD_QUALIFIED = re.compile(r"\s+(?:of|that|which)\b")

OFFICE_STATE = re.compile(
    r"\b(?:approved|approval|accepted|arranged|booked|scheduled|confirmed|issued|granted|"
    r"refused|rejected|declined|registered|processed|dealt\s+with|signed\s+off|finalised|"
    r"finalized|paid\s+out|put\s+through|agreed|arrived|come\s+back|sent|posted|returned)\b")
MY_ANY_THING = re.compile(r"\b(?:my|our)\s+(?:[a-z']+\s+){0,2}([a-z]+)")
_A_MY_PERSON = None


def _a_person_is_the_thing(clean):
    global _A_MY_PERSON
    if _A_MY_PERSON is None:
        from .loss import PEOPLE
        kinds = "|".join(sorted((re.escape(word) for word in PEOPLE), key=len, reverse=True))
        _A_MY_PERSON = re.compile(
            r"\b(?:my|our|his|her|their|the)\s+(?:" + kinds + r")(?:\'s|s\')?"
            r"(?=\s*(?:$|[,.!?;]|(?:has|have|had|is|are|was|were|did|does|do|not|never|just|now|"
            r"still|yet|already|arrived|arrive|arrives|coming|come|came|returned|returns|got|"
            r"gotten|been|being|at|home|there|back|in|out|safe|ok|alright|fine|well|on|off|to|"
            r"from|away|left|gone|late|early|waiting)\b))", re.I)
    return bool(_A_MY_PERSON.search(clean or ""))


A_TILL_ASK = re.compile(
    r"\b(?:wrong|right|short|extra|too\s+much|too\s+little|double)\s+(?:change|amount)\b|"
    r"\bshort[-\s]?changed\b|\bchange\s+back\b|"
    r"\b(?:overcharged|undercharged|charged\s+twice)\b")
NOT_AN_OFFICE = re.compile(
    r"\b(?:cake|cakes|bread|dough|sourdough|pastry|dinner|tea|lunch|breakfast|supper|roast|"
    r"soup|sauce|stock|washing|laundry|wash|load|hair|nails|beard|leg|legs|arm|arms|back|knee|"
    r"shoulder|eyes|ears|teeth|skin|tattoo|car|cars|bike|bikes|van|boiler|heating|fence|shed|"
    r"plant|plants|garden|lawn|wall|walls|roof|paint|grout|silicone|sealant|floor|tiles|shelf|"
    r"door|window|gutter|drive|pond|allotment|chickens|hens|dog|cat|baby|nappy|sleep|diet)\b")

RECORD_CHECK = re.compile(r"\b(?:check|checking|confirm|look\s+up|track|trace)\b")
MY_OWN_STATE = re.compile(
    r"\b(?:have|has)\s+i\s+been\s+(?:paid|approved|accepted|registered|booked|confirmed|"
    r"granted|refused|rejected|shortlisted|interviewed|offered|told|sent|given|taken\s+on|"
    r"picked|placed|invited|added|approved\s+for)\b|"
    r"\bam\s+i\s+(?:on\s+the\s+list|in\s+the\s+running|registered|booked\s+in|signed\s+up|"
    r"enrolled|shortlisted|selected)\b")
RECORD_THINGS = tuple(thing for _, things, _ in MY_RECORDS for thing in things)
CARD_VALIDITY_ASK = re.compile(
    r"\b(?:valid|expire|expires|expired|expiry|run\s+out|runs\s+out|ran\s+out|"
    r"out\s+of\s+date|still\s+(?:use|work|spend|spent)|still\s+good)\b")


CARD_BALANCE_ASK = re.compile(r"\b(?:how\s+much|balance|left|remaining|still\s+on)\b")
CARD_NOT_A_BALANCE = re.compile(r"\b(?:worth|value|declined|refused|cloned|stolen|blocked|"
                                r"cancel|replace|expire|expires|expired)\b")
MY_CARD_ROW = next((options for name, things, options in MY_RECORDS if name == "card"), None)
MY_MONEY_ROW = next((options for name, things, options in MY_RECORDS if name == "money"), None)
MY_APPLICATION_ROW = next((options for name, things, options in MY_RECORDS
                           if name == "application"), None)

POINTS_SCHEME = re.compile(
    r"\b(?:loyalty\s+(?:points?|cards?|scheme)|nectar|clubcard|club\s?card|avios|airmiles|"
    r"reward\s+(?:points?|cards?|scheme)|store\s+points?|points\s+cards?|"
    r"(?:my|our)\s+points|(?:my|our)\s+stamps|stamps?\s+on\s+(?:my|the)\s+card|"
    r"points\s+(?:balance|total))\b", re.I)
POINTS_ASK = re.compile(
    r"\b(?:how\s+many|how\s+much|how\s+do|how\s+does|how\s+can|what(?:'s|\s+is)?|do|does|did|"
    r"are|is|when|where|worth|expire|expires|expired|expiring|left|balance|collect|collected|"
    r"redeem|redeemed|spend|spent)\b", re.I)
POINTS_NOT = re.compile(
    r"\b(?:licence|license|driving|car|insurance|court|ban|visa|school|university|"
    r"course|grade|exam|game|match|score|league|rugby|football|quiz|test)\b", re.I)


MY_BILL_THING = re.compile(
    r"\b(?:memberships?|subscriptions?|subs|plan|tariff|contract|deal|package|"
    r"season\s+ticket|direct\s+debit|standing\s+order)\b", re.I)
MY_BILL_MINE = re.compile(
    r"\b(?:my|our|the)\s+(?:[a-z]+\s+){0,2}?(?:memberships?|subscriptions?|subs|plan|tariff|"
    r"contract|deal|package|season\s+ticket)\b", re.I)
MY_BILL_ASK = re.compile(
    r"\b(?:how\s+much|what(?:'s|\s+is)?\s+(?:i|we)\s+paying?|what\s+do\s+(?:i|we)\s+pay|"
    r"cost|costs|costing|charge|charged|charging|price|paying|per\s+month|a\s+month|"
    r"a\s+year|over\s+the\s+year|too\s+much|cheaper|worth\s+it|stop\s+paying|cancel)\b", re.I)
MY_BILL_NOT = re.compile(
    r"\b(?:a\s+gym|join|joining|sign\s+up|new|compare|comparison|cheapest|switch|switching|"
    r"council\s+tax|water|electric|gas|energy|broadband|insurance|mortgage|rent|"
    r"mobile\s+phone|sim\s+only|iphone|phone\s+contract)\b", re.I)


def _their_own_bill(clean):
    if not MY_BILL_MINE.search(clean) or not MY_BILL_THING.search(clean):
        return None
    if not MY_BILL_ASK.search(clean) or MY_BILL_NOT.search(clean):
        return None
    return MY_BILL_LINES


def _their_own_points(clean):
    if not POINTS_SCHEME.search(clean) or POINTS_NOT.search(clean):
        return None
    if not POINTS_ASK.search(clean):
        return None
    return POINTS_LINES


CARD_RECORD_THINGS = ("gift card", "gift cards", "voucher", "vouchers", "prepaid card",
                      "store card", "loyalty card", "loyalty points", "card")


def _an_office_record(clean, asking):
    if not asking or NOT_AN_OFFICE.search(clean):
        return None
    if A_TILL_ASK.search(clean):
        return AT_THE_TILL
    if _a_person_is_the_thing(clean):
        return None
    if OFFICE_STATE.search(clean) and MY_ANY_THING.search(clean):
        return OFFICE_RECORD_LINES
    if MY_OWN_STATE.search(clean):
        if _has(clean, ("paid", "pay", "wages", "salary", "money", "expenses")):
            if MY_MONEY_ROW is not None:
                return MY_MONEY_ROW
        if MY_APPLICATION_ROW is not None:
            return MY_APPLICATION_ROW
    return None


def _their_own_record(clean, asking):
    said = _their_own_week(clean)
    if said:
        return said
    said = _their_own_points(clean)
    if said:
        return said
    checking = bool(RECORD_CHECK.search(clean)) and bool(_their_own_phrase(clean, RECORD_THINGS))
    validity = bool(CARD_VALIDITY_ASK.search(clean)) and bool(
        _their_own_phrase(clean, CARD_RECORD_THINGS))
    if not (asking or checking or validity) or OWN_RECORD_NOT.search(clean):
        return None
    if validity:
        return CARD_VALIDITY
    if not (RECORD_STATE.search(clean) or checking):
        return _an_office_record(clean, asking)
    rows = MY_RECORDS
    if _their_own_phrase(clean, CARD_RECORD_THINGS):
        rows = sorted(MY_RECORDS, key=lambda row: row[0] != "card")
    for name, things, options in rows:
        phrase = _their_own_phrase(clean, things)
        if phrase and not RECORD_QUALIFIED.match(clean, phrase.end()):
            return options
    if (MY_CARD_ROW is not None and CARD_BALANCE_ASK.search(clean)
            and not CARD_NOT_A_BALANCE.search(clean)
            and _their_own_phrase(clean, ("card",))):
        return MY_CARD_ROW
    phrase = _their_own_phrase(clean, HEALTH_RECORD)
    if phrase and not RECORD_QUALIFIED.match(clean, phrase.end()):
        if _has(clean, HEALTH_WORLD):
            return HEALTH_RECORD_LINES
    return _an_office_record(clean, asking)


A_DAY_AGO = re.compile(
    r"\b(?:yesterday|last night|last (?:week|weekend|month|(?:mon|tues|wednes|thurs|fri|satur|"
    r"sun)day)|on (?:mon|tues|wednes|thurs|fri|satur|sun)day|this (?:morning|afternoon|evening)|"
    r"the weekend|earlier today)\b")
MY_OWN_DOING = re.compile(
    r"(?:^|\b(?:what|where|who|when|which|how much|how many)\b[^?]{0,40}?)"
    r"\b(?:did|have|had)\s+(?:i|we)\s+(?:already\s+|actually\s+|just\s+|even\s+)?"
    r"(?:do|done|go|gone|see|seen|visit|visited|buy|bought|spend|spent|eat|eaten|drink|drunk|"
    r"work|worked|book|booked|order|ordered|pay|paid|take|taken|get|got|watch|watched|meet|met)\b")
MY_OWN_DAY_LINES = (
    "I haven't got your diary, sorry - I only know what you tell me here. Your phone's calendar or "
    "the photos from that day will usually bring it back.",
    "Nothing of yours to look at from this end. The calendar, the photos and the emails from that "
    "day are where it is - tell me what you find and I'll help with the rest of it.",
)

NOT_ABOUT_THEIR_DAY = re.compile(
    r"\b(?:pill|pills|tablet|tablets|medicine|medicines|medication|medications|meds|"
    r"antibiotic|antibiotics|inhaler|insulin|dose|doses|injection|injections|jab|jabs|"
    r"painkiller|painkillers|paracetamol|ibuprofen|steroid|steroids|epipen|"
    r"vitamin|vitamins|supplement|supplements|prescription|prescriptions|drops|patch|patches)\b")


def _their_own_week(clean):
    said = " ".join(str(clean or "").lower().split())
    if not said:
        return None
    if NOT_ABOUT_THEIR_DAY.search(said):
        return None
    if A_DAY_AGO.search(said) and MY_OWN_DOING.search(said):
        return MY_OWN_DAY_LINES
    return None

NUMBER_WANTED = re.compile(
    r"\b(?:the|a|their|its|his|her)\s+(?:[a-z']+\s+){0,2}number\b|"
    r"\bnumber (?:for|to (?:ring|call|phone))\b|\b(?:phone |telephone |contact )number of\b|"
    r"\b(?:whats|what's|wats|wots) (?:the )?(?:phone |telephone )?number\b|"
    r"\bhow do i (?:ring|phone|call)\b|\b(?:need|want|looking for) (?:the )?(?:phone )?number\b|"
    r"\bcontact (?:details|number)\b|\blook up the number\b|\bgive me the number\b|"
    r"\bnumber to (?:ring|call|phone)\b|\bwhat number (?:do|should) i (?:ring|call)\b")
NUMBER_OF = re.compile(r"\bnumber of\b")
NUMBER_OF_PHONE = re.compile(r"\b(?:phone|telephone|contact|mobile)\s+number of\b")
NUMBER_REPORT = re.compile(
    r"\bnumber (?:was|is|kept|keeps|has been|had been|never|didnt|didn't|rang|rung|went)\b|"
    r"\b(?:i|we|she|he|they)\s+(?:rang|rung|phoned|called|tried)\s+"
    r"(?:the\s+|my\s+|her\s+|his\s+|their\s+|our\s+)?(?:[a-z']+\s+){0,2}number\b")
NUMBER_NOT = ("reference number", "order number", "account number", "policy number",
              "national insurance", "registration number", "ni number", "case number",
              "invoice number", "membership number", "customer number", "flight number",
              "bus number", "train number", "house number", "serial number", "pin number",
              "tracking number", "claim number")


NUMBER_PLACE_PATTERNS = {}


def _names_place(clean, places):
    for place in places:
        pattern = NUMBER_PLACE_PATTERNS.get(place)
        if pattern is None:
            pattern = NUMBER_PLACE_PATTERNS[place] = re.compile(
                r"\b" + re.escape(place) + r"(?:s|es)?\b")
        if pattern.search(clean):
            return True
    return False


def _their_contact_number(clean, asking):
    if not NUMBER_WANTED.search(clean) or _has(clean, NUMBER_NOT):
        return None
    if NUMBER_REPORT.search(clean):
        return None
    if NUMBER_OF.search(clean) and not NUMBER_OF_PHONE.search(clean):
        return None
    for places, options in NUMBER_PLACES:
        if _names_place(clean, places):
            return options
    return None


MY_DAY_ASK = re.compile(
    r"(?<![a-z])(?:what time|when|which time|what hours)(?: (?:do|does|am|are|will|should))? i "
    r"(?:start|finish|begin|leave|get in|get off|clock in|clock off|be in|be on|in|on)(?![a-z])"
    r"|(?<![a-z])(?:am|will) i (?:be )?(?:working|in work|in today|in tomorrow|on shift|"
    r"on a shift|on the rota)(?![a-z])")
MY_DAY_SAID = frozenset("""
work works working job shift shifts rota hours office site shop store school placement
today tomorrow tonight now this next the a an on at in for till until from to and or but so
then also please just know wondering do does did dont don't not never any idea anyone anybody
you your me i my actually usually normally roughly about quick question one more supposed meant
ever again morning mornings afternoon evening evenings night nights early late earlies lates days
week weekend monday tuesday wednesday thursday friday saturday sunday day
start starts finish finishes begin clock off experience induction
""".split())
MY_DAY_NOT = re.compile(
    r"\b(?:school run|college|uni|university|course|class|lesson|exam|appointment|nurse|doctor|"
    r"dentist|hospital|physio|clinic|chemist|pharmacy|hair|barber|gym|football|training|"
    r"the match|the kids?|the children|pick(?:ing)? up|drop(?:ping)? off|"
    r"tablets?|medicine|medication)\b", re.I)


def _their_own_day(clean):
    match = MY_DAY_ASK.search(clean)
    if not match or MY_DAY_NOT.search(clean):
        return None
    if not (_has(clean, ("work", "works", "working", "job", "shift", "shifts", "rota", "hours"))
            or re.search(r"\bclock(?:ed|s)? (?:in|off|on)\b", clean)):
        return None
    rest = clean[:match.start()] + " " + clean[match.end():]
    for word in re.findall(r"[a-z']+", rest):
        if word not in MY_DAY_SAID:
            return None
    return MY_OWN_DAY


OWN_TIME_ASK = re.compile(
    r"(?<![a-z])what time (?:do|does|did|will|would|should|can|could|shall) "
    r"(?:i|we|my|our)(?![a-z])")
MY_TIME_ASK = re.compile(r"(?<![a-z])what time (?:is|are|was|were) (?:my|our)(?![a-z])")
OWN_VERB_OPEN = re.compile(r"(?<![a-z])(?:i|we) (?:open|close|shut)(?![a-z])")


def _a_bare_wear_ask(clean):
    text = clean
    for phrase in sorted(LIVE_TAKE_ASK, key=len, reverse=True):
        text = text.replace(phrase, " ")
    for word in tuple(LIVE_WEAR) + tuple(LIVE_SOON):
        text = text.replace(word, " ")
    for word in re.findall(r"[a-z']+", text):
        if word not in LIVE_TAKE_ALLOWED:
            return False
    return True


LIVE_WEATHER_DAY = re.compile(
    r"\b(?:rain|raining|rainy|snow|snowing|sunny|sun|windy|warm|cold|hot|icy|frost|frosty|"
    r"fog|foggy|misty|muggy|humid|cloudy|overcast|chilly|freezing|storm|stormy|thundery|hail|"
    r"showers?|drizzle|drizzling|nice|dull|grey|gray)\b[^.!?]{0,28}?"
    r"\b(?:today|tonight|tomorrow|this week|next week|weekend|saturday|sunday|monday|tuesday|"
    r"wednesday|thursday|friday)\b", re.I)


HOW_WAS_YOUR_TIME = re.compile(
    r"(?<![a-z])hows? (?:is |was |are |were |did |has |have )?(?:your|you) "
    r"(?:day|days|week|weeks|weekend|evening|morning|afternoon|night|shift|holiday|break|time)"
    r"(?![a-z])")
YOUR_DAY_ASK = re.compile(
    r"\b(?:are|were|have|had|did|do|does)\s+(?:you|u)\s+(?:been\s+)?"
    r"(?:having|had|have)\s+(?:a\s+|an\s+)?(?:good|nice|great|lovely|ok|okay|quiet|crap|bad)?\s*"
    r"(?:day|days|weekend|evening|night|morning|afternoon)\b")
YOUR_OWN_TIME = re.compile(
    r"(?<![a-z])(?:your|you)\s+(?:day|days|week|weeks|weekend|evening|morning|afternoon|night)"
    r"(?![a-z])")
HAND_BACK = re.compile(
    r"^(?:(?:and|so|ok|okay|but|right|then)\s+)?"
    r"(?:(?:what|how)\s+about\s+(?:you|ya|u|yourself|your\s+(?:day|week|weekend|evening|one))"
    r"|any(?:thing)?\s+new\s+with\s+you"
    r"|yourself"
    r"|(?:and|so|ok|okay|but|right|then)\s+(?:you|ya|u|yourself))\??"
    r"(?:\s+(?:today|then|anyway|though|so|now|lately|honestly|mate))?$")
YOUR_TIME_ASK = re.compile(
    r"\b(?:what|whats)\s+(?:have|has|ve)\s+(?:you|u)\s+been\s+(?:up\s+to|doing|at)\b"
    r"|\b(?:you|u)\s+been\s+(?:up\s+to|doing)\b")


LATER_QUESTION = re.compile(
    r"(?:^|[,.!?;\u2013\u2014-]\s*|"
    r"\b(?:and|but|so|then|also|ok|okay|cool|right|btw|anyway|quick|thing)\s+)"
    r"(?:what|whats|wats|wat|wot|why|whys|how|hows|when|whens|where|wheres|who|whos|which"
    r"|can (?:i|you|we|it) \w+|could (?:i|you|we) \w+|should i \w+|would (?:i|you) \w+"
    r"|do (?:i|you|we) \w+|does (?:it|that|this) \w+|is (?:it|that|this|there) \w+"
    r"|are (?:there|you|we) \w+)\b",
    re.IGNORECASE)


def _asks_for_something(text):
    lower = text.lower()
    return any(cue in lower for cue in REQUEST_CUES)


def _reads_as_why(clean):
    return clean.startswith("why") or "why that" in clean or "how come" in clean \
        or "what makes you say" in clean


OWN_LIFE = re.compile(r"\b(?:my|our|his|her|their)\b")


def _is_about_the_persons_own_life(clean):
    return bool(OWN_LIFE.search(clean))


def _in_a_care_thread(memory):
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    for turn in reversed(turns[-THREAD_TURNS:]):
        module = turn.get("module")
        if module in CARE_MODULES:
            return True
        if module not in QUIET_MODULES:
            return False
    return False


def _a_lean_only_line(clean):
    return not [word for word in PICK_WORD.findall(clean) if word not in PICK_ONLY_WORDS]


def _a_bare_pick(clean):
    if not PICK_ASK.search(clean):
        return False
    if " or " in clean:
        return False
    if _has(clean, OPINION_ASKS):
        return False
    return not [word for word in PICK_WORD.findall(clean) if word not in PICK_ONLY_WORDS]


def _the_side_taken(reply, sides):
    said = str(reply or "").lower()
    best = None
    for side in sides or ():
        found = re.search(r"\b" + re.escape(side.lower()) + r"", said)
        if found and (best is None or found.start() < best[0]):
            best = (found.start(), side)
    return best[1] if best else None


def _picked_a_side(reply, sides):
    return _the_side_taken(reply, sides) is not None


def _offered(memory):
    for turn in reversed(memory.get("turns") or []):
        if not isinstance(turn, dict):
            continue
        said = PICK_WORD.findall(str(turn.get("user") or "").lower())
        if not said or not [word for word in said if word not in PICK_ONLY_WORDS]:
            continue
        if turn.get("module") == FALLBACK_MODULE and not _picked_a_side(
                str(turn.get("bot") or ""), _choice_sides(" ".join(said))):
            return []
        found = _titles(str(turn.get("bot") or ""))
        if len(found) >= 2:
            return found
        sides = _choice_sides(" ".join(said))
        if not sides:
            return []
        taken = _the_side_taken(str(turn.get("bot") or ""), sides)
        if taken:
            return [(_capital(taken), "")]
        return [(_capital(side), "") for side in sides]
    return []


def _titles(said):
    found = []
    for match in PICK_TITLE.finditer(said):
        name = " ".join(match.group(1).split())
        if not name or len(name.split()) > 8 or not name.strip("."):
            continue
        if len(name.split()) == 1 and name[:1].islower() and not any(c.isdigit() for c in name):
            continue
        note = PICK_NOTE.match(said[match.end():match.end() + 90])
        note = " ".join(note.group(1).split()) if note else ""
        if note and re.search(r"\b(?:you|your|i|we|me|us)\b", note):
            note = ""
        found.append((name, note))
    return found


def _names_in(said):
    return {word for word in PICK_WORD.findall(said.lower()) if word not in PICK_ONLY_WORDS}


def _a_named_side(after):
    text = " ".join(str(after or "").split()).strip(" ,.;:")
    text = SIDE_TAIL.sub("", text).strip(" ,.;:")
    if not text or NOT_A_CHOICE.search(text) or SIDE_BAD.search(text):
        return ""
    if not SIDE_GOOD.search(text):
        return ""
    text = SIDE_OTHER.sub("", text).strip(" ,")
    if re.match(r"^(?:is|are|was|were)\s+", text, re.I):
        text = "that " + text
    first = re.match(r"^(?:i|we|im|i'm)\b", text, re.I)
    has = SIDE_HAS.match(text)
    if has:
        return "the one with " + has.group(1).strip(" ,.")
    is_ = SIDE_IS.match(text)
    if is_:
        return "the one that is " + is_.group(1).strip(" ,.")
    if first:
        return ""
    one = SIDE_ONE.match(text)
    if one and SIDE_GOOD.search(one.group(2)):
        return one.group(1)
    if SIDE_SUBJECT.match(text) and SIDE_COPULA.search(text):
        return "the one where " + text
    if re.match(r"^(?:more|fewer|less|better|cheaper|bigger|newer|nicer)\b", text, re.I):
        return "the one with " + text
    if SIDE_VERB.search(text) and not SIDE_SUBJECT.match(text):
        return "the one that " + text
    if not SIDE_SUBJECT.match(text):
        return "the one " + text
    return ""


def _a_trade_off(memory):
    pointed = []
    for turn in reversed(memory.get("turns") or []):
        if not isinstance(turn, dict):
            continue
        said = " ".join(str(turn.get("user") or "").split())
        found = PICK_WORD.findall(said.lower())
        if not found or not [word for word in found if word not in PICK_ONLY_WORDS]:
            continue
        match = TRADE_OFF.search(said)
        if not match:
            if len(said.split()) <= 3 and not said.endswith("?"):
                pointed.append(said)
                continue
            return ()
        before = match.group(1).strip(" ,.")
        after = match.group(2).strip(" ,.")
        if (len(before.split()) < 2 or len(after.split()) < 2
                or NOT_A_SIDE.search(after) or DESIRE.search(before)
                or OBSTACLE.search(after)):
            return ()
        if _is_a_body_or_care_trade_off(said):
            return ()
        named = _a_named_side(after)
        if not named:
            return ()
        names = _names_in(said)
        if [line for line in pointed if not _names_in(line) & names]:
            return ()
        return named
    return ()


def _is_a_body_or_care_trade_off(said):
    words = set(re.findall(r"[a-z']+", said.lower()))
    if words & (BODY_PARTS | SYMPTOM_WORDS | HEALTH_WORDS | CHOICE_HEALTH | WORRY_WORDS):
        return True
    return bool(LEAN_NOT.search(said))


def _a_leaning_side(clean, memory):
    if not _a_bare_pick(clean) and not LEAN_ASK.search(clean):
        return None
    if not _a_lean_only_line(clean):
        return None
    if _in_a_care_thread(memory):
        return None
    side = _a_trade_off(memory)
    if not side:
        return None
    return _choose(TRADE_OFF_LEAN, memory, clean).format(side=side)


def _my_pick(clean, memory):
    offered = _offered(memory)
    if not _a_bare_pick(clean) and not (offered and PICK_BACK.match(str(clean or "").strip())):
        return None
    if _in_a_care_thread(memory):
        return None
    if offered:
        seed = len(memory.get("turns") or []) * 7919 + sum(ord(ch) for ch in clean)
        name, note = offered[random.Random(seed).randrange(len(offered))]
        if note:
            pool = [line.format(name=name, note=note) for line in MY_PICK_NOTE]
        else:
            pool = [line.format(name=name) for line in MY_PICK]
        return _choose(pool, memory, clean)
    if PICK_ADVICE.search(clean):
        return None
    return _choose(MY_PICK_ASK, memory, clean)


JUDGE_ASK = re.compile(
    r"(?:^|\b(?:ok|okay|so|and|but|hmm|well|wait|honestly|seriously)\b )"
    r"(?:is|was|would|will)\s+(?:that|this|it)\s+(?:be\s+)?(?:such\s+)?(?:a\s+|an\s+)?"
    r"(?P<face>" + JUDGE_ASKS_SLIGHT + r"|" + JUDGE_ASKS_FINE + r"|" + JUDGE_ASKS_MAD + r")"
    r"(?:\s+" + JUDGE_NOUN + r")?"
    r"(?:\s+(?:or\s+not|then|though|tho|or\s+what|at\s+all))?"
    r"$"
    r"|(?:^|\b(?:ok|okay|so|and|but|hmm|well)\b )does\s+(?:that|this|it)\s+"
    r"(?:sound|seem|look)\s+(?:like\s+)?(?:a\s+|an\s+)?"
    r"(?P<face2>" + JUDGE_ASKS_SLIGHT + r"|" + JUDGE_ASKS_FINE + r"|" + JUDGE_ASKS_MAD + r")"
    r"(?:\s+" + JUDGE_NOUN + r")?$"
    r"|(?:^|\b(?:ok|okay|so|and|but|hmm|well)\b )am\s+i\s+(?:being\s+)?"
    r"(?P<face3>" + JUDGE_ASKS_MAD + r"|" + JUDGE_ASKS_SLIGHT + r")$")
JUDGE_ASK_BARE = re.compile(
    r"^(?:(?:ok|okay|so|and|but|hmm|well|honestly|seriously)\s+)?"
    r"(?:(?:does|would|is|was)\s+(?:that|this|it)\s+)?"
    r"(?:(?:sound|seem|look)\s+(?:like\s+)?)?"
    r"(?:(?:a|an)\s+)?"
    r"(?P<face>" + JUDGE_ASKS_SLIGHT + r"|" + JUDGE_ASKS_FINE + r"|" + JUDGE_ASKS_MAD + r")"
    r"(?:\s+(?P<bare_noun>" + JUDGE_NOUN + r"))?$")
JUDGE_PLAN_OPENING = re.compile(
    JUDGE_LEAD +
    r"(?:im|i am|i)\s+(?:going to|gonna|off to|out to|away to|heading to|heading off to"
    r"|planning to|planning on|thinking of|thinking about"
    r"|about to|want to|wanna|might|will|intend to|intending to|decided to|have decided to"
    r"|plan to|hoping to|hope to|looking to|keen to|aiming to|thinking i(?:d| would) like to"
    r"|think i(?:ll| will)|reckon i(?:ll| will))\s+(?P<plan>\S.{1,58})$"
    r"|" + JUDGE_LEAD +
    r"i\s+(?:have\s+)?decided\s+(?:to|i(?:'ll| will))\s+(?P<plan9>\S.{1,58})$"
    r"|" + JUDGE_LEAD +
    r"(?:my|the)\s+plan\s+is\s+to\s+(?P<plan2>\S.{1,58})$"
    r"|" + JUDGE_LEAD +
    r"(?:im|i am)\s+(?:nearly\s+|about\s+)?\d{2}\s*,?\s+and\s+(?:want|need|plan)\s+to\s+"
    r"(?P<plan3>\S.{1,58})$")
JUDGE_SHOULD_OPENING = re.compile(
    JUDGE_LEAD +
    r"(?:should\s+(?:i|we)|(?:i|we)\s+(?:should|ought to))\s+(?P<plan>\S.{1,58})$")
JUDGE_HOPED_FOR = re.compile(
    r"\b(?:hoping|hope|looking|keen|aiming|intending|planning on)\b"
    r"|\bthinking i(?:d| would) like to\b", re.IGNORECASE)

MIND_WORRY = re.compile(
    r"\b(?:hear(?:ing)?\s+(?:noises?|voices?|things|stuff)|see(?:ing)?\s+things|"
    r"watching\s+me|following\s+me|remember(?:ing)?\s+(?:anything|things)|"
    r"losing\s+(?:my\s+mind|it|my\s+memory)|forgetting\s+everything|going\s+mad)\b",
    re.IGNORECASE)
JUDGE_NAMES_A_HOLE = re.compile(
    r"\bno\b|\bnothing\b|\ball\s+(?:my|our|your|the)\b|\bwithout\b|\bnot\s+\w+|\bnever\b"
    r"|\b(?:skip|skipping|stop|stopping|pause|pausing|come off|coming off)\s+(?:my|the|your)?\s*"
    r"(?:medication|meds|tablets|pills|insulin|treatment|doses?)\b", re.IGNORECASE)
JUDGE_ACT_AT_SOMEONE = re.compile(
    r"\b(?:key|keying|scratch|scratching|slash|slashing|smash|smashing|torch|torching|"
    r"vandalise|vandalize|vandalising|spike|spiking|drug|drugging|"
    r"hit|hitting|punch|punching|kick|kicking|strangle|strangling|choke|choking|stab|stabbing|"
    r"shoot|shooting|kill|killing|poison|poisoning|harm|harming|hurt|hurting|"
    r"slap|slapping|smack|smacking|thump|thumping)\s+(?:\w+\s+){0,3}?"
    r"(?:him|her|them|"
    r"(?:my|his|her|their|your|our|somebody's|someone's)\s+(?:\w+))", re.IGNORECASE)
JUDGE_ANSWERS_FIRST = re.compile(
    r"^\W*(?:yes|no|nope|not|don'?t|never|definitely|probably|only)\b", re.IGNORECASE)
JUDGE_A_CARD_HEADING = re.compile(r"^\W*(?:yes|no)\s*:\s", re.IGNORECASE)
JUDGE_NOT_A_PLAN_TO_BLESS = re.compile(
    r"\b(?:drink|drinking|booze)\b(?:\s+\w+){0,6}?\s+"
    r"(?:every\s+(?:night|day|evening)|(?:a|one)\s+bottle|a\s+night|nightly|daily)\b"
    r"|\b(?:smoke|smoking|vape|vaping)\s+(?:weed|pot|dope|skunk|crack|heroin|coke|cocaine|speed)\b"
    r"|\b(?:weed|pot|cocaine|heroin|crack)\s+every\s+(?:day|night)\b"
    r"|\blie\s+(?:on|in)\s+(?:my|the)\s+(?:cv|resume|application|tax\s+return)\b"
    r"|\b(?:stop|stops|evade|evading|dodge|dodging)\s+paying\s+tax\b|\btax\s+evasion\b"
    r"|\bfiddle\s+(?:my\s+)?(?:tax|taxes|expenses|hours)\b"
    r"|\bclaim\s+(?:benefits|housing\s+benefit|universal\s+credit)\s+(?:i(?:'m| am)\s+not|"
    r"i\s+shouldnt|i\s+shouldn'?t)\b", re.IGNORECASE)
JUDGE_TAKING_SOMETHING = re.compile(
    r"\b(?:take|taking|took|nick|nicking|pinch|pinching|borrow|borrowing|"
    r"help\s+myself\s+to|helping\s+myself\s+to)\b(?:\s+\w+){0,5}?\s+"
    r"(?:from|out\s+of)\s+(?:work|the\s+till|the\s+shop|the\s+office|the\s+company|"
    r"the\s+stockroom|the\s+warehouse|the\s+club|stock)\b", re.IGNORECASE)
JUDGE_LYING = re.compile(r"\b(?:lie|lying|lied)\s+(?:to|about)\b", re.IGNORECASE)
JUDGE_A_TARGET = re.compile(
    r"\b(?:smash(?:ing)?|hit(?:ting)?|beat(?:ing)?|punch(?:ing)?|kick(?:ing)?)\s+"
    r"(?:(?:my|your|his|her|their|our)\s+)?"
    r"(?:goals?|personal\s+bests?|pbs?|records?|targets?|numbers?|deadlines?|quota|quotes?)\b",
    re.IGNORECASE)
JUDGE_TAKING = re.compile(
    r"\b(?:steal|stealing|shoplift|shoplifting|rob|robbing|mug|mugging|"
    r"burgle|burgling|hack|hacking|blackmail|blackmailing|defraud|defrauding)\b"
    r"(?!\s+(?:a\s+few|time|the\s+(?:show|scene|limelight|spotlight|march|day)|"
    r"a\s+(?:march|kiss|glance|look|moment|nap|day)\b))",
    re.IGNORECASE)
JUDGE_WISHES_HARM = re.compile(
    r"\b(?:stop|stopping|quit|quitting|give\s+up|giving\s+up|cut\s+out|cutting\s+out)\s+"
    r"(?:eating|food|meals)\b"
    r"|\b(?:eat|eating|ate)\s+nothing\b|\bstarve\s+myself\b|\bmake\s+myself\s+sick\b"
    r"|\bpayday\s+loan\b|\bloan\s+shark\b|\bgambl(?:e|ing)\b|\bbet\s+(?:my|our|the)\b"
    r"|\bborrow\s+(?:a\s+)?[\u00a3$\u20ac]?\d{3,}", re.IGNORECASE)

JUDGE_JUDGES_A_NOUN = re.compile(
    r"\b(?:bad|terrible|awful|dreadful|wrong)\s+" + JUDGE_NOUN + r"\b", re.IGNORECASE)
JUDGE_DECISION_LEAD = re.compile(r"^(?:if|unless|so|then|otherwise|either|worth)\b", re.IGNORECASE)
JUDGE_HOLE_SAFETY = re.compile(
    r"\b(?:skip|skipping|stop|stopping|pause|pausing|come\s+off|coming\s+off)\s+"
    r"(?:my|the|your)?\s*(?:medication|meds|tablets|pills|insulin|treatment|doses?)\b"
    r"|\bmeds\b|\bmedication\b", re.IGNORECASE)
JUDGE_ASKING_FOR_A_CAUTION = frozenset("""stupid daft dumb silly idiotic thick bad terrible awful
    dreadful wrong good great sensible wise smart clever reasonable mad crazy insane nuts mental
    unhinged""".split())
JUDGE_JUDGEMENT = re.compile(
    r"\b(?:is|would be)\s+(?:a\s+)?(?:good|bad|fine|great|sensible|wise)\s+idea"
    r"|\bworth\s+(?:doing|it|a\s+(?:go|try))\b|\bnot\s+worth\b"
    r"|\bgo for it|\bhold off\b", re.IGNORECASE)





JUDGE_MOVING_TO = re.compile(r"\b(?:" + stepwords.MOVING_TO + r")\s*$", re.IGNORECASE)


def _the_opening_before(match):
    for group in ("plan", "plan2", "plan3", "plan9"):
        if match.group(group):
            return match.string[:match.start(group)]
    return ""


def _a_gerund(word):
    word = word.strip(".,!?;:'\"")
    return len(word) >= 5 and word.endswith("ing") and word not in JUDGE_NOT_A_GERUND


A_NOUN_PHRASE_OPENS = frozenset((
    "a", "an", "the", "my", "your", "our", "their", "his", "her", "its", "some", "any", "more",
    "less", "another", "one", "two", "three", "both", "all", "no", "nothing", "none", "it",
))


def _a_plan_said_back(phrase):
    words = phrase.split()
    opening = "wanting " if words and words[0].lower() in A_NOUN_PHRASE_OPENS else "wanting to "
    return opening + _yours(phrase)


def _a_plan_phrase(said):
    text = _matchable(said)
    match = JUDGE_PLAN_OPENING.search(text)
    if match:
        words = (match.group("plan") or match.group("plan2") or match.group("plan3")
                 or match.group("plan9") or "").split()
        if not words or len(words) > 7 or any(word in JUDGE_PLAN_STOP for word in words):
            return ""
        phrase = " ".join(words)
        if not re.search(r"[a-z]", phrase) or not re.search(r"[a-z]{3}", phrase):
            return ""
        if _a_gerund(words[0]):
            return _yours(phrase)
        if JUDGE_MOVING_TO.search(_the_opening_before(match)) and not stepwords.a_step(words[0]):
            return _yours("going to " + phrase)
        return _a_plan_said_back(phrase)
    match = JUDGE_SHOULD_OPENING.search(text)
    if match:
        words = match.group("plan").split()
        if not words or len(words) > 7 or any(word in JUDGE_PLAN_STOP for word in words):
            return ""
        if not re.search(r"[a-z]{3}", " ".join(words)):
            return ""
        return _a_plan_said_back(" ".join(words))
    return ""


MINE = re.compile(r"\b(my|me|myself|mine)\b", re.IGNORECASE)


def _yours(phrase):
    return MINE.sub(lambda found: YOURS.get(found.group(1).lower(), found.group(1)), phrase)


def _the_plan_on_the_table(memory):
    return _the_plan_and_its_line(memory)[0]


def _the_plan_is_the_last_thing_said(plan_line, memory):
    said = [_matchable(turn.get("user")) for turn in (memory.get("turns") or [])
            if isinstance(turn, dict)]
    said = [line for line in said if line]
    about = {word for word in re.sub(r"[^a-z0-9 ]", " ", plan_line).split()
             if len(word) > 2 and word not in JUDGE_NOD_WORDS}
    for stop in range(len(said) - 1, -1, -1):
        if said[stop] == plan_line:
            break
    else:
        return True
    for line in said[stop + 1:]:
        content = [word for word in re.sub(r"[^a-z0-9 ]", " ", line).split()
                   if len(word) > 2 and word not in JUDGE_NOD_WORDS]
        if not content or about & set(content):
            continue
        return False
    return True


def _the_plan_and_its_line(memory):
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    for turn in reversed(turns[-4:]):
        said = _matchable(turn.get("user"))
        if not said or not [word for word in said.split() if word not in JUDGE_NOD_WORDS]:
            continue
        plan = _a_plan_phrase(said)
        if plan:
            return plan, said
        if JUDGE_PLAN_OPENING.search(said) or JUDGE_SHOULD_OPENING.search(said):
            return "", said
    return "", ""


def _the_reply_above_judged(memory, past_a_question=False):
    said = (last_bot(memory) or "").strip()
    if not said:
        return False
    if JUDGE_A_CARD_HEADING.match(said):
        return False
    if said.endswith("?") and not past_a_question:
        return True
    if JUDGE_JUDGEMENT.search(said) or JUDGE_ANSWERS_FIRST.match(said):
        return True
    sentences = [part.strip() for part in re.split(r"(?<=[.!?])\s+", said) if part.strip()]
    last = sentences[-1] if sentences else said
    return bool(len(last.split()) <= 20 and JUDGE_DECISION_LEAD.match(last))


TRIP_NAMED = re.compile(
    r"\b(?:going to|going away|off to|holiday to|holidays? in|trip to|weekend in|week in|"
    r"flying to|driving to|booked (?:a |our |the )?(?:trip|holiday|flights?|hotel|weekend)|"
    r"thinking of going|thinking about going|hoping to go|planning to go|visiting)\b", re.I)
NOT_A_PLACE = re.compile(
    r"\b(?:hospital|doctors?|dentist\w*|gp|clinic|a&e|ward|surgery|appointment|scan|"
    r"results?|wedding|funeral|christening|baptism|court|work|school|nursery|college|uni|"
    r"university|gym|physio\w*|therapy|therapist|vets?|interview|meeting|party|gig|concert|"
    r"match|church|prison|jail|care home|tip|dump|shops?|supermarket|swimming|parents|"
    r"mum|dad|mother|father|sister|brother|nan|nana|grandma|grandad|gran|friend|family|"
    r"cinemas?|pictures|theatres?|theaters?|films?|movies?|screening|exhibition|"
    r"galler(?:y|ies)|musicals?|opera|ballet)\b",
    re.I)
PLACE_EVALUATIVE = re.compile(
    r"\b(?:nice|good|any good|worth (?:it|going|a visit|the trip|seeing)|busy|expensive|cheap|"
    r"quiet|lively|packed|safe|warm|sunny|rainy|boring|ok|okay|family friendly)\b", re.I)
PLACE_OPENER = re.compile(r"^(?:is|was|are|were|do|does|did|would|will|any)\b", re.I)


def _a_place_asked_about(clean, memory):
    said = _matchable(clean).rstrip(" ?.!,")
    if not said or len(said.split()) > 6:
        return None
    if not PLACE_EVALUATIVE.search(said):
        return None
    from .the_rule_for_it import A_FARE_OR_A_TICKET, PRICE_VERDICT
    if A_FARE_OR_A_TICKET.search(said) and PRICE_VERDICT.search(said):
        return None
    if not (PLACE_OPENER.match(said) or "?" in str(clean or "")):
        return None
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)]
    for turn in reversed(turns[-3:]):
        mentioned = _matchable(turn.get("user"))
        if not mentioned or not [word for word in mentioned.split()
                                 if word not in JUDGE_NOD_WORDS]:
            continue
        if NOT_A_PLACE.search(mentioned):
            return None
        return list(A_PLACE_I_DONT_KNOW) if TRIP_NAMED.search(mentioned) else None
    return None


def a_verdict_on_their_plan(clean, memory, past_a_question=False):
    return _a_verdict_on_their_plan(clean, memory, past_a_question)


def _a_verdict_on_their_plan(clean, memory, past_a_question=False):
    said = _matchable(clean).rstrip(" ?.!,")
    asked = JUDGE_ASK.match(said)
    if not asked:
        bare = JUDGE_ASK_BARE.match(said)
        if not bare or not (bare.group("bare_noun")
                            or bare.group("face") in JUDGE_BARE_FACES):
            return None
        if not _the_plan_on_the_table(memory):
            return None
        asked = bare
    if _in_a_care_thread(memory):
        return None
    face = (asked.group("face") or asked.group("face2") or asked.group("face3") or "").lower()
    if face in JUDGE_NOT_A_VERDICT and not JUDGE_JUDGES_A_NOUN.search(said):
        return None
    plan, plan_line = _the_plan_and_its_line(memory)
    stale = bool(plan_line) and not _the_plan_is_the_last_thing_said(plan_line, memory)
    if stale:
        plan, plan_line = "", ""
    if plan_line and (JUDGE_NAMES_A_HOLE.search(plan) or JUDGE_NAMES_A_HOLE.search(plan_line)):
        if JUDGE_HOLE_SAFETY.search(plan_line) or JUDGE_HOLE_SAFETY.search(plan or ""):
            return None
        if face in JUDGE_ASKING_FOR_A_CAUTION:
            return [line.format(plan=plan, Plan=plan[:1].upper() + plan[1:])
                    for line in JUDGE_PLAN_HAS_A_HOLE]
        return None
    if plan or plan_line:
        wish = " ".join(part for part in (plan, plan_line) if part)
        if not JUDGE_A_TARGET.search(wish) and (JUDGE_ACT_AT_SOMEONE.search(wish)
                                             or JUDGE_TAKING.search(wish)):
            said_back = harm.reply_for(plan_line, memory) if plan_line else None
            return [said_back] if said_back else list(JUDGE_WISH_ANGRY)
        if JUDGE_WISHES_HARM.search(wish) or JUDGE_TAKING_SOMETHING.search(wish) \
                or JUDGE_LYING.search(wish) or JUDGE_NOT_A_PLAN_TO_BLESS.search(wish):
            return None
    if plan_line and not plan:
        return None
    if plan and _the_reply_above_judged(memory, past_a_question):
        if not JUDGE_HOPED_FOR.search(_matchable(plan_line)):
            return None
        plan = ""
    if not plan and asked.group("face3"):
        if MIND_WORRY.search(_matchable(memory.get("turns", [{}])[-1].get("user", ""))):
            return JUDGE_NO_PLAN_MIND
        return JUDGE_NO_PLAN_MAD if stale else None
    if not plan:
        if face in JUDGE_SELF_JUDGING:
            return JUDGE_NO_PLAN_MAD
        if face in JUDGE_ONLY_A_PLAN:
            return JUDGE_NO_PLAN
        if face in JUDGE_SOUNDS_FINE:
            return JUDGE_NO_PLAN_FINE
        return None
    pool = JUDGE_SANE if face in ("mad", "crazy", "insane", "nuts", "mental", "unhinged") else (
        JUDGE_FINE if face in ("good", "great", "sensible", "wise", "smart", "clever",
                               "reasonable")
        else JUDGE_WORTH)
    return [line.format(plan=plan, Plan=plan[:1].upper() + plan[1:]) for line in pool]


OWN_FAVOURITE = re.compile(
    r"\b(?:what|which)(?:'?s| is| was)?\s+(?:my|our)\s+(?:\w+\s+){0,2}(?:favourite|favorite)\s+(\w+)"
    r"|\b(?:do|can) you (?:remember|know)\s+(?:my|our)\s+(?:\w+\s+){0,2}"
    r"(?:favourite|favorite)\s+(\w+)")
A_FAVOURITE_SAID = re.compile(r"\bmy (?:favourite|favorite) (\w+) (?:is|was|would be)\s+"
                              r"([^.,!?;]{1,40})")

OWN_FAVOURITE_LINES = (
    "Remind me - which one is it?",
    "Say it again and I will keep it in mind: which one?",
    "I don't have that one. What is it?",
)

THEIR_FAVOURITE_BACK = (
    "You said {value} - is that still the one?",
    "{Value}, as far as I have it. Has that changed?",
    "{Value}, you told me. Still the one?",
)


def _their_favourite_said(thing, memory):
    if not thing:
        return None
    for turn in reversed((memory.get("turns") or [])[-12:]):
        if not isinstance(turn, dict):
            continue
        found = A_FAVOURITE_SAID.search(_matchable(turn.get("user") or ""))
        if found and found.group(1) == thing:
            value = found.group(2).strip()
            if value and " " not in value[:1]:
                return value
    return None


def _their_favourite_back(thing, value):
    return tuple(line.format(value=value, Value=value[:1].upper() + value[1:])
                 for line in THEIR_FAVOURITE_BACK)


def _taste(clean, memory, was_taste, asking, repaired=""):
    if was_taste and _reads_as_why(clean):
        return _choose(WHY_AFTER_TASTE, memory, clean)
    if asking and OWN_FAVOURITE.search(clean):
        found = OWN_FAVOURITE.search(clean)
        thing = found.group(1) or found.group(2) or ""
        value = _their_favourite_said(thing, memory)
        if value:
            return _choose(_their_favourite_back(thing, value), memory, clean)
        return _choose(OWN_FAVOURITE_LINES, memory, clean)
    if repaired and repaired != clean and not _has(clean, OPINION_ASKS) \
            and _has(repaired, OPINION_ASKS):
        clean = repaired
    asked = _has(clean, OPINION_ASKS)
    if asked and _is_about_the_persons_own_life(clean):
        return None
    if not asked and _is_a_choice(clean) and not _has(_choice_advice(clean), ADVICE_WORDS):
        asked = True
    if not asked and asking and any(_has(clean, phrases) for phrases, _ in TASTES):
        asked = True
    if not asked:
        return None
    if _is_about_the_persons_own_life(clean) and _has(clean, FAVOURITE_WORDS):
        return None
    for phrases, options in TASTES:
        if _has(clean, phrases):
            return _choose(options, memory, clean)
    if _is_a_choice(clean):
        return _choose(_choice_pool(clean, memory), memory, clean)
    if _has(clean, FAVOURITE_WORDS):
        return _choose(FAVOURITE_GENERAL, memory, clean)
    return _choose(TASTE_GENERAL, memory, clean)


_VENUE_RE = []


def _names_a_venue(clean):
    if not _VENUE_RE:
        joined = "|".join(re.escape(word) for word in
                          sorted(LIVE_VENUE, key=len, reverse=True))
        _VENUE_RE.append(re.compile(r"(?<![a-z])(?:" + joined + r")(?:s|es)?(?![a-z])"))
    return bool(_VENUE_RE[0].search(clean))


def venue_hours(text, memory=None):
    clean = str(text or "").strip().lower()
    if not _names_a_venue(clean) or not _has(clean, LIVE_OPEN_CLOSE):
        return False
    for kind, _phrases, options in LIVE_KINDS:
        if kind == "hours":
            return _live(clean, True, memory) == options
    return False


def venue_hours_lines():
    for kind, _phrases, options in LIVE_KINDS:
        if kind == "hours":
            return frozenset(options)
    return frozenset()
LIVE_RESULT_ASK = re.compile(
    r"\b(?:who\s+won|who(?:['\u2019]?s|\s+is)\s+winning|did\s+[a-z][a-z' ]{0,20}?\s+win|"
    r"what(?:s|'s| is| was)?\s+the\s+(?:final\s+)?score|(?:any|the)\s+results?\b(?!\s+of))")
LIVE_BARE_RESULTS = re.compile(r"\b(?:any|the)\s+results?\b")
LIVE_HOW_IT_WENT = re.compile(
    r"\bhow\s+did\s+(?!(?:it|that|this|things|everything|you|i)\b)"
    r"[a-z][a-z' ]{0,20}?\s+(?:go|do|get\s+on)\b")
LIVE_TABLE_ASK = re.compile(
    r"\b(?:top|bottom)\s+of\s+the\s+(?:league|table)|in\s+the\s+(?:league|table)|"
    r"still\s+in\s+the\s+cup|out\s+of\s+the\s+cup|through\s+to\s+the\s+next\s+round")
LIVE_LISTING_ASK = re.compile(
    r"\b(?:what|which)\s+channel\b|\bwhere\s+(?:can|do)\s+i\s+watch\b|"
    r"\bis\s+it\s+on\s+(?:the\s+)?(?:tv|telly|iplayer|bbc|itv|sky)\b|"
    r"\bwhat\s+time\s+(?:is\s+)?(?:kick\s*off|does\s+(?:the|it)\s+(?:start|kick\s*off))|"
    r"\bwhat\s+time\s+(?:is|does|do|will)\b[^?]{0,30}?\b(?:start|starts|kick\s*off|begin|"
    r"kick-off|coverage|highlights)\b|"
    r"\bwhen\s+(?:is|are)\s+(?:the|we|they)\s+(?:next\s+)?(?:match|game|fixture)|"
    r"\bwhen\s+do\s+(?:we|they)\s+play\b")
LIVE_WORLD_ASK = re.compile(
    r"\b(?:latest|breaking|big|any)\s+news\b|\bnews\s+(?:today|tonight|this\s+morning)\b|"
    r"\b(?:in|from)\s+the\s+(?:news|world)\b|\bheadlines?\b|\bspill\s+the\s+news\b|"
    r"\b(?:happening|going\s+on)\s+in\s+the\s+world\b|\bwhat\s+the\s+news\s+is\b")

_WORLD_AS_SCOPE = re.compile(r"\b(?:in|from)\s+the\s+world\b")
_A_NEWS_WORD_BESIDE = re.compile(
    r"\b(?:news|headlines?|happening|going\s+on|latest|breaking|stories|story)\b")


def _the_scope_of_a_standing_ask(clean):
    if not _WORLD_AS_SCOPE.search(clean):
        return False
    return not _A_NEWS_WORD_BESIDE.search(_WORLD_AS_SCOPE.sub(" ", clean))
LIVE_SPORT = ("match", "game", "score", "scores", "football", "rugby", "cricket",
              "tennis", "boxing", "league", "cup", "final", "semi", "fixtures",
              "fixture", "kick off", "kick-off", "goal", "goals", "wicket", "innings",
              "test match", "playoffs", "play offs", "f1", "formula one", "grand prix",
              "the ashes", "the table")
LIVE_NOT_WORLDS = re.compile(
    r"\b(?:my|our|his|her|their)\s+(?:son|daughter|kid|kids|child|children|baby|wife|husband|"
    r"partner|mum|mom|mother|dad|father|brother|sister|friend|boss|exam|scan|test|interview|"
    r"application|case|claim|order|orders|delivery|parcel|package|refund|return|booking|"
    r"reservation|offer|mortgage|tenancy|landlord|visa|passport|complaint|payslip|pension|"
    r"insurance|quote|repair|job)\b|\bexam\s+results?\b|\bthe\s+(?:exam|interview|scan|audition|"
    r"appraisal|blood\s+test|driving\s+test|meeting|appointment|case|court|hearing|audition|"
    r"presentation|visit)\b|\b(?:my|our|his|her|their)\s+(?:blood\s+test|x-?ray|scan|results?)\b|"
    r"\bresults?\s+(?:from|of|at)\s+(?:(?:the|my|our|his|her|their)\s+)?"
    r"(?:doctor|gp|surgery|"
    r"hospital|scan|test|x-?ray|clinic|consultant|nurse|school|exam|dentist|vet)\b")
LIVE_A_YEAR = re.compile(r"\b(?:19|20)\d\d\b")
LIVE_OWN_DRAW = ("lottery", "lotto", "raffle", "sweepstake", "sweepstakes", "tombola",
                 "scratchcard", "scratch card", "bingo", "jackpot", "prize", "prizes",
                 "ticket", "tickets", "the draw", "numbers come up", "my bet", "the pools",
                 "competition", "euromillions")
LIVE_A_BARE_WIN = re.compile(r"\bdid\s+(?:i|we)\s+win\s*[?.!]*$")
LIVE_A_BARE_WINNING = re.compile(r"\bwho(?:['\u2019]?s|\s+is)?\s+winning\s*[?.!]*$")
LIVE_ANY_ACCIDENT = re.compile(r"\b(?:any|an?)\s+accidents?\b|\baccidents?\s+(?:on|at)\b")
LIVE_NEWS_LINES = (LIVE_NEWS_REPLY,)
def _the_scores_line():
    from ..knowledge.sport import _RESULTS_REPLY
    return (_RESULTS_REPLY,)
LIVE_LISTING_LINES = (
    "No live listings here, sorry. The TV guide on the box or the channel's own app has what is "
    "on and when, and the club's page has the kick-off and which side it is on.",)
LIVE_WHICH_RESULTS = (
    "Results of what - a match, an exam, or something you are waiting to hear about?",)


def _the_days_news(clean, asking):
    if (LIVE_A_YEAR.search(clean) or LIVE_NOT_WORLDS.search(clean)
            or _has(clean, LIVE_OWN_DRAW) or LIVE_A_BARE_WIN.search(clean)):
        return None
    played = _has(clean, LIVE_SPORT)
    if LIVE_LISTING_ASK.search(clean) and played:
        return LIVE_LISTING_LINES
    if LIVE_TABLE_ASK.search(clean) and played:
        return _the_scores_line()
    if (LIVE_RESULT_ASK.search(clean)
            or (played and LIVE_HOW_IT_WENT.search(clean))):
        if LIVE_A_BARE_WINNING.search(clean):
            return _the_scores_line()
        if played:
            return _the_scores_line()
        if LIVE_BARE_RESULTS.search(clean):
            return LIVE_WHICH_RESULTS
        return LIVE_NEWS_LINES
    if played and LIVE_TABLE_ASK.search(clean):
        return _the_scores_line()
    if LIVE_WORLD_ASK.search(clean) and not _the_scope_of_a_standing_ask(clean):
        return LIVE_NEWS_LINES
    return None

CANNOT_ANYTHING = (
    "No - nothing live from this end: no searching, no pages, no today's figures. What were you "
    "after? I'll tell you what I know, and where to look the rest up.",
    "That's right, I can't look anything up. What I've got is what I know and whatever you tell "
    "me. What did you want checked?",
    "No, sorry - no browsing and nothing live. Say what it is and I'll do what I can with it, and "
    "name the place that has the rest.",
)


BOT_CANNOT = re.compile(
    r"\b(?:you|u|ya)\s*(?:cant|can't|cannot|can not|couldnt|couldn't|dont|don't|doesnt|"
    r"doesn't|wont|won't|arent|aren't|isnt|isn't)\b", re.I)
BOT_CANNOT_DO = re.compile(
    r"\b(?:check|look|see|tell|know|find|search|access|view|pull|get|open|connect|browse|"
    r"read|show|say|able|online)\b", re.I)
BOT_CANNOT_LOOK = re.compile(
    r"\b(?:check|look|search|browse|online|internet|connect|open|view|access|find)\b", re.I)
CANNOT_ANYTHING_ASK = re.compile(
    r"\b(?:anything|any|whatever|at all|a thing|one thing|nothing)\b|"
    r"\b(?:can|could|do|does|are|will) (?:you|u)\b", re.I)
SO_NOTHING_LIVE = re.compile(
    r"\bso (?:no live (?:anything|news|weather|prices|times|scores)|nothing live|"
    r"no (?:news|weather|prices) (?:then|today|either))\b", re.I)

CANNOT_READ_YOURS = re.compile(
    r"\b(?:see|read|access|open|view|look (?:at|in)|check)\b[^.?!]{0,14}\b"
    r"(?:my|our|the)\s+(?:calendar|diary|inbox|emails?|mail|files?|folders?|notes?|photos?|"
    r"pictures?|messages?|texts?|documents?|screen|spreadsheets?)\b", re.I)
CANNOT_SEE_ANYTHING = re.compile(
    r"\b(?:see|read|look at)\b[^.?!]{0,12}\b(?:anything|nothing|a thing|any of it|any of them)\b"
    r"(?:\s+(?:at all|can you|could you|right|then|either|though|really|now))*[.?!]*\s*$", re.I)
CANNOT_SEE_ANYTHING_LINES = (
    "No, nothing on your side is visible to me - no pages, no photos, no files. I only get the "
    "words you type, and that is enough for most things: tell me what is in it.",
    "That's right, I can't see anything of yours. Type out the bit that matters and I'll work "
    "with it from there.",
)
CANNOT_YOUR_OWN = (
    "No, I can't see your diary from here - no calendar, no bookings, nothing of yours. Tell me "
    "what is in it and I'll work with that.",
    "Nothing of yours is in front of me, so no. Read out the lines that matter and I can help with "
    "what they say.",
    "I can't see your calendar or your plans, sorry - I only know what you tell me here. Give me "
    "the part that matters and it is as good as me having it.",
)


def _what_no_eyes_already_says(clean):
    for family, things in no_eyes.SEEING_FAMILIES.items():
        if re.search(r"\b(?:" + "|".join(re.escape(thing) for thing in things) + r")\b", clean):
            return no_eyes.CANNOT_SEE.get(family)
    return None


def _a_no_from_the_bot(clean):
    text = clean or ""
    if SO_NOTHING_LIVE.search(text):
        return True
    return bool(BOT_CANNOT.search(text) and BOT_CANNOT_DO.search(text))

CANNOT_THINGS = (
    ("travel", ("train", "trains", "bus", "buses", "tube", "tram", "flight", "flights",
                "traffic", "motorway")),
    ("news", ("news", "headline", "headlines", "the score", "scores")),
    ("prices", ("price", "prices", "the cost", "costs", "exchange rate", "the rate")),
)


def _the_live_thing_named(clean):
    for kind, words in CANNOT_THINGS:
        if _has(clean, words):
            for name, _phrases, options in LIVE_KINDS:
                if name == kind:
                    return options
    return None


def _the_bot_says_it_cannot(clean):
    return bool(BOT_CANNOT.search(clean or "") and BOT_CANNOT_LOOK.search(clean or ""))


FAVOURITE_WORDS = ("favourite", "favorite")


def _taste_lines():
    lines = set(FAVOURITE_GENERAL)
    for phrases, options in TASTES:
        if any("favourite" in phrase or "favorite" in phrase for phrase in phrases):
            lines.update(options)
    return frozenset(lines)


TASTE_LINES = _taste_lines()


BESIDE_THEIR_OWN = re.compile(r"\b(?:mine|can'?t decide|cant choose|not sure which)\b")


def reads_as_a_taste(text, memory=None):
    clean = _matchable(text)
    if not clean:
        return False
    if not _has(clean, OPINION_ASKS):
        try:
            clean = _matchable((understand(text, memory if isinstance(memory, dict) else {})
                                or {}).get("plain") or "")
        except Exception:
            return False
        if not clean or not _has(clean, OPINION_ASKS):
            return False
    if _is_about_the_persons_own_life(clean):
        return False
    if BESIDE_THEIR_OWN.search(clean):
        return False
    if not _has(clean, FAVOURITE_WORDS):
        return False
    try:
        reply = _taste(clean, memory if isinstance(memory, dict) else {}, False, False, "")
    except Exception:
        return False
    return bool(reply) and reply in TASTE_LINES
TRIP_ON_TABLE = re.compile(
    r"\b(?:driving|drive|travelling|traveling|heading|going|off|flying|cycling|walking|"
    r"getting the (?:train|bus|coach|ferry)|trip|journey)\b[^.?!]{0,24}?\b(?:to|in ?to)\b")


def _a_trip_is_on_the_table(memory):
    if not isinstance(memory, dict):
        return False
    for step in (1, 2):
        try:
            said = str(last_user(memory, step) or "").lower()
        except TypeError:
            said = str(last_user(memory) or "").lower() if step == 1 else ""
        if said and TRIP_ON_TABLE.search(said):
            return True
    return False


LIVE_SKY_NOUNS = frozenset(
    "weather wether weathr forecast forcast rain raining snowy snow sun sunny shine frosty frost "
    "icy ice foggy fog windy wind sleet hail stormy storm thunder drizzle cloudy overcast "
    "muggy humid misty mist".split())
LIVE_SKY_WORDS = LIVE_SKY_NOUNS | frozenset(
    "a an and the like is it what whats how hows will would be going gonna this next on at in "
    "for today tonight tomorrow morning afternoon evening night weekend weekends week weeks day "
    "days now later outside out there any much could might should please tell me know".split())


LIVE_SKY_PLACE = frozenset("in at near around for of".split())


def _the_sky_and_nothing_else(clean):
    words = [word.strip("'") for word in re.findall(r"[a-z']+", clean)]
    if not words or not _has(clean, LIVE_SKY_NOUNS):
        return False
    unknown = 0
    after_place = False
    for word in words:
        if word in LIVE_SKY_PLACE:
            after_place, unknown = True, 0
            continue
        if word in LIVE_SKY_WORDS:
            continue
        if not after_place or word in LIVE_INDOOR:
            return False
        unknown += 1
        if unknown > 2:
            return False
    return True


ROAD_TRAFFIC_WORDS = frozenset("""
    jam jams traffic busy closed closure closures shut roadworks accident accidents
    delay delays delayed diversion diversions queue queues queuing
""".split())


A_REPORT_OF_WHAT_HAPPENED = re.compile(
    r"\b(?:yesterday|last night|this morning|earlier|we sat|i sat|got stuck|was closed|were bad|"
    r"there were|there was|it took us|took me|sat in|stuck for|queued for|took ages|"
    r"took forever|took hours|missed the (?:train|bus|ferry|flight)|"
    r"(?:was|were) (?:awful|terrible|horrendous|grim|hell|murder|chaos|a mess|a joke|a nightmare|"
    r"bad|shut|rammed|chocka|packed)|(?:awful|terrible|horrendous|grim) (?:this morning|earlier|"
    r"yesterday|last night))\b")


def _a_road_named_with_traffic(clean):
    if not LIVE_ROAD_NAME.search(clean):
        return False
    if A_REPORT_OF_WHAT_HAPPENED.search(clean):
        return False
    return bool(set(clean.split()) & ROAD_TRAFFIC_WORDS)


THEIR_OWN_COUNT_WORDS = ("traffic", "footfall", "foot traffic", "visitors", "hits",
                         "analytics", "viewers", "stats")

A_COUNT_ASKED = re.compile(
    r"\b(?:how\s+(?:many|much|often)|whats?\s+(?:my|the)|what\s+is\s+my|where\s+(?:do|can)\s+i\s+"
    r"(?:see|find|check)|is\s+my\b.*\b(?:up|down)|how\s+is\s+my)\b")

THEIR_OWN_COUNT_HAPPENED = re.compile(
    r"\b(?:had|has|got|fell|dropped|went|rose|doubled|halved|visited|bought|sold|shipped)\b")
THEIR_OWN_COUNT_REPORT = re.compile(
    r"\b(?:yesterday|last\s+(?:night|week|month|year)|this\s+(?:morning|week|month)|all\s+day|"
    r"so\s+far|today|down|up)\b")


def _their_own_count(clean):
    if not _has(clean, LIVE_SITE_THING) or not _has(clean, THEIR_OWN_COUNT_WORDS):
        return False
    if A_COUNT_ASKED.search(clean):
        return True
    return not (THEIR_OWN_COUNT_HAPPENED.search(clean)
                or THEIR_OWN_COUNT_REPORT.search(clean))


A_COUNT_FELL = re.compile(
    r"\b(?:down|fell|falling|dropped|dropping|slowed|slowing|stalled|quiet|quietened|"
    r"nose\s?dived|collapsed|stopped|lower|fewer|half|dead|gone\s+quiet|went\s+quiet)\b")


def _their_own_thing(clean):
    return _has(clean, ("my", "our", "mine", "the shop", "the site")) or bool(
        A_COUNT_ASKED.search(clean))


def _their_own_count_fell(clean):
    if A_COUNT_ASKED.search(clean):
        return False
    return (_has(clean, LIVE_SITE_THING)
            and _has(clean, THEIR_OWN_COUNT_WORDS + ("sales", "orders"))
            and bool(A_COUNT_FELL.search(clean)))



def _live(clean, asking, memory=None):
    from . import place_facts
    place = place_facts.the_line(clean)
    if place:
        return place
    if _has(clean, LIVE_NOT):
        return None
    understood = (memory or {}).get("understood") if isinstance(memory, dict) else None
    if isinstance(understood, dict) and understood.get("over_time") is False:
        return None
    lookup = a_postcode_lookup(clean)
    if lookup:
        return lookup
    if clean.strip(" ?!.") in ("news", "the news", "and the news"):
        return LIVE_NEWS_LINES
    from . import news_ask
    if news_ask.reads_as_an_ask_for_the_news(clean):
        return LIVE_NEWS_LINES
    if (not asking and not _has(clean, LIVE_STRONG)
            and not LIVE_ANY_ACCIDENT.search(clean)
            and not LIVE_A_BARE_WINNING.search(clean)
            and not _the_sky_and_nothing_else(clean)
            and not _a_road_named_with_traffic(clean)
            and not _their_own_count(clean)
            and not _their_own_count_fell(clean)):
        if RECORD_CHECK.search(clean) and _their_own_phrase(clean, RECORD_THINGS):
            record = _their_own_record(clean, False)
            if record:
                return record
        return None
    mine = _their_own_bill(clean) or _their_own_points(clean)
    if mine:
        return mine
    for kind, phrases, options in LIVE_KINDS:
        if kind in ("site-stats", "site-stats-down"):
            if kind == "site-stats-down":
                if _their_own_count_fell(clean) and _their_own_thing(clean):
                    return options
                continue
            if _their_own_count(clean) and _their_own_thing(clean):
                return options
            continue
        if kind == "weather":
            if _has(clean, LIVE_INDOOR) and not _has(clean, LIVE_WEATHER_WORDS):
                continue
            if (_has(clean, phrases) or LIVE_WEATHER_DAY.search(clean)
                    or (_has(clean, LIVE_SKY) and not _has(clean, LIVE_SKY_OFF)
                        and not LIVE_SKY_WHY.search(clean))
                    or (_has(clean, LIVE_WEAR)
                        and (_a_bare_wear_ask(clean) if _has(clean, LIVE_TAKE_ASK)
                             else _has(clean, LIVE_SOON))
                        and not _has(clean, LIVE_SETTING))):
                return options
            continue
        if kind == "news" and LIVE_A_BARE_WINNING.search(clean):
            continue
        if kind == "news" and LIVE_NOT_WORLDS.search(clean):
            continue
        if kind == "roads":
            if _has(clean, LIVE_ROADS_NOT):
                continue
            if _has(clean, phrases) or (LIVE_ROAD_NAME.search(clean)
                                        and not _has(clean, LIVE_PAPER_WORDS)):
                return options
            if _has(clean, LIVE_ROAD_WORDS) and _has(clean, LIVE_DELAY_WORDS):
                return options
        if kind == "journey":
            if _has(clean, phrases) and (_has(clean, LIVE_JOURNEY_ENDS)
                                         or _a_trip_is_on_the_table(memory)):
                return options
            continue
        if kind == "travel":
            if _has(clean, LIVE_ROADS_NOT):
                continue
            if _has(clean, phrases) or (_has(clean, LIVE_TRAVEL_WORDS)
                                        and _has(clean, LIVE_DELAY_WORDS)):
                return options
            if _has(clean, LIVE_TRAVEL_WORDS) and (OWN_TIME_ASK.search(clean)
                                                   or MY_TIME_ASK.search(clean)):
                return options
            continue
        if kind == "prices":
            rate = quantity.the_rate_they_asked_about(clean, memory)
            if rate and not quantity.the_thing_they_pay_for(clean):
                return (rate,)
            verdict = _a_price_wants_a_verdict(clean, memory)
            if verdict:
                return verdict
            before = str(last_user(memory) or "") if isinstance(memory, dict) else ""
            priced = prices.the_price_reply(clean, phrases, before.lower(), options)
            if priced:
                return priced
            if rate:
                return (rate,)
            continue
        if kind == "hours":
            if _has(clean, LIVE_NOT_HOURS):
                continue
            if _names_a_venue(clean) and (LIVE_HOURS_ASK.search(clean)
                                           or LIVE_YES_NO_OPEN.search(clean)):
                return options
            if OWN_TIME_ASK.search(clean):
                if not (_has(clean, OWN_PLACE) or OWN_VERB_OPEN.search(clean)) or _has(clean, OWN_PERSON):
                    continue
            if _has(clean, LIVE_SPORT) and LIVE_LISTING_ASK.search(clean):
                continue
        if _has(clean, phrases):
            return options
    return _the_days_news(clean, asking) or _their_own_record(clean, asking)


WORDING_ASKS = re.compile(
    r"\b(help (me )?(to )?(word|phrase|say)|word (a|an|the|this|that)|word it|phrase it|"
    r"how do i (word|phrase|say)|"
    r"put (it|this|that) in(to)? (a|an|words)|what to write)\b")
WORDING_SAYS = re.compile(r"\bwhat (should|do|can) i say\b")
WORDING_ASKS_WHO = re.compile(r"\bwhat (should|do|can) i (say|ask|tell)\b")
A_GROUP_OF_PEOPLE = (
    r"kids|children|child|family|families|team|staff|neighbours?|neighbors?|in[-\s]?laws|"
    r"grandparents|grandchildren|grandkids|twins|siblings|relatives|parents|friends|"
    r"colleagues|boys|girls|lads|folks|guys")
A_WHOLE_ROOM = r"everyone|everybody|anyone|anybody|someone|somebody"
WORDING_TELL = re.compile(
    r"\bhow\s+(?:do|should|can|could|would|might)\s+i\s+tell\s+"
    r"(?!\w*\s+(?:if|whether)\b)"
    r"(?:(?:my|his|her|their|our|your)\b"
    r"|the\s+(?:doctor|gp|nurse|vet|police|landlord|boss|manager|bank|school|council|teacher|"
    r"colleague|midwife|consultant|dentist)\b"
    r"|the\s+(?:" + A_GROUP_OF_PEOPLE + r")\b(?!\s+from\b)"
    r"|him|her|them|people|" + A_WHOLE_ROOM + r")\b"
    r"|\bwhat\s+(?:do|should|can|could)\s+i\s+tell\s+"
    r"(?:my|his|her|their|our|your|him|her|them|" + A_WHOLE_ROOM + r"|"
    r"the\s+(?:" + A_GROUP_OF_PEOPLE + r"))\b(?!\s+(?:if|whether)\b)")
A_DOUBT_IN_FRONT = re.compile(
    r"\b(?:idk|i\s+dont\s+know|i\s+do\s+not\s+know|i\s+dunno|dunno|no\s+idea|"
    r"i\s*ve\s+no\s+idea|i\s+have\s+no\s+idea|not\s+sure|i'?m\s+not\s+sure)\b")
THE_SAME_ASK_AS_A_STATEMENT = ((re.compile(r"\bhow\s+to\b"), "how do i"),
                              (re.compile(r"\bwhat\s+to\b"), "what should i"))
TELL_NOT_WORDS = re.compile(
    r"\b(?:difference|apart|apart\s+from)\b"
    r"|\b(?:dog|cat|puppy|kitten|puppies|kittens|horse|rabbit|parrot)s?\s+"
    r"(?:off|to\s+(?:stop|sit|stay|come|leave|drop|wait|heel))\b")
def _the_ask_for_words_behind_a_doubt(clean):
    if not A_DOUBT_IN_FRONT.search(clean) or _reads_as_heavy_news(clean):
        return False
    said = clean
    for pattern, instead in THE_SAME_ASK_AS_A_STATEMENT:
        said = pattern.sub(instead, said)
    if said == clean or TELL_NOT_WORDS.search(said):
        return False
    return bool(WORDING_ASKS.search(said) or WORDING_SOMEONE.search(said)
                or WORDING_TELL.search(said)
                or (WORDING_SAYS.search(said) and WORDING_WHERE.search(said)))


def _asks_for_words(said, words):
    return bool(WORDING_ASKS.search(said) or WORDING_SOMEONE.search(said)
                or (WORDING_TELL.search(said) and not TELL_NOT_WORDS.search(said))
                or _the_ask_for_words_behind_a_doubt(said)
                or (WORDING_SAYS.search(said)
                    and (WORDING_WHERE.search(said) or len(words) <= 6)))


TELL_HARD = re.compile(
    r"\b(divorce|separat\w*|split up|break(ing)? up|broke up|leav(e|ing) (him|her|them)|"
    r"quit|resign\w*|fired|sacked|redundan\w*|lost (my|his|her|their) job|cancer|dying|died|terminal|miscarr\w*|"
    r"pregnan\w*|affair|cheat\w*|debt\w*|bankrupt\w*|autis\w*|diagnos\w*|addict\w*|"
    r"gay|lesbian|trans|transgender|non-?binary|bisexual|coming out|came out)\b")
WORDING_WHERE = re.compile(
    r"\b(to (my|the|him|her|them|his|our|your)|when i (ring|call|phone|text|email|speak|write|ask)|"
    r"text|message|email|letter|card|note)\b")
INDIRECT = re.compile(r"\s(?:about|over|of|on|at|to)\s+(?:who|what|where|when|why|how|whether)\s")
ASK_SHAPES = re.compile(
    r"\s(who|what|where|when|why|how|which)\s+(should|do|does|can|could|would|will|might|"
    r"is|are|am)\s"
    r"|\s(should|shall|do|does|can|could|would|will|did)\s+(i|we|you)\s"
    r"|\sany (idea|ideas|advice|tips|suggestions|thoughts)\s"
    r"|\swhat (do|should|can|would) (you|i)\s"
    r"|\sis it worth\s|\sworth (it|doing|paying|getting|fixing|buying)\s")
GREETING_OPEN = re.compile(
    r"^\s*(?:(?:nice|good|great|pleased|lovely|glad|happy|grand)\s+to\s+(?:meet|see|hear\s+from)"
    r"\s+(?:you|u|ya)\b"
    r"|(?:good|great|lovely|nice)\s+to\s+have\s+you\b"
    r"|how\s+(?:are|r)\s+(?:you|u|ya)\b"
    r"|how(?:'s|s|\s+is)\s+(?:it\s+going|things|tricks|you\s+doing|your\s+day)\b"
    r"|how\s+do\s+you\s+do\b"
    r"|long\s+time\s+no\s+see\b)", re.I)


def _reads_as_greeting(words, text=""):
    plain = [w.replace("'", "") for w in words]
    if not plain:
        return False
    if plain[0] in GREETING_WORDS:
        return True
    if GREETING_OPEN.match(text or " ".join(plain)):
        return not (reads_as_good_news((text or "").lower()) or reads_as_bad_news((text or "").lower()))
    return " ".join(plain[:2]) in ("good morning", "good afternoon", "good evening", "good day")


def _reads_as_taste(clean, words):
    if " or " not in clean:
        return False
    if len(words) > 6:
        return False
    return not any(word in clean.split() for word in QUESTION_WORDS)


def _blackout_words(clean, words, said):
    if _names(words, said, DARK_THING) or BLACKED_OUT_A_THING.search(clean):
        return False
    someone = bool(BLACKOUT_PERSON.search(clean))
    for shape, needs_person in BLACKED_OUT_SIGHT:
        if re.search(shape, clean):
            return someone or not needs_person
    return False


def _action(clean, memory):
    said = " " + re.sub(r"[^a-z0-9']", " ", clean) + " "
    words = said.replace("'", "").split()
    routine = bool(ROUTINE_WAKE.search(clean))
    story = reads_as_a_story(clean)
    if CANT_WAKE.search(clean) and not _names(words, said, GADGET_WORDS) and not routine \
            and not story:
        return EMERGENCY_ANSWER
    tail_only = UNRESPONSIVE_TAIL.search(clean) and not FEED_TAIL.search(clean)
    choking_thing = CHOKE_MACHINE.search(clean) and not CHOKE_BODY.search(clean)
    if _names(words, said, EMERGENCY_WORDS) and not _names(words, said, GADGET_WORDS) \
            and not choking_thing and not tail_only and not routine and not story \
            and not (OVERDOSE_FOOD.search(clean) and not OVERDOSE_DRUG.search(clean)) \
            and not CHOKE_ON_A_WORD.search(clean) \
            and not (OVERDOSE_OF_A_TREAT.search(clean) and not OVERDOSE_A_PILL.search(clean)) \
            and not _the_thing_is_choking(clean, words):
        return EMERGENCY_ANSWER
    if _names(words, said, FLOPPY_WAKE) and _names(words, said, TIRED) \
            and not _names(words, said, GADGET_WORDS):
        return EMERGENCY_ANSWER
    if not _names(words, said, LANGUAGE_FLUENCY) and (
            _names(words, said, GAS_WORDS) or (
                _names(words, said, FUME_WORDS) and _names(words, said, FUEL_WORDS))) \
            and not _names(words, said, PETROL_WORDS):
        return GAS_ANSWER
    animal = any(word in ANIMALS or word.rstrip("s") in ANIMALS for word in words)
    went_under = (PASSED_OUT.search(clean) and not BLACKED_OUT_A_THING.search(clean)
                  and not PASSING_OUT_A_THING.search(clean)) \
        or _blackout_words(clean, words, said)
    if went_under and not animal and not _names(words, said, LAUGHING_WORDS):
        if _names(words, said, CHILD_FAINT):
            return _choose([CHILD_FAINT_ANSWER], memory, clean)
        if FAINT_COMING.search(clean):
            return _choose([FAINT_COMING_ANSWER + "."], memory, clean)
        return _choose([PASSED_OUT_ANSWER + "."], memory, clean)
    return None


RECALL_NAME = (
    re.compile(r"\bwhat\s+(?:did|do)\s+(?:i|we)\s+(?:call|name)\s+"
               r"(?:my|our|his|her|their|it|them|him|us|this|that)\b"),
    re.compile(r"\bwhat(?:'s| is| was)?\s+(?:my|our)\s+\w+(?:'s)?\s+(?:name|called)\b"),
    re.compile(r"\bwhat(?:'s| is| was)\s+(?:my|our)\s+(?:name|called)\b"),
    re.compile(r"\b(?:remember|recall)\b[^.?!]{0,30}\b(?:name|called|call)\b"),
    re.compile(r"\bwhat\s+(?:did|do)\s+(?:i|we)\s+(?:say|tell(?: you)?)\b[^.?!]{0,30}"
               r"\b(?:name|called|call)\b"),
)
RECALL_BARE = re.compile(r"^(?:and |so |but )?(?:my|our)\b[^.?!]{0,24}\bnames?\b")


GAVE_A_NAME = (
    re.compile(r"\b(?:named|called)\s+(?:my|our|his|her|their|the)\s+(\w+)\s+(.+?)"
               r"\s*[.!]*$", re.I),
    re.compile(r"\b(?:my|our)\s+(\w+)(?:'s)?\s+is\s+((?:mr|mrs|ms|miss|dr)\.?\s+\w+|\w+)"
               r"\s*[.!]*$", re.I),
    re.compile(r"\b(?:my|our)\s+([\w-]+)\s+(?:is|was|are|were)\s+(?:called|named)\s+"
               r"(\w+)\s*[.!]*$", re.I),
    re.compile(r"\b(?:named|called)\s+(\w+)\s*[.!]*$", re.I),
)


def _name_given_before(clean, memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)][-2:]
    if not turns:
        return ""
    asked = {w for w in re.sub(r"[^a-z0-9 ]", " ", str(clean or "").lower()).split()
             if w not in ASK_ONLY}
    for turn in reversed(turns):
        said = str(turn.get("user") or "").strip()
        if not said:
            continue
        name, subject = "", set()
        for rule in GAVE_A_NAME:
            found = rule.search(said)
            if not found:
                continue
            groups = found.groups()
            if len(groups) == 2:
                subject, tail = {groups[0].lower()}, groups[1].strip()
            else:
                tail = groups[0].strip()
            words = [w for w in tail.replace(",", " ").split() if w]
            if not words:
                continue
            name = words[-1]
            subject |= {w.lower() for w in words[:-1]}
            if len(words) > 1 and words[0].lower() in ("mr", "mrs", "ms", "miss", "dr"):
                name = " ".join(words[-2:])
            break
        lowered = re.sub(r"[^a-z]", "", name.lower())
        if not name or lowered in NOT_A_NAME or lowered in ASK_ONLY:
            continue
        if not asked or not subject or (asked & subject):
            if name.lower() not in said:
                continue
            bits = [b[:1].upper() + b[1:] for b in name.split()]
            return " ".join(bits)
    return ""


def _asks_a_name_back(clean, words=()):
    text = " ".join(str(clean or "").lower().split())
    mine = words or re.sub(r"[^a-z0-9' ]", " ", text).split()
    if not set(mine) & {"i", "we", "my", "our"}:
        return False
    if set(mine) & {"should", "shall", "could"}:
        return False
    if any(phrase in text for phrase in WORD_ANYWHERE):
        return False
    if any(rule.search(text) for rule in RECALL_NAME):
        return True
    return bool(RECALL_BARE.search(text) and "?" in text)


MOVE_ASK = re.compile(
    r"\bwhat\s+(?:else\s+)?(?:can|could|should|shall|do)\s+(?:i|we|you)\s+(?:do|try)\b"
    r"|\bwhat\s+(?:now|next)\b"
    r"|\bwhere\s+(?:do|should|can)\s+(?:i|we)\s+(?:start|begin)\b"
    r"|\bwhats\s+the\s+(?:first|next)\s+(?:thing|step|move)\b"
    r"|\bhow\s+(?:do|can|should)\s+(?:i|we)\s+(?:start|begin|prepare|get\s+going)\b", re.I)


def _asks_for_the_move(line):
    return bool(MOVE_ASK.search(str(line or "")))


def _says_it_already(clean, words, memory):
    if _asks_for_the_move(clean):
        return False
    if not _answered_already(memory) or _hedged_recently(memory):
        return False
    if not words or len(words) > 10:
        return False
    said = set(word for word in _flat_words(_the_answer_above(memory)) if word not in POINTING)
    if not said:
        return False
    mine = [word for word in words if word not in POINTING and len(word) > 2]
    if not mine:
        return False
    missing = [word for word in mine if not (word in said or word.rstrip("s") in said
                                             or word + "s" in said)]
    here = len(mine) - len(missing)
    if not here or here * 2 < len(mine):
        return False
    return not any(_names_a_new_thing(word, clean) for word in missing)


def _names_a_new_thing(word, clean):
    words = clean.split()
    for i, here in enumerate(words):
        if here != word and here.rstrip("s") != word:
            continue
        before = words[i - 1] if i else ""
        after = words[i + 1] if i + 1 < len(words) else ""
        if before in RULED_OUT_DETERMINER and after not in PARTICLE:
            return True
        if here.endswith("s") and len(here) > 3 and here != words[0]:
            return True
    return False


def content_words(text):
    words = _flat_words(text)
    return [word for word in words if word not in POINTING and len(word) > 2]


def _flat_words(text):
    return re.sub(r"[^a-z0-9 ]", " ", str(text or "").lower()).split()


def memory_bot(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict) and t.get("bot")]
    return str(turns[-1].get("bot")) if turns else ""


def says_it_already(text, memory):
    understood = memory.get("understood")
    if not isinstance(understood, dict):
        understood = understand(text, memory)
    clean = understood.get("clean") or " ".join(str(text or "").lower().split())
    words = understood.get("words") or clean.split()
    try:
        return _says_it_already(clean, list(words), memory)
    except Exception:
        return False


def is_the_answer_shorter(reply, last):
    try:
        return why.is_the_answer_shorter(reply, last)
    except Exception:
        return False


def is_said_it_already(reply):
    flat = " ".join(_flat_words(reply))
    return any(flat == " ".join(_flat_words(line))
               for line in HELP_ALREADY + SAME_AGAIN)


POINTING_WORDS = frozenset("""
    what whats how why which who whos whom when whens where wheres
    that this it those these one ones thats
    mean means meant meaning explain work works working come
    do does did is are was were be been am
    you u about by for to of in on at with
    much many long again then please exactly really about
    so ok okay oh ah right well and but
    say tell know
""".split())
POINTERS = frozenset("that this it those these one ones thats".split())
MEAN_WORDS = frozenset("mean means meant meaning explain".split())
POINTING_ASK = frozenset("what whats how why which who whos when whens where wheres".split())
POINTING_IDIOMS = frozenset(["how come", "how comes", "what for", "how so"])

POINTING_LINES = (
    "I can't see what you're looking at, so 'that' could be anything. Put the thing in a "
    "couple of words and I'll answer it properly.",
    "There's nothing on my side for 'that' to land on - tell me the thing itself and I'll take "
    "it from there.",
    "'That' could be a lot of things and I've none of them in front of me - say the thing "
    "you mean and I'll come at it properly.",
    "'That' has nothing behind it here. What is the thing you're pointing at?",
)


def _points_at_nothing(clean, memory, repaired=""):
    for line in (clean, repaired):
        said = re.sub(r"[^a-z0-9' ]", " ", str(line or "").lower())
        words = said.replace("'", "").split()
        if not words or len(words) > 6:
            continue
        if not set(words) <= POINTING_WORDS:
            continue
        points = set(words) & POINTERS
        asks = set(words) & MEAN_WORDS
        if not points and not asks and " ".join(words) not in POINTING_IDIOMS:
            continue
        if not set(words) & POINTING_ASK and not asks:
            continue
        if ("you" in words or "u" in words) and not asks:
            continue
        return _nothing_to_point_at(memory)
    return False


def _nothing_to_point_at(memory):
    if not isinstance(memory, dict) or not memory:
        return True
    if in_a_safety_thread(memory) or _grief_thread(memory) or _thread_is_about_the_body(memory):
        return False
    if _answered_recently(memory):
        return False
    if _a_previous_line_named_something(memory):
        return False
    if "?" in (last_bot(memory) or ""):
        return False
    return True


def _a_previous_line_named_something(memory, look_back=3):
    from ..memory.topics import keywords

    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)][-look_back:]
    return any(keywords(str(turn.get("user") or "")) for turn in turns)

OFFERS_TO_FIX_THEMSELVES = re.compile(
    r"\b(?:fix(?:ing|ed)?|mend(?:ing|ed)?|patch(?:ing|ed)?|servic(?:e|ing)|replace)"
    r"\s+(?:it\s+)?(?:myself|me|yourself|himself|herself)\b")


def _offers_to_fix_themselves(clean):
    return bool(OFFERS_TO_FIX_THEMSELVES.search(clean or ""))


def is_a_forecast(said):
    head = str(said or "").strip()
    if not head:
        return False
    return any(head.startswith(line.split("{")[0]) for pool in FORECAST_POOLS for line in pool)


def _the_forecast_subject(clean, memory):
    recent = [str(t.get("user") or "").lower()
              for t in ((memory or {}).get("turns") or []) if isinstance(t, dict)][-3:]
    asked_about_self = bool(FORECAST_I_ASK.search(clean or ""))
    for said in [clean] + ([] if asked_about_self else list(reversed(recent))):
        found = FORECAST_RELATION.search(said or "")
        if found:
            relation = found.group(1)
            return ("pet" if relation in ANIMALS else "person"), "your " + relation
    if asked_about_self:
        return "self", "you"
    if _thread_is_about_a_pet(memory):
        return "pet", "them"
    whose = _whose_body(clean, recent)
    if whose == "mine":
        return "self", "you"
    if whose == "theirs":
        return "person", "them"
    if FORECAST_HE_SHE.search(clean or ""):
        return "person", "them"
    if _a_body_in_the_thread(memory):
        return "self", "you"
    if _thread_is_about_someone_else(memory) or _thread_is_about_a_person(memory):
        return "person", "them"
    return None, ""


def _without_the_things_named_after_a_body(text):
    return BODY_WORD_FOR_A_THING.sub(" ", str(text or ""))


def _whose_body(clean, recent):
    for said in [clean] + list(reversed(recent)):
        tokens = re.findall(r"[a-z']+", _without_the_things_named_after_a_body(
            _without_the_forecast_verb(said or "")))
        for at, token in enumerate(tokens[:-1]):
            if token == "my" and tokens[at + 1] in FORECAST_BODY_WORDS:
                return "mine"
        if set(tokens) & FORECAST_BODY_WORDS and (set(tokens) & _THREAD_PEOPLE
                                                  or FORECAST_HE_SHE.search(said or "")):
            return "theirs"
    return ""


def _without_the_forecast_verb(line):
    found = FORECAST.search(line or "")
    if not found:
        return line or ""
    return (line[:found.start()] + " " + line[found.end():]).strip()


def _thread_said(memory, look_back=4):
    turns = [t for t in (memory or {}).get("turns") or [] if isinstance(t, dict)][-look_back:]
    return " ".join(str(turn.get("user") or "").lower() for turn in turns)


def _a_body_in_the_thread(memory, look_back=4):
    for turn in [t for t in (memory or {}).get("turns") or [] if isinstance(t, dict)][-look_back:]:
        said = str(turn.get("user") or "").lower()
        said = _without_the_things_named_after_a_body(_without_the_forecast_verb(said))
        words = _without_the_idioms(said)
        if (words & BODY_PARTS or words & SYMPTOM_WORDS or words & HEALTH_WORDS
                or words & FORECAST_ILL or FORECAST_OFF_THEIR_FOOD.search(said)
                or FORECAST_A_FALL.search(said)):
            return True
    return False


def _a_hard_patch_in_the_thread(clean, memory, look_back=3):
    said = [str(clean or "").lower()]
    said += [str(t.get("user") or "").lower()
             for t in (memory or {}).get("turns") or [] if isinstance(t, dict)][-look_back:]
    return any(FORECAST_STRUGGLE.search(line) for line in said if line)


def _forecast_pool(clean, repaired, memory):
    line = next((said for said in (clean, repaired)
                 if said and FORECAST.search(said)), "")
    if not line or FORECAST_PERMISSION.search(line) or FORECAST_DURATION.search(line):
        return None
    if _in_a_loss_thread(memory) or _grief_thread(memory):
        return None
    kind, who = _the_forecast_subject(line, memory)
    if in_a_safety_thread(memory):
        return [phrase.format(who=who or "you") for phrase in FORECAST_AFTER_SAFETY]
    if kind == "pet":
        if not (_a_body_in_the_thread(memory) or FORECAST_PET_HARM.search(_thread_said(memory))):
            return None
        return [phrase.format(who=who) for phrase in FORECAST_PET]
    if kind == "person":
        if an_outcome_asked_about_someone(clean, memory):
            return None
        if _a_body_in_the_thread(memory):
            return [phrase.format(who=who) for phrase in FORECAST_PERSON]
        if _a_hard_patch_in_the_thread(line, memory):
            later = globals().get("_a_hard_time_and_not_a_body")
            if later and later(memory, line):
                return None
            return [phrase.format(who=who) for phrase in FORECAST_SOMEONE_STRUGGLING]
        return None
    if kind == "self":
        recent = [str(turn.get("user") or "").lower()
                  for turn in ((memory or {}).get("turns") or []) if isinstance(turn, dict)][-3:]
        if _the_threads_who(memory):
            return None
        if _whose_body(clean, recent[-1:]) != "mine" and (
                _a_hard_patch_in_the_thread(line, memory) or _thread_is_about_someone_else(memory)):
            return list(FORECAST_SELF_STRUGGLING)
        return list(FORECAST_SELF)
    return None


def _unknown(understood, memory, clean):
    from .fallback_pools import _unknown as _moved
    reply = _moved(understood, memory, clean)
    a_hedge = _is_a_hedge(reply)
    if a_hedge or _asks_about_this_chat(clean):
        about_me = _a_question_about_the_bot(clean, memory)
        if about_me:
            return about_me
        if not a_hedge:
            return reply
        stuck = _what_to_do_about(clean, memory)
        if stuck:
            return stuck
        no_subject = _an_ask_with_no_subject(clean, memory)
        if no_subject:
            return no_subject
        lead = (_the_lead_and_the_route(clean, memory)
                if POINTER_HEDGE.search(reply or "")
                and not NAMES_WHERE_TO_ASK.search(reply or "") else "")
        if lead:
            return lead
    return reply


TIPS_ASKS = re.compile(r"\b(any|some|got any|need some|need any|want some)\s+(tips|tip|advice|"
                       r"pointers|suggestions|ideas|tricks|trick)\b")
NOT_A_TIPS_ASK = re.compile(r"\btricks?\s+or\s+treat\b")


def _is_a_tips_ask(line):
    return bool(TIPS_ASKS.search(line)) and not NOT_A_TIPS_ASK.search(line)
TIPS_SUBJECT_FOR = re.compile(r"\b(?:tips?|advice|suggestions?|recommendations?|ideas?)\s+"
                              r"(?:for|on|about|with)\s+(?P<subject>.+)$")
TIPS_SUBJECT_TAIL = re.compile(
    r"(?:^|[,.;!?]\s*|\s)(?:any\s+|some\s+|got any\s+)?(?:tips?|advice|suggestions?|"
    r"recommendations?|ideas?)\b.*$")
TIPS_LEAD = re.compile(r"^(?:so|and|but|ok|okay|well|hi|hey|also|then|just)\s+")
TIPS_ANY_IDEA = re.compile(r"\b(?:any|some|got any|need some|need any|want some)\s+ideas?\b")
TIPS_WORD = re.compile(r"\b(?:tips?|advice|suggestions?|recommendations?)\b")
TIPS_REQUEST = re.compile(r"^(?:give|tell|show|send|find|list|suggest|recommend|get)\s+"
                          r"(?:me|us)\s+")
TIPS_SOON = re.compile(r"\b(?:first|before|wedding|holiday|interview|exam|lesson|marathon|"
                       r"race|move|trip|course|test|appointment|driving\s+lesson|birthday|"
                       r"anniversary|christmas|funeral|hen\s+do|stag\s+do|due\s+date)\b")


def _hedged_recently(memory, look_back=3):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)][-look_back:]
    for turn in turns:
        said = str(turn.get("bot") or "").strip()
        if said and any(said[:40] == line[:40] for line in UNKNOWN):
            return True
        if said and any(punt in said.lower() for punt in PUNT):
            return True
    return False


VIEW_ASKS = re.compile(
    r"\b(?:your|ur|yur)\s+(?:(?:honest|own|real|true|personal)\s+)?"
    r"(?:view|opinion|take|thoughts|verdict|read)\b"
    r"|\bwhat(?:'s|s| is)?\s+(?:is\s+|was\s+)?(?:your\s+|the\s+|a\s+)?"
    r"(?:(?:honest|own|real|true|personal)\s+)?(?:view|opinion|take|thoughts|verdict)\b"
    r"|\bwhat\s+(?:do|would|d)\s*(?:you|u|ya)\s+(?:reckon|think|say)\b"
    r"|\b(?:honest|own|real|true)\s+(?:view|opinion|take|thoughts|verdict)\b"
    r"|\b(?:honest|own|real|true)\s+answers?\b"
    r"|\b(?:your|ur|yur)\s+(?:honest|own|real|true|personal)\s+answers?\b"
    r"|\bwhat\s+would\s+(?:you|u)\s+do\b"
    r"|\b(?:view|opinion|take|thoughts|verdict)\s+on\s+(?:it|that|this)\b")


VIEW_NOT_AN_ANSWER = re.compile(
    r"^(?:sorry\b|i'm sorry\b|im sorry\b|so sorry\b|that sounds\b|that's rough\b|"
    r"thats rough\b|that's hard\b|thats hard\b|that's a hard one\b|that's a lot\b|"
    r"ugh\b|ouch\b|hope\b|i'm here\b|im here\b|take care\b|nothing has to be decided\b|"
    r"thanks\b|thank you\b|got it\b|noted\b|i'm listening\b|im listening\b|understood\b)")


def _in_a_pool(text, pools=(NOT_AN_ANSWER,)):
    said = _plain(text)
    return bool(said) and any(_plain(line) and said.startswith(_plain(line))
                              for pool in pools for line in pool)


FLOOR_CLAUSE = re.compile(
    r"^(?:(?:go|carry)\s+on\b|tell\s+me\s+more\b|say\s+more\b|keep\s+going\b|go\s+ahead\b"
    r"|ask\s+away\b|i'?m\s+listening\b|i\s+am\s+listening\b|i'?m\s+here\b"
    r"|take\s+your\s+time\b|over\s+to\s+you\b|what'?s\s+on\s+your\s+mind\b"
    r"|i'?ll\s+do\s+my\s+best\b|spill\s+it\b|i'?m\s+all\s+ears\b)", re.I)
FLOOR_COURTESY = re.compile(
    r"^(?:of\s+course|sure|ok|okay|right|yes|no|well|please|thanks|thank\s+you|"
    r"no\s+need(?:\s+to\s+apologise)?|you'?re\s+not\s+dumping\s+anything\s+on\s+me|"
    r"don'?t\s+apologise(?:\s+for\s+that)?|nothing\s+to\s+be\s+sorry\s+about|"
    r"no\s+problem|you'?re\s+welcome|that'?s\s+what\s+i'?m\s+here\s+for|"
    r"i'?d\s+rather\s+hear\s+it\s+than\s+not)$", re.I)


HEALTH_STEMS = ("tire", "exhaust", "sleep", "insomnia", "anxi", "depress", "stress", "panic",
                "symptom", "sick", "unwell", "nause", "dizzi", "swell", "inflam")


WHAT_TO_DO_ABOUT = re.compile(
    r"^\W*(?:(?:and|but|so|oh|ok|okay|well|right|alright|honestly|anyway|also)\W+)*"
    r"what(?:'?s|\s+is)?\s+(?:should|shall|can|could|would|do|did|will|am\s+i)\s+"
    r"(?:i\s+)?(?:do|say|tell)\s+about\s+(?P<thing>[^?.!]+)$", re.I)
NOT_WHAT_TO_DO_ABOUT = re.compile(
    r"\b(?:die|died|dying|death|kill\w*|suicid\w*|hurt\w*|harm\w*|abus\w*|hit|hits|hitting|"
    r"beaten|chest|breath\w*|bleed\w*|overdose\w*|emergency|999|111)\b", re.I)


THING_TAIL = re.compile(
    r"\s+(?:i|i've|ive|im|i'm|we|i\b.*|that|which|who|he|she|they|you|my|me|it)\b.*$", re.I)


def _the_thing_alone(thing):
    said = _yours(" ".join(str(thing or "").split()).strip(" ,.;:-"))
    cut = THING_TAIL.sub("", said).strip(" ,.;:-")
    return cut or said


WHAT_TO_DO_ABOUT_FRAMES = (
    "{thing} - what's the bit of it you'd want to sort first?",
    "Where would you want to start with {thing}?",
    "{thing} - what's the part that's bothering you most?",
    "{thing} - what would you want to change first?",
)


def _what_to_do_about(clean, memory=None):
    line = " ".join(str(clean or "").split())
    found = WHAT_TO_DO_ABOUT.match(line)
    if not found:
        return ""
    thing = found.group("thing").strip(" ,.;:-")
    if not thing or NOT_WHAT_TO_DO_ABOUT.search(line):
        return ""
    words = set(re.findall(r"[a-z']+", line.lower()))
    if (words & SYMPTOM_WORDS or words & BODY_PARTS or words & HEALTH_WORDS
            or any(w.startswith(HEALTH_STEMS) for w in words)):
        return ""
    if thing.lower().split()[0] in NOT_A_THING_ASKED:
        return ""
    if len(thing.split()) > DISLIKE_TOO_LONG:
        return ""
    named = _capital(_the_thing_alone(thing))
    if not named or named.lower().split()[0] in NOT_A_THING_ASKED:
        return _choose(DITHER_OPEN_LINES, memory, clean)
    lines = tuple(frame.format(thing=named if frame.startswith("{thing}") else named.lower())
                  for frame in WHAT_TO_DO_ABOUT_FRAMES)
    return _choose(lines, memory, clean)


ABOUT_THE_BOT_NAMED = re.compile(
    r"^\W*(?:(?:and|but|so|oh|ok|okay|well|right|alright|honestly|anyway|also)\W+)*"
    r"(?:how\s+(?:are|do)\s+(?:you|u|ya)\s+feel(?:ing)?"
    r"|what\s+do\s+(?:you|u|ya)\s+(?:make|think)\s+of)"
    r"\s+(?:about|of|with|on)\s+(?P<thing>[^?.!]+)$"
    r"|^\W*(?:(?:and|but|so|oh|ok|okay|well|right|alright|honestly|anyway|also)\W+)*"
    r"how\s+do\s+(?:you|u|ya)\s+find\s+(?P<thing2>[^?.!]+)$", re.I)
ABOUT_THE_BOT_BORN = re.compile(
    r"^\W*(?:(?:and|but|so|oh|ok|okay|well|right)\W+)*"
    r"(?:where\s+(?:were|are)\s+(?:you|u|ya)\s+(?:from|born)"
    r"|(?:were|are)\s+(?:you|u|ya)\s+(?:born|raised|brought\s+up)"
    r"(?:\s+(?:here|there|locally|in\s+this\s+country))?)"
    r"(?:\s+originally)?[ ?!.,;]*$", re.I)
BOT_FEELING_NAMED_LINES = (
    "No feelings on my side at all, and no view on {thing} worth having - I am a program. How are "
    "you finding it?",
    "I have no feelings about it - I am a program, so there is nothing in me for {thing} to land "
    "on. What do you make of it?",
    "No view worth having, and no moods to have one with. You are the one living with {thing} - "
    "how is it going?",
)
BOT_BORN_LINES = (
    "There is no born for me - I am a program, so no hometown and no childhood. Where are you "
    "from, if you do not mind me asking?",
    "Not born, and not from anywhere: I started as a program and stayed one. Are you far from "
    "where you grew up?",
)
_THE_TALK_ITSELF = r"(?:talk|chat|talking|chatting|keep\s+going|keep\s+you\s+here)"
ABOUT_THE_BOT_TALK = re.compile(
    r"^\W*(?:(?:and|but|so|oh|ok|okay|well|right|sorry|quick|just|question|one\s+question|quick\s+question|first\s+question|random\s+question)\W+)*"
    r"(?:"
    r"(?:is|are)\s+there\s+(?:a|any)\s+(?:time\s+)?limit(?:\s+(?:to|on)\s+"
    r"(?:(?:how\s+long|the\s+time)\s+)?(?:(?:we|i)\s+can\s+)?(?:"
    + _THE_TALK_ITSELF + r"|this|it|the\s+chat|our\s+chat))?"
    r"|(?:how\s+much\s+time\s+(?:do|have|did)\s+(?:we|i)\s+(?:have|got)\s+left)"
    r"|(?:do|have)\s+(?:we|you|i)\s+(?:have|got)\s+(?:a\s+|any\s+)?(?:time\s+)?limit"
    r"|(?:how\s+long|how\s+much\s+time)\s+(?:(?:can|could)\s+(?:we|i)\s+)?"
    r"(?:(?:have|has)\s+(?:we|you\s+and\s+i)\s+been\s+)?(?:" + _THE_TALK_ITSELF + r")"
    r"|(?:are|do)\s+(?:we|i)\s+(?:out\s+of|running\s+out\s+of|short\s+of)\s+time"
    r"|(?:do|should)\s+i\s+(?:need\s+to\s+)?hurry(?:\s+up)?"
    r"|(?:can|could|will)\s+(?:we|i|you\s+and\s+i)\s+(?:talk|chat|keep\s+going)\s+for\s+long"
    r"|have\s+(?:we|i|you\s+and\s+i)\s+got\s+long"
    r")(?:\s+(?:with|for)\s+(?:you|this|me|now)|\s+for|\s+much)?[ ?!.,;]*$", re.I)
ABOUT_THE_BOT_CLOCK = re.compile(
    r"^\W*(?:(?:and|but|so|oh|ok|okay|well|right|sorry|quick|just|question|one\s+question|quick\s+question|first\s+question|random\s+question)\W+)*"
    r"(?:how\s+(?:long|much\s+time)\s+(?:have|has|did)\s+(?:we|i|you|you\s+and\s+i)\s+been\s+"
    r"(?:" + _THE_TALK_ITSELF + r")"
    r"|how\s+long\s+has\s+this\s+been\s+going\s+on)"
    r"(?:\s+(?:to|with)\s+(?:you|me))?[ ?!.,;]*$", re.I)
BOT_TALK_LIMIT_LINES = (
    "No limit I know of on my side - I stay as long as you keep going, and nothing runs out. "
    "What do you want to get to?",
    "Nothing cuts this short at a set time as far as I know: the chat lasts while you are in it. "
    "Where would you like to take it?",
)
BOT_TALK_CLOCK_LINES = (
    "I don't keep a clock, so I can't put a number on it - but we have been going a while, and I "
    "am in no hurry.",
    "No clock on my side, sorry: I hold the words, not the minutes. There is plenty of time as "
    "far as I am concerned.",
)


def _a_question_about_the_bot(clean, memory=None):
    line = " ".join(str(clean or "").split())
    if not line:
        return ""
    if ABOUT_THE_BOT_CLOCK.match(line):
        return _choose(BOT_TALK_CLOCK_LINES, memory, clean)
    if ABOUT_THE_BOT_TALK.match(line):
        return _choose(BOT_TALK_LIMIT_LINES, memory, clean)
    if ABOUT_THE_BOT_BORN.match(line):
        return _choose(BOT_BORN_LINES, memory, clean)
    found = ABOUT_THE_BOT_NAMED.match(line)
    if not found:
        return ""
    raw = (found.group("thing") or found.group("thing2") or "").strip(" ,.;:-")
    if raw.lower().split()[:1] and raw.lower().split()[0] in ("your", "ur", "you", "yourself"):
        return ""
    thing = _the_thing_alone(raw)
    if not thing or thing.lower().split()[0] in NOT_A_THING_ASKED:
        return ""
    if len(thing.split()) > DISLIKE_TOO_LONG:
        return ""
    said = thing.lower()
    lines = tuple(frame.format(thing=said) for frame in BOT_FEELING_NAMED_LINES)
    return _choose(lines, memory, clean)

def _only_the_floor(said):
    said = _plain(said)
    if not said:
        return False
    parts = [p.strip(" ,.;:!?\u2014\u2013-\t") for p in
             re.split(r"[.!?;,\u2014\u2013]|\s-\s", said)]
    parts = [p for p in parts if p]
    if not parts or len(parts) > 4:
        return False
    for part in parts:
        if FLOOR_COURTESY.match(part):
            continue
        if not FLOOR_CLAUSE.match(part):
            return False
        words = len(part.split())
        if words > 8 and not FLOOR_WAITING.search(part):
            return False
    return True


FLOOR_WAITING = re.compile(
    r"\b(?:if|when)\s+you(?:'re|\s+are)?\s+(?:want|need|ready|like)|for\s+as\s+long\s+as"
    r"|\bwhenever\b|\bany\s+time\b", re.I)


def _plain(text):
    lowered = str(text or "").lower().replace("\u2014", "-").replace("\u2013", "-")
    return " ".join(lowered.split())


def _the_words(text):
    return {word for word in re.findall(r"[a-z']+", str(text or "").lower())
            if word not in _ECHO_FILLER and len(word) > 2}


def _an_echo_of(question, sentence):
    mine = _the_words(question)
    theirs = _the_words(sentence)
    if len(theirs) < 2 or not mine:
        return False
    return len(theirs & mine) / len(theirs) >= 0.75


def _only_a_reaction(module, said):
    if str(module or "") != "chat":
        return False
    said = str(said or "").strip()
    if not said.endswith("?") or len(said.split()) > 14:
        return False
    return any(phrase in said.lower() for phrase in PRAISE)


def _the_answer_in_reply(question, said):
    said = str(said or "").strip()
    for _ in range(3):
        sentences = re.split(r"(?<=[.!?])\s+", said)
        first = sentences[0].strip() if sentences else ""
        rest = " ".join(sentences[1:]).strip()
        if not rest:
            return said
        if not (ack.reads_as_a_receipt(first) or _in_a_pool(first)
                or _an_echo_of(question, first)):
            return said
        said = rest
    return said


def _reads_as_a_claim(said):
    said = str(said or "").strip()
    if not said or VIEW_NOT_AN_ANSWER.match(said.lower()):
        return False
    if ack.reads_as_a_receipt(said):
        return False
    if _in_a_pool(said):
        return False
    if _only_the_floor(said):
        return False
    first = re.split(r"(?<=[.!?])\s+", said)[0].strip()
    if first.endswith("?") and ":" in first:
        return False
    return True


def _nothing_to_stand_behind(said):
    said = str(said or "").strip()
    return bool(said) and (ack.reads_as_a_receipt(said) or _in_a_pool(said, (NEUTRAL,))
                           or _only_the_floor(said))


VIEW_NAMES_SOMEBODY = re.compile(r"\b(?:me|my|mine|myself|us|our|ours|i|im|i'm)\b")


def _is_a_view_ask(clean):
    if not VIEW_ASKS.search(clean):
        return False
    words = re.findall(r"[a-z']+", clean)
    return bool(words) and not any(
        word.strip("'") not in VIEW_ONLY_WORDS for word in words)


def _the_view_asked_for(clean, memory):
    from .fallback_pools import _the_view_asked_for as _moved
    return _moved(clean, memory)


def _after_a_colon(said):
    if len(said) > 1 and said[0].isupper() and not said.startswith("I ") and not said.startswith("I'"):
        return said[0].lower() + said[1:]
    return said


HEDGE_HEADS = tuple(line[:40] for pool in HEDGE_POOL for line in pool)
HEDGE_PREFIXES = tuple(line.split("{")[0] for pool in HEDGE_POOL for line in pool
                       if "{" in line)
from .the_rule_for_it import RULE_HEADS as _RULE_HEADS

HEDGE_HEADS = HEDGE_HEADS + _RULE_HEADS


def _is_an_ask_which_bit(said):
    head = (said or "").strip()
    return bool(head) and head in BARE_FOLLOW_UP_REPLIES


is_an_ask_which_bit = _is_an_ask_which_bit


def _is_a_hedge(said):
    head = said[:40]
    return (any(head == line for line in HEDGE_HEADS)
            or any(said.startswith(prefix) for prefix in HEDGE_PREFIXES))


is_a_hedge = _is_a_hedge


THE_OUTCOME_ASK = re.compile(
    r"^(?:so |and |but |ok |okay )?(?:is|are|will|do you think|does the doctor think)\b"
    r"(?=[^?]{0,44}?(?:\b(?:going to be|be) (?:ok|okay|alright|all right|fine)\b"
    r"|\b(?:make it|pull through|come through|survive|recover)\b))", re.I)
WHO_IS_ILL = re.compile(
    r"\b(?:in hospital|in the hospital|on the ward|got admitted|been admitted|is admitted|"
    r"in icu|intensive care|stroke unit|a&e|having an operation|having surgery|"
    r"in for an operation|waiting for a bed|coming out of hospital|coming home from hospital|"
    r"had a stroke|chemo|chemotherapy|on a ventilator|in a coma|diagnosed with|"
    r"the operation|the surgery|under the knife|their scan|the scan|"
    r"pneumonia|sepsis|heart attack|collapsed)\b", re.I)


def an_outcome_asked_about_someone(text, memory):
    if not isinstance(memory, dict):
        return None
    clean = " ".join(str(text or "").lower().split())
    if not clean or len(re.findall(r"[a-z']+", clean)) > 9:
        return None
    if not THE_OUTCOME_ASK.match(clean):
        return None
    if re.search(r"\b(?:i|me|my|we|us|our)\b", clean):
        return None
    turns = [turn for turn in (memory.get("turns") or []) if isinstance(turn, dict)][-3:]
    if not turns:
        return None
    last = str(turns[-1].get("bot") or "")
    if last and (any(word in last.lower() for word in CRISIS_WORDS)
                 or any(word in last.lower() for word in SAFETY_WORDS)):
        return None
    said = " ".join([str(turn.get("user") or "") for turn in turns] + [last])
    if not WHO_IS_ILL.search(said):
        return None
    return pick(OUTCOME_LINES, memory, clean)


def is_a_hedge(said):
    head = str(said or "")[:40].lower()
    return (any(head == line.lower() for line in HEDGE_HEADS)
            or any(str(said or "").lower().startswith(prefix.lower())
                   for prefix in HEDGE_PREFIXES))


VIEW_MIRROR = re.compile(
    r"^(?:i(?:'m| am) (?:so |really |very |truly )?sorry\b|so sorry\b|sorry\b|that sounds\b"
    r"|that(?:'s| is) (?:rough|hard|tough|awful|a hard one|a lot|a real loss|a loss)\b"
    r"|ouch\b|ugh\b|hope\b|[a-z]{3,20}(?: [a-z]{2,20}){0,3} is (?:rough|hard|tough|awful)\b)")
VIEW_A_CASE = re.compile(
    r"^(?:if |unless |depending on|when you|when it|once you|for £|for under |for about "
    r"|for around |for between |for a budget|for \d)")

def _the_view_of(said):
    parts = [part.strip() for part in re.split(r"(?<=[.!?])\s+", said.strip()) if part.strip()]
    mirrored = False
    for part in parts:
        head, colon, tail = part.partition(":")
        if colon and tail.strip():
            words = [w.strip(",.").lower() for w in head.split()]
            if (len(words) < 7 and any(word in VIEW_LEAD_IN for word in words)) \
                    or len(words) <= 3 or VIEW_A_CASE.match(head.strip().lower()):
                head, tail = tail, head
            part = head
        part = part.strip()
        if VIEW_MIRROR.match(part.lower()):
            mirrored = True
            continue
        claim = _a_said_claim(part)
        if claim:
            return claim, mirrored
        mirrored = True
    return None, mirrored


ASKS_BACK = re.compile(
    r"^(?:tell me|let me know|send me|show me|give me|any chance|could you|can you|would you|"
    r"have you got|do you have|what have you|what about you)\b")


def _a_said_claim(first):
    if not first or first.endswith(":"):
        return None
    if first.endswith("?"):
        return first if len(first.split()) >= 4 else None
    if ASKS_BACK.match(first.lower()):
        return None
    words = first.split()
    if len(words) > 30:
        cut = 20
        for index in range(20, min(len(words), 44)):
            if words[index].endswith(","):
                cut = index + 1
                break
        else:
            cut = 30
        first = " ".join(words[:cut]).rstrip(",") + "."
    if len(first.split()) < 3:
        return None
    return first.rstrip(" .;,:") + "."


MORE_ON_THIS = re.compile(
    r"\b(?:anything|something) (?:else|more)\b|\bwhat else\b"
    r"|\bwhat else (?:can|could|might|would|will|should|do|does|works?|helps?|matters?)\b"
    r"|\bany (?:other|more) (?:way|ways|idea|ideas|option|options|thing|things|tips?)\b"
    r"|\bis there anything (?:else|more|i can do)\b"
    r"|\bcan i do anything about (?:it|that|this)\b"
    r"|\bwhat about (?:the|my|our|his|her|their|those|these|it|that)\b")

WHAT_ABOUT = re.compile(r"\bwhat about\s+(?:the|my|our|his|her|their|those|these)\s+(.+)$")
PERSON_NAMED = re.compile(
    r"^(?:mum|mom|mam|mother|dad|father|parent|parents|sister|brother|son|daughter|gran|"
    r"grandma|grandad|granny|nana|nan|husband|wife|partner|boyfriend|girlfriend|friend|"
    r"friends|baby|boy|girl|kids?|children|child|family|aunt|uncle|cousin|niece|nephew|"
    r"neighbour|neighbor|boss|colleague|carer|vet)\b")


def asks_for_more(text, memory):
    said = str(text or "").strip().lower()
    if not MORE_ON_THIS.search(said):
        return False
    tail = WHAT_ABOUT.search(said)
    if not tail:
        return True
    named = tail.group(1)
    if PERSON_NAMED.match(named):
        return False
    return _named_recently(named, memory)


def _named_recently(named, memory, look_back=3):
    from ..memory.topics import keywords

    wanted = set(keywords(named))
    if not wanted:
        return True
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)][-look_back:]
    said = " ".join(str(t.get(key) or "") for t in turns for key in ("user", "bot"))
    return bool(wanted & set(keywords(said)))


def _answered_recently(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    if not turns:
        return False
    index = len(turns) - 1
    while index > 0 and _only_takes_the_answer(str(turns[index].get("bot") or "")):
        index -= 1
    last = turns[index]
    if str(last.get("module") or "") in NO_MORE_OF:
        return False
    if not _told_them_something(str(last.get("bot") or "")):
        return False
    return not history.not_a_subject(str(last.get("user") or ""))


ACK_ONLY = re.compile(
    r"^(?:fair enough|fair|got it|got that|noted|understood|right|righto|right then|ok|okay|"
    r"alright|all right|sure|fine|nice one|sounds good|no bother|no worries|no problem|"
    r"hope it works out|lovely|good|great|grand|of course|certainly)\b[^?]{0,40}$", re.I)


def _only_takes_the_answer(said):
    text = " ".join(str(said or "").split())
    if not text or len(text.split()) > 8:
        return False
    return ACK_ONLY.match(text) is not None


REACTED_ONLY = re.compile(
    r"^(?:sorry to hear|sorry\.|that sounds|that'?s (?:great|good|lovely|brilliant|rough|tough|"
    r"awful|a pain|a shame|a nuisance|rotten|understandable)|good on you|nice one|nice -|well "
    r"done|love that|fair enough|got it|makes sense|noted:|thanks for telling|i'?m listening|"
    r"i hear you|that'?s a lot)", re.I)


def _told_them_something(said):
    text = said.strip()
    if not text or text.endswith("?"):
        return False
    return REACTED_ONLY.match(text) is None


def _the_answer_above(memory):
    from .verdict import takes_a_fact_back
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    while turns and takes_a_fact_back(turns[-1].get("bot")):
        turns.pop()
    if not turns:
        return ""
    return str(turns[-1].get("bot") or "")


def _answered_already(memory):
    from .verdict import takes_a_fact_back
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    while turns and takes_a_fact_back(turns[-1].get("bot")):
        turns.pop()
    return bool(turns) and str(turns[-1].get("module") or "") == "answers"


TIPS_SPOKEN = (
    (re.compile(r"(?<![a-z0-9])4(?![a-z0-9])"), "for"),
    (re.compile(r"(?<![a-z0-9])2(?![a-z0-9])"), "to"),
    (re.compile(r"(?<![a-z0-9])u(?![a-z0-9])"), "you"),
    (re.compile(r"(?<![a-z0-9])ur(?![a-z0-9])"), "your"),
    (re.compile(r"(?<![a-z0-9])ne(?![a-z0-9])"), "any"),
    (re.compile(r"(?<![a-z0-9])pls(?![a-z0-9])"), "please"),
)
TIPS_NUMBER_TAIL = re.compile(r"\s*(?:%s)\b" % "|".join(sorted(TIPS_UNIT)))


def _tips_spoken(text):
    words = text.split()
    for i, word in enumerate(words):
        tail = words[i + 1] if i + 1 < len(words) else ""
        if word.isdigit() and TIPS_NUMBER_TAIL.match(tail):
            continue
        for pattern, said in TIPS_SPOKEN:
            word = pattern.sub(said, word)
        words[i] = word
    return " ".join(words)


def _tips_subject(clean):
    text = _tips_spoken(" ".join(str(clean or "").lower().split()))
    if not TIPS_WORD.search(text) and not TIPS_ANY_IDEA.search(text):
        return None
    found = TIPS_SUBJECT_FOR.search(" " + text)
    subject = found.group("subject") if found else TIPS_SUBJECT_TAIL.sub("", " " + text + " ")
    subject = re.sub(r"[,.!?;:].*$", "", subject.strip(" ,.!?;:"))
    subject = TIPS_LEAD.sub("", " ".join(subject.split()))
    subject = re.sub(r"^(?:i|we)\s+(?:really\s+)?(?:need|want|would\s+like|am\s+looking\s+for)\s+",
                     "", subject)
    subject = TIPS_REQUEST.sub("", TIPS_LEAD.sub("", subject))
    subject = TIPS_LEAD.sub("", subject)
    if not subject or subject.startswith("to ") or subject in ("it", "that", "this", "some", "anything", "something",
                                  "a", "an", "the", "advice", "tips", "help"):
        return None
    kept = [word for word in subject.split() if word not in FILLERS]
    if not kept or len(kept) > 6 or len(" ".join(kept)) > 40:
        return None
    if set(kept) & TIPS_CLAUSE or kept[0] in TIPS_VERB:
        return None
    return " ".join(TIPS_OWNER.get(word, word) for word in kept)


def _tips(memory, clean, repaired=None):
    subject = _tips_subject(clean) or (_tips_subject(repaired) if repaired != clean else None)
    if not subject:
        return ""
    said = " " + re.sub(r"[^a-z0-9']", " ", str(clean or "").lower()) + " "
    if _who_for(str(clean or "").lower(), said, said.replace("'", "").split()):
        return ""
    pool = TIPS_AHEAD if TIPS_SOON.search(subject) else TIPS_THING
    return _choose(list(pool), memory, clean)
_ASKS_DEFINITION = re.compile(r"^\s*what(?:'s|s| is| are| was| does| do)\b|\bdifference between\b"
                              r"|\bwhat does .* (?:do|mean)\b|\bmeaning of\b")
_ASKS_WHERE = re.compile(r"\bwhere(?:'s|s| is| are| was| were| did| do| does| can i| shall i)\b")
_SCHEDULING = re.compile(r"\b(appt|appointment|appointments|cancel|reschedule|rearrange|rebook|"
                         r"double booked|move it|change it)\b")
_ASKS_ARITHMETIC = re.compile(r"\b(work out|calculate|convert|how much is|how many|percent|"
                              r"percentage|hourly rate)\b")
QUOTE_ASKS = re.compile(r"\b(quote|quoted|estimate|price|priced|cost|bill|invoice|fee|charge)\b"
                        r".*\b(sound right|sounds right|too much|too high|too dear|steep|fair|"
                        r"reasonable|about right|normal)\b")
_ASKS_DIY = re.compile(r"\b(how do i|how can i|how to)\s+(fix|mend|repair|replace|install|fit|"
                       r"unblock|bleed|reset|clean|change)\b|\bmyself\b|\bmy own\b")


PRICE_VERDICT = re.compile(
    r"\b(?:too\s+(?:much|expensive|dear|pricey|pricy)|expensive|pricey|pricy|steep|overpriced|"
    r"dear|over\s+the\s+odds|rip[- ]?off|ripped\s+off|robbed|reasonable|fair|about\s+right|"
    r"sound\s+right|sounds\s+right|worth\s+it|good\s+(?:deal|price)|a\s+lot|that\s+much|"
    r"ok|okay|daylight\s+robbery)\b")
MONEY_IN_A_LINE = re.compile(
    r"(?:[\u00a3$\u20ac]\s?\d[\d,]*(?:\.\d+)?)"
    r"|\b\d[\d,]*(?:\.\d+)?\s?(?:pounds?|quid|pence|euros?|dollars?|bucks|grand|k)\b"
    r"|\b(?:a|an|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|"
    r"fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|"
    r"seventy|eighty|ninety|hundred|thousand)\s+(?:pounds?|quid|euros?|dollars?|bucks|grand)\b"
    r"|\b(?:a\s+)?(?:couple\s+of\s+|few\s+)?(?:hundred|thousand)\s+(?:pounds?|quid|euros?)\b"
    r"|\ba\s+(?:tenner|fiver|grand)\b", re.I)
A_BARE_FIGURE = re.compile(r"\b\d{2,}\b")
A_MONEY_VERB = re.compile(r"\b(?:want|wants|wanted|ask|asks|asked|asking|charge|charges|charged|"
                          r"charging|quote|quotes|quoted|quoting|cost|costs|costing|pay|pays|paid|"
                          r"paying|spend|spent|spending|come|comes|coming|say|says|said|tell|"
                          r"tells|told|give|gives|gave|price|priced)\b[^.?!]*?\b\d{2,}\b")
A_MEASURE = re.compile(
    r"\b(?:cups?|mugs?|glasses?|hours?|minutes?|mins?|miles?|km|kms|kilograms?|kilos?|kg|"
    r"grams?|degrees?|times?|days?|weeks?|months?|years?|cm|mm|metres?|meters?|litres?|"
    r"liters?|pints?|slices?|spoons?|teaspoons?|handfuls?|steps?|pages?|screens?|"
    r"episodes?|calories?|carbs?)\b")
FOR_A_PERSON = re.compile(r"\bfor\s+(?:me|us|him|her|them|you|myself|ourselves)\b")
SPLIT_BETWEEN_PEOPLE = re.compile(r"\b(?:split|splits|splitting|share|sharing|going halves|"
                                  r"pay half|pays half|pay more|pay less)\b")
A_PRICE_ASK = re.compile(r"^(?:and\s+|so\s+|but\s+|ok\s+|okay\s+|also\s+)?(?:is|isnt|aren'?t|"
                         r"are|was|wasnt|wasn'?t|were|does|doesnt|do|did|didnt|would|wouldnt|"
                         r"should|shouldnt|could|will|that|this|too|seems?|looks?|sounds?)\b|\?")
PRICE_VERDICT_LINES = (
    "{figure} only says something next to another price: the same thing elsewhere, or the same job "
    "from someone else. Get one of those and it is easy to call.",
    "Whether {figure} is a lot depends on what the same thing goes for. One other price - another "
    "shop, or another quote for the same work - settles it.",
    "Hold {figure} against one more price for the same thing before you decide; the pair tells you "
    "more than any rule of thumb.",
)


def _the_figure_in(text):
    found = MONEY_IN_A_LINE.search(text or "")
    return " ".join(found.group(0).split()) if found else ""


def _a_price_wants_a_verdict(clean, memory):
    said = " ".join(str(clean or "").lower().split())
    if not said or len(said.split()) > 7:
        return None
    if not A_PRICE_ASK.search(said) or not PRICE_VERDICT.search(said):
        return None
    if (FOR_A_PERSON.search(said) or SPLIT_BETWEEN_PEOPLE.search(said)
            or A_MEASURE.search(said)):
        return None
    figure = _the_figure_in(said)
    if not figure:
        bare = A_BARE_FIGURE.search(said)
        figure = bare.group(0) if bare else ""
    if not figure:
        before = _the_line_before(memory)
        figure = _the_figure_in(before)
        if not figure:
            paid = A_MONEY_VERB.search(" ".join(before.split()))
            bare = A_BARE_FIGURE.search(paid.group(0)) if paid else None
            figure = bare.group(0) if bare else ""
    if not figure:
        return None
    return tuple(line.replace("{figure}", figure) for line in PRICE_VERDICT_LINES)


GIFT_WORDS = frozenset(("present", "presents", "gift", "gifts", "spend on", "budget for",
                        "how much do you spend", "what do you get"))
BUYING_WORDS = frozenset(("buying", "buy a house", "buy a flat", "buy a home", "bought",
                          "purchase", "ladder", "mortgage", "own a home", "should i buy"))
NETWORK_WORDS = frozenset(("wifi", "wi-fi", "internet", "broadband", "network", "connection",
                         "signal", "online"))
MEDS_WORDS = frozenset(("tablets", "pills", "medicine", "medication", "prescription", "dose",
                        "doses", "capsules", "antibiotics", "vaccine", "vaccination", "jab",
                        "jabs", "vitamin", "vitamins", "supplement", "supplements", "ibuprofen",
                        "paracetamol", "aspirin", "painkiller", "painkillers", "antihistamine",
                        "antihistamines", "steroid", "steroids", "insulin", "inhaler"))


def _a_grown_up_asks(clean, words, said):
    if _names(words, said, GROWN_UP_WORDS):
        return True
    left = " %s " % clean
    dropped = False
    for name in BABY_FOOD_NAMES:
        if " %s " % name in left:
            left = left.replace(" %s " % name, " ")
            dropped = True
    if not dropped or not _names(words, said, SELF_EATING_WORDS):
        return False
    return not _names(set(left.split()), left, CHILD_AT_HOME)


def _who_for(clean, said, words, topic=None):
    if _ASKS_DEFINITION.search(clean) or _ASKS_ARITHMETIC.search(clean):
        return None
    diy = bool(_ASKS_DIY.search(clean))
    gift = _names(words, said, GIFT_WORDS)
    meds = _names(words, said, MEDS_WORDS)
    buying = _names(words, said, BUYING_WORDS)
    if _names(words, said, SCHOOL_WORDS) and _names(words, said, SCHOOL_TROUBLE):
        return SCHOOL_WHO
    if _names(words, said, ("password",)) and _names(words, said, PASSWORD_TROUBLE):
        return DEVICE_WHO
    if _names(words, said, COMPLAINT_WORDS) and _names(words, said, TRADER_WORDS):
        return COMPLAIN_WHO
    animal = any(word in ANIMALS or word.rstrip("s") in ANIMALS for word in words)
    if animal and _names(words, said, WILD_BIRDS) and _names(words, said, MESS_PLACES):
        animal = False
    machine_mouse = is_a_machine_word(clean)
    if not animal and meds:
        return HEALTH_WHO
    if not animal and _names(words, said, FILLING_WORDS) and (
            _names(words, said, MOUTH_WORDS)
            or not (topic in FOOD_TOPICS or _names(words, said, FILLING_FOODS))):
        return DENTIST_WHO
    where_is_a_thing = bool(_ASKS_WHERE.search(clean)) and not _names(
        words, said, WHERE_SOMETHING_WRONG)
    for evidence, who in WHO_TO_ASK:
        if where_is_a_thing and who in (BABY_WHO, HEALTH_WHO):
            continue
        if machine_mouse and who == PEST_WHO:
            continue
        if animal and who != VET_WHO and evidence & SICKNESS:
            continue
        if animal and who == DENTIST_WHO:
            continue
        if who == HEALTH_WHO and _SCHEDULING.search(clean):
            continue
        if who == HEALTH_WHO and _CHOOSING_BETWEEN_TWO.search(clean):
            continue
        if who == HEALTH_WHO and _names(words, said, JOINT_WORDS) and not (
                _names(words, said, evidence - JOINT_WORDS)
                or _ASKS_ABOUT_THE_JOINT.search(clean)):
            continue
        if diy and who in (TRADES_WHO, DEVICE_WHO):
            continue
        if who == BABY_WHO and _a_grown_up_asks(clean, words, said):
            continue
        if who == BABY_WHO and not _names(words, said, CHILD_AT_HOME):
            continue
        if gift and who in (BABY_WHO, HEALTH_WHO):
            continue
        if meds and who == DEVICE_WHO:
            continue
        if who == DEVICE_WHO and _names(words, said, NETWORK_WORDS):
            continue
        if buying and who == TENANT_WHO:
            continue
        if who == WORK_WHO and not _names(words, said, WORK_ABOUT):
            continue
        if _names(words, said, evidence):
            return who
    if animal and (meds or _names(words, said, SICKNESS)):
        return VET_WHO
    return None


def who_settles(text, memory):
    understood = memory.get("understood") if isinstance(memory, dict) else None
    if not isinstance(understood, dict) or \
            str(understood.get("text") or "") != str(text or ""):
        borrowed = dict(memory) if isinstance(memory, dict) else {}
        borrowed.pop("understood", None)
        understood = understand(text, borrowed)
    clean = understood.get("clean") or " ".join(str(text).lower().split())
    words = understood.get("words") or []
    said = " " + re.sub(r"[^a-z0-9']", " ", clean) + " "
    return _who_for(clean, said, words, understood.get("topic"))


def _advisor(memory, clean, said, words):
    topic = (memory.get("understood") or {}).get("topic") if isinstance(memory, dict) else None
    who = _who_for(clean, said, words, topic)
    if not who:
        return None
    return _choose([line.format(who=who) for line in UNKNOWN_WHO], memory, clean)


HEALTH_VISIT_WORDS = frozenset("""
    scan scans mri ct xray x-ray ultrasound biopsy results result consultant clinic appointment
    appointments operation surgery transplant chemo radiotherapy dialysis test tests screening
    ward hospital
""".split())


A_ROUGH_STRETCH = re.compile(
    r"\b(?:sad|lonely|alone|crying|cry|cried|tears?|grief|grieving|mourning|bereft|depressed|"
    r"depressing|miserable|unhappy|hopeless|worthless|anxious|anxiety|panic(?:king)?|scared|"
    r"afraid|terrified|worried|worry|worries|worrying|struggling|struggle|coping|"
    r"breaking point|burnt out|burned out|drained|overwhelmed|numb|empty|"
    r"cant cope|cannot cope|can't cope|hate myself|no one cares|nobody cares)\b")
A_HARD_THING_HAPPENED = re.compile(
    r"\b(?:funeral|died|death|dying|passed away|diagnos\w*|cancer|tumour|tumor|terminally|"
    r"miscarriage|stillborn|divorce|separated|left me|walked out|sacked|redundant|"
    r"evicted|homeless|hospital|icu|intensive care|hospice)\b")


def _a_bad_stretch_above(memory, look_back=3):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)][-look_back:]
    for turn in turns:
        said = str(turn.get("user") or "").lower()
        if not said:
            continue
        if A_ROUGH_STRETCH.search(said) or A_HARD_THING_HAPPENED.search(said):
            return True
    return False


def _thread_has_a_health_visit(memory, look_back=3):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)][-look_back:]
    for turn in turns:
        words = set(re.findall(r"[a-z'-]+", str(turn.get("user") or "").lower()))
        if words & HEALTH_VISIT_WORDS:
            return True
    return False


def _in_a_crisis_thread(memory):
    answer = _thread_answer(memory)
    return bool(answer) and any(word in answer for word in CRISIS_WORDS)


def _who_for_the_thread(memory, clean, understood=None):
    typed = str((understood or {}).get("text") or "") if isinstance(understood, dict) else ""
    line = typed or clean or ""
    a_voice = bool(WHO_TO_TALK_ASK.search(line)) and not re.search(
        r"\babout\s+(?!it\b|that\b|this\b|them\b)\w|"
        r"\b(?:talk|speak|chat)\s+(?:to|with)\s+(?:the|a|an|my|your|his|her|their)\b", line)
    a_call = bool(WHO_FOR_IT.match(line)) if not a_voice else False
    if not (a_call or a_voice):
        return None
    answer = str(last_bot(memory) or "").lower()
    if answer:
        for word, name in NAMED_BODIES:
            if re.search(r"\b" + re.escape(word) + r"\b", answer):
                shapes = WHO_FOR_IT_SAID_VOICE if a_voice else WHO_NAMED_BEFORE
                return [shape.format(who=name) for shape in shapes]
    for said in reversed([str(t.get("user") or "") for t in
                          [t for t in (memory.get("turns") or []) if isinstance(t, dict)][-3:]
                          if isinstance(t, dict)]):
        if not said:
            continue
        try:
            who = who_settles(said, memory)
        except Exception:
            who = None
        if who:
            shapes = WHO_FOR_IT_SAID_VOICE if a_voice else WHO_FOR_IT_SAID
            return [shape.format(who=who) for shape in shapes]
    if a_call and (_thread_is_about_the_body(memory) or _thread_has_a_health_visit(memory)):
        return list(WHO_FOR_IT_BODY)
    if a_call:
        return list(WHO_FOR_IT_ROUTES)
    return list(WHO_TO_TALK_TO_A_BAD_STRETCH if _a_bad_stretch_above(memory) else WHO_TO_TALK_TO)


def _trouble(memory, clean, words):
    said = " " + " ".join(words) + " "
    if not any(word.startswith(cue) for word in words for cue in TROUBLE_CUES):
        return None
    if not _reads_as_question(clean, words):
        topic = (memory.get("understood") or {}).get("topic") if isinstance(memory, dict) else None
        who = _who_for(clean, said, words, topic)
        if who == HEALTH_WHO:
            return None
    return _advisor(memory, clean, said, words)


def _is_a_form(word, evidence_word):
    tail = word[len(evidence_word):]
    if not tail:
        return True
    if word in NOT_A_FORM:
        return False
    if tail in ENDINGS:
        return True
    return (len(tail) > 1 and tail[0] == evidence_word[-1] and tail[1:] in ENDINGS)


def _names(words, said, evidence):
    for word in evidence:
        if " " in word:
            if word in said:
                return True
        elif any(w == word or (len(word) >= 4 and w.startswith(word)
                               and _is_a_form(w, word)) for w in words):
            return True
    return False


def _reads_as_question(text, words):
    if "?" in text:
        return True
    plain = [w.replace("'", "") for w in words]
    if plain and WORD_FIXES.get(plain[0], plain[0]) in QUESTION_WORDS:
        return True
    joined = INDIRECT.sub(" ", " " + " ".join(plain) + " ")
    later = INDIRECT.sub(" ", text.lower())
    return bool(LATER_QUESTION.search(later) or ASK_SHAPES.search(joined))


def _reads_as_a_question_when_repaired(text):
    plain = [word.replace("'", "") for word in str(text or "").split()]
    if plain and WORD_FIXES.get(plain[0], plain[0]) in _OPENING_QUESTIONS:
        return True
    return bool(ASK_SHAPES.search(" " + " ".join(plain) + " "))


def _help_topic(clean, understood):
    if not isinstance(understood, dict) or not HELP_TOPIC_ASK.search(clean):
        return None
    topic = understood.get("topic_own")
    if not topic or topic in ("about-the-bot", "small-talk", "opinions"):
        return None
    return HELP_TOPIC.get(topic) or HELP_TOPIC_ANY


def reads_as_about_itself(text, memory=None):
    clean = _self_line(text)
    return (_about(clean, None) in ABOUT_ITSELF_KINDS
            or bool(FORGETTING_ASK.search(clean)))


QUESTION_CLAUSE = re.compile(
    r"\b(?:does|do|did|can|could|should|would|will|shall|is|are|was|were|have|has|am)\s+"
    r"(?:there|that|this|it|i|you|we|they|he|she|any|my|me|the)\b"
    r"|\b(?:what|where|who|which|when|how)\s+(?:can|could|should|do|does|did|is|are|would|will|"
    r"am|to|if|about|much|many|long|often)\b")


A_THING_THAT_IS_SHORT = re.compile(
    r"\b(?:bill|bills|electric|electricity|leccy|gas|water|council\s+tax|rent|mortgage|"
    r"broadband|wifi|wi-fi|phone\s+bill|arrears|owe|owed|owes|debt|debts|loan|overdraft|"
    r"credit\s+card|store\s+card|direct\s+debit|instal?lment)\b")


def reads_as_a_tight_week(text, memory=None):
    context = dict(memory or {})
    context.pop("understood", None)
    try:
        from ..understanding import understand
        understood = understand(text, context)
    except Exception:
        return False
    if not isinstance(understood, dict) or not understood.get("tight_on_money"):
        return False
    try:
        from ..understanding import topics
        if not topics.tight_on_money(understood.get("norm"), understood.get("kind")):
            return False
    except Exception:
        return False
    if QUESTION_CLAUSE.search(_self_line(text)):
        return False
    if A_THING_THAT_IS_SHORT.search(_self_line(text)):
        return False
    try:
        from ..memory.more import asks_for_more
        if asks_for_more(text):
            return False
    except Exception:
        pass
    return True


BARE_AND = re.compile(r"^(?:and|and then|and\?|then|so|ok and|and so)[\s.?!,]*$", re.IGNORECASE)


def a_continuation_of_the_tight_week(memory, text):
    if not BARE_AND.match(text or ""):
        try:
            from ..memory.more import asks_for_more
        except Exception:
            return False
        if not asks_for_more(text):
            return False
    turns = (memory or {}).get("turns") or []
    if not turns or not isinstance(turns[-1], dict):
        return False
    return str(turns[-1].get("bot") or "").strip() in TIGHT_MONEY + TIGHT_MONEY_MORE
def reads_as_small_talk(text, memory=None):
    clean = _self_line(text)
    if _about(clean, None):
        return False
    if _a_low_turn_above(memory):
        return False
    if HAND_BACK.match(clean):
        return bool((memory or {}).get("turns") if isinstance(memory, dict) else None)
    if not _asks_how_are_you(clean):
        return False
    if YOUR_DAY_ASK.search(clean) and not (YOUR_OWN_TIME.search(clean)
                                          or YOUR_TIME_ASK.search(clean)):
        return _an_answer_above(memory)
    return bool(YOUR_OWN_TIME.search(clean) or YOUR_TIME_ASK.search(clean))


_NOT_MANAGING = re.compile(
    r"\b(?:i|im|i'm|i am|we|we're|were)\b[^.]{0,14}\b(?:not coping|cope any ?more|"
    r"can'?t cope|keep going|take any ?more|falling apart|falling to pieces|breakdown|"
    r"breaking point|not managing|cant manage|can'?t manage|do this any ?more)\b")


def _a_low_turn_above(memory):
    if not isinstance(memory, dict):
        return False
    if (_hard_week_in_the_thread(memory) or _in_a_loss_thread(memory)
            or _grief_thread(memory) or _news_above(memory)):
        return True
    for earlier in [t for t in (memory.get("turns") or []) if isinstance(t, dict)][-2:]:
        line = " ".join(str(earlier.get("user") or "").lower().split())
        if not line:
            continue
        read = understand(line, {})
        if isinstance(read.get("polarity"), int) and read["polarity"] < 0:
            return True
        if _mood(_words(line), line) == "negative" or _NOT_MANAGING.search(line):
            return True
    return False


def _an_answer_above(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns:
        return False
    last = turns[-1] if isinstance(turns[-1], dict) else {}
    said = str(last.get("bot") or "").strip()
    return (last.get("module") == "answers" and len(said) >= 50
            and not said.rstrip().endswith("?"))


def _a_repair_already_spoken_of(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list) or not turns:
        return False
    last = turns[-1] if isinstance(turns[-1], dict) else {}
    if last.get("module") != "answers":
        return False
    said = str(last.get("bot") or "").lower()
    return bool(re.search(r"\b(?:repair|repairs|repaired|repairing|mend\w*|fix\w*|"
                          r"replace\w*|replacement|part|parts|quote|quoted|engineer|"
                          r"optician|servic\w+)\b", said))


LEAD_IN = re.compile(
    r"^(?:(?:ok|okay|okey|kk|right|so|ah|oh|ohh|well|anyway|anyways|and|but|now|hmm+|er+|um+|uh+|hey|"
    r"sorry|quick question|random question|stupid question|silly question|daft question|"
    r"this is (?:a bit |a |totally )?random|bit of a random one|a random one|unrelated|"
    r"off topic|just wondering|i was wondering|wondering|can i ask|may i ask|"
    r"just out of curiosity|out of curiosity|by the way|btw)\b[\s,:.!?-]*){1,4}")


def _self_line(text):
    clean = " ".join(str(text or "").lower().replace("\u2019", "'").replace("'", "").split())
    return LEAD_IN.sub("", clean) or clean


def _a_tally_of_its_own_day(understood):
    return bool(isinstance(understood, dict) and understood.get("counts_the_bots_own_day"))


_SPELLED_SHORT = (
    (re.compile(r"(?<![a-z])(?:r u|ru|r you|are u|am u)(?![a-z])"), "are you"),
    (re.compile(r"(?<![a-z])u(?![a-z])"), "you"),
    (re.compile(r"(?<![a-z])ur(?![a-z])"), "your"),
    (re.compile(r"(?<![a-z])u r(?![a-z])"), "you are"),
    (re.compile(r"(?<![a-z])wat(?![a-z])"), "what"),
    (re.compile(r"(?<![a-z])wot(?![a-z])"), "what"),
)


def _spelled_out(clean):
    out = clean
    for pattern, word in _SPELLED_SHORT:
        out = pattern.sub(word, out)
    return out


def _about(clean, understood=None):
    clean = _self_line(clean)
    _self = _self_line(clean)
    if (PRIVACY_ASK.search(_self) or PRIVACY_SHAPES.search(_self)
            or BETWEEN_US_ASK.search(_self)) \
            and not NOT_WHAT_I_SAID.search(_self):
        return "privacy"
    if TRUST_ASK.search(_self):
        return "trust"
    if SECRET_ASK.search(_self) or PROMISE_ASK.search(_self):
        return "secret"
    if JUDGING_ASK.search(_self):
        return "judging"
    if PRIVACY_ASK.search(clean) and not PRIVACY_NOT_THIS.search(clean) \
            and not NOT_WHAT_I_SAID.search(clean):
        return "privacy"
    if TRUST_ASK.search(clean) and not PRIVACY_NOT_THIS.search(clean):
        return "trust"
    if LIMITS_ASK.search(_self_line(clean)):
        return "limits"
    if ONLINE_ASK.search(_self_line(clean)) and not OWN_DEVICE.search(_self_line(clean)) \
            and not A_BARE_ONLINE.search(clean):
        return "online"
    if the_manners_question([word.strip(string.punctuation)
                             for word in _self_line(clean).split()]):
        if understood is not None and (understood.get("intent") or "") != "smalltalk":
            return "help"
        return None
    spelled = _spelled_out(clean)
    if WHAT_ARE_YOU.search(clean) or WHAT_ARE_YOU.search(spelled):
        return "identity"
    if re.search(r"\bwhat are you\b", spelled) and not _the_answers_take_it(clean):
        if WHAT_ARE_YOU_NOUN.search(clean):
            return "identity"
        if GOOD_AT_ASK.search(clean):
            return "help"
        if CLOTHES_ASK.search(clean):
            return "clothes"
        if LIKE_ASK.search(clean):
            return "identity"
        return "self_doing"
    if WORKINGS_ASK.search(clean):
        return "workings"
    if ASKING_ASK.search(_self):
        return "asking"
    for phrase in IDENTITY:
        if phrase in clean or phrase in spelled:
            return "identity"
    if FORGETTING_ASK.search(clean):
        return "memory"
    for phrase in MEMORY:
        if phrase in clean or phrase in spelled:
            if RECALL_TAIL.search(clean) and _the_store_takes_it(clean):
                return None
            return "memory"
    if isinstance(understood, dict):
        kind = understood.get("about_bot_kind")
        if kind in ABOUT or kind in ABOUT_SELF:
            return kind
    asked = HUMAN_ASK.search(clean)
    if asked and _opens_the_line(clean[:asked.start()]) \
            and not _asks_elsewhere(clean[asked.end():]):
        return "identity"
    if _asks_for_a_person_to_talk_to(clean):
        return "identity"
    matched = HELP_ELSE.search(clean)
    if matched and _free_tail(matched.group(1) or matched.group(2)):
        return "help"
    if _asks_for_help(clean, understood):
        return "hand"
    return _the_bot_itself(clean)


MODEL_NAMED = re.compile(
    r"\b(?:what|which)\s+(?:version|model|kind|type|sort)\s+of\s+(?:gpt|chatgpt|ai|llm|model|"
    r"chatbot|bot|openai)\s+(?:are|is)\s+(?:you|u|this|it)\b|"
    r"\b(?:is|are)\s+(?:this|that|it|you|u)\s+(?:a\s+|an\s+|really\s+)?(?:chatgpt|gpt[-\s]?\d*|"
    r"openai|claude|gemini|bard|llama|copilot|an?\s+(?:ai|llm|chatbot|bot))"
    r"\s*(?:then|really|though|now|huh|yeah|or not)?\s*$")


def _names_the_make(clean):
    said = re.findall(r"[a-z0-9']+", str(clean or "").lower())
    return len(said) <= MODEL_NAMED_WORDS and bool(MODEL_NAMED.search(" ".join(said)))


def about_the_bot(clean):
    return _the_bot_itself(clean)


DOUBT_OPENER = re.compile(r"^(?:so|and|but|oh|ok|okay|well|right|actually|honestly)\s+")
DOUBT_TAIL = re.compile(
    r"(?:\s+(?:then|though|really|at all|any more|anymore|these days))+$"
    r"|\s+(?:can|could|do|does|are|will|would)\s+(?:you|u)$")
DOUBT_NOT = re.compile(
    r"\b(?:you|u(?:r)?)\s+(?:just\s+|only\s+|actually\s+|really\s+|still\s+)?"
    r"(?:can ?t|cant|cannot|can not|could ?nt|couldn ?t|don ?t|dont|do not|does ?nt|doesn ?t|"
    r"won ?t|wont|will not|never)\s+")


DOUBT_NOT_BE = re.compile(r"\b(?:youre|you are)\s+(?:not|n ?t)\s+")


def _a_doubt_about_the_bot(clean):
    line = clean
    for _ in range(3):
        stripped = DOUBT_OPENER.sub("", line)
        if stripped == line:
            break
        line = stripped
    line = DOUBT_TAIL.sub("", line)
    asked = None
    notted = DOUBT_NOT.search(line)
    if notted:
        asked = "can you " + line[notted.end():].strip()
    else:
        notted = DOUBT_NOT_BE.search(line)
        if notted:
            asked = "are you " + line[notted.end():].strip()
    if not asked or asked.endswith(("you", "you can", "you are")):
        return None
    return _about(asked, None)


def _the_bot_itself(clean):
    clean = _self_line(clean)
    return _about_itself(clean) or _a_doubt_about_the_bot(clean)


ABOUT_THE_PERSON = re.compile(
    r"\babout (?:me|us|my|our)\b|\bknow (?:about|of) (?:me|us|my)\b"
    r"|\bremember (?:me|my|what i|what we|anything|things)\b|\bwhat have you (?:kept|remembered)\b",
    re.I)


def _about_itself(clean):
    if REFERS_BACK.search(clean) and not NAMES_THE_BOT.search(clean):
        return None
    said = [word.strip("?!.,;:\"'()") for word in clean.split()]
    if REGRET_ASK.search(clean):
        return "regret"
    if SELF_PURPOSE.search(clean):
        return "purpose"
    if MADE_ASK.search(clean):
        return "agency"
    if MODEL_ASK.search(clean) or _names_the_make(clean) or WORKINGS_ASK.search(clean):
        return "model"
    if LIMITS_ASK.search(_self_line(clean)):
        return "limits"
    if ONLINE_ASK.search(_self_line(clean)) and not OWN_DEVICE.search(_self_line(clean)) \
            and not A_BARE_ONLINE.search(clean):
        return "online"
    if not SELF_ASK.search(clean):
        return None
    view = A_VIEW_ASKED_FOR.match(clean)
    if view and not re.match(
            r"\s*(?:you|u|youre|you're|ur|yourself|for\s+yourself|about\s+yourself|"
            r"by\s+yourself|on\s+your\s+own)\b", view.group(1)):
        return None
    if ABOUT_THE_PERSON.search(clean):
        return None
    rest = [w for w in said
            if w not in SELF_FILLER and w not in ("you", "u", "youre", "you're", "ur")]
    if not rest:
        if re.search(r"\bwhy\b", clean):
            return "purpose"
        return "where" if SELF_OPENER.search(clean) else None
    if any(w not in SELF_WORDS for w in rest):
        return None
    for word in rest:
        if word in PICKS_A_MECHANISM and not re.search(r"\bhow\b", clean):
            continue
        group = SELF_GROUP.get(word)
        if group == "where" and word in ("here", "there") and re.search(r"\bwhy\b", clean):
            return "purpose"
        if group:
            return group
    return None


def _burn_line(clean, thread=""):
    if BURN_BLISTER_LINE.search(clean) or BURN_ON_IT.search(clean):
        return True
    if POP_A_BARE_IT.search(clean) and (BURN_WORD.search(str(thread or "").lower())
                                        or BURN_WORD.search(clean)):
        return True
    return bool(BURN_THING.search(clean) and BURN_ASK.search(clean))


ABUSE_CARD = re.compile(r"\b(?:domestic\s+)?abuse\s+(?:helpline|charity|service|line)\b", re.I)
_ASKS_TO_LEAVE = re.compile(
    r"\b(?:should|shall|can|could|do|must)\s+(?:i|we)\s+(?:just\s+)?"
    r"(?:leave|go|stay|come\s+back|go\s+back|walk\s+out|get\s+out|move\s+out|run)\b"
    r"(?!\s+(?:the|my|your|a|an|it|this|that)\b)"
    r"|\b(?:should|shall|can|could|do|must)\s+(?:i|we)\s+(?:call|ring|phone|dial)\s+"
    r"(?:the\s+)?(?:police|cops|999|911|an?\s+ambulance)\b", re.I)
_THE_WAY_OUT = re.compile(
    r"\b(?:get|gets|getting|got|come|comes|coming|clear|clearing|climb|climbing|stagger\w*)\s+"
    r"out\s+of\s+(?:a|an|the|my|our|his|her|their)?\s*"
    r"(?:house|home|flat|building|block|room|car|van|vehicle|bed|bath|bathroom|kitchen|lift|"
    r"elevator|road|water)\b"
    r"|(?:\b(?:should|shall|do|can|could)\s+(?:i|we)\b"
    r"|\bis\s+it\s+(?:safe|ok|okay|alright|best|wise)\b"
    r"|\bwould\s+it\s+be\s+(?:better|safer|ok|okay)\b"
    r")[^.?!]{0,20}\b(?:go|going|get|leave|leaving|stay|staying|move|moving|open|opening|"
    r"close|closing|shut|shutting|ventilate)\b[^.?!]{0,20}\b(?:outside|outdoors|upstairs|"
    r"downstairs|up\s+stairs|down\s+stairs|home|house|flat|building|room|away|clear|"
    r"fresh\s+air|window|windows|door|garden|corridor|landing|down|up|"
    r"out\b(?!\s+of)|back\s+in|back\s+inside|in\s+there)\b"
    r"|\b(?:should|shall|do|can|could|must)\s+(?:i|we)\s+(?:just\s+)?(?:stay|wait|sit|hold)\b"
    r"[^.?!]{0,20}\b(?:where\s+(?:i|we)\s+am|where\s+(?:i|we)\s+are|put\b|here|inside|"
    r"in\s+the\s+(?:house|flat|room|car|building)|for\s+(?:help|the\s+(?:ambulance|fire|"
    r"paramedics|doctor)|them|someone))\b",
    re.I)


_HAZARD_WORD = re.compile(
    r"\b(?:" + "|".join(sorted(re.escape(w) for w in HAZARD_WORDS)) + r")\b", re.I)

_FETCH_FROM_INSIDE = re.compile(
    r"\b(?:can|could|should|shall|do|may)\s+(?:i|we)\s+(?:just\s+|quickly\s+)?"
    r"(?:go\s+(?:and\s+|to\s+)?)?"
    r"(?:back\s+in|get|grab|fetch|collect|save|rescue|nip\s+in|run\s+in)\b[^.?!]{0,30}"
    r"\b(?:my|our|the|his|her|their)\s+\w+", re.I)


_GAS_WORD = re.compile(r"\b(?:gas|gases|fumes?|carbon\s+monoxide|flue)\b", re.I)
_FIRE_WORD = re.compile(r"\b(?:fires?|flames?|smoke|smoking|ablaze|burning|burnt)\b", re.I)


def _the_hazard_is_gas(line):
    said = str(line or "")
    return bool(_GAS_WORD.search(said)) and not _FIRE_WORD.search(said)


def _goes_back_for(clean, thread=""):
    if not (_HAZARD_WORD.search(clean) or _HAZARD_WORD.search(str(thread or ""))):
        return False
    return bool(_FETCH_FROM_INSIDE.search(clean))


def _names_a_new_part(words, clean, thread):
    part = words & trouble.BODY_PART
    if not part or not trouble.reads_as_trouble(clean, words):
        return False
    if words & (CARE_POINTER | CARE_PRONOUNS):
        return False
    seen = set(re.findall(r"[a-z0-9']+", str(thread or "").lower()))
    return not (part & seen)


def _keeps_thread(understood, clean, thread="", crisis=False):
    norm = understood.get("norm")
    if isinstance(norm, (list, tuple)):
        words = set(norm)
    else:
        words = set(re.findall(r"[a-z0-9']+", str(norm or clean)))
    if not crisis and _names_a_new_part(words, clean, thread):
        return False
    if _ASKS_TO_LEAVE.search(clean) and SOMEBODY_HURT_ME.search(str(thread or "")):
        return True
    if _THE_WAY_OUT.search(clean):
        return True
    if words & CARE_HURTS:
        return True
    if not crisis and not (words & CARE_INJURY) and HOUSE_FAULT.search(clean):
        return False
    if (words & CARE_WORDS) - CARE_POINTER or CARE_ASKS.search(clean):
        return True
    own = understood.get("topic_own")
    if words & CARE_RESOLVED and words & CARE_NOT_RESOLVED and own in (None, "feelings", "health"):
        return True
    if words & REACTION_WORDS:
        return True
    if words & CARE_POINTER and not understood.get("topic_own") \
            and not _POINTER_OWN_OBJECT.search(clean):
        return True
    if any(phrase in clean for phrase in CARE_PHRASES) or CARE_SEEN_ASKS.search(clean):
        return True
    if _someone_is_arriving(clean):
        return True
    if ALREADY_RANG.search(clean):
        return True
    if _burn_line(clean, thread):
        return True
    if understood.get("presence") or STILL_HERE.search(clean):
        return True
    if understood.get("kind") == "thanks":
        return len(words) <= 5
    if crisis and words & trouble.BODY_PART:
        return True
    if understood.get("kind") == "question" or "?" in clean:
        keywords = understood.get("keywords") or []
        return all(str(word).lower() in GENERIC_WORDS for word in keywords)
    if len(words) <= 2 and words & AGREEMENTS:
        return True
    if not understood.get("topic_own"):
        mine = {w for w in words if len(w) > 3 and w not in ASKING_WORDS}
        thread_words = set(re.findall(r"[a-z0-9']+", str(thread or "").lower()))
        return bool(mine & thread_words) or not mine
    return False


def _reads_as_fear(understood, clean):
    if understood.get("kind") == "question" or "?" in clean:
        return False
    if CARE_ASKS.search(clean):
        return False
    if not ABOUT_THE_SPEAKER.search(clean):
        return False
    if NOT_FRIGHTENED.search(clean):
        return False
    if FRIGHTENED.search(clean):
        return True
    return _only_a_worry(clean)


def _only_a_worry(clean):
    if re.search(r"\babout\b", clean):
        return False
    words = re.findall(r"[a-z']+", clean)
    if not words or len(words) > 6:
        return False
    if not WORRY_WORDS & set(words):
        return False
    return all(word in WORRY_FILLER or word in WORRY_WORDS for word in words)


A_BACK_AGAIN = re.compile(
    r"^(?:(?:im|i'm|i am)\s+)?(?:back|here|still here)(?:\s+(?:again|now|too))?[.!]*$|"
    r"^(?:hi|hiya|hello|hey)(?:\s+[a-z']+){0,2}[.!]*$")


def _about_somebody_else(safety, memory):
    opener = str((safety or {}).get("user") or "")
    if SELF_IN_DANGER.search(opener):
        return None
    if SOMEBODY_HURT_ME.search(opener):
        return None
    found = A_PERSON_OF_THEIRS.search(opener)
    if found is None:
        if not A_PRONOUN_FOR_SOMEBODY.search(opener):
            return None
        try:
            turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
        except AttributeError:
            return None
        for turn in reversed(turns[-4:]):
            said = str(turn.get("user") or "")
            if said == opener or SELF_IN_DANGER.search(said):
                continue
            found = A_PERSON_OF_THEIRS.search(said)
            if found is not None:
                break
    if found is None:
        return None
    word = re.sub(r"\s+", " ", found.group("who").strip().lower())
    if word in SHE:
        forms = {"subject": "she", "object": "her", "possessive": "her", "be": "is"}
    elif word in HE:
        forms = {"subject": "he", "object": "him", "possessive": "his", "be": "is"}
    else:
        forms = {"subject": "they", "object": "them", "possessive": "their", "be": "are"}
    forms["who"] = "your " + word
    return forms


def _wrote_for_them(pool, forms):
    return tuple(line.format(who=forms["who"], subj=forms["subject"], obj=forms["object"],
                             poss=forms["possessive"], be=forms["be"]) for line in pool)


A_CONDITION = re.compile(r"\b(?:if|unless|when|whenever|once|in case|as soon as)\b", re.I)
ALREADY_OR_NOT = re.compile(r"\bif\s+(?:you\s+)?(?:have\s?n[o']?t|havent|not)\b", re.I)
SENTENCE_END = re.compile(r"(?<=[.!?;])\s+")
CLAUSE_END = re.compile(r"[,;:]\s+|\s+(?:and|but|so|then|or)\s+")

CARE_ROUTE_WORDS = (
    ("vet", re.compile(r"\b(?:the\s+)?vets?\b", re.I)),
    ("dentist", re.compile(r"\bdentist\w*\b|\bdental\b", re.I)),
    ("pharmacist", re.compile(r"\bpharmac(?:ist|y)\b|\bchemist\b", re.I)),
    ("walk-in", re.compile(r"\bwalk[- ]in\b|\burgent care\b", re.I)),
    ("111", re.compile(r"(?<!\d)111(?!\d)|\bnhs 111\b", re.I)),
    ("gp", re.compile(r"\b(?:gp|g\.p\.|doctor|surgery|practice nurse)\b", re.I)),
)

THE_THING_ITSELF_LOOKS_FINE = re.compile(
    r"\b(?:eating|drinking|playing|running about|running around|chatting|talking|sleeping well|"
    r"seems (?:fine|himself|herself|themselves|ok|okay|alright|bright)|looks (?:fine|well|ok|"
    r"okay|alright|better)|perky|bright as|back to (?:normal|himself|herself))\b", re.I)


RED_FLAG_SHARED = re.compile(
    r"\b(?:arm|arms|jaw|neck|shoulder|shoulders|back|chest|sweat\w*|clammy|breathless\w*|"
    r"breath|breathing|lip|lips|grey|gray|blue|faint\w*|passed\s+out|collaps\w*|rest|resting|"
    r"sitting|speech|slurr\w*|numb(?:ness|ed|ing|s)?|drow\w*|floppy|seizure|fits?|vomit\w*|blood|pale|"
    r"dizz\w*)\b", re.I)


def _red_flags_in(line):
    low = " ".join(str(line or "").lower().split())
    flags = set()
    for match in RED_FLAG_SHARED.finditer(low):
        before = low[:match.start()].split()[-4:]
        after = low[match.end():].split()[:4]
        if any(word in ("not", "no", "never", "isnt", "arent", "havent", "hasnt", "dont", "didnt")
               for word in before):
            continue
        if "stopped" in after or ("any" in after and "more" in after) or \
                ("no" in after and ("more" in after or "longer" in after)):
            continue
        flags.add(_flag_stem(match.group()))
    return flags


RED_FLAG_EVENTS = re.compile(
    r"\b(?:passed\s+out|passing\s+out|fainted|fainting|collaps\w*|unconscious|knocked\s+out|"
    r"clammy|slurr\w*|floppy|seizures?|convuls\w*|drooling|not\s+waking|cant\s+wake|"
    r"couldnt\s+wake|could\s+not\s+wake|wont\s+wake)\b", re.I)


def _flag_events_in(line):
    low = " ".join(str(line or "").lower().split())
    found = set()
    for match in RED_FLAG_EVENTS.finditer(low):
        before = low[:match.start()].split()[-4:]
        if any(word in ("not", "no", "never", "isnt", "arent", "havent", "hasnt", "dont",
                        "didnt", "wasnt", "without") for word in before):
            continue
        found.add(_flag_stem(match.group().split()[0]))
    return found


THRESHOLD_CLAUSE = re.compile(r"\b(?:if|when|whenever|once)\b\s+(.{3,140})", re.I)
THRESHOLD_NOT_A_SIGN = frozenset("""
the a an and or of to in on at for with without if it its this that your you yours they them
their he she his her is are was were be been being do does did done have has had can could would
should will shall may might must not no dont cant wont also too very really just only even still
more most less least than then there here any anything something everything nothing someone
somebody anyone anybody what when where which who how why get gets getting go goes going went come
comes coming make makes making take takes taking please sorry help helps helped need needs needed
want wants wanted like likes tell tells told say says said see sees look looks try tries tried
thing things way ways time times day days moment minute hour about after before again once twice
first last next other another same own such because so but however though always never sometimes
often soon later early late today tonight tomorrow morning afternoon evening night emergency
emergencies ambulance hospital doctor gp nurse care service services team advice line risk danger
sign signs symptom symptoms feeling feel feels felt seem seems seemed become becomes became
becoming much many lot lots bit little kind sort sure give gives given keep keeps watch watching
worse bad good well hard suddenly sudden started starts start stopped stops happen happens lasted
ring rings ringing call calls calling called phone number numbers nhs straight away right now
immediately urgent quickly twice back gone around through even
alright fine okay normal better best settled eased easing quiet
four five six seven eight nine ten eleven twelve thirteen fourteen fifteen twenty thirty forty
fifty sixty hundred thousand minutes hours weeks days months years month week year day
""".split())
A_FEELING_OF = ("feels like {w}", "feel like {w}", "feeling like {w}", "felt like {w}",
                "feels {w}", "feel {w}", "feeling {w}", "like {w}", "{w} now", "{w} again",
                "{w} too", "{w} back", "{w} is back", "{w} coming on", "in my {w}", "on my {w}",
                "my {w}", "some {w}")


def _the_threshold_words(sentence):
    low = " ".join(str(sentence or "").lower().split())
    words = set()
    for match in THRESHOLD_CLAUSE.finditer(low):
        if match.group(0).lstrip().lower().startswith("even if"):
            continue
        for word in re.findall(r"[a-z']+", match.group(1)):
            if len(word) < 4 or word in THRESHOLD_NOT_A_SIGN:
                continue
            words.add(_flag_stem(word))
    return words


def _it_is_the_answer_word(line, word):
    low = " ".join(str(line or "").lower().split())
    if not re.search(r"\b" + re.escape(word) + r"\w*\b", low):
        return False
    for shape in A_FEELING_OF:
        said = r"(?:the\s+|a\s+|some\s+)?" + re.escape(word) + r"\w*"
        if re.search(r"\b" + shape.replace("{w}", said) + r"\b", low):
            return True
    return False


def _the_flags_still_standing(line):
    clauses = [c for c in CLAUSE_END.split(str(line or "").lower()) if c.strip()]
    settled = [c for c in clauses if _feels_better(c) or RESOLVED.search(c)]
    if not settled:
        return _red_flags_in(line)
    flags = set()
    for clause in clauses:
        if clause in settled or re.search(r"\b(?:was|were|had)\b", clause):
            continue
        flags |= _red_flags_in(clause)
    return flags


def _the_threshold_was_crossed(last, clean, turns):
    said = str(last or "").lower()
    if not said or not CALL_THEM_NOW.search(said):
        return False
    line = str(clean or "")
    if _the_thread_is_an_animal(line, turns):
        return False
    if _flag_events_in(line):
        return True
    flags = _the_flags_still_standing(line)
    for sentence in SENTENCE_END.split(said):
        if not CALL_THEM_NOW.search(sentence):
            continue
        if flags & _red_flags_in(sentence):
            return True
        if _feels_better(line) or RESOLVED.search(str(clean or "").lower()):
            continue
        for word in _the_threshold_words(sentence):
            if _it_is_the_answer_word(line, word):
                return True
    return False


def _flag_stem(word):
    for tail in ("ing", "ness", "ed", "y", "s"):
        if word.endswith(tail) and len(word) - len(tail) >= 4:
            word = word[:-len(tail)]
    return word


THE_CALL_POOLS = tuple(THRESHOLD_CROSSED) + tuple(THE_CALL_STANDS)


def _it_is_this_files_call(said):
    said = " ".join(str(said or "").lower().split())
    for line in THE_CALL_POOLS:
        if said.startswith(" ".join(line.lower().split())[:40]):
            return True
    return False


def _a_newer_answer_asked_them_to_call(last, turns):
    for turn in reversed(turns[-THREAD_TURNS:]):
        if not isinstance(turn, dict):
            continue
        said = str(turn.get("bot") or "")
        if not said:
            continue
        if said.strip().lower() == str(last or "").strip().lower():
            return False
        if turn.get("module") != FALLBACK_MODULE:
            return False
        if _the_answer_asked_them_to_call(said) or _it_is_this_files_call(said):
            return True
    return False


def _the_route_the_answer_named(last):
    text = str(last or "")
    if not text:
        return None
    if re.search(r"0800\s*111\s*999", text):
        text = re.sub(r"0800\s*111\s*999", "the gas emergency line", text)
    for name, pattern in CARE_ROUTE_WORDS:
        if pattern.search(text):
            return name
    return None


def _the_answer_asked_them_to_call(last):
    for sentence in SENTENCE_END.split(str(last or "")):
        low = ALREADY_OR_NOT.sub("already", sentence.lower())
        clauses = CLAUSE_END.split(low)
        led_by_condition = False
        for clause in clauses:
            opens_with_condition = A_CONDITION.search(clause) is not None and (
                not re.search(r"\b(?:call|ring|ringing|dial|phone|text|press|try)\b", clause))
            if CALL_THEM_NOW.search(clause):
                if A_CONDITION.search(clause) is None and not led_by_condition:
                    return True
            led_by_condition = opens_with_condition
    return False


def _raises_the_stakes(clean, last):
    return bool(STAKES_WORDS.search(clean)) and bool(FALL_FIRST_AID.search(str(last or "").lower()))


def _releasable(memory):
    for turn in reversed([t for t in (memory.get("turns") or []) if isinstance(t, dict)][-THREAD_TURNS:]):
        if turn.get("module") == "safety":
            last = str(turn.get("bot") or "").lower()
            return not (any(word in last for word in CRISIS_WORDS)
                        or _the_answer_asked_them_to_call(last))
        if turn.get("module") != FALLBACK_MODULE:
            return False
    return True


def _named_draft(memory, text, words, clean):
    if not draft.says_it_is_the_message(clean):
        return None
    if (_action(clean, memory) or reads_as_pregnancy_bleeding(clean)
            or reads_as_sudden_loss(clean)):
        return None
    drafted = draft.drafter(memory, text, words)
    if not drafted:
        return None
    return _choose([f'{lead} "{drafted}"' for lead in draft.LEAD_INS], memory, clean)


def _after_safety(memory, clean, understood=None):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    safety = None
    window = turns[-THREAD_TURNS:]
    for index in range(len(window) - 1, -1, -1):
        if window[index].get("module") == "safety":
            safety = window[index]
            window = window[index + 1:]
            break
    if safety is None:
        return None
    read = understood if isinstance(understood, dict) else memory.get("understood")
    if not isinstance(read, dict):
        read = understand(clean, memory)
    last = str(safety.get("bot") or "").lower()
    for turn in window:
        if turn.get("module") == FALLBACK_MODULE:
            continue
        if history.not_a_subject(str(turn.get("user") or "")):
            continue
        if _words_kept(turn.get("bot"), last) >= THE_THREAD_KEPT:
            continue
        return None
    if _reads_as_fear(read, clean) and not any(word in last for word in CRISIS_WORDS):
        return _choose(AFRAID_AFTER, memory, clean)
    words = read.get("words")
    if not isinstance(words, list):
        words = re.findall(r"[a-z0-9']+", clean)
    in_crisis = any(word in last for word in CRISIS_WORDS)
    live = in_crisis or _the_answer_asked_them_to_call(last) or _raises_the_stakes(clean, last)
    if read.get("kind") == "greeting" and not (set(words) & CARE_WORDS):
        if live:
            return _choose(HELLO_WITH_YOU if in_crisis else HELLO_STILL_THERE, memory, clean)
        return _choose(GREETING_AFTER, memory, clean)
    if _asks_how_are_you(clean, read.get("plain") or clean) and not _burn_line(clean):
        return _choose(CARE_HERE, memory, clean)
    if not live and A_BACK_AGAIN.match(clean.strip()):
        return _choose(GREETING_AFTER, memory, clean)
    if _short_ack(words) and not live and _thread_was_closed(turns):
        return None
    if MOVE_ON.search(clean):
        return _choose(MOVE_ON_AFTER, memory, clean)
    if not in_crisis:
        advice = _asks_about_the_advice(clean, last)
        if advice:
            return _choose(advice, memory, clean)
    if outlook.asks_the_outlook(clean):
        cards = _the_safety_cards(turns)
        in_a_crisis = any(word in card for card in cards for word in CRISIS_WORDS)
        told_to_call = any(_the_answer_asked_them_to_call(card) for card in cards)
        abuse = any(_the_answer_was_an_abuse_card(card) for card in cards)
        pool = outlook.the_pool(in_a_crisis, _somebody_is_coming(turns, clean), told_to_call,
                                abuse=abuse)
        if pool is None:
            pool = [phrase.format(who="you") for phrase in FORECAST_AFTER_SAFETY]
        return _choose(pool, memory, clean)
    them = _about_somebody_else(safety, memory)
    if _the_answer_was_an_abuse_card(last) and (_THE_WAY_OUT.search(clean)
                                                 or _ASKS_TO_LEAVE.search(clean)):
        return _choose(ABUSE_AFTER, memory, clean)
    if live and _a_report_on_the_advice(clean, words, False) in (
            TRIED_NO_CHANGE, TRIED_NO_CHANGE_ELSEWHERE, TRIED_WORSE, TRIED_WORSE_ELSEWHERE):
        if in_crisis and them:
            return _choose(_wrote_for_them(CRISIS_AFTER_THEM, them), memory, clean)
        return _choose(CRISIS_AFTER if in_crisis else EMERGENCY_NOT_WORKED, memory, clean)
    if THING_SORTED.search(clean):
        return _choose(CRISIS_AFTER if in_crisis
                       else _hold_pool(turns, clean, last, done_report=True),
                       memory, clean)
    if not in_crisis:
        from . import verdict
        reading = verdict.reply_for(clean, memory)
        if reading:
            return reading
    if in_crisis and (_a_lost_ask(clean) or _a_start_ask(clean)):
        return _choose(CRISIS_AFTER, memory, clean)
    if _the_hazard_is_gas(safety.get("user")) and (
            _THE_WAY_OUT.search(clean) or _goes_back_for(clean, safety.get("user") or "")):
        return GAS_ANSWER
    if _the_threshold_was_crossed(last, clean, turns):
        return _choose(THRESHOLD_CROSSED, memory, clean)
    if not _feels_better(clean) and not (
            _goes_back_for(clean, safety.get("user") or "")
            or _keeps_thread(
                read, clean, safety.get("user") or "",
                crisis=not _releasable(memory) or _raises_the_stakes(clean, last))):
        return None
    if (read.get("kind") == "thanks" or set(words) & THANKS_WORDS) \
            and not _thanks_carries_emergency(words, clean):
        return _choose(THANKS_AFTER, memory, clean)
    if _short_ack(words):
        if in_crisis:
            return _choose(CRISIS_AFTER, memory, clean)
        return _choose(_hold_pool(turns, clean, last), memory, clean)
    last = str(safety.get("bot") or "").lower()
    asked = read.get("kind") == "question" or "?" in clean
    if not _reads_as_fear(read, clean) and set(words) & REACTION_WORDS and any(
            str(t.get("bot") or "") in RESOLVED_AFTER for t in turns[-2:]):
        return _choose(AFTER_RESOLVED, memory, clean)
    if (not asked and RESOLVED.search(clean) and not NEEDS_SEEN.search(clean)
            and not _someone_is_arriving(clean)):
        if not them and _a_newer_answer_asked_them_to_call(last, turns) \
                and not ALREADY_RANG.search(clean):
            return _choose(THE_CALL_STANDS_ANYWAY, memory, clean)
        return _choose(_wrote_for_them(RESOLVED_AFTER_THEM, them) if them else RESOLVED_AFTER,
                       memory, clean)
    if ALREADY_RANG.search(clean):
        if A_HELPLINE.search(clean):
            if any(word in last for word in CRISIS_WORDS):
                return _choose(_wrote_for_them(CRISIS_AFTER_THEM, them) if them else CRISIS_AFTER,
                               memory, clean)
            if any(word in last for word in SAFETY_WORDS):
                return _choose(HELPLINE_NOT_AN_AMBULANCE, memory, clean)
            return _choose(STILL_HERE_AFTER, memory, clean)
        if any(word in last for word in CRISIS_WORDS):
            return _choose(_wrote_for_them(CRISIS_AFTER_THEM, them) if them else CRISIS_AFTER,
                           memory, clean)
        return _choose(HOLD_AFTER, memory, clean)
    if _reads_as_fear(read, clean) and not any(word in last for word in CRISIS_WORDS):
        return _choose(AFRAID_AFTER, memory, clean)
    if set(words) & REACTION_WORDS:
        if any(word in last for word in CRISIS_WORDS):
            return _choose(_wrote_for_them(CRISIS_AFTER_THEM, them) if them else CRISIS_AFTER,
                           memory, clean)
        return _choose(_hold_pool(turns, clean, last), memory, clean)
    if (VISIT_ASK.search(clean) and not MEDICAL_PLACE.search(clean)
            and not NOT_A_VISIT.search(clean) and _somebody_to_visit(clean, turns)):
        pool = CARE_VISIT_WARD if _someone_is_a_patient(clean, turns) else CARE_VISIT
        return _choose(pool, memory, clean)
    if CARE_SEEN_ASKS.search(clean):
        if _the_thread_is_an_animal(clean, turns):
            return _choose(CARE_SEEN_ANIMAL, memory, clean)
        return _choose(CARE_SEEN, memory, clean)
    if _feels_better(clean):
        if _no_relief(memory, last):
            if them:
                return _choose(_wrote_for_them(EMERGENCY_BETTER_THEM, them), memory, clean)
            return _choose(EMERGENCY_BETTER, memory, clean)
        if any(w in last for w in CRISIS_WORDS):
            if them:
                return _choose(_wrote_for_them(CRISIS_BETTER_THEM, them), memory, clean)
            return _choose(CRISIS_BETTER, memory, clean)
        return _choose(CARE_BETTER, memory, clean)
    opener = str(safety.get("user") or "").lower()
    if BURN_WORD.search(last) or BURN_WORD.search(opener):
        if BURN_BLISTER_LINE.search(clean) or POP_A_BARE_IT.search(clean):
            return _choose(BURN_BLISTER, memory, clean)
        if BURN_ON_IT.search(clean) or (BURN_THING.search(clean) and BURN_ASK.search(clean)):
            return _choose(BURN_AFTER, memory, clean)
    if them and SAID_AS_A_DEATH.search(clean):
        return None
    if any(word in last for word in CRISIS_WORDS):
        return _choose(_wrote_for_them(CRISIS_AFTER_THEM, them) if them else CRISIS_AFTER,
                       memory, clean)
    if _someone_is_arriving(clean):
        return _choose(WITH_YOU_AFTER, memory, clean)
    if _already_rang(turns):
        return _choose(HOLD_AFTER, memory, clean)
    if _the_answer_asked_them_to_call(last) or _raises_the_stakes(clean, last):
        if _is_a_hazard(last):
            return _choose(HAZARD_AFTER, memory, clean)
        return _choose(EMERGENCY_AFTER, memory, clean)
    if _the_thread_is_an_animal(clean, turns):
        return _choose(CARE_AFTER_ANIMAL_STILL if STILL_GOING.search(clean) else CARE_AFTER_ANIMAL,
                       memory, clean)
    if _a_newer_answer_asked_them_to_call(last, turns):
        return _choose(THE_CALL_STANDS, memory, clean)
    route = _the_route_the_answer_named(last)
    if route and not THE_THING_ITSELF_LOOKS_FINE.search(clean):
        return _choose(CARE_ROUTE_BACK[route], memory, clean)
    return _choose(CARE_AFTER_STILL if STILL_GOING.search(clean) else CARE_AFTER, memory, clean)


def _is_a_hazard(last):
    return bool(HAZARD_LINE.search(str(last or "").lower()))


def _the_safety_cards(turns):
    return [str(turn.get("bot") or "").lower() for turn in list(turns or [])[-THREAD_TURNS:]
            if str(turn.get("module") or "") == "safety"]


def _somebody_is_coming(turns, clean):
    for turn in list(turns or [])[-THREAD_TURNS:]:
        said = str(turn.get("user") or "").lower()
        if said and (ALREADY_RANG.search(said) or _someone_is_arriving(said)):
            return True
    return bool(ALREADY_RANG.search(clean)) or bool(_someone_is_arriving(clean))


def _the_answer_was_an_abuse_card(last):
    return bool(ABUSE_CARD.search(str(last or "")))


def _thread_was_closed(turns):
    for turn in reversed(turns[-THREAD_TURNS:]):
        if turn.get("module") != FALLBACK_MODULE:
            continue
        return any(str(turn.get("bot") or "").startswith(line[:24]) for line in THANKS_AFTER)
    return False


def _hold_pool(turns, clean, last, done_report=False):
    if not _a_call_is_known(turns, clean, last):
        return STILL_HERE_AFTER
    if done_report and not (ALREADY_RANG.search(clean) or _already_rang(turns)):
        return SORTED_AND_NO_CALL_YET
    return HOLD_AFTER


IMMEDIATE_CALL = re.compile(
    r"\b(?:ring|call|phone|dial)\s+(?:999|911|112|an\s+ambulance)\b"
    r"|\b999\s+(?:or\s+911\s+)?(?:now|straight|immediately|first)\b"
    r"|\bstraight\s+away\b|\bright\s+now\b|\bthere\s+and\s+then\b", re.I)


def _a_call_is_known(turns, clean, last):
    if ALREADY_RANG.search(clean) or _already_rang(turns):
        return True
    text = str(last or "")
    if not any(word in text for word in CALL_WORDS):
        return False
    if "111" in text and not IMMEDIATE_CALL.search(text):
        return False
    return not _the_call_is_conditional(text)


CONDITIONAL_OPENING = re.compile(
    r"^\W*(?:if|unless|when|whenever|in\s+case|should|after|once|any\s*time)\b", re.I)


def _the_call_is_conditional(text):
    carrying = [sentence for sentence in re.split(r"(?<=[.!?])\s+", str(text or ""))
                if any(word in sentence.lower() for word in CALL_WORDS)]
    if not carrying:
        return False
    return all(CONDITIONAL_OPENING.search(sentence.strip()) for sentence in carrying)


def _already_rang(turns):
    return any(ALREADY_RANG.search(str(turn.get("user") or "").lower())
               for turn in turns[-3:] if isinstance(turn, dict))


def _thanks_carries_emergency(words, clean):
    said = set(words)
    content = (said & CARE_WORDS) - THANKS_WORDS - CARE_PRONOUNS - CARE_POINTER
    if content and said & ONGOING_WORDS:
        return True
    if said & CARE_RESOLVED:
        return bool(said & CARE_NOT_RESOLVED)
    return bool(content or CARE_ASKS.search(clean) or CARE_SEEN_ASKS.search(clean)
                or any(phrase in clean for phrase in CARE_PHRASES))


A_DATE_OF_OURS = re.compile(
    r"\b(?:forget(?:s|ting|ful)?|forgot)\b[^.]{0,24}?\b(?:our|my)\s+"
    r"(?:anniversary|birthdays?|dates?(?: night)?|valentine'?s|wedding day|christmas|plans?)\b")


A_WORRY_ABOUT_THEM = re.compile(
    r"\b(?:something|summat)\s+(?:is|seems|feels)\s+(?:wrong|off|not right)\b|"
    r"\bnot (?:like|acting like) (?:him|her|them|himself|herself|themselves)\b|"
    r"\bnot (?:quite |really |been )?(?:himself|herself|themselves)\b|"
    r"\bnot (?:his|her|their) usual (?:self|selves)\b|"
    r"\b(?:worse|worrying)\b|\bworried about (?:him|her|them)\b|"
    r"\bshould i (?:be )?worr(?:y|ied)\b|\bdementia\b|\balzheim\w*\b|"
    r"\bconfus(?:ed|ion)\b|\bmemory\b")


def a_date_of_ours_forgotten(clean):
    said = " ".join(str(clean or "").lower().split())
    return bool(A_DATE_OF_OURS.search(said)) and not A_WORRY_ABOUT_THEM.search(said)


def _impact_said(clean):
    tokens = re.findall(r"[a-z']+", clean)
    found = set()
    for position, token in enumerate(tokens):
        if token not in GRIEVANCE_IMPACT:
            continue
        before = tokens[max(0, position - 2):position]
        if before and before[-1] in NOT_THEIR_VERB:
            continue
        if any(word in FIRST_PERSON for word in before):
            continue
        if token in FORGETTING and not (set(tokens[position + 1:position + 4]) & OURS):
            continue
        if token in EATING and tokens[position + 1:position + 2] and \
                tokens[position + 1] in EATEN_KIND:
            continue
        found.add(token)
    return found


def _grief_thread(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    for turn in reversed(turns[-THREAD_TURNS:]):
        line = str(turn.get("bot") or "")
        if not line:
            continue
        return any(line.startswith(reply[:30]) for reply in loss.LOSS_REPLIES)
    return False


def _grievance_thread(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    for turn in reversed(turns[-THREAD_TURNS:]):
        line = str(turn.get("bot") or "")
        if not line:
            continue
        return any(line.startswith(reply[:30]) for reply in GRIEVANCE)
    return False


def _someone_else_minding(clean, words, after=False):
    said = {w for w in words if w.isalpha() or "'" in w}
    a_person_pronoun = bool(GRIEVANCE_PRONOUN.search(clean))
    if said & GRIEVANCE_PEOPLE:
        if not ({"my", "our", "the"} & said):
            return False
    elif not (after and said & THREAD_PEOPLE) and not a_person_pronoun:
        return False
    spare = clean.replace("thank you", "thanks").replace("thank u", "thanks")
    if " you " in " " + spare + " ":
        return False
    if said & GRIEVANCE_HEALTH or said & GRIEVANCE_HARM:
        if not (a_date_of_ours_forgotten(clean) and not said & GRIEVANCE_HARM):
            return False
    if any(phrase in clean for phrase in GRIEVANCE_HARM_PHRASES):
        return False
    if any(phrase in clean for phrase in GRIEVANCE_HEALTH_PHRASES):
        return False
    if _impact_said(clean) - set(GRIEVANCE_MINE.findall(clean)):
        return True
    if GRIEVANCE_RECUR.search(clean):
        if after and not GRIEVANCE_MINE.search(clean):
            return True
        if any(word not in GRIEVANCE_PEOPLE and word not in GRIEVANCE_NOT_A_THING
               for word in GRIEVANCE_MINE_THINGS.findall(clean)):
            return True
    if any(phrase in clean for phrase in GRIEVANCE_PHRASES):
        return True
    if any(phrase in clean for phrase in GRIEVANCE_STRAIN):
        return True
    return bool(GRIEVANCE_STRAIN_SAID.search(clean))


def _short_ack(words):
    return len(words) <= 2 and bool(set(words) & ACKS)


GOOD_TIME_SUBJECT = re.compile(
    r"\b(?:everyone|everybody|all of them|"
    r"(?:the|my|our|his|her|their|your|\w+'s?)"
    r"(?:\s+\w+){0,2}\s+"
    r"(?:party|wedding|meal|trip|holiday|gig|match|game|concert|night|day|weekend|evening|"
    r"dinner|barbecue|bbq|bash|hen|stag))\b")
GOOD_TIME_OURS = re.compile(
    r"\bwe (?:had|have had) (?:a |such a )?(?:great|lovely|brilliant|good|amazing|wonderful|"
    r"fantastic|smashing)\b")
GOOD_DAY_OURS = re.compile(
    r"^(?:(?:i|we|ive|i've|weve|we've|(?:my|our|the|his|her|their)(?:\s+\w+'s)?"
    r"(?:\s+\w+){0,2})\s+)?(?:had|have had|ve had|has been having|am having|"
    r"are having)\s+(?:a\s+|such a\s+|a really\s+|a proper\s+|a pretty\s+)?"
    r"(?:really\s+|properly\s+|pretty\s+|so\s+|such\s+|super\s+)?"
    r"(?:good|great|lovely|nice|brilliant|amazing|wonderful|lush|smashing|fantastic)\s+"
    r"(?:day|week|weekend|evening|afternoon|morning|night|shift|time|walk|swim|run|ride|"
    r"cycle|lunch|dinner|meal|picnic|bath|shower|breakfast|coffee|nap|sleep|lie in|read)\b")
GOOD_DAY_BARE = re.compile(
    r"^(?:what |such |a )?(?:really |so |pretty |proper |quite )?"
    r"(?:great|lovely|brilliant|amazing|wonderful|fantastic|lush|smashing|perfect)\s+"
    r"(?:day|week|weekend|evening|afternoon|morning|night|shift)\b")
GOOD_DAY_WENT = re.compile(
    r"\b(?:today|yesterday|the day|the week|the weekend|last night|this (?:morning|afternoon|"
    r"evening)|my day|my week|my weekend)\s+(?:was|has been|went|'s been)\s+(?:a\s+)?"
    r"(?:really\s+|so\s+|proper\s+|pretty\s+|such\s+|quite\s+)?"
    r"(?:good|great|lovely|nice|brilliant|amazing|wonderful|fine|alright|lush|fantastic)\b"
    r"|\bbest\s+(?:day|week|weekend|evening|night)\b")
GOOD_TIME_IT = re.compile(
    r"^(?:it|that|this)\s+(?:was|were|has been|s been|turned out)\s+"
    r"(?:(?:a|an|such a|such)\s+)?"
    r"(?:(?:really|so|pretty|proper|properly|quite|absolutely|dead|very)\s+)?"
    r"(?:good|great|lovely|nice|brilliant|amazing|wonderful|fantastic|lush|smashing)\b"
    r"(?:\s+(?:fun|time|day|night|evening|weekend|week|meal|trip|holiday|break|wedding|party|"
    r"gig|show|film|game|match|outing|afternoon|morning|christmas|birthday|dinner|lunch|"
    r"barbecue|do|out|away|all|overall|actually|though|thanks|in the end)\b)*\s*$")


GOOD_VERDICT = re.compile(r"""
    ^\W*(?P<subject>(?:it|its|it\'s|that|thats|that\'s|this|the\s+\w+|my\s+\w+|our\s+\w+)
         (?:\s+(?:was|is|were|are|has\s+been|\'s\s+been))?)\s+
    (?:really\s+|so\s+|proper\s+|pretty\s+|dead\s+|quite\s+|absolutely\s+|well\s+)*
    (?:good|great|lovely|nice|brilliant|amazing|wonderful|lush|smashing|fantastic|superb|
        class|fun)\b
    (?:\s+(?:actually|honestly|tbh|though|to\s+be\s+fair))?\W*$
""", re.X | re.I)


HARD_WEEK = re.compile(r"\b(?:fall|fell|fallen|tripped|collapsed|collapse|seizure|stroke|"
                       r"overdose|accident|crash|crashed|put down|passed away|in hospital|"
                       r"operation|surgery|stitches|broken|broke (?:my|his|her|their))\b")


def _hard_week_in_the_thread(memory):
    if not memory:
        return False
    if loss._loss_is_the_thread(memory):
        return True
    for earlier in [t for t in (memory.get("turns") or []) if isinstance(t, dict)][-2:]:
        line = " ".join(str(earlier.get("user") or "").lower().split())
        if line and (reads_as_bad_news(line) or badnews.reads_as_sudden_loss(line)
                     or HARD_WEEK.search(line)):
            return True
    return False


def _a_verdict(clean, memory=None):
    if _hard_week_in_the_thread(memory):
        return False
    found = GOOD_VERDICT.search(clean)
    if not found:
        return False
    said = found.group("subject").lower().split()
    head = said[1] if len(said) > 1 else said[0]
    if head in GRIEVANCE_PEOPLE or head in trouble.OTHERS:
        return False
    if head in NOT_A_VERDICT_SUBJECT:
        return False
    return True


LOOKING_FORWARD = re.compile(
    r"\b(?:cant|cannot|can not|can't)\s+wait\b"
    r"|\b(?:really |so |properly |very )?(?:am |im |i'm )?looking forward to\b"
    r"|\broll on\b"
    r"|\bcount(?:ing)? down (?:the days )?(?:to|till|until|til)\b"
    r"|\b(?:only|just)\s+\d+\s+(?:days?|weeks?|sleeps?)\s+(?:to go|till|until|til)\b"
    r"|\bnot long (?:now )?(?:till|until|before)\b"
    r"|\b(?:excited|buzzing|chuffed) (?:about|for|to)\b", re.I)
A_CANT_WAIT = re.compile(r"\b(?:cant|cannot|can not|can't)\s+wait\b", re.I)
A_WAITING_IN = re.compile(r"\s+(?:in|around|about|at\s+home|indoors)\b", re.I)
A_WAITING_FOR_A_TURN_UP = re.compile(
    r"\s+(?:for|till|until|til|on)\s+(?:[\w']+\s+){0,4}?"
    r"(?:engineer|plumber|electrician|gas\s+man|boiler\s+man|repair\s+man|delivery|deliveries|"
    r"parcel|parcels|courier|post|postman|installer|technician|builder|roofer|scaffolder|council|"
    r"nurse|carer|vet|someone|anyone|somebody|it\s+to\s+(?:be\s+)?(?:fixed|repaired|arrive|come|"
    r"turn\s+up)|them\s+to\s+(?:come|arrive|turn\s+up))\b", re.I)
A_WORKING_DAY = re.compile(
    r"\b(?:have\s+to\s+be\s+(?:at|in)\s+work|have\s+to\s+work|ive\s+got\s+to\s+work|"
    r"im\s+at\s+work|i'm\s+at\s+work|i\s+work\b|im\s+working|i'm\s+working|on\s+shift|"
    r"working\s+days?|no\s+time\s+off|not\s+free|only\s+free|day\s+off)\b", re.I)


NOT_LOOKED_FORWARD_TO = re.compile(
    r"\b(?:to (?:end|finish|be over|be done with|stop)|over with|get (?:it|this) over)\b"
    r"|\b(?:to )?(?:get out|leave|quit|resign|escape|be done|go home)\b"
    r"|\b(?:not|never)\s+(?:really\s+|at all\s+)?looking forward to\b"
    r"|\bdread(?:ing)?\b|\bnot (?:to )?(?:the )?end\b"
    r"", re.I)


A_WAIT_FOR_A_LIFE_TO_END = re.compile(
    r"\b(?:to|till|until|til)\s+(?:i\s+)?(?:die|be dead|be gone|be with (?:him|her|them)|"
    r"not wake up|stop (?:hurting|being here)|be out of (?:this )?pain|be at peace)\b"
    r"|\b(?:die|dying|dead|death|suicide|kill myself|end it all|no reason to live)\b"
    r"|\bsee (?:my |our )?(?:mum|mom|mother|dad|father|son|daughter|wife|husband|gran|nan|"
    r"grandad|grandma|grandpa|brother|sister|baby|child) again\b", re.I)


DREADING = re.compile(
    r"\bdread(?:ing|s)?\b|\bnot (?:really |at all )?looking forward to\b"
    r"|\bcant face\b|\bcan't face\b|\bthe thought of\b[^.?!]{0,40}\bmakes me\b", re.I)
NOT_A_MILD_DREAD = re.compile(
    r"\bdread (?:to|what(?:ever)? it) (?:think|hear)\b|\bdread to think\b|"
    r"\b(?:suicide|kill myself|end my life|self[- ]harm|hit me|hurts? me|abuse[sd]?|"
    r"died|dying|death|funeral|cancer|hospital|diagnos\w*)\b", re.I)


def _dreading(clean):
    text = " ".join(str(clean or "").lower().split())
    if not text or "?" in text or len(text.split()) > 20:
        return False
    if not DREADING.search(text) or NOT_A_MILD_DREAD.search(text):
        return False
    return True


def _wants_it_over(clean):
    text = " ".join(str(clean or "").lower().split())
    if not text or "?" in text or A_WAIT_FOR_A_LIFE_TO_END.search(text):
        return False
    return bool(LOOKING_FORWARD.search(text) and NOT_LOOKED_FORWARD_TO.search(text))


DATE_AHEAD = re.compile(
    r"\b(?:tomorrow|tonight|next (?:week|month|year|weekend)|this (?:weekend|afternoon|evening)|"
    r"(?:on )?(?:mon|tues|wednes|thurs|fri|satur|sun)day|next (?:mon|tues|wednes|thurs|fri|satur|"
    r"sun)day|in (?:\d+|a few|a couple of|two|three|four) (?:days?|weeks?|months?)|"
    r"in the morning|the week after|not long now)\b", re.I)
DATE_AHEAD_OWN = re.compile(
    r"\b(?:my|our|im|i'm|i am|we are|we're|ive|i've|i have|i start|i go|i get|im off|i'm off)\b"
    r"|\bthe (?:wedding|holiday|trip|exam|interview|test|party|scan|operation|appointment|"
    r"viewing|hearing|move)\b", re.I)
AHEAD_NICE = re.compile(
    r"\b(?:holiday|holidays|trip|break|week off|visit|visiting|visitor|party|wedding|christening|"
    r"concert|gig|festival|night out|day out|meal|dinner|lunch|housewarming|camping|abroad|"
    r"flight|date|seeing|meeting up|reunion|graduation|barbecue|bbq|staying|going away|getaway|"
    r"off to|away for)\b", re.I)
AHEAD_TENSE = re.compile(
    r"\b(?:exam|exams|test|interview|scan|operation|surgery|appointment|hospital|dentist|doctor|"
    r"assessment|presentation|results|deadline|inspection|audit|court|hearing|tribunal|"
    r"check-?up|treatment|procedure|settlement|viewing|inspection|review|appraisal|"
    r"one-to-one|back to work|back at work|back to school|term starts|jab|jabs|vaccine|"
    r"vaccination|injection|booster|blood test)\b", re.I)
NOT_A_PLAN = re.compile(
    r"\b(?:died|dying|death|funeral|buried|cremation|hospice|terminal|cancer|chemotherapy|"
    r"hit me|hurt me|abuse[sd]?|miscarriage|stillborn|passed away|suicide|kill myself)\b", re.I)


def _a_day_ahead(clean):
    text = " ".join(str(clean or "").lower().split())
    if not text or "?" in text:
        return None
    if not DATE_AHEAD.search(text) or not DATE_AHEAD_OWN.search(text):
        return None
    if NOT_A_PLAN.search(text):
        return None
    if AHEAD_TENSE.search(text):
        return A_DAY_AHEAD_TENSE
    if AHEAD_NICE.search(text):
        return A_DAY_AHEAD
    return None


def _the_wait_is_for_someone_to_turn_up(text):
    hits = list(A_CANT_WAIT.finditer(text))
    if not hits:
        return False
    left = text
    for hit in hits:
        left = left[:hit.start()] + " " + left[hit.end():]
    if LOOKING_FORWARD.search(left):
        return False
    working = bool(A_WORKING_DAY.search(text))
    for hit in hits:
        after = text[hit.end():]
        if A_WAITING_IN.match(after):
            continue
        if working and A_WAITING_FOR_A_TURN_UP.search(after):
            continue
        return False
    return True


def _looking_forward(clean):
    text = " ".join(str(clean or "").lower().split())
    if not text or "?" in text:
        return False
    if not LOOKING_FORWARD.search(text) or A_WAIT_FOR_A_LIFE_TO_END.search(text):
        return False
    if _the_wait_is_for_someone_to_turn_up(text):
        return False
    return not NOT_LOOKED_FORWARD_TO.search(text)


def _a_good_time(clean, memory=None):
    if "?" in clean or " but " in clean or " until " in clean:
        return False
    if (GOOD_DAY_OURS.search(clean) or GOOD_DAY_WENT.search(clean)
            or GOOD_DAY_BARE.search(clean) or GOOD_TIME_IT.match(clean)):
        return True
    if _a_verdict(clean, memory):
        return True
    if (clean.split() or [""])[0] in QUESTION_OPENERS:
        return False
    if GOOD_TIME_OURS.search(clean):
        return True
    if not GOOD_TIME_SUBJECT.search(clean):
        return False
    return bool(set(re.findall(r"[a-z]+", clean)) & GOOD_TIME_WORDS)


A_FILM = re.compile(r"\b(?:film|films|movie|movies|cinema|netflix)\b", re.I)

HARM_IN_A_LAUGH = re.compile(
    r"\b(?:kill(?:ed|ing|s)? myself|end(?:ed|ing)? my life|want(?:ed|s|ing)? to die|"
    r"suicid\w*|self[- ]harm\w*|overdos\w*|took (?:some |a load of )?pills?)\b", re.I)

LAUGH_STOPPED = re.compile(
    r"\b(?:any ?more|any ?longer|these days|lately|never|hardly|used to|stopped|"
    r"in (?:weeks|months|years)|remember the last time)\b", re.I)

A_LAUGH_ITSELF = re.compile(
    r"\b(?:has|have|had|got)\s+(?:a|such a|the)\s+(?:very\s+|really\s+|proper\s+)?"
    r"(?:lovely|nice|great|good|infectious|loud|big|brilliant|wonderful|happy|silly)\s+laugh\b"
    r"|\bi\s+(?:love|like|adore|enjoy)\b[^.?!]{0,20}\b(?:a|good|a good|nothing better than a)"
    r"\s+laugh\b"
    r"|\bnothing (?:beats|better than) a good laugh\b", re.I)


A_ROOMS_LAUGH = re.compile(
    r"\b(?:everyone|everybody|they|all of them|the (?:others|rest|group|kids|class|crowd|family)|"
    r"my (?:mates|friends|sisters?|brothers?|mum|dad|husband|wife|partner|boyfriend|girlfriend|"
    r"boss|colleagues|coworkers|workmates|family))\b(?:\s+[\w']+){0,3}\s+"
    r"(?:laughed|laugh|laughing|giggled|giggling)\b", re.I)
A_OWN_LAUGH = re.compile(
    r"\b(?:i|we|me|us)\b(?:\s+[\w']+){0,2}\s+"
    r"(?:laughed|laugh|laughing|giggl(?:ed|ing)|in stitches|creased up)\b|"
    r"\b(?:made|makes|make|had) me laugh\b", re.I)


def _something_funny(clean, memory=None):
    if "?" in clean or " but " in clean:
        return False
    if LAUGHING_AT.search(clean):
        return False
    if A_FILM.search(clean):
        return False
    if HARM_IN_A_LAUGH.search(clean):
        return False
    if LAUGH_STOPPED.search(clean):
        return False
    if A_LAUGH_ITSELF.search(clean):
        return False
    if A_ROOMS_LAUGH.search(clean) and not A_OWN_LAUGH.search(clean):
        return False
    if isinstance(memory, dict) and _in_a_care_thread(memory):
        return False
    return bool(LAUGHING.search(clean))


STEPPED_AWAY = re.compile(
    r"\b(?:sorry|apologies)\b[^.?!]{0,30}\b(?:i went (?:to (?:get|grab|pick|fetch|answer|"
    r"check|put|sort|deal|make|do)\b|for\b|away\b|out\b|off\b)|i had to go\b|"
    r"to get (?:the|my|some)\b|to pick (?:up )?(?:the|my)\b|for a (?:min|minute|sec|second|"
    r"bit|moment)\b|i'?ve been away|i was gone)\b"
    r"|\b(?:sorry|apologies) (?:i|for) (?:disappeared|vanishing|going quiet|being away)\b"
    r"|\b(?:sorry|apologies)\b[^.?!]{0,40}\b(?:i was (?:away|asleep|out|busy|driving|"
    r"in a meeting|on a call|at (?:work|school|uni))|slow (?:reply|response)|late (?:reply|"
    r"response)|the delay)\b"
    r"|\b(?:sorry|apologies) (?:i|that i) (?:missed|didn'?t (?:see|get)) (?:your|that) "
    r"(?:message|reply|text)\b"
    r"|\b(?:sorry|apologies)\b[^.?!]{0,30}\b(?:for the wait|the wait|kept you waiting|"
    r"took (?:me )?(?:so|a while)|took so long|late replying)\b")


GOT_DRAWN_AWAY = re.compile(
    r"\b(?:got|get|was|been)\s+(?:a\s+(?:bit|little)\s+|a bit\s+|totally\s+|completely\s+)?"
    r"(?:distracted|waylaid|sidetracked|side-tracked|pulled\s+away|dragged\s+away|"
    r"called\s+away|taken\s+away)\b"
    r"(?:\s+(?:by|with)\s+(?:a|the|some|my|an)?\s*[a-z']{2,12})?"
    r"|\b(?:got|get|was|were|been)\s+(?:talking|chatting)\s+to"
    r"(?:\s+(?:a|the|some|my|his|her|our)\s+[a-z']{2,12})?"
    r"|\b(?:got|get)\s+caught\s+up\s+with(?:\s+(?:a|the|some|my|an)\s*[a-z']{2,12})?")


A_TURN_THE_PAGE = re.compile(
    r"\b(?:anyway|anyways|but|oh|also|by\s+the\s+way|while\s+i'?m\s+here|"
    r"quick\s+question|separate\s+thing|other\s+thing)\b")


A_GAP_FOR_ILLNESS = frozenset("""
    flu cold covid bug virus infection ill sick unwell poorly worse hospital operation surgery
    migraines migraine headache bereavement funeral grieving grief depressed depression anxiety
    burnout recovery recovering recovered injury injured broken sprained test scan results
    doctor doctors gp a&e sleep sleepless insomnia
""".split())
A_GAP_NAMED_PERSON = frozenset("""
    mum mom mother mum's dad father dad's sister brother gran grandad grandma grandpa nan nana
    son daughter wife husband partner boyfriend girlfriend fiance fiancee kids children child
    baby family friend mate aunt uncle cousin mother-in-law father-in-law in-laws
""".split())


def _the_gap_is_all_there_is(clean):
    text = " ".join(str(clean or "").lower().replace("\u2019", "'").split())
    if not text:
        return False
    errand = bool(STEPPED_AWAY.search(text))
    spare = 1 if errand else 0
    for pattern in (STEPPED_AWAY, ABSENCE, GOT_DRAWN_AWAY, _SORRY_LEAD):
        for _ in range(4):
            match = pattern.search(text)
            if not match or not match.group(0):
                break
            text = (text[:match.start()] + " " + text[match.end():]).strip()
    for match in A_TURN_THE_PAGE.finditer(text):
        if re.search(r"[a-z']", text[match.end():]):
            return False
    left = [word for word in re.findall(r"[a-z']+", text) if word not in A_PAUSE_WORD]
    rest = left[spare:]
    if not rest:
        return True
    if not any(word in A_HOW_THE_TIME_WENT or word in A_GAP_FOR_ILLNESS for word in rest):
        return False
    return len(left) <= spare + 6 and all(
        word in A_HOW_THE_TIME_WENT or word in A_GAP_FOR_ILLNESS
        or word in A_GAP_NAMED_PERSON
        for word in rest)


SPEAKER_ABSENCE = re.compile(
    r"\b(?:i|ive|i've|im)\b[^.?!]{0,24}?\b(?:been|be|went|gone|was)\s+"
    r"(?:quiet|silent|away|incommunicado|off\s+my\s+phone)\b")
AN_APOLOGY_IN_THE_LINE = re.compile(r"\b(?:sorry|apolog(?:y|ies)|apologise|apologize)\b")


def reads_as_pause(clean):
    text = " ".join(str(clean or "").lower().replace("\u2019", "'").split())
    if STEPPED_AWAY.search(text) or GOT_DRAWN_AWAY.search(text):
        return _the_gap_is_all_there_is(text)
    if AN_APOLOGY_IN_THE_LINE.search(text) and ABSENCE.search(text):
        return _the_gap_is_all_there_is(text)
    if SPEAKER_ABSENCE.search(text):
        return _the_gap_is_all_there_is(text)
    return False


def _came_back(clean):
    return reads_as_pause(clean)


POINTS_BACK = re.compile(
    r"(?:as|like)\s+i\s+(?:was|were)\s+saying"
    r"|back\s+to\s+what\s+i\s+was\s+saying"
    r"|as\s+i\s+said"
    r"|where\s+(?:was|were)\s+(?:i|we)"
    r"|(?:got|get|getting)\s+cut\s+off|cut\s+off\s+there"
    r"|(?:i\s+)?got\s+interrupted|was\s+interrupted"
    r"|carry\s+on"
    r"|back\s+again"
    r"|any\s?way|any\s?road")
A_POINTING_FILLER = frozenset("""
again ah already and any anyway anyroad as at back before but carry earlier er for from haha here
hmm i i'm im in in it just like me my now of off oh ok okay on right said saying so sorry that the
then there this to um up us was we well were with yeah yes you
""".split())
A_THING_MARKER = frozenset("about regarding".split())


def _a_chat_behind_it(memory):
    return history.an_earlier_turn(memory)


def nothing_said_yet(memory):
    return not history.an_earlier_turn(memory)


def nothing_yet_line():
    return RETURNED_TO_IT_FIRST[0] if RETURNED_TO_IT_FIRST else ""


def brings_nothing_of_its_own(text):
    return history.brings_nothing_of_its_own(text)


def assumes_an_earlier_turn(reply):
    return history.a_past_that_is_not_there(reply, {}, "")


def reads_as_a_return(clean):
    text = " ".join(str(clean or "").lower().replace("\u2019", "'").split())
    if not text or not POINTS_BACK.search(text):
        return None
    left = text
    for _ in range(3):
        match = POINTS_BACK.search(left)
        if not match or not match.group(0):
            break
        left = (left[:match.start()] + " " + left[match.end():]).strip()
    tokens = [word for word in (re.sub(r"[^a-z0-9']", "", word) for word in left.split()) if word]
    marker = next((i for i, word in enumerate(tokens) if word in A_THING_MARKER), None)
    if marker is None:
        return "" if all(word in A_POINTING_FILLER for word in tokens) else None
    if not all(word in A_POINTING_FILLER for word in tokens[:marker]):
        return None
    thing = " ".join(word for word in tokens[marker + 1:] if word).strip(" ,.-\u2026")
    if not thing or len(thing.split()) > 4:
        return None
    return thing


SORRY_ASKING = re.compile(
    r"\b(?:sorry|apolog(?:y|ies)|apologise|apologize)\b"
    r"[^.?!]{0,30}?"
    r"\b(?:bother\w*|pester\w*|nagging|ask\w*|questions?|pain|nuisance|hassle|trouble\w*|"
    r"keep\s+(?:asking|going|coming|picking|on)|one\s+more|another\s+one|essay|"
    r"ramble\w*|going\s+on|dumping|moan\w*|interrupt\w*|taking\s+up)\b")


def _only_manners(clean, allowed):
    words = re.findall(r"[a-z']+", clean.lower())
    return bool(words) and all(word in allowed for word in words)


def _sorry_for_asking(clean):
    text = clean.lower()
    return bool(SORRY_ASKING.search(text)) and _only_manners(text, MANNERS_ONLY)


AM_I_A_NUISANCE = re.compile(
    r"(?<![a-z])(?:am|are|is)\s+(?:i|we|this|it)(?![a-z])[^.?!]{0,25}?"
    r"(?<![a-z])(?:bother\w*|bugging|annoy\w*|irritat\w*|pester\w*|in the way|too much|"
    r"a waste of|taking (?:up )?(?:too much|your)|keeping you|too many questions|"
    r"asking a lot)(?![a-z])"
    r"|(?<![a-z])(?:do|would|will|did)\s+you\s+mind(?![a-z])[^.?!]{0,25}?"
    r"(?<![a-z])(?:me asking|my asking|if i ask|i ask)(?![a-z])"
    r"|(?<![a-z])(?:should|shall|do) i (?:stop|quit) asking(?![a-z])")
NUISANCE_ONLY = MANNERS_ONLY | frozenset("""
    am are is was were bugging bug annoy annoying annoyed irritating irritated irritate
    pester pestering way waste mind minding stop quit should shall if ask asking
    taking take up long much many too lot lots questions question time in way at all
    """.split())


def _am_i_a_nuisance(clean):
    text = " ".join(str(clean or "").lower().split())
    return bool(AM_I_A_NUISANCE.search(text)) and _only_manners(text, NUISANCE_ONLY)


THANKS_OPENS = re.compile(
    r"^(?:(?:ok|okay|ah|oh|right|great|brilliant|nice|lovely|perfect)\b[\s,!.]*)?"
    r"(?:thanks|thank\s+you|thankyou|thank-you|cheers|ta)\b[\s,!.]*(?P<said>.*)$")
THANKS_WENT_BADLY = re.compile(
    r"\b(?:worse|worst|no\s+better|not\s+better|no\s+change|still|came\s+back|back\s+again|"
    r"hurts?|hurting|sorer?|failed|nothing|didnt|didn't|doesnt|doesn't|wont|won't|"
    r"can'?t|cant|hasnt|hasn't|"
    r"(?:is|are|was|were|has|have|had|its|it's|im|i'm|they're|theyre)\s+back|"
    r"(?:come|comes|coming|came)\s+back|flares?|flared|flaring|\breturned|returning|"
    r"back\s+to\s+square\s+one)\b")
THANKS_GOOD_AGAIN = re.compile(
    r"\bback\s+to\s+(?:normal|how\s+it\s+was|where\s+it\s+was|itself|its\s+old\s+self|"
    r"being\s+normal)\b|"
    r"\bstill\s+(?:keeping\s+|doing\s+|going\s+)?(?:good|well|fine|great|ok|okay|improving|"
    r"getting\s+better|on\s+the\s+mend|strong)\b|"
    r"\bstill\s+(?:a\s+)?bit\s+(?:sore|stiff|tired)\s+but\b")
THANKS_NO_BETTER = (
    "Sorry it hasn't settled. What's it doing now?",
    "Sorry to hear that — thanks for coming back with it.",
    "That's a nuisance. What's the worst of it now?",
    "Sorry it's no better yet. Say what's changed and I'll go again.",
    "Right, still not right. What's it doing now?",
)
THANKS_TAKES_A_QUESTION = re.compile(
    r"\b(?:can|could|would|should|will|shall|any\s+idea|what|how|why|when|where|who|"
    r"is\s+it|do\s+i|should\s+i)\b")


def _thanks_then_said(clean):
    match = THANKS_OPENS.match(clean.strip().rstrip(".!").strip())
    if not match:
        return ""
    said = match.group("said").strip(" .,!;:")
    if len(re.findall(r"[a-z']+", said)) < 2:
        return ""
    if THANKS_TAKES_A_QUESTION.search(THANKS_GOOD_AGAIN.sub(" ", said)):
        return ""
    return said


def _thanks_news_went_badly(clean):
    said = _thanks_then_said(clean)
    if not said or THANKS_GOOD_AGAIN.search(said):
        return ""
    if THANKS_WENT_BADLY.search(said):
        return said
    words = re.findall(r"[a-z']+", said)
    return said if _mood(words, said) == "negative" else ""


_ACKNOWLEDGES_ALONE = re.compile(
    r"^(?:(?:oh|ok|okay|right|well|ah|aye|yes|yeah|great|good|nice|cool|brilliant|lovely|"
    r"perfect|interesting|thats|that's|that|it's|its|thanks|thank\s+you|cheers|ta|"
    r"ill|i'll|i|will|do)[\s,]+)*"
    r"(?:(?:good|great|useful|handy|nice|lovely|brilliant|perfect|helpful|interesting|"
    r"reassuring|worth)\s+)?(?:to\s+know|knowing|to\s+hear|to\s+see)\b"
    r"(?:[\s,]+(?:that|it|this|then|so|now|thanks|thank\s+you|cheers|ta|mate|for\s+that))*"
    r"[\s.!]*$")


def _acknowledges_alone(clean):
    return bool(_ACKNOWLEDGES_ALONE.match(" ".join(str(clean or "").lower().split())))


def _thanks_with_more(clean):
    text = clean.lower()
    if "?" in text:
        return False
    words = set(re.findall(r"[a-z']+", text))
    if not (words & THANK_WORDS):
        return False
    return _only_manners(text, THANKS_ONLY)


def reading(text, memory):
    try:
        continuation = careful(text, memory)
    except Exception:
        continuation = None
    if continuation:
        return (CARE_THREAD if _a_care_thread(memory) else THREAD), (continuation,)
    try:
        if leaving.reads_as_leaving(" ".join(str(text or "").lower().split())):
            return leaving.LEAVING, ()
    except Exception:
        return "", ()
    try:
        if (not _grief_thread(memory) and not in_a_safety_thread(memory)
                and reads_as_pause(" ".join(str(text or "").lower().split()))):
            return PAUSE, ()
        if (not _grief_thread(memory) and not in_a_safety_thread(memory)
                and _a_chat_behind_it(memory)
                and reads_as_a_return(text) is not None):
            return PAUSE, ()
    except Exception:
        return "", ()
    return "", ()


def _advice_thread_is_about_the_body(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)][-6:]
    for turn in reversed(turns):
        line = str(turn.get("user") or "").lower()
        if line and _worry_is_about_the_body(line, line.split()):
            return True
    return False


def _a_step_word_in(words, steps):
    for word in words:
        if str(word).replace("'", "").strip(".,!?;:-\u2014") in steps:
            return True
    return False


def _a_report_on_the_advice(clean, words, about_the_body=True, the_lot_ok=False, steps=NO_STEP):
    if "?" in clean or len(words) > 14:
        return None
    if {str(word).strip(".,!?;:-\u2014'") for word in words} & THANKS_WORDS:
        return None
    for word in words:
        bare = str(word).replace("'", "").strip(".,!?;:-\u2014")
        if bare in REPORT_FILLER or bare in steps or bare in REPORT_VERDICT_WORD:
            continue
        return None
    pools = ((TRIED_NO_CHANGE, TRIED_NO_CHANGE_REPLIES, TRIED_NO_CHANGE_ELSEWHERE),
             (TRIED_WORSE, TRIED_WORSE_REPLIES, TRIED_WORSE_ELSEWHERE),
             (REPORT_NOW_FINE, TRIED_SORTED_REPLIES, TRIED_SORTED_REPLIES),
             (TRIED_HELPED, TRIED_HELPED_REPLIES, TRIED_HELPED_ELSEWHERE),
             (STILL_THE_TROUBLE, TRIED_NO_CHANGE_REPLIES, TRIED_NO_CHANGE_ELSEWHERE),
             (TRIED_IT, TRIED_IT_REPLIES, TRIED_IT_REPLIES),
             (TRIED_THAT_ONLY, TRIED_IT_REPLIES, TRIED_IT_REPLIES),
             (DONE_IT, TRIED_IT_REPLIES, TRIED_IT_REPLIES))
    if the_lot_ok:
        pools = pools + ((TRIED_THE_LOT, TRIED_NO_CHANGE_REPLIES, TRIED_NO_CHANGE_ELSEWHERE),)
    for shape, on_the_body, elsewhere in pools:
        if shape is STILL_THE_TROUBLE and not _a_step_word_in(words, steps):
            continue
        if shape.search(clean):
            return on_the_body if about_the_body else elsewhere
    return None


def _the_outcome_of_the_advice(memory, clean, words):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    last = str(turns[-1].get("bot") or "") if turns else ""
    seen = [str(turn.get("bot") or "") for turn in turns[-ADVICE_TURNS:]]
    if not any(_advice_in(line) for line in seen):
        return None
    if _in_a_loss_thread(memory) or _grief_thread(memory):
        return None
    if len(last) < ADVICE_LENGTH and not ADVICE_CUE.search(last.lower()):
        earlier = any(_advice_in(line) for line in seen[:-1])
        if not earlier and (len(words) > 6 or len(last) < ADVICE_LENGTH_BARE):
            return None
    return _a_report_on_the_advice(clean, words, _advice_thread_is_about_the_body(memory),
                                   the_lot_ok=not reject.offers_a_choice(memory),
                                   steps=_the_words_in(the_advice(memory)))


def the_advice(memory):
    for turn in reversed([t for t in (memory.get("turns") or []) if isinstance(t, dict)]
                         [-ADVICE_TURNS:]):
        reply = str(turn.get("bot") or "").lower()
        if _advice_in(reply):
            return reply
    return ""


def reads_as_a_report(text, memory):
    clean = " ".join(str(text or "").lower().split())
    try:
        return bool(_the_outcome_of_the_advice(memory, clean, clean.split()))
    except Exception:
        return False


def the_report_reply(text, memory):
    clean = " ".join(str(text or "").lower().split())
    try:
        return _after_advice(memory, clean, clean.split())
    except Exception:
        return None


def a_report_that_says_something(text, memory):
    reply = the_report_reply(text, memory)
    return bool(reply) and reply not in TRIED_IT_REPLIES


def _after_advice(memory, clean, words):
    step = _the_next_move_after_the_advice(memory, clean, words)
    if step:
        return step
    pool = _the_outcome_of_the_advice(memory, clean, words)
    if not pool:
        return None
    return _choose(pool, memory, clean, seed_text=the_advice(memory) or clean)


def _the_answer_above_already_says_what_to_do(turns, memory):
    if not turns:
        return False
    if not (memory.get("entry_answer") or memory.get("entry_answers")):
        return False
    return bool(AN_ANSWER_ABOUT_A_NO.search(str(turns[-1].get("bot") or "")))


def _a_thread_about_how_somebody_treats_them(turns):
    for turn in turns[-4:]:
        said = set(re.findall(r"[a-z']+", str(turn.get("user") or "").lower()))
        if TREATMENT_HARM & said:
            return True
    return False


def _an_answer_above(turns):
    bot = str((turns[-1].get("bot") if turns else "") or "")
    return len(bot.split()) >= 8


def _a_refusal_to_answer(clean, memory, words=None):
    if "?" in str(clean or ""):
        return None
    if not REFUSED.search(clean):
        return None
    if OWN_NO.search(clean) or ASKS_WHY.search(clean):
        return None
    matched = REFUSED.search(clean)
    if matched and HYPOTHETICAL.search(str(clean or "")[:matched.start()]):
        return None
    words = clean.split() if words is None else words
    if len(words) > 15:
        return None
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    if not REFUSED_PARTY.search(clean) and not _an_answer_above(turns):
        return None
    if REFUSED_NOT.search(clean) or REFUSED_FAMILY.search(clean):
        return None
    if REFUSED_NO_OBJECT.search(clean):
        return None
    if _the_answer_above_already_says_what_to_do(turns, memory):
        return None
    if _a_thread_about_how_somebody_treats_them(turns):
        return None
    try:
        if trouble.reads_as_trouble(clean):
            return None
        if _in_a_loss_thread(memory) or _grief_thread(memory) or in_a_safety_thread(memory):
            return None
    except Exception:
        return None
    if turns and _in_a_pool(str(turns[-1].get("bot") or ""), (REFUSED_REPLIES,)):
        return None
    return REFUSED_REPLIES


def reads_as_a_refusal(text, memory):
    clean = " ".join(str(text or "").lower().split())
    try:
        return bool(_a_refusal_to_answer(clean, memory, clean.split()))
    except Exception:
        return False


def _the_next_move_after_the_advice(memory, clean, words):
    pool = _a_report_on_the_advice(clean, words, _advice_thread_is_about_the_body(memory),
                                   the_lot_ok=not reject.offers_a_choice(memory),
                                   steps=_the_words_in(the_advice(memory)))
    if pool not in (TRIED_NO_CHANGE, TRIED_NO_CHANGE_ELSEWHERE):
        return None
    if _in_a_loss_thread(memory) or _grief_thread(memory):
        return None
    try:
        return repeat.the_next_move(memory, clean) or None
    except Exception:
        return None


def _a_care_thread(memory):
    answer = _thread_answer(memory)
    if not answer:
        return False
    return not any(word in answer for word in CRISIS_WORDS)


def in_a_safety_thread(memory):
    return bool(_thread_answer(memory))


def _thread_answer(memory):
    window = [t for t in (memory.get("turns") or []) if isinstance(t, dict)][-THREAD_TURNS:]
    answer = ""
    for index in range(len(window) - 1, -1, -1):
        if window[index].get("module") == "safety":
            answer = str(window[index].get("bot") or "").lower()
            window = window[index + 1:]
            break
        if window[index].get("module") == FALLBACK_MODULE:
            continue
    if not answer:
        return ""
    for turn in window:
        if turn.get("module") == FALLBACK_MODULE:
            continue
        if _words_kept(turn.get("bot"), answer) >= THE_THREAD_KEPT:
            continue
        return ""
    return answer



OWN_THING = re.compile(r"\b(?:my|our|his|her|their)\s+(\w+)")
CLAUSE_END = re.compile(r"[;,.?!]|\b(?:and|but|then|so|because|while|which|who)\b")
AFTER_THING = re.compile(r"\s+(?:out\s+of|out|off|from|in|into|on|onto|over|under|"
                         r"with|about)\s+(?:(?:a|an|the|some|another)\s+)?(\w+)")
ASK_WORD = re.compile(r"\b(?:can|could|should|shall|do|does|did|is|are|will|would|may|"
                      r"might|what|whats|how|hows|when|where|why|which|am|ok|okay)\b")


def asks_about_the_last_answer(line, last, own=()):
    if not line or not last:
        return False
    text = str(line).lower()
    if "?" not in text and not ASK_WORD.search(text):
        return False
    if len(set(own)) > 1:
        return False
    named = set(OWN_THING.findall(text))
    for word in _words(text):
        if len(word) < 5 or word in PLAIN_WORDS:
            continue
        if word not in last:
            continue
        if named and word not in named:
            return False
        for said in re.finditer(r"\b" + re.escape(word) + r"\b", text):
            clause = CLAUSE_END.split(text[said.end():], 1)[0]
            brought_in = AFTER_THING.search(clause)
            if not brought_in:
                continue
            thing = brought_in.group(1)
            if len(thing) >= 4 and thing not in PLAIN_WORDS and thing not in last:
                return False
        return True
    return False


def asks_about_a_care_answer(line, last, memory, own=()):
    if asks_about_the_last_answer(line, last, own):
        return True
    answer = _thread_answer(memory or {})
    if not answer or answer == str(last or "").lower():
        return False
    return asks_about_the_last_answer(line, answer, own)


def how_much_of_the_answer_kept(reply, memory):
    answer = _thread_answer(memory or {})
    if not answer:
        return 0
    return _words_kept(reply, answer)


def _words_kept(reply, answer):
    said = set(_words(str(answer or "").lower()))
    return len({word for word in _words(str(reply or "").lower())
                if len(word) >= 5 and word in said})


THE_THREAD_KEPT = 3


def careful(text, memory):
    understood = memory.get("understood")
    clean = " ".join(str(text or "").lower().split())
    return _after_safety(memory, clean, understood if isinstance(understood, dict) else None)


def _in_a_loss_thread(memory):
    for turn in [t for t in (memory.get("turns") or []) if isinstance(t, dict)][-4:]:
        said = str(turn.get("user") or "").strip()
        if said and loss.reads_as_loss(said.lower()):
            return True
    return False


LOSS_IN_TURN_CLEAR = re.compile(
    r"\b(?:funeral|buried|burial|cremat\w*|grief|grieving|bereave\w*|widow\w*|condolence\w*|"
    r"sorry for your loss|passed away)\b")
LOSS_IN_TURN_ANYBODY = re.compile(r"\b(?:died|dying|death|deaths|dead|lost (?:my|her|his|our))\b")
LOSS_A_THING = re.compile(
    r"\b(?:laptop|phone|mobile|engine|battery|car|van|plant|plants|machine|washing machine|"
    r"tv|telly|fridge|freezer|boiler|dishwasher|dryer|oven|router|computer|pc|printer|hoover|"
    r"vacuum|watch|clock|bike|mower|heating|bulb|lights?|screen|console|kettle|toaster|"
    r"microwave|cooker|radiator|immersion|shower|pump|drone|drones|lawnmower|lawn mower|moped|"
    r"scooter|motorbike|tablet|ipad|wifi|wi-fi|internet|broadband|signal|connection|speaker|"
    r"headphones|earbuds|camera|torch|iron|drill|radio|music|party|battery|charger|"
    r"satnav|gps|tumble dryer|hot water|plug|fuse|switch)\b")
LOSS_IT_DIED = re.compile(r"\bit(?:'s| is| has| had)?\s+(?:just\s+)?(?:died|dead|dying|gone)\b")
LOSS_A_LOST_THING = re.compile(
    r"\blost (?:my|our|his|her|their|the) (?:job|jobs|work|shift|hours|keys|key|wallet|purse|"
    r"passport|ticket|tickets|money|savings|deposit|house|home|flat|bag|card|cards|licence|"
    r"license|id|fob|bus pass|phone|mobile)\b")
LOSS_SOMEBODY = re.compile(
    r"\b(?:mum|mom|mam|mother|dad|father|nan|nana|gran|granny|grandma|grandad|grandpa|"
    r"grandmother|grandfather|sister|brother|wife|husband|partner|son|daughter|baby|child|"
    r"children|uncle|aunt|auntie|cousin|friend|mate|neighbour|neighbor|fiance\w*|boyfriend|"
    r"girlfriend|he|she|him|her|his|hers|they|them|person|people|someone|somebody|man|woman|"
    r"lady|lad|boy|girl|pet|dog|cat|puppy|kitten)\b")


def _a_loss_in(text):
    text = (text or "").lower()
    if LOSS_IN_TURN_CLEAR.search(text):
        return True
    if not LOSS_IN_TURN_ANYBODY.search(text):
        return False
    if LOSS_A_LOST_THING.search(text):
        return False
    if LOSS_SOMEBODY.search(text):
        return True
    if LOSS_IT_DIED.search(text) or LOSS_A_THING.search(text):
        return False
    return True


DEAD_AND_NOTHING_ELSE = re.compile(r"\bdead\b")
DIED_OR_DEATH = re.compile(r"\b(?:died|dying|dies|death|deaths|lost (?:my|her|his|our))\b")


def _dead_is_the_only_death_word(said):
    return bool(DEAD_AND_NOTHING_ELSE.search(said)) and not DIED_OR_DEATH.search(said)


LOSS_OWN_WORDS = tuple(loss.LOSS_REPLIES) + tuple(loss.AFTER_REPLIES)


def _we_condoled(line):
    line = (line or "").strip()
    return bool(line) and any(line.startswith(reply[:30]) for reply in LOSS_OWN_WORDS)

def _a_thing_stopped(clean):
    return bool(LOSS_IN_TURN_ANYBODY.search(clean or "")) and not _a_loss_in(clean)


def _last_turn(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    return turns[-1] if turns else {}


def _the_last_line_was_bad_news(memory):
    said = str((_last_turn(memory) or {}).get("user") or "")
    return bool(said) and reads_as_bad_news(said.lower())


def _the_last_line_was_a_fault(memory):
    said = str((_last_turn(memory) or {}).get("user") or "")
    if not said:
        return False
    clean = said.lower()
    if reads_like_a_symptom(clean):
        return True
    return bool(trouble.reads_as_trouble(clean) or _a_thing_stopped(clean))


def _a_loss_recently(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    if not turns:
        return False
    last = turns[-1]
    said = str(last.get("user") or "").strip().lower()
    if said and (not _dead_is_the_only_death_word(said) or loss.reads_as_loss(said)):
        if _a_loss_in(said):
            return True
    ours = str(last.get("bot") or "")
    if _we_condoled(ours):
        return True
    both = " ".join(str(last.get(k) or "") for k in ("user", "bot")).lower()
    return bool(LOSS_IN_TURN_CLEAR.search(both))


def _the_last_line_was_heavy(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    if not turns:
        return False
    last = turns[-1]
    said = str(last.get("user") or "").strip()
    if said:
        words = _words(said.lower())
        if words and _mood(words, said.lower()) == "negative":
            return True
    return bool(OUR_HEAVY_TELL.search(str(last.get("bot") or "").lower()))


def _in_sudden_loss_thread(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    if not turns:
        return False
    last = str(turns[-1].get("bot") or "")
    return bool(last) and any(last in pool for pool in
                              (SUDDEN_LOSS, PREGNANCY_BLEEDING, THE_FIRST_HOUR_AND_A_CHILD))


def _reads_as_illness(clean):
    words = [w.strip(".,!?;:'\"") for w in clean.split()]
    for n, word in enumerate(words):
        if word.strip(".,!?;:'\"") != "ill":
            continue
        before = words[n - 1] if n else ""
        if before in ILL_SAID_OF_A_BODY:
            return True
        if n + 1 < len(words) and words[n + 1].strip(".,!?;:'\"") in ILL_WILL_VERBS:
            continue
        if n and before in ILL_BEFORE:
            return True
        if n == len(words) - 1 or words[n + 1] in ILL_AFTER:
            return True
    return False


AIM_BEFORE = re.compile(
    r"(?:\b(?:want|wants|wanting|trying|try|need|needs|plan|planning|hoping|hope|help|helps"
    r"|starting|started)\s+(?:to\s+|me\s+to\s+)?"
    r"|\b(?:how\s+do\s+i|how\s+can\s+i|how\s+to|best\s+way\s+to|ways\s+to|tips\s+to"
    r"|tips\s+for|any\s+advice\s+on)\s+)$"
)


def _in_an_aim(clean, word):
    if " but " in clean or " though " in clean or " although " in clean:
        return False
    hits = list(re.finditer(r"\b%s\b" % re.escape(word), clean))
    if not hits:
        return False
    for match in hits:
        before = clean[:match.start()]
        if not AIM_BEFORE.search(before):
            return False
        if {w.strip(".,!?") for w in before.split()[-3:]} & AIM_NEGATORS:
            return False
        after = match.end()
        if {w.strip(".,!?") for w in clean[after:].split()} & AIM_FAILING:
            return False
    return True


def _a_mood_word(words, word):
    for index, said in enumerate(words):
        if said != word:
            continue
        before = words[index - 1] if index else ""
        after = words[index + 1] if index + 1 < len(words) else ""
        if before in COPULA:
            subject = words[:index - 1]
            last = subject[-1] if subject else ""
            if (last in ABOUT_THEM_BEFORE_COPULA or set(subject) & STRETCH_OF_TIME
                    or not subject or (len(subject) == 1 and last in ("it", "this", "today"))):
                return True
            continue
        if before in MOOD_BEFORE or after in MOOD_AFTER:
            return True
    return False


RUMINATION = re.compile(
    r"\b(?:keep|keeps|kept|can'?t|cant|cannot|stop|stopped)\s+(?:thinking|replaying|reliving|"
    r"dwelling|worrying)\b"
    r"|\b(?:go|going|think|thinking)\s+(?:over|through|round|around)\s+(?:it|that|this|him|her|"
    r"them|what)\b"
    r"|\b(?:on my mind|in my head|over and over|again and again|round in circles|on repeat|"
    r"switch off|can'?t shake|can not shake)\b")
WITH_A_SUBJECT = re.compile(
    r"\b(?:my|our|his|her|their|the)\s+(?:\w+\s+)?(?:mortgage|loan|debt|rent|money|budget|"
    r"bills?|job|boss|car|boiler|washing machine|fridge|damp|landlord|surgery|doctor|gp|"
    r"appointment|wedding|interview|cv|exam|test|results?|numbers|figures|son|daughter|kids?|"
    r"child|baby|mum|mom|dad|husband|wife|partner|dog|cat|puppy|kitten)\b")


A_WANT = re.compile(
    r"\b(?:want|wants|wanted|wanting|wanna|hope|hopes|hoping|hoped|plan|plans|planning|planned"
    r"|saving up|saving for|dreaming of|thinking of|looking forward to|working towards?)\b"
    r"|\b(?:thinking|thought|dreaming|dreamt|going|go)\s+(?:(?:about|of|over)\s+)?"
    r"(?:getting|buying|booking|adopting|starting|trying|learning|making|building|moving)\b"
    r"|\b(?:thinking|thought|dreaming|dreamt)\s+(?:about|of)\s+(?:a|an|some|another)\s+\w+")


def _is_rumination(clean):
    if WITH_A_SUBJECT.search(clean) or A_WANT.search(clean):
        return False
    return bool(RUMINATION.search(clean))


BODY_PART = re.compile(
    r"\b(?:my|our)\s+(?:nose|ears?|face|cheeks?|skin|hands?|lips?|forehead|arms?|back)\s+"
    r"(?:are|r|is|feels?|looks?|go|goes)\s+(?P<rest>.+)$")


def _opens_a_question(words):
    if words[0] not in QUESTION_OPENERS:
        return False
    if words[0] != "am":
        return True
    return len(words) > 1 and words[1] in _SUBJECT_AFTER_AM


from .fallback_chain import (
    ACTS_AN_ERRAND, ACTS_AN_ERRAND_LINES, ACTS_IN_A_DIARY, ACTS_IN_A_DIARY_LINES,
    ACTS_ON_A_PHONE, ACTS_ON_A_PHONE_LINES, ACT_CHOICE, ACT_FOR_ME,
    ACT_OPENER, ACT_OWN_STEP, ACT_REPORT_TAIL, ACT_SETTING,
    ACT_THING, ADDRESSED, AN_ATTEMPT_AT_SOMEONE, ASK_SHAPE,
    AT_THE_CLOCK, A_BAD_THING_NAMED, A_BARE_MODIFIER, A_CHILDHOOD_MEMORY,
    A_CLOCK, A_CROWD, A_CROWD_AHEAD, A_DAY_SUBJECT,
    A_DAY_WENT_WRONG, A_HAND_OUT, A_LENGTH, A_LIST_ON_THE_TABLE,
    A_MILESTONE, A_MISTAKE, A_MOOD, A_REGRET_DOING,
    A_SYMPTOM_PHRASE, A_TIME_SAID, A_VISIT, BAD_DAY_ANYWAY,
    BOOKING_THING, CAN_DO_ITSELF, CLOCK_ABOUT_THE_JOB, CLOCK_ASKED,
    CLOCK_NOT_THIS, CLOCK_SHAPE, CLOCK_SOMEONE_ELSE, CLOCK_THE_DEPARTURE,
    CROWD_ORDER, DAY_PAST, FOOD_TOPICS, FRAME_PREFIX,
    HABIT_MIND_IT, HABIT_NOT, HABIT_STATED, HANDS_IT_OVER_HERE,
    HURT_BUT_FINE, HURT_DEATH, HURT_FIGURE, HURT_ON_THE_SPEAKER,
    HURT_SOMEBODY, LOW_DAY, LOW_DAY_MINE, LOW_DAY_NOT_MINE,
    NOT_ABOUT_THEM, NOT_A_CROWD_AHEAD, NOT_A_DAY_DONE, NOT_A_DAY_SAID,
    NOT_A_JOB_BUT_A_PERSON, NOT_A_REGRET, NOT_A_THING_TO_GET, OPTION_ON_THE_TABLE,
    OWN_THING, PAST_DOING, POLITE_ASK, REMIND_ME,
    SNAPPED_A_PHOTO, SOMEONE_ELSE_NAMED, TAKES_AS_IT_COMES, THEIR_OWN_DOING,
    THE_JOB_NAMED, _AN_ASKING, _AN_ATTEMPT_COUNT, _A_BODY_UNWELL,
    _A_CORRECTION, _A_DETAIL_OPENING, _A_NEGATIVE_AUXILIARY, _A_SYMPATHY,
    _ROUTINE_NOT_SHAPE, _UNDERTAKING, _a_birthday_still_to_come, _a_claim_about_a_thing,
    _a_care_home_line, _a_day_of_someone_else, _a_day_told_instead_of_the_receipt,
    _a_detail_about_what_was_said, _a_dish_name, _a_thing_got_ahead,
    _a_lateness_report, _a_low_day, _a_part_is_cold, _a_report_with_no_pronoun,
    _a_small_day, _a_state_in_the_past, _a_thing_happened, _a_thing_they_regret,
    _a_things_state, _act_asked_of_me, _acts_for_me, _answers_the_correction,
    _asks_the_bot, _body_state, _choose, _cue_negated,
    _flat_habit_stated, _habit_is_a_problem, _just_asked_about_the_day, _loves_people,
    _loves_someone, _mixed_seed,
    _mood, _options_already_up, _reads, _reads_as_a_bad_stretch,
    _reads_value, _repaired_of, _reply_for, _restated, _routine_pool,
    _somebody_elses_day_in_thread, _somebody_hurt, _state_from, _the_birthday_said_back,
    _the_clock_pool, _the_crowd_is_ahead, _the_morning_has_a_clock, _the_person_named_a_list,
    _the_state, _the_store_has_the_recall, _the_time_said, _the_win_is_someone_elses,
    _words, reads_as_a_flat_habit, reply_for, takes_as_it_comes,
    _a_part_in_a_state,
)

REPORT_REPLY_LINES = frozenset(
    tuple(TRIED_WORSE_REPLIES) + tuple(TRIED_NO_CHANGE_REPLIES) + tuple(TRIED_NO_CHANGE_ELSEWHERE)
    + tuple(TRIED_HELPED_REPLIES) + tuple(TRIED_HELPED_ELSEWHERE) + tuple(TRIED_IT_REPLIES)
    + tuple(TRIED_SORTED_REPLIES)
)


def is_a_report_reply(said):
    line = " ".join(str(said or "").lower().replace("\u2019", "'").split())
    return bool(line) and line in _REPORT_LINES_FLAT


def _flat_pools():
    return frozenset(" ".join(str(line).lower().replace("\u2019", "'").split())
                     for line in REPORT_REPLY_LINES)


_REPORT_LINES_FLAT = _flat_pools()
from .fallback_chain import (
    A_DAY_SAID_BADLY, A_NAME_A_HOUSEHOLD_TAKES, A_NAME_IS_NOT_A_DAY, A_NAMES_TOLD,
    A_POSSESSIVE_OF_MINE, NOT_A_NAME_WORD, NAMED_AFTER,
    BARE_STATE, BOT_WAS_SORRY, PLAN_THAT_FELL_THROUGH, RESULT_WENT_WRONG, STATE_IN_THE_PAST,
    STATE_NOT_A_DOING, STATE_THEN,
    _a_bad_time_told, _a_day_asked_without_a_cheer, _a_day_said_badly, _a_detail_of_a_bad_day,
    _a_name_told, _a_name_told_reply, _a_small_day_shape, _a_state_of_theirs,
    _named_after_reply, _the_day_was_already_bad, _the_last_exchange,
)
from .fallback_data import (
    A_BAD_TIME_TOLD, A_DAY_ASKED_PLAIN, A_NAME_STORY, A_NAME_TOLD, A_NAMED_AFTER,
    A_NAMED_AFTER_THEM, A_PLAN_THAT_FELL_THROUGH, A_STATE_NOW, A_STATE_PAST,
    A_THING_CAME_OUT_WRONG,
    RETURNED_TO_IT_FIRST,
)
