
import random
import re
import string
from ..memory import ack, facts, history, last_bot, last_user, obstacle, reject, repeat, swap
from ..memory import stuck as stuck_line
from ..understanding import understand
from ..understanding import kinds as understanding_kinds
from ..understanding.body import GOING_BOTH_WAYS
from ..understanding.kinds import (ANSWERING_A_QUOTED_ASK, greeting_only,
                                  the_manners_question, two_ends_of_one_scale,
                                  verdicts_a_thing)
from ..understanding.topics import IDIOM_PHRASES, THE_PEOPLE, is_a_machine_word
from . import (A_STEP_ASK, DOUBT, DOUBTED, LINGERED_LINE, NEARLY, says_it_has_lingered,
               step_when_low, turned, turns_round)
from .limit import NO_LAUGH_OR_SCARES, NOTHING_THAT_LIMITS, a_limit_on_the_answer
from . import (badnews, circumstance, draft, finding_out, goodnews, handoff, harm, leaving, loss,
               morning_after, no_eyes, onething, pick, prices, quantity,
               reaction as answer_reaction, remark, safetyask, trouble, unseen, why, worn)
from .postcode import a_postcode_lookup
from .urgent import reads_as_a_story
from .badnews import (reads_as_a_closed_door, reads_as_an_award_lost, reads_as_bad_news,
                      reads_as_heavy_news, reads_as_news_with_a_name,
                      reads_as_pregnancy_bleeding, reads_as_the_leaving,
                      reads_as_a_leaving_already_gone, reads_as_a_pet_condition,
                      reads_as_the_speakers_own_plan,
                      reads_as_sudden_loss,
                      reads_as_a_carer_body, reads_for_a_carer, reads_for_a_pet,
                      reads_as_a_pet_low, reads_like_a_symptom)
from .goodnews import (reads_as_an_occasion, reads_as_a_win_nobody_noticed,
                      reads_as_a_win_a_cost_came_with,
                       reads_as_a_clear_result, reads_as_good_news, reads_as_news_to_come,
                       reads_as_recovery,
                       reads_as_settled, worry_on_the_table)
from .fallback_data import (
    A_CARE_HOME,
    A_CARE_HOME_BRING,
    A_CARE_HOME_GUILT,
    A_CARE_HOME_MOVED,
    A_CARE_HOME_VISITING,
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
    ASKED_IF_I_SAW_LINES,
    ASKING_WORDS,
    ASK_ONLY,
    ASK_OUT_ANSWER,
    AT_IT_EXTRA,
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
    A_NEWS_OF_SOMETHING_ELSE,
    A_NEWS_OF_WEATHER,
    A_PAUSE_WORD,
    A_PERSON,
    A_PLACE_I_DONT_KNOW,
    A_REST_OF_A_GOOD_DAY,
    A_REST_OF_A_HARD_DAY,
    A_SMALL_DAY,
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
    A_BETRAYAL,
    A_WANT_IT_OVER,
    BABY_FOOD_NAMES,
    BABY_WHO,
    BAD_STRETCH,
    BAD_STRETCH_REPLIES,
    BARE_FOLLOW_UP_CARE_REPLIES,
    BARE_FOLLOW_UP_REPLIES,
    BARE_PICK_AFTER_NEWS,
    BARE_PICK_BRING,
    BARE_PICK_DO,
    BARE_PICK_GET,
    BARE_PICK_KIND,
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
    FORECAST_HE_SHE,
    FORECAST_ILL,
    FORECAST_OFF_THEIR_FOOD,
    FORECAST_PERMISSION,
    FORECAST_PERSON,
    FORECAST_PET,
    FORECAST_PET_HARM,
    FORECAST_POOLS,
    FORECAST_RELATION,
    FORECAST_SELF,
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
    MY_RECORDS,
    MY_WORKINGS,
    NAMED_NEGATIVE,
    NAMED_TYPES,
    NARROW_ANSWERED,
    NARROW_SUBSTANCE,
    NARROW_WORDS,
    NEGATIVE,
    NEGATIVE_CUES,
    NEGATORS,
    NOTHING_AT_ALL,
    CONTRAST,
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
    PET_LOW_REPLY,
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
    A_WAIT_ENDING,
    SOMETHING_CAME_APART,
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
    SAME_AGAIN,
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
    RETURNED_TO_IT_FIRST,
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
    WHY_AFTER_TASTE,
    WILD_BIRDS,
    WIN_IN_A_SILENCE, WIN_AND_A_COST,
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
    A_BAD_TIME_TOLD, A_DAY_ASKED_PLAIN, A_NAMED_AFTER, A_NAMED_AFTER_THEM, A_NAME_STORY,
    A_NAME_TOLD, A_PLAN_THAT_FELL_THROUGH, A_STATE_NOW, A_STATE_PAST, A_THING_CAME_OUT_WRONG,
)
from .fallback_data import (
    ABSENCE,
    A_BOOKING_AHEAD,
    A_BOOKING_AHEAD_DATED,
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
    PAUSE_IN_A_SAFETY_THREAD,
    PRIVACY_ASK,
    PRIVACY_SHAPES,
    THE_DAY,
    WORDING_SOMEONE,
    _LANDED,
)

from .fallback import (
    ABOUT, ABOUT_SELF, ABOUT_TALLY, ABOUT_WORDS,
    ACK, ACKS, ACK_AFTER_TROUBLE, ACK_WARM,
    ACTS_FOR_ME, AGREEMENT, AIM_HEADS, ANIMALS,
    ANSWERING_A_QUOTED_ASK, A_BIRTHDAY_STILL_TO_COME, A_BIT_PAST_IT, A_CHILD,
    A_CHILD_LEAVING, A_CHILD_LEFT, A_COMPARISON_OF_STANDING, A_COST_SOMEBODY_ASKS,
    A_DISMISSAL, A_DREAD, A_GOOD_TIME, A_GOOD_TIME_IN_A_CARE_THREAD,
    A_HELP_WORD, A_LAUGH, A_MOOD_WITH_A_CATCH, A_SMALL_DAY,
    A_SORRY_ON_ITS_OWN, A_SUGGESTED, A_SUGGESTED_BY_SOMEONE, A_THING_LOOKS_SAD,
    A_THING_THEY_REGRET, A_WANT_IT_OVER, A_WAY_OF_BEING, BAD_STRETCH,
    BAD_STRETCH_REPLIES, BEHIND_ON_MONEY, BODY_ALSO, BODY_LEAD,
    BODY_PART, BODY_PART_QUALIFIER, BODY_PART_TAIL, BODY_POOLS,
    BODY_SITUATION, BODY_STATES, BODY_TAIL, BOUND_FOR,
    CAME_BACK, CANNOT_ANYTHING, CANNOT_ANYTHING_ASK, CANNOT_READ_YOURS,
    CANNOT_SEE_ANYTHING, CANNOT_SEE_ANYTHING_LINES, CANNOT_YOUR_OWN, CARD_LINES,
    CARING, CARING_FOR_A_BODY, CHECK_PHRASES, CLOSED_DOOR,
    COMFORT_SAID, CONGRATS, CROWD, CUT_FOR,
    DATES_KEEP_SLIPPING, DATE_AHEAD, DECLINED_PLAN, DECLINED_PLAN_GENTLE, DISH_DETERMINER,
    DISH_PARTICIPLE, DITHER, DITHER_DECIDE, DITHER_OPEN,
    DITHER_OPEN_LINES, DITHER_TWO_WAY_LINES, DITHER_YES_NO, DONE_NOT_THIS,
    DONE_VERB, DOUBLE_BOOKED, DOUBT, DOUBTED,
    ELDER_AID_REPLIES, ELDER_CLINIC_REPLIES, ELDER_DOCTOR_REPLIES, ELDER_HELP_REPLIES,
    EMBARRASSED, EMERGENCY_CALL, EMPTY, EXPERT_WORDS,
    FLAT, FLAT_LINE, FOOD_TOPICS, FORGETS_AGAIN,
    FORGETS_A_CLASH, FORGET_A_DATE, FORGET_A_SECRET, FOUND_IT,
    FRAME_WORDS, FRIGHTENED, GOING_BOTH_WAYS, GREETING,
    GRIEF_AFTER, GRIEVANCE, HABIT_ACT, HABIT_PROBLEM_ACT,
    HABIT_REPLY, HAND, HANDS_BACK, HANDS_IT_BACK,
    HAND_BACK, HARM_ANYWHERE, HARM_NAMED, HARM_ON_ME, A_HURT_MYSELF,
    HEALTH_MODIFIER, HEALTH_WORDS, HELP_ALREADY, HELP_SERVICE,
    HOUSE_VERB, HOW_ARE_YOU, HURT_EVENT, IDIOM_GLAD,
    IDIOM_SHY, IMPERATIVE, INVITED, INVITED_TO_TALK,
    A_GOODNESS_ASKED_OF_ME, A_SKILL_ASKED_OF_ME, ASKED_A_RATING, ASKED_IF_GOOD,
    I_RATE_A_SKILL, JUNK_CUES, KEEPS_FORGETTING, KNOCKED,
    LANDED_BAD, LATE_ASKS, LATE_BEHIND_LINES, LATE_NOT_A_TIME,
    LATE_NOT_IT, LATE_NOW, LATE_NOW_LINES, LAUGHED_AT,
    LEAVING_A_PERSON, LEFT_BEHIND, LEFT_POOL, LEFT_POOL_GONE,
    LOCKED_OUT_LINES, LOCKED_OUT_OF_THE_CAR, LOST_A_THING, LOST_A_THING_AGAIN,
    LOST_QUESTION, LOW_DAY_REPLIES, LUMP, MILESTONE,
    MISHAP_BACK, NAMED_NEGATIVE, NEARLY, NEGATIVE,
    NEGATIVE_CUES, NEGATIVE_LINE, NEGATORS, NEUTRAL,
    NEVER_MIND, NEWS_TO_COME, NOT_FIT_ENOUGH, NOT_LEAVING_ANYONE,
    A_CORRECTION_TAKEN,
    NOT_SELF, NOT_TOO_OLD, NO_DIRECTION_REPLY, ONE_SKILL_RATED,
    OWN_THING, PAST_STATE_CUES, PENDING_DOUBT, PENDING_LANDED,
    PENDING_WAITING, PENDING_WHEN, PERSON_WORDS, PET_CONDITION_TROUBLE,
    PET_TROUBLE, PLAN, PLAN_DONE, PLAN_DONE_ACK, reads_as_a_change_of_medicine,
    PLAN_MEDICINE_REPLY, PLAN_MEDICINE_SLOW, PLAN_MEDICINE_SLOW_REPLY,
    PLAN_IDIOM, PLAN_KNOCKED, PLAN_NOT_YET, POLICE_CALL,
    POSITIVE, POSITIVE_CUES, PREGNANCY_BLEEDING, PRESENT,
    PUNT, QUOTE_ASKS, QUOTE_LINES, RATES_A_SKILL,
    REACTIONS_CARE, REACTIONS_SAID, REACTION_REPEAT, RELATIONSHIP_DECISION,
    RELIEF, ROUTINE, ROUTINE_NOT, ROUTINE_PHRASES,
    ROUTINE_WORDS, RUMINATION_REPLIES, RUN_OUT_LINES, SECRETS_KEEP_SLIPPING,
    SELF_BLAME, SELF_BLAME_ASKS, SELF_SUBJECT, SOMEBODY_HURT,
    SOMEONE_GONE, SOMEONE_LEAVING, SOMEONE_SERIOUSLY_ILL, SORRY_FOR_ASKING,
    SORRY_ON_ITS_OWN, SO_NOTHING_LIVE, STATE_CUES, STRETCH_OF_TIME,
    STUCK_AFTER_TROUBLE, SUDDEN_LOSS, SYMPTOM, SYMPTOM_COLD,
    SYMPTOM_LINGERS, TELL_HARD, TELL_HARD_LINES, TELL_NOT_WORDS,
    THANKS, THANKS_GOOD_AGAIN, THANKS_NO_BETTER, THANKS_THEN_SAID,
    THANKS_WENT_BADLY, THE_FIRST_HOUR_AND_A_CHILD, THE_LEAVE_HAS_HAPPENED, TIGHT_MONEY,
    TIGHT_MONEY_MORE, TIPS_LINES, TOO_MUCH, TOO_MUCH_PHRASES,
    UNKNOWN, UNKNOWN_HEALTH, UNKNOWN_MONEY, UNKNOWN_WORD,
    VET_WHO, WALKED_INTO_POOL, WIN_IN_A_SILENCE, WORDING_ASKS,
    WORDING_ASKS_WHO, WORDING_LINES, WORDING_SAYS, WORDING_SOMEONE,
    WORDING_TELL, WORDING_WHERE, WOULD_HAVE_BEEN, YOU_SUBJECTS,
    _CAUGHT, _DAY_WORDS, _ILL, _LUMP,
    _NO_DAY_OF_THEIR_OWN, _START_ASK, _THING_DONE_LINES, _WAS,
    _a_bad_line_above, _a_care_thread_to_leave_alone, _a_carer_refused, _a_cost_somebody_asks,
    _a_day_ahead, _a_dead_end, _a_declined_plan, _a_doable,
    _a_good_time, _a_guessed_result, _a_hard_week, _a_knock_into_a_thing,
    _a_knock_on_oneself, _a_leaning_side, _a_loss_recently, _a_mishap,
    _a_mishap_to_ask_about, _a_mood_word, _a_no_from_the_bot, _a_place_asked_about,
    _a_plan_on_the_table, _a_question_about_the_person, _a_refusal_to_answer, _a_relationship_ending,
    _a_start_ask, _a_subject_above, _a_tally_of_its_own_day, _a_thing_they_started,
    _a_time_in_it, _a_verdict_line, _a_verdict_on_their_plan, _about,
    _action, _after_advice, _after_safety, _an_invitation,
    _an_open_result, _answered_recently, _asks_for_help, _asks_how_are_you,
    _came_back, _dreading, _grief_thread, _grievance_thread,
    _hedged_recently, _help_topic, _in_a_care_thread, _in_a_loss_thread,
    _in_a_pool, _in_an_aim, _in_sudden_loss_thread, _is_a_tips_ask,
    _is_presence_check, _is_rumination, _live, _looking_forward,
    _matchable, _money_decision, _my_pick, _named_draft,
    _names_their_age, _news_above, _no_words, _occasion_pool,
    _only_the_stuck_phrase, _opens_a_question, _own_feeling, _plain,
    _plan_reported, _reaction_pool, _reads_as_a_question_when_repaired, _reads_as_dither,
    _reads_as_greeting, _reads_as_illness, _reads_as_question, _run_out,
    _a_promise_that_keeps_moving,
    _says_only_what_they_said, _self_line, _someone_else_dropped_it, _someone_else_minding,
    _am_i_a_nuisance, _something_funny, _sorry_for_asking, _summons_pool, _taste,
    _acknowledges_alone,
    _thanks_news_went_badly, _thanks_then_said, _thanks_with_more, _the_answers_take_it,
    _asks_for_words, _the_ask_for_words_behind_a_doubt, _the_bot_says_it_cannot,
    _the_day_described, _the_heavy_pool,
    _the_last_line_was_a_fault, _the_last_line_was_bad_news, _the_last_line_was_heavy, _the_line_before,
    _the_line_cancels, _the_live_thing_named, _the_news_landed, _the_person_already_said_it,
    _the_person_they_are_stuck_on, _the_stretch_of_time, _the_turn_before_was_a_heavy_one, _the_view_asked_for,
    _their_contact_number, _their_own_slip, _thing_done_pool, _thing_done_scan,
    _thread_is_about_the_body, _tips, _trouble, _unknown,
    _verdict_pool, _wants_it_over, _weighs_a_choice, _what_no_eyes_already_says,
    _who_for, _words, a_comparison_of_standing, a_continuation_of_the_tight_week,
    a_fresh_death_and_the_words, a_happening_now, a_loss_in_the_thread, ack,
    answer_reaction, asks_for_more, circumstance, draft,
    facts, finding_out, goodnews, greeting_only,
    handoff, in_a_safety_thread, is_a_hedge, last_bot,
    last_user, leaving, loss, no_eyes,
    onething, quantity, random, re,
    reading, reads_as_a_carer_body, reads_as_a_clear_result, reads_as_a_closed_door,
    reads_as_a_leaving_already_gone, reads_as_a_narrowing, reads_as_a_pet_condition,
    reads_as_a_report, reads_as_a_return, _a_chat_behind_it,
    reads_as_a_win_nobody_noticed, reads_as_an_award_lost, reads_as_an_occasion, reads_as_bad_news,
    reads_as_good_news, reads_as_if_i_saw, reads_as_news_to_come, reads_as_news_with_a_name,
    reads_as_pregnancy_bleeding, reads_as_recovery, reads_as_settled, reads_as_someone_close_is_ill,
    reads_as_sudden_loss, reads_as_the_leaving, reads_as_the_speakers_own_plan, reads_for_a_carer,
    reads_for_a_pet, reads_like_a_symptom, remark, says_it_has_lingered,
    step_when_low, stuck_line, swap, the_advice,
    the_answer_to_cut, the_bound_said, the_dislike_ask, the_limits_said, the_lost_ask_reply,
    trouble, turns_round, understand, unknown_pool,
    unseen, verdicts_a_thing, who_settles, why,
    WEATHER_COLD, WEATHER_HOT, WEATHER_WET,
    worn, worry_on_the_table,
)

FEEL_COPULA = frozenset(("feel", "feeling"))


def _body_state(clean):
    if "?" in clean or " but " in clean or " not " in clean:
        return None
    flat = clean.replace("light-headed", "lightheaded").replace("light headed", "lightheaded")
    flat = flat.replace("bunged-up", "bungedup").replace("bunged up", "bungedup")
    flat = flat.replace("blocked-up", "blockedup").replace("blocked up", "blockedup")
    words = [w.strip(".,!?;:") for w in flat.split()]
    words = [w for w in words if w]
    if not words or _opens_a_question(words):
        return None
    for index in range(len(words) - 1):
        if words[index] not in ("im", "i'm", "am", "iam") and not (
                words[index] == "i" and (words[index + 1] == "am"
                                         or words[index + 1] in FEEL_COPULA)):
            continue
        if any(w not in BODY_LEAD for w in words[:index]):
            continue
        start = index + 2 if words[index] == "i" else index + 1
        if GOING_BOTH_WAYS.search(clean):
            return None
        state, after = _state_from(" ".join(words[start:]))
        if state:
            return state
    part_state = _a_part_in_a_state(clean)
    if part_state:
        return part_state
    return None


def _a_part_in_a_state(clean):
    part = BODY_PART.search(clean)
    if not part:
        return None
    words = [w.strip(".,!?;:") for w in part.group("rest").split()]
    words = [w for w in words if w]
    for index, word in enumerate(words):
        state = _the_state(word)
        if not state:
            if word not in BODY_PART_QUALIFIER:
                return None
            continue
        if state == "hot":
            return None
        rest = [w for w in words[index + 1:] if w != "and"]
        if all(w in BODY_PART_TAIL or _the_state(w) == state for w in rest):
            return state
        return None
    return None


def _a_part_is_cold(clean):
    return _a_part_in_a_state(clean) == "cold"


def _state_from(rest):
    if not rest:
        return None, []
    words = [w.strip(".,!?;:") for w in rest.split()]
    for index, word in enumerate(words):
        state = _the_state(word)
        if not state:
            continue
        tail = words[index + 1:]
        if tail and tail[0] == "and" and len(tail) == 2 and tail[1] in BODY_ALSO:
            return state, []
        if not tail or all(w in BODY_TAIL for w in tail):
            return state, tail
        if " ".join(tail) in BODY_SITUATION:
            return state, tail
    return None, []


def _the_state(word):
    for name, pool in BODY_STATES.items():
        if word in pool:
            return name
    return None


HABIT_STATED = re.compile(
    r"\b(?:i|we)\s+(?:(?:always|never)\s+" + HABIT_ACT +
    r"|(?:keep|keeps|end\s+up|ends\s+up|can'?t\s+stop|cant\s+stop)\s+" + HABIT_ACT +
    r"|(?:tend|tends)\s+to\s+" + HABIT_ACT +
    r"|never\s+get\s+round\s+to\b" +
    r")"
    r"|\b(?:im|i'?m)\s+always\s+" + HABIT_ACT +
    r"|\bmy\s+(?:brain|mind|memory|head|hands?|eyes?|stomach|skin|body|voice|mood|sleep|"
    r"focus|concentration|attention|nerves|anxiety|appetite|breathing|gut|bladder|jaw)\s+"
    r"(?:keeps|always|never)\s+" + HABIT_ACT, re.I)
HABIT_NOT = re.compile(r"\b(?:never\s+get\s+(?:invited|asked|picked|chosen|included)|"
                       r"left\s+out|no\s+one\b|nobody\b|"
                       r"\b(?:always|never)\s+do(?:es)?\s+(?:this|that|it)\b|"
                       r"\b(?:always|never)\s+late\b|"
                       r"\b(?:going|go|went|running|run)\s+back\s+to\s+(?:him|her|them)\b|"
                       r"\bnever\s+(?:hear|heard|see|saw|seen|win|won)\b)", re.I)
HABIT_MIND_IT = re.compile(
    r"(?:i\s+wish|can'?t\s+stop|cant\s+stop|want\s+to\s+stop|need\s+to\s+stop|"
    r"trying\s+to\s+stop|drives\s+me\s+(?:mad|crazy|nuts|up\s+the\s+wall)|"
    r"bothers\s+me|gets\s+to\s+me|sick\s+of|fed\s+up|i\s+hate\s+that|shouldn'?t|"
    r"shouldnt|i\s+feel\s+bad|i\s+feel\s+guilty|upsets\s+me|i\s+do\s+it\s+again)", re.I)


def _habit_is_a_problem(clean):
    return bool(HABIT_PROBLEM_ACT.search(clean) or HABIT_MIND_IT.search(clean))


def reads_as_a_flat_habit(text, understood=None):
    said = [str(text or "")]
    repaired = (understood or {}).get("plain") if isinstance(understood, dict) else None
    if repaired and repaired != said[0]:
        said.append(repaired)
    for line in said:
        if _flat_habit_stated(line):
            return True
    return False


def _flat_habit_stated(raw):
    clean = " ".join(raw.lower().split())
    words = clean.split()
    try:
        return bool(HABIT_STATED.search(clean) and not HABIT_NOT.search(clean)
                    and _mood(words, clean) == "neutral"
                    and not _reads_as_question(raw, words)
                    and _habit_is_a_problem(clean))
    except Exception:
        return False


NOT_ABOUT_THEM = re.compile(r"\bthe\s+([\w']+)\s+(?:is|was|are|were|gets|looks)\s*$")


def _a_claim_about_a_thing(before):
    found = NOT_ABOUT_THEM.search(before + " ")
    return bool(found) and found.group(1) not in STRETCH_OF_TIME


ACT_OPENER = re.compile(
    r"^(?:please\s+|ok\s+|okay\s+|right\s+|so\s+|hi\s+|hello\s+|hey\s+|and\s+|"
    r"(?:can|could|would|will)\s+you\s+(?:please\s+)?)*"
    r"(?:take|put|get|bring|grab|turn|set|fill|switch|open|lock|wash|hoover|tidy|clean|post|"
    r"feed|walk|make|book|reserve|order|call|ring|phone|text|email|buy|pay|renew|"
    r"send|search|sign|pick|save|keep|chase|look|find)\b")
ACT_THING = re.compile(
    r"\b(?:rubbish|bins?|bin\s+bags?|kettle|cuppa|tea|coffee|oven|heat|heating|thermostat|"
    r"alarm|washing|laundry|dishes|door|window|windows|light|lights|lamp|water|bottle|table|"
    r"taxi|cab|appointment|doctor|dentist|gp|surgery|prescription|milk|bread|paper|"
    r"post|parcel)\b")
ADDRESSED = re.compile(
    r"^(?:ok\s+|okay\s+|right\s+|so\s+|hi\s+|hello\s+|hey\s+|and\s+)*"
    r"(?:(?:can|could|would|will)\s+you\b|please\b|kindly\b)")
BOOKING_THING = re.compile(r"\b(?:table|taxi|cab|room|tickets?|flight|hotel|appointment|"
                           r"restaurant|booking)\b")
A_MESSAGE_OR_A_FORM = re.compile(
    r"\b(?:text|message|email|e-mail|letter|note|reply|voicemail|form|application|document)\b"
    r"|\b(?:sign|fill)\s+(?:this|it|that|in|out)\b|\bfill\s+in\b")
KEEP_ME_POSTED = re.compile(
    r"\bkeep\s+me\s+(?:posted|informed|updated|in\s+the\s+(?:loop|picture)|company)\b")
ACT_FOR_ME = re.compile(r"\b(?:for me|on my behalf)\b|^\s*(?:please\s+)?(?:book|reserve|order|"
                        r"call|ring|phone|text|email|buy|pay|send|save|pick|sign|keep|search)\s+"
                        r"(?:me|us)\b")
REMIND_ME = re.compile(r"^(?:please\s+|ok\s+|okay\s+|hi\s+|hello\s+)?remind me\b")
ACT_REPORT_TAIL = re.compile(
    r"(?:\b(?:and|but|then|so|because|till|until|when|while|whereas)\b|[,;])\s*"
    r"(?:it|they|he|she|i|we|the|my|its|this|that|there|nothing|nobody|everything|"
    r"someone|something)\b"
    r"|\b(?:still|keeps|kept|never|always|wont|cant|cannot|doesnt|didnt)\b"
    r"|\b(?:it'?s|its|it|they'?re|theyre|they|we'?re|we|i'?m|im|i|he'?s|she'?s|he|she|there)"
    r"\s+(?:not\s+)?(?:been|was|were|is|are|got|get|gets|went|goes|gone|split|splits|came|comes|"
    r"trips|cuts|leaks|floods|flooded|keeps|kept|stopped|broke|breaks|smells|smelt|died|works|"
    r"worked|fails|failed|\w+ing|full|empty|dirty|wet|broken|dead|stuck|blocked|loud|noisy|"
    r"cold|hot|freezing|boiling|on|off|open|shut|late|early)\b")


ACT_CHOICE = re.compile(r"\bor\b")
ACT_OWN_STEP = re.compile(r"^\s*(?:it|them|that|this|those|these|one)\b")
ACT_SETTING = re.compile(
    r"\bgas\s+mark\s+\d+"
    r"|\b\d{2,3}\s*(?:c\b|\u00b0|degrees)"
    r"|\b(?:at|on|to)\s+\d{2,3}\b"
    r"|\b(?:for|about)\s+\d+\s*(?:mins?|minutes|hours?|hrs?)\b")


POLITE_ASK = re.compile(
    r"^(?:(?:ok|okay|right|so|hi|hello|hey|and|thanks|ta|now|sorry|please)\s+)*"
    r"(?:(?:any\s+chance\s+)?(?:can|could|would|will)\s+(?:you|u)"
    r"|any\s+chance\s+(?:you|u)\s+(?:could|can|would|will))\s+(?:please\s+|possibly\s+)?"
    r"(?P<rest>[a-z0-9 ',.\-?!]+)$")
ACTS_IN_A_DIARY = re.compile(
    r"\b(?:put|add|save|write|note|stick|move)\b.*\b(?:in|on|into|to)\s+(?:my|the)\s+"
    r"(?:calendar|diary|phone|notes?|list|fridge)\b")
ACTS_ON_A_PHONE = re.compile(
    r"^(?:just\s+|also\s+)?(?:(?:call|ring|phone|text|message|contact|chase)\b"
    r"|(?:speak|talk)\s+to\s+(?!me\b|us\b))")
ACTS_AN_ERRAND = re.compile(
    r"^(?:just\s+|also\s+)?(?:(?:book|reserve|buy|pay|purchase|renew|cancel|collect|pick\s+up|"
    r"apply|set\s+up|drop\s+off)\b|(?:get|ring|call|book|order)\s+(?:me|us)\s+(?:a|an|some)\b)")
HANDS_IT_OVER_HERE = re.compile(
    r"\b(?:call|ring|phone|text|message|email|send|post|contact|chase)\s+(?:me|us)\b"
    r"(?!\s+(?:a|an|some)\b)")
NOT_A_THING_TO_GET = re.compile(
    r"\b(?:(?:some|a bit of|a little)\s+(?:time|rest|peace|quiet|space|slack)"
    r"|attention|my thoughts|the steps|a break|a rest|a day|a night|it a day|it a night)\b")
CAN_DO_ITSELF = re.compile(
    r"^(?:write|draft|rewrite|help|suggest|recommend|explain|remember|remind|tell|say|show|"
    r"pick\s+(?:one|which|between|the\b)|choose|plan|make|give|keep|freeze|cook|reheat|bake|"
    r"read|listen|work|sort|order(?!\s+(?:me|us)\b)|deal|spell|"
    r"check\s+(?:my\s+)?(?:spelling|grammar|writing|english|essay|answer|answers|maths|sums|"
    r"homework|work)|check\s+this|check\s+that|check\s+it)\b")
ACTS_ON_A_PHONE_LINES = (
    "I can't ring or message anyone for you - there's no phone on this end. Tell me who it is and "
    "what has to be said, and I'll help you find the words before you call.",
    "No phone here, so the call can't be mine. Give me the who and the one thing you need from "
    "them, and we'll work out what to say.",
)
ACTS_AN_ERRAND_LINES = (
    "I can't book, buy or pay for anything from here, sorry - the doing is yours. What I can do "
    "is the choosing: the options, the order to do it in and the questions to ask. Which part?",
    "Nothing in the world is mine to do - no booking, no paying. Tell me what you're after and "
    "I'll narrow it down, or work out what to check before you commit.",
)
ACTS_IN_A_DIARY_LINES = (
    "I can't put anything in your calendar - I only hold it for this chat, and it goes when the "
    "chat does. Put it in your phone with a reminder; tell me the date and I'll help you plan "
    "around it.",
    "Your calendar isn't something I can reach, sorry. Write it in your phone with a reminder, "
    "and say the day here and I'll help you get ready for it.",
)
ACTS_ON_A_CLOCK_LINES = (
    "No clock on this end - nothing here can ring or buzz. The timer in your phone's clock app "
    "does it in two taps; tell me what it's for and I'll help with the rest of it.",
    "I can't set a timer or an alarm, sorry - I'm only up while you are typing. Set it on your "
    "phone and tell me the job it's for; that part I can help with.",
)
ACTS_ON_A_DOCUMENT_LINES = (
    "Nothing on this end can print, scan or send a file - no printer, no outbox. The print or "
    "share button on whatever you're reading this on does it; tell me what it is and I'll help "
    "with the rest.",
    "That one needs a printer or an inbox, and neither is mine. Do it on your own device, and "
    "bring me the wording or the order to send things in.",
)


ORDER_OPENER = re.compile(
    r"^(?:(?:ok|okay|right|so|hi|hello|hey|and|just|now|quick|quickly|please|ta|thanks)\s+)*"
    r"(?P<job>(?:text|message|whatsapp|sms|email|mail|ring|call|phone|facetime|contact|chase|book|"
    r"reserve|order|buy|purchase|renew|collect|pick\s+up|put|add|save|write|note|jot|set|wake|"
    r"alarm|print|scan|photocopy|copy|download|upload|send|forward|share)\b)(?P<tail>.*)$")
ORDER_A_MESSAGE = re.compile(
    r"^(?:text|message|whatsapp|sms|email|mail|ring|call|phone|facetime|contact|chase)\s+"
    r"(?:my|our|the|his|her|their|a|an|\w+'s)\s+\w+")
ORDER_A_BUY = re.compile(
    r"^(?:book|reserve|order|buy|purchase|renew|collect|pick\s+up)\s+(?:me\s+|us\s+)?"
    r"(?:a|an|the|some|two|three|four|more|my|our|another)\b")
ORDER_A_RECORD = re.compile(
    r"^(?:put|add|save|write|note|jot|stick|move)\b.*\b(?:in|on|into|to)\s+(?:my|the)\s+"
    r"(?:\w+\s+){0,2}(?:calendar|diary|phone|notes?|list|app|reminders?|fridge|whiteboard)\b"
    r"|^(?:save|keep)\s+(?:this|that|it)\b")
ORDER_A_CLOCK = re.compile(
    r"^(?:set|put)\s+(?:a|an|the|my)\s+(?:timer|alarm|countdown|reminder|stopwatch)\b"
    r"|^wake\s+me\b|^(?:set|put)\s+(?:a|an|the)\s+alarm\b|^alarm\s+me\b")
ORDER_A_DOCUMENT = re.compile(
    r"^(?:print|scan|photocopy|copy|download|upload|send|forward|share)\s+"
    r"(?:this|that|it|these|those|them|a|an|the|my|two|three)\b")
ORDER_A_REPORT = re.compile(
    r"\b(?:and|but|then|so|because|till|until|while)\s+"
    r"(?:it|they|he|she|i|we|the|my|its|there|nothing|nobody|everyone)\b"
    r"|\b(?:yesterday|last\s+night|last\s+week|this\s+morning|earlier|already|never|always|"
    r"every\s+day|usually|used\s+to|didnt|didn't|did|keeps|kept)\b")
ORDER_NOT_A_JOB = re.compile(
    r"\b(?:ambulance|paramedic|paramedics|999|911|112|fire\s+brigade|police|cops|101|"
    r"it\s+a\s+(?:day|night)|a\s+day|a\s+night|it\s+off|quits)\b")


def _an_order_it_cannot_do(clean):
    bare = " ".join(re.sub(r"[^a-z0-9 ']+", " ", str(clean or "").lower()).split())
    if not ORDER_OPENER.match(bare) or ORDER_A_REPORT.search(bare):
        return None
    if ORDER_NOT_A_JOB.search(bare):
        return None
    if ORDER_A_CLOCK.search(bare):
        return ACTS_ON_A_CLOCK_LINES
    if ORDER_A_RECORD.search(bare):
        return ACTS_IN_A_DIARY_LINES
    if ORDER_A_MESSAGE.search(bare):
        return ACTS_ON_A_PHONE_LINES
    if ORDER_A_BUY.search(bare):
        return ACTS_AN_ERRAND_LINES
    if ORDER_A_DOCUMENT.search(bare):
        return ACTS_ON_A_DOCUMENT_LINES
    return None


def _act_asked_of_me(clean):
    match = POLITE_ASK.match(" ".join(str(clean or "").lower().split()))
    if not match:
        return None
    rest = match.group("rest").strip()
    if not rest or CAN_DO_ITSELF.match(rest):
        return None
    if ACTS_IN_A_DIARY.search(rest):
        return ACTS_IN_A_DIARY_LINES
    if EMERGENCY_CALL.search(rest) or POLICE_CALL.search(rest):
        return None
    if NOT_A_THING_TO_GET.search(rest) or HANDS_IT_OVER_HERE.search(rest):
        return None
    if ACTS_AN_ERRAND.search(rest):
        return ACTS_AN_ERRAND_LINES
    if ACTS_ON_A_PHONE.search(rest):
        return ACTS_ON_A_PHONE_LINES
    return None


def _the_store_has_the_recall(clean, memory):
    try:
        from ..modules import memory_store
    except Exception:
        return False
    try:
        return bool(memory_store.respond(clean, memory if isinstance(memory, dict) else {}))
    except Exception:
        return False


def _acts_for_me(clean, memory=None):
    bare = " ".join(re.sub(r"[^a-z0-9 ']+", " ", str(clean or "").lower()).split())
    if KEEP_ME_POSTED.search(bare):
        return False
    if A_MESSAGE_OR_A_FORM.search(bare):
        if (no_eyes.writes_the_message(clean)
                or no_eyes.cannot_see_your_thing(clean)
                or no_eyes.look_at_a_body_lines(clean, bare)):
            return False
    if REMIND_ME.match(bare):
        return not _the_store_has_the_recall(clean, memory)
    opener = ACT_OPENER.match(bare)
    if not opener:
        return False
    tail = bare[opener.end():]
    if ACT_REPORT_TAIL.search(tail):
        return False
    if not ACT_FOR_ME.search(bare):
        if ACT_CHOICE.search(bare) or ACT_OWN_STEP.match(tail) or ACT_SETTING.search(bare):
            return False
    if ACT_FOR_ME.search(bare):
        return True
    verb = bare.split()[0]
    if verb not in HOUSE_VERB and not ADDRESSED.match(bare):
        return False
    if verb in ("call", "ring", "phone", "text", "email", "buy", "pay", "renew"):
        return False
    if verb in ("book", "reserve", "order"):
        return bool(BOOKING_THING.search(bare))
    return bool(ADDRESSED.match(bare) or ACT_THING.search(bare))


def _reads_as_a_bad_stretch(clean):
    words = [w.strip(".,!?;:") for w in clean.split()]
    for index, word in enumerate(words):
        if word not in BAD_STRETCH:
            continue
        before = " ".join(words[max(0, index - 4):index])
        if _a_claim_about_a_thing(before):
            continue
        after = words[index + 1:]
        if after[:1] in (["few"], ["couple"]) and len(after) > 1:
            after = after[1:]
        if after and after[0] in STRETCH_OF_TIME:
            return True
        if not after and any(w in STRETCH_OF_TIME for w in before.split()):
            return True
    return False
def _cue_negated(words, cue):
    for index, word in enumerate(words):
        if word != cue:
            continue
        if any(other in NEGATORS for other in words[max(0, index - 2):index]):
            return True
        before = words[max(0, index - 3):index]
        if set(before) & DOUBTED:
            return True
        if set(before) & DOUBT and turns_round(before):
            return True
    return False


def _a_state_in_the_past(words, index):
    return bool(set(words[max(0, index - 3):index]) & _WAS)


def _the_win_is_someone_elses(words, index):
    after = words[index + 1:index + 3]
    if after and after[0] in ABOUT_WORDS and set(after[1:]) & PERSON_WORDS:
        return False
    for j in range(index - 1, max(-1, index - 7), -1):
        word = words[j]
        if word in YOU_SUBJECTS:
            return False
        if word in CROWD:
            return True
        if (word in loss.PEOPLE and word.endswith("s")
                and "all" in words[max(0, j - 3):j + 1]):
            return True
    return False


THINGS_THAT_STOP = frozenset((
    "died", "dead", "broke", "broken", "collapsed", "failed", "stopped", "conked",
))
THINGS_THAT_STOP_AFTER_UP = frozenset(("gave", "given", "packed", "went"))
THE_WORDS_BETWEEN = frozenset(("has", "have", "had", "is", "was", "were", "s", "just", "now"))


PLEASURE_WORD = (r"(?:fun|funny|joy|joyful|pleasure|enjoy(?:s|ed|ing|able)?|happy|happiness|"
                 r"smile|laugh|mood|worth(?:while|\s+doing)?|interest(?:s|ed|ing)?|"
                 r"look\s+forward\s+to|content|exciting|excites?)")
NOTHING_AND_A_PLEASURE = re.compile(
    r"\bnothing\b[^.?]{0,28}?\b" + PLEASURE_WORD + r"\b")
A_COMPARISON = re.compile(r"\b(?:than|beats?|more\s+than|as\s+much\s+as)\b")
NOTHING_NEGATED = re.compile(
    r"\b(?:no|not|never|dont|don'?t|doesnt|doesn'?t|cant|can'?t|cannot|stopped|without)\b"
    r"[^.?]{0,24}?\b" + PLEASURE_WORD + r"\b[^.?]{0,20}?"
    r"\b(?:anything|nothing|much|things|life|it|myself|any\s?more|anymore|at\s+all)\b")
PLEASURE_GONE_OUT = re.compile(
    r"\b(?:fun|joy|pleasure|interest|point|enjoyment)\b\s+(?:has|have|had)\s+"
    r"(?:gone|gone\s+right|all\s+gone)\s+out\s+of\b")
FEELING_NOTHING = re.compile(
    r"\bfeel(?:s|ing)?\s+nothing\b|\bnothing\s+matters\b"
    r"|\bnothing\s+(?:makes\s+me\s+)?feels?\s+(?:good|right|nice|better)\b"
    r"|\b(?:enjoy|enjoying|enjoyed)\s+nothing\b")


PLEASURE_ABOUT_ONE_THING = re.compile(
    r"\b(?:happy|glad|pleased|excited|thrilled|proud)\s+about\s+"
    r"(?:it|that|this|them|him|her|the\b|my\b|his\b|her\b|their\b|our\b)")


def reads_as_no_pleasure(clean):
    text = " ".join(str(clean or "").lower().split())
    if not text:
        return False
    if A_COMPARISON.search(text):
        return False
    if NOTHING_THAT_LIMITS.search(text) or PLEASURE_ABOUT_ONE_THING.search(text):
        return False
    if FEELING_NOTHING.search(text) or PLEASURE_GONE_OUT.search(text):
        return True
    if NOTHING_AND_A_PLEASURE.search(text):
        return True
    return bool(NOTHING_NEGATED.search(text))


ABOUT_THE_BOT_LINES = (
    "Nothing to do it with, I'm afraid: I'm a program, so no body, no senses and no car keys. Ask "
    "me the thing you would ask a friend and I will take that half of it on.",
    "No, and I would rather say so than guess. I am a program in a chat window, so what I can do "
    "is read, remember this conversation and think the question through with you.",
    "Not at all - there is no body here. If it is something you are wondering about, ask it "
    "anyway: plenty of that I can still help with.",
)

ABOUT_THE_BOT = re.compile(
    r"^(?:can|could)\s+(?:you|u)\s+(?:actually\s+|even\s+|really\s+|still\s+)?"
    r"(?:drive|smell|taste|feel|see|hear|touch|breathe|eat|drink|swim|run|walk|dance|sing|laugh"
    r"|cry|shiver|sweat|blink|wave|hold|hug|kick|jump|climb|fly)\b"
    r"(?:\s+(?:anything|something|things?|pain|cold|the\s+sun|a\s+car|at\s+all|either|yet|though))?"
    r"\s*(?:please|then)?\s*\?*\s*$", re.I)


def reads_as_a_question_about_the_bot(clean):
    text = " ".join(str(clean or "").lower().split())
    return bool(text) and bool(ABOUT_THE_BOT.match(text))


PLEASURE_GONE_LINES = (
    "That flatness is a miserable thing to carry, and it is not laziness or a mood to be talked "
    "out of. More than a couple of weeks of it is worth saying to a GP, and until then the "
    "smallest thing that helps is one thing you used to like, put back in this week on a day you "
    "pick. What did you look forward to a year ago?",
    "I'm sorry - when nothing gives pleasure the days go flat and everything takes effort, and "
    "waiting for it to lift is the one thing that does not work. Tell one person, and put one "
    "small piece of what you used to enjoy back on the calendar this week; if it has been weeks, "
    "say it to a GP. What did you like doing before this started?",
    "That is worth taking seriously rather than shaking off: nothing giving pleasure for weeks is "
    "something a GP wants to hear about, and it is not a failing to say so. Until then the "
    "things to try are small and concrete - one walk, one person, one thing you used to look "
    "forward to, this week. Which of those feels least impossible?",
)


def _a_thing_stopping_after(words, i):
    after = list(words[i + 1:i + 5])
    while after and after[0] in THE_WORDS_BETWEEN:
        after.pop(0)
    if not after:
        return False
    if after[0] in THINGS_THAT_STOP:
        return True
    if after[0] in THINGS_THAT_STOP_AFTER_UP and len(after) > 1 and after[1] in ("up", "in",
                                                                               "out"):
        return len(after) == 2 or after[2] in ("on", "it", "them", "me", "him", "her", "us")
    return False


_A_HURT_DONE = re.compile(
    r"\b(?:i|we)\s+(?:just\s+|nearly\s+|think\s+i\s+)?(?:have\s+|had\s+|ve\s+)?"
    r"(?:broke|broken|fractured|cracked|dislocated|sprained|tore|torn|snapped|slipped|"
    r"hurt|injured|done)\b", re.I)
_A_BODY_WORD = re.compile(
    r"\b(?:back|knees?|legs?|feet|foot|ankles?|hips?|arms?|elbows?|wrists?|hands?|fingers?|"
    r"thumbs?|shoulders?|ribs?|neck|toes?|heels?|shins?|calves|calf|thighs?|collarbone|"
    r"jaw|nose|eyes?|head|spine|disc|kneecap|ligaments?|muscles?|tendons?|bones?|"
    r"teeth|tooth|nail|shoulder blade|lip|lips|cheek|cheeks|chin|ears?|eyebrow|"
    r"forehead|scalp)\b", re.I)
_A_HARM_HAD = re.compile(
    r"\b(?:(?:i|we)\s+(?:(?:have|had|has)\s+been\s+)?(?:have|had|got|caught|was given|were given|"
    r"been given|been told|was diagnosed with|diagnosed with)|"
    r"(?:i've|we've|ive|weve)\s+(?:had|got|been given|been diagnosed with))"
    r"\s+(?:to have\s+|to get\s+)?"
    r"(?:a|an|the|my|some|a few|a couple of|two|three|four|five|six|seven|eight|nine|ten|\d+)?\s*"
    r"(?:concussion|concussions|stitches?|staples?|whiplash|pneumonia|sepsis|septicaemia|meningitis|"
    r"covid|coronavirus|shingles|glandular fever|miscarriage|stillbirth|seizure|seizures|"
    r"stroke|heart attack|blood clot|pulmonary embolism|breakdown|relapse|"
    r"chemo|chemotherapy|radiotherapy)\b", re.I)


_A_ILLNESS_WORD = (
    r"(?:[a-z]+\s+){0,2}?"
    r"(?:infections?|bugs?|virus(?:es)?|flu|influenza|fever|colds?|cough|temperature|"
    r"poisoning|disease|illness|ailment|condition|attack|migraines?|seizures?|"
    r"sore throat|sickness|nausea|diarrhoea|diarrhea|rash|abscess|cyst|ulcer|thrush|"
    r"gout|shingles|covid|coronavirus|malaria|tuberculosis|hepatitis|uti|dvt|copd|ibs|mrsa|"
    r"strep|\w+(?:itis|osis|aemia|emia|iasis|pox|virus))"
)
_A_HARM_ILL = re.compile(
    r"\b(?:(?:i|we)\s+(?:(?:have|had|has)\s+been\s+)?(?:have|had|got|caught|was given|were given|"
    r"been given|been told|was diagnosed with|diagnosed with)|"
    r"(?:i've|we've|ive|weve)\s+(?:had|got|been given|been diagnosed with|"
    r"caught))"
    r"\s+(?:to have\s+|to get\s+)?"
    r"(?:a|an|the|my|some|a few|a couple of|two|three|four|five|six|seven|eight|nine|ten|\d+)?\s*"
    + _A_ILLNESS_WORD + r"\b", re.I)
_A_HARM_ILL_NOT = re.compile(
    r"\b(?:cold (?:one|beer|drink|water|shower|bath|snap|call|weather|night|morning|day|"
    r"evening|outside|front|shoulder|hands|feet)|"
    r"bugs? (?:in|on) (?:my |the )?(?:code|computer|laptop|phone|app|program|software|system)|"
    r"virus (?:on|in) (?:my |the )?(?:computer|laptop|phone)|"
    r"temperature (?:setting|gauge|dial|outside|gauge)|"
    r"sickness (?:policy|pay|record|note)|"
    r"in (?:good|no|great|perfect|top) condition|condition of (?:the|my) (?:car|house|road)|"
    r"attack of (?:the )?(?:nerves|conscience)|"
    r"fever pitch|cabin fever|spring fever)\b", re.I)


_A_HARM_IDIOM = re.compile(
    r"\b(?:stroke of (?:luck|genius|good luck|the brush)|brush ?stroke|stroke of a pen|"
    r"broke the ice|broke the news|broke even|broke the bank|broke a record|broke the rules|"
    r"broke a promise|broke the silence|cracked a joke|cracked a smile|cracked on|"
    r"cracked a window|slipped my mind|slipped away|tore a strip off|torn between)\b", re.I)
_A_HARM_KNOCK = re.compile(
    r"\b(?:knocked|thrown|shoved|swiped|swept)\s+off\s+(?:my|our|his|her|their|the|a)\b"
    r"|\bhit\s+by\s+a\s+(?:car|van|lorry|truck|bus|taxi|bike|motorbike|cyclist)\b", re.I)
_A_OUT_OF_SOCKET = re.compile(
    r"\bcame out of (?:its|the|my) socket\b|\bout of (?:its|the) socket\b"
    r"|\b(?:my|our|his|her|their|the)\s+(?:shoulders?|knees?|kneecap|hips?|elbows?|jaw|"
    r"ankles?|fingers?|thumbs?|wrist|toe)\s+(?:came|comes|went|goes|popped|pops) out\b",
    re.I)
_A_IN_AGONY = re.compile(r"\bin (?:absolute |sheer |real )?agony\b", re.I)
_A_PART_WENT = re.compile(
    r"\bmy\s+(?:back|knee|knees|leg|arm|shoulder|hip|ankle|neck)\s+(?:just\s+|suddenly\s+)?"
    r"(?:went|gone|gave way|gives way)\b", re.I)


_A_SOMEONE = (
    r"(?:he|she|they|someone|somebody|anyone|"
    r"(?:a|the)\s+(?:man|woman|lad|bloke|chap|guy|girl|boy|teen|carer|nurse|neighbour|neighbor)|"
    r"(?:my|his|her|their|our)\s+\w+)")
_A_HURT_BY_SOMEONE = re.compile(
    r"\b" + _A_SOMEONE + r"\s+(?:\w+\s+){0,2}?"
    r"(?:hit|punch(?:ed|es|ing)?|kick(?:ed|s|ing)?|slapp?(?:ed|ing)|smack(?:ed|ing)?|"
    r"beat|beats|beating|beaten|headbutt(?:ed)?|bit|bites|burn(?:ed|t|s)|"
    r"chok(?:ed|ing)|strangl(?:ed|ing)|stabbed|stabs|raped|molested|groped|"
    r"dragg?(?:ed|ing)|whipp?(?:ed|ing)|belt(?:ed|ing))\s+(?:me|us)\b"
    r"|\b" + _A_SOMEONE + r"\s+(?:\w+\s+){0,2}?"
    r"(?:hit|punched|kicked|slapped|grabbed|pinched|twisted|yanked|wrenched|bit|bitten)\s+my\s+\w+"
    r"|\b" + _A_SOMEONE + r"\s+(?:\w+\s+){0,2}?(?:push(?:ed|es|ing)?|shov(?:ed|es|ing)?)\s+"
    r"(?:me|us)\s+(?:down|into|against|over|off|up|to the)\b"
    r"|\b" + _A_SOMEONE + r"\s+(?:\w+\s+){0,2}?(?:threw|throws|tossed|spat|spits?)\b"
    r"[^.?!]{0,25}?\bat\s+(?:me|us)\b"
    r"|\b(?:held|holds|holding|put|puts|pointed|pointing|pressed|had|pulled)\s+"
    r"(?:a|an|the|his|her|their)\s+(?:knife|gun|blade|scissors|hammer|bat|belt|bottle|"
    r"glass|razor|needle|pillow|cushion)\s+(?:to|at|against)\s+(?:my|her|his|our)\s+\w+",
    re.I)
_A_HURT_BY_SOMEONE_NOT = re.compile(
    r"\b(?:hit me up\b|hit on me\b|kicked me out\b|beat me (?:at|in|to)\b|"
    r"bit my head off\b|grabbed my (?:attention|eye)\b|"
    r"pushed (?:me|us) into \w+ing\b|"
    r"burn(?:ed|t) me (?:out|a copy|a cd)\b)", re.I)


_A_PART_OUT = re.compile(
    r"\b(?:(?:had|have|having|needed|need|getting|got)\s+)?(?:to have\s+|to get\s+)?"
    r"(?:a|an|my|two|some|the)\s+(?:tooth|teeth|wisdom tooth|wisdom teeth|molars?|"
    r"appendix|tonsils?|adenoids|gallbladder|gall bladder|kidney stone|cataract|"
    r"splinter|ingrown nail|nail)\s+"
    r"(?:out|removed|taken out|pulled|drained)\b", re.I)


_A_PROGNOSIS = re.compile(
    r"\b(?:been given|given|been told (?:i (?:have|'ve|have got|got)|there (?:is|are))|"
    r"told i (?:have|'ve|have got|got))\s+(?:about\s+|only\s+|maybe\s+|perhaps\s+)?"
    r"(?:a|two|three|four|five|six|nine|ten|twelve|eighteen|a few|a couple of)\s+"
    r"(?:more\s+)?(?:days|weeks|months|years)\b"
    r"|\b(?:two|three|four|five|six|nine|ten|twelve|eighteen|a few|a couple of)\s+"
    r"(?:more\s+)?(?:weeks|months|years)\s+(?:left|to live|at most|maybe)\b"
    r"|\b(?:terminal(?:ly)? (?:ill|illness|cancer)|palliative care|in a hospice|"
    r"end of life care)\b", re.I)
_A_PROGNOSIS_THAT_IS_NOT = re.compile(
    r"\b(?:to pay|to repay|to clear|to save|to appeal|to file|to finish|to complete|"
    r"notice|sentence|probation|tenancy|contract|lease|to build|to train|to study|"
    r"to sell|to deliver|warranty|guarantee|to get out of)\b", re.I)


def _a_harm_said(clean):
    said = " ".join(str(clean or "").lower().split())
    if not said:
        return False
    if _A_HARM_IDIOM.search(said):
        return False
    if _A_PART_OUT.search(said):
        return True
    if _A_PROGNOSIS.search(said) and not _A_PROGNOSIS_THAT_IS_NOT.search(said):
        return True
    if _A_HURT_DONE.search(said) and _A_BODY_WORD.search(said):
        return True
    if _A_HURT_BY_SOMEONE.search(said) and not _A_HURT_BY_SOMEONE_NOT.search(said):
        return True
    if _A_HARM_ILL.search(said) and not _A_HARM_ILL_NOT.search(said):
        return True
    return bool(_A_HARM_HAD.search(said) or _A_PART_WENT.search(said)
                or _A_HARM_KNOCK.search(said) or _A_OUT_OF_SOCKET.search(said)
                or _A_IN_AGONY.search(said))


_A_BREAK_THAT_IS_GOOD = re.compile(
    r"\bbroke(?:n)?\s+(?:a|the|my|our|his|her|their|new|world|personal|course|club|national)\s+"
    r"(?:\w+\s+)?(?:records?|ice|sweat|ground|habit|cycle|deadlock|stalemate|personal\s+best)\b"
    r"|\bbroke\s+even\b"
    r"|\bbroke\s+through\b(?!\s+(?:the|a|an|my|our|his|her|their)\s)"
    r"|\bbreak(?:ing)?\s+a\s+record\b", re.I)
_BREAK_WORDS = frozenset(("broke", "broken", "breaking", "breaks"))


def _mood(words, clean=""):
    words = tuple(words)
    if ack.only_a_dislike(clean):
        return "neutral"
    if a_limit_on_the_answer(clean):
        return "neutral"
    if reads_as_no_pleasure(clean):
        return "negative"
    good = bad = False
    if "ill" in words and _reads_as_illness(clean):
        bad = True
    if not good and _a_harm_said(clean) and not reads_like_a_symptom(clean):
        bad = True
    for i, word in enumerate(words):
        if _in_an_aim(clean, word):
            continue
        if word in JUNK_CUES and _a_mood_word(words, word):
            bad = True
            continue
        if word in _BREAK_WORDS and _A_BREAK_THAT_IS_GOOD.search(clean):
            good = True
            continue
        if word not in POSITIVE_CUES and word not in NEGATIVE_CUES:
            continue
        if word in A_MOOD_WITH_A_CATCH:
            before = set(words[max(0, i - 3):i])
            after = words[i + 1] if i + 1 < len(words) else ""
            if after == "up":
                good = True
                continue
            if not (before & A_MOOD_WITH_A_CATCH[word]) and after not in ("me", "him", "her",
                                                                          "them", "us"):
                continue
        window = words[max(0, i - 3):i]
        if set(window) & NEARLY:
            continue
        back = _cue_negated(words, word)
        if word in PAST_STATE_CUES and _a_state_in_the_past(words, i):
            continue
        if word in POSITIVE_CUES and _a_thing_stopping_after(words, i):
            continue
        if word in POSITIVE_CUES:
            if _no_such_thing_before(words, i):
                back = True
            if back:
                if word in STATE_CUES:
                    bad = True
            elif word in A_WAIT_ENDING and SOMETHING_CAME_APART.search(clean or ""):
                continue
            elif _the_win_is_someone_elses(words, i):
                continue
            else:
                good = True
        elif not back or set(window) & AIM_HEADS:
            bad = True
    if bad:
        return "negative"
    if good:
        return "positive"
    return "neutral"


def _no_such_thing_before(words, i):
    for step in range(1, 9):
        if i - step < 0:
            return False
        word = words[i - step]
        if word in CONTRAST:
            return False
        if word in NOTHING_AT_ALL or (word == "one" and i - step - 1 >= 0
                                      and words[i - step - 1] == "no"):
            return True
    return False


def _mixed_seed(text):
    value = 7
    for char in str(text or ""):
        value = (value * 31 + ord(char)) % 1000003
    return value


SAYS_A_FEELING = re.compile(
    r"\b(?:hurts?|hurting|stings?|stung|miss(?:es|ed)?|dreading|dreads|sad|upset|gutted|"
    r"lonely|ach(?:e|es|ing|y)|cry(?:ing)?|broken|struggling|hate|worried|devastated)\b",
    re.IGNORECASE)
A_FEELING_IN_THE_LINE = re.compile(
    r"\b(?:hurts?|hurting|stings?|stung|(?:will|do|would|could)\s+miss|miss(?:es|ed)\b(?!\s+\?)|"
    r"dreading|sad|upset|gutted|lonely|ach(?:e|es|ing|y)|cry(?:ing)?|broken|struggling|hate|"
    r"worried|devastated|hard|tough|quiet|empty)\b",
    re.IGNORECASE)


def _only_what_the_line_gives(pool, clean):
    if A_FEELING_IN_THE_LINE.search(clean or ""):
        return pool
    kept = []
    for line in pool:
        asserts = False
        for sentence in re.split(r"(?<=[.!?])\s+", line):
            if sentence.rstrip().endswith("?"):
                continue
            if SAYS_A_FEELING.search(sentence):
                asserts = True
                break
        if not asserts:
            kept.append(line)
    return tuple(kept) or pool


def _choose(options, memory, clean, seed_text=None):
    turns = memory.get("turns") or []
    recent = [t.get("bot") for t in turns[-5:] if t.get("bot")]
    fresh = [o for o in options if o not in recent]
    if not fresh:
        last = recent[-1] if recent else None
        fresh = [o for o in options if o != last] or list(options)
    if not fresh:
        return None
    if seed_text is None:
        seed = len(turns) * 7919 + sum(ord(c) for c in clean)
    else:
        seed = len(turns) * 7919 + _mixed_seed(seed_text)
    return random.Random(seed).choice(fresh)


def _a_birthday_still_to_come(clean, memory):
    said = " ".join((clean or "").lower().split())
    if not said:
        return None
    met = []
    for one in memory.get("others") or []:
        if not isinstance(one, dict) or one.get("pronoun") or not one.get("who"):
            continue
        age, when = one.get("to_come"), " ".join(str(one.get("turns") or "").lower().split())
        if not isinstance(age, int) or not when:
            continue
        if str(age) not in said or when not in said:
            continue
        met.append(one)
    return met[0] if len(met) == 1 else None


def _the_birthday_said_back(birthday):
    who = str(birthday.get("who") or "").lower()
    if who and not who.startswith(("your ", "my ")):
        who = "your " + who
    age = str(birthday.get("to_come"))
    when = " ".join(str(birthday.get("turns") or "").split())
    said = []
    for line in A_BIRTHDAY_STILL_TO_COME:
        line = line.replace("{who}", who).replace("{age}", age).replace("{when}", when)
        said.append(line[:1].upper() + line[1:])
    return tuple(said)


_ROUTINE_NOT_SHAPE = re.compile(r"\b\d+\s*-?\s*year\s*-?\s*old\b")
_UNDERTAKING = re.compile(r"\b(?:for|with|about)\s+(?:my|our|the|a|an|this|that)?\s*([a-z']+)")


def _somebody_elses_day_in_thread(memory):
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)][-1:]
    for turn in turns:
        said = str(turn.get("user") or "").lower()
        if any(word in said for word in _NO_DAY_OF_THEIR_OWN) or loss.reads_as_loss(said):
            return False
        said_words = set(w.strip(".,!?;:'\"()") for w in said.split())
        if said_words & ROUTINE_NOT or _ROUTINE_NOT_SHAPE.search(said):
            return True
    return False


A_LIST_ON_THE_TABLE = re.compile(
    r"\b(?:too much|lots (?:on|of|to)|a lot (?:on|to)|so much|everything|list|lists|jobs|"
    r"things|plates|spinning|juggling|overwhelmed|swamped|drowning|stretched|spread thin|"
    r"deadlines?|behind|catch(?:ing)? up|workload)\b")


def _the_person_named_a_list(memory):
    if not isinstance(memory, dict):
        return False
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)][-2:]
    return any(A_LIST_ON_THE_TABLE.search(str(turn.get("user") or "").lower()) for turn in turns)


def _routine_pool(clean, words, memory=None):
    words = set(words)
    if memory is not None and stuck_line.the_advice_was_to_get_seen(memory) and (
            any(phrase in clean for phrase in TOO_MUCH_PHRASES)
            or words & {"overwhelmed", "drowning", "swamped"}):
        return stuck_line.URGENT_ALREADY_GIVEN
    if any(phrase in clean for phrase in TOO_MUCH_PHRASES if phrase not in _START_ASK):
        return TOO_MUCH
    if _money_decision(clean) and words & BEHIND_ON_MONEY:
        return UNKNOWN_MONEY
    if any(word not in _DAY_WORDS for word in _UNDERTAKING.findall(clean)):
        return None
    if words & ROUTINE_NOT or _ROUTINE_NOT_SHAPE.search(clean):
        return None
    if memory is not None and _somebody_elses_day_in_thread(memory):
        return None
    if any(phrase in clean for phrase in ROUTINE_PHRASES):
        return ROUTINE
    if words & ROUTINE_WORDS:
        return TOO_MUCH if words & {"overwhelmed", "drowning", "swamped"} else ROUTINE
    if any(phrase in clean for phrase in _START_ASK):
        return TOO_MUCH if _the_person_named_a_list(memory) else None
    return None


def _asks_the_bot(understood):
    if set(understood.get("asks") or ()) & {"recommend", "steps", "options"}:
        return True
    norm = understood.get("norm") or []
    return bool(norm) and norm[0] in IMPERATIVE


def _words(text):
    return tuple(re.findall(r"[a-z']+", str(text or "").lower()))


def _reads(pred, clean, repaired, lower=False, memory=None):
    def ask(text):
        return pred(text.lower() if lower else text, memory) if memory is not None else pred(
            text.lower() if lower else text)
    if ask(clean):
        return True
    if repaired and repaired != clean:
        return bool(ask(repaired))
    return False


ASK_SHAPE = re.compile(r"\b(?:should|could|can|do|does|did|is|are|was|were|will|would|shall|"
                       r"what|when|where|which|who|why|how|any)\b")
FRAME_PREFIX = re.compile(
    r"^(?:(?:no|nah|nope|sorry|ok|okay|wait|oops|actually|oh|right|and|but),?\s+)*"
    r"(?:i\s+(?:mean|meant|said)|scratch\s+that|wait\s+no|no\s+wait|i\s+mean\s+to\s+say)\s+",
    re.I)


def _restated(understood):
    if understood.get("intent") != "correction":
        return ""
    focus = " ".join(understood.get("focus") or []).strip()
    focus = FRAME_PREFIX.sub("", focus).strip(" ,.!?")
    if len(focus.split()) < 2:
        return ""
    if all(word.lower() in FRAME_WORDS for word in focus.split()):
        return ""
    if not ASK_SHAPE.search(focus.lower()):
        return ""
    return focus


def _answers_the_correction(restated, memory):
    from . import verdict
    sub = dict(memory)
    sub["compose"] = dict(memory.get("compose") or {})
    sub["understood"] = understand(restated, memory)
    sub["correction_answered"] = True
    for pool in (verdict.next_step, verdict.reply_for, reply_for):
        reply = pool(restated, sub)
        if reply and not any(punt in reply.lower() for punt in PUNT):
            return reply
    return None


OWN_THING = re.compile(r"\b(?:my|our)\s+[a-z]"
                       r"|\b(?:i|we)\s*(?:'ve|ve|have)\s+(?:got\s+)?(?:a|an|some|two|three|four|"
                       r"a few|another)\b")
A_MOOD = re.compile(r"\b(?:sad|miserable|unhappy|depressed|lonely|dejected|glum|sorry for itself|"
                    r"in the wars|seen better days)\b")


NEAR_MISS = re.compile(r"""
    \b(?:almost|nearly|just\s+about)\s+
    (?:
        won\b
      | beat\s+(?:him|her|them|it|everyone|the\s+\w+)
      | broke\s+(?:the|my|a)\s+(?:\w+\s+)?(?:record|pb|best|streak)\b
      | passed\b(?!\s*(?:out|away|on|wind|water|blood|a\s+stool)\b)
      | got\s+(?:the|that|my)\s+(?:job|place|part|role|promotion|record|pb)\b
      | got\s+(?:it|in|through)\b
      | made\s+it\b
      | qualified\b
      | came\s+(?:first|second|third|top)\b
      | scored\b
    )
""", re.I | re.X)
NEAR_MISS_REPLY = (
    "So close. Was there a last bit that got away, or was it lost earlier than that?",
    "Almost is its own kind of annoying, being right there. What happened at the end?",
    "Ugh, that is the hardest way to miss something. Will there be another go at it?",
    "That is a hard one to sit with, because nearly is not the same as not good enough. What "
    "would have made the difference?",
)


def _a_near_miss(clean):
    return bool(NEAR_MISS.search(str(clean or "")))


def _a_things_state(memory, clean):
    understood = (memory or {}).get("understood") or {}
    text = str(clean or "").lower()
    return (understood.get("state_owner") == "thing"
            and bool(OWN_THING.search(text)) and bool(A_MOOD.search(text)))
_A_CORRECTION = re.compile(facts.CORRECTION_LEAD, re.I)

TAKING_SOMETHING_BACK = re.compile(
    r"^\s*(?:(?:ok|okay|right|so)\s*[,.]?\s*)?"
    r"(?!no\s+(?:one|body)\b)"
    r"(?:no|nope|wait|hold\s+on|hang\s+on|scratch\s+(?:that|it)|forget\s+(?:it|that)|"
    r"my\s+mistake|i\s+(?:got|had)\s+(?:that|it|this)\s+wrong|i\s+made\s+a\s+mistake|"
    r"i'?m\s+wrong|(?:sorry\s*,?\s*)?i\s+(?:mean|meant))\b", re.I)
SAYS_A_THING = re.compile(
    r"\b(?:is|are|was|were|am|be|been|being|do|does|did|done|have|has|had|can|could|will|would|"
    r"shall|should|must|might|may|its|it's|thats|that's|hes|he's|shes|she's|theyre|they're|"
    r"we're|youre|you're|im|i'm|ive|i've)\b|\w+ed\b", re.I)
THE_THING_ITSELF = re.compile(r"^(?:the|these|those|this|that)\b", re.I)
ASKS_AFTER_THE_OPENER = re.compile(
    r"^\s*(?:what|how|why|when|where|who|which|can|could|should|would|will|do|does|did|is|are|"
    r"was|were|have|has|any)\b", re.I)
THE_OPENER = re.compile(r"^\s*(?:(?:ok|okay|right|so|no|nope|wait|ah|oh|sorry)\s*[,.]?\s*)+", re.I)


def _a_chat_to_correct(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    for turn in turns or ():
        if isinstance(turn, dict) and str(turn.get("bot") or "").strip():
            return True
    return False


def _takes_something_back(clean, memory=None):
    text = " ".join(str(clean or "").split())
    if not text or "?" in text or not TAKING_SOMETHING_BACK.match(text):
        return False
    if not _a_chat_to_correct(memory):
        return False
    body = THE_OPENER.sub("", text, count=1).strip(" ,.;:-")
    if body and TAKING_SOMETHING_BACK.match(body):
        body = THE_OPENER.sub("", TAKING_SOMETHING_BACK.sub("", body, count=1), count=1)
    if len(body.split()) < 2 or ASKS_AFTER_THE_OPENER.match(body):
        return False
    return bool(SAYS_A_THING.search(body) or THE_THING_ITSELF.match(body))


def _a_lateness_report(clean, normalised=""):
    if "?" in clean or len(clean.split()) > 12:
        return False
    if LATE_ASKS.search(clean) or LATE_NOT_A_TIME.search(clean):
        return False
    if _mood(_words(clean), clean) != "neutral":
        return False
    read = clean
    hit = LATE_NOW.search(read)
    if hit is None and normalised:
        read = " ".join(normalised.replace(" | ", " ").split())
        hit = LATE_NOW.search(read)
    if hit is None:
        return False
    between = hit.group(1) or ""
    if LATE_NOT_IT.search(between):
        return False
    if (hit.group(0) or "").endswith("behind"):
        after = read[hit.end():]
        if any(word in loss.SELF_NOUNS for word in re.findall(r"[a-z']+", after)):
            return False
    return True


HURT_SOMEBODY = re.compile(
    r"\b(?:my|our|his|her|their|the)\s+(?:son|daughter|boy|girl|child|kid|baby|mum|mom|mother|"
    r"dad|father|brother|sister|husband|wife|partner|boyfriend|girlfriend|friend|mate|"
    r"neighbour|neighbor|grandad|granddad|grandma|gran|nan|nana|uncle|aunt|auntie|cousin|"
    r"colleague|flatmate|housemate|carer|teacher|boss|fella|lass|lad|family)\b")
HURT_BUT_FINE = re.compile(
    r"\bbut\s+(?:he|she|they|hes|shes|theys|it)(?:'s|\s+is|\s+was|\s+seems)?\s*"
    r"(?:ok|okay|alright|fine|good|bruised|home)\b"
    r"|\b(?:he|she|they)(?:'s|\s+is|\s+seems)\s+(?:ok|okay|alright|fine)\b"
    r"|\bnothing\s+(?:broken|serious|bad)\b|\bnot\s+(?:too\s+bad|serious)\b"
    r"|\bonly\s+(?:a\s+)?(?:bruise|scrape|scratch|graze)\b")
HURT_FIGURE = re.compile(
    r"\b(?:collapsed|fell|fall|falls)\b[^.!?]{0,12}?\b(?:laughing|about|over\s+laughing|ill|"
    r"sick\s+with\s+laughter)\b"
    r"|\b(?:fell|fallen)\s+(?:out|for|in\s+love|asleep)\b"
    r"|\b(?:knocked|blown)\s+(?:out|away)\b(?!\s+by\s+(?:a|the)\s+\w+\s*(?:car|bus))")


HURT_ON_THE_SPEAKER = re.compile(
    r"\b(?:attacked|hit|punched|stabbed|kicked|pushed|thrown|strangled|bitten|bit|beat|beaten|"
    r"burned|burnt|hurt|injured|raped)\s+me\b")


HURT_DEATH = re.compile(
    r"\b(?:died|dead|death|dying|passed\s+away|killed|kills?|funeral|buried|suicide|"
    r"took\s+(?:his|her|their)\s+own\s+life)\b")


def _somebody_hurt(clean, memory, understood):
    if understood.get("asks"):
        return None
    if _in_a_care_thread(memory):
        return None
    found = HURT_SOMEBODY.search(clean)
    if not found:
        return None
    if HURT_DEATH.search(clean):
        return None
    if not HURT_EVENT.search(clean):
        return None
    if HURT_ON_THE_SPEAKER.search(clean):
        return None
    if HURT_BUT_FINE.search(clean):
        return None
    if HURT_FIGURE.search(clean):
        return None
    who = re.sub(r"^(?:my|our)\b", "your", found.group(0))
    return _choose(tuple(line.format(who=who) for line in SOMEBODY_HURT), memory, clean)


LOW_DAY = re.compile(
    r"\b(?:low|rough|bad|rubbish|crap|hard|tough|awful|terrible|dreadful|long|heavy|rotten|flat)"
    r"\s+(?:old\s+)?(?:day|week|month|morning|afternoon|evening|night|shift)\b")
LOW_DAY_MINE = re.compile(
    r"^(?:so |and |but |ok |okay |well |god |ugh |honestly |anyway |yeah |yeh |hmm )*"
    r"(?:i\s+(?:had|have|'ve|ve)\b|ive\b|i\s*'?m\s+having\b|i\s+am\s+having\b"
    r"|we\s+(?:had|have|'ve|ve)\b|weve\b"
    r"|(?:kind\s+of\s+|sort\s+of\s+|bit\s+of\s+|such\s+an?\s+)?a\b"
    r"|(?:today|yesterday|this\s+(?:morning|afternoon|evening|week))\s+(?:was|has\s+been|is)\b"
    r"|really\b|such\s+an?\b|what\s+an?\b"
    r"|(?:low|rough|bad|rubbish|crap|hard|tough|awful|terrible|dreadful|long|heavy|rotten|flat)"
    r"\s+(?:old\s+)?(?:day|week|month|morning|afternoon|evening|night|shift)\b)")
LOW_DAY_NOT_MINE = re.compile(
    r"\b(?:he|she|they|it)\s+(?:had|has|was|is)\b"
    r"|\b(?:my|his|her|their|your)\s+(?!day\b|week\b|month\b|morning\b|night\b|evening\b)\w+"
    r"\s+(?:had|has|was|is)\b"
    r"|\bthe\s+\w+\s+had\b")


def _a_low_day(clean, understood):
    if (understood or {}).get("kind") == "question":
        return False
    if LOW_DAY_NOT_MINE.search(clean):
        return False
    if "," in clean or " because " in clean or " cos " in clean:
        return False
    return bool(LOW_DAY.search(clean)) and bool(LOW_DAY_MINE.match(clean))


LOVE_ONE = (r"(?:mum|mom|mam|mother|dad|father|nan|nana|gran|granny|grandma|grandad|grandpa|"
            r"sister|brother|son|daughter|kid|child|wife|husband|partner|girlfriend|boyfriend|"
            r"fiance|fiancee|fiancé|fiancée|stepmum|stepmom|stepdad|stepson|stepdaughter|"
            r"mother[- ]in[- ]law|father[- ]in[- ]law|son[- ]in[- ]law|daughter[- ]in[- ]law)")
LOVE_GROUP = (r"(?:kids|children|family|families|parents|grandparents|grandkids|"
              r"grandchildren|siblings|brothers|sisters|boys|girls|aunts|aunties|uncles|"
              r"cousins|nieces|nephews|stepchildren|stepkids|in[- ]laws|friends|mates)")
LOVE_PERSON = r"(?:" + LOVE_ONE + r"|" + LOVE_GROUP + r")"
LOVE_OPENER = (r"^(?:oh |aw+ |ah |ha+ |lol |tbh |honestly |ok |okay |well |and |but |so )*"
               r"(?:i|we)(?: really| just| absolutely| so| still| do| totally| truly)?"
               r" love (?:my|our) ")
LOVE_TAIL = (r"(?: (?:so much|lots|loads|to bits|to pieces|more than anything|really|tbh|"
             r"honestly|though|tho|too|also))*[.!]*$")
LOVES_SOMEONE = re.compile(LOVE_OPENER + LOVE_ONE + LOVE_TAIL)
LOVES_A_GROUP = re.compile(LOVE_OPENER + LOVE_GROUP + LOVE_TAIL)
LOVES_PEOPLE = re.compile(
    LOVE_OPENER + LOVE_PERSON
    + r"(?: (?:and|&|n) (?:my |our |the )?" + LOVE_PERSON + r")+" + LOVE_TAIL)
LOVE_START = re.compile(LOVE_OPENER + LOVE_PERSON + r"(?:[ ,'-]+[a-z0-9][^?.!]{0,60})?[.!]*$")


def _loves_people(clean):
    if "?" in (clean or ""):
        return 0
    text = (clean or "").strip()
    if " but " in " " + text + " " or " though " in " " + text + " ":
        return 0
    if LOVES_A_GROUP.match(text) or LOVES_PEOPLE.match(text):
        return 2
    if LOVES_SOMEONE.match(text):
        return 1
    if LOVE_START.match(text) and not re.search(
            r"\b(?:mum|mom|dad|nan|gran|sister|brother|kid|child|parent|family)'?s\b"
            r"|\band (?:my|our|his|her|their)\b", text):
        return 1
    return 0


def _loves_someone(clean):
    return bool(_loves_people(clean))
A_CLOCK = (
    r"(?:\d{1,2}(?:[:.]\d{2})?\s*(?:am|pm)|"
    r"(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\s*(?:am|pm)|"
    r"(?:\d{1,2}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\s*o'?clock|"
    r"half\s+(?:one|two|three|four|five|six|seven|eight|nine|ten))")
A_TIME_SAID = re.compile(
    r"\b(?:at|by|for|before|around|about|until|till|from)\s+"
    r"(\d{1,2}[:.]\d{2}\s*(?:am|pm)?|" + A_CLOCK + r"|\d{1,2}|"
    r"one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\b",
    re.I)
CLOCK_THE_DEPARTURE = re.compile(
    r"\bthe\s+(\d{1,2}[:.]\d{2}\s*(?:am|pm)?|\d{1,2}\s*(?:am|pm)|half\s+past\s+"
    r"(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve))\s+"
    r"(?:train|flight|bus|coach|ferry|boat|tram|tube|plane)\b", re.I)
CLOCK_SHAPE = re.compile(
    r"\b(?:need|needs|needed|have|has|had|got|must|ought)\s+(?:to\s+)?"
    r"(?:be|get|leave|head|go|catch|make)\b"
    r"|\b(?:train|flight|bus|coach|ferry|boat|taxi|shift|meeting|work|check-?in)\s+"
    r"(?:is|are|starts?|leaves?|departs?|takes?\s+off|begins?|kicks?\s+off)?\b"
    r"|\b(?:be|get|wake)\s+up\b|\bset\s+(?:the|my|an)\s+alarm\b")
A_LENGTH = re.compile(
    r"^\s*(?:hours?|hrs?|minutes?|mins?|days?|weeks?|months?|years?|miles?|km|kms|"
    r"people|quid|pounds|kilos?|kg|st[o]?ne|times|of\s+them|more|less)\b")
CLOCK_NOT_THIS = re.compile(
    r"\b(?:was|were|been|missed|lost|yesterday|last\s+night|this\s+morning|cancelled|"
    r"canceled|used\s+to|usually|always|every\s+day)\b")
CLOCK_ASKED = re.compile(
    r"^\s*(?:what|when|how|which|why|who|should|shall|can|could|would|do|does|did|is|are|"
    r"was|were|have|has|any|is\s+it)\b")
CLOCK_ABOUT_THE_JOB = re.compile(
    r"\b(?:im|i'm|i am)\s+an?\b|\bi\s+work\s+as\b|\bmy\s+job\b|\bmy\s+shift\s+pattern\b")
CLOCK_SOMEONE_ELSE = re.compile(
    r"\b(?:my|our|his|her|their)\s+(?:mum|mom|mam|mother|dad|father|wife|husband|partner|"
    r"boyfriend|girlfriend|son|daughter|child|kid|brother|sister|nan|nana|gran|granny|"
    r"grandma|grandad|grandpa|aunt|uncle|cousin|niece|nephew|friend|mate|neighbour|neighbor|"
    r"colleague|boss)\b")
AT_THE_CLOCK = (
    "Work it back from {at}: the journey, then getting ready, then ten minutes spare. What is "
    "the trip like at that hour?",
    "{At} gives you a time to work back from. How long does the journey take from yours?",
    "Count backwards from {at} and set the alarm by the time you have to walk out. What has to "
    "happen before you get out of the door?",
    "The leaving time is the thing to fix for {at}, not the arriving one. How long does it take "
    "from yours?",
    "{At} is a timetable rather than a rush, as long as the leaving time is right. Where are you "
    "travelling from?",
)


def _the_clock_pool(at):
    at = (at or "").strip()
    if not at:
        return AT_THE_CLOCK
    return tuple(line.format(at=at, At=at[:1].upper() + at[1:]) for line in AT_THE_CLOCK)


def _the_time_said(clean):
    return A_TIME_SAID.search(clean) or CLOCK_THE_DEPARTURE.search(clean)

def _the_morning_has_a_clock(clean):
    if "?" in clean or CLOCK_ASKED.match(clean):
        return False
    if CLOCK_NOT_THIS.search(clean) or CLOCK_SOMEONE_ELSE.search(clean):
        return False
    if CLOCK_ABOUT_THE_JOB.search(clean):
        return False
    said = _the_time_said(clean)
    if not said:
        return False
    if A_LENGTH.match(clean[said.end():]):
        return False
    return bool(CLOCK_SHAPE.search(clean) or said.re is CLOCK_THE_DEPARTURE)


def reply_for(text, memory, verdict=True):
    if verdict and isinstance(memory, dict):
        alone = (ack.a_person_named_alone(_matchable(text), memory)
                 or ack.a_person_pointed_at(_matchable(text), memory))
        if alone:
            return alone
    said = _reply_for(text, memory, verdict=verdict)
    if verdict and said and is_a_hedge(said):
        clean = _matchable(text)
        pool = _a_verdict_on_their_plan(clean, memory, past_a_question=True)
        if pool:
            return _choose(pool, memory, clean)
    if verdict and said:
        from . import fallback as composer
        if (composer.nothing_said_yet(memory)
                and composer.brings_nothing_of_its_own(text)
                and composer.assumes_an_earlier_turn(said)):
            return _choose(composer.NOTHING_SAID_YET, memory, _matchable(text))
    return said


OPTION_ON_THE_TABLE = re.compile(r"\b(?:or|either)\b")

def _options_already_up(memory):
    if not isinstance(memory, dict):
        return False
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)][-2:]
    for turn in turns:
        said = str(turn.get("bot") or "")
        asked = str(turn.get("user") or "")
        if len(OPTION_ON_THE_TABLE.findall(said.lower())) or " or " in asked.lower():
            return True
    return False



def _reads_value(pred, clean, repaired, memory=None):
    found = pred(clean) if memory is None else pred(clean, memory)
    if found or not repaired or repaired == clean:
        return found
    return pred(repaired) if memory is None else pred(repaired, memory)

COUNTDOWN_ASK = re.compile(
    r"(?<![a-z])(?:how long|how many (?:days|weeks|months|sleeps|more days)|how much longer|"
    r"how far away)(?![a-z])")
COUNTDOWN_TO = re.compile(r"(?<![a-z])(?:till|til|until|before|away|to go)(?![a-z])")
COUNTDOWN_AFTER_CARE = (
    "{count} That is a while to be counting towards, and you don't have to get through it on "
    "your own - what is tonight like?",
    "{count} If there is something about that date you are counting towards, say what it is and "
    "we'll take it a day at a time.",
    "{count} A long stretch of days is hard to carry on your own. Who knows how you are doing "
    "tonight?",
)


COUNTED = re.compile(
    r"^(?:that's |that is |it's |its )?(?:about |around |just |nearly |only |almost |another )?"
    r"(?:\d|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|"
    r"fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|a hundred)")


def _a_countdown_in_a_care_thread(memory, clean, repaired, understood):
    from ..memory.topics import in_a_safety_thread
    if not in_a_safety_thread(memory):
        return None
    said = " ".join(str(repaired or clean or "").lower().split())
    if not COUNTDOWN_ASK.search(said) or not COUNTDOWN_TO.search(said):
        return None
    from ..knowledge.maths import solve
    reading = {"clean": said, "words": said.split(), "kind": "question"}
    count = solve(said, reading, {})
    if not isinstance(count, str) or not count.strip():
        return None
    if not COUNTED.match(count.strip().lower()):
        return None
    count = count.strip().rstrip(".") + "."
    return _choose(tuple(line.format(count=count) for line in COUNTDOWN_AFTER_CARE),
                   memory, clean)


def _reply_for(text, memory, understood=None, verdict=True):
    if understood is None:
        understood = memory.get("understood")
    if not isinstance(understood, dict):
        understood = understand(text, memory)
    state = memory.setdefault("compose", {})
    was_taste = bool(state.get("taste"))
    state["taste"] = False
    kind = understood.get("kind") or "statement"
    words = understood.get("words") or []
    clean = understood.get("clean") or " ".join(text.lower().split())
    counted = _a_countdown_in_a_care_thread(memory, clean, text, understood)
    if counted:
        return counted
    after = _after_safety(memory, clean, understood)
    if after:
        return after
    from . import childwords
    if childwords.asks_the_words_for_a_child(text or clean, memory):
        return _choose(childwords.THE_WORDS_FOR_A_CHILD, memory, clean)
    from . import talktime
    at_a_time = talktime.answer_for(clean, memory)
    if at_a_time:
        return at_a_time

    if morning_after.reads_as_a_morning_after(clean):
        return _choose(morning_after.A_MORNING_AFTER, memory, clean)

    hurt = _somebody_hurt(clean, memory, understood)
    if hurt:
        return hurt
    if not _a_care_thread_to_leave_alone(memory):
        safety_ask = safetyask.reply_for(clean, memory)
        if safety_ask:
            return _choose(safety_ask, memory, clean)
    if HANDS_IT_BACK.match(clean) and not _options_already_up(memory):
        return _choose(HANDS_BACK, memory, clean)
    returned = reads_as_a_return(clean)
    if returned is not None and not _came_back(clean) and not _grief_thread(memory):
        if returned:
            return _choose(RETURNED_TO_A_THING, memory, clean).format(thing=returned)
        if not _a_chat_behind_it(memory):
            return _choose(RETURNED_TO_IT_FIRST, memory, clean)
        return _choose(RETURNED_TO_IT, memory, clean)
    drafted = _named_draft(memory, text, words, clean)
    if drafted:
        return drafted
    if understood.get("agreement"):
        return _choose(AGREEMENT, memory, clean)
    if understood.get("tight_on_money"):
        pool = TIGHT_MONEY
        if understood.get("amount_left"):
            pool = tuple(line for line in pool if "what's left" not in line.lower())
        return _choose(pool, memory, clean)
    if a_continuation_of_the_tight_week(memory, clean):
        return _choose(TIGHT_MONEY_MORE, memory, clean)
    if _a_low_day(clean, understood):
        return _choose(LOW_DAY_REPLIES, memory, clean, seed_text=text)
    if HAND_BACK.match(_self_line(text)) and (memory or {}).get("turns"):
        return _choose(HOW_ARE_YOU, memory, clean, seed_text=text)
    verdict = _verdict_pool(clean, memory) if verdict else None
    if verdict and in_a_safety_thread(memory):
        verdict = None
    elif verdict and a_happening_now(memory):
        verdict = None
    elif verdict and a_loss_in_the_thread(memory):
        verdict = _the_heavy_pool(memory)
    tried_reply = None if verdict else _after_advice(memory, clean, words)
    if tried_reply:
        return tried_reply
    refused = _a_refusal_to_answer(clean, memory, words)
    if refused:
        return _choose(refused, memory, clean, seed_text=the_advice(memory) or clean)
    doable = _a_doable(clean, memory)
    if doable:
        return doable
    if verdict:
        return _choose(verdict, memory, clean)
    answered = answer_reaction.reply_for(clean, memory) if isinstance(memory, dict) else None
    if answered:
        return answered
    reaction = _reaction_pool(clean, memory)
    if reaction is REACTION_REPEAT:
        again = why.said_again(clean, memory) if isinstance(memory, dict) else None
        if again:
            return again
    if reaction and not _a_care_thread_to_leave_alone(memory):
        if _the_person_already_said_it(memory):
            reaction = REACTIONS_SAID.get(reaction, reaction)
        return _choose(reaction, memory, clean)
    if reaction and _a_care_thread_to_leave_alone(memory) and reaction is not REACTION_REPEAT:
        return _choose(REACTIONS_CARE, memory, clean)
    the_day = _the_day_described(clean)
    if the_day and not in_a_safety_thread(memory) \
            and not _a_care_thread_to_leave_alone(memory) \
            and not _the_turn_before_was_a_heavy_one(memory, clean):
        return _choose(the_day, memory, clean)
    if words and len(words) <= 6 and FLAT_LINE.match(" ".join(words)):
        return _choose(FLAT, memory, clean)

    view = _the_view_asked_for(clean, memory)
    if view:
        return view
    no_words = _no_words(clean)
    if no_words:
        return _choose(no_words, memory, clean)

    if kind == "thanks" and "?" in text:
        kind = "question"
    asks_for_help = _asks_for_help(_plain(clean), understood)
    opens_with_hello = kind == "statement" and _reads_as_greeting(words, text) \
        and not _reads_as_question(text, words)
    if opens_with_hello and not asks_for_help \
            and (greeting_only(words) or understood.get("intent") == "request"):
        kind = "greeting"
    if kind == "empty":
        return _choose(EMPTY, memory, clean)
    if kind == "greeting" and not asks_for_help:
        return _choose(GREETING, memory, clean)
    if kind == "thanks":
        if _thanks_news_went_badly(clean):
            return _choose(THANKS_NO_BETTER, memory, clean)
        bye = leaving.pool(clean, words, memory=memory)
        if bye:
            return _choose(bye, memory, clean)
        return _choose(THANKS, memory, clean)
    loved = _loves_people(clean)
    if kind != "question" and loved:
        return _choose(A_LOVE_FOR_PEOPLE if loved > 1 else A_LOVE_FOR_SOMEONE,
                       memory, clean)

    going_on = handoff.reply_for(clean, memory)
    if going_on:
        return going_on

    restated = "" if memory.get("correction_answered") else _restated(understood)
    if restated:
        reply = _answers_the_correction(restated, memory)
        if reply:
            return reply

    corrected = ack.value_put_right(clean, memory)
    if corrected:
        return corrected
    wondered = ack._a_condition_they_wonder_about(clean, memory)
    if wondered:
        return wondered
    plain = _plain(clean)
    repaired = understood.get("plain") or clean
    if _is_presence_check(clean):
        return _choose(PRESENT, memory, clean)

    if _a_declined_plan(plain) and not draft.drafter(memory, clean):
        if _a_hard_week(memory):
            return _choose(DECLINED_PLAN_GENTLE, memory, clean)
        if _the_turn_before_was_a_heavy_one(memory, plain):
            pass
        elif _someone_else_dropped_it(plain):
            return _choose(PLAN_KNOCKED, memory, clean)
        else:
            return _choose(DECLINED_PLAN, memory, clean)

    help_topic = _help_topic(clean, understood)
    if help_topic:
        return _choose(help_topic, memory, clean)

    leaning = _a_leaning_side(plain, memory)
    if leaning:
        return leaning
    mine = _my_pick(plain, memory)
    if mine:
        return mine
    verdict = _a_verdict_on_their_plan(plain, memory)
    if verdict:
        return _choose(verdict, memory, clean)
    place_ask = _a_place_asked_about(plain, memory)
    if place_ask:
        return _choose(place_ask, memory, clean)

    saying_ask = why.respond_to_a_saying_ask(clean, memory, understood,
                                             body=_thread_is_about_the_body(memory))
    if saying_ask:
        return saying_ask

    about = _about(plain, understood)
    if about in ("self_doing", "clothes") and ANSWERING_A_QUOTED_ASK.search(clean or "") \
            and _the_answers_take_it(clean or ""):
        about = None
    if about == "memory" and _a_tally_of_its_own_day(understood):
        return _choose(ABOUT_TALLY, memory, clean)
    if about == "hand":
        return _choose(HAND, memory, clean)
    if about in ABOUT:
        return _choose(ABOUT[about], memory, clean)
    if about:
        return _choose(ABOUT_SELF[about], memory, clean)

    awkward = _their_own_slip(clean, memory)
    if awkward:
        said = _choose(awkward, memory, clean)
        if said is None:
            said = _choose(EMBARRASSED if awkward is LAUGHED_AT else LAUGHED_AT, memory, clean)
        if said:
            return said

    if SELF_SUBJECT.search(clean) and not SELF_BLAME_ASKS.search(clean) \
            and not WORDING_ASKS.search(clean) and not RATES_A_SKILL.search(clean) \
            and not _own_feeling(clean):
        return _choose(SELF_BLAME, memory, clean)

    asking = kind == "question" or (kind == "statement" and (
        _reads_as_question(text, words)
        or (repaired != clean and _reads_as_a_question_when_repaired(repaired))))
    if asking and _thanks_then_said(clean):
        asking = False
    if asking and _acknowledges_alone(clean):
        asking = False

    action = _action(clean, memory)
    if action:
        return action
    if WOULD_HAVE_BEEN.search(clean):
        return _choose(MILESTONE, memory, clean)

    bye = leaving.pool(clean, words, memory=memory)
    if bye:
        return _choose(bye, memory, clean)
    if leaving.reads_as_a_leave_with_a_body_in_it(clean, words):
        bye = leaving.pool(clean, words, unwell_blocks=False, memory=memory)
        if bye:
            return _choose(bye, memory, clean)

    asks_for_words = _asks_for_words(clean, words) or (
        repaired != clean and _asks_for_words(repaired, words))
    if WORDING_ASKS_WHO.search(clean) and any(w in EXPERT_WORDS for w in words):
        asks_for_words = True
    if QUOTE_ASKS.search(clean):
        return _choose(QUOTE_LINES, memory, clean)
    if asks_for_words:
        if TELL_HARD.search(clean):
            return _choose(TELL_HARD_LINES, memory, clean)
        if "card" in words:
            return _choose(CARD_LINES, memory, clean)
        return _choose(WORDING_LINES, memory, clean)
    if _asks_how_are_you(plain, understood.get("plain") or "") \
            or understood.get("asks_how_i_am"):
        return _choose(HOW_ARE_YOU, memory, clean)
    taste = _taste(plain, memory, was_taste, asking, repaired)
    if taste:
        state["taste"] = True
        return taste
    number = _their_contact_number(plain, asking)
    if number:
        return _choose(number, memory, clean)
    if _a_no_from_the_bot(plain):
        cannot = _live(plain, True, memory) or _the_live_thing_named(plain)
        if cannot:
            return _choose(cannot, memory, clean)
        if CANNOT_SEE_ANYTHING.search(plain):
            return _choose(CANNOT_SEE_ANYTHING_LINES, memory, clean)
        if CANNOT_READ_YOURS.search(plain):
            return _choose(_what_no_eyes_already_says(plain) or CANNOT_YOUR_OWN, memory, clean)
        if SO_NOTHING_LIVE.search(plain) or (
                _the_bot_says_it_cannot(plain) and CANNOT_ANYTHING_ASK.search(plain)):
            return _choose(CANNOT_ANYTHING, memory, clean)
    live = _live(plain, asking, memory)
    if live:
        return _choose(live, memory, clean)
    if loss.found_what_was_lost(clean) and loss.lost_thing_to_find(last_user(memory) or ""):
        return _choose(FOUND_IT, memory, clean)
    if loss.locked_out(clean):
        if loss.locked_out_of_the_car(clean):
            return _choose(LOCKED_OUT_OF_THE_CAR, memory, clean)
        return _choose(LOCKED_OUT_LINES, memory, clean)
    if loss.keeps_losing_thing(clean):
        return _choose(LOST_A_THING_AGAIN, memory, clean)
    if loss.lost_thing_to_find(clean):
        return _choose(LOST_A_THING, memory, clean)
    if unseen.reads(clean):
        return _choose(unseen.LINES, memory, clean)
    own = _own_feeling(clean) or (
        NO_DIRECTION_REPLY if LOST_QUESTION.search(clean) and not NOT_SELF.search(clean) else None)
    if own:
        return _choose(own, memory, clean)
    routine = _routine_pool(clean, words, memory)
    if routine:
        return _choose(routine, memory, clean)
    if (I_RATE_A_SKILL.search(clean) and not WORDING_ASKS.search(clean)
            and not A_WAY_OF_BEING.search(clean)):
        return _choose(ONE_SKILL_RATED, memory, clean)
    if not SELF_BLAME_ASKS.search(clean):
        if A_SKILL_ASKED_OF_ME.search(clean) and not A_WAY_OF_BEING.search(clean):
            return _choose(ASKED_A_RATING, memory, clean)
        if A_GOODNESS_ASKED_OF_ME.search(clean):
            return _choose(ASKED_IF_GOOD, memory, clean)

    why_follow_up = why.respond(clean, memory, understood,
                                body=_thread_is_about_the_body(memory))
    if why_follow_up:
        return why_follow_up
    asked = _act_asked_of_me(clean)
    if asked:
        return _choose(asked, memory, clean)
    if _acts_for_me(clean, memory):
        return _choose(ACTS_FOR_ME, memory, clean)
    ordered = _an_order_it_cannot_do(clean)
    if ordered:
        return _choose(ordered, memory, clean)


    if reads_like_a_symptom(repaired.lower()) and _LUMP.search(repaired):
        return _choose(LUMP, memory, clean)
    settled = " " + re.sub(r"[^a-z0-9']", " ", clean) + " "
    if (reads_like_a_symptom(repaired.lower())
            and not _who_for(clean, settled, settled.replace("'", "").split())
            and not (trouble.reads_as_trouble(clean, words, repaired) == "sore"
                     and not _CAUGHT.search(clean))
            and says_it_has_lingered(repaired, illness=bool(_ILL.search(repaired)))):
        return _choose(SYMPTOM_LINGERS, memory, clean)
    if (asking and reads_like_a_symptom(repaired.lower())
            and not _who_for(clean, settled, settled.replace("'", "").split())
            and not (trouble.reads_as_trouble(clean, words, repaired) == "sore"
                     and not _CAUGHT.search(clean))):
        return _choose(SYMPTOM_COLD if _ILL.search(repaired) else SYMPTOM, memory, clean)
    if _a_lateness_report(clean, (understood or {}).get("norm_text") or ""):
        pool = (LATE_BEHIND_LINES
                if "behind" in clean or "behind" in ((understood or {}).get("norm_text") or "")
                else LATE_NOW_LINES)
        return _choose(pool, memory, clean)

    invited = _an_invitation(clean)
    if invited == "talk":
        return _choose(INVITED_TO_TALK, memory, clean)
    if invited:
        return _choose(INVITED, memory, clean)
    limits = the_limits_said(clean) or [(reads_as_a_narrowing(clean), "")]
    for axis, part in limits:
        if not axis or not the_answer_to_cut(memory, axis):
            continue
        bound = the_bound_said(part or clean)
        if bound:
            return _choose(BOUND_FOR[axis], memory, clean).format(bound=bound)
        return _choose(CUT_FOR[axis], memory, clean)

    refused = _a_carer_refused(clean) or _a_carer_refused(repaired)
    if (refused and not _hedged_recently(memory)
            and not (_in_a_loss_thread(memory) or _grief_thread(memory)
                     or in_a_safety_thread(memory))):
        pool = {"aid": ELDER_AID_REPLIES, "clinic": ELDER_CLINIC_REPLIES,
                "doctor": ELDER_DOCTOR_REPLIES, "help": ELDER_HELP_REPLIES}[refused]
        said_before = str((memory.get("turns") or [{}])[-1].get("bot") or "")
        if not _in_a_pool(said_before, (ELDER_AID_REPLIES, ELDER_CLINIC_REPLIES,
                                        ELDER_DOCTOR_REPLIES, ELDER_HELP_REPLIES,)):
            return _choose(pool, memory, clean, clean + " " + _the_line_before(memory))

    handed = no_eyes.handed_you_something(clean)
    if handed:
        return _choose(handed, memory, clean)

    body_lines = no_eyes.look_at_a_body_lines(clean, None, memory)
    if body_lines:
        return _choose(body_lines, memory, clean)
    cannot_see = no_eyes.cannot_see_your_thing(clean)
    if cannot_see:
        return _choose(cannot_see, memory, clean)

    if _am_i_a_nuisance(clean) and not _grief_thread(memory) and not in_a_safety_thread(memory):
        return _choose(SORRY_FOR_ASKING, memory, clean)

    if asking and not _takes_something_back(clean, memory):
        if reads_as_no_pleasure(clean) or (repaired and reads_as_no_pleasure(repaired)):
            return _choose(PLEASURE_GONE_LINES, memory, clean)
        step = step_when_low(clean, memory, COMFORT_SAID)
        if step:
            return step
        if reads_as_a_question_about_the_bot(clean) or reads_as_a_question_about_the_bot(repaired):
            return _choose(ABOUT_THE_BOT_LINES, memory, clean)
        unknown = _unknown(understood, memory, clean)
        if _a_wear_ask_about_a_day(clean, repaired, text) and is_a_hedge(unknown):
            return _choose(_the_wear_pool_for_the_line(clean, repaired, text), memory, clean)
        return unknown

    drafted = draft.drafter(memory, text, words)
    if drafted:
        return _choose([f'{lead} "{drafted}"' for lead in draft.LEAD_INS], memory, clean)
    if draft.not_the_message(memory, text):
        return _choose(draft.NOT_YET, memory, clean)

    if _reads(reads_as_pregnancy_bleeding, clean, repaired):
        return _choose(PREGNANCY_BLEEDING, memory, clean)
    if a_fresh_death_and_the_words(clean):
        return _choose(THE_FIRST_HOUR_AND_A_CHILD, memory, clean)
    if _reads(reads_as_sudden_loss, clean, repaired):
        return _choose(SUDDEN_LOSS, memory, clean)
    if _reads(reads_as_recovery, clean, repaired, lower=True) and not _in_a_loss_thread(memory):
        return _choose(RELIEF, memory, clean)
    if _reads(reads_as_a_clear_result, clean, repaired, lower=True) and not _in_a_loss_thread(memory):
        return _choose(RELIEF, memory, clean)
    if (reads_as_settled(clean.lower()) and worry_on_the_table(memory)
            and not _in_a_loss_thread(memory)):
        return _choose(RELIEF, memory, clean)
    if _reads(reads_as_a_closed_door, clean, repaired):
        return _choose(CLOSED_DOOR, memory, clean)
    if _came_back(clean) and in_a_safety_thread(memory):
        return _choose(PAUSE_IN_A_SAFETY_THREAD, memory, clean)
    if _came_back(clean) and not _grief_thread(memory):
        return _choose(CAME_BACK, memory, clean)
    if (_reads(reads_as_the_leaving, clean, repaired)
            and not _reads(reads_as_the_speakers_own_plan, clean, repaired)
            and not _a_things_state(memory, clean)):
        return _choose(
            LEFT_POOL_GONE if reads_as_a_leaving_already_gone(clean) else LEFT_POOL,
            memory, clean)
    situation = circumstance.pool(clean)
    if situation:
        return _choose(situation, memory, clean)
    broken_into = remark.break_in_reply_for(clean, words, memory)
    if broken_into:
        return broken_into
    if (_reads(reads_as_bad_news, clean, repaired)
            and not _reads(reads_as_the_speakers_own_plan, clean, repaired)
            and not PLAN_IDIOM.search(clean)
            and not (_reads(reads_as_an_award_lost, clean, repaired)
                     and who_settles(clean, memory))):
        if _a_things_state(memory, clean):
            return _choose(A_THING_LOOKS_SAD, memory, clean)
        if _reads(reads_as_the_leaving, clean, repaired):
            return _choose(
                LEFT_POOL_GONE if reads_as_a_leaving_already_gone(clean) else LEFT_POOL,
                memory, clean)
        if remark.reads_as_report(clean, words) == "again":
            again = remark.report_reply_for(clean, words, memory)
            if again:
                return again
        if not asking and _reads(reads_as_someone_close_is_ill, clean, repaired):
            return _choose(SOMEONE_SERIOUSLY_ILL, memory, clean)
        pool = NAMED_NEGATIVE if _reads(reads_as_news_with_a_name, clean, repaired) else NEGATIVE
        return _choose(pool, memory, clean)
    if (not asking
            and not _in_a_loss_thread(memory)
            and _reads(LEAVING_A_PERSON.search, clean, repaired)
            and _reads(LEFT_BEHIND.search, clean, repaired)
            and not _reads(NOT_LEAVING_ANYONE.search, clean, repaired)):
        is_a_child = _reads(A_CHILD.search, clean, repaired)
        has_happened = _reads(THE_LEAVE_HAS_HAPPENED.search, clean, repaired)
        if has_happened:
            pool = A_CHILD_LEFT if is_a_child else SOMEONE_GONE
        else:
            pool = _only_what_the_line_gives(
                A_CHILD_LEAVING if is_a_child else SOMEONE_LEAVING, clean)
        return _choose(pool, memory, clean)
    if _reads(ack.COMPLAINT.search, clean, repaired):
        if _a_things_state(memory, clean):
            return _choose(A_THING_LOOKS_SAD, memory, clean)
        return _choose(NEGATIVE, memory, clean)

    if (_asks_the_bot(understood) and not _takes_something_back(clean, memory)
            and not _reads_value(_a_good_time, clean, repaired, memory)
            and not _reads(reads_as_a_win_nobody_noticed, clean.lower(), repaired.lower())
            and not _a_good_time(clean, memory)
            and not (_reads_as_dither(clean, repaired) and _weighs_a_choice(clean))
            and not _a_dead_end(clean) and not _the_person_they_are_stuck_on(clean)
            and not _acknowledges_alone(clean)):
        tips = _tips(memory, clean, repaired)
        if tips:
            return tips
        free_time = _the_stretch_of_time(clean, memory)
        if free_time:
            return free_time
        lost = the_lost_ask_reply(memory, clean, repaired)
        if lost:
            return lost
        pool = unknown_pool(clean, words)
        if pool is UNKNOWN_WORD:
            from .fallback_pools import _drafting_pool
            return _choose(_drafting_pool(clean), memory, clean)
        routed = finding_out.for_the_ask(clean, repaired, understood)
        if routed:
            said = _choose(routed, memory, clean)
            if said:
                return said
        if _a_wear_ask_about_a_day(clean, repaired, text):
            return _choose(_the_wear_pool_for_the_line(clean, repaired, text), memory, clean)
        return _choose(UNKNOWN, memory, clean)
    if _reads(_is_a_tips_ask, clean, repaired):
        tips = _tips(memory, clean, repaired)
        if tips:
            return tips
        return _choose(TIPS_LINES, memory, clean)
    told = _trouble(memory, repaired, words)
    if told:
        return told

    if (asks_for_more(clean, memory) and not _hedged_recently(memory)
            and _answered_recently(memory)):
        return _choose(HELP_ALREADY, memory, clean)
    if _in_sudden_loss_thread(memory):
        return _choose(loss.AFTER_REPLIES, memory, clean)
    if len(words) <= 2 and set(words) & ACKS:
        if _a_loss_recently(memory):
            return _choose(loss.AFTER_REPLIES, memory, clean)
        if _the_last_line_was_bad_news(memory):
            return _choose(loss.AFTER_REPLIES, memory, clean)
        if _the_last_line_was_a_fault(memory):
            return _choose(ACK_AFTER_TROUBLE, memory, clean)
        if _the_last_line_was_heavy(memory):
            return _choose(ACK_WARM, memory, clean)
        return _choose(ACK, memory, clean)
    if not _in_a_loss_thread(memory):
        if FORGETS_A_CLASH.search(plain):
            return _choose(DOUBLE_BOOKED, memory, clean)
        if FORGET_A_DATE.search(plain):
            return _choose(DATES_KEEP_SLIPPING, memory, clean)
        if FORGET_A_SECRET.search(plain):
            return _choose(SECRETS_KEEP_SLIPPING, memory, clean)
    if FORGETS_AGAIN.search(plain) and not _in_a_loss_thread(memory):
        return _choose(KEEPS_FORGETTING, memory, clean)
    if _is_rumination(clean):
        return _choose(RUMINATION_REPLIES, memory, clean)
    mood = _mood(words, clean)
    carried = trouble.carried_on(clean, words, memory)
    if carried:
        return _choose(carried, memory, clean)
    if _a_near_miss(clean):
        return _choose(NEAR_MISS_REPLY, memory, clean)
    if mood == "neutral" and repaired and repaired != clean:
        mood = _mood(_words(repaired), repaired)
    if mood != "positive" and _reads(reads_for_a_pet, clean.lower(), repaired.lower()):
        if _reads(reads_as_a_pet_low, clean.lower(), repaired.lower()):
            return _choose(PET_LOW_REPLY, memory, clean)
        condition = _reads(reads_as_a_pet_condition, clean.lower(), repaired.lower())
        return _choose(PET_CONDITION_TROUBLE if condition else PET_TROUBLE, memory, clean)
    if mood != "positive" and _reads(reads_as_a_carer_body, clean.lower(), repaired.lower(),
                                     memory=memory):
        return _choose(CARING_FOR_A_BODY, memory, clean)
    if mood != "positive" and _reads(reads_for_a_carer, clean.lower(), repaired.lower(),
                                     memory=memory):
        return _choose(CARING, memory, clean)
    if (mood == "neutral" and _reads(reads_like_a_symptom, clean.lower(),
                                     repaired.lower())
            and not (trouble.reads_as_trouble(clean, words, repaired) == "sore"
                     and not _CAUGHT.search(clean))):
        return _choose(SYMPTOM_COLD if _ILL.search(repaired) else SYMPTOM, memory, clean)
    if _a_relationship_ending(clean):
        return _choose(RELATIONSHIP_DECISION, memory, clean)
    if a_comparison_of_standing(clean) and not _in_a_loss_thread(memory):
        return _choose(A_COMPARISON_OF_STANDING, memory, clean)
    if (mood != "negative" and not a_limit_on_the_answer(clean)
            and _something_funny(clean, memory)):
        return _choose(A_LAUGH, memory, clean)
    if not _in_a_care_thread(memory) and _the_crowd_is_ahead(clean):
        return _choose(A_CROWD_AHEAD, memory, clean)
    if mood != "negative" and _reads_value(_a_good_time, clean, repaired, memory):
        if _in_a_care_thread(memory):
            return _choose(A_GOOD_TIME_IN_A_CARE_THREAD, memory, clean)
        return _choose(A_GOOD_TIME, memory, clean)
    if mood != "negative" and _reads(reads_as_a_win_nobody_noticed, clean.lower(),
                                     repaired.lower()):
        return _choose(WIN_IN_A_SILENCE, memory, clean)
    if mood != "negative" and _reads(reads_as_a_win_a_cost_came_with, clean.lower(),
                                     repaired.lower()):
        return _choose(WIN_AND_A_COST, memory, clean)
    occasion = (reads_as_an_occasion(clean.lower())
                or (reads_as_an_occasion(repaired.lower()) if repaired != clean else None))
    if mood != "negative" and occasion:
        return _choose(_occasion_pool(occasion, clean), memory, clean)
    ahead_pool = _reads_value(_a_day_ahead, clean, repaired)
    if mood != "negative" and ahead_pool is not None:
        return _choose(ahead_pool, memory, clean)
    if mood != "negative" and _reads(reads_as_news_to_come, clean.lower(), repaired.lower()):
        birthday = _a_birthday_still_to_come(clean, memory)
        if birthday:
            return _choose(_the_birthday_said_back(birthday), memory, clean)
        return _choose(NEWS_TO_COME, memory, clean)
    if ack.a_limit_on_the_plan(clean):
        said_back = ack.a_limit_reply(text, memory)
        if said_back:
            return said_back
    if mood == "neutral" and _dreading(clean):
        return _choose(A_DREAD, memory, clean)
    if mood == "neutral" and _wants_it_over(clean):
        return _choose(A_WANT_IT_OVER, memory, clean)
    if mood != "negative" and _reads_value(_looking_forward, clean, repaired):
        return _choose(NEWS_TO_COME, memory, clean)
    if mood == "neutral" and _reads(reads_as_good_news, clean.lower(), repaired.lower()):
        return _choose(_says_only_what_they_said(CONGRATS, clean),
                       memory, clean)
    arrived = goodnews.new_thing(clean.lower())
    if arrived and mood != "negative":
        return _choose(goodnews.new_thing_replies(arrived), memory, clean)

    regretted = remark.regret_reply_for(clean, words, memory,
                                        understood.get("plain") or "")
    if regretted:
        return regretted
    idiom = PLAN_IDIOM.search(clean)
    if idiom:
        return _choose(IDIOM_SHY if "excit" not in idiom.group(0) else IDIOM_GLAD, memory, clean)
    if _plan_reported(clean, mood) and not ack.reads_as_a_trip(clean):
        if reads_as_a_change_of_medicine(clean):
            whole = (PLAN_MEDICINE_SLOW_REPLY if PLAN_MEDICINE_SLOW.search(clean)
                     else PLAN_MEDICINE_REPLY)
            return _choose(whole, memory, clean)
        if any(phrase in clean for phrase in PLAN_DONE) and not PLAN_NOT_YET.search(clean):
            return _choose(PLAN_DONE_ACK, memory, clean)
        return _choose(PLAN, memory, clean)
    promise = _a_promise_that_keeps_moving(clean)
    if promise is not None and mood != "positive":
        return _choose(promise, memory, clean)
    if mood != "positive" and _someone_else_minding(clean, words, _grievance_thread(memory)):
        if _grief_thread(memory):
            return _choose(GRIEF_AFTER, memory, clean)
        return _choose(GRIEVANCE, memory, clean)
    if mood == "neutral" and _sorry_for_asking(clean):
        return _choose(SORRY_FOR_ASKING, memory, clean)
    said = _thanks_then_said(clean)
    if _thanks_news_went_badly(clean):
        return _choose(THANKS_NO_BETTER, memory, clean)
    if said:
        said_words = re.findall(r"[a-z']+", said)
        if THANKS_GOOD_AGAIN.search(said) or (
                not THANKS_WENT_BADLY.search(said) and _mood(said_words, said) != "negative"):
            return _choose(THANKS_THEN_SAID, memory, clean)
    if mood == "neutral" and (_thanks_with_more(clean) or _acknowledges_alone(clean)):
        return _choose(THANKS, memory, clean)
    if mood == "neutral" and (DITHER.search(clean) or DITHER.search(repaired or "")) \
            and HELP_SERVICE.search(clean):
        if "vet" in clean or "vets" in clean or any(
                word in ANIMALS or word.rstrip("s") in ANIMALS for word in words):
            return VET_WHO
        return _choose(UNKNOWN_HEALTH, memory, clean)
    if mood == "neutral":
        about_a_person = _a_question_about_the_person(clean, memory)
        if about_a_person:
            return about_a_person
    free_time = _the_stretch_of_time(clean, memory)
    if free_time:
        return free_time
    if mood == "neutral" and _reads_as_dither(clean, repaired) and _weighs_a_choice(clean):
        if ((set(words) & HEALTH_WORDS and not HEALTH_MODIFIER.search(clean))
                or any(phrase in clean for phrase in CHECK_PHRASES)):
            return _choose(UNKNOWN_HEALTH, memory, clean)
        if DITHER_YES_NO.search(clean):
            return _choose(DITHER_DECIDE, memory, clean)
        if DITHER_OPEN.search(clean):
            return _choose(DITHER_OPEN_LINES, memory, clean)
        return _choose(DITHER_TWO_WAY_LINES, memory, clean)
    if mood == "neutral" and _run_out(clean) and not _in_a_care_thread(memory):
        return _choose(RUN_OUT_LINES, memory, clean)
    if mood == "neutral" and _only_the_stuck_phrase(clean) and not _in_a_care_thread(memory):
        if A_HELP_WORD.search(clean):
            return _choose(HAND, memory, clean)
        if _news_above(memory) or _a_subject_above(memory) or _a_bad_line_above(memory):
            return _choose(STUCK_AFTER_TROUBLE, memory, clean)
        if not (stuck_line.STUCK.match(clean) or _a_start_ask(clean)):
            return _choose(DITHER_OPEN_LINES, memory, clean)
    if _a_problem_stated(clean, repaired):
        return _choose(HAND, memory, clean)
    amount = quantity.reply_for(clean, memory)
    if amount:
        return amount
    named_after = _named_after_reply(clean, memory)
    if named_after:
        return named_after
    if mood == "neutral":
        own = _own_feeling(clean)
        if own:
            return _choose(own, memory, clean)
        if _a_knock_on_oneself(clean):
            return _choose(KNOCKED, memory, clean)
        if _a_knock_into_a_thing(clean):
            return _choose(WALKED_INTO_POOL, memory, clean)
        if _a_mishap(clean, words):
            return _choose(MISHAP_BACK, memory, clean)
        summons = understood.get("summons")
        if summons:
            return _choose(_summons_pool(summons, clean), memory, clean)
        taken = remark.interest_reply_for(understood.get("taking_up"), memory)
        if taken:
            return taken
        planned = remark.reply_for(clean, words, memory, understood.get("topics") or ())
        if planned:
            return planned
        arranged = remark.arranged_reply_for(clean, words, memory)
        if arranged:
            return arranged
        pool = _thing_done_pool(clean)
        if mood != "negative" and pool:
            return _choose(pool, memory, clean)
        reported = remark.report_reply_for(clean, words, memory)
        if reported:
            return reported
        if not asking and reads_as_a_flat_habit(text, understood):
            return _choose(HABIT_REPLY, memory, clean)
        together = remark.the_two_of_them(clean, memory)
        if together:
            return together
        of_theirs = remark.their_people_reply_for(clean, words, memory)
        if of_theirs:
            return of_theirs
        got_ahead = _a_thing_got_ahead(clean)
        if got_ahead:
            return _choose(got_ahead, memory, clean)
        going_on = remark.their_mood_going_on_reply_for(clean, memory)
        if going_on:
            return going_on
        mooded = remark.their_mood_with_you_reply_for(clean, words, memory)
        if mooded:
            return mooded
        wear = worn.reads_as_worn(clean, words, repaired)
        if wear:
            return _choose(worn.pool(wear), memory, clean)
        disliked = the_dislike_ask(clean, memory)
        if disliked:
            return disliked
        said_back = ack.reply(text, memory)
        if remark.a_want_said_back(said_back, clean):
            theirs = remark.dependant_want_reply_for(clean, words, memory)
            if theirs:
                return theirs
        told = _a_day_told_instead_of_the_receipt(said_back, clean, memory)
        if told:
            return told
        if said_back:
            return said_back
    if mood == "neutral":
        of_theirs = remark.their_people_reply_for(clean, words, memory)
        if of_theirs:
            return of_theirs
        if _the_morning_has_a_clock(clean):
            said = _the_time_said(clean)
            return _choose(_the_clock_pool(said.group(1) if said else ""), memory, clean)
        said_back = ack.reply(text, memory)
        if remark.a_want_said_back(said_back, clean):
            theirs = remark.dependant_want_reply_for(clean, words, memory)
            if theirs:
                return theirs
        told = _a_day_told_instead_of_the_receipt(said_back, clean, memory)
        if told:
            return told
        if said_back:
            return said_back
        shape = trouble.reads_as_trouble(clean, words, repaired)
        if shape:
            said = _choose(trouble.pool(shape, clean, memory), memory, clean)
            if said:
                return said
    if mood == "negative":
        shape = trouble.reads_as_trouble(clean, words, repaired)
        if shape == "sore" and not _CAUGHT.search(clean) and not FRIGHTENED.search(clean):
            said = _choose(trouble.pool(shape, clean, memory), memory, clean)
            if said:
                return said
    landed = None
    if not (_in_a_loss_thread(memory) or _grief_thread(memory)):
        landed = _the_news_landed(clean)
    if landed == "bad":
        return _choose(LANDED_BAD, memory, clean)
    if landed == "good":
        return _choose(_says_only_what_they_said(CONGRATS, clean), memory, clean)
    if landed == "landed":
        return _choose(PENDING_LANDED, memory, clean)
    from .toknow import ask_about_what_to_look_out_for as _ask_about

    answered = _ask_about(clean, memory)
    if answered:
        return answered
    if answered is None and _an_open_result(clean):
        if _a_time_in_it(clean):
            pool = PENDING_WAITING
        elif _a_guessed_result(clean):
            pool = PENDING_DOUBT
        else:
            pool = PENDING_WHEN
        return _choose(pool, memory, clean)
    if opens_with_hello and mood == "neutral":
        return _choose(GREETING, memory, clean)
    if _reads_as_a_bad_stretch(clean):
        return _choose(BAD_STRETCH_REPLIES, memory, clean)
    if _says_there_is_nothing_to_wear(clean, repaired, text):
        return _choose(NOTHING_TO_WEAR_REPLIES, memory, clean)
    if _a_wear_ask_about_a_day(clean, repaired, text):
        return _choose(_the_wear_pool_for_the_line(clean, repaired, text), memory, clean)
    if mood == "neutral" and not _A_CORRECTION.match(clean) and swap.rewritten(clean, memory):
        return _choose(UNKNOWN, memory, clean)
    if verdicts_a_thing(clean):
        return _choose(NEGATIVE, memory, clean)
    state = _body_state(clean)
    if not state:
        repaired = understood.get("plain") or ""
        if repaired and repaired != clean:
            state = _body_state(repaired)
    if state:
        return _choose(BODY_POOLS[state], memory, clean)
    pool = _thing_done_pool(clean)
    if mood != "negative" and pool and not _a_things_state(memory, clean):
        return _choose(pool, memory, clean)
    if mood == "negative" and _a_things_state(memory, clean):
        return _choose(A_THING_LOOKS_SAD, memory, clean)
    if (A_BIT_PAST_IT.search(clean) and _a_thing_they_started(memory)
            and not _hedged_recently(memory) and not _thread_is_about_the_body(memory)):
        return _choose(NOT_TOO_OLD if _names_their_age(clean) else NOT_FIT_ENOUGH, memory, clean)
    if leaving.reads_as_a_leave_with_a_trouble_in_it(clean, words):
        bye = leaving.pool(clean, words, trouble_blocks=False, memory=memory)
        if bye:
            return _choose(bye, memory, clean)
    if _a_cost_somebody_asks(clean):
        return _choose(A_COST_SOMEBODY_ASKS, memory, clean)
    lost = the_lost_ask_reply(memory, clean, repaired)
    if lost:
        return lost
    if RESULT_WENT_WRONG.search(clean):
        return _choose(A_THING_CAME_OUT_WRONG, memory, clean)
    if PLAN_THAT_FELL_THROUGH.search(clean):
        return _choose(A_PLAN_THAT_FELL_THROUGH, memory, clean)
    state = None if RESULT_WENT_WRONG.search(clean) or mood == "positive" else _a_state_of_theirs(clean)
    if state:
        return _choose(A_STATE_PAST if state == "then" else A_STATE_NOW, memory, clean)
    if _a_bad_time_told(clean, memory):
        return _choose(A_BAD_TIME_TOLD, memory, clean)
    if _a_day_asked_without_a_cheer(clean, memory):
        return _choose(A_DAY_ASKED_PLAIN, memory, clean)
    named = _a_name_told_reply(clean, memory)
    if named:
        return named
    suggestion = understood.get("suggestion") if isinstance(understood, dict) else None
    if suggestion and not asking:
        who = str(suggestion.get("who") or "")
        if who:
            return _choose(tuple(line.format(who=who) for line in A_SUGGESTED_BY_SOMEONE),
                           memory, clean)
        return _choose(A_SUGGESTED, memory, clean)
    if _a_thing_they_regret(clean):
        return _choose(A_THING_THEY_REGRET, memory, clean)
    if _a_betrayal(clean):
        return _choose(A_BETRAYAL, memory, clean)
    care = _a_care_home_line(understood, memory)
    if care:
        return care
    wrecked = finding_out.the_wrecked_form_reply(clean)
    if wrecked:
        said = _choose(wrecked, memory, clean)
        if said:
            return said
    sum_said = _a_sum_with_nothing_beside_it(clean, memory)
    if sum_said:
        return _choose([line.format(said=sum_said) for line in A_SUM_STATED], memory, clean)
    rest = _the_rest_of_the_day(clean, memory, mood)
    if rest is not None:
        return _choose(rest, memory, clean)
    reported = _a_report_from_elsewhere(clean)
    if reported is not None:
        return _choose(reported, memory, clean)
    if mood == "neutral" and _a_small_day(clean, memory) and not _just_asked_about_the_day(memory):
        return _choose(A_SMALL_DAY, memory, clean)
    if A_SORRY_ON_ITS_OWN.match((clean or "").strip()):
        return _choose(SORRY_ON_ITS_OWN, memory, clean)
    if A_DISMISSAL.match((clean or "").strip()):
        return _choose(NEVER_MIND, memory, clean)
    if _takes_something_back(clean, memory):
        return _choose(A_CORRECTION_TAKEN, memory, clean)
    positive = _says_only_what_they_said(POSITIVE, clean)
    if mood == "neutral":
        one_thing = onething.pool(clean, understood, memory)
        if one_thing:
            return _choose(one_thing, memory, clean)
        from . import limit as limit_line
        narrowed = limit_line.a_limit_the_reading_missed(clean, memory)
        if narrowed:
            return narrowed
    if reads_as_no_pleasure(clean):
        return _choose(PLEASURE_GONE_LINES, memory, clean)
    return _choose({"positive": positive, "negative": NEGATIVE, "neutral": NEUTRAL}[mood],
                   memory, clean)


A_REGRET_DOING = re.compile(
    r"\bi\s+(?:have\s+|had\s+)?(?:did|done|said|been|was|am|feel|felt)\s+(?:something\s+)?"
    r"(?:really\s+|so\s+|very\s+|quite\s+|a bit\s+|pretty\s+|such\s+)?"
    r"(?:stupid|dumb|thick|silly|bad|awful|terrible|horrible|horrid|wrong|mean|nasty|rude|"
    r"selfish|unfair|pathetic|useless|worthless|guilty|ashamed|judged|daft|idiotic|moronic|"
    r"embarrassing|cringe|a cow|a bitch|a jerk)\b"
    r"|\bsomething\s+(?:a\s+bit\s+|really\s+|so\s+|very\s+|quite\s+|pretty\s+|such\s+)?"
    r"(?:daft|idiotic|moronic|cringe|awkward)\b"
    r"|\b(?:did|done|made|make|said)\s+a\s+(?:really\s+|so\s+|very\s+|quite\s+|right\s+|"
    r"real\s+|proper\s+|bit\s+of\s+a\s+)?(?:stupid|daft|dumb|thick|silly|idiotic|moronic|"
    r"embarrassing|cringe|awful|terrible|bad)\s+(?:thing|things|stuff|job)\b"
    r"|\bi\s+(?:have\s+|had\s+)?(?:lied|cheated|stole|shouted|lost\s+my\s+temper|"
    r"wasted|ruined|messed\s+up|screwed\s+up|cocked\s+up|botched|betrayed|snapped)\b"
    r"|\b(?:cocked|balls(?:ed)?|buggered|botched)\s+(?:it|things?|that)?\s*up\b"
    r"|\bput\s+my\s+(?:foot|feet)\s+in\s+it\b"
    r"|\bmade\s+a\s+(?:pig'?s?\s+ear|hash)\s+of\b"
    r"|\bi\s+(?:have\s+|had\s+)?(?:made|make)\s+(?:a\s+|one\s+)?(?:huge\s+|big\s+|silly\s+|"
    r"stupid\s+|terrible\s+|awful\s+|bad\s+|daft\s+|dumb\s+|thick\s+)?(?:mistake|error)\b"
    r"|^\s*(?:i\s+)?(?:made|did)\s+(?:a\s+|an\s+|some\s+|the\s+)?(?:\w+\s+){0,2}?"
    r"(?:mistake|error|howler|blunder)\b"
    r"|\bi\s+(?:have\s+|had\s+)?let\s+(?:him|her|them|everyone|everybody|my\s+\w+|"
    r"someone|somebody)\s+down\b"
    r"|\bi\s+(?:really\s+)?(?:regret)\b"
    r"|\bi\s+shouldnt\s+have\s+(?:said|done|told|lied|shouted|yelled|snapped|eaten|drunk|"
    r"bought|spent|sent|texted|signed|answered|opened|posted|shared|taken|stayed|called|"
    r"let|been|gone)\b"
    r"|\bi\s+should\s+not\s+have\s+(?:said|done|told|lied|shouted|yelled|snapped|eaten|drunk|"
    r"bought|spent|sent|texted|signed|answered|opened|posted|shared|taken|stayed|called|"
    r"let|been|gone)\b")
NOT_A_REGRET = re.compile(
    r"\?|^(?:can|could|should|would|will|do|does|did|is|are|was|were|what|how|why|when|where|"
    r"who|which|any)\b|"
    r"\b(?:how\s+(?:do|can|should)|what\s+should|should\s+i|shall\s+i|do\s+i|can\s+i|"
    r"tomorrow|next\s+(?:time|week)|from\s+now\s+on|in\s+future|"
    r"want\s+to|wanna|gonna|going\s+to|i\s+will|i'?ll|plan(?:ning)?\s+to|"
    r"(?:if|unless|whether)\s+i)\b")
SNAPPED_A_PHOTO = re.compile(
    r"\bsnapped\s+(?:a|another|some|two|three)\s+"
    r"(?:photo|photos|pic|pics|picture|pictures|selfie|shot|shots)\b"
    r"|\blet\s+(?:my|his|her|their|our)\s+(?:hair|guard)\s+down\b"
    r"|\blet\s+off\s+steam\b")


A_MISTAKE = re.compile(r"\b(?:mistake|error|messed\s+(?:it\s+)?up|screwed\s+(?:it\s+)?up)\b")
THE_JOB_NAMED = re.compile(
    r"\b(?:mistake|error|messed\s+(?:it\s+)?up|screwed\s+(?:it\s+)?up)\b[^.]{0,24}?"
    r"\b(?:on|in|with|at|to)?\s*(?:my|the|our|a|an)\s+([a-z]+)")
NOT_A_JOB_BUT_A_PERSON = frozenset("""
    mum mom mummy dad daddy mate mates friend friends son daughter wife husband partner fiance
    boss team kid kids child colleague workmate sister brother nana gran granny nan neighbour
    neighbor someone somebody him her them everyone everybody people lass lad girl boy man woman
""".split())


WHO_DID_IT = re.compile(
    r"\b(?:s?he|they|my (?:partner|husband|wife|boyfriend|girlfriend|fianc\w*|ex|mate|friend|"
    r"brother|sister|son|daughter|mum|dad|mother|father|boss|landlord|flatmate|housemate))\b")
A_WRONG_PLAIN = re.compile(
    r"\b(?:gambl\w*|affair|seeing someone|texting (?:his|her|their) ex|"
    r"back with (?:his|her|their) ex|drinking again|on the (?:booze|drugs) again|using again|"
    r"owed? (?:me|us) money|gone behind my back|kept it from me|been unfaithful|"
    r"cheat(?:ing|ed) on (?:me|us)|slept with (?:someone|somebody|my)|sent pictures)\b")
A_WRONG_SAID = re.compile(
    r"\b(?:ly(?:ing|ed)|lied|lies|cheat\w*|hiding|hidden|hides|stole|stolen|stealing)\b")
A_WRONG_AIMED = re.compile(
    r"\s+(?:to|at|with|on)\s+(?:me|us)\b|\babout\s+(?:\w+\s+){0,2}(?:me|my|us|our|mine|ours)\b"
    r"|\s+(?:money|his wages|her wages|the savings|the rent|the bills)\b"
    r"|\s+(?:it\s+)?from\s+(?:me|us)\b")
A_WRONG_ABOUT_A_THING = re.compile(
    r"\s+(?:to|at|in|on|over|about|with|for)\s+\S"
    r"|\s+(?:the|a|an|his|her|their|its)\s+\S")
FOUND_IT_OUT = re.compile(
    r"\b(?:found|find|turned|turn)\s+(?:it\s+)?out\b|\b(?:turns|turned)\s+out\b"
    r"|\b(?:just\s+)?(?:heard|learned|learnt|discovered|found)\b")
FOUND_OUT = re.compile(
    r"\b(?:found|find|turned|turn) (?:it )?out\b|\b(?:turns|turned) out\b|"
    r"\b(?:just )?(?:heard|learned|learnt|discovered|found)\b")


def _a_betrayal(clean):
    text = " ".join(str(clean or "").lower().split())
    if not text or len(text.split()) > 22:
        return False
    wrong = A_WRONG_PLAIN.search(text)
    if not wrong:
        wrong = A_WRONG_SAID.search(text)
        if not wrong:
            return False
        if not A_WRONG_AIMED.search(text):
            if A_WRONG_ABOUT_A_THING.match(text[wrong.end():]):
                return False
            if not FOUND_IT_OUT.search(text):
                return False
    if not WHO_DID_IT.search(text[:wrong.start()]) and not FOUND_OUT.search(text[:wrong.start()]):
        return False
    after = text[wrong.end():]
    if re.search(r"\b(?:to|with|from|on|at)\s+(?!me\b|us\b)"
                 r"(?:his|her|their|my|the|a|an|some)\b", after):
        return False
    if HARM_ON_ME.search(text) and not WHO_DID_IT.search(text):
        return False
    return True


def _a_thing_they_regret(clean):
    text = " ".join(str(clean or "").lower().split())
    if not text or len(text.split()) > 20:
        return False
    if not A_REGRET_DOING.search(text):
        return False
    if NOT_A_REGRET.search(text) or SNAPPED_A_PHOTO.search(text):
        return False
    job = THE_JOB_NAMED.search(text) if A_MISTAKE.search(text) else None
    if job and job.group(1) not in NOT_A_JOB_BUT_A_PERSON:
        return False
    if HARM_NAMED.search(text) or HARM_ON_ME.search(text):
        return False
    return True


DAY_PAST = re.compile(
    r"\b(?:today|tonight|last night|yesterday|this morning|this afternoon|this evening|"
    r"at the weekend|over the weekend|this weekend|last weekend|all day|all morning|"
    r"the other day|earlier)\b")
A_DAY_SUBJECT = re.compile(
    r"\b(?:i|i'm|im|ive|i've|we|we're|weve|we've|my|our|it|work|school|the weather|the day)\b")
PAST_DOING = re.compile(
    r"\b(?:had|got|saw|was|were|went|did|made|took|met|ate|drank|bought|brought|read|played|"
    r"watched|walked|cooked|cleaned|painted|cut|sorted|finished|started|spent|sat|ran|came|left|"
    r"gave|found|booked|visited|helped|learned|learnt|worked|slept|drove|caught|wore|won|felt|"
    r"heard|told|said|sold|paid|sent|kept|put|let|set|fell|held|stood|thought|knew|began|broke|"
    r"spoke|rang|sang|wrote|built|swam|saw|ran)"
    r"\b|\b(?:(?!red\b|bed\b|shed\b|"
    r"need\b|feed\b|bleed\b|speed\b|weed\b|seed\b|breed\b|proceed\b|succeed\b|exceed\b|"
    r"indeed\b|hundred\b|greed\b|creed\b)\w+ed)\b")
A_SYMPTOM_PHRASE = re.compile(
    r"\b(?:hot|warm)\s+(?:and\s+)?(?:red|redder|swollen|tender|puffy|angry)\b"
    r"|\bred(?:ness)?\s+(?:and\s+)?(?:hot|warm|spreading|swollen|tender|angry|streaky)\b"
    r"|\bhot to (?:the )?touch\b|\bweeping\b|\boozing\b|\boozed\b|\bpus\b"
    r"|\bswollen (?:and|or) (?:red|hot|tender)\b", re.I)


NOT_A_DAY_DONE = re.compile(
    r"\b(?:tomorrow|next (?:week|weekend|month|year|monday|tuesday|wednesday|thursday|friday|"
    r"saturday|sunday)|gonna|going to|i will|i'll|ill|want to|wanna|plan to|planning to|"
    r"should i|shall i|can i|could i|do i|did i|have i|am i|are we|named|renamed)\b")


def _a_care_home_line(understood, memory):
    care = (understood or {}).get("care_home") if isinstance(understood, dict) else None
    if not isinstance(care, dict):
        return None
    pronoun = str(care.get("pronoun") or "they")
    several = pronoun == "they"
    words = {"they": pronoun, "them": "them", "their": "their",
             "is": "are" if several else "is"}
    shape = str(care.get("shape") or "")
    if shape == "bring":
        pool = A_CARE_HOME_BRING
    elif shape == "guilt":
        pool = A_CARE_HOME_GUILT
    elif shape == "visiting":
        pool = A_CARE_HOME_VISITING
    elif shape == "moved":
        pool = A_CARE_HOME_MOVED
    else:
        pool = A_CARE_HOME
    return _choose(tuple(line.format(**words) for line in pool), memory,
                   str(care.get("who") or ""))


HAVE_GOT_A_THING = re.compile(
    r"\b(?:i|we)(?:['\u2019]?ve|['\u2019]?d|\s+have)\s+"
    r"(?:only\s+|just\s+|still\s+|already\s+|now\s+)?(?:got|gotten)\b(?!\s+to\b)", re.I)


def _a_day_told_instead_of_the_receipt(said_back, clean, memory):
    if not said_back or not ack.reads_as_a_receipt(said_back):
        return None
    named = _a_name_told_reply(clean, memory)
    if named:
        return named
    if _a_small_day_shape(clean) and _a_detail_of_a_bad_day(memory, clean):
        return _choose(A_BAD_TIME_TOLD, memory, clean)
    if _a_thing_they_regret(clean):
        return _choose(A_THING_THEY_REGRET, memory, clean)
    if _a_betrayal(clean):
        return _choose(A_BETRAYAL, memory, clean)
    care = _a_care_home_line((memory or {}).get("understood"), memory)
    if care:
        return care
    if HAVE_GOT_A_THING.search(clean or ""):
        return None
    if _just_asked_about_the_day(memory):
        return None
    if _a_bad_time_told(clean, memory):
        return _choose(A_BAD_TIME_TOLD, memory, clean)
    if _a_day_asked_without_a_cheer(clean, memory):
        return _choose(A_DAY_ASKED_PLAIN, memory, clean)
    if not _a_small_day(clean, memory):
        return None
    wrecked = finding_out.the_wrecked_form_reply(clean)
    if wrecked:
        said = _choose(wrecked, memory, clean)
        if said:
            return said
    rest = _the_rest_of_the_day(clean, memory)
    if rest:
        return _choose(rest, memory, clean)
    return _choose(A_SMALL_DAY, memory, clean)


A_CROWD = re.compile(
    r"\b(?:everyone|everybody|everyone'?s|everybody'?s|other people|others|the only one|only one|"
    r"nobody else|no one else|no-one else|"
    r"(?:everyone|everybody|people|friends|mates)\s+(?:i know|around me|my age|else|at work|"
    r"from school|from uni|from work|these days)|"
    r"all (?:of )?my (?:mates|friends|family|cousins|brothers|sisters|colleagues|workmates)|"
    r"people my age|people of my age|my age)\b")
A_MILESTONE = re.compile(
    r"\b(?:behind|ahead of|sorted|sorted out|settled|milestone|milestones|"
    r"bought|buying|own(?:s|ed)? a|house|houses|flat|mortgage|babies|baby|kids|children|"
    r"married|wedding|engaged|pregnan\w*|career|promotion|their lives|getting on with it|"
    r"moved on|all sorted)\b")
NOT_A_CROWD_AHEAD = re.compile(
    r"\b(?:hate|hates|hated|bully|bullied|bullying|picks? on|picked on|leaves? me out|"
    r"left me out|laughs? at|laughed at|ignores? me|ignored me|mean to me|rumours?|gossip|"
    r"happy for (?:us|me)|proud of me|delighted for|congratulat\w*|well done|"
    r"coming round|coming over|round tonight|tonight|tomorrow|next week|next month|next year|"
    r"this weekend|party|gonna|going to|we'?re all|we are all|shall we|should we|any tips|"
    r"how do i|what should|am i|"
    r"only one (?:who|doing|that|bothered))\b")
CROWD_ORDER = re.compile(
    r"\b(?:behind|ahead of|sorted|settled|caught up|only one|but me|"
    r"all (?:of )?my (?:mates|friends|family|cousins|brothers|sisters|colleagues|workmates)|"
    r"around me|my age|people my age|"
    r"(?:and )?i(?:'?m| am)? (?:havent|haven't|have not|aint|ain't|am not|dont|do not)|"
    r"i'?m not|im not|and i'?m still|still not|without)\b")
A_CROWD_AHEAD = (
    "That comparison lands on nearly everybody, and it is not a fair one: you are seeing their "
    "headline and your own whole week. What would you actually like for yourself?",
    "The people who look sorted are mostly just further into their own thing. What is the next "
    "bit you would choose for yourself, if nobody were watching?",
    "It is worth pulling those two apart: which of those things do you actually want, and which "
    "do you only want because they have it?",
    "Everyone's timetable is their own and yours is not late, it is just not the same one. What "
    "would a good year look like for you?",
    "Nobody posts the part where it is going badly. What is the bit of your own you would want "
    "to change first?",
    "That is the comparison that makes everybody feel behind, and it has never once had the "
    "full picture. What would you want to be true for yourself a year from now?",
)


def _the_crowd_is_ahead(clean):
    text = " ".join(str(clean or "").lower().split())
    if not text or "?" in text or len(text.split()) > 16:
        return False
    if not A_CROWD.search(text) or not A_MILESTONE.search(text):
        return False
    if not CROWD_ORDER.search(text):
        return False
    return not NOT_A_CROWD_AHEAD.search(text)


A_HARD_DAY_MOOD = ("angry", "sad", "tired", "worried", "stressed", "upset")


def _the_rest_of_the_day(clean, memory, mood="neutral"):
    if not isinstance(memory, dict) or mood == "negative":
        return None
    if not _a_small_day(clean, memory):
        return None
    turns = [t for t in (memory.get("turns") or []) if isinstance(t, dict)]
    if not turns:
        return None
    was = _matchable(str(turns[-1].get("user") or ""))
    if not was:
        return None
    if _a_good_time(was) or _in_a_pool(str(turns[-1].get("bot") or ""),
                                      (A_GOOD_TIME, A_GOOD_TIME_IN_A_CARE_THREAD)):
        return A_REST_OF_A_GOOD_DAY
    if _in_a_pool(str(turns[-1].get("bot") or ""), (LOW_DAY_REPLIES,)):
        return A_REST_OF_A_HARD_DAY
    if _an_emotion(was) in A_HARD_DAY_MOOD:
        return A_REST_OF_A_HARD_DAY
    return None


def _an_emotion(clean):
    try:
        return understanding_kinds.emotion_of(clean) or None
    except Exception:
        return None


def _just_asked_about_the_day(memory):
    turns = [t for t in ((memory or {}).get("turns") or []) if isinstance(t, dict)]
    if not turns:
        return False
    return _in_a_pool(str(turns[-1].get("bot") or ""), (A_SMALL_DAY,))


_A_NEGATIVE_AUXILIARY = ("not|never|no|isn['’]?t|aren['’]?t|don['’]?t|didn['’]?t|"
                         "wasn['’]?t|weren['’]?t|can['’]?t|couldn['’]?t|"
                         "won['’]?t|hardly|cannot|haven['’]?t|hasn['’]?t|"
                         "hadn['’]?t|wouldn['’]?t|shouldn['’]?t|mustn['’]?t|"
                         "needn['’]?t|ain['’]?t|daren['’]?t|shan['’]?t|"
                         "oughtn['’]?t")
NOT_A_DAY_SAID = re.compile(r"\b(?:" + _A_NEGATIVE_AUXILIARY + r")\b")
_A_TELLING_OF_WRONG = (
    r"ly(?:ing|ed)|lies|lie\b|cheat\w*|hiding|hidden|stole|stealing|steals|gambl\w*|"
    r"affair|seeing someone|texting (?:his|her|their) ex|back with (?:his|her|their) ex|"
    r"drinking again|on the (?:booze|drugs) again|using again|owed? (?:me|us) money|"
    r"borrowed money|spent (?:it|the|our|my) .{0,20}money|gone behind my back")
A_BETRAYAL_FOUND_OUT = re.compile(
    r"\b(?:i |we )?(?:just |only |now )?(?:found|find|findin[g]|turned|turn) (?:it )?out\b"
    r"[^.!?]{0,45}\b(?:" + _A_TELLING_OF_WRONG + r")\b"
    r"|\b(?:turns|turned) out\b[^.!?]{0,45}\b(?:" + _A_TELLING_OF_WRONG + r")\b"
    r"|\b(?:i )?(?:just )?(?:heard|learned|learnt|discovered)\b[^.!?]{0,40}"
    r"\b(?:s?he|they|my \w+) (?:has been|had been|was|were|is|cheated|lied|stole)\b")


_AN_ASKING = (r"asked|told|texted|messaged|phoned|rang|called|emailed|chased|reminded|warned|"
              r"complained|spoke|talked|written|wrote")
_AN_ATTEMPT_COUNT = (r"twice|three times|four times|five times|repeatedly|again|once more|"
                     r"for the (?:second|third|fourth|fifth) time")
AN_ATTEMPT_AT_SOMEONE = re.compile(
    r"\b(?:" + _AN_ASKING + r")(?: to)?\s+(?:him|her|them|us)\b"
    r"|\b(?:" + _AN_ASKING + r")\b(?:\s+\w+){0,4}?\s+(?:" + _AN_ATTEMPT_COUNT + r")\b")


SOMEONE_ELSE_NAMED = re.compile(
    r"\b(?:my|our|his|her|their)\s+(?:mum|mam|mom|mother|dad|father|son|daughter|wife|husband|"
    r"partner|boyfriend|girlfriend|brother|sister|mate|friend|boss|marriage|relationship|"
    r"nan|nana|gran|granny|grandad|grandma|uncle|aunt|cousin|neighbour|neighbor|child|kid|baby|"
    r"mother-in-law|father-in-law|in-laws|"
    r"ex|ex-wife|ex-husband|ex-partner|ex-boyfriend|ex-girlfriend|"
    r"flatmate|housemate|roommate|landlord|stepson|stepdaughter|stepmum|stepdad)\b"
    r"|\b(?:someone|somebody|a man|a woman|a bloke|a lad)\b")
A_CHILDHOOD_MEMORY = re.compile(
    r"\bwhen i was (?:\d+|little|young|a kid|a child|at school|small)\b")
THEIR_OWN_DOING = re.compile(r"\b(?:i|im|i'm|ive|i've|we|we're|weve|we've)\b")
A_VISIT = re.compile(
    r"\b(?:came (?:round|over|by|in)|come (?:round|over)|coming (?:round|over|by)|"
    r"popped (?:round|in|over)|"
    r"stopped by|visiting|visited|rang|phoned|called|texted|facetimed|stayed over)\b")


def _a_day_of_someone_else(text):
    if A_CHILDHOOD_MEMORY.search(text):
        return True
    who = SOMEONE_ELSE_NAMED.search(text)
    if not who:
        return False
    if A_VISIT.search(text):
        return False
    mine = THEIR_OWN_DOING.search(text)
    return mine is None or who.start() < mine.start()


A_BARE_MODIFIER = frozenset(
    "a an the again already too as well anyway now so just really instead back then still yet "
    "before either though even also all of it in on at to my me myself i we our for with".split())


def _a_thing_happened(text):
    doing = PAST_DOING.search(text)
    rest = text if doing is None else text[:doing.start()] + " " + text[doing.end():]
    return bool([word for word in rest.split()
                 if len(word) > 2 and word not in A_BARE_MODIFIER])


A_THING_GOT_AHEAD = re.compile(
    r"\b(?:i|we)(?:'?ve| have)?\s+(?:just\s+|finally\s+)?"
    r"(?:got|booked|secured|bagged|landed|sorted)\s+(?:myself\s+|us\s+)?"
    r"(?:a|an|the|my|our|two|three|four|some|another|front row|cheap)?\s*"
    r"(?:audition|tickets?|viewing|viewings|booking|slot|reservations?|table booked)\b")
GOT_AHEAD_GONE = re.compile(
    r"\b(?:yesterday|last (?:night|week|month|year|saturday|sunday|monday|tuesday|wednesday|"
    r"thursday|friday)|this morning|earlier|the other day|on (?:mon|tues|wednes|thurs|fri|satur|"
    r"sun)day)\b", re.I)
A_MONTH = re.compile(
    r"\b(?:january|february|march|april|may|june|july|august|september|october|november|"
    r"december|jan|feb|mar|apr|jun|jul|aug|sept|sep|oct|nov|dec|weekend after next|"
    r"the \d+(?:st|nd|rd|th))\b", re.I)
GOT_AHEAD_NOT_A_DATE = re.compile(
    r"\b(?:parking|speeding|penalty|fine|fined|clamped|bus|train|plane|coach|tube|ferry|tram|"
    r"lottery|raffle|on the way)\b", re.I)


def _a_thing_got_ahead(clean):
    text = " ".join(str(clean or "").lower().split())
    if not text or "?" in text:
        return None
    if not A_THING_GOT_AHEAD.search(text):
        return None
    if GOT_AHEAD_GONE.search(text) or GOT_AHEAD_NOT_A_DATE.search(text):
        return None
    if A_MONTH.search(text) or DATE_AHEAD.search(text):
        return A_BOOKING_AHEAD_DATED
    return A_BOOKING_AHEAD


PROBLEM_STATED = re.compile(
    r"^(?:so |ok |okay |right |and |hi |hiya |hello |hey |um |er |honestly |well |but )*"
    r"(?:(?:i|we)(?:'?ve|'?m| have| am| got|'?ve got)\s+|there (?:is|'?s) |theres |its |"
    r"it'?s )?"
    r"(?:a |an |one )?"
    r"(?:(?:bit of a|small|big|massive|real|proper|slight|little|serious|tiny|huge|nasty|"
    r"right|bit of|wee|awkward) )?"
    r"(?:problem|issue|trouble)"
    r"(?: (?:here|really|actually|now|again|too|i (?:need|could do with) (?:some )?help(?: with)?|"
    r"that i (?:need|could do with) (?:some )?help(?: with)?|i (?:need|could do with) "
    r"(?:some )?advice))?$")

SOMETHING_UP = re.compile(
    r"^(?:so |ok |okay |right |and |hi |hello |hey |um |er |honestly |well |but )*"
    r"(?:"
    r"(?:there (?:is|'?s) |theres )?"
    r"(?:(?:something|somethings|sommat|summat)(?: really| bad| weird| odd| serious| not right)?"
    r"(?:'?s)? )?"
    r"(?:is |was |keeps )?"
    r"(?:wrong|up|not right|off|the matter)"
    r"|(?:something|somethings|sommat|summat)\s+(?:has |had |just )?"
    r"(?:happened|gone wrong|come up)"
    r"|(?:something|somethings|sommat|summat)\s+(?:is |was |keeps )?"
    r"(?:bothering|worrying|upsetting|bugging|nagging)\s+me"
    r")"
    r"(?: (?:here|today|yesterday|tonight|last night|this morning|this week|at work|at home|"
    r"again|right now|at the moment)){0,2}$")


def _a_problem_stated(clean, repaired=None):
    for line in (clean, repaired):
        bare = " ".join(re.sub(r"[^a-z0-9 ]+", " ", str(line or "").lower()).split())
        if bare and (PROBLEM_STATED.match(bare) or SOMETHING_UP.match(bare)):
            return True
    return False


WEAR_ASK = re.compile(
    r"\b(?:what|which|how)\b[^.?!]{0,40}?\b(?:wear|wearing|dress code|outfits?)\b", re.I)

WEAR_WHEN_NOTHING_ANSWERS = (
    "Clothes come down to the weather and how long you are standing about: a layer you can take "
    "off, and shoes you can spend the day in. Is it indoors or out?",
    "Go off the room rather than the label - one notch up from what most people there will have "
    "on, and a layer to shed if you are the only one dressed up. Cold where you are?",
    "Dress for the coldest hour of it and the longest you will be on your feet: shoes decide "
    "more of a day than people expect. Are you inside or out?",
)


NOTHING_TO_WEAR = re.compile(
    r"\b(?:nothin|nothing|nowt)\b\s+(?:at all\s+)?to\s+(?:wear|put on)\b|"
    r"\b(?:nothin|nothing|nowt)\s+fits\b", re.I)

NOTHING_TO_WEAR_REPLIES = (
    "Nothing to wear usually means nothing you fancy - pick the one thing you feel good in and "
    "build the rest round it. What is the day?",
    "Everyone has nothing to wear the night before. Is it work, a meal out, or a long walk?",
    "Then wear the one you always skip and keep everything else plain. What is it for?",
)


def _says_there_is_nothing_to_wear(clean, repaired=None, text=None):
    for line in (clean, repaired, text):
        said = " ".join(str(line or "").lower().split())
        if said and NOTHING_TO_WEAR.search(said):
            return True
    return False


def _a_wear_ask_about_a_day(clean, repaired=None, text=None):
    for line in (clean, repaired, text):
        said = " ".join(str(line or "").lower().split())
        if not said or not WEAR_ASK.search(said):
            continue
        rest = WEAR_ASK.sub(" ", said, count=1)
        if re.findall(r"[a-z']{2,}", rest):
            return True
    return False


HOT_FIGURE = re.compile(
    r"\b(?:\d{2})\s*(?:degrees?|°|c\b)|\b(?:minus|below)\s+(?:\d{1,2}|zero)\b|"
    r"\b(?:heat|heatwave|warm spell)\b", re.I)
WEATHER_SUN = re.compile(
    r"\b(?:sunburn\w*|sunbathe?\w*|sunny|sun cream|sunscreen|factor\s*(?:15|20|30|50)|"
    r"beach|blazing|scorching sun)\b|\bburn(?:s|t)? in (?:\w+ )?minutes?\b", re.I)
COLD_FIGURE = re.compile(
    r"\b(?:freezing|frost|snow|sleet|chilly|bitter(?:ly)?)\b|"
    r"\b(?:minus|below)\s+(?:\d{1,2}|zero)\b", re.I)


def _the_wear_pool_for_the_line(clean, repaired=None, text=None):
    said = " ".join(" ".join(str(line or "").lower().split())
                    for line in (clean, repaired, text))
    if WEATHER_WET.search(said):
        return BARE_PICK_WEAR_WET
    if COLD_FIGURE.search(said) or WEATHER_COLD.search(said):
        return BARE_PICK_WEAR_COLD
    if HOT_FIGURE.search(said) or WEATHER_HOT.search(said) or WEATHER_SUN.search(said):
        return BARE_PICK_WEAR_HOT
    return WEAR_WHEN_NOTHING_ANSWERS


def _a_small_day(clean, memory=None):
    if not _a_small_day_shape(clean):
        return False
    text = " ".join(str(clean or "").lower().split())
    read = memory.get("understood") if isinstance(memory, dict) else None
    if isinstance(read, dict) and read.get("suggestion"):
        return False
    if _a_good_time(clean, memory):
        return False
    if _a_detail_about_what_was_said(text, memory):
        return False
    if A_LOOKING_BACK.match(text):
        return False
    if ((memory or {}).get("understood") or {}).get("polarity") == -1:
        return False
    if _a_thing_got_ahead(text):
        return False
    if remark.THEIR_NAME_AGE.match(text) or remark.THEIR_NAME.match(text):
        return False
    if _a_day_of_someone_else(text):
        return False
    if _a_problem_stated(text):
        return False
    if not DAY_PAST.search(text) and not _a_thing_happened(text):
        return False
    if not (A_DAY_SUBJECT.search(text) and PAST_DOING.search(text)):
        return False
    if not DAY_PAST.search(text) and len(text.split()) > 10:
        return False
    if NOT_A_DAY_DONE.search(text) or NOT_A_DAY_SAID.search(text):
        return False
    if _a_thing_they_regret(text):
        return False
    if A_SYMPTOM_PHRASE.search(text):
        return False
    if (NEGATIVE_LINE.search(text) or HARM_NAMED.search(text)
            or A_HURT_MYSELF.search(text)):
        return False
    if A_DAY_WENT_WRONG.search(text) or remark.done_to_me(text):
        return False
    if _a_mishap_to_ask_about(text):
        return False
    if SOMEONE_DONE_WRONG.search(text):
        return False
    if A_BAD_THING_NAMED.search(text) or A_HAND_OUT.search(text):
        return False

    if _the_day_was_already_bad(memory) and not DAY_PAST.search(text):
        return False
    if (onething.A_MEDS.search(text) and onething.A_MEDS_CHANGE.search(text)
            and onething.A_MEDS_MINE.match(text)
            and not onething.A_MEDS_SYMPTOM.search(text)):
        return False
    return not BAD_DAY_ANYWAY.search(text)


A_BAD_THING_NAMED = re.compile(
    r"\b(?:bad|sad|awful|terrible|dreadful|grim|rotten|lousy|horrible|horrid|rubbish|tough)\s+"
    r"(?:news|tidings)\b")

A_HAND_OUT = re.compile(
    r"\b(?:asked|ask|asking|looked|looking|reached|reaching)\s+(?:for|out for)\s+"
    r"(?:help|support|a hand|some help)\b")


A_DAY_WENT_WRONG = re.compile(
    r"\b(?:burgl\w*|broken into|broke into|break-in|break in|robbed|robbery|mugged|mugging|"
    r"stolen|stole|theft|shoplifted|nicked|pinched|keyed|vandalised|vandalized|scratched the car|"
    r"written off|wrote it off|wrote the car off|caught fire|went on fire|on fire|burst pipe|"
    r"water damage|smoke damage|gone missing|went missing|disappeared|vanished|"
    r"crash|car crash|had a prang|a prang|in a smash|was rear-ended|rear-ended|hit by a car|"
    r"fell off|come off my bike|came off my bike|fell down the stairs)"
    r"\b|\bcrash(?:ed)?\b(?!\s+out)\b|\bflood(?:ed)?\b(?!\s+with)\b")
_A_SYMPATHY = re.compile(r"\b(?:sorry|condolences|sad news|real loss)\b")

_A_BODY_UNWELL = re.compile(r"\b(?:ill|illness|unwell|poorly|sick|infection)\b")

_A_DETAIL_OPENING = re.compile(r"^(?:it|that|this|there)\s+(?:was|were|is|had|happened)\b")

A_LOOKING_BACK = re.compile(
    r"^(?:and\s+|but\s+|so\s+|well\s+)?(?:like\s+|as\s+)?i\s+(?:already\s+|did\s+)?"
    r"(?:said|told\s+you|mention\w*)\b"
    r"[^.!?]{0,50}?\b(?:it|that|this)\s+(?:only\s+|just\s+|actually\s+|never\s+)?"
    r"(?:was|were|is|had|started|began)\b",
    re.I,
)
def _a_detail_about_what_was_said(text, memory):
    if not _A_DETAIL_OPENING.match(text):
        return False
    turns = [turn for turn in ((memory or {}).get("turns") or []) if isinstance(turn, dict)]
    if not turns:
        return False
    last_bot = str(turns[-1].get("bot") or "")
    if _in_a_pool(last_bot, (A_SMALL_DAY,)):
        return False
    if _A_SYMPATHY.search(last_bot.lower()):
        return True
    before = " ".join(str(turns[-1].get("user") or "").lower().split())
    return any(reading.search(before)
               for reading in (HARM_ANYWHERE, NEGATIVE_LINE, BAD_DAY_ANYWAY,
                              A_DAY_WENT_WRONG, _A_BODY_UNWELL))


SOMEONE_DONE_WRONG = re.compile(
    r"\b(?:called (?:me|him|her|them|us) names|"
    r"call (?:me|him|her|them|us) names|"
    r"called names|name[- ]calling|called (?:me|him|her|them|us) a \w+ name|"
    r"got called names|got called (?:a |an |the )?(?:\w+ )?names?\b|"
    r"(?:was|were|is|are|being) called (?:a |an |the )?(?:\w+ )?names?\b|"
    r"teased (?:me|him|her|them|us)|teasing (?:me|him|her|them|us)|"
    r"bullied|bullying|bullies|"
    r"picked on|picking on|picked last|picking (?:me|him|her|them) last|"
    r"left (?:me|him|her|them|us) out|leaving (?:me|him|her|them|us) out|"
    r"laughed at (?:me|him|her|them|us)|laughing at (?:me|him|her|them|us)|"
    r"made fun of (?:me|him|her|them|us)|making fun of (?:me|him|her|them|us)|"
    r"mean to (?:me|him|her|them|us)|nasty to (?:me|him|her|them|us)|"
    r"horrible to (?:me|him|her|them|us)|"
    r"(?:would|wouldnt|wouldn't|wont|won't|didnt|didn't) let (?:me|him|her|them) play|"
    r"nobody (?:will|would|wants to) play with|"
    r"snatched (?:it|the \w+) (?:off|from) (?:me|him|her|them))\b")


BAD_DAY_ANYWAY = re.compile(
    r"\b(?:hospital|a&e|ambulance|fell over|a fall|funeral|died|death|test results|biopsy|"
    r"crash|crashed|accident|collision|flood|flooded|burst pipe|fire|burgled|robbed|stolen|"
    r"wrote off|killed|killing|(?:massive|big|huge|proper|right|awful|terrible) row|"
    r"row (?:about|over|with)|"
    r"chemo|miscarriage|evicted|lost my job|sacked|fight|row with|panic|anxiety attack|ticket|"
    r"morphine|diamorphine|midazolam|syringe driver|palliative|end of life|hospice|terminal|"
    r"clamped|fined|argued|argument|shouted|cried|upset|worried|worries|sick|threw up|migraine|"
    r"rained|soaked|drenched|wet through|late for|missed my|missed the|clinic|dentist|surgery|"
    r"wrong|mistake|messed up|screwed up|"
    r"waited|waiting|queued|queue|on hold|hung around|hung about|two hours|three hours|"
    r"four hours|an hour|all night|"
    r"headache|aching|exhausted|shattered|knackered|gutted|a row|an argument|strange|grim|"
    r"full on|fell flat|meh|"
    r"came\s+off|smashed|smash|flooded|flooding|"
    r"stacked\s+it\b|stacked\s+(?:my|the|his|her|their)\s+"
    r"(?:bike|motorbike|moped|scooter|motorcycle|car|van|horse)\b|"
    r"wrecked|dented|chipped|snapped\s+(?:at|my|the|his|her|their)\b|"
    r"went up in flames|caught fire|blew up|blew a fuse|went bang|collapsed|fell apart|"
    r"packed in|conked out|stopped working|wouldnt start|wouldn't start|broke down|leaking|"
    r"came back (?:short|lower|worse)|under (?:our|the) (?:offer|asking)|over budget|"
    r"went over budget|(?:is|are|was|were) (?:still )?closed|"
    r"told\s+[^,.;!?]{0,25}?\boff\b|had a go at me|had a right go|"
    r"boot on (?:my|the|our) (?:car|van|motor|bike)\b|fell in (?!love)|"
    r"choked(?!\s+up)|short of breath|"
    r"blackened|burnt|burned|scorched|stained|rusted|scratched|slipping up|slipped up|"
    r"messed up|mucking up|mucked up|"
    r"knocked\s+over|tipped\s+over)\b")


FOOD_TOPICS = frozenset(("cooking", "food-and-drink"))


def _a_dish_name(clean, words, memory):
    if len(words) < 2 or words[0] not in DISH_PARTICIPLE:
        return False
    if words[1] in DISH_DETERMINER:
        return False
    understood = memory.get("understood") if isinstance(memory, dict) else None
    if not isinstance(understood, dict):
        return False
    topics = set(understood.get("topics") or ())
    if isinstance(understood.get("topic"), str):
        topics.add(understood["topic"])
    return bool(topics & FOOD_TOPICS)


def _a_report_with_no_pronoun(clean, text, memory):
    words = re.findall(r"[a-z']+", clean)
    if not words or words[0] not in DONE_VERB:
        return False
    if HARM_ANYWHERE.search(clean):
        return False
    if any(w in DONE_NOT_THIS for w in words[1:3]):
        return False
    if _a_dish_name(clean, words, memory):
        return False
    if _thing_done_scan(clean)[0] != "done":
        return False
    try:
        reply = reply_for(text, memory)
    except Exception:
        return False
    return reply in _THING_DONE_LINES


def _repaired_of(text, memory):
    try:
        read = memory.get("understood")
        if isinstance(read, dict) and read.get("plain"):
            return str(read["plain"])
        read = understand(text, memory)
        return str((read or {}).get("plain") or "")
    except Exception:
        return ""


def takes_as_it_comes(text, memory):
    clean = " ".join(str(text or "").lower().split())
    try:
        if reads_as_a_report(text, memory):
            return True
        if remark.regret_reply_for(clean, clean.split(), memory,
                                   _repaired_of(text, memory)):
            return True
        if _a_report_with_no_pronoun(clean, text, memory):
            return True
        if why.takes_as_it_comes(text, memory):
            return True
        if _a_verdict_line(clean, memory):
            return True
        if safetyask.reply_for(clean, memory):
            return not _after_safety(memory, clean, memory.get("understood"))
        if _a_verdict_on_their_plan(clean, memory):
            return True
        if _a_place_asked_about(clean, memory):
            return True
        if reads_as_if_i_saw(text, memory):
            return True
        if "?" not in str(text or "") and trouble.answers_a_strain_question(clean, memory):
            return True
        if (_a_declined_plan(_plain(clean), without_a_thing=True)
                and (_a_hard_week(memory)
                     or not _the_turn_before_was_a_heavy_one(memory, _plain(clean)))
                and not (_a_plan_on_the_table(memory) and not _the_line_cancels(_plain(clean)))):
            return not _after_safety(memory, clean, memory.get("understood"))
        if not handoff.takes_as_it_comes(text, memory):
            return False
        return not _after_safety(memory, clean, memory.get("understood"))
    except Exception:
        return False


TAKES_AS_IT_COMES = takes_as_it_comes


A_NAME_IS_NOT_A_DAY = re.compile(r"\b(?:is|are|was|were)\s+(?:called|named)\b")
A_NAMES_TOLD = re.compile(
    r"\bmy\s+(?:(?:new|old|little|big|eldest|youngest|middle|first|second|step|ex|late)\s+)?"
    r"(?P<person>[a-z][a-z'-]{1,20})\s+(?:is|are|was|were)\s+(?:called|named)\s+"
    r"(?P<names>[a-z][a-z'-]{0,20}(?:\s*(?:,|and|\s)\s*[a-z][a-z'-]{0,20}){0,3})"
    r"(?:\s+(?:and|,)?\s*(?:she|he|they|it)s?\b[^.!?]{0,80})?\s*$")
A_NAME_A_HOUSEHOLD_TAKES = re.compile(
    r"\b(?:we|they)\s+(?:are|were)\s+(?:called|named)\s+"
    r"(?P<names>[a-z][a-z'-]{0,20}(?:\s*(?:,|and|\s)\s*[a-z][a-z'-]{0,20}){0,3})\s*$")
NOT_A_NAME_WORD = frozenset((
    "the", "a", "an", "it", "its", "that", "this", "him", "her", "them", "me", "after",
    "something", "nothing", "whatever", "what", "which", "who", "but", "and",
    "she", "hes", "he", "they", "we", "us", "his", "hers", "theirs", "is", "was", "were",
))


def _a_name_told(clean):
    said = " ".join(str(clean or "").lower().split()).strip(" .!,")
    if not said or "?" in said:
        return None
    match = A_NAMES_TOLD.search(said)
    person = match.group("person") if match else ""
    if not match:
        match = A_NAME_A_HOUSEHOLD_TAKES.search(said)
        if not match:
            return None
    names = [word.strip() for word in re.split(r"\s*(?:,|and)\s*", match.group("names"))]
    kept = []
    for word in names:
        if not word or set(word.split()) <= NOT_A_NAME_WORD:
            break
        kept.append(word)
    names = kept
    if not names:
        return None
    if len(names) == 1:
        spoken = names[0].title()
    else:
        spoken = ", ".join(word.title() for word in names[:-1]) + " and " + names[-1].title()
    if person and person not in THE_PEOPLE and "-" not in person:
        person = ""
    return spoken, person, len(names) > 1


NAMED_AFTER = re.compile(
    r"\b(?:called|named)\s+(?:(?:him|her|them|it|me|us)\s+)?after\s+(?P<who>me|us|you|i|"
    r"(?:my|his|her|their|our)\s+[a-z-]+)\b")
A_POSSESSIVE_OF_MINE = frozenset(("my", "our"))


def _named_after_reply(clean, memory):
    said = " ".join(str(clean or "").lower().split())
    found = NAMED_AFTER.search(said)
    if not found:
        return None
    who = found.group("who")
    if who in ("me", "us", "you", "i"):
        return _choose(A_NAMED_AFTER_THEM, memory, clean) or None
    words = who.split()
    if words[0] in A_POSSESSIVE_OF_MINE:
        who = "your " + words[1]
    lines = [remark.fill_person(line.replace("{who}", who), words[-1])
             for line in A_NAMED_AFTER]
    return _choose(lines, memory, clean) or None


def _a_name_told_reply(clean, memory):
    told = _a_name_told(clean)
    if not told:
        return None
    spoken, person, plural = told
    if not person:
        return _choose([line.replace("{names}", spoken) for line in A_NAME_STORY],
                       memory, clean) or None
    lines = [remark.fill_person(line.replace("{names}", spoken), "kids" if plural else person)
             for line in A_NAME_TOLD]
    return _choose(lines, memory, clean) or None
STATE_NOT_A_DOING = re.compile(
    r"\b(?:self[- ]?employed|unemployed|retired|married|divorced|engaged|separated|pregnant|"
    r"based|interested|tired|exhausted|worried|bothered|pleased|delighted|annoyed|scared|"
    r"frightened|settled|sorted|done|on a diet|on benefits|in debt|in credit|on the dole|"
    r"a vegetarian|a vegan|on medication|on tablets)\b")
BARE_STATE = re.compile(r"\b(?:was|were|been|is|are|am|im|i'm|its|it's)\b")
STATE_THEN = re.compile(
    r"\b(?:last (?:year|summer|winter|spring|autumn|month)|years ago|used to|back then|"
    r"when i was|in the past)\b")
STATE_IN_THE_PAST = re.compile(r"\b(?:was|were)\b")


PLAN_THAT_FELL_THROUGH = re.compile(
    r"\b(?:was|were|is|are|had|have)\s+(?:meant|supposed)\s+to\s+[a-z]+")


def _a_state_of_theirs(text):
    text = " ".join(str(text or "").lower().split())
    if not text or not A_DAY_SUBJECT.search(text):
        return None
    if not STATE_NOT_A_DOING.search(text):
        return None
    rest = BARE_STATE.sub(" ", STATE_NOT_A_DOING.sub(" ", text))
    if DAY_PAST.search(text) or PAST_DOING.search(rest):
        return None
    if STATE_THEN.search(text) or STATE_IN_THE_PAST.search(text):
        return "then"
    return "now"


RESULT_WENT_WRONG = re.compile(
    r"\b(?:came out|comes out|turned out|turns out|came back|comes back|ended up|went|goes)\s+"
    r"(?:a bit\s+|a little\s+|all\s+|really\s+|quite\s+|so\s+)?\s*"
    r"(?:grey|gray|dry|soggy|burnt|burned|raw|tough|dense|rubbery|pale|lumpy|stodgy|stale|"
    r"bland|wrong|ruined|awful|horrible|terrible|overdone|undercooked|flat|sour|bitter|"
    r"curdled|split|seized)\b")


BOT_WAS_SORRY = re.compile(
    r"\b(?:sorry|that sounds (?:rough|awful|horrible|hard|heavy|tough)|that is (?:rough|awful|"
    r"hard|heavy|tough)|that's (?:rough|awful|horrible|hard|heavy|tough)|rough one|hard one)\b",
    re.I)


A_DAY_SAID_BADLY = re.compile(
    r"\b(?:bad day|bad one|rough day|rough one|rubbish day|rubbish|awful day|horrible day|"
    r"terrible day|hard day|hard one|long day|tough day|tough one|strange day|grim|draining|"
    r"it kicked off|"
    r"wiped out|hectic|full on|knackered|exhausted|shattered|gutted|a row|an argument)\b")
A_DOING_GONE_BADLY = re.compile(
    r"\b(?:badly|too\s+much|too\s+many|too\s+often|not\s+enough|nothing\s+but|binged|"
    r"overdid\s+it|junk|crap|rubbish)\b")
A_THING_SKIPPED = re.compile(
    r"\bskipped\b(?:\s+\w+){0,4}\s+(?:all\s+(?:week|month|weekend)|this\s+week|last\s+week|"
    r"lately|every\s+(?:day|morning|week)|again)\b")
A_MEAL_SKIPPED = re.compile(
    r"\bskipped\b(?:\s+\w+){0,2}\s+(?:a\s+|any\s+|my\s+|the\s+)?"
    r"(?:breakfast|lunch|lunches|dinner|dinners|tea|supper|meals?|food)\b")


def _a_day_said_badly(text):
    said = " ".join(str(text or "").lower().split()).strip(" .!,")
    if not said or "?" in said or len(said.split()) > 12:
        return False
    return bool(A_DAY_SAID_BADLY.search(said))


def _the_last_exchange(memory):
    turns = [t for t in ((memory or {}).get("turns") or []) if isinstance(t, dict)]
    for turn in reversed(turns):
        if str(turn.get("bot") or "").strip():
            return turn
    return None


def _the_day_was_already_bad(memory):
    seen = _the_last_exchange(memory)
    if seen is None:
        return False
    last = str(seen.get("bot") or "")
    if _in_a_pool(last, (LOW_DAY_REPLIES, NEGATIVE, A_BAD_TIME_TOLD, A_THING_CAME_OUT_WRONG,
                         A_PLAN_THAT_FELL_THROUGH, A_DAY_ASKED_PLAIN)):
        return True
    if BOT_WAS_SORRY.search(last[:80]):
        return True
    return _a_day_said_badly(seen.get("user"))


def _a_detail_of_a_bad_day(memory, text=None):
    seen = _the_last_exchange(memory)
    if seen is None:
        return False
    if text and DAY_PAST.search(str(text).lower()):
        return bool(_a_detail_about_what_was_said(text, memory))
    return _a_day_said_badly(seen.get("user"))


A_BEING_DONE_NOW = re.compile(
    r"\b(?:i|we|he|she|they|it|you|the|my|our|his|her|their|\w+s)\s+"
    r"(?:am|is|are|was|were|been)\s+being\b|\b(?:i'm|im|we're|they're|he's|she's|it's)\s+being\b",
    re.I)
A_DECISION_NOT_A_DAY = re.compile(r"\b(?:approved|granted|confirmed)\b", re.I)
A_WISH = re.compile(r"\b(?:i|we)\s+(?:really\s+|just\s+|so\s+|do\s+)?wish\b|\bif only\b", re.I)
A_SUM_STATED = (
    "{said} on its own tells me nothing about whether it is high or low. What were you paying "
    "before, or what has someone else been quoted for the same thing?",
    "Put {said} beside the other figure for the same job - what you were paying before, or what a "
    "friend was quoted - and then it means something. What have you got to compare it with?",
)
PRICE_NOUNS = frozenset((
    "paid", "pay", "pays", "paying", "cost", "costs", "costing", "charged", "charge",
    "charging", "quote", "quoted", "quoting", "price", "priced", "fee", "fees", "bill",
    "bills", "invoice", "deposit", "fare", "fares", "spent", "spend", "spending", "wants",
    "wanting", "asking",
))
NO_THING_SAID = frozenset((
    "i", "me", "my", "we", "us", "our", "it", "its", "it's", "that", "thats", "that's",
    "this", "they", "them", "their", "he", "she", "his", "her", "was", "were", "is",
    "are", "be", "been", "a", "an", "the", "and", "but", "so", "then", "now", "just",
    "only", "about", "around", "at", "for", "of", "to", "in", "on", "with", "from",
    "much", "many", "um", "err", "well", "really",
))
MONEY_IN_NOUNS = frozenset((
    "bonus", "bonuses", "refund", "refunds", "rebate", "rebates", "payout", "payouts", "pay",
    "wages", "salary", "earnings", "income", "pension", "pensions", "winnings", "commission",
    "dividend", "dividends", "raise", "rise", "backpay", "arrears",
))
MONEY_IN_SHAPES = re.compile(
    r"\b(?:paid|pay|pays|paying|gave|give|gives|giving|refunded|reimbursed|repaid)\s+"
    r"(?:me|us)\b"
    r"|\b(?:i|we)\s+(?:was|were|am|are|got|get|have|had)\s+(?:paid|given|refunded|"
    r"reimbursed|awarded)\b"
    r"|\b(?:i|we)\s+(?:earned|earn|made|make|won|win|sold)\b[^.]{0,24}?\bfor\b"
    r"|\b(?:sold|selling)\b[^.]{0,24}?\bfor\b\s*[\u00a3$\u20ac]?\d"
    r"|\b(?:got|get|gets|getting)\s+[\u00a3$\u20ac]?\d+\s+(?:for|from|back)\b"
    r"|\b(?:pay|wages|salary|income|pension)\s+(?:went|goes|has gone|rose|increased|is up)\b",
    re.I,
)


def _money_came_to_them(text, words):
    if words & MONEY_IN_NOUNS:
        return True
    return bool(MONEY_IN_SHAPES.search(text))


def _a_sum_with_nothing_beside_it(clean, memory=None):
    from . import reading

    text = " ".join(str(clean or "").lower().split())
    if not text or "?" in text:
        return None
    words = set(re.findall(r"[a-z']+", text))
    if _money_came_to_them(text, words):
        return None
    marked = bool(re.search(r"[\u00a3$\u20ac]", text))
    named = bool(words - NO_THING_SAID)
    if not (marked or (words & PRICE_NOUNS) or (named and reading.A_PRICE_VERB.search(text))):
        return None
    found = reading._their_figure({"turns": [{"user": text}]})
    if not found:
        return None
    _value, _unit, said, money = found
    if not money or not said:
        return None
    return said
A_ASKING_WORD = re.compile(
    r"^(?:did|do|does|have|has|had|are|is|was|were|can|could|would|will|should|shall|"
    r"what|whats|how|why|when|where|who|which|any)\b", re.I)
A_REPORTED_NOT_LIVED = re.compile(
    r"\b(?:i|we)\s+(?:saw|seen|heard|read|watched)\s+"
    r"(?:that\b|there(?:'s|s| is| are)\b|on\s+the\s+\w+|in\s+the\s+\w+|"
    r"the\s+\w+|"
    r"somebody\b|someone\b|they\b)|"
    r"\b(?:on|in)\s+the\s+(?:news|paper|radio|telly|local news)\b|"
    r"\bthey\s+say\b|\bive\s+been\s+told\b|"
    r"\b(?:says|said|told\s+me)\s+(?:that\b|there(?:'s|s| is| are)\b)", re.I)
A_NEWS_IS_A_CHANGE = re.compile(
    r"\b(?:clos(?:e|es|ed|ing|ure)|cancel\w*|chang(?:e|es|ed|ing)|charg(?:e|es|ed|ing)|"
    r"rules?|ban(?:s|ned|ning)?|cuts?|ris(?:e|es|ing)|increas(?:e|es|ed|ing)|delay\w*|"
    r"roadworks?|strikes?|walkout|fees?|prices?|tax(?:es)?|fines?|shut|"
    r"new\s+(?:rules|charges|prices|fares)|from\s+(?:monday|next\s+week|january|april))\b",
    re.I)
A_NEWS_IS_WEATHER = re.compile(
    r"\b(?:storm|storms|gale|gales|wind|winds|windy|rain|snow|ice|sleet|flood|floods|"
    r"freeze|freezing|frost|heatwave|thunder|lightning|hurricane|tornado|weather)\b", re.I)


def _a_report_from_elsewhere(clean):
    text = " ".join(str(clean or "").lower().split())
    if not text or "?" in text:
        return None
    if A_ASKING_WORD.match(text):
        return None
    if not A_REPORTED_NOT_LIVED.search(text):
        return None
    if A_NEWS_IS_WEATHER.search(text):
        return A_NEWS_OF_WEATHER
    if A_NEWS_IS_A_CHANGE.search(text):
        return A_NEWS_OF_SOMETHING_ELSE
    return None


def _a_small_day_shape(clean):
    text = " ".join(str(clean or "").lower().split())
    if not text or "?" in text:
        return False
    if len(text.split()) > 14:
        return False
    if A_BEING_DONE_NOW.search(text):
        return False
    if A_DECISION_NOT_A_DAY.search(text):
        return False
    if A_WISH.search(text):
        return False
    if AN_ATTEMPT_AT_SOMEONE.search(text):
        return False
    if A_BETRAYAL_FOUND_OUT.search(text):
        return False
    if _a_day_of_someone_else(text):
        return False
    if not DAY_PAST.search(text) and not _a_thing_happened(text):
        return False
    if not (A_DAY_SUBJECT.search(text) and PAST_DOING.search(text)):
        return False
    if not DAY_PAST.search(text) and len(text.split()) > 10:
        return False
    if NOT_A_DAY_DONE.search(text) or NOT_A_DAY_SAID.search(text):
        return False
    if _a_thing_they_regret(text):
        return False
    if A_SYMPTOM_PHRASE.search(text):
        return False
    if NEGATIVE_LINE.search(text) or HARM_NAMED.search(text):
        return False
    if A_DAY_WENT_WRONG.search(text):
        return False
    if _a_mishap_to_ask_about(text):
        return False
    if A_BAD_THING_NAMED.search(text) or A_HAND_OUT.search(text):
        return False
    if A_NAME_IS_NOT_A_DAY.search(text):
        return False
    if _a_report_from_elsewhere(text) is not None:
        return False
    if _a_state_of_theirs(text):
        return False
    if RESULT_WENT_WRONG.search(text) or PLAN_THAT_FELL_THROUGH.search(text):
        return False
    return True


def _a_bad_time_told(clean, memory=None):
    if not _a_small_day_shape(clean):
        return False
    text = " ".join(str(clean or "").lower().split())
    if NEGATIVE_LINE.search(text) or HARM_NAMED.search(text) or A_DAY_WENT_WRONG.search(text):
        return False
    if ((memory or {}).get("understood") or {}).get("polarity") == -1:
        return True
    if _a_detail_of_a_bad_day(memory, text):
        return True
    if A_DOING_GONE_BADLY.search(text) or (A_THING_SKIPPED.search(text)
                                          and not A_MEAL_SKIPPED.search(text)):
        return True
    return bool(A_DAY_SAID_BADLY.search(text))


def _a_day_asked_without_a_cheer(clean, memory=None):
    if not _a_small_day_shape(clean):
        return False
    text = " ".join(str(clean or "").lower().split())
    if NEGATIVE_LINE.search(text) or HARM_NAMED.search(text) or A_DAY_WENT_WRONG.search(text):
        return False
    if _a_bad_time_told(clean, memory):
        return False
    if _just_asked_about_the_day(memory):
        return False
    return bool(BAD_DAY_ANYWAY.search(text))
