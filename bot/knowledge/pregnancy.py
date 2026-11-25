import datetime
import re

from .lookup import entry

ANSWERS = ("health", "food-and-drink")


def _a_late_that_is_not_a_period(understood):
    if not isinstance(understood, dict):
        return True
    if (understood.get("sense") or {}).get("late") == "time":
        return False
    if not understood.get("shift"):
        return True
    text = understood.get("clean") or ""
    return bool(re.search(r"\b(?:periods?|cycles?|pregnan\w*|tests?)\b", text, re.I))

PREGNANT = ("pregnant", "pregnancy", "pregnancies", "expecting a baby", "expecting our baby",
            "trimester", "weeks pregnant", "months pregnant", "im having a baby",
            "i'm having a baby", "baby on the way", "antenatal", "first baby", "second baby",
            "third baby")

PREGNANT_MOVEMENT = ("exercise", "exercising", "workout", "work out", "workouts", "gym",
                     "run", "running", "jog", "jogging", "swim", "swimming", "lengths",
                     "weights", "lift", "lifting", "weight training", "strength training",
                     "yoga", "pilates", "spin", "spinning", "cycling", "cycle", "bike",
                     "walking", "walks", "hike", "hiking", "dance", "dancing", "zumba",
                     "tennis", "badminton", "netball", "football", "hockey", "climbing",
                     "horse riding", "riding", "skiing", "ski", "crossfit", "fitness class",
                     "aerobics", "training", "keep fit", "stay active", "active")

NOT_FOOD = (
    "morning sickness", "nausea", "sick every", "bleeding", "bleed", "spotting", "cramps",
    "cramping", "scan", "scans", "midwife", "labour", "labor", "birth", "c-section", "induction",
    "glucose test", "gestational", "pre-eclampsia", "blood pressure", "kick", "kicks",
    "movement", "movements", "heartbeat", "twins", "miscarriage", "ectopic", "test", "tests",
    "folic acid", "vitamin d", "vitamin a", "supplement", "supplements", "paracetamol",
    "ibuprofen", "medicine", "medication", "tablet", "tablets", "antibiotic", "vaccine",
    "headache", "headaches", "migraine", "migraines", "pain", "painful", "sore",
    "soreness", "ache", "aches", "aching", "hurts", "hurting", "toothache",
    "travel", "flight", "fly", "flying", "sleep", "sleeping", "sex", "exercise", "gym",
    "swim", "swimming", "bump", "back", "backache", "heartburn", "constipation", "swollen",
    "stretch marks", "weight gain", "how much weight", "mood", "anxious", "anxiety", "sick of",
    "not pregnant", "no longer pregnant", "was pregnant", "weren't pregnant",
    "breastfeeding", "breastfeed", "nursing", "formula", "weaning", "my wife is not",
    "trying to get pregnant", "trying for a baby", "ivf", "fertility", "baby shower",
    "baby names", "nursery", "pram", "pushchair", "cot", "nappy", "nappies",
    "egg", "eggs", "runny egg", "raw egg", "mayonnaise", "mayo", "dippy",
)

LIST = ("The list is short: no soft mould-ripened or blue cheese unless it is cooked until "
        "steaming, no pate or liver, no raw or undercooked meat, fish or shellfish, and nothing "
        "made with unpasteurised milk. "
        "Everything else is fine - hard cheese, cooked eggs, cooked fish, peanuts, fruit and veg "
        "- though wash the veg and heat leftovers until they are steaming hot, because listeria "
        "is the reason for the whole list and it is killed by heat.")

PREG_WORRY_FOODS = (
    (("pineapple", "pineapples", "pineapple juice"),
     "Fine. Pineapple does not bring on labour: the enzyme people blame for it is in the stem, "
     "not in the fruit you eat, and a portion has nowhere near enough of it to do anything. So "
     "have it fresh, tinned or juiced - the myth is the only thing to worry about."),
    (("juice", "juices", "orange juice", "apple juice", "fruit juice", "grapefruit juice",
      "cranberry juice", "tomato juice", "a glass of juice"),
     "Juice is fine: the cartons and bottles in a shop are pasteurised already, so nothing on the "
     "pregnancy list applies to them, and juice you squeeze yourself is fine if you wash the fruit "
     "and drink it the same day. It is mostly sugar without the fibre that slows it down, so one "
     "glass with a meal is the habit to aim for rather than sipping it through the day, and whole "
     "fruit is the better version of the same vitamins."),
    (("mango", "mangoes", "mangos", "melon", "melons", "watermelon", "grapes", "grape", "kiwi",
      "kiwis", "berries", "strawberries", "blueberries", "raspberries", "blackberries",
      "peach", "peaches", "pear", "pears", "plum", "plums", "banana", "bananas", "orange",
      "oranges", "apple", "apples", "pineapple chunks", "satsuma", "satsumas", "clementine",
      "clementines"),
     "Fine, and worth eating: fruit is where most of the vitamin C comes from. Rinse it under the "
     "tap first, because listeria and toxoplasmosis are on the outside of fruit and veg rather "
     "than in it, and a melon wants washing before it is cut, not after. Fruit juice is fine too, "
     "but it is sugary - whole fruit is the better habit."),
    (("papaya", "papayas", "pawpaw", "pawpaws", "green papaya", "unripe papaya"),
     "Ripe papaya is fine. The one to leave is the unripe green papaya, and papaya skin and seeds: "
     "unripe papaya carries a latex-like substance that is said to act on the womb, so a green "
     "papaya salad is one to skip for nine months. A ripe orange one is a good breakfast."),
    (("honey",),
     "Fine for you. The warning about honey is for babies under one, whose gut can let botulism "
     "spores grow - it does not apply to you or to the baby before birth. It is still sugar, so a "
     "spoon in a drink rather than a jar a day."),
    (("hummus", "houmous", "humous", "tahini", "houmus"),
     "Fine, including the tubs from the supermarket: shop hummus is made with pasteurised sesame "
     "and chickpeas, and sesame is not one of the allergens to avoid in pregnancy. Keep an opened "
     "tub in the fridge and eat it within a couple of days, because it is a cold food and the "
     "listeria advice is about cold food."),
    (("spicy food", "spicy", "curry", "curries", "chilli", "chili", "chillies", "chilies",
      "hot sauce", "spices", "spice"),
     "Fine. Spicy food does not bring on labour or harm the baby, and the old advice to avoid it "
     "was about the mother's comfort. If you get heartburn, which is common later on, it is worth "
     "eating smaller amounts more often rather than avoiding spice altogether."),
    (("ice cream", "icecream", "soft serve", "soft-serve", "soft whip", "milkshake",
      "milkshakes"),
     "Fine from a tub: ice cream is made with pasteurised milk. The one to skip is soft-serve from "
     "a machine, the sort that sits in a hopper all day - that is the cold-served food listeria "
     "has been found in, and a machine that is not cleaned often is the risk. A scoop from a shop "
     "tub is no riskier than a supermarket one."),
    (("coleslaw", "slaw", "potato salad", "deli salad"),
     "Fine from a packet or a supermarket tub, which is made with pasteurised mayonnaise. The one "
     "to skip is salad that has been sitting out on a deli counter, and anything you are unsure "
     "has been kept cold: listeria grows in food that is kept cold for a while, not in food that "
     "is freshly made."),
    (("bean sprouts", "beansprouts", "sprouts", "sprouted seeds", "alfalfa"),
     "Cook them through, or leave them: raw bean sprouts and sprouted seeds are one of the foods "
     "listeria and salmonella have been found in, and washing does not reliably clear them. "
     "Sprouts cooked into a stir fry, a curry or a soup are fine."),
    (("olives", "pickles", "gherkins", "sauerkraut"),
     "Fine, and the vinegar or brine they are in is not a problem. They are salty, so if your "
     "ankles or blood pressure are being watched, keep them to a few rather than a bowl."),
    (("dates", "dates fruit"),
     "Fine, and a good snack: they are sweet, so they are the thing to reach for instead of a "
     "biscuit at four in the afternoon. There is no evidence they bring on labour, whatever "
     "you read."),
)

DRINKS_WITH_THEIR_OWN_ANSWER = (
    "alcohol", "wine", "beer", "lager", "cider", "stout", "ale", "prosecco", "champagne", "gin",
    "vodka", "whisky", "whiskey", "rum", "brandy", "tequila", "booze", "cocktail", "cocktails",
    "coffee", "caffeine", "decaf", "tea", "espresso", "latte", "cappuccino", "energy drink",
    "energy drinks", "cola", "diet coke", "hot chocolate", "mulled wine", "alcopop")

PREG_ANY_FOOD = (
    "That food is not on the list of things to avoid, so it is fine. The list is short: no "
    "mould-ripened or blue cheese unless it is cooked until steaming, no pate or liver, no raw "
    "meat, fish or shellfish, and nothing made with unpasteurised milk. Wash fruit and veg and "
    "heat leftovers until steaming - listeria is why the list exists, and heat kills it.")


def _preg_food(memory, understood):
    words = set(understood.get("words") or ())
    joined = " ".join(understood.get("words") or ())
    for names, reply in PREG_WORRY_FOODS:
        for name in names:
            if " " in name:
                if name in joined:
                    return reply
                continue
            if name in words or (name.endswith("s") and name[:-1] in words):
                return reply
    return PREG_ANY_FOOD


AM_I = ("am i", "am i not", "could i be", "could i", "might be", "might i", "maybe", "perhaps",
        "possibly", "possible", "think", "think im", "think i'm", "suspect", "wondering",
        "not sure", "unsure", "no idea", "or not", "when will i know", "how do i know",
        "how can i tell", "signs", "symptoms", "early", "missed")

WHEN = ("period", "periods", "missed period", "late period", "period late", "no period",
        "periods late", "period hasnt come", "period hasn't come", "period not come",
        "late", "late by", "days late", "weeks late", "due date", "baby due",
        "when am i due", "due date is", "missed", "irregular")

TEST_WORDS = ("pregnancy test", "test", "tests", "tested", "faint line",
              "clearblue", "test kit", "test strip", "test strips", "positive", "negative")

PREGNANT_ALREADY = ("im pregnant what", "i am pregnant what", "i'm pregnant what",
                    "im pregnant now what", "i am pregnant now what",
                    "im pregnant so what", "i am pregnant so what",
                    "found out im pregnant what", "found out i am pregnant what")

CYCLE_SHAPE = ("normal", "how long", "how often", "how many days", "days between", "lasts",
               "started", "when do periods", "first period", "regular")

FERTILITY = ("get pregnant on", "get pregnant after", "get pregnant if", "get pregnant while",
             "get pregnant from", "pregnant on my period",
             "conceive", "conceiving", "conception", "ovulate", "ovulating", "ovulation",
             "fertile", "fertility", "chance of", "chances of", "how likely")

NOT_A_TEST = ("covid", "coronavirus", "lateral flow", "pcr", "mot", "theory", "driving test",
              "eye test", "blood test", "urine test", "hearing test", "smear", "cervical",
              "chlamydia", "sti", "std", "thyroid", "diabetes", "allergy", "intolerance",
              "paternity", "dna", "quiz", "exam", "revision", "mock", "interview", "coding",
              "swab", "skin prick")

TEST_REPLY = (
    "A test is the answer, and the timing is the part people get wrong: from the day your period "
    "is due, on the first pee of the morning, which has the most hormone in it. A faint second "
    "line is still a line. If it is negative and nothing comes in three days, test again, because "
    "the hormone doubles every couple of days. Early signs - sore breasts, going off food, "
    "tiredness, feeling sick - are not reliable enough to go on either way. If you would rather "
    "not be pregnant, a GP or a sexual health clinic will go through the options without pushing "
    "you either way, and the sooner you ring the more there is to choose from.")

POSITIVE_REPLY = (
    "Ring the GP surgery and say you have had a positive test: the booking-in appointment is "
    "usually between 8 and 10 weeks, and they will sort the midwife, the scans and the bloods. "
    "Start 400 micrograms of folic acid and 10 micrograms of vitamin D every day, and stop "
    "alcohol - most of what you eat is still fine, and the list of what is not is short. If the "
    "line was faint or early, test again in three days. A negative test with no period in three "
    "days is worth testing again; a positive one with pain or bleeding is a call to the GP or "
    "111 rather than something to sit on.")

NEGATIVE_REPLY = (
    "A negative test this early is worth repeating rather than believing: test again in three "
    "days, first pee of the morning, because the hormone doubles every couple of days and an "
    "early test can simply be too soon. Plenty else shifts a period - stress, a bug, a bad "
    "month of sleep, a change in weight, travel, the pill - so one late period with a negative "
    "test is common and usually settles. Ring the GP if nothing comes for three months, if the "
    "tests stay negative but you feel pregnant, or if there is pain one side at all.")

EARLY_REPLY = (
    "A period that comes early is common and usually just a short cycle: stress, a bug, a change "
    "in sleep or travel, a big drop in weight, or the pill can all bring one on, and the spotting "
    "some people get at ovulation a couple of weeks before is often taken for one. Write the "
    "dates down for the next two or three - if they stay under three weeks apart, if you bleed "
    "between periods or after sex, or if the bleeding is very heavy, that is a GP appointment. "
    "If there is any chance you could be pregnant, test anyway: a bleed can happen early on.")

CYCLE_REPLY = (
    "The usual cycle is 21 to 35 days from the first day of one period to the first day of the "
    "next, and the bleeding itself is usually two to seven days - up to eight is still normal. "
    "What is worth a GP appointment: cycles closer than 21 days or longer than 35, bleeding that "
    "lasts more than eight days, bleeding between periods or after sex, soaking a pad or tampon "
    "an hour for several hours, or three months with no period at all. Write the dates down for "
    "three cycles first, because that is what the GP will ask for, and the pill can change the "
    "pattern while you are on it.")

LATE_REPLY = (
    "Plenty shifts a period by a few days - stress, a bug, a bad month of sleep, a change in "
    "weight, travel, the pill - so the useful next step is a test rather than a wait: from the "
    "day it was due, first pee of the morning, and again in three days if it is negative and "
    "nothing comes. Three months without a period, bleeding between periods or after sex, or a "
    "positive test with pain or bleeding is a GP appointment. If your cycles were always "
    "irregular, a few weeks late on its own is not alarming.")

_FEEDING_WORDS = ("breastfeed", "breastfeeding", "breast feeding", "breast fed", "breastfed",
                  "nursing", "nurse", "lactating", "chestfeeding", "expressing",
                  "pumping", "feeding")


_DUE_SHAPE = re.compile(
    r"\b(?:due date|due dates|baby due|baby is due|due in|when am i due|when are you due|"
    r"weeks pregnant|weeks along|weeks am i|weeks gone|"
    r"how far along|how far gone|what week am i|which week am i|"
    r"how many (?:weeks?|wks?|months) (?:pregnant|preg|am i|along|into|gone|left|to go)|"
    r"how pregnant am i|pregnancy weeks|"
    r"how many weeks (?:is|does|are) (?:a |the |an )?pregnan\w*|"
    r"how many months (?:pregnant|along)|"
    r"how long (?:is|does|are|do|can) (?:a |the |an )?pregnan\w*|"
    r"how long (?:are you|is a woman|is she|is he) pregnant|"
    r"last period|first day of (?:my|her|your|the) last period|"
    r"lmp\b|"
    r"(?:when|what date|which date)\b[^.?!]{0,30}\bdue\b|"
    r"when will (?:the baby|my baby|she|he|it) (?:arrive|come|be born|get here)|"
    r"when (?:is|are) (?:the baby|my baby|she|he|it) born|"
    r"when (?:is|are) (?:the baby|my baby|she|he|it) (?:due|coming))", re.I)

_PREG_WORD = re.compile(
    r"\b(?:pregnan\w*|preg|expecting|baby|babies|due date|lmp|last period|"
    r"weeks (?:pregnant|preg|along|gone|am i)|birth|born|midwife)\b", re.I)
_PREG_SOFT = re.compile(
    r"\b(?:how far along|how far gone|weeks am i|wks am i|what week am i|which week am i|"
    r"when am i due|when are you due|"
    r"when (?:is|are) (?:she|he) due|"
    r"due (?:in|on) (?:january|february|march|april|may|june|july|august|september|"
    r"october|november|december))\b", re.I)
_OTHER_SUBJECT = re.compile(
    r"\b(?:essay|project|thesis|dissertation|book|build|renovation|course|game|sprint|"
    r"assignment|paper|novel|training|app|website)\b", re.I)

_DUE_ELSEWHERE = re.compile(
    r"\bdue\s+(?:back|at work|for work|in work|"
    r"to (?:start|finish|go|leave|renew|pay|return|hand|come back)|"
    r"(?:a|an|any|some|my|the)?\s*(?:tax\s+)?(?:refund|rebate|payment|bill|rise|bonus|"
    r"money|fee|invoice))\b", re.I)

_A_MILESTONE = re.compile(
    r"\bwhen (?:will|do|should|can)\b[^?]{0,40}?"
    r"\b(?:feel (?:the )?(?:baby|it|them|kicks?|movement|movements)|kicks? (?:start|begin)|"
    r"start (?:to )?(?:show|showing)|be showing|bump (?:show|appear|grow)|"
    r"feel (?:him|her) move|movement)\b", re.I)

_PERIOD_ONLY = re.compile(r"\bperiods?\b", re.I)
_PERIOD_WITH_A_PREGNANCY = re.compile(
    r"\b(?:pregnan\w*|expecting|baby|babies|last period|lmp|weeks (?:pregnant|along|gone|am i)|"
    r"due date|when am i due|when are you due)\b", re.I)

_MONTHS = {
    "january": 1, "jan": 1, "february": 2, "feb": 2, "march": 3, "mar": 3, "april": 4,
    "apr": 4, "may": 5, "june": 6, "jun": 6, "july": 7, "jul": 7, "august": 8,
    "aug": 8, "september": 9, "sep": 9, "sept": 9, "october": 10, "oct": 10,
    "november": 11, "nov": 11, "december": 12, "dec": 12}
_DAY_THEN_MONTH = re.compile(
    r"\b(\d{1,2})(?:st|nd|rd|th)?\s+(?:of\s+)?([a-z]{3,9})\b", re.I)
_MONTH_THEN_DAY = re.compile(
    r"\b([a-z]{3,9})\s+(?:the\s+)?(\d{1,2})(?:st|nd|rd|th)?\b", re.I)
_A_PREGNANCY = re.compile(r"\b(?:a|the|an) pregnanc(?:y|ies)|\bpregnancies\b|"
                          r"\bpregnancy last(?:s|ing)?\b|\bpregnancy norm(?:al|ally)\b", re.I)
_MY_OWN = re.compile(r"\b(?:am i|i am|i'?m|im|my|me|we|us|our)\b", re.I)
_ASKS_WEEKS = re.compile(
    r"\b(?:how many (?:weeks?|wks?|months)|how far along|how far gone|weeks am i|wks am i|"
    r"weeks pregnant|weeks along|weeks gone)\b", re.I)
_WEEKS_NOW = re.compile(
    r"\b(?:im|i'?m|i am|am|is|are|at|now|about|nearly|almost|just|only)\s+"
    r"(\d{1,2})\s*(?:weeks?|wks?)\b"
    r"|\b(\d{1,2})\s*(?:weeks?|wks?)\s+(?:pregnant|along|gone|in)\b", re.I)


_SHORT_ASK = re.compile(r"\bdue date\b|\bhow far along\b", re.I)
_ASKED = re.compile(
    r"\bwhens?\b|\bwhen's\b|\bhow (?:many|far|long|soon|pregnant)\b|\bwhich date\b|"
    r"\bwhat date\b|\bwhat week\b|\bwhich week\b|\bpregnancy weeks\b|"
    r"\bcalculat\w* (?:my|the) due date\b|\bdue date calculator\b|"
    r"\bwhat(?:'s|s)? (?:is |was )?(?:my|the|your) (?:due date|date thing)\b", re.I)


_GIVES_THE_DAY = re.compile(r"\b(?:last period|period started|lmp|first day)\b", re.I)
_A_MONTH = re.compile(r"\b(?:january|february|march|april|may|june|july|august|september|"
                      r"october|november|december|jan|feb|mar|apr|jun|jul|aug|sep|sept|oct|"
                      r"nov|dec)\b", re.I)


def _gives_a_month(line):
    return bool(_A_MONTH.search(line or ""))


def _asks_when_due(understood):
    line = " ".join(str((understood or {}).get("clean") or "").split())
    if not line or not _DUE_SHAPE.search(line):
        return False
    if not _ASKED.search(line) and not (_GIVES_THE_DAY.search(line) and _A_MONTH.search(line)):
        if not (_SHORT_ASK.search(line) and len(line.split()) <= 4):
            return False
    if _DUE_ELSEWHERE.search(line) or _A_MILESTONE.search(line):
        return False
    if _PERIOD_ONLY.search(line) and not _PERIOD_WITH_A_PREGNANCY.search(line):
        return False
    if _PREG_WORD.search(line):
        return True
    return bool(_PREG_SOFT.search(line)) and not _OTHER_SUBJECT.search(line)


def _the_day(date, today):
    said = f"{date.day} {date.strftime('%B')}"
    return said if date.year == today.year else f"{said} {date.year}"


def _the_date_named(line, today):
    for match in _DAY_THEN_MONTH.finditer(line):
        day, month = int(match.group(1)), _MONTHS.get(match.group(2).lower())
        if month is not None:
            date = _the_date_in_this_year(today, month, day)
            if date:
                return date
    for match in _MONTH_THEN_DAY.finditer(line):
        month, day = _MONTHS.get(match.group(1).lower()), int(match.group(2))
        if month is not None:
            date = _the_date_in_this_year(today, month, day)
            if date:
                return date
    return None


def _the_date_in_this_year(today, month, day):
    for year in (today.year, today.year - 1):
        try:
            date = datetime.date(year, month, day)
        except ValueError:
            return None
        if date <= today + datetime.timedelta(days=3):
            return date
    return None


def _the_weeks_named(line):
    for match in _WEEKS_NOW.finditer(line):
        figure = match.group(1) or match.group(2)
        if figure:
            weeks = int(figure)
            if 1 <= weeks <= 45:
                return weeks
    return None


CARD = ("Forty weeks from the first day of your last period, so count 280 days from it "
        "(nine months and a week): a midwife writes that date in your notes at your "
        "booking-in appointment, and the dating scan can move it by a few days. If you have "
        "neither to hand, the date on your scan report or in your maternity notes is the one "
        "they will go by. Weeks gone are counted from that same first day of your last "
        "period, not from the day you conceived.")


def _preg_due_date(memory, understood):
    line = " ".join(str((understood or {}).get("clean") or "").split())
    today = datetime.date.today()
    weeks = _the_weeks_named(line)
    if weeks is not None:
        left = 40 - weeks
        if left < 0:
            return (f"At {weeks} weeks you are past the 40-week due date, so the date on your "
                    "notes and your midwife are the ones to go by now. Most places offer an "
                    "induction by 41 or 42 weeks, and she will talk you through what happens "
                    "next - worth asking her at your next appointment rather than waiting.")
        date = today + datetime.timedelta(days=left * 7)
        return (f"Week {weeks} of 40 leaves {left} weeks to go, which puts the due date at about "
                f"{_the_day(date, today)}. That is the 40-week count, but the dating scan at 11 "
                "to 14 weeks is the date the midwife goes by, so go by what is on the notes if "
                "the scan moved it.")
    named = _the_date_named(line, today)
    if named is not None:
        date = named + datetime.timedelta(days=280)
        said = (f"Counted from the first day of the last period, {_the_day(named, today)}, the "
                f"due date is about {_the_day(date, today)} - 40 weeks, or 280 days, later. ")
        days = (today - named).days
        if 0 <= days <= 300:
            return (said + f"That makes you {days // 7} weeks now. The dating scan at 11 to 14 "
                    "weeks is the date the midwife goes by, so if it moved the date, the scan is "
                    "the one that counts.")
        return (said + "If that is not the day you meant, tell me the first day of the last "
                "period as a date and I will work it out again.")
    return CARD


def _preg_hair_dye(memory, understood):
    line = " " + str((understood or {}).get("clean") or "") + " "
    if any((" " + word + " ") in line or word in line for word in _FEEDING_WORDS):
        return ("A colour is fine while you are breastfeeding: the dye does not get into your "
                "milk, so nothing reaches the baby through a feed. Keep the room aired, wear the "
                "gloves that come with the kit and do the 48-hour patch test first, because skin "
                "can react differently after a baby. Highlights or a semi-permanent keep the dye "
                "off your scalp if you would rather be careful, and a salon can do the mixing for "
                "you.")
    return ("Fine, and there is no evidence hair dye harms a baby: the amount that reaches your "
            "bloodstream through the scalp is tiny. Plenty of women wait until after 12 weeks "
            "before colouring, which is a reasonable choice rather than a rule. Have the patch "
            "test as usual, keep the dye off a cut or an eczema patch, and make sure the room is "
            "ventilated if you are doing it at home.")


_TIME_ASK = re.compile(
    r"\bhow long\b|\bhow many hours\b|\bhow many days\b|\bhow soon\b|\bhow early\b|"
    r"\bwhen should i\b|\bwhen do i\b|\bwhen to\b|\bwhat week\b|\bhow far along\b|"
    r"\bwhat (?:should|shall|can|do) i (?:take|bring|pack|put)\b|"
    r"\bwhat do i (?:need|want|have) to (?:pack|take|bring)\b|"
    r"\bwhat to (?:take|bring|pack)\b|"
    r"\blonger\b|\bshorter\b|\bquicker\b|\bfaster\b|\blongest\b|\btoo long\b", re.I)
_BIRTH_WORD = re.compile(
    r"\bin labour\b|\bin labor\b|\blabour\b|\blabor\b|\bgiv(?:e|ing) birth\b|"
    r"\bthe birth\b|\bbirth\b|\bcontractions?\b|\bwaters\b|\bc-section\b|"
    r"\bc section\b|\bcaesarean\b|\bcesarean\b|\bepidural\b|\bpregnan\w*\b|"
    r"\bbaby\b|\bdelivery\b|\bhospital bag\b|\bmaternity bag\b|\bmaternity\b|"
    r"\b(?:first|second|third) stage\b|\bstage of (?:labour|labor|birth)\b|"
    r"\bpushing stage\b|\bhow long (?:is|does) pushing\b|\bplacenta\b", re.I)
_NOT_THE_BIRTH = (
    "car", "cars", "garage", "mot", "bill", "bills", "quote", "wage", "wages", "hourly",
    "party", "mp", "mps", "election", "vote", "voted", "government", "council", "worker",
    "workers", "job", "jobs", "engine", "clutch", "cambelt", "servicing", "price", "cost",
    "union", "manifesto", "poll", "brexit", "tax", "budget",
    "praevia", "previa",
)
_SECOND_BIRTH = re.compile(r"\bsecond\b|\bthird\b|\bfourth\b|\bnot my first\b|"
                           r"\banother baby\b|\b2nd\b|\b3rd\b|\bnot the first\b", re.I)
_AFTER_THE_BIRTH = re.compile(
    r"\bdriv(?:e|ing)\b|\bexercise\b|\bexercising\b|\bgym\b|\bswim(?:ming)?\b|"
    r"\bbath\b|\bbath(?:e|ing)\b|\bback to work\b|\bto work\b|\blift(?:ing)?\b|"
    r"\bsex\b|\bstitches\b|\bbleed(?:ing)?\b|\bperiod\b|\bwash my hair\b|"
    r"\balcohol\b|\bdrink\b|\brun(?:ning)?\b|\bwalk(?:ing)?\b|\bhoover\b|"
    r"\bhousework\b|\bpelvic floor\b|\bscar\b|\brecover\w*\b|\bheal\w*\b|"
    r"\bnumb\b|\bcontinence\b|\bpostnatal\b|\bpost natal\b", re.I)


def _the_line(understood):
    return " ".join(str((understood or {}).get("clean") or "").split())


def _asks_a_birth_time(understood):
    line = _the_line(understood)
    if not line or not _TIME_ASK.search(line) or not _BIRTH_WORD.search(line):
        return False
    if _AFTER_THE_BIRTH.search(line):
        return False
    words = set(re.findall(r"[a-z']+", line.lower()))
    return not words & set(_NOT_THE_BIRTH)


def _asks_about_the_bag(understood):
    line = _the_line(understood)
    if not line or not _TIME_ASK.search(line):
        return False
    if not re.search(r"\bpack\b|\bpacked\b|\bpacking\b", line, re.I):
        return False
    return bool(re.search(r"\bhospital\b|\bmaternity\b|\bbag for\b|\bdelivery\b", line,
                          re.I))


def _preg_labour_length(memory, understood):
    line = _the_line(understood)
    if re.search(r"\bin hospital\b|\bstay in\b|\bstay at\b|\bcome home\b|\bgoing home\b|"
                 r"\bhow long do i stay\b", line, re.I):
        return ("After a straightforward birth most women are home within a day: a few hours if "
                "everything is well and it is not your first, overnight or a day or two with a "
                "first baby. A caesarean is two to four days, and any concern about you or the "
                "baby adds a day, so plan for the longer end when you arrange a lift home.")
    if re.search(r"\bcontractions?\b", line, re.I) and not re.search(
            r"\blabour\b|\blabor\b|\bthe birth\b|\bgiv(?:e|ing) birth\b", line, re.I):
        return ("Each contraction usually lasts 30 to 60 seconds early on, then 60 to 90 seconds "
                "once labour is established, with a few minutes between them. They get longer, "
                "stronger and closer together as it goes on - that pattern is what tells you it "
                "is real labour rather than the practice tightenings. Ring the midwife if one "
                "lasts much longer than 90 seconds, or there is no gap between them.")
    if re.search(r"\blongest\b|\btoo long\b|\bstall(?:ed|ing)?\b|"
                 r"\bhow long can (?:a |the |my )?(?:labour|labor|it|this) (?:go|last|be)\b|"
                 r"\bgo on for\b", line, re.I):
        return ("There is no fixed limit: a first labour is usually under 18 hours once it is "
                "established, but slow is not the same as dangerous, and they go by how it is "
                "progressing, how you are and how the baby is rather than the clock. If it "
                "stalls they offer to break the waters or a hormone drip, and if it is not "
                "moving at all they talk to you about a caesarean. Ask what has changed each "
                "time they examine you.")
    if re.search(r"\b(?:first|second|third|1st|2nd|3rd) stage\b|\bpushing\b|"
                 r"\bplacenta (?:take|takes|come|comes|coming|out)\b|"
                 r"\bdelivery of the placenta\b|\bskin to skin\b", line, re.I):
        if re.search(r"\bfirst\b|\b1st\b", line, re.I):
            return ("The first stage is the long part: the cervix opening to 10cm, which takes "
                    "most of the 8 to 18 hours of a first labour and is much quicker with a "
                    "second. It starts with contractions you can talk through and ends with "
                    "strong ones a few minutes apart - that middle stretch, 4 to 6cm, is usually "
                    "the hardest, so ask for pain relief before you need it.")
        if re.search(r"\bthird\b|\b3rd\b|\bplacenta\b|\bskin to skin\b", line, re.I):
            return ("The third stage is the placenta: usually 5 to 15 minutes, and up to half an "
                    "hour if you wait for it to come away by itself rather than having the "
                    "injection that speeds it up. They check it is all out, and it is also when "
                    "any tear is stitched, so it can feel longer than it is.")
        return ("The second stage is the pushing: about an hour on average for a first baby, "
                "sometimes two, and often 10 or 20 minutes with a second or later one. The urge "
                "to push is hard to resist and that is normal - go with it, take the breaks "
                "between contractions, and expect the midwife to guide you to slow down at the "
                "end so you tear less.")
    if re.search(r"\bwaters?\b", line, re.I) and re.search(
            r"\bbreak|broke|broken|gone|went|went off\b", line, re.I):
        return ("Once your waters break, ring the midwife and go in to be checked - she will "
                "want to know the time, the colour and the smell. If labour has not started, "
                "most units offer to induce it within about 24 hours, because the risk of "
                "infection to you and the baby starts to rise after that. Do not use tampons or "
                "have sex once the waters have gone, and ring straight away if the water is "
                "green, brown or smelly, or if you feel unwell or the baby is not moving as "
                "usual.")
    if _SECOND_BIRTH.search(line):
        return ("A second or later labour is usually quicker than the first - often 5 to 12 hours "
                "from regular contractions to the birth, and some are much faster than that. "
                "Because it can move quickly, ring the midwife early rather than timing it at "
                "home, and go in when the contractions are strong and regular.")
    return ("A first labour usually takes 8 to 18 hours from the first regular contractions to the "
            "birth, and a second or later baby is usually quicker. Early labour at home can run "
            "much longer than that - a day or more of stop-start contractions is normal - so it "
            "is the pattern that matters: contractions getting stronger, longer and closer "
            "together, or your waters breaking, is the point to ring the midwife.")


def _preg_bag(memory, understood):
    line = _the_line(understood)
    when = ("Pack it by about 36 weeks - roughly a month before the due date - so it is ready if "
            "you go early. Two bags: yours with your maternity notes, a nightdress or two, big "
            "pads, toiletries, a phone charger and snacks; the baby's with nappies, vests, "
            "sleepsuits, a hat and a blanket. Keep it by the door, and add the notes last because "
            "you need them at appointments before then.")
    if re.search(r"\bwhat (?:should|do) i (?:pack|take|bring)\b|\bwhat to (?:pack|take|bring)\b|"
                 r"\bwhat goes in\b", line, re.I):
        return ("For you: maternity notes, a nightdress or two, big pads, toiletries, a phone "
                "charger and snacks. For the baby: nappies, vests, sleepsuits, a hat and a "
                "blanket. Pack it by about 36 weeks so it is ready if you go early, keep it by "
                "the door, and leave the notes on top because you need them at appointments "
                "before then.")
    return when



_PREG_SAID = re.compile(
    r"\b(?:pregnan\w*|expecting a baby|expecting our baby|with child|trimester|"
    r"\d\d? weeks (?:pregnant|gone))\b")
_PREG_DENIED = re.compile(
    r"\b(?:not|isn't|isnt|aren't|arent|no longer|stopped being|never)\s+(?:pregnan\w*)")


HEAD_PREGNANCY_REPLY = (
    "Paracetamol is the one to take for a headache in pregnancy, at the lowest dose that works "
    "and for the shortest time - not ibuprofen or aspirin unless a doctor or midwife has told "
    "you to. Water, food and sleep do a lot, and a skipped meal, dehydration and caffeine "
    "withdrawal are the usual causes. Mention headaches that keep coming back to your midwife, "
    "and go in the same day if a bad headache comes with blurred vision or flashing lights, pain "
    "under the ribs, swelling of the face or hands, or vomiting after 20 weeks: that combination "
    "is the one that has to be checked for pre-eclampsia.")


def _said_pregnant(understood):
    said = " ".join(str((understood or {}).get(key) or "")
                    for key in ("clean", "text", "norm_text")).lower()
    if _PREG_DENIED.search(said):
        return False
    return bool(_PREG_SAID.search(said))



ENTRIES = [
    entry("preg-soft-cheese",
          (("brie", "camembert", "soft cheese", "soft cheeses", "blue cheese", "stilton",
            "gorgonzola", "roquefort", "chevre", "goats cheese", "mould ripened", "mold ripened",
            "mexicana", "mould ripened cheese", "mold ripened cheese", "baked camembert"),
           PREGNANT),
          "Skip it unless it is cooked until steaming hot: brie, camembert, soft blue cheeses and "
          "any mould-ripened cheese can carry listeria, and listeria can reach the baby. Baked "
          "camembert or brie in a hot dish is fine because the heat kills it. Hard cheese is a "
          "different story - cheddar, parmesan, and the tubs of cream cheese, cottage cheese and "
          "mozzarella are all fine, because they are made with pasteurised milk.",
          ask=("can i", "is it", "ok", "safe", "eat", "avoid", "should", "what about"),
          bias=2, avoid=NOT_FOOD),
    entry("preg-cheese-list",
          (("cheese", "cheeses", "dairy"),
           PREGNANT),
          "Hard cheese is all fine - cheddar, parmesan, gruyere - and so are feta, halloumi, "
          "mozzarella, cottage cheese and cream cheese, because they are made with pasteurised "
          "milk. The ones to cook until steaming or leave alone are the mould-ripened and blue "
          "ones: brie, camembert, stilton, gorgonzola, and any soft cheese with a rind. Skip "
          "anything labelled unpasteurised.",
          ask=("which", "what", "can i", "is it", "safe", "ok", "avoid", "eat", "list"),
          bias=2, avoid=NOT_FOOD),
    entry("preg-feta-halloumi",
          (("feta", "halloumi", "goats cheese", "goat cheese", "cottage cheese", "cream cheese",
            "mozzarella", "cheddar", "parmesan", "hard cheese", "paneer"),
           PREGNANT),
          "Fine, and this is where people cut out more than they need to: feta, halloumi, "
          "mozzarella, cottage cheese, cream cheese and all the hard cheeses - cheddar, parmesan, "
          "paneer - are made with pasteurised milk, and listeria is the only reason soft cheese "
          "is a worry. Check the label says pasteurised if it is a farm shop one; the "
          "supermarket tubs always are.",
          ask=("can i", "is it", "ok", "safe", "eat", "avoid", "have"),
          bias=2, avoid=NOT_FOOD),
    entry("preg-raw-milk",
          (("unpasteurised", "unpasteurized", "raw milk", "raw cheese", "farmhouse cheese",
            "goats milk", "sheeps milk", "raw dairy"),
           PREGNANT),
          "No: anything made with unpasteurised milk can carry listeria and campylobacter, so "
          "leave the raw-milk cheese and the milk straight from the farm. Pasteurised milk and "
          "cheese are fine, and most goat and sheep cheese sold in supermarkets is pasteurised - "
          "the label will say so.",
          ask=("can i", "is it", "ok", "safe", "eat", "avoid", "drink"),
          bias=2, avoid=NOT_FOOD),
    entry("preg-pate-liver",
          (("pate", "pates", "liver", "liver sausage", "liver pate", "chicken liver", "foie gras",
            "haggis", "liver and onions", "cod liver oil", "vitamin a"),
           PREGNANT),
          "No pate and no liver, and that includes vegetable pate: liver is so high in vitamin A "
          "that too much of it can harm the baby, and pate can carry listeria. The same goes for "
          "cod liver oil and any multivitamin with vitamin A in it - take folic acid and vitamin "
          "D instead, and ask the midwife about anything else.",
          ask=("can i", "is it", "ok", "safe", "eat", "avoid", "take"),
          bias=2, avoid=NOT_FOOD),
    entry("preg-raw-meat",
          (("rare", "raw meat", "undercooked", "pink", "medium rare", "steak", "salami",
            "chorizo", "prosciutto", "parma ham", "salami", "pepperoni", "cured meat",
            "cured meats", "sausage", "sausages", "hot dog", "hot dogs", "beef", "lamb", "pork",
            "chicken", "turkey", "mince", "burgers", "meat"),
           PREGNANT),
          "Cook meat right through: no rare steak, no pink lamb, and nothing raw or cured unless "
          "it is cooked into a hot dish. The worry is toxoplasmosis, which is in raw meat, and "
          "salami, chorizo, Parma ham and prosciutto are cured rather than cooked. Well-done "
          "steak, cooked chicken, ham from the deli counter and hot dogs heated until steaming "
          "are all fine.",
          ask=("can i", "is it", "ok", "safe", "eat", "avoid", "have"),
          bias=2, avoid=NOT_FOOD),
    entry("preg-raw-fish",
          (("sushi", "sashimi", "raw fish", "raw salmon", "smoked salmon", "gravadlax",
            "oysters", "oyster", "raw prawns", "shellfish", "mussels", "prawns", "fish",
            "salmon", "cod", "ceviche", "anchovies", "sardines", "mackerel", "sashimi"),
           PREGNANT),
          "Yes, with one rule. Raw is the part to skip: cooked prawns, mussels that have opened "
          "in the pan, tinned tuna and smoked salmon are all fine in the UK, and so is sushi made "
          "with cooked or frozen fish. What to leave alone is raw fish and raw shellfish - no "
          "oysters, no raw prawns - because of listeria and norovirus. Cooked fish is good for "
          "you and the baby too: salmon, mackerel and sardines are the ones to have, twice a week.",
          ask=("can i", "is it", "ok", "safe", "eat", "avoid", "have"),
          bias=2, avoid=NOT_FOOD),
    entry("preg-big-fish",
          (("swordfish", "shark", "marlin", "tuna", "tinned tuna", "tuna steak", "oily fish",
            "mercury"),
           PREGNANT),
          "Skip swordfish, shark and marlin completely, and keep tuna to two fresh steaks or four "
          "medium tins a week: those three are the fish with the most mercury, and tuna is the one "
          "people eat most of. Oily fish like salmon, mackerel and sardines is good for the baby's "
          "brain - two portions a week, and no more than one of them tuna.",
          ask=("can i", "is it", "ok", "safe", "eat", "avoid", "how much", "how many"),
          bias=2, avoid=NOT_FOOD),
    entry("preg-peanuts",
          (("peanuts", "peanut", "nuts", "nut", "almonds", "peanut butter", "tree nuts"),
           PREGNANT),
          "Peanuts and nuts are fine in pregnancy, and avoiding them does not prevent an allergy - "
          "the old advice to cut them out has been dropped. The exception is if you are allergic "
          "yourself, or the midwife or GP has told you to avoid them. Nuts are a good snack: a "
          "handful with an apple beats a biscuit at three in the afternoon.",
          ask=("can i", "is it", "ok", "safe", "eat", "avoid", "have"),
          bias=2, avoid=NOT_FOOD),
    entry("preg-herbal",
          (("herbal tea", "herbal teas", "green tea", "fennel", "liquorice", "raspberry leaf",
            "camomile", "chamomile", "peppermint tea"),
           PREGNANT),
          "Keep herbal teas to a couple of cups a day and don't treat any of them as medicine: "
          "liquorice is the one to avoid (it can raise blood pressure), and raspberry leaf is "
          "usually left until the last weeks and only with the midwife's agreement. Ordinary tea, "
          "decaf tea and water are the easy answers.",
          ask=("can i", "is it", "ok", "safe", "drink", "have"),
          bias=2, avoid=NOT_FOOD),
    entry("preg-listeria",
          (("listeria", "listeriosis", "food poisoning", "food hygiene", "toxoplasmosis"),
           PREGNANT),
          "Listeria is a bug that is rare but dangerous in pregnancy because it can cross to the "
          "baby, and it grows in food kept cold rather than in food left out - soft cheese, pate, "
          "smoked fish and cooked meats from a deli are the usual culprits. That is why the advice "
          "is to heat leftovers until steaming, wash the veg, and skip those foods. It usually "
          "shows as a mild flu-like illness, so mention any fever to the midwife.",
          ask=("is", "what", "can i", "should", "worried", "dangerous", "risk", "how"),
          bias=2, avoid=NOT_FOOD),
    entry("preg-what-can-i-eat",
          (("eat", "eating", "food", "foods", "diet", "avoid", "anything", "menu"),
           PREGNANT),
          LIST,
          ask=("what can i eat", "what can't i eat", "what cant i eat", "what can i not eat",
               "what should i avoid", "what to avoid", "what foods", "which foods",
               "what shouldn't i eat", "what is off limits", "can i eat", "avoid",
               "anything i shouldn't",
               "what should i eat", "what should i be eating", "what to eat", "what do i eat",
               "what not to eat", "what i shouldn't eat", "what i shouldnt eat",
               "shouldn't eat", "shouldnt eat", "shouldn't i eat", "shouldnt i eat",
               "not eat", "not to eat", "can't i eat", "cant i eat", "avoid eating",
               "what's safe to eat", "whats safe to eat", "safe to eat"),
          avoid=NOT_FOOD),
    entry("preg-hot-bath",
          (("hot bath", "bath", "baths", "bathwater", "hot tub", "jacuzzi", "sauna", "steam room",
            "spa", "warm bath"),
           PREGNANT),
          "Warm is fine, hot is the part to avoid: keep the water comfortable rather than "
          "steaming, and get out if you feel light-headed. Hot tubs, saunas and steam rooms are "
          "best skipped for the first 12 weeks, because raising your core temperature early on "
          "has been linked to problems with the baby's spine. A warm bath, a shower and a swim "
          "are all fine right through.",
          ask=("safe", "ok", "okay", "fine", "allowed", "can i", "should i", "is it", "is a",
               "how hot", "how warm"),
          bias=2,
          avoid=NOT_FOOD + ("baby", "babies", "newborn", "toddler", "child", "clean the",
                            "cleaning", "limescale", "mould", "drain")),
    entry("preg-flying",
          (("fly", "flying", "flight", "flights", "plane", "airplane", "aeroplane", "air travel",
            "long haul", "long-haul", "holiday abroad",
            "travel", "travelling", "traveling", "a trip", "trip abroad", "go abroad",
            "going abroad", "flying abroad",
            "holiday", "holidays", "on holiday", "vacation", "a break abroad"),
           PREGNANT),
          "Flying is usually fine: most airlines take you up to 36 weeks for one baby, and 32 "
          "weeks for twins, and some ask for a letter from the midwife from 28 weeks, so check "
          "your airline before you book. Drink water, get up and walk every hour or so and wear "
          "compression socks on a long flight. Ask the midwife first if you have had bleeding, "
          "high blood pressure, pre-eclampsia or twins.",
          ask=("safe", "ok", "okay", "fine", "allowed", "can i", "should i", "is it", "when can i",
               "how late", "how far", "abroad",
               "can you", "can we", "could i", "is it ok to", "still ok", "still fine"),
          bias=2,
          avoid=tuple(w for w in NOT_FOOD if w not in ("fly", "flying", "flight", "travel")) + (
              "cheap", "cheaper", "cheapest", "book a flight", "price", "fare", "delayed",
              "cancelled", "luggage", "legroom", "jet lag")),
    entry("preg-hair-dye",
          (("hair dye", "dye my hair", "dye your hair", "dyeing my hair", "colour my hair",
            "color my hair", "hair colour", "hair color", "highlights", "bleach my hair",
            "hair treatment", "salon"),
           PREGNANT + ("breastfeeding", "breastfeed", "breast feeding", "nursing")),
          _preg_hair_dye,
          ask=("safe", "ok", "okay", "fine", "allowed", "can i", "should i", "is it", "when can i",
               "still"),
          bias=2,
          avoid=tuple(w for w in NOT_FOOD if w not in ("breastfeeding", "breastfeed", "nursing")) + (
              "cut", "cuts", "trim", "hairdresser", "fringe", "grey", "thinning", "hair loss",
              "hair falling", "shampoo", "conditioner", "dandruff")),

    entry("preg-exercise",
          (PREGNANT_MOVEMENT, PREGNANT),
          "Keep doing what you already do, at a pace where you can still hold a conversation: "
          "150 minutes a week of walking, swimming, yoga, pilates or light weights is what the "
          "guidance recommends, and it is good for you and the baby. Leave out contact sports "
          "and anything with a fall risk such as riding, skiing or cycling on the road, and in a "
          "class do not lie flat on your back after 16 weeks. Stop and ring your midwife if you "
          "bleed, leak fluid, feel dizzy or very breathless, and ask her first if you have a "
          "condition or were not active before.",
          ask=("safe", "ok", "okay", "fine", "allowed", "can i", "should i", "is it", "still",
               "while", "when", "how much", "how often", "how long", "continue", "keep"),
          bias=2,
          avoid=("bring on labour", "bring on labor", "start labour", "start labor", "induce",
                 "kick start", "weight gain", "how much weight", "put on", "gained",
                 "back pain", "backache", "pelvic", "sciatica", "cramp", "sick", "nausea",
                 "bleeding", "bleed", "discharge", "waters", "contractions")),

    entry("preg-headache",
          (("headache", "headaches", "migraine", "migraines", "head ache", "head aches",
            "my head hurts", "my head is banging", "head is pounding", "head pounding",
            "splitting headache", "bad head"),
           ("pregnant", "pregnancy", "expecting a baby", "expecting our baby", "trimester",
            "weeks pregnant", "weeks gone", "safe", "ok", "okay", "can i", "could i", "is it",
            "while pregnant", "in pregnancy", "take")),
          HEAD_PREGNANCY_REPLY,
          bias=2,
          guard=_said_pregnant,
          avoid=("folic acid", "vitamin", "supplement", "scan", "scans", "midwife appointment",
                 "bp", "blood pressure", "glucose test", "sugar test", "kick", "kicks",
                 "movement", "movements", "bleeding", "bleed", "spotting", "waters",
                 "contractions", "swollen feet", "swollen ankles", "sickness", "nausea",
                 "vomiting", "heartburn", "constipation", "piles", "stretch marks", "sleep",
                 "travel", "flight", "flying", "food", "eat", "eating", "diet", "sex",
                 "exercise", "gym", "swim", "nursery", "pram", "cot", "nappy", "nappies")),

    entry("preg-any-food",
          (tuple(name for names, _ in PREG_WORRY_FOODS for name in names) +
           ("safe", "safely", "ok", "okay", "fine", "allowed", "allow", "bad", "harm", "harmful",
            "danger", "dangerous", "risky", "risk",
            "drink", "drinks", "drinking", "juice", "squash", "squashes", "smoothie"),
           PREGNANT),
          _preg_food,
          ask=("safe", "ok", "okay", "fine", "allowed", "allow", "bad", "harm", "harmful",
               "danger", "dangerous", "risky", "risk", "can i", "should i", "is it", "are they",
               "is", "are"),
          bias=1,
          avoid=NOT_FOOD + PREGNANT_MOVEMENT + (
              "bath", "baths", "sauna", "jacuzzi", "hot tub", "steam room", "hair dye", "dye",
              "dying my hair", "highlights", "hair colour", "hair color", "nails", "massage",
              "tattoo", "tattoos", "fake tan", "sunbed", "sunbathing", "cat litter", "litter",
              "cleaning products", "bleach", "paint", "x-ray", "xray", "dentist", "dental",
              "white spirit", "turps", "turpentine", "paint thinner", "thinner", "varnish",
              "wood stain", "primer", "gloss paint", "spray paint", "aerosol", "adhesive",
              "wood glue", "superglue", "solvent", "solvents", "fumes", "fumigate",
              "weedkiller", "weed killer", "glyphosate", "pesticide", "insecticide",
              "antifreeze", "oven cleaner", "drain cleaner", "descaler", "disinfectant",
              "ammonia", "mould spray", "ant powder", "slug pellets", "rat poison", "rodenticide",
              "flea treatment", "flea bomb", "creosote", "wood preserver", "decking oil",
              "paint stripper", "nitromors", "caustic", "swimming pool chemicals",
              "jab", "jabs", "jabbed", "booster jab", "booster", "vaccination", "immunisation",
              "immunization", "covid jab", "flu jab", "covid vaccine", "flu vaccine",
              "what can i eat", "what cant i eat", "what can't i eat", "what can i not eat",
              "what should i avoid", "what to avoid", "what foods", "which foods", "diet",
              "menu", "foods to avoid", "eat when pregnant", "eat while pregnant") +
              DRINKS_WITH_THEIR_OWN_ANSWER +
              ("milk", "a pint of milk", "dairy", "milkshake", "milkshakes", "hot chocolate")),

    entry("preg-milk",
          (("milk", "a pint of milk", "dairy", "milkshake", "milkshakes", "hot chocolate"),
           ("pregnant", "pregnancy", "expecting", "drink", "drinking", "is it", "safe", "ok",
            "okay", "fine", "can i", "should i", "much")),
          "Pasteurised milk is fine, and worth drinking: about three servings of dairy a day "
          "covers the calcium and iodine a baby needs. The one to skip is unpasteurised milk and "
          "anything made with it - some farm-shop milk, and raw-milk cheese - because of "
          "listeria. If milk turns your stomach early on, yoghurt, cheese and a fortified plant "
          "milk cover the same ground.",
          avoid=("breastfeeding", "nursing", "formula", "weaning", "my baby", "a baby",
                 "the baby", "baby have", "baby need", "how much milk", "ounces", "oz",
                 "expressing", "colic", "reflux", "allergy", "allergic", "lactose",
                 "cows milk protein", "cheese", "brie", "camembert", "feta", "stilton",
                 "yoghurt", "yogurt", "ice cream", "goat", "soya", "oat milk", "almond milk",
                 "freeze", "freezes", "freezing", "frozen", "freezer", "thaw", "thawed",
                 "defrost", "defrosted", "use by", "out of date", "gone off", "goes off",
                 "how long does milk", "how long can i keep", "storage"),
          guard=_said_pregnant),

    entry("preg-am-i",
          (("pregnant", "pregnancy"), AM_I + TEST_WORDS + WHEN),
          TEST_REPLY, bias=2,
          avoid=tuple(w for w in NOT_FOOD if w not in ("test", "tests")) + NOT_A_TEST +
                PREGNANT_ALREADY + FERTILITY +
                ("how many weeks", "weeks pregnant", "weeks am i", "due date", "trimester",
                 "maternity", "birth control", "contraception", "condom", "morning after",
                 "test was negative", "test is negative", "test was positive",
                 "test is positive", "tests were negative", "tests are negative")),
    entry("preg-two-lines",
          (("two lines", "both lines"), ("mean", "means", "meant", "pregnant", "pregnancy",
                                         "test", "tests", "positive", "got", "have", "see",
                                         "showing", "shows")),
          POSITIVE_REPLY,
          avoid=NOT_A_TEST + ("negative", "not pregnant")),
    entry("preg-test-positive",
          (("positive", "two lines", "both lines", "faint line", "faint", "it says",
            "says positive"),
           TEST_WORDS),
          POSITIVE_REPLY,
          ask=("what", "should", "do i", "is", "does", "test", "result", "now", "next", "so"),
          bias=2, avoid=NOT_A_TEST + ("negative", "not pregnant")),
    entry("preg-test-negative",
          (("negative", "not pregnant", "one line", "no line", "no lines", "nothing there"),
           TEST_WORDS),
          NEGATIVE_REPLY,
          ask=("what", "should", "do i", "is", "does", "test", "result", "now", "next", "so",
               "can i", "how"),
          bias=2, avoid=NOT_A_TEST + ("positive",)),
    entry("preg-late-period",
          (WHEN, ("late", "missed", "days", "weeks", "hasnt", "not come", "where", "why",
                  "when", "worry", "normal", "pregnant", "pregnancy", "test")),
          LATE_REPLY,
          ask=("my period", "period", "late", "missed", "why", "when", "should", "is it",
               "how long", "what"),
          guard=_a_late_that_is_not_a_period,
          avoid=("period pain", "period pains", "cramps", "heavy period", "period pads",
                 "menopause", "hot flushes", "contraception", "condom", "morning after",
                 "early", "days early", "week early", "weeks early", "sooner", "shorter",
                 "driving test", "theory test", "theory", "mot", "exam", "exams",
                 "missed my test", "missed the test", "missed a test", "interview",
                 "deadline", "payment", "train", "bus", "flight",
                 "due date", "weeks pregnant", "weeks am i", "trimester", "maternity",
                 "due back", "due to be", "back at work", "back to work", "refund",
                 "tax return", "parcel", "library", "renewal", "invoice",
                 "normal", "how long", "how often", "how many days", "days between",
                 "lasts", "started", "when do periods", "first period", "heavy", "light",
                 "boss", "manager", "rota", "my job", "work late", "working late", "work every",
                 "overtime", "be paid for", "paid for it", "get paid", "wages", "salary",
                 "hourly", "hours i work", "for the hours"
                 ) + FERTILITY),
    entry("preg-cycle-normal",
          (("period", "periods", "cycle", "cycles"),
           CYCLE_SHAPE + ("how often", "typical", "average", "length", "between")),
          CYCLE_REPLY, bias=1,
          guard=_a_late_that_is_not_a_period,
          avoid=NOT_A_TEST + NOT_FOOD +
                ("heavy", "light", "late", "missed", "pregnant", "pregnancy", "test",
                 "tests", "period pain", "cramps",
                 "tank", "tanks", "aquarium", "fish tank", "nitrogen cycle", "ammonia",
                 "nitrite", "nitrate",
                 "probation", "probationary", "on probation", "trial period", "trial shift",
                 "contract", "contracts", "employment", "employer", "job offer", "new job",
                 "at work", "sentence", "court", "parole",
                 "dishwasher", "dishwashers", "washing machine", "washer", "washer dryer",
                 "tumble dryer", "dryer", "spin cycle", "wash cycle",
                 "bike", "bikes", "bicycle", "bicycles", "cycle to work",
                 "cycling to work", "learn to cycle", "learning to cycle",
                 "pedal", "pedals", "pedalling", "saddle", "ride a bike", "riding a bike",
                 "learn to ride",
                 "wash", "washing", "washed", "laundry", "programme", "program", "quick wash",
                 "eco",
                 "cycle ride", "cycle lane", "cycle path", "cycle route")),

    entry("preg-pms-days",
          (("pms", "pmt", "premenstrual", "pre menstrual", "pre-menstrual"),
           ("how many days", "how long", "when", "before", "last", "lasts", "start", "starts",
            "days", "week", "weeks", "early")),
          "Premenstrual symptoms usually start a week or two before a period and are at their "
          "worst in the five days before it, then ease within a day or two of bleeding starting. "
          "Track them for two or three cycles - the pattern is what tells you it is the cycle and "
          "not the week. If it is bad enough to wreck two weeks in four, or the mood change is "
          "severe, that is worth the GP: PMDD is real and treatable.",
          bias=1,
          avoid=NOT_FOOD + NOT_A_TEST + ("pregnant", "pregnancy", "test", "tests", "missed",
                                         "late", "period pain", "cramps")),

    entry("preg-early-period",
          (("period", "periods", "cycle"), ("early", "days early", "week early", "weeks early",
                                            "sooner", "shorter", "before i expected",
                                            "earlier than usual", "two weeks early")),
          EARLY_REPLY, bias=1,
          avoid=NOT_FOOD + NOT_A_TEST + ("late", "missed", "period pain", "cramps", "heavy")),

    entry("preg-due-date",
          (("due date", "due date is", "when am i due", "when is my due", "whens my due",
            "when's my due", "baby due", "when is the baby due", "how far along",
            "weeks pregnant am i", "weeks am i", "how many weeks pregnant",
            "how pregnant am i", "how many weeks am i", "pregnancy weeks",
            "when will the baby", "when will my baby", "when is the baby born",
            "how long left of my pregnancy", "how many weeks left of my pregnancy",
            "weeks pregnant", "how many wks am i", "how many weeks along",
            "how many weeks into", "how many weeks gone", "what week am i",
            "which week am i",
            "how many weeks is a pregnancy", "how long is a pregnancy",
            "when are you due", "when is she due", "when is he due", "baby is due",
            "last period", "lmp", "first day of my last period", "period started",
            "my period started", "how many months"),
           ("when", "what", "how many", "how far", "date", "weeks", "days", "am i",
            "due", "work out", "worked out", "calculate", "count", "left", "born",
            "is it", "will it", "how long")),
          _preg_due_date, bias=4,
          ask=("when", "whens", "how many", "how far", "how long", "which date", "what date",
               "due date", "weeks", "week", "months", "calculate", "worked out", "left",
               "am i", "is", "are", "will",
               "last period", "first day", "period started", "lmp"),
          shape=(_gives_a_month,),
          guard=_asks_when_due,
          avoid=NOT_FOOD + NOT_A_TEST + (
              "am i pregnant", "could i be pregnant", "test was", "test is", "two lines",
              "one line", "negative", "positive", "missed period", "late period",
              "period late", "contraction", "contractions", "induction", "c section",
              "c-section", "epidural", "maternity pay", "maternity leave", "paternity",
              "birth certificate", "names", "name", "nursery", "cot",
              "rent", "bill", "bills", "payment", "pay", "invoice", "loan",
              "library", "essay", "assignment", "coursework", "homework",
              "deadline", "tax", "mot", "insurance", "subscription")),

    entry("preg-labour-length",
          (("labour", "labor", "birth", "give birth", "in labour", "contractions", "waters",
            "first stage", "second stage", "third stage", "pushing", "pushing stage", "placenta",
            "stage of labour"),
           ("how long", "how many hours", "hours", "long", "longer", "shorter", "quicker",
            "faster", "slow", "take", "last", "how soon", "longest", "too long", "stalled",
            "stalling", "go on")),
          _preg_labour_length, bias=1,
          guard=_asks_a_birth_time, avoid=_NOT_THE_BIRTH),
    entry("preg-hospital-bag",
          (("hospital bag", "hospital bags", "maternity bag", "bag for hospital",
            "bag for the hospital", "bags for hospital", "hospital"),
           ("pack", "packed", "packing", "when", "what to take", "what to bring")),
          _preg_bag, bias=2,
          guard=_asks_about_the_bag,
          avoid=("bin", "bin bag", "tea", "teabag", "teabags", "shopping", "dog", "school",
                 "rucksack", "backpack", "handbag", "luggage", "suitcase", "sleeping bag")),
]

_BIRTH_WORDS = (
    (("c section", "c-section", "caesarean", "caesarian", "cesarean", "cesarian",
      "caesarean section", "cesarean section"),
     "A caesarean is the baby delivered through a cut in the tummy and womb, usually because "
     "labour is not progressing, the baby is breech or either of you is unwell. It is a major "
     "operation: about 45 minutes, a spinal so you are awake, and roughly four to six weeks of "
     "careful lifting afterwards. An emergency one is done for a reason found in labour, not "
     "because anything went wrong on your part."),
    (("doula", "doulas"),
     "A doula is a person who supports you through pregnancy, birth and the first weeks - "
     "practical help and someone who stays with you - but she is not a midwife and does no "
     "clinical care. Doulas are hired privately, usually GBP 300 to 800, and there are free "
     "volunteer doulas in many areas; ask what she does at a hospital birth, as some trusts "
     "limit how many people are in the room."),
    (("midwife", "midwives"),
     "A midwife is the trained professional who looks after a straightforward pregnancy, birth "
     "and the first weeks, and she is who you see at the antenatal appointments. She is a nurse "
     "or a direct-entry midwife with a degree, and she can order scans and blood tests, deliver "
     "the baby and stitch a tear. A doctor takes over only if something needs one."),
    (("epidural", "epidurals"),
     "An epidural is pain relief given through a fine tube in the back, numbing from the waist "
     "down while you stay awake. It takes about 20 minutes to set up and 15 to 20 to work, and "
     "it can make your legs heavy and slow labour, so it is usually offered once labour is "
     "established. You can still push with one; ask early if you want one, because it needs an "
     "anaesthetist."),
    (("birth plan", "birth plans"),
     "A birth plan is a page saying what you would prefer - who is with you, how you want pain "
     "relief, water, feeding, and what to do if things change - written so a midwife can read it "
     "in a minute. Keep it to one side of A4 and put your first two wishes at the top: the plan "
     "that helps is a short list of preferences, not a script, because birth often goes its own "
     "way."),
    (("induced", "induction", "inductions", "being induced", "induced labour"),
     "Induction is starting labour with medicine or a balloon instead of waiting for it to start "
     "itself, usually offered if you go past about 41 weeks or there is a reason the baby is "
     "better out. It is a prostaglandin tablet or gel first, then a drip if needed, and it can "
     "take two or three days from the first dose to the baby. You can ask what the reason is and "
     "what happens if you wait."),
    (("water birth", "water births", "birthing pool", "birth pool"),
     "A water birth is labouring, and sometimes delivering, in a deep pool of warm water, which "
     "takes the weight off and often eases the pain of contractions. Many birth centres and some "
     "labour wards have pools; ask early, as there may be one and it may be taken. You can get "
     "out at any point, and being in water is not offered if there are complications."),
    (("colostrum", "colostrum harvesting"),
     "Colostrum is the first milk: thick, yellow and made in small amounts in the last weeks and "
     "the first days, and it is all a newborn needs - a teaspoon at a time, full of antibodies. "
     "It acts as a laxative that clears the meconium, which is why the first dirty nappies come. "
     "Hand expressing a little into a syringe before the birth is worth asking about if your "
     "baby may need extra."),
    (("membrane sweep", "stretch and sweep", "sweep", "sweeps"),
     "A membrane sweep is a midwife's gloved finger passing over the cervix to separate the "
     "membranes, which releases hormones and can start labour - offered from about 40 weeks if "
     "you are keen to avoid induction. It takes a minute, feels like a smear test and a period "
     "cramp, and works for roughly one in eight. You can say no and ask again in a week."),
    (("ventouse", "ventouse delivery", "vacuum delivery", "vacuum extraction"),
     "A ventouse is a soft cup on the baby's head that a doctor pulls with, to help in the last "
     "stage when pushing is not moving the baby or either of you is tiring. It leaves a bruise "
     "and a cone-shaped head that settles in a few days. Forceps do the same job with metal "
     "tongs; the doctor will explain which they want and why."),
    (("episiotomy", "episiotomies"),
     "An episiotomy is a small cut made at the bottom of the vagina during birth to make room, "
     "done with local anaesthetic when the baby needs to come quickly or the tissue is about to "
     "tear badly. It is stitched and heals in two to three weeks, and it is not routine - a tear "
     "that happens on its own is often smaller and heals better, so not every birth needs one."),
    (("nicu", "scbu", "special care baby unit", "neonatal unit"),
     "NICU is the neonatal intensive care unit, and SCBU the special care baby unit - where a "
     "baby goes if they are early, small or need help breathing or feeding. You can visit almost "
     "all the time, ask to do the nappy changes and feeds, and ask the nurse to explain every "
     "tube and number: babies on these units are usually there for warmth, feeding and time."),
    (("labour", "in labour", "going into labour"),
     "Labour is the womb contracting to open the cervix and push the baby out: for a first baby "
     "it usually takes 8 to 18 hours from regular contractions, and it comes in three stages - "
     "the cervix opening to 10 cm, the pushing, and the placenta. Call the midwife when "
     "contractions are regular, getting longer and stronger, about every five minutes."),
    (("placenta", "the afterbirth", "afterbirth"),
     "The placenta is the organ on the womb wall that feeds the baby through the cord, and it "
     "comes out as the third stage of labour, usually within 15 to 30 minutes of the birth. You "
     "can have an injection to speed that up or wait for it to happen on its own. It is checked "
     "whole afterwards, which is the one reason to look at it if you want to."),
    (("birth centre", "birth centres", "midwife led unit", "midwifery led unit"),
     "A birth centre is a midwife-led unit for a straightforward birth - a room with a pool, "
     "your own space, no doctors on site and usually a shorter stay, so it suits a pregnancy "
     "with no complications. If something needs a doctor you are transferred to the labour ward, "
     "which is usually minutes away. Ask for a look round at about 30 weeks."),
    (("home birth", "home births", "birth at home"),
     "A home birth means two midwives come to you, with gas and air and a pool if you have one, "
     "and you are transferred to hospital by ambulance if it is needed. It is offered for a "
     "straightforward second or later pregnancy, and it is your choice to ask for it - about 2 "
     "in 100 births in the UK happen at home."),
    (("perineal tear", "tear", "tears", "second degree tear", "third degree tear", "a tear"),
     "A tear is the skin at the bottom of the vagina stretching and splitting as the baby comes: "
     "most are small, most need a few stitches with local anaesthetic, and they heal in two to "
     "three weeks. A third or fourth degree tear reaches the muscle and the back passage and is "
     "repaired in theatre. Tell your midwife about the pain rather than sitting on it."),
    (("lochia", "postnatal bleeding", "bleeding after birth"),
     "Lochia is the bleeding after birth: heavy red blood for three to five days, then browner "
     "and lighter for up to six weeks. Use pads rather than tampons, and get help the same day "
     "if you soak a pad in an hour, pass clots bigger than a 50p coin, or the blood smells bad "
     "or you feel feverish - that is a sign to have checked."),
    (("heel prick test", "newborn blood spot", "blood spot test", "heel prick"),
     "The heel prick test is the newborn blood spot test, done at five days old: a few drops of "
     "blood from the heel onto a card, checked for nine rare conditions including cystic "
     "fibrosis, sickle cell and an underactive thyroid. It takes a minute and the baby cries "
     "briefly. It is offered to every baby and you can ask what each result means."),
    (("mucus plug", "bloody show", "show in pregnancy", "a show in pregnancy", "show"),
     "The mucus plug is the plug of mucus that seals the cervix, and it comes away as a thick "
     "jelly, sometimes streaked with blood - the \'show\'. It can be days or a fortnight before "
     "labour and means nothing on its own; call the midwife if the blood is more than a streak "
     "or comes with regular contractions."),
    (("nuchal scan", "nuchal translucency", "dating scan", "20 week scan", "anomaly scan"),
     "A nuchal scan is the 12-week scan: it measures the fluid at the back of the baby's neck "
     "and, with a blood test, gives a risk figure for Down's, Edwards' and Patau's syndromes - "
     "a screening test, not a diagnosis. The 20-week scan checks how the baby is growing and "
     "developing. Both are offered, and you can decline or ask for time to think."),
    (("skin to skin", "skin to skin contact", "kangaroo care"),
     "Skin to skin is the naked baby laid on your bare chest, covered with a blanket, in the "
     "first hour and as often as you like after. It keeps them warm, steadies their breathing "
     "and blood sugar, and is the strongest start to feeding - and it works just as well for a "
     "dad or a partner, which is useful when the mother needs stitching or a rest."),
    (("forceps", "forceps delivery", "kiwi cup"),
     "Forceps are the metal tongs a doctor uses to guide the baby out in the last stage, when "
     "pushing is not moving them or one of you is tiring. They leave marks on the head that fade "
     "in a few days, and you are given pain relief first. They are used in about one birth in "
     "fourteen, and a ventouse is the alternative when a cup is enough."),
    (("tongue tie", "tongue-tie", "tongue tied", "tongue-tied"),
     "A tongue tie is the strip of tissue under the tongue being tight or short, so the tongue "
     "cannot lift or reach forward as far as it should - which can make feeding sore and slow. It "
     "is common, it is checked at the newborn examination, and a simple snip in the first weeks "
     "is quick and needs no anaesthetic. Ask a midwife or health visitor to look if feeding "
     "hurts."),
    (("gestational diabetes", "gestational diabetes test", "glucose tolerance test"),
     "Gestational diabetes is high blood sugar that starts in pregnancy, from the placenta's "
     "hormones making insulin work less well - it is tested for with a glucose drink and blood "
     "tests at 24 to 28 weeks if you are at risk. It is managed with diet, monitoring and "
     "sometimes tablets or insulin, and it usually goes after the birth. Nothing you did caused "
     "it."),
)
_BIRTH_WORD_KEY = tuple(word for words, _ in _BIRTH_WORDS for word in words)
_BIRTH_WORD_NAMES = tuple(sorted(((word, reply) for words, reply in _BIRTH_WORDS
                                  for word in words), key=lambda pair: len(pair[0]),
                                 reverse=True))
_BIRTH_ASK = ("what is", "whats", "what's", "what are", "mean", "means", "meaning", "explain",
              "definition", "define", "stand for", "difference", "what does",
              "what happens", "what happens during", "what happens at", "what happens in",
              "what goes on", "what goes on during", "whats it like", "what is it like")


_AMBIGUOUS = frozenset(("section", "show", "a show", "tear", "tears", "a tear", "sweep",
                        "sweeps", "labour", "in labour", "going into labour", "induction",
                        "contraction", "contractions", "bump"))


_NOT_A_BIRTH_LINE = re.compile(r"\blabou?r day\b|\bpublic holiday\b|\bday off\b|"
                               r"\bbank holiday\b", re.I)


def _a_birth_word(memory, understood):
    reading = understood if isinstance(understood, dict) else {}
    said = (" " + " ".join(str(reading.get("plain") or reading.get("text") or "").lower().split())
            + " ")
    if _NOT_A_BIRTH_LINE.search(said):
        return None
    for word, reply in _BIRTH_WORD_NAMES:
        if not re.search(r"\b" + re.escape(word) + r"s?\b", said):
            continue
        if word in _AMBIGUOUS and not _A_BIRTH_LINE.search(said):
            continue
        return reply
    return None


_A_BIRTH_LINE = re.compile(
    r"\b(?:pregnan\w*|labour|labor|birth|births|midwife|midwives|due date|weeks|bump|baby|"
    r"babies|newborn|waters|dilat\w*|hospital|epidural|cervix)\b", re.I)


_WHEN_TO_CALL = re.compile(
    r"\b(?:how far apart|how often|how close|close together|when should i (?:go|call)|"
    r"how long (?:do|should) (?:they|contractions) last|timing|time them)\b", re.I)
_DO_THEY_HURT = re.compile(r"\b(?:hurt|hurts|painful|pain|supposed to)\b", re.I)

_HOW_FAR_APART = (
    "Time them from the start of one to the start of the next, and call the midwife when they are "
    "about five minutes apart, each one lasting 45 to 60 seconds, for an hour - or straight away "
    "if your waters break, you bleed, the baby stops moving or you feel frightened. A first labour "
    "is usually 8 to 18 hours, so early ones at ten or fifteen minutes apart are the time to rest "
    "and eat rather than go in.")

_THEY_HURT = (
    "Yes, contractions hurt - it is a strong muscle working, and for most people it is the "
    "hardest pain they meet. It peaks and then stops completely between contractions, which is "
    "what makes it bearable, and the relief you can ask for is real: gas and air, a pool, "
    "diamorphine or an epidural. Say what you want early rather than waiting to see how bad it "
    "gets.")


def _a_labour_contraction(memory, understood):
    reading = understood if isinstance(understood, dict) else {}
    said = str(reading.get("plain") or reading.get("text") or "")
    if _WHEN_TO_CALL.search(said):
        return _HOW_FAR_APART
    if _DO_THEY_HURT.search(said):
        return _THEY_HURT
    if not _A_BIRTH_LINE.search(said):
        return None
    return ("A contraction is the womb muscle tightening and then relaxing, which is what opens the "
            "cervix: it builds, holds for 45 to 60 seconds and fades, and the first ones feel like "
            "a bad period pain. They get longer, stronger and closer together as labour goes on. "
            "Time them from the start of one to the start of the next, and call the midwife when "
            "they are about five minutes apart.")


ENTRIES.append(entry(
    "birth-words", (_BIRTH_WORD_KEY, _BIRTH_ASK), _a_birth_word,
    ask=_BIRTH_ASK,
    avoid=("bleeding", "bled", "waters broke", "my waters", "pain", "pains", "hurt", "hurts",
           "cramp", "cramps", "contractions are", "how much", "cost", "costs", "price", "pay",
           "should i", "shall i", "or not", "worth it", "safe", "dangerous", "risk",
           "how do i", "how to", "how long", "when do i", "when should i",
           "appointment", "results", "not offered", "decline", "choose", "decide",
           "my friend", "my sister", "my wife", "my partner", "for my"),
    bias=1))

ENTRIES.append(entry(
    "a-contraction-has-a-birth-in-it",
    (("contraction", "contractions"),
     _BIRTH_ASK + ("how far apart", "how often", "how long", "hurt", "hurts", "painful",
                   "supposed to", "close together")),
    _a_labour_contraction,
    ask=_BIRTH_ASK + ("how far apart", "how often", "hurt", "painful"), bias=3))

_POSTNATAL_BLEED = (
    "bleed", "bleeds", "bled", "bleeding", "blood", "bloods", "clot", "clots",
    "pad", "pads", "lochia", "postnatal", "post natal", "postpartum")
_POSTNATAL_BIRTH = (
    "birth", "births", "after birth", "baby", "babies", "the baby", "my baby",
    "section", "c section", "c-section", "caesarean", "cesarean", "caesarian",
    "postnatal", "post natal", "postpartum", "lochia", "maternity", "midwife",
    "give birth", "gave birth", "giving birth", "delivered", "weeks after", "days after",
    "born", "was born",
    "having my son", "having my daughter", "having a baby", "had my son", "had my daughter",
    "had a baby", "months after", "month after")

ENTRIES.append(entry(
    "postnatal-bleeding",
    (_POSTNATAL_BLEED, _POSTNATAL_BIRTH),
    "Lochia is the bleeding after birth: heavy red blood for three to five days, then browner and "
    "lighter for up to six weeks, coming back a little when you do more - so a bleed still going "
    "past six weeks is a GP visit, not lochia. Use pads, not tampons. Ring your maternity unit the "
    "same day if you soak a pad in an hour, pass clots bigger than a 50p coin, or the blood smells "
    "bad or you are feverish - and 999 or 911 if you are faint, dizzy or flooding.",
    avoid=("period", "periods", "menstrual", "between periods", "miscarriage", "missed",
           "ectopic", "implantation", "pregnant", "pregnancy test", "after sex", "sex",
           "nappy", "nappies", "poo", "stool", "stools", "cord", "circumcision", "nose",
           "nosebleed", "gums", "tooth", "teeth", "urine", "wee", "cut", "wound", "gash",
           "stitches in my hand", "dog", "cat",
           "scar", "scars", "scar tissue", "incision", "stitches", "dressing",
           "blood test", "blood tests", "blood test tomorrow", "heel prick", "screening",
           "jab", "jabs", "vaccine", "vaccination", "vaccinated", "injection", "immunisation",
           "group b strep", "newborn screening",
           "birth control", "contraception", "pill", "pills", "implant", "coil", "iud",
           "morning after", "brain", "head injury", "hit my head"),
    bias=4))

