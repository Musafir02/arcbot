import re

from ..compose.repair import owns_the_deed
from .lookup import MACHINE_SOUNDS, entry, the_fault, SLIPS

NOISE_WORDS = ("noise", "noises", "noisy", "loud", "racket", "racketing", "din", "clatter",
               "clattering", "thunderous", "deafening", "row", "drone", "droning", "palaver")

_A_CHILD_NAMED = (
    "kid", "kids", "child", "children", "toddler", "toddlers", "baby", "son", "sons",
    "daughter", "daughters", "boy", "girl", "teen", "teens", "teenager", "teenagers",
    "stepson", "stepdaughter", "grandchild", "grandchildren", "grandson", "granddaughter",
    "year old", "year olds", "primary school", "secondary school", "nursery", "school age")
_ONLY_SAID_ABOUT_A_CHILD = ("screen time", "screentime")
_SOMEBODY_AT_HOME = (
    "my mum", "my mom", "my mother", "my dad", "my father", "my husband", "my wife",
    "my partner", "my girlfriend", "my boyfriend", "my stepson", "my stepdaughter",
    "my flatmate", "my housemate", "my room mate", "my roommate", "my friend", "my mate",
    "my brother", "my sister", "my nan", "my nana", "my gran", "my granny", "my grandma",
    "my grandad", "my grandpa", "my uncle", "my aunt", "my auntie", "my cousin", "my boss",
    "my colleague", "my staff")
_THEIR_SCREENS = re.compile(r"\b(?:his|her|their)\s+(?:phone|phones|screens?|tablet|ipad|ipads)\b")
_MY_OWN_SCREENS = re.compile(r"\b(?:my|the)\s+(?:phone|phones)\b|\bim\s+(?:always\s+)?on\b|"
                             r"\bi'm\s+(?:always\s+)?on\b")


def the_line_said(understood):
    reading = understood if isinstance(understood, dict) else {}
    said = " ".join(str(reading.get("clean") or reading.get("text") or "").split()).lower()
    return f" {said} " if said else ""


def _names_one_of(said, phrases):
    tokens = set(re.findall(r"[a-z']+", said))
    return any(phrase in said if " " in phrase else phrase in tokens for phrase in phrases)


def screens_are_a_childs(understood):
    said = the_line_said(understood)
    if not said.strip():
        return True
    if any(phrase in said for phrase in _ONLY_SAID_ABOUT_A_CHILD):
        return True
    return _names_one_of(said, _A_CHILD_NAMED)


def screens_are_somebody_elses(understood):
    said = the_line_said(understood)
    if not said.strip():
        return False
    if _MY_OWN_SCREENS.search(said):
        return False
    if screens_are_a_childs(understood):
        return False
    if _THEIR_SCREENS.search(said):
        return True
    return any(phrase + " " in said for phrase in _SOMEBODY_AT_HOME)


def _birthday_age(text):
    said = str(text or "").lower()
    found = re.search(r"\b(\d{1,3})(?:st|nd|rd|th)\b", said)
    if not found:
        found = re.search(r"(?:birthday|turning|turns|going on|hits?)\D{0,12}(\d{1,3})\b", said)
    if not found:
        found = re.search(r"\b(\d{2,3})\b\s*(?:next|this|in)\s*"
                          r"(?:week|month|year|weekend|june|july|august|september|october|november"
                          r"|december|january|february|march|april|may|christmas|summer|spring"
                          r"|autumn|winter|easter)\b", said)
    if not found:
        found = re.search(r"\b(\d{1,2})\s*(?:year|yr)s?[ -]?old\b", said)
    if not found:
        return None
    age = int(found.group(1))
    return age if 1 <= age <= 120 else None


def _ordinal(number):
    if number % 100 in (11, 12, 13):
        return "%dth" % number
    return "%d%s" % (number, {1: "st", 2: "nd", 3: "rd"}.get(number % 10, "th"))


_NO_FUSS = re.compile(
    r"\b(hates?|hated|doesnt|does not|doesn't|dont|don't|not|no|never|isnt|isn't)\b[^.?!]{0,30}"
    r"\b(fuss|attention|centre of attention|center of attention|spotlight|big deal|surprise|"
    r"surprises|party|to do|big do|a do|night out|speech|faff)\b"
    r"|\b(quiet|low key|low-key|private|small|low|no fuss)\b[^.?!]{0,16}"
    r"\b(birthday|do|party|meal|dinner|card|thing)\b")


def _names_an_age(words):
    return _birthday_age(words) is not None


_A_COLLEAGUE = re.compile(
    r"\b(?:colleagues?|co-?workers?|workmates?|boss|manager|staff|team|teacher|neighbou?r|"
    r"acquaintance|someone at work|people at work|the office)\b")
_A_CLOSE_ONE = re.compile(
    r"\b(?:nan|nana|gran|granny|grandma|grandmother|grandad|grandpa|grandfather|mum|mom|mam|"
    r"mother|dad|father|sister|brother|aunt|auntie|uncle|cousin|wife|husband|partner|"
    r"girlfriend|boyfriend|friends?|mates?|best mate|son|daughter|grandson|granddaughter)\b")


def _card_birthday(memory, reading):
    reading = reading if isinstance(reading, dict) else {}
    said = reading.get("clean") or reading.get("text") or ""
    age = _birthday_age(said)
    which = _ordinal(age) if age else "birthday"
    if _NO_FUSS.search(said):
        return ("Keep it plain and quiet, because that is the card a person who hates a fuss "
                "actually wants: \"Happy %s - no fuss, I'm just glad you're in my life.\" One "
                "true thing about them, no joke and no speech, and give the present quietly "
                "rather than in front of everyone." % which)
    if age and age < 13:
        example = ("\"Happy %s - the year you finally beat me at cards.\" One true thing they did "
                   "beats any joke, and for a small child the card is really for the parent: keep "
                   "it short and kind." % which)
    elif age and age < 18:
        example = ("\"Happy %s - still the best person to be stuck in a car with.\" One thing the "
                   "two of you actually do together beats any joke about the number, and a "
                   "teenager reads a short card: no advice, no speech, and the money is welcome."
                   % which)
    elif _A_COLLEAGUE.search(said):
        example = ("\"Happy %s - hope you get spoiled.\" With someone you do not know well the "
                   "warm plain line is the card itself: no in-joke, and put the money or gift "
                   "honestly (\"Have a drink on me\")." % which)
    elif _A_CLOSE_ONE.search(said):
        example = ("\"Happy %s - I still tell people about the night you drove us home at 3am.\" "
                   "They are close enough for the in-joke, so use the one only the two of you "
                   "would get." % which)
    else:
        example = ("\"Happy %s - I still tell people about the night you drove us home at 3am.\" "
                   "For a colleague or someone you do not know well, a warm plain line is enough "
                   "(\"Happy birthday - hope you get spoiled\"), and put the money or gift "
                   "honestly (\"Have a drink on me\")." % which)
    return ("Name one thing you like about them and skip the round-number joke: " + example)


def _card_plain(memory, reading):
    reading = reading if isinstance(reading, dict) else {}
    said = reading.get("clean") or reading.get("text") or ""
    if _NO_FUSS.search(said):
        return ("Keep it plain and quiet, because that is the card this person actually wants: "
                "\"Happy birthday - no fuss, I'm just glad you're in my life.\" One true thing "
                "about them, no joke and no speech, and give the present quietly rather than in "
                "front of everyone.")
    return ("Name one real thing about them and one wish, then stop - two lines is a card: "
            "\"Thinking of you both - hope the year is a good one.\" If you do not know them well, "
            "warm and plain beats clever, and sign it with your full name.")


_ASKS_FOR_THE_WORDS = re.compile(
    r"\b(?:what|how)\b[^.?!]{0,14}?\b(?:do|should|shall|can|could|would|will|might|to|am i)\b"
    r"[^.?!]{0,10}?\b(?:write|writing|say|saying|put|word|phrase|sign off)\b"
    r"[^.?!]{0,24}?\b(?:card|cards|note|notes|message|messages|letter|letters|inside|envelope)\b"
    r"|\b(?:card|cards|note|notes|message|messages|letter|letters)\b[^.?!]{0,24}?\b(?:what|how)\b"
    r"[^.?!]{0,12}?\b(?:write|say|put|word|phrase)\b")


def _asks_for_the_words(line):
    return bool(_ASKS_FOR_THE_WORDS.search(str(line or "").lower()))


ANSWERS = ("language-and-writing",)


SPELLINGS = (
    ("definitely", ("definately", "definatly", "definitley", "defintely"),
     "Definitely has **finite** inside it: de-finite-ly. Two i's, and no a anywhere."),
    ("separate", ("seperate", "seperately", "seperatly", "seperates"),
     "Separate has **a rat** in the middle: sep-a-rat-e. There is an a after the p, and another "
     "before the t."),
    ("tomorrow", ("tommorow", "tommorrow", "tomorow"),
     "Tomorrow has one m and two r's: to-m-o-rr-o-w. Say \"to morrow\", then close it up."),
    ("because", ("becuase", "becasue", "becouse"),
     "Because has **cause** in it: be-cause. If you can spell cause, you can spell because."),
    ("receive", ("recieve", "recieved", "recieving"),
     "Receive is i before e except after c: re-cei-ve. Recieve gets it the wrong way round, which "
     "is why it is the classic one."),
    ("believe", ("beleive", "belive", "beleiving"),
     "Believe is be-lie-ve: the **lie** is in the middle. Receive is the one that goes -ei-."),
    ("accommodation", ("accommodate", "accomodation", "acommodation", "acomodation",
                       "accomodate"),
     "Accommodation has two c's and two m's: a-cc-o-mm-odation, and accommodate keeps both."),
    ("necessary", ("neccessary", "necesary", "neccesary"),
     "Necessary has one c and two s's: picture a shirt with one **c**ollar and two **s**leeves. "
     "Necessarily and necessity keep the same shape."),
    ("calendar", ("calender",),
     "The thing with the months is calendar, with an a before the r. A calender is a machine that "
     "presses paper flat."),
    ("embarrass", ("embarass", "embarrassing", "embarasing"),
     "Embarrass has two r's and two s's: em-ba-rr-a-ss. Think \"bare arse\" and you will not "
     "forget it."),
    ("rhythm", ("rythm", "rythem", "rhythym"),
     "Rhythm is r-h-y-t-h-m and has no ordinary vowel of its own: \"rhythm helps your two hips "
     "move\" spells it."),
    ("weird", ("wierd", "wierdly"),
     "Weird breaks the rule: w-e-i-r-d, e before i. The line to remember is \"we are weird\"."),
    ("friend", ("freind", "freinds", "frend"),
     "Friend ends in **end**: fri-end. The e goes before the n, unlike most -ie- words."),
    ("beautiful", ("beutiful", "beautifull", "beatiful"),
     "Beautiful is beauty plus -ful: b-e-a-u-t-i-f-u-l. One t, one l."),
    ("business", ("buisness", "busines", "buisnesses"),
     "Business is busy-ness gone crooked: b-u-s-i-n-e-s-s."),
    ("beginning", ("begining", "beginnig"),
     "Beginning has two n's in the middle: be-gi-nn-ing. The stress is on the second syllable, so "
     "the n doubles."),
    ("occurred", ("occured", "occuring", "ocurred"),
     "Occurred has two c's and two r's: o-cc-u-rr-ed. Occur doubles both when it grows a tail."),
    ("until", ("untill", "untl"),
     "Until has one l. Till and until both exist, but the one-l until is the one people write."),
    ("address", ("adress", "adres", "addres"),
     "Address has two d's and two s's: a-dd-re-ss."),
    ("argument", ("arguement",),
     "Argument loses the e from argue: ar-gu-ment. Arguement has one letter too many."),
    ("forty", ("fourty",),
     "Forty has no u: four becomes forty by dropping it. Fourteen and fourth keep theirs."),
    ("probably", ("probly", "probally", "probaly"),
     "Probably is prob-ab-ly, all three syllables written even though we say two."),
    ("immediately", ("immediatly", "immediatley", "imediately"),
     "Immediately is im-medi-ate-ly: mediate is in the middle, so the a stays."),
    ("environment", ("enviroment", "enviornment"),
     "Environment has an n after the o: env-i-ron-ment, from environ, the surroundings."),
    ("government", ("goverment", "governement"),
     "Government has an n in the middle: govern-ment. It is govern with ment on the end."),
    ("surprise", ("suprise", "surprize", "surpise"),
     "Surprise starts sur-, from the French, not sup-. English uses s here, not z."),
    ("truly", ("truely", "truley"),
     "Truly drops the e from true: tru-ly. It is one of the few -ly words that loses it, with duly "
     "and wholly."),
    ("their", ("thier",),
     "Their is the belonging one: **their** house, like **her** house with a t. There is a place "
     "(it has here inside it), and they're means they are."),
    ("you're", ("youre", "your welcome", "your right", "your doing"),
     "You're means **you are**, so it keeps the apostrophe; your is belonging, as in your coat. If "
     "you can say \"you are\" in the sentence, it is you're."),
    ("lose", ("loose weight", "loosing"),
     "Lose has one o and rhymes with news; loose has two, rhymes with goose, and means not tight. "
     "\"Loose weight\" says the wrong word."),
    ("practice", ("practise or practice",),
     "In British English the noun is practice and the verb is practise: \"the practice\" but \"to "
     "practise\". American English uses practice for both."),
    ("congratulations", ("congradulations", "congratualtions", "congratuations"),
     "Congratulations has a t after the grat: con-grat-u-la-tions. Say \"gratitude\" to yourself "
     "and the t is there."),
    ("occasion", ("ocassion", "occassion", "ocasion"),
     "Occasion has two c's and one s: o-cc-a-s-ion. The double c is the one people drop."),
    ("across", ("accross", "acros"),
     "Across is one c and two s's: a-cross. The double c comes from hearing the join as a double "
     "sound."),
    ("quiet", ("quite or quiet", "quiett"),
     "Quiet, with the e last, is the opposite of noisy: q-u-i-e-t. Quite, with the e before the t, "
     "means fairly or completely - a quiet evening, but quite tired."),
)

THANKS_ANY = ("Name the thing they did, not the day in general: \"Thank you for the lemon cake and "
              "for staying to help with the chairs, it made the afternoon easy.\" One line about a "
              "specific detail beats a paragraph of adjectives, and send it the same day, because "
              "thanks the next morning reads as an afterthought.")
THANKS_FLOWERS = ("flower", "flowers", "bouquet", "bouquets", "orchid", "orchids")
THANKS_GIFT = ("present", "presents", "gift", "gifts", "voucher", "vouchers", "hamper")
THANKS_STAY = ("stay", "stays", "staying", "stayed", "host", "hosts", "hosted", "hosting",
               "put me up", "weekend", "weekends", "nights")
THANKS_MEAL = ("meal", "meals", "dinner", "lunch", "tea", "supper", "party", "barbecue",
               "bbq", "food", "cooked", "cook", "fed", "cake", "roast")
THANKS_WRITTEN = ("card", "cards", "letter", "letters", "note", "notes", "text", "texts",
                  "message", "messages", "email", "emails")
THANKS_LIFT = ("lift", "lifts", "drive", "drove", "driving", "picking up", "picked up",
               "dropping off", "dropped off", "run to", "airport", "station")
THANKS_FAVOUR = ("feeding", "fed", "watering", "watered", "looking after", "looked after",
                 "collecting the post", "collected the post", "cat", "dog", "plants", "post",
                 "bin", "house sitting", "housesitting")
THANKS_PERSON = ("teacher", "nurse", "carer", "midwife", "doctor", "neighbour", "neighbor",
                 "colleague", "boss", "manager", "childminder", "helped me", "helped us",
                 "who helped")


_MOVING_OUT = re.compile(r"\bmoving out\b|\bmoving (?:house|flat|home)\b|\bleaving home\b|"
                         r"\bmoved out\b|\bmoving in with\b", re.IGNORECASE)
_MOVING_AWAY = re.compile(r"\bmoving away\b|\bemigrat\w*\b|\bgoing travelling\b|"
                          r"\bmoving abroad\b|\bmoving to (?:australia|canada|spain|france|"
                          r"new zealand|america|the us|germany|ireland|scotland)", re.IGNORECASE)
_BABY = re.compile(r"\bpregnan\w*\b|\bexpecting a baby\b|\bbaby on the way\b|"
                   r"\bhaving a baby\b", re.IGNORECASE)
_SAID_IT_IS_NEWS = re.compile(r"\bnews\b|\bannounc\w*\b|\bbreak\s+(?:it|this|the)\b|"
                              r"\bbreak\s+bad\b", re.IGNORECASE)
_MONEY = re.compile(r"\bmoney\b|\bfinances?\b|\bdebts?\b|\bsalary\b|\bbills?\b|"
                    r"\bwages?\b", re.IGNORECASE)
_SHARED_HOUSE = re.compile(r"\b(?:housemate|flatmate|roommate|house ?mate)s?\b", re.IGNORECASE)
_HOUSEHOLD_MONEY = re.compile(r"\b(?:we|our|us|partner|husband|wife|spouse|bills?|rent|"
                              r"split|share|sharing|housemates?|flatmates?|roommates?|"
                              r"household|money with|finances)\b", re.IGNORECASE)
_PARENT_MONEY = re.compile(r"\b(?:my )?(?:parents?|mum|mom|mam|mother|dad|father|family|"
                            r"in ?laws?)\b", re.IGNORECASE)
_SHARE_MONEY = re.compile(r"\bpay\w*\b|\brent\b|\bbills?\b|\bshare\b|\bowe\w*\b|"
                          r"\bsplit\b|\bcouncil tax\b", re.IGNORECASE)
_MESS = re.compile(r"\bclean\w*\b|\bwashing up\b|\bwashing-up\b|\bdishes\b|\bmess\b|"
                   r"\btidy\w*\b|\bbins?\b|\bhoover\w*\b|\bload of washing\b", re.IGNORECASE)
_RAISE_MONEY = re.compile(r"\bmoney\b|\blent\b|\blend\w*\b|\bborrow\w*\b|\bowe\w*\b|"
                          r"\bdebt\w*\b|\bpay\w*\b|\bquid\b|£", re.IGNORECASE)
_RAISE_CAT_OUTSIDE = re.compile(r"\b(?:cat|cats|kitten|kittens)\b(?=[^.]*\bgarden\b)|"
                                r"\bgarden\b(?=[^.]*\b(?:cat|cats|kitten|kittens)\b)",
                                re.IGNORECASE)
_RAISE_CAT = re.compile(r"\b(?:cat|cats|kitten|kittens)\b", re.IGNORECASE)
_RAISE_ANIMAL = re.compile(r"\b(?:dog|dogs|puppy|pets?|animal|horse|rabbit|parrot)\b",
                           re.IGNORECASE)
_RAISE_CHILD = re.compile(r"\b(?:child|children|kid|kids|son|daughter|baby|toddler|niece|"
                          r"nephew|boys|girls)\b", re.IGNORECASE)
_RAISE_HOUSE = re.compile(r"\b(?:noise|noisy|music|loud|party|parking|garden|"
                          r"hedge|fence|bin|bins|rubbish|alarm)\b", re.IGNORECASE)
_RAISE_SMOKE = re.compile(r"\bsmok\w*|\bcigarette\w*|\bvap\w*|\bsmoking\b", re.IGNORECASE)
_RAISE_EXAMPLES = (
    (_RAISE_CAT_OUTSIDE, '"your cat keeps using my veg bed - could you keep her in at night?"'),
    (_RAISE_CAT, '"Mog swiped at Nell again on Saturday - could you keep her out of the room '
                 'while we are there?"'),
    (_RAISE_ANIMAL, '"Rex jumped up at Nell again on Saturday - could you keep him in the kitchen '
                    'while she is here?"'),
    (_RAISE_CHILD, '"the boys were a bit rough with Nell on Saturday - could you keep an eye when '
                   'they are in the garden?"'),
    (_RAISE_SMOKE, '"the smoke comes through the wall - could you smoke by the back door?"'),
    (_RAISE_HOUSE, '"the music was still going at half one - could we call it midnight next time?"'),
    (_RAISE_MONEY, '"I lent you £200 and I have been unsure how to bring it up"'),
)
_RAISE_PLAIN = '"I felt left out when the plans changed"'
_RAISE_ASK_SUBJECTS = (_RAISE_CAT_OUTSIDE, _RAISE_CAT, _RAISE_ANIMAL, _RAISE_CHILD,
                       _RAISE_SMOKE)


def _raise_example(line, patterns=None):
    for pattern, words in _RAISE_EXAMPLES:
        if patterns is not None and pattern not in patterns:
            continue
        if pattern.search(line):
            return words
    return None


_HURT_PART = (r"(?:back|arm|arms|leg|legs|knee|knees|ankle|ankles|shoulder|shoulders|wrist|wrists|"
              r"hand|hands|finger|fingers|thumb|toe|toes|foot|feet|hip|hips|head|neck|ribs?|rib|"
              r"shin|shins|calf|elbow|elbows|eye|jaw|collarbone|collarbones|spine)")
_SOMEONE_HURT_A_PART = re.compile(
    r"\bhurt\w*\s+(?:[a-z-]+\s+){0,2}(?:his|her|their|its)\s+(?:[a-z-]+\s+){0,2}"
    + _HURT_PART + r"\b"
    r"|\bhurt\w*\s+(?:my|his|her|their|your)\s+" + _HURT_PART + r"\b"
    r"|\bhurt\w*\s+(?:himself|herself|themselves|myself)\b",
    re.IGNORECASE)


def _not_a_hurt_body(understood):
    line = str((understood or {}).get("clean") or (understood or {}).get("text") or "")
    return _SOMEONE_HURT_A_PART.search(line) is None


def _raise_problem(memory, understood):
    line = str((understood or {}).get("clean") or (understood or {}).get("text") or "")
    example = _raise_example(line) or _RAISE_PLAIN
    return ("Say what happened, how it made you feel and what you want to change, once: "
            + example + ". One topic at a time, no list of past grievances, and ask for their side.")


_TALKS_OVER = re.compile(r"\b(?:talks?|talking|talk) over (?:me|my)\b|"
                         r"\bkeeps? (?:talking|interrupting|cutting)\b|"
                         r"\b(?:interrupts?|interrupting) (?:me|my)\b|"
                         r"\bcuts? me off\b|\bkeeps? cutting me off\b|"
                         r"\b(?:butts?|butting) in\b|\bfinishes? my sentences?\b|"
                         r"\btalks? over people\b", re.IGNORECASE)


def _saying_it(memory, understood):
    line = str((understood or {}).get("clean") or (understood or {}).get("text") or "")
    if _TALKS_OVER.search(line):
        return ("Say it once, plainly, and not in the moment it is happening: \"Can I finish this "
                "one? You jump in and I lose the thread.\" Name what they do rather than what they "
                "are - one line, no list of past times - and give them the benefit of the doubt "
                "once, because most people who talk over you are excited or nervous rather than "
                "rude. Then keep a short version for the moment itself, a hand up and \"hang on, "
                "let me finish this bit\", since that is the only place the habit can change. If "
                "it carries on after you have said it plainly, say it plainly a second time and "
                "say how it lands; that is not nagging, it is the second half of the same "
                "sentence.")
    if _MOVING_OUT.search(line):
        return ("Give them the plan, not a request for permission: \"I've found a flat and I'm "
                "moving out on the 14th - I wanted you to hear it from me first.\" Then let them "
                "react without defending it, and come back to the practical bits - how often you "
                "will visit, what you need - once the first conversation has cooled.")
    if _MOVING_AWAY.search(line):
        return ("Tell the people you will miss before the ones who will hear it second hand, and "
                "give them a date: \"I'm moving to Bristol in March - I didn't want you to find "
                "out from someone else.\" Then say what you want to keep going, a call every "
                "couple of weeks or a visit in the summer, so the news comes with a plan rather "
                "than a goodbye.")
    if _BABY.search(line):
        return ("Tell them in person or on a call rather than in a message, and lead with the news: "
                "\"I'm pregnant - it's early, and I wanted you to know.\" Then say what you want "
                "from them now, help or time before anyone else is told; that one sentence saves "
                "the guessing.")
    if _RAISE_SMOKE.search(line) or _RAISE_HOUSE.search(line):
        example = (_raise_example(line, _RAISE_ASK_SUBJECTS)
                   or '"the music was still going at half one - could we call it midnight next time?"')
        return ("Ask for the one thing, name when it happens and say what you want instead, once "
                "and in private: " + example + " Not the whole list and not in the moment it is "
                "annoying you, and leave them room to say why it is hard; a habit that is asked "
                "for plainly usually bends a little, where a rule handed down does not.")
    if _MESS.search(line):
        return ("Ask for the one job rather than the whole mess, and say when: \"Could you do the "
                "washing up tonight? I did it the last four nights and it is stacking up.\" Name "
                "the thing, the reason and the deadline in one breath - a general complaint about "
                "the flat gets an apology and no change.")
    if _SHARED_HOUSE.search(line) and (_MONEY.search(line) or _SHARE_MONEY.search(line)):
        return ("Ask once, with the amount and the date, and leave the history out of it: \"The "
                "broadband comes to 32 a month and your half is 16 - could you send it by "
                "Friday?\" A plain ask reads as fair; hinting over the washing up reads as a "
                "buildup.")
    if _PARENT_MONEY.search(line):
        return None
    if _MONEY.search(line) and _HOUSEHOLD_MONEY.search(line):
        return ("Pick a time that is not the moment a bill lands, and put the numbers side by side "
                "rather than asking for a verdict: what comes in, what goes out, and what each of "
                "you wants to be able to afford. Open with a question - \"how do you feel about "
                "the way we split things?\" - and leave one decision for next time.")
    if not _SAID_IT_IS_NEWS.search(line):
        return None
    return ("Say it in one flat sentence, then stop: the news, the reason if there is one, and what "
            "you want from them. The wait for the perfect moment is usually longer and worse than "
            "the conversation itself.")


def _thanks_has(understood, words):
    typed = {str(word).lower() for word in (understood.get("words") or ())}
    clean = (understood.get("clean") or understood.get("text") or "").lower()
    for word in words:
        if " " in word:
            if word in clean:
                return True
        elif word in typed:
            return True
    return False


def thanks_note(memory, understood):
    if _thanks_has(understood, THANKS_FLOWERS):
        return ("Say where the flowers are and what they have done for the room: \"Thank you for "
                "the flowers - they are on the kitchen table and the whole week looks better.\" "
                "Two or three lines, say when you will see them next, and stop.")
    if _thanks_has(understood, THANKS_GIFT):
        return ("Name the thing and what you are doing with it, rather than thanking them for it: "
                "\"Thank you for the cafetiere - it is on my desk and I use it every morning.\" "
                "Two or three lines, say when you will see them next, and stop; a present does not "
                "need a page.")
    if _thanks_has(understood, THANKS_STAY):
        return ("Pick the one thing they did that you noticed - the spare bed, the early start, the "
                "extra trip to the station - and say what it saved you: \"Thank you for having me "
                "for the weekend - the lift on Sunday saved me the whole morning.\" Then say when "
                "you will have them back, if you mean it.")
    if _thanks_has(understood, THANKS_MEAL):
        return ("Name the thing they did and what it changed for you, then stop: \"Thank you for "
                "the meal on Saturday - I came home full and happy.\" One detail from the evening "
                "that only you would know beats a paragraph of adjectives, and anything you are "
                "actually going to do, say when.")
    if _thanks_has(understood, THANKS_LIFT):
        return ("Name the trip and what it saved you: \"Thank you for the lift to the station on "
                "Friday - it saved me an hour and a soaking.\" Then one line about what it meant "
                "to you, and stop.")
    if _thanks_has(understood, THANKS_FAVOUR):
        return ("Name the job they did and what it saved you, then stop: \"Thank you for looking "
                "after the cat while we were away - coming back to a happy animal was the whole "
                "holiday.\" One line about what it meant to you beats a paragraph, and say what "
                "you will do in return if you mean it.")
    if _thanks_has(understood, THANKS_PERSON):
        return ("Say what they did and what it was worth to you: \"Thank you for the time you gave "
                "me over the summer - I still use the list you wrote.\" One sentence of detail, "
                "one of what it meant, then stop; people keep the short ones.")
    return THANKS_ANY


def _inflections(word):
    forms = {word}
    if " " not in word and len(word) > 3:
        forms.update({word + "ly", word + "s", word + "es", word + "ing", word + "ed"})
        if word.endswith("e"):
            forms.update({word[:-1] + "ing", word[:-1] + "ed", word[:-1] + "ly"})
    return forms


_SPELLING_WORDS = tuple(sorted({form for right, slips, _tip in SPELLINGS
                                for word in (right,) + slips
                                for form in (_inflections(word) if word == right else (word,))}))
_SPELLING_SLIPS = tuple(slip for _right, slips, _tip in SPELLINGS for slip in slips)


_SPELLING_ENTRY_IDS = ("spelling-tricky-word", "spelling-pick-one")
for _slip in _SPELLING_SLIPS:
    SLIPS.setdefault(_slip, set()).update(_SPELLING_ENTRY_IDS)


_SPELLING_TIPS = {form: tip for right, slips, tip in SPELLINGS
                  for word in (right,) + slips for form in _inflections(word)}


def _spelling(memory, understood):
    clean = (understood.get("clean") or "").lower()
    for word in clean.replace("?", " ").replace(",", " ").replace(":", " ").split():
        tip = _SPELLING_TIPS.get(word.strip("."))
        if tip:
            return tip
    for phrase, tip in _SPELLING_TIPS.items():
        if " " in phrase and phrase in clean:
            return tip
    return None


SAID = ("what did i say", "what did we say", "did i say", "did i tell", "you said",
        "i said", "own words", "i told you")
SAY = ("what do i say", "what should i say", "what to say", "say to", "say at")
MOURNING = ("died", "dies", "dying", "death", "dead", "passed away", "passed on", "loss",
            "lost my", "funeral", "burial", "cremation", "bereavement", "grief", "grieving",
            "condolence", "condolences", "sympathy", "widow", "terminal", "cancer")


ON_THE_PHONE = ("answerphone", "answer machine", "answering machine", "voicemail", "voice mail",
                "to leave a message", "leave a message on", "left a message on", "take a message",
                "took a message", "who should i leave", "can i leave a message", "missed call",
                "ring back", "call back",
                "on the phone", "by phone", "phone call", "phonecall", "him a message",
                "her a message", "them a message", "message on his", "message on her",
                "message on the")
_EULOGY_LENGTH = ("how long", "length", "words", "word count", "minutes", "too long", "short")
_EULOGY_START = ("how do i start", "how to start", "start", "opening", "open", "begin", "first line",
                 "example", "examples", "template", "give me", "ideas", "what do i say")


def _eulogy(memory, understood):
    clean = ((understood or {}).get("clean") or "").lower()
    has = lambda *wanted: any(shape in clean for shape in wanted)
    if has(*_EULOGY_LENGTH):
        return ("A eulogy runs about three to five minutes, so 500 to 750 words read slowly - time "
                "it out loud once, because reading to a room is slower than reading to yourself. "
                "Shorter and warm beats long and solemn: two minutes with one real story in it "
                "lands better than ten minutes of a life in order, and nobody has ever wished a "
                "eulogy had listed more jobs.")
    if has(*_EULOGY_START):
        return ("Start with a plain, specific fact about them, not a summary: \"Dad was born in "
                "Leeds and never once chose a different chippy.\" Then one story that only your "
                "family could tell, with a detail in it - what they said, what they were wearing, "
                "the thing they did with their hands. Close on what they gave you, in one sentence, "
                "and step back; the last line does not have to be poetry, it has to be theirs.")
    return ("Write it in four short parts: who they were in a sentence, one story with a real "
            "detail in it, one thing they gave you, and a last line to the room. Aim for 500 to 750 "
            "words - three to five minutes out loud - and read it from paper rather than memory. "
            "Say the funny thing if it was funny, because a laugh at a funeral is a relief and not "
            "a mistake, and put the plainest, truest sentence you have near the end where it will "
            "be heard.")



FOLLOW_UP_THANKS = ("Send a short thank-you the same day: \"Thank you for the conversation "
                      "today — I'm even keener on the role after hearing about the new system. "
                      "Happy to answer anything else.\"")
FOLLOW_UP_CHASE = ("Chase once, a week after you applied: two lines, say you are still interested "
                   "and one thing you would bring to the job, and ask if they need anything else "
                   "from you. Then leave it - ring only if the advert gave a date and it has "
                   "passed. Keep applying elsewhere in the meantime.")
INTERVIEW_WORDS = ("interview", "interviews", "interviewed", "panel", "met them", "met the team",
                   "after the interview", "thank you note", "thank-you", "thank you letter",
                   "spoke to them", "spoke to the manager")
CHASE_WORDS = ("chase", "chasing", "chased", "follow up", "following up", "follows up",
               "followed up", "follow-up", "heard",
               "heard back", "heard nothing", "no reply", "nothing back", "no answer", "waiting",
               "not heard", "still waiting", "when should i")


def _said(said, word):
    return re.search(r"\b" + re.escape(word) + r"\b", said) is not None


WHEN_WORDS = ("how long", "how many days", "how many day", "how many weeks", "how many week",
              "how soon", "how much longer", "when should i", "when do i", "days should i wait",
              "weeks should i wait", "how long should i wait",
              "should i wait", "should i leave it")
_TRADES = ("builder", "builders", "plumber", "plumbers", "electrician", "electricians",
           "roofer", "roofers", "decorator", "decorators", "painter", "painters",
           "plasterer", "plasterers", "tiler", "tilers", "joiner", "carpenter", "gardener",
           "landscaper", "handyman", "contractor", "tradesman", "tradesperson", "workman",
           "mechanic", "garage", "fitter", "installer")
FOLLOW_UP_ASK = ("how long", "how many days", "how many day", "how many weeks", "how many week",
                 "how soon", "how much longer", "when should i", "when do i", "when to",
                 "what is the right time", "what's the right time", "after a week", "a week after",
                 "left it a week", "leave it", "how many days before")
NOT_A_JOB = _TRADES + (
    "council", "landlord", "letting agent", "bank", "refund", "parcel", "delivery", "order",
    "insurance", "warranty", "broadband", "energy", "supplier", "dentist", "doctor", "surgery",
    "hospital", "school", "nursery", "vet", "garage", "neighbour",
    "complaint", "complaints", "complaining", "claim", "claims", "compensation")
FOLLOW_UP_AFTER_INTERVIEW = ("Give it a week after the interview: one short note that thanks them "
                             "for the time, gives one reason you want the job, and asks plainly "
                             "for a timescale. Then leave it - ring only if they gave you a date "
                             "that has passed.")
FOLLOW_UP_WHEN = ("Give it a week: a week from the day you sent it, or a week after the date "
                  "they gave you, long enough that they have news and short enough that you are "
                  "still live. Then one short message - what you are following up, when you sent "
                  "it, and a plain ask for a timescale - and after that leave it with them rather "
                  "than chase again.")


def _follow_up_general(memory, understood):
    return FOLLOW_UP_WHEN

EARLY_WORDS = ("leave early", "leaving early", "finish early", "finishing early",
               "an hour early", "half day", "early on friday", "early tomorrow", "go early",
               "leave at", "leaving at", "dip out", "knock off early", "leave a bit early",
               "leave work early", "out early")
TIME_OFF_SCRIPT = ("Ask early, name the dates and say who covers: \"Could I take 12–16 May off? "
                   "I've arranged cover with Priya and nothing is due that week.\" One question, "
                   "one answer, and put it in writing.")
EARLY_SCRIPT = ("Give the time and the cover, not the whole story: \"Hi Sam, is it OK if I leave "
                "at 3 today? I've moved the 4pm call to Priya and I'll pick the rest up in the "
                "morning.\" Ask the day before when you can, keep it to two lines, and if it is "
                "more than a one-off ask for a change of hours instead of asking again each week.")


TIME_OFF_SCRIPT_YES = ("Yes, if you ask early and name the dates: \"Could I take 12-16 May off? "
                       "I've arranged cover with Priya and nothing is due that week.\" One "
                       "question, one answer, and put it in writing.")
EARLY_SCRIPT_YES = ("Yes - give the time and who covers it rather than the whole story: \"Hi Sam, "
                    "is it OK if I leave early on Friday? I've moved the 4pm call to Priya and I'll "
                    "pick the rest up on Monday.\" Say it the day before if you can, and keep it "
                    "to two lines.")
YES_WORDS = ("can i", "can we", "could i", "may i", "am i allowed", "is it ok", "is it okay",
             "is it fine", "would it be ok", "would it be okay", "do you think i can",
             "should i ask")


_ALREADY_HAD = ("booked", "approved", "confirmed", "in the diary", "granted",
                "got the time off", "got the week off", "got my holiday", "have the time off")

_HAS_THE_TIME = ("taking next week off", "taking the week off", "off work next week",
                 "off next week", "next week off", "im off", "i'm off", "i am off",
                 "off work from", "off work for", "off next month", "off all week")
_AWAY_OR_HOME = ("go somewhere", "going somewhere", "go away", "going away", "get away",
                 "stay at home", "staying at home", "at home or away", "away or at home",
                 "somewhere warm", "a trip", "trip with")

_USE_THE_WEEK = ("no plans", "nothing planned", "how do i use", "how do i plan", "how to plan",
                 "how should i spend", "how do i spend", "use a week off", "use my week off",
                 "use the week off", "use the time off", "spend a week off", "spend my week off",
                 "spend the week off", "plan a week off", "plan my week off", "plan the week off",
                 "a week off well", "what to do with", "make the most of", "sort my",
                 "week off the booze", "week off booze", "week off the drink", "week off drink",
                 "week off wine", "week off alcohol", "week off the alcohol", "week off sugar",
                 "week off dairy", "week off meat", "week off caffeine", "week off takeaways",
                 "week off vaping", "week off smoking", "week off social media", "week off chocolate",
                 "week off crisps", "week off my phone", "week off the phone", "week off sweets",
                 "week off carbs", "week off bread", "week off cheese", "week off gluten",
                 )

_ASKING_FRAME = ("ask", "asking", "asked", "request", "requesting", "book", "booking", "booked",
                 "put in for", "entitled", "entitlement", "can i", "can we", "could i", "may i",
                 "am i allowed", "is it ok", "is it okay", "allowed to", "permission",
                 "want to take", "want to book", "want to request", "wanted to take",
                 "need to take", "need to book", "need to request", "hope to take", "planning to take",
                 "how do i", "how should i", "how would i", "how to get", "how to take",
                 "what do i say", "what should i say", "who do i ask", "how much notice",
                 "how many days", "take a day off", "take a week off", "take some time off",
                 "take time off", "take it off", "take the day off", "take the week off",
                 "need a", "need some", "need time", "need leave", "want some", "want a day off",
                 "want the day off", "want time off", "like a day off",
                 "like a week off", "like some time off", "id like", "i'd like", "would like a",
                 "get a day off", "get a week off", "get time off", "get the day off",
                 "annual leave", "leave request", "request leave", "book leave", "holiday form",
                 "leave form", "holiday request", "date of leave")

_MONTHS_NAMED = ("january", "february", "march", "april", "may", "june", "july", "august",
                 "september", "october", "november", "december", "next month", "this month",
                 "end of the month", "month")
_HOW_LONG = ("two weeks", "three weeks", "four weeks", "five weeks", "ten days", "a fortnight",
             "fortnight off", "week off in", "weeks off in")
_ASKS_TO_HAVE = ("can i", "can we", "could i", "may i", "am i allowed", "is it ok", "is it okay",
                 "want to", "need to", "wish to", "hope to", "planning to", "like to",
                 "ask", "asking", "request", "book", "take", "put in for", "claim",
                 "entitled", "how many days", "what do i say", "how do i get time off",
                 "need a", "need some", "need time", "need leave", "want a day off")

_ASK_VERBS = ("can i", "can we", "could i", "may i", "am i allowed", "is it ok", "is it okay",
              "how do i ask", "how do i take", "how do i book", "how do i request",
              "how do i get time off", "how do i go about", "how do you ask", "how to ask",
              "should i ask", "want to", "need to", "need a", "ask",
              "asking", "book", "booking", "request", "entitled", "what do i say",
              "how should i")


def _asks_for_the_time(understood):
    said = " " + str(understood.get("clean") or understood.get("text") or "").lower() + " "
    if any(phrase in said for phrase in _ALREADY_HAD):
        return False
    if any(phrase in said for phrase in _AWAY_OR_HOME):
        return False
    if any(phrase in said for phrase in _USE_THE_WEEK):
        return False
    if ((any(word in said for word in _MONTHS_NAMED) or any(word in said for word in _HOW_LONG))
            and not any(word in said for word in _ASKS_TO_HAVE)):
        return False
    if (any(phrase in said for phrase in _HAS_THE_TIME)
            and not any(phrase in said for phrase in _ASKING_FRAME)):
        return False
    return any(phrase in said for phrase in _ASKING_FRAME)


def _time_off(memory, understood):
    said = " " + str(understood.get("clean") or understood.get("text") or "").lower() + " "
    early = any(" " + phrase + " " in said or phrase in said for phrase in EARLY_WORDS)
    asking = any(word in said for word in YES_WORDS)
    if early:
        return EARLY_SCRIPT_YES if asking else EARLY_SCRIPT
    return TIME_OFF_SCRIPT_YES if asking else TIME_OFF_SCRIPT


def _follow_up(memory, understood):
    said = (understood.get("norm_text") or understood.get("text") or "")
    thanked = any(_said(said, word) for word in INTERVIEW_WORDS)
    chasing = any(_said(said, word) for word in CHASE_WORDS)
    if any(_said(said, word) for word in WHEN_WORDS):
        return FOLLOW_UP_AFTER_INTERVIEW if thanked else FOLLOW_UP_CHASE
    if thanked:
        return " ".join((FOLLOW_UP_THANKS, FOLLOW_UP_CHASE))
    if chasing:
        return " ".join((FOLLOW_UP_CHASE, FOLLOW_UP_THANKS))
    return " ".join((FOLLOW_UP_THANKS, FOLLOW_UP_CHASE))


MY_DOG_NOISE = tuple(
    "%s %s" % (owner, verb)
    for owner in ("my dog", "our dog", "my dogs", "our dogs", "my puppy", "our puppy")
    for verb in ("barks", "keeps barking", "is barking", "barking",
                 "wont stop barking", "will not stop barking")
)


COMFORT_SAY = ("what do i say", "what should i say", "what can i say", "what to say",
               "what do i tell", "what should i tell", "what can i tell", "what to tell",
               "how do i comfort", "how do i console", "comfort", "console", "comforting",
               "cheer up", "cheering up", "how do i cheer", "be there for", "how do i support",
               "how do i help them", "how do i help her", "how do i help him",
               "how do i help my", "what can i do for")
COMFORT = (
    (("crying", "cries", "cried", "tears", "tearful", "sobbing", "sobs", "broke down",
      "in bits"),
     "Say the plain thing and then stop talking: \"I'm here, and you don't have to explain.\" A "
     "hand on the arm and the silence do more than any advice; when they are ready, ask what they "
     "need today - company, a walk, or to be left alone."),
    (("dumped", "breakup", "broke up", "split up", "divorce", "divorced", "divorcing",
      "separated", "walked out", "left her", "left him", "left them", "his ex", "her ex"),
     "Say it plainly and skip the silver lining: \"that's rotten, and I'm sorry.\" Let them tell "
     "it more than once without running the ex down, and offer one concrete thing this week - a "
     "drink, a lift, dinner at yours - rather than \"let me know if you need anything\"."),
    (("sacked", "fired", "redundant", "unemployed", "lost her job", "lost his job",
      "lost their job"),
     "Lead with them, not with the fix: \"that's a horrible way to start the week - I'm sorry.\" "
     "Don't send job links in the first conversation; ask what they want to do today, and offer "
     "one practical thing later, like reading over the CV when they ask."),
    (("failed", "flunked", "rejected", "gutted", "didnt get", "didnt pass", "turned down",
      "missed out"),
     "\"That's gutting, and you were right to expect it\" beats \"something better will come "
     "along\". Let them be disappointed first; then ask whether they want to talk it through or "
     "be distracted, and do whichever they say."),
    (("ill", "sick", "unwell", "poorly", "hospital", "operation", "diagnosed", "diagnosis",
      "cancer", "chemo", "treatment", "recovering"),
     "Keep it simple and specific: \"I'm thinking of you - is a visit welcome, or would you rather "
     "I text?\" Don't ask about the prognosis or offer a cure, and offer a lift, a meal or an "
     "afternoon with the kids instead of \"anything I can do\"."),
    (("homesick", "lonely", "missing home", "moved away", "knows nobody", "on her own",
      "on his own", "on their own"),
     "Say it out loud: \"that sounds lonely, especially in the evenings.\" Ask about one specific "
     "person or place at home, and put a fixed call in the diary - a Tuesday phone call beats "
     "\"we must catch up\"."),
)
NERVES_BODY = ("feel sick", "feeling sick", "felt sick", "am sick with nerves",
               "sick with nerves", "ill with nerves", "feel ill", "queasy", "butterflies",
               "stomach turns", "stomach turning", "stomach churns", "stomach churning",
               "churning stomach", "tummy turns", "gut churning", "cant eat", "can't eat",
               "cannot eat", "dry mouth", "shaky hands", "hands shake", "shaking hands",
               "shake all over", "shaking all over", "legs like jelly", "heart racing",
               "heart races", "heart pounding", "pounding heart", "sweaty palms", "clammy",
               "cant breathe", "can't breathe", "need the loo", "running to the loo",
               "bright red", "go red", "blush")

SIGNS = (
    (("feel sick", "feeling sick", "felt sick", "am sick", "sick with nerves", "ill with nerves",
      "feel ill", "feeling ill", "nauseous", "nausea"), "Feeling sick"),
    (("queasy", "stomach turns", "stomach turning", "stomach churns", "stomach churning",
      "churning stomach", "tummy turns", "gut churning"), "That churning stomach"),
    (("butterflies",), "Butterflies"),
    (("cant eat", "can't eat", "cannot eat"), "Not being able to eat"),
    (("dry mouth",), "A dry mouth"),
    (("shaky hands", "hands shake", "shaking hands"), "Shaky hands"),
    (("shake all over", "shaking all over", "shaking", "shaky"), "That shaking"),
    (("legs like jelly", "jelly legs", "weak at the knees"), "Legs like jelly"),
    (("heart racing", "heart races", "heart pounding", "pounding heart", "heart thumping"),
     "A racing heart"),
    (("sweaty palms", "sweaty hands", "clammy"), "Clammy hands"),
    (("cant breathe", "can't breathe", "hard to breathe"), "That tight chest"),
    (("need the loo", "running to the loo"), "Needing the loo"),
    (("bright red", "go red", "going red", "blush", "blushing"), "Going red"),
)


def sign_said(text):
    said = str(text or "").lower()
    for phrases, label in SIGNS:
        if any(phrase in said for phrase in phrases):
            return label
    return None


_SIGN_PLURAL = frozenset(("Shaky hands", "Butterflies", "Legs like jelly", "Clammy hands"))


def nerves_opening(text, situation, tail):
    label = sign_said(text)
    if label is None:
        return "That feeling " + situation + " is " + tail
    return label + " " + situation + (" are " if label in _SIGN_PLURAL else " is ") + tail


TOLD_OFF = ("had a go at me", "had a go at us", "had a right go", "a go at me about",
            "had a go at me about", "told me off", "told us off", "tells me off",
            "telling me off", "got told off", "been told off", "got a telling off",
            "a telling off", "bollocked", "bollocking", "got a bollocking",
            "gave me an earful", "got an earful", "laid into me", "went off at me",
            "read me the riot act", "had a pop at me", "gave me a mouthful", "balled me out")

COMFORT_SITUATIONS = tuple(word for words, _reply in COMFORT for word in words)
COMFORT_UNNAMED = ("upset", "struggling", "hard time", "rough time", "going through",
                   "devastated", "not coping", "mental health", "dumped", "sacked")
COMFORT_LAST = ("Say it plainly and don't rush to fix it: \"that's really hard, and I'm glad you "
                "told me.\" Ask what they need today - company, quiet, or a distraction - and "
                "offer one concrete thing, like a walk or dinner on Thursday, rather than \"let me "
                "know if you need anything\".")
A_BEHAVIOUR_TOWARD_THE_ASKER = (
    "cancel", "cancels", "cancelling", "cancelled", "canceled", "bailed", "bails",
    "no show", "a no show", "flaked", "flaky",
    "late", "lateness", "always late", "late again",
    "never replies", "does not reply", "doesnt reply", "won't reply", "wont reply",
    "never texts", "doesnt text", "doesn't text", "leaves me on read",
    "ignores me", "ignored me", "ignoring me", "stopped texting", "gone quiet",
    "left me out", "leaves me out", "leaving me out", "didnt invite", "didn't invite",
    "not invited", "no invite",
    "owes me", "owes", "borrowed", "borrows", "teased", "teasing", "teases",
    "made a joke", "joke about", "jokes about", "joking about", "took the mick",
    "rude", "put me down", "puts me down", "putting me down", "snide", "nasty about me",
    "talks about me", "behind my back",
)

COMFORT_PLAIN = ("You don't need the perfect words: name it in one line (\"that sounds really "
                 "hard\"), say you are glad they told you, and offer one concrete thing - a walk, "
                 "dinner on Thursday - rather than \"let me know if you need anything\". Then ask "
                 "what they need today, company or quiet or a distraction, and do that instead of "
                 "fixing it.")


def _comfort(memory, understood):
    said = " " + ((understood or {}).get("clean") or "").lower() + " "
    leans = (understood or {}).get("leans_on")
    earlier = ""
    if isinstance(leans, dict) and isinstance(leans.get("words"), list):
        earlier = " " + " ".join(w for w in leans["words"] if isinstance(w, str)).lower() + " "
    for words, reply in COMFORT:
        for word in words:
            if " " in word:
                if " " + word + " " in said or " " + word + " " in earlier:
                    return reply
            elif re.search(r"\b" + re.escape(word) + r"\b", said + earlier):
                return reply
    if not any(re.search(r"\b" + re.escape(word) + r"\b", said + earlier)
               for word in COMFORT_SITUATIONS + COMFORT_UNNAMED):
        return None
    return COMFORT_LAST



_BEING_WRITTEN = re.compile(
    r"\b(?:how|what|whats|what's|should|could|can|would|do i|help|idea|ideas|need to|needs to|"
    r"want to|wants to|about to|write|writing|wrote|draft|drafting|word|words|"
    r"say|saying|tell|telling|template|example|examples|letter|email|e-mail|message|advice|"
    r"tips?)\b", re.I)


def _the_notice_is_being_written(understood):
    reading = understood or {}
    return bool(_BEING_WRITTEN.search(str(reading.get("clean") or "")))


ENTRIES = [
    entry("card-writing", (("card", "cards", "message", "messages", "note", "wishes",
                            "lines", "write", "writing") + SAY,
                           ("leaving", "leaving do", "last day", "goodbye", "farewell",
                            "moving on", "emigrating", "retiring", "retirement")),
          ("Keep it to two lines and one real detail: \"Working with you made the Monday mornings "
           "survivable, and I still owe you for the time you covered for me.\" Say what you will "
           "actually miss, then a plain good luck. If you want it funny, keep the joke to something "
           "the two of you share and never about their job or their leaving, and sign your full name "
           "for anyone who is not in your team."),
          bias=1,
          avoid=SAID + ON_THE_PHONE + (
              "abroad", "overseas", "australia", "canada", "usa", "america", "spain", "france",
              "italy", "ireland", "new zealand", "europe", "dubai", "first class",
              "second class", "envelope", "envelopes"),
          ask=("card", "cards", "message", "messages", "note", "wishes", "write", "writing",
               "lines", "what do i write", "what to write", "what should i write") + SAY),
    entry("card-birthday", (("card", "cards", "message", "messages", "note", "wishes",
                             "wish", "greeting", "greetings", "write", "writing",
                             "birthday card", "birthday cards", "card for", "cards for",
                             "birthday message", "birthday messages", "birthday wishes",
                             "bday card") + SAY,
                            ("birthday", "bday", "30th", "40th", "50th", "60th", "70th",
                             "18th", "21st", "65th")),
          _card_birthday,
          avoid=SAID + ("make", "makes", "making", "craft", "draw", "drawing", "design", "print",
                        "cut out", "card shop", "buy", "buying", "bought", "shop", "shops",
                        "cheap", "price", "where can i",
                        "abroad", "overseas", "australia", "canada", "usa", "america", "spain",
                        "france", "italy", "ireland", "new zealand", "europe", "dubai",
                        "first class", "second class", "envelope", "envelopes", ),
          bias=1,
          shape=(_names_an_age,),
          ask=("card", "cards", "message", "messages", "note", "wishes", "wish", "write",
               "writing", "greeting", "greetings", "what do i write", "what to write") + SAY),
    entry("card-congrats", (("card", "cards", "message", "messages", "note", "wishes",
                              "congratulations", "congrats", "write", "writing") + SAY,
                             ("new job", "new role", "promotion", "graduation", "graduated",
                              "passed", "results", "driving test", "first day")),
          ("Name the thing they did and one thing you noticed about them doing it: \"All those "
           "late nights paid off - well done, Dr Chen.\" Skip the advice and the joke, and if the "
           "card is from a group, sign the group rather than one person's name."),
          avoid=SAID + MOURNING + ("leaving", "leaving do", "last day", "goodbye", "farewell", "moving on",
                        "emigrating", "retiring", "retirement", "removals", "van", "packing",
                        "deposit", "mortgage", "house price", "buying a house", "moved out",
                        "get married", "speech", "toast", "venue", "guest list"),
          bias=1,
          ask=("card", "cards", "message", "messages", "note", "wishes", "congratulations",
               "congrats", "write", "writing", "what do i write", "what to write") + SAY),
    entry("card-new-home", (("card", "cards", "message", "messages", "note", "wishes",
                              "congratulations", "congrats", "write", "writing") + SAY,
                             ("new home", "new house", "new flat", "moved in", "moving in",
                              "first house")),
          ("Wish them well in the place, not the paperwork: \"Congratulations - may the boiler "
           "behave and the neighbours be quiet.\" A small thing for the house instead of a bottle "
           "of wine is a good present, and if you are visiting, ask before you bring anything big."),
          avoid=SAID + ("removals", "removal", "van", "packing", "pack", "unpacking", "deposit",
                        "mortgage", "house price", "buying a house", "moved out", "rent"),
          bias=1,
          ask=("card", "cards", "message", "messages", "note", "wishes", "congratulations",
               "congrats", "write", "writing", "what do i write", "what to write") + SAY),
    entry("card-something", (("card", "cards", "note", "message", "messages", "write",
                              "writing") + SAY,
                             ("what do i write", "what to write", "what should i write",
                              "what do i say", "what to say", "blank", "stuck", "no idea")),
          _card_plain,
          bias=-1,
          avoid=MOURNING + ("refund", "refunds", "complaint", "complain", "complaining",
                            "compensation", "replacement", "money back", "owed", "owes me",
                            "reference", "references", "referee", "referees", "testimonial",
                            "recommendation", "cv", "job application", "employer", "interview",
                            "how much", "how many", "cash", "money", "quid", "pounds",
                            "dollars", "euros"),
          guard=lambda reading: not _names_an_age(
              (reading or {}).get("clean") or (reading or {}).get("text")),
          shape=(_asks_for_the_words,),
          ask=("card", "cards", "note", "notes", "message", "messages", "write", "writing",
               "blank")),
    entry("card-anniversary", (("card", "cards", "message", "messages", "note", "wishes",
                                "write", "writing") + SAY,
                               ("anniversary", "years together", "married for", "wedding day")),
          ("Name the year, then one thing you are glad about: \"Ten years, and you still make me "
           "laugh at the worst jokes.\" A line about a specific time beats anything about "
           "forever; if it is someone else's anniversary, keep it to the pair and skip the advice."),
          avoid=SAID + ("buy", "buying", "present", "presents", "gift", "gifts", "restaurant",
                        "book a table", "meal out", "hotel"),
          bias=1,
          ask=("card", "cards", "message", "messages", "note", "wishes", "write", "writing",
               "what do i write", "what to write") + SAY),
    entry("card-valentines", (("card", "cards", "message", "messages", "note", "wishes",
                               "write", "writing", "love") + SAY,
                              ("valentine", "valentines", "valentines day", "14 february",
                               "romantic", "romance", "girlfriend", "boyfriend")),
          ("One true thing you would say out loud, then stop: \"I like who I am when I am with "
           "you.\" Long lists and borrowed lines read as effort, not feeling, so keep it to two "
           "lines and sign it properly unless it is going to a secret valentine."),
          avoid=SAID + ("buy", "buying", "present", "presents", "gift", "gifts", "flowers",
                        "restaurant", "book a table", "meal out", "hotel"),
          bias=1,
          ask=("card", "cards", "message", "messages", "note", "wishes", "write", "writing",
               "love", "what do i write", "what to write") + SAY),
    entry("card-parents-day", (("card", "cards", "message", "messages", "note", "wishes",
                                "write", "writing") + SAY,
                               ("mothers day", "mothering sunday", "fathers day",
                                "mums day", "dads day")),
          ("One thing she or he actually did for you, named plainly: \"Thanks for every school "
           "run in the rain.\" A memory does more than \"best mum ever\", and if you are not "
           "close, a warm two lines and both your names is enough - the present is a separate job."),
          avoid=SAID + ("buy", "buying", "bought", "present", "presents", "gift", "gifts",
                        "ideas", "what should i get", "cheap", "price", "restaurant",
                        "book a table", "birthday"),
          bias=1,
          ask=("card", "cards", "message", "messages", "note", "wishes", "write", "writing",
               "what do i write", "what to write") + SAY),
    entry("card-new-baby", (("card", "cards", "message", "messages", "text", "texts", "note",
                              "wishes", "congratulations", "congrats", "congratulate",
                              "congratulating", "write", "writing") + SAY,
                             ("new baby", "newborn", "baby", "babies", "birth", "born",
                              "has arrived", "have arrived", "just arrived", "arrived yesterday",
                              "arrived last night", "arrived this morning",
                              "having a baby", "had a baby", "baby on the way")),
          ("Name the baby if you know the name, wish the parents some sleep, and skip the jokes "
           "about their life being over: \"Congratulations - she is beautiful. Wishing all three "
           "of you a slow, sleepy first month.\" If it is a second baby, say something about the "
           "older one too; nobody else will."),
          avoid=SAID + ("buy", "buying", "bought", "shop", "shops", "present", "presents", "gift",
                        "gifts", "make", "making", "craft", "take", "taking", "bring",
                        "visiting"),
          bias=1,
          ask=("card", "cards", "message", "messages", "text", "texts", "note", "wishes",
               "congratulations", "congrats", "congratulate", "congratulating", "write",
               "writing", "what do i write", "what to write") + SAY),
    entry("card-get-well", (("card", "cards", "message", "messages", "note", "write",
                             "writing", "wishes") + SAY,
                            ("get well", "get better", "speedy recovery", "poorly", "operation",
                             "surgery", "in hospital", "recovering", "recovery",
                             "illness"),
                            ("hospital", "in hospital", "ward", "operation", "surgery")),
          ("Say the one thing you want for them and keep it light: \"Thinking of you - take the "
           "time you need and we will save you a seat.\" No advice, no story about your own "
           "operation, and do not say \"let me know if you need anything\": offer something "
           "specific instead, like a lift home or dinner on Thursday."),
          avoid=SAID + ("how long", "how soon", "recover from", "back to work", "pain",
                        "take", "taking", "bring", "brings", "give them", "visit", "visiting",
                        "better at", "get better at", "improve", "improving", "improvement",
                        "mp", "msp", "councillor", "council", "landlord", "letting agent",
                        "insurer", "insurance", "employer", "appeal", "ombudsman", "dwp"),
          bias=1,
          ask=("card", "cards", "message", "messages", "note", "write", "writing",
               "wishes", "what do i write", "what to write") + SAY),
    entry("card-wedding", (("card", "cards", "message", "messages", "note", "write", "writing",
                            "wishes") + SAY,
                           ("wedding", "married", "marriage", "engagement", "engaged",
                            "the big day")),
          ("Two lines, one about them as a pair: \"So glad you two found each other - the way you "
           "laugh at the same things is the whole thing.\" Put both their names on the envelope, "
           "and if you are not going, say so warmly in one line and leave it there."),
          avoid=SAID + ("speech", "toast", "venue", "seating", "table plan", "guest list",
                        "first dance", "my husband", "my wife", "get married", "propose"),
          bias=1,
          ask=("card", "cards", "message", "messages", "note", "write", "writing",
               "wishes", "what do i write", "what to write") + SAY),
    entry("card-christening", (("card", "cards", "message", "messages", "note", "write",
                                "writing", "wishes") + SAY,
                               ("christening", "baptism", "baptised", "naming ceremony",
                                "godparent", "godparents")),
          ("Name the baby and one wish: \"Welcome to the world, Ada - may you be as loved as you "
           "were today.\" Sign both your names, and if you gave a present, the card is not the "
           "place to describe it."),
          avoid=SAID + ("wear", "wearing", "dress", "outfit", "suit", "what should i wear",
                        "christening gown", "present", "presents", "gift", "gifts"),
          bias=1,
          ask=("card", "cards", "message", "messages", "note", "write", "writing",
               "wishes", "what do i write", "what to write") + SAY),
    entry("card-christmas", (("card", "cards", "message", "messages", "note", "write",
                              "writing", "wishes", "greetings") + SAY,
                             ("christmas", "xmas", "festive", "new year", "season's")),
          ("Two lines is plenty unless it is family: \"Merry Christmas - hope the year has been "
           "kind to you and the next one is better.\" Add a specific thing you remember from the "
           "year for anyone close (\"still laughing about the tent\"), and for a neighbour or a "
           "colleague a plain wish and both your names is the whole job."),
          bias=1,
          avoid=SAID + ("make", "makes", "making", "craft", "draw", "design", "print",
                        "cut out", "buy", "buying", "bought", "shop", "shops", "cheap",
                        "price", "where can i"),
          ask=("card", "cards", "message", "messages", "note", "write", "writing",
               "wishes", "greetings", "what do i write", "what to write") + SAY),
    entry("landlord-broken-boiler", ("landlord", "broken", "repair", ("boiler", "heating", "email", "message")),
          the_fault(
              "Keep it short, dated and specific, and ask for a date: \"Hi — I reported the "
              "{fault} on [date] and nothing has been done. Please let me know when an engineer "
              "can come; I'm home after 5pm on weekdays. Thanks, [name].\" Follow it up in "
              "writing if nothing happens in 48 hours. Anything unsafe, the heating, the hot water "
              "and any appliance that came with the flat are the landlord's job, so if they ignore "
              "you ask the council's environmental health team to step in, keep the messages, and "
              "keep paying the rent: withholding it usually puts you in the wrong.",
              "Keep it short, dated and specific, and ask for a date. Say what is wrong, when it "
              "started and when you are in, and follow it up in writing if nothing happens in 48 "
              "hours. Anything unsafe, the heating, the hot water and any appliance that came with "
              "the flat are the landlord's job, so if they ignore you ask the council's "
              "environmental health team to step in, keep the messages, and keep paying the rent: "
              "withholding it usually puts you in the wrong."),
          avoid=("deposit", "moved out", "moving out", "washing machine", "dishwasher", "fridge",
                 "freezer", "oven", "tumble dryer", "vacuum", "hoover", "car", "laptop", "phone"),
          ask=("landlord", "landlady", "letting agent", "letting agency", "housing", "council",
               "letter", "email", "message", "text", "note", "write", "writing", "word", "wording",
               "complain", "complaint", "rights", "refusing", "refuses", "ignoring", "honour")),
    entry("neighbour-dangerous-dog",
          (("neighbours", "neighbour", "neighbors", "neighbor", "next door", "next-door",
            "nextdoors", "upstairs", "downstairs", "flat above"),
           ("dog", "dogs", "puppy")),
          ("Keep your own dog out of its way while this is going on - walk a different way and do "
           "not try to introduce them through the fence. Write down each time it happens: the date, "
           "the time, what the dog did, and whether anyone was hurt. Report it to the council's dog "
           "warden with those details, since a dog out of control in a public place or in your "
           "garden is their job, and a dog that has injured a person or another animal is a police "
           "matter. If the owner is approachable, say it plainly once: \"your dog went for mine on "
           "Tuesday by the gate - can you put it on a lead there?\" If anyone is bitten, get medical "
           "help or a vet first and report it afterwards, and keep every message you send."),
          ask=("aggressive", "aggression", "attacks", "attacking", "attacked", "bites", "bitten",
               "bit my", "bit me", "growls", "growling", "growled", "snarls", "snarling",
               "snapped at", "lunges", "lunging", "went for", "goes for", "dangerous", "vicious",
               "savage", "out of control", "terrified of it", "scared of it", "chased", "chasing"),
          bias=2,
          avoid=("i got bitten", "i was bitten", "i have been bitten", "bit someone",
                 "my dog bit", "my puppy bit", "my dog is aggressive", "my dog attacks",
                 "my dog snapped", "what should i do if a dog bites")),
    entry("neighbour-noise",
          (("neighbours", "neighbour", "neighbors", "neighbor", "next door", "upstairs",
            "downstairs", "flat above", "someones dog", "someone else's dog", "someone elses dog",
            "someone's dog", "a dog down the road", "dog down the road", "their dog"),
           ("music", "banging", "barking", "bark", "dog", "party",
            "message", "talk",
            "wont shut up", "won't shut up", "shut up", "never shuts up", "keeps barking",
            "drill", "drilling", "hammering", "sawing", "building work", "builders",
            "renovation", "renovating", "extension") + NOISE_WORDS +
            ("keeps me awake", "wakes me up", "all night", "all day")),
          ("Talk to them once, at a calm time, and say when it happened and what you need: \"this "
           "has gone on after 11pm most nights this week, and I'm up at six - can it stop by then?\" "
           "Name the time and the nights, not the person. If it carries on, keep a short log of dates "
           "and times and report it to the council's noise team, who can act on it without you having "
           "to confront anyone."),
          ask=("music", "banging", "barking", "barks", "bark",
               "howling", "howls", "all night", "at night", "every night", "all hours",
               "cant sleep", "can't sleep", "awake", "wake", "woken", "party",
               "keep me up", "keeps me up", "shut up", "goes mad", "yapping", "whining",
               "screaming", "disturbing",
               "drill", "drilling", "hammering", "sawing", "building work", "builders",
               "renovation", "renovating", "extension") + NOISE_WORDS,
          bias=1,
          avoid=("fun", "enjoyed", "enjoy", "enjoying", "loved", "love", "lovely", "great",
                 "nice", "thanks", "wedding", "birthday", "sad", "upset", "anxious", "worried",
                 "lonely") + MY_DOG_NOISE),
    entry("ask-for-refund", (("complain", "complaint", "refund", "refunds", "money back",
                              "complained about"),
                             "product",
                             ("service", "back", "message", "money", "broke", "broken", "faulty",
                             "write", "writing", "email", "words", "word", "draft", "letter",
                             "say", "saying", "ask", "asking", "phrasing",
                             "asking for", "letter asking", "asking for a refund",
                             "asking for my money back", "letter of complaint",
                             "email asking", "write asking")),
          ("State the order, the problem and what you want, in that order: \"I ordered a lamp on 3 May "
           "(order 12345). It arrived cracked. Please send a replacement or refund the £40.\" Give a "
           "deadline of 14 days and mention your rights only if they say no."),
          ask=("write", "writing", "email", "message", "say", "saying", "words", "word",
               "ask", "asking", "how do i ask",
               "draft", "letter", "text", "reply", "phrasing", "complain", "complaining",
               "complaint"),
          avoid=("shop", "shops", "in store", "store i", "receipt", "entitled", "consumer rights",
                 "my rights", "30 days", "thirty days",
                 "can i get", "am i entitled", "are they allowed", "do i have to",
                 "is it legal", "should they", "how long",
                 "train", "trains", "rail", "railway", "railcard", "delay repay", "flight",
                 "flights", "airline", "plane", "hotel", "booking", "concert", "gig",
                 "festival", "theatre", "theater", "cinema", "match", "festival ticket",
                 "train ticket", "bus ticket", "coach ticket", "season ticket", "ferry",
                 "ticket", "tickets", "holiday", "package holiday", "cruise", "travel agent",
                 "tour operator", "cottage", "villa", "campsite",
                 "tax", "tax refund", "tax rebate", "rebate", "hmrc", "p800",
                 "benefit", "benefits", "universal credit", "council tax", "pension",
                 "text saying", "email saying", "emailed saying", "rang saying", "called saying",
                 "phoned saying", "message saying", "telling me", "saying im", "saying i am")),
    entry("decline-a-meeting",
          (("meeting", "meetings", "zoom", "call with", "stand-up", "standup"),
           ("decline", "declining", "cancel", "cancelling", "excuse", "politely",
            "get out of", "skip", "reschedule")),
          ("Be brief and offer a substitute: \"I can't make Tuesday — can we do Thursday, or shall I "
           "send a note with my points?\" A short reason and an alternative reads as organised rather "
           "than rude.")),
    entry("apology-message",
          (("sorry", "apologise", "apologize", "apologise", "apology"),
           ("friend", "sister", "brother", "mum", "dad", "partner", "said", "hurt", "upset",
            "row", "argument", "fight", "write", "message", "properly",
            "wife", "husband", "girlfriend", "boyfriend", "partner", "fiance", "fiancee",
            "flatmate", "housemate", "neighbour", "neighbor", "son", "daughter", "mother",
            "father", "colleague", "say", "tell", "words", "wording")),
          ("Name what you did, say why it was wrong, and don't add a but: \"I said I'd call and I "
           "didn't, and that left you waiting. I'm sorry.\" Then say what you will do differently, in "
           "one sentence."),
          ask=("sorry", "apologise", "apologize", "apology")),
    entry("accept-an-apology",
          (("sorry", "apology", "apologise", "apologize", "apologies", "apologises",
            "apologizes", "apologising", "apologizing", "apologized", "apologised"),
           ("to me", "said sorry", "says sorry", "said it", "someone said", "someone apologised",
            "someone apologizes", "someone apologises", "reply", "respond", "answer", "accept",
            "accepting", "forgive", "forgiving", "what do i say", "what should i say",
            "how do i reply", "how do i respond", "they said sorry", "he said sorry",
            "she said sorry", "apologised to me", "apologized to me", "apologises to me",
            "apologizes to me", "said sorry to me", "says sorry to me")),
          ("Take it plainly and say so: \"Thanks for saying that - it means a lot.\" Then, if "
           "something is still needed, name one thing in a sentence (\"a text next time you are "
           "running late would help\") and leave it there. You do not have to forgive on the spot; "
           "accepting the apology is enough for today."),
          ask=("sorry", "apology", "apologise", "apologize", "say", "saying", "what", "how",
               "reply", "respond", "accept", "forgive", "back", "after", "when"),
          avoid=("i said sorry", "i already said sorry", "i apologise", "i apologize",
                 "i have apologised", "how do i say sorry", "how to say sorry",
                 "should i apologise", "should i say sorry", "wont apologise", "wont say sorry",
                 "never apologises", "never says sorry", "owes me an apology",
                 "owe me an apology", "refuses to apologise", "refuses to say sorry",
                 "stop saying sorry", "sorry for your loss", "condolence", "died", "funeral",
                 "passed away", "grief",
                 "how do i write", "how to write", "write a text", "write a message",
                 "text to say", "draft", "drafting", "wording", "how do i say", "how to say",
                 "should i send"),
          bias=2),

    entry("apology-somebody-owes",
          (("wont apologise", "wont say sorry", "wont apologise to me", "never apologises",
            "never apologize", "never apologise", "never says sorry", "never say sorry",
            "doesnt apologise", "doesnt say sorry", "not apologising", "refuses to apologise",
            "refuses to say sorry", "owes me an apology", "owe me an apology",
            "owes me a sorry", "apologise to me", "apologize to me",
            "should apologise to me", "should say sorry to me", "should have apologised",
            "get him to apologise", "get her to apologise", "get them to apologise",
            "wont admit he", "wont admit she", "never admits", "never admits he is wrong"),
           ("my husband", "my wife", "my partner", "my mum", "my dad", "my friend", "my boss",
            "my sister", "my brother", "my boyfriend", "my girlfriend", "my son", "my daughter",
            "my mother", "my father", "he", "she", "they", "him", "her", "them", "his",
            "himself", "herself", "how", "what", "should", "can", "why", "never")),
          ("You cannot make someone sorry, so ask for the repair rather than the words: say what "
           "you needed and what you will do now - \"I needed you to say it mattered, and I am not "
           "going to keep bringing it up.\" Ask once, plainly, and let them decide; if it never "
           "comes, the useful question is what you want next, not how to get it out of them."),
          ask=("never", "wont", "doesnt", "owes", "owe", "owed", "should", "refuses", "to me",
               "how", "what", "why", "can"),
          bias=3,
          avoid=("died", "death", "funeral", "passed away", "sorry i", "im sorry", "my fault",
                 "stop saying sorry", "all the time", "too much", "so much", "i apologise",
                 "i apologize", "i said sorry", "i should say sorry",
                 "what do i say", "what should i say", "what do i write", "reply", "respond",
                 "accept", "said sorry to me", "says sorry to me", "apologises to me",
                 "apologizes to me", "apologised to me", "apologized to me",
                 "when someone apologises", "when someone apologized", "when someone says sorry")),
    entry("email-to-teacher", ("teacher", "childs", "school", ("email", "write", "message")),
          ("Put the child's name and class in the subject, say what you have noticed and what you "
           "would like: \"Sam (5B) has been anxious about maths homework — could we talk for ten "
           "minutes this week?\" Keep it to a few lines and ask for a specific next step."),
           avoid=("with a cold", "a cold", "with flu", "a cough", "temperature", "chest infection",
                 "thank you", "thankyou", "thank-you", "thanks",
                 "vomiting", "sickness bug", "chickenpox",
                 "off school", "home from school", "keep my child home", "well enough",
                 "should i keep", "keep him home", "keep her home", "keep them home",
                 "when can he", "when can she", "how long off",
                 "bullied", "bullying", "bullies", "picked on", "being picked on",
                 "my teacher", "my lecturer", "my tutor", "my professor", "my form tutor",
                 "choose a school", "choosing a school", "choose the school",
                 "which school", "what school", "schools to look at", "look at schools",
                 "visit schools", "school visits", "school open day", "compare schools",
                 "pick a school", "picking a school", "decide on a school",
                 "school for my child", "school for my son", "school for my daughter"),
          bias=2),
    entry("note-to-school-absence",
          (("report my child absent", "report an absence", "report the absence",
            "report my child off", "absent from school", "absence from school",
            "school absence", "school absences", "note for school", "note to school",
            "letter to school", "letter for school", "email the school", "email school about",
            "write to the school", "write to school about", "sick note", "school note",
            "note about my child", "letter about my child", "off school note"),
           ("report", "note", "letter", "absent", "absence", "absences", "written")),
          "Say the child's name and class, the dates they were off, and the reason in one line: "
          "\"Sam, 5B, off Thursday and Friday with a sickness bug - back on Monday.\" Ask them to "
          "mark it authorised, and offer a doctor's note or appointment card if they want one. "
          "Email the school office with the dates in the subject line; most schools want a call "
          "on the first morning as well as the note.",
          bias=2,
          ask=("note", "letter", "email", "write", "written", "absent", "absence", "absences",
               "sick note", "report"),
          avoid=("uniform", "uniforms", "blazer", "pinafore", "pe kit", "shoes", "socks",
                 "stain", "stains", "school run", "dropping off", "drop off",
                 "choose a school", "choosing a school", "which school", "school place",
                 "admissions", "ofsted", "catchment")),
    entry("asking-for-time-off",
          (("time off", "holiday", "holidays", "day off", "days off",
            "week off", "weeks off", "week off work", "leave early", "leaving early",
            "finish early", "half day", "an hour early", "early on friday", "dentist", "doctor",
            "appointment", "friday off", "monday off", "tuesday off", "wednesday off",
            "thursday off", "tomorrow off"),
           ("boss", "request", "email", "book", "work", "ask", "asking", "leave", "leaving", "take",
            "can i", "could i", "off")),
          _time_off,
          ask=("time off", "day off", "days off", "boss", "work", "email", "early", "half day",
               "off"),
          bias=2,
          avoid=("sick", "ill", "unwell", "poorly", "not well", "temperature", "fever", "flu",
                 "migraine", "headache", "vomiting", "throwing up",
                 "with the kids", "with my kids", "with my children", "with the children",
                 "kids off school", "school holidays", "half term",
                 "another job", "new job", "second job", "quit", "quitting", "leave my job",
                 "lose weight", "lose a stone", "losing weight", "diet", "get fit", "gym",
                 "entitled", "entitlement", "statutory", "pro rata", "pro-rata", "minimum",
                 "how many days holiday", "how much holiday", "how many holidays",
                 "putting", "postponing", "procrastinating",
                 "calls me", "calling me", "called me", "rings me", "rang me", "ring me",
                 "ringing me", "texts me", "texted me", "texting me", "messages me",
                 "phoned me", "phones me", "keeps calling", "keeps ringing", "keeps texting",
                 "contacts me", "expects me at work",
                 "pay off", "paying off", "credit card", "card debt", "card payment", "debts",
                 "debt", "savings", "save up", "saving up", "or save", "overpay", "mortgage",
                 "interest",
                 "where can i go", "where should i go", "where could i go", "where to go",
                 "where would you go", "where should we go", "where can we go",
                 "where could we go", "where would we go", "which country", "somewhere warm",
                 "what should i do", "what can i do", "what to do", "any ideas", "any tips",
                 "no idea", "nothing planned", "nothing to do", "keep busy", "bored",
                 "cook", "cooking", "bake", "baking", "meal", "meals", "dinner", "dinners",
                 "lunch", "lunches", "recipe", "recipes", "save", "saving", "savings",
                 "save up", "money", "budget", "cost", "afford", "quid", "pounds",
                 "broke", "skint", "hard up", "no money", "tight month", "on a budget",
                 "plan a trip", "planning a trip", "book a trip", "a trip", "trip with",
                 "going away", "go away for", "get away for", "a break away",
                 "book a holiday", "plan a holiday", "planning a holiday"),
                guard=_asks_for_the_time),
    entry("follow-up-email",
          (("chase", "chasing", "chased", "follow up", "followed up", "follow-up",
            "following up", "follows up", "chase up", "chasing up", "email",
            "emailed", "emailing", "note", "reply", "replies", "write", "writing", "message",
            "nudge"),
           ("interview", "interviews", "application", "applications", "applied", "recruiter",
            "hiring manager", "panel", "job offer", "about a job", "for a job", "the job",
            "vacancy", "role",
            "following up", "follows up", "follow up", "chase up", "chasing up", "chasing")),
          _follow_up,
          avoid=("never replies", "never reply", "never answers", "never answer", "never emails",
                 "letter of application",
                 "wont reply", "won't reply", "wont answer", "doesnt reply", "doesn't reply",
                 "doesnt answer", "doesn't answer", "ignores my", "ignored my", "no reply",
                 "no response", "nothing back", "my manager", "my boss", "my employer",
                 "chased twice", "asked twice",
                 "cover letter", "covering letter",
                 "results", "blood test", "bloods", "scan", "x-ray", "smear", "biopsy", "gp",
                 "doctor", "hospital", "surgery", "nurse", "test result", "appointment",
                 "after applying", "after i applied", "after you apply", "after my application",
                 "after sending my cv", "after sending my application",
                 "after sending the application", "after sending it",
                 "after the closing date", "after the closing date should") + NOT_A_JOB),
    entry("raise-a-problem-with-friend", ("friend", "upset", "hurt", ("problem", "bring", "tell")),
          _raise_problem,
          avoid=("cooking", "cooks", "baking", "bakes", "food", "singing", "haircut", "outfit",
                 "writing", "drawing", "performance",
                 "cheat", "cheats", "cheated", "cheating", "affair", "affairs",
                 "like her", "like him", "like them", "fancy", "feelings", "a crush", "in love",
                 "depression", "depressed", "anxiety", "anxious", "mental health", "diagnosis",
                 "coming out", "gay", "lesbian", "trans",
                 "cant come", "cant make it", "not coming", "cant be there", "cant go",
                 "wont be able to come", "have to cancel", "had to cancel", "cannot make it",
                 "wedding", "christening", "funeral", "engagement", "hen do", "stag do"),
          guard=_not_a_hurt_body),
    entry("tell-someone-you-cant-come",
          (("cant come", "cant make it", "not coming", "cant be there", "wont be able to come",
            "cant go", "have to cancel", "had to cancel", "pull out", "cannot make it"),
           ("wedding", "birthday", "christening", "party", "dinner", "christmas", "lunch",
            "visit", "meal", "funeral", "barbecue", "bbq", "engagement", "hen do", "stag do")),
          ("Say it early and plainly, give one reason and offer one thing instead: \"I'm so sorry, I "
           "can't make Saturday after all - I'm not well enough to travel. Can I take you both out "
           "once the dust settles?\" Short is kinder than detailed; a long excuse sounds like a "
           "choice, and telling them before they have paid for your plate is the whole kindness.",
           "Say it as soon as you know, name the reason in one line and say what you can still do: "
           "\"I can't be there on the day, but I'd love to come and see you the week after.\" Do not "
           "leave it until the last week, and do not offer a string of excuses - one reason and one "
           "alternative reads as true, several read as invented."),
          ask=("cant come", "cant make it", "not coming", "cant be there", "wont be able to come",
               "cant go", "have to cancel", "had to cancel", "pull out", "cannot make it"),
          avoid=("money", "lend", "lent", "debt", "borrow", "job", "resign", "quit")),
    entry("how-to-tell-them",
          (("how do i tell", "how should i tell", "how to tell", "how do i break",
            "how do i ask", "how should i ask", "how can i ask", "how to ask",
            "break the news", "how do i say", "how do i bring it up", "how do i bring up",
            "bring it up with", "how do i raise it", "how do i talk to my", "talk to my",
            "how do i tell my", "telling my", "how do i announce",
            "talks over me", "talking over me", "talk over me", "talks over my",
            "keeps talking over", "interrupts me", "interrupting me", "interrupts my",
            "keeps interrupting", "cuts me off", "keeps cutting me off", "butts in",
            "keeps butting in", "always butts in", "butting in on",
            "finishes my sentences",
            "how do i give", "how to give", "how do i break it", "how to break it",
            "words to say", "words to use", "words to tell", "give me the words",
            "help me word", "put it in words", "put this in words", "find the words",
            "what words", "which words"),
           ("parents", "parent", "mum", "dad", "mother", "father", "partner", "husband", "wife",
            "housemate", "housemates", "flatmate", "flatmates", "roommate", "family",
            "my friend", "my friends", "brother", "sister", "son", "daughter", "kids",
            "children", "my boss", "my team", "team", "staff", "colleagues", "everyone",
            "someone", "somebody", "person", "people", "friend", "friends",
            "neighbour", "neighbours", "neighbor", "neighbors", "my neighbour",
            "housemates", "flatmates", "roommates", "workmate", "workmates", "coworker",
            "co-worker", "boyfriend", "girlfriend", "fiance", "fiancee", "my ex", "ex partner",
            "nan", "nana", "grandma", "grandad", "granny", "grandparent", "in laws", "in-law",
            "stepson", "stepdaughter", "stepchildren")),
          _saying_it,
          ask=("tell", "say", "ask", "asking", "asks", "bring", "raise", "talk", "breaking",
               "announce", "telling", "give", "giving",
               "talks over me", "talking over me", "talk over me", "talks over my",
               "keeps talking over", "interrupts me", "interrupting me", "interrupts my",
               "keeps interrupting", "cuts me off", "keeps cutting me off", "butts in",
               "keeps butting in", "always butts in", "butting in on", "finishes my sentences"),
          avoid=("cant come", "cant make it", "not coming", "cannot make it", "have to cancel",
                 "wedding", "funeral", "hen do", "stag do",
                 "resign", "resigning", "leaving my job", "quit", "notice period",
                 "santa", "father christmas",
                 "died", "dying", "death", "dead", "passed away", "put down",
                 "im leaving", "i'm leaving", "leaving my job", "leaving the job", "leaving work",
                 "leaving the company", "resigning", "resign", "my notice", "notice period",
                 "divorce", "divorced", "divorcing", "divorce papers", "getting divorced",
                 "separating", "separated", "splitting up",
                 "diagnosis", "diagnosed", "depression", "depressed", "anxiety", "mental health",
                 "coming out", "gay", "lesbian", "trans",
                 "cheated", "cheating", "affair", "betrayed",
                 "say no", "saying no", "no to my", "how to say no",
                 "lend", "lending", "loan", "borrow", "borrowing", "lend them",
                 "owes me", "owe me", "owed me", "owes me money", "pay me back", "pays me back",
                 "paid me back", "get it back", "money back",
                 "pay rise", "payrise", "raise", "promotion", "pay review", "more money",
                 "time off", "day off", "days off", "annual leave", "holiday", "holidays",
                 "im busy", "i'm busy", "dont want to go", "don't want to go",
                 "doesnt want to go", "cant go", "can't go", "turned down", "turn down",
                 "not invited", "uninvited",
                 "my boss", "boss", "manager", "colleagues", "colleague", "in meetings",
                 "in a meeting", "at work", "standup", "stand-up", "line manager",
                 "work from home", "working from home", "wfh", "my kids interrupt",
                 "the kids interrupt", "children interrupt", "kids keep interrupting",
                 "tell off", "telling off", "told off", "tell him off", "tell her off",
                 "tell them off", "tell my kid off", "tell my son off", "tell my daughter off",
                 "tick off")),
    entry("tell-kids-santa",
          (("santa", "father christmas"),
           ("real", "pretend", "truth", "isnt real", "doesnt exist", "believe", "believes",
            "belief", "tell", "telling", "how old", "age", "found out", "teased")),
          ("Answer what they asked and keep the game: \"The presents come from us - the Santa story "
           "is a game grown-ups play to make Christmas feel magic, and now you are in on it.\" Ask "
           "them to keep it going for a younger cousin or brother, which turns the news into a job. "
           "Most children work it out at six or seven and want the ritual more than the belief.",
           "Keep it warm and short: \"The Santa story is a game we all play - I put the presents "
           "out, and now you know the secret.\" Then give them a part to play for a younger child, "
           "because being trusted with the secret is what makes it feel like growing up rather "
           "than being lied to."),
          ask=("tell", "telling", "told", "should i tell", "do i tell", "break it",
               "break the news", "worked out", "work out", "found out", "stop believing",
               "keep believing", "now she knows", "now he knows", "the truth about santa")),
    entry("break-hard-news-to-children",
          (("break the news", "bad news", "hard news", "difficult news", "something awful",
            "something terrible"),
           ("children", "kids", "child", "son", "daughter", "family", "toddler")),
          "Pick a calm moment with time after it, sit at their level and give the one fact in a "
          "short sentence, then say what stays the same: who picks them up, where they sleep, that "
          "you are not going anywhere. Then stop and let them ask; the real questions come later, "
          "in the bath or the car, and answering them plainly is the rest of the job.",
          ask=("break the news", "bad news", "hard news", "difficult news", "something awful",
               "something terrible"),
          avoid=("died", "death", "dying", "passed away", "divorce", "separating", "splitting up",
                 "cancer", "ill", "illness", "diagnosis", "job", "redundant", "sacked", "fired",
                 "santa", "pregnant", "baby"),
          bias=1),
    entry("news-pregnancy",
          (("say", "said", "saying", "text", "message", "write", "words", "reply",
            "respond", "react", "answer", "congratulate", "congratulations", "congrats",
            "tell her", "tell him", "tell them", "what do i say back") + SAY,
           ("pregnant", "pregnancy", "expecting", "expecting a baby", "baby on the way",
            "having a baby")),
          ("Say congratulations first and mean it, then ask how she is: \"That is such good news "
           "- how are you feeling?\" Let her set the tone, because the first months are often "
           "sick and tired rather than shiny, and ask who already knows before you tell anyone "
           "else. Skip your own birth stories and do not ask whether it was planned."),
          avoid=SAID + (
                        "if i am", "if im", "if i'm", "asks if", "asked if", "asking if",
                        "whether i am", "whether im", "do you think i am", "am i pregnant",
                        "tell my boss", "tell my employer", "tell my manager", "maternity",
                        "paternity", "am i", "could i be", "test", "trying", "conceive",
                        "ivf", "bleeding", "cramps", "miscarriage", "losing the baby",
                        "symptoms", "due date", "weeks",
                        "buy", "buying", "present", "presents", "gift", "gifts", "visit",
                        "visiting", "take round",
                        "payslip", "payslips", "pay slip", "wages", "wage", "salary",
                        "salaries", "paid", "underpaid", "overpaid", "tax", "short this month"),
          bias=1),
    entry("news-splitting-up",
          (("say", "said", "saying", "text", "message", "write", "words", "reply",
            "respond", "react", "answer") + SAY,
           ("divorce", "divorcing", "divorced", "separating", "separated", "separation",
            "splitting up", "split up", "breaking up", "broke up", "marriage is over",
            "leaving her husband", "leaving his wife", "left her husband", "left his wife",
            "walked out")),
          ("Do not take a side and do not ask what happened: \"I'm sorry - that's a lot. How are "
           "you holding up?\" Then listen, and offer one thing you can actually do, like a bed for "
           "the night or dinner on Thursday. Say nothing about their ex that you might have to take "
           "back later, and keep checking in over the next few months, when the visits stop."),
          avoid=SAID + ("lawyer", "solicitor", "legal",
                        "custody", "child maintenance", "csa", "house", "mortgage", "deposit",
                        "pension", "split the money", "who gets", "petition", "fees",
                        "i want to", "how do i tell", "tell my husband", "tell my wife",
                        "i'm leaving", "im leaving", "i cheated", "affair"),
          bias=1),
    entry("news-diagnosis",
          (("say", "said", "saying", "text", "message", "write", "words", "reply",
            "respond", "answer", "react") + SAY,
           ("diagnosed", "diagnosis", "cancer", "tumour", "tumor", "chemo", "chemotherapy",
            "radiotherapy", "ill", "illness", "unwell", "poorly", "condition",
            "multiple sclerosis", "parkinsons", "crohns", "epilepsy", "diabetes", "lupus",
            "heart condition", "has hiv")),
          ("Say the plain thing and stop there: \"I'm sorry, that's a shock. How are you doing?\" "
           "Let them name the illness and the treatment in their own time, and take your steer from "
           "how much they want to talk about it. No cures, no \"my aunt had that and she's fine\", "
           "no advice - and offer one specific, repeatable help, like lifts to appointments, then "
           "do it."),
          avoid=SAID + ("symptoms", "treatment", "cure", "diet", "do i have", "do they have",
                        "tell work", "tell my boss", "survival", "prognosis", "stages",
                        "is it", "am i", "are these", "could it be",
                        "died", "dying", "passed away", "funeral", "terminal",
                        "buy", "buying", "present", "presents", "gift", "gifts", "visit",
                        "visiting", "take round"),
          bias=1),
    entry("news-lost-job",
          (("say", "said", "saying", "text", "message", "write", "words", "reply",
            "respond", "answer", "react") + SAY,
           ("lost his job", "lost her job", "lost their job", "made redundant",
            "being made redundant", "redundant", "redundancy", "laid off", "losing his job",
            "losing her job", "losing their job", "been sacked", "got sacked", "been fired",
            "got fired", "let go from work", "lost the job")),
          ("Do not rush to fix it: \"That's rough - I'm sorry. How are you doing?\" Then offer the "
           "practical thing they will need in a week or two, like a reference, a look over their CV "
           "or a name to ring, rather than a plan on the first day. Skip anything that sounds like a "
           "lesson - everything happens for a reason, it worked out for the best - and do not ask "
           "what they did wrong."),
          avoid=SAID + ("i lost my job", "i've lost my job", "i got sacked", "i was sacked",
                        "i got fired", "i was made redundant", "i've been made redundant",
                        "benefits", "universal credit", "sign on", "mortgage", "rent",
                        "interview", "notice pay", "redundancy pay", "tribunal", "sack him",
                        "sack her", "fire him", "fire her", "dismiss", "appraisal"),
          bias=1),
    entry("quit-a-job-message",
          (("resign", "resignation", "my notice", "notice in", "quitting", "quit", "leaving my job",
            "leaving the job", "leave my job", "leaving work for good", "im leaving", "i'm leaving",
            "hand in my notice", "working my notice", "leave a job", "leaving a job",
            "leaving email", "leaving message", "farewell email", "farewell message",
            "goodbye email", "goodbye message"),
           ("letter", "email", "message", "boss", "manager", "hand", "job", "tell", "write",
            "resign")),
          ("Keep it to four lines: that you are resigning, the date your notice starts, your last "
           "working day, and thanks. Do it in a short meeting first, then send the letter the same "
           "day, and check your contract for the notice period."),
          guard=_the_notice_is_being_written,
          avoid=("landlord", "landlady", "flat", "tenancy", "rent", "lease", "house",
                 "last job", "previous job", "old job", "current job", "interview", "cv",
                 "why i left", "why i'm leaving", "why i quit", "why did i leave",
                 "reference", "references", "left out", "left over", "left behind",
                 "left the", "left my keys", "left my phone", "left my wallet",
                 "leaving early", "leave early", "half day", "dentist", "pick up", "collect",
                 "appointment", "sick", "early on", "hour early", "time off", "day off",
                 "partner", "husband", "wife", "boyfriend", "girlfriend", "fiance", "fiancee",
                 "friend", "brother", "sister", "mum", "dad", "son", "daughter", "colleague",
                 "should i quit", "should i resign", "if i should quit", "if i should leave",
                 "whether to quit", "whether i should quit", "whether i should leave",
                 "know if i should", "should i leave", "should i stay", "quit or stay",
                 "worth quitting", "worth resigning", "worth leaving",
                 "he wants to", "she wants to", "he is going to", "she is going to",
                 "interview", "interviews", "interviewer", "why i left", "why did i leave",
                 "ask why i left", "cv", "application", "applying",
                 "no notice", "without notice", "short notice", "at short notice", "on notice",
                 "rota", "rotas", "shift", "shifts", "hours changed", "changed my hours",
                 "holiday", "holidays", "annual leave", "entitlement", "entitled",
                 "statutory", "pro rata", "pro-rata", "accrued", "accrue",
                 "how much holiday", "how many days")
                 + ON_THE_PHONE),
    entry("voicemail",
          (("voicemail", "answerphone", "answer machine", "answering machine", "voice mail",
            "leave a message on", "message on his", "message on her", "leave a voicemail",
            "him a message", "her a message", "them a message", "to leave a message",
            "who should i leave", "can i leave a message"),
           ("leave", "leaving", "record", "say", "how", "good", "best", "clear", "tip", "tips",
            "should i", "when")),
          ("Keep it under 20 seconds: your name, your number said slowly and twice, why you rang, "
           "and when you can be reached. \"Hi, it's Sam on 07700 900123 - 07700 900123, about the "
           "boiler. Any time after six is fine.\" The number is the part people replay, so it is "
           "the part to slow down for.")),
    entry("asking-for-a-favour", ("favour", "favor", "big", "friend", "borrow"),
          ("Make it small, specific and easy to refuse: \"Could you water my plants on Tuesday and "
           "Friday? No problem if not.\" Saying what it involves and that they can say no makes people "
           "much more likely to say yes."),
          ask=("favour", "favor")),
    entry("message-cancelling-dinner",
          (("cancel", "cancelling", "canceling", "cancelled", "bail", "bailing"),
           ("dinner", "plans", "tonight", "message", "text", "politely", "friend")),
          ("Say it early, be honest and offer a concrete alternative: \"So sorry, I'm going to have to "
           "cancel tonight — I'm wiped out. Can we do Thursday instead? My treat.\" Don't invent an "
           "illness; a plain reason is easier to forgive."),
          avoid=("always cancels", "keeps cancelling", "keeps canceling", "last minute", "cancels on me")),
    entry("friend-keeps-cancelling",
          (("cancels", "cancelling", "canceling", "canceled", "cancelled", "flakes", "flaking",
            "bails", "bail", "bailing", "bailed", "stands me up", "stood me up"),
           ("always", "keeps", "last minute", "flaky", "again", "all the time", "every time",
            "three times", "twice", "four times", "on me", "plans", "stood me up")),
          ("Say it once, about the pattern rather than the last time: \"We've cancelled three times now "
           "and honestly it's starting to feel like I'm an afterthought. Can we pick a night we'll both "
           "keep?\" Naming the pattern and asking for one firm date keeps it about the diary, not "
           "about her character."),
          ask=("friend", "mate", "she", "he", "they", "her", "him", "plans", "dinner", "pub", "lunch",
               "drink", "meet", "date", "birthday", "night out", "manager", "boss", "colleague",
               "workmate", "supervisor", "meeting", "meetings", "one to one", "one to ones", "1:1",
               "catch up", "catch-up", "our"),
          avoid=("shift", "shifts", "rota", "day off", "days off", "annual leave", "employer",
                 "overtime", "called in",
                 "subscription", "subscriptions", "charged", "bill", "bills", "direct debit", "refund",
                 "contract", "membership", "gym", "payment", "order", "booking", "flight",
                 "on me again", "on me twice", "on me three times", "on me every time"),
          guard=lambda reading: not owns_the_deed(reading)),

    entry("comfort-someone",
          (COMFORT_SAY,
           COMFORT_SITUATIONS + ("upset", "struggling", "hard time", "rough time",
                                 "going through", "devastated", "not coping",
                                 "whos upset", "is upset", "so upset", "really upset",
                                 "upset about", "upset over", "been dumped", "is struggling",
                                 "having a hard time", "having a rough time", "mental health"),
           ("my friend", "my mate", "my friend is", "my friend whos", "my friend has",
            "my friend got", "my friends",
            "my mate is", "my mate whos", "my mate has", "my mate got", "a friend of mine",
            "to my friend", "to my mate", "to her", "to him", "to them", "for my friend",
            "for my mate", "someone i know", "someone whos", "someone who is")),
          _comfort,
          bias=1,
          avoid=("died", "dies", "dying", "death", "dead", "passed away", "passed on",
                 "funeral", "grief", "grieving", "bereaved", "bereavement", "miscarriage",
                 "stillborn", "lost her mum", "lost his mum", "lost her dad", "lost his dad",
                 "lost their mum", "lost their dad", "lost my mum", "lost my dad",
                 "card", "cards",
                 "doctor", "gp", "nurse", "boss", "manager", "employer",
                 "interview", "interviews", "interviewer", "interviewers", "recruiter",
                 "hiring manager", "job application", "cv", "resume",
                 "with me", "at me", "off with me", "annoyed", "ignoring me", "ignores me",
                 "not talking to me", "isnt talking to me", "insulted me", "insulted",
                 "rude to me", "shouted at me", "laughed at me", "picked on me", "bullied me",
                 "mean to me", "offended me", "upset me", "horrible to me", "hurt me",
                 "seems upset", "seems off", "seems distant", "looks upset", "might be upset",
                 "maybe upset", "could be upset", "acts off", "acting off", "seems down",
                 "baby", "babies", "toddler", "newborn", "infant", "child", "children", "kid",
                 "kids", "depressed", "depression"),
          ask=COMFORT_SAY),

    entry("comfort-plainly",
          (("how do i comfort", "how do i console", "how do i cheer", "console",
            "comfort", "comforting", "cheer up", "cheering up", "be there for",
            "what do i say", "what should i say", "what can i say", "what to say",
            "shares bad news", "share bad news", "shared bad news", "shares some bad news",
            "shares news", "tells me bad news", "told me bad news", "tells me something awful",
            "told me something awful", "with bad news", "bad news about", "hard news",
            "when someone has bad news", "when someone had bad news", "someone has bad news",
            "respond to bad news", "reply to bad news", "react to bad news"),
           ("someone", "somebody", "a friend", "a mate", "my friend", "my mate",
            "my best friend", "my sister", "my brother", "my mum", "my mom", "my dad",
            "my son", "my daughter", "my wife", "my husband", "my partner", "my gran",
            "a loved one", "a family member", "a colleague", "people", "a person", "anyone",
            "bad news", "sad news", "hard news")),
          COMFORT_PLAIN,
          avoid=COMFORT_SITUATIONS + ("upset", "struggling", "hard time", "rough time",
                                      "going through", "devastated", "not coping",
                                      "whos upset", "is upset", "so upset", "really upset",
                                      "upset about", "upset over", "been dumped",
                                      "having a hard time", "having a rough time",
                                      "mental health",
                                      "died", "dies", "dying", "death", "dead", "passed away",
                                      "funeral", "grief", "grieving", "bereaved",
                                      "card", "cards", "doctor", "gp", "nurse", "boss",
                                      "manager",
                                      "baby", "babies", "toddler", "newborn", "child",
                                      "children", "kid", "kids", "myself", "my own",
                                      "insulted me", "insulted", "hurt me", "rude to me",
                                      "shouted at me", "laughed at me", "picked on me",
                                      "bullied me", "mean to me", "offended me", "upset me",
                                      "horrible to me", "with me", "at me",
                                      "pregnant", "pregnancy", "expecting", "engaged",
                                      "engagement", "promotion", "promoted", "got the job",
                                      "new job", "passed", "graduated", "won")
                                      + A_BEHAVIOUR_TOWARD_THE_ASKER),

    entry("affect-vs-effect", ("affect", "effect", "difference"),
          ("Affect is usually the verb and effect the noun: the rain affected the game, the rain had "
           "an effect on the game. The exception worth knowing is that you can \"effect a change\", "
           "meaning to bring it about.")),
    entry("fewer-vs-less", ("fewer", "less", "difference"),
          ("\"Fewer\" for things you can count, \"less\" for things you can't: fewer people, fewer cups, "
           "but less water and less time. The one everyday exception is money and time in speech — "
           "\"less than five pounds\" is fine.")),
    entry("how-to-pronounce", ("pronounce", "pronunciation", "word"),
          ("Tell me the word and I'll spell out the sounds syllable by syllable in plain English, "
           "with the stressed part in capitals. If it is a name, I'll say it the way the person "
           "would.")),
    entry("word-count-essay", (("count", "length", "word", "how long", "how many words",
                                "word limit", "long"),
                               ("essay", "essays", "dissertation", "dissertations",
                                "coursework", "report")),
          ("A short essay is usually 1,000–1,500 words, a university one 2,000–3,000, and coursework "
           "will state it. Aim for 10% under the limit; going over is the mistake markers mind."),
          avoid=("plan", "planning", "planned", "spend planning", "outline")),
    entry("write-a-eulogy",
          (("eulogy", "eulogies", "eulogy for my mum", "eulogy for my dad", "eulogy for my nan",
            "reading at the funeral", "speech at the funeral", "speak at the funeral"),
           ("write", "writing", "help", "how", "draft", "start", "opening", "open", "example",
            "examples", "template", "length", "long", "words", "minutes", "what do i say",
            "structure", "include", "add", "read", "reading", "say")),
          _eulogy,
          avoid=("toast", "wedding", "best man", "maid of honour", "birthday", "anniversary",
                 "retirement", "thank you", "card", "cards", "vows",
                 "what time", "what day", "tuesday", "wednesday", "thursday", "friday",
                 "saturday", "sunday", "monday", "parking", "flowers", "coffin", "casket"),
          ask=(("write", "writing", "help", "how", "draft", "template", "examples", "length",
                "long", "words", "minutes", "structure", "start", "opening", "open", "what do i say",
                "say", "include", "nervous", "scared")),
          bias=1),
    entry("write-a-toast", ("speech", "toast", ("wedding", "sisters", "best man", "maid of honour",
                                                "father of the bride", "few words", "write",
                                                "birthday", "70th", "60th", "50th", "retirement",
                                                "leaving do", "anniversary")),
          ("Three minutes, about 450 words, is the length to aim for: a line thanking the people who "
           "got everyone there, one story with a real detail in it that shows what the person is like, "
           "then what they mean to you and a toast. Open with a fact everyone in the room recognises, "
           "then turn it: \"My sister has spent her life fixing animals, so it's a relief she's finally "
           "found one she can train.\" Keep that opening 30 seconds short, and put the sincere bit in "
           "the middle where people aren't braced for it."),
          avoid=("thank you", "thankyou", "card", "cards", "invitation", "invitations",
                 "save the date", "place card", "place cards", "order of service", "vows", "vow",
                 "reading", "readings", "venue", "guest list", "seating", "table plan")),
    entry("thank-you-card-note", (("card", "note", "letter", "message", "text"),
                                  ("thank you", "thankyou", "thank-you", "thanks", "grateful",
                                   "appreciate", "appreciated")),
          THANKS_ANY,
          avoid=("birthday card", "christmas card", "wedding card", "christening card",
                 "wedding message", "christening message", "card game", "cardiff")),
    entry("thanks-for-hospitality",
          (("thank", "thanks", "thank you", "thankyou", "thank-you", "grateful"),
           ("letter", "note", "card", "message", "text", "email", "say", "saying", "write",
            "wording", "words", "meal", "dinner", "lunch", "party", "weekend", "staying",
            "stayed", "host", "hosted", "put me up", "lift", "present", "gift", "flowers",
            "helped me", "help", "wedding")),
          thanks_note,
          ask=("how do i", "how can i", "how should i", "how do you", "what should i say",
               "what do i say", "what to say", "what do i write", "what should i write", "write",
               "writing", "wording", "word", "words", "letter", "note", "card", "message", "text",
               "email", "thank you for the", "thanks for the", "thank them"),
          avoid=("interview", "interviews", "interviewer", "interviewing", "job interview",
                 "panel", "recruiter"),
          bias=1),
    entry("learn-spanish-20-minutes", ("spanish", ("learn", "learning", "language", "months", "six", "minutes")),
          ("Spend the 20 minutes on speaking aloud and short listening, not on apps that only make "
           "you tap words: 10 minutes of a course with audio, 5 of vocabulary you will actually use, "
           "5 of repeating phrases. Twenty minutes every day beats two hours on Sunday, and in six "
           "months you will manage the basics of a trip.")),
    entry("spanish-train-station", ("station", "train", "phrases", ("travel", "spanish")),
          ("¿Dónde está la estación de tren? — \"Where is the train station?\" Useful next to it: ¿A "
           "qué hora sale el próximo tren? for \"what time is the next train?\"."),
          avoid=("italy", "italian", "france", "french", "germany", "german", "portugal",
                 "greece", "spain by", "netherlands", "belgium", "train travel", "by train",
                 "take the train", "get around", "travel around", "travelling around",
                 "rail", "railway", "interrail", "railcard", "tickets", "book a train",
                 "cheap train", "trainline", "high speed",
                 "gym", "gyms", "workout", "work out", "weights", "i train", "exercising")),
    entry("trains-in-italy",
          (("italy", "italian", "trenitalia", "italo", "rome", "florence", "venice", "milan",
            "naples"),
           ("train", "trains", "rail", "by train", "get around", "travel around", "tickets",
            "book", "high speed", "frecciarossa")),
          "Book on Trenitalia, the state operator, or Italo for the other fast line: both sell "
          "online and at the machines in the station, and a ticket bought a week or two ahead is "
          "much cheaper than one bought on the day. The fast Frecciarossa trains do Rome to "
          "Florence in about 1 hour 30, Florence to Venice in about 2 hours, and Rome to Naples in "
          "about 1 hour 10, so Milan, Florence and Rome makes a comfortable week. Regional trains "
          "are cheap and need no reservation but are slow, and a regional ticket bought at a "
          "machine has to be stamped in the small machine on the platform before you get on.",
          avoid=("food", "pizza", "weather", "hotel", "hotels", "flight", "flights", "visa",
                 "passport", "work", "job", "move to", "living in", "rent", "house"),
          bias=1),

    entry("spelling-tricky-word", (("spell", "spelling", "spelt", "spelled", "correct",
                                    "correctly", "written"),
                                   _SPELLING_WORDS),
          _spelling,
          ask=("spell", "spelling", "spelt", "spelled", "correct", "correctly", "written",
               "how do you", "which is", "is it"),
          slips=_SPELLING_SLIPS),
    entry("improve-spelling", (("spelling", "spell", "spelt", "spelled"),
                               ("improve", "better", "learn", "remember", "struggle", "bad",
                                "terrible", "awful", "hopeless", "rules", "good")),
          ("Work from your own mistakes, not a list of hard words: take the twenty words you "
           "actually get wrong in texts and emails, and use look-say-cover-write-check on five a "
           "day - look at it, say it, cover it, write it, check it. Break long words into "
           "syllables as you say them (gov-ern-ment, sep-a-rate), and read your own writing out "
           "loud, because most spelling slips are words you can hear. Spellcheck is fine as a "
           "check, but read the suggestion before you accept it, or the same mistake survives."),
          ask=("improve", "better", "learn", "remember", "struggle", "bad", "terrible", "awful",
               "hopeless", "how do i", "how can i", "help")),
    entry("spelling-pick-one", (("which", "correct", "or"), _SPELLING_SLIPS),
          _spelling,
          ask=("which", "correct", "is it", "or"),
          slips=_SPELLING_SLIPS),

    entry("letter-to-mp",
          (("letter to my mp", "write to my mp", "my mp", "to my mp", "contact my mp",
            "email my mp", "member of parliament", "mps", "councillor", "councillors",
            "mp's"),
           ("write", "writing", "how do i", "how can i", "complain", "contact", "email",
            "what do i say", "who is", "who's", "should i", "get in touch", "reach")),
          ("One page, one issue, one ask. Say who you are and where you live first, with the full "
           "postcode, because an MP can only act for their own constituents; then the problem in "
           "three sentences with the dates, then exactly what you want them to do - change a rule, "
           "chase a department, or write to a minister for you. Attach copies, never originals, and "
           "ask for a reply within four weeks. Address it to the House of Commons, London SW1A "
           "0AA, or find the name and the office email on theyworkforyou.com. A short factual "
           "letter gets an answer from a caseworker; a long angry one gets a standard reply."),
          avoid=("council tax", "mp3", "music", "player", "download", "app", "video",
                 "game", "film", "book", "series"),
          ask=("write", "letter", "how do i", "complain", "contact", "who is", "what do i say")),
]

TALKING_IS_NOT_A_CHAT = ("class", "classes", "classroom", "classrooms", "lesson", "lessons",
                         "lecture", "lectures", "school", "schools", "assembly", "teacher",
                         "teachers", "tutor", "seminar", "in class", "at school", "during class",
                         "exam", "exams", "playground",
                         "meeting", "meetings", "board meeting", "team meeting",
                         "one to one")

ASKING = ("how do i tell", "how do i say", "how do i ask", "how to tell", "how to say",
          "how to ask", "what do i say", "what should i say", "how can i tell", "how can i say",
          "how can i ask", "ways to say", "way to say", "word for", "how do you tell",
          "how do you say", "how would i say", "tell someone", "telling someone",
          "say to someone", "saying to someone", "tell a friend", "tell my friend",
          "tell people", "break it to", "bring it up", "polite way", "politely")

_NOT_A_SIMPLE_NO = ("cant afford", "afford it", "stand up for myself", "second date",
                    "goodbye", "leaving do", "leaving present", "thank you", "condolence",
                    "sympathy", "eulogy", "toast", "wedding speech", "reference", "resign",
                    "notice", "complaint", "refund")

ENTRIES += [
    entry("ask-for-help",
          (("help", "hand", "support", "a favour", "favour", "assistance"),
           ("ask", "asking", "sound", "sounding", "weak", "stupid", "embarrassed", "ashamed",
            "awkward", "burden", "bothering", "admit", "need")),
          ("Name the job, the bit you are stuck on, and the smallest thing that would unstick it, "
           "with a time on it: \"I'm stuck on the last two pages of this report - could you read "
           "them before Friday?\" A specific, finished ask is easy to say yes to, and it reads as "
           "competence rather than weakness; \"can you help me with this\" gives them nothing to "
           "hold on to. If it still feels like a lot, say why you are asking them: they were good "
           "at this, or they have done it before."),
          ask=ASKING + ("sound weak", "sounding weak", "without sounding", "dont want to sound",
                        "feel bad asking", "hate asking", "hate to ask", "hard to ask"),
          avoid=("how do i ask for a favour", "favours", "favor", "reference", "landlord",
                 "boss for", "pay rise", "raise", "extension", "deadline", "lend", "borrow",
                 "money", "lift", "ride", "cv", "resume", "covering letter", "cover letter",
                 "personal statement", "application")),
    entry("ask-for-space",
          (("space", "some room", "room to breathe", "room to think", "room to myself",
            "time alone", "time to myself", "time on my own", "breathing room", "a break"),
           ("need", "needs", "want", "tell", "say", "ask", "asking", "how", "someone", "i need")),
          ("Say it as a need for a few days rather than a verdict on them, and put a date on it so "
           "it cannot sound like leaving: \"I've got a lot on and I need a couple of quiet days - "
           "I'll ring you Thursday.\" Do not explain it as their fault and do not apologise for "
           "it three times; a short clear ask with a return date is the kindest version, and it "
           "gives them something to wait for instead of something to worry about."),
          ask=ASKING + ("i need space", "need some space", "need a bit of space", "time apart"),
          avoid=("flat", "bedroom", "kitchen", "cupboard", "wardrobe", "shed", "office", "desk",
                 "storage", "box room", "car", "van", "parking", "garden", "garage",
                 "paint", "painting", "painted", "repaint", "decorate", "decorating",
                 "decoration", "wallpaper", "plaster", "plastering", "carpet", "flooring",
                 "tiles", "curtains", "blinds", "furniture", "sofa", "shelves", "rug",
                 "lamp", "lights", "tidy", "tidying", "clear out", "clearing", "damp",
                 "sprain", "sprained", "strain", "fracture", "fractured", "broken", "bone",
                 "bones", "wrist", "ankle", "knee", "elbow", "shoulder", "rib", "ribs",
                 "x-ray", "xray", "swelling", "swollen", "injury", "injured", "numb")),
    entry("ask-for-quiet",
          (("quiet", "quieter", "quietly", "noise", "noisy", "loud", "turn it down",
            "keep it down", "lower the volume"),
           ("ask", "asking", "tell", "telling", "say", "saying", "how", "neighbour", "neighbor",
            "flatmate", "roommate", "housemate", "someone")),
          ("Ask once, in private, at a calm time, and make it about the thing and not the person: "
           "\"The telly carries through the wall after eleven - could you turn it down a notch?\" "
           "Give when it happens, how it lands and what would fix it. Do not knock at midnight "
           "while it is loud - the ask that lands is the one made in daylight, and the first ask "
           "should sound like a favour between neighbours, because it is."),
          ask=ASKING + ("be quiet", "be quieter", "keep it down", "turn it down", "less noise"),
          avoid=("dog", "dogs", "barking", "party", "parties", "music", "builders", "drilling",
                 "landlord", "council", "police", "baby", "toddler", "child", "children", "kid",
                 "kids", "son", "daughter", "boss", "manager", "quiet word", "appraisal", "hr",
                 "who is making", "what is that noise", "banging", "alarm",
                 "colleague", "colleagues", "coworker", "coworkers", "co-worker", "co-workers",
                 "workmate", "workmates", "teammate", "teammates", "team mate", "team mates",
                 "at work", "at my desk", "open plan", "in the office", "the office")),
    entry("leave-a-party",
          (("party", "parties", "a do", "gathering", "event", "wedding", "drinks", "dinner",
            "barbecue", "bbq", "celebration", "night out", "house party"),
           ("leave", "leaving", "left", "go home", "going home", "slip away", "slip out",
            "leave early", "get away", "escape", "politely", "without being rude",
            "say goodbye", "say goodbyes", "goodbye", "goodbyes", "say bye", "head off",
            "excuse myself", "excusing myself", "make my excuses", "made my excuses",
            "my excuses")),
          ("Thank the host, mean it, and go: \"It's been lovely - I'm going to head off, thank "
           "you so much.\" Say your goodbyes to the host and the one or two people you actually "
           "spent the evening with, not the whole room, and have your reason ready in one line "
           "(\"early start tomorrow\") because the second question is always why. Leaving at the "
           "natural lull is easier than the big goodbye, and nobody minds nearly as much as the "
           "leaving feels like it will."),
          ask=ASKING + ("leave early", "leave a party", "politely leave", "slip away",
                        "leave without", "get out of a party", "say goodbye", "goodbye",
                        "goodbyes",
                        "excuse myself", "excusing myself", "make my excuses",
                        "made my excuses", "my excuses"),
          avoid=("leaving do", "leaving present", "leaving job", "leaving my job", "resign",
                 "notice", "school", "hotel", "airbnb", "car", "parking", "before it ends",
                 "keys", "flat", "tenancy", "landlord",
                 "on the phone", "phone call", "the phone", "call", "calls", "voicemail")),
    entry("end-a-conversation",
          (("conversation", "chat", "talking", "call", "phone call", "small talk"),
           ("end", "ending", "finish", "finishing", "stop", "get out", "escape", "leave",
            "close", "politely", "how")),
          ("Close it with a reason and a warm line, then move: \"I'll let you go - it's been "
           "really good to catch up.\" Turning it round to them is the trick, because \"I'll let "
           "you get back to it\" ends the call without anyone being brushed off. In person, say "
           "one thing you want to come back to (\"I want to hear how the move went - let's get a "
           "coffee next week\"), then go; a promise to continue is what makes leaving feel "
           "friendly rather than rude."),
          ask=ASKING + ("end a conversation", "end the conversation", "stop talking",
                        "get out of a conversation", "politely end", "politely get away",
                        "end a chat", "end the chat", "how do i end", "how to end",
                        "how do i get out"),
          avoid=("meeting", "presentation", "interview", "argument", "row", "relationship",
                 "break up", "landlord", "contract", "phone contract", "paid", "bill",
                 "stop calling", "stop texting", "stop messaging", "keeps calling",
                 "block", "blocked", "blocking", "unwanted calls", "spam", "cold callers",
                 ) + TALKING_IS_NOT_A_CHAT,
          bias=1),
    entry("console-someone",
          (("console", "comfort", "sympathy", "condolence", "condolences", "cheer up",
            "make them feel better", "say to someone"),
           ("someone", "friend", "grieving", "bereaved", "loss", "lost", "died", "death",
            "dying", "crying", "upset", "hurt", "bad news", "how", "what")),
          ("Say the plain thing and then be quiet: \"I'm so sorry - I don't have words, but I'm "
           "here.\" Name the person who died if they have named them, say their name back, and "
           "offer one concrete thing instead of \"let me know if you need anything\": a lift, a "
           "meal on Thursday, sitting with them. Do not explain, compare it to your own loss, or "
           "look for the bright side; the comfort is in staying, and in being the one who is "
           "still there in three weeks."),
          ask=ASKING + ("console someone", "comfort someone", "what do i say to",
                        "what to say when someone", "cheer someone up"),
          avoid=("child", "children", "kid", "kids", "dog", "cat", "pet", "bereavement leave",
                 "funeral cost", "funeral flowers", "eulogy", "obituary", "death certificate",
                 "probate", "will", "inheritance", "what to wear")),
    entry("apologise-to-a-customer",
          (("customer", "client", "customer service", "complaint", "complaining", "review",
            "reviewer", "client"),
           ("apologise", "apologize", "apology", "sorry", "how", "say", "write", "respond",
            "reply", "answer", "bad", "unhappy", "angry", "upset")),
          ("Name what happened, own it once, say what you are doing and by when, and leave your "
           "process out of it: \"I'm sorry - we sent the wrong size twice, and that's on us. The "
           "right one goes out today on next-day delivery.\" One apology is enough; explaining "
           "the system reads as an excuse, and asking them to do the work reads as a second "
           "failure. If it is a public review, answer in two sentences and move the detail to "
           "email."),
          ask=ASKING + ("apologise to a customer", "apologize to a customer", "sorry to a customer",
                        "reply to a bad review", "respond to a complaint", "answer a complaint",
                        "apologise to a client"),
          avoid=("refund", "guarantee", "warranty", "legal", "sue", "ombudsman", "trading standards",
                 "tell a customer no", "tell customers no", "say no", "saying no", "turn down",
                 "refuse", "decline", "price", "quote", "delay", "late", "waiting",
                 "small claims", "compensation", "my landlord", "my boss", "my colleague",
                 "my friend", "my partner", "my wife", "my husband", "my mum", "my dad")),
]

ENTRIES += [
    entry("thanks-for-a-gift",
          (("present i dont like", "present i don't like", "gift i dont like",
            "gift i don't like", "present i hate", "gift i hate", "already have it",
            "already got one", "wrong size", "ugly present", "ugly gift", "bad present",
            "bad gift", "didnt like the present", "didn't like the present",
            "didnt like the gift", "didn't like the gift", "someone gives me", "gives me a gift",
            "gave me a present", "gave me a gift", "thank you for a present",
            "thank you for the present", "thank you note", "thank you card",
            "thank you letter", "thank someone for a gift", "what do i say when someone gives me"),
           ("present", "gift", "presents", "gifts", "thank", "thanks", "say", "write",
            "reply", "respond", "polite", "politely", "card", "note", "letter", "how", "what")),
          ("Say the thanks and mean that part, in one line, and do not name the thing: \"Thank "
           "you - it was so kind of you to think of me.\" If you will use some of it, say how - "
           "\"the scarf is going straight on tomorrow\" - and if you will not, say nothing about "
           "it and thank them again later for the thought. Ask for the receipt only from someone "
           "close, and only when the thing was expensive: \"It's lovely but the size is wrong - "
           "could I swap it?\" Nobody is owed the truth about a present."),
          ask=("say", "said", "saying", "write", "reply", "respond", "thank", "thanks", "what",
               "how", "words", "message", "text", "card", "note", "letter")),

    entry("asked-if-pregnant",
          (("are you pregnant", "if i am pregnant", "if im pregnant", "if i'm pregnant",
            "asks if i am pregnant", "asked if i am pregnant", "asking if i am pregnant",
            "asks if im pregnant", "asked if im pregnant", "do you think i am pregnant",
            "when are you due", "when is the baby due", "when is your baby due",
            "any news", "is there a baby", "are you expecting", "asks if i am expecting",
            "asked if i am expecting", "asking about a baby", "asks about a baby"),
           ("say", "said", "saying", "reply", "respond", "answer", "how", "what", "words",
            "someone", "people", "asks", "asked", "asking", "relative", "relatives", "mum",
            "mother", "mother in law", "colleague", "colleagues", "aunt", "friend")),
          ("One easy line closes it, and you do not owe anyone more than that: \"No - I've just "
           "had a big lunch.\" If it keeps coming, or it is someone who should know better, name "
           "it once and flatly: \"I'd rather not talk about that.\" You do not have to explain "
           "whether you are trying, whether it happened and did not last, or whether you have "
           "decided not to - and you can say exactly that: \"that's not something I talk about.\" "
           "Then change the subject to them, which is what most people want anyway."),
          ask=("say", "said", "saying", "reply", "respond", "answer", "how", "what", "words",
               "someone", "people", "asks", "asked", "asking")),
]


LEAVING_SPEECH = (
    "Three short parts, three minutes at most: say who you are and why you are the one talking, "
    "give one concrete thing you will miss about them - a habit, a phrase, a thing they always "
    "fixed - and end with the room raising a glass. Write it out in full sentences and then cut it "
    "in half: the best version is two clean stories and a line about what they were like to work "
    "with. Name two or three people who are in the room and thank them for something specific, and "
    "finish on a toast like 'to Priya' rather than a thank-you to everyone, which always sounds "
    "like a wedding.")

ENTRIES.append(entry(
    "leaving-speech",
    (("speech", "speeches", "toast", "few words", "say a few words", "stand up and say",
      "say at a leaving", "say at the leaving", "say at my leaving", "say at a farewell",
      "say at the retirement", "words at a leaving"),
     ("leaving do", "leaving party", "leaving drinks", "leaving", "leaving us", "leaving work",
      "last day", "farewell", "goodbye", "send off", "retirement", "retiring", "colleague",
      "team", "boss", "work", "thank you", "thanks", "tribute")),
    LEAVING_SPEECH,
    ask=("speech", "speeches", "toast", "say", "words"),
    avoid=("card", "cards", "message", "sign", "resignation", "resign", "notice", "letter",
           "email", "wedding", "bride", "groom", "best man", "father of the bride",
           "funeral", "eulogy", "death", "died", "passed away", "birthday", "anniversary",
           "maid of honour", "speech to text", "speech delay", "speech therapy",
           "figure of speech"),
    bias=2))


A_JOB_LEFT_UNDONE = (
    "two goes", "two cycles", "two washes", "two loads", "three goes", "three cycles",
    "three washes", "took two", "takes two", "went through twice", "put it through twice",
    "still wet", "still damp", "leaves everything damp", "leaves the clothes damp",
    "leaves clothes damp", "leaves them damp", "leave everything damp", "come out damp",
    "comes out damp", "come out wet", "comes out wet", "doesnt dry", "doesn't dry", "isnt drying",
    "isn't drying", "not drying", "never dries", "doesnt finish", "doesn't finish", "not finishing",
    "doesnt cook", "doesn't cook", "undercooked", "comes out raw", "not hot enough",
    "takes ages", "taking ages", "takes forever", "taking forever", "taking hours", "takes hours",
    "taking so long", "takes so long", "taking all day", "takes all day", "long to dry",
    "slow to dry", "drying slowly", "dries slowly", "hours to dry", "all night to dry",
)
