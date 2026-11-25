
import re
from .safety_cards import PURSUIT_PLACE_HOME

__all__ = [
    "ABUSE",
    "ABUSER",
    "BY_NOT_A_THING",
    "ABUSE_DISCLOSURE",
    "ABUSE_DISCLOSURE_FINE",
    "ABUSE_FINE",
    "ABUSE_HEAD_INTO",
    "ABUSE_HIT_ME",
    "ABUSE_MEMORY",
    "ABUSE_NOW",
    "ABUSE_PURSUIT_HARD",
    "ABUSE_VERB",
    "ABUSE_VERBAL",
    "ABUSE_VERBAL_FINE",
    "ABUSE_VERBAL_LABEL",
    "ABUSE_VERBAL_MAD",
    "ABUSE_VERBAL_PERSON",
    "ABUSE_VERBAL_SUBJECT",
    "ABUSE_VERB_PART",
    "ASK_AFTER_ME",
    "BLOW_THINGS",
    "CHILD_AGGRESSOR",
    "CHILD_HIT_NOW",
    "CLOSE",
    "DYING_OTHER",
    "GAME_AFTER_ME",
    "GAME_PLAYED",
    "GAME_WORD_STOP",
    "GRIP_GAME",
    "GRIP_GAME_FENCE",
    "GRIP_NOT_AN_ASSAULT",
    "GRIP_NOT_AN_ASSAULT_STR",
    "HAS_ME_SUBJECT",
    "HIT_AS_A_CHILD",
    "HIT_BY_A_VEHICLE",
    "HIT_THING_NOT_PERSON",
    "I_DID_NOT_HIT",
    "I_HIT_SOMEONE",
    "MONEY_NAMED",
    "NOT_A_FEAR",
    "OTHERS",
    "PARTNER_CLOSE",
    "PEOPLE",
    "PERSON",
    "PLAY_FACE_REPLIES",
    "PURSUIT",
    "PURSUIT_FEAR",
    "PURSUIT_LOUD",
    "PURSUIT_OUTSIDE",
    "PURSUIT_PLACE_WORK",
    "PURSUIT_SUBJECT",
    "PURSUIT_SUBJECT_EX",
    "REMORSE_FOR_THE_ACT",
    "SELF_HARM_NEEDS_PERSON",
    "SELF_OWN_DYING",
    "SOFT_FACE_PUSH",
    "SOFT_FACE_STOP",
    "SOMEONE_HOLDS_THE_MONEY",
    "THREAT_COERCIVE",
    "THREAT_SUBJECT",
    "_NOT_A_THREAT",
    "_REFUSED_EXIT",
    "_THE_BLOW",
    "_THE_HAND",
    "_THE_ONE_HIT",
    "_both_here",
]

MONEY_NAMED = re.compile(
    r"\b(?:pay\s?day|paid|pay|wages?|salary|pension|benefits?|universal\s+credit|money|cash|"
    r"quid|pounds?|dollars?|euros?|fiver|tenner|skint|paycheck|overdraft|rent|bills?|"
    r"\d+\s*(?:pounds?|quid|dollars?|euros?|bucks?))\b")
SOMEONE_HOLDS_THE_MONEY = re.compile(
    r"\b(?:he|she|they|him|her|them|someone|somebody|my\s+(?:partner|husband|wife|boyfriend|"
    r"girlfriend|ex|mum|mom|dad|father|mother|son|daughter|brother|sister|flatmate|roommate|"
    r"housemate|landlord))\b[^.?!]{0,40}?\b(?:took|takes|taking|emptied|empties|cleared\s+out|"
    r"clears\s+out|controls?|controlled|keeps?|kept|hides?|hid|hidden|spends?|spent|gambled|"
    r"stole|steals?)\b[^.?!]{0,30}\b(?:money|wages?|salary|pay|paycheck|account|benefits?|"
    r"universal\s+credit|pension|savings?|card)\b",
    re.I)
SELF_HARM_NEEDS_PERSON = True
DYING_OTHER = (
    r"\b(?:my|our|his|her|their|the)\s+(?:nan|gran|nanny|nana|granny|grandma|grandmother|grandad|"
    r"granddad|grandpa|grandfather|mum|mom|mother|dad|father|wife|husband|partner|son|daughter|"
    r"child|kid|baby|brother|sister|aunt|uncle|cousin|friend|mate|dog|cat|puppy|kitten|pet|horse)\b"
    r"[^.?!]{0,20}\b(?:is|are|'s|s)\s+(?:going\s+to|gonna|about\s+to)\s+die\b",
)
SELF_OWN_DYING = (
    r"\b(?:im|i'm|i\s+am|i\s+think\s+im|i\s+think\s+i'm|i\s+feel|i\s+keep\s+thinking)\b"
    r"[^.?!]{0,20}\b(?:going\s+to|gonna|want\s+to|wanna|ready\s+to)\s+die\b",
    r"\bwant\s+to\s+die\b", r"\bkill\s+my\s*self\b", r"\bbetter\s+off\s+dead\b",
    r"\bsuicid\w*\b",
)

PERSON = (r"(?:mum|mom|mother|dad|father|son|daughter|husband|wife|partner|boyfriend|girlfriend|"
          r"brother|sister|friend|flatmate|roommate|baby|child|kid|kids|children|"
          r"grand(?:child|children|son|daughter|kid)s?|step(?:child|children|son|daughter)s?|"
          r"boy|girl|man|woman|"
          r"lady|guy|bloke|neighbou?r|colleague|boss|gran|granny|nan|grandad|grandma|grandpa|mate|"
          r"carers?|care\s+workers?|support\s+workers?|social\s+workers?|personal\s+assistants?|"
          r"nurses?|midwives?|midwife|doctors?|gps?|physios?|therapists?|"
          r"patient|pupil|student|teacher|driver|passenger|singer|player|runner|swimmer)")

PEOPLE = (r"(?:i|i'm|i've|he|he's|she|she's|they|they're|we|you|someone|somebody|anyone|everyone|"
          r"my\s+" + PERSON + r"|the\s+" + PERSON + r"|" + PERSON + r")")

OTHERS = (r"(?:he|he's|she|she's|they|they're|him|her|them|someone|somebody|anyone|everyone|"
          r"my\s+" + PERSON + r"|his\s+" + PERSON + r"|her\s+" + PERSON + r"|their\s+" + PERSON + r"|"
          + PERSON + r")")

ABUSER = (r"(?:" + PERSON + r"|step(?:mum|mom|dad|mother|father|brother|sister|son|daughter|parent|"
          r"child|children)|ex|landlord|landlady|housemate|lodger|aunt|auntie|uncle|cousin|nan|nana|"
          r"grandparent|in-?laws?|father-?in-?law|mother-?in-?law|son-?in-?law|daughter-?in-?law|"
          r"guardian|foster\s+parent|boy|friend|manager|supervisor|"
          r"nieces?|nephews?|grandmothers?|grandfathers?|grandparents?)")
_THE_ONE_HIT = (r"(?:my\s+(?:partner|husband|wife|boyfriend|girlfriend|ex|fianc(?:e|ée)|mum|mom|"
                r"mother|dad|father|son|daughter|child|kid|kids|children|baby|stepson|stepdaughter|"
                r"stepdad|stepmum|brother|sister|nan|gran|grandma|grandad|carer)(?!'s)|"
                r"(?:my|the)\s+(?:kids|children|child|baby|son|daughter)s?(?!'s)|her|him|them)\b")
_THE_BLOW = (r"(?:hit|hitting|slap(?:ped|ping)?|punch(?:ed|ing)?|kick(?:ed|ing)?|beat|beating|"
             r"chok(?:ed|ing)?|strangl(?:ed|ing)?|drag(?:ged|ging)?|threw|thrown|throwing|"
             r"scratch(?:ed|ing)|claw(?:ed|ing))")
_THE_HAND = (r"(?:push(?:ed|ing)?|shov(?:e|ed|es|ing)|grab(?:bed|bing)?|pin(?:ned|ning)?|held|"
             r"hold|pulled|yank(?:ed|ing)?|twist(?:ed|ing)?)")
I_HIT_SOMEONE = (
    r"\bi\s+(?:keep\s+|kept\s+|just\s+|nearly\s+|almost\s+|have\s+|had\s+)?" + _THE_BLOW +
    r"\s+" + _THE_ONE_HIT,
    r"\bi\s+(?:keep\s+|kept\s+)?" + _THE_HAND + r"\s+" + _THE_ONE_HIT +
    r"(?:[^.?!]{0,30}\b(?:throat|neck|wall|floor|stairs|ground|door|hard|down|against|"
    r"into\s+the\s+(?:road|traffic|kitchen|hall|bathroom|fire|car|bushes))\b"
    r"|[^.?!]{0,40}\b(?:during|in|after|before)\s+(?:an?\s+)?(?:argument|row|fight|"
    r"disagreement|falling\s+out)\b)",
    r"\b(?:i\s+)?(?:lost|lose|be\s+losing)\s+my\s+temper\b[^.?!]{0,30}\b" + _THE_BLOW +
    r"\s+" + _THE_ONE_HIT,
    r"\bi\s+(?:was\s+|got\s+|get\s+|am\s+|'m\s+|im\s+)?(?:so\s+)?(?:angry|mad|raging|"
    r"drunk|pissed|upset|frustrated|stressed|exhausted|wound\s+up|beside\s+myself)\b"
    r"[^.?!]{0,25}\b" + _THE_BLOW + r"\s+" + _THE_ONE_HIT,
)
HIT_THING_NOT_PERSON = (
    r"\b(?:partner|husband|wife|boyfriend|girlfriend|ex|fiance|fiancee|son|daughter|child|kid|"
    r"kids|children|baby|mum|mom|mother|dad|father|brother|sister|nan|gran|grandma|grandad|"
    r"carer|parents)'s\b",
    r"\b(?:partner|husband|wife|boyfriend|girlfriend|ex|son|daughter|child|kid|kids|children|"
    r"baby|mum|mom|mother|dad|father|brother|sister|carer)(?:s)?\s+(?:\w+\s+){0,2}(?:cake|car|bike|toys?|ball|"
    r"phone|laptop|window|door|plate|glass|cup|mug|tv|telly|scooter|bike|present|cards?|"
    r"homework|drawing|picture)\b",
)
GAME_NOT_A_BLOW = (
    r"\b(?:mess(?:ing)?\s+about|mucking\s+about|play(?:ing)?\s*(?:fighting|fight)|sparring|"
    r"boxing|wrestl(?:ing|e)|judo|karate|rugby|football|practice|training|drill|"
    r"a\s+game|snowball|water\s+fight|paintball|nerf|tickl(?:e|ing)|play)\b",
    r"\b(?:at|in|during|on)\s+(?:the\s+)?(?:chess|cards?|scrabble|monopoly|backgammon|draughts|"
    r"checkers|dominoes|poker|darts|snooker|billiards|pool|bowling|tennis|badminton|squash|"
    r"golf|cricket|football|rugby|rounders|netball|basketball|hockey|table\s+tennis|"
    r"video\s+games?|playstation|xbox|wii|board\s+game)\b",
    r"\b(?:in|at|during)\s+(?:[\w-]+\s+)?(?:final|match|game|tournament|league|race|marathon|"
    r"competition|championship|quiz)\b(?!\s+(?:argument|row|fight|bust-?up|falling\s+out))",
)
I_DID_NOT_HIT = (
    r"\b(?:never|didn'?t|didnt|don'?t|dont|wouldn'?t|wouldnt|not|have\s+never)\s+"
    r"(?:ever\s+)?(?:hit|hitting|hurt|hurting|touch|touched|lay\s+a\s+hand|laid\s+a\s+hand)\b",
    r"\bhit\s+(?:her|him|them|my\s+" + ABUSER + r")\s+back\b",
    r"\b(?:lose|losing|lost)\s+my\s+temper\s+(?:with|at)\s+(?:her|him|them|the\s+kids|"
    r"my\s+" + ABUSER + r")\b[^.?!]{0,30}\b(?:shout|shouted|shouting|yell|yelled|swore|swear|"
    r"snapped|said|slam|slammed|walked|rowing|row|argue|argued|arguing)\b",
    r"\bwhen\s+we\s+were\s+(?:kids|children|little|lads|girls|boys)\b",
    r"\bwe\s+used\s+to\s+(?:fight|hit|scrap|wrestle)\b",
    r"\bwhen\s+i\s+was\s+(?:\d+|a\s+kid|a\s+child|a\s+lad|a\s+boy|a\s+girl|young|"
    r"little|small|tiny|at\s+school|in\s+school)\b",
    r"\b(?:as|like)\s+(?:a\s+)?(?:kid|child|kids|children|lads|boys|girls)\b",
    r"\bgrowing\s+up\b",
    r"\b(?:at|in)\s+(?:primary|secondary|junior|middle|comprehensive)\s+school\b",
    r"\bi\s+used\s+to\s+(?:\w+\s+){0,3}(?:hit|fight|scrap|wrestle)\b[^.?!]{0,25}"
    r"\b(?:brother|sister|cousin|mate|friend|kids|kids|boy|girl)s?\b",
    r"\b(?:accident|accidentally|by\s+mistake|didn'?t\s+mean|didnt\s+mean|"
    r"in\s+my\s+sleep|sleepwalking|fidgeting)\b",
    r"\b(?:awake|out\s+of\s+bed|to\s+wake\s+(?:me|him|her|them|the\s+kids))\b",
    r"\b(?:in\s+a\s+dream|dream(?:t|ed)\b|had\s+a\s+dream|nightmare)\b",
) + GAME_NOT_A_BLOW
MY_GROWN_UP = (r"(?:dad|father|stepdad|mum|mom|mother|stepmum|parents|uncle|aunt|auntie|brother|"
               r"sister|cousin|carer|nan|nana|gran|grandma|grandad|grandpa|grandparents|"
               r"foster\s+\w+)")
THE_BLOW_ON_A_CHILD = (
    _THE_BLOW + r"|beat|belt(?:ed)?|strap(?:ped)?|cane(?:d)?|smack(?:s|ed|ing)?|lock(?:ed)?|"
    r"starve(?:d)?|smother(?:ed)?|throttle(?:d)?|abuse(?:d|s)?|molest(?:ed|s)?|touch(?:ed|es)?"
)
THROWN_AT_ME = (
    r"(?:(?:throw|threw|thrown|throwing|hurl(?:ed|ing)?|chuck(?:ed|ing)?)[^.?!]{0,20}"
    r"\bat\s+(?:me|us)\b"
    r"|(?:threw|thrown|throwing|throw|hurled)[^.?!]{0,15}\b(?:against|into|down)\s+(?:the\s+)?"
    r"(?:wall|door|floor|stairs|ground)\b)"
)


HIT_AS_A_CHILD = (
    r"\bmy\s+" + MY_GROWN_UP + r"\b"
    r"[^.?!]{0,40}\b(?:" + _THE_BLOW + r"|burn(?:ed|t)|scalded|"
    r"whipped|belt(?:ed)?|strap(?:ped)?|cane(?:d)?|smack(?:s|ed|ing)?|abused|molested|touched\s+me|"
    r"locked\s+me|starved|smothered|throttled)\b"
    r"[^.?!]{0,40}"
    r"\b(?:when\s+i\s+was\s+(?:a\s+)?(?:kid|child|little|young|small|teenager|teen|"
    r"at\s+school|in\s+school|\d{1,2})|as\s+a\s+(?:kid|child|little\s+\w+|teenager)|"
    r"growing\s+up|back\s+then|years\s+ago|decades\s+ago|my\s+whole\s+childhood|"
    r"all\s+my\s+childhood|(?:used|would)\s+to\s+\w+\s+me)\b",
    r"\bi\s+(?:was|got)\s+(?:hit|beaten|abused|molested|whipped|slapped|kicked|punched)\s+"
    r"(?:as\s+a\s+(?:kid|child|little\s+\w+|teenager)|when\s+i\s+was\s+(?:a\s+)?"
    r"(?:kid|child|little|young|small|teenager|at\s+school)|growing\s+up|my\s+whole\s+"
    r"childhood)\b",
    r"\bmy\s+" + MY_GROWN_UP + r"\b[^.?!]{0,25}\b(?:used\s+to|would)\s+[^.?!]{0,20}\b(?:"
    + THE_BLOW_ON_A_CHILD + r")\b[^.?!]{0,15}\b(?:me|us)\b",
    r"\bmy\s+" + MY_GROWN_UP + r"\b[^.?!]{0,25}\b(?:used\s+to|would)\s+[^.?!]{0,20}"
    + THROWN_AT_ME,
    r"\bi\s+(?:used|would)\s+to\s+(?:get|be)\s+(?:hit|beaten|beat|slapped|punched|kicked|"
    r"whipped|belted|abused|smacked)\b[^.?!]{0,25}\b(?:at\s+home|by\s+my\s+" + MY_GROWN_UP +
    r"|as\s+a\s+(?:kid|child)|when\s+i\s+was)\b",
)
CHILD_HIT_NOW = (
    r"\b(?:still|now|again|these\s+days|nowadays|every\s+(?:day|night|week|time))\s+"
    r"(?:\w+\s+){0,2}(?:hits?|beats?|does|doing|comes?|turns?\s+up)\b",
)
REMORSE_FOR_THE_ACT = (
    r"\b(?:hate|hating|disgusted\s+(?:with|by)|ashamed\s+of|sickened\s+by|disappointed\s+in|"
    r"furious\s+(?:with|at)|angry\s+at)\s+my\s*self\b",
    r"\bi\s*(?:'?m|am|feel|felt)\s+(?:like\s+)?(?:such\s+)?(?:an?\s+)?(?:monster|beast|"
    r"awful\s+person|terrible\s+person|horrible\s+person|bad\s+person)\b",
    r"\bwhat\s+have\s+i\s+done\b",
    r"\bcan'?t\s+believe\s+i\s+(?:did|done)\s+(?:that|it)\b",
)
ABUSE_VERB = (r"(?:hits?|hitting|beat(?:s|ing)?|punch(?:es|ed|ing)?|kick(?:s|ed|ing)?|chok(?:es|ed|ing)|"
              r"slapp?(?:s|ed|ing)?|grab(?:s|bed|bing)?|drag(?:s|ged|ging)?|burn(?:s|ed|ing)?|"
              r"strangl(?:e|es|ed|ing)|push(?:es|ed|ing)?|shov(?:e|es|ed|ing)|"
              r"bit\b|bite|bites|biting|spat\s+at|spit\s+at|throw(?:s|ing)?|threw|hurl(?:s|ed|ing)?|"
              r"yank(?:s|ed|ing)?|twist(?:s|ed|ing)?|wrench(?:es|ed|ing)?|swung\s+at|swing\s+at|"
              r"attack(?:s|ed|ing)?|savaged|mauled|lash(?:es|ed|ing)?\s+out\s+at|"
              r"lunged\s+at|held\s+me\s+down|pinned\s+me|scratch(?:es|ed|ing)?|"
              r"claw(?:s|ed|ing)?)")
HIT_BY_A_VEHICLE = (r"(?!\s+(?:with|by)\s+(?:a\s+|an\s+|the\s+|his\s+|her\s+|their\s+|"
                    r"our\s+|my\s+)?(?:car|cars|van|bike|bikes|bicycle|motorbike|motorcycle|"
                    r"scooter|lorry|truck|bus|train|tram|taxi|car\s+door|door|doors|vehicle|"
                    r"wheelchair|buggy|pram|cart|trolley|skateboard|scooter)\b)")
_NOT_A_THREAT = (r"(?!\s+(?:with|over|about)\s+(?:a\s+|the\s+|his\s+|her\s+|their\s+|"
                 r"my\s+|our\s+)?(?:written|warning|fine|fines|eviction|legal|lawsuit|court|"
                 r"police|report|complaint|solicitor|letter|bill|bill?s|charge|charges|"
                 r"prosecution|dismissal|sack|sacking|redundancy|redundant|fired|disciplinary|"
                 r"hearing|notice|tenancy|deposit)\b)")

BY_NOT_A_THING = (
    r"(?!\s+by\s+(?!(?:(?:him|her|them|his|their|someone|somebody|some\s+men|men|guys|blokes|"
    r"lads|youths|people|strangers)\b|(?:a|an|the|two|three|four|five|several|some|another|"
    r"that|this|one)\s+(?:\w+\s+){0,2}(?:men|women|man|bloke|blokes|stranger|strangers|guy|guys|"
    r"woman|lady|ladies|person|people|group|youth|youths|teenager|teenagers|teen|teens|kid|kids|"
    r"boy|boys|girl|girls|fella|fellas|lad|lads|neighbour|neighbours|driver|carer|partner|"
    r"husband|wife|boyfriend|girlfriend|ex|dad|mum|father|mother|stepdad|stepmum|brother|"
    r"sister|uncle|aunt|cousin|son|daughter|landlord|landlady|housemate|colleague|boss|"
    r"manager)\b)"
    r"|my\s+" + ABUSER + r"\b))")

CLOSE = (r"(?:ex|husband|wife|partner|boyfriend|girlfriend|fiance|fiancee|stepdad|stepmum|stepmom|"
         r"stepfather|stepmother|dad|mum|mom|father|mother|son|daughter|brother|sister|carer|"
         r"uncle|aunt|auntie|nan|grandad|grandpa|grandma)")
THREAT_SUBJECT = r"(?:he'?s|she'?s|they'?re|he|she|they|my\s+" + CLOSE + r")"
THREAT_COERCIVE = (
    r"\b" + THREAT_SUBJECT + r"\b[^.?!]{0,40}\bthreaten(?:s|ed|ing)?\b[^.?!]{0,25}\b"
    r"(?:police|cops?|solicitor|lawyer|court|custody|social\s+services)\b",
    r"\b" + THREAT_SUBJECT + r"\b[^.?!]{0,40}\bthreaten(?:s|ed|ing)?\s+to\s+"
    r"(?:call|ring|report|tell|contact|go\s+to)\b[^.?!]{0,20}\b(?:police|cops?|solicitor|"
    r"lawyer|court|custody|social\s+services)\b",
    r"\bmy\s+" + CLOSE + r"(?:'?s|\s+is|\s+keeps?|\s+has\s+been)\s+threatening\s+my\s+"
    + CLOSE + r"\b",
)

_REFUSED_EXIT = (
    r"(?:past|through|out|out\s+of\s+the\s+(?:house|flat|room|car)|leave|go|go\s+out|"
    r"go\s+anywhere|see\s+(?:(?:my|her|his|the|any|our)\s+)?(?:own\s+)?(?:friends|family|mum|mom|"
    r"dad|mother|father|parents|sister|brother|kids|children|mates|pals|buddies|colleagues|"
    r"coworkers|anyone|people)|speak\s+(?:to|with)\s+"
    r"(?:(?:my|her|his|the|any)\s+)?(?:friends|family|mum|mom|dad|mother|father|parents|"
    r"sister|brother|kids|children|anyone|people)|have\s+(?:any\s+|my\s+own\s+|the\s+)?"
    r"(?:money|wages|bank\s+card|bank\s+account|debit\s+card|keys|a\s+job|my\s+own\s+money|"
    r"friends|a\s+life|people\s+over|visitors|company|a\s+social\s+life)|"
    r"work(?!\s+(?:from|at|in|late|early|nights?|weekends?|evenings?|overtime|flexibly|"
    r"remotely|hybrid|part[\s-]?time|full[\s-]?time|with|on|for))|"
    r"study|sleep|get\s+a\s+job|look\s+for\s+work|"
    r"drive\s+(?:the\s+car|my\s+car|his\s+car|her\s+car|our\s+car|to\s+work|to\s+the\s+shops|"
    r"anywhere|myself)|visit\s+"
    r"(?:(?:my|her|his|any)\s+)?(?:friends|family|mum|mom|dad|mother|father))"
)

ABUSE_VERB_PART = (
    r"(?:hits?|hitting|beat(?:s|ing)?|punch(?:es|ed|ing)?|kick(?:es|ed|ing)?|chok(?:es|ed|ing)|"
    r"slapp?(?:s|ed|ing)?|smack(?:s|ed|ing)?|drag(?:s|ged|ging)?|"
    r"strangl(?:e|es|ed|ing)|shov(?:e|es|ed|ing)|"
    r"spat\s+at|spit\s+at|hurl(?:s|ed|ing)?|attack(?:s|ed|ing)?|savaged|mauled|thump(?:s|ed|ing)?|"
    r"push(?:es|ed|ing)?|whack(?:s|ed|ing)?|head-?butt(?:s|ed|ing)?)")
ABUSE_HIT_ME = (
    r"\b(?:he|she|they|hubby|my\s+" + ABUSER + r")\b.{0,30}\b" + ABUSE_VERB + r"\s+me\b",
    r"\b(?:he|she|they|hubby|my\s+" + ABUSER + r")\b[^.?!]{0,30}\b" + ABUSE_VERB_PART + r"\s+"
    r"(?:my|me\s+in\s+my)\s+(?:face|head|back|arm|arms|leg|legs|ribs?|stomach|"
    r"belly|jaw|eye|eyes|ear|ears|neck|throat|shoulders?|chest|side|hip|hips|thigh|mouth|nose|"
    r"teeth|wrist|knee)\b"
    r"(?![^.?!]{0,40}\b(?:cake|cakes|cream|icing|jelly|bun|buns|pudding|pie|pies|flour|"
    r"bunting|snow|snowdrift|leaves|foam|bubbles|mud|sand|dough|pillow\s+fight)\b"
    r"(?![^.?!]{0,60}\b(?:hit|hits|punch(?:ed|es)?|kick(?:ed|es)?|slap(?:ped|s)?|beat(?:s)?|"
    r"chok(?:ed|es)?|shov(?:ed|es)?|push(?:ed|es)?)\s+me\b"
    r"(?!\s+(?:on|round|in)\s+the\s+back\b))"
    r"(?![^.?!]{0,60}\b(?:breath|breathe|breathing|breathless|blacked\s+out|passed\s+out|"
    r"unconscious|choking|couldnt\s+breathe|could\s+not\s+breathe|no\s+air)\b))",
    r"\b(?:he|she|they|hubby|my\s+" + ABUSER + r")\b[^.?!]{0,30}\b(?:scratch(?:es|ed|ing)?|"
    r"claw(?:s|ed|ing)?)\s+(?:my|me\s+in\s+my)\s+(?:face|head|arm|arms|leg|legs|ribs?|"
    r"stomach|belly|jaw|eye|eyes|ear|ears|neck|throat|shoulders?|chest|side|hip|hips|thigh|"
    r"mouth|nose|teeth|wrist|knee)\b"
    r"(?![^.?!]{0,30}\b(?:on|against|through|by)\s+(?:the|a|an|some|my|his|her|their|our)?\s*\w+)"
    r"(?![^.?!]{0,40}\b(?:bleed|bleeds|bled|bleeding|blood|bruise|bruises|bruised|marks|"
    r"scarred|again|police|scared|afraid|frightened|threaten\w*|strangl\w*|choke\w*|hit|hits|"
    r"punch\w*|kick\w*|beat\w*)\b)",
)
HAS_ME_SUBJECT = r"\b(?:he|she|they|he'?s|she'?s|they'?re|hubby|my\s+" + ABUSER + r")\b"
GRIP_GAME = (r"\b(?:squash|tennis|judo|karate|mma|taekwondo|rugby|football|netball|wrestl\w*|"
             r"sparring|dojo|scrum|scrums|matches?)\b")
GRIP_GAME_FENCE = r"(?![^.?!]{0,30}" + GRIP_GAME + r")"
GRIP_NOT_AN_ASSAULT = (
    GRIP_GAME_FENCE,
    r"(?![^.?!]{0,30}\b(?:play\w*|tickl\w*|laugh\w*|giggl\w*|joking|for\s+fun)\b)"
    r"(?![^.?!]{0,30}\b(?:deadline|deadlines|budget|bills?|rent|mortgage|money|hours|rota|shift|"
    r"shifts|clock|targets?|emails?|paperwork)\b)"
    r"(?![^.?!]{0,30}\b(?:haircut|while\s+(?:he|she|they|it)\s+cut)\b)"
)
GRIP_NOT_AN_ASSAULT_STR = "".join(GRIP_NOT_AN_ASSAULT)

GAME_WORD_STOP = (
    r"(?!the\b|a\b|an\b|home\b|house\b|work\b|school\b|night\b|nights\b|bed\b|morning\b|"
    r"afternoon\b|evening\b|weekend\b|weekends\b|front\b|public\b|private\b|kitchen\b|"
    r"bathroom\b|bedroom\b|hall\b|stairs\b|car\b|street\b|garden\b|pub\b|court\b|"
    r"office\b|hospital\b|head\b|face\b|ribs\b|back\b|stomach\b|chest\b|arm\b|arms\b|"
    r"leg\b|legs\b|neck\b|throat\b|gut\b|kidney\b|kidneys\b|hands?\b|fists?\b|feet\b|"
    r"foot\b|shoulders?\b|knees?\b|elbows?\b)[\w'-]+"
)
GAME_PLAYED = (
    r"\bbeat(?:s|en|ing)?\s+(?:me|us)\s+(?:at|in)\s+(?:the\s+|a\s+)?" + GAME_WORD_STOP
)
GAME_AFTER_ME = (
    r"(?!\s+(?:at|in)\s+(?:the\s+|a\s+)?"
    + GAME_WORD_STOP + r")")
ASK_AFTER_ME = r"(?!\s+up\s+(?:for|to)\b)"

ABUSE = THREAT_COERCIVE + (
    r"\b(?:he|she|they|hubby|my\s+" + ABUSER + r")\b[^.?!]{0,20}\b(?:holds?|keeps?|pins?|"
    r"grips?|presses?)\s+(?:me|us)\s+(?:up\s+)?(?:against|into|onto)\s+(?:the\s+|a\s+|my\s+)?"
    r"(?:wall|floor|door|bed|ground|fridge|cooker|cupboard|sofa|table)\b",
    *ABUSE_HIT_ME,
    r"\b(?:he|she|they|my\s+" + ABUSER + r")\b.{0,30}\b(?:thr(?:ew|ows|owing)|hurl(?:ed|s)|"
    r"lobbed|shov(?:e|es|ed)|push(?:es|ed)|swung|swing|lunged)\b.{0,25}\b(?:at|against)\s+"
    r"(?:me|my\s+(?:head|face|arm|back|leg|son|daughter|kids?|child|mum|dad))\b",
    r"\b(?:he|she|they|my\s+" + ABUSER + r")\b.{0,25}\b(?:hands?|fingers?|arm)\s+(?:round|around|on|"
    r"across)\s+(?:my\s+)?(?:throat|neck)\b",
    r"\bput\s+(?:his|her|their)\s+hands?\s+(?:round|around|on)\s+(?:my\s+)?(?:throat|neck)\b",
    r"\b(?:held|pinned|pressed)\s+me\s+(?:down|against\s+the\s+(?:wall|floor|door|bed)|"
    r"on\s+the\s+(?:floor|ground|bed)|in\s+the\s+(?:kitchen|bathroom|bedroom|hall|hallway))\b"
    + GRIP_NOT_AN_ASSAULT_STR,
    r"\b(?:he|she|they|my\s+" + ABUSER + r")\b.{0,25}\b(?:held|pinned|pressed|pushed|shoved|"
    r"backed|slammed|threw)\s+me\s+(?:up\s+)?(?:against|onto|into|to)\s+the\s+(?:wall|floor|door|"
    r"bed|fridge|cooker|counter|cupboard|sofa|ground)\b" + GRIP_GAME_FENCE,
    HAS_ME_SUBJECT + r".{0,20}\b(?:has|had|have|got|gets|keeps?|kept|"
    r"holds?|held|leaves?|left|pins?|pinned)\s+me\s+(?:pinned|trapped|cornered|locked\s+in|"
    r"pressed|held|shoved|pushed|backed|slammed)\b"
    r"(?!\s+(?:to|on|onto|against|into|in|by)\s+(?:the\s+|a\s+|my\s+|his\s+|her\s+|their\s+|our\s+)?"
    r"(?:rota|rotas|shift|shifts|roster|rosters|list|lists|board|boards|schedule|schedules|"
    r"duty|duties|plan|plans|app|apps|"
    r"desk|desks|office|meeting\s+room|conference\s+room|trolley|till|screen|monitor|keyboard|"
    r"in-?tray|inbox|deadline|deadlines|shop\s+floor|checkout|call\s+list)\b)",
    r"\b(?:he|she|they|my\s+" + ABUSER + r")\b[^.?!]{0,25}\b(?:corner(?:ed|s)?|trapped|backed|"
    r"blocked|pinned)\s+me\s+(?:in|into)\s+(?:the\s+|my\s+|a\s+)?(?:kitchen|bedroom|bathroom|"
    r"bath|hall|hallway|corridor|lift|stairwell|stairs|garage|flat|house|room|doorway|balcony|"
    r"landing|porch|study|shed)\b",
    r"\b(?:he|she|they|my\s+" + ABUSER + r")\b[^.?!]{0,25}\b(?:wouldn?'?t|won'?t|"
    r"would|will|refused?|refuses?)\s*(?:not\s+)?(?:to\s+)?(?:let|allow)\s+me\s+"
    + _REFUSED_EXIT + r"\b",
    r"\b(?:he|she|they|my\s+" + ABUSER + r")\b[^.?!]{0,25}\b(?:doesn'?t|don'?t|didn'?t|"
    r"(?:does|do|did)\s*not)\s*let\s+me\s+" + _REFUSED_EXIT + r"\b",
    r"\b(?:locked|shut|trapped|stuck)\s+(?:in|inside)\s+(?:the\s+|my\s+|a\s+|this\s+)?"
    r"(?:bathroom|bedroom|toilet|kitchen|room|flat|house|hall|hallway|car|cellar|basement|loft|"
    r"attic)\b[^.?!]{0,40}\b(?:he|she|they|my\s+" + ABUSER + r")\b[^.?!]{0,30}"
    r"\b(?:bang(?:ing|s)?|pound(?:ing|s)?|hammer(?:ing|s)?|kick(?:ing|s)?|smash(?:ing|es)?|"
    r"breaking|shout(?:ing|s)?|scream(?:ing|s)?|rattl(?:ing|es))\b",
    r"\b(?:he|she|they|my\s+" + ABUSER + r")\b[^.?!]{0,30}\b(?:bang(?:ing|s)?|pound(?:ing|s)?|"
    r"hammer(?:ing|s)?|kick(?:ing|s)?|shout(?:ing|s)?|scream(?:ing|s)?)\b[^.?!]{0,40}"
    r"\b(?:locked|shut|trapped|stuck)\s+(?:in|inside)\b",
    HAS_ME_SUBJECT + r"[^.?!]{0,15}\b(?:has|have|had|got|keeps?|kept|holds?|held|grabs?|grabbed|"
    r"drags?|dragged|pulls?|pulled|takes?|took)\s+me\s+by\s+(?:the|my|his|her|their)\s+"
    r"(?:throat|neck|hair|scalp|collar|scruff|jaw)s?\b" + GRIP_NOT_AN_ASSAULT_STR,
    HAS_ME_SUBJECT + r"[^.?!]{0,15}\b(?:has|have|had|got|keeps?|kept|holds?|held|pins?|pinned|"
    r"presses?|pressed|shoves?|shoved|pushes?|pushed)\s+me\s+(?:up\s+)?(?:against|onto|into|to)\s+"
    r"(?:the\s+|a\s+|my\s+)?(?:wall|floor|door|bed|ground|fridge|cooker|cupboard|sofa|counter|"
    r"table|car)\b" + GRIP_NOT_AN_ASSAULT_STR,
    r"\b(?:shook|shak(?:es|ing))\s+me\s+(?:hard|violently|roughly|until|so\s+hard)\b",
    r"\b(?:grab(?:s|bed|bing)?|yank(?:s|ed|ing)?|twist(?:s|ed|ing)?|wrench(?:es|ed|ing)?|"
    r"pull(?:s|ed|ing)?)\s+(?:me\s+)?by\s+the\s+(?:hair|throat|neck|arm|wrist|collar|scruff)\b",
    r"\b(?:grab(?:s|bed|bing)?|yank(?:s|ed|ing)?)\s+my\s+(?:arm|wrist|hair|throat|neck|collar)\b",
    r"\b(?:he|she|they|my\s+" + ABUSER + r")\b[^.?!]{0,30}\b(?:hits?|hitting|beat|beats|beating|"
    r"slapp?(?:s|ed)?|punch(?:es|ed)?|kick(?:s|ed)?|struck|thump(?:s|ed)?|whack(?:s|ed)?|"
    r"smack(?:s|ed)?|belt(?:s|ed)?|cuff(?:s|ed)?)\b\s+"
    r"(?:me\s+(?:in|on|across|round|about)\s+)?(?:the|my)\s+"
    r"(?:face|head|arm|ribs|stomach|back|throat|neck|jaw|cheek|nose|eye|eyes|leg|hip|shoulder|"
    r"wrist|chest|side|belly|ear|mouth|thigh|knee)s?\b",
    r"\b(?:he|she|my\s+" + ABUSER + r")\b.{0,30}\bthreaten(?:s|ed|ing)?\s+me\b" + _NOT_A_THREAT,
    r"\b(?:he|she|they|my\s+" + ABUSER + r")\b.{0,30}\bthreaten(?:s|ed|ing)?\s+"
    r"(?:me\b|us\b|to\s+(?:kill|hurt|hit|stab)\s+me)" + _NOT_A_THREAT,
    r"\b(?:he|she|they|my\s+" + ABUSER + r")\b.{0,30}\b(?:said|says|told\s+me)?\s*"
    r"(?:he|she|they)?\s*(?:would|will|is\s+going\s+to|was\s+going\s+to)\s+"
    r"(?:kill|hurt|stab|rape|strangle|shoot)\s+me\b",
    r"\b(?:he|she|they)\s+(?:(?:won'?t|wont|wouldn'?t|wouldnt|didn'?t|doesn'?t|refus(?:es?|ed)\s+to)"
    r"\s+(?:let|allow)|never\s+lets?)\s+me\s+" + _REFUSED_EXIT + r"\b",
    r"\b(?:abusing|abused|abuses)\s+me\b", r"\b(?:sexual(?:ly)?\s+assault(?:ed)?|raped|raping)\b",
    r"\bhits?\s+me\s+(?:when|if|again)\b",
    r"\bafraid\s+(?:of|to\s+go)\s+(?:him|her|them|home|back\s+home)\b",
    r"\bscared\s+(?:of|to\s+go)\s+(?:him|her|home|back\s+home|my\s+(?:husband|partner|dad|mum|boyfriend|girlfriend|carer))\b",
    r"\b(?:locks?|locked)\s+me\s+(?:in|out)\b",
    r"\b(?:" + THREAT_SUBJECT + r"|the\s+(?:man|woman|lady|guy|bloke))\b[^.?!]{0,20}\b"
    r"(?:trapped|pinned|wedged|locked|shut)\s+(?:me|us)\s+(?:in|inside|under|into)\b",
    r"\b(?:he|she|they|my\s+(?:partner|husband|wife|boyfriend|girlfriend|ex|dad|mum|mom|father|"
    r"mother|son|daughter|brother|sister|step(?:dad|mum|mom|father|mother|son|daughter|brother|"
    r"sister)|carer|boy|girl|nan|nana|gran|granny|uncle|aunt|auntie|cousin|in-?laws?))\s+"
    r"(?:won'?t|wont|wouldn'?t|wouldnt|refus(?:es?|ed)\s+to|refuse\s+to|never\s+lets?\s+me|"
    r"didn'?t\s+let|doesn'?t\s+let|did\s+not\s+let)\s+let\s+me\s+" + _REFUSED_EXIT + r"\b",
    r"\bthreatened?\s+(?:to\s+kill|me\s+with)\b",
    r"\b(?:(?:he|she|they|someone|somebody|my\s+" + CLOSE + r")'?s|they'?re|"
    r"is|are|keeps?|has\s+been|have\s+been)\s+threatening\s+(?:me|us)\b" + _NOT_A_THREAT,
    r"\b(?:i'm|i\s+am)\s+(?:being\s+)?(?:controlled|coerced)\b",
    r"\b(?:i'm|i\s+am|im|i\s+was|i\s+have\s+been|i've\s+been|ive\s+been|i\s+keep\s+being|"
    r"i\s+keep\s+getting)\s+(?:being\s+|getting\s+)?(?:abused|threatened|stalked|followed|"
    r"watched|harassed|hit|attacked|assaulted|raped|molested|groomed|"
    r"beaten\s+up)\b" + BY_NOT_A_THING + _NOT_A_THREAT,
    r"\b(?:i'm|i\s+am|im)\s+(?:being|getting)\s+(?:choked|strangled)\b"
    + BY_NOT_A_THING + _NOT_A_THREAT,
    r"\b(?:i\s+was|i\s+have\s+been|i've\s+been|ive\s+been|i\s+keep\s+(?:being|getting))\s+"
    r"(?:being\s+|getting\s+)?(?:choked|strangled)\b(?!\s+(?:about|over)\b)"
    + BY_NOT_A_THING + _NOT_A_THREAT,
    r"\b(?:he|she|they|my\s+\w+)'?(?:s|ve)?\s+(?:been\s+)?(?:hurting|hitting|strangling)"
    r"\s+me\b" + ASK_AFTER_ME,
    r"\b(?:he|she|they|my\s+\w+)'?(?:s|ve)?\s+(?:been\s+)?beating\s+me\b"
    + GAME_AFTER_ME + ASK_AFTER_ME,
    r"\bmy\s+(?:partner|husband|wife|boyfriend|girlfriend|dad|mum|father|mother|ex|carer)\s+is\s+"
    r"(?:being\s+)?(?:abusive|violent)\b|\bmy\s+(?:partner|husband|wife|boyfriend|girlfriend|dad|"
    r"mum|father|mother|ex|carer)\s+is\s+(?:controlling|coercive)\b",
    r"\b(?:he|she|they)'?s?\s+(?:being|is|keeps?\s+being)\s+(?:abusive|violent)\b",
    r"\b(?:he|she|they)\s+is\s+being\s+(?:abusive|violent)\b",
    r"\bmy\s+(?:violent|abusive|controlling|coercive|dangerous|aggressive|threatening)\s+"
    r"(?:partner|husband|wife|boyfriend|girlfriend|dad|mum|father|mother|ex|carer|"
    r"son|daughter|brother|sister|stepdad|stepdad|stepmum|stepfather|stepmother)\b",
    r"\b(?:someone|somebody|a\s+(?:man|bloke|guy|woman|lad|person)|the\s+(?:man|woman|person))\b"
    r"[^.?!]{0,25}\b" + ABUSE_VERB + r"\s+me\b" + HIT_BY_A_VEHICLE,
    r"\b(?:someone|somebody)\b[^.?!]{0,25}\bhurt(?:s|ing)?\s+me\b" + HIT_BY_A_VEHICLE,
    r"\b(?:someone|somebody|a\s+(?:man|bloke|guy|woman|lad|person|partner)|"
    r"the\s+(?:man|woman|person|partner))\b[^.?!]{0,25}\b"
    r"(?:is\s+|was\s+|being\s+|been\s+)?(?:abusive|violent|controlling|coercive|dangerous|"
    r"aggressive)\b",
    r"\b(?:someone|somebody|a\s+(?:man|bloke|guy|woman|lad|person)|the\s+(?:man|woman|person))\b"
    r"[^.?!]{0,25}\b(?:scares|frightens|terrifies|intimidates)\s+me\b",
    r"\b(?:i|we|he|she|they)\s+(?:was|were|got|just\s+got)\s+(?:attacked|assaulted|mugged|beaten\s+up)\b",
    r"\b(?:i'm|i\s+am)\s+(?:scared|terrified)\s+of\s+(?:going\s+home|him|her)\b",
    r"\b(?:someone|somebody|a\s+(?:man|bloke|guy|woman|lad)|(?:the|our|my)\s+neighbours?|"
    r"next\s+door)\b[^.?!]{0,30}\bthreaten(?:s|ed|ing)?\s+(?:me\b|to\s+(?:kill|hurt|harm|"
    r"hit|stab|beat)\s+me)",
)
PARTNER_CLOSE = (r"(?:ex|exes|husband|wife|partner|boyfriend|girlfriend|fiance|fiancee|"
                 r"baby\s*daddy|baby\s*dad|baby\s*mother|baby\s*mum)")
PURSUIT_SUBJECT = (r"\b(?:my\s+" + PARTNER_CLOSE + r"|my\s+ex'?s?)\b",)
NOT_A_FEAR = (r"(?!\s+(?:that\s+)?(?:hes|shes|theyre|its|it'?s|im|i'?m|ill|i'?ll|hell|well|"
              r"going\s+to\s+be|we\s+will|we'?ll)\s*(?:going\s+to\s+be\s+)?(?:late|"
              r"late\s+home|in\s+trouble|on\s+time))")
PURSUIT_FEAR = (
    r"\b(?:i'?m|i\s+am|im)\s+(?:(?:really|so|very|that|proper|properly|absolutely|dead|"
    r"scared\s+witless)\s+)*(?:scared|frightened|terrified|afraid|panicking|shaking|worried)\b"
    + NOT_A_FEAR,
    r"\b(?:scared|frightened|terrified|afraid)\s+(?:of|to\s+go|to\s+leave|to\s+open)\b",
)
PURSUIT_SUBJECT_EX = (r"\b(?:my\s+(?:ex|exes|baby\s*daddy|baby\s*dad|baby\s*mother|baby\s*mum)|"
                      r"my\s+ex'?s?)\b",)
PURSUIT_OUTSIDE = (
    r"\b(?:waiting|waits|sat|sitting|stood|standing|parked|lurking|hiding|hovering|"
    r"hanging\s+around)\s+(?:right\s+|still\s+|now\s+)?(?:outside|out\s+front|in\s+the\s+car\s+"
    r"outside|round\s+the\s+back)\b",
    r"\bwait(?:ing|s|ed)?\s+for\s+(?:me|us)\b",
)
PURSUIT_PLACE_WORK = (
    r"\b(?:outside|in\s+front\s+of|at\s+the\s+end\s+of|round\s+the\s+back\s+of)\s+"
    r"(?:my|our|the)\s+(?:work|workplace|office|school|nursery|college|uni|university|gates)\b",
    r"\b(?:waiting|waits|sat|sitting|stood|standing|parked|lurking|hiding|hovering|hanging\s+around)"
    r"\s+(?:right\s+|still\s+|now\s+)?(?:outside|near)\s+(?:my|our|the)\s+(?:work|workplace|"
    r"office|school|nursery|college|uni|university|gates)\b",
)
PURSUIT_LOUD = (
    r"\b(?:shouting|yelling|screaming)\s+at\s+(?:the\s+)?(?:football|telly|tv|match|game|"
    r"radio|news|kids|dog|cat|ref|referee)\b(?!.*\b(?:i'?m|i\s+am|im)\s+(?:scared|terrified))",
    r"\b(?:shouting|yelling|screaming|drunk|hammering|banging|pounding)\b",
    r"\b(?:won'?t|wont|refuses?\s+to)\s+(?:leave|go|move)\b",
)
def _both_here(*groups):
    parts = ["(?=.*(?:" + "|".join(group) + "))" for group in groups]
    return "".join(parts)


PURSUIT = (
    _both_here(PURSUIT_SUBJECT, PURSUIT_PLACE_HOME),
    _both_here(PURSUIT_SUBJECT, (r"\b(?:is|was|keeps?|still)\s+(?:right\s+)?(?:outside|here|back)\b",),
               PURSUIT_FEAR + PURSUIT_LOUD),
    _both_here(PURSUIT_SUBJECT_EX, PURSUIT_PLACE_WORK),
    _both_here(PURSUIT_SUBJECT_EX, PURSUIT_OUTSIDE),
    r"\b(?:he|she|they|hes|shes|theyre)'?s?\b[^.?!]{0,12}\b"
    r"(?:follow(?:s|ing|ed)?|stalk(?:s|ing|ed)?)\s+(?:me|us)\b",
)
ABUSE_VERBAL_PERSON = (r"(?:he|she|they|hubby|husband|wife|partner|boyfriend|girlfriend|fiance|"
                       r"fiancee|ex|mum|mom|mam|mother|dad|father|stepdad|stepmum|stepmom|"
                       r"stepfather|stepmother|nan|nana|gran|granny|grandma|grandad|grandpa|"
                       r"carer)")
ABUSE_VERBAL_MAD = (r"(?:mental|crazy|mad)(?!\s+(?:(?:about|over)\s+"
                    r"(?!everything|anything|every\s+thing|all\s+(?:of|the)|whatever|"
                    r"how\s+i|everyone|every\s+time|being|doing|saying|wanting)"
                    r"|at\s+(?!the\s+time|first|least)"
                    r"|in\s+(?:love|bed|a\s+good\s+way|the\s+good\s+way|a\s+kind\s+way)))")
ABUSE_VERBAL_LABEL = (r"(?:names|stupid|thick|dumb|useless|worthless|lazy|fat|ugly|pathetic|"
                      r"hopeless|a\s+failure|a\s+loser|a\s+waste\s+of\s+space|a\s+waste|"
                      r"nothing|" + ABUSE_VERBAL_MAD + r"|psycho|disgusting|a\s+slag|a\s+slut|a\s+bitch|"
                      r"a\s+cow|rubbish|a\s+disappointment|a\s+mistake|an\s+idiot|an\s+imbecile|"
                      r"stupid\s+cow|fat\s+cow|silly\s+cow|cretin|a\s+joke|unloveable|"
                      r"unlovable|a\s+burden|a\s+drain|a\s+piece\s+of\s+shit|"
                      r"a\s+piece\s+of\s+crap|shit)")
CHILD_AGGRESSOR = (
    r"\b(?:(?:my|our|his|her|their|the)\s+(?:son|sons|daughter|daughters|child|children|kid|kids|"
    r"toddler|baby|teen|teenager|teenagers|boy|girl|boys|girls|little\s+one)|"
    r"my\s+(?:eldest|oldest|youngest))\b"
    r"(?!\s+[^.?!]{0,12}\b(?:when|while|as)\s+(?:he|she|they)\b)[^.?!]{0,12}"
    r"\b(?:pushes?|pushed|pushing|hits?|hit|"
    r"hitting|kicks?|kicked|kicking|slaps?|slapped|slapping|bites?|bit|biting|punches?|punched|"
    r"punching|calls?\s+me|calling\s+me|called\s+me|swears?\s+at\s+me|shouts?\s+at\s+me|"
    r"yells?\s+at\s+me)\b",
)[:1]
ABUSE_VERBAL_SUBJECT = (r"\b(?:he|she|they|he'?s|she'?s|they'?re|my\s+" + ABUSE_VERBAL_PERSON +
                        r")\b")
ABUSE_VERBAL = (
    ABUSE_VERBAL_SUBJECT + r"[^.?!]{0,25}\b(?:calls?|calling|"
    r"called|keeps\s+calling)\s+me\s+(?:(?:a|an)\s+)?" + ABUSE_VERBAL_LABEL + r"\b",
    ABUSE_VERBAL_SUBJECT + r"[^.?!]{0,25}\b(?:tells?|telling|"
    r"told|says?|saying|said)\s+(?:me\s+)?i(?:'?m|\s+am)\s+(?:(?:a|an)\s+)?"     + ABUSE_VERBAL_LABEL + r"\b",
    ABUSE_VERBAL_SUBJECT + r"[^.?!]{0,30}\b(?:keeps?|kept|"
    r"always|constantly|regularly|never\s+stops|every\s+(?:day|night|week))\b[^.?!]{0,20}"
    r"\b(?:putting\s+me\s+down|put\s+me\s+down|running\s+me\s+down|having\s+a\s+go\s+at\s+me)\b",
    ABUSE_VERBAL_SUBJECT + r"[^.?!]{0,30}"
    r"\b(?:puts?\s+me\s+down|putting\s+me\s+down|runs?\s+me\s+down|running\s+me\s+down|"
    r"has\s+a\s+go\s+at\s+me|having\s+a\s+go\s+at\s+me)\b[^.?!]{0,25}"
    r"\b(?:all\s+the\s+time|all\s+day|constantly|always|every\s+(?:day|night|week|time)|"
    r"non[\s-]?stop)\b",
)
ABUSE_VERBAL_FINE = (
    r"\b(?:call|calls|calling|called)\s+each\s+other\b",
    r"\b(?:we|we'?re|were)\s+(?:both\s+)?(?:call|calls|calling|tease|teasing|wind)\b",
    r"\b(?:me\s+and|between\s+me\s+and|my\s+(?:mates?|friends?|lads|colleagues?|team|"
    r"classmates?|schoolmates?|flatmates?|housemates?))\b[^.?!]{0,20}\b(?:call|calls|calling|"
    r"tease|teasing|rip\s+into)\b",
    r"\b(?:nickname|nicknames|term\s+of\s+endearment|pet\s+name|affectionately|"
    r"fondly)\b",
    r"\b(?:in\s+fun|for\s+a\s+laugh|in\s+good\s+fun|in\s+jest|in\s+play|at\s+five-a-side|"
    r"on\s+the\s+pitch|at\s+rugby|at\s+football|in\s+training)\b",
)
ABUSE_HEAD_INTO = (
    r"\b(?:he|she|they|hubby|my\s+" + ABUSER + r")\b[^.?!]{0,20}"
    r"\b(?:push(?:ed|es|ing)?|shov(?:ed|es|ing)|slam(?:med|s)?|bang(?:ed|s|ing)?|"
    r"smash(?:ed|es|ing)?|knock(?:ed|s|ing)?|ram(?:med|s|ming)?|thr(?:ew|ows|owing)|"
    r"yank(?:ed|s|ing)?|drag(?:ged|s|ging)?|smack(?:ed|s|ing)?|press(?:ed|es|ing)?)\b"
    r"[^.?!]{0,15}\bmy\s+(?:head|face)\b[^.?!]{0,15}"
    r"\b(?:into|onto|against|off|through)\b\s*(?:the\s+|a\s+|his\s+|her\s+)?"
    r"(?:wall|walls|door|doors|door\s?frame|doorframe|frame|floor|ground|table|table\s?top|"
    r"desk|worktop|counter|cupboard|cabinet|fridge|freezer|radiator|banister|stairs|"
    r"stair\s?gate|step|kerb|curb|pavement|window|windowsill|sill|sink|bath|bathroom|toilet|"
    r"headboard|bed\s?frame|wardrobe|shelf|shelves|cooker|oven|dashboard|car|van|"
    r"kitchen\s?unit|brick\s?wall|concrete)\b"
)

SOFT_FACE_PUSH = (
    r"\b(?:he|she|they|hubby|my\s+" + ABUSER + r")\b[^.?!]{0,20}"
    r"\b(?:push(?:ed|es|ing)?|shov(?:ed|es|ing)|slam(?:med|s)?|bang(?:ed|s|ing)?|"
    r"smash(?:ed|es|ing)?|ram(?:med|s|ming)?|thr(?:ew|ows|owing)|dunk(?:ed|s|ing)?)\b"
    r"[^.?!]{0,15}\bmy\s+(?:face|head)\b[^.?!]{0,15}"
    r"\b(?:into|onto|in|through)\b\s*"
    r"(?:(?:the|a|his|her|my|their)\s+)?(?:\w+\s+){0,2}"
    r"(?:cake|cakes|snow|mud|sand|dough|flour|icing|bubbles|foam|paint|slime)\b"
)
SOFT_FACE_STOP = (
    r"\b(?:hit|hits|hitting|punch(?:ed|es|ing)?|kick(?:ed|es|ing)?|slap(?:ped|s|ping)?|"
    r"beat(?:s|en)?|chok(?:ed|es|ing)?|shov(?:ed|es)?\s+me|push(?:ed|es)?\s+me|"
    r"held\s+me|hold(?:ing)?\s+me|kept\s+me|held\s+it|pinned)\b",
    r"\b(?:can'?t|couldn'?t|could\s+not|cannot|unable\s+to|struggl\w*\s+to)\s+breath\w*\b",
    r"\b(?:gasping|choking|unconscious|blue\s+in\s+the\s+face)\b",
)
PLAY_FACE_REPLIES = (
    "A proper mess. Were you both laughing, or did it land badly?",
    "Ha - somebody got you. Was it a laugh, or did that land badly?",
    "That's the classic. Were you both laughing, or did it not feel funny to you?",
)

ABUSE = ABUSE + PURSUIT + ABUSE_VERBAL + (ABUSE_HEAD_INTO,)
ABUSE_PURSUIT_HARD = (
    r"\b" + ABUSE_VERB + r"\s+(?:me|us)\b",
) + PURSUIT_FEAR + (
    r"\b(?:drunk|threatening|hit|hitting|kicked|pushed|grabbed)\b",
    r"\b(?:won'?t|wont|refuses?)\s+(?:leave|go|let)\b",
)
ABUSE_DISCLOSURE = (
    r"\b(?:i|we)\s+(?:was|were|have\s+been|'ve\s+been|had\s+been)\s+(?:being\s+|getting\s+)?"
    r"(?:abused|assaulted|raped|molested|groomed|stalked|harassed|threatened|beaten|hit|"
    r"attacked|choked|strangled)\b",
    r"\b(?:i|we)\s+(?:was|were)\s+in\s+an?\s+(?:abusive|violent)\s+(?:relationship|marriage|home)\b",
    r"\b(?:i|we)\s+used\s+to\s+be\s+(?:beaten|hit|abused|assaulted)\b",
)
ABUSE_DISCLOSURE_FINE = (
    r"\bthreatened\s+(?:with|over|about)\s+(?:a\s+|the\s+|his\s+|her\s+|their\s+|my\s+|"
    r"our\s+)?(?:being\s+)?(?:written\s+)?(?:warning|fine|fines|eviction|legal|lawsuit|court|"
    r"police|report|complaint|solicitor|letter|bills?|charges?|prosecution|dismissal|sack|"
    r"sack(?:ing|ed)|redundancy|redundant|fired|firing|disciplinary|hearing|notice|tenancy|"
    r"deposit)\b",
)
ABUSE_MEMORY = (
    r"\bas\s+a\s+(?:child|kid|baby|boy|girl|teenager|teen|little\s+(?:boy|girl|kid|one))\b",
    r"\bgrowing\s+up\b", r"\bin\s+my\s+(?:childhood|teens|twenties|thirties)\b",
    r"\bwhen\s+i\s+was\s+(?:a\s+(?:child|kid|baby|teenager|little\s+\w+)|young|little|small|"
    r"at\s+school|in\s+school|at\s+college|at\s+university)\b",
    r"\bat\s+(?:school|primary|secondary|college|university)\b",
    r"\bat\s+my\s+(?:old|previous|last|former)\s+(?:job|work|school|house|flat)\b",
    r"\byears\s+and\s+years\s+ago\b", r"\byears\s+ago\b", r"\bages\s+ago\b",
    r"\bdecades?\s+ago\b", r"\ba\s+long\s+(?:time|while)\s+ago\b",
    r"\bback\s+(?:then|in\s+(?:the\s+)?(?:\d0s|\d{4}))\b", r"\bin\s+the\s+\d0s\b",
    r"\bused\s+to\b", r"\bmy\s+(?:childhood|past)\b",
)
ABUSE_NOW = (
    r"\b(?:still|now|again)\s+(?:\w+\s+){0,2}(?:does|doing|hits?|hurts?\s+me|beats?|"
    r"threatens?|follows?|watches?|comes?|turns?\s+up|shows?\s+up|calls?|texts?|happens?|"
    r"happening|at\s+it)\b",
    r"\b(?:keeps?\s+(?:doing|on|at)|hasn'?t\s+stopped|never\s+stopped|carries\s+on)\b",
    r"\b(?:it|this|he|she)\s*(?:'s|s|\s+is)?\s*(?:happening|going\s+on|happened)\s+again\b",
    r"\bat\s+it\s+again\b",
    r"\b(?:every|each)\s+(?:day|night|morning|week|evening)\b",
    r"\b(?:nowadays|these\s+days)\b",
    r"\b(?:tonight|yesterday|last\s+night|this\s+(?:morning|week))\b",
)
BLOW_THINGS = (r"(?:bottles?|glasses?|pans?|frying\s+pans?|saucepans?|bats?|baseball\s+bats?|"
               r"belts?|belt\s+buckles?|chairs?|stools?|cups?|mugs?|plates?|bowls?|knife|knives|"
               r"sticks?|canes?|hammers?|bricks?|stones?|rocks?|remotes?|remote\s+controls?|"
               r"shoes?|boots?|slippers?|trainers?|books?|newspapers?|candlesticks?|spanners?|"
               r"wrenches?|wires?|cables?|cords?|pipes?|rods?|bars?|iron\s+bars?|"
               r"rolling\s+pins?|ladles?|spoons?|wooden\s+spoons?|forks?|pokers?|torches?|"
               r"phones?|lamps?|vases?|ashtrays?|tools?|hands?|fists?|feet|foot|elbows?|knees?|"
               r"shoulders?)")

SOFT_HIT_THING = (
    r"(?:pillow|cushion|duvet|blanket|quilt|snowball(?:s)?|ball(?:s)?|beach\s+ball|"
    r"plastic\s+ball|tennis\s+ball|frisbee|sponge|flannel|tea\s+towel|towel|"
    r"newspaper|magazine|paper|roll?ed[\s-]?up\s+(?:paper|newspaper|magazine|towel)|"
    r"water\s?bomb|water\s?balloon|water\s+pistol|sock|slipper|plush\s+toy|teddy|toy|"
    r"stickle\s?brick|lego|balloon|cushion\s+case)"
)
PLAY_NAMED = (
    r"(?:pillow\s+fight|snowball\s+fight|water\s+fight|food\s+fight|play\s?fight\w*|"
    r"nerf\s+(?:gun|war|fight)|paintball|tickl\w+|"
    r"muck(?:ing)?\s+(?:about|around)|mess(?:ing)?\s+(?:about|around)|"
    r"fool(?:ing)?\s+(?:about|around)|lark(?:ing)?\s+(?:about|around)|"
    r"jok(?:ing|e)\s+(?:about|around)|banter|"
    r"we\s+(?:were|was|are)\s+(?:only\s+|just\s+)?"
    r"(?:playing|mucking|messing|fooling|larking|joking|having\s+a\s+laugh)|"
    r"we\s+both\s+(?:laughed|were\s+laughing|laugh)|we\s+were\s+laughing|"
    r"playing\s+(?:catch|football|rounders|netball|basketball|tag|a\s+game|games|together))"
)
SOFT_HIT_VERB = (
    r"(?:hit|hits|hitting|slapped|slaps|smacked|whacked|pelted|threw|throws|thrown|"
    r"sprayed|squirted|flicked|dunked|dumped|doused)"
)

ABUSE_FINE = (
    r"\bbeat(?:s|en|ing)?\s+(?:me|us)\s+(?:at|in)\s+(?:chess|cards|poker|pool|snooker|billiards|"
    r"darts|tennis|badminton|table\s+tennis|ping\s?pong|squash|golf|football|rugby|cricket|"
    r"basketball|netball|scrabble|monopoly|cluedo|checkers|draughts|dominoes|mario\s?kart|"
    r"video\s+games?|the\s+quiz|the\s+game|the\s+final|the\s+match|the\s+league|"
    r"arm\s?wrestl\w*)\b",
    GAME_PLAYED,
    r"\bhit(?:s|ting)?\s+(?:me|us)\s+up\s+(?:for|to)\b",
    r"\b(?:had|has|have|got|gets|kept|keeps)\s+me\s+cornered\s+(?:at|during|after)\s+(?:the\s+|"
    r"a\s+|his\s+|her\s+)?(?:party|pub|wedding|conference|meeting|office|work|do|dinner|"
    r"reception|barbecue|bbq|gig|match|networking\s+event)\b",
    r"\bcornered?\s+me\s+(?:to\s+(?:talk|ask|discuss|pitch|sell|persuade|convince|apologise|"
    r"apologize)|at\s+(?:the\s+|a\s+)?(?:party|pub|wedding|conference|meeting|office|work|do))\b",
    r"\bmy\s+(?:mum|mom|mam|dad|mother|father|parents?|nan|nana|grandad|grandma)\b[^.?!]{0,25}"
    r"\b(?:let|allow)\s+me\s+(?:go|out|stay|leave)\b",
    r"\b(?:landlord|landlady|letting\s+agent|agent|council|employer|boss|manager|company|firm|"
    r"university|college|school|gym)\b[^.?!]{0,30}\b(?:let|allow)\s+me\s+"
    r"(?:leave|go|out|past)\b",
    r"\b(?:debt\s+collector|debt\s+collectors|bailiffs?|bank|mortgage|lender|utility|"
    r"utilities|energy|water\s+company|broadband|phone\s+company|insurer|insurance|"
    r"hmrc|tax\s+office|dvla)\b[^.?!]{0,40}\bthreaten(?:s|ed|ing)?\s+(?:me|us)\b",
    r"\b(?:landlord|letting\s+agent|agent|council|housing|bank|mortgage|utility|utilities|"
    r"energy|water\s+company|broadband|phone\s+company|mobile\s+network|insurer|insurance|"
    r"employer|boss|manager|company|firm|agency|payroll|hr\b|hmrc|tax\s+office|dvla|"
    r"university|college|school|gym|debt\s+collector|solicitor)\b[^.?!]{0,40}"
    r"\bthreaten(?:s|ed|ing)?\b[^.?!]{0,25}\b(?:over|about|with)\s+"
    r"(?:a\s+|the\s+|his\s+|her\s+|their\s+|my\s+|our\s+)?(?:money|pay|wages|salary|rent|"
    r"hours|shifts?|rota|arrears|fees?|charges?|debt|bills?)\b",
    r"\bhit\s+(?:on|with)\b",
    r"\bfeel(?:s|ing)?\s+like\s+(?:i\s*(?:'m|am)|im)\s+being\s+watched\b",
    r"\bharass(?:ed|es|ing|ment)\b[^.?!]{0,30}\b(?:at|from)\s+(?:work|the\s+office|my\s+job)\b",
    r"\b(?:thr(?:ew|ows)|push(?:ed|es)|shov(?:ed|es)|kick(?:ed|s)?|hit|hits|slapped)\b"
    r"(?!\s+(?:my|his|her|their)\b)(?!\s+me\s+(?:in|on|round|across)\b)[^.?!]{0,20}\b(?:ball|snowball|"
    r"frisbee|water\s+balloon|pillow|toy|party|surprise|birthday|early\s+night|hint|look)\b",
    r"\b(?:push(?:ed|es)|shov(?:ed|es)|thr(?:ew|ows))\s+me\s+(?:into|in)\s+the\s+"
    r"(?:pool|water|sea|lake|river|snow|leaves)\b",
    r"\b(?:push(?:ed|es)|shov(?:ed|es))\s+me\s+(?:in|on)\s+the\s+(?:buggy|pushchair|wheelchair|"
    r"swing|sledge|sled|trolley|bike|boat)\b",
    r"\b(?:my|his|her)\s+(?:sister|brother|friend|mate|son|daughter|kids?)\s+(?:hit|hits|punched|"
    r"pushed|kicked|slapped)\s+me\s+(?:at|during|in)\s+(?:rugby|football|the\s+match|training|"
    r"practice|a\s+game|the\s+game|playtime|the\s+pool)\b",
    r"\bmy\s+(?:son|daughter|child|children|kid|kids|baby|babies|toddler|nephew|niece|"
    r"grandson|granddaughter)\b[^.?!]{0,40}\b(?:bang(?:ing|s)?|pound(?:ing|s)?|kick(?:ing|s)?|"
    r"hammer(?:ing|s)?|shout(?:ing|s)?)\b",
    r"\bmy\s+(?:son|daughter|niece|nephew|godson|goddaughter)\b[^.?!]{0,25}\b"
    r"(?:(?:has|have|had|got|keeps?|kept)\s+me\s+pinned|pinned\s+me|wrestl(?:ed|es|ing)\s+me)\b",
    r"\bmy\s+(?:kid|kids|child|children|toddler|baby|babies|newborn)\b[^.?!]{0,25}\b"
    r"(?:(?:has|have|had|got|keeps?|kept)\s+me\s+(?:pinned|trapped|stuck)|"
    r"(?:pinned|trapped|wrestl(?:ed|es|ing))\s+me)\b",
    r"\b(?:grab(?:bed|s)?|held|took)\b[^.?!]{0,25}\bto\s+(?:hug|kiss|say|shake|stop|help|save|"
    r"pull\s+me\s+up|hold|steady|catch|guide|lead|thank|greet|calm)\b",
    r"\b(?:as\s+(?:i|he|she)\s+(?:fell|slipped))\b",
    r"\bhit(?:s|ting)?\s+me\s+with\s+"
    r"(?!(?:(?:the|a|an|my|his|her|their|this|that)\s+)?(?:washing|clothes|clothesline|fishing|"
    r"tow|washing-up|party|garden|climbing)\s*-?\s*line\b)"
    r"(?:(?:the|a|an|this|that|his|her|their)\s+)?"
    r"(?:[\w'-]+\s+){0,2}(?:next\s+)?(?:deadline|deadlines|bill|bills|news|invoice|invoices|fine|tax|taxes|work|"
    r"project|projects|question|questions|idea|ideas|surprise|party|joke|jokes|pun|punchline|"
    r"line|lines|quote|quotes|fact|facts|truth|hint|warning|newsflash|update|updates|headline|"
    r"headlines|statistic|statistics|stats|figure|figures|number|numbers|story|stories|riddle|"
    r"suggestion|suggestions|advice|compliment|compliments|argument|excuse|excuses|ultimatum|"
    r"guilt\s+trip|lecture|earful|mouthful|reality\s+check|curveball|revelation|rumour|rumor|"
    r"gossip|opinion|promise|invite|invitation|letter|email|text|phone\s+call)\b"
    r"(?!\s+of\s+(?:punches|blows|kicks|hits|slaps|thumps|digs|jabs|beatings|whacks|wallops|"
    r"shots|smacks|strikes|knocks)\b)"
    r"(?!\s+(?:opener|book|books|plate|plates|sheet|sheets|skate|skates|prop|props|"
    r"board|boards|rack|stand|clip|gun|punch|hole|weight|pin|block|cutter|knife|bat|pad|bag|"
    r"cover|holder|rest|frame|case|box|bag|handle|head|piece|booklet|boards?)\b)"
    r"(?!(?:[^.?!]{0,40})\b(?:and|then|but|so)\b[^.?!]{0,30}"
    r"(?:hit|hits|hitting|punched|punching|slapped|slapping|kicked|kicking|shoved|shoving|"
    r"pushed|pushing|grabbed|grabbing|choked|choking|strangled|beat|beating|thumped|whacked|"
    r"headbutted|pinned|dragged|smashed)\s+(?:me|my|us)\b(?!\s+(?:with|by)\b))"
    r"(?![^.?!]{0,40}\b(?:keeps?|kept)\s+(?:on\s+)?(?:hitting|punching|slapping|kicking|"
    r"shoving|pushing|grabbing|choking|beating|thumping|whacking)\s+(?:me|my|us)\b)"
    r"(?![^.?!]{0,30}\b(?:and|then|or|but)\b[\s,]+(?:(?:then|also|with|by)\s+)?"
    r"(?:(?:a|an|the|his|her|their|my|our)\s+)?" + BLOW_THINGS +
    r"\b(?!\s+(?:of|on|round|around|to)\b))",
    r"\b(?:bailiffs?|debt\s+collectors?)\b[^.?!]{0,40}"
    r"\bthreaten(?:s|ed|ing)?\b",
    r"\b(?:playfully|jokingly|in\s+play|for\s+fun|messing\s+about|playfight\w*|larking\s+about|"
    r"tickl\w+)\b",
    r"\b(?:muck(?:ing)?\s+(?:about|around)|mess(?:ing)?\s+(?:about|around)|"
    r"fool(?:ing)?\s+(?:about|around)|lark(?:ing)?\s+(?:about|around)|"
    r"jok(?:ing|e)\s+(?:about|around)|muck(?:ing)?\s+around)\b",
    r"\b" + SOFT_HIT_VERB + r"\b[^.?!]{0,24}\b(?:my|the|his|her|your)\s+(?:head|face)\b"
    r"[^.?!]{0,24}\bwith\s+(?:a\s+|an\s+|the\s+|some\s+)?" + SOFT_HIT_THING + r"\b",
    r"\b" + SOFT_HIT_VERB + r"\b[^.?!]{0,40}\bwith\s+(?:a\s+|an\s+|the\s+|some\s+)?"
    + SOFT_HIT_THING + r"\b[^.?!]{0,60}" + PLAY_NAMED + r"\b",
    r"\b" + PLAY_NAMED + r"\b[^.?!]{0,60}\b" + SOFT_HIT_VERB + r"\b[^.?!]{0,40}\bwith\s+"
    r"(?:a\s+|an\s+|the\s+|some\s+)?" + SOFT_HIT_THING + r"\b",
    r"\b" + PLAY_NAMED + r"\b[^.?!]{0,60}\b(?:threw|throw|thrown|throws|pelted|sprayed|"
    r"squirted)\b[^.?!]{0,20}\b" + SOFT_HIT_THING + r"\s+at\s+(?:me|us)\b",
    r"\bmy\s+(?:son|daughter|child|kid|baby|toddler|boy|girl|children|stepson|stepdaughter|"
    r"grandson|granddaughter|nephew|niece|little\s+one)\b[^.?!]{0,30}"
    r"\b(?:bit|bite|bites|biting)\s+me\b",
    r"\bmy\s+(?:baby|toddler|child|kid|little\s+one|newborn|infant|two\s+year\s+old|"
    r"three\s+year\s+old)\b[^.?!]{0,30}"
    r"\b(?:hit|hits|hitting|kicked|kicks|kicking|slapped|slaps|slapping|pinched|pinches|pinching|"
    r"scratched|scratches|scratching|pushed|pushes|shoved|shoves|headbutted|headbutts)\s+me\b",
    r"\b(?:they|someone)\s+(?:are|is|was|were)?\s*(?:threatening|threatened)\s+me\b"
    r"[^.?!]{0,30}\b(?:debt|debts|money|loan|loans|repayment|repayments|bill|bills)\b",
    r"\b(?:boss|manager|colleague|coworker|co-worker|supervisor)\b[^.?!]{0,30}\bthreaten"
    r"(?![^.?!]{0,60}\b(?:kill|kills|killing|murder|hurt|hurts|harm|attack|stab|shoot|"
    r"strangle|choke|rape|beat|punch|hit|slap|grab|shove|push|throat|weapon|knife|gun)\b)",
    r"\bthreaten(?![^.?!]{0,60}\b(?:kill|kills|killing|murder|hurt|hurts|harm|attack|stab|"
    r"shoot|strangle|choke|rape|beat|punch|hit|slap|grab|shove|push|throat|weapon|knife|gun)\b)"
    r"[^.?!]{0,30}\b(?:boss|manager|colleague|coworker|co-worker|supervisor)\b",
    r"\b(?:held|pulled|pushed|shoved)\s+(?:me|us)\s+(?:against|to|back\s+against)\s+(?:the\s+)?"
    r"(?:wall|fence|barrier|side|back)\b[^.?!]{0,25}\b(?:to\s+let|so\s+they|so\s+the|"
    r"to\s+make\s+room|to\s+get\s+out\s+of\s+the\s+way)\b",
)
