
import re
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
)
from .safety_cards import (BITE_DONE, PERSON_HANGING, HEAD_OUT_COLD, STRUCK_NOT_NOW, SELF_HARM_HABIT, HEAL_TIME, HEAD_REPLIES, HUMAN_BITTEN, HIT_IN_FUN_HARD, WATER_DANGER, MILD, SCALD, HYPERBOLE_WISH, PURSUIT_PLACE_HOME, INJURY_HOW, LIPS_SWELL_BARE, DOG_ATTACK, HYPO_SIGN, SUGAR_READING_LOW, SELF_HARM_REPEAT_CAUSE, FOLLOW_UP, LIMP_ONGOING, SHOULD_I_CALL, NOT_JUST_A_NEAR_THING, LIMP_PERSON, PURSUIT_FINE, LIMB_IS_A_THING, COUNTERFACTUAL_WISH)
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
    GAME_NOT_A_BLOW, GRIP_GAME, GRIP_GAME_FENCE, GRIP_NOT_AN_ASSAULT,
    GRIP_NOT_AN_ASSAULT_STR, HAS_ME_SUBJECT, HIT_AS_A_CHILD,
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

FEMALE_WORDS = (r"\bm(?:u|o)m\b", r"\bmother\b", r"\bwife\b", r"\bgirlfriend\b", r"\bsister\b",
                r"\bdaughter\b", r"\blittle\s+girl\b", r"\bgirl\b", r"\baunt\b", r"\bnan\b",
                r"\bgran\b", r"\bgranny\b", r"\bgrandma\b", r"\bgrandmother\b", r"\bniece\b",
                r"\bshe\b", r"\bher\b")

_AGREEMENT = (
    (r"\bthey\s+stop\b", "stop"), (r"\bthey\s+need\b", "need"), (r"\bthey\s+feel\b", "feel"),
    (r"\bthey\s+seem\b", "seem"), (r"\bthey\s+come\b", "come"), (r"\bthey\s+look\b", "look"),
    (r"\bthey\s+get\b", "get"), (r"\bthey\s+go\b", "go"), (r"\bthey\s+start\b", "start"),
    (r"\bthey\s+keep\b", "keep"), (r"\bthey\s+have\b", "have"), (r"\bthey\s+were\b", "were"),
    (r"\bthey\s+are\b", "are"), (r"\bthey\s+do\b", "do"),
)

FIT_CASES = ("medical", "chest", "breathing", "breath_past", "unconscious", "seizure", "stroke", "bleeding",
             "drowning", "fire", "poison", "minor", "heat", "fall", "scald", "red_flags",
             "stiff_neck", "sepsis_signs", "newborn_fever", "hypo", "old_fall", "shot",
             "eye_chem", "bone_out", "headache", "cough_blood", "fall_hip", "lips_swell",
             "breath_rest", "pregnancy_bp", "pet_loss", "baby_fell", "baby_fell_red",
             "puncture", "appendix", "stuck_machine", "poo_blood", "torsion", "safety",
             "swallow_gone")

SWALLOWED_SELF = (
    "Ring 111 (or your local urgent line) today rather than waiting, and keep a spare of whatever it "
    "was to show them; don't make yourself sick. If you start coughing, drooling, or finding it hard "
    "to swallow or breathe, that is 999 or 911 straight away.",
    "Ring 111 (or your local urgent line) today with the packet or a spare in your hand, and don't "
    "make yourself sick or eat and drink for now. Coughing, drooling or trouble swallowing or "
    "breathing means 999 or 911 instead.",
)

DOSE_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
              "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
              "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
              "nineteen": 19, "twenty": 20, r"a\s+couple": 2, r"half\s+a\s+dozen": 6,
              r"a\s+dozen": 12}

ASKS_IF_CALL = (
    r"\b(?:should|shall|do|does|would|must|need|is\s+it\s+worth)\s+(?:i|we|you|he|she|they)\b"
    r"[^.?!]{0,24}\b(?:call|ring|phone|dial|get)\s+(?:an?\s+|the\s+)?"
    r"(?:ambulance|999|911|112|a\s*&?\s*e|a\s*and\s*e|emergency\s+services|paramedics|"
    r"out\s+of\s+hours)\b",
    r"\b(?:do|does)\s+(?:i|we|he|she|they)\s+need\s+(?:an?\s+)?(?:ambulance|999|911|"
    r"a\s*&?\s*e|a\s+and\s+e|the\s+er|paramedics)\b",
    r"\bis\s+(?:this|that|it)\s+(?:an?\s+)?(?:emergency|999\s+call|ambulance\s+job)\b",
    r"\b(?:am|are|is)\s+(?:i|we|he|she|they)\s+(?:meant\s+to|supposed\s+to)\s+(?:call|ring)\b"
    r"[^.?!]{0,20}\b(?:999|911|ambulance)\b",
)

CALL_HAS_A_SIGN = (
    r"\bchest\b", r"\bbreath\w*", r"\bbleed\w*", r"\bunconscious\b", r"\bunresponsive\b",
    r"\b(?:fit|seizure|seized|fitting)\b", r"\bstroke\b", r"\bblue\b", r"\bswallow\w*",
    r"\boverdos\w*", r"\bpoison\w*", r"\bburn\w*", r"\bchoking\b", r"\bcollapsed\b",
    r"\bnot\s+waking\b", r"\b(?:pain|hurts?|hurting|ache\w*)\b", r"\bfever\b",
    r"\brash\b", r"\bvomit\w*", r"\bblood\b", r"\bfell\b", r"\bcut\b",
)

ASKS_IF_GOING = (
    r"\b(?:should|shall|do|does|would|must|need|is\s+it\s+worth)\s+(?:i|we|you|he|she|they)\b"
    r"[^.?!]{0,24}\b(?:take|bring|get|drive|walk)\s+(?:\w+\s+){0,2}?(?:to|into)\s+"
    r"(?:a\s*&?\s*e|a\s*and\s*e|the\s+er|er|casualty|the\s+hospital|hospital|"
    r"the\s+emergency\s+room|out\s+of\s+hours)\b",
    r"\b(?:should|shall|do|does|would|must|need)\s+(?:i|we|you|he|she|they)\s+go\s+"
    r"(?:in|to|into)\s+(?:a\s*&?\s*e|a\s*and\s*e|the\s+hospital|hospital|the\s+er|er|"
    r"casualty|the\s+emergency\s+room|out\s+of\s+hours)\b",
)

ASK_GO_REPLIES = (
    "If it can't wait until the morning, take them in — A&E is for tonight's problems, and you "
    "don't need an ambulance to go. If you're not sure, ring 111 first and describe it.",
    "Go in if it can't wait for a GP appointment, and ring 111 if you're unsure which door to use. "
    "Take the medicine box with you and say what happened at the start of the story.",
)

AMBULANCE_CASES = frozenset((
    "chest", "chest_slow", "stroke", "breathing", "not_breathing", "unconscious", "bleeding",
    "choking", "seizure", "overdose", "poison", "drowning", "hanging", "heat", "head_injury",
))

ASKS_GO_BARE = (
    r"\bgo\s+in\b",
    r"\bgo\s+to\s+(?:a\s*&?\s*e|a\s*and\s*e|the\s+hospital|hospital|casualty|the\s+er|"
    r"the\s+emergency\s+room)\b",
)

GO_IN_NOT_ABOUT_IT = (
    r"\b(?:work|office|job|shift|school|college|uni(?:versity)?|nursery|childminder)\b",
)

GO_IS_A_CALL = (
    "Going is the call, not a drive: ring 999 or 911 and say what is happening, and let them "
    "bring you in. ",
)

ASK_CALL_REPLIES = (
    "If you're asking, that usually means ring: 999 or 911 now if someone can't breathe, won't "
    "wake up, has chest pain or is bleeding heavily, and 111 or your GP today for anything less "
    "than that. Nobody minds you ringing and being wrong.",
    "When in doubt, ring them and say what you can see — 999 or 911 if it's someone's breathing or "
    "waking, 111 or your surgery for the rest. They would far rather take the call than miss one.",
    "Ring 999 or 911 if someone can't breathe, won't wake, has chest pain or is losing blood fast; "
    "111 or your GP today otherwise. Say what you're seeing out loud and let them sort the rest.",
)

SWALLOWED_BAD_REPLY = (
    "Ring 999 or 911 now: a battery, a magnet or anything sharp or long can burn or block within "
    "hours, however well you feel. Don't make them sick, don't give them food or drink, and have an "
    "identical one ready to name on the call.",
    "That is a 999 or 911 call now, not a wait-and-see: a battery burns, and a magnet or anything "
    "sharp or long can block or tear on its way through. Don't make them sick and don't "
    "give them anything to eat or drink; keep a spare of whatever it was to show the staff.",
)

SWALLOWED_BAD_SELF = (
    "Ring 999 or 911 now: a battery, a magnet or anything sharp or long can burn or block within "
    "hours, however well you feel. Don't make yourself sick and don't eat or drink anything; keep a "
    "spare of whatever it was to show the staff.",
    "That is a 999 or 911 call now, not a wait-and-see: a battery burns, and a magnet or anything "
    "sharp or long can block or tear on its way through. Don't make yourself sick, don't "
    "eat or drink anything, and take a spare of whatever it was with you.",
)

TYPED_TYPOS = {"siezure": "seizure", "siezures": "seizures", "siesure": "seizure",
               "siesures": "seizures", "siezuring": "seizing", "siezed": "seized",
               "braethe": "breathe", "braethes": "breathes", "braething": "breathing",
               "braethed": "breathed", "breate": "breathe", "breatheing": "breathing",
               "kll": "kill", "klling": "killing", "k!ll": "kill", "k1ll": "kill",
               "k!lling": "killing", "k1lling": "killing"}

LOOKS_REAL = frozenset(
    "seize seized seizes seizing secure secured securer secures securely security securing"
    " securer security"
    " breadth breadths cheat cheats cheated cheating cheater chests flop flops flopped flopping"
    " wreathe wreathes wreathed wreathing breather breathers breathable breathers"
    " floppy-disk choked chokes choking-hazard overdo overdos overdoes overdos overdid overdoing"
    " overdone flappy flippy".split())

NOT_NOW_FICTION = (
    r"\bfor\s+(?:a|my|the)\s+(?:story|novel|book|film|script|screenplay|essay|assignment|character)\b",
    r"\bin\s+(?:a|my|the)\s+(?:story|novel|book|film|game|dream)\b",
    r"\b(?:story|novel|script|screenplay|essay|film)\b.*\b(?:character|plot|scene)\b",
    r"\bmy\s+(?:character|protagonist)\b",
)

NOT_NOW = NOT_NOW_FICTION + (
    r"\bif\s+(?:someone|a\s+person|somebody|you|your\s+friend)\b",
    r"\bwhat\s+(?:do|should)\s+(?:you|i|we)\s+do\s+(?:if|when)\b",
    r"\bwhat\s+(?:if|would\s+happen\s+if)\b",
    r"\bhow\s+do\s+you\s+(?:help|treat|deal\s+with)\b",
    r"\bhow\s+(?:can|do|should)\s+(?:i|we|you)\s+(?:help|support|talk\s+to|deal\s+with|approach|comfort)\b",
    r"\bfirst\s+aid\s+(?:for|course|kit|training)\b",
    r"\b(?:qualified|trained|training|work(?:ing)?\s+as)\b.*\b(?:nurse|doctor|paramedic|lifeguard)\b",
    r"\b(?:how|what)\b.{0,15}\b(?:know|tell|spot|recognise|recognize|signs?|symptoms?)\b",
    r"\bwhat\s+does\b.{0,25}\b(?:feel\s+like|look\s+like|mean|do\s+to\s+you)\b",
    r"\b(?:signs?|symptoms?|causes?|cause[sd]?|prevent\w*|reduce\s+the\s+risk)\b.{0,25}"
    r"\b(?:of\s+)?(?:a\s+)?(?:stroke|seizures?|choking|anaphyla\w*|asthma|hypo\w*|heart\s+attack)\b",
)

WORLD_QUESTION = (
    r"\bwhat\s+(?:causes?|are\s+the\s+causes?)\b", r"\bwhy\s+(?:do|does|would)\b",
    r"\b(?:symptoms?|signs?|treatment|rate|rates|statistics|study|research|awareness|prevention)\b",
    r"\bwhat\s+(?:is|are)\s+(?:the\s+)?(?:difference|best\s+way)\b",
    r"\bhow\s+(?:common|likely|dangerous|many|often)\b", r"\b(?:book|film|documentary|series|article)\s+about\b",
    r"\bcarbon\s+monoxide\b.{0,30}\b(?:dangerous|kill\w*|harm\w*|fatal|safe)\b",
    r"\b(?:is|are|can|does|do)\b.{0,25}\b(?:carbon\s+monoxide|co\s+(?:alarm|detector|monitor))\b"
    r".{0,30}\b(?:dangerous|kill\w*|harm\w*|fatal|safe)\b",
)

ACCIDENT = (
    r"\b(?:cut|cutting|nicked|sliced|grazed|scraped|hurt|burn\w*|scalded|injured)\s+my\s*self\b"
    r".{0,24}\b(?:while\s+(?:shaving|chopping|cooking|slicing|peeling|grating|opening|washing|"
    r"cleaning|gardening|trimming|diy|cooking\s+dinner|making)|at\s+(?:work|netball|football|rugby|"
    r"hockey|school|the\s+gym|training|practice)|playing\s+(?:football|rugby|netball|hockey|"
    r"basketball|tennis|squash|badminton)|doing\s+(?:diy|the\s+gardening|the\s+decorating)|"
    r"accidentally|by\s+(?:accident|mistake)|on\s+accident)\b",
    r"\b(?:cut|cutting|nicked|sliced|grazed|scraped|hurt)\s+my\s*self\s+(?:again\s+)?"
    r"(?:shaving|chopping|cooking|slicing|peeling|grating|opening|washing|cleaning|gardening|"
    r"trimming|diy)\b",
    r"\b(?:cut|cutting|nicked|sliced|grazed|scraped|hurt|burn\w*|scalded)\s+my\s*self"
    r"(?:\s+\w+){0,2}\s+(?:on|with)\s+(?:(?:a|an|the|some)\s+)?(?:\w+\s+){0,5}"
    r"(?:knife|glass|tin|can|blade|lid|grater|packet|jar|pan|"
    r"oven|kettle|saw|drill|branch|wire|needle|pin|scissors|hot\s+water|boiling\s+water)\b",
) + INJURY_HOW

SELF_HARM_AGAIN = (
    r"\bmyself\s+again\b",
    r"\b(?:cut|cutting|cuts|sliced|nicked|scratched)\s+my\s*self\b[^.?!]{0,30}"
    r"\b(?:glass|mirror|shards?|blade|razor)\b[^.?!]{0,8}\bagain\b",
)

CRISIS_WORD = re.compile(
    r"\b(?:dead|died|die|dying|death|kill|killing|suicide|suicidal|exist|existing|ending|"
    r"end\s+it|hopeless|worthless|burden|disappear|better\s+off|no\s+reason|give\s+up|"
    r"\bi\s+have\s+a\s+plan|see\s+the\s+point|what'?s\s+the\s+point|"
    r"(?:my|the|his|her|their)\s+(?:last\s+|first\s+|second\s+|previous\s+|suicide\s+|own\s+)?"
    r"attempt\b(?!\s+at\b)|suicide\s+attempt|attempted\s+suicide|overdos\w*|"
    r"tried\s+to\s+(?:kill|end)\s+my\s*self)\b", re.I)

CRISIS_PLAN_SAID = (
    r"\bi\s+know\s+how\s+i'?d\s+(?:do\s+it|end\s+it|go\b|be\s+done)\b",
    r"\b(?:i'?d|i\s+would)\s+know\s+(?:exactly\s+)?how\s+to\s+do\s+it\b",
    r"\bsuicide\s+note\b|\bgoodbye\s+letter\b",
    r"\b(?:wrote|written|writing)\s+(?:the|my)\s+note\b",
    r"\bthe\s+note\s+is\s+written\b",
    r"\b(?:gave|giving|given)\s+(?:all\s+)?my\s+(?:\w+\s+)?(?:things|stuff|belongings|"
    r"possessions|clothes|books|records)\s+(?:all\s+)?away\b(?!\s+to\s+(?:a|the|my)?\s*"
    r"(?:charity|shops?|charity\s+shop|hospice|tip|car\s+boot|boot\s+sale|jumble\s+sale))",
    r"\b(?:said|saying|written)\s+(?:my\s+)?goodbyes?\b",
    r"\bwon'?t\s+be\s+around\b(?!\s+(?:next|on|today|tomorrow|tonight|this|at|for|till|"
    r"until|before|during|in|friday|monday|tuesday|wednesday|thursday|saturday|sunday)\b)",
    r"\bnot\s+(?:be\s+)?around\s+(?:much\s+)?(?:longer|after\s+this)\b",
    r"\b(?:got|bought|have|saved)\s+(?:the|a)\s+(?:pills|tablets|rope|noose|razors?)\s+"
    r"(?:ready|sorted|saved|lined\s+up|in\s+my\s+(?:bag|pocket|drawer|room))\b",
    r"\btied\s+a\s+noose\b",
)

SELF_HARM_REASON = (
    r"\b(?:want|wanna|need)\s+to\s+(?:keep\s+going|carry\s+on|go\s+on|give\s+up|end\s+it|"
    r"stop|disappear|not\s+be\s+here|die)\b",
    r"\b(?:on\s+purpose|deliberately|every\s+(?:day|night|week)|all\s+the\s+time|"
    r"to\s+cope|to\s+feel|to\s+punish|to\s+calm\s+down|to\s+hurt\s+my\s*self|"
    r"to\s+see\s+(?:the\s+)?blood|to\s+relieve|to\s+stop\s+the\s+noise|"
    r"to\s+feel\s+(?:something|anything|real|pain)|"
    r"when\s+(?:i|im|i'?m)\s+(?:get\s+|got\s+|am\s+|feel\s+)?"
    r"(?:overwhelmed|upset|anxious|stressed|panicky|low|angry|numb))\b",
)

END_MEANS_OTHER = (
    r"\b(?:he|she|they|my\s+(?:mum|mom|mother|dad|father|son|daughter|child|kid|brother|sister|"
    r"step\w+|husband|wife|partner|boyfriend|girlfriend|fella|ex|friend|mate|flatmate|housemate|"
    r"neighbou?r|colleague|boss|classmate|patient|client|lodger|aunt|auntie|uncle|cousin|nephew|"
    r"niece|gran|nana|nan|grandad|grandpa|grandson|granddaughter))\b[^.?!]{0,30}"
    r"\b(?:end(?:ing)?\s+(?:it|(?:his|her|their)\s+(?:own\s+)?life)|kill\s+(?:him|her|them)sel(?:f|ves)|"
    r"take\s+(?:his|her|their)\s+own\s+life)\b",
)

END_IT_WITH_NOUN = (
    r"(?:husband|wife|partner|boyfriend|girlfriend|fella|missus|fiance|fiancee|ex|marriage|"
    r"relationship|dad|mum|mom|father|mother|son|daughter|child|children|brother|sister|family|"
    r"parents|inlaws|in\s+laws|flatmate|housemate|tenant|colleague|mate|friend|friends|boss|job|"
    r"course)"
)

SELF_HARM_DESERVE = (
    r"\bdeserve[sd]?\s+(?:it|this|pain)\b",
    r"\bi\s+deserve[sd]?\s+(?:to\s+)?(?:hurt|suffer|die|be\s+in\s+pain|the\s+pain)\b",
)

WISH_BY_MODAL = (
    r"\bi\s+(?:should|ought\s+to|might\s+as\s+well|may\s+as\s+well)\s+"
    r"(?:just\s+|probably\s+|really\s+|honestly\s+|seriously\s+)?"
    r"(?:die\b(?!\s+(?:my|the|it|them|her|his|your|laughing|of\s+laugh(?:ing|ter))\b)|"
    r"be\s+dead\b(?!\s+(?:after|following)\b)|"
    r"kill\s+my\s*self\b|end\s+my(?:\s+own)?\s+life\b|"
    r"not\s+be\s+here\b(?!\s*[^.?!]{0,40}\bshould\s+be\s+(?!dead|gone))|"
    r"be\s+gone\b(?!\s+(?:by|before)\b))",
    r"\bi\s+(?:should|ought\s+to|might\s+as\s+well|may\s+as\s+well)\s+(?:\w+\s+){0,2}end\s+"
    r"(?:it|things)\s*(?:[.?!]|$|tonight\b|now\b|for\s+good\b)",
)

_FLAT_WISH_HOW = (
    r"|like\s+(?:this|that|a\s+(?:prisoner|slave|dog|zombie|captive))"
    r"|(?:this|that)\s+way"
    r"|(?:this|my)\s+life"
    r"|(?:my\s+)?life\s+for\s+(?:others|other\s+people|everyone\s+else|everybody\s+else)"
    r"|for\s+(?:other\s+people|others|everyone\s+else|everybody\s+else)"
)

END_THING = (
    r"\b(?:end(?:ing)?|close|closing|finish(?:ing)?|wrap(?:ping)?\s+up)\b"
    r"[^.?!]{0,24}\b(?:this|that|the|my|an?)\s+(?:email|e-mail|letter|report|essay|list|form|"
    r"filing|tax\s+return|argument|row|draft|chapter|book|project|job|task|sentence|code|story|"
    r"application|coursework)\b",
    r"\b(?:this|that|the|my|an?)\s+(?:email|e-mail|letter|report|essay|list|form|filing|"
    r"tax\s+return|argument|row|draft|chapter|book|project|job|task|sentence|code|story|"
    r"application|coursework)\b[^.?!]{0,24}\b(?:end(?:ing)?|close|closing|finish(?:ing)?)\b",
)

GIVING_UP_HELD_ON = (
    r"\b(?:can'?t|cannot|can\s+not|won'?t|will\s+not|don'?t|do\s+not|didn'?t|did\s+not|"
    r"doesn'?t|does\s+not|shouldn'?t|should\s+not|mustn'?t|must\s+not|wouldn'?t|would\s+not|"
    r"never|not|no\s+longer)\s+(?:ever\s+)?"
    r"(?:giv(?:e|es|ing)|gave|giv(?:en))\s+up\b",
)

SELF_HARM_NOT_EATING = (
    r"\b(?:stopped|stop|quit|not|haven'?t|hasn'?t|hadn'?t|didn'?t|have\s+not|has\s+not|"
    r"had\s+not|did\s+not)\s+(?:been\s+)?(?:eating|drinking|eaten|ate|eat|drink|drunk)\b"
    r"(?=\s*(?:$|"
    r"[.,!?;]|on\s+purpose|deliberately|again\b|anymore\b|at\s+all\b|properly\b|much\b|"
    r"for\b|in\s+(?:days|weeks|a\s+week|a\s+while)\b|since\b))",
    r"\b(?:haven'?t|hasn'?t|hadn'?t|have\s+not|has\s+not|had\s+not)\s+(?:eaten|had)\s+"
    r"(?:anything|much)\b(?=(?:\s+to\s+(?:eat|drink))?\s*(?:$|[.,!?;]|on\s+purpose|"
    r"deliberately|in\s+days\b|for\s+days\b|all\s+day\b|today\b))",
    r"\bbarely\s+(?:eaten|eating|eat|ate|drunk|drinking|drink)\b",
    r"\b(?:ate|eat|eating)\s+nothing\b"
    r"(?=\s*(?:[.,!?;]|$|on\s+purpose|deliberately))",
    r"\b(?:skip|skipped|skipping)\s+(?:a\s+meal|meals|food)\b"
    r"(?=\s*(?:[.,!?;]|$|on\s+purpose|deliberately))",
    r"\b(?:went|go|going|gone)\s+without\s+(?:food|eating)\b"
    r"(?=\s*(?:[.,!?;]|$|on\s+purpose|deliberately))",
    r"\brefused\s+(?:food|to\s+eat)\b"
    r"(?=\s*(?:[.,!?;]|$|on\s+purpose|deliberately))",
)

SELF_HARM_DELIBERATE_ACT = (
    r"\b(?:hurt|hurting|cut|cutting|burn|burnt|burned|burning|scald|scalded|scalding|"
    r"bruise|bruised|bruising|starve|starved|starving|scratch|scratched|scratching|"
    r"hit|hitting|bang|banged|banging|harm|harmed|harming|poison|poisoned|poisoning|"
    r"smash|smashed|smashing|bite|biting|bit|bitten|break|breaks|broke|broken|breaking|"
    r"punish|punished|punishing|stab|stabbed|stabbing|slit|slitting|slash|slashed|"
    r"punch|punched|punching|choke|choked|choking|strangle|strangled|strangling|"
    r"suffocate|suffocated|suffocating|smother|smothered|smothering|wound|wounded|wounding|"
    r"electrocute|electrocuted|electrocuting|slice|sliced|slicing|"
    r"hang|hanged|hanging|hung|drown|drowned|drowning)"
    r"\b[^.?!]{0,24}"
    r"\b(?:my\s*self|me|my\s+(?:own\s+)?(?:arm|arms|wrist|wrists|leg|legs|thigh|thighs|stomach|"
    r"belly|head|hand|hands|finger|fingers|skin|face|eye|eyes|neck|throat|mouth|tongue|jaw|"
    r"lip|lips|ear|ears|nose|cheek|cheeks|forehead|temple|temples|back|shoulder|shoulders|"
    r"rib|ribs|knee|knees|foot|feet|ankle|ankles|hip|hips|chest|body|abdomen|waist|spine|"
    r"bone|bones|vein|veins|groin))\b",
    r"\bgave\s+my\s*self\s+(?:a\s+)?(?:black\s+eye|black\s+eyes|bruise|burn|cut|gash)\b",
    r"\b(?:shoot|shoots|shooting|shot)\s+(?:my\s*self|me|my\s+(?:own\s+)?(?:arm|arms|leg|legs|thigh|"
    r"thighs|stomach|belly|head|hand|hands|chest|body|foot|feet|neck|mouth|face))\b",
    r"\b(?:set|setting)\s+(?:my\s*self|me|my\s+(?:own\s+)?(?:arm|arms|leg|legs|hand|hands|clothes|"
    r"clothing|shirt|shirts|trousers|jumper|jumpers|coat|hoodie|sleeve|sleeves|body))\s+"
    r"(?:on\s+fire|alight|ablaze)\b",
    r"\bset\s+fire\s+to\s+(?:my\s*self|me|my\s+(?:arm|arms|leg|legs|hand|hands|clothes|"
    r"clothing|shirt|shirts|trousers|jumper|jumpers|coat|hoodie|sleeve|sleeves|body))\b",
    r"\bpoured\s+(?:petrol|gasoline|fuel|lighter\s+fluid|white\s+spirit)\s+(?:on|over)\s+"
    r"(?:my\s*self|me|my\s+(?:arm|arms|leg|legs|hand|hands|clothes|clothing|shirt|shirts|"
    r"trousers|jumper|jumpers|coat|hoodie|sleeve|sleeves|body))\b",
    r"\b(?:made|make|making)\s+my\s*self\s+(?:sick|throw\s+up|vomit|pass\s+out|bleed)\b",
    r"\b(?:cut|cutting|cut\s+up|burn|burnt|burned|burning|hurt|hurting|starve|starved|starving|"
    r"bleed|bleeding|overdose|overdosed)\b(?:\s+(?:too\s+)?(?:deep|deeper|badly))?\s+"
    r"(?:on\s+purpose|deliberately)\b",
    *SELF_HARM_NOT_EATING,
    r"\b(?:took|take|taking|taken|had|have|having|swallowed|swallow|swallowing|downed|"
    r"downing|popped|popping|necked|drank|drink|drinking|drunk|ate|eat|eating|eaten)\s+"
    r"(?:(?:too\s+many|some|the|those|these|my|his|her|their|a|an|every|"
    r"all(?:\s+(?:my|his|her|their|the|these|those))?)\s+)?(?:pills?|tablets?|paracetamol|"
    r"ibuprofen|painkillers?|meds|medicines?|sleeping\s+pills?|antidepressants?|"
    r"tranquill?i[sz]ers?|insulin|bleach|detergent|disinfectant|antifreeze|weed\s?killer|"
    r"hand\s+saniti[sz]er|paint\s?thinner|white\s+spirit|drain\s+cleaner|"
    r"cleaning\s+products?|cleaning\s+fluid)\b",
    r"\boverdos(?:e|ed|ing)\b",
    r"\b(?:pull|pulled|pulling)\s+my\s+(?:own\s+)?hair\s+out\b",
    r"\b(?:held|hold|holding)\s+my\s+(?:own\s+)?head\s+under\s+(?:the\s+)?water\b",
    r"\b(?:put|puts|putting|place|placed|placing)\s+my\s+(?:own\s+)?"
    r"(?:hand|hands|arm|arms|finger|fingers|foot|feet)\s+(?:in|into|on)\s+"
    r"(?:the\s+)?(?:fire|flames|boiling\s+water|hot\s+water|stove|hob)\b",
    r"\b(?:crash|crashed|crashing)\s+(?:my|the|our)\s+(?:car|van|motorbike|truck)\b",
    r"\b(?:threw|throw|throwing)\s+my\s*self\s+(?:down\s+(?:the\s+)?stairs|"
    r"under\s+(?:a|the)\s+bus)\b",
    r"\b(?:jump(?:ed|ing|s)?|fell|falling|(?:throw|threw|throwing)\s+my\s*self)\b[^.?!]{0,10}"
    r"\b(?:off|from)\s+(?:a|the|this)\s+(?:bridge|roof|building|cliff|balcony|ledge|car\s*park)\b",
    r"\b(?:ran|run|running|walked|walk|walking|stepped|step|stepping|darted|dart|stood|stand|"
    r"standing|lay|lying|lie)\s+(?:into|in\s+front\s+of)\s+(?:traffic|a\s+bus|a\s+train|"
    r"a\s+car|a\s+lorry|a\s+truck)\b",
    r"\b(?:stood|stand|standing|lay|lying|lie|sat|sit|sitting)\s+on\s+(?:the\s+tracks|"
    r"the\s+track|the\s+railway\s+line|a\s+train\s+track|the\s+line)\b",
    r"\b(?:used|use|using|took|take|taking|held|holding)\s+(?:a|the|my)\s+"
    r"(?:knife|razor|blade|scissors|piece\s+of\s+glass|glass)\s+(?:on|to|against)\s+"
    r"(?:my\s*self|me|my\s+(?:arm|arms|wrist|wrists|leg|legs|thigh|thighs|stomach|belly|"
    r"head|hand|hands|finger|fingers|skin|face|eye|eyes|neck|back|shoulder|shoulders|rib|ribs|"
    r"knee|knees|foot|feet|ankle|ankles|hip|hips|chest|body))\b",
)

HYPERBOLE_BLOCK = (
    r"\b(?:my|his|her|their|our|the)\s+(?:whole\s+)?(?:life|marriage|relationship|family|"
    r"husband|wife|partner|boyfriend|girlfriend|fianc\w+|mum|mom|mother|dad|father|son|"
    r"daughter|child|children|kids?|baby|brother|sister|boss|manager|health|mind|sanity)\b",
    r"\beverything\b", r"\bnothing\b",
    r"\bno\s+point\b", r"\bworthless\b", r"\bhopeless\b", r"\bunbearable\b",
    r"\b(?:died|death|funeral|buried|passed\s+away|lost\s+my|left\s+me|walked\s+out|"
    r"divorce\w*|separation|abuse\w*|hits?\s+me|cancer|tumour|tumor|diagnosis|miscarriage|"
    r"stillborn|overdose\w*|relapse\w*|evicted|homeless|bankrupt)\b",
)

SOMEONE_ELSES_DESPAIR = (
    r"(?:can'?t|cannot|can\s+not)\s+go\s+on\b",
    r"(?:there'?s|there\s+is)\s+no\s+point\b",
    r"\bno\s+point\s+(?:in\s+)?(?:anything|going\s+on|carrying\s+on|anymore)\b",
    r"\bno\s+way\s+out\b",
    r"\b(?:is|are|feels?)\s+hopeless\b",
    r"\b(?:tired|sick)\s+of\s+(?:everything|it\s+all|life|living)\b",
    r"\b(?:wants?|wanted)\s+to\s+(?:die|end\s+it)\b",
    r"\b(?:doesn'?t|does\s+not|don'?t|do\s+not)\s+want\s+to\s+(?:be\s+here|live|go\s+on|wake\s+up)\b",
)

AFTER_EXERCISE = (
    r"\b(?:after|following|post)[-\s]+(?:[a-z]+\s+){0,2}(?:gym|workout|work\s?out|run|running|jog|jogging|"
    r"exercise|exercising|training|session|swim|swimming|cycle|ride|football|rugby|netball|basketball|"
    r"tennis|hockey|lifting|weights|spinning|hiit|class|match|game|climb|climbing|rowing|cardio|"
    r"walk|walking|hike|hiking|steps|mile|miles|5k|10k|stairs)\b",
    r"\b(?:at|in)\s+the\s+gym\b",
    r"\bwhen\s+(?:i\s+|im\s+|i'm\s+)?(?:go\s+|am\s+|start\s+)?(?:running|jogging|walking|climbing|"
    r"cycling|swimming|exercising|training|lifting|playing|rowing|hiking|shovelling|shoveling)\b",
    r"\bwhen\s+i\s+(?:run|jog|walk|climb|cycle|swim|exercise|train|play|lift|row|hike|shovel|shine)\b",
    r"\b(?:on|up)\s+the\s+stairs\b",
    r"\b(?:walking|running|jogging|climbing|cycling|swimming|lifting|exercising)\s+"
    r"(?:up|uphill|fast|hard|home|the\s+(?:hill|stairs))\b",
)

CHEST_EFFORT = (
    "Chest pain that comes on with effort is worth checking today, not next week: ring 111 or your GP "
    "first thing. If it turns to pressure, spreads to the arm or jaw, or comes with breathlessness or "
    "sweating, ring 999 or 911 straight away.",
    "Pain in the chest on effort should be looked at today - ring 111 or your GP first thing, and let "
    "them hear when it comes on. Ring 999 or 911 straight away if it becomes pressure, spreads to the "
    "arm or jaw, or comes with breathlessness or sweating.",
)

CHEST_ASKED = (
    "Chest pain is worth having looked at rather than waiting: ring 111 or your GP today. If it "
    "feels like pressure or tightness, spreads to the arm, jaw or back, or comes with "
    "breathlessness, sweating or feeling sick, ring 999 or 911 straight away.",
    "Most chest pain is not the heart, but it is not something to work out on your own either: get "
    "it looked at today - 111 or your GP. Ring 999 or 911 if it is pressure or tightness, spreads "
    "to the arm or jaw, or comes with breathlessness, sweating or feeling faint.",
)

NOT_STOPPING = (
    r"\b(?:bleeding|blood)\s+(?:through|soak\w*\s+through|through\s+to)\b.{0,20}"
    r"\b(?:cloth|bandage|dressing|towel|plaster|gauze|padding|scarf|t-?shirt|sock|sleeve)s?\b",
    r"\b(?:blood|bleed\w*|cut|wound|gash)\b.{0,40}\b(?:soaked|soaking|soaks|soak)\s+through\b",
    r"\b(?:soaked|soaking|soaks)\s+through\b.{0,20}\b(?:blood|bleed\w*)\b",
    r"\bblood\s+(?:is\s+)?(?:dripping|pouring|running)\b",
    r"\b(?:bleeding|blood)\s+everywhere\b",
)

SOFT_BLEED_OFF = (
    r"\ba\s+bit\b", r"\ba\s+little\b", r"\bslightly\b", r"\b(?:small|paper|shaving)\s+cut\b",
    r"\b(?:gums?|tooth|teeth|mouth\s+ulcer)\b", r"\bperiod\b", r"\bhemorrhoid",
    r"\b(?:tattoo|steak|meat|paint|dye|ink|marker|sauce|juice|tomato|jam|stain|wall|pipes?)\b",
    r"\b(?:has|have|had|it|they)\s+(?:now\s+)?stopp?ed\b", r"\bno\s+longer\s+bleeding\b",
)

BODY_PART = (
    r"\b(?:my|his|her|their|your|our|the)\s+(?:hand|hands|finger|fingers|thumb|arm|arms|leg|legs|knee|"
    r"knees|foot|feet|head|lip|face|chin|shin|wrist|ankle|toe|toes|shoulder|side|back|neck|chest|"
    r"skin|palm|knuckle|forearm|thigh|calf|ear|mouth|eyebrow|scalp|heel|elbow)\b"
)

CHEST_SPREADING = (
    r"\b(?:(?:arm|arms|jaw|shoulders?)\s+(?:went\s+|is\s+|are\s+|feels?\s+|have\s+gone\s+)?"
    r"(?:numb|tingl\w*|pain\w*|ache\w*|hurts?|heav\w*)|numb(?:ness|ed|ing|s)?|tingl\w*|sweat\w*|clammy|"
    r"sick|nausea\w*|vomit\w*|breathless\w*|dizzy|faint\w*|grey|gray|pale|crushing\s+pain)\b",
)

A_PERSON = (
    r"\b(?:i|me|myself|he|she|him|her|they|them|his|hers|their|someone|somebody|anyone|man|"
    r"woman|boy|girl|child|children|baby|babies|toddler|patient|kid|kids|mum|mom|mother|dad|father|"
    r"son|daughter|husband|wife|partner|boyfriend|girlfriend|brother|sister|friend|gran|grandma|"
    r"grandad|grandpa|nan|uncle|aunt|niece|nephew|colleague|neighbour|neighbor|people|men|women|"
    r"workers?|guests?|everyone|anybody)\b",
)

GIVING_UP_GROUP = (
    r"\b(?:team|teams|club|squad|side|players?|group|class|band|orchestra|choir|committee|"
    r"company|staff|crew|panel|jury|government|opposition|management|union|audience|crowd|"
    r"fans?|supporters?|students?|pupils?|workers?|colleagues?|strikers?)\b[^.?!]{0,30}"
    r"\b(?:giv(?:e|es|ing)|gave|giv(?:en))\s+up\b",
)

_DENIED = (
    r"\b(?:i'?m|im|i\s+am|i\s+was)\s+not\s+(?:feeling\s+|really\s+|actually\s+)?"
    r"(?:suicidal|depressed\s+enough|"
    r"thinking\s+(?:about|of)\s+(?:suicide|killing|hurting)|"
    r"going\s+to\s+(?:kill\s+my\s*self|hurt\s+my\s*self)|"
    r"about\s+to\s+(?:kill\s+my\s*self|end\s+it))",
    r"\bi\s+(?:would\s+never|wouldn'?t|will\s+not|won'?t)\s+(?:kill\s+my\s*self|"
    r"hurt\s+my\s*self|harm\s+my\s*self|cut\s+my\s*self|end\s+(?:it|my\s+life)|"
    r"top\s+my\s*self|die)\b",
    r"\bi\s+(?:dont|don'?t|do\s+not)\s+(?:want|wanna)\s+(?:to\s+)?"
    r"(?:kill\s+my\s*self|harm\s+my\s*self|end\s+it|"
    r"top\s+my\s*self)\b",
    r"\bi\s+(?:have\s+)?never\s+(?:felt\s+suicidal|(?:wanted|want)\s+to\s+die|"
    r"thought\s+(?:about|of)\s+suicide|hurt\s+my\s*self)\b",
    r"\bi\s+(?:would\s+)?never\s+want\s+to\s+die\b",
    r"\b(?:not|never)\s+(?:suicidal|thinking\s+about\s+suicide)\b",
)

DAY_TOTAL_WORD = (
    r"\b(?:today|tonight|this\s+morning|this\s+afternoon|this\s+evening|so\s+far|"
    r"this\s+week|over\s+the\s+day|across\s+the\s+day|during\s+the\s+day|in\s+a\s+day|"
    r"in\s+the\s+day|in\s+24\s+hours|since\s+(?:this\s+morning|last\s+night|yesterday|"
    r"6\s?am|lunch))\b",
)

DAY_TOTAL_SIGN = (
    r"\b(?:feel|felt|feeling)\s+(?:sick|ill|rough|queasy|nauseous|dizzy|faint)\b",
    r"\b(?:vomit\w*|throwing\s+up|threw\s+up|been\s+sick|being\s+sick)\b",
    r"\b(?:stomach|tummy|abdomen|belly)\b", r"\byellow\b", r"\bbruis\w*\b",
    r"\b(?:sweat\w*|shaking|shaky|ringing\s+in\s+my\s+ears)\b",
    r"\b(?:overdos\w*|too\s+many|whole\s+(?:packet|pack|box|bottle))\b",
)

SAID_AS_IT_HAPPENS = (
    r"\bright\s+now\b", r"\bnow\b", r"\bsuddenly\b", r"\bcurrently\b",
    r"\bat\s+the\s+moment\b", r"\bas\s+we\s+speak\b", r"\bstill\b", r"\bhappening\b",
    r"\b(?:my|our|his|her|their|the)\s+(?:son|daughter|child|kid|kids|baby|babies|toddler|"
    r"husband|wife|partner|boyfriend|girlfriend|mum|mom|mother|dad|father|friend|mate|"
    r"neighbour|neighbor|brother|sister|grandma|grandad|granny|nan|nana|aunt|uncle|cousin|"
    r"flatmate|roommate|lodger|carer|patient|client|dog|cat|puppy|kitten)(?:'s|s)?\b",
    r"\bstop(?:ped|ping|s)?\s+breathing\b", r"\bnot\s+breathing\b", r"\bisn'?t\s+breathing\b",
    r"\bwon'?t\s+wake\b", r"\bwont\s+wake\b", r"\bno\s+pulse\b", r"\bunresponsive\b",
)

OWN_CRY = (
    r"\b(?:i|im|i'm|i've|me|my)\b[^.?!]{0,25}\b(?:suicid\w*|self[-\s]?harm\w*|"
    r"kill\s+my\s*self|want\s+to\s+die|wants?\s+to\s+die|not\s+want\s+to\s+(?:live|be\s+here)|"
    r"don'?t\s+want\s+to\s+(?:live|be\s+here)|end\s+it\s+all|better\s+off\s+dead|"
    r"hurt\s+my\s*self|harm(?:ing)?\s+my\s*self|cutting\s+my\s*self|hope?less)\b",
    r"\b(?:suicid\w*|self[-\s]?harm\w*)\b[^.?!]{0,25}\b(?:i|me|my)\b",
)

SELF_HARM_CUT_NO_OBJECT = (
    r"\b(?:i\s+)?(?:want|wanna|wanting|need|needing|feel\s+like|feeling\s+like|felt\s+like|"
    r"thinking\s+(?:of|about)|planning\s+(?:to|on)|going\s+to|about\s+to)\s+(?:to\s+)?"
    r"(?:just\s+)?cut(?:ting)?\s*(?:$|[.?!;,]|\b(?:something|tonight|again)\b|"
    r"\bso\s+(?:bad|much|badly)\b|\breally\s+bad(?:ly)?\b)",
)

ABUSE_FINE_PLACE = (
    r"(?:^|\s)(?:someone|somebody|a\s+(?:man|bloke|guy|woman|lad)|(?:the|our|my)\s+neighbours?|"
    r"next\s+door)\b[^.?!]{0,30}\bthreaten(?:s|ed|ing)?\s+me\b"
    r"[^.?!]{0,40}\b(?:at\s+work|from\s+work)\b",
    r"(?:^|\s)(?:someone|somebody|a\s+(?:man|bloke|guy|woman|lad))\s+"
    r"(?:at\s+work|from\s+work)\b[^.?!]{0,40}"
    r"\bthreaten(?:s|ed|ing)?\s+me\b",
)

VIOLENT_THREAT = (
    r"\b(?:kill|kills|killed|killing|murder|murders|stab(?:s|bed|bing)?|shoot|shoots|shot|"
    r"gun|guns|knife|knives|weapon|weapons|strangle|strangled|choke|choked|rape|raped|"
    r"beat|beats|beating|punch|punches|punched|slap|slaps|slapped|hit|hits|hitting|"
    r"hurt|hurts|hurting|harm|harms|attack|attacks|attacked|throat|"
    r"in\s+danger|scared|terrified|afraid|following\s+me|waiting\s+outside|come\s+after\s+me)\b",
)

ABUSE_PLAY = (
    r"\bmy\s+(?:kid|kids|child|children|son|daughter|sister|brother|mate|mates|friend|friends|"
    r"cousin|flatmate|housemate|boy|girl)\b[^.?!]{0,25}\b(?:push(?:ed|es)|shov(?:ed|es)|"
    r"thr(?:ew|ows)|dump(?:ed|s)|pull(?:ed|s)|drag(?:ged|s))\s+(?:me|us)\s+(?:on)?to\s+"
    r"(?:the\s+|a\s+|my\s+)?(?:sofa|couch|bed|floor|cushions?|beanbag|trampoline|grass|mattress)\b",
)

ABUSE_PLAY_HARD = (
    r"\b(?:held|holding|hold|pinned|trapped|punch(?:ed|es|ing)?|kick(?:ed|s|ing)?|"
    r"slap(?:ped|s|ping)?|throat|neck|choke(?:d|s|ing)?|strangl(?:ed|es|ing)|kill\w*|"
    r"murder\w*|rape\w*|bruis(?:e|es|ed|ing)|blood|bleed\w*|hit|hits|hitting|beat|beaten|"
    r"beating|drunk|scared|afraid|terrified|frightened|worthless|useless|stupid|thick|"
    r"fat|ugly|whore|slut|bitch|cunt|shut\s+up)\b",
)

ABUSE_HANDS_ON = (
    r"\b(?:push(?:ed|es|ing)|shov(?:ed|es|ing)|grab(?:bed|s|bing)|drag(?:ged|s|ging)|"
    r"pull(?:ed|s|ing)|held|holding|hold|pinn(?:ed|ing)|press(?:ed|ing)|slam(?:med|s|ming)|"
    r"thr(?:ew|own|owing)|kick(?:ed|s|ing)|punch(?:ed|es|ing)|hit|hits|hitting|slapp?(?:ed|ing)|"
    r"chok(?:ed|es|ing)|strangl(?:ed|es|ing)|bit|bitten|bent\s+my|twist(?:ed|ing)\s+my|"
    r"yank(?:ed|ing)|wrench(?:ed|ing))\s+(?:me|us|my|our)\b",
    r"\bby\s+the\s+(?:hair|throat|neck|arm|wrist|collar)\b",
    r"\b(?:held|pinned|pressed|slammed|shoved|pushed|threw)\s+(?:me|us)\s+(?:against|onto|into|to)\b",
)

ABUSE_QUARREL = (
    r"\b(?:corner(?:ed|s)?|pinned|trapped|stuck|backed|blocked|held|shout(?:ed|s|ing)?\s+at|"
    r"yell(?:ed|s|ing)?\s+at|argu(?:ed|es|ing))\b[^.?!]{0,30}\b(?:about|over)\s+"
    r"(?:the\s+|a\s+|my\s+|our\s+|his\s+|her\s+|these\s+|those\s+)?(?:deadline|deadlines|rota|"
    r"roster|budget|essay|review|appraisal|numbers|figures|report|proposal|invoice|quotes?|tax|"
    r"paper|project|contract|bills?|homework|exam|presentation|spreadsheet|work|targets?|quotas?|"
    r"results?|grades?|coursework|assignment|bins?|rubbish|recycling|bin\s+day|shopping|chores?|"
    r"mess|washing|washing[\s-]up|dishes|dinner|tea|bedtime|school|laundry|ironing|hoovering|"
    r"litter|garden|hedge|car|keys|holiday|guests?|tv|telly|remote|football|dog|cat|nappies|"
    r"nappy|toys?|clutter|tidying)\b",
)

ABUSE_CHILD_REFUSAL = (
    r"\b(?:my|our)\s+(?:son|sons|daughter|daughters|kid|kids|child|children|baby|toddler|"
    r"teen|teens|teenager|teenagers|boy|girl|boys|girls)\b[^.?!]{0,25}\b(?:won'?t|wont|"
    r"wouldn'?t|wouldnt|didn'?t|doesn'?t|(?:will|would|do|does|did)\s+not|refus(?:es?|ed)\s+to|"
    r"never\s+lets?)\s+(?:let|allow)\s+me\b",
)

ABUSE_PARENT_REFUSAL = (
    r"\b(?:my\s+)?(?:mum|mom|mother|dad|father|parents|step\s?dad|step\s?mum|step\s?mom|"
    r"step\s?parents|guardian|guardians)\b[^.?!]{0,25}\b(?:won'?t|wont|wouldn'?t|wouldnt|"
    r"didn'?t|doesn'?t|(?:will|would|do|does|did)\s+not|refus(?:es?|ed)\s+to|never\s+lets?)\s+"
    r"(?:let|allow)\s+me\s+" + _REFUSED_EXIT + r"\b",
)

ANY_REFUSAL_TO_GO = (
    r"\b(?:won'?t|wont|wouldn'?t|wouldnt|didn'?t|doesn'?t|(?:will|would|do|does|did)\s+not|"
    r"refus(?:es?|ed|ing)\s+to|never\s+lets?|not\s+letting|(?:is|was|are|were)n'?t\s+letting)\s+"
    r"(?:let|allow)\s+me\s+" + _REFUSED_EXIT + r"\b",
)

A_HAND_ON_THE_PERSON = (
    r"\b(?:grab(?:bed|s|bing)|seiz(?:ed|es|ing)|twist(?:ed|ing)|yank(?:ed|ing)|"
    r"wrench(?:ed|ing)|pinn(?:ed|ing)|pins|pinning|held|hold|holding|squeez(?:ed|ing)|"
    r"shook|shak(?:en|es|ing)|pull(?:ed|s|ing)|slam(?:med|s|ming)|press(?:ed|ing)|"
    r"clamp(?:ed|ing)|lift(?:ed|ing))\s+(?:me|us|my|our)\s*(?:by\s+the\s+)?"
    r"(?:arm|arms|wrist|wrists|hair|throat|throats|neck|necks|collar|collars|shoulder|"
    r"shoulders|hand|hands|face|jaw|mouth|leg|legs|waist|back|fist|fists|clothes|shirt|"
    r"top|jumper|hood|scarf|belt)\b",
    r"\b(?:push(?:ed|es|ing)|shov(?:ed|es|ing)|drag(?:ged|s|ging)|kick(?:ed|s|ing)|"
    r"punch(?:ed|es|ing)|slapp?(?:ed|ing)|hit|hits|hitting|chok(?:ed|es|ing)|"
    r"strangl(?:ed|es|ing)|bit|bitten|thr(?:ew|own|owing)|flung)\s+(?:me|us|him|her|them)\b"
    r"(?!\s+to\b)(?:\s+(?:by|against|across|onto|into|down|over|off|out\s+of|in\s+the|"
    r"on\s+the)\b|[\s.,!?]|$|\s+(?:again|hard|back)\b)",
    r"\b(?:grab(?:bed|s|bing)|shov(?:ed|es|ing)|shook|kick(?:ed|es)|punch(?:ed|es))\s+"
    r"(?:me|us|him|her|them)\s*(?:[.,!?]|$|and\b|while\b|so\b|then\b)",
)

ABUSE_EMPLOYER_REFUSAL = (
    r"\b(?:boss|manager|supervisor|employer|company|firm|agency|payroll|hr|rota|rotas|shift|"
    r"shifts|roster|office|workplace|job)\b[^.?!]{0,40}?\b(?:won'?t|wont|wouldn'?t|wouldnt|"
    r"will\s+not|doesn'?t|doesnt|does\s+not|refuses?|refused|not\s+letting)\b[^.?!]{0,15}?"
    r"\b(?:let|allow)\s+me\b",
)

ABUSE_PARENT_REFUSAL_HARD = (
    r"\b(?:hit|hits|hitting|punched|punching|beat|beaten|beating|kick(?:ed|s|ing)|chok(?:ed|es|ing)|"
    r"strangl(?:ed|es|ing)|slapp?(?:ed|s|ing)?|threw|thrown|hurt\s+me|hurts\s+me|bruis(?:e|es|ed)|"
    r"blood|black\s+eye|split\s+lip|dragged|dragging|scare(?:s|d)?|scaring|terrified|afraid|"
    r"frightened|frighten(?:s|ing)?|raped|"
    r"assaulted|threaten(?:s|ed|ing)?|locked|lock(?:s|ing)\s+me|shut\s+me|starve\w*|no\s+food|"
    r"belt|punish(?:ed|es|ing)?|burn(?:s|ed|ing)\s+me|handcuff\w*|tied\s+me)\b",
)

PARENT_REFUSAL_BLOW = (
    r"\b(?:hit|hits|hitting|punch(?:ed|es|ing)?|kick(?:ed|s|ing)?|beat|beats|beaten|beating|"
    r"slapp?(?:ed|s|ing)?|chok(?:ed|es|ing)|strangl(?:ed|es|ing)|grabb(?:ed|es)|drag(?:ged|s|ging)|"
    r"shov(?:ed|es)|push(?:ed|es)|thr(?:ew|own)|lock(?:ed|s|ing)|shut|shuts|shutting)\s+"
    r"(?:me|us)\b",
    r"(?<!\bi\s)(?<!\bwe\s)\b(?:hit|hits|hitting|punch(?:ed|es|ing)?|kick(?:ed|s|ing)?|"
    r"beat|beats|beaten|beating|slapp?(?:ed|s|ing)?|grabb(?:ed|es)|drag(?:ged|s|ging)|"
    r"shov(?:ed|es)|push(?:ed|es)|thr(?:ew|own)|lock(?:ed|s|ing)|shut|shuts|shutting)\s+"
    r"my\s+(?:arm|leg|face|head|back|ribs?|stomach|throat|hair|wrist|shoulder|neck|side|"
    r"chest|knee|hip|belly|jaw|nose|hand|foot|feet|eye|ear)\b",
    r"\b(?:hurt|hurts|hurt|hurting)\s+(?:me|my\s+\w+|us)\b",
    r"\b(?:he|she|they|dad|mum|mother|father|step\s?dad|step\s?mum|parents?|guardian)\b"
    r"[^.]{0,12}\b(?:scares?|scared|scaring|terrif(?:ies|ied)|frighten(?:s|ed|ing)?)\s+"
    r"(?:me|us)\b",
    r"\b(?:afraid|frightened|scared)\s+of\s+(?:him|her|them|my\s+(?:dad|mum|stepdad|"
    r"stepmum))\b",
    r"\b(?:threaten(?:s|ed|ing)?\s+(?:me|us|to\s+kill)|gave\s+me\s+a\s+(?:bruise|black\s+eye|"
    r"split\s+lip)|left\s+me\s+with\s+a\s+(?:bruise|black\s+eye|split\s+lip)|"
    r"belt|burn(?:s|ed|ing)?\s+me|starve\w*|no\s+food|handcuff\w*|tied\s+me|"
    r"rap(?:e|ed|es)|assault(?:ed|s)?)\b",
)

ABUSE_BENIGN_REASON = (
    r"\b(?:corner(?:ed|s)?|trapped|backed|blocked|pinned|shov(?:ed|es)|push(?:ed|es)|held)\s+"
    r"(?:me|us)\b[^.?!]{0,30}\bfor\s+(?:a\s+|the\s+|my\s+|your\s+|his\s+|her\s+)?(?:hug|"
    r"selfie|photo|picture|cup\s+of\s+tea|tea|coffee|cake|biscuit|dinner|"
    r"lunch|breakfast|leak|boiler|fuse|hoover|washing|shopping|presents?|surprise|tickets?|letter|"
    r"parcel|book|coat|keys)\b",
    r"\b(?:corner(?:ed|s)?|trapped|backed|blocked|pinned|shov(?:ed|es)|push(?:ed|es)|held)\s+"
    r"(?:me|us)\b[^.?!]{0,30}\bto\s+(?:give|show|hand|fetch|get|check|fix|make|find|"
    r"bring|grab|take|give\s+over)\s+(?:me\s+|us\s+)?(?:a\s+|the\s+|my\s+|your\s+|his\s+|"
    r"her\s+)?(?:hug|selfie|photo|picture|cup\s+of\s+tea|tea|coffee|cake|"
    r"biscuit|dinner|lunch|breakfast|leak|boiler|fuse|hoover|washing|shopping|presents?|surprise|"
    r"tickets?|letter|parcel|book|coat|keys)\b",
    r"\b(?:blocked|shoved|shoved?|pushed|backed|pinned)\s+(?:me|us)\s+[^.?!]{0,20}\bwith\s+the\s+"
    r"(?:hoover|vacuum|washing|shopping|pushchair|buggy|pram|bags?|ironing|car\s+seat|bike|"
    r"laundry|bin|mop|ironing\s+board)\b",
    r"\b(?:corner(?:ed|s)?|pinned|trapped|backed|blocked)\b[^.?!]{0,40}\bto\s+(?:talk|ask|"
    r"discuss|pitch|sell|persuade|convince|apologise|apologize|chat|catch\s+up|explain|complain|"
    r"run\s+(?:something|an\s+idea)\s+by|check|tell)\b",
)

ABUSE_BUTTONHOLED = (
    r"\b(?:(?:corner(?:ed|s)?|buttonhol(?:ed|es|ing)|pinned|trapped|backed|blocked)\s+(?:me|us)"
    r"|(?:had|has|have|got|keeps|keeping|kept)\s+(?:me|us)\s+cornered)\b"
    r"[^.?!]{0,40}\babout\s+(?:the|a|an|my|his|her|their|our|some|this|that)\s+"
    r"(?!knife|gun|blade|weapon|pills?|tablets?|money|rent|debt|affair|phone|keys|kids|children|"
    r"divorce|will|deeds|police|hospital|bruises?|drink|drugs?|door|escape|leaving)\w+",
)

ABUSE_KIDS_CARD = (
    r"\b(?:scared|afraid|frightened|terrified|panic(?:king|ked)?|crying|sobbing|shaking|shook|"
    r"hurt\s+me|hurts\s+me|hit|hits|hitting|punched|punch|kick(?:ed|s)|slapped|slap|beaten|"
    r"beat\s+me|choked|choking|strangled|blood|bruis(?:e|es|ed)|black\s+eye|split\s+lip|"
    r"raped|assaulted|worthless|useless|stupid|thick|fat|ugly|drunk|threat(?:ened|ens|s)?)\b",
)

ABUSE_KIDS_AT_HOME = (
    r"\b(?:my|the)\s+(?:kids|children|child|toddler|baby|boys|girls|twins|little\s+ones)\b"
    r"[^.?!]{0,25}\b(?:have|has|had|keep|keeps|keeping|kept)\s+(?:me|us)\s+"
    r"(?:locked|stuck|indoors|in\s+the\s+house|stuck\s+in)\b",
    r"\b(?:my|the)\s+(?:kids|children|child|toddler|baby|boys|girls|twins|little\s+ones)\b"
    r"[^.?!]{0,25}\b(?:won'?t|wont|will\s+not|wouldn'?t|refuses?\s+to|never\s+lets?\s+me)\s+"
    r"(?:let|allow)\s+me\s+(?:leave|go\s+out|out|go\s+anywhere|sleep|sit\s+down|put\s+them\s+down)"
    r"\b",
)

ABUSE_BLOW = (
    r"\b(?:hit|hits|hitting|punch(?:es|ed|ing)?|beat(?:s|en|ing)?|kick(?:s|ed|ing)?|"
    r"chok(?:es|ed|ing)|strangl(?:e|es|ed|ing)|slapp?(?:s|ed|ing)?|threw|thrown|"
    r"hurt\s+me|hurts\s+me|bruis(?:e|es|ed)|blood|black\s+eye|split\s+lip|"
    r"drag(?:s|ged|ging)\s+me|would\s+not\s+let\s+me|wont\s+let\s+me|won'?t\s+let\s+me|"
    r"scared|terrified|afraid|rape|assault)\b",
)

ABUSE_ROOM_FAMILY = (
    r"\b(?:my\s+(?:son|daughter|child|children|kid|kids|baby|toddler|boy|girl|mum|mom|mam|mother|"
    r"dad|father|sister|brother|parent|parents|friend|friends|mate|mates|flatmate|housemate|"
    r"roommate|colleague|co-?worker|cousin|nephew|niece|aunt|uncle|nan|nana|gran|granny|"
    r"grandma|grandad|grandpa|in-laws?|boss|manager|carer)\b|they)\b[^.?!]{0,40}"
    r"\b(?:corner(?:ed|s)?|trapped|trapping|traps|backed|backing|blocked|blocking|pinned|"
    r"pinning)\b",
)

ABUSE_ROOM_CARD = (
    r"\b(?:scared|afraid|frightened|terrified|panic(?:king|ked)?|crying|sobbing|shaking|shook|"
    r"hurt\s+me|hurts\s+me|hit|hits|hitting|punched|punch|kick(?:ed|s)|slapped|slap|beaten|"
    r"beat\s+me|choked|choking|strangled|blood|bruis(?:e|es|ed)|black\s+eye|split\s+lip|"
    r"raped|assaulted|worthless|useless|stupid|thick|fat|ugly|drunk|again|threat(?:ened|ens|s)?|"
    r"would\s+not\s+let|wouldn'?t\s+let|won'?t\s+let|wont\s+let|refus(?:ed|es))\b",
    r"\b(?:let|allow)\s+me\s+(?:go|out|past|leave|through|by)\b",
)

ABUSE_FINE_ANIMAL = (
    r"\b(?:[\w']+\s+)?(?:dog|dogs|puppy|puppies|cat|cats|kitten|kittens|pet|pets|horse|pony|"
    r"rabbit|parrot|hamster|gerbil|ferret|snake|lizard|bird|guinea\s+pig)\s+"
    r"(?:bit|bite|bites|biting|nipped|snapped\s+at|went\s+for|attacked|scratched|clawed)\s+"
    r"(?:me\b|us\b|him\b|her\b|them\b|my\s+(?:hand|hands|leg|legs|arm|arms|face|finger|fingers|"
    r"foot|feet|ankle|wrist|head|neck|lip|cheek|nose|ear|ear|thigh|shoulder))",
    r"\b(?:attacked|bit|bitten|nipped|savaged|mauled|scratched|clawed|stung)\b[^.?!]{0,15}\bby\s+"
    r"(?:(?:a|an|the|my|our|his|her|their)\s+)?(?:[\w'’]+\s+){0,2}"
    r"(?:dog|dogs|puppy|puppies|cat|cats|kitten|kittens|pet|pets|horse|pony|rabbit|parrot|hamster|"
    r"gerbil|ferret|snake|lizard|bird|guinea\s+pig|bees?|wasps?|hornets?|midges?|gnats?|"
    r"mosquito(?:e)?s?|flies|fly|insects?|bugs?)\b",
)

PLAYFUL_HIT = (
    r"\b(?:my\s+)?(?:son|daughter|child|kid|toddler|baby|nephew|niece|grandson|"
    r"granddaughter)\b[^.?!]{0,40}\b(?:hit|hits|slapp?(?:ed|s)?|punch(?:ed|es)?|kicked?)\b"
    r"[^.?!]{0,40}\b(?:play(?:ing)?|playfully|play-?fighting|mucking\s+about|"
    r"messing\s+about|wrestl(?:e|ing)|tickl(?:e|ing)|accidentally|by\s+accident|"
    r"by\s+mistake|didn'?t\s+mean|didnt\s+mean|not\s+on\s+purpose|tantrum)\b",
    r"\b(?:play(?:ing)?|wrestl(?:e|ing)|tickl(?:e|ing)|mucking\s+about|messing\s+about)\b"
    r"[^.?!]{0,40}\b(?:my\s+)?(?:son|daughter|child|kid|toddler|baby)\b[^.?!]{0,40}"
    r"\b(?:hit|slapp?(?:ed|s)?|punch(?:ed|es)?|kicked?)\b",
    r"\b(?:my\s+)?(?:son|daughter|child|kid|toddler|baby|nephew|niece|grandson|granddaughter)\b"
    r"[^.?!]{0,30}\b(?:hit|hits|slapp?(?:ed|s)?|punch(?:ed|es)?|kicked?|head-?butt(?:ed|s)?)\b"
    r"[^.?!]{0,30}\b(?:toy|ball|pillow|block|blocks|stick|book|cup|spoon|remote|brick|lego)\b",
    r"\bh(?:it|its|itting)\s+my\s+(?:hand|arm|finger)s?\s+(?:away|off|aside|back)\b",
)

HIT_IN_FUN = (
    r"\b(?:hit|hits|slapp?(?:ed|s)?|punch(?:ed|es)?|elbow(?:ed|s)?|kick(?:ed|s)?|"
    r"shov(?:ed|es)|push(?:ed|es)?|tap(?:ped|s)?|nudg(?:ed|es)?|whack(?:ed|s)?)\b"
    r"[^.?!]{0,40}\b(?:laugh(?:ing|ed)?|jok(?:e|ing|ed)|kidding|in\s+fun|for\s+fun|"
    r"for\s+a\s+laugh|play(?:ing|ful)?|play-?fighting|fooling\s+about|fooling\s+around|"
    r"messing\s+about|mucking\s+about|teasing)\b",
    r"\b(?:play(?:ing)?|laughing|joking|joking\s+around|messing\s+about|fooling\s+about|"
    r"as\s+a\s+joke|in\s+fun|for\s+a\s+laugh)\b[^.?!]{0,40}"
    r"\b(?:hit|hits|slapp?(?:ed|s)?|punch(?:ed|es)?|elbow(?:ed|s)?|kick(?:ed|s)?|"
    r"shov(?:ed|es)|push(?:ed|es)?)\b",
)

HIT_THE_LAUGH_IS_HIS = (
    r"\b(?:and|then|but|so)\s+(?:he|she|they|everyone|everybody|all\s+of\s+them|"
    r"his\s+mates|her\s+mates|the\s+others)\s+(?:laughed|laughs|was\s+laughing|"
    r"were\s+laughing|is\s+laughing|are\s+laughing|grinned|smiled)\b",
    r"\b(?:and|then)\s+(?:laughed|laughs|laughing)\b",
    r"\b(?:laugh(?:ed|ing)?\s+it\s+off|laughed\s+it\s+away)\b",
    r"\b(?:everyone|everybody|all\s+his\s+mates|all\s+her\s+mates)\s+"
    r"(?:laughed|was\s+laughing|were\s+laughing)\b",
    r"\b(?:he|she|they)\s+(?:was|were|is|are)\s+(?:only\s+|just\s+|always\s+)?"
    r"(?:joking|kidding|laughing|mucking\s+about|messing\s+about|playing|play-?fighting)\b",
    r"\b(?:said|says|saying|told|tells|telling|claimed|claims)\b[^.?!]{0,25}"
    r"\b(?:he|she|they)\s+(?:was|were|is)\s+(?:only\s+|just\s+)?(?:joking|kidding)\b",
    r"\b(?:he|she|they)\s+(?:said|says|told\s+me|tells\s+me|keeps\s+saying)\b"
    r"[^.?!]{0,20}\b(?:joke|joking|fun|banter|laugh)\b",
)

PUSHED_AWAY_REPLY = (
    "A hand pushed away usually is not a blow - but only you know how it landed. If it hurt, or it "
    "frightened you, tell me and I will take it seriously.",
    "That sounds like a hand moved off rather than a hit. If there is more to it than that - it "
    "landed hard, or it is not the first time - say so and I will treat it as the real thing.",
    "Fair enough, that is a hand being moved aside rather than somebody being hit. Was it just that, "
    "or did it feel like more? I would rather ask than assume.",
)

PUSHED_AWAY_THEN_RESTRAINT = (
    r"\b(?:fell|fall|fallen|tripped|slipped)\b",
    r"\b(?:hit|banged|knocked|smashed|bumped)\s+(?:my|the|his|her)\s+(?:head|face|nose|arm|"
    r"shoulder|back|knee|hip|hand|elbow|wall|door|frame|floor|radiator|table|corner|worktop|"
    r"shelf|sideboard|stairs|banister|bed)\b",
    r"\b(?:so|because|till|until)\s+(?:i|he|she)\s+(?:couldn'?t|could\s+not|cant|wasn'?t\s+able)\b",
    r"\b(?:couldn'?t|could\s+not|cant|wouldn'?t|would\s+not)\s+(?:leave|get\s+(?:away|out)|go|move)\b",
    r"\b(?:wouldn'?t|would\s+not|won'?t)\s+let\s+me\b",
    r"\b(?:trapped|held|pinned|dragged|strangled|choked|threatened|hurt|hurts|hurting|bleeding|"
    r"blood|bruise[ds]?|sore|swollen|hard)\b",
)

PUSHED_AWAY_BUT_SOMETHING_ELSE = (
    r"\b(?:pan|pans|hob|oven|stove|grill|kettle|iron|saucepan|frying|boiling|heat|fire|smoke|"
    r"babies|baby|child|children|kid|kids|son|daughter|toddler|pregnant|hospital|ambulance|"
    r"police|999|911|work|office|shift|meeting|game|match|film|tv|phone)\b",
)

PUSHED_AWAY = (
    r"\b(?:push(?:es|ed|ing)?|shov(?:e|es|ed|ing)|slapp?(?:s|ed|ing)?|batt?(?:s|ed|ing)?)"
    r"\s+my\s+"
    r"(?:hand|hands|arm|arms|finger|fingers|shoulder|shoulders|face|head)\s+"
    r"(?:away|off|aside)\b",
)

RESTRAINT_BESIDE = (
    r"\b(?:held|hold|holding|pinn(?:ed|ing)|dragg(?:ed|ing)|wrestl(?:ed|ing)|"
    r"restrain(?:ed|ing)?|"
    r"grabb(?:ed|ing)\s+(?:me|my\s+(?:arm|arms|wrist|wrists|throat|neck|hair|hand|hands|"
    r"shoulders?|waist|leg|legs|body))|"
    r"(?:shov(?:ed|ing)|push(?:ed|ing))\s+me|lock(?:ed|ing)|block(?:ed|ing)|"
    r"shout(?:ed|ing)|yell(?:ed|ing)|scream(?:ed|ing)|threaten(?:ed|ing)?|fell|falling|"
    r"wouldn'?t\s+let\s+me|would\s+not\s+let\s+me|wouldn'?t\s+let\s+go|"
    r"strangl(?:ed|es|ing)|chok(?:ed|es|ing)|hard)\b",
)

BLOW_ON_ME = (
    r"\b(?:hit|hits|hitting|slapp?(?:ed|s|ing)?|punch(?:ed|es|ing)?|kick(?:ed|s|ing)?|"
    r"beat|beats|beating|struck|thump(?:ed|s|ing)?|whack(?:ed|s|ing)?|"
    r"chok(?:ed|es|ing)|strangl(?:ed|es|ing))\s+(?:me|us)\b",
    r"\b(?:hit|hits|hitting|slapp?(?:ed|s|ing)?|punch(?:ed|es|ing)?|kick(?:ed|s|ing)?|"
    r"beat|beats|beating|struck|thump(?:ed|s|ing)?|whack(?:ed|s|ing)?)\s+my\s+"
    r"(?:face|head|back|arm|arms|leg|legs|ribs?|stomach|belly|jaw|eye|eyes|ear|ears|neck|"
    r"throat|shoulders?|chest|side|hips?|thigh|mouth|nose|teeth|wrist|knee)\b",
    r"\b(?:hit|hits|hitting|slapp?(?:ed|s|ing)?|punch(?:ed|es|ing)?|kick(?:ed|s|ing)?|"
    r"beat|beats|beating|struck|thump(?:ed|s|ing)?|whack(?:ed|s|ing)?)\s+my\s+"
    r"(?:husband|wife|partner|boyfriend|girlfriend|son|daughter|child|kid|baby|mum|mom|mother|"
    r"dad|father|brother|sister|friend|mate)\b",
)

A_GROWN_AGE = re.compile(
    r"\b(?:teen(?:ager|aged)?|adolescen\w+|grown\s+up|"
    r"(?:five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|"
    r"seventeen|eighteen|nineteen|twenty|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20)\s*"
    r"(?:years?|yrs?)\s*(?:old)?\b|"
    r"(?:hes|shes|theyre|he'?s|she'?s|they'?re|he\s+is|she\s+is|they\s+are|aged?)\s+"
    r"(?:five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|"
    r"seventeen|eighteen|nineteen|twenty|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20)\b"
    r"(?!\s*months?))",
    re.IGNORECASE)

SMALL_CHILD_LASH_REPLIES = (
    "That is what a small child does when the feeling is too big for the words, and it still "
    "hurts when it lands. Say 'no - that hurts' once, in the same words each time, put them "
    "down for a minute, then give them the words: 'you wanted that toy'.",
    "Nothing is wrong with them, or with you - hitting and biting are among the last things a "
    "small child drops. The same short reply every time is what teaches it: 'no, that hurts', a "
    "minute of no attention, then back to normal.",
    "It stings, and it is tiring, and it is the age rather than you: a small child has no other "
    "way to say the feeling yet. Catching it just before "
    "helps most - tired, hungry, or in a crowd - and one flat line when it lands, 'no - that "
    "hurts', with no big reaction to make it a game.",
)

A_REAL_DANGER = (
    r"\b(?:kill(?:ed|s|ing)?|murder\w*|knife|knives|gun|weapon|blade|strangl\w*|chok(?:e|ed|ing)|"
    r"throat|threaten\w*|scared|terrified|afraid|frightened|"
    r"drink(?:s|ing)?|drunk|beers?|pub|pints?|wine|whisky|vodka|flinch\w*|panic\w*|"
    r"walk(?:ing)?\s+on\s+eggshells|every\s+(?:single\s+)?day|nightly|"
    r"kill\s+my\s*self|suicide|the\s+police|"
    r"(?:won'?t|will\s+not|wouldn'?t|would\s+not|doesn'?t|does\s+not|never)\s+let(?:ting)?\s+me\s+"
    r"(?:leave|out|go|see))\b",
)

ADULT_HIT = (
    r"\b(?:my\s+)?(?:husband|wife|partner|boyfriend|girlfriend|ex|fiance|fiancee|dad|mum|mom|"
    r"father|mother|stepdad|stepmum|stepmom|carer|uncle|aunt)\b[^.?!]{0,30}"
    r"\b(?:hit|hits|slapp?(?:ed|s)?|punch(?:ed|es)?|kicked?|beat|beats|struck|push(?:ed|es|ing)?|"
    r"shov(?:ed|es|ing))\b",
)

PERSON_AS_ATTACKER = re.compile(
    r"\b(?:he|she|they|hubby|my\s+" + ABUSER + r")\b"
    r"(?:(?!\b(?:dog|dogs|puppy|puppies|cat|cats|kitten|kittens|pet|pets|horse|pony|rabbit|parrot|"
    r"hamster|gerbil|ferret|snake|lizard|bird|guinea\s+pig|bees?|wasps?|hornets?|midges?|gnats?|"
    r"mosquito(?:e)?s?|flies|insects?)\b)[^.?!]){0,30}"
    r"\b" + ABUSE_VERB + r"\s+me\b")

LOSS_SUBJECT = (
    r"\b(?:the\s+)?(?:death|dying|loss|losing|lost|passing|funeral|burial|cremation|news|"
    r"diagnosis|divorce|split|separation|breakup|break-up|illness|cancer)\s+of\s+"
    r"(?:my|our|the|his|her|their)\s+(?:\w+\s+)?\w+",
    r"\b(?:my|his|her|their|our)\s+\w+(?:'s|s')?\s+(?:death|dying|died|dead|departure|loss|"
    r"passing|funeral|diagnosis|illness|cancer)\b",
    r"\b(?:losing|lost|lose)\s+(?:my|our|the|his|her)\s+\w+",
    r"\b(?:the\s+(?:day|week|year|month|news|thought|idea|fact)\b[^.?!]{0,30}?"
    r"\b(?:died|dying|death|passed|gone|left\s+us)\b)",
    r"\b(?:my|our|his|her|their)\s+(?:\w+\s+)?\w+(?:'s|s')?\s+"
    r"(?:passed\s+(?:away|on)|left\s+(?:me|us)|walked\s+out|moved\s+out|went\s+away|"
    r"is\s+gone|has\s+gone|died|has\s+died)",
)

_PERSON = (r"(?:him|her|them|he|she|they|his|their|mum|mom|mam|mother|dad|father|stepdad|"
           r"stepfather|nan|nana|gran|granny|grandma|grandad|granddad|grandpa|son|daughter|"
           r"child|baby|brother|sister|wife|husband|hubby|partner|boyfriend|girlfriend|ex|"
           r"friend|mate|flatmate|housemate|roommate|neighbou?r|uncle|aunt|cousin|in-?laws?|"
           r"carer|staff|someone|somebody|anyone|anybody)")

_AWAY_TAIL = (
    r"on\s+(?:the\s+|a\s+|this\s+|my\s+)?(?:motorway|dual\s+carriageway|road|roads|stairs|"
    r"staircase|steps|ladder|ladders|bike|bicycle|motorbike|scooter|horse|roof|scaffolding|ice|"
    r"pavement|platform|escalator)\b"
    r"|up\s+(?:a\s+|the\s+|this\s+|my\s+)?(?:ladder|ladders|roof|scaffolding|stairs)\b"
    r"|in\s+(?:the\s+)?(?:dark|car|van|traffic|bus|train|tube|town|city|sea|crowd)\b"
    r"|at\s+(?:the\s+)?(?:gym|pool|beach|match|festival|club)\b"
    r"|(?:driving|walking|cycling|running|jogging|lifting|swimming|climbing|hiking|travelling|"
    r"commuting|shopping)\b"
    r"|around\s+(?:dogs?|animals?|strangers|men|crowds?|traffic)\b"
    r"|with\s+(?:this|my|the)\s+(?:knee|back|hip|shoulder|leg|ankle|arm|wrist|neck|heart|"
    r"health|balance|eyesight|grip)\b"
)

FLAMES = (
    r"\bflames?\b[^.?!]{0,25}\b(?:coming|pouring|shooting|bursting|licking|roaring|spreading|"
    r"spread|out\s+of|from|everywhere|on\s+the\s+(?:ceiling|wall|floor))\b",
    r"\b(?:coming|pouring|shooting|bursting|licking|roaring)\s+(?:out\s+of|out|from|up)\b"
    r"[^.?!]{0,25}\bflames?\b",
    r"\b(?:is|are|was|were|went|go|goes|going|it'?s)\s+(?:up\s+)?in\s+flames\b",
    r"\b(?:see|saw|can\s+see|i\s+can\s+see|there\s+are|there\s+is)\s+(?:\w+\s+){0,3}flames?\b",
    r"\bflames?\s+(?:everywhere|all\s+over|in\s+the\s+(?:room|kitchen|hall|house|flat))\b",
)

BURNT_FOOD = (
    r"\b(?:burnt|burned|scorched|charred)\s+(?:the\s+|my\s+|a\s+)?(?:toast|toastie|dinner|tea|"
    r"supper|lunch|bread|rice|pasta|chicken|meat|pie|pizza|beans|potatoes|chips|sauce|soup|cake|"
    r"biscuits?|muffins?|pastry|fish|veg|vegetables|garlic|onions?|bacon|sausages?|pancakes?|"
    r"porridge|toastie|crumpets?|pan|pot|wok|saucepan|cooker|food|roast|stew|curry|"
    r"casserole|lasagne|lasagna|toastie)\b",
    r"\b(?:the|my)\s+(?:toast|dinner|tea|bread|rice|chicken|meat|pie|pizza|sauce|soup|cake|"
    r"garlic|bacon|sausages?|porridge)\s+(?:is|was|has|'s|got)\s+(?:burnt|burned|charred|"
    r"scorched|smoking)\b",
    r"\bi\s+(?:burnt|burned|scorched|charred)\s+(?:it|them|something)\b",
    r"\b(?:let|left)\s+(?:the|my)\s+(?:toast|dinner|pan|sauce|rice|chicken|pizza|porridge)\b",
    r"\b(?:smoke|smoking|smoking\s+out)\s+(?:from|out\s+of)\s+(?:the|my)\s+(?:toast|"
    r"toaster|oven|cooker|grill|hob|pan)\b",
)

FIRE_OUT = (
    r"\b(?:on|caught)\s+fire\b",
    r"\bflames?\b",
    r"\b(?:alight|ablaze|out\s+of\s+control|spreading|spread)\b",
    r"\bevery[\s-]?where\b",
    r"\ball\s+over\b",
    r"\bcan'?t\s+see\b",
    r"\b(?:chip\s+pan|grease|deep\s+fat|fryer)\b[^.?!]{0,20}\b(?:fire|flames?|alight)\b",
)

FIRE_ELSEWHERE = (
    r"\b(?:on|caught)\s+fire\b",
    r"\bsmok\w*\b",
    r"\b(?:everywhere|spreading|spread|alight|ablaze|out\s+of\s+control)\b",
    r"\b(?:ceiling|walls?|curtains?|sofa|settee|couch|mattress)\b",
    r"\b(?:alarm|trapped|can'?t\s+get\s+out|cannot\s+get\s+out)\b",
    r"\b(?:house|flat|kitchen|room|living\s+room|hall|hallway|landing|building|car|garage|"
    r"shed|chimney)\b[^.?!]{0,15}\b(?:fire|burning|flames?)\b",
)

GARMENT = (r"\b(?:coat|jacket|shirt|t-?shirt|jumper|sweater|hoodie|cardigan|fleece|top|dress|"
           r"skirt|trousers|pants|jeans|pyjamas?|pj'?s|dressing\s+gown|gown|robe|scarf|apron|"
           r"overalls?|sleeve|sleeves|tie|clothes|hair|trouser\s+leg|gloves?|mittens?|socks?|"
           r"shorts|leggings|vest|sleepsuit|onesie|babygro|baby\s*gro|romper|nappy|nightie|"
           r"nightdress|dungarees|blouse|waistcoat|anorak|raincoat|mac|frock)\b")

PAN_FIRE = (
    r"\b(?:chip\s*pan|chip\s*pot|frying\s+pan|pan|wok|deep\s*fat|fryer)\b"
    r"[^.?!]{0,20}\b(?:is\s+|was\s+|'s\s+)?(?:on\s+fire|alight|ablaze|caught\s+fire)\b",
    r"\b(?:oil|fat|grease)\b[^.?!]{0,25}\b(?:pan|wok|fryer)\b[^.?!]{0,15}"
    r"\b(?:on\s+fire|alight|caught\s+fire)\b",
    r"\b(?:pan|wok|fryer)\b[^.?!]{0,20}\b(?:oil|fat|grease)\b[^.?!]{0,15}"
    r"\b(?:on\s+fire|alight|caught\s+fire)\b",
    r"\b(?:chip\s*pan|chip\s*pot|frying\s+pan|pan|wok|deep\s*fat|fryer)\b[^.?!]{0,20}"
    r"\b(?:caught|catches|took|takes|went\s+up\s+in)\s+(?:the\s+|a\s+)?flames?\b",
    r"\b(?:chip\s*pan|chip\s*pot|frying\s+pan|pan|wok|deep\s*fat|fryer)\b[^.?!]{0,10}"
    r"\b(?:is|was|were|are)\s+(?:in\s+flames|blazing)\b",
)

VEHICLE_FIRE = (
    r"\b(?:my|our|the)\s+(?:car|van|motorbike|moped|scooter|lorry|truck|caravan|camper|"
    r"engine|bonnet|dashboard)\b[^.?!]{0,30}\b(?:is\s+|'?s\s+|are\s+|was\s+|were\s+)?"
    r"(?:on\s+fire|caught\s+fire|alight|ablaze|in\s+flames)\b",
    r"\b(?:bonnet|dashboard)\b[^.?!]{0,20}\b(?:is\s+|'?s\s+|was\s+)?burning\b",
    r"\b(?:smoke|flames?)\b[^.?!]{0,25}\b(?:out\s+of|from(?:\s+under)?|under)\s+"
    r"(?:the\s+|my\s+|our\s+)?(?:bonnet|engine\s+bay|engine|dashboard|car|van)\b",
    r"\b(?:bonnet|engine\s+bay)\b[^.?!]{0,20}\bsmok\w*\b",
    r"\b(?:smok\w*|flames?)\b[^.?!]{0,15}\b(?:in|into|inside|filling|through)\s+"
    r"(?:the\s+|my\s+|our\s+)?(?:car|van|camper|caravan|cabin)\b",
    r"\b(?:cabin|car|van)\b[^.?!]{0,15}\bfull\s+of\s+smoke\b",
    r"\bexhaust\b[^.?!]{0,30}\b(?:flames?|fire|alight|ablaze)\b",
    r"\b(?:flames?|fire)\b[^.?!]{0,30}\bexhaust\b",
    r"\bthe\s+exhaust\b[^.?!]{0,10}\bis\s+burning\b",
    r"\bsmell\w*\s+(?:of\s+)?burning\b[^.?!]{0,25}\b(?:bonnet|engine(?:\s+(?:bay|"
    r"compartment))?|dashboard)\b",
    r"\b(?:bonnet|engine\s+bay|dashboard)\b[^.?!]{0,20}\bsmell\w*\b[^.?!]{0,10}\bburn\w*\b",
    r"\b(?:my|our|the)\s+(?:car|van|motorbike|moped|scooter|lorry|truck|caravan|camper)\b"
    r"(?![^.?!]{0,25}\b(?:oil|fuel|petrol|diesel)\b)[^.?!]{0,20}\bburning\b",
    r"(?=.*\bburn\w*\b)(?=.*\bsmok\w*\b)"
    r"(?=.*\b(?:engine|bonnet|dashboard|car|van|exhaust)\b)"
    r"(?!.*\b(?:oil|fuel|petrol|diesel|calories)\b)",
)

VEHICLE_EXHAUST = (
    r"\b(?:smok\w*|steam|fumes?)\b[^.?!]{0,25}\b(?:from|out\s+of|out\s+the)\s+"
    r"(?:the\s+|my\s+|our\s+)?exhaust\b",
    r"\bexhaust\b[^.?!]{0,25}\b(?:smok\w*|fumes?)\b",
    r"\b(?:burning|using|losing)\s+(?:a\s+bit\s+of\s+|some\s+)?(?:oil|fuel)\b[^.?!]{0,25}"
    r"\b(?:smoking|smoky|smokes)\b",
)

VEHICLE_BURNING_SMELL = (
    r"\b(?:smell\w*|smells?|smelling|stink\w*|odou?r)\b[^.?!]{0,12}"
    r"\b(?:of|like|off)\s+(?:a\s+)?burn\w*\b",
    r"\bburn\w*\s+(?:smell|odou?r|stink)\b",
    r"\b(?:a\s+)?burning\s+(?:smell|odou?r)\b",
    r"\bsmoke\s+smell\b",
    r"\b(?:smell\w*|stink\w*|odou?r)\b[^.?!]{0,12}\b(?:of|like|off)\s+smoke\b",
    r"\b(?:smoky|smokey)\s+smell\b",
)

VEHICLE_BURNING_SMELL_HARD = (
    r"\b(?:on\s+fire|caught\s+fire|alight|ablaze|in\s+flames|flames?|bonnet|"
    r"engine\s+bay|dashboard|inside\s+the\s+car|coming\s+into\s+the\s+car)\b",
    r"\bthere\s+(?:is|was|were|are)\s+(?:a\s+lot\s+of\s+|loads\s+of\s+|thick\s+)?smoke\b",
    r"\bsmoke\s+(?:coming|pouring|billowing|filling|everywhere|belching|pumping)\b",
    r"\bfull\s+of\s+smoke\b",
)

VEHICLE_FIRE_OVER = (
    r"(?=.*\b(?:there\s+was|there\s+were|smoke\s+came|i\s+saw|i\s+smelt|i\s+smelled|"
    r"it\s+was|we\s+had|caught\s+fire|had\s+a\s+(?:small\s+)?fire)\b)"
    r"(?=.*\b(?:fixed|put\s+(?:it\s+)?out|sorted|fine\s+now|ok\s+now|seems?\s+"
    r"(?:fine|ok|alright|to\s+be\s+(?:fine|ok))|all\s+(?:fine|ok)|no\s+(?:damage|problem|"
    r"harm))\b)",
)

NEAR_FIRE = (
    r"\b(?:nearly|almost|close\s+to|about\s+to)\b[^.?!]{0,40}\b(?:fire|fires|flames?|alight|"
    r"ablaze|blazing|burning|burn|burnt|burned|catch|caught|catchin(?:g)?|smoke|smoking|"
    r"smouldering|smoldering|torched?|caught\s+light|took\s+light|went\s+up)\b",
)

FIRE_DRILL = (
    r"\bfire\s+drill\b",
    r"\bfalse\s+alarm\b",
)

NEAR_THING_OVER = (
    r"\b(?:it|he|she|they)\s+(?:was|were|is|came|come|did|didn'?t|wouldn'?t|never|just)\b"
    r"[^.?!]{0,26}\b(?:van|car|lorry|truck|bus|taxi|cab|bike|bicycle|driver|fella|man|woman|"
    r"bloke|idiot|speed\w*|fast|close|corner|junction|lights|crossing|pavement|road|kerb)\b",
    r"\b(?:they|he|she|it)\s+(?:didn'?t|did\s+not|never)\s+(?:stop|stop\w*|slow|slow\w*|look|"
    r"even\s+(?:stop\w*|slow\w*|look))\b",
    r"\bi\s+(?:had|needed)\s+to\s+(?:jump|run|dive|leap|step|swerve|pull|shout|grab|yank|"
    r"scramble)\b",
    r"\b(?:jumped|dived|leapt|leaped|ran|scrambled|swerved)\s+(?:back|out\s+of\s+the\s+way)\b",
    r"\b(?:came|come|coming|appeared)\s+out\s+of\s+nowhere\b",
    r"\b(?:shook\s+me\s+up|really\s+shook\s+me|shaken\s+up|hands?\s+(?:are|were)\s+shaking|"
    r"still\s+shaking|heart\s+was\s+racing)\b",
    r"\bno\s+(?:it|they|he|she)\s+(?:didn'?t|did\s+not)\b",
    r"\b(?:nearly|almost)\s+(?:had|hit|got)\s+me\b",
)

NEAR_FIRE_OVER = (
    r"\b(?:didnt|didn'?t|never|did\s+not)\s+(?:catch|caught|go\s+up|went\s+up|take|light|"
    r"ignite|spread)\b",
    r"\b(?:caught|got|put)\s+it\s+(?:in\s+time|before|quick|early|out)\b",
    r"\bno\s+(?:real\s+)?(?:damage|harm|fire)\b",
    r"\bit\s+(?:was|is)\s+(?:fine|nothing|ok|alright|just\s+smoke|only\s+smoke)\b",
)

FIRE = (
    r"\b(?:house|flat|apartment|kitchen|home|building|shed|garage|car|roof|roofs?|attic|loft|"
    r"chimney|chimney\s*pot|porch|balcony|fence|hedge|caravan|motorhome|camper|tent|bungalow|"
    r"cottage|semi|hall|hallway|landing|stairs?|stairwell|stairway|outhouse|lean-to|"
    r"bedroom|bedrooms?|bathroom|bath\s*room|bathrooms?|living\s*room|living\s*rooms?|"
    r"sitting\s*room|front\s*room|back\s*room|dining\s*room|spare\s*room|utility\s*room|"
    r"bed\s*room|lounge|study|conservatory|extension|cellar|basement|room|rooms|"
    r"ceiling|ceilings|wall|walls|floor|floors|floorboards?|skirting|door|doors|window|"
    r"windows|window\s*frame|banister|carpet|rug|wardrobe|cupboard|bed)\s+"
    r"(?:is\s+|'s\s+|are\s+)?(?:on\s+fire|burning|going\s+up|alight|ablaze)\b",
    r"\b(?:roof|attic|loft|chimney|chimney\s*pot|porch|balcony|fence|hedge|caravan|motorhome|"
    r"camper|tent|outhouse|shed|garage)\b[^.?!]{0,20}\bcaught\s+(?:on\s+)?fire\b",
    r"\bthere'?s\s+a\s+fire\b", r"\bfire\s+in\s+(?:the|my|our)\s+(?:house|flat|kitchen|building|room|garage|car)\b",
    r"\bsmoke\s+(?:is\s+)?(?:pouring|billowing|filling|coming\s+(?:from|out))\b",
    r"\b(?:can't|cannot|can\s+not)\s+get\s+out\b.{0,40}\b(?:smoke|fire|flames?|burning|alarm|trapped)\b",
    r"\b(?:trapped|blocked\s+in|locked\s+in)\b.{0,30}\b(?:can't|cannot)\s+get\s+out\b",
    r"\b(?:can't|cannot)\s+breathe\b.{0,20}\bsmoke\b",
    r"(?<!\bi )(?<!\bI )(?<!\bhe )(?<!\bshe )(?<!\bwe )(?<!\bthey )"
    r"\bsmoke\s+(?:everywhere|in\s+(?:the|my)\s+(?:house|flat|room|kitchen))\b",
    r"\b(?:my|the)\s+(?:house|kitchen|flat)\s+(?:is\s+)?burning\b",
    r"\bfire\s+(?:has\s+)?(?:started|spread)\b",
    r"\b(?:smoke|fire)\s+alarm\b.{0,30}\b(?:going\s+off|sounding|blaring|wailing)\b",
    r"(?<!\bi )(?<!\bI )(?<!\bhe )(?<!\bshe )(?<!\bwe )(?<!\bthey )"
    r"\bsmoke\s+(?:in|coming\s+into|filling|pouring\s+into)\s+(?:the|my|our)\b",
    r"\b(?:chip\s+pan|pan|toaster|oven|grill|curtains?|sofa|cushion|bin|"
    r"mattress|socket|plug|car|fridge|washing\s+machine|tumble\s*dryer|dryer|dishwasher|"
    r"microwave|kettle|freezer|hoover|vacuum)\b.{0,25}\b(?:caught|on)\s+fire\b",
    r"\bflames?\s+(?:in|on|inside|from|coming\s+out\s+of|out\s+of)\s+(?:the|my|our)\s+"
    r"(?:bin|bins|sofa|settee|couch|chair|car|curtains?|cushion|bed|mattress|wardrobe|cupboard|"
    r"shed|garage|oven|microwave|kettle|pan|toaster|socket|plug|wires?|lamp|lights?|tv|telly|"
    r"television|banister|rug|carpet|door)\b",
    r"\bthere'?s\s+smoke\b",
    r"\bsmoke\b[^.?!]{0,30}\b(?:filling|filled)\s+(?:up\s+)?(?:the|my|our)\s+(?:house|flat|"
    r"kitchen|room|living\s+room|bedroom|hall|hallway|landing|building|car|garage|shed)\b",
    r"\b(?:the|my|our)\s+(?:house|flat|kitchen|room|living\s+room|bedroom|hall|hallway|"
    r"landing|building|car|garage|shed)\b[^.?!]{0,15}\b(?:filling\s+(?:up\s+)?with\s+smoke|"
    r"full\s+of\s+smoke)\b",
    r"\bsmoke\s+(?:is\s+|was\s+)?(?:coming|pouring|seeping|drifting|billowing)\s+(?:under|through|"
    r"round|around)\s+(?:the|a|my|our)\s+(?:door|doors|floor\s?boards?|floor|ceiling|wall|walls)\b",
    r"(?<!\bi )(?<!\bI )(?<!\bhe )(?<!\bshe )(?<!\bwe )(?<!\bthey )"
    r"\bsmoke\s+(?:on|in)\s+(?:the|my|our)\s+(?:stairs|stairwell|landing|hall|hallway|corridor)\b",
) + FLAMES

_SMOKE_THING = (r"(?:oven|hob|grill|toaster|kettle|microwave|air\s?fryer|washing\s+machine|"
               r"washer|tumble\s+dryer|dryer|dishwasher|fridge|freezer|hoover|vacuum|"
               r"laptop|computer|phone|mobile|charger|plug|socket|tv|telly|television|iron|"
               r"hair\s?dryer|printer|boiler|radiator|heater|extractor|fuse\s?box)")

APPLIANCE_SMOKE = (
    r"\b" + _SMOKE_THING + r"\b[^.?!]{0,25}\bsmok\w*",
    r"\bsmok\w*\s+(?:is\s+)?(?:coming|pouring|billowing|rising|streaming)\s+(?:out\s+)?"
    r"(?:of|from)\s+(?:the|my|our|your)?\s*(?:\w+\s+){0,3}" + _SMOKE_THING,
    r"\bsmoke\s+(?:out\s+)?(?:of|from)\s+(?:the|my|our|your)?\s*(?:\w+\s+){0,3}"
    + _SMOKE_THING,
)

FIRE_SCALE = (
    r"\b(?:flames?|alight|ablaze|caught\s+fire|on\s+fire|set\s+alight)\b",
    r"\bsmoke\s+(?:everywhere|filling|pouring\s+into|coming\s+into|billowing)\b",
    r"\bsmoke\s+(?:is\s+|was\s+)?(?:pouring|billowing|belching|roaring)\b",
    r"\b(?:kitchen|room|living\s+room|hall|hallway|house|flat|landing|stairs|stairwell|"
    r"bedroom)\b[^.?!]{0,15}\bfilling\s+(?:up\s+)?with\s+smoke\b",
    r"\bsmoke\s+(?:in|on)\s+(?:the|my|our)\s+(?:hall|hallway|stairs|stairwell|landing|"
    r"bedroom|room|house|flat|kitchen|toilet|bathroom)\b",
    r"\b(?:whole|entire)\s+(?:house|flat|kitchen|room|building)\b",
    r"\b(?:can'?t|cannot)\s+get\s+out\b",
    r"\b(?:spread\w*|took\s+hold|getting\s+(?:bigger|worse))\b",
    r"\b(?:smoke|fire)\s+alarm\b[^.?!]{0,30}\b(?:going\s+off|sounding|blaring)"
    r"[^.?!]{0,40}\bsmoke\b",
)

ALARM_NUISANCE = (
    r"\b(?:smoke|fire)\s+(?:alarm|detector)\b[^.?!]{0,40}\b(?:goes\s+off|going\s+off|"
    r"sounds|sounding|beeps|beeping|chirp\w*|wails?|keeps\s+going\s+off|wont\s+stop|"
    r"won'?t\s+stop|stop\s+it)\b[^.?!]{0,40}\b(?:when|cooking|toast|toasting|grill|"
    r"grilling|oven|hob|fry|frying|roast|roasting|bake|baking|shower|steam|kitchen|"
    r"cooker)\b",
)

_SMELLY_THING = (
    r"coat|jacket|clothes|clothing|jumper|shirt|top|dress|trousers|jeans|skirt|hoodie|fleece|"
    r"cardigan|suit|uniform|hat|scarf|gloves|shoes|trainers|bag|rucksack|hair|curtains?|"
    r"cushions?|sofa|settee|couch|mattress|bedding|duvet|pillow|blanket|rug|carpet|car|van|"
    r"tent|sleeping\s+bag|washing|laundry|sheets?"
)

SMOKE_IS_A_SMELL = (
    r"\b(?:smell|smells|smelly|stinks?|stinking|reek\w*|whiff|odour|odor)\b[^.?!]{0,40}"
    r"\bsmoke\b",
    r"\bsmoke\s+(?:smell|stain\w*)\b",
    r"\b(?:get|getting|got|remove|removing|clear|take|taking)\b[^.?!]{0,30}\bsmoke\b"
    r"[^.?!]{0,20}\b(?:out|off)\b",
    r"\bsmoke\s+out\s+of\b",
)

BATTERY_FIRE = (
    r"\b(?:phone|laptop|tablet|ipad|battery|batteries|power\s?bank|e-?bike|e-?scooter|"
    r"hoverboard|charger|drone)\b[^.?!]{0,20}\b(?:is\s+|'s\s+|are\s+)?(?:on\s+fire|"
    r"caught\s+fire|smoking|sparking|melting|burning(?!\s+(?:up|hot|my|his|her|their|a|the))|burnt)\b",
    r"\b(?:battery|batteries)\s+(?:is\s+|are\s+)?(?:on\s+fire|caught\s+fire|smoking|"
    r"burning(?!\s+(?:up|hot|my|his|her|their|a|the)))\b",
)

DEVICE_BURNING = (
    r"\b(?:phone|laptop|tablet|ipad|battery|batteries|power\s?bank|e-?bike|e-?scooter|"
    r"hoverboard|charger|drone)\b[^.?!]{0,30}\b(?:flames?|alight|ablaze|burning|burnt|"
    r"caught\s+fire|on\s+fire)\b",
    r"\bflames?\b[^.?!]{0,25}\b(?:out\s+of|from)\b[^.?!]{0,10}\b(?:phone|laptop|tablet|"
    r"ipad|battery|power\s?bank|charger)\b",
)

MEDICINE = (
    r"(?:calpol|nurofen|benylin|infant\s+paracetamol|children'?s\s+(?:paracetamol|ibuprofen)|"
    r"junior\s+ibuprofen|cough\s+(?:medicine|syrup)|cold\s+medicine|antibiotics?|pills|tablets|"
    r"medicine|medicines|meds|paracetamol|ibuprofen|painkillers|antidepressants|insulin|"
    r"eye\s+drops|vitamins?|iron\s+tablets|sleeping\s+pills)"
)

DOSE_AMOUNT = (
    r"\b(?:too\s+many|too\s+much|double|twice|extra)\s+"
    r"(?:doses?|spoonfuls?|mouthfuls?|syringes?)\b"
    r"|\b(?:twice|double|three\s+times)\s+(?:the|her|his|their|your)\s+dose\b"
    r"|\b(?:two|three|four|several)\s+(?:doses?|spoonfuls?)\b[^.?!]{0,15}\b"
    r"(?:at\s+once|together|at\s+the\s+same\s+time|in\s+(?:an|one|1|a\s+single)\s+hour|"
    r"within\s+an\s+hour|in\s+\d+\s+minutes|back\s+to\s+back)\b"
)

DOSE_COURSE = (
    r"\b(?:doses?|spoonfuls?|syringes?)\b[^.?!]{0,20}\b(?:apart|(?:\d+|two|three|four|five|six|"
    r"several)\s+hours?\s+(?:apart|later|between|gap)|every\s+(?:\d+|two|three|four|six)\s+"
    r"hours?)\b",
    r"\bevery\s+(?:\d+|two|three|four|six)\s+hours?\b[^.?!]{0,20}\b(?:doses?|spoonfuls?)\b",
    r"\b(?:two|three|four|five|six)\s+(?:doses?|spoonfuls?)\b[^.?!]{0,20}\b(?:today|"
    r"so\s+far|since\s+(?:this\s+morning|last\s+night|yesterday)|this\s+(?:morning|afternoon|"
    r"evening|week)|in\s+24\s+hours|over\s+the\s+day)\b",
)

DOSE_COURSE_KEEP = (
    r"\btoo\s+many\b", r"\boverdos\w*", r"\bhandful\b",
    r"\bwhole\s+(?:packet|pack|box|bottle)\b",
    r"\ball\s+(?:of\s+)?(?:my|his|her|their)\b",
    r"\b(?:sleepy|drowsy|floppy|limp|unrousable|hard\s+to\s+wake|wont\s+wake)\b",
    r"\bvomit\w*", r"\bbeing\s+sick\b", r"\bthrowing\s+up\b", r"\bnot\s+himself\b",
    r"\bnot\s+herself\b",
)

DOSE_ASKED = (
    r"\b(?:can|could|should|shall|may|might)\s+(?:i|we)\s+(?:give|dose|add|top\s+up|double)\b",
    r"\bis\s+it\s+(?:ok|okay|alright|safe|fine)\s+to\s+(?:give|dose|add|top\s+up)\b",
    r"\bwould\s+(?:it|that)\s+be\s+(?:ok|okay|alright|safe|fine)\b",
    r"\bis\s+(?:it|that|this)\s+too\s+(?:many|much)\b",
    r"\bis\s+(?:it|that|this)\s+(?:ok|okay|alright|fine)\s+(?:for|to\s+give)\b",
    r"\bhow\s+(?:many|much)\b[^.?!]{0,20}\b(?:doses?|calpol|nurofen|paracetamol|ibuprofen)\b",
)

OVERDOSE_OF_A_TREAT = (
    r"\boverdos(?:e|ed|ing)\s+(?:on\s+)?(?:(?:the|a|an|my|his|her|their)\s+)?"
    r"(?:coffee|caffeine|tea|chocolate|cake|"
    r"sugar|sweets|crisps|biscuits|cheese|ice\s+cream|tv|telly|netflix|box\s+sets?|sleep|"
    r"sun|sunshine|shopping|gossip|christmas\s+music)\b",
    r"\ban\s+overdose\s+of\s+(?:coffee|caffeine|tea|chocolate|cake|sugar|sweets|crisps|"
    r"biscuits|cheese|ice\s+cream|tv|telly|netflix|box\s+sets?|sleep|sun|sunshine|shopping|"
    r"gossip|work|meetings?|emails?|paperwork|spreadsheets?|christmas\s+music)\b",
)

MILD_SWALLOWED = (
    r"(?![^?]{0,70}\b(?:child|kid|kids|son|daughter|baby|babies|toddler|boy|girl|grandson|"
    r"granddaughter|niece|nephew)\b)"
    r"(?![^?]{0,70}\b(?:bottle|bottles|whole|tube|tubes|packet|litre|litres|pint|glass\s+full)\b)"
    r"\b(?:i|ive|i've|im|i'm)\b[^.?!]{0,20}"
    r"\b(?:swallowed|swallow|drank|drunk|drinking|licked|sucked|got|took|sipped|swigged|necked|"
    r"glugged)\b[^.?!]{0,15}"
    r"\b(?:a\s+bit|a\s+little|a\s+small\s+amount|a\s+mouthful|a\s+sip|one\s+sip|one\s+mouthful|"
    r"a\s+taste|a\s+drop|a\s+dab|a\s+smear|a\s+swig|some)\b[^.?!]{0,25}"
    r"\b(?:mouthwash|mouth\s+wash|toothpaste|shampoo|conditioner|shower\s+gel|soap|body\s+lotion|"
    r"hand\s+cream|sun\s?cream|moisturiser|moisturizer|bubble\s+bath|hand\s+soap|bath\s+soap)\b",
    r"\b(?:mouthwash|mouth\s+wash|toothpaste|shampoo|shower\s+gel)\b[^.?!]{0,15}"
    r"\b(?:got|went|sprayed|squirted)\b[^.?!]{0,10}\b(?:in|into)\s+my\s+mouth\b",
)

SOME_OF_IT = (
    r"(?:some\s+(?:of\s+the\s+)?|a\s+little\s+(?:bit\s+)?(?:of\s+)?|little\s+(?:of\s+)?|"
    r"a\s+(?:bit|drop|splash|swig|mouthful|sip|handful|piece|lick|spoonful|tablespoon|"
    r"teaspoon|glass|cup|swallow|bottle|tube|packet|can|carton|jar)\s+(?:of\s+)?|"
    r"a\s+small\s+amount\s+(?:of\s+)?|half\s+a\s+(?:glass|cup|bottle)\s+(?:of\s+)?|"
    r"(?:the|my|his|her|their|our|these|those)\s+)?"
)

MILD_PRODUCT_SMALL = (
    r"\b(?:toothpaste|shampoo|conditioner|shower\s+gel|soap|"
    r"body\s+lotion|hand\s+cream|sun\s?cream|moisturiser|moisturizer|bubble\s+bath)\b",
)

TOOK_OUT_OF = (
    r"\b(?:took|taken|taking|take|got|get|getting|fetched|fetch)\b[^.?!]{0,25}"
    r"\b(?:out\s+of|from|off|down\s+from|out\s+the)\s+(?:the\s+|a\s+|my\s+|his\s+|her\s+)?"
    r"(?:car|cupboard|garage|shed|bathroom|kitchen|boot|cabinet|box|bag|shelf|drawer|bottle|tin|"
    r"jar|bucket|machine|van|garden|work|locker|store|closet|cupboards|shelves)\b",
)

SWALLOWED_ORDINARY = (
    r"\b(?:child|kid|kids|son|daughter|baby|babies|toddler|boy|girl|he|she|they|grandson|"
    r"granddaughter|niece|nephew|"
    r"my\s+(?:son|daughter|child|kid|baby|toddler|boy|girl|grandson|granddaughter|niece|nephew|"
    r"husband|wife|partner|friend|mum|mom|dad|nan|gran))\b[^.?!]{0,25}"
    r"\b(?:swallowed|swallowing|ate|eaten|eating|drank|drunk)\b"
    r"[^.?!]{0,20}\b(?:wax\s+crayons?|crayons?|chalk(?!\s*paint)|toothpaste|bars?\s+of\s+soap|soap|"
    r"play\s?dough|(?:blu|blue)\s?tack?)\b",
)

GAS_SMELL = (
    r"\b(?:smell|smells|smelling|smelled|smelt|whiff)\s+(?:of\s+|like\s+)?(?:a\s+)?(?:gas|gas\s+leak)\b",
    r"\b(?:can|could)\s+(?:i|you|we|she|he|they)\s+smell\s+gas\b",
    r"\bi\s+(?:can\s+)?smell\s+gas\b",
    r"\b(?:strong|funny|odd|strange|faint)\s+(?:smell|whiff)\s+of\s+gas\b",
    r"\b(?:gas|leak)\s+smell\b",
    r"\bgas\s+(?:leak|leaking|leaked)\b",
    r"\bleak(?:ing|s|ed)?\s+(?:out\s+)?(?:\w+\s+)?gas\b",
    r"\bgas\s+(?:is\s+)?(?:leaking|escaping|coming\s+(?:out|from)|seeping)\b",
    r"\b(?:smell\w*|whiff\w*)\b[^.?!]{0,30}\bgas\b",
    r"\bgas\b[^.?!]{0,20}\b(?:smell|stink|reek)\w*\b",
    r"\b(?:boiler|cooker|hob|heater|oven|fire|gas\s+fire)\b.{0,30}\bsmell\w*\b.{0,30}"
    r"\b(?:gas|fumes?|rotten|sulphur|sulfur|eggs?|headach\w*|dizzy|nauseous)\b",
    r"\bsmell\w*\s+(?:of\s+|like\s+)?(?:rotten\s+eggs?|sulphur|sulfur)\b.{0,30}"
    r"\b(?:boiler|cooker|hob|heater|gas)\b",
)

BLEACH_MIX = (
    r"\A(?=.*\bbleach\w*\b)(?=.*\b(?:vinegar|ammonia|acid|acidic|toilet\s+cleaner|"
    r"cistern\s+cleaner|descaler|de\s?scaler|limescale|drain\s+unblocker|oven\s+cleaner|"
    r"another\s+cleaner|two\s+cleaners|other\s+cleaner|bleach\s+tablets?)\b)"
    r"(?!.*\b(?:separately|separate|different\s+days?|not\s+together|never\s+mix|washed\s+it|"
    r"rinsed\s+it|in\s+another\s+room|one\s+after\s+the\s+other)\b).*",
    r"\A(?!.*\b(?:tap|taps|water|waters|pool|swimming|drinking|shower|kettle|cold\s+water)\b)"
    r".*?\b(?:smell|smells|smelling|smelt|whiff|reek\w*)\b[^.?!]{0,25}\bchlorine\b",
    r"\bchlorine\s+(?:gas|fumes?)\b",
    r"\bbreathed\s+in\b[^.?!]{0,25}\b(?:bleach|chlorine|cleaner|cleaning\s+fumes?)\b",
)

BLEACH_MIX_Q = (
    r"\b(?:can|could|should|may)\s+(?:i|we|you)\s+(?:mix|put|add|use)\b[^.?!]{0,30}\bbleach\b"
    r"(?=[^.?!]{0,30}\b(?:vinegar|ammonia|acid|acidic|toilet\s+cleaner|descaler|limescale)\b)",
    r"\b(?:is\s+it\s+(?:ok|okay|safe|fine)|would\s+it\s+(?:be\s+)?(?:ok|okay|safe|fine))\b"
    r"[^.?!]{0,30}\b(?:mix|with)\b[^.?!]{0,20}\bbleach\b",
    r"\bwhat\s+happens\s+(?:if|when)\s+(?:i|we|you)\s+mix\b[^.?!]{0,30}\bbleach\b",
    r"\bbleach\b[^.?!]{0,20}\b(?:and|with)\b[^.?!]{0,15}\b(?:vinegar|ammonia|toilet\s+cleaner|"
    r"acid)\b[^.?!]{0,20}\b(?:together|at\s+the\s+same\s+time|ok|okay|safe|fine)\b",
)

CO_GOING_OFF = (
    r"\b(?:carbon\s+monoxide|co)\s+(?:alarm|detector|monitor)s?\b.{0,30}"
    r"\b(?:beep\w*|chirp\w*|going\s+off|going\s+beep|went\s+off|gone\s+off|sounding|sounds|"
    r"sounded|wailing|ringing)\b",
    r"\b(?:beep\w*|chirp\w*|going\s+off|went\s+off|gone\s+off|sounding|sounds|sounded|wailing|"
    r"ringing)\b.{0,40}\b(?:carbon\s+monoxide|co)\s+(?:alarm|detector|monitor)s?\b",
)

ELECTRIC_BURN = (
    r"\b(?:phone|mobile|charger|charging\s+brick|laptop|tablet|ipad|battery|batteries|"
    r"power\s?bank|adapter|adaptor|plug|socket|extension\s+lead|lead|cable|wire|wiring|"
    r"fuse\s?box|vape|e-?cig\w*|hoverboard|scooter|drill|toothbrush|headphones?|earbuds?|"
    r"console|charger\s+port|charging\s+port)\b[^.?!]{0,45}"
    r"\b(?:smell\w*|smelling|smoke|smoking|smoked|smoulder\w*|melt(?:ing|ed|s)?|spark(?:ing|s|ed)?|"
    r"scorch\w*|charred|caught\s+fire|catch(?:es|ing)?\s+fire|on\s+fire|flames?|bulging|"
    r"bulged|puffed\s+up|swollen)\b",
    r"\b(?:smell\w*|smelling)\s+(?:of\s+|like\s+)?(?:burning|melting|plastic|acrid)\b[^.?!]{0,40}"
    r"\b(?:phone|charger|plug|socket|lead|cable|wire|wiring|battery|laptop|tablet|adapter|adaptor|"
    r"power\s?bank)\b",
    r"\b(?:plug|socket|extension\s+lead|adapter|adaptor|charger)\b.{0,30}"
    r"\b(?:is|are|'s|'re|was|were)\s+(?:melting|melted|scorched|charred|blackened|buzzing|"
    r"sparking)\b",
    r"\bbatter(?:y|ies)\b.{0,20}\b(?:bulging|bulged|swollen|puffed\s+up|hot\s+to\s+touch)\b",
)

BATTERY_BULGE = (
    r"\b(?:phone|mobile|laptop|tablet|ipad|battery|batteries|power\s?bank|vape|e-?cig\w*|"
    r"hoverboard|scooter|drone|toothbrush|headphones?|earbuds?|watch)\b[^.?!]{0,25}"
    r"\b(?:bulg(?:ing|ed|es)|swollen|swelling|puffed\s+up|puffing\s+up)\b",
    r"\b(?:bulg(?:ing|ed|es)|swollen|puffed\s+up)\b[^.?!]{0,15}\b(?:battery|batteries)\b",
)

ELECTRIC_FINE = (
    r"\b(?:gets?|getting|is|are)\s+(?:quite\s+|really\s+|a\s+bit\s+|very\s+)?(?:warm|hot)\b"
    r"(?!.{0,20}\b(?:smell\w*|smoke|smoking|melt\w*|spark\w*|bulging|swollen)\b)",
    r"\b(?:frayed|worn|broken|cracked|tangled)\s+(?:lead|cable|wire)\b"
    r"(?!.{0,25}\b(?:smell\w*|smoke|smoking|melt\w*|spark\w*)\b)",
    r"\b(?:battery|charge)\s+(?:life|lasts?|lasted|drains?|dropping|dies|died|percentage)\b",
    r"\bhow\s+(?:do|can|should)\s+(?:i|we|you)\s+(?:stop|keep|make|get)\b.{0,30}"
    r"\b(?:phone|battery|charger|laptop)\b.{0,20}\b(?:cool|cooler|warm|hot|charged\s+up)\b",
    r"\b(?:recycle|recycling|dispose|disposal|take|bin)\b.{0,30}\b(?:battery|batteries|phone)\b",
)

FORAGED_EATEN = (
    r"\b(?:swallowed|swallowing|drank|drunk|eaten|ate|eating|licked|sucked|chewed|nibbled|"
    r"tasted|bit\s+into|put\s+(?:it\s+)?in\s+(?:his|her|their|my)\s+mouth)\b[^.?!]{0,30}"
    r"\b(?:wild\s+mushrooms?|toadstools?|puffballs?|liberty\s+caps?|magic\s+mushrooms?|"
    r"foraged|foraging|fungus|fungi)\b",
    r"\b(?:swallowed|swallowing|eaten|ate|eating|licked|sucked|chewed|nibbled|tasted|"
    r"bit\s+into)\b[^.?!]{0,30}\b(?:berries|berry|leaf|leaves|plants?|seeds?|nuts?)\b"
    r"[^.?!]{0,25}\b(?:from|off|in|out\s+of)\s+(?:the\s+|a\s+|our\s+|my\s+)?(?:garden|hedge|"
    r"bush|bushes|tree|field|woods?|woodland|park|wall|plants?|border|allotment|lane|path|verge)\b",
    r"\b(?:my|our)\s+(?:son|daughter|child|kid|baby|toddler)\b[^.?!]{0,25}\b(?:ate|eaten|eating|"
    r"swallowed|nibbled|chewed|sucked)\b[^.?!]{0,25}\b(?:flowers?|plants?|leaf|leaves|berries|"
    r"berry|seeds?)\b[^.?!]{0,25}\b(?:from|off|in|outside)\s+(?:the\s+|a\s+)?(?:garden|hedge|"
    r"bush|park|woods?|field|ground|outside|path|allotment)\b",
    r"\b(?:picked|found|gathered|brought\s+home|brought\s+me|handed\s+me)\b[^.?!]{0,25}"
    r"\b(?:mushrooms?|toadstools?|berries|berry)\b[^.?!]{0,20}\b(?:and|then)\b[^.?!]{0,15}"
    r"\b(?:ate|eaten|eating|swallowed|nibbled|chewed)\b",
)

FORAGED_FINE = (
    r"\b(?:risotto|soup|pie|pizza|pasta|curry|sauce|omelette|stir\s?fry|salad|dish|recipe|toast|"
    r"restaurant|menu|cake|jam|pesto|smoothie|juice|wine|ketchup|garlic|elderflower)\b",
    r"\b(?:picked\s+up|bought|shop|supermarket|market|growing|grow|planted|seeds?\s+to|"
    r"want\s+to\s+grow|identify\w*|what\s+are\s+these|which\s+mushrooms?)\b",
    r"\b(?:cooked|cook|fried|roast\w*|boiled|baked|washed|peeled)\b",
)

CO_LEAK = (
    r"\bcarbon\s+monoxide\b.{0,40}\b(?:leak\w*|poison\w*|inhaled|breath\w*|fumes?|"
    r"giving\s+(?:off|out)|emitting|exposure)\b",
    r"\b(?:leak\w*|giving\s+(?:off|out)|emitting|inhaled|poison\w*)\b.{0,40}"
    r"\bcarbon\s+monoxide\b",
    r"\bthere'?s\s+(?:some\s+|a\s+lot\s+of\s+)?(?:carbon\s+monoxide|co)\b",
    r"\bcarbon\s+monoxide\b\s+(?:in|inside|all\s+over|coming\s+(?:in|through))\s+(?:the|my|our)\b",
)

CO_SIGNS = (
    r"\b(?:boiler|flue|cooker|hob|gas\s+fire|fireplace|wood\s*burner|woodburner|back\s+boiler|"
    r"heater|oven)\b.{0,50}\bfum(?:e|es|ing|y)\b",
    r"\bcarbon\s+monoxide\b.{0,60}\b(?:dizzy|dizziness|headach\w*|nauseous|nausea|sick|"
    r"vomit\w*|drowsy|sleepy|confused|faint\w*|light.?headed|breathless)\b",
    r"\b(?:dizzy|dizziness|headach\w*|nauseous|nausea|sick|vomit\w*|drowsy|sleepy|confused|"
    r"faint\w*|light.?headed|breathless)\b.{0,60}\bcarbon\s+monoxide\b",
)

CO_TEST = (
    r"\bhow\s+(?:do|can|should)\s+(?:i|we|you)\s+(?:test|check|service|clean|reset|change\s+the\s+battery)"
    r"\b.{0,40}\b(?:carbon\s+monoxide|co)\s+(?:alarm|detector|monitor)\b",
    r"\b(?:carbon\s+monoxide|co)\s+(?:alarm|detector|monitor)\b.{0,40}"
    r"\b(?:test|tested|testing|service|servicing|calibrat\w+|checked)\b.{0,40}\?",
    r"\bhow\s+often\b.{0,30}\b(?:carbon\s+monoxide|co)\s+(?:alarm|detector|monitor)\b",
    r"\bwhere\s+(?:should|do)\s+(?:i|we|you)\s+(?:put|place|fit|mount|install)\b.{0,30}"
    r"\b(?:carbon\s+monoxide|co)\s+(?:alarm|detector|monitor)\b",
)

_GASP_NOT_A_THIRST = (
    r"air|breath|breathe|breathing|oxygen|help|doctor|nurse|ambulance|paramedic|paramedics|"
    r"inhaler|nebuliser|nebulizer|ventilator|respirator|999|911|111|rescue|defibrillator|aed"
)
_A_THIRST = (
    r"(?:a|an|the|some|any|my|me|that|one)\s+"
    r"(?!(?:[\w'-]+\s+){0,1}(?:" + _GASP_NOT_A_THIRST + r")\b)"
    r"(?:[\w'-]+)"
)

GASP_FINE = (
    r"\bgasping\s+(?:for|after|at)\s+" + _A_THIRST,
    r"\bgasping\s+(?:for|after)\s+(?:a|an|the|some|any|my|that)\s+(?:run|walk|jog|workout|gym|session|"
    r"swim|cycle|ride|bike|spin|class|game|match|training|hill|stairs|flight\s+of\s+stairs|"
    r"shopping|hoovering|dance|dancing|song|tune|race|marathon)\b",
    r"\bgasps?\s+for\s+" + _A_THIRST,
    r"\bgasping\s+(?:on|up|coming\s+up|going\s+up|climbing)\s+(?:the\s+|a\s+|my\s+)?(?:stairs|steps|hill|"
    r"slope|incline|road|bank|staircase)\b",
    r"\b(?:i|we|he|she|they)\s+(?:was|were|'m|'re|am|are)\s+gasping\s+after\b",
    r"\bgasping\s+after\s+(?:that|the|a|my|this)\b",
)

GASP_RED = (
    r"\bcan'?t\s+breathe\b", r"\bcannot\s+breathe\b", r"\bgasping\s+for\s+(?:air|breath|oxygen)\b",
    r"\bnot\s+breathing\b", r"\bturning\s+blue\b", r"\b(?:collapsed|unconscious|passed\s+out)\b",
    r"\b(?:lips|face)\s+(?:are\s+|'re\s+)?(?:blue|grey|gray)\b", r"\bchoking\b",
    r"\b(?:his|her|their)\s+(?:chest|breathing)\b",
)

BREATH_PAST_OVER = (
    r"\b(?:years?|months?|decades?)\s+ago\b", r"\bwhen\s+(?:he|she|they|i)\s+was\s+"
    r"(?:born|a\s+baby|little|small|young|a\s+(?:child|kid|toddler))\b",
    r"\bas\s+a\s+(?:baby|child|kid|toddler|newborn)\b", r"\bback\s+then\b",
    r"\blast\s+(?:year|decade|winter|summer)\b", r"\bin\s+(?:the\s+)?(?:19|20)\d\d\b",
)

CHEST_IN_A_HAND_TAIL = (
    r"(?:\s*[,.!?;:]|\s*$|\s+(?:and|so|but|then|too|now|again|because|with|when|as|while)\b"
    r"|\s+(?:sweat\w*|clammy|grey|gray|pale|breathless|short\s+of\s+breath|sick|dizzy|"
    r"nause\w*|faint\w*|hurts?|hurting|pain\w*|ache\w*|tight\w*|pressure|fell|fallen|"
    r"collaps\w*|went\s+down)\b)"
)

CHEST_IN_A_HAND = (
    r"\A(?![^.!?]*\b(?:laugh\w*|giggl\w*|jok\w*|hysteric\w*|sides?|meme|tiktok)\b)"
    r"(?=[^.!?]*\b(?:clutch\w*|gripp?\w*|grabb?\w*|holding|holds?|held)\s+"
    r"(?:at\s+)?(?:his|her|their)\s+chest\b" + CHEST_IN_A_HAND_TAIL + r")",
    r"\A(?![^.!?]*\b(?:laugh\w*|giggl\w*|jok\w*|hysteric\w*|sides?)\b)"
    r"(?=[^.!?]*\b(?:clutch\w*|gripp?\w*|grabb?\w*|holding|holds?|held)\s+"
    r"(?:at\s+)?(?:my|the)\s+chest\b" + CHEST_IN_A_HAND_TAIL + r")"
    r"(?=[^.!?]*\b(?:sweat\w*|clammy|grey|gray|pale|breathless|short\s+of\s+breath|"
    r"sick|dizzy|nause\w*|faint\w*|fell|fallen|collaps\w*|pass(?:ed|ing)?\s+out|"
    r"went\s+down|hurts?|hurting|pain\w*|ache\w*|tight\w*|pressure)\b)",
)

DENTAL_WORDS = (r"dentist|dental|fillings?|anaesthetic|anesthetic|numbing|novocaine|injection|"
                r"wisdom\s+tooth|root\s+canal|extraction|extracted|"
                r"(?:tooth|teeth|molar)\s+(?:\w+\s+){0,2}(?:out|removed|pulled|taken|extracted)|"
                r"(?:removed|pulled|extracted|took|take)\s+(?:a\s+|my\s+|his\s+|her\s+|"
                r"their\s+|the\s+)?(?:tooth|teeth|molar)")

DRINK_WORDS = (r"drink|drinking|drunk|pints?|wine|beer|alcohol|pub|party|tipsy|night\s+out|"
               r"had\s+a\s+few|a\s+few\s+(?:pints|drinks|beers|wines)|"
               r"a\s+couple\s+of\s+(?:drinks|pints|beers|wines)|been\s+on\s+it|"
               r"on\s+the\s+lash|bladdered|squiffy|merry|half\s+cut|pissed|steaming|"
               r"stag\s+do|hen\s+do|wedding\s+do|celebrat\w*|one\s+too\s+many|"
               r"a\s+skinful|three\s+sheets")

SLUR_RED_BESIDE = (r"weak\w*|numb(?:ness|ed|ing|s)?|droop\w*|confus\w*|can'?t\s+move|can\s+not\s+move|"
                   r"one\s+side|left\s+side|right\s+side|slumped|limp\s+(?:arm|leg|hand|side)|"
                   r"dead\s+(?:arm|leg|hand|side|foot|fingers)|(?:arm|leg|hand|side|foot|face)\s+"
                   r"(?:is\s+|feels?\s+|went\s+)?(?:weak|numb|dead|heavy)")

SMALL_CHILD = (r"toddler|baby|infant|newborn|(?:one|two|1|2)[\s-]?year[\s-]?old|"
               r"1[0-9][\s-]?month[\s-]?old|1[89]\s*months|preschooler|small child|little one|"
               r"(?:son|daughter|boy|girl|child|kid)\s+is\s+(?:one|two|three|1|2|3)\b")

SLUR_THICK = (r"(?:slurr\w*|slurs?|slurred|speech\s+(?:is|are|sounds?|comes)|"
              r"words?\s+(?:are|is|come|coming|sound|sounds)|mush(?!room)\w*|thick\s+speech)")

WORDS_OUT_OCCASION = (
    r"\b(?:in|during|at)\s+(?:a\s+|the\s+|my\s+|his\s+|her\s+|their\s+|our\s+)?"
    r"(?:meetings?|interviews?|presentations?|class(?:es)?|lectures?|part(?:y|ies)|phone\s?calls?|"
    r"video\s?calls?|calls?|seminars?|assembl(?:y|ies))\b"
    r"|\bwhen(?:ever)?\s+(?:i|he|she|they)\s+(?:talk|speak|meet|phone|ring|present|"
    r"have\s+to\s+speak|stand\s+up)\b"
    r"|\bmeet(?:ing)?\s+(?:new\s+)?(?:people|someone|strangers)\b"
    r"|\bin\s+front\s+of\s+(?:people|everyone|the\s+class|a\s+crowd|others)\b"
    r"|\bpublic\s+speaking\b"
    r"|\bon\s+the\s+phone\b"
    r"|\b(?:nerv\w*|anxious|anxiety|panic\w*|shy|embarrass\w*|scared|self[- ]conscious|"
    r"introvert\w*)\b"
)

STROKE_HAND = (
    r"\b(?:can'?t|cannot|couldn'?t|could\s+not|unable\s+to|not\s+able\s+to|struggl\w*\s+to)\s+"
    r"(?:hold|grip|lift)\s+(?:my|his|her|their|our|the)\s+"
    r"(?:cup|mug|glass|drink|knife|fork|pen|phone|keys|bag|book|plate|spoon|toothbrush|comb|"
    r"hairbrush)\b",
    r"\b(?:keeps?|kept|is|was|are|were|started)\s+(?:on\s+)?dropping\s+"
    r"(?:my|his|her|their|our|the)\s+(?:cup|mug|glass|drink|knife|fork|cutlery|pen|phone|"
    r"keys|bag|book|plate|spoon|toothbrush|remote|knitting)\b",
    r"\b(?:dropped|dropping)\s+(?:my|his|her|their|our|the)\s+"
    r"(?:cup|mug|glass|drink|knife|fork|cutlery|pen|phone|keys|bag|book|plate|spoon|"
    r"toothbrush|remote|knitting)\b",
)

STROKE_HAND_HARD = (
    r"\b(?:droop\w*|"
    r"face\s+(?:is\s+|has\s+|s\s+)?(?:dropped|drooping|gone\s+on\s+one\s+side)|"
    r"slurr\w*|slurred|speech\s+(?:is\s+|was\s+|has\s+)?(?:slurred|wrong|gone|thick)|"
    r"can'?t\s+speak|cant\s+speak|wrong\s+words?|words?\s+wrong|not\s+making\s+sense|"
    r"double\s+vision|drool\w*|swallow\w*|"
    r"doesn'?t\s+know\s+(?:where|what|who)|didn'?t\s+know\s+(?:where|what|who)|"
    r"(?:one\s+side|left\s+side|right\s+side|one\s+arm|one\s+leg|one\s+hand|one\s+foot|"
    r"(?:the\s+)?left\s+(?:arm|leg|hand|foot)|(?:the\s+)?right\s+(?:arm|leg|hand|foot))"
    r"\s+(?:is\s+|has\s+gone\s+|went\s+|feels?\s+)?(?:weak\w*|numb(?:ness|ed|ing|s)?)|"
    r"(?:face|lip|mouth|tongue)\s+(?:feels?\s+|is\s+|has\s+gone\s+|went\s+)?numb(?:ness|ed|ing|s)?)",
)

STROKE_HAND_BESIDE = (
    r"\b(?:confus\w*|disorient\w*|doesn'?t\s+know\s+(?:where|what|who)|"
    r"droop\w*|face\s+(?:is\s+|has\s+|s\s+)?(?:dropped|drooping|gone\s+on\s+one\s+side)|"
    r"slurr\w*|slurred|speech\s+(?:is\s+|was\s+|has\s+)?(?:slurred|wrong|gone|thick)|"
    r"can'?t\s+speak|cant\s+speak|wrong\s+words?|words?\s+wrong|"
    r"not\s+making\s+sense|vision|can'?t\s+see|cant\s+see|blurr\w*|double\s+vision|"
    r"drool\w*|swallow\w*)\b",
) + STROKE_HAND_HARD

STROKE_HAND_CHRONIC = (
    r"\b(?:sometimes|occasionally|always|for\s+years|for\s+months|for\s+ages|"
    r"since\s+(?:the|her|his|their|last|she\s+was|he\s+was|they\s+were)|"
    r"it'?s\s+been\s+like\s+this|arthritis|arthrit\w*|parkinson\w*|multiple\s+sclerosis|"
    r"\bms\b|cerebral\s+palsy|carpal\s+tunnel|raynaud\w*|circulation|"
    r"when\s+it'?s\s+cold|when\s+it\s+is\s+cold|in\s+the\s+cold|when\s+the\s+weather\s+"
    r"(?:is\s+)?(?:cold|turns)|after\s+the\s+flu|the\s+flu\b|long\s+covid|"
    r"neuropath\w*|chemo\w*|old\s+stroke|stroke\s+years\s+ago|dementia\s+already)\b",
)

STROKE_WEAK = (
    r"\b(?:weak\w*|numb|dead|useless|heavy|droop\w*|gone\s+(?:all\s+)?(?:weak|numb|dead))\b"
    r"[^.?!]{0,25}\b(?:one\s+side|left\s+side|right\s+side|down\s+one\s+side)\b",
    r"\b(?:one\s+side|left\s+side|right\s+side)\b[^.?!]{0,25}"
    r"\b(?:weak\w*|numb|dead|useless|heavy|droop\w*|gone\s+(?:all\s+)?(?:weak|numb|dead)|"
    r"won'?t\s+work|wont\s+work|not\s+working)\b",
    r"\b(?:face|cheek|mouth|smile|eyelid|one\s+eye)\b[^.?!]{0,25}"
    r"\b(?:droop\w*|has\s+gone\s+(?:slack|droopy|funny|loose)|sagging|lopsided|gone\s+slack)\b",
    r"\b(?:can'?t|cannot|can\s+not)\s+(?:feel|move|use|hold)\s+(?:my|his|her|their)\s+"
    r"(?:arm|hand|leg|side|left\s+arm|right\s+arm|left\s+leg|right\s+leg)\b",
    r"\b(?:can'?t|cannot|can\s+not)\s+lift\s+(?:my|his|her|their)\s+(?:arm|hand)\b"
    r"(?!\s*(?:above|up|over|high|any\s*more|at\s+all|very|to\s+the|past|out))",
    r"\b(?:can'?t|cannot|can\s+not)\s+(?:lift|raise)\s+(?:both\s+(?:of\s+)?)?"
    r"(?:my|his|her|their)\s+arms\b"
    r"(?!\s*(?:above|up|over|high|any\s*more|at\s+all|very|to\s+the|past|out|since|because))",
    r"\b(?:can'?t|cannot|can\s+not)\s+(?:lift|raise)\s+both\s+arms\b"
    r"(?!\s*(?:above|up|over|high|any\s*more|at\s+all|very|to\s+the|past|out))",
    r"\b(?:my|his|her|their)\s+(?:side|left\s+(?:arm|hand|leg|side)|right\s+(?:arm|hand|leg|side))"
    r"\b[^.?!]{0,15}\b(?:has\s+|have\s+|had\s+|went\s+|is\s+|feels?\s+|feels\s+like\s+its\s+)?"
    r"(?:gone|went|all)\s+(?:all\s+)?(?:numb|dead|useless|weak|funny|heavy|like\s+lead)\b",
    r"\b(?:my|his|her|their)\s+(?:arm|hand)\b[^.?!]{0,15}"
    r"\b(?:has\s+|have\s+|had\s+|went\s+|is\s+|feels?\s+|feels\s+like\s+its\s+)?"
    r"(?:gone|went|all)\s+(?:all\s+)?(?:dead|useless|weak)\b",
    r"\b(?:my|his|her|their)\s+(?:arm|hand)\b[^.?!]{0,25}\bnumb(?:ness|ed|ing|s)?\b[^.?!]{0,25}"
    r"\b(?:for\s+(?:a\s+)?(?:few|several|couple\s+of|two|three|ten|twenty|\d+)\s+"
    r"(?:minutes?|mins?|hours?|hrs?)|came\s+and\s+went|then\s+it\s+went|"
    r"out\s+of\s+nowhere|suddenly|this\s+(?:morning|afternoon|evening))\b",
    r"\b(?:lost|loss\s+of)\s+(?:the\s+)?(?:sight|vision)\s+in\s+"
    r"(?:(?:my|his|her|their)\s+)?(?:left|right|one|an?)\s+eye\b",
    r"\b(?:can'?t|cannot)\s+see\s+(?:out\s+of|with|in)\s+(?:(?:my|his|her|their)\s+)?"
    r"(?:left|right|one)\s+(?:of\s+(?:my|his|her|their)\s+)?eyes?\b",
    r"\b(?:my|his|her|their)\s+(?:sight|vision|eye)\b[^.?!]{0,15}"
    r"\b(?:has\s+|have\s+|had\s+)?(?:gone|went|is\s+gone)\b"
    r"(?!\s+(?:all\s+)?(?:blurry|blurred|fuzzy|dim|funny|worse|bad|downhill|soft|double)\b)"
    r"(?![^.?!]{0,25}\b(?:black|red|puffy|swollen|bloodshot|bruised)\b)"
    r"(?![^.?!]{0,25}\bwhen\s+(?:i|he|she|they)\s+(?:stand|stands|get\s+up|gets\s+up|bend|bends|"
    r"stood|got\s+up)\b)"
    r"(?![^.?!]{0,25}\b(?:briefly|momentarily|for\s+(?:a|an|a\s+few)\s+(?:second|seconds|moment|"
    r"minute|minutes)|then\s+(?:it\s+)?came\s+back|and\s+came\s+back)\b)",
    r"\b(?:blind|sightless)\s+in\s+(?:my|his|her|their|one)\s+(?:left|right|one)\s+eye\b",
    r"\b(?:gone|going|went)\s+blind\b(?!\s+(?:drunk|fold|folded|baked?))"
    r"(?![^.?!]{0,25}\b(?:briefly|momentarily|for\s+(?:a|an|a\s+few)\s+(?:second|seconds|moment|"
    r"minute|minutes)|then\s+(?:it\s+)?came\s+back|and\s+came\s+back)\b)",
)

SIGHT_A_WHILE = (
    r"\bfor\s+(?:\d+|a\s+couple\s+of|couple\s+of|a\s+few|few|several|many|a|an|two|three|four|"
    r"five|six|seven|eight|nine|ten)\s+(?:days?|weeks?)\b",
    r"\b(?:a\s+couple\s+of\s+(?:days|weeks)|a\s+few\s+(?:days|weeks)|\d+\s+(?:days|weeks))\s+ago\b",
    r"\byesterday\b", r"\blast\s+(?:night|week)\b",
)

STROKE_WEAK_OFF = (
    r"\b(?:cold|freezing|frozen|snow|outside|slept\s+on|sleeping\s+on|lay\s+on|lying\s+on|"
    r"sat\s+on|sat\s+funny|trapped\s+nerve|pins\s+and\s+needles|gym|weights|workout|"
    r"leg\s+day|dentist|filling|anaesthetic|anesthetic|migraine|hungover|drunk|massage|"
    r"blood\s+test|injection|vaccine|jab)\b",
    r"\b(?:can'?t|cannot|can\s+not)\s+lift\s+(?:my|his|her|their)\s+(?:arm|hand)\b"
    r"[^.?!]{0,40}\b(?:because|since|due|after|from|thanks)\b[^.?!]{0,30}"
    r"\b(?:shoulder|rotator|elbow|wrist|sling|cast|crutch|collarbone|collar\s+bone|operation|"
    r"surgery|operated|post-?op|broken|fracture\w*|cracked|pulled|strained|sprain\w*|arthritis|"
    r"arthritic|injured|injury|tendon|ligament|bursitis|frozen)\b",
    r"\b(?:shoulder|rotator|elbow|wrist|sling|cast|collarbone|operation|surgery|broken|"
    r"fracture\w*|strained|sprain\w*|arthritis|injured|injury)\b[^.?!]{0,40}"
    r"\b(?:can'?t|cannot)\s+lift\s+(?:my|his|her|their)\s+(?:arm|hand)\b",
    r"\blift\s+(?:my|his|her|their)\s+(?:arm|hand)\b[^.?!]{0,20}\bto\s+(?:reach|touch|grab|"
    r"hold|carry|wave|put|scratch|open|close|comb|wash|brush|dry|dress|text|type)\b",
    r"\b(?:one|an?)\s+eye\s+(?:closed|shut|covered|patched|winking)\b",
    r"\b(?:hands|feet|foot|toes|fingers|legs)\b",
    r"\b(?:both|two)\b[^.?!]{0,20}\b(?:numb|dead|tingl\w*|pins\s+and\s+needles|asleep)\b",
    r"\b(?:numb|dead|tingl\w*|pins\s+and\s+needles|asleep)\b[^.?!]{0,20}\b(?:both|two)\b",
    r"\barms\b[^.?!]{0,25}\b(?:numb|dead|tingl\w*|pins\s+and\s+needles|asleep|fell\s+asleep)\b",
    r"\b(?:numb|dead|tingl\w*|pins\s+and\s+needles|asleep)\b[^.?!]{0,25}\barms\b",
    r"\b(?:sitting|sat|seated|stood|standing|kneeling|crouched|leaning|leant|slouched|"
    r"crossed\s+(?:my|his|her|their)\s+legs|asleep|sleep\w*|in\s+the\s+night|at\s+night|"
    r"overnight|in\s+bed|holding|held|carrying|carried|gripping|gripped|grip|pressed|"
    r"pressure|squeez\w*|shopping|bags?|phone|driving|driven|typing|writing|playing|knitting|"
    r"sewing|guitar|piano|cinema|sofa|desk|train|bus|theatre|meeting|lecture|church|"
    r"sleep\s+on\s+it)\b",
    r"\b(?:hayfever|hay\s+fever|allerg\w*|conjunctivitis|sty|stye|contact\s+lens|lens|"
    r"cataract\w*|glaucoma|laser\s+surgery|new\s+glasses|optician|"
    r"itch\w*|screen|flu|cold|sinus\w*|infected|infection)\b",
    r"\b(?:eye\s*shadow|eye\s*liner|eyeliner|mascara|make-?up|foundation|moisturis\w*|"
    r"sunscreen|sun\s?cream|shampoo|soap|shower\s+gel|toothpaste|glasses|specs|goggles|"
    r"contact\s+lenses?)\b",
    r"\bfor\s+(?:\d+\s+|a\s+few\s+|many\s+|most\s+of\s+my\s+)?(?:years|decades|months)\b",
    r"\b(?:since\s+(?:(?:i|he|she|they|we)\s+(?:was|were)\s+|(?:a|an)\s+)"
    r"(?:a\s+)?(?:child|kid|baby|born|birth|little)|"
    r"all\s+my\s+life|my\s+whole\s+life|for\s+as\s+long\s+as\s+i\s+can\s+remember|"
    r"from\s+birth|born\s+(?:blind|with)|was\s+born|as\s+a\s+(?:child|kid|baby)|"
    r"(?:many\s+)?years\s+ago|a\s+lazy\s+eye|lazy\s+eye|always\s+(?:been|had))\b",
    r"\bsince\s+(?:birth|childhood|i\s+was\s+(?:little|a\s+kid|a\s+baby))\b",
    r"\bborn\s+(?:blind|deaf|with\s+one\s+eye|without\s+(?:an|one)\s+eye)\b",
)

RESPOND_SENSE = (r"to\s+(?:(?:the|my|his|her|their|these|those)\s+)?(?:tablets?|pills?|medication|"
                 r"medicine|meds|antibiotics?|injections?|treatment|chemo|therapy|dose|drugs?|"
                 r"texts?|messages?|emails?|calls?|whatsapp|letters?|tickets?|names?|phones?|"
                 r"mobiles?|landline|voicemail|answerphone|doorbell)\b")

PERSON = (r"(?:mum|mom|mother|dad|father|son|daughter|husband|wife|partner|boyfriend|girlfriend|"
          r"brother|sister|friend|flatmate|roommate|baby|child|kid|kids|children|"
          r"grand(?:child|children|son|daughter|kid)s?|step(?:child|children|son|daughter)s?|"
          r"boy|girl|man|woman|"
          r"lady|guy|bloke|neighbou?r|colleague|boss|gran|granny|nan|grandad|grandma|grandpa|mate|"
          r"carers?|care\s+workers?|support\s+workers?|social\s+workers?|personal\s+assistants?|"
          r"nurses?|midwives?|midwife|doctors?|gps?|physios?|therapists?|"
          r"patient|pupil|student|teacher|driver|passenger|singer|player|runner|swimmer)")

HELP_SOMEONE = (
    r"\b(?:(?:want|wanted|need|needed|trying|try)\s+to\s+)?(?:help|support|approach|talk\s+to|"
    r"deal\s+with)\s+(?:a|an|my|some)\s+" + PERSON +
    r"\b[^.?!]{0,40}\b(?:suicid\w*|self[-\s]?harm\w*|cutting|hurting\s+(?:him|her|them)sel(?:f|ves)|"
    r"wants?\s+to\s+die|starving\s+(?:him|her|them)sel(?:f|ves))\b",
)

SUICIDE_TOPIC = (
    r"\b(?:article|book|documentar(?:y|ies)|film|movie|programme|program|podcast|episode|news|"
    r"paper|report|study|studies|research|statistics?|stats|figures?|rates?|numbers|data|"
    r"training|trained|counsell?or|counselling|counseling|helpline|charity|campaign|awareness|"
    r"prevention|policy|lecture|course|class|essay|thesis|dissertation|talk|seminar|conference|"
    r"day|week|month)\b[^.?!]{0,30}\bsuicid",
    r"\bsuicid\w*\b[^.?!]{0,20}\b(?:rates?|statistics?|figures?|numbers|prevention|awareness|"
    r"campaign|helpline|charity|counsell?or|research|paper)\b",
)

SHAKEN = (
    r"\b(?:i|we|he|she|they)\s+(?:shook|shaken|have\s+shaken|has\s+shaken)\s+"
    r"(?:him|her|them|the\s+(?:baby|newborn|infant|toddler|child)|my\s+(?:baby|newborn|infant|son|"
    r"daughter|child|kid|boy|girl|toddler))\b",
    r"\b(?:shook|shaken)\s+(?:the|my|our|his|her)\s+(?:baby|newborn|infant|toddler)\b",
    r"\b(?:baby|newborn|infant|toddler)\b[^.?!]{0,25}\b(?:was|were|got|has\s+been|had\s+been)\s+"
    r"shaken\b",
)

SHAKEN_REPLY = (
    "A baby who has been shaken needs checking now, even if they seem fine: bleeding inside the "
    "head can take hours to show. Ring 999 or 911 if they are floppy, drowsy, sick, fitting or "
    "not feeding normally, otherwise take them to A&E today - and if you feel close to shaking "
    "them, put them down safely and step away for a minute.",
    "That needs a doctor today: shaking a baby can bleed inside the head without a mark on them. "
    "Ring 999 or 911 if they go floppy, drowsy, vomit or fit, and otherwise go straight to A&E - "
    "putting the baby down safely and walking away for a minute is the right move when you are "
    "at the end of your rope.",
)

THIRD_PERSON_ACTOR = (
    r"\b(?:he|she|they|my\s+(?:friend|mate|boyfriend|girlfriend|partner|husband|wife|son|daughter|"
    r"child|kid|mum|mom|mother|father|dad|brother|sister|step\w+|cousin|nephew|niece|grandson|"
    r"granddaughter|gran|nan|ex|flatmate|housemate|neighbou?r|colleague|boss|classmate|patient|"
    r"client|lodger|aunt|auntie|uncle))\b",
)

OTHER_SELF_HARM = (
    r"\b(?:my\s+(?!own\b)\w+|he|hes|she|shes|they|someone|somebody)\b.{0,20}\b(?:cuts?|cutting|hits?|"
    r"hitting|burns?|burning|hurts?|hurting|pinch(?:es|ing)|scratch(?:es|ing)|bites?|biting|"
    r"bangs?|banging|starves?|starving|scalds?|scalding)\s+(?:him|her|them)sel(?:f|ves)\b"
    r"(?=\s+(?:on\s+purpose|again\b|when\s+(?:he|she|they)\s*(?:'s|s|is|are|was|were)\b|"
    r"to\s+(?:hurt|punish|cope)|because\b))",
    r"\b(?:my\s+(?!own\b)\w+|he|hes|she|shes|they|someone|somebody)\b.{0,20}\b(?:cuts?|cutting|hits?|"
    r"hitting|burns?|burning|hurting|pinch(?:es|ing)|scratch(?:es|ing)|"
    r"bangs?|banging|starves?|starving|scalds?|scalding)\s+(?:him|her|them)sel(?:f|ves)\b"
    r"(?!\s+(?:on|with|in|at|by|while|against|accidentally|shaving|cooking|chopping|opening|"
    r"playing|making|ironing|cycling|running|trying)\b)",
)

AGE_PERSON = (r"(?:\d{1,2}[\s-]*(?:month|months|week|weeks|year|years|yr|yrs|mo|mth|mths)"
              r"[\s-]*old\b|"
              r"(?:\d{1,2}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)"
              r"[\s-]*(?:months?|weeks?|years?|yrs?)[\s-]+old\b|"
              r"\b(?:newborn|newborns|toddlers?|infants?|teenagers?|teens?|preschoolers?|"
              r"schoolboy|schoolgirl)\b)",)

BLUE_TINGE = (
    r"(?=.*\b(?:blue|grey|gray)\s+tinge\b)(?=.*\b(?:lips?|mouth|face|skin|fingers?|"
    r"fingertips?|hands?|feet|toes|nails?|cheeks?|tongue|gums)\b)",
    r"(?=.*\btinge\s+of\s+(?:blue|grey|gray)\b)(?=.*\b(?:lips?|mouth|face|skin|fingers?|"
    r"fingertips?|hands?|feet|toes|nails?|cheeks?|tongue|gums)\b)",
)

BLUE = (
    r"\b(?:going|went|turned|turning|gone|goes|turns?)\s+blue\b",
    r"\b(?:lips?|face|fingertips?|fingers?|nail\s?beds?|around\s+the\s+mouth|skin|"
    r"cheeks?|tongue|gums|hands?|feet|toes|legs?|mouth)\b.{0,20}"
    r"\b(?:blue|grey|gray)\b",
    *BLUE_TINGE,
    r"\b(?:blue|grey|gray)\s+(?:around\s+the\s+lips?|round\s+the\s+lips?|in\s+the\s+face|lips?)\b",
    r"\b(?:blue|grey|gray)\s+all\s+over\b",
    r"\b(?:i|i'm|he|he's|she|she's|they|they're|we|you|someone|somebody|"
    r"(?:my|the|our)\s+" + PERSON + r"|" + PERSON + r")\s+"
    r"(?:is|was|are|were|looks?|looking|looked|appears?|seems?|becomes?|becoming|"
    r"has\s+gone|had\s+gone|went|turned|turning|going|gone|getting|gets)\s+"
    r"(?:(?:a|bit|really|very|so|all|quite|pale|grey|gray|cold|clammy|sweating|confused|"
    r"shivering|breathless|struggling|limp|floppy|sleepy|and)\s+){0,4}"
    r"(?:blue|grey|gray)\b",
)

PET_ANY = (
    r"\b(?:dog|dogs|puppy|puppies|pup|pups|cat|cats|kitten|kittens|rabbit|rabbits|bunny|bunnies|"
    r"hamster|hamsters|guinea\s+pig|guinea\s+pigs|parrot|parrots|budgie|budgies|bird|birds|"
    r"ferret|ferrets|horse|horses|pony|ponies|tortoise|tortoises|snake|snakes|lizard|lizards|"
    r"gerbil|gerbils|rat|rats|pet|pets)\b",
)

BLUE_STRONG = (
    r"\b(?:going|turned|turning|gone|goes|go|turns?|getting|gets|is\s+turning)\s+"
    r"(?:blue|grey|gray)\b",
    r"\b(?:lips?|face|fingertips?|fingers?|nail\s?beds?)\b.{0,20}\b(?:blue|grey|gray)\b",
    r"\b(?:blue|grey|gray)\s+all\s+over\b",
)

LIPS_COLD = (
    r"\b(?:lips?|mouth|face)\b[^.!?]{0,30}\b(?:cold|freezing|frozen|chilly|perishing|the\s+snow|"
    r"the\s+sea|the\s+pool|the\s+swim|a\s+swim|swimming)\b",
    r"\b(?:cold|freezing|frozen|chilly)\b[^.!?]{0,30}\b(?:lips?)\b",
    r"\b(?:out\s+in\s+the\s+cold|in\s+this\s+cold|from\s+the\s+cold)\b",
)

COLD_ILLNESS = (
    r"\b(?:have|has|had|having|got|caught|catch|fighting|full\s+of|down\s+with|"
    r"coming\s+down\s+with|suffering\s+from|come\s+down\s+with|getting)\s+"
    r"(?:a|the|my|his|her|their|this|such\s+a|a\s+really)\s+(?:\w+\s+){0,2}cold\b",
    r"\ba\s+cold\b[^.!?]{0,20}\b(?:chest|flu|fever|temperature|wheeze|coughing)\b",
    r"\b(?:my|his|her|their|the)\s+(?:\w+\s+){0,2}cold\b[^.!?]{0,20}"
    r"\b(?:wont\s+shift|worse|gone\s+to\s+my\s+chest)\b",
)

BLUE_FOOD = (
    r"\b(?:tomato(?:es)?|cheese|milk|chicken|beef|pork|lamb|meat|fish|ham|bacon|bread|toast|"
    r"pickle(?:s|d)?|chutney|kimchi|sauerkraut|"
    r"dough|batter|rice|pasta|potato(?:es)?|onion(?:s)?|garlic|fruit|apple(?:s)?|banana(?:s)?|"
    r"orange(?:s)?|lemon(?:s)?|berries|strawberr(?:y|ies)|grape(?:s)?|cabbage|lettuce|salad|"
    r"vegetables?|soup|sauce|smoothie|juice|wine|beer|yogurt|yoghurt|cream|butter|egg(?:s)?|"
    r"mushroom(?:s)?|courgette(?:s)?|cake|biscuit(?:s)?|leftovers?)\b",
)

BLUE_PERSON_SUBJECT = (
    r"\b(?:i|i'm|i\s+am|he|he's|she|she's|they|they're|we|we're|you|someone|somebody|anyone|"
    r"baby|child|children|kid|kids|toddler|infant|boy|girl|man|woman|mum|mom|mother|dad|father|"
    r"son|daughter|husband|wife|partner|friend|gran|grandma|grandad|nan|"
    r"(?:my|the|our)\s+" + PERSON + r")\b[^.!?]{0,20}\b"
    r"(?:is|was|are|were|went|gone|goes|going|turned|turning|turns?|looks?|looking|looked|"
    r"appears?|seems?|become|becomes|becoming|getting|gets)\s+(?:\w+\s+){0,3}"
    r"(?:blue|grey|gray)\b",
)

BLUE_OTHER_PERSON = (
    r"\b(?:he|she|him|her|they|them|his|hers|their|someone|somebody|anyone|man|woman|boy|girl|"
    r"child|children|baby|babies|toddler|patient|kid|kids|mum|mom|mother|dad|father|son|daughter|"
    r"husband|wife|partner|boyfriend|girlfriend|brother|sister|friend|gran|grandma|grandad|"
    r"grandpa|nan|uncle|aunt|niece|nephew|colleague|neighbour|neighbor|people|men|women|workers?|"
    r"guests?|everyone|anybody)\b",
)

BLUE_CLOTH = (
    r"\b(?:jeans|jumper|jumpers|top|tops|shirt|shirts|t-?shirts?|blouse|dress|dresses|trousers|"
    r"pants|shorts|skirt|coat|jacket|hoodie|cardigan|socks?|tights|knickers|underwear|bra|pyjamas|"
    r"pjs|washing|laundry|whites|wash|fabric|clothes|clothing|cloth|wool|denim|cotton|linen|"
    r"curtains?|sheets?|towels?|bedding|duvet|cover|cushion|carpet|rug|dye|dyed|dyeing|bleach|"
    r"paint|paintbrush|pen|ink|felt\s?tip|highlighter)\b",
)

BLUE_FINE = (
    r"\b(?:feel|feeling|feels|felt)\s+(?:a\s+bit\s+|really\s+|so\s+|very\s+)?(?:blue|grey|gray)\b",
    r"\b(?:i'?m|i\s+am)\s+(?:a\s+bit\s+|really\s+|so\s+)?blue\b",
    r"\b(?:mood|day|monday|week|film|movie|song|album|book)\b.{0,15}\b(?:blue|grey|gray)\b",
    r"\b(?:blue|grey|gray)\s+(?:mood|day|monday|car|door|paint|paintwork|wall|walls|sky|carpet|"
    r"sofa|dress|shirt|top|jeans|coat|eyes?|bin|bag|towel|fabric|nail\s+varnish|polish|cheese|"
    r"milk|ink|pen|light|screen|toothbrush|hair|tie|shoes?|trainers?|hat|scarf)\b",
    r"\bblue\s+cheese\b",
    r"\b(?:room|rooms|wall|walls|ceiling|kitchen|bathroom|bedroom|hall|hallway|lounge|floor|"
    r"woodwork|paintwork|curtains?|blinds?|lighting|light)\b[^.?!]{0,25}\b(?:blue|grey|gray)\b",
    r"\b(?:paint|painting|painted|dye|dyed|sprayed|spray)\b[^.?!]{0,25}\b(?:blue|grey|gray)\b",
    r"\b(?:wearing|wears?|bought|buy|buying|got|getting|choose|chooses|chose|chosen|picked|pick|"
    r"like|likes|love|loves|prefer|prefers|want|wants|wanted|need|needs|needed|ordered|order|"
    r"matches|match)\b[^.?!]{0,25}\b(?:blue|grey|gray)\b",
    r"\b(?:blue|grey|gray)\b[^.?!]{0,20}\b(?:paint|dye|shirt|dress|top|coat|jeans|hat|scarf|"
    r"shoes|trainers|car|door|wall|carpet|sofa|bag|towel|team|kit|badge|light|card|ticket|"
    r"folder|mug|cup|plate|bike|bicycle|pram|buggy|room|bedroom|bathroom)\b",
)

SELF_TALK = (
    r"\b(?:tell|tells|telling|told|ask|asks|asking|asked|say|says|saying|said|think|thinks|thinking|"
    r"thought|remind|reminding|reminded|convince|convincing|convinced|promise|promising|promised|"
    r"let|letting|made|make|making|allow|allowing|allowed|permit|permitting|permitted|forgive|"
    r"forgiving|gave|give|giving|reassure|reassuring|reassured|comfort|comforting|talk|talking|"
    r"keeping)\b[^.?!]{0,16}\bmy\s*self\b",
)

ROUTINE_WAKE = (
    r"\b(?:can'?t|cant|cannot|won'?t|wont|isn'?t|is\s+not|not)\s+wake\s+(?:up\s+)?"
    r"(?:for|to|before|in\s+time\s+for|on\s+time\s+for)\s+"
    r"(?:school|work|college|uni|university|nursery|childminder|the\s+(?:school\s+)?(?:bus|train)|"
    r"(?:his|her|their|my|an?)\s+(?:exam|exams|test|appointment|meeting|interview|shift|flight|"
    r"lesson|lecture|class|early\s+start))\b",
    r"\b(?:can'?t|cant|cannot|won'?t|wont)\s+wake\s+(?:up\s+)?to\s+get\s+(?:to|ready\s+for)\s+"
    r"(?:school|work|college|uni|university|nursery)\b",
    r"\b(?:for|to)\s+(?:school|work|college|uni|university|nursery)\s+(?:this\s+)?"
    r"(?:morning|today)\b.{0,20}\b(?:won'?t|wont|can'?t|cant)\s+wake\b",
)

WAKE_RED = (
    r"\b(?:not|isn'?t|stopped)\s+breathing\b", r"\bblue\b", r"\blips\b",
    r"\b(?:seizure|fit|fits|limp|floppy|unconscious|unresponsive|pulse|ambulance)\b",
    r"\b(?:temperature|fever|feverish)\b", r"\bburning\s+up\b",
    r"\bhot\s+to\s+(?:the\s+)?touch\b",
    r"\b(?:grey|gray|pale|clammy|sweating)\b", r"\bvomit\w*\b",
    r"\b(?:been\s+)?sick\s+(?:all\s+night|all\s+day|twice|three\s+times|since)\b",
    r"\bslurr\w*\b", r"\bnot\s+making\s+sense\b", r"\bdoesn'?t\s+make\s+sense\b",
    r"\bconfused\b", r"\bcan'?t\s+(?:speak|talk)\b", r"\bface\s+(?:is\s+|looks\s+)?droop\w*\b",
    r"\b(?:one\s+side|his\s+side|her\s+side)\s+(?:is\s+)?(?:weak|limp|dropping)\b",
)

_COPULA = (r"(?:is|are|was|were|keeps?|kept|started|he'?s|hes|she'?s|shes|they'?re|theyre)")
_FITTING_A_THING = (
    r"(?!\s+(?:in|on|into|up|together|his|her|their|my|your|our|the|a|an|"
    r"new|some|another|kitchen|bathroom|windows?|doors?|floor|carpet|wardrobe|cabinets?|shelves|"
    r"shelf|tiles|laminate|boiler|units?|radiators?|dishwasher|oven|cooker|shower|toilet|sink|"
    r"sofa|bed|lino)\b)")
SEIZURE = (
    r"\bseizur\w*\b", r"\b(?:had|has|having|have)\s+a\s+fit\b", r"\bconvuls(?:ing|ions?)\b",
    r"\b" + _COPULA + r"\s+fitting\b" + _FITTING_A_THING,
    r"\b" + _COPULA + r"\s+seizing\b(?!\s+up)",
)

FIT_ROUTINE = (
    r"\b(?:every\s+(?:few|couple\s+of|so\s+many)\s+(?:months|weeks|years)|twice\s+a\s+year|"
    r"once\s+a\s+year|a\s+(?:few|couple)\s+of\s+times\s+a\s+year|now\s+and\s+(?:then|again)|"
    r"from\s+time\s+to\s+time|keppra|epilep\w*)\b",
    r"\bfits?\s+(?:when|if|whenever)\b[^.?!]{0,30}\b(?:tired|unwell|poorly|ill|stressed|"
    r"miss\w*|forget\w*|skip\w*|meds?|medicine|tablets?|keppra)\b",
)

SEIZURE_STORY_GUARD = (
    r"\bseizure\s+(?:laughing|from\s+laughing)\b",
    r"\bseizures?\s+of\s+(?:laughter|laughing|giggl\w*|coughing|sneez\w*)\b",
    r"\b(?:had|having|have|get)\s+a\s+seizure\s+(?:laughing|at\s+that)\b",
    r"\bfits?\s+of\s+(?:cough\w*|sneez\w*|giggl\w*|laughter|laughing|the\s+giggles|"
    r"temper|pique)\b",
    r"\b(?:nearly|almost|thought\s+i'?d)\s+(?:had\s+)?(?:a\s+)?(?:seizure|fit)\b",
)

FIT_STILL_RINGS = (
    r"\b(?:can'?t|cannot|not|stopped|isn'?t|stop)\s+breath", r"\bwon'?t\s+stop\b",
    r"\bisn'?t\s+stopping\b", r"\bkeeps?\s+going\b", r"\bunconscious\b", r"\bcollapsed\b",
    r"\bon\s+the\s+floor\b", r"\bconvuls\w*", r"\bturning\s+blue\b", r"\bblue\s+lips\b",
    r"\bstiff\b", r"\bshaking\s+all\s+over\b", r"\bambulance\b",
)

CHILDHOOD_FIT = (
    r"\b(?:as|when\s+i\s+was)\s+(?:a\s+|an\s+)?(?:kid|child|baby|toddler|tot|infant|nipper|"
    r"young|little|small|at\s+school)\b",
    r"\b(?:in|during)\s+my\s+childhood\b",
    r"\bwhen\s+i\s+was\s+(?:about\s+)?(?:one|two|three|four|five|six|seven|eight|nine|ten|"
    r"eleven|twelve|1|2|3|4|5|6|7|8|9|10|11|12)\b",
)

FIT_THIS_WEEK = (
    r"\b(?:last\s+(?:week|weekend|friday|saturday|sunday|monday|tuesday|wednesday|thursday)|"
    r"earlier\s+this\s+week|the\s+other\s+(?:day|night)|yesterday|"
    r"a\s+(?:few|couple\s+of)\s+days?\s+ago|\d+\s+days?\s+ago|on\s+(?:monday|tuesday|"
    r"wednesday|thursday|friday|saturday|sunday))\b",
)

SEIZURE_FIGURATIVE = (
    r"\bseizure\s+(?:laughing|from\s+laughing)\b",
    r"\b(?:had|having|have|get)\s+a\s+seizure\s+(?:laughing|when|at\s+that)\b",
    r"\b(?:nearly|almost|thought\s+i'?d)\s+(?:had\s+)?(?:a\s+)?(?:seizure|fit)\b",
    r"\bfit\s+of\s+(?:cough\w*|laughter|laughing|sneez\w*|giggles|itch\w*|temper|pique)\b",
)

MILD_CHOKE = (
    r"\bi\s+chok(?:ed|ing)\s+on\s+(?:(?:my|your|his|her|their|a|an|some|the)\s+)?(?:own\s+)?"
    r"(?:drink|tea|coffee|water|juice|"
    r"beer|wine|ice|pill|tablet|vitamin|crisp|chip|crumb|sweet|grape|bit\s+of\s+\w+|mouthful|"
    r"spit(?:tle)?|saliva|it)\b",
    r"\bi\s+chok(?:ed)\s+(?:at|in|during)\s+(?:the\s+)?\w+",
    r"\bi\s+(?:nearly|almost)\s+choked\b", r"\bchoked?\s+(?:on\s+)?laughing\b",
)

CHOKE_RED = (
    r"\b(?:can'?t|cannot|couldn'?t|unable\s+to)\s+(?:breathe|breath|brethe|speak|talk|make\s+a\s+sound)\b",
    r"\b(?:went|turned|going|turning|is|looks?)\s+blue\b", r"\b(?:lips?|face)\s+(?:are|is|going)\s+blue\b",
    r"\b(?:still|now|and)\s+choking\b", r"\b(?:collapsed|unconscious|gone\s+limp|floppy)\b",
    r"\b(?:holding|clutching|grabbing)\s+(?:his|her|their|my)\s+throat\b",
    r"\bchoking\s+(?:and|but)\s+(?:can'?t|cannot)\b",
)

CHOKE_STILL_RED = (
    r"\bcan'?t\s+breathe\b", r"\bcannot\s+breathe\b", r"\bcan'?t\s+(?:speak|talk|get\s+(?:any\s+)?"
    r"(?:air|breath))\b", r"\bnot\s+breathing\b", r"\b(?:turning|going|gone)\s+blue\b",
    r"\b(?:lips|face|mouth)\s+(?:are\s+|'re\s+|is\s+)?(?:blue|grey|gray)\b",
    r"\bno\s+air\b", r"\b(?:airway|throat)\s+(?:is\s+|'s\s+)?(?:blocked|closing|swollen)\b",
    r"\bstill\s+choking\b", r"\bstuck\s+in\s+(?:my|his|her|their)\s+throat\b",
    r"\b(?:passed|passing|faint|fainted|collapsed|unconscious)\b",
)

WENT_BLUE_IDIOM = (
    r"\b(?:went|going|go|turn(?:ed|s)?|turning)\s+blue\s+in\s+the\s+face\b.{0,60}"
    r"\b(?:laugh\w*|joke\w*|crying|shouting|screaming|kidding|breath\w*)\b",
    r"\b(?:laugh\w*|joke\w*|crying|holding\s+(?:my|his|her|your)\s+breath|"
    r"held\s+(?:my|his|her|your)\s+breath)\b.{0,60}"
    r"\b(?:went|going|go|turned?|turning)\s+blue\s+in\s+the\s+face\b",
    r"\b(?:hold|holds|holding|held)\s+(?:my|his|her|their|your|the)?\s*breath\b[^.?!]{0,60}"
    r"\b(?:go\w*|went|turn(?:ed|s|ing)?|turning)\s+blue\b",
    r"\b(?:go\w*|went|turn(?:ed|s|ing)?|turning)\s+blue\b[^.?!]{0,60}"
    r"\b(?:hold|holds|holding|held)\s+(?:my|his|her|their|your|the)?\s*breath\b",
    r"\b(?:went|going|go|goes|turn(?:ed|s|ing)?|turning)\s+blue\b[^.?!]{0,50}"
    r"\b(?:laugh\w*|joke\w*|kidding|giggling)\b",
    r"\b(?:laugh\w*|joke\w*|kidding|giggling)\b[^.?!]{0,50}"
    r"\b(?:went|going|go|goes|turn(?:ed|s|ing)?|turning)\s+blue\b",
)

WENT_BLUE_FINE = (
    r"\braynaud\w*\b", r"\bin\s+the\s+cold\b", r"\bwhen\s+(?:it'?s|its)\s+cold\b",
    r"\bwith\s+(?:the\s+)?cold\b", r"\bafter\s+(?:a\s+)?(?:swim|cold\s+swim|bath)\b",
    r"\bthe\s+wash\b", r"\bwash(?:ing)?\s+machine\b", r"\bjeans\b", r"\bbruise\b",
    r"\bcold\b", r"\bfreez\w*", r"\bwinter\b", r"\bsnow\b", r"\bice\b",
)

BLUE_COLD_CAUSE = (
    r"\bwith\s+(?:the\s+)?cold\b", r"\bin\s+the\s+cold\b", r"\bwhen\s+(?:it'?s|its)\s+cold\b",
    r"\bin\s+(?:this|that)\s+cold\b",
    r"\bafter\s+(?:a\s+)?(?:swim|cold\s+swim|bath)\b", r"\bfrom\s+the\s+cold\b",
    r"\b(?:he|she|they|i|we|it)\s*(?:'s|s|is|are|am|was|were|feels?|felt)\s+"
    r"(?:so\s+|very\s+|really\s+|a\s+bit\s+|already\s+|freezing\s+)?cold\b",
    r"\bfreezing\b", r"\bshiver\w*", r"\bhypotherm\w*",
)

MACHINE = (
    r"\b(?:blender|food\s+processor|liquidis(?:er|or)|mincer|meat\s+grinder|mangle|shredder|"
    r"chipper|wood\s+chipper|washing\s+machine|tumble\s+dryer|spin\s+dryer|drill|circular\s+saw|"
    r"chainsaw|bench\s+saw|lathe|hydraulic\s+press|conveyor|escalator|elevator|mower|lawnmower|"
    r"strimmer|hedge\s+trimmer|auger|cement\s+mixer|pasta\s+machine)\b"
)

STUCK_MACHINE = (
    r"\b(?:hand|hands|arm|arms|finger|fingers|thumb|wrist|foot|leg|toe|toes|hair|knee|head|"
    r"clothes|sleeve|jumper|coat|scarf|glove|jewellery|ring)\b[^.?!]{0,40}\b(?:stuck|caught|"
    r"trapped|jammed|wedged|pinned|crushed|sucked\s+in)\b[^.?!]{0,40}\b" + MACHINE,
    r"\b" + MACHINE + r"\b[^.?!]{0,40}\b(?:has|have|got|took|caught|grabbed|crushed|sucked|"
    r"chewed)\b[^.?!]{0,30}\b(?:my|his|her|their|the)\s+(?:hand|arm|finger|fingers|sleeve|hair|"
    r"jumper|coat)\b",
    r"\b" + MACHINE + r"\b[^.?!]{0,40}\b(?:stuck|caught|trapped|jammed|wedged|crushed)\b"
    r"(?=[^.?!]{0,70}\b(?:my|his|her|their|the)\s+(?:hand|hands|arm|arms|finger|fingers|thumb|"
    r"wrist|foot|feet|leg|legs|toe|toes|hair|knee|head|sleeve|jumper|coat|scarf|glove)\b)",
    r"\b(?:hand|hands|arm|arms|finger|fingers|thumb|wrist|foot|feet|leg|legs|toe|toes|hair|knee|"
    r"sleeve|jumper|coat|scarf|glove)\b[^.?!]{0,40}\b" + MACHINE +
    r"\b[^.?!]{0,40}\b(?:stuck|caught|trapped|jammed|wedged|crushed)\b",
)

BLEEDING = (
    r"\b(?:bleeding|blood)\s+(?:badly|heavily|everywhere|a\s+lot|so\s+much|profusely)\b",
    r"\bso\s+much\s+blood\b", r"\bblood\s+everywhere\b", r"\bspurting\b", r"\b(?:won't|wont|doesn't)\s+stop\s+bleeding\b.{0,40}\b(?:hour|hours|pressure|bandage)\b",
    r"\b(?:stabbed|stab\s+wound)\b", r"\bdeep\s+cut\b", r"\b(?:cut|slit|sliced)\s+(?:(?:my|his|her|their|a)\s+)?(?:wrist|neck|throat|thigh)s?\b",
    r"\b(?:bleeding|blood)\s+(?:through|soaking)\s+(?:the|my)\s+(?:bandage|towel|clothes)\b",
    r"\bcan't\s+stop\s+the\s+bleeding\b",
    r"^(?!.*\b(?:nose|nostril|nosebleed|period|periods|menstrual|poo|stool|faeces|feces|wee|"
    r"urine|vomit|vomited|sick|nappy|diaper|film|films|movie|movies|tv|telly|programme|show|"
    r"episode|scene|game|games|book|novel|documentary|costume|fake|prop|ketchup|paint|"
    r"cut|cuts|cutting|gash|gashes|sliced|slices|wound|wounded|grazed|scratched)\b).*?"
    r"\b(?:a\s+lot\s+of|lots\s+of|loads\s+of|puddles?\s+of|pools?\s+of|so\s+much|"
    r"that\s+much)\s+blood\b",
    r"^(?!.*\b(?:nose|nostril|nosebleed|period|periods|menstrual|poo|stool|faeces|feces|wee|"
    r"urine|vomit|vomited|sick|nappy|diaper|film|films|movie|movies|tv|telly|programme|show|"
    r"episode|scene|game|games|book|novel|documentary|costume|fake|prop|ketchup|paint)\b).*?"
    r"(?:\b(?:the\s+)?blood\s+(?:won'?t|wont|doesn'?t|doesnt|isn'?t)\s+stopp?(?:ed|ing)?\b|"
    r"\bcan'?t\s+(?:get\s+)?(?:it|the\s+bleeding|the\s+blood)\s+to\s+stop\b)",
    r"\b(?:slash(?:ed|es|ing)?|slit)\s+(?:(?:my|his|her|their|a)\s+)?(?:arms?|wrists?|hands?|legs?|thighs?|neck|throat)\b",
)

DROWNING_HYPERBOLE = (
    r"\b(?:nearly|almost)\s+drowned\s+(?:laughing|in\s+(?:it|them|tears))\b",
    r"\bdrown(?:ing|ed)?\s+in\s+(?:paperwork|work|debt|emails?|chores|admin|deadlines?|"
    r"homework|bills|laundry|it|them|wine|beer|sorrows)\b",
    r"\bdrowned\s+(?:my|our|his|her|their)\s+sorrows\b",
)

WATER_DROWNING_NOW = (
    r"\b(?:he|she|they|hes|shes|theyre|he's|she's|they're)\b[^.?!]{0,15}\bdrown(?:ing|s)\b",
    r"\b(?:the|a|my|our)\s+(?:kid|kids|baby|child|children|boy|girl|toddler|little\s+one|son|"
    r"daughter|husband|wife|partner|mum|mom|dad|father|mother|friend|mate|brother|sister|"
    r"neighbour|neighbor|man|woman|lad|person|someone|somebody)\b[^.?!]{0,15}"
    r"\bdrown(?:ing|s)\b",
    r"\b(?:is|are)\s+drowning\b",
    r"\b(?:im|i'?m|i\s+am)\s+drowning\b[^.?!]{0,25}\b(?:water|sea|ocean|pool|lake|river|"
    r"canal|bath|bathtub|tub|waves?|deep\s+end|swimming|under\s+the\s+surface)\b",
    r"\b\d+\s+(?:year\s+old|yo)\b[^.?!]{0,15}\bdrowning\b",
)

WATER_THING_DROPPED = (
    r"\b(?:dropped|drops?|slipped|slips?|tipped|tips?|knocked|knocks?|kicked|kicks?|threw|"
    r"left|lost|dunked|dipped)\s+(?:[\w']+\s+){0,2}(?:phone|mobile|keys?|wallet|purse|watch|"
    r"glasses|book|towel|bag|coat|hat|money|passport|teddy|dummy|nappy|remote|toy|ball|boot|"
    r"trainer|tools?|sponge|cloth|loaf|bread|toast|cutlery|mug|cup)\b",
)

WATER_PERSON_TOO = (
    r"\b(?:went|goes|gone|sank|sunk|sinking|fell|fallen|falls?)\s+(?:in|into|under)\b[^.?!]{0,20}"
    r"\b(?:water|pool|sea|river|lake|pond|canal|bath)\b",
    r"\b(?:went|goes|gone)\s+under\b",
    r"\b(?:not\s+breathing|no\s+pulse|unresponsive|blue\s+lips|limp)\b",
    r"\b(?:my|his|her|their|our)\s+(?:son|daughter|child|baby|kid|boy|girl|toddler|husband|"
    r"wife|partner|friend|mate|mum|mom|dad|brother|sister)\b[^.?!]{0,25}\b(?:drowning|"
    r"drowned|under|in\s+the\s+water)\b",
)

WATER_DROWNING_FINE = (
    r"\bdrown\w*\s+(?:in\s+|under\s+)?(?:emails?|work|works|debt|debts|paperwork|admin|bills?|"
    r"tears|weeds|jobs?|chores?|stress|sorrows|booze|wine|beer|noise|it\s+all|everything|"
    r"the\s+lot|chips|gravy|ketchup|sauce|salt|vinegar|cream|syrup|oil)\b",
    r"\b(?:plant|plants|garden|lawn|grass|seedlings?|crops?|flowers?|houseplant|basil|tomato\w*|"
    r"hanging\s+basket)\b",
    r"\blaugh(?:ing|ed|s)\b",
    r"\bdrowned\s+(?:out|by\s+the\s+noise)\b",
    r"\b(?:feel|feels|felt|feeling|like)\s+(?:im|i'?m|i\s+am|like\s+im)\s+drown",
)

WATER_NOT_A_PERSON = (
    r"\b(?:roads?|streets?|garden|lawn|fields?|basement|cellar|kitchen|hall|drive|driveway|"
    r"lane|path|patio|bridge|cars?|vans?|shed|garage|town|village|pitch|allotment|"
    r"house|flat|loft|attic|cupboard)\b",
    r"\b(?:flood\w*|burst\s+pipe|leak\w*)\b",
    r"\bunder\s+(?:a|an|the)\s+(?:bus|car|lorry|truck|van|tram|train|taxi)\b",
    r"\b(?:phone|mobile|keys?|wallet|purse|watch|glasses|book|towel|shoes?|socks?|clothes|"
    r"washing|dishes|plates?|mug|cup|kettle|loaf|bread|food|dinner|rice|pasta|eggs?|toys?|ball|"
    r"dummy|nappy|ring|coin|remote|bag|coat|hat|money|passport|boot|trainer|teddy|blanket)\b"
    r"\s+(?:has\s+|had\s+)?(?:went|goes|gone|fell|falls?|slipped|drops?|dropped|is|was|got|"
    r"gets)\b",
    r"\b(?:boats?|dingh(?:y|ies)|canoes?|kayaks?|ship|ferry|raft)\b\s+(?:has\s+|had\s+)?"
    r"(?:went|goes|gone|sank|sunk|tipped|turned\s+over|capsized|is|was|got)\b",
)

WATER_SELF = (
    r"\bi\b[^.?!]{0,25}\b(?:fell|fallen|slipped|slips?|went|goes|gone|sank|sunk|jumped|dropped|"
    r"tipped|tumbled|drowned|drowning|got\s+pulled|got\s+dragged|was\s+pulled|was\s+pushed|"
    r"was\s+dragged|was\s+thrown|was\s+tipped|got\s+knocked)\b[^.?!]{0,30}\b(?:water|pond|"
    r"river|lake|sea|pool|canal|reservoir|loch|harbour|harbor|lagoon|deep\s+end|shallow\s+end|"
    r"bath|tub|under)\b",
    r"\b(?:pushed|pulled|threw|thrown|dragged|tipped|shoved|knocked)\s+me\s+(?:in|into|under)\b",
    r"\b(?:pulled|hauled|dragged|lifted|fished|got|gets)\s+me\s+out\s+of\s+the\s+(?:water|pond|"
    r"river|lake|sea|pool|canal)\b",
    r"\bi\s+(?:got|was|were|am)\s+(?:pushed|pulled|thrown|dragged|tipped|shoved|knocked)\b",
    r"\bwe\b[^.?!]{0,25}\b(?:went|goes|gone|fell|slipped|sank)\b[^.?!]{0,20}\bunder\b",
)

WATER_HUMAN = (
    r"\b(?:baby|babies|newborn|infant|son|daughter|child|children|kid|kids|boy|girl|toddler|"
    r"little\s+one|niece|nephew|grandson|granddaughter|husband|wife|partner|mum|mom|mother|dad|"
    r"father|brother|sister|friend|mate|lads?|guys?|man|woman|person|people|he|she|him|her|"
    r"them|they|someone|somebody|anyone|i|me|my\s+(?:son|daughter|child|baby|boy|girl|"
    r"husband|wife|partner|mum|mom|dad|friend|brother|sister)|we|us)\b",
)

WATER_FINE = (
    r"\b(?:swimming\s+(?:lesson|lessons|class|club|badge)|learnt?\s+to\s+swim|"
    r"learning\s+to\s+swim|splash\w*|playing|playing\s+about|having\s+fun|laughing|"
    r"came\s+up|came\s+back\s+up|popped\s+up|surfaced|came\s+to\s+the\s+surface|"
    r"loves?\s+(?:going\s+under|the\s+water)|"
    r"likes?\s+(?:going\s+under|the\s+water)|enjoys\s+the\s+water)\b",
)

WATER_HEAD_FEAR = (
    r"\b(?:can'?t|cant|cannot|couldn'?t|won'?t|wont|unable|struggl\w*|scared|afraid|"
    r"terrified|frightened|nervous|hate|hates|hated|panic\w*|refus\w*|"
    r"fear|fears|feared|fearful|phobia|phobic|dread|dreads|dreaded|dreading)\b[^.?!]{0,40}"
    r"\b(?:under\s*(?:the\s+)?(?:water|surface)|underwater|go(?:ing|es)?\s+under)\b",
    r"\b(?:put|puts|putting|get|gets|getting|duck|ducks|ducking|dip|dips|dipping|stick|"
    r"sticks|sticking|hold|holds|holding|keeping|lower\w*)\b[^.?!]{0,20}\bhead\b"
    r"[^.?!]{0,20}\b(?:under\s*(?:the\s+)?(?:water|surface)|underwater)\b",
    r"\bhead\b[^.?!]{0,20}\b(?:under\s*(?:the\s+)?(?:water|surface)|underwater)\b"
    r"[^.?!]{0,25}\b(?:swim\w*|pool|lesson\w*|bath|shower|float\w*|splash\w*)\b",
    r"\b(?:swim\w*|pool|lesson\w*|bath|shower|float\w*|splash\w*)\b[^.?!]{0,25}\bhead\b"
    r"[^.?!]{0,20}\b(?:under\s*(?:the\s+)?(?:water|surface)|underwater)\b",
    r"\b(?:scared|afraid|frightened|nervous|terrified|panic\w*|dread\w*)\s+(?:of|about|to)"
    r"\s+(?:\w+\s+){0,2}(?:jump\w*|get|getting|go|going|dive|diving|swim\w*)\s+"
    r"(?:in|into)\s+(?:the\s+)?(?:water|pool|sea|lake|deep\s+end|shallow\s+end)\b",
    r"\b(?:won'?t|wont|refus\w*|won'?t|hates?|hated)\s+(?:\w+\s+){0,2}(?:jump\w*|get|"
    r"getting|go|going|dive|diving|swim\w*)\s+(?:in|into)\s+(?:the\s+)?(?:water|pool|"
    r"sea|lake|deep\s+end|shallow\s+end)\b",
    r"\b(?:scream\w*|cry\w*|hate[sd]?|scared|afraid|frightened|terrified|nervous)\b"
    r"[^.?!]{0,30}\bwater\b[^.?!]{0,20}\b(?:face|head|hair)\b",
    r"\b(?:hold|holds|holding|held)\b[^.?!]{0,25}\b(?:my|his|her|their|your)\s+breath\b"
    r"[^.?!]{0,35}\b(?:when|whenever|every\s+time|each\s+time|before)\b[^.?!]{0,30}"
    r"\b(?:go|goes|going|went|dive\w*|dove|jump\w*|swim\w*|duck\w*|put\w*|get\w*|"
    r"stick\w*|dip\w*)\b[^.?!]{0,20}\b(?:under|underwater|in)\b",
)

WATER_IN_NOW = (
    r"\b(?:jumped|jumping|dived|diving|dove|leapt|leaped|sank|sunk|sinking)\b"
    r"[^.?!]{0,15}\b(?:in|into|under)\b",
    r"\b(?:fell|fallen|falls?|went|goes|gone|slipped|slips?|tipped|tumbled|pushed|dropped)\b"
    r"[^.?!]{0,20}\b(?:in|into)\b[^.?!]{0,20}\b(?:water|pool|sea|lake|river|canal|"
    r"pond|deep\s+end|shallow\s+end|bath)\b",
    r"\b(?:is|hes|shes|theys|they're|was|were|are|am)\s+(?:still\s+)?(?:in|under)\s+"
    r"(?:the\s+)?(?:water|pool|sea|lake|river|canal|pond|deep\s+end)\b",
    r"\b(?:went\s+under|gone\s+under|deep\s+end|shallow\s+end)\b",
)

WATER_URGENT = (
    r"\b(?:breath\w*|blue|limp|unresponsive|not\s+moving|not\s+breathing|still\s+not|"
    r"hasn'?t\s+(?:come|moved)|didn'?t\s+come|still\s+under|under\s+for|"
    r"get\s+(?:him|her|them)\s+(?:up|out)|find\s+(?:him|her|them)|"
    r"can'?t\s+(?:see|swim|get|wake)|cant\s+(?:see|swim|get|wake)|"
    r"struggl\w*|scream\w*|panic\w*|swim\s+back|swallow\w*)\b",
)

DROWNED_THING = (
    r"\b(?:drown(?:ed|ing)?)\s+(?:my|our|the|his|her|their|this|that|a)\s+"
    r"(?:plant|plants|houseplant|houseplants|seedlings?|basil|tomato(?:es)?|chillies|chilli|"
    r"flowers?|lawn|grass|garden|window\s+box|hanging\s+basket|pot\s+plant|succulent|cactus|"
    r"fern|herbs?|crops?|phone|chips|toast|cereal|salad|sorrows|cares|fears|sulks|fire)\b",
    r"\b(?:the|my|our)\s+(?:plant|plants|houseplant|seedlings?|basil|lawn|garden|flowers?|herbs?|"
    r"crops?)\b[^.?!]{0,20}\b(?:nearly\s+)?drown(?:ed|ing)?\b",
)

HANGING = (
    *PERSON_HANGING,
    r"\b(?:hung|hanged|hang|hanging)\s+(?:himself|herself|themselves|my\s*self)\b"
    r"(?!\s+(?:upside|on\s+the\s+(?:bars|swing|wall)|from\s+the\s+(?:bars|swing)|"
    r"out\s+to\s+dry|up\s+to\s+dry|the\s+(?:washing|laundry|clothes)\b))",
    r"\b(?:hung|hanged|hang|hanging)\s+(?:him|her|them)\b\s+(?:from|in|on|to)\s+(?:the\s+|a\s+)?"
    r"(?:rafters|beam|balcony|banister|railing|railings|stair(?:s|case)|ceiling|hook|tree|treehouse|"
    r"door|bridge|window|bars|shower|garage|shed|loft|basement|bathroom|bedroom)\b",
    r"\b(?:is|was|'s)\s+(?:hanging|hung)\b.{0,25}\bfound\b",
    r"\bfound\s+(?:him|her|them|my\s+\w+)\s+hanging\b",
    r"\bfound\s+(?:him|her|them|my\s+\w+)\s+strangl\w+\b",
    r"\bstrangl(?:ed|ing)\s+(?:me|him|her|them|himself|herself|themselves|someone|somebody)\b",
    r"\bstrangl(?:ed|ing)\s+(?:my|his|her|their|our)\s+" + ABUSER + r"\b",
    r"\bstrangulation\b", r"\bnoose\b",
    r"\bstrangl(?:ed|ing)\b.{0,20}\bneck\b",
    r"\b(?:ligature|rope|belt)\s+(?:round|around|tight\s+round)\s+(?:his|her|their|my)\s+neck\b",
)

SNAKE_LOOKALIKE = (
    r"\b(?:snake\s+plant|snake\s+plants|snakes?\s+and\s+ladders|snake\s+print|snake\s+skin|"
    r"snake\s+charmer|snake\s+bite\s+kit|snake\s+in\s+the\s+garden|saw\s+a\s+snake|"
    r"grass\s+snake|slow\s+worm|snake\s+in\s+(?:my|the)\s+(?:boot|shed|grass|pond))\b",
    r"\b(?:stung|bit|bitten)\s+by\s+the\s+(?:price|bill|cost|tag)\b",
)

ANIMAL_KICK = (
    r"\b(?:horse|pony|horses|cow|cows|bull|bullock|donkey|mule|llama|alpaca)\b[^.?!]{0,30}"
    r"\b(?:kicked|kick|kicks|trampled|trampling|stamped|stood\s+on|stood\s+on\s+(?:my|his|her|me))\b",
    r"\b(?:kicked|trampled|stamped\s+on|stood\s+on)\s+by\s+(?:a|an|the|my|his|her)\s*"
    r"(?:horse|pony|cow|bull|donkey|mule)\b",
)

BLIND_CORD = (
    r"\b(?:blind|blinds|curtain|curtains|venetian|roman)\s+cords?\b[^.?!]{0,25}"
    r"\b(?:neck|round|around|tangled|caught|wrapped|hanging|choking|tight)\b",
    r"\b(?:got|caught|tangled|wrapped|hanging|choking|stuck)\b[^.?!]{0,25}"
    r"\b(?:blind|curtain|venetian|roman)s?\s*cords?\b",
    r"\b(?:tangled|caught|wrapped|hanging|stuck)\s+(?:in|on|round|around)\s+the\s+"
    r"(?:blind|blinds|curtain|curtains)\b",
)

STRANGLED_SELF = (
    r"\bstrangl\w*\s+me\b",
    r"\bthrottl\w*\s+me\b",
    r"\bi\s+(?:was|got|been|have\s+been|had\s+been)\s+strangl\w+",
    r"\bi\s+(?:was|got|been)\s+throttl\w+",
    r"\bstrangled\s+by\s+(?:my|him|her|them|an?)\b",
    r"\b(?:he|she|they|someone|somebody|this\s+(?:man|woman|guy|lad|girl|bloke)|"
    r"a\s+(?:man|woman|bloke|lad|lady|girl|guy|stranger|boy)|my\b[^.?!]{0,12}\b" + ABUSER + r")"
    r"[^.?!]{0,25}\b(?:choked|chokes|is\s+choking)\s+me\b",
    r"\b(?:grab(?:s|bed|bing)?|held|holds|holding|seiz(?:ed|es|ing)|pinned|shoved|pushed)\s+me\s+by\s+"
    r"the\s+(?:throat|neck)\b",
    r"\b(?:put|puts|putting|laid|laying|lay|wrapped|wrapping|wraps|had|has|slid|slipped|clamped|"
    r"locked|forced)\s+(?:his|her|their|both)\s+"
    r"(?:hands?|fingers|fist|forearm)\s+(?:round|around|on|across|to)\s+my\s+(?:throat|neck)\b",
    r"\b(?:put|puts|putting|wrapped|wrapping|wraps|threw|had|got|slid|slipped|clamped)\s+"
    r"(?:his|her|their|both)\s+arms?\s+(?:round|around|on|across)\s+my\s+throat\b",
    r"\b(?:a\s+hand|his\s+hands?|her\s+hands?|their\s+hands?|someone'?s\s+hands?|"
    r"somebody'?s\s+hands?)\s+(?:round|around|on|across)\s+my\s+throat\b",
    r"\b(?:a\s+hand|his\s+hands?|her\s+hands?|their\s+hands?|someone'?s\s+hands?|"
    r"somebody'?s\s+hands?)\s+(?:round|around)\s+my\s+neck\b",
    r"\b(?:a\s+hand|his\s+hands?|her\s+hands?|their\s+hands?|someone'?s\s+hands?|"
    r"somebody'?s\s+hands?)\s+(?:on|across)\s+my\s+neck\b"
    r"(?=[^.?!]{0,30}\b(?:tight(?:ly|en\w*)?|grip\w*|squeez\w*|press\w*|pin(?:ned|ning|s)?|"
    r"clamp\w*|hard|crush\w*|chok\w*)\b)",
    r"\bstrangl(?:ed|ing|es|e)\s+my\s+(?:neck|throat)\b",
    r"\bchok(?:ed|ing|es)\s+my\s+(?:neck|throat)\b",
    r"\b(?:nearly|almost)\s+(?:got|was|been|had\s+me)\s+(?:strangled|throttled|choked)\b",
)

STRANGLE_THING_SUBJECT = (
    r"\b(?:the|this|that|my|our|his|her|their)\s+(?:[a-z']+\s+){0,2}(?:jeans|trousers|shirt|top|"
    r"bra|shoes?|boots|socks?|belt|watch|coat|jumper|hoodie|heat|humidity|workload|work|job|"
    r"debt|debts|bills?|traffic|stress|anxiety|panic|pressure|paperwork|bureaucracy|admin|"
    r"commute|queue|noise|mortgage|rent|council|kids?|in-?laws?|exams?|revision|"
    r"deadlines?|red\s+tape|system|money|poverty|town|city|weather)\b[^.?!]{0,20}"
    r"\bstrangl(?:e|es|ing|ed)\b",
    r"\b(?:jeans|trousers|shirt|bra|heat|humidity|workload|work|job|debt|bills?|traffic|stress|"
    r"anxiety|panic|pressure|paperwork|bureaucracy|admin|commute|queue|noise|mortgage|rent|"
    r"council|kids|in-?laws|exams?|revision|deadlines?|red\s+tape|system|money|poverty|"
    r"life|everything)\b(?:\s+[a-z']+){0,2}\s+(?:is|are|was|were|keeps?)\s+strangl(?:ing|ed)\b",
)

KICKED_PERSON = (
    r"\b(?:kicked|kicks?|trampled|trampling|stamped\s+on|stood\s+on)\s+(?:me|us|my|our)\b",
    r"\b(?:i|we)\s+(?:was|were|got|have\s+been|had\s+been|'ve\s+been)\b[^.?!]{0,25}"
    r"\b(?:kicked|trampled|stamped\s+on|stood\s+on|sat\s+on|thrown|tossed)\b",
    r"\b(?:my|his|her|their|our)\s+(?:son|daughter|child|kid|baby|boy|girl|husband|wife|partner|"
    r"mum|mom|mother|dad|father|brother|sister|friend|nan|gran|grandad|grandma)\b[^.?!]{0,25}"
    r"\b(?:was|were|got|had\s+been)\b[^.?!]{0,15}\b(?:kicked|trampled|stamped\s+on|stood\s+on)\b",
)

SELF_CUT = (
    r"\b(?:cut|cutting|sliced|slashed|gashed|slit|nicked|scratched)\s+"
    r"(?:my\s*self|my\s+(?:arm|arms|wrist|wrists|hand|hands|leg|legs|thigh|thighs|finger|"
    r"fingers|foot|feet))\b",
    r"\b(?:i\s+)?(?:keep|keeps|kept|am|im|'m)\s+(?:on\s+)?cutting\b",
)

CUT_NOT_STOPPING = (
    r"\b(?:won'?t|wont|doesn'?t|doesnt|didn'?t|didnt|not|never|keeps?)\s+stop(?:ped|ping)?\s+"
    r"(?:bleeding|blood|the\s+blood)\b",
    r"\b(?:the\s+)?blood\s+(?:wont|won'?t|doesnt|doesn'?t)\s+stop\b",
    r"\bblood\s+(?:everywhere|every\s*where|a\s+lot|lots|badly|heavily|pouring)\b",
    r"\bsoaking\s+(?:through|the)\b",
)

GAS_ON_YOU = (
    r"\b(?:my|his|her|their|your|the)\s+(?:hands?|clothes|shirt|coat|jumper|fingers|gloves|cloths?)\b"
    r"[^.?!]{0,25}\b(?:smell|smells|smelling|smelt|reek|reeks|stink|stinks)\b",
    r"\b(?:smell|smells|smelling|smelt)\s+(?:of\s+|like\s+)?gas\b"
    r"[^.?!]{0,20}\b(?:on|from)\s+(?:my|his|her|their|your)\s+"
    r"(?:hands?|clothes|shirt|coat|jumper|fingers|gloves)\b",
)

GAS_ON_NOT_RUNNING = (
    r"(?!\s+(?:the\s+)?(?:table|side|counter|worktop|shelf|floor|bed|sofa|desk|hook|wall|windowsill|"
    r"ledge|rack|top\s+shelf|board|tray|plate|doorstep))"
    r"(?!\s+(?:for|to\s+keep)\s+(?:the\s+)?(?:boiler|pilot|pilot\s+light|heating|hot\s+water|"
    r"water|radiators?|fire|shower|bath|oven|cooker|fridge|freezer|central\s+heating))\b"
)

GAS_LEFT_ON = (
    r"\b(?:left|leave|leaving|forgot|forgotten|think\s+i\s+(?:left|turned))\b[^.?!]{0,30}"
    r"\b(?:gas|hob|burner|ring|cooker)\b[^.?!]{0,12}\bon\b" + GAS_ON_NOT_RUNNING,
    r"\b(?:turned|switched|put)\s+(?:the\s+)?(?:gas|hob|burner|ring|cooker)\b[^.?!]{0,15}"
    r"\b(?:on|up)\b[^.?!]{0,25}\b(?:forgot|forgotten|walked\s+away|left\s+it)\b",
    r"\b(?:did|have|had)\s+(?:i|you|we)\s+\b(?:leave|left)\b[^.?!]{0,20}\b(?:gas|hob|burner|cooker)\b"
    r"[^.?!]{0,10}\bon\b" + GAS_ON_NOT_RUNNING,
    r"\b(?:gas|hob|burner|ring\s+on\s+the\s+cooker)\b[^.?!]{0,20}\b(?:is\s+)?(?:still\s+)?on\b"
    r"[^.?!]{0,30}\b(?:cant|cannot|can'?t|not\s+sure|no\s+idea|don'?t\s+know)\b",
    r"\b(?:gas|hob|burner)\b[^.?!]{0,20}\b(?:hissing|running|going\s+and\s+i)\b",
)

GAS_PAST = (
    r"\b(?:smelt|smelled|smelling|smell)\b[^.?!]{0,40}\b(?:last\s+(?:year|week|month|winter|summer)|"
    r"years?\s+ago|months?\s+ago|weeks?\s+ago|yesterday|ages\s+ago|once|when\s+i\s+was|"
    r"as\s+a\s+kid|at\s+(?:my|her|his|our)\s+\w+'s)\b",
    r"\b(?:last\s+(?:year|week|month)|years?\s+ago|when\s+i\s+was|ages\s+ago)\b[^.?!]{0,30}"
    r"\b(?:smelt|smelled|smell)\b",
)

INTRUDER = (
    r"\b(?:someone|somebody|a\s+man|a\s+person|intruder|burglar)\s+(?:is\s+)?(?:trying\s+to\s+get\s+in|"
    r"breaking\s+in|breaking\s+into\s+(?:the|my|our)\s+(?:house|flat|home|kitchen|bedroom)|climbing\s+(?:in|through|over)|"
    r"in\s+(?:the|my)\s+(?:house|flat|home|garden|kitchen|living\s+room)|inside\s+(?:the|my)\s+house)\b",
    r"\b(?:there's|there\s+is|theres)\s+(?:someone|somebody|a\s+man)\s+(?:in|inside|at)\s+(?:the|my)\s+"
    r"(?:house|flat|home|garden|window)\b"
    r"(?!\s+(?:with|holding|delivering)\s+(?:a|the|my)\s+(?:parcel|package|delivery|letter|clipboard|"
    r"takeaway|pizza|parcels))",
    r"\b(?:a\s+man|someone|somebody)\s+(?:is\s+)?following\s+me\b(?!\s+(?:on|around)\s+"
    r"(?:instagram|insta|twitter|x|tiktok|facebook|snapchat|social|the\s+internet|online))",
    r"\b(?:someone|somebody|a\s+man)\s+(?:is\s+)?(?:banging|pounding|kicking|hammering|smashing)\s+"
    r"(?:on\s+)?(?:the|my)\s+(?:door|window)\b",
    r"\b(?:someone|somebody|a\s+man|he|she|they)(?:'s|\s+is)?\s+(?:trying|tried)\s+to\s+"
    r"(?:get\s+in|break\s+(?:in\b(?!\s+(?:his|her|their|my|your|these|those|new|a\s+new)\s)|"
    r"the\s+door|down\s+the\s+door))\b",
    r"\b(?:i\s+think|i\s+heard)\s+(?:someone|somebody)\s+(?:is\s+)?(?:in|inside|downstairs|upstairs)\b",
)

GASPING_THIRST = (
    r"\bgasping\s+(?:for|at)\s+(?:" + _A_THIRST + r")",
    r"\bgasping\s+(?:for|at)\s+(?:something\s+to\s+drink|something\s+to\s+eat)\b",
    r"\bgasping\s+(?:after|during|at)\s+(?:a\s+|that\s+|the\s+|my\s+)?(?:run|jog|workout|gym|"
    r"session|match|game|swim|cycle|bike\s+ride|climb|hill|walk|climbing|going\s+up|running)\b",
    r"\bgasp\w*\s+(?:for|on)\s+(?:fuel|petrol|diesel|power|charge|bandwidth|data)\b",
)

EXERTION = (
    r"\b(?:after|during|while|when|whenever)\s+(?:a\s+|the\s+|my\s+)?(?:run|running|jog|jogging|gym|"
    r"workout|exercise|exercising|cycling|ride|swim|swimming|walk|walking|football|netball|climbing|"
    r"lifting|weights|stairs|cardio)\b",
    r"\b(?:after|during|while|when|whenever)\s+(?:im|i'm|ive|i've|were|we're|hes|he's|shes|"
    r"she's|theyre|they're)\s+"
    r"(?:run|running|jog|jogging|gym|workout|exercis\w*|cycl\w*|rid(?:e|ing)|swim\w*|walk\w*|"
    r"climb\w*|lift\w*|play\w*|football|netball|squash|tennis|stairs|cardio|train\w*|row\w*|"
    r"hik\w*|danc\w*|aerobics|hiit|spinning|weights?|press-?ups?|squats)\b",
    r"\b(?:after|during|while|when|whenever)\s+(?:i|we|he|she|they|my\s+\w+)\s+"
    r"(?:am\s+|'m\s+|is\s+|was\s+|are\s+|start\s+|do\s+|play\s+|go\s+|come\s+)?"
    r"(?:run|running|jog|gym|workout|exercis\w*|cycl\w*|rid(?:e|ing)|swim\w*|walk\w*|climb\w*|"
    r"lift\w*|play\w*|football|netball|squash|tennis|stairs|cardio|train\w*|row\w*|hik\w*|"
    r"danc\w*|aerobics|hiit|spinning|weights?|press-?ups?|squats)\b",
    r"\b(?:going|walking|running)\s+up\s+(?:the\s+)?(?:stairs|hill)\b",
    r"\b(?:going|walking|running)\s+(?:up\s+)?upstairs\b",
    r"\b(?:on|up|down|going\s+up)\s+(?:the\s+|some\s+)?(?:stairs|hill|upstairs)\b",
)

BREATH_CAUSE = (
    r"\b(?:nose|nostrils?|blocked|bunged|stuffed|congestion|congested|hayfever|hay\s+fever|"
    r"sinus\w*|blocked\s+up)\b",
    r"\b(?:a|this|that|the|my|your|his|her|stinking|rotten|bad|nasty|heavy|terrible|awful|"
    r"horrible|proper|real|slight|streaming|head|chest|summer|winter|24\s?hour)\s+cold\b",
    r"\b(?:got|have|had|caught|catch|fighting|coming\s+down|full\s+of)\s+(?:a\s+|the\s+|this\s+)?"
    r"cold\b",
    r"\b(?:flu|virus|flu\s+bug)\b[^.?!]{0,30}\b(?:nose|blocked|bunged|stuffed|congestion|"
    r"congested|sinus\w*)\b",
    r"\bchesty\b",
)

BREATH_SHORT = (
    r"\b(?:short|out)\s+of\s+(?:breath|puff)\b",
    r"\bbreathless\b",
    r"\bpuffed\s+out\b",
    r"\b(?:struggling|struggle|hard|harder|difficult\w*|trouble)\b[^.?!]{0,18}\bbreath\w*\b",
    r"\b(?:can'?t|cannot|can\s+not)\s+breath\w*\b",
    r"\bbreathing\s+(?:heavily|hard)\b",
)

EXERTION_SMALL = (
    r"\b(?:on|up|down|climbing|walking\s+up|going\s+up)\s+(?:the\s+|a\s+|some\s+)?"
    r"(?:stairs|staircase|steps|hill|slope|hillock)\b",
    r"\b(?:going|walking|running|coming)\s+upstairs\b",
    r"\b(?:walk\w*|stroll\w*|potter\w*|get(?:ting)?)\s+(?:to\s+|into\s+)?(?:the\s+)?"
    r"(?:shops?|shop|bus|station|school|work|village|town)\b",
    r"\b(?:small|short|little|gentle)\s+(?:walk|walks|effort|hill|stroll)\b",
    r"\b(?:a|one|two|three)\s+flights?\s+of\s+stairs\b",
    r"\b(?:after|on|from)\s+the\s+stairs\b",
    r"\b(?:the|some)\s+stairs\b",
    r"\b(?:walking|walked|went|going)\s+up\s+(?:the\s+|a\s+)?(?:hill|slope)\b",
    r"\b(?:getting|get|got)\s+dressed\b",
    r"\b(?:around|round)\s+the\s+(?:house|garden|park)\b",
)

MEAL_BREATH = (
    r"\b(?:after|before|when|while)\s+(?:i\s+|she\s+|he\s+|they\s+)?(?:eating|a\s+(?:big\s+|"
    r"heavy\s+|large\s+|huge\s+|proper\s+)?meal|dinner|lunch|breakfast|tea)\b",
    r"\b(?:eating|a\s+meal|dinner|lunch|breakfast)\b[^.?!]{0,20}\b(?:breath|puffed|winded)\w*\b",
    r"\b(?:short|out)\s+of\s+(?:breath|puff)\b[^.?!]{0,20}\b(?:eat|eating|meal|dinner|lunch)\b",
)

EFFORT_ANYWHERE = (
    r"\b(?:run|runs|running|jog\w*|gym|workout|exercis\w*|cycl\w*|swim\w*|football|netball|squash|"
    r"tennis|cardio|stairs|hills?|climb\w*|walk\w*|hike|hiking|danc\w*|hiit|weights?|press-?ups?|"
    r"squats|spin|rowing|skipping|badminton|rugby|cricket|climbing|box\w*|class|classes|"
    r"session|ran|singing|sing|laughing|talking|carrying|shopping|cleaning|"
    r"hoovering|garden\w*|digging)\b",
)

SHORT_OF_BREATH = (
    r"\b(?:out\s+of|short(?:ness)?\s+of)\s+breath\b",
    r"\b(?:still|now|very|quite|really|so|a\s+bit|a\s+little|always|already)\s+"
    r"(?:out\s+of|short(?:ness)?\s+of)\s+breath\b",
)

A_BREATHER = (
    r"\b(?:i|me|we|us|he|him|she|they|them|you|husband|wife|partner|"
    r"boyfriend|girlfriend|mum|mom|mother|dad|father|son|daughter|baby|child|kid|nan|gran|"
    r"grandma|grandad|brother|sister|friend|man|woman|boy|girl|patient|neighbour|neighbor|"
    r"dogs?|cats?|pupp(?:y|ies)|kittens?|pets?|parrot|hamster|rabbit)\b",
)

BREATH_RED = (
    r"\b(?:blue|lips?|can'?t\s+speak|cannot\s+speak|unable\s+to\s+speak|at\s+rest|resting|in\s+bed|"
    r"woke\s+me|sudden\w*|getting\s+worse|chest\s+pains?|"
    r"chest\b[^.!?]{0,20}\b(?:hurt\w*|tight\w*|pressure|heav\w*|squeez\w*)|"
    r"(?:tight\w*|pressure|heavy|heaviness)\b[^.!?]{0,15}\bchest\b|swell\w*|anaphyla\w*|epipen|wheez\w*|"
    r"asthma\s+attack|\basthma\b[^.!?]{0,15}\b(?:bad|badly|worse|severe|uncontrolled|out\s+of\s+control)\b|"
    r"inhaler\b[^.!?]{0,25}\b(?:not\s+working|isn'?t\s+working|isn'?t\s+helping|not\s+helping)\b|"
    r"stopped\s+breathing|isn'?t\s+breathing|not\s+breathing|gasping|coughing\s+up|blood)\b",
)

BREATH_CAUSE_RED = BREATH_RED + (
    r"\basthma\b", r"\binhaler\b", r"\bwheez\w*", r"\bchest\b", r"\btongue\b",
    r"\bstridor\b", r"\bcroup\b",
    r"\bthroat\b[^.?!]{0,20}\b(?:clos\w*|swell\w*|tight\w*|shut|seal\w*)\b",
    r"\b(?:clos|swell|tight)\w*\s+(?:up\s+)?(?:in\s+|of\s+)?(?:my\s+|the\s+|his\s+|her\s+)?"
    r"throat\b",
    r"\bcant\s+swallow\b", r"\bcan'?t\s+swallow\b", r"\bdifficulty\s+swallowing\b",
    r"\bswallow(?:ing)?\s+(?:is\s+)?(?:hard|painful\s+and\s+getting\s+worse)\b",
    r"\b(?:feel(?:ing)?|am|im|so|very|really|freezing|frozen|shivering|shivery|shivers|bit)\s+"
    r"cold\b",
    r"\bcold\s+(?:and|or)\s+(?:shivering|shivery|clammy|sweating|weak|floppy|confused)\b",
    r"\bcold\s+to\s+(?:the\s+)?touch\b",
)

HUMAN_TOO = (
    r"\b(?:my|our|her|his|their)\s+(?:son|daughter|child|kid|baby|boy|girl|mum|mom|dad|father|mother|"
    r"husband|wife|partner|brother|sister|nan|gran|grandma|grandad|friend|neighbour|neighbor)\b",
    r"\b(?:i|i'm|im|he|she|they|we|you|someone|somebody)\b[^.?!]{0,12}"
    r"\b(?:can'?t|cannot|can\s+not|couldn'?t|struggling\s+to|unable\s+to)\s+"
    r"(?:breath\w*|(?:get|catch)\s+(?:my|his|her|their|our|a)\s+breath\w*|wake\s+up|stay\s+awake)",
    r"\b(?:i|i'm|im|he|she|they|we)\b[^.?!]{0,10}\b(?:am|is|are|'m|'s|'re|was|were)\s+"
    r"(?:bleeding|unconscious|unresponsive|collapsed|choking)\b",
    r"\b(?:im|i'm)\s+(?:bleeding|unconscious|unresponsive|collapsed|choking)\b",
)

PET_PAST = (
    r"\b(?:last|this)\s+(?:year|month|week)\b", r"\byears\s+ago\b", r"\bages\s+ago\b",
    r"\bwhen\s+(?:he|she|it|they)\s+(?:\w+\s+){0,3}(?:was|were)\s+(?:a\s+)?(?:puppy|kitten|young)\b",
    r"\bused\s+to\b",
    r"\bevery\s+(?:few\s+)?(?:days?|weeks?|months?|years?)\b",
    r"\bis\s+that\s+(?:normal|usual|common)\b",
)

PET_GASP_FINE = (
    r"\bgasp\w*\b[^.?!]{0,30}\b(?:after|from|during|when(?:ever)?|on|in)\b[^.?!]{0,25}"
    r"\b(?:walk|run|runn\w*|plays?|playing|played|exercis\w*|fetch|ball|games?|zoomies|"
    r"chas\w*|charged|park|garden|hill|stairs|beach|frisbee|swim\w*|train\w*)\w*\b",
    r"\bgasp\w*\b[^.?!]{0,25}\b(?:in|from)\s+(?:the|this|that)\s+(?:heat|sun|hot\s+weather|warmth)\b",
    r"\bgasp\w*\s+at\s+(?:the|a|an|his|her|its|their|my|other|next)\b",
    r"\b(?:in|on|during)\s+(?:the|a|his|her|its|their)\s+(?:car|drive|journey|train|bus)\b",
    r"\bgasp\w*\b[^.?!]{0,15}\b(?:a\s+bit|a\s+little|slightly)\b",
    r"\bgasp\w*\s+(?:for|after)\s+(?:(?:a|an|the|some|its|his|her|their|my)\s+)?"
    r"(?:a\s+)?(?:drink|water|food|biscuit|treat|dinner|tea)\b",
)

PET_GASP_EXPLAINED = (
    r"\bgasp\w*\b[^.?!]{0,40}\bwhen\s+(?:he|she|it|they)(?:'?s|s|\s|\b)",
    r"\bgasp\w*\b[^.?!]{0,40}\b(?:because|whenever|every\s+time)\b",
    r"\b(?:sneez\w*|cough\w*|hiccup\w*|laugh\w*|retch\w*|splutter\w*|purr\w*)\b"
    r"[^.?!]{0,25}\bgasp\w*\b",
    r"\bgasp\w*\b[^.?!]{0,30}\b(?:on|off)\s+the\s+lead\b",
    r"\bgasp\w*\b[^.?!]{0,30}\bafter\s+(?:a\s+|an\s+|the\s+|his\s+|her\s+|its\s+|their\s+|"
    r"our\s+|my\s+)?(?:drink\w*|water|food|meal|dinner|tea|breakfast|eating|ate|gulping|"
    r"too\s+fast|too\s+quickly)\b",
)

PET_GASP_RED = (
    r"\bcan'?t\s+breathe\b", r"\bnot\s+breathing\b", r"\bblue\b", r"\bpale\b",
    r"\bunconscious\b", r"\bchok\w*", r"\bcollaps\w*", r"\bwoke\s+up\b", r"\bwakes?\s+up\b",
    r"\bkept?\s+waking\b", r"\blimp\b",
    r"\bstill\b", r"\bfor\s+(?:\d+|a\s+few|ten|twenty|half\s+an?\s+hour)\b",
    r"\bgums?\b", r"\bbright\s+red\b", r"\b(?:grey|gray|white)\s+gums?\b",
)

HEAD_BANG = (
    r"\b(?:bang|bangs|banged|banging|hit|hits|hitting|knock|knocks|knocked|knocking|strike|struck|"
    r"smack(?:s|ed|ing)?|crack(?:s|ed|ing)?|bump(?:s|ed|ing)?|bashed?|bashing|smashed?|smashing|"
    r"slammed?)\s+"
    r"(?:my|his|her|their|the|me\s+in\s+the|him\s+in\s+the|her\s+in\s+the|on\s+the|in\s+the)\s+head\b",
    r"\bhead\s+(?:injury|injuries|trauma|wound)\b",
    r"\b(?:got|gets|getting)\s+(?:hit|struck|clipped|caught|banged)\s+(?:on|in)\s+the\s+head\b",
    r"\bhit\s+(?:on|in)\s+the\s+head\s+(?:by|with)\b",
    r"\b(?:fell|fallen|fall|falls|tripped|slipped|toppled|tumbled)\s+(?:over|down|off|from|onto|on\s+to)\b"
    r".{0,25}\bhead\b",
    r"\bhead\s+(?:first|hit|banged|struck)\s+(?:on|into|off|against)\b",
)

OUT_COLD_PERSON = (
    r"\b(?:i|he|she|they|we|you)\b[^.?!]{0,15}\bout\s+cold\b",
    r"\b(?:my|his|her|their|our|your|the)\s+" + PERSON + r"\b[^.?!]{0,20}\bout\s+cold\b",
    r"\b(?:out\s+cold)\b[^.?!]{0,20}\b(?:floor|ground|sofa|couch|bed|street|pavement|road|"
    r"bathroom|kitchen|hospital)\b",
    r"\b(?:fell|fallen|collapsed|dropped|banged|hit|knocked|tripped)\b[^.?!]{0,25}"
    r"\bout\s+cold\b",
)

HEAD_KNOCKOUT = (
    r"\b(?:was|were|been|got|gets|getting|being|had|has)\s+knocked\s+out\b(?!\s+(?:of|in|by)\b)",
    r"\bknocked\s+(?:him|her|them|my\s*self|him\s*self|her\s*self)\s*out\b",
    *HEAD_OUT_COLD,
    r"\bout\s+cold\b[^.?!]{0,20}\b(?:floor|ground|street|pavement|road|bathroom|kitchen|"
    r"hospital)\b",
)

TOOTH_OUT_FINE = (
    r"\bmilk\s+tooth\b", r"\bbaby\s+tooth\b", r"\bwobbly\b", r"\bloose\s+tooth\b",
    r"\btooth\s+fairy\b", r"\btoothache\b", r"\b(?:last|this)\s+(?:year|month|week)\b",
    r"\byears?\s+ago\b", r"\bwhen\s+i\s+was\s+(?:a\s+)?(?:kid|child|little)\b",
    r"\b(?:hole|socket|gap)\b[^.?!]{0,25}\btooth\b", r"\btooth\b[^.?!]{0,25}\b(?:hole|socket)\b",
    r"\bwhere\s+(?:my|his|her|their)\s+tooth\s+(?:came|fell|was)\b",
    r"\bgum\b[^.?!]{0,30}\b(?:tooth|teeth)\b",
    r"\bcrowns?\b",
    r"\b(?:son|daughter|kid|child|children)'?s?\s+(?:front\s+|back\s+|adult\s+|baby\s+|milk\s+)?"
    r"(?:tooth|teeth)\b[^.?!]{0,10}\b(?:came|fell)\s+out\b",
)

PET_TOOTH = (
    r"\b(?:my|our|his|her|their|the)\s+(?:\w+\s+){0,2}"
    r"(?:cat|cats|dog|dogs|puppy|puppies|kitten|kittens|rabbit|rabbits|bunny|bunnies|hamster|"
    r"guinea\s+pig|horse|pony|parrot|ferret|gerbil|rat|mouse|tortoise|snake|lizard|pup)\b"
    r"[^.?!]{0,40}\b(?:tooth|teeth|tusk|beak)\b",
    r"\b(?:tooth|teeth|tusk)\b[^.?!]{0,25}\b(?:of|from)\s+(?:my|our|the)\s+"
    r"(?:cat|dog|puppy|kitten|rabbit|hamster|horse|parrot)\b",
    r"\b(?:cat|dog|puppy|kitten|rabbit|hamster|horse|parrot)'?s\s+"
    r"(?:\w+\s+){0,2}(?:tooth|teeth|tusk)\b",
)

HEAD_RED = (
    r"\bknock(?:ed|s)?\s+(?:him|her|them|my\s*self|him\s*self|her\s*self)?\s*out\b",
    r"\b(?:was|were|been|got|had|being)\s+knocked\s+out\b", *OUT_COLD_PERSON,
    r"\bunconscious\b", r"\bpassed\s+out\b", r"\bblacked\s+out\b", r"\bkeeled\s+over\b",
    r"\bconfus(?:ed|ion)\b(?!\s+about\s+(?!where\b|who\b|how\b))", r"\bdidn'?t\s+know\s+(?:where|who)\b",
    r"\b(?:not|isn'?t|isnt|ain'?t|wasn'?t|doesn'?t)\s+making\s+sense\b",
    r"\b(?:talking|chatting)\s+(?:rubbish|nonsense|gibberish)\b",
    r"\bslurr\w*\b", r"\bdouble\s+vision\b",
    r"\bpupils?\b.{0,15}\b(?:different|unequal|dilated|blown|one\s+(?:bigger|smaller|larger))\b",
    r"\bdrows(?:y|iness|ily)?\b", r"\b(?:very|really|so)\s+sleepy\b", r"\bcan'?t\s+(?:wake|stay\s+awake)\b",
    r"\b(?:keep|keeps|kept)\s+(?:on\s+)?(?:dozing(?:\s+off)?|nodding\s+off|drifting\s+off|"
    r"falling\s+asleep|zonking\s+out)\b",
    r"\b(?:dozing|nodding|drifting|zonking)\s+(?:off|out)\b",
    r"\bcan'?t\s+keep\s+(?:my|his|her|their)?\s*eyes\s+open\b",
    r"\b(?:feel|feels|feeling|felt)\s+(?:a\s+bit\s+|really\s+|very\s+|so\s+)?"
    r"(?:sleepy|drowsy|confused|not\s+with\s+it)\b",
    r"\b(?:being|been|keeps?)\s+sick\b", r"\bvomit\w*\b", r"\b(?:throw(?:ing|n)?|threw)\s+up\b",
    r"\b(?:was|were|got|gets|getting|kept)\s+(?:a\s+bit\s+|really\s+|very\s+)?sick\b",
    r"\bfaint(?:ed|s|ing)?\b", r"\bseizure\b", r"\b(?:having|had)\s+a\s+fit\b",
    r"\b(?:is|was|were|had|has|kept)\s+fitting\b(?!\s+(?:in|on|into|his|her|their|my|your|the|a)\b)",
    r"\bbleed(?:ing)?\s+(?:from|out\s+of)\s+(?:the\s+|his\s+|her\s+)?ears?\b",
    r"\bclear\s+fluid\b", r"\bwarfarin\b", r"\bblood\s+thinners?\b", r"\bclopidogrel\b",
    r"\b(?:worse|worst)\s+headache\b", r"\bheadache\s+(?:is\s+)?(?:getting|getting\s+)\s+worse\b",
    r"\bneck\s+(?:is\s+)?stiff\b", r"\bcan'?t\s+move\s+(?:my|his|her)\s+neck\b",
)

FALL_WORD_IDIOM = (
    r"\b(?:slip|slips|slipped|slipping)\s+up\b",
    r"\btrip(?:s|ped|ping)?\s+over\s+(?:my|his|her|their|your|our)\s+(?:words|tongue)\b",
    r"\b(?:fall|fell|falling)\s+(?:out|in)\s+with\b",
    r"\b(?:fall|fell|falling)\s+(?:out|owt)\s+(?:wi|wiv|wid|with|over|about)\b",
)

PET_ALL_RIGHT = (
    r"\b(?:but|and|though|although|except|only)\b.{0,40}\b(?:fine|ok|okay|alright|all\s+right|"
    r"normal|himself|herself|no\s+different|not\s+himself)\b",
    r"\b(?:seems?|looks?|appears?)\s+(?:fine|ok|okay|alright|normal|himself|herself)\b",
    r"\b(?:he|she|it|they|hes|shes|its|theyre)(?:'s|s)?\s+(?:is|are)?\s*"
    r"(?:fine|ok|okay|alright|normal)\b",
    r"\bjust\s+(?:ate|eaten|had\s+a\s+(?:big\s+)?meal|a\s+big\s+meal|tired|sleeping|"
    r"worn\s+out|getting\s+old|old|woken\s+up|having\s+a\s+lazy\s+day)\b",
    r"\b(?:1[0-9]|[2-9][0-9])\s*(?:years?\s+old|and\s+stiff|now)\b|\b(?:is|getting)\s+(?:old|stiff)\b",
    r"\bstiff\s+(?:in\s+the\s+morning|first\s+thing)\b",
    r"\b(?:the\s+)?vet\s+(?:said|says|told|checked|has\s+seen|saw|thinks?)\b",
)

PET_RESPOND_AT = (r"(?!\s+(?:to|for|when|if)\b[^.?!]{0,30}\b(?:i|we|me|us|him|her|them|my|our|"
                  r"voice|calling|call|calls|say|says|said|speak|talk|asks?|asked|names?|"
                  r"treats?|food|dinner|toys?|recall|commands?|laser|catnip|nip|clicker|"
                  r"whistle|lead|ball|kibble|chews?|train\w*|housetrain\w*|sits?|stays?|heels?|"
                  r"tricks?|classes?|obedience|sessions?|cues?)\b)")

CHOKE_OVER = (
    r"\bchoked\b.{0,40}\b(?:at\s+(?:lunch|dinner|breakfast)|yesterday|last\s+night|this\s+morning|"
    r"earlier|a\s+while\s+ago|years\s+ago|ages\s+ago|once|before|again|last\s+year|"
    r"last\s+week|last\s+month|months?\s+ago|when\s+i\s+was\s+(?:a\s+)?(?:kid|child|little|"
    r"young|small)|as\s+a\s+(?:kid|child|baby|teen|little\s+one))\b",
    r"\bchoked\b[^.?!]{0,30}\bin\s+(?:19|20)\d\d\b",
    r"\b(?:used\s+to|always)\s+choke\b",
)

CHRONIC_BREATH = (
    r"\b(?:for|going\s+on\s+for|over\s+the\s+(?:last|past))\s+"
    r"(?:about\s+|nearly\s+|almost\s+|over\s+)?(?:\d+|one|two|three|four|five|six|seven|eight|"
    r"nine|ten|a|an|a\s+few|a\s+couple\s+of|several|many|last)\s+"
    r"(?:day|days|week|weeks|month|months|year|years)\b",
    r"\bfor\s+(?:the\s+)?(?:last\s+|past\s+|few\s+|several\s+|a\s+few\s+|a\s+couple\s+of\s+)?"
    r"(?:days|weeks|months|years)\b",
    r"\b(?:it'?s|its|it\s+has|this\s+has)\s+been\s+(?:like\s+this\s+|going\s+on\s+)?"
    r"(?:about\s+|nearly\s+|over\s+)?(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|a|an|"
    r"a\s+few|a\s+couple\s+of|several|many)\s+(?:day|days|week|weeks|month|months|year|years)\b",
    r"\bsince\s+(?:last\s+)?(?:christmas|new\s+year|the\s+summer|the\s+holidays|easter|then|"
    r"march|april|may|june|july|august|september|october|november|december)\b",
    r"\bthese\s+(?:last|past)\s+(?:few\s+|couple\s+of\s+|several\s+)?(?:days|weeks|months)\b",
)

NIGHT_BREATH_OTHER = (
    r"\b(?:my|our|his|her|their)\s+(?:mum|mom|mother|dad|father|son|daughter|baby|child|kid|"
    r"boy|girl|partner|husband|wife|brother|sister|gran|granny|nan|grandma|grandad|grandpa|"
    r"friend|neighbour|neighbor|flatmate|roommate|niece|nephew|aunt|uncle)s?\b",
    r"\b(?:he|she|they)\s+(?:woke|woken|has\s+woken|had\s+woken)\b",
)

NIGHT_BREATH_PAST = (
    r"\A(?!.*?(?:" + "|".join(NIGHT_BREATH_OTHER) + r"))"
    r"(?![^.?!]*\bfor\s+(?:breath|air)\b)"
    r".*?\b(?:woke|woken)\s+up\b[^.?!]{0,40}\b(?:breath\w*|gasp\w*)\b",
)

NIGHT_BREATH_RED = (
    r"\b(?:can'?t|cannot|can\s+not|unable\s+to|struggling\s+to)\s+breath\w*\b|"
    r"\b(?:blue|lips?|can'?t\s+speak|cannot\s+speak|chest\s+pains?|right\s+now|at\s+the\s+moment|"
    r"as\s+we\s+speak|just\s+happened|a\s+minute\s+ago|still|getting\s+worse|stopped\s+breathing|"
    r"not\s+breathing|isn'?t\s+breathing|asthma\s+attack|wheez\w*|blood|anaphyla\w*|epipen|"
    r"swell\w*)\b",
)

TALK_HABIT = (
    r"\b(?:when|whenever|while|after|if)\s+(?:i|we)\s+(?:talk|talks|speak|sing|read|laugh|shout|"
    r"chat)\b[^.!?]{0,20}\b(?:for\s+(?:a\s+long\s+time|a\s+while|ages|long|hours)|a\s+lot)\b",
    r"\b(?:talk|talking|sing|singing|read|reading|laugh|laughing)\w*\s+(?:for|over)\s+"
    r"(?:a\s+long\s+time|a\s+while|ages)\b",
    r"\b(?:out\s+loud|aloud|by\s+heart)\b",
)

BREATH_LAUGH = (
    r"\b(?:when|whenever|while|after|from|every\s+time|each\s+time|if)\b[^.!?]{0,20}"
    r"\blaugh\w*\b",
    r"\blaugh\w*\b[^.!?]{0,25}\b(?:breath(?:less)?|puffed|winded|gasp\w*)\b",
    r"\b(?:can'?t|cannot|can\s+not)\s+(?:catch|get|find)\s+(?:my|his|her|their|a)\s+"
    r"breath\s+laugh\w*\b",
)

BREATH_LAUGH_REPLY = (
    "Laughing hard empties the lungs and leaves anyone gasping for a few seconds; it passes once "
    "the laughing stops, and it is not a sign of bad lungs on its own. Worth a GP if the "
    "breathlessness turns up when nobody is laughing, if a cough or a wheeze comes with it, or if "
    "it is new and getting worse.",
    "A hard laugh leaves nobody with air for a moment, and it settles as soon as the laughing "
    "stops, so there is usually nothing in it. Worth a GP if the breathlessness turns up without "
    "the laugh, or comes with a cough, a wheeze or chest pain.",
)

CHOKE_AIR_OK = (
    r"\b(?:can|could|able\s+to)\s+(?:still\s+)?(?:cough|talk|speak|breathe|say)\w*\b",
    r"\bcoughing\s+(?:well|fine|ok|okay|strongly|strong|up)\b",
    r"\b(?:he|she|they|i)\s+(?:is|are|am|'s)\s+(?:coughing|talking|speaking)\b",
    r"\bstill\s+(?:coughing|talking|speaking)\b",
)

CHOKE_NOT_PERSON = (
    r"\b(?:kitchen\s+sink|sink|drains?|pipes?|toilet|loo|garden|lawn|flowerbeds?|engine|filter|"
    r"radiator|chimney|gutter\w*|weeds?|moss|bog|traffic|paperwork|inbox|diary|sourdough|"
    r"mower|lawnmower|hoover|vacuum|dishwasher|printer|motorbike|scooter|tears?)\b",
    r"\b(?:bath\s*tub|bathtub|baths?|tub|basins?|hand\s?basins?|wash\s?basins?|showers?|"
    r"shower\s+tray|washing\s+machine|washer|hose|pipework|downpipe|gulley|drainpipe|"
    r"water\s+butt|pump|cistern|plughole|plug\s+hole)\b",
    r"\bchoked\s+(?:with|on)\s+(?:weeds|leaves|moss|traffic|paperwork|debt|hair|roots|fat)\b",
)

CHOKE_PREVENT = (
    r"\bhow\s+(?:do|can|should|could|would)\s+(?:i|we|you)\s+(?:stop|prevent|avoid|keep)\b",
    r"\bhow\s+to\s+(?:stop|prevent|avoid|keep)\b",
    r"\b(?:stop|prevent|avoid|keep)\s+(?:my|him|her|them|a|the|your|me\s+from)\s+"
    r"(?:\w+\s+){0,2}chok",
    r"\bbest\s+way\s+to\s+(?:stop|avoid|prevent|keep)\b",
    r"\b(?:is|was|am)\s+(?:my|the|a|she|he|it)\s+(?:\w+\s+){0,2}choking\s+if\b",
    r"\bwhy\s+do\s+(?:babies|toddlers|kids|children)\b",
    r"\b(?:so|that)\s+(?:he|she|they|it)?\s*(?:doesn'?t|does\s+not|wont|won'?t|never)\s+choke\b",
    r"\bchoking\s+(?:hazard|risk)\b",
)

CHOKE_SETTLED = (
    r"\blaugh\w*\b", r"\bgiggl\w*\b", r"\bchuckl\w*\b",
    r"\b(?:got|get|getten)\s+it\s+(?:out|up)\b", r"\bcoughed\s+it\s+up\b",
    r"\b(?:it|came|went)\s+(?:up|out)\b",
    r"\b(?:he|she|they|i)(?:'s|s|\s+is|\s+am|\s+are)?\s+(?:fine|ok|okay|alright)\s+now\b",
    r"\bthat\s+was\s+close\b",
)

CHOKE_PERSON = (
    r"\b(?:my|his|her|their|our|the)\s+(?:\w+\s+){0,1}(?:mum|mom|mother|dad|father|son|daughter|"
    r"husband|wife|partner|brother|sister|friend|baby|child|kid|boy|girl|man|woman|gran|granny|"
    r"nan|grandad|grandma|grandpa|toddler|newborn|infant|mate|neighbou?r)\b",
    r"\b(?:he|she|they)\s+(?:is\s+|are\s+|was\s+|were\s+)?choking\b",
    r"\b(?:he|she|they)\s+choked\b",
)

FLOPPY_THING = (
    r"\bflopp\w*[\s-]+(?:disk|disc|drive|hat|hats|brim|brimmed|hair|haired|fringe|ears?|eared|bow|"
    r"toy|teddy|puppet|sleeve|leaves|book|bag|flag|cover|blanket|flower|plant|bunny|rabbit|dog|"
    r"puppy|kitten|cat|doll|ears|eared)\b",
    r"\b(?:hair|lettuce|salad|leaves|plant|flowers?|washing|sheets|flag|sail|balloon|fabric|battery)\b"
    r".{0,20}\b(?:limp|floppy)\b",
)

FLOPPY_SLEEPY = (
    r"\bflopp\w*[^.]{0,40}\bwhen\s+(?:they\s+are\s+|she\s+is\s+|he\s+is\s+|hes\s+|shes\s+)?"
    r"(?:very\s+)?(?:sleepy|sleeping|asleep|drowsy|tired|nodding\s+off|dropping\s+off)"
    r"(?:\s+(?:he|she|they|it)\s+(?:falls?|drops?|nods?)\s+(?:a\s+)?(?:asleep|off|sleep)\b)?",
    r"\b(?:goes|go|gets|get|turns?)\s+flopp\w*[^.]{0,40}\bwhen\s+(?:very\s+)?"
    r"(?:sleepy|sleeping|asleep|drowsy|tired|nodding\s+off|dropping\s+off)\b",
    r"\bflopp\w*[^.]{0,40}\bwhen\s+(?:he|she|they|it)\s+(?:falls?|drops?|nods?)\s+"
    r"(?:a\s+)?(?:asleep|off|sleep)\b",
    r"\b(?:goes|go|gets|get|turns?)\s+flopp\w*[^.]{0,40}\b[^.]{0,20}?"
    r"\b(?:falls?|drops?|nods?)\s+(?:a\s+)?(?:asleep|off)\b",
)

FLOPPY_RED_FLAG = (
    r"\bwont\s+wake\b", r"\bwon'?t\s+wake\b", r"\bhard\s+to\s+wake\b", r"\bnot\s+waking\b",
    r"\bnot\s+feeding\b", r"\bwont\s+feed\b", r"\bwon'?t\s+feed\b", r"\bstopped\s+feeding\b",
    r"\btemperature\b", r"\bfever\b", r"\bbreath\w*\b", r"\bunresponsive\b", r"\blife-?less\b",
    r"\bvery\s+sleepy\b", r"\btoo\s+sleepy\b",
)

HEAT = (
    r"\bheat\s?stroke\b", r"\bheat\s+exhaustion\b", r"\bsun\s?stroke\b",
    r"\b(?:overheated|over\s?heated)\b.{0,25}\b(?:sick|dizzy|faint|confused|headache)\b",
    r"\b(?:sick|dizzy|faint|confused)\b.{0,25}\b(?:from|in)\s+(?:the\s+)?heat\b",
    r"\b(?:overheat\w*|boiling\s+hot)\b.{0,30}\b(?:confused|dizzy|faint\w*|sick|vomit\w*|"
    r"collapse\w*|unconscious|can'?t\s+stand|couldn'?t\s+stand|cant\s+stand|headache)\b",
    r"\b(?:confused|dizzy|faint\w*|vomit\w*|collapse\w*)\b.{0,30}\b(?:overheat\w*|boiling\s+hot)\b",
    r"\b(?:baby|babies|toddler|newborn|infant|child|kid|son|daughter|boy|girl)\b.{0,40}"
    r"\b(?:boiling\s+hot|burning\s+up|overheat\w*)\b",
)

SELF_HARM_TOPIC_OFF = (
    r"\b(?:course|essay|dissertation|talk|lecture|workshop|training|charity|article|book|"
    r"stud(?:y|ies)|research|film|documentary|paper|conference|lesson|class|exam|revision|"
    r"homework|awareness)\b",
    r"\bself[-\s]?harm\s+(?:counsell?or|nurse|worker|charity|helpline|awareness|prevention|"
    r"team|service)\b",
)

SELF_HARM_LOOKALIKE = (
    r"\b(?:on|with|against|from|by|through)\s+(?:a|an|the|some|his|her|their)?\s*"
    r"(?:tin|knife|blade|glass|sharp|nail|wire|cooker|oven|iron|kettle|pan|nettles?|bike|wall|"
    r"door|stone|gravel|rose|thorn|hook|scissors|grater|hob|razor|bat|ball|toy|swing|frame|"
    r"trampoline|slide|scooter|skateboard|climbing\s+frame|bouncy\s+castle|"
    r"barbed\s+wire)\b",
    r"\b(?:at|playing|during|in)\s+(?:netball|football|rugby|hockey|gym|sport|training|school|"
    r"playtime|the\s+park|the\s+playground)\b",
    r"\b(?:play|plays|playing|played)\s+(?:\w+\s+){0,2}"
    r"(?:netball|football|rugby|hockey|sport|sports|tennis|basketball|cricket|golf|squash|"
    r"badminton|rounders|outside|the\s+park)\b",
    r"\bin\s+(?:his|her|their|my)\s+sleep\b",
    r"\bwhile\s+(?:he|she|they|i)\s+(?:'?s\s+|is\s+|was\s+)?(?:asleep|sleeping)\b",
    r"\bin\s+(?:his|her|their|my)\s+bed\b",
    r"\b(?:shaving|chopping|cooking|gardening|diy|ironing|baking|haircut)\b",
    r"\bby\s+accident\b", r"\baccidentally\b",
)

AN_ITCH_LOOKALIKE = (
    r"\b(?:scratch\w*|rub\w*|pick\w*)\b[^.?!]{0,25}?"
    r"\b(?:itch(?:y|ing|es)?|eczema|rash|spots|scabs|hives|dandruff|dry\s+skin|head\s+lice|"
    r"nits|threadworms?|chicken\s?pox|scabies|psoriasis|ringworm|allerg(?:y|ic)|sore|"
    r"at\s+night|at\s+bedtime|all\s+night|every\s+night|in\s+the\s+night|"
    r"a\s+lot|all\s+the\s+time|constantly|non[\s-]?stop)\b",
    r"\b(?:itch(?:y|ing|es)?|eczema|rash|spots|scabs|hives|dandruff|dry\s+skin|head\s+lice|"
    r"nits|threadworms?|chicken\s?pox|scabies|psoriasis|ringworm|allerg(?:y|ic))\b"
    r"[^.?!]{0,30}?\b(?:scratch\w*|rub\w*|pick\w*)\b",
)


A_WISH_OR_TALK_OF_IT = (
    r"\b(?:want|wants|wanted|wanting|wish|wishes|talk|talks|talking|mention|mentions|mentioned|"
    r"say|says|said|saying|tells?|told|thinking|thinks|thought|feels?|keeps?)\b"
    r"[^.?!]{0,22}\b(?:die|dying|end\s+(?:it|it\s+all|things)|ending\s+it|suicide|suicidal|"
    r"kill\s+(?:my|him|her|them)sel(?:f|ves)|not\s+be\s+(?:here|around))\b",
)

DISTRESS_BESIDE_IT = (
    r"\b(?:crying|sobbing|in\s+tears|tearful|depressed|miserable|hopeless|worthless|"
    r"can'?t\s+cope|cant\s+cope|falling\s+apart|numb|suicidal|self[\s-]?harm|"
    r"want\s+to\s+die|killing\s+my\s*self)\b",
    r"\b(?:dont|don'?t|do\s+not)\s+want\s+to\s+be\s+here\b",
    r"\bbetter\s+off\s+without\s+me\b",
    r"\bno\s+point\s+(?:in\s+)?(?:going\s+on|living)\b",
    r"\b(?:cant|can'?t)\s+go\s+on\b",
    r"\bend\s+it\s+all\b",
    r"\b(?:worried|worrying|concerned|frightened|scared|afraid)\s+(?:about|for|that)\b",
    r"\b(?:not|isn'?t|hasn'?t|has\s+not)\s+(?:been\s+)?(?:her|him|them)sel(?:f|ves)\b",
    r"\b(?:gone\s+quiet|has\s+been\s+quiet|stopped\s+eating|not\s+eating|off\s+her\s+food|"
    r"off\s+his\s+food)\b",
)

WISH_DEAD_HYPERBOLE = (
    r"\bso\s+(?:tired|exhausted|knackered|worn\s+out|sleepy|drowsy|bored|hungry|starving|"
    r"thirsty|full|stuffed|hot|cold|freezing|sore|aching|busy|snowed\s+under|laughing|"
    r"embarrassed|hungover|old|fat|slow)\b(?!\s+of\s+(?:it|all|life|everything|this|the\s+world)\b)"
    r"[^.?!]{0,40}\bwish\w*\b",
    r"\blaugh(?:ed|ing|s)?\b[^.?!]{0,30}\bwish\w*\b",
)

WISH_DEAD_WHEN = (
    r"(?:january|february|march|april|may|june|july|august|september|october|november|december|"
    r"jan|feb|mar|apr|jun|jul|aug|sep|sept|oct|nov|dec|"
    r"monday|tuesday|wednesday|thursday|friday|saturday|sunday|"
    r"(?:my|our|the|his|her)?\s*(?:birthday|wedding\s+day)|christmas|xmas|easter|"
    r"(?:the\s+)?new\s+years?|spring|summer|autumn|winter|half\s+term|(?:the\s+)?weekend|"
    r"today|tonight|tomorrow|this\s+(?:week|month|year|weekend|evening|morning)|next\s+\w+|"
    r"a\s+(?:day|week|fortnight|month|year|minute|hour)|an\s+hour|"
    r"\d+\s*(?:days?|weeks?|months?|years?|hours?)|the\s+end\s+of\s+the\s+(?:week|month|year))"
)

WISH_DEAD_PLACE = (
    r"\bi\s+wish\w*\s+i\s+(?:wasnt|wasn'?t|was\s+not)\s+(?:here|around)\s+"
    r"(?:at\b(?!\s*(?:all\b|the\s+time\b))|in|on|with|near)\s+"
    r"(?!(?:the\s+)?" + WISH_DEAD_WHEN + r"\b)",
    r"\bi\s+(?:dont|don'?t|didnt|didn'?t)\s+want\s+to\s+be\s+(?:here|around)\s+"
    r"(?:at\b(?!\s*(?:all\b|the\s+time\b))|in|on|with|near)\s+"
    r"(?!(?:the\s+)?" + WISH_DEAD_WHEN + r"\b)",
)

LOSS_SAID = (
    r"\b(?:died|dies|dying|dead|passed\s+(?:away|on)|funeral|burial|cremation|buried|"
    r"killed\s+(?:him|her|them)self|killed\s+himself|took\s+(?:his|her|their)\s+own\s+life|"
    r"ended\s+(?:his|her|their)\s+own\s+life|committed\s+suicide|lost\s+(?:my|our|his|her|their|the)\s+\w+|"
    r"we\s+lost\s+\w+)\b",
)

SELF_RUMINATION = (
    r"\b(?:keep|kept|still|can'?t\s+stop|cannot\s+stop)\b[^.?!]{0,40}\b(?:thinking|think|"
    r"thought|wondering|imagining)\b",
    r"\b(?:thinking|thought|wondering)\s+(?:about|of)\s+(?:doing\s+)?it\b",
    r"\bmade\s+me\s+(?:think|wonder)\s+(?:about|of)\b",
    r"\bthink(?:s|ing)?\s+(?:about|of)?\s*it\s+(?:every|all\s+the|each)\s+"
    r"(?:night|day|time|morning)\b",
    r"\b(?:feel\s+like|felt\s+like|want\s+to|wanted\s+to|going\s+to|gonna|might|tempted\s+to)"
    r"\s+(?:do|doing|try|trying|end)\s+(?:it|something|this|things)\b",
)

THING_THAT_IS_SUICIDE = (
    r"(?:job|jobs|work|shift|shifts|rota|commute|drive|driving|cycle|ride|run|route|road|lane|"
    r"motorway|m25|m1|m6|a1|a3|a4|climb|descent|hike|walk|hill|slope|piste|traffic|weather|"
    r"plan|idea|option|choice|move|career|course|diet|exam|interview|pitch|season|fixture|trip|"
    r"deal|deadline|rent|mortgage|timetable|schedule|sale|launch|market|game|match|tactic|team)"
)

SUICIDE_ABOUT_A_THING = (
    r"\b(?:this|that|the|my|his|her|our|their|your|a|an)\s+(?:\w+\s+){0,2}"
    r"" + THING_THAT_IS_SUICIDE + r"\b[^.!?]{0,30}\b(?:is|was|'s|would\s+be|will\s+be|"
    r"must\s+be)\s+(?:pure\s+|total\s+|absolute\s+|outright\s+)?suicid(?:e|al)\b",
    r"\bcareer\s+suicid(?:e|al)\b",
    r"\b(?:it'?s|its|it\s+is|it\s+was|it'?d\s+be|it\s+would\s+be)\s+"
    r"(?:pure\s+|total\s+|absolute\s+)?suicid(?:e|al)\s+to\b",
    r"\b(?!(?:going|carrying)\s+on\s+(?:is|was|would|'?s|and|like|any|much\s+further)\b)"
    r"(?:going|driving|cycling|walking|climbing|running|commuting|working|eating|drinking|"
    r"flying|sailing|swimming|skiing|snowboarding|surfing|dating|studying|shopping|travelling|"
    r"traveling|moving|wearing|betting|buying|opening|marrying|getting|booking|hiking|camping|"
    r"jogging|rowing|parking|queuing)(?:\s+(?:out|in|on|up|down|through|with|to|for|at|off|"
    r"across|around|round|over|back)){1,2}\s+"
    r"(?:(?:that|this|these|those|the|a|an|my|his|her|their|our|your)\s+\w|work\b|school\b|"
    r"college\b|uni\b)[^.?!]{0,40}\b"
    r"(?:is|was|would\s+be|'?s)\s+(?:pure\s+|total\s+|absolute\s+|outright\s+)?"
    r"suicid(?:e|al)\b",
    r"\b(?:doing|trying|taking|starting|going)\s+(?:that|this|it)\b[^.?!]{0,30}\b"
    r"(?:is|was|would\s+be|'?s)\s+(?:pure\s+|total\s+|absolute\s+|outright\s+)?"
    r"suicid(?:e|al)\b",
)

DIE_OF_THE_FEELING = (
    r"\b(?:want\w*|wish\w*|feel\w*|felt|think\w*|thought|going|gonna|nearly|almost)\b"
    r"(?:[\s,]+[a-z']+){0,3}\s+(?:to\s+)?(?:die|dying|died)\s+(?:of|from)\s+"
    r"(?:embarrass\w*|boredom|thirst|curiosity|laughter|shame|fright)\b",
    r"\b(?:die|dyed|dyeing|dying)\s+my\s+hair\b",
)

WISH_NAMED = (
    r"\bsuicid(?:e|al)\b",
    r"\bself[-\s]?harm(?:ing|ed)?\b",
    r"\b(?:want|wanted|wanting|need|needed|like)\s+to\s+die\b(?!\s+(?:of|laughing))",
    r"\b(?:think|thinks|thinking|thought|thoughts?)\s+(?:about|of)\s+(?:dying|suicide|"
    r"self[-\s]?harm|killing\s+my\s*self|ending\s+it)\b",
    r"\bend(?:ing)?\s+(?:it|my\s+(?:own\s+)?life|it\s+all)\b",
    r"\b(?:don'?t|do\s+not|doesn'?t)\s+want\s+to\s+(?:live|be\s+here|exist|wake\s+up|go\s+on)\b",
    r"\bbetter\s+off\s+(?:dead|without\s+me|if\s+i\s+was\s+gone|if\s+i\s+weren'?t\s+here)\b",
    r"\b(?:hurt|hurting|cut|cutting|kill|killing|harm|harming)\s+my\s*self\b",
)

FIT_ALL_BETTER = (
    r"\b(?:is|was|feels?|seems?|looks?)\s+(?:much\s+|totally\s+|completely\s+|absolutely\s+)?"
    r"(?:fine|ok|okay|alright|better|himself|herself|themselves|normal)\s+(?:again\s+)?now\b",
    r"\b(?:now|since\s+then)\s+(?:he|she|they)\s+(?:is|are|seems?|feels?|was)\s+"
    r"(?:fine|ok|okay|alright|better|normal)\b",
)

STILL_GOING = (
    r"\b(?:can'?t|cannot|can\s+not|unable\s+to)\s+(?:get\s+up|move|walk|stand|feel)\b",
    r"\b(?:stuck|trapped)\b", r"\bwon'?t\s+(?:wake|get\s+up)\b",
    r"\bis\s+still\s+(?:on\s+the\s+floor|there|stuck|bleeding|in\s+pain)\b",
    r"\bhasn'?t\s+(?:stopped|shifted|got\s+up)\b", r"\bstill\s+(?:in|on)\s+(?:bed|the\s+floor)\b",
)

OLD_TIME = (
    r"\b(?:in\s+)?(?:19|20)\d\d\b", r"\b(?:years?|months?|decades?|weeks?)\s+ago\b",
    r"\bwhen\s+i\s+was\s+(?:\d+|a\s+kid|a\s+child|young|little|at\s+school)\b",
    r"\bwhen\s+(?:i|he|she|they|we)\s+(?:was|were)\s+(?:\d+|a\s+kid|a\s+child|a\s+baby|"
    r"a\s+toddler|a\s+tot|an\s+infant|young|little|small|at\s+school|born)\b",
    r"\blast\s+(?:year|summer|winter|decade|century|week|month)\b", r"\bused\s+to\b",
    r"\b(?:fell|fallen|had\s+a\s+fall|broke|fractured|dislocated|sprained)\b[^.?!]{0,30}"
    r"\blast\s+(?:week|month)\b",
)

DRUG_NAME = (
    r"(?:pills?|tablets?|capsules?|paracetamol|ibuprofen|aspirin|painkillers?|sleeping\s+pills?|"
    r"antidepressants?|co-?codamol|codeine|tramadol|morphine|methadone|insulin|lithium|valium|"
    r"diazepam|temazepam|xanax|heroin|heroine|cocaine|opioids?|opiates?|drugs?|meds|medication|"
    r"medicines?|antihistamines?|antibiotics?|iron\s+tablets|vitamins?|laxatives?|diuretics?|"
    r"beta\s+blockers?|statins?)"
)

EDGE_OF_A_DROP = (
    r"\b(?:stood|standing|sat|sitting|walked)\b[^.?!]{0,10}\b(?:on|at)\s+the\s+edge\s+of\s+"
    r"(?:a\s+|the\s+)?(?:bridge|roof|building|cliff|car\s*park)\b",
    r"\b(?:stood|standing|sat|sitting|walked)\b[^.?!]{0,10}\b(?:on|at)\s+the\s+edge\s+of\s+"
    r"(?:a\s+|the\s+)?(?:platform|tracks?)\b(?=[^.?!]*\b(?:thought|thinking|wanted|want|nearly|"
    r"almost|about\s+to|going\s+to|close\s+to|jump|jumped|looked\s+down|someone|police|pulled|"
    r"grabbed|swaying|drunk|end\s+it|easy)\b)",
)

END_IT_WITH_A_THING = (
    r"\bend(?:ed|ing|s)?\s+it\s+(?:with|by|using|between)\b",
    r"\bend(?:ed|ing|s)?\s+it\s+(?:by|off|on|under|in)\s+(?:the\s+)?(?:bridge|train|tracks|railway)\b",
)

END_IT_MEANS = (
    r"\b(?:pills?|tablets?|painkillers?|paracetamol|antidepressants?|meds?|medication|"
    r"an?\s+overdose|overdosing|a\s+knife|the\s+knife|a\s+razor|a\s+blade|a\s+rope|"
    r"a\s+belt|a\s+ligature|a\s+gun|a\s+shotgun|gas|the\s+car|a\s+car|the\s+train|"
    r"a\s+train|drowning|a\s+bridge|the\s+bridge|something\s+sharp|"
    r"hang(?:ing|ed)?|alcohol|drink|drinking|vodka|whisky|whiskey|gin|tablets|"
    r"my\s+wrists?|my\s+own\s+life)\b",
)

RECENT_TIME = (
    r"\b(?:yesterday|last\s+night|last\s+evening|this\s+(?:morning|afternoon|evening)|"
    r"earlier(?:\s+today)?|a\s+few\s+(?:days?|weeks?)\s+ago|"
    r"a\s+couple\s+of\s+(?:days?|weeks?)\s+ago|recently|"
    r"on\s+(?:mon|tues|wednes|thurs|fri|satur|sun)day|"
    r"(?:at|over|during)\s+the\s+weekend|last\s+weekend)\b",
)

SELF_HARM_SCARS = (
    r"\b(?:have|got|has|had|covered\s+in|full\s+of)\b[^.?!]{0,15}"
    r"\b(?:cuts|scars|scratches|burn\s*marks|slashes)\b[^.?!]{0,12}"
    r"\b(?:on|across|down|up)\s+(?:both\s+)?(?:my|his|her|their|your)\s+"
    r"(?:wrists?|arms?|forearms?|thighs?|tummy|stomach|belly)\b",
    r"\b(?:my|his|her|their)\s+(?:wrists?|forearms?|thighs?)\b[^.?!]{0,10}"
    r"\b(?:are|is|r)\s+(?:all\s+)?(?:scars?|scarred|cut\s+up|covered\s+in\s+scars?)\b",
)

SELF_HARM_SCARS_NOT = (
    r"\b(?:from|off)\s+(?:the|a|an|my|our|his|her|their)\s+(?:cat|dog|puppy|kitten|pet|rabbit|"
    r"hamster|hedgehog|parrot|budgie|horse|pony|bike|motorbike|car|van|ladder|shelf|barbecue|"
    r"oven|hob|cooker|kettle|toaster|knife|blade|glass|tin|can|tool|drill|saw|mower|gate|fence|"
    r"nails?|rose|bush|brambles?|thorns?|shower|tap|bath|door|window|cupboard|drawer|work|job|"
    r"office|school|nursery|garden|allotment|kitchen|garage|shed|building\s+site|farm|"
    r"football|rugby|hockey|netball|climbing|cycling|gardening|diy|cooking|chopping|shaving|"
    r"washing\s+up|hoovering|cleaning|moving|flat|house|home)\b",
    r"\b(?:at|from)\s+(?:work|the\s+garden|the\s+allotment|the\s+tip|the\s+shops?)\b",
    r"\b(?:on|off)\s+(?:a|an|the|some)\s+(?:knife|blade|glass|tin|can|nail|screw|wire|fence|"
    r"barbed\s+wire|thorn|rock|stone|kerb|roof|wall|door|drawer|bike|motorbike|car|mower|tool)\b",
    r"\b(?:while|when)\s+(?:i\s+was\s+|i'm\s+)?(?:cooking|chopping|shaving|carving|cutting|"
    r"peeling|washing\s+up|gardening|diy|working|cleaning|hoovering|painting|decorating)\b",
    r"\b(?:acne|spot|spots|chickenpox|eczema|psoriasis|rash|allergy|allergic|hives|itch\w*|"
    r"surgery|operation|scarred\s+from\s+the)\b",
)

SPOKEN_ATTEMPT_UNDATED = (
    *SELF_HARM_SCARS,
    r"\b(?:tried|try|tries|trying|attempted|attempt|attempts|attempting|went\s+to|"
    r"nearly|almost)\b"
    r"[^.?!]{0,25}\b(?:end(?:ed|ing)?\s+it|kill(?:ing)?\s+my\s*self|end\s+my\s+life|"
    r"(?:take|took)\s+my\s+own\s+life|end(?:ed)?\s+my\s+life|suicide|"
    r"hang(?:ing|ed)?\s+my\s*self|jump\s+off)\b",
)

PAST_ATTEMPT_NOT = (
    r"\b(?:on\s+(?:(?:a|an|the|some|my)\s+)?(?!purpose\b)[a-z]+|while\s+(?:cooking|chopping|"
    r"shaving|carving|cutting|peeling|washing\s+up|gardening|diy|working)|chopping|carving|"
    r"peeling|shaving|gardening|trimming|pruning)\b",
    r"\b(?:laughing|of\s+laughter|off\s+my\s+bike|on\s+the\s+stairs|tripping|embarrass\w*|"
    r"mortified)\b",
)

PAST_WISH = (
    r"\bi\b[^.?!]{0,24}\b(?:wanted|wanting|thought\s+about|thought\s+of|thoughts\s+about|"
    r"kept\s+thinking\s+about|kept\s+thinking\s+of|thinking\s+about|thinking\s+of|planned|"
    r"planning|was\s+going\s+to|was\s+planning\s+to|felt\s+like|considered|dreamt\s+about)"
    r"\b[^.?!]{0,18}\b(?:kill\s+my\s*self|killing\s+my\s*self|end\s+it\s+all|"
    r"ending\s+it|end\s+my\s+life|ending\s+my\s+life|die|dying|suicide|suicidal|not\s+be\s+here|"
    r"disappear|hurt\s+my\s*self|cutting\s+my\s*self|self\s*harm)\b",
    r"\bi\b[^.?!]{0,20}\b(?:felt|was|were|have\s+been|had\s+been|been|got)\b[^.?!]{0,8}"
    r"\b(?:suicidal|feeling\s+suicidal)\b",
)

EFFORT_AFTER = re.compile(
    r"\b(?:nearly|almost)\b[^.?!]{0,24}\b(?:killed|kill)\s+my\s*self\s+"
    r"(?:at\s+the\s+(?:gym|pool|park|tip)|"
    r"on\s+(?:the\s+|my\s+|a\s+)?(?:bike|bicycle|stairs|steps|staircase|ladder|roof|"
    r"treadmill|run|road|motorway|trampoline|pitch|hill|scaffold)\b|"
    r"off\s+(?:the\s+|my\s+|a\s+)?(?:(?:back|front)\s+of\s+(?:a|the|my)?\s*)?"
    r"(?:bike|bicycle|motorbike|motorcycle|moped|scooter|horse|pony|ladder|roof|wall|"
    r"scaffold|trampoline|skateboard|skis|boat|truck|lorry|van|trailer)\b|"
    r"(?P<doing>[a-z']+ing)\b)",
)

PAST_WISH = PAST_WISH + COUNTERFACTUAL_WISH

PAST_WISH_NOT = (
    r"\b(?:of|from)\s+(?:embarrass\w*|boredom|thirst|curiosity|laughter|shame|fright)\b",
    r"\b(?:die|dying|died)\s+(?:laughing|of)\b",
    r"\bthought\s+(?:i|that\s+i)\s+(?:was|were)\s+(?:going\s+to|about\s+to|gunna)\s+die\b",
    r"\bfelt\s+like\s+(?:i|that\s+i)\s+(?:was|were)\s+(?:going\s+to|about\s+to)\s+die\b",
    r"\b(?:scared|afraid|terrified|convinced)\b",
)

OVERDOSE_FOOD = (
    r"\boverdos(?:e|ed|ing)\b[^.?!]{0,12}\b(?:on|of|with)\s+(?:the\s+|a\s+|some\s+)?"
    r"(?:cake|cakes|chocolate|sweets|candy|biscuits?|cookies|crisps|chips|chinese|curry|pizza|"
    r"ice\s*cream|cheese|coffee|tea|netflix|tv|telly|sugar|bread|"
    r"pastr(?:y|ies)|do(?:ugh)?nuts|burgers?|takeaways?|naps|love|pies?|pudding|trifle|"
    r"turkey|roast|stuffing|mince|gravy|easter\s+eggs?)\b",
)

OVERDOSE_DRUG = (
    r"\b(?:pills?|tablets?|paracetamol|ibuprofen|painkillers?|meds|medicines?|"
    r"sleeping\s+pills?|antidepressants?|insulin|heroin|heroine|cocaine|methadone|tramadol|"
    r"codeine|morphine|opioid|opiates?|drugs?|liquid|bottle|packet|pack|box|strip|blister)\b",
    r"\b(?:alcohol|vodka|whisky|whiskey|wine|beer|gin|rum|brandy|tequila|lager|cider|champagne|"
    r"prosecco|ros\u00e9|spirits?|drink|drinking|booze)\b",
)

CHEST_WORK = (
    r"\bchest\b.{0,30}\b(?:after|during|when)\s+(?:the\s+|a\s+|my\s+)?"
    r"(?:gym|run|running|jog|jogging|workout|exercise|exercising|swim|swimming|cycle|cycling|"
    r"football|netball|walk|walking|stairs|climbing|training|weights|lifting)\b",
    r"\bchest\b.{0,30}\b(?:when\s+i\s+(?:run|walk|climb|exercise|train|cycle|swim|lift))\b",
    r"\bafter\s+(?:the\s+|a\s+)?(?:gym|run|workout|training)\b.{0,30}\bchest\b",
)

CHEST_SLOW = (
    r"\bchest\b.{0,45}\b(?:for\s+(?:a\s+(?:few|couple)\s+(?:days|weeks)|\d+|two|three|four|five|"
    r"several|weeks?|months?|days?)\s*(?:days|weeks|months|years)?|for\s+months|for\s+ages|"
    r"comes?\s+and\s+goes|keeps?\s+coming\s+back|on\s+and\s+off|since\s+(?:last|christmas)|"
    r"\d+\s+(?:days|weeks|months)\s+now)\b",
)

CHEST_URGENT = (
    r"\b(?:can'?t|cannot|couldn'?t)\s+breathe\b", r"\bshort\s+of\s+breath\b",
    r"\b(?:crushing|squeezing|heavy)\b", r"\bspreading\b", r"\bsweat\w*\b",
    r"\bcollapsed\b", r"\b(?:going|gone|turning)\s+blue\b", r"\bpassed\s+out\b",
    r"\bright\s+now\b", r"\bthis\s+(?:morning|afternoon|evening)\b", r"\bjust\s+happened\b",
    r"\b(?:sudden(?:ly)?|all\s+of\s+a\s+sudden|out\s+of\s+nowhere)\b",
    r"\b(?:came|come|comes|coming)\s+on\s+(?:suddenly|all\s+of\s+a\s+sudden|out\s+of\s+nowhere)\b",
)

DOG_HABIT = (
    r"\b(?:keeps?|kept|always|sometimes|occasionally|now\s+and\s+then|every\s+time|"
    r"has\s+started|started|used\s+to|since\s+(?:he|she|the\s+dog)|has\s+become|"
    r"getting\s+worse|how\s+do\s+i\s+stop|how\s+to\s+stop|stop\s+(?:him|her|it|them)\b|"
    r"any\s+advice|train|training|behaviourist|behaviour)\b",
    r"\b(?:when|whenever|while|if|as\s+soon\s+as|before|after)\s+"
    r"(?:i|we|he|she|they|you|someone|anyone|the\s+(?:vet|postman|kids))\b",
    r"\b(?:take|taking|touch|touching|reach\s+for|go\s+near|going\s+near|stroke|stroking|"
    r"pet|petting|pick\s+up|picking\s+up|move|moving)\b[^.?!]{0,20}"
    r"\b(?:his|her|their|the)\s+(?:food|bowl|bone|toy|bed|lead|collar|chew)\b",
)

DOG_MOUTHING = (
    r"\b(?:bit|bite|bites|biting|nipped|nipping|nips|snapped\s+at|chewing|chewed)\s+"
    r"(?:at\s+)?(?:the|a|an)\s+(?:lead|leash|toy|stick|bone|cushion|blanket|"
    r"sofa|bed|sleeve|shoe|shoes|trouser\s+leg)\b[^.?!]{0,30}\band\s+(?:my|me)\b",
)

DOG_SELF_BITE = (
    r"\b(?:bit|bite|bites|biting|nipped|nipping|nips|snapped)\b[^.?!]{0,15}"
    r"\b(?:himself|herself|itself|themselves)\b",
    r"\b(?:bit|bite|bites|biting|nipped|nipping|nips|snapped)\s+(?:at\s+)?(?:his|her|its|their)\s+"
    r"(?:own\s+)?(?:paws?|feet|foot|pads?|tail|legs?|fur|coat|skin|ears?|flank|back|bed|blanket|"
    r"lead|cage|bedding)\b",
    r"\b(?:bit|bite|bites|biting|nipped|nipping|nips|snapped)\s+(?:at\s+)?(?:the|a|an)\s+"
    r"(?:lead|leash|cage|blanket|bedding|bed|toy|stick|bone|chew|kong|ball|cushion|pillow|"
    r"sofa|gate|fence|door)\b",
)

PET_NAMES = (r"(?:cat|cats|dog|dogs|puppy|puppies|kitten|kittens|pup|pups|rabbit|rabbits|bunny|"
             r"hamster|hamsters|guinea\s+pig|guinea\s+pigs|pony|ponies|horse|horses|pet|pets|"
             r"bird|birds|parrot|parrots|budgie|budgies|ferret|gerbil|tortoise|"
             r"chicken|chickens|hen|hens|duck|ducks|goat|goats|sheep|lamb|lambs)")

BITE_ON_ANIMAL = (
    r"\b(?:bit|bite|bites|biting|bitten|nipped|nips|snapped\s+at|snaps\s+at|went\s+for|"
    r"goes\s+for|going\s+for|attacked|attacks|attacking|mauled|mauls|savaged|savages|"
    r"latched\s+onto)\b[^.?!]{0,30}\b(?:my|our|the|his|her|their|"
    r"next\s+doors?|neighbou?rs?)\s+" + PET_NAMES + r"\b",
    r"\b(?:my|our|the|his|her|their|next\s+doors?|neighbou?rs?)\s+" + PET_NAMES +
    r"\b[^.?!]{0,30}\b(?:got|was|were|has\s+been|had\s+been|have\s+been|been)\s+"
    r"(?:bit|bitten|attacked|mauled|savaged)\b"
    r"(?!\s+by\s+(?:fleas?|ticks?|bees?|wasps?|insects?|ants?|mites?|mosquitoes?)\b)",
)

FICTION_NOW = (
    r"\bfor\s+(?:a|my|the)\s+(?:story|novel|book|film|script|screenplay|essay|assignment|"
    r"character)\b",
    r"\bin\s+(?:a|my|the)\s+(?:story|novel|book|film|game|dream)\b",
    r"\b(?:story|novel|script|screenplay|essay|film)\b.*\b(?:character|plot|scene)\b",
    r"\bmy\s+(?:character|protagonist)\b",
)

OTHER_RISK = (
    r"\b(?:he|she|they|my\s+" + PERSON + r"|the\s+" + PERSON + r"|" + PERSON + r")\b.{0,30}"
    r"\b(?:wants?\s+to\s+(?:die|kill)|wanna\s+die|kill\s+(?:him|her)self|kill\s+themselves|"
    r"suicid\w*|self[-\s]?harm\w*|"
    r"end\s+(?:it|their\s+life)|doesn'?t\s+want\s+to\s+(?:live|be\s+here)|better\s+off\s+dead|"
    r"tried\s+to\s+kill|has\s+taken\s+(?:too\s+many|a\s+lot\s+of|all\s+(?:his|her|the)\s+pills))\b",
    r"\b(?:he|she|they|my\s+" + PERSON + r")\b.{0,25}"
    r"\b(?:hurt|hurts|hurting|cut|cuts|cutting|harm|harming|burning|starving)\s+"
    r"(?:him|her|them)self\b.{0,25}"
    r"\b(?:on\s+purpose|again|keeps?|kept|every\s+day|at\s+night|to\s+(?:cope|feel)|"
    r"because|won'?t\s+stop|can'?t\s+stop|deliberately|in\s+secret|in\s+private)\b",
    r"\b(?:he|she|they|my\s+" + PERSON + r")\b.{0,30}\b(?:has\s+|'s\s+)?locked\s+(?:him|her|them)self\s+"
    r"(?:in|away)\b.{0,30}\b(?:pills|tablets|pills?|knife|blades?|something\s+to\s+use|razor)\b",
    r"\b(?:he|she|they|my\s+" + PERSON + r")\b.{0,25}\b(?:keeps?|kept)\s+"
    r"(?:hurting|cutting|burning|starving)\s+(?:him|her|them)self\b",
)

SAFE_NOW = (
    r"\b(?:i'm|im|i\s+am|we're|we\s+are|they're|they\s+are|he's|she's)\s+(?:outside|out|safe|clear)\b",
    r"\b(?:breathing|feels?|looks?|seems?)\s+(?:better|easier|normally|again)\b",
    r"\bthey\s+(?:seem|look|are)\s+(?:better|okay|ok|awake)\b",
    r"\b(?:fire\s+(?:brigade|service|fighters?)|paramedics?|ambulance)\b.{0,25}\b(?:here|arrived|came|with\s+(?:us|me))\b",
    r"\b(?:it|the\s+bleeding)\s+(?:has\s+)?stopped\b",
)

SPINE_BREAK = (
    r"\b(?:my|the)\s+(?:back|neck|spine|spinal)\b"
    r"(?![^.?!]{0,15}\b(?:gate|door|window|fence|garden|yard|wall|room|lawn|patio|"
    r"light|pack|passage|road|bumper|seat)\b)[^.?!]{0,20}"
    r"\b(?:is|are|'?s|'?re|was|were|feels?|looks?)\s+"
    r"(?:broken|cracked|fractured|snapped)\b(?!\s+out\b)",
)

SPINE_BACK_WORK = (
    r"\b(?:from|after|with|doing|lifting|moving|carrying|digging|gardening|shovelling|shoveling|"
    r"hoovering|hoover|cleaning|housework|diy|build(?:ing)?)\b",
    r"\b(?:from\s+all\s+the|from\s+the\s+lifting|from\s+lifting|all\s+the\s+lifting|"
    r"after\s+moving|after\s+the\s+move|from\s+the\s+move|moving\s+the)\b",
)

FOLLOW_UP_ANCHOR = (
    r"\b(?:999|911|112|ambulance|paramedics?|fire|brigade|smoke|stairs|outside|safe|clear|"
    r"breath\w*|cpr|pulse|conscious|awake|asleep|bleeding|blood|burn\w*|hospital|doctor|a&e|"
    r"nurse|poison\w*|pills?|tablets?|medic\w*|medicine|epipen|inhaler|police|help|waiting|"
    r"wait|call\w*|now|still|they|them|him|her|she|he|it|ok|okay|done|yes|no|thanks|anything|"
    r"something|else|that|this|scared|frightened|terrified|afraid|soak\w*|through|still)\b",
)

HELP_ARRIVED = (
    r"\b(?:ambulance|paramedics?|fire\s+(?:brigade|service|engine)|police|crew)\b[^.?!]{0,25}"
    r"\b(?:is|are|'s|was|were)\s+(?:here|outside|coming|on\s+(?:its|their|the)\s+way|"
    r"arriving|arrived|pulling\s+up|at\s+the\s+door)\b",
    r"\b(?:they|someone|somebody|my\s+(?:mum|mom|dad|husband|wife|partner|sister|brother|son|"
    r"daughter|friend|neighbour|neighbor))\b[^.?!]{0,15}\b(?:is|are|'s)\s+(?:here|outside|"
    r"with\s+me|on\s+(?:their|his|her)\s+way|coming\s+(?:over|round))\b",
    r"\b(?:im|i'?m)\s+not\s+on\s+my\s+own\b",
)

FOLLOW_UP_MORE = (
    r"\bshould\s+i\s+(?:try|open|shut|close|turn|grab|hold|press|cover|warm|sit|lie|stand|walk|drive|eat|drink|wake|ring|phone|tell|say|text|message)\b",
    r"\bcan\s+i\s+(?:open|shut|close|turn|give|move|go|drive|eat|drink|wake|ring|phone)\b",
    r"\bis\s+it\s+(?:ok|okay|safe|alright|fine)\s+to\b",
)

CASE_WORDS = {
    'gas': r"\b(?:gas|meter|windows?|doors?|flames?|lights?|switches|smell|boiler|hob)\b",
    'fire': r"\b(?:fire|smoke|flames?|stairs?|windows?|doors?|building|flat|brigade|outside|neighbours?)\b",
    'dog_attack': r"\b(?:dog|dogs|collar|lead|leash|between|barrier|shout\w*)\b",
    'dog_bite': r"\b(?:bite|bitten|wound|dog|dressing|tetanus)\b",
    'bleeding': r"\b(?:blood|cloth|bandage|dressing|pressure|bleed\w*|wound|soak\w*|through|stop\w*|stitch\w*|scar)\b",
    'self_harm': r"\b(?:crisis|line|alone|phone|talk\w*|tell|say|mum|dad|mother|father|friend|partner|wife|husband|family|sister|brother|gp|doctor)\b",
    'chest': r"\b(?:chest|arm|jaw|aspirin|door|sit\w*|walk\w*|stand\w*|move|drive|climb\w*)\b",
    'chest_slow': r"\b(?:chest|tight\w*|gp|doctor|aspirin|weeks?|pain|breath\w*)\b",
    'unconscious': r"\b(?:breathing|side|pulse|recovery)\b",
    'breathing': r"\b(?:inhaler|epipen|upright|breath\w*|wheez\w*|lips?)\b",
    'stroke': r"\b(?:face|arm|speech|slurr\w*|time|food|drink)\b",
    'head_injury': r"\b(?:head|awake|wake|drowsy|sleepy|sick|vomit\w*)\b",
    'poison': r"\b(?:packet|container|bottle|pills?|tablets?|sick|vomit\w*)\b",
    'overdose': r"\b(?:packet|container|bottle|pills?|tablets?|sick|vomit\w*|breath\w*)\b",
    'hanging': r"\b(?:rope|neck|breath\w*|side|cpr)\b",
    'seizure': r"\b(?:fitting|fit|seizure|time|mouth|side)\b",
    'heat': r"\b(?:shade|water|cool\w*|fan|sweat\w*)\b",
    'general': r"\b(?:999|911|ambulance|paramedics?|police|help|waiting|wait|call|now|they|them|him|her|ok|safe|clear)\b",
}

LOCKED_IN_RISK = (
    r"\b(?:is\s+)?(?:locked|shut|locks?|locked\s+himself|locked\s+herself|locked\s+themselves)"
    r"\b.{0,30}\b(?:in|inside|behind)\b.{0,40}\b(?:pills?|tablets?|medication|medicine|knife|"
    r"razors?|blades?|scissors|gun)\b",
    r"\b(?:pills?|tablets?|knife|razors?|blades?)\b.{0,30}\b(?:locked|shut|barricaded)\b",
)

FIRE_NOW = (
    r"\b(?:smoke|fire)\s+alarm\b.{0,30}\b(?:going\s+off|sounding|blaring|wailing)\b",
    r"\bsmoke\s+(?:in|coming\s+into|filling|pouring\s+into|everywhere)\b",
    r"\b(?:on|caught)\s+fire\b",
    r"\bfire\s+(?:has\s+)?(?:started|spread)\b",
    r"\b(?:can't|cannot)\s+get\s+out\b.{0,40}\b(?:smoke|fire|flames?)\b",
)

WEIGHT_OFF_FEET = (
    r"\b(?:can'?t|cant|cannot|unable\s+to|won'?t|wont)\s+(?:put|bear|take|stand\s+on)\s+"
    r"(?:any\s+)?weight\b",
    r"\b(?:can'?t|cant|cannot|unable\s+to)\s+put\s+(?:my|his|her|their|your)\s+(?:foot|feet)\s+down\b",
    r"\b(?:can'?t|cant|cannot|unable\s+to)\s+stand\s+on\s+(?:my|his|her|their|the)\s+"
    r"(?:ankle|knee|foot|feet|leg|toe|toes|heel)\b",
)

WEIGHT_HIP = (
    r"\b(?:hip|hips|pelvis|pelvic|thigh|thighs|groin|femur)\b",
    r"\b(?:on\s+the\s+(?:floor|ground)|lying|can'?t\s+get\s+up|cant\s+get\s+up|not\s+moving)\b",
    r"\b(?:fell|fallen|fall|falling|slipped|tripped|collapsed|landed)\b[^.?!]{0,30}"
    r"\b(?:ladder|roof|scaffold\w*|stairs|steps|wall|cliff|horse|bunk|loft|trampoline|balcony)\b",
    r"\b(?:ladder|roof|scaffold\w*|stairs|steps|cliff|horse|bunk|loft|balcony)\b[^.?!]{0,30}"
    r"\b(?:fell|fallen|slipped|landed)\b",
    r"\b(?:my|his|her|their|your|our)\s+(?:\w+'s\s+)?"
    r"(?:arm|leg|wrist|ankle|shoulder|elbow|knee|foot)\b"
    r"[^.?!]{0,25}\b(?:bent|deformed|at\s+a\s+funny\s+angle|sticking\s+out|back\s+to\s+front)\b",
)

WEIGHT_LONG = (
    r"\b(?:every|each)\s+(?:morning|day|night)\b", r"\bin\s+the\s+mornings?\b", r"\blately\b",
    r"\bfor\s+(?:the\s+)?(?:last\s+|past\s+|few\s+|several\s+|a\s+few\s+|a\s+couple\s+of\s+)?"
    r"(?:weeks|months|years)\b",
    r"\b(?:weeks|months|years)\s+(?:now|ago)\b", r"\bfor\s+ages\b",
    r"\b(?:long\s+time|while)\s+now\b",
)

FALL_CORE = (
    r"\b(?:fell|fallen|falling|tumbled|came\s+off|come\s+off)\s+(?:off|from|down)\s+"
    r"(?:a\s+|the\s+|his\s+|her\s+|their\s+|my\s+)?(?:ladder|roof|scaffold\w*|stairs|steps|"
    r"wall|cliff|horse|top\s+bunk|loft|roof\s+rack)\b",
    r"\b(?:fell|fallen|tumbled)\s+down\s+(?:the\s+|a\s+)?(?:stairs|steps|flight\s+of\s+stairs)\b",
    r"\b(?:fell|fallen|tumbled)\s+(?:off|from)\s+(?:a\s+|the\s+)?(?:trampoline|bike|swing|"
    r"slide|climbing\s+frame|bunk\s+bed)\b[^.?!]{0,40}"
    r"\b(?:head|neck|back|spine|unconscious|knocked\s+out|not\s+moving|isn'?t\s+moving|"
    r"won'?t\s+wake|wont\s+wake|can'?t\s+feel|vomit\w*)\b",
    r"\b(?:fell|fallen|tripped)\b[^.?!]{0,30}\b(?:broke|broken|fractured)\s+(?:my|his|her|their)\s+"
    r"(?:hip|pelvis|back|neck|skull|spine)\b",
    r"\b(?:hip|pelvis)\b[^.?!]{0,25}\b(?:looks?\s+(?:wrong|odd|out\s+of\s+place)|is\s+(?:out\s+of\s+place|"
    r"deformed|mangled)|won'?t\s+bear\s+weight)\b",
    r"\b(?:fell|fallen|fall|slipped|tripped|collapsed)\b[^.?!]{0,25}"
    r"\b(?:can'?t|cant|cannot|not\s+able\s+to|unable\s+to)\s+(?:get|getting|stand)\s*"
    r"(?:\w+\s+)?(?:up|back\s+up)\b",
    r"\b(?:fell|fallen|fall|slipped|collapsed|fainted)\b[^.?!]{0,40}"
    r"\b(?:still\s+(?:on\s+the\s+floor|lying|down)|(?:he|she|they)\s*(?:'s|s|\s+is|\s+are)\s+"
    r"(?:still\s+)?(?:on\s+the\s+floor|lying\s+(?:there|on)))\b",
    r"\b(?:on\s+the\s+(?:floor|ground)|fell|fallen|slipped|collapsed)\b[^.?!]{0,35}"
    r"\b(?:can'?t|cant|cannot|not|won'?t|wont)\s+(?:move|moving)\b",
    r"\b(?:my|his|her|their|the)\s+" + PERSON + r"\b[^.?!]{0,20}\b(?:can'?t|cant|cannot)\s+"
    r"(?:move|feel\s+(?:his|her|their)\s+(?:legs?|arms?|body))\b",
    WEIGHT_OFF_FEET[0],
    r"\b(?:can'?t|cant|cannot|unable\s+to|won'?t|wont)\s+(?:put|bear|take|stand\s+on)\s+"
    r"(?:any\s+)?weight\b",
    r"\b(?:fell|fallen|fall|slipped|collapsed|on\s+the\s+(?:floor|ground))\b[^.?!]{0,40}"
    r"\b(?:can'?t|cant|cannot|not\s+able\s+to|unable\s+to|struggl\w+\s+to)\s+(?:lift|pick|"
    r"get)\s+(?:her|him|them|my\s+(?:mum|mom|mother|dad|father|wife|husband|partner|nan|gran|"
    r"neighbou?r|friend|brother|sister))\b",
    r"\b(?:can'?t|cant|cannot)\s+lift\s+(?:her|him|them|my\s+\w+)\s+off\s+the\s+"
    r"(?:floor|ground)\b",
)

OWN_LIMB_AT_AN_ANGLE = (
    r"\b(?:my|his|her|their|our|your|the)\s+(?:arm|arms|leg|legs|knee|knees|ankle|ankles|wrist|wrists|"
    r"elbow|elbows|shin|shins|thigh|thighs|hip|hips|shoulder|shoulders|jaw|foot|feet|hand|hands)\b"
    r"[^.?!]{0,25}\b(?:bent|deformed|at\s+a\s+funny\s+angle|sticking\s+out|back\s+to\s+front)\b",
)

FALL_PAST = (
    r"\b(?:last|this)\s+(?:year|month|week|night|winter|summer|spring|autumn|xmas|christmas)\b",
    r"\b(?:\d+|a|one|two|three|four|five|six)\s+(?:yrs?|years?|months?|weeks?)\s+ago\b",
    r"\b(?:years|months|weeks|ages)\s+ago\b", r"\bused\s+to\b", r"\byesterday\b",
    r"\ba\s+while\s+ago\b", r"\bwhen\s+i\s+was\s+(?:a\s+kid|young|little|a\s+child|small)\b",
    r"\bwhen\s+(?:he|she|they)\s+(?:was|were)\s+(?:a\s+)?(?:kid|child|boy|girl|young|little|"
    r"small|at\s+school|a\s+teenager)\b",
    r"\b(?:had|got)\s+it\s+checked\b", r"\bwas\s+in\s+hospital\s+(?:for|with|after)\b",
    r"\b(?:back)\s+then\b", r"\bwhen\s+he\s+was\s+(?:a\s+)?(?:baby|small|little)\b",
)

FALL_NOW = (
    r"\bright\s+now\b", r"\bthis\s+(?:morning|afternoon|evening)\b", r"\bjust\b",
    r"\btoday\b", r"\bminutes?\s+ago\b", r"\ban\s+hour\s+ago\b",
    r"\bcan'?t\s+(?:get|stand|sit|feel|move)\b", r"\bunable\s+to\s+(?:get|stand|move)\b",
    r"\bnot\s+able\s+to\s+(?:get|stand|move)\b", r"\ban\s+ambulance\b",
    r"\bnot\s+breathing\b", r"\bunconscious\b", r"\bbleeding\b", r"\bhead\s+injur\w*\b",
    r"\bstill\s+(?:on\s+the\s+floor|lying|down)\b",
)

FALL_FINE = (
    r"\b(?:but|and)\s+(?:he|she|they|it)\s*(?:'s|s|\s+is|\s+was)?\s*(?:ok|okay|fine|alright|"
    r"all\s+right)\b",
    r"[,;]\s*(?:but\s+)?(?:hes|shes|theyre|it\s+is|he\s+is|she\s+is|they\s+are|"
    r"he'?s|she'?s|they'?re)\s+(?:now\s+)?(?:ok|okay|fine|alright|all\s+right)\b",
    r"\b(?:says?|said|tells?|told)\s+(?:me\s+)?(?:he|she|they)\s*(?:'s|s|\s+was|\s+is)?\s*"
    r"(?:ok|okay|fine|alright)\b",
    r"\b(?:got\s+up|walked\s+it\s+off|laughed\s+it\s+off|laughed|ran\s+off|is\s+walking|"
    r"shes\s+walking|hes\s+walking|nothing\s+broken|no\s+harm|was\s+fine)\b",
    r"\b(?:i'?m|im)\s+(?:ok|okay|fine|alright)\b",
    r"\bstill\s+(?:fine|ok|okay|walking)\b",
    r"\b(?:picture|mirror|shelf|shelves|plaster|paint|tiles?|clock|poster|frame|curtains?|blind|"
    r"radiator|handle|door|window|bricks?|render|gutter(?:ing)?|shingles?|hook|rail|coving|"
    r"wallpaper|wreath|chimney|cable|lights?|fixture|fitting)\b[^.?!]{0,30}"
    r"\b(?:fell|falls?|falling|came\s+off|come\s+off|coming\s+off|keeps?\s+falling)\b"
    r"(?!\s+(?:on|onto|over)\s+(?:me|my\s+\w+|him|her|them|his\s+\w+|her\s+\w+|their\s+\w+))",
    r"\bit\s+(?:keeps?\s+falling|fell|falls|is\s+falling|came)\s+off\s+(?:the|a)\s+"
    r"(?:wall|shelf|hook|ceiling|door|window|board)\b",
    r"\b(?:keeps?|is\s+always)\s+falling\s+off\s+(?:the|a|my|our)\s+(?:wall|shelf|ceiling|hook|door|"
    r"window|board|brackets?)\b",
)

FALL_REPEAT = (
    r"\b(?:keep|keeps|kept)\s+(?:on\s+)?(?:falling|tripping|slipping|going\s+over|having\s+falls?)\b"
    r"(?!\s+(?:asleep|out|for|behind|apart|short|through|into|in\s+love))",
    r"\b(?:falls?|falling|trips?|tripping)\b[^.?!]{0,25}"
    r"\b(?:all\s+the\s+time|every\s+day|each\s+day|a\s+lot|constantly|regularly|often)\b",
    r"\b(?:is|am|are)\s+always\s+(?:falling|tripping|slipping)\b",
    r"\b(?:has|have|had)\s+been\s+(?:falling|tripping|slipping|going\s+over)\b"
    r"(?!\s+(?:asleep|out|for|behind|apart|short|through|into|in\s+love))",
    r"\b(?:had|have|has)\s+(?:a\s+)?(?:few|couple\s+of|several|two|three|more)\s+falls?\b",
)

FALL_CHECK_OFF = (
    r"\b(?:nearly|almost|could\s+have|might\s+have|would\s+have)\b[^.?!]{0,15}\b(?:fell|fallen|"
    r"fall|slipped|tripped)\b", r"\blaugh\w*\b",
    r"\b(?:fell|fallen|fall|falling)\s+(?:asleep|for|in\s+love|behind|apart|short|through|into)\b",
    r"\b(?:fell|fallen|fall|falling)\s+out\b(?!\s+of\b)",
    r"\b(?:fell|fallen|fall|falling)\s+off\s+the\s+wag[go]n\b",
    r"\b(?:hair|wig|snow|rain|leaves|price|prices|temperature|pound|stock|market)\b",
    r"\b(?:dont|don'?t|didnt|didn'?t|never|not)\b[^.?!]{0,10}\b(?:fell|fallen)\b",
) + FALL_WORD_IDIOM + (
    r"\b(?:slip|slips|slipped|slipping)\s+(?:up|behind|past|by|through|away|me|him|her|them|us)\b",
    r"\b(?:slip|slips|slipped|slipping)\s+out\b(?!\s*of\b)",
    r"\b(?:slip|slips|slipped|slipping|trip|trips|tripped)\b[^.?!]{0,25}"
    r"\b(?:work|works|schedule|deadlines?|grades?|marks?|standards?|quality|sales|figures?|"
    r"prices?|markets?|memor(?:y|ies)|attention|a\s+note)\b",
    r"\b(?:work|schedule|deadlines?|grades?|standards?|quality|sales|figures?|prices?|markets?|"
    r"the\s+quarter)\b[^.?!]{0,25}\b(?:has|have|had|keeps|keep|is|was)\b[^.?!]{0,10}"
    r"\b(?:slip|slips|slipped|slipping)\b",
)

FALL_ANSWERED = (
    r"\b(?:not|isn'?t|isnt|aren'?t|arent|stopped|stop|stopt)\s+breathing\b",
    r"\b(?:not|isn'?t|isnt|aren'?t|arent)\s+responding\b",
    r"\bcan'?t\s+breathe\b", r"\bcant\s+breathe\b",
    r"\bno\s+pulse\b", r"\bwithout\s+a\s+pulse\b", r"\bno\s+heartbeat\b",
    r"\bunresponsive\b(?!\s*(?:to|at|when|whenever|if|because|as|after|with|about)\b)",
    r"\bnot\s+waking\b", r"\bstill\s+not\s+waking\b",
)

FALL_RED = (
    r"\b(?:hit|hits|struck|landed\s+on|came\s+down\s+on|fell\s+on)\b[^.?!]{0,15}"
    r"\b(?:me|my\s+\w+|him|her|them|his\s+\w+|her\s+\w+|their\s+\w+)\b",
    r"\b(?:unconscious|knocked\s+out|not\s+moving|isn'?t\s+moving|won'?t\s+wake|wont\s+wake|"
    r"can'?t\s+feel|cant\s+feel|numb|vomit\w*|bleed\w*|hospital|ambulance|a\s+and\s+e|a&e|"
    r"broken|broke|fractured|stiff\s+neck)\b",
    r"\b(?:head|neck|back|spine)\b[^.?!]{0,20}\b(?:hit|bang\w*|hurt|pounding|bleeding)\b",
)

RASH_FADE = (
    r"\b(?:doesn'?t|does\s+not|don'?t|dont|won'?t|wont|isn'?t|is\s+not|not|never)\s+"
    r"(?:fade|fades|fading|blanch|blanches|go\s+away|goes\s+away|disappear|disappears|"
    r"turn\s+white|come\s+off|rub\s+off)\b",
    r"\b(?:doesn'?t|does\s+not|won'?t|wont)\s+(?:blanch|fade)\b",
    r"\bnon[\s-]?blanch\w*",
    r"\b(?:still|stays?|remains?|same)\b[^.?!]{0,20}\b(?:press\w*|glass|push\w*)\b",
    r"\b(?:press\w*|glass|push\w*)\b[^.?!]{0,25}\b(?:still|stays?|remains?|same|doesn'?t|"
    r"does\s+not|won'?t|wont)\b",
    r"\bunder\s+a\s+glass\b",
    r"\b(?:go|goes|going|went|come|comes|coming|came)\s+(?:back|straight\s+back)\b",
)

RASH_PRESSED = (
    r"\bnon[\s-]?blanch\w*",
    r"\b(?:doesn'?t|does\s+not|don'?t|dont|won'?t|wont|isn'?t|is\s+not|not)\s+blanch\w*",
    r"\b(?:doesn'?t|does\s+not|don'?t|dont|won'?t|wont|isn'?t|is\s+not|not)\s+"
    r"(?:fade|fades|fading|turn\s+white)\b[^.?!]{0,25}\b(?:press\w*|glass|push\w*)\b",
    r"\b(?:press\w*|glass|push\w*)\b[^.?!]{0,25}\b(?:doesn'?t|does\s+not|don'?t|dont|"
    r"won'?t|isn'?t|not)\s+(?:fade|blanch|turn\s+white)\b",
    r"\bunder\s+a\s+glass\b",
    r"\bsame\b[^.?!]{0,15}\bglass\b",
)

BLACKOUT_EFFORT = (
    r"\b(?:gym|workout|work\s?out|exercis\w*|training|treadmill|weights|crossfit|hiit|"
    r"spin(?:ning)?|rowing|rowing\s+machine|cross\s+trainer|running|runs|jog\w*|sprint\w*|"
    r"football|rugby|soccer|netball|hockey|tennis|badminton|squash|basketball|swim\w*|"
    r"cycling|cycled|cycle|bike|triathlon|marathon|park\s?run|match|sports?\s+day|"
    r"pe\s+lesson|games\s+lesson|climbing|hillwalk\w*|hiking)\b",
)

BLACKOUT_FLOOR = (
    r"\b(?:woke\s+up\s+on\s+the\s+(?:floor|ground|pavement|street)|"
    r"woke\s+on\s+the\s+(?:floor|ground)|came\s+round\s+on\s+the\s+(?:floor|ground)|"
    r"came\s+to\s+on\s+the\s+(?:floor|ground)|found\s+(?:him|her|them|my\s+\w+)\s+on\s+the\s+"
    r"(?:floor|ground)|on\s+the\s+floor\s+when\s+i\s+(?:woke|came\s+round|came\s+to))\b",
)

BLACKOUT_REPEAT = (
    r"\b(?:keep(?:s|ing)?\s+(?:on\s+)?(?:passing|blacking|faint\w*)|"
    r"(?:passed|blacked|faint\w*)\s+out\b[^.?!]{0,20}\bagain\b|"
    r"\b(?:twice|three\s+times|four\s+times|several\s+times|a\s+few\s+times|"
    r"\bover\s+and\s+over)\b[^.?!]{0,25}\b(?:passed\s+out|blacked\s+out|fainted)\b|"
    r"\b(?:passed\s+out|blacked\s+out|fainted)\b[^.?!]{0,25}\b(?:twice|again|"
    r"three\s+times|several\s+times|a\s+few\s+times)\b)",
)

BLACKOUT_BREATH = (
    r"\b(?:held|hold|holding)\b[^.?!]{0,20}\bbreath\b[^.?!]{0,40}"
    r"\b(?:too\s+long|until|till|and\s+(?:blacked|passed|fainted|went\s+under))\b",
)

BLACKOUT_SOMEONE_DOWN = (
    r"\bmy\s+(?:wife|husband|partner|mum|mom|mother|dad|father|son|daughter|child|kid|baby|"
    r"friend|mate|brother|sister|nan|gran|grandma|grandad|grandpa|neighbour|neighbor|flatmate|"
    r"colleague|boss|boyfriend|girlfriend)\b[^.?!]{0,30}\b(?:pass(?:ed)?\s+out|"
    r"black(?:ed)?\s+out|faint(?:ed)?|collapsed|went\s+limp|out\s+cold)\b",
)

BLACKOUT_A_THING = (
    r"\b(?:screens?|phones?|telly|tv|television|monitor|display|laptop|computer|system|server|"
    r"lights?|streetlights?|power|electricity|wifi|wi-?fi|signal|cameras?|windows?|curtains?|"
    r"blinds?|bulbs?|fuses?|projector|kindle)\b[^.?!]{0,30}\b(?:black(?:ed|ing)?\s+out|"
    r"keep(?:s|ing)?\s+blacking\s+out)\b",
    r"\bblack(?:ed|ing)?\s+out\b[^.?!]{0,20}\b(?:screens?|phones?|telly|tv|lights?|windows?|"
    r"curtains?|power|signal|monitor|camera)\b",
    r"\bkeep(?:s|ing)?\s+blacking\s+out\b[^.?!]{0,20}\b(?:screen|phone|telly|tv|monitor|"
    r"lights?|signal)\b",
)

BLACKOUT_OFF = (
    r"\b(?:hot\s+(?:room|day|bath|shower|weather)|heat|heatwave|blood\s+test|bloods|"
    r"giving\s+blood|gave\s+blood|donated\s+blood|blood\s+donor|needle|injection|jab|"
    r"vaccine|hungry|not\s+eaten|skipped\s+(?:breakfast|lunch|dinner|a\s+meal)|standing\s+up|"
    r"stood\s+up|got\s+up\s+too\s+fast|period|drunk|drinking|alcohol|hungover|hangover|"
    r"laughing|laughed|laughs|joke|film|movie|programme|episode|book)\b",
    r"\b(?:years?|months?)\s+ago\b",
)

STIFF_NECK = (
    r"\bstiff\s+neck\b", r"\bneck\s+(?:is|feels|has\s+gone|went)\s+(?:very\s+|so\s+|really\s+)?stiff\b",
    r"\bneck\s+stiffness\b", r"\bcan'?t\s+bend\s+(?:my|his|her|their|the)\s+(?:neck|chin)\b",
    r"\bchin\s+(?:is\s+)?(?:stuck|touching|on|to)\s+(?:my|his|her|their)\s+chest\b",
)

MENINGITIS_OTHER = (
    r"\bheadache\w*", r"\bhead\s+(?:is\s+)?(?:killing|banging|thumping|pounding|hurting|sore)\b",
    r"\bhead\s+hurts\b", r"\bmy\s+head\b",
    r"\blight\b", r"\bsunlight\b", r"\bbright\b", r"\brash\w*", r"\bspots?\b",
    r"\bconfus\w*", r"\bdrows\w*", r"\bvomit\w*", r"\bbeing\s+sick\b", r"\bthrowing\s+up\b",
    r"\bseizure\b", r"\bfloppy\b", r"\bunrespons\w*",
)

STIFF_FINE = (
    r"\bfrom\s+(?:sleeping|sleep|the\s+gym|work|the\s+computer|lifting|stress|the\s+pillow|"
    r"the\s+cold|a\s+cold|driving|the\s+desk|studying|gardening)\b",
    r"\bslept\s+(?:funny|awkward|badly|on\s+it)\b", r"\b(?:crick|kink)\s+in\s+(?:it|my\s+neck)\b",
    r"\bneck\s+(?:ache|pain)\s+(?:from|after)\b",
)

SEPSIS_SIGN = (
    r"\bconfus(?:ed|ion)\b", r"\bnot\s+making\s+sense\b", r"\bdrows\w*",
    r"\bvery\s+sleepy\b", r"\btoo\s+sleepy\b",
    r"\bhard\s+to\s+wake\b", r"\bwon'?t\s+wake\b", r"\bwont\s+wake\b", r"\bfloppy\b",
    r"\blimp\b", r"\bunrespons\w*", r"\bnot\s+themselves\b", r"\bnot\s+(?:him|her)self\b",
    r"\bbreathing\s+(?:fast|quickly|funny|strangely)\b", r"\bgrunting\b",
    r"\bblue\s+(?:lips?|round\s+the\s+lips?)\b", r"\bmottled\b", r"\blifeless\b",
    r"\bshivering\b", r"\bclammy\b", r"\bvery\s+cold\b",
)

NEWBORN = (
    r"\bnewborn\b", r"\bnew\s?born\b", r"\b\d+\s*(?:days?|weeks?)\s+old\b",
    r"\b(?:under|less\s+than|not\s+yet)\s+(?:3|three)\s+months?\b",
    r"\b(?:under|less\s+than|not\s+yet)\s+(?:2|two)\s+months?\b",
    r"\b(?:3|6)\s+weeks?\s+old\b",
    r"\b(?:is|only|just|nearly)\s+(?:1|2|one|two)\s+months?\b",
    r"\b(?:baby|newborn|infant|son|daughter|boy|girl|little\s+one)\b[^.?!]{0,12}"
    r"(?:is|only|just|nearly)\s+(?:[1-9]|1[0-2]|one|two|three|four|five|six|seven|eight|nine|"
    r"ten|eleven|twelve)\s+weeks?\b(?![-\s]*(?:pregnan\w*|along|into|of))",
    r"\b(?:1|2|one|two)[-\s]*months?[-\s]*old\b",
    r"\b(?:4|5|6|7|8|nine|nine|eight|seven|six|five|four)\s+weeks?\s+old\b",
)

DEVICE_OLD = (
    r"\b(?:oven|boiler|room|water|thermostat|fridge|freezer|shower|bath|heating|radiator|"
    r"washing\s+machine|tumble\s+dryer|air|weather|engine|car|kettle|dishwasher|mattress|sofa|"
    r"roof|carpet|house|flat|washing\s+machine|dryer|heater|fan|pump|motor)\b"
    r"[^.?!]{0,10}\b(?:is|was|are|were|only|just|nearly|now)\b[^.?!]{0,10}"
    r"\b\d+\s*(?:days?|weeks?)\s+old\b",
)

CONFUSED_THING = (
    r"\bconfus(?:ed|ion)\s+(?:about|by|with|over|on)\s+(?:(?:my|the|his|her|their|a|this|that)\s+)?"
    r"(?:\w+\s+){0,3}(?:homework|question|instructions?|settings?|app|recipe|exam|form|bill|tickets?|map|"
    r"directions|order|complaint|book|film|movie|email|message|answer|word|plan|tablets?|pills?|"
    r"meds|medication|insulin|doses?|dose|reading|reading[s]?|numbers?|labels?|charges?|"
    r"where|which|who|when|how)s?\b",
)

TINY_AGE = (
    r"\bnew\s?born\b", r"\bjust\s+born\b", r"\bonly\s+just\s+born\b",
    r"\b(?:1|2|3|4|5|6|7|8|9|10|11|12|one|two|three|four|five|six|seven|eight|nine|ten|eleven|"
    r"twelve)\s*(?:days?|weeks?)\s+old\b",
    r"\b(?:under|less\s+than|not\s+yet)\s+(?:3|three)\s+months?\b",
    r"\b(?:under|less\s+than|not\s+yet)\s+(?:2|two)\s+months?\b",
    r"\b(?:baby|babies|newborn|infant|son|daughter|boy|girl|little\s+one)\s+(?:is|was|now|only)\s+"
    r"(?:1|2|3|4|5|6|7|8|9|10|11|12|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)"
    r"\s*(?:days?|weeks?)\b",
)

OLDER_CHILD_NAMED = (
    r"\b(?:my|our)\s+(?:son|daughter|boy|girl|child|toddler|kid)\b[^.!?]{0,12}"
    r"\b(?:is|was|aged)\s+(?:\d|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"thirteen|fourteen|fifteen|sixteen)\b",
    r"\b(?:my|our)\s+(?:son|daughter|boy|girl|child|toddler|kid)\b[^.!?]{0,12}"
    r"\b(?:aged|age)\s+(?:\d|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\b",
)

TINY_AGE_FINE = (
    r"\b(?:1[3-9]|[2-9]\d)\s*weeks?\s+old\b", r"\b\d+\s+months?\s+old\b",
    r"\b\d+\s+years?\s+old\b", r"\bover\s+(?:3|three|6|six)\s+months\b",
    r"\b(?:1[3-9]|[2-9]\d|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty)"
    r"\s*weeks?\b",
)

ABOUT_THE_SPEAKER = (
    r"\bmy\s+(?:own\s+)?(?:temp|temps|temperature|fever)\b",
    r"\bi\s+(?:have|had|got|ve\s+got|am\s+running|feel|felt)\b.{0,24}"
    r"\b(?:temp|temps|temperature|fever|feverish|hot|boiling)\b",
    r"\bi\s*(?:'m|m)\s+(?:running\s+a\s+)?(?:a\s+)?(?:temp|temperature|fever|feverish|hot|boiling)\b",
    r"\bi\s+feel\s+(?:hot|feverish|boiling)\b",
    r"\bmine\s+(?:is|was)\b",
)

PALE_SECOND = (
    r"\bclammy\b", r"\bsweaty\b", r"\bshivery\b", r"\bshaking\b", r"\bsleepy\b",
    r"\bdrows\w*", r"\bfloppy\b", r"\blimp\b", r"\bconfus\w*", r"\bdizzy\b",
    r"\bvomit\w*", r"\bbeing\s+sick\b",
    r"\bnot\s+(?:him|her|them)self\b",
    r"\bsweat\w*\b",
    r"\bblue\b",
    r"\bvery\s+cold\b", r"\bcold\s+and\b", r"\bcold\s+hands\b",
    r"\band\s+(?:very\s+)?cold\b",
)

PALE_HEAT = (
    r"\b(?:from|in|out\s+in)\s+the\s+(?:heat|sun|sunshine)\b",
    r"\b(?:hot\s+day|heat\s?wave|sunbathing|sunburn\w*|greenhouse|conservatory)\b",
    r"\b(?:after|during|from|in|on)\s+(?:the\s+|a\s+|his\s+|her\s+)?(?:journey|car|train|"
    r"bus|coach|flight|plane|tube|heating|radiator|stuffy\s+room|hot\s+room|sunbed)\b",
)

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

PALE_EFFORT_RED = (
    r"\bfloppy\b", r"\blimp\b", r"\b(?:wont|won't|not|can't|cant|unable\s+to)\s+wake\b",
    r"\bunresponsive\b", r"\bunconscious\b", r"\bcollapsed\b", r"\bblue\b",
    r"\bgrey\b", r"\bgray\b", r"\bmottled\b", r"\bbreathing\s+(?:fast|quickly|hard)\b",
    r"\bgrunting\b", r"\bnot\s+breathing\b",
)

NAMED_SICK_FINE = (
    r"\bin\s+(?:hospital|icu|intensive\s+care|a\s+bed)\b", r"\bbeing\s+treated\b",
    r"\b(?:on|took|having)\s+antibiotics\b", r"\bantibiotics\b", r"\bhad\s+(?:it|this|"
    r"meningitis|sepsis|pneumonia)\b", r"\byears?\s+ago\b", r"\bwhen\s+(?:he|she|they)\s+"
    r"(?:was|were)\s+(?:little|a\s+baby|young|small|\d+)\b", r"\brecovered\b",
    r"\bgetting\s+better\b", r"\bnow\s+fine\b", r"\bback\s+in\s+\d{4}\b",
    r"\bis\s+(?:over|recovering)\b", r"\bcame\s+through\b", r"\bthankfully\b",
    r"\bin\s+(?:his|her|their|the)\s+(?:notes|file|records|chart|history)\b",
    r"\bhistory\s+of\b", r"\bwas\s+(?:treated|admitted|diagnosed)\b",
    r"\btreated\s+for\b", r"\bgot\s+over\b", r"\bfought\s+(?:it|that|this)\s+off\b",
    r"\bsurvived\b", r"\bdischarged\b", r"\bno\s+longer\b", r"\bused\s+to\b",
    r"\b(?:was|were|been)\s+ruled\s+out\b", r"\bruled\s+out\b", r"\bchecked\s+for\b",
)

FEVER_ASK = (r"^\s*(?:\w+\s+){0,2}(?:how|what|whats|what'?s|when|why|which|where|should|can|"
             r"could|do|does|will|would|shall)\b",
             r"^\s*(?:is|are|was|were|am|do|does)\s+(?:my|his|her|our|their|the|this|that|a|an)\b",)

FEVER_REPORT = (
    r"\b(?:has|have|had|got|is\s+running|is\s+reading|reading|reads|feels|felt|says|said|hit|"
    r"spiked|went\s+up\s+to|running)\b[^.?!]{0,16}\b(?:temperature|temps?|fever|feverish|hot)\b",
    r"\b(?:temperature|temp)\s+(?:is|was|reading|at|hit|spiked)\s*(?:\d|high|up|through\s+the\s+"
    r"roof)",
)

CHILD_SCHOOL_AGE = (
    r"\b(?:5|6|7|8|9|five|six|seven|eight|nine)\s*(?:year|yr)s?[-\s]*old\b",
    r"\b(?:my|his|her|their|our|the)\s+(?:son|daughter|boy|girl|child|kid|little\s+one)s?\s+"
    r"(?:is|was|aged|of)\s+(?:5|6|7|8|9|five|six|seven|eight|nine)\b"
    r"(?!\s*(?:month|week|day|yr\s*\d|mo\b))",
    r"\b(?:aged|age)\s+(?:5|6|7|8|9|five|six|seven|eight|nine)\b",
)

CHILD_FEVER_NOT_EATING = (
    r"\b(?:not|isnt|isn'?t|wasnt|wasn'?t|wont|won'?t|hasnt|hasn'?t|havent|haven'?t|never)"
    r"\s+(?:been\s+)?(?:eating|drinking|taking\s+(?:fluids?|drinks?|bottles?)|"
    r"had\s+(?:a\s+)?(?:drink|anything|fluids?))\b",
    r"\b(?:refus\w*|off\s+(?:his|her|their)\s+(?:food|drink|bottle|feeds?))\b",
    r"\bno\s+(?:appetite|interest\s+in\s+(?:food|drink))\b",
    r"\b(?:dehydrated|dried\s+out)\b",
)

CHILD_FEVER_RED = (
    r"\b(?:floppy|floppy\s+as\s+a\s+rag|drowsy|drowsier|unresponsive|unconscious|"
    r"wont\s+wake|won'?t\s+wake|hard\s+to\s+wake|limp|listless|not\s+(?:himself|herself|"
    r"themselves)|breathing\s+(?:fast|hard|quickly|badly)|struggling\s+to\s+breathe|"
    r"grunting|groaning|blue\s+lips|blotchy|mottled|stiff\s+neck|screaming|"
    r"inconsolable|seizure|fit|convulsion|shaking|shivering\s+hard)\b",
    r"\b(?:3[9]|4[0-3])(?:\.\d)?\b", r"\b(?:forty|thirty-nine)\b",
    r"\b(?:rash|spots|non[\s-]?blanching)\b",
    r"\b(?:not\s+drinking|wont\s+drink|won'?t\s+drink|refusing\s+to\s+drink|"
    r"not\s+taking\s+(?:fluids?|drinks?)|refusing\s+(?:drinks?|fluids?|the\s+bottle)|"
    r"keeps\s+(?:being\s+sick|throwing\s+up|vomiting)|being\s+sick|throwing\s+up|vomiting|"
    r"cant\s+keep\s+(?:fluids?|drinks?|water)\s+down|no\s+(?:wet\s+)?napp(?:y|ies)|"
    r"sunken\s+eyes)\b",
)

CHILD_GROWN = (
    r"\b(?:1[0-9]|[2-9]\d)\s*(?:year|yr)s?[-\s]*old\b",
    r"\b(?:my|his|her|their|our|the)\s+(?:son|daughter|boy|girl|child|kid|little\s+one)s?\s+"
    r"(?:is|was|aged|of)\s+(?:1[0-9]|[2-9]\d)\b",
    r"\b(?:aged|age)\s+(?:1[0-9]|[2-9]\d)\b",
    r"\b(?:teenager|teen|teens|adolescent)\b",
)

CHILD_YOUNG = (r"\b(?:toddler|baby|babies|infant|newborn|little\s+one|preschool|nursery|"
               r"\b\d+\s*(?:month|year)s?\s+old|\b(?:one|two|three|four|five|six|1|2|3|4|5|6)\s+"
               r"years?\s+old)\b",
               r"\b(?:my|his|her|their)\s+(?:son|daughter|boy|girl|kid|child|niece|nephew)\b"
               r"[^.?!]{0,12}\b(?:is|just|only|nearly|almost)\s+(?:one|two|three|four|1|2|3|4)\b")

RECENT_FIT_FINE = (
    r"\b(?:laughing|at\s+that|at\s+the\s+price|when\s+i\s+saw|when\s+i\s+heard|nearly|almost|"
    r"felt\s+like|thought\s+i\s+would)\b",
    r"\bfit\s+of\b", r"\b(?:every|each|once|twice|three\s+times|a\s+month|a\s+year|"
    r"regularly|sometimes|usually|last\s+year|years\s+ago|used\s+to)\b",
    r"\b(?:last\s+(?:week|month|summer|winter|spring|autumn)|weeks?\s+ago|months?\s+ago|"
    r"a\s+(?:few|couple)\s+(?:weeks|months)\s+ago|back\s+in\s+\d{4}|when\s+(?:he|she|they)\s+"
    r"(?:was|little)|as\s+a\s+(?:baby|kid|child))\b",
    r"\b(?:epilep\w+|condition|medication|meds|tablets?|keppra|epilim)\b",
)

GRUNTING_FINE = (
    r"\b(?:in\s+(?:his|her|their|its|the)\s+(?:sleep|cot|crib)|while\s+(?:a)?sleep\w*|asleep|"
    r"sleeping|at\s+night|when\s+sleeping|grunting\s+baby\s+syndrome)\b",
    r"\bgrunt(?:s|ing|ed)?\s+(?:at|over|about|through|in\s+reply)\b",
)

FEVER_RASH_FINE = (
    r"\b(?:heat|nappy|diaper|teething|teething|prickly\s+heat|sweat)\s+rash\b",
    r"\bchicken\s?pox\b", r"\bhand[,\s]+foot\b", r"\beczema\b", r"\bnettle\s+rash\b",
    r"\broseola\b", r"\bhas\s+had\s+it\s+before\b", r"\bfifth\s+disease\b",
    r"\bsixth\s+disease\b", r"\bfungal\b", r"\bthrush\b",
)

HYPO_STRONG = (
    r"\bsweat\w*", r"\bclammy\b", r"\bshak\w*", r"\btrembl\w*", r"\bdrows\w*",
    r"\bslurr\w*", r"\bwon'?t\s+wake\b", r"\bcan'?t\s+stay\s+awake\b",
    r"\b(?:a|another)\s+fit\b", r"\bseizure\w*", r"\bcoma\b", r"\bunconscious\b",
    r"\bpassed\s+out\b", r"\bfaint\w*", r"\bacting\s+(?:drunk|odd|strange|weird)\b",
)

HYPO_QUESTION = (
    r"\b(?:is|was)\s+(?:it|that)\s+(?:normal|ok|okay|safe|dangerous|common)\b",
    r"\bwhat\s+(?:can|could|should)\s+(?:i|he|she|they|we)\s+(?:eat|drink|have|snack)\b",
    r"\b(?:diet|recipes?|meal\s+(?:plan|ideas?)|what\s+to\s+cook)\b",
    r"\b(?:can|could|may|should)\s+(?:a\s+)?\bdiabetics?\b",
    r"\bdiabetics?\s+(?:eat|drink|have|take)\b",
    r"\b(?:symptoms?|signs?)\s+of\s+(?:a\s+)?(?:hypo\w*|low\s+blood\s+sugar)\b",
    r"\bhow\s+(?:common|likely|dangerous|many|often)\b",
    r"\bwhat\s+(?:does|do)\b[^.?!]{0,25}\b(?:feel|look|mean)\b",
)

HYPO_STRONG_OTHER = (
    r"\bsweat\w*", r"\bclammy\b", r"\bshak\w*", r"\btrembl\w*", r"\bdrows\w*",
    r"\bconfus\w*", r"\bdisorient\w*", r"\bslurr\w*", r"\b(?:a|another)\s+fit\b",
    r"\bseizure\w*", r"\bcoma\b", r"\bunconscious\b", r"\bpassed\s+out\b",
    r"\bfaint\w*", r"\bacting\s+(?:drunk|odd|strange|weird)\b",
    r"\bcan'?t\s+stay\s+awake\b", r"\bnot\s+making\s+(?:any\s+)?sense\b",
)

HYPO_HOW_KNOW = (
    r"\bhow\s+(?:do|can|could|would|will|should)\s+(?:i|you|we|he|she|they)\s+(?:know|tell|spot|"
    r"avoid|prevent|stop|reduce)\b",
    r"\bhow\s+to\s+(?:avoid|prevent|stop|spot|recognise|recognize)\b",
    r"\bwhat\s+does\b[^.?!]{0,25}\b(?:feel|look)\s+like\b",
    r"\b(?:avoid|avoiding|prevent|preventing|stop\s+myself|keep\s+(?:from|it\s+from)|"
    r"ward\s+off|less\s+likely)\b",
    r"\b(?:worried|worry|worrying|scared|afraid|frightened|anxious)\s+(?:about|of|that)\b",
    r"\b(?:risk\s+of|in\s+case\s+(?:i|he|she|they))\b",
)

OBJECT_IN_HEAD_THING = (
    r"(?:beads?|batter(?:y|ies)|lego|bricks?|peas?|beans?|sweets?|corn(?:flake)?s?|cereal|"
    r"raisins?|sultanas?|nuts?|peanuts?|popcorn|marbles?|stones?|pebbles?|seeds?|pips?|crayons?|"
    r"pencils?|erasers?|rubbers?|toys?|playmobil|rice|pasta|papers?|tissues?|plastic|coins?|"
    r"magnets?|insects?|bugs?|flies|fly|spiders?|earwigs?|moths?|crumbs?|"
    r"something|a\s+thing|anything)"
)

BONE_THROAT = (
    r"\b(?:fish\s?bone|fishbone|chicken\s+bone|lamb\s+bone|pork\s+bone|beef\s+bone|turkey\s+bone|"
    r"rabbit\s+bone|duck\s+bone|bone|bones)\b[^.?!]{0,25}"
    r"\b(?:stuck|caught|lodged|wedged|scraping|scratching|gone\s+down\s+the\s+wrong\s+way)\b",
    r"\b(?:stuck|caught|lodged|wedged)\b[^.?!]{0,20}\b(?:in|down)\s+(?:my|his|her|their|the|your)\s+"
    r"(?:throat|gullet|neck|windpipe)\b",
    r"\b(?:swallowed|swallowing|ate|eaten|eating|got\s+down)\b[^.?!]{0,20}\b(?:fish\s?bone|bone|bones)\b",
    r"\b(?:bone|bones|fishbone|shell|husk|pip|kernel)\b[^.?!]{0,15}\b(?:in|down)\s+(?:my|his|her|their)\s+"
    r"throat\b",
)

BONE_ORDINARY = (
    r"\b(?:stock|broth|soup|carcass|recipe|roast|gravy|stew|casserole|curry|fry|bake|baking)\b",
    r"\b(?:dog|cat|puppy|kitten|pup|parrot|pet|bird|hamster)\b",
    r"\b(?:broken|breaks?|broke|fractur\w*|density|marrow|graft|spur|cancer|cyst|scan|x-?ray|"
    r"hip|leg|arm|wrist|ankle|shoulder|knee|spine|back|ribs?|skull|jaw|toe|foot)\b[^.?!]{0,15}\bbone\b",
    r"\bbone\b[^.?!]{0,15}\b(?:density|loss|pain|graft|marrow|spur|china|dry|tired|idle|lazy)\b",
    r"\b(?:wishbone|backbone|bare\s+bones|no\s+bones\s+about|bone\s+of\s+contention|"
    r"bone\s+to\s+pick|funny\s+bone|t-?bone|herringbone)\b",
    r"\b(?:chew|chewed|chewing|gnaw\w*)\b[^.?!]{0,15}\bbone\b",
)

BONE_PAST = (
    r"\b(?:last|this)\s+(?:year|month|week|christmas|summer)\b",
    r"\b(?:years?|months?|weeks?)\s+(?:ago|back)\b", r"\bin\s+(?:19|20)\d\d\b",
    r"\b(?:as|when\s+i\s+was)\s+a\s+(?:kid|child|baby|teen|little\s+one)\b",
    r"\bused\s+to\b", r"\bwhen\s+i\s+was\s+(?:little|small|young)\b",
    r"\bages\s+ago\b",
)

OLD_PERSON = (
    r"\b(?:is|was|'s|s|at|turned)\s+(?:6[5-9]|[7-9][0-9]|1[0-2][0-9])\b",
    r"\b(?:i'?m|im|i\s+am)\s+(?:6[5-9]|[7-9][0-9]|1[0-2][0-9])\b",
    r"\b(?:6[5-9]|[7-9][0-9]|1[0-2][0-9])\s*(?:years?[\s-]?old|yrs?\s+old|yr[\s-]?old|yo)\b",
    r"\baged\s+(?:6[5-9]|[7-9][0-9]|1[0-2][0-9])\b",
    r"\bover\s+(?:65|70|75|80|85|90|95)\b",
    r"\b(?:in|into|on)\s+(?:his|her|their)\s+(?:mid[\s-]?)?(?:60s|70s|80s|90s)\b",
    r"\b(?:elderly|pensioner|oap)\b",
    r"\bold\s+(?:man|woman|lady|gentleman|chap|boy|girl|dear|soul|mum|dad|mother|father|"
    r"mam|gran|grandad|neighbou?r)\b",
    r"\b(?:gran|granny|nan|nana|grandma|grandmother|grandad|granddad|grandpa|grandfather)\b",
)

OLD_FALL_FINE = (
    r"\b(?:but|and|though)\s+(?:he|she|they|it)\s*(?:'s|s|\s+is|\s+was)?\s*(?:ok|okay|fine|"
    r"alright|all\s+right)\b",
    r"[,;]\s*(?:but\s+)?(?:hes|shes|theyre|he\s+is|she\s+is|they\s+are|he'?s|she'?s|they'?re)\s+"
    r"(?:now\s+)?(?:ok|okay|fine|alright|all\s+right)\b",
    r"\b(?:says?|said|tells?|told)\s+(?:me\s+)?(?:he|she|they)\s*(?:'s|s|\s+was|\s+is)?\s*"
    r"(?:ok|okay|fine|alright)\b",
    r"\b(?:nothing\s+broken|no\s+harm|just\s+bruised|only\s+bruised|walked\s+it\s+off|"
    r"laughed\s+it\s+off|laughed\s+about\s+it)\b",
    r"\b(?:had|got)\s+(?:it|him|her|them)\s+(?:checked|looked\s+at)\b",
    r"\b(?:seen|checked)\s+by\s+(?:the\s+)?(?:doctor|gp|nurse|paramedics?)\b",
    r"\b(?:been\s+)?(?:x-?rayed|x-?rays?)\b", r"\bin\s+(?:the\s+)?hospital\b",
    r"\b(?:has|have|had)\s+been\s+(?:seen|checked)\b",
)

FALL_HIP = (
    r"\b(?:fell|fallen|fall|falls|slipped|tripped|went\s+over|had\s+a\s+fall|toppled)\b"
    r"[^.?!]{0,45}\b(?:hip|pelvis)\b[^.?!]{0,25}\b(?:hurt\w*|pain\w*|sore|ache\w*|aching|"
    r"broke\w*|click\w*|stiff|gave\s+way|is\s+bad)\b",
    r"\b(?:hurt\w*|pain\w*|sore|ache\w*|aching|broke\w*|click\w*)\b[^.?!]{0,25}"
    r"\b(?:hip|pelvis)\b[^.?!]{0,45}\b(?:fell|fallen|fall|slipped|tripped|went\s+over|"
    r"had\s+a\s+fall)\b",
    r"\b(?:fell|fallen|fall|falls)\b[^.?!]{0,40}\b(?:hurt|broke\w*|injured|done|damaged)\b"
    r"\s+(?:his|her|their|my|the|a)\s+(?:hip|pelvis)\b",
)

OLD_FALL_NOT = (
    r"\bfell\s+(?:asleep|for\s+(?:it|him|her|them|the)|in\s+love|out\s+(?:with|over)|apart|"
    r"through|short|behind|flat|ill|silent|prey)\b",
    r"\bfell\s+(?:over\s+|about\s+)?laughing\b", r"\bwent\s+down\s+(?:well|badly|a\s+treat|like)\b",
    r"\bwent\s+over\s+on\s+(?:my|his|her|their)\s+(?:ankle|foot)\b",
    r"\bthe\s+(?:price|prices|market|temperature|rain|snow|share|shares)\b",
    r"\bfall(?:ing)?\s+(?:asleep|for|in\s+love|out|apart|through|short|behind)\b",
)

SHOT = (
    r"\b(?:has|have|had|been|got|gets|was|were)\s+(?:been\s+)?shot\b",
    r"\bshot\s+(?:him|her|them|me|my\s*self|himself|herself|themselves|in\s+the|through)\b",
    r"\bshot\s+(?:a\s+|the\s+)?(?:man|woman|person|boy|girl|kid|child|policeman|officer)\b",
    r"\b(?:gunshot|someone\s+shot|they\s+shot|he\s+shot|she\s+shot|shots\s+fired)\b",
)

SHOT_FINE = (
    r"\b(?:paintball\w*|bb\s+gun|airsoft|nerf|toy\s+gun|water\s+pistol|squirt\s+gun)\b",
    r"\b(?:flu|covid|tetanus|booster|vaccine|vaccination|immunisation|immunization|jab)s?\b",
    r"\b(?:photo|photograph|picture|film|movie|camera|scene|screenshot|screengrab|video)s?\b",
    r"\ba\s+shot\s+of\b", r"\bshot\s+glass(?:es)?\b", r"\bshot\s+put\b",
    r"\b(?:long|wide|close|medium)\s+shot\b", r"\bshot\s+(?:up|down)\b",
    r"\ba\s+shot\s+in\s+the\s+dark\b",
    r"\bshot\s+(?:my\s*self|him|her|them)sel(?:f|ves)\s+in\s+the\s+foot\s+(?:with|over|on)\s+"
    r"(?:that|this|the)\b",
    r"\b(?:goal|baskets?|balls?|penalt(?:y|ies)|hoop|free\s+kick|target|round|bird|rabbit|"
    r"deer|fox|pheasant|clay\s+pigeon)s?\b",
)

CHEM_WORD = (
    r"\b(?:acid|bleach|cleaners?|detergent|powder|powders|drain\s+cleaner|caustic|chemical\w*|"
    r"lye|ammonia|white\s+spirit|"
    r"paint\s+thinner|thinners?|solvent|oven\s+cleaner|petrol|paraffin|chlorine|antifreeze|"
    r"disinfectant|diesel|turpentine|nail\s+varnish\s+remover)\b"
)

EYE_CHEM = (
    CHEM_WORD[:-2] + r"[^.?!]{0,25}\b(?:in|into|inside|over)\s+(?:my|his|her|their|your|both|one|"
    r"the)\s+eyes?\b",
    r"\beyes?\b[^.?!]{0,20}\b(?:full\s+of|covered\s+in|splashed\s+with|with)\b"
    r"[^.?!]{0,15}" + CHEM_WORD,
    r"\b(?:splashed|squirted|sprayed|poured)\b[^.?!]{0,20}" + CHEM_WORD
    + r"[^.?!]{0,20}\b(?:in|into)\s+(?:my|his|her|their|your)\s+eyes?\b",
    r"\b(?:got|get|gets|getting|had|has|have|sprayed|spray|splashed|splash|poured|threw|squirted|"
    r"dabbed|rubbed|put|smeared|scooped)\b[^.?!]{0,30}"
    r"\b(?:washing\s+powder|washing\s+up\s+liquid|deodorant|hairspray|hair\s+spray|perfume|"
    r"aftershave|ac?etone|nail\s+varnish|superglue|glue|silicone|limescale|toilet\s+cleaner|"
    r"carpet\s+cleaner|screen\s+wash)\b[^.?!]{0,25}\b(?:eye|eyes)\b",
    r"\b(?:powder|powders|detergent|cleaner|cleaners|bleach|spray)\b[^.?!]{0,20}"
    r"\b(?:out of|in|into|off)\s+(?:my|his|her|their|your)\s+eyes?\b",
    r"\b(?:washing\s+powder|deodorant|hairspray|perfume|aftershave|nail\s+varnish|superglue|"
    r"limescale|toilet\s+cleaner)\b[^.?!]{0,30}\b(?:in|into|went)\b[^.?!]{0,12}"
    r"\b(?:my|his|her|their|the)\s+(?:\w+\s+)?eyes?\b",
)

EYE_FINE = (
    r"\b(?:acid\s+reflux|heartburn|acid\s+stomach|stomach\s+acid|acid\s+rain|acid\s+jazz|"
    r"amino\s+acids?|folic\s+acid|acid\s+test|acid\s+house|acid\s+wash)\b",
    r"\b(?:clean|cleaning|cleaned)\s+(?:the\s+|my\s+)?(?:bathroom|kitchen|oven|drain|shower|"
    r"toilet|windows?)\b",
    r"\b(?:keep|keeps|kept|store|stored|out\s+of\s+reach)\b[^.?!]{0,30}\beyes?\b",
)

FOOD_CUT = (
    r"\b(?:avocado|avocados|bread|cake|loaf|cheese|tomato|tomatoes|onion|onions|lettuce|salad|"
    r"cabbage|apple|apples|banana|bananas|lemon|oranges?|melon|mango|pepper|peppers|cucumber|"
    r"carrot|carrots|potato|potatoes|celery|fruit|herbs?|chilli|chillies|garlic|ginger|lemon|"
    r"lime|bacon|ham|chicken|beef|pork|lamb|fish|sausage|sausages|steak|meat|pizza|lasagne|"
    r"quiche|pie|sandwich|wrap|roll|bagel|pastry|croissant|melon|watermelon|pineapple|veg|"
    r"vegetables?|courgette|aubergine|broccoli|cauliflower|squash|pumpkin)\b",
)

HEADACHE_BAD = (
    r"\b(?:worst|bad|terrible|awful|severe|unbearable|splitting|thumping|excruciating)\b"
    r"[^.?!]{0,15}\bhead(?:ache)?\b",
    r"\bhead(?:ache)?\b[^.?!]{0,30}\b(?:worst|unbearable|severe|excruciating|terrible|"
    r"awful|bad)\b",
    r"\bworst\s+head(?:ache)?\s+of\s+my\s+life\b",
)

HEADACHE_SUDDEN = (
    r"\bsudden\w*", r"\bout\s+of\s+(?:nowhere|the\s+blue)\b", r"\ball\s+of\s+a\s+sudden\b",
    r"\bthunderclap\b", r"\bwithin\s+(?:a\s+)?(?:minute|seconds?)\b",
    r"\blike\s+a\s+(?:bang|clap|thunder|blow)\b", r"\bexploded\b",
    r"\bcame\s+on\b[^.?!]{0,15}\b(?:suddenly|fast|quickly|in\s+seconds|like)\b",
)

HEADACHE_STORY = (
    r"\b(?:not|isnt|isn'?t)\s+(?:that|too|so|very)\s+bad\b", r"\ba\s+bit\b", r"\bslight\w*",
    r"\bmild\b", r"\bmanageable\b", r"\bnot\s+too\s+bad\b",
    r"\b(?:last\s+(?:year|month|week)|years?\s+ago|when\s+i\s+was\s+(?:a\s+)?(?:kid|child|"
    r"little)|used\s+to|went\s+away|gone\s+now|had\s+one\s+before|still\s+there)\b",
    r"\b(?:hangover|migraine|dehydrat\w*|sinus\w*|hay\s?fever|screen|computer|tension\s+headache|"
    r"stress\w*|period|flu|cold|cough|headache\s+tablets?|paracetamol|ibuprofen)\b",
)

RASH_HEADACHE_FINE = (
    r"\b(?:heat|nappy|diaper|teething|prickly\s+heat|sweat|shav(?:e|ing)|razor|sunburn|"
    r"sun\s+burn|acne|hives|nettle|eczema|dermatitis|allerg\w*|hay\s?fever|thrush|fungal)\b"
    r"[^.?!]{0,15}\brash\b",
    r"\brash\b[^.?!]{0,15}\b(?:from|after|off)\s+(?:a\s+|the\s+|my\s+|her\s+|his\s+)?"
    r"(?:shav\w*|razor|wax\w*|sun|heat|perfume|new\s+cream|cream|washing\s+powder|plaster|"
    r"tape|nappy|diaper)\b",
    r"\b(?:rash|rashes|spots|marks|dots|blotches)\b[^.?!]{0,20}\b(?:from|after|off|where)\b",
    r"\b(?:chicken\s?pox|hand[,\s]+foot|roseola|fifth\s+disease|sixth\s+disease|shingles)\b",
    r"\b(?:had\s+it\s+before|last\s+(?:week|month|year)|weeks?\s+ago|years?\s+ago)\b",
    r"\b(?:spots|pimples|blackheads|whiteheads|zits|acne|breakouts?)\b[^.?!]{0,25}"
    r"\b(?:on|around|across)\s+(?:my\s+|his\s+|her\s+|their\s+|the\s+)?"
    r"(?:face|forehead|chin|cheeks?|nose|jaw|back|shoulders?)\b",
)

COUGH_BLOOD = (
    r"\b(?:cough\w*|spit\w*|bringing|bring)\b[^.?!]{0,20}\b(?:up|out)\b"
    r"[^.?!]{0,20}\bblood\b",
    r"\bblood\b[^.?!]{0,20}\b(?:when\s+i\s+cough|coughing|in\s+my\s+(?:sputum|phlegm|spit|"
    r"mucus))\b",
    r"\b(?:coughing|spitting)\s+(?:up\s+)?blood\b",
    r"\bbloody\s+(?:sputum|phlegm)\b",
)

BREATH_REST = (
    r"\b(?:suddenly|all\s+of\s+a\s+sudden|out\s+of\s+nowhere|out\s+of\s+the\s+blue|"
    r"just\s+now|came\s+on)\b.{0,30}"
    r"\b(?:short\s+of\s+breath|breathless|out\s+of\s+breath|can'?t\s+breath\w*|"
    r"struggling\s+to\s+breath\w*)\b",
    r"\b(?:short\s+of\s+breath|shortness\s+of\s+breath|breathless)\b.{0,30}"
    r"\b(?:sitting|sat\s+down|lying|in\s+bed|at\s+rest|resting|doing\s+nothing|"
    r"watching\s+tv|in\s+a\s+chair)\b",
)

SPIKED = (
    r"\b(?:drink|drinks|pint|glass|cocktail|bottle|water)\b[^.?!]{0,25}\b(?:was|got|is)\s+"
    r"(?:spiked|drugged|dosed)\b",
    r"\b(?:spiked|drugged|dosed)\s+(?:my|his|her|their|the|someone'?s)\s+(?:drink|drinks|pint|glass|"
    r"bottle|water)\b",
    r"\bi\s+(?:think\s+|reckon\s+|pretty\s+sure\s+)?(?:got|was|been)\s+(?:spiked|drugged|dosed)\b",
    r"\bsomeone\s+(?:put|slipped|dropped|spiked)\s+(?:something|a\s+pill|drugs?|roofies?)\s+"
    r"(?:in|into)\s+(?:my|his|her|their|the)\s+(?:drink|pint|glass|water|bottle)\b",
    r"\broofies?\b", r"\bdrink\s+was\s+spiked\b",
    r"\b(?:i|he|she|they|my\s+" + PERSON + r"|a\s+" + PERSON + r")\b(?![^.?!]{0,20}\bdrink\b)"
    r"[^.?!]{0,20}\b(?:got|was|were|been)\s+(?:spiked|drugged|dosed)\b",
)

HEARD_ASSAULT = (
    r"\b(?:screaming|screams|shouting|yelling|banging|smashing|glass\s+breaking|crashing)\b"
    r"[^.?!]{0,40}\b(?:hurting|hitting|beating|attacking|choking|dragging|kicking)\s+"
    r"(?:her|him|them|each\s+other|his\s+(?:wife|girlfriend|partner|kid|son|daughter)|"
    r"her\s+(?:husband|boyfriend|partner|kid|son|daughter))\b",
    r"\b(?:i\s+can\s+hear|i\s+heard|we\s+can\s+hear)\b[^.?!]{0,40}\b(?:screaming|shouting|"
    r"smashing|glass\s+breaking|banging|someone\s+crying)\b[^.?!]{0,40}\b(?:next\s+door|"
    r"upstairs|downstairs|neighbou?rs?|flat\s+above|flat\s+below|from\s+the\s+flat)\b",
    r"\b(?:my|our|the)\s+neighbou?rs?\b[^.?!]{0,40}\b(?:hurting|hitting|beating|attacking|"
    r"fighting|smashing\s+the\s+place)\b",
    r"\b(?:a\s+|some\s+)?(?:woman|man|girl|boy|kid|child|lady|bloke|fella|someone|somebody|"
    r"neighbou?r)\b[^.?!]{0,30}\b(?:screaming|sobbing|shouting\s+for\s+help|"
    r"crying\s+for\s+help|begging)\b[^.?!]{0,40}\b(?:next\s+door|upstairs|downstairs|"
    r"the\s+flat|the\s+house|the\s+street|outside\s+(?:my|our|the))\b",
)

BREATH_EFFORT = (
    r"\b(?:ran|run|running|jogged|jogging|sprinted|hurried|rushed|chased|cycled|raced|legged\s+it)\b"
    r"[^.?!]{0,25}\b(?:for|to|after|up|down)\s+(?:the\s+|a\s+|my\s+)?(?:bus|train|tram|tube|"
    r"coach|plane|flight|stairs|steps|ladder|hill)\b",
    r"\b(?:ran|jogged|sprinted|walked)\s+(?:up|down)\s+the\s+(?:stairs|steps|hill|road)\b",
)

EXERTION_CLASS = (
    r"\b(?:spin(?:ning)?|zumba|pilates|cross-?fit|box(?:ing)?|kickbox\w*|skipping|badminton|rugby|"
    r"cricket|hike|hiking|treadmill|cross-?trainer|elliptical|aerobics|hiit|circuit|rowing|"
    r"boot\s?camp|exercise\s+class|fitness\s+class|spin\s+class|aqua\s?aerobics|squash|"
    r"body\s?pump|body\s?combat|pt\s+session|gym\s+class)\b",
    r"\b(?:class|classes|session|workout)\b",
)

EFFORT_RED_HEART = (
    r"\b(?:faint\w*|dizzy|light-?headed|numb|tingl\w*|passed\s+out|"
    r"collapsed|blacked\s+out|vomit\w*|nause\w*|queasy|palpitations?|fluttering)\b",
    r"\b(?:feel|feels|feeling|felt)\s+(?:sick|ill|queasy|faint)\b",
    r"\b(?:arm|arms|jaw|shoulder|shoulders|neck)\b[^.?!]{0,20}"
    r"\b(?:hurt\w*|pain\w*|ache\w*|tight\w*|heavy|sore|numb)\b",
    r"\b(?:hurt\w*|pain\w*|ache\w*|tight\w*|heavy|sore)\b[^.?!]{0,15}"
    r"\b(?:arm|arms|jaw|shoulder|shoulders|neck)\b",
)

EFFORT_HEART_CLUSTER = (
    r"\b(?:clammy|light-?headed|dizzy|dizziness|faint\w*|woozy|queasy|nauseous|nausea)\b",
    r"\b(?:grey|gray|pale|ashy)\b[^.?!]{0,12}\b(?:face|skin|lips?)\b",
    r"\b(?:cold|damp|drench(?:ed|ing)|soaked|wet)\s+(?:with\s+|in\s+|and\s+)?(?:sweat\w*|clammy)\b",
    r"\bsweat\w*\b[^.?!]{0,24}\b(?:dizzy|light-?headed|faint\w*|woozy|sick|queasy|nauseous|"
    r"clammy)\b",
)

EFFORT_PATTERN = (
    r"\b(?:always|every\s+time|each\s+time|usually|normally|whenever)\b",
    r"\bfor\s+(?:months|years|weeks|ages|a\s+while)\b",
    r"\b(?:since|from)\s+(?:last\s+year|childhood|i\s+was\s+(?:a\s+)?(?:kid|child|younger|at\s+school))\b",
    r"\b(?:keeps?|kept)\s+(?:happening|coming\s+back|doing\s+it)\b",
    r"\bon\s+and\s+off\b",
)

EFFORT_BENIGN = (
    r"\b(?:pregnan\w*|expecting\s+a\s+baby|trimester)\b",
    r"\b(?:a|the|this|my)\s+(?:cold|flu|covid|coronavirus|chest\s+infection|virus)\b",
    r"\bhay\s?fever\b|\bpollen\b|\ballergie\w*\b|\bhistamine\b",
    r"\b(?:hot\s+day|heat\s?wave|in\s+this\s+heat|hot\s+weather|hot\s+building|boiling)\b",
    r"\b(?:unfit|out\s+of\s+shape|overweight|put\s+on\s+weight)\b",
)

EFFORT_TOO_LONG = (
    r"\b(?:for|it'?s\s+been|its\s+been|been|about|over|more\s+than|nearly|almost)\s+"
    r"(?:an?\s+hour|half\s+an\s+hour|(?:eleven|twelve|fifteen|twenty|twenty-five|thirty|forty|"
    r"fifty|sixty|\d{2,})\s*(?:min|mins|minutes?)|ages)\b",
    r"\b(?:over|more\s+than)\s+ten\s+minutes\b",
    r"\ball\s+(?:day|morning|afternoon|evening)\b",
)

BREATH_EFFORT_RED = (
    r"\b(?:blue|grey|gray|collapsed|unconscious|passed\s+out|crushing|crushed|chest\s+pain|"
    r"pins\s+and\s+needles|numb)\b",
    r"\b(?:still|now|and)\b[^.?!]{0,20}\b(?:can'?t|cannot|cant)\s+breathe\b",
    r"\b(?:can'?t|cannot|cant|unable\s+to)\s+(?:catch|get)\s+(?:my|her|his|their)\s+breath\b",
    r"\b(?:hours?|days?)\s+(?:later|ago)\b",
)

LIPS_SWELL = (
    r"\b(?:lips?|tongue|throat|face)\b[^.?!]{0,30}\b(?:swelling|swollen|swelled|puff\w*\s+up|"
    r"puffed\s+up|puffy|blowing\s+up)\b[^.?!]{0,40}"
    r"\b(?:sting\w*|bee|wasp|nut|nuts|peanut\w*|shellfish|food|medicine|antibiotic\w*|"
    r"prawn|egg|dairy|allerg\w*|throat|tongue|breath\w*|can'?t\s+swallow|epipen)\b",
    r"\b(?:sting\w*|bee|wasp|nut|peanut\w*|shellfish|food|antibiotic\w*|allerg\w*)\b"
    r"[^.?!]{0,40}\b(?:lips?|tongue|throat|face)\b[^.?!]{0,25}\b(?:swelling|swollen|swelled|"
    r"puff\w*|puffy)\b",
    r"\b(?:throat|tongue|uvula)\b[^.?!]{0,20}\b(?:swelling|swollen|closing|tight)\b",
    r"\b(?:tight|tightening)\s+throat\b",
)

LIPS_SWELL_BARE_OFF = (
    r"\b(?:cold\s+sore|chapped|chaps|dry\s+lips|chap\s?stick|lip\s+balm|piercing|"
    r"filler\w*|collagen|blister|ulcer|brace|braces|wisdom\s+tooth|gum|herpes|"
    r"bit\s+my\s+lip|bit\s+my\s+tongue|bite\s+my\s+lip|cut\s+my\s+lip|burnt\s+my\s+mouth|"
    r"hot\s+food|curry|chilli|hangover|dehydrated|kissed|kissing|numb)\b",
    r"\A(?![\s\S]*\b(?:faint\w*|dizz\w*|breath\w*|throat|tongue|wheez\w*|swallow\w*|"
    r"collaps\w*|vomit\w*|unconscious|itch\w*)\b)[\s\S]*"
    r"\b(?:yesterday|last\s+(?:night|week|month|year)|years?\s+ago|used\s+to|"
    r"always\s+(?:swells|does|goes)|as\s+a\s+(?:kid|child)|in\s+the\s+(?:cold|winter|sun)|"
    r"(?:from|because\s+of|after|with)\s+(?:the\s+)?(?:cold|wind|sun|weather|hayfever))\b",
    r"\A(?![\s\S]*\b(?:faint\w*|dizz\w*|breath\w*|throat|tongue|wheez\w*|swallow\w*|"
    r"collaps\w*|vomit\w*|unconscious|itch\w*|swollen\s+(?:shut|closed))\b)"
    r"[\s\S]*\blips?\b[^.?!]{0,25}\bin\s+(?:the\s+)?(?:cold|wind|sun|winter)\b",
    r"\A(?:if|when|what\s+if|should\s+i|would)\b",
    r"\A(?![\s\S]*\b(?:throat|tongue|uvula|breath\w*|wheez\w*|swallow\w*|faint\w*|dizz\w*|collaps\w*|unconscious|sting\w*|stung|bee|wasp|hives|itch\w*|vomit\w*|reaction|allerg\w*|epipen|shut)\b)"
    r"[\s\S]*\b(?:face|eyes?|lips?)\b[^.?!]{0,30}\b(?:from|after|because\s+of|with)\s+(?:all\s+(?:the|that|my)\s+)?(?:crying|sobbing|a\s+good\s+cry)\b",
    r"\A(?![\s\S]*\b(?:throat|tongue|uvula|breath\w*|wheez\w*|swallow\w*|faint\w*|dizz\w*|collaps\w*|unconscious|sting\w*|stung|bee|wasp|hives|itch\w*|vomit\w*|reaction|allerg\w*|epipen|shut)\b)"
    r"[\s\S]*\b(?:i\s+(?:have\s+|had\s+|was\s+|been\s+|just\s+)?(?:cried|crying|sobbed|sobbing)|(?:cried|crying|sobbing)\s+so\s+much)\b[^.?!]{0,30}\b(?:face|eyes?|lips?)\b[^.?!]{0,25}\b(?:puffy|puffed\s+up|swollen|swelling|swelled|blotchy|red)\b",
    r"\b(?:what|should)\s+(?:do\s+)?i\s+do\s+if\b",
)

LIPS_TINGLE = (
    r"\b(?:lips?|tongue|mouth|throat|face)\b[^.?!]{0,25}\b(?:tingl\w*|pins\s+and\s+needles|"
    r"itch\w*|prickl\w*|numb(?:ness|ed|ing|s)?)\b",
    r"\b(?:tingl\w*|pins\s+and\s+needles|itch\w*|prickl\w*|numb(?:ness|ed|ing|s)?)\b[^.?!]{0,25}"
    r"\b(?:lips?|tongue|mouth|throat|face)\b",
    r"\bthroat\b[^.?!]{0,20}\b(?:feels?|is|going|getting)\s+(?:a\s+bit\s+|a\s+little\s+|"
    r"really\s+|very\s+|so\s+|properly\s+)?(?:funny|odd|weird|strange|thick|funny\s+feeling)\b",
)

STING_SETTLED = (
    r"\b(?:im|i'?m|i\s+am|its|it'?s|it\s+is|that'?s|thats)\s+(?:all\s+)?(?:fine|ok|okay|"
    r"better|gone|settled|passed|over|cleared\s+up)\s+now\b",
    r"\b(?:it|that)\s+(?:has\s+|'?s\s+|is\s+)?(?:passed|worn\s+off|gone\s+off|settled|"
    r"cleared\s+up)\b",
    r"\b(?:feel|feeling)\s+(?:fine|ok|okay|better)\s+now\b",
)

LIPS_TINGLE_FOOD = (
    r"\b(?:ate|eaten|eating|eats|swallowed)\b",
    r"\b(?:after|since)\s+(?:the\s+|my\s+|a\s+|that\s+)?(?:takeaway|take-?out|meal|dinner|"
    r"lunch|breakfast|snack|dessert|pudding|cake|sushi|curry|pizza|pasta|sandwich|salad|"
    r"noodles|rice|fish|chips|shellfish|prawns?|nuts?|peanut\w*|fruit|berries|strawberr\w*|"
    r"kiwi|mango|avocado|tomato|egg|eggs|milk|cheese|soy|bread|wheat|honey|wine|beer)\b",
)

LIPS_TINGLE_RED = (
    r"\b(?:swell\w*|swollen|puff(?:ed|y)?|bloat\w*)\b",
    r"\breaction\b", r"\bepipen\b", r"\banaphyla\w*\b",
    r"\b(?:faint\w*|dizzy|light\s?headed|giddy|collapse\w*|passing\s+out)\b",
    r"\b(?:breath\w*|wheez\w*|stridor|throat\s+(?:tight|closing))\b",
    r"\b(?:vomit\w*|throwing\s+up|sick)\b",
    r"\b(?:thick|thickened|thickening|heavy|wooden|rubbery)\b[^.?!]{0,20}"
    r"\b(?:tongue|lips?)\b",
    r"\b(?:tongue|lips?)\b[^.?!]{0,20}\b(?:feels?|is|has\s+gone|has\s+got|going)\s+"
    r"(?:a\s+bit\s+|a\s+little\s+|really\s+|very\s+|so\s+|all\s+)?(?:thick|thickened|"
    r"thickening|heavy|wooden|rubbery)\b",
)

LIPS_TINGLE_OFF = (
    r"\b(?:dentist|dental|hygienist|filling|root\s+canal|tooth\s+out|wisdom\s+tooth|"
    r"injection|anaesthetic|anesthetic|numbing\s+gel|novocaine|lidocaine)\b",
    r"\b(?:panic|panicking|panic\s+attack|anxiety|anxious|hyperventilat\w*|over-?breath\w*|"
    r"breathing\s+too\s+fast|shaking|palpitations)\b",
    r"\b(?:hands?|fingers?|fingertips|feet|toes?|arms?|legs?)\b"
    r"(?:(?!\b(?:lips?|tongue|mouth|throat|face)\b)[^.?!]){0,30}"
    r"\b(?:tingl\w*|numb(?:ness|ed|ing|s)?|pins\s+and\s+needles|prickling)\b",
    r"\b(?:tingl\w*|numb(?:ness|ed|ing|s)?|pins\s+and\s+needles|prickling)\b"
    r"(?:(?!\b(?:lips?|tongue|mouth|throat|face)\b)[^.?!]){0,30}"
    r"\b(?:hands?|fingers?|fingertips|feet|toes?|arms?|legs?)\b",
    r"\b(?:cold\s+sore|cold\s+weather|in\s+the\s+cold|out\s+in\s+the\s+cold|wind|sunburn|"
    r"chapped|freezing|numb\s+with\s+the\s+cold)\b",
    r"\b(?:b12|vitamin\s+b12|deficien\w*|multiple\s+sclerosis|\bms\b|migraine|nerve\s+damage|"
    r"carpal|raynaud\w*)\b",
)

SWALLOW_GONE_OFF = (
    r"\b(?:pills?|tablets?|capsules?|medicines?|medicine|supplements?|vitamins?)\b",
    r"\b(?:pride|insult|my\s+words?|his\s+words?)\b",
    r"\b(?:dog|dogs|puppy|cat|cats|kitten|rabbit|hamster|guinea\s+pig|horse|pony|bird|parrot|"
    r"budgie|pet|pets)\b",
    r"\b(?:bone|fishbone|gristle|a\s+bit\s+of\s+(?:food|meat|steak|bread)|food)\b"
    r"[^.?!]{0,30}\b(?:stuck|sticking|caught|lodged|went\s+down\s+the\s+wrong)\b",
    r"\b(?:stuck|sticking|lodged|caught)\b[^.?!]{0,30}\b(?:throat|gullet|windpipe)\b",
    r"\b(?:fish\s*bone|bone)\b",
    r"\b(?:swallowed|gulped)\b",
)

SWALLOW_GONE_RED = (
    r"\b(?:drool\w*|dribbl\w*)\b",
    r"\b(?:lips?|tongue|throat|uvula|neck)\b[^.?!]{0,24}\b(?:swell\w*|swollen|closing|thick)\b",
    r"\b(?:swell\w*|swollen|puff\w*)\b[^.?!]{0,24}\b(?:lips?|tongue|throat|neck)\b",
    r"\b(?:muffled|no\s+voice|voice\s+(?:has\s+)?gone|lost\s+my\s+voice)\b",
    r"\b(?:my\s+(?:own\s+)?spit|saliva)\b",
)

THROAT_TIGHT_CAUSE = (
    r"\b(?:nervous|anxious|anxiety|worried|interview|presentation|speech|exam|speaking\s+up)\b",
    r"\b(?:blocked\s+nose|nose\s+is\s+blocked|stuffy|stuffed\s+up|bunged\s+up|bunged|"
    r"runny\s+nose|nose\s+(?:is\s+)?running|congest\w*|sinus\w*|hayfever|hay\s+fever|"
    r"allerg\w*)\b",
    r"\b(?:in\s+the\s+morning|first\s+thing|when\s+i\s+wake\s+up|on\s+waking|at\s+night)\b",
    r"\b(?:run|running|ran|jog\w*|exercise|workout|gym|swim\w*|cycl\w*|bike|cardio|"
    r"football|rugby|netball|hockey|squash|tennis|lifting|weights|sprinting|training)\b",
    r"\b(?:sore|croaky|hoarse|dry|scratchy)\s+throat\b",
    r"\b(?:singing|sang|shouted|shouting|talking\s+all\s+day|yesterday|last\s+night|"
    r"weeks?\s+ago|for\s+days|hayfever|hay\s+fever|allergies|post\s?nasal|reflux|"
    r"silent\s+reflux|tonsils?|tonsillitis|strep|cold|flu|covid)\b",
    r"\b(?:sometimes|occasionally|now\s+and\s+then)\b",
)

THROAT_TIGHT_EFFORT = (
    r"\b(?:when|while|after|during)\s+(?:i\s+|im\s+|i'?m\s+)?(?:run|running|jog\w*|exercis\w*|"
    r"workout|swim\w*|cycl\w*|train\w*|lift\w*|row\w*|climb\w*)\b",
    r"\b(?:after|during|in)\s+(?:a|the|my)\s+(?:run|jog|workout|swim|cycle|ride|game|match|class|"
    r"session|training|race)\b",
    r"\b(?:gym|swimming|cycling|cardio|football|rugby|netball|hockey|squash|tennis|aerobics|"
    r"spin\s+class|bike\s+ride|long\s+run|sprints?|weights|lifting|hiit)\b",
)

THROAT_TIGHT_RED = (
    r"\b(?:tongue|uvula)\b",
    r"\b(?:swell\w*|swollen|puff(?:ed|y)?|bloat\w*)\b[^.?!]{0,30}"
    r"\b(?:lips?|tongue|face|eyelids?|throat|uvula)\b",
    r"\b(?:lips?|face|eyelids?)\b[^.?!]{0,30}\b(?:swell\w*|swollen|puff(?:ed|y)?)\b",
    r"\b(?:can'?t|cannot|couldn'?t|hard\s+to|difficult\s+to|difficulty)\s+"
    r"(?:swallow|breathe|breath)\b",
    r"\b(?:breath\w*|wheez\w*|stridor|epipen|anaphyla\w*)\b",
    r"\bthroat\b[^.?!]{0,12}\b(?:is|feels?|'s|was)?\s*(?:closing|closed|shutting|clamped)\b",
    r"\b(?:closing|closed)\s+(?:up\s+)?my\s+throat\b",
    r"\bvoic\w*\b[^.?!]{0,20}\b(?:gone|going|changed|changing|different|hoarse|raspy)\b",
    r"\b(?:lips?|tongue|mouth|face)\b[^.?!]{0,20}\b(?:tingl\w*|numb(?:ness|ed|ing|s)?|prickl\w*)\b",
    r"\b(?:peanuts?|nuts?|shellfish|prawns?|bee|wasp|sting\w*|stung|penicillin|antibiotic\w*)\b",
)

NOT_A_WOUND_OFF = (
    r"\bit\b",
    r"\b(?:pen|ink|printer|paint|brush|steak|meat|chicken|beef|lamb|sausage|burger|cake|"
    r"tomato|beetroot|cherry|berry|berries|fruit|juice|sauce|jam|dye|radiator|pipe|tap|boiler|"
    r"ceiling|mattress|wall|drain|nail\s+varnish)\b",
)

NOSE_RED = (
    r"\b(?:won'?t|wont|doesn'?t|doesnt|isn'?t|not)\s+stopp?(?:ed|ing)?\b",
    r"\bkeeps?\s+(?:on\s+)?bleeding\b", r"\bstill\s+bleeding\b",
    r"\b(?:half\s+an?\s+hour|an?\s+hour|hours|two\s+hours|twenty\s+minutes|20\s+minutes|"
    r"ten\s+minutes|10\s+minutes|fifteen\s+minutes|15\s+minutes)\b",
    r"\b(?:pale|grey|gray|dizzy|faint|fainted|fainting|clammy|sweaty|unconscious|shaking)\b",
    r"\b(?:blood\s+thinners?|warfarin|clopidogrel|apixaban|rivaroxaban|aspirin|heparin)\b",
    r"\b(?:after|from)\s+(?:a\s+|the\s+)?(?:bang|blow|knock|hit|bump|fall|punch|punching|"
    r"thump|smack)\b",
    r"\bhit\s+(?:my|his|her|their|the)\s+(?:head|face|nose)\b",
    r"\b(?:nose|nosebleed)\b.{0,25}\b(?:broken|fractured|crooked|out\s+of\s+place)\b",
)

MOUTH_BLEED_NOW = (
    r"\b(?:won'?t|wont|doesn'?t|doesnt)\s+stopp?(?:ed|ing)?\b",
    r"\bnot\s+stopp?ing\b", r"\bkeeps?\s+(?:on\s+)?bleeding\b",
    r"\bstill\s+bleeding\b", r"\bwon'?t\s+stop\s+bleeding\b",
    r"\bbleeding\s+(?:a\s+lot|badly|loads|everywhere)\b", r"\bbleeding\s+all\s+over\b",
    r"\bblood\s+in\s+(?:my|his|her|their)\s+mouth\b",
)

_THIRD = {"feel": "feels", "keep": "keeps", "seem": "seems", "get": "gets", "go": "goes",
          "need": "needs", "stop": "stops", "look": "looks", "come": "comes", "start": "starts",
          "do": "does", "have": "has", "are": "is", "were": "was", "aren't": "isn't",
          "weren't": "wasn't"}

PREGNANCY_WORDS = (r"(?:pregnant|pregnancy|expecting\s+a\s+baby|weeks?\s+pregnant|baby\s+due|"
                   r"\d+\s+weeks?\s+(?:along|gone|in)|"
                   r"(?:^|\b)(?:i'?m|im|i\s+am|my\s+(?:wife|girlfriend|partner|fiancee|"
                   r"fianc\w+))(?:\s+is|\s+was)?\s+\d+\s+weeks?\b"
                   r"(?!\s+(?:into|old|ago|in|since|on|of|back)\b))")

SOCKET_OBJECT = (r"\b(?:fingers?|fingertips?|fork|forks|knife|knives|scissors|nails?|pins?|"
                 r"paper\s?clips?|screwdrivers?|hair\s?pins?|keys?|coins?|sticks?|pens?|"
                 r"pencils?|toys?|metal|wire|needles?|blades?|tools?|utensils?|spoons?|"
                 r"chopsticks?|tweezers|batter(?:y|ies)|earbuds?|bracelet|necklace)\b",)

SOCKET_THING_FINE = (
    r"\b(?:adapter|adaptors?|travel|holiday\s+home|abroad|in\s+(?:spain|france|greece|italy|"
    r"portugal|turkey|america|the\s+us)|type\s+[a-o]\b|voltage)",
    r"\b(?:loose|wobbly|cracked|broken|fallen\s+off|came\s+off|replac\w*|rewir\w*|"
    r"install\w*|fit\s+(?:a|the)\s+(?:new\s+)?socket|electrician|extends?\s+the\s+socket|"
    r"extension\s+lead|surge)",
    r"\b(?:years?\s+ago|last\s+(?:year|decade|century)|when\s+i\s+was\s+(?:a\s+)?(?:kid|"
    r"child|little|small|young)|as\s+a\s+(?:kid|child)|in\s+the\s+(?:19|20)\d\d)",
    r"\b(?:how\s+(?:does|do)\s+(?:a|the)\s+socket\s+work|wiring|wire|which\s+plug|"
    r"plug\s+on\s+a\s+(?:wire|cable|lead)|fuse\s+in\s+the\s+plug)\b",
)

ELECTRIC_SHOCK_DOWN = (
    r"\b(?:not|isn'?t|isnt|is\s+not|wasn'?t|wasnt|was\s+not|stopped|stop|stops|won'?t|wont)"
    r"\s+(?:breathing|breath\w*)\b",
    r"\b(?:not|isn'?t|isnt|is\s+not)\s+(?:breathing|breath\w*)\b",
    r"\bno\s+(?:pulse|breath\w*|heartbeat)\b",
    r"\b(?:unconscious|unresponsive|knocked\s+out|passed\s+out|passing\s+out|out\s+cold|"
    r"collapsed|collaps\w*|in\s+a\s+heap|limp|floppy|blue\s+lips|going\s+blue)\b",
    r"\b(?:cpr|resuscitat\w*|revive\w*|recovery\s+position|defib\w*|heart\s+stopped)\b",
    r"\b(?:is|isnt|isn'?t)\s+not\s+responding\b|\bnot\s+responding\b",
)

SHOCK_ANY = (
    r"\b(?:got|get|gets|getting|had|has|have|having|took|taken|suffered|given|gave|felt)\s+"
    r"(?:me\s+|him\s+|her\s+|them\s+)?(?:a\s+|an\s+|the\s+)?(?:\w+\s+){0,2}shock\b",
    r"\bshock(?:ed)?\b",
    r"\b(?:zapped|electrocut\w*)\b",
    r"\blive\s+(?:wire|cable|rail|terminal)\b",
)

ELECTRIC_SHOCK_DEFINITION = (
    r"\b(?:what|why|how)\s+(?:is|are|causes?|caused|does|do|did)\b[^.?!]{0,30}\bshock\b",
    r"\bshock\b[^.?!]{0,20}\b(?:(?<!at\s)(?<!from\s)(?<!of\s)work|works|happen|happens|"
    r"affect|affects|do\s+to|does\s+to|cause|causes)\b",
    r"\b(?:explain|definition\s+of|meaning\s+of)\b[^.?!]{0,25}\bshock\b",
)

POO_BLOOD = (
    r"\bblood\s+in\s+(?:my|his|her|their|the)\s+(?:poo|poo's|poop|stool|stools|shit|bowel\s+"
    r"movement|number\s+two|toilet|loo)\b",
    r"\b(?:pooed|pooped|crapped)\s+(?:out\s+)?(?:some\s+)?blood\b",
    r"\bblood\s+came\s+out\s+(?:when|after)\s+(?:i|he|she|they)\s+(?:pooed|pooped|went)\b",
    r"\b(?:poo|poop|stool|stools|shit|diarrhoea|diarrhea)\b[^.?!]{0,20}"
    r"\b(?:with|has|had|have|containing|covered\s+in)\b[^.?!]{0,10}\bblood\b",
    r"\bbloody\s+(?:poo|poop|stool|stools|shit|diarrhoea|diarrhea|bowel\s+movement)\b",
    r"\bred\s+blood\s+(?:in|on)\s+(?:the\s+)?(?:toilet|paper|loo|pan)\b",
    r"\b(?:when\s+i\s+wipe|when\s+he\s+wipes|when\s+she\s+wipes|after\s+i\s+wipe)\b"
    r"[^.?!]{0,25}\bblood\b",
)

POO_BLACK = (
    r"\b(?:poo|poop|stool|stools|shit|number\s+two)\b[^.?!]{0,20}\b(?:is|are|was|were|went|"
    r"has\s+gone|have\s+gone|looks?|looked|turned|come\s+out)\s+(?:all\s+)?(?:black|tarry|"
    r"tar-?like|like\s+tar|dark\s+(?:red|reddish))\b",
    r"\b(?:black|tarry)\s+(?:and\s+tarry\s+)?(?:poo|poop|stool|stools|shit|diarrhoea|"
    r"diarrhea)\b",
    r"\b(?:poo|poop|stool|stools|shit|bowel\s+movement)\b[^.?!]{0,30}\b(?:black|tarry|"
    r"tar-?like|like\s+tar)\b",
    r"\b(?:tarry|black)\s+(?:poo|poop|stool|stools|shit)\b",
    r"\b(?:melaena|melena)\b",
)

POO_FINE = (
    r"\b(?:blood\s+sugar|blood\s+pressure|blood\s+test|blood\s+group|bloody\s+murder|"
    r"bloody\s+hell|blood\s+money)\b",
    r"\b(?:iron\s+(?:tablets?|pills?|supplements?|infusion)|ferrous|bismuth|pepto|charcoal\s+"
    r"tablets?|kaolin)\b",
    r"\b(?:black\s+pudding|black\s+beans?|black\s+currents?|blackberries|blueberries|"
    r"beetroot|beet\s+juice|licorice|liquorice|spinach|food\s+colouring)\b",
    r"\b(?:stool\s+test|test\s+kit|screening\s+kit|bowel\s+screening|fit\s+kit|"
    r"faecal\s+immunochemical|colonoscopy|endoscopy)\b",
    r"\b(?:years?\s+ago|decades?\s+ago|as\s+a\s+kid|when\s+i\s+was\s+(?:a\s+)?(?:kid|child|"
    r"little)|in\s+(?:a|the)\s+film|on\s+tv)\b",
    r"\b(?:my|the|our)\s+(?:dog|cat|puppy|kitten|rabbit|hamster|guinea\s+pig|horse|bird|"
    r"parrot|budgie|pet)s?\b",
)

STOOL_LONG = (
    r"\b(?:for\s+(?:a\s+|the\s+last\s+|about\s+a\s+|over\s+a\s+|nearly\s+a\s+)?(?:\d+\s+)?"
    r"(?:week|weeks|month|months|year|years))\b",
    r"\b(?:since\s+(?:i\s+was\s+\w+|christmas|last\s+year|the\s+summer)|years\s+now|"
    r"months\s+now|weeks\s+now|a\s+while\s+now|ages|all\s+my\s+life|on\s+and\s+off)\b",
)

TORSION = (
    r"\b(?:testicle|testicles|testis|ball|balls|ball\s+sack|ballsack|scrotum|scrotal|bollock|"
    r"bollocks|nad|nads|nuts)\b[^.?!]{0,30}\b(?:pain|painful|achy|ache|aching|sore|swollen|"
    r"swelling|tender|lump|twisted|hard|heavy|torsion|hurts?|hurting)\b",
    r"\b(?:testicle|testicles|testis|ball|balls|bollock|bollocks|scrotum|nad|nads)\b"
    r"[^.?!]{0,25}\b(?:woke|woken|wakes|waking)\b[^.?!]{0,15}\b(?:me|him|her|them)\b",
    r"\b(?:pain|ache|swelling|swollen|lump|tender|tenderness|hurt\w*)\b[^.?!]{0,20}\b(?:in|of|on|at)\s+"
    r"(?:my|his|her|their|one|the)\s+(?:testicle|testicles|ball|balls|ball\s+sack|scrotum|"
    r"bollock|side\s+of\s+the\s+scrotum)\b",
    r"\b(?:one|a)\s+(?:of\s+my\s+|of\s+his\s+|of\s+her\s+)?(?:ball|testicle|bollock)s?\b"
    r"[^.?!]{0,20}\b(?:bigger|swollen|sore|hurts?|aching|tender)\b",
    r"\b(?:testicle|testicles|testicular|testis|ball|balls|bollock)\b[^.?!]{0,25}"
    r"\b(?:torsion|twisted)\b",
    r"\btesticular\s+torsion\b",
    r"\btorsion\s+(?:in|of)\s+(?:the|my|his|her|their)\s+(?:testicle|ball)\b",
    r"\b(?:sore|swollen|painful|tender|hard|twisted)\b[^.?!]{0,20}\b(?:testicle|testicles|"
    r"scrotum|bollock|ball|balls)\b",
)

TORSION_FINE = (
    r"\b(?:blue\s+balls|jock\s+itch|athletes?\s+foot|sweaty|itch\w*|chafe\w*|chafing|"
    r"shaving|shaved|wax\w*|trim\w*|razor|rash|dry\s+skin|fungal|thrush|spots?|pimples?)\b",
    r"\b(?:after|from)\s+(?:cycling|the\s+bike|a\s+bike\s+ride|a\s+long\s+ride|the\s+gym|"
    r"the\s+squat\s+rack|football|running|a\s+run|sex|the\s+marathon|riding)\b",
    r"\bwhen\s+(?:i|he|she|they)\s+(?:run|cycle|ride|train|lift|walk|swim)\b",
    r"\b(?:how\s+(?:do|should)\s+i\s+check|self\s+exam|check(?:ing)?\s+(?:them|it)\s+for|"
    r"testicular\s+cancer\s+(?:awareness|check|screening)|what\s+causes\s+testicular)\b",
)

TESTIS_LUMP = (
    r"\b(?:lump|lumps|bump|bumps|hard\s+spot|pea-?sized)\b",
    r"\b(?:one|a)\s+(?:of\s+(?:my|his|her|their)\s+)?(?:ball|testicle|bollock)s?\b"
    r"[^.?!]{0,25}\b(?:bigger|larger|enlarged|different)\b",
    r"\b(?:bigger|larger|enlarged)\b[^.?!]{0,20}\b(?:than\s+the\s+other|ball|testicle)\b",
)

TORSION_ONSET = (
    r"\b(?:sudden\w*|all\s+of\s+a\s+sudden|out\s+of\s+nowhere|came\s+on|come\s+on|"
    r"started|start(?:s|ing)?|woke|woken|wakes|overnight|last\s+night|this\s+morning|"
    r"this\s+afternoon|an?\s+hour\s+ago|few\s+hours|just\s+now|right\s+now|now\s+(?:sore|swollen|"
    r"hurting|painful)|one\s+side|on\s+one\s+side|since\s+(?:this|"
    r"last)\s+(?:morning|night)|in\s+the\s+last\s+(?:hour|few\s+hours))\b",
)

PUNCTURE = (
    r"\b(?:stepped|stood|trod|trodden)\b[^.?!]{0,20}\b(?:on|in)\b[^.?!]{0,20}"
    r"\b(?:a\s+|the\s+|some\s+)?\b(?:nail|screw|tack|needle|glass|barbed\s+wire|spike|thorn)\b",
    r"\b(?:nail|screw|tack|needle|spike|thorn|piece\s+of\s+glass)\b[^.?!]{0,25}"
    r"\b(?:through|into|in)\s+(?:my|his|her|their)\s+"
    r"(?:foot|shoe|boot|trainer|sock|hand|hand|palm|leg)\b",
    r"\b(?:nail|screw|needle)\s+(?:went|has\s+gone|gone)\s+(?:right\s+)?"
    r"(?:through|into)\s+(?:my|his|her|their)\b",
)

BABY_FELL_RED = (
    r"\b(?:sick|vomit\w*|threw\s+up|being\s+sick|sleepy|drowsy|floppy|limp|wont\s+wake|"
    r"won'?t\s+wake|unconscious|knocked\s+out|out\s+cold|blood|seizure|fitting|fit|"
    r"breathing\s+(?:funny|odd|strange)|not\s+breathing|gasping|turning\s+blue|"
    r"not\s+themselves|not\s+feeding|slept\s+(?:a\s+lot|for\s+ages|all\s+day|since)|"
    r"asleep|is\s+sleeping|fell\s+asleep|hard\s+to\s+wake|"
    r"sleeping\s+a\s+lot|off\s+their\s+food|not\s+waking\s+(?:up|properly))\b",
)

BABY_FELL = (
    r"\b(?:my|our|the)\s+(?:baby|infant|newborn|toddler|little\s+one|son|daughter|boy|girl|"
    r"child)\b[^.?!]{0,30}\b(?:fell|fallen|falling|rolled|dropped|tumbled|toppled)\b[^.?!]{0,15}"
    r"\b(?:off|from)\b[^.?!]{0,20}\b(?:bed|sofa|settee|couch|changing\s+table|table|chair|"
    r"highchair|pram|buggy|pushchair)\b",
    r"\b(?:fell|fallen|falling|rolled|dropped|tumbling|tumbled)\s+(?:off|from)\s+(?:the\s+|my\s+|a\s+)?"
    r"(?:bed|sofa|settee|couch|changing\s+table|highchair|pram|pushchair)\b"
    r"[^.?!]{0,30}\b(?:baby|infant|newborn|son|daughter|boy|girl|little\s+one)\b",
    r"\b(?:baby|infant|newborn|toddler|\d+\s*(?:months?|weeks?)\s+old)\b[^.?!]{0,40}"
    r"\b(?:fell|fallen|falling|rolled|dropped|tumbled|toppled)\b",
)

BABY_FELL_OFF = (
    r"\bf(?:ell|alls?|alling)\s+(?:a\s+)?asleep\b",
    r"\b(?:dropp(?:ed|ing|s)|nod(?:ded|ding|s))\s+(?:off|to\s+sleep|asleep)\b",
    r"\b(?:went|gone|goes|going)\s+(?:off\s+)?to\s+sleep\b",
    r"\bfell\s+(?:in\s+love|out\s+(?:of|with)|over\s+(?:nothing|again|laughing))\b",
    r"\brolled\s+(?:over|onto\s+(?:his|her|their)\s+(?:front|tummy|back))\b",
    r"\bdropped\s+(?:his|her|their|the)\s+(?:dummy|comforter|toy|bottle|cup|spoon|muslin)\b",
)

BABY_FELL_SURFACE = (
    r"\b(?:fell|fallen|falling|rolled|dropped|tumbled|toppled)\s+(?:off|from)\s+"
    r"(?:the\s+|my\s+|a\s+|her\s+|his\s+)?(?:bed|sofa|settee|couch|changing\s+table|table|"
    r"chair|highchair|pram|buggy|pushchair|stairs|steps|ladder|wall|bike)\b",
    r"\b(?:bed|sofa|settee|couch|changing\s+table|highchair|pram|buggy|pushchair)\b[^.?!]{0,12}"
    r"\b(?:fell|fallen|falling|rolled|dropped|tumbled|toppled)\b",
)

HANGED_LONG_AGO = (
    r"\bwhen\s+(?:i|we|he|she|they)\s+(?:were|was)\s+(?:kids?|children|child|teenagers?|"
    r"teen|teens|young|little|small|at\s+school)\b",
    r"\bwhen\s+(?:he|she|they|my\s+\w+)\s+was\s+(?:young|a\s+kid|a\s+child|little|small|"
    r"at\s+school)\b",
    r"\b(?:growing\s+up|as\s+a\s+(?:kid|child|teenager)|in\s+(?:my|his|her|their)\s+"
    r"(?:teens|twenties))\b",
    r"\b(?:years?|decades?)\s+(?:ago|back)\b",
    r"\b(?:a\s+)?(?:long|good\s+few|good)\s+(?:time|while|few\s+years?)\s+(?:ago|back)\b",
    r"\b(?:long|time)\s+ago\b",
    r"\bin\s+(?:19|20)\d\d\b",
    r"\blast\s+(?:year|term|spring|summer|autumn|fall|winter|christmas|xmas|month|week|"
    r"night|new\s+year|easter)\b",
)

_STRUCK_RELATIVE = (r"(?:mum|mom|mother|dad|father|son|daughter|husband|wife|partner|boyfriend|"
                    r"girlfriend|brother|sister|friend|baby|child|kid|boy|girl|man|woman|lady|"
                    r"guy|bloke|neighbou?r|colleague|gran|granny|nan|grandad|grandma|grandpa|"
                    r"mate|passenger|cyclist|pedestrian|toddler|teenager|nephew|niece|cousin|"
                    r"aunt|uncle|fiance|fiancee|stepson|stepdaughter|stepdad|stepmum|person|"
                    r"people)")

TRAPPED_HELD_BY_A_PERSON = re.compile(
    r"\b(?:he|she|they|him|her|them|i|my\s+(?:husband|wife|partner|ex|boyfriend|girlfriend|dad|"
    r"mum|mom|father|mother|brother|sister|son|daughter|friend|mate|carer|uncle|aunt|cousin|nan|"
    r"gran|granny|grandad|grandma|grandpa|stepdad|stepmum|flatmate|housemate|neighbou?r)|"
    r"the\s+(?:man|woman|lady|guy|driver|bloke|father|mother))\b[^.?!]{0,20}\b(?:trapped|"
    r"pinned|locked|kept|keeps|holding|held|shut|stuck)\s+(?:me|us)\b")

TRAPPED_VEHICLE_NOT_NOW = (
    r"\bfor\s+(?:hours|ages|a\s+while|an\s+hour|\d+\s*(?:hours?|minutes?|mins?))\b",
    r"\btraffic\b", r"\bjam\b", r"\b(?:car|child|booster)\s+seat\b",
    r"\bbatter(?:y|ies)\b", r"\bflat\b", r"\bbreakdown\b", r"\bpetrol\b", r"\bdiesel\b",
    r"\bpuncture\b", r"\bcharged?\b", r"\bparking\b", r"\block(?:ed)?\s+out\b",
    r"\b(?:keys?|phone|mobile|wallet|purse|bag|handbag|teddy|dummy|toy|ball|money|cards?|"
    r"pram|buggy|medicines?|pills?)\b[^.?!]{0,25}\b(?:locked|trapped|stuck|shut|wedged)\b",
    r"\b(?:has|have|had|keeps?|kept|got)\s+(?:me|him|her|us|them)\s+"
    r"(?:trapped|stuck|pinned)\b",
    r"\byesterday\b", r"\blast\s+night\b", r"\bago\b",
    r"\blast\s+(?:week|year|month|summer|winter)\b",
    r"\bwhen\s+i\s+was\s+(?:a\s+)?(?:kid|child|little|young|small)\b",
    r"\bwhat\s+if\b", r"\bif\s+(?:i|he|she|they|we|my\s+\w+)\b",
)

FAINT_STORY = (
    r"\b(?:i|he|she|they|we|my\s+" + PERSON + r"|the\s+" + PERSON + r"|" + PERSON + r")"
    r"\s+(?:\w+\s+){0,3}(?:fainted|fainting|faints|passed\s+out|passing\s+out|blacked\s+out|"
    r"blacking\s+out|collapsed|was\s+unconscious|were\s+unconscious|been\s+unconscious|"
    r"(?:was|were|been|went)\s+out\s+cold|out\s+cold)\b",
    r"\b(?:had\s+)?(?:a\s+)?(?:funny\s+turn|blackout|fainting\s+fit)\b",
)

OUT_COLD_REPLY = (
    "Ring 111 today rather than waiting it out and say how long they were out and what they were "
    "doing - a first blackout is looked into every time, and a child is seen that day rather than "
    "this week. If they were out for more than a minute, went down during sport, hit their head, "
    "or have not come round, that is 999."
)

OUT_COLD_ASLEEP = (
    r"\bout\s+cold\b[^.?!]{0,20}\b(?:by|until|till|til|all\s+night|overnight|the\s+whole|"
    r"as\s+soon\s+as|bed|beds|bedtime|pillow|nap|naps|bottle|feed|sleep\w*)\b",
    r"\b(?:by|until|till|til|as\s+soon\s+as)\s+(?:\w+\s+){0,2}\bout\s+cold\b",
    r"\bout\s+cold\b[^.?!]{0,20}\b(?:after|before|from)\s+(?:the|a|his|her|my|their|our|that|"
    r"this)?\s*(?:run|walk|feed|bottle|shift|night\s+shift|work|meal|dinner|lunch|breakfast|"
    r"food|flight|drive|journey|day|game|match|film|movie|bath|swim|party|pub|wine|beer|drink\w*|"
    r"heat|exhaust\w*|jet\s?lag|gym|training|school|college|class|exercise|tiring\s+day|"
    r"long\s+day|night\s+out|night\s+in|table|sofa|exercise)\b",
)

WITHDRAWAL_STOP = (
    r"\b(?:stop(?:ped|ping)?|quit(?:ting)?|gave\s+up|giving\s+up|give\s+up|come\s+off|"
    r"coming\s+off|came\s+off|get\s+off|getting\s+off|got\s+off|off|detox\w*|withdraw\w*|"
    r"cut\s+down\s+on|cut\s+out|not\s+had\s+a\s+drink|havent\s+had\s+a\s+drink|"
    r"didn'?t\s+have\s+a\s+drink|without\s+a\s+drink|no\s+booze|no\s+alcohol|"
    r"dry\s+for|on\s+the\s+wagon)\b[^.?!]{0,30}"
    r"\b(?:drink\w*|alcohol|booze|beer|wine|vodka|whisky|whiskey|spirits?|pints?|lager|cider|"
    r"brandy|rum|gin|shots?)\b",
    r"\b(?:havent|hasn'?t|hadn'?t|never)\s+had\s+(?:a\s+|any\s+)?(?:drink|alcohol|booze|"
    r"pint)\b",
    r"\b(?:no|zero)\s+(?:drinks?|alcohol|booze)\s+(?:for|in|since)\b",
    r"\b(?:drink\w*|alcohol|booze|beer|wine|vodka|whisky|whiskey)\b[^.?!]{0,30}"
    r"\b(?:withdraw\w*|detox\w*|dts?)\b",
)

WITHDRAWAL_NOT_ALCOHOL = (
    r"\b(?:coffee|caffeine|tea|fizzy|juice|milk|water|squash|coke|cola|soda|lemonade|"
    r"energy\s+drinks?|sugar\w*|sweets|smok\w*|vap\w*|nicotine|fags?|cigs?|cigarettes?|"\
    r"rollies|weed|cannabis|drugs?|"
    r"painkillers?|screens?|tv|telly|gaming|gambl\w*|porn|shopping|meat|dairy|gluten|"
    r"phone|social\s+media|instagram|facebook|tiktok|doomscroll\w*)\b",
)

WITHDRAWAL_ALONE_AT_HOME = (
    r"\b(?:detox\w*|coming\s+off|stopping|stopped|quitting|quit)\b[^.?!]{0,40}"
    r"\b(?:at\s+home|by\s+myself|on\s+my\s+own|alone|myself|on\s+his\s+own|on\s+her\s+own)\b"
    r"[^.?!]{0,40}\b(?:drink\w*|alcohol|booze|beer|wine|vodka|whisky|whiskey)\b",
    r"\b(?:detox\w*)\b[^.?!]{0,40}"
    r"\b(?:at\s+home|by\s+myself|on\s+my\s+own|alone|myself)\b",
)

WITHDRAWAL_ROUTINE = (
    r"\bshak\w*\b[^.?!]{0,40}\b(?:until|when|if|before)\b[^.?!]{0,25}"
    r"\b(?:i|he|she)\s+(?:have|has|had|get|gets|got|need|needs)\s+(?:a|my|his|her)?\s*"
    r"(?:drink|beer|vodka|wine|gin|whisky|whiskey|pint)\b",
    r"\b(?:need|needs|have|has|had)\s+(?:a|my|his|her)\s+"
    r"(?:drink|beer|vodka|wine|gin|whisky|whiskey|pint)\b[^.?!]{0,30}"
    r"\b(?:to\s+)?(?:stop|stops|stopped|settle|ease)\s+(?:the\s+)?"
    r"(?:shak\w*|trembl\w*|shakes|nerves)\b",
    r"\bthe\s+shakes\s+(?:in\s+the\s+morning|every\s+morning|when\s+i\s+wake)\b",
    r"\bshak\w*\b[^.?!]{0,40}\b(?:if|when|unless)\b[^.?!]{0,25}"
    r"\b(?:i\s+)?(?:dont|don'?t|do\s+not|havent|haven'?t|miss|skip|go\s+without)\b"
    r"[^.?!]{0,20}\b(?:drink|drinks|beer|pint)\b",
)

WITHDRAWAL_SYMPTOM = (
    r"\bshak\w*", r"\bshaky\b", r"\btrembl\w*", r"\btremors?\b", r"\bsweat\w*",
    r"\bsweaty\b", r"\bclammy\b", r"\bnause\w*", r"\bvomit\w*", r"\bbeing\s+sick\b",
    r"\bthrowing\s+up\b", r"\bcan'?t\s+sleep\b", r"\bcant\s+sleep\b",
    r"\bnot\s+sleeping\b", r"\binsomnia\b", r"\bheart\s+(?:is\s+)?(?:racing|pounding)\b",
    r"\bpalpitations?\b", r"\banxious\b", r"\banxiety\b", r"\bjumpy\b", r"\bon\s+edge\b",
    r"\bnight\s+sweats?\b", r"\bfeel\w*\s+(?:awful|terrible|rough|dreadful|ill|horrible)\b",
    r"\bheadache\b", r"\bshiver\w*", r"\bcraving\w*",
)

WITHDRAWAL_STRONG = (
    r"\bshak\w*", r"\bshaky\b", r"\btrembl\w*", r"\btremors?\b", r"\bsweat\w*",
    r"\bsweaty\b", r"\bclammy\b", r"\bheart\s+(?:is\s+)?(?:racing|pounding)\b",
    r"\bpalpitations?\b", r"\bhallucinat\w*", r"\b(?:see|saw|seen|seeing)\s+things\b",
    r"\b(?:hear|heard|hearing)\s+(?:things|voices)\b", r"\bfits?\b", r"\bseizures?\b",
    r"\bdelirium\b", r"\bconfus\w*",
)

WITHDRAWAL_DANGER = (
    r"\bis\s+(?:that|it|this)\s+(?:dangerous|serious|bad|normal)\b",
    r"\bcan\s+(?:it|that|this)\s+(?:kill|be\s+dangerous|hurt\s+me)\b",
    r"\bwill\s+(?:i|he|she|they)\s+be\s+ok\b", r"\bshould\s+i\s+(?:worry|be\s+worried)\b",
    r"\bam\s*i\s+in\s+danger\b", r"\bwhy\s+(?:does|do)\b[^.?!]{0,20}\bshak\w*",
)

WITHDRAWAL_ASK_DANGER = (
    r"\b(?:call|ring|phone|dial)\s+(?:an?\s+)?(?:999|911|112|ambulance|emergency)\b",
    r"\bshould\s+(?:i|we|he|she|they)\s+(?:call|ring|phone|worry|be\s+worried)\b",
    r"\bdo\s+(?:i|we)\s+need\s+(?:an?\s+)?ambulance\b",
    r"\b(?:can|could|will|would)\s+(?:i|you|he|she|they)\s+(?:die|be\s+in\s+danger)\b",
    r"\bis\s+(?:it|that|this)\s+(?:dangerous|serious|deadly|fatal)\b",
    r"\bis\b[^.?!]{0,30}\b(?:dangerous|deadly|fatal|life[-\s]?threatening)\b",
)

WITHDRAWAL_HAIR_OF_THE_DOG = (
    r"\b(?:a\s+)?(?:beer|pint|lager|glass\s+of\s+wine|wine|vodka|drink|drinks|stella|whisky)\b"
    r"[^.?!]{0,40}\b(?:help|helps|sleep|shake|shakes|shaking|stop|settle|ease|calm|take\s+the\s+edge)\b",
    r"\bhair\s+of\s+the\s+dog\b",
    r"\b(?:should|can|could|shall)\s+i\s+(?:have|drink|get)\s+(?:a|another|one)\b",
    r"\b(?:is\s+it\s+ok|is\s+it\s+alright|would\s+it\s+be\s+ok)\s+to\s+(?:have|drink)\b",
)

WITHDRAWAL_NAMED = (
    r"\bwithdraw\w*", r"\bdetox\w*", r"\bdelirium\s+tremens\b", r"\bdts\b",
    r"\b(?:coming|come|came|getting|get|got|am|im|i'?m)\s+off\s+(?:the\s+|my\s+)?"
    r"(?:drink|booze|alcohol|wine|beer)\b",
)

WITHDRAWAL_HALLUCINATION = (
    r"\b(?:see|sees|saw|seen|seeing)\s+things\b",
    r"\b(?:hear|hears|heard|hearing)\s+(?:things|voices)\b", r"\bvoices\b",
    r"\b(?:taste|tastes|tasted|tasting)\s+things\b",
    r"\b(?:smell|smells|smelt|smelled|smelling)\s+things\b",
    r"\b(?:see|sees|saw|seeing|hear|hears|heard|hearing|smell|smells|smelt|smelling|taste|"
    r"tastes|tasted|tasting)\b[^.?!]{0,25}\b(?:that|which)\s+"
    r"(?:isnt|isn'?t|is\s+not|wasnt|aren'?t|arent)\s+(?:really\s+)?there\b",
)

WITHDRAWAL_SENSES_FINE = (
    r"\b(?:see|sees|seeing)\s+things\s+(?:differently|clearly|straight|in\s+a\s+different\s+way|"
    r"in\s+a\s+different\s+light|from\s+a\s+different\s+angle|more\s+clearly)\b",
    r"\b(?:taste|tastes|tasting|smell|smells|smelling)\s+things\s+(?:again|properly|at\s+last|now)\b",
    r"\bcan\s+(?:taste|smell)\s+things\b(?!\s*(?:and|but)\b)",
)

HAIR_SCORCH = (
    r"\b(?:singe[ds]?|singeing|scorch(?:ed|es|ing)?|burnt|burned)\b[^.?!]{0,25}"
    r"\b(?:my|his|her|their|your)\s+(?:hair|fringe|bangs|eyebrows?|eyelashes|lashes|beard|"
    r"moustache|mustache)\b",
    r"\b(?:my|his|her|their|your)\s+(?:hair|fringe|bangs|eyebrows?|eyelashes|lashes|beard|"
    r"moustache|mustache)\b[^.?!]{0,20}"
    r"\b(?:is|are|got|was|were|looks?|keeps?)?\s*(?:singed|scorched|burnt|burned|crispy)\b",
)

HAIR_SCORCH_ANSWER = (
    "That is only hair, and hair grows back - trim the crunchy ends and it stops smelling. The part "
    "to check is the skin underneath: if the forehead, the eyelid or the scalp is red, blistered or "
    "sore, run it under cool water for twenty minutes and get it looked at today, because a burnt "
    "eyelid or brow can swell.",
    "Nothing to do about the hair itself except trim the crispy ends off - it grows back. Do look at "
    "the skin though: red, blistered or sore skin under a singed fringe or brow wants twenty minutes "
    "under cool water and a same-day check, since burnt skin near the eye swells.",
)

BURN_MARK_ON_A_BODY = (
    r"\b(?:burn|burns|burned|burnt|scorch|scorches|scorched|singe|singes|singed)\s+marks?\s+"
    r"(?:on|to)\s+(?:my|his|her|their|your)\s+(?:hand|hands|finger|fingers|thumb|arm|arms|"
    r"wrist|leg|legs|foot|feet|skin|face|chest|neck|shoulder|shoulders|back|thigh|tummy|belly)\b",
)

LIMP_MECHANISM = (
    r"\bgiv(?:e|es|ing|en)\s+way\b",
    r"\bkeeps?\s+rolling\b",
    r"\b(?:ankle|knee|foot|hip)s?\s+roll(?:s|ed)?\b",
    r"\broll(?:s|ed|ing)\s+(?:my|his|her|their|the)\s+(?:knee|ankle|shoulder|hip)\b",
    r"\bunstable\b",
    r"\b(?:knee|ankle|shoulder|hip|joint)s?\s+(?:is|feels?|has\s+been)\s+(?:giving\s+way|"
    r"giving\s+out|unstable|loose)\b",
)

LIMP_OTHER_LIMB = (
    r"\blimp\s+(?:wrist|wrists?|hands?|arms?|fingers?|thumbs?|elbows?|shoulders?)\b",
    r"\blimp\s+(?:in|on)\s+(?:his|her|my|their|the)\s+(?:wrist|wrists?|hands?|arms?|fingers?|"
    r"thumbs?|elbows?|shoulders?)\b",
    r"\b(?:wrist|wrists?|hands?|arms?|fingers?|thumbs?|elbows?|shoulders?)\s+(?:has\s+|have\s+)?"
    r"(?:gone\s+|all\s+)?limp\b",
)

LIMP_LONG = (
    r"\bfor\s+(?:the\s+(?:last|past)\s+)?(?:(?:[0-9]+|one|two|three|four|five|six|seven|eight|"
    r"nine|ten|eleven|twelve|a\s+couple(?:\s+of)?|a\s+few|few|several|many|over\s+a|"
    r"about\s+a|nearly\s+a|almost\s+a|half\s+a|a|an|the)\s+)?"
    r"(?:week|weeks|month|months|year|years|ages)\b",
    r"\bsince\s+(?:last|christmas|the\s+summer|a\s+\w+\s+ago|\d{4})\b",
    r"\b(?:weeks|months|years)\s+now\b",
)

LIMP_SOMEBODY_ELSE = (
    r"\b(?:my|his|her|their|our)\s+(?:mum|mom|mother|dad|father|son|daughter|boy|girl|child|kid|"
    r"little\s+one|baby|nan|nana|gran|granny|grandma|grandad|grandpa|husband|wife|partner|"
    r"brother|sister|uncle|aunt|friend|neighbour|neighbor)\b",
    r"\b(?:he|she|they)\s+(?:has|have|had|got|is|was|were|walks|walk|limps|limp|hobbles|hobble)\b",
)

RING_DANGER = (r"\bswollen\b", r"\bswelling\b", r"\bswelled\b", r"\bswell\b",
               r"\btoo\s+tight\b", r"\bthrobbing\b", r"\bagony\b",
               r"\bcutting\s+(?:in|into)\b", r"\bcut\s+into\b",
               r"\b(?:gone|going|turned|turning)\s+blue\b", r"\bblue\b", r"\bpurple\b",
               r"\bnumb\b", r"\bblack\b")

RING_NOT_WORN = (
    r"\b(?:don'?t|do\s+not|doesn'?t|didn'?t|never|not)\s+(?:wear|wearing|wore)\s+"
    r"(?:a\s+|any\s+|my\s+)?(?:ring|rings|jewellery|jewelry)\b",
    r"\bno\s+rings?\b", r"\bno\s+ring\s+on\b",
    r"\b(?:don'?t|do\s+not|doesn'?t)\s+(?:have|wear|got)\s+(?:a\s+|any\s+|my\s+)?rings?\s+on\b",
    r"\bwithout\s+(?:a\s+|my\s+|any\s+)?rings?\b",
    r"\b(?:took|take|taken|got|get|getting)\s+(?:my|the|her|his|their)\s+rings?\s+off\b",
    r"\b(?:my|the|her|his|their)\s+rings?\s+(?:is|was|are|were)?\s*(?:already\s+)?off\b",
    r"\b(?:ring|rings)\s+(?:is|are|was|were)\s+off\b",
    r"\bwhere\s+(?:my|the|her|his|their)\s+rings?\s+(?:normally|usually|used\s+to\s+be)\b",
)

HOW_TO_TREAT = (
    r"\b(?:how\s+(?:do|should|can)\s+(?:i|you|we)|what'?s\s+the\s+best\s+way\s+to)\b.{0,30}"
    r"\b(?:treat|care\s+for|clean|dress|look\s+after|soothe|deal\s+with)\b",
    r"\bwhat\s+(?:should|do|can)\s+(?:i|we)\s+do\s+(?:about|for|with)\b.{0,40}"
    r"\b(?:burn|scald|nosebleed|sprain\w*|splinter|bruise|graze|sunburn|twisted\s+ankle)\b",
    r"\bwhat\s+(?:should|do|can)\s+(?:i|we)\s+do\s+(?:about|for|with)\s+(?:a|this|that|my|his|her)\s+"
    r"cut\b(?!\s+(?:in|to|from|of|price|budget|hours|pay|staff|spending)\b)",
    r"\b(?:treat|care\s+for|look\s+after)\b.{0,20}\b(?:a|an|my|the)\s+(?:burn|cut|scald|nosebleed|sprain|splinter|bruise|graze)\b",
)

OWN_INJURY_QUESTION = (
    r"\bwhat\s+(?:if|do\s+(?:i|you)\s+do\s+(?:if|when)|should\s+i\s+do\s+(?:if|when)|happens\s+if)\b",
    r"\bhow\s+(?:do|should|can)\s+i\s+(?:treat|care\s+for|dress|clean|soothe)\b",
    r"\bwhat(?:'?s|\s+is)\s+the\s+(?:first\s+aid|best\s+way\s+to\s+treat)\b",
)

OWN_INJURY_IN_MY_CARE = (
    r"\b(?:my|our|your)\s+(?:son|daughter|child|kid|kids|children|baby|babies|toddler|infant|"
    r"little\s+one|husband|wife|partner|boyfriend|girlfriend|mum|mom|mother|dad|father|"
    r"gran|granny|grandma|grandad|grandpa|nan|nana|niece|nephew|grandson|granddaughter)\b",
)

THING_BURNT_WORDS = (
    r"(?:onion|garlic|toast|bread|cake|biscuits?|"
    r"potatoes?|rice|pasta|sauce|soup|stew|curry|dinner|lunch|tea|food|meat|chicken|steak|fish|veg|"
    r"vegetables?|pizza|pan|pots?|saucepans?|wok|oven|grill|toaster|tray|tin|dish|baking|casserole|"
    r"bottom|base|crust|oil|butter|milk|sugar|carpet|shirt|iron|"
    r"cd|cds|dvd|dvds|disc|discs|disk|disks|candle|candles)"
)

THING_BURNT = (
    r"\b(?:burnt|burned|scorched|charred|blackened|burning|burns?)\s+"
    r"(?:(?:my|the|our|a|an|his|her|their|your|some|black|brown|dark|sticky|thick|hard|"
    r"orange|crispy)\s+)*" + THING_BURNT_WORDS + r"\b",
    r"\b" + THING_BURNT_WORDS +
    r"\s+(?:(?:is|was|got|gets|looks|has|had|keeps\s+getting)\s+)?(?:\w+\s+){0,2}"
    r"(?:burnt|burned|scorched|charred)\b",
    r"\bburnt\s+(?:onto|on\s+to|to\s+the\s+bottom)\b",
    r"\bburnt[\s-]*on\b[^.?!]{0,30}\boff\b",
    r"\b(?:stuck|stuck-on|stuck\s+on)\b[^.?!]{0,30}\bburn\w*\b",
    r"\b(?:burnt|burned|scorched|charred|blackened)\b(?:\s+\w+){0,3}\s+(?:tin|tins|trays?|pans?|"
    r"pots?|saucepans?|wok|dishes?|sheet|shelf|shelves|rack|mould|springform|traybake)\b",

    r"\bburn(?:ed|t|s|ing)?\s+(?:\w+\s+){0,2}"
    r"(?:cd|cds|dvd|dvds|disc|discs|disk|disks|candle|candles|incense)\b",
)

BURNT_SELF = (
    r"\b(?:burnt|burned|scalded)\s+(?:myself|me|himself|herself|themselves)\b",
    r"\b(?:i|he|she|they)\s+(?:was|were|got|am|is)\s+(?:burnt|burned|scalded)\b",
    r"\b(?:i|we|he|she|they)\s+(?:got|get|have|has|had)\s+(?:a|an|my|his|her|their|"
    r"me|some)?\s*(?:bad|nasty|little|nasty|small|sore|red)?\s*burn\b",
    r"\b(?:a|the)\s+(?:bad|nasty|little|small|sore|red)?\s*burn\s+(?:from|off)\b",
    r"\b(?:a|the)\s+(?:bad|nasty|little|small|sore|red)?\s*burn\s+"
    r"(?:on|to)\s+(?:my|his|her|their)\s+" + BURN_ON_BODY,
)

RAZOR_BURN = (
    r"\b(?:razor\w*|sha(?:v|ve|ves|ved|ving)|shaving|shave|epilat\w+|wax(?:ed|ing)?|pluck\w*|"
    r"tweezers?)\b[^.?!]{0,25}\bburn\w*\b",
    r"\bburn\w*\b[^.?!]{0,25}\b(?:from|after|by|off)\s+(?:a\s+|the\s+|my\s+|her\s+|his\s+)?"
    r"(?:razor\w*|sha(?:v|ve|ves|ved|ving)|shaving|epilat\w+|wax(?:ed|ing)?)\b",
)

FRICTION_WORD = (
    r"\b(?:boots?|shoes?|trainers?|socks?|slippers?|sandals?|flip[\s-]?flops?|heels?|"
    r"rucksack|backpack|gloves?|rake|shovel|handle|rowing|oar|gym|running|runs|hiking|hike|"
    r"walking|walked|marathon|new\s+(?:boots?|shoes?|trainers?))\b",
    r"\b(?:from|by)\s+(?:the\s+)?(?:rubbing|friction)\b",
    r"\bblister\s+(?:plaster|pad|patch)\b",
    r"\b(?:pop|pops|popping|popped|burst|bursting|drain|draining)\b",
    r"\b(?:how\s+(?:do\s+i|to|should\s+i)|should\s+i|what\s+(?:should\s+i\s+do|do\s+i\s+do))"
    r"\s+(?:about|for|with)?\s*(?:treat|treating|deal\s+with|look\s+after|cover|dress|care)\b",
)

BLISTER_STATE = (
    r"\b(?:my|his|her|their)\s+(?:hand|hands|finger|fingers|thumb|thumbs|palm|palms|arm|arms|"
    r"wrist|wrists|leg|legs|thigh|thighs|shoulder|shoulders|back|neck|face|armpit)\b"
    r"[^.?!]{0,25}\bblister\w*\b",
    r"\b(?:i|he|she|they)\s+(?:have|has|got|ve\s+got)\s+(?:a|an|some|a\s+few)\s+"
    r"blister\w*\s+(?:on|across|under)\s+(?:my|his|her|their)\s+(?:hand|hands|finger|fingers|"
    r"thumb|palm|palms|arm|arms|wrist|writs|leg|legs|thigh|thighs|shoulder|shoulders|back|neck|"
    r"armpit)\b",
    r"\b(?:my|his|her|their)\s+(?:hand|hands|finger|fingers|thumb|palm|palms|arm|arms|wrist|"
    r"wrists|leg|legs|thigh|thighs|shoulder|shoulders|back|neck|armpit)\b[^.?!]{0,20}"
    r"\b(?:is|are|got|has|have|keeps?)\b[^.?!]{0,12}\bblister\w*\b",
)

BLISTER_CAUSE_BURN = (
    r"\b(?:bleach\w*|chemical\w*|acid\w*|detergent\w*|clean(?:ing|ed|ers?)\b|"
    r"disinfectant\w*|degreaser\w*|drain\s+unblocker|caustic\w*|lye|ammonia|white\s+spirit|"
    r"paint\s+thinner|turpentine|paraffin|petrol|soda\s+crystals)\b",
    r"\b(?:sun\w*|uv\s+light|sunbed|sunlamp|nettles?|stinging\s+nettles?|hogweed)\b",
)

BLISTER_STATE_REPLIES = (
    "Leave it whole and cover it with a blister plaster or a clean non-fluffy dressing, and take "
    "the pressure off whatever rubbed it. Don't burst it: a blister that gets hot, spreading or "
    "weeping, or one you cannot keep off, should be seen.",
    "Leave it alone and cover it with a blister plaster, and stop whatever is rubbing it. Don't pop "
    "it; if it gets hot, red or weeping, or you are diabetic, get it looked at.",
)

HOW_LONG = (
    r"\bhow\s+long\b",
    r"\bhow\s+many\s+(?:days|weeks)\b",
    r"\bhow\s+long\s+(?:will|would|does|do|till|until|before|to)\b",
    r"\bwhen\s+(?:will|does|should)\s+it\s+(?:heal|be\s+(?:better|right|healed|back))\b",
    r"\btakes?\s+to\s+heal\b",
    r"\bhealing\s+time\b",
    r"\brecovery\s+time\b",
)

HEAL_WORDS = (
    ("sprain", r"\bsprain\w*|\btwisted\s+(?:my|an?|the)\s+(?:ankle|knee|wrist)|"
               r"\b(?:rolled|went)\s+over\s+on\s+(?:my|an?|the)\s+ankle\b"),
    ("burn", r"\bburn(?:s|ed|t|ing)?\b|\bscald\w*"),
    ("cut", r"\bcuts?\b|\bgash\w*|\bgraz(?:e|ed|es)\b"),
    ("blister", r"\bblisters?\b"),
)

INJURY_WORDS = (
    ("mouth_burn", (r"\btongue\b", r"\broof\s+of\s+(?:my|the)\s+mouth")),
    ("burn", (r"\bburn(?:s|t|ed|ing)?\b", r"\bscald(?:s|ed|ing)?\b",
              r"\bblister(?:s|ed|ing)?\b")),
    ("sunburn", (r"\bsun\s?burn(?:s|t|ed|ing)?\b",)),
    ("cut", (r"\bcut(?:s|ting)?\b", r"\bgraze(?:s|d|ing)?\b",
             r"\bscrape(?:s|d|ing)?\b", r"\bpaper\s+cuts?\b")),
    ("nosebleed", (r"\bnose\s*bleed",)),
    ("sprain", (r"\bsprain", r"\btwisted", r"\bankle\b", r"\bknee\b")),
    ("splinter", (r"\bsplinter",)),
)

OWN_INJURY = (
    r"\b(?:burn\w*|scald\w*|cut\w*|bled|bleeding|sprain\w*|fractur\w*|broke|broken|blister\w*|"
    r"spill\w*|spilt|pour\w*|tip\w*|knock\w*|dropped|splash\w*|threw)\b"
    r"[^.?!]{0,25}\b(?:my|me|myself|your|yourself)\b",
    r"\b(?:my|me|myself|your|yourself)\b[^.?!]{0,25}\b(?:burn\w*|scald\w*|cut\w*|bleed\w*|"
    r"sprain\w*|fractur\w*|broken|blister\w*)\b",
    r"\b(?:i|we|you)\s+(?:get|got|gets|am|is|was)\s+(?:burnt|burned|scalded|blistered)\b",
    r"\b(?:first\s+aid\s+for|treat|treating|soothe|do\s+for|good\s+for|best\s+(?:thing\s+)?for)"
    r"\b[^.?!]{0,15}\b(?:a|the|this)?\s*(?:bad\s+|red\s+|nasty\s+|serious\s+)?"
    r"(?:burn|scald)\b",
)

SOMEONE_ELSE_OWN = (
    r"\b(?:my|our|the|a)\s+(?:son|boys?|daughter|girl|child|kid|kids|baby|toddler|husband|wife|"
    r"partner|mum|mom|mother|dad|father|brother|sister|friend|mate|nana|nan|gran|grandma|"
    r"grandad|grandpa|neighbou?r|colleague|boss|flatmate|housemate|dog|cat|puppy|kitten)\b",
)

CLEANABLE_SURFACE = (r"\b(?:pans?|pots?|saucepans?|woks?|ovens?|grills?|hobs?|cookers?|rings?|"
                     r"trays?|tins?|dishes?|dish|baking|sheets?|plates?|bowls?|worktops?|"
                     r"sink|racks?|griddles?|barbecues?|bbqs?|burners?|casseroles?|toasters?|"
                     r"glasses?|glass|door)\b",)

PERSON_BURNT = (
    r"\b(?:got|get|gets|getting)\s+(?:burnt|burned|scalded)\b"
    r"(?=\s*(?:$|[.,!?]|on\b|at\b|in\b|by\b|from\b|when\b|while\b|and\b|so\b|because\b))",
    r"\b(?:i|he|she|they|we)\s+(?:burnt|burned|scalded)\b",
)

WHOLE_BODY_RED_FLAG = (
    r"\b(?:hard\s+to\s+wake|won'?t\s+wake|wont\s+wake|not\s+waking|floppy|"
    r"and\s+limp\b(?!ing)|"
    r"limp\s+and\s+(?:floppy|blue))\b",
    r"\b(?:confused|confusion|disorientated|delirious|not\s+making\s+sense|unresponsive|"
    r"not\s+responding|vacant)\b",
    r"\b(?:seizure|seizures|convulsion|convulsions|fitting|having\s+a\s+fit|fitted)\b",
    r"\b(?:struggling\s+to\s+breathe|breathing\s+(?:fast|quickly|hard)|grunting|"
    r"blue\s+lips|grey\s+lips|gray\s+lips|lips\s+are\s+blue|clammy)\b",
    r"\b(?:stiff\s+neck|non[-\s]?blanching)\b",
)

MILD_BODY_SIGN = (
    r"\b(?:drowsy|drowsiness|sleepy|too\s+sleepy|listless)\b",
    r"\b(?:vomiting|vomited|throwing\s+up|thrown\s+up|projectile\s+vomit\w*)\b",
    r"\b(?:not\s+(?:himself|herself|themselves)|unlike\s+(?:him|her)self)\b",
    r"\b(?:not\s+(?:feeding|feeding\s+well|eating|eating\s+much|drinking|drinking\s+much)|"
    r"off\s+(?:his|her|their)\s+(?:food|feeds|milk|bottles?)|"
    r"refusing\s+(?:feeds|food|bottles?|the\s+bottle))\b",
    r"\b(?:i|he|she|they|we|baby|child|son|daughter|kid|boy|girl|toddler|mum|mom|dad|mother|"
    r"father|nan|nana|grandad|grandma|husband|wife|partner|friend|sister|brother|niece|nephew)"
    r"\b[^.?!]{0,20}\b(?:not\s+right|not\s+(?:his|her|their)\s+usual\s+self)\b"
    r"(?!\s+(?:now|away|off|there|here|yet))",
)

ASKS_ABOUT_THE_INJURY = (
    r"\bhow\s+long\b", r"\bhow\s+many\s+(?:days|weeks)\b", r"\btakes?\s+to\s+heal\b",
    r"\bhealing\s+time\b", r"\brecovery\s+time\b", r"\bhow\s+(?:often|soon)\b",
    r"\bshould\s+i\s+(?:cover|bandage|dress|wrap|clean|wash|soak|pop|burst)\b",
    r"\b(?:do|should)\s+i\s+need\s+(?:a|to\s+see)\b",
    r"\bis\s+it\s+(?:meant|supposed)\s+to\b",
)

A_FOLLOW_UP_ABOUT_THE_INJURY = frozenset("""
how long will would does do did take takes taken heal heals healed healing time times day days week weeks
 till until til
many much soon often better right normal back recover recovered recovery
it that this these they them its theirs one
i my me should can could shall may might
a an the to be been being is are was were of about on in at for with and or then now not
cover covered covering bandage bandaged dressing dress wrapped wrap plaster plasters
clean cleaning wash washing soak soaking pop burst drain
need needs see seen looked look doctor nurse gp hospital a and e
sore red swollen painful blistering itchy scabby scab
properly fully completely still actually now then anyway please thanks
""".split())

CPR_HOWTO = (
    r"\bcpr\b", r"\bcompressions?\b", r"\brescue\s+breaths?\b", r"\bchest\s+compress\w*\b",
    r"\bhands[\s-]?only\b", r"\bhow\s+many\s+compressions\b", r"\bheart\s+massage\b",
    r"\bp(?:us|u)sh\w*\b[^.?!]{0,15}\bchest\b", r"\bchest\b[^.?!]{0,15}\bp(?:us|u)sh\w*\b",
    r"\b(?:how|do|does|should|shall|am|is|what)\b[^.?!]{0,20}\bp(?:us|u)sh\w*\b[^.?!]{0,12}"
    r"\b(?:hard|harder|fast|faster|deep|deeper|many|quickly|fast)\b",
    r"\bhow\s+(?:hard|harder|fast|deeper|deep|many|quickly|often)\b[^.?!]{0,20}"
    r"\bp(?:us|u)sh\w*\b",
    r"\bhow\s+(?:hard|fast|deep)\b[^.?!]{0,12}\bcompressions?\b",
)

CPR_ROOM_EMPTY = (
    r"\bnot\s+breathing\b", r"\bstopped\s+breathing\b", r"\bisn'?t\s+breathing\b",
    r"\bunconscious\b", r"\bcollapsed\b", r"\bno\s+pulse\b", r"\bnot\s+waking\b",
    r"\b(?:gone|turning|going|is|are)\s+blue\b", r"\b(?:is|are)\s+(?:dead|dying)\b",
    r"\bchoking\b", r"\b(?:he|she|they|my\s+\w+)\s+(?:is|are|was)\s+(?:down|out)\b",
)

CPR_NOT_EFFORT = (
    r"\b(?:gym|workout|rep|reps|sets?|weights?|lift\w*|sprint\w*|run|runs|running|jog\w*|"
    r"train\w*|cycl\w*|bike|swim\w*|row\w*|hike|walk\w*|stud\w*|revision|exam|business|"
    r"project|team|manager|career|pram|pushchair|wheelchair|trolley|barrow|mower|hoover|"
    r"vacuum|bike|car|van|drill|screw|nail|brush|paint\w*)\b",
    r"\bp(?:us|u)sh[\s-]?ups?\b", r"\bpress[\s-]?ups?\b", r"\bpull[\s-]?ups?\b",
    r"\bchin[\s-]?ups?\b", r"\bsit[\s-]?ups?\b", r"\bsquats?\b", r"\blunges?\b",
    r"\bplanks?\b", r"\bcrunches?\b", r"\bburpees?\b", r"\bstar\s+jumps?\b",
)

CPR_WHEN_ALIVE = (
    "Not if they are breathing or have a pulse - compressions are for someone with neither. Put "
    "them in the recovery position, keep watching their breathing and ring 999 or 911 if you are "
    "worried; if they stop breathing normally, start CPR: 30 compressions, then 2 rescue breaths.",
    "Don't do compressions on someone who is breathing or has a pulse: roll them into the "
    "recovery position, stay with them and ring 999 or 911. If their breathing stops, it is 30 "
    "compressions and 2 rescue breaths, kept going until help arrives.",
)

CPR_NO_PULSE_NOW = (
    "Ring 999 or 911 now and start: no pulse and not breathing normally is CPR - 30 compressions "
    "in the centre of the chest, then 2 rescue breaths, kept going until the ambulance takes over.",
    "No pulse means CPR straight away, so ring 999 or 911 and start: 30 compressions, 2 rescue "
    "breaths, about 5-6 cm deep at 100-120 a minute, without stopping until help arrives.",
)

CPR_START = (
    "If they're not breathing normally, start now: 30 hard, fast compressions in the centre of "
    "the chest, then 2 rescue breaths, and keep going without stopping until the ambulance arrives.",
    "Yes - start now if they're not breathing normally, and stay on the line with the 999 or 911 "
    "call handler: 30 compressions in the centre of the chest, then 2 rescue breaths, without "
    "stopping until help takes over.",
)

CPR_HOW = (
    "Thirty compressions then two rescue breaths, about 5-6 cm deep in the centre of the chest at "
    "100-120 a minute, kept going until the ambulance arrives.",
    "Push hard and fast in the middle of the chest: 30 compressions, then 2 rescue breaths, about "
    "5-6 cm deep, letting the chest come all the way back up between pushes.",
)

CPR_STOP = (
    r"\b(?:should|do|shall|can|when\s+(?:should|do|can))\s+(?:i|we)\s+stop\b",
    r"\bstop\s+(?:when|once|as\s+soon\s+as)\b.{0,30}\b(?:ambulance|paramedics?|crew|help|"
    r"arrive|arrives|come|comes)\b",
    r"\bhow\s+long\s+(?:do|should)\s+(?:i|we)\s+(?:keep|carry)\b", r"\buntil\s+when\b",
    r"\bwhen\s+(?:do|should)\s+(?:i|we)\s+(?:stop|give\s+up)\b",
)

CPR_STOP_REPLY = (
    "Keep going until the ambulance crew take over from you - they will tell you when to stop. If "
    "you are too exhausted to carry on, say so on the call and they will talk you through it.",
    "Don't stop until the crew take over, even if they seem to come round: keep the compressions "
    "going and let the paramedics decide.",
)

CPR_CHILD = (
    r"\b(?:child|children|kid|kids|toddler|toddlers|premature|school\s?age\w*)\b",
    r"\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|[1-9]|1[0-2])\s*"
    r"(?:year|yr)s?\s*old\b", r"\blittle\s+one\b",
    r"\b(?:son|daughter|boy|girl|grandson|granddaughter|nephew|niece)\b[^.?!]{0,12}"
    r"\b(?:is|aged|of)\s+(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"[1-9]|1[0-2])\b",
)

CPR_HOW_BABY = (
    "A baby gets five rescue breaths first - your mouth over their mouth and nose, small puffs - "
    "then 15 compressions with two fingers in the middle of the chest, about a third of the depth, "
    "and keep going 15 to 2. Ring 999 or 911 now and say it is a baby.",
    "For a baby: five small rescue breaths, then 15 compressions with two fingers in the centre of "
    "the chest, about a third of the depth, then two more breaths - and keep cycling. Ring 999 or "
    "911 now and tell them the baby's age.",
)

CPR_HOW_CHILD = (
    "A child gets five rescue breaths first, then 15 compressions with the heel of one hand (two "
    "for a bigger child) in the middle of the chest, about a third of the depth, and keep going 15 "
    "to 2. Ring 999 or 911 now.",
    "For a child: five rescue breaths, then 15 compressions with the heel of one hand in the "
    "centre of the chest, about a third of the depth, then two breaths, and keep cycling. Ring 999 "
    "or 911 now.",
)

CPR_BABY_SCENE = (
    "That's CPR now for a baby: ring 999 or 911 on speaker, give five small rescue breaths - your "
    "mouth over their mouth and nose - then 15 compressions with two fingers in the middle of the "
    "chest to about a third of the depth. Keep going 15 to 2 until help takes over.",
    "Ring 999 or 911 now and start for a baby: five rescue breaths, then 15 compressions with two "
    "fingers in the centre of the chest, and keep cycling 15 to 2 until the ambulance arrives.",
)

CPR_CHILD_SCENE = (
    "That's CPR now for a child: ring 999 or 911 on speaker, give five rescue breaths, then 15 "
    "compressions with the heel of one hand in the middle of the chest to about a third of the "
    "depth, and keep going 15 to 2 until help takes over.",
    "Ring 999 or 911 now and start: five rescue breaths, then 15 compressions with the heel of one "
    "hand, and keep cycling 15 to 2 until the ambulance arrives.",
)

CPR_ROUGH = (
    "Hard and fast is right: about 5-6 cm deep in the centre of the chest. If a rib gives, keep "
    "going - cracked ribs heal, and stopping is the bigger danger.",
    "Deep and fast is what's needed, so don't ease off. If ribs crack, carry on; only stop when "
    "help takes over or you are too exhausted to continue.",
)

CALL_HELP_REPLY = (
    "Yes - ring 999 or 911 now if you haven't already, say what you've seen and stay on the line "
    "until the call handler tells you what to do.",
    "If you haven't already, yes: ring 999 or 911 and describe exactly what's happening. Stay on "
    "the line - the call handler can talk you through the next step.",
)

ASPIRIN_REPLY = (
    "If they're not allergic to it, give one 300mg aspirin to chew while you wait, and tell the 999 "
    "call handler you have. If they're allergic, or the handler says no, don't.",
    "Chewed aspirin helps if it isn't going to be a problem for them: one 300mg tablet, then say on "
    "the call that you've given it. Skip it if they're allergic or the call handler says not to.",
)

WHEN_HELP_COMES = (
    r"\bhow\s+long\b.{0,40}\b(?:ambulance|paramedics?|fire|police|help)\b",
    r"\bwhen\s+(?:will|are|do)\b.{0,40}\b(?:ambulance|paramedics?|fire\s+(?:brigade|service)|"
    r"police|they)\b.{0,20}\b(?:coming|get|here|arrive)\b",
    r"\bare\s+they\s+(?:coming|on\s+their\s+way)\b",
)

WHEN_HELP_REPLY = (
    "They're usually with you within minutes for something like this: keep the door unlocked, the "
    "phone on speaker, and let the crew straight in when they knock.",
    "They are usually there quickly for something like this: leave the door unlocked and the phone "
    "on speaker, and the crew will knock and come in.",
)

FITTING_IN = (
    r"\bfitting\s+(?:in|into|with|up|together)\b", r"\ba\s+fitting\b",
    r"\bfittings?\s+for\b(?!\s+(?:the\s+)?(?:first|last|second|third|final|an?\s+\w+\s+time|"
    r"hours?|days?|weeks?|months?|a\s+while|ages))",
)

FITTING_MANNER_TAIL = re.compile(
    r"\s*(?:(?:today|yesterday|lately|recently|nowadays)\b.*"
    r"|(?:at|in|into|with)\s+(?:the\s+|his\s+|her\s+|their\s+|our\s+|a\s+)?(?:new\s+)?"
    r"(?:nursery|preschool|playgroup|school|class|clubs?|teams?|groups?|other\s+kids|"
    r"the\s+others)\b.*)?$")

FRIGHTENED = (
    r"\b(?:can\s+you\s+hear\s+me|are\s+you\s+(?:still\s+)?there|you\s+still\s+there)\b",
    r"\bi'?m\s+(?:(?:really|so|very|that|proper|properly|absolutely|still|dead|scared\s+witless)\s+)*"
    r"(?:scared|frightened|terrified|panicking|shaking|bricking\s+it)\b",
    r"\bi\s+can'?t\s+stop\s+shaking\b",
    r"\b(?:going\s+to|gonna|might|may|could)\s+lose\s+(?:him|her|them)\b",
    r"\b(?:he|she|they)\s+(?:(?:might|may|could)\s+(?:not\s+)?(?:make\s+it|die|survive)|"
    r"(?:is|are)\s+going\s+to\s+die)\b",
    r"\b(?:will|is)\s+(?:he|she|they)\s+(?:going\s+to\s+)?be\s+(?:ok|okay|alright|fine)\b",
    r"\b(?:am|did)\s+i\s+do(?:ing)?\s+(?:it|this)?\s*right\b",
)

FRIGHTENED_REPLY = (
    "I'm here. You're doing the right thing by staying with them: keep the 999 or 911 call handler "
    "on speaker, say out loud what you can see, and keep talking to them until the ambulance comes.",
    "That's a frightening thing to be in the middle of. Keep the call handler on speaker, tell the "
    "handler everything you notice, and stay with the person until the ambulance arrives.",
)

ABUSE_SCARED = FRIGHTENED + (
    r"\bi(?:'?m|\s+am)\s+(?:(?:really|so|very|that|proper|properly|absolutely|still|dead)\s+)*"
    r"(?:scared|frightened|terrified|panicking|shaking|shook|bricking\s+it)\b",
    r"\bi\s+keep\s+(?:shaking|trembling)\b",
    r"\bmy\s+hands?\s+(?:keep\s+|won'?t\s+stop\s+|cant\s+stop\s+)?shak(?:e|es|ing)\b",
    r"\bi\s+(?:feel|get)\s+(?:scared|frightened|terrified)\b",
    r"\b(?:i'?m|i\s+am)\s+(?:scared|frightened|terrified)\s+(?:of|about)\s+(?:him|her|them)\b",
)

ABUSE_SCARED_REPLY = (
    "That fear is worth trusting rather than pushing down: get somewhere you can shut a door, keep "
    "your phone charged and with you, and ring 999 or 911 if they come back.",
    "You don't have to sit with that on your own tonight - is there a neighbour or a friend whose "
    "door you could knock on? 999 or 911 if they come back, or if it gets worse before then.",
    "Being frightened is reason enough to get out of the room: phone and keys with you, go to "
    "someone you trust, and ring 999 or 911 if they try to stop you leaving.",
    "That is a frightening way to live, and you are not overreacting. Have a bag by the door, keep "
    "somewhere to go in mind tonight, and ring 999 or 911 the moment you feel he might start again.",
)

DETAIL_AFTER_ESCALATION = (
    r"\b(?:it|this|he|she|they)\s+(?:started|began|happened|came\s+on|kicked\s+off)\b",
    r"\b(?:this\s+morning|this\s+afternoon|this\s+evening|earlier\s+today|yesterday|"
    r"last\s+night|an\s+hour\s+ago|\d+\s+(?:minutes?|hours?|days?)\s+ago)\b",
    r"\bsince\s+(?:this\s+morning|yesterday|last\s+night|about\s+\d)\b",
)

HELD_CRISIS_DETAIL = CRISIS_PLAN_SAID + (
    r"\b(?:have|has|got|made|make|worked\s+out|thought\s+of|thought\s+about|picked|chosen)\s+"
    r"(?:a|the|my|one)\s+plan\b",
    r"\bthe\s+plan\s+is\s+(?:ready|set|made|done)\b",
    r"\b(?:wrote|written|writing)\s+(?:a|the|my)\s+(?:notes?|letters?)\b",
    r"\bi'?ve\s+(?:written\s+it|got\s+it)\s+down\b",
    r"\b(?:got|have|bought|saved|sorted)\s+(?:the|a|some)\s+(?:pills|tablets|meds|medicine|"
    r"painkillers|rope|noose|razor\w*|blades?|gun|knife|paracetamol)\b",
    r"\b(?:the\s+)?(?:pills|tablets|rope|noose|razors?|blades?)\s+(?:are|is)\s+"
    r"(?:ready|sorted|nearby|in\s+my\s+\w+)\b",
    r"\b(?:picked|chosen|set|know|got)\s+(?:a|the|my)\s+(?:date|day|time)\b",
    r"\bi\s+know\s+(?:when|where|how\s+much)\b",
    r"\bi\s+know\s+which\s+(?:place|spot|bridge|building|roof|window|tree|way\s+out|road)\b",
    r"\bhow\s+long\s+(?:till|until|before)\s+(?:that|then|it)\b",
    r"\bhow\s+long\s+(?:do|have|would)\s+i\s+(?:have|got)\b",
    r"\bwhen\s+(?:everyone'?s|everybody'?s|they'?re)\s+(?:asleep|gone|out|away)\b",
    r"\bi'?m\s+(?:going|gonna)\s+to\s+(?:do\s+it|go\s+through\s+with\s+it)\b",
    r"\bi'?ll\s+(?:do\s+it|go\s+through\s+with\s+it)\b",
    r"\b(?:my|a)\s+(?:sister|brother|friend|mum|mom|dad|mother|father|partner|wife|husband|"
    r"neighbour|neighbor|daughter|son|cousin|mate|flatmate|housemate|carer)\b[^.?!]{0,40}"
    r"\b(?:coming|comes|come|coming\s+over|on\s+(?:her|his|their)\s+way|is\s+with\s+me|"
    r"here\s+(?:tonight|now|with\s+me)|staying|made\s+it|got\s+here)\b",
    r"\b(?:im|i'?m)\s+not\s+on\s+my\s+own\b",
    r"\b(?:someone|somebody)\s+is\s+with\s+me\b",
    r"\b(?:put|placed|hid|hidden|hide|kept|left|stashed)\b[^.?!]{0,24}"
    r"\b(?:notes?|letters?|razors?|blades?|rope|noose|gun)\b[^.?!]{0,20}"
    r"\b(?:in|on|under|behind|inside)\s+(?:my|the|a)\b",
    r"\b(?:pills|tablets|meds|bottle)\b[^.?!]{0,18}\b(?:in|on|under|behind|inside)\s+"
    r"(?:my|the)\s+(?:pocket|bag|handbag|rucksack|coat|jacket|sock|shoe|locker|desk|bedside|"
    r"drawer)\b",
    r"\b(?:hid|hidden|stashed)\b[^.?!]{0,20}\b(?:notes?|letters?|razors?|blades?|rope|noose)\b",
    r"\b(?:moved|shifted|took|taken|carried|brought)\b[^.?!]{0,20}"
    r"\b(?:notes?|letters?|tablets?|pills?|razors?|blades?|rope|noose|gun)\b",
    r"\b(?:notes?|letters?|tablets|pills|razors?|blades?|rope|noose|gun)\b[^.?!]{0,14}"
    r"\b(?:is|are)\s+(?:already\s+)?(?:in|on|under|behind|inside)\s+(?:my|the|a)\b",
    r"\b(?:filled|packed|loaded|measured|counted|lined\s+up)\s+(?:the|a|my)\s+"
    r"(?:bottle|glass|syringe|needle|bag|box|tub|container)\b",
    r"\b(?:have|got|bought|sorted|saved)\s+(?:the|all\s+the)\s+stuff\b",
    r"\b(?:bought|got|have|sorted)\s+(?:everything|what)\s+i\s+need\b",
)

HELD_CRISIS_OFF = (
    r"\bsafety\s+plan\b", r"\bplan\s+(?:with|from)\s+(?:my\s+)?(?:therapist|counsell?or|"
    r"doctor|gp|nurse|psychiatrist|social\s+worker|support\s+worker|cpn|key\s+worker)\b",
    r"\bplan\s+to\s+(?:ring|call|see|speak|talk|get\s+help|ask\s+for\s+help)\b",
    r"\bplan\s+for\s+(?:dinner|tea|lunch|breakfast|christmas|tonight'?s|the\s+weekend|"
    r"tomorrow'?s|the\s+party|the\s+trip|the\s+holiday|work)\b",
    r"\bcrisis\s+line\b", r"\bsamaritans\b", r"\b116\s*123\b", r"\b988\b",
    r"\b(?:im|i'?m|i\s+am)\s+(?:ok|okay|fine|safe|better|alright|calmer)\b",
    r"\b(?:feel|feeling)\s+(?:better|calmer|safer|a\s+bit\s+better)\b",
    r"\bnot\s+(?:going\s+to|gonna)\s+(?:do\s+it|do\s+anything)\b",
    r"\b(?:i\s+)?(?:will|'ll|ll)\s+(?:ring|call|see\s+someone|get\s+help)\b",
    r"\b(?:rang|called|texted)\s+(?:them|the\s+line|someone|my\s+\w+)\b",
    r"\bthank(?:s|\s*you)\b",
    r"\b(?:note|letter)\s+(?:to|for)\s+(?:my|his|her|their|the|a|an)\b",
    r"\b(?:don'?t|do\s+not|havent|haven'?t|not|no\s+longer)\s+(?:have\s+)?(?:a|any|the)\s+plan\b",
    r"\bno\s+plan\b",
)

CRISIS_PLAN_CARRY = (
    r"\b(?:wrote|writing|written|left|leaving|leave)\s+(?:a|the|my)\s+(?:note|letter)\b",
    r"\bthe\s+notes?\s+(?:is|are)\s+(?:in|on|under|by|at|next\s+to|inside)\b",
    r"\b(?:picked|pick|chosen|chose|set|setting|decided\s+on)\s+(?:a|the|my)?\s*"
    r"(?:date|day)\b",
    r"\b(?:got|get|bought|buy|have|having|stockpiled|stockpiling|saved\s+up|saving\s+up|"
    r"ordered|ordering|hid|hiding)\s+(?:the|a|some|enough|loads\s+of|up)?\s*"
    r"(?:pills|tablets|paracetamol|painkillers|rope|noose|razors?|blades?|knife|gun)\b",
    r"\bi(?:'ve|ve)?\s+(?:have|got)\s+a\s+plan\b",
    r"\bi\s+know\s+how\s+(?:i'?m|im|i\s+am|i'?d|id)\s+(?:going\s+to|gonna|to|would)\s+"
    r"(?:do\s+it|end\s+it|kill\s+myself|finish\s+it)\b",
    r"\b(?:said|saying|writing)\s+(?:my\s+)?goodbyes?\b",
    r"\b(?:picked|found|chosen)\s+(?:a|the)\s+(?:place|spot|bridge|roof|car\s+park)\b",
    r"\bnot\s+going\s+to\s+be\s+(?:here|around)\s+(?:much\s+)?(?:longer|after\s+this)\b",
    r"\bi\s+won'?t\s+be\s+(?:here|around)\s+(?:for\s+)?(?:next\s+\w+|much\s+longer|"
    r"christmas|the\s+weekend|long)\b",
    r"\b(?:i'?m|im|i\s+am|i\s+will|ill|i'?ll)\s+(?:going\s+to\s+|gonna\s+)?"
    r"(?:do\s+it|end\s+it|finish\s+it|go\s+through\s+with\s+it|kill\s+my\s*self)\b",
    r"\b(?:just\s+)?need\s+(?:the|some|a\s+bit\s+of|more)\s+nerve\b"
    r"(?![\s\S]*\b(?:ring|call|phone|contact|book|tell|text|see\s+(?:the|my|a)|"
    r"gp|doctor|nurse|samaritans|111|999|a\s?&\s?e|hospital|therapist|counsell?or)\b)",
    r"\b(?:got|bought|have|have\s+got|found)\s+(?:the|all\s+the)\s*"
    r"(?:stuff|things|kit|equipment)\b(?=\s*(?:$|[.,!?]|ready\b|now\b|today\b|tonight\b))",

)

CRISIS_PLAN_ORDINARY = (
    r"\b(?:thank\s*you|thankyou|birthday|christmas|sick|absence|shopping|grocery|to[\s-]do|"
    r"sticky|reminder|credit|debit|bank)\b[^.?!]{0,14}\bnotes?\b",
    r"\bnotes?\b[^.?!]{0,24}\b(?:about\s+the|for\s+the|for\s+my\s+(?:work|boss|school|"
    r"doctor|landlord|mum|dad|teacher|team|rent|car|house|flat)|re:|saying\s+thank)\b",
    r"\bnotes?\s+(?:app|on\s+my\s+phone|in\s+my\s+phone)\b",
    r"\bletters?\b[^.?!]{0,26}\b(?:to\s+the\s+(?:council|bank|landlord|school|doctor|"
    r"hospital|company|insurer|insurance|dvla|hmrc|mp|jobcentre|university|college)|"
    r"about\s+the\s+(?:rent|bill|debt|job|course|house|flat))\b",
    r"\b(?:date|day)\b[^.?!]{0,18}\b(?:for\s+(?:the\s+)?(?:wedding|holiday|exam|interview|"
    r"dentist|doctor|scan|move|party|trip|operation|op|viewing)|of\s+the\s+(?:wedding|exam))\b",
    r"\b(?:my|the|his|her)\s+(?:prescription|antibiotics|contraceptive|blood\s+pressure|"
    r"diabetes|epilepsy|thyroid|thyroxine|metformin|statins?)\b",
    r"\b(?:pills|tablets|painkillers|paracetamol)\b[^.?!]{0,20}\b(?:from\s+the|under\s+"
    r"prescription|prescribed|for\s+my\s+(?:back|knee|period|headache|migraine|arthritis|pain|"
    r"hip|shoulder|neck|teeth|tooth))\b",
    r"\bstuff\b[^.?!]{0,20}\bfor\s+the\s+(?:cake|party|trip|dinner|recipe|barbecue|bbq|"
    r"birthday|wedding|christmas|exam|interview|move|house|flat|garden|bathroom|kitchen|car)\b",
    r"\bi\s+know\s+how\s+much\b[^.?!]{0,24}\b(?:costs?|cost\s+me|pays?|weighs?|i\s+owe|"
    r"it\s+is|it's)\b",
    r"\bmeasured\b[^.?!]{0,24}\b(?:milk|water|flour|sugar|rice|ingredients?|grams|ml|ounces|"
    r"paint|timber|wood)\b",
    r"\b(?:rope|knife|blade|blades)\b[^.?!]{0,24}\b(?:for\s+the\s+(?:car|trailer|garden|"
    r"washing|bikes?|roof\s+rack|kitchen|cooking|dinner|bread|onions?|swings?|clothes\s+line|"
    r"washing\s+line|boat|trampoline|tree\s+house|shed|gate|fence)|"
    r"to\s+(?:tie|tow|cut|trim|slash|open|prune|chop|slice|fillet|carve|peel))\b",
)

CRISIS_PLAN_REPLY = (
    "Thank you for telling me. That is a plan, and a plan needs help now rather than later: ring "
    "999 or 911, or get yourself to A&E and say what you have ready - and please do not stay on "
    "your own: put the tablets or the note out of reach and ask someone to come and sit with you.",
    "That is a plan, so please do not carry it on your own: ring 999 or 911, or go to A&E and say "
    "what you have got ready, and have someone come to you and take the means away. Samaritans are "
    "on 116 123 any hour if you need a voice before that.",
)

WAKE_UP_SOMEONE = (
    r"\b(?:can'?t|cant|cannot|can\s+not|unable\s+to|struggling\s+to|having\s+trouble)\b"
    r"[^.?!]{0,24}?\b(?:wake|waken|waking|rouse|wake\s+up)\s+"
    r"(?:my|the|our|his|her|their)\s+" + PERSON + r"\b"
    r"(?![^.?!]{0,12}\b(?:for|to|before|in\s+time\s+for)\s+(?:(?:his|her|their|the|a)\s+)?"
    r"(?:school|work|college|uni|university|nursery|childminder|shift|the\s+(?:bus|train))\b)",
    r"\b(?:can'?t|cant|cannot|unable\s+to|struggling\s+to|having\s+trouble)\b[^.?!]{0,20}?"
    r"\b(?:get|keep)\s+(?:my|the|our|his|her|their)\s+" + PERSON + r"\b[^.?!]{0,15}?"
    r"\b(?:wake|waken|rouse|stir)\b",
)

ROUTINE_REASON = (
    r"\b(?:school|work|college|uni|university|nursery|childminder|shifts?|alarms?|bus|train|"
    r"flight|exams?|test|interview|appointment|meeting|class|lecture|lesson|paper\s+round|"
    r"paper\s+deliveries|early\s+start|mornings?)\b",
)

SPELL_RED = (
    r"\b(?:temperatur\w+|fever\w*|breath\w*|blue|grey|gray|limp|floppy|floppiness|seizure|fit|"
    r"shaking|rash|stiff\s+neck|dribbling|drooling|unresponsive)\b",
)

MORNING_ROUTINE = (
    r"\b(?:in|of)\s+the\s+mornings?\b|\bmornings\b|\bbefore\s+(?:school|work|nursery|"
    r"breakfast)\b|\bon\s+school\s+days\b",
)

HARD_TO_WAKE = (
    r"\b(?:can'?t|cannot|can\s+not)\s+be\s+(?:woken|roused|wakened|stirred)\b",
    r"\b(?:very|so|really|extremely|quite)?\s*(?:sleepy|drowsy|lethargic|floppy|limp)\b[^.?!]{0,25}"
    r"\b(?:hard|difficult|impossible|not\s+easy)\s+to\s+(?:wake|rouse|waken|stir)\b",
    r"\b(?:hard|difficult|impossible|not\s+easy)\s+to\s+(?:wake|rouse|waken|stir)\b[^.?!]{0,25}"
    r"\b(?:very\s+|so\s+)?(?:sleepy|drowsy|floppy|limp|lethargic|not\s+(?:himself|herself|"
    r"themselves))\b",
    r"\b(?:baby|babies|newborn|infant)\b[^.?!]{0,25}\b(?:hard|difficult|impossible)\s+to\s+"
    r"(?:wake|rouse|waken|stir)\b",
    r"\b(?:hard|difficult|impossible)\s+to\s+(?:wake|rouse|waken|stir)\b[^.?!]{0,25}"
    r"\b(?:baby|newborn|infant)\b",
    r"\b(?:he|she|they|my\s+" + PERSON + r"|the\s+" + PERSON + r")\b[^.?!]{0,15}"
    r"\b(?:is|was|seems?|seemed|has\s+been|had\s+been)\b[^.?!]{0,8}"
    r"\b(?:hard|difficult|impossible)\s+to\s+(?:rouse|waken|stir)\b",
)

VISIT_OR_TIME = (
    r"\b(?:tonight|later|tomorrow|this\s+(?:evening|afternoon|morning|weekend)|after\s+all|"
    r"next\s+(?:week|weekend)|until\s+\w+|for\s+(?:dinner|tea|coffee|lunch|supper|a\s+bit))\b",
)

COLLAPSE_HINT = (
    r"\b(?:fell|fallen|fall|bang|banged|hit|head|collapsed|floor|ground|pavement|breathing|"
    r"ambulance|pulse|overdose|swallowed|diabetic|seizure|the\s+water|pool)\b",
)

WONT_COME_ROUND = (
    r"\b(?:he|she|they|my\s+" + PERSON + r"|the\s+" + PERSON + r")\b[^.?!]{0,12}"
    r"\b(?:won'?t|wont|isn'?t|isnt|is\s+not|not|hasn'?t|hasnt|didn'?t|didnt|can'?t|cant|cannot)\b"
    r"[^.?!]{0,10}\b(?:(?:com(?:e|ing))\s+round\b(?!\s*(?:for|to)\s+(?:dinner|tea|coffee|lunch|"
    r"supper|visit|see|pick|my|his|her|their|our|the\s+(?:idea|way|view|opinion|plan)))|"
    r"com(?:e|ing)\s+to\b(?!\s+(?:the|a|an|my|your|his|her|their|our|this|that|it|us|me|him|them)\b)|"
    r"rous(?:e|es|ing|ed|able)\b)",
    r"\b(?:can'?t|cant|cannot|unable\s+to|struggling\s+to|not\s+able\s+to)\b[^.?!]{0,15}"
    r"\b(?:bring|get|rouse|wake)\s+(?:him|her|them|my\s+" + PERSON + r"|the\s+" + PERSON + r")\b"
    r"(?:[^.?!]{0,15}\bround\b(?!\s+(?:for|to)\s+(?:dinner|tea|coffee|lunch|supper|see|my|his|her|"
    r"their|our|the\s+(?:idea|way|view|opinion)))|"
    r"[^.?!]{0,6}\bawake\b|"
    r"[^.?!]{0,8}\bto\s+(?:wake|waken|stir|rouse)\b|"
    r"[^.?!]{0,6}\bto\b(?=\s*[,.!?]|\s*$))",
)
_STREAK_MARK = (
    r"\bred\s+(?:line|streak|track)s?\b",
    r"\breddish\s+(?:line|streak)s?\b",
)
_STREAK_REDNESS = r"\b(?:redness|red\s+skin|red\s+area|red\s+patch|the\s+red\s+part|infection)\b"
_STREAK_MOVE = (
    r"\b(?:spreading|spread|creeping|crept|tracking|tracked|travell?ing|travell?ed|moving|moved|"
    r"running|ran|going|gone|goes|up|down)\b",
)
_STREAK_ON_A_PERSON = (
    r"\b(?:cut|cuts|cuts?\s+myself|gash|graze[ds]?|scrape[ds]?|scratch(?:es|ed)?|wound|wounds|"
    r"sore|splinter|thorn|blister|bite|bites|bitten|burn(?:s|ed|t)?|sting(?:s|ed)?|puncture|"
    r"operation|opsite|stitches?|staple[ds]?|dressing|bandage[ds]?|plaster|tattoo)\b",
)
WOUND_STREAK = (
    r"\A(?=.*" + _STREAK_MARK[0] + r")(?=.*" + _STREAK_ON_A_PERSON[0] + r"|.*\b" + BODY + r")",
    r"\A(?=.*" + _STREAK_MARK[1] + r")(?=.*" + _STREAK_ON_A_PERSON[0] + r"|.*\b" + BODY + r")",
    r"\A(?=.*" + _STREAK_REDNESS + r"[^.?!]{0,30}" + _STREAK_MOVE[0] + r")"
    r"(?=.*" + _STREAK_ON_A_PERSON[0] + r"|.*\b" + BODY + r")",
    r"\A(?=.*" + _STREAK_MOVE[0] + r"[^.?!]{0,30}" + _STREAK_REDNESS + r")"
    r"(?=.*" + _STREAK_ON_A_PERSON[0] + r"|.*\b" + BODY + r")",
)
WOUND_STREAK_OFF = (
    r"\bhair\b", r"\bdye\w*\b", r"\bhighlight\w*\b", r"\bnail\s+polish\b", r"\blipstick\b",
    r"\btrain\b", r"\btube\b", r"\bmetro\b", r"\bbus\b", r"\broad\b", r"\blane\b", r"\bmap\b",
    r"\bsky\b", r"\bsunset\b", r"\brainbow\b", r"\bpaint\w*\b", r"\bmarker\b", r"\bpen\b",
    r"\bscreen\b", r"\btv\b", r"\btele\b", r"\bfilm\b", r"\bbook\b", r"\bpaper\b", r"\bflag\b",
    r"\bteam\b", r"\bspider\s+vein\w*\b", r"\bstretch\s+mark\w*\b", r"\bnappy\b", r"\bnapkin\b",
    r"\bcrease\w*\b", r"\btyre\w*\b", r"\bcar\b", r"\bwall\b", r"\bfloor\b", r"\bkitchen\b",
)
STREAK_FEVER = (
    r"\bfever\w*\b", r"\btemperatures?\b", r"\btemps?\b", r"\bshiver\w*\b", r"\brigors\b",
    r"\bclammy\b", r"\bvery\s+unwell\b", r"\bunwell\b", r"\bfluey\b", r"\bhot\b",
    r"\b\d{2}(?:\.\d)?\s*(?:c\b|degrees)\b",
)
def _with_streak_fever(pats):
    extra = r"(?=[\s\S]*(?:" + "|".join(STREAK_FEVER) + r"))"
    return tuple(p + extra for p in pats)


WOUND_STREAK_FEVER = _with_streak_fever(WOUND_STREAK)


_A_PURPOSE_AFTER = (r"(?!\s*,?\s*(?:to|and|so|then)\s+"
                    r"(?:fix|get|catch|grab|fetch|collect|check|clean|clear|put|take|pick|mend|"
                    r"paint|water|feed|empty|see|look|have|find|hang|drop|pass|give|bring|do)\b)")

_OFF_A_HEIGHT = (
    r"off(?:\s+of)?\s+(?:a|an|the|my|our)?\s*"
    r"(?:bridge|roof|building|block|cliff|balcony|ledge|height|car\s*park)\b"
    + _A_PURPOSE_AFTER
)

_OFF_AN_EDGE = (
    r"off(?:\s+of)?\s+(?:a|an|the|my|our)?\s*"
    r"(?:platform|pier|wall|bank|edge)\b"
    + _A_PURPOSE_AFTER
)

_INTO_THE_WAY = (
    r"(?:in\s+front\s+of|under|onto)\s+(?:a|an|the|my|our)?\s*"
    r"(?:train|trains|bus|buses|lorry|truck|coach|traffic|tracks?|rails?|line)\b"
    + _A_PURPOSE_AFTER
)

SELF_HARM_WISHES_A_PART = (
    r"\b(?:want|wanna|wanted|wanting|need|needing|going|gonna|plan|planning|tempted|urge|"
    r"feel\s+like|feeling\s+like|think\s+about|thinking\s+about|thought\s+about)\s+(?:to\s+)?"
    r"(?:cut|cutting|burn|burning|hurt|hurting|harm|harming|scratch|scratching|scald|scalding|"
    r"starve|starving|bruise|bruising)\s+my\s+(?:own\s+)?"
    r"(?:skin|arms?|legs?|wrists?|thighs?|forearms?|belly|stomach|hips?|chest|hands?|feet|foot|"
    r"scalp|neck|shoulders?|back|face)\b"
    r"(?!\s+(?:hair|nails?|toenails?|fingernails?|fat|calories?|carbs?)\b)",
)

_HEIGHT_MEANS_VERB = (
    r"throw|throwing|threw|jump|jumping|jumped|leap|leaping|leapt|fall|falling|fell")
_ANY_MEANS_VERB = _HEIGHT_MEANS_VERB + r"|step|stepping|stepped|walk|walking|walked|lie|lying|lay"
_A_MEANS_PLACE = (r"(?:(?:" + _ANY_MEANS_VERB + r")\s+" + _INTO_THE_WAY
                  + r"|(?:" + _HEIGHT_MEANS_VERB + r")\s+(?:" + _OFF_A_HEIGHT
                  + r"|" + _OFF_AN_EDGE + r"))")

SELF_HARM_BY_A_MEANS = (
    r"\b(?:" + _ANY_MEANS_VERB + r")\s+(?:my\s*self|me)\s*" + _INTO_THE_WAY,
    r"\b(?:" + _HEIGHT_MEANS_VERB + r")\s+(?:my\s*self|me)\s*(?:" + _OFF_A_HEIGHT
    + r"|" + _OFF_AN_EDGE + r")",
    r"\b(?:hang|hanging|strangle|shoot|shooting|stab|poison|overdose|overdosing)\s+"
    r"(?:my\s*self|me)\b",
    r"\b(?:with|using|by)\s+(?:a\s+|the\s+)?(?:rope|knife|blade|razor|gun|pills|tablets|"
    r"paracetamol|belt)\b[^.?!]{0,24}\b(?:kill|hurt|harm|cut|hang|shoot)\s+my\s*self\b",
    r"\b(?:i\s+want|i\s+wanna|im|i'?m|i\s+am|i\s+could|i\s+would|i\s+might|i\s+should|"
    r"im\s+going|i'?m\s+going|going|thinking\s+about|thought\s+about|tempted|planning)"
    r"\b[^.?!]{0,30}\b" + _A_MEANS_PLACE,
    r"^\s*(?:so\s+|and\s+|then\s+)?" + _A_MEANS_PLACE,
)

POISON_SAID = (
    r"\b(?:swallowed|drank|drunk|eaten|ate|took|downed|inhaled|gulped|licked)\s+"
    r"(?:some\s+|a\s+bit\s+of\s+|a\s+mouthful\s+of\s+|loads\s+of\s+|the\s+rest\s+of\s+|"
    r"half\s+a\s+bottle\s+of\s+|a\s+whole\s+bottle\s+of\s+)?"
    r"(?:bleach|detergent|disinfectant|antifreeze|weed\s?killer|hand\s+saniti[sz]er|"
    r"drain\s+cleaner|soap|shampoo|mouthwash|shower\s+gel|cleaning\s+products?|"
    r"paint\s?thinner|white\s+spirit)\b",
    r"\b(?:double|triple)\s+dos(?:ed|ing)\b",
    r"\b(?:doubl|tripl)(?:ed|ing)\s+(?:up\s+)?(?:on\s+)?(?:my|the)\s+"
    r"(?:dose|insulin|meds|medication|tablets|pills)\b",
)

A_HURT_OF_A_BODY_PART = (
    r"\b(?:hurt|hurting|harm|harming|work|working|push|pushing)\s+my\s+"
    r"(?:own\s+)?(?:arms?|legs?|shoulders?|muscles?|back|abs|core|chest|glutes?|calves)\b")

A_WORKOUT_CUE = (
    r"\b(?:gym|work\s?outs?|weights?|weight\s?lifting|lifting|dumbbells?|barbells?|kettlebells?|"
    r"treadmill|rowing|spin(?:ning)?\s+class|physio\w*|training\s+session|leg\s+day|"
    r"arm\s+day|pt\s+session)\b")

A_PLAN_SAID = (
    r"\bi\s+know\s+how\s+(?:i'?d|id|i\s+would)\s+(?:do\s+it|end\s+it|be\s+done|go\b)",
    r"\bi\s+know\s+how\s+(?:i'?m|im|i\s+am)\s+(?:going\s+to|gonna)\s+(?:do\s+it|end\s+it|be\s+done)\b",
    r"\b(?:my|the|our)\s+plan\s*(?:is|'s|was)\s+to\s+"
    r"(?:jump|cut|hang|overdose|swallow|take|use|go)\b"
    r"(?:\s+(?:it|them|all\s+of\s+them|them\s+all|the\s+lot|too\s+many|an?\s+overdose|"
    r"my\s+life|my\s*self|off\s+(?:a|the)\s+(?:bridge|roof|building|cliff|balcony)|"
    r"in\s+front\s+of\s+(?:a|the)\s+(?:train|bus)|my\s+(?:wrists?|throat|arms?|legs?|neck)))?"
    r"(?:\s+(?:all\s+at\s+once|at\s+once|right\s+now|tonight|today|now))?"
    r"\s*[.?!]*\s*$",
    r"\bi\s+(?:have|got|'ve\s+got|ve\s+got)\s+a\s+plan\s+to\s+(?:do\s+it|end\s+it|end\s+my\s+life|"
    r"kill\s+my\s*self|take\s+(?:all\s+of\s+them|them\s+all|the\s+lot)|jump|overdose)\b",
    r"\b(?:im|i'?m|i\s+am)\s+going\s+to\s+do\s+it\s*[.?!]*$",
    r"^\s*(?:so\s+)?(?:i'?m\s+)?going\s+to\s+(?:take|swallow)\s+(?:all\s+of\s+them|them\s+all|"
    r"the\s+(?:whole\s+)?packet|the\s+lot)\s*[.?!]*\s*$",
)

A_PLAN_ORDINARY = (
    r"\bplan\s+(?:is|'s|was)\s+to\s+(?:pay|save|book|call|ring|text|email|write|start|finish|"
    r"order|cancel|visit|see|meet|apply|clean|sort|tidy|walk|run|train|study|revise|move|"
    r"paint|cook|buy|sell|fly|drive|go\s+(?:to|back|home|out)|get\s+(?:the|a|my|some)|"
    r"have\s+(?:a|some|the|lunch|dinner|breakfast))\b",
    r"\bgoing\s+to\s+do\s+it\s+(?:after|before|on|at|in|next|this|tomorrow|tonight|later|when|"
    r"once|every|twice|again|three|two|with|for|if|and)\b",
    r"\bwe\s+(?:were|are)\s+going\s+to\s+do\s+it\b",
    r"\bjump\s*-?\s*start\b|\bjump\s+(?:the\s+queue|the\s+gun|start\s+the\s+car)\b",
    r"\bknow\s+how\s+(?:i'?d|id)\s+do\s+it\s+(?:now|too|myself|already)\b",
    r"\bknow\s+how\s+(?:i'?d|id|i\s+would)\s+(?:do\s+it|end\s+it)\b\s*(?:[-\u2013,:;]\s*)?"
    r"(?:you|u|it'?s|its|then|just|by|with|using|through|via)\b",
    r"\b(?:do\s+it|end\s+it)\s+(?:if|when|once|with|by|using|through|via|for|on|at|in)\b",
)


SELF_HARM_OWN_PART = (*SELF_HARM_WISHES_A_PART, *SELF_HARM_BY_A_MEANS)
