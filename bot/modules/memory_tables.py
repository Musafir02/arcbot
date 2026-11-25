
import re
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

MISSED_CATCH_UP = re.compile(
    r"\bwhat (?:have|had|did) i miss(?:ed)?\b"
    r"(?=\s*(?:so far|then|here|yet|today|again)?\s*[?.,!]*$)|"
    r"\b(?:have|did) i miss(?:ed)? anything\b(?=\s*[?.,!]*$)", re.I)
TOPIC_ASK = re.compile(
    r"\bwhat (?:were|are|was|did|do|have|had) we\s+"
    r"(?:talk|chat|discuss|mention|speak|spoke|say|said|cover)\w*\s*(?:about|of|on)\b|"
    r"\bwhat (?:were|was|did|have|had) we\s+"
    r"(?:talk|chat|discuss|mention|speak|spoke|say|said|cover|do|done)\w*"
    r"(?=\s*[?.!,]|\s*$)|"
    r"\bwhat we\s+(?:talk|chat|discuss|mention)\w*\s*(?:about|of|on)\b|"
    r"\bwhat (?:were|are|was) (?:we|i|you) (?:talking|chatting|saying|on) about\b|"
    r"\bwhat (?:were|are|was) (?:we|i|you) saying\b|"
    r"\bwhere (?:were we|are we)(?=\s*[?.!,]|\s*$)|\bwhere did we (?:leave|get to|stop)\b|"
    r"\bwhat was i (?:saying|on about|asking|learning|studying|reading|researching|working on|"
    r"up to)\b|"
    r"\bwhat (?:was|is) (?:my|the|that) question\b\s*(?:again)?\s*[?.!,]*$|"
    r"\bwhat question (?:did i (?:just )?ask|(?:was|is) (?:it|that))\b|"
    r"\bwhat (?:was|were) (?:i|we|you) up to\b|"
    r"\bwhat (?:am|was) i (?:learning|studying|reading|researching)\b|"
    r"\bcatch me up\b|\brecap\b|" + MISSED_CATCH_UP.pattern + r"|"
    r"\bremind me (?:what|where|how)\b|\bsum (?:up )?what we\b|"
    r"\bwhat (?:did|have) we (?:talk|chat|say) about\b|"
    r"\bwhat we (?:have|had) (?:covered|talked|discussed|done|said|been on)\b|"
    r"\bwhat we were (?:on|up to)\b|"
    r"\bwhat did i (?:just )?(?:ask|want to know)\b"
    r"(?![^.?!]*\babout\b(?!\s+(?:me|it|that|this|them|us)\b))|"
    r"\bwhat did i (?:just )?say\b"
    r"(?!\s+(?:about|to|when|in|on|at|for|during|before|after|since|wrong)\b)")
ASK_WITHOUT_MY = re.compile(
    r"\b(?:what|which) (?:pets?|dogs?|cats?|animals?) (?:do|did|have) i\b|"
    r"\b(?:do|have|did) i (?:have|got) (?:any )?(?:pets?|dogs?|cats?|animals?|allergies|"
    r"a budget)\b|"
    r"\bam i allergic to\b|\b(?:anything|something) i(?:'m| am) allergic to\b")
HOW_MANY_OF_MINE = re.compile(
    r"\bhow many (?:pets?|dogs?|pupp(?:y|ies)|cats?|kittens?|animals?|rabbits?|hamsters?|"
    r"parrots?|fish|horses?|pon(?:y|ies)) (?:do|did) (?:i|we) (?:have|got|own)\b|"
    r"\bhow many (?:pets?|dogs?|pupp(?:y|ies)|cats?|kittens?|animals?|rabbits?|hamsters?|"
    r"parrots?|fish|horses?|pon(?:y|ies)) (?:have|had) (?:i|we) got\b", re.I)
MEMORY_POINTER = re.compile(r"\b(?:again|remind me|did i (?:say|tell)|for a living|for work)\b")
PLAN_ASKS = re.compile(
    r"\bwhat (?:am i|are we) (?:planning|up to)\b|\bwhat (?:am i|are we) doing\b(?!\s+wrong)\b|"
    r"\bwhat(?:'s| is|s)?\s+(?:coming up|on for (?:me|us))\b|"
    r"\bwhat (?:have|has) (?:i|we) got (?:coming up|on|planned|left)\b|"
    r"\bwhat (?:have|has) (?:i|we) got to (?:do|sort|get|finish|arrange)\b|"
    r"\bwhat (?:have|has) (?:i|we) got (?:in|on) (?:the|my|our) (?:diary|calendar)\b|"
    r"\bwhat (?:have|has) (?:i|we) got\s*[?.!,]*\s*$|"
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
    r"\bremind me where\b")
PLAN_MINE = re.compile(
    r"\bwhat (?:was|is) my plan\b|\bwhat my plan (?:was|is)\b|"
    r"\bwhat (?:did|do) i say (?:my plan|i was planning)\b|"
    r"\bwhat (?:are|were) (?:my|our) plans?\b" + NOT_THE_PLAN + r"|"
    r"\bwhat plans (?:do|did) (?:i|we) have\b" + NOT_THE_PLAN + r"|"
    r"\b(?:do|did) (?:i|we) have (?:any |some )?plans?\b|"
    r"\b(?:do|did) (?:i|we) have anything (?:planned|coming up|on)\b|"
    r"\bhave (?:i|we) got (?:any |some )?(?:plans?|anything (?:planned|coming up|on))\b|"
    r"\b(?:is|are) there anything (?:planned|coming up|on) for (?:me|us)\b")
WHEN_ASKS = re.compile(r"\bwhen (?:do|does|will|am|are) (?:i|we)\s+(?:going to\s+)?([a-z]+)")
DAY_ASKS = re.compile(r"\b(?:what|which) (?:day|date) (?:do|does|will|am|are) (?:i|we)\s+"
                      r"(?:going to\s+)?([a-z]+)")
WHERE_PLAN = re.compile(
    r"\bwhere (?:are|were|was|am) (?:we|i) (?:going|off|headed|heading|away|moving|flying|"
    r"travelling|traveling|driving)\b|"
    r"\bwhere (?:we|i) (?:are|were|am|was) (?:going|off|away|moving|flying|travelling|traveling|"
    r"driving)\b|"
    r"\bwhere to again\b|\bwhere (?:are|were) we off to\b|\bremind me where\b")
SAID_AS_A_SENTENCE = re.compile(r"^(?:we|i|we'?ve|i'?ve|we'?re|i'?m|we'?ll|i'?ll|we'?d|i'?d|"
                                r"we are|i am|we were|i was|my|our)\b", re.I)

WHEN_PLAN = re.compile(
    r"\bwhen (?:are|were|was|am) (?:we|i) (?:off|going|away|moving|flying|travelling|traveling)\b|"
    r"\b(?:which|what) (?:month|day|week|date|time of year) (?:are|am|is) (?:we|i)\b|"
    r"\b(?:which|what) (?:month|day|week|date|time of year) (?:is|was) that\b|"
    r"\bwhat date (?:are|am) (?:we|i)\b")
THAT_DATE = re.compile(r"\b(?:which|what) (?:date|day) (?:is|was) that\b")
CALENDAR_SAID = re.compile(
    r"\b\d{1,2} (?:january|february|march|april|may|june|july|august|september|october|"
    r"november|december)\b", re.IGNORECASE)
WEEKDAY_WORD = re.compile(r"\b(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b")
DAY_OF_MONTH = re.compile(r"\b(?:on the |the )?(\d{1,2}(?:st|nd|rd|th))\b")
WHEN_THING = re.compile(
    r"\bwhen(?:'s| is| are| was| were)\s+(?:the|my|our|his|her|their|your|a|an)\s+([a-z][a-z'-]*)")
WHEN_INVERTED = re.compile(
    r"^(?:when|when's)\s+(the|my|our|his|her|their|your|a|an)\s+([a-z][a-z'-]*)\s+"
    r"(is|are|was|were)\b(?:[\s,]*(?:again|please|then))?$")
WHEN_INVERTED_SUBJECT = re.compile(
    r"^when\s+(i|we)\s+((?:am|are|was|were|do|does|did|will|have|has)\b.*)$")
WHEN_THING_VERB = re.compile(
    r"\bwhen (?:does|do|did|will|would|can|could)\s+(?:the|my|our|his|her|their|your)\s+"
    r"([a-z][a-z'-]*)\s+([a-z][a-z'-]*)")
WHEN_END_ASK = frozenset("""end ends finish finishes last lasts leave leaves return returns come
arrive arrives land lands close closes stop stops expire expires wrap""".split())
WHEN_START_ASK = frozenset("start starts begin begins open opens kick".split())
WHEN_END_WORD = frozenset("end ends finish finishes last lasts over expire expires close closes "
                          "wrap wrapped""".split())
TIME_ASKS = re.compile(r"\bwhat time (?:do|does|will|am|are) (?:i|we)\s+(?:going to\s+)?([a-z]+)")
TIME_THING = re.compile(
    r"\bwhat time(?:'s| is| are| was| were)\s+(?:the|my|our|his|her|their|your|a|an)\s+"
    r"([a-z][a-z'-]*)")
DAY_THING = re.compile(
    r"\b(?:what|which) (?:day|date) (?:is|was|are|were)\s+(?:the|my|our|his|her|their|your|a|an)\s+"
    r"([a-z][a-z'-]*)")
DAY_IT = re.compile(
    r"\b(?:what|which) (?:day|date) (?:is|was) (?:that|this)\b|"
    r"\b(?:what|which) (?:day|date) (?:is|was) (?:it|that)\s+(?:on|at|for|again)\b")
TIME_IT = re.compile(
    r"\bwhat time (?:is|was|will be) (?:that|this)\b|"
    r"\bwhat time (?:is|was) (?:it|that)\s+(?:on|at|for|again)\b")
WHEN_VAGUE = frozenset("next last best first good right usual actual whole thing stuff one time"
                       .split())
WHEN_QUALITY = frozenset("best good right usual actual".split())
WHEN_VERB = frozenset("""prep prepare get go leave book buy tell say send start take plant apply ask
call visit fly travel do make set put order renew sort pack move pay file check wrap post""".split())
POINTS_BACK = frozenset("it its them there that this these those one ones back again""".split())

ELIDED_ASK = re.compile(
    r"\bwhat (?:did|do) i (?:say|call|name) (?:it|him|her|them|they|he|she)"
    r"(?: (?:was|were|is|are))?(?: (?:called|named))?\b"
    r"|\b(?:and )?what (?:was|is) (?:it|that) again\b"
    r"|\b(?:and )?(?:what|which) (?:was|is) (?:its |his |her |their |the )?name(?: again)?\b"
    r"|\b(?:and )?what did i (?:call|name) (?:him|her|them)\b"
    r"|\bwhat (?:was|is) that called again\b")
ELIDED_AGAIN = re.compile(r"\b(?:where|when) (?:was|is) (?:it|that|that one)\b")
ELIDED_WORDS = frozenset("""
and so but ok okay oh then well right what which where when was is did do i call called name
said say it that this him her them they he she his hers its their the again to me you my of
were was that one
""".split())
ELIDED_NOT_SURE = re.compile(r"\bhaven't (?:told|mentioned)\b|\bdon't know (?:it|your)\b")
ELIDED_NAMES = (
    ("name", re.compile(r"\b(?:call|called|name|named)\b")),
    ("city", re.compile(r"\b(?:live|living|from|town|city|moved)\b")),
    ("job", re.compile(r"\b(?:work|working|job)\b")),
    ("age", re.compile(r"\b(?:old|age)\b")),
    ("budget", re.compile(r"\b(?:budget|spend|money|cost)\b")),
    ("allergy", re.compile(r"\ballerg\w*\b")),
    ("pets", re.compile(r"\b(?:pet|pets|dog|cat|animal)\b")),
)

COUNT_ANIMAL = re.compile(
    r"^\s*(?:ok |okay |so |and |but |well |oh |quick |just )*how many\s+"
    r"(dogs?|cats?|puppies|puppy|kittens?|kitten|rabbits?|bunnies|bunny|hamsters?|fish|horses?|"
    r"ponies|parrots?|pets?)\b\s*"
    r"(?:do (?:i|we) have|have (?:i|we) got|did (?:i|we) say|do (?:i|we) own|have we|"
    r"are there|(?:is|was|are|were) (?:that|it|this)(?: again| now)?|again|then|now)?"
    r"\s*[?.!]*\s*$", re.I)
COUNT_BARE = re.compile(
    r"^\s*(?:ok |okay |so |and |but |well |oh |quick |just )*how many\s+"
    r"(?:do (?:i|we) have|have (?:i|we) got|do (?:i|we) own|are there|did (?:i|we) say|"
    r"in total|altogether)?\s*[?.!]*\s*$", re.I)

WHAT_I_SAID = re.compile(
    r"\bwhat did i (?:just )?(?:say|tell you|mention)\b|\bwhat have i (?:said|mentioned)\b")

SAID_ASK = re.compile(
    r"\bwhat did i (?:just )?(?:say|tell you)(?: just)?(?: then| last| before| earlier| again)?"
    r"\s*\??$"
    r"|\bwhat (?:was|is|were) (?:the |my )?(?:last|previous|most recent) "
    r"(?:thing|bit|line|message|one) (?:that )?i (?:said|told you|mentioned)\s*\??$")
