import re

from .health import HEADACHE_NO_DRUGS, NO_DRUGS
from ..compose.repair import owns_the_deed as _owns_the_deed
from .lookup import names_a_thing
from .lookup import (ASK_ABOUT, FEELING_WORDS, IMPROVE, NOT_A_NOSE, ORIGIN_ASK, all_of, entry,
                     not_a_count_for_the_box_or_the_dish, not_a_sleepy_body,
                     not_the_flat_you_live_in)

ANSWERS = ("science", "sleep")

_ANOTHER_ADULTS_MEMORY = re.compile(
    r"\b(?:my|his|her|our|their|the)\s+(?:\w+\s+){0,2}"
    r"(?:mum|mom|mam|mother|dad|father|parent|parents|husband|wife|partner|spouse|other half|"
    r"nan|nana|gran|granny|grandma|grandad|grandpa|grandmother|grandfather|"
    r"brother|sister|aunt|auntie|uncle|cousin|mother in law|father in law|friend|"
    r"neighbour|neighbor|boss|colleague|flatmate|housemate|carer|pal|chum|mate|"
    r"nephew|niece|grandchild|grandson|granddaughter|fiance|fiancee|stepmum|stepdad|missus|"
    r"girlfriend|boyfriend)\b|"
    r"\b(?:he|she|they)\s+(?:keeps?|is|are|has|have|always|never|used to)\b")
_A_CHILD = r"(?:son|daughter|child|kid|kid|children|kids|toddler|teenager|teen|baby)"
_SOMEBODY_ELSE_IS_THE_SUBJECT = re.compile(
    r"\b(?:my|his|her|our|their|the)\s+(?:\w+\s+){0,2}" + _A_CHILD + r"\b|" +
    _ANOTHER_ADULTS_MEMORY.pattern)


def _not_somebody_elses_memory(understood):
    from .habits import _words_of
    text = _words_of(understood)
    if not text:
        return True
    return not _SOMEBODY_ELSE_IS_THE_SUBJECT.search(text)


_NAMES_THE_ILLNESS = re.compile(
    r"\bdementia\b|\balzheimers?\b|\balzheimer's\b|\bmemory clinic\b|"
    r"\bmemory assessment\b|\bearly onset\b|\bsigns? of (?:it|this|that)\b")
_MY_OWN_ERRAND = re.compile(
    r"\b(?:i|im|i'm|ive|i've)\b(?:\s+\w+){0,4}?\s+(?:keep\s+|kept\s+)?(?:forget|forgets|"
    r"forgetting|forgot|forgotten)\s+(?:about\s+)?to\b")


def _the_speaker_forgot_to_do_it(understood):
    from .habits import _words_of
    text = _words_of(understood)
    return bool(text and _MY_OWN_ERRAND.search(text))


_MONEY_OWED = re.compile(
    r"\b(?:owes?|owed|owing|quid|pay (?:me )?back|paid back|repay|repays|borrowed|lent|"
    r"debt|debts|in arrears|wont pay|won't pay|not paid me|still hasnt paid|still hasn't paid)\b")


def _its_money_that_has_not_come_back(understood):
    from .habits import _words_of
    text = _words_of(understood)
    return bool(text and _MONEY_OWED.search(text))


_A_HABIT_THING = re.compile(
    r"\b(?:names?|keys|glasses|wallet|purse|password|passwords|pin|birthdays?|anniversary|"
    r"tablets?|medication|medicines|pills|appointments?|shopping|bills?)\b")


def _a_habit_without_the_illness(understood):
    from .habits import _words_of
    text = _words_of(understood)
    if not text:
        return False
    if _ANOTHER_ADULTS_MEMORY.search(text):
        return False
    return bool(_A_HABIT_THING.search(text)) and not _NAMES_THE_ILLNESS.search(text)


DEFINITION_ASK = ("what is", "what's", "what are", "what does", "what do", "how does",
                  "how do", "how is", "how are", "why is", "why are", "why does", "explain",
                  "tell me about", "define")

GRAZERS = ("cat", "cats", "dog", "dogs", "puppy", "pet", "pets", "cow", "cows", "rabbit",
           "rabbits", "horse", "horses", "sheep", "deer")

PESTS_AND_CARE = ("slug", "slugs", "snail", "snails", "aphid", "aphids", "caterpillar",
                  "caterpillars", "pest", "pests", "bug", "bugs", "insect", "insects",
                  "eating my", "eats my", "ate my", "rid of", "stop", "killed", "kill",
                  "dying", "dead", "droop", "drooping", "wilt", "wilted", "yellow leaves",
                  "repot", "fertiliser", "fertilizer", "feed my", "prune", "lawn", "weed",
                  "weeds", "look after", "care for", "water my", "water them", "water it",
                  "how often", "how much water", "once a week", "shade", "frost",
                  "tomato plant", "my leaves", "yellow leaves", "leaves yellow",
                  "leaves are yellow", "houseplant", "houseplants", "plant food")
PLANT_CARE_AVOID = tuple(word for word in PESTS_AND_CARE
                         if word not in ("houseplant", "houseplants"))
WATERING = ("how often", "how much water", "water my", "water them", "water it",
            "water a", "should i water", "when to water", "once a week", "twice a week",
            "every day", "hose", "sprinkler", "tap water")

MOONS = {"mercury": 0, "venus": 0, "earth": 1, "mars": 2, "jupiter": 95,
         "saturn": 146, "uranus": 28, "neptune": 16}

LOW_MORNING = ("cant get out of bed", "can't get out of bed", "cannot get out of bed",
               "cant get up in the morning", "can't get up in the morning",
               "dont want to get up", "don't want to get up", "cant face the day",
               "can't face the day", "no point getting up", "no point in getting up",
               "no point at all", "hopeless", "worthless", "hate mornings",
               "cant get up", "can't get up", "struggling in the mornings",
               "struggling to get up", "not sleeping and not", "no energy for anything")

WAKE_AT_NIGHT = (
    "Waking in the night is normal - sleep runs in cycles of about ninety minutes - and the "
    "common patch is the small hours, around three. The fix is what you do in those minutes: "
    "do not check the clock, keep the light off, and if you are properly awake after about "
    "twenty minutes get up and sit somewhere dim with something dull until you feel heavy "
    "again. Keep the wake-up time the same, and go easy on alcohol and late coffee, because "
    "both knock you out and then wake you at four.")


EARLY_HOUR = (
    r"\b(?:at|by|around|about)\s*(?:5|five|6|six)\b",
    r"\b(?:5|five|6|six)\s*(?:am|a\.m\.|o'?clock)\b",
)
STILL_ASLEEP = (
    r"\bback\s+(?:off\s+)?to\s+sleep\b",
    r"\bstay(?:ing)?\s+asleep\b", r"\bsleep(?:ing)?\s+through\b",
    r"\bwake\s+(?:up\s+)?(?:several|a\s+few|couple|twice|three)\s+times\b",
)


def _dinosaurs(memory, understood):
    clean = ((understood or {}).get("clean") or (understood or {}).get("plain") or "").lower()
    if re.search(r"when|how long|how old|hoe long|what era|which era|what period|"
                 r"which period|million years", clean):
        return ("The dinosaurs were around for about 165 million years, from roughly 230 million "
                "years ago to 66 million years ago, in the Triassic, Jurassic and Cretaceous "
                "periods. The first ones were small and two-legged, the biggest - the long-necked "
                "sauropods and then T. rex - came late, and by the end they were on every "
                "continent including Antarctica.")
    return ("An asteroid about 10 km wide hit what is now Mexico 66 million years ago. The dust "
            "it threw up blocked the sun for years, plants and the animals that ate them "
            "collapsed, and the dinosaurs that could not fly died out; birds, which are their "
            "descendants, survived.")


_FEELINGS = ("tired", "knackered", "exhausted", "exhausting", "worn out", "drained",
             "run down", "shattered", "no energy", "any energy", "falling asleep",
             "more energy", "energy levels", "energy back", "get energy",
             "zero energy", "low on energy", "wiped out", "zonked", "lethargic",
             "no get up and go", "no oomph", "keep my eyes open", "yawning", "sleepy",
             "shattered all the time", "dead on my feet")

_KEYED_FEELINGS = tuple(p for p in _FEELINGS if p not in (
    "exhausted", "exhausting", "drained", "run down", "shattered", "tired",
    "more energy", "energy levels", "energy back", "get energy", "falling asleep"))

_TIRED = re.compile(r"\b(" + "|".join(_FEELINGS) + r")\b")


def _names_the_feeling(understood):
    if not isinstance(understood, dict):
        return False
    parts = [understood.get("text") or "", understood.get("clean") or "",
             " ".join(understood.get("words") or ())]
    return any(_TIRED.search(str(part).lower()) for part in parts if part)

def _any_hit(patterns, text):
    return any(re.search(pattern, text) for pattern in patterns)


FELL_OUT = re.compile(
    r"\bf(?:ell|all|alls|alling|allen)\s+out\b(?!\s+of\b)|\bfell\s+about\b")


def _a_fall_and_not_a_row(understood):
    if not isinstance(understood, dict):
        return True
    words = " ".join(str(word).lower() for word in (understood.get("words") or ()))
    text = " ".join((str(understood.get("clean") or ""), str(understood.get("text") or ""),
                     str(understood.get("raw") or ""), words)).lower()
    text = re.sub(r"[^a-z0-9' ]+", " ", text)
    return not FELL_OUT.search(text)


STANDS_UP_THINGS = re.compile(
    r"\b(?:buildings?|skyscrapers?|high[ -]?rises?|tower blocks?|blocks? of flats|towers?|"
    r"cranes?|bridges?|chimneys?|pylons?|statues?|cathedrals?|domes?|monuments?|trees?|"
    r"forests?|woods|houseplants?|plants?|seedlings?|tomato(?:es)?|flowers?|tulips?|"
    r"daffodils?|sunflowers?|roses?|hanging baskets?|shrubs?)\b")

PEOPLE_WHO_FALL = re.compile(
    r"\b(?:nan|nana|gran|granny|grandma|grandad|grandpa|grandmother|grandfather|mum|mum's|"
    r"mom|mother|dad|father|husband|wife|partner|sister|brother|aunt|uncle|friend|neighbour|"
    r"neighbor|carer|patient|resident|she|he|her|him|his|they|them|someone|somebody|"
    r"elderly|pensioner|oap|old people|old lady|old man|people|person)\b")


def _a_person_who_falls(understood):
    if not isinstance(understood, dict):
        return True
    said = " ".join(str(part or "") for part in ((understood.get("clean"),
                                                   understood.get("text")))).lower()
    said = re.sub(r"[^a-z0-9' ]+", " ", said)
    if PEOPLE_WHO_FALL.search(said):
        return True
    return not STANDS_UP_THINGS.search(said)


A_FALL_VERB = re.compile(r"\bf(?:all|alls|alling|ell|allen)\b")
BEFORE_THE_FALL = re.compile(
    r"([a-z']+)\s+(?:keeps?|kept|is|are|was|were|has|have|had|just|nearly|almost|"
    r"keep|would|did|didnt|never|still|always)\s+(?:f(?:all|alls|alling|ell|allen))\b")
NOT_A_FALL_PHRASE = re.compile(
    r"\bf(?:all|alls|alling|ell|allen)\s+(?:(?:over|down|about|in|out)\s+)?"
    r"(?:behind|for|short|through|flat|foul|silent|quiet|ill|asleep|pregnant|in love|"
    r"into place|in place|laughing)\b")
PEOPLE_WHO_ARE_THE_SUBJECT = PEOPLE_WHO_FALL.pattern

NOT_THE_SUBJECT = frozenset("""
    and but so then than that which who whom whose where when what why how if or nor yet though
    although while until till since because as also still just now even ever never always
    sometimes often usually again once only really nearly almost quite very too much more most
    s t d ll re ve m
    """.split())


def _a_thing_falls_not_a_person(understood):
    if not isinstance(understood, dict):
        return True
    said = " ".join(str(part or "") for part in ((understood.get("clean"),
                                                  understood.get("text"),
                                                  understood.get("raw")))).lower()
    said = re.sub(r"[^a-z0-9' ]+", " ", said)
    if NOT_A_FALL_PHRASE.search(said):
        return False
    for subject in BEFORE_THE_FALL.findall(said):
        if subject in ("i", "we", "you"):
            continue
        if re.search(PEOPLE_WHO_ARE_THE_SUBJECT, subject):
            continue
        if subject in NOT_THE_SUBJECT:
            continue
        return False
    return True


def _a_fall_a_person_had(understood):
    return (_a_fall_and_not_a_row(understood) and _a_person_who_falls(understood)
            and _a_thing_falls_not_a_person(understood))


GRINDING_BABY = ("baby", "babies", "baby's", "toddler", "toddlers", "newborn", "newborns",
                 "months old", "month old", "1 year old", "one year old", "2 year old",
                 "two year old", "3 year old", "three year old", "first teeth", "new teeth",
                 "baby teeth", "milk teeth", "teething", "child", "children", "kid", "kids",
                 "little one", "my little", "my son", "my daughter", "my boy", "my girl")

GRINDING_ADULT = ("Ask your dentist for a night guard: a splint made for your teeth protects the "
                  "enamel and takes the load off the jaw, and most practices can fit one in about a "
                  "week. Cut caffeine and alcohol in the evening, and when you catch yourself "
                  "clenching, rest your tongue behind your top teeth with your jaw slack. If you "
                  "wake with a sore jaw or headaches, tell your dentist rather than buying a "
                  "one-size guard online.")

_SAME_OR_TWICE = re.compile(r"\bsame\b|\bdifference\b", re.I)
_TWICE = re.compile(r"\btwice\b|\bagain\b|more than once", re.I)


def _cold_or_flu_verdict(understood):
    text = str((understood or {}).get("text") or "").lower()
    if _SAME_OR_TWICE.search(text):
        return "No"
    if _TWICE.search(text):
        return "Yes"
    return ""


BABY_GRINDING = ("Mostly nothing to fix: a child grinding brand-new teeth is common, harmless "
                 "and passes as the bite settles, and sore gums make a teething baby grind. It "
                 "does not damage the teeth, and no guard goes on a child whose teeth are still "
                 "coming through. If it carries on for months, or comes with a sore jaw, mention "
                 "it at the next dental check.")


_HANGOVER_LENGTH = (
    "A hangover peaks at about 12 hours and is usually gone within a day, with the headache and "
    "the tiredness easing as it goes; a heavy one can run into a second day. ")
_HANGOVER_CURE = (
    "There is no cure, only time: what your body needs back is water and sleep. Drink a pint "
    "of water or an electrolyte drink, eat something plain even if you don't want it, and "
    "take paracetamol if you want a painkiller, with food. Don't have another drink to steady "
    "yourself; a pint of water before bed helps a little, and eating before you started "
    "helps more.")
_HANGOVER_LENGTH_ASK = re.compile(
    r"\bhow long\b|\bhow many (?:hours|days)\b|\bwhen (?:will|does|do|should)\b|"
    r"\bhow soon\b|\bhow many hours does\b|\blasts?\b|\blast\b", re.I)


def _hangover(memory, understood):
    said = "%s %s" % (str((understood or {}).get("clean") or ""),
                      " ".join(str(word) for word in ((understood or {}).get("words") or ())))
    if _HANGOVER_LENGTH_ASK.search(said):
        return _HANGOVER_LENGTH + _HANGOVER_CURE
    return _HANGOVER_CURE


def _grinding(memory, understood):
    clean = " " + str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower() + " "
    clean = re.sub(r"[^a-z0-9' ]+", " ", clean)
    if any(" " + word + " " in clean for word in GRINDING_BABY):
        return BABY_GRINDING
    if _asks_what_it_is(clean):
        return GRINDING_WHAT
    return GRINDING_ADULT


GRINDING_WHAT = ("Bruxism is grinding or clenching your teeth, usually in your sleep, and most "
                 "people only find out from a dentist or a partner rather than noticing it. The "
                 "pressure is what wears enamel and leaves the jaw achey, and it is often worse "
                 "with stress, caffeine and alcohol in the evening. A night guard from a dentist "
                 "protects the teeth, and it is worth asking about one if you wake with a sore "
                 "jaw or headaches.")

_WHAT_IS_IT = ("what is ", "what's ", "whats ", "what are ", "explain ", "define ",
               "meaning of ", "what does")


def _asks_what_it_is(clean):
    said = (clean or "").strip()
    return any(said.startswith(opening) for opening in _WHAT_IS_IT)


NIGHT_CAUSE_TOPICS = ("health", "feelings")
NIGHT_SYMPTOM = ("pain", "painful", "ache", "aches", "aching", "achy", "hurt", "hurts",
                 "hurting", "cramp", "cramps", "cough", "coughing", "tooth", "toothache",
                 "headache", "headaches", "migraine", "heartburn", "reflux", "nausea",
                 "nauseous", "fever", "temperature", "itch", "itching", "sore", "swollen",
                 "stiff", "restless legs", "sick", "throwing up", "period pain")


def _night_waking(memory, understood):
    said_so_far = " ".join(
        str((understood or {}).get(key) or "") for key in ("clean", "norm", "plain"))
    topics = (understood or {}).get("topics") or ()
    if any(topic in NIGHT_CAUSE_TOPICS for topic in topics):
        return None
    if _any_hit(NIGHT_SYMPTOM, said_so_far):
        return None
    if _any_hit(EARLY_HOUR, said_so_far) and not _any_hit(STILL_ASLEEP, said_so_far):
        return None
    try:
        from ..memory import thread
        said = " ".join((text or "").lower() for text, _reading in thread.user_lines(memory))
    except Exception:
        return WAKE_AT_NIGHT
    if any(phrase in said for phrase in LOW_MORNING):
        return None
    return WAKE_AT_NIGHT


NAMED_MOONS = {
    "jupiter": "Io, Europa, Ganymede and Callisto are the four worth knowing - the ones Galileo "
               "saw in 1610 - and Europa is the one with an ocean under the ice",
    "saturn": "Titan is the one worth knowing - bigger than Mercury, with lakes of methane - then "
              "Enceladus, Rhea, Iapetus and Mimas",
    "mars": "Phobos and Deimos, both small lumps of rock no more than twenty-odd kilometres "
            "across",
    "uranus": "Titania, Oberon, Umbriel, Ariel and Miranda, all named after Shakespeare and Pope "
              "characters",
    "neptune": "Triton, the big one, which orbits backwards and is probably a captured "
               "Kuiper-belt object",
}


def _moons(memory, understood):
    clean = (understood or {}).get("clean") or ""
    if any(word in clean for word in ("name", "called", "which moon", "which moons", "list")):
        if "earth" in clean:
            return ("Just the Moon, the fifth largest in the solar system and the only "
                           "other world people have stood on.")
        for planet in ("jupiter", "saturn", "mars", "uranus", "neptune"):
            if planet in clean:
                return NAMED_MOONS[planet] + "."
        return ("Earth's is the Moon, Mars has Phobos and Deimos, and the four big Jovian moons "
                "are Io, Europa, Ganymede and Callisto. Most of the hundreds the counts refer to "
                "are unnamed rocks a few kilometres across.")
    if "most" in clean and not any(name in clean for name in ("earth", "mars", "jupiter")):
        return "Saturn has the most confirmed moons, more than 140, ahead of Jupiter at about 95."
    for planet in ("jupiter", "saturn", "uranus", "neptune", "mars", "earth", "venus",
                   "mercury"):
        if planet in clean:
            count = MOONS[planet]
            if count == 0:
                return f"{planet.capitalize()} has no moons."
            if count == 1:
                return f"{planet.capitalize()} has one moon."
            return f"{planet.capitalize()} has {count} confirmed moons."
    return ("Mercury and Venus have none, Earth has one and Mars has two; the gas giants have "
            "dozens, with Saturn topping the list at more than 140.")

DISCOVERERS = {
    "penicillin": ("Alexander Fleming found penicillin in 1928, when a mould that had drifted "
                   "onto a petri dish killed the bacteria round it."),
    "gravity": ("Isaac Newton worked out the law of gravity in 1687, and the same rule still "
                "covers a falling apple and an orbiting moon."),
    "evolution": ("Charles Darwin set out evolution by natural selection in 1859, in On the "
                  "Origin of Species, with Alfred Russel Wallace reaching the same idea at the "
                  "same time."),
    "natural selection": ("Charles Darwin set out natural selection in 1859, in On the Origin of "
                          "Species."),
    "x-rays": ("Wilhelm Rontgen discovered X-rays in 1895, and won the first Nobel Prize in "
               "Physics for them."),
    "x rays": ("Wilhelm Rontgen discovered X-rays in 1895, and won the first Nobel Prize in "
               "Physics for them."),
    "radioactivity": ("Henri Becquerel found radioactivity in 1896; Marie and Pierre Curie then "
                      "did the chemistry that explained it."),
    "dna": ("The structure of DNA was worked out by James Watson and Francis Crick in 1953, "
            "using Rosalind Franklin's X-ray photographs."),
    "the electron": ("J. J. Thomson discovered the electron in 1897."),
    "oxygen": ("Joseph Priestley isolated oxygen in 1774, and Carl Wilhelm Scheele had found it "
               "two years earlier without publishing first."),
    "the vaccine": ("Edward Jenner made the first vaccine in 1796, using cowpox against "
                    "smallpox."),
    "vaccines": ("Edward Jenner made the first vaccine in 1796, using cowpox against smallpox."),
}


def who_discovered(memory, understood):
    clean = (understood or {}).get("clean") or (understood or {}).get("text") or ""
    clean = clean.lower().replace("'", "")
    best = None
    for thing in DISCOVERERS:
        if re.search(r"\b" + re.escape(thing) + r"\b", clean):
            if best is None or len(thing) > len(best):
                best = thing
    if best is None:
        return None
    return DISCOVERERS[best]


SLEEP_SAID = re.compile(r"\b(\d{1,2}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|"
                        r"twelve)\s*(?:-\s*\d{1,2}\s*)?(?:hours?|hrs?|h)\b", re.IGNORECASE)
SLEEP_NUMBER = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
                "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12}
SLEEP_WORD = {6: "Six", 5: "Five", 4: "Four", 7: "Seven", 8: "Eight", 9: "Nine",
              10: "Ten", 11: "Eleven", 12: "Twelve"}
SLEEP_TALK = re.compile(r"\b(?:sleep|sleeping|slept|sleeps|bed|hours?)\b", re.IGNORECASE)


def _sleep_said(clean):
    match = SLEEP_SAID.search(clean)
    if not match or not SLEEP_TALK.search(clean):
        return None
    word = match.group(1).lower()
    hours = SLEEP_NUMBER.get(word) or int(word)
    return hours if 1 <= hours <= 14 else None


def _sleep_hours(memory, understood):
    clean = ((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    said = _sleep_said(clean)
    if any(word in clean for word in ("teenager", "teenagers", "teen", "teens", "teenage",
                                      "15", "16", "17", "sixteen", "fifteen", "seventeen")):
        return ("Teenagers need eight to ten hours a night, and their body clock runs late, so an "
                "11pm bedtime is not late for them. The fix that helps most is a light morning "
                "and the same wake-up time at weekends.")
    if any(phrase in clean for phrase in ("over 65", "over-65", "older", "elderly", "pensioner",
                                          "70")):
        return ("Seven to eight hours is usual after 65, and the sleep gets lighter and more "
                "broken, which is ordinary. Twenty-minute naps are fine; a long afternoon sleep "
                "is what makes the night worse.")
    if said is not None and said < 7:
        return ("%s hours is on the short side: most adults need seven to nine, and the shortfall "
                "shows as yawning, coffee and losing the thread by mid-afternoon. Half an hour "
                "earlier to bed, and the same wake-up time every day, is the fix - a long weekend "
                "lie-in is not." % SLEEP_WORD.get(said, said))
    if said is not None and 7 <= said <= 9:
        yes = "Yes - " if re.search(r"\b(enough|ok|okay|fine|normal)\b", clean) else ""
        return ("%s%s hours is inside the seven to nine most adults need, so there is nothing to "
                "fix if your days are fine. If you are yawning by mid-afternoon anyway, half an "
                "hour earlier to bed does more than a weekend lie-in."
                % (yes, SLEEP_WORD.get(said, said).lower() if yes else SLEEP_WORD.get(said, said)))
    if said is not None and said > 9:
        return ("%s hours is more than an adult needs, and the extra is not doing anything for "
                "you. Long nights after a short week are fine; sleeping that long every night and "
                "still waking unrefreshed is worth a word with the GP." % SLEEP_WORD.get(said, said))
    return ("Most adults do best on seven to nine hours, but the number is a guide and the test "
            "that matters is how you are by mid-afternoon: yawning, reaching for coffee and "
            "losing the thread on six hours means you are short, whatever the chart says. The fix "
            "is usually a 30-minute earlier bedtime rather than a lie-in at the weekend, and "
            "keeping the wake-up time the same even after a bad night. Some people genuinely run "
            "fine on six and it runs in families; if your days are fine, the number is not a "
            "problem to solve.")


EYES_COST = re.compile(r"\b(?:free|cost|costs|pay|paid|price|how much|charge|charges|"
                       r"afford|nhs)\b", re.IGNORECASE)


def _eyes_test(memory, understood):
    clean = ((understood or {}).get("clean") or (understood or {}).get("text") or "")
    money = ("free if you are under 16, over 60, or on some benefits or a low income - otherwise "
             "about £25 to £45")
    when = ("every two years suits most adults, and every year from 70 or if you have diabetes, "
            "glaucoma in the family or a big change in your vision")
    if EYES_COST.search(clean):
        return ("In the UK a sight test is " + money + ". It checks eye health as well as glasses, "
                "and " + when + ".")
    asks_when = re.search(r"\b(?:how often|how frequently|when|how soon)\b", clean, re.IGNORECASE)
    says_yes = (re.search(r"\b(?:should|shall|ought)\b", clean, re.IGNORECASE) and not asks_when)
    return (("Yes - a sight test " if says_yes else "A sight test ") + when + ". It is " + money + ".")


_MED_MISSED = re.compile(
    r"\b(missed|miss|forgot|forgotten|skipped|skip)\b|\brain out\b|\bran out\b")
_MED_DOUBLE = re.compile(r"\b(double|doubled|doubling|two|2|extra|catch up|catch-up|twice)\b")
_MED_REPEAT = re.compile(
    r"\b(keep|keeps|kept|always|forget|forgets|forgetting|remember|remembers|remembering|muddle|"
    r"muddled|mixed up)\b")
_MED_SUGAR = re.compile(r"\b(diabetes|diabetic|insulin|hypo|blood sugar\w*)\b")
_MED_CONFUSED = re.compile(r"\b(confused|confusion|muddled|not himself|not herself)\b")
_MED_TABLET_MUDDLE = re.compile(
    r"\b(confus\w*|muddled|muddle|mixed\s+up)\b[^.?!]{0,20}"
    r"\b(about|over|with|by|between)\b[^.?!]{0,24}"
    r"\b(tablets?|pills?|medicines?|medication|dose|doses|packet|blister|boxes|"
    r"which\s+(?:ones?|tablets?|pills?)|what\s+to\s+take|when\s+to\s+take)\b"
    r"|\b(tablets?|pills?|medicines?|medication|doses?)\b[^.?!]{0,12}"
    r"\b(muddled|confused|mixed\s+up)\b")
_MED_CONFUSED_NEW = re.compile(
    r"\b(suddenly|sudden|since|yesterday|tonight|today|this\s+week|last\s+night|overnight|"
    r"started|for\s+days?|for\s+hours?|fever|temperature|fell|fallen|fall|not\s+eating|"
    r"cannot\s+wake|can'?t\s+wake|out\s+of\s+it|drowsy|sleepy|shaky|sweaty)\b")
_MED_TOO_MUCH = re.compile(
    r"\b(took|taken|had|swallowed)\s+(two|2|an extra|extra|double)\b|\bdouble(d)?\s+(up|my)\b|"
    r"\btwice\s+(today|already|by mistake)\b|\bby mistake\b|\baccident\w*\b|\binstead\b")

_MED_DOUBLE_ANSWER = (
    "Never double up to catch up: skip the missed dose and take the next one at its usual time. "
    "Check the leaflet or ask a pharmacist first, because a few medicines (insulin, blood thinners, "
    "epilepsy tablets, the contraceptive pill) are exceptions where an extra dose is the right "
    "thing.")
_MED_BOX = (
    "A weekly box or a blister pack from the chemist - most do it free - is what stops the next one "
    "being missed: fill it together on a Sunday, write the times on the lid and set a phone alarm "
    "for each dose.")
_MED_ROUTINE = (
    "A weekly box or a blister pack from the chemist is the fix: fill it together on a Sunday, "
    "write the times on the lid and set a phone alarm for each dose. If the same one keeps being "
    "missed or taken twice, ask the GP or the pharmacist for a medicines review - they can often "
    "cut the number of tablets as well as time them.")
_MED_CONFUSED_ANSWER = (
    "New confusion in someone who takes tablets every day is worth a same-day call to their GP or "
    "111: it can be an infection, a side effect, or a low blood sugar if they have diabetes. Test "
    "their blood sugar if they have a meter, and ring 999 if they cannot be woken or cannot swallow."
    )
_MED_TOOK_TWO = (
    "Ring 111 or ask a pharmacist now, before your next dose: for most tablets an accidental double "
    "means waiting longer before the next one rather than skipping it, and they will tell you which "
    "for yours. Take nothing more in the meantime, and get seen straight away if you feel faint, very "
    "sleepy or sick.")
_PILL_SEX = re.compile(
    r"\b(sex|unprotected|condom|condoms|intercourse|slept with)\b|\bhad it\b")
_PILL_MINI = re.compile(r"\b(mini pill|desogestrel|cerazette|progestogen only|progesterone only)\b")


def _missed_pill(memory, understood):
    clean = ((understood or {}).get("clean") or "").lower()
    first = ("Take the missed pill as soon as you remember, then carry on at your usual time, and "
             "use condoms for the next 7 days.")
    if _PILL_MINI.search(clean):
        first = ("Take the missed mini pill as soon as you remember - the window is 12 hours (3 "
                 "hours for the older progestogen-only pills), and a later one counts as missed - "
                 "and use condoms for the next 7 days.")
    return (first + " If you had sex in those days, get emergency contraception today: a pharmacy "
            "gives it free without an appointment and it is licensed up to 5 days, but it works "
            "best the sooner it is taken.")


_MED_RAN_OUT = re.compile(r"\b(ran out|run out|running out|out of my|out of her|out of his)\b")
_MED_CRITICAL = re.compile(
    r"\b(epilepsy|epileptic|anti-epileptic|seizures|warfarin|blood thinner|blood thinners|"
    r"clot|thyroid|levothyroxine|heart tablets|lithium|steroids|prednisolone|immunosuppressant)\w*",
    )
_MED_RAN_OUT_ANSWER = (
    "A pharmacist can give most repeat medicines an emergency supply of up to 30 days without a "
    "prescription, so ring the pharmacy first, then 111 or the GP surgery if they cannot help "
    "today. Do not just stop taking them: some tablets are dangerous to stop suddenly.")
_MED_CRITICAL_ANSWER = (
    "Epilepsy medicines, blood thinners, thyroid and heart tablets each have their own rule for a "
    "missed dose, and the leaflet in the box says which - ring the pharmacist or your GP surgery and "
    "they will tell you what to do today. Do not double up in the meantime.")
_MED_THIRD = re.compile(
    r"\bmy (mum|mother|mam|mom|dad|father|nan|nanna|gran|granny|grandma|grandad|grandpa|wife|"
    r"husband|partner|sister|brother|aunt|uncle|friend)\b|\b(she|he|they) (keeps|keep|forgets|"
    r"forgot|is forgetting)\b")
_MED_THIRD_PERSON = re.compile(
    r"\b(he|she|they|him|her|them|his|their|mum|mother|mam|mom|dad|father|nan|nanna|gran|granny|"
    r"grandma|grandad|grandpa|wife|husband|partner|sister|brother|aunt|uncle|friend|son|"
    r"daughter)\b")
_MED_PATTERN = (
    "If they are forgetting other things too - names, the day, where the keys went - write down what "
    "they forget for a fortnight and take that to the GP, because a pattern that is new is worth "
    "checking rather than sorting out with a box.")
_MED_ANTIBIOTIC = re.compile(r"\bantibiotics?\b|\bpenicillin\b|\bamoxicillin\b")
_MED_ANTIBIOTIC_ANSWER = (
    "Take the missed antibiotic as soon as you remember, unless the next dose is nearly due - then "
    "skip it and carry on as normal, and never take two at once. Finish the whole course even if "
    "you feel better, and if you were sick within a couple of hours of a dose ask a pharmacist "
    "whether it needs taking again.")
_MED_INSULIN = (
    "A missed insulin dose is one to ask about rather than guess: ring your diabetes team, the "
    "out-of-hours number or 111, test your blood sugar while you wait, and they will tell you how "
    "much to take. Do not take a make-up dose on top without advice, and get seen straight away if "
    "you are being sick or your blood sugar stays high.")
_MED_SUGAR_LINE = (
    "If someone with diabetes goes suddenly confused, sweaty or shaky that is usually a blood sugar "
    "rather than the tablets: sugar first, and 999 if they cannot swallow.")


_KEEP_ANY = re.compile(r"\b(for life|for good|forever|long term|long-term|rest of my life)\b")
_KEEP_LONG = re.compile(
    r"\b(blood pressure|statins?|cholesterol|thyroid|levothyroxine|heart tablets?|warfarin|"
    r"anti-?coagulant\w*|beta ?blocker\w*|ramipril|amlodipine|bisoprolol)\b")


def _keep_taking(memory, understood):
    clean = ((understood or {}).get("clean") or "").lower()
    if _MED_ANTIBIOTIC.search(clean) or "finish the course" in clean or "finish them" in clean:
        return ("Finish the course even if you feel better - a half-finished course is how "
                "infections come back and how resistance starts - and take the missed dose when "
                "you remember unless the next one is nearly due. If the side effects are why you "
                "want to stop, ring the pharmacist: there is usually another antibiotic that suits "
                "better, and they can swap it today.")
    if _KEEP_LONG.search(clean) or _KEEP_ANY.search(clean):
        return ("Keep taking it: tablets for blood pressure, cholesterol, the thyroid and the heart "
                "are for the long haul, and they work precisely because you do not feel them - so "
                "stopping when you feel well is when the risk comes back. If the dose or the side "
                "effects are a problem, ask for a review rather than stopping, and never stop one "
                "of these suddenly on your own. Ring the pharmacist or the surgery if you have "
                "already stopped.")
    return ("Keep taking it until a pharmacist, nurse or GP tells you to stop, and ask for a review "
            "rather than deciding on your own: tablets for the heart, blood pressure, thyroid, "
            "epilepsy, steroids and antidepressants can be dangerous to stop suddenly. If it is not "
            "suiting you, the fix is usually the dose, the brand or the time of day, so say what "
            "has changed and ask. If you have already stopped and feel unwell, ring the pharmacist "
            "today or 111.")


def _missed_medication(memory, understood):
    clean = ((understood or {}).get("clean") or "").lower()
    if _MED_CONFUSED.search(clean):
        if _MED_TABLET_MUDDLE.search(clean) and not _MED_CONFUSED_NEW.search(clean):
            return _MED_BOX + (" " + _MED_PATTERN if _MED_THIRD_PERSON.search(clean) else "")
        return _MED_CONFUSED_ANSWER
    if _MED_RAN_OUT.search(clean):
        return _MED_RAN_OUT_ANSWER
    if _MED_CRITICAL.search(clean):
        return _MED_CRITICAL_ANSWER
    if _MED_REPEAT.search(clean) and _MED_MISSED.search(clean):
        return _MED_ROUTINE + (" " + _MED_SUGAR_LINE if _MED_SUGAR.search(clean) else "")
    if _MED_ANTIBIOTIC.search(clean):
        return _MED_ANTIBIOTIC_ANSWER
    if _MED_MISSED.search(clean) and _MED_SUGAR.search(clean) and not _MED_REPEAT.search(clean):
        return _MED_INSULIN
    if _MED_TOO_MUCH.search(clean) and not _MED_MISSED.search(clean):
        return _MED_TOOK_TWO
    if _MED_MISSED.search(clean) and _MED_DOUBLE.search(clean):
        return _MED_DOUBLE_ANSWER + " " + _MED_BOX
    if _MED_MISSED.search(clean) and not _MED_REPEAT.search(clean):
        return ("Skip the missed dose and take the next one at its usual time, and do not take two "
                "to catch up. " + _MED_BOX)
    if _MED_THIRD.match(clean):
        return _MED_BOX + " " + _MED_PATTERN
    if not _MED_REPEAT.search(clean):
        return ""
    reply = _MED_ROUTINE
    if _MED_SUGAR.search(clean):
        reply += " " + _MED_SUGAR_LINE
    return reply

_CAFFEINE_SYMPTOM = ("anxious", "anxiety", "jittery", "jitters", "shaky", "shaking",
                     "palpitations", "palpitation", "wired", "racing", "races", "pounding",
                     "flutter", "heart", "panic", "panicky")
_CAFFEINE_COUNT = re.compile(
    r"\b(\d{1,3})\b(?:\s+(?:of\s+)?)(cups?|mugs?|coffees?|teas?|cans?|espressos?)"
    r"\s*(?:(?:a|per|each|every)\s+(day|week))?")


def _caffeine_while_expecting(memory, understood):
    clean = ((understood or {}).get("clean") or "").lower()
    figure = ("200mg of caffeine a day, about two mugs of coffee or four cups of tea: half the "
              "usual limit. It is also in cola, energy drinks, chocolate and some cold remedies, "
              "so those count too. Stay under the figure rather than at it")
    if any(word in clean for word in ("breastfeeding", "breast feeding", "nursing", "feeding")):
        return ("While you are breastfeeding the advice is the same as in pregnancy: " + figure +
                ". A coffee before a feed is fine, and the caffeine peaks in your milk an hour "
                "later, so the evening ones are the ones to make decaf.")
    return ("In pregnancy the advice is " + figure + ", and the same 200mg is what to keep to "
            "while you are trying or breastfeeding.")


_KIDS_LINE = ("Children under 12 are better off with no caffeine at all, and 12 to 18 should keep "
             "under about 100mg a day: a can of cola is around 35mg, a cup of tea about 50mg, a "
             "coffee 80mg or more. Energy drinks are the ones to refuse outright, since one can "
             "hold a teenager's whole day's worth and the sugar and taurine come with it.")

_KID_WORDS = ("child", "children", "kid", "kids", "son", "daughter", "toddler", "baby",
              "teenager", "teenagers", "boy", "girl", "school", "under 12", "under 5")
_PRONOUN_SUBJECT = re.compile(r"\b(she|he|they|him|her|them|his|hers)\b")


def _child_in_chat(memory):
    for turn in ((memory or {}).get("turns") or [])[-3:]:
        if not isinstance(turn, dict):
            continue
        text = " ".join(str(turn.get("user") or "").lower().split())
        if not text:
            continue
        if any(word in text.split() for word in _KID_WORDS) or "$" in text:
            return True
        if any(phrase in text for phrase in _TEEN_AGE_PHRASES) or "under 12" in text:
            return True
    return False


def _per_day(daily):
    whole = int(daily)
    if abs(daily - whole) < 0.05:
        return "%d" % whole
    return ("%.1f" % daily).rstrip("0").rstrip(".")


def _caffeine_limit(memory, understood):
    clean = ((understood or {}).get("clean") or "").lower()
    if any(word in clean for word in _CAFFEINE_SYMPTOM):
        return ("Those are the usual signs of too much caffeine: cut back to a cup or two in the "
                "morning and make the rest decaf, which keeps the habit without the jitters. Taper "
                "over a week rather than stopping dead, or the headaches will be worse than the "
                "shakes, and if your heart pounds for no reason, get it checked.")
    if (_child_in_chat(memory) and _PRONOUN_SUBJECT.search(clean)
            and not re.search(r"\bi\b", clean)
            and not re.search(r"\b\d+\b", clean) and not _CAFFEINE_COUNT.search(clean)):
        return _KIDS_LINE
    heaviest = None
    for found in _CAFFEINE_COUNT.finditer(clean):
        count, unit, period = int(found.group(1)), found.group(2), (found.group(3) or "day")
        daily = count / 7.0 if period == "week" else float(count)
        if heaviest is None or daily > heaviest[0]:
            heaviest = (daily, count, unit, period)
    if heaviest and heaviest[0] >= 5:
        _, count, unit, period = heaviest
        return ("%d %s a %s is well over the 400mg adult limit, which is about four instant coffees "
                "or two large filter ones; a cup of tea is around 50mg against 80mg or more in a "
                "coffee. Come down a cup every few days and make the later ones decaf, and the "
                "sleep and the jitters both settle." % (count, unit, period))
    milligram = re.search(r"\b(\d{2,4})\s*(?:mg|milligrams?)\b", clean)
    if milligram and any(word in clean for word in ("a lot", "lot", "ok", "okay", "alright",
                                                    "fine", "safe", "too much", "bad")):
        amount = int(milligram.group(1))
        if amount >= 400:
            return ("%dmg a day is at or over the 400mg adult limit - four instant coffees or two "
                    "large filter ones - so it is the point to come down from, a cup every few "
                    "days rather than all at once. Keep it under 200mg if you are pregnant, and if "
                    "it comes with a pounding heart or bad sleep, get that looked at." % amount)
        return ("%dmg is under the 400mg adult limit, which is about four instant coffees or two "
                "large filter ones, so on the caffeine count alone it is fine. It is still worth "
                "keeping the last one before early afternoon if sleep is a problem, and the limit "
                "halves to 200mg in pregnancy." % amount)
    if not any(word in clean for word in ("much", "too", "limit", "safe", "many", "a lot", "lot",
                                          "ok", "okay", "alright", "fine", "bad")):
        if heaviest:
            _, count, unit, period = heaviest
            return ("%d %s a %s is about %s a day, which is inside the 400mg adult limit - that is "
                    "four instant coffees or two large filter ones. Keep the last one before early "
                    "afternoon if sleep is a problem, and stay under 200mg a day if you are "
                    "pregnant." % (count, unit, period, _per_day(heaviest[0])))
        return ""
    return ("Around 400mg of caffeine a day is the usual safe limit for an adult, which is about "
            "four cups of instant coffee or two large filter coffees; pregnant women are advised to "
            "keep to 200mg. Stop by early afternoon if your sleep is affected, and cut down slowly "
            "over a week or two, since going cold turkey can bring headaches and irritability.")


_CAFFEINE_LEAD = {
    "tea": ("Around 400mg of caffeine a day is the usual safe limit for an adult, which is about "
            "six to eight mugs of ordinary tea at 50mg a mug - a strong one is nearer 70mg, so "
            "four or five of those"),
    "coffee": ("Around 400mg of caffeine a day is the usual safe limit for an adult, which is about "
               "four cups of instant coffee or two large filter coffees"),
    "energy": ("Around 400mg of caffeine a day is the usual safe limit for an adult, which is two "
               "or three 250ml energy drinks"),
    "cola": ("Around 400mg of caffeine a day is the usual safe limit for an adult, which is about "
             "eleven cans of cola at 35mg a can"),
    "herbal": ("Camomile, peppermint and fruit teas have no caffeine in them, so there is no daily "
               "limit to count against - the only thing to watch is how much sugar or honey goes "
               "in, and a herbal tea at night is the reason people drink it"),
}
_CAFFEINE_TAIL = ("; pregnant women are advised to keep to 200mg. Stop by early afternoon if your "
                  "sleep is affected, and cut down slowly over a week or two, since going cold "
                  "turkey can bring headaches and irritability.")
_CAFFEINE_DRINKS = (("herbal", ("herbal tea", "herbal teas", "camomile", "chamomile",
                                "peppermint tea", "fruit tea", "rooibos")),
                    ("tea", ("tea", "teas", "green tea", "builder's tea", "builders tea",
                             "cup of tea", "cups of tea", "mug of tea", "mugs of tea")),
                    ("coffee", ("coffee", "coffees", "espresso", "filter coffee",
                                "instant coffee", "latte", "cappuccino", "americano")),
                    ("energy", ("energy drink", "energy drinks", "monster", "red bull")),
                    ("cola", ("cola", "coke", "pepsi")))


_LIMIT_ASKS = frozenset((
    "much", "many", "too", "limit", "limits", "safe", "safely", "day", "days", "daily",
    "week", "weekly", "cups", "often", "amount", "maximum", "max",
    "bad", "good", "harmful", "healthy", "unhealthy", "ok", "okay", "fine", "worse",
    "risky", "risk"))


def _the_limit_for_the_drink_named(memory, reading):
    clean = ((reading or {}).get("clean") or "").lower()
    if not (set((reading or {}).get("words") or ()) & _LIMIT_ASKS):
        return None
    herbal = dict(_CAFFEINE_DRINKS)["herbal"]
    if any(phrase in clean for phrase in herbal):
        return _CAFFEINE_LEAD["herbal"] + "."
    found = [name for name, phrases in _CAFFEINE_DRINKS if name != "herbal"
             and any(phrase in clean for phrase in phrases)]
    if len(found) == 1 and found[0] in _CAFFEINE_LEAD:
        return _CAFFEINE_LEAD[found[0]] + _CAFFEINE_TAIL
    if "tea" in found and "coffee" in found:
        return _CAFFEINE_LEAD["coffee"] + _CAFFEINE_TAIL
    return _CAFFEINE_LEAD["coffee"] + _CAFFEINE_TAIL


_TEEN_AGES = ("12", "13", "14", "15", "16", "17", "18")
_TEEN_AGE_PHRASES = tuple(shape % age for age in _TEEN_AGES
                          for shape in ("i am %s", "im %s", "aged %s", "age %s",
                                        "%s year old", "%s years old"))
_COLD_PREVENT = ("prevent", "preventing", "prevention", "ward off", "avoid", "avoiding",
                "keep away", "keeping away", "colds away", "stay well", "keeping well",
                "not catch",
                "coming on", "in its tracks", "catch", "catching", "not get", "dodge",
                "before it",
                "stop a cold", "stop this cold", "stop the cold", "stop my cold", "stops a cold")
_COLD_HELP = ("For a cold, the things that genuinely help are rest, plenty of fluids, honey in "
              "warm water for a cough, and paracetamol or ibuprofen for aches and a sore throat; "
              "steam can ease a blocked nose. Vitamin C, zinc and echinacea have not held up in "
              "trials, nothing cures it, and it usually settles in about a week - see someone if "
              "it lasts longer or you are breathless.")
_COLD_STOP = ("You cannot stop a cold once it has started, and nothing you can buy shortens one "
              "by much: rest, fluids and sleep do more than any remedy. To catch fewer of them, "
              "wash your hands properly and often, use your own cup and towel, keep your sleep up "
              "and stay away from smoke, which is most of what the evidence supports.")


_COLD_NAMED = ("vitamin c", "vitamin", "zinc", "echinacea", "supplement", "tablets", "lemsip")


def _cold_help(memory, understood):
    said = " ".join(str(value) for value in ((understood or {}).get(key)
                                             for key in ("clean", "norm_text", "norm"))
                    if isinstance(value, str)).lower()
    if any(word in said for word in _COLD_NAMED):
        return _COLD_HELP
    if any(word in said for word in _COLD_PREVENT):
        return _COLD_STOP
    return _COLD_HELP


_NUMBER_WORDS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
    "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
    "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
    "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "ninety": 90,
    "a couple of": 2, "couple": 2, "few": 3, "a few": 3, "several": 4, "many": 5,
    "lots of": 5, "ages": 5, "half a": 0,
}
_UNIT_DAYS = {"day": 1, "days": 1, "week": 7, "weeks": 7, "weekend": 2, "fortnight": 14,
              "month": 30, "months": 30}
_BARE_LENGTHS = ("days", "weeks", "months", "days now", "for days", "days on end",
                 "days running", "weeks now", "lasted days", "going on days")
_EVERY_DAY = ("every day", "every single day", "each day", "every morning", "daily",
              "day after day", "every blessed day")


def _headache_days(words):
    said = " ".join(words)
    for phrase in _EVERY_DAY:
        if phrase in said:
            return 3
    best = None
    for at, word in enumerate(words):
        unit = _UNIT_DAYS.get(word)
        if unit is None:
            continue
        count = None
        for back in (1, 2, 3):
            if at - back < 0:
                break
            before = words[at - back]
            if before.isdigit():
                count = int(before)
                break
            if before in ("a", "an"):
                count = 1
                break
            if before in _NUMBER_WORDS:
                count = _NUMBER_WORDS[before]
                break
            if before not in ("a", "an", "of", "the", "this", "last", "past", "few"):
                break
        if count is None:
            if word in ("week", "weeks") and any(one in said for one in
                                                 ("all week", "past week", "last week",
                                                  "over a week", "a week", "this past")):
                count = 7
            elif word in ("day", "days"):
                count = 1 if "all day" in said else None
        if count is None:
            continue
        days = count * unit
        best = days if best is None else max(best, days)
    if best is not None:
        return best
    for phrase in _BARE_LENGTHS:
        if phrase in said:
            return 3
    return None


HEADACHE_DAYS = ("A headache that has gone on for three days or more is one to have looked at: "
                 "book a GP appointment in the next few days rather than keep taking painkillers, "
                 "which can themselves cause a daily headache if used more than two or three days "
                 "a week. Keep a short note of when it comes, what you have taken and how you "
                 "slept - it makes the appointment much more useful.")


def _headache_days_reply(memory, understood):
    words = understood.get("words") or []
    days = _headache_days(words)
    if days is None or days < 3:
        return None
    return HEADACHE_DAYS


_HEADACHE_AFTERNOON = (
    "An afternoon headache is usually tension, a day of screens, too little water or food, or "
    "too much coffee, and paracetamol or ibuprofen with water and a quiet dark room settles "
    "most of them within a few hours. Get one checked the same day if it comes on like a "
    "thunderclap, comes with a fever and a stiff neck, follows a bang on the head, or is the "
    "worst you have ever had.")


def _headache_reply(memory, understood):
    text = ((understood or {}).get("clean") or "").lower()
    if any(phrase in text for phrase in NO_DRUGS):
        return HEADACHE_NO_DRUGS
    return _HEADACHE_AFTERNOON
_HEAVY_PERIOD_WORDS = ("heavy", "heavier", "flooding", "flood", "clots", "clot", "soaking",
                       "soak", "soaked", "a lot", "lots", "seven days", "longer than usual")

_PERIOD_CHANGE_WORDS = ("irregular", "all over the place", "gone mad", "haywire", "skipping",
                        "skipped", "skipping a month", "closer together", "further apart",
                        "every two weeks", "every three weeks", "random", "randomly",
                        "not regular", "unpredictable", "stopped", "stopping", "no period")
PERIOD_CHANGE_REPLY = (
    "Periods that change - closer together, further apart, lighter, or skipped altogether - are "
    "usually perimenopause if you are over 40, and it can go on for years. Check a pregnancy test "
    "first if there is any chance. Keep using contraception until you have gone a full 12 months "
    "with no period, because you can still conceive. Over 40, see a GP about bleeding between "
    "periods, after sex, or a heavy bleed after a year with none; HRT or the pill can settle the "
    "cycle. Under 40, a period that stops needs a GP anyway - thyroid, PCOS and weight loss are "
    "the usual causes.")
NOT_THIS_PERSONS_PERIOD = ("pcos", "pcod", "polycystic", "endometriosis", "thyroid", "coil",
                           "implant", "my wife", "my mum", "my mother", "my nan", "my sister",
                           "my friend", "my daughter", "she is", "she has", "her periods")


def _period_answer(memory, understood):
    words = set(understood.get("words") or ())
    clean = " " + (understood.get("clean") or "").lower() + " "
    if any(word in words or " " + word + " " in clean for word in NOT_THIS_PERSONS_PERIOD):
        return None
    if (not any(word in words or " " + word + " " in clean for word in _HEAVY_PERIOD_WORDS)
            and any(word in words or " " + word + " " in clean
                    for word in _PERIOD_CHANGE_WORDS)):
        return PERIOD_CHANGE_REPLY
    if not any(word in words or " " + word + " " in clean for word in _HEAVY_PERIOD_WORDS):
        return ("Period pain that is bad enough to stop your day is worth taking seriously: "
                "ibuprofen works better than paracetamol for it, started a day before, and heat "
                "on your lower tummy helps. Pain that is getting worse month by month, or that "
                "has started later in life, is the pattern to describe to a GP - it can be "
                "endometriosis, which takes years to get diagnosed if nobody is told.")
    return ("Heavy periods are common and treatable: soaking a pad or tampon every hour, clots "
            "bigger than a 10p coin, or bleeding past seven days are the things to describe to a "
            "GP, who can check for fibroids, thyroid trouble or a copper coil and offer tablets, "
            "the pill or a coil that thins the lining. Eat iron - red meat, beans, fortified "
            "cereal - and go the same day if you are flooding or feel faint.")



HICCUPS_BABY = (
    "Hiccups in a baby or a small child are normal and they do not bother them: feed a little more "
    "upright, burp them, and the hiccups stop on their own within a few minutes. Mention it to a "
    "health visitor or GP if they come with reflux, coughing or trouble feeding.")

HICCUPS_BABY_AGAIN = (
    "Hiccups coming back in a baby are still normal: a feed, a burp or a gulp of air sets them off, "
    "and they need no treatment. If they seem to bother them, stop and wind them partway through a "
    "feed, and keep them upright for a while after. Only reflux, coughing or trouble feeding is "
    "worth a call to the health visitor.")

_BABY_WORDS = ("baby", "babies", "newborn", "newborns", "infant", "infants", "toddler",
               "toddlers", "my son", "my daughter", "my child", "breastfeeding", "bottle feeding")


def _said_before(memory, opening):
    for turn in (memory or {}).get("turns") or ():
        if isinstance(turn, dict) and str(turn.get("bot") or "").startswith(opening):
            return True
    return False


def _hiccups_remedy(memory, understood):
    words = set((understood or {}).get("words") or ())
    if words & set(_BABY_WORDS):
        if _said_before(memory, HICCUPS_BABY[:24]) or _said_before(memory, HICCUPS_BABY_AGAIN[:24]):
            return HICCUPS_BABY_AGAIN
        return HICCUPS_BABY
    return ("Sip cold water slowly, hold your breath for a few seconds, swallow a few times or "
            "breathe into a paper bag, and one of those stops most hiccups within a couple of "
            "minutes. They start when a big meal, a fizzy drink or a laugh pushes the stomach up "
            "against the diaphragm, which is why they pass on their own. A GP can help if they "
            "last more than two days, or come with pain or trouble swallowing.")



STEPS_PISA = "The Leaning Tower of Pisa is 296 steps to the top."
STEPS_EMPIRE = "The Empire State Building is 1,860 steps to the 102nd-floor observatory."
STEPS_PAULS = "St Paul's dome is 528 steps."
STEPS_FLIGHT = ("A single flight between house floors is 12 to 13 steps, and a whole staircase "
                "up to an upstairs flat is usually 14 to 16.")
STEPS_TAIL = "A cathedral or a stadium prints its own count at the entrance."


def _steps_up_a_building(memory, understood):
    said = str((understood or {}).get("clean") or "").lower()
    if "pisa" in said or "leaning tower" in said:
        lead, rest = STEPS_PISA, [STEPS_EMPIRE, STEPS_PAULS, STEPS_FLIGHT]
    elif "empire" in said:
        lead, rest = STEPS_EMPIRE, [STEPS_PISA, STEPS_PAULS, STEPS_FLIGHT]
    elif "paul" in said or "dome" in said or "cathedral" in said:
        lead, rest = STEPS_PAULS, [STEPS_PISA, STEPS_EMPIRE, STEPS_FLIGHT]
    elif any(word in said for word in ("flight", "floor", "storey", "story", "riser",
                                       "stair")):
        lead, rest = STEPS_FLIGHT, [STEPS_PISA, STEPS_EMPIRE, STEPS_PAULS]
    else:
        lead, rest = STEPS_PISA, [STEPS_EMPIRE, STEPS_PAULS, STEPS_FLIGHT]
    return " ".join([lead] + rest + [STEPS_TAIL])


STEPS_A_MILE = (
    "About 2,000 steps to a mile, so 10,000 steps is roughly five miles, a 5k is about "
    "6,500 steps and a marathon is around 55,000. Stride length moves that by around a "
    "tenth either way - a tall walker covers a mile in fewer - so use it for a pedometer "
    "target rather than a measurement.")

STEPS_REPORT_WORDS = ("today", "so far", "yesterday", "already", "just", "did", "done",
                      "walked", "walking", "managed", "clocked", "hit", "reached", "notched",
                      "this morning", "this afternoon", "by lunchtime", "before work")
STEPS_COUNT = re.compile(r"\b(\d{1,3},\d{3}|\d{4,5})\b")


def _steps_in_a_distance(memory, understood):
    said = str((understood or {}).get("clean") or "").lower()
    found = STEPS_COUNT.search(said)
    if found and any(word in said for word in STEPS_REPORT_WORDS):
        count = int(found.group(1).replace(",", ""))
        if 1000 <= count <= 100000:
            miles = round(count / 2000.0, 1)
            if float(miles).is_integer():
                miles = int(miles)
            return ("That's about {} miles - {:,} steps at roughly 2,000 to a mile. A 5k is "
                    "about 6,500 steps and a marathon around 55,000, so that is a proper "
                    "walk.").format(miles, count)
    return STEPS_A_MILE
_A_FOOD_WORD = r"[a-z][a-z'-]*(?: [a-z][a-z'-]*){0,2}"
_HEARTBURN_REPORT_BEFORE = re.compile(
    r"\b(" + _A_FOOD_WORD + r")\s+(?:gives? me|gives|give|sets? off|brings? on|"
    r"triggers?|triggered|does? it to me|do it)\b")
_HEARTBURN_REPORT_AFTER = re.compile(
    r"\b(?:heartburn|acid reflux|reflux|indigestion)\s*,?\s*(?:from|with|off)\s+"
    r"(" + _A_FOOD_WORD + r")")
_HEARTBURN_NOT_A_FOOD = frozenset((
    "i", "me", "it", "this", "that", "them", "they", "we", "you", "he", "she", "my", "the",
    "a", "an", "always", "sometimes", "often", "really", "badly", "awful", "terrible", "food",
    "eating", "everything", "anything", "something", "nothing", "things", "thing", "life",
    "and", "but", "so", "just", "too", "again", "still", "every", "time", "day", "night",
    "loads", "lots", "as", "well", "too much", "a lot", "all the time", "every time",
    "after", "before", "dinner", "lunch", "breakfast", "tea", "supper", "meal", "meals",
    "late", "early", "lately", "recently",
    "a meal", "bed", "going to bed", "lying down", "drinking", "drink",
    "get", "gets", "got", "give", "gives", "gave", "set", "sets", "bring", "brings",
    "trigger", "triggers", "does", "do", "take", "takes", "ate", "eat", "eaten", "drank",
    "stress", "worry", "worrying", "anxiety", "anxious", "being anxious", "work", "life",
    "tiredness", "being tired", "lack of sleep", "no sleep", "my weight", "weight", "being fat",
    "being overweight", "overweight", "age", "getting older", "hormones", "period", "my period",
    "periods", "the pill",
    "heartburn", "heartburns", "reflux", "indigestion", "acid", "burning",
    "what", "which", "why", "food", "foods", "list", "diet", "avoid", "should", "can"))


def _heartburn_blames(said):
    for pattern in (_HEARTBURN_REPORT_BEFORE, _HEARTBURN_REPORT_AFTER):
        found = pattern.search(said or "")
        if not found:
            continue
        words = [w for w in found.group(1).split()
                 if w.strip("'") and w not in _HEARTBURN_NOT_A_FOOD]
        if not words:
            continue
        phrase = " ".join(words[-3:])
        return phrase if names_a_thing(phrase) else ""
    return ""


_HEARTBURN_ANSWER = (
    "An antacid or an alginate (Gaviscon and the like) settles most heartburn within minutes, and "
    "a pharmacy tablet such as omeprazole, taken daily for a fortnight, works better if it keeps "
    "coming back. Eat smaller meals, leave three hours between dinner and bed, and raise the head "
    "of the bed 10 to 15cm. See a GP if it lasts more than three weeks or you find food sticking "
    "on the way down.")
_HEARTBURN_BLAMED = (
    "Cut {} out for a fortnight and see if the heartburn eases; an antacid or an alginate (Gaviscon "
    "and the like) settles a bad night in minutes. Tomato, chilli, onion and garlic, citrus, fried "
    "food, chocolate, mint, coffee and alcohol are the other usual triggers, so smaller meals, three "
    "hours between dinner and bed and the head of the bed 10 to 15cm up do the rest. See a GP if it "
    "lasts more than three weeks.")
_HEARTBURN_PREGNANT = (
    "Heartburn is very common in pregnancy and eases once the baby is born: the hormones relax the "
    "valve at the top of the stomach, and later the baby takes the room. Eat little and often, stay "
    "upright an hour after eating, prop the head of the bed up 10 to 15cm, and try an antacid or an "
    "alginate (Gaviscon and the like) - ask a pharmacist or your midwife before omeprazole. Tell your "
    "midwife if it stops you eating or sleeping.")
_HEARTBURN_PILLS = (
    "Some painkillers set heartburn off - ibuprofen, aspirin and naproxen are the usual three, "
    "because they irritate the stomach lining. Do not just stop a tablet you were prescribed: ask a "
    "pharmacist or your GP whether paracetamol would do instead, and take any of them with food. An "
    "antacid or an alginate settles a bad night in the meantime, and see a GP if it lasts more than "
    "three weeks.")
_HEARTBURN_EAT = (
    "Plain, dry food sits easiest: porridge, rice, bread, bananas, melon, ginger, plain chicken or "
    "fish, and a glass of milk - little and often beats one big meal, and nothing within three hours "
    "of bed. Go steady on tomato, chilli, onion and garlic, citrus, fried and fatty food, chocolate, "
    "mint, coffee and alcohol, since those are the usual triggers. An antacid or an alginate "
    "(Gaviscon and the like) settles a bad night in minutes.")
_HEARTBURN_EAT_WORDS = ("what can i eat", "what should i eat", "what to eat", "what can i have",
                        "what should i have", "foods i can eat", "food i can eat", "safe to eat")
_HEARTBURN_PREGNANT_WORDS = ("pregnant", "pregnancy", "expecting a baby", "having a baby",
                             "with child")
_HEARTBURN_PILL_WORDS = ("ibuprofen", "aspirin", "naproxen", "voltarol", "nurofen", "painkiller",
                         "painkillers", "pain killer", "pain killers", "anti inflammatories",
                         "anti-inflammatory")
_HEARTBURN_TABLETS_NOT_WORKING = (
    "If the antacid is not holding it, a pharmacist can suggest a 14-day course of a PPI - "
    "omeprazole, esomeprazole or lansoprazole, one a day before breakfast - which is what GPs "
    "prescribe first for regular heartburn. Keep off the usual triggers meanwhile and stay upright "
    "for three hours after eating. See a GP if it has gone on three weeks, if you are over 55 and "
    "it is new, or if swallowing is getting hard.")
_HEARTBURN_TREATMENT_WORDS = ("gaviscon", "antacid", "antacids", "ranitidine", "omeprazole",
                              "lansoprazole", "esomeprazole", "ppi", "ppis", "alginate")
_HEARTBURN_TABLETS_WORDS = ("tablets", "tablet", "pills", "pill", "medication", "medicine")
_HEARTBURN_NOT_WORKING_WORDS = ("not working", "arent working", "arent helping", "not helping",
                                "doesnt work", "doesnt help", "no good", "stopped working",
                                "isnt working", "not doing anything")
_HEARTBURN_TEA = (
    "Tea is not one of the usual ones - coffee, alcohol, mint and fizzy drinks are the drinks that "
    "matter most - but tea has caffeine in it too, so a strong cup can loosen the valve the same way "
    "coffee does. If tea is the one thing you always have before it starts, a fortnight without it "
    "will tell you. An antacid or an alginate (Gaviscon and the like) settles a bad night in "
    "minutes.")
_HEARTBURN_TRIGGERS = (
    (("tomato", "tomatoes", "tomato sauce", "passata", "ketchup", "bolognese", "pasta sauce"),
     "Tomato, and anything made with it, is one of the usual triggers, along with chilli, onion, "
     "garlic, citrus, chocolate and alcohol: they loosen the valve at the top of the stomach, so "
     "acid travels back up. Cut back on it for a fortnight and the heartburn usually eases, and "
     "an antacid or an alginate (Gaviscon and the like) settles a bad night within minutes. "
     "See a GP if it lasts more than three weeks."),
    (("spicy", "spice", "spices", "curry", "curries", "chilli", "chilli sauce", "chili", "hot sauce",
      "hot food", "jalapeno", "jalapenos", "vindaloo", "tikka", "naga"),
     "Chilli and curry are the usual triggers, along with onion, garlic, citrus, chocolate and "
     "alcohol: they loosen the valve at the top of the stomach, so acid travels back up. A plain "
     "rice or bread with it soaks some of it up, and an antacid or an alginate (Gaviscon and the "
     "like) settles a bad night within minutes. See a GP if it lasts more than three weeks."),
    (("citrus", "orange", "oranges", "orange juice", "lemon", "lemons", "grapefruit", "lime",
      "satsuma", "clementine"),
     "Citrus is one of the usual triggers, along with tomato, chilli, onion, garlic, chocolate and "
     "alcohol: they loosen the valve at the top of the stomach, so acid travels back up. Cut back "
     "on it for a fortnight and the heartburn usually eases, and an antacid or an alginate "
     "(Gaviscon and the like) settles a bad night within minutes. See a GP if it lasts more than "
     "three weeks."),
    (("onion", "onions", "garlic", "shallot", "shallots", "leek", "leeks"),
     "Onion and garlic are two of the usual triggers, along with tomato, chilli, citrus, chocolate "
     "and alcohol: they loosen the valve at the top of the stomach, so acid travels back up. "
     "Cooking them well softens the effect for a lot of people, and an antacid or an alginate "
     "(Gaviscon and the like) settles a bad night within minutes. See a GP if it lasts more than "
     "three weeks."),
    (("fried", "frying", "fatty", "greasy", "chips", "batter", "pizza", "cheese", "cream",
      "takeaway"),
     "Fried and fatty food is one of the usual triggers, along with tomato, chilli, onion, garlic, "
     "citrus and alcohol: fat slows the stomach down, so the acid has longer to travel back up. "
     "Grilling rather than frying helps, and an antacid or an alginate (Gaviscon and the like) "
     "settles a bad night within minutes. See a GP if it lasts more than three weeks."),
    (("mint", "mint tea", "peppermint", "peppermint tea", "spearmint", "after dinner mint",
      "polos"),
     "Mint is a quiet trigger: it relaxes the valve at the top of the stomach, so the peppermint "
     "tea people drink for a bad stomach can make heartburn worse. Swap it for camomile or ginger, "
     "and an antacid or an alginate (Gaviscon and the like) settles a bad night within minutes. "
     "See a GP if it lasts more than three weeks."),
    (("coffee", "espresso", "latte", "cappuccino", "caffeine", "cola", "energy drink"),
     "Coffee is one of the usual triggers, along with alcohol, tomato, chilli, onion, citrus and "
     "chocolate: caffeine loosens the valve at the top of the stomach, so acid travels back up. "
     "Two cups a day is usually fine and four is usually not, and an antacid or an alginate "
     "(Gaviscon and the like) settles a bad night within minutes. See a GP if it lasts more than "
     "three weeks."),
    (("wine", "beer", "lager", "alcohol", "vodka", "gin", "cider", "prosecco", "whisky",
      "whiskey", "brandy", "cocktail", "cocktails"),
     "Alcohol is one of the usual triggers, along with tomato, chilli, onion, garlic, citrus and "
     "chocolate: it loosens the valve at the top of the stomach, so acid travels back up. Drinking "
     "earlier in the evening and less of it is what helps most, and an antacid or an alginate "
     "(Gaviscon and the like) settles a bad night within minutes. See a GP if it lasts more than "
     "three weeks."),
    (("chocolate",),
     "Chocolate is one of the usual triggers, along with alcohol, tomato, chilli, onion, citrus "
     "and coffee: it loosens the valve at the top of the stomach, so acid travels back up. Keeping "
     "it to the afternoon rather than the evening helps, and an antacid or an alginate (Gaviscon "
     "and the like) settles a bad night within minutes. See a GP if it lasts more than three "
     "weeks."),
)
_HEARTBURN_ASKS = tuple(word for words, _label in _HEARTBURN_TRIGGERS for word in words)


_HEARTBURN_WHY = (
    "A ring of muscle where the food pipe meets the stomach keeps the acid down, and heartburn is "
    "that ring relaxing at the wrong moment so acid travels back up and burns. Big or late meals, "
    "fatty and spicy food, alcohol, coffee, chocolate, mint and extra weight all loosen it. Eating "
    "smaller and earlier, and raising the head of the bed 10 to 15cm, is what settles it; an "
    "antacid or an alginate (Gaviscon and the like) covers a bad night in minutes.")
_HEARTBURN_WHICH = (
    "Tomato and tomato sauces, chilli and curry, onion and garlic, citrus, fried and fatty food, "
    "chocolate, mint, coffee and alcohol are the usual ones, and which of them matter is personal. "
    "Write down what you ate on the bad nights for a fortnight and two or three will stand out; cut "
    "those back and it usually eases, with an antacid or an alginate (Gaviscon and the like) settling "
    "a bad night in minutes.")


def _heartburn(memory, understood):
    said = " ".join(str(value) for value in ((understood or {}).get(key)
                                             for key in ("clean", "norm_text", "norm"))
                    if isinstance(value, str)).lower()
    if _any_hit([r"\b" + re.escape(word) + r"\b" for word in _HEARTBURN_PREGNANT_WORDS], said):
        return _HEARTBURN_PREGNANT
    if (_any_hit([re.escape(word) for word in _HEARTBURN_NOT_WORKING_WORDS], said)
            and _any_hit([r"\b" + re.escape(word) + r"\b"
                          for word in _HEARTBURN_TABLETS_WORDS + _HEARTBURN_TREATMENT_WORDS], said)):
        return _HEARTBURN_TABLETS_NOT_WORKING
    if _any_hit([r"\b" + re.escape(word) + r"\b" for word in _HEARTBURN_PILL_WORDS], said):
        return _HEARTBURN_PILLS
    if _any_hit([r"\b" + re.escape(word) + r"\b" for word in _HEARTBURN_TABLETS_WORDS], said):
        return _HEARTBURN_PILLS
    if _any_hit([r"\b" + re.escape(word) + r"\b" for word in _HEARTBURN_TREATMENT_WORDS], said):
        return _HEARTBURN_ANSWER
    if (re.search(r"\btea\b", said) and not re.search(r"\b(mint|peppermint|spearmint) tea\b",
                                                       said)):
        return _HEARTBURN_TEA
    for words, label in _HEARTBURN_TRIGGERS:
        if _any_hit([r"\b" + re.escape(word) + r"\b" for word in words], said):
            return label
    if _any_hit([re.escape(word) for word in _HEARTBURN_EAT_WORDS], said):
        return _HEARTBURN_EAT
    blamed = _heartburn_blames(said)
    if _any_hit([r"\b" + re.escape(word) + r"\b"
                 for word in ("which", "what foods", "what food", "food", "foods", "diet",
                              "trigger", "triggers", "causes", "cause", "avoid", "cut out",
                              "what should", "list", "what can i eat")],
                said) and not blamed:
        return _HEARTBURN_WHICH
    if _any_hit([r"\bwhy\b", r"\bwhat causes\b"], said):
        return _HEARTBURN_WHY
    if blamed:
        return _HEARTBURN_BLAMED.format(blamed)
    return _HEARTBURN_ANSWER


def _freezing_point(memory, understood):
    line = str((understood or {}).get("clean") or (understood or {}).get("text") or "").lower()
    if re.search(r"slippery|slippy|slips? |slip on|skate|skating|glide", line):
        return ("Ice is slippery because a skate or a boot melts a thin film of water under "
                "it, so you are sliding on water rather than on ice, and the film keeps "
                "refreezing as you go over it. Water freezes at 0C (32F); salt lowers that, "
                "which is why roads are gritted.")
    return WATER_FREEZES


WATER_FREEZES = ("Water freezes at 0C (32F). Salt lowers that, which is why roads are "
                 "gritted, and pressure lowers it too, which is why ice skates glide on a "
                 "thin film of water.")
CALORIE_WORDS = ("calorie", "calories", "kcal", "energy")
TIME_WORDS = ("an hour", "hour", "hours", "minutes", "minute", "mins", "half an hour", "hr",
              "hrs")
STEPS_PER_MILE = 2000.0
STEPS_PER_KM = 1250.0


def _step_count_said(said, default=10000):
    found = STEPS_COUNT.search(said)
    if found:
        count = int(found.group(1).replace(",", ""))
        if 200 <= count <= 100000:
            return float(count)
    return float(default)


def _steps_from_a_distance(said):
    for word, steps in (("mile", STEPS_PER_MILE), ("miles", STEPS_PER_MILE),
                        ("km", STEPS_PER_KM), ("kms", STEPS_PER_KM),
                        ("kilometre", STEPS_PER_KM), ("kilometres", STEPS_PER_KM),
                        ("kilometer", STEPS_PER_KM), ("kilometers", STEPS_PER_KM)):
        if re.search(r"\b" + word + r"\b", said):
            count = re.search(r"(\d+(?:\.\d+)?)\s*" + word + r"\b", said)
            many = float(count.group(1)) if count else 1.0
            return many * steps
    return None


def _steps_from_a_time(said):
    minutes = None
    found = re.search(r"\b(\d+(?:\.\d+)?)\s*(?:hours?|hrs?)\b", said)
    if found:
        minutes = float(found.group(1)) * 60.0
    elif re.search(r"\b(?:an|one|a single)\s+hour\b", said):
        minutes = 60.0
    elif re.search(r"\bhalf an hour\b", said):
        minutes = 30.0
    else:
        found = re.search(r"\b(\d+)\s*(?:minutes|minute|mins|min)\b", said)
        if found:
            minutes = float(found.group(1))
    return 6250.0 * minutes / 60.0 if minutes else None


def _steps_calories(memory, understood):
    said = str((understood or {}).get("clean") or "").lower()
    steps = _steps_from_a_distance(said)
    if steps is None:
        steps = _steps_from_a_time(said)
    if steps is None:
        steps = _step_count_said(said)
    low = int(round(steps * 0.04 / 10.0)) * 10
    high = int(round(steps * 0.05 / 10.0)) * 10
    return ("About {:,} to {:,} calories in {} steps - roughly 0.04 to 0.05 of a calorie a "
            "step, which is the figure for an average adult. It climbs with your weight and "
            "your pace, and it is a small number next to what a snack costs: a biscuit is often "
            "a whole mile's worth, so the walking is for the habit and the heart as much as the "
            "calories.").format(low, high, _said_steps(steps))


def _duration_phrase(minutes):
    if abs(minutes - 60) < 0.5:
        return "an hour"
    if abs(minutes - 30) < 0.5:
        return "half an hour"
    if abs(minutes % 60) < 0.5:
        hours = int(minutes // 60)
        return "%d hour%s" % (hours, "" if hours == 1 else "s")
    return "%d minutes" % int(round(minutes))


def _round_steps(value):
    for step in (1000, 500, 250, 50):
        if value >= step * 4:
            return int(round(value / step) * step)
    return int(round(value))


def _said_steps(value):
    return "{:,}".format(_round_steps(value))


def _steps_in_a_time(memory, understood):
    said = str((understood or {}).get("clean") or "").lower()
    minutes = None
    found = re.search(r"\b(\d+(?:\.\d+)?)\s*(?:hours?|hrs?)\b", said)
    if found:
        minutes = float(found.group(1)) * 60.0
    elif re.search(r"\bhalf an hour\b", said):
        minutes = 30.0
    else:
        found = re.search(r"\b(\d+)\s*(?:minutes|minute|mins|min)\b", said)
        if found:
            minutes = float(found.group(1))
    brisk = bool(re.search(r"\b(brisk|fast|quick|power|uphill|hilly)\b", said))
    ordinary = 6250.0 * (minutes if minutes else 60.0) / 60.0
    quick = 7500.0 * (minutes if minutes else 60.0) / 60.0
    if minutes:
        return ("About %s steps in %s of walking at an ordinary pace, or %s if you are walking "
                "briskly - that is 1,250 steps a kilometre at about 5km/h. Hills, a slow stroll "
                "and short legs all move it."
                % (_said_steps(ordinary), _duration_phrase(minutes), _said_steps(quick)))
    if brisk:
        return ("About %s steps in an hour of brisk walking - 6.5km/h or so, which is 1,250 steps "
                "a kilometre over six and a half of them. An ordinary-paced hour is about %s, and "
                "a slow wander round the shops is well under that."
                % (_said_steps(7500.0), _said_steps(6250.0)))
    return ("About %s to %s steps in an hour of walking: an ordinary pace is about 5km/h, which "
            "is 1,250 steps a kilometre, so an hour gets you five of them. A brisk walk nearer "
            "6.5km/h is the top of that range, and a slow wander round shops is well under it."
            % (_said_steps(6250.0), _said_steps(7500.0)))


BLANK_WORDS = ("what i was saying", "what i was about to say", "what i was going to say",
               "what i wanted to say", "lose my words", "train of thought", "mid sentence",
               "mid-sentence",
               "the word i", "word", "words")


def _forgetting(memory, understood):
    reading = understood if isinstance(understood, dict) else {}
    said = str(reading.get("clean") or reading.get("plain") or "").lower()
    if re.search(r"\b(?:tip of my tongue|the word (?:i|for)|a word for|word for|"
                 r"can'?t find the word|cant find the word|find the words?)\b", said):
        return ("Word-finding blanks are ordinary and commoner when you are tired, stressed or "
                "under pressure: describe the word out loud, or let it go and get on with the "
                "sentence, because it usually turns up a few minutes later once you stop "
                "reaching for it. Run through the alphabet or the first letter if you want to "
                "help it along. If you are losing everyday words often, or the wrong word comes "
                "out and you do not notice, that is worth a word with a GP.")
    if re.search(r"\b(?:saying|say|said|train of thought|mid sentence|mid-sentence|"
                 r"what i was about to)\b", said):
        return ("That is usually not memory loss: a blank mid-sentence comes from being tired, "
                "distracted or holding too much at once, and it passes. Say the last few words "
                "you did get out, or retrace the point you were making, and the rest normally "
                "follows; jotting the thing down before you go on stops it slipping again. If it "
                "starts happening most days, or it comes with losing everyday words and getting "
                "lost in familiar places, see a GP and say how long it has been going on.")
    if re.search(r"\b(?:at work|in work|at the office|work\b|tasks?|to-?do|deadlines?|"
                 r"meetings?|emails?|appointments?|errands?|shopping list|birthdays?)\b", said):
        return ("Keep one list instead of holding it in your head - a notebook or the notes app, "
                "written down the moment it comes up rather than later, because the thing you "
                "mean to remember is the thing that goes. Put a reminder on your phone for "
                "anything with a time on it, and if a thing takes under two minutes do it now "
                "rather than noting it. Keep a fixed place for keys, wallet and phone, and repeat "
                "a name back once when you are introduced. Most of this is too much at once "
                "rather than a fading memory, so sleep and one thing at a time help; if you are "
                "forgetting recent conversations or the names of people you know well, get it "
                "checked.")
    return ("Most forgetting is not a lost file: new memories fade unless they are slept on and "
            "retrieved, and the brain clears out details to keep the gist; being tired, stressed "
            "or trying to hold too much at once makes it worse. Write things down and sleep on "
            "it; if you are forgetting recent conversations or the names of people you know "
            "well, get it checked.")


_SOMETHING_IN_THE_HAIR = ("gum", "chewing gum", "paint", "paints", "resin", "tar", "varnish",
                          "glue", "stuck", "sticky", "lice", "nits", "playdough", "slime",
                          "blu tack", "blue tack", "wax")

_HAIR_NOT_ON_A_HEAD = ("plughole", "plug hole", "plugholes", "plug holes", "drain", "drains",
                       "sink", "sinks", "basin", "blocked", "blockage", "unblock", "trap",
                       "u bend", "u-bend", "waste pipe", "bath", "baths", "bathroom", "shower",
                       "showers", "shower tray", "hairbrush", "hair brush", "hair brushes",
                       "hoover", "vacuum", "vacuumed", "tumble dryer",
                       "pet hair", "dog hair", "cat hair", "fur", "fur ball", "furball",
                       "moulting", "molting", "shedding", "sheds", "upholstery", "sofa",
                       "settee", "carpet", "rug", "car seat", "back seat", "clothes", "clothing",
                       "shirt", "jumper", "coat", "jacket", "duvet", "pillow")

_SMOKE_IS_NOT_A_HABIT = ("brisket", "ribs", "rib", "pork", "pulled pork", "chicken", "turkey",
                         "wings", "sausage", "sausages", "salmon", "haddock", "mackerel", "trout",
                         "fish", "cheese", "tofu", "beef", "steak", "lamb", "duck", "meat",
                         "peppers", "aubergine", "eggplant", "mushrooms", "bacon", "gammon",
                         "ham", "hams", "almonds", "almond", "cashews", "nuts", "salt",
                         "smoke some", "smoke my", "smoke the", "smoking some", "smoked it",
                         "smoke ring", "wood chips", "bark", "smoke a joint", "smoke a pipe",
                         "smoking a joint",
                         "low and slow", "internal temp", "probe")


def _asks_about_itching(understood):
    words = understood.get("words") if isinstance(understood, dict) else None
    text = " ".join(words) if isinstance(words, list) else str(understood or "")
    return any(word in text.split() for word in
               ("itch", "itches", "itchy", "itching", "pick", "picking", "scratch", "scratching"))


def _not_about_itching(understood):
    return not _asks_about_itching(understood)


WHAT_IS_IT = ("what is", "whats a", "what's a", "what are", "what does", "what do", "what makes",
              "why do", "why does", "why is", "how come", "explain", "tell me about",
              "how does", "what happens")

BODY_WHAT = {
    "scab": (("scab", "scabs", "scabbing"),
             ("made of", "made", "form", "forms", "fall off", "falls off", "heal", "heals",
              "healing"),
             "A scab is a plug of dried blood, platelets and a stringy protein called fibrin that "
             "seals a cut while new skin grows underneath it. Leave it alone - it is the dressing - "
             "because picking it off reopens the wound and makes a scar more likely, and the itch "
             "under it is new skin and nerve endings knitting back. A scab with spreading redness, "
             "heat or pus around it is the one to get looked at.",
             ("weeping", "oozing", "smell", "smells", "yellow", "green", "hot", "red", "sore",
              "painful", "knee", "arm", "face", "head", "child", "baby", "bleeding",
              "infected", "infection", "looks infected", "getting infected",
              "mouth", "in my mouth", "in the mouth", "gum", "gums", "tongue", "lip")),
    "blister": (("blister", "blisters", "blistering"),
                ("come from", "form", "forms", "cause", "causes", "heal", "heals"),
                "A blister is fluid trapped under a separated top layer of skin, usually from "
                "friction, heat or a burn, and the fluid is serum protecting the new skin "
                "underneath. Leave it whole and cover it loosely - popping it invites infection - "
                "and if it bursts on its own keep it clean and put a plaster on it. A burn blister "
                "bigger than a 50p, or any blister with spreading redness, wants a pharmacist or GP.",
                ("burns", "burn", "scald", "scalded", "pop", "popped", "popping", "burst",
                 "bursting", "drain", "lance", "should i", "can i",
                 "prevent", "prevents", "preventing", "stop", "stops", "stopping", "avoid",
                 "avoiding", "not get", "from getting",
                 "feet", "foot", "heel", "toe", "shoe",
                 "shoes", "running", "walking", "hand", "finger", "mouth", "cold sore")),
    "plaque": (("plaque",),
               ("teeth", "teeth mean", "gum", "gums", "tartar", "brush", "brushing", "remove",
                "get rid", "build up", "buildup", "cause", "causes", "bad"),
               "Plaque is the soft, sticky film of bacteria that forms on teeth within hours of "
               "brushing, feeding on sugar and making the acid that causes decay and sore gums. "
               "Brushing twice a day with fluoride toothpaste and cleaning between the teeth once "
               "a day shifts it, and once it hardens into tartar only a dentist can scale it off. "
               "Blood on the toothbrush is the sign gum inflammation has started.",
               ("artery", "arteries", "heart", "brain", "skin", "psoriasis",
                "how often", "electric", "toothbrush")),
    "mole": (("mole", "moles"),
             ("check", "checks", "normal", "dangerous", "cancer", "remove", "removed", "new",
              "changing", "changed", "grow", "growing", "itch", "itchy", "bleed", "bleeding"),
             "A mole is a small cluster of pigment cells, the kind you are born with or that "
             "arrive slowly over years, and almost all are harmless. The check is the alphabet "
             "one: Asymmetry, a ragged Border, more than one Colour, a Diameter over 6mm, and "
             "anything Evolving in size, shape or itch. A new dark spot, or a mole that changes "
             "over weeks, wants a GP look rather than a wait.",
             ("on my back", "my back", "shoulder", "arm", "leg", "face", "removed", "shave",
              "garden", "grass", "in the garden", "lawn", "yard")),
    "callus": (("callus", "calluses", "callous"),
               ("form", "forms", "cause", "causes", "remove", "get rid", "treat",
                "hard", "skin", "why"),
               "A callus is thickened skin built where repeated pressure or friction makes the "
               "skin protect itself: hands from tools, weights or a guitar, feet from tight shoes. "
               "File it gently after a bath and use gloves or better-fitting shoes so it stops "
               "coming back, and don't cut it with a blade. A painful hard lump on a foot, or any "
               "foot callus with diabetes, is a podiatrist's job.",
               ("feet", "foot", "heel", "toe", "shoe", "shoes", "running", "diabetes", "hand",
                "hands", "guitar", "weight", "weights", "deadlift", "gym",
                "painful", "pain", "hurts", "hurt", "sore", "aching", "aches", "bleeding",
                "cracked", "split", "infected")),
    "cough": (("cough", "coughs", "coughing"),
              ("dry", "chesty", "wet", "cause", "causes", "why", "what does", "mean",
               "normal", "how long", "last"),
              "A cough is a reflex that clears the airway: a quick breath in, the vocal cords "
              "shut, and air is forced out to shift mucus, dust or an irritant. Most coughs after "
              "a cold are viral and settle in two to three weeks, and honey in warm water eases "
              "the tickle. A cough with breathlessness, blood, chest pain, or one that lasts over "
              "three weeks needs a GP.",
              ("child", "baby", "kid", "toddler", "son", "daughter", "night", "at night",
               "cant stop", "can't stop", "wont stop", "won't stop", "medicine", "syrup",
               "antibiotic", "antibiotics", "get rid", "stop", "treat", "smoker", "smoking",
               "vape", "asthma", "covid", "chest infection", "fever")),
    "immunity": (("immunity", "immune system", "immune"),
                 ("how does", "how do", "what is", "work", "works", "build", "boost",
                  "stronger", "low", "weak", "mean"),
                 "Immunity is your body's memory of a germ: white blood cells that have met a "
                 "virus or a vaccine keep a record of its shape, so the next meeting is fought off "
                 "before it makes you ill. That is why some illnesses you only get once and why a "
                 "vaccine works without the disease, and why some of it fades over years - which "
                 "is what tetanus and flu boosters are for.",
                 ("boost", "boosting", "supplement", "supplements", "vitamin", "vitamins",
                  "weak", "compromised", "autoimmune", "hiv", "chemo", "steroid", "steroids")),
    "stitch": (("stitch", "stitches"),
               ("what is", "whats a", "what's a", "explain", "mean"),
               "A stitch is a cramp-like pain in the side, from the diaphragm and the ligaments "
               "holding it being pulled while you breathe hard - most often in running. Slow down, "
               "breathe out fully, and press a hand into the sore spot; it usually eases in a "
               "minute or two, and building distance up gradually stops it coming back. Pain that "
               "stays after you stop, or comes with vomiting, is not a stitch.",
               ("get rid", "stop", "prevent", "why", "cause", "causes", "running", "run",
                "when i run", "while running", "side", "in my side", "in the side", "avoid",
                "wound", "cut", "surgery", "operation", "scar", "healing", "after birth",
                "perineum", "dissolvable", "removed", "nurse", "hospital", "a&e", "children",
                "child", "knitted")),
    "tonsils": (("tonsils", "tonsil"),
                ("what are", "what do", "do", "for", "removed", "out", "why"),
                "The tonsils are two lumps of lymph tissue at the back of the throat that catch "
                "germs coming in through the mouth and nose, and they swell while they are "
                "fighting an infection. They shrink with age, which is why an adult's are small; "
                "very large ones in a child that cause snoring or pauses in breathing, or "
                "tonsillitis again and again, are what gets a referral.",
                ("swollen", "swelling", "big", "large", "enlarged", "lumpy",
                 "sore", "painful", "hurts", "hurt", "throat", "swallowing", "fever", "white",
                 "spots", "pus", "child", "son", "daughter", "kid", "tonsillitis", "antibiotic",
                 "antibiotics", "should i", "get them")),
    "sneeze": (("sneeze", "sneezes", "sneezing"),
               ("why", "cause", "causes", "what", "happen", "happens", "twice", "three times",
                "in a row", "sunlight", "light"),
               "A sneeze is a reflex that clears the nose: dust, pollen or a virus irritates the "
               "lining and the body takes a sharp breath and blasts air out to shift it. The droplets fly several "
               "metres, which is why you catch it in your elbow rather than your hand, and bright "
               "light makes some people sneeze.",
               ("cant stop", "can't stop", "wont stop", "won't stop", "hayfever", "hay fever",
                "allergy", "allergies", "pollen", "cold", "flu", "covid", "snot", "blocked",
                "medicine", "antihistamine", "tablet", "tablets", "sun", "sunlight", "sunshine",
                "light", "bright", "in the sun", "in the light", "photic")),
}

_SUN_FACTORS = ("15", "20", "25", "30", "40", "50", "60", "70", "90", "100")


def _a_factor_question_without_the_sun(understood):
    if not isinstance(understood, dict):
        return True
    text = str(understood.get("clean") or "").lower()
    if "factor" not in text:
        return True
    if any(word in text for word in ("sun", "spf", "suncream", "sun cream", "sunscreen",
                                     "sunblock", "sun factor")):
        return True
    words = text.replace("?", " ").replace(",", " ").replace(".", " ").split()
    numbers = [word for word in words if word.isdigit()]
    if len(numbers) > 1 or ("of" in words and numbers):
        return False
    if numbers and ("divisible" in words or "have" in words or "has" in words):
        return False
    if any(number not in _SUN_FACTORS for number in numbers):
        return False
    return not any(word in text for word in ("multiple", "multiples", "highest", "common"))


def _a_burn_without_the_sun(understood):
    if not isinstance(understood, dict):
        return True
    text = str(understood.get("clean") or "").lower()
    if not any(word in text for word in ("burn", "burns", "burning", "burnt")):
        return True
    return any(word in text for word in ("sun", "sunlight", "sunshine", "sun cream", "suncream",
                                         "sunscreen", "sunblock", "spf", "uv", "sunbed",
                                         "sunbed", "sun factor", "factor 30", "factor 50"))


DIZZY_SPELL = (
    "Sit or lie down the moment it starts, with your feet up, and drink a glass of water: most "
    "spells are the blood pressure dipping, not enough to drink, a skipped meal, being too hot, or "
    "a passing virus, and they pass in a minute. Get up in stages from now on, and eat something "
    "if it has been hours. See a GP if it keeps happening, if your hearing changes or rings with "
    "it, or if it happens lying down too.")


def _a_dizzy_spell(memory, understood):
    if memory.get("safety_case") and not memory.get("safety_safe"):
        return ""
    return DIZZY_SPELL

POUNDS_THAT_ARE_MONEY = re.compile(
    r"\b(?:a tip|the tip|tip on|tip the|tips? for the|tipping|gratuity|service charge|"
    r"bill|bills|receipt|pence|quid|price|prices|cost|costs|costing|charge|charges|fee|fees|"
    r"pay|paid|paying|spend|spent|percent|percentage)\b|£|\$|€", re.I)


def _the_pounds_are_weight(understood):
    if not isinstance(understood, dict):
        return True
    text = str(understood.get("clean") or understood.get("text") or "")
    return not POUNDS_THAT_ARE_MONEY.search(text)


AN_AMOUNT_OF_IT = re.compile(r"\bhow (?:much|many|long|often)\b", re.I)
WHAT_IS_REMEMBERED = re.compile(
    r"\b(?:forget\w*|forgot\w*|forgotten|memor\w+|remember\w*|things?|stuff|names?|words?|"
    r"anything|everything|dates?|numbers?|birthdays?|faces?|keys?|passwords?)\b", re.I)


LOSING_SOMETHING_ELSE = re.compile(
    r"\b(?:lose|loses|losing|lost)\s+(?:the\s+|my\s+|our\s+|your\s+)?"
    r"(?:temper|patience|plot|mind|head|sleep|hair|voice|job|jobs|home|house|flat|"
    r"game|games|money|deposit|match|matches|argument|arguments|bet|race)\b", re.I)


def _an_amount_of_losing(understood):
    if not isinstance(understood, dict):
        return True
    text = str(understood.get("clean") or understood.get("text") or "")
    if LOSING_SOMETHING_ELSE.search(text):
        return False
    if not AN_AMOUNT_OF_IT.search(text):
        return True
    return bool(WHAT_IS_REMEMBERED.search(text))


_WHAT_WATER_IS = (
    "Water is H2O: two hydrogen atoms to one oxygen. It is wet because its molecules pull on each "
    "other and on most surfaces, so a drop spreads into a thin film instead of beading up - which "
    "is why water creeps along glass and soaked paper, and why it beads on a waxy leaf.")

WATER_IS_THE_SUBJECT = frozenset("""
    a about actually an and answer are as ask at be been being called can chemical chemistry
    composed composition consist consists define defined definition describe description do does
    earth element elements exactly explain explained for formula from h2o how in is it its it's
    kind made make makes made mean meaning molecule molecules name of on or out physical physics
    plain please really s science simple simply so sort substance substances tell terms than that
    the then there thing things this to up water waters what whats what's when where which who
    why you your
""".split())


def _water_is_the_subject(understood):
    if not isinstance(understood, dict):
        return True
    words = [str(word).lower() for word in (understood.get("words") or ())]
    return not [word for word in words if word not in WATER_IS_THE_SUBJECT]
_COLD_FOOD = re.compile(
    r"cold (?:rice|pizza|chicken|pasta|potato|potatoes|noodles?|chips|meat|sausages?|beans|curry|"
    r"stew|takeaway|sandwich)\b|\bleft ?overs?\b|\bleft over rice\b", re.I)


def _not_a_food_cold(understood):
    if (understood or {}).get("warmth"):
        return False
    said = str((understood or {}).get("text") or (understood or {}).get("clean") or "")
    return not _COLD_FOOD.search(said)


_A_AGE = re.compile(
    r"\b(?P<n>\d{1,2}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|eighteen)"
    r"\s*(?P<unit>-?month|-?week|-?year)s?\s*old\b")
_A_NUMBER_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
                   "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "eighteen": 18}
_A_WORRY = re.compile(
    r"\b(?:a lot|too much|all the time|all day|so much|more than usual|always sleeping|"
    r"sleeping loads|sleeps loads)\b")
_BABY_SLEEP_BANDS = (
    (0, 3, "a newborn sleeps 15 to 17 hours a day in stretches of two to four hours, day and "
           "night mixed together"),
    (3, 7, "a three to six month old sleeps about 14 to 16 hours over the 24, in three or four "
           "naps"),
    (7, 10, "a six to nine month old sleeps about 14 hours over the 24, usually in two or three "
            "naps plus eleven or so at night"),
    (10, 13, "a nine to twelve month old sleeps about 12 to 15 hours over the 24, in two naps "
             "and eleven or twelve at night"),
    (13, 36, "a one to three year old sleeps 11 to 14 hours over the 24, usually with one nap "
             "after lunch that drops somewhere between two and four"),
    (36, 72, "a three to five year old sleeps 10 to 13 hours a night, and most have given the "
             "nap up by five"),
)
_BABY_SLEEP_TAIL = ("What matters is feeding and nappies: six or more wet a day and steady "
                    "weight gain, and a call to the health visitor if they are hard to wake for a "
                    "feed.")
_BABY_SLEEP_PLAIN = ("A baby sleeping a lot is usually fine: a six-week-old still sleeps 15 to 17 "
                     "hours a day, in stretches of two to four hours, and a growth spurt makes "
                     "them sleepier for a few days. " + _BABY_SLEEP_TAIL)
_BABY_SLEEP_TAIL_UNDER_MONTHS = 12.0


def _the_age_in_months(said):
    found = _A_AGE.search(said)
    if not found:
        return None
    number = found.group("n")
    count = _A_NUMBER_WORDS.get(number, None)
    if count is None:
        try:
            count = int(number)
        except (TypeError, ValueError):
            return None
    if count <= 0:
        return None
    unit = found.group("unit").replace("-", "")
    if unit == "week":
        return count / 4.345
    if unit == "year":
        return count * 12
    return float(count)


def _a_baby_sleep_reply(memory, understood):
    said = " ".join(str(understood.get("text") or understood.get("clean") or "").lower().split())
    if not said:
        said = " ".join(str((memory or {}).get("turns", [{}])[-1].get("text", "")).lower().split())
    months = _the_age_in_months(said)
    if months is None and re.search(r"\btoddlers?\b", said):
        months = 18.0
    if months is None:
        return _BABY_SLEEP_PLAIN
    band = None
    for low, high, line in _BABY_SLEEP_BANDS:
        if low <= months < high:
            band = line
            break
    if band is None:
        return _BABY_SLEEP_PLAIN
    tail = _the_baby_sleep_tail(months)
    if _A_WORRY.search(said):
        opening = ("A baby sleeping a lot is usually fine: " if tail
                   else "Sleeping a lot is usually fine: ")
        return (opening + band + "." + tail)
    return (band[0].upper() + band[1:] + "." + tail)


def _the_baby_sleep_tail(months):
    if months is not None and months >= _BABY_SLEEP_TAIL_UNDER_MONTHS:
        return ""
    return " " + _BABY_SLEEP_TAIL
FEMUR_RECORD = (
    "The thigh bone, the femur, is the strongest: it takes about 30 times your body weight "
    "lengthwise before it breaks, and it is also the longest bone in the body. It breaks across "
    "the shaft rather than along it, which is why a car bumper at knee height is such a common "
    "way to break one.")
STAPES_RECORD = (
    "The stapes, one of the three tiny bones in the middle ear: about 3mm long and lighter than "
    "a grain of rice. It passes the vibration of the eardrum on to the inner ear, and the three "
    "ear bones together are the smallest in the body. Because they are so small, a hard blow to "
    "the side of the head can break them.")
ENAMEL_RECORD = (
    "Tooth enamel, the outer layer of the teeth: harder than bone, and it is the only part of you "
    "that cannot repair itself, because it is not living tissue. That is why acid and grinding do "
    "permanent damage while a broken bone heals. Fluoride makes it a little more acid-resistant, "
    "which is most of what a fluoride toothpaste does.")
TEETH_RECORD = (
    "An adult has 32 teeth including the four wisdom teeth, and a child has 20 milk teeth, which "
    "start arriving at about six months and are all replaced by about 12. The wisdom teeth come "
    "last, in the late teens or twenties, and roughly a third of people never get room for all "
    "four, which is why so many are removed.")
MUSCLES_RECORD = (
    "About 600 skeletal muscles - the ones you can move on purpose - and something like 650 in "
    "all once the smooth muscle in the gut, blood vessels and bladder is counted. They are "
    "roughly 40% of your body weight, and the strongest for its size is the masseter, the muscle "
    "that closes the jaw.")
FINGERPRINT_RECORD = (
    "Fingerprints are ridges that form in the womb, and they help in two ways: the ridges give "
    "grip on a wet or smooth surface, the way a treaded tyre does, and they put the touch "
    "receptors closer to whatever you are handling, which is why a fingertip can feel a hair on "
    "a page. The pattern is set before birth and is different even in identical twins.")

FEMUR_LENGTH = (
    "The thigh bone, the femur, is the longest bone in the body - about a quarter of your height, "
    "so roughly 45cm in a 1.8m adult. The shortest is the stapes, deep in the ear, at about 3mm.")
FEMUR_BIGGEST = (
    "The thigh bone, the femur, is the biggest bone in the body: about 45cm long in a 1.8m adult, "
    "a quarter of your height, and it takes roughly 30 times your body weight lengthwise before "
    "it breaks, which also makes it the strongest. It breaks across the shaft rather than along "
    "it, which is why a car bumper at knee height is such a common way to break one.")
SARTORIUS_RECORD = (
    "The longest muscle is the sartorius, the thin one that runs from the outside of the hip "
    "across the front of the thigh to the inside of the knee - about 50cm, the longest in the "
    "body. It is the muscle that lets you sit cross-legged, and it is not a strong one: it is "
    "long and thin, and its job is to swing and turn the leg rather than to carry weight.")
STRONGEST_MUSCLE = (
    "The strongest muscle for its size is the masseter, the one that closes your jaw: the back "
    "teeth can bite with about 70kg of force, and the muscle is the strongest there is per square "
    "centimetre. The most powerful overall is the gluteus maximus in your backside, the muscle "
    "that stands you up and drives you upstairs.")
GLUTEUS_RECORD = (
    "The biggest muscle is the gluteus maximus, the large one in your backside: it is the most "
    "powerful muscle in the body and the one that straightens the hip when you stand up, climb "
    "stairs or run. The longest is a different one - the sartorius, the thin muscle that runs "
    "across the front of the thigh.")

_GENERIC_PARTS = ("substance", "thing", "part", "material")
_FINGER_WORDS = ("finger", "fingers", "fingertip", "fingertips", "hand", "hands", "thumb")
_SAYS_A_BODY = ("body", "bodies", "human", "humans", "animal", "mammal")
_AN_ANIMAL = ("horse", "horses", "cow", "cows", "sheep", "pig", "pigs", "dog", "dogs",
              "cat", "cats", "puppy", "puppies", "kitten", "kittens", "rabbit", "rabbits",
              "hamster", "bird", "birds", "fish", "paw", "paws", "beak", "beaks",
              "tail", "tails", "animal", "animals", "pet", "pets")


BODY_RECORDS = (
    (("bone", "bones", "thigh bone", "femur"),
     ("strongest", "sturdiest"), FEMUR_RECORD),
    (("bone", "bones", "thigh bone", "femur"),
     ("biggest", "largest", "heaviest", "thickest"), FEMUR_BIGGEST),
    (("bone", "bones", "thigh bone", "femur"),
     ("longest", "tallest", "length"), FEMUR_LENGTH),
    (("bone", "bones", "ear"),
     ("smallest", "tiniest", "littlest", "shortest", "smallest bone"), STAPES_RECORD),
    (("substance", "thing", "part", "material", "enamel", "tooth enamel"),
     ("hardest", "toughest", "strongest"), ENAMEL_RECORD),
    (("teeth", "tooth", "adult teeth", "milk teeth"),
     ("how many", "many", "number", "count", "adults", "adult", "children", "kids", "baby",
      "people"), TEETH_RECORD),
    (("muscle", "muscles"), ("longest", "length"), SARTORIUS_RECORD),
    (("muscle", "muscles"), ("strongest",), STRONGEST_MUSCLE),
    (("muscle", "muscles"), ("biggest", "largest", "heaviest"), GLUTEUS_RECORD),
    (("muscle", "muscles"),
     ("how many", "many", "number", "count"), MUSCLES_RECORD),
    (("fingerprint", "fingerprints", "fingertips", "finger tips", "prints"),
     ("why", "what for", "what are", "purpose", "for", "how"), FINGERPRINT_RECORD),
)

_RECORD_ASK = ("what", "whats", "what's", "which", "why", "how", "many", "much", "biggest",
               "strongest", "smallest", "longest", "hardest", "number", "count", "is", "the",
               "have", "has", "do", "does", "we", "my", "body", "adults", "adult", "people",
               "for", "what for", "purpose")


def _what_the_body_is_like(memory, understood):
    text = " " + str(((understood or {}).get("clean")
                      or (understood or {}).get("text") or "")).strip().lower() + " "
    def said(word):
        return re.search(r"\b" + re.escape(word) + r"\b", text) is not None

    if any(said(word) for word in _AN_ANIMAL) and not said("human"):
        return None
    body_said = any(said(word) for word in _SAYS_A_BODY)
    for parts, asks, reply in BODY_RECORDS:
        named = [word for word in parts if said(word)]
        if not named or not any(word not in _GENERIC_PARTS for word in named) and not body_said:
            continue
        if "prints" in named and not any(said(word) for word in _FINGER_WORDS):
            continue
        if any(said(word) for word in asks):
            return reply
    return None


def _the_body_record_key():
    subjects = tuple(word for parts, _asks, _reply in BODY_RECORDS for word in parts)
    return subjects


_A_A_COLD = re.compile(r"\bcolds?\b|\bflu\b|\bsniffles?\b")

HAYFEVER_ADVICE = ("A once-a-day non-drowsy antihistamine (cetirizine or loratadine) is the usual "
                   "first step, and a steroid nasal spray from the pharmacy works better if your "
                   "nose is the worst part, started a week or two before your season begins. Shower "
                   "and change when you come in, keep windows shut in the morning and around midday "
                   "when the count peaks, and dry washing indoors.")


def _hayfever_or_a_cold(memory, understood):
    said = " ".join(str((understood or {}).get(key) or "")
                    for key in ("clean", "text", "norm_text", "plain")).lower()
    if _A_A_COLD.search(said):
        return ("Hay fever itches - eyes, nose, throat, the roof of your mouth - and comes in "
                "sneezing fits with no fever, in the same weeks each year. A cold starts with a "
                "sore throat, then a blocked nose, a cough and often a mild fever, and clears in "
                "about a week. In June grass pollen is the usual one, so a week of antihistamine "
                "is the test.")
    return HAYFEVER_ADVICE


_VOLCANO_CAUSE = re.compile(r"\b(?:what|that|which|why)\s+(?:makes|make|made|causes|cause)\b|"
                             r"\bwhy\s+(?:do|does|did)\b", re.I)
_VOLCANO_BUILD = re.compile(
    r"\b(?:make|makes|making|made|build|builds|building|built|model|models|project|projects)"
    r"\s+(?:(?:a|an|the|my|our|your|one)\s+)?(?:model\s+|paper\s+|own\s+)?volcano", re.I)


def _not_a_volcano_build(understood):
    said = understood if isinstance(understood, dict) else {}
    text = " " + str(said.get("text") or said.get("clean") or " ".join(said.get("words") or ())) + " "
    if not _VOLCANO_BUILD.search(text):
        return True
    return bool(_VOLCANO_CAUSE.search(text))
_SITTING_KIT = frozenset((
    "chair", "chairs", "desk", "desks", "screen", "screens", "monitor", "monitors", "keyboard",
    "keyboards", "mouse", "mousemat", "laptop", "workstation", "office", "seat", "seating",
    "armrest", "armrests", "footrest", "posture", "slouch", "slouching", "setup",
))

_A_PLACE_SHAPED = ("where should", "where do i", "where does", "how high", "how low",
                   "too low", "too high", "set up", "setting up", "set my", "should my")

def _a_place_for_the_kit(understood):
    understood = understood or {}
    clean = " ".join(str(understood.get("clean") or "").split())
    if not clean:
        return False
    if not any(phrase in clean for phrase in _A_PLACE_SHAPED):
        return True
    return bool(set(clean.split()) & _SITTING_KIT)



_ICE_WHEN = re.compile(r"\b(?:how\s+long|how\s+many\s+(?:minutes|hours)|how\s+quickly|"
                       r"how\s+fast|time\s+to|take\s+to)\b", re.I)


def _how_long_ice_takes(understood):
    why = ("Ice melts when its molecules take in enough heat from the room or the air to break "
           "free of the fixed lattice they are locked in and slide around as liquid. It stays at "
           "0C the whole time it is melting, because the heat goes into loosening the bonds "
           "rather than raising the temperature.")
    text = " " + str(understood.get("clean") or understood.get("text") or "") + " "
    if not _ICE_WHEN.search(text):
        return why
    when = ("An ice cube on the counter is gone in about half an hour in a warm kitchen, and a "
            "whole tray left out takes a few hours. In a drink it is quicker still, a few minutes, "
            "because the drink is warmer than the freezer. ")
    return when + why


_BRUISE_PLAIN = (
    "A bruise is blood leaking under the skin from small vessels broken by a knock, which is "
    "why it turns purple, then green, then yellow as the blood is cleared away. It fades on "
    "its own in one to two weeks, and a cold pack for twenty minutes with a cloth round it, a "
    "few times in the first two days, keeps it from spreading and eases the throbbing. "
    "If a bruise turns up with no injury behind it, or you bruise far more easily "
    "than you used to, get it checked: that is worth a blood test.")

_BRUISE_SPREADING = (
    "A bruise does spread a little in the first day or two, as the blood that leaked tracks "
    "along under the skin, and the colour drifting outwards is that blood being cleared rather "
    "than a new injury. Cold for twenty minutes at a time, with a cloth round the pack, for the "
    "first day or two, keeps the swelling down. Get it looked at if it is still growing after "
    "two days, if it goes hard, tight and hot, or if it came up without a knock.")

_BRUISE_FASTER = (
    "Cold is what speeds a bruise up: a cold pack for twenty minutes at a time, a cloth round "
    "it, a few times a day for the first two days, then time - and raise the limb on a cushion "
    "when you sit. It still fades over one to two weeks through purple, green and yellow, and no "
    "cream honestly changes that; arnica has little evidence behind it. Take paracetamol rather "
    "than aspirin or ibuprofen, which thin the blood and can make the bruising worse.")

_BRUISE_STAYS = (
    "A bruise that is still there after two weeks has stopped being an ordinary bruise: blood "
    "under the skin is cleared away in one to two weeks, so one that will not fade, or that keeps "
    "coming back in the same place, is worth showing to a GP. The same goes for bruising that "
    "arrives with no knock behind it, or bruising far more easily than you used to - that is a "
    "blood test, and it is a quick one. While you wait, treat it as any bruise: cold for twenty "
    "minutes at a time, a cloth round the pack, for the first day or two.")

_BRUISE_HURTS = (
    "A bruise hurts because the blood that leaked under the skin is pressing on the tissue "
    "around it, and that tightness eases over the first day or two as the blood settles and "
    "starts to clear. Cold for twenty minutes at a time, with a cloth round the pack, takes the "
    "throb down, and paracetamol is the painkiller to reach for: aspirin and ibuprofen thin the "
    "blood and can make the bruise bigger. Get it seen if the pain is worse rather than better "
    "after two days, or the area goes hard, hot and tight.")

_BRUISE_ASKS = (
    (("spread", "spreading", "spreads", "growing", "bigger", "larger", "getting worse"),
     _BRUISE_SPREADING),
    (("wont go", "won't go", "not going", "doesnt fade", "doesn't fade", "not fading",
      "still there", "still here", "keeps coming back", "keeps coming", "for weeks",
      "months", "lasts", "lasting"),
     _BRUISE_STAYS),
    (("hurts", "hurt", "hurting", "pain", "painful", "throbbing", "sore", "aching", "ache"),
     _BRUISE_HURTS),
    (("faster", "quicker", "quickly", "quick", "get rid", "go away", "clear up", "heal",
      "healing", "fade", "treat", "treatment", "help"),
     _BRUISE_FASTER),
)


def _the_bruise_answer(memory, reading):
    text = " " + str(reading.get("text") or reading.get("clean") or "").lower() + " "
    for words, answer in _BRUISE_ASKS:
        for word in words:
            if " " + word + " " in text.replace("?", " ").replace(".", " ").replace(",", " "):
                return answer
    return _BRUISE_PLAIN


def _the_backs_are_a_body(understood):
    from .body import _back_is_a_direction

    return not _back_is_a_direction(understood)


ENTRIES = [
    entry("sky-blue", ("sky", ("blue", "colour", "color", "rayleigh")),
          "Sunlight contains every colour, and air scatters the short blue wavelengths far more "
          "than the long red ones, so blue light reaches your eyes from all over the sky. That is "
          "also why the sky reddens at sunset: the light crosses more air, the blue is scattered "
          "away, and the reds come through.",
          avoid=("night", "dark", "black")),
    entry("sky-dark", ("sky", ("dark", "black", "night")),
          "Night is simply the side of the Earth turned away from the Sun: with no sunlight to "
          "scatter, the sky is dark. The stars are there all day too, but the bright blue "
          "scattered light drowns them out.",
          avoid=("blue",)),
    entry("sky-green", (("sky",), ("not green", "never green", "isnt", "isn't", "never")),
          "Blue is scattered much more strongly than green, so the green that is scattered "
          "arrives mixed with far more blue and the sky reads as pale blue. Violet is scattered "
          "even more, but there is less of it in sunlight and our eyes are less sensitive to it, "
          "so it never dominates.",
          avoid=("blue",),
          ask=("why", "what", "colour", "color", "not", "green", "isnt", "isn't")),
entry("gas-flame-blue", (("gas flame", "gas hobs", "gas hob", "blue flame", "hob flame",
                             "flame on the hob", "boiler flame", "pilot light", "burner flame",
                             "yellow flame", "orange flame", "cooker flame", "flame yellow",
                             "flame orange", "flame is yellow", "flame is orange",
                             "flame on my cooker", "flame on the cooker"),
                            ("why", "blue", "yellow", "orange", "colour", "color", "mean", "means",
                             "normal", "safe", "should", "too much", "air")),
          "A blue gas flame is the clean one: blue means the gas is mixing with plenty of air, so "
          "it burns hot and leaves almost no soot. Yellow or orange tips mean it is short of air "
          "and burning dirty, which can give off carbon monoxide, so have the hob or boiler "
          "serviced, keep the vents clear and put a carbon monoxide alarm nearby.",
          avoid=("smell", "smells", "smelling", "leak", "leaking", "rotten", "egg", "boiler is",
                 "not lighting", "wont light", "won't light", "pilot light gone", "bill",
                 "meter", "pressure", "radiator", "radiators", "cooker", "oven", "barbecue",
                 "bbq", "camping", "stove", "lighter", "welding", "fireworks", "birthday",
                 "candle", "candles", "wood", "log", "logs", "fire", "fires", "campfire",
                 "bonfire", "torch", "lamp", "lantern", "match", "matches")),
    entry("sunset-red", (("sunset", "sunrise", "dusk", "dawn", "sun", "low sun"),
                         ("red", "orange", "pink", "yellow", "white", "colour", "color")),
          "Sunlight is white, but the air scatters the blue end of it away, so the Sun looks "
          "yellow and, low down, orange or red. At sunset the light crosses much more air, which "
          "takes out the blue and lets the reds through; dust and cloud deepen it.",
          avoid=("hot", "heat", "burn", "burning", "sunburn", "sun cream", "sunscreen",
                 "screen", "exposure", "vitamin", "lamp", "bed")),
    entry("moon-size", (("moon",),
                         ("how big", "how large", "size", "diameter", "across", "wide",
                          "bigger than", "bigger")),
          "The Moon is about 3,475 km across, a little over a quarter of the Earth's width, and "
          "you could fit about 50 Moons inside the Earth. It looks small only because it is about "
          "384,000 km away.",
          avoid=("photo", "photos", "photograph", "picture", "pictures", "camera", "phone",
                 "shoot", "capture", "zoom", "lens", "telescope", "horizon"),
          bias=2),
    entry("sun-times", (("sun", "sunrise", "sunset", "sun sets", "sun set", "sun comes up",
                         "sun come up", "sun goes down", "sun go down", "gets dark", "get dark"),
                        ("what time does the sun", "what time is sunrise", "what time is sunset",
                         "what time is the sunrise", "what time is the sunset",
                         "when does the sun", "when is sunrise", "when is sunset",
                         "when will the sun", "sunrise time", "sunset time",
                         "what time does it get dark", "what time does it go dark",
                         "when does it get dark", "when will it get dark",
                         "what time does it get light", "when does it get light",
                         "time of sunrise", "time of sunset",
                         "how long until sunrise", "how long until sunset",
                         "how long till sunrise", "how long till sunset",
                         "how long to sunrise", "how long to sunset")),
          "The exact time depends on where you are and the date, so I cannot give you the clock "
          "time: a weather app or the Met Office page for your postcode has it, along with "
          "tomorrow's. Sunrise moves only a minute or two a day, but the gap between sunrise and "
          "sunset swings by hours across the year.",
          avoid=("alarm", "lamp", "light therapy", "wake up light", "wake-up light",
                 "red", "orange", "pink", "colour", "color", "glow")),
    entry("sunrise-east", (("sun", "sunrise", "sunset"),
                           ("rise", "rises", "rising", "set", "sets", "setting",
                            "east", "west", "go down", "goes down")),
          "The Sun does not move round the Earth: the Earth spins from west to east, so the Sun "
          "appears to come up in the east, cross the sky and set in the west. The ground is "
          "turning under you at about 1,000 mph at the equator.",
          avoid=("red", "orange", "pink", "colour", "color", "glow", "alarm", "lamp",
                 "light therapy", "wake up light", "wake-up light",
                 "what time", "when does", "when is", "time does")),
    entry("space-dark", ("space", ("dark", "black", "why")),
          "Space looks black because there is almost nothing there to scatter light into your "
          "eyes; light only reaches you if it comes straight from a star or a lit object. The "
          "sky is bright blue from Earth because our air scatters sunlight everywhere."),
    entry("sun-hot", (("sun",), ("hot", "heat", "why", "energy", "temperature")),
          "About 5,500C at the surface and around 15 million C at the core, hot enough to fuse "
          "hydrogen into helium. That reaction is what makes the heat: the Sun's own gravity "
          "squeezes the hydrogen together, and the energy crosses space as light.",
          avoid=("burn", "sunburn", "burning",
                 "today", "outside", "out there", "right now", "at the moment", "this heat",
                 "heatwave", "weather", "hot day",
                 "flat", "house", "home", "room", "bedroom", "kitchen", "office", "indoors",
                 "inside", "in here", "my place", "our place", "windows", "curtains"),
          ask=("hot", "heat", "temperature", "boil", "energy", "warm"),
          bias=2),
    entry("lava-hot",
          (("lava", "magma"), ("hot", "heat", "temperature", "how hot", "degrees", "celsius",
                               "fahrenheit")),
          "About 700 to 1,200C, or 1,300 to 2,200F, depending on the rock: basalt runs hottest and "
          "flows fastest, while the thick slow lava of a volcano like Etna is cooler. Steel melts "
          "at about 1,500C, so lava is hot enough to glow but not to melt steel."),
    entry("sun-distance",
          (("sun",), ("how far", "far away", "away", "distance", "miles", "km",
                      "kilometres", "light seconds", "how long does light")),
          "The Sun is about 150 million km (93 million miles) away, and sunlight takes 8 minutes "
          "20 seconds to reach us. That is why you never see the Sun as it is now, only as it was "
          "eight minutes ago."),
    entry("universe-size",
          (("universe", "observable universe", "cosmos"),
           ("big", "large", "wide", "size", "across", "how big", "how large")),
          "The observable universe is about 93 billion light years across, and that is wider than "
          "its 13.8 billion year age because space itself stretched while the light travelled. "
          "The whole universe may be far larger again, and we cannot see past that horizon."),
    entry("popcorn-pop",
          (("popcorn", "popping corn", "corn pop"), ("why", "pop", "pops", "popped", "explode", "kernel",
                                         "kernels", "corn")),
          "Each kernel holds a little water inside a hard shell. Heat turns that water to steam, "
          "the pressure builds until the shell splits, and the starch inside puffs out and sets: "
          "the pop is the shell giving way, and a kernel that is too dry or has a cracked shell "
          "will not pop."),
    entry("black-hole", (("black hole", "black holes"), ("what", "how", "form", "forms", "gravity")),
          "A black hole is a place where matter is packed so tightly that its gravity pulls in "
          "everything, even light. Most form when a very massive star runs out of fuel and "
          "collapses; we spot them by the way their gravity moves and heats nearby gas."),
    entry("supernova", (("supernova", "supernovae", "supernovas"),
                        ("what", "star", "explode", "explodes", "explosion", "happen", "why")),
          "A supernova is the explosion of a massive star at the end of its life: its core "
          "collapses and the outer layers are blown off, briefly outshining a whole galaxy. The "
          "iron in your blood and the calcium in your bones were made in stars that ended this "
          "way."),
    entry("galaxy", (("galaxy", "galaxies"),
                     ("what", "many", "made", "formed", "form", "big", "stars", "types")),
          "A galaxy is a huge group of stars, gas and dust held together by gravity; galaxies form "
          "as clouds of gas and dark matter pull together. Our Milky Way holds 100 to 400 billion "
          "stars and is about 100,000 light years across, and there are billions of galaxies beyond "
          "it, most with a supermassive black hole at the centre.",
          ask=("what", "many", "made", "formed", "form", "big", "stars", "types"),
          avoid=("hitchhiker", "guide", "samsung", "phone", "tablet")),
    entry("milky-way", (("milky way", "our galaxy", "galaxy called"),
                        ("what", "our", "galaxy", "why", "called", "see", "visible")),
          "The Milky Way is the galaxy we live in: a flat spiral of 100 to 400 billion stars, "
          "with the Sun about 26,000 light years from the centre. The pale band you see on a dark "
          "night is us looking along the disc from inside it.",
          ask=("what", "our", "galaxy", "why", "called", "see", "visible"),
          avoid=("chocolate", "candy", "bar", "recipe", "biscuit", "cake")),
    entry("satellite", (("satellite", "satellites"),
                        ("what", "how", "work", "orbit", "made", "stay", "natural")),
          "A satellite is anything that orbits a larger body: the Moon is Earth's natural "
          "satellite, and most people mean the machines we launch. They stay up by moving "
          "sideways fast enough that they keep falling around the Earth and missing it.",
          ask=("what", "how", "work", "orbit", "made", "stay", "natural"),
          avoid=("dish", "aerial", "tv", "television", "broadband", "internet", "receiver",
                 "signal", "phone", "phones")),
    entry("planets-orbit", (("planet", "planets", "earth"),
                            ("orbit", "orbits", "around the sun", "sun")),
          "Planets orbit the Sun because of gravity: the Sun's pull bends their straight-line "
          "motion into a curve, and their sideways speed stops them falling in. The same balance "
          "keeps the Moon going round the Earth and satellites going round the Earth.",
          ask=("orbit", "orbits", "around the sun", "sun", "how"),
          avoid=("travel", "trip", "holiday", "hotel")),
    entry("moon-follows", (("moon",),
                           ("follow", "follows", "following me", "move with me", "keep up")),
          "The Moon only looks as if it follows you: it is about 384,000 km away, so driving a "
          "few kilometres barely changes its angle against the stars. Nearby trees and houses "
          "rush past, which makes the Moon seem to keep pace.",
          ask=("follow", "follows", "following me", "move with me", "keep up", "why", "how"),
          avoid=("photo", "photograph", "picture", "camera", "shoot", "capture", "lens")),
    entry("gravity-space", (("gravity", "astronaut", "astronauts", "space station", "iss"),
                            ("space", "float", "floating", "weightless", "no gravity",
                             "zero gravity")),
          "There is gravity in space: astronauts on the space station float because they and the "
          "station are falling around the Earth together at the same speed, not because gravity "
          "has gone. At that height gravity is still about 90% as strong as it is on the ground.",
          ask=("why", "how", "what", "float", "floating", "weightless", "space"),
          avoid=("black hole", "the moon", "mars", "planet")),
    entry("speed-of-light", (("speed of light", "light"),
                             ("speed", "what", "what's", "how fast", "fast", "value")),
          "Light travels at about 300,000 kilometres per second in a vacuum, which is 299,792,458 "
          "metres per second exactly. At that speed it takes sunlight about 8 minutes to reach "
          "Earth.",
          ask=("speed of light", "speed", "how fast", "fast", "value", "light year",
               "light years", "travels at", "made of", "what is light", "photon",
               "photons", "wave", "waves", "particle", "particles", "discovered",
               "measured", "how long does light"),
          avoid=("bulb", "traffic", "switch", "lamp", "room", "lunch", "meal")),
    entry("star-twinkle", (("star", "stars"), ("twinkle", "twinkling", "shimmer", "flicker",
                                              "steady")),
          "Stars twinkle because their light passes through moving layers of air, which bend it "
          "slightly this way and that before it reaches your eyes. Planets look steadier because "
          "they are close enough to show a tiny disc rather than a single point of light.",
          ask=("twinkle", "twinkling", "shimmer", "flicker", "steady")),
    entry("north-star", (("north star", "polaris", "pole star"),
                        ("what", "which", "find", "brightest", "where", "how")),
          "Polaris sits almost exactly above the Earth's north pole, so the rest of the sky turns "
          "around it while it stays put. Find it from the two stars at the end of the Big Dipper's "
          "bowl: follow the line through them about five times their gap. It is not the brightest "
          "star in the sky, just the one that marks north.",
          ask=("what", "which", "find", "brightest", "where", "how"),
          avoid=("photo", "photograph", "picture", "camera", "shoot", "capture", "exposure",
                 "lens", "telescope", "trail", "night sky", "north pole", "hotel",
                 "north star hotel")),

    entry("summer-hot", (("summer", "hot", "hotter", "heat"),
                         ("why", "than", "winter", "more", "cause")),
          "Summer is hotter because the Sun is higher in the sky and stays up longer, so the same "
          "patch of ground gets more direct sunlight and more hours of it. The Earth is actually "
          "farthest from the Sun in July, which is why distance is not the explanation.",
          ask=("why", "than", "winter", "more", "cause"),
          avoid=("boiler", "radiator", "radiators", "thermostat", "central heating", "heating",
                 "hot water", "plumber", "kettle", "flask")),
    entry("moons", (("moon", "moons"), ("jupiter", "saturn", "mars", "earth", "venus", "neptune",
                                        "uranus", "mercury", "planet", "how many", "number of")),
          _moons, ask=("how many", "number of", "what about", "which planet", "does",
                       "names", "name", "called", "list")),
    entry("weather-climate", ("weather", "climate", ("difference", "between", "vs")),
          "Weather is what the air is doing today: rain, wind, sun, temperature. Climate is the "
          "long-run pattern of that weather over years and decades, so one cold week says nothing "
          "about climate change and one hot day is not proof of it."),
    entry("ice-floats", ("ice", ("float", "floats", "water", "density")),
          "Water is unusual: it expands as it freezes, so ice is about 9% less dense than liquid "
          "water and floats. That is also why a full bottle left in the freezer can split.",
          avoid=("dry", "hot water bottle", "heat or ice", "ice or heat", "better than ice",
                 "ice pack", "cold compress", "compress", "sprain", "sprained", "swelling",
                 "swollen", "muscle", "sore", "ache", "aching")),
    entry("ocean-blue", (("ocean", "sea"), ("blue", "colour", "color", "why")),
          "Water absorbs red light much more strongly than blue, so the deeper the water the more "
          "the reds disappear and the blue is left. The sky's reflection adds to it, but the "
          "colour is mostly the water itself.",
          avoid=("salty", "salt", "saltier")),
    entry("sea-salty", (("ocean", "sea"), ("salty", "salt", "why")),
          "Rain wears minerals out of rocks and carries them to the sea, and when the water "
          "evaporates the salt stays behind. Rivers keep adding a little, so the sea has become "
          "salty over hundreds of millions of years.",
          avoid=("blue", "colour", "color")),
    entry("stroke-signs", (("stroke", "strokes", "mini stroke", "tia"),
                           ("sign", "signs", "symptom", "symptoms", "spot", "recognise",
                            "recognize", "first", "early", "warning", "how do i know",
                            "how would i know", "what are", "sudden",
                            "watch for", "watching for", "look out for", "watch out for")),
          "Think FAST: Face - ask them to smile, has one side dropped? Arms - can they raise both "
          "and hold them up? Speech - is it slurred or garbled? Time - if any of those is off, "
          "call 999 straight away and note when it started, because clot-busting treatment depends "
          "on the clock. A sudden loss of sight, or the worst headache of your life, is the same "
          "call. Do not drive them yourself.",
          avoid=("heat", "sun", "lawn", "paint", "brush", "cat", "happy", "lucky", "worry")),
    entry("tinnitus", (("tinnitus", "ringing", "buzzing", "humming", "whistling",
                        "ringing in my ears", "ringing in the ears", "buzzing in my ears"),
                       ("ear", "ears", "head", "hear", "hearing", "night", "silent", "quiet",
                        "what causes", "why", "help", "stop", "cope", "worse at night")),
          "Tinnitus is your hearing system filling silence with a sound, and it is common and "
          "rarely a sign of anything serious. It feels worse at night because the room is quiet, "
          "so give your ears something else: a fan, quiet radio or white noise at low volume. Cut "
          "back on caffeine and alcohol and look after your sleep. See a GP if it is one-sided, "
          "came with hearing loss or dizziness, or is stopping you sleeping.",
          ask=("ear", "ears", "hearing", "hear", "tinnitus", "ringing in my ears",
               "ringing in the ears", "in my head", "quiet", "silent", "silence", "at night",
               "night time", "in the night", "worse at night"),
          avoid=("ringing me", "rings me", "ring me", "rang me", "rings back", "rang back",
                 "ringing my", "ringing us", "calling me", "called me", "calls me",
                 "texted me", "messaged me", "phone", "phone is ringing", "doorbell",
                 "door bell", "bell", "bells",
                 "church", "alarm", "timer", "door", "in my head", "ring piece", "sausage",
                 "fridge", "freezer", "washing machine", "machine", "dishwasher", "fan",
                 "extractor", "boiler", "motor", "compressor", "microwave", "kettle",
                 "laptop", "computer", "hoover", "vacuum", "engine", "car", "tumble dryer",
                 "washer", "dryer", "refrigerator", "oven", "appliance",
                 "radiator", "radiators", "printer", "pipes", "tap", "taps", "shower",
                 "light bulb", "lightbulb", "in the walls"),
          report=True),
    entry("cough-lasting", (("cough", "coughs", "coughing"),
                            ("week", "weeks", "month", "months", "wont shift", "won't shift",
                             "not going", "still", "keeps", "persistent", "long", "lingering",
                             "for ages")),
          "Most coughs after a cold last two to three weeks and settle on their own: honey in warm "
          "drinks, plenty of fluids and a propped-up pillow at night ease it, and cough medicines "
          "do little. See a GP if it lasts more than three weeks, you are coughing blood or "
          "breathless, you have lost weight, or it came with a fever that will not go.",
          ask=("week", "weeks", "month", "months", "shift", "long", "still", "keeps", "night",
               "ages", "persistent", "lingering"),
          bias=2,
          avoid=("cough drop", "cough sweets", "cough medicine", "syrup", "child", "baby",
                 "toddler", "son", "daughter", "my son", "my daughter",
                 "dog", "cat", "smoker", "smoking", "vape", "vaping")),
    entry("verruca-pharmacy",
          (("verruca", "verrucas", "verruca pedis", "plantar wart", "wart", "warts"),
           ("get rid", "rid of", "remove", "removing", "treat", "treatment", "cure", "clear",
            "going", "go away", "goes away", "disappear", "freeze", "worth", "how", "best",
            "home remedy", "help", "have", "got", "keep getting", "growing", "painful")),
          "Most verrucas clear up on their own within two years, but a pharmacy treatment is "
          "quicker: soak the foot, file the hard skin down with a pumice or emery board, then "
          "paint on salicylic acid once a day for up to 12 weeks. Keep it covered in pools and "
          "gym showers. See a GP if it bleeds, is very painful, or you have diabetes or poor "
          "circulation in your feet.",
          ask=("get rid", "rid of", "remove", "removing", "treat", "treatment", "cure", "clear",
               "going", "go away", "goes away", "disappear", "freeze", "worth", "how", "best",
               "home remedy", "help", "have", "got", "keep getting", "growing", "painful"),
          avoid=("my dog", "my cat", "my puppy", "the dog", "the cat", "dog", "cat", "puppy",
                 "kitten", "hamster", "horse")),
    entry("athletes-foot-itch",
          (("athlete's foot", "athletes foot", "athletic foot", "fungal infection",
            "feet itch", "foot itch", "itchy feet", "my feet itch", "itching between my toes",
            "between my toes", "between the toes", "my toes", "toes", "peeling between my toes",
            "toes itch", "toe itch"),
           ("get rid", "rid of", "treat", "treatment", "cure", "clear", "stop", "itching",
            "itch", "itchy", "keeps", "coming back", "how", "best", "help", "cream", "worth",
            "peel", "peeling", "peely", "flaky", "cracked", "sore", "smell", "smelly",
            "sweaty")),
          "Use a terbinafine cream from the pharmacy twice a day for two weeks, and carry on for "
          "a week after the itching stops or it comes back. Dry between the toes properly, wear "
          "cotton socks and change them daily, and alternate shoes so each pair dries out; wash "
          "socks at 60C. If the skin is cracked, weeping or has not cleared in a month, ask a "
          "pharmacist.",
          ask=("get rid", "rid of", "treat", "treatment", "cure", "clear", "stop", "itching",
               "itch", "itchy", "keeps", "coming back", "how", "best", "help", "cream", "worth",
               "peel", "peeling", "peely", "flaky", "cracked", "sore", "smell", "smelly",
               "sweaty"),
          avoid=("dog", "cat", "puppy", "kitten", "hands", "between my fingers")),
    entry("flu-jab", (("flu jab", "flu vaccine", "flu shot", "flu vaccination"),
                      ("should", "free", "need", "get", "worth", "who", "where", "when",
                       "eligible", "pay")),
          "In the UK the flu jab is free on the NHS if you are 65 or over, pregnant, or have a "
          "condition like asthma, diabetes or a weak immune system, and for some carers and "
          "young children. At 45 without one of those you would pay, about 15 to 20 pounds at a "
          "pharmacy, and it is worth it if you would rather not lose a week to flu. Best asked "
          "for in the autumn.",
          ask=("should", "free", "need", "get", "worth", "who", "where", "when", "pay"),
          avoid=("bird", "chicken", "poultry", "hamster", "reptile")),
    entry("teeth-check", (("teeth", "teeth checked", "dentist", "dental", "check-up",
                           "check up", "hygienist", "scale and polish"),
                          ("often", "how often", "how many times", "regular", "year", "yearly",
                           "check", "checkup", "check-up", "visit", "see")),
          "Most adults are told every six months, but if your teeth and gums are healthy a dentist "
          "may say twelve, and the NHS guidance is that the interval should be set by your risk - "
          "so ask them to write it down. Go sooner for bleeding gums, a tooth that hurts when you "
          "bite, or a mouth ulcer that has not healed in three weeks.",
          ask=("often", "regular", "year", "yearly", "check", "checkup", "check-up", "visit",
               "many"),
          avoid=("baby", "toddler", "child", "dog", "cat", "whiten", "whitening", "brace",
                 "braces", "false", "denture", "dentures", "grind", "grinding",
                 "manager", "boss", "micromanage", "micromanaging", "micromanages",
                 "my team", "my staff", "colleague", "colleagues", "employee", "employees",
                 "apprentice", "trainee", "at work", "in work", "workplace", "my job",
                 "every move", "over my shoulder", "watches me", "watching me",
                 "checks on me", "checks up on me", "checking up on me")),
    entry("period-pain", (("period pain", "period pains", "period cramps", "cramps", "period",
                           "periods", "menstrual"),
                          ("worse", "worsening", "getting worse", "each month", "every month",
                           "help", "helps", "painful", "pain", "bad", "severe", "unbearable",
                           "what can i do", "stop",
                           "heavy", "heavier", "very heavy", "so heavy", "flooding", "clots",
                           "soaking", "soak",
                           "irregular", "all over the place", "gone mad", "haywire", "skipping",
                           "skipped", "closer together", "further apart", "every two weeks",
                           "every three weeks", "randomly", "unpredictable", "stopped",
                           "stopping")),
          _period_answer,
          ask=("worse", "worsening", "help", "helps", "painful", "pain", "bad", "severe",
               "unbearable", "stop", "what", "heavy", "heavier", "flooding", "clots", "soaking",
               "irregular", "all over the place", "gone mad", "haywire", "skipping", "skipped",
               "closer together", "further apart", "every two weeks", "every three weeks",
               "randomly", "unpredictable", "stopped", "stopping"),
          avoid=("period drama", "history", "school", "grace period", "period of time",
                 "pause", "full stop", "menopause", "pregnant", "pregnancy", "test",
                 "leg", "legs", "calf", "calves", "foot", "feet", "toe", "toes", "thigh",
                 "hand", "hands", "arm", "arms", "muscle", "muscles")),
    entry("blocked-nose-lining", (("blocked nose", "nose is blocked", "bunged up", "stuffy nose",
                            "nose is bunged", "congested", "congestion", "cant breathe through my nose",
                            "can't breathe through my nose"),
                           ("what", "help", "helps", "clear", "unblock", "night", "sleep",
                            "better", "get rid", "how",
                            "all the time", "all day", "always", "every day", "constant",
                            "constantly", "for weeks", "months")),
          "Saline spray or a salt-water rinse clears a blocked nose, and steam loosens it; sleep "
          "with your head raised. A nose blocked most days rather than after a cold is usually "
          "allergic rhinitis, and a steroid nasal spray from the pharmacy, used every day for two "
          "weeks, beats anything by mouth. A decongestant spray works a few days only - longer "
          "and the rebound makes it worse. See a GP if it is one-sided or comes with a nosebleed "
          "you cannot stop.",
          ask=("what", "help", "helps", "clear", "unblock", "night", "better", "rid", "how",
               "all the time", "all day", "always", "every day", "constant", "constantly",
               "weeks", "months"),
          avoid=("sink", "drain", "pipe", "pipes", "toilet", "road", "traffic", "spray paint",
                 "sinus", "child", "baby", "toddler")),
    entry("vitamins-with-food", (("vitamin", "vitamins", "supplement", "supplements",
                                  "multivitamin", "multivitamins", "iron tablets", "cod liver oil"),
                                 ("with food", "with a meal", "empty stomach", "before food",
                                  "after food", "when", "how", "take", "taking", "best time",
                                  "morning", "night")),
          "Take them with a meal: the fat in food helps you absorb vitamins A, D, E and K, and "
          "most people find a multivitamin easier on the stomach with breakfast. Iron is better "
          "with orange juice than with tea or coffee, which block it. Do not double up - a "
          "multivitamin plus a separate one of the same vitamin can push you over the daily limit, "
          "so compare the labels.",
          ask=("when", "how", "best", "morning", "night", "food", "meal", "stomach", "take",
               "taking"),
          avoid=("plant", "plants", "soil", "garden", "dog", "cat", "fish", "dose", "overdose",
                 "pregnant", "pregnancy", "child", "deficiency", "b12")),
    entry("stiff-neck", (("stiff neck", "neck is stiff", "neck stiffness", "neck ache",
                          "neck aches", "crick", "cricked"),
                         ("morning", "mornings", "wake up", "waking", "every", "pillow",
                          "sleep", "sleeping", "desk", "helps", "help", "what can i do")),
          "A neck that is stiff every morning is usually how you slept rather than anything else: "
          "a pillow that keeps your head in line with your spine - not propped up, not flat - and "
          "a warm shower first thing loosen it. Move it gently through its range rather than "
          "holding still. Get it checked the same day if it comes with a fever, a bad headache, "
          "or light hurting your eyes.",
          ask=("morning", "mornings", "wake", "waking", "every", "pillow", "sleep", "helps",
               "help", "what"),
          avoid=("child", "baby", "pregnant", "fever", "rash", "car", "crash", "whiplash",
                 "guitar", "violin")),
    entry("clockwork", (("clock", "clocks", "watch", "watches", "pendulum", "clockwork"),
                        ("work", "works", "working", "how does", "mechanism", "inside",
                         "tick", "tick tock", "spring")),
          "A weight or a wound spring stores the energy, a gear train slows it down, and an "
          "escapement lets it out one tick at a time - that tick is what moves the hands at a "
          "steady rate. A pendulum or balance wheel sets the rhythm, which is why a grandfather "
          "clock keeps good time and a cheap watch drifts. A quartz watch swaps the pendulum for a "
          "crystal vibrating 32,768 times a second, which a chip counts down to one second.",
          avoid=("wrong", "change", "clocks go back", "clocks go forward", "daylight", "late for",
                 "alarm", "snooze", "watch the", "watch tv", "watch a film", "watch the match",
                 "watch netflix")),
    entry("earthquakes", (("earthquake", "earthquakes", "quake", "quakes"),
                          ("happen", "happens", "cause", "causes", "caused", "why", "made",
                           "makes", "what makes", "what causes", "plate", "plates")),
          "The Earth's outer shell is broken into plates that move slowly and catch against each "
          "other. When the strain builds up and the rock suddenly slips, the ground shakes: that "
          "is an earthquake, and most happen near plate edges."),
    entry("volcanoes", (("volcano", "volcanoes", "volcanic"), ("erupt", "erupts", "eruption",
                                                               "how", "why", "what", "cause",
                                                               "causes", "magma", "lava",
                                                               "makes", "make", "made", "happen",
                                                               "happens", "formed", "forms")),
          "Deep underground, rock melts into magma, which is lighter than the rock around it and "
          "rises. It collects in a chamber until the pressure forces it up through a vent, and it "
          "erupts as lava, ash and gas. Most volcanoes sit where plates pull apart or push "
          "together.",
          guard=_not_a_volcano_build,
          avoid=("for school", "school project", "science project", "project", "model",
                 "model volcano", "volcano model", "build",
                 "baking soda", "bicarbonate", "vinegar", "papier", "paper mache",
                 "food colouring", "science fair")),
    entry("lightning", ("lightning", ("form", "forms", "why", "cause", "causes", "strike",
                                      "strikes", "happen", "makes", "make", "what")),
          "Collisions between ice and water drops in a storm cloud build up electric charge. When "
          "the difference gets big enough, the charge leaps through the air as a huge spark: "
          "lightning, which heats the air so fast it makes the bang of thunder."),
    entry("thunder", ("thunder", ("sound", "why", "happen", "after", "lightning",
                                   "cause", "causes", "makes", "make", "what") + ORIGIN_ASK),
          "Lightning heats the air along its path to about 30,000°C in a split second, and the air "
          "expands violently, making a shock wave we hear as thunder. You see the flash first "
          "because light travels far faster than sound."),
    entry("honey", ("honey", ORIGIN_ASK),
          "Bees make it: a worker drinks nectar out of flowers into a honey stomach, where "
          "enzymes start breaking the sugar down, then passes it to a hive bee who packs it into "
          "a wax cell and fans the water out of it until it is too thick to spoil. One bee makes "
          "about a twelfth of a teaspoon in her whole life."),
    entry("paper", ("paper", ORIGIN_ASK),
          "Most paper is wood: chips are cooked with chemicals until the fibres separate into "
          "pulp, and the pulp is washed, pressed and dried into a sheet. Recycled paper skips the "
          "tree and goes back to pulp, and most office paper is now a mix of new and recycled "
          "fibre."),
    entry("electricity-made", (("electricity", "mains electricity", "power"), ORIGIN_ASK),
          "Nearly all of it is made by spinning a generator: gas, coal, nuclear, wind and water "
          "all turn the same kind of shaft, and the National Grid carries the result around the "
          "country and steps the voltage down through substations to your street. Solar panels "
          "are the odd ones out - they make it straight from light, with nothing turning.",
          bias=2),
    entry("glass", ("glass", ORIGIN_ASK),
          "Glass is sand melted with soda ash and limestone at about 1,700°C, then cooled fast "
          "enough that it sets as a liquid instead of forming crystals - which is why you can see "
          "through it. It can be melted down and remade indefinitely without losing anything."),
    entry("chocolate", ("chocolate", ORIGIN_ASK),
          "Cocoa beans grow in pods on trees in the tropics; they are fermented, dried, roasted "
          "and ground, and the fat that comes out with the powder - cocoa butter - is what makes "
          "chocolate smooth enough to melt on your tongue."),
    entry("milk-made", ("milk", ORIGIN_ASK),
          "Dairy milk is made by cows, in the udder, from what they eat - mostly grass and "
          "silage - and it is about 87% water. A milking cow gives roughly 25 to 30 litres a day, "
          "in two or three milkings."),
    entry("eggs", ("eggs", ORIGIN_ASK),
          "Hens lay them. Each one starts as a yolk released from the hen's ovary, which picks up "
          "the white and then the shell on its way down the oviduct, roughly one egg every 25 "
          "hours in a good laying hen."),
    entry("water", (("water", "tap water", "drinking water"), ORIGIN_ASK),
          "Rain soaks into the ground and runs into rivers, and your tap water is drawn from a "
          "river, a reservoir or a borehole, then filtered and treated so nothing can grow in it "
          "and pumped to the house under pressure. A town near hills is usually fed from a "
          "reservoir; anywhere else it comes from a river or from deep underground.",
          avoid=("dishwasher", "washing machine", "washer", "tumble dryer", "fridge", "freezer",
                 "leaking", "puddle", "puddles", "flooded", "flooding")),
    entry("bread", (("bread", "loaf", "loaves"), ORIGIN_ASK),
          "Flour, water, salt and yeast. The yeast gives off gas as it feeds on the flour, and "
          "the gluten in the flour - stretchy because it is wheat - traps it as bubbles, which is "
          "what makes the loaf rise; the oven then sets the structure and browns the crust."),
    entry("salt", (("salt",), ORIGIN_ASK),
          "Either dug up as rock salt, laid down by seas that dried out long ago, or dried out of "
          "sea water in shallow ponds. Both are the same sodium chloride, and the difference in "
          "the shop is the size of the crystal and whether iodine or an anti-caking agent has "
          "been added."),
    entry("petrol", (("petrol", "petroleum", "diesel", "fuel"), ORIGIN_ASK),
          "Crude oil, heated in a refinery until its parts separate by boiling point. Petrol is "
          "one of the light fractions taken off near the top, then cleaned and blended, which is "
          "why it evaporates so quickly and catches light so easily.",
          avoid=("car wont", "car won't", "wont start", "won't start", "misfuel", "misfuelled",
                 "wrong fuel", "diesel in", "petrol in", "bill", "cost", "price", "cheap",
                 "cheapest", "per litre", "a litre", "fill up", "empty")),
    entry("tea", (("tea",), ORIGIN_ASK + ("tea grow", "tea grown", "tea growing", "tea planted")),
          "One bush, Camellia sinensis: the leaves are picked, then wilted, rolled and dried, and "
          "how far they are allowed to oxidise decides the kind - none for green, all the way "
          "for black. Almost every tea in the shop, white, green, oolong and black, comes off that "
          "same bush.",
          avoid=("caffeine", "milk", "brew", "brew it", "stewed", "cups", "cup a day",
                 "how many cups", "before bed", "bag", "bags", "sugar", "green tea good",
                 "black tea good", "iced", "sweet tea")),
    entry("coffee", (("coffee",), ORIGIN_ASK + ("coffee grow", "coffee grown", "coffee growing",
                                                 "beans grow", "beans grown")),
          "Coffee beans are the seeds of a cherry that grows on bushes in the tropics, mostly in "
          "a band round the equator. The picked fruit is dried, the two seeds inside are "
          "removed and roasted, and the roast is what turns them brown and flavours the drink.",
          avoid=("caffeine", "how much", "cups a day", "cup a day", "before bed", "instant",
                 "machine", "grinder", "ground", "brew", "strong", "decaf", "milk", "sugar",
                 "stain", "stains", "stained")),
    entry("wine", (("wine",), ORIGIN_ASK),
          "Grapes, crushed and left to ferment: the yeast on the skins eats the sugar in the juice "
          "and turns it into alcohol. Red wine spends its time with the skins and white is "
          "pressed off them first, which is where the colour comes from.",
          avoid=("red wine", "white wine", "glass of", "bottle", "hangover", "stain", "stains",
                 "pair with", "open", "leftover", "keeps", "calories", "sulphites", "sulfites")),
    entry("cheese", (("cheese", "cheddar"), ORIGIN_ASK),
          "Milk, and mostly cow's milk: it is warmed, a culture and rennet go in so the curds set, "
          "and the curds are cut, pressed and salted. Roughly 10 litres of milk go into a kilo of "
          "hard cheese, which is where the whey drains off to.",
          avoid=("melt", "melted", "melting", "grated", "substitute", "instead", "toast",
                 "toastie", "mouldy", "mould", "gone off", "how much", "calories", "bake",
                 "freeze", "keeps")),
    entry("steel", (("steel", "stainless steel"), ORIGIN_ASK),
          "Iron with a little carbon in it - under about 2% - and the stainless kind also has "
          "chromium, which is what stops it rusting. The carbon is the part that makes it hard: "
          "pure iron is soft and bends.",
          avoid=("pan", "pans", "knife", "knives", "wok", "rust", "rusty", "cutting",
                 "sharpen", "seasoning", "wool", "scrub", "scourer")),
    entry("plastic", (("plastic", "plastics"), ORIGIN_ASK),
          "Oil or gas, mostly: the refinery makes small molecules like ethylene and propylene and "
          "a chemical plant links them into long chains called polymers. How the chains are built "
          "decides whether it ends up as a clear bottle or a washing-up bowl.",
          avoid=("recycle", "recycling", "recycled", "bin", "bins", "bpa", "microwave",
                 "freezer", "freeze", "smell", "melt", "melting", "safe")),
    entry("rubber", (("rubber",), ORIGIN_ASK),
          "Latex sap from the rubber tree, for natural rubber: it is tapped out of the bark, then "
          "mixed with sulphur and heated, which links the chains so it springs back instead of "
          "staying sticky. Most car tyres are synthetic rubber made from oil.",
          avoid=("tyre", "tyres", "puncture", "smell", "perished", "perishing", "seal", "washer",
                 "gasket", "glue", "stuck", "squeak", "wipers", "boot")),
    entry("wool", (("wool", "woollen", "woolen"), ORIGIN_ASK),
          "Sheep, and sometimes alpaca, goat or rabbit: the fleece is shorn once a year, washed, "
          "carded into loose fibres and spun into yarn. Merino is the same sheep bred for a finer "
          "fibre, which is why it does not itch.",
          avoid=("shrink", "shrunk", "shrank", "wash", "washing", "bobble", "bobbles", "itch",
                 "itchy", "jumper", "cardigan", "socks", "moth", "moths", "dryer", "tumble")),
    entry("cotton", (("cotton",), ORIGIN_ASK),
          "The boll of the cotton plant, which is a ball of fluff around the seed: the fibres are "
          "picked, ginned out of the seed, combed straight and spun into thread. The plant wants "
          "heat and a long dry season, which is why so much of it grows in India, China and the "
          "southern United States.",
          avoid=("shrink", "shrunk", "wash", "washing", "iron", "bleach", "tshirt", "t-shirt",
                 "shirt", "sheets", "towel", "dryer", "tumble", "bobble")),
    entry("silk", (("silk", "silks"), ORIGIN_ASK),
          "Silkworms, the caterpillars of a moth, which spin a cocoon out of one continuous "
          "thread. The cocoons are unwound into a single fibre, which is why silk is smooth and "
          "strong where cotton is short fibres twisted together.",
          avoid=("wash", "washing", "iron", "stain", "stains", "dress", "shirt", "tie",
                 "delicate", "shrink", "dry clean")),
    entry("sugar", (("sugar", "white sugar", "brown sugar"), ORIGIN_ASK),
          "The juice of sugar cane or of sugar beet, boiled down until the sugar crystallises out "
          "and the molasses drains away. Brown sugar is white sugar with some of that molasses "
          "left on or stirred back in.",
          avoid=("how much", "blood sugar", "diabetes", "diabetic", "icing", "caster",
                 "granulated", "instead of", "substitute", "cut down", "give up", "addictive",
                 "teeth", "cavities", "cravings", "too much")),
    entry("olive-oil", (("olive oil", "olive oils"), ORIGIN_ASK),
          "Olives, crushed and pressed: the fruit is ground to a paste and the paste is pressed or "
          "spun so the oil separates from the water and the solids. Extra virgin means pressed "
          "cold with low acidity; the refined kind is heat-treated and blended.",
          avoid=("how much", "smoke", "smoking", "fry", "frying", "instead of", "butter",
                 "calories", "healthy", "healthier", "keep", "store", "rancid", "goes off",
                 "bottle", "use up")),
    entry("rice", (("rice", "paddy"), ORIGIN_ASK + ("rice grow", "rice grown", "rice growing",
                                                     "grows rice")),
          "Rice grows in a paddy: a field walled to hold a few inches of water, planted with "
          "seedlings and flooded for most of the season. It wants heat and a lot of water, which "
          "is why so much of it comes from Asia.",
          avoid=("cook", "boil", "how long", "leftover", "microwave", "keep", "reheat",
                 "washing", "rinse", "absorb", "calories")),
    entry("bananas", (("banana", "bananas"), ORIGIN_ASK + ("bananas grow", "bananas grown",
                                                           "banana grow", "banana tree")),
          "On a huge herb rather than a tree: the plant pushes up a single stem, flowers once and "
          "fruits once, and then it is cut down and a shoot from the root takes over. Bananas want "
          "heat and rain all year, which is why they come from the tropics.",
          avoid=("ripen", "ripe", "store", "keep", "brown", "black", "freeze", "mash", "bread",
                 "bunch", "smoothie", "too many", "gone soft")),
    entry("apples", (("apple", "apples", "apple tree"), ORIGIN_ASK + ("apples grow",
                                                                      "apples grown",
                                                                      "apple grow")),
          "On trees, and in an orchard nearly every tree is grafted: the fruiting variety on top "
          "and a rootstock underneath that decides how tall it grows. An apple grown from a pip "
          "comes up a different apple, which is why every Cox is a cutting of one old tree.",
          avoid=("store", "keep", "cook", "pie", "crumble", "bake", "fall", "drop", "windfall",
                 "juice", "brown", "soft", "variety")),
    entry("vanilla", (("vanilla", "vanilla pod", "vanilla pods"), ORIGIN_ASK),
          "The pod of an orchid, and it has almost no smell when it is picked: the pods are cured "
          "for months, dried and sweated until the flavour crystals form. The flowers have to be "
          "pollinated by hand outside Mexico, which is why real vanilla costs so much.",
          avoid=("essence", "extract", "substitute", "instead", "ice cream", "custard", "cake",
                 "how much", "cheaper")),
    entry("leather", (("leather", "suede"), ORIGIN_ASK),
          "Animal hide, mostly cow, that has been tanned: the skin is cleaned, then treated with "
          "tannins or chromium so the protein stops rotting and stays soft. Suede is the same "
          "skin buffed on the inside face.",
          avoid=("clean", "cleaning", "condition", "conditioner", "scuff", "scuffs", "shoe",
                 "shoes", "sofa", "jacket", "bag", "smell", "stain", "stains", "crack")),
    entry("rain", ("rain", ("form", "forms", "why", "fall", "falls", "happen")),
          "Water evaporates, rises and cools, and its vapour condenses into tiny droplets that "
          "make clouds. Those droplets collide and grow until they are too heavy to stay up, and "
          "then they fall as rain.",
          avoid=("bow", "bows", "coat", "jacket")),
    entry("metal-cold", (("metal",), ("cold", "colder", "feels", "touch", "why")),
          "Metal is not colder than the room; it conducts heat away from your hand much faster "
          "than wood or cloth, so your skin loses heat quickly and reads that as cold. That is "
          "also why a metal spoon feels cold and a wooden one does not."),
    entry("soap", ("soap", ("work", "works", "clean", "germs", "hands", "why")),
          "Soap molecules have one end that grabs water and one that grabs oil and grease, so "
          "they surround dirt and lift it off your skin into the water. Washing with water alone "
          "leaves the oils behind; the rubbing and rinsing matter as much as the soap."),
    entry("static", (("static", "static electricity"), ("shock", "spark", "hair", "why",
                                                         "happen")),
          "Rubbing two materials together can pull electrons from one to the other, leaving a "
          "charge that builds up on a surface. When you touch something, the charge jumps across "
          "as a small spark, which you feel as a shock.",
          avoid=("stop", "stops", "stopping", "prevent", "preventing", "get rid", "fix",
                 "reduce", "how can i",
                 "full of static", "all static", "so much static", "nothing but static",
                 "goes static", "going static", "bit of static", "so static", "really static",
                 "very static", "gets static", "getting static", "keeps going static",
                 "car", "cars", "seat", "seats", "van", "door handle")),
    entry("magnets", (("magnet", "magnets", "magnetic"), ("work", "works", "why", "attract",
                                                           "field")),
          "A magnet has a magnetic field, and it pulls on materials whose electrons can line up "
          "with that field, like iron, nickel and cobalt. Cut a magnet in half and you get two "
          "smaller magnets, each with its own north and south pole."),
    entry("magnet-what", (("magnet", "magnets"),
                          ("what", "mean", "made", "material")),
          "A magnet is an object that produces a magnetic field, which pulls on iron, nickel and "
          "cobalt and pushes or pulls on other magnets. In most fridge magnets the field comes "
          "from tiny magnetic regions lined up in the same direction; in a compass needle it comes "
          "from a small piece of magnetised metal.",
          ask=("what", "mean", "made", "material"),
          avoid=("work", "works", "how", "field", "attract", "repel")),
    entry("electricity", (("electricity",), ("what", "how", "work", "works", "flow")),
          "Electricity is the flow of electric charge, usually electrons pushed along a wire by a "
          "voltage. A circuit has to be a complete loop: the source pushes the charge, the wires "
          "carry it, and a device like a bulb uses the energy as it passes."),
    entry("sound-travel", ("sound", ("travel", "travels", "speed", "faster", "vacuum", "through")),
          "Sound is a vibration that travels as a wave through air, water or solids; in air it "
          "moves at about 343 metres per second. It travels faster in water and fastest in "
          "solids, and it cannot travel through a vacuum because there is nothing to vibrate.",
          ask=("how", "why", "fast", "speed", "travel")),
    entry("plane-fly", (("plane", "planes", "aeroplane", "airplane", "aircraft"),
                        ("fly", "flies", "lift", "wing", "wings", "aerodynamics", "stay")),
          "A wing is shaped so air moves faster over the top than underneath, and the pressure "
          "difference pushes the wing up; that force is called lift. Engines provide the forward "
          "thrust, and lift grows with speed until it beats the plane's weight.",
          ask=("how", "why", "what")),
    entry("gravity", (("gravity",), ("work", "works", "what", "why", "pull", "force")),
          "Gravity is the attraction between anything with mass: the Earth pulls you toward its "
          "centre, and you pull the Earth back by the same rule. Bigger mass means a stronger "
          "pull, which is why the Moon orbits the Earth and the Earth orbits the Sun."),
    entry("atoms", (("atom", "atoms"), ("what", "made", "small", "how", "matter")),
          "An atom is the smallest unit of an element, with a nucleus of protons and neutrons "
          "surrounded by electrons. Atoms join into molecules, and everything you can touch is "
          "made of them; they are mostly empty space."),
    entry("dna", (("dna",), ("what", "mean", "stand", "do", "gene", "genes", "work")),
          "DNA is the long molecule that carries the instructions for building and running a "
          "living thing, written in a four-letter code. Genes are sections of it, and they are "
          "copied from parents to offspring."),
    entry("cell-what", (("cell", "cells"),
                        ("what", "smallest", "body", "living", "biology", "made", "inside",
                         "how many")),
          "A cell is the smallest unit of a living thing: a jelly-like space wrapped in a thin "
          "skin, with DNA inside and machinery that turns food into energy. Your body is made of "
          "about 30 trillion of them, and each kind is shaped for its job, from a nerve cell that "
          "carries signals to a red blood cell that carries oxygen.",
          ask=("what", "smallest", "body", "living", "biology", "made", "inside", "how many",
               "how", "why"),
          avoid=("prison", "jail", "police", "holding", "phone", "battery", "solar", "fuel",
                 "spreadsheet", "excel", "terror", "hotel", "room", "monk", "cellar")),
    entry("evolution", (("evolution",), ("work", "works", "natural", "selection", "what", "how")),
          "Living things vary, and the ones whose variations suit their surroundings tend to "
          "survive and pass those variations on. Over many generations that selection changes "
          "the population: small changes accumulate into new species."),
    entry("vaccines", (("vaccine", "vaccines", "vaccination", "jab", "immunisation", "immunization"),
                       ("work", "works", "teach", "teaches", "body", "immune", "how")),
          "A vaccine shows your immune system a harmless piece or blueprint of a germ, so it can "
          "practise making antibodies without you getting ill. If the real germ turns up later, "
          "those memory cells recognise it and fight it off fast."),
    entry("how-seeds-form",
          (("seed", "seeds", "seedling", "pollination", "pollinate", "pollen"),
           ("form", "forms", "made", "make", "makes", "grow", "grows", "plant", "plants",
            "flower", "flowers", "fruit", "how", "why", "where do", "come from", "produce")),
          "In the flower: pollen from the male part (the stamen) lands on the sticky tip (the "
          "stigma), and a tube grows down to the ovule at the base. The fertilised ovule becomes "
          "the seed and the ovary around it swells into the fruit - which is why every fruit has "
          "seeds inside. Wind, insects or your own brush carry the pollen; a tomato or a pea "
          "pollinates itself before the flower even opens.",
          bias=1,
          avoid=("eat", "eating", "toast", "bread", "recipe", "bake", "sow", "sowing", "plant out",
                 "when do i plant", "when should i plant", "bird seed", "sunflower seed",
                 "sesame", "chia", "pumpkin seed", "seed tray", "germinate", "germination")),
    entry("plants-make-food", (("plant", "plants", "tree", "trees"),
                               ("food", "make", "makes", "made", "eat", "eats", "feed",
                                "energy")),
          "Plants make their own food by photosynthesis: they take carbon dioxide from the air and "
          "water from the soil and use sunlight to turn them into sugar. The green chlorophyll in "
          "their leaves captures the light, and oxygen is released as a by-product.",
          avoid=GRAZERS + PESTS_AND_CARE, bias=1),
    entry("photosynthesis", (("photosynthesis",), ("plant", "plants", "leaves", "explain", "what",
                                                    "how")),
          "Plants use sunlight to turn carbon dioxide from the air and water from the soil into "
          "sugar, which is their food, and they release oxygen as a by-product. The green "
          "chlorophyll in their leaves captures the light that powers it."),
    entry("oxygen-source", ("oxygen", ("come", "comes", "from", "plants", "produced", "where",
                                       "make", "made")),
          "The oxygen in the air comes from photosynthesis: plants, algae and plankton split water "
          "and release oxygen as they make sugar. Most of the oxygen you breathe was made by "
          "ocean plankton rather than trees."),
    entry("plant-roots", (("roots", "root", "root system"),
                          ("plant", "plants", "why", "what", "have", "need", "do")),
          "Roots do three jobs: they hold the plant in the ground, they take up the water and "
          "minerals the leaves cannot make, and they store food for next year. The fine root hairs "
          "are what does the drinking, which is why a plant in a small pot dries out so fast.",
          avoid=("canal", "dental", "tooth", "teeth", "hair", "tree roots", "cracks", "pipes",
                 "drains", "blocked", "beetroot", "carrot", "carrots", "parsnip", "swede",
                 "turnip", "ginger", "turmeric", "propagate", "propagation", "cutting",
                 "cuttings", "bare root", "root bound", "rootbound", "rot", "rotting",
                 "grey", "gray", "dye", "dyed", "colour", "color", "regrowth",
                 "touch up", "touch-up")),
    entry("plant-sunlight", (("plant", "plants"),
                             ("need", "needs", "use", "uses", "without", "why")),
          "Plants need sunlight as the energy source for photosynthesis, the reaction that makes "
          "their food. Without enough light they cannot make sugar, so they stop growing and "
          "their leaves yellow and drop.",
          ask=("plant", "plants", "leaf", "leaves", "grass", "tree", "trees",
               "sunlight", "sun", "light", "shade", "dark", "windowsill"),
          avoid=("green", "colour", "color") + PESTS_AND_CARE + (
                                  "flicker", "flickers", "flickering", "bulb", "bulbs", "switch",
                                  "socket", "wiring", "fuse", "led", "headlight", "headlights",
                                  "torch", "streetlight", "streetlights",
                                  "soil", "compost", "dirt", "potting", "nutrient", "nutrients",
                                  "minerals", "fertiliser", "fertilizer",
                                  "dropped", "dropping", "fell", "fallen", "knocked", "tipped",
                                  "broke", "broken", "cracked", "smashed", "spilled", "spilt")),
    entry("plant-soil", (("plant", "plants", "roots"),
                         ("soil", "compost", "dirt", "potting", "nutrient", "nutrients",
                          "minerals", "fertiliser", "fertilizer")),
          "Soil holds a plant up and holds the two things it needs: water around the roots and the "
          "minerals it cannot make itself, like nitrogen for leaves and phosphorus for roots. "
          "Plants can grow without it only if someone feeds them those minerals in water, which "
          "is how hydroponics works.",
          avoid=PESTS_AND_CARE + ("water", "watering", "dry", "damp", "when", "how often",
                                  "repot", "compost heap", "weed", "weeds", "mould", "mold",
                                  "white", "fungus", "gnats", "flies",
                                  "dropped", "dropping", "fell", "fallen", "knocked", "broke",
                                  "broken", "cracked", "smashed", "shattered", "tipped",
                                  "spilled", "spilt")),
    entry("plant-leaves-curl",
          (("leaf", "leaves", "plant", "plants", "tomato", "tomatoes", "basil", "fern", "rose"),
           ("curl", "curls", "curled", "curling", "rolled", "rolling", "crinkled", "wrinkled")),
          "Curling is nearly always the climate rather than a disease: dry air and a hot windowsill "
          "make the edges roll up, and a plant that dried out badly once keeps its new leaves "
          "curled. Water it properly and move it off direct sun, then feel under the curled leaves "
          "for aphids, which cluster on soft new growth and make it pucker.",
          ask=("plant", "plants", "leaf", "leaves", "tomato", "tomatoes", "basil", "fern", "rose",
               "seedling", "seedlings", "houseplant", "houseplants"),
          avoid=PESTS_AND_CARE + ("hair", "page", "paper", "eyelash", "toenail", "nail",
                                  "curling tongs", "curling wand", "straighteners")),
    entry("tomato-sun",
          (("tomato", "tomatoes", "tomato plant", "tomato plants", "tomato seedlings"),
           ("sun", "sunlight", "light", "shade", "how much", "hours", "sunny", "windowsill")),
          "Tomatoes want full sun - six to eight hours a day - and they will not set fruit in shade. "
          "A south-facing wall or a sunny patio is ideal, and indoors they need the brightest "
          "windowsill you have plus a turn now and then so they do not lean. Too little light gives "
          "you a tall pale plant with leaves and no tomatoes.",
          ask=("tomato", "tomatoes"),
          avoid=("ketchup", "sauce", "soup", "salad", "chutney", "pizza", "recipe", "recipes",
                 "grow from seed", "how do i grow", "water", "watering", "feed", "feeding")),
    entry("plant-not-growing",
          (("plant", "plants", "houseplant", "houseplants", "seedling", "seedlings", "basil",
            "fern", "monstera"),
           ("not growing", "isnt growing", "isn't growing", "stopped growing", "no growth",
            "no new growth", "wont grow", "won't grow", "stunted", "slow to grow",
            "hasnt grown", "hasn't grown", "havent grown", "has not grown", "have not grown",
            "not grown", "grown in months", "grown at all", "growth",
            "grown")),
          "Three things stop a plant growing, in order: not enough light, a pot that is full of "
          "roots, and no food. Move it somewhere brighter for a fortnight, check whether roots are "
          "coming out of the drainage holes, and give it a feed - that order fixes most of them. A "
          "plant that has not grown since autumn is usually asleep rather than ill.",
          ask=("plant", "plants", "houseplant", "houseplants", "seedling", "seedlings", "basil",
               "fern", "monstera", "cactus", "orchid"),
          avoid=PLANT_CARE_AVOID + ("child", "children", "baby", "kid", "kids", "teenager",
                                    "beard", "hair", "tumour", "tooth", "teeth",
                                    "a lot", "lots", "so much", "loads", "bigger", "taller",
                                    "massive", "huge")),
    entry("houseplant-feed-growing",
          (("feed", "feeding", "fertiliser", "fertilizer", "plant food", "houseplant food",
            "nutrients"),
           ("houseplant", "houseplants", "plant", "plants", "often", "much", "need", "winter")),
          "Feed houseplants only while they are growing, from March to September: a half-strength "
          "liquid feed every two to four weeks is plenty, and none in winter while they rest. "
          "Overfeeding is worse than underfeeding - it burns the roots and leaves white crust on "
          "the compost - so if the leaves look pale, check the light before you reach for more "
          "food.",
          ask=("houseplant", "houseplants", "plant", "plants", "orchid", "fern", "basil",
               "monstera", "cactus", "succulent", "compost", "pot"),
          avoid=("baby", "babies", "breast", "breastfeeding", "formula", "bottle", "newborn",
                 "cow", "cows", "calf", "calfs", "calf's", "sheep", "horse", "dog", "cat",
                 "bird", "birds", "wildlife", "sourdough", "yeast", "starter", "twitter",
                 "facebook", "newsfeed", "rss")),
    entry("compost-mould",
          (("mould", "mold", "fuzz", "fungus", "white fluffy", "grey fluffy"),
           ("soil", "compost", "pot", "pots", "surface", "houseplant", "houseplants", "top of the pot")),
          "That white or grey fuzz on the compost is a fungus eating dead plant matter, and it is "
          "harmless to the plant: scrape the top centimetre off, water less and let the surface dry "
          "between waterings, and give the room some air. It only appears where the compost stays "
          "warm and wet.",
          ask=("soil", "compost", "pot", "pots", "surface", "houseplant", "houseplants", "plant",
               "plants"),
          avoid=PESTS_AND_CARE + ("bread", "jam", "wall", "walls", "bathroom", "shower", "ceiling",
                                  "fridge", "food", "cheese", "fruit", "tennis", "badminton",
                                  "seedling", "seedlings", "seed tray", "damping off", "damping",
                                  "curry", "stew", "soup", "sauce", "rice", "pasta", "noodles",
                                  "risotto", "casserole", "chilli", "chili", "broth", "gravy",
                                  "bolognese", "cooked", "leftovers", "leftover", "takeaway",
                                  "slow cooker", "yoghurt", "yogurt")),
    entry("seeds-grow", (("seed", "seeds"), ("grow", "germinate", "sprout", "sprouting")),
          "A seed waits until it has water, warmth and oxygen, then its stored food fuels the "
          "first root and shoot. Once the shoot reaches light, the plant starts making its own "
          "food by photosynthesis, so the seed's reserves matter less.",
          avoid=("business", "businesses", "company", "companies", "startup", "start up",
                 "startups", "funding", "fund", "investor", "investors", "invest", "raise",
                 "raising", "venture", "capital", "money", "round", "loan",
                 "lawn", "grass", "turf", "sow", "sowing", "sowed", "seed tray", "seedling"),
          bias=1),
    entry("green-plants", (("plant", "plants", "grass", "leaves"), ("green", "colour", "color",
                                                                     "why")),
          "Leaves look green because chlorophyll, the pigment that captures sunlight for "
          "photosynthesis, reflects green light and absorbs the reds and blues. In autumn the "
          "chlorophyll breaks down and the yellow and orange pigments underneath show through.",
          avoid=GRAZERS + ("slug", "slugs", "snail", "snails", "aphid", "aphids", "caterpillar",
                           "caterpillars", "pest", "pests", "bug", "bugs", "insect", "insects",
                           "dying", "dead", "droop", "drooping", "wilt", "wilted", "repot",
                           "fertiliser", "fertilizer", "prune", "lawn", "weed", "weeds",
                           "look after", "care for", "water my", "how often", "houseplant",
                           "houseplants",
                           "autumn", "fall", "winter", "drop", "dropping", "fallen",
                           "bulb", "bulbs", "sow", "sowing", "plant out", "plant bulbs",
                           "planting bulbs",
                           "when to plant", "in the green",
                           "plant a green",
                           "when do i plant", "when should i plant", "how do i plant",
                           "where do i plant", "green manure", "green roof", "green wall",
                           "green beans", "green fingers",
                           "how do i", "how can i", "how to", "how do you", "how should i"),
          ask=("green", "colour", "color")),
    entry("dreams", (("dream", "dreams", "dreaming"), ("why", "what", "mean", "happen", "during")),
          "Dreaming happens mostly in REM sleep, when the brain is nearly as active as when "
          "awake. Scientists think it helps sort memories and practise threats and feelings; "
          "there is no good evidence that dreams predict the future.",
          avoid=("job", "career", "goal", "house", "holiday", "career",
                 "i dreamt", "i dreamed", "i had a dream", "i had a nightmare", "nightmare",
                 "nightmares", "last night", "dream about", "dreamt about", "dreamed about",
                 "dreaming about", "dream of", "dreamt of", "dreamed of",
                 "keep dreaming", "keeps dreaming", "kept dreaming", "still dreaming")),
    entry("yawn", ("yawn", ("why", "contagious", "happen", "cause", "tired")),
          "A yawn stretches the jaw and takes a deep breath, and it seems to help cool the brain "
          "and shift gears between waking and sleep. Yawning is contagious because seeing or "
          "hearing one triggers the same response, more so in people you are close to."),
    entry("hiccups", (("hiccup", "hiccups"),
                      ("stop", "stopped", "stops", "cure", "cured", "get rid", "rid",
                       "what can i do", "what should i do", "how do i get", "wont stop",
                       "won't stop", "wont go", "won't go", "home remedy", "remedy",
                       "remedies", "fast", "quickly", "hold my breath", "help",
                       "have hiccups", "got hiccups", "how long", "last", "lasts")),
          _hiccups_remedy, bias=1),
    entry("hiccups-baby", (_BABY_WORDS, ("hiccup", "hiccups", "hiccupping", "hiccupped")),
          HICCUPS_BABY),
    entry("hiccups-why", (("hiccup", "hiccups"),
                          ("why", "get", "cause", "causes", "happen", "what are") + ASK_ABOUT),
          "A hiccup is a sudden spasm of the diaphragm followed by your vocal cords snapping shut, "
          "which makes the 'hic' sound. It usually happens after a big meal, a fizzy drink or a "
          "laugh, when the stomach pushes up against the diaphragm, and it is harmless.",
          avoid=("stop", "stopped", "cure", "rid", "remedy", "remedies", "what can i do",
                 "what should i do", "wont stop", "won't stop", "fast", "quickly",
                 "hold my breath", "have hiccups", "got hiccups", "how long", "last",
                 "lasts")),
    entry("goosebumps", (("goosebumps", "goose bumps"), ("why", "get", "cause", "happen")),
          "Cold or strong emotion makes tiny muscles pull your hairs upright, which traps a layer "
          "of air for warmth and made our furry ancestors look bigger. We have kept the reflex "
          "even though we no longer have the fur for it to work."),
    *[entry(f"body-what-{name}", (words, WHAT_IS_IT + asks), reply, bias=1, avoid=avoid,
            guard=_not_about_itching if name == "scab" else None)
      for name, (words, asks, reply, avoid) in BODY_WHAT.items()],
    entry("body-what-scab-itch", (("scab", "scabs"), ("itch", "itches", "itchy", "itching",
                                                     "pick", "picking", "should i pick")),
          "Itching under a scab is healing: new skin and nerve endings are growing back, and the "
          "histamine in the repairing tissue makes it tingle. Don't pick or scratch it off - it is "
          "the dressing, and taking it off reopens the wound and makes a scar more likely - and a "
          "cool flannel over it or a firm press with a finger settles the itch for a bit.",
          bias=2),
    entry("hair-wash-how", (("hair", "hair wash", "shampoo", "scalp"),
                            ("how do i", "how to", "properly", "correctly", "right way",
                             "best way", "step by step", "method", "technique")),
          "Wet the hair, rub a 10p-sized blob of shampoo between your palms and work it into the "
          "scalp with your fingertips, not the ends, for about 30 seconds. Rinse until the water "
          "runs clear, put conditioner on the mid-lengths and ends only, leave it a minute and "
          "rinse cool. Wash the scalp, condition the hair: that is the whole trick.",
          bias=1,
          avoid=("greasy", "oily", "stop", "static", "dandruff", "flaky", "flakes", "falling",
                 "thinning", "bald", "loss", "every day", "daily", "often", "too much",
                 "frizzy", "curl", "curly", "colour", "dye", "bleach", "straighten", "dryer",
                 "hair dryer", "hairdryer", "blow dry", "blowdry", "blow", "tongs", "straighteners",
                 "beard", "dog", "cat", "car", "hands", "face",
                 "volume", "flat", "lifeless", "limp", "sticking up", "sticks up",
                 "sticking out", "sticks out", "flyaway", "flyaways", "cowlick",
                 "grow", "grows", "growing", "grew", "faster", "longer", "thicker", "growth",
                 "gum", "chewing gum", "lice", "nits", "paint", "glue", "sticky",
                 "detangle", "detangling", "tangle", "tangles", "tangled", "knot", "knots",
                 "knotty", "matted", "matt", "brush", "brushing", "comb", "combing",
                 "cut", "cuts", "cutting", "haircut", "trim", "trimming", "scissors",
                 "clippers", "fringe", "layers",
                 "plughole", "plug hole", "drain", "drains", "blocked", "unblock", "trap",
                 "bath", "sink", "shower", "showers", "shower tray", "u bend",
                 "hairbrush", "hair brush", "hair brushes",
                 "pet hair", "dog hair", "cat hair", "fur", "sofa", "settee", "couch", "carpet",
                 "rug", "floor", "mattress", "upholstery", "clothes", "clothing", "jumper",
                 "shirt", "coat", "vacuum", "hoover")),
    entry("curly-hair", (("curly hair", "curls", "wavy hair", "curly", "waves", "coils",
                          "coily hair", "3a", "4c"),
                         ("look after", "look after it", "care", "care for", "manage", "routine",
                          "wash", "washing", "dry", "drying", "style", "styling", "advice",
                          "product", "products", "how do i", "best way", "what should i")),
          "Curls want water and conditioner more than shampoo: wash the scalp two or three times a "
          "week, put plenty of conditioner through the lengths and squish it in with your head "
          "upside down, then rinse it out cool. Dry by scrunching with a cotton T-shirt rather "
          "than a towel, add a little leave-in while it is still soaking wet and then leave it "
          "alone until it is dry, because touching it is what makes it frizz. A trim every ten to "
          "twelve weeks keeps the shape.",
          avoid=("cut", "cutting", "haircut", "trim", "trimming", "straighten", "straightening",
                 "relaxer", "relaxing", "perm", "perming", "colour", "dye", "bleach", "grey",
                 "thinning", "bald", "dandruff", "stop", "greasy", "oily", "static", "gum",
                 "plughole", "drain", "sofa", "dog", "cat", "beard",
                 "iud", "fitted", "fitting", "contraception", "contraceptive", "hormonal",
                 "gynae", "the coil", "copper coil",
                 "cable", "cables", "wire", "wires", "charger", "lead", "headphones",
                 "coil fitted", "the coil", "copper coil", "coil in", "coil out", "coil removed",
                 "contraception", "contraceptive", "iud", "intrauterine", "mirena", "implant",
                 "period", "periods", "pregnant")),

    entry("hair-wash", (("hair", "hair wash", "washing my hair", "shampoo", "shampooing"),
                        ("how often", "often", "should", "wash", "washing", "every day", "daily",
                         "too much", "greasy", "oily", "fine")),
          "Two or three times a week suits most people: washing more often strips the oil the scalp "
          "needs, and washing less leaves it greasy. Very oily hair can take a daily wash, and dry "
          "or curly hair does better every three or four days with conditioner on the ends. If your "
          "scalp itches or flakes, use a shampoo for that rather than washing more.",
          ask=("how often", "often", "should", "wash", "daily", "every day", "too much"),
          avoid=("falling out", "falls out", "fall out", "falling", "thinning", "hair loss",
                 "losing my hair", "lose my hair", "going bald", "bald", "balding", "baldness",
                 "patchy", "alopecia", "flakes", "flaky",
                 "detangle", "detangling", "tangle", "tangles", "tangled", "knot", "knots",
                 "knotty", "matted",
                 "hair brush", "hairbrush", "brush clean", "wash my brush", "clean my brush",
                 "washing my brush",
                 "cut", "cuts", "cutting", "haircut", "trim", "trimming")),
    entry("hair-ask-for",
          (("haircut", "hair cut", "cut my hair", "cutting my hair", "hair", "hair style",
            "hairstyle", "fringe", "bangs", "layers", "trim", "hairdresser", "hairdressers",
            "salon", "barber", "stylist"),
           ("what should i ask for", "what do i ask for", "what to ask for", "what shall i ask for",
            "what should i get", "what should i do with", "what do i do with", "which cut",
            "which haircut", "change", "changed", "different", "new style", "new look",
            "suits me", "suit me", "look good", "looks good", "interview", "new job",
            "grown out", "growing out", "bored of",
            "ask", "asking", "get", "want", "should", "style")),
          ("Take in three photos of cuts on hair like yours - same thickness and wave, not a "
           "different length - and ask for the nearest thing to one of them, because a photo says "
           "more than any name for a cut. Then say what you hate about it now: too flat on top, "
           "too heavy at the sides, frizzy ends. Ask for a dry cut if yours is curly, and if it is "
           "a big change have it two weeks before the interview or the wedding, not the day "
           "before, so it has time to settle."),
          ask=("ask", "get", "should", "want", "change", "changed", "suits", "suit", "interview",
               "job", "style", "look", "different"),
          avoid=("how often", "how long", "grow", "grows", "growing", "grew", "faster", "thicker",
                 "at home", "myself", "cut it myself", "cutting it myself", "clippers",
                 "grey", "gray", "colour", "color", "dye", "dyed", "dyeing", "bleach",
                 "highlights", "regrowth", "wash", "washing", "shampoo", "conditioner",
                 "dandruff", "frizz", "frizzy", "static", "greasy", "oily", "falling out",
                 "thinning", "hair loss", "bald", "my dog", "my cat", "dog", "cat",
                 "children", "child", "toddler", "baby", "beard")),

    entry("hair-brush",
          (("hair", "my hair", "brush my hair", "brushing my hair", "brushing hair",
            "hair brush", "comb", "combing"),
           ("brush", "brushing", "how often", "often", "should", "wet", "every day", "daily",
            "tangles", "tangled", "knots", "detangle", "100 strokes", "hundred strokes")),
          "Once or twice a day is plenty for most hair: start at the ends, work up towards the "
          "scalp in small sections, and use a wide-tooth comb on wet hair, because wet hair "
          "stretches and snaps where dry hair gives. The 100 strokes idea is a myth, since that "
          "much brushing only roughens the outside of the hair, and a comb through conditioner in "
          "the shower is what actually gets tangles out.",
          ask=("how", "often", "should", "is it", "why"),
          avoid=("hairbrush", "hair brush", "clean", "cleaning", "wash the brush", "dog", "cat",
                 "catch a cold", "make me ill",
                 "colour", "color", "dye", "dyed", "dyeing", "bleach", "bleached", "fade",
                 "fading", "highlights", "roots", "regrowth", "tint",
                 "teeth", "tooth", "toothbrush", "beard", "dandruff", "flakes", "falling out",
                 "thinning", "bald", "wig", "dreadlocks", "curly", "frizzy", "straighten",
                 "cut", "cuts", "cutting", "haircut", "trim", "trimming", "scissors",
                 "clippers", "fringe", "layers")),
    entry("wet-hair-at-night",
          (("wet hair", "hair wet", "wet head", "damp hair", "hair still wet", "dry my hair",
            "wet hair before bed", "with it wet", "bed with it wet",
            "to bed with it"),
           ("sleep", "sleeping", "slept", "bed", "night", "bad", "ill", "cold", "catch",
            "catch a cold", "catch a chill", "before bed", "should i")),
          "No: wet hair does not make you ill. A cold comes from a virus, and being damp or cold "
          "only nudges down what your nose fights it with, so nobody catches one from a wet head. "
          "What a wet head does do is break the hair, because wet hair stretches and snaps where "
          "dry hair gives, and a damp pillow is a night of rubbing. Towel it until it stops "
          "dripping, do not rub hard, and a loose braid or a silk-ish pillowcase is enough if you "
          "would rather not dry it properly. Dry it if you are going out into the cold with it, "
          "for comfort, not for the cold.",
          avoid=("brush", "brushing", "comb", "cut", "trim", "haircut", "dye", "colour", "color",
                 "how often", "wash my hair", "washing my hair", "shampoo my", "hair wash",
                 "shampoo", "conditioner", "dryer", "hairdryer", "straighten",
                 "curly", "frizz", "dandruff", "flakes", "thin", "thinning", "bald", "beard"),
          bias=2),
    entry("wash-a-body",
          (("wash myself", "wash my body", "clean myself", "wash properly", "wash all over",
            "wash my back", "wash my legs", "wash my feet", "wash my arms", "wash my chest",
            "wash my neck", "shower properly", "wash under my arms", "how to wash"),
           ("how", "should", "do i", "often", "properly", "best", "good")),
          "Stand in a warm shower - warm enough to be comfortable, not hot enough to redden the "
          "skin - and work from the top down: hair if you are washing it, then the face, then the "
          "places that hold sweat, which are under the arms, under the breasts, the groin and "
          "between the toes. Plain soap or shower gel on your hands, a flannel or a soft cloth is "
          "all it needs, and a rinse of everything afterwards. Dry the folds properly rather than "
          "rubbing, and a wash of the face, hands, feet and under the arms is enough on the days "
          "in between a full shower.",
          ask=("how", "what", "should", "can", "is it", "do i"),
          avoid=("hair", "face", "hands", "car", "dog", "cat", "baby", "toddler", "child", "kids",
                 "dishes", "windows", "washing machine", "clothes", "laundry", "duvet", "pillow",
                 "trainers", "shoes", "brush", "brushes", "teeth", "bottle"),
          bias=1),
    entry("hair-cut", (("hair", "haircut", "hair cut", "cut my hair", "cutting my hair",
                        "hair style", "fringe", "bangs"),
                       ("how often", "often", "should", "when", "how do i", "how to", "cut",
                        "trim", "haircut", "home", "myself")),
          "Every six to eight weeks for short hair, eight to twelve for long, or whenever the "
          "ends start looking ragged. A trim does not make hair grow faster, but it stops the "
          "split ends travelling up the hair shaft, which is what makes long hair look thin. A "
          "dry cut on wavy or curly hair is more honest about how it falls than a wet one.",
          ask=("how often", "often", "should", "when", "how do i", "how to"),
          avoid=("ask for", "ask the", "which cut", "which haircut", "new style", "new look",
                 "change of hairstyle", "different hairstyle",
                 "cut myself", "cutting myself", "burn", "scalp", "scissors in", "dandruff",
                 "book", "booking", "appointment", "reserve", "a slot",
                 "grey", "color", "colour", "dye", "dyed", "dyeing", "bleach", "bleached",
                 "shampoo", "wash", "washing", "fade", "fading", "highlights", "regrowth",
                 "my dog", "my cat", "children", "my child", "my son", "my daughter", "babys",
                 "own hair", "my own hair", "cut it myself", "at home", "haircut at home",
                 "grow", "grows", "growing", "grew", "growth", "faster", "longer", "thicker",
                 "static", "frizz", "frizzy", "flyaway", "flyaways", "greasy", "oily", "flakes",
                 "flaky", "falling out", "thinning", "bald", "tangles", "tangled", "knots",
                 "straighten", "straightener", "curling", "tongs", "dryer", "blow dry",
                 "flat", "lifeless", "limp", "volume", "curly", "curls", "wavy", "sticking up",
                 "sticks up", "rain", "raining", "humid", "humidity",
                 "gum", "chewing gum", "stuck", "glue", "lice", "nits", "sap", "wax",
                 "beard", "beards", "moustache", "mustache", "eyebrows", "eyebrow",
                 "nose hair", "ear hair", "pubic", "nails", "nail", "toenails", "cuticles",
                 "hedge", "hedges", "lawn", "bush", "bushes", "shrub", "claws", "wick",
                 "video", "videos",
                 "breakage", "breaking", "snapping", "snaps",
                 "plughole", "plug hole", "plugholes", "plug holes", "drain", "drains",
                 "sink", "sinks", "basin", "blocked", "blockage", "unblock", "trap",
                 "u bend", "waste pipe",
                 "door", "doors", "gate", "gates", "shutter", "shutters", "window", "windows",
                 "chimney", "chimneys", "blind", "blinds", "fence", "fences", "panel", "panels",
                 "radiator", "radiators", "pipe", "pipes", "loo", "toilet", "car", "van",
                 "cupboard", "drawer", "drawers", "shed", "garage", "letterbox", "bin",
                 "banging sound", "banging noise", "banging when", "is banging", "was banging",
                 "keeps banging", "bangs when", "bangs at", "bangs on",
                 "sound", "sounds", "noise", "noises", "knocking", "rattling", "clanking",
                 "humming", "whistling", "gurgling") + _HAIR_NOT_ON_A_HEAD + _SOMETHING_IN_THE_HAIR),
    entry("hair-split-ends", (("split ends", "split end", "ends", "hair"),
                              ("split", "ends", "stop", "fix", "get rid", "why", "splitting",
                               "frizzy", "dry", "damaged", "trim")),
          "Split ends cannot be repaired, so a 1cm trim is the only fix: then keep them tidy with "
          "conditioner on the mid-lengths and ends, a wide-tooth comb on wet hair and a towel "
          "squeezed rather than rubbed. Heat styling and a tight band in the same spot are what "
          "split them again fastest.",
          avoid=("washing", "shampoo", "greasy", "falling", "thinning", "dandruff", "matted",
                 "detangle", "knotty", "dog", "cat",
                 "bleach", "bleached", "dye", "dyed", "perming", "perm", "relaxer",
                 "nose hair", "ear hair", "eyebrows", "eyebrow", "beard", "moustache",
                 "blow dry", "blowdry", "hair dryer", "hairdryer", "curlers", "tongs",
                 "straighteners", "straighten",
                 "static", "static electricity", "flyaway", "flyaways", "flat", "volume",
                 "lifeless", "limp", "curly", "curls", "wavy", "sticking up", "sticks up")
                 + _HAIR_NOT_ON_A_HEAD
                 + _SOMETHING_IN_THE_HAIR),
    entry("hair-cut-yourself",
          (("fringe", "bangs", "own hair", "my own hair", "cut it myself", "haircut at home",
            "cut my hair at home", "trim it myself", "blunt cut", "layers"),
           ("cut", "cutting", "trim", "trimming", "myself", "how do i", "how to", "home",
            "at home", "best way", "evenly", "straight")),
          "Cut dry hair, so you can see where it actually falls, and take less off than you think: "
          "small snips across the width, not one line, because hair springs up once it dries. For a "
          "fringe, comb a thin section down flat, hold it between two fingers and cut just under "
          "them, checking both sides sit level with the eyebrow. For length, part it down the "
          "middle, bring both sides forward under the chin and cut them together so they match. "
          "Sharp hairdressing scissors, about fifteen pounds, give a far cleaner line than kitchen "
          "ones.",
          ask=("how do i", "how to", "how can i", "myself", "at home", "trim", "cut"),
          bias=1,
          avoid=("how often", "how frequently", "how regularly", "every few weeks", "how long between",
                 "beard", "beards", "moustache", "mustache", "eyebrows", "eyebrow", "nose hair",
                 "ear hair", "pubic", "toenails", "nails", "nail", "cuticles", "hedge", "hedges",
                 "lawn", "bush", "bushes", "shrub", "dog", "cat", "puppy", "kitten", "horse",
                 "baby", "babys", "babies", "newborn", "toddler", "my son", "my daughter",
                 "my child", "my kid", "children", "child",
                 "dye", "colour", "color", "bleach", "perm", "perming", "highlights", "blow dry",
                 "hair dryer", "hairdryer", "straighteners", "curlers", "tongs", "plughole",
                 "drain", "sink", "blocked",
                 "door", "doors", "gate", "gates", "shutter", "shutters", "window", "windows",
                 "chimney", "chimneys", "blind", "blinds", "fence", "fences", "panel", "panels",
                 "radiator", "radiators", "pipe", "pipes", "loo", "toilet", "car", "van",
                 "cupboard", "drawer", "drawers", "shed", "garage", "letterbox", "bin")),
    entry("hair-grow",
          (("grow", "grows", "growing", "grew", "growth", "longer", "faster", "thicker"),
           ("hair", "my hair", "it", "beard", "nails", "fringe")),
          "Hair grows about 1 to 1.5cm a month, and nothing makes that much faster: the length is "
          "set by your genes and how long each follicle keeps growing before it sheds. What you can "
          "do is stop losing it to breakage - fewer hot washes and straighteners, a wide-tooth comb "
          "on wet hair, a loose band rather than a tight bobble - and keep the ends trimmed every "
          "two or three months so splits do not travel up and make the length look thin. If it is "
          "thinning as well as slow, get iron, ferritin, thyroid and vitamin D checked, because "
          "that is the one cause worth fixing.",
          ask=("how", "grow", "grows", "faster", "longer", "thicker", "why", "what"),
          avoid=("beard", "beards", "moustache", "mustache", "nails", "toenails", "lawn", "grass",
                 "hedge", "hedges", "plant", "plants", "tomato", "tomatoes", "vegetables",
                 "business", "company", "savings", "pension", "money", "dog", "cat", "puppy",
                 "kitten", "baby", "babys", "babies", "newborn", "toddler", "my son",
                 "my daughter", "children", "child", "crystals", "crystal", "mould", "mold",
                 "friendship", "taller", "children grow")),
    entry("shower-often", (("shower", "showers", "showering", "bath", "baths", "bathe"),
                           ("how often", "often", "should", "daily", "every day", "a day",
                            "wash", "washing", "too much", "long")),
          "Two or three times a week is plenty for most adults, with a wash of the face, hands, "
          "feet, under the arms and the groin every day; the rest of the skin can wait. Five to "
          "ten minutes and lukewarm is enough for a whole shower, and long hot ones strip the oils "
          "out of dry skin, so moisturise while it is still damp. Wash more often in hot weather "
          "or after sport, because sweat and smell are what need washing off.",
          avoid=("blocked", "drain", "leak", "mould", "mold", "shower curtain", "shower head",
                 "limescale", "boiler", "bath bomb", "baby", "toddler", "newborn", "my dog",
                 "my cat", "screen", "tray", "grout", "tiles", "thermostat",
                 "day trip", "day out", "worth visiting", "worth it", "things to do",
                 "what to do", "to do in", "to see", "see in", "sightseeing", "get to",
                 "how long to", "how long does it take", "roman baths", "city", "town",
                 "weekend away", "stay in", "hotel", "travel", "visit",
                 "replace", "replacing", "replaced", "swap", "swapping", "swapped",
                 "install a shower", "installing a shower", "fit a shower", "fitting a shower",
                 "fitted a shower", "shower over the bath")),
    entry("grey-hair", (("hair",), ("grey", "gray", "white", "turn", "turning", "going",
                                     "coming out", "why")),
          "Hair gets its colour from melanin, and the cells that make it gradually stop as we "
          "age, so new hairs grow in without pigment. Genetics decides when that starts, and "
          "stress can speed it up but does not turn a single hair white overnight.",
          ask=("grey", "gray", "white", "silver"), bias=2,
          avoid=("loss", "lose", "losing", "fall", "falling", "fell", "bald", "balding",
                 "thinning", "thin", "shed", "shedding", "patch", "patches",
                 "roots", "regrowth", "cover", "dye", "dyed", "tint", "colour it",
                 "color it", "get rid", "rid of", "hide", "conceal", "blend")),
    entry("gone-grey", (("going", "gone", "goes", "turning", "turned", "turn"), ("grey", "gray")),
          "Hair gets its colour from melanin, and the cells that make it gradually stop as we "
          "age, so new hairs grow in without pigment. Genetics decides when that starts, and "
          "stress can speed it up but does not turn a single hair white overnight.",
          ask=("grey", "gray"), bias=2, slips=("grey", "gray"),
          avoid=("lips", "lip", "face", "facial", "skin", "gums", "gum", "fingertips",
                 "fingertip", "fingers", "finger", "toes", "toe", "hands", "hand", "feet",
                 "foot", "clammy", "sweaty", "passed out", "pass out", "faint", "fainted",
                 "unconscious", "unresponsive", "floppy", "limp", "breathing", "breathe",
                 "ambulance", "999", "911", "nails", "nail", "tongue", "teeth", "eyes",
                 "dog", "dogs", "cat", "cats", "puppy", "kitten", "horse", "pony", "pet",
                 "paint", "wall", "walls", "ceiling", "sky", "cloud", "clouds", "weather",
                 "car", "cars", "hair dye", "roots", "dye", "dyed", "tint", "cover",
                 "colour it", "color it", "hide", "conceal", "blend", "wardrobe", "curtains",
                 "washing", "laundry", "shirt", "shirts", "socks", "fabric", "wool",
                 "jeans", "trousers", "denim", "top", "tops", "jumper", "jumpers", "cardigan",
                 "hoodie", "dress", "dresses", "skirt", "coat", "jacket", "bedding", "sheets",
                 "towels", "towel", "wash", "washed", "wash it", "faded", "fading", "bleach",
                 "bleached", "faded black", "black clothes", "dark clothes")),
    entry("blood-red", (("blood",), ("red", "why", "colour", "color")),
          "Blood is red because of haemoglobin, the iron-containing protein in red cells that "
          "carries oxygen. Bright red blood is rich in oxygen; darker blood has given its oxygen "
          "to the body."),
    entry("fridge", (("fridge", "refrigerator", "freezer"), ("work", "works", "cold", "why",
                                                              "cool")),
          "A fridge moves heat out of the inside and dumps it at the back. A pump compresses a "
          "refrigerant gas, which releases heat, then lets it expand inside the fridge, where it "
          "absorbs heat and cools the air.",
          avoid=("smell", "smells", "smelly", "stink", "stinks", "odour", "noise", "noisy", "hum",
                 "humming", "rattl", "leak", "leaking", "frost", "frosting", "broken", "repair",
                 "keep", "keeping", "cooked", "raw", "store", "stored", "storage", "freeze",
                 "freezer", "days", "long")),
    entry("birds-fly", (("bird", "birds"), ("fly", "flying", "wing", "wings")),
          "A bird's wing is curved on top, so air moving over it travels faster and presses less "
          "than the air underneath; the difference lifts the bird. Flapping provides thrust, and "
          "light, hollow bones keep the whole body easy to carry.",
          avoid=("broken", "bleeding", "hurt", "injury", "injured", "vet", "sick", "clip",
                 "clipping", "pluck", "plucking", "feather", "feathers", "cage", "nest", "nests",
                 "roof", "eaves", "pet", "parrot", "budgie", "aviary", "chicken", "chickens",
                 "eat", "feed", "seed", "south", "migrate", "migrating", "migration", "winter",
                 "window", "windows", "glass")),
    entry("antibiotics", (("antibiotic", "antibiotics"), ("work", "works", "what", "how", "do")),
          "Antibiotics kill bacteria or stop them growing, usually by attacking something "
          "bacterial cells have and ours do not, such as their cell walls. They do nothing for "
          "colds and flu, which are viruses, and using them when they are not needed helps "
          "resistant bacteria spread.",
          avoid=("pill", "contraception", "contraceptive", "pregnant", "alcohol", "drinking",
                 "drunk", "missed", "dose", "side effect", "side effects",
                 "cold", "colds", "flu", "virus", "viral")),
    entry("plant-up", (("plant", "plants", "seedling", "seedlings", "roots", "shoots"),
                       ("gravity", "which way", "upside down", "up from down", "grow up",
                        "grows up", "growing up", "grow down", "grows down", "growing down",
                        "upwards", "downwards")),
          "Plants sense gravity using tiny starch grains inside their cells: shoots grow away "
          "from gravity and roots grow towards it. They also bend towards light, which is why a "
          "seedling on a windowsill leans that way.",
          avoid=("bulb", "bulbs", "potato", "potatoes", "tulip", "tulips", "daffodil",
                 "daffodils", "onion", "onions", "garlic", "seed", "seeds", "sow", "sowing",
                 "depth", "deep", "spacing", "compost", "soil", "pot", "pots")),
    entry("climate-change", (("climate change", "global warming"), ("what", "why", "cause",
                                                                      "causes", "happen")),
          "Burning coal, oil and gas releases carbon dioxide, which traps heat in the atmosphere "
          "instead of letting it escape to space. That extra heat raises average temperatures, "
          "melts ice and makes extreme weather more likely; the science is settled, though "
          "predicting any one storm is not."),

    entry("sun-yellow", (("sun",), ("yellow", "white", "colour", "color")),
          "The Sun sends out every colour mixed together, so from space it looks white; through "
          "our air the blue is scattered away and what reaches you looks yellow-white. Low in the "
          "sky it looks orange because the light crosses even more air on the way in.",
          ask=("why", "what", "how", "is"),
          bias=2),
    entry("sun-age", (("sun",), ("old", "age")),
          "The Sun is about 4.6 billion years old, roughly halfway through its life, and it has "
          "another 5 billion years or so before it swells into a red giant. The Earth formed at "
          "about the same time, from the same cloud of dust and gas.",
          ask=("how", "old", "age")),
    entry("stars-night", (("star", "stars"), ("night", "dark", "day", "daytime")),
          "The stars are there in the daytime too: the sun lights up the air above you so "
          "brightly that their faint light is drowned out. Away from city lights, and out of the "
          "sun's glare, thousands more of them come into view.",
          ask=("why", "only", "see", "visible", "what")),
    entry("moon-horizon", (("moon",), ("big", "bigger", "large", "huge", "horizon", "size",
                                        "illusion")),
          "The Moon looks bigger near the horizon because of an illusion in how your brain judges "
          "it against the landscape; photograph it and it comes out the same size as when it is "
          "high overhead. It also looks dimmer down there, not brighter, because its light is "
          "crossing more air.",
          ask=("why", "look", "looks", "seems", "appear", "appears"),
          bias=2),
    entry("mountain-cold", (("mountain", "mountains", "altitude", "hill", "summit"),
                            ("cold", "colder", "temperature", "freezing")),
          "Air thins and expands as it rises, so it holds less heat, and the ground gives its "
          "warmth up to the cold sky faster than thin air can hold it: the temperature drops about "
          "6.5C for every kilometre you climb. The sunshine up high can still feel fierce while "
          "the air around you stays cold.",
          ask=("why", "colder", "cold")),
    entry("earth-age", (("earth", "planet"), ("old", "age", "formed", "born")),
          "The Earth is about 4.54 billion years old, worked out from meteorites and the oldest "
          "rocks. Life got going within the first billion years, and everything humans have done "
          "fits into the last tiny sliver of that time.",
          ask=("how", "old", "age", "when")),
    entry("earth-spin", (("earth",), ("spin", "spins", "spinning", "rotate", "rotates",
                                     "rotation")),
          "The Earth spins because the cloud of dust and gas it formed from was already turning, "
          "and nothing has braked it much in 4.5 billion years. The Moon's tides are slowly "
          "slowing it, so the day grows about a second longer every 50,000 years or so.",
          ask=("why", "does", "what", "how")),
    entry("fish-breathe", (("fish", "fishes"), ("breathe", "breathing", "underwater", "gills",
                                                 "water")),
          "Fish take oxygen out of the water with gills: water flows in at the mouth and over thin, "
          "blood-rich filaments, where oxygen passes into the blood and carbon dioxide passes out. "
          "Out of water the filaments collapse and stick together, so the fish suffocates even in "
          "air.",
          ask=("how", "why", "do", "does", "what"),
          bias=2),
    entry("birds-migrate", (("bird", "birds"), ("migrate", "migration", "south", "leave",
                                                 "leaves")),
          "Birds head off in autumn because the insects, worms and berries they live on run out as "
          "the days shorten; the trip costs a lot of energy but beats starving. They find their "
          "way by the sun, the stars, landmarks and the Earth's magnetic field, and many come back "
          "to the same nest site.",
          avoid=("home", "job", "city", "nest", "leaving me"),
          ask=("why", "south", "winter", "when", "do"),
          bias=2),

    entry("virus-bacteria", (("virus", "viruses", "viral"),
                            ("bacteria", "bacterial", "bacterium", "difference", "vs", "versus")),
          "A virus is a scrap of genetic code in a protein coat that can only multiply inside your "
          "cells; bacteria are single living cells that can grow and divide on their own. So "
          "antibiotics kill bacteria but do nothing for a cold or flu, which are viral.",
          ask=("difference", "vs", "versus", "between", "bacteria", "bacterial")),
    entry("virus-what", (("virus", "viruses"),
                         ("what", "mean", "made", "work", "live", "cell", "alive")),
          "A virus is a scrap of genetic code wrapped in a protein coat, and it can only copy "
          "itself inside a living cell. That is why antibiotics do nothing for a cold or flu: "
          "they kill bacteria, which are cells that can grow on their own.",
          ask=("what", "mean", "made", "work", "live", "cell", "alive"),
          avoid=("bacteria", "bacterial", "difference", "vs", "versus", "antibiotic",
                 "computer", "email", "phone")),
    entry("bacteria-what", (("bacteria", "bacterium", "bacterial"),
                            ("what", "mean", "made", "good", "bad", "work", "live")),
          "Bacteria are single-celled living things, so small that millions fit on a pinhead. "
          "Most are harmless or useful, from the ones in yoghurt to the ones in your gut, and a "
          "few cause illness; unlike a virus, a bacterium can grow and divide on its own.",
          ask=("what", "mean", "made", "good", "bad", "work", "live"),
          avoid=("virus", "viral", "difference", "vs", "versus", "antibiotic", "probiotic",
                 "yoghurt", "yogurt", "urine", "uti", "pee", "bladder", "infection")),
    entry("antibiotics-cold", (("antibiotic", "antibiotics", "penicillin"),
                              ("cold", "colds", "flu", "virus", "viral", "sore throat")),
          "Antibiotics do nothing for a cold or flu: those are viruses and antibiotics only kill "
          "bacteria. What actually helps is rest, plenty of fluids, and paracetamol or ibuprofen "
          "for the aches, plus honey in warm water for a cough; see someone if a fever lasts more "
          "than a few days or you are breathless.",
          ask=("cold", "colds", "flu", "virus", "viral", "throat"),
          bias=2),
    entry("cold-remedy", (("cold", "colds"), ("help", "helps", "actually", "best", "remedy",
                                              "cure", "better", "shift", "take", "takes",
                                              "taking", "rid",
                                              "stop", "stopping", "shake", "shaking", "fight",
                                              "fighting", "get over", "getting over",
                                              "prevent", "preventing", "ward off", "avoid",
                                              "avoiding", "coming on", "in its tracks",
                                              "dodge", "quickly", "fast",
                                              "deal", "dealing", "treat", "treating",
                                              "treatment", "lingering", "still got",
                                              "look after", "looking after", "looked after",
                                              "care", "caring", "care for", "caring for",
                                              "nurse", "nursing", "get through",
                                              "what can i do", "what do i do", "can i do",
                                              "anything i can",
                                              "what should i do", "what shall i do",
                                              "should i do about", "do about",
                                              "medicine", "medicines", "medication",
                                              "tablets", "tablet", "syrup", "lemsip",
                                              "pharmacy", "chemist", "good for",
                                              "what is good for", "whats good for",
                                              "keep away", "keeping away", "keeps away",
                                              "colds away", "stay well", "keeping well",
                                              "not catch", "fight off")),
          _cold_help,
          avoid=("eat", "eating", "food", "left out", "leaving", "shower", "bath", "sauna",
                 "beer", "drink", "shell", "sweat", "sweatshirt", "weather", "sore shoulder",
                 "fridge", "freezer", "frozen", "freezing", "radiator", "draught", "draft",
                 "window", "outside", "tap",
                 "heating", "boiler", "boilers", "thermostat", "central heating", "hot water",
                 "plumbing", "flue", "immersion", "combi", "trv", "no heat", "stone cold",
                 "cold sore", "cold sores", "herpes", "lip", "lips", "blister", "blisters",
                 "hands", "hand", "feet", "foot", "fingers", "fingertips", "toes", "toe",
                 "feeling cold", "always cold", "being cold", "so cold", "too cold",
                 "call", "calls", "caller", "callers", "calling", "cold call", "cold calls",
                 "flat", "house", "home", "room", "rooms", "bedroom", "kitchen", "office",
                 "shed", "garage", "caravan", "conservatory",
                 "wall", "walls", "ceiling", "ceilings", "corner", "corners",
                 "condensation", "condensing", "damp", "mould", "damp patch",
                 "keep getting", "keeps getting", "getting colds", "get colds",
                 "catching colds", "catch colds", "one after another", "all the time",
                 "always ill", "always sick", "every winter", "every year",
                 "hands getting cold", "hands are cold", "hands get cold", "hands go cold",
                 "hands going cold", "cold hands", "hand is cold", "my hand is cold",
                 "fingers are cold", "fingers getting cold", "fingers go cold",
                 "cold fingers", "feet are cold", "feet get cold", "feet getting cold",
                 "feet go cold", "cold feet", "foot is cold", "toes are cold",
                 "toes get cold", "cold toes", "toes go cold",
                 "car", "cars", "van", "engine", "battery", "ignition", "starter",
                 "windscreen", "windshield", "diesel", "petrol", "motorbike"),
          ask=("help", "helps", "actually", "best", "remedy", "cure", "better", "shift",
               "take", "takes", "taking", "rid",
               "stop", "stopping", "shake", "shaking", "fight", "fighting", "get over",
               "getting over", "prevent", "preventing", "ward off", "avoid", "avoiding",
               "coming on", "in its tracks", "dodge", "quickly", "fast",
               "deal", "dealing", "treat", "treating", "treatment", "lingering", "still got",
               "look after", "looking after", "looked after", "care", "caring", "care for",
               "caring for", "nurse", "nursing", "get through",
               "what can i do", "what do i do", "can i do", "anything i can",
               "what should i do", "what shall i do", "should i do", "do about",
               "what helps", "anything for",
               "medicine", "medicines", "medication", "tablets", "syrup", "lemsip",
               "pharmacy", "chemist", "good for",
               "keep away", "keeping away", "colds away", "stay well", "keeping well",
               "not catch", "fight off"),
          bias=1, guard=_not_a_food_cold),
    entry("colds-repeated", (("cold", "colds"), ("keep getting", "keeps getting", "get colds",
                                                 "getting colds", "always ill", "always sick",
                                                 "one after another", "cold after cold",
                                                 "so many colds", "colds constantly",
                                                 "constantly ill", "catching colds",
                                                 "catch colds", "cold every", "colds every",
                                                 "colds a year", "cold a year", "how many colds",
                                                 "colds in a year",
                                                 "how often do colds", "how often do you get",
                                                 "how often do i get", "how often do people get",
                                                 "how often should i get", "how often am i")),
          "Most adults catch two to four colds a year and children get more, because hundreds of "
          "different viruses cause them, so one after another is normal. Sleep, handwashing, your "
          "own cup and towel and not smoking all help; if they come much more often than that, or "
          "each one turns into a chest infection, get it checked.",

          avoid=("cold sore", "cold sores", "blister", "blisters",
                 "hands getting cold", "hands are cold", "hands get cold", "hands go cold",
                 "hands going cold", "cold hands", "hand is cold", "my hand is cold",
                 "fingers are cold", "fingers getting cold", "fingers go cold",
                 "cold fingers", "feet are cold", "feet get cold", "feet getting cold",
                 "feet go cold", "cold feet", "foot is cold", "toes are cold",
                 "toes get cold", "cold toes", "toes go cold",
                 "cold call", "cold calls", "call", "calls", "caller", "callers", "phone",
                 "phone call", "phone calls"),
          guard=not_the_flat_you_live_in,

          ask=("cold", "colds", "getting", "keep", "ill", "sick", "always"),
          bias=1),
    entry("ageing", (("ageing", "aging", "get older", "getting older", "grow old", "growing old",
                      "old age", "we age", "people age", "humans age", "body age", "we get old",
                      "people get old", "humans get old"),
                     ("why", "how", "cause", "causes", "happen", "happens", "what", "does")),
          "Ageing is the slow build-up of small damage: cells divide less accurately, DNA and "
          "proteins get worn, and the body's repair and energy systems slow down. That makes "
          "illness more likely over time, but sleep, exercise, not smoking and a varied diet all "
          "shift the odds; how fast it happens is only partly fixed by your genes.",
          avoid=("school", "kid", "kids", "child", "children", "nursery", "potty", "start",
                 "at my age", "at your age", "at what age", "learn", "learning", "guitar",
                 "wrinkle", "wrinkles", "wrinkled", "skin", "dog", "dogs", "cat", "cats",
                 "pet", "pets",
                 "iron age", "stone age", "bronze age", "ice age", "dark ages", "middle ages",
                 "age of", "space age", "new age", "nuclear age", "coming of age")),
    entry("sneeze-sun", (("sneeze", "sneezing", "sneezes"),
                        ("sun", "sunlight", "bright", "sunshine")),
          "Bright light sets off a sneeze in about one person in four: the light triggers the same "
          "nerve that starts a sneeze reflex, so looking at the sun or walking out of a dark "
          "cinema does it. It is harmless and tends to run in families.",
          ask=("why", "does", "do", "sun", "light", "bright"),
          bias=2),
    entry("sneeze-why", (("sneeze", "sneezing", "sneezes"),
                        ("why", "makes", "make", "nose", "dust", "pollen", "allergy", "cause",
                         "happen")),
          "A sneeze is your nose clearing itself: dust, pollen or a virus irritates the lining and "
          "the body blasts air out to shift it. The droplets fly several metres, which is why you "
          "catch it in your elbow rather than your hand.",
          ask=("why", "cause", "happen", "what")),
    entry("ears-pop", (("ear", "ears"), ("pop", "pops", "popping", "popped", "plane",
                                          "flight", "pressure")),
          "Ears pop because the air pressure around you changes faster than the pressure inside "
          "your middle ear - in a lift, or in a plane as it climbs. Swallowing, yawning, or holding "
          "your nose and blowing gently pushes it back into balance; a blocked nose from a cold "
          "makes it harder.",
          ask=("why", "do", "does", "what", "pop", "pops", "popping", "popped", "pressure"),
          avoid=("hurt", "hurts", "hurting", "pain", "painful", "ache", "aches", "aching",
                 "throb", "throbbing", "sore", "tender", "tenderness"),
          bias=2),
    entry("brain-freeze", (("brain freeze", "brainfreeze", "ice cream headache"),
                          ("ice", "cream", "cold", "drink", "drinks", "eat", "eating", "why",
                           "get", "getting", "cause", "causes")),
          "A cold mouthful chills the roof of your mouth and the blood vessels there tighten, then "
          "widen again; that swing is the stabbing headache behind your forehead. Eat more slowly, "
          "or press your tongue to the roof of your mouth to warm it, and it fades in a minute.",
          ask=("why", "get", "gets", "what", "cause"),
          bias=1),
    entry("freckles-why", (("freckle", "freckles"),
                           ("why", "cause", "causes", "happen", "happens", "get", "getting",
                            "what", "appear")),
          "Freckles are little patches of melanin, the pigment that colours skin, made by cells "
          "that respond to sunlight; people with paler skin and certain genes make more of it, "
          "which is why they show up after time in the sun. They are harmless, but a new or "
          "changing spot needs checking, and sunscreen keeps them from darkening.",
          avoid=("rid", "remove", "fade", "laser", "cover", "makeup", "cream", "bleach",
                 "mole", "moles", "changing", "cancer", "check", "checking", "worried",
                 "worry", "baby", "babies", "child", "children", "kid", "kids")),
    entry("deja-vu-why", (("deja vu", "déjà vu", "dejavu"),
                          ("why", "cause", "causes", "happen", "happens", "what", "get", "feels",
                           "feel", "mean")),
          "Deja vu is a brief misfire in memory: the brain takes in a new scene and, for a second, "
          "files it as familiar, often because a similar layout or sound has primed the same "
          "circuits. It is common and harmless, especially when tired; if it comes with a seizure, "
          "a smell or a feeling of losing time, get it checked.",
          avoid=("seizure", "seizures", "epilepsy", "medication", "medicine", "doctor", "gp",
                 "worried", "worry", "dementia")),
    entry("forgetting-why", (("forget", "forgetting", "forgot", "memory", "memories",
                              "lose", "losing",
                              "remember birthdays", "remembering birthdays",
                              "remember everyones birthdays",
                              "keep track of birthdays", "remember birthdays and", "birthday list",
                              "track of everyones birthdays", "track of everybodys birthdays",
                              "everyones birthdays", "everybodys birthdays",
                              "track of my friends birthdays"),
                             ("why", "cause", "causes", "happen", "happens", "what", "things",
                              "everything", "names", "words", "so")
                             + BLANK_WORDS),
          _forgetting,
          guard=_an_amount_of_losing,
          avoid=("study", "studied", "studying", "revise", "revising", "revision", "exam",
                 "exams", "learn", "learning", "test", "school", "course", "keys", "key",
                 "password", "passwords", "dementia", "alzheimer", "alzheimers",
                 "mum", "dad", "mother", "father", "grandma", "grandad", "wife", "husband",
                 "worried", "worry", "what did i", "what you said", "remind", "told", "again",
                 "nan", "nana", "granny", "grandmother", "grandfather", "aunt", "uncle", "friend",
                 "partner", "son", "daughter", "brother", "sister", "neighbour",
                 "things better", "remember better", "better at remembering",
                 "he says", "she says", "he just", "she just", "he doesnt", "she doesnt",
                 "he doesn't", "she doesn't", "he cant", "she cant", "he can't", "she can't",
                 "to drink", "to eat", "to take", "to feed", "to walk", "to pay", "to call",
                 "to text", "to reply", "to post", "to book", "to bring", "to charge",
                 "interest", "interested", "interesting", "enjoy", "enjoyed", "enjoying",
                 "enjoyment", "hobbies", "hobby", "motivation", "motivated", "bothered",
                 "to water", "to tidy", "to clean", "to put", "to send", "to ring",
                 "scary", "scared", "scares", "frightening", "frightened", "terrifying",
                 "lately", "recently", "these days", "nowadays", "for months", "for weeks",
                 "for a while", "all the time", "constantly", "non stop",
                 "terrified", "upsetting", "upsets",
                 "so lost", "feel lost", "feeling lost", "felt lost", "completely lost",
                 "totally lost", "bit lost", "little lost", "get lost", "got lost", "lost at",
                 "lost in life", "lost in it", "lost with all", "lost with it", "lost with the",
                 "lost my way", "im lost", "i am lost", "i was lost",
                 "improve", "improving", "improvement", "improvements", "sharper", "boost",
                 "technique", "techniques", "better memory", "memory better",
                 "improve my memory", "improve your memory", "memory improve",
                 "memorise", "memorize", "memorising", "memorizing")),
    entry("remember-the-birthdays",
          (("birthday", "birthdays"),
           ("how do i", "how can i", "how could i", "how do you", "how to", "how should i",
            "tips", "tip", "advice", "best way", "any way", "is there a way", "keep track",
            "track of", "a way to", "the trick", "tricks",
            "reminder ideas", "reminder idea", "reminders for birthdays")),
          _forgetting, bias=1,
          avoid=("party", "parties", "plan", "planned", "planning", "present", "presents",
                 "gift", "gifts", "cake", "cakes", "decorate", "decorations", "host", "hosting",
                 "venue", "invite", "invites", "invitations", "surprise", "theme", "themes",
                 "games", "song", "songs", "dinner", "balloons", "when is", "whens", "what date",
                 "how old", "age", "card", "cards", "message", "wish", "wishes", "happy birthday",
                 "song", "sang", "sing")),
    entry("pruney-fingers", (("finger", "fingers", "fingertip", "fingertips", "toe", "toes",
                              "hand", "hands"),
                             ("pruney", "shrivelled", "shriveled", "shrivel", "prune", "bath",
                              "bathtub", "swim", "swimming", "pool", "soak", "soaking", "water",
                              "wet")),
          "The skin on fingers and toes puckers in water because the outer layer soaks up water "
          "while the nerves underneath tighten tiny blood vessels, which pulls the surface into "
          "ridges; it seems to give a better grip on wet things. It fades within minutes of drying "
          "and is not a sign of getting old.",
          ask=("why", "what", "how", "cause", "happen", "get", "go", "become", "turn"),
          avoid=("cut", "cuts", "hurt", "hurts", "pain", "painful", "swollen", "swelling", "numb",
                 "tingle", "tingling", "rash", "eczema", "arthritis", "infection", "cracked",
                 "age", "old", "ageing", "aging")),
    entry("morning-breath", (("morning breath", "bad breath", "breath smells", "breath stinks",
                              "halitosis"),
                             ("why", "cause", "morning", "get", "what", "how", "stop", "fix")),
          "Morning breath comes from a dry mouth: saliva slows overnight, so bacteria on the "
          "tongue and between the teeth break down food and cells and give off sulphur-smelling "
          "gas. Brush and floss before bed, clean your tongue, drink water, and see a dentist if it "
          "lasts all day, because gum disease is a common cause.",
          avoid=("dog", "dogs", "cat", "cats", "puppy", "kitten", "baby", "babies", "child",
                 "children", "mask", "diabetes", "ketone", "liver", "kidney", "coffee",
                 "garlic", "onion", "onions", "eating", "food", "lunch",
                 "tell", "tells", "telling", "mention", "raise it", "bring it up",
                 "bring this up", "how do i say", "how should i say")),
    entry("dark-circles", (("dark circles", "bags under my eyes", "bags under the eyes",
                            "puffy eyes", "under eye bags", "dark rings under my eyes"),
                           ("why", "cause", "get", "what", "how", "rid", "help", "always")),
          "The skin under the eyes is thin, so blood vessels and muscle show through more when you "
          "are tired, dehydrated or have a cold; genes, allergies and thinning skin with age make "
          "them darker. Sleep, water and an antihistamine if allergies are behind it help, and a "
          "caffeine eye cream can soften the look for a while.",
          avoid=("concealer", "makeup", "filler", "surgery", "laser", "tattoo", "dog", "cat",
                 "baby", "child", "pregnant", "pregnancy")),
    entry("sleepy-after-eating", (("sleepy after eating", "tired after eating", "sleepy after lunch",
                                   "food coma", "drowsy after eating", "sleepy after a meal",
                                   "tired after lunch"),
                                  ("why", "feel", "get", "always", "what", "cause")),
          "After a big meal, blood flow shifts to the gut and the body clock dips in the early "
          "afternoon, so feeling sleepy is normal, especially with a lot of refined carbs or "
          "alcohol. A smaller lunch, a short walk and daylight help; see a GP if it happens after "
          "every meal with thirst, weight loss or falling asleep mid-conversation.",
          avoid=("baby", "babies", "child", "children", "dog", "cat", "medicine", "tablet",
                 "diabetes", "pregnant", "pregnancy")),
    entry("laughter-why", (("laugh", "laughing", "laughter", "giggle", "giggling"),
                           ("why", "human", "humans", "contagious", "nervous", "funny", "social",
                            "what")),
          "Laughter is mostly social: people laugh far more with someone else there, and it "
          "signals that a threat or a mistake is harmless, which is why nervous giggles and "
          "contagious laughter happen. It releases tension and bonds a group, and there is no "
          "single joke centre in the brain.",
          ask=("why", "what", "human", "humans", "people", "contagious", "nervous", "social"),
          avoid=("at me", "bully", "bullied", "can't stop", "cant stop", "uncontrollable",
                 "crying", "therapy", "nervous breakdown", "baby", "babies", "child",
                 "children", "infant", "infants", "toddler", "toddlers", "kid", "kids")),
    entry("stomach-growl", (("stomach growl", "stomach growling", "tummy rumbling",
                             "stomach rumbling", "belly rumbling", "gurgling stomach",
                             "stomach gurgling"),
                            ("why", "what", "cause", "loud", "hungry", "mean", "happen")),
          "The growl is peristalsis: the gut's muscles squeeze and push gas and fluid along, and "
          "an empty stomach sounds louder because there is less food to muffle it. It is normal, "
          "and eating something or drinking water usually settles it; see a GP if it comes with "
          "pain, bloating or weight loss.",
          avoid=("dog", "dogs", "cat", "cats", "puppy", "kitten", "baby", "babies", "child",
                 "children", "period", "pregnant", "pregnancy")),
    entry("shiver", (("shiver", "shivering", "shivers", "shivery"),
                     ("cold", "warm", "body", "freezing", "get", "why", "keep", "keeps",
                      "always", "cant stop", "can't stop", "fever", "flu")),
          "Shivering is your muscles twitching fast on purpose: the movement makes heat, which is "
          "the body's way of holding its temperature when it is losing warmth faster than it makes "
          "it. Shivering with a fever means your temperature is still climbing, so wrap up and "
          "drink something warm.",
          avoid=("hands", "hand", "fingers", "arm", "arms", "voice", "nervous", "anxious",
                 "tremor", "tremors", "shaky", "shaking", "parkinsons", "parkinson's",
                 "dog", "dogs", "dog's", "puppy", "puppies", "pup", "cat", "cats", "kitten",
                 "kittens", "rabbit", "rabbits", "bunny", "horse", "horses", "pony", "ponies",
                 "hamster", "guinea pig", "budgie", "bird", "parrot", "pet", "pets"),
          ask=("why", "do", "does", "what", "keep", "keeps", "always", "cant stop",
               "can't stop", "fever"),
          bias=2),
    entry("pins-needles", (("pins and needles", "pins", "needles"),
                          ("hand", "hands", "arm", "foot", "feet", "leg", "numb", "tingle",
                           "tingling", "get", "why")),
          "Pins and needles come from a nerve being squashed, say by sitting on your foot: the "
          "signals get muddled, and the tingling is the nerve waking up as the pressure comes off. "
          "It usually clears in a minute or two; if it keeps coming back on its own, get it "
          "checked.",
          ask=("why", "get", "what", "cause")),
    entry("spicy-burn", (("spicy", "chilli", "chili", "chillies", "chillis", "hot sauce",
                          "curry"),
                        ("burn", "burns", "burning", "mouth", "hot", "heat", "throat")),
          "Chilli heat is not real heat: capsaicin switches on the same nerve receptors as a burn, "
          "so your mouth reports fire. Milk, yoghurt or ice cream settle it because the fat and "
          "milk protein lift the capsaicin away; water and beer just spread it round.",
          ask=("why", "does", "do", "so", "what", "how", "cool", "stop", "settle",
               "burning", "burns")),
    entry("blush", (("blush", "blushing", "blushes", "go red", "going red", "face go red",
                     "face goes red", "face is red", "face red"),
                    ("face", "cheeks", "embarrassed", "embarrassing", "red", "why", "cause",
                     "causes")),
          "Blushing is adrenaline opening up the small blood vessels in your face, and it happens "
          "when you feel exposed to other people's attention. You cannot stop it on purpose, which "
          "is exactly why it makes you more embarrassed, though people read it as honest rather "
          "than weak.",
          ask=("why", "do", "does", "what"),
          avoid=("makeup", "make up", "blusher", "powder", "shade", "blend", "apply",
                 "patchy", "patch",
                 "drink", "drinking", "drunk", "alcohol", "beer", "wine", "vodka", "hangover",
                 "exercise", "exercising", "running", "run", "gym", "sport", "workout",
                 "hot", "heat", "fever", "temperature", "sun", "sunburn", "sunburnt",
                 "rash", "rosacea", "allergic", "allergy", "spicy", "menopause",
                 "high blood pressure",
                 "cry", "crying", "cried", "tears", "shower", "bath",
                 "cough", "coughing", "sneeze", "sneezing", "sing", "singing")),
    entry("butterflies", (("butterflies", "knots in my stomach", "fluttery stomach"),
                          ("stomach", "tummy", "belly", "gut", "nervous", "nerves")),
          "Nerves and gut share the same wiring: adrenaline diverts blood to your muscles and slows "
          "digestion, so your stomach feels fluttery or churny. Slow breathing helps because it "
          "switches the body back toward rest, and it passes once the moment does.",
          ask=("why", "get", "what")),
    entry("dizzy-standing", (("dizzy", "dizziness", "lightheaded", "light headed", "head rush",
                              "faint", "fainting", "feel faint", "nearly faint",
                              "woozy", "woozy headed", "giddy", "swimmy", "swimmy headed",
                              "swim headed", "head spins", "head spinning", "head swims",
                              "saw stars", "see stars", "stars in front of my eyes",
                              "my vision went", "vision goes", "the spins", "all funny",
                              "eyes go funny", "drains from my head", "blood drains"),
                            ("stand", "standing", "stood", "get up", "getting up", "up",
                             "stand up", "stood up", "sat up", "sitting up", "out of bed",
                             "on my feet")),
          "Standing up quickly lets blood pool in your legs for a moment before your body tightens "
          "the vessels and adjusts, so your head is briefly short of blood and you see stars. Get "
          "up in two stages, drink enough water, and see a doctor if you actually faint or it "
          "happens most times you stand.",
          ask=("why", "when", "do", "does", "every time", "each time", "whenever", "sometimes",
               "often", "always", "most times")),
    entry("dizzy-spell", (("dizzy", "dizziness", "lightheaded", "light headed", "light-headed",
                     "giddy", "woozy", "head rush", "seeing stars",
                     "pass out", "passing out", "going to pass out", "about to pass out",
                     "faint", "fainting", "feel faint", "nearly faint", "going faint",
                     "see stars"),
                    ("what", "why", "how", "causes", "cause", "feel", "feels", "feeling", "felt",
                     "get", "getting", "keep", "keeps", "kept", "always", "constantly",
                     "suddenly", "stop", "treat", "help", "normal", "morning", "mornings",
                     "every", "when", "whenever", "after", "before", "during", "at", "in",
                     "on", "going", "might", "im", "i'm", "ive", "have", "had", "am", "and")),
          _a_dizzy_spell,
          avoid=("stand", "standing", "stood", "get up", "getting up", "getting out of bed",
                 "yesterday", "last night", "last week", "this morning", "this afternoon",
                 "earlier", "ago", "already", "the other day", "an hour ago",
                 "keep fainting", "keeps fainting", "fainting spells", "keep passing out",
                 "keeps passing out", "passed out", "black out",
                 "sometimes", "often", "twice", "again and again", "every few weeks",
                 "blacked out", "blacking out",
                 "out of bed", "on my feet",
                 "heights", "film", "films", "movie", "movies", "hitchcock", "ride", "roller",
                 "coaster", "rollercoaster", "theme park", "fairground",
                 "child", "children", "kid", "kids", "son", "sons", "daughter", "daughters",
                 "baby", "babies", "toddler", "toddlers", "boy", "boys", "girl", "girls",
                 "grandson", "grandsons", "granddaughter", "granddaughters", "pupil", "pupils",
                 "teenager", "teenagers", "school",
                 "heart", "palpitations", "heartbeat", "racing", "pounding", "pounding heart",
                 "chest", "flutters", "fluttering",
                 "dog", "dogs", "puppy", "cat", "cats", "kitten", "rabbit", "hamster", "horse",
                 "printer", "screen", "monitor", "computer",
                 "smell", "smells", "faint smell", "line", "lines", "faint line", "writing",
                 "print", "noise", "sound", "light", "accent", "memory", "hope", "chance",
                 "vertigo when i lie down", "vertigo lying down", "vertigo when i lay down",
                 "vertigo in bed", "vertigo rolling over", "vertigo turning over",
                 "bppv", "epley", "positional vertigo"),
          bias=1),
    entry("falls-elderly",
          (("fall", "falls", "falling", "fell", "fallen", "trips", "tripped", "tripping",
            "shuffle", "shuffles", "shuffling", "shuffled", "small steps", "tiny steps",
            "little steps", "not lifting her feet", "not lifting his feet",
            "wont lift her feet", "wont lift his feet", "feet dont leave the floor",
            "tripping over", "trips over", "tripped over", "keeps tripping", "trip over",
            "gone over", "goes over", "unsteady", "wobbly", "off balance", "bad balance",
            "poor balance", "balance is bad", "balance is poor", "balance isnt great",
            "balance isn't great", "balance problems", "lost her footing", "lost his footing",
            "lost their footing", "losing her balance", "losing his balance",
            "losing their balance", "loses her balance", "loses his balance",
            "loses their balance", "lost her balance", "lost his balance",
            "lost their balance"),
           ("keeps", "keep", "kept", "twice", "three times", "several times", "a few times",
            "lately", "recently", "often", "always", "constantly", "unsteady", "wobbly",
            "balance", "feet", "foot", "walking", "stand", "standing", "all the time",
            "off her feet",
            "off his feet", "risk", "worried", "worry", "scared",
            "stop", "stops", "stopped", "prevent", "prevention", "reduce the risk",
            "safer", "help her", "help him", "help them", "what can i do", "how do i",
            "in the night", "at night", "during the night", "night time", "nighttime",
            "gets up in the night", "in the dark", "when it is dark", "when its dark",
            "what should i do", "should i do", "do about", "falls over", "falling over",
            "fell over", "my dad", "my mum", "my mother",
            "my father", "my nan", "my nana", "my grandad", "my grandma", "my granny",
            "grandad", "grandma", "granny", "grandpa", "elderly", "oap", "in her 80s",
            "in his 80s", "in her 90s", "in his 90s", "80", "90",
              "had", "has had", "two", "three", "four", "this month", "last month",
            "this year", "since", "again")),
          "Falls are usually several small things adding up rather than one bit of clumsiness: leg "
          "strength and balance, eyesight, blood pressure that dips on standing, medicines, and the "
          "house itself - which is why the second one is worth acting on rather than waiting for the "
          "third. Ask the GP for a falls review: they check blood pressure lying and standing, go "
          "through the medicines, and can refer to a falls clinic or a strength and balance class, "
          "which is what actually cuts falls. Then take the house apart: grab rails on the stairs "
          "and by the loo, a night light, rugs lifted or taped down, cables out of the walkway, and "
          "a phone within reach from the floor. If they cannot get up or put weight on it, or knock "
          "their head - especially on a blood thinner - that is a same-day call.",
          bias=1,
          guard=_a_fall_a_person_had,
          avoid=("asleep", "sleep", "fell out with", "fall out with", "falling out with",
                 "fallen out with", "out with", "not talking", "stopped talking", "made up",
                 "make up", "behind", "apart", "prices", "shares", "rain",
                 "had a falling out", "a falling out", "falling out last", "fell out over",
                 "fall out over", "falling out over",
                 "keep falling out", "always falling out", "keeps falling out",
                 "we fell out", "we have fallen out", "weve fallen out", "we've fallen out",
                 "out over money", "out over something",
                 "toilet seat", "toilet", "seat", "chair", "chairs", "table", "desk", "gate",
                 "door", "hinge", "shelf", "shelves", "bolt", "screw", "screws",
                 "washing machine", "washer", "fridge", "freezer", "wheel", "wheels",
                 "floorboard", "floorboards", "handrail", "railing", "stair gate", "tap",
                 "radiator", "trolley", "pram",
                 "playlist", "playlists", "music", "songs", "song", "spotify", "album", "shuffle "
                 "play", "on shuffle", "cards", "deck of cards", "shuffle the",
                 "fence", "fences", "fencing", "fence post", "fence posts", "gate post",
                 "gatepost", "gravel board",
                 "falling for", "fall for", "fell for", "fall in love", "falling in love",
                 "fell in love", "tripping myself up", "trips myself up", "tripped myself up",
                 "pack", "packing", "packed", "suitcase", "suitcases", "luggage",
                 "hand luggage", "rucksack", "backpack", "kit list", "packing list",
                 "survive a", "coach trip", "coach journey", "train journey", "long journey",
                 "long trip", "long drive", "long flight",
                 "guilt tripping", "guilt trip", "guilt trips", "guilt tripped",
                 "guilt-tripping", "guilt-trip", "tripping me", "trips me", "tripping him",
                 "tripping her", "trip out", "trip abroad",
                 "road trip", "road trips", "roadtrip", "plan a trip", "planning a trip",
                 "plan the trip", "itinerary", "driving holiday", "long drive",
                 "snow", "leaves", "hair", "temperature", "standards", "short", "through",
                 "ladder", "roof", "scaffold",
                 "dog", "dogs", "puppy", "pup", "cat", "cats", "kitten", "pet", "pets",
                 "toddler", "baby", "child", "children", "kid", "kids", "son", "daughter",
                 "nursery", "boy", "girl",
                 "fuse", "fuses", "breaker", "breakers", "plug", "plugs", "socket", "sockets",
                 "rcd", "electric", "electrics", "electricity", "wiring", "power", "lights",
                 "light", "consumer unit", "trip switch", "switch", "appliance", "appliances",
                 "circuit", "circuits", "mcb", "rcbo", "fuse box", "distribution board",
                 "plan a trip", "planning a trip", "planned a trip", "plan my trip",
                 "plan the trip", "plan our trip", "plan a holiday", "trip plan", "trip plans",
                 "itinerary", "trip to", "trip with", "trip for", "city break", "days away",
                 "week away", "travel plan", "holiday plan", "organise a trip", "organize a trip",
                 "sort out a trip",
                 "holiday", "holidays", "abroad", "flight", "flights", "booking", "booked",
                 "save", "saves", "saving", "savings", "saved", "money", "budget", "fund",
                 "plan a trip", "a trip", "trip to", "the trip", "our trip", "vacation",
                 "hotel", "hotels", "itinerary", "travel", "city break", "going away",
                 "book a trip", "passport", "airport", "packing", "planning a trip",
                 "plan my trip")),
    entry("bones", (("bones", "bone"), ("how many", "count", "number")),
          "An adult has 206 bones; a baby is born with roughly 270, and many of those fuse together "
          "as you grow. The smallest are three tiny ones in each middle ear.",
          avoid=("dog", "cat", "puppy", "kitten", "pet", "chew", "chewed", "eat", "ate",
                 "horse", "horses", "cow", "cows", "sheep", "pig", "pigs", "rabbit",
                 "rabbits", "bird", "birds", "fish", "paw", "paws", "beak", "beaks",
                 "tail", "tails", "animal", "animals"),
          ask=("how", "many", "count", "number")),
    entry("body-record", (_the_body_record_key(), _RECORD_ASK),
          _what_the_body_is_like,
          avoid=("dog", "cat", "puppy", "kitten", "pet", "chew", "chewed", "toothache",
                 "tooth hurts", "my tooth", "dentist", "filling", "braces", "brace",
                 "broken bone", "break a bone", "broke my", "fracture", "sprain",
                 "muscle ache", "sore muscles", "strain", "cramp", "cut my finger",
                 "numb", "numbness", "tingling", "nail",
                 "cook", "cooking", "cooked", "bake", "baking", "roast", "recipe", "recipes",
                 "dinner", "supper", "meal", "meals", "menu")),
    entry("heart-rate", (("heart", "heartbeat", "pulse"),
                        ("fast", "faster", "beat", "beats", "run", "running", "exercise",
                         "racing")),
          "Working muscles need more oxygen, so your heart beats faster and harder to move blood "
          "round; a fit heart pumps more with each beat, which is why fit people have slower "
          "resting rates. Anywhere from 60 to 100 beats a minute at rest is normal for adults.",
          ask=("why", "does", "when", "do")),
    entry("immune-system", (("immune system", "immunity", "immune"),
                           ("fight", "fights", "work", "works", "body", "infection", "germs")),
          "Your body fights infection in layers: skin and mucus keep germs out, white blood cells "
          "attack whatever gets through, and antibodies tag specific germs for destruction. "
          "Memory cells remember each germ, which is why you rarely catch the same one twice and "
          "why vaccines work.",
          ask=("how", "what", "why", "does")),

    entry("predict-earthquakes", (("predict", "prediction", "forecast"), ("earthquake",
                                                                          "earthquakes", "quake")),
          "Nobody can say when a particular earthquake will hit: the rock gives way suddenly and "
          "the signs beforehand are unreliable. What we can do is forecast where and how strongly "
          "the ground is likely to shake, which is why buildings in earthquake zones are built to "
          "flex.",
          ask=("can", "could", "how", "why", "do", "we")),
    entry("ice-melt", (("ice", "ices"), ("melt", "melts", "melting", "melted")),
          lambda memory, understood: _how_long_ice_takes(understood)),
    entry("cramp", (("cramp", "cramps", "cramping", "charley horse"),
                    ("leg", "legs", "foot", "feet", "calf", "calves", "toe", "toes", "night",
                     "muscle", "muscles", "why", "cause", "causes", "happen", "happens",
                     "stop", "help", "holds", "get rid", "clear up", "cure", "fix",
                     "getting", "got", "keep", "keeps", "kept", "always", "often", "most days",
                     "every day", "have", "had")),
          "A cramp is a muscle contracting hard and not relaxing, which hurts sharply for a minute "
          "or so. Stretch it gently, pull your toes up toward you for a calf cramp, and drink "
          "water; cramps at night often come with tired muscles, dehydration or low magnesium. "
          "Before exercise, warm up and add distance slowly, and see a GP if a cramp comes on "
          "every time you walk a set distance, or comes with a calf that is swollen and hot.",
          avoid=("stomach", "stomachs", "tummy", "abdomen", "belly", "period", "periods",
                 "menstrual", "ibs", "diarrhoea", "diarrhea",
                 "child", "children", "kid", "kids", "daughter", "son", "baby", "toddler",
                 "toddlers", "boy", "girl"),
          ask=("why", "get", "gets", "getting", "got", "at", "what", "how", "stop", "help",
               "cure", "keep", "keeps", "kept", "always", "often", "have", "had")),
    entry("allergy-why", (("allergy", "allergies", "allergic", "hay fever", "hayfever"),
                          ("why", "cause", "causes", "happen", "happens", "what", "get",
                           "getting", "develop")),
          "An allergy is the immune system mistaking something harmless - pollen, pet dander, "
          "dust, a food - for a threat and releasing histamine, which causes the sneezing, itchy "
          "eyes or rash. Hay fever is that reaction to pollen; antihistamines block the histamine, "
          "and a pharmacist can advise on the best one for you.",
          avoid=("throat", "breathing", "wheeze", "wheezing", "swollen", "swelling", "epipen",
                 "anaphylaxis", "hospital", "take", "tablet", "tablets", "medicine",
                 "antihistamine", "relief", "am", "was", "im", "i'm", "remind", "remember",
                 "said", "say", "told", "again", "anything", "did", "help", "helps", "relieve",
                 "treat", "treatment", "stop", "prevent", "manage", "best",
                 "what can i do", "what should i do", "what can we do", "how do i",
                 "how can i", "is there anything", "anything i can do")),
    entry("runny-nose-why", (("runny nose", "nose runs", "nose is running", "blocked nose",
                              "stuffy nose", "snot", "mucus"),
                             ("why", "cause", "causes", "happen", "happens", "what", "get", "keep")),
          "A runny nose is mostly your body flushing out irritants: the lining makes extra mucus "
          "to trap pollen, dust or a virus and wash it away, and it can keep running for a while "
          "after the trigger is gone. Clear, watery stuff is usually allergy or cold; thick green "
          "mucus is not automatically an infection, but a fever or one-sided pain should be checked.",
          avoid=("blood", "bleeding", "nosebleed", "baby", "babies", "child", "children", "kid",
                 "kids", "take", "medicine", "spray", "decongestant", "stop", "treat", "cure",
                 "am", "was", "im", "i'm", "said", "say", "told", "remind", "remember", "again",
                 "help", "helps", "relieve", "relief", "prevent", "manage", "best")),
    entry("fever-why", (("fever", "feverish", "high temperature"),
                        ("why", "cause", "causes", "happen", "happens", "what", "get")),
          "A fever is the immune system turning up the body's thermostat to make it harder for "
          "germs to multiply, so it is a response rather than the illness itself. It is common with "
          "infections and usually settles in a few days; in a baby under three months, or with a "
          "stiff neck, confusion, a rash that does not fade or trouble breathing, get medical help "
          "urgently.",
          avoid=("baby", "babies", "infant", "child", "children", "kid", "kids", "paracetamol",
                 "ibuprofen", "medicine", "take", "reduce", "bring", "lower", "how to", "have",
                 "has", "got", "do i", "should i", "what can i", "what should i", "help",
                 "helps", "relieve", "relief", "treat", "treatment", "cure", "stop", "prevent",
                 "manage", "best")),
    entry("craving-why", (("craving", "cravings", "crave", "craving sugar", "craving sweets",
                           "sugar", "sweets", "sweet", "sweet things", "chocolate", "carbs",
                           "crisps", "biscuits", "cake", "salt", "salty", "junk food", "bread",
                           "pasta", "cheese"),
                          ("why", "cause", "causes", "happen", "happens", "what", "get", "always",
                           "suddenly", "mean")),
          "Cravings are usually the brain asking for quick energy or a habit cue rather than a "
          "nutrient shortage: sugar and salty fat hit the reward system fast, and seeing or "
          "smelling food can set one off. Eat a proper meal with protein and fibre first, then wait "
          "ten minutes; if you are craving non-food things, get that checked.",
          avoid=("pregnant", "pregnancy", "baby", "child", "kid", "ice", "dirt", "cigarette",
                 "smoke", "alcohol", "drink", "drug", "drugs", "was", "im", "i'm", "said",
                 "say", "told", "remind", "remember", "again", "did", "help", "helps", "relieve",
                 "relief", "treat", "treatment", "cure", "stop", "prevent", "manage", "best",
                 "oven", "recipe", "recipes", "icing",
                 "decorate", "how long in the oven", "what should i bake", "what to bake"),
          ask=("want", "wants", "wanting", "crave", "craves", "craving", "cravings", "fancy",
               "feel like"),
          bias=1),
    entry("acne-why", (("acne", "pimples", "spots", "breakouts", "zits"),
                       ("why", "cause", "causes", "happen", "happens", "what", "get", "getting",
                        "adult", "teenage", "teenager", "teenagers", "teen", "teens",
                        "teenaged", "hormonal",
                        "get rid", "rid of", "clear", "clearing", "treat", "treatment", "cure",
                        "stop", "prevent", "best", "help", "helps", "relieve", "relief",
                        "manage")),
          "Acne happens when hair follicles get blocked by oil and dead skin, and skin bacteria "
          "multiply in the blocked pore; hormones make the oil glands busier, which is why it peaks "
          "in the teens. Wash gently twice a day, do not pick, and a pharmacy treatment with benzoyl "
          "peroxide or salicylic acid is a reasonable first try; painful cysts or scarring deserve "
          "a GP.",
          avoid=("shirt", "shirts", "clothes", "clothing", "fabric", "stain", "stains",
                 "detergent", "laundry", "wash", "washing", "rash", "chickenpox", "measles",
                 "mole", "cancer", "bleeding", "am", "was", "said", "say", "told",
                 "remind", "remember", "again", "did",
                 "car", "cars", "windscreen", "wall", "walls", "floor", "floors", "carpet",
                 "carpets", "sofa", "duvet", "mattress", "paint", "leaf", "leaves", "plant",
                 "plants", "garden", "grease", "oil", "mud", "sink", "mirror",
                 "sunbed", "sunbeds", "sun", "tan", "tanning", "solarium",
                 "moisturiser", "moisturizer", "sunscreen", "spf", "lotion", "serum",
                 "cleanser", "cleansers", "product", "products", "brand")),
    entry("sweat", (("sweat", "sweating", "sweaty"), ("nervous", "stress", "why", "smell",
                                                      "body")),
          "Nervous sweat comes from glands that open up under stress hormones, and it is the "
          "bacteria on your skin breaking that sweat down that makes it smell. Ordinary "
          "antiperspirant works better than deodorant for the smell and dampness, because it "
          "reduces the sweat itself.",
          avoid=("night", "nights", "overnight", "asleep", "sleep", "sleeping", "bed",
                 "pillow", "pillows", "sheets", "wake", "waking", "woke", "drenched",
                 "soaked",
                 "trainers", "trainer", "sneakers", "shoes", "shoe", "boots", "socks",
                 "sock", "insoles", "insole", "footwear", "plimsolls")),
    entry("night-sweats",
          (("sweat", "sweats", "sweating", "sweaty", "drenched", "soaked"),
           ("night", "nights", "overnight", "asleep", "sleep", "sleeping", "bed", "pillow",
            "pillows", "sheets", "wake", "waking", "woke", "doctor", "gp", "worried",
            "weeks", "months", "see a doctor", "see the doctor", "see my doctor",
            "should i worry")),
          "Most night sweats are a hot room, a thick duvet or a fever, so check those first: a "
          "cooler room and a lighter duvet settle it often enough. If you wake drenched for weeks "
          "with no explanation, or with weight loss, a cough or swollen glands, see a GP, because "
          "night sweats are worth checking for an infection, a thyroid problem and, rarely, "
          "lymphoma.",
          avoid=("baby", "babies", "child", "children", "kid", "kids", "boy", "girl",
                 "daughter", "son", "toddler", "newborn", "teething", "fever", "flu",
                 "covid", "interview", "speech",
                 "presentation", "exam", "gym", "run", "running", "exercise", "workout",
                 "beans", "bean", "lentils", "lentil", "chickpeas", "chickpea", "rice",
                 "oats", "porridge", "pasta", "noodles", "chicken", "stock", "sauce",
                 "cashews", "cashew", "almonds", "almond", "walnuts", "walnut", "peanuts",
                 "peanut", "raisins", "raisin", "sultanas", "sultana", "dried fruit",
                 "apricots", "prunes", "dates", "barley", "bulgur", "couscous", "quinoa",
                 "millet", "buckwheat", "haricot", "cannellini", "soya", "soy", "adzuki",
                 "split peas", "black beans", "kidney bean",
                 "washing", "laundry", "clothes", "shirt", "shirts", "towel", "towels",
                 "dishes", "dishcloth", "sink", "bucket", "stain", "stains", "stained"),
          ask=("night", "nights", "overnight", "asleep", "sleep", "sleeping", "bed", "pillow",
               "pillows", "sheets", "wake", "waking", "woke"),
          bias=2),
    entry("cry", (("cry", "crying", "tears", "tearful"), ("sad", "why", "happy", "emotion",
                                                          "upset")),
          "Crying is a pressure valve: strong feeling sets off the same nerves that make your "
          "breath catch, and the tears are part of that response rather than a sign of weakness. "
          "Emotional tears carry stress hormones, and most people feel calmer afterwards.",
          avoid=("dog", "dogs", "puppy", "pup", "cat", "cats", "kitten", "pet", "pets", "bird",
                 "parrot", "rabbit", "horse", "baby", "babies", "newborn", "new born", "infant",
                 "teething", "nappy", "feeding", "breastfeeding", "formula")),
    entry("blink", (("blink", "blinking", "blinks"), ("why", "eye", "eyes", "often", "do")),
          "You blink about 15 to 20 times a minute to keep the eye wet and to clear dust, and a "
          "blink also gives your brain a tiny rest from the visual stream. Screening and driving "
          "make people blink less, which is why eyes get sore and gritty after a long session."),
    entry("wrinkles", (("wrinkle", "wrinkles", "wrinkled", "wrinkly", "wrinklies",
                        "ageing skin", "aging skin", "thin skin", "skin thin", "skin thinner",
                        "skin gets thin", "skin so thin"),
                       ("why", "get", "skin", "face", "age", "stop", "prevent", "avoid",
                        "reduce", "how")),
          "Skin gets thin and creases as the collagen and elastin that keep it springy thin out "
          "with age and sun damage; smoking and too much sun make it happen much sooner. "
          "Sunscreen every day is "
          "the one thing that reliably slows it, and moisturiser plumps out the fine lines a "
          "little.",
          avoid=("bath", "baths", "water", "swim", "swimming", "pool", "washing up", "dishes",
                 "pruney", "prune", "shrivel", "shriveled", "shrivelled",
                 "cactus", "cacti", "succulent", "plant", "plants", "leaf", "leaves",
                 "leather",
                 "flower", "flowers", "tomato", "tomatoes",
                 "shirt", "shirts", "clothes", "clothing", "trouser", "trousers", "fabric",
                 "iron", "ironing", "laundry", "cotton", "linen", "dryer", "sheet", "sheets",
                 "dehydrated", "dehydration", "ill", "illness", "unwell", "sick"),
          ask=("skin", "face", "wrinkle", "wrinkles", "wrinkled", "wrinkly", "wrinklies",
               "ageing skin", "aging skin"),
          bias=1),
    entry("sleep-why", (("sleep", "sleeping", "asleep"),
                       ("why", "what", "happen", "happens", "need", "needed", "important",
                        "purpose", "body", "brain")),
          "Sleep is when the brain files the day's memories and clears waste, and the body repairs "
          "muscle and releases growth hormone. Most adults need seven to nine hours; if you are "
          "short for weeks, mood, concentration and immunity suffer before you feel sleepy.",
          ask=("we", "people", "humans", "purpose", "need sleep", "sleep needed",
               "sleep important", "sleep for", "what does sleep do"),
          avoid=("can't", "cant", "cannot", "trouble", "insomnia", "awake", "fall asleep",
                 "stay asleep", "too much", "so much", "how much", "hours", "baby", "babies",
                 "newborn", "toddler", "kid", "kids", "child", "children", "puppy", "puppies",
                 "cat", "dog", "wont sleep", "won't sleep", "weeks old", "months old")),
    entry("sleep-too-much",
          (("sleep too much", "sleeping too much", "slept too much", "sleep so much",
            "sleeping so much", "oversleep", "oversleeping", "too much sleep", "sleep 10 hours",
            "sleep 12 hours", "sleeping 10 hours", "sleeping all day", "slept all day",
            "slept 10 hours", "slept 12 hours", "slept 9 hours", "sleep 9 hours", "10 hours",
            "11 hours", "12 hours", "ten hours", "eleven hours", "twelve hours",
            "slept in till", "cant wake up properly", "always sleepy", "sleepy all day"),
           ("why", "bad", "normal", "worry", "worried", "still tired", "still knackered",
            "keep", "every day", "always", "lately", "weeks", "months", "problem", "wrong",
            "night", "nights", "too much",
            "should", "what")),
          "Long sleeps now and then are just a debt being paid, especially after a run of short "
          "nights. Needing nine or ten hours most nights and still waking flat is worth a GP "
          "visit: an underactive thyroid, low iron, low vitamin D, depression and sleep apnoea "
          "all show up that way, and each is easy to test for. Keep the wake-up time the same "
          "every day while you wait, because long lie-ins at the weekend hide the pattern.",
          avoid=("my baby", "baby", "newborn", "toddler", "my son", "my daughter", "kids",
                 "month old", "months old", "week old", "weeks old", "year old", "years old",
                 "puppy", "cat", "dog", "insomnia", "cant sleep", "can't sleep", "cant get to "
                 "sleep", "shift work", "jet lag", "time zone", "hangover", "teenager",
                 "in a day", "a day have", "hibernate", "pregnant")),
    entry("baby-sleep",
          (("baby", "babies", "newborn", "new born", "infant", "week old", "weeks old",
            "month old", "months old", "6 week", "six week", "8 week", "eight week",
            "12 week", "twelve week",
            "toddler", "toddlers", "2 year old", "two year old", "3 year old",
            "three year old"),
           ("sleep", "sleeping", "sleeps", "slept", "sleepy", "drowsy",
            "sleeping a lot", "sleeps a lot", "sleeping all the time", "sleeps all the time",
            "sleeping all day", "sleeps all day", "sleeping too much", "sleeps too much",
            "more than usual", "normal", "hard to wake", "wont wake", "won't wake",
            "hours", "hour", "too much", "how much")),
          _a_baby_sleep_reply,
          avoid=("wont sleep", "won't sleep", "not sleeping", "cant sleep", "can't sleep",
                 "isnt sleeping", "isn't sleeping", "not sleeping well", "never sleeps",
                 "will not sleep", "wont settle", "won't settle",
                 "get my baby to sleep", "get a baby to sleep", "get them to sleep",
                 "help my baby sleep", "help them sleep", "goes to sleep",
                 "sleeping through", "sleeps through", "sleep through", "through the night",
                 "wakes", "woke", "waking up", "up every", "every hour", "every two hours",
                 "at night", "all night", "night feeds", "night feeding", "up all night",
                 "colic", "reflux", "teething", "fever", "temperature", "rash", "cough",
                 "cold", "not feeding", "wont feed", "won't feed", "weaning", "milk",
                 "routine", "cot", "sids", "cot death", "swaddle", "cry", "crying",
                 "pale", "floppy", "limp", "blue", "grey", "unresponsive", "not responding",
                 "cant wake", "can't wake", "cannot wake", "not waking", "isnt waking",
                 "isn't waking", "wont wake", "won't wake", "wont wake up", "won't wake up",
                 "struggling to breathe", "breathing", "not breathing", "seizure", "fit",
                 "very sleepy", "too sleepy", "sleepy and")),

    entry("sleep-hours",
          (("sleep", "sleeping", "slept", "hours sleep", "hours of sleep", "sleep a night",
            "hours a night", "hours at night", "hours per night", "hours in bed",
            "hours of kip", "hours kip",
            "teenager", "teenagers", "teen", "teens", "teenage", "over 65", "pensioner"),
           ("enough", "how much", "how many", "need", "needed", "short", "hours", "five", "six",
            "how long", "long should i", "long do i",
            "seven", "eight", "5", "6", "7", "8", "only", "less than", "plenty", "normal",
            "healthy", "recommended")),
          _sleep_hours,
          avoid=("my baby", "baby", "newborn", "toddler", "my son", "my daughter", "my child",
                 "week old", "weeks old", "month old", "months old", "6 week", "six week",
                 "kids", "puppy", "shift work", "jet lag", "time zone", "insomnia", "cant sleep",
                 "month old", "months old", "month-old", "months-old", "weeks old", "week old",
                 "can't sleep", "cannot sleep", "cant get to sleep", "wake up", "waking", "woke",
                 "snoring", "apnoea", "sleep apnoea", "in a day", "a day have", "pregnant",
                 "sleeping tablet", "melatonin", "how long to sleep", "hibernate",
                 "nap", "naps", "napping", "nap for",
                 "calcium", "iron", "vitamin", "vitamins", "protein", "fibre", "fiber",
                 "calories", "calorie", "potassium", "magnesium", "zinc", "b12", "folate",
                 "water", "milk", "steps", "exercise",
                 "ill", "unwell", "sick", "illness", "flu", "fever", "cold", "covid",
                 "concussion", "sore throat", "chest infection", "hospital", "recovering",

                 "sleeps until", "sleeps till", "sleeps to go", "sleeps left",
                 "sleeps is it", "sleeps before", "hours is it till", "hours until",
                 "hours till",
                 "birthday", "christmas",
                 "tired", "tiredness", "exhausted", "knackered", "fatigued")),
    entry("snoring", (("snore", "snores", "snoring", "snored", "snorer"),
                      ("stop", "how", "why", "help", "prevent", "reduce", "less", "loud", "loudly",
                       "partner", "wife", "husband", "boyfriend", "girlfriend", "wake",
                       "wakes", "tips", "advice", "keep",
                       "normal", "common", "usual", "ok", "bad", "worried", "worry",
                       "serious", "problem", "matter", "matters", "harm", "harmful")),
          "Most snoring is air whistling through a narrowed throat, so start with what widens it: "
          "sleep on your side, keep the last drink to three hours before bed, clear a blocked nose "
          "with a saline rinse or a strip, and lose a bit of weight if you have some to lose. If "
          "your partner hears you stop breathing or gasp, or you are tired all day, ask the GP "
          "about sleep apnoea - that one needs treating and a nose strip will not do it.",
          ask=("how", "stop", "what", "any", "help", "tips", "advice", "reduce", "prevent",
               "should", "is there", "why", "normal", "common", "usual", "ok", "bad",
               "worried", "worry", "serious", "problem", "matter", "matters", "harm",
               "harmful"),
          avoid=("dog", "dogs", "puppy", "cat", "cats", "kitten", "baby", "babies", "newborn",
                 "toddler", "child", "children", "kid", "kids", "teeth", "grind", "grinding",
                 "apnoea", "cpap", "machine", "sleep talk", "talk in my sleep",
                 "paralysis", "nap", "dream", "dreams", "cot", "crib")),
    entry("sleep-talking",
          (("sleep talking", "sleep talk", "sleeptalking", "talk in my sleep",
            "talking in my sleep", "talks in his sleep", "talks in her sleep",
            "talks in their sleep", "talk while asleep", "talking while asleep",
            "mumble in my sleep", "mumbling in my sleep", "shout in my sleep"),
           ("normal", "common", "why", "stop", "how", "harm", "harmful", "bad", "worry",
            "worried", "serious", "mean", "does it", "should", "is it")),
          "Sleep talking is common and almost always harmless: it happens in light sleep, it "
          "runs in families, and most people never know they do it. Nothing needs treating - "
          "keep the last drink early, cut late caffeine and get enough sleep, because it gets "
          "worse when someone is overtired or feverish. Ask the GP about it if the talking "
          "comes with acting out dreams or violent movement, since that pairing is worth "
          "checking for a sleep disorder.",
          report=True,
          avoid=("baby", "babies", "newborn", "toddler", "my son", "my daughter", "my child",
                 "snore", "snoring", "snorer", "apnoea", "cpap")),

    entry("nap-afternoon",
          (("nap", "naps", "napping", "napped", "siesta", "forty winks"),
           ("afternoon", "good idea", "bad idea", "how long", "worth", "daytime", "lunchtime",
            "every day", "after lunch", "too long", "20 minutes", "help", "good for you",
            "bad for you", "take a nap", "benefit", "point",
            "properly", "proper", "best way", "right way")),
          "A short nap is worth having: 20 minutes, ideally before about 3pm, and set an alarm, "
          "because 90 minutes leaves you groggier than when you lay down. It helps most if you "
          "lost sleep the night before or you are driving later. Skip it if you already lie awake "
          "at night, and if you need one every afternoon for weeks, that is worth a word with the "
          "GP, especially with low mood, thirst or weight loss.",
          avoid=("baby", "babies", "newborn", "toddler", "my son", "my daughter", "my child",
                 "kids", "puppy", "night shift", "jet lag", "can't sleep", "cant sleep",
                 "1 year old", "one year old", "2 year old", "two year old", "3 year old",
                 "three year old", "4 year old", "four year old", "5 year old",
                 "five year old", "months old", "18 months", "15 months", "6 months old")),

    entry("sleep-onset",
          (("get to sleep", "fall asleep", "go to sleep", "nod off", "drop off", "drift off",
            "getting to sleep", "falling asleep"),
           ("fast", "faster", "quick", "quicker", "quickly", "sooner", "short", "shorter",
            "easier", "easy", "long", "longer", "ages", "hour", "hours", "cant", "can't",
            "cannot", "struggle", "takes", "hard", "help", "how", "tips", "advice", "what")),
          "Give yourself a run-up rather than trying to switch off: the same wake-up time every "
          "day, no caffeine after about two, the last hour dim with the phone out of reach, and a "
          "cool dark room. Falling asleep is a slope you slide down, so nothing you try harder at "
          "helps: if you are still awake after about twenty minutes, get up, sit somewhere dim "
          "with something dull, and go back when your eyes are heavy. Counting minutes on the "
          "clock is what keeps it going.",
          ask=("how", "what", "any", "anything", "help", "tips", "advice", "why", "should",
               "best", "faster", "quicker", "quickly", "cant", "can't", "want", "struggle",
               "takes", "need"),
          avoid=("overthinking", "overthink", "racing", "thoughts", "mind", "switch off",
                 "year old", "years old", "bedtime", "bed time", "put him to bed",
                 "put her to bed", "put them to bed", "school night", "school nights",
                 "worry", "worried", "worrying", "anxious", "anxiety", "stress", "stressed",
                 "baby", "babies", "newborn", "toddler", "kids", "child", "children",
                 "my son", "my daughter", "puppy", "cat", "dog", "snoring", "apnoea",
                 "apnea", "melatonin", "sleeping tablet", "sleeping tablets", "pregnant",
                 "shift work", "night shift", "jet lag", "time zone", "hangover", "died",
                 "funeral", "depressed", "suicidal", "out of bed", "red light", "phone",
                 "sleep better", "sleeping better", "sleep well", "sleeping well", "good night",
                 "wind down", "sleep routine", "bedtime routine", "sleep hygiene", "sleep tips",
                 "tips for sleeping", "fall asleep faster", "fall asleep quicker",
                 "get to sleep faster", "help me fall asleep", "help me get to sleep")),
    entry("wake-at-night",
          (("wake up at", "waking up at", "wake at", "waking at", "woke up at", "woke at",
            "up at", "im up at", "i'm up at", "up every night", "up at night",
            "wake up in the night", "wake in the night", "waking in the night",
            "wake up in the middle of the night", "middle of the night", "wake up several times",
            "waking up several times", "wake up every night", "waking up every night",
            "cant get back to sleep", "can't get back to sleep", "cant get back off to sleep",
            "get back to sleep", "get back off to sleep", "back to sleep",
            "get to sleep and stay asleep"),
           ("2", "3", "4", "5", "2am", "3am", "4am", "5am", "night", "nights",
            "why", "how", "stop", "always", "every", "again", "back to sleep", "repeat")),
          _night_waking,
          ask=("how", "why", "what", "should", "stop", "help", "any", "wake", "waking",
               "cant", "can't", "keep",
               "up", "im", "i'm", "every night", "night", "nights", "every"),
          avoid=("baby", "babies", "newborn", "toddler", "kids", "child", "children",
                 "year old", "years old", "bedtime", "bed time", "school night", "school nights",
                 "my son", "my daughter", "puppy", "cat", "dog", "snoring", "snore", "apnoea",
                 "apnea", "toilet", "pee", "wee", "bathroom", "thirsty", "pregnant",
                 "shift work", "night shift", "insomnia for years", "out of bed", "depressed",
                 "suicidal", "melatonin", "sleeping tablet", "sleeping tablets", "dying", "died",
                 "too early", "up early", "wakes me early", "5am", "5 am", "5:30", "6am", "6 am",
                 "early riser", "wide awake at 5", "wake up early", "waking up early")),
    entry("body-clock",
          (("sleep pattern", "sleep routine", "sleep schedule", "body clock", "circadian",
            "reset my sleep", "fix my sleep", "sort my sleep", "my sleep is", "sleeping pattern",
            "falling asleep late", "stay up too late", "staying up too late", "go to bed too late",
            "going to bed too late", "sleeping in late", "lie in at the weekend",
            "sleep in at the weekend", "night owl", "sleep in the day", "sleeping in the day",
            "sleep is all over the place", "sleep is a mess", "sleep is messed up",
            "sleep is shot", "my sleep is", "body clock is", "naps in the day", "get up earlier",
            "wake up earlier", "go to bed earlier", "sleep earlier", "wake earlier",
            ),
           ("fix", "reset", "change", "sort", "better", "earlier", "later", "how", "what",
            "tips", "advice", "wrong", "messed", "mess", "routine", "pattern", "should",
            "help", "late", "always", "kids", "shot", "place")),
          "Anchor the wake-up time first and let the bedtime follow: get up at the same time every "
          "day, weekend included, and get outside into daylight within an hour of it, because "
          "morning light is what sets the clock. Then move bedtime fifteen minutes at a time, a "
          "couple of nights each, rather than an hour overnight. Keep naps under twenty minutes "
          "and early in the afternoon, skip caffeine after lunch while you shift it, and give it a "
          "week before it stops feeling like effort.",
          ask=("how", "what", "any", "help", "tips", "advice", "should", "fix", "reset",
               "change", "sort", "better", "messed", "mess", "wrong", "late", "shot",
               "all over", "out of whack"),
          avoid=("baby", "babies", "newborn", "toddler", "kids", "child", "children",
                 "year old", "years old", "bedtime", "bed time", "school night", "school nights",
                 "my son", "my daughter", "teenager", "puppy", "cat", "dog", "shift work",
                 "night shift", "jet lag", "time zone", "time difference", "melatonin",
                 "pregnant", "snoring", "apnoea", "apnea", "insomnia for years", "depressed",
                 "suicidal", "out of bed", "dying", "died", "funeral")),
    entry("headache-why", (("headache", "headaches", "migraine", "migraines", "head hurts",
                            "head is pounding", "sore head"),
                           ("why", "cause", "causes", "happen", "happens", "what", "every day",
                            "often", "always", "behind", "one side", "sudden", "bad")),
          "Most headaches are tension: muscles in the neck, jaw and scalp tighten with stress, "
          "screens, skipped meals or poor sleep, and the pain sits like a band round the head. "
          "Migraine is different: throbbing, often on one side, with nausea or light sensitivity, "
          "and regular or sudden worst-ever headaches should be checked by a doctor.",
          avoid=("take", "medicine", "medication", "paracetamol", "ibuprofen", "painkiller",
                 "painkillers", "relief", "help", "cure", "rid", "stop", "tablet", "tablets",
                 "my", "these", "behind", "desk", "at work", "should i", "worried")),
    entry("bald", (("bald", "balding", "baldness"),
                   ("men", "man", "why", "happen", "genetic", "male")),
          "Male pattern baldness is mostly inherited: hair follicles on top of the head become "
          "sensitive to testosterone by-products and shrink, so hairs get thinner and eventually "
          "stop. It is not caused by hats, washing or stress alone, and treatments only work while "
          "you keep using them.",
          avoid=("women", "woman")),
    entry("hair-loss", (("hair fall out", "hair falling out", "hair falls out", "hair is falling out", "losing my hair",
                         "losing hair", "thinning hair", "thinning", "shedding hair", "shedding",
                         "hair loss", "hair coming out", "hair is coming out", "hair come out",
                         "hair comes out"),
                        ("why", "happen", "cause", "normal", "much", "stop", "prevent", "my",
                         "women", "woman")),
          "Hair loss is usually a pattern that runs in families: follicles on top of the head "
          "shrink under testosterone by-products, so hairs get thinner and eventually stop. "
          "Sudden or patchy shedding is more often stress, illness, childbirth, iron or thyroid "
          "trouble, so see a GP if it is fast or patchy; minoxidil helps pattern loss but only "
          "while you keep using it.",
          avoid=("men", "man", "male", "dog", "dogs", "cat", "cats", "pet", "pets", "puppy",
                 "kitten", "rabbit", "grey", "gray", "white", "colour", "color",
                 "chemo", "chemotherapy", "radiotherapy", "cancer",
                 "paint", "varnish", "sauce", "gravy", "soup",
                 "snake", "snakes", "lizard", "lizards", "reptile", "reptiles", "bird", "birds"),
          ask=("hair",)),
    entry("fish-sleep", (("fish", "fishes"), ("sleep", "sleeping", "rest", "night", "asleep")),
          "Fish rest but do not sleep the way we do: most have no eyelids, so they hover still in "
          "a sheltered spot, often at night, with their gills still moving. Some, like sharks, "
          "keep swimming the whole time so water keeps flowing over their gills."),
    entry("greenhouse-effect", (("greenhouse effect", "greenhouse gas", "greenhouse gases"),
                                ("what", "work", "works", "how", "why", "trap", "explain",
                                 "cause", "causes", "is")),
          "Gases in the air, mainly carbon dioxide and water vapour, let sunlight in but absorb "
          "the heat that bounces back off the ground, much like glass in a greenhouse. That keeps the "
          "Earth about 33C warmer than it would be. Burning coal, oil and gas adds more of those "
          "gases, so more heat is trapped and the planet warms."),
    entry("ozone-layer", (("ozone layer", "ozone"), ("what", "why", "hole", "protect",
                                                       "damage", "harm", "do")),
          "The ozone layer is a thin band of ozone high in the atmosphere that absorbs most of the "
          "Sun's ultraviolet light, which would otherwise burn skin and damage crops. CFCs thinned "
          "it; they were banned and it is slowly healing."),
    entry("acid-rain", (("acid rain",), ("what", "why", "cause", "causes", "happen", "bad")),
          "Acid rain forms when sulphur dioxide and nitrogen oxides from burning coal and oil mix "
          "with water in the air and fall as weak acid. It harms trees and lakes; filters on power "
          "stations and cleaner fuel have cut it a lot since the 1980s."),
    entry("water-cycle", (("water cycle", "the water cycle", "how does the water cycle",
                           "how the water cycle", "why does the water cycle",
                           "what is the water cycle", "explain the water cycle",
                           "water cycle work", "water cycle works", "water cycle for kids",
                           "water cycle for a child"),
                          ("what", "how", "work", "works", "explain", "cycle", "is", "why",
                           "mean", "means")),
          "Water evaporates from the sea and land, rises and cools into clouds, falls as rain or "
          "snow, and runs back to the sea: the same water goes round and round. Sunlight drives it "
          "and gravity brings it back down.",
          bias=2, avoid=("project", "projects", "poster", "presentation", "assignment",
                         "essay", "coursework", "revision", "exam")),

    entry("sun-size", ("sun", ("big", "large", "size", "wide", "compared", "how")),
          "The Sun is about 1.4 million km across, roughly 109 Earths side by side, and you could "
          "fit about 1.3 million Earths inside it. It looks small only because it is 150 million "
          "km away.", ask=("how big", "how large", "size", "bigger", "compared")),
    entry("earth-size", ("earth", ("big", "large", "size", "wide", "across", "diameter",
                                   "circumference", "weigh", "weighs", "heavy", "mass", "how",
                                   "compared")),
          "The Earth is about 12,742 km across (12,756 km at the equator, 12,714 km from pole to "
          "pole) and 40,008 km round the poles, a little less than the 40,075 km round the "
          "equator because the spin bulges it out. It weighs about 6 billion trillion tonnes."),
    entry("eclipse", (("eclipse", "eclipses"), ("solar", "lunar", "moon", "sun", "what",
                                                  "why", "happen", "explain")),
          "An eclipse happens when the Sun, Earth and Moon line up. In a solar eclipse the Moon "
          "passes between us and the Sun and covers it; in a lunar eclipse the Earth's shadow "
          "falls on the Moon, which turns a dull red."),
    entry("dark-matter", (("dark matter",), ("what", "made", "universe", "space", "unknown")),
          "Dark matter is the name for mass we cannot see but can measure: galaxies spin and bend "
          "light as if they hold far more matter than the stars show. Nobody yet knows what it is "
          "made of, which is why it is one of the big open questions."),
    entry("comet", (("comet", "comets"), ("what", "why", "tail", "made", "shooting", "shoot")),
          "A comet is a lump of ice, dust and rock left over from the birth of the solar system. "
          "Near the Sun its ice turns to gas, and the solar wind blows that gas and dust into a "
          "long tail pointing away from the Sun."),
    entry("mars-travel", ("mars", ("how long", "get", "travel", "reach", "trip", "time",
                                   "journey")),
          "A trip to Mars takes about seven months each way with current rockets, because the "
          "planets are so far apart. Missions wait for a launch window about every 26 months, "
          "when Earth and Mars are lined up best.",
          ask=("how long", "get", "take", "travel", "reach", "trip"),
          bias=4,
          avoid=("year", "years", "day", "days", "sol", "seasons", "length")),
    entry("mars-year", ("mars", ("year", "years", "day", "days", "sol", "seasons", "months")),
          "A year on Mars lasts 687 Earth days, nearly two of ours, because Mars is further from "
          "the Sun and moves more slowly round it. A Martian day is only about 40 minutes longer "
          "than an Earth day."),
    entry("mars-distance", (("mars", "red planet"),
                            ("far", "distance", "away", "miles", "km", "kilometres",
                             "kilometers")),
          "Mars is about 225 million km from Earth on average, but the gap swings from roughly 55 "
          "million to 400 million km as the two planets move round the Sun. That is why a mission "
          "leaves only every 26 months, and why radio messages take between 3 and 22 minutes each "
          "way.",
          ask=("how far", "far", "distance", "away", "miles", "km", "kilometres", "kilometers"),
          bias=3,
          avoid=("travel", "trip", "journey", "get there", "how long does it take", "year",
                 "day", "moon", "rocket", "launch")),
    entry("calorie", (("calorie", "calories", "kcal"), ("what", "mean", "burning", "burned",
                                                           "food", "energy", "need", "eat", "day")),
          "A calorie is a unit of energy; the calories on food labels are really kilocalories, the "
          "energy to raise 1 kg of water by 1C. An average adult needs roughly 2,000 to 2,500 a "
          "day, and eating fewer than you burn is what loses weight."),
    entry("helium-voice", (("helium",), ("voice", "high", "squeaky", "why", "balloon")),
          "Helium does not raise your voice: sound travels about three times faster in it than in "
          "air, which makes the echoes in your throat ring higher. Your vocal cords move exactly "
          "as before, and it wears off in seconds."),
    entry("rust", (("rust", "rusty", "rusting"), ("what", "why", "form", "forms", "metal",
                                                     "iron", "stop")),
          "Rust is iron oxide: iron reacts with oxygen and water in the air and slowly turns into a "
          "flaky orange layer that no longer holds together. Paint, oil or simply keeping the metal "
          "dry keeps water away and stops it."),
    entry("batteries", (("battery", "batteries"), ("work", "works", "how", "store", "stored",
                                                     "charge", "electricity", "why")),
          "A battery turns chemical energy into electricity: a reaction inside pushes electrons "
          "from one terminal to the other, and the circuit carries them round to do work. A "
          "rechargeable one reverses that reaction when you plug it in.",
          avoid=("alarm", "smoke", "recycle", "recycling", "bin", "dispose", "test", "cost",
                 "price", "how much", "replace", "replacement", "phone", "laptop", "car",
                 "drain", "drains", "draining", "overnight",
                 "loses charge", "losing charge", "battery life", "last the day", "flat",
                 "watch", "watches", "wristwatch", "strap", "fob", "keyring", "hearing aid",
                 "thermostat", "thermostats", "boiler", "radiator", "radiators", "heating",
                 "smoke detector", "carbon monoxide",
                 "remote", "remote control", "zapper", "telly", "tv remote", "set-top")),
    entry("microwave-metal",
          (("microwave", "microwaves", "microwave oven"),
           ("metal", "foil", "tinfoil", "tin foil", "aluminium", "aluminum", "fork", "forks",
            "spoon", "spoons", "knife", "cutlery", "spark", "sparks", "sparked", "sparking",
            "gold rim", "gold rims", "takeaway carton", "carton", "crisp packet", "twist tie")),
          "No - metal reflects the microwaves and the tips of it spark, which can scorch the wall or "
          "start a fire, so keep forks, foil, gold-rimmed plates and takeaway cartons with metal "
          "handles out. If it has already sparked, switch it off and unplug it before you touch "
          "anything, and let it cool. A microwave with a burnt patch on the inside wall is worth "
          "replacing rather than carrying on with.",
          ask=("microwave", "microwaves", "microwave oven"),
          avoid=("not heating", "wont heat", "won't heat", "stopped working", "not working",
                 "repair", "fix", "sparked", "sparking", "smoking", "smoke", "flames",
                 "on fire", "caught fire", "burnt", "burning"),
          bias=1),
    entry("microwave", (("microwave", "microwaves"),
                        ("heat", "heats", "heating", "work", "works", "why", "radioactive",
                         "radiation", "dangerous", "safe", "evenly", "uneven", "spin")),
          "A microwave floods food with microwaves, which make water molecules spin and rub against "
          "each other, and that friction heats the food. It does not make the food radioactive, and "
          "it heats unevenly, so stir or leave it to stand.",
          avoid=("spark", "sparks", "sparking", "broken", "not working", "metal", "foil",
                 "tinfoil", "tin foil", "aluminium", "cutlery", "fork", "forks",
                 "not heating", "isnt heating", "isn't heating", "not heating up",
                 "isnt heating up", "isn't heating up", "wont heat", "won't heat",
                 "wont heat up", "won't heat up", "doesnt heat", "doesn't heat",
                 "no heat", "stopped heating", "not getting hot", "not hot", "stays cold",
                 "cold food", "heats nothing", "not warming", "faulty", "repair", "mend",
                 "dead", "died", "stopped working",
                 "reheat", "reheats", "reheating", "reheated", "warm up", "warms up",
                 "warming up", "warmed up", "heat up", "heats up", "heating up", "heated up",
                 "leftover", "leftovers", "left over", "bacteria", "food poisoning",
                 "piping hot", "safe to eat", "is it safe to eat"),
          bias=1),
    entry("sink-float", (("float", "floats", "floating", "sink", "sinks", "sinking"),
                         ("why", "things", "object", "water", "does", "some")),
          "Something floats when it is less dense than the water it pushes aside, and sinks when it "
          "is denser. That is why a steel ship floats: it is mostly air inside, so the whole thing "
          "weighs less than the water it displaces.",
          avoid=("drain", "drains", "draining", "plughole", "plug hole", "blocked", "unblock",
                 "unblocking", "tap", "taps", "pipe", "pipes", "plumber", "going down",
                 "not going down", "waste", "trap", "water down",
                 "smell", "smells", "smelly", "stink", "stinks", "odour", "odor", "clean",
                 "cleaning", "dirty", "grime", "grease", "limescale", "stain", "stains",
                 "bicarbonate", "scrub", "wash up", "washing up",
                 "bread", "loaf", "loaves", "cake", "cakes", "dough", "batter", "pastry",
                 "sponge", "souffle", "baked", "bake", "baking", "oven", "risen", "recipe")),
    entry("salt-ice", (("salt", "salting", "rock salt", "grit", "gritting"),
                       ("ice", "icy", "melt", "melts", "road", "roads", "driveway", "why")),
          "Salt lowers the temperature at which water freezes, so ice on a road melts even when the "
          "air is below 0C. It only works down to about -6C, which is why councils grit before the "
          "coldest nights.",
          avoid=("sea", "ocean", "salt water", "food", "recipe", "cook", "cooking", "eat",
                 "diet", "blood pressure", "bath", "swimming", "softener", "water softener"),
          bias=3),
    entry("friction", (("friction",), ("what", "why", "work", "works", "slow", "heat",
                                        "explain")),
          "Friction is the force between two surfaces that rub together, and it slows movement and "
          "turns the lost energy into heat. It is why brakes get hot and why oil and smooth surfaces "
          "make machines last longer."),

    entry("plant-needs-water",
          (("plant", "plants", "houseplant", "house plant", "pot plant", "pot", "soil", "compost"),
           ("needs water", "need water", "thirsty", "tell if", "how often", "when to water",
            "watering", "water", "dry", "drooping")),
          "Push a finger about 2cm into the soil: water it if the soil is dry at that depth, and "
          "wait a day or two if it is still damp. A pot tells you by weight as well, because a "
          "light pot is a dry pot, and a thirsty plant droops and then perks up within a day of a "
          "drink. Water until it runs out of the drainage holes and empty the saucer, because "
          "roots left standing in water rot.",
          ask=("tell", "know", "how often", "when", "should i", "how do i", "how can i",
               "needs", "need", "thirsty", "dry"),
          avoid=("why", "roots", "stem", "drink", "absorb", "tree", "garden", "lawn", "grass",
                 "basil", "tomato", "potato", "monstera", "orchid", "cactus", "succulent", "fern",
                 "chilli", "lavender", "hydrangea", "slug", "slugs", "pest", "pests", "insect",
                 "insects", "repot", "fertiliser", "fertilizer", "prune", "dead", "died", "dying",
                 "wilt", "wilted", "leaves", "leaf",
                 "feed", "feeds", "feeding", "plant food", "nutrients", "food")),
    entry("plants-drink", (("roots", "root", "plant", "plants", "planting"),
                            ("water", "drink", "absorb", "absorbed", "travels")),
          "Plants take up water through their roots, and it is pulled up narrow tubes in the stem "
          "by evaporation from the leaves. That is why a cut flower wilts and why overwatering "
          "drowns roots that need air.",
          ask=("how", "where", "drink", "absorb", "roots", "up"),
          avoid=WATERING + ("needs water", "need water", "tell", "tell if", "thirsty", "drooping",
                            "cutting", "cuttings", "propagate", "propagating", "root it",
                            "root a cutting"),
          bias=4),
    entry("fireflies", (("firefly", "fireflies", "glow worm", "glowworm"), ("glow", "light",
                                                                              "why", "how", "shine")),
          "Fireflies glow through a chemical reaction in their tail: luciferin reacts with oxygen "
          "and gives off light with almost no heat. They use it to attract mates, and each species "
          "has its own flash pattern."),
    entry("food-chain", (("food chain", "food web"), ("what", "how", "work", "works", "mean")),
          "A food chain is the line of who eats whom, starting with a plant that makes its own food "
          "and ending with a predator. Energy is lost at every step, which is why top predators "
          "are few and a chain rarely has more than four or five links."),
    entry("fossils", (("fossil", "fossils"), ("what", "how", "form", "formed", "made", "become",
                                                "dinosaur")),
          "A fossil forms when a dead animal or plant is buried quickly and its hard parts are "
          "slowly replaced by minerals from the surrounding rock over thousands of years. Most "
          "living things rot away entirely, which is why fossils are rare."),
    entry("spider-web", (("spider", "spiders"), ("web", "webs", "silk", "make", "makes",
                                                  "how")),
          "Spiders spin silk from glands in the abdomen and pull it out with their back legs, "
          "laying a frame first and then a spiral inside it. The silk is stronger than steel for its "
          "weight, and many spiders hunt without a web at all.",
          avoid=("house", "home", "inside", "bath", "bedroom", "get rid",
                 "spider plant", "spider plants", "houseplant", "houseplants", "propagate",
                 "propagating", "cutting", "cuttings", "water it", "repot")),
    entry("duck-float", (("duck", "ducks"), ("float", "floats", "water", "why", "swim")),
          "Ducks float because their bodies are light and their feathers trap air, while a gland "
          "near the tail supplies oil that keeps the water out. Their bones are hollow too, so the "
          "whole bird is far less dense than the water it sits in."),
    entry("crocodile-alligator", (("crocodile", "crocodiles"), ("alligator", "difference",
                                                                "between", "vs")),
          "Crocodiles have narrow, V-shaped snouts and their fourth tooth shows when the mouth is "
          "shut; alligators have broad, U-shaped snouts and it stays hidden. Crocodiles are also the "
          "ones that tolerate salt water."),
    entry("mosquito", (("mosquito", "mosquitoes", "mosquitos", "midge", "midges"),
                       ("why", "bite", "bites", "bitten", "itch", "some", "me", "attract")),
          "Mosquitoes find you by the carbon dioxide you breathe out, your body heat and the "
          "chemicals on your skin, so they are drawn to some people more than others. Covering up "
          "and a repellent with DEET or picaridin are what actually keep them off."),

    entry("tsunami", (("tsunami", "tidal wave", "tidal waves"), ("what", "why", "cause", "causes",
                                                                  "happen", "wave")),
          "A tsunami is a series of waves usually set off by an earthquake under the sea, which "
          "lifts a whole column of water. Out at sea they are barely noticeable, but they steepen "
          "as they reach shallow water; if the sea suddenly pulls back, get to high ground."),
    entry("leap-year", (("leap year", "leap years"), ("why", "what", "when", "have", "366",
                                                       "extra")),
          "A year is about 365.24 days long, so every four years we add 29 February to keep the "
          "calendar in step with the seasons. Century years skip it unless they divide by 400, "
          "which trims the last bit of error."),
    entry("year-length", (("year",),
                          ("365", "why", "how long", "length", "days")),
          "A year is 365 days because that is roughly how long the Earth takes to go round the "
          "Sun once: 365.24 days. The extra quarter day is why we add a leap day every four years, "
          "so the calendar stays in step with the seasons.",
          ask=("365", "why", "how long", "length"),
          avoid=("leap", "new year", "tax year", "school year", "academic year", "birthday",
                 "age", "resolution", "christmas", "month", "months", "12 months")),
    entry("time-zones", (("time zone", "time zones", "time difference", "time differences"),
                         ("why", "what", "exist", "different", "hours")),
          "Time zones exist because the Earth turns: noon is when the Sun is highest, and that "
          "happens at a different moment in each place. The world is split into 24 zones of about "
          "an hour, so the clock roughly matches daylight; some countries bend the borders or use "
          "half-hour zones.",
          ask=("why", "what", "exist", "different", "hours", "how"),
          avoid=("jet lag", "flight", "travel", "call", "meeting", "zoom")),
    entry("universe-age", (("universe",), ("old", "age", "big", "how", "years", "billion",
                                           "expand", "expanding")),
          "The universe is about 13.8 billion years old, measured from how fast it is expanding "
          "and the oldest light we can see. It has no edge or centre that we know of; space itself "
          "stretches between the galaxies.",
          ask=("how old", "age", "how big", "when", "expand", "expanding", "billion")),
    entry("earth-inside", (("earth",), ("made", "inside", "core", "layers", "what", "crust",
                                        "mantle", "composition")),
          "The Earth is layered: a thin rocky crust, a hot slow-flowing mantle, a liquid outer core "
          "of iron and nickel, and a solid inner core. The churning iron outer core is what makes "
          "the magnetic field that keeps the solar wind off us.",
          ask=("what", "made", "inside", "core", "layers", "crust", "mantle")),
    entry("dinosaurs", (("dinosaur", "dinosaurs"), ("die", "died", "extinct", "extinction", "why",
                                                     "disappear", "kill", "killed", "gone", "live",
                                                     "lived", "long ago", "how long", "when",
                                                     "era", "period", "old", "million years")),
          _dinosaurs),
    entry("vitamin-d", (("vitamin d", "vit d"),
                        ("winter", "dark", "october", "november", "december", "january", "february",
                         "march", "need", "should", "sun", "sunlight", "not enough")),
          "Take 10 micrograms (400 IU) of vitamin D every day through autumn and winter, roughly "
          "October to March: the sun is too low in the sky here for your skin to make it, however "
          "grey or bright the day is. From April to September, short spells outside with hands and "
          "face uncovered is enough for most people, and oily fish, eggs and fortified cereal help "
          "the rest of the year.",
          avoid=("iron", "calcium", "folic", "folate", "magnesium", "zinc", "multivitamin",
                 "multivitamins", "multivit", "protein", "creatine", "collagen", "omega", "fish oil",
                 "b12", "pregnant", "pregnancy", "deficiency", "deficient")),
    entry("stye", (("stye", "styes",
                    "sty",
                    "lump on my eyelid", "bump on my eyelid", "eyelid lump",
                    "chalazion", "lash line"),
                   ("get rid", "gone", "go away", "treat", "help", "what", "drain", "red",
                    "should i",
                    "have", "has", "had", "ive", "i've", "got", "my", "is", "are", "im",
                    "i'm", "it", "this", "lump", "bump", "pimple", "spot", "hard", "pea",
                    "swollen", "tender", "sore", "painful", "blocked", "how long", "last")),
          "Hold a warm, clean flannel against it for ten minutes, three or four times a day: that "
          "helps it drain, usually within two weeks. Don't squeeze it, and leave off eye make-up "
          "and contact lenses until it has gone. A hard, painless lump on the lid is a chalazion "
          "and wants the same warmth. See a pharmacist or GP if it has not settled in a week, or "
          "the lid is red and swollen.",
          avoid=("twitch", "twitching", "itchy", "itching", "sticky", "crusty", "gunky",
                 "watering", "watery", "gritty", "dry", "contact lens", "contacts", "mascara",
                 "makeup", "test", "glasses", "screen", "sleep", "tired", "dog", "cat",
                 "puppy")),
    entry("cold-sore", (("cold sore", "cold sores", "sore on my lip"),
                        ("get rid", "treat", "help", "stop", "first", "tingle", "spread", "how",
                         "what", "cream", "lip")),
          "Start aciclovir cream from the pharmacy at the first tingle and keep going for five "
          "days: caught early, it shortens the sore. It stays contagious until it has crusted over, "
          "so don't share towels, cups or lip balm, and don't pick it. Keep it away from newborn "
          "babies, who need a doctor straight away if one appears on them."),
    entry("hangover-morning", (("hangover", "hungover", "drank too much", "too much to drink",
                        "drank too much alcohol", "too much wine", "too much beer",
                        "sober up", "sobering up", "get sober", "sober", "sobered",
                        "still drunk", "still pissed", "still tipsy"),
                       ("help", "cure", "get rid", "best", "what", "how", "water", "stop",
                        "avoid", "morning")),
          _hangover,
          avoid=("coffee", "tea", "water", "caffeine", "sugar", "juice", "milk", "fizzy",
                 "squash",
                 "sober for", "sober since", "years sober", "months sober", "weeks sober",
                 "days sober", "sober app", "gave up drinking", "quit drinking", "stop drinking",
                 "drive", "driving", "the car")),
    entry("teeth-grinding", (("grind", "grinding", "bruxism", "clench", "clenching"),
                             ("teeth", "jaw", "night", "sleep", "stop", "dentist", "morning")),
          _grinding,
          explain=True),
    entry("knuckles", (("knuckle", "knuckles", "crack", "cracking", "clicking"),
                       ("bad", "harm", "damage", "arthritis", "hurt", "why", "habit", "cause",
                        "bad for")),
          "No: the pop is gas coming out of the fluid in the joint, and the studies that have "
          "looked have found no link between cracking your knuckles and arthritis. Forcing a joint "
          "can make it sore or swollen, so if one clicks with real pain rather than a clean pop, "
          "get it looked at.",
          ask=("knuckle", "knuckles", "crack", "cracking", "cracked"),
          avoid=("knee", "knees", "ankle", "hip", "hips", "elbow", "shoulder", "jaw", "neck",
                 "back", "wrist",
                 "egg", "eggs", "shell", "boil", "boiling", "boiled", "pan", "pot",
                 "carrot", "carrots", "parsnip", "parsnips", "beetroot", "radish", "radishes",
                 "turnip", "turnips", "swede", "celery", "cucumber", "cucumbers",
                 "voice", "throat", "lip", "lips", "skin", "hands", "heels", "heel",
                 "mug", "cup", "plate", "bowl", "glass", "window", "screen", "phone",
                 "wall", "walls", "ceiling", "tile", "tiles", "plaster", "pavement", "road",
                 "driveway", "brick", "concrete", "pipe", "whip", "meringue",
                 "batter", "pastry", "dough", "bread", "cake", "biscuit",
                 "cheesecake", "cheesecakes", "tart", "tarts", "choux", "macaron", "macarons",
                 "brownie", "brownies", "ganache", "pie", "loaf", "scone", "scones",
                 "hurt", "hurts", "hurting", "pain", "painful", "sore", "swollen", "aching",
                 "ache", "aches",
                 "dry", "drier", "dryness", "flaky", "flaking", "chapped", "moisturiser",
                 "moisturizer", "emollient"),
          bias=2),
    entry("eye-twitch", (("eye", "eyelid"),
                         ("twitch", "twitching", "flicker", "flickering", "ticking", "spasm",
                          "jumping", "tics")),
          "A twitching eyelid is usually tiredness, caffeine or stress, and it settles by itself "
          "within a few days to a couple of weeks. Sleep more, ease off the coffee, and use "
          "lubricating drops if your eyes are dry from screens. See a GP if the twitch spreads "
          "down that side of your face, or the eye closes on its own."),
    entry("bruise", (("bruise", "bruised", "bruising"),
                     ("why", "treat", "treatment", "help", "get rid", "how", "fast", "heal",
                      "appear", "randomly", "explain", "gone",
                      "go away", "wont go", "not going", "still there", "lasts", "lasting",
                      "weeks", "months", "stay",
                      "spread", "spreading", "spreads", "growing", "bigger", "larger",
                      "getting bigger", "keeps growing",
                      "fade", "fading", "fades", "doesnt fade", "not fading",
                      "hurts", "hurt", "hurting", "pain", "painful", "sore", "throbbing",
                      "aching", "easily", "easy", "yellow", "colour", "color", "turning")
                     + ASK_ABOUT),
          _the_bruise_answer),
    entry("heartburn", (("heartburn", "acid reflux", "reflux", "indigestion"),
                        ("night", "help", "get rid", "stop", "what", "antacid", "burning", "worse",
                         "relief",
                         "after dinner", "after eating", "after a meal", "after food",
                         "after my tea", "in the night", "at night", "when i lie down",
                         "lying down", "keep getting", "keeps coming back",
                         "every", "every evening", "every night", "most evenings", "most nights",
                         "most days", "often", "always", "reflux")
                        + _HEARTBURN_ASKS
                        + ("why", "why do i", "why am i", "cause", "causes", "trigger", "triggers",
                           "food", "foods", "diet", "avoid", "cut out", "eat", "eating",
                           "gives me", "gives", "gives you", "sets off", "set off", "brings on",
                           "bring on", "i get", "getting", "get", "from", "reaction", "reactions",
                           "awake", "sleep", "sleeping", "asleep", "wake me", "wakes me",
                           "woke me", "cant sleep", "keep me up", "keeps me up", "propped up",
                           "pregnant", "pregnancy", "expecting", "tablets", "pills", "medication",
                           "medicine", "ibuprofen", "aspirin", "naproxen", "painkillers",
                           "take", "taking", "safe", "ok to take",
                           "have", "having", "got", "suffering", "again", "killing me", "terrible",
                           "awful", "so bad", "really bad", "hurts", "hurting", "today",
                           "right now", "all the time", "constantly", "drink", "drinking",
                           "gaviscon", "antacid", "antacids", "isnt helping", "not helping",
                           "doesnt work", "doesnt help", "isnt working", "not working",
                           "stopped working", "any more")),
          _heartburn,
          bias=4,
          avoid=("chest", "arm", "jaw", "breathless", "short of breath", "sweating", "crushing",
                 "tight", "baby", "babies", "newborn", "infant", "toddler", "my son",
                 "my daughter", "my child")),
    entry("hayfever", (("hayfever", "hay fever", "pollen", "allergy season"),
                       ("help", "stop", "get rid", "treat", "worst", "control", "antihistamine",
                        "what", "how", "symptoms", "bad", "i have", "ive got", "i've got",
                        "i have got", "suffer", "suffering", "every year", "each year",
                        "seasonal", "started", "starting",
                        "is it", "a cold", "or a cold", "cold or", "difference", "or is it",
                        "which is it", "all the time")),
          _hayfever_or_a_cold,
          avoid=("dog", "cat", "kitten", "puppy", "pet", "food", "peanut", "nuts", "bee", "wasp",
                 "sting", "baby", "milk", "gluten"),
          report=True),
    entry("always-tired",
          (("tired", "no energy", "any energy", "keep falling asleep", "tired even after", "knackered",
            "low on energy", "low in energy", "low of energy",
            "am exhausted", "i'm exhausted", "im exhausted", "feel exhausted", "feeling exhausted",
            "so exhausted", "always exhausted", "exhausted all the time", "exhausted after",
            "am i exhausted",
            "exhausted by", "exhausted lately", "worn out", "feel worn out", "feeling worn out",
            "i'm worn out", "im worn out", "so worn out", "worn out after", "worn out all the time",
            "feel drained", "feeling drained", "so drained", "drained after", "drained all the time",
            "feel run down", "feeling run down", "i'm run down", "im run down", "a bit run down",
            "feeling a bit run down", "shattered",
            "still tired", "still exhausted", "still knackered", "tired all day",
            "tired all the time", "exhausted all the time",
            "more energy", "some energy", "energy levels", "energy back", "get energy",
            "often exhausted", "often tired", "often knackered", "often shattered",
            "often worn out", "often drained", "exhausted a lot", "tired a lot",
            "knackered a lot",
            "tired most days", "exhausted most days", "regularly tired",
            "regularly exhausted", "keep feeling tired", "keep feeling exhausted")
           + _KEYED_FEELINGS,
           ("normal", "why", "what", "how", "should", "worry", "worried", "fix", "wrong",
            "always", "constantly", "every day", "all the time", "all day", "lately", "for weeks",
            "for months", "doctor", "gp", "blood test", "sleep", "desk", "afternoon", "morning",
            "driving", "mornings",
            "often", "a lot", "regularly", "most days", "most weeks")),
          "Most constant tiredness is dull rather than medical: too little sleep, a late screen, "
          "alcohol, caffeine after lunch, or no daylight. Give it two weeks of the basics before "
          "you assume anything else - the same bedtime and getting-up time every day, twenty "
          "minutes outside in the morning, no caffeine after two, and no phone in the bedroom. "
          "If it is still there after that, see a GP for a blood test: low iron, an "
          "underactive thyroid and low vitamin D are the usual finds, and iron is common and easy "
          "to treat, especially for anyone with heavy periods.",
          avoid=("chest", "breathless", "cant breathe", "fainted", "passed out", "blood", "coughing",
                 "cancer", "chemo", "pregnant", "baby", "newborn", "depressed", "suicidal",
                 "battery", "phone", "laptop", "charger", "charging",
                 "cant get out of bed", "slept badly", "long day", "children are", "kids are",
                 "this week", "this month", "killing me", "want to help", "but im exhausted",
                 "my son", "my daughter", "my child", "my kids", "toddler", "teenager", "baby",
                 "eyes", "eye", "screen", "monitor", "glasses", "flu", "virus", "covid",
                 "cold", "infection", "chemo",
                 "phone battery", "phone's battery", "phones battery",
                 "laptop battery", "laptop's battery", "battery drains", "battery drain",
                 "battery dies", "battery dying", "battery health",
                 "down the drain", "the drain", "drain is", "drains are", "drain pipe",
                 "my drain", "drain blocked", "drain slow", "drain smells", "drain smelly",
                 "drain dripping", "drain leaking", "drain clogged",
                 "drainage", "plumbing", "plumber", "plughole", "bleach", "blocked drain",
                 "unblock", "sewer", "sink", "toilet", "tap", "washing machine", "dishwasher",
                 "sleep in", "lie in", "let her sleep", "let him sleep", "let them sleep",
                 "draining friend", "friend is draining", "friend drains", "friends draining",
                 "draining me", "drains me", "exhausting friend", "friend is exhausting",
                 "friends are exhausting", "friend who drains", "wears me out", "worn me out",
                 "car", "cars", "van", "vans", "lorry", "truck", "mot", "motorbike",
                 "motorcycle", "scooter", "engine", "silencer", "exhaust pipe", "exhaust fumes",
                 "brake", "brakes", "brake pads", "pads", "clutch", "gearbox", "suspension",
                 "tyre", "tyres", "muffler", "catalytic",
                 "tired of", "sick of", "bored of", "bored with", "fed up of", "had enough of"),
          guard=_names_the_feeling),
    entry("more-energy",
          (("more energy", "low energy", "energy levels", "my energy", "afternoon slump",
            "energy slump", "sluggish", "keep flagging"),
           ("how", "what", "get", "getting", "eat", "should", "increase", "boost", "keep",
            "any", "tips", "help", "have", "why")),
          "Energy comes from sleep, daylight and food, in that order: the same bedtime and "
          "getting-up time every day, ten minutes outside in the morning light, and a lunch with "
          "protein and slow carbs rather than just a sandwich, so three o'clock does not flatten "
          "you. Water through the day and no caffeine after two help too. Still flat after two "
          "weeks, ask your GP for a blood test for iron and thyroid.",
          bias=1,
          avoid=("contract", "contracts", "cancel", "cancelling", "cancellation", "supply",
                 "account", "accounts", "meter", "meters", "switch", "switching", "switched",
                 "direct debit", "unit rate", "economy 7", "prepayment", "smart meter",
                 "bill", "bills", "company", "companies", "supplier", "tariff", "solar",
                 "electricity", "gas", "price cap", "standing charge", "renewable", "kwh",
                 "energy drink", "energy drinks", "red bull", "monster", "drink", "drinks",
                 "exercise", "workout", "gym", "calories", "carbs", "protein shake",
                 "my car", "the car", "house", "home", "flat", "boiler", "heating")),
    entry("sleep-in",
          (("sleep in", "sleeping in", "lie in", "lying in", "let her sleep", "let him sleep",
            "let them sleep", "let me sleep"),
           ("should", "shall", "is it", "is a", "ok to", "okay to", "alright to", "worth",
            "better", "bad", "allowed", "can i", "can we", "could i", "let")),
          "An extra hour or two is usually the good call after a short night. Let the sleep "
          "happen, then open the curtains and get some daylight. Keep the rest of the day on "
          "the usual times and go to bed at the usual hour tonight: a long lie-in shifts the "
          "body clock and makes the next night harder. If the tiredness is there most mornings "
          "for weeks, that is worth a GP and a blood test.",
          avoid=("night shift", "work nights", "night shifts", "in the day", "missed my train",
                 "late for work", "alarm", "baby", "newborn", "toddler")),
    entry("parent-memory",
          (("mum", "mom", "mother", "dad", "father", "parent", "parents", "grandma", "grandmother",
            "grandad", "grandfather", "gran", "nan", "nana", "mother in law", "father in law",
            "husband", "wife", "partner", "spouse", "other half", "brother", "sister",
            "aunt", "auntie", "uncle", "boyfriend", "girlfriend",
            "cousin", "friend", "mate", "pal", "chum",
            "neighbour", "neighbor", "colleague", "coworker", "boss", "flatmate", "housemate",
            "carer", "nephew", "niece", "grandchild", "grandson", "granddaughter", "fiance",
            "fiancee", "missus", "stepmum", "stepdad", "sister in law", "brother in law",
            "daughter in law", "son in law"),
           ("forgetting", "forgetful", "forgets", "forgot", "memory", "repeats", "repeating",
            "confused", "confusion", "gets lost", "wandering", "same question", "forget things",
            "forgetting things", "forget names", "forgets names", "cannot remember",
            "cant remember", "can't remember", "cant recall", "keeps forgetting",
            "forget words", "cant remember words",
            "losing her", "losing his", "losing their", "keeps losing", "loses things",
            "losing things", "losing track", "loses her", "loses his", "loses their")),
          "Write down for a fortnight what they forget, and whether it is new. Slower recall of "
          "names is ordinary; asking the same question within minutes, getting lost on a familiar "
          "route, or forgetting something they have always done are not, and want a GP "
          "appointment. Take the notes and ask for a memory assessment, and say if they still "
          "drive: an infection, low B12, an underactive thyroid, poor hearing and some medicines "
          "can all cause a fixable muddle.",
          guard=lambda reading: (not _owns_the_deed(reading)
                                and not _a_habit_without_the_illness(reading)
                                and not _the_speaker_forgot_to_do_it(reading)
                                and not _its_money_that_has_not_come_back(reading)),
          avoid=("died", "passed away", "funeral", "burial", "cancer", "hospice", "birthday",
                 "christmas", "never calls", "wont call", "anniversary", "card", "present",
                 "hospital", "stroke", "dementia diagnosed", "care home",
                 "wandering", "wanders", "wandered", "gone missing", "went missing",
                 "gone walkabout", "left the house at night", "found in the street",
                 "tablet", "tablets", "medication", "medications", "meds", "medicine", "medicines",
                 "dose", "doses", "insulin", "diabetes", "diabetic", "pills", "pill",
                 "blood pressure", "warfarin", "epilepsy",
                 "i keep forgetting", "i keep forgetting to", "i'm always forgetting",
                 "im always forgetting", "i always forget", "i forget to", "i forgot to",
                 "me keep forgetting"),
          bias=2),
    entry("own-memory-worry",
          (("memory", "memories", "forgetful", "forgetfulness", "forgetting", "forget",
            "dementia", "alzheimers", "alzheimer's", "recall", "remember", "remembers",
            "remembering"),
           ("my memory", "my memories", "my recall", "im getting forgetful",
            "i am getting forgetful", "im so forgetful", "i am so forgetful", "so forgetful",
            "getting forgetful", "getting worse", "worse lately", "getting bad",
            "memory loss", "my memory is", "memory is getting", "memory problems",
            "short term memory", "short-term memory", "losing my memory", "losing it",
            "keep forgetting things", "cant remember things", "can't remember things",
            "keep forgetting everything", "forgetting everything", "forgetting a lot",
            "forget things", "cant remember things like i used to", "remember things like i used to",
            "things like i used to", "not as good as it was",
            "should i worry", "is it normal", "how do i know", "am i getting", "am i losing",
            "could it be", "am i", "why am i", "worried", "worry",
            "scared", "frightened", "terrified", "im worried", "worried im", "scared im",
            "getting alzheimers", "getting dementia", "mean dementia",
            "does forgetting mean", "is forgetting", "does this mean", "does that mean",
            "cant hold on to", "forgetting names", "forgets names", "forgetting words",
            "sign of dementia", "sign of alzheimers", "signs of dementia", "a sign", "signs",
            "symptom of", "symptoms of", "early signs", "first signs", "is it dementia",
            "could it be dementia", "does it mean dementia", "start of dementia")),
          "Note it down for a fortnight before you decide anything: what was forgotten, when, and "
          "whether it was new. Forgetting names, or where the keys went, is ordinary at any age "
          "and worse when you are tired, stressed, low or sleeping badly. What is not ordinary is "
          "losing the thread of something you have always done - a recipe you know by heart, the "
          "way to a place you drive every week, paying the same bill twice - and that is what "
          "wants a GP. Book one if it is getting worse, if it came on suddenly, or if it frightens "
          "you, and take the notes with you: a GP can check the causes that are fixable, which "
          "include low B12, an underactive thyroid, blood pressure, sleep apnoea, depression and "
          "the medicines you already take. Going early is not an overreaction; it is how the "
          "fixable ones get found.",
          guard=lambda reading: (_not_somebody_elses_memory(reading) and not _owns_the_deed(reading)
                                and not _a_habit_without_the_illness(reading)
                                and not _the_speaker_forgot_to_do_it(reading)
                                and not _its_money_that_has_not_come_back(reading)),
          avoid=("forgetting to", "forgot to", "forget to",
                 "interview", "interviews", "presentation", "presentations", "go red", "went red",
                 "blush", "blushes", "go blank", "went blank", "nervous", "panic",
                 "what causes", "why does", "why do we", "how does memory work", "sleep",
                 "tired", "exhausted", "baby", "newborn", "pregnant", "menopause",
                 "why", "revise", "revising", "revision", "revised", "study", "studying",
                 "studied", "exam", "exams", "coursework", "flashcards", "learn", "learning",
                 "memorise", "memorize", "test myself",
                 "improve", "improving", "sharpen", "sharpening", "boost", "train my memory",
                 "better memory", "memory better", "memory tricks", "techniques", "tips",
                 "games for", "exercises", "get sharper", "keep my memory", "stay sharp",
                 "memory is fine", "memory is good", "memory is ok", "memory is okay")),

    entry("why-cant-i-sleep",
          (("why cant i sleep", "why can't i sleep", "why cant i sleep at night",
            "why can't i sleep at night", "why am i not sleeping", "why am i not tired",
            "cant sleep at night", "can't sleep at night", "not sleeping well",
            "not sleeping at all", "why am i awake", "what keeps me awake"),
           ("night", "nights", "lately", "always", "any more", "anymore", "at all",
            "why", "cause", "reason", "again", "every night", "these days", "week")),
          "Usually it is the wake-up time rather than the bedtime: a lie-in at the weekend, a nap, "
          "or coffee after about two in the afternoon keeps the body clock late, and a warm room "
          "or a phone in bed finishes the job. Fix the getting-up time first, move the coffee "
          "before lunch, keep the bedroom around 18C and dark, and give it a week before you "
          "judge it. If it is a worry that wakes you, spend ten minutes before bed writing the "
          "list down so your head is not doing it at three. See a GP if it has gone on a month, "
          "or if the days are falling apart.",
          avoid=("baby", "newborn", "toddler", "child", "children", "snoring", "apnoea",
                 "shift work", "jet lag", "how long does it take", "minutes to fall",
                 "melatonin", "sleeping tablets", "depressed", "hopeless", "suicidal",
                 "self harm", "died", "funeral", "exam tomorrow",
                 "wake up", "wakes up", "woke up", "waking up", "i wake", "keeps waking",
                 "keep waking", "in the night", "through the night", "middle of the night",
                 "get back to sleep", "back to sleep", "on my back", "on my front")),
    entry("cant-switch-off",
          (("overthinking", "overthink", "cant switch off", "can't switch off", "mind racing",
            "racing thoughts", "cant stop thinking", "can't stop thinking", "lying awake",
            "wide awake", "cant sleep", "can't sleep", "cant get to sleep",
            "my head wont stop", "thoughts spinning"),
           ("night", "stop", "how", "help", "worry", "worrying", "anxious", "stress", "stressed",
            "work", "tomorrow", "always", "waking", "wake", "early", "hours", "thought")),
          "Get the thinking out of your head before bed: ten minutes with a pen, a list of what is "
          "actually worrying you and the first step for each, and a line at the bottom saying what "
          "can wait until morning. Then keep the bed for sleeping - if you are still awake after "
          "about twenty minutes, get up, sit somewhere dim with something dull, and go back when "
          "you are sleepy, so the bed does not become the place you argue with yourself. Same "
          "winding-down half hour each night, phone out of reach, and get up at the same time "
          "whatever happened, because the wake-up time is what steadies the sleep.",
          ask=("how", "why", "what", "should", "help", "stop", "any", "tips", "advice", "could"),
          avoid=("suicidal", "kill myself", "self harm", "panic attack", "died", "funeral",
                 "snoring", "apnoea", "sleep apnoea", "baby", "newborn", "shift work", "jet lag",
                 "melatonin", "sleeping tablets", "insomnia for years", "get out of bed",
                 "out of bed", "depressed", "hopeless", "no point", "cant face", "crying",
                 "empty", "numb", "worthless")),
    entry("sleep-how-to",
          (("how do i sleep better", "how to sleep better", "sleep better", "sleep properly",
            "how do i get to sleep", "how to get to sleep", "get to sleep faster",
            "fall asleep faster", "fall asleep quicker", "help me fall asleep",
            "help me get to sleep", "how do i fall asleep",
            "how do i get a good nights sleep", "how do i get a good night's sleep",
            "how do i get a good night sleep", "how can i get a good nights sleep",
            "how can i get a good night's sleep", "how can i sleep well",
            "how do i sleep well", "tips for sleeping well", "what helps me sleep well",
            "any tips for sleeping well",
            "improve my sleep", "improve my sleeping", "sort out my sleep", "sort my sleep out",
            "better sleep", "get better sleep", "sleep improvement", "work on my sleep",
            "wind down", "sleep routine",
            "bedtime routine", "sleep hygiene", "sleep tips", "tips for sleeping",
            "keep waking up", "waking up in the night", "wake up in the night",
            "waking in the night", "wake up every night",
            "what helps me sleep", "helps me sleep", "help me sleep", "anything to help me sleep",
            "sleep through the night", "sleep right through", "stay asleep", "stop waking up"),
           ("sleep", "sleeping", "asleep", "bed", "bedtime", "night", "nights", "tonight")),
          "Fix the wake-up time first: the same hour every day, including after a bad night, and "
          "the rest tends to follow within a fortnight. Then the three that do most of the work - "
          "daylight and a walk in the first hour, no caffeine after lunch, and a screen-free half "
          "hour before bed - and only get into bed when you are sleepy rather than tired. Waking in "
          "the small hours is usually the mind, not a sleep problem: keep the room dark, don't check "
          "the clock, and after about twenty minutes get up and sit somewhere dim until you are "
          "sleepy, so the bed stops being the place you lie and argue with yourself. Still broken "
          "after six weeks of that is worth a word with a GP.",
          avoid=("overthinking", "overthink", "cant switch off", "can't switch off", "mind racing",
                 "racing thoughts", "cant stop thinking", "can't stop thinking", "lying awake",
                 "worry", "worried", "worrying", "anxious", "anxiety", "stress", "stressed",
                 "baby", "babies", "newborn", "toddler", "my son", "my daughter", "my child",
                 "kids", "puppy", "cat", "dog", "snoring", "snore", "apnoea", "shift work",
                 "night shift", "jet lag", "time zone", "melatonin", "sleeping tablets",
                 "work nights", "working nights", "on nights", "night shifts", "shifts",
                 "sleeping tablet", "insomnia for years", "out of bed", "get out of bed",
                 "too much", "how much", "how many hours", "hours of sleep")),
    entry("smoking-harm",
          (("smoking", "cigarettes", "cigarette", "tobacco", "nicotine",
            "cigarette smoke"),
           ("bad", "harmful", "harm", "damage", "damages", "effects", "effect", "why is",
            "what does it do", "do to your body", "bad for you", "bad for", "cause", "causes",
            "cancer", "dangerous", "how bad", "unhealthy", "health", "how many", "safe")),
          "Smoking is the single biggest cause of cancer and heart disease you can remove "
          "yourself: the tar and the carbon monoxide damage the lungs and the arteries, and about "
          "half of lifelong smokers die early because of it. There is no safe number of "
          "cigarettes - one to four a day still multiplies the heart risk - and the gains start "
          "within days of stopping, which is why quitting at any age is worth it.",
          avoid=("stop", "stops", "stopping", "quit", "quits", "quitting", "give up", "cut down",
                 "patch", "patches", "cold turkey", "vape", "vapes", "vaping", "e cigarette",
                 "weed", "cannabis", "joint", "joints", "skunk", "marijuana", "dope", "spliff",
                 "passive", "second hand", "secondhand", "smoked salmon", "smoked haddock",
                 "smoked mackerel", "smoked bacon", "smoked paprika", "smoked cheese", "barbecue",
                 "bbq", "brisket", "smoker", "campfire", "bonfire", "wood smoke", "chimney",
                 "smoke alarm", "smell", "stain", "smoke from",
                 "exhaust", "exhausts", "engine", "engines", "motorbike", "motorcycle",
                 "scooter", "mower", "lawnmower", "lawn mower", "generator", "van",
                 "dad", "mum", "mother", "father",
                 "husband", "wife", "partner", "girlfriend", "boyfriend", "friend", "son",
                 "daughter", "brother", "sister", "worried", "worry", "he smokes", "she smokes",
                 "cost", "price", "how much do", "tax")),

    entry("secondhand-smoke",
          (("second hand smoke", "secondhand smoke", "passive smoking", "passive smoke",
            "second hand smoking", "secondhand smoking", "someone smokes", "smokes in the house",
            "smokes indoors", "smoke in the house", "smoke around"),
           ("bad", "harmful", "harm", "risk", "risks", "dangerous", "affect", "effects", "effect",
            "health", "pregnant", "pregnancy", "baby", "children", "kids", "child", "really",
            "is it", "how bad", "safe", "do to")),
          "Secondhand smoke is a real risk, not a smell: it carries the same tar, carbon monoxide "
          "and carcinogens, and living with a smoker raises a non-smoker's lung cancer risk by "
          "roughly a quarter and a child's risk of chest and ear infections much more. There is no "
          "safe level of exposure, and an open window or a separate room does not clear it - the "
          "only thing that works is smoking outside, away from the door.",
          avoid=("stop", "stops", "stopping", "quit", "quits", "quitting", "give up", "cut down",
                 "vape", "vapes", "vaping", "e cigarette", "patch", "patches", "help", "how do i",
                 "weed", "cannabis", "joint", "joints", "smoked salmon", "barbecue", "bbq",
                 "campfire", "bonfire", "wood smoke", "smoke alarm", "smell", "stain")),

    entry("cannabis-harm",
          (("weed", "cannabis", "marijuana", "skunk", "joint", "joints", "spliff", "ganja",
            "hash", "dope", "stoned", "smoking weed", "smoke weed"),
           ("bad", "harmful", "harm", "worse than", "compared", "compare", "cigarettes",
            "tobacco", "health", "risk", "risks", "effects", "effect", "psychosis", "mental",
            "addictive", "addicted", "safe", "how bad", "lungs", "brain", "for you")),
          "Smoked cannabis is harmful in a different way from tobacco: most joints are rolled "
          "with tobacco, so they carry the same tar and nicotine, a joint is held in longer, and "
          "the risk of psychosis and of anxiety is real and rises with heavy use and with high-THC "
          "skunk. It is not physically addictive like nicotine but the habit is hard to shift, and "
          "the damage is worse under about 25 while the brain is still developing. Vaping THC or "
          "eating it takes out the smoke, not the effects on the mind.",
          avoid=("stain", "stains", "carpet", "sofa", "garden", "lawn", "flowerbed", "driveway",
                 "patio", "knees", "weed killer", "roundup", "stop", "stops",
                 "stopping", "quit", "quits", "quitting", "give up", "cut down", "how do i",
                 "help me", "vape", "vaping")),

    entry("alcohol-harm",
          (("alcohol", "drinking", "drink", "drinker", "beer", "wine", "booze", "vodka",
            "whisky", "spirits"),
           ("bad for you", "bad for", "harmful", "harm", "damage", "damages", "risks", "risk",
            "effects", "effect", "cancer", "health", "does to your body", "liver", "safe",
            "how bad", "why is")),
          "Alcohol is a group 1 carcinogen and there is no amount that is good for you: the risk "
          "starts with the first drink and rises with the total, which is why the guidance is "
          "about keeping it low rather than finding a safe level. The liver, the blood pressure "
          "and the risk of seven cancers - mouth, throat, oesophagus, liver, colon, and in women "
          "breast - all move the same way. A couple of drink-free days and staying under 14 units "
          "a week is what keeps the risk small.",
          avoid=("how much", "how many", "units", "weekly", "limit", "limits", "recommended",
                 "guidelines", "drive", "driving", "drink driving", "licence", "police", "test",
                 "hangover", "hungover", "pregnant", "pregnancy", "breastfeeding", "antibiotics",
                 "tablets", "medication", "medicine", "stain", "stains", "spill", "carpet",
                 "recipe", "sauce", "cake", "opened", "fridge", "keep", "keeps", "calories",
                 "cut down", "reduce", "less", "stop", "quit", "give up", "dog", "cat", "pet",
                 "coffee", "tea", "energy drink", "battery", "hand gel", "smell", "pour")),

    entry("alcohol-clearance",
          (("alcohol", "alcohol i drank", "drinks", "pint", "pints", "wine", "beer", "vodka",
            "booze", "a drink"),
           ("how long", "stay in", "stays in", "still in", "out of my system", "out of your system",
            "clear my system", "clear of", "blood", "breath", "system", "metabolise", "burn off",
            "leave my body", "last in")),
          "Alcohol leaves at about one unit an hour and nothing speeds that up - coffee, a cold "
          "shower and food only make you feel different, not soberer. A pint of normal-strength "
          "beer, a medium glass of wine or a single spirit is two to three units, so a heavy "
          "evening can still leave alcohol in your blood the next morning, which is why the "
          "morning-after drive is the one that catches people.",
          avoid=("units", "how much is too much", "weekly limit", "limit", "limits", "legal",
                 "drive", "driving", "drink driving", "licence", "arrested", "police", "test",
                 "pregnant", "pregnancy", "breastfeeding", "antibiotics", "tablets", "medication",
                 "medicine", "hangover", "hungover", "stop", "quit", "cut down", "less", "reduce",
                 "recipe", "sauce", "cake", "opened", "fridge", "keep", "keeps", "calories",
                 "unit in", "how many units", "spill", "stain")),

    entry("just-quit-smoking",
          (("quit smoking", "stopped smoking", "gave up smoking", "quit vaping", "stopped vaping",
            "given up smoking", "off the cigarettes", "no cigarettes", "haven t smoked",
            "havent smoked", "not had a cigarette", "lungs"),
           ("last week", "yesterday", "days", "day", "week", "weeks", "month", "months",
            "first day", "first week", "how long", "feel", "feels", "feeling", "withdrawal",
            "cravings", "craving", "recover", "what happens", "now what", "awful", "tired",
            "mood", "anxious", "irritable", "worth it")),
          "The first week is the hardest and it does get easier: a craving peaks in about five "
          "minutes and the gaps between them stretch out after the third or fourth day. Expect a "
          "few days of being short-tempered and foggy, and a cough that brings up more than usual - "
          "the airways clearing is a good sign, not a relapse. The carbon monoxide is gone within "
          "a couple of days, breathing is easier in two to twelve weeks, and if a bad moment "
          "arrives, ride it out with water and a walk rather than testing your willpower.",
          avoid=("how do i", "how can i", "plan", "patch", "patches", "gum", "lozenge", "spray",
                 "best way", "tips", "tip", "stop date", "set a date", "should i",
                 "smoked salmon", "barbecue", "bbq", "brisket", "weed", "cannabis", "joint",
                 "weight", "vape flavour", "flavours", "cost", "price", "tax")),

    entry("stop-smoking",
          (("quit smoking", "stop smoking", "give up smoking", "quit cigarettes", "stop cigarettes",
            "cigarettes", "cigarette", "smoking", "vaping", "vape", "nicotine",
            "nicotine patch", "nicotine patches", "patch work", "patches work",
            "patch help", "patches help", "patch safe", "patches safe", "patch better",
            "patches better", "patch or gum", "patches or gum", "patch worth",
            "patches worth", "do patches", "does the patch", "does a patch", "the patch work",
            "patches any good", "patch any good", "gum",
            "which patch", "which patches", "best patch", "best patches", "patch is best",
            "patches is best", "patch best", "patches best", "patch better than", "patches do i",
            "smoked for", "smoked since", "been a smoker", "pack a day"),
           ("quit", "stop", "give up", "cut down", "how", "help", "best", "way", "tip", "tips",
            "worth", "try", "again", "cant", "can't", "struggling", "failed", "start",
            "good", "work", "works", "work for", "effective", "better", "safe")),
          "Set a stop date in the next two weeks and use nicotine replacement or a prescription "
          "aid as well as willpower: on willpower alone most attempts fail, and patches, gum or a "
          "vape roughly double to triple your odds, with free help from a stop-smoking service "
          "adding more. Know your two triggers and plan the swap - a walk after meals, something "
          "in your hands on the phone - because a craving peaks in about five minutes and passes. "
          "Slips are normal, not the end of it: two failed tries still leave you far better off, "
          "and the health gains start within days.",
          avoid=("meat", "brisket", "salmon", "barbecue", "bbq", "smoker", "smoked salmon",
                 "dad", "mum", "mother", "father", "husband", "wife", "partner", "girlfriend",
                 "boyfriend", "friend", "son", "daughter", "brother", "sister", "worried",
                 "worry", "wont", "won't",
                 "cough", "coughing", "vape", "vaping",
                 "last week", "yesterday", "havent smoked", "haven t smoked",
                 "not had a cigarette", "since i quit", "since i stopped", "i ve quit",
                 "i ve stopped", "3 days ago", "a week ago", "a month ago", "already",
                 "smoked meat", "smoked fish", "smoking meat", "wood smoke", "campfire",
                 "chimney", "is smoking bad", "why is smoking bad", "effects of smoking",
                 "passive smoking", "second hand", "secondhand", "smell", "as bad as",
                 "worse than", "safer than", "compared", "how many", "too many", "safe limit",
                 "gum disease", "gingivitis", "bleeding gums", "sore gums", "swollen gums",
                 "gums bleed", "my gums", "gums are", "teeth", "tooth", "toothache",
                 "dentist", "floss", "flossing", "mouth ulcer", "mouthwash",
                 "hair", "hairs", "scalp", "in my hair", "out of my hair", "stuck in",
                 "gum out of", "gum off", "gum on", "gum in", "gum from", "gum stain",
                 "how much sugar", "sugar in", "calories", "calorie", "sweetener",
                 "sweeteners",
                 "smoke alarm", "smoke detector", "alarm", "detector", "carbon monoxide",
                 "chirp", "chirping", "beeping", "battery", "chimney", "bonfire", "bbq",
                 "lawn", "lawns", "grass", "garden", "gardens", "yellow", "yellowing",
                 "leaves", "plant", "plants", "flower", "flowers", "shrub", "shrubs",
                 "soil", "moss", "turf", "brown patches", "bare patches",
                 "gum off", "gum on", "gum from", "gum stuck", "stuck to", "stuck on",
                 "jeans", "denim", "trousers", "carpet", "sofa", "settee", "shoe", "shoes",
                 "trainers", "fabric", "clothes", "stain", "stains",
                 ) + _SMOKE_IS_NOT_A_HABIT),
    entry("cholesterol",
          (("cholesterol", "ldl", "hdl", "triglycerides", "statins", "statin"),
           ("lower", "reduce", "bring down", "cut", "high", "diet", "food", "foods", "eat",
            "avoid", "help", "how", "what")),
          "Cut saturated fat first, because that moves the number more than anything else: less "
          "cheese, butter, fatty meat, pastry, biscuits and coconut oil, and swap to olive or "
          "rapeseed oil and leaner cuts. Then add the things that help - oats, beans or lentils "
          "daily, nuts, oily fish twice a week, and 30 minutes of walking on most days - and get a "
          "retest after about three months, since diet alone typically takes 10 to 20 percent off. "
          "If you have been given a statin, keep taking it; diet and the tablet work together.",
          avoid=("egg", "eggs", "shell", "yolk")),
    entry("steps-a-day",
          (("how many steps", "steps", "step count", "steps a day", "walking", "walk every day",
            "10,000 steps", "10000 steps"),
           ("how many", "a day", "in the day", "daily", "every day", "target", "should i",
            "enough", "recommended", "need")),
          "About 7,000 to 8,000 steps a day is where most of the benefit is - the health gain "
          "levels off there rather than at 10,000, which came from a 1960s pedometer advert - so "
          "add a daily twenty minutes on top of what you already do rather than chasing a round "
          "number. If you are a long way off, two ten-minute walks beat one long one because they "
          "are easier to keep up, and the walking you do getting about counts.",
          ask=("how many", "how much", "should i", "do i need", "enough", "recommended",
               "target", "a day", "daily"),
          avoid=("dog", "puppy", "cat", "pram", "pushchair", "baby", "toddler", "hike", "hiking",
                 "rambling", "trek", "stairs", "step by step", "stepper", "pedometer", "app",
                 "umbrella", "forecast", "suncream",
                 "waterproof", "waterproofs", "overtrousers", "trousers", "jacket", "coat",
                 "boots", "wellington", "wellies", "rucksack", "gaiters",
                 "litre", "litres", "liter", "liters", "how much water",
                 "eiffel", "tower", "building", "cathedral", "church", "abbey", "castle",
                 "monument", "stadium", "pyramid", "pisa", "empire state", "shard",
                 "snowdon", "ben nevis", "scafell", "mountain", "climb", "climbing", "summit",
                 "are there", "storey", "storeys", "story", "stories", "flight", "flights",
                 "floor", "floors",
                 "mile", "miles", "kilometre", "kilometres", "kilometer", "kilometers", "km",
                 "marathon", "half marathon", "5k", "10k", "parkrun", "race",
                 "calorie", "calories", "kcal",
                 "lose weight", "losing weight", "weight loss", "lose a stone", "lose fat",
                 "slim", "slimming")),
    entry("steps-in-a-distance",
          (("how many steps", "steps per", "steps in", "steps to a",
            "10000 steps", "10,000 steps", "5000 steps", "5,000 steps", "12000 steps",
            "12,000 steps", "15000 steps", "15,000 steps", "20000 steps", "20,000 steps"),
           ("mile", "miles", "km", "kilometre", "kilometres", "kilometer", "kilometers",
            "marathon", "half marathon", "5k", "10k", "parkrun", "race",
            "10000 steps", "10,000 steps", "5000 steps", "5,000 steps", "12000 steps",
            "12,000 steps", "15000 steps", "15,000 steps", "20000 steps", "20,000 steps")),
          _steps_in_a_distance,
          avoid=("a day", "daily", "every day", "per day", "target", "recommended", "enough",
                 "eiffel", "tower", "building", "cathedral", "pisa", "stadium", "stairs",
                 "calorie", "calories", "kcal",
                 )),
    entry("steps-up-a-building",
          (("how many steps", "how many stairs", "steps up", "stairs up"),
           ("pisa", "leaning tower", "empire state", "cathedral", "st pauls", "dome",
            "monument", "stadium", "flight of stairs", "flight", "risers", "between floors",
            "floor", "floors", "storey", "storeys", "story", "stories",
            "the stairs", "up the stairs", "upstairs", "staircase", "stairway",
            "flight of stairs", "are there")),
          _steps_up_a_building,
          bias=1,
          avoid=("eiffel", "a day", "daily", "every day", "per day", "to lose weight",
                 "mile", "miles", "km", "marathon", "5k", "10k", "shard",
                 "rent", "price", "cost", "square", "sq ft", "apartment for")),
    entry("steps-calories",
          (("steps", "step count", "walking", "walk"), CALORIE_WORDS),
          _steps_calories,
          bias=2,
          ask=("how many", "how much")),
    entry("steps-in-a-time",
          (("steps", "step count", "walking", "walk"), TIME_WORDS),
          _steps_in_a_time,
          bias=3,
          ask=("how many", "how much"),
          avoid=("a day", "per day", "daily", "every day", "each day", "a week",
                 "to lose weight", "lose weight",
                 "calorie", "calories", "kcal", "energy")),
    entry("steps-to-lose-weight",
          (("steps", "step count", "walking", "walk"),
           ("lose weight", "losing weight", "weight loss", "lose a stone", "lose fat", "slim",
            "slimming", "drop a dress size")),
          "Walking alone will not do it - what you eat decides most of it - but 8,000 to 10,000 "
          "steps a day is a fair target, and the gain is that it burns a little and keeps you "
          "from sitting down all day. The quicker half is the plate: a smaller portion of the "
          "starch, more protein and vegetables, and no drinks with sugar in. Half a kilo a week "
          "is a good rate, and the walking is easier to keep up than a gym plan.",
          bias=2),
    entry("strength-at-home",
          (("build muscle", "get stronger", "get stronger at home", "strength training",
            "home workout", "work out at home", "push ups", "push-ups", "pushups", "squats",
            "bodyweight", "resistance band", "resistance bands", "dumbbells", "dumbbell",
            "kettlebell", "free weights", "lift weights", "get stronger", "stronger"),
           ("home", "at home", "without", "no gym", "how", "start", "beginner", "beginning",
            "routine", "plan", "best", "way", "muscle", "stronger")),
          "Two or three sessions a week of five moves covers the whole body at home: squats or "
          "sit-to-stands for legs, press-ups (hands on a worktop if needed) for chest and arms, a "
          "row pulling a loaded bag or a band towards you for the back, glute bridges for hips, and "
          "a plank for the middle. Do two or three sets of eight to twelve, and add a little each "
          "week - more reps, a slower lower, a heavier bag - because muscle only grows when the "
          "last rep is hard. Two sessions a week beats five that you stop after a fortnight.",
          avoid=("protein", "how much protein", "knee", "back pain", "sore back", "injury",
                 "shoulder pain", "sciatica", "osteoporosis", "sarcopenia",
                 "coffee", "espresso", "tea", "cuppa", "brew", "beer", "ale", "cider",
                 "form", "technique", "proper", "how deep", "depth", "posture",
                 "signal", "wifi", "wi-fi", "wireless", "internet", "broadband", "reception",
                 "router", "upstairs", "downstairs", "booster", "mesh")),
    entry("posture",
          (("posture", "slouching", "slouch", "hunched", "hunching", "rounded shoulders",
            "stand up straight", "sit up straight", "sit properly", "sitting properly",
            "sit straight", "at my desk", "at a desk", "sitting at a desk", "sitting all day",
            "sit all day", "desk job", "working at a desk",
            "set up", "setting up", "set my", "too low", "too high",
            "how high", "how low",
            "where should my", "where should the", "where should i place",
            "sitting position", "sitting posture"),
           ("fix", "improve", "better", "bad", "correct", "how", "help", "desk", "chair",
            "screen", "office", "work", "should i", "ache", "aches", "aching", "achey",
            "hurt", "hurts", "sore",
            "good", "what is", "proper", "right way",
            "terrible", "awful", "poor", "rubbish", "dreadful",
            "monitor", "position")),
          "Most bad posture is the chair and the sitting still, not the spine: set the screen so "
          "the top of it is at eye level, feet flat, elbows near a right angle, and get up every "
          "half hour - five minutes of standing beats a whole evening of trying to sit straighter. "
          "Then strengthen what holds you up: chin tucks, rows with a band, and squeezing the "
          "shoulder blades ten times a few times a day. Aches that come with numbness, weakness or "
          "pain down an arm are worth a GP or physio, not a new chair.",
          avoid=("height", "tall", "bra", "support", "corset", "brace", "baby", "newborn",
                 "how tall", "grow", "clean", "clear", "tidy", "organise", "organize", "buy",
                 "buying", "wobbly", "broken", "standing desk", "move the desk", "surgery",
                 "slipped disc", "sciatica",
                 "nail", "nails", "chewing", "biting", "bite", "thumb", "fingers", "typing",
                 "keyboard",
                 "put", "mount", "mounting", "shelf", "shelves", "bracket",
                 ) + FEELING_WORDS,
          guard=all_of(_a_place_for_the_kit, not_a_sleepy_body)),

    entry("blood-pressure-numbers",
          (("blood pressure", "hypertension", "systolic", "diastolic"),
           ("lower", "reduce", "bring down", "high", "diet", "exercise", "naturally", "how",
            "help", "without", "worried",
            "healthy", "normal", "ideal", "what should it be", "what should mine be",
            "what should my", "should my")),
          "Under about 120/80 is normal and 140/90 or over at home is high. Salt is the biggest "
          "single lever: under 6g a day means watching bread, cheese, ham, stock cubes, sauces and "
          "takeaways rather than the salt cellar. Add 150 minutes of walking a week, more fruit "
          "and vegetables, at most 14 units of alcohol and a few kilos off if you carry them, and "
          "a typical reading comes down about 10 points in a couple of months. A week of home "
          "readings, sitting still, is what a GP wants - and never stop a blood pressure tablet to "
          "try diet alone.",
          avoid=("over 90", "over 140", "reading", "monitor", "stroke", "dizzy", "faint",
                 "pregnant", "my mum", "my dad", "my husband", "my wife", "tablet side effect",
                 "should i take", "can i stop", "stop taking", "come off", "side effect",
                 "my tablets", "my medication", "on tablets", "started on")),
    entry("snore-less",
          (("snoring", "snore", "snores", "snored", "loud breathing at night"),
           ("stop", "help", "how", "prevent", "reduce", "quiet", "partner", "wife", "husband",
            "night", "nightly", "bad", "loud",
            "other half", "oh", "bf", "gf", "dh", "dw", "dp", "boyfriend", "girlfriend")),
          "Sleeping on your side, cutting out alcohol in the evening and losing a little weight "
          "fix it for most people who snore, and a blocked nose is worth treating with a "
          "decongestant or a steroid spray from the chemist for a couple of weeks to see. A "
          "pillow that keeps you off your back, or a tennis ball sewn into the back of a top, "
          "does the side-sleeping job. Snoring with gasping, choking or stopping breathing, or "
          "daytime sleepiness despite enough hours, needs a GP - that is sleep apnoea and it is "
          "treatable.",
          avoid=("apnoea", "apnea", "gasping", "stop breathing", "sleep study", "cpap", "baby",
                 "child", "kids", "dog", "cat", "puppy", "sleeping tablet")),
    entry("weight-loss",
          (("lose weight", "lose fat", "losing weight", "slim down", "slimming", "belly fat",
            "flat stomach", "love handles", "get lean", "lose a stone", "lose a few pounds",
            "flat tummy", "fat around", "fat round", "around my waist", "round my waist",
            "thigh fat", "bingo wings", "muffin top", "saddlebags", "flabby",
            "lose my belly", "lose the belly", "lose my tummy", "lose the tummy",
            "flatten my belly", "flatten my tummy", "flat belly",
            "lose 10kg", "lose a kg", "drop a dress size", "tone up", "get in shape",
            "not losing weight", "not losing anything", "not lost anything", "losing nothing",
            "scales wont move", "scales won't move", "scales havent moved",
            "scales have not moved", "scales are stuck", "weight is stuck",
            "stuck at the same weight", "weight wont shift", "weight won't shift",
            "not shifting the weight",
            "how much should i lose", "how much can i lose", "how much do i lose",
            "how much to lose", "how much do i need to lose", "how much weight should i lose",
            "how much weight can i lose", "how many pounds should i lose",
            "how many pounds can i lose", "how many kilos should i lose"),
           ("how", "what", "best", "way", "tips", "advice", "start", "safely", "quickly",
            "fast", "should i", "can i", "want to", "trying to", "help", "plan", "diet",
            "why", "stuck", "anything", "nothing", "same")),
          "A steady half a kilo to a kilo a week comes from a deficit you can live with, not a "
          "crash: cut the drinks, the handfuls and the second helping - usually 300 to 500 "
          "calories a day - and eat the protein and vegetables first, because they fill you up "
          "longer than the same calories of bread. Walk 30 minutes most days and lift something "
          "twice a week, so what goes is fat, not muscle. You cannot choose where it comes off: "
          "belly fat goes when the total comes down, and the scales stalling for a week is normal.",
          ask=("how", "what", "best", "way", "tips", "advice", "help", "start", "safely",
               "quickly", "fast", "plan", "diet", "why", "stuck"),
          avoid=("hate my body", "hate the way", "disgusting", "starve", "starving myself",
                 "mat", "mats", "bath mat", "bath mats", "shower", "bathroom", "grout",
                 "floor", "floors", "towel", "towels", "sink", "drain", "tiles", "curtain",
                 "purge", "anorexic", "anorexia", "bulimia", "binge", "not eating", "cant eat",
                 "eat nothing", "my mum", "my dad", "my wife", "my husband", "my friend",
                 "my daughter", "my son", "my child", "kids", "toddler", "baby", "dog", "cat",
                 "puppy", "dress size 8", "wedding", "in two weeks", "by summer", "my face",
                 "my hair", "i keep losing weight", "losing weight without trying",
                 "unexplained")),
    entry("cut-down-sugar",
          (("sugar", "sugary", "sweets", "cravings", "sweet tooth", "chocolate", "biscuits",
            "fizzy drinks", "coke"),
           ("stop", "cut", "cut down", "eat less", "too much", "too many", "addicted",
            "addiction", "reduce", "quit", "how", "help", "less", "every day", "every night",
            "all the time", "cant stop", "can't stop", "eating too much", "eating too many")),
          "Cut the liquid sugar first, because it is the easiest to lose and the least filling: "
          "fizzy drinks, juice and squash swapped for water, sparkling water or tea. Then make the "
          "sweet thing a planned part of the day - a biscuit with the afternoon cup - instead of a "
          "thing you graze on, since grazing is what keeps the craving going. Protein and fibre at "
          "breakfast (eggs, porridge, yoghurt with nuts) takes the edge off the four o'clock "
          "search, and half a teaspoon less in the tea for a fortnight gets your taste down "
          "without noticing.",
          avoid=("blood sugar", "diabetes", "diabetic", "insulin", "recipe", "baking", "cake",
                 "banana bread", "bread", "loaf", "cookies", "cookie", "muffins", "muffin",
                 "sponge", "brownies", "brownie", "scones", "scone", "meringue", "pancakes",
                 "pancake", "pudding", "dessert", "gateau", "frosting", "buttercream",
                 "how much sugar is in", "sugar in a", "jam", "child", "kids", "toddler",
                 "protein", "calories", "calorie", "kcal", "carbs", "carb", "carbohydrates",
                 "fat", "fibre", "fiber", "nutrition", "nutrients",
                 "baby", "hyper",
                 "melt", "melts", "melting", "melted", "temper", "tempering", "seize", "seized",
                 "ganache", "dipping", "double boiler", "bain marie",
                 "off the", "off my", "off a", "out of", "out the", "stain", "stains", "stained",
                 "carpet", "sofa", "settee", "couch", "upholstery", "shirt", "jeans", "duvet",
                 "mattress", "cushion", "fabric", "washed", "scrub", "blot",
                 "spread", "spreads", "spreading", "flat", "dough", "batter", "oven",
                 "bake", "baked", "flour", "yeast", "soggy", "sank", "sunken", "lumpy",
                 "curdled", "rise", "risen", "prove", "proofed", "shortcrust", "icing")),
    entry("sleep-latency",
          (("fall asleep", "falling asleep", "get to sleep", "getting to sleep", "nod off",
            "sleeping"),
           ("how long", "long does it", "minutes", "normal", "quickly")),
          "Most people nod off within 10 to 20 minutes of lights out, and 30 minutes or more is "
          "the usual sign of a body clock that is not ready yet: shift your getting-up time "
          "earlier slowly rather than going to bed earlier. Lying there clock-watching makes it "
          "longer, so get up and do something dull for ten minutes and try again.",
          ask=("long", "minutes", "normal", "much", "quickly", "takes"),
          avoid=("plane", "train", "flight", "baby", "toddler", "child", "children", "medicine",
                 "melatonin", "tablet", "tablets", "falling asleep at my desk", "driving",
                 "driving tired", "wheel")),
    entry("sore-throat", (("sore throat", "throat", "tonsils", "swallowing", "hurts to swallow",
                          "hurts when i swallow"),
                          ("hurt", "hurts", "sore", "help", "helps", "soothe", "stop", "painful",
                           "scratchy", "worse", "what", "killing", "kills", "agony", "raw")),
          "Paracetamol or ibuprofen, plenty to drink, honey in warm water and a salt-water gargle "
          "(half a teaspoon in a glass) all ease it, and most sore throats are viral and settle in "
          "three to five days. See a GP if it lasts more than a week, you cannot swallow fluids, or "
          "it comes with a high fever and a stiff neck.",
          ask=("what", "help", "helps", "how", "ease", "soothe", "tip", "tips", "remedy", "stop",
               "painful", "scratchy", "worst", "swallow", "swallowing", "killing", "kills", "agony",
               "raw"),
          avoid=("sing", "singing", "singer", "voice", "lump", "cancer", "hoarse", "shout",
                 "shouting", "atm", "cashpoint", "cash machine", "swallowed my card",
                 "swallowed the card", "ate my card", "kept my card", "card stuck",
                 "sim card", "memory card", "sd card", "gift card", "loyalty card")),
    entry("headache", (("headache", "headaches", "head ache", "my head is banging",
                       "heads banging", "head banging", "head is thumping", "head pounding",
                       "head is pounding", "banging head", "head hurting", "head hurts",
                       "my head hurts"),
                       ("what", "help", "helps", "get rid", "cure", "stop", "painkiller",
                        "worst", "sore", "should i", "anything", "medicine")),
          _headache_reply,
          avoid=("migraine", "migraines", "chest", "child", "baby", "pregnant", "tablet", "tablets",
                 "dose", "doses", "how many", "overdose",
                 "pregnancy", "breastfeeding", "breast feeding", "nursing", "chestfeeding",
                 "expecting", "trimester"),
          bias=2),
    entry("water-with-meals", (("water", "drink", "drinking", "fluids"),
                               ("with meals", "with food", "with my meal", "with a meal",
                                "during meals", "before a meal", "before meals", "after a meal",
                                "after meals", "while eating")),
          "Water with a meal is fine: it does not dilute your stomach acid enough to matter, and "
          "it helps if you eat fast or get constipated. The only thing to watch is filling up on "
          "it so there is no room for the food - a glass or two rather than a pint before you sit "
          "down. Soup, tea and squash count towards the day the same way.",
          avoid=("dog", "dogs", "cat", "cats", "puppy", "kitten", "pet", "pets", "plant", "garden",
                 "tap", "abroad", "holiday"),
          bias=1),
    entry("water-too-much", (("drink", "drinking", "drunk", "thirsty", "thirst", "water"),
                             ("too much", "so much", "stop drinking", "cant stop", "can't stop",
                              "always thirsty", "constantly thirsty", "never quenched",
                              "still thirsty", "all the time")),
          "If you are drinking far more than usual and still thirsty, see a GP: thirst that will "
          "not quench is worth a blood test, because it can be the first sign of diabetes. If it "
          "is just habit, spread the day's drinks out, keep water out of sight between meals, and "
          "sip rather than down a pint at once - but do not ration it, since your body asks for "
          "what it needs.",
          avoid=("dog", "dogs", "cat", "cats", "puppy", "kitten", "pet", "pets", "bowl", "plant",
                 "plants", "garden", "lawn", "tap", "abroad", "holiday", "alcohol", "beer", "wine",
                 "coffee", "before bed", "night")),
    entry("water-intake", (("water", "fluids", "litres", "liters",
                            "hydration",
                            "glasses a day", "glasses a week", "glasses daily"),
                           ("day", "daily", "drink", "drinking", "drinks", "how much",
                            "enough", "more", "forget", "forgetting", "forgot", "remind",
                            "remember", "habit", "keep", "8 glasses", "eight glasses",
                            "glasses of water")),
          "Six to eight glasses a day, about 1.5 to 2 litres, is plenty, and more in heat or after "
          "exercise; tea, coffee, milk, squash and food all count towards it, and pale straw-coloured "
          "urine is the check that you are about right. If you forget, keep a filled bottle where you "
          "sit and drink a glass with every meal.",
          ask=("much", "many", "litres", "liters", "daily", "day", "glasses", "enough",
               "drink more", "more water", "enough water", "should i drink", "forget",
               "forgetting", "forgot", "remind", "remember", "hydrat"),
          avoid=("plant", "plants", "flowers", "garden", "lawn", "turf", "sod", "grass",
                 "seedbed", "tomato", "tomatoes", "seedlings", "houseplant", "houseplants",
                 "where i put my glasses", "where are my glasses", "where my glasses",
                 "left my glasses", "lost my glasses", "find my glasses", "my glasses are",
                 "broke my glasses", "glasses broke", "clean my glasses", "glasses dirty",
                 "glasses are dirty", "smudged", "spectacles", "sunglasses", "reading glasses",
                 "optician", "glasses case", "contact lenses", "new glasses",
                 "losing my glasses", "lose my glasses", "glasses go missing",
                 "forgot my glasses", "forget my glasses", "forgotten my glasses",
                 "keep forgetting my glasses", "steaming up", "steams up", "steam up",
                 "fogging up", "fogs up", "fogged up", "fog up", "lens", "lenses", "specs",
                 "wearing glasses", "wear glasses", "pair of glasses", "glasses are broken",
                 "glasses fell", "sat on my glasses", "glasses slide",
                 "water them", "water it", "water the", "water my", "water your", "water once",
                 "water twice", "water every", "water in the morning", "water in the evening",
                 "water deeply", "feed and water",
                 "hose", "water butt", "water bill",
                 "kettle", "boiler", "bill",
                 "bills", "leak", "leaking", "pool", "swim", "filter", "softener", "bottle",
                 "bottles", "salt", "salting", "boil", "boils", "boiling",
                 "cup of tea", "cups of tea", "pasta", "rice", "pan", "saucepan", "stock",
                 "couscous", "quinoa", "bulgur", "porridge", "oats", "oatmeal", "dough",
                 "batter", "flour", "recipe", "gravy",
                 "baby", "babies", "toddler", "toddlers", "child", "children", "kid", "kids",
                 "infant", "newborn", "year old", "years old", "pregnant", "pregnancy",
                 "breastfeeding", "nursing", "formula",
                 "dog", "dogs", "puppy", "puppies", "cat", "cats", "kitten", "kittens",
                 "pet", "pets", "hamster", "hamsters", "rabbit", "rabbits", "guinea pig",
                 "parrot", "horse", "horses", "litter tray",
                 "before bed", "at night", "before sleeping", "before sleep",
                 "bath", "baths", "bathtub", "shower", "showers", "toilet", "toilets", "flush",
                 "cistern", "bucket", "buckets", "mop bucket", "paddling pool", "hot water bottle",
                 "washing machine", "dishwasher", "tank", "water tank", "hose", "hosepipe",
                 "sprinkler", "watering can",
                 "litre of paint", "litre of petrol", "litre of diesel", "litre of oil",
                 "litre of olive oil", "litre of bleach", "litre of screenwash",
                 "litre of emulsion", "litre of white spirit", "litre of milk",
                 "litre of juice", "litre of beer", "litre of wine")),
    entry("sunscreen", (("sunscreen", "suncream", "sun cream", "spf", "sunblock",
                         "sun protection", "protect my skin", "protect your skin",
                         "protect skin", "skin in the sun", "skin from the sun",
                         "factor 30", "factor 50", "sun factor", "what factor",
                         "which factor", "what spf",
                         "burn", "burns", "burning", "burnt",
                         "burning in the sun", "burn in the sun", "burns in the sun",
                         "burning in sunlight", "face burning", "get burnt", "gets burnt"),                        ("use", "wear", "need", "should", "what", "which", "high", "apply",
                         "reapply", "protect", "choose", "choosing", "best", "buy", "stop",
                         "prevent", "everyday", "day to day", "enough",
                         "face", "skin", "nose", "shoulders", "arms", "chest",
                         "block", "blocks", "blocking", "uv", "uva", "uvb", "work", "works")),
          "Use a broad-spectrum sunscreen of at least SPF 30, with four or five stars for UVA, "
          "and use more than feels right: about two tablespoons for an adult in a costume, "
          "reapplied every two hours and after swimming or sweating. SPF 50 for children, and "
          "sunscreen adds to shade, a hat and a shirt rather than replacing them.",
          guard=lambda understood: (_a_factor_question_without_the_sun(understood)
                                    and _a_burn_without_the_sun(understood)),
          avoid=("common factor", "highest common factor", "isan", "insurance",
                 "tan", "tanning", "tanned", "suntan", "sun tan", "get a tan", "have a tan")),
    entry("sunscreen-expiry",
          (("sun cream", "suncream", "sunscreen", "sunblock", "spf"),
           ("go off", "gone off", "goes off", "out of date", "use by", "expire", "expires",
            "expired", "expiry", "last", "lasts", "keep", "keeps", "shelf life", "old",
            "from last year", "last summer", "still good", "still work")),
          "Sunscreen keeps about three years unopened and about a year once it is open, so write "
          "the month on the bottle when you start it. Out of date it does not turn dangerous, it "
          "just stops protecting as the label says: if it has separated, gone gritty or smells "
          "odd, replace it, and a bottle that has sat in a hot car all summer is the one to bin."),

    entry("cosmetic-lifetime",
          (("moisturiser", "moisturizer", "face cream", "facial cream", "day cream", "night cream",
            "body lotion", "face lotion", "skin cream", "serum", "cleanser", "foundation",
            "makeup", "make up", "mascara", "lipstick", "concealer", "blusher", "blush",
            "eye cream", "hand cream", "body cream", "shaving cream", "spot cream", "nappy cream",
            "eczema cream", "lip balm", "lip salve", "toner", "aftershave"),
           ("go off", "gone off", "goes off", "out of date", "use by", "expire", "expires",
            "expired", "expiry", "last", "lasts", "keep", "keeps", "shelf life", "old",
            "from last year", "still good", "still ok", "still fine", "still alright",
            "still work", "how long",
            "smell", "smells", "smelly", "smells funny", "smells off", "smells odd",
            "smells sour", "separated", "gritty", "gone gritty")),
          "Most creams keep about 30 months sealed and 12 months once they are open, so write the "
          "month you opened it on the jar; a cleanser or a serum is roughly the same, and mascara "
          "is the short one at three months because the wand picks up bacteria. A cream that has "
          "separated, gone gritty or smells sour should go, and anything you would not put on a cut "
          "does not belong on your face."),

    entry("tan-through-glass",
          (("tan", "tanned", "tanning", "a tan", "tan line", "tan lines", "suntan", "sun tan",
            "uv", "uva", "uvb"),
           ("window", "windows", "glass", "car", "car window", "office", "driving", "drive",
            "through", "indoors", "inside", "sunlight", "sun", "block", "blocked", "blocking",
            "protect", "protects")),
          "The UVA that tans and ages skin goes straight through glass, so a day by a window "
          "or a long drive gives you colour and lines, while the UVB that burns is mostly "
          "filtered out. It creeps up on you because you do not feel it getting hot. Glass is not "
          "sun protection, so use SPF 30 on the arm and face nearest the window if you sit there "
          "for hours, and do not treat a sunbed as a shortcut to the same thing.",
          avoid=("sunscreen", "sun cream", "suncream", "spf", "factor", "sunblock", "sunburn",
                 "after sun", "aftersun", "fake tan", "spray tan", "self tan", "false tan",
                 "sunbed", "tanning bed", "tanning shop", "moisturiser", "exfoliate", "streaks",
                 "clean", "cleaning", "cleaner", "smear", "smears", "dust", "dusty", "dirty",
                 "squeegee", "windscreen", "wipers", "condensation", "double glazing", "glazier",
                 "insulate", "insulation", "curtains", "blinds", "replace", "repair", "cracked",
                 "broken", "lamp", "nails", "filter", "purifier", "sparkle", "vinegar")),
    entry("sunbed-risk",
          (("sunbed", "sunbeds", "tanning bed", "tanning beds", "tanning salon", "tanning shop",
            "uv bed", "fake tan bed"),
           ("safe", "bad", "harm", "harmful", "risk", "risks", "cancer", "ok", "worth",
            "healthy", "damage", "how often", "should i", "is it")),
          "No: a sunbed gives out mostly UVA, the ray that ages skin and drives melanoma, in doses "
          "several times stronger than midday sun, and using one before 35 raises the melanoma "
          "risk by around three quarters. Under-18s are banned from them in the UK. A spray tan or "
          "a gradual self-tan gives the same colour without the damage.",
          avoid=("window", "glass", "bed size", "bed sheets", "mattress", "sleep")),
    entry("freckles", (("freckle", "freckles", "freckled"), ("why", "get", "have", "sun", "skin",
                                                             "cause", "appear")),
          "Freckles are clumps of the brown pigment melanin that your skin makes in response to "
          "sun, so they show up most on fair skin in summer and fade in winter. They are harmless, "
          "and the fairer your skin the more carefully you need to cover up: sunscreen and a hat "
          "stop new ones and protect against sun damage."),
    entry("cut-or-crush-a-tablet",
          (("tablet", "tablets", "pill", "pills", "capsule", "capsules", "medicine", "medication",
            "paracetamol", "ibuprofen", "antibiotic", "antibiotics"),
           ("crush", "crushed", "crushing", "split", "splitting", "break", "breaking", "broken",
            "cut", "cutting", "halve", "halved", "half", "in half", "in two", "swallow",
            "break a tablet", "break a pill", "break my tablet", "break my pill",
            "break the tablet", "break the pill", "break it in half", "cut a tablet",
            "cut a pill", "split a tablet", "split a pill", "split the tablet",
            "swallowing", "dissolve", "chew", "chewed", "grind", "open the capsule")),
          "Check the box first: if it says modified release, extended release, MR, XL or SR, or "
          "that the tablet is film-coated or a capsule, do not crush, split or open it - the whole "
          "dose comes out at once. An ordinary plain tablet can usually be broken along the score "
          "line, or crushed and taken in water or yoghurt. Ask a pharmacist for the same medicine "
          "as a liquid or a dispersible tablet; they do that most days and it costs nothing to ask.",
          avoid=("overdose", "too many", "took too much", "swallowed the pack", "suicide", "harm",
                 "child", "children", "toddler", "baby", "kid", "kids", "son", "daughter",
                 "cant swallow", "can't swallow", "cannot swallow", "too big", "stuck", "choking",
                 "throat", "tablet stuck", "side effect", "side effects", "contraceptive",
                 "pill free week", "morning after", "antibiotic course", "dose", "dosage")),
    entry("earwax", (("earwax", "ear", "ears"),
                     ("blocked", "block", "clean", "cleaning", "remove", "build up", "cotton",
                      "buds", "bud", "plug", "plugged",
                      "out", "get wax out", "full of wax", "drops", "soften", "syringed",
                      "microsuction", "syringe", "clear",
                      "wax", "waxing")),
          "Leave earwax alone: it works its way out, and cotton buds push it back and pack it "
          "against the eardrum. If it blocks your hearing, a pharmacist can sell you olive or "
          "sodium bicarbonate drops for a week; if that does not shift it, a nurse can syringe or "
          "microsuction it. Never put anything smaller than your elbow in your ear.",
          ask=("blocked", "block", "clean", "cleaning", "remove", "wax", "cotton", "buds", "plugged",
               "build", "out", "drops", "soften", "full of wax", "syringe", "clear"),
          avoid=("phone", "earphones", "headphones", "buds in", "airpods", "ringing", "infection",
                 "table", "tables", "tablecloth", "floor", "carpet", "wood", "wooden",
                 "furniture", "worktop", "skirting", "cloth", "fabric")),
    entry("bloating", (("bloating", "bloated", "wind", "windy", "trapped wind", "fart",
                        "farting",
                        "gut", "guts", "my gut"),
                       ("after", "meals", "eating", "help", "stop", "reduce", "get rid", "why",
                        "always", "much",
                        "all the time", "constantly", "every day", "most days", "for weeks",
                        "feels", "feel", "stomach", "tummy", "belly",
                        "settle", "calm", "sort") + ASK_ABOUT + IMPROVE),
          "Most bloating is gas and fluid moving slowly: eat more slowly, drink less fizzy stuff, "
          "and try cutting back on one thing at a time for a fortnight, usually fizzy drinks, "
          "chewing gum, or a big jump in fibre. A daily walk helps, and peppermint tea or capsules "
          "settle wind for many people. See a GP if you are bloated most days for weeks, lose "
          "weight without trying, or have blood in your stool.",
          avoid=("door", "doors", "gate", "gates", "window", "windows", "latch", "hinge",
                 "draught", "draft", "slam", "slamming", "bang", "banging", "cupboard",
                 "drawer", "radiator", "pipe", "pipes", "trampoline", "flag",
                 "gut feeling", "gut instinct", "trust my gut", "trusted my gut", "beer gut",
                 "gut the", "gut a", "gut reaction",
                 "fence", "fences", "roof", "roofs", "tree", "trees", "garden", "kite",
                 "sail", "sailing", "storm", "storms", "gale", "weather",
                 "better today", "better now", "is better now", "is much better", "much better",
                 "feels better", "feeling better", "gut is better", "getting better")),
    entry("eyes-test", (("eye test", "eyes test", "eyes tested", "eye exam", "optician",
                         "eyes checked", "get my eyes", "sight test", "sight check",
                         "eyesight test", "eye health check", "sight tests"),
                        ("often", "how often", "regular", "should", "need", "due", "when",
                         "free", "cost", "how much", "time")),
          _eyes_test,
          ask=("often", "when", "should", "need", "due", "free", "cost", "regular", "how much"),
          bias=3,
          avoid=("how much", "cost of", "price", "prices", "cheapest", "afford",
                 "dry eyes", "dry eye", "sore eyes", "red eyes", "itchy eyes", "stye",
                 "conjunctivitis", "contacts", "contact lens", "contact lenses", "glasses",
                 "scratched", "laser", "cataract", "floaters",
                 "child", "children", "kids", "kid", "son", "daughter", "toddler", "baby",
                 "school", "squint", "squinting", "year old", "years old")),
    entry("toothache-weekend", (("toothache", "tooth ache", "tooth hurts", "tooth is killing",
                                 "dental", "dentist"),
                                ("weekend", "dentist is shut", "shut", "closed", "out of hours",
                                 "emergency", "cant get", "can't get", "night", "help",
                                 "what do i do", "do i do")),
          "Ring 111 for the out-of-hours dental service: they can book you an urgent appointment "
          "at a surgery that is open, and they can prescribe antibiotics if the tooth is infected. "
          "Until then, take ibuprofen or paracetamol as the packet says, keep the mouth clean, and "
          "do not put aspirin next to the gum. Swelling that closes the eye, a fever or trouble "
          "swallowing is a hospital job, so ring 999 or go to A&E.",
          ask=("what do i do", "weekend", "shut", "closed", "out of hours", "help",
               "cant get", "can't get", "night", "emergency"),
          avoid=("wisdom tooth extraction", "braces", "whitening", "veneer", "implant",
                 "how much does", "cost of", "price")),
    entry("toothbrush-change", (("toothbrush", "toothbrushes", "electric toothbrush",
                                "brush head", "brush heads"),
                               ("change", "changing", "replace", "new one", "often", "long",
                                "when", "how often", "should i")),
          "Change it every three months, or sooner if the bristles splay: a worn brush cleans "
          "much less well. Electric brush heads are the same, rinsing it after use and letting it "
          "dry upright, and swap it after any illness if it has been in a shared pot."),
    entry("caffeine-limit", (("caffeine", "coffee", "coffees", "espresso", "energy drinks",
                              "tea", "teas"),
                             ("much", "too", "limit", "safe", "how many", "too much",
                              "day", "week", "cups", "daily", "weekly")),
          _the_limit_for_the_drink_named,
          ask=("much", "too", "limit", "safe", "many", "day", "week", "cups", "daily",
               "weekly"),
          avoid=("plant", "plants", "grounds", "garden", "compost", "coffee table", "machine",
                 "mug", "shop", "cafe", "pod", "pods", "stain", "stains", "kettle",
                 "tea bag", "tea bags", "leaves",
                 "weak", "watery", "bitter", "sour", "strong", "stronger", "taste", "tastes",
                 "tasting", "brew", "brewing", "brewed", "stewed", "grind", "grinder", "strength",
                 "pregnant", "pregnancy",
                 "spend", "spends", "spent", "spending", "cost", "costs", "buy", "buys",
                 "buying", "price", "prices", "expensive", "afford", "budget", "money",
                 "a year", "per year", "a month", "save", "saving", "savings",
                 "how much water", "water for", "how many cups of water",
                 "sat down with", "sitting with", "over a cup of", "over a mug of",
                 "cup of tea and a", "cuppa and a", "sipping", "sipped",
                 "sugar", "sugars", "sugary", "calorie", "calories", "kcal", "milkshake",
                 "made", "cooked", "leftover", "leftovers", "left over", "freeze", "fridge",
                 "reheat", "keeping", "keep it",
                 "to make", "should i make", "for 4", "for 6", "for 8", "for 20", "per person",
                 "child", "children", "kid", "kids", "son", "daughter", "toddler", "baby",
                 "year old", "years old", "teen", "teenager", "teenagers", "school",
                 "people", "cafetiere", "jug", "tablespoon", "tablespoons", "ground coffee",
                 "mugs", "per mug", "per cup", "mug of")),
    entry("cola-caffeine-limit",
          (("cola", "coca cola", "pepsi", "fizzy drink", "fizzy drinks", "diet coke"),
           ("much", "too", "limit", "safe", "how many", "too much", "day", "week", "cans",
            "daily", "weekly")),
          _CAFFEINE_LEAD["cola"] + _CAFFEINE_TAIL,
          ask=("much", "too", "limit", "safe", "many", "day", "week", "cans", "daily",
               "weekly"),
          avoid=("child", "children", "kid", "kids", "son", "daughter", "toddler", "baby",
                 "year old", "years old", "teen", "teenager", "pregnant", "pregnancy",
                 "stain", "stains", "teeth", "tooth", "sugar", "calories", "plant", "plants",
                 "cake", "ham", "chicken", "rum", "vodka", "whisky", "whiskey", "mixer",
                 "diet", "recipe", "bottle", "bottles", "price", "cost", "buy")),

    entry("caffeine-kids",
          (("caffeine", "coffee", "coffees", "tea", "teas", "cola", "energy drinks",
            "energy drink", "fizzy"),
           ("child", "children", "kid", "kids", "son", "daughter", "toddler", "baby",
            "year old", "years old", "teenager", "teenagers", "teen", "school")),
          "Children under 12 are better off with no caffeine at all: a small body clears it "
          "slowly, so a can of cola at lunch can still be keeping a seven-year-old awake at ten. "
          "Teenagers should stay under about 100mg a day - one coffee, or two cans of cola - and "
          "none after early afternoon. Energy drinks are the usual culprit and a big can is "
          "160mg or more, so they are worth a firm no under 16, and none of it replaces sleep.",
          avoid=("plant", "plants", "grounds", "garden", "compost", "coffee table", "mug",
                 "pod", "pods", "stain", "stains", "kettle", "brew", "brewing", "taste",
                 "tastes", "bitter", "sour", "machine", "shop", "cafe")),
    entry("mountains-form",
          (("mountain", "mountains", "mountain range", "himalayas", "alps"),
           ("form", "formed", "forming", "made", "make", "created", "created", "grow", "grown",
            "how", "why", "build", "built")),
          "Most mountains are made by two plates of the earth's crust pushing together, which folds "
          "and crumples the rock into ranges like the Himalayas and the Alps. Others are volcanoes "
          "piled up by eruptions, or blocks of crust lifted along a fault, like the Sierra Nevada.",
          avoid=("highest", "tallest", "everest", "oldest", "biggest", "longest", "climb",
                 "climbing", "cold", "snow", "altitude", "height", "how high", "steps",
                 "stairs", "staircase")),
    entry("what-is-a-calorie", (("calorie", "calories", "kcal", "kilocalorie", "kilocalories"),
                                ("what is", "whats", "what are", "mean", "meaning", "define",
                                 "explain", "actually")),
          "A calorie is a unit of energy - the heat that raises 1 gram of water by 1 degree "
          "Celsius - and the calories on a food label are really kilocalories, a thousand of "
          "those each. Most adults need around 2,000 to 2,500 of them a day, and a pound of body "
          "fat holds about 3,500.",
          ask=("what", "mean", "meaning", "define", "explain", "tell me about")),

    entry("what-water-is", (("water",), ("what is water", "whats water", "made of", "made from",
                                        "made out of", "h2o", "chemical formula",
                                        "what are water")),
          _WHAT_WATER_IS,
          avoid=("boil", "boiling", "kettle", "bill", "meter", "bottle", "drink", "drinking",
                 "plant", "plants", "water the", "leak", "leaking", "shower", "bath", "tap",
                 "filter", "softener", "hard water", "salt water", "sea", "swim", "swimming",
                 "pool", "weight", "litre", "litres", "glasses", "dehydrated", "hydration"),
          ask=("what", "why", "made", "h2o", "formula"),
          guard=_water_is_the_subject,
          bias=2),
    entry("water-boiling", (("boiling point", "boils", "boil"), ("water", "temperature",
                                                                "degrees", "celsius",
                                                                "fahrenheit", "what", "at")),
          "Water boils at 100C (212F) at sea level, and the boiling point drops as you go up: "
          "about 95C in Denver or Mexico City, and 71C on the summit of Everest, which is why "
          "tea brews badly up there.",
          avoid=("egg", "eggs", "pasta", "rice", "potato", "potatoes", "kettle", "vegetables",
                 "cook", "cooking", "saucepan", "pan", "how long", "soft", "hard",
                 "my hand", "my hands", "my arm", "my arms", "my foot", "my feet", "my leg",
                 "my legs", "my skin", "my face", "my finger", "my fingers", "on my",
                 "hand in", "arm in", "foot in", "scald", "scalded", "scalding", "splashed",
                 "spilt", "spilled", "poured",
                 "about a boil", "a boil on", "my boil", "squeeze", "squeezing", "pop a",
                 "popping", "pus", "abscess", "carbuncle", "flannel", "dressing", "sore",
                 "notice", "alert", "tap", "do not drink", "safe to drink")),
    entry("water-freezing", (("freezing point", "freezes", "freeze", "ice"),
                             ("water", "temperature", "degrees", "celsius", "fahrenheit", "what",
                              "slippery", "slippy")),
          _freezing_point,
          avoid=("pipes", "pipe", "boiler", "fridge", "freezers", "food", "meat", "chicken",
                 "milk", "bread", "defrost", "thaw", "bedroom", "house", "flat", "home",
                 "heating", "radiator", "indoors", "inside the house", "at night",
                 "black ice"),
          ask=("water", "temperature", "degrees", "celsius", "fahrenheit", "freezing point",
               "slippery", "slippy", "zero")),
    entry("ice-freezing-time", (("ice", "ice cube", "ice cubes", "freeze", "freezes",
                                 "freezing", "frozen"),
                                ("how long", "long", "take", "takes", "taking", "time",
                                 "hours", "hour", "quick", "quickly", "fast", "soon")),
          "About 3 to 4 hours for a tray of ice cubes in a freezer set to -18C, two hours for a "
          "thin layer of water in a shallow tray, and overnight for a deep tub. Smaller, flatter "
          "and colder all freeze faster, so an empty freezer beats a full one.",
          ask=("how long", "long", "take", "takes", "time", "hours", "hour", "quick",
               "quickly", "fast", "soon"),
          bias=1,
          avoid=("temperature", "degrees", "celsius", "fahrenheit", "slippery", "slippy",
                 "melts", "melt", "melting", "thaw", "defrost", "defrosting", "refreeze",
                 "re-freeze", "food", "meat", "chicken", "beef", "pork", "fish", "milk",
                 "bread", "cake", "cakes", "dough", "pastry", "rice", "soup", "stew",
                 "fridge", "pipes", "pipe", "boiler", "windscreen",
                 "my feet", "my foot", "my toes", "my hands", "my hand", "my fingers", "my finger",
                 "feet", "foot", "toes", "toe", "hands", "hand", "fingers", "finger",
                 "always cold", "freezing all", "i am freezing", "im freezing", "i feel freezing",
                 "car", "road", "roads", "grit", "salt", "black ice", "pond", "lake",
                 "leaves", "lawn", "hose", "tap", "milk bottle",
                 "ice cream", "ice pack", "ice packs", "ice bath", "ice rink",
                 "keep", "keeps", "keeping", "kept", "last", "lasts", "lasting", "stay", "stays",
                 "store", "stores", "storing", "stored", "can i freeze", "can you freeze",
                 "can i keep", "how long can i", "how long can you",
                 "cook", "cooking", "cooked", "oven", "bake", "baking", "roast", "grill",
                 "grilled", "air fryer", "air fry", "airfryer", "air fried", "microwave",
                 "microwaved", "boil", "boiled", "fry", "fries", "fried", "frying", "reheat",
                 "reheated", "ready meal", "nuggets", "fish fingers", "sausages", "pie", "pizza",
                 "yorkshire", "toast", "chips", "wedges", "peas", "spinach", "berries",
                 "prawns", "veg", "vegetables", "defrost in the microwave",
                 "stock", "stocks", "broth", "bouillon")),
    entry("ice-keeping", (("ice", "ice cube", "ice cubes", "cubes"),
                          ("keep", "keeps", "keeping", "kept", "store", "stores", "storing",
                           "stored", "last", "lasts", "how long", "months")),
          "Ice cubes keep for months in a sealed bag or box, but they pick up freezer smells "
          "within a few weeks, and they shrink and go cloudy as the ice slowly turns to vapour. "
          "Seal the tray's cubes in a bag, use them within about three months, and bin any that "
          "smell of the freezer - ice takes on the smell of whatever is next to it.",
          avoid=("take", "takes", "quick", "quickly", "fast", "soon", "temperature", "degrees",
                 "meat", "chicken", "fish", "peas", "spinach", "berries", "mince", "prawns",
                 "chips", "bread", "cake", "rice", "soup", "milk", "veg", "food", "cream",
                 "lollies", "defrost", "melting", "melt", "slippery", "lolly", "sorbet",
                 "ice pack", "ice packs", "ice bath", "ice rink", "bag of ice for a bruise",
                 "stock", "stocks", "broth", "bouillon"),
          bias=1),
    entry("planets-count", (("planet", "planets"), ("how many", "solar system", "there",
                                                    "eight")),
          "There are eight planets: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus and "
          "Neptune. Pluto was reclassified as a dwarf planet in 2006, which is why the number "
          "went down from nine.",
          ask=("how many", "number", "count", "solar system"),
          bias=2),
    entry("hottest-planet", (("planet", "planets", "venus", "mercury"), ("hottest", "hot",
                                                                       "hotter", "warmest")),
          "Venus is the hottest planet, around 465C, and it is hotter than Mercury even though "
          "Mercury is closer to the Sun: Venus is wrapped in a thick carbon dioxide atmosphere "
          "that traps the heat.",
          ask=("hottest", "hotter", "warmest", "which", "why")),
    entry("biggest-planet", (("planet", "planets", "jupiter"),
                              ("biggest", "largest", "bigger", "big", "size")),
          "Jupiter is the biggest planet: about 143,000 km across, or 11 Earths side by side, and "
          "more than twice as massive as all the other planets put together. It is a gas giant "
          "with no solid surface to stand on.",
          ask=("biggest", "largest", "bigger", "which", "what"),
          avoid=("model", "project", "cake", "hot", "hottest", "hottest planet", "temperature"),
          bias=3),
    entry("who-discovered", (("who",), ("discovered", "found out", "worked out")),
          who_discovered,
          avoid=("pregnant", "i was", "she was", "he was", "that", "this")),

    entry("periodic-table", (("periodic table", "periodic", "first 20 elements",
                              "first twenty elements"),
                             ("what", "remember", "memorise", "memorize", "learn", "elements",
                              "first 20", "how", "who", "invented", "made", "mendeleev",
                              "groups", "columns", "rows", "school", "gcse")),
          "There are 118 elements in order of atomic number, and Mendeleev put the first table "
          "together in 1869 leaving gaps for elements nobody had found yet. For school you need "
          "the first 20 by heart: hydrogen, helium, lithium, beryllium, boron, carbon, nitrogen, "
          "oxygen, fluorine, neon, sodium, magnesium, aluminium, silicon, phosphorus, sulfur, "
          "chlorine, argon, potassium, calcium. Learn the columns rather than the rows: a column "
          "is a family that behaves alike, which is why sodium and potassium both fizz in water."),
    entry("painkillers-together-safe",
          (("paracetamol", "acetaminophen", "ibuprofen", "painkiller", "painkillers", "nurofen",
            "co-codamol"),
           ("together", "at the same time", "same time", "both", "alternate", "alternating",
            "with each other", "and ibuprofen", "plus ibuprofen", "and paracetamol",
            "with paracetamol", "with ibuprofen", "with nurofen", "with co-codamol",
            "ibuprofen with paracetamol", "paracetamol with ibuprofen",
            "ibuprofen and paracetamol", "paracetamol and ibuprofen")),
          "Yes - paracetamol and ibuprofen work in different ways, so you can take both, and "
          "alternating them is what people often do for a bad headache, toothache or a bad back. "
          "Keep to the box: two 500mg paracetamol up to four times a day, at least four hours "
          "apart and no more than eight in 24 hours, and 400mg of ibuprofen three times a day "
          "with food. Skip ibuprofen if you have a stomach ulcer, kidney trouble or are on a "
          "blood thinner, and read the labels of anything else you take - a lot of cold remedies "
          "already contain paracetamol.",
          ask=("can i", "should i", "is it", "does it", "do i", "ok", "safe", "okay", "better"),
          avoid=("baby", "babies", "newborn", "infant", "calpol",
                 "alcohol", "drink", "drinking", "beer", "wine", "pint", "pints", "hangover",
                 "booze", "blood thinner", "thin your blood", "thins the blood", "warfarin",
                 "sleepy", "drowsy", "drowsiness", "how long", "take to work", "kick in",
                 "stomach", "ulcer",
                 "antibiotic", "antibiotics", "pregnant", "pregnancy", "breastfeeding",
                 "empty stomach", "before or after food", "with food", "without food",
                 "with a meal", "before food", "after food", "eat with", "eat before",
                 "need to eat", "have to eat")),
    entry("eye-test-frequency",
          (("eye test", "eye tests", "eyes tested", "eyesight test", "sight test", "optician",
            "optometrist", "glasses"),
           ("how often", "how frequently", "when should", "frequency", "overdue", "need",
            "free", "regular", "every")),
          "Every two years is the usual answer for an adult, and every year once you are over 70 "
          "or if you are diabetic or have glaucoma in the family. In Scotland, Wales and Northern "
          "Ireland the sight test is free on the NHS; in England it is free if you are under 16, "
          "over 60, diabetic, on certain benefits or have a close relative with glaucoma, and "
          "otherwise it is usually around £25 - worth it, because the test spots glaucoma and "
          "diabetes changes years before you would notice them.",
          avoid=("last", "remember", "headache", "headaches", "migraine", "migraines", "dog",
                 "cat",
                 "child", "children", "kids", "kid", "son", "daughter", "toddler", "baby",
                 "school", "squint", "squinting")),
    entry("swallow-a-tablet",
          (("tablet", "tablets", "pill", "pills", "capsule", "capsules", "medicine"),
           ("too big", "swallow", "swallowing", "cant swallow", "can't swallow",
            "cannot swallow", "hard to swallow", "stuck", "trouble swallowing")),
          "Take a mouthful of water first, put the tablet on your tongue, then drink from a "
          "bottle or through a straw - and tip your head the right way: a tablet is denser than "
          "water so it sinks, so tilt your head back, while a capsule floats, so tip your chin "
          "down. Swallowing with a mouthful of yoghurt or a soft banana hides the shape. If it "
          "is still hard, ask the pharmacist for a liquid, a dispersible or a smaller tablet, but "
          "never crush or split one that says not to - some are slow release.",
          avoid=("dog", "cat", "puppy", "kitten", "pet", "horse")),
    entry("cold-vs-flu",
          (("cold", "colds", "flu", "influenza"),
           ("same", "difference", "different", "same thing", "worse", "which is", "or is it",
            "twice", "again", "still get")),
          "A cold stays in the nose and throat: a runny nose, sneezing, a sore throat, and you "
          "can still get up and work. Flu comes on in hours with a fever, aching limbs and being "
          "flattened in bed, and the cough and the tiredness can drag on for two or three weeks. "
          "You can get flu more than once, because each season has different strains - that is "
          "why the jab changes every year - and a cold is a different family of viruses again.",
          bias=1,
          lead=("yesno", _cold_or_flu_verdict)),
    entry("cold-duration-cough",
          (("cold", "colds", "a cold", "sniffles", "runny nose"),
           ("how long", "last", "lasts", "go away", "gone", "over it", "weeks", "still",
            "go", "going")),
          "A cold usually peaks in two or three days and is gone in about a week, though a cough "
          "and a blocked nose can linger for two weeks and that is normal. Rest, plenty of fluid "
          "and paracetamol for the ache are the treatment; antibiotics do nothing for a virus. "
          "See a GP if it lasts more than three weeks, if you are breathless or wheezing, or if "
          "a child is drinking less and has a fever that will not come down.",
          bias=1,
          avoid=("sore", "sores", "hands", "feet", "fingers", "toes", "war", "country",
                 "mottled", "clammy", "grey", "gray", "ashen", "white as a sheet",
                 "blue round the lips", "blue lips",
                 "countries", "weather", "room", "water", "outside", "garden", "morning",
                 "too cold to", "too cold for", "cold enough", "cold outside", "out in the cold",
                 "bike", "bikes", "bicycle", "cycle", "cycling", "ride", "walk", "walking",
                 "hike", "picnic", "barbecue", "bbq", "parasol", "washing", "laundry",
                 "line", "dog", "dogs", "baby out", "pram", "buggy",
                 "beer", "lager", "wine", "milk", "juice", "brew", "coffee", "tea", "fridge", "freezer",
                 "freeze",
                 "leftovers", "leftover", "food", "meat", "chicken", "rice", "pasta", "cake",
                 "bread", "eggs", "egg", "cheese", "yoghurt", "yogurt", "opened", "unopened",
                 "school", "nursery", "off school", "dog", "cat", "puppy", "kitten",
                 "radiator", "radiators", "rads", "heating", "central heating",
                 "boiler", "hot water", "hot tap", "hot taps", "thermostat", "immersion",
                 "towel rail", "pipe", "pipes",
                 "pack", "packing", "packed", "suitcase", "luggage", "hand luggage",
                 "handbag", "backpack", "rucksack", "carry on", "wear", "wearing",
                 "clothes", "layers",
                 "can i still", "can i run", "can i train", "can i exercise", "can i swim",
                 "can i go to the gym", "should i run", "should i train", "should i exercise",
                 "run with", "running with", "train with", "training with", "exercise with",
                 "still run", "still train", "still play", "still swim", "still cycle",
                 "go running", "go for a run", "work out", "workout", "gym",
                 "running", "swim", "swimming", "cycle", "cycling", "football", "netball",
                 "hockey", "training",
                 "radiator", "radiators", "boiler", "heating", "thermostat", "shower", "tap",
                 "hot water", "washing machine", "dishwasher", "kettle", "oven", "fridge",
                 "freezer", "car", "engine", "bath water", "hot tub", "shed", "greenhouse",
                 "appliance", "furnace", "heat pump",
                 )),
    entry("five-a-day-grams",
          (("5 a day", "five a day", "five portions", "fruit and veg", "fruit and vegetables",
            "smoothie", "smoothies", "juice"),
           ("count", "counts", "really", "thing", "true", "enough", "portion", "portions",
            "what counts", "does it")),
          "Five a day is real, and it is about 400g of fruit and vegetables rather than five "
          "items: a portion is 80g, which is one apple, three heaped tablespoons of peas, or a "
          "handful of grapes. A smoothie counts once however much of it you drink, and so does a "
          "150ml glass of juice, because the fibre is broken up and it goes down too fast - "
          "whole fruit is better. Potatoes, chips and crisps do not count: they are the "
          "carbohydrate on the plate.",
          bias=1),
    entry("night-snacking",
          (("snack", "snacks", "snacking", "crisps", "biscuits", "chocolate"),
           ("night", "nights", "evening", "evenings", "late", "bed", "bedtime", "stop",
            "habit", "why", "midnight")),
          "Evening snacking is usually a habit loop rather than hunger: it starts with being "
          "tired, bored or in front of a screen, and it is the cue you have to change. Brush "
          "your teeth straight after dinner, keep food out of the living room, and make dinner "
          "big enough and with enough protein and fibre that you are not catching up at ten. If "
          "you know you will want something, plan it - a yoghurt or a bowl of cereal at nine, "
          "eaten sitting down, beats an unplanned raid at eleven.",
          avoid=("toddler", "baby", "child", "children", "kids", "dog", "cat", "puppy",
                 "lunch", "school", "party")),
    entry("cold-and-school",
          (("cold", "cough", "sniffles", "runny nose"),
           ("school", "nursery", "off school", "go to school", "keep her off", "keep him off",
            "keep my kid off", "keep them off", "send her", "send him")),
          "A cold with no fever, and a child who is eating and drinking, is fine for school - a "
          "runny nose on its own is not a reason to stay off. Keep her home if she has a "
          "temperature, is too tired or clingy to join in, is being sick, or has a cough that "
          "leaves her breathless or wheezing. Send tissues and tell the teacher, and let her go "
          "back once the fever has been gone for 24 hours without medicine; the cough can hang "
          "on for a week or two after that and does not need another day off."),
    entry("flu-recovery",
          (("flu", "influenza", "virus", "cold"),
           ("last", "how long", "tired", "exhausted", "fatigue", "weeks", "recover", "recovery",
            "better", "still", "ache", "aches", "weak", "knackered")),
          "Flu usually hits hardest for two or three days and is mostly gone in a week, but a "
          "cough and a flat, tired feeling can drag on for two or three weeks, and that is normal. "
          "Sleep as much as your body asks for, drink more than you think you need, and go back to "
          "work or training gently. See a doctor if you are breathless, have chest pain, a fever "
          "past five days, or are still exhausted after a month.",
          avoid=("antibiotic", "antibiotics", "penicillin", "covid", "test", "vaccine", "vaccines",
                 "beer", "lager", "ale", "stout", "cider", "wine", "fridge", "bottle", "bottles",
                 "opened", "unopened",
                 "jab", "jabs", "baby", "babies", "toddler", "child", "children", "pregnant",
                 "temperature", "rash", "vomiting", "diarrhoea",
                 "can i still", "can i run", "can i train", "can i exercise", "can i swim",
                 "can i go to the gym", "should i run", "should i train", "should i exercise",
                 "run with", "train with", "exercise with", "gym", "running", "swim",
                 "swimming", "football", "training")),
    entry("eggs-daily", (("egg", "eggs"), ("every day", "daily", "too many", "ok", "okay", "fine",
                                           "safe", "healthy", "bad", "cholesterol", "harm")),
          "An egg a day is fine for most people: the cholesterol in food moves blood cholesterol "
          "far less than saturated fat does, which is the butter you cook it in. An egg gives "
          "cheap protein, vitamin D and B12. Two a day is still reasonable for a healthy adult; "
          "if you have heart disease or diabetes, ask your GP what suits you.",
          avoid=("dog", "cat", "puppy", "kitten", "bird", "chicken", "hatch", "boil", "boiled",
                 "poach", "scramble", "fry", "frying", "recipe", "bake", "baking", "cake",
                 "cook", "cooked", "yolk", "white", "shell", "go off", "gone off", "fresh",
                 "date", "dates", "use by", "best before", "out of date", "expired", "expiry",
                 "crack", "cracked", "cracks")),
    entry("nail-biting-habit", (("nail biting", "bite my nails", "biting my nails", "biting nails",
                           "chew my nails", "chewing my nails", "bitten nails", "nail biter"),
                          ("stop", "stopping", "how", "habit", "quit", "break", "help")),
          "Nail biting is a habit that turns up when you are bored, tense or concentrating, so "
          "give the hand something else to do: keep nails short and filed, hold a pen or a ring "
          "of putty, and try a bitter polish for a month. Many people beat it, and most of the "
          "way is noticing the moment rather than forcing it.",
          bias=2),
    entry("cold-hands", (("hands", "hand", "fingers", "fingertips", "raynauds", "raynaud",
                          "raynaud's", "feet", "foot", "toes", "toe"),
                         ("cold", "freezing", "freeze", "always", "white", "blue", "purple",
                          "circulation", "winter", "help", "helps", "worse", "feet", "toes",
                          "warm", "warmer", "warmth", "warmish", "toasty")),
          "Cold hands and feet are usually just circulation: the body pulls blood in from the "
          "skin when you are cold. Warm the whole body, not just the hands - gloves, thick socks, a "
          "hat, a warm drink - and flex the fingers and toes. White, then blue, then red and "
          "painful in the cold is Raynaud's, and "
          "keeping the wrists warm helps. See a GP if it is one hand only, or comes with "
          "tiredness or weight change.",
          avoid=("burn", "burnt", "scald", "swollen", "swelling", "rash", "itch", "numb since",
                 "fell", "cut", "wound", "broken", "baby", "babies", "child", "children", "kid",
                 "kids", "pins and needles",
                 "bedroom", "bedrooms", "living room", "room", "rooms", "house", "home", "flat",
                 "oven", "cook", "cooking",
                 "catching colds", "catch colds", "keep getting colds",
                 "got a cold", "have a cold", "had a cold", "cold after cold", "a cold and",
                 "wash my hands", "washing my hands", "handwashing", "hand washing",
                 "sore throat", "flu", "virus", "viruses",
                 "cold feet about", "cold feet over", "cold feet before"),
          ask=("cold", "freezing", "numb", "white", "blue", "circulation", "raynauds",
               "raynaud", "warm", "warmer", "warmth", "toasty")),

    entry("cold-feet-nerves", (("cold feet", "cold foot"),
                               ("about", "over", "before", "getting", "got", "gotten",
                                "wedding", "married", "marrying", "interview", "move",
                                "moving", "exam", "flight", "driving test", "second thoughts")),
          "Nerves before something big are normal. Slow breaths for a minute genuinely help, "
          "and so does saying the worry out loud to one person: what is it that the day itself "
          "might bring? Cold feet before a wedding, a move or an interview are usually the size "
          "of the change rather than a warning about it, so give it a night before you act on it "
          "- and if it is a promise you are not sure you want, that is worth talking through "
          "properly, with the person if you can.",
          avoid=("feet are", "feet get", "feet go", "feet feel", "feet were", "hands and feet",
                 "bed", "night", "nights", "winter", "morning", "evening", "weather",
                 "cold day", "when", "whenever", "always", "all day", "all the time", "toes",
                 "toe", "raynauds", "raynaud", "socks", "slippers", "gloves", "duvet",
                 "blanket"),
          bias=2),

    entry("teen-sleep", (("teenager", "teenagers", "teen", "teens", "puberty", "adolescent",
                          "adolescents"),
                         ("sleep", "sleepy", "tired", "late", "wake", "waking", "morning",
                          "night", "owl", "bedtime")),
          "In the teen years the body clock shifts later by up to two hours, so a teenager really "
          "is not sleepy at 10pm and cannot wake at 7am. It is biology, not laziness: keep a "
          "steady wake time, get morning daylight and dim screens late, and aim for 8 to 10 hours. "
          "Tiredness that persists with low mood, or falling asleep in class, is worth a GP visit.",
          ask=("why", "what", "how", "cause", "always", "help", "should"),
          avoid=("baby", "babies", "toddler", "child", "children", "dog", "cat")),
    entry("caffeine-awake", (("caffeine", "coffee", "espresso", "energy drink", "energy drinks",
                              "tea", "cola", "coke"),
                             ("awake", "wake", "wakes", "waking", "wired", "insomnia", "sleep",
                              "sleeping", "keep me awake", "keeps me awake", "stops me sleeping",
                              "stop me sleeping", "can't sleep", "cant sleep", "late", "night")),
          "Caffeine blocks adenosine, the molecule that builds up through the day and makes you "
          "sleepy, so it hides tiredness rather than removing it. Its effect lasts about five "
          "hours: have your last coffee by early afternoon, and cut down slowly to avoid headaches.",
          ask=("why", "what", "how", "cause", "keep", "stop", "can't", "cant",
                "does", "can"),
          avoid=("much", "limit", "safe", "many", "pregnant", "pregnancy", "plant", "plants",
                 "grounds", "compost", "stain", "stains", "table", "mug", "pod", "pods"),
          bias=2),
    entry("earworm", (("earworm", "earworms", "song stuck", "songs get stuck", "song gets stuck",
                       "tune stuck", "tunes get stuck", "tune gets stuck", "music stuck",
                       "song in my head", "tune in my head"),
                      ("why", "what", "stuck", "head", "get rid", "stop", "how", "happen")),
          "A catchy piece with a simple shape and a repeated phrase loops because the brain "
          "predicts the next note and keeps replaying the bit it knows. Chewing gum, singing the "
          "song all the way through, or listening to a different familiar song usually breaks it; "
          "it is harmless.",
          ask=("why", "what", "how", "get", "stop", "happen"),
          bias=1,
          avoid=("hearing", "hear", "tinnitus", "ringing", "deaf", "deafness")),
    entry("boredom", (("bored", "boredom", "boring"),
                      ("why", "feel", "get", "always", "what", "mean")),
          "Boredom is the brain asking for something engaging: with no clear goal it looks for "
          "novelty or meaning, and time feels slow because little is being laid down as a memory. "
          "It is not a flaw, and letting yourself be bored for a bit often restarts curiosity and "
          "ideas.",
          ask=("why", "what", "feel", "always"),
          avoid=("film", "movie", "book", "show", "series", "game", "lesson", "class",
                 "job", "work", "meeting", "party", "podcast", "podcasts", "listen",
                 "recommend", "recommendation"),
          bias=1),
    entry("fake-tan",
          (("fake tan", "spray tan", "self tan", "self-tan", "false tan", "tanning lotion",
            "tanning mousse", "gradual tan", "bronzer", "tan in a bottle"),
           ("safe", "safety", "protect", "spf", "sun", "last", "long", "how", "what", "does",
            "work", "risk", "breathe", "fade", "wash", "off")),
          "Fake tan is a dye, usually DHA, that colours only the dead cells on the surface and "
          "fades after about five to seven days, so it gives no sun protection; you still need "
          "SPF, and the one real risk is breathing in a spray mist - ask for a lotion or mousse, "
          "hold your breath or wear the mask, and patch test first.",
          ask=("fake", "spray", "self", "false", "gradual", "bronzer", "mousse", "lotion", "bottle",
               "dha")),
    entry("skin-tan", (("tan", "tanning", "tanned", "suntan", "sun tan", "sunbed", "solarium"),
                       ("why", "how", "get", "skin", "sun", "safe", "faster", "work", "use",
                        "stop", "prevent", "block", "protect")),
          "A tan is your skin making extra melanin to shield skin-cell DNA from ultraviolet "
          "light, and that is damage, not health: it raises the risk of skin cancer and ageing, "
          "so use SPF 30, shade and a hat and skip sunbeds; a fake tan is safer because it colours "
          "only the top layer.",
          ask=("why", "how", "what", "get", "safe", "work", "stop", "prevent", "block",
                "protect", "does", "can"),
          avoid=("leather", "shoe", "shoes", "bag", "bags", "boot", "boots", "carpet", "paint",
                 "wood", "furniture")),

    entry("sleep-teenagers",
          (("sleep", "sleeping", "slept", "hours", "bedtime", "bed time"),
           ("teenager", "teenagers", "teen", "teens", "teenage", "year 9", "year 10", "year 11",
            "secondary school", "college",
            "13 year", "14 year", "15 year", "16 year", "17 year", "18 year",
            "13-year", "14-year", "15-year", "16-year", "17-year", "18-year",
            "13 years old", "14 years old", "15 years old", "16 years old", "17 years old",
            "18 years old", "aged 13", "aged 14", "aged 15", "aged 16", "aged 17", "aged 18",
            "im 13", "im 14", "im 15", "im 16", "im 17", "im 18",
            "i am 13", "i am 14", "i am 15", "i am 16", "i am 17", "i am 18")),

          "Teenagers need more sleep than adults, not less: 8 to 10 hours a night from 14 to 17, "
          "and 9 to 12 from 6 to 13. Their body clock also shifts late, so an 11pm natural "
          "bedtime is biology rather than laziness, and a school start of 8am means lights out "
          "by 10:30 with the phone out of the room for the last hour. A weekend lie-in of more "
          "than two hours moves the clock further back and makes Monday worse, so a shorter "
          "catch-up and a dark room work better.",
          avoid=("my baby", "baby", "newborn", "toddler", "puppy", "cat", "dog", "insomnia",
                 "shift work", "jet lag", "apnoea", "snoring",
                 "pregnant", "hibernate",
                 "calcium", "iron", "vitamin", "vitamins", "protein", "fibre", "fiber",
                 "calories", "calorie", "potassium", "magnesium", "zinc", "b12", "folate",
                 "water", "milk", "steps"),
          ask=("teenager", "teenagers", "teen", "teens", "teenage", "year old", "year-old",
               "my son", "my daughter", "hour", "hours", "how much", "how many", "sleep")),
    entry("cholesterol-lower",
          (("cholesterol", "ldl", "hdl", "triglycerides", "lipid", "lipids"),
           ("lower", "reduce", "high", "how", "bring down", "improve", "diet", "statins",
            "statin", "raised", "bad", "down", "naturally")),
          "Cut saturated fat first, since that is what raises LDL: butter, cheese, fatty and "
          "processed meat, pastries and coconut oil. Swap to olive or rapeseed oil, and add oats, "
          "beans, nuts and oily fish twice a week, all of which lower LDL or triglycerides a "
          "little. Activity most days raises the good HDL. Together that is often 5 to 10%, so if "
          "your LDL is high enough for medication your GP will offer a statin, which does more "
          "than any diet does.",
          avoid=("egg", "eggs", "prawns", "shellfish", "butter or margarine", "my levels are")),
    entry("blood-pressure-lower",
          (("blood pressure", "hypertension"),
           ("lower", "reduce", "high", "bring down", "how", "diet", "exercise", "naturally",
            "salt", "down", "help")),
          "Salt is the biggest lever most people have: aim under about 6g a day, a teaspoon, "
          "which means cooking from scratch and reading the labels on bread, sauces and "
          "takeaways. Then 150 minutes a week of walking, cycling or swimming, losing a few kilos "
          "round the middle, cutting back on alcohol, and eating more fruit, vegetables, beans "
          "and dairy. Together those often take 5 to 10 points off; if your reading is around "
          "140/90 or more on repeated home checks, see your GP, because tablets do more than the "
          "lifestyle changes alone.",
          avoid=("what is", "whats a normal", "what's a normal", "normal", "reading", "machine",
                 "monitor", "cuff", "over 80", "too low", "low")),
    entry("weight-without-dieting",
          (("weight", "lose weight", "losing weight", "slim down", "kilos", "pounds", "fat",
            "stone", "stones"),
           ("lose", "without dieting", "diet", "dieting", "how", "start", "slowly", "keep off",
            "sustainable", "naturally", "losing")),
          "Change a few things you can keep doing rather than going on a diet: fill half the "
          "plate with vegetables, put protein in every meal so you are not hungry an hour later, "
          "swap sugary drinks for water or squash, and walk for half an hour a day. Losing about "
          "0.5 to 1kg a week is the rate that stays off, and the plan that works is the one you "
          "would still follow in a year. If you are hungry all the time, or the weight is going on "
          "without trying, see a GP.",
          guard=_the_pounds_are_weight,
          ask=("how", "what", "want to", "trying to", "should i", "tips", "advice", "best",
               "start", "help", "plan", "lose", "losing", "diet", "dieting", "slim"),
          avoid=("baby weight", "pregnant", "weight of", "weight limit", "baggage",
                 "suitcase", "how much does", "weight training", "lifting weights",
                 "the weights", "my weights", "keeps losing weight", "keep losing weight",
                 "i keep losing", "for no reason", "without trying", "unexplained",
                 "gone off my food", "no appetite",
                 "per kilo", "per kg", "per pound", "a kilo of", "how many kilos of",
                 "put by", "putting by", "save up", "saving up", "savings", "save",
                 "saved", "to save", "a week to have", "a month to have",
                 "how heavy is a stone", "how heavy is stone", "a stone in kilos",
                 "a stone in kg", "stone in kilos", "stone in kg", "how much is a stone",
                 "how many kilos in a stone", "how many kilos is a stone",
                 "how much does a stone weigh", "what is a stone in", "whats a stone in",
                 "stone from", "stone out", "stones from", "stones out",
                 "plum", "plums", "peach", "peaches", "cherry", "cherries", "damson",
                 "damsons", "greengage", "avocado", "mango", "olive", "olives", "apricot",
                 "apricots", "date stone", "pips", "pitted",
                 "oven", "hob", "tray", "pizza", "grill", "paving", "patio", "worktop",
                 "wall", "walls", "path", "steps", "slab", "slabs", "gravel", "driveway",
                 "floor", "sink", "drain", "garden", "rockery", "shoes", "shoe", "foot",
                 "kidney", "kidneys", "gallbladder", "bladder", "tonsil", "tonsils",
                 "basting", "bast", "carving", "stuffing", "cooking time", "minutes per",
                 "joint of", "how long do i cook", "how long to cook",
                 "per kilos", "per lb", "per 500g", "per 500 g", "kilo of", "kilos of",
                 "pound of", "pounds of", "how much is a kilo", "how much is a pound",
                 "how far", "how far can i go", "how far will", "far will",
                 "year old weigh", "year olds weigh", "year old weight", "what should a 5 year",
                 "my son is", "my daughter is", "my child is", "my kid is", "my children are",
                 "my kids are", "my son wants to lose", "my daughter wants to lose",
                 "my child wants to lose", "my kid wants to lose",
                 "cat", "cats", "dog", "dogs", "puppy", "puppies", "kitten", "kittens",
                 "rabbit", "hamster", "guinea pig", "my pet", "vet")),
    entry("statin-work",
          (("statin", "statins", "atorvastatin", "simvastatin", "rosuvastatin"),
           ("work", "how", "do i need", "need", "side effects", "side effect", "worth",
            "should i take", "stop", "muscle", "safe",
            "should i be on", "should i go on", "should i start", "should i keep taking",
            "keep taking")),
          "A statin blocks the liver enzyme that makes cholesterol, so less LDL ends up in your "
          "blood: expect roughly a 30 to 50% fall in LDL depending on the dose, with the biggest "
          "benefit for anyone who has already had a heart attack or stroke. Muscle aches are the "
          "side effect people worry about, and in trials they were about as common on the dummy "
          "tablet; if you do get them, try a different statin or a lower dose before giving up, "
          "because the benefit is real. Don't stop one on your own: ask the GP or pharmacist.",
          avoid=("how much do statins cost", "how much is a statin", "when should i take",
                 "when do i take",
                 "when to take", "what time", "time of day", "at night", "in the evening",
                 "in the morning", "same time each day")),
    entry("bmi-healthy",
          (("bmi", "body mass index"),
           ("healthy", "what", "whats", "good", "normal", "range", "calculate", "work out",
            "chart", "mean", "do i")),
          "BMI is weight in kilos divided by height in metres squared, and 18.5 to 24.9 is the "
          "range the NHS calls healthy. It is a crude tool: it cannot tell muscle from fat and it "
          "reads badly for very tall, very short or very muscular people, so waist measurement "
          "and how you feel matter alongside it. Use it as a rough flag, not a diagnosis, and if "
          "you want a real assessment ask the GP or a pharmacist.",
          avoid=("child", "children", "kid", "kids", "my son", "my daughter", "baby", "toddler")),
    entry("quit-smoking",
          (("smoking", "smoke", "smoked", "smoker", "smokers", "i smoke", "cigarettes",
            "cigarette", "cigs", "vape", "vaping", "nicotine",
            "pack a day", "packs a day", "smoke a pack", "pack and a half"),
           ("quit", "stop", "give up", "cut down", "how", "help", "best way", "cold turkey",
            "a day", "for years", "since i was", "i want to stop",
            "i want to quit", "want to give up", "years")),
          "The most reliable way is nicotine replacement plus a stop date: patches for the "
          "background craving and a fast-acting gum, lozenge or spray for the moments it spikes, "
          "used together. Set a date in the next two weeks, tell people, and change the routines "
          "that went with a cigarette - the first coffee, the car, the pub garden. Your GP can "
          "prescribe and refer you to a free stop-smoking service, and vaping is far less harmful "
          "than smoking if you need something in your hand.",
          avoid=("smoked salmon", "smoked haddock", "smoked mackerel", "smoked bacon",
                 "smoked paprika", "smoked cheese", "barbecue", "bbq", "smoke alarm",
                 "brisket", "briskets", "meat", "ribs", "pork", "pastrami", "jerky",
                 "sausages", "smokehouse", "low and slow",
                 "smoke from", "bonfire", "smoke house",
                 "pellet smoker", "electric smoker", "charcoal smoker", "smoker grill",
                 "smoker box", "smoker tube", "use a smoker", "my smoker", "buy a smoker",
                 "dad", "mum", "mother", "father", "husband", "wife", "partner", "girlfriend",
                 "boyfriend", "friend", "son", "daughter", "brother", "sister", "worried",
                 "worry", "wont", "won't",
                 "last week", "yesterday", "havent smoked", "haven t smoked",
                 "not had a cigarette", "since i quit", "since i stopped", "i ve quit",
                 "i ve stopped", "3 days ago", "a week ago", "a month ago",
                 "cough", "coughs", "coughing",
                 ) + _SMOKE_IS_NOT_A_HABIT),
    entry("helping-someone-stop-smoking",
          (("quit smoking", "stop smoking", "giving up smoking", "giving up", "smokes", "smoker",
            "cigarettes", "cigarette", "vaping", "vape", "nicotine"),
           ("dad", "mum", "mother", "father", "husband", "wife", "partner", "girlfriend",
            "boyfriend", "son", "daughter", "brother", "sister", "friend", "mate", "nan",
            "nana", "gran", "grandad", "grandma", "grandpa", "he", "she", "they", "worried",
            "worry", "him", "her", "their", "their smoking")),
          "The decision has to be theirs, but you can make it much easier: pick a date together, "
          "say once what you have noticed and then leave it, and offer the nicotine patches or gum "
          "rather than a lecture. Keep the house and the car smoke-free, and do something else "
          "when the craving hits at the usual times. Expect two or three tries, so a slip is not "
          "a failure - just start again the next day.",
          avoid=("cough", "coughs", "coughing", "chest", "wheeze", "phlegm",
                 "weed", "cannabis", "joint", "joints", "skunk", "marijuana", "dope",
                 "spliff", "ganja", "hash", "stoned", "high",
                 "years ago", "already quit", "already stopped", "used to smoke",
                 "has quit", "has stopped", "gave up years", "quit years")),
    entry("cough-after-quitting",
          (("stopped smoking", "quit smoking", "gave up smoking", "stopped vaping",
            "since i stopped", "since i quit"),
           ("cough", "coughs", "coughing", "chest", "wheeze", "phlegm")),
          "That cough is usually the airways clearing themselves: the little hairs that sweep "
          "mucus out start working again once the smoke stops, so a few weeks of coughing up is "
          "normal and a good sign. Do not let it send you back to cigarettes. See a doctor if "
          "there is blood, if you are breathless, or if it is still there after a month.",
          avoid=("stop date",)),
    entry("vaping-vs-smoking",
          (("vaping", "vape", "vapes", "e cigarette", "e cigarettes", "ecig", "ecigs"),
           ("better than", "worse than", "safer", "healthier", "harmful", "harm", "risk",
            "as bad", "bad as",
            "risks", "bad for", "damage", "compared", "compare", "switch", "switching",
            "instead of", "worth it", "side effects", "long term")),
          "Vaping is not harmless, but it is much less harmful than smoking: there is no tar "
          "and no carbon monoxide, and the nicotine arrives without the smoke that does most of "
          "the damage. What is left is the unknown - vapes are too new for long-term data, and "
          "the flavours are not tested for inhaling - so if you already smoke, switching is a "
          "real win, and if you do neither there is no reason to start. Most people's end point "
          "is neither one.",
          avoid=("stop", "stops", "stopping", "quit", "quits", "quitting", "giving up",
                 "give up", "help", "helping", "how do i", "cut down")),
    entry("cut-alcohol",
          (("alcohol", "drinking", "beer", "wine", "booze", "units"),
           ("cut down", "reduce", "less", "how much", "too much", "stop", "healthy", "limit",
            "week", "safe")),
          "The guideline is no more than 14 units a week, spread over three or more days, with "
          "a couple of drink-free days: that is about six pints of average beer or six medium "
          "glasses of wine. The changes that work are the boring ones - smaller glasses, a glass "
          "of water between drinks, no alcohol at home on weeknights, and a couple of alcohol-free "
          "beers in the fridge. If you are drinking every day to feel normal, or shaking without "
          "it, see a GP before stopping suddenly.",
          ask=("alcohol", "drinking", "drink", "drinks", "beer", "wine", "booze", "units",
               "pint", "pints", "vodka", "whisky", "gin"),
          avoid=("water", "hydrate", "hydration", "thirsty", "fluids", "juice", "milk",
                 "coffee", "coffees", "espresso", "latte", "cappuccino", "tea", "teas",
                 "caffeine", "decaf", "cola", "energy drink", "energy drinks",
                 "how do i make", "recipe", "wine with", "pair with", "hangover",
                 "pregnant", "pregnancy", "expecting", "trimester", "breastfeeding")),
    entry("stress-relief",
          (("stress", "stressed", "overwhelmed", "burnout", "burnt out", "anxious",
            "clear my head", "clear my mind", "clear my thoughts", "head is full",
            "mind is full", "cant think straight", "too much in my head",
            "destress", "de-stress", "de stress", "destressing", "unwind"),
           ("deal", "manage", "how", "help", "reduce", "cope", "stop", "better", "relieve",
            "handling")),
          "Pick the smallest physical thing first, because stress lives in the body: a slow "
          "breath out for longer than the breath in, a ten-minute walk, or a glass of water and "
          "something to eat if you have skipped a meal. Then write down what is actually on your "
          "plate and cut one thing or ask for one deadline to move. Sleep, exercise and talking "
          "to someone once a week do more than any app; if it has been most days for weeks, or "
          "you cannot work or sleep, that is a GP conversation.",
          avoid=("stress fracture", "stress test", "stressed about money", "work stress",
                 "tell my boss", "tell your boss", "tell the boss", "tell my manager",
                 "talk to my boss", "talk to my manager", "with my boss", "raise it with",
                 "bring it up with",
                 "before bed", "before bedtime", "to bed", "bedtime", "at bedtime",
                 "at night", "before sleep", "to sleep", "asleep", "so i can sleep",
                 "cant sleep", "can't sleep", "sleep",
                 "helps me", "helped me", "helps my", "helped my", "works for me",
                 "helps a lot", "helps so much", "helps when")),
    entry("panic-attack",
          (("panic attack", "panic attacks", "panicking", "cant breathe", "heart racing"),
           ("stop", "how", "help", "deal", "cope", "what do i do", "during", "calm",
            "having", "right now", "think im", "think i am", "symptoms", "symptom", "why",
            "what is", "again", "at night", "feel like", "feels like", "keep", "started",
            "coming on", "what can i do")),
          "A panic attack peaks in about ten minutes and cannot hurt you, so the aim is to ride "
          "it rather than stop it: breathe out for longer than you breathe in, name five things "
          "you can see and four you can touch, and remind yourself it will pass. Don't fight the "
          "heart rate - it is adrenaline, not a heart problem. If they keep coming, ask about CBT: "
          "it is the treatment with the best evidence, and a GP can refer you.",
          avoid=("dog", "cat", "puppy", "kitten", "child", "my son", "my daughter")
                + NOT_A_NOSE),
    entry("friend-depression",
          (("friend", "mate", "husband", "wife", "partner", "brother", "sister"),
           ("depressed", "depression", "not themselves", "withdrawn", "suicidal", "self harm",
            "self-harm", "low", "help them", "support")),
          "Say it plainly and once - \"you have not seemed yourself, and I am worried about you\" "
          "- and then listen without fixing. Ask whether they have thought about suicide: asking "
          "does not plant the idea, and it is the thing that opens the door. Practical help is "
          "what people remember: a lift to a GP appointment, a walk, a text on a bad day. If they "
          "are in danger now, stay with them and call 999 or the Samaritans on 116 123.",
          avoid=("how do i tell", "how do i deal with", "my friend hurt me", "friend at work",
                 "my son", "my daughter", "my child", "my kid", "teenager", "my mum", "my dad",
                 "my mother", "my father")),
    entry("posture-sitting",
          (("posture", "sitting", "sit all day", "desk", "slouching", "hunched"),
           ("improve", "fix", "bad", "back", "pain", "hurts", "better", "how", "help")),
          "There is no perfect posture to hold: the fix is moving, not sitting straighter. Set "
          "the screen so the top is at eye level, feet flat, elbows near a right angle, and stand "
          "up every 30 to 40 minutes even for a minute. Two or three times a day, stand with your "
          "hands on the door frame and lean through for 20 seconds to open the chest, and do a "
          "few slow chin tucks. Back pain that comes with numbness, weakness or trouble passing "
          "water is a GP matter, not a posture one.",
          bias=1,
          avoid=("dog", "cat", "horse riding", "baby carrier", "chair", "mattress",
                 "a sit down", "sit down with", "sit down about", "sit down and talk",
                 "sit down to talk", "proper sit down", "sit down meeting",
                 "fan", "fans", "ceiling fan", "desk fan", "pedestal fan", "blades", "grille",
                 "sit out", "sits out", "sat out", "sitting out", "left out", "left on the side",
                 "on the side", "room temperature", "out of the fridge", "out overnight",
                 "overnight", "how long can", "how long do", "how long does",
                 "sit up", "sit ups", "situp", "situps", "crunch", "crunches", "press up",
                 "press ups", "push up", "push ups", "squat", "squats", "plank", "planks",
                 "lunge", "lunges", "deadlift", "deadlifts", "reps", "rep", "workout",
                 "exercise", "form", "technique", "gym",
                 "paint", "paints", "painted", "painting", "repaint", "varnish", "sand")),
    entry("cholesterol-eggs",
          (("eggs", "egg", "prawns", "shellfish", "liver", "dietary cholesterol"),
           ("cholesterol", "raise", "bad", "safe", "how many", "every day", "too many",
            "high", "affect", "ok", "good")),
          "For most people the cholesterol in food matters much less than the saturated fat in it: "
          "an egg a day is fine, and it is the butter, cheese, fatty meat and pastries around the "
          "egg that move your LDL. People with diabetes or an inherited high cholesterol are "
          "usually advised to keep to about one a day, and it is worth asking your GP if that "
          "applies to you. Prawns and liver are similar: fine in normal amounts, not a reason to "
          "worry on their own.",
          guard=not_a_count_for_the_box_or_the_dish,
          avoid=("how do i cook", "poach", "scramble", "how many minutes", "how many mins",
                 "how long", "minutes", "minute", "timer", "eggs for breakfast ideas",
                 "open", "opened", "unopened", "shut", "closed", "stays open", "stayed shut",
                 "didnt open", "didn't open", "not opened")),
    entry("cough-lingering", (("cough", "coughs", "coughing"),
                              ("weeks", "week", "wont go away", "won't go away", "still",
                               "nearly", "persistent", "lingering", "long")),
          "A cough after a cold often lasts three to four weeks and still settles on its own: "
          "sip fluids, take honey (a spoonful, or in a warm drink), and don't bother with most "
          "cough medicines, which do little. See a GP if it is still there after three weeks, or "
          "sooner if you are coughing blood, getting breathless or wheezy, losing weight, or "
          "have a fever that keeps coming back.",
          ask=("weeks", "week", "long", "still", "nearly", "went", "back", "away"),
          avoid=("dog", "cat", "puppy", "kennel", "child", "children", "baby", "kid", "kids",
                 "toddler", "pregnant", "smoker", "smoking", "vape", "vaping"),
          bias=1),
    entry("chesty-cough", (("chesty", "cough", "phlegm", "mucus", "catarrh", "rattly",
                            "clear my chest", "clear the chest", "chest feels full"),
                           ("cold", "cough", "chest", "green", "yellow", "worse at night",
                            "at night")),
          "A chesty cough is usually a cold that has moved down, and the colour of what comes up "
          "does not mean you need antibiotics. Drink plenty, breathe steam from a bowl or a hot "
          "shower, prop yourself up to sleep, and give it two or three weeks. A GP the same day "
          "if you are breathless at rest, coughing blood, or feel properly unwell with a fever.",
          avoid=("dog", "cat", "puppy", "child", "children", "baby", "kid", "kids", "toddler",
                 "son", "daughter", "my son", "my daughter",
                 "pigeon", "bird", "horse", "chicken", "chickens",
                 "drawers", "drawer", "of drawers", "furniture", "freezer", "cupboard",
                 "wardrobe", "chest of drawers", "treadmill",
                 "dry", "dry cough", "tickly", "tickly cough"),
          bias=1),
    entry("cold-back-to-work", (("work", "office"),
                                ("stay off", "go back", "back to", "should i go", "off work",
                                 "go in", "return")),
          "Stay off while you have a fever, and go back when you have been 24 hours without one "
          "and feel up to it: a normal cold with a bunged nose is fine to work through if you can "
          "keep away from people who are vulnerable. Rest and fluids get you back quicker than "
          "pushing through, and a fever, aches or a chesty cough means wait.",
          ask=("should", "when", "can", "safe", "ok", "okay"),
          avoid=("dog", "cat", "puppy", "chicken", "build", "diy", "shed", "garden", "plant",
                 "holiday", "flight", "abroad", "gym", "run", "running",
                 "post", "post office", "parcel", "parcels", "package", "label", "parcel shop",
                 "return a parcel", "return the parcel",
                 "go to the office", "go into the office", "into the office", "the office on",
                 "back to the office", "the office tomorrow", "the office at the end",
                 "hybrid", "work from home",
                 "my son", "my daughter", "my child", "my kid", "my kids", "my baby",
                 "my toddler", "she", "he",
                 "broken", "broke", "fracture", "fractured", "cast", "plaster", "sprain",
                 "sprained", "injury", "injured", "operation", "surgery", "heal", "healing",
                 "recovery", "recovering", "physio", "crutches", "wrist", "ankle", "collarbone",
                 "rib", "ribs", "hip", "shoulder", "knee",
                 "week off", "weeks off", "week off work", "few days off", "off work for a week",
                 "off for a week", "off all week", "off for the week", "week off sick"),
          bias=1),
    entry("back-tweak", (("back", "back has gone", "put my back out", "tweaked my back",
                          "lower back"),
                         ("lifting", "lift", "tweaked", "twisted", "went", "gone", "rest",
                          "keep moving", "moving", "move", "better")),
          "Keep moving gently rather than resting in bed: most back strains ease in one to two "
          "weeks, and staying in bed makes them last longer. Carry on with your usual jobs but "
          "cut the lifting, take paracetamol or ibuprofen if you need it, and use a hot water "
          "bottle on the tight part. See a GP or a physio if the pain is down a leg, you have "
          "numbness or tingling, or it is no better after two weeks.",
          ask=("rest", "moving", "move", "better", "should", "what"),
          avoid=("dog", "cat", "horse", "chair", "sofa", "garden", "hedge", "car", "seat",
                 "sit all day", "sitting all day", "sat all day", "sit at a desk",
                 "sitting at a desk", "sit at my desk", "sitting at my desk", "desk job",
                 "my son", "my daughter", "my husband", "my wife", "my mum", "my dad",
                 "my partner", "pregnant",
                 ),
          guard=_the_backs_are_a_body, bias=1),
    entry("sprain-heal", (("sprain", "sprained", "twisted", "ankle", "wrist", "thumb"),
                          ("heal", "healing", "how long", "long", "recover", "recovery", "take",
                           "weeks", "better")),
          "A sprained ankle or wrist usually hurts a lot for two or three days and is properly "
          "better in two to six weeks; a bad one can take three months. Ice it for 20 minutes at "
          "a time for the first couple of days, wrap it, keep it up when you can, and start "
          "moving it gently as the pain allows. Get it checked if you cannot put weight on it, "
          "it is badly swollen and bruised, or the joint looks out of shape.",
          ask=("how long", "long", "weeks", "when", "should"),
          avoid=("dog", "cat", "car", "wheel", "bike", "house", "market",
                 "broken", "broke", "fracture", "fractured", "cracked", "cast", "plaster",
                 "pregnant", "pregnancy", "weeks pregnant", "trimester", "midwife"),
          bias=1),
    entry("headache-see-doctor", (("headache", "headaches", "head ache", "migraine"),
                                  ("worry", "worrying", "serious", "should i see", "doctor",
                                   "gp", "dangerous", "normal", "checked")),
          "Most headaches are not serious, and the ones to get checked the same day are: the "
          "worst you have ever had, one that comes on like a thunderclap, one with a fever and a "
          "stiff neck, one after a bang on the head, one with weakness, slurred speech or a "
          "change in vision, or a headache that is getting steadily worse over weeks. Otherwise "
          "a GP can look at it in the normal way if painkillers are needed more than a couple of "
          "days a week.",
          ask=("should", "worry", "serious", "normal", "dangerous", "checked", "see"),
          avoid=("dog", "cat", "child", "children", "baby", "kid", "kids", "pregnant"),
          bias=2),
    entry("headache-days", (("headache", "headaches", "head ache"),
                            ("day", "days", "week", "weeks", "weekend", "month", "months",
                             "fortnight", "while", "constant")),
          _headache_days_reply,
          avoid=("dog", "cat", "child", "children", "baby", "kid", "kids", "pregnant",
                 "pregnancy", "breastfeeding", "breast feeding", "nursing", "chestfeeding",
                 "expecting", "trimester", "before my period", "hangover"),
          bias=4),
    entry("out-of-breath-stairs", (("out of breath", "breathless", "short of breath",
                                    "puffed out", "puffed", "cant breathe",
                                    "gasping", "gasp", "gasped"),
                                   ("stairs", "upstairs", "walking", "hills", "hill",
                                    "exercise", "everyday")),
          "Getting puffed on the stairs is usually fitness rather than illness, and it improves "
          "in a few weeks if you walk a little more each day. Get it checked if it has come on "
          "over weeks, if you are breathless sitting still or lying flat, if it comes with chest "
          "pain, swollen ankles or a cough, or if it is worse than it was a month ago - that is a "
          "GP appointment, not a training problem.",
          avoid=("dog", "cat", "car", "bike", "stairs at work", "lift", "running", "run",
                 "marathon", "swim"),
          bias=1),
    entry("tablets-forgotten", (("tablet", "tablets", "pill", "pills", "medication",
                                 "medicine", "inhaler"),
                                ("forget", "forgetting", "forgot", "miss", "missing",
                                 "remember", "keep forgetting")),
          "Put the tablets where the job happens rather than where they are stored - by the "
          "kettle, the toothbrush, the front door - and set a phone alarm with the name of the "
          "dose. A weekly pill box from the pharmacy makes a missed day obvious, and a pharmacist "
          "can switch you to a once-a-day version or a combined tablet if the timing is the "
          "problem. If you have missed a dose, take it when you remember unless it is nearly time "
          "for the next one, and never double up; ask the pharmacist about your particular tablet.",
          ask=("how", "keep", "help", "what", "should"),
          avoid=("dog", "cat", "puppy", "horse", "child", "children", "baby", "kid", "kids",
                 "water", "dishwasher", "washing machine", "toilet", "limescale"),
          bias=1),
    entry("tired-after-illness", (("flu", "cold", "virus", "infection", "covid", "illness"),
                                  ("tired", "knackered", "exhausted", "fatigue", "weeks",
                                   "still", "normal", "energy")),
          "Feeling washed out for a week or two after flu or another virus is normal, and it "
          "eases faster if you build back up slowly - a short walk, then a bit further - rather "
          "than going straight back to everything. Eat properly, keep fluids up and get your "
          "usual sleep. See a GP if the tiredness is no better after three or four weeks, or if "
          "it comes with breathlessness, a racing heart or feeling low.",
          ask=("tired", "tiredness", "knackered", "exhausted", "exhaustion", "fatigue",
               "washed out", "no energy", "worn out", "drained", "shattered", "lethargic"),
          avoid=("dog", "cat", "puppy", "horse", "child", "children", "baby", "kid", "kids",
                 "toddler", "pregnant", "my mum", "my dad", "my husband", "my wife"),
          bias=1),
    entry("immune-boost",
          (("immune system", "immunity", "immune"),
           ("boost", "improve", "stronger", "strengthen", "how", "better", "support",
            "naturally", "build")),
          "You cannot boost it with a pill: the things that hold up are sleep of seven to nine "
          "hours, regular activity, enough fruit and vegetables, not smoking, keeping alcohol "
          "low, and the vaccines you are offered. Vitamin D 10 micrograms a day through autumn "
          "and winter is the one supplement worth taking for most people. Big doses of vitamin C, "
          "echinacea and the rest have not held up in trials, and if you keep getting infections "
          "that is a GP question rather than a supplement one."),

    entry("missed-contraceptive-pill",
          (("pill", "pills", "contraceptive", "contraception", "mini pill", "combined pill"),
           ("missed", "miss", "forgot", "forgotten", "skipped", "late", "sex", "unprotected",
            "condoms", "contraceptive", "mini", "last night", "this week")),
          _missed_pill,
          bias=2,
          ask=(("missed", "miss", "forgot", "forgotten", "skipped", "late", "sex", "unprotected",
                "condoms"),),
          avoid=("blood pressure", "statins", "tablet", "tablets", "medication", "medicines",
                 "insulin", "diabetes", "antibiotics", "water", "vitamin", "vitamins", "diet",
                 "painkiller", "painkillers", "headache", "hayfever", "allergy", "morning after",
                 "emergency contraception", "paracetamol", "ibuprofen")),
    entry("missed-medication",
          (("tablets", "tablet", "medication", "medications", "medicines", "medicine", "pills",
            "pill", "insulin", "dose", "doses", "dosage", "prescription", "prescriptions",
            "warfarin", "epilepsy", "epileptic", "thyroid", "levothyroxine", "blood thinner",
            "blood thinners", "antibiotic", "antibiotics", "penicillin", "amoxicillin"),
           ("confused", "muddled", "muddle", "forgot", "forget", "forgets", "forgetting",
            "missed", "miss", "missing", "double", "doubled", "doubling", "twice", "remember",
            "remembering", "remembers", "keeps forgetting", "ran out", "runs out", "mixed up",
            "instead", "by mistake", "mistake", "accident", "accidentally")),
          _missed_medication,
          bias=2,
          avoid=("overdose", "too many", "took all", "swallowed", "years ago", "side effect",
                 "side effects", "paracetamol", "ibuprofen", "morning after",
                 "contraceptive", "contraception", "mini pill", "combined pill", "my pill",
                 "had sex", "unprotected")),
    entry("keep-taking",
          (("tablet", "tablets", "pill", "pills", "medication", "meds", "medicine", "medicines",
            "prescription", "statins", "statin", "inhaler", "steroids", "prednisolone",
            "antidepressants", "antibiotics", "antibiotic", "blood pressure tablets",
            "thyroid tablets", "levothyroxine"),
           ("keep taking", "keep on taking", "keep them up", "carry on taking", "carrying on",
            "stay on", "staying on", "still take", "still taking", "still be taking",
            "should i still be", "should i be taking", "am i supposed to keep", "supposed to be",
            "should i keep",
            "should i stop", "can i stop", "stop taking", "stop them", "come off", "coming off",
            "do i have to keep", "do i have to take", "have to take them", "need to keep",
            "for life", "for good", "forever", "long term", "is it ok to stop", "ok to stop",
            "bad to stop", "safe to stop", "should i finish", "finish the course", "finish them")),
          _keep_taking,
          bias=5,
          ask=("keep", "keeps", "should", "can", "do i", "is it", "stop", "stay", "come off",
               "still", "finish", "safe", "ok", "bad", "have to", "need"),
          avoid=("screen", "screens", "app", "apps", "wifi", "wi-fi", "battery", "batteries",
                 "charger", "charging", "sim", "storage", "draw", "drawing", "stylus", "pen",
                 "cracked", "slow", "kindle", "ipad", "android", "samsung", "fire", "kids",
                 "child", "children", "baby", "toddler", "puppy", "dog", "cat",
                 "out of date", "past the date", "expired", "expiry", "use by", "old tablets",
                 "shop", "refund", "warranty", "guarantee", "receipt", "exchange", "return it",
                 "returning it", "send it back", "took it back", "take it back", "money back",
                 "the pill", "my pill", "on the pill", "contraceptive", "contraception",
                 "mini pill", "combined pill", "morning after", "vitamin", "vitamins",
                 "hayfever", "hay fever", "allergy",
                 "overdose", "too many", "swallowed", "double", "doubled", "missed", "miss",
                 "forgot", "forget", "forgetting", "ran out", "run out", "with alcohol",
                 "side effect", "side effects", "making me", "breastfeeding", "pregnant")),

]

ENTRIES.append(entry(
    "nhs-dentist-free",
    (("dentist", "dentists", "dental", "check up", "checkup", "nhs", "filling", "crown"),
     ("free", "get it free", "free treatment", "do i pay", "do i have to pay", "covered",
      "who pays", "qualify", "exempt", "concession")),
    "NHS dentistry is free for children, anyone under 19 in full-time education, pregnant women "
    "and mothers in the year after the birth, and people on certain benefits such as universal "
    "credit or income support. Everyone else pays a fixed band per course of treatment - about "
    "£27 for a check-up, £75 for a filling and £325 for a crown or a denture - and a check-up is "
    "free in Scotland. Ask at the desk which band you are in, because the work in one band is "
    "covered by one charge.",
    avoid=("how much", "how many", "cost", "costs", "price", "prices", "charge", "charges",
           "private", "expensive", "cheaper", "worth it", "going rate"),
    bias=2))



_CLOCK_AT = re.compile(r"\b(up|awake|wake|wakes|alarm|get up|getting up)\b[^0-9]{0,16}?"
                       r"\b(\d{1,2})(?:[:.](\d{2}))?\s*(am|pm)?\b")
_BED_AT = re.compile(r"\b(bed|bedtime|sleep|lights out)\b[^0-9]{0,14}?"
                     r"\b(\d{1,2})(?:[:.](\d{2}))?\s*(am|pm)?\b")


def _clock_time(hour, minute):
    suffix = "am" if hour < 12 else "pm"
    on_clock = hour % 12 or 12
    return "%d%s" % (on_clock, suffix) if not minute else "%d.%02d%s" % (on_clock, minute, suffix)


def _back_from(hour, minute, hours):
    total = (hour * 60 + minute - hours * 60 - 20) % (24 * 60)
    return total // 60, total % 60


def _forward_from(hour, minute, hours):
    total = (hour * 60 + minute + 20 + hours * 60) % (24 * 60)
    return total // 60, total % 60


def _sleep_clock(memory, understood):
    text = (understood or {}).get("clean") or ""
    found = _CLOCK_AT.search(text)
    in_bed = None if found else _BED_AT.search(text)
    hour, minute = 0, 0
    if found or in_bed:
        match = found or in_bed
        try:
            hour, minute = int(match.group(2)), int(match.group(3) or 0)
        except (TypeError, ValueError):
            hour, minute = 0, 0
        if match.group(4) == "pm" and hour < 12:
            hour += 12
        if in_bed and hour < 12 and not match.group(4):
            hour += 12
    if in_bed and 20 <= hour <= 23 or in_bed and hour <= 3:
        eight = _forward_from(hour % 24, minute, 8)
        nine = _forward_from(hour % 24, minute, 9)
        return ("In bed at %s, asleep about twenty minutes later, so up at %s on eight hours or "
                "%s on nine - and that alarm is worth keeping the same every day, weekend "
                "included, because the fixed morning is what sets the body clock and the bedtime "
                "then follows it."
                % (_clock_time(hour % 24, minute), _clock_time(*eight), _clock_time(*nine)))
    if 4 <= hour <= 11:
        eight = _back_from(hour, minute, 8)
        nine = _back_from(hour, minute, 9)
        return ("To be up at %s, count back eight hours and leave twenty minutes to drop off, so "
                "lights out about %s - and about %s if you are a nine-hour sleeper. What matters "
                "more than the exact minute is keeping the morning the same every day, weekend "
                "included, because that is the end of the night the body clock sets itself by, "
                "and the bedtime then falls into place on its own."
                % (_clock_time(hour, minute), _clock_time(*eight), _clock_time(*nine)))
    return ("Work it back from the morning: pick the time you have to be up, count back eight "
            "hours and allow twenty minutes to drop off - a half six alarm means lights out about "
            "ten, a seven o'clock one about half ten. Nine-hour sleepers go an hour earlier. Keep "
            "the wake-up time the same every day, weekends included: a bedtime held while the "
            "mornings shift is the wrong way round. If you lie awake an hour, the bedtime is too "
            "early, not too late.")


ENTRIES.append(entry(
    "sleep-clock",
    (("wake up", "waking up", "get up", "getting up", "alarm", "up", "awake"),
     ("what time", "what hour", "when should i", "how late", "how early", "time should i",
      "time do i", "time to", "goal", "need to be")),
    _sleep_clock, bias=1,
    ask=("what time", "when should i", "how late", "how early", "time should i"),
    avoid=("kids", "child", "children", "my son", "my daughter", "toddler", "baby", "babies",
           "newborn", "teenager", "teenagers", "teen", "school night", "school nights",
           "year old", "years old", "yr old", "yrs old", "month old", "months old",
           "year-old", "years-old", "old go to bed", "puppy",
           "cat", "dog", "shift work", "night shift", "jet lag", "time zone", "nap", "naps",
           "insomnia", "cant sleep", "can't sleep", "cant get to sleep", "wake up at 3",
           "wake at 3", "wake up at 4", "wake at 4", "2am", "3am", "4am", "5am",
           "cant get back to sleep", "middle of the night", "too late", "stay up too late",
           "tree up", "put up", "putting up", "christmas tree", "xmas tree", "decorations",
           "decorate", "decorating")))



ENTRIES.append(entry(
    "closest-planet",
    (("closest to the sun", "closest planet to the sun", "nearest to the sun",
      "nearest the sun", "closest to the sun", "first planet", "innermost planet",
      "mercury closest", "mercury the closest"),
     ("which planet", "what planet", "mercury", "closest", "nearest", "sun")),
    "Mercury is the closest planet to the Sun, about 58 million km out, and it goes round once "
    "every 88 Earth days. It is not the hottest, though: Venus is, because its thick carbon "
    "dioxide atmosphere traps the heat.",
    avoid=("moon", "moons", "star", "stars", "toxic", "poison", "thermometer", "fish",
           "element", "barometer", "symbol", "planet facts", "retrograde", "astrology",
           "sign", "horoscope", "metal")))

ENTRIES.append(entry(
    "moon-orange",
    (("moon", "moons"), ("orange", "red", "yellow", "pink")),
    "Near the horizon the Moon's light crosses much more air, and the air scatters the blue end "
    "of it away, so what reaches you looks orange or red. The same effect reddens a low Sun, and "
    "dust or smoke deepens it.",
    ask=("orange", "red", "yellow", "pink", "why", "colour", "color"),
    bias=1))

ENTRIES.append(entry(
    "blood-moon",
    (("blood moon", "lunar eclipse", "lunar eclipses"),
     ("what", "why", "is", "red", "orange", "happen", "happens")),
    "A blood moon is a lunar eclipse: the Earth sits between the Sun and the Moon, and the only "
    "sunlight reaching the Moon has passed through Earth's atmosphere, which scatters the blue "
    "away and leaves red. It is safe to look at, unlike a solar eclipse.",
    bias=1))

ENTRIES.append(entry(
    "moon-white",
    (("moon", "moons"), ("white", "grey", "gray", "silver", "pale")),
    "The Moon is grey-brown rock; it looks white because it is lit by direct sunlight against a "
    "black sky, and your eyes judge it against that darkness. The bright and dark patches are "
    "different rocks, not ice or cloud.",
    ask=("white", "grey", "gray", "silver", "pale", "why", "colour", "color"),
    bias=1))

ENTRIES.append(entry(
    "moon-craters",
    (("moon", "moons"), ("crater", "craters", "pothole", "potholes", "dark spot",
                          "dark spots", "dark patch", "dark patches")),
    "The Moon's craters are mostly impact scars from rocks that hit it over billions of years, "
    "and with no air or water to erode them they stay. The dark patches are old lava plains, not "
    "shadows.",
    ask=("why", "how", "what", "made", "made of", "formed", "have", "get")))

ENTRIES.append(entry(
    "shooting-star",
    (("shooting star", "shooting stars", "falling star", "falling stars", "meteor", "meteors"),
     ("what", "why", "is", "are", "see", "night", "sky")),
    "A shooting star is a speck of dust or grit burning up high in the atmosphere, not a star "
    "falling. Most are the size of a grain of sand and vanish in a second; during a meteor shower "
    "you can see dozens an hour.",
    avoid=("photograph", "photography", "photo", "picture", "camera", "phone", "film",
           "movie", "song", "lyrics", "lyric", "band", "album", "track", "cook", "chicken"),
    bias=3))

ENTRIES.append(entry(
    "rockets-work",
    (("rocket", "rockets", "rocket engine", "rocket engines"),
     ("how", "work", "works", "fly", "launch", "space", "get to space", "escape")),
    "A rocket pushes gas out of the back at high speed, and the equal push forwards lifts it; it "
    "does not need air to push against. It has to reach about 28,000 km/h sideways to stay in "
    "orbit rather than fall back.",
    avoid=("toy", "toys", "lego", "bottle", "water bottle", "cress", "salad", "leaf",
           "leaves", "my app", "launch my", "game", "games", "kerbal", "rocket league",
           "app store", "startup", "business")))

ENTRIES.append(entry(
    "humidity",
    (("humidity", "humid", "relative humidity", "muggy", "sticky", "close and",
      "close in here", "close weather"),
     ("what", "why", "mean", "means", "high", "low", "air", "hot")),
    "Humidity is how much water vapour the air holds; relative humidity is that as a share of "
    "the most it could hold at that temperature. Warm air holds more, which is why a hot muggy "
    "day feels worse than the same heat in dry air.",
    avoid=("forecast", "weather app", "tomorrow", "weekend")))

ENTRIES.append(entry(
    "hunger",
    (("hungry", "hunger", "why am i hungry", "why do i get hungry"),
     ("why", "what", "always", "still", "after", "eat", "eating", "meal", "meals")),
    "Hunger is your body's signal that fuel is running low: the stomach releases a hormone "
    "called ghrelin, and blood sugar and habit both feed into it. Feeling hungry again soon after "
    "a meal is often a fast carbohydrate meal rather than a real shortage; protein, fibre and fat "
    "keep it down for longer.",
    avoid=("food bank", "food banks", "starving", "starve", "cant afford", "can't afford",
           "no money", "benefits", "hunger strike", "africa", "famine", "cat", "cats",
           "dog", "dogs", "puppy", "puppies", "kitten", "kittens", "pet", "pets", "vet",
           "horse", "horses", "pony", "ponies", "rabbit", "rabbits", "bunny", "bunnies",
           "guinea pig", "guinea pigs", "hamster", "hamsters", "gerbil", "gerbils", "ferret",
           "parrot", "parrots", "budgie", "budgies", "bird", "birds", "chicken", "chickens",
           "fish tank", "tortoise", "lizard", "snake", "reptile", "livestock",
           "cattle", "sheep", "goat", "goats",
           "hunger games", "the hunger games", "book", "books", "novel", "novels",
           "film", "films", "movie", "movies", "box set", "tv series", "series",
           "watch", "watching", "reading", "read", "author", "called")))

ENTRIES.append(entry(
    "thirst",
    (("thirsty", "thirst", "why am i thirsty", "why do i get thirsty"),
     ("why", "what", "always", "so", "very", "mean", "means")),
    "Thirst means your body is slightly short of water and your blood has become a little more "
    "concentrated; your brain responds by making you want a drink and your kidneys concentrate "
    "your urine. If you are always thirsty and passing a lot of urine, get it checked, because "
    "that can be diabetes.",
    avoid=("beer", "wine", "hangover", "pub", "drink less", "alcohol")))

ENTRIES.append(entry(
    "things-fall",
    (("things fall", "why do things fall", "falling", "fall"),
     ("why", "what", "makes", "make", "gravity", "down")),
    "Things fall because gravity pulls every mass towards every other mass, and the Earth is by "
    "far the biggest thing near you. Drop a stone and a coin together with no air and they hit "
    "at the same time; air resistance is what makes a feather float.",
    avoid=("hair", "leaves", "leaf", "rain", "snow", "prices", "stocks", "shares", "asleep",
           "apart", "falls apart", "falling apart", "fell apart", "breaks up", "breaking up",
           "to bits", "crumbles", "crumbling", "in the pan", "in the oven", "when i cook",
           "fell over", "fall over", "fell down the stairs",
           "aztec", "aztecs", "inca", "incas", "rome", "roman", "romans", "empire", "empires",
           "civilisation", "civilization", "dynasty", "regime", "soviet", "berlin wall",
           "government", "governments", "monarchy", "kingdom", "republic", "slave trade",
           "falling for", "fell for", "fall for", "fall out", "falling out",
           "fell out", "falls out", "falling behind", "fell behind", "falls behind",
           "my dad", "my mum", "my mother", "my father", "my nan", "my nana", "my grandad",
           "my grandma", "grandad", "grandma", "granny", "grandpa", "elderly", "oap",
           "unsteady", "balance", "his feet", "her feet", "on his feet", "on her feet",
           "shaky", "hip", "hospital", "ambulance", "the stairs")))

ENTRIES.append(entry(
    "bubbles-pop",
    (("bubble", "bubbles", "soap bubble", "soap bubbles"),
     ("pop", "pops", "burst", "why", "last", "float", "make")),
    "A bubble is a thin film of water with soap holding it together, and it pops when the water "
    "drains or evaporates from the top until the film is too thin. Dry air and a dusty surface "
    "speed that up, which is why bubbles last longer in a steamy bathroom.",
    avoid=("bubble tea", "bubble wrap", "gum", "economy", "housing", "market",
           "stomach", "tummy", "gut", "wind", "gas", "bloating", "belly", "fart",
           "urine", "pee", "wee", "piss", "bladder", "kidney")))

ENTRIES.append(entry(
    "stars-count",
    (("stars", "star"),
     ("how many", "number", "count", "in the sky", "universe")),
    "From a dark place you can see about 2,000 to 3,000 stars at once, and the whole sky holds "
    "around 9,000 visible to the naked eye. The Milky Way alone has 100 to 400 billion, and the "
    "observable universe has more stars than there are grains of sand on Earth.",
    avoid=("star sign", "star signs", "horoscope", "zodiac", "star wars", "movie", "film",
           "hotel", "restaurant", "review", "rating", "michelin")))


ENTRIES.append(entry(
    "moon-bright",
    (("moon", "moons"), ("bright", "shining", "shine", "glow", "glowing")),
    "The Moon makes no light of its own: it reflects sunlight, and at full moon it is opposite "
    "the Sun so nearly all of its lit face is turned towards you. Its rock is dark grey, but "
    "with no air to dim the light and a black sky around it, it looks brilliant.",
    ask=("why", "what", "so", "look", "looks", "bright", "shine", "glow"),
    bias=1))

ENTRIES.append(entry(
    "kettle-whistle",
    (("kettle", "kettles", "electric kettle"),
     ("whistle", "whistles", "whistling")),
    "The whistle is a small cap with a slit: steam from boiling water is forced through it and "
    "makes the air vibrate, which is the note you hear. It stops when you lift the cap or the "
    "switch cuts the power, and a whistle that never sounds usually means the cap is loose or "
    "blocked.",
    avoid=("descale", "descaler", "descaling", "limescale", "scale", "fur", "furred", "clean",
           "cleaning", "element", "slow", "not boiling", "wont boil", "won't boil",
           "taste", "tastes", "smell", "smells", "plastic", "so long", "take so long",
           "takes so long", "boil over", "boils over"),
    bias=3))

ENTRIES.append(entry(
    "banana-curved",
    (("banana", "bananas"), ("curved", "curve", "bent", "bend", "why", "shape")),
    "A banana starts growing downwards, then turns and grows upwards towards the light, and the "
    "side facing the ground grows faster, so the fruit ends up curved. The bend is set by the "
    "time it is cut, which is why a bunch hangs like a hand of fingers.",
    avoid=("bread", "cake", "muffin", "loaf", "milkshake", "smoothie", "recipe", "brown",
           "black", "ripe", "ripen", "eat", "peel", "banana plant", "banana tree",
           "how do bananas grow", "growing bananas"),
    ask=("why", "what", "how", "curved", "curve", "bent", "shape")))


ENTRIES.append(entry(
    "mirror-reverse",
    (("mirror", "mirrors"), ("reverse", "reverses", "backwards", "back to front",
                             "left and right", "left right", "why", "what")),
    "A mirror does not swap left and right: it swaps front and back, because it sends the light "
    "straight back at you. Your face is nearly symmetrical, so the only thing you notice is that "
    "a raised right hand seems to be on the other side.",
    avoid=("makeup", "make up", "shave", "shaving", "clean", "cleaning", "fog", "steam",
           "hang", "hanging", "wall", "buy", "shatter", "broken", "bedroom", "bathroom"),
    ask=("why", "what", "how", "reverse", "reverses", "backwards", "left", "right")))

ENTRIES.append(entry(
    "cut-sting",
    (("cut", "cuts", "graze", "scrape", "scratch", "paper cut"),
     ("sting", "stings", "hurt", "hurts", "why", "salt", "lemon")),
    "A cut stings because the broken skin leaves nerve endings exposed, and salt, lemon or soap "
    "irritates them directly; the sting fades as the cut seals. Rinse it with clean water and "
    "cover it, and get help if it is deep, very dirty or will not stop bleeding.",
    avoid=("recipe", "cook", "cooking", "meat", "beef", "lamb", "pork", "chicken", "cake",
           "hair", "grass", "lawn", "wood", "metal", "budget", "pay", "job", "staff",
           "infected", "infection", "septic", "pus", "swollen", "red", "hot", "smell", "smells",
           "tetanus", "deep", "bleeding", "stitches",
           "cut out", "cuts out", "cutting out", "cut off", "cuts off", "cutting off",
           "cut out on me", "keeps cutting out", "cutting out at", "cuts out when",
           "scratching the", "scratches the", "scratch the", "keeps scratching", "scratching my",
           "scratch its", "scratch his", "scratch her", "scratch everything", "scratch the door",
           "furniture", "flea", "fleas", "mites", "scratching post", "scratch post",
            "sofa", "settee", "couch", "carpet", "floor", "claws", "clawing",
           "dog scratching", "dog scratches", "dog keeps scratching", "scratches himself",
           "scratching himself", "my dog scratching"),
    ask=("why", "what", "how", "sting", "stings", "hurt", "hurts", "salt", "lemon"),    bias=2))


ENTRIES.append(entry(
    "sun-made-of",
    (("sun",), ("made of", "made from", "composed", "composition", "hydrogen", "helium",
                "inside", "what is it made")),
    "The Sun is about three-quarters hydrogen and a quarter helium, all so hot that it is a "
    "gas-like plasma. Its gravity squeezes the core until hydrogen fuses into helium, and that "
    "reaction is what makes its light and heat.",
    avoid=("hot", "heat", "temperature", "burn", "sunburn", "sun cream", "sunscreen", "lamp",
           "bed", "bright", "moon"),
    ask=("what", "made", "of", "from", "inside")))

ENTRIES.append(entry(
    "day-night",
    (("day and night", "day night", "night and day"),
     ("why", "what", "cause", "causes", "happen", "happens", "have", "earth", "sun", "work",
      "works", "get", "how", "does", "do")),
    "The Earth turns on its axis about once every 24 hours, so the half facing the Sun is in "
    "daylight while the other half is in night. The Sun itself does not go anywhere.",
    ask=("why", "what", "cause", "have", "how", "get", "does", "make", "makes"),
    avoid=("baby", "babies", "toddler", "newborn", "sleep", "sleeping", "slept", "wake",
           "waking", "woke", "night shift", "shift work", "jet lag", "insomnia")))

ENTRIES.append(entry(
    "earth-round",
    (("earth", "world"), ("round", "sphere", "spherical", "flat", "shape", "why")),
    "Gravity pulls every part of a large body towards its centre, and over 4.5 billion years that "
    "has pulled the Earth into a ball. Its spin makes it bulge slightly at the equator, so it is a "
    "squashed sphere rather than a perfect one.",
    avoid=("around the world", "travel", "trip", "song", "lyrics", "earthquake", "earth wire",
           "rare earth", "earth day", "earth hour", "down to earth"),
    ask=("why", "is", "round", "flat", "shape")))

ENTRIES.append(entry(
    "urine-yellow",
    (("urine", "pee", "wee"), ("yellow", "why", "colour", "color")),
    "Urine is yellow because it carries urobilin, a breakdown product of old red blood cells, and "
    "the more water you drink the paler it gets. See a doctor if it is dark brown or red, or comes "
    "with pain or fever, because those are not just concentration.",
    avoid=("dark", "brown", "red", "blood", "pain", "burning", "stings", "smell", "foamy",
           "cloudy", "infection", "doctor", "gp", "uti", "pregnant", "test"),
    ask=("why", "yellow", "colour", "color")))

ENTRIES.append(entry(
    "energy-what",
    (("energy",), ("mean", "meaning", "definition", "explain", "what is energy")),
    "Energy is the ability to make something happen - to move, heat, light or power something - "
    "and it is never used up, only changed from one form into another. Food stores chemical "
    "energy, a moving bike has kinetic energy, and a hot cup has thermal energy.",
    avoid=("bill", "bills", "electricity", "gas", "supplier", "tariff", "meter", "saving",
           "save", "tired", "sluggish", "drink", "food", "calories", "protein", "solar",
           "panel", "company", "price", "cost", "cheap"),
    ask=("what", "mean", "meaning", "explain")))

ENTRIES.append(entry(
    "temperature-what",
    (("temperature",), ("mean", "meaning", "definition", "explain", "measure",
                        "what is temperature")),
    "Temperature measures how fast the particles in something are moving: faster particles mean a "
    "higher temperature and slower ones mean a lower one. It is not the same as how much heat is "
    "stored, which is why a cup of tea and a bath can be the same temperature but hold very "
    "different amounts of heat.",
    avoid=("fever", "high", "low", "body", "baby", "child", "thermometer", "room", "oven",
           "cook", "weather", "outside", "today", "hot", "cold", "forecast"),
    ask=("what", "mean", "meaning", "explain", "measure"),
    bias=3))


ENTRIES.append(entry(
    "anger-why",
    (("angry", "anger", "rage"), ("why", "what", "cause", "causes", "get", "feel")),
    "Anger is the body's alarm at a threat or at a goal being blocked: adrenaline speeds your heart "
    "and tenses your muscles, and the emotional part of the brain reacts before the thinking part "
    "has caught up. It usually passes in minutes; slow breathing and naming what set it off help it "
    "pass sooner.",
    avoid=("always", "every day", "all the time", "my partner", "my wife", "my husband", "my kids",
           "hit", "hurt", "violent", "abuse", "depressed", "anxiety", "therapy", "counselling",
           "hungry", "hunger", "hangry", "snappy", "stopped eating"),
    ask=("why", "what", "get", "feel")))

ENTRIES.append(entry(
    "water-wet",
    (("water",), ("wet", "why", "what")),
    "Water is wet because it clings to surfaces and spreads across them instead of beading up: its "
    "molecules stick to each other and to most things, so a thin film stays on your skin. Wetness "
    "is that film, not a property of the water on its own.",
    avoid=("floor", "carpet", "bed", "washing", "laundry", "leak", "pipe", "boiler", "bottle",
           "drink", "pool", "swim", "rain", "garden", "plant", "kettle", "tap", "bill", "meter",
           "softener", "filter", "blue", "green", "boil", "boils", "freeze", "freezes", "salty",
           "taste", "tastes", "hard", "soft", "sea", "hot", "cold", "warm", "lukewarm", "tepid",
           "heating", "cylinder", "immersion", "combi", "radiator", "radiators", "shower", "bath",
           "temperature", "thermal store", "mixing valve", "pressure"),
    ask=("why", "wet")))



ENTRIES.append(entry(
    "molecule-what",
    (("molecule", "molecules"), ("what", "mean", "meaning", "definition", "explain", "made")),
    "A molecule is two or more atoms joined together: two hydrogen atoms and one oxygen make a "
    "water molecule, and DNA is a very long one. The atoms can be the same, as in oxygen gas, or "
    "different, as in water.",
    avoid=("mole", "moles", "skin", "spot", "spots"),
    ask=("what", "mean", "definition", "explain")))

ENTRIES.append(entry(
    "element-what",
    (("element", "elements"), ("what", "mean", "meaning", "definition", "explain",
                              "chemistry", "periodic")),
    "An element is a substance made of just one kind of atom: gold, oxygen and carbon are "
    "elements, and there are 118 known. A chemical reaction can join elements to other elements, "
    "but it cannot split one element into a simpler substance.",
    avoid=("element of surprise", "in my element", "out of my element", "heating element",
           "element of risk", "the element"),
    ask=("what", "mean", "definition", "explain"),
    bias=1))

ENTRIES.append(entry(
    "compound-what",
    (("compound", "compounds"), ("what", "mean", "meaning", "definition", "explain",
                                "chemistry", "made")),
    "A compound is two or more different elements chemically joined in fixed proportions: water "
    "is hydrogen and oxygen, and table salt is sodium and chlorine. Unlike a mixture, the elements "
    "in a compound cannot be separated just by filtering or boiling.",
    avoid=("interest", "money", "savings", "save", "loan", "bank", "rate", "mortgage",
           "invest", "fracture"),
    ask=("what", "mean", "definition", "explain"),
    bias=4))

ENTRIES.append(entry(
    "chemical-reaction-what",
    (("chemical reaction", "chemical reactions", "chemical change", "chemical changes"),
     ("what", "mean", "meaning", "definition", "explain", "happen", "example")),
    "A chemical reaction is when substances rearrange their atoms to make new ones: bonds break, "
    "new bonds form, and the starting materials are used up. Burning, rusting, baking and "
    "digestion are all reactions, and they usually give out or take in heat.",
    avoid=("periodic table", "element", "atom", "lab report", "experiment", "school"),
    ask=("what", "mean", "explain"),
    bias=1))

ENTRIES.append(entry(
    "acid-what",
    (("acid", "acids", "acidic"), ("what", "mean", "meaning", "definition", "explain",
                                  "strong", "weak", "ph")),
    "An acid is a substance that releases hydrogen ions when it dissolves in water: it tastes "
    "sour, turns blue litmus red, and reacts with a base to make a salt and water. Vinegar, lemon "
    "juice and stomach acid are weak acids; car battery acid is strong.",
    avoid=("rain", "heartburn", "reflux", "indigestion", "stomach", "battery", "lsd", "trip",
           "amino", "fatty", "folic", "uric", "acid house"),
    ask=("what", "mean", "definition", "explain"),
    bias=2))

ENTRIES.append(entry(
    "base-chemistry",
    (("base", "bases", "alkali", "alkalis", "alkaline"),
     ("what", "mean", "meaning", "definition", "explain", "chemistry", "acid", "ph")),
    "A base is the opposite of an acid: it takes hydrogen ions, turns red litmus blue, and reacts "
    "with an acid to make a salt and water. An alkali is a base that dissolves in water, such as "
    "baking soda or bleach.",
    avoid=("military", "army", "navy", "air force", "baseball", "database", "home base",
           "touch base", "base rate", "customer base", "tax base", "knowledge base",
           "base camp", "london", "manchester", "birmingham", "office", "hotel", "city",
           "make up", "makeup", "foundation", "primer", "concealer", "in maths", "maths",
           "math", "logarithm",
           "concrete", "cement", "mortar", "ballast", "postcrete", "shed", "shed base",
           "sheds", "patio", "footing", "footings", "slab", "slabs", "drive", "driveway",
           "brick", "bricks", "garden wall", "retaining wall", "damp course"),
    ask=("what", "mean", "definition", "explain"),
    bias=3))

ENTRIES.append(entry(
    "magnetism-what",
    (("magnetism", "magnetic field", "magnetic force"),
     ("what", "mean", "meaning", "definition", "explain", "work", "works")),
    "Magnetism is the force a magnet exerts on other magnets and on iron, nickel and cobalt, "
    "carried by a magnetic field around the magnet. Like poles repel and opposite poles attract, "
    "and a compass needle is a tiny magnet lining up with Earth's field.",
    avoid=("fridge", "freezer", "seal", "strip", "door", "phone", "card", "train",
           "mri", "scan", "scans", "hospital", "hospitals"),
    ask=("what", "mean", "explain"),
    bias=2))

ENTRIES.append(entry(
    "sound-what",
    (("sound", "sound wave", "sound waves"),
     ("what", "mean", "meaning", "definition", "explain", "made", "cause", "hear")),
    "Sound is a pressure wave travelling through air, water or a solid: something vibrates, "
    "pushes the particles next to it, and the push travels outwards. It cannot cross a vacuum, "
    "and it goes faster through water and solids than through air.",
    avoid=("alarm", "smoke alarm", "notification", "ringtone", "keyboard", "video call",
           "speaker", "speakers", "headphones", "tv", "telly", "loud", "quiet", "noise",
           "like", "sounds like", "safe and sound", "soundproof", "sound bar", "soundbar",
           "travel", "travels", "speed", "through", "vacuum", "hearing", "ear", "ears",
           "proof", "proofing", "sound proof"),
    ask=("what", "mean", "definition", "explain"),
    bias=2))

ENTRIES.append(entry(
    "light-what",
    (("light", "visible light"),
     ("what", "mean", "meaning", "definition", "explain", "made", "nature", "particle",
      "wave", "photon")),
    "Light is a form of energy that travels as a wave and also as particles called photons, at "
    "about 300,000 km a second in a vacuum. It carries colour, lets us see, and is only a tiny "
    "part of the electromagnetic spectrum.",
    avoid=("speed", "how fast", "fast", "travel", "houseplant", "plant", "window", "windowsill",
           "bulb", "bulbs", "lamp", "switch", "fitting", "traffic", "light blue", "light meal",
           "light headed", "lightheaded", "blocking", "sunlight", "year", "years",
           "light year", "light years", "how far", "distance", "far", "away", "long",
           "kitchen", "bathroom", "hall", "hallway", "ceiling", "bedside", "fairy lights",
           "christmas lights",
           "dinner", "dinners", "lunch", "lunches", "supper", "breakfast", "meal", "meals",
           "diet", "calorie", "calories", "eating", "im watching what i eat",
           "engine", "engine light", "warning light", "warning lights", "dashboard",
           "dash light", "on the dash", "on my dash", "headlight", "headlights",
           "brake light", "brake lights", "mot",
           "oil", "oil light", "oil pressure", "pressure light", "coolant", "temperature light",
           "battery light", "abs light", "airbag light", "glow plug", "dpf light", "warning",
           "traction light", "handbrake light", "dipped beam", "indicator", "indicators"),
    ask=("what", "mean", "definition", "explain"),
    bias=4))

ENTRIES.append(entry(
    "force-what",
    (("force", "forces"), ("what", "mean", "meaning", "definition", "explain", "physics",
                          "newton", "newtons")),
    "A force is a push or a pull that can change an object's speed, direction or shape, measured "
    "in newtons. Gravity, friction and the push of a hand are all forces, and an object with no "
    "net force keeps doing what it was doing.",
    avoid=("air force", "workforce", "work force", "police force", "force of habit",
           "force quit", "force close", "force stop", "by force", "task force",
           "driving force", "armed forces", "labour force", "labor force", "sales force",
           "majeure"),
    ask=("what", "mean", "definition", "explain"),
    bias=2))

ENTRIES.append(entry(
    "pressure-what",
    (("pressure",), ("what", "mean", "meaning", "definition", "explain", "physics",
                     "measure", "measured", "formula")),
    "Pressure is force spread over an area: the same push on a smaller area gives a higher "
    "pressure, which is why a knife cuts and a wide boot does not sink into snow. It is measured "
    "in pascals, and in a fluid it rises with depth.",
    avoid=("blood pressure", "blood", "peer pressure", "pressure washer", "washer", "tyre",
           "tire", "water pressure", "gas pressure", "boiler", "tap", "shower", "time pressure",
           "under pressure", "pressure to", "high pressure", "low pressure", "pension",
           "cooker", "headache", "behind my eyes", "ear", "ears", "pan",
           "do about", "what should i do", "what shud i do", "fix", "fault", "keeps dropping",
           "keeps droppin", "droppin", "dropin", "dropping"),
    ask=("what", "mean", "definition", "explain"),
    bias=2))

ENTRIES.append(entry(
    "density-what",
    (("density",), ("what", "mean", "meaning", "definition", "explain", "measure",
                    "measured", "formula", "water")),
    "Density is how much mass is packed into a volume: a block of iron and a block of foam the "
    "same size have very different densities. Water has a density of about 1 kg per litre, which "
    "is why things less dense than water float.",
    avoid=("population", "housing", "traffic", "urban", "city", "cities", "bone", "breast"),
    ask=("what", "mean", "definition", "explain"),
    bias=2))

ENTRIES.append(entry(
    "wave-what",
    (("wave", "waves"), ("what", "mean", "meaning", "definition", "explain", "physics",
                         "type", "types")),
    "A wave is a moving disturbance that carries energy without carrying the material with it: a "
    "sound wave is air particles pushing and pulling, and a water wave is the surface moving up "
    "and down while the water stays roughly in place. Light is a wave too, and so is a radio "
    "signal.",
    avoid=("wave to", "wave goodbye", "heat wave", "heatwave", "wave of", "new wave",
           "microwave", "tsunami", "tidal wave", "shock wave", "crime wave", "wave at",
           "hand", "flag", "hello", "goodbye", "hair", "curls", "curly", "perm", "permanent",
           "straighteners", "straightener"),
    ask=("what", "mean", "definition", "explain"),
    bias=3))

ENTRIES.append(entry(
    "star-what",
    (("star", "stars"), ("what", "mean", "meaning", "definition", "explain", "made",
                        "how", "formed")),
    "A star is a huge ball of gas held together by gravity, with fusion in its core turning "
    "hydrogen into helium and giving out light and heat. The Sun is the nearest star, and stars "
    "look small only because they are very far away.",
    avoid=("sign", "signs", "horoscope", "zodiac", "wars", "trek", "movie", "film", "pop",
           "rock", "football", "rating", "ratings", "review", "reviews", "five star",
           "5 star", "star of", "lucky", "shooting", "falling", "twinkle",
           "north star", "how many", "count", "night", "sky"),
    ask=("what", "mean", "definition", "explain"),
    bias=2))

ENTRIES.append(entry(
    "ecosystem-what",
    (("ecosystem", "ecosystems", "eco system", "eco systems"),
     ("what", "mean", "meaning", "definition", "explain", "example")),
    "An ecosystem is a community of living things plus the non-living parts they depend on - "
    "soil, water, air and sunlight - interacting in one place. A pond, a woodland and a garden "
    "are ecosystems, and they work because energy flows through them and materials are recycled.",
    avoid=("business", "digital", "startup", "start up", "company", "app", "software"),
    ask=("what", "mean", "definition", "explain"),
    bias=1))

ENTRIES.append(entry(
    "natural-selection-what",
    (("natural selection",), ("what", "mean", "meaning", "definition", "explain", "work",
                            "works", "how", "evolution")),
    "Natural selection is how evolution works: individuals vary, the ones whose variations suit "
    "their surroundings have more surviving young, and those variations become common over "
    "generations. It is not a plan or a choice - the environment simply filters what is already "
    "there.",
    avoid=("selection box", "select", "choose", "chosen", "job", "team", "school"),
    ask=("what", "mean", "explain"),
    bias=1))
ENTRIES.append(entry(
    "light-year",
    (("light year", "light years", "lightyear", "lightyears", "light-year"),
     ("what", "how far", "distance", "long", "far", "mean", "meaning", "explain", "measure",
      "many", "km", "kilometres", "kilometers", "miles")),
    "A light year is a distance, not a time: it is how far light travels in a year, about 9.46 "
    "trillion kilometres (5.88 trillion miles). Proxima Centauri, the nearest star after the Sun, "
    "is about 4.2 light years away, and the Milky Way is about 100,000 light years across.",
    avoid=("how fast", "speed", "travel at", "wavelength", "per second", "last year", "this year",
           "next year", "new year"),
    ask=("what", "how far", "distance", "long", "far", "mean", "explain", "measure", "many")))

ENTRIES.append(entry(
    "electric-current",
    (("electric current", "electrical current", "current electricity", "amps", "amperes",
      "ampere", "electric flow"),
     ("what", "mean", "meaning", "definition", "explain", "flow", "measure", "measured", "unit",
      "how")),
    "An electric current is the flow of electric charge: in a wire, electrons drift along and carry "
    "energy from the battery or the mains to whatever is using it. It is measured in amperes (amps), "
    "and a current only flows round a complete circuit.",
    avoid=("account", "bank", "mortgage", "job", "address", "partner", "temperature", "weather",
           "news", "bill", "bills", "tariff", "supplier", "price", "cost", "cheap", "saving"),
    ask=("what", "mean", "definition", "explain", "flow", "measure", "unit", "how")))

ENTRIES.append(entry(
    "electric-shock",
    (("electric shock", "electrical shock", "electrocuted", "electrocution",
      "electricity shock", "electricity shocks", "shock from the socket",
      "shock from the wire", "shock from the plug"),
     ("what", "why", "cause", "get", "happen", "happens", "electricity", "electric", "live",
      "wire", "socket", "plug", "mains", "body")),
    "An electric shock happens when your body becomes part of a circuit: touching something live "
    "lets current flow through you to the ground, and it is the current, not the voltage alone, "
    "that does the harm. Switch the power off at the mains before touching anyone who is still "
    "connected, and call the emergency services if they are unconscious or burned.",
    avoid=("surprise", "surprised", "news", "anaphylactic", "allergic", "bill", "bills",
           "price", "cost", "bleeding", "unconscious", "collapse", "collapsed", "pale",
           "fainting"),
    ask=("what", "why", "cause", "get", "happen", "electricity", "electric", "live", "wire",
         "socket", "plug", "mains")))

ENTRIES.append(entry(
    "gene-what",
    (("gene", "genes", "genetic code"),
     ("what", "mean", "meaning", "definition", "explain", "work", "works", "do", "does", "make",
      "made", "for", "inherit", "inherited")),
    "A gene is a section of DNA that holds the instructions for making one thing the body needs, "
    "usually a protein: eye colour, blood type and how a muscle works all come from genes. You "
    "inherit half your genes from each parent, and they switch on and off depending on the cell.",
    avoid=("jeans", "denim", "trousers", "genealogy", "family tree", "test", "testing", "cancer",
           "brca", "crispr", "edit", "editing", "therapy"),
    ask=DEFINITION_ASK))

ENTRIES.append(entry(
    "blood-types",
    (("blood type", "blood types", "blood group", "blood groups"),
     ("what", "why", "have", "different", "mean", "which", "compatible", "compatibility",
      "transfusion", "donor", "negative", "positive", "rhesus", "rh")),
    "Blood types come from markers on the surface of red blood cells: the ABO system gives A, B, AB "
    "or O, and the rhesus factor adds positive or negative. Your type is inherited, and it matters "
    "for transfusions because the immune system attacks markers it does not recognise; O negative is "
    "the universal red-cell donor, and only a blood test can tell you yours.",
    avoid=("blood pressure", "blood test", "blood in", "blood clot", "period", "donate", "donation",
           "give blood", "needle", "needles"),
    ask=("what", "why", "have", "different", "mean", "which", "compatible", "transfusion",
         "donor")))

ENTRIES.append(entry(
    "cholesterol-what",
    (("cholesterol",), ("what is", "what's", "mean", "meaning", "definition", "explain",
                        "is cholesterol")),
    "Cholesterol is a waxy fat the body needs for cell walls and hormones, and the liver makes most "
    "of it; the rest comes from food. The number that matters most is the LDL ('bad') part, which can "
    "clog arteries, and diet, exercise and sometimes a statin bring it down.",
    avoid=("lower", "reduce", "bring down", "high", "diet", "food", "foods", "eat", "avoid", "help",
           "statin", "statins", "hdl", "ldl", "triglycerides", "level", "levels", "number"),
    ask=("what is", "what's", "mean", "meaning", "definition", "explain"),
    bias=2))

ENTRIES.append(entry(
    "brain-what",
    (("brain", "brains"), ("how", "work", "works", "what", "does", "do", "function", "parts")),
    "The brain is a network of about 86 billion nerve cells that talk to each other through "
    "electrical and chemical signals. Different regions handle different jobs - movement, sight, "
    "language, emotion and memory - and the connections between them are what let you think, learn "
    "and remember; it runs on about 20 percent of the body's energy.",
    avoid=("study", "studying", "revise", "revision", "exam", "exams", "memorise", "memorize",
           "remember", "forget", "forgetting", "learn", "learning", "memory", "dementia",
           "alzheimers", "alzheimer's", "injury", "tumour", "tumor", "stroke", "concussion"),
    ask=DEFINITION_ASK,
    bias=2))

ENTRIES.append(entry(
    "memory-what",
    (("memory",), ("what", "how", "work", "works", "mean", "meaning", "definition", "explain",
                   "stored", "store", "made")),
    "Memory is not one store: short-term memory holds a handful of things for seconds, and long-term "
    "memory is a web of connections between neurons that gets stronger each time you recall it. "
    "Sleep and repetition file it away, and forgetting details is normal - the brain keeps the gist "
    "and drops the rest.",
    avoid=("forget", "forgetting", "forgot", "remember", "remembering", "memorise", "memorize",
           "study", "exam", "my mum", "my dad", "dementia", "alzheimers", "alzheimer's", "loss",
           "losing", "improve", "better", "card", "cards", "ram", "phone", "computer"),
    ask=DEFINITION_ASK,
    bias=2))

ENTRIES.append(entry(
    "mixture-what",
    (("mixture", "mixtures"), ("what", "mean", "meaning", "definition", "explain", "example")),
    "A mixture is two or more substances together that are not chemically joined, so each keeps "
    "its own properties: sand and salt, or air, are mixtures. You can usually separate a mixture "
    "by filtering, sieving or boiling, which you cannot do with a compound.",
    avoid=("cake", "cooking", "recipe", "concrete", "cement", "mortar", "trail mix", "nuts",
           "dj", "djing", "music", "playlist", "track", "song", "set"),
    ask=("what", "mean", "definition", "explain"),
    bias=2))

ENTRIES.append(entry(
    "solution-what",
    (("solution", "solutions"), ("what", "mean", "meaning", "definition", "explain",
                                "chemistry", "made")),
    "A solution is a mixture where one substance dissolves in another: the dissolved substance is "
    "the solute and the liquid it goes into is the solvent. Salt water and sugar water are "
    "solutions, and the dissolved part cannot be filtered out.",
    avoid=("problem", "solve", "solved", "fix", "answer", "software", "it support", "cleaning",
           "cleaner", "contact lens", "saline", "eye", "drops", "your", "maths", "math",
           "equation", "puzzle",
           "drain", "plughole", "blocked", "unblock", "squeak", "squeaky", "hinge", "leak",
           "damp", "condensation", "mould", "weeds", "weed", "stain", "limescale", "scuff",
           "crack"),
    ask=("what", "mean", "definition", "explain"),
    bias=2))

ENTRIES.append(entry(
    "solid-what",
    (("solid", "solids"), ("what", "mean", "meaning", "definition", "explain", "state", "matter")),
    "A solid has a fixed shape and a fixed volume: its particles are packed tightly together and "
    "vibrate in place, which is why a solid keeps its shape unless something pushes or breaks it. "
    "Ice, wood and rock are solids; melting turns a solid into a liquid.",
    avoid=("solid wood", "solid food", "solid fuel", "solid tumour", "solid state drive",
           "solid oak", "solid pine", "solid door", "solid wall", "solid ground", "solid start"),
    ask=("what", "mean", "definition", "explain", "state"),
    bias=2))

ENTRIES.append(entry(
    "liquid-what",
    (("liquid", "liquids"), ("what", "mean", "meaning", "definition", "explain", "state",
                            "matter")),
    "A liquid has a fixed volume but takes the shape of its container: its particles are close "
    "enough to stick together but free to slide past each other. Water, milk and oil are liquids; "
    "heating a liquid enough turns it into a gas.",
    avoid=("liquid diet", "liquid soap", "liquid nitrogen", "liquid oxygen", "liquid gold",
           "liquid lunch", "liquid asset", "liquid cash", "liquid damage", "liquid food"),
    ask=("what", "mean", "definition", "explain", "state"),
    bias=2))

ENTRIES.append(entry(
    "gas-what",
    (("gas", "gases", "gaseous"), ("what", "mean", "meaning", "definition", "explain", "state",
                                   "matter")),
    "A gas has no fixed shape or volume: its particles are far apart and move freely, so a gas "
    "spreads out to fill whatever it is in. Air and steam are gases; cooling a gas enough turns "
    "it into a liquid.",
    avoid=("bill", "boiler", "cooker", "hob", "oven", "leak", "supplier", "meter", "heating",
           "central heating", "price", "cap", "tariff", "cylinder", "canister", "bottle",
           "nitrogen", "oxygen", "laughing gas", "tear gas", "gaslight", "gas fire", "gas safe",
           "gas mark", "roast", "roasting", "bake", "baking", "grill", "grilling", "cook",
           "cooking", "oven temperature"),
    ask=("what", "mean", "definition", "explain", "state"),
    bias=2))

ENTRIES.append(entry(
    "organ-what",
    (("organ", "organs"), ("what", "mean", "meaning", "definition", "explain", "body", "job")),
    "An organ is a part of the body made of several tissues working together for one job: the "
    "heart pumps blood, the lungs take in oxygen and the liver cleans the blood. Your skin is the "
    "largest organ, and organs work together in systems.",
    avoid=("donor", "donation", "transplant", "recipient", "donate", "organ recital", "church",
           "pipe organ", "mouth organ", "hammond", "musical", "music"),
    ask=("what", "mean", "definition", "explain", "body"),
    bias=2))

ENTRIES.append(entry(
    "species-what",
    (("species",), ("what", "mean", "meaning", "definition", "explain", "same", "breed")),
    "A species is a group of living things that can breed together and produce fertile young: "
    "dogs are one species, and a horse and a donkey are different species because their mule "
    "offspring cannot have young. Members of a species share most of their genes.",
    avoid=("endangered", "extinct", "extinction", "invasive", "protected", "rare", "native",
           "introduced", "alien", "conservation", "red list", "bird", "birds", "animal",
           "animals", "plant", "plants", "tree", "trees", "flower", "flowers", "fish", "insect",
           "mushroom", "identify", "this", "that"),
    ask=("what", "mean", "definition", "explain"),
    bias=2))

ENTRIES.append(entry(
    "enzyme-what",
    (("enzyme", "enzymes"), ("what", "mean", "meaning", "definition", "explain", "do", "work")),
    "An enzyme is a protein that speeds up a chemical reaction in a living thing without being "
    "used up itself: amylase in saliva starts breaking down starch, and lactase splits milk "
    "sugar. Each enzyme fits only the substance it acts on, like a key in a lock.",
    avoid=("cleaner", "washing", "detergent", "laundry", "drain", "bio", "powder", "tablet",
           "supplement", "digestive", "digestive enzyme", "bromelain"),
    ask=("what", "mean", "definition", "explain", "do"),
    bias=2))

ENTRIES.append(entry(
    "hormone-what",
    (("hormone", "hormones"), ("what", "mean", "meaning", "definition", "explain", "do", "work")),
    "A hormone is a chemical messenger made by a gland and carried in the blood to switch "
    "something on or off somewhere else: insulin tells cells to take up sugar, and adrenaline "
    "gets the body ready for action. Small amounts can have big effects, and each hormone only "
    "acts on cells that can receive it.",
    avoid=("therapy", "treatment", "imbalance", "hrt", "testosterone", "oestrogen", "estrogen",
           "growth hormone", "thyroid", "menopause", "contraceptive", "replacement"),
    ask=("what", "mean", "definition", "explain", "do"),
    bias=2))

ENTRIES.append(entry(
    "carbohydrate-what",
    (("carbohydrate", "carbohydrates", "carbs"), ("what", "mean", "meaning", "definition",
                                                 "explain", "are", "do")),
    "Carbohydrates are one of the main food groups: sugars and starches that the body breaks "
    "down into glucose for energy. Bread, rice, pasta, potatoes, fruit and sugar are "
    "carbohydrates, and fibre is a carbohydrate the body cannot digest.",
    avoid=("low carb", "low-carb", "cut carbs", "cutting carbs", "count", "counting", "keto",
           "grams", "how many", "diet", "lose weight", "weight loss", "no carb"),
    ask=("what", "mean", "definition", "explain"),
    bias=2))

ENTRIES.append(entry(
    "mineral-what",
    (("mineral", "minerals"), ("what", "mean", "meaning", "definition", "explain", "made",
                               "rock")),
    "A mineral is a natural solid with a definite chemical make-up and a crystal structure, "
    "formed in the earth without anything living making it: quartz, calcite and iron ore are "
    "minerals. A rock is usually a mixture of minerals.",
    avoid=("vitamin", "vitamins", "supplement", "supplements", "deficiency", "water", "drink",
           "food", "diet", "intake", "iron", "calcium", "zinc", "bottle", "spring", "spa"),
    ask=("what", "mean", "definition", "explain"),
    bias=3))

ENTRIES.append(entry(
    "rock-what",
    (("rock", "rocks"), ("what", "mean", "meaning", "definition", "explain", "made", "type")),
    "A rock is a solid piece of the earth made of one or more minerals: granite is mostly quartz "
    "and feldspar, and limestone is mostly calcite. Rocks come in three kinds - igneous from "
    "cooled magma, sedimentary from settled layers, and metamorphic changed by heat and pressure.",
    avoid=("music", "band", "concert", "gig", "album", "song", "rock star", "punk", "indie",
           "climbing", "climb", "bouldering", "cake", "bun", "on the rocks", "rock bottom",
           "rock salt", "rock pool", "rockery", "garden"),
    ask=("what", "mean", "definition", "explain"),
    bias=2))

ENTRIES.append(entry(
    "habitat-what",
    (("habitat", "habitats"), ("what", "mean", "meaning", "definition", "explain", "animal",
                               "live")),
    "A habitat is the place where a plant or animal lives, with the food, water, shelter and "
    "space it needs: a hedge is a habitat for sparrows, and a pond is one for frogs. Different "
    "species are suited to different habitats, and losing a habitat is the biggest threat to "
    "many of them.",
    avoid=("loss", "destruction", "destroy", "destroying", "restore", "restoration", "create",
           "creating", "garden", "pond", "hedge", "wildlife", "project"),
    ask=("what", "mean", "definition", "explain"),
    bias=2))

ENTRIES.append(entry(
    "predator-what",
    (("predator", "predators"), ("what", "mean", "meaning", "definition", "explain", "animal",
                                 "eat")),
    "A predator is an animal that hunts and eats other animals: a fox, an owl and a lion are "
    "predators, and the animals they eat are their prey. Predators keep prey numbers in check, "
    "which is why removing them can upset a whole habitat.",
    avoid=("child", "children", "kid", "kids", "online", "sexual", "grooming", "groomer",
           "drone", "tank", "fish tank", "aquarium", "game", "film", "movie", "alien"),
    ask=("what", "mean", "definition", "explain", "animal"),
    bias=2))

ENTRIES.append(entry(
    "protein-what",
    (("protein", "proteins"), ("what", "mean", "meaning", "definition", "explain", "made",
                               "body", "do")),
    "Protein is a building material made of chains of amino acids: the body uses it to build and "
    "repair muscle, skin, hair and organs, and enzymes are proteins too. Meat, fish, eggs, milk, "
    "beans, lentils, nuts and tofu are good sources.",
    avoid=("how much", "much protein", "grams", "need", "needed", "daily", "day", "powder",
           "shake", "whey", "supplement", "diet", "lose", "weight", "build muscle",
           "vegan", "vegetarian", "deficiency", "kidney", "uric",
           "eat", "eats", "eating", "food", "foods", "meal", "meals", "breakfast", "lunch",
           "dinner", "snack", "snacks", "shop", "shopping", "cook", "cooking", "recipe",
           "recipes", "high in protein", "protein rich", "protein-rich", "source", "sources"),
    ask=("what", "mean", "definition", "explain"),
    bias=3))

ENTRIES.append(entry(
    "vaccine-what",
    (("vaccine", "vaccines", "vaccination", "jab"), ("what", "mean", "meaning", "definition",
                                                    "explain", "work", "do")),
    "A vaccine teaches the immune system to recognise a germ without you having to get the "
    "illness: it shows a harmless part or a weakened version, and the body makes antibodies and "
    "memory cells ready for the real thing. That protection usually takes a few weeks and may "
    "need boosters.",
    avoid=("safe", "safety", "side effect", "side effects", "should i", "should my", "child",
           "children", "baby", "flu", "travel", "pregnant", "autism", "reaction", "passport",
           "certificate", "booster", "booking", "appointment", "nhs"),
    ask=("what", "mean", "definition", "explain"),
    bias=3))

ENTRIES.append(entry(
    "vitamin-what",
    (("vitamin", "vitamins"), ("what", "mean", "meaning", "definition", "explain", "do",
                               "body")),
    "A vitamin is a nutrient the body needs in small amounts and cannot make enough of, so it "
    "has to come from food: vitamin C is in fruit and vegetables, vitamin A in carrots and dairy, "
    "and vitamin D is made in skin from sunlight. A varied diet usually covers them.",
    avoid=("should i", "take", "supplement", "supplements", "deficiency", "deficient", "d3",
           "b12", "vitamin d", "vitamin c", "vitamin b", "folic", "prenatal", "pregnant",
           "child", "baby", "daily", "dose", "tablet", "chewable"),
    ask=("what", "mean", "definition", "explain"),
    bias=3))

ENTRIES.append(entry(
    "metal-what",
    (("metal", "metals"), ("what", "mean", "meaning", "definition", "explain", "made",
                           "properties")),
    "A metal is an element that conducts heat and electricity, is usually shiny, and can be "
    "bent or hammered into shape without breaking: iron, copper, aluminium and gold are metals. "
    "Most elements are metals, and they sit on the left and middle of the periodic table.",
    avoid=("cold", "colder", "taste", "tastes", "detector", "detecting", "recycle", "recycling",
           "scrap", "scrapyard", "precious", "heavy metal", "band", "music", "concert", "gig",
           "roof", "roofing", "sheet", "fence", "gate", "rust", "rusty", "alloy"),
    ask=("what", "mean", "definition", "explain"),
    bias=3))

ENTRIES.append(entry(
    "digestion-what",
    (("digestion", "digestive system", "digest", "digests", "digesting"),
     ("what", "how", "work", "works", "process", "happen", "happens", "mean", "definition",
      "explain", "stomach", "gut", "body")),
    "Digestion is how the body breaks food into pieces small enough to absorb: chewing and stomach "
    "acid start it, enzymes in the small intestine split carbohydrates into sugars, proteins into "
    "amino acids and fats into fatty acids, and the nutrients pass through the gut wall into the "
    "blood. The whole trip usually takes six to eight hours, and fibre and water keep it moving.",
    avoid=("indigestion", "heartburn", "reflux", "acid reflux", "bloating", "constipation",
           "diarrhoea", "diarrhea", "stomach ache", "stomach pain", "ibs", "food poisoning",
           "ulcer", "vomit", "vomiting", "nausea", "medicine", "medication", "tablet", "tablets",
           "supplement", "probiotic", "fibre supplement", "laxative", "news", "book", "books",
           "email", "emails", "information", "read", "reading", "report", "reports", "article",
           "biscuit", "biscuits"),
    ask=DEFINITION_ASK))

ENTRIES.append(entry(
    "voltage-what",
    (("voltage", "volt", "volts", "potential difference"),
     ("what", "how", "mean", "meaning", "definition", "explain", "measure", "measured", "unit",
      "difference", "work")),
    "Voltage is the push that makes electric charge move: it is the difference in electrical energy "
    "between two points, measured in volts (V), and one volt gives one joule of energy to each "
    "coulomb of charge that passes. A AA battery is 1.5 volts and the mains is about 230 volts in "
    "the UK; current is how much charge flows, voltage is how hard it is pushed.",
    avoid=("car", "cars", "battery", "batteries", "charger", "charging", "phone", "laptop",
           "mains", "wiring", "wire", "shock", "electric shock", "fuse", "socket", "plug"),
    ask=DEFINITION_ASK))

ENTRIES.append(entry(
    "watt-what",
    (("watt", "watts", "kilowatt", "kilowatts", "kw", "kwh", "kilowatt hour",
      "kilowatt-hour"),
     ("what", "how", "mean", "meaning", "definition", "explain", "many", "much", "difference",
      "work", "unit", "measure")),
    "A watt is a rate of energy use: one watt is one joule every second, so a 10-watt LED left on "
    "for 100 hours uses one kilowatt-hour, and a unit on your electricity bill is exactly that. "
    "Watts are volts times amps, which is why a 2,400-watt kettle on 230 volts pulls about 10 "
    "amps. A kilowatt is 1,000 watts, and a kWh is a kilowatt for an hour - the number the meter "
    "counts, not the number on the label.",
    avoid=("car", "cars", "battery", "batteries", "charger", "charging", "phone", "laptop",
           "wiring", "wire", "shock", "fuse", "socket", "plug", "boiler", "heater", "bulb",
           "light bulb", "microwave", "kettle"),
    ask=DEFINITION_ASK + ("how many", "how much", "what is a", "whats a", "in a kilowatt",
                          "per hour")))

ENTRIES.append(entry(
    "circuit-what",
    (("circuit", "circuits", "electrical circuit", "electric circuit"),
     ("what", "how", "work", "works", "mean", "meaning", "definition", "explain", "complete",
      "closed", "open", "series", "parallel")),
    "An electric circuit is a complete loop that charge can flow round: a source such as a battery "
    "pushes current out through a wire, through a component such as a bulb, and back to the source. "
    "Break the loop with a switch and the current stops; in a series circuit everything shares one "
    "path, and in a parallel circuit each branch has its own.",
    avoid=("workout", "exercise", "training", "gym", "court", "judge", "legal", "appeal",
           "board", "boards", "soldering", "repair", "repairs", "fuse", "fuse box", "breaker",
           "trips", "tripping", "keeps tripping", "socket", "socket keeps", "light", "lights",
           "short circuit", "short-circuit", "shorts", "electrics", "electrician"),
    ask=DEFINITION_ASK))

ENTRIES.append(entry(
    "conductor-what",
    (("conductor", "conductors", "electrical conductor", "electric conductor", "thermal conductor"),
     ("what", "how", "why", "mean", "meaning", "definition", "explain", "electricity", "heat",
      "material", "materials", "metal", "metals", "copper", "good")),
    "A conductor is a material that lets heat or electricity pass through it easily because some of "
    "its electrons are free to move. Metals are the usual conductors - copper and aluminium carry "
    "current in wires, and a metal pan conducts heat - while materials that hold their electrons "
    "tightly, such as rubber and plastic, are insulators.",
    avoid=("train", "trains", "rail", "railway", "ticket", "tickets", "fare", "orchestra",
           "symphony", "music", "band", "choir", "bus", "driver", "inspector", "concert"),
    ask=DEFINITION_ASK))

ENTRIES.append(entry(
    "insulator-what",
    (("insulator", "insulators", "electrical insulator", "thermal insulator", "insulation"),
     ("what", "how", "why", "mean", "meaning", "definition", "explain", "electricity", "heat",
      "material", "materials", "good", "plastic", "rubber", "keeps")),
    "An insulator is a material that does not let heat or electricity pass through it easily because "
    "its electrons are not free to move. Plastic and rubber insulate electrical wires, and trapped "
    "air in foam, wool or double glazing slows heat loss; that is why a woolly jumper keeps you warm "
    "and a plastic handle lets you hold a hot pan.",
    avoid=("loft", "attic", "wall", "walls", "roof", "house", "home", "cavity", "boiler", "pipe",
           "pipes", "cost", "grant", "install", "installation", "damp", "floor", "floors",
           "garage", "conservatory", "how much"),
    ask=DEFINITION_ASK))

ENTRIES.append(entry(
    "shadow-what",
    (("shadow", "shadows", "shadow form", "shadow made"),
     ("what", "how", "why", "make", "makes", "made", "form", "formed", "mean", "definition",
      "explain", "light", "sun", "lamp")),
    "A shadow is the patch where an object blocks light: light travels in straight lines, so an "
    "opaque object stops the rays and leaves a dark shape behind it. The shadow is biggest when the "
    "light source is close to the object and the surface is far behind, and a point of light gives a "
    "sharper edge than a wide one.",
    avoid=("eyes", "eye", "under my eyes", "dark circles", "makeup", "eyeshadow", "eye shadow",
           "face", "sunken", "tired", "panda eyes", "concealer", "cabinet", "minister",
           "government", "politics", "shadow ban", "shadowban", "five o'clock", "doubt",
           "shadow work", "therapy", "journal"),
    ask=DEFINITION_ASK))

ENTRIES.append(entry(
    "reflection-what",
    (("reflection", "reflections", "reflect", "reflects", "reflected", "mirror", "mirrors"),
     ("what", "how", "why", "work", "works", "mean", "meaning", "definition", "explain", "light",
      "mirror", "mirrors", "water", "surface")),
    "Reflection is light bouncing off a surface: the ray hits the surface and leaves at the same "
    "angle on the other side of an imaginary line straight up from it. A smooth surface such as a "
    "mirror reflects the rays in one direction and gives a clear image; a rough surface scatters them "
    "and gives a duller, softer one.",
    avoid=("self reflection", "self-reflection", "journal", "journaling", "diary", "essay",
           "feedback", "performance", "behaviour", "behavior", "yourself", "myself", "my life",
           "how do i reflect", "write a reflection", "reflective essay", "hang", "hanging",
           "wall", "bathroom", "buy", "clean", "cleaning", "mirror cabinet", "mirror ball",
           "stop", "stops", "stopping", "prevent", "prevents", "fog", "fogging", "fogged",
           "foggy", "steaming up", "misted", "misty",
           "hairspray", "hair spray", "toothpaste", "marks", "mark", "dirty", "smudge",
           "smudges", "washed", "washes"),
    ask=DEFINITION_ASK,
    bias=2))

ENTRIES.append(entry(
    "osmosis-what",
    (("osmosis",), ("what", "is", "work", "works", "mean", "explain", "water")),
    "Osmosis is water moving through a thin membrane from where there is more of it to where there is "
    "less, until the two sides even out. A raisin plumps up in water and a slug shrivels in salt for "
    "the same reason: the water follows the salt. That is also how a plant's roots drink, and why a "
    "wilted lettuce leaf firms up in cold water.",
    ask=("what", "work", "works", "mean", "explain", "how"),
    bias=2))

ENTRIES.append(entry(
    "diffusion-what",
    (("diffusion",), ("what", "is", "work", "works", "mean", "explain", "spread", "spreads",
                     "smell")),
    "Diffusion is particles spreading out on their own from where there are many of them to where "
    "there are few, because they are always moving. A drop of ink colours a whole glass of water "
    "without stirring, and the smell of toast reaches the next room the same way. Warmer means "
    "faster, which is why tea brews quicker in hot water.",
    ask=("what", "work", "works", "mean", "explain", "how"),
    bias=2))

ENTRIES.append(entry(
    "neuron-what",
    (("neuron", "neurons", "nerve cell", "nerve cells", "synapse", "synapses"),
     ("what", "are", "do", "does", "work", "works", "mean", "explain")),
    "A neuron is a nerve cell: a long strand that carries an electrical pulse from one end to the "
    "other and passes it on to the next cell through a tiny gap called a synapse, using a chemical. "
    "You have around 86 billion of them, and learning is the connections between them getting "
    "stronger with use.",
    ask=("what", "are", "do", "does", "work", "works", "mean", "explain"),
    bias=2))

ENTRIES.append(entry(
    "chromosome-what",
    (("chromosome", "chromosomes"), ("what", "are", "do", "does", "many", "mean", "explain")),
    "A chromosome is one long tightly wound packet of DNA; humans have 46 of them in most cells, in "
    "23 pairs, with one of each pair from each parent. They are the filing system that lets a cell "
    "copy all its instructions without tangling them, and the sex chromosomes are the pair that "
    "decides whether you develop as male or female.",
    ask=("what", "are", "do", "does", "many", "mean", "explain"),
    bias=2))

ENTRIES.append(entry(
    "rna-what",
    (("rna",), ("what", "is", "do", "does", "mean", "explain", "dna", "differ", "difference")),
    "RNA is DNA's working copy: the same four-letter code, but single-stranded and short-lived. A "
    "cell copies the gene it needs into RNA, carries it out of the nucleus and builds a protein from "
    "it, which is why a cell can keep its DNA safe and still make what it needs. Some viruses, "
    "including the cold and flu viruses, store their instructions as RNA instead.",
    ask=("what", "is", "do", "does", "mean", "explain", "difference", "how"),
    bias=2))

ENTRIES.append(entry(
    "isotope-what",
    (("isotope", "isotopes", "radioisotope", "radioactive"), ("what", "are", "do", "mean",
                                                              "explain", "difference")),
    "Isotopes are versions of the same element with different numbers of neutrons, so the same "
    "chemistry but a different weight. Carbon-12 and carbon-14 both behave like carbon, but "
    "carbon-14 is unstable and decays at a steady rate, which is how archaeologists date old bone "
    "and wood. Some isotopes are radioactive enough to be useful in medicine and power, and some "
    "are harmless.",
    avoid=("carbon dating", "how does carbon dating", "radon", "radiotherapy", "cancer", "x-ray"),
    ask=("what", "are", "do", "mean", "explain", "difference"),
    bias=2))

ENTRIES.append(entry(
    "ion-what",
    (("ion", "ions"), ("what", "are", "do", "mean", "explain", "charge", "charged")),
    "An ion is an atom or molecule that has lost or gained electrons, which leaves it with an "
    "electrical charge. Table salt is sodium ions and chloride ions held together by that charge, "
    "and the ions in seawater are what make it conduct electricity. Your nerves and muscles work by "
    "shuffling ions in and out through their membranes.",
    ask=("what", "are", "do", "mean", "explain", "charge", "charged", "how"),
    bias=2))

ENTRIES.append(entry(
    "catalyst-what",
    (("catalyst", "catalysts", "catalyse", "catalyze", "catalysis"),
     ("what", "do", "does", "mean", "explain", "work", "works")),
    "A catalyst speeds up a reaction and comes out of it unchanged, so a small amount does the job "
    "over and over. It works by giving the molecules an easier route, which means the reaction can "
    "happen at a lower temperature. Enzymes are nature's catalysts and the catalytic converter on a "
    "car uses metals to turn exhaust fumes into less harmful gases.",
    ask=("what", "do", "does", "mean", "explain", "work", "works"),
    bias=2))

ENTRIES.append(entry(
    "soil-what",
    (("soil",), ("what", "is", "made", "mean", "explain", "difference", "form", "formed")),
    "Soil is crushed rock mixed with rotted plant and animal matter, plus air, water and a vast "
    "number of microbes. The rotted part, humus, is what holds water and feeds plants, and it takes "
    "hundreds of years to build up an inch of it. A handful of healthy soil has more living things in "
    "it than there are people on Earth.",
    avoid=("garden", "plant", "plants", "pot", "pots", "compost", "clay", "sandy", "chalk",
           "for", "need", "needs", "should", "best", "good", "want", "wants",
           "improve", "test", "ph", "mulch", "border", "lawn", "veg", "vegetable", "seed",
           "sow", "grow", "dig", "weed",
           "my soil", "the soil", "this soil", "dry", "wet", "soggy", "poor", "acid", "alkaline",
           "erosion", "eroded", "pollution", "polluted"),
    ask=("what", "is", "made", "mean", "explain", "difference", "form", "formed"),
    bias=2))


ENTRIES.append(entry(
    "mammal-what",
    (("mammal", "mammals", "mammalian"),
     ("what", "define", "definition", "mean", "meaning", "explain", "called", "animal",
      "animals", "science", "warm", "fur", "milk")),
    "A mammal is a warm-blooded animal with a backbone that has hair or fur and feeds its young on "
    "milk. Almost all give birth to live young rather than laying eggs, and they keep a steady body "
    "temperature - which is why a whale is a mammal even though it lives in the sea, and a bat is "
    "one even though it flies.",
    ask=DEFINITION_ASK))

ENTRIES.append(entry(
    "reptile-what",
    (("reptile", "reptiles", "reptilian"),
     ("what", "define", "definition", "mean", "meaning", "explain", "called", "animal",
      "animals", "science", "cold", "scales", "eggs")),
    "A reptile is a cold-blooded animal with a backbone and dry, scaly skin. It cannot keep its own "
    "body temperature, so it warms up in the sun, and most lay leathery eggs on land - lizards, "
    "snakes, turtles and crocodiles are the groups.",
    avoid=("brain", "lizard brain", "alien", "aliens", "person", "people",
           "house", "reptile house", "zoo", "vivarium", "pet shop", "enclosure"),
    ask=DEFINITION_ASK))

ENTRIES.append(entry(
    "amphibian-what",
    (("amphibian", "amphibians"),
     ("what", "define", "definition", "mean", "meaning", "explain", "called", "animal",
      "animals", "science", "water", "land", "frog", "frogs")),
    "An amphibian is a cold-blooded animal with moist skin that lives part of its life in water and "
    "part on land. Frogs, toads and newts hatch as tadpoles with gills, then change into adults with "
    "lungs, and their skin has to stay damp, which is why you find them near ponds and in wet grass.",
    avoid=("vehicle", "car", "cars", "plane", "planes", "boat", "boats", "amphibious"),
    ask=DEFINITION_ASK))

ENTRIES.append(entry(
    "insect-what",
    (("insect", "insects"),
     ("what", "define", "definition", "mean", "meaning", "explain", "called", "animal",
      "animals", "science", "body", "legs", "wings")),
    "An insect is a small animal with a hard outer skeleton and three body parts - head, thorax and "
    "abdomen - with six legs and usually two pairs of wings. Beetles, bees, ants and butterflies are "
    "insects; a spider is not, because it has eight legs and two body parts.",
    avoid=("bite", "bites", "bitten", "sting", "stings", "stung", "pest", "pests", "infestation",
           "infestation", "kill", "get rid", "in my house", "in the house", "spider", "spiders"),
    ask=DEFINITION_ASK))

ENTRIES.append(entry(
    "bird-what",
    (("bird", "birds"),
     ("what", "define", "definition", "mean", "meaning", "explain", "called", "animal",
      "animals", "science", "feathers", "wings", "fly", "flies")),
    "A bird is a warm-blooded animal with feathers, a beak and two wings, and it lays hard-shelled "
    "eggs. All birds have feathers and none has teeth, and most can fly - though ostriches, penguins "
    "and kiwi cannot.",
    avoid=("bird flu", "flu", "table", "spotting", "watching", "watching", "feed", "feeder",
           "feeder", "bath", "nest", "nests", "cage", "aviary", "chicken", "chickens", "turkey",
           "window", "windows", "glass", "flew into", "flew at", "flew in", "hit my window",
           "hits my window", "hit the window", "crashed into", "stunned", "dead bird"),
    ask=DEFINITION_ASK))


ENTRIES.append(entry(
    "bird-at-the-window",
    (("bird", "birds", "pigeon", "sparrow", "blackbird", "robin", "starling", "swallow"),
     ("window", "windows", "glass", "flew into", "flew at", "hit the window", "hit my window",
      "hits the window", "crashed", "stunned", "dead", "flying into",
      "stickers", "sticker", "tape", "silhouette", "silhouettes", "box", "the box",
      "still there", "sitting there", "hasnt moved", "hasn't moved", "let it go")),
    ("A window acts like a mirror: it reflects the sky and the trees you have behind you, so a bird "
     "flies at what looks like more trees. Put something on the outside of the glass - stickers, "
     "tape, a hanging silhouette - because one on the inside does nothing. If the bird is alive and "
     "stunned, put it in a box with air holes in a warm, dark, quiet place and leave it an hour or "
     "two; most fly off, and one that has not gone by then wants a wildlife rescue or a vet. A "
     "feeder within a metre of the window, or past three metres, helps too. It is not a sign of "
     "anything."),
    avoid=("eat", "recipe", "cook", "feed", "feeder", "table", "nest", "nests", "cage",
           "chicken", "chickens", "turkey", "bird flu", "keep", "keeping", "as a pet",
           "dog", "dogs", "doggy", "cat", "cats", "kitten", "puppy", "pup",
           "brought in", "brought it in", "brought me", "brings in", "brings me", "bringing in",
           "carried in", "left it", "left a", "left me", "on the mat", "on the doormat",
           "doorstep", "door step", "at the door", "in the house", "in the kitchen",
           "poo", "poos", "mess", "droppings", "dirt", "muck", "clean", "cleaning", "clean off",
           "wash", "washing", "smear", "smears", "squeegee", "wipes", "wipe"),
    bias=2))

ENTRIES.append(entry(
    "a-stunned-bird",
    (("bird", "birds", "pigeon", "sparrow", "blackbird", "robin", "starling", "swallow"),
     ("stunned", "stunned bird", "sitting there", "still there", "hasnt moved", "hasn't moved",
      "not moving", "the box", "in a box", "let it go", "what do i do with", "wont fly",
      "won't fly", "on the path", "on the ground")),
    ("Put it in a cardboard box with air holes in the lid, somewhere warm, dark and quiet, and "
     "leave it an hour or two: most come round and fly off. Do not feed it or try to give it "
     "water, and do not keep it longer than a few hours - one that is still there after that "
     "wants a wildlife rescue or a vet. Wash your hands afterwards. Then stop the next one: "
     "something on the outside of the glass, because a pane reflects the sky and the birds fly "
     "at it."),
    avoid=("eat", "recipe", "cook", "feed", "feeder", "table", "nest", "nests", "cage",
           "chicken", "chickens", "turkey", "bird flu", "keep", "keeping", "as a pet",
           "poo", "poos", "mess", "droppings", "dirt", "muck", "clean", "cleaning", "clean off",
           "wash", "washing", "smear", "smears", "squeegee", "wipes", "wipe"),
    bias=3))

ENTRIES.append(entry(
    "fish-what",
    (("fish", "fishes"),
     ("what", "define", "definition", "mean", "meaning", "explain", "called", "animal",
      "animals", "science", "water", "gills", "fins")),
    "A fish is a cold-blooded animal with a backbone that lives in water and breathes through gills. "
    "It has fins to swim and usually scales, and most lay eggs; a whale or a dolphin is not a fish "
    "because it breathes air and feeds its young on milk.",
    avoid=("eat", "eats", "cook", "cooking", "recipe", "fry", "fried", "bake", "baked", "chips",
           "pet", "pets", "tank", "tanks", "aquarium", "pond",
           "catch", "caught", "market", "monger", "mongers", "oil", "omega", "finger", "fingers",
           "slice", "fillet", "fillets", "smell", "smells", "sick", "ill", "dying", "dead"),
    ask=DEFINITION_ASK))

ENTRIES.append(entry(
    "planet-what",
    (("planet", "planets"),
     ("what", "define", "definition", "mean", "meaning", "explain", "called", "space",
      "science", "solar", "sun", "star", "orbit")),
    "A planet is a large round body that orbits a star and has cleared other objects out of its own "
    "orbit. There are eight in our solar system - Mercury, Venus, Earth, Mars, Jupiter, Saturn, "
    "Uranus and Neptune - and Pluto is a dwarf planet because it shares its orbit with other icy "
    "bodies.",
    avoid=("fitness", "gym", "hollywood", "daily planet", "bank", "insurance"),
    ask=DEFINITION_ASK))

ENTRIES.append(entry(
    "orbit-what",
    (("orbit", "orbits", "orbiting"),
     ("what", "define", "definition", "mean", "meaning", "explain", "called", "space",
      "science", "earth", "sun", "moon", "satellite", "gravity")),
    "An orbit is the curved path one object takes around another because gravity pulls it inward "
    "while its sideways speed carries it forward. The Moon orbits Earth about once a month, and "
    "Earth orbits the Sun once a year at about 30 kilometres a second.",
    avoid=("gum", "chewing", "chewing gum", "brand", "sugar free", "sugar-free", "tube"),
    ask=DEFINITION_ASK))

ENTRIES.append(entry(
    "solar-system-what",
    (("solar system", "the solar system", "our solar system"),
     ("what", "define", "definition", "mean", "meaning", "explain", "called", "space",
      "science", "sun", "planets", "made", "how")),
    "The solar system is the Sun and everything held in orbit around it by its gravity: eight "
    "planets, their moons, dwarf planets such as Pluto, and billions of asteroids and comets. It "
    "formed about 4.6 billion years ago from a cloud of gas and dust, and the Sun holds 99.8% of its "
    "mass.",
    avoid=("panel", "panels", "solar panel", "solar panels", "install", "installation", "cost",
           "quote", "roof", "home", "house", "battery", "inverter", "tariff"),
    ask=DEFINITION_ASK))

ENTRIES.append(entry(
    "asteroid-what",
    (("asteroid", "asteroids"),
     ("what", "define", "definition", "mean", "meaning", "explain", "called", "space",
      "science", "rock", "space", "belt", "meteor", "planet")),
    "An asteroid is a lump of rock and metal left over from the birth of the solar system, smaller "
    "than a planet and usually irregular in shape. Most circle the Sun in the asteroid belt between "
    "Mars and Jupiter; one that enters Earth's atmosphere and burns up is a meteor, and one that "
    "lands is a meteorite.",
    avoid=("mining", "mine", "game", "games", "film", "movie", "documentary"),
    ask=DEFINITION_ASK))

ENTRIES.append(entry(
    "evaporation-what",
    (("evaporation", "evaporate", "evaporates", "evaporating"),
     ("what", "define", "definition", "mean", "meaning", "explain", "called", "science",
      "water", "liquid", "gas", "heat", "sun")),
    "Evaporation is a liquid turning into a gas at its surface, without needing to reach boiling "
    "point. Water left in a glass disappears over days because the fastest molecules escape into the "
    "air; warmth, wind and a larger surface make it happen faster, which is why washing dries on a "
    "line.",
    avoid=("milk", "evaporated milk", "recipe", "cook", "cooking", "pan", "sauce", "soup",
           "puddle", "spill", "spilled", "smell", "odour", "odor"),
    ask=DEFINITION_ASK))

ENTRIES.append(entry(
    "condensation-what",
    (("condensation", "condense", "condenses", "condensing"),
     ("what", "define", "definition", "mean", "meaning", "explain", "called", "science",
      "water", "liquid", "gas", "cool", "cold")),
    "Condensation is a gas turning back into a liquid when it cools. Warm air holds water vapour, "
    "and when it meets a cold surface the vapour loses heat and forms droplets - that is the mist on "
    "a bathroom mirror, the water on a cold glass, and the clouds in the sky.",
    avoid=("stop", "stops", "prevent", "reduce", "get rid", "damp", "mould", "mold", "window",
           "windows", "wall", "walls", "boiler", "pipe", "pipes", "car", "headlight",
           "headlights", "dryer", "tumble dryer", "dehumidifier", "loft", "ceiling"),
    ask=DEFINITION_ASK))
ENTRIES.append(entry(
    "life-cycle-what",
    (("life cycle", "life cycles", "lifecycle", "lifecycles"),
     ("what", "mean", "meaning", "definition", "explain", "stages", "animal", "plant")),
    "A life cycle is the stages a living thing goes through from one generation to the next: a "
    "frog goes egg, tadpole, froglet, adult, and a butterfly goes egg, caterpillar, chrysalis, "
    "butterfly. A plant's is seed, seedling, flowering plant, then seed again. The adult stage is "
    "the one that makes the next generation, which is what closes the circle.",
    avoid=("washing machine", "washer", "dishwasher", "tumble dryer", "drying", "spin",
           "menstrual", "period", "periods", "carbon", "assessment", "product", "products",
           "laundry", "clothes", "machine", "processor", "cpu", "duty"),
    ask=DEFINITION_ASK,
    bias=2))

ENTRIES.append(entry(
    "triangle-what",
    (("triangle", "triangles"),
     ("what", "mean", "meaning", "definition", "explain", "type", "types", "kind", "kinds",
      "angles", "sides")),
    "A triangle is a flat shape with three straight sides and three corners, and its three angles "
    "always add up to 180 degrees. By its sides it is equilateral (all three equal), isosceles "
    "(two equal) or scalene (all different); by its angles it is acute, right-angled or obtuse.",
    avoid=("love triangle", "roof", "roofing", "sandwich", "toastie", "warning", "road",
           "sign", "yoga", "pose", "garden", "land", "plot", "field", "bermuda", "area",
           "perimeter", "hypotenuse", "pythagoras"),
    ask=DEFINITION_ASK,
    bias=2))

ENTRIES.append(entry(
    "quadrilateral-what",
    (("quadrilateral", "quadrilaterals"),
     ("what", "mean", "meaning", "definition", "explain", "type", "types", "kind", "kinds",
      "sides")),
    "A quadrilateral is a flat shape with four straight sides and four corners, and its angles add "
    "up to 360 degrees. Squares, rectangles, parallelograms, rhombuses, trapeziums and kites are all "
    "quadrilaterals; a shape with four sides that is not a quadrilateral does not exist.",
    avoid=("garden", "land", "plot", "field", "room", "floor", "table", "rug", "tile",
           "tiles", "area", "perimeter"),
    ask=DEFINITION_ASK,
    bias=2))

ENTRIES.append(entry(
    "diameter-what",
    (("diameter", "diameters"),
     ("what", "mean", "meaning", "definition", "explain", "radius", "circle", "difference")),
    "The diameter is the distance straight across a circle through its centre, and it is twice the "
    "radius. A circle 10 cm across has a radius of 5 cm and a circumference of about 31.4 cm, "
    "because circumference is pi times the diameter.",
    avoid=("pipe", "pipes", "hose", "wire", "cable", "tree", "trunk", "hole", "drill", "bit",
           "saw", "pizza", "cake", "tin", "pan", "wheel", "tyre", "tire"),
    ask=DEFINITION_ASK,
    bias=2))

ENTRIES.append(entry(
    "vertebrate-what",
    (("vertebrate", "vertebrates"),
     ("what", "mean", "meaning", "definition", "explain", "animal", "animals")),
    "A vertebrate is an animal with a backbone: fish, amphibians, reptiles, birds and mammals are "
    "the five groups. The backbone is a column of bones or cartilage that protects the spinal cord, "
    "and it lets the animal grow large and move actively.",
    avoid=("invertebrate", "invertebrates", "pet", "dog", "cat", "horse", "back pain", "spine",
           "surgery", "injury", "fracture"),
    ask=DEFINITION_ASK,
    bias=2))

ENTRIES.append(entry(
    "invertebrate-what",
    (("invertebrate", "invertebrates"),
     ("what", "mean", "meaning", "definition", "explain", "animal", "animals")),
    "An invertebrate is an animal with no backbone: insects, spiders, worms, snails, crabs, "
    "jellyfish and squid are all invertebrates. They are most of the animal species on Earth, and "
    "many have a hard shell or exoskeleton instead of bones.",
    avoid=("pet", "dog", "cat", "horse", "back pain", "spine", "surgery", "injury"),
    ask=DEFINITION_ASK,
    bias=2))

ENTRIES.append(entry(
    "erosion-what",
    (("erosion", "erode", "eroding", "eroded"),
     ("what", "mean", "meaning", "definition", "explain", "cause", "causes", "coast",
      "soil", "rock", "land")),
    "Erosion is the wearing away and moving of rock, soil or sand by water, wind, ice or waves: "
    "rain washing soil off a bare field, or a river cutting into its banks. The material is then "
    "dropped somewhere else, which is deposition, and planting cover or slowing the water is the "
    "usual defence.",
    avoid=("tooth", "teeth", "enamel", "acid", "gum", "dental", "dentist", "rights",
           "confidence", "trust", "market", "profit", "brand", "relationship", "friendship",
           "democracy", "freedoms"),
    ask=DEFINITION_ASK,
    bias=2))

ENTRIES.append(entry(
    "moon-orbit",
    (("what keeps the moon", "what holds the moon", "how does the moon stay",
      "how does the moon keep", "what makes the moon stay"),
     ("orbit", "orbits", "up", "up there", "in orbit", "in the sky", "going round")),
    "The Moon is falling towards the Earth all the time and moving sideways fast enough - about "
    "1 km a second - that it keeps missing, and that curved fall is the orbit. Gravity is the "
    "pull; with no sideways speed it would drop straight in. It has kept its own motion for 4.5 "
    "billion years because there is almost nothing out there to slow it down.",
    bias=2))

ENTRIES.append(entry(
    "moon-what",
    (("moon",),
     ("what", "mean", "meaning", "definition", "explain", "satellite", "earth")),
    "The Moon is the Earth's only natural satellite, about 384,000 km away, and gravity holds it "
    "in orbit. It makes no light of its own - we see sunlight reflected from its surface - and its "
    "pull is the main cause of our tides. It takes about 27 days to go round the Earth and the same "
    "time to turn once, so we always see the same side.",
    avoid=("honeymoon", "moonlight", "moonlighting", "boot", "landing", "apollo", "nasa",
           "astronaut", "flag", "made of", "made from", "inside", "core", "surface",
           "full", "new", "blue", "blood", "super", "harvest", "crescent", "phase",
           "phases", "bright", "orange", "white", "craters", "follows", "size", "big",
           "bigger", "horizon", "eclipse", "jupiter", "saturn", "mars", "venus", "neptune",
           "uranus", "titan", "io", "europa"),
    ask=DEFINITION_ASK,
    bias=2))
PLANET_SIZES = (
    (("mercury",), "Mercury is about 4,879 km across, a little over a third of the Earth's width "
                   "and smaller than Jupiter's moon Ganymede."),
    (("venus",), "Venus is about 12,104 km across, almost exactly the Earth's width - about 95% "
                 "of it - and a little hotter than a pizza oven all over its surface."),
    (("mars",), "Mars is about 6,779 km across, a bit over half the Earth's width, so nearly two "
                "Marses would fit across the Earth's face."),
    (("jupiter",), "Jupiter is about 143,000 km across, eleven Earths side by side, and about "
                   "1,300 Earths would fit inside it: it is the biggest planet by a wide margin."),
    (("saturn",), "Saturn is about 116,460 km across, nine Earths side by side, and about 760 "
                  "Earths would fit inside it. Its rings are far wider than the planet and, in "
                  "places, only tens of metres thick."),
    (("uranus",), "Uranus is about 50,724 km across, four Earths side by side, and about 63 "
                  "Earths would fit inside it."),
    (("neptune",), "Neptune is about 49,244 km across, nearly four Earths side by side, and "
                   "about 58 Earths would fit inside it - a little smaller than Uranus but "
                   "heavier."),
    (("pluto",), "Pluto is about 2,377 km across: about a fifth of the Earth's width, and smaller "
                 "than our Moon."),
)

_SIZE_ASK = ("how big", "how large", "how wide", "what size", "size", "diameter", "across",
             "bigger", "smaller", "compared", "how many earths", "how much bigger",
             "how much smaller")


def _the_planet_size(memory, understood):
    said = " ".join(str(part).lower() for part in ((understood or {}).get("clean"),
                                                  (understood or {}).get("text")) if part)

    def at(name):
        found = re.search(r"(?<![a-z])" + name + r"(?![a-z])", said)
        return found.start() if found else None

    found = [(at(name), answer) for names, answer in PLANET_SIZES for name in names
             if at(name) is not None]
    if not found:
        return None
    first, answer = min(found)
    for other in ("sun", "moon", "earth"):
        found_other = re.search(r"(?<![a-z])" + other + r"(?![a-z])", said)
        if found_other is not None and found_other.start() < first:
            return None
    return answer


ENTRIES.append(entry(
    "planet-size",
    (("mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto"),
     _SIZE_ASK),
    _the_planet_size,
    ask=_SIZE_ASK,
    avoid=("see", "visible", "tonight", "telescope", "horoscope", "star sign", "zodiac",
           "astrology", "chart", "retrograde", "mission", "nasa", "rover", "rocket",
           "travel", "trip", "holiday", "hotel", "live on", "life on", "temperature",
           "hot", "cold", "weather", "moons", "orbit", "distance", "how far", "weight",
           "weigh", "gravity", "ring", "rings", "how many planets", "planet names"),
    bias=2))


BUILDING_STANDS = (
    "A tall building stays up because its weight runs straight down a braced frame into deep "
    "foundations, so wind bends it a little instead of tipping it, and the tallest carry a heavy "
    "damper near the top to soak up the sway. Pisa leans without falling because its weight still "
    "sits over its base: it sank slowly into soft ground, and soil taken out from the high side is "
    "what steadied it.")

CRANE_STANDS = (
    "A tower crane stays up because its mast is bolted to a concrete base and tied into the "
    "building as that rises, and a counterweight on the short arm balances the load on the long "
    "one. It is built to lift a set weight at a set reach and no more, so it trips out before it "
    "can tip.")

BRIDGE_STANDS = (
    "A bridge gets its load to the ground in one of three ways: a beam rests the span on a support "
    "at each end, an arch pushes the weight outwards into solid abutments, and a suspension or "
    "cable-stayed bridge hangs the deck from cables over towers anchored into the ground. Whichever "
    "it is, the span is never left to carry itself.")

CHIMNEY_STANDS = (
    "A chimney stays up because each stack of bricks is bonded into the wall it stands on and "
    "strapped to the roof, and every joint is staggered so the bricks cannot slide on each other - "
    "a straight stack of bricks with a flue down the middle is strong only while the mortar and the "
    "flaunching at the top are sound. That is why a chimney comes down in a storm, and why it comes "
    "down as one piece: the mortar in the joints has gone soft, or smoke and rain have washed it out "
    "from under the flaunching, so the whole stack rocks on its base.")

TREE_STANDS = (
    "A tree stays up because its roots spread about as wide as its branches and the trunk tapers as "
    "it rises, so most of the weight is low down and the crown is light. Wind is what tests it: a "
    "tree that bends sheds the force, and the one that comes down is the one whose roots were cut "
    "on one side or left standing in waterlogged soil.")

PLANT_STANDS = (
    "A houseplant flops over for one of three reasons: it has grown tall and thin reaching for "
    "light, the pot has become top-heavy for its roots, or the roots have rotted in soggy compost "
    "and let go. Move it somewhere brighter, put a cane or a hoop in and tie the stems loosely, and "
    "check the drainage holes before you water again - a pot standing in a full saucer is the usual "
    "cause.")

GARDEN_PLANT_STANDS = (
    "A plant in the ground or a grow bag goes over for one of four reasons, and the fix is the one "
    "that matches: it grew tall and soft reaching for light, so stake it loosely with a cane and a "
    "soft tie in a figure of eight and give it more sun; it was sown too thickly and the stems are "
    "thin, so thin them next time; the roots have been eaten or rotted, so lift the sick one and "
    "look; or wind and rain bent it, so a windbreak or a row of sturdier plants on that side is "
    "what stops it next year. Seedlings that flop at soil level are damping off from cold wet "
    "compost rather than anything above it.")

GARDEN_PLANTS = re.compile(
    r"\b(?:tomato(?:es)?|sunflowers?|tulips?|daffodils?|roses?|seedlings?|sweetcorn|corn|"
    r"beans?|peas?|courgettes?|pumpkins?|squash|dahlias?|climbers?|clematis|wisteria|"
    r"shrub|shrubs|hedge|hedges|garden|gardens|outdoor|outdoors|outside|allotment|"
    r"grow bag|bed|beds|plot)\b")

STANDING_WORDS = ("fall over", "falls over", "falling over", "fallen over", "fell over",
                  "fall down", "falls down", "fell down", "falling down",
                  "fall", "falls", "collapse", "collapses", "collapsed", "topple", "topples",
                  "flop over", "flops over", "flopped over", "keel over", "keels over",
                  "keeled over", "keeling over", "stay up", "stays up",
                  "stay standing", "stays standing", "still standing", "stay upright",
                  "not fall", "dont fall", "doesnt fall", "does not fall",
                  "not collapse", "sway", "sways", "wobble", "wobbles", "blown over",
                  "blow over", "blows over", "not tip", "tip over", "stand up", "stands up",
                  "standing up", "survive", "survives", "withstand", "withstands",
                  "hold up", "holds up", "earthquake", "earthquakes", "quake", "quakes",
                  "hurricane", "high winds",
                  "top heavy", "top-heavy", "tips over", "tipping over", "keeps falling",
                  "lopsided")


def _tall_thing(memory, understood):
    said = " ".join(str(part).lower() for part in ((understood or {}).get("clean"),
                                                   (understood or {}).get("text")) if part)
    if re.search(r"\bcranes?\b", said):
        return CRANE_STANDS
    if re.search(r"\bbridges?\b", said):
        return BRIDGE_STANDS
    if re.search(r"\bchimneys?\b", said):
        return CHIMNEY_STANDS
    if re.search(r"\btrees?\b|\bforest\b|\bwoods\b", said):
        return TREE_STANDS
    if GARDEN_PLANTS.search(said):
        return GARDEN_PLANT_STANDS
    if re.search(r"\bplants?\b|\bhouseplants?\b|\bflowers?\b|\bhanging basket\b",
                 said):
        return PLANT_STANDS
    return BUILDING_STANDS


ENTRIES.append(entry(
    "tall-things-stand-up",
    (("building", "buildings", "skyscraper", "skyscrapers", "high rise", "high-rise",
      "tower", "towers", "tower block", "tower blocks", "block of flats", "blocks of flats",
      "crane", "cranes", "bridge", "bridges", "chimney", "chimneys", "pylon", "pylons",
      "tree", "trees", "forest", "woods", "plant", "plants", "houseplant", "houseplants",
      "seedling", "seedlings", "tomato", "tomatoes", "flowers", "hanging basket",
      "tulip", "tulips", "daffodil", "daffodils", "sunflower", "sunflowers", "rose", "roses",
      "shrub", "shrubs", "climber", "climbers", "sweetcorn", "dahlia", "dahlias"),
     STANDING_WORDS),
    _tall_thing,
    ask=("why", "how", "what", "does", "do", "dont", "doesnt", "can", "is", "are", "will",
         "has", "have", "keeps", "keep", "fell", "fallen", "flopped", "flop"),
    avoid=("shares", "stocks", "prices", "share price", "the market", "markets", "hair",
           "leaves", "leaf", "rain", "snow", "asleep", "twin towers", "9/11", "nine eleven",
           "world trade", "rent", "price", "value", "house prices",
           "nan", "nana", "grandad", "grandma", "granny", "gran", "mum", "mom", "dad",
           "elderly", "pensioner", "old people", "old lady", "old man", "i fell", "tripped",
           "stairs", "ladder", "roof",
           "frost", "frosts", "frosty", "freezing", "cold", "winter", "winters", "ice"),
    bias=1))


STRUCTURE_ANSWERS = (
    (("longest bridge", "longest bridges", "longest bridge in the world"),
     "The longest bridge in the world is the Danyang-Kunshan Grand Bridge on the Beijing-Shanghai "
     "high-speed railway, about 165 km, most of it on piers over land and water. The longest over "
     "open sea is the Jiaozhou Bay Bridge at about 42 km, and the longest in Europe is the Crimean "
     "Bridge at about 19 km. A long bridge is nearly always a run of short spans on piers rather "
     "than one big span."),
    (("suspension bridge", "suspension bridges"),
     "A suspension bridge hangs its deck from two main cables slung over the towers and anchored "
     "into the ground at each end, with vertical hangers dropping to the deck. The cables pull, "
     "the towers carry that pull down, and the anchors take it at the ends, which is why it can "
     "span 1 to 2 km - the Humber Bridge, the Golden Gate, the Akashi Kaikyo."),
    (("cable stayed", "cable-stayed", "cable stayed bridge"),
     "A cable-stayed bridge runs cables straight from the tower to the deck, a fan or a harp of "
     "them, instead of one main cable with hangers. It needs no big anchorage at the ends, so it "
     "suits spans of a few hundred metres - the Queen Elizabeth II Bridge at Dartford and the "
     "Millau Viaduct are cable-stayed."),
    (("box girder", "box girders", "box girder bridge"),
     "A box girder is a beam made as a hollow box of steel or concrete, wide at the top to carry "
     "the road and deep enough to be stiff: a hollow box is far stiffer than a solid bar of the "
     "same weight, because the material sits out at the edges. Most long concrete bridges and "
     "cable-stayed decks are a box girder, and the box is also where the cables and the air for "
     "the inside run."),
    (("pier", "piers"),
     "A pier is one of the upright supports a bridge span rests on, and it is what the weight of "
     "the span comes down through to the ground. In a river they are built inside a cofferdam or "
     "a caisson, and the spans sit on bearings on top of them so the deck can expand and "
     "contract without cracking."),
    (("beam bridge", "beam bridges", "girder bridge", "girder bridges"),
     "A beam bridge is the simplest kind there is: a slab or a girder laid across two supports. "
     "The deck bends under the load, so the top is squeezed and the bottom is stretched, and the "
     "deeper the girder the further it reaches. Cheap, quick, and right for a short span."),
    (("arch bridge", "arch bridges", "how does an arch work", "how do arches work",
      "why do arches work"),
     "An arch bridge carries its load in compression: the weight comes down through the arch and "
     "pushes outwards at the bottom, so the ground or the abutments at each end have to resist "
     "that push. That is why stone and brick are so good in an arch - they take squeezing and not "
     "stretching - and why the Iron Bridge at Coalbrookdale, the first big cast-iron arch, was "
     "built in 1779 in the same shape."),
    (("viaduct", "viaducts", "aqueduct", "aqueducts"),
     "A viaduct carries a road or a railway across a valley on a run of arches or piers rather "
     "than one span, which is what you need when the gap is long and the ground below is uneven - "
     "the Ribblehead Viaduct has 24 arches. An aqueduct is the same structure carrying water: the "
     "Romans built them on stone arches, and a canal aqueduct does the same job for boats."),
    (("cantilever", "cantilevers", "cantilever bridge", "cantilever bridges"),
     "A cantilever is a beam held at one end with the other end free: a balcony, a diving board, a "
     "crane jib. Two cantilevers reaching out from opposite banks make a cantilever bridge, and it "
     "can be built outwards from each side without scaffolding in the water - the Forth Bridge is "
     "the famous one."),
    (("expansion joint", "expansion joints"),
     "Bridges have expansion joints because steel and concrete change length as they warm and "
     "cool, and a long deck moves by several centimetres between winter and summer. The joint is "
     "the strip that lets it happen without cracking the deck or shoving the abutments - the "
     "toothed metal you hear clicking under the wheels - and it is also what lets the bridge move "
     "in an earthquake."),
    (("tunnel", "tunnels"),
     "A tunnel under water is usually not bored through the seabed: most are immersed tubes - a "
     "trench is dredged, boxed sections are floated out, sunk into it and joined, then covered "
     "over, which is how the Oresund link and the Fehmarn tunnel were built. Boring is used where "
     "the ground is good, as in the chalk under the Channel: a shielded machine cuts the face and "
     "the lining goes up behind it as it goes."),
)


def _a_tunnel_named(said):
    if " tunnel" not in said and " tunnels" not in said:
        return None
    if "channel tunnel" in said or (" channel " in said and ("how long" in said or "long" in said)):
        return ("The Channel Tunnel is 50.5 km from end to end, with about 38 km of it under the "
                "sea, and a train takes about 35 minutes from Folkestone to Calais. Three tubes "
                "run side by side: two for trains and a smaller service tunnel between them, "
                "bored through chalk that is soft enough to cut and stiff enough to stand while "
                "you do it.")
    if "longest" in said or "how long" in said:
        return ("The longest railway tunnel in the world is the Gotthard Base Tunnel in "
                "Switzerland at 57 km, opened in 2016; the longest road tunnel is the Laerdal "
                "Tunnel in Norway at 24.5 km. The longest undersea one is still the Channel "
                "Tunnel at 38 km under the water.")
    return None


PLACES_WITH_A_TALLEST = ("the world", "world", "london", "uk", "the uk", "britain", "great britain",
                         "the united kingdom", "united kingdom", "england", "scotland", "wales",
                         "british")


PLACES_WITH_A_LONGEST = ("the world", "world", "europe", "uk", "the uk", "britain",
                         "great britain", "the united kingdom", "united kingdom", "england",
                         "scotland", "wales", "british")


def _the_place_asked(said, known=PLACES_WITH_A_TALLEST):
    parts = said.split(" in ")
    if len(parts) < 2:
        return None
    words = parts[-1].split()
    for count in (3, 2, 1):
        guess = " ".join(words[:count])
        if guess in known:
            return guess
    return words[0] if words else None


def _the_longest_bridge(said):
    if " bridge" not in said and " bridges" not in said:
        return None
    if "longest" not in said and "biggest" not in said and "largest" not in said:
        return None
    place = _the_place_asked(said, PLACES_WITH_A_LONGEST)
    if place and place not in PLACES_WITH_A_LONGEST:
        return None
    if " europe " in said and " world " not in said:
        return ("The longest bridge in Europe is the Crimean Bridge at about 19 km, if you count "
                "the crossing built in 2018; inside the European Union the longest is the Vasco "
                "da Gama Bridge in Lisbon at about 17 km, opened in 1998. The Oresund link between "
                "Denmark and Sweden is about 8 km of bridge and 4 km of tunnel.")
    if any((" " + word + " ") in said for word in ("uk", "britain", "england", "scotland",
                                                   "wales", "british")):
        return ("The longest bridge in Britain is the Prince of Wales Bridge over the Severn, "
                "about 5 km, which carries the M4; the Queen Elizabeth II Bridge at Dartford is "
                "about 2.9 km and the Humber Bridge 2.2 km, though the Humber has the longest "
                "single span in Britain.")
    return None


def _a_kind_of_bridge(memory, understood):
    said = _the_line(understood) if "_the_line" in globals() else ""
    if not said:
        said = " " + str((understood or {}).get("clean") or (understood or {}).get("text")
                         or "").lower() + " "
    named = _the_longest_bridge(said) or _a_tunnel_named(said)
    if named:
        return named
    if "longest" in said or "biggest" in said or "largest" in said:
        place = _the_place_asked(said, PLACES_WITH_A_LONGEST)
        if place and place not in PLACES_WITH_A_LONGEST:
            return None
    if any(word in said for word in (" build ", " built ", " builds ", " building ",
                                     " construct ", " constructed ")) and any(
            (" " + word + " ") in said for word in ("bridge", "bridges", "viaduct", "flyover")) and any(
            (" " + word + " ") in said for word in ("motorway", "motorways", "road", "roads",
                                                    "railway", "railways", "rail")):
        return ("A bridge over a motorway is built a piece at a time so the road can stay open: "
                "the beams or the whole deck are put together beside it and lifted or slid into "
                "place in overnight closures, or the deck is pushed out from one side with a "
                "launching girder. The piers go in first, the beams land on them, and the road "
                "below is only shut for the hours it takes to place each piece.")
    if any(word in said for word in (" how long does it take ", " how long to ", " cost of ",
                                     " how much does ")):
        return None
    if any(word in said for word in (" what does ", " what do ", " meaning ", " in english ")) and not any(
            (" " + word + " ") in said for word in ("bridge", "bridges", "tunnel", "tunnels",
                                                    "viaduct", "aqueduct", "span", "spans")):
        return None
    for names, answer in STRUCTURE_ANSWERS:
        if any((" " + name + " ") in said for name in names):
            return answer
    return ("A bridge carries a load across a gap, and it does it in one of four ways: a beam "
            "resting on a support at each end, an arch pushing the weight outwards into solid "
            "ground, a truss or box girder making a beam stiffer, or cables hanging the deck from "
            "towers - suspension or cable-stayed. Stone and brick work in an arch, steel works in "
            "all four.")


TALL_BUILDINGS = (
    (("shard",),
     "The Shard in London is 310 m to the tip of its spire, 95 storeys, finished in 2012 - the "
     "tallest building in the United Kingdom and, for four years, in western Europe. Its floor "
     "plate is glass on all sides and the tower leans in as it rises, so the top storeys are "
     "smaller than the bottom ones."),
    (("burj khalifa", "burj"),
     "The Burj Khalifa in Dubai is 828 m, 163 floors, finished in 2010, and it is the tallest "
     "building in the world. It is concrete from top to bottom rather than steel, and it steps in "
     "as it rises to break up the wind, which is what allows the height."),
)

def _the_tallest_building(memory, understood):
    said = " " + str((understood or {}).get("clean") or (understood or {}).get("text") or ""
                     ).lower() + " "
    for names, answer in TALL_BUILDINGS:
        if any((" " + name + " ") in said for name in names):
            return answer
    place = _the_place_asked(said)
    if place and place not in PLACES_WITH_A_TALLEST:
        return None
    if ((" skyscraper " in said or " skyscrapers " in said)
            and not any((" " + word + " ") in said for word in
                        ("tallest", "highest", "biggest", "world", "london", "uk", "britain"))):
        return ("A skyscraper is a very tall building, and the usual line is 100 m for one and "
                "150 m for a supertall. Two things made them possible: a steel frame that carries "
                "the weight instead of the walls, and the safety lift, so the building could go up "
                "rather than out. The first was the Home Insurance Building in Chicago in 1885, "
                "ten storeys; the Burj Khalifa is 163.")
    if " london " in said and " world " not in said:
        return ("The tallest building in London is The Shard at 310 m, finished in 2012, with 95 "
                "storeys; One Canada Square at Canary Wharf, 235 m, was the tallest before it. "
                "The tallest in the United Kingdom is still The Shard.")
    if any((" " + word + " ") in said for word in ("uk", "britain", "england", "scotland",
                                                   "wales", "british")):
        return ("The tallest building in the United Kingdom is The Shard in London at 310 m, "
                "finished in 2012. The tallest in Scotland is the Aughton Street tower in "
                "Glasgow, and in Wales it is the Sky Plaza in Cardiff.")
    return ("The tallest building in the world is the Burj Khalifa in Dubai at 828 m, 163 floors, "
            "finished in 2010; Merdeka 118 in Kuala Lumpur at 679 m is second, and the Shanghai "
            "Tower at 632 m third. The Burj was built that tall because the client wanted it to "
            "be, and the limits above 500 m are the lifts - a single lift run gets too long - and "
            "the wind, which is why the tower steps in as it rises.")


ENTRIES.append(entry(
    "the-tallest-building",
    (("tallest building", "tallest buildings", "tallest tower", "tallest skyscraper",
      "highest building", "biggest building", "burj khalifa", "burj", "shard", "skyscraper",
      "skyscrapers"),
     ("what", "whats", "what's", "which", "where", "how tall", "tall", "highest", "tallest",
      "in the world", "world", "uk", "britain", "london", "explain", "tell me")),
    _the_tallest_building,
    avoid=("hold up", "holds up", "stay up", "stays up", "stand up", "stands up", "fall down",
           "collapse", "sway", "wobble", "topple", "leaning", "my flat", "my office", "rent",
           "my building", "upstairs", "neighbour", "neighbours", "lease", "cladding",
           "fire", "fires", "insurance", "mortgage", "buy", "move", "moving"),
    bias=1))

ENTRIES.append(entry(
    "a-kind-of-bridge",
    (("bridge", "bridges", "suspension bridge", "beam bridge", "arch bridge", "girder",
      "cantilever", "viaduct", "viaducts", "aqueduct", "tunnel", "tunnels", "expansion joint",
      "expansion joints", "arch", "arches"),
     ("what", "whats", "what's", "how", "why", "explain", "mean", "means", "built", "build",
      "building", "work", "works", "working", "used for", "made", "made of", "difference",
      "definition", "define", "longest", "highest", "biggest")),
    _a_kind_of_bridge,
    avoid=("hold up", "holds up", "hold it up", "stay up", "stays up", "standing up",
           "stand up", "fall down", "falls down", "fell down", "falling down", "collapsed",
           "collapse", "sway", "wobble", "topple", "lean", "leaning",
           "foot", "feet", "fallen arches", "arch support", "arch supports", "insole",
           "insoles", "plantar", "heel", "nose", "tooth", "teeth", "dental", "dentist",
           "dentures", "dentistry", "bridgework", "implants", "crown", "crowns",
           "card game", "cards", "bridge the gap", "bridge a gap", "loan",
           "the gap",
           "network", "networking", "ethernet", "router", "routers", "wifi", "wi-fi", "modem",
           "switch", "lan", "vlan", "docker", "hypervisor", "virtual machine",
           "roman", "romans", "roman britain", "the romans", "boudicca", "hadrians wall",
           "hastings", "castle", "castles", "monastery", "cathedral", "cathedrals",
           "car", "rear suspension", "front suspension", "suspension arm", "suspension arms",
           "suspension bush", "suspension bushes", "shock", "shocks", "spring", "springs",
           "mot", "wheel",
           "carpal", "wrist", "tunnel vision", "polytunnel", "wind tunnel", "garden",
           "allotment", "greenhouse", "sewing", "fabric", "music", "song", "guitar", "piano"),
    bias=1))


_DEFINE = ("what is", "what are", "whats", "what's", "define", "definition", "meaning", "mean",
           "means", "explain", "explanation", "difference between", "difference", "vs",
           "measured in", "measure", "measured", "how is it", "simple terms", "for kids",
           "gcse", "physics", "chemistry", "biology", "science")

_DEFINITION_FILLER = frozenset((
    "what", "whats", "is", "are", "the", "a", "an", "of", "in", "and", "or", "it", "its", "mean",
    "means", "meaning", "define", "definition", "explain", "explanation", "simple", "terms",
    "for", "kids", "gcse", "physics", "chemistry", "biology", "science", "difference", "between",
    "vs", "versus", "measured", "measure", "how", "do", "you", "that", "this", "please", "sir",
    "miss", "again", "when", "would", "be", "use", "used", "example", "examples", "give", "me",
    "one", "some", "tell", "about", "which", "so", "then", "kind", "sort", "class", "school"))


def _the_line(understood):
    said = ""
    if isinstance(understood, dict):
        said = str(understood.get("clean") or understood.get("text") or "")
    return " " + said.lower() + " "


def _names(said, words):
    best, at = "", None
    for word in words:
        found = said.find(" " + word + " ")
        if found == -1:
            found = said.find(word)
            if found == -1:
                continue
        if at is None or found < at:
            best, at = word, found
    return best

MASS_OR_WEIGHT_WORDS = ("mass", "weight", "weigh", "weighs", "weighed", "weighing", "newton",
                        "newtons", "gravity")
MASS_OR_WEIGHT_UNITS = ("kg", "kgs", "kilo", "kilos", "kilogram", "kilograms", "kilogramme",
                        "kilogrammes", "lb", "lbs", "pounds", "pound", "stone", "stones")


def asks_about_mass_or_weight(understood):
    said = ""
    if isinstance(understood, dict):
        said = str(understood.get("text") or understood.get("clean") or "")
    said = " " + said.lower() + " "
    if isinstance(understood, dict) and isinstance(understood.get("leans_on"), dict):
        borrowed = {str(word).lower() for word in
                    (understood["leans_on"].get("words") or []) if isinstance(word, str)}
        words = re.findall(r"[a-z0-9']+", said)
        while words and words[-1] in borrowed:
            words.pop()
        said = " " + " ".join(words) + " "
    if _names(said, MASS_OR_WEIGHT_WORDS):
        return True
    return bool(_names(said, MASS_OR_WEIGHT_UNITS) and _names(said, _DEFINE))


def _mass_and_weight(memory, understood):
    said = _the_line(understood)
    if _names(said, ("weight", "weigh")) == "weight" and not _names(said, ("mass",)):
        return ("Weight is the pull of gravity on a mass, measured in newtons: a 60 kg person "
                "weighs about 600 N on Earth, about 100 N on the Moon and nothing at all in "
                "orbit. Mass is how much stuff is in something, measured in kilograms, and it is "
                "60 kg in all three places. The scales in your bathroom measure weight and are "
                "marked in kilograms for the mass that goes with it here.")
    return ("Mass is how much stuff is in something, measured in kilograms, and it does not change "
            "wherever you go. Weight is the pull of gravity on that mass, measured in newtons: a "
            "60 kg person weighs about 600 N on Earth, about 100 N on the Moon and nothing at all "
            "in orbit, while their mass is 60 kg in all three places. So the scales in your "
            "bathroom measure weight and are marked in kilograms for the mass that goes with it "
            "here.")


ENTRIES.append(entry(
    "mass-and-weight",
    (("mass", "weight", "mass and weight", "mass vs weight", "kg", "newtons"),
     _DEFINE + ("in space", "on the moon", "on the moon", "gravity", "moon", "kilogram",
                "kilogramme", "pounds", "lb", "same")),
    _mass_and_weight,
    guard=asks_about_mass_or_weight,
    avoid=("church", "catholic", "in church", "the mass", "bmi", "lose weight", "losing weight",
           "lose", "losing", "diet", "gain weight", "put on weight", "slimming", "scale",
           "scales", "how much should i weigh", "healthy weight", "protein", "deadlift",
           "what time", "sunday", "saturday", "say mass", "dead weight", "mass in",
           "newton metre", "newton metres", "newton-metre", "newton meter", "newton meters",
           "nm", "torque", "wrench", "priest", "communion", "midnight mass", "christmas",
           "easter"),
    bias=1))
def _kinetic_and_potential(memory, understood):
    said = _the_line(understood)
    named = _names(said, ("potential", "kinetic"))
    if named == "potential":
        return ("Potential energy is energy stored ready to be used: a ball held up high has "
                "potential energy, and it turns into kinetic energy as it falls, faster and "
                "faster. Kinetic energy is the energy something has because it is moving. Both "
                "are measured in joules. Potential is mass times gravity times height, so twice "
                "the height is twice the energy; kinetic is half the mass times the speed "
                "squared, so doubling the speed gives four times the energy.")
    return ("Kinetic energy is the energy something has because it is moving, and potential "
            "energy is energy stored ready to move: a ball held up high has potential energy, "
            "and it turns into kinetic energy as it falls, faster and faster. Both are measured "
            "in joules. Kinetic is half the mass times the speed squared, so doubling the speed "
            "gives four times the energy; potential is mass times gravity times height, so twice "
            "the height is twice the energy.")


ENTRIES.append(entry(
    "kinetic-and-potential-energy",
    (("kinetic energy", "potential energy", "kinetic and potential", "kinetic", "potential",
      "stored energy", "energy of motion"),
     _DEFINE + ("store", "stored", "difference between", "convert", "converted", "transfer",
                "example", "examples", "joules", "falling", "swing", "roller coaster")),
    _kinetic_and_potential,
    avoid=("boiler", "thermostat", "battery", "solar", "tariff", "bill", "meter", "kettle"),
    bias=1))
ENTRIES.append(entry(
    "electrical-resistance",
    (("resistance", "ohms", "ohm", "ohm's law", "ohms law"),
     _DEFINE + ("circuit", "circuits", "current", "voltage", "wire", "conductor", "measure",
                "measured in", "increase", "decrease", "lower", "reduce", "series", "parallel",
                "lamp", "bulb", "resistor")),
    "Resistance is how much a material fights the current, measured in ohms: a thin, long, hot "
    "wire has more of it than a short thick cold one, which is why a laptop charger stays cool "
    "and a toaster element glows. Ohm's law ties the three together, voltage equals current "
    "times resistance, so at 12 V a 4 ohm resistor carries 3 A. It turns the energy into heat, "
    "which is the point of a heater and the reason a long cable warms up.",
    avoid=("band", "bands", "training", "gym", "workout", "weights", "exercise", "antibiotic",
           "antibiotics", "insulin", "airway", "drug", "drugs"),
    bias=1))
ENTRIES.append(entry(
    "respiration",
    (("respiration", "aerobic respiration", "anaerobic respiration", "breathing and respiration",
      "cellular respiration"),
     _DEFINE + ("difference between", "equation", "word equation", "aerobic", "anaerobic",
                "muscle", "muscles", "lactic", "energy", "glucose", "oxygen", "plants", "cell",
                "cells")),
    "Respiration is how cells release energy from glucose: glucose plus oxygen gives carbon "
    "dioxide plus water plus energy, and every cell does it all the time. Breathing is only the "
    "moving of air in and out - the oxygen it brings is used in respiration and the carbon "
    "dioxide it carries away was made there. Sprinting, or holding your breath under water, "
    "outruns the oxygen, so muscles switch to anaerobic respiration, which makes energy fast and "
    "leaves lactic acid: that is the burn.",
    avoid=("cough", "colds", "chest", "lung", "lungs", "asthma", "doctor", "gp", "nhs",
           "my breathing", "breathless", "wheeze", "wheezing", "sleep", "snoring", "apnoea",
           "rate", "per minute", "breaths a minute", "breaths per minute", "my baby",
           "baby", "normal"),
    bias=1))
def _mitosis_meiosis(memory, understood):
    said = _the_line(understood)
    named = _names(said, ("meiosis", "cell cycle", "mitosis"))
    if named == "meiosis":
        return ("Meiosis makes four cells with half the chromosomes each, and that is how eggs "
                "and sperm are made, so that when two of them join the new cell has a full set "
                "again. Mitosis makes two identical cells, each with the same chromosomes as the "
                "parent, and that is how you grow and how a cut heals. Meiosis has two divisions "
                "in a row, mitosis one; the mnemonic that works is mitosis for maintenance, "
                "meiosis for making babies.")
    if named == "cell cycle":
        return ("The cell cycle is the whole life of a cell from one division to the next: a "
                "growth stage where the cell gets bigger and copies its DNA, then the division "
                "itself, which is mitosis if it makes two identical cells. Cells that stop "
                "dividing leave the cycle and sit in a resting state instead. Meiosis is the "
                "different division that makes eggs and sperm, with half the chromosomes each.")
    return ("Mitosis makes two identical cells, each with the same chromosomes as the parent, and "
            "that is how you grow and how a cut heals. Meiosis makes four cells with half the "
            "chromosomes, and that is how eggs and sperm are made, so that when two of them join "
            "the new cell has a full set again. The mnemonic that works: mitosis for maintenance, "
            "meiosis for making babies. Mitosis has one division, meiosis has two in a row.")


ENTRIES.append(entry(
    "mitosis-and-meiosis",
    (("mitosis", "meiosis", "cell division", "mitosis and meiosis", "cell cycle"),
     _DEFINE + ("difference between", "stages", "phases", "how", "why", "purpose", "gcse",
                "growth", "repair", "gametes", "sex cells", "chromosomes", "diploid", "haploid")),
    _mitosis_meiosis,
    bias=1))
def _frequency_wavelength_amplitude(memory, understood):
    said = _the_line(understood)
    named = _names(said, ("wavelength", "amplitude", "frequency"))
    if named == "wavelength":
        return ("Wavelength is the length of one whole wave, from one peak to the next, measured "
                "in metres. Frequency is how many of those waves pass a point each second, in "
                "hertz, and the two are locked together by the speed of the wave: wavelength is "
                "the speed divided by the frequency, so a 340 m/s sound at 50 Hz has a wavelength "
                "of 6.8 m. That is why a low note travels further round a corner than a high one.")
    if named == "amplitude":
        return ("Amplitude is how big the wave is - how far it swings from the middle - and it is "
                "what you hear as volume or see as brightness: a bigger amplitude is a louder "
                "sound or a brighter light. Frequency is the different thing, how many waves pass "
                "each second, measured in hertz, and that is the pitch. So a loud low note is big "
                "amplitude and small frequency, and turning the volume up changes the amplitude "
                "only.")
    return ("Frequency is how many times something happens in a second, measured in hertz: 50 Hz "
            "is fifty times a second. A sound's frequency is its pitch - 440 Hz is the A above "
            "middle C, and the higher the number the higher the note - while a radio station's "
            "100 MHz is a hundred million waves a second. It is the reciprocal of the period, so "
            "a wave that repeats every 0.02 seconds has a frequency of 50 Hz, and the wavelength "
            "is the speed divided by the frequency.")


ENTRIES.append(entry(
    "frequency",
    (("frequency", "hertz", "wavelength", "amplitude", "wave frequency",
      "amplitude of a wave", "amplitude of the wave", "wavelength of a wave",
      "wavelength of the wave", "frequency of a wave", "wave amplitude", "wave length",
      "peak to peak", "trough to trough"),
     _DEFINE + ("physics", "sound", "sound wave", "wave", "waves", "light", "radio", "signal",
                "measured in", "measure", "hz", "pitch", "loudness", "period", "unit")),
    _frequency_wavelength_amplitude,
    avoid=("wifi", "wi-fi", "broadband", "train", "trains", "bus", "buses", "tram", "how often",
           "hoover", "washing", "shower", "cleaning", "water the", "cut the grass", "floss",
           "dehumidifier"),
    bias=2))
ENTRIES.append(entry(
    "rock-cycle",
    (("rock cycle", "igneous", "sedimentary", "metamorphic", "types of rock", "type of rock"),
     _DEFINE + ("cycle", "formed", "how are", "how is", "made", "form", "forms", "examples",
                "example", "gcse", "difference between", "which")),
    "The rock cycle is rocks being made, broken down and made again. Magma cools to igneous rock "
    "such as granite or basalt; wind and water wear any rock into grains that settle, get "
    "squashed and cement into sedimentary rock such as limestone and sandstone; heat and pressure "
    "bake or squeeze rock into metamorphic rock such as marble, from limestone, or slate, from "
    "shale. Bury it deeper and it melts back to magma: the three types are one loop, not three "
    "separate things.",
    avoid=("my rock", "rock music", "rock band", "rock salt", "on the rocks", "rock the",
           "punk", "gig", "concert"),
    bias=6))
_NEWTON_SECOND = (
    "The second law is the useful one: force equals mass times acceleration, F = ma, so the same "
    "push moves a light thing quickly and a heavy one slowly, and a 1,000 kg car pushed with "
    "2,000 N accelerates at 2 m/s each second.")
_NEWTON_FIRST = (
    "The first law says a thing keeps still, or keeps going in a straight line at the same speed, "
    "unless a force acts on it - which is why a passenger is thrown forward when a bus brakes, and "
    "why a seatbelt is the force that stops them.")
_NEWTON_THIRD = (
    "The third law says every force has an equal force back the other way: you push the ground and "
    "it pushes you forward, a rocket throws gas down and the gas throws the rocket up.")
_NEWTON_EACH = re.compile(
    r"\b(first|1st|second|2nd|third|3rd)\s+law\b"
    r"|\blaw\s+(?:number\s+)?(first|1st|second|2nd|third|3rd)\b"
    r"|\b(first|1st|second|2nd|third|3rd)\b")
_NEWTON_WORD = {"first": 0, "1st": 0, "second": 1, "2nd": 1, "third": 2, "3rd": 2}


def _newtons_laws(memory, understood):
    said = ""
    if isinstance(understood, dict):
        said = str(understood.get("text") or "")
    order = [_NEWTON_SECOND, _NEWTON_FIRST, _NEWTON_THIRD]
    match = _NEWTON_EACH.search(" " + said.lower() + " ")
    if match:
        word = match.group(1) or match.group(2) or match.group(3)
        which = _NEWTON_WORD.get(word)
        if which == 0:
            order = [_NEWTON_FIRST, _NEWTON_SECOND, _NEWTON_THIRD]
        elif which == 2:
            order = [_NEWTON_THIRD, _NEWTON_SECOND, _NEWTON_FIRST]
    return " ".join(order)
ENTRIES.append(entry(
    "newtons-laws",
    (("newton's second law", "newtons second law", "newton's first law", "newtons first law",
      "newton's third law", "newtons third law", "newton's laws", "newtons laws",
      "law of motion", "laws of motion", "second law of motion", "first law of motion",
      "third law of motion", "f=ma", "f = ma", "f ma", "force equals mass times acceleration",
      "force equals mass times acceleration", "mass times acceleration", "force mass"),
     _DEFINE + ("second", "first", "third", "law", "laws", "force", "motion", "acceleration",
                "mass", "action", "reaction", "inertia", "example", "explain", "use")),
    _newtons_laws,
    avoid=("who was", "biography", "born", "died", "apple", "newton metres", "newton metre",
           "nm", "torque", "wrench", "newton abbot"),
    bias=2))
ENTRIES.append(entry(
    "acceleration",
    (("acceleration", "accelerate", "accelerating", "deceleration", "decelerating"),
     _DEFINE + ("physics", "calculate", "calculated", "measured in", "unit", "units",
                "formula", "m/s", "per second", "gravity", "speed", "velocity", "motion",
                "equation", "constant")),
    "Acceleration is how quickly speed changes, measured in metres per second squared: 2 m/s "
    "squared means each second it goes 2 m/s faster. A car from 0 to 60 mph in 9 seconds is "
    "accelerating at about 3 m/s squared, and gravity pulls a falling thing at about 9.8. "
    "Slowing down is acceleration the other way, so a brake is not a different idea, just one "
    "that points backwards.",
    avoid=("car makes", "noise", "noisy", "clunk", "judder", "judder", "engine", "clutch",
           "gear", "gears", "pedal", "bike", "insurance", "company", "startup", "business",
           "growth"),
    bias=1))
ENTRIES.append(entry(
    "momentum",
    (("momentum", "conservation of momentum"),
     _DEFINE + ("physics", "calculate", "measured in", "formula", "mass", "velocity", "speed",
                "collision", "collisions", "conserved", "unit", "units", "moving")),
    "Momentum is mass times velocity, measured in kg m/s, and it is what makes a lorry harder to "
    "stop than a bike going at the same speed. Its rule is that the total is unchanged in a "
    "collision: two skaters pushing apart, or a cue ball hitting another, end up with the same "
    "total momentum they started with - one gains what the other loses. That is why a big "
    "airbag spreads the change over longer, so the force on you is smaller.",
    avoid=("diet", "exercise", "gym", "running", "training", "motivation", "motivated",
           "keeping going", "keep going", "study", "studying", "project", "habit", "losing",
           "lost my", "weight loss",
           "at work", "no momentum", "momentum going", "keep momentum", "build momentum",
           "back on track"),
    bias=1))
def _speed_and_velocity(memory, understood):
    said = _the_line(understood)
    if _names(said, ("velocity",)) == "velocity" and _names(said, ("speed",)) != "speed":
        return ("Velocity is how fast you are going and which way: 50 mph north is a velocity, "
                "and 50 mph on its own is a speed. So a car going round a roundabout at a steady "
                "30 mph has a constant speed and a changing velocity, because the direction keeps "
                "changing. Speed is distance over time, and average speed is the whole trip's "
                "distance over the whole time, which is why a two-hour journey with a stop does "
                "not average the speed you had on the motorway.")
    return ("Speed is how fast you are going, distance over time: 100 miles in two hours is "
            "50 mph. Velocity is that speed with a direction, so a car going round a roundabout "
            "at a steady 30 mph has a constant speed and a changing velocity. Average speed is "
            "the whole trip's distance over the whole time, which is why a two-hour journey with "
            "a stop does not average the speed you had on the motorway.")


ENTRIES.append(entry(
    "speed-and-velocity",
    (("speed", "velocity", "speed and velocity", "speed vs velocity", "average speed",
      "calculate average speed", "how do you work out average speed",
      "distance time graph", "distance-time graph"),
     _DEFINE + ("physics", "calculate", "calculated", "formula", "measured in", "unit", "units",
                "difference between", "average", "constant", "graph", "motion", "direction")),
    _speed_and_velocity,
    avoid=("broadband", "wifi", "wi-fi", "internet", "download", "upload", "connection",
           "cycling", "running", "my run", "pace", "mph", "speed camera", "speed limit",
           "caught speeding", "got a speeding", "fixed penalty", "fast",
           "serve", "tennis", "golf", "swing", "bowling", "my car", "my bike", "top speed",
           "0-60", "quarter mile", "terminal velocity",
           "speed of light", "speed of sound", "of light", "of sound", "of a wave",
           "miles an hour", "km/h", "kilometres an hour", "kilometers an hour",
           "speed of", "velocity of"),
    bias=3))


_SKY_ASK = ("what", "mean", "meaning", "definition", "explain", "why")
_RECORD_WORDS = ("biggest", "largest", "longest", "shortest", "highest", "lowest", "deepest",
                 "oldest", "how many", "how much", "how long", "what date", "which date",
                 "what time", "when is", "when does", "this year", "next year", "2025", "2026")

ENTRIES.append(entry(
    "solstice-what",
    (("solstice", "solstices", "summer solstice", "winter solstice", "midsummer"),
     _SKY_ASK),
    "A solstice is the day the sun is highest or lowest in the sky, which is why it is the "
    "longest day (about 21 June in the north) or the shortest (about 21 December): the Earth's "
    "tilt is leaning that half of the planet most towards or away from the sun.",
    avoid=_RECORD_WORDS + ("party", "festival", "celebrate", "bonfire", "sweden", "ritual",
                           "what happens at", "tradition"),
    ask=_SKY_ASK,
    bias=2))

ENTRIES.append(entry(
    "equinox-what",
    (("equinox", "equinoxes", "spring equinox", "autumn equinox", "vernal equinox",
      "autumnal equinox"), _SKY_ASK),
    "An equinox is the day the sun sits over the equator, so day and night are about twelve "
    "hours each everywhere: around 20 March and 22 September, which is when spring starts on one "
    "half of the planet and autumn on the other.",
    avoid=_RECORD_WORDS + ("celebrate", "ritual", "tradition", "pagan", "party", "festival"),
    ask=_SKY_ASK,
    bias=2))

ENTRIES.append(entry(
    "crystal-what",
    (("crystal", "crystals", "crystalline"), ("what", "mean", "meaning", "definition",
                                             "explain", "science", "structure")),
    "A crystal is a solid whose atoms sit in a regular repeating pattern, which is why it grows "
    "flat faces and sharp edges: salt, sugar, quartz and ice from the freezer are all crystals. "
    "The pattern decides the shape, so salt makes cubes and snowflakes make six-armed stars.",
    avoid=_RECORD_WORDS + ("ball", "meth", "healing", "heal", "chakra", "energy", "vibrations",
                           "shop", "pendant", "necklace", "decorative", "wine", "glasses",
                           "champagne", "clear", "grow", "growing", "make", "buy", "gift",
                           "battery", "watch", "screen", "lamp", "display"),
    ask=("what", "mean", "meaning", "definition", "explain"),
    bias=2))

ENTRIES.append(entry(
    "coral-what",
    (("coral", "corals", "coral reef", "coral reefs"), ("what", "mean", "meaning",
                                                       "definition", "explain")),
    "Coral is an animal, not a plant: a colony of tiny polyps that build a hard skeleton around "
    "themselves, and the reef is thousands of years of those skeletons stacked up. They get most "
    "of their food from algae living inside them, which is why they bleach white when the water "
    "gets too warm.",
    avoid=_RECORD_WORDS + ("necklace", "jewellery", "jewelry", "earring", "beads", "cut",
                           "bleaching", "bleached", "dying", "dead", "restore", "planting",
                           "pink", "red coral", "coral island", "coral sea"),
    ask=("what", "mean", "meaning", "definition", "explain"),
    bias=2))

ENTRIES.append(entry(
    "antibody-what",
    (("antibody", "antibodies"), ("what", "mean", "meaning", "definition", "explain")),
    "An antibody is a protein your immune system makes that sticks to one particular germ or "
    "chemical, marking it so the body can clear it, and it stays in the blood afterwards, which "
    "is why you usually do not get the same illness twice. That is also how a vaccine works: it "
    "shows you the shape first, so the antibodies are ready.",
    avoid=_RECORD_WORDS + ("test", "tests", "tested", "positive", "negative", "result",
                           "results", "level", "levels", "high", "low", "how long do they last",
                           "do i have", "should i get"),
    ask=("what", "mean", "meaning", "definition", "explain"),
    bias=2))


_MEASURED = ("what", "mean", "meaning", "definition", "explain",
             "how does", "how do", "how do they", "how do you", "how it works", "how they work",
             "how it happens", "how that works", "what makes", "what causes", "what creates")

ENTRIES.append(entry(
    "lever-what",
    (("lever", "levers"), _MEASURED + ("physics", "simple machine", "machines")),
    "A lever is a bar that turns on a pivot, and it lets a small push move a big weight if the "
    "pivot sits close to the weight: a crowbar, a wheelbarrow, a see-saw and a bottle opener are "
    "all levers.",
    avoid=_RECORD_WORDS + ("arch file", "file", "folder", "handle", "tap", "gate", "door",
                           "buy", "shop", "pull"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "pulley-what",
    (("pulley", "pulleys"), _MEASURED + ("physics", "simple machine", "machines")),
    "A pulley is a wheel with a rope running over it: one changes the direction of a pull, so you "
    "pull down to lift a load up, and two together halve the force you need by doubling the rope. "
    "That is why a flagpole and a crane both use one.",
    avoid=_RECORD_WORDS + ("gym", "cable machine", "lat", "workout", "buy", "shop"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "gear-what",
    (("gear", "gears"), _MEASURED + ("physics", "simple machine", "machines", "ratio")),
    "A gear is a toothed wheel that turns another wheel, so turning one turns the other at a "
    "different speed or with more force: a small gear driving a big one gives slow, strong, and "
    "the other way round gives fast, weak, which is how a bike's gears work.",
    avoid=_RECORD_WORDS + ("camping", "fishing", "climbing", "walking", "kit", "stuff",
                           "what gear do i need", "what gear should i", "list", "buy", "shop",
                           "cheap", "best"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "pendulum-what",
    (("pendulum", "pendulums"), _MEASURED + ("physics", "clock", "swing")),
    "A pendulum is a weight on a string that swings to and fro at a steady rate, which is how "
    "clocks kept time for three hundred years: a longer string swings more slowly, and the weight "
    "hardly matters.",
    avoid=_RECORD_WORDS + ("buy", "shop", "gift", "decor", "art", "tattoo"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "torque-what",
    (("torque",), _MEASURED + ("physics", "car", "engine", "measured in", "unit", "formula")),
    "Torque is a turning force, measured in newton metres: force times the distance from the "
    "pivot. That is why a longer spanner loosens a tight bolt more easily, and why a car engine's "
    "torque figure tells you how hard it pulls low down rather than how fast it goes.",
    avoid=_RECORD_WORDS + ("figures", "bhp", "hp", "spec", "specs", "which car", "buy",
                           "setting", "wrench", "nm setting", "manual"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "buoyancy-what",
    (("buoyancy", "buoyant"), _MEASURED + ("physics", "float", "floats", "water")),
    "Buoyancy is the upward push a liquid or gas gives anything in it, equal to the weight of the "
    "fluid it pushes aside. A steel ship floats because the air inside makes it push aside more "
    "water than the ship itself weighs, while a solid lump of steel cannot.",
    avoid=_RECORD_WORDS + ("aid", "jacket", "life jacket", "swim", "swimming", "pool",
                           "boat", "buy"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "viscosity-what",
    (("viscosity", "viscous"), _MEASURED + ("physics", "oil", "liquid", "measured in")),
    "Viscosity is how thick a liquid is, or how hard it is to pour: honey is far more viscous "
    "than water. Engine oil is graded by it, so a 5W-30 flows easily when cold and stays thick "
    "enough when hot.",
    avoid=_RECORD_WORDS + ("oil", "engine oil", "grade", "5w", "10w", "car", "which oil",
                           "brand", "buy"),
    ask=_MEASURED, bias=2))


ENTRIES.append(entry(
    "convection-what",
    (("convection", "convection current", "convection currents"), _MEASURED),
    "Convection is heat carried by a moving fluid: warm air or water rises because it is lighter, "
    "cooler stuff sinks to take its place, and that loop is what heats a room and builds a "
    "thundercloud.",
    avoid=_RECORD_WORDS + ("oven", "fan oven", "microwave", "hob", "cooker", "setting", "bake",
                           "air fryer", "recipe"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "conduction-what",
    (("conduction", "thermal conduction"), _MEASURED),
    "Conduction is heat moving through a solid, passed from one particle to the next: a metal "
    "spoon left in soup gets hot to the handle while a wooden one does not, because metals carry "
    "heat well and wood does not.",
    avoid=_RECORD_WORDS + ("nerve", "hear", "hearing", "block", "heart", "bone", "headphones",
                           "audio", "earbuds"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "radiation-what",
    (("radiation",), _MEASURED + ("physics", "heat", "sun")),
    "Radiation is energy travelling as waves or particles, and heat that reaches us from the Sun "
    "crosses empty space that way, with nothing to carry it. The word also covers the harmful "
    "ionising sort, from X-rays and nuclear material, which is why those have safety limits.",
    avoid=_RECORD_WORDS + ("therapy", "cancer", "treatment", "exposure", "safe", "leak",
                           "nuclear", "radon", "wifi", "5g", "mobile phone", "microwave"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "refraction-what",
    (("refraction", "refract"), _MEASURED),
    "Refraction is light bending as it crosses from one material into another at an angle, "
    "because it changes speed: that is why a straw looks broken in a glass of water, and how a "
    "lens or a pair of glasses focuses light.",
    avoid=_RECORD_WORDS + ("eye", "eyes", "test", "glasses", "prescription", "laser", "surgery",
                           "cataract", "specs"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "decibel-what",
    (("decibel", "decibels", "db"), _MEASURED + ("sound", "loud", "noise")),
    "A decibel measures how loud a sound is, on a scale where each extra 10 dB is about ten times "
    "the power and roughly twice as loud to the ear: a whisper is about 30, ordinary talk about "
    "60, and 85 or more for long spells can damage hearing.",
    avoid=_RECORD_WORDS + ("tinnitus", "hearing", "ear", "headphones", "noise complaint",
                           "too loud", "how loud", "is it too"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "solvent-what",
    (("solvent", "solvents"), _MEASURED + ("chemistry", "dissolve")),
    "A solvent is the liquid something dissolves in, and the thing that dissolves is the solute: "
    "water is the usual solvent, while white spirit and acetone dissolve things water cannot, "
    "like paint and nail polish.",
    avoid=_RECORD_WORDS + ("abuse", "glue", "adhesive", "paint", "pvc", "cement", "cleaner",
                           "which solvent", "buy", "fumes"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "half-life-what",
    (("half life", "half-life", "half lives"), _MEASURED + ("physics", "radioactive",
                                                           "radiation", "chemistry")),
    "The half-life of a radioactive substance is the time it takes for half of it to decay: "
    "carbon-14's is about 5,730 years, which is how wood and bone are dated, and after ten "
    "half-lives almost none is left.",
    avoid=_RECORD_WORDS + ("game", "film", "movie", "series", "book", "song", "value",
                           "dose", "medicine", "drug", "tablet"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "radioactivity-what",
    (("radioactivity", "radioactive"), _MEASURED + ("physics", "atom", "atoms")),
    "Radioactivity is what unstable atoms give off, rays or particles, as they settle into a "
    "steadier state: it happens on its own and cannot be switched off. It powers a nuclear plant, "
    "and the tiny amount in a smoke alarm is what sets it off.",
    avoid=_RECORD_WORDS + ("test", "level", "levels", "safe", "radon", "leak", "waste",
                           "nuclear", "danger", "is it"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "equator-what",
    (("equator",), ("what", "mean", "meaning", "definition", "explain", "why")),
    "The equator is the imaginary line round the middle of the Earth, halfway between the poles "
    "at zero degrees latitude: day and night are about twelve hours each there all year, and the "
    "sun passes almost straight overhead.",
    avoid=_RECORD_WORDS + ("crossing", "ceremony", "cruise", "flight", "hotel", "visit"),
    ask=("what", "mean", "meaning", "definition", "explain"), bias=2))

ENTRIES.append(entry(
    "latitude-what",
    (("latitude",), ("what", "mean", "meaning", "definition", "explain", "why")),
    "Latitude is how far north or south of the equator a place is, in degrees from 0 at the "
    "equator to 90 at the poles: London is about 51 north, and your latitude is what sets how "
    "long the days are and how warm the place gets.",
    avoid=_RECORD_WORDS + ("of london", "of my", "what is my", "app", "gps", "phone"),
    ask=("what", "mean", "meaning", "definition", "explain"), bias=2))

ENTRIES.append(entry(
    "longitude-what",
    (("longitude",), ("what", "mean", "meaning", "definition", "explain", "why")),
    "Longitude is how far east or west of Greenwich a place is, measured in degrees up to 180 "
    "each way, and it is what sets your time zone. Sailors could find their latitude for "
    "centuries before they could find their longitude, which is why accurate clocks were so "
    "valuable.",
    avoid=_RECORD_WORDS + ("what is my", "app", "gps", "phone"),
    ask=("what", "mean", "meaning", "definition", "explain"), bias=2))

ENTRIES.append(entry(
    "nebula-what",
    (("nebula", "nebulae", "nebulae"), ("what", "mean", "meaning", "definition", "explain")),
    "A nebula is a cloud of gas and dust in space, either thrown off by a dying star or the stuff "
    "new stars are forming out of: the Orion Nebula is a star nursery you can pick out with your "
    "eyes as a fuzzy patch below the belt.",
    avoid=_RECORD_WORDS + ("film", "movie", "song", "game", "wallpaper", "buy"),
    ask=("what", "mean", "meaning", "definition", "explain"), bias=2))


ENTRIES.append(entry(
    "herbivore-what",
    (("herbivore", "herbivores"), _MEASURED),
    "A herbivore is an animal that eats only plants: a cow, a rabbit, a deer, a caterpillar. Its "
    "teeth grind and its gut is long enough to break down plant fibre, which is why it spends much "
    "of the day eating.",
    avoid=_RECORD_WORDS + ("dinosaur", "diet", "recipe", "vegan", "lose weight", "meal"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "carnivore-what",
    (("carnivore", "carnivores"), _MEASURED),
    "A carnivore is an animal that eats other animals: a lion, a cat, a heron, a spider. Most have "
    "sharp teeth or a beak for tearing meat, and a short gut, because meat is easier to digest than "
    "plants.",
    avoid=_RECORD_WORDS + ("dinosaur", "diet", "recipe", "cooking", "restaurant", "meal"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "omnivore-what",
    (("omnivore", "omnivores"), _MEASURED),
    "An omnivore eats both plants and animals: people, pigs, bears, crows and most gulls. That mix "
    "is why our teeth are partly sharp and partly flat, and why a varied diet suits us.",
    avoid=_RECORD_WORDS + ("dinosaur", "diet", "recipe", "meal"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "prey-what",
    (("prey",), _MEASURED),
    "Prey is the animal a predator hunts and eats: a rabbit for a fox, a zebra for a lion. The word "
    "is about the role in the food chain rather than the act of hunting: an animal can be prey to "
    "one thing and a predator of another.",
    avoid=_RECORD_WORDS + ("prey on my mind", "prey upon", "prayer", "pray", "church",
                           "religion", "fishing lure", "hunting"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "biome-what",
    (("biome", "biomes"), _MEASURED),
    "A biome is a large region with one climate and the plants and animals that go with it: "
    "rainforest, desert, grassland, tundra, coral reef. The same biome turns up on different "
    "continents, because it is the climate that decides it.",
    avoid=_RECORD_WORDS + ("minecraft", "game", "skin", "mod", "seed"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "niche-what",
    (("niche",), ("what", "mean", "meaning", "definition", "explain", "biology", "ecology")),
    "In biology, a niche is the job a species does where it lives: what it eats, when it is active, "
    "where it shelters and what eats it. Two species with the same niche in one place compete, and "
    "one usually wins or moves away.",
    avoid=_RECORD_WORDS + ("perfume", "fragrance", "scent", "business", "market", "shop",
                           "buy", "products"),
    ask=("what", "mean", "meaning", "definition", "explain"), bias=2))

ENTRIES.append(entry(
    "lichen-what",
    (("lichen", "lichens"), _MEASURED),
    "A lichen is not one thing but two living together: a fungus with algae or bacteria inside it, "
    "sharing food the algae make from light and shelter the fungus gives. That is why lichen grows "
    "on bare rock and why it is a sign of clean air.",
    avoid=_RECORD_WORDS + ("proxy", "sclerosis", "skin", "treatment", "cream", "planus",
                           "lichen planus", "genital", "mouth", "rash"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "plankton-what",
    (("plankton",), _MEASURED),
    "Plankton is the mass of tiny plants and animals drifting in water that cannot swim against the "
    "current: the plant sort makes oxygen and feeds everything up to the whales. Half the oxygen you "
    "breathe was made by it.",
    avoid=_RECORD_WORDS + ("spongebob", "film", "movie", "game"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "spore-what",
    (("spore", "spores"), _MEASURED),
    "A spore is a single cell that fungi, mosses and ferns release instead of seed, and it grows "
    "into a new plant if it lands somewhere damp enough. That is why mould spreads through a room "
    "as dust, and why moss appears on a wall.",
    avoid=_RECORD_WORDS + ("pore", "skincare", "skin", "cream", "acne"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "nectar-what",
    (("nectar",), _MEASURED),
    "Nectar is the sugary liquid flowers make to attract bees, butterflies and birds, and it is the "
    "payment for carrying pollen to the next flower. Honey is nectar that bees have concentrated.",
    avoid=_RECORD_WORDS + ("juice", "drink", "brand", "buy", "skincare", "face"),
    ask=_MEASURED, bias=2))


ENTRIES.append(entry(
    "alloy-what",
    (("alloy", "alloys"), _MEASURED + ("chemistry", "metal", "metals")),
    "An alloy is a metal mixed with another element to make it stronger or easier to work: steel "
    "is iron with carbon, brass is copper with zinc, and solder is tin with lead or silver. The "
    "mix is melted together rather than just glued, so it behaves as one metal.",
    avoid=_RECORD_WORDS + ("wheel", "wheels", "rim", "rims", "car", "tyre", "tire", "scuff",
                           "paint", "gate", "roof", "fence"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "sublimation-what",
    (("sublimation", "sublime"), _MEASURED + ("chemistry", "physics")),
    "Sublimation is a solid turning straight into a gas without melting first: dry ice does it at "
    "room temperature, and so does the ice in a freezer over months, which is why ice cubes shrink. "
    "The reverse, gas straight to solid, is deposition.",
    avoid=_RECORD_WORDS + ("print", "printing", "shirt", "mug", "design", "psychology",
                           "meaning in"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "distillation-what",
    (("distillation", "distil", "distilled"), _MEASURED + ("chemistry", "water")),
    "Distillation is boiling a liquid off a mixture and condensing it back to a liquid somewhere "
    "cooler, which separates things that boil at different temperatures: spirit is distilled from "
    "a fermented mash, and distilled water is water with the minerals left behind.",
    avoid=_RECORD_WORDS + ("whisky", "whiskey", "gin", "vodka", "rum", "still", "buy",
                           "brand", "brewing"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "filtration-what",
    (("filtration", "filtrate"), _MEASURED + ("chemistry", "water")),
    "Filtration is passing a mixture through something with holes too small for the solid bits, so "
    "the liquid goes through and the solid stays behind: a coffee filter, a sieve in a flour mill, "
    "a kidney. It separates a solid from a liquid but not one dissolved chemical from another.",
    avoid=_RECORD_WORDS + ("pool", "pond", "tap", "water filter", "aquarium", "fish tank",
                           "coffee", "kettle", "buy"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "oxidation-what",
    (("oxidation", "oxidise", "oxidize"), _MEASURED + ("chemistry",)),
    "Oxidation is a substance reacting with oxygen: iron rusts, a cut apple browns, a fire burns, "
    "and the cells in your body get energy the same way. It does not always need a flame; slow "
    "oxidation is what rust and browning are.",
    avoid=_RECORD_WORDS + ("cholesterol", "antioxidant", "wine", "stainless", "rust", "rusty",
                           "metal", "apple", "avocado"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "combustion-what",
    (("combustion",), _MEASURED + ("chemistry",)),
    "Combustion is burning: a fuel reacts with oxygen and gives out heat and light, usually "
    "leaving carbon dioxide and water. It needs fuel, oxygen and enough heat to start, which is why "
    "a fire goes out when you cut off the air.",
    avoid=_RECORD_WORDS + ("engine", "car", "boiler", "spontaneous", "human", "fire", "stove",
                           "wood burner", "efficiency"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "proton-what",
    (("proton", "protons"), _MEASURED + ("physics", "chemistry", "atom")),
    "A proton is one of the particles in the middle of an atom, carrying a positive charge, and the "
    "number of them is what makes an element what it is: one is hydrogen, six is carbon, eight is "
    "oxygen.",
    avoid=_RECORD_WORDS + ("therapy", "cancer", "beam", "treatment", "nhs"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "electron-what",
    (("electron", "electrons"), _MEASURED + ("physics", "chemistry", "atom")),
    "An electron is the tiny negative particle that orbits the nucleus of an atom, and it is the "
    "one that moves when electricity flows. Its arrangement decides how an atom joins others, which "
    "is the whole of chemistry in one sentence.",
    avoid=_RECORD_WORDS + ("microscope", "configuration", "bill", "billing", "signature",
                           "document", "transfer", "app"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "exothermic-what",
    (("exothermic", "exothermic reaction"), _MEASURED + ("chemistry",)),
    "An exothermic reaction gives out heat as it happens, so the mixture gets warmer: burning, "
    "rusting and the reaction in a hand warmer are all exothermic. The opposite, one that takes "
    "heat in and feels cold, is endothermic.",
    avoid=_RECORD_WORDS + ("example", "examples", "gcse", "exam", "revision", "worksheet"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "suspension-what",
    (("suspension", "suspensions"), ("what", "mean", "meaning", "definition", "explain",
                                     "chemistry", "mixture")),
    "In chemistry a suspension is solid bits mixed through a liquid that do not dissolve and settle "
    "out if you leave it: muddy water, or flour stirred into water. Shaking it mixes it again, "
    "which is how it differs from a solution.",
    avoid=_RECORD_WORDS + ("car", "bike", "bicycle", "fork", "shock", "shocks", "spring",
                           "school", "work", "job", "driving", "licence", "license", "mot",
                           "bridge", "bridges", "viaduct", "tower", "towers", "span", "cables"),
    ask=("what", "mean", "meaning", "definition", "explain"), bias=2))

ENTRIES.append(entry(
    "colloid-what",
    (("colloid", "colloids", "colloidal"), _MEASURED + ("chemistry", "mixture")),
    "A colloid is a mixture where tiny particles of one substance are spread through another and "
    "stay spread: milk, fog, mayonnaise and paint are colloids. The particles are bigger than in a "
    "solution but too small to settle like a suspension.",
    avoid=_RECORD_WORDS + ("silver", "supplement", "oatmeal", "bath", "buy"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "covalent-bond-what",
    (("covalent bond", "covalent bonds", "covalent"), _MEASURED + ("chemistry", "bonding")),
    "A covalent bond is two atoms sharing a pair of electrons, which is how most of the molecules "
    "around you are held together: water, oxygen, sugar, plastic. Sharing is what makes a molecule "
    "stay one thing, rather than the ions of an ionic bond.",
    avoid=_RECORD_WORDS + ("gcse", "exam", "revision", "worksheet"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "electrolysis-what",
    (("electrolysis",), _MEASURED + ("chemistry",)),
    "Electrolysis is passing a current through a liquid or solution to drive a chemical change that "
    "would not happen on its own: it splits water into hydrogen and oxygen, and it is how aluminium "
    "is extracted and how metal is plated.",
    avoid=_RECORD_WORDS + ("hair", "hair removal", "beauty", "facial", "laser", "permanent",
                           "treatment", "salon", "painful"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "meteorite-what",
    (("meteorite", "meteorites", "meteor", "meteors"), _MEASURED),
    "A meteorite is a rock from space that has landed on the ground; while it is still burning "
    "through the air it is a meteor, or a shooting star. Most are chips off asteroids, and the "
    "biggest found weighs about 60 tonnes.",
    avoid=_RECORD_WORDS + ("for sale", "buy", "worth", "value", "price", "ring", "pendant",
                           "jewellery", "jewelry", "watch"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "pulsar-what",
    (("pulsar", "pulsars"), _MEASURED),
    "A pulsar is a tiny, extremely dense dead star that spins and sweeps a beam of radio waves past "
    "the Earth, so a telescope sees a regular pulse: some tick faster than a kitchen blender. They "
    "are accurate enough to be used as clocks.",
    avoid=_RECORD_WORDS + ("watch", "buy", "price", "casio", "seiko"),
    ask=_MEASURED, bias=2))


THE_ROCK = frozenset("""weathering weathered erosion erode rock rocks soil science homework
geology""".split())
THE_SKY = frozenset("""weather forecast today tomorrow tonight weekend weekends outside""".split())


def _the_rock_and_not_the_sky(understood):
    words = set(understood.get("words") or ())
    if words & THE_ROCK:
        return True
    return not (words & THE_SKY)


ENTRIES.append(entry(
    "weathering-what",
    (("weathering",), _MEASURED + ("rock", "rocks", "science", "erosion")),
    "Weathering is rock being broken up where it sits, by rain, frost, wind, roots or weak acid, "
    "without being carried away. Erosion is the next step: the loosened pieces being moved "
    "somewhere else.",
    avoid=("forecast", "today", "tomorrow", "weekend", "rain today", "sunny", "climate",
           "cold", "hot", "snow"),
    guard=_the_rock_and_not_the_sky,
    ask=_MEASURED, bias=6))

ENTRIES.append(entry(
    "rain-shadow-what",
    (("rain shadow", "rain shadow desert"), _MEASURED + ("desert", "mountain", "mountains")),
    "A rain shadow is the dry side of a mountain range: air is forced up the windward side, drops "
    "its rain there, and comes down the other side warm and dry. Deserts like the one east of the "
    "Rockies sit in a rain shadow.",
    avoid=("of an object", "light", "length", "sunlight", "dark", "eye shadow", "eyeshadow"),
    ask=_MEASURED, bias=6))

def _the_ocean_current(understood):
    words = understood.get("words") or ()
    return "stream" in words and "gulf" in words or "atlantic" in words


ENTRIES.append(entry(
    "gulf-stream-what",
    (("gulf stream", "gulf", "atlantic current"),
     _MEASURED + ("ocean", "atlantic", "weather", "climate")),
    "The Gulf Stream is a fast warm current that carries water from the Gulf of Mexico up the east "
    "coast of America and across the Atlantic. Its heat is why Britain and Ireland are milder than "
    "the same latitude in Canada.",
    avoid=("netflix", "series", "tv", "watch", "service", "subscription", "subscribe",
           "film", "movie", "shows", "boxset"),
    ask=_MEASURED, guard=_the_ocean_current, bias=6))

ENTRIES.append(entry(
    "tide-pool-what",
    (("tide pool", "tide pools", "rock pool", "rock pools"), _MEASURED),
    "A tide pool is the pocket of seawater left behind in the rocks when the tide goes out, and it "
    "is a small sheltered world: anemones, limpets, crabs and weed that survive being cut off until "
    "the water comes back.",
    ask=_MEASURED, bias=3))

ENTRIES.append(entry(
    "sediment-what",
    (("sediment", "sediments"), _MEASURED),
    "Sediment is the loose material that settles at the bottom of water or is dropped by wind and "
    "ice: sand, mud, grit and bits of shell. Pressed together over millions of years, sediment "
    "becomes sedimentary rock like sandstone and chalk.",
    avoid=_RECORD_WORDS + ("wine", "bottle", "coffee", "filter", "sediment in my"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "magma-what",
    (("magma",), _MEASURED),
    "Magma is molten rock under the ground; once it reaches the surface it is called lava. It forms "
    "where rock gets hot enough to melt, and because it is lighter than the rock around it, it rises.",
    avoid=_RECORD_WORDS + ("film", "movie", "game", "band", "album", "poem"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "lava-what",
    (("lava",), _MEASURED),
    "Lava is molten rock that has come out of a volcano onto the surface; the same stuff underground "
    "is magma. It cools into rock, and runny lava flows far while thick lava piles up near the vent.",
    avoid=_RECORD_WORDS + ("lamp", "lamps", "soap", "buy", "colour", "color"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "earthquake-what",
    (("earthquake", "earthquakes"), _MEASURED),
    "An earthquake is the ground shaking when two slabs of the Earth's crust slip past each other "
    "and the energy built up is released as waves. The slipping happens at a fault, and the shaking "
    "is strongest near it.",
    avoid=_RECORD_WORDS + ("insurance", "cover", "damage", "claim", "building", "house",
                           "safe", "kit"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "sea-breeze-what",
    (("sea breeze", "sea breezes", "land breeze"), _MEASURED),
    "A sea breeze is the cool air blowing in off the sea on a sunny afternoon, because land heats "
    "faster than water, so the warm air over the land rises and the cooler sea air moves in to "
    "replace it. At night the pattern reverses as the land cools faster.",
    avoid=_RECORD_WORDS + ("hair", "skin", "perfume", "candle", "candle scent", "air freshener"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "precipitation-what",
    (("precipitation",), _MEASURED + ("weather", "rain", "water cycle")),
    "Precipitation is water falling out of the sky - rain, snow, sleet or hail - when droplets in a "
    "cloud join up until they are too heavy to stay up. It is one step of the water cycle, after "
    "evaporation and condensation.",
    avoid=_RECORD_WORDS + ("chemistry", "reaction", "test", "blood", "chemical"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "carbon-footprint-what",
    (("carbon footprint", "carbon footprints"), _MEASURED),
    "A carbon footprint is the total greenhouse gas your choices add up to in a year, counted as "
    "carbon dioxide: heating, electricity, flights, car trips, the food and things you buy. A "
    "typical UK footprint is around 10 tonnes a year, and flying and meat are usually the biggest "
    "single items.",
    avoid=_RECORD_WORDS + ("calculate", "calculator", "offset", "offsets", "reduce",
                           "how do i"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "clay-what",
    (("clay",), _MEASURED + ("soil", "rock", "science")),
    "Clay is a soil and rock material made of microscopic flat particles that pack tightly, so it "
    "holds water and feels sticky when wet and hard when dry. Pots and bricks are made from it "
    "because it can be shaped wet and keeps that shape when fired.",
    avoid=_RECORD_WORDS + ("pigeon", "target", "shooting", "tennis", "court", "face mask",
                           "mask", "skin", "hair", "paint", "cat litter"),
    ask=_MEASURED, bias=2))

ENTRIES.append(entry(
    "fault-line-what",
    (("fault line", "fault lines", "geological fault"), _MEASURED),
    "A fault line is a crack in the Earth's crust where the rock on either side has moved, and it "
    "is where most earthquakes happen because the two sides keep slipping. The San Andreas fault is "
    "the best known.",
    avoid=_RECORD_WORDS + ("relationship", "team", "argument", "blame", "politics", "party"),
    ask=_MEASURED, bias=2))

_SLEEP_MAGNESIUM = ("Magnesium has only a little evidence behind it, and only if you are short "
                    "of it: the glycinate or citrate sorts, not the oxide.")
_SLEEP_VALERIAN = "Valerian and the herbal teas do very little in trials."
_SLEEP_GUMMIES = "The gummies are usually a low dose of melatonin or an antihistamine."
_SLEEP_HABIT = ("What beats them is a steady wake-up time, no caffeine after early afternoon, "
                "and getting up rather than lying there.")
_SLEEP_CHILD = "For a child, ask a pharmacist or the GP first."
_SLEEP_CHILD_WORDS = (" child", "kids", "kid ", "my son", "my daughter", "baby", "toddler",
                      "teenager", "my boy", "my girl", " 8 year", " 9 year", " 10 year",
                      " 11 year", " 12 year")


def _sleep_supplements_reply(memory, understood):
    clean = " " + (understood.get("clean") or understood.get("text") or "").lower() + " "
    for word in _SLEEP_CHILD_WORDS:
        if word in clean:
            return " ".join([_SLEEP_CHILD, _SLEEP_MAGNESIUM, _SLEEP_HABIT])
    if "valerian" in clean or "herbal" in clean or "tea" in clean:
        order = (_SLEEP_VALERIAN, _SLEEP_MAGNESIUM, _SLEEP_GUMMIES)
    elif "gumm" in clean or "melatonin" in clean or "antihistamine" in clean:
        order = (_SLEEP_GUMMIES, _SLEEP_MAGNESIUM, _SLEEP_VALERIAN)
    else:
        order = (_SLEEP_MAGNESIUM, _SLEEP_VALERIAN, _SLEEP_GUMMIES)
    return " ".join(order + (_SLEEP_HABIT,))

ENTRIES.append(entry(
    "sleep-supplements",
    (("magnesium", "valerian", "sleep gummies", "gummies", "herbal sleep", "sleep supplement",
      "sleep supplements", "supplements for sleep", "sleep aid", "sleep aids", "natural sleep",
      "natural remedy", "what can i take to sleep", "anything i can take to sleep",
      "something to help me sleep", "something to help me sleep", "sleeping remedy",
      "sleep remedy"),
     ("sleep", "sleeping", "asleep", "help", "helps", "work", "works", "take", "taking",
      "bed", "night", "nights", "insomnia", "better", "anything", "supplement", "tablet",
      "tablets", "pill", "pills")),
    ask=("take", "taking", "tablet", "tablets", "pill", "pills", "supplement", "supplements",
         "dose", "dosage", "gummy", "gummies", "magnesium", "valerian", "herbal", "remedy",
         "remedies", "aid", "aids", "anything", "something", "worth", "try", "trying",
         "help you sleep", "helps you sleep", "help me sleep", "good for sleep",
         "good for sleeping"),
    reply=_sleep_supplements_reply,
    bias=1,
    avoid=("foods", "food", "diet", "rich in", "deficiency", "deficient", "how much magnesium",
           "cramp", "cramps", "restless legs", "melatonin",
           "pregnant", "pregnancy", "breastfeeding")))

ENTRIES.append(entry(
    "vacuum-what",
    (("vacuum",), _MEASURED + ("physics", "space")),
    "In physics a vacuum is a space with no matter in it at all, or as close as anyone gets: there "
    "is no air in space, and a thermos flask keeps its heat by holding a vacuum between two walls. "
    "It is also why a vacuum cleaner's fan can push air in.",
    avoid=_RECORD_WORDS + ("cleaner", "cleaners", "hoover", "bag", "filter", "robot", "cordless",
                           "buy", "best", "which"),
    ask=_MEASURED, bias=4))
ENTRIES.append(entry(
    "carbon-footprint",
    (("carbon footprint", "carbon footprints", "my carbon footprint", "co2 footprint",
      "carbon emissions", "my emissions", "greenhouse gas"),
     ("what is", "whats", "what does", "mean", "means", "reduce", "lower", "cut", "shrink",
      "how big", "size", "offset", "calculate", "work out", "biggest", "how much", "co2")),
    "A carbon footprint is the total greenhouse gas a person, a household or a product causes, "
    "counted in kilograms of carbon dioxide equivalent over a year. For a household in the UK it "
    "is roughly 8 to 10 tonnes, and the weight is not where people think: heating and electricity "
    "and car travel are the bulk of it, while a flight is big in one hit and a plastic bag is "
    "almost nothing. The changes that move it most are the boring ones - a heat pump or good "
    "insulation, less red meat and dairy, fewer and shorter flights, a smaller car - and offsetting "
    "does not cancel them out.",
    avoid=("footprint in", "sand", "tyre", "tire", "shoe", "data footprint", "building footprint",
           "boot", "animal", "dinosaur", "imprint"),
    bias=1))
