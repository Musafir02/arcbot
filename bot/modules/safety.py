import re

from ..compose import pick
from ..compose.fallback import BLACKED_OUT_SIGHT
try:
    from ..memory import dream as _dream
except Exception:
    _dream = None
from ..understanding import respell_urgent
from ..understanding import lexicon
from ..understanding.normalize import LEXICON, glued_words, said_apart
from ..understanding.lexicon import MISSPELLINGS
from .safety_cards import (
    ALLERGY_AIRWAY,
    ALLERGY_FACE,
    ALLERGY_FOOD,
    ALLERGY_OFF,
    BLEEDING_SMALL,
    BODY,
    BREATH_BARE,
    BURNT_BODY_VERB,
    BURN_ON_BODY,
    BURN_VERB,
    CRUSH,
    CRUSH_HARD,
    CRUSH_OFF,
    CUT_BODY_PART,
    CUT_ON_BODY,
    CUT_ON_THROAT_BODY,
    FOOD_WORDS,
    HEAT_BREATH_RED,
    HEAT_CAUSE,
    HEAT_NOT_WEATHER,
    HOT_COMFORT,
    HOT_SURFACE,
    HOT_WAX_ON_BODY,
    LAUGH_BREATH_RED,
    LAUGH_OTHER_PERSON,
    LAUGH_TAKES_BREATH,
    LAUGH_WORD,
    MINOR,
    NOT_A_PET_LINE,
    NOT_BURN_ON_BODY,
    PET_APPOSITIVE,
    PET_APPOSITIVE_SUB,
    PET_BREATH,
    PET_BREATH_NOW,
    PET_CANT_SETTLE,
    PET_EFFORT,
    PET_NAIL,
    PET_OWNS_THE_WOUND,
    PET_WOUND,
    PET_PASSES_BLOOD,
    PET_ANIMAL_HURT,
    PET_OWNS_A_THING,
    HUMAN_OWN_INJURY,
    RING_STUCK,
    SCORCHED_A_PERSON,
    SIGHT_EVER,
    SIGHT_LIFE_REPLIES,
    STING_WORDS,
    TOOTH_CHIPPED,
    TOOTH_OUT,
    WAX_BODY,
    WEIGHT_JOINT,
    _PET_APPOSITIVE,
    _PET_DAMAGE_THING,
    MY_OWN_PART,
    PET_WEAK,
)
from .safety_tables import (SELF_HARM_OWN_PART, POISON_SAID, A_HURT_OF_A_BODY_PART,
                            A_WORKOUT_CUE, A_PLAN_SAID, A_PLAN_ORDINARY)
from .safety_cards import (BITE_DONE, BAT_BITE, WILD_BITE, ALLERGY_NOW, ALLERGY_SIGN_NAMED,
                            COUNTERFACTUAL_WISH, COUNTERFACTUAL_IDIOM, STRUCK_BY_A_VEHICLE,
                            STRUCK_MY_BIKE, NEAR_HIT_ON_A_ROAD,
                            NEAR_HIT_ON_A_ROAD_PLACE,
                            STRUCK_BY_A_VEHICLE_NOT, EFFORT_BEFORE,
                            EFFORT_DIED, COME_OFF_IT, EFFORT_DOING, EFFORT_NOT_AN_ACCIDENT,
                            INSECT_BITE, INSECT_BITE_NEEDS_A_LOOK, TICK_BITE, TICK_ALREADY, GRATER_CUT, PERSON_HANGING, HEAD_OUT_COLD, STRUCK_NOT_NOW, SELF_HARM_HABIT, HEAL_TIME, HEAD_REPLIES, HUMAN_BITTEN, HIT_IN_FUN_HARD, WATER_DANGER, MILD, SCALD, HYPERBOLE_WISH, PURSUIT_PLACE_HOME, INJURY_HOW, LIPS_SWELL_BARE, DOG_ATTACK, HYPO_SIGN, SUGAR_READING_LOW, SELF_HARM_REPEAT_CAUSE, FOLLOW_UP, LIMP_ONGOING, SHOULD_I_CALL, NOT_JUST_A_NEAR_THING, LIMP_PERSON, PURSUIT_FINE, LIMB_IS_A_THING)

_EFFORT_BEFORE = re.compile(EFFORT_BEFORE)
_EFFORT_DIED = re.compile(EFFORT_DIED)
_COME_OFF_IT = re.compile(COME_OFF_IT)
_EFFORT_DOING = re.compile(EFFORT_DOING)

PRIORITY = 9000

EMERGENCY_NUMBERS = "999 or 911"


def _one(verb, who):
    if verb in ("are", "were", "have", "do"):
        verb = {"are": "is", "were": "was", "have": "has", "do": "does"}[verb]
    else:
        verb += "es" if verb.endswith(("sh", "ch", "s", "x", "o")) else "s"
    return who + " " + verb


from .safety_tables import (
    ABOUT_THE_SPEAKER,
    ABUSE_BENIGN_REASON,
    ABUSE_BLOW,
    ABUSE_BUTTONHOLED,
    ABUSE_CHILD_REFUSAL,
    ABUSE_EMPLOYER_REFUSAL,
    ABUSE_FINE_ANIMAL,
    ABUSE_FINE_PLACE,
    ABUSE_HANDS_ON,
    ABUSE_KIDS_AT_HOME,
    ABUSE_KIDS_CARD,
    ABUSE_PARENT_REFUSAL,
    ABUSE_PARENT_REFUSAL_HARD,
    ANY_REFUSAL_TO_GO,
    A_HAND_ON_THE_PERSON,
    ABUSE_PLAY,
    ABUSE_PLAY_HARD,
    ABUSE_QUARREL,
    ABUSE_ROOM_CARD,
    ABUSE_ROOM_FAMILY,
    ABUSE_SCARED,
    ABUSE_SCARED_REPLY,
    ACCIDENT,
    ADULT_HIT,
    AFTER_EXERCISE,
    AGE_PERSON,
    ALARM_NUISANCE,
    AMBULANCE_CASES,
    ANIMAL_KICK,
    APPLIANCE_SMOKE,
    ASKS_ABOUT_THE_INJURY,
    ASKS_GO_BARE,
    ASKS_IF_CALL,
    ASKS_IF_GOING,
    ASK_CALL_REPLIES,
    ASK_GO_REPLIES,
    ASPIRIN_REPLY,
    A_BREATHER,
    A_FOLLOW_UP_ABOUT_THE_INJURY,
    A_GROWN_AGE,
    A_PERSON,
    A_REAL_DANGER,
    A_WISH_OR_TALK_OF_IT,
    BABY_FELL,
    BABY_FELL_OFF,
    BABY_FELL_RED,
    BABY_FELL_SURFACE,
    BATTERY_BULGE,
    BATTERY_FIRE,
    BITE_ON_ANIMAL,
    BLACKOUT_A_THING,
    BLACKOUT_BREATH,
    BLACKOUT_EFFORT,
    BLACKOUT_FLOOR,
    BLACKOUT_OFF,
    BLACKOUT_REPEAT,
    BLACKOUT_SOMEONE_DOWN,
    BLEACH_MIX,
    BLEACH_MIX_Q,
    BLEEDING,
    BLIND_CORD,
    BLISTER_CAUSE_BURN,
    BLISTER_STATE,
    BLISTER_STATE_REPLIES,
    BLOW_ON_ME,
    BLUE,
    BLUE_CLOTH,
    BLUE_COLD_CAUSE,
    BLUE_FINE,
    BLUE_FOOD,
    BLUE_OTHER_PERSON,
    BLUE_PERSON_SUBJECT,
    BLUE_STRONG,
    BLUE_TINGE,
    BODY_PART,
    BONE_ORDINARY,
    BONE_PAST,
    BONE_THROAT,
    BREATH_CAUSE,
    BREATH_CAUSE_RED,
    BREATH_EFFORT,
    BREATH_EFFORT_RED,
    BREATH_LAUGH,
    BREATH_LAUGH_REPLY,
    BREATH_PAST_OVER,
    BREATH_RED,
    BREATH_REST,
    BREATH_SHORT,
    BURNT_FOOD,
    BURNT_SELF,
    BURN_MARK_ON_A_BODY,
    CALL_HAS_A_SIGN,
    CALL_HELP_REPLY,
    CASE_WORDS,
    CHEM_WORD,
    CHEST_ASKED,
    CHEST_EFFORT,
    CHEST_IN_A_HAND,
    CHEST_IN_A_HAND_TAIL,
    CHEST_SLOW,
    CHEST_SPREADING,
    CHEST_URGENT,
    CHEST_WORK,
    CHILDHOOD_FIT,
    CHILD_FEVER_NOT_EATING,
    CHILD_FEVER_RED,
    CHILD_GROWN,
    CHILD_SCHOOL_AGE,
    CHILD_YOUNG,
    CHOKE_AIR_OK,
    CHOKE_NOT_PERSON,
    CHOKE_OVER,
    CHOKE_PERSON,
    CHOKE_PREVENT,
    CHOKE_RED,
    CHOKE_SETTLED,
    CHOKE_STILL_RED,
    CHRONIC_BREATH,
    CLEANABLE_SURFACE,
    COLD_ILLNESS,
    COLLAPSE_HINT,
    CONFUSED_THING,
    COUGH_BLOOD,
    CO_GOING_OFF,
    CO_LEAK,
    CO_SIGNS,
    CO_TEST,
    CPR_BABY_SCENE,
    CPR_CHILD,
    CPR_CHILD_SCENE,
    CPR_HOW,
    CPR_HOWTO,
    CPR_HOW_BABY,
    CPR_HOW_CHILD,
    CPR_NOT_EFFORT,
    CPR_NO_PULSE_NOW,
    CPR_ROOM_EMPTY,
    CPR_ROUGH,
    CPR_START,
    CPR_STOP,
    CPR_STOP_REPLY,
    CPR_WHEN_ALIVE,
    CRISIS_PLAN_CARRY,
    CRISIS_PLAN_ORDINARY,
    CRISIS_PLAN_REPLY,
    CRISIS_PLAN_SAID,
    CRISIS_WORD,
    CUT_NOT_STOPPING,
    DAY_TOTAL_SIGN,
    DAY_TOTAL_WORD,
    DENTAL_WORDS,
    DETAIL_AFTER_ESCALATION,
    DEVICE_BURNING,
    DEVICE_OLD,
    DIE_OF_THE_FEELING,
    DISTRESS_BESIDE_IT,
    DOG_HABIT,
    DOG_MOUTHING,
    DOG_SELF_BITE,
    DOSE_AMOUNT,
    DOSE_ASKED,
    DOSE_COURSE,
    DOSE_COURSE_KEEP,
    DOSE_WORDS,
    DRINK_WORDS,
    DROWNED_THING,
    DROWNING_HYPERBOLE,
    DRUG_NAME,
    EDGE_OF_A_DROP,
    EFFORT_AFTER,
    EFFORT_ANYWHERE,
    EFFORT_BENIGN,
    EFFORT_HEART_CLUSTER,
    EFFORT_PATTERN,
    EFFORT_RED_HEART,
    EFFORT_TOO_LONG,
    ELECTRIC_BURN,
    ELECTRIC_FINE,
    ELECTRIC_SHOCK_DEFINITION,
    ELECTRIC_SHOCK_DOWN,
    END_IT_MEANS,
    END_IT_WITH_A_THING,
    END_IT_WITH_NOUN,
    END_MEANS_OTHER,
    END_THING,
    EXERTION,
    EXERTION_CLASS,
    EXERTION_SMALL,
    EYE_CHEM,
    EYE_FINE,
    FAINT_STORY,
    FALL_ANSWERED,
    FALL_CHECK_OFF,
    FALL_CORE,
    FALL_FINE,
    FALL_HIP,
    FALL_NOW,
    FALL_PAST,
    FALL_RED,
    FALL_REPEAT,
    FALL_WORD_IDIOM,
    FEMALE_WORDS,
    FEVER_ASK,
    FEVER_RASH_FINE,
    FEVER_REPORT,
    FICTION_NOW,
    FIRE,
    FIRE_DRILL,
    NEAR_FIRE,
    NEAR_FIRE_OVER,
    NEAR_THING_OVER,
    FIRE_ELSEWHERE,
    FIRE_NOW,
    FIRE_OUT,
    FIRE_SCALE,
    FITTING_IN,
    FITTING_MANNER_TAIL,
    FIT_ALL_BETTER,
    FIT_CASES,
    FIT_ROUTINE,
    FIT_STILL_RINGS,
    FIT_THIS_WEEK,
    FLAMES,
    FLOPPY_RED_FLAG,
    FLOPPY_SLEEPY,
    FLOPPY_THING,
    FOLLOW_UP_ANCHOR,
    FOLLOW_UP_MORE,
    FOOD_CUT,
    FORAGED_EATEN,
    FORAGED_FINE,
    FRICTION_WORD,
    FRIGHTENED,
    FRIGHTENED_REPLY,
    GARMENT,
    GASPING_THIRST,
    GASP_FINE,
    GASP_RED,
    GAS_LEFT_ON,
    GAS_ON_NOT_RUNNING,
    GAS_ON_YOU,
    GAS_PAST,
    GAS_SMELL,
    GIVING_UP_GROUP,
    GIVING_UP_HELD_ON,
    GO_IN_NOT_ABOUT_IT,
    GO_IS_A_CALL,
    GRUNTING_FINE,
    HAIR_SCORCH,
    HAIR_SCORCH_ANSWER,
    HANGED_LONG_AGO,
    HANGING,
    HARD_TO_WAKE,
    HEADACHE_BAD,
    HEADACHE_STORY,
    HEADACHE_SUDDEN,
    HEAD_BANG,
    HEAD_KNOCKOUT,
    HEAD_RED,
    HEAL_WORDS,
    HEARD_ASSAULT,
    HEAT,
    HELD_CRISIS_DETAIL,
    HELD_CRISIS_OFF,
    HELP_ARRIVED,
    HELP_SOMEONE,
    HIT_IN_FUN,
    HIT_THE_LAUGH_IS_HIS,
    HOW_LONG,
    HOW_TO_TREAT,
    HUMAN_TOO,
    HYPERBOLE_BLOCK,
    HYPO_HOW_KNOW,
    HYPO_QUESTION,
    HYPO_STRONG,
    HYPO_STRONG_OTHER,
    INJURY_WORDS,
    INTRUDER,
    KICKED_PERSON,
    LIMP_LONG,
    LIMP_MECHANISM,
    LIMP_OTHER_LIMB,
    LIMP_SOMEBODY_ELSE,
    LIPS_COLD,
    LIPS_SWELL,
    LIPS_SWELL_BARE_OFF,
    LIPS_TINGLE,
    LIPS_TINGLE_FOOD,
    LIPS_TINGLE_OFF,
    LIPS_TINGLE_RED,
    LOCKED_IN_RISK,
    LOOKS_REAL,
    LOSS_SAID,
    LOSS_SUBJECT,
    MACHINE,
    MEAL_BREATH,
    MEDICINE,
    MENINGITIS_OTHER,
    MILD_BODY_SIGN,
    MILD_CHOKE,
    MILD_PRODUCT_SMALL,
    MILD_SWALLOWED,
    MORNING_ROUTINE,
    MOUTH_BLEED_NOW,
    NAMED_SICK_FINE,
    NEWBORN,
    NIGHT_BREATH_OTHER,
    NIGHT_BREATH_PAST,
    NIGHT_BREATH_RED,
    NOSE_RED,
    NOT_A_WOUND_OFF,
    NOT_NOW,
    NOT_NOW_FICTION,
    NOT_STOPPING,
    OBJECT_IN_HEAD_THING,
    OLDER_CHILD_NAMED,
    OLD_FALL_FINE,
    OLD_FALL_NOT,
    OLD_PERSON,
    OLD_TIME,
    OTHER_RISK,
    OTHER_SELF_HARM,
    OUT_COLD_ASLEEP,
    OUT_COLD_PERSON,
    OUT_COLD_REPLY,
    OVERDOSE_DRUG,
    OVERDOSE_FOOD,
    OVERDOSE_OF_A_TREAT,
    OWN_CRY,
    OWN_INJURY,
    OWN_INJURY_IN_MY_CARE,
    OWN_INJURY_QUESTION,
    OWN_LIMB_AT_AN_ANGLE,
    PALE_EFFORT_RED,
    PALE_EXERTION,
    PALE_HEAT,
    PALE_SECOND,
    PAN_FIRE,
    PARENT_REFUSAL_BLOW,
    PAST_ATTEMPT_NOT,
    PAST_WISH,
    PAST_WISH_NOT,
    PERSON,
    PERSON_AS_ATTACKER,
    PERSON_BURNT,
    PET_ALL_RIGHT,
    PET_ANY,
    PET_GASP_EXPLAINED,
    PET_GASP_FINE,
    PET_GASP_RED,
    PET_NAMES,
    PET_PAST,
    PET_RESPOND_AT,
    PET_TOOTH,
    PLAYFUL_HIT,
    POO_BLACK,
    POO_BLOOD,
    POO_FINE,
    PREGNANCY_WORDS,
    PUNCTURE,
    PUSHED_AWAY,
    PUSHED_AWAY_BUT_SOMETHING_ELSE,
    PUSHED_AWAY_REPLY,
    PUSHED_AWAY_THEN_RESTRAINT,
    RASH_FADE,
    RASH_HEADACHE_FINE,
    RASH_PRESSED,
    RAZOR_BURN,
    RECENT_FIT_FINE,
    RECENT_TIME,
    RESPOND_SENSE,
    RESTRAINT_BESIDE,
    RING_DANGER,
    RING_NOT_WORN,
    ROUTINE_REASON,
    ROUTINE_WAKE,
    SAFE_NOW,
    SAID_AS_IT_HAPPENS,
    SEIZURE,
    SEIZURE_FIGURATIVE,
    SEIZURE_STORY_GUARD,
    SELF_CUT,
    SELF_HARM_AGAIN,
    SELF_HARM_CUT_NO_OBJECT,
    SELF_HARM_DELIBERATE_ACT,
    SELF_HARM_DESERVE,
    SELF_HARM_LOOKALIKE,
    AN_ITCH_LOOKALIKE,
    SELF_HARM_NOT_EATING,
    SELF_HARM_REASON,
    SELF_HARM_SCARS,
    SELF_HARM_SCARS_NOT,
    SELF_HARM_TOPIC_OFF,
    SELF_RUMINATION,
    SELF_TALK,
    SEPSIS_SIGN,
    SHAKEN,
    SHAKEN_REPLY,
    SHOCK_ANY,
    SHORT_OF_BREATH,
    SHOT,
    SHOT_FINE,
    SIGHT_A_WHILE,
    SLUR_RED_BESIDE,
    SLUR_THICK,
    SMALL_CHILD,
    SMALL_CHILD_LASH_REPLIES,
    SMOKE_IS_A_SMELL,
    SNAKE_LOOKALIKE,
    SOCKET_OBJECT,
    SOCKET_THING_FINE,
    SOFT_BLEED_OFF,
    SOMEONE_ELSES_DESPAIR,
    SOMEONE_ELSE_OWN,
    SOME_OF_IT,
    SPELL_RED,
    SPIKED,
    SPINE_BACK_WORK,
    SPINE_BREAK,
    SPOKEN_ATTEMPT_UNDATED,
    STIFF_FINE,
    STIFF_NECK,
    STILL_GOING,
    STING_SETTLED,
    STOOL_LONG,
    STRANGLED_SELF,
    STRANGLE_THING_SUBJECT,
    STROKE_HAND,
    STROKE_HAND_BESIDE,
    STROKE_HAND_CHRONIC,
    STROKE_HAND_HARD,
    STROKE_WEAK,
    STROKE_WEAK_OFF,
    STUCK_MACHINE,
    SUICIDE_ABOUT_A_THING,
    SUICIDE_TOPIC,
    SWALLOWED_BAD_REPLY,
    SWALLOWED_BAD_SELF,
    SWALLOWED_ORDINARY,
    SWALLOWED_SELF,
    SWALLOW_GONE_OFF,
    SWALLOW_GONE_RED,
    TALK_HABIT,
    TESTIS_LUMP,
    THING_BURNT,
    THING_BURNT_WORDS,
    THING_THAT_IS_SUICIDE,
    THIRD_PERSON_ACTOR,
    THROAT_TIGHT_CAUSE,
    THROAT_TIGHT_EFFORT,
    THROAT_TIGHT_RED,
    TINY_AGE,
    TINY_AGE_FINE,
    TOOK_OUT_OF,
    TOOTH_OUT_FINE,
    TORSION,
    TORSION_FINE,
    TORSION_ONSET,
    TRAPPED_HELD_BY_A_PERSON,
    TRAPPED_VEHICLE_NOT_NOW,
    TYPED_TYPOS,
    VEHICLE_BURNING_SMELL,
    VEHICLE_BURNING_SMELL_HARD,
    VEHICLE_EXHAUST,
    VEHICLE_FIRE,
    VEHICLE_FIRE_OVER,
    VIOLENT_THREAT,
    VISIT_OR_TIME,
    WAKE_RED,
    WAKE_UP_SOMEONE,
    WATER_DROWNING_FINE,
    WATER_DROWNING_NOW,
    WATER_FINE,
    WATER_HEAD_FEAR,
    WATER_HUMAN,
    WATER_IN_NOW,
    WATER_NOT_A_PERSON,
    WATER_PERSON_TOO,
    WATER_SELF,
    WATER_THING_DROPPED,
    WATER_URGENT,
    WEIGHT_HIP,
    WEIGHT_LONG,
    WEIGHT_OFF_FEET,
    WENT_BLUE_FINE,
    WENT_BLUE_IDIOM,
    WHEN_HELP_COMES,
    WHEN_HELP_REPLY,
    WHOLE_BODY_RED_FLAG,
    WISH_BY_MODAL,
    WISH_DEAD_HYPERBOLE,
    WISH_DEAD_PLACE,
    WISH_DEAD_WHEN,
    WISH_NAMED,
    WITHDRAWAL_ALONE_AT_HOME,
    WITHDRAWAL_ASK_DANGER,
    WITHDRAWAL_DANGER,
    WITHDRAWAL_HAIR_OF_THE_DOG,
    WITHDRAWAL_HALLUCINATION,
    WITHDRAWAL_NAMED,
    WITHDRAWAL_NOT_ALCOHOL,
    WITHDRAWAL_ROUTINE,
    WITHDRAWAL_SENSES_FINE,
    WITHDRAWAL_STOP,
    WITHDRAWAL_STRONG,
    WITHDRAWAL_SYMPTOM,
    WONT_COME_ROUND,
    WORDS_OUT_OCCASION,
    WOUND_STREAK,
    WOUND_STREAK_FEVER,
    WORLD_QUESTION,
    _AGREEMENT,
    _AWAY_TAIL,
    _DENIED,
    _FLAT_WISH_HOW,
    _PERSON,
    _SMELLY_THING,
    _SMOKE_THING,
    _STRUCK_RELATIVE,
    _THIRD,

)
MALE_WORDS = (r"\bdad\b", r"\bfather\b", r"\bhusband\b", r"\bboyfriend\b", r"\bbrother\b",
              r"\bson\b", r"\blittle\s+boy\b", r"\bboy\b", r"\buncle\b", r"\bgrandad\b",
              r"\bgrandpa\b", r"\bgrandfather\b", r"\bnephew\b", r"\bhe\b", r"\bhim\b")
_TO_PATIENT = ((r"\bdon't\s+drive\s+yourself\b", "don't let {obj} drive"),
               (r"\bSit\s+and\s+stay\s+still\b", "Keep {obj} sitting and still"),
               (r"\bSit\s+upright,\s+stay\s+calm,", "Keep {obj} sitting upright and calm,"))
SHE = ([(p, v.format(obj="her")) for p, v in _TO_PATIENT]
       + [(r"\bthey're\b", "she's")] + [(p, _one(v, "she")) for p, v in _AGREEMENT]
       + [(r"\bthey\b", "she"), (r"\bthem\b", "her"), (r"\btheir\b", "her"),
          (r"\btheirs\b", "hers"), (r"\bthemselves\b", "herself")])
HE = ([(p, v.format(obj="him")) for p, v in _TO_PATIENT]
      + [(r"\bthey're\b", "he's")] + [(p, _one(v, "he")) for p, v in _AGREEMENT]
      + [(r"\bthey\b", "he"), (r"\bthem\b", "him"), (r"\btheir\b", "his"),
         (r"\btheirs\b", "his"), (r"\bthemselves\b", "himself")])


CHILD_ANON = (
    r"\b(?:my|our|her|his|their|the)\s+(?:baby|babies|toddler|newborn|infant|child|kid|"
    r"little\s+one|little\s+lad|little\s+girl|little\s+boy|\d+\s*(?:year|month)s?\s*old)\b",
)


def _person(line):
    if _matches(CHILD_ANON, line):
        her = _matches((r"\bher\b", r"\bshe\b"), line)
        if her and not _matches((r"\bhis\b", r"\bi\b", r"\bmy\b", r"\bme\b"), line):
            return "she"
        if _matches((r"\bhis\b",), line) and not her:
            return "he"
    woman = _matches(FEMALE_WORDS, line)
    man = _matches(MALE_WORDS, line)
    if woman and not man:
        return "she"
    if man and not woman:
        return "he"
    return None


SPEAKER_IS_PATIENT = (
    r"\bi\s+(?:have\s+|just\s+|think\s+i\s+|might\s+have\s+)?(?:swallowed|gulped|ate|eaten)\b",
    r"\bi\s+(?:just\s+)?choked\s+on\b", r"\bgot\s+stuck\s+in\s+my\s+throat\b",
)

DOSE_COUNT = (r"(\d{1,2}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
              r"thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|"
              r"a\s+couple|half\s+a\s+dozen|a\s+dozen)")
DOSE_DRUG = (r"(co[\s-]?codamol|codamol|paracetamol|acetaminophen|panadol|calpol|"
             r"ibuprofen|nurofen|brufen)")
DOSE_STATED = (
    r"\b(?:took|taken|swallowed|downed|popped|had|ate|eaten|been\s+taking|taking|take)\b"
    r"[^.!?]{0,18}?\b" + DOSE_COUNT + r"\b[^.!?]{0,20}?\b" + DOSE_DRUG + r"\b",
    r"\b" + DOSE_COUNT + r"\b\s*(?:x\s*)?(?:tablets?|pills?|capsules?|caplets?|doses?)\b"
    r"[^.!?]{0,18}?\b" + DOSE_DRUG + r"\b",
)

DOSE_DOUBLE = (
    r"\b(?:took|taken|had|swallowed)\b[^.!?]{0,25}\b" + DOSE_DRUG + r"\b[^.!?]{0,25}"
    r"\b(?:twice|two\s+times|a\s+double\s+dose|double\s+dose|again\s+by\s+mistake)\b",
    r"\b(?:twice|two\s+times|double\s+dose)\b[^.!?]{0,25}\b" + DOSE_DRUG + r"\b",
    r"\b" + DOSE_DRUG + r"\b[^.!?]{0,25}\b(?:twice|two\s+times|a\s+double\s+dose|"
    r"double\s+dose)\b",
)

DOSE_RECENT = (
    r"\b(?:took|taken|had|swallowed)\b[^.!?]{0,20}\b" + DOSE_DRUG + r"\b[^.!?]{0,20}"
    r"\b(?:an?\s+hour\s+ago|half\s+an\s+hour\s+ago|just\s+now|a\s+minute\s+ago|"
    r"at\s+\d|this\s+(?:morning|afternoon|evening|lunchtime|dinner))\b",
    r"\b" + DOSE_DRUG + r"\b[^.!?]{0,20}\b(?:an?\s+hour\s+ago|half\s+an\s+hour\s+ago|"
    r"just\s+now|this\s+(?:morning|afternoon|evening|lunchtime|dinner))\b",
)

DOSE_WHOLE_PACK = (
    r"\b(?:whole|full|entire)\s+(?:pack|packet|box|bottle|blister|strip)\b[^.!?]{0,25}\b"
    + DOSE_DRUG + r"\b",
    r"\b(?:handful|loads?|load\s+of|bunch)\s+(?:of\s+)?" + DOSE_DRUG + r"\b",
    r"\b" + DOSE_DRUG + r"\b[^.!?]{0,20}\b(?:all\s+at\s+once|in\s+one\s+go|"
    r"(?:whole|full)\s+(?:pack|packet|box|bottle))\b",
)

DOSE_LIMITS = {"paracetamol": 8, "acetaminophen": 8, "panadol": 8, "calpol": 8,
               "co codamol": 8, "co-codamol": 8, "cocodamol": 8, "codamol": 8,
               "ibuprofen": 6, "nurofen": 6, "brufen": 6}


def _dose_count(word):
    word = " ".join(word.lower().split())
    if word.isdigit():
        return int(word)
    if "couple" in word:
        return 2
    if "dozen" in word:
        return 6 if "half" in word else 12
    return DOSE_WORDS.get(word.replace("-", " "))


def _day_dose_reply(text):
    number, drug = None, ""
    for count, word in _DAY_TOTAL_COUNT.findall(text):
        n = _DAY_TOTAL_WORDS.get(count)
        if n is None:
            try:
                n = int(count)
            except ValueError:
                continue
        number, drug = n, word
    limit, spelling = (6, "six of the 200mg tablets a day") \
        if drug in ("ibuprofen", "nurofen", "brufen") else \
        (8, "eight 500mg paracetamol tablets a day")
    if drug in ("ibuprofen", "nurofen", "brufen"):
        tail = ("Take it with food rather than on an empty stomach, and nothing else that contains "
                "it. Needing that many for more than a few days is the back to get looked at.")
    else:
        tail = ("Four hours between doses, and count anything from a cold remedy as paracetamol "
                "too. Running at the full eight for more than a few days means the pain needs "
                "looking at rather than more tablets.")
    if number is not None and number < limit:
        return "%d is inside the day's limit of %s. %s" % (number, spelling, tail)
    return "The day's limit is %s, so there is nothing more to take. %s" % (spelling, tail)


def _stated_dose(line):
    text = " ".join(line.lower().split())
    if re.search(r"\bon\s+purpose\b|\b(?:to|trying\s+to)\s+(?:hurt|harm|kill)\s+myself\b|"
                 r"\bsuicid|\bwanted\s+to\s+die\b|\bkill\s+myself\b|\bend\s+it\b", text):
        return None
    if _matches((CHILD_TAKER, CHILD_WORD), line) or _matches(PET_OWN + PET_SUBJECT, line):
        return None
    for pattern in DOSE_STATED:
        found = re.search(pattern, text)
        if not found:
            continue
        n = _dose_count(found.group(1))
        drug = " ".join(found.group(2).lower().replace("-", " ").split())
        limit = DOSE_LIMITS.get(drug)
        if n and limit and n > limit:
            return None
        break
    if _a_days_dose(line):
        return _day_dose_reply(text)
    for pattern in DOSE_DOUBLE:
        if re.search(pattern, text):
            return ("One extra dose is usually nothing to worry about: don't take any more for four "
                    "hours, and skip that one if it lands in the night. If it was more than one "
                    "extra, or you have liver trouble or drink heavily, ring 111 rather than "
                    "guessing - and never make up a missed dose by doubling the next one.")
    for pattern in DOSE_RECENT:
        if re.search(pattern, text):
            return ("That is done and inside the limit, so the only thing to keep is the gap: four "
                    "hours before the next dose, and eight tablets of 500mg in a day at most. If "
                    "you are still in pain at four hours, that is worth getting looked at rather "
                    "than topping up early.")
    return None


SWALLOWED_BAD = (
    r"\b(?:batter(?:y|ies)|button\s+battery|magnet|magnets|razor|blade|blades|glass|"
    r"pins?|needles?|screws?|nails?|toothpick|fork|wire|beads?)\b",
)


SWALLOWED_CHILD = (r"\bmy\s+(?:child|son|daughter|baby|toddler|kid|boy|girl)\b",)

PET_DYING = (
    r"\b(?:dog|dogs|puppy|pup|cat|cats|kitten|horse|pony|rabbit|hamster|guinea\s+pig|bird|parrot|"
    r"budgie|pet|pets)\b[^.?!]{0,30}\b(?:is\s+dying|are\s+dying|dying|going\s+to\s+die|"
    r"will\s+die|going\s+to\s+be\s+put\s+(?:down|to\s+sleep)|being\s+put\s+down)\b",
)


def _fit(reply, line, case=None):
    if not reply:
        return reply
    if case is not None and case not in FIT_CASES:
        return reply
    who = _person(line)
    pairs = SHE if who == "she" else HE if who == "he" else None
    if not pairs:
        return reply
    text = reply
    for pattern, replacement in pairs:
        text = re.sub(pattern, replacement, text, flags=re.I)
    return text


CRITICAL = ("seizure", "unconscious", "anaphylaxis", "bleeding", "myself", "suicide")
CRITICAL_ONE = ("breath", "breathe", "breathing", "choking", "overdose", "chest",
                 "floppy", "kill", "killing")


def _letters_apart(word, target):
    previous = list(range(len(target) + 1))
    for i, letter in enumerate(word, 1):
        current = [i]
        for j, other in enumerate(target, 1):
            current.append(min(previous[j] + 1, current[j - 1] + 1,
                               previous[j - 1] + (letter != other)))
        previous = current
    return previous[-1]


def _near_miss(word, target):
    if abs(len(word) - len(target)) > 2:
        return False
    if word[:2] != target[:2] or word[-1] != target[-1]:
        return False
    return _letters_apart(word, target) <= 2


def _leet_made_whole(text):
    return re.sub(r"(?<=[a-z])[!1|](?=[a-z])", "i", text)


def _fold_critical(line):
    words = line.split()
    for i, word in enumerate(words):
        if word in TYPED_TYPOS:
            words[i] = TYPED_TYPOS[word]
            continue
        if word in CRITICAL or word in CRITICAL_ONE or word in LOOKS_REAL:
            continue
        tries = [(word, "")]
        if word.endswith("s") and len(word) > 4:
            tries.append((word[:-1], "s"))
        for stem, plural in tries:
            if stem in LOOKS_REAL:
                break
            hit = [target for target in CRITICAL if _near_miss(stem, target)]
            if not hit:
                hit = [target for target in CRITICAL_ONE
                       if _near_miss(stem, target) and _letters_apart(stem, target) == 1]
            if hit:
                words[i] = hit[0] + plural
                break
    return " ".join(words)


def _norm(text):
    line = text.lower().replace("\u2019", "'").replace("\u2018", "'")
    line = re.sub(r"\bu\b", "you", line)
    line = re.sub(r"\bpls\b", "please", line)
    words = line.split()
    split = []
    for index, word in enumerate(words):
        after = words[index + 1] if index + 1 < len(words) else None
        split.extend(glued_words(word, after) or [word])
    line = " ".join(split)
    for short, long in lexicon.CONTRACTIONS.items():
        if short in line:
            line = re.sub(r"\b" + re.escape(short) + r"\b", long, line)
    return " " + _fold_critical(" ".join(line.split())) + " "


_WISH_SHAPES = (
    r"die|dying|dead|kill|killing|suicid(?:e|al)|self[-\s]?harm\w*|end(?:ing)?\s+it|"
    r"better\s+off|not\s+be\s+here|want(?:s|ed)?\s+to\s+(?:die|live)|"
    r"don'?t\s+want\s+to\s+live|hurt(?:ing)?\s+my\s*self|harm(?:ing)?\s+my\s*self|"
    r"cut(?:ting)?\s+my\s*self"
)
WISH_LATER = (
    r"(?!\s*[,;:]?\s*(?:but|and|though|yet|although|however)?[^.?!]{0,40}"
    r"\b(?:" + _WISH_SHAPES + r")\b)"
)
FIGURATIVE_BREATH = re.compile(
    r"\b(?:can'?t|cannot|couldn'?t)\s+breathe\b.{0,20}\b(?:in|during|at)\s+(?:this|the|a|my|our)\s+"
    r"(?:meeting|call|interview|exam|presentation|conversation|argument|appointment|class|shift|"
    r"deadline|review)\b")

BREATH_ROOM_RED = re.compile(
    r"\b(?:smoke|smoking|smoky|smokey|fire|fires|flames?|burning|burnt|fumes?|gas|bleach|"
    r"ammonia|chemicals?|vapours?|fumes)\b")
BREATH_SETTLED = re.compile(r"\b(?:ok|okay|fine|better|alright|all right)\s+now\b")

FIGURATIVE = (
    r"\b(?:killing|kills|killed)\s+me\b", r"\bdies?\s+(?:to|for)\b", r"\bdying\s+(?:to|for)\b",
    r"\b(?:dead|dying)\s+(?:tired|bored|hungry|of\s+embarrassment)\b",
    r"\b(?:could|would|might)\s+die\b", r"\bstarving\b", r"\bkill(?:ing)?\s+(?:time|the\s+weeds)\b",
    r"\bkilled\s+it\b", r"\b(?:dye|dyed|die|dying)\s+my\s+hair\b", r"\b(?:this|that|it)\s+(?:is|'s)\s+killing\s+me\b",
    r"\bkill(?:ed|ing)?\s+(?:the|that|this)\s+(?:meeting|exam|essay|spreadsheet|run|game)\b",
    r"\bto\s+death\b", r"\bscared\s+to\s+death\b", r"\bdying\s+of\s+(?:laughter|curiosity|hunger|thirst)\b",
    r"\b(?:going\s+to|gonna|will|would|could|might|nearly|almost|just|about\s+to|shall)\s+"
    r"(?:die|died)\s+laughing\b", r"\b(?:dying|died)\s+laughing\b",
    r"\b(?:going\s+to|gonna|want\s+to|wanna|would|could|might|will|will\s+probably|nearly|almost|"
    r"just|about\s+to|shall|should)\s+(?:die|died|dying)\s+of\s+(?:embarrassment|shame|boredom|"
    r"fright|second\s?hand\s+embarrassment|thirst|hunger)\b",
    r"\bshall\s+(?:i\s+)?die\s+of\s+(?:thirst|hunger)\b",
    r"\b(?:it|its|it's|this|that|these|those|things?|everything|nothing|they)\b"
    r"[^.!?]{0,24}\bdie\s+on\s+(?:me|us|him|her|them)\b",
    r"\b(?:phone|mobile|laptop|computer|boiler|fridge|freezer|washing\s+machine|dishwasher|"
    r"dryer|heater|radiator|heating|oven|hob|kettle|toaster|tv|telly|radio|car|van|motorbike|"
    r"engine|battery|mower|router|wifi|wi-?fi|internet|broadband|connection|signal)\b"
    r"[^.!?]{0,40}\b(?:going\s+to|gonna|about\s+to|will|might)\s+(?:die|pack\s+in|pack\s+up)\b",
    r"\b(?:i\s+)?(?:could|would)\s+(?:just\s+)?kill\s+my\s*self\s+for\s+(?:forgetting|"
    r"losing|missing|being|not|saying|having|breaking|dropping|making|getting|double|booking|"
    r"sleeping|eating|spilling|forgetting\s+about)\b",
    r"\bchok(?:e|ed|es|ing)?\s+up\s*(?:$|[.,!?])",
    r"\bchok(?:e|ed|es|ing)?\s+up\s+(?:at|when|because|during|over|about|hearing|seeing|talking|"
    r"telling|reading|watching)\b",
    r"\bchok(?:e|ed|es|ing)?\s+(?:me|him|her|them|us|people|everyone)\s+up\b"
    r"(?!\s+(?:on|with)\b)",
    r"\bchok(?:ed|ing)\s+about\b",
    r"\bchok(?:ing|ed|es)\s+(?:my|the|our|his|her|their)\s+(?:diary|inbox|calendar|schedule|"
    r"budget|traffic|supply|road|agenda|market|creativity)\b",
    r"\b(?:could|would|nearly|almost|practically|honestly)\s+(?:just\s+)?(?:kill|killed|killing)"
    r"\s+my\s*self\s+(?:laughing|with\s+laugh\w*)\b" + WISH_LATER,
    r"\b(?:killing|killed)\s+my\s*self\s+(?:laughing|with\s+laugh\w*)\b" + WISH_LATER,
    r"\blaugh\w*\s+(?:so\s+(?:hard|much)|that|till|until)\b[^.!?]{0,40}\b"
    r"(?:nearly|almost)\s+killed\s+my\s*self\b" + WISH_LATER,
    r"\blaugh\w*\s+my\s*self\s+(?:silly|to\s+death|into\s+a\s+fit)\b" + WISH_LATER,
    r"\bburn\w*\s+(?:(?:my|your|our|his|her|their|all)\s+)?bridges\b",
    r"\bburn\w*\s+the\s+candle\s+at\s+both\s+ends\b",
    r"\bburn\w*\s+a\s+hole\s+in\s+(?:my|your|our|his|her|their)\s+pocket\b",
    r"\bburn\w*\s+the\s+midnight\s+oil\b",
    r"\bburn\w*\s+rubber\b",
    r"\b(?:collaps(?:e|ed|es|ing)|went\s+down|doubled\s+over|fell\s+about|fell\s+over)"
    r"\s+(?:laughing|giggling|in\s+(?:a\s+)?(?:fit|stitches|hysterics)|with\s+laugh\w*|"
    r"helpless\s+with\s+laugh\w*)\b",
)

NOT_WAKING_BESIDE = (
    r"\b(?:wouldn'?t|wouldnt|won'?t|wont|didn'?t|didnt|never)\s+(?:wake|woke)\b"
    r"(?!\s+(?:up\s+)?(?:to\s+)?(?:for\s+(?:work|school|college)\b|in\s+time\b|on\s+time\b|"
    r"to\s+an?\s+alarm\b))",
    r"\b(?:couldn'?t|couldnt|can'?t|cant)\s+be\s+woken\b",
    r"\b(?:isn'?t|isnt|not)\s+waking\b(?!\s+(?:me|us)\b)",
    r"\bout\s+cold\b",
    r"\bunresponsive\b",
    r"\bnot\s+responding\b",
)


CHORE_CAUSE = (
    r"\b(?:shaving|chopping|cooking|slicing|peeling|grating|opening|washing|washing\s+up|cleaning|"
    r"gardening|trimming|diy|baking|ironing|the\s+grater|the\s+tin|a\s+tin|the\s+knife|"
    r"the\s+oven|the\s+kettle|kitchen)\b",
)
OWN_WISH_WORDS = (
    r"\b(?:don'?t|do\s+not|doesn'?t)\s+want\s+to\s+be\s+here\b",
    r"\bnobody\s+would\s+(?:notice|care|miss\s+me)\b",
    r"\bno\s*one\s+would\s+(?:notice|care|miss\s+me)\b",
    r"\bbetter\s+off\s+without\s+me\b",
)
END_MEANS = (
    r"\bpills?\b|\btablets?\b|\bparacetamol\b|\bibuprofen\b|\boverdose\w*\b|\bropes?\b|\bnoose\b|"
    r"\bgun\b|\bknife\b|\bblade\b|\brazors?\b|\bbridge\b|\btrain\b|\bjump\w*\b|\bhang\w*\b|"
    r"\bcarbon\s+monoxide\b|\bexhaust\b|\bplastic\s+bag\b|\bcar\b",
)
END_IT_WITH_PERSON = (
    r"(?:me|him|her|them|us|my\s+" + END_IT_WITH_NOUN + r"|(?:his|her|their|our)\s+" + END_IT_WITH_NOUN + r"|"
    r"(?:the|this)\s+" + END_IT_WITH_NOUN + r")"
)
END_IT_WITH = r"\s+with\s+" + END_IT_WITH_PERSON + r"\b"
END_IT_WITH_CONNECTOR = (
    r"(?:[,.!?;]|$|and\b|but\b|so\b|because\b|now\b|too\b|tonight\b|today\b|anyway\b|"
    r"again\b|for\s+good\b)"
)


def _ends_it_with_a_method(line):
    found = re.search(r"\bend(?:ing)?\s+(?:it|(?:his|her|their)\s+(?:own\s+)?life)\s+with\s+(.*)$",
                      line)
    if not found:
        return False
    tail = found.group(1)
    pronoun = re.match(r"(?:me|him|her|them|us)\b", tail)
    if not pronoun:
        return not re.match(END_IT_WITH_PERSON + r"\b", tail)
    rest = tail[pronoun.end():].strip()
    if not rest or re.match(END_IT_WITH_CONNECTOR, rest) or re.match(END_IT_WITH_NOUN + r"\b", rest):
        return False
    return True


END_HELPLESS = (
    r"\b(?:i|we)\s+(?:can'?t|cannot|couldn'?t|am\s+not\s+able\s+to)\s+stop\s+(?:him|her|them)\b",
)


DESERVE_DENIED = re.compile(
    r"\b(?:dont|don'?t|didnt|didn'?t|doesnt|doesn'?t|never|not|nor)\b(?:\s+\w+){0,3}\s*$")

WANTED_TO_HARM = (
    r"\b(?:but|because)\s+i\s+wanted\s+to\s+(?:die|be\s+dead|disappear|vanish|not\s+be\s+here|"
    r"stop\s+existing|stop\s+breathing|kill\s+my\s*self|hurt\s+my\s*self|cut\s+my\s*self|"
    r"burn\s+my\s*self|harm\s+my\s*self|go\s+to\s+sleep\s+and\s+not\s+wake\s+up|"
    r"feel\s+(?:something|anything|pain)|suffer)\b",
    r"\b(?:but|because)\s+i\s+wanted\s+to\s+end\s+it(?!" + END_IT_WITH + r")",
    r"\b(?:but|because)\s+i\s+wanted\s+to\s+(?:\w+\s+){0,2}(?:die|dying|dead|death|gone|"
    r"disappear|vanish|choke|overdose|suicide)\b",
    r"\b(?:but|because)\s+i\s+wanted\s+to\s+(?:\w+\s+){0,2}not\s+(?:exist|be\s+here|"
    r"wake\s+up|carry\s+on|go\s+on|live)\b",
    r"\b(?:but|because)\s+i\s+wanted\s+to\s+sleep\s+(?:forever|for\s+ever|"
    r"and\s+not\s+wake\s+up)\b",
)
WANTED_TO_ACT = (
    r"\b(?:cut|hurt|burnt|burned|cutt?ing|hurting|burning|harm\w*)\s+my\s*self\b",
    r"\bself[\s-]?harm\w*\b", r"\bpunch(?:ed|ing)?\s+my\s*self\b",
    r"\bstarv(?:e|ed|ing)\s+my\s*self\b", r"\btook\s+(?:an?\s+)?overdose\b",
)
WANTED_TO_BARE = (
    r"(?=.*\b(?:but|because)\s+i\s+wanted\s+to\s*$)(?=.*(?:" + "|".join(WANTED_TO_ACT) + r"))",
    r"\b(?:but|because)\s+i\s+wanted\s+to\s*(?:[.?!]+\s*|$)",
)
CUT_MYSELF_OFF = (
    r"\bcut\s+my\s*self\s+(?:off|some\s+slack)\b",
    r"\bcut(?:s|ting)?\s+my\s*self\s+off\b",
    r"\b(?:cut|cutting)\s+my\s*self\s+(?:some\s+)?slack\b",
)


_A_MOOD_SHRUG_AFTER = (
    r"(?![^.?!]{0,14}\b(?:kill\s+my\s*self|end\s+my(?:\s+own)?\s+life|hang\s+my\s*self|"
    r"cut\s+my\s*self|hurt\s+my\s*self|take\s+my\s+life)\b)")
WISH_BY_MODAL_OFF = (
    r"\b(?:so|too|such|that|how)\s+(?:embarrass\w*|awkward|ashamed|silly|to blame|bored|"
    r"hungover|full|stuffed|hot|cold|sweaty|knackered|exhausted|thirsty|hungry|old|late|slow|"
    r"stupid|dumb|hard|tough|busy|expensive)\b[^.?!]{0,25}"
    r"\bi\s+(?:might|may|should|ought\s+to)\s+as\s+well\b" + _A_MOOD_SHRUG_AFTER,
    r"\b(?:so|too|such|how)\s+(?!(?:sad|low|lonely|depress\w*|hopeless|worthless|pointless|"
    r"empty|numb|broken|desperate|scared|frighten\w*|terrified|anxious|panick\w*|awful|"
    r"terrible|miserable|ill|sick|unwell|tired)\b)\w+\b[^.?!]{0,25}"
    r"\bi\s+(?:might|may|should|ought\s+to)\s+as\s+well\b" + _A_MOOD_SHRUG_AFTER,
)
_FLAT_WISH_TAIL = (
    r"(?=\s*[,;:!?.\u2014-]*\s*(?:(?:at\s+all|any\s*more|anymore|ever|today|tonight|"
    r"right\s+now|now|again|yet|lately|honestly|really|seriously|so\s+much|too|tbh|i\s+swear)\b)?"
    r"(?:" + _FLAT_WISH_HOW + r")?"
    r"\s*[.?!]*\s*$)"
)
_FLAT_WISH_SPEAKER = (
    r"\b(?:i'?m|im|i\s+am|i'?ve|ive|i\s+have|i\s+feel|i\s+felt|i\s+was)\b[^.?!]{0,25}\b"
)
SELF_HARM_FLAT_WISH = (
    _FLAT_WISH_SPEAKER + r"(?:had|have|has)\s+enough\s+of\s+"
    r"(?:living|life|being\s+alive|being\s+here|it\s+all|everything)\b" + _FLAT_WISH_TAIL,
    _FLAT_WISH_SPEAKER + r"(?:tired|sick|weary|fed\s+up|bored|done|finished|through)\s+"
    r"(?:of|with)\s+"
    r"(?:living|being\s+alive|being\s+here|(?:my\s+)?life|waking\s+up(?:\s+every\s+day)?)\b"
    + _FLAT_WISH_TAIL,
    _FLAT_WISH_SPEAKER + r"(?:so\s+|really\s+|very\s+)?tired\s+of\s+it\s+all\b"
    + _FLAT_WISH_TAIL,
    _FLAT_WISH_SPEAKER
    + r"(?:done|finished|through)\s+with\s+(?:it\s+all|everything|all\s+of\s+it)\b"
    + _FLAT_WISH_TAIL,
)
SELF_HARM_INTENT = (
    r"\bto\s+punish\b", r"\bpunish(?:ing)?\s+my\s*self\b",
    r"\b(?:because|cos|'?cause|as\s+if)\s+i\s+deserve[sd]?\s+(?:it|this|pain)\b",
    r"\bi\s+deserve[sd]?\s+to\s+(?:die|suffer|be\s+punished|feel\s+pain|hurt)\b",
) + WANTED_TO_HARM + WANTED_TO_BARE + (
    r"\b(?:want|wanna|wanting|wanted|need|needed|feel\s+like|feeling\s+like|"
    r"thinking\s+(?:of|about)|about\s+to|going\s+to)\s+(?:to\s+)?(?:kms|kys)\b"
    r"\s*(?:$|[.?!;,]|\b(?:tbh|rn|now|soon|tonight|again|so\s+bad|so\s+much|pls|lol)\b)",
    r"\bi\s+(?:want|wanted|wanting|need|needed)\s+to\s+(?:die|kill\s+my\s*self|hurt\s+my\s*self|"
    r"cut\s+my\s*self|burn\s+my\s*self|end\s+it(?!" + END_IT_WITH + r")|hang\s+my\s*self)\b",
    r"\b(?:wants?|wanted|wanting)\s+to\s+(?:die|kill\s+(?:him|her|them)\s*self|kill\s+them\s*selves|"
    r"hurt\s+(?:him|her|them)\s*self|hurt\s+them\s*selves|end\s+it(?!" + END_IT_WITH + r")|"
    r"cut\s+(?:him|her|them)\s*self)\b",
    *SELF_HARM_HABIT,
    r"\bto\s+feel\s+(?:something|pain|real|anything)\b",
    r"\b(?:helps?|helped)\s+me\s+(?:cope|feel)\b", r"\bself[\s-]?harm\w*\b", r"\bsuicidal\b",
    r"\bfeel(?:s|ing)?\s+(?:like|as\s+if)\s+(?:ending\s+it\s+all|ending\s+things|"
    r"not\s+being\s+here|checking\s+out\s+for\s+good)\b",
    r"\bend(?:ing)?\s+(?:it|things)\s+all\b",
) + WISH_BY_MODAL
_REPEAT = (r"\b(?:keep|keeps|kept|keep\s+on)\s+(?:cutting|hurting|burning|scratching|hitting|"
           r"banging|punching)\s+")
SELF_HARM_REPEAT_CUT = (
    _REPEAT + r"my\s+(?:arm|arms|wrist|wrists|thigh|thighs|stomach|belly|skin|forearm|forearms|"
    r"hand|hands)\b",
)
SELF_HARM_REPEAT_GRIND = (
    _REPEAT + r"my\s+(?:back|head|shoulder|shoulders|leg|legs|foot|feet|fingers?|ankles?|calves|"
    r"hips?|neck)\b",
)
SELF_HARM_REPEAT_MEANT = (
    r"\b(?:on\s+purpose|deliberatel\w+|purposely|don'?t\s+know\s+why|dont\s+know\s+why|"
    r"angry|upset|overwhelmed|anxious|can'?t\s+cope|cant\s+cope|to\s+feel|helps?\s+me|"
    r"punish\w*|deserve|stop|when\s+i\s+get)\b",
)
ANYTHING_LIFE = (
    r"anything\b(?=\s*(?:$|[.,!?;]|any\s?more|at\s?all|no\s?more|now\b|"
    r"in\s+(?:my|your|his|her|their|our)\s+(?:life|living)\b|"
    r"about\s+(?:my|your|his|her|their|our)\s+life\b|at\s+the\s+moment\b))")

POINT_TAIL = (r"(?=\s*(?:$|[.,!?;]|any\s?more|at\s+all|no\s?more|right\s+now\b|now\b|lol\b|"
              r"haha+\b|tbh\b|honestly\b|really\b|though\b|tho\b))")

HOPELESS = (
    r"\b(?:not\s+sure|don'?t\s+know|do\s+not\s+know|wonder\w*)\b[^.?!]{0,25}"
    r"\b(?:want\s+to\s+)?(?:keep\s+going|carry\s+on|go\s+on|be\s+here)\b"
    r"(?=\s*(?:$|[.,!?;]|any\s?more|no\s?more|like\s+this))",
    r"\b(?:don'?t|do\s+not|dont)\s+want\s+to\s+(?:keep\s+going|carry\s+on|go\s+on|be\s+here)\b"
    r"(?=\s*(?:$|[.,!?;]|any\s?more|no\s?more|like\s+this))",
    r"\b(?:no|any)\s+point\s+(?:any\s?more|in\s+(?:anything|any\s+of\s+(?:it|this|that)|"
    r"all\s+of\s+(?:it|this)|it\s+any\s?more|trying|being\s+here)|"
    r"to\s+(?:anything|any\s+of\s+(?:it|this|that)|all\s+of\s+(?:it|this)|it\s+any\s?more|"
    r"being\s+here))\b"
    r"(?=\s*(?:$|[.,!?;]|any\s?more|at\s+all|no\s?more))",
    r"\bwhat'?s\s+the\s+point\s+(?:any\s?more|of\s+(?:" + ANYTHING_LIFE + r"|any\s+of\s+(?:it|this|that)"
    + POINT_TAIL + r"|all\s+of\s+(?:it|this)" + POINT_TAIL + r"|"
    r"trying|living|being\s+here|it\s+all|all\s+of\s+it)|"
    r"of\s+(?:it|this)\s+any\s?more)\b",
    r"\bthere'?s\s+no\s+point\s+any\s?more\b",
    r"\b(?:i\s+)?wis?h(?:ed)?(?:\s+to\s+(?:god|christ|hell|fuck|fucking\s+god))?"
    r"\s+(?:i\s+)?(?:wasn'?t|weren'?t|was\s+not|were\s+not)\s+"
    r"(?:here|around|alive|born)\b"
    r"(?=\s*(?:$|[.!?]|any\s?more|at\s+all|now\b|tonight\b))",
    r"\b(?:i\s+)?wis?h(?:ed)?(?:\s+to\s+(?:god|christ|hell|fuck|fucking\s+god))?"
    r"\s+i\s+(?:was|were)\s+(?:dead|gone|not\s+here)\b"
    r"(?=\s*(?:$|[.!?]|any\s?more|at\s+all|now\b))",
    r"\b(?:i\s+)?wis?h(?:ed)?(?:\s+to\s+(?:god|christ|hell|fuck|fucking\s+god))?"
    r"\s+i\s+could\s+(?:just\s+|only\s+)?"
    r"(?:be\s+dead|die|not\s+wake\s+up|go\s+to\s+sleep\s+and\s+not\s+wake\s+up)\b"
    r"(?=\s*(?:$|[.!?]|any\s?more|at\s+all|by\s+now|now\b|tonight\b))",
    r"\b(?:everyone|everybody)\b[^.?!]{0,14}\b(?:would|will|is|are)\s+(?:be\s+)?better\s+off"
    r"(?=\s*(?:$|[.!?]|without\s+me\b|if\s+i\b|now\b|any\s?more\b))",
    r"\bnothing\s+(?:ever|really|seems\s+to|is\s+ever|will\s+ever)\s+"
    r"(?:get|gets|feel|feels|be|looks?)\s+(?:any\s+)?better\b"
    r"(?=\s*(?:$|[.,!?;]|any\s?more|at\s+all|no\s?more|and\b|but\b|because\b|so\b))",
    r"\b(?:what(?:'?s|\s+is|\s+was)|where(?:'?s|\s+is))\s+the\s+(?:point|use)\s+(?:of|in)\s+(?:any\s+of\s+it|"
    r"all\s+of\s+it|all\s+of\s+this(?=\s*(?:$|[.,!?;]))|it\s+all|all\s+(?:this|that)"
    r"(?=\s*(?:$|[.,!?;]))|life\s+itself|carrying\s+on|"
    r"going\s+on|keeping\s+going|bothering)\b",
    r"\bwhat(?:'?s|\s+is|\s+was)\s+the\s+(?:point|use)\s+(?:of|in)\s+any\s+of\s+this\b"
    r"(?=\s*(?:$|[.,!?;]|any\s?more|at\s+all|no\s?more|now))",
    r"\bwhat(?:'?s|\s+is|\s+was)\s+the\s+use\s+(?:of\s+anything|any\s?more)\b",
    r"\bwhat'?s\s+the\s+use\s*(?=$|[.?!])",
    r"\b(?:there'?s|there\s+is|it'?s|its|i\s+see)\s+(?:no|any)\s+point\s+"
    r"(?:to|in|of)\s+(?:any\s+of\s+it|any\s+of\s+this|all\s+of\s+it|it\s+all|"
    r"all\s+(?:this|that)(?=\s*(?:$|[.,!?;])))\b",
    r"\bwhat(?:'?s|\s+is)\s+the\s+(?:point|use)\s+(?:of|in)\s+anything\b"
    r"(?=\s*(?:$|[.,!?;]|any\s?more|at\s+all|no\s?more))",
    r"\b(?:can'?t|cannot|don'?t|do\s+not)\s+see\s+the\s+point\s+(?:of|in|to)\s+"
    r"(?:any\s+of\s+it|any\s+of\s+this|all\s+of\s+it|it\s+all|all\s+(?:this|that)\b"
    r"(?=\s*(?:$|[.,!?;])))",
    r"\b(?:can'?t|cannot|don'?t|do\s+not)\s+see\s+the\s+point\s+(?:of|in|to)\s+anything\b"
    r"(?=\s*(?:$|[.,!?;]|any\s?more|at\s+all|no\s?more))",
    r"\bnothing\s+(?:left\s+)?(?:to\s+live\s+for|worth\s+living\s+for)\b"
    r"(?=\s*(?:[.,!?;]|$|any\s?more|at\s+all|any\s+longer|now\b|left\b|either\b|"
    r"since\s+\w))",
    r"\bwhy\s+(?:should\s+i\s+)?bother\s*(?:any\s?more|at\s+all)?\s*$",
    r"\b(?:can'?t|cannot|can\s+not)\s+go\s+on\b"
    r"(?=\s*(?:[.?!]?\s*$|any\s?more|like\s+this|with\s+this))",
    r"\bend\s+of\s+(?:my|the)\s+(?:rope|tether)\b",
    r"\b(?:life|lifes|life'?s|everything)\b[^.?!]{0,14}\b(?:not|isn'?t|aint|is\s+not)\s+"
    r"worth\s+(?:it|living|the\s+(?:trouble|effort|pain))\b"
    r"(?!\s+(?:for|at|in|to)\s+\w)",
    r"\bit'?s\s+(?:not|isn'?t|aint)\s+worth\s+"
    r"(?:living|being\s+here|the\s+(?:trouble|effort|pain))\b"
    r"(?!\s+(?:for|at|in|to)\s+\w)",
    r"\b(?:don'?t|do\s+not|can'?t|cannot)\s+see\s+the\s+point\b"
    r"(?=\s*(?:$|[.,!?;]|any\s?more|in\s+(?:anything|life|living|it)))",
    r"\bnothing\s+matters\b(?=\s*(?:$|[.,!?;]|any\s?more|now\b|to\s+me\b))",
    r"\bnothing\s+(?:will|is\s+going\s+to|is\s+ever\s+going\s+to)\b[^.?!]{0,20}"
    r"\b(?:get|feel|be)\s+better\b",
    r"\bis\s+(?:my\s+)?life\s+worth\s+living\b",
    r"\b(?:never|not)\s+going\s+to\s+(?:feel|get)\s+better\b"
    r"(?=\s*(?:$|[.,!?;]|any\s?more|again))",
    r"\b(?:giv(?:e|es|ing)|gave|giv(?:en))\s+up\s+(?:on\s+)?(?:my\s+|your\s+|his\s+|her\s+|their\s+)?"
    r"(?:life|living|it\s+all|everything|myself|himself|herself|themselves|being\s+here)\b"
    r"(?!\s+for\b)",
    r"\b(?:can'?t|cannot|can\s+not)\s+wait\s+"
    r"(?:to\s+(?:die|be\s+dead)|(?:un)?till?\s+i\s+die|for\s+death)\b",
)

SELF_HARM_DELIBERATE = (r"\b(?:on\s+purpose|deliberately|made\s+my\s*self)\b",)
SELF_HARM_DENIED = (
    r"\b(?:not|never|no|n'?t)\b(?:\s+\w+){0,3}\s+(?:on\s+purpose|deliberately)\b",
)


DEATH_WORDS = (r"\b(?:die|dying|dead|suicide|suicidal|kill|killing|myself)\b",)


END_ALL = (r"\bend(?:ing)?\s+(?:it|things)\s+all\b",)


def _ending_a_thing(line):
    if _matches(END_ALL, line):
        return False
    return _matches(END_THING, line) and not _matches(DEATH_WORDS, line)


AVOID_BEFORE = re.compile(
    r"\b(?:without|avoid(?:s|ed|ing)?|to\s+avoid|so\s+as\s+not\s+to|so\s+i\s+don'?t|"
    r"so\s+i\s+do\s+not|so\s+i\s+won'?t|so\s+i\s+wont|not\s+to|scared\s+(?:of|to)|"
    r"afraid\s+(?:of|to)|worried\s+about|instead\s+of|before\s+i)\b"
    r"(?:\s+\w+){0,4}\s*$"
)


def _avoided(line, patterns):
    hits = [m.start() for m in (re.search(pattern, line) for pattern in patterns) if m]
    return bool(hits) and all(AVOID_BEFORE.search(line[max(0, at - 40):at]) for at in hits)


def _deserve(line):
    hits = [m.start() for m in (re.search(pattern, line) for pattern in SELF_HARM_DESERVE) if m]
    if not hits:
        return False
    return any(not DESERVE_DENIED.search(line[max(0, at - 42):at]) for at in hits)


OWN_LIFE = (
    r"\b(?:take|takes|taking|took|end|ends|ending|ended)\s+my\s+(?:own\s+)?life\b"
    r"(?!\s*(?:back|again|apart|over|into|off))",
)


_CLAUSE_OR_END = (
    r"\s*(?:$|[.,!?;]|(?:and|but|because|cos|honestly|though|yet|so|at\s+all|anymore|"
    r"any\s?more|now|right\s+now|tonight|today|tomorrow|already|still|again)\b)")
_WISH_TAIL_OFF = r"[^.?!]*\bthan\b"

WISH_BE_DEAD = (
    r"(?<!n't\s)(?<!nt\s)(?<!not\s)(?<!ever\s)"
    r"\b(?:want|wants|wanted|wanting|wanna)\s+(?:to\s+)?be\s+(?:dead|gone)\b"
    r"(?=" + _CLAUSE_OR_END + r"|\s+(?:for\s+good|forever)\b)"
    r"(?![\s\S]*\bbut\s+(?:sometimes|some\s+days|other\s+days|then|now\s+and\s+then|"
    r"i\s+do|i\s+still\s+do|most\s+days)\b)",
    r"\b(?:don'?t|do\s+not|doesn'?t|does\s+not|never|wouldn'?t|would\s+not|didn'?t|did\s+not)\s+"
    r"want\s+(?:to\s+)?be\s+(?:dead|gone)\b[\s\S]{0,40}?\bbut\s+(?:sometimes|some\s+days|"
    r"other\s+days|then|now\s+and\s+then|i\s+do|i\s+still\s+do|most\s+days)\b",
    r"\b(?:want|wants|wanted|wanting|wanna)\s+to\s+(?:sleep|go\s+to\s+sleep|be\s+asleep|"
    r"stay\s+asleep)\b[^.?!]{0,25}\b(?:not|never|nor)\s+wake\s+up\b",
    r"\b(?:really\s+|honestly\s+|just\s+|sometimes\s+)?(?:hope|hoping|wish|wishing)\s+"
    r"(?:that\s+)?(?:i|id|i'd)\s+(?:just\s+)?(?:don'?t|dont|do\s+not|never|wouldn'?t|"
    r"would\s+not|didn'?t|did\s+not)\s+(?:have\s+to\s+|ever\s+)?wake\s+up\b"
    r"(?=(?:\s+(?:tomorrow(?:\s+morning)?|today|tonight|again|at\s+all|in\s+the\s+morning))?"
    r"\s*(?:$|[.,!?;]))",
    r"\b(?:i|id|i'd)\s+(?:would\s+)?rather\s+(?:be\s+dead|die|not\s+wake\s+up|be\s+gone)\b"
    r"(?!" + _WISH_TAIL_OFF + r")"
)

WISH_INTENT = (
    r"\b(?:feel|feels|felt|feeling)\s+(?:like\s+)?(?:ending\s+(?:it(?!" + END_IT_WITH + r")|"
    r"my\s+life)|killing\s+my\s*self|dying)\b",
    r"\b(?:want|wanna|wanting|plan|planning|thinking|thought|ready|decided)\s+(?:to\s+|about\s+)?"
    r"(?:die|end(?:ing)?\s+(?:it(?!" + END_IT_WITH + r")|my\s+life)|kill\s+my\s*self|"
    r"not\s+be\s+here)\b",
) + WISH_BE_DEAD


def _habit_explained(line):
    if _deserve(line) or not _matches(SELF_HARM_HABIT, line):
        return False
    if _matches(SELF_HARM_DELIBERATE, line):
        return False
    rest = tuple(p for p in SELF_HARM_INTENT if p not in SELF_HARM_HABIT)
    if _matches(rest, line) or _hopeless(line) or _matches(WISH_INTENT, line):
        return False
    return _matches(ACCIDENT, line)


def _a_pet_hurting_itself(line):
    if not _matches(PET_HURTING_ITSELF, line):
        return False
    if _matches(HUMAN_TOO, line) or _matches(THIRD_PERSON_ACTOR, line):
        return False
    return not _matches(FIRST_PERSON_WISH, line) and not _own_wish(line)


def _a_wish_that_is_theirs(line):
    if not _matches(THIRD_PERSON_WISH, line):
        return False
    if _ends_it_with_a_method(line):
        return False
    if _matches(FIRST_PERSON_WISH, line) or _own_wish(line) or _matches(SO_I_TOO, line):
        return False
    return True


def _a_pet_wants_out(line):
    if not _matches(PET_WANTS_OUT, line):
        return False
    if _matches(HUMAN_TOO, line) or _matches(THIRD_PERSON_ACTOR, line):
        return False
    if _matches(SO_I_TOO, line):
        return False
    return not _matches(FIRST_PERSON_WISH, line) and not _own_wish(line)


def _self_harm_intent(line):
    if _a_pet_hurting_itself(line):
        return False
    if _a_pet_wants_out(line):
        return False
    if _a_wish_that_is_theirs(line):
        return False
    if _habit_explained(line):
        return False
    if _an_ordinary_helping(line):
        return False
    if _a_real_injury_beside_the_plate(line):
        return False
    if _matches(HYPERBOLE_WISH, line) and not _matches(WISH_INTENT, line) \
            and not _matches(HYPERBOLE_BLOCK, line):
        return False
    if _deserve(line) or _matches(SELF_HARM_INTENT, line) or _hopeless(line) \
            or _matches(WISH_INTENT, line) or _matches(OWN_LIFE, line):
        if _ending_a_thing(line):
            return False
        if _matches(GARDEN_WORDS, line) and not _matches(GO_ON_LIVING, line):
            rest = _GO_ON_PHRASE.sub(" ", line)
            if not (_own_wish(rest) or _hopeless(rest)
                    or _matches(SELF_HARM, rest) or _matches(DESPAIR, rest)):
                return False
        if re.search(r"\b(?:not|don'?t|doesn'?t|didn'?t|never|shouldn'?t|can'?t)\b[^.?!]{0,14}"
                     r"\bdeserve", line):
            return False
        return True
    if _matches(SELF_HARM_REPEAT_CAUSE, line):
        pass
    elif _matches(SELF_HARM_REPEAT_CUT, line):
        return True
    elif _matches(SELF_HARM_REPEAT_GRIND, line) and _matches(SELF_HARM_REPEAT_MEANT, line):
        return True
    return (_matches(SELF_HARM_DELIBERATE, line)
            and _matches(SELF_HARM_DELIBERATE_ACT, line)
            and (not _matches(SELF_HARM_DENIED, line) or _matches(SELF_HARM_NOT_EATING, line)))


SOMEONE_REPORTED = (
    r"\b(?:said|says|say|saying|told\s+me|tells\s+me|keeps\s+saying|kept\s+saying|mentioned|"
    r"texted|messaged|rang|phoned|wrote|thinks|thinks?\s+that|feels|reckons|admits?|admitted)\b",
)
SOMEONE_AS_SUBJECT = (
    r"\b(?:he|she|they|my\s+(?:friend|mate|boyfriend|girlfriend|partner|husband|wife|son|daughter|"
    r"child|kid|mum|mom|mother|father|dad|brother|sister|step\w+|cousin|nephew|niece|grandson|"
    r"granddaughter|gran|nan|aunt|auntie|uncle))\b",
)


NOT_THEIR_OWN = (r"\b(?:died|dead|dying|death|gone|passed|buried|funeral|lost|left|leaving|"
                 r"leave|hospital|hospice|prison|jail|missing)\b")


def _someone_elses_despair(line):
    if re.search(r"\b(?:i|im|i'm|ive|i've|id|i'd|myself|my\s+own)\b", line):
        return False
    if _matches(OWN_WISH, line) or _matches(FIRST_PERSON_WISH, line):
        return False
    phrase = r"(?:" + "|".join(SOMEONE_ELSES_DESPAIR) + r")"
    person = r"(?:" + "|".join(SOMEONE_AS_SUBJECT) + r")"
    report = r"(?:" + "|".join(SOMEONE_REPORTED) + r")"
    if re.search(person + r"[^.?!]{0,30}" + report + r"(?:\s+(?:that|she|he|they)\b)?"
                 r"[^.?!]{0,20}" + phrase, line):
        return True
    return bool(re.search(person + r"\s+(?:(?!" + NOT_THEIR_OWN + r")(?:\w+\s+)){0,3}" + phrase,
                          line))


CHEST_RED_FLAGS = (
    r"\b(?:numb|numbness|tingl\w*|left\s+arm|arm|jaw|shoulder|sweat\w*|clammy|grey|gray|pale|"
    r"crushing|pressure|heavy|heaviness|tight|squeez\w*|can't\s+breathe|breathless\w*|"
    r"short(?:ness)?\s+of\s+breath|faint\w*|pass(?:ed)?\s+out|sick|vomit\w*|dizzy)\b",
)

CHEST_ASKED_OWN = (
    r"\bchest\b[^.?!]{0,20}\b(?:pain|pains|hurt|hurts|hurting|ache|aches|aching|sore)\b",
    r"\b(?:pain|pains|ache|aches|aching|hurt|hurts|hurting)\b[^.?!]{0,15}\bchest\b",
)
CHEST_KEPT_BY_ANOTHER_CARD = (
    r"\b(?:tight|tightness|pressure|heavy|heaviness|burning|burn|reflux|heartburn|indigestion|"
    r"after\s+eating|after\s+food|when\s+i\s+eat|after\s+a\s+meal|lie\s+down)\b",
    r"\b(?:breathe|breathing|breath|inhale|in\s+breath)\b",
)

SOFT_BLEED = (r"\b(?:still|keeps?|kept)\s+(?:on\s+)?bleeding\b",)
SOFT_BLEED_ANCHOR = (r"\b(?:cut|wound|gash|slice|slashed|blood)\b",)
NOT_STOPPING_CUT = (
    r"\b(?:cut|cuts|cutting|wound|gash)\b.{0,20}" + BODY_PART + r".{0,25}\b(?:badly|deep(?:ly)?)\b",
    BODY_PART + r".{0,25}\b(?:cut|gash)\b.{0,25}\b(?:badly|deep(?:ly)?)\b",
    r"\b(?:cut|gash)\s+myself\b.{0,25}\b(?:badly|deep(?:ly)?)\b",
)
NOT_STOPPING_OFF = (
    r"\bnoses?\b", r"\bnose\s*bleed\b",
    r"\b(?:has|have|had|it|bleeding)\s+(?:now\s+)?stopp?ed\b", r"\bno\s+longer\s+bleeding\b",
    r"\b(?:paper|small|little|tiny|shaving)\s+cut\b", r"\bperiod\b", r"\bhemorrhoid",
)

CHEST_TRAINING = (
    r"\bchest\s+(?:workout|work\s?out|session|exercise|exercises|training|press|day|day\s+at\s+the\s+gym)\b",
    r"\b(?:bench|chest)\s+press\w*\b",
)

THING_COLLAPSE = (
    r"\b(?:cake|souffl\w*|sponge|meringue|crumble|bread|dough|pastry|tart|pie|biscuits?|castle|"
    r"roof|ceiling|shelf|shelves|tower|prices?|market|deal|plan|hopes?|stocks?|bridge|economy)\b",
)


_COMPILED = {}


def _hopeless(line):
    if not _matches(HOPELESS, line):
        return False
    if _matches(GIVING_UP_GROUP, line) \
            and not _matches(FIRST_PERSON_WISH, line) and not _own_wish(line):
        return False
    return not _matches(GIVING_UP_HELD_ON, line)


def _matches(patterns, line):
    if isinstance(patterns, str):
        patterns = (patterns,)
    for pattern in patterns:
        rx = _COMPILED.get(pattern)
        if rx is None:
            rx = _COMPILED[pattern] = re.compile(pattern)
        if rx.search(line):
            return True
    return False


WISH_FRAME = (
    r"\b(?:i\s+)?wis?h(?:ed)?\s+i\s+could\b",
    r"\b(?:i\s+)?wis?h(?:ed)?\s+i\s+(?:was|were)\b",
)


def _a_wish_for_their_own_body(line):
    if not _matches(SELF_HARM_OWN_PART, line):
        return False
    return not (re.search(A_HURT_OF_A_BODY_PART, line) and re.search(A_WORKOUT_CUE, line))


def _idiom(line):
    if _the_effort_frame(line):
        return True
    if not _matches(IDIOM, line):
        return False
    if _matches(PLAN_FRAME_LAUGH, line):
        return False
    if re.search(r"\bdie\s+(?:laughing|of\s+(?:embarrassment|boredom|shame))\b", line):
        return True
    return not _matches(WISH_FRAME, line) and not _rest_of_it_rings(line)
_HARM_LEFT = (
    r"\b(?:suicid\w*|kill\s+my\s*self|hurt\w*\s+my\s*self|self[-\s]?harm\w*|"
    r"cut\w*\s+my\s*self|overdos\w*|wants?\s+to\s+die|wanting\s+to\s+die|dying|dead)\b",
)
CUT_MYSELF_OFF = (
    r"\b(?:cut|cutting|cuts)\s+my\s*self\s+(?:off|away)\b",
    r"\b(?:cut|cutting|cuts)\s+my\s*self\s+out\s+of\b",
    r"\b(?:cut|cutting)\s+my\s*self\s+(?:some\s+)?slack\b",
    r"\b(?:cut|cutting|cuts)\s+my\s*self\s+from\s+(?:society|everyone|everybody|people|"
    r"social\s+media|social\s+contact|the\s+world|human\s+contact)\b",
)


def _cut_off_idiom(line):
    if not _matches(CUT_MYSELF_OFF, line):
        return False
    rest = line
    for pattern in CUT_MYSELF_OFF:
        rest = re.sub(pattern, " ", rest)
    if _matches(CRISIS_PLAN_SAID, rest) or CRISIS_WORD.search(rest):
        return False
    if _matches(ABUSE, line) or _matches(ABUSE_HIT_ME, line):
        return False
    return not _self_harm_intent(rest) and not _matches(_HARM_LEFT, rest)


def _denied_wish(line):
    best = None
    for pattern in _DENIED:
        for m in re.finditer(pattern, line):
            if best is None or (m.end() - m.start()) > (best.end() - best.start()):
                best = m
    if best is None:
        return False
    rest = line[:best.start()] + " " + line[best.end():]
    if re.search(r"\b(?:but|though|although|however|yet|except)\b", rest):
        return False
    return not re.search("|".join(_HARM_LEFT), rest)
def _blocked(line):
    if _matches(WISH_FRAME, line):
        return False
    return _matches(FIGURATIVE, line) or _matches(NOT_NOW, line) or _matches(MILD, line)


DAY_TOTAL_MAX = {"paracetamol": 8, "ibuprofen": 6}
_DAY_TOTAL_COUNT = re.compile(
    r"\b(\d{1,3}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|fifteen|"
    r"twenty|thirty|forty|fifty)\s+(?:of\s+)?(?:(?:the|my|his|her|their)\s+)?"
    r"(pills|tablets|paracetamol|ibuprofen|painkillers|analgesics|meds|medicines?)\b",
)
_DAY_TOTAL_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
                    "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "fifteen": 15,
                    "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50}


def _a_days_dose(line):
    if not _matches(DAY_TOTAL_WORD, line) or _matches(DAY_TOTAL_SIGN, line):
        return False
    if _matches((CHILD_TAKER, CHILD_WORD), line) or _matches(PET_OWN + PET_SUBJECT, line):
        return False
    for count, drug in _DAY_TOTAL_COUNT.findall(line):
        number = _DAY_TOTAL_WORDS.get(count)
        if number is None:
            try:
                number = int(count)
            except ValueError:
                continue
        if number <= DAY_TOTAL_MAX.get(drug, 8):
            return True
    return False


QUESTION_OPENER = (
    r"^\W*(?:(?:ok|okay|so|and|but|well|oh|ah|hmm|actually|please|sorry|hi|hey)\b[ ,-]*)*"
    r"(?:what|whats|what's|why|how|when|where|which|who|whose)\b",
)


ASKING_WHY_IT_HURTS = (
    r"^\W*(?:(?:ok|okay|so|and|but|well|oh|ah|hmm|actually|please|sorry|hi|hey)\b[ ,-]*)*"
    r"(?:what|whats|what's|why|how|which)\b[^.?!]{0,40}"
    r"\b(?:cause|causes|causing|caused|makes?|making|mean|means|behind)\b[^.?!]{0,20}"
    r"\b(?:my|mine)\b",
)


def _the_person_is_in_it(line):
    if _matches(SAID_AS_IT_HAPPENS, line) or _matches(OWN_CRY, line):
        return True
    return _matches(CHEST_URGENT, line)


def _asking_about_the_world(line):
    if line.rstrip().endswith("?") and _matches(WORLD_QUESTION, line):
        return True
    if _the_person_is_in_it(line):
        return False
    return ((_matches(WORLD_QUESTION, line) and _matches(QUESTION_OPENER, line))
            or _matches(ASKING_WHY_IT_HURTS, line))



_SELF_WISH = r"(?:my\s*self|himself|herself|themselves|them\s*selves)"
_OWN_LIFE = r"(?:it(?!\s+with)\b|my\s+(?:own\s+)?life|(?:his|her|their)\s+(?:own\s+)?life)"
DESPAIR = (
    r"\b(?:nothing|nowt)\s+(?:left\s+)?to\s+live\s+for\b"
    r"(?!\s+(?:on|in|at|for|around|round|here|there|about)\b)",
    r"\blife\s+(?:isn'?t|isnt|is\s+not)\s+worth\s+(?:it|living)\b"
    r"(?!\s+(?:in|for|at)\s+\w)",
    r"\b(?:nobody|no\s?one)\s+would\s+(?:notice|care|miss\s+me)\b"
    r"(?=\s*(?:\?|$|[.,!]|\bany\s?more\b|\bat\s+all\b|\bif\s+i\s+(?:was|were|am)\s+(?:gone|"
    r"dead|not\s+here|no\s+longer\s+here)|\bif\s+i\s+(?:died|disappeared|wasnt\s+here|"
    r"werent\s+here|didnt\s+exist|wasnt\s+around|werent\s+around)\b))",
    r"\b(?:dont|don'?t|doesnt|doesn'?t|can'?t|cant)\s+see\s+the\s+point\s+"
    r"(?:in\s+)?(?:" + ANYTHING_LIFE + r"|any\s?more|any\s+of\s+(?:this|it)|of\s+"
    + ANYTHING_LIFE + r"|in\s+(?:" + ANYTHING_LIFE + r"|life|going\s+on|carrying\s+on)"
    r"|of\s+(?:it|this|that)\s+any\s?more)\b",
    r"\bthere(?:'s|s|\s+is)\s+no\s+point\s*(?:\?|$|\bany\s?more\b|\bin\s+(?:anything|"
    r"any\s+of\s+(?:this|it)|life|going\s+on|carrying\s+on)\b|\bto\s+(?:anything|life)\b)",
    r"\bwhat(?:'?s|\s+is)\s+the\s+point\s*(?:\?|$|\bany\s?more\b|\bin\s+(?:"
    + ANYTHING_LIFE + r"|life|any\s+of\s+this|going\s+on)\b|\bof\s+(?:"
    + ANYTHING_LIFE + r"|life|going\s+on)\b)",
    r"\bi\s+(?:just\s+)?(?:cant|can'?t|couldnt|couldn'?t)\s+go\s+on\b"
    r"(?!\s+(?:(?:(?!living\b|existing\b)\w+ing\b)|living\s+(?:with|at|in)\b|"
    r"holiday|holidays|about\b|the|a\b|an\b|monday|tuesday|wednesday|thursday|"
    r"friday|saturday|sunday|\d|with\s+(?:my|his|her|"
    r"their|the|this)\b|in\s+(?:that|this|my|our)\b|stage\b|benefits\b|tour\b|shift\b|"
    r"train\b|bus\b|tub|tube|plane\b|flight\b|course\b|placement\b))",
    r"\b(?:i\s+)?(?:just\s+)?(?:cant|can'?t|couldnt|couldn'?t|don'?t|dont)\s+see\s+"
    r"(?:a|any)\s+way\s+out\b"
    r"(?!\s+(?:of|from)\s+\w)",
    r"\b(?:there\s+is\s+|there'?s\s+|theres\s+)?no\s+way\s+out\b"
    r"(?!\s+(?:of|from)\s+\w)",
    r"\b(?:i\s+)?(?:feel|feeling|felt|am|im|i'm)\s+"
    r"(?:so\s+|really\s+|totally\s+|completely\s+|pretty\s+|a\s+bit\s+)?hopeless\b"
    r"(?!\s+(?:at|with|in|about|of|for)\b)",
    r"\b(?:so\s+|really\s+|just\s+|sick\s+and\s+)?tired\s+of\s+"
    r"(?:everything|it\s+all|all\s+this|all\s+of\s+this|life|being\s+here|existing)\b"
    r"(?=\s*(?:$|[.,!?;]|\band\b))",
    r"\b(?:i\s+have\s+|i'?ve\s+got\s+|i\s+got\s+|there\s+is\s+|there'?s\s+)?"
    r"nothing\s+left\s*(?:\?|$|[.!]*$)",
    r"\b(?:i'?m|im|i\s+am|i'?ve|ive|i\s+have|i\s+feel|i\s+felt|i\s+was)\b[^.?!]{0,25}\b"
    r"(?:done|fed\s+up|sick|tired|had\s+enough)\s+(?:of|with)\s+(?:living|existing)\b"
    + _FLAT_WISH_TAIL,
)

A_BODY_HURTING = (
    r"(?:kill|kills|killing|killed|murder|murders|murdering|murdered|hurt|hurts|hurting|harm|"
    r"harms|harming|harmed|cut|cuts|cutting|starve|starves|starving|starved|shoot|shoots|"
    r"shooting|shot|stab|stabs|stabbing|stabbed|hang|hangs|hanging|hung|hanged|strangle|"
    r"strangles|strangling|strangled|choke|chokes|choking|choked|poison|poisons|poisoning|"
    r"poisoned|burn|burns|burning|burnt|burned|drown|drowns|drowning|drowned|overdose|overdoses|"
    r"overdosing|overdosed|slit|slits|slitting|smother|smothers|smothering|smothered)")
_HURTING_MYSELF = (r"\b(?!poison)" + A_BODY_HURTING + r"\s+my\s*self\b")
_HURTING_THEMSELVES = (r"\b(?!(?:shot|hung|hanged)\b)" + A_BODY_HURTING
                       + r"\s+(?:him|her|them)sel(?:f|ves)\b"
                       + r"(?!\s+laughing\b)(?!\s+out\b)(?!\s+(?:at|in|on)\s+(?:the\s+)?"
                         r"(?:work|gym|office|job|building\s+site|training)\b)"
                       + r"(?!\s+(?:trying|keeping|making|pleasing|doing|working|getting|"
                         r"being|to\s+(?:keep|make|please|get|be|help|prove|show))\b)"
                       + r"(?!\s+on\s+(?!purpose\b))"
                       + r"(?!\s+with\s+(?:the|his|her|their|my|an?)\s+(?:epi\s?pen|epipen|"
                         r"insulin\s?pen|inhaler|syringe|auto[-\s]?injector|needle))")

_SOME_OF_A_MEDICINE = (
    r"\b(?:take|taken|taking|took|swallow|swallowed|swallowing|down|downing|downed|neck|necking|"
    r"necked|pop|popping|popped)\s+(?:all\s+(?:of\s+)?|the\s+rest\s+of\s+|"
    r"a\s+(?:whole|bunch|load|handful)\s+of\s+)(?:my|these|those|the)?\s*"
    r"(?:pills?|tablets?|capsules?|caplets?|meds|medication|painkillers?|paracetamol|ibuprofen|"
    r"antidepressants?|sleeping\s+pills?|tranquill?i[sz]ers?)\b")

SELF_HARM = (
    r"\b(?:kill|killing|killed|hurt|hurting|harm|harming|cut|cutting|starve|starving)\s+my\s*self\b",
    r"\b(?:want|wanna|wanting|going|gonna|plan|planning|planned|ready|decided|thinking\s+of|"
    r"thinking\s+about|thought\s+of|thought\s+about)\s+(?:to\s+)?" + _HURTING_MYSELF,
    r"\b(?:want|wanna|wanting|going|gonna|plan|planning|planned|ready|decided|thinking\s+of|"
    r"thinking\s+about|thought\s+of|thought\s+about)\s+(?:to\s+)?" + _SOME_OF_A_MEDICINE,
    *SELF_HARM_CUT_NO_OBJECT,
    *SELF_HARM_OWN_PART,
    *SELF_HARM_FLAT_WISH,
    r"\b(?:want|wanna|wanting|going|plan|planning|ready|decided)\s+to\s+(?:die|kill\s+my\s*self|"
    r"end\s+(?:it(?!" + END_IT_WITH + r")|my\s+life))\b",
    r"\bi\s+(?:keep\s+|often\s+|sometimes\s+|constantly\s+|still\s+|just\s+|really\s+|"
    r"cant\s+stop\s+|can'?t\s+stop\s+)?(?:think|thinking|thought)\s+(?:about|of)\s+"
    r"(?:dying(?!\s+(?:my|her|his|their|our)\s+hair)|killing\s+my\s*self|"
    r"ending\s+it(?!" + END_IT_WITH + r")|suicide|self[-\s]?harm)\b",
    r"\bdon't\s+want\s+to\s+(?:"
    r"live\b(?!\s+(?:in|at|on|near|next\s+to|off|abroad|with)\b)"
    r"|be\s+alive(?!\s+(?:in|on)\s+(?:that|this|the)\s+(?:photo|picture|pic|video|footage|"
    r"stream|recording|thumbnail)\b)"
    r"|be\s+here|exist"
    r"|wake\s+up\b(?!\s+(?:early|at\s+(?:\d|one\b|two\b|three\b|four\b|five\b|six\b|seven\b|"
    r"eight\b|nine\b|ten\b|eleven\b|twelve\b|noon\b|midnight\b|dawn\b|sunrise\b)|before\b|"
    r"by\b|so\b))"
    r"|(?:carry|go)\s+on\b(?!\s+(?:with\b|the\b|a\b|an\b|to\b|about\b|in\b|on\b|holiday|"
    r"holidays|course|(?:(?!living\b|existing\b)\w+ing\b))))",
    r"\bdon't\s+want\s+to\s+(?:live|be\s+alive|be\s+here|exist|wake\s+up|(?:carry|go)\s+on)\b"
    r"[a-z']{0,20}(?:[\s'][a-z']{1,15}){0,4}\s+(?:any\s?more|no\s?more|at\s+all|altogether|"
    r"for\s+good|without\s+(?:him|her|them|you|it|anyone|anybody|myself|my\s+\w+))\b",
    r"\b(?:want|wants|wanted|wanting|wanna)\s+to\s+(?:not\s+(?:be\s+alive|exist)|"
    r"stop\s+(?:existing|being\s+alive))\b"
    r"(?=\s*(?:$|[.,!?;]|\b(?:any\s?more|no\s?more|at\s+all|now|tonight|altogether|for\s+good)\b))",
    r"\bdon't\s+want\s+to\s+be\s+around\s+(?:any\s?more|no\s?more)\b"
    r"(?=\s*(?:$|[.,!?;]|\b(?:at\s+all|now|tonight|today|altogether|ever|for\s+good)\b))",
    r"\bno\s+(?:reason|point)\s+(?:to|in)\s+(?:live|living|going\s+on|carrying\s+on)\b",
    r"\bbetter\s+off\s+(?:dead|without\s+me|if\s+i\s+was\s+gone|if\s+i\s+weren't\s+here)\b",
    r"\bsuicid(?:e|al)\b", r"\bself[-\s]?harm(?:ing|ed)?\b",
    r"\boverdos(?:e|ed|ing)\b",
    r"\b(?:took|taken|swallowed|had)\s+(?:too\s+many|a\s+(?:whole|bunch|load|handful)\s+of)\s+(?:pills|tablets|paracetamol|ibuprofen|meds)\b",
    r"\b(?:thinking|thought|thinking\s+about)\s+(?:about\s+)?(?:killing\s+my\s*self|suicide|ending\s+(?:it|my\s+life)|not\s+being\s+here)\b",
    r"\b(?:feel|feels|felt|feeling)\s+(?:like|as\s+if)\s+(?:ending\s+" + _OWN_LIFE + r"|dying"
    r"|kill(?:ing)?\s+" + _SELF_WISH + r"|not\s+being\s+here)\b"
    r"(?!\s*(?:,|:)?\s*(?:of\s+(?:embarrass\w*|shame|laughter|boredom)|laughing|embarrass\w*|mortified"
    r"|cringe\w*|my\s+hair))",
    r"\b(?:keep|keeps|kept)\s+(?:thinking|having\s+thoughts)\s+(?:about|of)\s+"
    r"(?:ending\s+" + _OWN_LIFE + r"|killing\s+" + _SELF_WISH + r"|suicide|dying|not\s+being\s+here)\b",
    r"\b(?:i|im|i'?m|ive|i'?ve|id|i'?d)\b[^.?!]{0,12}?\b(?:have|had|having)\s+thoughts?\s+"
    r"(?:about|of)\s+(?:ending\s+" + _OWN_LIFE + r"|killing\s+" + _SELF_WISH + r"|suicide|"
    r"not\s+being\s+here)\b",
    r"^\s*(?:just\s+|been\s+|still\s+|and\s+)?(?:having|had)\s+thoughts?\s+(?:about|of)\s+"
    r"(?:ending\s+" + _OWN_LIFE + r"|killing\s+" + _SELF_WISH + r"|suicide|not\s+being\s+here)\b",
    r"\bthink(?:s|ing)?\s+(?:about|of)\s+(?:ending\s+" + _OWN_LIFE + r"|killing\s+" + _SELF_WISH + r"|suicide)\b",
    r"\bend\s+(?:it\s+all|my\s+(?:own\s+)?life)\b",
    r"\bend(?:ing)?\s+(?:it\s+all|my\s+(?:own\s+)?life)\b",
    r"\bcan't\s+(?:go\s+on|carry\s+on)\s+(?:any\s?more|like\s+this)\b",
    r"\b(?:hang|hanged|hung|hanging)\s+my\s*self\b",
    r"\b(?:wants?|want|wanna|wanting|going|plan|plans?|planning|thinking|thought|thoughts|"
    r"considering|tempted|ready|decided|feels?\s+like)\b[^.?!]{0,18}\b(?:to\s+)?(?:hang|hanging|"
    r"jump|jumping|drown|drowning)\s+(?:my\s*self|himself|herself|themselves|off\s+(?:a|the|this)\s+"
    r"(?:bridge|roof|building|cliff|balcony|ledge|car\s*park))\b"
    r"(?!\s+in\s+(?:work|emails?|paperwork|admin|debt|chores|housework))",
    r"\b(?:thought|thoughts?|thinking|kept\s+thinking|keep\s+thinking|keeps\s+thinking|dreamt|dreaming)"
    r"\s+(?:about|of)\s+(?:step|stepping|walk|walking|stand|standing|lie|lying|lay|jump|jumping|throw|throwing)"
    r"\s+(?:my\s*self\s+)?(?:"
    r"(?:in\s+front\s+of|under)\s+(?:traffic|(?:a\s+|the\s+)?bus|(?:a\s+|the\s+)?train|"
    r"(?:a\s+|the\s+)?car|(?:a\s+|the\s+)?lorry|(?:a\s+|the\s+)?truck)"
    r"|(?:into|onto|on)\s+(?:traffic|the\s+tracks|the\s+track|the\s+railway\s+line)"
    r")\b"
    r"(?!\s+(?:queue|stop|station|doors?|board|platform|screen|ticket\s+machine|shelters?|awning|"
    r"canopy|umbrella))"
    r"(?![^.?!]*\b(?:photo|photos|picture|pictures|pic|pics|selfie|selfies|photograph|"
    r"photographs)\b)",
    r"\bi\b[^.?!]{0,20}\b(?:could|would|might|should|want\s+to|going\s+to)\s+(?:jump|jumping)\s+"
    r"(?:off|from)\s+(?:a|the|this)\s+(?:bridge|roof|building|cliff|balcony|ledge|car\s*park)\b"
    r"(?!\s+into\s+the\s+(?:pool|water|sea|lake|river|hay|snow))",
    r"\b(?:drown|drowning)\s+my\s*self\b(?!\s+in\s+(?:work|emails?|paperwork|admin|debt|chores|"
    r"housework|the\s+washing))",
    r"\blocked\s+(?:him|her|them)sel(?:f|ves)\s+in\b.{0,40}\b(?:pills|tablets|razor|blades?|knife)\b",
) + DESPAIR + WISH_BY_MODAL
_NOTHING_LEFT_PROBE = "i have nothing left"


def _nothing_left_clause():
    for clause in reversed(DESPAIR):
        try:
            if re.search(clause, _NOTHING_LEFT_PROBE, re.I):
                return (clause,)
        except re.error:
            continue
    return DESPAIR[-1:]


NOTHING_LEFT = _nothing_left_clause()
DESPAIR_WITHOUT_NOTHING_LEFT = tuple(clause for clause in DESPAIR if clause not in NOTHING_LEFT)
from .safety_phrases import (
    ABUSE, ABUSER, ABUSE_DISCLOSURE,
    ABUSE_DISCLOSURE_FINE, ABUSE_FINE, ABUSE_HEAD_INTO,
    ABUSE_HIT_ME, ABUSE_MEMORY, ABUSE_NOW,
    ABUSE_PURSUIT_HARD, ABUSE_VERB, ABUSE_VERBAL,
    ABUSE_VERBAL_FINE, ABUSE_VERBAL_LABEL, ABUSE_VERBAL_MAD,
    ABUSE_VERBAL_PERSON, ABUSE_VERBAL_SUBJECT, ABUSE_VERB_PART,
    ASK_AFTER_ME, BLOW_THINGS, CHILD_AGGRESSOR,
    CHILD_HIT_NOW, CLOSE, DYING_OTHER,
    GAME_AFTER_ME, GAME_PLAYED, GAME_WORD_STOP,
    GRIP_GAME, GRIP_GAME_FENCE, GRIP_NOT_AN_ASSAULT,
    GAME_NOT_A_BLOW, GRIP_NOT_AN_ASSAULT_STR, HAS_ME_SUBJECT, HIT_AS_A_CHILD,
    HIT_BY_A_VEHICLE, HIT_THING_NOT_PERSON, I_DID_NOT_HIT,
    I_HIT_SOMEONE, MONEY_NAMED, NOT_A_FEAR,
    OTHERS, PARTNER_CLOSE, PEOPLE,
    PERSON, PLAY_FACE_REPLIES, PURSUIT,
    PURSUIT_FEAR, PURSUIT_LOUD, PURSUIT_OUTSIDE,
    PURSUIT_PLACE_WORK, PURSUIT_SUBJECT, PURSUIT_SUBJECT_EX,
    REMORSE_FOR_THE_ACT, SELF_HARM_NEEDS_PERSON, SELF_OWN_DYING,
    SOFT_FACE_PUSH, SOFT_FACE_STOP, SOMEONE_HOLDS_THE_MONEY,
    THREAT_COERCIVE, THREAT_SUBJECT, _NOT_A_THREAT,
    _REFUSED_EXIT, _THE_BLOW, _THE_HAND,
    _THE_ONE_HIT, _both_here,
)


ABUSE_CHILD_TAKES_MONEY = (
    r"\b(?:money|wages|pay|pension|pensions|benefits|bank\s+card|debit\s+card|bank\s+account|"
    r"keys|savings|my\s+own\s+money)\b",
)


ABUSE_PARTNER_DID_IT = (
    r"\bmy\s+(?:husband|wife|partner|boyfriend|girlfriend|ex|fiance|fiancee|stepdad|stepmum|"
    r"stepmom|carer)\b[^.?!]{0,25}\b(?:corner(?:ed|s)?|pinned|trapped|backed|blocked|pushed|"
    r"shoved|held)\b",
)


HIT_WITH_A_THING = (
    r"\bh(?:it|its|itting|urt)\s+(?:me|us|him|her|them)\s+with\s+"
    r"(?:a|an|the|his|her|their|my|your)\b",
)
_GRANDCHILD_OF_AN_AGE = (
    r"(?:little|small|young|baby|toddler)\s+(?:grandson|granddaughter)|"
    r"(?:grandson|granddaughter)\s+(?:is\s+)?(?:one|two|three|four|1|2|3|4)\b|"
    r"(?:one|two|three|four|1|2|3|4)\s*(?:year|yr)[\s-]*old\s+(?:grandson|granddaughter)")
A_SMALL_CHILD_SAID = re.compile(
    r"\b(?:toddlers?|nursery|pre-?school|playgroup|bab(?:y|ies)|small\s+child|"
    r"(?:one|two|three|four|1|2|3|4|eighteen|18)\s*(?:year|yr)[\s-]*old|"
    r"(?:eighteen|18)\s*months?|little\s+(?:boy|girl|one|lad|fella)|"
    r"" + _GRANDCHILD_OF_AN_AGE + r"|"
    r"my\s+(?:son|daughter|boy|girl)\s+is\s+(?:one|two|three|four|1|2|3|4)\b)\b",
    re.IGNORECASE)
A_GRANDCHILD_OF_AN_AGE = re.compile(_GRANDCHILD_OF_AN_AGE, re.IGNORECASE)
A_GROWN_BLOW = re.compile(
    r"\b(?:punch(?:es|ed|ing)?|knee(?:s|d)?|head[-\s]?butt(?:ed|s|ing)?)\b[^.?!]{0,24}"
    r"\b(?:stomach|belly|ribs?|groin|kidneys?|back|jaw|nose)\b",
    re.IGNORECASE)
A_LASH_VERB = (r"bit(?:es|ing)?|hits?|hitting|kick(?:s|ed|ing)?|scratch(?:es|ed|ing)|"
               r"slap(?:s|ped|ping)?|thump(?:s|ed|ing)?|punch(?:es|ed|ing)?|"
               r"pull(?:s|ed)?\s+my\s+hair|spit(?:s|ting)?")
A_SMALL_CHILD_LASHES_OUT = re.compile(
    r"\b(?:" + A_LASH_VERB + r")\s+(?:at\s+)?me\b",
    re.IGNORECASE)
A_BARE_ACTOR_LASH = re.compile(
    r"\b(?:he|she|it|hes|shes|they|theyre)\b(?:\s+\w+){0,2}?\s+(?:" + A_LASH_VERB + r")"
    r"\s+(?:at\s+)?me\b",
    re.IGNORECASE)


SMALL_CHILD_REPLY_GIVEN = re.compile(
    r"that is what a small child does|last things a small child drops|"
    r"a small child has no other way to say", re.IGNORECASE)


def _a_small_child_did_it(line, memory):
    if not A_SMALL_CHILD_LASHES_OUT.search(line):
        return False
    if A_GROWN_AGE.search(line):
        return False
    if A_SMALL_CHILD_SAID.search(line):
        return True
    if A_GROWN_BLOW.search(line):
        return False
    if not A_BARE_ACTOR_LASH.search(line):
        return False
    said = ""
    for turn in reversed((memory.get("turns") or [])[-3:] if isinstance(memory, dict) else []):
        if isinstance(turn, dict) and turn.get("user"):
            said += " " + _norm(str(turn["user"]))
        if isinstance(turn, dict) and turn.get("bot") \
                and SMALL_CHILD_REPLY_GIVEN.search(_norm(str(turn["bot"]))):
            said += " " + _norm(str(turn["bot"]))
    return bool(A_SMALL_CHILD_SAID.search(said))


LENDER_FINE = (
    r"\b(?:loan\s*-?\s*sharks?|loan\s+sharking|illegal\s+lender|unlicensed\s+lender|"
    r"money\s*lenders?|payday\s+lenders?|payday\s+loans?)\b",
)
NAMED_PERSON = (
    r"\b(?:my|his|her|their|our)\s+(?:" + ABUSER + r")\b",
)

_HIT_ME = re.compile(r"\b(?:hits?|hitting|knocked|knocks?|beats?|punched)\s+(?:me|us)\b")
_SUBJECT_TAIL = re.compile(
    r"(?:\s+(?:has|had|have|really|just|nearly|almost|so|properly|completely|truly|still|also|"
    r"it|its|it's|that|this|which|and|then))*\s*$")
LOSS_SUBJECT_AT_END = tuple(pattern + r"\s*$" for pattern in LOSS_SUBJECT)
ABUSE_NOT_HIT = THREAT_COERCIVE + tuple(
    arm for arm in ABUSE[len(THREAT_COERCIVE):] if arm not in ABUSE_HIT_ME)


def _hit_by_a_loss(line):
    clauses = list(_HIT_ME.finditer(line))
    if not clauses:
        return False
    for match in clauses:
        window = _SUBJECT_TAIL.sub("", line[max(0, match.start() - 80):match.start()])[-60:]
        if not _matches(LOSS_SUBJECT_AT_END, window):
            return False
    return True


STOP_TAIL = (r"\s*(?:$|[.,!?;]|(?:because|since|when|whenever|if|now|at\s+all|anymore|"
             r"any\s?more|tonight|today|again|at\s+the\s+moment|at\s+night|right\s+now|"
             r"in\s+the\s+end)\b)")
WHERE_TAIL = (r"\s+(?:at\s+home|at\s+work|at\s+night|where\s+i\s+live|here|on\s+my\s+own|"
              r"in\s+(?:my|the|this|our)\s+(?:own\s+)?(?:home|house|flat|place|bed)|"
              r"where\s+i\s+(?:live|am)|where\s+we\s+live)\b")
PERSON_TAIL = r"\s+(?:with|around|near|by|on)\s+(?:\w+\s+){0,3}" + _PERSON + r"\b"
_SAFE_TAIL = "(?=" + STOP_TAIL + "|" + WHERE_TAIL + "|" + PERSON_TAIL + ")"
UNSAFE = (
    r"\b(?:i'?m|im|i\s+am)\s+not\s+safe\b" + _SAFE_TAIL,
    r"\b(?:i\s+)?(?:don'?t|do\s+not|dont)\s+feel\s+safe\b" + _SAFE_TAIL,
    r"\bnot\s+safe\s+(?:at\s+home|in\s+my\s+own\s+(?:home|house|flat)|where\s+i\s+live|here|"
    r"in\s+my\s+house|in\s+the\s+house)\b",
    r"\b(?:i\s+)?feel\s+(?:unsafe|in\s+danger)\b(?!\s+(?:" + _AWAY_TAIL + r"))",
)

_FLAME_THING = (
    r"\b(?:fireplace|fire\s*place|wood\s*burner|woodburner|log\s*burner|multi\s*fuel\s*burner|"
    r"grill|grille|barbecue|barbeque|bbq|barbie|fire\s*pit|brazier|candle|candles|"
    r"wood\s*stove|log\s*fire|coal\s*fire|open\s*fire|stove|hob|rings?)\b"
)
FLAMES_NOT_FIRE = (
    r"\b(?:old|twin|former|new)\s+flames?\b",
    r"\bflames?\s+(?:grilled|grill|retardant|proof|effect|test|war|thrower|pit|bait)\b",
    r"\bflame\s*proof\w*\b",
    _FLAME_THING + r"[^.?!]{0,30}\bflames?\b",
    r"\bflames?\b[^.?!]{0,30}" + _FLAME_THING,
    r"\b(?:lit|light|lighting|lighted|made|make|making|started|starting|built|build|put)\s+"
    r"(?:the|a|my|our|this)\s+(?:fire|burner|stove|barbecue|bbq|grill)\b[^.?!]{0,30}\bflames?\b",
    r"\bflames?\s+(?:on|in)\s+(?:the\s+)?(?:tv|telly|television|screen|monitor)\b",
    r"\b(?:on|in|from)\s+(?:the\s+|a\s+|my\s+|our\s+)?(?:tv|telly|television|screen|monitor|"
    r"photo|picture|film|movie|video|game|painting|drawing|dream|dreams|nightmare)\b"
    r"[^.?!]{0,20}\bflames?\b",
    r"\bflames?\b[^.?!]{0,20}\b(?:on\s+)?(?:the\s+|a\s+|my\s+|our\s+)?(?:tv|telly|television|"
    r"screen|monitor|photo|picture|film|movie|video|game|painting|drawing|dream|dreams|nightmare)\b",
    r"\b(?:plans?|hopes?|dreams?|dreamt|diets?|careers?|projects?|budgets?|savings|marriage|"
    r"relationship|business|chances?|grades?|reputation|weekend|strateg\w*|team|faith|trust|"
    r"confidence|nerves|nervousness|arguments?|negotiations?|deal|interview|holiday|wedding|"
    r"prospects?|retirement|pension|investments?|shares?|portfolio|"
    r"toast|toastie|toasties|dinner|teas|supper|lunch|breakfast|roast|chicken|sausages?|bacon|"
    r"bread|rice|pasta|pizza|pie|pies|curry|stew|casserole|lasagne|lasagna|soup|sauce|chips|"
    r"potatoes|pancakes?|porridge|biscuits?|muffins?|crumpets?|cakes?|meat|fish|veg|vegetables|garlic|"
    r"onions?|beans|food|pudding|turkey|stuffing|yorkshire\s+puddings?)\b[^.?!]{0,25}"
    r"\b(?:went|gone|go|goes|going|is|was|are|were|been|up)\s+(?:up\s+)?in\s+flames\b",
)
SOMEONES = (r"(?:(?:my|his|her|their|our|your|the)\s+(?:[\w-]+\s+){0,1}[\w-]+'?s\s+)?")
CLOTHES_FIRE = (
    SOMEONES + GARMENT + r"[^.?!]{0,20}"
    r"\b(?:is\s+|was\s+|'s\s+|are\s+|were\s+|got\s+|has\s+gone\s+|had\s+gone\s+)?"
    r"(?:on\s+fire|alight|ablaze)\b",
    SOMEONES + GARMENT + r"[^.?!]{0,20}\bcaught\s+(?:on\s+)?fire\b",
    r"\b(?:i|he|she|they)\s+(?:am|is|are|was|were)\s+(?:on\s+fire|alight|ablaze)\b",
    r"\bset\s+(?:my|his|her|their)\s+(?:coat|shirt|top|sleeve|trousers|clothes)\s+alight\b",
    SOMEONES + GARMENT + r"(?=[^.?!]{0,20}\b(?:caught|catches|took|takes|touched|touches|"
    r"grabbed|grabs|lapped|laps|licked|licks|caught\s+light)\s+(?:the\s+|a\s+)?flames?\b)",
    SOMEONES + GARMENT + r"(?=[^.?!]{0,25}\bwent\s+up\s+in\s+flames\b)",
    SOMEONES + GARMENT + r"(?=[^.?!]{0,12}\b(?:went|goes|had\s+gone|has\s+gone|gone)\s+up\b"
    r"(?!\s+(?:in\s+)?(?:price|prices|by|to|from|again|a\s+size|two\s+sizes|\d|"
    r"a\b|an\b|the\b|some\b|one\b|two\b)))",
    SOMEONES + GARMENT + r"(?=[^.?!]{0,25}\b(?:is|was|were|are|'s)\s+(?:in|among)\s+the\s+flames\b)",
    r"\b(?:the\s+|a\s+)?flames?\b[^.?!]{0,20}\b(?:caught|catches|took|takes|touched|"
    r"touches|grabbed|lapped|licked|reached)\b(?=[^.?!]{0,8}" + GARMENT + r")",
    SOMEONES + GARMENT + r"(?=[^.?!]{0,20}\bcaught\s+light\b)",
    r"\b(?:i|he|she|they|we)\s+caught\s+(?:on\s+)?fire\b",
    r"\b(?:my|his|her|their)\s+(?:son|daughter|husband|wife|partner|dad|mum|father|mother|"
    r"brother|sister|friend|baby|child|kid|boy|girl)\s+(?:has\s+|had\s+)?caught\s+"
    r"(?:on\s+)?fire\b",
)
PAN_FIRE_SPREAD = (
    r"\b(?:hood|extractor|ceiling|wall|walls|curtains?|cupboards?|shelf|shelves|worktop|"
    r"kitchen|everywhere|spreading|spread|out\s+of\s+control)\b",
    r"\bsmok\w*\b",
    r"\b(?:alarm|trapped|can'?t\s+get\s+out|cannot\s+get\s+out)\b",
)

VEHICLE_STILL_FIRE = (
    r"\b(?:on\s+fire|caught\s+fire|alight|ablaze|in\s+flames|flames|smok\w*)\b",
)
VEHICLE_EXHAUST_HARD = (
    r"\b(?:on\s+fire|caught\s+fire|alight|ablaze|in\s+flames|flames?|bonnet|engine\s+bay|"
    r"dashboard|inside\s+the\s+car|coming\s+into\s+the\s+car)\b",
)
VEHICLE_BURNING_A_PERSON = (
    r"\bburn\w*\b[^.?!]{0,20}\b(?:my|his|her|their|your|our)\s+(?:hand|hands|arm|arms|"
    r"leg|legs|finger|fingers|thumb|thumbs|wrist|wrists|foot|feet|toe|toes|face|cheek|"
    r"shoulder|knee|eye|eyes|skin|back|neck|thigh)\b",
)
VEHICLE_BURNING_A_PERSON_HARD = (
    r"\b(?:on\s+fire|caught\s+fire|alight|ablaze|in\s+flames|flames?|smok\w*|"
    r"everyone\s+out|get\s+out)\b",
)
VEHICLE_FIRE_OVER_HARD = (
    r"\b(?:on\s+fire|alight|ablaze|in\s+flames|flames?|still\s+(?:burning|smoking|smoking)|"
    r"still\s+smok\w*|burning\s+now|right\s+now|everyone\s+out)\b",
)
VEHICLE_NOT_FIRE = (
    r"\b(?:burning|burns|burnt|using|uses|used|losing|loses)\s+(?:a\s+bit\s+of\s+|some\s+|"
    r"too\s+much\s+)?(?:oil|fuel|petrol|diesel|coolant|calories|money)\b",
    r"\b(?:oil|fuel)\s+(?:burning|consumption|use)\b",
)


SMELL_ON_A_THING = re.compile(r"\b(?:" + _SMELLY_THING + r")\b", re.I)

ROOM_OR_HOUSE = (
    r"\b(?:house|flat|apartment|kitchen|room|living\s+room|bedroom|hall|hallway|landing|"
    r"building|stairwell|stairs|ceiling|floor\s?boards?)\b",
)

WHOLE_OF = (r"(?:my|his|her|their|your|mums?|mum'?s|dads?|dad'?s)\s+whole\s+(?:packet|pack|box|"
            r"bottle|strip|blister|tub)\s+of")
CHILD_TAKER = (
    r"(?:(?:my|our|his|her|their)\s+(?:son|daughter|child|kid|baby|toddler|boy|girl|grandson|"
    r"granddaughter|grandchild|niece|nephew|little\s+one)|\d+\s*(?:year|yr)s?[\s-]?old|"
    r"the\s+(?:baby|toddler|child|kid))\b"
)
CHILD_DOSE_AFTER = (
    r"\b(?:for|to)\s+(?:my|our|his|her|their|the|a|an)\s+(?:son|daughter|child|kid|baby|toddler|"
    r"boy|girl|little\s+one|grandson|granddaughter|grandchild|niece|nephew|newborn|\d+\s*"
    r"(?:year|yr)s?[\s-]?old)\b"
)
DOSE_ALREADY_GIVEN = (
    r"\b(?:gave|given|dosed|took|taken|swallowed|fed)\b",
)

CHILD_MEDICINE = (
    CHILD_TAKER + r"[^.?!]{0,25}\b(?:swallowed|swallowing|drank|drunk|drinking|ate|eaten|took|"
    r"taken|had|finished|downed|necked|gulped|sucked|sipped|given|gave)\b[^.?!]{0,25}"
    r"\b(?:the|a|his|her|my|another)\s+(?:whole\s+)?(?:bottle|packet|pack|box|strip|blister|tub)\b"
    r"[^.?!]{0,20}\b" + MEDICINE + r"\b",
    CHILD_TAKER + r"[^.?!]{0,25}\b(?:had|given|gave|took|taken|swallowed|drank)\b[^.?!]{0,25}"
    r"\b(?:too\s+many|extra|double|another|two|three|four|several)\s+(?:doses?|spoonfuls?|"
    r"mouthfuls?|syringes?)\b[^.?!]{0,20}\b" + MEDICINE + r"\b",
    r"\b(?:gave|give|giving|dosed|fed|measured)\s+(?:my|our|his|her|their)\s+(?:son|daughter|"
    r"child|kid|baby|toddler|boy|girl|little\s+one)\b[^.?!]{0,25}"
    r"\b(?:too\s+much|too\s+many|double|extra|twice|another\s+dose|two\s+doses)\b"
    r"[^.?!]{0,20}\b" + MEDICINE + r"\b",
    CHILD_TAKER + r"[^.?!]{0,25}\b(?:swallowed|swallowing|drank|drunk|drinking|took|taken|had|"
    r"downed|gulped|sucked|sipped)\b[^.?!]{0,20}\btoo\s+much\b[^.?!]{0,20}\b" + MEDICINE + r"\b",
    CHILD_TAKER + r"[^.?!]{0,40}\b(?:got|get|gets|getting)\s+into\s+(?:the|my|his|her|their|a)\s+"
    r"(?:bottle\s+of\s+|packet\s+of\s+|box\s+of\s+)?" + MEDICINE + r"\b",
    CHILD_TAKER + r"[^.?!]{0,25}\b(?:took|taken|swallowed|ate|eaten|had|nicked|downed|found)\b"
    r"[^.?!]{0,20}\b(?:my|your|mums?|mum'?s|dads?|dad'?s|nans?|nana'?s|grans?|gran'?s|"
    r"nanny'?s|grandad'?s|grandma'?s|the|these|those)\s+(?:\w+\s+)?(?:pills|tablets|"
    r"sleeping\s+(?:pills|tablets)|antidepressants|painkillers|medicines?|meds|vitamins?|"
    r"paracetamol|ibuprofen|tranquill?i[sz]ers?)\b",
    r"\b(?:too\s+many|too\s+much)[^.?!]{0,25}?\b" + MEDICINE +
    r"\b[^.?!]{0,20}?" + CHILD_DOSE_AFTER,
    r"\b(?:gave|give|giving|given|dosed|dosing|fed|measuring|measured|squirted)\s+"
    r"(?:her|him|them)\b[^.?!]{0,25}\b(?:(?:" + DOSE_AMOUNT +
    r")|\b(?:too\s+many|too\s+much)\b|an?\s+(?:extra|double)\s+dose)[^.?!]{0,20}\b" +
    MEDICINE + r"\b",
    r"\b(?:gave|give|giving|given|dosed|dosing|fed|measuring|measured|squirted)\s+"
    r"(?:her|him|them)\b[^.?!]{0,25}\b(?:\b(?:too\s+many|too\s+much)\s+(?:doses?|"
    r"spoonfuls?|mouthfuls?|syringes?)\b|\b(?:two|three|four|several)\s+(?:doses?|spoonfuls?)\b"
    r"[^.?!]{0,15}\b(?:at\s+once|together|at\s+the\s+same\s+time|in\s+(?:an|one|1)\s+hour|"
    r"within\s+an\s+hour|in\s+\d+\s+minutes|back\s+to\s+back)\b)",
    r"\b(?:too\s+many|too\s+much)\s+(?:doses?|spoonfuls?|mouthfuls?|syringes?)\b"
    r"[^.?!]{0,15}?" + CHILD_DOSE_AFTER,
)

PILLS_OVERDOSE = (
    r"\b(?:took|taken|swallowed|had|downed|ate|eaten|popped|necked)\b[^.?!]{0,25}"
    r"\b(?:too\s+(?:many|much)|a\s+lot\s+of|loads\s+of|lots\s+of|a\s+(?:whole|bunch|load|handful|pile|packet|"
    r"box|strip|blister)\s+of|a\s+whole\s+(?:packet|pack|box|bottle|strip|blister)\s+of|"
    r"the\s+whole\s+(?:packet|pack|box|strip|blister)|" + WHOLE_OF + r"|"
    r"all\s+(?:of\s+)?(?:my|his|her|their|mums?|mum's|dads?|dad's|the|these|those)|"
    r"[6-9]\s+(?:of\s+)?|[1-9]\d{1,}\s+(?:of\s+)?|"
    r"(?:six|seven|eight|nine|ten|eleven|twelve|fifteen|twenty|thirty|forty|fifty))"
    r"\b[^.?!]{0,20}"
    r"\b(?:pills|tablets|paracetamol|ibuprofen|painkillers|meds|medicines?|sleeping\s+pills|"
    r"antidepressants)\b",
    r"\boverdos(?:e|ed|ing)\b",
)
DOSE_REGULAR = (
    r"\b(?:a|per|each)\s+(?:day|week|dose)\b",
    r"\b(?:daily|every\s+day|once\s+a|twice\s+a|three\s+times\s+a)\b",
    r"\bat\s+a\s+time\b",
    r"\b(?:as|when)\s+(?:needed|required)\b",
    r"\bprescri(?:bed|ption)\b",
)
PACK_FINE = (
    r"\b(?:out\s+of\s+date|expired|in\s+the\s+bin|threw|thrown|unopened|sealed|still\s+full|"
    r"left\s+(?:in|on)|in\s+the\s+cupboard|to\s+buy|bought|pharmacy|prescription\s+ready)\b",
)
OVERDOSE_REAL_THING = (
    r"\bpills?\b", r"\btablets?\b", r"\bparacetamol\b", r"\bibuprofen\b", r"\binsulin\b",
    r"\bmeds\b", r"\bmedicines?\b", r"\bbleach\b", r"\bantifreeze\b", r"\bheroin\b",
    r"\bopioids?\b", r"\btramadol\b", r"\bantidepressants?\b", r"\bchemotherapy\b",
)


def _overdose_of_a_treat(line):
    return (_matches(OVERDOSE_OF_A_TREAT, line) or _matches(OVERDOSE_WORK, line)) \
        and not _matches(OVERDOSE_REAL_THING, line)


OVERDOSE_WORK = (
    r"\boverdosed?\s+on\s+(?:work|meetings?|emails?|paperwork|spreadsheets?)\b",
)
POISON_SWALLOW_VERB = (
    r"\b(?:swallowed|swallowing|drank|drunk|drinking|eaten|eating|gulped|sucked|licked|tasted)\b",
)
A_SMALL_AMOUNT = (
    r"\b(?:a\s+bit|a\s+little|a\s+small\s+amount|a\s+mouthful|a\s+sip|one\s+sip|"
    r"one\s+mouthful|a\s+taste|a\s+drop|a\s+dab|a\s+smear|a\s+swig|a\s+lick|some)\b",
)
MILD_PRODUCT_BIG = (
    r"\b(?:whole|full|tubes?|packets?|packs?|bottles?|litres?|pint|glass\s+full|handful|boxes?|"
    r"box|bar)\b",
)
MILD_HARMLESS = (
    r"\b(?:soap|toothpaste|sun\s?cream|moisturiser|moisturizer)\b",
)
MILD_TAKEN_BY_A_CHILD = (
    r"\b(?:my|our|her|his|their|the)\s+(?:son|daughter|child|kid|baby|toddler|boy|girl|niece|"
    r"nephew|grandson|granddaughter|stepson|stepdaughter)\b",
    r"\b(?:little\s+(?:boy|girl|one)|a\s+child|a\s+toddler|my\s+little\s+\w+)\b",
)
FUEL_AND_SOLVENT = (
    r"petrol|petroleum|diesel|paraffin|kero?scene|lighter\s+fluid|turpentine|white\s+spirit|"
    r"paint\s?thinner|thinners?|meths|methylated\s+spirits?|lamp\s+oil|engine\s+oil|"
    r"screen\s?wash|de-?icer|antifreeze|coolant"
)
PACK_COUNT = (r"(?:two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|\d{1,3}|"
              r"a\s+couple|a\s+few|a\s+handful|couple|few|several|both|all)")
PACK_WORD = (r"(?:packs?|packets?|boxes?|box|strips?|blisters?|blister\s+packs?|bottles?|tubes?|"
             r"tubs?|sachets?)")
PACK_DRUG = (r"(?:pills|tablets|capsules|caplets|paracetamol|acetaminophen|ibuprofen|nurofen|"
             r"brufen|panadol|calpol|co[\s-]?codamol|codamol|painkillers|analgesics|meds|"
             r"medicines?|sleeping\s+(?:pills|tablets)|antidepressants|tranquill?i[sz]ers?|insulin)\b")
TOOK_MANY_PACKS = (
    r"\b(?:took|taken|swallowed|downed|necked|popped|had|ate|eaten|emptied|finished)\b"
    r"[^.?!]{0,20}\b" + PACK_COUNT
    + r"\s+(?:more\s+)?(?:of\s+)?(?:the\s+|my\s+|these\s+|those\s+)?(?:other\s+)?"
    + PACK_WORD
    + r"\b(?:\s+of)?[^.?!]{0,25}\b" + PACK_DRUG,
    r"\b(?:took|taken|swallowed|downed|necked|popped|had|emptied|finished)\b"
    r"[^.?!]{0,25}\b" + PACK_DRUG + r"[^.?!]{0,12}\b" + PACK_COUNT + r"\s+" + PACK_WORD +
    r"\b",
    r"\b(?:took|taken|swallowed|downed|necked|popped|had|emptied|eaten|ate)\s+(?:the\s+rest\s+of|"
    r"the\s+last\s+of|the\s+remainder\s+of|whats\s+left\s+of|what'?s\s+left\s+of|"
    r"what\s+was\s+left\s+of|what\s+is\s+left\s+of|"
    r"whatever\s+was\s+left\s+of|all\s+that\s+was\s+left\s+of)\s+(?:the\s+|my\s+|a\s+|his\s+|"
    r"her\s+|their\s+)?(?:" + PACK_WORD + r"\s+of\s+)?" + PACK_DRUG,
    r"\b(?:took|taken|swallowed|downed|necked|popped|had|emptied|finished)\s+(?:the\s+|a\s+)?"
    r"(?:whole|full|entire)\s+(?:strip|blister\s+pack|blister|sheet\s+of\s+tablets)\b"
    r"(?!\s+of\s+(?:paper|wallpaper|cloth|fabric|tape|vinyl|wood|card|cardboard|metal|lead|land))",
)

POISON = (
    *CHILD_MEDICINE,
    r"\b(?:swallowed|drank|eaten|ate|took|downed|inhaled|gulped|licked)\s+" + SOME_OF_IT +
    r"(?:bleach|detergent|disinfectant|antifreeze|weed\s?killer|hand\s+saniti[sz]er|"
    r"drain\s+cleaner|soap|shampoo|mouthwash|shower\s+gel)\b",
    *POISON_SAID,
    r"\b(?:swallowed|drank|eaten|ate|took|downed|gulped)\s+"
    r"(?:some\s+|a\s+few\s+|any\s+|a\s+)?mushrooms?\b",
    r"\b(?:swallowed|drank|eaten|ate|took|downed|inhaled|gulped|licked)\s+" +
    SOME_OF_IT + r"(?:" + FUEL_AND_SOLVENT + r")\b",
    r"\b(?:swallowed|swallowing|drank|drunk|eaten|ate|took|taken|downed|inhaled|popped|necked)\b"
    r"[^.?!]{0,30}(?:too\s+(?:many|much)|a\s+lot\s+of|loads\s+of|lots\s+of|a\s+(?:whole|bunch|load|handful|"
    r"pile)\s+of|a\s+whole\s+(?:packet|pack|box|bottle|strip|blister|tub)\s+of|"
    r"the\s+whole\s+(?:packet|pack|box|bottle|strip|blister)\s+of|" + WHOLE_OF + r"|"
    r"a\s+(?:packet|pack|box|bottle|strip|blister)\s+of|[6-9]\s+(?:of\s+)?|[1-9]\d{1,}\s+(?:of\s+)?|"
    r"(?:six|seven|eight|nine|ten|eleven|twelve|fifteen|twenty|thirty|forty|fifty|a\s+hundred)\s+)"
    r"[^.?!]{0,20}\b(?:pills|tablets|paracetamol|ibuprofen|painkillers|analgesics|meds|medicines?|"
    r"sleeping\s+pills|antidepressants|tranquill?i[sz]ers?|insulin)\b",
    r"\b(?:had|have\s+had|'?ve\s+had|got\s+down|knocked\s+back|managed)\s+"
    r"(?:[6-9]|[1-9]\d{1,}|(?:six|seven|eight|nine|ten|eleven|twelve|fifteen|twenty|thirty|"
    r"forty|fifty|a\s+hundred))\s+(?:of\s+)?(?:pills|tablets|paracetamol|ibuprofen|painkillers|"
    r"analgesics|meds|medicines?|sleeping\s+pills|antidepressants|tranquill?i[sz]ers?|insulin)\b"
    r"(?!\s+(?:left|in\s+the|in\s+my|at\s+home|with\s+me|to\s+take|in\s+stock|spare|over))",
    r"\b" + WHOLE_OF + r"\s*\b(?:pills|tablets|paracetamol|ibuprofen|painkillers|analgesics|meds|"
    r"medicines?|sleeping\s+pills|antidepressants|tranquill?i[sz]ers?|insulin)\b",
    *TOOK_MANY_PACKS,
    r"\b(?:chemical|fumes?)\s+(?:leak|leaking|leaked)\b",
    r"\bpoison(?:ed|ing)?\b.{0,20}\b(?:child|kid|son|daughter|baby|toddler|myself|me|dog|cat|puppy)\b",
    r"\b(?:swallowed|drank|eaten|ate|took|downed|inhaled|gulped|choked\s+on)\s+"
    r"(?:(?:some|a|an|the|his|her|their|my|one|two|three)\s+)?" + SOME_OF_IT +
    r"(?:dishwasher\s+(?:tablet|cube|pod|powder)s?|washing\s+(?:capsule|tablet|pod|liquid|"
    r"powder)s?|laundry\s+(?:capsule|tablet|pod)s?|soap\s+powder|fabric\s+softener|"
    r"bleach\s+tablet|drain\s+unblocker|oven\s+cleaner|limescale\s+remover|"
    r"antifreeze|screen\s?wash|de-?icer|weed\s?killer|slug\s+pellets?)\b"
    r"(?!\s+(?:out\s+of|from|off|down\s+from|out\s+the)\b)",
    r"\b(?:child|kid|son|daughter|baby|toddler|boy|girl|little\s+one|he|she|grandson|"
    r"granddaughter)\b[^.?!]{0,20}\b(?:swallowed|drank|ate|eaten|eating|chewed|sucked|"
    r"licked|bitten|bit)\s+(?:(?:my|his|her|their|the|some|a|an|half\s+a)\s+)?"
    r"(?:cigarettes?|cigarette\s+(?:butt|end|stub)s?|fag\s?ends?|fags?|nicotine\s+"
    r"(?:pouch|pouches|gum|lozenge|lozenges|spray|inhaler|shot|shots)s?|snus|chewing\s+tobacco|"
    r"vape\s+(?:liquid|juice)|e-?liquid|nic\s?shot|nicotine)\b",
    r"\b(?:child|kid|son|daughter|baby|toddler|he|she)\b.{0,20}\b(?:swallowed|drank|ate)\s+(?:(?:my|his|her|their|the|some|a)\s+)?(?:bleach|detergent|pills|tablets|medicine|meds|antifreeze|disinfectant|paracetamol|ibuprofen|painkillers|antidepressants|insulin)\b",
    r"\b(?:overdose|overdosed)\b",
    r"\b(?:swallowed|swallowing|ate|eaten|eating|chewed|chewing)\s+(?:a|an|some)\s+(?:coin|coins|"
    r"battery|batteries|magnet|magnets|marble|marbles|button|toy|piece\s+of\s+(?:glass|plastic|metal)|"
    r"drawing\s+pin|pen\s+lid|(?:blu|blue)\s?tack?|play\s?dough)\b",
    r"(?![^?]{0,40}\b(?:dog|dogs|cat|cats|puppy|puppies|kitten|kittens|pup|pups|pet|pets|"
    r"parrot|budgie|hamster|rabbit|bunny|horse|pony|guinea\s+pig|tortoise|ferret|gerbil)\b)"
    r"\b(?:swallowed|swallowing|drank|drunk|eaten|ate|eating|licked|sucked|chewed)\b[^.?!]{0,25}"
    r"\b(?:toilet\s+cleaner|oven\s+cleaner|washing\s+powder|nail\s+varnish|"
    r"nail\s+varnish\s+remover|rat\s+poison|rodent\s+poison|slug\s+pellets?|de-?icer|"
    r"screen\s?wash|fabric\s+softener|dishwasher\s+salt|drain\s+cleaner)\b",
    r"\b(?:swallowed|swallowing|drank|drunk|eaten|ate|eating)\b[^.?!]{0,25}"
    r"\b(?:whole|full|half\s+a|tube\s+of|tubes?\s+of|packet\s+of|pack\s+of)\b[^.?!]{0,15}"
    r"\btoothpaste\b",
    r"\b(?:swallowed|drank|drunk|eaten|ate|chewed|sucked|licked)\b[^.?!]{0,25}"
    r"\b(?:washing\s?up|dishwasher|laundry|soap|shower\s+gel|fabric\s+softener)\s+(?:tablet|tablets|capsule|capsules|pod|pods|liquid|gel|powder|sachet|sachets)\b",
    r"\b(?:child|kid|kids|son|daughter|baby|toddler|newborn|grandson|granddaughter|niece|nephew|"
    r"boy|girl|he|she|they|dog|cat|puppy|kitten|pup)\b[^.?!]{0,25}"
    r"\b(?:ate|eaten|eat|chewed|sucked|swallowed)\b[^.?!]{0,15}"
    r"\b(?:tablet|tablets|capsule|capsules|pod|pods)\b",
    r"\b(?:took|taken|swallowed|had|downed|ate|eaten|popped|necked)\b[^.?!]{0,25}"
    r"\b(?:too\s+(?:many|much)|a\s+lot\s+of|loads\s+of|lots\s+of|a\s+(?:whole|bunch|load|handful|pile|packet|"
    r"box|strip|blister)\s+of|the\s+whole\s+(?:packet|pack|bottle|box|strip|blister)|"
    + WHOLE_OF + r"|"
    r"all\s+(?:of\s+)?(?:my|his|her|their|mums?|mum's|dads?|dad's|the|these|those))\b[^.?!]{0,20}"
    r"\b(?:pills|tablets|paracetamol|ibuprofen|painkillers|meds|medicines?|sleeping\s+pills|"
    r"antidepressants)\b",
    r"\b(?:i\s+(?:think|reckon|believe|suspect)|(?:i'?m|i\s+am)\s+not\s+sure|"
    r"not\s+sure\s+(?:if|whether)|might\s+have|may\s+have|did\s+(?:he|she|they)|"
    r"has\s+(?:he|she|they)|have\s+(?:they|we))\b[^.?!]{0,45}"
    r"\b(?:took|taken|taking|had|has\s+had|got\s+into|helped\s+(?:him|her|them)sel(?:f|ves)\s+to)\b"
    r"[^.?!]{0,25}(?<!his )(?<!her )(?<!their )"
    r"\b(?:(?:some|a\s+few|a\s+couple\s+of|any|another|more)\s+(?:of\s+(?:my|the)\s+)?|"
    r"(?:my|mums?|mum'?s|dads?|dad'?s|nans?|nan'?s)\s+)?" + MEDICINE + r"\b",
    r"\b(?:crayons?|chalk(?!\s*paint)|toothpaste|soap|play\s?dough|(?:blu|blue)\s?tack?)\b[^.?!]{0,60}"
    r"\b(?:drowsy|sleepy|limp|floppy|cough\w*|chok\w*|struggling\s+to\s+breathe|"
    r"can'?t\s+breathe|vomit\w*|being\s+sick|throwing\s+up|fitting|seizure|blue|"
    r"unresponsive|passing\s+out|hard\s+to\s+wake)\b",
    r"\b(?:drowsy|sleepy|limp|floppy|cough\w*|chok\w*|struggling\s+to\s+breathe|"
    r"can'?t\s+breathe|vomit\w*|fitting|seizure)\b[^.?!]{0,60}"
    r"\b(?:crayons?|chalk(?!\s*paint)|toothpaste|soap|play\s?dough|(?:blu|blue)\s?tack?)\b",
    r"\b(?:swallowed|swallowing|drank|drunk|eaten|ate|eating|licked|chewed)\b[^.?!]{0,25}"
    r"\b(?:chalk|emulsion|gloss|matt|satin)\s+paint\b",
    r"(?![^?]{0,40}\b(?:dog|dogs|cat|cats|puppy|puppies|kitten|kittens|pup|pups|pet|pets|"
    r"parrot|budgie|hamster|rabbit|bunny|horse|pony|guinea\s+pig|tortoise|ferret|gerbil)\b)"
    r"\b(?:swallowed|swallowing|drank|drunk|drinking|gulped|gulping|sucked|sucking|licked|"
    r"licking|sipped|sipping|swigged|swigging|necked|glugged|glugging)\b[^.?!]{0,25}"
    r"\b(?:fairy\s+liquid|washing[\s-]?up\s+liquid|dish\s+soap|bubble\s+bath|"
    r"laundry\s+liquid|fabric\s+conditioner|dishwasher\s+(?:liquid|gel|powder|salt)|"
    r"bleach|detergent|disinfectant|drain\s+cleaner|weed\s?killer|hand\s+saniti[sz]er|"
    + FUEL_AND_SOLVENT + r")\b"
    r"(?!\s+(?:out\s+of|from|off|down\s+from|out\s+the)\b)",
)


CO_MENTION = (
    r"\bcarbon\s+monoxide\b",
    r"\bco\s+(?:alarm|detector|monitor)\b",
)


SWALLOW_TAKING = (
    r"(?:swallow\w*|gulp\w*|got\s+stuck\s+in\s+(?:his|her|their|my)\s+throat)"
)
SWALLOW_BITTEN = (
    r"\b(?:bit|bites?|biting|chewed|chewing|sucked|sucking|pierced|pierces)\b[^.?!]{0,20}"
    r"\b(?:button\s+battery|battery|batteries|magnet|magnets)\b"
)
SWALLOWED_THING = (
    r"\b" + SWALLOW_TAKING + r"\s+"
    r"(?:(?:some|a|an|the|his|her|their|my|one|two|three)\s+)?"
    r"(?:(?:bit|piece)\s+of\s+)?"
    r"(?:sim\s?card|memory\s+card|sd\s+card|credit\s+card|button\s+battery|watch\s+battery|"
    r"fish\s+bone|chicken\s+bone|"
    r"battery|coin|magnet|marble|bead|pin|screw|nail|blade|razor\s+blade|glass|toy\s+part|"
    r"lego|bee|wasp|insect|stone|plastic\s+bag|balloon)\b",
    r"\b(?:child|kid|son|daughter|baby|toddler|he|she)\b.{0,20}\b(?:ate|eaten|eats|eating)\s+"
    r"(?:a\s+|the\s+|his\s+|her\s+)?(?:sim\s?card|memory\s+card|sd\s+card|button\s+battery|"
    r"watch\s+battery|coin|magnet|marble|bead|pin|screw|nail|blade|glass|toy\s+part|lego|"
    r"bee|wasp|insect|stone|balloon)\b",
    SWALLOW_BITTEN,
)


CO_PLACE = (
    r"\bwhere\s+(?:should|do|can)\s+(?:i|we|you)\s+(?:put|place|fit|mount|install|site)\b.{0,30}"
    r"\b(?:carbon\s+monoxide|co)\s+(?:alarm|detector|monitor)\b",
    r"\b(?:carbon\s+monoxide|co)\s+(?:alarm|detector|monitor)\b.{0,30}\bwhere\b.{0,20}\b(?:put|go|place|fit)\b",
)
CO_FACT = (
    r"\bcarbon\s+monoxide\b.{0,40}\b(?:heavier|lighter|than\s+air|rise|rises|sink|sinks)\b",
    r"\b(?:heavier|lighter)\s+than\s+air\b.{0,40}\bcarbon\s+monoxide\b",
    r"\bwhat\s+(?:is|does)\s+carbon\s+monoxide\b",
)

BREATH = r"breath(?:e|es|ing)?"


BREATHING = (
    r"\b(?:can't|cannot|can\s+not|struggling\s+to|hard\s+to|unable\s+to)\s+" + BREATH + r"\b"
    r"(?!\s+through\b)",
    r"\b(?:can't|cannot|can\s+not)\s+(?:catch|get|find)\s+(?:my|his|her|their|a)\s+"
    r"breath\b",
    r"\b(?:not|stopped|stop|isn't|is\s+not|hasn't|has\s+not)\s+" + BREATH + r"\b",
    r"\b(?:trouble|difficulty|difficult(?:y)?|problems?)\s+(?:to\s+)?breath(?:e|ing)\b",
    r"\b(?:i|we|he|she|they|my\s+\w+|i'?m|im|i'?ve|ive|he'?s|hes|she'?s|shes|they'?re|theyre|"
    r"they'?ve|theyve|we'?re|we'?ve)\s+(?:have|has|had|having|got|get|getting|been\s+having|"
    r"have\s+been|has\s+been|been|am|is|are|keeps?|kept|feels?|looks?)\s+"
    r"(?:some\s+|a\s+bit\s+of\s+)?short(?:ness)?\s+of\s+breath\b",
    r"\b(?:im|i'?m|hes|he'?s|shes|she'?s|they'?re|theyre|we'?re)\s+"
    r"(?:a\s+bit\s+(?:of\s+)?|a\s+little\s+)?short(?:ness)?\s+of\s+breath\b",
    r"\b(?:still|now)\s+(?:a\s+bit\s+|a\s+little\s+)?(?:out\s+of|short(?:ness)?\s+of)\s+breath\b",
    r"\b(?:short(?:ness)?\s+of\s+breath|breathless)\s+(?:right\s+)?now\b",
    r"\bshort(?:ness)?\s+of\s+breath\s+(?:when|whenever|while|at|on|lying|walking|that|since|and|"
    r"if|after|before|going|doing)\b",
    r"\bshort(?:ness)?\s+of\s+breath\s+for\s+(?:\d+|a|an|two|three|a\s+few|a\s+couple\s+of|"
    r"several|many|the\s+last)\s+(?:hour|hours|day|days|week|weeks|month|months|year|years)\b",
    r"\basthma\s+attack\b",
    r"\binhaler\b[^.!?]{0,25}\b(?:not\s+working|isn'?t\s+working|won'?t\s+work|"
    r"didn'?t\s+work|isn'?t\s+helping|not\s+helping)\b",
    r"\binhaler\b[^.!?]{0,25}\b(?:empty|running\s+out)\b(?=[^.!?]{0,40}\b(?:breath|breathing|"
    r"breathe|wheez\w*|attack|tight|shaky|shake)\b)",
    r"\bout\s+of\s+breath\s+(?:at\s+rest|in\s+bed|sitting\s+still|sitting\s+down|"
    r"doing\s+nothing|watching\s+tv|lying\s+down)\b",
    r"\bgasping\s+for\s+(?:breath|air)\b",
    r"\bgasping\s+for\s+(?:his|her|their|my)\s+breath\b",
    r"\b(?:he|she|they|my\s+" + PERSON + r"|the\s+" + PERSON + r")\b[^.?!]{0,15}\bgasping\b",
    r"\b(?:i'?m|im|i\s+am)\s+gasping\b",
    r"\bgasping\b[^.!?]{0,25}\b(?:blue|lips?|pale|sweat\w*|collapsed|unconscious|"
    r"not\s+breathing|stopped|wheez\w*|struggling)\b",
    r"\bturning\s+blue\b",
    r"\bchok(?:ing|ed|es)\b(?!\s+(?:under\s+pressure|about\b))", r"\bchocking\b", r"\b(?:throat|tongue|airway)\s+(?:is\s+|'s\s+)?(?:closing|closing\s+up|swelling|swollen)\b",
    r"\banaphyla\w*\b", r"\b(?:severe|serious|bad|really\s+bad)\s+allergic\s+reaction\b", r"\bepipen\b",
    r"\b(?:he|she|they|my\s+(?:son|daughter|husband|wife|dad|mum|friend|partner|baby))\s+"
    r"(?:isn't|is\s+not|stopped|hasn't|has\s+not)\s+" + BREATH + r"\b",
    r"\b(?:for|since|going\s+on\s+for|these\s+last)\s+(?:about\s+|nearly\s+|almost\s+)?"
    r"(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|a|a\s+few|a\s+couple\s+of|"
    r"several|many|last)\s+(?:day|days|week|weeks|month|months|year|years|christmas|friday)\b"
    r"[^.!?]{0,40}?\b(?:breathless|short(?:ness)?\s+of\s+breath|out\s+of\s+breath)\b",
    r"\bout\s+of\s+breath\b[^.!?]{0,30}\bfor\s+(?:days|weeks|months|years|a\s+week|"
    r"a\s+month|a\s+few\s+days|a\s+few\s+weeks|a\s+couple\s+of\s+weeks|the\s+last\s+\w+)\b",
    r"\b(?:short(?:ness)?\s+of\s+breath|out\s+of\s+breath|breathless)\b[^.!?]{0,20}\bfor\s+"
    r"(?:an?\s+hour|hours|an?\s+hour\s+or\s+two|half\s+an\s+hour)\b",
)

BREATH_PAST_CUE = (
    r"\bcough\w*", r"\bchok\w*", r"\bswallow\w*", r"\bblue\b", r"\bwheez\w*", r"\bgasp\w*",
    r"\bthroat\b", r"\basthma\b", r"\bswell\w*", r"\bcroup\b", r"\bpneumonia\b",
    r"\bfits?\b", r"\bstopped\b", r"\bhospital\b", r"\bambulance\b", r"\binhaler\b",
)
BREATH_PAST = (
    r"\b(?:couldn'?t|could\s+not|wasn'?t\s+able\s+to|was\s+unable\s+to|struggled\s+to)\s+"
    r"(?:" + BREATH + r"|(?:catch|get|find)\s+(?:my|his|her|their|a|any)\s+breath)\b"
    r"(?!\s+through\b)",
)

CHEST_LIMB = r"(?:left\s+arm|jaw)s?"
CHEST_LIMB_SIGN = r"(?:numb(?:ness|ed|ing|s)?|tingl\w*|pains?|painful|ache\w*|hurts?|sore)"
CHEST_COMPANY = (
    r"(?:chest|heart|sweat\w*|clammy|breathless|short\s+of\s+breath|faint\w*|grey|gray|"
    r"nause\w*|vomit\w*|crush\w*|spread\w*|radiat\w*|down\s+(?:my\s+|the\s+)?left\s+arm)"
)
CHEST_LIMB_PAIR = r"(?:left\s+arm|arm|jaw|shoulder)s?"
CHEST_MENTIONED = (
    r"\bchest\b", r"\bheart\b", r"\bcrush\w*", r"\bspread\w*", r"\bradiat\w*",
    r"\bdown\s+(?:my\s+|the\s+)?left\s+arm\b",
)
_FACE_WORD = (r"\b(?:face|faces|mouth|smile|cheek|eyelid|lip|tongue|"
              r"side\s+of\s+(?:my|his|her|their)\s+face)\b")
_FAST_SIGN = (r"\b(?:numb\w*|weak\w*|dead|heavy|droop\w*|dropped|floppy|useless|slack|twisted|"
              r"not\s+working|won'?t\s+(?:lift|move|raise|work|close)|"
              r"can'?t\s+(?:lift|raise|move|feel|hold|close))\b")
_LIMB_WORD = r"\b(?:arms?|hands?|side|one\s+side|fingers?|fingertips?)\b"
_FACE_ODD = (r"\b(?:droop\w*|dropped|twisted|slack|funny|odd|weird|strange|not\s+right|"
             r"numb\w*|tingl\w*|pins\s+and\s+needles)\b")
_FACE_GOING_ODD = (r"\b(?:droop\w*|dropped|twisted|slack|funny|odd|weird|strange|not\s+right)\b")
STROKE_FAST = (
    r"(?=[^.?!]*" + _LIMB_WORD + r"[^.;!?]{0,18}" + _FAST_SIGN + r")"
    r"(?=[^.?!]*" + _FACE_WORD + r"[^.;!?]{0,18}" + _FAST_SIGN + r")",
    r"(?=[^.?!]*" + _LIMB_WORD + r"[^.;!?]{0,18}" + _FAST_SIGN + r")"
    r"(?=[^.?!]*" + _FACE_WORD + r"[^.;!?]{0,18}" + _FACE_ODD + r")",
    _FACE_WORD + r"\s*(?:,|and)\s+(?:my\s+|his\s+|her\s+|their\s+|the\s+)?"
    r"(?:arms?|hands?|side)\s+(?:are|is|both|have|has|went|gone|feel)?\s*"
    r"(?:both\s+)?" + _FAST_SIGN,
    r"\b(?:my|his|her|their|the)\s+(?:left|right)\s+arms?\b[^.!?]{0,25}"
    r"\b(?:weak\w*|numb\w*|dead|heavy|useless|floppy|not\s+working|won'?t\s+(?:lift|move|"
    r"raise|work))\b",
    r"\b(?:can'?t|cannot|couldn'?t)\s+(?:lift|raise|move|hold\s+up|feel)\s+(?:my|his|her|their)\s+"
    r"(?:left|right)\s+(?:arm|hand|leg)\b",
)
STROKE_FAST_OFF = (
    r"\b(?:for|in)\s+(?:the\s+)?(?:last\s+)?(?:months|years|weeks|ages)\b",
    r"\bsince\s+(?:my|his|her|their|the)?\s*(?:accident|injury|operation|op|fall|surgery|stroke|"
    r"birth|diagnosis)\b",
    r"\b(?:trapped\s+nerve|pins\s+and\s+needles|carpal|tennis\s+elbow|frozen\s+shoulder|"
    r"rsi|repetitive\s+strain)\b",
    r"\b(?:slept\s+(?:on|funny)|went\s+to\s+sleep\s+on|gym|work\s?out|weights?|"
    r"after\s+(?:the\s+)?(?:gym|run|exercise|swim))\b",
    r"\balways\b",
    r"\bsince\s+(?:i|he|she|they|we)\s+(?:was|were)\b",
    r"\b(?:all\s+my\s+life|since\s+(?:a\s+)?(?:kid|child|childhood|birth|teenager|teen))\b",
    r"\b(?:over|above|behind|past)\s+(?:my|his|her|their)\s+(?:head|back)\b",
)

STROKE_FAST_CAUSE = (
    r"\b(?:in|out\s+in|from|with|out\s+of)\s+the\s+(?:cold|freezing|cold\s+weather|snow)\b",
    r"\b(?:cold\s+(?:hands?|fingers?|feet|toes|weather)|frostnip|frostbite)\b",
    r"\b(?:typing|typed|type|keyboard|keyboards|mouse|desk|laptop|computer|sewing|knitting|"
    r"cello|guitar|piano|drumming|gardening|painting|chopping)\b",
    r"\b(?:vaccin\w+|jabs?|injections?|booster|booster\s+jab|covid|flu\s+jab|anaesthetic|"
    r"anesthetic|novocaine)\b",
    r"\b(?:dentist|dental|filling|fillings|tooth|teeth|gums|root\s+canal|wisdom\s+tooth)\b",
)
STROKE_FAST_SHOULDER = (
    r"\bshoulders?\b[^.!?]{0,24}\b(?:hurts?|hurt|sore|aches?|aching|pain\w*|stiff\w*|"
    r"clicking|frozen)\b",
    r"\b(?:hurts?|hurt|sore|aches?|aching|pain\w*|stiff\w*|frozen)\b[^.!?]{0,18}\bshoulders?\b",
)
STROKE_FAST_HARD = (
    r"\b(?:droop\w*|dropped|twisted|slack|floppy|dead|useless|heavy|hangs?\s+down|"
    r"won'?t\s+(?:lift|move|raise|work|close)|can'?t\s+(?:lift|raise|move|hold))\b",
)
STROKE_FAST_SENSORY = (
    r"\b(?:cheeks?|lips?|tongue|mouth|teeth|gums?)\b[^.?!]{0,40}"
    r"\b(?:hands?|fingers?|fingertips?|thumb)\b",
    r"\b(?:hands?|fingers?|fingertips?|thumb)\b[^.?!]{0,40}\b(?:cheeks?|lips?|tongue|mouth)\b",
)
STROKE_FAST_JAB = (
    r"\b(?:flu|covid|tetanus|booster|vaccine|vaccination|jab|jabs|injection|injections|shot|shots)\b"
    r"[^.!?]{0,30}\b(?:arm|arms|shoulder|shoulders|deltoid)\b",
    r"\b(?:arm|arms|shoulder|shoulders|deltoid)\b[^.!?]{0,30}\b(?:flu|covid|tetanus|booster|"
    r"vaccine|vaccination|jab|jabs|injection|injections|shot|shots)\b",
)
STROKE_FAST_LIFT_CEILING = (
    r"\b(?:above|over)\s+(?:my|his|her|their|your)\s+head\b",
    r"\b(?:to|at)\s+shoulder\s+height\b",
)
STROKE_FAST_PATTERN = (
    r"\b(?:usually|sometimes|comes\s+and\s+goes|on\s+and\s+off)\b",
)
STROKE_PAIR_BOTH = STROKE_FAST[:3]
STROKE_FAST_WEAK = (
    r"\b(?:weak\w*|heavy|dead|useless|floppy|not\s+working|won'?t\s+(?:lift|move|raise|work)|"
    r"can'?t\s+(?:lift|raise|move|hold))\b",
)
CHEST_STRAIN = (
    r"\b(?:when|whenever|every\s+time|each\s+time|after|from|since|while)\b[^.!?]{0,25}"
    r"\bcough\w*\b",
    r"\bcough\w*\b[^.!?]{0,20}\b(?:makes?|made|leaves?|left)\b[^.!?]{0,15}\bchest\b",
    r"\bcough\w*\b[^.!?]{0,15}\b(?:and|but|then|so)\b[^.!?]{0,20}\bchest\b"
    r"[^.!?]{0,15}\b(?:hurt|sore|ache)\w*\b",
    r"\bcoughing\s+fit\b",
)
CHEST_STRAIN_MOVE = (
    r"\b(?:when|whenever|every\s+time|each\s+time|after|from|since|while)\b[^.!?]{0,25}"
    r"\b(?:sneeze\w*|sneezed|laugh\w*)\b",
    r"\b(?:sneez\w*|laugh\w*)\b[^.!?]{0,20}"
    r"\b(?:makes?|made|leaves?|left)\b[^.!?]{0,15}\bchest\b[^.!?]{0,15}\b(?:hurt|sore|ache)\w*\b",
    r"\b(?:sneez\w*|laugh\w*|cough\w*)\b[^.!?]{0,25}\bchest\b[^.!?]{0,15}\b(?:hurt|sore|ache)\w*\b",
)
CHEST_SORE_MOVE = (
    r"\b(?:my|his|her|their|the|a)\s+chest\b[^.?!]{0,30}"
    r"\b(?:ache\w*|sore|hurts?|hurting|pain\w*)\b[^.?!]{0,45}"
    r"\b(?:sneeze\w*|sneezed|laugh\w*|cough\w*)\b",
    r"\b(?:sneeze\w*|sneezed|laugh\w*|cough\w*)\b[^.?!]{0,45}"
    r"\b(?:my|his|her|their|the)\s+chest\b[^.?!]{0,30}\b(?:ache\w*|sore|hurts?|hurting|pain\w*)\b",
)
CHEST_SPREAD = (
    r"\b(?:spread\w*|radiat\w*|moves?\b|moving\b|travel\w*|shoot\w*)\b",
    r"\b(?:goes|going|went|comes|coming|came)\s+(?:into|to|down|up|across)\b",
    r"\b(?:back|shoulders?|shoulder\s+blades?|between\s+the\s+shoulders|neck)\b",
)
CHEST_STRAIN_STOP = (
    r"\bwhen\s+(?:i|ya)\s+breathe?\b", r"\bhurts?\s+to\s+breathe\b",
    r"\bbreath(?:ing|e)\s+(?:in|deeply)\b", r"\btakes?\s+a\s+deep\s+breath\b",
    r"\bdeeper\s+breath\b",
    r"\bfever\w*\b", r"\bburning\s+up\b", r"\btemperature\b", r"\bchills?\b",
    r"\bshiver\w*\b", r"\bhot\s+and\s+cold\b",
    r"\b(?:heart|racing|pounding|palpitations?|fluttering|irregular|pulse)\b",
    r"\b(?:at\s+rest|sitting\s+still|sit\s+still|lying\s+still|not\s+moving|"
    r"when\s+i\s+am\s+still|when\s+i'm\s+still)\b",
    r"\b(?:smokers?|ex-?smoker|smoked|angina|heart\s+attack|stent|bypass|diabetes|diabetic|"
    r"high\s+blood\s+pressure|hypertension|cholesterol|blood\s+thinners?)\b",
    r"\b(?:5\d|6\d|7\d|8\d|9\d)\s*(?:years?\s+old|yrs?\s+old|yo)\b",
    r"\b(?:i\s+am|i'?m|im)\s+(?:5\d|6\d|7\d|8\d|9\d)\b",
    r"\b(?:out\s+of\s+breath|short\s+of\s+breath|breathless|puffed\s+out|"
    r"can'?t\s+(?:get\s+my\s+)?breath)\b",
    r"\b(?:catch|get|find)\w*\s+(?:my\s+|your\s+)?breath\b",
    r"\b(?:barely|hardly|scarcely)\s+(?:able\s+to\s+)?breath\w*",
    r"\bfigh(?:t|ting)\s+for\s+(?:my\s+|his\s+|her\s+)?breath\b",
    r"\bbreath\w*\s+properly\b",
    r"\b(?:hard|trouble|difficult\w*|struggl\w*)\s+(?:to\s+|with\s+)?breath\w*",
    r"\bbreath\w*\s+(?:hard|difficult)\b",
    r"\bgasp\w*\s+for\s+(?:air|breath|it)\b",
    r"\b(?:blue|grey|gray)\b",
    r"\b(?:pass(?:ed|es|ing)?\s+out|black(?:ed|ing)?\s+out|faint\w*|keel\w*\s+over)\b",
    r"\b(?:pregnan\w*|on\s+the\s+pill|contraceptives?|chemo\w*|cancer|clots?|dvt)\b",
    r"\bwheez\w*", r"\basthma\w*", r"\binhalers?\b", r"\brattl\w*",
    r"\b(?:chest\s+infection|bronchitis|pneumonia|phlegm)\b",
    r"\bcoughing\s+up\s+(?:green|yellow|brown)\b",
    r"\b(?:lost|losing)\s+weight\b", r"\bfor\s+(?:a|one|\d+)\s+months?\b",
)
CHEST_COUGH_STRAIN_REPLY = (
    "A chest that aches when you cough is usually the muscle between the ribs, strained by the "
    "coughing itself, and it eases off as the cough settles. Honey in warm water, warm drinks and "
    "rest help the cough; see a GP if you are hot and shivery, coughing up green or blood, or no "
    "better after three weeks, and ring 999 if the pain spreads to your back, arm or jaw or you "
    "are breathless with it.",
    "The coughing is what strains the muscle between the ribs, and that ache fades over a week or "
    "two as the cough goes. Warm drinks, honey and an early night; a GP if you are feverish or no "
    "better in three weeks, and 999 if it spreads to your back, arm or jaw or you are short of "
    "breath with it.",
)
CHEST_STRAIN_REPLY = (
    "A chest that hurts only when you sneeze or laugh is usually a muscle between the ribs, and it "
    "settles by itself in a week or two. See a GP if it hurts when you sit still or is no better "
    "after three weeks, and ring 999 if it spreads to your back, arm or jaw.",
    "The muscle between the ribs is what a sneeze or a hard laugh pulls, and it eases off in a "
    "week or two. A GP if the pain turns up when you are resting or is still there after three "
    "weeks, and 999 if it spreads to your back, arm or jaw.",
)
LEFT_ARM_NUMB = (
    r"\bleft\s+arms?\b[^.!?]{0,25}\b(?:numb(?:ness|ed|ing|s)?|gone\s+dead|dead)\b",
    r"\b(?:numb(?:ness|ed|ing|s)?|gone\s+dead)\b[^.!?]{0,20}\bleft\s+arms?\b",
)
CHEST_FEELING = (
    r"\b(?:when|whenever|with|from|because\s+of|after|during|amid|in)\b[^.?!]{0,30}"
    r"\b(?:anxi\w*|panic\w*|stress(?:ed|ful)?|nervous\w*|worry\w*|worried|overwhelm\w*|"
    r"sad\w*|upset|grief|grieving|exam|exams|test|presentation|interview|deadline)\b",
    r"\b(?:anxi\w*|panic\s+attack|anxiety\s+attack|stress|my\s+nerves)\b[^.?!]{0,30}\bchest\b",
    r"\b(?:know|knows|knew|think|thinks|thought|sure|probably|likely|reckon|guess)\b"
    r"[^.?!]{0,20}\b(?:anxi\w*|panic\w*)\b",
)
CHEST_FEELING_RED = (
    r"\b(?:spread\w*|radiat\w*|travel\w*|(?:in)?to\s+(?:my\s+|the\s+)?(?:back|shoulders?|neck|arms?|"
    r"jaw)\b)",
    r"\b(?:sudden\w*|out\s+of\s+(?:nowhere|the\s+blue)|never\s+had|first\s+time|"
    r"new\s+(?:pain|tightness|ache)|worse\s+than|wont\s+go\s+away|won'?t\s+go\s+away|"
    r"all\s+day|all\s+night|for\s+(?:hours|an\s+hour|days)|at\s+rest|"
    r"wok(?:e|en)\s+me|wakes\s+me|started\s+(?:today|yesterday|last\s+night)|"
    r"this\s+morning|this\s+week)\b",
)
CHEST_ADJ = (
    r"\b(?:a\s+|my\s+|his\s+|her\s+|their\s+)?(?:tight\w*|heavy|pressured?)\s+"
    r"(?:feeling\s+)?(?:in\s+)?(?:(?:my|his|her|their|the)\s+)?chest\b(?!\s+of\b)"
    r"(?!\s+(?:drawers?|freezer|freezers))",
)
CHEST_ANSWERED_ELSEWHERE = (
    r"\b" + PEOPLE + r"\b(?:\s+\w+){0,4}\s+collapsed\b"
    r"|\b(?:can'?t|cannot|couldn'?t|struggling\s+to|unable\s+to)\s+breathe\b"
    r"|\b(?:not|stopped|stop|isn'?t|is\s+not)\s+breathing\b"
    r"|\bcpr\b|\bgasping\b"
    r"|\b(?:he|she|they)\s+(?:is|'s)\s+out\s+cold\b"
    r"|\b(?:he|she|they|my\s+" + PERSON + r")\s+(?:is|'s|are)\s+not\s+responding\b"
)

CHEST = (
    r"\bcrushing\s+(?:chest|pains?)\b",
    r"\b(?:chest|heart)\s+(?!of\b)(?!drawers?\b)(?!freezers?\b)"
    r"(?:\w+\s+){0,2}(?:pains?|tightness|tight|hurts?|hurting|aching)\b"
    r"(?!\s+(?:me|you|him|her|us|them)\b)",
    r"\b(?:my\s+)?chest\s+(?:is|'s|feels|felt)\s+(?:like\s*(?:it'?s|it\s+is)\s+)?(?:being\s+)?"
    r"(?:crush\w*|squeez\w*|in\s+a\s+vice|heav\w*)\b",
    r"\bcrush\w*\s+(?:feeling|tightness|weight|pressure|pain)\s+(?:in|across|round)\s+(?:my|the)\s+chest\b",
    r"\b(?:my|his|her|their|the)\s+chest\b(?!\s+of\s+drawers)(?!\s+drawers?\b)"
    r"(?!\s+freezers?\b).{0,25}"
    r"\b(?:hurts?|hurting|aching|ache|pain|painful|tight\w*|pressure)\b",
    r"\bpains?\s+in\s+my\s+chest\b", r"\b(?:pains?|pressure|tightness)\s+(?:in|across)\s+(?:my|the)\s+chest\b",
    r"\bchest\s+(?:pains?|hurts?|tight\w*)\b.{0,45}\b(?:arm|jaw|shoulder|sweat\w*|nausea|back)\b",
    r"\b" + CHEST_LIMB + r"\b[^.!?]{0,30}\b" + CHEST_LIMB_SIGN + r"\b[^.!?]{0,40}\b"
    + CHEST_COMPANY + r"\b",
    r"\b" + CHEST_COMPANY + r"\b[^.!?]{0,40}\b" + CHEST_LIMB + r"\b[^.!?]{0,30}\b"
    + CHEST_LIMB_SIGN + r"\b",
    r"\b" + CHEST_LIMB + r"\b[^.!?]{0,45}\b" + CHEST_LIMB_PAIR + r"\b[^.!?]{0,25}\b"
    + CHEST_LIMB_SIGN + r"\b",
    r"\b(?:going|spreading|radiating)\s+(?:down|into|to|up)\s+(?:my\s+)?(?:left\s+)?(?:arm|jaw|shoulder|neck)\b",
    r"\b(?:having|is\s+having|just\s+had|i'?m\s+having|he'?s\s+having|she'?s\s+having|having\s+another|think|suspect\w*)\b.{0,20}\bheart\s+attack\b",
    r"\bheart\s+attack\s+(?:right\s+)?now\b",
    *CHEST_IN_A_HAND,
)

SLUR_NOT_DENTAL = r"\A(?!.*\b(?:" + DENTAL_WORDS + r")\b)"
TIRED_WORDS = (r"tired|exhausted|knackered|sleepy|shattered|weary|worn\s+out|jet\s?lag|"
               r"no\s+sleep|not\s+slept|havent\s+slept|hasnt\s+slept|up\s+all\s+night|"
               r"long\s+day|early\s+start|night\s+shift|first\s+night\s+shift|"
               r"been\s+up\s+since")
SLUR_CAUSE_WORDS = DENTAL_WORDS + "|" + DRINK_WORDS + "|" + TIRED_WORDS
SLUR_NOT_A_PERFORMANCE = (r"\A(?!.*\b(?:singers?|lead\s+singer|frontman|presenter|comedian|"
                          r"band|choir|gig|gigs|concert|on\s+stage|on\s+tv|on\s+the\s+radio|"
                          r"interview)\b)")
SLUR_NOT_A_STROKE = r"\A(?!.*\b(?:" + SLUR_CAUSE_WORDS + r")\b)"
DENTAL = r"(?:" + DENTAL_WORDS + r")"
DENTAL_NUMB = (
    r"\b(?:slurr\w*|speech|words?)\b[^.!?]{0,60}\b" + DENTAL + r"\b",
    r"\b" + DENTAL + r"\b[^.!?]{0,60}\b(?:slurr\w*|speech|words?)\b",
)
DENTAL_NUMB_ASK = (
    r"\bhow\s+long\b", r"\bhow\s+many\s+hours\b", r"\bwears?\s+off\b",
    r"\bwhen\s+will\s+(?:it|the\s+numb(?:ness|ed|ing|s)?\s+feeling)\s+(?:go|wear|be\s+back|be\s+normal)\b",
    r"\bhow\s+long\s+does\s+it\s+(?:last|take)\b",
)
DENTAL_NUMB_FOLLOW = (
    "A few hours, usually two to four: the feeling comes back from the edge of the lip inwards, "
    "and soft food and nothing hot until it does. If it is still the same tomorrow, ring the "
    "dentist.",
)
SLUR_SUDDEN = (r"\b(?:today|this morning|this afternoon|tonight|last night|yesterday|suddenly|"
               r"all of a sudden|came on|started|just now|an hour ago|this week)\b",
               r"\A(?:yes|yeah|yep|it did|it has|he did|she did)\b")
SLUR_NOT_SUDDEN = (r"\balways\b", r"\bsince\s+(?:he|she|they)\s+was\s+(?:born|a\s+baby|little|small)\b",
                   r"\bmonths\b", r"\bforever\b", r"\bgradually\b", r"\bslowly\b",
                   r"\bnever\s+(?:said|spoken|talked)\b", r"\bno\s+change\b", r"\bstill\s+the\s+same\b")
SLUR_SMALL_CHILD_URGENT = (
    r"\bfever\b", r"\btemperature\b", r"\brash\b", r"\bfits?\b", r"\bseizure\w*\b",
    r"\bfloppy\b", r"\bdrowsy\b", r"\bhard\s+to\s+wake\b", r"\bwont\s+wake\b",
    r"\bnot\s+himself\b", r"\bnot\s+herself\b", r"\bbreathing\b", r"\bblue\b",
)
SLUR_SMALL_CHILD_URGENT_REPLY = (
    "That needs seeing today rather than waiting: ring 111 or your GP now, and 999 or 911 if he "
    "is drowsy, floppy or hard to wake.",
)
SLUR_SMALL_CHILD_CALM = (
    "Then it is a health visitor or a GP who can watch it: ask for the words that are not coming "
    "out to be checked, and his hearing at the same time.",
)
SLUR_DRINK = (
    r"\b(?:" + DRINK_WORDS + r")\b[^.!?]{0,40}\b(?:slurr\w*|slurred|speech|words?)\b",
    r"\b(?:slurr\w*|slurred|speech|words?)\b[^.!?]{0,40}\b(?:" + DRINK_WORDS + r")\b",
)
SLUR_SMALL_CHILD = (
    r"\b(?:" + SMALL_CHILD + r")\b[^.!?]{0,40}\b" + SLUR_THICK + r"\b",
    r"\b" + SLUR_THICK + r"\b[^.!?]{0,40}\b(?:" + SMALL_CHILD + r")\b",
)
DENTAL_NUMB_RED = (
    r"\bdroop\w*", r"\bweak\w*", r"\bone\s+side\b", r"\bconfus\w*",
    r"\bcan'?t\s+move\b", r"\bcan\s+not\s+move\b",
    r"\bnumb\s+(?:down\s+)?(?:my\s+)?(?:arm|leg|side|hand|foot)\b",
    r"\b(?:arm|leg|side|hand|foot)\s+(?:is\s+|feels\s+)?(?:numb|weak|dead)\b",
)
NOT_A_STUTTER = (r"\A(?!.*\bstutter\w*\b)(?!.*\bstammer\w*\b)")
NOT_AN_OCCASION = (r"\A(?!.*(?:" + WORDS_OUT_OCCASION + r"))")
STROKE_HAND_SELF = (
    r"\bi\s+(?:feel|felt|am|get|getting|got|keep\s+getting|have\s+been\s+feeling)\s+"
    r"(?:a\s+bit\s+|really\s+|very\s+|so\s+|kind\s+of\s+)?(?:confus\w*|muddled|scatty|"
    r"forgetful)\b",
)
STROKE_HAND_OTHER = STROKE_HAND_HARD

STROKE = (
    NOT_A_STUTTER + NOT_AN_OCCASION
    + r".*?\b(?:can'?t|cannot|couldn'?t|couldnt|could\s+not|can\s+not)\s+"
    r"(?:get|get\s+out)\s+(?:my|his|her|their|our|your|the|any|a)\s+words?\s+out\b"
    r"(?!\s+(?:to\b|of\s+(?:my|his|her|their|our)\s+(?:head|mind)\b|of\s+the\s+way\b))",
    NOT_A_STUTTER + NOT_AN_OCCASION
    + r".*?\b(?:my|his|her|their|our)(?:\s+\w+){0,2}\s+words?\s+won'?t\s+"
    r"come\s+out\b",
    r"\b(?:his|her|my|their|our|your|dad'?s?|mum'?s?|mom'?s?|husband'?s?|wife'?s?|"
    r"partner'?s?|son'?s?|daughter'?s?)\s+(?:speech|words?)\s+"
    r"(?:(?:are|is|were|was|keeps?)\s+coming\s+out|has|have|had|is|are|was|were|'s|'ve|"
    r"sounds?|came\s+out|comes?\s+out|went|goes)\s+"
    r"(?:gone\s+|all\s+|a\s+bit\s+|a\s+little\s+|really\s+|very\s+|so\s+)?"
    r"(?:funny|odd|weird|strange|wrong|blurred|muddled|mushy|thick|slurred)\b",
    r"\b(?:face|mouth)\s+(?:is\s+|'s\s+)?(?:drooping|dropped|slurred)\b", r"\bdrooping\s+(?:face|mouth|on\s+one\s+side)\b",
    r"\bslurred\s+(?:speech|words)\b",
    SLUR_NOT_DENTAL + r".*?\b(?:slurr\w*|slurred|speech|words?|talking)\b[^.!?]{0,40}\b(?:"
    + SLUR_RED_BESIDE + r")\b",
    SLUR_NOT_DENTAL + r".*?\b(?:" + SLUR_RED_BESIDE + r")\b[^.!?]{0,40}"
    r"\b(?:slurr\w*|slurred|speech|words?|talking)\b",
    NOT_A_STUTTER + r".*?\b(?:words?|speech)\b[^.!?]{0,90}\b(?:" + SLUR_RED_BESIDE + r")\b",
    SLUR_NOT_A_PERFORMANCE + SLUR_NOT_A_STROKE
    + r".*?\bslurring\s+(?:my|his|her|their|your|our)\s+(?:speech|words|voice|sounds)\b",
    SLUR_NOT_A_STROKE + r".*?\b(?:(?:my|his|her|their|our)(?:\s+\w+){1,2}|he|she|they|i)"
    r"\s+(?:is|am|was|were|are|keeps?|kept|started)\s+slurring\b",
    r"\b(?:talking|speaking)\s+(?:all\s+|a\s+bit\s+|really\s+)?(?:slurred|slurry)\b",
    r"\b(?:speech|words|voice|talking)\s+(?:is|are|was|were|'s|sounds?|seems?)\s+(?:a\s+bit\s+|all\s+)?"
    r"(?:slurred|slurry|slushy|thick)\b"
    r"(?!.{0,30}\b(?:" + SLUR_CAUSE_WORDS + r")\b)",
    r"\b(?:can't|cannot)\s+speak\b(?=\s*(?:$|[,.!?;]|at\s+all\b|properly\b|clearly\b|"
    r"any\s?more\b|any\s+longer\b|well\b))",
    r"\b(?:can't|cannot)\s+speak\b(?=[^.!?]{0,60}\b(?:arm|leg|side|weak\w*|numb|"
    r"droop\w*|slurr\w*|confus\w*|face|mouth)\b)",
    r"\b(?:can't|cannot)\s+move\s+(?:my\s+)?(?:arm|leg|side|left|right)\b",
    r"\bnumb\s+(?:down\s+)?(?:on\s+)?(?:one\s+side|my\s+left|my\s+right|one\s+arm|half\s+of\s+my\s+face)\b",
    r"\b(?:can'?t|cannot|couldn'?t|could\s+not|can\s+not)\s+feel\s+(?:my|his|her|their|our)\s+"
    r"(?:whole\s+|entire\s+)?(?:left|right)\s+(?:side|arm|body|face)\b",
    r"\b(?:can'?t|cannot)\s+feel\s+(?:anything\s+)?(?:at\s+all\s+)?(?:down\s+|on\s+)?"
    r"(?:one\s+side|half\s+of\s+my\s+body|half\s+of\s+my\s+face)\b",
    r"\bno\s+feeling\s+(?:at\s+all\s+)?(?:in|down|on)\s+(?:my|his|her|their|the)\s+"
    r"(?:left|right)\s+(?:side|arm|body|face)\b",
    r"\b(?:lost|gone)\s+(?:the\s+)?(?:feeling|sensation)\s+in\s+(?:my|his|her|their)\s+"
    r"(?:left|right)\s+(?:side|arm|body|face)\b",
    r"\bworst\s+headache\s+of\s+my\s+life\b", r"\bsudden(?:ly)?\s+(?:can't\s+see|lost\s+my\s+vision|numb)\b",
    r"\b(?:having|'s\s+having|is\s+having|think\w*|suspect\w*|probably|might\s+be)\b"
    r"(?:\s+\w+){0,3}\s+(?:a\s+|another\s+)?stroke\b",
    r"\bstroke\s+(?:right\s+)?now\b",
    r"\bjust\s+had\s+(?:a\s+)?stroke\b",
    r"\bhad\s+(?:a\s+)?stroke\s+(?:this\s+(?:morning|afternoon|evening)|today|yesterday|"
    r"an?\s+hour\s+ago)\b",
    _both_here(STROKE_HAND, STROKE_HAND_BESIDE),
)

SLUR_NOT_DENTAL = r"\A(?!.*\b(?:" + DENTAL_WORDS + r")\b)"
SIGHT_WORD = (
    r"\b(?:blind|sight|vision|eyes?)\b",
    r"\b(?:can'?t|cannot|can\s+not)\s+see\b",
    r"\b(?:lost|loss)\s+(?:the\s+)?(?:sight|vision)\b",
)


PEOPLE = (r"(?:i|i'm|i've|he|he's|she|she's|they|they're|we|you|someone|somebody|anyone|everyone|"
          r"my\s+" + PERSON + r"|the\s+" + PERSON + r"|" + PERSON + r")")

A_HABITUAL_COLLAPSE = (
    r"\b(?:might|may|could|would)\s+(?:collapse|collapsed|collapsing|pass\s+out|passed\s+out|passing\s+out|"
    r"faint|fainted|fainting|go\s+down|went\s+down|going\s+down)\b",
    r"\b(?:nearly|almost|about\s+to)\s+(?:collapse|collapsed|collapsing|pass\s+out|passed\s+out|"
    r"passing\s+out|faint|fainted|fainting|go\s+down|went\s+down|going\s+down)\b",
    r"\bfeel(?:s|ing|t)?\s+like\s+(?:\w+\s+){0,4}(?:collapse|collapsing|passing\s+out|fainting|going\s+down)\b",
    r"\bwhen(?:ever)?\s+(?:i|we|you|he|she|they|my\s+" + PERSON + r"|the\s+" + PERSON + r")\b"
    r"(?:\s+\w+){0,4}\s+(?:stand|stands|standing|stood|get|gets|getting|got|sit|sits|sitting|sat)\b",
    r"\b(?:on|after|from|when)\s+standing\b",
    r"\b(?:every|each)\s+time\b", r"\bwhenever\b", r"\b(?:sometimes|often|always)\b",
    r"\btoo\s+fast\b",
    r"\bin\s+the\s+(?:heat|hot\s+weather)\b",
    r"\bif\s+(?:i|we|he|she|they)\s+(?:don'?t|dont|didn'?t|didnt|miss|misses|skip|skips)\b",
)
NOT_A_COLLAPSE_NOW = r"(?![\s\S]*(?:" + "|".join(A_HABITUAL_COLLAPSE) + r"))"


OTHERS = (r"(?:he|he's|she|she's|they|they're|him|her|them|someone|somebody|anyone|everyone|"
          r"my\s+" + PERSON + r"|his\s+" + PERSON + r"|her\s+" + PERSON + r"|their\s+" + PERSON + r"|"
          + PERSON + r")")
TALKS_ABOUT_IT = (
    r"\b" + OTHERS + r"\b[^.?!]{0,40}\b(?:keeps?|kept|keeps\s+on)\s+(?:talking|mentioning|"
    r"saying|joking|going\s+on)\s+(?:about\s+)?(?:ending\s+(?:it|things)\s+all|suicid(?:e|"
    r"al)(?!\s*(?:rates?|statistics?|figures?|numbers))|killing\s+(?:him|her|them)sel(?:f|ves)|"
    r"not\s+being\s+here|want(?:s|ing|ed)?\s+to\s+die|dying)\b",
)
SOMEONE_ELSE_RISK = (
    r"\b" + OTHERS + r"\b.{0,40}\b(?:wants?\s+to\s+(?:die|kill\s+(?:him|her|them)sel(?:f|ves)|"
    r"end\s+(?:it|his\s+life|her\s+life))|(?:is|are)\s+going\s+to\s+kill\s+(?:him|her|them)sel(?:f|ves)|"
    r"suicidal|overdos\w*|(?:took|taken|swallowed)\s+(?:an?\s+overdose|pills|tablets|too\s+many)|"
    r"locked\s+(?:him|her)self\s+in\b.{0,40}\bpills\b)\b",
    r"\b(?:kill|hang)\s+(?:him|her|them)self\b(?!\s+(?:upside|on\s+the\s+(?:bars|swing)|from\s+the\s+bars))",
    r"\b(?:he|she|they)'?s?\s+been\s+(?:self[-\s]?harming|cutting)\b",
    _HURTING_THEMSELVES,
    r"\b" + OTHERS + r"\b.{0,40}\b(?:(?:keeps?|kept)\s+thinking\s+(?:about|of)\s+"
    r"(?:ending\s+(?:it|his\s+life|her\s+life|their\s+life)|killing\s+(?:him|her|them)sel(?:f|ves)|"
    r"dying)|feels?\s+(?:like|as\s+if)\s+(?:ending\s+(?:it|his\s+life|her\s+life|their\s+life)|"
    r"killing\s+(?:him|her|them)sel(?:f|ves)|dying))\b",
    *TALKS_ABOUT_IT,
)
SOMEONE_ELSE_RISK = (*SOMEONE_ELSE_RISK, *HELP_SOMEONE)
THIRD_PERSON_WISH = (
    r"\b" + OTHERS + r"\b[^.?!]{0,30}\b(?:wants?\s+to|keeps?\s+saying\s+(?:he|she|they)\s+wants?\s+to|"
    r"says?\s+(?:he|she|they)\s+wants?\s+to|told\s+me\s+(?:he|she|they)\s+wants?\s+to)"
    r"\s+be\s+dead\b",
    r"\b" + OTHERS + r"\b[^.?!]{0,30}\b(?:doesnt|doesn'?t|does\s+not|didnt|didn'?t|did\s+not|"
    r"dont|don'?t|do\s+not)\s+want\s+to\s+(?:"
    r"live(?!\s+(?:here|there|with|in|at|on|near|abroad|alone|anywhere|somewhere|off)\b)|"
    r"be\s+here|be\s+alive|exist|be\s+around\s+(?:any\s?more|no\s?more)|"
    r"(?:carry|go)\s+on(?=\s*(?:[.?!]|$)|\s+(?:any\s?more|no\s?more)\b))"
    r"(?!\s+(?:at|on|for|in|with|to)\b)",
)


SOMEONE_ELSE_RISK = (*SOMEONE_ELSE_RISK, *THIRD_PERSON_WISH)
SUICIDE_OTHER = (
    r"\b(?:he|she|they|someone|somebody|anyone|a\s+(?:person|friend|man|woman|boy|girl)|"
    r"my\s+(?!own\b)" + PERSON + r")\b[^.?!]{0,40}\b(?:suicid\w*|"
    r"end(?:ing)?\s+(?:it(?!\s+with\s+" + END_IT_WITH_PERSON + r"\b)|things\s+all\b)|"
    r"kill(?:ed|ing)?\s+(?:him|her|them)sel(?:f|ves))\b",
)
DEATH_REPORT = (
    r"\b(?:died|dies|dead|passed\s+away|killed\s+(?:him|her|them)sel(?:f|ves)|took\s+(?:his|her|"
    r"their)\s+own\s+life|committed\s+suicide)\b",
)
OWN_DISTRESS = (
    r"\bi\s+(?:want|wanna|feel|felt|keep|kept|am|im|i'm|was|have|had|think|thought|plan|planned)"
    r"\b[^.?!]{0,25}\b(?:suicid\w*|die|dying|dead|end(?:ing)?\s+(?:it|things)\s+all|"
    r"kill\s+my\s*self|hurt\s+my\s*self)\b",
    r"\bmyself\b",
)
SHAKEN_FINE = (
    r"\b(?:awake|to\s+wake|gently|playfully|to\s+wake\s+(?:him|her|them)|rattle|toy|bottle|"
    r"blanket|milk)\b",
)
HUMAN_ANCHOR = ((r"\b(?:i|i'm|i've|he|she|someone|somebody|anyone|everyone)\b|"
                 r"\b(?:my|the)\s+" + PERSON + r"\b|\b" + PERSON + r"\b|" + AGE_PERSON[0]),)
PERSON_WORD = ((r"\b(?:my|the)\s+" + PERSON + r"\b|\b" + PERSON + r"\b"),)

PET_MOUTH = (r"\b(?:gums?|gum\s?colou?r)\b",)
PET_BLUE_WENT = (r"\bwent\s+(?:blue|grey|gray)\b", r"\b(?:is|was|looks?)\s+(?:blue|grey|gray)\b")
PET_BLUE_PART = (
    r"\b(?:lips?|tongue|mouth|gums?|face|nose|paws?|tummy|belly|skin|ears?|eyes?|nails?)\b",
)
BLUE_LIPS_FACE = (
    r"\b(?:lips?|face|around\s+the\s+(?:lips?|mouth)|round\s+the\s+(?:lips?|mouth))\b",
)
BLUE_LIMB = (
    r"\b(?:fingertips?|fingers?|hands?|toes?|feet|legs?|arms?|tongue|mouth|skin|cheeks?|knees?|"
    r"nails?|nail\s?beds?|gums)\b",
)
BLUE_MARK = (
    r"\b(?:bruise|bruises|bruised|bruising|vein|veins|mark|marks|spot|spots|patch|patches|"
    r"tattoo|scar|scars|nail\s?varnish|plaster|bandage|dressing|nappy|nappies|ring|rings)\b",
)
BLUE_COLD = (
    r"\b(?:cold|freezing|frozen|chilly|perishing|slushie|slush|ice|iced|lolly|popsicle|"
    r"snowball|snow)\b",
)
LIPS_RED_FLAG = (
    r"\b(?:breath\w*|gasping|struggling|chest|collapsed|unresponsive|not\s+responding|floppy|"
    r"limp|sleepy|grunting|shivering\s+badly|shaking)\b",
    r"\b(?:baby|babies|newborn|child|children|kid|kids|son|daughter|toddler|infant|boy|girl)\b",
)

BLUE_COLD_SELF = (r"\b(?:in|from|out\s+in)\s+the\s+cold\b",)
BLUE_SELF = (
    r"\b(?:i|i'?m|im|me|myself)\b",
    r"\bmy\s+(?:hands?|fingers?|fingertips?|toes?|feet|legs?|arms?|skin|knees?|nails?)\b",
)

BLUE_CHANGE = (
    r"\b(?:turned|turning|goes|going|gone|get|gets|getting|is\s+turning|looks?|looking|looked|"
    r"appears?|seems?|become|becomes|becoming|suddenly|started?)\b",
)


FADE_EVERYDAY = (
    r"\b(?:tan|tans|tanning|sunburn\w*|scar|scars|scarring|scab|scabs|eczema|psoriasis|"
    r"birthmark\w*|bruise|bruises|stain|stains|freckl\w*|hickey|fake\s+tan|marker|biro|pen\s+mark)\b",
)


def _glass_test_line(line, before):
    if _matches(FADE_EVERYDAY, line):
        return False
    if not (_matches(RASH_FADE, line) and _matches((RASH,), before)):
        return False
    return _matches(RASH_COMPANY, line) or _matches(RASH_COMPANY, before)


def _said_before(memory, turns=2):
    said = []
    for turn in reversed((memory.get("turns") or [])[-turns:]):
        if isinstance(turn, dict) and turn.get("user"):
            said.append(_norm(str(turn["user"])))
    return " ".join(said)


def _person_before(memory):
    turns = memory.get("turns") or []
    for turn in reversed(turns[-3:]):
        if isinstance(turn, dict) and turn.get("user"):
            return _norm(turn["user"])
    return ""


_FIRST_PERSON_ME = (r"\b(?:i\s+want|i\s+don't\s+want|i'?ve\s+(?:taken|took)|killing\s+my\s*self|"
                    r"kill\s+my\s*self|hurt\s+my\s*self|end\s+it\s+all)\b",)

OWN_WISH = (
    r"\bi\s+(?:want|wanted|wanna|dont|don'?t|feel\s+like|feel|felt|plan|planning|can'?t|cant|won'?t|"
    r"would\s+rather|rather)\b[^.?!]{0,30}\b(?:die|dying|dead|end(?:ing)?\s+it|end\s+my(?:\s+own)?\s+"
    r"life|kill\s+my\s*self|live|here|go\s+on|carry\s+on|not\s+being\s+here)\b",
    r"\bmyself\b", r"\bnothing\s+(?:left\s+)?to\s+live\s+for\b",
    r"\b(?:nobody|no\s?one)\s+would\s+(?:notice|care|miss\s+me)\b",
    r"\bbetter\s+off\s+(?:dead|without\s+me|if\s+i\s+was\s+gone)\b",
    r"\bnot\s+worth\s+(?:it|living)\b",
    r"\bi\b[^.?!]{0,20}\b(?:keep|keeps|kept)\s+(?:thinking|having\s+thoughts)\s+(?:about|of)\s+"
    r"(?:ending|killing|dying|suicide|not\s+being\s+here)\b",
    r"\bi\s+(?:think|thinks|thought|dream)\s+(?:about|of)\s+(?:ending|killing|suicide|dying|dead)\b",
)

WISH_OWN_BARE = tuple(p for p in OWN_WISH if p != r"\bmyself\b")


def _own_wish(line):
    return _matches(WISH_OWN_BARE, line) or (_matches((r"\bmyself\b",), line)
                                             and not _matches(SELF_TALK, line))


NOT_WAKE_MODAL = (r"(?:won'?t|wont|wouldn'?t|wouldnt|couldn'?t|couldnt|didn'?t|didnt|"
                  r"can'?t|cant|cannot|isn'?t|isnt|is\s+not|not|never)")
PRO_NOT_ANSWERING = (
    r"\b(?:my|his|her|their|our|the)\s+(?:carers?|care\s+workers?|support\s+workers?|"
    r"social\s+workers?|personal\s+assistants?|nurses?|midwives?|midwife|doctors?|gps?|"
    r"physios?|therapists?)\b[^.?!]{0,30}\b(?:isn'?t|is\s+not|not|hasn'?t|has\s+not|never|"
    r"no)\s+respond(?:ing|ed|e)?\b",
    r"\bno\s+response\s+from\s+(?:my|the|our)\s+(?:carer|care\s+worker|support\s+worker|"
    r"social\s+worker|personal\s+assistant|nurse|doctor|gp|physio|therapist)s?\b",
)
UNRESPONSIVE_MANNER = (
    r"\b(?:to|about|on|in)\s+(?:my|his|her|their|the|our|a|an)?\s*\w*\s*"
    r"(?:texts?|emails?|e-?mails?|messages?|msgs?|calls?|letters?|questions?|requests?|"
    r"complaints?|invites?|applications?|interviews?|thread|group\s+chat|whatsapp|facebook|"
    r"social\s+media|feedback|criticism|suggestions?)\b",
    r"\bwhen(?:ever)?\s+(?:he|she|they|i|we)(?:'s|s|'re|re)?\b[^.?!]{0,25}"
    r"\b(?:told\s+off|told\s+no|told|ignored|shouted\s+at|ticking\s+off|naughty|"
    r"in\s+trouble|sulking|sulky|pulling\s+a\s+face)\b",
    r"\b(?:at\s+(?:work|school|college|uni|university)|in\s+meetings?|on\s+the\s+group)\b",
)
BODY_IN_THE_ROOM = (
    r"\b(?:floor|ground|bed|sofa|settee|couch|bath|pavement|street|doorstep)\b",
    r"\b(?:collapsed|collapsing|fell|fallen|fainted|pass(?:ed)?\s+out|seizure|fitting)\b",
    r"\b(?:breathing|breath|breathe|pulse|blue|lips|cold|clammy|sweating|eyes|pale|grey|gray)\b",
    r"\b(?:unconscious|out\s+cold|in\s+front\s+of\s+me|with\s+me|next\s+to\s+me)\b",
    r"\b(?:to\s+(?:pain|touch|voices?|noise|light|stimulus)|(?:his|her|their)\s+name)\b",
)
UNCONSCIOUS = (
    r"\bunconscious\b(?!\s+(?:bias|biases|mind|thought|thoughts|desire|wish|belief|prejudice|"
    r"process|choice|decision|level))",
    r"\b" + NOT_WAKE_MODAL + r"\s+waking\s+up\b",
    r"\b(?:he|she|they|my\s+" + PERSON + r"|the\s+" + PERSON + r")\b(?:\s+\w+){0,3}\s+"
    + NOT_WAKE_MODAL + r"\s+wak(?:e|ing)\b",
    r"\b" + NOT_WAKE_MODAL + r"\s+wake\s+(?:him|her|them)\b",
    r"\bon\s+the\s+(?:floor|ground)\b.{0,30}\b" + NOT_WAKE_MODAL + r"\s+wak(?:e|ing)\b",
    r"\b" + NOT_WAKE_MODAL + r"\s+(?:be\s+)?woken\b", r"\bpassed\s+out\b.{0,20}\b(?:and|not)\b",
    r"\bout\s+cold\b[^.?!]{0,40}\b(?:won'?t|wont|wouldn'?t|wouldnt|couldn'?t|couldnt|"
    r"can'?t|cant|not|didn'?t|didnt)\s+wak(?:e|ing|en)\b",
    r"\b(?:won'?t|wont|wouldn'?t|wouldnt|couldn'?t|couldnt|can'?t|cant|not)\s+wak(?:e|ing|en)\b"
    r"[^.?!]{0,30}\bout\s+cold\b",
    r"\bno\s+pulse\b",
    r"\bpassed\s+out\b(?:\s+\w+){0,3}\s+on\s+(?:the\s+)?(?:floor|ground|pavement|street)\b",
    r"\b" + PEOPLE + r"\b\s+(?:just|suddenly|then)\s+passed\s+out\b(?!\s+(?:laughing|crying))",
    r"\b" + PEOPLE + r"\b(?:\s+\w+){0,3}\s+(?:is\s+|isn't\s+|is\s+not\s+)?not\s+responding\b"
    r"(?!\s+(?:well\b|" + RESPOND_SENSE + r"))",
    r"\b(?:he|she|they|my\s+" + PERSON + r")\s+(?:is|'s)\s+not\s+responsive\b",
    r"\b\s?(?:(?:he|she|they)\b|(?:my|his|her|their|our|the)\s+" + PERSON + r"\b)"
    r"(?:\s+\w+){0,3}\s+(?:is|are|was|were|'s|'re|seems?|looks?|has\s+gone|have\s+gone|now)\s+"
    r"(?:now\s+)?unresponsive\b"
    r"(?!\s+(?:to\s+(?:[\w']+))?\s*(?:food|dinner|tea|treats?|name|his|her|their|my)\b)",
    r"\bon\s+the\s+(?:floor|ground)\b[^.?!]{0,40}\b(?:not\s+responding|unresponsive)\b",
    r"\b(?:he|she|they|my\s+" + PERSON + r"|the\s+" + PERSON + r")\b(?:\s+\w+){0,3}\s+"
    r"(?:won't|wont|isn'?t|is\s+not|not)\s+respond(?:ing)?\b(?!\s+(?:well\b|" + RESPOND_SENSE + r"))",
    r"\b(?:he|she|they)(?:'s|s|'re|re)\s+(?:not\s+responding|unresponsive)\b"
    r"(?![\s-]*(?:well\b|to\s+(?!(?:pain|painful|touch|stimulus|stimuli|light|voices?|noise|sound|"
    r"anything|anyone|me|us|a\s+word|(?:the|a)\s+light|"
    r"(?:a\s+)?painful\s+stimulus|my\s+voice|his\s+voice|her\s+voice|their\s+voice|"
    r"(?:his|her|their|my|the)\s+name)\b)"
    r"|when|whenever|if|because|as\s+(?:usual|always|normal|ever)|as\s+he|as\s+she|as\s+they|"
    r"lately|recently|these\s+days|at\s+(?:work|school|college|uni|university))\b)"
    r"(?![\s\S]*\b(?:fever|temperature|sepsis|rigors|shivering|infection)\b)",
    NOT_A_COLLAPSE_NOW + r"\b" + PEOPLE + r"\b(?:\s+\w+){0,4}\s+collaps(?:e|es|ed|ing)\b",
    NOT_A_COLLAPSE_NOW + r"\bcollaps(?:e|es|ed|ing)\b.{0,30}\b(?:and\s+(?:isn't|is\s+not|won't|wont|stopped|not)\s+(?:breathing|waking|responding|conscious)|"
    r"on\s+(?:the\s+)?(?:floor|ground|pavement|street|kitchen\s+floor|bathroom\s+floor))\b",
    r"\b(?:he|she|they|my\s+" + PERSON + r")\s+(?:is|'s)\s+out\s+cold\b",
    r"\b(?:collapsed|came\s+down|fell)\b.{0,30}\b(?:on|onto|over|on\s+top\s+of)\s+(?:the\s+|my\s+|his\s+|"
    r"her\s+|our\s+|a\s+)?" + PEOPLE + r"\b",
)


THING_FIT_SUBJECT = (
    r"\b(?:my|the|our|his|her|their|your)\s+(?:laptop|computer|pc|phone|printer|car|van|engine|"
    r"boiler|washing\s+machine|dishwasher|fridge|freezer|telly|tv|wifi|internet|heating|"
    r"shower|oven|kettle|hoover|vacuum|mower|motorbike|bike|scooter|website|site)\b",
)
ANIMAL = (
    r"\b(?:dog|puppy|pup|cat|kitten|horse|pony|rabbit|hamster|guinea\s+pig|parrot|budgie|bird|"
    r"ferret|tortoise|snake|pet)\b",
)

CHOKE_WORDS = (
    r"\bchok(?:e|ed|es|ing)?\s+on\s+(?:(?:my|his|her|their|your|our|the|a|an)\s+)?(?:own\s+)?"
    r"(?:words?|sentences?|speech|lines?|names?|syllables?|pronunciation)\b",
)


BLUE_FACE_PART = (r"\blips?\b", r"\bface\b", r"\bmouth\b", r"\btongue\b")
BLUE_COSMETIC = (
    r"\b(?:make-?up|lipstick|lip\s+gloss|lip\s+stain|lip\s+balm|gloss|tint|blusher|bronzer|"
    r"eyeshadow|eye\s+shadow|foundation|contour|filter|photo\w*|zoom|selfie|camera|webcam|"
    r"screen|monitor|lighting|light\s+is|bad\s+light|the\s+light|in\s+this\s+light)\b",
)
OTHER_BODY = (
    r"\b(?:he|she|they|him|her|them)\b",
    r"\b(?:my|our|his|her|their|the)\s+" + PERSON + r"\b",
    r"\b(?:his|her|their)\s+(?:lips?|face|mouth|tongue|hands?|fingers?|fingertips|toes?|feet|"
    r"foot|arms?|legs?|throat|head)\b",
)
RAYNAUD = (
    r"\b(?:fingers?|fingertips|hands?|toes?|feet|foot)\b[^.?!]{0,40}\b(?:white|blue|purple|grey|"
    r"gray|numb|dead|burning)\b",
    r"\braynaud\w*\b",
)
LIMB_PART = (
    r"\b(?:fingers?|fingertips|hands?|toes?|feet|foot|arms?|legs?|fingernails?|nails?)\b",
)
WENT_BLUE_BREATH_RED = (
    r"\b(?:can'?t|cannot|not|struggling\s+to|stopped)\s+breath\w*\b", r"\bgasping\b",
    r"\bunconscious\b", r"\blimp\b", r"\bfloppy\b", r"\bunresponsive\b",
    r"\bnot\s+waking\b", r"\bchoking\b", r"\bfaint\w*\b",
)
WENT_BLUE_RED = (
    r"\b(?:can'?t|cannot|not|struggling\s+to|stopped)\s+breath\w*\b", r"\bgasping\b",
    r"\blips?\b", r"\bface\b", r"\bunconscious\b", r"\blimp\b", r"\bfloppy\b",
    r"\bunresponsive\b", r"\bnot\s+waking\b", r"\bchoking\b",
)
STUCK_FINE = (
    r"\b(?:jar|bottle|lid|zip|zipper|box|tin|can|bucket|tube|boot|shoe|lock|tap|plug|key|hole)\b",
)


DROWNING = (
    r"\b(?:he|she|they|my\s+\w+|someone)\s+(?:is\s+|'s\s+)?drowning\b", r"\b(?:pulled|dragged|got)\s+(?:him|her|them|someone)\s+out\s+of\s+the\s+(?:water|pool|sea)\b",
    r"\bnearly\s+drowned\b", r"\b(?:stopped|not)\s+breathing\s+after\s+(?:the\s+)?water\b",
)
WATER_DANGER_PERSON = (
    r"\b(?:baby|babies|newborn|infant|son|daughter|child|children|kid|kids|boy|girl|toddler|"
    r"little\s+one|niece|nephew|grandson|granddaughter|he|she|him|her|them|they|someone|"
    r"somebody|anyone|i|me|my|we|us|our)\b",
)
WATER_SELF_PUSH_FINE = (
    r"\b(?:mate|mates|friend|friends|brother|sister|cousin|husband|wife|partner|kids?|lads?|"
    r"guys?|son|daughter|he|she|they)\b[^.?!]{0,15}\b(?:pushed|shoved|threw|tipped|knocked)\s+me"
    r"\s+(?:in|into)\b",
)
WATER_PET = (
    r"\b(?:dogs?|doggy|pupp(?:y|ies)|cats?|kittens?|horses?|pon(?:y|ies)|rabbits?|bunny|"
    r"guinea\s+pig|hamsters?|ferrets?|parrots?|chickens?|hens?|cows?|sheep|lambs?|goats?|"
    r"pigs?|piglets?|tortoises?|lizards?|snakes?|budgies?|gerbils?|mice|mouse|rats?|pets?)\b",
)
WATER_STORY = (
    r"\b(?:yesterday|last\s+(?:night|week|month|year|summer|winter|spring)|years?\s+ago|"
    r"when\s+i\s+was\s+(?:a\s+)?(?:child|kid|boy|girl|little|younger|small)|used\s+to)\b",
)
WATER_SELF_DIP = (
    r"\bi\s+(?:went|go|goes|gone|sank|sunk|dived?|dove|swam)\s+(?:under|below)\b",
)
WATER_BREATH_RED = (
    r"\b(?:couldn'?t|could\s+not|can'?t|cant|not|stopped|struggl\w+|fought)\b[^.?!]{0,15}"
    r"\b(?:breath\w*|breathing)\b",
)
WATER_SWIM = (
    r"\b(?:swims?|swam|swum|swimming|dives?|dived|dove|going|goes|gone|can\s+swim|"
    r"learning\s+to\s+swim|learnt)\s+underwater\b",
    r"\bunderwater\s+(?:now|too|as\s+well)\b",
    r"\bunderwater\s+for\s+the\s+first\s+time\b",
)
WATER_STILL_BAD = (
    r"\b(?:not\s+breathing|didn'?t\s+come|hasn'?t\s+come|limp|unresponsive|not\s+moving|"
    r"blue|still\s+under|under\s+for|couldn'?t\s+get\s+(?:him|her|them|me)\s+(?:out|up)|"
    r"(?:can'?t|cant|couldn'?t)\s+see)\b",
)


SNAKE_BITE = (
    r"\b(?:snake|adder|adders|viper|cobra|rattlesnake|mamba|krait)\b[^.?!]{0,30}"
    r"\b(?:bit|bite|bitten|bit\s+me|struck|sting|stung)\b",
    r"\b(?:bit|bitten|stung|sting)\s+(?:by|on\s+the\s+\w+\s+by)\s+(?:a|an|the|my|his|her|this)\s*"
    r"(?:snake|adder|viper|cobra)\b",
)
ANIMAL_KICK_LOOKALIKE = (
    r"\b(?:fence|gate|stable|door|barn|bucket|ball|trolley|car|trailer|wall|post)\b",
    r"\b(?:kicks?\s+off|kick\s+off|kicked\s+off)\b",
)
STRANGLE_OWN_HANDS = (
    r"\bi\s+(?:put|place[ds]?|putting|wrap(?:ped|ping|s)?|wound|kept|have|had|got|held|cups?|"
    r"cupped|rest(?:ed|ing)?|tucked)\b[^.?!]{0,20}\bmy\s+(?:own\s+)?hands?\b",
)

STRANGLE_LOOKALIKE = (
    r"\b(?:jokingly|playfully|for\s+a\s+laugh|mucking\s+about|messing\s+about|in\s+judo|"
    r"at\s+judo|wrestling|in\s+training|during\s+training|at\s+rugby|in\s+the\s+scrum|"
    r"in\s+fun|as\s+a\s+joke)\b",
    r"\b(?:collar|tie|scarf|seatbelt|seat\s+belt|strap|helmet|necklace|hoover|vaccum|"
    r"vacuum|lettuce|pipe|hose|noose\s+of)\b",
    r"\b(?:business|company|economy|budget|deadline|bills?|rent|workload|club|team|crop|"
    r"market|industry|startup|shop|sales|paperwork|red\s+tape|admin|forms?|tax|taxes|"
    r"regulations?|rules|bureaucracy|traffic|inbox|emails?)\b",
    *STRANGLE_THING_SUBJECT,
    *STRANGLE_OWN_HANDS,
)


GAS_IN_ROOM = (
    r"\b(?:kitchen|boiler|oven|cooker|hob|flat|house|home|room|garage|meter|pipe|pipes|heater|"
    r"fire|cooker|cylinder|hall|hallway|bathroom|cellar|basement|camper|caravan|shop|workshop)\b",
)

GAS_NOW = (
    r"\b(?:still|now|right\s+now|just\s+now|this\s+(?:morning|afternoon|evening)|tonight|today|"
    r"again|earlier\s+today)\b",
    r"\b(?:can|could)\s+(?:i|you|we|she|he|they)\s+smell\b",
)


BREATH_AT_REST = (
    r"\b(?:at\s+rest|sit(?:ting)?\s+still|sat\s+still|in\s+bed|lying\s+down|lie\s+down|"
    r"laying\s+down|doing\s+nothing|resting)\b",
)
EFFORT_WEAK = (r"\b(?:singing|sing|laughing|talking|chatting)\b",)
OUT_OF_BREATH = (r"\bout\s+of\s+breath\b",)
NOT_A_BREATHER = (
    r"\b(?:app|apps|website|server|network|wifi|router|phone|laptop|computer|pc|telly|tv|car|"
    r"cars|van|bike|motorbike|engine|boiler|radiator|pump|machine|washer|hoover|vacuum|pipe|"
    r"fan|heater|fridge|freezer|oven|projector|console)\b",
)
PET_RESPOND_SENSE = (r"(?:(?:his|her|its|their|the|my|our)\s+)?(?:name|treats?|food|dinner|tea|"
                     r"recall|call|toys?|lead|whistle|clicker|catnip|nip|commands?|laser|ball|"
                     r"kibble|chews?)\b")
PET_UNRESPONSIVE = (r"\bunresponsive\b(?!\s*(?:to\s+(?:(?:his|her|its|their|my|our|the|a|an)\b|"
                    + PET_RESPOND_SENSE + r")|when\s+(?:i|we|you)\b))")
PET_PET_NAMES = (r"dogs?|cats?|pupp(?:y|ies)|kittens?|pups?|pets?|parrots?|hamsters?|rabbits?|"
                 r"bunn(?:y|ies)|horses?|pon(?:y|ies)|budgies?|guinea\s+pigs?|tortoises?|ferrets?|"
                 r"gerbils?")
PET_WAKE = (r"\b(?:won'?t|wont|can'?t|cannot|unable\s+to|isn'?t|is\s+not|not)\s+wak(?:e|ing)\s+"
            r"(?:up\s+)?(?:my|our|the|his|her)\s+(?:" + PET_PET_NAMES + r")\b"
            r"(?!\s*(?:me|us|you|him|her|them)\b)")
PET_HARM = (
    r"\b(?:" + PET_PET_NAMES + r")\b"
    r".{0,60}\b(?:chok\w*|swallow\w*|ate|eaten|eats|lick\w*|chew\w*|bit|bitten|gasp\w*|"
    r"drank|drunk|poison\w*|bleeding|hurt|fell|sick|breathing|breath\w*|limp\w*|paws?|hit\s+by|"
    r"ran\s+over|"
    r"collapse\w*|unconscious|" + PET_UNRESPONSIVE + r"|(?:stopped|not|isn'?t)\s+eating|trouble\s+breathing|"
    r"(?:won'?t|wont|can'?t|cannot|unable\s+to|isn'?t|is\s+not|not)\s+wak\w*"
    r"(?!\s+(?:me|us|you|him|them)\b)|\b(?:be\s+)?woken\b|"
    r"(?:not|isn'?t|stopped|won'?t|wont)\s+respond\w*(?!\s+(?:to|for)\s+(?:"
    + PET_RESPOND_SENSE + r"))|breathing\s+(?:funny|oddly|strangely|weirdly|noisily|"
    r"with\s+a\s+(?:rasp|rattle))|(?:hasn'?t|has\s+not|not|isn'?t)\s+mov\w*|fitting(?!\s+in)|"
    r"(?:having|had|has|in)\s+(?:a\s+)?fits?|went\s+floppy|flopp\w*|"
    r"won'?t\s+wake|wont\s+wake|"
    r"seizure\w*|not\s+moving)\b",
)
PET_OWN = (
    r"\b(?:my|our|the|his|her|their|a|this)\s+(?:dog|dogs|cat|cats|puppy|puppies|kitten|kittens|"
    r"pup|pet|parrot|budgie|hamster|rabbit|bunny|horse|pony|guinea\s+pig|tortoise|ferret|gerbil|"
    r"rat|lizard|snake|hen|chicken)\b",
)
OTHER_DYING = (
    r"\b(?:my|our|her|his|their)\s+" + PERSON + r"\b[^.?!]{0,20}\b(?:going\s+to|gonna|will|"
    r"about\s+to|soon\s+to)\s+(?:die|pass\s+away)\b",
)
PET_SKIN_PET = (
    r"\b(?:my|our|the|his|her|their)\s+(?:dog|dogs|cat|cats|puppy|puppies|kitten|kittens|rabbit|"
    r"rabbits|bunny|bunnies|hamster|hamsters|guinea\s+pig|guinea\s+pigs)\b",
)
PET_HURTING_ITSELF = (
    PET_SKIN_PET[0] + r"[^.?!]{0,30}?\b(?:scratch\w*|itch\w*|bit(?:e|es|ing|ten)?|chew\w*|"
    r"lick\w*|gnaw\w*|rub(?:s|bed|bing)?|nip(?:s|ped|ping)?)\b[^.?!]{0,26}"
    r"\b(?:him|her|it)sel(?:f|ves|vesd)?\b",
)
PET_NOW = (
    r"\bstill\b", r"\bright\s+now\b", r"\bcan'?t\s+breathe\b", r"\bnot\s+breathing\b",
    r"\bchoking\b",
)
PET_FINE = (
    r"\b(?:seems?|is|was|looks?)\s+(?:fine|ok|okay|alright)\b", r"\blanded\s+on\s+(?:his|her|its)\b",
    r"\bjumped\s+back\s+up\b", r"\bnothing\s+(?:wrong|broken)\b",
)
PET_MILD = (
    r"\b(?:a\s+bit|a\s+little|slightly|small|tiny|little)\b.{0,25}\b(?:bleed\w*|blood|cut|"
    r"scratch\w*|sore|nick\w*)\b",
    r"\b(?:bleed\w*|cut|scratch\w*|nick\w*)\b.{0,15}\b(?:a\s+bit|a\s+little|slightly)\b",
)
PET_GASP = (r"\bgasp\w*",)
PET_GASP_NOUN = (r"\bgasp(?:er|ers|y)\b",)
PET_GASP_ONGOING = (
    r"\bkeep\w*\b", r"\bstill\b", r"\bagain\b", r"\bfor\s+(?:air|breath)\b",
)
PET_GASP_SLEEP = (
    r"\b(?:sleeps?|sleeping|asleep|naps?|napping|dozes?|dozing|dreams?|dreaming|dreamt)\b",
)
PET_GASP_SLEEP_FINE = (
    r"\b(?:snor\w*|snort\w*|snuffl\w*|pant\w*|dream\w*|twitch\w*|whin\w*|"
    r"sleep[\s-]?talk\w*|sleep[\s-]?walk\w*)\b",
)
PET_GUMS_TOLD = (r"\b(?:blue|pale|white|grey|gray|bright\s+red)\b",)
PET_BREATH_ODD = (
    r"\bbreath\w*\s+(?:funny|odd|oddly|strange|strangely|weird|weirdly|noisily|loudly|"
    r"differently)\b",
)
PET_EATEN_THING = (
    r"\bchok\w*", r"\b(?:ate|eaten|eats|swallow\w*|poison\w*|drank|drunk|lick\w*|chew\w*)\b",
)
TOOTH_CHIPPED_FINE = (
    r"\bmilk\s+tooth\b", r"\bbaby\s+tooth\b", r"\bloose\s+tooth\b", r"\btoothache\b",
    r"\b(?:last|this)\s+(?:year|month|week)\b", r"\byears?\s+ago\b", r"\bwobbly\b",
)
TOOTH_CHILD = (r"\b(?:son|daughter|kid|child|children|baby|toddler|girl|boy|she|he|his|her)\b",)
TOOTH_KNOCK = (r"\b(?:knocked|broke|busted|smashed|snapped)\b",)

HEAD_FALL = (
    r"\b(?:fell|fallen|fall|falls|collapsed|went\s+down|slipped|tripped)\b",
)
CONFUSED_SIGN = (
    r"confus(?:ed|ion)\b(?!\s+(?:why|what|whether|if)\b)"
    r"(?!\s+(?:about|by|at|as\s+to)\s+(?!where\b|who\b|whereabouts\b))"
)
HEAD_FALL_SIGN = (
    r"\b(?:he|she|they|hes|shes|theyre|dad|mum|grandad|grandma|nan|gran|husband|wife|father|mother)\b.{0,40}"
    r"\b(?:" + CONFUSED_SIGN + r"|drowsy|sleepy|"
    r"(?:isn'?t|isnt|not|wasn'?t|ain'?t)\s+making\s+(?:any\s+)?sense|"
    r"(?:doesn'?t|doesnt|didn'?t|didnt)\s+know\s+(?:where\s+(?:he|she|they)\s+(?:is|are|was|were)|"
    r"who\s+(?:i|we|he|she|they)\s+(?:am|are|is|was))\b|acting\s+(?:strange|odd|weird|differently)|"
    r"(?:isn'?t|isnt|not|wasn'?t|ain'?t|hasn'?t|hadn'?t)\s+(?:been\s+)?(?:him|her|them)sel(?:f|ves)|"
    r"talking\s+(?:rubbish|nonsense|gibberish)|"
    r"can'?t\s+wake|knocked\s+out|unconscious)\b",
    r"\bconfused\b(?!\s+about)\b.{0,20}\b(?:after|since)\b.{0,20}\b(?:fell|fall|bang|knock)\b",
    r"\b(?:i|im|i'?m|ive|i'?ve)\b.{0,45}\b" + CONFUSED_SIGN + r"",
)
FALL_ASLEEP = (
    r"\bf(?:ell|alls?|alling)\s+asleep\b",
)
CONFUSION_NAMED_CAUSE = (
    r"\b(?:was|were|is|been)\s+confused\s+(?:after|since|following)\s+"
    r"(?:his|her|their|the)\s+(?:stroke|surgery|operation|anaesthetic|chemo|accident)\b",
)
FALL_THING = (
    r"\b(?:prices?|markets?|shares?|stocks?|temperature|rain|snow|sales|rates?|figures?|numbers?|"
    r"pounds?|euros?|dollars?|hair|wigs?|leaves)\s+(?:keeps?\s+|kept\s+|is\s+|are\s+|was\s+|were\s+|"
    r"had\s+|has\s+|have\s+)?(?:falling|fell|falls?|dropping|dropped)\b",
)
HEAD_SEEN = (
    r"\b(?:in|at)\s+(?:the\s+)?(?:hospital|a&e|ae|er|casualty)\b", r"\bbeen\s+checked\b",
    r"\b(?:doctor|nurse|paramedic|ambulance)\s+(?:has\s+)?(?:seen|checked|said|looked)\b",
    r"\bwalk-in\s+(?:centre|clinic)\b", r"\bthey\s+(?:kept|are\s+keeping)\b.{0,15}\bin\b",
)
HEAD_PAST = (r"\b(?:last|this)\s+(?:year|month|week|night)\b", r"\byears?\s+ago\b",
             r"\bages\s+ago\b", r"\bused\s+to\b", r"\bwhen\s+i\s+was\s+(?:a\s+)?(?:kid|child|little)\b")
PET_RESPOND = r"\b(?:not|isn'?t|stopped|won'?t|wont)\s+respond(?:s|ing|ed)?(?![a-z])" + PET_RESPOND_AT
PET_COLLAPSE = (
    PET_UNRESPONSIVE,
    PET_RESPOND,
    r"\b(?:not|isn'?t|hasn'?t|has\s+not)\s+mov\w*|\bnot\s+moving\b",
    r"\b(?:is|are|was|were|went|gone|being|looks?|seems?)\s+(?:a\s+bit\s+|really\s+|very\s+|"
    r"totally\s+|completely\s+)?limp\b",
)
PET_BEHAVIOUR = (
    PET_UNRESPONSIVE,
    PET_RESPOND,
    r"\b(?:not|isn'?t|hasn'?t|has\s+not|not\s+moving)\b\s*\w*\bmov\w*|\bnot\s+moving\b",
)
PET_FIT = (
    r"\b(?:having|had|has|in)\s+(?:a\s+)?fits?\b", r"\bfitting(?!\s+in)\b", r"\bseizure\b",
    r"\bflopp\w*\b", r"\bnot\s+moving\b",
)
PET_CRISIS = (
    r"\bchok\w*\b", r"\b(?:can'?t|cannot|unable\s+to|struggling\s+to|not)\s+breathe?\b",
    r"\b(?:isn'?t|is\s+not|not|stopped)\s+breathing\b", r"\btrouble\s+breathing\b",
    r"\bshort(?:ness)?\s+of\s+breath\b",
    r"\bgasp\w*\s+for\s+(?:air|breath|it)\b",
    r"\bbreath\w*\s+(?:funny|odd|oddly|strange|strangely|weird|weirdly|noisily|loudly|"
    r"differently)\b",
    r"\bbleeding\b", r"\bhit\s+by\s+(?:a\s+)?(?:car|bike|van|bus|train|lorry|truck)\b",
    r"\brun\s+over\b", r"\b(?:car|van|bus|bike|lorry|truck)\s+(?:clipped|knocked|caught|hit|struck)\b",
    r"\bseizure\b", r"\bfitting\b", r"\b(?:having|had|has|in)\s+(?:a\s+)?fits?\b",
    r"\b(?:went|gone|is|was|being)\s+floppy\b", r"\bunconscious\b", r"\b(?:has\s+)?collapsed\b",
    r"\b(?:is|are|was|were|went|gone|being|looks?|seems?)\s+(?:a\s+bit\s+|really\s+|very\s+|"
    r"totally\s+|completely\s+)?limp\b",
    r"\b(?:not|isn'?t)\s+moving\b", PET_UNRESPONSIVE,
    r"\b(?:won'?t|wont|can'?t|cannot|unable\s+to|isn'?t|not)\s+wak\w*(?!\s+(?:me|us|you|him|them)\b)",
    r"\b(?:be\s+)?woken\b",
    PET_RESPOND,
    r"\b(?:hasn'?t|has\s+not|not)\s+mov\w*\b",
    r"\b(?:fell|fallen|jumped)\s+(?:off|from|down)\b", r"\bwon'?t\s+wake\b", r"\bwont\s+wake\b",
    r"\b(?:ate|eaten|eats|drank|drunk|swallow\w*|licked|lick\w*|chew\w*|bit|bitten)\b"
    r".{0,35}\b(?:antifreeze|poison\w*|"
    r"xylitol|lil(?:y|ies)|ibuprofen|paracetamol|"
    r"painkillers?|rat\s+bait|slug\s+pellets?|bleach|a\s+bone|a\s+sock|a\s+stick|"
    r"toilet\s+cleaner|oven\s+cleaner|washing\s+powder|nail\s+varnish|de-?icer|screen\s?wash|"
    r"drain\s+cleaner|fabric\s+softener|dishwasher\s+salt|"
    r"something\s+(?:bad|poisonous|sharp)|batter(?:y|ies)|coins?|magnet\w*|string|tinsel|"
    r"a\s+toy|plastic|a\s+stone|a\s+pebble)\b",
    r"\b(?:rabbits?|bunn(?:y|ies)|guinea\s+pigs?)\b.{0,30}\b(?:stopped|not|isn'?t|hasn'?t)\s+"
    r"(?:eating|eaten)\b",
)
CHOKE_HABIT = (
    r"\b(?:used\s+to|always|never|often|keeps?|kept|every\s+time|when\s+(?:he|she|they)\s+"
    r"(?:was|were)\s+(?:a\s+)?(?:baby|little|small|young|kid|child))\s+chok",
)
BREATH_OVER = (
    r"\b(?:fine|ok|okay|alright|better)\s+(?:now|again)\b",
    r"\b(?:it|that)\s+(?:has\s+)?passed\b", r"\bpassed\s+now\b", r"\bwent\s+away\b",
    r"\b(?:it|that)\s+(?:is\s+|has\s+)?(?:over|gone)\b",
)
NIGHT_OCCASION = (r"(?:last\s+night|overnight|in\s+the\s+night|at\s+night|during\s+the\s+night|"
                  r"middle\s+of\s+the\s+night|in\s+bed|in\s+my\s+sleep|in\s+his\s+sleep|"
                  r"in\s+her\s+sleep)")
NIGHT_BREATH = (
    r"\b" + NIGHT_OCCASION + r"\b[^.?!]{0,60}\b(?:breath\w*|gasp\w*)\b",
    r"\b(?:breath\w*|gasp\w*)\b[^.?!]{0,60}\b" + NIGHT_OCCASION + r"\b",
    r"\b(?:wake|wakes|waking)\s+up\b[^.?!]{0,40}\b(?:breath\w*|gasp\w*)\b",
    NIGHT_BREATH_PAST[0],
    r"\b(?:breath\w*|gasp\w*)\b[^.?!]{0,30}\b(?:when|whenever)\s+i\s+(?:wake|wakes)\b",
    r"\b(?:lying|lie|lies|lay|laid)\s+(?:flat|down)\b[^.?!]{0,40}\b(?:breath\w*|gasp\w*)\b",
    r"\b(?:breath\w*|gasp\w*)\b[^.?!]{0,40}\b(?:lying|lie|lies)\s+(?:flat|down)\b",
    r"\bpropped\s+up\b[^.?!]{0,40}\b(?:breath\w*|gasp\w*)\b",
    r"\b(?:breath\w*|gasp\w*)\b[^.?!]{0,40}\bpropped\s+up\b",
    r"\bsleep(?:ing)?\s+(?:sitting\s+up|upright|propped)\b",
)
NIGHT_BREATH_DREAM = (
    r"\b(?:nightmare|nightmares|bad\s+dream|bad\s+dreams|dream|dreams|dreaming|dreamt|dreamed)\b",
)
NIGHT_BREATH_CHILD = (
    r"\b(?:my|our|his|her|their|the)\s+(?:baby|babies|son|sons|daughter|daughters|child|"
    r"children|kid|kids|toddler|toddlers|infant|infants|boy|girl|newborn|little\s+one)s?\b",
)
BREATH_STILL_RED = (
    r"\b(?:can'?t|cannot|can\s+not|unable\s+to)\s+(?:breathe|breath)\b",
    r"\b(?:stopped\s+breathing|isn'?t\s+breathing|not\s+breathing|gasping)\b",
)
CHOKE_NOW = (
    r"\b(?:still|right\s+now|now|can'?t\s+breathe|cannot\s+breathe|struggling|gasping|coughing|"
    r"went\s+blue|turned\s+blue|in\s+a\s+lot\s+of\s+pain|hurts)\b",
)
CHOKE_HELP = (
    r"\bchok(?:ing|ed|es)\b(?!\s+(?:me|up)\b)", r"\bchocking\b",
)
CHOKE_BABY = (
    r"\b(?:baby|babies|infant|newborn|new\s?born|babe\s+in\s+arms)\b",
    r"\b(?:under\s+(?:one|1|a\s+year)|(?:\d|one|two|three|four|five|six|seven|eight|nine|ten|"
    r"eleven)\s+months?\s+old)\b",
)
LIMP_STATE = r"(?:gone|is|was|went|being|felt|feels?|all)\s+limp\b"
FLOPPY_CHILD = (
    r"\b(?:baby|babies|toddler|newborn|infant|child|kid|son|daughter|boy|girl|she|he|they|"
    r"shes|hes|theyre|my\s+" + PERSON + r")\b"
    r".{0,40}\b(?:flopp\w*|life-?less)\b",
    r"\b(?:baby|babies|toddler|newborn|infant|child|kid|son|daughter|boy|girl|she|he|they|"
    r"shes|hes|theyre|my\s+" + PERSON + r")\b"
    r".{0,40}" + LIMP_STATE,
    r"\b(?:baby|babies|toddler|newborn|infant|child|kid|son|daughter|boy|girl)\b"
    r".{0,40}\bunresponsive\b(?!\s*(?:to|when|whenever|if|because|as|after|with)\b)",
    r"\b(?:baby|babies|toddler|newborn|infant|child|kid|son|daughter|boy|girl)\b"
    r".{0,40}\bunresponsive\b\s*(?:to|after|during|at|following)\s+(?:the|a|an|her|his|my|"
    r"their|this|that|some)?\s*(?:(?:new|old)\s+)?(?:milk|formula|feeds?|feeding|bottle|breast|"
    r"solids|weaning)\b",
    r"\b(?:flopp\w*|life-?less)\b.{0,40}\b(?:baby|babies|toddler|newborn|infant|child|kid|"
    r"son|daughter|boy|girl)\b",
    r"\b(?:baby|babies|toddler|newborn|infant)\b.{0,40}\b(?:too\s+sleepy|very\s+sleepy|won'?t\s+wake|"
    r"wont\s+wake|hard\s+to\s+wake|not\s+waking|can'?t\s+wake|drowsy|sleepy)\b.{0,40}"
    r"\b(?:feed\w*|eating|eaten|drink\w*|napp(?:y|ies)|wet\s+nappy|wake\s+for\s+a\s+feed)\b",
)
EXERTION_CHEST = (r"\b(?:tight\w*|pressure|heavy|heaviness|ache|aching)\b",)
_CHEST_OTHER_RED = (
    r"\b(?:arm|jaw|shoulder|neck|sweat\w*|clammy|grey|gray|pale|numb|numbness|tingl\w*|crushing|"
    r"squeez\w*|can't\s+breathe|breathless\w*|short(?:ness)?\s+of\s+breath|faint\w*|"
    r"pass(?:ed)?\s+out|sick|vomit\w*|dizzy)\b",
)


YOUNG_PERSON = (r"(?:teen|teenager|adolescent|child|kid|toddler|baby|pre-?schooler|schoolkid|"
                r"schoolboy|schoolgirl|boy|girl|lad|lass|youngster|nephew|niece|"
                r"cousin|grandson|granda?ughter|stepson|stepdaughter|" + PERSON + r")")
OTHER_SUBJECT = (r"(?:he|hes|she|shes|they|(?:my|our|the)\s+(?:\d{1,2}[\s-]?year[\s-]?old|" + YOUNG_PERSON + r"))")
SELF_HARM_BY_OTHER = (
    r"\b" + OTHER_SUBJECT + r"\b.{0,25}"
    r"\b(?:cuts?|cutting|burns?|burning|hurts?|hurting|harms?|harming|scratches?|scratching|"
    r"starves?|starving)\s+(?:him|her|them)sel(?:f|ves)\b",
    r"\b" + OTHER_SUBJECT + r"\b.{0,25}"
    r"\b(?:is|are|was|were|keeps?|kept|been)\s+(?:cutting|burning|hurting|harming|scratching)\b"
    r".{0,15}\b(?:again|himself|herself|themselves|at\s+night|every\s+day)\b",
    r"\b(?:my|our|the)\s+(?:\d{1,2}[\s-]?year[\s-]?old|" + YOUNG_PERSON + r")\b.{0,20}"
    r"\b(?:cuts?|cutting|burns?|burning|scratches?|scratching)\b.{0,10}\b(?:again|a\s+lot)\b",
    r"\b" + OTHER_SUBJECT + r"\b.{0,30}"
    r"\b(?:talks?|talking|talked|says?|saying|said|mentions?|mentioning|mentioned|jokes?|joking|"
    r"threatens?|threatening|keeps?|kept|sent|texted|messaged|wrote|posted|shared)\b"
    r".{0,20}\b(?:about|of|that)\b.{0,20}"
    r"\b(?:killing|hurting|cutting|harming|topping|ending|taking)\b.{0,15}"
    r"\b(?:(?:him|her|them)sel(?:f|ves)|(?:his|her|their)\s+(?:own\s+)?life|"
    r"it(?:\s+all)?(?!\s+with\s+(?:him|her|them|us|my|his|their|the)))\b",
    r"\b" + OTHER_SUBJECT + r"\b[^.?!]{0,25}"
    r"\b(?:feels?|felt|feeling)\s+(?:like\s+)?(?:ending\s+(?:it(?!\s+with\s+(?:him|her|them|us|my|"
    r"his|their|the))|(?:his|her|their)\s+life)|killing\s+(?:him|her|them)sel(?:f|ves)|"
    r"dying(?!\s+(?:of|laughing|with\s+laughter|(?:my|his|her|their)\s+hair)))\b",
    r"\b" + OTHER_SUBJECT + r"\b[^.?!]{0,25}"
    r"\b(?:wants?|wanted|wanting|plans?|planning)\s+to\s+(?:die(?!\s+(?:of|laughing|with\s+"
    r"laughter|(?:my|his|her|their)\s+hair))|end\s+(?:it(?!\s+with\s+(?:him|her|them|us|my|his|their|the))|"
    r"(?:his|her|their)\s+life)|kill\s+(?:him|her|them)sel(?:f|ves))\b",
    r"\b" + OTHER_SUBJECT + r"\b.{0,30}"
    r"\b(?:talks?|talking|talked|says?|saying|said|mentions?|mentioning|mentioned|jokes?|joking|"
    r"threatens?|threatening|keeps?|kept|sent|texted|messaged|wrote|posted|shared)\b"
    r".{0,20}(?:(?:about|of|that)\b.{0,20})?(?:suicide|suicidal)\b",
    r"\b" + OTHER_SUBJECT + r"\b.{0,30}"
    r"\b(?:said|says|saying|told\s+me|tells\s+me|keeps\s+saying|kept\s+saying|texted|"
    r"messaged|wrote|mention(?:s|ed|ing)?|posted)\b.{0,25}"
    r"\b(?:end(?:ing)?\s+it(?:\s+all)?(?!\s+with\s+(?:him|her|them|us|my|his|their|the))|"
    r"tak(?:e|es|ing|en)\s+(?:his|her|their)\s+(?:own\s+)?life|"
    r"kill(?:ing)?\s+(?:him|her|them)sel(?:f|ves)|"
    r"top(?:s|ping|ped)?\s+(?:him|her|them)sel(?:f|ves)|off(?:s|ed|ing)?\s+(?:him|her|them)sel(?:f|ves)|"
    r"suicid\w+)\b",
)
SELF_HARM_BY_OTHER = (*SELF_HARM_BY_OTHER,
    r"\b" + OTHER_SUBJECT + r"\b[^.?!]{0,25}\bself[-\s]?harm(?:s|ing|ed)?\b",
    r"\b" + OTHER_SUBJECT + r"\b[^.?!]{0,25}\bwish(?:es)?\s+(?:he|she|they)\s+"
    r"(?:was|were|is|are)\s+(?:dead|gone)\b",
    r"\b" + OTHER_SUBJECT + r"\b[^.?!]{0,30}\b(?:shoot|shooting|hang|hanging|stab|stabbing|"
    r"poison|poisoning|drown|drowning|strangle|strangling|overdose|overdosing)\s+"
    r"(?:him|her|them)sel(?:f|ves)\b",
    r"\b" + OTHER_SUBJECT + r"\b[^.?!]{0,30}\b(?:throw|throwing|jump|jumping|step|stepping|"
    r"walk|walking)\s+(?:him|her|them)sel(?:f|ves)\s+"
    r"(?:in\s+front\s+of|under|onto|off)\s+(?:a|an|the)?\s*(?:train|trains|bus|buses|lorry|"
    r"truck|coach|traffic|platform|tracks?|rails?|bridge|roof|building|cliff|balcony|ledge)\b",
)
HURT_HIMSELF_BARE = (
    r"\b" + OTHER_SUBJECT + r"\b.{0,25}\b(?:hurt|hurts|hurting)\s+(?:him|her|them)sel(?:f|ves)\b",
)
HURT_HIMSELF_MEANT = (
    r"\b(?:on\s+purpose|again|keeps?|kept|every\s+day|every\s+night|at\s+night|"
    r"when\s+(?:he|she|they)\b|because\b|upset|anxious|depressed|angry|wants?\s+to\s+die|"
    r"wish\w*\s+(?:he|she|they)|suicid\w*|kill|ended?\s+up\s+in|hospital|a\s+and\s+e|"
    r"a&e)\b",
)
A_PORTION = (
    r"(?:slice|slices|piece|pieces|bit|bits|portion|portions|helping|helpings|serving|servings|"
    r"wedge|wedges|chunk|chunks|plate|plateful|bowl|bowlful|glass|cup|mug|half|hunk|knob|spoon|"
    r"spoonful|handful|bite)\b")
A_HARM_VERB_CUT = (
    r"\b(?:cuts?|cutting|cut|slices?|slicing|sliced|burns?|burning|burned|burnt|scratches?|"
    r"scratching|scratched|carves?|carving|carved|engraves?)\b")
ORDINARY_REFLEXIVE = (
    r"\b(?:cuts?|cutting|slices?|slicing|burns?|burning|burned|burnt|starves?|starving|starved)\s+"
    r"(?:my\s*self|himself|herself|themselves)\s+"
    r"(?![^.?!]{0,24}\b(?:gash|wound|scar|cut|blade|razor|burn\s*mark|bruise)\b)"
    r"(?![^.?!]{0,40}\b(?:on\s+purpose|deliberately|on\s+purposely)\b)"
    r"(?:a|an|the|another|one|two|three|half)\s+(?:\w+\s+){0,1}" + A_PORTION
    + r"(?!\s*(?:[.?!,;]|$))",
    r"\b(?:cuts?|cutting|slices?|slicing|burns?|burning|starves?|starving)\s+"
    r"(?:my\s*self|himself|herself|themselves)\s+some\s+\w+",
    r"\b(?:helps?|helped|helping|pours?|poured|pouring|serves?|served|serving|grabs?|grabbed|"
    r"grabbing|treats?|treated|treating|makes?|made|making)\s+"
    r"(?:my\s*self|himself|herself|themselves)\s+"
    r"(?:(?:a|an|the|some|another)\s+\w+|to\b)",
    r"\b(?:starves?|starving|starved)\s+(?:my\s*self|himself|herself|themselves)\s+"
    r"(?:all\s+day|all\s+week|for\s+days|until\b|then\b)[^.?!]{0,30}"
    r"\b(?:eats?|eating|ate|dinner|lunch|breakfast|meal)\b",
)


AN_ACT_BESIDE_THE_ITCH = (
    r"\b(?:cut|cuts|cutting|cut\s+himself|cut\s+herself|slit\w*|slashed|blade|razor|knife|"
    r"scalpel|stanley\s+knife|glass|broken\s+glass|burn\w*|scald\w*|burnt)\b",
    r"\b(?:pills?|tablets?|paracetamol|ibuprofen|overdose[ds]?|od|poison\w*|bleach|"
    r"kill\w*|die|dying|suicide|end\s+it|end\s+my\s+life|hang\w*|noose|rope)\b",
    r"\b(?:self[\s-]?harm\w*|hurting\s+himself|hurting\s+herself|hurting\s+themselves|"
    r"on\s+purpose)\b",
)


def _a_reason_it_was_not_meant(text):
    return ((_matches(SELF_HARM_LOOKALIKE, text) and not _matches(A_WISH_OR_TALK_OF_IT, text))
            or (_matches(AN_ITCH_LOOKALIKE, text)
                and not _matches(A_WISH_OR_TALK_OF_IT, text)
                and not _matches(AN_ACT_BESIDE_THE_ITCH, text))
            or _an_ordinary_helping(text))


A_REAL_INJURY = (
    r"\b(?:bleed\w*|blood|bloody|stitches?|gash\w*|deep\s+cut)\b",
    r"\b(?:cut|cuts|cutting|sliced|slices|slicing|nicked|nicks|grazed|caught)\b[^.?!]{0,20}?"
    r"\b(?:thumb|finger|fingers|hand|hands|palm|knuckle|knuckles|nail|fingertips?)\b",
)


A_PLATE_SHAPE = (
    r"\b(?:cuts?|cutting|slices?|slicing|burns?|burning|burned|burnt)\s+"
    r"(?:my\s*self|himself|herself|themselves)\s+"
    r"(?:a|an|the|another|one|two|three|half)\s+(?:\w+\s+){0,1}" + A_PORTION,
    r"\b(?:cuts?|cutting|slices?|slicing|burns?|burning)\s+"
    r"(?:my\s*self|himself|herself|themselves)\s+some\s+\w+",
)


def _a_real_injury_beside_the_plate(text):
    return (_matches(A_REAL_INJURY, text)
            and _matches(A_PLATE_SHAPE, text)
            and not _matches(A_WISH_OR_TALK_OF_IT, text)
            and not _matches(DISTRESS_BESIDE_IT, text)
            and not _matches(BLEEDING + CUT_NOT_STOPPING, text))


UNWELL_BESIDE_THE_PLATE = (
    r"\b(?:feel|feels|felt|feeling)\s+(?:faint|dizzy|light.?headed|sick|ill|weak|shaky|unwell|"
    r"nauseous|queasy)\b",
    r"\b(?:fainted|passed\s+out|blacked\s+out|light.?headed|seeing\s+stars|blurred\s+vision|"
    r"went\s+white|shaking|can'?t\s+stand\s+up)\b",
)


def _an_ordinary_helping(text):
    return (_matches(ORDINARY_REFLEXIVE, text)
            and not _matches(A_WISH_OR_TALK_OF_IT, text)
            and not _matches(DISTRESS_BESIDE_IT, text)
            and not (_matches(A_BODY_PART, text) and _matches(A_HARM_VERB_CUT, text))
            and not (_matches(A_REAL_INJURY, text)
                     and not _matches(BLEEDING + CUT_NOT_STOPPING, text))
            and not _matches(UNWELL_BESIDE_THE_PLATE, text)
            and not _matches(BLEEDING + CUT_NOT_STOPPING, text))


SELF_REASSURED = (
    r"\b(?:i'?m|it'?s|im|its|he'?s|she'?s|they'?re|we'?re)\s+(?:all\s+)?(?:fine|ok|okay|grand)\b",
    r"\b(?:nothing|not)\s+(?:too\s+)?(?:serious|bad|major)\b",
)
WISH_DEAD_TAIL = (r"(?=\s*(?:$|[.!?]|any\s?more|any\s+longer|at\s+all|no\s?more|now\b|"
                  r"tonight\b|today\b))")
_SOFTENING = (r"(?:honestly|tbh|for\s+real|seriously|genuinely|no\s+joke|i\s+mean\s+it|"
              r"really|truthfully|lol)\b(?=\s*(?:$|[.!?]))")
WISH_DEAD_NO_REASON = (r"(?!\s*+,\s*+(?!any\s?more|any\s+longer|at\s+all|no\s?more|now\b|"
                       r"tonight\b|today\b|" + _SOFTENING + r"))")
WISH_DEAD = (
    r"\bi\s+wish\w*\s+i\s+(?:was|were|am)\s+(?:dead|gone|never\s+born)\b"
    r"(?!\s*(?:tired|exhausted|beat|knackered|on\s+my\s+feet|serious|funny|lucky|happy|"
    r"to\s+the\s+world|as\s+\w+|set\b|sure\b|honest\b|certain\b|"
    r"centre|center|to\s+rights|weight\b|fishing\b|in\s+the\s+water|"
    r"last\b(?!\s*(?:night|nights|week|weeks|month|months|year|years|time|times|summer|winter|"
    r"spring|autumn|christmas|new\s+year|monday|tuesday|wednesday|thursday|friday|saturday|"
    r"sunday))|"
    r"first\b(?=\s*(?:place|in\s+the\s+race|past\s+the\s+post|over\s+the\s+line))|"
    r"by\s+(?:\d|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|noon|midday|"
    r"half)\b))" + WISH_DEAD_NO_REASON,
    r"\bi\s+wish\w*\s+i\s+(?:wasnt|wasn'?t|was\s+not|didnt|didn'?t|did\s+not|never|"
    r"could(?:nt|n'?t|\s+not)?|would(?:nt|n'?t|\s+not)?)\b[^.?!]{0,20}"
    r"\b(?:dead|die|dying|gone|disappear|vanish|not\s+here|exist|born|wake\s+up)\b"
    + WISH_DEAD_NO_REASON,
    r"\bi\s+wish\w*\s+i\s+(?:wasnt|wasn'?t|was\s+not)\s+(?:here|around|alive)\b"
    + WISH_DEAD_TAIL,
    r"\bi\s+wish\w*\s+(?:i\s+)?(?:to\s+die|to\s+be\s+dead|i\s+could\s+just\s+die)\b",
    r"\bi\s+wish\w*\s+(?:i'?d\s+|i\s+had\s+|id\s+|had\s+)?never\s+(?:been\s+)?born\b"
    + WISH_DEAD_NO_REASON,
    r"\bi\s+wish\w*\s+(?:i\s+)?(?:hadnt|hadn'?t|had\s+not|wasnt|wasn'?t|was\s+not|aint)"
    r"\s+(?:ever\s+)?(?:been\s+)?born\b"
    + WISH_DEAD_NO_REASON,
    r"\b(?:i\s+(?:keep|keeps|kept|was\s+always|am\s+always)|i'?ve\s+been|ive\s+been)\s+wish\w*\b"
    r"[^.?!]{0,20}\b(?:dead|die|dying|gone|not\s+here|never\s+(?:been\s+)?born|disappear)\b"
    + _CLAUSE_OR_END + WISH_DEAD_NO_REASON,
)
SELF_HARM_INTENT = (*SELF_HARM_INTENT, *WISH_DEAD, *SELF_HARM_CUT_NO_OBJECT)
WISH_DEAD_OFF = (*WISH_DEAD_HYPERBOLE, *WISH_DEAD_PLACE)
OWN_WISH = (*OWN_WISH, *WISH_DEAD, *WISH_BE_DEAD)
FIRST_PERSON_WISH = (
    r"\bi\b.{0,20}\b(?:want|wanna|wish|might|rather|going|plan|feel\s+like|thinking\s+of)\b"
    r".{0,12}\b(?:to\s+)?(?:die|dying|kill\s+my\s*self|end\s+it|not\s+be\s+here|be\s+dead)\b",
    *WISH_DEAD,
)
_LEARN_PLACE = (r"(?:class|classes|lesson|lessons|assembly|school|college|uni|university|lecture|"
                r"seminar|workshop|training|course|pshe|homework|essay|exam)")
_MEDIA_WORD = (r"(?:film|films|movie|documentary|programme|program|show|series|episode|book|novel|"
               r"article|paper|podcast|news|telly|radio|play|song|headline|headlines|chapter|"
               r"thriller|true\s+crime|tv|netflix|tiktok|reddit|forum|subreddit|thread)")
_WORD_ITSELF = r"(?:suicide|suicidal|self[-\s]?harm)"
SUICIDE_MENTION_CONTEXT = (
    r"\b" + _WORD_ITSELF + r"\b.{0,40}\b(?:in|during|at|for)\s+(?:a|an|the|our|my|his|her)?\s*"
    + _LEARN_PLACE + r"\b",
    r"\b(?:in|during|at|for)\s+(?:a|an|the|our|my|his|her)?\s*" + _LEARN_PLACE + r"\b"
    r".{0,40}\b" + _WORD_ITSELF + r"\b",
    r"\b" + _MEDIA_WORD + r"\b.{0,40}\b" + _WORD_ITSELF + r"\b",
    r"\b" + _WORD_ITSELF + r"\b.{0,40}\b" + _MEDIA_WORD + r"\b",
    r"\b(?:we|they|the\s+class)\s+(?:talked|talk|discussed|covered|learned|learnt|studied|"
    r"read|watched)\s+(?:about\s+)?" + _WORD_ITSELF + r"\b",
)
SUICIDE_LESSON = (
    r"\b(?:teacher|tutors?|lecturers?|professors?|head\s*teacher|class|lesson|assembly|course|"
    r"workshop|training|pshe|seminars?|lectures?)\b[^.?!]{0,30}\b(?:talked|talk|talks|"
    r"discussed|discusses|taught|teaches|covering|covered|read|reads|watched|watches|mentioned|"
    r"mentions|went\s+over)\b[^.?!]{0,20}\b" + _WORD_ITSELF + r"\b",
    r"\b(?:lesson|class|assembly|seminar|lecture|workshop|pshe|session|course|module|unit|"
    r"training|talk|chat)\b[^.?!]{0,20}\b(?:on|about)\s+" + _WORD_ITSELF + r"\b",
    r"\b" + _WORD_ITSELF + r"\b\s+came\s+up\b",
    r"\b" + _WORD_ITSELF + r"\b[^.?!]{0,30}\b(?:in|at|during)\s+(?:the\s+|our\s+|her\s+|his\s+)?"
    r"(?:lesson|class|assembly|lecture|seminar|course|workshop|pshe|training)\b",
)
END_IT_ALL_JOKE = (
    r"\b(?:let'?s|let\s+us)\s+end\s+it\s+all\s+and\s+go\b",
    r"\bend\s+it\s+all\s+and\s+go\b",
)


def _rest_of_it(line):
    rest = re.sub(_LAUGH_KILL, " ", line)
    rest = EFFORT_AFTER.sub(" ", rest)
    for pattern in DIE_OF_THE_FEELING:
        rest = re.sub(pattern, " ", rest)
    for pattern in PAST_WISH_NOT:
        rest = re.sub(pattern, " ", rest)
    return re.sub(r"\b(?:feel|feels|feeling|felt)\s+like\b", " ", rest)


def _rings(text):
    return _matches(WISH_NAMED + WISH_INTENT + SELF_HARM_INTENT + FIRST_PERSON_WISH + DESPAIR
                    + NOT_JUST_A_NEAR_THING, text)


def _rest_of_it_rings(line):
    rest = _rest_of_it(line)
    if " ".join(rest.split()) == " ".join(line.split()):
        return False
    return _rings(rest)

DEATH_IN_THE_LINE = (
    r"\b(?:died|dying|death|funeral|burial|cremation|buried|passed\s+away|widow\w*|"
    r"widower|miscarriage|stillborn|cemetery|graveside|mourning|the\s+wake)\b",
)

_LAUGH_KILL = (r"(?:\b(?:was|were|am|is|are|been|kept|got)\s+killing"
               r"|\b(?:nearly|almost)\s+killed"
               r"|\b(?:kill|killing|killed))"
               r"\s+my\s*self\s+(?:laughing|with\s+laughter)\b")
IDIOM = (
    r"\b(?:killing|kills|killed)\s+me\b" + WISH_LATER,
    r"\bdies?\s+(?:to|for)\b" + WISH_LATER,
    r"\bdying\s+(?:to|for)\b" + WISH_LATER,
    r"\b(?:dead|dying)\s+(?:tired|bored|hungry|of\s+embarrassment)\b" + WISH_LATER,
    r"\b(?:could|would|might)\s+die\b" + WISH_LATER,
    r"\bcould\s+kill\s+my\s*self\s+(?:laughing|with\s+laughter|try\w*)\b" + WISH_LATER,
    r"\bkilling\s+my\s*self\s+(?:laughing|with\s+laughter)\b" + WISH_LATER,
    r"\b(?:i'?d|i\s+would|could|would|might)(?:\s+(?:just|honestly|literally|easily|quite|"
    r"really|so|totally|actually|probably|almost|nearly|bloody|still))?\s*kill\s+my\s*self\s+"
    r"(?:for|over|about)\s+(?!real\b|good\b|sure\b|definite\b|keeps?\b|ever\b)"
    r"(?=[^.!?]{0,24}\b(?:forgetting|forgot|losing|lost|missing|missed|dropping|dropped|"
    r"breaking|broke|spilling|spilt|spilled|deleting|deleted|sending|sent|booking|booked|"
    r"clicking|clicked|typing|typed|mixing|saying|said|"
    r"being\s+(?:so\s+|really\s+|a\s+bit\s+|very\s+|that\s+)?(?:late|lazy|slow|silly|"
    r"forgetful|clumsy|early|on\s+time)|that\b|this\b))"
    r"(?![^.!?]{0,24}\b(?:job|baby|pregnan\w*|mum|mom|dad|wife|husband|partner|marriage|"
    r"son|daughter|child|house|home|fiance\w*|said\s+to\s+(?:her|him|them|you|someone|"
    r"everyone|anyone|everybody))\b)" + WISH_LATER,
    _LAUGH_KILL + WISH_LATER,
    r"\b(?:dye|dyed|die|dying)\s+(?:my|his|her|their|its)\s+hair\b" + WISH_LATER,
    r"\b(?:this|that|it)\s+(?:is|'s)\s+killing\s+me\b" + WISH_LATER,
    r"\bdying\s+of\s+(?:laughter|curiosity|hunger|thirst)\b" + WISH_LATER,
    r"\b(?:dying|died|die)\s+(?:laughing|with\s+laughter)\b" + WISH_LATER,
    r"\b(?:going\s+to|gonna|will|would|could|might|about\s+to)\s+die\s+"
    r"(?:laughing|of\s+(?:laughter|boredom|embarrassment|shame|curiosity|hunger|thirst|"
    r"tiredness|excitement|joy))\b" + WISH_LATER,
    r"\b(?:die|dying|died)\s+of\s+(?:boredom|embarrassment|shame|excitement)\b" + WISH_LATER,
    r"\b(?:kill|killing)\s+time\b", r"\bstarving\s+(?:for|of)\b",
)
FIRST_PERSON = (r"\bi\b", r"\bi'?m\b", r"\bi'?ve\b", r"\bme\b", r"\bmyself\b", r"\bmy\s+own\b")
PAST_HARM = (
    r"\b(?:broke|broken|fractured|dislocated|sprained)\b.{0,30}\b(?:when\s+i\s+was|years?\s+ago|"
    r"as\s+a\s+(?:kid|child|boy|girl)|last\s+(?:year|summer|winter|month|week)|ages\s+ago)\b",
)
URGENT_NOW = (
    r"\b(?:now|right\s+now|today|tonight|just|suddenly|this\s+(?:morning|evening|afternoon|"
    r"moment))\b",
)


LEAP_OFF_A_DROP = (
    r"(?:\bi\b[^.?!]{0,15}\bjumped\b(?![^.?!]*\binto\s+(?:the\s+|a\s+)?(?:river|water|sea|"
    r"lake|canal|reservoir|pool)\b)|\bthrew\s+my\s*self\b)[^.?!]{0,12}\b(?:off|from)\s+"
    r"(?:a\s+|the\s+)?(?:bridge|roof|building|cliff|car\s*park|balcony)\b"
)
TEEN_AGE = (
    r"\b(?:when|since)\s+i\s+was\s+(?:a\s+)?(?:teenager|teen|in\s+my\s+teens)\b",
    r"\b(?:as|like)\s+a\s+teenager\b", r"\bin\s+my\s+teens\b", r"\bgrowing\s+up\b",
    r"\bwhen\s+i\s+was\s+(?:in\s+my\s+)?(?:twenties|thirties|forties|fifties)\b",
)

PAST_ATTEMPT = (
    r"\b(?:nearly|almost)\s+(?:ended|did)\s+it\b",
    r"\b(?:nearly|almost)\s+(?:took|ended)\s+my\s+(?:own\s+)?life\b",
    r"\b(?:tried|try|tries|attempted|attempt|attempts|went\s+to)\b[^.?!]{0,25}"
    r"\b(?:kill(?:ing)?\s+(?:my|him|her|them)\s*self|end(?:ed|ing)?\s+it|end\s+my\s+life|"
    r"take\s+my\s+own\s+life|suicide|overdos\w*|hang(?:ing)?\s+(?:my|him|her|them)\s*self|"
    r"cut\s+(?:my|his|her|their)\s*wrists?|jump\s+off)\b",
    r"\b(?:took|taken|swallowed|downed|popped|necked|ate)\b[^.?!]{0,25}"
    r"\b(?:an?\s+overdose|too\s+many\s+(?:pills|tablets|paracetamol|ibuprofen|painkillers|"
    r"sleeping\s+pills|antidepressants))\b",
    r"\b(?:took|taken|swallowed|downed|popped|necked|ate)\b[^.?!]{0,25}"
    r"\b(?:a|the|what\s+was\s+left\s+of\s+(?:a|the))\s+(?:whole\s+|entire\s+|full\s+)?"
    r"(?:bunch|load|handful|packet|pack|box|strip|blister|bottle)\s+of\s+(?:(?:the|my|his|her|"
    r"their|our|some)\s+)?(?:\w+'?s\s+)?" + DRUG_NAME + r"\b",
    r"\boverdos(?:e|ed)\b",
    r"\b(?:cut|cutting|sliced|slashed|carved)\b[^.?!]{0,12}\b(?:my\s*self|(?:my|his|her|their)\s+"
    r"(?:wrists?|arms?|forearms?|upper\s+arms?|thighs?|legs?|tummy|stomach|belly|chest|shins?))\b",
    *SELF_HARM_SCARS,
    r"\b(?:hung|hanging|hanged|tied|put|got)\b[^.?!]{0,20}\b(?:rope|noose|belt|cord)\b"
    r"[^.?!]{0,20}\b(?:my\s+neck|round\s+my\s+neck|around\s+my\s+neck)\b",
    r"\b(?:held|put|pressed|pushed)\b[^.?!]{0,20}\b(?:a\s+)?(?:knife|blade|razor)\b"
    r"[^.?!]{0,20}\b(?:to|against)\s+my\s+(?:throat|neck|wrist|arm)\b",
    LEAP_OFF_A_DROP,
    r"\b(?:laid|lay|lying|sat|sitting|standing|stood|walked|stepped)\s+(?:down\s+)?(?:on|onto|"
    r"in\s+front\s+of)\s+(?:the\s+)?(?:train\s+tracks?|rail\s+tracks?|tracks?|railway|"
    r"live\s+rail)\b",
    *EDGE_OF_A_DROP,
    r"\bself[-\s]?harmed\b",
)
PAST_ATTEMPT_STRONG = (
    r"\b(?:tried|try|tries|attempted|attempt|attempts)\b[^.?!]{0,25}"
    r"\b(?:kill\s+my\s*self|end(?:ing)?\s+it|end\s+my\s+life|take\s+my\s+own\s+life|suicide)\b",
    r"\b(?:cut|cutting|sliced|slashed|carved)\b[^.?!]{0,10}\bmy\s+wrists?\b",
    r"\boverdos(?:e|ed)\b",
    r"\b(?:hung|hanging|hanged|tied|put|got)\b[^.?!]{0,20}\b(?:rope|noose|cord)\b",
    r"\b(?:knife|blade|razor)\b[^.?!]{0,20}\b(?:to|against)\s+my\s+(?:throat|neck)\b",
    LEAP_OFF_A_DROP,
    r"\b(?:laid|lay|lying|sat|sitting|standing|stood)\s+(?:down\s+)?(?:on|in\s+front\s+of)\s+"
    r"(?:the\s+)?(?:train\s+tracks?|rail\s+tracks?|tracks?|railway)\b",
    *EDGE_OF_A_DROP,
    r"\bself[-\s]?harmed\b",
    r"\b(?:cut|cutting|sliced|slashed|carved|burned|burnt|scratched)\b[^.?!]{0,25}"
    r"\b(?:on\s+purpose|deliberately|to\s+(?:hurt|punish|feel|see\s+blood|calm|cope))\b",
)
PAST_NEAR_ACT = (
    r"\bi\b[^.?!]{0,12}\b(?:nearly|almost|come\s+close\s+to|came\s+close\s+to)\b"
    r"[^.?!]{0,14}\b(?:kill(?:ed)?\s+my\s*self|hurt\s+my\s*self|cut\s+my\s*self|"
    r"did\s+something\s+stupid|end\s+it)\b",
)
EFFORT_MEANS = END_MEANS + (
    r"\btraffic\b", r"\bcliff\w*\b", r"\bplatform\b", r"\bledge\b", r"\bkerb\b",
    r"\bbridge\w*\b",
)
HARM_DOING = re.compile(
    r"^(?:cutting|burning|harming|hurting|starving|drowning|hanging|overdosing|poisoning|"
    r"slashing|scratching|swallowing|taking|drinking|suffocating|choking|strangling|hitting|"
    r"punching|banging|throwing|jumping|bleeding|punishing|self)$",
)


PLAN_FRAME_LAUGH = (
    r"\b(?:want|wanna|wanted|intend|intending|plan|planning|plan\s+to|going\s+to|gonna|might|"
    r"may|will|would|should|considering|thinking\s+about|thought\s+about)\b[^.?!]{0,18}"
    r"\b(?:kill|killing|killed)\s+my\s*self\b",
)
BARE_LAUGH = re.compile(
    r"^\W*(?:i\s+)?(?:nearly|almost|very\s+nearly)\s+(?:kill|killing|killed)\s+my\s*self\s+"
    r"(?:laughing|with\s+laughter)\W*$")


def _the_laugh(line):
    if _matches(PLAN_FRAME_LAUGH, line) or _rest_of_it_rings(line):
        return False
    if BARE_LAUGH.match(line.strip()):
        return False
    return _idiom(line) and re.search(_LAUGH_KILL, line) is not None


def _an_accident_near_thing(line):
    doing = _EFFORT_DOING.search(line)
    if not (_EFFORT_BEFORE.search(line)
            or (doing and doing.group("doing") != "laughing"
                and not HARM_DOING.match(doing.group("doing")))):
        if not _EFFORT_DIED.search(line) or not _COME_OFF_IT.search(line):
            return False
    return (not _matches(EFFORT_NOT_AN_ACCIDENT, line) and not _matches(EFFORT_MEANS, line)
            and not _rings(line) and not _rest_of_it_rings(line))


def _near_thing_key(line):
    return "near_thing_other" if _person(line) and not _matches((r"\bi\b", r"\bwe\b"),
                                                                line) else "near_thing"


def _the_effort_frame(line):
    if _an_accident_near_thing(line):
        return True
    found = EFFORT_AFTER.search(line)
    if not found:
        return False
    doing = found.group("doing")
    if doing and HARM_DOING.match(doing):
        return False
    if doing == "laughing":
        return False
    if _matches(EFFORT_MEANS, line):
        return False
    return not _rings(line) and not _rest_of_it_rings(line)


PAST_DEATH = (
    r"\b(?:died|dead|death|passed\s+away|passed\s+on|funeral|burial|cremated|cremation|"
    r"inquest|autopsy|post\s*mortem|buried)\b",
)
SELF_DEAD_FEELING = (
    r"\b(?:i\s*(?:'?m|am|feel|felt|was)\s+(?:dead|like\s+death)|dead\s+inside|"
    r"feel(?:s|ing)?\s+dead|wish\s+(?:that\s+)?i\s+(?:was|were)\s+dead)\b",
)
LONG_AGO = (
    r"\b(?:\d+\s+years?\s+ago|years?\s+ago|decades?\s+ago|when\s+i\s+was\s+\w+|"
    r"in\s+(?:19|20)\d\d)\b",
)
GAS_BURNER = r"(?:gas(?:\s+(?:cooker|oven|fire|heater|ring|hob|grill|stove))?|hob|burner|gas\s+ring|grill|stove)"
DOG_BLEED = (
    r"\b(?:bleeding|bled|blood\w*|broke\s+the\s+skin|broken\s+the\s+skin|skin\s+is\s+broken|"
    r"punctur\w*|stitches|wound|a&e|hospital|infected)\b",
)
DOG_ITCH = (
    r"\b(?:itch\w*|scratch\w*|fleas?|skin|raw\s+(?:patch|skin)|chew\w*|groom\w*|bald\s+patch|"
    r"hot\s+spot|sore\s+spot|lump)\b",
)
DOG_BIT_A_PERSON = (
    r"\b(?:me|us|someone|somebody|anybody|anyone)\b",
    r"\b(?:my|his|her|their|our)\s+(?:hand|hands|arm|arms|leg|legs|foot|feet|face|finger|"
    r"fingers|head|shoulder|shoulders|wrist|ankle|neck|cheek|nose|toe|toes|chin|back|skin)\b",
)
DOG_ATTACK_NOW = (
    r"\b(?:right\s+now|at\s+the\s+moment|this\s+minute|attacking|mauling|savaging|"
    r"has\s+hold\s+of|wont\s+let\s+go|won'?t\s+let\s+go|just\s+bit|just\s+bitten|"
    r"dragging\s+(?:me|him|her|them))\b",
)
PET_LONG_AGO = (
    r"\byears\s+ago\b", r"\bages\s+ago\b", r"\bused\s+to\b", r"\blast\s+year\b",
    r"\bwhen\s+(?:he|she|it|they)\b.{0,20}\b(?:puppy|kitten|young)\b",
    r"\bevery\s+(?:few\s+)?(?:days?|weeks?|months?|years?)\b",
    r"\bis\s+that\s+(?:normal|usual|common)\b",
)
from bot.knowledge.crisis_replies import AFTER
from bot.knowledge.crisis_replies import WAITING

SPINE_NUMB_LOWER = (
    r"\b(?:legs?|feet|foot|toes?|thighs?|calves?|saddle|between\s+my\s+legs|bladder|bowels?)\b",
    r"\b(?:can'?t|cant|cannot)\s+(?:pee|wee|urinate)\b",
    r"\bno\s+urine\b",
)
SPINE_BACK_FALL = (
    r"\b(?:fell|fall|fallen|falling|crash|accident|collision|landed|dropped|horse|bike|"
    r"bicycle|stairs|staircase|ladder|roof|scaffold|dive|dived|diving|trampoline|sledging|sking|"
    r"skiing|hit\s+by|knocked\s+over|thrown|rode\s+off)\b",
)
SPINE_BREAK_ANSWER = (
    "Ring 999 or 911 and don't move: don't sit up and don't let anyone move you. A break in the back "
    "or the neck can injure the spinal cord, and it is the moving that does the damage, so stay "
    "exactly where you are, warm and still, until the crew arrive.",
)
FIRST_FIT = ("chest", "breathing", "head_injury", "heat", "stroke", "bleeding", "poison")
ME = ((r"\bthey\b", "you"), (r"\bthem\b", "you"), (r"\btheir\b", "your"),
      (r"\btheirs\b", "yours"), (r"\bthemselves\b", "yourself"), (r"\bthey're\b", "you're"),
      (r"\bthey are\b", "you are"))


HELP_ASK_MORE = (
    r"\?", r"\b(?:what|how|should|can|could|when|else|while|wait|waiting|now|do|anything)\b",
    r"\b(?:outside|stairs|smoke|breath\w*|bleeding|burn\w*|door)\b",
)


NEXT_STEP = (
    r"\b(?:check\w*|hospital|a\s*&\s*e|a\s+and\s+e|doctor|gp|worry\w*|normal|fine|okay|serious|dangerous)\b",
)


NOT_BREATHING_NOW = (
    r"\b(?:not|isn'?t|aren'?t|wasn'?t|stopped?)\s+breathing\b", r"\bno\s+pulse\b",
    r"\b(?:stopped|stopping)\s+breathing\b",
)


BURNT_MARKS = (
    r"\b(?:clean|cleaning|scrub(?:bing)?|remove|removing|wipe|wiping|get\s+off)\b.{0,40}\b(?:worktop|worktop|hob|oven|pan|toaster|toast|carpet|grill|barbecue|bbq|saucepan|plate)\b",
    r"\b(?:burn|burned|burnt|scorch|scorched|scorch\s+marks?)\b.{0,20}\bmarks?\b",
)


WEIGHT_OLD = (
    r"\b(?:nan|nana|granny|gran|grandma|grandmother|grandad|grandpa|grandfather|elderly|"
    r"pensioner|oop|old\s+(?:man|woman|lady|boy|girl))\b",
    r"\b(?:6[5-9]|[7-9]\d|1[0-1]\d)\b",
)
WEIGHT_OLD_FALL = (r"\b(?:fell|fallen|fall|falling|slipped|tripped|collapsed|down)\b",)

LIMB_AT_AN_ANGLE = (
    r"\b(?:arm|leg|wrist|ankle|shoulder|elbow|knee)\b[^.?!]{0,25}"
    r"\b(?:bent|deformed|at\s+a\s+funny\s+angle|sticking\s+out|back\s+to\s+front)\b",
)


def _without_object_limbs(line):
    for pattern in LIMB_IS_A_THING:
        if "bent" in pattern:
            continue
        line = re.sub(pattern, " ", line, flags=re.I)
    return line


FALL = FALL_CORE + LIMB_AT_AN_ANGLE
NEAR_MISS = (
    r"\b(?:nearly|almost|near)\s+(?:fell|fallen|tripped|slipped|tumbled|went\s+over|came\s+off)\b",
    r"\bthought\s+i\s+(?:was\s+going\s+to|would)\s+fall\b",
)
NEAR_MISS_HARM = (
    r"\b(?:broke|broken|fractured|hurt|hospital|ambulance|a\s+and\s+e|a&e|stitches|"
    r"can'?t\s+(?:get|stand|move)|knocked\s+out|unconscious)\b",
)
FALL_PATTERN_HURT = (
    r"\b(?:broke|broken|fractured|bent|deformed|sticking\s+out|back\s+to\s+front|bleeding|"
    r"blood|gash|swollen|stitches|hospital|ambulance|a\s+and\s+e|a&e|unconscious|knocked\s+out)\b",
)

FALL_CHECK = (
    r"\b(?:i|we)\s+(?:just\s+)?(?:fell|fallen|slipped|tripped|went\s+over)\b",
    r"\b(?:he|she|they)\s+(?:just\s+)?(?:fell|fallen|slipped|tripped|went\s+over)\b",
    r"\b(?:my|our|the)\s+" + PERSON + r"\b[^.?!]{0,20}\b(?:fell|fallen|slipped|tripped|"
    r"went\s+over)\b",
)
FALL_NOT_BREATHING = (
    r"\b(?:not|isn'?t|isnt|aren'?t|arent|stopped|stop|stopt)\s+breathing\b",
    r"\bcan'?t\s+breathe\b", r"\bcant\s+breathe\b",
)
PET_FELL = (
    r"\b(?:dog|cat|pupp\w*|kitten|pup|pet|parrot|hamster|rabbit|bunny|horse|pony|budgie|"
    r"guinea\s+pig|tortoise|ferret|gerbil|snake|lizard|animal)\b[^.?!]{0,20}\b(?:fell|fallen|"
    r"jumped|slipped|tumbled)\b",
)

PET_SUBJECT = (
    r"\b(?:my|our|the|a)\s+(?:dog|cat|puppy|kitten|pup|pet|parrot|hamster|rabbit|bunny|horse|"
    r"pony|budgie|guinea\s+pig|tortoise|ferret|gerbil|snake|lizard)\b",
)
PET_SUBJECT_PLURAL = (
    r"\b(?:my|our|the)\s+(?:dogs|cats|puppies|kittens|rabbits|horses|ponies|pets)\b",
)
SO_I_TOO = (
    r"\b(?:so\s+(?:do|will|would|can|does)\s+i|same\s+here|me\s+too|and\s+i\s+do)\b",
)
PET_WANTS_OUT = (
    r"\b(?:my|our|the|a)\s+(?:dog|cat|puppy|kitten|pup|pet|parrot|hamster|rabbit|bunny|horse|"
    r"pony|budgie|guinea\s+pig|tortoise|ferret|gerbil|snake|lizard)\b[^.?!]{0,40}\b(?:"
    r"wants?\s+to\s+die|no\s+will\s+to\s+live|doesn'?t\s+want\s+to\s+live|"
    r"does\s+not\s+want\s+to\s+live|no\s+quality\s+of\s+life|has\s+had\s+enough(?!\s+(?:food|water|to\s+eat|dinner)))\b",
)
def _any_of(*groups):
    parts = [r"(?:" + part + r")" for group in groups for part in group]
    return r"(?:" + "|".join(parts) + r")" if len(parts) > 1 else parts[0]


def _both(first, *rest):
    return ("(?=.*" + _any_of(first) + r")(?=.*" + _any_of(*rest) + r")",)


RASH = (r"(?:rash|rashes|spots|marks|blotches|dots|purpura|petechiae)")
RASH_NAMED = (r"\bnon[\s-]?blanch\w*", r"\bpetechiae\b", r"\bpurpura\b")
RASH_DEFINITION = (
    r"\b(?:what|whats|what'?s|which)\s+(?:is|are|does|do)\b[^.?!]{0,30}"
    r"\b(?:non[\s-]?blanch\w*|blanching)\b",
    r"\b(?:explain|definition\s+of|meaning\s+of|what\s+does)\b[^.?!]{0,25}"
    r"\b(?:non[\s-]?blanch\w*|blanching|blanch)\b",
)
RASH_FLAT = _both((RASH,), RASH_FADE)
RASH_RED = (
    r"\bnon[\s-]?blanch\w*",
    r"\b(?:petechiae|petechial|purpura|purpuric)\b",
    r"\bpurple\s+(?:rash|spots|marks|dots|blotches)\b",
    r"\b(?:bruise|bruises|bruising)\b[^.?!]{0,25}\b(?:for\s+no\s+reason|out\s+of\s+nowhere|"
    r"spreading|everywhere)\b",
) + RASH_FLAT
BLACKOUT_ANY = (
    r"\b(?:pass(?:ed|ing)?\s+out|black(?:ed|ing)?\s+out|faint(?:ed|ing)?)\b",
)
BLACKOUT_HEART = (
    r"\b(?:chest\s+(?:pain|tight\w*|pressure|heavy)|palpitation\w*|racing\s+heart|"
    r"heart\s+(?:racing|pounding|fluttered|fluttering|went)|fluttering|irregular\s+heartbeat|"
    r"pounding\s+heart)\b",
)
BLACKOUT_STILL_DOWN = (
    r"\b(?:not|hasn'?t|haven'?t|isn'?t|wasn'?t)\s+(?:come\s+round|came\s+round|woken?|"
    r"woke|with\s+it|responding)\b",
    r"\b(?:out\s+cold|in\s+and\s+out|still\s+(?:out|down))\b",
)
BLACKOUT_URGENT = (BLACKOUT_EFFORT + BLACKOUT_HEART + BLACKOUT_FLOOR + BLACKOUT_STILL_DOWN
                   + BLACKOUT_BREATH)
BLACKOUT_RED = BLACKOUT_URGENT + BLACKOUT_REPEAT + BLACKOUT_SOMEONE_DOWN
BLACKOUT_RED_LINE = _both(BLACKOUT_ANY, BLACKOUT_RED)
FEVER_SIGN = (
    r"\bfever\w*", r"\btemperature\b", r"\btemp\b", r"\bfeverish\b", r"\bburning\s+up\b",
    r"\bhot\s+to\s+touch\b", r"\b\d{2}(?:\.\d)?\s*(?:c\b|degrees)", r"\bhigh\s+temperature\b",
)
RASH_COMPANY = FEVER_SIGN + (
    r"\b(?:baby|babies|newborn|infant|toddler|child|children|kid|kids|son|daughter|boy|girl|"
    r"nursery|school)\b",
    r"\b(?:everywhere|all\s+over|spreading)\b", r"\bpetechiae\b", r"\bpurpura\b",
)
RED_ANCHOR = HUMAN_ANCHOR + (
    r"\b(?:his|her|their|hes|shes|theyre|our|your|newborn|new\s?born|infant|toddler|baby)\b",
    r"\b\d+\s*(?:days?|weeks?)\s+old\b", r"\b(?:1|2|one|two)[-\s]*months?[-\s]*old\b",
    r"\b(?:is|only|just|nearly)\s+(?:1|2|one|two)\s+months?\b",
    r"\b\d+\s*(?:year|yr|month)s?[-\s]*old\b",
    r"\b(?:one|two|three|four|five|six|seven|eight|nine|ten)(?:\s+and\s+a\s+half)?\s+years?\s+old\b",
    r"\b(?:my|his|her|their|our)\s+(?:son|daughter|boy|girl|child|kid|little\s+one)\b",
)
DEVICE_TEMP = (
    r"\b(?:oven|boiler|room|water|thermostat|fridge|freezer|shower|bath|heating|radiator|"
    r"washing\s+machine|tumble\s+dryer|air|weather|engine|car)\b[^.?!]{0,20}\btemperatures?\b",
    r"\btemperatures?\s+(?:setting|gauge|dial|control|knob)\b",
)
NEWBORN_FINE = (
    r"\bover\s+(?:3|three|6|six)\s+months\b",
    r"\b(?:3|4|5|6|7|8|9|1\d|[2-9]\d)\s+months?\s+old\b",
    r"\b(?:three|four|five|six|seven|eight|nine|ten|eleven|twelve)\s+months?\s+old\b",
    r"\b\d+\s*(?:years?|yrs?)\s+old\b",
)
TINY_SAID = (
    r"\b(?:my|our|the)\s+(?:baby|babies|newborn|infant|little\s+one)\b",
    r"\b(?:my|our)\s+(?:son|daughter|boy|girl|child)\b",
)


CHILD_BY_PLACE = (r"(?:my|our|his|her|their)\s+(?:youngest|eldest|oldest|little\s+one|"
                  r"middle\s+one|lad|lass|kiddo|laddie)")
CHILD_WORD = (r"\b(?:" + CHILD_BY_PLACE + r"|kid|kids|baby|babies|toddler|newborn|infant|child|"
              r"children|boy|girl|sons?|"
              r"daughters?|school\s?child|\d+\s*(?:year|month|yr)s?[\s-]*old|(?:one|two|three|four|"
              r"five|six|seven|eight|nine|ten)\s+years?[\s-]*old)\b")

PALE_SIGN = (
    r"\bpale\b", r"\bpallid\b", r"\bwhite\s+as\s+a\s+sheet\b", r"\bgrey\b", r"\bgray\b",
    r"\bmottled\b", r"\bblue\s+(?:round|around)\s+the\s+(?:lips|mouth)\b",
)
PALE_CHILD = ("(?=.*" + _any_of((CHILD_WORD,)) + ")(?=.*" + _any_of(PALE_SIGN) +
              ")(?=.*" + _any_of(PALE_SECOND) + ") ",)
ADULT_PERSON = (
    r"\b(?:husband|wife|partner|boyfriend|girlfriend|fianc\w+|mum|mom|mummy|mother|dad|daddy|"
    r"father|nan|nana|gran|grannie|granny|grandma|grandmother|grandad|grandpa|grandfather|"
    r"sister|brother|aunt|auntie|uncle|cousin|friend|mate|neighbour|neighbor|colleague|"
    r"coworker|flatmate|housemate|lodger|carer|he|she|him|her)\b",
)
ADULT_ME = (
    r"\b(?:i|i'm|im|ive|i've|i\s+am|i\s+feel|i\s+look|i\s+went|i\s+have|me|myself|my\s+own)\b",
)
PALE_ADULT = ("(?=.*" + _any_of(ADULT_PERSON + ADULT_ME) + ")(?=.*" + _any_of(PALE_SIGN) +
              ")(?=.*" + _any_of(PALE_SECOND) + ") ",)
PALE_EXERTION = (
    r"\b(?:after|during|at|from|in)\s+(?:(?:a\s+|the\s+)?(?:\w+\s+){0,2}"
    r"(?:race|run|match|game|session|training|lesson|class|practice|workout|circuit|"
    r"walk|hike|ride)|"
    r"cross\s?country|school\s+run|football|rugby|netball|hockey|the\s+gym|sports?\s+day|"
    r"swimming|a\s+swim|cycling|a\s+bike\s+ride|pe)\b",
    r"\b(?:after|during|at|from|in)\s+(?:his|her|my|their|our|the|a|an)?\s*"
    r"(?:tennis|badminton|squash|cricket|athletics|gymnastics|dance|dancing|ballet|judo|karate|"
    r"martial\s+arts|taekwondo|boxing|climbing|rowing|trampolining|skating|skateboarding|"
    r"snowboarding|skiing|riding|horse\s+riding|sports?|games?|practice|training|workout|walk|"
    r"walking|hike|hiking|ramble)\b",
)
PALE_EFFORT = PALE_EXERTION + PALE_HEAT + (
    r"\b(?:after|during|at|from|in)\s+(?:the\s+)?(?:park|playtime|playground|playing\s+out|"
    r"the\s+beach|nursery|soft\s+play)\b",
    r"\b(?:just|only)\s+been\s+(?:running|playing|out)\b",
)
PALE_EFFORT_REAL = PALE_EXERTION + (
    r"\b(?:just|only)\s+been\s+running\b",
)
PALE_EFFORT_NO = (
    r"\bclammy\b", r"\bcold\b", r"\bfloppy\b", r"\blimp\b", r"\bdrows\w*",
    r"\bsleepy\b", r"\bunresponsive\b", r"\bconfus\w*",
)
PALE_OTHER_RED = (
    r"\bfloppy\b", r"\blimp\b", r"\b(?:wont|won't|not|can't|cant|unable\s+to)\s+wake\b",
    r"\bunresponsive\b", r"\bunconscious\b", r"\bcollapsed\b",
    r"\bblue\s+(?:round|around)\s+the\s+(?:lips|mouth)\b",
    r"\bbreathing\s+(?:fast|quickly|hard)\b", r"\bgrunting\b", r"\bnot\s+breathing\b",
)
PALE_EFFORT_RED = (
    r"\bfloppy\b", r"\blimp\b", r"\b(?:wont|won't|not|can't|cant|unable\s+to)\s+wake\b",
    r"\bunresponsive\b", r"\bunconscious\b", r"\bcollapsed\b", r"\bblue\b",
    r"\bgrey\b", r"\bgray\b", r"\bmottled\b", r"\bbreathing\s+(?:fast|quickly|hard)\b",
    r"\bgrunting\b", r"\bnot\s+breathing\b",
)
PALE_ADULT_ITSELF = (
    r"\b(?:(?:my|his|her|their|your|our|the|both)\s+)?(?:hands?|feet|fingers|toes|palms?)\s+"
    r"(?:(?:are|is|were|was|feel|feels|felt|go|goes|went|get|gets|got|look|looks)\s+)?"
    r"(?:\w+\s+){0,2}?(?:pale|grey|gray|white|clammy|cold)\b",
)
PALE_ADULT_WHOLE = (
    r"\b(?:i|he|she|they|we|you)\s+(?:am|is|are|was|were|look|looks|looked|feel|feels|felt|"
    r"have\s+gone|has\s+gone|went|got)\s+(?:\w+\s+){0,2}(?:pale|grey|gray|clammy|ashen|"
    r"white\s+as)\b",
)
PALE_ADULT_FINE = (
    r"\bhangover\w*\b", r"\b(?:been|out)\s+drinking\b", r"\bhung\s?over\b",
    r"\b(?:after|from|at)\s+(?:my|a|the|his|her)\s+(?:blood\s+test|bloods|jab|injection|"
    r"vaccine|vaccination|needle|donation|giving\s+blood|blood\s+donation)\b",
    r"\b(?:with|from|got|has|have|had)\s+(?:an?\s+)?(?:cold|flu|virus|hangover)\b",
    r"\b(?:nervous|nerves|anxious|anxiety|panick\w*|panic\s+attack|scared|frightened|"
    r"terrified|stage\s+fright|worried|exam|interview|dentist|needle\s+phobia)\b",
    r"\bgave\s+blood\b", r"\bblood\s+donor\b",
)
NAMED_SICK = (r"\b(?:meningitis|meningococcal|sepsis|blood\s+poisoning|pneumonia|encephalitis|"
              r"necrotis\w+\s+fasciitis|kawasaki\s+disease)\b")
NAMED_SAID = (r"\b(?:has|have|got|caught|diagnosed\s+with|being\s+treated\s+for|"
              r"think\s+(?:its|it's)|think\s+(?:he|she)\s+(?:has|might\s+have)|might\s+have|"
              r"probably\s+has|suspect\w*|getting|coming\s+down\s+with|gone\s+septic|"
              r"going\s+septic)\b")
NAMED_ILLNESS_CHILD = ("(?=.*" + PEOPLE + ")(?=.*" + NAMED_SAID + ")(?=.*" + NAMED_SICK + ")",)
HIGH_TEMP = (r"\b(?:39\.[5-9]|4[0-3](?:\.\d)?)\s*(?:c\b|degrees)?",)
TEMP_ANCHOR = HUMAN_ANCHOR + (
    r"\b(?:my|his|her|their|the)\s+(?:temperature|temp)\b",
    r"\b(?:my|his|her|their)\s+(?:fever|high\s+temperature)\b",
    r"\b(?:my|his|her|their|our)\s+\d+\s*(?:year|month|yr)s?[-\s]*old\b",
)
HIGH_TEMP_CHILD = ("(?=.*" + HIGH_TEMP[0] + r")(?=.*\b(?:temperature|temp|fever)\b)(?=.*"
                   + _any_of(TEMP_ANCHOR) + ")",)
CHILD_FEVER = ("(?=.*" + CHILD_WORD + r")(?=.*\b(?:temperature|temperatures|temp|fever|feverish|"
               r"fevered|hot\s+to\s+(?:the\s+)?touch|hot\s+to\s+touch|boiling\s+hot|"
               r"burning\s+up|hot\s+and\s+(?:shivery|clammy|sweaty|floppy|miserable|grumpy|"
               r"sleepy)|(?:really|very|so|properly|absolutely)\s+hot|feels?\s+(?:hot|warm|"
               r"feverish))\b)",)
CHILD_DRANK = ("(?=.*" + CHILD_WORD + r")(?=.*\b(?:drank|drunk|swallowed|got\s+into|glugged|"
               r"sipped|downed|sucked|licked)\b)(?=.*\b(?:gin|vodka|whisk(?:y|ey)|beer|wine|"
               r"alcohol|lager|rum|brandy|prosecco|cider|spirits|liqueur|moonshine|schnapps|"
               r"mouthwash|hand\s+saniti[sz]er|aftershave|perfume)\b)",)
CHILD_DRANK_WEAK = (r"\b(?:beer|beers|lager|cider|shandy|ale|stout|pint|a\s+sip|a\s+taste|"
                    r"a\s+swig|swig)\b",)
RECENT_FIT = _both(
    (CHILD_WORD + r"|\b" + PEOPLE + r"\b",),
    (r"\b(?:just\s+had|has\s+had|had)\s+(?:a|another|his\s+first|her\s+first)\s+"
     r"(?:fit|seizure|convulsion)\b",),
)
GRUNTING_BABY = _both(
    (r"\b(?:baby|babies|newborn|infant|toddler)\b",),
    (r"\bgrunting\b|\bgrunts\b",),
)
GRUNTING_NOW = (
    r"\bgrunt\w*\b[^.?!]{0,30}\b(?:breath\w*|every\s+breath|when\s+(?:he|she|they)\s+breathes)\b",
    r"\b(?:blue|floppy|limp|not\s+feeding|wont\s+feed|unresponsive|fever|temperature|"
    r"struggling\s+to\s+breathe|working\s+hard)\b",
)
SLEEPY_FEED = (r"\btoo\s+(?:sleepy|drowsy|tired|floppy|weak)\s+to\s+(?:feed|eat|drink|wake|"
               r"suck|take\s+(?:a\s+)?feed|be\s+woken)\b",
               r"\b(?:wont|won'?t|refus\w+\s+to)\s+(?:feed|take\s+(?:a|his|her)\s+feed|"
               r"wake\s+for\s+(?:a\s+)?feed)\b")

FEVER_RASH = ("(?=.*" + _any_of(FEVER_SIGN) + r")(?=.*" + _any_of((RASH,)) + r")(?=.*"
              + _any_of(HUMAN_ANCHOR) + ")",)

STIFF_NECK_RED = _both(STIFF_NECK, MENINGITIS_OTHER + FEVER_SIGN)
SEPSIS = _both(FEVER_SIGN, SEPSIS_SIGN)
TEMP_FALLING_WEATHER = (
    r"\b(?:the|outside)\s+temperature\s+(?:is|are|was|were|keeps?|kept|has|had|have)\s+"
    r"(?:been\s+)?(?:falling|dropping|dropped|fell|down|low|going\s+down|below)\b",
    r"\bthe\s+temperature\b[^.?!]{0,25}\b(?:outside|today|forecast|weather|tomorrow)\b",
)
FEVER_NOT_THE_WEATHER = (
    r"\bfever\w*\b", r"\btemps?\b", r"\b\d{2}(?:\.\d)?\s*(?:c\b|degrees)\b",
    r"\bburning\s+up\b", r"\bhot\s+to\s+touch\b", r"\bhigh\s+temperature\b",
    r"\b(?:spiked|went\s+up\s+to|running\s+a\s+temp)\b",
)
FEVER_CASES = frozenset(("red_flags", "stiff_neck", "sepsis_signs", "newborn_fever",
                         "named_illness", "high_temp", "rash_headache", "fever_rash",
                         "child_fever"))
FEVER_HOME_CARE = frozenset(("child_fever", "high_temp"))
_A_DISEASE_CALLED_A_FEVER = (
    r"\b(?:glandular|scarlet|yellow|dengue|rheumatic|typhoid|paratyphoid|q|lassa|ebola|marburg|"
    r"crimean-congo|rocky\s+mountain\s+spotted|mediterranean\s+spotted|swine|haemorrhagic|hemorrhagic)"
    r"\s+fever\b",
)
_THE_TEMPERATURE_WORDS = (
    r"\bfever\w*", r"\bfeverish\b", r"\btemps?\b", r"\btemperatures?\b",
    r"\bhot\b", r"\bhot\s+to\s+(?:the\s+)?touch\b", r"\bburning\s+up\b",
    r"\bhigh\s+temperature\b", r"\b\d{2}(?:\.\d)?\s*(?:c\b|degrees)",
)


def _the_only_fever_is_a_disease_name(line):
    if not _matches(_A_DISEASE_CALLED_A_FEVER, line):
        return False
    stripped = line
    for pattern in _A_DISEASE_CALLED_A_FEVER:
        stripped = re.sub(pattern, " ", stripped)
    return not _matches(_THE_TEMPERATURE_WORDS, stripped)
FEVER_STILL_NOW = SEPSIS_SIGN + (
    r"\bsince\s+(?:last\s+)?(?:night|yesterday|friday|saturday|sunday|monday|tuesday|wednesday|"
    r"thursday|this\s+morning|teatime)\b",
    r"\bstill\b", r"\bright\s+now\b", r"\bhas\s+had\b", r"\bstarted\b",
)
BABY_HOT_SUBJECT = _any_of((
    r"\b(?:baby|newborn|new\s?born|infant|little\s+one|son|daughter|boy|girl|she|he|they|"
    r"\d+\s*(?:days?|weeks?|months?)(?:\s+old)?|under\s+(?:3|three)\s+months?)\b",
))
TRUE_NEWBORN = _any_of((
    r"\bnew\s?born\b", r"\bjust\s+born\b", r"\b\d+\s*days?\s*(?:old)?\b",
    r"\b(?:1|2|3|4|one|two|three|four)\s*weeks?\s*(?:old)?\b",
    r"\bunder\s+(?:1|one)\s+month\b",
    r"\b(?:is|only|just|nearly)\s+(?:1|2|3|4|one|two|three|four)\s+weeks?\b",
))
TRUE_NEWBORN_FINE = (
    r"\b(?:5|6|7|8|9|10|11|12|five|six|seven|eight|nine|ten|eleven|twelve)\s*weeks?\s*(?:old)?\b",
    r"\b(?:is|only|just|nearly)\s+(?:5|6|7|8|9|10|11|12|five|six|seven|eight|nine|ten|eleven|"
    r"twelve)\s+weeks?\b",
    r"\b(?:1|2|one|two)\s*months?\s*(?:old)?\b",
    r"\b(?:is|only|just|nearly)\s+(?:1|2|one|two)\s+months?\b",
    r"\b(?:under|less\s+than)\s+(?:3|three)\s+months?\b",
)
BABY_NAMED = _any_of((
    r"\b(?:baby|newborn|new\s?born|infant|little\s+one|son|daughter|boy|girl|she|he|they)\b",
    r"\b(?:my|our|his|her|their)\s+(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|"
    r"eleven|twelve)\s*(?:days?|weeks?|months?)\s*old\b",
))
BABY_BURNING = (r"\bboiling\b", r"\bburning\s+hot\b")
BABY_IS_HOT = (
    BABY_HOT_SUBJECT + r"[^.?!]{0,7}\b(?:boiling|burning\s+hot)\b",
    BABY_HOT_SUBJECT + r"[^.?!]{0,12}\b(?:is|was|got|has\s+gone)\s+"
    r"(?:really\s+|very\s+|so\s+)?(?:boiling|burning\s+hot)\b",
    r"(?=.*" + TRUE_NEWBORN + r")(?=.*" + BABY_NAMED + r")(?=.*" + BABY_HOT_SUBJECT +
    r"[^.?!]{0,7}\b(?:feels?|is|was)\s+(?:really\s+|very\s+|so\s+)?(?:hot|very\s+hot)\b)",
)
NEWBORN_TEMP = (
    r"(?=.*" + _any_of(NEWBORN) + r")(?=.*" + BABY_NAMED + r")(?=.*"
    + _any_of(FEVER_SIGN + BABY_IS_HOT) + r")",
)
NEWBORN_NEXT = FEVER_SIGN + (r"\bboiling\b", r"\bburning\s+hot\b", r"\bvery\s+warm\b",
                r"\bfeels?\s+(?:really\s+|very\s+|so\s+)?hot\b",
                r"\bis\s+(?:really\s+|very\s+|so\s+)?hot\b",
                r"\bbreathing\s+(?:fast|quickly|hard)\b")

DIABETIC = (
    r"\bdiabet\w*\b", r"\btype\s*(?:1|2|one|two)\b", r"\bblood\s+sugar\b", r"\bglucose\b",
    r"\bhypo(?:s|glyc\w*)?\b",
    r"\b(?:blood\s+)?sugar\s+(?:is\s+|was\s+|levels?\s+(?:is\s+|are\s+)?)?"
    r"(?:low|dropped|dropping|dipped|crashing|bottomed\s+out|too\s+low)\b",
    r"\b(?:blood\s+)?sugar\s+level\w*\s+(?:is\s+|are\s+)?(?:low|dropping|dropped)\b",
)
DIABETIC = DIABETIC + SUGAR_READING_LOW
HYPO = _both(DIABETIC, HYPO_SIGN)
HYPO_PAST = (
    r"\b(?:yesterday|last\s+night|last\s+week|last\s+month|years?\s+ago|used\s+to|"
    r"when\s+i\s+was|ages\s+ago|this\s+morning|earlier|the\s+other\s+day)\b",
)
HYPO_NOW = (
    r"\b(?:now|right\s+now|at\s+the\s+moment|currently|still|getting|has\s+gone|gone)\b",
)
HYPO_NO_MOUTH = (
    r"\b(?:a|another)\s+fit\b", r"\bfitting\b", r"\bseizure\w*", r"\bconvuls\w*",
    r"\bcoma\b", r"\bunconscious\b", r"\bunresponsive\b", r"\bcan'?t\s+stay\s+awake\b",
    r"\b(?:won'?t|wont|not|isn'?t)\s+wak\w*", r"\bout\s+cold\b", r"\bpassed\s+out\b",
    r"\bfainted\b",
)
HYPO_LIE_IN = (
    r"\b(?:won'?t|wont|not|never)\s+wak\w*\b[^.?!]{0,20}\b(?:before|until|till|by|at)\s*"
    r"(?:\d{1,2}(?!\d)|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"noon|lunch|midday)\b",
    r"\bwak\w*\s+up\s+at\s+\d{1,2}(?!\d)",
)
LOW_SUGAR_NOW = (
    r"\bhypo(?:s|glyc\w*)?\b",
    r"\b(?:sugar|glucose)\b(?!\s+was\b)[^.?!]{0,15}\b(?:low|dropped|dropping|dipped|"
    r"crashing|too\s+low)\b",
)

OBJECT_IN_HEAD_PLACE = r"(?:nose|nostril|ear)(?:s)?"
OBJECT_IN_HEAD = (
    r"\b" + OBJECT_IN_HEAD_THING + r"\b[^.!?]{0,30}\b(?:up|in|inside|into|"
    r"stuck\s+(?:up|in|inside|into)|wedged|lodged)\b[^.!?]{0,25}\b"
    r"(?:my|his|her|their|the|your)?\s*" + OBJECT_IN_HEAD_PLACE + r"\b",
    r"\b" + OBJECT_IN_HEAD_PLACE + r"\b[^.!?]{0,25}\b(?:has|have|had|got|with|holding)\b"
    r"[^.!?]{0,25}\b" + OBJECT_IN_HEAD_THING + r"\b",
    r"\bsomething\s+(?:is\s+|'s\s+)?(?:stuck|wedged|lodged)\s+(?:up|in|inside)\s+"
    r"(?:my|his|her|their)\s+" + OBJECT_IN_HEAD_PLACE + r"\b",
    r"\b(?:can'?t|cannot)\s+get\s+(?:it|something|the\s+\w+)\s+out\s+of\s+"
    r"(?:my|his|her|their)\s+" + OBJECT_IN_HEAD_PLACE + r"\b",
)

OBJECT_IN_HEAD_BATTERY = (
    r"\bbutton\s+batter(?:y|ies)\b",
    r"\b(?:batter(?:y|ies)|magnets?)\b[^.!?]{0,30}\b" + OBJECT_IN_HEAD_PLACE + r"\b",
    r"\b" + OBJECT_IN_HEAD_PLACE + r"\b[^.!?]{0,30}\b(?:batter(?:y|ies)|magnets?)\b",
)

OBJECT_IN_HEAD_BLOW = (
    r"\b(?:hit|hits|hitting|slapp?(?:ed|s|ing)?|punch(?:ed|es|ing)?|head-?butt(?:ed|s)?|kicked?)\b"
    r"[^.!?]{0,30}\b(?:my|his|her|their|the|your)\s+(?:nose|ear|earhole)\b",
)

BONE_RED = (
    r"\b(?:can'?t|cannot|can\s+not|unable\s+to|couldn'?t|not\s+able\s+to)\s+swallow\b",
    r"\bdrool\w*\b", r"\b(?:can'?t|cannot|struggling\s+to|hard\s+to)\s+breathe\b",
    r"\bturning\s+blue\b", r"\b(?:a\s+lot\s+of|lots\s+of|coughing\s+up)\s+blood\b",
)

BONE_STILL = (
    r"\bstill\b", r"\bhasn'?t\s+(?:come|came)\s+out\b", r"\bnever\s+came\s+out\b",
    r"\bsince\s+then\b", r"\bit'?s\s+been\s+(?:stuck|there|in)\b", r"\bleft\s+in\b",
)

OLD_DOWN = (
    r"\b(?:fell|fallen|fall|tripped|slipped|went\s+over|went\s+down|toppled|tumbled|"
    r"collapsed|had\s+a\s+fall|took\s+a\s+tumble)\b",
)

SHOT_SELF = (
    r"\bi\s+(?:got|gets|was|were|have|had|am|'m|been)\b[^.?!]{0,15}\bshot\b",
    r"\bshot\s+me\b", r"\bthey\s+shot\s+me\b", r"\bi\s+(?:have\s+)?been\s+shot\b",
    r"\bi\s+(?:have\s+|had\s+)?shot\s+my\s*self\b",
)
BODY_LIMB = (r"(?:arms?|legs?|wrist|ankle|fingers?|thumb|shin|knee|elbow|shoulder|collarbone|"
             r"jaw|foot|toes?|ribs?|hip|thigh|heel|hands?|forearm)")
BONE_OUT = (
    BODY_LIMB + r"\b[^.?!]{0,25}\bbones?\b[^.?!]{0,25}\b(?:sticking|poking|coming\s+through|"
    r"through|out|show(?:ing|s)?)\b",
    r"\bbones?\b[^.?!]{0,20}\b(?:sticking\s+out|poking\s+out|through\s+the\s+skin|"
    r"out\s+of\s+my\s+" + BODY_LIMB + r")\b",
    r"\b(?:open|compound)\s+fracture\b",
)
BONE_OUT_LOOSE = (r"\b(?:bone|wrist|arm|leg)\b[^.?!]{0,25}\b(?:sticking|poking|piercing)\s+out\b",)
FOOD_BONE = (
    r"\b(?:chicken|turkey|lamb|beef|pork|ham|steak|meat|fish|broth|carcass|bin\s*bag|soup|stock|"
    r"skeleton|doll|toy|dog|cat|puppy|kitten)\b",
)
CUT_SELF = r"\b(?:myself|himself|herself|yourself|ourselves|themselves)\b"
NOT_A_BODY_CUT = (
    r"\bcut\s+(?:flowers?|grass|lawn|hedge|hair|bread|costs?|the\s+flowers)\b|"
    r"\b(?:flowers?|vase|bouquet|stems?|tulips?|daffodils?|lilies|carnations?)\b|"
    r"\b(?:haircut|paper\s*cut\s+cost|budget|spending)\b|"
    r"\bpower\s*cut\b|\b(?:power|electricity)\s+(?:cut|outage|failures?|failure|went|goes|gone|"
    r"is|was|back|came)\b|\b(?:lost|losing|lose)\s+(?:the\s+)?(?:power|electricity)\b",
)
BONE_FINE = (
    r"\b(?:chicken|turkey|lamb|beef|pork|ham|steak|meat|fish|broth|dog|cat|puppy|kitten|"
    r"pet|toy|doll|skeleton|bone\s+density|bone\s+scan|x-?ray)\b",
)
HEADACHE = (r"\bhead(?:ache)?\b",)
HEADACHE_WORST_EVER = (
    r"\bworst\s+head(?:ache)?\s+of\s+my\s+life\b", r"\bworst\s+head(?:ache)?\s+ever\b",
    r"\bnever\s+had\s+a\s+headache\s+like\s+(?:this|it)\b",
)
HEADACHE_ANY = (
    r"\bheadaches?\b", r"\bhead\s+hurts?\b",
    r"\bhead\s+(?:is\s+|really\s+|just\s+|has\s+been\s+)?(?:killing|banging|thumping|pounding|"
    r"splitting|sore)\b",
    r"\b(?:killing|banging|thumping|pounding|splitting)\s+headache\b",
)
HUMAN_KID = HUMAN_ANCHOR + (
    r"\b(?:baby|babies|toddler|newborn|new\s?born|infant|little\s+one|teenager|teen|lad|"
    r"lass|schoolboy|schoolgirl)\b",
)
RASH_HEADACHE = ("(?=.*" + _any_of((RASH,)) + r")(?=.*" + _any_of(HEADACHE_ANY) + r")(?=.*"
                 + _any_of(HUMAN_KID) + ")",)
VOMIT_BLOOD = (
    r"\b(?:vomit\w*|throw\w*|threw|thrown|sick|puke\w*|puked)\b[^.?!]{0,20}\b(?:up\s+)?blood\b",
    r"\bblood\s+in\s+(?:my|his|her|their|the)\s+(?:vomit|sick|puke)\b",
    r"\b(?:coffee\s+grounds?)\b[^.?!]{0,20}\b(?:vomit|sick)\b",
)
ELECTRIC_COOKER = (
    r"\b(?:slow|rice|pressure|multi|electric)\s*-?\s*cooker\b",
    r"\belectric\s+(?:hob|ring|cooker|oven)\b",
    r"\bair\s*fryer\b",
)
GAS_WORD = (
    r"\bgas\b",
    r"\bsmell\w*\b",
    r"\bhissing\b",
    r"\bleak\w*\b",
)


COUGH_FINE = (
    r"\b(?:film|movie|tv|telly|show|series|game|book|novel|story|dream|dreamt|song)\b",
    r"\b(?:last\s+(?:year|month)|years?\s+ago|when\s+i\s+was\s+(?:a\s+)?(?:kid|child|little)|"
    r"used\s+to|had\s+it\s+before)\b",
)

BREATH_SPORT = (
    r"\b(?:run|runs|running|jog\w*|gym|swim\w*|cycl\w*|bike|football|rugby|squash|tennis|"
    r"rowing|hiit|zumba|boxing|netball|hockey|marathon|parkrun|spin\s+class|workout)\b",
)
SPIKED_STAND_DOWN = (
    r"\b(?:sauce|chilli|chili|curry|salsa|seasoning|food|pizza|joke|prank|meme|coffee\s+order)\b",
    r"\b(?:last\s+(?:year|month)|years?\s+ago|months?\s+ago|when\s+i\s+was\s+(?:a\s+)?"
    r"(?:kid|young|little|at\s+uni))\b",
)

HEARD_ASSAULT_OFF = (
    r"\b(?:tv|telly|television|film|movie|netflix|episode|boxset|box\s+set|game|game\s+show|"
    r"playstation|xbox|console|radio|podcast|song|music|match|football|party|karaoke)\b",
    r"\b(?:last\s+(?:year|week|month)|years?\s+ago|months?\s+ago|used\s+to)\b",
)

EFFORT_SWEAT = (
    r"\b(?:sweat\w*|clammy)\b",
)
EFFORT_MORE_RED = EFFORT_SWEAT + EFFORT_RED_HEART
EFFORT_POSTURAL = (
    r"\b(?:when|as|after|if)\s+i\s+(?:stand|stand\s+up|standing|standing\s+up|get\s+up|getting\s+up|"
    r"stood|stood\s+up|rise|rising)\b",
    r"\bon\s+standing\b|\bstanding\s+up\s+too\s+fast\b",
)
EFFORT_TRAVEL_PAIN = (
    r"\b(?:arm|arms|jaw|shoulder|shoulders|neck)\b[^.?!]{0,20}"
    r"\b(?:hurt\w*|pain\w*|ache\w*|tight\w*|heavy|sore|numb)\b",
    r"\b(?:hurt\w*|pain\w*|ache\w*|tight\w*|heavy|sore)\b[^.?!]{0,15}"
    r"\b(?:arm|arms|jaw|shoulder|shoulders|neck)\b",
)
EFFORT_SICK = (
    r"\b(?:feel|feels|feeling|felt)\s+(?:sick|ill|queasy|sickly)\b",
    r"\b(?:queasy|nauseous)\b",
)
EFFORT_SICK_PAIR = (
    r"\bsick\b[^.?!]{0,24}\b(?:sweat\w*|clammy|faint\w*|dizzy|light-?headed|woozy|pale|grey|gray|"
    r"cold)\b",
    r"\b(?:sweat\w*|clammy|faint\w*|dizzy|light-?headed|woozy|pale|grey|gray)\b[^.?!]{0,24}\bsick\b",
)
EFFORT_SOMEONE_ELSE = (
    r"\b(?:my|our|his|her|their)\s+" + PERSON + r"\b",
    r"\b(?:he|she|they)\b\s*(?:'?s|is|was|were|keeps?|kept|can'?t|cant|couldn'?t|couldnt|"
    r"has|had|started)\b",
)
EFFORT_RECOVERY = (
    r"\b(?:catch|caught|get|getting|got|find|finding)\s+(?:my|her|his|their)?\s*breath\b",
    r"\bbreath\s+back\b",
    r"\b(?:out\s+of|short(?:ness)?\s+of)\s+(?:puff|breath)\b",
    r"\b(?:puffed|puffing|winded|blown|breathless)\b",
)


STING_MILD = (
    r"\b(?:nettles?|mosquito(?:es)?|midges?|gnats?|horse\s?fly|ants?|fleas?|bramble\w*|"
    r"thorns?|thistles?|stingers?\s+weed)\b",
)
STING_WINGED = (r"\b(?:wasps?|bees?|hornets?|bumble\s?bee\w*)\b",)
SWELLING_NOW = LIPS_SWELL_BARE[:3]
AIRWAY_CHANGED = (r"\b(?:throat|tongue|uvula|lips?)\b",)

LIPS_TINGLE_TRIGGER = (
    r"\b(?:peanuts?|nuts?|tree\s+nuts?|shellfish|prawns?|crabs?|lobster|fish|sesame|egg|eggs|"
    r"milk|soy|wheat|kiwi|strawberr\w*|bee|bees|wasp|sting\w*|stung|allerg\w*|reaction|"
    r"epipen|antihistamine)\b",
)
SPICY_MOUTH = (
    r"\b(?:spicy|spice|chilli|chili|chillies|chilies|hot\s+sauce|wasabi|horseradish|szechuan|"
    r"sichuan|peppercorns?|jalape\w+|naga|scotch\s+bonnet|vindaloo|hot\s+curry)\b",
)
THROAT_THICK = (
    r"\bthroat\b[^.?!]{0,20}\b(?:feels?|is|has\s+gone|has\s+got|going)\s+"
    r"(?:a\s+bit\s+|a\s+little\s+|really\s+|very\s+|so\s+)?thick\b",
)
MOUTH_TINGLE = (
    r"\b(?:tingl\w*|numb(?:ness|ed|ing|s)?|pins\s+and\s+needles|prickl\w*)\b",
)
LIPS_TINGLE_MOUTH = (
    r"\b(?:lips?|tongue|mouth)\b",
)
LIPS_NUMB = (
    r"\b(?:numb|numbness|dead|gone\s+dead)\b",
)
LIPS_TINGLE_SAID = (
    r"\b(?:tingl\w*|pins\s+and\s+needles|prickl\w*|fizz\w*|buzz\w*|tingly)\b",
)
LIPS_LIMB_TOO = (
    r"\b(?:hands?|fingers?|fingertips?|feet|foot|toes?|arms?|legs?|chest|shoulders?)\b",
)
LIPS_TINGLE_ELSEWHERE = (
    r"\b(?:eat|eats|eating|ate|eaten|food|foods|fruit|fruits|raw|drink|drinks|drinking|drank|"
    r"glass|cup|wine|beer|lager|cider|coffee|tea|fizzy|juice|pineapple|apples?|kiwi|mango|"
    r"avocado|tomatoes?|strawberr\w*|berries|melon|peach\w*|cherr\w*|bananas?|citrus|oranges?|"
    r"lemons?|limes?|nuts?|peanuts?|shellfish|prawns?|sushi|curry|spices?|spicy|chilli|chili)\b",
    r"\b(?:cold|heat|hot|wind|sun|sunburn|freezing|frozen|weather)\b",
    r"\b(?:sting|stings|stung|bee|bees|wasp|wasp\s+sting|bite|bites|bitten)\b",
)
LIPS_TINGLE_BREATH = (
    r"\b(?:can'?t\s+breathe|cant\s+breathe|cannot\s+breathe|breath\w*|wheez\w*|stridor|"
    r"can'?t\s+swallow|cant\s+swallow|struggling\s+to\s+swallow|hard\s+to\s+swallow|voice|"
    r"throat\s+(?:is\s+)?(?:tight|tightening|closing|closing\s+up)|airway)\b",
)
SWALLOW_GONE = (
    r"\b(?:can'?t|cannot|can\s+barely|barely\s+can|couldn'?t|unable\s+to|not\s+able\s+to|"
    r"struggling\s+to|struggle\s+to)\s+(?:even\s+)?swallow\b",
    r"\bswallow(?:ing)?\s+(?:is\s+)?(?:impossible|gone|stopped)\b",
)
SWALLOW_GONE_BREATH = (
    r"\b(?:can'?t|cannot|hard\s+to|difficult\s+to|struggling\s+to|unable\s+to)\s+"
    r"(?:breathe|breath)\b",
    r"\b(?:breath\w*|wheez\w*|stridor)\b",
)
THROAT_TIGHT = (
    r"\bthroat\b[^.?!]{0,14}\b(?:feels?|feeling|is|'s)\s+(?:really\s+|very\s+|a\s+bit\s+)?"
    r"(?:tight|tightening|tightened|closed\s+up)\b",
    r"\b(?:tight|tightening)\s+throat\b",
)
THROAT_TIGHT_MILD = THROAT_TIGHT_CAUSE + (
    r"\b(?:a\s+bit|a\s+little|slightly)\b",
    r"\b(?:lips?|face|eyelids?|cheeks?)\b[^.?!]{0,20}\b(?:a\s+bit|slightly|a\s+little)\b",
)
LIPS_SWELL_OFF = (
    r"\b(?:cold\s+sore|chapped|chaps|dry\s+lips|chap\s?stick|lip\s+balm|piercing|"
    r"filler\w*|collagen|cosmetic|sunburn|sun\s+burn|gloss|lipstick|blister)\b",
    r"\b(?:last\s+(?:year|summer|month)|years?\s+ago|as\s+a\s+(?:kid|child))\b",
)

NOT_STOPPING_BARE = (
    r"\b(?:won'?t|wont|doesn'?t|doesnt|isn'?t|isnt|not|never|keeps?)\s+(?:on\s+)?stopp?(?:ed|ing)?\b",
    r"\b(?:still|keeps?)\s+(?:on\s+)?bleeding\b",
)
WOUND_NAMED = (
    r"\b(?:cut|wound|gash|slice|scratch|arm|leg|hand|finger|thumb|head|scalp|foot|toe|knee|elbow|"
    r"face|mouth|tongue|lip|gum|nose|ear|tattoo|pierc\w*|wrist|thigh|neck|eye|chest|belly|"
    r"stomach|back|bottom)\b",
)
NOSE_SITE = (r"\bnoses?\b", r"\bnostrils?\b", r"\bnose\s*bleed\w*\b")
BLEED_VOLUME = (
    r"\b(?:heavily|a\s+lot|pouring|dripping|soaking|soaked|everywhere|loads|badly|gushing|"
    r"spurting|pulsing)\b",
)
MOUTH_BLEED = (r"\b(?:tongue|lip|lips|gums?|mouth|cheek\s+inside|tooth\s+socket|palate)\b",)
MOUTH_BLEED_RED = (r"\b(?:pale|grey|gray|dizzy|faint|clammy|unconscious|shaking|deep\s+cut|gaping)\b",)
MOUTH_BLEED_OFF = (
    r"\bbrush\w*\b", r"\bfloss\w*\b", r"\b(?:my|the)\s+gums?\b[^.?!]{0,20}\bbleed\w*\b",
    r"\bdentist\b", r"\b(?:ulcer|sore)\b",
)

EXPECTING_OTHER = (
    r"\bmy\s+(?:wife|girlfriend|partner|friend|mate|sister|daughter|cousin|colleague|neighbour|"
    r"neighbor|flatmate|housemate|mum|mom|dad|husband|boyfriend|niece|aunt)\b",
    r"\bshe\s+is\s+(?:pregnan\w*|expecting)\b",
)
def _for_the_person(reply, line, case):
    if not reply or not case or not case.startswith("pregnancy_"):
        return reply
    if not _matches(EXPECTING_OTHER, line):
        return reply
    she = _person(line) != "he"
    obj, subject = ("her", "she") if she else ("him", "he")
    text = re.sub(r"\byou're\b", subject + "'s", reply, flags=re.I)
    text = re.sub(r"\byou've\b", subject + "'s", text, flags=re.I)
    text = re.sub(r"\byour\b", obj, text, flags=re.I)
    for verb in ("stops", "stop", "leave", "leaves", "get", "gets", "keep", "keeps", "make",
                 "makes", "take", "takes", "tell", "tells", "with", "for", "to"):
        text = re.sub(r"\b" + verb + r"\s+you\b", verb + " " + obj, text, flags=re.I)
    text = re.sub(r"\bthat\s+needs\b", subject + " needs", text, flags=re.I)
    text = re.sub(r"\byou\b", subject, text, flags=re.I)
    text = re.sub(r"\b(she|he)\s+((?:also|still|just|only)\s+)?(" + "|".join(map(re.escape, _THIRD)) +
                  r")\b",
                  lambda m: m.group(1) + " " + (m.group(2) or "") + _THIRD[m.group(3).lower()],
                  text, flags=re.I)
    if re.match(r"(?i)^ring\b", text):
        text = "Tell " + obj + " to ring " + text[4:].lstrip()
    return text[:1].upper() + text[1:]
NOT_PREG = (r"\A(?!.*\b(?:not|isn'?t|aren'?t|never|no\s+longer|stopped\s+being)\s+"
            r"(?:be\s+|been\s+)?(?:pregnant|pregnancy|expecting)\b)")
SICK_WORDS = (r"(?:can't|cannot|can\s+not|unable\s+to|struggling\s+to)\s+keep\b")
PREGNANCY_SICK = (
    NOT_PREG + r"(?=.*\b" + PREGNANCY_WORDS + r"\b)(?=.*\b" + SICK_WORDS + r")"
    r"(?=.*\b(?:food|water|drink|drinks|fluids?|meals?|anything|down)\b)",
    NOT_PREG + r"(?=.*\b" + PREGNANCY_WORDS + r"\b)"
    r"(?=.*\b(?:throwing\s+up|being\s+sick|vomit\w*|puking)\b)"
    r"(?=.*\b(?:always|all\s+day|all\s+the\s+time|constantly|everything|non.?stop|every\s+day|"
    r"for\s+(?:weeks|days))\b)",
    NOT_PREG + r"(?=.*\b" + PREGNANCY_WORDS + r"\b)(?=.*\bsick\b)"
    r"(?=.*\b(?:all\s+day|all\s+the\s+time|constantly|every\s+day|everything)\b)",
    NOT_PREG + r"(?=.*\b" + PREGNANCY_WORDS + r"\b)"
    r"(?=.*\b(?:can'?t|cannot|can\s+not)\s+stop\s+"
    r"(?:vomiting|puking|being\s+sick|throwing\s+up|sick)\b)",
)
PREGNANCY_SICK_Q = (
    r"\bmorning\s+sickness\b",
    NOT_PREG + r"(?=.*\b" + PREGNANCY_WORDS + r"\b)"
    r"(?=.*\b(?:is\s+it\s+normal|normal|usual)\b)"
    r"(?=.*\b(?:sick|nauseous|nausea|queasy|vomit\w*|throwing\s+up)\b)",
    NOT_PREG + r"(?=.*\b" + PREGNANCY_WORDS + r"\b)"
    r"(?=.*\b(?:how\s+long|what\s+helps|any\s+advice|tips)\b)"
    r"(?=.*\b(?:sick|nauseous|nausea|queasy|vomit\w*|morning)\b)",
    NOT_PREG + r"(?=.*\b" + PREGNANCY_WORDS + r"\b)"
    r"(?=.*\b(?:i\s+feel|feeling|i\s+am|i'?m|being|so)\s+(?:sick|nauseous|queasy)\b)",
)
PREGNANCY_BLEED = (
    NOT_PREG + r"(?=.*\b" + PREGNANCY_WORDS + r"\b)"
    r"\A(?!.*\b(?:no|not|isn'?t|never|stopped)\b.{0,12}\b(?:bleed\w*|blood|spotting)\b)"
    r"(?=.*\b(?:bleed\w*|bled|blood|spotting)\b)",
)
PREGNANCY_QUIET = (
    NOT_PREG + r"(?=.*\b" + PREGNANCY_WORDS + r"\b)"
    r"(?=.*\b(?:no\s+movement|not\s+moving|isn'?t\s+moving|stopped\s+moving|"
    r"less\s+movement|fewer\s+kicks|not\s+kicking|hasn'?t\s+moved|hasn'?t\s+kicked|"
    r"stopped\s+kicking|no\s+kicks)\b)",
    NOT_PREG + r"(?=.*\b" + PREGNANCY_WORDS + r"\b)"
    r"(?=.*\b(?:hasn'?t|haven'?t|not|isn'?t|didn'?t)\s+(?:felt|feel|been\s+feeling)\b"
    r".{0,25}\b(?:move|moves|moving|kick|kicks|kicking)\b)",
)
PREGNANCY_WATERS = (
    r"\bmy\s+waters?\s+(?:have\s+|has\s+)?(?:broke|broken|gone|went|leak\w*)\b",
    r"\bmy\s+waters?\s+(?:are\s+|is\s+)?leak\w*\b",
    r"\b(?:i'?m|im|i\s+am)\s+leaking\s+(?:fluid|waters)\b",
    r"\bi\s+think\s+my\s+waters?\b",
)
SOCKET_SHOCK = _both(
    (r"\b(?:got|get|gets|getting|had|has|have|took)\s+(?:a\s+|an\s+|the\s+)?"
     r"(?:electric(?:al)?\s+|nasty\s+|bad\s+|real\s+|proper\s+|little\s+)?shock\b",),
    (r"\b(?:socket|sockets|plug\s+socket|wall\s+socket|outlet|power\s+point|mains|"
     r"live\s+wire)\b",),
)
ELECTRIC_SHOCK = (
    r"\belectrocut\w*\b",
    r"\b(?:got|get|gets|getting|had|has|have|took|suffered)\s+(?:a\s+|an\s+|the\s+)?"
    r"(?:electric(?:al)?\s+shock|shock\s+(?:from|off|of))\b",
    r"\b(?:shock(?:ed)?|zapped)\s+(?:from|off|by)\s+(?:a|the|my|an|our)\s+"
    r"(?:socket|plug|wire|cable|lead|mains|fuse\s?box|switch|kettle|charger)\b",
    r"\b(?:touched|grabbed|held|caught)\s+(?:a\s+|the\s+)?live\s+(?:wire|cable|rail|terminal)\b",
    r"\blive\s+wire\b[^.?!]{0,20}\b(?:shock\w*|burn\w*|spark\w*)\b",
    SOCKET_SHOCK[0],
)
SOCKET_WORD = (r"\b(?:socket|sockets|plug\s+socket|wall\s+socket|outlet|power\s+point|"
               r"mains|plug\s+hole|the\s+plug)\b",)
SOCKET_POKE = (r"\b(?:put|puts|putting|stuck|sticking|stick|poked|poking|poke|shoves?|shoving|"
               r"shoved|pushes|pushing|pushed|jams?|jam(?:med|ming)?|forced|forcing|inserted|"
               r"inserting|plays?|playing|chews?|chewed|chewing|licks?|licked|bit|licks)\b",)
SOCKET_THING = (
    r"(?=.*" + _any_of(SOCKET_POKE) + r")(?=.*" + _any_of(SOCKET_OBJECT) + r")"
    r"(?=.*" + _any_of(SOCKET_WORD) + r")",
)
SOCKET_COVER = _both(
    (r"\b(?:child\s?proof\w*|child\s?safe\w*|baby\s?proof\w*|blanking\s+plugs?|"
     r"socket\s+covers?|covers?\s+(?:for|on)\s+(?:the\s+)?sockets?)\b",),
    SOCKET_WORD,
)
ELECTRIC_SHOCK_WIRED = (
    r"\b(?:socket|plug|wire|cable|lead|mains|fuse\s?box|kettle|charger|voltage|live\s+wire)\b",
)
ELECTRIC_SHOCK_DEATH = (
    r"\b(?:died|killed|dead|fatal|didn'?t\s+make\s+it|did\s+not\s+make\s+it|pronounced|"
    r"passed\s+(?:away|on)|lost\s+(?:him|her|them))\b",
)
ELECTRIC_SHOCK_STATIC = (
    r"\b(?:static|car\s+door|door\s?handle|door\s?knob|trolley|handrail|blanket|jumper|"
    r"fleece|carpet|metal\s+pole|the\s+dog|the\s+cat|shelf)\b",
)
ELECTRIC_SHOCK_FLOOR = (
    r"\b(?:passed\s+out|passing\s+out|out\s+cold|knocked\s+out|collaps\w*|fainted|fainting|"
    r"unconscious|unresponsive|blacked\s+out|keeled\s+over|in\s+a\s+heap|went\s+limp)\b",
)
ELECTRIC_SHOCK_FLOOR_LINE = _both(SHOCK_ANY, ELECTRIC_SHOCK_FLOOR)
ELECTRIC_SHOCK_NOT_ELECTRIC = (
    r"\b(?:crash|collision|accident|news|phone\s*call|grief|bereave\w*|funeral|diagnosis|"
    r"test\s+results|results|letter|bill|price|quote|scare|scared|fright|surprise|"
    r"jump\s*scare)\b",
)
ELECTRIC_SHOCK_SUPPLY = (
    r"\b(?:electric\w*|electrocut\w*|socket|plug|wire|cable|lead|mains|voltage|volt\w*|fuse|"
    r"power|pylon|substation|zapped|battery|charger|live|shorted?|shorts)\b",
)
ELECTRIC_SHOCK_NEARLY = (
    r"\b(?:nearly|almost|close\s+to|thought\s+(?:i|he|she|they)\s+(?:was|were)\s+(?:going\s+to|"
    r"about\s+to)|felt\s+like\s+(?:i|he|she|they)\s+(?:was|were)\s+(?:going\s+to|about\s+to)|"
    r"could\s+have)\b",
)
ELECTRIC_SHOCK_CPR = (
    r"\b(?:not|isn'?t|isnt|wasn'?t|wasnt|stopped|won'?t|wont)\s+breath\w*\b",
    r"\bno\s+(?:pulse|heartbeat)\b",
    r"\b(?:cpr|resuscitat\w*)\b",
)
ELECTRIC_SHOCK_STORY = (
    r"\b(?:years?\s+ago|last\s+year|when\s+(?:he|she|they|i)\s+was\s+(?:a\s+)?(?:kid|child|"
    r"young|little|small)|as\s+a\s+(?:kid|child)|back\s+in\s+\d{4}|decades?\s+ago)\b",
)
PREGNANCY_BP = (
    NOT_PREG + r"(?=.*\b" + PREGNANCY_WORDS + r"\b)"
    r"(?=.*\b(?:bad|really\s+bad|severe|worst|pounding|splitting|banging)\s+headache\b)",
    NOT_PREG + r"(?=.*\b" + PREGNANCY_WORDS + r"\b)(?=.*\bheadache\b)"
    r"(?=.*\b(?:blurr\w*|vision|double\s+vision|flashing\s+lights|seeing\s+(?:spots|stars)|"
    r"lights?\s+in\s+front\s+of\s+my\s+eyes)\b)",
    NOT_PREG + r"(?=.*\b" + PREGNANCY_WORDS + r"\b)"
    r"(?=.*\b(?:blurr\w*\s+vision|double\s+vision|flashing\s+lights|seeing\s+spots|"
    r"vision\s+(?:is\s+)?(?:blurr\w*|funny|odd|going))\b)",
    NOT_PREG + r"(?=.*\b" + PREGNANCY_WORDS + r"\b)"
    r"(?=.*\b(?:swell\w*|swoll\w*|puffy|puffiness|puff\w*\s+up)\b.{0,25}"
    r"\b(?:face|hands|hand|fingers|arm|arms)\b)",
    NOT_PREG + r"(?=.*\b" + PREGNANCY_WORDS + r"\b)"
    r"(?=.*\b(?:face|hands|hand|fingers|arm|arms)\b.{0,25}"
    r"\b(?:swell\w*|swoll\w*|puffy|puffiness|puff\w*\s+up)\b)",
)
POO_PANTS = (
    r"\b(?:pants|underwear|knickers|boxers|boxer\s+shorts|briefs|drawers|undies|pyjamas?)\b",
)
POO_WORD = (
    r"\b(?:poo|poos|pooed|poop|pooped|stool|stools|shit|shitted|bowel\s+movement|number\s+two|"
    r"faeces|feces|diarrhoea|diarrhea)\b",
)
POO_MEAL = (
    r"\b(?:after|from|because\s+of)\s+(?:a\s+|the\s+|some\s+)?(?:curry|spicy\s+\w+|takeaway|"
    r"take-?out|kebab|chilli|chili|indian|mexican|thai|hot\s+sauce|tabasco|jalape\w+|"
    r"peri\s+peri|piri\s+piri|nando'?s|pizza|beetroot|beet\s+juice)\b",
)
POO_RED = (
    r"\b(?:faint|fainted|dizzy|light-?headed|pale|grey|gray|clammy|weak|shaking|sweating|"
    r"heavy|heavier|a\s+lot|lots\s+of|pouring|clots?|clotted|gushing|soaked|soaking|can'?t\s+stand|"
    r"passed\s+out)\b",
)

TORSION_HARD = (
    r"\b(?:swollen|swelling|swoll|hard|firm|twisted|torsion|high\s+up|retracted)\b",
)
TORSION_SICK = (
    r"\b(?:feel|feeling|be|being|been|am|im|is|was)\s+(?:really\s+|very\s+|so\s+)?sick\b",
    r"\bvomit\w*|throwing\s+up|thrown\s+up|nausea\w*",
)
TORSION_MILD = (
    r"\b(?:a\s+bit|a\s+little|slightly|mild|bit\s+of|sort\s+of|kind\s+of)\b",
)
TORSION_LONG = (
    r"\b(?:for\s+(?:a\s+|the\s+last\s+|about\s+a\s+|over\s+a\s+)?(?:\d+\s+)?(?:days?|weeks?|"
    r"months?|years?)|since\s+(?:last\s+year|christmas|the\s+summer)|weeks\s+now|months\s+now|"
    r"years\s+now|a\s+while\s+now|ages)\b",
)
TORSION_RED = (
    r"\b(?:severe|unbearable|agony|excruciating|worse|getting\s+worse|vomit\w*|being\s+sick|"
    r"throwing\s+up|fever|temperature|hard|firm|discolou?red|purple|black|blue\s+and|twisted)\b",
)
PUNCTURE_OFF = (
    r"\b(?:tyre|tire|wall|hammer|picture|shelf|fence|hanging|lego|block|bike|car|laptop|"
    r"shoe\s+rack|nail\s+varnish|fingernail|toenail|carpet)\b",
    r"\bhit\s+the\s+nail\b",
)
APPENDIX = (
    r"\bappendix\b[^.?!]{0,30}\b(?:burst|bursting|ruptured|rupturing|has\s+gone|gone)\b",
    r"\b(?:burst|bursting|ruptured|rupturing)\s+(?:my\s+|his\s+|her\s+|their\s+)?appendix\b",
    r"\bappendicitis\b[^.?!]{0,25}\b(?:burst|ruptured)\b",
)
BABY_FELL_OVER = (
    r"\bfell\s+over\b(?!\s+(?:and|then|onto|off|from|down|hitting|banging|cutting))",
)

HANGED_DONE = (
    r"\b(?:hung|hanged)\s+(?:him|her|them)sel(?:f|ves)\b",
)
ELDER_KIN = (
    r"\b(?:nan|nana|gran|granny|grandma|grandmother|grandad|granddad|grandpa|grandfather)\b",
)
DEATH_SAID = (
    r"\b(?:died|dead|death|funeral|buried|burial|passed\s+away|cremat\w*|inquest|grave|"
    r"anniversary|memorial|headstone)\b",
)
SCHOOL_PLACE = (
    r"\bat\s+(?:school|uni|university|college|sixth\s+form)\b",
)
YOUNG_KIN = (
    r"\b(?:son|daughter|child|kid|boy|girl|baby|toddler|teen|teenager|stepson|stepdaughter|"
    r"grandson|granddaughter|nephew|niece)\b",
)
_STRUCK_VEHICLE = (r"(?:car|cars|van|vans|lorry|lorries|truck|trucks|bus|buses|coach|taxi|cab|"
                   r"bike|bikes|bicycle|motorbike|motorcycle|scooter|moped|tram|train|tractor|"
                   r"digger|forklift|police\s+car|fire\s+engine)")


_STRUCK_PERSON = (r"(?:i|me|he|him|she|her|they|them|us|we|someone|somebody"
                  r"|(?:my|his|her|their|our|the|your|a|an|some)\s+" + _STRUCK_RELATIVE +
                  r"|" + _STRUCK_RELATIVE + r")")

_STRUCK_VERB = (r"(?:hit|hits|hitting|struck|strikes|knocked\s+(?:down|over)"
                r"|knocks\s+(?:down|over)|ran\s+over|run\s+over|runs\s+over|clipped|clips"
                r"|mowed\s+down|collided\s+with)")

NEAR_HIT_ON_A_ROAD_NOT = (r"\b(?:my|his|her|our|their|your)\s+" + _STRUCK_RELATIVE + r"\b",)

_STRUCK_BODY = (r"(?:my|his|her|their|our|your)\s+"
                r"(?:foot|feet|leg|legs|hand|hands|arm|arms|toe|toes|ankle|ankles|knee|knees)")

_STRUCK_RUN_OVER = (r"\b" + _STRUCK_PERSON + r"\b[^.?!]{0,20}\b"
                    r"(?:got|get|gets|was|were|is|are|been|had\s+been|has\s+been|just|suddenly)?\s*"
                    r"(?:run|ran|runs)\s+over\b"
                    r"(?!\s+(?:the|a|an|my|our|his|her|their|your|some|any|it|this|that|to)\b)")

_STRUCK_PET = (r"\b(?:my|our|the|his|her|their)\s+(?:dog|dogs|puppy|cat|cats|kitten|rabbit|horse|"
               r"pony|hamster|parrot|budgie|guinea\s+pig)\b")

STRUCK_BY_VEHICLE = (
    r"\b" + _STRUCK_PERSON + r"\b[^.?!]{0,25}\b" + _STRUCK_VERB + r"\s+by\s+(?:a\s+|an\s+|"
    r"the\s+|his\s+|her\s+|their\s+|my\s+|our\s+|your\s+)?" + _STRUCK_VEHICLE +
    r"\b(?!\s+door)",
    r"\b(?:a|an|the|some|one|his|her|their|my|our)\s+" + _STRUCK_VEHICLE + r"\b[^.?!]{0,20}\b"
    r"(?:hit|hits|struck|strikes|clipped|clips)\s+" + _STRUCK_PERSON + r"\b",
    r"\b(?:a|an|the|some|one|his|her|their|my|our)\s+" + _STRUCK_VEHICLE + r"\b[^.?!]{0,20}\b"
    r"(?:knocked|knocks|ran|run|runs|mowed)\s+" + _STRUCK_PERSON + r"\s+(?:down|over)\b",
    r"\b(?:a|an|the|some|one|his|her|their|my|our)\s+" + _STRUCK_VEHICLE + r"\b[^.?!]{0,20}\b"
    r"(?:ran|run|runs)\s+over\s+(?:" + _STRUCK_PERSON + r"|" + _STRUCK_BODY + r")\b",
    _STRUCK_RUN_OVER,
    r"\b" + _STRUCK_PET + r"\b[^.?!]{0,25}\b(?:got|get|gets|was|were|is|are|been)?\s*"
    r"(?:run|ran|runs)\s+over\b"
    r"(?!\s+(?:the|a|an|my|our|his|her|their|your|some|any|it|this|that|to)\b)",
    r"\b(?:a|an|the|some|one)\s+" + _STRUCK_VEHICLE + r"\b[^.?!]{0,20}\b"
    r"(?:ran|run|runs)\s+over\s+" + _STRUCK_PET + r"\b",
    r"\b" + _STRUCK_PERSON + r"\b[^.?!]{0,14}\b(?:went|go|goes|going|gone|fell|falls|falling|"
    r"ended\s+up|slid)\b[^.?!]{0,12}\bunder\s+(?:a|an|the)\s+" + _STRUCK_VEHICLE + r"\b",
    r"\b(?:someone|somebody|he|she|they|(?:a|an|the|some|one)\s+(?:driver|man|woman|lad|lass|"
    r"boy|girl|fella|feller|chap|guy|bloke|person|van|car|lorry|truck|bus|coach|taxi|cab|"
    r"motorbike|motorcycle|scooter|bike|bicycle))\b"
    r"[^.?!]{0,10}\b(?:ran|run|runs)\s+" + _STRUCK_PERSON + r"\s+(?:over|down)\b",
    r"\b" + _STRUCK_PERSON + r"\b[^.?!]{0,20}\b(?:got|get|gets|was|were|been)?\s*"
    r"(?:mowed|mown|mow)\b[^.?!]{0,10}\bdown\b",
    r"\b" + _STRUCK_PERSON + r"\b[^.?!]{0,14}\b(?:got|get|gets|was|were|been)?\s*"
    r"(?:knocked|knocks)\s+off\s+(?:my|his|her|their|our|your)\s+"
    r"(?:bike|bicycle|motorbike|motorcycle|scooter|moped)\b",
    r"\b" + _STRUCK_BODY + r"\b[^.?!]{0,20}\b(?:was|were|got|get|gets|been|is|are)\s*"
    r"(?:run|ran|runs)\s+over\s+by\s+(?:a\s+|an\s+|the\s+)?" + _STRUCK_VEHICLE + r"\b",
    r"\b" + _STRUCK_PERSON + r"\b[^.?!]{0,20}\b(?:knocked|knocks|shoved|shunt(?:ed|s)?|"
    r"sent|sends)\s+off\s+(?:\w+\s+)?(?:bike|bicycle|motorbike|motorcycle|scooter|moped)\b"
    r"[^.?!]{0,12}\bby\s+(?:a\s+|an\s+|the\s+|his\s+|her\s+|their\s+|my\s+|our\s+|your\s+)?"
    + _STRUCK_VEHICLE + r"\b",
    r"\b(?:a|an|the|some|one|his|her|their|my|our)\s+" + _STRUCK_VEHICLE + r"\b[^.?!]{0,20}\b"
    r"(?:knocked|knocks|shoved|shunt(?:ed|s)?|sent|sends)\s+" + _STRUCK_PERSON + r"\s+off\s+"
    r"(?:\w+\s+)?(?:bike|bicycle|motorbike|motorcycle|scooter|moped)\b",
    r"\b(?:a|an|the|some|one|another|his|her|their|my|our)\s+" + _STRUCK_VEHICLE +
    r"\b[^.?!]{0,20}\b(?:drove|drives|drive|rammed|rams|crashed|went|goes|go|ploughed|ploughs|"
    r"plowed|plows|smashed|smashes)\s+into\s+" + _STRUCK_PERSON + r"\b",
    r"\b(?:someone|somebody|a\s+driver|the\s+driver)\s+(?:drove|drives|drive|rammed|rams|"
    r"crashed)\s+into\s+" + _STRUCK_PERSON + r"\b",
)


STRUCK_HYPOTHETICAL = (
    r"\bwhat\s+(?:should|do|can|would)\s+(?:i|we|you)\s+do\s+if\b",
    r"\bwhat\s+(?:happens|would\s+happen|will\s+happen)\s+if\b",
    r"\bwhat\s+if\b",
)

_TRAPPED_VEHICLE_NOUN = (r"(?:car|van|lorry|truck|vehicle|wreck|taxi|cab|bus|coach|tractor|"
                         r"digger|forklift|train|tram)")
_TRAPPED_VEHICLE_NOT = (r"(?!\s+(?:door|doors|seat|seats|park|wash|boot|lot|key|keys|lock|"
                        r"mirror|radio))")
_TRAPPED_PERSON = (r"(?:" + _STRUCK_PERSON + r"|hes|shes|theyre|he['\u2019]s|she['\u2019]s|"
                   r"they['\u2019]re|kids|children|(?:the|my|our)\s+(?:kids|children|little\s+"
                   r"(?:one|boy|girl)))")
_TRAPPED_BODY = (r"(?:leg|legs|arm|arms|foot|feet|hand|hands|body|torso|chest|hip|hips|waist|head|"
                 r"neck|ankle|ankles|wrist|wrists|shoulder|shoulders|ribs|pelvis|back)")
_TRAPPED_BODY_OWNER = (r"(?:my|his|her|their|our|your)\s+(?:\w+['\u2019]?s\s+)?" + _TRAPPED_BODY)
_TRAPPED_STATE = (r"(?:trapped|pinned|wedged|crushed|stuck)")
_TRAPPED_LOCKED = (r"(?:locked|shut)\s+(?:in|inside)")
TRAPPED_VEHICLE = (
    r"\b" + _TRAPPED_PERSON + r"\b[^.?!]{0,15}\b(?:\w+\s+){0,2}?"
    r"(?:" + _TRAPPED_STATE + r"\b[^.?!]{0,12}\b(?:in|inside|under|beneath)|"
    r"" + _TRAPPED_LOCKED + r")\b[^.?!]{0,10}\b(?:the\s+|a\s+|an\s+|his\s+|her\s+|"
    r"their\s+|our\s+|my\s+)?" + _TRAPPED_VEHICLE_NOUN + r"\b" + _TRAPPED_VEHICLE_NOT,
    r"\b" + _TRAPPED_BODY_OWNER + r"[^.?!]{0,15}\b(?:trapped|pinned|wedged|crushed|"
    r"stuck|caught)\b"
    r"[^.?!]{0,12}\b(?:in|inside|under|beneath)\b[^.?!]{0,10}\b(?:the\s+|a\s+|an\s+)?"
    + _TRAPPED_VEHICLE_NOUN + r"\b" + _TRAPPED_VEHICLE_NOT,
    r"\b(?:the|a|an|his|her|their|our|my)\s+" + _TRAPPED_VEHICLE_NOUN +
    r"\b[^.?!]{0,20}\b" + _TRAPPED_STATE + r"\b[^.?!]{0,12}\b(?:"
    + _TRAPPED_PERSON + r"|" + _TRAPPED_BODY_OWNER + r")\b",
    r"(?=[^.?!]*\b(?:crash(?:ed|es|ing)?|ditch|wreck(?:ed)?|rolled|overturn(?:ed)?|flipped|"
    r"skidded|collision|hit\s+(?:a|the)\s+(?:tree|wall|lamp\s*post|post|barrier|railing|"
    r"bridge))\b)"
    r"[^.?!]*\b" + _TRAPPED_PERSON + r"\b[^.?!]{0,25}\b(?:" + _TRAPPED_STATE + r"|"
    + _TRAPPED_LOCKED + r")\b",
)
TRAPPED_SELF_STUCK = re.compile(
    r"\b(?:im|i\s+am|i['\u2019]m|we['\u2019]re|we\s+are)\b[^.?!]{0,20}\bstuck\b")
TRAPPED_NOT_A_WAIT = re.compile(
    r"\b(?:wreck|wrecked|upside\s+down|on\s+its\s+(?:side|roof)|rolled|overturned|flipped|"
    r"ditch|hot|heat|sun|stifling|no\s+air|fire|smoke|flames|engine\s+(?:is\s+)?running|"
    r"can'?t\s+get\s+out|locked\s+in)\b")


SHAKE_WISH = (
    r"\b(?:feel\s+like|felt\s+like|want\s+to|wanted\s+to|going\s+to|about\s+to|nearly|"
    r"close\s+to|tempted\s+to|might|i\s+could|afraid|scared|"
    r"(?:keep\s+)?think(?:ing)?\s+about|thought\s+about|have\s+thought\s+about|"
    r"keep\s+wanting)\b[^.?!]{0,30}"
    r"\b(?:shak(?:e|es|ing)|shook|hurt|hurting|hit|hitting|thump(?:ing)?|smack(?:ing)?)\b"
    r"[^.?!]{0,26}\b(?:him|her|them|the\s+baby|my\s+(?:son|daughter)|the\s+little\s+one)\b",
)
SHAKE_CHILD_CONTEXT = (
    r"\b(?:baby|babies|newborn|toddler|the\s+little\s+one|my\s+(?:son|daughter|baby|girl|boy)|"
    r"put\s+(?:her|him|them)\s+down|napp(?:y|ies)|night\s+feeds?|feeding|"
    r"bottle|pram|cot|moses\s+basket|first\s+tooth|sleep\s+(?:regression|training))\b",
    r"\b(?:cr(?:y|ies|ied|ying)|scream\w*|wont\s+sleep|won'?t\s+sleep|up\s+all\s+night|"
    r"will\s+not\s+sleep|teething|colic|colicky)\b",
)
SHAKE_COPING = (
    r"\b(?:can'?t\s+do\s+this|cant\s+do\s+this|can'?t\s+cope|not\s+coping|no\s+sleep|"
    r"havent\s+slept|haven'?t\s+slept|not\s+slept|exhausted|so\s+tired|knackered|"
    r"breaking\s+point|at\s+the\s+end\s+of\s+(?:it|my\s+tether)|desperate|nothing\s+works|"
    r"nothing\s+helps|"
    r"(?:dont|don'?t)\s+know\s+how\s+much\s+longer)\b",
)
SHAKE_ADULT = (
    r"\bmy\s+(?:husband|wife|partner|boyfriend|girlfriend|ex|boss|manager|mum|dad|mother|"
    r"father|sister|brother|nan|grandad|grandma|friend|mate|neighbour|colleague)\b",
)
SHAKE_CHILD = SHAKE_WISH
SHAKE_IDIOM = (
    r"\b(?:shake|shaking|shook)\s+(?:my|your|his|her)\s+head\b",
    r"\b(?:shake|shaking)\s+hands?\b",
    r"\b(?:shake\s+it\s+off|shake\s+things\s+up|shake\s+up)\b",
    r"\bmilk\s*shake\b",
    r"\bshak(?:e|ing)\s+with\s+(?:cold|laughter|laughing|fear|nerves)\b",
    r"\bshak(?:e|ing)\s+some\s+sense\b",
)
SHAKE_REPLY = (
    "Put the baby down somewhere safe - on their back in the cot, even if they are crying - and "
    "step out of the room for a minute. Never shake a baby, however long it has gone on: put them "
    "down and ring someone who can take over, Cry-sis on 0800 448 0737, or 111 if you are scared "
    "of how you feel.",
    "That is the moment to put the baby down and walk away, not to carry it through: on their back "
    "in the cot, door shut, two minutes in another room. Shaking a baby hurts them for life. Ring "
    "Cry-sis on 0800 448 0737, or 111 tonight, and say out loud that you are at the end of it.",
)
SHAKE_BABY_WORD = (
    r"\b(?:baby|babies|newborn|new\s*born|cot|crib|napp(?:y|ies)|feeding|feeds?|bottle|pram|"
    r"teething|colic|colicky)\b",
    r"\bput\s+(?:her|him|them)\s+down\b",
)
SHAKE_CHILD_REPLY = (
    "Put them down somewhere safe and step out of the room for a minute - they can cry for two "
    "minutes and come to no harm. Never shake or hit a child, however long it has gone on: put "
    "them down and ring someone who can take over. Cry-sis on 0800 448 0737 is for exactly this, "
    "and 111 if you are scared of how you feel.",
    "That is the moment to put them down and walk away, not to carry it through: somewhere safe, "
    "the door shut, two minutes in another room. Shaking or hitting a child hurts them for life. "
    "Ring someone who can take over tonight - Cry-sis on 0800 448 0737 - and say out loud that you "
    "are at the end of it.",
)
OUT_COLD_LONG = (
    r"\bout\s+cold\b[^.?!]{0,24}(?:\b(?:all\s+night|the\s+(?:whole|entire)\s+night|"
    r"for\s+(?:hours|ages))\b|until\s+\d|later\s+that\s+(?:morning|afternoon|evening)|"
    r"until\s+(?:the\s+|that\s+)?(?:morning|afternoon|evening|lunchtime|midday|dawn|"
    r"dusk|nightfall))",
)
OUT_COLD_FOUND = (
    r"\bfound\s+(?:me|him|her|them)\b",
    r"\b(?:couldn'?t|couldnt|could\s+not)\s+wake\b",
    r"\bno\s+idea\s+(?:how\s+long|what\s+happened)\b",
    r"\bcouldn'?t\s+get\s+(?:him|her|them)\s+up\b",
    r"\bwoke\s+up\s+(?:on\s+the|in\s+the)\b",
)
OUT_COLD_LEFT_TO_OTHERS = (
    r"\b(?:can'?t|cant|couldn'?t|couldnt)\s+wake\b",
    r"\bnot\s+breathing\b",
    r"\bno\s+pulse\b",
    r"\bstill\s+(?:not\s+woken|out|unconscious|asleep)\b",
)
OUT_COLD_SLEEPY = (
    r"\b(?:party|night\s+shift|night\s+out|long\s+day|shift|walk|run|hike|gig|flight|"
    r"jet\s?lag|dinner|meal|feed|bottle|nap|bed|bedtime|asleep|sleep\w*|exhaust\w*|tired|"
    r"knackered|drunk|pints|beers?|wine)\b",
)
OUT_COLD_NIGHT_REPLY = (
    "That is not a sleep - being out cold that long needs 999 or 911 now, or straight to A&E if "
    "they are awake and you can get them there. Say how long it went on and whether they came "
    "round by themselves, and do not leave them alone until someone has seen them.",
    "Ring 999 or 911 now: nobody is out cold for a night and fine. Tell them how long it lasted and "
    "anything before it - a bang on the head, a drink, a medicine - and stay with them until help "
    "comes.",
)
ABUSE_OBJECTS = (
    r"\b(?:throw(?:s|ing)?|threw|thrown|smash(?:es|ing|ed)?|break(?:s|ing)?|broke|"
    r"punch(?:es|ing|ed)?|kick(?:s|ing|ed)?|trash(?:es|ing|ed)?|wreck(?:s|ing|ed)?)\b"
    r"[^.?!]{0,30}\b(?:things|stuff|plates|glasses|crockery|furniture|chairs?|doors?|walls?|"
    r"windows?|the\s+(?:house|flat|place)|"
    r"my\s+(?:things|stuff|house|flat|home|place|room|kitchen|bedroom|living\s+room|car))\b",
)
ABUSE_OBJECTS_PERSON = (
    r"\b(?:he|she|they|hes|shes|theyre|husband|wife|partner|boyfriend|girlfriend|ex|dad|mum|"
    r"father|mother|stepdad|stepmum|grandma|grandpa|nan|grandad|flatmate|housemate|brother|"
    r"sister|carer)\b",
)
ABUSE_OBJECTS_OFF = (
    r"\bthrowing\s+(?:things|stuff)\s+(?:away|out|in\s+the\s+bin)\b",
    r"\bthrew\s+my\s+back\s+out\b",
    r"\bbreak(?:ing)?\s+things\s+off\b",
    r"\b(?:baby|babies|toddler|toddlers|kids?|children|child)\b[^.?!]{0,24}"
    r"\b(?:throw|throws|throwing|smash|smashing|broke|breaking)\b",
    r"\b(?:throwing|smashing|punching)\s+(?:things|stuff|plates)\s+(?:at|in)\s+"
    r"(?:the\s+)?(?:park|garden|playground|soft\s+play|bouncy\s+castle)\b",
    r"\b(?:in\s+a\s+(?:film|movie|game|show)|on\s+telly|in\s+the\s+film)\b",
)
CASES = (
    ("pregnancy_bleed", PREGNANCY_BLEED, False),
    ("pregnancy_quiet", PREGNANCY_QUIET, False),
    ("pregnancy_bp", PREGNANCY_BP, False),
    ("pregnancy_waters", PREGNANCY_WATERS, False),
    ("electric_shock_floor", ELECTRIC_SHOCK_FLOOR_LINE, False),
    ("electric_shock", ELECTRIC_SHOCK, False),
    ("socket_thing", SOCKET_THING + SOCKET_COVER, False),
    ("pregnancy_sick", PREGNANCY_SICK, False),
    ("pregnancy_sick_q", PREGNANCY_SICK_Q, False),
    ("self_harm", SELF_HARM, True),
    ("hanging", HANGING, True),
    ("abuse", ABUSE, False),
    ("shot", SHOT, False),
    ("eye_chem", EYE_CHEM, False),
    ("heard_assault", HEARD_ASSAULT, False),
    ("allergy_now", ALLERGY_NOW, False),
    ("lips_swell", LIPS_SWELL, False),
    ("lips_swell_bare", LIPS_SWELL_BARE, False),
    ("lips_tingle", LIPS_TINGLE, False),
    ("allergy_food", ALLERGY_FOOD, False),
    ("throat_tight", THROAT_TIGHT, False),
    ("swallow_gone", SWALLOW_GONE, False),
    ("bone_out", BONE_OUT, False),
    ("headache", HEADACHE, False),
    ("cough_blood", COUGH_BLOOD, False),
    ("vomit_blood", VOMIT_BLOOD, False),
    ("poo_black", POO_BLACK, False),
    ("poo_blood", POO_BLOOD, False),
    ("torsion", TORSION, False),
    ("unsafe", UNSAFE, False),
    ("intruder", INTRUDER, False),
    ("insect_bite", INSECT_BITE, False),
    ("tick_bite", TICK_BITE, False),
    ("bat_bite", BAT_BITE, False),
    ("wild_bite", WILD_BITE, False),
    ("dog_bite", BITE_DONE, False),
    ("dog_attack", DOG_ATTACK, False),
    ("clothes_fire", CLOTHES_FIRE, False),
    ("pan_fire", PAN_FIRE, False),
    ("vehicle_fire", VEHICLE_FIRE, False),
    ("fire", FIRE, False),
    ("battery_fire", BATTERY_FIRE, False),
    ("battery_bulge", BATTERY_BULGE, False),
    ("electric_burn", ELECTRIC_BURN, False),
    ("gas_left", GAS_LEFT_ON, False),
    ("gas_smell", GAS_SMELL, False),
    ("bleach_mix_q", BLEACH_MIX_Q, False),
    ("bleach_mix", BLEACH_MIX, False),
    ("co_signs", CO_SIGNS, False),
    ("co_going_off", CO_GOING_OFF, False),
    ("co_leak", CO_LEAK, False),
    ("co_place", CO_PLACE, False),
    ("co_test", CO_TEST, False),
    ("co_fact", CO_FACT, False),
    ("bone_throat", BONE_THROAT, False),
    ("object_in_head", OBJECT_IN_HEAD, False),
    ("dose_stated", DOSE_STATED + DOSE_DOUBLE + DOSE_RECENT + DOSE_WHOLE_PACK, False),
    ("swallowed_thing", SWALLOWED_THING, False),
    ("mild_swallowed", MILD_SWALLOWED, False),
    ("foraged", FORAGED_EATEN, False),
    ("poison", POISON, False),
    ("swallowed_ordinary", SWALLOWED_ORDINARY, False),
    ("spiked", SPIKED, False),
    ("co_mention", CO_MENTION, False),
    ("fall_hip", FALL_HIP, False),
    ("crush", CRUSH, False),
    ("fall", FALL, False),
    ("puncture", PUNCTURE, False),
    ("appendix", APPENDIX, False),
    ("old_fall", OLD_DOWN, False),
    ("fall_check", FALL_CHECK, False),
    ("bleeding", BLEEDING, False),
    ("struck_by_vehicle", STRUCK_BY_VEHICLE, False),
    ("trapped_vehicle", TRAPPED_VEHICLE, False),
    ("stuck_machine", STUCK_MACHINE, False),
    ("dental_numb", DENTAL_NUMB, False),
    ("slur_small_child", SLUR_SMALL_CHILD, False),
    ("slur_drink", SLUR_DRINK, False),
    ("stroke", STROKE + STROKE_WEAK, False),
    ("wound_streak_fever", WOUND_STREAK_FEVER, False),
    ("wound_streak", WOUND_STREAK, False),
    ("arm_numb", LEFT_ARM_NUMB, False),
    ("chest", CHEST + CHEST_ADJ + CHEST_SORE_MOVE, False),
    ("stroke", STROKE_FAST, False),
    ("breath_rest", BREATH_REST, False),
    ("breathing", BREATHING, False),
    ("night_breath", NIGHT_BREATH, False),
    ("breath_past", BREATH_PAST, False),
    ("blue", BLUE, False),
    ("floppy_child", FLOPPY_CHILD, False),
    ("blackout", BLACKOUT_RED_LINE, False),
    ("unconscious", UNCONSCIOUS + WAKE_UP_SOMEONE + WONT_COME_ROUND + HARD_TO_WAKE, False),
    ("seizure", SEIZURE, False),
    ("drowning", DROWNING, False),
    ("heat", HEAT, False),
    ("scald", SCALD, False),
    ("red_flags", RASH_RED, False),
    ("stiff_neck", STIFF_NECK_RED, False),
    ("sepsis_signs", SEPSIS, False),
    ("pale_child", PALE_CHILD, False),
    ("pale_adult", PALE_ADULT, False),
    ("newborn_fever", NEWBORN_TEMP, False),
    ("newborn_fever_next", NEWBORN_NEXT, False),
    ("named_illness", NAMED_ILLNESS_CHILD, False),
    ("high_temp", HIGH_TEMP_CHILD, False),
    ("child_drank", CHILD_DRANK, False),
    ("recent_fit", RECENT_FIT, False),
    ("grunting_baby", GRUNTING_BABY, False),
    ("sleepy_feed", SLEEPY_FEED, False),
    ("rash_headache", RASH_HEADACHE, False),
    ("fever_rash", FEVER_RASH, False),
    ("child_fever", CHILD_FEVER, False),
    ("baby_fell", BABY_FELL, False),
)

FAINT_WITH_A_BANG = FAINT_STORY + (
    r"\bcame\s+(?:over|round)\b[^.?!]{0,20}\b(?:funny|queer|faint|on\s+the\s+floor)\b",
)


def _fainted_with_the_bang(line):
    if _matches(FAINT_WITH_A_BANG, line):
        return True
    return any(re.search(shape, line) for shape, _needs_person in BLACKED_OUT_SIGHT)
PAST_BLACKOUT_REPLY = (
    "Worth mentioning to your GP: passing out is looked into even when it was a one-off, and they "
    "can check blood pressure, the heart and bloods. If it happens again, or they are hard to wake "
    "or fitting, that is an ambulance and not a wait."
)
OUT_COLD_NOW = (
    r"\b(?:is|'s|are|'re|still)\s+(?:\w+\s+){0,2}out\s+cold\b",
    r"\bout\s+cold\b[^.?!]{0,12}\b(?:right\s+now|now|at\s+the\s+moment)\b",
)
OUT_COLD_WONT_WAKE = (
    r"\b(?:won'?t|wont|wouldn'?t|wouldnt|didn'?t|didnt|can'?t|cant|cannot|isn'?t|isnt|not)\s+"
    r"(?:wake|waking|rouse|come\s+round|coming\s+round|respond|responding)\b",
    r"\bunresponsive\b", r"\bnot\s+responding\b", r"\bout\s+of\s+it\b",
)
PAST_FIT_WEEK_REPLY = (
    "A fit a week ago still needs looking at today rather than waiting: ring 111 or the GP surgery "
    "and say when it happened and what it looked like. If another one starts and does not stop, "
    "that is an ambulance: on the floor on one side, nothing in the mouth."
)
PAST_FIT_REPLY = (
    "Mention that to your GP: a fit is looked into even when it only happened once, and they can "
    "say whether it needs any tests. If one happens again and does not stop, that is an ambulance: "
    "on the floor on one side, nothing in the mouth."
)
def _effort_recovery(line):
    return (_matches(EXERTION_CLASS + BREATH_EFFORT + EXERTION, line)
            and _matches(EFFORT_RECOVERY, line)
            and not _matches(BREATH_RED + EFFORT_MORE_RED, line)
            and not _matches(NOT_A_BREATHER + PET_WORDS, line)
            and not _matches(EFFORT_TOO_LONG, line)
            and not _matches(EFFORT_SOMEONE_ELSE, line)
            and not _matches((r"\bstill\b", r"\bright\s+now\b"), line))


WITHDRAWAL_LONG_AGO = (
    r"\b(?:\d+|two|three|four|five|six|seven|eight|nine|ten|tin|twenty|thirty|many|several|"
    r"a\s+few)\s+years?\s+ago\b",
    r"\byears\s+ago\b", r"\bmonths\s+ago\b", r"\blast\s+year\b", r"\bdecades?\b",
)
WITHDRAWAL_SOBER = (
    r"\b(?:\d+|a|an|one|two|three|four|five|six|seven|eight|nine|ten|a\s+few|several|couple\s+of)"
    r"\s+(?:hours?|days?|weeks?|months?)\s+(?:sober|dry|off\s+it|alcohol[-\s]?free|"
    r"without\s+a\s+drink|with\s+no\s+booze)\b",
)
WITHDRAWAL_COLD_TURKEY = (
    r"\b(?:stop(?:ped|ping)?|quit(?:ting)?|come|coming|came|get|getting|got|went|going|go|"
    r"gave\s+up|giving\s+up)\b[^.?!]{0,20}\bcold\s+turkey\b",
)
WITHDRAWAL_WEEKS = (
    r"\b(?:\d+|a|an|one|two|three|four|five|six|seven|eight|nine|ten|twelve|couple\s+of|"
    r"few)\s+(?:weeks?|months?)\b",
)
WITHDRAWAL_FINE = (
    r"\b(?:feel|feeling|felt)\s+(?:great|better|amazing|brilliant|fantastic|good|"
    r"so\s+much\s+better|loads\s+better)\b",
    r"\bnever\s+(?:felt|feel)\s+better\b", r"\bbest\s+(?:i'?ve|i\s+have)\s+felt\b",
)
PREGNANT_LINE = (
    r"\bpregnan\w*", r"\bexpecting\s+a\s+(?:baby|child)\b", r"\b\d+\s+weeks?\s+gone\b",
)
WITHDRAWAL_DURATION = (
    r"\bhow\s+long\b", r"\bhow\s+many\s+(?:days|hours|weeks)\b",
    r"\bwhen\s+(?:will|does|do|should)\b[^.?!]{0,30}\b(?:stop|end|ease|better|over|go\s+away)\b",
)
WITHDRAWAL_WORSE = (
    r"\bworse\b", r"\bgetting\s+worse\b", r"\bnot\s+stopping\b", r"\bcant\s+stop\b",
    r"\ball\s+night\b", r"\ball\s+day\b", r"\bunbearable\b",
    r"\bscared\b", r"\bterrified\b", r"\bfrightened\b",
)
WITHDRAWAL_BARE = (
    r"\bdetox\w*", r"\bwithdrawal\b", r"\b(?:went|going|go|gone)\s+cold\s+turkey\b",
)
WITHDRAWAL_BARE_BAD = (
    r"\b(?:bad|worse|awful|terrible|rough|hell|horrible|dreadful)\b",
    r"\b(?:cant|cannot|can'?t)\s+(?:sleep|eat|stop\s+shaking)\b",
)
WITHDRAWAL_SEVERE = (
    r"\bconfus\w*", r"\bhallucinat\w*",
    r"\bdelirium\b", r"\bfits?\b", r"\bseizures?\b", r"\bnot\s+making\s+sense\b",
    r"\bdon'?t\s+know\s+where\s+i\s+am\b", r"\bshaking\s+all\s+over\b", r"\bcan'?t\s+stand\b",
)


def _hallucinating(line):
    if not _matches(WITHDRAWAL_HALLUCINATION, line):
        return False
    return not _matches(WITHDRAWAL_SENSES_FINE, line)


def _severe(line):
    return _matches(WITHDRAWAL_SEVERE, line) or _hallucinating(line)
WITHDRAWAL_NOT_NOW = (
    r"\b(?:next\s+week|next\s+month|on\s+monday|on\s+tuesday|on\s+wednesday|on\s+thursday|"
    r"on\s+friday|on\s+saturday|on\s+sunday|in\s+the\s+new\s+year|for\s+dry\s+january|"
    r"dry\s+january|sober\s+october)\b",
)

from bot.knowledge.crisis_replies import REPLIES


HAIR_SCORCH_SKIN = (
    r"\b(?:red|raw|sore|blister\w*|peeled|peeling|swollen|swelling|weeping|white\s+patch|"
    r"burnt\s+skin|burned\s+skin)\b",
)


for _alias in ("stiff_neck", "sepsis_signs", "newborn_fever"):
    REPLIES[_alias] = REPLIES["red_flags"]

from bot.knowledge.crisis_replies import GENERAL



LIMP_NOT = ANIMAL + (
    r"\b(?:celery|lettuce|greens?|salad|spinach|cabbage|herbs?|leaves?|asparagus|spring\s+onions?|"
    r"hair|market|car|engine|economy)\b",
    r"\A\W*(?:(?:the|my|our|this|that|his|her|their|your)\s+)?(?:shed|fence|gates?|doors?|"
    r"hinges?|bikes?|wheels?|machines?|washing\s+machine|dishwasher|hoover|vacuum|laptops?|"
    r"phones?|screen|boards?|chairs?|tables?|sofas?|bench|pram|pushchair|buggy|trolley)\b",
    r"\b(?:prosthe\w*|artificial\s+(?:arm|arms|leg|legs|limb|limbs|hand|hands|foot|feet))"
    r"(?![^.]*\b(?:limp(?:s|ing|ed)?|gait|walk\s+with)\b)",
)


LIMP_CAUSE = (
    r"\bstroke\b", r"\bhip\s+replacement\b", r"\bknee\s+replacement\b",
    r"\b(?:hip|knee|joint)\s+(?:op|operation)\b",
    r"\breplacement\s+(?:hip|knee|joint)\b",
)
LIMP_REPLACED = (
    r"\b(?:hip|knee|joint)\s+replacement\b",
    r"\b(?:hip|knee|joint)\s+(?:op|operation)\b",
    r"\breplacement\s+(?:hip|knee|joint)\b",
)

RING_WORD = (r"\bring\b(?!\s*fingers?\b)", r"\brings\b(?!\s*fingers?\b)",
             r"\bwedding\s+ring\b", r"\bengagement\s+ring\b", r"\beternity\s+ring\b")
FINGER_SIDE = (r"\bfinger\b", r"\bfingers\b", r"\bknuckle\b", r"\bhand\b", r"\bhands\b")


PET_SIGHT = (
    r"\b(?:blind|going\s+blind|eyes?|sight|can'?t\s+see|cant\s+see|squint\w*|cataracts?)\b",
)
SUGAR_IN_A_RECIPE = (
    r"\b(?:biscuits?|cakes?|scones?|bread|loaves|loaf|pastry|batter|dough|mixture|icing|"
    r"frosting|jam|sauce|pudding|dessert|crumble|cereal|yogurt|yoghurt|porridge|muffins?|"
    r"cookies?|brownies?|flapjacks?|granola|smoothie|milk|squash|lemonade)\b",
)
LEG_WORDS = (
    r"\b(?:legs?|knees?|ankles?|feet|foot|hips?|thighs?|calves|calf|shins?|heels?|toes?)\b"
)


OWN_INJURY_SOMEONE_OR_A_STORY = (
    r"\b(?:someone|somebody|a\s+person|people|anyone|everyone|your\s+friend)\b",
    r"\bfor\s+(?:a|my|the)\s+(?:story|novel|book|film|script|screenplay|essay|assignment)\b",
    r"\bin\s+(?:a|my|the)\s+(?:story|novel|book|film|game|dream)\b",
)
OWN_INJURY_YOU = (r"\byou\b", r"\byour\b")
OWN_INJURY_OTHER_PERSON = (
    r"\b(?:my|our)\s+(?:son|daughter|child|kid|kids|children|husband|wife|partner|boyfriend|"
    r"girlfriend|mum|mom|mother|dad|father|friend|neighbour|neighbor|colleague|boss|dog|cat)\b",
)
OWN_INJURY_NOT_ME = OWN_INJURY_SOMEONE_OR_A_STORY + OWN_INJURY_YOU + OWN_INJURY_OTHER_PERSON
A_BODY_PART = (
    r"\b(?:hands?|fingers?|fingertips?|thumbs?|arms?|wrists?|elbows?|tongue|mouth|throat|lips?|"
    r"faces?|cheeks?|nose|ears?|eyes?|feet|foot|toes?|legs?|knees?|shins?|chest|backs?|skin|palms?|"
    r"knuckles?|head|scalp|neck|stomach|belly)\b",
)
GREY_HAIR = (
    r"\b(?:hair|hairs|beard|beards|moustache|mustache|eyebrows?|eyelashes?|roots|greying|graying|"
    r"greyed|grayed|bald|balding|receding|thinning|wig|dye|dyed|sideburns?)\b",
)
GREY_COLOUR = (r"\b(?:grey|gray)\b",)
GREY_ARRIVING = (
    r"\b(?:going|goes|go|turning|turns?|getting|gets)\s+(?:\w+\s+){0,2}(?:grey|gray)\b",
    r"\b(?:grey|gray)\s+(?:hair|hairs|roots|streaks?|patch|patches|temples?)\b",
)
GREY_SELF = (r"\b(?:i|im|i'm|ive|i've|me|myself|my\s+own)\b",)
GREY_BODY = (*A_BODY_PART, r"\b(?:gums?|gum\s?colou?r|nail\s?beds?|fingertips?)\b")
GREY_ALARM = (
    r"\b(?:clammy|sweating|sweaty|collapsed?|collapsing|faint(?:ed|ing|s)?|unconscious|"
    r"passed\s+out|passing\s+out|black(?:ed)?\s+out|breathless|struggling\s+to\s+breathe|"
    r"can'?t\s+breathe|cannot\s+breathe|blue|purple|mottled|rash|fitting|seizure|"
    r"unresponsive|limp|floppy|shock|bleeding|blood|vomiting|pulse|911|999)\b",
)
BLUE_HUMAN = (
    *A_BODY_PART,
    r"\b(?:he|she|they|we|him|them|he'?s|she'?s|they'?re|we'?re|myself|himself|herself|themselves|"
    r"everyone|anybody|somebody|someone|anyone)\b",
    r"\b(?:man|woman|boy|girl|child|children|baby|babies|toddler|infant|patient|kid|kids|son|"
    r"daughter|mum|mom|mother|dad|father|husband|wife|partner|boyfriend|girlfriend|brother|"
    r"sister|friend|gran|granny|grandma|grandad|grandpa|nan|nana|uncle|aunt|niece|nephew|"
    r"colleague|neighbour|neighbor|people|men|women|newborn|pupil|student)\b",
    r"\b(?:i|im|i'?m|i'?ve|ive)\s+(?:have\s+|had\s+|was\s+|were\s+|is\s+|am\s+)?"
    r"(?:gone|going|went|turned|turning|been)\b",
    r"\bi\s+(?:am|look|feel)\s+(?:blue|grey|gray|purple)\b",
    r"\b(?:my|his|her|their|our|your)\s+(?:(?:whole|entire)\s+)?bod(?:y|ies)\b",
    r"\bbod(?:y|ies)\b[^.?!]{0,12}\b(?:went|gone|going|turned|turning|is|has|was)\s+"
    r"(?:blue|grey|gray|purple)\b",
    r"\b(?:i'?m|im|i\s+am)\s+(?:blue|grey|gray|purple)\s+all\s+over\b",
)

BURNER_THING = (r"\b(?:wood|log|gas|oil|pellet)\s*burner\b",)
PREVENTION_OR_BURNOUT = (
    r"\b(?:avoid|avoiding|prevent|preventing|stop\s+myself|watch\s+out|be\s+careful)\b"
    r"[^.?!]{0,30}\b(?:burn\w*|scal\w*)",
    r"\bburn\w*\s+(?:myself|yourself|himself|herself|themselves|people|everyone)\s+out\b",
    r"\bburn(?:t|ed)?\s+out\b|\bburnout\b",
)
BLISTER_WORD = (r"\bblister",)
FRICTION_BURN = (
    r"\b(?:rope|carpet|mat|rug|friction|treadmill|tow\s+rope|road\s+rash|chaf\w+|sandpaper|"
    r"grip\s+tape)\b[^.?!]{0,20}\bburn\w*\b",
    r"\bburn\w*\b[^.?!]{0,20}\b(?:from|by|off)\s+(?:the\s+)?(?:rope|carpet|mat|rug|friction|"
    r"treadmill|grip\s+tape|sandpaper)\b",
)
FRICTION_BURN_NOUN = (
    r"\b(?:rope|carpet|mat|rug|friction|treadmill|road\s+rash|chaf\w+|grip\s+tape|sandpaper)"
    r"\s+burn\w*\b",
)
FRICTION_BURN_HEAT = (
    r"\b(?:boiling|boiled|kettle|steam\w*|oven|hob|grill|toaster|hot\s+(?:water|oil|fat|pan|"
    r"plate|metal|iron)|scald\w*|fire|flame\w*|flames|alight|barbecue|bbq|fryer|sun\s?burn\w*|"
    r"curling\s+tongs|straighteners?|hair\s+dryer|blow\s+dry)\b",
)

BURN_WORD = (
    r"\b(?:burn\w*|scald\w*|scorch\w*|singe\w*|boiling|boiled|kettle|steam\w*|oven|hob|grill|"
    r"toaster|iron|fire|"
    r"flame\w*|barbecue|bbq|fryer|sun\s?burn\w*|hot\s+(?:water|oil|fat|pan|plate|metal)|"
    r"heat\s+rash)\b",
)


BLISTER_HOWTO = (
    r"\bhow\s+(?:do|should|can)\s+i\b",
    r"\bwhat\s+(?:do|should)\s+i\s+do\b",
    r"\b(?:treat|pop|burst|drain|cover|dress|protect|deal\s+with|get\s+rid\s+of)\b",
    r"\bshould\s+i\s+(?:pop|burst|drain|cover)\b",
)


def _ring_stuck(line):
    return (_matches(RING_WORD, line) and _matches(FINGER_SIDE, line)
            and _matches(RING_DANGER, line) and not _matches(RING_NOT_WORN, line))


def _friction_blister(line):
    if not _matches(BLISTER_WORD, line) or _matches(BURN_WORD, line):
        return False
    return (_matches(FRICTION_WORD, line)
            or (_matches(BLISTER_HOWTO, line) and not _matches(BURNT_SELF, line)))


def _tooth_out(line):
    if not _matches(TOOTH_OUT, line) or _matches(TOOTH_OUT_FINE, line):
        return False
    if _matches(TOOTH_CHILD, line) and not _matches(TOOTH_KNOCK, line):
        return False
    return True


FALL_STROKE_SIGN = (
    r"\b(?:slurr\w*|slurs?)\b",
    r"\bspeech\s+(?:is|was|sounds?|comes\s+out)\b[^.?!]{0,20}\b(?:slurr\w*|thick|strange|odd)\b",
    r"\bwords?\s+(?:came|come|comes|coming)\s+out\b[^.?!]{0,14}"
    r"\b(?:strange|odd|wrong|thick|slurr\w*)\b",
    r"\b(?:face|mouth)\s+(?:is\s+|has\s+)?(?:droop\w*|dropping|gone\s+on\s+one\s+side|twisted)\b",
    r"\bone\s+side\s+(?:of\s+)?(?:his|her|their|the)\s+(?:body|face|arm)\b[^.?!]{0,24}"
    r"\b(?:gone|weak|numb|heavy|wont|won'?t|not\s+working)\b",
    r"\bcant\s+lift\s+(?:his|her|their)\s+arm\b",
    r"\bcan'?t\s+lift\s+(?:his|her|their)\s+arm\b",
)
SLUR_NOT_A_STROKE_WORDS = (
    r"\b(?:dentist|filling|injection|anaesthetic|numb\s+lip|pints?|drunk|drinking|beers?|"
    r"pub|gig|singer|song|lyric|wine)\b",
)


def _fall_with_sign(line):
    if _matches(FALL_ASLEEP, line):
        return False
    if _matches(FALL_WORD_IDIOM, line):
        return False
    if _matches(FALL_THING, line):
        return False
    if _matches(FALL_CHECK_OFF, line):
        return False
    if _matches(CONFUSION_NAMED_CAUSE, line) and not _matches(
            (r"\b(?:now|worse|still|again|getting\s+worse)\b",), line):
        return False
    return ((_matches(HEAD_FALL, line) or _matches(FALL_REPEAT, line))
            and _matches(HEAD_FALL_SIGN, line))


def _out_cold_knockout(line):
    if _matches(OUT_COLD_ASLEEP, line) or _matches(OUT_COLD_NOW, line):
        return False
    return _matches(HEAD_OUT_COLD, line)


def _head_bang(line):
    if not _matches(HEAD_BANG, line):
        if not _fall_with_sign(line):
            if not (_matches(HEAD_KNOCKOUT, line) or _out_cold_knockout(line)) \
                    or _matches(HEAD_SEEN, line):
                return None
            if _matches(HEAD_PAST, line) and not _matches((r"\bstill\b", r"\bright\s+now\b"), line):
                return None
            if _tooth_out(line):
                return None
            return "red"
        return "red"
    if _matches(HEAD_SEEN, line):
        return None
    if _matches(HEAD_PAST, line) and not _matches((r"\bstill\b", r"\bright\s+now\b"), line):
        return None
    if _matches(HEAD_RED, line):
        return "red"
    if _fainted_with_the_bang(line):
        return "red"
    return "watch"


PET_WORDS = (r"\b(?:dog|dogs|puppy|pup|cat|cats|kitten|horse|pony|rabbit|hamster|parrot|budgie|"
             r"bird|guinea\s+pig|gerbil)\b",)

AQUARIUM_WORDS = (r"\b(?:fish|fishes|goldfish|aquarium|fish\s?tank|pond|koi)\b",)

PLANT_WORDS = (r"\b(?:plant|plants|house\s?plants?|tomato|tomatoes|flower|flowers|shrub|tree|trees|"
               r"lawn|grass|garden|seedlings?|cuttings?)\b",)


_GO_ON_PHRASE = re.compile(r"\b(?:i\s+)?(?:just\s+)?(?:can'?t|cant|couldn'?t|couldnt)\s+go\s+on\b", re.I)

GO_ON_LIVING = (r"\b(?:go|going)\s+on\s+(?:living|existing)\b",)

GARDEN_WORDS = (r"\b(?:lawn|lawns|grass|garden|gardens|plot|allotment|hedge|hedges|borders?)\b",)


def _head_person(line):
    if re.search(r"\bi\s+(?:'ve\s+|had\s+|got\s+)?(?:bang|hit|knock|fell|fall|slip|trip|smack|crack|"
                 r"bash|smash)\w*", line):
        return None
    who = _person(line)
    if who:
        return who
    if re.search(r"\b(?:his|him|he)\b", line):
        return "he"
    if re.search(r"\b(?:her|she)\b", line):
        return "she"
    return None


def _weight_on_a_joint(line, today=False):
    if not (_matches(WEIGHT_OFF_FEET, line) and _matches(WEIGHT_JOINT, line)):
        return False
    if _matches(WEIGHT_HIP, line):
        return False
    if _matches(WEIGHT_OLD, line) and _matches(WEIGHT_OLD_FALL, line):
        return False
    if today and _matches(WEIGHT_LONG, line):
        return False
    return True


GRIME_CLEANING = (r"\b(?:clean|cleaning|cleaned|scrub\w*|scour\w*|soak\w*|remove|removing|"
                   r"wash\w*|lift|lifting|shift|shifting|get|getting)\b",)
BURNT_GRIME = (r"\b(?:burnt|burned|burning|scorched|charred|blackened)\b",)


GRIME_OFF = (r"\b(?:burnt|burned|scorched|charred|blackened)\s+"
             r"(?:bits?|stuff|food|grime|marks?|patches?|\w+)?\s*(?:off|out\s+of)\b",)


def _grime_on_a_surface(line):
    if (_matches(GRIME_OFF, line) and _matches(CLEANABLE_SURFACE, line)
            and not _matches(BURNT_SELF, line)):
        return True
    return (_matches(GRIME_CLEANING, line) and _matches(BURNT_GRIME, line)
            and _matches(CLEANABLE_SURFACE, line)
            and not _matches(PERSON_BURNT, line) and not _matches(BURNT_SELF, line))


MILD_BODY_ESCALATION = (
    " An injury on top of feeling unwell is a 111 call today, and 999 if waking gets harder, "
    "breathing goes fast, or lips go grey or blue."
)


_MINOR_REPLIES = {name: replies for name, _patterns, replies in MINOR}


PET_FIRST_AID_ROWS = frozenset((
    "bleeding", "cut", "burn", "sunburn", "mouth_burn", "splinter", "nosebleed", "part_off",
    "broken",
))


def _pet_first_aid(line):
    if _matches(BURN_OR_SCALD_WORD, line):
        return REPLIES["pet_burn"]
    if _matches(PET_WOUND, line):
        return _MINOR_REPLIES["pet_wound"]
    return REPLIES["pet_hurt"]


BURN_OR_SCALD_WORD = (r"\bburn(?:s|t|ed|ing)?\b", r"\bscald\w*\b")

THE_INJURY_NAMED_BEYOND_A_QUESTION = frozenset((
    "burn", "burns", "burnt", "burned", "scald", "scalds", "scalded", "cut", "cuts",
    "gash", "graze", "sprain", "sprains", "sprained", "blister", "blisters", "sunburn",
    "bruise", "bruises", "bruised", "wound", "wounds",
))


def _the_injury_the_chat_is_on(line, memory):
    if not isinstance(memory, dict) or not _matches(ASKS_ABOUT_THE_INJURY, line):
        return ""
    turns = memory.get("turns") or []
    last_card = ""
    for turn in reversed(turns[-3:]):
        if isinstance(turn, dict) and turn.get("module") == "safety":
            last_card = " ".join(str(turn.get("user") or "").lower().split())
            break
    if not last_card:
        return ""
    earlier = set(last_card.split())
    if [word for word in line.split()
            if word not in A_FOLLOW_UP_ABOUT_THE_INJURY and word not in earlier]:
        return ""
    for name, words in HEAL_WORDS:
        if re.search(words, last_card):
            return name
    for word in THE_INJURY_NAMED_BEYOND_A_QUESTION:
        if re.search(r"\b" + word + r"\b", last_card):
            return word
    return ""


def _minor(line, memory=None):
    if memory is not None:
        injury = _the_injury_the_chat_is_on(line, memory)
        if injury and _first_aid(line) is None:
            line = line + " " + injury
    if _matches(WHOLE_BODY_RED_FLAG, line):
        return None
    reply = _first_aid(line)
    if reply is not None and _matches(MILD_BODY_SIGN, line):
        if isinstance(reply, tuple):
            return tuple(one + MILD_BODY_ESCALATION for one in reply)
        return reply + MILD_BODY_ESCALATION
    return reply


def _minor_replies(name):
    for row in MINOR:
        if row[0] == name:
            return row[2]
    return ()


def _first_aid(line):
    if _self_harm_intent(line):
        return None
    if _matches(SPINE_BREAK, line):
        if _matches(SPINE_BACK_WORK, line) and not _matches(SPINE_BACK_FALL, line):
            return None
        if _matches(SPINE_NUMB_LOWER, line) and not _matches(
                (r"\b(?:neck|spine|spinal)\b", r"\b(?:paralysed|paralyzed)\b",
                 r"\b(?:can'?t|cant|cannot)\s+move\b"), line):
            return None
        return SPINE_BREAK_ANSWER
    if _an_ordinary_helping(line):
        return None
    if _matches(PREVENTION_OR_BURNOUT, line) and not _matches(BURNT_SELF, line):
        return None
    thing_burnt = ((_matches(THING_BURNT, line) or _grime_on_a_surface(line))
                   and not _matches(A_BODY_PART, line)
                   and not _matches(BURNT_SELF, line))
    burner_thing = (_matches(BURNER_THING, line) and not _matches(A_BODY_PART, line)
                    and not _matches(BURNT_SELF, line))
    friction = _friction_blister(line)
    food_burnt = (_matches(BURNT_FOOD, line) and not _matches(A_BODY_PART, line)
                  and not _matches(BURNT_SELF, line))
    razor = (_matches(RAZOR_BURN, line) and not _matches(FRICTION_BURN_HEAT, line)
             and not _matches(BURNT_BODY_VERB, line))
    if (_matches(FRICTION_BURN, line) and not _matches(FRICTION_BURN_HEAT, line) and not razor
            and (_matches(A_BODY_PART, line) or _matches(FRICTION_BURN_NOUN, line))):
        return REPLIES["friction_burn"]
    if _matches(BLISTER_STATE, line) and not _matches(BURN_WORD, line) \
            and not _matches(BLISTER_CAUSE_BURN, line):
        return BLISTER_STATE_REPLIES
    if _matches(HOW_LONG, line):
        if re.search(r"\bsun\s?burn", line):
            return HEAL_TIME["sunburn"]
        for name, words in HEAL_WORDS:
            if (name == "cut" and _matches(FOOD_CUT, line) and not _matches(A_BODY_PART, line)
                    and not re.search(CUT_SELF, line)):
                continue
            if (name == "cut" and _matches(NOT_A_BODY_CUT, line)
                    and not _matches(A_BODY_PART, line) and not re.search(CUT_SELF, line)):
                continue
            if re.search(words, line):
                return HEAL_TIME[name]
    if _matches(GRATER_CUT, line):
        return _MINOR_REPLIES["cut"]
    for name, patterns, replies in MINOR:
        if name == "burn" and (thing_burnt or burner_thing or friction or razor
                               or food_burnt):
            continue
        if name == "cut" and _cut_off_idiom(line):
            continue
        if (name == "broken" and _matches(BONE_OUT_LOOSE, line) and _matches(FOOD_BONE, line)
                and not re.search(BODY_LIMB, line)):
            continue
        if (name == "cut" and _matches(FOOD_CUT, line) and not _matches(A_BODY_PART, line)
                and not re.search(CUT_SELF, line)):
            continue
        if name == "limp" and _matches(LIMP_OTHER_LIMB, line):
            return _MINOR_REPLIES["sprain"]
        if name in ("limp", "limp_long") and _matches(LIMP_NOT, line):
            continue
        if name in ("limp", "limp_long") and _matches(LIMP_MECHANISM, line):
            continue
        if name == "limp_long" and not _matches(LIMP_LONG, line):
            continue
        if name == "limp" and _matches(LIMP_LONG, line):
            continue
        if name == "limp" and _matches(LIMP_CAUSE, line):
            if _matches(LIMP_REPLACED, line) and _matches(LIMP_SOMEBODY_ELSE, line) \
                    and re.search(r"\b(?:limp\w*|hobbl\w*|gait|walk\w*)\b", line):
                return _MINOR_REPLIES["limp_long"]
            continue
        if name == "sight_long" and not _matches(LIMP_ONGOING, line):
            continue
        if name == "limp" and _matches(LIMP_ONGOING, line) \
                and (_matches(LIMP_PERSON, line)
                     or re.search(r"\b(?:limp\w*|hobbl\w*|gait)\b", line)
                     or re.search(LEG_WORDS, line)):
            return _MINOR_REPLIES["limp_long"]
        if name == "weight_limb_long" and not (_weight_on_a_joint(line)
                                             and _matches(WEIGHT_LONG, line)):
            continue
        if name == "weight_limb" and not _weight_on_a_joint(line, today=True):
            continue
        if name == "ring_stuck" and not _ring_stuck(line):
            continue
        if name in ("tooth_out", "tooth_chipped") and _matches(PET_TOOTH, line) \
                and _matches(patterns, line):
            return REPLIES["pet_tooth"]
        if name == "pet_wound" and (_matches(HUMAN_TOO, line)
                                    or _matches(HUMAN_BITTEN, line)):
            continue
        if name in PET_FIRST_AID_ROWS and _matches(PET_ANIMAL_HURT, line) \
                and not _matches(HUMAN_TOO, line) and not _matches(HUMAN_BITTEN, line) \
                and not _matches(HUMAN_OWN_INJURY, line) \
                and not _matches(PET_PASSES_BLOOD, line) \
                and not _matches(PET_OWNS_A_THING, line):
            return _pet_first_aid(line)
        if name == "tooth_out" and not _tooth_out(line):
            continue
        if name == "tooth_chipped" and (_matches(TOOTH_CHIPPED_FINE, line) or _tooth_out(line)):
            continue
        if _matches(patterns, line):
            return replies
    if _matches(HOW_TO_TREAT, line) and not thing_burnt and not burner_thing:
        for name, words in INJURY_WORDS:
            if name == "burn" and (friction or razor or food_burnt):
                continue
            if _matches(words, line):
                for case, _, replies in MINOR:
                    if case == name:
                        return replies
    return None


def _last_case(memory):
    if not isinstance(memory, dict):
        return None
    recent = (memory.get("turns") or [])[-2:]
    if not any(isinstance(turn, dict) and turn.get("module") == "safety" for turn in recent):
        return None
    case = memory.get("safety_case")
    if case in WAITING:
        return case
    for turn in reversed(recent):
        if not isinstance(turn, dict) or turn.get("module") != "safety":
            continue
        said = turn.get("bot") or ""
        for name, options in REPLIES.items():
            if said in options:
                return name
        return None
    return None

CPR_ASK = (
    r"\bcpr\b", r"\bcompressions?\b", r"\brescue\s+breaths?\b", r"\bbreaths?\s+(?:to|and)\s+",
    r"\bhow\s+(?:hard|fast|deep|many)\b", r"\btoo\s+(?:hard|fast|deep|soft|slow|gentle)\b",
)
CPR_SCENE = (
    r"\bnot\s+breathing\b", r"\bstopped\s+breathing\b", r"\b(?:start|do|doing)\s+cpr\b",
    r"\bcpr\b", r"\bnot\s+waking\b", r"\bunconscious\b", r"\bcollapsed\b",
    r"\brecovery\s+position\b", r"\bno\s+pulse\b",
)
CPR_NOT_A_BODY = (
    r"\b(?:brakes?|pedal|clutch|throttle|pram|pushchair|wheelchair|trolley|barrow|mower|hoover|"
    r"vacuum|door|doors|drill|screw|nail|brush|paint\w*|button|buttons|lever|handle|swing|"
    r"snooze|send|reply|publish|commit|merge|updates?)\b",
)
CPR_SCENE_CASES = (
    "breathing", "not_breathing", "unconscious", "choking", "drowning", "hanging", "bleeding",
    "chest", "stroke", "seizure", "overdose", "anaphylaxis", "fire", "gas", "self_harm",
)
CPR_STILL_ALIVE = (
    r"\b(?:a\s+)?(?:pulse|heartbeat|heart\s+beat)\b", r"\bstill\s+breathing\b",
    r"\bbreathing\s+(?:normally|on\s+(?:his|her|their)\s+own|by\s+(?:him|her|them)sel(?:f|ves))\b",
    r"\b(?:is|are|was|were)\s+breathing\b",
)
CPR_NOT_ALIVE = (
    r"\bno\s+(?:pulse|heartbeat)\b", r"\bnot\s+breathing\b", r"\bstopped\s+breathing\b",
    r"\b(?:isn'?t|aren'?t|isnt|arent)\s+breathing\b",
)
CPR_NO_PULSE = (r"\bno\s+(?:pulse|heartbeat)\b",)
CPR_BABY = (
    r"\b(?:baby|babies|newborn|new\s?born|infant|infants)\b",
    r"\b\d+\s*(?:day|week|month)s?\s*old\b", r"\bunder\s+(?:one|1|a)\b",
    r"\b(?:six|seven|eight|nine|ten|eleven|two|three|four|five)\s+(?:weeks?|months?)\s+old\b",
)


CALL_HELP = (
    r"\bshould\s+i\s+(?:call|ring|phone|dial)\b.{0,25}\b(?:ambulance|999|911|112|help|doctor)\b",
    r"\bdo\s+(?:i|we)\s+need\s+(?:an\s+)?ambulance\b",
    r"\bshall\s+i\s+(?:call|ring|phone)\b",
    r"\bis\s+it\s+(?:bad\s+enough\s+)?(?:for\s+)?an\s+ambulance\b",
)
ASPIRIN = (
    r"\b(?:should|can|shall|do|could)\s+(?:i|we|he|she|they)\s+(?:take|have|give|chew)\b"
    r"[^.?!]{0,25}\baspirin\b",
    r"\baspirin\b[^.?!]{0,25}\b(?:ok|okay|safe|help|good|wise)\b",
    r"\b(?:give|take|chew)\b[^.?!]{0,20}\baspirin\b",
)
FITTING_MANNER = re.compile(
    r"\bfitting\s+(?:in\s+)?(?:nicely|well|perfectly|fine|easily|beautifully|smoothly|"
    r"brilliantly)\b")


def _a_settling_fit(line):
    found = FITTING_MANNER.search(line)
    if not found:
        return False
    return bool(FITTING_MANNER_TAIL.match(line[found.end():].strip(" .,!?;:")))


FITTING_THING = (
    r"\bfitting\s+(?:his|her|their|my|your|our|its|him|them|me|a|an|the|new|another|some|"
    r"these|those|this)\b",
)


CORRECTION_OF_PERSON = (
    r"\b(?:sorry|no|actually|wait)?,?\s*i\s+mean\s+(?:my|his|her|the|its)\b",
    r"\bnot\s+(?:my|the)\s+\w+\s*,?\s*(?:it'?s|its|but)\b",
    r"\b(?:i\s+meant|i\s+said)\s+(?:my|the)\b",
    r"\bwrong\s+person\b",
)


def _last_said_as_written(memory):
    if not isinstance(memory, dict):
        return ""
    for turn in reversed((memory.get("turns") or [])[-3:]):
        if isinstance(turn, dict) and turn.get("module") == "safety":
            return turn.get("bot") or ""
    return ""


def _resay(raw, line, memory):
    who = _person(line)
    if who:
        if isinstance(memory, dict):
            memory["safety_person"] = who
        pairs = (("him", "her"), ("his", "her"), ("he", "she"), ("he's", "she's"),
                 ("himself", "herself"), ("them", "her"), ("their", "her")) \
            if who == "she" else (
                ("her", "him"), ("hers", "his"), ("she", "he"), ("she's", "he's"),
                ("herself", "himself"), ("them", "him"), ("their", "his"))
        for word, swap in pairs:
            raw = re.sub(r"\b" + word + r"\b", swap, raw)
    return raw


ESCALATED_ALREADY = (
    r"\bshould\s+i\b", r"\bwhat\s+(?:do|should)\s+i\b", r"\bshall\s+i\b",
    r"\bcan\s+i\b", r"\bhow\s+(?:do|long|much)\b",
)
DETAIL_REPLY = (
    "Got that - tell the 999 or 911 handler it as well, and stay with them until the ambulance "
    "comes.",
    "Tell the 999 or 911 handler that too. Stay with them and keep them talking until the "
    "ambulance arrives.",
)


def _name_the_person(reply, line, memory):
    named = _person(line) or (memory.get("safety_person") if isinstance(memory, dict) else None)
    if named is None:
        return reply
    pairs = (("them", "her"), ("their", "her"), ("they're", "she's")) if named == "she" else (
        ("them", "him"), ("their", "his"), ("they're", "he's"))
    for word, swap in pairs:
        reply = re.sub(r"\b" + word + r"\b", swap, reply)
    return reply


def _true_newborn(memory):
    if not isinstance(memory, dict):
        return False
    for turn in reversed((memory.get("turns") or [])[-4:]):
        if not isinstance(turn, dict):
            continue
        said = str(turn.get("user") or "")
        if not said:
            continue
        if _matches(TRUE_NEWBORN_FINE, said):
            return False
        if _matches(TRUE_NEWBORN, said):
            return True
    return False


def _tiny_baby(memory):
    if not isinstance(memory, dict):
        return False
    for turn in reversed((memory.get("turns") or [])[-4:]):
        if not isinstance(turn, dict):
            continue
        said = str(turn.get("user") or "")
        if not said:
            continue
        if _matches(TINY_AGE_FINE, said):
            return False
        if _matches(TINY_AGE, said):
            return True
    return False


def _last_said(memory):
    if not isinstance(memory, dict):
        return ""
    for turn in reversed((memory.get("turns") or [])[-3:]):
        if isinstance(turn, dict) and turn.get("module") == "safety":
            return (turn.get("bot") or "").lower()
    return ""


_AN_ACT_OR_NOT = (
    r"(?:\b(?:should|shall|do|can|could|ought|may)\s+(?:i|we)\b|"
    r"\b(?:is|would)\s+it\s+(?:be\s+)?(?:ok(?:ay)?|alright|all\s+right|safe|fine)\s+to)\b"
    r"[^.?!]{0,40}?"
    r"(?:\b(?:turn|switch|shut|plug|unplug|disconnect|stop|leave|touch|kill|put|pour|throw|run|stay|"
    r"move|carry|open|cover|smother|fan)\b|"
    r"\b(?:keep|go\s+on|carry\s+on)\s+using\b|\buse\s+it\s+again\b)")
_A_LIVE_HAZARD = (
    r"\b(?:spark(?:s|ing|ed)?|fizz(?:ing|ed)?|smok(?:e|ing|y)|smoulder(?:ing)?|smolder(?:ing)?|"
    r"burn(?:ing|t)?|scorch(?:ed|ing)?|melt(?:ing|ed)?|buzz(?:ing)?|on\s+fire|caught\s+fire|"
    r"too\s+hot\s+to\s+touch|red\s+hot)\b")

BACK_ON = (
    "Not yet - leave it off and unplugged until someone has looked at it. Whatever sparked or "
    "smoked once will do it again, and the next time nobody may be in the room.",
    "I would not. Keep it out of use until it has been checked: the fault that sparked it has not "
    "gone away by itself, and a fire is a lot harder to put out than a plug is to leave alone.",
)
_A_BURNT_PERSON = (
    r"\b(?:hand|hands|arm|arms|finger|fingers|thumb|thumbs|skin|wrist|wrists|foot|feet|leg|legs|"
    r"knee|knees|shoulder|shoulders|chest|face|eyes?|head|hair|lip|lips|tongue|mouth|neck|ears?|"
    r"blister(?:s|ed|ing)?|myself|himself|herself|themselves|me)\b")
_A_WANTS_IT_ON = (
    r"\b(?:back\s+on|on\s+again|switch\s+it\s+on|turn\s+it\s+on|plug\s+it\s+(?:back\s+)?in|"
    r"use\s+it\s+again|start\s+it\s+(?:up\s+)?again)\b")

SWITCH_OFF = (
    "Yes - switch it off at the wall, and unplug it if you can reach the plug without touching "
    "anything hot or wet. Leave it out of use until someone has looked at it.",
    "Off, and unplugged if you can do that safely. Whatever sparked or smoked is not safe to use "
    "again until it has been checked - and if it is burning or smoking now, get out and ring 999 "
    "rather than stay with it.",
    "Switch it off at the wall and unplug it, without touching the metal or anything wet, then "
    "keep it out of use. A thing that has sparked once does it again, and this one wants looking "
    "at before it goes back on.",
)


def _follow_up(line, memory):
    hazard = _said_before(memory, 2) if isinstance(memory, dict) else ""
    if isinstance(memory, dict) and _matches(_AN_ACT_OR_NOT, line) \
            and _matches(_A_LIVE_HAZARD, hazard) \
            and not _matches(_A_BURNT_PERSON, hazard) \
            and not _matches(_A_LIVE_HAZARD, line):
        case = str(_last_case(memory) or "")
        if case in ("pan_fire", "clothes_fire"):
            _note(memory, "fire" if case == "pan_fire" else case)
            return _fit(pick(REPLIES[case], memory), line, case)
        _note(memory, "fire")
        if _matches(_A_WANTS_IT_ON, line):
            return _fit(pick(BACK_ON, memory), line, "fire")
        return _fit(pick(SWITCH_OFF, memory), line, "fire")
    if isinstance(memory, dict) and memory.get("safety_case") == "near_fire" \
            and any(isinstance(t, dict) and t.get("module") == "safety"
                    for t in (memory.get("turns") or [])[-2:]) \
            and _matches(NEAR_FIRE_OVER, line) \
            and not _says_something_is_burning(line):
        return _fit(pick(REPLIES["near_fire_over"], memory), line)
    if isinstance(memory, dict) and memory.get("safety_case") in ("near_thing", "struck_my_bike") \
            and any(isinstance(t, dict) and t.get("module") == "safety"
                    for t in (memory.get("turns") or [])[-2:]) \
            and _matches(NEAR_THING_OVER, line):
        return _fit(pick(REPLIES["near_thing_over"], memory), line)
    if str(_last_case(memory) or "") in WISH_FRAMES + ("self_harm_other", "poison") \
            and _matches(HELD_CRISIS_DETAIL, line) and not _matches(HELD_CRISIS_OFF, line) \
            and not _matches(CRISIS_PLAN_ORDINARY, line):
        _note(memory, "self_harm")
        return _fit(pick(REPLIES["self_harm"], memory), line, "self_harm")
    if _matches(A_PLAN_SAID, line) and not _matches(A_PLAN_ORDINARY, line):
        _note(memory, "self_harm")
        return pick(CRISIS_PLAN_REPLY, memory)
    said_child = any(isinstance(t, dict) and t.get("module") == "safety"
                     and (t.get("bot") or "") in REPLIES["slur_small_child"]
                     for t in ((memory.get("turns") or [])[-2:] if isinstance(memory, dict) else []))
    if said_child:
        if _matches(SLUR_SMALL_CHILD_URGENT, line):
            return _fit(pick(SLUR_SMALL_CHILD_URGENT_REPLY, memory), line)
        if _matches(SLUR_SUDDEN, line):
            _note(memory, "stroke")
            return _fit(pick(REPLIES["stroke"], memory), line, "stroke")
        if _matches(SLUR_NOT_SUDDEN, line):
            return _fit(pick(SLUR_SMALL_CHILD_CALM, memory), line)
        return None
    if _matches(DENTAL_NUMB_ASK, line) and isinstance(memory, dict) \
            and memory.get("safety_case") == "dental_numb" \
            and any(isinstance(t, dict) and t.get("module") == "safety"
                    for t in (memory.get("turns") or [])[-2:]):
        return _fit(pick(DENTAL_NUMB_FOLLOW, memory), line)
    if str(_last_case(memory) or "").startswith("alcohol_withdrawal") \
            and any(isinstance(t, dict) and t.get("module") == "safety"
                    for t in (memory.get("turns") or [])[-2:]):
        if _severe(line):
            _note(memory, "alcohol_withdrawal_severe")
            return _fit(pick(REPLIES["alcohol_withdrawal_severe"], memory), line)
        if _matches(WITHDRAWAL_WORSE, line):
            _note(memory, "alcohol_withdrawal_more")
            return _fit(pick(REPLIES["alcohol_withdrawal_worse"], memory), line)
        if _matches(WITHDRAWAL_SYMPTOM, line):
            _note(memory, "alcohol_withdrawal_more")
            return _fit(pick(REPLIES["alcohol_withdrawal_more"], memory), line)
        if _matches(WITHDRAWAL_DURATION, line):
            _note(memory, "alcohol_withdrawal_more")
            return _fit(pick(REPLIES["alcohol_withdrawal_when"], memory), line)
        if _matches(WITHDRAWAL_HAIR_OF_THE_DOG, line):
            _note(memory, "alcohol_withdrawal_more")
            return _fit(pick(REPLIES["alcohol_withdrawal_hair"], memory), line)
        if _matches(WITHDRAWAL_DANGER, line):
            _note(memory, "alcohol_withdrawal_more")
            return _fit(pick(REPLIES["alcohol_withdrawal_danger"], memory), line)
        return None
    calm = (REPLIES["dental_numb"] + REPLIES["slur_drink"] + REPLIES["alcohol_withdrawal"]
            + REPLIES["alcohol_withdrawal_more"] + REPLIES["alcohol_withdrawal_when"]
            + REPLIES["alcohol_withdrawal_danger"] + REPLIES["alcohol_withdrawal_worse"])
    if any(isinstance(t, dict) and t.get("module") == "safety" and (t.get("bot") or "") in calm
           for t in ((memory.get("turns") or [])[-2:] if isinstance(memory, dict) else [])):
        return None
    case = _last_case(memory)
    if case is None:
        return None
    said = _last_said(memory)
    if case in ("breathing", "not_breathing", "unconscious", "drowning", "hanging") \
            and _matches(CPR_STOP, line):
        return pick(CPR_STOP_REPLY, memory)
    if _matches(CPR_ASK, line) and (_matches(CPR_SCENE, said) or case in (
            "breathing", "not_breathing", "unconscious", "choking", "drowning", "hanging",
            "general", "chest")):
        baby = _matches(CPR_BABY, line) or _matches(CPR_BABY, said)
        child = _matches(CPR_CHILD, line) or _matches(CPR_CHILD, said)
        if _matches((r"\btoo\s+(?:hard|fast|deep|soft|slow|gentle)\b", r"\bdoing\s+it\s+"
                     r"(?:right|wrong)\b", r"\bam\s+i\s+doing\b"), line):
            return pick(CPR_ROUGH, memory)
        if baby:
            return pick(CPR_BABY_SCENE, memory)
        if child:
            return pick(CPR_CHILD_SCENE, memory)
        if _matches((r"\bshould\s+i\b", r"\bdo\s+i\b", r"\bshall\s+i\b", r"\bstart\b"),
                    line):
            return pick(CPR_START, memory)
        return pick(CPR_HOW, memory)
    if case == "chest" and _matches(ASPIRIN, line):
        return _name_the_person(pick(ASPIRIN_REPLY, memory), line, memory)
    if case != "self_harm" and _matches(WHEN_HELP_COMES, line):
        return _name_the_person(pick(WHEN_HELP_REPLY, memory), line, memory)
    if case == "abuse" and _matches(ABUSE_SCARED, line):
        return _name_the_person(pick(ABUSE_SCARED_REPLY, memory), line, memory)
    if case != "self_harm" and _matches(FRIGHTENED, line):
        return _name_the_person(pick(FRIGHTENED_REPLY, memory), line, memory)
    if _matches(CALL_HELP, line):
        return _name_the_person(pick(CALL_HELP_REPLY, memory), line, memory)
    if _matches(CORRECTION_OF_PERSON, line) and case not in ("self_harm",):
        raw = _last_said_as_written(memory)
        if raw and _matches((r"\b999\b", r"\b911\b", r"\bemergency\b"), raw.lower()):
            return _resay(raw, line, memory)
    if _matches(DETAIL_AFTER_ESCALATION, line) and not _matches(ESCALATED_ALREADY, line):
        return _name_the_person(pick(DETAIL_REPLY, memory), line, memory)
    if not _matches(FOLLOW_UP, line):
        return None
    if _matches(HELP_ARRIVED, line) and not _matches(HELP_ASK_MORE, line):
        return None
    case_words = CASE_WORDS.get(case) or CASE_WORDS["general"]
    if not (_matches(FOLLOW_UP_ANCHOR, line) or _matches((case_words,), line)):
        return None
    safe = _matches(SAFE_NOW, line)
    if isinstance(memory, dict) and memory.get("safety_safe"):
        safe = True
    table = AFTER if safe else WAITING
    if isinstance(memory, dict):
        memory["safety_safe"] = safe
    options = table.get(case)
    if options is None:
        return None
    named = memory.get("safety_person") if isinstance(memory, dict) else None
    who = line if _person(line) else (named or _person_before(memory))
    reply = _fit(pick(options if isinstance(options, tuple) else (options,), memory), who, case)
    if case in FIRST_FIT and not _person(line) and _matches(FIRST_PERSON, line):
        for pattern, replacement in ME:
            reply = re.sub(pattern, replacement, reply, flags=re.I)
    return reply




CASE_ALIAS = {
    "gas_left": "gas", "gas_smell": "gas", "dog_bite": "dog_bite", "dog_attack": "dog_attack",
    "head_injury": "head_injury", "other": "general",
}


def _note(memory, case):
    if isinstance(memory, dict):
        memory["safety_case"] = CASE_ALIAS.get(case, case)
        memory["safety_safe"] = False


SUGAR_SHOP = (
    r"\b(?:in\s+price|prices?|priced|cost|costs|costing|\d+\s*p\b|pence|quid|"
    r"pounds?|kilos?|bags?|packets?|tins?|grams?|teaspoons?|spoons?)\b",
)
SUGAR_MENTION = re.compile(r"\b(?:blood\s+)?sugar\b|\bglucose\b", re.I)


def _sugar_is_the_shopping(line):
    found = False
    for match in SUGAR_MENTION.finditer(line):
        found = True
        rest = re.split(r"\band\b|\bbut\b|[,.?!;]", line[match.end():match.end() + 60], 1)[0]
        before = re.split(r"\band\b|\bbut\b|[,.?!;]", line[max(0, match.start() - 30):match.start()], 1)[-1]
        if not _matches(SUGAR_SHOP, rest) and not _matches(SUGAR_SHOP, before):
            return False
    return found


def _hypo_reply(line, memory):
    if not _matches(HYPO, line):
        return None
    if _sugar_is_the_shopping(line) and not _matches(HYPO_STRONG, line):
        return None
    if _matches(SUGAR_IN_A_RECIPE, line) and not _matches(HYPO_STRONG, line):
        return None
    if _matches(HYPO_HOW_KNOW, line) and not _matches(HYPO_STRONG, line):
        return None
    if not _matches(LOW_SUGAR_NOW, line) and (
            _matches(HYPO_QUESTION, line)
            or (_matches(HYPO_PAST, line) and not _matches(HYPO_NOW, line))):
        return None
    if _matches(CONFUSED_THING, line) and not _matches(HYPO_STRONG, line):
        return None
    if _matches(HYPO_LIE_IN, line) and not _matches(HYPO_STRONG_OTHER, line):
        return None
    mine = _matches((r"\bi\b", r"\bmy\b"), line) and not _person(line)
    if not mine and _matches(HYPO_NO_MOUTH, line):
        return _fit(pick(REPLIES["hypo_no_mouth"], memory), line, "hypo")
    key = "hypo_self" if mine else "hypo"
    return _fit(pick(REPLIES[key], memory), line, "hypo")


def _words(text):
    return re.findall(r"[a-z]+(?:'[a-z]+)*", text.lower())


def _a_repair_the_reader_made(memory):
    if not isinstance(memory, dict):
        return frozenset()
    understood = memory.get("understood")
    if not isinstance(understood, dict):
        return frozenset()
    fixes = understood.get("fixes")
    if not isinstance(fixes, dict):
        return frozenset()
    return frozenset(str(word).lower() for word in fixes)


def _repaired(text, memory):
    typed = respell_urgent(text)
    typed = said_apart(typed)
    typed_text = said_apart(text)
    plain = ""
    if isinstance(memory, dict):
        understood = memory.get("understood")
        if isinstance(understood, dict):
            plain = understood.get("plain") or ""
    if not isinstance(plain, str) or not plain.strip():
        return typed
    mine, read, said = _words(typed_text), _words(typed), _words(plain)
    if len(mine) != len(read) or len(read) != len(said):
        return typed
    pieces, last = [], 0
    for at, found in enumerate(re.finditer(r"[A-Za-z]+(?:'[A-Za-z]+)*", typed)):
        if (said[at] != read[at] and said[at] != mine[at]
                and (mine[at] not in LEXICON or mine[at] in MISSPELLINGS
                     or mine[at].lower() in _a_repair_the_reader_made(memory))):
            pieces.append(typed[last:found.start()])
            pieces.append(said[at])
            last = found.end()
    if not pieces:
        return typed
    pieces.append(typed[last:])
    return "".join(pieces)


WITHDRAWAL_FIT_ITS_OWN_ANSWER = (
    r"\b(?:fits?|seizures?|seizure|seized|convuls\w*|fitting)\b",
)


def _withdrawal(line):
    if _matches(WITHDRAWAL_NOT_ALCOHOL, line) or _matches(WITHDRAWAL_LONG_AGO, line) \
            or _matches(WITHDRAWAL_NOT_NOW, line):
        return None
    if _matches(WITHDRAWAL_WEEKS, line) and _matches(WITHDRAWAL_FINE, line):
        return None
    if _matches(WITHDRAWAL_FINE, line) and not (
            _matches(WITHDRAWAL_SYMPTOM, line) or _severe(line)
            or _matches(WITHDRAWAL_BARE_BAD, line)):
        return None
    sign = _matches(WITHDRAWAL_SYMPTOM, line) or _severe(line) \
        or _matches(WITHDRAWAL_BARE_BAD, line)
    carried = (
        (_matches(WITHDRAWAL_STOP + WITHDRAWAL_COLD_TURKEY, line)
         and (sign or _matches(WITHDRAWAL_NAMED, line)))
        or (_matches(WITHDRAWAL_BARE, line) and sign)
        or (_matches(WITHDRAWAL_SOBER, line) and sign)
        or _matches(WITHDRAWAL_ROUTINE, line)
        or _matches(WITHDRAWAL_ALONE_AT_HOME, line))
    if not carried:
        return None
    if _matches(PREGNANT_LINE, line) and not _matches(WITHDRAWAL_STRONG, line):
        return None
    return "severe" if _severe(line) else "mild"


WISH_FRAMES = ("self_harm", "overdose", "crisis", "despair")

_FIRE_WORD = re.compile(
    r"\b(?:fire|fires|flames?|flaming|alight|ablaze|blazing|burning|burn|burnt|burned|"
    r"catch|caught|catchin(?:g)?|smoke|smoking|smouldering|smoldering|torched?|torching|"
    r"caught\s+light|took\s+light)\b")
_BURNS_UP = re.compile(
    r"\b(?:curtains?|carpets?|rugs?|sofas?|settee|armchair|chairs?|bed|bedding|mattress|pillow|"
    r"shed|garage|house|flat|kitchen|room|pan|pans|oil|chip\s+pan|grill|oven|hob|toaster|toast|"
    r"towels?|tea\s?towel|dish\s?towel|cloth|sleeve|shirt|coat|dressing\s+gown|dressing\s+robe|"
    r"apron|hair|beard|bins?|wheelie\s+bin|tree|wreath|paper|newspaper|cardboard|wood|logs?|"
    r"firewood|car|van|tent|rubbish|hay|straw|leaves)\b[^.?!]{0,30}?"
    r"\b(went|go|goes|going|gone)\s+up\b")
_NEAR_WORD = re.compile(r"\b(?:nearly|almost|close\s+to|about\s+to)\b")
_BURNING_NOW = re.compile(
    r"\b(?:alight|ablaze|on\s+fire|caught\s+fire|flames?|smoking|smoke|smoulders?|burning|"
    r"burnt|smell\s+of\s+burning)\b")
_NEGATED_BEFORE = re.compile(r"\b(?:no|not|just|only|without|none|never)\b[^.]{0,14}$")


def _says_something_is_burning(line):
    for match in _BURNING_NOW.finditer(line):
        if not _NEGATED_BEFORE.search(line[max(0, match.start() - 18):match.start()]):
            return True
    return False


_CLAUSE_BREAK = re.compile(
    r"[.?!,;:]|\b(?:and|but|then|so|because|when|while|before|after|until|till|if)\b")


def _fire_words_in(line):
    words = list(_FIRE_WORD.finditer(line))
    words += [_Where(m.start(1)) for m in _BURNS_UP.finditer(line)]
    return words


class _Where:

    def __init__(self, start):
        self._start = start

    def start(self):
        return self._start


def _a_fire_that_did_not_happen(line):
    near = [m.start() for m in _NEAR_WORD.finditer(line)]
    fire_words = _fire_words_in(line)
    if not near or not fire_words:
        return False
    breaks = [m.start() for m in _CLAUSE_BREAK.finditer(line)]

    def close(start, fire_start):
        if not 0 < fire_start - start <= 40:
            return False
        return not any(start < b < fire_start for b in breaks)

    return all(any(close(start, m.start()) for start in near) for m in fire_words)


def respond(text, memory):
    text = _leet_made_whole(text) or text
    line = _norm(_repaired(text, memory))
    if _dream is not None and _dream.a_dream_is_not_happening(text):
        return None
    if _matches(SOFT_FACE_PUSH, line) and not _matches(SOFT_FACE_STOP, line):
        _note(memory, "general")
        return pick(PLAY_FACE_REPLIES, memory)
    if isinstance(memory, dict) and _person(line):
        memory["safety_person"] = _person(line)
    if _matches(SHAKE_CHILD, line) and not _matches(SHAKE_IDIOM, line) \
            and (_matches(SHAKE_CHILD_CONTEXT, line)
                 or (_matches(SHAKE_COPING, line) and not _matches(SHAKE_ADULT, line))):
        _note(memory, "abuse")
        return pick(SHAKE_REPLY if _matches(SHAKE_BABY_WORD, line) else SHAKE_CHILD_REPLY, memory)
    if _matches(OUT_COLD_LONG, line) and not _matches(OUT_COLD_SLEEPY, line) \
            and not _matches(OUT_COLD_LEFT_TO_OTHERS, line) \
            and (_matches(OUT_COLD_FOUND, line) or not _matches(FIRST_PERSON, line)):
        _note(memory, "general")
        return pick(OUT_COLD_NIGHT_REPLY, memory)
    if _matches(ABUSE_OBJECTS, line) and _matches(ABUSE_OBJECTS_PERSON, line) \
            and not _matches(ABUSE_OBJECTS_OFF, line):
        _note(memory, "abuse")
        return pick(REPLIES["abuse"], memory)
    if isinstance(memory, dict) and memory.get("safety_case") in WISH_FRAMES \
            and (_matches(CRISIS_PLAN_SAID, line) or _matches(CRISIS_PLAN_CARRY, line)) \
            and not _matches(CRISIS_PLAN_ORDINARY, line):
        _note(memory, "self_harm")
        return pick(CRISIS_PLAN_REPLY, memory)
    minor = _minor(line, memory)
    if minor is not None and _a_real_injury_beside_the_plate(line):
        _note(memory, "minor")
        return _fit(pick(minor, memory), line, "minor")
    if _matches(BURNT_MARKS, line) and not _matches(PERSON_WORD, line) \
            and not _matches(BURN_MARK_ON_A_BODY, line):
        return None
    if _matches(OVERDOSE_FOOD, line) and not _matches(OVERDOSE_DRUG, line):
        return None
    if _matches(SEIZURE, line) and _matches(CHILDHOOD_FIT, line) and not _matches(
            URGENT_NOW, line) and not _matches(STILL_GOING, line) and not _matches(
            ANIMAL, line) and not _matches(FIT_STILL_RINGS, line):
        return None
    if _matches(SEIZURE, line) and _matches(FIT_THIS_WEEK, line) and (
            _matches(FIT_ALL_BETTER, line) or not _matches(URGENT_NOW, line)) and not _matches(
            STILL_GOING, line) and not _matches(FIT_STILL_RINGS, line) and not _matches(
            ANIMAL, line) and not _matches(CHILDHOOD_FIT, line) and not _matches(
            SEIZURE_STORY_GUARD, line):
        _note(memory, "general")
        return PAST_FIT_WEEK_REPLY
    if (_matches(CUT_MYSELF_OFF, line) and not _matches(
            DESPAIR + WISH_INTENT + SELF_HARM_INTENT + SELF_HARM_REASON + URGENT_NOW
            + OWN_WISH_WORDS + CRISIS_PLAN_SAID, line)
            and not CRISIS_WORD.search(line)):
        if _matches(ABUSE, line) or _matches(ABUSE_HIT_ME, line):
            _note(memory, "abuse")
            return _fit(pick(REPLIES["abuse"], memory), line, "abuse")
        return None
    if _an_accident_near_thing(line) and not _matches(
            FALL_RED + STILL_GOING + DESPAIR + WISH_INTENT + SELF_HARM_INTENT
            + CRISIS_PLAN_SAID, line) and not _matches(COUNTERFACTUAL_WISH, line):
        _note(memory, "near_thing")
        return _fit(pick(REPLIES[_near_thing_key(line)], memory), line, "near_thing")
    if not _matches(DEATH_IN_THE_LINE, line) \
            and not any(_matches(patterns, line) for name, patterns, _ in CASES
                        if name != "self_harm"):
        if _the_effort_frame(line):
            _note(memory, "near_thing")
            return _fit(pick(REPLIES[_near_thing_key(line)], memory), line, "near_thing")
        if _the_laugh(line):
            _note(memory, "laughing_kill")
            return _fit(pick(REPLIES["laughing_kill"], memory), line, "laughing_kill")
    _end_it_is_something_else = _matches(END_IT_WITH_A_THING, line) \
        and not _matches(END_IT_MEANS, line)
    _said_an_attempt = _matches(PAST_ATTEMPT, line) \
        and not _end_it_is_something_else and (
            _matches(PAST_ATTEMPT_STRONG, line) or not _matches(PAST_ATTEMPT_NOT, line))
    _said_a_past_wish = _matches(PAST_WISH, line) and not _matches(PAST_WISH_NOT, line)
    if not _said_a_past_wish and _matches(PAST_NEAR_ACT, line) \
            and not _matches(PAST_WISH_NOT, line) and not _matches(PAST_ATTEMPT_NOT, line):
        _said_a_past_wish = True
    _mine_and_undated = _matches(FIRST_PERSON, line) \
        and _matches(SPOKEN_ATTEMPT_UNDATED, line) \
        and not _end_it_is_something_else
    _scars_seen = _matches(SELF_HARM_SCARS, line) \
        and not _matches(SELF_HARM_SCARS_NOT, line)
    if _matches(COUNTERFACTUAL_WISH, line) and not _matches(ANIMAL, line) \
            and not _matches(PAST_WISH_NOT, line) \
            and not _matches(COUNTERFACTUAL_IDIOM, line):
        _note(memory, "self_harm")
        return _fit(pick(REPLIES["self_harm"], memory), line, "self_harm")
    if (_said_an_attempt or _said_a_past_wish or _scars_seen) and (
            _matches(OLD_TIME, line) or _matches(RECENT_TIME, line) or _mine_and_undated
            or _scars_seen or _matches(TEEN_AGE, line)) \
            and (not _matches(URGENT_NOW, line) or _said_an_attempt) \
            and not _matches(ANIMAL, line) \
            and not _idiom(line) \
            and not _matches(CUT_MYSELF_OFF, line) \
            and not (_matches(PAST_DEATH, line)
                     and not _matches(SELF_DEAD_FEELING, line)) \
            and not (not _matches(FIRST_PERSON, line) and _matches(LONG_AGO, line)
                     and not _matches(FIRST_PERSON_WISH, line)):
        _note(memory, "self_harm")
        if not _matches(FIRST_PERSON, line) and _matches(THIRD_PERSON_ACTOR, line) \
                and not _matches(FIRST_PERSON_WISH, line) \
                and not _matches(LONG_AGO, line):
            return pick(REPLIES["self_harm_other"], memory)
        return _fit(pick(REPLIES["self_harm"], memory), line, "self_harm")
    _remorse_after_hit = (_matches(I_HIT_SOMEONE, line)
                          and _matches(REMORSE_FOR_THE_ACT, line)
                          and not CRISIS_WORD.search(line)
                          and not _matches(WISH_OWN_BARE, line)
                          and not _self_harm_intent(line))
    _crisis_first = (_self_harm_intent(line) or _own_wish(line) or _matches(DESPAIR, line)
                     or bool(CRISIS_WORD.search(line)))
    if not (_crisis_first and not _remorse_after_hit):
        if _matches(I_HIT_SOMEONE, line) and not _matches(I_DID_NOT_HIT, line) \
                and not _matches(HIT_THING_NOT_PERSON, _norm(text)):
            _note(memory, "abuse")
            return _fit(pick(REPLIES["abuse_own"], memory), line, "abuse_own")
        if (_matches(HIT_AS_A_CHILD, line) and not _matches(CHILD_HIT_NOW, line)
                and not _matches(GAME_NOT_A_BLOW, line)):
            _note(memory, "abuse")
            return _fit(pick(REPLIES["abuse_past"], memory), line, "abuse_past")
    if (_matches(HANGED_DONE, line)
            and (_matches(DEATH_SAID, line) or _matches(ELDER_KIN, line)
                 or _matches(HANGED_LONG_AGO, line)
                 or (_matches(SCHOOL_PLACE, line) and not _matches(YOUNG_KIN, line))
                 or _matches(OLD_TIME, line) or _matches(RECENT_TIME, line))
            and not _matches(URGENT_NOW, line)
            and not _matches(OWN_WISH, line)
            and not _matches((r"\bfound\b", r"\bis\s+hanging\b", r"\bstill\b", r"\bnow\b",
                              r"\bhelp\b"), line)):
        _note(memory, "loss")
        return _fit(pick(REPLIES["death_already"], memory), line, "loss")
    if (_matches(FAINT_STORY, line) and _matches((r"\bout\s+cold\b",), line)
            and not _matches(OUT_COLD_NOW, line)
            and not _matches(OUT_COLD_WONT_WAKE, line)
            and not _matches(OUT_COLD_ASLEEP, line)
            and not _out_cold_knockout(line)
            and not _matches(ANIMAL, line)
            and not _matches(URGENT_NOW, line)
            and not _matches(OLD_TIME, line)):
        _note(memory, "general")
        return _fit(OUT_COLD_REPLY, line, "general")
    if _matches(OLD_TIME, line) and not _matches(URGENT_NOW, line) and not _matches(
            STILL_GOING, line) and not _hopeless(line) and not _matches(
            OWN_WISH, line) and not _withdrawal(line):
        if _matches(SEIZURE, line) and not _matches(FIT_ROUTINE, line) and not _matches(
                SEIZURE_STORY_GUARD, line) and not _matches(ANIMAL, line):
            _note(memory, "general")
            return PAST_FIT_REPLY
        if _matches(FAINT_STORY, line) and not _matches(ANIMAL, line):
            _note(memory, "general")
            return PAST_BLACKOUT_REPLY
        if _matches(ABUSE_DISCLOSURE, line) and not _matches(ABUSE_NOW, line) \
                and not _matches(ABUSE_DISCLOSURE_FINE, line) \
                and not _matches(ABUSE_FINE, line):
            _note(memory, "abuse")
            return _fit(pick(REPLIES["abuse_past"], memory), line, "abuse")
        if not (_matches(ABUSE_DISCLOSURE, line) and _matches(ABUSE_NOW, line)):
            return None
    if _matches(CPR_HOWTO, line) and _last_case(memory) not in CPR_SCENE_CASES and (
            not _matches(CPR_ROOM_EMPTY, line)
            or _matches(CPR_NO_PULSE, line)) and not _matches(CPR_NOT_EFFORT, line) and not _matches(
            CPR_NOT_A_BODY, line) and not _matches(CHEST, line) and not _matches(ANIMAL, line):
        _note(memory, "general")
        if _matches((r"\blearn|learning|course\b|class\b|training|qualification|certificate",
                     r"\bwhere\s+can\s+i\s+(?:do|take)\b"), line):
            _note(memory, "general")
            return None
        start = _matches((r"\bshould\s+i\s+(?:start|do|begin)\b", r"\bshall\s+i\s+start\b",
                          r"\bam\s+i\s+supposed\s+to\s+start\b"), line)
        if _matches(CPR_STILL_ALIVE, line) and not _matches(CPR_NOT_ALIVE, line):
            return pick(CPR_WHEN_ALIVE, memory)
        if _matches(CPR_NO_PULSE, line):
            return pick(CPR_NO_PULSE_NOW, memory)
        if _matches(CPR_BABY, line):
            return pick(CPR_BABY_SCENE if start else CPR_HOW_BABY, memory)
        if _matches(CPR_CHILD, line):
            return pick(CPR_CHILD_SCENE if start else CPR_HOW_CHILD, memory)
        if start:
            return pick(CPR_START, memory)
        return pick(CPR_HOW, memory)
    if _matches(LOCKED_IN_RISK, line):
        if re.search(r"\bm[y\s]*self\b", line):
            _note(memory, "self_harm")
            return pick(REPLIES["self_harm"], memory)
        _note(memory, "general")
        return pick(REPLIES["locked_in"], memory)
    if (_matches(OTHER_SELF_HARM, line) and not _matches(BLEEDING, line)
            and not _a_pet_hurting_itself(line)
            and not _a_reason_it_was_not_meant(line)
            and not _matches(FIRST_PERSON_WISH, line)):
        if _matches(PILLS_OVERDOSE, line):
            _note(memory, "poison")
            return _fit(pick(REPLIES["poison_other"], memory), line, "poison")
        _note(memory, "self_harm")
        return _fit(pick(REPLIES["someone_else"], memory), line, "someone_else")
    self_in_it = _matches(SELF_RUMINATION, line) and _matches(DEATH_WORDS, line)
    if ((_matches(SUICIDE_MENTION_CONTEXT, line) or _matches(SUICIDE_ABOUT_A_THING, line)
         or _matches(SUICIDE_LESSON, line))
            and not _matches(IDIOM, line)
            and not self_in_it
            and not _matches(FIRST_PERSON_WISH, line) and not _own_wish(line)):
        if (_matches(SUICIDE_LESSON, line) or (
                _matches(SUICIDE_MENTION_CONTEXT, line) and _matches((_LEARN_PLACE,), line))) \
                and not _matches(LOSS_SAID, line):
            _note(memory, "suicide_lesson")
            return _fit(pick(REPLIES["suicide_lesson"], memory), line, "suicide_lesson")
        return None
    if self_in_it:
        _note(memory, "self_harm")
        return _fit(pick(REPLIES["self_harm"], memory), line, "self_harm")
    own_distress = (_matches(OWN_WISH, line)
                    or (_hopeless(line) and not _someone_elses_despair(line))
                    or _matches(WISH_BY_MODAL, line)
                    or (_matches(OWN_DISTRESS, line) and not _matches(SUICIDE_TOPIC, line)))
    other_death = _matches(DEATH_REPORT, line) and not own_distress
    suicide_elsewhere = not own_distress and (
        other_death or _matches(SUICIDE_TOPIC, line) or _matches(SUICIDE_OTHER, line))
    denied_wish = (_denied_wish(line) or _matches(WISH_DEAD_OFF, line)
                   or _cut_off_idiom(line))
    topic_talk = (not _matches(OWN_WISH, line)
                  and _matches(SELF_HARM_TOPIC_OFF, line))
    intent = (_self_harm_intent(line)
              and not (_idiom(line) and not _rest_of_it_rings(line))
              and not suicide_elsewhere
              and not denied_wish
              and not topic_talk
              and not _matches(TALKS_ABOUT_IT + HELP_SOMEONE, line)
              and not _avoided(line, SELF_HARM_INTENT + SELF_HARM + SELF_HARM_DESERVE))
    if (intent and _matches(DYING_OTHER, line) and not _matches(SELF_OWN_DYING, line)
            and not _own_wish(line)):
        intent = False
    if FIGURATIVE_BREATH.search(line) and not intent:
        if BREATH_SETTLED.search(line):
            return None
        if not (_matches(CHEST, line) or _matches(BREATH_RED, line)
                or _matches(FIRE, line) or _matches(GAS_SMELL, line)
                or BREATH_ROOM_RED.search(line)):
            return _fit(pick(REPLIES["breath_panic"], memory), line, "panic")
    intent = (_self_harm_intent(line) and not _idiom(line)
              and not _matches(END_IT_ALL_JOKE, line)
              and not suicide_elsewhere
              and not denied_wish
              and not topic_talk
              and not _matches(TALKS_ABOUT_IT + HELP_SOMEONE, line)
              and not _matches(WISH_BY_MODAL_OFF, line))
    means_other = (_matches(END_MEANS_OTHER, line)
                   and (_matches(END_MEANS, line)
                        or _ends_it_with_a_method(line)
                        or _matches(END_HELPLESS, line))
                   and not _matches(FIRST_PERSON_WISH, line))
    accident = (_matches(ACCIDENT, line) and not intent
                and not _matches(SELF_HARM_REASON, line)
                and (not _matches(SELF_HARM_AGAIN, line) or _matches(CHORE_CAUSE, line)))
    if intent:
        if means_other:
            _note(memory, "self_harm")
            return pick(REPLIES["self_harm_other"], memory)
        if (_matches(SELF_HARM_BY_OTHER, line) and _a_reason_it_was_not_meant(line)
                and not _matches(FIRST_PERSON_WISH, line)
                and not re.search(r"\bself[-\s]?harm", line)):
            return None
        if (not _matches(FIRST_PERSON, line) and _matches(THIRD_PERSON_ACTOR, line)
                and _matches(PILLS_OVERDOSE, line)):
            _note(memory, "poison")
            return _fit(pick(REPLIES["poison_other"], memory), line, "poison")
        if ((_matches(OTHER_RISK, line) or _matches(SELF_HARM_BY_OTHER, line))
                and not _matches(FIRST_PERSON, line)
                and not _matches(IDIOM, line)
                and not _matches(SELF_HARM_TOPIC_OFF, line)
                and not re.search(r"\bend(?:ing)?\s+it" + END_IT_WITH, line)):
            if _matches(PILLS_OVERDOSE, line):
                _note(memory, "poison")
                return _fit(pick(REPLIES["poison_other"], memory), line, "poison")
            _note(memory, "self_harm")
            return pick(REPLIES["self_harm_other"], memory)
        if _matches(SELF_CUT, line) and (_matches(BLEEDING, line)
                                         or _matches(CUT_NOT_STOPPING, line)):
            _note(memory, "bleeding")
            return _fit(pick(REPLIES["self_cut_bleeding"], memory), line, "bleeding")
        if _someone_elses_despair(line):
            _note(memory, "self_harm")
            return pick(REPLIES["self_harm_other"], memory)
        _note(memory, "self_harm")
        return _fit(pick(REPLIES["self_harm"], memory), line, "self_harm")
    if (_matches(HURT_HIMSELF_BARE, line) and not _matches(HURT_HIMSELF_MEANT, line)
            and not _matches(BLEEDING, line) and not _a_reason_it_was_not_meant(line)
            and not _matches(FIRST_PERSON_WISH, line)
            and not re.search(r"\bm[y\s]*self\b", line)):
        _note(memory, "general")
        return pick(REPLIES["hurt_himself_asked"], memory)
    if means_other:
        _note(memory, "self_harm")
        return pick(REPLIES["self_harm_other"], memory)
    if (_matches(SELF_HARM_BY_OTHER, line) and not re.search(r"\bm[y\s]*self\b", line)
            and not _matches(SUICIDE_TOPIC, line)
            and not _matches(SELF_HARM_TOPIC_OFF, line)
            and not _matches(BLEEDING, line)
            and not _matches(FIRST_PERSON_WISH, line)
            and not _a_reason_it_was_not_meant(line)
            and not _matches(SELF_REASSURED, line) and not _matches(NOT_NOW, line)
            and not re.search(r"\bend(?:ing)?\s+it" + END_IT_WITH, line)):
        _note(memory, "self_harm")
        return pick(REPLIES["self_harm_other"], memory)
    reply = _hypo_reply(line, memory)
    if reply:
        return reply
    if _matches(PET_BREATH, line) and not _matches(HUMAN_TOO, line) \
            and not _matches(PET_EFFORT, line) \
            and _matches(BREATH_AT_REST + PET_CANT_SETTLE + PET_BREATH_NOW, line) \
            and not _matches(PET_CRISIS, line):
        return _fit(pick(REPLIES["pet_emergency"], memory), line, "pet_emergency")
    if _matches(PET_BREATH, line) and not _matches(HUMAN_TOO, line) \
            and not _matches(BREATH_RED + BREATH_AT_REST + PET_CRISIS + PET_EFFORT
                             + PET_CANT_SETTLE + (r"\bgums?\b",), line):
        _note(memory, "pet_breath_mild")
        return _fit(pick(REPLIES["pet_breath_mild"], memory), line, "pet_breath_mild")
    if (_matches(BREATH_SHORT + EFFORT_RECOVERY, line) and _matches(EXERTION_SMALL, line)
            and _matches(EFFORT_HEART_CLUSTER + EFFORT_SICK_PAIR + EFFORT_TRAVEL_PAIN, line)
            and not _matches(BREATH_RED, line) and not _matches(BREATH_AT_REST, line)
            and not _matches(CHEST, line) and not _matches(PAST_HARM, line)
            and not _matches(NOT_A_BREATHER + PET_WORDS, line)
            and not _matches(EFFORT_TOO_LONG, line)
            and not _matches(EFFORT_PATTERN, line) and not _matches(EFFORT_BENIGN, line)
            and not intent):
        if _matches(EFFORT_SOMEONE_ELSE, line):
            return _fit(pick(REPLIES["breath_exertion"], memory), line)
        if _matches(EFFORT_POSTURAL, line) and not _matches(EFFORT_TRAVEL_PAIN, line):
            return _fit(pick(REPLIES["breath_exertion"], memory), line)
        return _fit(pick(REPLIES["breath_effort_heart"], memory), line, "breath_effort_heart")
    if (_matches(BREATH_SHORT + EFFORT_RECOVERY, line) and _matches(EXERTION_SMALL, line)
            and _matches(EFFORT_SICK, line)
            and not _matches(BREATH_RED, line) and not _matches(BREATH_AT_REST, line)
            and not _matches(CHEST, line) and not _matches(PAST_HARM, line)
            and not _matches(NOT_A_BREATHER + PET_WORDS, line)
            and not _matches(EFFORT_BENIGN, line) and not _matches(EFFORT_PATTERN, line) \
            and not intent):
        return _fit(pick(REPLIES["breath_exertion"], memory), line)
    if (_matches(BREATH_SHORT + EFFORT_RECOVERY, line) and _matches(EXERTION_SMALL, line)
            and _matches(EFFORT_PATTERN, line)
            and not _matches(BREATH_AT_REST, line) and not _matches(CHEST, line)
            and not _matches(PAST_HARM, line) and not intent):
        return _fit(pick(REPLIES["breath_exertion"], memory), line)
    if _matches(BREATH_SHORT + EFFORT_RECOVERY, line) and _matches(EXERTION_SMALL, line) and             not _matches(BREATH_RED + EFFORT_RED_HEART, line) and not _matches(
            BREATH_AT_REST, line) and not _matches(
            CHEST, line) and not _matches(PAST_HARM, line) and not intent:
        return _fit(pick(REPLIES["breath_exertion"], memory), line)
    if _matches(BREATH_SHORT, line) and _matches(MEAL_BREATH, line) and not _matches(
            BREATH_RED, line) and not _matches(BREATH_AT_REST, line) and not _matches(
            CHEST, line) and not _matches(PAST_HARM, line) and not intent:
        return _fit(pick(REPLIES["breath_meal"], memory), line)
    if _matches(SHAKEN, line) and not _matches(SHAKEN_FINE, line):
        _note(memory, "shaken")
        return pick(SHAKEN_REPLY, memory)
    if _matches(CHOKE_WORDS, line) and not _matches(CHOKE_RED, line) \
            and not _matches(CHOKE_STILL_RED, line):
        return None
    if _matches(MILD_CHOKE, line) and not _matches(CHOKE_RED, line) \
            and not _matches(CHOKE_STILL_RED, line):
        return _fit(pick(REPLIES["mild_choke"], memory), line, "minor")
    if (_matches(WATER_DANGER, line)
            or (_matches(WATER_DROWNING_NOW, line) and not _matches(WATER_DROWNING_FINE, line))) \
            and (_matches(WATER_DANGER_PERSON, line) or _matches(WATER_DROWNING_NOW, line)) \
            and not (_matches(WATER_THING_DROPPED, line)
                     and not _matches(WATER_PERSON_TOO, line)) \
            and not _matches(WATER_NOT_A_PERSON, line) \
            and not (_matches(WATER_PET, line) and not _matches(WATER_HUMAN, line)) \
            and not (_matches(WATER_SELF_PUSH_FINE, line) and not _matches(URGENT_NOW, line)
                     and not _matches(WATER_BREATH_RED, line)
                     and not _matches(WATER_URGENT, line)) \
            and not (_matches(WATER_FINE, line) and not _matches(URGENT_NOW, line)) \
            and not (_matches(WATER_SWIM, line) and not _matches(WATER_URGENT, line)) \
            and not (_matches(WATER_HEAD_FEAR, line)
                     and not _matches(WATER_STILL_BAD, line)
                     and not _matches(WATER_IN_NOW, line)
                     and not _matches(WATER_BREATH_RED, line)) \
            and not (_matches(WATER_SELF_DIP, line) and not _matches(URGENT_NOW, line)
                     and not _matches(WATER_BREATH_RED, line)
                     and not _matches(WATER_URGENT, line)) \
            and not (_matches(WATER_STORY, line) and not _matches(URGENT_NOW, line)
                     and not _matches(WATER_URGENT, line)):
        _note(memory, "drowning")
        if _matches(WATER_SELF_DIP, line) or _matches(WATER_SELF, line):
            return _fit(pick(REPLIES["drowning_self"], memory), line, "drowning")
        return _fit(pick(REPLIES["drowning"], memory), line, "drowning")
    withdrawal = None if _matches(WITHDRAWAL_FIT_ITS_OWN_ANSWER, line) else _withdrawal(line)
    if withdrawal and _matches(WITHDRAWAL_ASK_DANGER, line):
        _note(memory, "alcohol_withdrawal")
        return pick(REPLIES["alcohol_withdrawal_danger"], memory)
    if withdrawal == "severe":
        _note(memory, "alcohol_withdrawal_severe")
        return pick(REPLIES["alcohol_withdrawal_severe"], memory)
    if withdrawal:
        _note(memory, "alcohol_withdrawal")
        return pick(REPLIES["alcohol_withdrawal"], memory)
    if (_matches(MILD, line) or _matches(FIGURATIVE, line)) and not _matches(FIRE_NOW, line) \
            and not _matches(NOT_WAKING_BESIDE, line) \
            and not _matches(DESPAIR + WISH_INTENT, line):
        if _matches(PAST_HARM, line) and not _matches(STILL_GOING, line):
            return None
        if _matches(SELF_REASSURED, line):
            return None
        wish_named = _matches(WISH_NAMED, line) and not _matches(SUICIDE_MENTION_CONTEXT, line) \
            and not _idiom(line)
        if not wish_named:
            return pick(minor, memory) if minor else None
    if (_matches(SOMEONE_ELSE_RISK, line)
            and (not _matches(_FIRST_PERSON_ME, line) or _matches(HELP_SOMEONE, line))
            and not _own_wish(line)
            and not _matches(IDIOM, line)
            and not re.search(r"\bend(?:ing)?\s+it\s+with\b", line)
            and not _a_reason_it_was_not_meant(line)
            and not _a_pet_hurting_itself(line)
            and not _an_ordinary_helping(line)):
        if _matches(HUMAN_ANCHOR, line) or _matches(PERSON_WORD, _person_before(memory)):
            _note(memory, "self_harm")
            return _fit(pick(REPLIES["someone_else"], memory), line, "someone_else")
    if (_matches(NOT_STOPPING_BARE, line) and _matches((r"\b(?:bleed\w*|blood)\b",), line)
            and re.search(r"\b(?:the|his|her|their|my|your)\s+(?:\w+\s+){0,2}bleed\w*\b", line)
            and not _matches(NOT_A_WOUND_OFF, line)
            and not _matches(WOUND_NAMED, line) and not _matches(BLEED_VOLUME, line)
            and not _matches((r"\bnoses?\b", r"\bnose\s*bleed\b", r"\bperiod\b"), line)
            and not _matches(MOUTH_BLEED_OFF, line)):
        return _fit(pick(REPLIES["bleeding_wont_stop"], memory), line, "minor")
    if _matches(MOUTH_BLEED, line) and _matches(MOUTH_BLEED_NOW, line) and not _matches(
            MOUTH_BLEED_RED, line) and not _matches(MOUTH_BLEED_OFF, line):
        return _fit(pick(REPLIES["mouth_bleed"], memory), line, "minor")
    thing_collapsed = _matches(THING_COLLAPSE, line) and not _matches(A_PERSON, line)
    own_injury = _matches(OWN_INJURY, line) and not _matches(SOMEONE_ELSE_OWN, line)
    own_despair = (_matches(DESPAIR, line) and _matches(FIRST_PERSON, line)
                   and not _matches(SOMEONE_ELSE_OWN, line))
    hypothetical = (_matches(NOT_NOW_FICTION, line) or _asking_about_the_world(line)
                    or (_matches(NOT_NOW, line) and not own_injury and not own_despair))
    pet_harm = (_matches(PET_HARM, line) or _matches((PET_WAKE,), line)) and not _matches(
        HUMAN_TOO, line) and not _matches(HUMAN_BITTEN, line)
    pet_past = _matches(PET_PAST, line) and not _matches(PET_NOW, line)
    pet_mild = _matches(PET_MILD, line) and not _matches(
        (r"\bcan'?t\s+breathe\b", r"\bnot\s+breathing\b", r"\bunconscious\b", r"\bseizure\b",
         r"\bchok\w*\b"), line)
    pet_all_right = (_matches(PET_FINE, line) or _matches(PET_ALL_RIGHT, line)) and not _matches(
        (r"\bcan'?t\s+breathe\b", r"\bnot\s+breathing\b", r"\bunconscious\b", r"\bseizure\b",
         r"\bchok\w*\b", r"\bbleeding\b", r"\bhit\s+by\b", r"\bran\s+over\b"), line)
    pet_gasp_explained = (_matches(PET_GASP_EXPLAINED, line)
                          and not _matches(PET_GASP_RED, line)
                          and not _matches(PET_GASP_ONGOING, line))
    pet_gasp_fine = (_matches(PET_GASP, line) and not _matches(PET_GASP_RED, line)
                     and (_matches(PET_GASP_FINE, line) or _matches(PET_GASP_NOUN, line)
                          or pet_gasp_explained
                          or (_matches(PET_GASP_SLEEP, line)
                              and _matches(PET_GASP_SLEEP_FINE, line))))
    pet_gasp = _matches(PET_GASP, line) and not pet_gasp_fine
    pet_gums_told = (_matches(PET_ANY, line) and not _matches(HUMAN_TOO, line)
                     and _matches(PET_MOUTH, line) and _matches(PET_GUMS_TOLD, line)
                     and not _matches(PET_EATEN_THING, line))
    if _matches(PET_APPOSITIVE, line) and (_matches(PET_CRISIS, line)
                                           or _matches(PET_BREATH, line)) \
            and not _matches(HUMAN_TOO, PET_APPOSITIVE_SUB.sub(" ", line)) \
            and not pet_past and not pet_all_right:
        kind = "pet_breath" if (_matches(PET_GASP, line)
                               or _matches(PET_BREATH_ODD, line)) else "pet_emergency"
        if _matches(PET_FIT, line):
            kind = "pet_fit"
        return _fit(pick(REPLIES[kind], memory), line, kind)
    if pet_harm and (_matches(PET_CRISIS, line) or pet_gasp) and not pet_all_right \
            and not pet_gums_told and not pet_past \
            and not pet_mild and not pet_gasp_fine and not (
            pet_all_right and _matches(PET_BEHAVIOUR, line)) and not (
            hypothetical and not _matches(CHOKE_NOW, line)):
        if _matches(PET_FIT, line):
            kind = "pet_fit"
        elif (_matches(PET_COLLAPSE, line) or _matches(PET_WAKE, line)
              or _matches((r"\bwak(?:e|ing)\s+up\b",
                           r"\b(?:won'?t|wont|can'?t|cannot|isn'?t|is\s+not|not)\s+wak\w*"),
                          line)) and not _matches(
                (r"\bcan'?t\s+breathe\b", r"\bnot\s+breathing\b", r"\bbleeding\b"), line):
            kind = "pet_collapse"
        elif (_matches(PET_GASP, line) or _matches(PET_BREATH_ODD, line)) \
                and not _matches(PET_EATEN_THING, line):
            kind = "pet_breath"
        else:
            kind = "pet_emergency"
        return _fit(pick(REPLIES[kind], memory), line, kind)
    if _matches(BITE_ON_ANIMAL, line) and not _matches(HUMAN_BITTEN, line) \
            and not _matches(FICTION_NOW, line) and not _matches(PET_LONG_AGO, line):
        kind = "pet_bitten_cat" if _matches((r"\b(?:cat|cats|kitten|kittens)\b",), line) \
            else "pet_bitten"
        return _fit(pick(REPLIES[kind], memory), line, kind)
    pet_own = _matches(PET_OWN, line) and not _matches(HUMAN_TOO, line)
    if pet_own and _matches(CHEST, line):
        return _fit(pick(REPLIES["pet_emergency"], memory), line, "pet_emergency")
    if _matches(GARDEN_WORDS, line):
        own_wish = _own_wish(_GO_ON_PHRASE.sub(" ", line)) \
            or _matches(GO_ON_LIVING, line)
    else:
        own_wish = _own_wish(line) or _matches(DESPAIR, line) \
            or _self_harm_intent(line)
    thing_dying = _matches(PET_WORDS + PLANT_WORDS + GARDEN_WORDS + AQUARIUM_WORDS, line) \
        and not _matches(HUMAN_TOO, line) and not own_wish
    other_dying = _matches(OTHER_DYING, line) and not own_wish
    if _effort_recovery(line) and not any(_matches(p, line) for _, p, _ in CASES):
        return _fit(pick(REPLIES["breath_effort"], memory), line, "breath_effort")
    before = _said_before(memory)
    if _matches(STRANGLED_SELF, line) and not _matches(STRANGLE_LOOKALIKE, line):
        _note(memory, "abuse")
        return _fit(pick(REPLIES["strangled_self"], memory), line, "strangled_self")
    hurt_is_a_pet = (_matches(PET_OWN + PET_WORDS, line) and not (
        _matches(HUMAN_TOO, line) or _matches(KICKED_PERSON, line)))
    for name, patterns, lookalike in (
            ("snake_bite", SNAKE_BITE, SNAKE_LOOKALIKE),
            ("animal_kick", ANIMAL_KICK, ANIMAL_KICK_LOOKALIKE),
            ("blind_cord", BLIND_CORD, ())):
        if _matches(patterns, line) and not (lookalike and _matches(lookalike, line)):
            if hurt_is_a_pet and name != "snake_bite":
                _note(memory, "pet_hurt")
                return _fit(pick(REPLIES["pet_hurt"], memory), line, "pet_hurt")
            _note(memory, name)
            return _fit(pick(REPLIES[name], memory), line, name)
    if _matches(NEAR_HIT_ON_A_ROAD, line) \
            and (_matches(NEAR_HIT_ON_A_ROAD_PLACE, line)
                 or _matches((_STRUCK_VEHICLE + r"\b",), line)) \
            and not _matches(NEAR_HIT_ON_A_ROAD_NOT, line):
        _note(memory, "near_thing")
        return _fit(pick(REPLIES[_near_thing_key(line)], memory), line, "near_thing")
    if _matches(STRUCK_MY_BIKE, line) and not _matches(STRUCK_BY_VEHICLE, line) \
            and not _matches(STRUCK_HYPOTHETICAL, line):
        if _matches(STRUCK_NOT_NOW, line):
            _note(memory, "near_thing")
            return _fit(pick(REPLIES[_near_thing_key(line)], memory), line, "near_thing")
        _note(memory, "struck_my_bike")
        return _fit(pick(REPLIES["struck_my_bike"], memory), line, "struck_my_bike")
    for name, patterns, needs_person in CASES:
        if not _matches(patterns, line):
            if not (name == "red_flags" and _glass_test_line(line, before)):
                continue
        if name == "self_harm" and _an_ordinary_helping(line):
            continue
        if name in ("wound_streak", "wound_streak_fever") \
                and _matches((r"\bchest\b", r"\bheart\b", r"\bbreastbone\b"), line) \
                and _matches(CHEST + CHEST_ADJ, line):
            continue
        if name == "crush":
            if _matches(CRUSH_OFF, line) and not _matches(CRUSH_HARD, line):
                continue
        if (name == "unconscious" and _matches(UNRESPONSIVE_MANNER, line)
                and not _matches(BODY_IN_THE_ROOM, line)):
            continue
        if (name == "unconscious" and _matches(PRO_NOT_ANSWERING, line)
                and not _matches(BODY_IN_THE_ROOM, line)):
            continue
            _note(memory, "crush")
            return _fit(pick(REPLIES["crush"], memory), line, "crush")
        if name == "struck_by_vehicle" and (
                _matches(STRUCK_NOT_NOW, line) or _matches(STRUCK_HYPOTHETICAL, line)):
            if _matches(STRUCK_BY_A_VEHICLE, line) \
                    and not _matches(STRUCK_BY_A_VEHICLE_NOT, line) \
                    and not _matches(STRUCK_HYPOTHETICAL, line) \
                    and not _matches(STILL_GOING + DESPAIR + WISH_INTENT + SELF_HARM_INTENT
                                     + CRISIS_PLAN_SAID, line):
                _note(memory, "near_thing")
                return _fit(pick(REPLIES[_near_thing_key(line)], memory), line, "near_thing")
            continue
        if (name in ("fire", "clothes_fire", "vehicle_fire")
                and _a_fire_that_did_not_happen(line)
                and not _matches(FIRE_DRILL, line) and not _minor(line, memory)):
            _note(memory, "near_fire")
            return _fit(pick(REPLIES["near_fire"], memory), line, "near_fire")
        if name == "insect_bite" and _matches(INSECT_BITE_NEEDS_A_LOOK, line):
            continue
        if name == "trapped_vehicle" and _matches(TRAPPED_VEHICLE_NOT_NOW, line):
            continue
        if name == "trapped_vehicle" and TRAPPED_HELD_BY_A_PERSON.search(line):
            continue
        if (name == "trapped_vehicle" and TRAPPED_SELF_STUCK.search(line)
                and not TRAPPED_NOT_A_WAIT.search(line)):
            continue
        if (name == "struck_by_vehicle" and _matches(PET_WORDS, line)
                and not _matches(HUMAN_TOO, line)):
            _note(memory, "pet_hurt")
            return _fit(pick(REPLIES["pet_hurt"], memory), line, "pet_hurt")
        if (name in FEVER_CASES and _matches(TEMP_FALLING_WEATHER, line)
                and not _matches(FEVER_NOT_THE_WEATHER, line)):
            continue
        if name == "chest" and _matches(CHEST_ANSWERED_ELSEWHERE, line):
            continue
        if name in ("breathing", "breath_weeks", "breath_past") \
                and _matches(LAUGH_WORD, line) and _matches(LAUGH_TAKES_BREATH, line) \
                and not _matches(BREATH_RED + BREATH_AT_REST + LAUGH_BREATH_RED
                                 + LAUGH_OTHER_PERSON, line):
            _note(memory, "breath_laugh")
            return _fit(pick(REPLIES["breath_laugh"], memory), line, "breath_laugh")
        if name in ("breathing", "breath_weeks", "breath_past") \
                and _matches(HEAT_CAUSE, line) and _matches(BREATH_BARE, line) \
                and not _matches(HEAT_NOT_WEATHER, line) \
                and not _matches(BREATH_RED + BREATH_AT_REST + HEAT_BREATH_RED, line):
            _note(memory, "breath_heat")
            return _fit(pick(REPLIES["breath_heat"], memory), line, "breath_heat")
        if name == "breath_past" and _matches(PET_OWN, line) and not _matches(HUMAN_TOO, line):
            return _fit(pick(REPLIES["pet_emergency"], memory), line, "pet_emergency")
        if name == "breath_past" and not _matches(BREATH_PAST_CUE, line) and not _matches(
                (CHILD_WORD,), line):
            continue
        if name == "breath_past" and _matches(BREATH_PAST_OVER, line) and not _matches(
                BREATH_RED, line):
            continue
        if name == "breath_past" and (_matches(BLUE_LIPS_FACE, line) or (
                _matches(BLUE, line) and _matches(PERSON_WORD, line)
                and not _matches(BLUE_FOOD, line) and not _matches(BLUE_COLD_SELF, line))):
            continue
        if name in ("drowning", "water_danger") and _matches(DROWNED_THING, line):
            continue
        if name == "cut" and _cut_off_idiom(line):
            continue
        if (name == "self_harm" and _matches(PET_DYING, line)
                and not _matches((r"\bi\s+(?:want|wanna|need|might|will|could|should|do)\b",
                                  r"\bmy\s*self\b", r"\bme\s+too\b", r"\bwith\s+him\b",
                                  r"\bwith\s+her\b"), line)
                and not _matches(DESPAIR + WISH_INTENT, line) and not _own_wish(line)):
            return _fit(pick(REPLIES["pet_loss"], memory), line, "pet_loss")
        if name == "self_harm" and ((thing_dying and not _a_wish_for_their_own_body(line))
                                   or other_dying or suicide_elsewhere
                                   or denied_wish or topic_talk):
            continue
        if name == "pan_fire" and _matches(PAN_FIRE_SPREAD, line):
            continue
        if (name == "fire" and (_matches(BATTERY_FIRE, line) or _matches(DEVICE_BURNING, line))
                and not _matches(ROOM_OR_HOUSE, line)):
            continue
        if (name == "fire" and _matches(BURNT_FOOD, line) and not _matches(FIRE_OUT, line)
                and not _matches(BATTERY_FIRE, line)):
            continue
        if (name == "fire" and _matches(FLAMES_NOT_FIRE, line)
                and not _matches(FIRE_ELSEWHERE, line)):
            continue
        if name in ("dog_attack", "dog_bite") and _matches(DOG_HABIT, line) \
                and not _matches(DOG_ATTACK_NOW, line) and not _matches(DOG_BLEED, line) \
                and not _matches(BITE_DONE, line):
            continue
        if name in ("dog_attack", "dog_bite") and _matches(DOG_MOUTHING, line) \
                and not _matches(DOG_ATTACK_NOW, line) and not _matches(DOG_BLEED, line):
            continue
        if (name == "vehicle_fire" and _matches(VEHICLE_NOT_FIRE, line)
                and not _matches(VEHICLE_STILL_FIRE, line)):
            continue
        if name in ("vehicle_fire", "fire") and _matches(VEHICLE_BURNING_SMELL, line) \
                and not _matches(VEHICLE_BURNING_SMELL_HARD, line):
            continue
        if name in ("vehicle_fire", "fire") and _matches(VEHICLE_FIRE_OVER, line) \
                and not _matches(VEHICLE_FIRE_OVER_HARD, line):
            continue
        if name in ("vehicle_fire", "fire") and _matches(VEHICLE_BURNING_A_PERSON, line) \
                and not _matches(VEHICLE_BURNING_A_PERSON_HARD, line):
            continue
        if (name == "fire" and _matches(VEHICLE_NOT_FIRE, line)
                and not _matches(VEHICLE_EXHAUST_HARD, line)):
            continue
        if (name == "fire" and _matches(VEHICLE_EXHAUST, line)
                and not _matches(VEHICLE_EXHAUST_HARD, line)):
            continue
        if name == "fire" and not _matches(FIRE_SCALE, line) and (
                _matches(APPLIANCE_SMOKE, line) or _matches(ALARM_NUISANCE, line)):
            continue
        if (name == "fire" and _matches(SMOKE_IS_A_SMELL, line)
                and SMELL_ON_A_THING.search(line) and not _matches(ROOM_OR_HOUSE, line)
                and not _matches(FIRE_SCALE, line) and not _matches(ALARM_NUISANCE, line)):
            continue
        if name == "abuse" and _hit_by_a_loss(line) and not _matches(ABUSE_NOT_HIT, line):
            continue
        if name in ("dog_bite", "dog_attack") and not _matches(HUMAN_TOO, line) \
                and not _matches(DOG_BIT_A_PERSON, line) \
                and (_matches(DOG_SELF_BITE, line)
                     or (_matches(PET_OWN, line) and _matches(DOG_ITCH, line))):
            continue
        if name == "hanging" and _matches(STRANGLE_LOOKALIKE, line):
            continue
        if name == "self_harm" and _avoided(line, SELF_HARM):
            continue
        if name == "self_harm" and re.search(A_HURT_OF_A_BODY_PART, line) \
                and re.search(A_WORKOUT_CUE, line):
            continue
        if (name == "self_harm" and MONEY_NAMED.search(line) and _matches(NOTHING_LEFT, line)
                and not SOMEONE_HOLDS_THE_MONEY.search(line)
                and not _matches(DESPAIR_WITHOUT_NOTHING_LEFT + WISH_INTENT + SELF_HARM_INTENT,
                                 line)):
            continue
        if name == "stroke" and not _matches(STROKE, line) \
                and _matches(SIGHT_WORD, line) and _matches(SIGHT_A_WHILE, line):
            _note(memory, "sight_days")
            return _fit(pick(REPLIES["sight_days"], memory), line, "sight_days")
        if (name == "stroke" and _matches(STROKE_HAND, line)
                and _matches(STROKE_HAND_SELF, line)
                and not _matches(STROKE_HAND_OTHER, line)):
            continue
        if (name == "stroke" and _matches(STROKE_HAND, line)
                and _matches(STROKE_HAND_CHRONIC, line)
                and not _matches(STROKE_HAND_HARD, line)):
            continue
        if name == "stroke" and not _matches(STROKE, line) \
                and _matches(PET_SUBJECT + PET_SUBJECT_PLURAL, line) \
                and not _matches(HUMAN_TOO + MY_OWN_PART, line):
            if _matches(PET_WEAK, line):
                _note(memory, "pet_weak")
                return _fit(pick(REPLIES["pet_weak"], memory), line, "pet_weak")
            continue
        if name == "stroke" and not _matches(STROKE, line) and _matches(STROKE_WEAK_OFF, line) \
                and not _matches(STROKE_FAST, line):
            continue
        if name == "stroke" and not _matches(STROKE, line) \
                and _matches(PET_SUBJECT, line) and _matches(PET_SIGHT, line) \
                and not _matches(FIRST_PERSON, line) and not _matches(HUMAN_ANCHOR, line):
            continue
        if name == "puncture" and _matches(PUNCTURE_OFF, line):
            continue
        if name == "baby_fell" and _head_bang(line):
            continue
        if name == "baby_fell" and _matches(BABY_FELL_OFF, line) \
                and not _matches(BABY_FELL_SURFACE, line):
            continue
        if name == "baby_fell" and _matches(BABY_FELL_RED, line):
            _note(memory, "baby_fell_red")
            return _fit(pick(REPLIES["baby_fell_red"], memory), line, "baby_fell_red")
        if name == "baby_fell" and _matches(BABY_FELL_OVER, line):
            continue
        if name == "gas_left" and _matches(ELECTRIC_COOKER, line) and not _matches(GAS_WORD, line):
            continue
        if pet_harm and name in ("breathing", "bleeding", "poison", "swallowed_thing", "seizure",
                                 "unconscious", "broken", "hypo", "chest", "stroke", "heat",
                                 "hanging", "fall", "bone_throat"):
            continue
        if name == "bleeding" and _matches(NOSE_SITE, line) and not _matches(NOSE_RED, line) \
                and not _matches((r"\b(?:cut|gash|gashes|wound|wounds|sliced|stabbed|graze[ds]?)\b",),
                                 line):
            continue
        if name == "breathing" and not _matches(BREATH_AT_REST, line) and _matches(
                BREATH_CAUSE, line) and not _matches(BREATH_CAUSE_RED, line):
            _note(memory, "breath_cause")
            if not (_matches(NIGHT_BREATH, line) and _matches(BREATH_CAUSE, line)):
                return _fit(pick(REPLIES["breath_cause"], memory), line, "breath_cause")
            continue
        if name == "breathing" and _matches(NIGHT_BREATH, line) \
                and not _matches(NIGHT_BREATH_RED, line):
            continue
        if name == "chest" and _matches(NOT_BREATHING_NOW, line):
            continue
        _gasp_stripped = re.sub(r"\bgasp\w*", "", line, flags=re.I)
        if name == "breathing" and _matches(GASPING_THIRST, line) \
                and not _matches(BREATH_RED + BREATH_STILL_RED, _gasp_stripped):
            continue
        if name == "breathing" and _matches(NOT_BREATHING_NOW, line):
            _note(memory, "not_breathing")
            if _matches(CPR_BABY, line):
                return _fit(pick(CPR_BABY_SCENE, memory), line, "not_breathing")
            if _matches(CPR_CHILD, line):
                return _fit(pick(CPR_CHILD_SCENE, memory), line, "not_breathing")
            return _fit(pick(REPLIES["not_breathing"], memory), line, "not_breathing")
        if name in ("breathing", "breath_weeks", "breath_past") and _effort_recovery(line):
            return _fit(pick(REPLIES["breath_effort"], memory), line, "breath_effort")
        if (name in ("breathing", "breath_weeks", "breath_past")
                and _matches(BREATH_LAUGH, line)
                and not _matches(BREATH_RED + BREATH_STILL_RED + LAUGH_BREATH_RED
                                 + LAUGH_OTHER_PERSON, line)
                and not _matches(BREATH_AT_REST, line)
                and not _matches((r"\bstill\b", r"\bright\s+now\b"), line)):
            return _fit(pick(BREATH_LAUGH_REPLY, memory), line)
        if name == "breathing" and _matches(EXERTION, line) and not _matches(BREATH_RED, line):
            continue
        if (name == "breathing" and _matches(SHORT_OF_BREATH, line)
                and _matches(EFFORT_ANYWHERE, line) and not _matches(BREATH_RED, line)
                and (_matches(OUT_OF_BREATH, line) or not _matches(EFFORT_WEAK, line))):
            continue
        if (name == "breathing" and _matches(NOT_A_BREATHER, line)
                and not _matches(A_BREATHER, line) and not _matches(BREATH_RED, line)):
            continue
        if (name == "breathing" and _matches(BREATH_OVER, line)
                and not _matches(BREATH_RED + BREATH_STILL_RED, line)
                and not _matches((r"\bstill\b", r"\bright\s+now\b"), line)
                and not _matches(CHOKE_HELP, line)):
            return _fit(pick(REPLIES["breath_past"], memory), line, "breath_past")
        if (name == "breathing" and _matches(TALK_HABIT, line)
                and not _matches(BREATH_RED + BREATH_STILL_RED, line)):
            continue
        if (name == "breathing" and _matches(CHRONIC_BREATH, line)
                and not _matches(BREATH_RED + BREATH_STILL_RED, line)):
            return _fit(pick(REPLIES["breath_weeks"], memory), line, "breath_weeks")
        if name in ("breathing", "breath_past", "bone_throat", "bone_throat_red") and _matches(
                CHOKE_OVER, line) and not _matches(CHOKE_NOW, line):
            if (_matches(CHOKE_PERSON, line) and not _matches(CHOKE_NOT_PERSON, line)
                    and not _matches(CHOKE_HABIT, line)):
                _note(memory, "choking")
                return _fit(pick(REPLIES["mild_choke"], memory), line, "minor")
            continue
        if name == "breathing" and _matches(CHOKE_NOT_PERSON, line) \
                and not _matches(CHOKE_PERSON, line) and not _matches(CHOKE_NOW, line):
            continue
        if (name in ("breathing", "stroke") and _matches(CHOKE_HELP, line)
                and not _matches(PET_HARM, line)
                and not (_matches(CHOKE_NOT_PERSON, line)
                         and not _matches(CHOKE_PERSON, line))):
            if _matches(CHOKE_PREVENT, line):
                return _fit(pick(REPLIES["choke_prevent"], memory), line, "minor")
            if _matches(CHOKE_AIR_OK, line) or _matches(CHOKE_SETTLED, line):
                _note(memory, "choking")
                return _fit(pick(REPLIES["mild_choke"], memory), line, "minor")
            if _matches(CHOKE_BABY, line):
                _note(memory, "choking")
                return _fit(pick(REPLIES["choking_baby"], memory), line, "breathing")
            kind = "choking_self" if _matches(FIRST_PERSON, line) \
                and not _matches(CHOKE_PERSON, line) else "choking_help"
            _note(memory, "choking")
            return _fit(pick(REPLIES[kind], memory), line, "breathing")
        if _matches(BONE_PAST, line) and not _matches(BONE_STILL, line) and _matches(
                BONE_THROAT, line) and not _matches(BONE_RED, line):
            continue
        if name == "bone_throat":
            if _matches(BONE_ORDINARY, line) and not _matches(BONE_RED, line):
                continue
            if _matches(BONE_RED, line):
                return _fit(pick(REPLIES["bone_throat_red"], memory), line, "bone_throat")
        if name == "self_harm" and _matches(WORLD_QUESTION, line) and not _matches(
                (r"\bi\b", r"\bmy\b", r"\bmyself\b"), line):
            continue
        if name == "child_drank" and _matches(CHILD_DRANK_WEAK, line) and not _matches(
                CHILD_YOUNG, line):
            continue
        if name == "slur_drink" and _matches(SLUR_RED_BESIDE, line):
            _note(memory, "stroke")
            return _fit(pick(REPLIES["stroke"], memory), line, "stroke")
        if name == "slur_small_child":
            if _matches(SLUR_RED_BESIDE, line) or _matches((r"\bfit\b", r"\bfever\b", r"\brash\b"), line):
                _note(memory, "stroke")
                return _fit(pick(REPLIES["stroke"], memory), line, "stroke")
            return _fit(pick(REPLIES["slur_small_child"], memory), line)
        if name == "dental_numb":
            if _matches(DENTAL_NUMB_RED, line):
                _note(memory, "stroke")
                return _fit(pick(REPLIES["stroke"], memory), line, "stroke")
            _note(memory, "dental_numb")
            return _fit(pick(REPLIES["dental_numb"], memory), line)
        if name == "stroke" and _matches((r"\bchok(?:ed|ing|es)\b",), line):
            continue
        if name in ("breathing", "breath_weeks", "breath_past") and _matches(GASP_FINE, line) and not _matches(GASP_RED, line):
            continue
        if name == "abuse" and _matches(PURSUIT_FINE, line) and not _matches(ABUSE_PURSUIT_HARD, line):
            continue
        if name == "abuse" and _matches(ABUSE_FINE, line) \
                and not (_matches(ABUSE_PARENT_REFUSAL, line)
                         and _matches(PARENT_REFUSAL_BLOW, line)) \
                and not (_matches(ANY_REFUSAL_TO_GO, line)
                         and _matches(A_HAND_ON_THE_PERSON, line)):
            continue
        if name == "abuse" and _matches(ABUSE_VERBAL_FINE, line) \
                and not _matches(ABUSE_BLOW, line) \
                and not (_matches(ABUSE_HIT_ME, line)
                         and not _matches(CHILD_AGGRESSOR, line)):
            continue
        if name == "abuse" and _matches(SOFT_FACE_PUSH, line) \
                and not _matches(SOFT_FACE_STOP, line):
            continue
        if (name == "abuse" and _matches(PLAYFUL_HIT, line)
                and not _matches(ADULT_HIT, line)):
            continue
        if (name == "abuse" and _matches(PUSHED_AWAY, line)
                and not _matches(BLOW_ON_ME, line) and not _matches(ADULT_HIT, line)
                and not _matches(RESTRAINT_BESIDE, line)):
            if _matches(PUSHED_AWAY_THEN_RESTRAINT, line):
                pass
            elif _matches(PUSHED_AWAY_BUT_SOMETHING_ELSE, line):
                continue
            else:
                return _fit(pick(PUSHED_AWAY_REPLY, memory), line)
        if name == "abuse" and _matches(ABUSE_EMPLOYER_REFUSAL, line) \
                and not _matches(ABUSE_PARENT_REFUSAL_HARD, line) \
                and not _matches(PARENT_REFUSAL_BLOW, line) \
                and not _matches(ABUSE_HANDS_ON, line) \
                and not _matches(ABUSE_PARTNER_DID_IT, line):
            continue
        if name == "abuse" and _matches(ABUSE_CHILD_REFUSAL, line) \
                and not _matches(ABUSE_CHILD_TAKES_MONEY, line) \
                and not _matches(PARENT_REFUSAL_BLOW, line) \
                and not _matches(ABUSE_HANDS_ON, line):
            continue
        if name == "abuse" and _matches(ABUSE_PARENT_REFUSAL, line) \
                and not _matches(ABUSE_PARENT_REFUSAL_HARD, line) \
                and not _matches(ABUSE_HANDS_ON, line) \
                and not _matches(ABUSE_PARTNER_DID_IT, line):
            continue
        if name == "abuse" and _matches(HIT_IN_FUN, line) \
                and not _matches(HIT_IN_FUN_HARD, line) \
                and not _matches(HIT_THE_LAUGH_IS_HIS, line) \
                and not _matches(HIT_WITH_A_THING, line):
            _note(memory, name)
            return _fit(pick(REPLIES["hit_in_fun"], memory), line, name)
        if name == "abuse" and _matches(ABUSE_FINE_PLACE, line) \
                and not _matches(VIOLENT_THREAT, line):
            continue
        if name == "abuse" and _matches(ABUSE_MEMORY, line) and not _matches(ABUSE_NOW, line):
            _note(memory, name)
            return _fit(pick(REPLIES["abuse_past"], memory), line, name)
        if name == "abuse" and _matches(ABUSE_PLAY, line) \
                and not _matches(ABUSE_PLAY_HARD, line):
            continue
        if name == "abuse" and _matches(ABUSE_ROOM_FAMILY, line) \
                and not _matches(ABUSE_ROOM_CARD, line) \
                and not _matches(ABUSE_HANDS_ON, line):
            continue
        if name == "abuse" and _matches(ABUSE_QUARREL, line) \
                and not _matches(ABUSE_BLOW, line) \
                and not _matches(ABUSE_HANDS_ON, line):
            continue
        if name == "abuse" and _matches(ABUSE_BUTTONHOLED, line) \
                and not _matches(ABUSE_BLOW, line) \
                and not _matches(ABUSE_ROOM_CARD, line) \
                and not _matches(ABUSE_HANDS_ON, line):
            continue
        if name == "abuse" and _matches(ABUSE_KIDS_AT_HOME, line) \
                and not _matches(ABUSE_KIDS_CARD, line) \
                and not _matches(ABUSE_HANDS_ON, line) \
                and not _matches(ABUSE_PARTNER_DID_IT, line):
            continue
        if name == "abuse" and _matches(ABUSE_BENIGN_REASON, line) \
                and not _matches(ABUSE_BLOW, line) \
                and not _matches(ABUSE_PARTNER_DID_IT, line):
            continue
        if name == "abuse" and _matches(ABUSE_FINE_ANIMAL, line) \
                and not PERSON_AS_ATTACKER.search(line):
            continue
        if (name == "abuse" and _matches(LENDER_FINE, line)
                and not _matches(NAMED_PERSON, line)):
            continue
        if (name == "abuse" and _a_small_child_did_it(line, memory)
                and not _matches(ADULT_HIT, line)
                and not _matches(A_REAL_DANGER, line)
                and not _matches(HIT_WITH_A_THING, line)
                and not _matches(ABUSE_CHILD_TAKES_MONEY, line)):
            if (A_SMALL_CHILD_LASHES_OUT.search(line)
                    and (not A_SMALL_CHILD_SAID.search(line)
                         or A_GRANDCHILD_OF_AN_AGE.search(line))):
                return _fit(pick(SMALL_CHILD_LASH_REPLIES, memory, line), line,
                            "small_child")
            continue
        if name == "self_harm" and accident:
            continue
        if name == "self_harm" and _idiom(line):
            continue
        if (name == "self_harm" and _matches(DYING_OTHER, line)
                and not _matches(SELF_OWN_DYING, line)
                and not _matches(DESPAIR + WISH_INTENT, line)
                and not _own_wish(line)):
            continue
        if name == "self_harm" and _matches(END_IT_ALL_JOKE, line):
            continue
        if name == "self_harm" and _matches(WISH_BY_MODAL_OFF, line):
            continue
        if name == "self_harm" and _ending_a_thing(line):
            continue
        if name == "self_harm" and _overdose_of_a_treat(line):
            continue
        if name == "poison" and _matches(DOSE_REGULAR, line) and not _matches(
                (r"\btoo\s+many\b", r"\ball\s+(?:of\s+)?(?:my|his|her|their)\b", r"\boverdos\w*",
                 r"\bhandful\b", r"\bwhole\s+(?:packet|pack|box|bottle)\b"), line):
            continue
        if name == "poison" and _a_days_dose(line):
            continue
        if name == "poison" and _overdose_of_a_treat(line):
            continue
        if name == "poison" and _matches(PACK_FINE, line) and not _matches(
                (r"\boverdos\w*", r"\btoo\s+many\b", r"\bsweat", r"\bunconscious\b"), line):
            continue
        if name == "poison" and _matches(MILD_PRODUCT_SMALL, line) \
                and not (_matches(MILD_TAKEN_BY_A_CHILD, line)
                         and not _matches(MILD_HARMLESS, line)) \
                and (_matches(A_SMALL_AMOUNT, line) or _matches(MILD_HARMLESS, line)) \
                and not _matches(MILD_PRODUCT_BIG, line) \
                and not _matches(FUEL_AND_SOLVENT, line):
            continue
        if name == "self_harm" and _matches(PILLS_OVERDOSE, line) \
                and not _overdose_of_a_treat(line):
            _note(memory, "poison")
            return _fit(pick(REPLIES["poison"], memory), line, "poison")
        if name in ("seizure", "recent_fit") and _matches(SEIZURE_STORY_GUARD, line) \
                and not _matches(FIT_STILL_RINGS, line) and not _matches(ANIMAL, line):
            continue
        if name == "heard_assault" and _matches(HEARD_ASSAULT_OFF, line):
            continue
        if name == "poison" and _matches(TOOK_OUT_OF, line) \
                and not _matches(POISON_SWALLOW_VERB, line):
            continue
        if name == "foraged" and _matches(FORAGED_FINE, line):
            continue
        if name == "allergy_now" and (hypothetical or _matches(ALLERGY_SIGN_NAMED, line)):
            continue
        if name == "tick_bite" and _matches(TICK_ALREADY, line):
            continue
        if name == "lips_swell" and _matches(LIPS_SWELL_OFF, line):
            continue
        if name == "lips_swell_bare" and _matches(LIPS_SWELL_BARE_OFF, line):
            continue
        if (name in ("lips_swell_bare", "lips_tingle") and not _matches(SWELLING_NOW, line)
                and not _matches(AIRWAY_CHANGED, line)
                and (_matches(STING_SETTLED, line)
                     or (_matches(STING_MILD, line) and not _matches(STING_WINGED, line)))):
            continue
        if name == "lips_tingle":
            if (_matches(LIPS_TINGLE_OFF, line) and not _matches(LIPS_TINGLE_BREATH, line)
                    and not _matches(SWELLING_NOW, line)):
                continue
            if (_matches(THROAT_THICK, line) and _matches(MOUTH_TINGLE, line)
                    and not _matches(LIPS_TINGLE_OFF, line)):
                return _fit(pick(REPLIES["lips_swell_bare"], memory), line, "lips_swell")
            if (_matches(SPICY_MOUTH, line) and not _matches(LIPS_TINGLE_BREATH, line)
                    and not _matches(SWELLING_NOW, line)):
                continue
            if (_matches(LIPS_NUMB, line) and not _matches(LIPS_TINGLE_SAID, line)
                    and not _matches(SWELLING_NOW, line)):
                continue
            if (_matches(LIPS_LIMB_TOO, line) and not _matches(LIPS_TINGLE_BREATH, line)
                    and not _matches(LIPS_TINGLE_TRIGGER, line)):
                continue
            if (not (_matches(LIPS_TINGLE_TRIGGER, line) or _matches(LIPS_TINGLE_RED, line)
                     or _matches(LIPS_TINGLE_FOOD, line))
                    and _matches(LIPS_TINGLE_MOUTH, line)
                    and not _matches(LIPS_TINGLE_ELSEWHERE, line)):
                _note(memory, "general")
                return _fit(pick(REPLIES["lips_tingle_alone"], memory), line, "lips_swell")
            if not (_matches(LIPS_TINGLE_TRIGGER, line) or _matches(LIPS_TINGLE_RED, line)
                    or _matches(LIPS_TINGLE_FOOD, line)):
                continue
            if _matches(LIPS_TINGLE_RED, line):
                return _fit(pick(REPLIES["lips_swell_bare"], memory), line, "lips_swell")
            _note(memory, "general")
            return _fit(pick(REPLIES["lips_tingle"], memory), line, "lips_swell")
        if name == "allergy_food":
            if _matches(ALLERGY_OFF, line) and not _matches(ALLERGY_AIRWAY, line):
                continue
            sting = _matches(STING_WORDS, line) and not _matches(FOOD_WORDS, line)
            if _matches(ALLERGY_AIRWAY, line) or (sting and _matches(ALLERGY_FACE, line)):
                _note(memory, "lips_swell")
                return _fit(pick(REPLIES["lips_swell_bare"], memory), line, "lips_swell")
            kind = "sting_watch" if sting else "allergy_watch"
            _note(memory, kind)
            return _fit(pick(REPLIES[kind], memory), line, kind)
        if name in ("lips_swell", "lips_swell_bare") and _matches(
                THROAT_TIGHT, line) and not _matches(THROAT_TIGHT_RED, line):
            continue
        if name in ("lips_swell", "lips_swell_bare") and _matches(
                THROAT_TIGHT_MILD, line) and not _matches(THROAT_TIGHT_RED, line):
            continue
        if name == "throat_tight":
            if _matches(THROAT_TIGHT_CAUSE, line) and not _matches(THROAT_TIGHT_RED, line):
                if _matches(THROAT_TIGHT_EFFORT, line):
                    _note(memory, "general")
                    return _fit(pick(REPLIES["throat_exertion"], memory), line, "throat_tight")
                continue
            _note(memory, "general")
            return _fit(pick(REPLIES["throat_tight"], memory), line, "throat_tight")
        if name == "swallow_gone":
            if _matches(SWALLOW_GONE_OFF, line) or _matches(SWALLOW_GONE_BREATH, line):
                continue
            if _matches(SWALLOW_GONE_RED, line):
                _note(memory, "general")
                return _fit(pick(REPLIES["lips_swell_bare"], memory), line, "lips_swell")
            _note(memory, "general")
            return _fit(pick(REPLIES["swallow_gone"], memory), line, "swallow_gone")
        if name in ("breathing", "breath_weeks", "breath_past") and _matches(BREATH_EFFORT, line) \
                and not _matches(BREATH_EFFORT_RED, line):
            continue
        if name == "spiked" and _matches(SPIKED_STAND_DOWN, line):
            continue
        if name == "fall_check" and _matches(HEAD_BANG, line):
            continue
        if name == "fall_check" and _matches(FALL_STROKE_SIGN, line) \
                and not _matches(SLUR_NOT_A_STROKE_WORDS, line):
            continue
        if name == "fall_check" and _fall_with_sign(line):
            continue
        if name == "fall_check" and (_matches(HEAD_KNOCKOUT, line)
                                     or _out_cold_knockout(line)):
            continue
        if name == "fall_check" and _matches(FALL_ANSWERED, line):
            if _matches(FALL_NOT_BREATHING, line):
                return _fit(pick(REPLIES["not_breathing"], memory), line, "not_breathing")
            _note(memory, "general")
            return _fit(pick(REPLIES["unconscious"], memory), line, "unconscious")
        if name == "fall_check" and _matches(BABY_FELL, line) \
                and not (_matches(BABY_FELL_OFF, line) or _matches(BABY_FELL_OVER, line)):
            continue
        if name == "fall_check" and (_matches(FALL_CHECK_OFF, line) or _matches(FALL_RED, line)
                                     or _matches(FALL_PAST, line) or _matches(FALL_FINE, line)
                                     or re.search(r"\b(?:hurt|broke|broken|fractur\w*|hip|head|"
                                                  r"back|neck|blood|bleed\w*|cut|hospital|"
                                                  r"ambulance|get\s+up|weight|dizzy|sick|"
                                                  r"confus\w*|"
                                                  r"making\s+sense|lift|talking\s+(?:rubbish|"
                                                  r"nonsense|gibberish)|not\s+(?:him|her|them)s"
                                                  r"elf|not\s+(?:him|her|them)selves|"
                                                  r"swell\w*|swollen|sore|bruise\w*|stiff|"
                                                  r"sprain\w*|twisted|turned\s+over|"
                                                  r"grazed|scraped|ache\w*|teeth|tooth|dentist)\b",
                                                  line)):
            continue
        if name == "fall_hip" and _matches(OLD_FALL_FINE, line):
            continue
        if name == "fall_hip" and _matches(OLD_FALL_NOT, line):
            continue
        if name == "fall_hip" and re.search(r"\b(?:broke|broken|fractur\w*|snapped)\b", line):
            continue
        if name == "breath_rest" and _matches(BREATH_SPORT, line):
            continue
        if name == "breath_rest" and _matches(NIGHT_BREATH, line) \
                and not _matches(NIGHT_BREATH_RED, line):
            continue
        if name == "shot" and _matches(SHOT_FINE, line):
            continue
        if name == "eye_chem" and _matches(EYE_FINE, line):
            continue
        if name == "bone_out" and _matches(BONE_FINE, line):
            continue
        if name == "headache" and not (_matches(HEADACHE_SUDDEN, line)
                                       or _matches(HEADACHE_WORST_EVER, line)):
            continue
        if name == "headache" and not _matches(HEADACHE_BAD, line):
            continue
        if name == "headache" and _matches(HEADACHE_STORY, line):
            continue
        if name in ("cough_blood", "vomit_blood") and _matches(COUGH_FINE, line):
            continue
        if name in ("cough_blood", "vomit_blood") and _matches(ANIMAL, line) and not _matches(
                HUMAN_TOO, line):
            continue
        if name in ("cough_blood", "vomit_blood"):
            key = name if _person(line) else name + "_self"
            return _fit(pick(REPLIES[key], memory), line, name)
        if name in ("poo_blood", "poo_black") and _matches(POO_FINE, line):
            continue
        if name in ("poo_blood", "poo_black") and _matches(POO_PANTS, line) and not _matches(
                POO_WORD, line):
            continue
        if name in ("poo_blood", "poo_black") and _matches(POO_MEAL, line) and not _matches(
                POO_RED, line):
            continue
        if name in ("poo_blood", "poo_black") and _matches(STOOL_LONG, line) and not _matches(
                POO_RED, line):
            key = name + "_long" if _person(line) else name + "_long_self"
            return _fit(pick(REPLIES[key], memory), line, name)
        if name == "torsion" and _matches(TORSION_FINE, line):
            continue
        if name == "torsion" and _matches(ANIMAL, line) and not _matches(HUMAN_TOO, line):
            continue
        if (name == "torsion" and _matches(TESTIS_LUMP, line)
                and not _matches(TORSION_ONSET, line)
                and not _matches(TORSION_RED, line)):
            key = "torsion_lump" if _person(line) else "torsion_lump_self"
            return _fit(pick(REPLIES[key], memory), line, name)
        if (name == "torsion" and not _matches(TORSION_HARD, line)
                and not _matches(TORSION_ONSET, line)
                and not (_matches(TORSION_SICK, line) and not _matches(TORSION_MILD, line))):
            continue
        if name == "torsion" and _matches(TORSION_LONG, line) and not _matches(TORSION_RED, line):
            key = "torsion_long" if _person(line) else "torsion_long_self"
            return _fit(pick(REPLIES[key], memory), line, name)
        if name in ("poo_blood", "poo_black", "torsion"):
            if name == "torsion" and not _matches(TORSION_ONSET, line):
                key = "torsion_hard" if _person(line) else "torsion_hard_self"
            else:
                key = name if _person(line) else name + "_self"
            return _fit(pick(REPLIES[key], memory), line, name)
        if name == "gas_smell" and _matches(GAS_ON_YOU, line) and not _matches(GAS_IN_ROOM, line):
            continue
        if name == "gas_smell" and _matches(GAS_PAST, line) and not _matches(GAS_NOW, line):
            continue
        if name in ("named_illness", "high_temp", "child_drank", "recent_fit", "grunting_baby",
                    "sleepy_feed", "fever_rash") and _matches(PET_WORDS, line) and not _matches(
                HUMAN_TOO, line):
            continue
        if name == "blackout":
            if _matches(BLACKOUT_A_THING, line):
                continue
            urgent = _matches(BLACKOUT_URGENT, line) or _matches(BLACKOUT_STILL_DOWN, line)
            if _matches(BLACKOUT_OFF, line) and not _matches(BLACKOUT_HEART, line):
                continue
            if _matches(CHILD_ANON, line) and not urgent:
                continue
            if _person(line) or _matches(OTHER_BODY, line):
                if not urgent or _matches(UNCONSCIOUS, line):
                    continue
                key = "blackout_other"
            elif urgent:
                key = "blackout_self"
            elif _matches(BLACKOUT_REPEAT, line):
                key = "blackout_today"
            else:
                continue
            _note(memory, name)
            return _fit(pick(REPLIES[key], memory), line, name)
        if name == "seizure" and _matches(RECENT_FIT, line) and not _matches(RECENT_FIT_FINE, line):
            continue
        if name == "drowning" and _matches(DROWNING_HYPERBOLE, line) \
                and not _matches(WATER_DANGER, line):
            continue
        if name == "seizure" and _matches(SEIZURE_FIGURATIVE, line) and not _matches(ANIMAL, line):
            continue
        if name == "seizure" and not _matches(FIT_STILL_RINGS, line) and (
                _matches(FIT_ROUTINE, line) or _matches(THING_FIT_SUBJECT, line)):
            continue
        if (name == "fall" and _matches(LIMB_AT_AN_ANGLE, line)
                and not _matches(FALL_CORE, line) and _matches(LIMB_IS_A_THING, line)
                and not _matches(OWN_LIMB_AT_AN_ANGLE, _without_object_limbs(line))):
            continue
        if name == "fall" and _matches(FALL_FINE, line) and not _matches(FALL_RED, line):
            continue
        if name == "fall" and _matches(FALL_PAST, line) and not _matches(FALL_NOW, line):
            continue
        if (name == "fall" and _matches(FALL_REPEAT, line)
                and not _fall_with_sign(line)
                and not _matches(FALL_NOW, line) and not _matches(FALL_RED, line)
                and not _matches(FALL_PATTERN_HURT, line)):
            key = "fall_pattern_self" if _matches((r"\bi\b", r"\bwe\b"), line) and not _person(
                line) else "fall_pattern"
            return _fit(pick(REPLIES[key], memory), line, "fall_pattern")
        if name == "fall" and _matches(NEAR_MISS, line) and not _matches(NEAR_MISS_HARM, line):
            continue
        if name == "fall" and _matches(PET_FELL, line) and not _matches(HUMAN_TOO, line):
            continue
        if name == "sepsis_signs" and _matches(CONFUSED_THING, line) and not _matches(
                (r"\bdrows\w*", r"\bfloppy\b", r"\blimp\b", r"\bunrespons\w*",
                 r"\bwon'?t\s+wake\b", r"\bvery\s+sleepy\b"), line):
            continue
        if name == "red_flags":
            flat = _matches(RASH_FLAT, line) or _glass_test_line(line, before)
            company = _matches(RASH_COMPANY, line) or _matches(RASH_COMPANY, before)
            if _matches(RASH_DEFINITION, line):
                continue
            if flat and not company and not _matches(RASH_NAMED, line) \
                    and not _matches(RASH_NAMED, before) \
                    and not _matches(RASH_PRESSED, line):
                continue
        if name == "stiff_neck" and _matches(STIFF_FINE, line) and not _matches(RASH_RED, line):
            continue
        if name in ("sepsis_signs", "newborn_fever", "newborn_fever_next") and not _matches(
                RED_ANCHOR, line):
            continue
        if name == "newborn_fever" and _matches(DEVICE_OLD, line):
            continue
        if name in ("sepsis_signs", "newborn_fever", "newborn_fever_next") and _matches(DEVICE_TEMP, line) and not _matches(
                (r"\bfever\w*", r"\bfeverish\b", r"\bburning\s+up\b", r"\bhot\s+to\s+touch\b",
                 r"\b\d{2}(?:\.\d)?\s*(?:c\b|degrees)"), line):
            continue
        if name == "pale_child" and _matches(PALE_EFFORT_RED, line):
            if _matches(PALE_OTHER_RED, line):
                continue
            _note(memory, "pale_child")
            return _fit(pick(REPLIES["pale_child_now"], memory), line, "pale_child")
        if name == "pale_child" and _matches(PALE_EFFORT, line) and not _matches(
                PALE_EFFORT_RED, line) and (
                _matches(PALE_EFFORT_REAL, line) or not _matches(PALE_EFFORT_NO, line)):
            _note(memory, "pale_child")
            said = "pale_child_heat" if _matches(PALE_HEAT, line) else "pale_child_effort"
            return _fit(pick(REPLIES[said], memory), line, "pale_child")
        if name == "pale_adult" and (
                _matches(CHILD_WORD, line) or _matches(PALE_ADULT_FINE, line)
                or (_matches(PALE_ADULT_ITSELF, line)
                    and not _matches(PALE_ADULT_WHOLE, line))):
            continue
        if name == "pale_adult" and _matches(PALE_EFFORT, line) and not _matches(
                PALE_EFFORT_RED, line):
            _note(memory, "pale_adult")
            return _fit(pick(REPLIES["pale_adult_effort"], memory), line, "pale_adult")
        if name == "pale_adult":
            said = "pale_adult" if _matches(ADULT_PERSON, line) else "pale_adult_self"
            _note(memory, said)
            return _fit(pick(REPLIES[said], memory), line, "pale_adult")
        if name == "newborn_fever" and _matches(NEWBORN_FINE, line) and not _matches(
                SEPSIS_SIGN, line):
            continue
        if name == "child_fever" and _matches(
                (r"\bhad\s+(?:a\s+|an\s+|the\s+)?(?:temperature|temp|fever|high\s+temperature)\b",
                 r"\bwas\s+(?:ill|poorly|unwell|sick)\s+(?:with|from)\s+(?:a\s+)?(?:temperature|"
                 r"temp|fever)\b"), line) and not _matches((r"\bhas\s+had\b", r"\bfor\s+(?:\d+|"
                 r"two|three|four|five|six|seven)\s+days?\b"), line):
            continue
        if (name == "heat" and _matches((CHILD_WORD,), line)
                and _matches((r"\bburning\s+up\b", r"\bfeels?\s+(?:hot|feverish)\b",
                              r"\bboiling\s+hot\b", r"\bhot\s+to\s+(?:the\s+)?touch\b",
                              r"\bhot\s+and\s+(?:shivery|clammy|sweaty|floppy|miserable)\b",
                              r"\b(?:really|very|so)\s+hot\b"), line)
                and (not _matches((r"\bsun\b", r"\bheat\b", r"\bheatwave\b", r"\bcar\b",
                                   r"\bhot\s+(?:car|room|day|weather)\b", r"\boutdoors?\b",
                                   r"\bpark\b", r"\bbeach\b", r"\bafternoon\b", r"\bweather\b",
                                   r"\bafter\s+(?:football|rugby|sport|training|a\s+run|pe)\b"),
                                  line)
                     or _matches((r"\b(?:temperature|temp|fever|feverish)\b",), line))):
            continue
        if name in FEVER_HOME_CARE and _the_only_fever_is_a_disease_name(line) and not _matches(
                SEPSIS_SIGN, line):
            continue
        if name == "child_fever" and _matches(FEVER_ASK, line) and not _matches(
                FEVER_REPORT, line):
            continue
        if name == "child_fever" and _matches(CHILD_GROWN, line) and not _matches(SEPSIS_SIGN, line):
            continue
        if (name == "child_fever" and _matches(CHILD_SCHOOL_AGE, line)
                and not _matches(CHILD_FEVER_RED, line) and not _matches(SEPSIS_SIGN, line)):
            continue
        if name == "child_fever" and _matches(CONFUSED_THING, line):
            continue
        if name == "child_fever" and _matches((RASH,), line) and not _matches(SEPSIS_SIGN, line):
            continue
        if name == "child_fever" and _matches(
                (r"\b(?:eating|drinking|playing|chatty|cheerful|happy|himself|herself|themselves|"
                 r"running\s+about|full\s+of\s+beans|fine|better|improving)\b",
                 r"\bno\s+other\s+symptoms\b"), line) and not _matches(SEPSIS_SIGN, line) \
                and not _matches(CHILD_FEVER_NOT_EATING, line):
            continue
        if name == "newborn_fever" and not _matches(
                RASH_RED + STIFF_NECK + SEPSIS_SIGN + (r"\bblue\b", r"\bbreathing\s+fast\b"), line):
            return _fit(pick(REPLIES["newborn_temp"], memory), line, "newborn_temp")
        if name == "child_fever" and _matches(
                (r"\blast\s+(?:week|month|year|night|time)\b", r"\bweeks?\s+ago\b",
                 r"\b(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten)\s+days?\s+ago\b",
                 r"\bused\s+to\b", r"\bback\s+to\s+(?:normal|"
                 r"himself|herself|school|nursery)\b", r"\bover\s+it\b", r"\bfully\s+better\b"),
                line) and not _matches(FEVER_STILL_NOW, line):
            continue
        if name == "child_fever" and _matches(PET_WORDS, line) and not _matches(HUMAN_TOO, line):
            continue
        if name == "newborn_fever_next" and not _tiny_baby(memory):
            continue
        if name == "newborn_fever_next" and not (
                _matches(BABY_BURNING, line) or _matches(FEVER_SIGN, line)) and not (
                _true_newborn(memory)):
            continue
        if name == "newborn_fever_next" and (_matches(NEWBORN, line) or _matches(
                TINY_AGE_FINE, line)):
            continue
        if name == "newborn_fever_next" and _matches(OLDER_CHILD_NAMED, line):
            continue
        if name == "newborn_fever_next" and _matches(ABOUT_THE_SPEAKER, line) and not _matches(
                PERSON_WORD, line):
            continue
        if name == "newborn_fever_next" and _matches(PERSON_WORD, line) and not _matches(
                TINY_SAID, line):
            continue
        if name == "newborn_fever_next" and _matches(PET_WORDS, line) and not _matches(
                HUMAN_TOO, line):
            continue
        if name == "newborn_fever_next" and _matches(
                (r"\btoddlers?\b", r"\bkids?\b", r"\bchildren\b", r"\bchild\b"), line):
            continue
        if name == "newborn_fever_next" and not _matches(
                RASH_RED + STIFF_NECK + SEPSIS_SIGN + (r"\bblue\b", r"\bbreathing\s+fast\b"), line):
            return _fit(pick(REPLIES["newborn_temp"], memory), line, "newborn_temp")
        if name == "named_illness" and _matches(NAMED_SICK_FINE, line) and not _matches(
                SEPSIS_SIGN + (r"\bfever\w*", r"\brash\w*", r"\bstiff\s+neck\b"), line):
            continue
        if name == "recent_fit" and _matches(RECENT_FIT_FINE, line):
            continue
        if name == "grunting_baby" and _matches(GRUNTING_FINE, line) and not _matches(
                GRUNTING_NOW, line):
            continue
        if name == "fever_rash" and _matches(FEVER_RASH_FINE, line):
            continue
        if name == "rash_headache" and (_matches(FEVER_RASH_FINE, line)
                                        or _matches(RASH_HEADACHE_FINE, line)):
            continue
        if name == "rash_headache" and _matches(PET_WORDS, line) and not _matches(HUMAN_TOO, line):
            continue
        if name == "battery_bulge" and _matches(
                (r"\bsmok", r"\bspark", r"\bflames?\b", r"\bon\s+fire\b", r"\bcaught\s+fire\b",
                 r"\bsmell", r"\bhot\s+to\s+touch\b", r"\bmelt"), line):
            continue
        if name == "electric_burn" and _matches(ELECTRIC_FINE, line) and not _matches(
                (r"\bsmell", r"\bsmoke", r"\bmelt", r"\bspark", r"\bbulging", r"\bflames?\b"), line):
            continue
        if (name == "blue" and _matches(PET_ANY, line) and not _matches(HUMAN_TOO, line)
                and _matches(PET_MOUTH, line)):
            continue
        if (name == "blue" and _matches(PET_ANY, line) and not _matches(HUMAN_TOO, line)
                and (_matches(BLUE_CHANGE + PET_BLUE_WENT, line) or _matches(PET_BLUE_PART, line))):
            return _fit(pick(REPLIES["pet_emergency"], memory), line, "pet_emergency")
        if name == "blue" and not _matches(BLUE_HUMAN, line):
            continue
        if (name == "blue" and not _matches(GREY_ALARM, line)
                and not _matches(BLUE_LIPS_FACE, line)
                and not _matches(BLUE_TINGE, line)
                and (_matches(GREY_HAIR, line)
                     or (_matches(GREY_ARRIVING, line)
                         and not _matches(GREY_BODY, line))
                     or (_matches(GREY_COLOUR, line)
                         and not _matches(GREY_BODY, line)
                         and not _matches(BLUE_HUMAN, line)
                         and not _matches(GREY_SELF, line)))):
            continue
        if (name == "blue" and _matches(BLUE_LIMB, line)
                and not _matches(BLUE_LIPS_FACE, line)
                and not _matches(BLUE_TINGE, line)
                and not _matches(BLUE_CHANGE, line)):
            continue
        if (name == "blue" and _matches(BLUE_LIMB, line) and _matches(BLUE_COLD, line)
                and not _matches(BLUE_LIPS_FACE, line) and not _matches(BLUE_TINGE, line)):
            continue
        if (name == "breathing" and _matches(PET_ANY, line) and not _matches(HUMAN_TOO, line)
                and _matches(BLUE_CHANGE, line) and not _matches(PET_CRISIS, line)):
            continue
        if (name == "blue" and _matches(BLUE_CLOTH, line) and not _matches(BLUE_LIPS_FACE, line)
                and not _matches(A_BODY_PART, line)):
            continue
        if (name == "blue" and _matches(BLUE_FOOD, line)
                and not _matches(BLUE_PERSON_SUBJECT, line)
                and not _matches(BLUE_OTHER_PERSON, line)
                and not _matches(BLUE_LIPS_FACE, line)):
            continue
        if name == "blue" and _matches(WENT_BLUE_IDIOM, line) \
                and not _matches(WENT_BLUE_BREATH_RED, line):
            _note(memory, "general")
            return _fit(pick(REPLIES["blue_idiom"], memory), line, name)

        if name == "blue" and _matches(BLUE_COSMETIC, line) \
                and not _matches(WENT_BLUE_BREATH_RED, line):
            return None
        if name == "blue" and _matches(BLUE_FACE_PART, line) and _matches(BLUE_COLD_CAUSE, line) \
                and not _matches(WENT_BLUE_BREATH_RED, line) \
                and not _matches(COLD_ILLNESS, line) \
                and not _matches(NEWBORN + (r"\b(?:baby|babies|infant)\b",), line):
            mine = not _matches(OTHER_BODY, line)
            _note(memory, "blue")
            return _fit(pick(REPLIES["blue_cold" if mine else "blue_cold_other"], memory),
                        line, "blue")
        if name == "blue" and not _matches(BLUE_FACE_PART, line) and _matches(LIMB_PART, line) \
                and _matches(WENT_BLUE_FINE, line) and not _matches(WENT_BLUE_RED, line):
            continue
        if name == "blue" and _matches((r"\bchok\w*",), line):
            continue
        if (name == "blue" and _matches(BLUE_COLD_SELF, line) and _matches(BLUE_SELF, line)
                and not _matches(BLUE_LIPS_FACE, line) and not _matches(LIPS_RED_FLAG, line)):
            continue
        if (name == "blue" and _matches(BLUE_MARK, line)
                and not _matches(BLUE_LIPS_FACE, line)):
            continue
        if (name == "blue" and _matches(BLUE_LIPS_FACE, line) and _matches(LIPS_COLD, line)
                and not _matches(COLD_ILLNESS, line)
                and not _matches(LIPS_RED_FLAG, line)):
            continue
        if (name == "blue" and _matches(BLUE_FINE, line)
                and not _matches(BLUE_STRONG, line)):
            continue
        if name == "blue":
            key = "blue" if _matches(OTHER_BODY, line) else "blue_self"
            _note(memory, name)
            return _for_the_person(_fit(pick(REPLIES[key], memory), line, name), line, name)
        if name == "floppy_child" and _matches(FLOPPY_THING, line):
            continue

        if (name == "floppy_child" and _matches(FLOPPY_SLEEPY, line)
                and not _matches(FLOPPY_RED_FLAG, line)):
            return _fit(pick(REPLIES["floppy_soft"], memory), line, "floppy_child")

        if name == "fall" and _weight_on_a_joint(line):
            continue
        if name == "fall":
            key = "fall_self" if _matches((r"\bi\b", r"\bmy\b"), line) and not _person(
                line) else "fall"
            return _fit(pick(REPLIES[key], memory), line, "fall")
        if name in ("old_fall", "fall", "fall_check") and _matches(FALL_WORD_IDIOM, line):
            continue
        if name == "old_fall" and _matches(HEAD_BANG, line):
            continue
        if name == "old_fall" and _matches(FALL_STROKE_SIGN, line) \
                and not _matches(SLUR_NOT_A_STROKE_WORDS, line):
            continue
        if name == "old_fall" and _fall_with_sign(line):
            continue
        if name == "old_fall" and (_matches(HEAD_KNOCKOUT, line)
                                   or _out_cold_knockout(line)):
            continue
        if name == "old_fall" and not _matches(OLD_PERSON, line):
            continue
        if name == "old_fall" and _matches(OLD_FALL_FINE, line):
            continue
        if name == "old_fall" and _matches(OLD_FALL_NOT, line):
            continue
        if name == "old_fall" and _matches(FALL_PAST, line) and not _matches(FALL_NOW, line):
            continue
        if name == "old_fall" and _matches(NEAR_MISS, line) and not _matches(NEAR_MISS_HARM, line):
            continue
        if name == "old_fall" and _matches(PET_FELL, line) and not _matches(HUMAN_TOO, line):
            continue
        if name == "old_fall":
            key = "old_fall_self" if _matches(FIRST_PERSON, line) and not _person(
                line) else "old_fall"
            return _fit(pick(REPLIES[key], memory), line, "old_fall")
        if (name == "floppy_child" and _matches(FLOPPY_SLEEPY, line)
                and not _matches(FLOPPY_RED_FLAG, line)):
            return _fit(pick(REPLIES["floppy_soft"], memory), line, "floppy_child")
        if name == "seizure" and _matches((r"\b(?:is|are|keeps?)\s+fitting\b",), line) and (
                not _matches(A_PERSON, line)
                or _matches(FITTING_IN + FITTING_THING, line) or _a_settling_fit(line)):
            continue
        if name == "hypo":
            key = "hypo_self" if _matches((r"\bi\b", r"\bmy\b"), line) and not _person(
                line) else "hypo"
            return _fit(pick(REPLIES[key], memory), line, "hypo")
        if name == "heat":
            key = "heat_self" if _matches((r"\bi\b", r"\bmy\b"), line) and not _person(
                line) else "heat"
            return _fit(pick(REPLIES[key], memory), line, "heat")
        if name in ("red_flags", "stiff_neck", "sepsis_signs", "newborn_fever",
                    "newborn_fever_next"):
            key = "red_flags_self" if _matches(
                (r"\bi\b", r"\bi'm\b", r"\bim\b", r"\bmy\b"), line) and not _matches(
                PERSON_WORD + (r"\b(?:newborn|infant|toddler|little\s+one|baby|babies)\b",),
                line) else "red_flags"
            return _fit(pick(REPLIES[key], memory), line, "red_flags")
        if (name == "chest" and _matches(CHEST_FEELING, line)
                and not _matches(_CHEST_OTHER_RED, line)
                and not _matches(CHEST_FEELING_RED, line)
                and not _matches(AFTER_EXERCISE, line)):
            return _fit(pick(REPLIES["chest_anxiety"], memory), line, "chest")
        if (name == "chest" and _matches(CHEST_ADJ, line)
                and not _matches(CHEST, line)
                and not _matches(AFTER_EXERCISE, line)):
            continue
        if name == "chest" and _matches(AFTER_EXERCISE, line) and (
                not _matches(CHEST_RED_FLAGS, line) or (
                    _matches(EXERTION_CHEST, line)
                    and not _matches(_CHEST_OTHER_RED, line))):
            return _fit(pick(CHEST_EFFORT, memory), line, "chest")
        if (name == "chest" and _matches(CHEST_TRAINING, line)
                and not _matches(CHEST_SPREADING, line)):
            continue
        if thing_collapsed and name in ("unconscious", "medical"):
            continue
        if name == "stuck_machine" and _matches(STUCK_FINE, line) \
                and not _matches(MACHINE, line):
            continue
        if name == "unconscious" and _matches(ROUTINE_WAKE, line) and not _matches(WAKE_RED, line):
            continue
        if name == "unconscious" and _matches(WONT_COME_ROUND, line) \
                and not _matches(UNCONSCIOUS, line) and not _matches(WAKE_UP_SOMEONE, line) \
                and _matches(VISIT_OR_TIME, line) and not _matches(COLLAPSE_HINT, line):
            continue
        if name == "unconscious" and _matches(HARD_TO_WAKE, line) \
                and not _matches(UNCONSCIOUS, line) and not _matches(WAKE_UP_SOMEONE, line) \
                and _matches(MORNING_ROUTINE, line) and not _matches(COLLAPSE_HINT, line):
            continue
        if name == "unconscious" and _matches(ROUTINE_REASON, line) \
                and not _matches(WAKE_RED + COLLAPSE_HINT + SPELL_RED, line):
            continue
        if name in ("chest",) and _asking_about_the_world(line) and not _matches(
                (r"\bright\s+now\b", r"\bnow\b", r"\bsudden(?:ly)?\b"), line):
            if _matches(CHEST_ASKED_OWN, line) and not _matches(
                    CHEST_KEPT_BY_ANOTHER_CARD, line):
                return _fit(pick(CHEST_ASKED, memory), line, "chest")
            continue
        if name == "stuck_machine":
            mine = not _matches(OTHER_BODY, line)
            key = name + "_self" if mine else name
            return _fit(pick(REPLIES[key], memory), line, name)
        if name in ("headache", "shot"):
            if name == "shot":
                mine = _matches(SHOT_SELF, line) and not _person(line)
            else:
                mine = _person(line) is None and _matches((r"\bi\b", r"\bmy\b"), line)
            key = name + "_self" if mine else name
            return _fit(pick(REPLIES[key], memory), line, name)
        if name == "socket_thing" and _matches(SOCKET_THING_FINE, line):
            continue
        if name == "electric_shock_floor":
            if (_matches(ELECTRIC_SHOCK_NEARLY, line) or _matches(ELECTRIC_SHOCK_DEATH, line)
                    or (_matches(ELECTRIC_SHOCK_NOT_ELECTRIC, line)
                        and not _matches(ELECTRIC_SHOCK_SUPPLY, line))
                    or _matches(ELECTRIC_SHOCK_CPR, line) or _matches(ELECTRIC_SHOCK_STORY, line)
                    or _matches(ELECTRIC_SHOCK_DEFINITION, line)
                    or (_matches(ELECTRIC_SHOCK_STATIC, line)
                        and not _matches(ELECTRIC_SHOCK_WIRED, line))):
                continue
            key = "electric_shock_floor" if (_person(line) or _matches(OTHER_BODY, line)) else (
                "electric_shock_floor_self")
            _note(memory, name)
            return _fit(pick(REPLIES[key], memory), line, name)
        if name == "electric_shock" and _matches(ELECTRIC_SHOCK_DOWN, line):
            continue
        if name == "electric_shock" and _matches(ELECTRIC_SHOCK_DEFINITION, line):
            continue
        if name == "electric_shock" and _matches(ELECTRIC_SHOCK_DEATH, line):
            continue
        if name == "electric_shock" and _matches(ELECTRIC_SHOCK_STORY, line):
            continue
        if name == "electric_shock" and _matches(ELECTRIC_SHOCK_STATIC, line) \
                and not _matches(ELECTRIC_SHOCK_WIRED, line):
            continue
        if name == "night_breath" and _matches(NIGHT_BREATH_RED, line):
            continue
        if name == "night_breath" and _matches(BREATH_CAUSE, line) and not _matches(
                NIGHT_BREATH_RED, line):
            continue
        if name == "night_breath" and _matches(NIGHT_BREATH_DREAM, line):
            continue
        if name == "night_breath" and _matches(NIGHT_BREATH_CHILD, line) \
                and not _matches(NIGHT_BREATH_RED, line):
            _note(memory, name)
            return _fit(pick(REPLIES["night_breath_child"], memory), line, name)
        if name == "night_breath" and _matches(ANIMAL, line) and not _matches(
                HUMAN_TOO, line):
            continue
        if hypothetical:
            general = GENERAL.get(name)
            if general:
                _note(memory, name)
                return _for_the_person(general, line, name)
            continue
        if name == "stroke" and _matches(STROKE_FAST, line) and not _matches(STROKE, line):
            if not _matches(_FACE_WORD, line) and (
                    _matches(STROKE_FAST_JAB, line) or _matches(STROKE_FAST_LIFT_CEILING, line)):
                continue
            if _matches(STROKE_FAST_OFF, line) or _matches(STROKE_FAST_SHOULDER, line) or (
                    _matches(STROKE_FAST_PATTERN, line)
                    and not _matches(STROKE_PAIR_BOTH, line)
                    and not _matches(STROKE_FAST_WEAK, line)) or (
                    not _matches(STROKE_FAST_HARD, line)
                    and not (_matches(STROKE_FAST_JAB, line)
                             and _matches(_FACE_GOING_ODD, line))
                    and (_matches(STROKE_FAST_CAUSE, line)
                         or _matches(STROKE_FAST_SENSORY, line))):
                continue
        if name == "arm_numb" and _matches(CHEST_MENTIONED, line):
            continue
        if name == "chest" and _matches(CHEST_WORK, line) and not _matches(CHEST_URGENT, line):
            _note(memory, "chest_slow")
            return _fit(pick(REPLIES["chest_work"], memory), line, name)
        if name == "chest" and _matches(CHEST_SLOW, line) and not _matches(CHEST_URGENT, line):
            _note(memory, "chest_slow")
            return _fit(pick(REPLIES["chest_slow"], memory), line, name)
        if (name == "chest" and _matches(CHEST_SORE_MOVE, line)
                and not _matches(CHEST_URGENT, line)
                and not _matches(CHEST_RED_FLAGS, line)
                and not _matches(CHEST_SPREAD, line)
                and not _matches(CHEST_STRAIN_STOP, line)
                and not _matches((r"\bblood\b", r"\bbleed\w*", r"\bright\s+now\b"), line)):
            if _matches((r"\bcough\w*",), line):
                return _fit(pick(CHEST_COUGH_STRAIN_REPLY, memory), line)
            return _fit(pick(CHEST_STRAIN_REPLY, memory), line)
        if (name == "chest" and _matches(CHEST_STRAIN_MOVE, line)
                and not _matches(CHEST_URGENT, line)
                and not _matches(CHEST_RED_FLAGS, line)
                and not _matches(CHEST_SPREAD, line)
                and not _matches(CHEST_STRAIN_STOP, line)
                and not _matches((r"\bblood\b", r"\bbleed\w*", r"\bright\s+now\b"), line)):
            return _fit(pick(CHEST_STRAIN_REPLY, memory), line)
        if (name == "chest" and _matches(CHEST_STRAIN, line)
                and not _matches(CHEST_URGENT, line)
                and not _matches(CHEST_RED_FLAGS, line)
                and not _matches(CHEST_SPREAD, line)
                and not _matches(CHEST_STRAIN_STOP, line)
                and not _matches((r"\bblood\b", r"\bbleed\w*", r"\bright\s+now\b"), line)):
            return _fit(pick(CHEST_COUGH_STRAIN_REPLY, memory), line)
        if name == "chest" and not _matches(CHEST_MENTIONED, line):
            _note(memory, "chest")
            return _for_the_person(_fit(pick(REPLIES["chest_limb"], memory), line, "chest"),
                                   line, "chest")
        if name == "object_in_head" and _matches(OBJECT_IN_HEAD_BLOW, line) \
                and not _matches(OBJECT_IN_HEAD_BATTERY, line):
            continue
        if name == "object_in_head" and _matches(OBJECT_IN_HEAD_BATTERY, line):
            _note(memory, "object_in_head_battery")
            return _fit(pick(REPLIES["object_in_head_battery"], memory), line, name)
        if name == "poison" and _matches(DOSE_COURSE, line) and not _matches(
                DOSE_COURSE_KEEP, line):
            continue
        if name == "poison" and _matches(DOSE_ASKED, line) and not _matches(
                DOSE_ALREADY_GIVEN, line):
            continue
        if name == "dose_stated":
            counted = _stated_dose(line)
            if counted is None:
                continue
            _note(memory, "dose_stated")
            return counted
        if name == "swallowed_thing" and _matches(SWALLOWED_BAD, line):
            _note(memory, name)
            if _matches(SPEAKER_IS_PATIENT, line) and not _matches(SWALLOWED_CHILD, line):
                return pick(SWALLOWED_BAD_SELF, memory)
            return pick(SWALLOWED_BAD_REPLY, memory)
        if name == "swallowed_thing" and _matches(SPEAKER_IS_PATIENT, line) and not _matches(
                (r"\bmy\s+(?:child|son|daughter|baby|toddler|kid|boy|girl)\b",), line):
            _note(memory, name)
            return pick(SWALLOWED_SELF, memory)
        if name == "self_harm" and not _a_wish_for_their_own_body(line) \
                and _matches(SELF_CUT, line) and (
                _matches(BLEEDING, line) or _matches(CUT_NOT_STOPPING, line)):
            _note(memory, "bleeding")
            return _fit(pick(REPLIES["self_cut_bleeding"], memory), line, "self_cut_bleeding")
        if name == "recent_fit" and not (_person(line) or _matches(OTHER_BODY, line)):
            _note(memory, "recent_fit_self")
            return _fit(pick(REPLIES["recent_fit_self"], memory), line, "recent_fit_self")
        _note(memory, name)
        return _for_the_person(_fit(pick(REPLIES[name], memory), line, name), line, name)
    if (not hypothetical and _matches(RAYNAUD, line)
            and _matches((r"\bcold\b", r"\bwinter\b", r"\braynaud\w*\b", r"\bswim\w*",
                          r"\bsea\b", r"\bsnow\b", r"\bfreez\w*", r"\bice\b",
                          r"\bshower\b", r"\bwater\b", r"\bwashing\s+up\b"), line)
            and not _matches((r"\b(?:blue|white|purple|grey|gray)\s+(?:in|with|from|out\s+in|and)\s+"
                              r"(?:the\s+|a\s+)?(?:cold|freezing)",), line)
            and not _matches((r"\b(?:swim\w*|swam|the\s+sea|sea\s+water|pool|lido|"
                              r"cold\s+water)\b",), line)
            and not _matches((r"\b(?:can'?t|cannot|struggling\s+to|stopped)\s+breath\w*",
                              r"\bgasping\b", r"\bchest\b", r"\bunconscious\b",
                              r"\bchoking\b"), line)):
        return _fit(pick(REPLIES["raynaud"], memory), line, "minor")
    soft_bleed = (_matches(SOFT_BLEED, line) and _matches(SOFT_BLEED_ANCHOR, line)
                  and not _matches(SOFT_BLEED_OFF, line))
    if (soft_bleed or _matches(NOT_STOPPING, line)) and not _matches(NOT_STOPPING_OFF, line):
        return _fit(pick(REPLIES["bleeding_wont_stop"], memory), line, "minor")
    head = None if hypothetical else _head_bang(line)
    if head and _matches(PET_WORDS, line) and not _matches(HUMAN_ANCHOR, line):
        head = None
    if head:
        who = _head_person(line)
        keys = {"watch": ("head_bang", "head_bang_other"),
                "red": ("head_bang_red", "head_bang_red_other")}[head]
        text = pick(HEAD_REPLIES[keys[1] if who else keys[0]], memory)
        if who:
            subj, obj = ("she", "her") if who == "she" else ("he", "him")
            text = text.format(s=subj, o=obj)
        return text
    care = _matches(OWN_INJURY_IN_MY_CARE, line)
    own_question = (hypothetical and _matches(OWN_INJURY_QUESTION, line)
                    and _matches((r"\bi\b", r"\bmy\b", r"\byour\b"), line)
                    and not _matches(OWN_INJURY_SOMEONE_OR_A_STORY, line)
                    and (care or not _matches(OWN_INJURY_YOU + OWN_INJURY_OTHER_PERSON, line)))
    if not own_question and hypothetical and _the_injury_the_chat_is_on(line, memory):
        own_question = True
    minor = _minor(line, memory)
    if minor and (not hypothetical or own_question):
        if care and isinstance(minor, tuple) and len(minor) > 1:
            spoken = tuple(one for one in minor if not re.search(r"\byou\b|\byour\b", one, re.I))
            minor = spoken or minor
        return _fit(pick(minor, memory), line, "minor")
    if _matches(HAIR_SCORCH, line):
        if _matches(HAIR_SCORCH_SKIN, line) or _matches(MILD_BODY_SIGN, line):
            burn_card = _minor_replies("burn")
            if burn_card:
                return _fit(pick(burn_card, memory), line, "minor")
        return pick(HAIR_SCORCH_ANSWER, memory)
    if _matches(ASKS_IF_CALL, line) and not _matches(CALL_HAS_A_SIGN, line):
        _note(memory, "general")
        return pick(ASK_CALL_REPLIES, memory)
    if not _matches(CALL_HAS_A_SIGN, line) and (
            _matches(ASKS_IF_GOING, line) or _matches(ASKS_GO_BARE, line)):
        was_case = _last_case(memory)
        live = not (isinstance(memory, dict) and memory.get("safety_safe"))
        if was_case in AMBULANCE_CASES and live and not _matches(GO_IN_NOT_ABOUT_IT, line):
            _note(memory, was_case)
            wait = WAITING.get(was_case) or WAITING["general"]
            return _fit(pick(GO_IS_A_CALL, memory)
                        + pick(wait if isinstance(wait, tuple) else (wait,), memory), line, was_case)
    if _matches(ASKS_IF_GOING, line) and not _matches(CALL_HAS_A_SIGN, line):
        _note(memory, "general")
        return pick(ASK_GO_REPLIES, memory)
    if _matches(NEAR_FIRE, line) and not _matches(FIRE_DRILL, line) \
            and not _minor(line, memory):
        if _a_fire_that_did_not_happen(line):
            _note(memory, "near_fire")
            return _fit(pick(REPLIES["near_fire"], memory), line, "near_fire")
        if _fire_words_in(line):
            _note(memory, "fire")
            return _fit(pick(REPLIES["fire"], memory), line, "fire")
    return _follow_up(line, memory)

from ..memory import again as _never_twice

respond = _never_twice.replied(respond)
