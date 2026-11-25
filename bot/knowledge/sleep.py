import re

from .lookup import entry, not_the_heat_of_an_argument

ANSWERS = ("sleep",)

INFANT_RED_FLAGS = ("floppy", "flopp", "limp", "unresponsive", "wont wake", "won't wake",
                    "cant wake", "can't wake", "cannot wake", "not waking", "wouldnt wake",
                    "wouldn't wake", "temperature", "fever", "rash", "breathing", "ambulance",
                    "blue", "39", "40")

_AGE_WORDS = ("three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
              "twelve", "thirteen", "fourteen", "fifteen")
SELF_IS_A_CHILD = tuple(
    "%s %s" % (lead, age)
    for age in [str(number) for number in range(3, 16)] + list(_AGE_WORDS)
    for lead in ("am", "im", "i'm", "aged")
)
SLEEPING_BADLY = ("sleep badly", "sleeps badly", "sleeping badly", "sleep terribly",
                  "sleeps terribly", "sleep is bad", "sleep has been bad", "sleep is terrible",
                  "sleep is rubbish", "sleep is awful", "sleep is not great",
                  "sleep has been terrible", "sleep has been awful", "sleep has been rubbish",
                  "sleep is still bad", "sleep is still rubbish", "sleep is still terrible",
                  "dont sleep well", "don't sleep well", "doesnt sleep well",
                  "not sleeping well", "not sleeping properly", "sleeping badly",
                  "sleep poorly", "sleeps poorly", "poor sleep", "bad sleep", "bad nights",
                  "broken sleep", "sleep is broken",
                  "tossing and turning", "tossing and turning all night", "toss and turn",
                  "toss and turn all night", "tosses and turns", "cant stay asleep",
                  "can't stay asleep", "cannot stay asleep")


_BED_CLOCK = re.compile(r"\b([01]?\d|2[0-3])\s*(am|pm|o'?clock)\b", re.IGNORECASE)
_BED_AT_HOUR = re.compile(r"\b(?:at|till|until|by|around|about)\s+([01]?\d|2[0-3])\b",
                          re.IGNORECASE)
_BED_WORD_HOUR = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "eleven": 11,
                  "twelve": 12, "ten": 10, "nine": 9, "eight": 8,
                  "seven": 7, "six": 6}
_HOUR_WORDS = {4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
               10: "ten", 11: "eleven", 12: "twelve"}
_WIDE_OPEN = ("all over the place", "varies", "different every night", "no set time",
              "whenever", "when i feel like it", "at different times")


def _clock_said(hour):
    if hour == 0:
        return "midnight"
    if hour == 12:
        return "noon"
    if hour > 12:
        return "%dpm" % (hour - 12)
    return "%dam" % hour


def _bedtime_said(memory, understood):
    line = _line(understood)
    hour = None
    found = _BED_CLOCK.search(line)
    if found:
        hour = int(found.group(1))
        when = found.group(2).lower()
        if when.startswith("p") and hour < 12:
            hour += 12
        elif when.startswith("a") and hour == 12:
            hour = 0
    if hour is None:
        half = re.search(r"\bhalf\s+(\d{1,2})\b", line)
        if half:
            hour = int(half.group(1))
            if hour <= 11:
                hour += 12
    if hour is None and re.search(r"\bmidnight\b", line):
        hour = 0
    if hour is None:
        found = _BED_AT_HOUR.search(line)
        if found:
            hour = int(found.group(1))
            if hour == 12:
                hour = 0
            elif 6 <= hour <= 11:
                hour += 12
    if hour is None:
        for word, number in _BED_WORD_HOUR.items():
            if re.search(r"\b%s\b" % word, line):
                hour = number
                if hour == 12:
                    hour = 0
                elif 6 <= hour <= 11:
                    hour += 12
                break
    if hour is None:
        if any(w in line for w in _WIDE_OPEN):
            return ("A bedtime that moves every night is harder to sleep on than a late one that "
                    "holds: fix the wake-up time first and keep it seven days a week, get daylight "
                    "before noon, and let the bedtime find its own level. Move it 15 minutes "
                    "earlier every few nights rather than all at once.")
        return ("Late enough that it is the hours rather than the sleep itself: pick a wake-up "
                "time you can keep seven days a week and the bedtime follows within a week or "
                "two, because the morning light is what sets the clock. No caffeine after two.")
    hours = (7 - hour) % 24
    said = _clock_said(hour)
    count = _HOUR_WORDS.get(hours, str(hours))
    if hours >= 7:
        return ("%s is a good bedtime - %s hours before a seven o'clock start - and keeping it the "
                "same seven days a week matters more than the exact hour: dark, cool room, phone "
                "outside the bedroom." % (said.capitalize(), count))
    return ("Bed at %s is %s hours if you are up at seven, and most adults need seven to nine. "
            "Don't force an early night: get up at the same time every day, daylight before noon, "
            "no caffeine after two, and the bedtime follows the wake-up time within a week or "
            "two." % (said, count))


def _the_clock_i_go_to_bed(understood):
    line = _line(understood)
    if any(w in line for w in _WIDE_OPEN):
        return True
    if _BED_CLOCK.search(line) or _BED_AT_HOUR.search(line):
        return True
    if re.search(r"\b(late|later|midnight)\b", line):
        return True
    return bool(re.search(r"\b(?:one|two|three|eleven|twelve)\b", line))


def _line(understood):
    text = understood.get("plain") or understood.get("clean") or ""
    return " " + str(text).lower() + " "


_CUP_GOES = ("Half a cup of coffee is gone in about five hours, so a 4pm cup is still a quarter "
             "in you at 2am, which is why early afternoon is the cutoff for sleep.")
_CUTTING_DOWN = ("Cutting down or quitting brings a headache 12 to 24 hours after the last cup, "
                 "worst on day one or two and gone in one to two weeks: take one cup off every "
                 "couple of days, not all at once, and sleep is better within a few days.")


def _caffeine_timeline(memory, understood):
    text = _line(understood)
    if re.search(r"\bheadache|headaches|withdrawal|withdrawals|shaky|irritable|"
                 r"stopped|stopping|quit|quitting|without|cut(ting)? (down|out|back)\b", text):
        return _CUTTING_DOWN
    return _CUP_GOES


MACHINES = ("washing machine", "washer dryer", "washer", "tumble dryer", "dryer", "dishwasher",
            "boiler", "fridge freezer", "fridge", "freezer", "oven", "hob", "cooker",
            "microwave", "kettle", "toaster", "hoover", "vacuum", "radiator", "air fryer",
            "immersion", "appliance", "machine")
SWITCHED_ON = ("is on", "s on", "on but", "on and nothing", "switched on", "turned on",
               "running", "started", "comes on", "switches on", "light is on", "powers on")


SLEEPLESS = ("cant sleep", "can't sleep", "cannot sleep", "cant get to sleep",
             "can't get to sleep", "lie awake", "lying awake", "wide awake", "asleep",
             "insomnia", "in bed", "to bed", "bedtime")


def _a_machine_that_is_on_is_not_a_sleeper(understood):
    text = " " + str((understood or {}).get("text") or "").lower() + " "
    if any(phrase in text for phrase in SLEEPLESS):
        return True
    if not any(" " + name + " " in text or " " + name + "s " in text for name in MACHINES):
        return True
    return not any(phrase in text for phrase in SWITCHED_ON)


ENTRIES = [
    entry("night-wee", (("pee", "weeing", "toilet", "wee", "bathroom", "bladder", "loo",
                         "for a wee", "to wee", "need a wee", "needing a wee", "a wee in the night",
                         "wee in the night", "up for a wee", "up in the night for a wee",
                         "wake up for a wee", "waking up for a wee", "wake up to wee"),
                        ("night", "nights", "nighttime", "wake", "waking", "woken")),
          "Stop drinking anything an hour or two before bed, cut the evening cup of tea and any "
          "alcohol, and empty your bladder just before you lie down. If you are up two or more "
          "times a night most nights, or it is new, see a GP: it can be an infection, an enlarged "
          "prostate or diabetes, and it is worth checking rather than just putting up with.",
          avoid=("baby", "toddler", "child", "son", "daughter", "dog", "cat", "puppy",
                 "pregnant", "nappy", "nursery", "mirror", "fog", "fogging", "condensation",
                 "steam", "shower", "window", "lens", "glasses")),

    entry("snooze-alarm", (("snooze", "snoozing", "alarm"),
                           ("stop", "how", "keep", "should", "turn off", "five more",
                            "hit", "hitting", "morning")),
          "Put the alarm across the room so you have to stand up, and set it for the last minute "
          "you can actually get up: snoozing for nine minutes at a time just restarts the groggy "
          "part. Going to bed 30 minutes earlier fixes the reason you want to snooze better than "
          "any alarm app.",
          avoid=("baby", "toddler", "child", "phone", "notifications", "neighbour", "neighbor",
                 "car", "fire", "pendant", "personal alarm", "telecare", "lifeline",
                 "careline", "falls alarm", "panic alarm",
                 "burglar", "burglar alarm", "intruder", "house alarm", "home alarm",
                 "security alarm", "security system", "alarm system", "alarm panel",
                 "control panel", "the panel", "keypad", "sensor", "sensors", "cctv",
                 "smoke", "smoke alarm", "smoke detector", "carbon monoxide", "beeping",
                 "chirping",
                 "sound", "sounds", "song", "tune", "ringtone", "music", "louder", "quieter",
                 "volume", "silent")),

    entry("bedtime-said", (("go to bed", "get to bed", "go to sleep at", "bedtime", "bed time",
                            "stay up", "up till", "up until", "lights out", "turn in"),
                           ("am", "pm", "at", "midnight", "late", "later", "till", "until",
                            "oclock", "o'clock", "usually", "every night", "every day",
                            "all over the place", "varies", "whenever", "no set time")),
          _bedtime_said,
          guard=_the_clock_i_go_to_bed,
          avoid=("wake", "wakes", "waking", "woke", "get up", "up at", "alarm", "snooze",
                 "baby", "babies", "toddler", "child", "children", "my son", "my daughter",
                 "newborn", "school", "shift", "night shift", "nights",
                 "cant sleep", "can't sleep", "cannot sleep", "insomnia", "cant get to sleep",
                 "tossing", "wake up", "hour", "hours", "enough", "nap", "naps", "jet lag",
                 "phone", "phones", "scroll", "scrolling", "screen", "screens", "tv", "telly",
                 "laptop", "ipad", "tablet", "games", "gaming",
                 "how many", "how much", "how long", "should i", "what time", "when should")),

    entry("bedtime-clock", (("what time should i go to bed", "what time to go to bed",
                             "when should i go to bed", "time to go to bed",
                             "good time to go to bed", "time should i be in bed"),
                            ("sleep", "bed", "night", "work", "morning", "up", "good")),
          "Count back about eight hours from the time you have to get up, and keep that bedtime "
          "the same seven days a week: the regularity matters more than the exact hour. If you lie "
          "there awake, go to bed half an hour later rather than earlier, so bed means sleep again.",
          avoid=("baby", "toddler", "child", "shift", "nap")),

    entry("sleep-schedule", (("sleep schedule", "body clock", "sleep routine", "sleep pattern",
                              "circadian", "back into a routine", "fix my sleep"),
                             ("fix", "reset", "how", "back", "help", "should", "get", "regular")),
          "Pick one wake-up time and keep it every day for two weeks, weekends included: the "
          "morning light is what sets the clock. Then move bedtime 15 minutes earlier every few "
          "nights, keep the room dark and cool, and take a short walk in daylight before noon. "
          "Melatonin half an hour before bed helps some people while the habit sets.",
          avoid=("baby", "toddler", "child", "shift work", "night shift")),

    entry("sleep-cycle",
          (("sleep cycle", "sleep cycles", "sleep stage", "sleep stages", "stages of sleep",
            "rem sleep", "deep sleep", "light sleep", "dream sleep"),
           ("what", "why", "how long", "long", "mean", "means", "explain", "normal", "wake",
            "waking", "work")),
          "A night runs in cycles of about ninety minutes: light sleep, then deeper sleep, then a "
          "stretch of REM where you dream, and round again. The deep sleep is heaviest in the "
          "first half of the night and the dream stretches get longer towards morning, which is "
          "why a 6am wake with a dream still in your head is normal and why the last hour feels "
          "so strange to be woken out of. Waking between cycles feels much better than waking in "
          "the middle of deep sleep, so count back in ninety-minute blocks from your alarm: five "
          "is seven and a half hours of sleep, which is why 11pm to 6.30am often feels better "
          "than 11pm to 6am.",
          explain=True),

    entry("nightmares", (("nightmare", "nightmares", "bad dream", "bad dreams", "night terror"),
                         ("keep", "always", "how", "stop", "why", "every", "about", "having",
                          "had", "have", "got", "last night", "woke", "waking", "keeps",
                          "often", "scary", "terrifying", "vivid", "upset")),
          "Nightmares usually follow stress, late food, alcohol or a heavy film before bed, so "
          "start there. If the same one keeps coming back, write it down in the day and rehearse a "
          "different ending a few times: that is the technique that works. See a GP if they are "
          "waking you most nights or coming with flashbacks.",
          avoid=("baby", "toddler", "child", "son", "daughter", "kid", "kids", "dog", "cat",
                 "year old", "years old", "my boy", "my girl", "grandson", "granddaughter",
                 "niece", "nephew", "pupil", "school",
                 "little girl", "little boy", "little one", "little lad", "my little",
                 "girl", "boy", "lad") + SELF_IS_A_CHILD),

    entry("bedtime-routine", (("before bed", "bedtime routine", "wind down", "get ready for bed",
                               "bedtime"),
                              ("should", "what", "how", "do", "routine", "tips", "best")),
          "The routine matters less than the regularity: same time, lights down, screens off, and "
          "something calm for the last half hour, like a shower, a few pages of a book or the "
          "dishes. Keep the bed for sleeping, and if you are not asleep in 20 minutes get up and "
          "read somewhere dim until you are sleepy.",
          avoid=("baby", "toddler", "child", "son", "daughter", "tea", "coffee", "drink",
                 "phone", "tv", "wine", "alcohol", "beer", "glass")),

    entry("switch-off", (("switch off", "mind racing", "racing mind", "mind is racing",
                          "brain is racing", "head is racing", "thoughts racing",
                          "overthinking", "my brain wont", "my brain won't", "head won't stop",
                          "clear my head at night", "clear my mind at night",
                          "clear my head before bed", "clear my mind before bed",
                          "clear my head before sleep", "clear my mind before sleep",
                          "clear my head to sleep", "clear my mind to sleep",
                          "clear my thoughts before bed", "clear my head for bed"),
                         ("night", "bed", "sleep", "how", "cant", "can't", "help", "should",
                          "off", "wont", "won't")),
          "Write tomorrow's list down before bed: most of the racing is your head keeping the "
          "list for you. Then a slow breathing pattern, in for four and out for six, for a couple "
          "of minutes, and get up rather than lie there arguing with yourself if it goes on past "
          "20 minutes.",
          avoid=("work", "boss", "meeting", "email", "deadline", "mobile data", "data",
                 "mobile", "phone setting", "settings", "wi-fi", "wifi", "bluetooth",
                 "airplane", "roaming", "power", "light switch", "plug",
                 "stop thinking", "thinking about",
                 "phone", "mobile", "battery", "charger", "charging", "laptop", "tv", "telly",
                 "screen", "appliance", "kettle", "boiler", "car", "engine", "light",
                 "water", "mains", "stopcock", "stop tap", "stop valve", "tap", "taps", "pipe",
                 "pipes", "plumbing", "valve", "radiator", "heating", "gas", "electricity",
                 "electric", "lectric", "supply", "fuse", "fuse box", "circuit",
                 "socket", "sockets", "alarm", "timer")),

    entry("wake-earlier", (("wake up earlier", "get up earlier", "wake earlier", "wake up at 5",
                            "wake up at 6", "become a morning person", "early riser"),
                           ("how", "should", "want", "help", "tips", "can i")),
          "Shift it 15 minutes at a time, not an hour: set the alarm a quarter of an hour earlier "
          "every three or four days and go to bed a quarter earlier too, or you just lose sleep. "
          "Get daylight on your face within half an hour of waking, and keep the new time at "
          "weekends or Monday undoes it.",
          avoid=("baby", "toddler", "child", "son", "daughter", "kid")),

    entry("get-up-in-the-morning",
          (("get out of bed", "getting out of bed", "out of bed", "get up in the morning",
            "getting up in the morning", "get up when", "getting up when", "hard to get up",
            "struggle to get up", "struggling to get up", "cant get out of bed",
            "can't get out of bed", "get myself up", "get going in the morning",
            "cannot get up", "cant get up", "can't get up"),
           ("how", "should", "want", "help", "tips", "can i", "why", "what can",
            "morning", "mornings", "in the morning", "every morning", "myself")),
          "Stand up as soon as the alarm goes, before you have thought about it: that heavy, "
          "can't-move feeling is sleep inertia and it lifts about fifteen minutes after you are "
          "upright. Alarm across the room, curtains open, and the same wake time every day. If "
          "every morning is like that with no energy at all, a blood test for thyroid and "
          "anaemia is the next step.", bias=1,
          avoid=("feel", "feeling", "feels", "depressed", "depression", "hopeless", "worthless",
                 "anxious", "anxiety", "panic", "no point", "miserable", "unhappy", "sad all",
                 "cant face", "can't face", "dread", "dreading", "hangover", "hungover",
                 "baby", "babies", "toddler", "toddlers", "child", "children", "kid", "kids",
                 "son", "daughter", "dog", "dogs", "puppy", "cat", "cats", "pet", "pets",
                 "snooze", "snoozing", "alarm", "tired all the time",
                 "my back", "my knee", "my hip", "my neck", "shower", "shaving")),

    entry("hot-night", (("night", "sleep", "sleeping", "bed", "bedroom", "asleep",
                         "sleep in the heat", "sleeping in the heat", "better sleep in the heat",
                         "in the heat", "in this heat", "hot weather", "warm night", "warm nights",
                         "cool in bed", "stay cool", "keep cool", "cool down at night",
                         "keeping me awake", "keeps me awake", "keeping me up", "hot in bed",
                         "too hot to sleep"),
                        ("too hot", "so hot", "its hot", "is hot", "getting hot", "hot night",
                         "hot nights", "boiling hot", "heatwave",
                         "heat", "cool",
                         "sweating", "sweaty", "sticky", "fan", "no air", "hot night")),
          "Cool the room rather than the bed: open windows on both sides for a through draught, "
          "keep the curtains shut in the day, and put a bowl of ice in front of a fan. A lukewarm "
          "shower before bed, cotton sheets and a hot water bottle filled with cold water at your "
          "feet all help more than sleeping with no cover at all.",
          avoid=("goodnight", "night night", "off to bed", "im off", "bedtime for me", "see you",
                 "bye", "good night", "baby", "toddler", "child", "fever", "radiator", "boiler",
                 "wear", "wearing", "what to wear", "should i wear", "outfit", "outfits",
                 "what do i wear", "what shall i wear", "dress code",
                 "water bottle", "hot flush", "menopause",
                 "thermostat", "put the heating", "turn the heating", "heating off",
                 "heating on", "heating bill", "heating cost", "radiator valve",
                 "cool the room", "cool my bedroom down", "keep the room cool",
                 "keep the house cool", "keep my bedroom cool",
                 "heat my", "heat the room", "heat the house", "heat a room", "how do i heat",
                 "heating the", "warm my bedroom", "warm the room",
                 "dog", "dogs", "cat", "cats", "puppy", "kitten", "pet", "pets", "rabbit",
                 "in the car", "my car", "the car", "car seat"),
          guard=not_the_heat_of_an_argument,
          bias=2),
    entry("toddler-wakes", (("wakes up at", "wakes at", "waking at", "wakes in the night",
                             "wakes every night", "still wakes", "up at night"),
                            ("toddler", "2 year old", "two year old", "3 year old",
                             "three year old", "18 months", "one year old", "she", "he", "her",
                             "him", "night")),
          "A toddler who goes down at seven and is awake again at ten is usually treating bedtime "
          "as a nap: push bedtime later by 15 minutes every few days, keep the room dark and the "
          "last hour quiet, and make the 10pm wake-up boring - a quick cuddle in the dark, no "
          "lights, no play. Ask your health visitor if it is still happening after two weeks.",
          ask=("toddler", "child", "baby", "son", "daughter", "kid", "she", "he", "her", "him",
               "year old", "months old"),
          avoid=("died", "grief", "funeral", "widow", "miss him", "miss her", "passed away",
                 "hospital", "pain", "teething", "ill",
                 "up at 4", "up at 5", "up at 6", "at 4am", "at 5am", "at 6am", "at 4 am",
                 "at 5 am", "at 6 am", "4am", "5am", "6am", "early waking", "every morning at",
                 "cat", "cats", "kitten", "kittens", "dog", "dogs", "puppy", "puppies",
                 "pet", "pets", "rabbit", "hamster", "guinea pig", "parrot")),

    entry("fall-asleep", (("fall asleep", "get to sleep", "drop off", "nod off", "drift off",
                           "go to sleep", "lie there", "lying there", "lie awake", "lying awake",
                           "still awake", "wide awake", "nothing happens"),
                          ("cant", "can't", "cannot", "fast", "faster", "quick", "quickly",
                           "hours", "struggle", "hard", "help", "how", "nothing", "happens",
                           "what if", "then what", "just", "awake", "bed", "night",
                           "thinking", "worries", "worrying")),
          "Get up after 20 minutes of lying there awake and do something dull in low light until "
          "you feel sleepy, then go back: staying in bed teaches your brain that bed is where you "
          "lie awake. Keep the wake-up time the same every day, dim the lights an hour before, "
          "and park tomorrow's worries on paper before you get in.",
          avoid=("baby", "babies", "toddler", "child", "children", "kid", "kids", "died",
                 "death", "grief", "passed away", "funeral", "widow", "miss him", "miss her",
                 "dog", "cat", "puppy", "book", "exercise", "yoga", "massage", "phone",
                 "battery", "charger", "engine", "car", "tv", "telly", "screen",
                 "button", "press", "remote", "keyboard", "mouse", "reset", "reboot",
                 "switch on", "turn on", "wont start", "will not start"),
          guard=_a_machine_that_is_on_is_not_a_sleeper),

    entry("sleep-trouble",
          (("sleep", "sleeping", "insomnia", "awake") + SLEEPING_BADLY,
           ("trouble", "can't", "cant", "cannot", "struggle", "problems",
            "better", "at all", "half the night", "help",
            "badly", "bad", "poorly", "terribly", "awful", "horribly",
            "have", "got", "ive got", "i've got", "suffer", "suffering",
            "chronic", "years", "mild", "real", "sometimes",
            "improve", "improves", "improving", "improvement", "better sleep",
            "sleep well", "sleeping well", "get more sleep", "more sleep", "need more sleep",
            "make myself sleep", "sort my sleep", "sort out my sleep",
            "reset my sleep", "catch up on sleep", "rest better",
            "cure", "cured", "curing", "get rid of", "stopped",
            "tossing", "turning", "stay asleep", "staying asleep",
            "keeps me awake", "keep me awake", "kept me awake", "wide awake",
            "awake all night", "awake half the night",
            "what should i do", "what can i do", "what do i do", "what shall i do",
            "what would you do", "do about", "anything i can do", "any tips", "any advice")
           + SLEEPING_BADLY),
          "The things that work: same wake-up time every day, no caffeine after early afternoon, "
          "not much alcohol in the evening (it wakes you in the second half of the night), a "
          "cool dark room, and getting out of bed if you're awake for more than 20 minutes. Screens "
          "off half an hour before bed and a short walk most days help more than any app. If you're "
          "worn out all day too, or it has gone on for weeks, ask a GP: they can check your bloods, "
          "and broken sleep plus no energy is worth ruling out.",
          avoid=("baby", "toddler", "child", "nap", "died", "death", "grief", "passed away",
                 "funeral", "lost my", "widow", "miss him", "miss her",
                 "miss my", "miss them", "still miss", "thinking about my",
                 "waking up at", "wake up at", "waking at", "wake at", "up at 3", "up at 4",
                 "up at 5", "at 3am", "at 4am", "at 5am", "at 6am",
                 "fever", "flu", "cough", "chesty", "sore throat",
                 "sofa", "couch", "settee", "car", "floor", "tent", "sleeping bag",
                 "tracker", "watch", "fitbit", "app", "study", "test",
                 "make up", "makeup", "contacts", "contact lenses", "lenses", "fan",
                 "window", "heating", "air con", "radiator", "shift", "night shift",
                 "laptop", "computer", "macbook", "pc", "monitor", "keyboard", "router",
                 "last night", "tonight", "no sleep", "not slept", "didnt sleep",
                 "didn't sleep", "couldnt sleep", "couldn't sleep", "havent slept",
                 "haven't slept", "one night", "jet lag", "jetlag",
                 "havent been sleeping", "haven't been sleeping",
                 "not been sleeping", "not sleeping at all", "able to sleep",
                 "exam", "exams", "revision", "revise", "cramming", "cram", "mock",
                 "mocks", "coursework", "dissertation", "thesis", "revision notes",
                 "plane", "airport", "hotel", "hotels",
                 "time zone", "timezone", "travelling", "traveling",
                 "newborn", "new baby", "son", "daughter", "stepson", "stepdaughter",
                 "grandson", "granddaughter", "year old", "years old", "kids",
                 "my boy", "my girl", "my little one",
                 "tired", "exhausted", "no energy", "fatigue",
                 "hot", "heat", "heatwave", "humid", "boiling", "warm room",
                 "alcohol", "beer", "wine", "tea", "coffee",
                 "caffeine", "espresso", "latte",
                 "back", "backs", "sore back", "back pain", "backache", "lower back",
                 "back hurts", "back hurt", "back aches", "back ache", "sciatica",
                 "night shift", "night shifts", "nightshift", "shifts", "shift work",
                 "jet lag", "jetlag",
                 "snore", "snores", "snoring", "snorer", "partner snores",
                 "back", "back pain", "backache", "lower back", "sore back",
                 "pain", "pains", "painful", "hurts", "hurting", "ache", "aches", "aching",
                 "exam", "exams", "revision", "revising", "deadline", "deadlines",
                 "knackered", "shattered", "wiped out", "done in", "worn out", "drained",
                 "feel low", "feeling low", "low mood", "depressed", "miserable",
                 "hayfever", "hay fever", "allergy", "allergies", "allergic",
                 "night before a flight", "before an early flight", "early flight",
                 "neighbour", "neighbours", "neighbors", "noisy", "noise", "loud music",
                 "dog", "dogs", "puppy", "puppies", "cat", "cats", "kitten", "kittens",
                 "pet", "pets", "vet",
                 "my son", "my daughter", "my husband", "my wife", "my partner", "my mum",
                 "my dad")),
    entry("baby-sleep-night", (("baby", "babies", "newborn", "toddler", "toddlers",
                                "1 year old", "2 year old", "two year old"),
                               ("sleep", "night", "nighttime", "through", "wakes", "waking",
                                "wake up")),
          "For a baby over six months, a consistent wind-down, dim lights and a fixed bedtime help "
          "more than any trick; feedings at night are normal for much longer than people expect. "
          "Ask your health visitor or GP if you're worried, and never use anything that promises a "
          "quick fix for a very young baby.",
          avoid=INFANT_RED_FLAGS + ("not feeding", "grunt", "grunting", "grunts", "snorting",
                                    "gasping", "cough", "coughs", "coughing", "cold", "colds",
                                    "fever", "temperature", "rash", "wheeze", "wheezing",
                                    "congested", "congestion", "blocked nose", "runny nose",
                                    "chesty", "breathing", "breath", "vomiting", "being sick",
                                    "reflux", "colic", "teething", "ill", "poorly", "unwell",
                                    "how many hours", "how much sleep", "hours a day",
                                    "toddler", "toddlers", "three year old", "3 year old",
                                    "two year old", "2 year old", "four year old", "4 year old",
                                    "grind", "grinds", "grinding", "grinds her teeth",
                                    "grinds his teeth", "grinding her teeth",
                                    "grinding his teeth",
                                    "preschooler", "preschool", "early waking", "wakes at 5",
                                    "wakes up at 5", "wakes at 4", "wakes up at 4")),
    entry("tv-sleep", (("tv", "television"), ("sleep", "bed", "bad", "before bed")),
          "It isn't dangerous, but the light and the story keep your brain alert, so you fall "
          "asleep later and wake more in the night. If you need something playing, a podcast or "
          "radio set to sleep is easier on sleep than a screen."),
    entry("read-bedtime",
          (("read", "reading", "reads", "book", "books", "novel", "kindle", "ereader",
            "e-reader", "chapter", "chapters", "audiobook", "audio book"),
           ("bed", "in bed", "before bed", "bedtime", "night", "sleep", "asleep", "late",
            "sleeping", "fall asleep", "wind down", "evening", "bad", "good", "ok", "okay",
            "stop")),
          ("Reading on paper in low light is one of the better wind-downs there is, and a book you "
           "have read before is easier to put down than a new one. It is the backlit screen and "
           "the scrolling that delay sleep, so a phone or tablet story is the one to move; an "
           "e-reader on a warm setting is much closer to paper. If a book hooks you so hard you "
           "are still going at 2am, keep a dull one by the bed and save the page-turner for the "
           "daytime."),
          avoid=("kid", "kids", "child", "children", "son", "daughter", "toddler", "baby",
                 "teenager", "teen", "year old", "years old", "read to", "reading to",
                 "aloud", "out loud", "stories for", "bedtime story", "bedtime stories",
                 "recommend", "suggest", "what book", "which book", "what should i read",
                 "good book", "book to read", "books to read", "something to read", "any book",
                 "a book for", "some book", "reading list",
                 "gift", "present", "birthday", "christmas", "library", "bookshop",
                 "book club", "lamp", "bulb", "light", "lights", "torch", "curtain", "blind",
                 "shut", "broken", "battery", "glasses", "eyes", "eye test", "sight",
                 "how do i read", "how to read", "learn to read", "dyslexia",
                 "finished", "finish a book", "gave up", "give up"),
          bias=1),
    entry("afternoon-slump",
          (("afternoon", "after lunch", "after my lunch", "3pm", "3 pm", "three o'clock",
            "mid afternoon", "midafternoon", "post lunch", "2pm", "2 pm", "4pm", "4 pm",
            "late afternoon", "middle of the day", "after eating", "tired in the afternoon",
            "sleepy in the afternoon", "afternoon slump", "afternoon dip"),
           ("tired", "sleepy", "slump", "sluggish", "drained", "flagging", "yawn", "yawning",
            "crash", "nod off", "no energy", "low energy", "knackered", "exhausted", "feel",
            "feeling", "focus", "concentrate", "foggy", "brain fog", "drowsy", "stop", "beat",
            "avoid", "fix", "cure"),
           ("how do i stop", "how do i", "how can i", "how to", "what can i do", "tips",
            "ways", "best way", "help")),
          "The dip after lunch is your body clock, not laziness: eat a lunch with protein and "
          "fibre in it rather than a big pile of white carbs, and go outside for ten minutes "
          "afterwards, because daylight and moving your legs take the dip down most. A coffee "
          "before 2pm helps, one after 3pm costs you tonight's sleep. If it happens every day for "
          "weeks, get your iron and thyroid checked.",
          avoid=("toddler", "child", "kid", "baby", "year old", "son", "daughter", "pregnant",
                 "pregnancy", "expecting", "breastfeeding", "nursing", "newborn", "my mum",
                 "my dad", "my husband", "my wife", "elderly", "dementia",
                 "headache", "migraine", "nap", "naps", "nap", "can't sleep", "cant sleep",
                 "wake up", "waking", "insomnia", "at night", "before bed")),
    entry("nap", (("nap", "naps", "napping", "power nap", "siesta"),
                  ("groggy", "afternoon", "how long", "20 minutes", "best way", "refreshed",
                   "sleepy", "tired", "before", "after lunch", "feel", "wake up",
                   "day", "in the day", "during the day", "ok", "okay", "alright", "bad",
                   "good", "harm", "healthy", "worth it", "should i", "is it ok")),
          "Keep a nap to 20 minutes and take it before 3pm, or you'll feel groggy and sleep worse "
          "that night; 30 to 60 minutes is where the grogginess lives, so set an alarm. Skip it if you "
          "already lie awake at night, and if you need one every afternoon for weeks, that is "
          "worth a word with the GP, especially with low mood, thirst or weight loss.",
          avoid=("toddler", "child", "kid", "baby", "year old", "son", "daughter", "she", "he",
                 "her", "him", "pregnant", "pregnancy", "expecting", "breastfeeding", "nursing",
                 "cut them", "cut it",
                 "stop napping", "stop taking naps", "stop my naps", "give up naps",
                 "stop napping in", "quit napping")),
    entry("caffeine-sleep", (("caffeine", "coffee", "espresso", "energy drink", "energy drinks",
                              "cola", "diet coke"),
                             ("sleep", "afternoon", "cut", "stop", "bed", "keep me up", "up",
                              "would that", "keep me awake", "keep you up", "keep you awake",
                              "keeps me awake", "keeps you awake", "awake at night", "cant sleep",
                              "can't sleep", "not sleep", "wake up")),
          "Caffeine has a half-life of about five hours, so a 4pm coffee is still in your system "
          "at bedtime: stop by early afternoon. Cutting down gradually over a week avoids the "
          "headaches that a sudden stop brings.",
          bias=1),
    entry("caffeine-how-long", (("caffeine", "coffee", "coffees", "espresso", "caffeinated",
                                "energy drink", "energy drinks", "cola", "diet coke"),
                               ("how long", "how soon", "how many hours", "last", "lasts",
                                "till it helps", "until it helps", "how long till",
                                "how long until", "till i feel", "until i feel",
                                "wears off", "wear off", "worn off", "system", "withdrawal",
                                "withdrawals", "skip", "skipped", "skipping", "stopped",
                                "stopped drinking", "quit", "gone", "missing", "missed",
                                "dont drink", "without"),
                               ("headache", "headaches", "head", "tired", "irritable", "grumpy",
                                "helps", "feel", "long", "shaky")),
          _caffeine_timeline,
          avoid=("keep", "keeps", "kept", "stored", "store", "beans", "ground", "grounds",
                 "brewing", "brew", "pot", "mug", "fridge", "freezer", "shop", "cafe",
                 "price", "cost", "pods", "pod", "machine", "maker", "makers", "grinder",
                 "after opening", "once opened", "opened", "good for", "shelf life", "shelf",
                 "sleep", "sleeping", "sleepy", "bed", "bedtime", "awake", "insomnia",
                 "dehydrate", "dehydration", "addicted", "addiction", "bad for", "safe", "limit",
                 "much", "many", "pregnant", "pregnancy", "breastfeeding"),
          bias=3),
    entry("lie-in", (("lie in", "lie-in", "lying in", "lay in", "sleep in", "sleeping in",
                      "slept in", "longer in bed", "stay in bed", "catch up on sleep",
                      "catch up on my sleep"),
                     ("weekend", "ok", "okay", "bad", "harm", "saturday", "sunday", "allowed",
                      "matter", "should i", "is it ok", "can i")),
          "Up to an hour later is free; two hours or more moves your body clock, so Sunday night "
          "is harder and Monday morning feels like jet lag. If you are short of sleep, an earlier "
          "night is worth more than a long lie-in, and a 20-minute nap in the afternoon gets you "
          "through without shifting the clock.",
          avoid=("toddler", "child", "kid", "baby", "year old", "son", "daughter", "school",
                 "teenager", "dog", "cat", "pet", "hospital", "care home", "car", "van")),
    entry("alcohol-sleep", (("alcohol", "wine", "beer"),
                            ("sleep", "drink", "night", "bed", "wind down", "winding down",
                             "relax")),
          "A drink helps you fall asleep but breaks it up later: expect to wake around 3am and "
          "sleep less deeply. Leaving three hours between your last drink and bed, with water in "
          "between, makes a clear difference.",
          avoid=("pregnant", "pregnancy", "expecting", "breastfeeding", "breast feeding",
                 "nursing", "antibiotics", "tablets", "medication", "medicine", "pills",
                 "paracetamol", "ibuprofen", "nurofen", "painkiller", "painkillers",
                 "co-codamol", "co codamol", "codamol", "aspirin", "antihistamine",
                 "doctor", "driving", "drive")),
    entry("screen-bedtime", (("phone", "phones", "screens", "screen", "scroll", "scrolling",
                              "doomscroll", "doom scrolling", "tiktok", "instagram", "reels",
                              "youtube", "facebook"),
                             ("bed", "sleep", "before bed", "evening", "night")),
          "The light isn't the main problem; the scrolling is, because it keeps your mind busy. Try "
          "putting the phone on charge outside the bedroom for a week, or set a timer 30 minutes "
          "before bed and read on paper instead.",
          avoid=("died", "battery", "charger", "broken", "lost", "cracked", "contract", "bill",
                 "left", "left it", "taxi", "cab", "stolen", "stole", "theft", "robbed",
                 "missing", "found", "hand it in", "dropped", "airport", "train", "bus",
                 "block", "blocked", "sim", "police",
                 "notification", "notifications", "do not disturb", "alert", "alerts",
                 "ringing", "rings", "buzzing", "buzzes", "vibrating", "vibrates",
                 "ping", "pings", "pinging", "pinged",
                 "wakes me", "waking me", "woke me", "keeps waking", "keep waking",
                 "woken up by", "being woken",
                 "kid", "kids", "child", "children", "son", "daughter", "teenager", "teen",
                 "photo", "photos", "picture", "pictures", "camera", "night mode", "video",
                 "a row", "row with", "row about", "had a row", "proper row", "right row",
                 "argued", "arguing", "argues", "argument", "arguments", "quarrel",
                 "quarrelled", "quarreling", "fell out", "falling out", "fight with",
                 "fought", "cross with", "angry with",
                 "my boy", "my girl")),
    entry("wake-up-tired", (("wake up", "waking up", "wake", "woke up", "get up", "morning",
                             "even after", "even though", "hours sleep", "8 hours", "seven hours",
                             "8hrs", "seven hours sleep"),
                            ("tired", "knackered", "exhausted", "groggy", "drained", "shattered",
                             "not rested", "more tired", "worse than", "no energy", "unrested")),
          "Waking up tired usually means broken sleep rather than too little: a warm room, a drink "
          "in the evening, a snoring partner and a phone in bed all fragment it. Try a cooler "
          "bedroom, no alcohol within three hours of bed, and the same wake time every day for two "
          "weeks, because that last one is what rebuilds a steady night.",
          avoid=INFANT_RED_FLAGS + ("baby", "toddler", "child", "children", "kid", "kids", "son",
                                    "daughter", "puppy", "cat", "dog")),
    entry("wake-middle-night", (("middle of the night", "in the middle of the night",
                                 "wake up in the middle of the night", "waking in the night",
                                 "wake in the night", "cant stay asleep", "can't stay asleep",
                                 "wake several times", "waking several times"),
                                ("night", "why", "how", "stop", "keep", "help", "always",
                                 "every", "sleep", "again")),
          "Waking in the middle of the night is normal - the trick is what you do next: stay in "
          "bed, keep the room dark, and do not look at the clock or your phone, because that is "
          "what teaches your brain to be awake at 3am. If you are awake more than 20 minutes, get "
          "up and sit somewhere dim until you feel sleepy. Alcohol, a late meal and a warm bedroom "
          "are the usual culprits.",
          ask=("wake", "waking", "woke", "awake", "night", "asleep"),
          avoid=("baby", "toddler", "child", "children", "kid", "kids", "son", "daughter",
                 "dog", "cat", "nightmare", "pregnant", "pregnancy")),

    entry("night-shift-sleep", (("work nights", "working nights", "work nights", "night shift",
                                "night shifts", "nightshifts", "on nights", "on shifts",
                                "shift work", "shift pattern", "rotating shifts"),
                               ("sleep", "sleeping", "day", "daytime", "cant", "can't", "never",
                                "tired", "rest")),
          "Pick one stretch of daytime to sleep and guard it like a night: straight home, dark "
          "room, phone off, and the same hours seven days a week, including days off, so your body "
          "clock settles. Wear sunglasses on the way home and keep the bedroom cold, and take a "
          "short nap before the shift rather than a long one after it.",
          avoid=("baby", "toddler", "child", "newborn", "cough", "cold", "worse at night",
                 "hurts", "pain", "ache")),

    entry("duvet-tog",
          (("duvet", "duvets", "quilt", "quilts", "bedding"),
           ("tog", "togs", "warm", "warmest", "warmer", "winter", "cold", "cosy",
            "thick", "thicker", "summer")),
          "A 13.5 tog duvet is the winter one, 4.5 tog is for summer and 10.5 tog or two thin ones "
          "that button together cover the rest of the year. Tog measures warmth for its weight, "
          "not how heavy it feels, so a 13.5 tog feather duvet and a 13.5 tog hollowfibre one are "
          "equally warm - buy the filling you can wash and dry. For a cold bedroom, a second "
          "lighter duvet on top or a hot water bottle at your feet warms you faster than a heavier "
          "one over your whole body.",
          avoid=("wash", "washing", "washed", "clean", "cleaning", "stain", "stains",
                 "smell", "smells", "musty", "yellow", "dryer", "tumble", "machine",
                 "baby", "babies", "newborn", "toddler", "cot", "crib", "moses",
                 "fever", "temperature", "sweat", "sweating", "night sweats", "allergy",
                 "allergic", "feather allergy", "dust mite",
                 "always cold", "always so cold", "all the time", "constantly", "cold hands",
                 "cold feet", "cold all", "feel the cold", "thyroid", "iron", "anaemic",
                 "anemic", "circulation", "shivering", "shiver", "tired all", "exhausted",
                 "cold sweats", "cant get warm", "can't get warm", "never warm"),
          bias=1),
    entry("bedroom-temp", (("bedroom", "room temperature", "my room"), ("warm", "warmth",
                            "temperature", "degrees", "hot", "cold", "how warm", "how cool",
                            "bedroom is freezing", "bedroom is freezing cold",
                            "bedroom freezing", "freezing bedroom", "bedroom is so cold",
                            "bedroom is too cold", "bedroom is baltic", "bedroom is chilly",
                            "bedroom is always freezing", "bedroom is freezing at night",
                            "bedroom is cold at night",
                            "like a fridge", "like a freezer", "like an oven", "like a sauna",
                            "like a furnace", "like the arctic", "icebox", "an icebox")),
          "A bedroom around 16 to 18C suits most people for sleep: cool enough that you need a "
          "duvet, not so cold you wake up. Cracking a window for ten minutes before bed, a lighter "
          "duvet in summer and a hot water bottle rather than a hot room all help, and a warm "
          "bath an hour before bed sends you to sleep faster than a warm bedroom does.",
          ask=("bedroom", "room temperature", "my room"),
          avoid=("baby", "babies", "newborn", "toddler", "cot", "crib", "nursery", "infant",
                 "child", "children", "kid", "kids",
                 "butter", "cake", "meat", "chicken", "egg", "eggs", "milk", "cheese", "dough",
                 "yeast", "batter", "chocolate", "wine", "beer", "yoghurt", "yogurt", "roast",
                 "baking", "thaw", "defrost",
                 "in the fridge", "the fridge", "my fridge", "fridge is", "fridge not",
                 "fridge door", "in the freezer", "the freezer", "my freezer", "freezer is",
                 "steak", "steaks", "beef", "pork", "lamb", "turkey", "bacon", "sausage",
                 "sausages", "fish", "salmon", "pastry", "cream", "cook", "cooking", "oven",
                 "recipe", "soften", "mayonnaise",
                 "radiator", "radiators", "heating", "boiler", "thermostat", "thermostatic",
                 "bleed", "bleeding", "trv", "valve", "valves"),
          bias=1),

    entry("tea-bedtime", (("tea", "coffee", "drink"), ("bed", "sleep", "night", "bedtime",
                                                       "before", "keep you up", "keep me up",
                                                       "keep you awake", "keep me awake",
                                                       "keeps you awake", "keeps me awake",
                                                       "late at night", "late")),
          "Tea has enough caffeine to keep you awake if it's after about 2pm, so switch to a herbal "
          "one or a warm drink without caffeine in the evening. A milky drink is fine; it's the "
          "caffeine and the late loo trip that cost you sleep.",
          bias=1),

    entry("wake-in-pain",
          (("keep waking", "wake up", "waking up", "wake at", "waking at", "woken up",
            "wide awake", "up in the night", "in the night", "at 3am", "at 2am", "at 4am",
            "at 3", "at 2", "at 4", "3am", "2am", "4am", "3 am", "2 am", "4 am"),
           ("pain", "painful", "ache", "aching", "hurts", "hurting", "sore", "stiff",
            "my back", "bad back", "back pain", "backache", "aching back", "sore back",
            "stiff back", "lower back", "back problem", "back trouble",
            "shoulder", "hip", "knee", "legs", "leg", "arm", "neck", "cramp", "cramps",
            "pins and needles", "heartburn", "reflux", "toothache")),
          "If pain is what wakes you, treat the pain rather than the sleep: take a painkiller half "
          "an hour before bed if you can, prop the sore part on a pillow and put a rolled towel "
          "under a bad back. Warm bath and gentle stretches before bed loosen a stiff shoulder or "
          "hip. If it wakes you most nights for weeks, or comes with numbness, weakness or weight "
          "loss, get it looked at.",
          bias=3,
          avoid=("calf", "calves", "swollen", "swelling", "chest", "breathless", "fever",
                 "cough", "coughing", "baby", "toddler", "child", "children", "son", "daughter",
                 "mum", "dad", "partner", "husband", "wife", "dog", "cat", "pregnant",
                 "morning", "mornings", "first thing", "all over", "get out of bed",
                 "throat", "voice", "hoarse", "croaky", "sore throat",
                 "cramp", "cramps", "cramping", "leg cramp", "leg cramps", "charley horse",
                 ) + INFANT_RED_FLAGS),

]

ENTRIES.append(entry(
    "sleep-position",
    (("front", "on my front", "on your front", "on my back", "on your back", "on my side",
      "on your side", "stomach", "sleeping position", "position to sleep", "best position",
      "which side", "side to sleep"),
     ("sleep", "sleeping", "slept", "asleep", "bed", "night", "bad", "best", "should i",
      "better", "position", "healthy", "okay", "ok")),
    "On your side is the best default: it keeps the airway open and takes the load off your "
    "lower back, and a pillow between the knees keeps the hips level. Front sleeping leaves the "
    "neck turned for hours, which is why front sleepers wake with a stiff neck, and on your back "
    "snoring and heartburn are worse. The position you can stay asleep in beats the perfect one - "
    "and if you wake with a sore neck or back, the pillow is usually the thing to change first.",
    ask=("sleep", "sleeping", "slept", "asleep", "bed", "night", "position", "nap"),
    avoid=("my back hurts", "back pain", "sore back", "back ache", "lower back", "back door",
           "front door", "back garden", "front garden", "come back", "go back", "back to work",
           "back home", "back from", "on the front", "front room", "back room", "back seat",
           "pregnant", "pregnancy", "expecting", "wrinkle", "wrinkles", "wrinkly", "skin",
           "baby", "babies", "newborn", "new born", "infant", "cot", "cot death", "toddler",
           "my son", "my daughter", "my child", "children", "kids", "my boy", "my girl",
           "hurts", "hurt", "hurting", "pain", "painful", "sore", "ache", "aches", "aching",
           "stiff"),
    bias=1))

ENTRIES.append(entry(
    "a-night-routine",
    (("routine", "routines", "ritual", "wind down", "winddown", "wind-down", "what should i do"),
     ("night", "nights", "evening", "evenings", "before bed", "bedtime", "sleep", "bed")),
    "The same hour in the same order every night: screens off 45 minutes before bed, the lights "
    "down, and three small things done the same way - teeth, tomorrow's clothes out, ten minutes "
    "of a book. Keep the bedroom cool, dark and quiet, and put the phone on charge in another "
    "room, because the check at 11pm is what stretches the hour. If you are not asleep in about "
    "twenty minutes, get up and read somewhere dim until you are sleepy rather than lying there "
    "watching the clock.",
    bias=3,
    avoid=("baby", "babies", "newborn", "infant", "cot", "toddler", "child", "children", "kids",
           "my son", "my daughter", "pregnant", "pregnancy", "shift", "night shift",
           "work nights", "worked nights", "insomnia", "cant sleep", "can't sleep",
           "wake up", "waking", "woke up", "hot", "sweating", "pain", "ache", "snore",
           "snoring", "nap", "naps",
           "wifi", "wi fi", "wi-fi", "internet", "broadband", "router", "connection",
           "phone signal", "mobile signal", "boiler", "heating", "radiator", "radiators",
           "thermostat", "tap", "taps", "drip", "drips", "dripping", "leak", "leaks", "leaking",
           "fridge", "freezer", "washing machine", "washer", "dishwasher", "tumble dryer",
           "oven", "hob", "cooker", "kettle", "telly", "tv", "television", "printer", "laptop",
           "computer", "bulb", "bulbs", "flicker", "flickering", "flickers", "clicking",
           "clicks", "banging", "bangs", "rattling", "rattles", "humming", "hums"),
    ask=("whats a good", "what is a good", "what's a good", "good", "best", "recommend",
         "suggest", "what should i do", "look like", "help me", "give me")))
