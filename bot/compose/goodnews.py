import datetime
import re

from . import NEARLY, doubted
from .badnews import reads_as_someones_death

_MONTH = (r"(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|"
          r"aug(?:ust)?|sep(?:t|tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)")
_WEEKDAY = (r"(?:mon(?:day)?|tue(?:sday)?|wed(?:nesday)?|thu(?:rsday)?|fri(?:day)?|"
            r"sat(?:urday)?|sun(?:day)?)")
_A_DATE = (r"\s+(?:the\s+)?(?:early\s+|late\s+|mid-?)?"
           r"(?:\d|" + _MONTH + r"|" + _WEEKDAY + r"|christmas|easter|spring|summer|autumn|"
           r"winter|month|week|day|year|a week|a month|two weeks|three weeks)\b")
_DUE = r"\s+due\b"
_WHEN_DUE = r"\s+(?:in|on|next|by|at|early|late|mid)\b"
_WHO_DUE = (r"\b(?:i'm|im|i am|we're|we re|we are|she's|shes|she is|he's|hes|he is|they're|"
            r"theyre|they are)" + _DUE + _WHEN_DUE)
_PERSON_DUE = (r"\b(?:the|our|my)?\s*(?:baby|babies|twins?|wife|partner|girlfriend|fiancee?|"
               r"daughter|sister|brother|friend|surrogate)")

BABY = (
    re.compile(r"\b(?:had|have|has|have just had|had just had)\s+(?:her|his|the|a|our)\s+"
               r"(?:baby|little (?:girl|boy|one)|girl|boy)\b", re.I),
    re.compile(r"\b(?:baby|girl|boy|twins|daughter|son)\s+(?:was |were |is )?(?:born)\b", re.I),
    re.compile(r"\bgave birth\b", re.I),
    re.compile(r"\b(?:we|she|he|they)(?:'re| are|re)?\s+(?:now\s+)?(?:expecting|pregnant)\b", re.I),
    re.compile(r"\bexpecting\s+(?:a|our|twins)\b", re.I),
    re.compile(r"\b(?:it'?s|its)\s+(?:a\s+)?(?:little\s+)?(?:girl|boy|healthy|twins)\b", re.I),
    re.compile(r"^(?:so|well|and|ok|okay|ah|oh)?[\s,]*a\s+(?:little\s+)?"
               r"(?:girl|boy|twins|healthy\s+baby)\s*[.!]*$", re.I),
    re.compile(r"^(?:so|well|and|ok|okay|ah|oh)?[\s,]*a\s+(?:little\s+)?(?:girl|boy|twins)\b"
               r"[^.!?]{0,20}?\b\d+(?:\.\d+)?\s*(?:lb|lbs|pounds?|kg|kilos?|oz|ounces?)\b",
               re.I),
    re.compile(r"\b(?:the|our|my)\s+baby\s+(?:is|was|'s)\s+(?:a\s+)?(?:little\s+)?"
               r"(?:girl|boy|twins|healthy)\b", re.I),
    re.compile(r"\b(?:we|i|she|he|they|my\s+\w+|his\s+\w+|her\s+\w+|their\s+\w+)"
               r"(?:'re|re|\s+are|\s+am|\s+is)?\s+(?:now\s+)?having\s+"
               r"(?:a\s+|our\s+)?(?:little\s+)?(?:boy|girl|twins)\b"
               r"(?!\s+(?:over|round|to\s+stay|for\s+(?:dinner|lunch|tea|supper|christmas)))",
               re.I),
    re.compile(_WHO_DUE + _A_DATE, re.I),
    re.compile(_PERSON_DUE + r"(?:'s|s'|s)?\s+(?:is\s+|are\s+)?due\b" + _WHEN_DUE + _A_DATE,
               re.I),
    re.compile(r"\b(?:my|her|his|their|the)\s+due date\b"
               r"(?:\s+(?:is|was))?" + _WHEN_DUE + _A_DATE, re.I),
)

_A_CLASS = (r"(?:first|2[:. ]?1|2[:. ]?2|1st|2nd|upper\s+second|third|distinction|merit)")
_MY_OWN = r"\b(?:i|we)\b[^.!?]{0,30}?"
_A_COUNT = r"(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\s+"
_A_COURSE = (r"(?:degree|degrees|honours|graduat\w+|classification|results?|finals|dissertation|"
             r"thesis|course|uni|university|masters?|phd|doctorate|btec|diploma|hnd|"
             r"a\s+levels?|gcses?|qualification|exams?)")

PASSED = (
    re.compile(r"\bpassed\b(?:\s+\w+){0,3}?\s+(?:test|exams?|course|interview|boards?|"
               r"driving|theory|assessment|audition|viva|dissertation|grade|gcses?|a level|"
               r"finals|mocks?|check|inspection|audit|probation|review)\b", re.I),
    re.compile(r"\bpassed\s+(?:it\b(?!\s+(?:to|on|up|over|round|around|back)\b)|with\b|"
               r"first time|everything|all of)", re.I),
    re.compile(r"\b(?:i|we) (?:just |finally )?passed\b(?=$|[.!]| (?:now|today|yay|at last)\b)",
               re.I),
    re.compile(r"\bwe passed (?:the |an? )?\w+", re.I),
)

WIN = (
    re.compile(r"\bgot\s+(?:the|a|my|her|his|our|their)\s+(?:job|role|keys|offer)\b"
               r"(?!\s+(?:interview|application|centre|center))", re.I),
    re.compile(r"\bgot\s+into\b(?:\s+\w+){0,4}?\s+(?:uni|university|college|school|course|"
               r"team|squad|finals?|semis|shortlist|first choice|apprenticeship|placement|"
               r"nursing|med school|medical school|the show|the exhibition|the choir)\b", re.I),
    re.compile(r"\b(?:got|getting|had)\s+(?:a|the|my|her|his)\s+(?:promotion|pay rise|payrise|"
               r"raise|new job)\b", re.I),
    re.compile(r"\bpromoted\b", re.I),
    re.compile(r"\b(?:my|our|his|her|their)\s+(?:\w+\s+){0,2}?"
               r"(?:got|was|were|has\s+been|have\s+been|had\s+been|been)\s+"
               r"(?:approved|granted)\b", re.I),
    re.compile(r"\b(?:i|we)\s+(?:just\s+|finally\s+)?got\s+(?:\w+\s+){0,3}?"
               r"(?:approved|granted)\b", re.I),
    re.compile(r"\b(?:won|win|wins)\s+(?:\w+\s+){0,3}?(?:cup|medal|prize|award|race|match|"
               r"competition|league|final|round|gold|silver|bronze)\b", re.I),
    re.compile(r"\bcame\s+(?:first|top|second)\b", re.I),
    re.compile(r"\b(?:my|our|his|her|their)\s+(?:\w+\s+){0,2}?"
               r"(?:leave|holiday|time\s+off|visa|application|offer|mortgage|transfer|grant|"
               r"funding|booking|planning\s+permission|request)\b[^.!?]{0,24}"
               r"\b(?:got|was|were|is|been|just|now|finally)\s+(?:\w+\s+){0,2}?"
               r"(?:approved|accepted|granted|signed\s+off|came\s+through|went\s+through)\b",
               re.I),
    re.compile(r"\b(?:my|our|his|her|their)\s+(?:\w+\s+){0,2}?"
               r"(?:leave|visa|application|offer|mortgage|transfer|grant|funding|booking)\b"
               r"[^.!?]{0,24}\b(?:came\s+through|went\s+through|signed\s+off)\b", re.I),
    re.compile(r"\b(?:my|our|his|her|their)\s+(?:\w+\s+){0,2}?"
               r"(?:leave|visa|application|offer|mortgage|transfer|grant|funding|booking|"
               r"request|day\s+off|time\s+off)\s+"
               r"(?:(?:got|was|were|is|been|now|just|finally|all)\s+){0,2}"
               r"(?:approved|accepted|granted|signed\s+off)\b", re.I),
    re.compile(r"\bgraduated\b", re.I),
    re.compile(_MY_OWN + r"(?:got|gotten|achieved|came\s+away\s+with|graduated\s+with|"
               r"finished\s+with)\s+(?:a\s+|an\s+|my\s+|our\s+)?"
               + _A_CLASS + r"(?!\s+of\b)(?=[^.!?]{0,60}?\b" + _A_COURSE + r"\b)", re.I),
    re.compile(_MY_OWN + r"(?:got|gotten|achieved)\s+(?:a|an)\s+" + _A_CLASS +
               r"(?!\s+of\b)(?=\s*(?:[.!?]|$|,|\s+(?:in|for|overall|class)\b))", re.I),
    re.compile(_MY_OWN + r"(?:got|gotten|achieved|came\s+away\s+with|ended\s+up\s+with)\s+"
               r"(?:a\s+|an\s+|my\s+|our\s+|" + _A_COUNT + r")?"
               r"(?:a[\s*-]?stars?\b(?![\s-]*(?:wars|trek|gazer|"
               r"gazing|sign|bucks|fish|city|chart))|(?:all|straight)\s+(?:9s|8s)\b)", re.I),
    re.compile(r"\b(?:got|gotten|now)\s+engaged\b"
               r"|\b(?:i'm|im|i\s+am|we're|were|we\s+are|weve|we've|she's|shes|she\s+is|he's|"
               r"hes|he\s+is)\s+(?:now\s+|just\s+|finally\s+)?engaged\b"
               r"(?!\s+(?:in|on|with|to\s+(?:a|an|the|some)\s+\w))", re.I),
    re.compile(r"\b(?:he|she)\s+(?:only\s+|just\s+|finally\s+|only\s+went\s+and\s+)?"
               r"proposed\b(?=\s*(?:[.!]|,|$|\bto\s+me\b|\byesterday\b|\blast\b|\bat\b|"
               r"\bon\b|\band\b|\bso\b|\bnow\b|\btoday\b))", re.I),
    re.compile(r"\b(?:moving|moved|move)\s+in\s+together\b", re.I),
    re.compile(r"\b(?:had|got|have|having)\s+(?:an?\s+|our\s+|the\s+|my\s+|their\s+)?"
               r"offer\s+accepted\b"
               r"|\boffer\s+(?:got|was|is|has\s+been|have\s+been)\s+accepted\b", re.I),
    re.compile(r"\b(?:been|being|was|were|got)\s+(?:just\s+)?offered\s+(?:the|a|my|this)\s+"
               r"(?:job|role|position|place|post)\b", re.I),
    re.compile(r"\b(?:they|he|she|the\s+\w+)\s+offered\s+me\s+(?:the|a)\s+"
               r"(?:job|role|position|post)\b", re.I),
    re.compile(r"\bfinished\s+(?:my|the|our)\s+(?:degree|course|exams?|dissertation|thesis|"
               r"apprenticeship|training|masters?|phd|nursing|gcses?|a\s+levels?)\b", re.I),
    re.compile(r"\b(?:going|gonna)\s+to\s+be\s+(?:(?:a|an)\s+(?:grandma|grandmother|nan|nana|"
               r"granny|gran|grandad|grandfather|grandpa|auntie|aunty|uncle)\b|grandparents\b)",
               re.I),
    re.compile(r"\b(?:bought|got)\s+(?:a|our own|our first)\s+(?:house|flat|place)\b", re.I),
    re.compile(r"\b(?:got|signed)\s+the\s+keys\b|\bcompletion\s+(?:date|day)\b", re.I),
    re.compile(r"\b(?:all clear|got the all clear|out of hospital|rang the bell)\b", re.I),
    re.compile(r"\b(?:we're|we are|were|we've\s+started|we\s+have\s+started)\s+"
               r"(?:in\s+the\s+middle\s+of\s+)?adopting\b"
               r"(?![^.!?]*\b(?:policy|policies|approach|stance|attitude|method|tactic)\b)"
               r"|\b(?:the\s+)?adoption\s+(?:went\s+through|is\s+going\s+through)\b"
               r"|\b(?:started|starting|began)\s+(?:the|an|our)\s+adoption\b", re.I),
    re.compile(r"\b(?:came|come)\s+(?:in\s*to|into)\s+(?:some\s+|a\s+bit\s+of\s+|a\s+little\s+)?"
               r"(?:money|an\s+inheritance|cash)\b", re.I),
    re.compile(r"\b(?:my|our)\s+(?:book|novel)\s+"
               r"(?:got|was|is|has\s+been|have\s+been)\s+published\b", re.I),
)

_SAID = (r"(?:said|says|saying|told\s+me|tells\s+me|texted|texts|wrote|emailed|emails|"
         r"rang|phoned|reckons|thinks)")
_PRAISING = (r"(?:doing\s+(?:really\s+|very\s+)?well|done\s+(?:really\s+|very\s+)?well|"
             r"did\s+(?:really\s+|very\s+)?well|doing\s+(?:really\s+|very\s+)?great|"
             r"did\s+great|a\s+(?:really\s+|very\s+)?(?:good|great|smashing)\s+job|"
             r"(?:really\s+|very\s+)?(?:proud|pleased|impressed)\s+(?:of|with)\s+"
             r"(?:me|us|him|her|them)|well\s+done|star\s+of\s+the\s+week|"
             r"top\s+of\s+the\s+class)")
_AWARD = (r"(?:merit|gold\s+star|star\s+of\s+the\s+week|"
          r"head\s+teachers?\s+award|player\s+of\s+the\s+match)")
_I_PRAISED = re.compile(r"\b(?:i|we)\s+(?:said|say|says|told|tell|tells|texted|wrote|emailed)\b",
                        re.I)
PRAISED = (
    re.compile(r"\b" + _SAID + r"\b(?:\s+\w+){0,5}?\s+" + _PRAISING + r"\b", re.I),
    re.compile(r"\b(?:got|came\s+home\s+with|won|awarded)\s+(?:(?:a|an|the)\s+)?"
               + _AWARD + r"\b", re.I),
)

GOOD = BABY + PASSED + WIN + PRAISED

ARRIVED = (
    re.compile(r"\b(?:we|i)(?:\s+(?:just|finally|only))?\s+(?:got|gotten|adopted|rescued|"
               r"rehomed|picked up|bought|chose)\s+"
               r"(?:a|an|our|my|his|her|their|another|two|some|"
               r"one|a few|a couple|a pair|three|four|five|six)\s+"
               r"(?P<thing>[a-z][a-z' ]{1,30})", re.I),
    re.compile(r"\b(?:we|i)(?:'ve|ve)\s+(?:just|finally|only)\s+(?:got|gotten|adopted|"
               r"rescued|rehomed|picked up|bought|chose)\s+"
               r"(?:a|an|our|my|his|her|their|another|two|some|"
               r"one|a few|a couple|a pair|three|four|five|six)\s+"
               r"(?P<thing>[a-z][a-z' ]{1,30})", re.I),
    re.compile(r"\b(?:we|i)\s*(?:'re|re|are)?\s+(?:getting|having)\s+"
               r"(?:a|an|our|another)\s+(?P<thing>[a-z][a-z' ]{1,30}?)\s+"
               r"(?:put in|fitted|installed|done|built|delivered)\b", re.I),
)
HAVE_GOT = re.compile(r"\b(?P<who>we|i)(?:\s+(?:have|has|had)|'ve|ve)\s+got\b", re.I)
NEWS_OF_IT = re.compile(r"\b(?:new|brand[- ]new|another|just|finally|only|now)\b", re.I)

MOVED_IN = re.compile(r"\b(?:we|i)(?:'ve|ve)?\s+(?:just\s+|finally\s+|now\s+)?(?:moved|"
                      r"moving)\s+(?:house|flat|home|in|into)\b", re.I)

ANIMAL_THING = frozenset("""
    dog puppy pup cat kitten greyhound lurcher whippet terrier spaniel retriever labrador
    collie poodle rabbit bunny bunnies hamster gerbil guinea pig rat mice mouse horse pony
    donkey parrot budgie cockatiel bird chicken chickens hen hens duck ducks fish goldfish
    tortoise snake lizard ferret chinchilla koi
""".split())
HOME_WORK = frozenset("""
    kitchen bathroom extension loft garden shed decking conservatory roof windows drive
    driveway fence flooring tiles tiling wallpaper fireplace plastering rewiring insulation
""".split())
HOME_THING = HOME_WORK | frozenset("""
    boiler carpet carpets sofa bed fridge freezer oven cooker hob washer washing machine
    dishwasher door doors window
""".split())
OBJECT_THING = frozenset("""
    bike bicycle trike motorbike scooter car van caravan camper moped boat kayak canoe
    phone iphone mobile tablet ipad laptop computer pc desktop macbook monitor keyboard
    printer camera headphone headphones speaker speakers radio tv television kindle watch
    guitar piano violin drums ukulele keyboard sofa couch armchair chair table desk bed
    mattress wardrobe cupboard drawers bookcase shelf shelves rug lamp light curtains
    blinds mirror picture painting fridge freezer kettle toaster microwave oven cooker hob
    dishwasher washer washing machine dryer vacuum hoover iron blender airfryer
    coat jacket dress skirt trousers jeans shirt dress suit shoes boots trainers sandals
    hat cap scarf gloves bag handbag rucksack suitcase pram pushchair buggy cot crib
    toy toys lego doll dolls console playstation xbox switch game games book books
    ring necklace bracelet earring tattoo plant plants tree seeds greenhouse pond
    mower lawnmower bbq barbecue grill tent sleeping bag
""".split())

NOT_AN_ARRIVAL = frozenset("""
    ticket fine bill bills letter letters cold cough bug virus parking quote estimate
    refund diagnosis invoice debt summons notice warning complaint infection
    job role promotion offer keys tenancy
""".split())
THING_STOPS = frozenset("""
    for from in on at with by to of last next this yesterday today tomorrow and but so because
    that which who when while if then than as about after before over under into onto
    fitted installed delivered built done put made changed fixed coming arriving called
    named
""".split())
FAULT = re.compile(r"\b(?:no|not|isnt|isn't|wont|won't|doesnt|doesn't|dont|don't|broken|"
                   r"leaking|leak|damaged|fault|faulty|problem|issues?|wrong|blocked|"
                   r"flooded|stuck|cracked|smell|smells|nightmare|hated|hates?|regret\w*|"
                   r"disappoint\w*|rip[- ]off|useless|rubbish|waste of|went wrong|fell apart|"
                   r"dead on arrival|crash\w*|dud|lemon)\b", re.I)
NEW_ANIMAL = (
    "A {thing} — how are they settling in?",
    "Lovely. What's the {thing} like so far?",
    "How's the {thing} getting on?",
)
NEW_HOME = (
    "A {thing} is a proper job — how far along is it?",
    "How's the {thing} coming along?",
    "Good news. What's the part of the {thing} you're dreading?",
)
NEW_PLACE = (
    "How's the new place?",
    "What's the best thing about the new place so far?",
    "How's it feeling, being somewhere new?",
)
NEW_THING = (
    "Tell me about the {thing} — what's it like?",
    "Nice. What made you go for the {thing}?",
    "How are you finding the {thing}?",
)


A_POINTER_IN_FRONT = re.compile(r"^of\s+(?:those|these|them|the|my|our|his|her|their)\s+", re.I)


def _bare(word):
    if len(word) > 3 and word.endswith("ies"):
        return word[:-3] + "y"
    if len(word) > 3 and word.endswith("es") and word[-3] in "sxz":
        return word[:-2]
    if len(word) > 3 and word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    return word


def _thing_words(match):
    kept = []
    said = A_POINTER_IN_FRONT.sub("", match.group("thing") or "")
    for word in said.split():
        bare = word.strip(".,!?;:\"'")
        if not bare or bare in THING_STOPS or bare in NOT_AN_ARRIVAL or len(kept) == 3:
            break
        kept.append(bare)
    return " ".join(kept)


def new_thing(clean):
    if not clean:
        return None
    if NOT_NEWS.search(clean) or BAD.search(clean) or FAULT.search(clean) \
            or doubted(clean):
        return None
    said = clean
    if HAVE_GOT.search(said) and NEWS_OF_IT.search(said):
        said = HAVE_GOT.sub(r"\g<who> got", said)
    if MOVED_IN.search(said):
        return {"kind": "place", "thing": ""}
    for pattern in ARRIVED:
        match = pattern.search(said)
        if not match:
            continue
        thing = _thing_words(match)
        if not thing or thing in ("new", "another", "first", "second"):
            continue
        words = set(thing.split())
        words |= {_bare(word) for word in words}
        if words & NOT_AN_ARRIVAL:
            continue
        if not (words & (ANIMAL_THING | HOME_THING | OBJECT_THING)):
            continue
        if words & ANIMAL_THING:
            return {"kind": "animal", "thing": thing}
        if words & HOME_WORK:
            return {"kind": "home", "thing": thing}
        if words & HOME_THING:
            return {"kind": "thing", "thing": thing}
        return {"kind": "thing", "thing": thing}
    return None


def new_thing_replies(arrived):
    kind = arrived.get("kind")
    thing = arrived.get("thing") or ""
    if kind == "place":
        return NEW_PLACE
    pool = {"animal": NEW_ANIMAL, "home": NEW_HOME}.get(kind, NEW_THING)
    return tuple(line.format(thing=thing) for line in pool)


ORDINAL_DAY = re.compile(
    r"\b(?:my|our)\s+(?:(?P<whose>[\w'-]+)\s+)?(?P<day>\d+(?:st|nd|rd|th))\b"
    r"(?:\s*,?\s*(?:is|was|are)?\s*(?:in|on|next|this|tomorrow|tonight|soon|coming|"
    r"at\s+the\s+end|early|late|this\s+weekend|the\s+weekend)\b|[\s.!]*$)", re.I)

OCCASION = (
    ("birthday", re.compile(r"\b(?:its|it's|it is)\s+(?:\d+(?:st|nd|rd|th)\s+)?birthday\b"
                            r"|\b(?:my|our)\s+(?:[\w'-]+\s+)?(?:\d+(?:st|nd|rd|th)\s+)?"
                            r"birthday\b", re.I)),
    ("anniversary", re.compile(r"\b(?:its|it's|it is|my|our)\s+(?:\d+(?:st|nd|rd|th)\s+)?"
                               r"(?:\w+\s+)?anniversary\b", re.I)),
    ("wedding", re.compile(r"\b(?:im|i'm|i am|we're|we are|we re)\s+(?:getting\s+)?married\b"
                           r"|\b(?:my|our)\s+wedding\b", re.I)),
    ("wish", re.compile(r"^(?:a\s+|very\s+|so\s+|aw+\s+|oh\s+|many\s+)*"
                         r"(?:happy\s+(?:birthday|bday|b-day)|many\s+happy\s+returns)"
                         r"\s*[\s!.,]*$", re.I)),
)

NOT_AN_OCCASION = re.compile(
    r"\byou\b|\byour\b"
    r"|\bwould(?:'ve| have|ve)?\s+been\b"
    r"|\b(?:what|which|when|whens|when's|how|where)\b"
    r"|\b(?:present|presents|gift|gifts|idea|ideas|nothing|need|needs)\b"
    r"|\b(?:was|were)\b", re.I)

SOMEONE_LEFT = re.compile(
    r"\b(?:he|she|they)\s*(?:'s|'d|s|d)?\s+(?:has\s+|had\s+|just\s+|then\s+|already\s+)?"
    r"(?:left|leaves|leaving|walked\s+out|walking\s+out|moved\s+out|dumped|split\s+up)\b",
    re.I)

LET_DOWN = re.compile(r"\b(?:forgot|forgets|forgetting|forgotten|fell\s+apart|"
                      r"cancell?ed|ruined|messed|mucked|hate|"
                      r"wrong|disaster|horrible|"
                      r"nobody|no\s?body|no\s?one|none\s+of\s+them|"
                      r"annoyed|annoying|upset|arguing|argued|row|fight|fighting|didn't|didnt|"
                      r"did not|won't|wont|worried|worry|scared|terrified|dreading|stressed|"
                      r"anxious)\b", re.I)


RELATION_BEFORE_DAY = re.compile(
    r"\b(?:my|our)\s+(?:(?P<whose>[\w'-]+(?:\s+[\w'-]+)?)\s+)?"
    r"(?:\d+(?:st|nd|rd|th)\s+)?(?:birthday|anniversary)\b", re.I)
FAMILY = frozenset((
    "son", "daughter", "kid", "child", "baby", "twins", "girl", "boy", "lad", "teenager",
    "wife", "husband", "partner", "boyfriend", "girlfriend", "ex", "fiance", "fiancee",
    "mum", "mom", "mother", "dad", "father", "parent", "parents", "stepmum", "stepdad",
    "stepson", "stepdaughter", "sister", "brother", "sibling", "sisterinlaw", "brotherinlaw",
    "motherinlaw", "fatherinlaw", "aunt", "uncle", "cousin", "niece", "nephew", "grandchild",
    "gran", "granny", "nan", "nana", "grandma", "grandad", "grandpa", "grandparent",
    "friend", "mate", "boss", "colleague", "coworker", "neighbour", "neighbor", "flatmate",
    "housemate", "landlord", "carer", "client", "student", "teacher",
))


def _the_person_word(word):
    word = str(word or "").strip().strip("'").lower()
    if word.endswith("s"):
        word = word[:-1]
    return word


def someone_elses_occasion(clean):
    text = " ".join(str(clean or "").lower().split())
    for found in RELATION_BEFORE_DAY.finditer(text):
        words = (found.group("whose") or "").split()
        if any(_the_person_word(word) in FAMILY for word in words):
            return True
    for found in ORDINAL_DAY.finditer(text):
        if _the_person_word(found.group("whose") or "") in FAMILY:
            return True
    return False


def reads_as_an_occasion(clean):
    text = " ".join(str(clean or "").lower().split())
    if not text or "?" in text:
        return None
    if (NOT_AN_OCCASION.search(text) or LET_DOWN.search(text)
            or SOMEONE_LEFT.search(text)
            or doubted(text) or BAD.search(text)):
        return None
    for name, pattern in OCCASION:
        if pattern.search(text):
            return name
    if ORDINAL_DAY.search(text):
        return "birthday"
    return None

NOT_NEWS = re.compile(r"\b(?:did|do|does|will|would|are|is|was|were|can|could|shall|should|have|"
                      r"has)\s+(?:i|you|we|she|he|they)\b"
                      r"|\b(?:hope|hoping|wish|wishing|wonder|wondering|praying|"
                      r"fingers crossed|fingers are crossed)\b", re.I)
NOT_QUITE = re.compile(r"\b(?:" + "|".join(sorted(NEARLY)) + r")\b", re.I)

A_TURN_IN_THE_TALE = re.compile(
    r"\band\s+now\s+(?:every\w+|nobody|no\s+one|no-one|they|he|she)\b"
    r"|\band\s+[^.!?]{0,40}\b(?:hates?|hate\b|disapproves?|refuses?|won'?t|wont|"
    r"doesn'?t\s+(?:like|approve|want)|doesnt\s+(?:like|approve|want)|is\s+against|"
    r"objects?)\b", re.I)

A_SETBACK_AFTER_THE_WIN = re.compile(
    r"\band\s+(?:then\s+|now\s+)?[^.!?]{0,60}\b(?:broke|broken|breaks|packed\s+in|"
    r"stopped\s+working|gone\s+wrong|went\s+wrong|on\s+the\s+blink|is\s+a\s+(?:state|mess|tip)|"
    r"ruined|leaking|leaks?\b|flooded|cracked|worse|awful|terrible|horrible|nightmare|"
    r"regrets?|cant\s+afford|cant\s+cope|i\s+cant\s+do\b|just\s+my\s+luck|"
    r"died|dead)\b", re.I)


A_GOOD_ENDING = re.compile(
    r"\band\s+(?:now\s+|at\s+last\s+)?(?:we|i)\s+(?:can|could|get\s+to|are\s+able)\b"
    r"|\band\s+(?:now\s+)?(?:that\s+means\s+)?"r"(?:we|i)\s+can\b", re.I)

BAD = re.compile(r"\b(?:lost|miscarried|miscarriage|died|death|stillborn|failed|failing|"
                 r"not going|didn't|didnt|did not|haven't|havent|hasn't|hasnt|not yet|"
                 r"never|gave up|turned down|rejected|"
                 r"but|except|however|fight|fights|trouble|accident|argument|row|debt|"
                 r"hospital|intensive care|poorly|poorly|not well)\b", re.I)


A_GAP_WITHOUT_A_NO = (r"(?:(?!\b(?:not|no|never|hardly|barely|without|nothing|none)\b)"
                      r"[^.!?])")

RECOVERY = (
    re.compile(r"\b(?:feel|feeling|felt)\s+(?:a\s+(?:bit|lot|whole\s+lot)\s+|much\s+|so\s+much\s+|"
               r"loads\s+|really\s+|a\s+lot\s+)?better\b", re.I),
    re.compile(r"\b(?:im|i'm|i\s+am)\s+(?:much\s+|a\s+lot\s+|so\s+much\s+|loads\s+)?better\b"
               r"(?!\s+at\b)", re.I),
    re.compile(r"\b(?:pain|headache|migraine|cough|cold|sickness|nausea|rash|swelling|soreness|"
               r"knee|back|shoulder|ankle|wrist|hip|neck|throat|stomach|ear|tooth|chest)\b"
               + A_GAP_WITHOUT_A_NO + r"{0,8}?\b(?:is|are|feels?)\s+(?:much\s+|a\s+lot\s+|"
               r"so\s+much\s+|loads\s+)?better\b", re.I),
    re.compile(r"\bbetter\s+than\s+(?:yesterday|this\s+morning|last\s+(?:night|week|month)|"
               r"before|earlier|it\s+was|i\s+was)\b", re.I),
    re.compile(r"\b(?:pain|headache|migraine|cough|cold|sickness|nausea|temperature|fever|rash|"
               r"swelling|soreness|ache)\b" + A_GAP_WITHOUT_A_NO + r"{0,12}?"
               r"\b(?:has|have|is|are)?\s*(?:all\s+)?"
               r"(?:gone|eased|easing|cleared\s+up|stopped|settled)\b(?!\s+(?:on|to|into|in|down|"
               r"through|round|around|for|up))\b", re.I),
    re.compile(r"\b(?:(?:over|past|through)\s+the\s+worst|on\s+the\s+mend|back\s+on\s+my\s+"
               r"feet|back\s+to\s+normal)\b", re.I),
    re.compile(r"\b(?:i|we)(?:'m|m|\s+am|\s+are|'re)?\s+(?:finally\s+|just\s+|mostly\s+|"
               r"nearly\s+)?over\s+(?:the|my|that|this)\s+(?:flu|cold|cough|bug|virus|"
               r"infection|chest\s+infection|sickness|norovirus|migraine|sore\s+throat|"
               r"tonsillitis|bronchitis|pneumonia|stomach\s+bug|hangover)\b", re.I),
    re.compile(r"\b(?:got|get|getting)\s+over\s+(?:the|my|that|this)\s+(?:flu|cold|cough|"
               r"bug|virus|infection|sickness|norovirus|migraine|sore\s+throat|tonsillitis|"
               r"bronchitis|pneumonia|stomach\s+bug|hangover)\b", re.I),
    re.compile(r"\b(?:it|that|this|my\s+\w+|the\s+\w+|the\s+\w+\s+\w+|wound|cut|burn|"
               r"scar|sore)\s+(?:has|have|is|are|'s|s)?\s*(?:all\s+)?healed\b", re.I),
)

ABOUT_THEM = re.compile(r"^(?:so|well|ok|okay|and|but|tbh|honestly|ah|oh|right|good)?[\s,]*"
                        r"(?:i|im|i'm|ive|i've|we|we're|weve|we've|my|the|feeling|feel|over|"
                        r"on|back|still)\b", re.I)

CONDITIONAL = re.compile(r"\bbetter\b[^.!?]{0,24}?\b(?:when|whenever|if|unless|as\s+long\s+as)\b",
                         re.I)
PASS_PARTICLE = frozenset(("on", "up", "over", "away", "round", "around", "out", "by",
                           "through", "for", "to"))
PASS_TAKEN = frozenset(("salt", "ball", "butter", "plate", "bottle", "note", "message", "book",
                        "pen", "phone", "remote", "keys", "sugar", "jug", "envelope"))


def _a_hand_over(words):
    for i, word in enumerate(words):
        if word not in ("passed", "pass"):
            continue
        after = words[i + 1:i + 4]
        if not after:
            continue
        if after[0] in PASS_PARTICLE:
            return True
        thing = after[1] if after[0] in ("the", "a", "an") and len(after) > 1 else after[0]
        if thing in PASS_TAKEN:
            return True
        if after[0] == "it" and len(after) > 1 and after[1] in PASS_PARTICLE:
            return True
    return False


def reads_as_a_pass(clean):
    if not clean:
        return False
    if NOT_NEWS.search(clean) or NOT_QUITE.search(clean) or doubted(clean):
        return False
    if reads_as_a_win_nobody_noticed(clean):
        return False
    words = [w.strip(".,!?;:\"'") for w in clean.split()]
    if _a_hand_over(words):
        return False
    return any(pattern.search(clean) for pattern in PASSED)


NEWS_ASK = re.compile(
    r"^(?:(?:so|ok|okay|well|and|but|oh|right|hi|hey|hello|morning|now|then)\s*,?\s+)*"
    r"(?:got|get|any|anything|whats|what's|what\s+is|what\s+about|how\s+about|"
    r"do\s+you\s+have|have\s+you\s+got|have\s+you|has|have|did|you|u|is\s+there|are\s+there|"
    r"tell\s+me|give\s+me|hear\s+any|heard\s+any|share|spill)\b", re.I)
NEWS_WORD = re.compile(r"\b(?:news|anything|something)\b", re.I)
WORLD_NEWS = re.compile(
    r"\b(?:the|todays|today's)\s+(?:(?:latest|current|world|local|national|main|evening|"
    r"morning|morning's)\s+)?news\b|\bnews\s+today\b|\bheadlines?\b|"
    r"\bcurrent events\b|\bwhat happened in the\b", re.I)
_STANDIN = re.compile(
    r"\b(?:anything|something)\s+(?:good|nice|great|happy|brilliant|lovely|exciting)\b"
    r"(?:\s+(?:has\s+|have\s+)?(?:happen|happened|happens|happening|been\s+happening))?"
    r"(?:\s+(?:today|lately|recently|this\s+week|this\s+weekend|at\s+work|with\s+you|"
    r"for\s+you))*\s*$"
    r"|\b(?:anything|something)\s+(?:happen|happened|happens|happening)\b"
    r"(?:\s+(?:today|lately|recently|this\s+week|this\s+morning|at\s+work|at\s+school|then|"
    r"so\s+far|with\s+you))*\s*$", re.I)
NEWS_FRAME = frozenset("""got get any anything whats what's what is about how do you u have it
    there tell give us hear heard share spill some good nice happy great brilliant amazing
    wonderful excellent fantastic news today lately now then so well and but ok okay oh hi hey
    hello morning hows how's been new happen happened happening anything the a an i we me my
    week weekend day on going with for at""".split())


HANDED_OVER = re.compile(r"\bfor\s+(?:you|u|ya|you\s+two|us\s+all)\b|\b(?:to|i'?ll)\s+tell\s+you\b")


NEWS_IDIOM = re.compile(
    r"^(?:(?:so|ok|okay|well|and|but|oh|right|hi|hey|hello|morning|now|then)\s*,?\s+)*"
    r"(?:whats|what's|what\s+is|what\s+was|tell\s+me|give\s+me|spill)\s+"
    r"(?:(?:the|any|all\s+the)\s+)?"
    r"(?:script|crack|craic|story|latest|word|buzz|goss|gossip|happening|occurring|"
    r"been\s+happening)\b", re.I)
NEWS_IDIOM_TAIL = frozenset("""then now today lately mate pal folks everyone guys all so
    far at the moment please thanks""".split())


def _an_idiom_standing_alone(low, end):
    tail = [w.strip(".,!?;:\"'") for w in low[end:].split()]
    return all(w in NEWS_IDIOM_TAIL for w in tail if w)


WHAT_HAPPENED_ASK = re.compile(
    r"^(?:(?:so|ok|okay|well|and|but|oh|right|hi|hey|hello|morning|now|then)\s*,?\s+)*"
    r"what(?:'s|s|\s+has|\s+have)?\s+happened"
    r"(?:\s+(?:today|lately|recently|this\s+week|this\s+morning|tonight|then|so\s+far|"
    r"at\s+work|at\s+school|in\s+your\s+day|with\s+you))*\s*$", re.I)


def asks_for_news(clean):
    if not clean:
        return False
    low = clean.strip().rstrip("?!.").lower()
    idiom = NEWS_IDIOM.match(low)
    if idiom and _an_idiom_standing_alone(low, idiom.end()):
        return not HANDED_OVER.search(low)
    if WHAT_HAPPENED_ASK.match(low):
        return True
    if not (NEWS_ASK.match(low) and NEWS_WORD.search(low)):
        return False
    if "news" in low:
        if WORLD_NEWS.search(low):
            return False
    elif not _STANDIN.search(low):
        return False
    if HANDED_OVER.search(low):
        return False
    words = [word for word in (w.strip(".,!?;:\"'") for w in low.split()) if word]
    if all(word in NEWS_FRAME for word in words):
        return True
    return words[0] not in ("tell", "give", "share", "spill")


_AHEAD = re.compile(
    r"\b(?:in\s+(?:the\s+)?(?:\d+\s+)?(?:days?|weeks?|months?|years?|"
    r"spring|summer|autumn|winter|" + _MONTH + r")"
    r"|next\s+(?:week|month|year|spring|summer|autumn|winter|weekend|" + _WEEKDAY + r")"
    r"|on\s+" + _WEEKDAY +
    r"|starting\s+(?:on\s+)?" + _WEEKDAY +
    r"|tomorrow|tonight|this\s+(?:weekend|week|month|spring|summer|autumn|winter)"
    r"|soon|coming\s+up|later\s+(?:this|in)\b)", re.I)
_COUNTED_UP = re.compile(
    r"\b(?:turning|turns?|is|am|im|i'm|are|be|will\s+be|'ll\s+be)\s+\d{1,3}\b"
    r"(?!\s*(?:pounds?|quid|dollars?|euros?|grand|thousand|percent|%|hours?|minutes?|mins?|"
    r"miles?|kg|kilos?|litres?|liters?)\b)"
    r"(?!\s+a\s+(?:month|week|year|hour|day)\b)"
    r"(?!\s+per\s+\w+)", re.I)
_A_PERSON = re.compile(
    r"\b(?:i|im|i'm|me|we|us|she|he|they)\b"
    r"|\b(?:my|our|his|her|their|the|a)\s+(?:\w+\s+)?"
    r"(?:son|daughter|kid|child|baby|boy|girl|toddler|teen|teenager|nipper|youngster|unborn|"
    r"mum|mom|mother|dad|father|nan|nana|gran|granny|grandma|grandad|grandpa|grandmother|"
    r"grandfather|sister|brother|niece|nephew|cousin|aunt|auntie|uncle|twins?|"
    r"friend|mate|wife|husband|partner|girlfriend|boyfriend|fiance|fiancee|boss|colleague|"
    r"dog|puppy|pup|cat|kitten|rabbit|hamster|guinea\s+pig|horse|pony|pet)\b", re.I)
_AN_AGE_SAID = re.compile(
    r"\b(?:years?|yrs?)\s+old\b|\bage[sd]?\b|\bturning\b|\bturns?\b|\bbirthday\b|"
    r"\bbday\b|\bdue\b", re.I)


_COMING_UP = (
    re.compile(r"\b(?:getting|get)\s+(?:married|wed)\b|\b(?:our|the|my)\s+wedding\b"
               r"|\bset\s+(?:a|the)\s+date\b", re.I),
    re.compile(r"\b(?:having|expecting)\s+(?:a\s+|our\s+|twins?\b|a\s+little\b)", re.I),
    re.compile(r"\bbaby\s+(?:is\s+|'s\s+)?due\b"
               r"|\b(?:i'm|im|i am|we're|we are|she's|she is|hes|he is)\s+due\b", re.I),
    re.compile(r"\bstart(?:s|ing)?\s+(?:my\s+|a\s+|the\s+|our\s+)?(?:[\w-]+\s+){0,2}?"
               r"(?:job|role|course|college|uni|university|school|placement|apprenticeship|"
               r"training|shift|work)\b", re.I),
    re.compile(r"\b(?:new\s+)?(?:job|role|course|shift)\s+(?:starts|starting|begins|beginning)\b",
               re.I),
    re.compile(r"\bmov(?:e|ing)\s+(?:houses?|home|flats?|place|into|in|out|to|away|abroad|back)\b", re.I),
    _COUNTED_UP,
    re.compile(r"\bretir(?:e|es|ing)\b", re.I),
    re.compile(r"\b(?:half\s+)?marathon\b|\b10k\b|\btriathlon\b", re.I),
)
_SOON_ITSELF = re.compile(r"\bset\s+(?:a|the)\s+date\b|\b(?:having|expecting)\s+a\s+baby\b"
                          r"|\b(?:a|our|the|my)?\s*baby\s+(?:is\s+|'s\s+)?due\b", re.I)
_ALREADY = re.compile(r"\b(?:yesterday|last\s+(?:week|month|year|night|weekend)|"
                      r"a\s+few\s+(?:days|weeks)\s+ago|already|used\s+to)\b", re.I)
_DREAD = re.compile(r"\b(?:dread(?:ing|ed)?|not\s+looking\s+forward|worr(?:y|ied|ies|ying)|"
                    r"scared|terrified|nervous|anxious|panic(?:king)?|stress(?:ed|ful)?|"
                    r"afford|terrible|awful|hate|hopeless|no\s+idea\s+how|"
                    r"upset|angry|furious|livid|annoyed|not\s+speaking|not\s+talking|"
                    r"stopped\s+speaking|not\s+happy)\b", re.I)


_NOT_HAPPENING = re.compile(
    r"\b(?:not|never|no\s+longer|stopped|cancelled?|canceled?|called\s+off)\s+(?:\w+\s+){0,3}"
    r"(?:get(?:ting)?\s+(?:married|wed)|having|expecting|turning|turns?|mov(?:e|ing)|retir(?:e|es|ing))"
    r"\b", re.I)
_BARELY_ASKED = re.compile(
    r"^(?:is|are|am|was|were|do|does|did|have|has|had|can|could|would|should|shall|may|might"
    r"|what|when|where|who|why|how)\b", re.I)


_MONEY = re.compile(r"\b(?:rent|pay|wage|wages|salary|bill|bills|price|prices|cost|costs|"
                    r"deposit|savings?|income|mortgage|overdraft|loan|loans|debt|debts|"
                    r"arrears|fine|fines|invoice|quote|quotes|tax|council\s+tax)\b", re.I)
_CLAUSE_BREAK = re.compile(r"[,;]|\b(?:but|and|so|because|though|although)\b", re.I)


def _a_money_clause(clean):
    for clause in _CLAUSE_BREAK.split(clean or ""):
        if _MONEY.search(clause) and re.search(r"\d", clause):
            return True
    return False


_AHEAD_SPAN = re.compile(
    r"\bin\s+(?:the\s+)?(?:about\s+|around\s+|roughly\s+|nearly\s+|almost\s+|"
    r"just\s+over\s+|over\s+)?(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|"
    r"eleven|twelve|a\s+few|a\s+couple\s+of|a|an)?\s*"
    r"(?:hours?|days?|weeks?|fortnights?|months?|years?|"
    r"spring|summer|autumn|winter|" + _MONTH + r")\b", re.I)


_DONE_ALREADY = re.compile(
    r"\b(?:moved|have\s+moved|had\s+moved|comes\s+home|we\s+did\s+move)\b"
    r"|\b(?:yesterday|last\s+(?:week|month|year|weekend))\b|\balready\b", re.I)


def ahead_of_now(text):
    clean = " ".join(str(text or "").lower().split())
    if not clean or "?" in clean:
        return False
    if _DONE_ALREADY.search(clean):
        return False
    return bool(_AHEAD.search(clean) or _AHEAD_SPAN.search(clean))


def reads_as_news_to_come(clean):
    if not clean or "?" in clean:
        return False
    if (BAD.search(clean) or NOT_NEWS.search(clean) or NOT_QUITE.search(clean)
            or doubted(clean) or reads_as_someones_death(clean)):
        return False
    if _ALREADY.search(clean) or _DREAD.search(clean):
        return False
    if _NOT_HAPPENING.search(clean) or _BARELY_ASKED.search(clean):
        return False
    if not _AHEAD.search(clean) and not _SOON_ITSELF.search(clean):
        return False
    if not re.search(r"\b(?:i|we|my|our|im|i'm|we're|were)\b|\bthe\s+baby\b", clean):
        return False
    hits = [pattern for pattern in _COMING_UP if pattern.search(clean)]
    if not hits:
        return False
    if all(pattern is _COUNTED_UP for pattern in hits):
        if _a_money_clause(clean) or not _the_number_counts_a_life(clean, hits):
            return False
    return True


def _the_number_counts_a_life(clean, hits):
    if _AN_AGE_SAID.search(clean):
        return True
    for clause in _CLAUSE_BREAK.split(clean or ""):
        if _COUNTED_UP.search(clause) and _A_PERSON.search(clause):
            return True
    return False


_A_WIN = r"(?:won|win|winner|winnings|prize|prizes|jackpot|lottery|competition|sweepstake)"
_A_MEDIUM = (r"(?:text|texts|texted|message|messages|email|emails|letter|letters|call|phone call|"
             r"voicemail|whatsapp|dm|notification)")
_ENTERED_IT = re.compile(
    r"\b(?:i|we)\s+(?:entered|entered it|took part|did the|bought|played|signed up|applied)\b"
    r"|\bscratchcard\b|\braffle ticket\b|\bticket\b|\bmy number came up\b", re.I)
_A_MESSAGE_THAT_CLAIMS_A_WIN = re.compile(
    r"\b" + _A_MEDIUM + r"\b(?:(?!" + _A_WIN + r").){0,60}?\b" + _A_WIN + r"\b", re.I | re.S)
_A_WIN_THEN_A_MESSAGE = re.compile(
    r"\b" + _A_WIN + r"\b(?:(?!" + _A_MEDIUM + r").){0,60}?\b" + _A_MEDIUM + r"\b", re.I | re.S)
_ASKS_FOR_SOMETHING_BACK = re.compile(
    r"\b(?:fee|fees|pay|paid|send|transfer|wire|release|admin|processing|clearance|customs|"
    r"bank details|account details|card details|sort code|final notice|get in touch|"
    r"contact us|text them|text back|call them|ring them|reply|respond|confirm your)\b|£",
    re.I)
_NEVER_ENTERED = re.compile(
    r"\b(?:never|did\s*nt|did\s+not|do\s*nt|do\s+not)\s+(?:even\s+)?(?:enter|entered|"
    r"applied|signed up|took part)\b", re.I)


_ABOUT_THE_WIN = re.compile(
    r"\b(?:about|over)\s+it\b|\bto\s+(?:tell|let)\s+me\b|\bto\s+say\b|\bconfirming\b"
    r"|\bwell\s+done\b|\bcame\s+after\b|\bafterwards\b|\bthe\s+details\b"
    r"|\bcongratulat\w*\b|\bto\s+let\s+us\s+know\b", re.I)
_A_RELATIVE_TOLD_ME = re.compile(
    r"\b(?:(?:my|our)\s+)?(?:sister|brother|son|daughter|mum|mam|mother|dad|father|friend|mate|partner|"
    r"husband|wife|colleague|girlfriend|boyfriend|cousin|nan|gran|granny|aunt|uncle|niece|"
    r"nephew|neighbour|neighbor)\b.{0,40}?\b(?:texted|texts|messaged|messages|told|tells|"
    r"called|calls|rang|rings|phoned|phones|wrote|whatsapped|emailed|emails)\b.{0,20}?"
    r"\b(?:me|us)\b", re.I | re.S)


def reads_as_a_prize_in_a_message(clean):
    if not clean or _ENTERED_IT.search(clean):
        return False
    if _ABOUT_THE_WIN.search(clean) or _A_RELATIVE_TOLD_ME.search(clean):
        return False
    if _NEVER_ENTERED.search(clean):
        return True
    if _A_MESSAGE_THAT_CLAIMS_A_WIN.search(clean):
        return True
    return bool(_A_WIN_THEN_A_MESSAGE.search(clean) and _ASKS_FOR_SOMETHING_BACK.search(clean))


A_YEAR_AFTER = re.compile(r"\b(?:in|since|back\s+in|during|of|from)\s+((?:19|20)\d\d)\b", re.I)
JUST_HAPPENED = re.compile(
    r"\b(?:just|only\s+just|this\s+(?:week|month|year)|today|yesterday|last\s+(?:night|week)|"
    r"at\s+the\s+weekend|finally)\b", re.I)


def a_year_behind(text, today=None):
    when = today or datetime.date.today()
    for match in A_YEAR_AFTER.finditer(str(text or "")):
        try:
            if int(match.group(1)) < when.year:
                return True
        except (TypeError, ValueError):
            continue
    return False


YEARS_BACK_LINES = (
    "Good to hear. What made you think of it now?",
    "Nice one - what brings it up today?",
    "Good to hear. Is it something you still think about?",
)


SAYS_IT_IN_THE_PRESENT = re.compile(r"\b(?:im|i'm|i\s+am|we\s+are|we're)\b", re.I)


def reply_for_a_year_ago(text, reply, memory=None):
    if not (reads_as_a_congratulation(reply) or the_cheer_was_this_pool(memory)):
        return None
    return reply_for_a_win_from_a_past_year(text)


def reply_for_a_win_from_a_past_year(text):
    line = str(text or "")
    if not a_year_behind(line):
        return None
    if JUST_HAPPENED.search(line.lower()) or SAYS_IT_IN_THE_PRESENT.search(line):
        return None
    return YEARS_BACK_LINES[sum(map(ord, line.strip().lower())) % len(YEARS_BACK_LINES)]


def the_cheer_was_this_pool(memory):
    note = memory.get("said_kind") if isinstance(memory, dict) else None
    if not isinstance(note, dict) or note.get("kind") != "good_news":
        return False
    turns = memory.get("turns")
    return note.get("turn") == (len(turns) if isinstance(turns, list) else 0)


_A_CHEER = re.compile(
    r"^(?:congratulations|well\s+done|brilliant|lovely(?:\s+news)?|wonderful|fantastic|"
    r"that(?:'s|s)?\s+(?:great|lovely|wonderful|brilliant|fantastic|really\s+lovely)\b|"
    r"good\s+for\s+you|so\s+pleased|really\s+pleased|lovely\s+to\s+hear)", re.I)


def reads_as_a_congratulation(reply):
    said = " ".join(str(reply or "").split())
    return bool(_A_CHEER.match(said))


_AN_ATTEMPT = re.compile(
    r"\b(?:first|second|third|fourth|fifth|sixth|1st|2nd|3rd|4th|5th|6th|last)\s+"
    r"(?:time|go|try|attempt|sit)\b")
_A_NUMBER = r"(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten)"
_A_SCORE = re.compile(_A_NUMBER + r"\s*(?:-|to)\s*" + _A_NUMBER + r"|" + _A_NUMBER + r"\s*nil")
_OR_A_SCORE = re.compile(r"^\s*" + _A_NUMBER + r"\s*(?:-|to)?\s*(?:" + _A_NUMBER + r"|nil)\s*$")
_A_CLOCK_MINUTES = (r"(?:5|10|15|20|25|30|35|40|45|50|five|ten|quarter|fifteen|twenty|twenty[- ]five"
                    r"|thirty|thirty[- ]five|forty|forty[- ]five|fifty)")
_AN_HOUR = (r"(?:1|2|3|4|5|6|7|8|9|10|11|12|one|two|three|four|five|six|seven|eight|nine|ten"
            r"|eleven|twelve)")
_A_CLOCK = re.compile(r"^\s*" + _A_CLOCK_MINUTES + r"\s*(?:past|to)\s*" + _AN_HOUR + r"\s*$")
_A_WEIGHT = re.compile(r"\b\d+(?:\.\d+)?\s*(?:lb|lbs|pounds?|kg|kilos?|oz|ounces?)\b", re.I)
_AROUND_THE_FIGURES = frozenset("""
    a an the its it's hes shes he she they theyre were was is are both and so just about exactly
    weighing weighed weigh born baby twins boy girl little pound pounds lb lbs kg kilo kilos oz
    ounce ounces gram grams g of on in at with each apiece together
""".split())
_A_FIGURE_IN_THE_LINE = re.compile(
    r"\d+(?:\.\d+)?\s*(?:lb|lbs|pounds?|kg|kilos?|oz|ounces?|g|grams?)?", re.I)


def _only_the_arrivals_figures(said):
    for word in str(said or "").lower().replace("\u2019", "'").split():
        bare = word.strip(".,!;:\"'")
        if not bare or bare in _AROUND_THE_FIGURES:
            continue
        if _A_FIGURE_IN_THE_LINE.fullmatch(bare):
            continue
        return False
    return True
_ASKS_OR_THANKS = re.compile(
    r"\?|\b(?:what|how|why|when|where|who|which|can|could|should|would|will|shall|do|does|did|"
    r"is|are|was|were|thanks|thank|thx|ty|ta|cheers|bye|goodbye|night|please|sorry)\b")


MORE_OF_THE_NEWS = (
    "However many goes it took, you have it now.",
    "The win is the whole of it, not which go it was.",
    "{X} — the way to have it.",
)
MORE_OF_THE_NEWS_SCORE = (
    "{X} — better than a plain win.",
    "A score like that makes it a better story.",
    "Even better than it sounded.",
)
MORE_OF_THE_NEWS_ARRIVAL = (
    "{X} — lovely news. Really pleased for you.",
    "{X}. Really pleased for you.",
    "{X} — that is the best kind of news.",
)
_MORE_OF_THE_NEWS_MARKS = ("however many goes", "the win is the whole of it", "the way to have it",
                           "better than a plain win", "makes it a better story",
                           "even better than it sounded", "the best kind of news")


def reads_as_the_detail_line(reply):
    said = " ".join(str(reply or "").lower().replace("\u2019", "'").split())
    return any(mark in said for mark in _MORE_OF_THE_NEWS_MARKS)


def the_reply_just_cheered(memory):
    if not isinstance(memory, dict):
        return False
    note = memory.get("said_kind")
    turns = memory.get("turns")
    if not isinstance(note, dict) or note.get("kind") != "good_news":
        return False
    if not isinstance(turns, list) or not turns:
        return False
    last = turns[-1]
    if not isinstance(last, dict) or str(last.get("module") or "") != "chat":
        return False
    return note.get("turn") == len(turns) - 1


def a_detail_of_the_news(clean, memory=None):
    said = " ".join(str(clean or "").split())
    if not said or len(said.split()) > 6:
        return ""
    if (_A_WEIGHT.search(said) and "?" not in said and _only_the_arrivals_figures(said)
            and a_birth_just_announced(memory)):
        return "arrival"
    if memory is not None and not (the_cheer_was_this_pool(memory) or the_reply_just_cheered(memory)):
        return ""
    if _AN_ATTEMPT.search(said):
        return "attempt"
    if _OR_A_SCORE.match(said) and _A_SCORE.search(said) and not _A_CLOCK.match(said):
        return "score"
    return ""


def a_birth_just_announced(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    if not isinstance(turns, list):
        return False
    said = [str(one.get("user") or "") for one in turns[-2:] if isinstance(one, dict)]
    return any(any(pattern.search(line) for pattern in BABY) for line in said if line)


def reads_as_a_detail_of_the_news(clean, memory=None):
    if _ASKS_OR_THANKS.search(" ".join(str(clean or "").split())):
        return False
    return bool(a_detail_of_the_news(clean, memory))


def reads_as_good_news(clean):
    if reads_as_news_to_come(clean):
        return False
    if not clean:
        return False
    if (BAD.search(clean) or NOT_NEWS.search(clean) or NOT_QUITE.search(clean)
            or doubted(clean) or reads_as_someones_death(clean)):
        return False
    if asks_for_news(clean):
        return False
    if reads_as_a_win_nobody_noticed(clean):
        return False
    if reads_as_a_prize_in_a_message(clean):
        return False
    if A_TURN_IN_THE_TALE.search(clean) or A_SETBACK_AFTER_THE_WIN.search(clean):
        return False
    if _a_hand_over([w.strip(".,!?;:\"'") for w in clean.split()]):
        return False
    if _I_PRAISED.search(clean) and not any(
            pattern.search(clean) for pattern in BABY + PASSED + WIN):
        return False
    return any(pattern.search(clean) for pattern in GOOD)


NOBODY = (r"(?:nobody|no\s+one|no-one|not\s+(?:a\s+)?single\s+(?:one|person|soul)|"
          r"none\s+of\s+(?:them|us|my\s+\w+|the\s+\w+))")
_TOLD = (r"(?:said|says|saying|told\s+me|tells\s+me|congratulated|congratulates|noticed|notices|"
         r"mentioned|mentions|asked|asks|texted|texts|called|calls|rang|replied|replies|phoned|"
         r"wrote|written|thanked|thanks|clapped|acknowledged|commented|reached\s+out)")
NOBODY_SAID_ANYTHING = re.compile(
    r"(?P<first>\b" + NOBODY + r"\s+(?:even\s+|ever\s+|actually\s+|\w+\s+){0,2}?"
    r"(?P<verb>" + _TOLD + r")\b)"
    r"|(?P<object>\b" + _TOLD + r"\s+(?:me\s+)?nothing\b)"
    r"|\b(?:didnt|didn't|did\s+not|doesnt|doesn't|never|not)\s+(?:even\s+)?"
    r"(?:say|said|text|texted|call|called|ask|asked|notice|noticed|mention|mentioned|reply|replied|"
    r"congratulate|congratulated|thank|thanked|bother|bothered|ring|rang|write|wrote)\b",
    re.I)


CLAUSE = re.compile(r"[,;.!?]|\b(?:and|but|so|yet|cos|because|while|when|if|though|although|"
                    r"then|till|until)\b")
SPEAKER = frozenset(("i", "im", "ive", "id", "ill", "myself"))


def _the_speaker_is_the_quiet_one(text, match):
    words = [w.strip(".,!?;:\"'") for w in CLAUSE.split(text[:match.start()])[-1].split()[-4:]]
    return any(word in SPEAKER for word in words)


TAKES_A_CLAUSE = frozenset(("noticed", "notices", "noticing", "mentioned", "mentions",
                            "mentioning"))
SILENCE_WORDS = frozenset(("nothing", "anything", "a", "word", "well", "done", "congrats",
                           "congratulation", "congratulations", "nice", "hello", "hi", "hooray",
                           "bravo", "much", "all", "good", "luck", "me", "us", "her", "him",
                           "them", "everybody", "anybody", "anyone", "on", "for",
                           "about", "at", "with", "to", "either", "it", "that"))
CLAUSE_STOPS = frozenset(("and", "but", "so", "yet", "though", "although", "while", "which",
                          "when", "because", "cos", "then", "if"))


def _the_silence_is_the_whole_of_it(text, match):
    if match.group("object") is not None:
        return True
    verb = " ".join((match.group("verb") or "").split()[-1:])
    if verb in TAKES_A_CLAUSE:
        return True
    rest = re.split(r"[,.;!?]", text[match.end():], 1)[0]
    kept = []
    for word in rest.split():
        bare = word.strip(".,!?;:\"'")
        if bare in CLAUSE_STOPS:
            break
        kept.append(bare)
    return all(bare in SILENCE_WORDS for bare in kept)


def reads_as_a_win_a_cost_came_with(clean):
    text = " ".join(str(clean or "").lower().split())
    if not text or "?" in text:
        return False
    if NOT_NEWS.search(text) or NOT_QUITE.search(text) or doubted(text):
        return False
    if not any(pattern.search(text) for pattern in GOOD):
        return False
    if not (A_TURN_IN_THE_TALE.search(text) or A_SETBACK_AFTER_THE_WIN.search(text)):
        return False
    return not A_GOOD_ENDING.search(text)


def reads_as_a_win_nobody_noticed(clean):
    text = " ".join(str(clean or "").lower().split())
    if not text or "?" in text:
        return False
    if NOT_NEWS.search(text) or NOT_QUITE.search(text) or doubted(text):
        return False
    if not any(pattern.search(text) for pattern in GOOD):
        return False
    for match in NOBODY_SAID_ANYTHING.finditer(text):
        if _the_speaker_is_the_quiet_one(text, match):
            continue
        if _the_silence_is_the_whole_of_it(text, match):
            return True
    return False


NEGATED = re.compile(r"\b(?:dont|don't|doesnt|doesn't|didnt|didn't|did\s+not|do\s+not|"
                     r"isnt|isn't|wasnt|wasn't|not|never|no\s+longer|no)\s+"
                     r"(?:(?:really|very|much|so|still|any|getting|feel|feels|feeling|felt|"
                     r"seem|seems|be|is|was|am|a|bit|lot|longer)\s+){0,3}better\b", re.I)


DENIED = re.compile(r"(?:\bnot\b|\bnever\b|\bno\s+(?:better|good|improvement)\b|\bstill\b|"
                    r"\bn't\b|\bain'?t\b|\b(?:do|does|did|is|are|was|were|has|have|had|could|"
                    r"would|should)n'?t\b|\bworse\b)", re.I)


def _denied(text, start, end=None):
    return bool(DENIED.search(text[max(0, start - 26):(end if end is not None else start)]))


def reads_as_recovery(clean):
    text = " ".join(str(clean or "").lower().split())
    if not text or "?" in text:
        return False
    if not ABOUT_THEM.search(text):
        return False
    if BAD.search(text) or NOT_NEWS.search(text):
        return False
    if CONDITIONAL.search(text):
        return False
    if NEGATED.search(text):
        return False
    return any(pattern.search(text) for pattern in RECOVERY)


SETTLED = (
    re.compile(r"\b(?:is|are|seems?|looks?|feels?)\s+(?:ok|okay|alright|fine|clear|normal)\s+"
               r"(?:now|again)\b", re.I),
    re.compile(r"\b(?:ok|okay|alright|fine)\s+now\b", re.I),
    re.compile(r"\b(?:(?:she|he|it|they)(?:'s|s)?\s+(?:is|are|was|were)?|(?:is|are|seems?|"
               r"looks?))\s*(?:much\s+|a\s+lot\s+|so\s+much\s+|loads\s+)?better\s+"
               r"(?:now|today|again|thanks)\b", re.I),
    re.compile(r"\b(?:has|have|had)\s+(?:gone|eased|cleared(?:\s+up)?|settled(?:\s+down)?|"
               r"stopped|come\s+down)\b", re.I),
    re.compile(r"\b(?:went|goes)\s+(?:away|down)\b", re.I),
    re.compile(r"\b(?:gone|eased\s+off|cleared\s+up|settled\s+down|died\s+down)\s+"
               r"(?:now|again|overnight|since)\b", re.I),
    re.compile(r"\b(?:gone|come|went)\s+(?:down|away|off)\b", re.I),
    re.compile(r"\b(?:eased|calmed|settled|cleared)\s+(?:off|down|up)\b", re.I),
    re.compile(r"\b(?:results?|tests?|scans?)\s+(?:came|come|are|is|were)\s+(?:back\s+)?"
               r"(?:clear|fine|normal|ok|okay|all\s+clear)\b", re.I),
    re.compile(r"\b(?:it|they)\s+came\s+back\s+(?:clear|fine|normal|ok|okay)\b", re.I),
    re.compile(r"\bit'?s\s+(?:all\s+)?gone\b", re.I),
    re.compile(r"\b(?:she|he|they)(?:'s|s)?\s+(?:over\s+(?:it|the\s+worst)|back\s+to\s+"
               r"(?:herself|himself|themselves|normal))\b", re.I),
    re.compile(r"\b(?:she|he|they)(?:'s|s|\s+is|\s+are)?\s+out\s+(?:now|today|again)\b", re.I),
    re.compile(r"\b(?:all\s+clear|out\s+of\s+(?:hospital|the\s+woods)|back\s+to\s+normal|"
               r"back\s+on\s+(?:his|her|their)\s+feet|over\s+the\s+worst)\b", re.I),
    re.compile(r"\b(?:has|have|had|is|are|was|were|s|'s)\s+(?:all\s+|now\s+|finally\s+)?"
               r"healed\b", re.I),
    re.compile(r"\bhealed\s+(?:up|over|now|nicely|well)\b", re.I),
    re.compile(r"\b(?:it|that|this|it's|its|thats|that's|the\s+\w+)\s*(?:'s|s|\s+is|\s+has|"
               r"\s+have)?\s*stopped\s+(?:now|again|completely|properly|finally)\b", re.I),
    re.compile(r"\bnothing\s+(?:hurts|aches|is\s+sore|\w+\s+hurts)\s+"
               r"(?:now|any\s?more|today|at\s+all)\b", re.I),
)


WORRY_WORDS = frozenset("""
sick ill poorly unwell fever temperature cough cold flu covid chest throat tummy stomach
headache migraine pain ache aches sore hurting swollen swelling rash lump dizzy faint
vomit vomiting sick diarrhoea infection antibiotics hospital a&e operation surgery scan
xray x-ray test results test radiography chemo chemotherapy treatment dose medicine
allergy allergic asthma inhaler epilepsy seizure seizure fit fits bleed bleeding
virus bug tonsils ear ears tooth teeth back knee hip ankle wrist shoulder neck leg arm
temperature poorly worried scared nervous accident fall fell collapsed plaster cast
burnt burn burns scald scalded cut cuts wound wounds blood bled bleeding nosebleed nosebleeds
blister blisters sting stung bite bitten bruise bruised sprain sprained splint fracture
broken finger fingers thumb hand hands foot feet toe toes eye eyes gum gums toothache
dressing bandage stitches stitch plastering
""".split())


def worry_on_the_table(memory, look_back=4):
    turns = [t for t in ((memory or {}).get("turns") or []) if isinstance(t, dict)]
    seen = 0
    for turn in reversed(turns):
        said = " ".join(str(turn.get("user") or "").lower().split())
        if not said:
            continue
        if set(re.findall(r"[a-z']+", said)) & WORRY_WORDS:
            return True
        seen += 1
        if seen >= look_back:
            break
    return False


ASK_OPEN = re.compile(r"^(?:so|well|ok|okay|and|but|ah|oh|right|and)?[\s,]*(?:is|are|was|were|"
                      r"do|does|did|has|have|will|would|can|could|should|any)\b", re.I)


BARE_GONE = re.compile(r"\b(?:gone|went)\b(?!\s*(?:down|away|off|all))", re.I)
BODY_GAVE_WAY = re.compile(
    r"\b(?:my|his|her|their|your|the)\s+(?:\w+\s+)?(?:back|knee|knees|leg|legs|arm|arms|"
    r"shoulder|shoulders|hip|hips|ankle|ankles|wrist|wrists|neck|foot|feet|hand|hands|"
    r"elbow|elbows|jaw|stomach|tummy|chest|side)\b"
    r"(?!\s*(?:pain|ache|aches|hurt|hurts|trouble|problem|injury|stiffness|muscle))", re.I)


def the_tail_adds_nothing(text, end):
    tail = re.sub(r"[,;:!?]", " ", str(text or "")[end:]).strip()
    return not tail or bool(SETTLED_TAIL.match(" " + tail))


def _a_bare_gone_is_not_the_news(text, match):
    if not BARE_GONE.search(match.group(0)):
        return True
    if re.search(r"\bgone\s+again\b", text, re.I):
        return False
    if BODY_GAVE_WAY.search(text):
        return False
    return the_tail_adds_nothing(text, match.end())


SETTLED_TAIL = re.compile(r"\s*(?:(?:now|again|today|tonight|thanks|completely|properly|finally|"
                          r"at\s+last|anyway|so\s+far|for\s+good|down|off|"
                          r"this\s+week|this\s+morning|this\s+afternoon|this\s+evening|"
                          r"these\s+days|the\s+last\s+few\s+days|a\s+few\s+days|"
                          r"recently|lately|nowadays|for\s+now|for\s+a\s+while)\s*)*[.!]?$", re.I)


def the_news_is_the_whole_of_it(clean):
    text = " ".join(str(clean or "").lower().split())
    end = 0
    for pattern in RECOVERY + SETTLED:
        for match in pattern.finditer(text):
            end = max(end, match.end())
    return bool(end) and bool(SETTLED_TAIL.match(text[end:]))


CLEAR_RESULT = (
    re.compile(r"\b(?:in|out\s+of)\s+(?:full\s+)?remission\b", re.I),
    re.compile(r"\b(?:scan|scans|results?|tests?|biopsy|mri|ct|x-?ray|bloods?|screening|"
               r"checks?|check\s?up|swabs?)\b[^.!?]{0,24}?\b(?:came\s+back|come\s+back|"
               r"was|were|is|are|looks?|looked)\s+(?:all\s+)?(?:clear|normal|fine|negative)\b",
               re.I),
    re.compile(r"\b(?:biopsy|lump|mole|tumou?r|cyst|polyp|growth|cells?|cells)\b"
               r"[^.!?]{0,20}?\b(?:was|were|is|are|turned\s+out|come\s+back|came\s+back)\s+"
               r"(?:benign|harmless|nothing\s+to\s+worry\s+about)\b", re.I),
    re.compile(r"\b(?:hasnt|hasn't|hadnt|hadn't|has|had)\s+not\s+spread\b"
               r"|\bit\s+(?:hasnt|hasn't|hadnt|hadn't)\s+spread\b", re.I),
    re.compile(r"\bno\s+(?:sign|trace|evidence)\s+of\s+(?:it|any\s+cancer|the\s+cancer|"
               r"the\s+disease)\b", re.I),
    re.compile(r"\b(?:treatment|chemo|chemotherapy|radiotherapy|surgery|operation|transplant)\b"
               r"[^.!?]{0,24}?\b(?:is\s+working|worked|went\s+(?:well|fine)|was\s+a\s+success|"
               r"has\s+worked)\b", re.I),
    re.compile(r"\b(?:tumou?r|lump|cancer|growth)s?\b[^.!?]{0,16}?\b(?:has|have)\s+"
               r"(?:gone|shrunk|shrinking|stopped\s+growing)\b", re.I),
    re.compile(r"\b(?:its|it\s+is|it\s+was|hes|she's|theyre|they're)\s+(?:shrinking|"
               r"stopped\s+growing|gone)\b", re.I),
)

CLEAR_TAIL = re.compile(r"\s*(?:(?:now|again|today|thanks|thank\s+god|thankfully|thank\s+fully|"
                        r"finally|at\s+last|anyway|so\s+far|great|brilliant|"
                        r"so\s+(?:relieved|happy|pleased|glad)|relieved|what\s+a\s+relief)\s*)*"
                        r"[.!]?$", re.I)

NOT_CLEAR = re.compile(r"\b(?:not|isnt|isn't|wasnt|wasn't|arent|aren't|werent|weren't|never|"
                       r"no)\s+(?:\w+\s+){0,2}?(?:\w+\s+)?(?:clear|benign|remission|normal|"
                       r"negative|gone|harmless)\b"
                       r"|\b(?:has|had)\s+spread\b|\bhasnt\s+(?:worked|helped)\b"
                       r"|\bdidnt\s+work\b|\bnot\s+(?:worked|working)\b", re.I)


def reads_as_a_clear_result(clean):
    text = " ".join(str(clean or "").lower().split())
    if not text or "?" in text:
        return False
    if ASK_OPEN.search(text) or NOT_CLEAR.search(text) or NEGATED.search(text):
        return False
    if CONDITIONAL.search(text) or NOT_NEWS.search(text) or NOT_QUITE.search(text):
        return False
    for pattern in CLEAR_RESULT:
        for match in pattern.finditer(text):
            if CLEAR_TAIL.match(text[match.end():]):
                return True
    return False


def reads_as_settled(clean):
    text = " ".join(str(clean or "").lower().split())
    if not text or "?" in text:
        return False
    if ASK_OPEN.search(text):
        return False
    if CONDITIONAL.search(text):
        return False
    return any(match and not _denied(text, match.start(), match.end())
               and _a_bare_gone_is_not_the_news(text, match)
               for match in (pattern.search(text) for pattern in SETTLED))


if __name__ == "__main__":
    import sys
    for line in sys.argv[1:]:
        low = line.lower()
        print(f"{reads_as_good_news(low)!s:5} {reads_as_a_pass(low)!s:5} {line}")
