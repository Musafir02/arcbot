import re
import string

from bot.memory import facts

NUMBER_AHEAD = re.compile(
    r"\b(?P<n>a couple of|a pair of|couple of|pair of|one|two|three|four|five|six|seven|eight|"
    r"nine|ten|eleven|twelve|\d{1,2})\s+"
    r"(?:(?:more|other|elder|older|younger|little|lovely|grown|grown-up|step|half|"
    r"foster|adopted|healthy|beautiful|new|old)\s+){0,2}"
    r"(?P<who>[a-z][a-z-]{2,})\b", re.I)
THEY_HAVE = re.compile(
    r"\b(?:i|we)(?:\s+have|'ve|ve|\s+got|\s+have got|\s+own)\s+(?P<rest>[^.!?]{0,48})", re.I)
MY_THREE = re.compile(
    r"\b(?:my|our)\s+(?P<rest>(?:a couple of|a pair of|couple of|pair of|one|two|three|four|"
    r"five|six|seven|eight|nine|ten|eleven|twelve|\d{1,2})\b[^.!?]{0,40})", re.I)

CORRECTED = re.compile(
    r"^\W*(?:no|nope|sorry|actually|wait|i mean|make that|oops|correction|sorry, no)\b"
    r"[\s,]*"
    r"(?:(?:make|change|put)\s+(?:that|it)(?:\s+to)?|its|it's|to)?\s*"
    r"((?:a couple of|a pair of|one|two|three|four|five|six|seven|eight|nine|ten|"
    r"eleven|twelve|\d{1,2})\b[^.!?]{0,32})$", re.I)
_SUBJECT_AFTER = (r"(?:i|you|we|they|he|she|it|there|that|this|these|those|any|some|"
                  r"my|your|our|their|his|her|its)\b")
ASKING = re.compile(r"^\W*(?:(?:do|did|does|have|has|are|is|was|were|can|could|would|should|"
                    r"will)\s+" + _SUBJECT_AFTER + r"|how|what|which|who|when|where|why)\b",
                    re.I)

IRREGULAR = {"children": "child", "people": "person", "men": "man", "women": "woman",
             "grandchildren": "grandchild", "grandkids": "grandkid", "nieces": "niece",
             "nephews": "nephew", "mice": "mouse", "geese": "goose", "feet": "foot",
             "teeth": "tooth", "oxen": "ox", "wives": "wife", "lives": "life",
             "knives": "knife", "shelves": "shelf", "wolves": "wolf", "halves": "half"}
THEIRS = frozenset("""cat cats dog dogs puppy puppies kitten kittens rabbit rabbits bunny
bunnies hamster hamsters fish horse horses pony ponies parrot parrots pet pets animal animals
kid kids child children baby babies son sons daughter daughters""".split())
NOT_A_THING = frozenset("""minutes minute hours hour days day weeks week months month years year
o'clock pounds pound quid euros euro dollars dollar pence pennies percent times time
years-old oclock weeks-old months-old miles mile kilometres km kilos kilo pounds-weight
stone stones stones-weight left right quarter quarters third fourth fifth half halves dozen
litres litre pints pint ounces ounce grams kilo kilos""".split())

GROUP_NUMBER = (r"a couple of|a pair of|couple of|pair of|one|two|three|four|five|six|seven|"
                r"eight|nine|ten|eleven|twelve|\d{1,2}")
_GROUP_TAIL = (r"(?=\s*(?:$|[,.!?;:]|\b(?:here|now|at home|in the house|in the flat|"
               r"in the home|in total|altogether|total|and|but|so)\b))")
GROUP_OF_US = re.compile(
    r"\b(?:(?:there|it)\s*(?:'s|s|'re|re|are|is|'ll|ll|will|would)|"
    r"we\s*(?:'re|re|are|'ll|ll|will))\s+"
    r"(?:(?:going to be|gonna be|will be|would be|should be|be)\s+)?"
    r"(?:(?:just|only|now|still|currently|actually)\s+){0,2}"
    r"(?:the\s+)?(?P<n>" + GROUP_NUMBER + r")\s+of us\b" + _GROUP_TAIL +
    r"|\b(?:we\s*(?:'re|re|are)|there\s*(?:'s|s|'re|re|are|is))\s+"
    r"(?:(?:just|only|now|still|currently|actually)\s+){0,2}"
    r"(?P<n2>" + GROUP_NUMBER + r")\s+(?:people|persons?)\b" + _GROUP_TAIL +
    r"|^\W*(?:(?:and|so|well|ok|okay|oh|hmm)\b[,.]?\s+)*(?:(?:just|only)\s+)?(?:the\s+)?"
    r"(?P<n3>" + GROUP_NUMBER + r")\s+of us\b" + _GROUP_TAIL, re.I)
GROUP_CORRECTED = re.compile(
    r"^\W*(?:no|nope|sorry|actually|wait|i mean|make it|make that|hold on|hang on|correction)\b"
    r"[^.!?]{0,12}?(?:the\s+)?(?P<n>" + GROUP_NUMBER + r")\s+of us\b", re.I)
GROUP_OF_FOUR = re.compile(
    r"\b(?:family|household)\s+of\s+(?P<n>" + GROUP_NUMBER + r")\b(?!\s+[a-z])", re.I)

_GROUP_ASK_WORDS = (r"(?:are|is|were|was|there|here|now|altogether|total|in all|at home|"
                    r"it|that|again|then|did i say|did we say|do you remember|remind me|"
                    r"in the house|in the flat|in the home|in my (?:house|flat|home|household)|"
                    r"in our (?:house|flat|home|household)|live here|living here|"
                    r"live in the (?:house|flat|home)|living in the (?:house|flat|home))")
_GROUP_POINTER = r"(?:is it|was it|were they|is that|was that|again|then|did i say|did we say|i say)"

_GROUP_TAIL = _GROUP_ASK_WORDS + r"|" + _GROUP_POINTER

GROUP_ASK = re.compile(
    r"\bhow many of us(?:\s+(?:" + _GROUP_TAIL + r"))*\s*[?.!]*$"
    r"|\bhow many people(?:\s+(?:" + _GROUP_TAIL + r"))*\s*[?.!]*$"
    r"|\bhow (?:big|large) (?:is|are) (?:my|our|the) (?:family|household)\b", re.I)
GROUP_ASK_YOU = re.compile(
    r"\bhow many of (?:you|u)(?:\s+(?:" + _GROUP_ASK_WORDS + r"|" + _GROUP_POINTER + r"))*"
    r"\s*[?.!]*$"
    r"|\bhow many of (?:you|u) (?:live|living|are living)"
    r"(?:\s+(?:there|here|at home|now|altogether))?\s*[?.!]*$", re.I)
BARE_GROUP_ASK = re.compile(
    r"\bhow many (?:are|is|were|was) (?:coming|going|expected|there)"
    r"(?:\s+(?:then|now|again|altogether|in total))?\s*[?.!]*$", re.I)

BARE_COUNT_ASK = re.compile(
    r"\bhow many\s+(?:was|is|were|are)\s+(?:it|that|there)"
    r"(?:\s+(?:again|then|now|altogether|in total))?\s*[?.!]*$"
    r"|\bhow many again\b\s*[?.!]*$"
    r"|\A\W*how many\W*[?.!]*$", re.I)

GROUP = "us"

TABLE_MEAL = (r"roast|dinner|supper|tea|lunch|breakfast|meal|barbecue|bbq|barbeque|party|"
              r"spread|buffet|feast|brunch|carvery")
_A_DAY = (r"monday|tuesday|wednesday|thursday|friday|saturday|sunday|mon|tues|tues|tue|weds|"
          r"wed|thurs|thur|thu|fri|sat|sun|weekend|tonight|tomorrow|today")
BARE_NUMBER = GROUP_NUMBER + r"|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|"
BARE_NUMBER += (r"twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|a hundred|one hundred|"
                r"\d{1,3}")
PARTY = re.compile(
    r"\b(?:for|having|expecting|feeding|cooking for|catering for|a table for|table for|"
    r"booking for|booked for|party for|dinner for|lunch for|tea for|supper for|seats? for|"
    r"invited|inviting)\s+(?:the\s+|just\s+|only\s+)?(?P<n>" + GROUP_NUMBER + r")\s+"
    r"(?:people|persons?|guests?|adults?|heads?|folk|friends|kids|children)\b"
    r"|\b(?P<n2>" + GROUP_NUMBER + r")\s+"
    r"(?:people|persons?|guests?|adults?|heads?|friends)\s+"
    r"(?:coming|over|round|for|at|on)\b"
    r"|\b(?P<n4>" + GROUP_NUMBER + r")\s+of us\s+"
    r"(?:(?:coming|over|round)\b|for\s+(?!(?:a|an|the|good|now|once|ages|keeps|ever)\b)[a-z])"
    r"|\b(?P<n7>" + GROUP_NUMBER + r")\s+of us\s+(?:on|this|next)\s+(?:the\s+)?"
    r"(?:" + _A_DAY + r")\b"
    r"|\b(?:a table for|table for|booking for|booked for|reservation for)\s+"
    r"(?P<n3>" + GROUP_NUMBER + r")\b(?!(?:\s*(?:minutes?|hours?|days?|weeks?|months?|years?|"
    r"courses?)\b))"
    r"|\b(?:cooking for|catering for|feeding|having over|having round)\s+"
    r"(?P<n6>" + GROUP_NUMBER + r")\b(?!(?:\s*(?:minutes?|hours?|days?|weeks?|months?|years?|"
    r"courses?|of them)\b))"
    r"|\b(?:" + TABLE_MEAL + r")\b[^.?!]{0,24}?\bfor\s+(?:the\s+|just\s+|only\s+)?"
    r"(?P<n5>" + BARE_NUMBER + r")\b(?!(?:\s*(?:minutes?|hours?|days?|weeks?|months?|years?|"
    r"courses?|more|less|pounds?|quid|euros?|dollars?|kg|kilos?|grams?|litres?|pints?|miles?|"
    r"metres?|o'clock)\b))", re.I)
PARTY_ASK = re.compile(
    r"\bhow many (?:people|persons?|guests?|heads?|adults?)\b\s*"
    r"(?:$|[,.!?;:]|\b(?:again|then|though|is it|is that|are coming|coming|was it|was that|"
    r"you think|do you think|do i need|do i cook|am i cooking|we having|did i say|did we say)\b)"
    r"|\bhow many (?:are|is) (?:coming|it for|we having|we cooking for|we expecting)\b"
    r"|\bhow many did i say\b"
    r"|\bhow many (?:did|have) (?:i|we) (?:book|booked|reserve|reserved|ask for|asked for)\b"
    r"|\bhow many is (?:the|that|this|my|our) (?:table|booking|reservation) for\b"
    r"|\bhow many (?:am|are|was|were) (?:i|we) (?:cooking|baking|making|catering|feeding|"
    r"preparing|planning|doing)\b[^.?!]{0,18}?\bfor\b"
    r"|\bhow many (?:do|did|will) (?:i|we) (?:cook|bake|make|cater|feed|prepare|plan) for\b",
    re.I)
CHANGED = re.compile(r"\b(?:actually|instead|now|sorry|hang on|one more|another|extra|"
                     r"make that|no)\b", re.I)
CHANGED_BARE = re.compile(
    r"\b(?:make it|make that|put it at|change it to|change to|actually|sorry|no|instead|"
    r"lets say|let's say|now)\b[\s,]*"
    r"(?:it\s+)?(?:to\s+|at\s+)?(?P<n>" + GROUP_NUMBER + r")\b"
    r"(?:\s*,?\s*(?:people|persons?|guests?|heads?|adults?|of us|now|instead|please|thanks|"
    r"after all))*\s*[.!]*$", re.I)
NOW_THE_NUMBER = re.compile(
    r"\b(?:we|there)\s*(?:'s|'re|re|are|is|s)?\s+(?:now\s+)?(?P<n>" + GROUP_NUMBER + r")\s+"
    r"(?:of us\s+)?now\b", re.I)
ONE_MORE = re.compile(
    r"^\W*(?:and\s+|oh\s+|plus\s+)?(?:one|1)\s+more"
    r"(?:\s+(?:is\s+coming|is\s+coming\s+now|coming|now|person|guest|guest\s+is\s+coming|"
    r"of\s+us|of\s+them))?\s*[.!]*$", re.I)
ONE_LESS = re.compile(
    r"^\W*(?:and\s+|oh\s+)?(?:one|1)(?:\s+of\s+(?:them|the\s+guests?|the\s+group))?\s+"
    r"(?:less|cant\s+come|cannot\s+come|can't\s+come|"
    r"isnt\s+coming|isn't\s+coming|is\s+not\s+coming|has\s+dropped\s+out|dropped\s+out|"
    r"cant\s+make\s+it|can't\s+make\s+it)"
    r"(?:\s+(?:now|after\s+all|anymore|any\s+more))?\s*[.!]*$", re.I)
ABOUT_THE_HOUSE = re.compile(r"\b(?:at home|in the house|in the flat|in the home|live|lives|"
                             r"living|living here|household|family|house)\b", re.I)
POINTS_AT_A_NUMBER = re.compile(r"\b(?:again|was it|was that|is it for|did i say|did we say|"
                                r"do you remember|remind me)\b", re.I)
PARTY_THING = "person"

LOOK_BACK_FOR_A_MEAL = 6

BARE_PEOPLE = re.compile(
    r"\b(?:(?:about|around|roughly|maybe|probably|just|only|some|like)\s+)?(?P<n>" + BARE_NUMBER +
    r")\s+(?:people|persons?|guests?|adults?|heads?|folk)\b", re.I)
A_MEAL_IN_THE_CHAT = re.compile(
    r"\b(?:" + TABLE_MEAL + r"|cake|cakes|bake|baking|cooking|cook|menu|scones?|birthday|"
    r"buffet|canapes|finger food)\b", re.I)


PHRASE_ENDS = frozenset("""called named of and but with for to in at on from by near who that
which because so then when if about today tomorrow yesterday tonight now ago already still here
there not no only just instead rather than""".split())
CHAT_JOINERS = frozenset("n nd".split())
MAX_PHRASE = 3
VERB_IN_PHRASE = frozenset("""live lives are is was were be been am come comes go goes went
have has had do does did get gets got make makes made take takes need needs want wants eat eats
ate cost costs work works stays stay move moves play plays run runs see saw know knows think
thinks feel feels look looks seem seems sit sits speak speaks grow grows cost""".split())


def _many(n):
    for word, value in facts.PET_COUNT_WORDS.items():
        if value == n and " " not in word:
            return word
    return str(n)


def _head(after):
    phrase = []
    for word in str(after or "").lower().split()[:MAX_PHRASE]:
        word = word.strip(string.punctuation + "\u2019")
        if not word.isalpha() or word in PHRASE_ENDS or word in CHAT_JOINERS:
            break
        if word in facts.PET_COUNT_WORDS:
            break
        if word in VERB_IN_PHRASE or word.endswith(("ly", "ing")):
            break
        phrase.append(word)
    return phrase


RELATION_AHEAD = frozenset(("grand", "step", "half", "foster", "adopted", "adoptive", "ex",
                            "surrogate"))
A_PERSON_TAIL = ("child", "kid", "son", "daughter", "aunt", "uncle", "niece", "nephew",
                 "parent", "mother", "father", "grandma", "grandad", "granddaughter",
                 "grandson", "gran", "nan", "dad", "mum")


def _the_relation(phrase):
    if not phrase:
        return ""
    thing = _thing(phrase[-1])
    if not thing or len(phrase) < 2:
        return thing
    before = phrase[-2]
    if before in RELATION_AHEAD:
        return before + " " + thing
    if before == "great" and thing.endswith(A_PERSON_TAIL):
        return "great " + thing
    return thing


def _thing_of(phrase):
    return _the_relation(_head(phrase))


def _thing(word):
    word = str(word or "").lower().strip("-")
    if not word or word in NOT_A_THING or len(word) < 3:
        return ""
    if word in IRREGULAR:
        return IRREGULAR[word]
    if word.endswith("ies") and len(word) > 4:
        return word[:-3] + "y"
    if word.endswith(("ches", "shes", "sses", "xes", "zes")):
        return word[:-2]
    if word.endswith("s") and not word.endswith(("ss", "us", "is")):
        return word[:-1]
    return word


def _beds(rest):
    line = " ".join(str(rest or "").split())
    words = line.lower().split()
    for match in BEDS.finditer(line):
        said = match.group("n").lower()
        number = int(said) if said.isdigit() else facts.PET_COUNT_WORDS.get(said, 0)
        if not 0 < number <= 20:
            continue
        after = line[match.end():].strip(string.punctuation).split()
        if match.group("join").strip() == "-" or after or any(
                word in A_KIND_OF_PLACE for word in words):
            return number
    return 0


BEDS = re.compile(
    r"\b(?P<n>" + GROUP_NUMBER + r")\s*(?P<join>-?)\s*bed(?:room)?s?\b", re.I)
A_KIND_OF_PLACE = frozenset("""house home flat place bungalow maisonette semi terrace terraced
cottage apartment rental rented bedsit studio pad maisonette maisonettes""".split())
A_MEASURE_WORD = frozenset("bed beds bedroom bedrooms".split())


_NUM_WORD = r"(?:a couple of|a pair of|one|two|three|four|five|six|seven|eight|nine|ten|\d{1,3})"
NOT_A_COUNT = frozenset("""degrees degree percent miles mile km kms kilometres kilometers metres
meters cm mm kg kgs lbs lb oz litres liters ml celsius fahrenheit mph kph""".split())
A_RANGE_AROUND = re.compile(
    r"\bbetween\b[^.!?]{0,14}?" + _NUM_WORD + r"[^.!?]{0,10}?\band\b"
    r"|" + _NUM_WORD + r"\s*(?:-|\u2013|to|or)\s*" + _NUM_WORD, re.I)


def _counted(rest):
    found = {}
    rest = str(rest or "")
    for match in NUMBER_AHEAD.finditer(" " + rest):
        window = rest[max(0, match.start("n") - 16):match.end("who") + 12]
        if A_RANGE_AROUND.search(window):
            continue
        tail = rest[match.start("who") - 1:]
        if "," in tail:
            tail = tail.split(",", 1)[0]
        phrase = _head(tail)
        if any(word in NOT_A_THING for word in phrase):
            continue
        thing = _the_relation(phrase)
        if not thing or thing in THEIRS or thing.split()[-1] in THEIRS:
            continue
        if len(phrase) > 1 and phrase[0] in A_MEASURE_WORD:
            continue
        said = match.group("n").lower()
        number = int(said) if said.isdigit() else facts.PET_COUNT_WORDS.get(said, 0)
        if number > 0:
            found[thing] = number
    return found


_BIGGER_NUMBERS = {"eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
                   "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20,
                   "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70,
                   "eighty": 80, "ninety": 90, "a hundred": 100, "one hundred": 100,
                   "a dozen": 12, "dozen": 12}


def _said_number(said):
    said = str(said or "").lower().strip()
    if said.isdigit():
        return int(said)
    found = facts.PET_COUNT_WORDS.get(said)
    if isinstance(found, int):
        return found
    return _BIGGER_NUMBERS.get(said, 0)


def _the_group(said):
    for pattern in (GROUP_OF_US, GROUP_OF_FOUR, GROUP_CORRECTED):
        for match in pattern.finditer(said):
            number = _said_number(match.group("n") or match.group("n2")
                                  or match.group("n3"))
            if number > 0:
                return number
    return 0


def _the_party(said):
    for match in PARTY.finditer(said):
        number = _said_number(match.group("n") or match.group("n2") or match.group("n3")
                          or match.group("n4") or match.group("n5")
                          or match.group("n6") or match.group("n7"))
        if number > 0:
            return number
    return 0


A_TABLE_BOOKED = re.compile(
    r"\b(?:book(?:ed|ing|ings)?|reserv(?:ed|ing|ation|ations))\b[^.]{0,24}\btables?\b"
    r"|\btables?\b[^.]{0,12}\bfor\s+(?:\d+|two|three|four|five|six|seven|eight|nine|ten|eleven|"
    r"twelve)\b"
    r"|\b(?:book(?:ed|ing)?|reserved)\b\s+(?:for\s+)?(?:\d+|two|three|four|five|six|seven|eight|"
    r"nine|ten|eleven|twelve)\b", re.I)


def _the_chat_lines(memory):
    lines = [str(((memory or {}).get("user") or {}).get("plan") or "")]
    lines += [str(turn.get("user") or "") for turn in ((memory or {}).get("turns") or [])
              if isinstance(turn, dict)][-LOOK_BACK_FOR_A_MEAL:]
    return lines


def _the_chat_feeds_people(memory):
    return any(A_MEAL_IN_THE_CHAT.search(line) for line in _the_chat_lines(memory))


A_TABLE_CUE = re.compile(
    r"\b(?:people|persons?|guests?|adults?|heads?|folk|friends|kids|children)\b"
    r"[^.]{0,16}\b(?:coming|over|round)\b"
    r"|\b(?:for|having|expecting|feeding|catering for|cooking for|invited|inviting)\s+"
    r"(?:the\s+|just\s+|only\s+)?(?:" + GROUP_NUMBER + r")\b", re.I)


def _the_chat_sets_a_table(memory):
    lines = _the_chat_lines(memory)
    return any(A_MEAL_IN_THE_CHAT.search(line) or A_TABLE_BOOKED.search(line)
               or A_TABLE_CUE.search(line) for line in lines)


def _the_bare_people(said):
    for match in BARE_PEOPLE.finditer(said):
        number = _said_number(match.group("n"))
        if number > 0:
            return number
    return 0


def _the_number_put_right(said, memory):
    held = ((memory or {}).get("user") or {}).get("how_many")
    held_party = held.get(PARTY_THING) if isinstance(held, dict) else None
    if not isinstance(held_party, int) or held_party <= 0:
        return 0
    if ABOUT_THE_HOUSE.search(said):
        return 0
    if ONE_MORE.match(said):
        return held_party + 1
    if ONE_LESS.match(said):
        return held_party - 1 if held_party > 1 else 0
    for pattern in (CHANGED_BARE, NOW_THE_NUMBER):
        for match in pattern.finditer(said):
            number = _said_number(match.group("n"))
            if number > 0:
                return number
    return 0


A_FIGURE = re.compile(r"\b(?P<n>" + GROUP_NUMBER + r")\b", re.I)
SAID_AS_A_CHANGE = re.compile(
    r"\b(?:actually|instead|now|sorry|wait|hold on|make (?:it|that)|change|put it at|no|nope|"
    r"correction|then|after all|not|still|only)\b", re.I)
POINTS_AT_THE_THING = re.compile(r"\bof (?:them|those|these|it)\b", re.I)
A_LABEL_IN_FRONT = frozenset("""number no nos num bus train flight room flat gate platform
seat table lane door channel code pin model version series episode chapter page line half
quarter past o'clock oclock platform route size step floor grade level class year""".split())
COUNTS_THE_THING_AFTER = frozenset("""of now then instead too as well please thanks again
still only just left to go more another""".split())
A_DUMMY_SUBJECT = frozenset("""its it's it thats that's theres there's""".split())
A_COPULA = re.compile(r"\b(?P<subj>[a-z][a-z'-]*)\s+(?:is|are|was|were|be|being)\s*$", re.I)


def _forms_of(thing):
    thing = str(thing or "")
    if not thing:
        return frozenset()
    forms = {thing, thing + "s", thing + "es"}
    for plural, single in IRREGULAR.items():
        if single == thing:
            forms.add(plural)
    return frozenset(forms)


def _the_figure_counts_the_thing(said, match, after_word, thing):
    before = said[:match.start("n")].strip(string.punctuation + " ")
    front = before.split()[-1].lower().strip(string.punctuation) if before else ""
    if front in A_LABEL_IN_FRONT:
        return False
    subject = A_COPULA.search(before)
    if subject and subject.group("subj").lower() not in _forms_of(thing) \
            and subject.group("subj").lower() not in ("it", "there", "that", "this"):
        return False
    if after_word not in _forms_of(thing):
        first = said.split()[0].lower().strip(string.punctuation) if said.split() else ""
        if first in A_DUMMY_SUBJECT:
            return False
    if after_word in COUNTS_THE_THING_AFTER or not after_word:
        return True
    return after_word in _forms_of(thing)


def _the_lines(memory):
    turns = memory.get("turns") if isinstance(memory, dict) else None
    said = []
    for turn in turns if isinstance(turns, list) else ():
        line = str((turn or {}).get("user") or "") if isinstance(turn, dict) else ""
        if line.strip():
            said.append(line)
    return said


def _the_thing_in_hand(memory, held):
    for line in reversed(_the_lines(memory)):
        for thing in _counted(line):
            if isinstance(held.get(thing), int):
                return thing
    return ""


WRONG_NUMBER_AFTER = re.compile(
    r"\W*\b(?:not|instead of|rather than|no longer|as opposed to)\b", re.I)


def _the_figure_that_stands(said):
    match = WRONG_NUMBER_AFTER.search(said)
    if not match:
        return said
    kept = said[:match.start()].strip()
    return kept if A_FIGURE.search(kept) else said


def _a_figure_for_a_thing_the_chat_counts(said, memory, already=()):
    held = ((memory or {}).get("user") or {}).get("how_many")
    if not isinstance(held, dict) or not held:
        return {}
    if "?" in said or ASKING.match(said) or NOT_THE_COUNT.search(said):
        return {}
    said = _the_figure_that_stands(said)
    figures = [match.group("n") for match in A_FIGURE.finditer(said)]
    if len(figures) != 1:
        return {}
    number = _said_number(figures[0])
    if number <= 0:
        return {}
    named = [thing for thing in _counted(said) if thing in held]
    if named:
        thing = named[0]
    elif POINTS_AT_THE_THING.search(said) or SAID_AS_A_CHANGE.search(said):
        match = A_FIGURE.search(said)
        after = said[match.end("n"):].strip(string.punctuation + " ")
        word = after.split()[0].lower() if after else ""
        word = word.strip(string.punctuation)
        if already:
            return {}
        if word in NOT_A_THING or word in NOT_A_COUNT:
            return {}
        thing = _the_thing_in_hand(memory, held)
        if not _the_figure_counts_the_thing(said, match, word, thing):
            return {}
    else:
        return {}
    if not thing or held.get(thing) == number:
        return {}
    return {thing: number}


def observe(text, memory):
    if not isinstance(text, str) or not isinstance(memory, dict):
        return
    said = " ".join(text.split())
    if not said or ASKING.match(said):
        return
    counts = {}
    beds = _beds(said)
    if beds:
        counts["bedroom"] = beds
    group = _the_group(said)
    if group:
        counts[GROUP] = group
    party = _the_party(said)
    if party:
        counts[PARTY_THING] = party
    elif _the_number_put_right(said, memory):
        counts[PARTY_THING] = _the_number_put_right(said, memory)
    elif _the_chat_feeds_people(memory) and _the_bare_people(said):
        counts[PARTY_THING] = _the_bare_people(said)
    elif group and CHANGED.search(said) and not ABOUT_THE_HOUSE.search(said):
        held_party = ((memory.get("user") or {}).get("how_many") or {}).get(PARTY_THING)
        if isinstance(held_party, int):
            counts[PARTY_THING] = group
    put_right = CORRECTED.match(said)
    if put_right:
        counts.update(_counted(put_right.group(1)))
    for pattern in (THEY_HAVE, MY_THREE):
        for match in pattern.finditer(said):
            rest = match.group("rest")
            for thing, number in _counted(rest).items():
                counts.setdefault(thing, number)
    for thing, number in _a_figure_for_a_thing_the_chat_counts(said, memory, counts).items():
        counts.setdefault(thing, number)
    if not counts:
        return
    user = memory.get("user")
    if not isinstance(user, dict):
        user = memory["user"] = {}
    held = user.get("how_many")
    if not isinstance(held, dict):
        held = {}
    for thing, number in counts.items():
        if held.get(thing) != number:
            held[thing] = number
    user["how_many"] = held


HOW_MANY = re.compile(
    r"\bhow many (?P<what>[a-z-]+(?:\s+[a-z-]+){0,2}?)"
    r"(?:\s+(?:and|n|nd)\s+(?P<also>[a-z-]+(?:\s+[a-z-]+){0,2}?))?\s*"
    r"(?:(?:do|did) (?:i|we) (?:have|got|own)|(?:have|had) (?:i|we) got|(?:do|did) (?:i|we) own|"
    r"are there|have we|again|then|now)?\s*[?.!]*$", re.I)
NOT_THE_COUNT = re.compile(r"\b(?:should|could|would|might|may|can|will)\b", re.I)


def answer(text, memory):
    if not isinstance(text, str) or not memory.get("user"):
        return None
    held = memory["user"].get("how_many")
    if not isinstance(held, dict) or not held:
        return None
    low = " ".join(str(text).lower().split())
    if NOT_THE_COUNT.search(low):
        return None
    of_you = bool(GROUP_ASK_YOU.search(low))
    if GROUP_ASK.search(low) or BARE_GROUP_ASK.search(low) or of_you:
        number = held.get(GROUP)
        if isinstance(number, int) and number > 0:
            return _the_group_said_back(number)
        if of_you:
            return None
        number = held.get(PARTY_THING)
        if isinstance(number, int) and number > 0:
            return _the_party_said_back(number, low, memory, of_the_group="of us" in low)
    if PARTY_ASK.search(low):
        number = held.get(PARTY_THING)
        if isinstance(number, int) and number > 0 and _the_chat_sets_a_table(memory):
            return _the_party_said_back(number, low, memory)
        number = held.get(GROUP)
        if isinstance(number, int) and number > 0 and POINTS_AT_A_NUMBER.search(low):
            return _the_party_said_back(number, low, memory, of_the_group=True)
        return None
    if BARE_COUNT_ASK.search(low):
        for thing, of_the_group in ((PARTY_THING, False), (GROUP, True)):
            number = held.get(thing)
            if isinstance(number, int) and number > 0:
                return _the_party_said_back(number, low, memory, of_the_group=of_the_group)
        return None
    match = HOW_MANY.search(" " + low)
    if not match:
        return None
    asked = [_thing_of(match.group("what"))]
    if match.group("also"):
        asked.append(_thing_of(match.group("also")))
    asked = [thing for thing in asked if thing]
    if not asked:
        return None
    counted = [(thing, held[thing]) for thing in asked if isinstance(held.get(thing), int)]
    if not counted:
        return None
    parts = []
    for thing, number in counted:
        many = thing if number == 1 else thing + "s"
        if thing in IRREGULAR.values() and number != 1:
            many = [plural for plural, one in IRREGULAR.items() if one == thing][0]
        parts.append(_many(number) + " " + many)
    said = parts[0] if len(parts) == 1 else " and ".join(parts[:-1]) + " and " + parts[-1]
    if len(counted) < len(asked):
        missing = [thing for thing in asked if not isinstance(held.get(thing), int)]
        return ("You've got " + said + " - I've not been told how many " + missing[0] + "s you "
                "have.")
    return "You've got " + said + "."


def _the_chat_books(memory):
    user = (memory or {}).get("user") or {}
    plans = list(user.get("plans") or [])
    if user.get("plan"):
        plans.append(user.get("plan"))
    return any(re.search(r"\b(?:book|booked|booking|reserv\w*|table)\b", str(plan).lower())
               for plan in plans)


def _the_party_said_back(number, low, memory=None, of_the_group=False):
    many = _many(number)
    if of_the_group:
        plain = "You said " + many + " of you."
        said = {str(turn.get("bot") or "") for turn in (memory or {}).get("turns") or []
                if isinstance(turn, dict)}
        return "Still " + many + " of you." if plain in said else plain
    if "guest" in low:
        noun = "guest" if number == 1 else "guests"
    elif "adult" in low:
        noun = "adult" if number == 1 else "adults"
    elif ("book" in low or "table" in low or "reserv" in low) and _the_chat_books(memory):
        return "The table is for " + many + "."
    else:
        noun = "person" if number == 1 else "people"
    plain = "You said " + many + " " + noun + "."
    said = {str(turn.get("bot") or "") for turn in (memory or {}).get("turns") or []
            if isinstance(turn, dict)}
    if plain in said:
        return "Still " + many + " " + noun + "."
    return plain


def _the_group_said_back(number):
    if number == 1:
        return "Just you, then."
    if number == 2:
        return "The two of you, then."
    return "There are " + _many(number) + " of you."
